# 1998 FIPS withdrawal: three exceptions to a proposed nineteen-standard retirement

Status: **source-backed research note; not a validated Problem Episode or 50-year lineage**. Checked against main at `ac3d0b5b179c2406d3a4bbd506f8a48c468734d1` on 2026-11-16. Do not treat this as a continuation of the 1970s magnetic-tape episode without independent identity evidence.

## New primary-source finding

The 1998-02-24 NIST proposal listed **19** FIPS for withdrawal (63 FR 9199, FR Doc 98-4683). The 1998-11-18 final notice withdrew **16** (63 FR 64062–64063, FR Doc 98-30796), effective that day. The final notice **explicitly explains all three exclusions**:

- **FIPS 183**, Integration Definition for Function Modeling (IDEF0), and **FIPS 184**, Integration Definition for Information Modeling (IDEF1X): retained **until voluntary industry standards are available**.
- **FIPS 160**, C (ANSI/ISO 9899:1992): retained **until NIST's C-language validation program ends**; the notice anticipated withdrawal later in 1998. This is an *announced plan*, **not evidence that a later withdrawal occurred**.

The notice says NIST reviewed written comments and delayed these three because of comments received, but **does not identify commenters or reproduce their submissions**. Do not infer which stakeholder argued for which exception.

## Actor formulations / reconstruction / analytical question

1. **Actor-explicit institutional issue (high confidence):** NIST asked whether to withdraw federal FIPS that duplicated voluntary industry standards, were outdated, or lacked updated references. Its final decision balanced retirement against continued availability of replacement standards and an ongoing validation program. The two notices directly support this.
2. **Context-supported reconstruction (medium):** retirement timing depended on whether an alternative standard and institutional implementation/validation infrastructure could assume the FIPS role. This is a reconstruction from the stated exceptions, not a verbatim question posed by a named participant.
3. **Present-day analytical question (hypothesis only):** when does a standard cease to be *maintainable as a federal requirement* even though the underlying technical or institutional problem persists? “Standards lifecycle” and “problem displacement” are our categories, not attributed to the 1998 actors.

## Evidence and locators

- NIST, “Proposed Withdrawal of Nineteen Federal Information Processing Standards (FIPS) Publications,” *Federal Register* 63 (1998-02-24), p. 9199, FR Doc 98-4683, docket 980107004-8004-01. Original HTML: https://www.govinfo.gov/content/pkg/FR-1998-02-24/html/98-4683.htm . **High** for original proposal, proposed set and rationale.
- NIST, “Approval of Withdrawal of Sixteen Federal Information Processing Standards (FIPS) Publications,” *Federal Register* 63 (1998-11-18), pp. 64062–64063, FR Doc 98-30796, docket 980107004-8216-02. Official issue PDF: https://www.govinfo.gov/content/pkg/FR-1998-11-18/pdf/FR-1998-11-18.pdf . **High** for decision, three exceptions and expressly stated reasons.
- NIST, “Procedures for Developing FIPS Publications,” https://www.nist.gov/itl/procedures-developing-fips-federal-information-processing-standards-publications . **Context only**, modern retrospective procedural guidance; **not** evidence of the exact 1998 workflow.

## Interpretation and counterevidence

The **19 → 16** discrepancy is not an arithmetic error or a uniform disappearance of need: the final document records explicit reasons for **retention**. FIPS 183/184 imply a missing acceptable successor at that point; FIPS 160 shows a validation dependency. Neither proves a particular technology's technical superiority, industry adoption rates, or a direct lineage to FIPS 51/79. The 1998 notice states a change in government standard-setting requirements; it does not prove the underlying interoperability problem was solved.

Potential discontinuity: FIPS 51/79 concerned magnetic-media exchange; the 1998 three exceptions concern modeling standards and C validation. Shared governance by NIST is **not** sufficient for historical problem identity. Treat as **analogy_only / undetermined** pending documentary linkage, not `continuous`.

## Missing evidence / next steps

1. Obtain the written public comments and Secretary's detailed justification, cited as available in the Department's Central Reference and Records Inspection Facility (Room 6020, Herbert C. Hoover Building); establish who requested each delay.
2. Search a *subsequent* Federal Register withdrawal notice for FIPS 160; separately establish when and under what replacement conditions FIPS 183/184 were withdrawn, if at all.
3. Compare 1996–1997 withdrawal notices to see whether “absence of successor” or “validation dependency” recurs, without conflating unrelated technical problems.
4. Only after obtaining actor-language evidence build a relation/episode and test against `docs/IDENTITY-CHECK.md`.

Suggested location: `research/fips-withdrawal-1998-exceptions.md`. This is an archival evidence note, **not** a new schema, an accepted pilot, or a claim to meet M2's three-primary-source minimum.
