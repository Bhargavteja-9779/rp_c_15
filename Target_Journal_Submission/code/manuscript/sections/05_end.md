# 16. Discussion

**What the user of a handheld instrument should take from this.** An error bar derived from the calibration set, by cross-validation, by a conformal quantile on held-out samples or by the predictive variance of a neural network, describes the past lots. On the lots of a later season it was too narrow in every one of the five seasons we could test and for every predictor. The size of the shortfall, six to fourteen coverage points at a nominal 90 % depending on the method and the predictor, is large enough to matter for a decision against a specification, and it is concentrated in a minority of lots that are covered very badly (Fig. 5).

**Without reference samples there is no cheap repair.** Season-held-out calibration is the honest label-free option and should replace sample-fold calibration when intervals are quoted for a future season. It restores coverage on average, at the price of intervals about a third wider, and its per-season coverage still ranged from 0.82 to 0.99. This is not a defect of the procedure. With four to six past seasons there is little information about how different the next one will be, and no reweighting of unlabelled spectra recovers a bias in the residual.

**The pattern is not specific to mango.** On soil spectra the same three observations recur: coverage is lost on a new population, by two points across exchangeable survey projects and by twenty-seven to fifty points across survey campaigns; no calibration confined to the source repairs a between-campaign shift; and five local reference samples bring coverage back to within a few points of nominal. The soil results also correct the method: they exposed the shrinkage step as unsafe, and they show that when the residual scale changes between campaigns the intervals remain slightly too narrow.

**A few reference samples are worth more than any modelling choice we tried.** Three destructive measurements per lot moved every bias-correcting method to at least nominal coverage and brought the width back to that of the invalid intervals. This supports, with coverage figures, the long-standing practice of checking a calibration against a few fruit of the new population. LotCP-S then answers the follow-up question of how to turn those samples into the narrowest interval that remains valid: it was the best of the compared methods for 3 to 20 samples per lot with PLS, its coverage was stable across predictors where that of the common bias-correction shortcut was not, and it converts additional reference samples into narrower intervals. On the mango data its efficiency advantage over that shortcut at fewer than about twenty reference samples came from the repeated scans of each fruit: without them the two did not differ significantly. On the soil survey, where there are no repeated scans but the shift is large, LotCP-S was significantly better than the shortcut because the shortcut under-covered. Taking two or three scans per fruit, which costs seconds, is therefore part of the recommendation. When 20 to 30 samples per lot are available, calibration on those samples alone is as good and has the stronger, lot-conditional guarantee; the past lots then add nothing.

**Average coverage is not what a grower buys.** With near-nominal marginal coverage, about three lots in ten were still covered below the nominal level, and target-only calibration, valid on average for each lot, was no better in this respect once the reference set was large. Calibrating on the lot-wise quantiles of past lots (LotCP-A) kept nine lots in ten at the stated coverage for a quarter more width, across predictors and on exchangeable soil projects, and fell a few points short across survey campaigns. We regard this lot-level statement as the more natural specification for calibration maintenance and the marginal interval as its efficient complement.

**Which parts of the method earn their place.** The ablation gives a sober answer. The lot-specific scale and, without reference samples, the season-level hold-out carry the result. Empirical-Bayes shrinkage of the bias, which motivated the design, was immaterial on the mango data, because lot biases are large compared with the noise of a sample mean, and harmful under the campaign shift of the soil survey, where it pulled the correction towards a past that no longer applied. It was removed. The general lesson is that a few-shot correction should not borrow strength from past groups for the very quantity that the shift changes. Season-held-out residuals are essential without reference samples but not with them: once the bias is corrected, lot-fold residuals gave slightly narrower intervals at coverage no lower by season, and a practitioner who always collects reference samples can use them and save the season-wise refits.

**Relation to concurrent work.** Kayaoğlu and Erdem [@kayaoglu2026] report that split conformal coverage is lost under instrument transfer and quantify the labelled target samples needed to restore it. Our findings for harvest seasons agree in direction. The settings differ in that a multi-season calibration set contains many past lots, which lets the few-shot correction be calibrated before the new lot is seen.

**Practical procedure.** (0) Decide whether the interval should be right on average (LotCP-S) or for nine lots in ten (LotCP-A). (1) Build the calibration with season-grouped cross-validation and store the season-held-out residuals with their lot and sample identifiers. (2) For a new lot, scan the fruit, with repeated scans where possible, and measure 5 to 10 randomly chosen fruit destructively. (3) Report $f(x)+\hat b\pm \hat q_m\hat s$. (4) After the season, add the lot to the calibration set.

# 17. Limitations

*One fruit data set.* The fruit results come from one public data set of mango scanned with handheld units of one model in two Australian regions. We found no second public fruit NIR data set with a lot and season structure. The external validation on soil spectra shows that the mechanism and the remedy carry over to another material, spectral range and instrument, but it does not replace a second fruit or a prospective orchard trial, and the soil analysis uses a single predictor (PLS), lots defined by us (grid cells) or by the survey (projects), and no season level.

