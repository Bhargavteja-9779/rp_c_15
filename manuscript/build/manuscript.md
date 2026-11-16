---
title: "Lot-level valid error bars for near-infrared predictions across harvest seasons: few-shot conformal calibration with a per-lot assurance and a reference-sampling planner"
---

**[Author One]^a,\*^, [Author Two]^a^, [Author Three]^b^**

^a^ [Department, Institution, City, Country]

^b^ [Department, Institution, City, Country]

\* Corresponding author: [name], [e-mail address], [postal address]

# Abstract

Handheld near-infrared (NIR) spectrometers guide fruit harvest decisions, yet their calibrations are built on past seasons and carry no error bar that holds on a new one. On a mango data set (199 harvest lots, seven seasons) we train on earlier seasons and measure interval coverage for dry matter content on 137 later-season lots. At a nominal 90 %, split conformal prediction covers 82 %; Gaussian bands, quantile models, deep ensembles and Monte-Carlo dropout cover 77–84 %. Season-held-out calibration restores average coverage only with 37 % wider intervals. We introduce a few-shot conformal calibration with proven guarantees: bias and scale of a new lot are estimated from *m* reference samples and repeated scans, and the half-width is calibrated by replaying this procedure on past lots. With 3–30 reference samples the marginal variant (LotCP-S) covers 91–92 % (91–92 % across three predictors and two protocols) and has the best interval score for 3–20 samples. A second variant (LotCP-A) targets the stated coverage within the lot for nine lots in ten: 92 % of lots reach it with ten samples, against 69 % for LotCP-S, at 25 % more width. The replay also forecasts the width for each *m* before the season (median error 7 %). As a lower bound against a 15 % specification, the calibration cuts non-compliant fruit among those accepted from 13 % to 1 %. On two soil vis–NIR libraries the loss is larger (coverage 40–88 %), and five local samples restore 87–91 %. 

**Keywords:** near-infrared spectroscopy; conformal prediction; uncertainty quantification; distribution shift; fruit maturity; soil spectral library; calibration maintenance

# Highlights

- Conformal intervals for mango dry matter cover 82 %, not 90 %, on later seasons.
- On soil spectra across survey campaigns coverage falls to 40–63 %.
- Few-shot calibration with proofs restores coverage from three reference samples.
- A lot-level variant keeps nine lots in ten at the stated coverage.
- A planner forecasts interval width for each sampling effort before the season.


# 1. Introduction

Handheld near-infrared (NIR) spectrometers are now routine tools for deciding when to harvest fruit. In mango, dry matter content (DMC) at harvest is the accepted index of eating quality, and growers scan fruit on the tree and compare the predicted DMC with a cultivar-specific specification [@walshsubedi2016; @walsh2020review]. The calibration behind such a reading is built on previous seasons and is then applied to fruit of a new season, a new orchard block, and often a different instrument unit. Three decades of work on fruit NIR spectroscopy have shown that the accuracy measured by cross-validation inside the calibration set overstates the accuracy obtained on a later, independent population [@nicolai2007; @walsh2020review]. For mango DMC this was documented with a multi-season data set: models that looked excellent in cross-validation lost accuracy on the following season, and the loss depended on the season, the cultivar and the fruit temperature [@anderson2020; @anderson2021; @sun2020].

A point estimate of DMC is therefore not enough for a harvest decision. A reading of 15.2 % against a 15 % specification means something different if the error bar is ±0.8 % than if it is ±2 %. What the user needs is a prediction interval that contains the true DMC with a stated probability, on *this* lot of fruit, and that is no wider than necessary. Current practice reports a single root-mean-square error of cross-validation or of an external validation set and, implicitly, a Gaussian band around every prediction. Recent work has started to attach uncertainty estimates to spectroscopic predictions, with Bayesian approximations for neural networks [@metz2025] and with conformal prediction [@jovic2025; @sun2026].

Conformal prediction is attractive here because it turns any point predictor into intervals with a finite-sample coverage guarantee and no distributional assumption [@vovk2022; @lei2018; @angelopoulos2023]. The guarantee, however, rests on exchangeability between the calibration data and the test data. That is the assumption a new harvest season breaks. A concurrent study reports that split-conformal intervals lose coverage when an NIR calibration is moved to another instrument [@kayaoglu2026]. Whether, and how strongly, the same happens under the biological and operational shift between harvest seasons, and what a grower can do about it at acceptable cost, has not been examined.

The practical setting offers two resources that generic remedies for distribution shift do not use. First, the data have a nested structure: scans are nested in fruit samples, samples in harvest lots (an orchard block harvested on a given date), and lots in seasons. A multi-season calibration set contains many past lots, so the lot-to-lot variation of the model error can be observed directly. Second, bias adjustment from a few reference measurements is a standard step of calibration maintenance and transfer [@fearn2001; @feudale2002]: a small number of fruit from the new population are measured destructively and used to check or adjust the model. The open questions are how many reference fruit are needed, how they should be used, and what coverage the resulting intervals then have.

This paper addresses these questions with a large public mango NIR data set (85,401 spectra, 10,560 reference samples, 199 harvest lots, seven seasons, 31 instrument units) [@mangodata] and two public soil spectral libraries [@safanelli2025]. Its contributions fall into three groups.

*New evidence.*

1. **A lot-level audit of prediction intervals across harvest seasons, to our knowledge the first for fruit NIR.** Under a forward-chaining protocol (train on all seasons before *T*, test on the lots of season *T*) we measure the coverage of split-conformal, Gaussian, conformalised-quantile-regression, quantile-forest, deep-ensemble, Monte-Carlo-dropout and covariate-shift-weighted conformal intervals on later-season lots, for three point predictors, and show how the result depends on whether calibration residuals are held out by sample, by lot or by season.
2. **Replication on soil spectra.** The same audit on a European soil survey across two campaigns and on a United States library across survey projects shows that the loss of coverage is not a property of one fruit data set and is far larger across survey campaigns.

*New methods.*

3. **LotCP-S, a few-shot calibration priced on past lots.** The bias of a new lot is corrected from *m* reference samples; the conformity score is rescaled by a lot-specific scale that combines the reference residuals with the variance of repeated scans, a quantity that needs no reference value; and the half-width is obtained by replaying this *m*-shot procedure on every past lot with season-held-out residuals, so that it accounts for the estimation error at the given *m*. We state and prove its marginal coverage for random reference sets, three nested levels and lots of unequal size (Appendix A).
4. **LotCP-A, a lot-level assurance.** Because a harvest decision concerns one lot, a second variant calibrates on the lot-wise score quantiles of past lots, so that the stated share of fruit is covered *within* the lot for at least a stated fraction of lots, with a finite-sample guarantee (Appendix A). None of the compared methods has this property, including calibration on the reference samples alone.
5. **A reference-sampling planner.** The replay yields, before the season and from past lots only, the interval width to expect for each number of reference samples, which turns the choice of sampling effort into an explicit trade.

*New evaluation.*

6. **A protocol at the level at which decisions are taken.** The unit of analysis is the lot; outcomes are lot-wise coverage, the share of lots reaching the nominal level, interval width and a proper interval score as functions of the reference budget; comparisons are paired across lots; ablations, robustness analyses and failures are reported, including a pre-specified component (shrinkage of the bias estimate) that failed on external data and was removed.
7. **A harvest-decision analysis.** One-sided bounds are evaluated against a minimum dry-matter specification, in terms of immature fruit accepted and compliant fruit withheld.

The coverage guarantees build on hierarchical conformal prediction [@lee2023]; what is new is the calibration procedure for this problem, its lot-level variant, the planner, and the evidence on how far the guarantees carry across real seasons and survey campaigns. The guarantees require lots to be exchangeable, which seasons make doubtful, and a central aim of the experiments is to measure the consequences.

# 2. Related work

**Robust NIR calibrations for fruit.** Calibration robustness across seasons, growing regions, cultivars and temperatures has been pursued by enlarging and diversifying the calibration set [@anderson2020], by local and nonlinear models [@anderson2021], by temperature-robust modelling [@sun2020], by convolutional networks [@cui2018; @mishra2021; @walsh2024; @passos2023] and by semi-supervised modelling [@mishra2023]. Calibration transfer and standardisation address the related problem of instrument differences [@fearn2001; @feudale2002]. All of this work targets the point prediction and reports aggregate error statistics; none provides per-prediction intervals with stated coverage on a new season.

**Uncertainty quantification for spectroscopic models.** Model-based approaches include quantile regression forests [@meinshausen2006], deep ensembles [@lakshminarayanan2017] and Monte-Carlo dropout [@gal2016]; the latter family has been applied to mango DMC prediction with neural networks [@metz2025]. Conformal prediction has been applied to mid-infrared adulteration data, where normalised scores gave narrower intervals than absolute residuals [@jovic2025], and to NIR quantification of botanical adulterants, where aggregated and cross-validated variants were compared [@sun2026]. These studies do not address a shift between harvest seasons or lots. The closest work to ours is the concurrent study of Kayaoğlu and Erdem, available as a code and results archive, which measures the loss of split-conformal coverage under instrument transfer on four paired-instrument data sets and the number of labelled target samples needed to restore it [@kayaoglu2026]. Our study differs in the type of shift (harvest seasons and lots rather than paired instruments), in the data structure that it exploits (many past lots), and in proposing a calibration that uses the past lots to price the few-shot correction rather than recalibrating from the target labels alone.

**Conformal prediction under distribution shift.** Weighted conformal prediction restores validity under covariate shift when the likelihood ratio between test and calibration covariates is known or estimated [@tibshirani2019]; it cannot repair a change in the conditional distribution of the residual, which is what a lot-specific bias is. Adaptive conformal inference adjusts the miscoverage level online from a stream of labelled outcomes [@gibbs2021], and non-exchangeable conformal prediction down-weights calibration points that are less relevant [@barber2023]. Cross-conformal and jackknife+ methods reuse the training data for calibration [@vovk2015; @barber2021]. For grouped data, Dunn et al. [@dunn2023] and Lee et al. [@lee2023] replace exchangeability of observations by exchangeability of groups; Lee et al. prove marginal coverage for a group-balanced split-conformal quantile (HCP) and remark that, when a few outcomes of the test group are observed, a score centred on their mean can be used. Fisch et al. [@fisch2021] calibrate few-shot predictors across exchangeable auxiliary tasks. LotCP builds directly on these results. What it adds is specific to calibration maintenance: residuals that are held out by season so that past lots look like future lots, a score scale that uses the reference residuals and repeated scans, and a replay of the reference-sampling protocol that handles lots of unequal size.

# 3. Research gap and questions

What exists: (i) evidence that point accuracy of mango DMC calibrations degrades on a new season; (ii) uncertainty methods for spectroscopy evaluated within one population; (iii) concurrent evidence that conformal coverage degrades under instrument transfer; (iv) hierarchical conformal theory for grouped data. What is missing is an assessment of interval coverage at the level of the harvest lot across real seasons, a calibration procedure that uses the lot structure of multi-season calibration sets together with a few reference samples, and a quantified trade-off between the number of reference samples and the width of a valid interval. This matters because the lot is the unit on which a harvest decision is taken, and because reference sampling is the only label source a grower has.

