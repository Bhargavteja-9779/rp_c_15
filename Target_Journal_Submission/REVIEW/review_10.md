# Review round 10 — final adversarial review (independent pass over the final manuscript, code and results)

Stance: find a reason to reject.

## Candidate fatal flaws

1. **Is the headline effect an artefact?** Checked independently of the earlier rounds by recomputing from
   `results/raw_results.csv` and from scan-level indicators: lot-macro coverage of sample-fold split CP 0.823;
   scan-weighted 0.820; by season 0.76–0.88; by predictor 0.76–0.82; leave-one-season-out protocol 0.849.
   The effect is present in every season, predictor and weighting. **Not an artefact.**
2. **Leakage that would favour the proposed method?** The only target information used is the m reference
   samples of the lot under test, and their scans are removed from the evaluation set. Variance components,
   pseudo-count and quantile use source seasons only. The sample-split check shows no optimism. **None found.**
3. **Was the method tuned on the test seasons?** One design decision (the scale term) followed a look at PLS/2018.
   It is disclosed; 2018 is the method's worst season. **Disclosed weakness, not fatal.**
4. **Integrity of authorship (AI-generated study).** Not a scientific flaw but can end a submission at the desk.
   **Unresolved; depends on the human authors** (see round 9, item 9.3).

No scientific fatal flaw was found.

## Major weaknesses that remain (real ones only)

| # | Weakness | Fixable now? |
|---|---|---|
| M1 | Single data set / commodity / instrument family. | No. |
| M2 | Five target seasons; season-level uncertainty is large (pooled LotCP-S coverage moves 0.893–0.933 under a season jackknife). | No. |
| M3 | Efficiency advantage over the simplest baseline depends on repeated scans and vanishes by m ≈ 20 against target-only calibration. The contribution is therefore narrow: 3–10 reference samples with repeated scans. | No; stated. |
| M4 | The proposed method was not fully pre-specified (scale term). | No; disclosed. |
| M5 | The pre-designated variant (season-fold residuals) is not the best variant for m > 0. | Reported; not swapped. |
| M6 | Marginal guarantee only; 8 % of lot-draws (11 % of single-instrument unit-draws) still below 0.80 coverage at m = 10. | No; reported. |
| M7 | Methodological novelty is an instantiation of hierarchical conformal prediction. | No; stated. |
| M8 | Reference-sampling protocol is simulated on archived data, with random sampling assumed. | No. |

## Moderate weaknesses

| # | Weakness | Status |
|---|---|---|
| m1 | No one-sided bounds / decision analysis against a DMC specification. | Limitation. |
| m2 | Scores not adaptive to predicted DMC; lower coverage at the extremes. | Limitation. |
| m3 | PLS component selection shares data with calibration residuals. | Limitation. |
| m4 | Deep-ensemble / MC-dropout / QRF settings not varied. | Audit. |
| m5 | Likelihood-ratio estimator for weighted CP is linear. | Audit. |
| m6 | Lots within a season treated as independent in tests. | Stated; season counts given. |
| m7 | CNN: fewer epochs than planned; lot-fold residuals for one seed only. | Deviation D3. |
| m8 | Journal guideline compliance unverified. | Audit. |
| m9 | Three cited sources are preprints/archives; the concurrent work was read only through its archive description. | Stated in round 2. |
| m10 | Energy not measured. | Stated. |
| m11 | The "population = harvest lot" reading is the authors' interpretation of the data file. | Stated. |
| m12 | Manuscript length. | Round 7. |

## Minor points found in this pass and fixed

* Abstract and highlights updated to reflect the replicate-scan finding.
* Section 5.4 now lists the slope/bias and spiking baselines; Section 5.7 lists all post hoc additions (D4).
* A sentence in the discussion on the fold unit contradicted the per-season numbers ("safety margin"); rewritten
  from the data (lot-fold variant has no lower per-season minimum).
* Table 9 gained the split-constants and single-instrument rows.

Fewer than "ten major / twenty moderate" real weaknesses exist; none were invented to reach a count.

## Recommendation
Scientifically sound and honest within a narrow, clearly bounded claim. Reject-level risk comes from M1 and from
the authorship/AI-policy question, not from the analysis.
