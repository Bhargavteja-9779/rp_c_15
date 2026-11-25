---
title: "Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons"
---

**P N Bhargav Teja^a^, Ragavan K^a,\*^**

^a^ [Department, Institution, City, Postal code, Country]

\* Corresponding author: Ragavan K, [e-mail address], [postal address]

# Abstract

A handheld near-infrared (NIR) prediction of mango dry matter content (DMC) supports a harvest decision only if its error is known for the lot being picked, yet error bars are calibrated on past seasons. We predicted each season of a public mango data set (199 harvest lots, seven seasons) from earlier seasons. Six standard error bars at a nominal 90 % covered 77–84 % of reference values on 137 later-season lots. A few-shot conformal calibration (LotCP-S) tests *m* fruit per lot destructively, corrects the lot bias and scale, and sets the half-width by replaying this procedure on past lots. With five to ten reference fruit it raised coverage over standard split conformal prediction in all five target seasons, to 0.919 pooled, but 0.893 without the over-covered first target season. The same correction without the replay covered 1–4 points less. A lot-level variant kept 92 % of lot-draws at 90 % coverage overall but met that target in only 2 of five seasons. In an exploratory harvest simulation under assumed costs, a calibrated lower bound cost 5.0 units per 100 fruit less than point decisions; reference fruit added no further saving. Conclusions held with the published PLS recipe. Shifts between seasons, not the number of reference fruit, limit what can be guaranteed, and a prospective orchard trial is needed before practical use.

**Keywords:** near-infrared spectroscopy; harvest decision; fruit maturity; dry matter; conformal prediction; uncertainty quantification; calibration maintenance

# Highlights

- Standard NIR error bars under-covered later-season mango lots in every season.
- Five to ten reference fruit per lot restored coverage on average, not every season.
- Replaying the few-shot correction on past lots protected coverage at small *m*.
- Calibrated lower bounds, not reference fruit, drove the assumed-cost savings.
- Lot-level assurance held over all lots but in only two of five seasons.


# 1. Introduction

Handheld near-infrared (NIR) spectrometers are a routine tool for deciding when to harvest fruit. In mango, dry matter content (DMC) at harvest is the accepted index of eating quality: fruit picked below a cultivar-specific DMC does not ripen to acceptable quality, so growers scan fruit on the tree and compare the predicted DMC with a specification before a block is picked [@walshsubedi2016; @anderson2017; @walsh2020review]. A reading of 15.2 % against a 15 % specification supports a harvest only if its error is known to be small for the lot in hand. The calibration behind the reading, however, was built on earlier seasons and is applied to a new season, a new block and often a different instrument unit. Work on fruit NIR spectroscopy has shown repeatedly that accuracy estimated inside the calibration set overstates accuracy on a later, independent population [@nicolai2007; @walsh2020review]. For mango DMC this was documented on a multi-season data set, where the loss depended on season, cultivar and fruit temperature [@anderson2020; @anderson2021; @sun2020]. Current practice still quotes one root-mean-square error and, implicitly, the same band around every prediction.

Conformal prediction turns any point predictor into intervals with a finite-sample coverage guarantee [@vovk2022; @lei2018; @angelopoulos2023] and has begun to be used for spectroscopic quantification [@jovic2025; @sun2026]. Its guarantee rests on exchangeability between calibration and test data, which a new harvest season breaks. Two features of the orchard setting offer a partial way out. First, the data are nested: scans within fruit, fruit within harvest lots (one orchard block on one date), lots within seasons. A multi-season calibration set therefore contains many past lots in which lot-to-lot variation of the error can be observed. Second, checking a calibration against a few destructively measured fruit of the new population is already part of calibration maintenance [@fearn2001; @feudale2002]. What is missing is evidence on how far error bars fail lot by lot across real seasons, a procedure that turns a few reference fruit into an error bar with a stated coverage, and an honest account of what such error bars change in a harvest decision.

This paper evaluates a risk-aware harvest workflow built on these two features (Fig. 1). Fruit of a lot are scanned, *m* of them are tested destructively, a few-shot conformal calibration corrects the lot bias and scale, and each fruit receives a lower bound that is compared with the specification at a confidence level set by the cost ratio of the two possible errors.

![Fig. 1. Risk-aware harvest workflow. Before the season, past lots are used to calibrate the few-shot correction and to plan the number of reference fruit. In the orchard, fruit of a new lot are scanned, m of them are tested destructively, and each fruit receives a calibrated lower bound that is compared with the dry-matter specification.](figures/fig1_workflow.png){width=6.5in}

## 1.1 Related work

*Robust fruit calibrations.* Robustness across seasons, regions, cultivars and temperatures has been pursued with larger and more diverse calibration sets [@anderson2020], local and nonlinear models [@anderson2021], temperature-robust modelling [@sun2020], convolutional networks [@cui2018; @mishra2021; @walsh2024; @passos2023], semi-supervised learning [@mishra2023] and new cross-cultivar models [@ma2026]. Calibration transfer, standardisation and model updating address instrument and population differences [@fearn2001; @feudale2002; @mishra2021transfer]; spiking a library with local samples is the corresponding practice in soil spectroscopy [@guerrero2010; @guerrero2014]. This work targets the point prediction.

*Uncertainty for spectroscopic models.* Methods for PLS prediction intervals in NIR spectroscopy have been compared within one population [@bouckaert2011], and uncertainty calibration for latent-variable regression has been revisited recently [@duma2025]. Quantile regression forests [@meinshausen2006], deep ensembles [@lakshminarayanan2017] and Monte-Carlo dropout [@gal2016] are model-based alternatives; Bayesian approximations have been applied to mango DMC networks [@metz2025]. Wadoux and Ramirez-Lopez modelled prediction uncertainty in absorption spectroscopy with quantile regression forests [@wadoux2025]. Conformal prediction has been applied to mid-infrared adulteration data [@jovic2025] and NIR quantification of botanicals [@sun2026]. None of these studies audits coverage lot by lot on later seasons. The closest work measures the loss of split-conformal coverage under instrument transfer and the labelled target samples needed to restore it [@kayaoglu2026]. Our setting differs in the shift (seasons and lots rather than paired instruments) and in using past lots to calibrate the few-shot correction before the new lot is seen.

*Conformal prediction under shift and for groups.* Weighted conformal prediction handles covariate shift with a known or estimated likelihood ratio [@tibshirani2019] but not a change in the residual distribution, which is what a lot bias is. Adaptive conformal inference tracks a labelled stream [@gibbs2021], non-exchangeable conformal prediction down-weights less relevant points [@barber2023], and cross-conformal methods reuse training data [@vovk2015; @barber2021]. For grouped data, Dunn et al. [@dunn2023] and Lee et al. [@lee2023] replace exchangeability of observations by exchangeability of groups. Lee et al. prove marginal coverage for a group-balanced quantile and note that a score centred on a few observed outcomes of the test group can be used; Fisch et al. [@fisch2021] and Park et al. [@park2022] calibrate few-shot predictors across tasks, and recent work meta-learns few-shot conformal calibration [@park2024metaxb], recalibrates at a new site from a few local labels [@nasir2026], audits coverage under shift with a label budget [@moussa2026], shows that recalibration often fails to transfer [@neyigapula2026], recalibrates conformal predictors at test time from unlabelled examples [@yilmaz2022] or handles shift for spectral classification [@khairbek2026]. The coverage theory used here is that of Lee et al.; our contribution lies in the calibration procedure for this maintenance problem and in measuring its limits on real seasons.