The work is positioned as follows.

- *Robust fruit calibrations* [@anderson2020; @anderson2021; @mishra2023] improve the point prediction across seasons. This paper adds per-prediction intervals whose coverage is measured on later seasons, lot by lot.
- *Uncertainty for spectroscopic models* has been proposed with Bayesian approximations for mango networks [@metz2025] and with conformal prediction for food and botanical quantification [@jovic2025; @sun2026]. This paper audits such estimates lot by lot against a nominal level on later seasons and campaigns, and shows that those calibrated within the training population fail there.
- *Conformal prediction under instrument transfer* [@kayaoglu2026] measures the loss of coverage between paired instruments and the labelled samples needed to restore it by recalibration. This paper treats seasons, lots and campaigns, and uses past lots to calibrate the few-shot correction before the new lot is seen.
- *Hierarchical and few-shot conformal prediction* [@lee2023; @dunn2023; @fisch2021; @park2022] provides the theory for grouped data. This paper supplies a calibration procedure for calibration maintenance (bias and scale from reference samples and repeated scans, season-held-out residuals, replay of the reference protocol), a lot-level assurance, a sampling planner, and their empirical limits.
- *Bias adjustment and spiking* [@fearn2001; @feudale2002; @guerrero2010; @guerrero2014] are the maintenance practices in use. This paper gives them an interval with stated coverage and compares them directly.

We ask five questions. RQ1: how far does the coverage of standard intervals fall on later-season lots, and which hold-out unit for calibration residuals repairs it? RQ2: with *m* reference samples per lot, what coverage, width and interval score does LotCP achieve relative to strong alternatives? RQ3: which components of LotCP matter? RQ4: do the findings hold for other point predictors, nominal levels, protocols, noisy reference values, fewer past lots, and unseen regions or cultivars? RQ5: what does the method cost, and on which lots does it still fail?


# 4. Proposed method

## 4.1 Setting and notation

Data are nested. A *lot* $k$ is a set of fruit harvested from one orchard block on one date; it contains $n_k$ reference *samples* $i$ (a piece of fruit tissue with one oven-dried DMC value $y_{ki}$), and sample $i$ has $J_{ki}\ge 1$ *scans* with spectra $x_{kij}$. Lots are nested in seasons. A point predictor $f$ maps a spectrum to a DMC estimate, and $r_{kij}=y_{ki}-f(x_{kij})$ is the residual of a scan. For a new lot the user scans all fruit of interest and measures $m\ge 0$ randomly chosen reference samples destructively. For each remaining scan we want an interval $C(x)$ such that $\mathbb{P}\{y\in C(x)\}\ge 1-\alpha$. Fig. 1 gives an overview of the procedure developed below.

![Fig. 1. Overview of LotCP. Top: calibration uses source seasons only. Bottom: deployment on a new lot with m reference samples.](figures/fig1_workflow.png){width=6.3in}

Split conformal prediction [@lei2018] takes residuals of a held-out calibration set, computes the $\lceil (n+1)(1-\alpha)\rceil/n$ empirical quantile $q$ of their absolute values and returns $f(x)\pm q$. The guarantee requires the test residual to be exchangeable with the calibration residuals.

## 4.2 A model of why the guarantee fails

We describe the residual of a scan in lot $k$ by

$$r_{kij} = b_k + u_{ki} + e_{kij}, \qquad b_k \sim (\mu,\tau^2),\quad u_{ki}\sim(0,\sigma_k^2),\quad e_{kij}\sim(0,\varepsilon_k^2), \qquad\text{(1)}$$

where $b_k$ is a lot bias (the calibration is systematically high or low for this block, date, instrument mix and fruit condition), $u_{ki}$ a sample effect and $e_{kij}$ scan-to-scan variation. Eq. (1) is used only to motivate the estimators; coverage does not depend on it being true. If calibration residuals are held out at random, each calibration scan has lot-mates in the training set, the predictor has partly absorbed $b_k$, and the calibration residuals are too small. Holding out whole lots exposes $\tau^2$ as it is *within* the training seasons. Holding out whole seasons additionally exposes the component of $b_k$ that is common to a season.

## 4.3 Season-held-out residuals

Let the source data comprise seasons $\mathcal{S}$. For each $s\in\mathcal{S}$ we fit the predictor on $\mathcal{S}\setminus\{s\}$ and predict the scans of season $s$, which gives out-of-fold predictions $\tilde f(x_{kij})$ and residuals $\tilde r_{kij}=y_{ki}-\tilde f(x_{kij})$ for every source scan. The deployed predictor $f$ is fitted on all of $\mathcal{S}$. This is a cross-conformal construction [@vovk2015] with seasons as folds. Sample-grouped and lot-grouped five-fold versions are computed in the same way and serve as ablations.

## 4.4 Bias correction

Let $\bar r_{ki}$ be the mean residual of sample $i$ over its scans and $\bar r_k$ the mean of $\bar r_{ki}$ over the samples of lot $k$. From the season-held-out residuals of the $K$ source lots we estimate, by the method of moments for a one-way random-effects layout,

$$\hat\mu=\frac1K\sum_k \bar r_k,\qquad \hat\sigma^2=\frac{\sum_k\sum_i(\bar r_{ki}-\bar r_k)^2}{\sum_k (n_k-1)},\qquad \hat\tau^2=\max\Big\{0,\; \frac{1}{K-1}\sum_k(\bar r_k-\hat\mu)^2-\hat\sigma^2\,\frac1K\sum_k\frac1{n_k}\Big\}. \qquad\text{(2)}$$

For a new lot with reference set $A$, $|A|=m$, the bias is estimated by the mean reference residual,

$$\hat b = \bar r_A \quad (m\ge1),\qquad \hat b=\hat\mu \quad (m=0). \qquad\text{(3)}$$

The corrected point prediction is $f(x)+\hat b$. The protocol originally specified an empirical-Bayes shrinkage of this mean towards $\hat\mu$ [@efron1975], $\hat b=\hat\mu+w_m(\bar r_A-\hat\mu)$ with $w_m=\hat\tau^2/(\hat\tau^2+\hat\sigma^2/m)$. It is evaluated as an ablation ("+ shrinkage"). We do not use it in the reported method, because it brought no benefit on the mango data and is unsafe when the new population is shifted by more than the between-lot variation seen in the past (Sections 7 and 12). The variance components of Eq. (2) remain in use for the scale estimate below.

## 4.5 Lot-specific scale (LotCP-S)

Lots differ not only in bias but in residual spread. LotCP-S divides the score by

$$\hat s^2=\hat u^2+\hat e^2,\qquad \hat u^2=\frac{\nu_0\hat\sigma^2+(m-1)s_A^2}{\nu_0+m-1},\qquad \hat e^2=\frac{\sum_i\sum_j\big(f(x_{ij})-\bar f_i\big)^2}{\sum_i (J_i-1)}. \qquad\text{(4)}$$

Here $s_A^2$ is the sample variance of the $m$ reference residual means, shrunk towards the prior $\hat\sigma^2$ with pseudo-count $\nu_0$ (for $m<2$, $\hat u^2=\hat\sigma^2$), and $\hat e^2$ is the pooled within-sample variance of the *predictions* of repeated scans in the new lot, where $\bar f_i$ is the mean prediction of sample $i$. The term $\hat e^2$ needs no reference value: it measures how much the reading of the same fruit changes from scan to scan (different cheek, instrument unit or fruit temperature). When a lot has no repeated scans, $\hat e^2$ is replaced by its mean over the source lots, $e_0$. The pseudo-count is chosen from $\{5,10,20,40\}$ as the value giving the narrowest calibrated intervals on the source lots. LotCP without the suffix uses $\hat s\equiv 1$.

## 4.6 Episodic lot-balanced conformal quantile

