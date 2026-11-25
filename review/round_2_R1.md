<!-- Reviewer 1 (methodology/statistics), fresh-context agent, round 2, 2026-11-25 -->

**Reviewer 1 (methodology and statistics)**

**(1) Score: 6/10. Recommendation: major revision.**
The paper is unusually candid. It reports by-season results and figures without 2017, labels what is exploratory, and does not hide that the confirmation failed. Most numbers reproduce. But some statements in the highlights, discussion and abstract are wrong or overstated, and the season-level confidence intervals are computed for a different quantity than the estimate printed next to them.

**(2) Concerns**

1. **MAJOR: the season-level CIs are for a different quantity than the estimate shown.** Table 4 prints the season-mean difference (each of the five seasons weighted equally). But `season_boot` in `experiments/season_inference.py` bootstraps the lot-weighted pooled mean, in which 2017 carries 56 of 137 lots. It then takes 2.5–97.5 percentiles from only five clusters. Example: for LotCP-S vs bias correction + source CP, coverage, SNV PLS, m=5, the printed estimate is −0.025 while the pooled difference is −0.011. A percentile bootstrap with five clusters also understates the spread.
   - I recomputed t-intervals (4 df) on the five season differences. The main conclusions survive: LotCP-S vs sample-fold split CP gives +0.056 to +0.153; the replay comparison at m=10 gives +0.006 to +0.022; LotCP-S vs bias correction, interval score, m=10, gives +0.050 to +0.488. The m=5 interval-score interval widens to −0.033 to +0.461.
   - Fix: report t-intervals on the season differences, or bootstrap the season-mean itself. Call these intervals descriptive, which matches Section 3.5's own statement that no season-level p-value is claimed.

2. **MAJOR: "every season" claims are false as written.**
   - Highlight 1 says standard error bars under-covered in every season. Not so: the Gaussian band covered 0.905 in 2017, and published-PLS split CP covered 0.916 in 2017 (Table 3 itself shows 1/5).
   - The Discussion says the bars were too narrow "in every season … by 6 to 13 coverage points". For sample-fold split CP the per-season shortfall is 1.6 points (2017, 0.884) to 14.0 points (2020, 0.760). The 6–13 range is the spread of pooled values across methods, not a per-season range.
   - Fix: limit the claim to seasons with ≥3 source seasons, or to SNV split CP.

3. **MAJOR: "reference fruit added no further saving" (abstract, highlight 4, conclusion) is conditional and partly contradicted by the supplement.**
   - The result holds at one assumed operating point (c_D = 1/9, c_R = 1.5, lots of 1000 fruit).
   - Supplementary Note S7 says the reference fruit add "a further, smaller saving" when withholding a mature fruit is relatively expensive, and that the cost-minimising m is 3–5 (5–10 for lots of 5000).
   - The Δ intervals (about ±1.4 units) cannot support "no saving", only "no detectable saving".
   - The point rule is a strawman: it costs 8.69, more than withholding everything (6.44). The "~5 units" gain follows from the asymmetric costs, not from calibration.
   - Fixes: (a) add an uncalibrated offset rule, such as the Gaussian-band lower bound; (b) add a sensitivity analysis over c_R in the main text; (c) rephrase as "no detectable further saving at the assumed operating point".

4. **MAJOR: framing and confirmation of efficiency.**
   - Contribution 2 and the Discussion credit the lot scale with narrower intervals.
   - That gain:
     - failed the pre-specified independent confirmation (P1 Holm p = 0.066; P2 p = 0.294);
     - vanished without repeated scans (Supplementary table S6b);
     - came with coverage below the simpler bias-correction baseline (lower in 4–5 of 5 seasons, 3/5 vs 5/5 seasons ≥ 0.90 at m=10).
   - The abstract does not mention the failed confirmation.
   - P3, the only confirmed independent endpoint, favours the wider method by construction, as Section 4.4 itself admits.
   - Fix: say in the abstract that the efficiency endpoints were not confirmed on independent data.

5. **MINOR: highlight 5, "Lot-level assurance held over all lots".** The pooled 92% is carried by 2017 (98%). Without 2017 it is 87.5%. Fix: say "pooled over lots, driven by 2017".

6. **MINOR: pooled and season-mean figures are mixed.**
   - The abstract's "1–4 points" comes from season means at m=3, 5, 10 (3.7, 2.4, 1.4). The pooled differences are 3.2, 2.1 and 1.1.
   - The "0.919 pooled" in the same sentence is a pooled figure.
   - Fix: name the averaging scheme for each number.

