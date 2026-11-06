# 1945: report-pruning candidates were filtered during committee review before enactment

## Research question

The current report-pruning genealogy already shows a standing-committee interest filter explicitly in 1965 and a comparable agency/committee selection process in 1995. Was this kind of candidate rescue only a later procedural refinement, or is there evidence that the 1945 H.R. 2504 round already filtered proposed report eliminations before the bill reached the floor?

## New finding

A March 8, 1945 House floor exchange supplies direct actor-level evidence that the 1945 committee process was already selective. Representative John J. Cochran, speaking for the Committee on Expenditures in the Executive Departments while preparing to report H.R. 2504, said the committee had held hearings for three days and had **eliminated several items where there were objections**.

The resulting bill proposed discontinuing 64 statutory reports. Cochran described many as obsolete and asked the House to waive the Ramseyer-rule printing burden, while assuring members that the committee report would explain every item.

This adds an earlier process state to the repository's report-pruning genealogy:

```text
candidate report eliminations
        ↓
committee hearings / objections
        ↓
some candidates removed from repeal package
        ↓
64-item H.R. 2504 reported
        ↓
later House/Senate action and P.L. 79-615
```

The evidence does not yet identify the removed candidates, who objected to each, or whether the objections came from agencies, committees, members, or other witnesses. It therefore supports `pre-enactment candidate filtering`, not yet a fully specified `committee-of-jurisdiction veto` identical to the 1965 procedure.

## Primary evidence

### March 8, 1945 House exchange

Cochran told the House that H.R. 2504 would repeal 64 statutory reporting requirements. When another member pressed for assurance that the House would know what was being discontinued, Cochran said the committee had held three days of hearings and had removed several items where objections were made. He promised the report would fully explain the retained items.

Primary source:

- *Congressional Record*, 79th Cong., 1st sess., Mar. 8, 1945, pp. 1922–1923, GovInfo bound edition: https://www.govinfo.gov/content/pkg/GPO-CRECB-1945-pt2/pdf/GPO-CRECB-1945-pt2-9.pdf

A later House precedents compilation independently reproduces the procedural episode and identifies the same pages while explaining the Ramseyer-rule waiver:

- *Deschler's Precedents of the United States House of Representatives*, vol. 4, ch. 17, §60.19: https://www.govinfo.gov/content/pkg/GPO-HPREC-DESCHLERS-V4/pdf/GPO-HPREC-DESCHLERS-V4-3-7-3.pdf

**Evidence strength: very high** for the existence of a three-day hearing process and removal of multiple candidates after objections; **unknown** for the identity and rationale of each removed item until the hearing record/candidate list is recovered.

### H. Rept. 79-311 confirms the surviving 64-item package and its general rationale

House Report 79-311 says H.R. 2504 would discontinue 64 reports or statements and explains the broader rationale: statutory reports often arose when Congress created or expanded functions, but after years of operation could become relatively low-value. The report also explicitly invokes the 1928 mass-repeal statute as a same-character precedent and preserves Congress's ability to obtain needed information on request.

Primary source:

- H. Rept. 79-311, *Discontinuing Certain Reports Now Required by Law*, Mar. 13, 1945, reproduced in the legislative history of P.L. 79-615: https://upload.wikimedia.org/wikipedia/commons/8/86/Legislative_History%2C_Public_Law_615_-_79th_Congress%2C_Chapter_770_-_2d_Session%2C_H.R._2504_%28IA_PL79615%29.pdf

**Evidence strength: very high** for the surviving package and committee-level rationale.

## Historical actors vs later reconstruction vs present analysis

### Historical actors

Directly supportable in March 1945:

- the committee had a larger candidate field than the 64 reports ultimately reported;
- it held three days of hearings;
- objections caused several candidate items to be eliminated from the bill;
- Cochran characterized many retained repeal targets as obsolete;
- members demanded enough item-level explanation to know what reports Congress was giving up.

### Later reconstruction

The repository already observes a more formal committee-interest filter in 1965 and agency/committee screening in 1995. The 1945 evidence pushes selective filtering earlier, but it does **not** prove that the same formal procedure persisted continuously from 1945 to 1965 or 1995.

