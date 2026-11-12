# Review round 1 — Reviewer #1 (general referee, Smart Agricultural Technology)

Manuscript version reviewed: first complete draft (commit "Manuscript build pipeline, README, results text").
Recommendation at this stage: **major revision**.

## Summary of the submission
The paper measures the coverage of prediction intervals for mango dry-matter content on later harvest seasons
and proposes a few-shot conformal calibration (LotCP / LotCP-S) that uses reference fruit of the new lot.

## Issues

| # | Severity | Issue | Fix requested | Outcome |
|---|---|---|---|---|
| 1.1 | MAJOR | One data set, one fruit, one instrument family. Every conclusion could be specific to it. | Add a second data set with lot and season structure, or state the limitation prominently. | **Not fixable with public data.** Zenodo and Mendeley were searched for NIR data with nested lot/season structure (candidates examined: NeoSpectra soil library, Austrian soil library, wheat DON spectra, SpectroFood); none has many groups with repeated reference sampling. Limitation now stated first in Section 13 and in the audit. Partial mitigation: unseen-region, unseen-cultivar, two-season-source and single-instrument protocols on the same data. |
| 1.2 | MAJOR | The standard chemometric maintenance tools are missing as baselines: slope-and-bias correction, and "spiking" (refit with the new samples). Without them a spectroscopist will not accept the comparison. | Implement both. | **Fixed by new experiments.** Slope/bias + source quantile added to the main evaluation (Table 4); spiking evaluated at m = 10 (`experiments/spiking.py`, Table S11). Slope/bias is worse than mean correction at m = 5 and similar from m = 10; spiking is clearly worse than mean correction. |
| 1.3 | MAJOR | "Largest public mango data set" is asserted without evidence. | Remove or support. | **Fixed**: wording changed to "a large public". |
| 1.4 | MAJOR | The instrument model and manufacturer were stated without a source that the authors had checked. | Verify or remove. | **Fixed**: the wavelength range, Savitzky–Golay pre-treatment and "harvest population" wording were verified against the abstract of Anderson et al. (2020); the unverified instrument model was removed; the remaining description is attributed to the cited papers and flagged in Limitations. |
| 1.5 | MODERATE | Pooled coverage of season-fold calibration (0.90) is presented next to a per-season range of 0.82–0.99; the first draft said "under-coverage in three of four later seasons" although all four are below 0.90. | Correct the sentence. | **Fixed** (text now generated from the per-season table). |
| 1.6 | MODERATE | Section 6.1 claimed that next-season error lies "between lot-fold and season-fold estimates or above"; for 2017 it lies below the lot-fold estimate. | Correct. | **Fixed**: the sentence now states what Table 2 shows. |
| 1.7 | MODERATE | No decision-level analysis (probability of wrongly accepting a lot against a DMC specification; one-sided bounds). | Add, or list as limitation. | **Not done**; listed as a limitation (one-sided bounds not studied). A specification threshold differs by cultivar and market and was not available in the data. |
| 1.8 | MODERATE | Equations lost their numbers in the DOCX. | Fix. | **Fixed** (numbers are part of the display equations). |
| 1.9 | MINOR | Table 3 contained an ablation row (HCP-mean at m = 0) identical to LotCP. | Remove. | **Fixed**. |
| 1.10 | MINOR | Table 2 printed seasons as "2017.00". | Fix. | **Fixed**. |
| 1.11 | MINOR | x-axis labels of Fig. 5 overlapped. | Fix. | **Fixed**. |

## Assessment after revision
The empirical finding (loss of coverage on later seasons for nine interval procedures) is solid within this data
set. The single-data-set limitation remains the main reason a referee could ask for more.