## 1.2 Contributions

1. **A lot-by-lot coverage audit across harvest seasons.** Six families of error bars, two PLS recipes and two machine-learning predictors are evaluated on 137 later-season lots under forward chaining, with season-level as well as lot-level inference.
2. **A few-shot calibration and what each part buys.** LotCP-S corrects a lot's bias from *m* reference fruit, scales the score by a lot scale that also uses the label-free variance of repeated scans, and obtains the half-width by replaying the *m*-shot procedure on past lots with season-held-out residuals. Matched baselines isolate the replay step: it protects coverage at small *m* and does not make intervals narrower.
3. **A lot-level variant and a planner, with their limits.** LotCP-A calibrates on lot-wise quantiles so that the stated share of fruit is covered within the lot for nine lots in ten under exchangeable lots; a planner forecasts the width for each *m* from past lots. We report where both fall short under season shift.
4. **An exploratory decision analysis.** Fruit- and lot-level harvest decisions are simulated with season-cluster confidence intervals at an operating point fixed in advance, under explicitly assumed costs. The analysis shows that the saving comes from using a calibrated bound at all, not from the reference fruit.

The evaluation is a retrospective simulation on public data. It shows what the workflow would have done, not what it has done in an orchard.


# 2. Method

## 2.1 Setting and a model of the failure

A *lot* $k$ is the fruit harvested from one orchard block on one date. It contains $n_k$ reference *samples* $i$ (a piece of fruit tissue with one oven-dried DMC value $y_{ki}$), and sample $i$ has $J_{ki}\ge1$ *scans* $x_{kij}$. Lots are nested in seasons. A point predictor $f$ gives residuals $r_{kij}=y_{ki}-f(x_{kij})$. For a new lot the user scans the fruit and measures $m\ge0$ randomly chosen samples destructively; for every other scan an interval $C(x)$ with $\mathbb{P}\{y\in C(x)\}\ge1-\alpha$ is wanted. Split conformal prediction [@lei2018] returns $f(x)\pm q$, with $q$ the $\lceil(n+1)(1-\alpha)\rceil/n$ empirical quantile of held-out absolute residuals, and is valid when test and calibration residuals are exchangeable. We describe a residual by

$$r_{kij}=b_k+u_{ki}+e_{kij},\qquad b_k\sim(\mu,\tau^2),\quad u_{ki}\sim(0,\sigma_k^2),\quad e_{kij}\sim(0,\varepsilon_k^2), \qquad\text{(1)}$$

with a lot bias $b_k$, a sample effect and scan-to-scan variation. Eq. (1) motivates the estimators; coverage does not depend on it. If calibration residuals are held out at random, each calibration scan has lot-mates in the training set, the predictor has partly absorbed $b_k$, and the residuals are too small. Holding out lots exposes the between-lot variance of the training seasons; holding out seasons also exposes the part of $b_k$ shared by a season.

## 2.2 Season-held-out residuals and bias correction

For each source season $s$ the predictor is refitted without $s$ and predicts the scans of $s$, giving season-held-out residuals $\tilde r_{kij}$ for every source scan; the deployed predictor uses all source seasons. This is cross-conformal calibration [@vovk2015] with seasons as folds. From these residuals the one-way random-effects moments $\hat\mu$, $\hat\sigma^2$ (between samples within lots) and $\hat\tau^2$ (between lots) are estimated by the method of moments. For a new lot with reference set $A$, $|A|=m$, the bias is the mean reference residual,

$$\hat b=\bar r_A\quad(m\ge1),\qquad \hat b=\hat\mu\quad(m=0). \qquad\text{(2)}$$

Empirical-Bayes shrinkage of $\bar r_A$ towards $\hat\mu$ was part of the pre-specified design; it was immaterial on mango and harmful under a large campaign shift on soil spectra, and it is reported only as an ablation (Supplementary Note S5).

## 2.3 Lot scale (LotCP-S)

Lots differ in residual spread as well as bias. LotCP-S divides the score by

$$\hat s^2=\hat u^2+\hat e^2,\qquad \hat u^2=\frac{\nu_0\hat\sigma^2+(m-1)s_A^2}{\nu_0+m-1},\qquad \hat e^2=\frac{\sum_i\sum_j\big(f(x_{ij})-\bar f_i\big)^2}{\sum_i(J_i-1)}, \qquad\text{(3)}$$

where $s_A^2$ is the variance of the $m$ reference residual means, shrunk towards $\hat\sigma^2$ with pseudo-count $\nu_0\in\{5,10,20,40\}$ (chosen as the value giving the narrowest calibrated source intervals), and $\hat e^2$ is the pooled within-sample variance of the *predictions* of repeated scans of the new lot. $\hat e^2$ needs no reference value. When a lot has no repeated scans it is replaced by its mean over the source lots. LotCP without the suffix uses $\hat s\equiv1$.

## 2.4 Replaying the m-shot procedure on past lots

The half-width must reflect that $\hat b$ and $\hat s$ come from only $m$ samples. We obtain it by replaying deployment on the past. For each source lot $k$ with at least $m+10$ samples and each episode $e=1,\dots,E$, a reference set $A_{ke}$ of $m$ samples is drawn, $\hat b_{ke}$ and $\hat s_{ke}$ are computed from it by Eqs. (2)–(3), and the remaining scans give scores

$$S_{keij}=|\tilde r_{kij}-\hat b_{ke}|/\hat s_{ke},\qquad i\notin A_{ke}. \qquad\text{(4)}$$

The multiplier $\hat q_m$ is the $(1-\alpha)$ quantile of the lot-balanced score distribution

$$\hat q_m=Q_{1-\alpha}\Big(\sum_{k=1}^{K_m}\frac{1}{K_m+1}\sum_{e=1}^{E}\frac1E\sum_{i\notin A_{ke}}\frac{1}{n_k-m}\sum_{j}\frac{1}{J_{ki}}\delta_{S_{keij}}+\frac{1}{K_m+1}\delta_{+\infty}\Big), \qquad\text{(5)}$$

in which every lot carries equal weight, every sample equal weight within its lot and every scan equal weight within its sample. The interval for a scan of the new lot is $C(x)=f(x)+\hat b\pm\hat q_m\hat s$. For $m=0$ and $\hat s\equiv1$, Eq. (5) is the hierarchical conformal quantile of Lee et al. [@lee2023] on season-held-out residuals; for $m\ge1$ it is their mean-centred few-shot score. What the replay changes, relative to a plug-in alternative that standardises each past lot by its own full-information bias and scale, is that the estimation error of $\hat b$ and $\hat s$ at the deployed $m$ enters the quantile. Section 4.3 measures what this buys.

## 2.5 What is guaranteed

If the predictor and the constants are fixed, the calibration lots and the new lot are exchangeable, and samples are exchangeable within lots, the score of a random non-reference scan of the new lot, computed with a random reference set, is exchangeable with the calibration scores, and $\mathbb{P}\{y\in C(x)\}\ge1-\alpha$ for every $m$, with the probability taken over lots, reference draws and scans (Appendix A, Proposition 1, which covers random reference sets, three levels and unequal lot sizes). In our use these conditions hold only approximately. Calibration residuals come from season-held-out predictors; the constants are estimated from the calibration lots; lots of a new season are not exchangeable with past lots when the season differs systematically; and the guarantee is marginal over lots, not conditional on the lot [@barber2021limits]. The third gap is the one that matters, and Section 4 measures it season by season.

