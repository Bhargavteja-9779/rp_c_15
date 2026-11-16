# Final audit

## 1. Consistency audit (title ↔ abstract ↔ method ↔ code ↔ results ↔ conclusion)

| Check | How it was done | Result |
|---|---|---|
| Every number in abstract, text and tables matches the results | Text is stored with `{{placeholders}}`; `manuscript/build_manuscript.py` fills them from `results/metrics.json`, `tables/*.csv`, `results/robustness/*`. The built Markdown contains no unresolved placeholder. | Pass by construction. The few quantities written as words in the Discussion ("about a third wider", "0.82 to 0.99", "six to fourteen coverage points", "seven procedures") were checked by hand against Tables 3, 5 and 8. |
| Every figure is drawn from result files | `src/visualization/figures.py` reads `raw_results.csv`, stored predictions and robustness files. Fig. 1 is a schematic without data. | Pass. |
| Every equation corresponds to code | Eqs. (2)–(7) checked against `src/evaluation/lotcp.py` (round 4). | Pass. |
| Every experiment mentioned exists | Each analysis in Sections 6–11 maps to a stage of `run_all.py`; see table below. | Pass. |
| Title/abstract/conclusion claim no more than the results | Rounds 7, 8 and 10. The claim of advantage is bounded (3–10 reference samples, repeated scans). | Pass. |
| Abstract ≤ 250 words; highlights ≤ 85 characters | 249 words; longest highlight 85 (checked by the packaging script). | Pass. |

## 2. Claim → evidence map

| Claim | Evidence | Where |
|---|---|---|
| Split conformal intervals cover 0.82 instead of 0.90 on later-season lots; 28 % of lots below 0.80 | 137 target lots, 5 seasons, forward chaining; CI 0.787–0.855; every season and predictor | Table 3, 5, 8; Fig. 5 |
| Gaussian, QRF, CQR, deep ensemble, MC dropout also under-cover (0.77–0.84) | same lots | Table 3 |
| Hold-out unit orders coverage: sample < lot < season, in all five seasons | cross-conformal with three fold units | Table 5 |
| Season-fold calibration restores pooled coverage at 37 % more width, 0.82–0.99 by season | same | Tables 3, 5, S4b |
| Weighted CP is not a remedy | widest intervals, worst interval score | Table 3 |
| ≥ 3 reference samples per lot bring bias-correcting methods to ≥ 0.90 | 100 reference draws per lot and m | Table 4, Fig. 4 |
| LotCP-S: 0.914–0.919 coverage for m ≥ 3; best interval score for m = 3–20 among compared methods | paired Wilcoxon tests, Holm | Tables 4, 7 |
| No advantage over centred target-only CP from m = 20–30 | paired tests | Table 7, S6 |
| Advantage over bias correction at small m depends on repeated scans | paired tests of the no-replicate variant | Table S6b, Section 7 |
| Shrinkage does not matter; scale does; season folds matter only at m = 0 | ablation | Table 6, Fig. 6 |
| Coverage of LotCP-S is 0.905–0.919 across 3 predictors × 2 protocols | LightGBM/CNN (3 seeds), LOSO | Table 8, Fig. 7 |
| Bias-correction shortcut is not coverage-stable across predictors (0.88–0.94) | same | Table 8 |
| Robust to reference error, outlier screening, tuning constants; needs ≈ 40 past lots | robustness grid | Table 9, Fig. 8 |
| Holds for single-instrument units, unseen region/cultivar, two-season source | extra protocols | Table 9 |
| Slope/bias correction and spiking are not better | added baselines | Table 4, S11 |
| Remaining failures are driven by lot residual scale | lot-level correlation and subgroup coverage | Section 11, Fig. 9 |
| The coverage loss and its repair replicate on soil vis–NIR spectra (LUCAS 2009→2015: 0.63 / 0.40 → 0.87–0.90 with 5–20 local samples; KSSL projects: 0.88 → 0.91) | OSSL external validation, paired tests | Section 12, Table 12, Fig. 10, S13 |
| Shrinkage of the bias estimate is unsafe under a campaign shift | LUCAS: 0.70 vs 0.87 (pH, m = 5) | Section 12, Table 12 |
| LotCP-A keeps ≈ 90 % of lots at ≥ 0.90 realised coverage (mango 90–92 %, KSSL 93 %, LUCAS 83–87 %), against 62–70 % for LotCP-S; +25 % width | lot-wise quantile calibration; unit test of the guarantee | Section 14, Table 14, Fig. 12 |
| Marginal and lot-level guarantees hold for random reference sets, three levels, unequal lots | Propositions 1–2 with proofs; simulation unit tests | Appendix A |
| The interval width for each reference budget can be forecast from past lots (median error 7 %; −21 % with two source seasons) | 150 planned-vs-realised comparisons | Section 15, Fig. 13, Table S15 |
| A calibrated lower bound reduces non-compliant fruit among accepted from 13 % to 1 % at a 15 % specification | one-sided LotCP-S, 137 lots | Section 13, Table 13, Fig. 11 |

