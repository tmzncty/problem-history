# M0 schema prototype (2026-11-11)

This is a **structural experiment**, not a frozen historical ontology. It follows [METHOD](../docs/METHOD.md), [IDENTITY-CHECK](../docs/IDENTITY-CHECK.md), and [SOURCE-CITATION](../docs/SOURCE-CITATION.md). JSON Schema draft 2020-12: https://json-schema.org/draft/2020-12 .

Three JSON fixtures under `fixtures/episode-schema/` are **fictional**, not historical evidence. They exercise a researcher-analytic question, a reconstructed-actor question with admissibility/alternative reading, and an explicitly undetermined relation. The schema requires source version, locator, provenance, mediation, claim-relative assessment, and continuity **and** discontinuity evidence for every relation. It does not infer historical validity from syntactic validity.

Run `python -m pip install jsonschema` and then `python scripts/check_episode_schema.py` to check schema, three positive fixtures, and deliberately invalid examples. The validator cannot check source ID referential integrity, independence of sources, the pilot's ≥3 primary-source threshold, actor-language historical plausibility, or whether a claimed relation is true. These require separate research review. A reconstructed actor formulation without `actor_language` or `competing_readings` is rejected structurally; it may still be unsubstantiated even if those fields exist.

Next: trial against a real episode with verified source locators, and revise field constraints only after checking whether the schema loses meaningful uncertainty. Do not mark ROADMAP M0 complete before that calibration.