## 2.6 Lot-level assurance (LotCP-A)

A grower harvests one lot at a time, so a statement about the lot is more useful than one averaged over lots. For a lot $k$ and draw $e$ let $Q_{ke}$ be the weighted $(1-\alpha)$ quantile of the scores of Eq. (4) over the non-reference scans of that lot. A multiplier $q$ covers at least $1-\alpha$ of those scans exactly when $q\ge Q_{ke}$. LotCP-A therefore takes

$$\hat q^{\,A}_m=Q_{1-\delta}\Big(\sum_{k=1}^{K_m}\frac{1}{K_m+1}\sum_{e=1}^{E}\frac1E\delta_{Q_{ke}}+\frac{1}{K_m+1}\delta_{+\infty}\Big). \qquad\text{(6)}$$

Under exchangeable lots, the realised coverage within the new lot is at least $1-\alpha$ with probability at least $1-\delta$ (Appendix A, Proposition 2), a statement of the probably-approximately-correct type [@park2022]. We use $1-\alpha=0.90$ and $\delta=0.10$. LotCP-A and LotCP-S at a smaller $\alpha$ lie on the same family of intervals. LotCP-A does not buy assurance more cheaply. It chooses, from past lots and without target labels, the level that delivers the requested assurance.

## 2.7 Planning the number of reference fruit

The replay yields, for every $m$ and from past lots alone, the multiplier and the mean lot scale $\bar s_m$ over episodes, and hence a planned width $2\hat q_m\bar s_m$. The curve of planned width against $m$ can be drawn before the season and turns the choice of $m$ into an explicit trade between laboratory effort and precision. Calibration costs one extra model fit per source season, done offline; deployment computes two means and one variance per lot.

## 2.8 From a bound to a harvest decision

Let $t$ be the minimum DMC a fruit must reach, $c_I$ the cost of accepting an immature fruit and $c_D$ the cost of withholding a mature one. If the probability that a fruit is below $t$ were known, expected cost would be minimised by accepting it when that probability is at most $\alpha^\ast=c_D/(c_I+c_D)$, the familiar newsvendor or Bayes threshold. A lower bound $L_{\alpha}(x)=f(x)+\hat b-\hat q^-_m\hat s$, with $\hat q^-_m$ calibrated as in Eq. (5) on the signed score $(\hat b-r)/\hat s$, gives the rule *harvest if* $L_{\alpha^\ast}(x)\ge t$, *otherwise wait or re-test*. Because the guarantee is marginal, not conditional on the spectrum, this rule is a calibrated approximation to the cost-optimal rule. A lot is harvested when at least a share $p$ of its scanned fruit is accepted, and it is called ready when at least a share $p$ of its fruit truly meets $t$ ($p=0.8$).


# 3. Experimental setup

## 3.1 Data

We use the public "Mango DMC and NIR spectra" data set, version 6 [@mangodata] (CC BY 4.0), which extends the data of Anderson et al. [@anderson2020; @anderson2021] and Walsh et al. [@walsh2024]. It contains 85,401 spectra of intact fruit from handheld spectrometers in interactance geometry, each paired with the oven-dry DMC of the tissue under the scanned position, and identifies the season (7 seasons, 2015–2021), region, cultivar (10), instrument unit (31), reference sample (10,560) and population (199). A population is the fruit of one orchard block and harvest date; we call it a lot. Every sample was scanned repeatedly (median 6 scans; several instrument units and, for a subset, three fruit temperatures). We use 684–990 nm at 3 nm steps [@anderson2020] and retain all spectra (Table 1).

| Season | Spectra | Samples | Lots | Cultivars | Instrument units | DMC mean (%) | DMC SD (%) | Median samples per lot |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2015 | 15200 | 1152 | 25 | 4 | 8 | 16.46 | 2.66 | 40 |
| 2016 | 15310 | 1697 | 37 | 5 | 17 | 15.21 | 1.91 | 40 |
| 2017 | 27312 | 2322 | 56 | 9 | 16 | 15.80 | 2.39 | 40 |
| 2018 | 16133 | 2894 | 38 | 8 | 23 | 16.53 | 2.51 | 60 |
| 2019 | 5604 | 860 | 14 | 6 | 18 | 15.84 | 2.44 | 40 |
| 2020 | 4452 | 1073 | 18 | 8 | 15 | 14.89 | 2.62 | 40 |
| 2021 | 1390 | 562 | 11 | 5 | 11 | 14.99 | 2.77 | 40 |
| All | 85401 | 10560 | 199 | 10 | 31 | 15.89 | 2.47 | 40 |

Table: Table 1. The data set by harvest season.


## 3.2 Protocols and leakage control

For each target season $T\in\{2017,\dots,2021\}$ the source data are all earlier seasons (forward chaining). Nothing from season $T$ enters training, preprocessing, model selection or calibration except the $m$ reference samples of the lot under test. This gives 137 target lots with at least 20 samples; 2017, with two source seasons, contributes 56 of them. All folds are grouped by sample, lot or season, so repeated scans of a sample never straddle a fold; reference samples are drawn at sample level and all their scans leave the evaluation set; pre-treatments are row-wise. Leave-one-season-out, two-season, region and cultivar shifts are robustness checks (Supplementary Note S5).

## 3.3 Point predictors

*SNV PLS*, developed for this study: standard normal variate [@barnes1989], Savitzky–Golay second derivative (17 points, second order) [@savitzky1964] and PLS [@wold2001] with 8–20 latent variables chosen by leave-one-season-out cross-validation in the source. *Published PLS*: the recipe of the data providers (mean-centred Savitzky–Golay second derivative without SNV, 6–30 latent variables), which reproduced the published accuracy (Section 4.1) and is reported alongside SNV PLS in every main table. LightGBM [@ke2017] and a compact 1D-CNN [@cui2018; @walsh2024] with three fixed seeds are reported in the supplement.

## 3.4 Interval methods

*Without reference samples* ($m=0$): Gaussian band $\pm z_{1-\alpha/2}\,$RMSECV; split conformal prediction with residuals held out by sample, lot or season; weighted conformal prediction for covariate shift [@tibshirani2019]; conformalised quantile regression [@romano2019] with sample or season folds; quantile regression forest [@meinshausen2006]; deep ensemble [@lakshminarayanan2017]; Monte-Carlo dropout [@gal2016].

*With $m$ reference samples*: (a) bias correction + source CP, the mean reference residual subtracted and the sample-fold split-conformal half-width kept (current practice made conformal); (b) **bias correction + lot scale without replay**, the same bias and lot scale as LotCP-S, but with the half-width taken from past lots standardised by their own full-information bias and scale, so that only the replay of Eq. (5) differs from LotCP-S; (b′) as (b) with the replicate-scan scale only; (c) target-only CP, centred, split conformal on the leave-one-out-centred reference residuals alone, which is valid within the lot but needs $m\ge9$; (d) LotCP-S; (e) LotCP-A. Baselines (b) and (b′) were added in response to review. Slope/bias correction, pooled recalibration, adaptive conformal inference [@gibbs2021] and spiking are in the supplement.

## 3.5 Evaluation and statistics

