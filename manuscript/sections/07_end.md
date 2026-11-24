# 15. Discussion

**From an error bar to a harvest decision.** The professional question behind a handheld NIR reading is not "what is the DMC?" but "can this fruit, or this block, be picked now?". The simulation shows that the answer depends less on the point predictor than on how its uncertainty is handled. Deciding on the point value let through {{r.hvp('point',0,None)}} % immature fruit among those accepted, and in {{r.hvp('point',0,None,'lots_over_10pct')}} % of lots more than one accepted fruit in ten was immature. A calibrated lower bound, with ten fruit of the lot tested destructively, brought these figures to {{r.hvp('lotcp_s_lower',10,0.1,digits=1)}} % and {{r.hvp('lotcp_s_lower',10,0.1,'lots_over_10pct')}} % of lots. In exchange, more mature fruit was held back ({{r.hvp('lotcp_s_lower',10,0.1,'compliant_accepted')}} % accepted instead of {{r.hvp('point',0,None,'compliant_accepted')}} %), a trade the grower can set explicitly through the cost ratio. At lot level, the reference fruit reduced premature harvests from {{r.lotdp('point',0,None)}} % to {{r.lotdp('lotcp_s_lower',10,1/3)}} % of not-ready lots at an unchanged rate of delay. Under every cost scenario we examined, any calibrated bound was far cheaper than a decision on the point value. The few-shot calibration added a further saving when withholding mature fruit is relatively costly, and a confidence level derived from the cost ratio that stayed close to the best one across predictors.

**What the method adds over a simple margin, and what it does not.** At fruit level, once the bias of a lot is corrected and the confidence level is free, LotCP-S and the simpler "bias correction plus a margin from past residuals" make nearly the same decisions. We report this plainly, because it locates the contribution: the large gain comes from using reference fruit and a bound at all, and the calibration of LotCP determines whether the bound means what it says. That matters in three places: when the level is set from costs, where the uncalibrated margin is well tuned for one predictor and not for another; when a statement about the lot itself is wanted, which only LotCP-A provides; and when the number of reference fruit must be planned before the season, which needs a calibration of how the width depends on *m*.

**What the user of a handheld instrument should take from this.** An error bar derived from the calibration set, by cross-validation, by a conformal quantile on held-out samples or by the predictive variance of a neural network, describes the past lots. On the lots of a later season it was too narrow in every one of the five seasons we could test and for every predictor. The size of the shortfall, {{f"{100*(0.9-max(r.m(k,0) for k in ('gauss','scp_sample','scp_lot','cqr_sample','qrf','ensemble','mc_dropout'))):.0f}"}} to {{f"{100*(0.9-min([r.m(k,0) for k in ('gauss','scp_sample','scp_lot','cqr_sample','qrf','ensemble','mc_dropout')]+[r.gen(mo,'forward','scp_sample',0) for mo in ('gbm','cnn')])):.0f}"}} coverage points at a nominal 90 % depending on the method and the predictor, is large enough to matter for a decision against a specification, and it is concentrated in a minority of lots that are covered very badly (Fig. 5).

**Without reference samples there is no cheap repair.** Season-held-out calibration is the honest label-free option and should replace sample-fold calibration when intervals are quoted for a future season. It restores coverage on average, at the price of intervals {{r.pct(r.m('scp_season',0,'width'), r.m('scp_sample',0,'width'))}} % wider, and its per-season coverage still ranged over {{r.season_range('scp_season',0)}}. This is not a defect of the procedure. With four to six past seasons there is little information about how different the next one will be, and no reweighting of unlabelled spectra recovers a bias in the residual.

**The pattern is not specific to mango.** On soil spectra the same three observations recur: coverage is lost on a new population, by two points across exchangeable survey projects and by twenty-seven to fifty points across survey campaigns; no calibration confined to the source repairs a between-campaign shift; and five local reference samples bring coverage back to within a few points of nominal. The soil results also correct the method: they exposed the shrinkage step as unsafe, and they show that when the residual scale changes between campaigns the intervals remain slightly too narrow.

