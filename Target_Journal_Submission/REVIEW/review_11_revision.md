# Review round 11 — revision after the ten rounds (response to the remaining "reject-level" risks)

Rounds 1–10 left two weaknesses that a referee could use to reject: a single data set (M1) and no
decision-level analysis (m1). This round removed the second and substantially reduced the first, and in doing
so found a real defect in the proposed method, which was fixed.

## What was added

| Addition | Why | Result |
|---|---|---|
| **External validation on the Open Soil Spectral Library (vis–NIR)**: LUCAS 2009 → 2015 (organic carbon, pH; 467 target grid cells, 18,393 → 21,782 samples) and KSSL held-out survey projects (total carbon; 79 projects, 19,807 samples). `src/data/soil.py`, `experiments/soil_external.py`. | Independent material, spectral range, instrument and chemistry; local "spiking" is established practice there, so the reference-sample setting is native. | The coverage loss replicates and is larger across campaigns (0.63 and 0.40 at nominal 0.90); small across exchangeable projects (0.88), as theory predicts. Five local samples restore 0.87–0.91 with LotCP-S. LotCP-S is significantly better than the bias-correction shortcut on LUCAS and not significantly worse than any baseline at m ≤ 10 on any task. |
| **Harvest-decision analysis** with one-sided lower bounds against a DMC specification. `experiments/decision.py`. | The interval has to change a decision to matter to this journal's readers. | Point-prediction rule: 13 % non-compliant among accepted fruit, 45 % of lots above 10 %. LotCP-S lower bound (m = 10): 1 %, 6 % of lots, while accepting more compliant fruit (65 %) than the uncalibrated split-CP bound (58 %). |

## Defect found and fixed

| # | Severity | Finding | Action |
|---|---|---|---|
| 11.1 | **MAJOR (method)** | The pre-specified empirical-Bayes shrinkage of the bias estimate under-corrects when the new population is shifted by more than the between-lot variance of the source: on LUCAS pH, coverage 0.70 at m = 5 against 0.87 with the plain mean. On mango it had been immaterial. | Shrinkage removed from the reported method (plain mean is the default in `LotCP`); shrinkage versions kept as ablations on every data set; protocol deviation D5; **all mango experiments were rerun** with the new default (headline numbers changed in the third decimal only). |
| 11.2 | MODERATE | With the new default, the reference-scale-only variant is significantly *worse* than the bias-correction shortcut at m = 3 on mango (p = 0.004); the previous text said "not different". | Text corrected from the test table. |
| 11.3 | MODERATE | On LUCAS, LotCP-S stays up to three points below nominal coverage: a between-campaign change in residual scale is not absorbed. | Reported in Section 12, Discussion and Limitations as a limit of the method. |
| 11.4 | MODERATE | A draft sentence in the Discussion said coverage is lost "by ten points" across exchangeable projects; the figure is two points. | Corrected. |
| 11.5 | MINOR | The soil analysis uses PLS only, 30 reference draws, and lots defined by one-degree cells. | Stated in Limitations. |

## Status of the earlier major weaknesses after this round

| Weakness (round 10) | Status |
|---|---|
| M1 single data set | **Reduced**: three additional tasks on two independent soil libraries. Still one *fruit* data set and no prospective field trial. |
| M3 advantage depends on repeated scans | **Refined**: true on mango; on LUCAS the advantage exists without repeated scans because the shortcut under-covers. |
| M5 pre-designated variant not the best | Unchanged (reported). |
| m1 no decision analysis | **Fixed.** |
| Method defect (shrinkage) | **Found and fixed** in this round. |

## What this round cannot change
Acceptance cannot be guaranteed. The authorship/AI-policy question (round 9, item 9.3), the unverified Guide
for Authors and the absence of a prospective orchard trial remain and are outside what further computation can fix.
