# 5. Discussion

**What the audit shows.** An error bar calibrated inside the training seasons, whether by cross-validation, a conformal quantile on held-out samples or the predictive variance of a neural network, describes past lots. On later-season mango lots it was too narrow: pooled over lots, by {{f"{100*(0.9-max(r.m(k,0) for k in ('gauss','scp_sample','cqr_sample','qrf','ensemble','mc_dropout'))):.0f}"}} to {{f"{100*(0.9-min(r.m(k,0) for k in ('gauss','scp_sample','cqr_sample','qrf','ensemble','mc_dropout'))):.0f}"}} coverage points at a nominal 90 % across the Gaussian band, sample-fold split CP and CQR, the quantile forest, the deep ensemble and MC dropout; for sample-fold split CP with SNV PLS the shortfall by season ranged from {{f"{100*(0.9-max(r.ss('scp_sample',0,f'cov_{y}') for y in range(2017,2022))):.1f}"}} to {{f"{100*(0.9-min(r.ss('scp_sample',0,f'cov_{y}') for y in range(2017,2022))):.1f}"}} points, and the shortfall was concentrated in a minority of badly covered lots. Holding out whole seasons is the honest repair without reference fruit, but with four to six past seasons it reached nominal coverage only in the season that happened to be over-covered. These findings agree in direction with the loss of coverage reported under instrument transfer [@kayaoglu2026] and with the long-standing observation that NIR accuracy degrades on new populations [@nicolai2007; @anderson2020]; the audit adds the lot-by-lot, season-by-season picture that a decision against a specification needs.

**What reference fruit and the calibration add.** A few reference fruit per lot did most of the work: once the lot bias was corrected, every method moved close to or above nominal coverage. Within LotCP-S, the lot scale estimated partly from repeated scans gave narrower intervals than bias correction with a fixed half-width, though this gain was not confirmed on independent soil data and vanished without repeated scans, and the replay of the $m$-shot procedure kept coverage {{f"{100*r.st('lotcp_s','biascorr_full','coverage',10):.0f}"}}–{{f"{100*r.st('lotcp_s','biascorr_full','coverage',3):.0f}"}} points higher than the same correction without replay. Pooled over past lots, however, the calibration still under-covered in seasons unlike the largest past ones: without 2017, LotCP-S covered {{f"{r.ss('lotcp_s',10,'coverage_ex2017'):.3f}"}}.

**Seasons as the unit of calibration.** Pooling past lots under-covered in seasons unlike the largest past ones. Calibrating within each past season and taking an upper order statistic across seasons, an idea introduced for multi-environment prediction [@duchi2024multienv] and applied here with the few-shot replay, restored coverage of 0.90 in every season and for every predictor across repeated reference draws. It did so at the width of a fixed level of about $\alpha=0.08$, so its value lies in choosing the level from the spread of past seasons, before the season and without target labels, not in narrower intervals. Its season-level guarantee is explicit but weak with two to six past seasons, and its success here is larger than the guarantee implies; it should be confirmed on new seasons. Two cheaper ideas did not help: the reference fruit of earlier lots in the same season were too few to estimate a season's tail, and label-free spectral statistics did not predict which lots were biased.

**What changes in the decision.** In the exploratory simulation, the benefit came from replacing the point value by any calibrated lower bound, which cut the assumed cost by about {{f"{r.dd('point',0):.0f}"}} units per 100 fruit in every season and kept immature fruit out of the harvest. Reference fruit did not lower the expected cost further at the pre-stated operating point. Their value lies in making the bound mean what it says for the lot in hand, which matters when the level is set from costs, and in a lower rate of delayed ready lots that five seasons could not resolve statistically. The cost-derived level $\alpha^\ast$ was as good as a level chosen from other seasons, which supports the newsvendor reading of the rule.

