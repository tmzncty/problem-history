#!/usr/bin/env python3
"""Validate stable IDs and graph references in Markdown Problem Episodes."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STUDIES = REPO_ROOT / "studies"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FENCE_OPEN_RE = re.compile(
    r"^(?P<indent> {0,3})(?P<marker>`{3,}|~{3,})(?P<info>[^\r\n]*)$"
)
MARKDOWN_LINE_END_RE = re.compile(r"\r\n|\r|\n")
TOP_LEVEL_KEY_RE = re.compile(
    r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?P<value>(?:[ \t]+.*)?)$"
)
RELATIONS_DECLARATION_RE = re.compile(r"^relations:(?:[ \t]+(?:\[\][ \t]*)?(?:#.*)?|)$")
EMPTY_RELATIONS_DECLARATION_RE = re.compile(r"^relations:[ \t]+\[\][ \t]*(?:#.*)?$")
RELATION_TYPES = (
    "continuous",
    "reformulated",
    "transformed_successor",
    "split",
    "merged",
    "displaced",
    "revived",
    "analogy_only",
    "unrelated",
    "undetermined",
)
RELATION_CONFIDENCES = ("low", "medium", "high")


@dataclass(frozen=True)
class YamlBlock:
    lines: tuple[str, ...]
    start_line: int


@dataclass(frozen=True)
class Episode:
    path: Path
    episode_id: str
    predecessor: str | None
    relation_type: str | None


@dataclass(frozen=True)
class Relation:
    path: Path
    line_number: int
    source: str
    target: str
    relation_type: str
    confidence: str


class ReferenceError(Exception):
    def __init__(self, errors: Iterable[str]):
        self.errors = tuple(sorted(set(errors)))
        super().__init__("\n".join(self.errors))


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _yaml_blocks(text: str) -> tuple[list[YamlBlock], str | None]:
    """Return actual YAML fences, ignoring fence-looking text inside other fences."""

    blocks: list[YamlBlock] = []
    active_marker: str | None = None
    active_length = 0
    active_indent = 0
    active_yaml = False
    active_start = 0
    active_lines: list[str] = []

    for line_number, line in enumerate(MARKDOWN_LINE_END_RE.split(text), start=1):
        if active_marker is None:
            match = FENCE_OPEN_RE.match(line)
            if match is None:
                continue
            marker = match.group("marker")
            raw_info = match.group("info")
            # GFM treats backticks in a backtick fence's info as plain text.
            if marker[0] == "`" and "`" in raw_info:
                continue
            info = raw_info.strip(" \t").lower()
            active_marker = marker[0]
            active_length = len(marker)
            active_indent = len(match.group("indent"))
            active_yaml = info == "yaml"
            active_start = line_number
            active_lines = []
            continue

        closer = re.fullmatch(
            rf" {{0,3}}{re.escape(active_marker)}{{{active_length},}}[ \t]*", line
        )
        if closer is not None:
            if active_yaml:
                blocks.append(YamlBlock(tuple(active_lines), active_start + 1))
            active_marker = None
            active_length = 0
            active_indent = 0
            active_yaml = False
            active_start = 0
            active_lines = []
        elif active_yaml:
            leading_spaces = len(line) - len(line.lstrip(" "))
            active_lines.append(line[min(active_indent, leading_spaces) :])

    if active_marker is not None and active_yaml:
        return blocks, f"unclosed YAML fence opened at line {active_start}"
    return blocks, None


def _decode_scalar(raw: str, *, label: str) -> str:
    value = raw.strip(" \t")
    if not value:
        raise ValueError(f"{label} must have a scalar value")

    if value.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'(?:[ \t]+#.*)?", value)
        if match is None:
            raise ValueError(f"{label} has malformed single-quoted YAML")
        return match.group(1).replace("''", "'")

    if value.startswith('"'):
        try:
            decoded, end = json.JSONDecoder().raw_decode(value)
        except json.JSONDecodeError as error:
            raise ValueError(f"{label} has malformed double-quoted YAML") from error
        remainder = value[end:]
        if not re.fullmatch(r"[ \t]*|[ \t]+#.*", remainder):
            raise ValueError(f"{label} has trailing content after its scalar")
        if not isinstance(decoded, str):
            raise ValueError(f"{label} must be a string")
        return decoded

    value = re.split(r"[ \t]+#", value, maxsplit=1)[0].rstrip(" \t")
    if not value:
        raise ValueError(f"{label} must have a scalar value")
    return value


def _top_level_mapping_entries(
    block: YamlBlock,
    *,
    label: str,
    single_line_keys: frozenset[str] = frozenset(),
) -> tuple[list[tuple[str, str, int]], list[str]]:
    entries: list[tuple[str, str, int]] = []
    errors: list[str] = []
    active_single_line_key: str | None = None
    for offset, line in enumerate(block.lines):
        line_number = block.start_line + offset
        if not line.strip(" \t") or line.lstrip(" \t").startswith("#"):
            continue
        if line.startswith(" "):
            if active_single_line_key is not None:
                errors.append(
                    f"{label}:{line_number}: {active_single_line_key} must be "
                    "a single-line scalar"
                )
                active_single_line_key = None
            continue
        match = TOP_LEVEL_KEY_RE.fullmatch(line)
        if match is None:
            active_single_line_key = None
            errors.append(
                f"{label}:{line_number}: top-level YAML metadata must use "
                "ASCII plain keys with SP/TAB separation after ':'"
            )
            continue
        key = match.group("key")
        entries.append((key, match.group("value"), line_number))
        active_single_line_key = key if key in single_line_keys else None
    return entries, errors


def _slug(raw: str, *, label: str) -> str:
    value = _decode_scalar(raw, label=label)
    if SLUG_RE.fullmatch(value) is None:
        raise ValueError(f"{label} must be a lowercase hyphenated slug, got {value!r}")
    return value


def _enum_scalar(raw: str, *, label: str, choices: tuple[str, ...]) -> str:
    value = _decode_scalar(raw, label=label)
    if value not in choices:
        expected = ", ".join(repr(choice) for choice in choices)
        raise ValueError(f"{label} must be one of {expected}, got {value!r}")
    return value


def _parse_episode(path: Path) -> tuple[Episode | None, list[str]]:
    errors: list[str] = []
    label = _display(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return None, [f"{label}: cannot read UTF-8 Markdown: {error}"]

    blocks, fence_error = _yaml_blocks(text)
    if fence_error is not None:
        errors.append(f"{label}: {fence_error}")
    if not blocks:
        errors.append(f"{label}: missing fenced YAML episode metadata")
        return None, errors

    entries, entry_errors = _top_level_mapping_entries(
        blocks[0],
        label=label,
        single_line_keys=frozenset({"episode_id", "predecessor", "relation"}),
    )
    errors.extend(entry_errors)
    values: dict[str, tuple[str, int]] = {}
    for key, value, line_number in entries:
        if key not in {"episode_id", "predecessor", "relation"}:
            continue
        if key in values:
            errors.append(f"{label}:{line_number}: duplicate metadata key {key!r}")
            continue
        values[key] = (value, line_number)

    if "episode_id" not in values:
        errors.append(f"{label}: first YAML block is missing episode_id")
        return None, errors

    if ("predecessor" in values) != ("relation" in values):
        present, required = (
            ("predecessor", "relation")
            if "predecessor" in values
            else ("relation", "predecessor")
        )
        errors.append(f"{label}: {present} requires {required}")

    identifiers: dict[str, str] = {}
    for key in ("episode_id", "predecessor"):
        if key not in values:
            continue
        raw, line_number = values[key]
        try:
            identifiers[key] = _slug(raw, label=f"{label}:{line_number}: {key}")
        except ValueError as error:
            errors.append(str(error))

    relation_type: str | None = None
    if "relation" in values:
        raw, line_number = values["relation"]
        try:
            relation_type = _enum_scalar(
                raw,
                label=f"{label}:{line_number}: relation",
                choices=RELATION_TYPES,
            )
        except ValueError as error:
            errors.append(str(error))

    if "episode_id" not in identifiers:
        return None, errors
    return (
        Episode(
            path,
            identifiers["episode_id"],
            identifiers.get("predecessor"),
            relation_type,
        ),
        errors,
    )


def _relation_block(path: Path) -> tuple[YamlBlock | None, list[str]]:
    label = _display(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        return None, [f"{label}: cannot read UTF-8 Markdown: {error}"]

    blocks, fence_error = _yaml_blocks(text)
    errors = [f"{label}: {fence_error}"] if fence_error is not None else []
    candidates = [
        (block, index)
        for block in blocks
        for index, line in enumerate(block.lines)
        if RELATIONS_DECLARATION_RE.fullmatch(line)
    ]
    if not candidates:
        errors.append(f"{label}: missing top-level relations YAML block")
        return None, errors
    if len(candidates) > 1:
        errors.append(f"{label}: multiple relations declarations are ambiguous")
        return None, errors
    _, entry_errors = _top_level_mapping_entries(candidates[0][0], label=label)
    errors.extend(entry_errors)
    return candidates[0][0], errors


def _parse_relations(path: Path) -> tuple[list[Relation], list[str]]:
    block, errors = _relation_block(path)
    if block is None:
        return [], errors

    label = _display(path)
    relation_start = next(
        index
        for index, line in enumerate(block.lines)
        if RELATIONS_DECLARATION_RE.fullmatch(line)
    )
    declaration = block.lines[relation_start]
    if EMPTY_RELATIONS_DECLARATION_RE.fullmatch(declaration):
        for offset, line in enumerate(
            block.lines[relation_start + 1 :], start=relation_start + 1
        ):
            if not line.strip(" \t") or line.lstrip(" \t").startswith("#"):
                continue
            if len(line) == len(line.lstrip(" \t")):
                break
            errors.append(
                f"{label}:{block.start_line + offset}: relations: [] cannot "
                "contain nested items"
            )
            break
        return [], errors
    items: list[tuple[int, dict[str, tuple[str, int]]]] = []
    current: dict[str, tuple[str, int]] | None = None
    list_indent: int | None = None
    field_indent: int | None = None

    def parse_field(content: str, line_number: int) -> None:
        nonlocal current
        if current is None:
            errors.append(
                f"{label}:{line_number}: relation field appears before a list item"
            )
            return
        match = TOP_LEVEL_KEY_RE.match(content)
        if match is None:
            errors.append(f"{label}:{line_number}: malformed relation mapping")
            return
        key = match.group("key")
        if key not in {"from", "to", "type", "confidence"}:
            return
        if key in current:
            errors.append(f"{label}:{line_number}: duplicate relation key {key!r}")
            return
        current[key] = (match.group("value"), line_number)

    for offset, line in enumerate(
        block.lines[relation_start + 1 :], start=relation_start + 1
    ):
        line_number = block.start_line + offset
        if not line.strip(" \t") or line.lstrip(" \t").startswith("#"):
            continue
        if "\t" in line[: len(line) - len(line.lstrip(" \t"))]:
            errors.append(
                f"{label}:{line_number}: tabs are not allowed in relation indentation"
            )
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == 0:
            break

        item = re.fullmatch(r"( *)-(?:[ \t]+(.*))?", line)
        if item is not None:
            indent = len(item.group(1))
            if list_indent is None:
                list_indent = indent
                field_indent = indent + 2
            elif indent != list_indent:
                errors.append(
                    f"{label}:{line_number}: inconsistent relation list indentation"
                )
            current = {}
            items.append((line_number, current))
            if item.group(2):
                parse_field(item.group(2), line_number)
            continue

        if current is None or field_indent is None or indent != field_indent:
            errors.append(f"{label}:{line_number}: malformed relation indentation")
            continue
        parse_field(line[indent:], line_number)

    relations: list[Relation] = []
    for item_line, fields in items:
        missing = sorted({"from", "to", "type", "confidence"} - fields.keys())
        if missing:
            errors.append(
                f"{label}:{item_line}: relation is missing {', '.join(missing)}"
            )
            continue
        try:
            source = _slug(
                fields["from"][0], label=f"{label}:{fields['from'][1]}: relation from"
            )
            target = _slug(
                fields["to"][0], label=f"{label}:{fields['to'][1]}: relation to"
            )
            relation_type = _enum_scalar(
                fields["type"][0],
                label=f"{label}:{fields['type'][1]}: relation type",
                choices=RELATION_TYPES,
            )
            confidence = _enum_scalar(
                fields["confidence"][0],
                label=f"{label}:{fields['confidence'][1]}: relation confidence",
                choices=RELATION_CONFIDENCES,
            )
        except ValueError as error:
            errors.append(str(error))
            continue
        relations.append(
            Relation(path, item_line, source, target, relation_type, confidence)
        )

    if not items:
        errors.append(f"{label}: relations block contains no list items")
    return relations, errors


def discover_episode_paths(studies_root: Path) -> list[Path]:
    return sorted(
        (path for path in studies_root.glob("*/episodes/*.md") if path.is_file()),
        key=lambda path: path.as_posix(),
    )


def _predecessor_cycles(
    predecessors: dict[str, str],
) -> list[tuple[str, ...]]:
    """Return each cycle once while following episode-to-predecessor pointers."""

    cycles: list[tuple[str, ...]] = []
    finished: set[str] = set()
    for start in sorted(predecessors):
        if start in finished:
            continue

        chain: list[str] = []
        positions: dict[str, int] = {}
        current = start
        while current in predecessors and current not in finished:
            if current in positions:
                cycle = chain[positions[current] :] + [current]
                cycles.append(tuple(cycle))
                break
            positions[current] = len(chain)
            chain.append(current)
            current = predecessors[current]
        finished.update(chain)

    return cycles


def validate_studies(studies_root: Path = DEFAULT_STUDIES) -> dict[str, int]:
    paths = discover_episode_paths(studies_root)
    if not paths:
        raise ReferenceError([f"{_display(studies_root)}: no Markdown episodes found"])

    errors: list[str] = []
    episodes: list[Episode] = []
    for path in paths:
        episode, episode_errors = _parse_episode(path)
        errors.extend(episode_errors)
        if episode is not None:
            episodes.append(episode)

    owners: dict[str, Path] = {}
    for episode in episodes:
        if episode.episode_id in owners:
            errors.append(
                f"{_display(episode.path)}: duplicate episode_id {episode.episode_id!r}; "
                f"first defined in {_display(owners[episode.episode_id])}"
            )
        else:
            owners[episode.episode_id] = episode.path

    readmes = sorted(
        {path.parent.parent / "README.md" for path in paths},
        key=lambda path: path.as_posix(),
    )
    relations: list[Relation] = []
    for readme in readmes:
        if not readme.is_file():
            errors.append(f"{_display(readme)}: study README is missing")
            continue
        parsed, relation_errors = _parse_relations(readme)
        relations.extend(parsed)
        errors.extend(relation_errors)

    edges: dict[tuple[str, str], Relation] = {}
    for relation in relations:
        edge = (relation.source, relation.target)
        if relation.source not in owners:
            errors.append(
                f"{_display(relation.path)}:{relation.line_number}: relation from "
                f"references unknown episode {relation.source!r}"
            )
        if relation.target not in owners:
            errors.append(
                f"{_display(relation.path)}:{relation.line_number}: relation to "
                f"references unknown episode {relation.target!r}"
            )
        if relation.source == relation.target:
            errors.append(
                f"{_display(relation.path)}:{relation.line_number}: self-relations are not allowed"
            )
        if edge in edges:
            first = edges[edge]
            errors.append(
                f"{_display(relation.path)}:{relation.line_number}: duplicate relation "
                f"{relation.source!r} -> {relation.target!r}; first defined at "
                f"{_display(first.path)}:{first.line_number}"
            )
        else:
            edges[edge] = relation

    for episode in episodes:
        predecessor = episode.predecessor
        if predecessor is None:
            continue
        if predecessor not in owners:
            errors.append(
                f"{_display(episode.path)}: predecessor references unknown episode "
                f"{predecessor!r}"
            )
        if predecessor == episode.episode_id:
            errors.append(f"{_display(episode.path)}: an episode cannot precede itself")
        edge = edges.get((predecessor, episode.episode_id))
        if edge is None:
            errors.append(
                f"{_display(episode.path)}: predecessor {predecessor!r} is not backed "
                "by a README relation"
            )
        elif (
            episode.relation_type is not None
            and episode.relation_type != edge.relation_type
        ):
            errors.append(
                f"{_display(episode.path)}: episode relation "
                f"{episode.relation_type!r} does not match README relation type "
                f"{edge.relation_type!r} at "
                f"{_display(edge.path)}:{edge.line_number}"
            )

    primary_predecessors: dict[str, str] = {}
    for episode in episodes:
        predecessor = episode.predecessor
        if (
            predecessor is not None
            and predecessor in owners
            and predecessor != episode.episode_id
            and owners.get(episode.episode_id) == episode.path
        ):
            primary_predecessors[episode.episode_id] = predecessor

    for cycle in _predecessor_cycles(primary_predecessors):
        rendered = " -> ".join(repr(episode_id) for episode_id in cycle)
        errors.append(
            f"{_display(owners[cycle[0]])}: predecessor cycle is not allowed: "
            f"{rendered}"
        )

    if errors:
        raise ReferenceError(errors)
    return {"episodes": len(episodes), "relations": len(relations)}


def main() -> int:
    try:
        counts = validate_studies()
    except ReferenceError as error:
        for message in error.errors:
            print(f"ERROR: {message}", file=sys.stderr)
        return 1
    print(
        f"validated {counts['episodes']} Markdown episodes and "
        f"{counts['relations']} relations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