## 3. Reproducibility audit (as a stranger)

| Question | Answer |
|---|---|
| Can I install it? | `pip install -r requirements.txt` (exact versions in `requirements-lock.txt`). |
| Can I obtain the data? | `python -m src.data.download` fetches the public file and verifies its SHA-256. |
| Does the pipeline run? | `python run_all.py --mode quick` was executed from start to finish in this environment (all eight stages, ≈ 1 min after data caching); `pytest` passes (15 tests). |
| Can I reproduce the reported numbers? | `python run_all.py --mode full --from eval` recomputes everything from the stored cross-fitted predictions; this was run three times during the project and unchanged methods gave identical tables. Full retraining takes ≈ 3 h on 4 CPU cores. |
| Exact reproducibility caveats | CNN training is seeded but may differ in the last digits across hardware/BLAS; stored predictions are float32; the three full evaluations in this project were on the same machine type. A clean-room rerun on different hardware was **not** performed. |
| Manuscript build | Needs pandoc; the PDF additionally needs LibreOffice with the Math component and symbol fonts. |

## 4. Rejection-risk report

| # | Risk | Evidence | Severity | Mitigation | Fixed? |
|---|---|---|---|---|---|
| 1 | Novelty | Method instantiates hierarchical conformal prediction (marginal and, added in revision, lot-level PAC-type assurance); concurrent instrument-transfer study exists | Medium | Framed as applied contribution; prior art cited and separated; negative ablation results reported | Partly |
| 2 | Methodology | Scale term added after a look at one season/predictor; shrinkage removed after external validation; season-fold variant not the best for m > 0; coverage up to 3 points below nominal under a campaign change of residual scale | Medium | Disclosed as deviations D1, D4, D5; all variants reported on every data set | Disclosed, not removable |
| 3 | Data set | One fruit data set; external validation on two soil vis–NIR libraries (three tasks) added in revision; no prospective field trial | **Medium** (was High) | Soil validation replicates the main findings; extra shift protocols on the mango data | Partly |
| 4 | Statistics | Five seasons; lots within season treated as independent | Medium | Per-season tables, season jackknife, season counts for paired differences | Partly |
| 5 | Reproducibility | No clean-room rerun on other hardware; data must be downloaded separately | Low | Stored predictions, seeds, checksum, quick mode, tests | Mostly |
| 6 | Baselines | Ensemble/MC-dropout/QRF settings not varied; linear likelihood-ratio estimator for weighted CP | Low–medium | Standard settings; CNN is the most accurate predictor; stated | Partly |
| 7 | Generalisation | Advantage needs repeated scans and ≈ 40 past lots; marginal guarantee only | Medium | Stated in abstract, Sections 7, 9, 12, 13 | Disclosed |
| 8 | Writing | Long manuscript; dense statistics for an applied journal | Low–medium | Practical procedure paragraph; supplement holds full tables | Partly |
| 9 | Journal formatting | Guide for Authors could not be opened (HTTP 403); generic Elsevier format used | Medium | Listed items for the authors to check | No |
| 10 | Citations | 44 references checked against Crossref/arXiv/Zenodo/Mendeley records; 3 preprints/archives; the concurrent work known only from its archive description; statements about the data provenance rely on abstracts, not full texts | Medium | Claims about cited works kept to what abstracts/records state | Partly — **authors should read the full texts of Anderson et al. (2020, 2021), Lee et al. (2023) and the concurrent study before submission** |
| 11 | Journal scope | Statistical paper in an agricultural-technology journal | Low–medium | Agronomic framing, sampling recommendation | Mostly |
| 12 | Journal-specific reviewers | May still request a second fruit or a field trial | Medium | Soil validation and decision analysis added | Partly |
| 13 | Integrity / compliance | (a) The study was generated by an AI agent: Elsevier requires disclosure, human oversight and author responsibility; (b) JCR quartile/impact factor not checked in JCR itself, journal is in ESCI; (c) the ≤ 72-day criterion is met only on the publisher's reported average (69–72 days) | **High** for (a) | Truthful AI declaration drafted; verification duties listed for the authors; all unverified journal facts flagged in `journal_selection/` | No — requires the human authors |

No claim of zero risk or of acceptance is made.

## 5. Readiness decision

**Scientific content (after revision rounds 11–13): READY FOR SUBMISSION**, in the sense that no further experiment that is feasible with the
available public data and hardware would change or strengthen the conclusions; every weakness found in thirteen review
rounds was either fixed by experiment, corrected in the text, or stated as a limitation.

**Administrative readiness: NOT YET.** Before submitting, the human authors must
1. verify the analysis and take responsibility for it (rerun `run_all.py`, read the code, read the key references in full);
2. complete author names, affiliations, CRediT, funding, repository URL/DOI;
3. check the manuscript against the journal's live Guide for Authors and its current generative-AI policy;
4. confirm the journal's JCR quartile/impact factor in JCR if their institution requires it.