**Practical procedure.** (0) Where coverage must hold season by season, choose the level from past seasons with the season-robust multiplier (LotCP-R2, or LotCP-AR for a lot-level statement), or, equivalently in width, a fixed level near $\alpha=0.08$ on these data. Where only single scans are taken and width matters little, bias correction with a sample-fold half-width was a safe simple option on these data; LotCP-S is preferable when repeated scans are available, when the half-width should shrink with *m*, or with flexible predictors for which that shortcut under-covered (Supplementary Note S5). (1) Build the calibration with season-grouped cross-validation and keep the season-held-out residuals with lot and sample identifiers. (2) Before the season, read the planned width for each $m$ and state the cost ratio, which fixes $\alpha^\ast$. (3) In the orchard, scan the fruit of a lot with two or three scans per fruit, test five to ten randomly chosen fruit, and harvest a fruit or lot when the calibrated lower bound meets the specification. (4) After the season, add the lot to the calibration set and check the realised coverage.

# 6. Limitations

In order of importance:

1. *Retrospective only.* All results replay archived data. The workflow has not been used to decide a harvest, and the paper does not show that it reduces losses in an orchard. A prospective trial that records decisions and verifies them on harvested fruit is the necessary next step.
2. *Few seasons and one fruit data set.* Five target seasons are a small sample at the level that dominates the error, and the confidence intervals reflect this. We found no second public fruit NIR data set with lot and season structure; the soil libraries test the coverage audit and the calibration on another material but have no season level, and the independent soil data showed little shift to repair.
3. *Guarantees hold only approximately, and the season-level one is weak with few seasons.* Pooled guarantees assume exchangeable lots and failed under season shift. The season-robust replay assumes exchangeable seasons, which a trend in climate, cultivars or instruments would violate, and with two to six past seasons its season-level probability is only {{f"{(r.rq('n_groups',fn=min)-1)/(r.rq('n_groups',fn=min)+1):.2f}"}}–{{f"{(r.rq('n_groups')-1)/(r.rq('n_groups')+1):.2f}"}} for LotCP-R2 (LotCP-R2 was chosen after LotCP-R failed its planned width limit); it was developed and evaluated on seasons already examined, so it needs confirmation on new seasons.
4. *Exploratory components.* The lot scale was designed after inspecting 2018, and LotCP-A, the planner, the decision simulation and the matched baselines were added after the main results. The protocol was committed internally, not publicly registered.
5. *Assumed costs and illustrative decision rules.* Costs are expressed in units of fruit value, the specification of 15 % DMC and the 80 % lot rule are illustrative, and maturity is not determined by DMC alone.
6. *Repeated scans richer than routine practice.* The data contain scans from several instrument units and temperatures per fruit; the efficiency gain of LotCP-S depended on them.
7. *Reference sampling.* Reference fruit are assumed to be drawn at random and measured as accurately as the calibration set.

# 7. Conclusion

Error bars for handheld NIR predictions of mango dry matter, calibrated inside the training seasons, did not keep their coverage on later-season lots. A few reference fruit per lot, with a few-shot conformal calibration that corrects bias and scale, restored coverage on average, but not season by season, because seasons differed by more than past lots suggested. Calibrating within each past season and across seasons, following multi-environment conformal prediction, restored 90 % coverage in every season in exploratory analyses, at the width of a modestly higher fixed confidence level that it selects from past seasons. Learning the shift from earlier lots of the season and spectral warning signs did not help. In an exploratory decision analysis, a calibrated lower bound was cheaper than the point value, a weak comparator, and reference fruit gave no detectable further saving. Confirmation on new seasons and a prospective orchard trial are the steps that remain.

# CRediT authorship contribution statement

**P N Bhargav Teja:** Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Visualization, Writing – original draft, Writing – review & editing. **Ragavan K:** Supervision.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Declaration of generative AI and AI-assisted technologies in the research and manuscript preparation process

During this work the authors used Claude (Anthropic) to search and screen the literature, write and run the analysis code, design and run experiments, draft and revise the text, and simulate peer review (Section 3.8); analyses added in response to the simulated review are marked as such. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

# Data availability

All data analysed are public. Mango NIR spectra and dry-matter values: Mendeley Data, "Mango DMC and NIR spectra", version 6, https://doi.org/10.17632/46htwnp833.6 (CC BY 4.0) [@mangodata]. NeoSpectra handheld NIR soil library: Zenodo, https://doi.org/10.5281/zenodo.13122321. Soil vis–NIR spectra: Open Soil Spectral Library v1.2 [@safanelli2025], https://soilspectroscopy.org (files ossl_visnir_L0_v1.2.csv.gz, ossl_soilsite_L0_v1.2.csv.gz, ossl_soillab_L0_v1.2.csv.gz). The code, the derived results, the internal protocol history and the decision-support prototype (Supplementary Note S6) will be made available from the corresponding author on reasonable request.