**A few reference samples are worth more than any modelling choice we tried.** Three destructive measurements per lot moved every bias-correcting method to at least nominal coverage and brought the width back to that of the invalid intervals. This supports, with coverage figures, the long-standing practice of checking a calibration against a few fruit of the new population. LotCP-S then answers the follow-up question of how to turn those samples into the narrowest interval that remains valid: it was the best of the compared methods for 3 to 20 samples per lot with PLS, its coverage was stable across predictors where that of the common bias-correction shortcut was not, and it converts additional reference samples into narrower intervals. On the mango data its efficiency advantage over that shortcut at fewer than about twenty reference samples came from the repeated scans of each fruit: without them the two did not differ significantly. On the soil survey, where there are no repeated scans but the shift is large, LotCP-S was significantly better than the shortcut because the shortcut under-covered. Taking two or three scans per fruit, which costs seconds, is therefore part of the recommendation. When 20 to 30 samples per lot are available, calibration on those samples alone is as good and has the stronger, lot-conditional guarantee; the past lots then add nothing.

**Average coverage is not what a grower buys.** With near-nominal marginal coverage, about three lots in ten were still covered below the nominal level, and target-only calibration, valid on average for each lot, was no better in this respect once the reference set was large. Calibrating on the lot-wise quantiles of past lots (LotCP-A) kept nine lots in ten at the stated coverage for a quarter more width, across predictors and on exchangeable soil projects, and fell a few points short across survey campaigns. We regard this lot-level statement as the more natural specification for calibration maintenance and the marginal interval as its efficient complement.

**Which parts of the method earn their place.** The ablation gives a sober answer. The lot-specific scale and, without reference samples, the season-level hold-out carry the result. Empirical-Bayes shrinkage of the bias, which motivated the design, was immaterial on the mango data, because lot biases are large compared with the noise of a sample mean, and harmful under the campaign shift of the soil survey, where it pulled the correction towards a past that no longer applied. It was removed. The general lesson is that a few-shot correction should not borrow strength from past groups for the very quantity that the shift changes. Season-held-out residuals are essential without reference samples but not with them: once the bias is corrected, lot-fold residuals gave slightly narrower intervals at coverage no lower by season, and a practitioner who always collects reference samples can use them and save the season-wise refits.

**Relation to concurrent work.** Kayaoğlu and Erdem [@kayaoglu2026] report that split conformal coverage is lost under instrument transfer and quantify the labelled target samples needed to restore it. Our findings for harvest seasons agree in direction. The settings differ in that a multi-season calibration set contains many past lots, which lets the few-shot correction be calibrated before the new lot is seen.

**Practical procedure.** (0) Decide whether the interval should be right on average (LotCP-S) or for nine lots in ten (LotCP-A), and state the relative cost of withholding a mature fruit and of accepting an immature one; this fixes the confidence level. (0′) Read from the planner, for the expected lot size, how many reference fruit to test. (1) Build the calibration with season-grouped cross-validation and store the season-held-out residuals with their lot and sample identifiers. (2) For a new lot, scan the fruit, with repeated scans where possible, and measure 5 to 10 randomly chosen fruit destructively. (3) Report $f(x)+\hat b\pm \hat q_m\hat s$. (4) After the season, add the lot to the calibration set.

# 16. Limitations

*Retrospective, not prospective.* All results come from replaying archived data season by season. The workflow has not been used to decide a real harvest, and the paper does not show that it reduces harvest losses in practice. A prospective validation would calibrate on all seasons up to the current one, apply the prototype to new lots during a harvest season, record the decisions and verify them with reference measurements on the harvested fruit; we regard it as the necessary next step before deployment.

*Assumed costs.* The economic analysis uses cost ratios expressed in units of fruit value because no cost data are available for the public data set. The ranking of rules was stable across the ratios examined, but the optimal number of reference fruit and the size of the saving depend on the assumptions, and growers would substitute their own.

*Decision model.* The lot-level rule (harvest when 80 % of scanned fruit pass) and the specifications of 14–16 % DMC are illustrative choices. Commercial practice varies by cultivar and market, and maturity is not determined by DMC alone.

*One fruit data set.* The fruit results come from one public data set of mango scanned with handheld units of one model in two Australian regions. We found no second public fruit NIR data set with a lot and season structure. The external validation on soil spectra shows that the mechanism and the remedy carry over to another material, spectral range and instrument, but it does not replace a second fruit or a prospective orchard trial, and the soil analysis uses a single predictor (PLS), lots defined by us (grid cells) or by the survey (projects), and no season level.

