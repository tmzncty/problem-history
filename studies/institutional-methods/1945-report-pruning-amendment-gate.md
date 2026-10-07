# 1945: report-pruning amendment gate and jurisdictional rescue

Status: **M2 source-control / institutional-method candidate / companion to `1945-reporting-lifecycle-direct-transmission.md`**

This packet closes two source debts in the companion study: the House amendment history of H.R. 2504 and the basic Senate disposition. The new evidence shows that report pruning was not a mechanical application of an efficiency rule. Before passage, House actors explicitly paused the bill so committees with substantive jurisdiction could inspect the reports proposed for repeal; an objection then rescued two Indian-affairs reports from repeal. The Senate later accepted the House-amended bill without further amendment.

## 1. New finding: repeal was gated by subject-matter jurisdiction

In the June 19 House debate, Rep. W. Sterling Cole explained why H.R. 2504 had been held on the calendar: members wanted to make sure that committees having jurisdiction over the subject matters covered by the bill knew which reports were proposed for discontinuance. Cole had written to ranking minority members of interested committees.

This recovers an actor-level constraint missing from a simple `obsolete report -> repeal` model:

```text
central pruning proposal
        ↓
generic efficiency / obsolescence rationale
        ↓
subject-matter committees are alerted
        ↓
item-level objection can preserve a report
        ↓
only then does repeal proceed
```

Primary source: Congressional Record, House, June 19, 1945, pp. 6393-6395, reproduced in the legislative history of Public Law 79-615.

Evidence: **very high / contemporaneous floor statement plus enacted amendment**.

## 2. Concrete rescue: two Indian-affairs reports survived

Cole reported that the one substantive objection he received came from a South Dakota member who believed the Indian-affairs reports should not be discontinued. Cole relayed the objection to sponsor John J. Cochran, who agreed to remove items 9 and 10 from the repeal bill. Cochran then offered the amendment on the floor; the House agreed to it.

The two rescued items were:

1. the statement to the Speaker on the fiscal affairs of Indian tribes for whose benefit public or tribal funds were expended (36 Stat. 1077); and
2. the report of transactions under the revolving fund for loans to Indians and Indian-chartered corporations (48 Stat. 986).

This is direct evidence that **a report's survival could depend on the political/institutional value assigned by the committee community responsible for the underlying subject**, even inside a broad report-pruning programme.

Evidence: **very high**.

## 3. Problem-history implication: generic burden and substantive oversight are distinct problems

The House committee's generic problem was administrative: statutory reports could become duplicative, costly, stale, or unused. The floor amendment exposes a second problem that cannot be collapsed into the first: Congress could lose a valued oversight channel in a substantive policy domain if pruning was done only from the perspective of administrative efficiency.

Safe actor-level reconstruction:

```text
Problem A:
How do we eliminate low-value recurring reports?

        intersects with

Problem B:
How do committees retain information they regard
as necessary for oversight of a substantive domain?

        ↓
report-by-report political review
```

Candidate researcher fixture: **`jurisdictional rescue gate`** — a general reform proposal is filtered through actors responsible for the underlying policy domain, and an item survives when those actors contest the reformer's generic classification.

Do not promote this to validator status yet.

## 4. This changes how `report obsolescence` should be coded

The companion packet already shows heterogeneous technical reasons for repeal: duplication, superior substitute channels, on-demand retrievability, institutional transfer, and low-use/high-cost decay. The House amendment adds another dimension: **technical redundancy is not sufficient to predict repeal**.

A report can have at least two different values:

```text
administrative / informational efficiency value
        !=
committee / political oversight value
```

Therefore an item-level model should preserve both the executive/administrative rationale for discontinuance and any congressional jurisdictional response.

## 5. Senate disposition

The legislative-history compilation records the sequence as follows: House Report 79-311 reported H.R. 2504 without amendment; the House passed it on June 19 with amendments; the Senate Committee on Expenditures in the Executive Departments later reported the House-amended bill without amendment as S. Rept. 79-519; the Senate ultimately passed it without further amendment.

This establishes that the item-level rescue was not undone in the Senate. However, the present evidence does **not** yet show whether S. Rept. 79-519 independently reproduced the House's reporting-lifecycle rationale or simply accepted the revised bill. That remains a source debt.