For every lot and $m\in\{0,3,5,10,20,30\}$, 100 reference sets are drawn and the scans of the other samples are evaluated; a lot enters at a given $m$ only if it has at least $m+10$ samples. Within a lot, samples have equal weight and scans equal weight within their sample. We report lot-macro *coverage*, the share of lot-draws whose coverage reaches 0.90, mean *width*, and the Winkler *interval score* [@winkler1972; @gneiting2007]. LotCP uses $E=30$ episodes per lot.

The season is the top-level cluster and there are five target seasons. Every headline figure is therefore reported pooled over lots, as the mean of the season values and without 2017, the season with two source seasons. Comparisons use a two-stage season-cluster bootstrap (seasons resampled, then lots within each resampled season; 2,000 resamples) and the number of seasons in which the difference favours a method. An exact sign test over five seasons cannot reach $p<0.05$, so no season-level p-value is claimed; mixed models with a season random intercept were fitted but are degenerate with four or five groups and are not used. Lot-level Wilcoxon tests with Holm correction, the original analysis, are in the supplement.

## 3.6 Confirmation data

Before opening a further data set we froze LotCP-S and LotCP-A and committed four endpoints and a success rule (experiments/plan_v2.yaml): the interval score of LotCP-S against bias correction + source CP at $m=5$ and 10 (P1, P2), and the share of lot-draws at ≥ 0.90 coverage for LotCP-A against the better of two baselines at $m=10$ and 20 (P3, P4), with five seeds fixed in advance. The data set was the NeoSpectra handheld NIR soil library (Zenodo 10.5281/zenodo.13122321; nine handheld units; organic carbon as log(1 + %); lots are one-degree cells; 20 evaluable lots). Its soil layers belong to the KSSL catalogue, but none of them (0 of 2,106) was among the 19,807 KSSL layers used in our development analyses of soil vis–NIR spectra (Supplementary Note S5). Fresh reference draws on the mango lots were run under the same plan but are not an independent test.

## 3.7 Harvest-decision simulation (exploratory)

For each target lot, each $m\in\{0,3,5,10,20\}$ and twenty reference draws, every non-reference fruit is classified against a specification of 15 % DMC (14 and 16 % in the supplement) by: the point prediction; the bias-corrected point prediction; a split-conformal lower bound from sample-fold residuals ($m=0$); bias correction plus the same source margin; the one-sided LotCP-S bound; and the one-sided LotCP-A bound. No cost data accompany the data set, so costs are *assumed* and expressed in units of the value of one marketable fruit: $c_I=1$, $c_D=1/9$ (so $\alpha^\ast=0.10$), a reference test $c_R=1.5$, and lots of 1000 fruit. The operating point, $\alpha=0.10$, $p=0.8$ and the comparison against the cheapest rule without reference fruit were fixed before the confidence intervals were computed. The level $\alpha$ is also chosen by leave-one-season-out cost minimisation to check the cost-derived level without hindsight. These are scenarios for comparing rules, not estimates of orchard losses.

## 3.8 What was pre-specified, and the role of AI tools

The protocol (hypotheses, splits, methods, metrics) was committed to an internal git repository before any model was trained; it was not deposited with a public registry, so its timing can be verified only from the repository history, which is available on request. The lot scale of LotCP-S was added after inspecting one predictor on 2018; shrinkage was removed after the soil analysis; LotCP-A, the planner, the decision simulation, the published-PLS analysis and the matched baselines were added after the main results. All of these are exploratory. Only P1–P4 of Section 3.6 were confirmatory, and of these only the NeoSpectra arm is independent. Supplementary Note S4 lists every deviation with its date and reason, and Supplementary Note S8 tells how the method changed.

The study was carried out with extensive use of an AI assistant (Claude, Anthropic). It searched and screened the literature, wrote and ran the analysis code, proposed and ran experiments, drafted the text and acted as simulated reviewers. The authors set the aims and constraints of the study and take responsibility for its content. Cited references were checked against Crossref, Semantic Scholar or arXiv records during the study, and every number in the text and tables is filled in by a script from the result files and checked by an automated audit for numbers typed by hand.


# 4. Results

## 4.1 Point accuracy and the structure of the error

On the data providers' published split (three seasons for training, n = 10243; the fourth season as test set, n = 1448), the published PLS recipe reached an RMSEP of 1.045 % DMC, against 1.01 % reported by Anderson et al. [@anderson2020]. Our SNV PLS reached 1.392 %, and the CNN without augmentation 1.07–1.08 % against 0.77 % for a tuned and augmented CNN [@walsh2024]. Both PLS recipes are therefore reported below.

Under forward chaining, the error on the next season exceeded the sample-fold cross-validation estimate in every target season (Table 2). The standard deviation of the lot mean residual within a target season was 0.82–1.26 % DMC, of the same order as the within-lot error. Lots scatter around season-specific offsets (Fig. 2). The season-held-out variance components put the between-lot standard deviation at 0.91–1.51 % DMC and the within-lot, between-sample standard deviation at 0.80–1.18 % DMC.

| Target season | RMSECV sample folds | RMSECV lot folds | RMSECV season folds | RMSEP PLS | RMSEP LightGBM | RMSEP 1D-CNN | Bias PLS | SD of lot bias, PLS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2017 | 1.20 | 1.33 | 2.08 | 1.26 | 1.32 | 1.21 | -0.03 | 0.82 |
| 2018 | 1.20 | 1.24 | 1.38 | 1.68 | 1.61 | 1.25 | -0.27 | 1.26 |
| 2019 | 1.25 | 1.28 | 1.45 | 1.77 | 1.82 | 1.70 | 0.71 | 1.18 |
| 2020 | 1.25 | 1.30 | 1.47 | 1.58 | 1.44 | 1.35 | -0.39 | 1.22 |
| 2021 | 1.27 | 1.32 | 1.48 | 1.60 | 1.73 | 1.52 | -0.69 | 1.21 |

Table: Table 2. Point-prediction error (% DMC) under forward chaining. RMSECV: cross-validation inside the source seasons with PLS under three fold units. RMSEP: error on the target season (LightGBM and CNN: mean of three seeds). The last column is the standard deviation of the lot mean residuals in the target season.


![Fig. 2. Why calibration on held-out samples fails (SNV PLS, forward chaining). (a) Residuals of sample-fold cross-validation in the source seasons and residuals on the following season. (b) Mean residual of each target lot; the bar marks the season mean.](figures/fig3_lot_bias.png){width=6.3in}

## 4.2 Error bars without reference fruit

Split conformal prediction with sample-grouped folds covered 0.823 of reference values on later-season lots at a nominal 0.90 (0.781 without 2017) and reached 0.90 in none of the five seasons (Table 3). The Gaussian band, the quantile forest and conformalised quantile regression with sample folds behaved alike (0.840, 0.841, 0.794). The deep ensemble and Monte-Carlo dropout gave the lowest coverage (0.766, 0.775), because their predictive variance describes the training seasons. With the published PLS recipe, sample-fold split conformal prediction covered 0.843.

Holding out whole seasons is the honest label-free option: pooled coverage became 0.900, at 37 % more width. The pooled figure, however, is carried by 2017. Coverage by season ranged over 0.82–0.99, the season mean was 0.877, and without 2017 it was 0.839. In 2017 only two source seasons were available, the season-held-out models were weak and the intervals were too wide. With four to six past seasons, the next one is not exchangeable with them to within a few coverage points. Weighting calibration points by the likelihood ratio of the unlabelled target spectra reached 0.909 coverage but returned unbounded intervals for 5 % of scans; the shift that matters is a bias in the residual, which reweighting spectra does not repair.