*Few seasons.* Five target seasons are a small sample at the level that matters most. Lot-level confidence intervals and tests treat lots within a season as independent, which they are not entirely; per-season results are reported for that reason, and the season-to-season range of coverage should be read as the realistic uncertainty.

*Marginal guarantee and approximate assumptions.* The guarantee of Section 4.7 is marginal over lots and assumes exchangeable lots. Lots of ripening fruit, of some cultivars and with unusually large scatter were covered below the nominal level. The calibration residuals come from season-held-out models rather than from the deployed model, which made the method conservative when only two source seasons were available.

*Selection effects.* The number of PLS latent variables is chosen with the same season-held-out predictions that later provide the calibration residuals, a choice among seven values that could make those residuals slightly optimistic. LightGBM and the CNN involve no such selection and behave alike.

*Reference sampling.* We assume that reference samples are drawn at random from the lot and that their reference values are as accurate as those of the calibration set. Sampling only the fruit that is easy to reach would bias the correction. In the data set a reference sample is a tissue sample with repeated scans; in an orchard the reference fruit would be scanned on the tree before being picked.

*Protocol deviation.* The scale-adaptive variant was designed after inspecting one predictor on one target season. The other seasons and predictors support it, but it was not pre-specified.

*Repeated scans.* The data set has many scans per sample (several instrument units and, for some samples, three temperatures), which is richer than routine practice. The single-instrument analysis reduces but does not remove this advantage.

*Scores.* The score does not adapt to the predicted DMC, and coverage was lower at the extremes of the DMC range. One-sided bounds were evaluated for two predictors and three illustrative specifications.

*Details taken from the data description.* The measurement geometry and reference method are described here as in the publications that accompany the data set; we did not collect the data, and we interpret the file's "population" field as a harvest lot following those publications.

# 17. Conclusion

Error bars attached to handheld NIR predictions of mango dry matter content, when they are calibrated within the training seasons, do not keep their nominal coverage on later seasons, and decisions taken on point predictions let a substantial share of immature fruit into the harvest. A risk-aware workflow addresses this. A few fruit per lot are tested destructively, a few-shot conformal calibration corrects the lot's bias and scale, and each fruit is harvested only when its calibrated lower bound meets the specification at a confidence level set by the cost ratio of the two possible errors. In a retrospective simulation over five seasons, this workflow restored near-nominal coverage from three reference fruit and reduced immature fruit among those accepted from about 13 % to about 1 %. It roughly halved premature lot harvests at an unchanged rate of delay and lowered the expected cost of the decision under every cost scenario examined. A planner computed from past lots tells the grower beforehand how precise the error bar will be for a given number of reference fruit. The findings replicated on soil spectral libraries. Prospective validation in an orchard is the step that remains before the workflow can be recommended for practice.

# CRediT authorship contribution statement

**P N Bhargav Teja:** Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Visualization, Writing – original draft, Writing – review & editing. **Ragavan K:** Supervision.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used Claude (Anthropic) to search and screen the literature, write and run the analysis code, and draft and revise the text. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

# Data availability

The data analysed in this study are publicly available. Mango NIR spectra and dry-matter reference values: Mendeley Data, "Mango DMC and NIR spectra", version 6, https://doi.org/10.17632/46htwnp833.6 (CC BY 4.0) [@mangodata]. Soil vis–NIR spectra and laboratory data: Open Soil Spectral Library v1.2 [@safanelli2025], https://soilspectroscopy.org, files ossl_visnir_L0_v1.2.csv.gz, ossl_soilsite_L0_v1.2.csv.gz and ossl_soillab_L0_v1.2.csv.gz at https://storage.googleapis.com/soilspec4gg-public/. The code, including the decision-support prototype, and the derived results will be made available from the corresponding author on reasonable request.

# Ethics statement

The study uses public data sets of fruit and soil spectra and involves no human participants, animals or personal data.

# Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

# Acknowledgements

The authors thank the creators of the mango data set at Central Queensland University and the developers of the Open Soil Spectral Library for making their data public.

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

Supplementary tables S1–S24 (complete machine-generated result tables, including all paired tests and per-seed results), figure S1 and the pre-specified protocol with its deviation log accompany this article.

# References

::: {#refs}
:::
