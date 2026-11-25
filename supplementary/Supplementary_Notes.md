# Supplementary Note S5. Ablation, generalisation, soil spectra and failure analysis

## S5.1 Ablation study

Table S-1 and Fig. S-1 remove or replace one component at a time.

| Variant | m=0 | m=3 | m=10 | m=30 |
|---|---:|---:|---:|---:|
| LotCP-S | 0.894 / 5.39 / 7.26 | 0.921 / 3.83 / 4.91 | 0.919 / 3.45 / 4.46 | 0.914 / 3.28 / 4.31 |
| LotCP-S + shrinkage | 0.894 / 5.39 / 7.26 | 0.919 / 3.77 / 4.86 | 0.919 / 3.45 / 4.46 | 0.914 / 3.28 / 4.32 |
| LotCP-S, reference scale only | 0.899 / 5.45 / 7.29 | 0.925 / 4.07 / 5.14 | 0.926 / 3.62 / 4.58 | 0.925 / 3.45 / 4.40 |
| LotCP-S, replicate scale only | 0.894 / 5.39 / 7.26 | 0.921 / 3.99 / 5.11 | 0.924 / 3.72 / 4.74 | 0.920 / 3.55 / 4.64 |
| LotCP-S, lot-fold residuals | 0.861 / 4.42 / 6.80 | 0.905 / 3.53 / 4.76 | 0.908 / 3.27 / 4.36 | 0.908 / 3.21 / 4.30 |
| LotCP | 0.899 / 5.45 / 7.29 | 0.924 / 4.25 / 5.40 | 0.927 / 3.97 / 5.01 | 0.921 / 3.74 / 4.86 |
| LotCP + shrinkage | 0.899 / 5.45 / 7.29 | 0.923 / 4.18 / 5.32 | 0.926 / 3.97 / 5.01 | 0.921 / 3.74 / 4.86 |
| LotCP w/o episodic quantile | 0.782 / 3.78 / 7.88 | 0.899 / 3.80 / 5.30 | 0.917 / 3.80 / 4.96 | 0.918 / 3.67 / 4.83 |
| LotCP, lot-fold residuals | 0.846 / 4.11 / 6.78 | 0.889 / 3.39 / 4.96 | 0.892 / 3.15 / 4.59 | 0.884 / 3.02 / 4.55 |
| LotCP, sample-fold residuals | 0.830 / 3.93 / 6.85 | 0.885 / 3.34 / 4.96 | 0.888 / 3.10 / 4.59 | 0.880 / 2.98 / 4.55 |
| LotCP, spectrum-pooled weights | 0.897 / 5.33 / 7.17 | 0.929 / 4.24 / 5.32 | 0.932 / 3.97 / 4.94 | 0.930 / 3.88 / 4.89 |

Table: Table S-1. Ablation of LotCP components (PLS, nominal 0.90). Each cell: coverage / width / interval score.


![Fig. S-1. Ablation: lot-macro coverage with bootstrap 95 % CI for m = 5 and m = 20; the interval score (IS) is printed next to each variant.](figures/fig6_ablation.png){width=6.3in}

*Scale.* The lot-specific scale is the component that matters most once $m>0$. Removing it (LotCP) raises the interval score at $m=10$ from 4.46 to 5.02. The two sources of scale information both contribute: with the reference-sample variance alone the score is 4.58, with the replicate-scan variance alone 4.74. The replicate-scan term is the only one available at $m\le1$ and costs no reference measurement. It is also what separates LotCP-S from the bias-correction shortcut when reference samples are few. Without the replicate-scan term, the per-lot interval score of the reference-scale-only variant is worse than that of bias correction with the source quantile at $m=3$ (mean difference 0.19, Holm-adjusted p = 0.004), because a scale estimated from three samples is noisy, does not differ from it at $m=5$ or 10 (p = 0.347 and = 0.421) and is better only from $m=20$ (p < 0.001; supplementary table S6b). A user who takes a single scan per fruit should therefore not expect an efficiency gain over that shortcut with fewer than about twenty reference samples; what remains is the stability of coverage across predictors shown in Supplementary Note S5.

*Fold unit.* At $m=0$, residuals held out by lot or by sample give coverage 0.846 and 0.830; season-held-out residuals are needed to reach the nominal level. With $m>0$ the picture changes. After the lot bias has been corrected, what is left to calibrate is the within-lot residual, and lot-fold residuals describe it well: LotCP on lot-fold residuals covers 0.892 at $m=10$, slightly below nominal, with narrower intervals than LotCP on season-fold residuals, which over-covers (0.927). LotCP-S on lot-fold residuals covers 0.908 with an interval score of 4.36, against 0.919 and 4.46 for season-fold residuals. The lot-fold variant of LotCP-S is therefore the more efficient one, and it is not less safe by season: its lowest per-season coverage at $m=10$ is 0.89, against 0.88 for season-fold residuals. Season-held-out residuals are thus needed without reference samples and are not needed with them. We keep the season-fold variant as the reported method because it was fixed before this comparison was made, and note that the choice costs about 6 % in width at $m=10$.

*Shrinkage.* The pre-specified empirical-Bayes shrinkage of the bias estimate has a small effect at $m=3$ (interval score 5.32 against 5.40 for the plain mean with the location-only method, 4.86 against 4.91 with LotCP-S) and none from $m=10$ (4.46 against 4.46). The reason is visible in the variance components: the lot bias is large relative to the sample noise, so the shrinkage weight is already 0.79–0.83 at $m=3$. On the soil data of Supplementary Note S5 shrinkage is harmful. The part of H4 that concerns shrinkage is not supported, and the reported method uses the plain mean.