*Few seasons.* Five target seasons are a small sample at the level that matters most. Lot-level confidence intervals and tests treat lots within a season as independent, which they are not entirely; per-season results are reported for that reason, and the season-to-season range of coverage should be read as the realistic uncertainty.

*Marginal guarantee and approximate assumptions.* The guarantee of Section 4.7 is marginal over lots and assumes exchangeable lots. Lots of ripening fruit, of some cultivars and with unusually large scatter were covered below the nominal level. The calibration residuals come from season-held-out models rather than from the deployed model, which made the method conservative when only two source seasons were available.

*Selection effects.* The number of PLS latent variables is chosen with the same season-held-out predictions that later provide the calibration residuals, a choice among seven values that could make those residuals slightly optimistic. LightGBM and the CNN involve no such selection and behave alike.

*Reference sampling.* We assume that reference samples are drawn at random from the lot and that their reference values are as accurate as those of the calibration set. Sampling only the fruit that is easy to reach would bias the correction. In the data set a reference sample is a tissue sample with repeated scans; in an orchard the reference fruit would be scanned on the tree before being picked.

*Protocol deviation.* The scale-adaptive variant was designed after inspecting one predictor on one target season. The other seasons and predictors support it, but it was not pre-specified.

*Repeated scans.* The data set has many scans per sample (several instrument units and, for some samples, three temperatures), which is richer than routine practice. The single-instrument analysis reduces but does not remove this advantage.

*Scores.* The score does not adapt to the predicted DMC, and coverage was lower at the extremes of the DMC range. One-sided bounds were studied for one predictor and illustrative specifications only; a cost-based choice of the confidence level was not attempted.

*Details taken from the data description.* The measurement geometry and reference method are described here as in the publications that accompany the data set; we did not collect the data, and we interpret the file's "population" field as a harvest lot following those publications.

# 18. Conclusion

Prediction intervals for mango dry matter content that are calibrated inside the training seasons, by any of the seven procedures we tested (Gaussian band, split conformal prediction with sample or lot folds, conformalised quantile regression, quantile regression forest, deep ensemble, Monte-Carlo dropout), do not keep their nominal coverage on the lots of a later season. Calibrating on season-held-out residuals repairs coverage on average but with much wider intervals and substantial variation between seasons. Three to ten destructively measured reference fruit per lot, used through a lot-exchangeable conformal calibration with a lot-specific scale, give intervals that cover close to the nominal level across predictors and are narrower than those of the alternatives; with twenty or more reference fruit, calibration on those fruit alone is as efficient on average. A lot-level variant keeps nine lots in ten at the stated coverage, which neither the average-coverage methods nor target-only calibration do. The same holds, more sharply, for soil spectra across survey campaigns. Used as a lower bound against a harvest specification, the calibrated interval reduces the share of immature fruit among those accepted by an order of magnitude relative to a decision on the point prediction. The number of reference samples, more than the choice of model, determines how informative a valid error bar can be.

# CRediT authorship contribution statement