| Predictor | Method | m | Coverage, pooled | Season mean | Excl. 2017 | Seasons ≥ 0.90 | Lot-draws ≥ 0.90 (%) | Width | Interval score |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SNV PLS | Split CP (sample folds) | 0 | 0.823 | 0.806 | 0.781 | 0/5 | 47 | 3.83 | 6.81 |
| SNV PLS | Split CP (season folds) | 0 | 0.900 | 0.877 | 0.839 | 1/5 | 73 | 5.26 | 7.05 |
| SNV PLS | Bias corr. + source CP | 5 | 0.931 | 0.935 | 0.921 | 4/5 | 74 | 3.83 | 4.80 |
| SNV PLS | Bias corr. + source CP | 10 | 0.938 | 0.942 | 0.929 | 5/5 | 77 | 3.83 | 4.68 |
| SNV PLS | Bias corr. + lot scale, no replay | 5 | 0.899 | 0.886 | 0.865 | 1/5 | 60 | 3.35 | 4.61 |
| SNV PLS | Bias corr. + lot scale, no replay | 10 | 0.908 | 0.897 | 0.883 | 1/5 | 62 | 3.29 | 4.37 |
| SNV PLS | Target-only CP, centred | 10 | 0.956 | 0.950 | 0.949 | 5/5 | 87 | 4.63 | 5.12 |
| SNV PLS | Target-only CP, centred | 20 | 0.932 | 0.929 | 0.928 | 5/5 | 78 | 3.58 | 4.29 |
| SNV PLS | LotCP-S | 5 | 0.920 | 0.910 | 0.893 | 2/5 | 70 | 3.60 | 4.62 |
| SNV PLS | LotCP-S | 10 | 0.919 | 0.911 | 0.893 | 3/5 | 69 | 3.45 | 4.46 |
| SNV PLS | LotCP-A (δ = 0.10) | 5 | 0.964 | 0.960 | 0.949 | 5/5 | 91 | 4.61 | 5.11 |
| SNV PLS | LotCP-A (δ = 0.10) | 10 | 0.964 | 0.959 | 0.952 | 5/5 | 92 | 4.30 | 4.77 |
| Published PLS | Split CP (sample folds) | 0 | 0.843 | 0.817 | 0.792 | 1/5 | 50 | 3.42 | 5.66 |
| Published PLS | Split CP (season folds) | 0 | 0.903 | 0.876 | 0.844 | 1/5 | 72 | 4.41 | 5.85 |
| Published PLS | Bias corr. + source CP | 5 | 0.937 | 0.932 | 0.919 | 5/5 | 79 | 3.42 | 4.10 |
| Published PLS | Bias corr. + source CP | 10 | 0.944 | 0.940 | 0.928 | 5/5 | 82 | 3.42 | 4.02 |
| Published PLS | Bias corr. + lot scale, no replay | 5 | 0.888 | 0.876 | 0.866 | 1/5 | 53 | 2.78 | 3.84 |
| Published PLS | Bias corr. + lot scale, no replay | 10 | 0.900 | 0.892 | 0.886 | 1/5 | 57 | 2.77 | 3.67 |
| Published PLS | Target-only CP, centred | 10 | 0.961 | 0.955 | 0.954 | 5/5 | 90 | 4.02 | 4.36 |
| Published PLS | Target-only CP, centred | 20 | 0.932 | 0.930 | 0.928 | 5/5 | 78 | 3.13 | 3.69 |
| Published PLS | LotCP-S | 5 | 0.910 | 0.899 | 0.890 | 2/5 | 68 | 2.99 | 3.85 |
| Published PLS | LotCP-S | 10 | 0.912 | 0.903 | 0.894 | 2/5 | 67 | 2.90 | 3.72 |
| Published PLS | LotCP-A (δ = 0.10) | 5 | 0.955 | 0.949 | 0.945 | 5/5 | 90 | 3.60 | 4.04 |
| Published PLS | LotCP-A (δ = 0.10) | 10 | 0.953 | 0.949 | 0.946 | 5/5 | 91 | 3.44 | 3.87 |

Table: Table 3. Intervals on later-season lots (forward chaining, 137 target lots in five seasons, nominal 0.90). Coverage is the lot-macro coverage pooled over lots, the mean of the five season values, and the pooled value without 2017 (56 lots, two source seasons). Seasons ≥ 0.90: seasons whose lot-macro coverage reaches 0.90. Lot-draws ≥ 0.90: share of lot × reference-draw pairs with coverage ≥ 0.90. Width and interval score in % DMC (pooled). Target-only CP cannot give a bounded interval for m < 9.


## 4.3 Error bars with reference fruit

With five to ten reference fruit per lot, LotCP-S raised coverage over sample-fold split conformal prediction by 0.10–0.10 (season mean) in all five seasons, with a season-cluster confidence interval excluding zero, for both PLS recipes (Table 4, Fig. 3). Its pooled coverage at $m=10$ was 0.919, its season mean 0.911, and without 2017 0.893. By season, coverage was 0.957, 0.882, 0.902, 0.897 and 0.914 for 2017–2021. LotCP-S therefore removed most of the shortfall but stayed slightly below nominal in the seasons with an adequate source set, and its gain over season-fold split conformal prediction without reference fruit was not distinguishable at season level (Table 4). Excluding 2018, the season used to design the lot scale, gives 0.934.

