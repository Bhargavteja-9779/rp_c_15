<!-- Reviewer 1 (methodology & statistics), fresh-context agent, cycle 2 round 1 -->

**Reviewer 1 report: methodology and statistics**

**1. Score: 4/10. Recommendation: major revision.**

**2. Concerns**

**C1 (MAJOR). The headline coverage and assurance figures come mostly from one over-covered season.**
- *Problem:* 2017 supplies 56 of the 137 target lots (41 %). It had only two source seasons, and the paper itself says it is over-conservative there (LotCP-S 0.957, LotCP-A meets-share 0.98 at m=10). I recomputed from results/raw_results.csv for the four later seasons only:
  - LotCP-S coverage at m=10 is 0.893 (below nominal). With the published PLS recipe it is 0.894 (results/published_pls/).
  - The LotCP-A share of lot-draws at ≥0.90 is 87.5 % at m=10 and 86.5 % at m=20, both below the 90 % target.
  - By season, LotCP-A at m=10 misses the target in 3 of 5 seasons (0.86, 0.86, 0.89).
- *Consequence:* the abstract's "91–92 %" and "kept 92 % of lots" do not hold for any season with an adequate source set. Section 7.2's "missed by a few points in the less favourable ones" understates this.
- *Fix:* report season-weighted and 2017-excluded figures alongside the pooled ones in the abstract, Tables 5/6 and the Highlights. State plainly that the assurance was not met in 3/5 seasons.

**C2 (MAJOR). The inference treats lots as independent, but the effective sample is five seasons.**
- *Problem:* Wilcoxon tests over 137 lots and bootstrap CIs stratified by season (Section 5.6; statistics.json) ignore the season random effect that the paper identifies as the dominant error source (Table 2, Fig. 3). The p-values and CIs are therefore anti-conservative. The "seasons favouring" counts (k/5) are the only season-level evidence, and they carry no test.
- *Fix:* add a mixed-effects model (season random intercept), or a season-level permutation or sign test. Bootstrap whole seasons, not just lots within them. Temper claims to match.

**C3 (MAJOR). The confirmation does not test the paper's central premise, and two endpoints are weak by design.**
- *Problem 1, the mango arm:* the four mango "confirmations" are re-draws on lots used during development, including 2018, which was used to design D1. They should not carry "Confirmed: yes" in Table 7.
- *Problem 2, NeoSpectra shows no shift:* split CP already covers 0.930, so this data set cannot test a seasonal or campaign shift.
- *Problem 3, the efficiency endpoints failed:* P1/P2 (the efficiency claim) failed on NeoSpectra.
- *Problem 4, the assurance endpoints reward width:* P3/P4 compare coverage shares with no width constraint, so a wider method wins automatically.
  - NeoSpectra P4: LotCP-A width 2.01 against 0.92 for the comparator.
  - NeoSpectra P3: LotCP-A width 1.19 against 1.13 for the comparator.
  - Even the Highlight "confirmed the lot-level guarantee" rests on P3/P4.
- *Fix:* recast the confirmation claims as limited. For the assurance endpoints, compare against width-matched baselines, e.g. bias correction or target-only CP at an inflated level tuned on source lots to the same mean width. Ideally, test prospectively or on a genuinely shifted held-out season.

**C4 (MAJOR). The baselines are not equivalent, and the comparator choices are selective.**
- *Problem 1, no matching baseline:* LotCP-S's efficiency gain over bias correction comes entirely from the replicate-scan scale. Without it there is no significant difference at m=5/10 (Section 11; table6b). Yet no baseline gets the same label-free scale, e.g. bias correction + source quantile of replicate-scaled residuals. The "bias corr + source CP" baseline also uses sample-fold half-widths, which the authors show to be miscalibrated.
- *Problem 2, Table 9 is selectively presented:*
  - It shows the bias-corrected margin only at m=5. At m=3 it is the cheapest rule overall at α*=0.05 and 0.10 (2.16 and 3.39 against 2.22 and 3.41 for LotCP-S; tables/table17_economics.csv).
  - It omits the computed "withhold all" rule (3.05 at c_D=1/19), which beats LotCP-S at m=10 (3.07).