# Ethics statement

The study uses public data sets of fruit and soil spectra and involves no human participants, animals or personal data.

# Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

# Acknowledgements

The authors thank the creators of the mango data set at Central Queensland University and the developers of the Open Soil Spectral Library and the NeoSpectra library for making their data public.

# Appendix A. Formal statements and proofs

*Setting.* Fix the number of reference samples $m$, the predictor and the constants entering Eqs. (2)–(3). A lot $Z$ is a finite random object: its samples, their scans, and the residual and prediction of every scan. For a lot $Z$ with at least $m+1$ samples, let $\Pi_Z$ denote the distribution of the score obtained as follows: draw a reference set $A$ uniformly among the $m$-subsets of the samples of $Z$; compute $\hat b$ and $\hat s$ from $A$ and the scans of $Z$; draw a sample uniformly among the non-reference samples and a scan uniformly among its scans; return the score of Eq. (4). $\Pi_Z$ is a probability measure on the real line determined by $Z$, and it embodies the lot, sample and scan weights of Eq. (5). Let $Z_1,\dots,Z_K$ be the calibration lots and $Z_{K+1}$ the new lot, whose reference set is drawn at random and whose score for a randomly drawn non-reference scan is $S_{K+1}\sim\Pi_{Z_{K+1}}$ given $Z_{K+1}$.

**Assumption 1.** The lots $Z_1,\dots,Z_{K+1}$ are exchangeable.

**Proposition 1 (marginal coverage of LotCP and LotCP-S).** Let $\hat G=\frac{1}{K+1}\sum_{k=1}^{K}\Pi_{Z_k}+\frac{1}{K+1}\delta_{+\infty}$ and $\hat q=Q_{1-\alpha}(\hat G)$. Under Assumption 1, $\mathbb{P}\{S_{K+1}\le\hat q\}\ge 1-\alpha$; equivalently, the interval $C(x)$ of Section 2.4 covers the reference value of a randomly drawn non-reference scan of the new lot with probability at least $1-\alpha$.

*Proof.* Let $G=\frac{1}{K+1}\sum_{k=1}^{K+1}\Pi_{Z_k}$ and $q^\ast=Q_{1-\alpha}(G)$. Replacing $\Pi_{Z_{K+1}}$ by a point mass at $+\infty$ can only move mass to the right, so $\hat q\ge q^\ast$. For each $k$ let $S_k$ be drawn from $\Pi_{Z_k}$ given the lots, independently across $k$. The pairs $(Z_k,S_k)$ are exchangeable because the lots are and the same kernel generates every $S_k$, and $q^\ast$ is a symmetric function of the lots. Hence $\mathbb{P}\{S_{K+1}\le q^\ast\}=\frac{1}{K+1}\sum_{k=1}^{K+1}\mathbb{P}\{S_k\le q^\ast\}=\mathbb{E}\big[G((-\infty,q^\ast])\big]\ge 1-\alpha$, the last step by the definition of the quantile. Since $\hat q\ge q^\ast$, the claim follows. $\square$

*Remark 1 (finite number of episodes).* The implementation replaces $\Pi_{Z_k}$ by the average over $E$ independent reference sets, with all non-reference scans enumerated. The proposition holds for this version as stated. Attach $E$ independent reference sets to every lot, including the new one, of which the first is the set actually used at deployment. The augmented lots are exchangeable, $q^\ast$ computed from the $E$-set averages is symmetric in the lots and in the $E$ sets of each lot, and by exchangeability of the $E$ sets of the new lot the score from its first set has the same probability of not exceeding $q^\ast$ as a score drawn from its $E$-set average. The proof then proceeds as above.

*Remark 2 (unequal lots).* No condition on lot sizes or on the number of scans per sample is needed beyond exchangeability of the lots as random objects, because $\Pi_Z$ is defined lot by lot. Lots with fewer than $m+10$ samples are excluded from calibration and from evaluation alike, so the statement refers to the population of eligible lots.