Evidence: **very high for procedural disposition; unresolved for Senate problem formulation**.

## 6. Historical actors / later reconstruction / researcher reconstruction

### Historical actors

The House floor record directly supports the following:
- H.R. 2504 was deliberately delayed so committees with jurisdiction over affected subject matters could be alerted;
- at least one substantive objection was received;
- that objection caused two Indian-affairs reports to be removed from the repeal list;
- the House enacted the rescue amendment before passage.

### Later reconstruction

A later legislative-history compilation makes the bill sequence easy to recover and confirms that the Senate accepted the House-amended text. It should not substitute for the Congressional Record when describing the House actors' own reasons.

### Researcher reconstruction

The labels **`jurisdictional rescue gate`**, **`generic-pruning problem`**, and **`substantive-oversight problem`** are present-day analytical fixtures. They are not actor vocabulary.

## 7. Hindsight risks

1. **"The 1945 bill simply removed reports judged obsolete."** Too coarse. At least two proposed repeals were reversed after a subject-matter objection.
2. **"Administrative redundancy determines political dispensability."** False as a general inference. The amendment shows that committee oversight value can override a generic pruning classification.
3. **"No objection means a committee affirmatively judged a report useless."** Unsafe. Cole reported very limited replies; silence is not affirmative agreement.
4. **"The House amendment proves the Indian reports were objectively indispensable."** No. It proves that an actor with relevant political/jurisdictional concern successfully contested their repeal.
5. **"The Senate shared the House's full rationale."** Not yet proven. We know the Senate accepted the House-amended bill, not yet how S. Rept. 79-519 formulated the problem.

## 8. Evidence strength

| Claim | Strength | Basis |
|---|---|---|
| House delayed H.R. 2504 to alert committees with subject-matter jurisdiction | very high | June 19, 1945 Congressional Record |
| a South Dakota member objected to repeal of Indian-affairs reports | very high | Cole floor statement |
| Cochran removed items 9 and 10 in response | very high | floor amendment and passage |
| items 9 and 10 concerned tribal fiscal affairs and Indian revolving-fund transactions | very high | bill text read on House floor |
| Senate accepted the House-amended bill without further amendment | very high | legislative-history procedural record |
| S. Rept. 79-519 reproduced the House lifecycle rationale | **not proven** | report text still needs direct review |
| silence from other committees equals affirmative consent | **not proven / unsafe** | absence of response is not a positive statement |

## 9. Suggested repository changes

- Cross-link this packet from `1945-reporting-lifecycle-direct-transmission.md` under the warning that item-level repeal is politically filtered, not mechanically inferred from generic obsolescence.
- In any future event schema, keep `proposed_for_repeal`, `objected_to`, `rescued_by_amendment`, and `finally_repealed` distinct.
- Keep `administrative rationale` separate from `legislative/jurisdictional valuation`.
- When comparing 1928 -> 1945 -> 1954, ask not only why reports were nominated for repeal but also **which nominated reports survived and through what veto/rescue mechanism**.

## 10. Remaining uncertainty / next candidates

1. Directly inspect **S. Rept. 79-519** for Senate actor-level formulation.
2. Recover the identity and committee position of the South Dakota member referred to by Cole, if the correspondence or committee records survive.
3. Compare the 64-item introduced/reported list with the final enacted list to determine whether the two Indian reports were the only House rescues.
4. Apply the same `proposed -> contested -> final` diff to the 1928 and 1954 pruning episodes.
5. For 1954 H.R. 6290, inspect H. Rept. 83-1193 for evidence that the 1945 precedent or a similar jurisdictional consultation mechanism was explicitly reused.

## 11. Compact finding

> The 1945 report-pruning episode was not a mechanical purge of reports classified as obsolete. House actors deliberately held H.R. 2504 so committees with substantive jurisdiction could inspect proposed repeals. A South Dakota member objected to eliminating two Indian-affairs reports; sponsor John J. Cochran accepted the objection, and the House amended the bill to preserve them. This reveals a second problem inside report-pruning reform: administrative efficiency had to be balanced against committee-specific oversight value. `Report nominated as obsolete` therefore cannot be treated as equivalent to `report politically dispensable`, and silence from consulted committees cannot be treated as affirmative agreement.