The half-width must reflect the fact that $\hat b$ and $\hat s$ are estimated from only $m$ samples. We obtain it by replaying the deployment on the past. For each source lot $k$ with at least $m+10$ samples and each episode $e=1,\dots,E$, we draw a reference set $A_{ke}$ of $m$ samples at random, compute $\hat b_{ke}$ and $\hat s_{ke}$ from Eqs. (3)–(4) using only $A_{ke}$ (and the lot's unlabelled scans), and form the scores of the remaining scans,

$$S_{keij}=\frac{|\tilde r_{kij}-\hat b_{ke}|}{\hat s_{ke}},\qquad i\notin A_{ke}. \qquad\text{(5)}$$

The half-width multiplier is the $(1-\alpha)$ quantile of the lot-balanced score distribution,

$$\hat q_m = Q_{1-\alpha}\Big(\sum_{k=1}^{K_m}\frac{1}{K_m+1}\sum_{e=1}^{E}\frac1E\sum_{i\notin A_{ke}}\frac{1}{n_k-m}\sum_{j=1}^{J_{ki}}\frac{1}{J_{ki}}\,\delta_{S_{keij}}+\frac{1}{K_m+1}\,\delta_{+\infty}\Big), \qquad\text{(6)}$$

where $K_m$ is the number of usable source lots and $\delta$ a point mass. Every lot carries the same total weight whatever its size, every sample the same weight within its lot, and every scan the same weight within its sample. The interval for a scan $x$ of the new lot is

$$C(x)=\big[f(x)+\hat b-\hat q_m\hat s,\; f(x)+\hat b+\hat q_m\hat s\big]. \qquad\text{(7)}$$

For $m=0$ and $\hat s\equiv1$, Eq. (6) is the hierarchical conformal prediction (HCP) quantile of Lee et al. [@lee2023] applied to season-held-out residuals. For $m\ge1$ and $\hat s\equiv1$ (LotCP) it is their mean-centred few-shot score applied to season-held-out model residuals. LotCP-S adds the lot-specific scale.

## 4.7 What is guaranteed, and what is not

Suppose the predictor and the constants $(\hat\mu,\hat\sigma^2,e_0,\nu_0)$ are fixed, the $K_m$ calibration lots and the test lot are exchangeable, and samples are exchangeable within lots. Then the score of a random scan of a random non-reference sample of the test lot, computed with a random reference set, is hierarchically exchangeable with the calibration scores, and Theorem 1 of Lee et al. [@lee2023] gives $\mathbb{P}\{y\in C(x)\}\ge 1-\alpha$ for every $m$, with the probability taken over lots, reference draws and scans. A formal statement that covers random reference sets, three nested levels and lots of unequal size is given with its proof in Appendix A (Proposition 1). A Monte-Carlo check under simulated exchangeable lots is part of the unit tests of the released code.

The assumptions are not met exactly in our use. (i) Calibration residuals come from season-held-out predictors, not from the deployed predictor. (ii) The constants are estimated from the calibration lots themselves. (iii) Lots of a future season are not exchangeable with past lots if the new season differs systematically; season-held-out residuals emulate such a difference but cannot guarantee that the next one is of the same size. (iv) The guarantee is marginal over lots; it does not promise the nominal coverage within each lot [@barber2021limits]. The experiments measure how much these gaps matter.

## 4.8 Lot-level assurance (LotCP-A)

A marginal guarantee averages over lots: some lots are covered above the nominal level and others below it, and a grower harvests one lot at a time. A statement about the lot itself is more useful: *in at least a fraction $1-\delta$ of lots, at least a fraction $1-\alpha$ of the fruit is covered*. The lot structure makes such a statement available. For a lot $k$ and a reference draw $e$, let $Q_{ke}$ be the weighted $(1-\alpha)$ quantile of the scores of Eq. (5) over the non-reference scans of that lot, with the within-lot weights of Eq. (6). The interval of Eq. (7) with multiplier $q$ covers at least $1-\alpha$ of those scans exactly when $q\ge Q_{ke}$. LotCP-A therefore replaces Eq. (6) by a quantile over lots of the lot-wise quantiles,

$$\hat q^{\,A}_m = Q_{1-\delta}\Big(\sum_{k=1}^{K_m}\frac{1}{K_m+1}\sum_{e=1}^{E}\frac1E\,\delta_{Q_{ke}}+\frac{1}{K_m+1}\,\delta_{+\infty}\Big). \qquad\text{(8)}$$

If the calibration lots and the new lot are exchangeable, including their numbers of samples and scans, then $Q$ of the new lot is exchangeable with the calibration values, and the realised coverage among the non-reference scans of the new lot is at least $1-\alpha$ with probability at least $1-\delta$ over lots and reference draws (Appendix A, Proposition 2). This is a guarantee of the probably-approximately-correct type, in the spirit of prediction sets that hold for most tasks in meta-learning [@park2022] and of the second-moment coverage of Lee et al. [@lee2023]; here the task is a harvest lot and the few-shot adaptation is the bias and scale correction. It concerns the scanned fruit of the lot, not a hypothetical infinite population, and it is subject to the same caveats as the marginal guarantee. We use $\delta=0.10$ and, for comparison, $\delta=0.20$, with $1-\alpha=0.90$. A unit test of the released code checks the statement on simulated lots that differ in bias and scale.

## 4.9 Planning the reference budget before the season

The episodic replay has a by-product that is useful in its own right. For every $m$ it yields, from past lots alone, the multiplier $\hat q_m$ (or $\hat q_m^{A}$) and the average lot scale $\bar s_m$ over the replayed episodes, and therefore a *planned width* $2\hat q_m\bar s_m$: the interval width that the user should expect in the coming season if $m$ reference samples are taken per lot. The curve of planned width against $m$ can be drawn before any fruit of the new season is scanned, and it turns the choice of the number of reference samples into an explicit trade between laboratory effort and the precision of the error bar. Section 15 compares planned and realised widths.

## 4.10 Computational cost

Calibration needs one additional model fit per source season, which is done once and offline. The episodic quantile costs $O(K E N)$ score evaluations for $N$ scans per lot. At deployment the method computes two means and one variance per lot.


# 5. Experimental setup

## 5.1 Data

We use the public "Mango DMC and NIR spectra" data set, version 6 [@mangodata] (CC BY 4.0), which extends the data of Anderson et al. [@anderson2020; @anderson2021] and Walsh et al. [@walsh2024] with further seasons and instrument units. It contains 85,401 spectra of intact mango fruit acquired with handheld spectrometers in interactance geometry [@anderson2021], each paired with the oven-dry DMC of the tissue under the scanned position. The file identifies the harvest season (7 seasons, 2015–2021), the growing region (Northern Territory or Queensland, Australia), the cultivar (10 cultivars), the physiological stage, the fruit temperature class, the instrument unit (31 units), the reference sample (10,560 samples) and the population (199 populations). A population is a set of fruit from one orchard block and harvest date; we call it a lot. Every sample was scanned repeatedly (median 6 scans per sample; different instrument units, and for a subset three fruit temperatures). Table 1 summarises the data by season and Fig. 2 shows the distribution of reference values, the number of lots and the mean spectra.

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


![Fig. 2. The data set. (a) Reference dry matter content by season. (b) Number of harvest lots by season. (c) Mean absorbance spectra of three seasons in the analysis window.](figures/fig2_data.png){width=6.3in}

We use the 684–990 nm window at 3 nm steps (103 variables), the range that gave the best PLS results in the original study [@anderson2020]. All spectra are retained. The provider's outlier flags are not applied in the main analysis because we cannot establish that they were assigned without reference to prediction residuals; their effect is examined in Section 9.

## 5.2 Protocols and leakage control

*Forward chaining (primary).* For each target season $T\in\{2017,\dots,2021\}$ the source data are all seasons before $T$. Nothing from season $T$ or later enters training, preprocessing, hyper-parameter selection or calibration, except the $m$ reference samples of the lot under test. This gives 137 target lots with at least 20 samples.

*Leave-one-season-out (secondary).* Each of the seven seasons is the target in turn and all other seasons are the source. This protocol uses later seasons to predict earlier ones and is reported as a robustness check only.

*Further shifts.* (i) Only the two seasons preceding $T$ as source; (ii) one growing region as target and the other as source; (iii) one cultivar as target and all others as source (five cultivars with enough lots).

Repeated scans of a sample share one reference value, so a random split of spectra would place near-duplicates on both sides. All folds are grouped: a sample never straddles a fold in the sample-grouped scheme, a lot never does in the lot-grouped scheme, and a season never does in the season-grouped scheme. The data provider's warning against random splitting is thereby respected. Reference samples are drawn at the sample level, and all scans of a drawn sample are removed from the evaluation set of that draw. Spectral pre-treatments are row-wise and learn nothing from other spectra; scaling constants of the neural network are computed on the training fold only.

## 5.3 Point predictors

*PLS.* Standard normal variate [@barnes1989] followed by a Savitzky–Golay second derivative (17-point window, second-order polynomial) [@savitzky1964] and partial least squares regression [@wold2001]. The number of latent variables is chosen from $\{8,10,\dots,20\}$ by leave-one-season-out cross-validation inside the source data.

*LightGBM.* Gradient-boosted trees [@ke2017] on the same pre-treated spectra (400 trees, learning rate 0.05, 31 leaves, minimum 40 samples per leaf, row subsampling 0.8, column subsampling 0.5).

*1D-CNN.* Three convolution layers (16, 32 and 64 filters; kernel sizes 7, 5 and 3; strides 1, 2 and 2; ELU activations), a 64-unit dense layer with dropout 0.1 and a linear output (103,265 parameters), in the spirit of compact networks used for NIR regression [@cui2018; @walsh2024]. Inputs are SNV spectra standardised per wavelength. Training uses AdamW (weight decay $10^{-4}$), a one-cycle learning-rate schedule peaking at $10^{-3}$, batch size 256 and 20 epochs. No early stopping is used, so no validation split is needed.

LightGBM and the CNN are run with three seeds fixed before the experiments (0, 1, 2). All results are reported for every seed or as mean and standard deviation over seeds; no seed was selected. Hyper-parameters of LightGBM and the CNN were set once from common defaults and not tuned on any target season. PLS is the primary predictor because it is the reference method of the field and is deterministic.

## 5.4 Interval methods compared

*Without reference samples* ($m=0$). (1) Gaussian band $\pm z_{1-\alpha/2}\cdot$RMSECV, the implicit practice in chemometrics. (2–4) Split conformal prediction with residuals held out by sample, by lot or by season (cross-conformal with the respective folds). (5) Weighted conformal prediction for covariate shift [@tibshirani2019], with the likelihood ratio between the scans of the target lot and the source scans estimated by logistic regression on the PLS scores; it uses the unlabelled spectra of the target lot. (6–7) Conformalised quantile regression [@romano2019] with LightGBM quantile models, calibrated with sample folds or with season folds. (8) Quantile regression forest [@meinshausen2006] on PLS scores (200 trees, minimum leaf size 10). (9) Deep ensemble of five heteroscedastic CNNs trained with the Gaussian negative log-likelihood [@lakshminarayanan2017]. (10) Monte-Carlo dropout with 30 passes on one such network [@gal2016]. (11–12) LotCP and LotCP-S with $m=0$.

*With $m$ reference samples.* (a) Bias correction + source CP: the mean reference residual is subtracted and the split-conformal half-width from sample-fold residuals is kept, which combines current practice with a naive use of conformal prediction. (a′) Slope/bias correction + source CP: as (a), with the reference values of the $m$ samples regressed on their mean predictions and both slope and intercept applied ($m\ge5$). (b) Pooled recalibration: the reference residuals are added to the source calibration set. (c) Adaptive conformal inference [@gibbs2021] run over the reference samples (step size 0.05) starting from the source quantile. (d) Target-only CP: split conformal on the reference residuals alone; it is valid within the lot but requires $m\ge 1/\alpha-1$. (e) Target-only CP, centred: as (d) with scores centred on the leave-one-sample-out mean of the other reference residuals, which removes the lot bias. (f) LotCP, which for $m\ge1$ is the mean-centred hierarchical score of Lee et al. [@lee2023] applied to season-held-out residuals. (g) LotCP-S. The shrinkage versions of (f) and (g) are reported as ablations.

In addition, "spiking", that is, refitting the PLS model with the reference samples added to the training set once or replicated twenty times, is evaluated at $m=10$ with three reference draws per lot.

Methods (5)–(10) are evaluated with their own point predictions. All other methods are wrapped around the same point predictor, so differences between them are differences in calibration only.

## 5.5 Evaluation

The unit of analysis is the target lot. For every lot and every $m\in\{0,3,5,10,20,30\}$ we draw 100 random reference sets and evaluate on the scans of the remaining samples; a lot is evaluated at a given $m$ only if it has at least $m+10$ samples. Within a lot every sample has equal weight and every scan equal weight within its sample, matching Eq. (6). We report: *coverage*, the weighted share of scans whose reference value lies in the interval, averaged over draws and then over lots (lot-macro coverage); the share of lot-draws with coverage below $1-\alpha-0.10$ (*under-covered lots*); the mean interval *width*; and the Winkler *interval score* [@winkler1972; @gneiting2007], $(u-l)+\tfrac{2}{\alpha}(l-y)_+ +\tfrac{2}{\alpha}(y-u)_+$, a proper score that rewards narrow intervals and penalises misses. The nominal level is $1-\alpha=0.90$; 0.80 and 0.95 are examined in Section 9. LotCP uses $E=30$ episodes per lot.

## 5.6 Statistical analysis

Methods are compared on the same lots, so tests are paired. For each $m$ and each competing method we apply the Wilcoxon signed-rank test [@wilcoxon1945] to the per-lot differences in interval score and in absolute coverage error $|\text{coverage}-0.90|$. The test assumes that the paired differences of lots are independent and symmetric under the null; independence across lots of the same season is an approximation, and we therefore also report in how many of the five target seasons the mean difference favours the reference method. P-values are adjusted by Holm's procedure [@holm1979] within each outcome family. The effect size is the matched-pairs rank-biserial correlation [@kerby2014]. Confidence intervals for lot-macro coverage and for mean differences are 95 % percentile intervals from 2,000 bootstrap resamples of lots, stratified by season. Because the season is the top-level cluster and there are only five target seasons, per-season results are always shown alongside pooled ones.

The experimental protocol, including hypotheses, splits, methods and metrics, was written and committed to the repository before any model was trained. Deviations are listed in Section 5.8.

## 5.7 External validation data and decision analysis

*Soil vis–NIR spectra.* To test whether the findings are specific to mango, the main comparisons are repeated on visible–near-infrared spectra of soils from the Open Soil Spectral Library, version 1.2 [@safanelli2025]. Prediction of soil properties from a spectral library, adjusted with a few locally analysed samples, is an established practice in soil spectroscopy known as spiking [@guerrero2010; @guerrero2014], so the reference-sample setting is native to that field. Two subsets with a nested structure are used. (i) LUCAS, the European Union topsoil survey [@orgiazzi2018]: the model is trained on the 2009 campaign (18,393 samples) and tested on the 2015 campaign (21,782 samples); a lot is a one-degree grid cell, which stands for a region in which a few local samples would be analysed. Targets are organic carbon and pH in water. (ii) KSSL, the library of the Kellogg Soil Survey Laboratory of the United States Department of Agriculture: 19,807 samples with total carbon; a lot is a survey project, and five-fold cross-validation over projects makes held-out projects the target. Carbon is modelled as $\log(1+\%)$. Spectra (400–2500 nm, thinned to 10 nm) are converted to absorbance and pre-treated by SNV and a Savitzky–Golay first derivative (11 points); PLS with 10 to 30 latent variables, chosen by lot-grouped cross-validation in the source, is the predictor. Each soil sample has one spectrum, so the replicate-scan term of Eq. (4) is not available and LotCP-S uses the reference-sample variance only. Each source set contains a single campaign or a set of projects, so there is no season level, and calibration residuals are held out by lot. Thirty reference draws per lot are used.

*Harvest decision.* For the mango data we also evaluate one-sided lower bounds, which is what a minimum-DMC specification requires. LotCP-S is calibrated with the signed score $(\hat b-r)/\hat s$ in place of the absolute score of Eq. (5), giving a lower bound $f(x)+\hat b-\hat q_m\hat s$ with nominal coverage 0.90. A fruit is accepted for harvest when the lower bound is at least a specification $t$; the alternatives are acceptance on the point prediction, on the bias-corrected point prediction, and on a split-conformal lower bound from sample-fold residuals. Specifications of 14, 15 and 16 % DMC are examined as illustrative values around the centre of the DMC distribution of the data (mean 15.9 %); results for 15 % are shown and the others are in the supplement.

## 5.8 Deviations from the pre-specified protocol

(D1) LotCP-S was added after the first run on one predictor and one target season (PLS, 2018) showed that the pre-specified LotCP under-covered because the residual scale of that season's lots exceeded that of the source lots. The scale estimator of Eq. (4) was developed on source-season residuals only. Results for PLS on 2018 should therefore be read as development data for LotCP-S; the other four target seasons and the other two predictors had not been evaluated when the design was fixed. Both variants are reported everywhere. (D2) The centred target-only baseline (e) was added to give target-only calibration its strongest form. (D4) After the first complete evaluation and during internal review, the following were added and are reported whatever their outcome: the ablation of LotCP-S on lot-fold residuals, the slope/bias and spiking baselines, the single-instrument deployment unit, the sample-split estimation of the constants and the season jackknife. (D5) The empirical-Bayes shrinkage of the bias estimate, part of the pre-specified method, was removed from the reported method after the external validation: it was immaterial on the mango data and harmful under the LUCAS campaign shift (Sections 7 and 12). All mango results were recomputed with the plain mean; the shrinkage versions are reported as ablations. (D6) The external validation on soil spectra, the harvest-decision analysis and the lot-level assurance variant LotCP-A were added in revision. (D3) For computational reasons the CNN was trained for 20 rather than 30 epochs; lot-grouped folds were computed for one CNN seed only; and in the leave-one-season-out protocol the CNN uses one seed with season folds. These choices were made before any CNN result existed.


# 6. Results

## 6.1 Point accuracy and the structure of the error

Table 2 gives the error of the three point predictors. Cross-validation with sample-grouped folds, the usual way of reporting a calibration, gives the smallest error; lot-grouped folds give a larger one and season-grouped folds the largest. The error obtained on the next season exceeds the sample-fold estimate for every target season, and from 2018 on it exceeds the season-fold estimate as well. The standard deviation of the lot mean residual in the target seasons is 0.82–1.26 % DMC for PLS, of the same order as the within-lot error. Fig. 3 shows both effects: the residual distribution on the next season is wider than the sample-fold cross-validation residuals, and lots scatter around zero with season-specific offsets. The variance components estimated by Eq. (2) from season-held-out residuals agree: the between-lot standard deviation $\hat\tau$ is 0.91–1.51 % DMC and the within-lot, between-sample standard deviation $\hat\sigma$ is 0.80–1.18 % DMC across the five source sets.

| Target season | RMSECV sample folds | RMSECV lot folds | RMSECV season folds | RMSEP PLS | RMSEP LightGBM | RMSEP 1D-CNN | Bias PLS | SD of lot bias, PLS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2017 | 1.20 | 1.33 | 2.08 | 1.26 | 1.32 | 1.21 | -0.03 | 0.82 |
| 2018 | 1.20 | 1.24 | 1.38 | 1.68 | 1.61 | 1.25 | -0.27 | 1.26 |
| 2019 | 1.25 | 1.28 | 1.45 | 1.77 | 1.82 | 1.70 | 0.71 | 1.18 |
| 2020 | 1.25 | 1.30 | 1.47 | 1.58 | 1.44 | 1.35 | -0.39 | 1.22 |
| 2021 | 1.27 | 1.32 | 1.48 | 1.60 | 1.73 | 1.52 | -0.69 | 1.21 |

Table: Table 2. Point-prediction error (% DMC) under forward chaining. RMSECV: cross-validation inside the source seasons with PLS under three fold units. RMSEP: error on the target season (LightGBM and CNN: mean of three seeds). The last column is the standard deviation of the lot mean residuals in the target season.


![Fig. 3. Why calibration on held-out samples fails (PLS, forward chaining). (a) Residuals of sample-fold cross-validation in the source seasons and residuals on the following season, pooled over the five target seasons. (b) Mean residual of each target lot; the bar marks the season mean.](figures/fig3_lot_bias.png){width=6.3in}

## 6.2 Intervals without reference samples (RQ1)

Table 3 lists the intervals that need no reference sample. Split conformal prediction with sample-grouped folds covers 0.823 of the reference values on later-season lots (95 % CI 0.787–0.855) at a nominal 0.90, and 28 % of the lots have coverage below 0.80. The Gaussian band, the quantile regression forest and conformalised quantile regression with sample folds behave similarly (coverage 0.840, 0.841 and 0.794). The deep ensemble and Monte-Carlo dropout give the narrowest intervals and the lowest coverage (0.766 and 0.775): their predictive variance reflects the training seasons, not the lot effect of a new one. Their interval score is nevertheless the best in the table, because the CNN underlying them has a lower point error than PLS (Table 2). The shortfall is not produced by the lot-balanced weighting: with every scan weighted equally, sample-fold split conformal prediction covers 0.820. H1 is confirmed.

| Method | Coverage | 95% CI | Under-covered lots (%) | Width | Interval score |
|---|---:|---:|---:|---:|---:|
| Gaussian ±z·RMSECV | 0.840 | 0.806–0.871 | 24 | 4.00 | 6.71 |
| Split CP (sample folds) | 0.823 | 0.787–0.855 | 28 | 3.83 | 6.81 |
| Split CP (lot folds) | 0.846 | 0.813–0.877 | 23 | 4.08 | 6.71 |
| Split CP (season folds) | 0.900 | 0.869–0.926 | 14 | 5.26 | 7.05 |
| Weighted CP (covariate shift) | 0.909 | 0.883–0.931 | 16 | 7.12 | 8.54 |
| CQR (sample folds) | 0.794 | 0.758–0.827 | 38 | 3.87 | 7.27 |
| CQR (season folds) | 0.907 | 0.881–0.931 | 15 | 5.58 | 7.03 |
| Quantile regression forest | 0.841 | 0.813–0.866 | 29 | 4.28 | 6.76 |
| Deep ensemble | 0.766 | 0.731–0.796 | 46 | 3.03 | 6.20 |
| MC dropout | 0.775 | 0.740–0.805 | 43 | 3.08 | 6.14 |
| LotCP | 0.899 | 0.868–0.926 | 12 | 5.45 | 7.29 |
| LotCP-S | 0.894 | 0.862–0.922 | 14 | 5.39 | 7.26 |

Table: Table 3. Intervals without reference samples (m = 0) on 137 later-season lots; nominal coverage 0.90, PLS predictor unless the method has its own model. Coverage is the lot-macro mean with a bootstrap 95% CI; under-covered lots have coverage below 0.80. Width and interval score in % DMC.


The hold-out unit orders coverage as hypothesised (H2): sample folds 0.823, lot folds 0.846, season folds 0.900, and the ordering holds in each of the five target seasons (Table 5). Holding out lots repairs only a small part of the gap, which shows that the lot effect within the training seasons is smaller than the lot effect of a new season. Season-held-out residuals bring the pooled coverage to the nominal level, for split conformal prediction and for conformalised quantile regression alike (0.907). Two qualifications are needed. First, the price is width: intervals are 37 % wider than with sample folds, and the interval score is not better (7.05 against 6.81). Second, the pooled figure hides season-to-season variation: coverage by season ranges over 0.82–0.99 (Table 5), with over-coverage in 2017, when only two source seasons were available and the season-held-out models were weak, and coverage below nominal in each of the four later seasons. With a handful of past seasons, the next season is simply not exchangeable with them to within a few coverage points. LotCP and LotCP-S at $m=0$ behave like season-fold split conformal prediction, as expected.

Weighted conformal prediction with likelihood-ratio weights from the unlabelled target spectra reaches 0.909 coverage, but with intervals 86 % wider than split conformal prediction and unbounded intervals for 5 % of scans: when a lot is spectrally distinct, the estimated weights concentrate on few calibration points. It has the worst interval score of all methods. Covariate-shift weighting is not the right tool here, because the shift that matters is a lot bias in the residual, not a change in the distribution of spectra alone.

| Method | 2017 | 2018 | 2019 | 2020 | 2021 |
|---|---:|---:|---:|---:|---:|
| Split CP (sample folds) (m=0) | 0.884 | 0.770 | 0.846 | 0.760 | 0.769 |
| Split CP (lot folds) (m=0) | 0.917 | 0.784 | 0.856 | 0.781 | 0.795 |
| Split CP (season folds) (m=0) | 0.987 | 0.819 | 0.894 | 0.831 | 0.854 |
| LotCP-S (m=0) | 0.980 | 0.841 | 0.878 | 0.786 | 0.842 |
| Bias corr. + source CP (m=10) | 0.952 | 0.904 | 0.956 | 0.946 | 0.954 |
| Target-only CP, centred (m=10) | 0.966 | 0.954 | 0.945 | 0.953 | 0.930 |
| LotCP (m=10) | 0.985 | 0.857 | 0.922 | 0.906 | 0.912 |
| LotCP-S (m=10) | 0.957 | 0.882 | 0.902 | 0.897 | 0.914 |

Table: Table 5. Lot-macro coverage by target season (PLS, nominal 0.90).


## 6.3 Intervals with reference samples (RQ2)

Table 4 and Fig. 4 show what $m$ reference samples per lot buy. Three samples are enough to change the picture: every method that corrects the lot bias then covers at least 0.90 with intervals of about the same width as the invalid sample-fold split conformal intervals. The corrected point prediction improves accordingly: the lot-level RMSE of PLS falls from 1.36 % DMC without correction to 1.06 with three and 0.98 with ten reference samples.

| Method | m=3 | m=5 | m=10 | m=20 | m=30 |
|---|---:|---:|---:|---:|---:|
| Bias corr. + source CP | 0.921 / 3.83 / 4.96 | 0.931 / 3.83 / 4.80 | 0.938 / 3.83 / 4.68 | 0.945 / 3.82 / 4.58 | 0.941 / 3.81 / 4.64 |
| Slope/bias corr. + source CP | n/a | 0.915 / 3.83 / 5.46 | 0.941 / 3.83 / 4.75 | 0.953 / 3.82 / 4.50 | 0.952 / 3.81 / 4.53 |
| Pooled recalibration | 0.823 / 3.83 / 6.81 | 0.823 / 3.83 / 6.80 | 0.823 / 3.83 / 6.80 | 0.822 / 3.82 / 6.81 | 0.827 / 3.81 / 6.78 |
| ACI on references | 0.873 / 4.06 / 5.94 | 0.894 / 4.08 / 5.78 | 0.914 / 4.16 / 5.62 | 0.917 / 4.18 / 5.50 | 0.914 / 4.16 / 5.45 |
| Target-only CP | n/a | n/a | 0.957 / 5.64 / 6.08 | 0.931 / 4.72 / 5.39 | 0.921 / 4.53 / 5.33 |
| Target-only CP, centred | n/a | n/a | 0.956 / 4.63 / 5.12 | 0.932 / 3.58 / 4.29 | 0.921 / 3.40 / 4.25 |
| LotCP | 0.924 / 4.25 / 5.40 | 0.925 / 4.09 / 5.18 | 0.927 / 3.97 / 5.01 | 0.930 / 3.90 / 4.86 | 0.921 / 3.74 / 4.86 |
| LotCP-S | 0.921 / 3.83 / 4.91 | 0.920 / 3.60 / 4.62 | 0.919 / 3.45 / 4.46 | 0.918 / 3.29 / 4.25 | 0.914 / 3.28 / 4.31 |

Table: Table 4. Intervals with m reference samples per lot (PLS, nominal 0.90). Each cell: lot-macro coverage / mean width / interval score. n/a: the method returns unbounded intervals at this m. ACI returned unbounded intervals in up to 10% of lot-draws; its width and score are over the finite ones.


![Fig. 4. Lot-macro coverage, mean width and interval score as a function of the number of reference samples per lot (PLS, forward chaining, 137 target lots, nominal 0.90). Dashed lines: split conformal prediction without reference samples.](figures/fig4_main.png){width=6.5in}

*Methods that do not correct the bias.* Pooling the reference residuals into the source calibration set has no visible effect (coverage 0.823 at $m=10$): a few target residuals among tens of thousands of source residuals do not move the quantile. Adaptive conformal inference over the reference samples raises coverage to 0.914 at $m=10$ but does so by widening the interval, and returns unbounded intervals in 9 % of lot-draws.

*Target-only calibration.* Split conformal prediction on the reference samples alone is valid within each lot, which shows in its tight distribution of lot-wise coverage (Fig. 5). It cannot return a bounded 90 % interval for $m<9$, and at $m=10$ it is conservative (coverage 0.956) and wide: the centred version is 34 % wider than LotCP-S. By $m=20$ the centred version reaches the interval score of LotCP-S (4.29 against 4.25) and at $m=30$ it is marginally better (4.25 against 4.31).

*Bias correction with the source quantile.* Subtracting the mean reference residual and keeping the sample-fold half-width is a strong baseline with PLS. Its coverage is above nominal (0.931–0.945) because two errors partly cancel: the sample-fold residuals contain a remnant of the lot effect, which widens the interval, and the uncertainty of the estimated bias is ignored, which should narrow it. The half-width does not depend on $m$, so the method cannot turn additional reference samples into narrower intervals, and Section 8 shows that the cancellation does not carry over to other predictors.

*Slope-and-bias correction and spiking.* Two further maintenance practices were tested. Regressing the reference values of the $m$ samples on their predictions and applying the fitted slope and intercept is worse than the mean correction at $m=5$ (interval score 5.46 against 4.80), because five points do not determine a slope, and is comparable from $m=10$ (4.75 against 4.68). Refitting the PLS model with ten reference samples added to the training set ("spiking") barely changes the predictions when the samples are added once (lot-level RMSE 1.34 % DMC against 1.36 without any correction) and remains clearly worse than the mean bias correction when they are replicated twenty times (1.16 against 0.98; supplementary table S11).

*LotCP and LotCP-S.* LotCP covers 0.921–0.930, somewhat above nominal, with a half-width that shrinks as $m$ grows. LotCP-S covers 0.914–0.921 for $m\ge3$ and has the lowest interval score of all methods for $m$ from 3 to 20 (Table 4). At $m=10$ its intervals are 10 % narrower than those of bias correction with the source quantile and 13 % narrower than those of LotCP. By season, its coverage at $m=10$ ranges over 0.88–0.96 (Table 5). Leaving out one target season at a time moves the pooled figure between 0.893 and 0.934, and the unweighted mean over seasons is 0.911 (supplementary table S4b); for sample-fold split conformal prediction the corresponding figures are 0.781–0.843 and 0.806. The 2018 value is below nominal even though 2018 served as development data for the scale estimator; we return to this in Section 11.

![Fig. 5. Coverage within each of the 137 target lots (PLS, nominal 0.90, dotted line). Marginal coverage near the nominal level can coexist with many badly covered lots.](figures/fig5_lot_coverage.png){width=6.5in}

*Paired tests.* Table 7 compares the per-lot interval score of LotCP-S with its competitors. Against bias correction with the source quantile the difference is not significant at $m=3$ (Holm-adjusted p = 1.000) and is significant from $m=5$ on (p = 0.002 at $m=5$, p < 0.001 at $m=10$), with the mean difference favouring LotCP-S in all five seasons from $m=5$. Against the centred target-only method LotCP-S is better at $m=10$ (p < 0.001), marginally better at $m=20$ (p = 0.036, mean difference -0.03) and not different at $m=30$ (p = 1.000). On absolute coverage error the centred target-only method is better than LotCP-S at $m=20$ and $m=30$ (mean difference 0.014 and 0.020; all tests are in the supplementary table S6), which reflects its lot-conditional validity. The conclusion for RQ2 is therefore bounded: LotCP-S is the best of the compared methods when few reference samples are available, roughly $3\le m\le 10$, and offers no advantage over target-only calibration once 20 to 30 samples per lot can be afforded.

| LotCP-S versus | m | Lots | Mean difference | 95% CI | Holm p | Rank-biserial r | Seasons favouring LotCP-S |
|---|---:|---:|---:|---:|---:|---:|---:|
| Bias corr. + source CP | 3 | 137 | -0.05 | -0.14 to 0.04 | 1.000 | -0.04 | 3/5 |
| Bias corr. + source CP | 5 | 137 | -0.18 | -0.27 to -0.07 | 0.002 | -0.39 | 5/5 |
| Bias corr. + source CP | 10 | 137 | -0.23 | -0.32 to -0.13 | <0.001 | -0.51 | 5/5 |
| Bias corr. + source CP | 20 | 129 | -0.32 | -0.42 to -0.22 | <0.001 | -0.66 | 5/5 |
| Bias corr. + source CP | 30 | 112 | -0.32 | -0.43 to -0.21 | <0.001 | -0.66 | 5/5 |
| Target-only CP, centred | 10 | 137 | -0.66 | -0.86 to -0.50 | <0.001 | -0.83 | 5/5 |
| Target-only CP, centred | 20 | 129 | -0.03 | -0.10 to 0.07 | 0.036 | -0.33 | 4/5 |
| Target-only CP, centred | 30 | 112 | 0.06 | -0.01 to 0.16 | 1.000 | -0.04 | 2/5 |
| LotCP-S + shrinkage | 3 | 137 | 0.05 | 0.01 to 0.08 | <0.001 | 0.52 | 1/5 |
| LotCP-S + shrinkage | 5 | 137 | -0.01 | -0.03 to 0.01 | 1.000 | 0.19 | 3/5 |
| LotCP-S + shrinkage | 10 | 137 | -0.00 | -0.01 to 0.01 | 1.000 | 0.14 | 3/5 |
| LotCP-S + shrinkage | 20 | 129 | -0.00 | -0.01 to 0.00 | 1.000 | 0.05 | 4/5 |
| LotCP-S + shrinkage | 30 | 112 | -0.00 | -0.01 to 0.00 | 1.000 | -0.05 | 4/5 |
| LotCP | 3 | 137 | -0.49 | -0.60 to -0.38 | <0.001 | -0.79 | 4/5 |
| LotCP | 5 | 137 | -0.56 | -0.70 to -0.43 | <0.001 | -0.80 | 4/5 |
| LotCP | 10 | 137 | -0.56 | -0.69 to -0.43 | <0.001 | -0.82 | 4/5 |
| LotCP | 20 | 129 | -0.61 | -0.72 to -0.49 | <0.001 | -0.85 | 5/5 |
| LotCP | 30 | 112 | -0.54 | -0.68 to -0.41 | <0.001 | -0.84 | 4/5 |

Table: Table 7. Paired comparison of the per-lot interval score of LotCP-S with competing methods (Wilcoxon signed-rank test, Holm-adjusted over all comparisons of the family; negative differences favour LotCP-S).


# 7. Ablation study (RQ3)

Table 6 and Fig. 6 remove or replace one component at a time.

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

Table: Table 6. Ablation of LotCP components (PLS, nominal 0.90). Each cell: coverage / width / interval score.


![Fig. 6. Ablation: lot-macro coverage with bootstrap 95 % CI for m = 5 and m = 20; the interval score (IS) is printed next to each variant.](figures/fig6_ablation.png){width=6.3in}

*Scale.* The lot-specific scale is the component that matters most once $m>0$. Removing it (LotCP) raises the interval score at $m=10$ from 4.46 to 5.02. The two sources of scale information both contribute: with the reference-sample variance alone the score is 4.58, with the replicate-scan variance alone 4.74. The replicate-scan term is the only one available at $m\le1$ and costs no reference measurement. It is also what separates LotCP-S from the bias-correction shortcut when reference samples are few. Without the replicate-scan term, the per-lot interval score of the reference-scale-only variant is worse than that of bias correction with the source quantile at $m=3$ (mean difference 0.19, Holm-adjusted p = 0.004), because a scale estimated from three samples is noisy, does not differ from it at $m=5$ or 10 (p = 0.347 and = 0.421) and is better only from $m=20$ (p < 0.001; supplementary table S6b). A user who takes a single scan per fruit should therefore not expect an efficiency gain over that shortcut with fewer than about twenty reference samples; what remains is the stability of coverage across predictors shown in Section 8.

*Fold unit.* At $m=0$, residuals held out by lot or by sample give coverage 0.846 and 0.830; season-held-out residuals are needed to reach the nominal level. With $m>0$ the picture changes. After the lot bias has been corrected, what is left to calibrate is the within-lot residual, and lot-fold residuals describe it well: LotCP on lot-fold residuals covers 0.892 at $m=10$, slightly below nominal, with narrower intervals than LotCP on season-fold residuals, which over-covers (0.927). LotCP-S on lot-fold residuals covers 0.908 with an interval score of 4.36, against 0.919 and 4.46 for season-fold residuals. The lot-fold variant of LotCP-S is therefore the more efficient one, and it is not less safe by season: its lowest per-season coverage at $m=10$ is 0.89, against 0.88 for season-fold residuals. Season-held-out residuals are thus needed without reference samples and are not needed with them. We keep the season-fold variant as the reported method because it was fixed before this comparison was made, and note that the choice costs about 6 % in width at $m=10$.

*Shrinkage.* The pre-specified empirical-Bayes shrinkage of the bias estimate has a small effect at $m=3$ (interval score 5.32 against 5.40 for the plain mean with the location-only method, 4.86 against 4.91 with LotCP-S) and none from $m=10$ (4.46 against 4.46). The reason is visible in the variance components: the lot bias is large relative to the sample noise, so the shrinkage weight is already 0.79–0.83 at $m=3$. On the soil data of Section 12 shrinkage is harmful. The part of H4 that concerns shrinkage is not supported, and the reported method uses the plain mean.

*Episodic quantile.* Replacing the replayed quantile by the quantile of within-lot residuals centred on the true lot mean, which ignores the estimation error of the bias, gives coverage 0.899 at $m=3$ and 0.917 at $m=10$ for the location-only method, and it fails at $m=0$ (0.782). Because season-fold residuals are conservative for $m>0$, the omission is not punished in this data set. The replay is nevertheless what makes the scale-adaptive score calibratable at all, since the distribution of $|r-\hat b|/\hat s$ depends on $m$ through both estimates.

*Weighting.* Giving every scan rather than every lot the same weight changes little (0.932 against 0.927 at $m=10$), because lot sizes are fairly homogeneous here.

In summary, H4 holds for the scale component and, at $m=0$, for the fold unit. It does not hold for shrinkage, which was therefore removed from the method, and holds only at very small $m$ for the episodic quantile of the location-only method.

# 8. Generalisation across predictors and protocols (RQ4)

Table 8 and Fig. 7 repeat the comparison for LightGBM and the CNN, and for the leave-one-season-out protocol. The seed-to-seed standard deviation of lot-macro coverage is at most 0.002 for the LotCP variants (supplementary table S7b).

| Predictor, protocol | Method | Lots | Coverage | Under-covered lots (%) | Width | Interval score |
|---|---:|---:|---:|---:|---:|---:|
| PLS, forward | Split CP (sample folds) (m=0) | 137 | 0.823 | 28 | 3.83 | 6.81 |
| PLS, forward | Split CP (season folds) (m=0) | 137 | 0.900 | 14 | 5.26 | 7.05 |
| PLS, forward | Bias corr. + source CP (m=10) | 137 | 0.938 | 5 | 3.83 | 4.68 |
| PLS, forward | Target-only CP, centred (m=10) | 137 | 0.956 | 3 | 4.63 | 5.12 |
| PLS, forward | LotCP (m=10) | 137 | 0.927 | 10 | 3.97 | 5.01 |
| PLS, forward | LotCP-S (m=10) | 137 | 0.919 | 8 | 3.45 | 4.46 |
| LightGBM, forward | Split CP (sample folds) (m=0) | 137 | 0.759 | 51 | 3.09 | 7.12 |
| LightGBM, forward | Split CP (season folds) (m=0) | 137 | 0.902 | 18 | 4.98 | 6.69 |
| LightGBM, forward | Bias corr. + source CP (m=10) | 137 | 0.882 | 19 | 3.09 | 4.60 |
| LightGBM, forward | Target-only CP, centred (m=10) | 137 | 0.957 | 3 | 4.62 | 5.03 |
| LightGBM, forward | LotCP (m=10) | 137 | 0.915 | 11 | 3.60 | 4.74 |
| LightGBM, forward | LotCP-S (m=10) | 137 | 0.914 | 8 | 3.43 | 4.41 |
| 1D-CNN, forward | Split CP (sample folds) (m=0) | 137 | 0.789 | 42 | 3.07 | 6.00 |
| 1D-CNN, forward | Split CP (season folds) (m=0) | 137 | 0.928 | 11 | 5.02 | 6.05 |
| 1D-CNN, forward | Bias corr. + source CP (m=10) | 137 | 0.909 | 12 | 3.07 | 4.03 |
| 1D-CNN, forward | Target-only CP, centred (m=10) | 137 | 0.959 | 3 | 4.11 | 4.46 |
| 1D-CNN, forward | LotCP (m=10) | 137 | 0.929 | 14 | 3.95 | 4.77 |
| 1D-CNN, forward | LotCP-S (m=10) | 137 | 0.914 | 7 | 3.06 | 3.87 |
| PLS, leave-one-season-out | Split CP (sample folds) (m=0) | 198 | 0.849 | 23 | 4.07 | 6.57 |
| PLS, leave-one-season-out | Split CP (season folds) (m=0) | 198 | 0.896 | 16 | 4.69 | 6.43 |
| PLS, leave-one-season-out | Bias corr. + source CP (m=10) | 198 | 0.949 | 3 | 4.07 | 4.79 |
| PLS, leave-one-season-out | Target-only CP, centred (m=10) | 198 | 0.957 | 3 | 4.63 | 5.11 |
| PLS, leave-one-season-out | LotCP (m=10) | 198 | 0.908 | 12 | 3.37 | 4.58 |
| PLS, leave-one-season-out | LotCP-S (m=10) | 198 | 0.907 | 8 | 3.26 | 4.36 |
| 1D-CNN, leave-one-season-out | Split CP (season folds) (m=0) | 198 | 0.923 | 11 | 4.34 | 5.39 |
| 1D-CNN, leave-one-season-out | LotCP (m=10) | 198 | 0.914 | 11 | 3.02 | 4.00 |
| 1D-CNN, leave-one-season-out | LotCP-S (m=10) | 198 | 0.908 | 7 | 2.87 | 3.75 |

Table: Table 8. Generalisation across point predictors and protocols (nominal 0.90). LightGBM and CNN under forward chaining: metrics averaged over three seeds within lot.


![Fig. 7. Lot-macro coverage of LotCP and LotCP-S for three point predictors and two protocols (nominal 0.90).](figures/fig7_generalisation.png){width=6.5in}

The failure of sample-fold split conformal prediction is larger for the more flexible predictors: coverage is 0.759 for LightGBM and 0.789 for the CNN, against 0.823 for PLS, because flexible models absorb more of the lot effects of their training lots. For the same reason, bias correction with the source quantile, which over-covers with PLS, under-covers with LightGBM (0.882 at $m=10$) and sits at 0.909 with the CNN. Its coverage depends on how strongly the predictor fits its training lots, which the user does not control. LotCP-S covers 0.914 and 0.914 at $m=10$ with these predictors, and 0.907 and 0.908 under leave-one-season-out with PLS and the CNN. Across the five predictor–protocol combinations its coverage at $m=10$ stays within 0.907–0.919. With the CNN, whose point error is lowest, LotCP-S at $m=10$ gives a mean width of 3.06 % DMC, that is, about ±1.5 % DMC.

# 9. Robustness and sensitivity (RQ4)

| Condition | m=0 | m=5 | m=10 | m=20 |
|---|---:|---:|---:|---:|
| Main setting | 0.894 / 5.39 | 0.920 / 3.60 | 0.919 / 3.45 | 0.918 / 3.29 |
| Reference error SD 0.25 % DMC | 0.894 / 5.39 | 0.920 / 3.63 | 0.920 / 3.48 | 0.921 / 3.33 |
| Reference error SD 0.5 % DMC | 0.894 / 5.39 | 0.921 / 3.73 | 0.923 / 3.57 | 0.928 / 3.47 |
| Provider-flagged outliers removed | 0.897 / 5.24 | 0.922 / 3.51 | 0.920 / 3.31 | 0.922 / 3.20 |
| 10 past lots for calibration | 0.975 / 8.74 | 0.989 / 6.80 | 0.989 / 6.34 | 0.996 / 14.31 |
| 20 past lots for calibration | 0.910 / 5.70 | 0.947 / 4.07 | 0.947 / 3.86 | 0.949 / 3.78 |
| 40 past lots for calibration | 0.902 / 5.52 | 0.930 / 3.76 | 0.929 / 3.56 | 0.931 / 3.46 |
| 80 past lots for calibration | 0.895 / 5.43 | 0.923 / 3.64 | 0.924 / 3.50 | 0.921 / 3.32 |
| 5 episodes per lot | 0.894 / 5.39 | 0.919 / 3.58 | 0.921 / 3.46 | 0.921 / 3.35 |
| 10 episodes per lot | 0.894 / 5.39 | 0.919 / 3.58 | 0.918 / 3.43 | 0.919 / 3.33 |
| 100 episodes per lot | 0.894 / 5.39 | 0.920 / 3.59 | 0.920 / 3.44 | 0.921 / 3.35 |
| Fixed pseudo-count ν₀ = 5 | 0.894 / 5.39 | 0.922 / 3.63 | 0.923 / 3.46 | 0.919 / 3.31 |
| Fixed pseudo-count ν₀ = 20 | 0.894 / 5.39 | 0.923 / 3.72 | 0.924 / 3.54 | 0.923 / 3.37 |
| Fixed pseudo-count ν₀ = 80 | 0.894 / 5.39 | 0.923 / 3.79 | 0.924 / 3.64 | 0.925 / 3.49 |
| Constants and quantile from disjoint halves of the past lots | 0.893 / 5.53 | 0.931 / 3.85 | 0.929 / 3.59 | 0.928 / 3.42 |
| Deployment unit: one instrument unit within a lot | 0.912 / 5.58 | 0.919 / 3.30 | 0.919 / 3.12 | 0.914 / 2.88 |
| Source: two preceding seasons only | 0.891 / 6.42 | 0.917 / 4.44 | 0.918 / 4.30 | 0.918 / 3.99 |
| Unseen growing region | 0.908 / 5.15 | 0.912 / 3.39 | 0.913 / 3.27 | 0.913 / 3.19 |
| Unseen cultivar | 0.911 / 4.83 | 0.907 / 3.29 | 0.907 / 3.17 | 0.906 / 3.11 |

Table: Table 9. Robustness and sensitivity of LotCP-S (PLS, nominal 0.90). Each cell: lot-macro coverage / mean width.


![Fig. 8. Robustness of LotCP-S coverage (PLS, nominal 0.90): (a) Gaussian error added to the reference values of the m reference samples; (b) number of past lots available for calibration; (c) other source–target shifts.](figures/fig8_robustness.png){width=6.5in}

*Error in the reference values.* Oven-drying has its own error, and the $m$ reference values carry it. Adding Gaussian error with a standard deviation of 0.25 or 0.5 % DMC to the reference samples at deployment (not to the calibration lots) leaves coverage at or slightly above nominal (0.923 at $m=10$ for 0.5 % DMC) and widens the intervals by 4 % (Table 9). The noisier references inflate the estimated lot scale, which errs on the conservative side.

*Reuse of the calibration lots.* The variance components and the pseudo-count are estimated from the same past lots that provide the conformal quantile. Estimating them on a random half of the lots and computing the quantile on the other half, with the pseudo-count fixed at 10, gives coverage 0.929 and an interval score of 4.46 at $m=10$, against 0.919 and 4.46; the reuse does not make the intervals optimistic.

*Single-instrument units.* In the data set a lot was usually scanned with several instrument units, whereas a grower would use one. Redefining the deployment unit as one instrument unit within a lot (reference and query scans from that unit only; 558 units) gives coverage 0.919 for LotCP-S at $m=10$ with a mean width of 3.12 % DMC, 0.833 for sample-fold split conformal prediction and 0.954 for bias correction with the source quantile. The interval score of LotCP-S is 4.12, against 4.32 for centred target-only calibration at $m=10$ and 3.88 against 3.85 at $m=20$. The share of unit-draws with coverage below 0.80 is higher than at lot level (11 %), because single-instrument units differ more in residual scale than lots that average over instruments.

*Outlier screening.* Removing the scans flagged by the data provider from calibration and evaluation leaves coverage unchanged (0.920) and narrows the intervals by 4 %.

*Number of past lots.* With only 10 past lots the lot-balanced quantile is close to the largest calibration score and the intervals are very wide; with 20 lots coverage is 0.947 and with 40 lots 0.929, at widths 12 % and 3 % above those obtained with all lots. The method is always conservative when lots are few, which follows from the $1/(K_m+1)$ mass at infinity in Eq. (6), and some 40 past lots are needed before the conservatism becomes small.

*Tuning constants.* The number of episodes (5 to 100) and the pseudo-count of the scale estimate (5 to 80) change coverage by less than 0.002 and 0.006 respectively.

*Nominal level.* Table 10 gives the results for nominal levels 0.80 and 0.95. The pattern is the same: sample-fold split conformal prediction under-covers and LotCP-S with $m\ge5$ covers slightly above the nominal level.

| Nominal | Method | Coverage | Width |
|---|---:|---:|---:|
| 0.80 | Split CP (sample folds) (m=0) | 0.716 | 2.94 |
| 0.80 | Split CP (season folds) (m=0) | 0.820 | 3.92 |
| 0.80 | Target-only CP, centred (m=20) | 0.832 | 2.58 |
| 0.80 | LotCP-S (m=5) | 0.831 | 2.70 |
| 0.80 | LotCP-S (m=20) | 0.835 | 2.55 |
| 0.90 | Split CP (sample folds) (m=0) | 0.823 | 3.83 |
| 0.90 | Split CP (season folds) (m=0) | 0.900 | 5.26 |
| 0.90 | Target-only CP, centred (m=20) | 0.932 | 3.58 |
| 0.90 | LotCP-S (m=5) | 0.920 | 3.60 |
| 0.90 | LotCP-S (m=20) | 0.918 | 3.29 |
| 0.95 | Split CP (sample folds) (m=0) | 0.889 | 4.63 |
| 0.95 | Split CP (season folds) (m=0) | 0.940 | 6.78 |
| 0.95 | Target-only CP, centred (m=20) | 0.981 | 5.54 |
| 0.95 | LotCP-S (m=5) | 0.963 | 4.58 |
| 0.95 | LotCP-S (m=20) | 0.963 | 4.14 |

Table: Table 10. Other nominal levels (PLS, forward chaining).


*Other shifts.* When only the two seasons before the target are used as source, LotCP-S still covers 0.918 at $m=10$, with wider intervals (4.30 % DMC) because fewer and less diverse past lots are available. When a whole growing region or a whole cultivar is held out, coverage at $m=10$ is 0.913 and 0.907. In these two protocols the source contains all seasons, so they test a region or cultivar shift without a season shift.

# 10. Computational analysis (RQ5)

| Component | Time | Per 1000 scans at deployment |
|---|---:|---:|
| PLS fit (final model) | 1.1 s | 6.6 ms |
| LightGBM fit | 2.0 s | 11.2 ms |
| 1D-CNN fit (20 epochs) | 147.6 s | 58.3 ms |
| PLS: all cross-fits for one target season | 40 s | – |
| 1D-CNN: all cross-fits for one target season | 1395 s | – |
| LotCP calibration, m = 10 | 0.5 s | < 0.1 ms (one bias, one scale per lot) |
| LotCP-S calibration, m = 10 | 1.8 s | < 0.1 ms (one bias, one scale per lot) |
| LotCP-S calibration, m = 30 | 1.1 s | < 0.1 ms (one bias, one scale per lot) |

Table: Table 11. Computing time on a 4-core CPU without GPU (mean over target seasons; CNN fits used one thread each).


The cost of the method is dominated by the season-held-out fits, one per source season, which are done once when the calibration is built (Table 11). Energy use was not measured; on the CPU used here the complete cross-fitting for one target season took 40 s for PLS and 23 min for the CNN. The episodic calibration itself takes about 1.8 s for 187 past lots and 30 episodes, and the deployment step is a bias and a scale per lot, which is negligible on the embedded processor of a handheld instrument. The relevant cost is the number of destructive reference measurements. Fig. 4 expresses the trade-off: with LotCP-S and PLS, three reference samples per lot give a mean width of 3.83 % DMC, ten give 3.45, and thirty give 3.28; most of the gain is obtained with the first five to ten samples.

# 11. Error analysis (RQ5)

![Fig. 9. Error analysis at m = 10 (PLS). (a) Lot coverage against the absolute lot bias. (b) Lot coverage against the ratio of the lot's residual standard deviation to the prior scale. (c) Coverage by reference DMC range.](figures/fig9_error_analysis.png){width=6.5in}

We examined coverage at the level of the lot and of the scan for $m=10$ (Fig. 9). Of the 137 target lots, 38 have coverage below 0.80 under sample-fold split conformal prediction, 13 under LotCP and 4 under LotCP-S. For split conformal prediction, lot coverage is governed by the absolute lot bias (Spearman correlation -0.79). After bias correction the bias no longer matters much, and the remaining failures are lots whose residual spread exceeds what past lots suggest: the correlation between lot coverage and the ratio of the lot's residual standard deviation to the prior scale is -0.95 for LotCP and -0.84 for LotCP-S. The scale estimate of LotCP-S reduces the number of badly covered lots but cannot identify a wide lot reliably from ten reference samples and the repeated scans; the lot with the lowest coverage has a residual spread of 2.2 times the prior scale.

By subgroup, LotCP-S coverage is 0.93 for fruit at the green stage and 0.90 for fruit at the ripening stage; 0.91, 0.90 and 0.89 for the low, medium and high fruit-temperature classes; 0.92 for instrument units present in the source seasons and 0.92 for units that are new in the target season; and 0.92 and 0.96 for cultivars present in and absent from the source seasons. The lower coverage at the ripening stage is in line with the finding of the data set's authors that physiological stage affects model performance more than cultivar, season or region [@anderson2020]. Among cultivars the lowest coverage is 0.86 for Keitt. Scans carrying the provider's first outlier flag are covered at 0.81 (0.50 under sample-fold split conformal prediction). Coverage is lower at the extremes of the DMC range (Fig. 9c), a known limitation of scores that do not adapt to the predicted value. These figures are a reminder that the guarantee is marginal: a lot of ripening fruit, or a lot measured with atypical scatter, can be covered below the nominal level even when coverage is nominal on average.


# 12. External validation on soil vis–NIR spectra (RQ4)

The experiments so far use one fruit and one instrument family. We therefore repeated the central comparisons on two soil subsets of the Open Soil Spectral Library (Section 5.7), a different material, spectral range, instrument and reference chemistry, in a field where adjusting a library model with a few local samples is established practice.

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

Table: Table 12. External validation on vis–NIR soil spectra (PLS, nominal 0.90). Carbon is modelled as log(1 + %); widths and interval scores are in the units of the modelled quantity. Calibration residuals are held out by lot (grid cell or project). All methods and m: supplementary table S13.


![Fig. 10. Lot-macro coverage on the soil data as a function of the number of local reference samples (PLS, nominal 0.90, dotted line). Dashed line: split conformal prediction with sample folds and no reference samples.](figures/fig10_soil.png){width=6.5in}

*The coverage loss is larger than for mango.* A model trained on the 2009 LUCAS campaign and applied to the 2015 campaign has a prediction error on the target of 0.57 log-units for organic carbon, against 0.32 in cross-validation, with a mean offset of 0.43; for pH the error is 1.36 against 0.61, with an offset of -1.15 pH units. We do not know the origin of this between-campaign offset; whatever its cause, it is the kind of batch effect a user of a spectral library can meet. Split conformal intervals calibrated within the 2009 campaign then cover 0.63 (organic carbon) and 0.40 (pH) of the 2015 values in 467 grid cells, at a nominal 0.90. Holding residuals out by lot does not help (0.64 and 0.40), because the shift is between campaigns and the source contains only one. This is the situation in which no label-free repair exists. For held-out KSSL projects, which are exchangeable with the calibration projects by construction, sample-fold split conformal prediction covers 0.881 and lot-fold calibration 0.895: with exchangeable lots and no campaign effect, the loss is small and holding out lots removes it, as hierarchical conformal theory predicts.

*A few local reference samples repair most of it.* With five reference samples per cell, LotCP-S covers 0.888 for organic carbon and 0.872 for pH; with twenty, 0.899 and 0.885. Coverage stays up to three points below nominal, because the residual scale of the 2015 campaign also differs from that of the 2009 cells that calibrate the half-width; the method does not fully absorb a shift in scale between campaigns. For KSSL projects it covers 0.914–0.916.

*Comparison with the alternatives.* On LUCAS organic carbon LotCP-S has a lower interval score than bias correction with the source quantile and slope/bias correction at $m=5$, 10 and 20, and than centred target-only calibration at $m=10$ and 20 (Holm-adjusted p ≤ 0.003 against the first two; p < 0.001 and < 0.001 against the third; supplementary table S13c). On LUCAS pH it is better than bias correction at $m=5$ and 10 (p < 0.001 and = 0.021) and not different at $m=20$ (p = 0.204); slope/bias correction has a numerically lower score from $m=10$, a difference that is not significant. On KSSL it does not differ from bias correction at $m=5$ and 10 (p = 1.000 and = 1.000) and is better at $m=20$ (p = 0.024); slope/bias correction has the numerically best score there at $m=20$. Bias correction with the source quantile under-covers on all three soil tasks (0.878, 0.891 and 0.872 at $m=10$), where it over-covered with PLS on mango: its coverage is again not under control. Centred target-only calibration is valid and wider, as before. Since soil samples have a single spectrum, these comparisons involve no replicate-scan information; the advantage of LotCP-S on LUCAS comes from calibrating the half-width for the estimation error and from the reference-sample scale.

*Shrinkage fails under a campaign shift.* The pre-specified shrinkage variant covers only 0.70 for pH and 0.85 for organic carbon at $m=5$, against 0.87 and 0.89 with the plain mean (supplementary table S13). The between-lot variance estimated inside the 2009 campaign is small, so the shrinkage weight is low and the estimate is pulled towards the 2009 mean, which the 2015 campaign has left. On KSSL, where lots are exchangeable, shrinkage gives a small gain at $m=5$ (interval score 2.05 against 2.10). Shrinkage thus helps a little when its assumption holds and fails badly when it does not, and the user cannot know in advance which case applies. This is why the reported method does not use it.

Taken together, the soil data reproduce the three main findings on independent material: intervals calibrated within the source population lose coverage on a new population, drastically so across survey campaigns; a handful of local reference samples restores most of the coverage; and LotCP-S is not significantly worse than any competing method at $m\le10$ and is significantly better where the shift is large. They also show a limit: under a between-campaign change of residual scale, coverage remains a few points short of nominal.

# 13. Consequences for a harvest decision

Table 13 and Fig. 11 translate the intervals into the decision they are meant to support, for a specification of 15 % DMC.

| Acceptance rule | Coverage of lower bound | Accepted (%) | Non-compliant among accepted (%) | Lots with > 10 % non-compliant (%) | Compliant fruit accepted (%) |
|---|---:|---:|---:|---:|---:|
| Point prediction ≥ t (m=0) | – | 60 | 13 | 45 | 90 |
| Split-CP lower bound ≥ t (m=0) | 0.838 | 35 | 3 | 12 | 58 |
| LotCP-S lower bound ≥ t (m=0) | 0.874 | 30 | 2 | 8 | 51 |
| Bias-corrected point prediction ≥ t (m=5) | – | 57 | 8 | 44 | 91 |
| LotCP-S lower bound ≥ t (m=5) | 0.919 | 38 | 1 | 5 | 64 |
| Bias-corrected point prediction ≥ t (m=10) | – | 57 | 8 | 40 | 91 |
| LotCP-S lower bound ≥ t (m=10) | 0.920 | 38 | 1 | 6 | 65 |
| LotCP-S lower bound ≥ t (m=20) | 0.918 | 41 | 1 | 4 | 67 |

Table: Table 13. Harvest decision against a minimum dry-matter specification t = 15 % (PLS, forward chaining, one-sided nominal level 0.90). A fruit is accepted when the rule's statistic is at least t; it is compliant when its reference DMC is at least t.


![Fig. 11. Harvest decision against a 15 % DMC specification (PLS, 137 later-season lots): share of accepted fruit that is non-compliant, share of lots in which more than 10 % of the accepted fruit is non-compliant, and share of compliant fruit that is accepted.](figures/fig11_decision.png){width=6.5in}

Accepting fruit on the point prediction lets through 13 % non-compliant fruit among those accepted, and in 45 % of lots more than one accepted fruit in ten is below the specification. Bias correction with ten reference samples reduces the first figure to 8 % but leaves 40 % of lots above the 10 % mark, because a decision on the point value ignores the scatter around it. A split-conformal lower bound from sample-fold residuals covers 0.838 instead of 0.90, passes 3 % non-compliant fruit and accepts 58 % of the compliant fruit. The LotCP-S lower bound with ten reference samples covers 0.920, passes 1 % non-compliant fruit, leaves 6 % of lots above the 10 % mark and accepts 65 % of the compliant fruit. It is therefore both safer and less wasteful than the uncalibrated bound: the reference samples remove the lot bias, so the bound can sit closer to the prediction. The price of any valid bound is visible in the last column: about a third of the compliant fruit is not accepted at this uncertainty level, compared with a tenth under the point rule. Whether that trade is acceptable depends on the cost of harvesting immature fruit relative to that of delaying harvest, which is the grower's judgement; the bounds make the trade explicit. Results for specifications of 14 and 16 % are in supplementary table S14.


# 14. Lot-level assurance

The marginal method leaves a minority of lots badly covered (Section 11), and near-nominal average coverage means that in a large share of lots the realised coverage is below the nominal level: with LotCP-S and ten reference samples only 69 % of lot-draws reach 0.90. Table 14 and Fig. 12 show what LotCP-A (Section 4.8) achieves when it is asked for 0.90 coverage in at least 90 % of lots.

| Method | m=5 | m=10 | m=20 | m=30 |
|---|---:|---:|---:|---:|
| Bias corr. + source CP | 74 % / 0.931 / 3.83 | 77 % / 0.938 / 3.83 | 78 % / 0.945 / 3.82 | 77 % / 0.941 / 3.81 |
| Target-only CP, centred | n/a | 88 % / 0.956 / 4.63 | 78 % / 0.932 / 3.58 | 71 % / 0.921 / 3.40 |
| LotCP-S | 70 % / 0.920 / 3.60 | 69 % / 0.919 / 3.45 | 68 % / 0.918 / 3.29 | 65 % / 0.914 / 3.28 |
| LotCP-A (δ = 0.20) | 81 % / 0.944 / 4.01 | 81 % / 0.941 / 3.77 | 80 % / 0.938 / 3.57 | 82 % / 0.941 / 3.65 |
| LotCP-A (δ = 0.10) | 91 % / 0.964 / 4.61 | 92 % / 0.964 / 4.30 | 90 % / 0.958 / 3.97 | 91 % / 0.958 / 4.02 |

Table: Table 14. Lot-level assurance (PLS, forward chaining, 137 target lots, 1 − α = 0.90). Each cell: share of lot-draws whose realised coverage is at least 0.90 / lot-macro coverage / mean width (% DMC). The target share is 90 % for δ = 0.10 and 80 % for δ = 0.20.


![Fig. 12. Lot-level assurance (PLS, forward chaining). (a) Share of lot-draws in which at least 90 % of the fruit is covered; dotted lines mark the targets of LotCP-A for δ = 0.10 and δ = 0.20. (b) Mean interval width.](figures/fig12_assurance.png){width=6.3in}

With $\delta=0.10$, the share of lot-draws that reach 0.90 coverage is 92 %, 91 %, 92 %, 90 % and 91 % for $m=3$, 5, 10, 20 and 30, against a target of 90 %; with $\delta=0.20$ it is 81 % and 81 % at $m=5$ and 10, against a target of 80 %. The share of lot-draws with coverage below 0.80 falls from 8 % under LotCP-S to 1 % at $m=10$. By target season the share reaching 0.90 at $m=10$ ranges over 86–98 % (50–91 % for LotCP-S), so the assurance, like the marginal coverage, is met on average over seasons and missed by a few points in the less favourable ones. Across the other predictors and the leave-one-season-out protocol the share at $m=10$ is 90–91 %. Without reference samples the assurance is not attained (88 %) and the intervals are very wide (7.19 % DMC).

The price is width. At $m=10$ the LotCP-A interval is 25 % wider than that of LotCP-S (4.30 against 3.45 % DMC) and at $m=20$ it is 21 % wider. None of the alternatives offers the property. Bias correction with the source quantile reaches 0.90 in 77 % of lot-draws at $m=10$. Target-only calibration is valid within each lot only on average over reference draws, so the realised coverage of a given draw scatters around the nominal level: the centred version reaches 0.90 in 88 % of lot-draws at $m=10$, where it is conservative and 8 % wider than LotCP-A, and in only 78 % and 71 % at $m=20$ and 30. At twenty reference samples LotCP-A is the only method examined that keeps nine lots in ten at the stated coverage, which is the regime in which the marginal comparison of Section 6.3 found no advantage for LotCP-S over target-only calibration.

On the soil data the share of lots reaching 0.90 at $m=10$ is 93 % for held-out KSSL projects, where lots are exchangeable, and 87 % and 83 % for LUCAS organic carbon and pH, where the between-campaign change of residual scale again costs a few points; for LotCP-S the corresponding shares are 70 %, 56 % and 47 % (supplementary table S13).

LotCP-S and LotCP-A answer different questions with the same calibration data. The first gives the narrowest interval that is right on average over lots; the second gives an interval that is right for the lot in hand in nine cases out of ten. For a decision that is taken lot by lot, the second statement is the one that corresponds to the risk the grower carries.


# 15. Planning the reference budget

Fig. 13 compares the width planned from the source seasons (Section 4.9) with the width realised on the lots of the target season, for the five target seasons, three predictors, five values of $m$ and both variants.

![Fig. 13. Reference-budget planning. (a) Interval width planned from past lots against the mean width realised on the lots of the following season; each point is one target season, predictor, number of reference samples and variant. (b) Planned and realised budget curves for PLS, averaged over target seasons.](figures/fig13_planning.png){width=6.3in}

The planned width is a usable forecast. Over all 150 combinations the median absolute relative difference between realised and planned width is 7 %, and the mean difference is -2 %. For PLS and LightGBM the median absolute difference is 8 % and 7 %; for the CNN it is 12 %. By target season the mean difference ranges from -21 % to 7 %: the forecast is too wide for 2017, when the calibration rested on two source seasons whose season-held-out models were weak, and within 8 % for the four later seasons (supplementary table S15). The shape of the curve is reproduced (Fig. 13b): most of the reduction in width is obtained with the first five reference samples, and beyond ten both curves flatten. The largest deviations in Fig. 13a are the CNN in 2017, where the planned width is well above the realised one. A grower or packhouse can therefore read the cost of a given precision from the calibration set before the season, separately for the average-coverage interval and for the lot-level assurance.


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
