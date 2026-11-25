<!-- Reviewer 1 (methodology/statistics), fresh-context agent, round 3, 2026-11-25 -->

**Reviewer 1 (methodology and statistics)**

**(1) Score: 5/10. Recommendation: major revision.**
The audit is careful. Season-level inference, matched baselines and the honest NeoSpectra failure are good practice. The weak point is the new headline (Section 2.7/4.5, abstract, highlights, conclusion). Its theory is overstated, the variant reported was picked after a pre-stated rule failed, and the fixed-alpha comparison is not matched.

**(2) Concerns**

1. **MAJOR. Proposition 3 does not support the coverage claim as stated.**
   - The second claim ("covered with probability ≥ 1−α on the event {T_{S+1} ≤ T_(k)}, conditional on the season") is not proven.
   - Within-season conformal coverage holds only marginally over that season's calibration lots. The event selects small values of T_{S+1}, so coverage conditional on it can fall below 1−α. "Conditional on the season" is also undefined when the season is a finite set of lots that includes Z.
   - What the proof does give, by a union bound, is P(cover) ≥ 1 − α − k/(S+1).
   - Section 2.7's "so a new lot of the new season is then covered with probability at least 1−α" is therefore wrong as written.
   - The "common, fixed score function" is not common either. Past-season residuals come from season-held-out models trained on S−1 seasons; target residuals come from the model trained on all S seasons. Remark 3 mentions only the constants.
   - Fix: state the union bound, or a correct joint statement. List the predictor asymmetry. Drop the 1−α sentence from 2.7.

2. **MAJOR. The guarantee quoted is for LotCP-R, but every headline number is for LotCP-R2.**
   - Discussion and Limitation 3 give 2/3–6/7 (0.67–0.86), which is k=1.
   - For R2 (k=2) the bound (S−1)/(S+1) is 1/3 for 2017 and 5/7 for 2021.
   - In 2017, R2's multiplier was below the pooled one (results/cycle4/robust_quantiles.csv: mult_R2 = 0.985 SNV).
   - Fix: report the R2 bound explicitly in the abstract, Limitation 3 and Discussion, or headline R.

3. **MAJOR. R2 was chosen after the planned primary method failed, and this is not disclosed.**
   - experiments/plan_v7.yaml names q_R = max as the idea, with R2 as a "variant". Its success rule requires a width increase of at most 15 %.
   - The addendum says: "Primary results seen (R fails width, R2 passes…)". R cost 15–18 % more width.
   - The manuscript says only that (f)–(g) "were planned in writing". S4 and S8 do not record the switch.
   - Fix: state that R failed its pre-stated width rule and that R2 was promoted afterwards, and soften the abstract and highlights accordingly.

4. **MAJOR. The fixed-alpha comparison is unfair, so "less than half the extra width" is unsupported.**
   - LotCP-S at α=0.05 over-shoots badly: season coverages are 0.946–0.981 (SNV, m=10, robust_lots.csv), against R2's minimum of 0.904.
   - The plan addendum itself called for a fixed α "giving the same mean width" and admits this was not run. cycle3/assurance_frontier.csv has only α = 0.05, 0.10 and 0.20.
   - The sensitivity analysis also undercuts the stated mechanism. Removing the +∞ conformal term removes the marginal gain. So R2 works largely through a finite-K_s level inflation, effectively α ≈ 0.04–0.08, i.e. a smaller fixed α. That contradicts "set by how much past seasons disagree".
   - Fix: run LotCP-S on a fine α grid and compare at matched season-minimum coverage or matched width. Revise Highlight 4, the abstract and the conclusion.

5. **MAJOR. "Seasons ≥ 0.90" counts are knife-edge and inconsistent between tables.**
   - Table 3 gives LotCP-S (SNV, m=10) as 3/5: 2019 = 0.9025 in raw_results.csv.
   - Table 5, Section 4.5 and the abstract ("only two of five") give 2/5: 2019 = 0.8978 in cycle4/robust_lots.csv, a different set of reference draws.
   - In cycle4/seq_summary.csv, 2019 at m=5 is 0.89999981.
   - R2's minimum of 0.904 is equally close to the threshold. Contrasts of 2/5 against 5/5 are therefore partly Monte-Carlo noise from the reference draws.
   - Fix: use one set of draws throughout. Report season coverages with draw-level Monte-Carlo SEs, and season-mean shortfall rather than threshold counts.

