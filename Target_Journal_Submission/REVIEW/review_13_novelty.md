# Review round 13 — response to the anticipated decision "limited new contribution and novelty"

## Diagnosis
The anticipated editor comment is the standard desk-rejection wording for a perceived lack of novelty. Reading the
previous draft as an editor would (title, abstract, highlights, first two pages), the objection was understandable:

* the introduction stated "We do not claim a new conformal theory" and described the method as one that
  "instantiates" existing work;
* the guarantees rested on an informal argument by reference;
* the contributions were listed as analyses rather than as deliverables;
* the title was a question, not a statement of what the paper provides.

The content was undersold, but there was also a real gap: no formal result and no tool beyond the interval itself.

## Changes

| # | Change | Type | Evidence |
|---|---|---|---|
| 13.1 | **Formal results.** Proposition 1 (marginal coverage for a score that depends on a random reference set, three nested levels, unequal lot sizes, finite number of replay episodes) and Proposition 2 (lot-level assurance), with proofs. | New theory, modest: an extension and formalisation of hierarchical conformal prediction for this setting | Appendix A; unit tests check both statements by simulation |
| 13.2 | **Reference-sampling planner.** The replay gives, from past lots only, the interval width to expect for each number of reference samples. Planned and realised widths compared on 150 combinations (5 seasons × 3 predictors × 5 budgets × 2 variants). | New tool and new experiment | Median absolute relative error 7 %; mean −2 %; −21 % for the season with two source seasons; Section 15, Fig. 13, Table S15 |
| 13.3 | **Reframing.** New title; contributions grouped as new evidence / new methods / new evaluation; an explicit positioning list against five strands of prior work; removal of the self-deprecating sentence, replaced by an exact statement of what is inherited and what is new. | Presentation | Sections 1 and 3 |
| 13.4 | Abstract and highlights rewritten around the deliverables (few-shot calibration with proofs, lot-level assurance, planner, decision analysis, soil replication). | Presentation | 246 words; highlights ≤ 85 characters |

## Claims checked for over-statement in this round

| Claim | Check | Outcome |
|---|---|---|
| "first lot-level audit" | Cannot be proven by search | Qualified: "to our knowledge the first for fruit NIR" |
| Prior uncertainty studies "evaluated within one population" | Only abstracts/records were read; one preprint mentions several seasons | Reworded so that nothing is asserted about what those studies did beyond what their records state |
| "proven guarantees" | Propositions hold under lot exchangeability and fixed constants | The limits are stated next to the propositions and in Section 4.7; abstract says LotCP-A "targets" the property |
| Planner is "usable" | 7 % median error, but 21 % over-estimate with two source seasons | Both figures reported |

## What is and is not new, stated plainly

* **Inherited:** hierarchical exchangeability and the group-balanced conformal quantile (Lee et al., 2023); the
  idea of PAC-type statements across tasks (Park et al., 2022); bias adjustment from reference samples
  (chemometric practice).
* **New here:** the lot-specific scale from repeated scans (label-free); the replay calibration of a few-shot bias and
  scale correction with season-held-out residuals; the propositions for that construction; the lot-level assurance
  for calibration maintenance; the sampling planner; the lot-level, budget-indexed evaluation protocol with a
  decision analysis; the evidence across seven mango seasons and two soil libraries; the negative result on shrinkage.

## Residual risk
An editor can still judge the methodological step too small for the journal, or the paper too statistical for its
readership. That judgement cannot be removed by further work on the manuscript. If the journal desk-rejects on
novelty, the same manuscript is a natural fit for chemometrics and precision-agriculture journals with a methods
readership (for example Chemometrics and Intelligent Laboratory Systems, Computers and Electronics in Agriculture,
Postharvest Biology and Technology), which were excluded here only by the 72-day acceptance constraint.