7. **MINOR: the comparator in Table 6 was chosen by its outcome.** It is defined as "the cheapest rule without reference fruit" (scp_lower). Choosing the minimum biases the comparison against reference fruit. Fix: name the comparator a priori, or adjust for the selection.

8. **MINOR: cost inconsistency.** Section 4.6 gives 2.47 units for LotCP-S at m=10, excluding reference tests. But Table 6 gives 4.22 − 1.50 (ten tests on a 1000-fruit lot) = 2.72. Fix: define both cost aggregations.

9. **MINOR: latent-variable choice.** In `results/reproduction/reproduction_meta.json`, published PLS selected 30 latent variables, the upper edge of its 6–30 grid. SNV PLS selected 26, outside the stated 8–20 range. The second external test set (val_ext2, n=320; RMSEP 1.67, bias −1.29) is not reported. Fix: widen the grid or justify it, and report both test sets.

10. **MINOR: leakage and pre-specification.** The leakage audit (`results/leakage_audit.json`) passes. The lot scale was designed on 2018 target data, and the analysis without 2018 (0.934) is appropriately given. Since only the NeoSpectra arm was confirmatory and its efficiency endpoints failed, nothing about LotCP-S efficiency on mango is confirmatory. Fix: state this plainly in the Conclusion.

11. **MINOR: typesetting.**
    - Section 4.3: "by 0.10–0.10" should read 0.081–0.105 across the two recipes.
    - Section 4.6: "3.69 [2.11, 5.16], The difference" (stray capital after a comma).
    - Section 3.5: write "pooled over lots, as the mean of the season values, and without 2017".

**(3) Numbers checked**

| # | Statement in manuscript | Result file / check | Match |
|---|---|---|---|
| 1 | Split CP (sample folds): 0.823 pooled, 0.781 without 2017, 0/5 seasons, 47% lot-draws | `season_summary.csv` | ✓ |
| 2 | Season-fold split CP 37% wider | 5.258 / 3.828 | ✓ |
| 3 | LotCP-S m=10: 0.919 / 0.911 / 0.893; by season 0.957, 0.882, 0.902, 0.897, 0.914; 0.934 without 2018 | `season_summary.csv` | ✓ |
| 4 | LotCP-A m=10: 92% pooled, 87.5% without 2017, by season 98/86/86/89/93, target met in 2/5 | `season_summary.csv` | ✓ |
| 5 | Replay gain 3.7 / 2.4 / 1.4 points; CI +0.005 to +0.019 (SNV, m=10) | `matched_baseline.csv` (season means); t-CI 0.006–0.022 | ✓ |
| 6 | α=0.05 comparison: LotCP-S 94.9% at width 4.29, LotCP-A 96.4% at 4.30 | `raw_results.csv` | ✓ |
| 7 | Target-only 34% wider; 4.29 vs 4.25 interval score at m=20 | `season_summary.csv` | ✓ |
| 8 | Table 6: point 8.69 [6.75, 11.21]; Δ +5.00 [2.96, 8.24]; immature 8.0 vs 0.5; mature withheld 6 vs 21; lot figures 7.3 / 20 / 3.7 / 69 / 0.2 / 59 | `decisions_ci.csv`, `decisions_vs_best_m0.csv` | ✓ |
| 9 | Leave-one-season-out level 2.70 vs 2.47 | `alpha_loso.csv` | ✓ |
| 10 | NeoSpectra: P1 −0.049 (−0.086, −0.013), Holm p 0.066; P3 95% vs 88%, widths 1.19 vs 1.13; split CP 0.930 | `confirmation_tests.csv`, `confirmation_summary.csv` | ✓ |
| 11 | Published-split reproduction: RMSEP 1.045; CNN 1.07–1.08; n = 10243 / 1448 | `reproduction.csv` | ✓ |
| 12 | NeoSpectra overlap 0 of 2,106 layers; 19,807 development layers | `neospectra_overlap.json` | ✓ |
| 13 | Lot counts 56 / 38 / 14 / 18 / 11 = 137 | `raw_results.csv` | ✓ |

**Mismatches:**
- "0.10–0.10" should be 0.081–0.105.
- "6 to 13 points in every season" should be 1.6–14.0 for sample-fold split CP.
- Highlight 1 is contradicted by the Gaussian band in 2017 (0.905) and published-PLS split CP in 2017 (0.916).
- The CI method does not match the reported estimand (concern 1).
- 2.47 vs 2.72 (concern 8).