*Episodic replay for LotCP-S.* A pre-specified ablation (plan_v2) removed the replay from LotCP-S, standardising each past lot with its own full-information bias and scale. Coverage then fell to 0.757 at m = 0, 0.888 at m = 3 and 0.908 at m = 10, against 0.894, 0.920 and 0.921 with replay (this ablation used its own reference draws, so its LotCP-S values differ slightly from those of the main tables). The share of lots reaching 0.90 fell from 71 % to 56 % at m = 3. The interval score was not better with the replay (4.44 against 4.38 at m = 10): the replay buys validity at small m, not efficiency.

*Episodic quantile.* Replacing the replayed quantile by the quantile of within-lot residuals centred on the true lot mean, which ignores the estimation error of the bias, gives coverage 0.899 at $m=3$ and 0.917 at $m=10$ for the location-only method, and it fails at $m=0$ (0.782). Because season-fold residuals are conservative for $m>0$, the omission is not punished in this data set. The replay is nevertheless what makes the scale-adaptive score calibratable at all, since the distribution of $|r-\hat b|/\hat s$ depends on $m$ through both estimates.

*Weighting.* Giving every scan rather than every lot the same weight changes little (0.932 against 0.927 at $m=10$), because lot sizes are fairly homogeneous here.

In summary, H4 holds for the scale component and, at $m=0$, for the fold unit. It does not hold for shrinkage, which was therefore removed from the method, and holds only at very small $m$ for the episodic quantile of the location-only method.

## S5.2 Generalisation across predictors and protocols

Fig. S-2 and supplementary table S21 repeat the comparison for LightGBM and the CNN, and for the leave-one-season-out protocol. The seed-to-seed standard deviation of lot-macro coverage is at most 0.002 for the LotCP variants (supplementary table S7b).


![Fig. S-2. Lot-macro coverage of LotCP and LotCP-S for three point predictors and two protocols (nominal 0.90).](figures/fig7_generalisation.png){width=6.5in}

The failure of sample-fold split conformal prediction is larger for the more flexible predictors: coverage is 0.759 for LightGBM and 0.789 for the CNN, against 0.823 for PLS, because flexible models absorb more of the lot effects of their training lots. For the same reason, bias correction with the source quantile, which over-covers with PLS, under-covers with LightGBM (0.882 at $m=10$) and sits at 0.909 with the CNN. Its coverage depends on how strongly the predictor fits its training lots, which the user does not control. LotCP-S covers 0.914 and 0.914 at $m=10$ with these predictors, and 0.907 and 0.908 under leave-one-season-out with PLS and the CNN. Across the five predictor–protocol combinations its coverage at $m=10$ stays within 0.907–0.919. With the CNN, whose point error is lowest, LotCP-S at $m=10$ gives a mean width of 3.06 % DMC, that is, about ±1.5 % DMC.

## S5.3 External validation on soil vis–NIR spectra

The experiments so far use one fruit and one instrument family. We therefore repeated the central comparisons on two soil subsets of the Open Soil Spectral Library (Section 3), a different material, spectral range, instrument and reference chemistry, in a field where adjusting a library model with a few local samples is established practice. Table S-2 and Fig. S-3 give the results.

