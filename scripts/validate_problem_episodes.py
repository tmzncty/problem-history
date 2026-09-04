#!/usr/bin/env python3
"""Validate Problem Episode JSON files and their cross-file references."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable, Sequence

from jsonschema import Draft202012Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = REPO_ROOT / "schemas" / "problem-episode.schema.json"
DEFAULT_FIXTURES = REPO_ROOT / "fixtures" / "problem-episodes"
DIRECT_EVIDENCE_TYPES = frozenset({"quotation", "paraphrase"})

# Match CPython's default integer-string ceiling, but enforce it before
# materializing exponent forms so process-wide settings cannot turn a short
# token such as ``1e100000000`` into an unbounded integer allocation.
_MAX_JSON_INTEGER_DIGITS = 4300


@dataclass(frozen=True)
class EpisodeDocument:
    path: Path
    data: dict[str, Any]


@dataclass(frozen=True)
class EvidenceIndexEntry:
    episode_id: str
    path: Path
    evidence_type: str


class ContractError(Exception):
    """Raised after all discoverable contract violations are collected."""

    def __init__(self, errors: Sequence[str]):
        self.errors = list(errors)
        super().__init__("\n".join(self.errors))


class _DuplicateJsonKeyError(ValueError):
    """Raised when one JSON object declares the same decoded key twice."""


class _NonFiniteJsonConstantError(ValueError):
    """Raised for JavaScript constants that the JSON decoder accepts by default."""


class _InvalidJsonNumberError(ValueError):
    """Raised when an exact JSON number exceeds safe decoder limits."""


def _object_with_unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateJsonKeyError(f"duplicate object key {key!r}")
        value[key] = item
    return value


def _reject_non_finite_constant(value: str) -> None:
    raise _NonFiniteJsonConstantError(
        f"non-finite numeric constant {value!r} is not valid JSON"
    )


def _parse_json_number(value: str) -> int | Decimal:
    """Decode exactly, normalizing mathematical integers within a fixed bound."""

    try:
        exact = Decimal(value)
    except InvalidOperation as error:
        raise _InvalidJsonNumberError("unrepresentable decimal exponent") from error

    if not exact.is_finite():
        raise _InvalidJsonNumberError("non-finite number")
    if exact != exact.to_integral_value():
        return exact

    integer_digits = 1 if exact.is_zero() else exact.adjusted() + 1
    if integer_digits > _MAX_JSON_INTEGER_DIGITS:
        raise _InvalidJsonNumberError(
            f"integer exceeds {_MAX_JSON_INTEGER_DIGITS} decimal digits"
        )
    return int(exact)


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path.resolve())


def discover_json(paths: Iterable[Path]) -> list[Path]:
    discovered: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved.is_dir():
            discovered.update(item.resolve() for item in resolved.rglob("*.json"))
        elif resolved.is_file():
            discovered.add(resolved)
        else:
            raise ContractError([f"{path}: path does not exist"])
    if not discovered:
        raise ContractError(["no JSON documents found"])
    return sorted(discovered)


def _load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_object_with_unique_keys,
            parse_constant=_reject_non_finite_constant,
            parse_float=_parse_json_number,
            parse_int=_parse_json_number,
        )
    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        _DuplicateJsonKeyError,
        _NonFiniteJsonConstantError,
        _InvalidJsonNumberError,
        InvalidOperation,
    ) as exc:
        raise ContractError([f"{_display(path)}: cannot load JSON: {exc}"]) from exc
    if not isinstance(value, dict):
        raise ContractError([f"{_display(path)}: document root must be an object"])
    return value


def _json_path(parts: Iterable[Any]) -> str:
    result = "$"
    for part in parts:
        if isinstance(part, int):
            result += f"[{part}]"
        else:
            result += f".{part}"
    return result


def _duplicates(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    repeated: set[str] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return sorted(repeated)


def _walk(value: Any, path: tuple[Any, ...] = ()) -> Iterable[tuple[tuple[Any, ...], Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _walk(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, path + (index,))


def _collect_key(value: Any, key: str) -> list[str]:
    collected: list[str] = []
    for _, item in _walk(value):
        if isinstance(item, dict) and isinstance(item.get(key), str):
            collected.append(item[key])
    return collected


def _schema_errors(
    validator: Draft202012Validator, document: EpisodeDocument
) -> list[str]:
    errors: list[str] = []
    for error in sorted(
        validator.iter_errors(document.data),
        key=lambda item: tuple(str(part) for part in item.absolute_path),
    ):
        errors.append(
            f"{_display(document.path)}:{_json_path(error.absolute_path)}: {error.message}"
        )
    return errors


def _local_invariants(document: EpisodeDocument) -> list[str]:
    data = document.data
    label = _display(document.path)
    errors: list[str] = []

    period = data.get("period", {})
    start = period.get("start_year")
    end = period.get("end_year")
    # JSON Schema defines "integer" mathematically, so values such as 1880.0
    # or 1.88e3 pass schema validation even though json.loads returns floats.
    if start is not None and end is not None and start > end:
        errors.append(f"{label}:$.period: start_year must not exceed end_year")

    namespaces: dict[str, list[str]] = {
        "actor_id": [item.get("actor_id", "") for item in data.get("actors", [])],
        "institution_id": [
            item.get("institution_id", "") for item in data.get("institutions", [])
        ],
        "formulation_id": [
            item.get("formulation_id", "")
            for item in data.get("formulations", [])
            + data.get("competing_formulations", [])
        ],
        "claim_id": _collect_key(data, "claim_id"),
        "risk_id": _collect_key(data, "risk_id"),
        "source_id": [item.get("source_id", "") for item in data.get("sources", [])],
        "evidence_id": [
            item.get("evidence_id", "") for item in data.get("evidence", [])
        ],
        "relation_id": [
            item.get("relation_id", "") for item in data.get("relations", [])
        ],
    }
    for namespace, values in namespaces.items():
        for repeated in _duplicates(value for value in values if value):
            errors.append(f"{label}: duplicate {namespace} {repeated!r}")

    local_sources = set(namespaces["source_id"])
    for index, evidence in enumerate(data.get("evidence", [])):
        source_id = evidence.get("source_id")
        if source_id not in local_sources:
            errors.append(
                f"{label}:$.evidence[{index}].source_id: unresolved local source {source_id!r}"
            )

    local_actors = set(namespaces["actor_id"])
    formulations = data.get("formulations", []) + data.get(
        "competing_formulations", []
    )
    for index, formulation in enumerate(formulations):
        for actor_id in formulation.get("actor_ids", []):
            if actor_id not in local_actors:
                errors.append(
                    f"{label}: formulation {formulation.get('formulation_id')!r} "
                    f"references unknown actor {actor_id!r}"
                )

    if "fixtures" in document.path.parts and data.get("is_fixture") is not True:
        errors.append(f"{label}: documents under fixtures/ must set is_fixture to true")

    audit = data.get("audit", {})
    if audit.get("record_status") == "reviewed" and not audit.get("reviewed_by"):
        errors.append(f"{label}: reviewed records must name at least one reviewer")

    for index, relation in enumerate(data.get("relations", [])):
        if relation.get("source_episode_id") != data.get("episode_id"):
            errors.append(
                f"{label}:$.relations[{index}].source_episode_id must equal "
                f"the containing episode_id {data.get('episode_id')!r}"
            )
        if relation.get("target_episode_id") == data.get("episode_id"):
            errors.append(f"{label}:$.relations[{index}]: self-relations are not allowed")
        if relation.get("identity_status") == "reviewed" and not relation.get(
            "reviewed_by"
        ):
            errors.append(
                f"{label}:$.relations[{index}]: reviewed relations must name a reviewer"
            )

    return errors


def _corpus_invariants(documents: Sequence[EpisodeDocument]) -> list[str]:
    errors: list[str] = []
    episode_owners: dict[str, Path] = {}
    episode_fixture_status: dict[str, bool] = {}
    evidence_index: dict[str, EvidenceIndexEntry] = {}
    source_owners: dict[str, Path] = {}
    relation_owners: dict[str, Path] = {}

    def register(
        registry: dict[str, Path], identifier: str, path: Path, namespace: str
    ) -> None:
        if identifier in registry:
            errors.append(
                f"{_display(path)}: duplicate corpus {namespace} {identifier!r}; "
                f"first defined in {_display(registry[identifier])}"
            )
        else:
            registry[identifier] = path

    def register_evidence(
        identifier: str, episode_id: str, evidence_type: str, path: Path
    ) -> None:
        if identifier in evidence_index:
            errors.append(
                f"{_display(path)}: duplicate corpus evidence_id {identifier!r}; "
                f"first defined in {_display(evidence_index[identifier].path)}"
            )
        else:
            evidence_index[identifier] = EvidenceIndexEntry(
                episode_id=episode_id,
                path=path,
                evidence_type=evidence_type,
            )

    for document in documents:
        data = document.data
        episode_id = data.get("episode_id")
        if isinstance(episode_id, str):
            is_first_owner = episode_id not in episode_owners
            register(episode_owners, episode_id, document.path, "episode_id")
            if is_first_owner and isinstance(data.get("is_fixture"), bool):
                episode_fixture_status[episode_id] = data["is_fixture"]
        for source in data.get("sources", []):
            source_id = source.get("source_id")
            if isinstance(source_id, str):
                register(source_owners, source_id, document.path, "source_id")
        for evidence in data.get("evidence", []):
            evidence_id = evidence.get("evidence_id")
            evidence_type = evidence.get("evidence_type")
            if (
                isinstance(evidence_id, str)
                and isinstance(episode_id, str)
                and isinstance(evidence_type, str)
            ):
                register_evidence(
                    evidence_id, episode_id, evidence_type, document.path
                )
        for relation in data.get("relations", []):
            relation_id = relation.get("relation_id")
            if isinstance(relation_id, str):
                register(relation_owners, relation_id, document.path, "relation_id")

    def has_direct_evidence(evidence_ids: Iterable[str]) -> bool:
        for evidence_id in evidence_ids:
            entry = evidence_index.get(evidence_id)
            if entry is not None and entry.evidence_type in DIRECT_EVIDENCE_TYPES:
                return True
        return False

    for document in documents:
        label = _display(document.path)
        for path, value in _walk(document.data):
            if (
                not path
                or path[-1] not in {"evidence_ids", "counterevidence_ids"}
                or not isinstance(value, list)
            ):
                continue
            for evidence_id in value:
                entry = evidence_index.get(evidence_id)
                if entry is None:
                    errors.append(
                        f"{label}:{_json_path(path)}: unresolved evidence {evidence_id!r}"
                    )
                elif len(path) > 1 and path[0] == "relations":
                    relation = document.data["relations"][path[1]]
                    source = relation.get("source_episode_id")
                    target = relation.get("target_episode_id")
                    if entry.episode_id not in {source, target}:
                        errors.append(
                            f"{label}:{_json_path(path)}: relation references evidence "
                            f"{evidence_id!r} owned by episode {entry.episode_id!r}; "
                            f"expected source/target {source!r} or {target!r}"
                        )
                elif entry.path != document.path:
                    errors.append(
                        f"{label}:{_json_path(path)}: non-relation field references "
                        f"evidence {evidence_id!r} owned by {_display(entry.path)}"
                    )

        for collection in ("formulations", "competing_formulations"):
            for index, formulation in enumerate(document.data.get(collection, [])):
                if formulation.get("source_type") != "actor_explicit":
                    continue
                if not has_direct_evidence(formulation.get("evidence_ids", [])):
                    errors.append(
                        f"{label}:$.{collection}[{index}].evidence_ids: "
                        "actor_explicit formulation must reference at least one "
                        "quotation or paraphrase"
                    )

        answer_space = document.data.get("answer_space", {})
        for collection in ("accepted", "marginal", "unthinkable_or_impossible"):
            for index, answer in enumerate(answer_space.get(collection, [])):
                if answer.get("epistemic_status") != "actor_explicit":
                    continue
                if not has_direct_evidence(answer.get("evidence_ids", [])):
                    errors.append(
                        f"{label}:$.answer_space.{collection}[{index}].evidence_ids: "
                        "actor_explicit answer must reference at least one quotation "
                        "or paraphrase"
                    )

        for index, relation in enumerate(document.data.get("relations", [])):
            target = relation.get("target_episode_id")
            if target not in episode_owners:
                errors.append(
                    f"{label}:$.relations[{index}].target_episode_id: "
                    f"unresolved episode {target!r}"
                )
                continue

            source_is_fixture = document.data.get("is_fixture")
            target_is_fixture = episode_fixture_status.get(target)
            if (
                isinstance(source_is_fixture, bool)
                and isinstance(target_is_fixture, bool)
                and source_is_fixture != target_is_fixture
            ):
                errors.append(
                    f"{label}:$.relations[{index}].target_episode_id: "
                    "relations cannot cross the fixture boundary; "
                    f"source is_fixture={str(source_is_fixture).lower()}, "
                    f"target is_fixture={str(target_is_fixture).lower()}"
                )

    return errors


def validate_documents(schema_path: Path, document_paths: Sequence[Path]) -> dict[str, int]:
    schema = _load_object(schema_path.resolve())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )

    documents: list[EpisodeDocument] = []
    load_errors: list[str] = []
    for path in document_paths:
        try:
            documents.append(EpisodeDocument(path=path, data=_load_object(path)))
        except ContractError as exc:
            load_errors.extend(exc.errors)
    if load_errors:
        raise ContractError(load_errors)

    schema_errors: list[str] = []
    for document in documents:
        schema_errors.extend(_schema_errors(validator, document))
    if schema_errors:
        raise ContractError(sorted(set(schema_errors)))

    errors: list[str] = []
    for document in documents:
        errors.extend(_local_invariants(document))
    errors.extend(_corpus_invariants(documents))
    if errors:
        raise ContractError(sorted(set(errors)))

    return {
        "documents": len(documents),
        "sources": sum(len(item.data.get("sources", [])) for item in documents),
        "evidence": sum(len(item.data.get("evidence", [])) for item in documents),
        "relations": sum(len(item.data.get("relations", [])) for item in documents),
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Problem Episode JSON and cross-file references."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[DEFAULT_FIXTURES],
        help="JSON file or directory (default: fixtures/problem-episodes)",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Draft 2020-12 schema path",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        paths = discover_json(args.paths)
        counts = validate_documents(args.schema, paths)
    except ContractError as exc:
        for error in exc.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    except Exception as exc:  # schema errors should still be actionable at the CLI
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        "validated "
        f"{counts['documents']} episodes, {counts['sources']} sources, "
        f"{counts['evidence']} evidence records, and {counts['relations']} relations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
