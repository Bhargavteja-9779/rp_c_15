# Review round 12 — second revision: a new methodological element (lot-level assurance)

## Motivation
After round 11 the strongest remaining scientific objection was conceptual: the method's guarantee is marginal
over lots, while a harvest decision concerns one lot. Empirically, near-nominal average coverage left about
three lots in ten below the nominal level and 8 % of lot-draws below 0.80 (round 10, M6). Target-only
calibration, the natural alternative, is valid per lot only on average over reference draws and does no better.

## What was added
**LotCP-A** (Section 4.8, Eq. 8; `LotCP(assure=delta)`): the half-width multiplier is the (1 − δ) quantile over
past lots of each lot's own (1 − α) score quantile, obtained in the same episodic replay. Under lot
exchangeability the realised coverage within a new lot is ≥ 1 − α with probability ≥ 1 − δ. A unit test checks
this on simulated lots that differ in bias and scale (`test_lotcp_assured_lot_level_guarantee`).

Prior art checked: PAC prediction sets for meta-learning (Park, Dobriban, Lee, Bastani, NeurIPS 2022; verified
on arXiv 2207.02440) and the second-moment coverage of Lee et al. (2023) give statements of this type for tasks /
groups. LotCP-A is the application of that type of statement to calibration maintenance with a few-shot bias and
scale correction; it is described as such, not as new theory.

## Results (machine-generated; Table 14, Fig. 12, Tables 8/S13)

| Setting (1 − α = 0.90, δ = 0.10, m = 10) | Lots reaching 0.90 coverage: LotCP-A | LotCP-S | Target-only, centred | Bias corr. + source CP |
|---|---|---|---|---|
| Mango, PLS, forward chaining | 92 % | 69 % | 88 % (78 % at m = 20, 71 % at m = 30) | 77 % |
| Mango, LightGBM / CNN / leave-one-season-out | 90–91 % | 62–69 % | — | — |
| KSSL soil projects | 93 % | 70 % | 66 % | 55 % |
| LUCAS organic carbon / pH (campaign shift) | 87 % / 83 % | 56 % / 47 % | 65 % / 66 % | 58 % / 46 % |

Cost: +25 % width at m = 10, +21 % at m = 20 (mango, PLS). Share of lot-draws below 0.80 coverage: 8 % → 1 %.

## Issues found in this round

| # | Severity | Issue | Outcome |
|---|---|---|---|
| 12.1 | MODERATE | Across LUCAS campaigns the assurance is missed by 3–7 points; by season on mango it ranges 86–98 %. | Reported in Section 14; it is the same non-exchangeability that limits the marginal method. |
| 12.2 | MODERATE | Without reference samples the assurance is not attained (88 %) and intervals are very wide. | Reported. |
| 12.3 | MODERATE | The statement concerns realised coverage among the scanned fruit of the lot and assumes exchangeable lot sizes. | Stated in Section 4.8. |
| 12.4 | MINOR | The abstract said LotCP-A "guarantees"; under non-exchangeable seasons it only targets the property. | Reworded to "targets". |
| 12.5 | MINOR | Abstract exceeded 250 words after the addition. | Trimmed (see build output). |
| 12.6 | MINOR | LotCP-A was added after all other results were known (deviation D7). | Disclosed; its tuning-free definition leaves no free parameter that could have been fitted to the target lots. |

## Effect on the contribution
The paper now offers, beyond the measurement of the failure: (i) an efficient average-coverage interval for few
reference samples, (ii) a lot-level assurance that no compared method provides, including in the regime of 20–30
reference samples where (i) had no advantage, (iii) a decision analysis, (iv) external validation on soil
libraries. Acceptance still cannot be guaranteed; the non-scientific risks listed in `final_audit.md` are unchanged.