| Data set and task | Method | Lots | Coverage | Under-covered lots (%) | Width | Interval score |
|---|---:|---:|---:|---:|---:|---:|
| LUCAS organic C, 2009 → 2015 | Split CP (sample folds) (m=0) | 467 | 0.628 | 73 | 1.03 | 3.00 |
| LUCAS organic C, 2009 → 2015 | Split CP (lot folds) (m=0) | 467 | 0.635 | 70 | 1.04 | 2.97 |
| LUCAS organic C, 2009 → 2015 | LotCP-S (m=5) | 467 | 0.888 | 16 | 1.05 | 1.55 |
| LUCAS organic C, 2009 → 2015 | Bias corr. + source CP (m=10) | 467 | 0.891 | 15 | 1.03 | 1.52 |
| LUCAS organic C, 2009 → 2015 | Slope/bias corr. + source CP (m=10) | 467 | 0.885 | 17 | 1.03 | 1.61 |
| LUCAS organic C, 2009 → 2015 | Target-only CP, centred (m=10) | 467 | 0.906 | 14 | 1.26 | 1.64 |
| LUCAS organic C, 2009 → 2015 | LotCP-S + shrinkage (m=10) | 467 | 0.875 | 19 | 1.01 | 1.57 |
| LUCAS organic C, 2009 → 2015 | LotCP-S (m=10) | 467 | 0.892 | 14 | 1.01 | 1.48 |
| LUCAS organic C, 2009 → 2015 | LotCP-S (m=20) | 330 | 0.899 | 11 | 0.97 | 1.38 |
| LUCAS pH, 2009 → 2015 | Split CP (sample folds) (m=0) | 467 | 0.395 | 96 | 1.94 | 9.61 |
| LUCAS pH, 2009 → 2015 | Split CP (lot folds) (m=0) | 467 | 0.397 | 96 | 1.95 | 9.57 |
| LUCAS pH, 2009 → 2015 | LotCP-S (m=5) | 467 | 0.872 | 18 | 2.03 | 3.00 |
| LUCAS pH, 2009 → 2015 | Bias corr. + source CP (m=10) | 467 | 0.872 | 19 | 1.94 | 2.89 |
| LUCAS pH, 2009 → 2015 | Slope/bias corr. + source CP (m=10) | 467 | 0.893 | 14 | 1.94 | 2.77 |
| LUCAS pH, 2009 → 2015 | Target-only CP, centred (m=10) | 467 | 0.907 | 14 | 2.52 | 3.19 |
| LUCAS pH, 2009 → 2015 | LotCP-S + shrinkage (m=10) | 467 | 0.797 | 45 | 1.92 | 3.43 |
| LUCAS pH, 2009 → 2015 | LotCP-S (m=10) | 467 | 0.878 | 16 | 1.97 | 2.86 |
| LUCAS pH, 2009 → 2015 | LotCP-S (m=20) | 330 | 0.885 | 14 | 1.97 | 2.83 |
| KSSL total C, held-out projects | Split CP (sample folds) (m=0) | 79 | 0.881 | 15 | 1.34 | 2.19 |
| KSSL total C, held-out projects | Split CP (lot folds) (m=0) | 79 | 0.895 | 13 | 1.42 | 2.19 |
| KSSL total C, held-out projects | LotCP-S (m=5) | 79 | 0.914 | 8 | 1.56 | 2.10 |
| KSSL total C, held-out projects | Bias corr. + source CP (m=10) | 79 | 0.878 | 17 | 1.34 | 2.09 |
| KSSL total C, held-out projects | Slope/bias corr. + source CP (m=10) | 79 | 0.895 | 12 | 1.34 | 2.02 |
| KSSL total C, held-out projects | Target-only CP, centred (m=10) | 79 | 0.907 | 13 | 1.71 | 2.23 |
| KSSL total C, held-out projects | LotCP-S + shrinkage (m=10) | 79 | 0.916 | 7 | 1.48 | 2.01 |
| KSSL total C, held-out projects | LotCP-S (m=10) | 79 | 0.916 | 6 | 1.50 | 2.02 |
| KSSL total C, held-out projects | LotCP-S (m=20) | 79 | 0.913 | 6 | 1.44 | 1.97 |

Table: Table S-2. External validation on vis–NIR soil spectra (PLS, nominal 0.90). Carbon is modelled as log(1 + %); widths and interval scores are in the units of the modelled quantity. Calibration residuals are held out by lot (grid cell or project). All methods and m: supplementary table S13.


![Fig. S-3. Lot-macro coverage on the soil data as a function of the number of local reference samples (PLS, nominal 0.90, dotted line). Dashed line: split conformal prediction with sample folds and no reference samples.](figures/fig10_soil.png){width=6.5in}

*The coverage loss is larger than for mango.* A model trained on the 2009 LUCAS campaign and applied to the 2015 campaign has a prediction error on the target of 0.57 log-units for organic carbon, against 0.32 in cross-validation, with a mean offset of 0.43; for pH the error is 1.36 against 0.61, with an offset of -1.15 pH units. We do not know the origin of this between-campaign offset; whatever its cause, it is the kind of batch effect a user of a spectral library can meet. Split conformal intervals calibrated within the 2009 campaign then cover 0.63 (organic carbon) and 0.40 (pH) of the 2015 values in 467 grid cells, at a nominal 0.90. Holding residuals out by lot does not help (0.64 and 0.40), because the shift is between campaigns and the source contains only one. This is the situation in which no label-free repair exists. For held-out KSSL projects, which are exchangeable with the calibration projects by construction, sample-fold split conformal prediction covers 0.881 and lot-fold calibration 0.895: with exchangeable lots and no campaign effect, the loss is small and holding out lots removes it, as hierarchical conformal theory predicts.

*A few local reference samples repair most of it.* With five reference samples per cell, LotCP-S covers 0.888 for organic carbon and 0.872 for pH; with twenty, 0.899 and 0.885. Coverage stays up to three points below nominal, because the residual scale of the 2015 campaign also differs from that of the 2009 cells that calibrate the half-width; the method does not fully absorb a shift in scale between campaigns. For KSSL projects it covers 0.914–0.916.

*Comparison with the alternatives.* On LUCAS organic carbon LotCP-S has a lower interval score than bias correction with the source quantile and slope/bias correction at $m=5$, 10 and 20, and than centred target-only calibration at $m=10$ and 20 (Holm-adjusted p ≤ 0.003 against the first two; p < 0.001 and < 0.001 against the third; supplementary table S13c). On LUCAS pH it is better than bias correction at $m=5$ and 10 (p < 0.001 and = 0.021) and not different at $m=20$ (p = 0.204); slope/bias correction has a numerically lower score from $m=10$, a difference that is not significant. On KSSL it does not differ from bias correction at $m=5$ and 10 (p = 1.000 and = 1.000) and is better at $m=20$ (p = 0.024); slope/bias correction has the numerically best score there at $m=20$. Bias correction with the source quantile under-covers on all three soil tasks (0.878, 0.891 and 0.872 at $m=10$), where it over-covered with PLS on mango: its coverage is again not under control. Centred target-only calibration is valid and wider, as before. Since soil samples have a single spectrum, these comparisons involve no replicate-scan information; the advantage of LotCP-S on LUCAS comes from calibrating the half-width for the estimation error and from the reference-sample scale.

