# Rudolf Unger: literary Problemgeschichte as a negative control

## Status

First-pass source and historiography packet. This note addresses an open item in `docs/PROBLEMGESCHICHTE.md`: compare Rudolf Unger's literary Problemgeschichte with later historicized models.

## Finding

Unger is not simply an early version of the repository's Problem Episode method. His program is a useful negative control because it treats literature as a mode of working on largely transhistorical, in-principle unresolved "human problems" (love, death, fate, existence). That makes his approach close to Hartmann at precisely the point where this repository must remain cautious: problem identity is strongly pre-structured before individual historical episodes are reconstructed.

A later historiographical reconstruction by Carlos Spoerhase describes Unger's literary Problemgeschichte as assuming "überzeitliche und unveränderliche Probleme" confronted by the poet, and reconstructing literature as attempted treatment of problems such as death or love. Spoerhase binds the central evidence to Unger's 1924 `Literaturgeschichte als Problemgeschichte`, especially the 1966 reprint pp. 155–167, and notes Unger's language of the "großen, ewigen Rätsel- und Schicksalsfragen des Daseins" and "elementare[n] Probleme des Menschenlebens".

This matters because the repository currently describes Werle's literary Problemgeschichte as relatively close to our practical use. Unger's older program should be separated sharply from that later historicization.

## Actor-level problem: Unger 1908

Unger’s 1908 `Philosophische Probleme in der neueren Literaturwissenschaft` was initially a disciplinary-methodological intervention. Contemporary and later histories bind it to his opposition to a narrowly philological/positivist literary history and his demand that modern literature also be investigated with philosophical, psychological, aesthetic, ethical, religious-philosophical and historical-philosophical methods.

So the actor-level problem in 1908 should not be rewritten as:

> How can we reconstruct historically emergent Problem Episodes?

A safer formulation is:

> How can literary history move beyond atomistic/positivist accumulation and interpret literary works as artistic formations and documents of broader intellectual life?

Evidence strength: **medium-high**. The 1908 publication is independently catalogued (Munich: Spiegelverlag, 30 pp.); the methodological characterization is supported by modern disciplinary histories quoting the 1929 reprint at pp. 13–18. Direct page-image verification of the 1908 original remains desirable.

## Actor-level problem: Unger 1924

By 1924, `Literaturgeschichte als Problemgeschichte` explicitly proposes problem history as a means of geisteshistorische synthesis. The problems are not primarily finite scientific questions awaiting a determinate solution. In the passages bound by Spoerhase to the 1924 essay (1966 reprint pp. 155–167), Unger treats the central objects as enduring existential/metaphysical residues: love, death, fate, and related "human problems" that literature interprets or works through.

This yields a model approximately like:

```
transhistorical / elemental human problem
        ↓
historically and individually situated consciousness
        ↓
literary Gestaltung / Deutung
        ↓
series of literary treatments
```

The history lies heavily in the treatments and configurations, not necessarily in the emergence of the problem itself.

Evidence strength: **medium-high** for the model, because the page-bound reconstruction is strong and cites the primary text precisely; **not yet direct-image high** because this pass did not recover a clean public scan of the 1924 original.

## Later reconstruction: Spoerhase and Werle

Carlos Spoerhase's `Dramatisierungen und Entdramatisierungen der Problemgeschichte` is especially useful because it distinguishes older literary Problemgeschichte from newer historicized approaches.

He reconstructs Unger as assuming transhistorical and unchanging problems and identifies the key methodological danger: the question "who has a problem?" can disappear behind "which problems exist?". He also distinguishes later literary Problemgeschichte that treats problems as context-modeling and explanatory categories rather than as a fixed repertoire of eternal human questions.

Dirk Werle similarly distinguishes Hartmann's immanent philosophical Problemgeschichte from Unger's literary version: Unger foregrounds the relation between problems and literary texts, i.e. a mode of contextualization. This is an important difference, but it does **not** by itself make Unger evidence-first or historically emergent in the repository's sense.

## New methodological consequence for this repository

### Problem-domain prior test

Before accepting a long problem chain, ask whether the domain of possible problems was fixed in advance by an anthropological, philosophical, disciplinary, or normative theory.

```
pre-given problem repertoire
        +
historical texts classified as treatments
        !=
historically demonstrated problem continuity
```

Candidate fields for episode/relation review:

```yaml
problem_domain_prior:
  status: none | actor_explicit | researcher_explicit | suspected
  source: []
  effect_on_identity_claim: ""
```