### Present analytical shorthand

Useful researcher labels only:

- `pre-enactment candidate filtering`;
- `objection-triggered rescue`;
- `candidate set != reported repeal set`;
- `proposal attrition before floor action`.

Do not attribute these phrases to Cochran or the committee.

## Problem-History payoff

The report-pruning process should no longer be modeled only as:

```text
report exists -> Congress judges obsolete -> repeal
```

At least by 1945, there is evidence for a contested selection stage:

```text
inherited reporting stock
        ↓
proposed repeal candidates
        ↓
hearings + objections
        ↓
retain some reports / advance others for repeal
        ↓
reported bill
```

This matters because an item that survives is not evidence that no one questioned it. It may instead be an **unsuccessful repeal candidate rescued during review**. Conversely, the final repeal list is a selected residue after objections, not a transparent census of everything actors initially considered obsolete.

That distinction should be carried into later item-level diffs. A failed candidate can remain historically important even though it disappears from the reported bill.

## Relation to the 1965 finding

The existing 1965 packet documents a stronger and more explicit procedure: standing-committee chairmen were asked whether they retained an interest in proposed reports; four repeal candidates were removed before introduction and sixteen afterward, while two reports were changed from quarterly to annual frequency.

The new 1945 evidence establishes an earlier family resemblance:

```text
1945: hearings -> objections -> several candidates removed
1965: formal committee consultation -> 20 candidates removed + frequency modifications
1995: agency proposals -> committee oversight review -> candidate rescues/modifications
```

Safe claim: **selective resistance to report elimination is observable by 1945**.

Unsafe claim: **the 1965 jurisdiction-filter procedure was inherited directly from 1945**. Documentary transmission is not established.

## Hindsight risks

1. Do not call the removed 1945 items `committee-of-jurisdiction rescues` unless the hearing record identifies the objectors and their institutional role.
2. Do not infer that every objection was accepted; Cochran only establishes that several objections resulted in removal.
3. Do not infer the size of the original candidate set from the final 64 items.
4. Do not treat the final repeal list as an objective set of useless reports. It is the output of a contested selection process.
5. Do not project the formal 1965 consultation procedure backward into 1945.
6. Do not equate removal from the repeal bill with permanent survival; rescued requirements may reappear as repeal candidates in later rounds.

## Suggested repository integration

Cross-link this packet from:

- `1928-1941-1945-report-pruning-direct-precedent-and-revival.md`;
- `1954-1965-report-pruning-recurring-review-cycle.md`;
- `1965-1995-report-pruning-to-default-sunset.md`.

The 1954–1965 synthesis should be softened where it makes 1965 appear to be the first evidence of candidate filtering. What is distinctive in 1965 is the **documented formal standing-committee consultation and quantified attrition**, not the first existence of objections/rescues.

Candidate Problem Episode fields:

- `candidate_set_known`;
- `screening_stage`;
- `objector_identity`;
- `objection_reason`;
- `candidate_removed_before_report`;
- `candidate_removed_after_report/introduction`;
- `final_disposition`.

## Remaining uncertainty / source debt

The highest-value next source is now the **three-day H.R. 2504 hearing record or committee files**. It could reveal:

- the initial candidate list before objections;
- which items were removed;
- who objected;
- whether objections concerned oversight value, administrative burden, statutory jurisdiction, substantive policy, or alternate information channels;
- whether any rescued 1945 items had already appeared in H.R. 5508 in 1941;
- whether rescued items later returned in the 1954/1960/1965 repeal rounds.

A second target is the bill text at introduction/referral, if preserved separately from the reported version. If its candidate list exceeds 64, a literal diff can recover proposal attrition even without the hearing transcript.

## Next candidates

1. Recover the 1945 three-day hearing transcript/committee record and enumerate objection-triggered rescues.
2. Diff H.R. 2504 introduced/referral text against the reported bill and P.L. 79-615.
3. Cross-match any rescued 1945 statutory citations against H.R. 5508 (1941) and later 1954–1965 pruning packages.
4. Only after objector identity is recovered decide whether 1945 should be coded as a true `jurisdiction filter` or the broader `contested candidate filter`.