# Review round 4 — Reviewer #4 (machine-learning methodology; code read against the manuscript)

The code in `src/` was read line by line against Sections 4 and 5.

## Contradictions found between code and manuscript

| # | Severity | Manuscript said | Code does | Resolution |
|---|---|---|---|---|
| 4.1 | MAJOR | (draft) CNN trained for 30 epochs | 20 epochs (protocol deviation D3) | Manuscript corrected; deviation listed in Section 5.7. |
| 4.2 | MODERATE | Eq. (2): mean over all K source lots | lots with a single sample are skipped when estimating variance components | No such lots exist in the data (minimum 10 samples per lot); a comment was not needed in the paper. Verified. |
| 4.3 | MODERATE | Eq. (6) weights "1/(K+1) per lot" | implemented as unit mass per lot plus unit mass at +∞ in a weighted quantile | Equivalent after normalisation; unit test `test_weighted_quantile_uniform_equals_split` covers the convention. |
| 4.4 | MODERATE | Section 4.5: replicate variance "of the new lot" | uses all scans of the lot, including those of reference samples; in calibration episodes it uses season-held-out predictions | Text now says "the lot's unlabelled scans"; consistent. |
| 4.5 | MODERATE | "pseudo-count chosen from {5,10,20,40}" | chosen only when m ≥ 2 and scale uses the references | Text states û² = σ̂² for m < 2. Consistent. |
| 4.6 | MINOR | Stored predictions | cast to float32 for storage | Negligible (< 1e-6 % DMC); documented in README. |
| 4.7 | MINOR | "No early stopping" | confirmed; fixed epoch budget, one-cycle schedule | Consistent. |

## Methodological issues

| # | Severity | Issue | Outcome |
|---|---|---|---|
| 4.8 | MAJOR | The evaluation stage wrote results only at the end; an interruption lost the run, and reruns could not be verified to give identical numbers. | Per-configuration caching added; reference draws are seeded from (config seed, target, model seed, alpha). The full evaluation was run three times in this project (before and after adding baselines); numbers of unchanged methods were identical in the generated tables. |
| 4.9 | MODERATE | LightGBM and CNN hyper-parameters are untuned defaults. | By design (no tuning on target seasons). The CNN nevertheless has the lowest point error (Table 2), so the predictors are not straw men. Stated in Section 5.3. |
| 4.10 | MODERATE | Deep ensemble has five members; MC dropout uses dropout 0.1, which may give small epistemic variance. | Standard settings; the finding that they under-cover under lot shift does not hinge on these values, because the missing variance is the lot effect. Not varied; noted in the audit as a baseline-sensitivity risk. |
| 4.11 | MODERATE | ACI is designed for sequential feedback; using it on m reference samples is an adaptation by the authors. | Described as such in Section 5.4. |
| 4.12 | MODERATE | Unit tests did not cover the evaluation metrics, the ACI helper or the split-constants path. | Tests added (`test_eval_metrics_and_aci`, `test_split_constants_keeps_coverage`); 15 tests pass. |
| 4.13 | MINOR | A Monte-Carlo test of the coverage guarantee exists only for exchangeable Gaussian lots. | Adequate as a correctness check of the implementation; the paper does not claim more. |

No implementation error affecting reported numbers was found.
