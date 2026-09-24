from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_markdown_episode_refs import (
    ReferenceError,
    validate_studies,
)  # noqa: E402


def episode(
    episode_id: str | None,
    predecessor: str | None = None,
    *,
    relation_type: str = "transformed_successor",
    fence_indent: int = 0,
    fence_marker: str = "```",
) -> str:
    fields = []
    if episode_id is not None:
        fields.append(f"episode_id: {episode_id}")
    fields.extend(["problem_id: fixture", "period: 1950", "status: active"])
    if predecessor is not None:
        fields.extend([f"predecessor: {predecessor}", f"relation: {relation_type}"])
    indent = " " * fence_indent
    content = "\n".join(f"{indent}{field}" for field in fields)
    return (
        f"# Fixture\n\n{indent}{fence_marker}yaml\n"
        f"{content}\n{indent}{fence_marker}\n"
    )


def readme(
    relations: list[tuple[str, str]],
    *,
    fence_indent: int = 0,
    fence_marker: str = "```",
) -> str:
    declaration = "relations:" if relations else "relations: []"
    indent = " " * fence_indent
    lines = ["# Fixture study", "", f"{indent}{fence_marker}yaml", declaration]
    for source, target in relations:
        lines.extend(
            [
                f"  - from: {source}",
                f"    to: {target}",
                "    type: transformed_successor",
                "    confidence: medium",
            ]
        )
    lines[3:] = [f"{indent}{line}" for line in lines[3:]]
    return "\n".join(lines + [f"{indent}{fence_marker}", ""])


class MarkdownEpisodeReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.studies = Path(self.temporary.name) / "studies"
        self.study = self.studies / "fixture-study"
        (self.study / "episodes").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def write(self, relative: str, content: str) -> None:
        (self.study / relative).write_text(content, encoding="utf-8")

    def valid_graph(
        self, names: tuple[str, str] = ("01_first.md", "02_second.md")
    ) -> None:
        self.write(f"episodes/{names[0]}", episode("first"))
        self.write(f"episodes/{names[1]}", episode("second", "first"))
        self.write("README.md", readme([("first", "second")]))

    def test_checked_in_study_is_valid(self) -> None:
        counts = validate_studies(REPO_ROOT / "studies")
        self.assertEqual(counts, {"episodes": 3, "relations": 2})

    def test_file_names_do_not_define_episode_identity(self) -> None:
        self.valid_graph(("renamed-later.md", "unrelated-file-name.md"))
        self.assertEqual(validate_studies(self.studies)["relations"], 1)

    def test_missing_episode_id_is_rejected(self) -> None:
        self.write("episodes/missing.md", episode(None))
        self.write("README.md", readme([]))
        with self.assertRaisesRegex(ReferenceError, "missing episode_id"):
            validate_studies(self.studies)

    def test_duplicate_episode_id_is_rejected(self) -> None:
        self.write("episodes/one.md", episode("same"))
        self.write("episodes/two.md", episode("same"))
        self.write("README.md", readme([]))
        with self.assertRaisesRegex(ReferenceError, "duplicate episode_id"):
            validate_studies(self.studies)

    def test_duplicate_metadata_key_is_rejected(self) -> None:
        duplicate = episode("first").replace(
            "episode_id: first", "episode_id: first\nepisode_id: second"
        )
        self.write("episodes/one.md", duplicate)
        self.write("README.md", readme([]))
        with self.assertRaisesRegex(ReferenceError, "duplicate metadata key"):
            validate_studies(self.studies)

    def test_metadata_keys_require_plain_separated_yaml(self) -> None:
        invalid_lines = {
            "compact": "episode_id:one",
            "non-breaking separation": "episode_id:\u00a0one",
            "quoted duplicate": 'episode_id: one\n"episode_id": two',
            "single-quoted duplicate": "episode_id: one\n'episode_id': two",
        }
        self.write("README.md", readme([]))
        for name, metadata in invalid_lines.items():
            with self.subTest(name=name):
                document = f"# Fixture\n\n```yaml\n{metadata}\n```\n"
                self.write("episodes/one.md", document)
                with self.assertRaises(ReferenceError):
                    validate_studies(self.studies)

    def test_unicode_whitespace_is_not_trimmed_from_slugs(self) -> None:
        self.write("README.md", readme([]))
        for name, value in {
            "leading NBSP": "\u00a0one",
            "trailing NBSP": "one\u00a0",
            "leading em space": "\u2003one",
            "trailing em space": "one\u2003",
        }.items():
            with self.subTest(name=name):
                self.write("episodes/one.md", episode(value))
                with self.assertRaisesRegex(
                    ReferenceError, "lowercase hyphenated slug"
                ):
                    validate_studies(self.studies)

    def test_identity_scalars_cannot_continue_on_indented_lines(self) -> None:
        self.write("README.md", readme([]))
        continued_id = episode("one").replace(
            "episode_id: one", "episode_id: one\n  suffix"
        )
        self.write("episodes/one.md", continued_id)
        with self.assertRaisesRegex(ReferenceError, "episode_id must be a single-line"):
            validate_studies(self.studies)

        self.write("episodes/one.md", episode("one"))
        continued_predecessor = episode("two", "one").replace(
            "predecessor: one", "predecessor: one\n  suffix"
        )
        self.write("episodes/two.md", continued_predecessor)
        self.write("README.md", readme([("one", "two")]))
        with self.assertRaisesRegex(
            ReferenceError, "predecessor must be a single-line"
        ):
            validate_studies(self.studies)

        continued_relation = episode("two", "one").replace(
            "relation: transformed_successor",
            "relation: transformed_successor\n  suffix",
        )
        self.write("episodes/two.md", continued_relation)
        with self.assertRaisesRegex(ReferenceError, "relation must be a single-line"):
            validate_studies(self.studies)

    def test_unresolved_predecessor_is_rejected(self) -> None:
        self.write("episodes/one.md", episode("one", "missing"))
        self.write("README.md", readme([]))
        with self.assertRaisesRegex(ReferenceError, "predecessor references unknown"):
            validate_studies(self.studies)

    def test_predecessor_must_have_a_readme_relation(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("episodes/two.md", episode("two", "one"))
        self.write("README.md", readme([]))
        with self.assertRaisesRegex(ReferenceError, "not backed by a README relation"):
            validate_studies(self.studies)

    def test_predecessor_requires_an_episode_relation(self) -> None:
        self.write("episodes/one.md", episode("one"))
        missing_relation = episode("two", "one").replace(
            "relation: transformed_successor\n", ""
        )
        self.write("episodes/two.md", missing_relation)
        self.write("README.md", readme([("one", "two")]))
        with self.assertRaisesRegex(ReferenceError, "predecessor requires relation"):
            validate_studies(self.studies)

    def test_episode_relation_requires_a_predecessor(self) -> None:
        orphan_relation = episode("one").replace(
            "status: active", "status: active\nrelation: continuous"
        )
        self.write("episodes/one.md", orphan_relation)
        self.write("README.md", readme([]))
        with self.assertRaisesRegex(ReferenceError, "relation requires predecessor"):
            validate_studies(self.studies)

    def test_episode_relation_must_match_the_readme_edge_type(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write(
            "episodes/two.md",
            episode("two", "one", relation_type="continuous"),
        )
        self.write("README.md", readme([("one", "two")]))
        with self.assertRaisesRegex(
            ReferenceError, "does not match README relation type"
        ):
            validate_studies(self.studies)

    def test_readme_edges_do_not_force_a_single_episode_predecessor(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("episodes/two.md", episode("two"))
        self.write("README.md", readme([("one", "two")]))
        self.assertEqual(validate_studies(self.studies)["relations"], 1)

    def test_primary_predecessor_cycles_are_rejected(self) -> None:
        cases = {
            "two nodes": (
                {
                    "one": "two",
                    "two": "one",
                },
                "'one' -> 'two' -> 'one'",
            ),
            "three nodes": (
                {
                    "one": "three",
                    "two": "one",
                    "three": "two",
                },
                "'one' -> 'three' -> 'two' -> 'one'",
            ),
        }
        for name, (predecessors, expected_cycle) in cases.items():
            with self.subTest(name=name):
                for episode_id, predecessor in predecessors.items():
                    self.write(
                        f"episodes/{episode_id}.md",
                        episode(episode_id, predecessor),
                    )
                self.write(
                    "README.md",
                    readme(
                        [
                            (predecessor, episode_id)
                            for episode_id, predecessor in predecessors.items()
                        ]
                    ),
                )
                with self.assertRaisesRegex(
                    ReferenceError,
                    f"predecessor cycle is not allowed: {expected_cycle}",
                ):
                    validate_studies(self.studies)

    def test_readme_only_analogy_cycle_remains_valid(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("episodes/two.md", episode("two"))
        graph = readme([("one", "two"), ("two", "one")]).replace(
            "type: transformed_successor", "type: analogy_only"
        )
        self.write("README.md", graph)
        self.assertEqual(
            validate_studies(self.studies), {"episodes": 2, "relations": 2}
        )

    def test_episode_relation_uses_the_contract_enum(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write(
            "episodes/two.md",
            episode("two", "one", relation_type="same_problem"),
        )
        self.write("README.md", readme([("one", "two")]))
        with self.assertRaisesRegex(ReferenceError, "relation must be one of"):
            validate_studies(self.studies)

    def test_duplicate_episode_relation_is_rejected(self) -> None:
        self.write("episodes/one.md", episode("one"))
        duplicate = episode("two", "one").replace(
            "relation: transformed_successor",
            "relation: transformed_successor\nrelation: continuous",
        )
        self.write("episodes/two.md", duplicate)
        self.write("README.md", readme([("one", "two")]))
        with self.assertRaisesRegex(
            ReferenceError, "duplicate metadata key 'relation'"
        ):
            validate_studies(self.studies)

    def test_unresolved_readme_endpoints_are_rejected(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("README.md", readme([("missing", "one"), ("one", "absent")]))
        with self.assertRaises(ReferenceError) as context:
            validate_studies(self.studies)
        message = str(context.exception)
        self.assertIn("relation from references unknown episode 'missing'", message)
        self.assertIn("relation to references unknown episode 'absent'", message)

    def test_duplicate_and_self_relations_are_rejected(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("README.md", readme([("one", "one"), ("one", "one")]))
        with self.assertRaises(ReferenceError) as context:
            validate_studies(self.studies)
        message = str(context.exception)
        self.assertIn("self-relations are not allowed", message)
        self.assertIn("duplicate relation", message)

    def test_duplicate_or_conflicting_relations_declarations_are_rejected(self) -> None:
        self.write("episodes/one.md", episode("one"))
        duplicate = readme([]).replace("relations: []", "relations: []\nrelations: []")
        self.write("README.md", duplicate)
        with self.assertRaisesRegex(ReferenceError, "multiple relations declarations"):
            validate_studies(self.studies)

        nested = readme([]).replace(
            "relations: []", "relations: []\n  - from: one\n    to: one"
        )
        self.write("README.md", nested)
        with self.assertRaisesRegex(ReferenceError, "cannot contain nested items"):
            validate_studies(self.studies)

        quoted = readme([]).replace(
            "relations: []", 'relations: []\n"relations":\n  - from: ghost\n    to: one'
        )
        self.write("README.md", quoted)
        with self.assertRaisesRegex(ReferenceError, "ASCII plain keys"):
            validate_studies(self.studies)

    def test_relation_fields_require_plain_separated_yaml(self) -> None:
        self.write("episodes/one.md", episode("one"))
        for name, source_line in {
            "compact field": "  - from:one\n    to: one",
            "quoted field": '  - "from": one\n    to: one',
            "unicode endpoint": "  - from: one\u00a0\n    to: one",
        }.items():
            with self.subTest(name=name):
                graph = (
                    "# Fixture study\n\n```yaml\nrelations:\n" + source_line + "\n```\n"
                )
                self.write("README.md", graph)
                with self.assertRaises(ReferenceError):
                    validate_studies(self.studies)

    def test_relations_require_type_and_confidence(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("episodes/two.md", episode("two", "one"))
        graph = readme([("one", "two")])
        for field, declaration in {
            "type": "    type: transformed_successor\n",
            "confidence": "    confidence: medium\n",
        }.items():
            with self.subTest(field=field):
                self.write("README.md", graph.replace(declaration, ""))
                with self.assertRaisesRegex(
                    ReferenceError, rf"relation is missing {field}"
                ):
                    validate_studies(self.studies)

    def test_relation_type_and_confidence_use_contract_enums(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("episodes/two.md", episode("two", "one"))
        graph = readme([("one", "two")])
        cases = {
            "unknown type": (
                graph.replace(
                    "type: transformed_successor", "type: definitely-not-a-relation"
                ),
                "relation type must be one of",
            ),
            "unknown confidence": (
                graph.replace("confidence: medium", "confidence: impossible"),
                "relation confidence must be one of",
            ),
        }
        for name, (document, message) in cases.items():
            with self.subTest(name=name):
                self.write("README.md", document)
                with self.assertRaisesRegex(ReferenceError, message):
                    validate_studies(self.studies)

    def test_documented_relation_metadata_values_are_supported(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("episodes/two.md", episode("two", "one"))
        graph = readme([("one", "two")])
        for relation_type in (
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
        ):
            with self.subTest(relation_type=relation_type):
                self.write(
                    "episodes/two.md",
                    episode("two", "one", relation_type=relation_type),
                )
                document = graph.replace(
                    "type: transformed_successor", f"type: {relation_type}"
                )
                self.write("README.md", document)
                self.assertEqual(validate_studies(self.studies)["relations"], 1)

        self.write("episodes/two.md", episode("two", "one"))
        for confidence in ("low", "medium", "high"):
            with self.subTest(confidence=confidence):
                document = graph.replace(
                    "confidence: medium", f"confidence: {confidence}"
                )
                self.write("README.md", document)
                self.assertEqual(validate_studies(self.studies)["relations"], 1)

    def test_duplicate_relation_fields_are_rejected(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("episodes/two.md", episode("two", "one"))
        graph = readme([("one", "two")])
        for field, (declaration, duplicate_declaration) in {
            "from": ("  - from: one", "    from: one"),
            "to": ("    to: two", "    to: two"),
            "type": (
                "    type: transformed_successor",
                "    type: transformed_successor",
            ),
            "confidence": ("    confidence: medium", "    confidence: medium"),
        }.items():
            with self.subTest(field=field):
                duplicate = graph.replace(
                    declaration, f"{declaration}\n{duplicate_declaration}"
                )
                self.write("README.md", duplicate)
                with self.assertRaisesRegex(
                    ReferenceError, rf"duplicate relation key '{field}'"
                ):
                    validate_studies(self.studies)

    def test_unknown_relation_fields_remain_outside_the_narrow_contract(self) -> None:
        self.write("episodes/one.md", episode("one"))
        self.write("episodes/two.md", episode("two", "one"))
        graph = readme([("one", "two")]).replace(
            "    confidence: medium",
            "    confidence: medium\n    review_status: provisional",
        )
        self.write("README.md", graph)
        self.assertEqual(validate_studies(self.studies)["relations"], 1)

    def test_quoted_slug_values_and_crlf_are_supported(self) -> None:
        first = episode('"first"').replace("\n", "\r\n")
        second = episode(
            "'second'",
            '"first"',
            relation_type="'transformed_successor'",
        ).replace("\n", "\r\n")
        graph = readme([("'first'", '"second"')]).replace("\n", "\r\n")
        self.write("episodes/one.md", first)
        self.write("episodes/two.md", second)
        self.write("README.md", graph)
        self.assertEqual(validate_studies(self.studies)["episodes"], 2)

    def test_yaml_looking_text_inside_an_outer_fence_is_ignored(self) -> None:
        disguised = (
            "# Fixture\n\n````text\n```yaml\nepisode_id: fake\n```\n````\n\n"
            + episode("real")
        )
        self.write("episodes/one.md", disguised)
        self.write("README.md", readme([]))
        self.assertEqual(validate_studies(self.studies)["episodes"], 1)

    def test_backtick_in_info_does_not_open_a_fence(self) -> None:
        self.write("README.md", readme([]))
        for indent in range(4):
            with self.subTest(indent=indent):
                invalid_opener = " " * indent + "```yaml`not-a-fence\n"
                document = invalid_opener + episode(
                    "real",
                    fence_indent=indent,
                    fence_marker="`" * (3 + indent % 2),
                )
                self.write("episodes/one.md", document)
                self.assertEqual(validate_studies(self.studies)["episodes"], 1)

    def test_tilde_fence_info_may_contain_backticks(self) -> None:
        outer = (
            "# Decoy\n\n~~~text`is-valid-here\n"
            "```yaml\nepisode_id: fake\n```\n~~~\n\n"
        )
        self.write("episodes/one.md", outer + episode("real"))
        self.write("README.md", readme([]))
        self.assertEqual(validate_studies(self.studies)["episodes"], 1)

    def test_invalid_backtick_info_does_not_bypass_narrow_yaml_rules(self) -> None:
        self.write("README.md", readme([]))
        invalid_opener = "```yaml`not-a-fence\n"
        cases = {
            "quoted key": (
                episode("real").replace("episode_id: real", '"episode_id": real'),
                "ASCII plain keys",
            ),
            "folded scalar": (
                episode("real").replace("episode_id: real", "episode_id: >\n  real"),
                "episode_id must be a single-line scalar",
            ),
        }
        for name, (document, message) in cases.items():
            with self.subTest(name=name):
                self.write("episodes/one.md", invalid_opener + document)
                with self.assertRaisesRegex(ReferenceError, message):
                    validate_studies(self.studies)

    def test_only_cr_and_lf_create_markdown_lines(self) -> None:
        pseudo_line_endings = {
            "vertical tab": "\v",
            "form feed": "\f",
            "file separator": "\x1c",
            "group separator": "\x1d",
            "record separator": "\x1e",
            "next line": "\u0085",
            "line separator": "\u2028",
            "paragraph separator": "\u2029",
        }
        self.write("README.md", readme([]))

        for name, separator in pseudo_line_endings.items():
            with self.subTest(name=name, placement="before LF"):
                disguised = f"# Fixture\n\n```yaml{separator}\nepisode_id: ghost\n```\n"
                self.write("episodes/one.md", disguised)
                with self.assertRaisesRegex(
                    ReferenceError, "missing fenced YAML episode metadata"
                ):
                    validate_studies(self.studies)

            with self.subTest(name=name, placement="inside physical line"):
                disguised = f"# Fixture\n\n```yaml{separator}episode_id: ghost\n```\n"
                self.write("episodes/one.md", disguised)
                with self.assertRaisesRegex(
                    ReferenceError, "missing fenced YAML episode metadata"
                ):
                    validate_studies(self.studies)

    def test_yaml_info_trims_only_gfm_ascii_whitespace(self) -> None:
        self.write("README.md", readme([]))
        for name, suffix in {
            "no-break space": "\u00a0",
            "em space": "\u2003",
            "byte-order mark": "\ufeff",
        }.items():
            with self.subTest(name=name):
                disguised = f"# Fixture\n\n```yaml{suffix}\nepisode_id: ghost\n```\n"
                self.write("episodes/one.md", disguised)
                with self.assertRaisesRegex(
                    ReferenceError, "missing fenced YAML episode metadata"
                ):
                    validate_studies(self.studies)

        spaced = episode("real").replace("```yaml\n", "``` \tyaml \t\n")
        self.write("episodes/one.md", spaced)
        self.assertEqual(validate_studies(self.studies)["episodes"], 1)

    def test_indented_yaml_fences_are_deindented_like_gfm(self) -> None:
        cases = ((1, "```"), (2, "~~~"), (3, "```"))
        for fence_indent, fence_marker in cases:
            with self.subTest(indent=fence_indent, marker=fence_marker):
                self.write(
                    "episodes/one.md",
                    episode(
                        "first",
                        fence_indent=fence_indent,
                        fence_marker=fence_marker,
                    ),
                )
                self.write(
                    "episodes/two.md",
                    episode(
                        "second",
                        "first",
                        fence_indent=fence_indent,
                        fence_marker=fence_marker,
                    ),
                )
                self.write(
                    "README.md",
                    readme(
                        [("first", "second")],
                        fence_indent=fence_indent,
                        fence_marker=fence_marker,
                    ),
                )
                self.assertEqual(
                    validate_studies(self.studies),
                    {"episodes": 2, "relations": 1},
                )

    def test_unclosed_yaml_fence_is_rejected(self) -> None:
        self.write("episodes/one.md", "# Fixture\n\n```yaml\nepisode_id: one\n")
        self.write("README.md", readme([]))
        with self.assertRaisesRegex(ReferenceError, "unclosed YAML fence"):
            validate_studies(self.studies)


if __name__ == "__main__":
    unittest.main()
