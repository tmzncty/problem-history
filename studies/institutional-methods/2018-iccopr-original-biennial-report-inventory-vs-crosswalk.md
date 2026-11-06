# 2018 ICCOPR original biennial report recovered: inventory versus coverage crosswalk

## Delta from existing PR #41 research

The 2019 meeting-minutes packet explicitly left the **FY2016–17 Biennial Report to Congress** unreadable. The original report is now directly retrievable, dated **7 November 2018**. This resolves the document-recovery debt, **not** the underlying mapping/validation debt.

**Primary source:** U.S. Coast Guard / ICCOPR, *Interagency Coordinating Committee on Oil Pollution Research: FY 2016–2017 Activities*, Report to Congress, November 7, 2018, https://www.dco.uscg.mil/Portals/9/CG-5R/ICCOPR/Files/USCG_ICCOPR%20Oil%20Pollution%20Research%20%28FY%202016-2017%29_Approved%20Version.pdf?ver=2018-11-28-154311-093

## Primary-source findings

1. **Exact source of the headline metrics (Executive Summary; Member Research and Technology Initiatives).** The report says **316 active member projects**, **over 250 publications**, research in **92% of 25 Standing Research Areas**, and research projects addressing **61% of 150 priorities**. These are four different measures; publications and projects are not interchangeable with priorities. At integer SRA granularity, 92% of 25 is **23 SRAs**. By contrast 61% of 150 is **91.5**, so it cannot literally be an exact integer count of distinct priorities: the percentage is necessarily rounded, approximate, weighted, or otherwise calculated. The text does not identify which. Do **not** assert either 91 or 92 as the verified numerator.
2. **The project inventory is actually present.** The PDF has an extensive, thematic **Appendix A, 'Listing of Fiscal Year 2016 and 2017 Research Projects'**, beginning at its labeled page A-1. It lists project titles grouped by research class/area, including explicit 'NONE' entries (e.g. Onshore Facilities and Systems and Vessel Design in Prevention). The main body refers to a complete project list as **'Appendix B'**, whereas the visible appendix is labeled **Appendix A**. This internal appendix-label inconsistency should be noted when citing and locating the inventory, not silently normalized.
3. **The inventory is not a priority crosswalk.** The visible list groups titles by topical category; it does not itself expose an explicit project × 150-priority matrix, a deduplication rule, or a documented calculation algorithm for the 61%. The 2019 meeting record's concern about manual project-to-SRA verification therefore remains relevant. Do not mistake the presence of the project inventory for independent replication of the coverage calculation.
4. **The temporal population is broader than completed work.** The footnote to the member-project analysis defines the projects as those **initiated, ongoing and/or completed** during FY2016–17. Therefore neither 316 projects nor 61% coverage represents 316 completions or 61% priority completion.
5. **The institution itself marks a coverage boundary.** The report notes research by nonmember federal agencies and state, local, academic, and industry actors outside its member-agency accounting. Thus uncovered-by-member-agencies is not necessarily unresearched, while the counterfactual inclusion of outside work is not an audited alternative percentage.
6. **The actor-stated forward problem.** The report lists tracking/monitoring under the OPRTP, increased joint research, public communication, and transfer from research to operations among future initiatives. This is the institution's own 2018 agenda, not a 2023 critique projected backward.

## Historical-actor / reconstruction / analytical distinction

- **Historical actor:** ICCOPR reported the 316/250+/92%/61% figures, explicitly defined the activity window to include projects initiated, ongoing, or completed, acknowledged the external research boundary, and named monitoring and transition-to-operations as future work.
- **Source-critical reconstruction:** The original report is now available, and the appendix provides a title-level inventory, but a priority-level crosswalk is not established. The discrepancy 'Appendix B' in the body versus 'Appendix A' in the appendix is a verifiable document feature.
- **Present-day analysis:** 'denominator audit', 'inventory ≠ crosswalk', 'measurement-frame boundary', and 'integer granularity test' are researcher vocabulary, not historical quotations.

## Evidence strength

- **High (primary official report):** date, report's published totals, activity-window definition, inventory existence, appendix-label mismatch, and the institution's own stated initiatives.
- **Medium (arithmetical constraint):** 92% × 25 = 23 and 61% × 150 = 91.5; this demonstrates a need for rounding/other accounting but **cannot select a numerator or rule**.
- **Unproven:** exact 61% numerator; whether project duplicates across categories are removed; full project-to-priority mapping; percentage independently validated; causal influence on 2019 legislation.

## Episode and integration

Append to the current sequence:
`2015 plan (25 SRAs / 150 priorities) → FY2016–17 activity inventory → 2018 reported coverage and stated tracking needs → 2019 observed manual reporting/classification workflow → 2023 external evaluation`.

Place this packet beside:
- `studies/institutional-methods/2018-iccopr-portfolio-coverage-vs-unfunded-coordination.md`
- `studies/institutional-methods/2019-iccopr-coverage-metric-production-and-reporting-friction.md`

Suggested episode fields: `inventory_artifact`, `inventory_scope`, `reporting_window`, `unit_of_count`, `coverage_denominator`, `coverage_numerator_verified`, `crosswalk_available`, `external_actor_exclusions`, `source_internal_inconsistencies`.

## Source debt / next candidates

1. Extract and compare Appendix A titles against the Coast Guard's archived FY2016–17 category pages; determine whether there are repeated titles or projects across categories, without assuming duplicates are errors.
2. Obtain the original project-to-priority spreadsheet, if retained, or any enclosure describing the mapping procedure; only then attempt an independent 61% replication.
3. Compare 2018–19 coverage statistics only after checking whether the inclusion frame and units match.
4. Investigate whether the 2018 report's forward initiatives were cited in subsequent committee testimony; no direct transmission is claimed here.
