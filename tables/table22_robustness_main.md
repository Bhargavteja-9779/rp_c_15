| Predictor | LotCP-S | LotCP-R2 | LotCP-R | LotCP-S at α = 0.05 | R, plain quantiles | LotCP-A | LotCP-AR | AR, plain quantiles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SNV PLS | 2/5 | 5/5 (+7 %) | 5/5 (+16 %) | 5/5 (+24 %) | 4/5 (+1 %) | 2/5 | 5/5 (+8 %) | 3/5 (+2 %) |
| Published PLS | 2/5 | 5/5 (+11 %) | 5/5 (+18 %) | 5/5 (+25 %) | 3/5 (+0 %) | 2/5 | 5/5 (+12 %) | 4/5 (+6 %) |
| LightGBM | 2/5 | 5/5 (+9 %) | 5/5 (+15 %) | 5/5 (+26 %) | 3/5 (+0 %) | 2/5 | 5/5 (+9 %) | 3/5 (+3 %) |
| 1D-CNN | 2/5 | 5/5 (+8 %) | 5/5 (+16 %) | 5/5 (+25 %) | 4/5 (+0 %) | 1/5 | 4/5 (+8 %) | 4/5 (+4 %) |

Table: Table S22. Season-robust replay (forward chaining, five target seasons, m = 10, nominal 0.90; exploratory). Columns LotCP-S to 'R, plain quantiles': number of target seasons whose lot-macro coverage reaches 0.90. Columns LotCP-A to 'AR, plain quantiles': number of seasons in which at least 90 % of lot-draws reach 0.90 coverage (the lot-level target). In brackets: change of mean width relative to LotCP-S (marginal columns) or LotCP-A (lot-level columns). LotCP-R/R2: largest/second-largest per-season conformal multiplier; plain: per-season empirical quantile without the conformal correction (sensitivity analysis). Results for m = 5 are in results/cycle4.
