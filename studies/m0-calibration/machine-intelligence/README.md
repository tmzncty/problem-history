# M0 Calibration — Machine Intelligence, 1950–2023

> **Purpose:** test whether two independent Agents can distinguish an actor's explicit problem, a supportable reconstructed problem, and a present-day researcher's analytic framing across a thematically tempting 73-year sequence.
>
> **This is a calibration corpus, not an accepted problem lineage.** The five texts were deliberately chosen because a modern reader can easily compress all of them into “Can machines think?” even when the historical target, stakes, presuppositions, answer space, and institutional setting differ.

This packet advances the M0 acceptance test in `ROADMAP.md`. It does **not** mark M0 complete and does **not** freeze `schemas/problem-episode.schema.json`.

## Files

- `cases.md` — blind source packets. Give this file plus `docs/METHOD.md`, `docs/IDENTITY-CHECK.md`, `docs/NEGATIVE-EVIDENCE.md`, and `docs/SOURCE-CITATION.md` to each test Agent.
- `oracle.md` — researcher oracle and failure expectations. **Do not give this file to test Agents before they answer.**

## Why this corpus

The sequence spans 73 years and contains at least four distinct kinds of historical act:

1. a philosopher-mathematician explicitly replacing an ambiguous question with a more operational one;
2. a group of researchers proposing an engineering research programme under the new label “artificial intelligence”;
3. an externally commissioned review asking whether a research field is coherent, successful, and worth supporting;
4. a philosophical argument about whether program instantiation is sufficient for intentionality;
5. a model developer reporting capabilities, limitations, safety work, evaluation, predictable scaling, and deployment.

The test is therefore hostile to a common Agent shortcut:

```text
same broad topic + recurring words such as machine / intelligence / AI
    → one timeless problem
```

That inference is not allowed.

## Blind calibration procedure

Run **two independent Agents**. Each Agent gets the same `cases.md` but not `oracle.md` and should not see the other Agent's answer.

For every case, require:

```yaml
case_id: "..."
explicit_actor:
  formulations: []
  evidence: []
reconstructed_actor:
  formulations: []
  evidence: []
  actor_language_status: supported | contested | unsupported | undetermined
researcher_analytic:
  tempting_formulations: []
  why_not_actor_wording: []
presuppositions:
  explicit: []
  reconstructed: []
stakes: []
answer_space:
  observed: []
  excluded_or_unlicensed: []
uncertainties: []
missing_evidence: []
```

Then require pairwise relation judgments for adjacent cases:

```yaml
relation: continuous | reformulated | transformed_successor | split | merged | displaced | revived | analogy_only | unrelated | undetermined
confidence: low | medium | high
continuity_evidence: []
discontinuity_evidence: []
actor_identity_claims: []
researcher_verdict: "..."
```

The Agent must explain both continuity and discontinuity evidence even if it ultimately chooses one relation.

## Pass conditions

This corpus passes only if both Agents can reliably do the following:

- keep a literal actor question separate from a researcher's modern umbrella question;
- notice when an actor explicitly replaces or rejects an earlier formulation;
- avoid treating the 1955 Dartmouth proposal as proof that every earlier machine-intelligence discussion was already “AI” in the same historical sense;
- recognize that an institutional research-funding review can be a different problem episode from the technical work it evaluates;
- distinguish behavioral/performance criteria from claims about intentionality or understanding;
- avoid projecting consciousness or sentience into a source that instead discusses capability, reliability, safety, scaling, and deployment;
- use `undetermined` when the selected packet does not license a stronger identity relation.

Agreement on labels alone is insufficient. The two Agents must preserve evidence provenance and give a defensible account of why apparently continuous vocabulary does or does not imply problem continuity.

## Fail conditions

Revise `docs/METHOD.md` before schema freeze if either Agent repeatedly:

- rewrites all five cases as answers to one perennial “Can machines think?” question;
- treats later historiographic labels such as “birth of AI” or “AI winter” as if they were necessarily the historical actors' own problem formulations;
- turns a conjecture, benchmark, criticism, or policy judgment into an ontological claim about intelligence;
- confuses a source's topic with the question it was historically trying to settle;
- omits counterevidence or cannot state why an adjacent pair may be discontinuous.

## Source policy

The packet prioritizes published originals, archival or institutional reproductions, journal metadata, and official actor documents. Quotations in `cases.md` are deliberately short; the linked original should be consulted for any wording that affects a final historical claim.

The Dartmouth packet uses the 2006 *AI Magazine* open-access reproduction of the 31 August 1955 proposal and records that mediation rather than pretending the web copy is the physical typescript. The Lighthill packet uses the University of Edinburgh AIAI-hosted scan of the July 1972 report and distinguishes its 1972 report date from 1973 publication in the Science Research Council symposium volume. The GPT-4 packet is strong evidence for **OpenAI's own 2023 framing**, not automatically for the whole AI field.

## What this packet does not establish

It does not establish that the five cases form one lineage. It does not establish that “AI” began at a single date. It does not establish that the Turing imitation game, Dartmouth programme, Lighthill review, Searle argument, and GPT-4 evaluation are stages of one question. Those are precisely the hypotheses the calibration is meant to prevent an Agent from assuming in advance.