[To be completed by the authors: Conceptualization; Methodology; Software; Validation; Formal analysis; Writing – original draft; Writing – review & editing.]

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. [Authors to confirm.]

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used Claude (Anthropic), an AI system operating as an autonomous research agent, to search the literature, select the research question, write the analysis code, run the experiments and draft the manuscript. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article. [The authors must make this statement true before submission by checking the code, re-running the analysis, verifying every reference and revising the text, and must confirm that this extent of AI use is compatible with the journal's current policy.]

# Data availability

The data are publicly available from Mendeley Data (doi:10.17632/46htwnp833, version 6) under a CC BY 4.0 licence [@mangodata]. The code, the stored cross-fitted predictions, all result files and the scripts that regenerate every table and figure of this article are available at [repository URL and archived DOI to be inserted].

# Ethics statement

The study uses a public data set of fruit spectra and involves no human participants, animals or personal data.

# Funding

[To be completed by the authors, or: This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.]

# Acknowledgements

The authors thank the creators of the mango data set at Central Queensland University for making it public.

# Appendix A. Formal statements and proofs

*Setting.* Fix the number of reference samples $m$, the predictor and the constants entering Eqs. (3)–(4). A lot $Z$ is a finite random object: its samples, their scans, and the residual and prediction of every scan. For a lot $Z$ with at least $m+1$ samples, let $\Pi_Z$ denote the distribution of the score obtained as follows: draw a reference set $A$ uniformly among the $m$-subsets of the samples of $Z$; compute $\hat b$ and $\hat s$ from $A$ and the scans of $Z$; draw a sample uniformly among the non-reference samples and a scan uniformly among its scans; return the score of Eq. (5). $\Pi_Z$ is a probability measure on the real line determined by $Z$, and it embodies the lot, sample and scan weights of Eq. (6). Let $Z_1,\dots,Z_K$ be the calibration lots and $Z_{K+1}$ the new lot, whose reference set is drawn at random and whose score for a randomly drawn non-reference scan is $S_{K+1}\sim\Pi_{Z_{K+1}}$ given $Z_{K+1}$.

**Assumption 1.** The lots $Z_1,\dots,Z_{K+1}$ are exchangeable.

**Proposition 1 (marginal coverage of LotCP and LotCP-S).** Let $\hat G=\frac{1}{K+1}\sum_{k=1}^{K}\Pi_{Z_k}+\frac{1}{K+1}\delta_{+\infty}$ and $\hat q=Q_{1-\alpha}(\hat G)$. Under Assumption 1, $\mathbb{P}\{S_{K+1}\le\hat q\}\ge 1-\alpha$; equivalently, the interval of Eq. (7) covers the reference value of a randomly drawn non-reference scan of the new lot with probability at least $1-\alpha$.

*Proof.* Let $G=\frac{1}{K+1}\sum_{k=1}^{K+1}\Pi_{Z_k}$ and $q^\ast=Q_{1-\alpha}(G)$. Replacing $\Pi_{Z_{K+1}}$ by a point mass at $+\infty$ can only move mass to the right, so $\hat q\ge q^\ast$. For each $k$ let $S_k$ be drawn from $\Pi_{Z_k}$ given the lots, independently across $k$. The pairs $(Z_k,S_k)$ are exchangeable because the lots are and the same kernel generates every $S_k$, and $q^\ast$ is a symmetric function of the lots. Hence $\mathbb{P}\{S_{K+1}\le q^\ast\}=\frac{1}{K+1}\sum_{k=1}^{K+1}\mathbb{P}\{S_k\le q^\ast\}=\mathbb{E}\big[G((-\infty,q^\ast])\big]\ge 1-\alpha$, the last step by the definition of the quantile. Since $\hat q\ge q^\ast$, the claim follows. $\square$

*Remark 1 (finite number of episodes).* The implementation replaces $\Pi_{Z_k}$ by the average over $E$ independent reference sets, with all non-reference scans enumerated. The proposition holds for this version as stated. Attach $E$ independent reference sets to every lot, including the new one, of which the first is the set actually used at deployment. The augmented lots are exchangeable, $q^\ast$ computed from the $E$-set averages is symmetric in the lots and in the $E$ sets of each lot, and by exchangeability of the $E$ sets of the new lot the score from its first set has the same probability of not exceeding $q^\ast$ as a score drawn from its $E$-set average. The proof then proceeds as above.

*Remark 2 (unequal lots).* No condition on lot sizes or on the number of scans per sample is needed beyond exchangeability of the lots as random objects, because $\Pi_Z$ is defined lot by lot. Lots with fewer than $m+10$ samples are excluded from calibration and from evaluation alike, so the statement refers to the population of eligible lots.

**Proposition 2 (lot-level assurance of LotCP-A).** For a lot $Z$ and a reference set $A$ let $Q(Z,A)$ be the weighted $(1-\alpha)$ quantile of the scores of the non-reference scans, and $C(Z,A,q)$ the weighted share of those scans whose score does not exceed $q$, with the weights of Eq. (6). Let $\Lambda_Z$ be the distribution of $Q(Z,A)$ over the random reference set, and $\hat q^{A}=Q_{1-\delta}\big(\frac{1}{K+1}\sum_{k=1}^{K}\Lambda_{Z_k}+\frac{1}{K+1}\delta_{+\infty}\big)$. Under Assumption 1, $\mathbb{P}\{C(Z_{K+1},A,\hat q^{A})\ge 1-\alpha\}\ge 1-\delta$.

*Proof.* By the definition of the quantile, $C(Z,A,q)\ge 1-\alpha$ if and only if $q\ge Q(Z,A)$. The statistic $Q(Z_{K+1},A)$ of the new lot is a draw from $\Lambda_{Z_{K+1}}$, and the argument of Proposition 1 applied to the measures $\Lambda_{Z_k}$ in place of $\Pi_{Z_k}$, at level $1-\delta$, gives $\mathbb{P}\{Q(Z_{K+1},A)\le\hat q^{A}\}\ge 1-\delta$. Remark 1 applies in the same way. $\square$

*Scope of the statements.* Proposition 1 is the hierarchical conformal guarantee of Lee et al. [@lee2023] written for a score that depends on a random reference set, with three nested levels and unequal group sizes; Proposition 2 is a statement of the probably-approximately-correct type [@park2022] at the level of the lot. Both require the predictor and the constants to be fixed independently of the calibration lots and the new lot to be exchangeable with past lots. Section 4.7 lists how the implementation departs from these conditions, and the experiments measure the consequences.

# Appendix B. Supplementary material

Supplementary tables S1–S15 (complete machine-generated result tables, including all paired tests and per-seed results), figure S1 and the pre-specified protocol with its deviation log accompany this article.

# References

::: {#refs}
:::