- *Problem 3, the published-PLS paragraph is selective:* it omits that target-only centred reaches 90.3 % of lot-draws at m=10, essentially equal to LotCP-A (91.1 %).
- *Fix:* add the matched baselines, report all m and all rules, and drop "further saving" claims that are not supported against bias correction + margin.

**C5 (MAJOR). The decision and economics claims have no uncertainty estimates and were chosen after the results were known.**
- *Problem 1, no uncertainty:* the harvest simulator, cost analysis, planner and LotCP-A were all added after the main results (D6/D7). None has CIs or tests.
- *Problem 2, the "halved" claim:* "premature lot harvests roughly halved" is 7.3 % against 3–4 % of 82 lots, about 6 against 3 lots. It is shown at α=1/3, an operating point picked from the frontier rather than the pre-stated α=0.10.
- *Problem 3, in-sample regret:* the regret comparison (1.4 % against 4.4 %) chooses the best α in hindsight on the same 137 lots.
- *Problem 4, the abstract's cost comparator:* the "29–71 %" cost reduction is measured against point decisions. The m=0 split-CP bound achieves a similar saving without any destructive testing.
- *Fix:* add lot- and season-bootstrap CIs to Tables 8–9. Pre-state the operating point. Choose α on held-out seasons. Report savings relative to the strongest m=0 bound.

**C6 (MAJOR). Development data and multiplicity.**
- *Problem:* the 19 ledger variants plus plan_v3 explorations, D1 tuned on 2018, and D4/D7 added after results all draw on the same 137 lots. Only 4 endpoints are Holm-corrected.
- *Fix:* report main results excluding 2018 for LotCP-S. Clearly label every non-pre-registered comparison as exploratory. I could not verify commit timing (git was not inspected), so please provide verifiable timestamps (e.g. OSF/Zenodo) for PROTOCOL.md and plan_v2.

**C7 (MINOR). The primary predictor is weak.**
- *Problem:* the SNV pipeline's RMSEP is 1.39, against 1.045 for the published recipe (results/reproduction/reproduction.csv). All main tables use the weaker model, and val_ext2 (bias -1.29) is not reported.
- *Fix:* make the published recipe primary, or at least report both predictors in all main tables.

**C8 (MINOR). The replicate-scan structure differs from deployment.**
- *Problem:* repeated scans in this data set span instrument units and temperatures, which is not how a single-unit grower would scan.
- *Fix:* move the single-unit analysis (table S22) into the main text with tests against the baselines.

**C9 (MINOR). The 2017 width forecast is poor.**
- *Problem:* the planner's forecast is off by 21 % in 2017.
- *Fix:* report planner error by number of source seasons, so users know when to trust it.

**C10 (MINOR). The NeoSpectra data are not fully "untouched".**
- *Problem:* the NeoSpectra samples partly overlap the KSSL soils examined during development.
- *Fix:* quantify the overlap and rerun the confirmation excluding the overlapping samples.

**3. Numbers checked against result files: inconsistencies found**
- **Section 11:** the text says removing the scale raises the m=10 interval score "to 5.02". Tables 5 and 11 give 5.01. The raw value is 5.015.
- **Section 11 replay ablation:** it quotes LotCP-S "with replay" as 0.921 coverage and 4.44 interval score at m=10. Table 11 has 0.919 / 4.46 for the same method. The different draws are not disclosed.
- **Variant ledger:** state/variants_tried.csv v015 gives single-instrument coverage as 0.914. The manuscript and table22 give 0.919 at m=10; 0.914 is the m=30 value.

Everything else I checked matches the result files: Tables 3, 4, 4b, 6, 7, 8 and 10, the Section 7.1 test p-values, the published-PLS figures, and the lot-decision rates.
