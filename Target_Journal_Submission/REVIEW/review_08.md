# Review round 8 — Reviewer #8 (a competing researcher with a similar method)

Position taken: "This is hierarchical conformal prediction with a bias correction every chemometrician already
applies. The reported gain is produced by something else."

| # | Severity | Claim by the competitor | Test | Verdict |
|---|---|---|---|---|
| 8.1 | MAJOR | "Bias correction plus the ordinary conformal quantile already solves the problem." | Included as a baseline from the start; compared by paired tests; evaluated on three predictors. | **Partly valid.** With PLS it reaches ≥ 0.92 coverage from m = 3 and its interval score is not significantly worse than LotCP-S at m = 3. It is over-covering with PLS (0.94), under-covering with LightGBM (0.88) and wider for m ≥ 5. The paper now calls it "a strong baseline" and explains why its coverage is not controlled. |
| 8.2 | MAJOR | "The gain comes from repeated scans, which you give to your method and not to mine." | Paired tests of the LotCP-S variant without replicate information (Table S6b). | **Valid.** Without the replicate term: no significant difference at m = 3, 5, 10. The paper states this in Sections 7 and 12 and in the abstract and turns it into a recommendation (scan each fruit two or three times). |
| 8.3 | MAJOR | "Slope/bias correction or spiking would do as well." | Both implemented. | **Not valid.** Slope/bias: worse at m = 5, equal from m = 10 but never better than LotCP-S; spiking: lot-level RMSE 1.34 (×1) and 1.16 (×20) against 0.98 for mean correction. |
| 8.4 | MAJOR | "Target-only conformal prediction has a real per-lot guarantee; yours is marginal." | Compared at every m. | **Valid for m ≥ 20**, where it matches or beats LotCP-S and has smaller coverage error; not available for m < 9 and 34 % wider at m = 10. Stated as the boundary of the contribution. |
| 8.5 | MODERATE | "Season-held-out residuals are an expensive gimmick." | Ablation with lot-fold residuals. | **Valid for m > 0** (lot-fold variant: 0.908 coverage, better interval score, no lower per-season minimum); **not valid for m = 0** (0.846–0.861 vs 0.894–0.900). Reported as found; the pre-designated variant was not swapped after the fact. |
| 8.6 | MODERATE | "Your data set favours you: many past lots." | Calibration restricted to 10–80 past lots. | With 20 lots the method is conservative (0.946, +12 % width); about 40 lots are needed. Reported. |
| 8.7 | MODERATE | "Your CNN/LightGBM baselines are weak, so model-based uncertainty looks bad." | The CNN has the lowest RMSEP of the three predictors; the ensemble has the best interval score at m = 0 despite under-coverage. | Not valid as a fairness objection, but the paper says explicitly that these methods give the best m = 0 interval score. |
| 8.8 | MINOR | "The name suggests a new method." | Framing changed (round 2). |

After this round the manuscript's claims are those the competitor could not knock down: the coverage loss; the
value of ≥ 3 reference samples; an efficiency advantage of LotCP-S for few reference samples that depends on
repeated scans; stability of its coverage across predictors.