| Comparison | Outcome | PLS | m | Season-mean difference | 95% season-cluster CI | Seasons favouring |
|---|---:|---:|---:|---:|---:|---:|
| LotCP-S vs split CP (sample folds, m = 0) | coverage | SNV | 5 | +0.104 | +0.061 to +0.152 | 5/5 |
| LotCP-S vs split CP (sample folds, m = 0) | coverage | SNV | 10 | +0.105 | +0.060 to +0.153 | 5/5 |
| LotCP-S vs split CP (sample folds, m = 0) | coverage | Pub. | 5 | +0.081 | +0.026 to +0.136 | 5/5 |
| LotCP-S vs split CP (sample folds, m = 0) | coverage | Pub. | 10 | +0.086 | +0.027 to +0.142 | 5/5 |
| LotCP-S vs split CP (season folds, m = 0) | coverage | SNV | 5 | +0.033 | -0.022 to +0.087 | 4/5 |
| LotCP-S vs split CP (season folds, m = 0) | coverage | SNV | 10 | +0.034 | -0.024 to +0.085 | 4/5 |
| LotCP-S vs split CP (season folds, m = 0) | coverage | Pub. | 5 | +0.023 | -0.041 to +0.082 | 3/5 |
| LotCP-S vs split CP (season folds, m = 0) | coverage | Pub. | 10 | +0.027 | -0.037 to +0.081 | 3/5 |
| LotCP-S vs bias corr. + source CP | interval score | SNV | 5 | +0.214 | -0.001 to +0.412 | 5/5 |
| LotCP-S vs bias corr. + source CP | interval score | SNV | 10 | +0.269 | +0.092 to +0.435 | 5/5 |
| LotCP-S vs bias corr. + source CP | interval score | Pub. | 5 | +0.218 | +0.093 to +0.341 | 4/5 |
| LotCP-S vs bias corr. + source CP | interval score | Pub. | 10 | +0.264 | +0.141 to +0.383 | 5/5 |
| LotCP-S vs bias corr. + source CP | coverage | SNV | 5 | -0.025 | -0.047 to +0.008 | 1/5 |
| LotCP-S vs bias corr. + source CP | coverage | SNV | 10 | -0.032 | -0.049 to -0.001 | 1/5 |
| LotCP-S vs bias corr. + source CP | coverage | Pub. | 5 | -0.033 | -0.045 to -0.015 | 0/5 |
| LotCP-S vs bias corr. + source CP | coverage | Pub. | 10 | -0.038 | -0.050 to -0.022 | 0/5 |
| LotCP-S vs same scale without replay | interval score | SNV | 5 | +0.004 | -0.074 to +0.083 | 3/5 |
| LotCP-S vs same scale without replay | interval score | SNV | 10 | -0.053 | -0.138 to +0.001 | 1/5 |
| LotCP-S vs same scale without replay | interval score | Pub. | 5 | +0.015 | -0.058 to +0.056 | 4/5 |
| LotCP-S vs same scale without replay | interval score | Pub. | 10 | -0.028 | -0.077 to +0.002 | 2/5 |
| LotCP-S vs same scale without replay | coverage | SNV | 5 | +0.024 | +0.013 to +0.030 | 5/5 |
| LotCP-S vs same scale without replay | coverage | SNV | 10 | +0.014 | +0.005 to +0.019 | 5/5 |
| LotCP-S vs same scale without replay | coverage | Pub. | 5 | +0.023 | +0.020 to +0.026 | 5/5 |
| LotCP-S vs same scale without replay | coverage | Pub. | 10 | +0.011 | +0.004 to +0.018 | 5/5 |
| LotCP-A vs LotCP-S | lot-draws ≥ 0.90 | SNV | 5 | +26.1 | +11.8 to +33.8 | 5/5 |
| LotCP-A vs LotCP-S | lot-draws ≥ 0.90 | SNV | 10 | +26.9 | +10.7 to +37.0 | 5/5 |
| LotCP-A vs LotCP-S | lot-draws ≥ 0.90 | Pub. | 5 | +26.8 | +12.9 to +34.3 | 5/5 |
| LotCP-A vs LotCP-S | lot-draws ≥ 0.90 | Pub. | 10 | +29.0 | +12.2 to +38.8 | 5/5 |

Table: Table 4. Season-level comparisons (exploratory except where Section 6.4 states otherwise). Differences are oriented so that positive values favour the first method (lower interval score, higher coverage or share). CI: two-stage bootstrap that resamples seasons and then lots within seasons (2,000 resamples). With five seasons an exact sign test cannot reach p < 0.05 (smallest two-sided p = 0.0625); all lot-level tests are in the supplementary tables.


![Fig. 3. Lot-macro coverage, mean width and interval score against the number of reference fruit per lot (SNV PLS, forward chaining, 137 target lots, nominal 0.90). Dashed lines: split conformal prediction without reference fruit.](figures/fig4_main.png){width=6.5in}

*What the replay buys.* The matched baseline (b) uses the same bias and lot scale as LotCP-S and differs only in how the multiplier is calibrated. It covered 0.899 at $m=5$ and 0.908 at $m=10$ (0.883 without 2017), 3.7, 2.4 and 1.4 points less than LotCP-S at $m=3$, 5 and 10, with confidence intervals excluding zero for both PLS recipes. Its interval score was equal or slightly lower (by 0.05 at $m=10$; season-cluster interval for the advantage of LotCP-S -0.14 to +0.00). Replaying the $m$-shot procedure on past lots thus prices the error of estimating the bias and scale from a few fruit. It protects coverage when $m$ is small. It does not make intervals narrower. The lot scale is what narrows them. Against the replicate-scan scale alone (b′), LotCP-S had a lower interval score (intervals excluding zero for $m\ge5$) and at least equal coverage.

*Current practice.* Bias correction with the sample-fold half-width over-covered (0.938 at $m=10$) because a remnant of the lot effect in sample-fold residuals offsets the ignored estimation error of the bias. Its half-width cannot shrink with $m$, and LotCP-S had a lower interval score at season level from $m=10$ with SNV PLS (+0.09 to +0.43) and from $m=3$ with the published recipe, at the price of lower coverage. In the pre-specified confirmation on independent soil data, the interval-score advantage over this baseline was not confirmed (Section 4.5). Target-only calibration on the reference fruit alone needs $m\ge9$, was conservative and 34 % wider than LotCP-S at $m=10$, and matched its interval score by $m=20$ (4.29 against 4.25). The other predictors, protocols, nominal levels, reference-value noise and the component ablation are in Supplementary Note S5. Without repeated scans per fruit, LotCP-S and bias correction did not differ significantly in interval score (supplementary table S6b).

## 4.4 Lot-level assurance

Near-nominal average coverage still leaves many lots below the nominal level: with LotCP-S at $m=10$ only 69 % of lot-draws reached 0.90 (Fig. 4). LotCP-A, asked for 0.90 coverage in nine lots of ten, brought this share to 92 % pooled at $m=10$, but 87.5 % without 2017. By season it was 98, 86, 86, 89 and 93 % for 2017–2021: the target was met in 2 of five seasons with SNV PLS and in 2 with the published recipe. The lot-level guarantee rests on exchangeable lots, and season shift breaks it in the same way as it breaks the marginal one. LotCP-A did raise the share relative to LotCP-S in all five seasons (Table 4), at 25 % more width at $m=10$.

The extra width buys no efficiency. Measured as the share of lots whose draw-averaged coverage reaches 0.90, LotCP-A at $m=10$ (96.4 %, width 4.30) is matched by LotCP-S run at $\alpha=0.05$ (94.9 %, width 4.29). LotCP-A is a way of choosing that level from past lots without target labels. It is not a cheaper route to assurance.

![Fig. 4. Lot-level assurance (SNV PLS, forward chaining). (a) Share of lot-draws in which at least 90 % of the fruit is covered; dotted lines mark the targets of LotCP-A for δ = 0.10 and δ = 0.20. (b) Mean interval width.](figures/fig12_assurance.png){width=6.3in}

## 4.5 Pre-specified confirmation

| Data set | Endpoint | Comparison | Outcome | m | Lots | Mean difference | 95% CI | Holm p | r | Criterion met |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Mango (re-draw; lots seen during development) | P1 | LotCP-S - bias corr. + source CP | interval score | 5 | 137 | -0.165 | -0.269 to -0.058 | <0.001 | -0.37 | yes (re-draw check) |
| Mango (re-draw; lots seen during development) | P2 | LotCP-S - bias corr. + source CP | interval score | 10 | 137 | -0.248 | -0.352 to -0.137 | <0.001 | -0.53 | yes (re-draw check) |
| Mango (re-draw; lots seen during development) | P3 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 10 | 137 | +0.037 | +0.010 to +0.064 | <0.001 | +0.40 | yes (re-draw check) |
| Mango (re-draw; lots seen during development) | P4 | LotCP-A - bias corr. + source CP | share of lots ≥ 0.90 | 20 | 129 | +0.121 | +0.072 to +0.175 | <0.001 | +0.44 | yes (re-draw check) |
| NeoSpectra soil (untouched) | P1 | LotCP-S - bias corr. + source CP | interval score | 5 | 20 | -0.049 | -0.086 to -0.013 | 0.066 | -0.54 | no |
| NeoSpectra soil (untouched) | P2 | LotCP-S - bias corr. + source CP | interval score | 10 | 20 | -0.028 | -0.079 to +0.023 | 0.294 | -0.28 | no |
| NeoSpectra soil (untouched) | P3 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 10 | 20 | +0.073 | +0.033 to +0.116 | 0.015 | +0.71 | yes |
| NeoSpectra soil (untouched) | P4 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 20 | 10 | +0.207 | +0.178 to +0.235 | 0.008 | +1.00 | uninformative |