6. **MAJOR. The decision claims rest on a weak comparator.**
   - The abstract and Highlight 5 credit "calibrated lower bound vs point value". But the point rule (8.69) is worse than withholding every fruit (6.44), as the text admits, and α* = 0.10 builds in the bound's advantage.
   - Fix: say so in the abstract and highlights, or compare against bias-corrected point predictions (5.95).

7. **MINOR. All season-robust evidence is in-sample.** It was developed on seasons already examined, alongside the 2018-designed lot scale. Limitation 3 says this. The abstract's "exploratory" is adequate, but the highlight is not hedged.

8. **MINOR. The LotCP-AR claim "The same held at m=5" is too broad.** At m=5 the SNV width increase was +15.7 % (5.332 vs 4.607), outside the "8–12 %" range and over the plan's 15 % rule.

9. **MINOR. NeoSpectra P4 relabelled.** It met the pre-specified rule (confirmation_tests.csv: confirmed=True). Relabelling it "uninformative" is conservative but post hoc, so say so. Also report how the "better of two baselines" for P3/P4 was selected, since it switches between target-only and bias correction.

10. **MINOR. Text errors and other small issues.**
    - Section 4.8 cites "Table 6" for decision costs; it should be Table 7.
    - "0.08–0.10" should be 0.08–0.11 (+0.081 to +0.105).
    - Multipliers growing with the number of seasons (R2: 0.98 → 1.25) means intervals widen as history accumulates. Discuss this property.

11. **MINOR. Leakage.** Controls look adequate: grouped folds, LV and ν0 selected on source only, leakage_audit.json present. The residual issue is design leakage, through 2018 and through the cycle-4 choices made after the target seasons had been seen. Fix: state this together with item 3.

**(3) Numbers checked (all matched except where noted)**

| Claim | Text | Result file |
|---|---|---|
| Split CP (sample folds), SNV | 0.823 / 0.806 / 0.781, width 3.83 | 0.8230 / 0.8057 / 0.7805, 3.828 |
| Split CP (season folds) | 0.900 / 0.877 / 0.839, 5.26 | 0.8998 / 0.8769 / 0.8392, 5.258 |
| Gauss, QRF, CQR, ensemble, MC dropout | 0.840, 0.841, 0.794, 0.766, 0.775 | 0.8403, 0.8414, 0.7938, 0.7655, 0.7749 |
| WCP coverage, unbounded share | 0.909, 5 % | 0.9086, 0.05 |
| LotCP-S m=10 by season | 0.957 / 0.882 / 0.902 / 0.897 / 0.914 | matches raw_results.csv |
| LotCP-S m=10 excluding 2018 | 0.934 | 0.9337 |
| LotCP-A m=10 lot-draws ≥ 0.90 by season | 98 / 86 / 86 / 89 / 93; 87 % excl. 2017 | 0.980 / 0.862 / 0.855 / 0.886 / 0.927; 0.875 |
| Target-only vs LotCP-S | 34 % wider; 4.29 vs 4.25 | 4.634 / 3.451; 4.286 vs 4.252 |
| Table 4, LotCP-S vs split CP (sample), m=5 | +0.104 [0.056, 0.153] | recomputed t-interval matches |
| Table 4, interval score vs bias corr., m=10 | +0.269 [0.050, 0.488] | matches |
| Table 5 width increases | +7 / 11 / 9 / 8 %; +24 % at α=0.05 | 3.672/3.446 etc. match |
| Lowest R2 season coverage | 0.904 | 0.9039 |
| R2 multipliers (SNV) | 0.98 → 1.25 | 0.985 → 1.250 |
| Decision costs | 8.69, 3.69 [2.11, 5.16]; Δ −0.28 / −0.12 / +0.53; 0.5 vs 8.0 immature | match decisions_ci.csv |
| Confirmation P1–P4 values | Table 6 | match confirmation_tests.csv |
| Shift indicator Spearman | 0.20 | 0.2026 |

**Mismatch:** LotCP-S SNV m=10 is "3/5 seasons ≥ 0.90" in Table 3 but "2/5" in Table 5, Section 4.5 and the abstract (2019: 0.9025 vs 0.8978, from different draws).
