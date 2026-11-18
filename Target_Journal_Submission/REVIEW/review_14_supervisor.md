# Review round 14 — response to the supervisor's review (applied-research repositioning)

## Supervisor's recommendations and what was done

| # | Recommendation | Done | Where | Result (machine-generated) |
|---|---|---|---|---|
| 1 | Make the real-world harvest decision the central story; do not add an unrelated application | Yes | New title; abstract, highlights, Introduction, Fig. 1 (workflow), Sections 8–10, Discussion and Conclusion rewritten around the grower's four questions | — |
| 2 | Harvest-decision simulator: immature fruit accepted vs mature fruit withheld under different rules | Yes | `experiments/harvest.py`; Section 8; Table 7; Fig. 7 | 6 rules × 6 confidence levels × 5 reference budgets × 3 specifications × 2 predictors, 137 later-season lots, 20 reference draws per lot. At 15 % DMC: point prediction 13.4 % immature among accepted (89.9 % of mature fruit accepted); LotCP-S bound, 10 reference fruit, α = 0.10: 1.2 % (65.1 %); split-CP bound without reference fruit: 2.9 % (58.4 %). Lot level: premature harvests 7.3 % → 4.0 % at an unchanged 20 % delay rate. |
| 3 | Economic impact, with assumed costs clearly separated from measured results | Yes | Section 5.7 (assumptions stated in units of fruit value), Section 8.3, Table 8, Fig. 8; `src/statistics/harvest_analysis.py` | Expected cost 29–71 % below point decisions across four assumed cost ratios at the 15 % specification. Cost-derived confidence level α* = c_D/(c_I + c_D) within 1.4 % (PLS) and 0.0 % (CNN) of the best level in hindsight for LotCP-S, against 4.4 % for bias correction + source margin (PLS) and 12.6 % for split CP (CNN). Cost-optimal number of reference fruit: 3–5 for 1000-fruit lots; 0 for 200-fruit lots under these assumptions. |
| 4 | Make the sampling planner central | Yes | Fig. 1 workflow; Section 9 with a grower-oriented planner table (Table 9) | Planned vs realised width: median absolute error 7 %; widths 5.1 → 3.8 % DMC from m = 0 to 3, 3.5 → 3.4 from m = 10 to 20. |
| 5 | Practical decision interface | Yes (command-line prototype) | `src/tool/harvest_tool.py` (export / decide / demo); Section 10, Box 1; unit test `tests/test_harvest_tool.py` | Demo on the median-size 2021 lot, chosen by rule before its result was seen: lot bias −2.9 % DMC detected from 10 reference fruit; recommendation WAIT; all 30 non-reference fruit truly below 15 %; 100 % of lower bounds held. |
| 6 | Validate with a grower or laboratory on a new lot | **Not possible from here** | Limitations ("Retrospective, not prospective") with a concrete prospective protocol | The paper states explicitly that it does not show reduced losses in practice. |
| 7 | Do not claim actual harvest-loss reductions | Yes | Abstract ("retrospective harvest simulation"), Introduction, Section 8.3 ("assumed"), Limitations, Conclusion, cover letter | — |
| 8 | Recommended title | Yes | "Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons" | — |

## New honest findings this round brought out
* At fruit level, once the lot bias is corrected and the confidence level is free, LotCP-S and the simpler
  "bias correction + source margin" trace practically the same trade-off curve. The large decision benefit comes
  from using reference fruit and a bound at all; the specific benefit of LotCP is calibration (a cost-derived
  level that works across predictors), the lot-level assurance, and the planner. This is stated in Sections 8.1,
  8.3 and 15.
* With few fruit per lot (200) and the assumed reference-test cost, destructive testing does not pay; the bound
  without reference fruit is then preferable.

## Structure and length
Main text reorganised: audit (6) → few-shot calibration (7) → harvest decisions and economics (8) → planner (9)
→ prototype (10) → validation (11–14) → discussion. Detailed robustness, cost, error analysis and the deviation list
moved to Supplementary Notes S1–S4; five validation tables moved to the supplement (S20–S24). Main text ≈ 13,700
words excluding tables, captions and references; 59 pages double-spaced with line numbers.

## Administrative changes requested by the author
Authors P N Bhargav Teja (first) and Ragavan K (corresponding); CRediT as specified (Ragavan K: Supervision);
no funding; no competing interests; data availability with direct dataset links; code available on reasonable
request. The generative-AI declaration was kept, worded to Elsevier's template, and must accurately describe the
use of AI.

## Remaining risks (unchanged by this round)
Prospective validation absent; assumed costs; single fruit data set; affiliations/e-mails to be filled; journal guide
to be checked; AI-use policy to be confirmed by the authors. Acceptance cannot be guaranteed.