Table: Table 5. Pre-registered confirmation of the frozen method (experiments/plan_v2.yaml) on five seeds fixed in advance (100–104), 20 reference draws per seed, lot and m. Unit of analysis: target lot; Wilcoxon signed-rank test, Holm correction over the four endpoints per data set; 95 % CI: bootstrap over lots; r: matched-pairs rank-biserial correlation. An endpoint is confirmed when Holm p < 0.05, the CI excludes 0 and |r| ≥ 0.2 in the expected direction. Negative interval-score differences and positive share differences favour the proposed method. The mango rows are fresh reference draws on lots examined during development and are not an independent confirmation. P3 and P4 compare coverage shares without a width constraint (Section 6.3); P4 had too few lots and is counted as uninformative.


On the independent NeoSpectra data (Table 5), the efficiency endpoints failed: the interval-score difference to bias correction + source CP at $m=5$ was -0.049 (95 % CI -0.086 to -0.013, Holm p 0.066) and at $m=10$ -0.028 (p = 0.294). The assurance endpoint P3 met its criterion: 95 % of lot-draws at ≥ 0.90 for LotCP-A against 88 % for target-only CP, at a width of 1.19 against 1.13. As Section 4.4 shows, a share endpoint without a width constraint favours the wider method, so P3 confirms that LotCP-A delivers its requested share on exchangeable lots, not that it does so efficiently. P4 is uninformative (10 lots). Split conformal prediction already covered 0.930 on these data: cells within one survey programme are close to exchangeable, so the confirmation could not test a seasonal shift. The mango rows are fresh draws on development lots and are not independent.

## 4.6 Harvest decisions (exploratory)

At the operating point fixed in advance, deciding on point predictions cost 8.7 units per 100 fruit under the assumed costs (SNV PLS; Table 6). Any calibrated lower bound cost about 5 units less: the split-conformal bound without reference fruit 3.69 [2.11, 5.16], The difference to point decisions had a confidence interval excluding zero and favoured the bound in all five seasons, for both PLS recipes. Reference fruit did not lower the cost further. The LotCP-S bound with $m=3$, 5 and 10 differed from the bound without reference fruit by -0.28, -0.12 and +0.53 units, all with intervals including zero, and bias correction with a source margin behaved alike. The bound accepted far fewer immature fruit than the point prediction (0.5 against 8.0 per 100 fruit at $m=5$) and withheld more mature fruit (21 against 6).

At lot level the point rule harvested 7.3 % of not-ready lots [0.0, 22.4] and delayed 20 % of ready lots. The bound without reference fruit harvested 3.7 % of not-ready lots and delayed 69 % of ready lots; with five reference fruit, LotCP-S harvested 0.2 % and delayed 59 %. The confidence intervals overlap: 82 not-ready and 55 ready lots in five seasons cannot resolve differences of this size. Choosing $\alpha$ by leave-one-season-out cost minimisation was not better than the cost-derived level $\alpha^\ast$ (LotCP-S, $m=10$: 2.70 against 2.47 units at $\alpha^\ast=0.10$, excluding the cost of reference tests, which does not depend on $\alpha$). Full trade-off curves are in Fig. 5 and Supplementary Note S7.

| PLS | Rule | m | Cost / 100 fruit [95% CI] | Δ vs split-CP bound [95% CI] | Premature lots (%) [CI] | Ready lots delayed (%) [CI] |
|---|---:|---:|---:|---:|---:|---:|
| SNV | Point prediction | 0 | 8.69 [6.75, 11.21] | +5.00 [+2.96, +8.24] | 7.3 [0.0, 22.4] | 20 [3, 32] |
| SNV | Split-CP lower bound | 0 | 3.69 [2.11, 5.16] | reference | 3.7 [0.0, 13.8] | 69 [53, 85] |
| SNV | Bias-corrected point | 5 | 5.95 [4.97, 7.24] | +2.25 [+0.90, +4.16] | 7.7 [2.5, 17.9] | 8 [1, 15] |
| SNV | Bias corr. + source margin | 5 | 3.62 [2.84, 4.12] | -0.07 [-1.14, +0.84] | 0.1 [0.0, 0.3] | 57 [37, 69] |
| SNV | LotCP-S lower bound | 3 | 3.41 [2.65, 3.86] | -0.28 [-1.50, +0.83] | 0.7 [0.0, 2.5] | 59 [39, 71] |
| SNV | LotCP-S lower bound | 5 | 3.57 [2.85, 4.02] | -0.12 [-1.36, +0.82] | 0.2 [0.0, 0.7] | 59 [38, 70] |
| SNV | LotCP-S lower bound | 10 | 4.22 [3.49, 4.65] | +0.53 [-0.67, +1.49] | 0.1 [0.0, 0.4] | 56 [36, 68] |
| SNV | LotCP-A lower bound | 5 | 3.99 [2.99, 4.47] | +0.30 [-0.87, +1.00] | 0.0 [0.0, 0.0] | 73 [56, 85] |
| SNV | Withhold all | 0 | 6.44 [4.26, 7.47] | +2.75 [+1.48, +3.63] | 0 | 100 |
| Pub. | Point prediction | 0 | 8.23 [6.35, 11.73] | +4.96 [+3.18, +8.96] | 7.3 [0.0, 20.0] | 18 [0, 29] |
| Pub. | Split-CP lower bound | 0 | 3.27 [2.47, 4.02] | reference | 0.0 [0.0, 0.0] | 60 [31, 73] |
| Pub. | Bias-corrected point | 5 | 5.79 [4.83, 7.28] | +2.52 [+1.63, +4.15] | 5.6 [1.4, 13.6] | 6 [0, 17] |
| Pub. | Bias corr. + source margin | 5 | 3.28 [2.63, 3.67] | +0.01 [-0.49, +0.36] | 0.0 [0.0, 0.0] | 50 [28, 63] |
| Pub. | LotCP-S lower bound | 3 | 2.95 [2.31, 3.32] | -0.33 [-0.81, +0.10] | 0.4 [0.0, 1.1] | 46 [29, 58] |
| Pub. | LotCP-S lower bound | 5 | 3.14 [2.52, 3.53] | -0.14 [-0.67, +0.27] | 0.0 [0.0, 0.0] | 46 [27, 59] |
| Pub. | LotCP-S lower bound | 10 | 3.79 [3.17, 4.15] | +0.52 [-0.03, +0.95] | 0.0 [0.0, 0.0] | 45 [28, 58] |
| Pub. | LotCP-A lower bound | 5 | 3.34 [2.63, 3.75] | +0.07 [-0.45, +0.42] | 0.0 [0.0, 0.0] | 58 [38, 70] |
| Pub. | Withhold all | 0 | 6.44 [4.15, 7.49] | +3.17 [+1.60, +4.08] | 0 | 100 |