*Shrinkage fails under a campaign shift.* The pre-specified shrinkage variant covers only 0.70 for pH and 0.85 for organic carbon at $m=5$, against 0.87 and 0.89 with the plain mean (supplementary table S13). The between-lot variance estimated inside the 2009 campaign is small, so the shrinkage weight is low and the estimate is pulled towards the 2009 mean, which the 2015 campaign has left. On KSSL, where lots are exchangeable, shrinkage gives a small gain at $m=5$ (interval score 2.05 against 2.10). Shrinkage thus helps a little when its assumption holds and fails badly when it does not, and the user cannot know in advance which case applies. This is why the reported method does not use it.

Taken together, the soil data reproduce the three main findings on independent material: intervals calibrated within the source population lose coverage on a new population, drastically so across survey campaigns; a handful of local reference samples restores most of the coverage; and LotCP-S is not significantly worse than any competing method at $m\le10$ and is significantly better where the shift is large. They also show a limit: under a between-campaign change of residual scale, coverage remains a few points short of nominal.

## S5.4 Robustness, computational cost and failure analysis

The detailed analyses are in Supplementary Notes S1–S3; the main results are these. *Robustness* (Note S1, Fig. S2, table S22). Adding Gaussian error with a standard deviation of 0.5 % DMC to the reference values left LotCP-S coverage at 0.923 at $m=10$ and widened the intervals by 4 %. Removing provider-flagged outliers changed coverage by 0.001. With only 20 past lots the method was conservative (0.947, intervals 12 % wider), and about 40 past lots were needed before the conservatism became small. Episode count and pseudo-count were immaterial. When the deployment unit was a single instrument unit within a lot, coverage was 0.919. When only the two preceding seasons were available it was 0.918, and for a held-out region or cultivar 0.913 and 0.907. Results at nominal levels 0.80 and 0.95 follow the same pattern (table S23). *Cost* (Note S2, table S24). The episodic calibration takes about 1.8 s for 187 past lots, and deployment computes one bias and one scale per lot. The binding cost is the number of destructive reference tests, which Section 4.7 and Supplementary Note S7 address. *Failures* (Note S3, Fig. S3). At $m=10$, 38 of the 137 target lots had coverage below 0.80 under sample-fold split conformal prediction, 13 under LotCP and 4 under LotCP-S. After bias correction the remaining failures were lots whose residual spread exceeded what past lots suggested (Spearman correlation of lot coverage with the ratio of lot to prior residual standard deviation, -0.84). Coverage was lower for fruit at the ripening stage (0.90 against 0.93), for the cultivar Keitt (0.86) and at the extremes of the DMC range.


# Supplementary Note S6. A decision-support prototype

To show that the workflow fits into routine practice, it is implemented as a small command-line tool that is part of the released code (`src/tool/harvest_tool.py`). Before the season, the owner of the calibration exports a file with the replay quantiles, the variance components and the planner output for each number of reference fruit. In the orchard or packhouse, the user supplies the NIR predictions of the lot's scans (repeated scans of a fruit are allowed and are used for the scale), the reference DMC of the destructively tested fruit and the specification. The tool returns a corrected prediction and a lower bound for every fruit, a HARVEST or WAIT/RE-TEST flag per fruit, a lot recommendation, a plain-language statement of what the bound guarantees, and the planned interval width for other numbers of reference fruit.

Box 1 shows the output for one lot of the 2021 season, calibrated on 2015–2020 and chosen as the lot of median size before its result was seen, with ten reference fruit and a specification of 15 % DMC.

> **Box 1.** Output of the prototype for lot 122300 (2021), *m* = 10, specification 15 % DMC.
>
> Lot bias correction: -2.91 % DMC · lot scale: 0.74 · fruit cleared for harvest: 0 % · **lot recommendation: WAIT / RE-TEST**
>
> Statement: Each lower bound holds for at least 90 % of fruit on average over lots (retrospective calibration; assumes the lot resembles past lots).
>
> Planned two-sided width (% DMC) for m = 0, 3, 5, 10, 20, 30: 4.83, 3.52, 3.34, 3.23, 3.16, 3.15
>
> Check against the reference values of the 30 non-reference fruit (not available to the tool): truly compliant 0 %; lower bounds that held 100 %.

In this lot the calibration over-predicted DMC by about 2.9 % points. The ten reference fruit exposed the bias and the tool recommended waiting. The reference values, unknown to the tool, confirm that none of the fruit had reached the specification. A single lot proves nothing about performance, which is the subject of Supplementary Note S7; the box shows the form in which the result would reach a user. The prototype is a research tool. Its use in practice would need an interface on the instrument or a phone, a calibration file maintained by the instrument provider or packhouse, and the prospective validation discussed in Section 6.


# Supplementary Note S7. Full harvest-decision and planning analysis (exploratory)

This note keeps the complete decision analysis of the first submission draft. Its operating points were chosen after the results were known; the main text (Section 2) reports the analysis at an operating point fixed in advance with season-cluster confidence intervals, which supersedes the statements here where they differ.

This section asks what the calibrated bounds change in the decision they are meant to support (RQ3). Table S-3 and Fig. S-4 give the outcomes of the six decision rules for a specification of 15 % DMC; the specifications of 14 and 16 % and the CNN predictor lead to the same conclusions (supplementary tables S16–S18).