**Proposition 2 (lot-level assurance of LotCP-A).** For a lot $Z$ and a reference set $A$ let $Q(Z,A)$ be the weighted $(1-\alpha)$ quantile of the scores of the non-reference scans, and $C(Z,A,q)$ the weighted share of those scans whose score does not exceed $q$, with the weights of Eq. (5). Let $\Lambda_Z$ be the distribution of $Q(Z,A)$ over the random reference set, and $\hat q^{A}=Q_{1-\delta}\big(\frac{1}{K+1}\sum_{k=1}^{K}\Lambda_{Z_k}+\frac{1}{K+1}\delta_{+\infty}\big)$. Under Assumption 1, $\mathbb{P}\{C(Z_{K+1},A,\hat q^{A})\ge 1-\alpha\}\ge 1-\delta$.

*Proof.* By the definition of the quantile, $C(Z,A,q)\ge 1-\alpha$ if and only if $q\ge Q(Z,A)$. The statistic $Q(Z_{K+1},A)$ of the new lot is a draw from $\Lambda_{Z_{K+1}}$, and the argument of Proposition 1 applied to the measures $\Lambda_{Z_k}$ in place of $\Pi_{Z_k}$, at level $1-\delta$, gives $\mathbb{P}\{Q(Z_{K+1},A)\le\hat q^{A}\}\ge 1-\delta$. Remark 1 applies in the same way. $\square$

**Proposition 3 (season level, LotCP-R).** Let seasons $1,\dots,S+1$ be exchangeable random collections of lots, with season $S+1$ the new one, and let $T_s$ be the multiplier of Eq. (7) computed with a common, fixed score function from the lots of season $s$. Let $T_{(k)}$ be the $k$-th largest of $T_1,\dots,T_S$. (i) $\mathbb{P}\{T_{S+1}\le T_{(k)}\}\ge (S+1-k)/(S+1)$. (ii) If, in addition, a new lot $Z$ of season $S+1$ is exchangeable with that season's lots, the interval with multiplier $T_{(k)}$ covers a random non-reference scan of $Z$ with probability at least $1-\alpha-k/(S+1)$.

*Proof.* (i) $T_1,\dots,T_{S+1}$ are exchangeable, so the rank of $T_{S+1}$ among them is uniform (ties broken at random), and $T_{S+1}>T_{(k)}$ requires it to be among the $k$ largest, which has probability at most $k/(S+1)$. (ii) A miss requires either $T_{S+1}>T_{(k)}$ or a score above $T_{S+1}$. By Proposition 1 applied within season $S+1$, a score of $Z$ exceeds $T_{S+1}$ with probability at most $\alpha$; a union bound gives the claim. $\square$

*Remark 3.* Coverage conditional on the event in (i) is not claimed: the event selects seasons with small $T_{S+1}$. Any statistic $T'_s\ge T_s$ computed alike for every season keeps (i); the plain per-season quantile used as a sensitivity analysis satisfies (i) but not the step in (ii). The implementation departs from the conditions in two ways: the constants are fitted on the $S$ past seasons only, and past-season residuals come from season-held-out models trained on $S-1$ seasons whereas the new season is predicted by the model trained on all $S$, so the score function is not exactly common. In simulations with exchangeable seasons the frequency of the event in (i) was within Monte-Carlo error of the bound (unit tests of the code).

*Scope of the statements.* Proposition 1 is the hierarchical conformal guarantee of Lee et al. [@lee2023] written for a score that depends on a random reference set, with three nested levels and unequal group sizes; Proposition 2 is a statement of the probably-approximately-correct type [@park2022] at the level of the lot. Both require the predictor and the constants to be fixed independently of the calibration lots and the new lot to be exchangeable with past lots. Section 2.5 lists how the implementation departs from these conditions, and the experiments measure the consequences.

# Appendix B. Supplementary material

Supplementary Notes S1–S8 (robustness, computation, error analysis, deviations, ablation and generalisation, prototype, full decision analysis, development history) and supplementary tables S1–S24 accompany this article; the pre-specified protocol files are available on request with the code.

# References

::: {#refs}
:::