Table: Table 6. Harvest decisions at the operating point fixed before this analysis (exploratory; specification 15 % DMC, bounds at α = 0.10, lot harvested when ≥ 80 % of its scanned fruit are accepted, ASSUMED costs c_I = 1, c_D = 1/9, c_R = 1.5 per reference fruit, lots of 1000 fruit; 137 target lots). Cost in units of the value of one marketable fruit, including reference tests. Δ: cost difference to the split-conformal lower bound, the cheapest rule without reference fruit. 95 % CIs: two-stage season-cluster bootstrap.


![Fig. 5. Trade-off between harvesting immature fruit and holding back mature fruit (SNV PLS, specification 15 % DMC, 137 later-season lots; exploratory). Each curve traces one rule as its level α varies from 0.02 to 0.5; crosses are rules without a level. (a) Fruit-level decision. (b) Lot-level decision: a lot is harvested when at least 80 % of its scanned fruit are accepted.](figures/fig14_harvest_frontier.png){width=6.5in}

## 4.7 Planning the number of reference fruit

The width planned from past lots matched the realised width with a median absolute relative difference of 7 % over all predictors, seasons and values of $m$ (Fig. 6). The error depended on the number of source seasons: LotCP-S widths were over-forecast by 17 % with two source seasons (2017) and within 8 % with three to six. Most of the reduction in width came from the first five reference fruit; beyond ten the curve was flat.

![Fig. 6. Reference-budget planning. (a) Width planned from past lots against the mean width realised on the following season; each point is one target season, predictor, number of reference fruit and variant. (b) Planned and realised curves for SNV PLS, averaged over target seasons.](figures/fig13_planning.png){width=6.3in}


# 5. Discussion

**What the audit shows.** An error bar calibrated inside the training seasons, whether by cross-validation, a conformal quantile on held-out samples or the predictive variance of a neural network, describes past lots. On later-season mango lots it was too narrow in every season we could test, by 6 to 13 coverage points at a nominal 90 %, and the shortfall was concentrated in a minority of badly covered lots. Holding out whole seasons is the honest repair without reference fruit, but with four to six past seasons it reached nominal coverage only in the season that happened to be over-covered. These findings agree in direction with the loss of coverage reported under instrument transfer [@kayaoglu2026] and with the long-standing observation that NIR accuracy degrades on new populations [@nicolai2007; @anderson2020]; the audit adds the lot-by-lot, season-by-season picture that a decision against a specification needs.

**What reference fruit and the calibration add.** A few reference fruit per lot did most of the work: once the lot bias was corrected, every method moved close to or above nominal coverage. The contribution of LotCP-S lies in two places. The lot scale, estimated partly from the label-free scatter of repeated scans, gave narrower intervals than bias correction with a fixed half-width, though this efficiency gain was not confirmed on independent soil data and vanished without repeated scans. The replay of the $m$-shot procedure on past lots priced the error of a few-fruit correction and kept coverage 1–4 points higher than the same correction without replay at three to ten reference fruit. Neither component removes the season effect: without the over-covered 2017 season, LotCP-S covered 0.893 and LotCP-A met its lot-level target in 2 of five seasons. A season-level shift that the past seasons do not span cannot be calibrated away from those seasons. The practical consequence is to report season-by-season coverage of the calibration itself and, when the lot-level statement matters, to choose a smaller $\alpha$ or LotCP-A with the expectation that the stated assurance is approximate.

**What changes in the decision.** In the exploratory simulation, the benefit came from replacing the point value by any calibrated lower bound, which cut the assumed cost by about 5 units per 100 fruit in every season and kept immature fruit out of the harvest. Reference fruit did not lower the expected cost further at the pre-stated operating point. Their value lies in making the bound mean what it says for the lot in hand, which matters when the level is set from costs, and in a lower rate of delayed ready lots that five seasons could not resolve statistically. The cost-derived level $\alpha^\ast$ was as good as a level chosen from other seasons, which supports the newsvendor reading of the rule.

**Practical procedure.** (1) Build the calibration with season-grouped cross-validation and keep the season-held-out residuals with lot and sample identifiers. (2) Before the season, read the planned width for each $m$ and state the cost ratio, which fixes $\alpha^\ast$. (3) In the orchard, scan the fruit of a lot with two or three scans per fruit, test five to ten randomly chosen fruit, and harvest a fruit or lot when the calibrated lower bound meets the specification. (4) After the season, add the lot to the calibration set and check the realised coverage.

# 6. Limitations

In order of importance:

1. *Retrospective only.* All results replay archived data. The workflow has not been used to decide a harvest, and the paper does not show that it reduces losses in an orchard. A prospective trial that records decisions and verifies them on harvested fruit is the necessary next step.
2. *Few seasons and one fruit data set.* Five target seasons are a small sample at the level that dominates the error, and the confidence intervals reflect this. We found no second public fruit NIR data set with lot and season structure; the soil libraries test the coverage audit and the calibration on another material but have no season level, and the independent soil data showed little shift to repair.
3. *Guarantees hold only approximately.* Coverage guarantees assume exchangeable lots. Under season shift the marginal coverage fell slightly below nominal and the lot-level assurance was missed in three of five seasons.
4. *Exploratory components.* The lot scale was designed after inspecting 2018, and LotCP-A, the planner, the decision simulation and the matched baselines were added after the main results. The protocol was committed internally, not publicly registered.
5. *Assumed costs and illustrative decision rules.* Costs are expressed in units of fruit value, the specification of 15 % DMC and the 80 % lot rule are illustrative, and maturity is not determined by DMC alone.
6. *Repeated scans richer than routine practice.* The data contain scans from several instrument units and temperatures per fruit; the efficiency gain of LotCP-S depended on them.
7. *Reference sampling.* Reference fruit are assumed to be drawn at random and measured as accurately as the calibration set.

# 7. Conclusion

Error bars for handheld NIR predictions of mango dry matter, calibrated inside the training seasons, did not keep their coverage on later-season lots. A few reference fruit per lot, with a few-shot conformal calibration that corrects bias and scale and replays the procedure on past lots, restored coverage on average and kept it at small numbers of reference fruit. Season-to-season shift still left coverage slightly below nominal in the seasons with an adequate source set, and the lot-level assurance held over all lots but not season by season. In an exploratory decision analysis, a calibrated lower bound rather than the point value was what lowered the assumed cost of harvest decisions. A prospective orchard trial is the step that remains.

# CRediT authorship contribution statement

**P N Bhargav Teja:** Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Visualization, Writing – original draft, Writing – review & editing. **Ragavan K:** Supervision.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Declaration of generative AI and AI-assisted technologies in the research and manuscript preparation process

During this work the authors used Claude (Anthropic) to search and screen the literature, write and run the analysis code, design and run experiments, draft and revise the text, and simulate peer review (Section 3.8). After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

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

*Scope of the statements.* Proposition 1 is the hierarchical conformal guarantee of Lee et al. [@lee2023] written for a score that depends on a random reference set, with three nested levels and unequal group sizes; Proposition 2 is a statement of the probably-approximately-correct type [@park2022] at the level of the lot. Both require the predictor and the constants to be fixed independently of the calibration lots and the new lot to be exchangeable with past lots. Section 2.5 lists how the implementation departs from these conditions, and the experiments measure the consequences.

# Appendix B. Supplementary material

Supplementary Notes S1–S8 (robustness, computation, error analysis, deviations, ablation and generalisation, prototype, full decision analysis, development history), supplementary tables S1–S24 and the pre-specified protocol accompany this article.

# References

::: {#refs}
:::