| Decision rule | m | Mature fruit accepted (%) | Immature among accepted (%) | Lots > 10 % immature among accepted (%) | Immature lots harvested (%) | Ready lots delayed (%) |
|---|---:|---:|---:|---:|---:|---:|
| Point prediction ≥ t | 0 | 89.9 | 13.4 | 43.1 | 7.3 | 20.0 |
| Split-CP lower bound ≥ t | 0 | 58.4 | 2.9 | 10.2 | 3.7 | 69.1 |
| LotCP-S lower bound ≥ t | 0 | 51.2 | 2.4 | 6.6 | 2.4 | 78.2 |
| Bias-corrected point ≥ t | 10 | 91.2 | 7.7 | 37.2 | 7.6 | 7.4 |
| Bias corr. + source margin ≥ t | 10 | 62.9 | 1.1 | 5.1 | 0.0 | 57.3 |
| LotCP-S lower bound ≥ t | 5 | 64.3 | 1.4 | 4.4 | 0.2 | 58.5 |
| LotCP-S lower bound ≥ t | 10 | 65.1 | 1.2 | 5.1 | 0.1 | 56.4 |
| LotCP-A lower bound ≥ t | 10 | 55.5 | 0.6 | 2.9 | 0.0 | 70.5 |

Table: Table S-3. Harvest decisions against a 15 % DMC specification on 137 later-season lots (PLS, forward chaining; bounds at α = 0.10). Fruit level: a fruit is accepted when the rule's statistic is at least t. Lot level: a lot is harvested when at least 80 % of its scanned fruit are accepted; it is ready when at least 80 % of its fruit have reference DMC ≥ t (55 ready and 82 not-ready lots). Specifications of 14 and 16 % and the CNN predictor: supplementary table S16.


![Fig. S-4. Trade-off between harvesting immature fruit and holding back mature fruit (PLS, specification 15 % DMC, 137 later-season lots). Each curve traces one rule as its confidence level α varies from 0.02 to 0.5; crosses are rules without a confidence level. (a) Fruit-level decision. (b) Lot-level decision: a lot is harvested when at least 80 % of its scanned fruit are accepted.](figures/fig14_harvest_frontier.png){width=6.5in}

## S7.1 Fruit-level decisions

Accepting a fruit when its predicted DMC reaches the specification, the decision that a handheld reading invites, accepts 90 % of the mature fruit but lets through 13.4 % immature fruit among those accepted, and in 43 % of lots more than one accepted fruit in ten is immature. Correcting the lot bias with ten reference fruit lowers the immature share to 7.7 %, but leaves 37 % of lots above the 10 % mark, because a decision on the point value ignores the scatter of individual fruit around it.

A lower bound at α = 0.10 changes the picture. Without reference fruit, the split-conformal bound reduces the immature share to 2.9 % while accepting 58 % of mature fruit. With ten reference fruit, the LotCP-S bound reduces it to 1.2 %, leaves 5 % of lots above the 10 % mark, and accepts 65 % of mature fruit, more than the split-conformal bound although its risk is lower. The reference fruit remove the lot bias, so the bound can sit closer to the prediction for the same protection. LotCP-A at the same level is more cautious (0.6 % immature among accepted, 56 % of mature fruit accepted), as its lot-level guarantee requires.

The curves in Fig. S-4a make the comparison independent of the chosen level. Over its whole range, every bound that uses ten reference fruit lies below the curves of the bounds without reference fruit: for a similar share of mature fruit accepted, it lets through about half as many immature fruit or fewer. The curve of LotCP-S lies on top of that of bias correction with a source margin; at fruit level, once the bias is corrected and the level is free, the two make practically the same decisions. The bias-corrected point decision is simply the end of the same curve (α = 0.5), where most mature fruit are accepted and the immature share is highest. The value of the reference fruit for the harvest decision is therefore large and robust, while the additional value of LotCP-S over the simpler margin lies elsewhere: in calibration, which matters when the level is set from costs (Supplementary Note S7), and in the lot-level assurance.

## S7.2 Lot-level decisions

Whether a block is picked now is decided per lot. Of the 137 target lots, 55 were ready by the criterion of Section 2 (at least 80 % of fruit at or above 15 % DMC). Deciding on point predictions harvested 7 % of the 82 lots that were not ready and delayed 20 % of the ready ones (Table S-3). With five to ten reference fruit and a calibrated bound at α = 1/3, premature harvests fall to 4–3 % at the same rate of delay (20–21 %), and at α = 0.20 to 1 % with 38 % of ready lots delayed (Fig. S-4b). Without reference fruit, no conformal bound reaches this frontier: the split-conformal bound harvests 6 % of not-ready lots while delaying 35 % of ready ones at α = 1/3. As at fruit level, LotCP-S and bias correction with a source margin trace nearly the same lot-level curve. A lot decision is therefore where the reference fruit pay off most: they roughly halve the rate of premature harvest at an unchanged rate of delay.

## S7.3 Expected cost under assumed cost ratios

Table S-4 and Fig. S-5 weigh the two errors and the reference tests under the cost assumptions of Section 3. Harvesting every fruit costs 42 units per 100 fruit, because 42 % of the fruit is below 15 % DMC. Deciding on point predictions costs 8.4–11.0 units across the four cost ratios. A LotCP-S lower bound at the cost-derived level α\* with five reference fruit costs 2.4–7.8 units, including the cost of the reference tests; relative to point decisions this is a reduction of 29–71 % at the 15 % specification and 15–80 % across the three specifications. Most of this reduction comes from using a bound instead of a point value: without any reference fruit, the split-conformal bound at α\* already costs 2.3–9.4 units. The reference fruit add a further, smaller saving when withholding a mature fruit is relatively expensive.

