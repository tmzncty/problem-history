from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_problem_episodes import (  # noqa: E402
    ContractError,
    discover_json,
    validate_documents,
)


SCHEMA = REPO_ROOT / "schemas" / "problem-episode.schema.json"
FIXTURES = REPO_ROOT / "fixtures" / "problem-episodes"


class ProblemEpisodeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture_paths = discover_json([FIXTURES])
        cls.documents = [
            json.loads(path.read_text(encoding="utf-8")) for path in cls.fixture_paths
        ]

    def _write_mutation(self, root: Path, documents: list[dict]) -> list[Path]:
        paths: list[Path] = []
        for index, document in enumerate(documents):
            path = root / f"fixture-{index}.json"
            path.write_text(
                json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            paths.append(path)
        return paths

    def _validate_mutation(self, documents: list[dict]) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            validate_documents(SCHEMA, self._write_mutation(root, documents))

    def _validate_raw_replacement(self, before: str, after: str) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths: list[Path] = []
            replaced = False
            for source in self.fixture_paths:
                text = source.read_text(encoding="utf-8")
                if not replaced and before in text:
                    text = text.replace(before, after, 1)
                    replaced = True
                path = root / source.name
                path.write_text(text, encoding="utf-8")
                paths.append(path)
            self.assertTrue(replaced, f"raw fixture anchor not found: {before!r}")
            validate_documents(SCHEMA, paths)

    def _validate_first_document_bytes(self, first_payload: bytes) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths: list[Path] = []
            for index, source in enumerate(self.fixture_paths):
                path = root / source.name
                payload = first_payload if index == 0 else source.read_bytes()
                path.write_bytes(payload)
                paths.append(path)
            validate_documents(SCHEMA, paths)

    def test_schema_is_valid_draft_2020_12(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)

    def test_all_fixtures_validate_as_one_corpus(self) -> None:
        counts = validate_documents(SCHEMA, self.fixture_paths)
        self.assertEqual(counts["documents"], 3)
        self.assertEqual(counts["relations"], 2)

    def test_fixture_suite_exercises_all_formulation_sources(self) -> None:
        represented = {
            formulation["source_type"]
            for document in self.documents
            for formulation in document["formulations"]
        }
        self.assertEqual(
            represented,
            {"actor_explicit", "actor_reconstructed", "researcher_analytic"},
        )

    def test_fixture_suite_keeps_researcher_vocabulary_visible(self) -> None:
        represented = {
            vocabulary["term_source_type"]
            for document in self.documents
            for vocabulary in document["vocabulary"]
        }
        self.assertIn("actor_explicit", represented)
        self.assertIn("researcher_analytic_label", represented)

    def test_researcher_vocabulary_requires_provenance_note(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[2]["vocabulary"][1].pop("provenance_note")
        with self.assertRaisesRegex(ContractError, "provenance_note"):
            self._validate_mutation(documents)

    def test_reconstructed_formulation_requires_an_audit_trail(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[1]["formulations"][0].pop("reconstruction_note")
        with self.assertRaisesRegex(ContractError, "reconstruction_note"):
            self._validate_mutation(documents)

        documents = copy.deepcopy(self.documents)
        documents[1]["formulations"][0]["evidence_ids"] = [
            "control-engineer-request"
        ]
        with self.assertRaises(ContractError):
            self._validate_mutation(documents)

    def test_actor_formulation_requires_an_actor(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["formulations"][0]["actor_ids"] = []
        with self.assertRaises(ContractError):
            self._validate_mutation(documents)

    def test_unretrievable_source_requires_an_explanation(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["sources"][0].pop("notes")
        with self.assertRaisesRegex(ContractError, "notes"):
            self._validate_mutation(documents)

    def test_required_prose_rejects_unicode_whitespace_only_values(self) -> None:
        whitespace = {
            "ASCII": " \t\n\v\f\r",
            "next-line and no-break": "\u0085\u00a0",
            "Ogham": "\u1680",
            "en through hair spaces": "".join(chr(value) for value in range(0x2000, 0x200B)),
            "line and paragraph separators": "\u2028\u2029",
            "narrow and medium spaces": "\u202f\u205f",
            "ideographic space and BOM": "\u3000\ufeff",
        }
        for name, value in whitespace.items():
            with self.subTest(name=name, shape="blank"):
                documents = copy.deepcopy(self.documents)
                documents[0]["sources"][0]["citation"] = value
                with self.assertRaisesRegex(
                    ContractError, r"\$\.sources\[0\]\.citation"
                ):
                    self._validate_mutation(documents)

            with self.subTest(name=name, shape="padded text"):
                documents = copy.deepcopy(self.documents)
                documents[0]["sources"][0]["citation"] = f"{value}史料{value}"
                self._validate_mutation(documents)

    def test_reviewed_status_requires_a_named_reviewer(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["audit"]["record_status"] = "reviewed"
        documents[0]["audit"]["reviewed_by"] = [" \t\r\n"]
        with self.assertRaisesRegex(ContractError, r"\$\.audit\.reviewed_by\[0\]"):
            self._validate_mutation(documents)

        documents = copy.deepcopy(self.documents)
        documents[0]["relations"][0]["identity_status"] = "reviewed"
        documents[0]["relations"][0]["reviewed_by"] = ["\u3000"]
        with self.assertRaisesRegex(
            ContractError, r"\$\.relations\[0\]\.reviewed_by\[0\]"
        ):
            self._validate_mutation(documents)

    def test_relation_requires_continuity_and_discontinuity_evidence(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["relations"][0]["discontinuity_evidence"] = []
        with self.assertRaises(ContractError):
            self._validate_mutation(documents)

    def test_unresolved_evidence_reference_is_rejected(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["stakes"][0]["evidence_ids"] = ["missing-evidence"]
        with self.assertRaisesRegex(ContractError, "unresolved evidence"):
            self._validate_mutation(documents)

    def test_unresolved_counterevidence_reference_is_rejected(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["relations"][0]["dimensions"]["target_object"][
            "counterevidence_ids"
        ] = ["missing-evidence"]
        with self.assertRaisesRegex(ContractError, "unresolved evidence"):
            self._validate_mutation(documents)

    def test_unresolved_relation_target_is_rejected(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["relations"][0]["target_episode_id"] = "missing-episode"
        with self.assertRaisesRegex(ContractError, "unresolved episode"):
            self._validate_mutation(documents)

    def test_non_relation_cross_episode_evidence_is_rejected(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["stakes"][0]["evidence_ids"] = ["control-question"]
        with self.assertRaisesRegex(ContractError, "non-relation field references"):
            self._validate_mutation(documents)

    def test_relation_source_must_match_container(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["relations"][0]["source_episode_id"] = documents[1][
            "episode_id"
        ]
        with self.assertRaisesRegex(ContractError, "must equal the containing"):
            self._validate_mutation(documents)

    def test_relation_rejects_evidence_from_a_third_episode(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["relations"][0]["dimensions"]["target_object"][
            "counterevidence_ids"
        ] = ["data-retention-dispute"]
        with self.assertRaisesRegex(ContractError, "expected source/target"):
            self._validate_mutation(documents)

    def test_retargeted_relation_rejects_old_target_evidence(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["relations"][0]["target_episode_id"] = documents[2][
            "episode_id"
        ]
        with self.assertRaisesRegex(ContractError, "expected source/target"):
            self._validate_mutation(documents)

    def test_relation_accepts_evidence_from_both_endpoints(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["relations"][0]["identity_claims"][0]["evidence_ids"] = [
            "fuel-question",
            "control-question",
        ]
        self._validate_mutation(documents)

    def test_relation_rejects_cross_fixture_boundary(self) -> None:
        cases = (
            ("fixture to non-fixture", 0, 1, True, False),
            ("non-fixture to fixture", 1, 2, False, True),
        )
        for name, source_index, target_index, source_fixture, target_fixture in cases:
            with self.subTest(name=name):
                documents = copy.deepcopy(self.documents)
                for document in documents:
                    document["relations"] = []

                source = documents[source_index]
                target = documents[target_index]
                source["relations"] = [
                    copy.deepcopy(self.documents[source_index]["relations"][0])
                ]
                source["is_fixture"] = source_fixture
                target["is_fixture"] = target_fixture
                source["relations"][0]["source_episode_id"] = source["episode_id"]
                source["relations"][0]["target_episode_id"] = target["episode_id"]

                historical_record = target if not target_fixture else source
                historical_record["audit"]["record_status"] = "reviewed"
                historical_record["audit"]["reviewed_by"] = ["fixture-boundary-test"]
                source["relations"][0]["identity_status"] = "reviewed"
                source["relations"][0]["reviewed_by"] = ["fixture-boundary-test"]

                with tempfile.TemporaryDirectory() as temporary:
                    paths = self._write_mutation(Path(temporary), documents)
                    source_path = paths[source_index].resolve()
                    with self.assertRaises(ContractError) as context:
                        validate_documents(SCHEMA, paths)

                self.assertEqual(
                    context.exception.errors,
                    [
                        f"{source_path}:$.relations[0]"
                        ".target_episode_id: relations cannot cross the fixture "
                        f"boundary; source is_fixture={str(source_fixture).lower()}, "
                        f"target is_fixture={str(target_fixture).lower()}"
                    ],
                )

    def test_relations_accept_matching_fixture_status(self) -> None:
        for name, is_fixture in (
            ("fixture relations", True),
            ("historical relations", False),
        ):
            with self.subTest(name=name):
                documents = copy.deepcopy(self.documents)
                for document in documents:
                    document["is_fixture"] = is_fixture
                self._validate_mutation(documents)

    def test_unrelated_fixture_and_historical_documents_share_a_corpus(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[1]["is_fixture"] = False
        for document in documents:
            document["relations"] = []
        self._validate_mutation(documents)

    def test_actor_explicit_formulation_rejects_context_only_evidence(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["formulations"][0]["evidence_ids"] = ["fuel-ledger-costs"]
        with self.assertRaisesRegex(
            ContractError, "actor_explicit formulation must reference"
        ):
            self._validate_mutation(documents)

    def test_actor_explicit_answer_rejects_silence_only_evidence(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[2]["answer_space"]["accepted"][0]["evidence_ids"] = [
            "data-no-debate-citation"
        ]
        with self.assertRaisesRegex(
            ContractError, "actor_explicit answer must reference"
        ):
            self._validate_mutation(documents)

    def test_actor_explicit_formulation_accepts_a_paraphrase(self) -> None:
        documents = copy.deepcopy(self.documents)
        evidence = next(
            item
            for item in documents[0]["evidence"]
            if item["evidence_id"] == "fuel-question"
        )
        evidence["evidence_type"] = "paraphrase"
        self._validate_mutation(documents)

    def test_reversed_period_is_rejected(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["period"]["start_year"] = 1882
        documents[0]["period"]["end_year"] = 1881
        with self.assertRaisesRegex(ContractError, "start_year must not exceed"):
            self._validate_mutation(documents)

    def test_reversed_period_with_integral_json_numbers_is_rejected(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["period"]["start_year"] = 2000.0
        documents[0]["period"]["end_year"] = 1000.0
        with self.assertRaisesRegex(ContractError, "start_year must not exceed"):
            self._validate_mutation(documents)

    def test_reversed_period_with_exponent_syntax_is_rejected(self) -> None:
        before = '"start_year": 1880,\n    "end_year": 1881'
        after = '"start_year": 2e3,\n    "end_year": 1e3'
        with self.assertRaisesRegex(ContractError, "start_year must not exceed"):
            self._validate_raw_replacement(before, after)

    def test_period_numbers_keep_exact_decimal_precision(self) -> None:
        before = '"start_year": 1880,\n    "end_year": 1881'
        cases = {
            "rounding": '"start_year": 1880.0000000000000001,\n    "end_year": 1880',
            "underflow": '"start_year": 1e-324,\n    "end_year": 0',
        }
        for name, after in cases.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ContractError, "is not of type 'integer'"
                ):
                    self._validate_raw_replacement(before, after)

    def test_large_finite_json_number_reaches_schema_bounds(self) -> None:
        before = '    "start_year": 1880,'
        with self.assertRaisesRegex(
            ContractError, "greater than the maximum of 3000"
        ):
            self._validate_raw_replacement(
                before,
                '    "start_year": 1e400,',
            )

    def test_unrepresentable_decimal_exponent_is_a_contract_error(self) -> None:
        before = '    "start_year": 1880,'
        with self.assertRaisesRegex(ContractError, "cannot load JSON"):
            self._validate_raw_replacement(
                before,
                '    "start_year": 1e1000000000000000000,',
            )

    def test_oversized_integer_is_a_path_qualified_contract_error(self) -> None:
        before = '    "start_year": 1880,'
        cases = {
            "integer literal": "1" * 4301,
            "expanded exponent": "1e4300",
        }
        for name, raw_number in cases.items():
            with self.subTest(name=name), self.assertRaises(ContractError) as context:
                self._validate_raw_replacement(
                    before,
                    f'    "start_year": {raw_number},',
                )

            message = str(context.exception)
            self.assertIn(self.fixture_paths[0].name, message)
            self.assertIn("cannot load JSON", message)
            self.assertIn("integer exceeds 4300 decimal digits", message)

    def test_integral_decimal_schema_keywords_are_meta_schema_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            schema = Path(temporary) / "schema.json"
            schema.write_text(
                SCHEMA.read_text(encoding="utf-8").replace(
                    '"minItems": 1',
                    '"minItems": 1.0',
                    1,
                ),
                encoding="utf-8",
            )

            counts = validate_documents(schema, self.fixture_paths)

        self.assertEqual(3, counts["documents"])

    def test_ordered_period_with_integral_json_numbers_is_accepted(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["period"]["start_year"] = 1880.0
        documents[0]["period"]["end_year"] = 1881.0
        self._validate_mutation(documents)

        before = '"start_year": 1880,\n    "end_year": 1881'
        for name, after in {
            "integral exponent": '"start_year": 1.88e3,\n    "end_year": 1881.0',
            "signed zero": '"start_year": -0.0,\n    "end_year": -0',
        }.items():
            with self.subTest(name=name):
                self._validate_raw_replacement(before, after)

    def test_reversed_period_covers_mixed_zero_and_negative_years(self) -> None:
        cases = (
            ("mixed types with zero end", 1, 0.0),
            ("mixed types with zero start", 0.0, -1),
            ("negative years", -1.0, -2),
        )
        for name, start, end in cases:
            with self.subTest(name=name):
                documents = copy.deepcopy(self.documents)
                documents[0]["period"]["start_year"] = start
                documents[0]["period"]["end_year"] = end
                with self.assertRaisesRegex(
                    ContractError, "start_year must not exceed"
                ):
                    self._validate_mutation(documents)

    def test_unknown_field_is_rejected_by_strict_schema(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["modern_summary"] = "This field bypasses the evidence model."
        with self.assertRaisesRegex(ContractError, "Additional properties"):
            self._validate_mutation(documents)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        cases = {
            "top-level escaped equivalent": (
                '  "episode_id": "harbor-night-signal-fuel-1880",',
                '  "episode_id": "shadow-episode",\n'
                '  "\\u0065pisode_id": "harbor-night-signal-fuel-1880",',
                "episode_id",
            ),
            "nested evidence identity": (
                '      "evidence_id": "fuel-inquiry-date",',
                '      "evidence_id": "shadow-evidence",\n'
                '      "evidence_id": "fuel-inquiry-date",',
                "evidence_id",
            ),
        }
        for name, (before, after, key) in cases.items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    ContractError, rf"duplicate object key '{key}'"
                ):
                    self._validate_raw_replacement(before, after)

    def test_duplicate_schema_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            schema = Path(temporary) / "schema.json"
            text = SCHEMA.read_text(encoding="utf-8")
            schema.write_text(
                text.replace(
                    '  "type": "object",',
                    '  "type": "array",\n  "type": "object",',
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ContractError, "duplicate object key 'type'"):
                validate_documents(schema, self.fixture_paths)

    def test_non_finite_json_constants_are_rejected_in_documents(self) -> None:
        before = '    "start_year": 1880,'
        first_name = self.fixture_paths[0].name
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                with self.assertRaises(ContractError) as context:
                    self._validate_raw_replacement(
                        before,
                        f'    "start_year": {constant},',
                    )
                message = str(context.exception)
                self.assertIn(f"{first_name}: cannot load JSON:", message)
                self.assertIn(
                    f"non-finite numeric constant {constant!r} is not valid JSON",
                    message,
                )

    def test_non_finite_json_constants_are_rejected_in_schema(self) -> None:
        schema_text = SCHEMA.read_text(encoding="utf-8")
        for constant in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(constant=constant):
                with tempfile.TemporaryDirectory() as temporary:
                    schema = Path(temporary) / "schema.json"
                    schema.write_text(
                        schema_text.replace(
                            '          "minimum": -10000,',
                            f'          "minimum": {constant},',
                            1,
                        ),
                        encoding="utf-8",
                    )
                    with self.assertRaises(ContractError) as context:
                        validate_documents(schema, self.fixture_paths)
                message = str(context.exception)
                self.assertIn("schema.json: cannot load JSON:", message)
                self.assertIn(
                    f"non-finite numeric constant {constant!r} is not valid JSON",
                    message,
                )

    def test_invalid_utf8_is_reported_as_a_contract_error(self) -> None:
        first_name = self.fixture_paths[0].name
        invalid_document = b"\xff" + self.fixture_paths[0].read_bytes()
        with self.assertRaises(ContractError) as context:
            self._validate_first_document_bytes(invalid_document)
        self.assertIn(
            f"{first_name}: cannot load JSON:",
            str(context.exception),
        )

        with tempfile.TemporaryDirectory() as temporary:
            schema = Path(temporary) / "schema.json"
            schema.write_bytes(b"\xff" + SCHEMA.read_bytes())
            with self.assertRaises(ContractError) as context:
                validate_documents(schema, self.fixture_paths)
        self.assertIn("schema.json: cannot load JSON:", str(context.exception))

    def test_utf8_bom_remains_a_clean_contract_error(self) -> None:
        bom = b"\xef\xbb\xbf"
        first_name = self.fixture_paths[0].name
        with self.assertRaises(ContractError) as context:
            self._validate_first_document_bytes(
                bom + self.fixture_paths[0].read_bytes()
            )
        message = str(context.exception)
        self.assertIn(f"{first_name}: cannot load JSON:", message)
        self.assertIn("Unexpected UTF-8 BOM", message)

        with tempfile.TemporaryDirectory() as temporary:
            schema = Path(temporary) / "schema.json"
            schema.write_bytes(bom + SCHEMA.read_bytes())
            with self.assertRaises(ContractError) as context:
                validate_documents(schema, self.fixture_paths)
        message = str(context.exception)
        self.assertIn("schema.json: cannot load JSON:", message)
        self.assertIn("Unexpected UTF-8 BOM", message)

    def test_strict_json_loading_accepts_large_integers_and_reused_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            schema = Path(temporary) / "schema.json"
            schema.write_text(
                SCHEMA.read_text(encoding="utf-8").replace(
                    "{",
                    '{\n  "x-large-integer": ' + "9" * 4300 + ",",
                    1,
                ),
                encoding="utf-8",
            )
            counts = validate_documents(schema, self.fixture_paths)
        self.assertEqual(counts["documents"], 3)

    def test_malformed_structure_returns_contract_error(self) -> None:
        documents = copy.deepcopy(self.documents)
        documents[0]["actors"] = {"not": "an array"}
        with self.assertRaisesRegex(ContractError, "is not of type 'array'"):
            self._validate_mutation(documents)


if __name__ == "__main__":
    unittest.main()