Do **not** add this to the validator yet. It should first be tested on non-literary chains.

### Topic/problem warning

Unger also provides a strong warning against collapsing topic, motif, existential concern, and historical problem:

```
love / death / freedom / fate
as recurrent themes
        !=
one continuous historical problem
```

A recurrent topic can host multiple historically distinct problems with different presuppositions, stakes, causal models, and answer criteria.

## Hindsight risks

1. **Anthropological backprojection** — a research tradition defines a small set of universal human problems, then reads historical texts as treatments of them.
2. **Theme-to-problem collapse** — recurrence of death/love/freedom is treated as evidence that the same problem persisted.
3. **Answer-implies-question circularity** — a literary work is classified as an answer to a problem, then used as the sole evidence that the problem existed.
4. **Disciplinary-purpose leakage** — Unger's own need for synthetic literary history can create the unity that is later attributed to the historical material.

## Evidence table

| Claim | Evidence | Strength |
|---|---|---|
| Unger's 1908 program opposed narrow positivist/philological literary history and demanded broader philosophical methods | 1908 bibliographic witness; modern disciplinary history with page-bound quotations from 1929 reprint | medium-high |
| Unger's 1924 program treats central literary problems as enduring existential/metaphysical human problems | Spoerhase 2010, with exact bindings to Unger 1924/1966 pp. 155–167 | medium-high |
| Unger's model differs from Hartmann by foregrounding problem–literary-text contextualization | Werle 2006 | high as later reconstruction |
| Later historicized literary Problemgeschichte can use problems as context/explanation without a fixed eternal repertoire | Spoerhase 2010 discussion of Werle | high as later reconstruction |
| Unger's 1924 exact wording and page layout | direct 1924 scan not recovered in this pass | unresolved |

## Suggested repository changes

1. Add an Unger subsection to `docs/PROBLEMGESCHICHTE.md` between Hartmann/Gadamer and Werle.
2. Mark the existing checklist item "调查 Rudolf Unger..." as first-pass complete, while retaining a direct-scan debt.
3. In the Werle section, explicitly say that "literary Problemgeschichte" is internally divided: Unger's older model presupposes a strong repertoire of elemental human problems; Werle's newer model historicizes problem/context relations much more radically.
4. Keep `problem_domain_prior` as a research-note candidate until tested against repository episodes.

## Sources

### Primary / near-primary witnesses

- Rudolf Unger, `Philosophische Probleme in der neueren Literaturwissenschaft`, Munich: Spiegelverlag, 1908, 30 pp. Bibliographic witness: Vienna City Library / Art Database.
- Rudolf Unger, `Literaturgeschichte als Problemgeschichte. Zur Frage geisteshistorischer Synthese, mit besonderer Beziehung auf Wilhelm Dilthey`, Berlin, 1924.
- Rudolf Unger, `Aufsätze zur Prinzipienlehre der Literaturgeschichte`, Berlin, 1929, containing the 1908 and 1924 texts.

### High-quality later reconstruction

- Dirk Werle, "Modelle einer literaturwissenschaftlichen Problemgeschichte", `Jahrbuch der Deutschen Schillergesellschaft` 50 (2006), 478–498.
- Carlos Spoerhase, "Dramatisierungen und Entdramatisierungen der Problemgeschichte", in Riccardo Pozzo / Marco Sgarbi (eds.), `Eine Typologie der Formen der Begriffsgeschichte`, Archiv für Begriffsgeschichte Sonderheft 7, 2010, esp. 114–121.
- Ralf Klausnitzer, "Institutionalisierung und Modernisierung der Literaturwissenschaft seit dem 19. Jahrhundert", in `Handbuch Literaturwissenschaft`, vol. 3, 2007, 70–147.

## Uncertainties / next candidates

- Recover a clean direct scan of Unger 1924 and verify original pp. 9–30 against the 1966 reprint pp. 137–170.
- Compare Unger's 1922 `Herder, Novalis und Kleist: Studien über die Entwicklung des Todesproblems...` with the 1924 program. This is the best candidate for testing how an "eternal" death problem is actually operationalized in a concrete historical chain.
- Test the Problem-domain prior test on one technology–labour chain. If the chain begins from a modern umbrella such as "technological unemployment", ask whether earlier episodes are being selected because they fit the modern domain rather than because actors transmitted or reformulated the problem.