The cost-derived level works for LotCP-S because its bound is calibrated. Using α\* instead of the best level on the grid chosen in hindsight raises the cost of LotCP-S with ten reference fruit by 1.4 % on average (at most 5 %) with PLS and by 0.0 % with the CNN (supplementary table S17b). The two simpler bounds are well tuned for one predictor and not for the other: for bias correction with a source margin the average regret is 4.4 % with PLS, and for the split-conformal bound it is 12.6 % with the CNN. In other words, with LotCP-S a grower can translate a cost ratio into a confidence level and expect the decision to be close to the best one available, whichever predictor the instrument uses.

![Fig. S-5. Expected cost under assumed cost ratios (PLS, specification 15 % DMC). (a) Cost per 100 fruit, in units of the value of one marketable fruit, for five decision rules as the assumed cost of withholding a mature fruit varies; the LotCP-S bound uses five reference fruit and the cost-derived level α*. (b) Cost of the LotCP-S rule as a function of the number of reference fruit for three lot sizes at c_D = 1/9; circles mark the minimum.](figures/fig15_economics.png){width=6.5in}

| Decision rule | c_D = 1/19 (α* = 0.05) | c_D = 1/9 (α* = 0.10) | c_D = 1/4 (α* = 0.20) | c_D = 1/2 (α* = 0.33) |
|---|---:|---:|---:|---:|
| Harvest all fruit | 42.05 | 42.05 | 42.05 | 42.05 |
| Point prediction ≥ t | 8.35 | 8.69 | 9.50 | 10.96 |
| Bias-corrected point ≥ t (m = 10) | 6.17 | 6.47 | 7.17 | 8.44 |
| Split-CP lower bound at α* | 2.28 | 3.69 | 6.28 | 9.43 |
| Bias corr. + source margin at α* (m = 5) | 2.41 | 3.62 | 5.60 | 7.80 |
| LotCP-S lower bound at α* (m = 3) | 2.22 | 3.41 | 5.42 | 7.85 |
| LotCP-S lower bound at α* (m = 5) | 2.41 | 3.57 | 5.52 | 7.80 |
| LotCP-S lower bound at α* (m = 10) | 3.07 | 4.22 | 6.12 | 8.35 |
| Cost-optimal m for LotCP-S, 200 fruit per lot | 0 | 0 | 0 | 0 |
| Cost-optimal m for LotCP-S, 1000 fruit per lot | 3 | 3 | 3 | 5 |
| Cost-optimal m for LotCP-S, 5000 fruit per lot | 5 | 5 | 5 | 10 |

Table: Table S-4. Expected cost per 100 fruit in units of the value of one marketable fruit, under ASSUMED costs (PLS, specification 15 % DMC, lots of 1000 fruit unless stated). Accepting an immature fruit costs c_I = 1; withholding a mature fruit costs c_D; each destructive reference test costs 1.5. α* = c_D/(c_I + c_D). The last three rows give the number of reference fruit that minimises the cost of LotCP-S. These are illustrative scenarios, not measured costs; other specifications, lot sizes and the CNN: supplementary table S17.


*How many reference fruit?* Each reference test costs one and a half fruit, so its value depends on how many fruit share it. For lots of 1000 fruit the cost-minimising number is 3–5 across the cost ratios, for lots of 5000 fruit 5–10, and for lots of 200 fruit it is 0 at c_D = 1/9: on small lots under these assumptions destructive testing does not pay for itself and the bound without reference fruit is preferable (Table S-4, Fig. S-5b). These optima rest on the assumed costs and on the retrospective simulation; they illustrate how the planner and the cost model combine, and a grower would substitute local values.


## S7.4 Planning the reference budget

Fig. S-6 compares the width planned from the source seasons (Section 2) with the width realised on the lots of the target season, for the five target seasons, three predictors, five values of $m$ and both variants.

![Fig. S-6. Reference-budget planning. (a) Interval width planned from past lots against the mean width realised on the lots of the following season; each point is one target season, predictor, number of reference samples and variant. (b) Planned and realised budget curves for PLS, averaged over target seasons.](figures/fig13_planning.png){width=6.3in}

The planned width is a usable forecast. Over all 150 combinations the median absolute relative difference between realised and planned width is 7 %, and the mean difference is -2 %. For PLS and LightGBM the median absolute difference is 8 % and 7 %; for the CNN it is 12 %. By target season the mean difference ranges from -21 % to 7 %: the forecast is too wide for 2017, when the calibration rested on two source seasons whose season-held-out models were weak, and within 8 % for the four later seasons (supplementary table S15). The shape of the curve is reproduced (Fig. S-6b): most of the reduction in width is obtained with the first five reference samples, and beyond ten both curves flatten. The largest deviations in Fig. S-6a are the CNN in 2017, where the planned width is well above the realised one. Table S-5 puts the planner in the form a grower would use: for each number of reference fruit, the width of the error bar to expect, the share of lots in which it will hold for at least 90 % of the fruit, and the cost of the tests. Going from no reference fruit to three narrows the LotCP-S interval from 5.1 to 3.8 % DMC; going from ten to twenty narrows it only from 3.5 to 3.4 % DMC, at twice the laboratory effort. A grower who needs the error bar to hold within nine lots in ten chooses LotCP-A and accepts a wider interval (4.4 % DMC at m = 10). Combined with the cost model of Supplementary Note S7, the planner turns the question "how many fruit should we cut?" into a calculation that can be made before the season from the calibration set.

| Reference fruit per lot, m | LotCP-S planned width | LotCP-S realised width | LotCP-A planned width | LotCP-A realised width | Lots ≥ 90 % covered, LotCP-S (%) | Lots ≥ 90 % covered, LotCP-A (%) | Reference cost per 100 fruit (1000-fruit lot) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 5.14 | 5.05 | 6.86 | 6.74 | 77 | 88 | 0.00 |
| 3 | 3.76 | 3.66 | 5.01 | 4.87 | 71 | 92 | 0.45 |
| 5 | 3.59 | 3.49 | 4.61 | 4.47 | 70 | 91 | 0.75 |
| 10 | 3.48 | 3.36 | 4.37 | 4.21 | 69 | 92 | 1.50 |
| 20 | 3.36 | 3.24 | 4.12 | 3.96 | 68 | 90 | 3.00 |
| 30 | 3.27 | 3.30 | 4.00 | 4.11 | 65 | 91 | 4.50 |

Table: Table S-5. The reference-sampling planner (PLS, mean over the five target seasons). Planned widths are computed from past lots before the season; realised widths are those obtained on the lots of the target season. Widths in % DMC; reference cost in units of fruit value (assumed 1.5 per test).



# Supplementary Note S8. How the method changed during development

Our first idea did not work. We expected that correcting each new lot's bias from a few reference fruit, with the correction shrunk towards past lots and its error calibrated on past lots, would be enough. On the first season we examined it was not: coverage was 0.86 at a nominal 0.90 with ten reference fruit, because lots of the new season differed from past lots in the spread of their errors, not only in their offset. The spread could be estimated in part without any reference value, from the scatter between repeated scans of the same fruit, and adding it repaired coverage. A second component we had designed in, the shrinkage of the bias towards past lots, later failed outright on soil spectra from a new survey campaign and was removed. And when we confirmed the frozen method on a data set we had not used before, the efficiency gain over a simple bias correction did not reach significance, whereas the lot-level guarantee did. Supplementary Note S8 summarises these failures, because they define what the method can and cannot claim.

*What did not work first, and why.* Four results from our own work shaped the method and the claims (journal entries in the study repository, available on request). (i) The pre-specified location-only correction under-covered on the first season examined, because the residual scale of new lots exceeded that of past lots; a lot-specific scale was added, partly estimated from repeated scans (protocol deviation D1). (ii) Empirical-Bayes shrinkage of the bias estimate, part of the original design, gave no benefit on mango and failed on the soil survey's campaign shift (coverage 0.70 instead of 0.87 for pH at five reference samples); it was removed. (iii) The point predictor we used throughout, PLS after standard normal variate correction, proved 0.35 % DMC worse in RMSEP than the published PLS recipe on the published split (Section 4); the interval conclusions were therefore re-checked with the published recipe. (iv) In the pre-specified confirmation on a data set not used during development, the lot-level assurance was confirmed but the efficiency gain of LotCP-S over a simple bias correction was not (Section 4).

In a further round after internal review, three additional analyses were run under a new plan (experiments/plan_v4.yaml): season-level inference, baselines that share the lot scale of LotCP-S but omit the replay, and decision outcomes with season-cluster confidence intervals at an operating point fixed in advance. They led to the restatement of the efficiency and decision claims in the main text.


# Supplementary Note S1. Robustness and sensitivity

Fig. S2 and supplementary table S22 summarise how the coverage of LotCP-S responds to errors in the reference values, to outlier screening, to the number of past lots and to other source–target shifts.


![Fig. S2. Robustness of LotCP-S coverage (PLS, nominal 0.90): (a) Gaussian error added to the reference values of the m reference samples; (b) number of past lots available for calibration; (c) other source–target shifts.](figures/fig8_robustness.png){width=6.5in}

*Error in the reference values.* Oven-drying has its own error, and the $m$ reference values carry it. Adding Gaussian error with a standard deviation of 0.25 or 0.5 % DMC to the reference samples at deployment (not to the calibration lots) leaves coverage at or slightly above nominal (0.923 at $m=10$ for 0.5 % DMC) and widens the intervals by 4 % (supplementary table S22). The noisier references inflate the estimated lot scale, which errs on the conservative side.

*Reuse of the calibration lots.* The variance components and the pseudo-count are estimated from the same past lots that provide the conformal quantile. Estimating them on a random half of the lots and computing the quantile on the other half, with the pseudo-count fixed at 10, gives coverage 0.929 and an interval score of 4.46 at $m=10$, against 0.919 and 4.46; the reuse does not make the intervals optimistic.

*Single-instrument units.* In the data set a lot was usually scanned with several instrument units, whereas a grower would use one. Redefining the deployment unit as one instrument unit within a lot (reference and query scans from that unit only; 558 units) gives coverage 0.919 for LotCP-S at $m=10$ with a mean width of 3.12 % DMC, 0.833 for sample-fold split conformal prediction and 0.954 for bias correction with the source quantile. The interval score of LotCP-S is 4.12, against 4.32 for centred target-only calibration at $m=10$ and 3.88 against 3.85 at $m=20$. The share of unit-draws with coverage below 0.80 is higher than at lot level (11 %), because single-instrument units differ more in residual scale than lots that average over instruments.

*Outlier screening.* Removing the scans flagged by the data provider from calibration and evaluation leaves coverage unchanged (0.920) and narrows the intervals by 4 %.

*Number of past lots.* With only 10 past lots the lot-balanced quantile is close to the largest calibration score and the intervals are very wide; with 20 lots coverage is 0.947 and with 40 lots 0.929, at widths 12 % and 3 % above those obtained with all lots. The method is always conservative when lots are few, which follows from the $1/(K_m+1)$ mass at infinity in Eq. (6), and some 40 past lots are needed before the conservatism becomes small.

*Tuning constants.* The number of episodes (5 to 100) and the pseudo-count of the scale estimate (5 to 80) change coverage by less than 0.002 and 0.006 respectively.

*Nominal level.* Supplementary table S23 gives the results for nominal levels 0.80 and 0.95. The pattern is the same: sample-fold split conformal prediction under-covers and LotCP-S with $m\ge5$ covers slightly above the nominal level.


*Other shifts.* When only the two seasons before the target are used as source, LotCP-S still covers 0.918 at $m=10$, with wider intervals (4.30 % DMC) because fewer and less diverse past lots are available. When a whole growing region or a whole cultivar is held out, coverage at $m=10$ is 0.913 and 0.907. In these two protocols the source contains all seasons, so they test a region or cultivar shift without a season shift.

# Supplementary Note S2. Computational analysis


The cost of the method is dominated by the season-held-out fits, one per source season, which are done once when the calibration is built (supplementary table S24). Energy use was not measured; on the CPU used here the complete cross-fitting for one target season took 40 s for PLS and 23 min for the CNN. The episodic calibration itself takes about 1.8 s for 187 past lots and 30 episodes, and the deployment step is a bias and a scale per lot, which is negligible on the embedded processor of a handheld instrument. The relevant cost is the number of destructive reference measurements. Fig. 4 expresses the trade-off: with LotCP-S and PLS, three reference samples per lot give a mean width of 3.83 % DMC, ten give 3.45, and thirty give 3.28; most of the gain is obtained with the first five to ten samples.

# Supplementary Note S3. Error analysis

![Fig. S3. Error analysis at m = 10 (PLS). (a) Lot coverage against the absolute lot bias. (b) Lot coverage against the ratio of the lot's residual standard deviation to the prior scale. (c) Coverage by reference DMC range.](figures/fig9_error_analysis.png){width=6.5in}

We examined coverage at the level of the lot and of the scan for $m=10$ (Fig. S3). Of the 137 target lots, 38 have coverage below 0.80 under sample-fold split conformal prediction, 13 under LotCP and 4 under LotCP-S. For split conformal prediction, lot coverage is governed by the absolute lot bias (Spearman correlation -0.79). After bias correction the bias no longer matters much, and the remaining failures are lots whose residual spread exceeds what past lots suggest: the correlation between lot coverage and the ratio of the lot's residual standard deviation to the prior scale is -0.95 for LotCP and -0.84 for LotCP-S. The scale estimate of LotCP-S reduces the number of badly covered lots but cannot identify a wide lot reliably from ten reference samples and the repeated scans; the lot with the lowest coverage has a residual spread of 2.2 times the prior scale.

By subgroup, LotCP-S coverage is 0.93 for fruit at the green stage and 0.90 for fruit at the ripening stage; 0.91, 0.90 and 0.89 for the low, medium and high fruit-temperature classes; 0.92 for instrument units present in the source seasons and 0.92 for units that are new in the target season; and 0.92 and 0.96 for cultivars present in and absent from the source seasons. The lower coverage at the ripening stage is in line with the finding of the data set's authors that physiological stage affects model performance more than cultivar, season or region [@anderson2020]. Among cultivars the lowest coverage is 0.86 for Keitt. Scans carrying the provider's first outlier flag are covered at 0.81 (0.50 under sample-fold split conformal prediction). Coverage is lower at the extremes of the DMC range (Fig. S3c), a known limitation of scores that do not adapt to the predicted value. These figures are a reminder that the guarantee is marginal: a lot of ripening fruit, or a lot measured with atypical scatter, can be covered below the nominal level even when coverage is nominal on average.


# Supplementary Note S4. Deviations from the pre-specified protocol

(D1) LotCP-S was added after the first run on one predictor and one target season (PLS, 2018) showed that the pre-specified LotCP under-covered because the residual scale of that season's lots exceeded that of the source lots. The scale estimator of Eq. (3) was developed on source-season residuals only. Results for PLS on 2018 should therefore be read as development data for LotCP-S; the other four target seasons and the other two predictors had not been evaluated when the design was fixed. Both variants are reported everywhere. (D2) The centred target-only baseline (e) was added to give target-only calibration its strongest form. (D4) After the first complete evaluation and during internal review, the following were added and are reported whatever their outcome: the ablation of LotCP-S on lot-fold residuals, the slope/bias and spiking baselines, the single-instrument deployment unit, the sample-split estimation of the constants and the season jackknife. (D5) The empirical-Bayes shrinkage of the bias estimate, part of the pre-specified method, was removed from the reported method after the external validation: it was immaterial on the mango data and harmful under the LUCAS campaign shift (Supplementary Note S5). All mango results were recomputed with the plain mean; the shrinkage versions are reported as ablations. (D6) The external validation on soil spectra, the lot-level assurance variant LotCP-A, the harvest-decision simulator, the economic analysis, the planner and the prototype were added in revision, after the main interval results were known. (D3) For computational reasons the CNN was trained for 20 rather than 30 epochs; lot-grouped folds were computed for one CNN seed only; and in the leave-one-season-out protocol the CNN uses one seed with season folds. These choices were made before any CNN result existed.
