---
title: "How many reference fruit does a valid error bar need? Lot-exchangeable few-shot conformal calibration of near-infrared dry-matter predictions across harvest seasons"
---

**[Author One]^a,\*^, [Author Two]^a^, [Author Three]^b^**

^a^ [Department, Institution, City, Country]

^b^ [Department, Institution, City, Country]

\* Corresponding author: [name], [e-mail address], [postal address]

# Abstract

Handheld near-infrared (NIR) spectrometers guide fruit harvest decisions, yet their calibrations are built on past seasons and report no error bar that holds on a new one. Using a large public mango data set (85,401 spectra, 199 harvest lots, seven seasons), we train on earlier seasons and measure the coverage of prediction intervals for dry matter content on 137 lots of later seasons. At a nominal 90 %, split conformal prediction covers 82 % and leaves 28 % of lots below 80 %; Gaussian bands, quantile forests, conformalised quantile regression, deep ensembles and Monte-Carlo dropout cover 77–84 %. Holding calibration residuals out by season restores pooled coverage but widens intervals by 37 % and still varies between 82 % and 99 % by season. We propose LotCP, a lot-exchangeable few-shot conformal calibration that corrects a new lot's bias from *m* destructively measured reference samples, rescales the score with a lot-specific scale that also uses repeated scans, and obtains the half-width by replaying the *m*-shot procedure on past lots. With 3 to 30 reference samples per lot the scale-adaptive variant covers 91–92 %, stays within 90–92 % across three predictors and two protocols, and has the best interval score for 3 to 20 samples; at 10 samples its intervals are 10 % narrower than bias correction with a source quantile and 26 % narrower than target-only calibration. Beyond 20 samples target-only calibration is equally good. The lot-specific scale drives the gain; shrinkage of the bias estimate does not.

**Keywords:** near-infrared spectroscopy; conformal prediction; uncertainty quantification; distribution shift; fruit maturity; calibration maintenance; mango

# Highlights

- Conformal intervals for mango dry matter cover 82 %, not 90 %, on later seasons.
- Deep ensembles, MC dropout and quantile models under-cover as well.
- Season-held-out calibration restores coverage only on average and at 37 % more width.
- Three to ten reference fruit per lot give near-nominal, narrower intervals.
- A lot-specific scale, not shrinkage, drives the gain of the proposed method.


# 1. Introduction

Handheld near-infrared (NIR) spectrometers are now routine tools for deciding when to harvest fruit. In mango, dry matter content (DMC) at harvest is the accepted index of eating quality, and growers scan fruit on the tree and compare the predicted DMC with a cultivar-specific specification [@walshsubedi2016; @walsh2020review]. The calibration behind such a reading is built on previous seasons and is then applied to fruit of a new season, a new orchard block, and often a different instrument unit. Three decades of work on fruit NIR spectroscopy have shown that the accuracy measured by cross-validation inside the calibration set overstates the accuracy obtained on a later, independent population [@nicolai2007; @walsh2020review]. For mango DMC this was documented with a multi-season data set: models that looked excellent in cross-validation lost accuracy on the following season, and the loss depended on the season, the cultivar and the fruit temperature [@anderson2020; @anderson2021; @sun2020].

A point estimate of DMC is therefore not enough for a harvest decision. A reading of 15.2 % against a 15 % specification means something different if the error bar is ±0.8 % than if it is ±2 %. What the user needs is a prediction interval that contains the true DMC with a stated probability, on *this* lot of fruit, and that is no wider than necessary. Current practice reports a single root-mean-square error of cross-validation or of an external validation set and, implicitly, a Gaussian band around every prediction. Recent work has started to attach uncertainty estimates to spectroscopic predictions, with Bayesian approximations for neural networks [@metz2025] and with conformal prediction [@jovic2025; @sun2026].

Conformal prediction is attractive here because it turns any point predictor into intervals with a finite-sample coverage guarantee and no distributional assumption [@vovk2022; @lei2018; @angelopoulos2023]. The guarantee, however, rests on exchangeability between the calibration data and the test data. That is the assumption a new harvest season breaks. A concurrent study reports that split-conformal intervals lose coverage when an NIR calibration is moved to another instrument [@kayaoglu2026]. Whether, and how strongly, the same happens under the biological and operational shift between harvest seasons, and what a grower can do about it at acceptable cost, has not been examined.

The practical setting offers two resources that generic remedies for distribution shift do not use. First, the data have a nested structure: scans are nested in fruit samples, samples in harvest lots (an orchard block harvested on a given date), and lots in seasons. A multi-season calibration set contains many past lots, so the lot-to-lot variation of the model error can be observed directly. Second, bias adjustment from a few reference measurements is a standard step of calibration maintenance and transfer [@fearn2001; @feudale2002]: a small number of fruit from the new population are measured destructively and used to check or adjust the model. The open questions are how many reference fruit are needed, how they should be used, and what coverage the resulting intervals then have.

This paper addresses these questions with a large public mango NIR data set (85,401 spectra, 10,560 reference samples, 199 harvest lots, seven seasons, 31 instrument units) [@mangodata]. The contributions are:

1. **A quantification of the failure.** Under a forward-chaining protocol (train on all seasons before *T*, test on the lots of season *T*) we measure the coverage of split-conformal, Gaussian, conformalised-quantile-regression, quantile-forest, deep-ensemble, Monte-Carlo-dropout and covariate-shift-weighted conformal intervals on later-season lots, for three point predictors.
2. **An analysis of the hold-out unit.** We show how coverage on the next season changes when calibration residuals are held out by sample, by lot or by season, which separates the contribution of within-season lot effects from that of between-season effects.
3. **LotCP, a lot-exchangeable few-shot conformal calibration.** LotCP instantiates hierarchical conformal prediction [@lee2023] for calibration maintenance. It corrects the lot bias by an empirical-Bayes shrinkage of the mean residual of *m* reference samples, optionally rescales the conformity score by a lot-specific scale that combines the reference residuals with the label-free variance of repeated scans (LotCP-S), and obtains the interval half-width by replaying the *m*-shot procedure on every past lot using season-held-out residuals. The half-width therefore accounts for the estimation error of the correction at the given *m*.
4. **An evaluation at the level at which decisions are made.** The unit of analysis is the harvest lot. We report lot-wise coverage, interval width and interval score as a function of the number of reference samples, with ablations, paired tests across lots, robustness to reference error, to the number of past lots, to unseen regions and cultivars, and an analysis of the lots on which the method still fails.

We do not claim a new conformal theory. The guarantee we rely on is that of hierarchical conformal prediction, and it holds only if lots are exchangeable, which seasons make doubtful. The contribution is the design of the calibration for this application, the evidence on how far the guarantee carries across real seasons, and a quantified answer to the reference-sampling question.

# 2. Related work

**Robust NIR calibrations for fruit.** Calibration robustness across seasons, growing regions, cultivars and temperatures has been pursued by enlarging and diversifying the calibration set [@anderson2020], by local and nonlinear models [@anderson2021], by temperature-robust modelling [@sun2020], by convolutional networks [@cui2018; @mishra2021; @walsh2024; @passos2023] and by semi-supervised modelling [@mishra2023]. Calibration transfer and standardisation address the related problem of instrument differences [@fearn2001; @feudale2002]. All of this work targets the point prediction and reports aggregate error statistics; none provides per-prediction intervals with stated coverage on a new season.

**Uncertainty quantification for spectroscopic models.** Model-based approaches include quantile regression forests [@meinshausen2006], deep ensembles [@lakshminarayanan2017] and Monte-Carlo dropout [@gal2016]; the latter family has been applied to mango DMC prediction with neural networks [@metz2025]. Conformal prediction has been applied to mid-infrared adulteration data, where normalised scores gave narrower intervals than absolute residuals [@jovic2025], and to NIR quantification of botanical adulterants, where aggregated and cross-validated variants were compared [@sun2026]. These studies calibrate and test within one population. The closest work to ours is the concurrent study of Kayaoğlu and Erdem, available as a code and results archive, which measures the loss of split-conformal coverage under instrument transfer on four paired-instrument data sets and the number of labelled target samples needed to restore it [@kayaoglu2026]. Our study differs in the type of shift (harvest seasons and lots rather than paired instruments), in the data structure that it exploits (many past lots), and in proposing a calibration that uses the past lots to price the few-shot correction rather than recalibrating from the target labels alone.

**Conformal prediction under distribution shift.** Weighted conformal prediction restores validity under covariate shift when the likelihood ratio between test and calibration covariates is known or estimated [@tibshirani2019]; it cannot repair a change in the conditional distribution of the residual, which is what a lot-specific bias is. Adaptive conformal inference adjusts the miscoverage level online from a stream of labelled outcomes [@gibbs2021], and non-exchangeable conformal prediction down-weights calibration points that are less relevant [@barber2023]. Cross-conformal and jackknife+ methods reuse the training data for calibration [@vovk2015; @barber2021]. For grouped data, Dunn et al. [@dunn2023] and Lee et al. [@lee2023] replace exchangeability of observations by exchangeability of groups; Lee et al. prove marginal coverage for a group-balanced split-conformal quantile (HCP) and remark that, when a few outcomes of the test group are observed, a score centred on their mean can be used. Fisch et al. [@fisch2021] calibrate few-shot predictors across exchangeable auxiliary tasks. LotCP builds directly on these results. What it adds is specific to calibration maintenance: residuals that are held out by season so that past lots look like future lots, a shrinkage rather than a plain mean correction, a score scale that uses repeated scans, and a replay of the reference-sampling protocol that handles lots of unequal size.

# 3. Research gap and questions

What exists: (i) evidence that point accuracy of mango DMC calibrations degrades on a new season; (ii) uncertainty methods for spectroscopy evaluated within one population; (iii) concurrent evidence that conformal coverage degrades under instrument transfer; (iv) hierarchical conformal theory for grouped data. What is missing is an assessment of interval coverage at the level of the harvest lot across real seasons, a calibration procedure that uses the lot structure of multi-season calibration sets together with a few reference samples, and a quantified trade-off between the number of reference samples and the width of a valid interval. This matters because the lot is the unit on which a harvest decision is taken, and because reference sampling is the only label source a grower has.

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

## 4.4 Shrinkage bias correction

Let $\bar r_{ki}$ be the mean residual of sample $i$ over its scans and $\bar r_k$ the mean of $\bar r_{ki}$ over the samples of lot $k$. From the season-held-out residuals of the $K$ source lots we estimate, by the method of moments for a one-way random-effects layout,

$$\hat\mu=\frac1K\sum_k \bar r_k,\qquad \hat\sigma^2=\frac{\sum_k\sum_i(\bar r_{ki}-\bar r_k)^2}{\sum_k (n_k-1)},\qquad \hat\tau^2=\max\Big\{0,\; \frac{1}{K-1}\sum_k(\bar r_k-\hat\mu)^2-\hat\sigma^2\,\frac1K\sum_k\frac1{n_k}\Big\}. \qquad\text{(2)}$$

For a new lot with reference set $A$, $|A|=m$, the bias is estimated by shrinking the mean reference residual $\bar r_A$ towards $\hat\mu$ [@efron1975]:

$$\hat b = \hat\mu + w_m(\bar r_A-\hat\mu),\qquad w_m=\frac{\hat\tau^2}{\hat\tau^2+\hat\sigma^2/m}, \qquad\text{(3)}$$

with $\hat b=\hat\mu$ for $m=0$. The corrected point prediction is $f(x)+\hat b$.

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

For $m=0$ and $\hat s\equiv1$, Eq. (6) is the hierarchical conformal prediction (HCP) quantile of Lee et al. [@lee2023] applied to season-held-out residuals. With $w_m=1$ and $\hat s\equiv1$ it is their mean-centred few-shot score applied to model residuals; we report this variant as "HCP-mean".

## 4.7 What is guaranteed, and what is not

Suppose the predictor and the constants $(\hat\mu,\hat\tau^2,\hat\sigma^2,e_0,\nu_0)$ are fixed, the $K_m$ calibration lots and the test lot are exchangeable, and samples are exchangeable within lots. Then the score of a random scan of a random non-reference sample of the test lot, computed with a random reference set, is hierarchically exchangeable with the calibration scores, and Theorem 1 of Lee et al. [@lee2023] gives $\mathbb{P}\{y\in C(x)\}\ge 1-\alpha$ for every $m$, with the probability taken over lots, reference draws and scans. A Monte-Carlo check of this statement under simulated exchangeable lots is part of the unit tests of the released code.

The assumptions are not met exactly in our use. (i) Calibration residuals come from season-held-out predictors, not from the deployed predictor. (ii) The constants are estimated from the calibration lots themselves. (iii) Lots of a future season are not exchangeable with past lots if the new season differs systematically; season-held-out residuals emulate such a difference but cannot guarantee that the next one is of the same size. (iv) The guarantee is marginal over lots; it does not promise the nominal coverage within each lot [@barber2021limits]. The experiments measure how much these gaps matter.

## 4.8 Computational cost

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

*With $m$ reference samples.* (a) Bias correction + source CP: the mean reference residual is subtracted and the split-conformal half-width from sample-fold residuals is kept, which combines current practice with a naive use of conformal prediction. (b) Pooled recalibration: the reference residuals are added to the source calibration set. (c) Adaptive conformal inference [@gibbs2021] run over the reference samples (step size 0.05) starting from the source quantile. (d) Target-only CP: split conformal on the reference residuals alone; it is valid within the lot but requires $m\ge 1/\alpha-1$. (e) Target-only CP, centred: as (d) with scores centred on the leave-one-sample-out mean of the other reference residuals, which removes the lot bias. (f) HCP-mean: the mean-centred hierarchical score of Lee et al. [@lee2023] on season-held-out residuals, equal to LotCP without shrinkage. (g) LotCP. (h) LotCP-S.

Methods (5)–(10) are evaluated with their own point predictions. All other methods are wrapped around the same point predictor, so differences between them are differences in calibration only.

## 5.5 Evaluation

The unit of analysis is the target lot. For every lot and every $m\in\{0,3,5,10,20,30\}$ we draw 100 random reference sets and evaluate on the scans of the remaining samples; a lot is evaluated at a given $m$ only if it has at least $m+10$ samples. Within a lot every sample has equal weight and every scan equal weight within its sample, matching Eq. (6). We report: *coverage*, the weighted share of scans whose reference value lies in the interval, averaged over draws and then over lots (lot-macro coverage); the share of lot-draws with coverage below $1-\alpha-0.10$ (*under-covered lots*); the mean interval *width*; and the Winkler *interval score* [@winkler1972; @gneiting2007], $(u-l)+\tfrac{2}{\alpha}(l-y)_+ +\tfrac{2}{\alpha}(y-u)_+$, a proper score that rewards narrow intervals and penalises misses. The nominal level is $1-\alpha=0.90$; 0.80 and 0.95 are examined in Section 9. LotCP uses $E=30$ episodes per lot.

## 5.6 Statistical analysis

Methods are compared on the same lots, so tests are paired. For each $m$ and each competing method we apply the Wilcoxon signed-rank test [@wilcoxon1945] to the per-lot differences in interval score and in absolute coverage error $|\text{coverage}-0.90|$. The test assumes that the paired differences of lots are independent and symmetric under the null; independence across lots of the same season is an approximation, and we therefore also report in how many of the five target seasons the mean difference favours the reference method. P-values are adjusted by Holm's procedure [@holm1979] within each outcome family. The effect size is the matched-pairs rank-biserial correlation [@kerby2014]. Confidence intervals for lot-macro coverage and for mean differences are 95 % percentile intervals from 2,000 bootstrap resamples of lots, stratified by season. Because the season is the top-level cluster and there are only five target seasons, per-season results are always shown alongside pooled ones.

The experimental protocol, including hypotheses, splits, methods and metrics, was written and committed to the repository before any model was trained. Deviations are listed in Section 5.7.

## 5.7 Deviations from the pre-specified protocol

(D1) LotCP-S was added after the first run on one predictor and one target season (PLS, 2018) showed that the pre-specified LotCP under-covered because the residual scale of that season's lots exceeded that of the source lots. The scale estimator of Eq. (4) was developed on source-season residuals only. Results for PLS on 2018 should therefore be read as development data for LotCP-S; the other four target seasons and the other two predictors had not been evaluated when the design was fixed. Both variants are reported everywhere. (D2) The centred target-only baseline (e) was added to give target-only calibration its strongest form. (D3) For computational reasons the CNN was trained for 20 rather than 30 epochs; lot-grouped folds were computed for one CNN seed only; and in the leave-one-season-out protocol the CNN uses one seed with season folds. These choices were made before any CNN result existed.


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

Table 3 lists the intervals that need no reference sample. Split conformal prediction with sample-grouped folds covers 0.823 of the reference values on later-season lots (95 % CI 0.787–0.855) at a nominal 0.90, and 28 % of the lots have coverage below 0.80. The Gaussian band, the quantile regression forest and conformalised quantile regression with sample folds behave similarly (coverage 0.840, 0.841 and 0.794). The deep ensemble and Monte-Carlo dropout give the narrowest intervals and the lowest coverage (0.766 and 0.775): their predictive variance reflects the training seasons, not the lot effect of a new one. Their interval score is nevertheless the best in the table, because the CNN underlying them has a lower point error than PLS (Table 2). H1 is confirmed.

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
| LotCP (m=10) | 0.984 | 0.857 | 0.922 | 0.904 | 0.912 |
| LotCP-S (m=10) | 0.957 | 0.882 | 0.902 | 0.895 | 0.914 |

Table: Table 5. Lot-macro coverage by target season (PLS, nominal 0.90).


## 6.3 Intervals with reference samples (RQ2)

Table 4 and Fig. 4 show what $m$ reference samples per lot buy. Three samples are enough to change the picture: every method that corrects the lot bias then covers at least 0.90 with intervals of about the same width as the invalid sample-fold split conformal intervals. The corrected point prediction improves accordingly: the lot-level RMSE of PLS falls from 1.36 % DMC without correction to 1.05 with three and 0.98 with ten reference samples.

| Method | m=3 | m=5 | m=10 | m=20 | m=30 |
|---|---:|---:|---:|---:|---:|
| Bias corr. + source CP | 0.921 / 3.83 / 4.96 | 0.931 / 3.83 / 4.80 | 0.938 / 3.83 / 4.68 | 0.945 / 3.82 / 4.58 | 0.941 / 3.81 / 4.64 |
| Pooled recalibration | 0.823 / 3.83 / 6.81 | 0.823 / 3.83 / 6.80 | 0.823 / 3.83 / 6.80 | 0.822 / 3.82 / 6.81 | 0.827 / 3.81 / 6.78 |
| ACI on references | 0.873 / 4.06 / 5.94 | 0.894 / 4.08 / 5.78 | 0.914 / 4.16 / 5.62 | 0.917 / 4.18 / 5.50 | 0.914 / 4.16 / 5.45 |
| Target-only CP | n/a | n/a | 0.957 / 5.64 / 6.08 | 0.931 / 4.72 / 5.39 | 0.921 / 4.53 / 5.33 |
| Target-only CP, centred | n/a | n/a | 0.956 / 4.63 / 5.12 | 0.932 / 3.58 / 4.29 | 0.921 / 3.40 / 4.25 |
| HCP-mean (LotCP w/o shrinkage) | 0.924 / 4.25 / 5.40 | 0.925 / 4.09 / 5.18 | 0.927 / 3.97 / 5.01 | 0.930 / 3.90 / 4.86 | 0.921 / 3.74 / 4.86 |
| LotCP | 0.923 / 4.18 / 5.32 | 0.925 / 4.06 / 5.16 | 0.926 / 3.97 / 5.01 | 0.930 / 3.90 / 4.86 | 0.921 / 3.74 / 4.86 |
| LotCP-S | 0.919 / 3.77 / 4.86 | 0.918 / 3.56 / 4.63 | 0.919 / 3.45 / 4.46 | 0.918 / 3.29 / 4.25 | 0.914 / 3.28 / 4.32 |

Table: Table 4. Intervals with m reference samples per lot (PLS, nominal 0.90). Each cell: lot-macro coverage / mean width / interval score. n/a: the method returns unbounded intervals at this m. ACI returned unbounded intervals in up to 10% of lot-draws; its width and score are over the finite ones.


![Fig. 4. Lot-macro coverage, mean width and interval score as a function of the number of reference samples per lot (PLS, forward chaining, 137 target lots, nominal 0.90). Dashed lines: split conformal prediction without reference samples.](figures/fig4_main.png){width=6.5in}

*Methods that do not correct the bias.* Pooling the reference residuals into the source calibration set has no visible effect (coverage 0.823 at $m=10$): a few target residuals among tens of thousands of source residuals do not move the quantile. Adaptive conformal inference over the reference samples raises coverage to 0.914 at $m=10$ but does so by widening the interval, and returns unbounded intervals in 9 % of lot-draws.

*Target-only calibration.* Split conformal prediction on the reference samples alone is valid within each lot, which shows in its tight distribution of lot-wise coverage (Fig. 5). It cannot return a bounded 90 % interval for $m<9$, and at $m=10$ it is conservative (coverage 0.956) and wide: the centred version is 34 % wider than LotCP-S. By $m=20$ the centred version reaches the interval score of LotCP-S (4.29 against 4.25) and at $m=30$ it is marginally better (4.25 against 4.31).

*Bias correction with the source quantile.* Subtracting the mean reference residual and keeping the sample-fold half-width is a strong baseline with PLS. Its coverage is above nominal (0.931–0.945) because two errors partly cancel: the sample-fold residuals contain a remnant of the lot effect, which widens the interval, and the uncertainty of the estimated bias is ignored, which should narrow it. The half-width does not depend on $m$, so the method cannot turn additional reference samples into narrower intervals, and Section 8 shows that the cancellation does not carry over to other predictors.

*LotCP and LotCP-S.* LotCP covers 0.921–0.930, somewhat above nominal, with a half-width that shrinks as $m$ grows. LotCP-S covers 0.914–0.919 for $m\ge3$ and has the lowest interval score of all methods for $m$ from 3 to 20 (Table 4). At $m=10$ its intervals are 10 % narrower than those of bias correction with the source quantile and 13 % narrower than those of LotCP. By season, its coverage at $m=10$ ranges over 0.88–0.96 (Table 5). The 2018 value is below nominal even though 2018 served as development data for the scale estimator; we return to this in Section 11.

![Fig. 5. Coverage within each of the 137 target lots (PLS, nominal 0.90, dotted line). Marginal coverage near the nominal level can coexist with many badly covered lots.](figures/fig5_lot_coverage.png){width=6.5in}

*Paired tests.* Table 7 compares the per-lot interval score of LotCP-S with its competitors. Against bias correction with the source quantile the difference is not significant at $m=3$ (Holm-adjusted p = 1.000) and is significant from $m=5$ on (p = 0.002 at $m=5$, p < 0.001 at $m=10$), with the mean difference favouring LotCP-S in all five seasons from $m=5$. Against the centred target-only method LotCP-S is better at $m=10$ (p < 0.001), marginally better at $m=20$ (p = 0.044, mean difference -0.03) and not different at $m=30$ (p = 1.000). On absolute coverage error the centred target-only method is better than LotCP-S at $m=20$ and $m=30$ (mean difference 0.014 and 0.020; all tests are in the supplementary table S6), which reflects its lot-conditional validity. The conclusion for RQ2 is therefore bounded: LotCP-S is the best of the compared methods when few reference samples are available, roughly $3\le m\le 10$, and offers no advantage over target-only calibration once 20 to 30 samples per lot can be afforded.

| LotCP-S versus | m | Lots | Mean difference | 95% CI | Holm p | Rank-biserial r | Seasons favouring LotCP-S |
|---|---:|---:|---:|---:|---:|---:|---:|
| Bias corr. + source CP | 3 | 137 | -0.10 | -0.20 to 0.00 | 1.000 | -0.15 | 4/5 |
| Bias corr. + source CP | 5 | 137 | -0.17 | -0.27 to -0.06 | 0.002 | -0.39 | 5/5 |
| Bias corr. + source CP | 10 | 137 | -0.22 | -0.32 to -0.12 | <0.001 | -0.51 | 5/5 |
| Bias corr. + source CP | 20 | 129 | -0.32 | -0.42 to -0.22 | <0.001 | -0.66 | 5/5 |
| Bias corr. + source CP | 30 | 112 | -0.32 | -0.43 to -0.21 | <0.001 | -0.66 | 5/5 |
| Target-only CP, centred | 10 | 137 | -0.66 | -0.85 to -0.50 | <0.001 | -0.83 | 5/5 |
| Target-only CP, centred | 20 | 129 | -0.03 | -0.10 to 0.07 | 0.044 | -0.31 | 4/5 |
| Target-only CP, centred | 30 | 112 | 0.06 | -0.01 to 0.17 | 1.000 | -0.01 | 1/5 |
| HCP-mean (LotCP w/o shrinkage) | 3 | 137 | -0.54 | -0.66 to -0.42 | <0.001 | -0.80 | 4/5 |
| HCP-mean (LotCP w/o shrinkage) | 5 | 137 | -0.55 | -0.68 to -0.42 | <0.001 | -0.80 | 4/5 |
| HCP-mean (LotCP w/o shrinkage) | 10 | 137 | -0.56 | -0.68 to -0.43 | <0.001 | -0.80 | 4/5 |
| HCP-mean (LotCP w/o shrinkage) | 20 | 129 | -0.61 | -0.72 to -0.48 | <0.001 | -0.84 | 5/5 |
| HCP-mean (LotCP w/o shrinkage) | 30 | 112 | -0.54 | -0.68 to -0.41 | <0.001 | -0.84 | 4/5 |
| LotCP | 3 | 137 | -0.46 | -0.57 to -0.35 | <0.001 | -0.76 | 3/5 |
| LotCP | 5 | 137 | -0.53 | -0.65 to -0.40 | <0.001 | -0.77 | 4/5 |
| LotCP | 10 | 137 | -0.56 | -0.68 to -0.43 | <0.001 | -0.81 | 4/5 |
| LotCP | 20 | 129 | -0.61 | -0.72 to -0.48 | <0.001 | -0.84 | 5/5 |
| LotCP | 30 | 112 | -0.54 | -0.68 to -0.41 | <0.001 | -0.83 | 4/5 |

Table: Table 7. Paired comparison of the per-lot interval score of LotCP-S with competing methods (Wilcoxon signed-rank test, Holm-adjusted over all comparisons of the family; negative differences favour LotCP-S).


# 7. Ablation study (RQ3)

Table 6 and Fig. 6 remove or replace one component at a time.

| Variant | m=0 | m=3 | m=10 | m=30 |
|---|---:|---:|---:|---:|
| LotCP-S | 0.894 / 5.39 / 7.26 | 0.919 / 3.77 / 4.86 | 0.919 / 3.45 / 4.46 | 0.914 / 3.28 / 4.32 |
| LotCP-S, reference scale only | 0.899 / 5.45 / 7.29 | 0.924 / 4.00 / 5.09 | 0.926 / 3.61 / 4.58 | 0.925 / 3.46 / 4.40 |
| LotCP-S, replicate scale only | 0.894 / 5.39 / 7.26 | 0.920 / 3.92 / 5.05 | 0.924 / 3.71 / 4.74 | 0.920 / 3.55 / 4.64 |
| LotCP-S, lot-fold residuals | 0.861 / 4.42 / 6.80 | 0.902 / 3.46 / 4.72 | 0.908 / 3.26 / 4.36 | 0.908 / 3.21 / 4.30 |
| LotCP | 0.899 / 5.45 / 7.29 | 0.923 / 4.18 / 5.32 | 0.926 / 3.97 / 5.01 | 0.921 / 3.74 / 4.86 |
| HCP-mean (LotCP w/o shrinkage) | 0.899 / 5.45 / 7.29 | 0.924 / 4.25 / 5.40 | 0.927 / 3.97 / 5.01 | 0.921 / 3.74 / 4.86 |
| LotCP w/o episodic quantile | 0.782 / 3.78 / 7.88 | 0.902 / 3.80 / 5.23 | 0.918 / 3.80 / 4.96 | 0.918 / 3.67 / 4.83 |
| LotCP, lot-fold residuals | 0.846 / 4.11 / 6.78 | 0.886 / 3.30 / 4.89 | 0.891 / 3.13 / 4.58 | 0.884 / 3.02 / 4.55 |
| LotCP, sample-fold residuals | 0.830 / 3.93 / 6.85 | 0.881 / 3.25 / 4.89 | 0.887 / 3.09 / 4.58 | 0.880 / 2.98 / 4.55 |
| LotCP, spectrum-pooled weights | 0.897 / 5.33 / 7.17 | 0.927 / 4.15 / 5.24 | 0.931 / 3.95 / 4.94 | 0.930 / 3.88 / 4.88 |

Table: Table 6. Ablation of LotCP components (PLS, nominal 0.90). Each cell: coverage / width / interval score.


![Fig. 6. Ablation: lot-macro coverage with bootstrap 95 % CI for m = 5 and m = 20; the interval score (IS) is printed next to each variant.](figures/fig6_ablation.png){width=6.3in}

*Scale.* The lot-specific scale is the component that matters most once $m>0$. Removing it (LotCP) raises the interval score at $m=10$ from 4.46 to 5.02. The two sources of scale information both contribute: with the reference-sample variance alone the score is 4.58, with the replicate-scan variance alone 4.74. The replicate-scan term is the only one available at $m\le1$ and costs no reference measurement.

*Fold unit.* At $m=0$, residuals held out by lot or by sample give coverage 0.846 and 0.830; season-held-out residuals are needed to reach the nominal level. With $m>0$ the picture changes. After the lot bias has been corrected, what is left to calibrate is the within-lot residual, and lot-fold residuals describe it well: LotCP on lot-fold residuals covers 0.891 at $m=10$, slightly below nominal, with narrower intervals than LotCP on season-fold residuals, which over-covers (0.926). LotCP-S on lot-fold residuals covers 0.908 with an interval score of 4.36, against 0.919 and 4.46 for season-fold residuals. The lot-fold variant of LotCP-S is therefore the more efficient one, and it is not less safe by season: its lowest per-season coverage at $m=10$ is 0.89, against 0.88 for season-fold residuals. Season-held-out residuals are thus needed without reference samples and are not needed with them. We keep the season-fold variant as the reported method because it was fixed before this comparison was made, and note that the choice costs about 6 % in width at $m=10$.

*Shrinkage.* Shrinking the bias estimate has a small effect at $m=3$ (interval score 5.32 against 5.40 for the plain mean) and none from $m=10$. The reason is visible in the variance components: the lot bias is large relative to the sample noise, so the shrinkage weight is already 0.79–0.83 at $m=3$. The part of H4 that concerns shrinkage is not supported; in this data set the plain mean of Lee et al.'s remark is sufficient.

*Episodic quantile.* Replacing the replayed quantile by the quantile of within-lot residuals centred on the true lot mean, which ignores the estimation error of the bias, gives coverage 0.902 at $m=3$ and 0.918 at $m=10$ for the location-only method, and it fails at $m=0$ (0.782). Because season-fold residuals are conservative for $m>0$, the omission is not punished in this data set. The replay is nevertheless what makes the scale-adaptive score calibratable at all, since the distribution of $|r-\hat b|/\hat s$ depends on $m$ through both estimates.

*Weighting.* Giving every scan rather than every lot the same weight changes little (0.931 against 0.926 at $m=10$), because lot sizes are fairly homogeneous here.

In summary, H4 holds for the scale component and, at $m=0$, for the fold unit. It does not hold for shrinkage, and holds only at very small $m$ for the episodic quantile of the location-only method.

# 8. Generalisation across predictors and protocols (RQ4)

Table 8 and Fig. 7 repeat the comparison for LightGBM and the CNN, and for the leave-one-season-out protocol. The seed-to-seed standard deviation of lot-macro coverage is at most 0.003 for the LotCP variants (supplementary table S7b).

| Predictor, protocol | Method | Lots | Coverage | Under-covered lots (%) | Width | Interval score |
|---|---:|---:|---:|---:|---:|---:|
| PLS, forward | Split CP (sample folds) (m=0) | 137 | 0.823 | 28 | 3.83 | 6.81 |
| PLS, forward | Split CP (season folds) (m=0) | 137 | 0.900 | 14 | 5.26 | 7.05 |
| PLS, forward | Bias corr. + source CP (m=10) | 137 | 0.938 | 5 | 3.83 | 4.68 |
| PLS, forward | Target-only CP, centred (m=10) | 137 | 0.956 | 3 | 4.63 | 5.12 |
| PLS, forward | LotCP (m=10) | 137 | 0.926 | 10 | 3.97 | 5.01 |
| PLS, forward | LotCP-S (m=10) | 137 | 0.919 | 8 | 3.45 | 4.46 |
| LightGBM, forward | Split CP (sample folds) (m=0) | 137 | 0.759 | 51 | 3.09 | 7.12 |
| LightGBM, forward | Split CP (season folds) (m=0) | 137 | 0.902 | 18 | 4.98 | 6.69 |
| LightGBM, forward | Bias corr. + source CP (m=10) | 137 | 0.882 | 19 | 3.09 | 4.60 |
| LightGBM, forward | Target-only CP, centred (m=10) | 137 | 0.957 | 3 | 4.62 | 5.03 |
| LightGBM, forward | LotCP (m=10) | 137 | 0.914 | 11 | 3.58 | 4.75 |
| LightGBM, forward | LotCP-S (m=10) | 137 | 0.912 | 8 | 3.40 | 4.41 |
| 1D-CNN, forward | Split CP (sample folds) (m=0) | 137 | 0.789 | 42 | 3.07 | 6.00 |
| 1D-CNN, forward | Split CP (season folds) (m=0) | 137 | 0.928 | 11 | 5.02 | 6.05 |
| 1D-CNN, forward | Bias corr. + source CP (m=10) | 137 | 0.909 | 12 | 3.07 | 4.03 |
| 1D-CNN, forward | Target-only CP, centred (m=10) | 137 | 0.959 | 3 | 4.11 | 4.46 |
| 1D-CNN, forward | LotCP (m=10) | 137 | 0.929 | 14 | 3.93 | 4.76 |
| 1D-CNN, forward | LotCP-S (m=10) | 137 | 0.913 | 7 | 3.06 | 3.88 |
| PLS, leave-one-season-out | Split CP (sample folds) (m=0) | 198 | 0.849 | 23 | 4.07 | 6.57 |
| PLS, leave-one-season-out | Split CP (season folds) (m=0) | 198 | 0.896 | 16 | 4.69 | 6.43 |
| PLS, leave-one-season-out | Bias corr. + source CP (m=10) | 198 | 0.949 | 3 | 4.07 | 4.79 |
| PLS, leave-one-season-out | Target-only CP, centred (m=10) | 198 | 0.957 | 3 | 4.63 | 5.11 |
| PLS, leave-one-season-out | LotCP (m=10) | 198 | 0.908 | 12 | 3.36 | 4.57 |
| PLS, leave-one-season-out | LotCP-S (m=10) | 198 | 0.905 | 8 | 3.23 | 4.34 |
| 1D-CNN, leave-one-season-out | Split CP (season folds) (m=0) | 198 | 0.923 | 11 | 4.34 | 5.39 |
| 1D-CNN, leave-one-season-out | LotCP (m=10) | 198 | 0.914 | 11 | 3.01 | 4.00 |
| 1D-CNN, leave-one-season-out | LotCP-S (m=10) | 198 | 0.908 | 6 | 2.87 | 3.75 |

Table: Table 8. Generalisation across point predictors and protocols (nominal 0.90). LightGBM and CNN under forward chaining: metrics averaged over three seeds within lot.


![Fig. 7. Lot-macro coverage of LotCP and LotCP-S for three point predictors and two protocols (nominal 0.90).](figures/fig7_generalisation.png){width=6.5in}

The failure of sample-fold split conformal prediction is larger for the more flexible predictors: coverage is 0.759 for LightGBM and 0.789 for the CNN, against 0.823 for PLS, because flexible models absorb more of the lot effects of their training lots. For the same reason, bias correction with the source quantile, which over-covers with PLS, under-covers with LightGBM (0.882 at $m=10$) and sits at 0.909 with the CNN. Its coverage depends on how strongly the predictor fits its training lots, which the user does not control. LotCP-S covers 0.912 and 0.913 at $m=10$ with these predictors, and 0.905 and 0.908 under leave-one-season-out with PLS and the CNN. Across the five predictor–protocol combinations its coverage at $m=10$ stays within 0.905–0.919. With the CNN, whose point error is lowest, LotCP-S at $m=10$ gives a mean width of 3.06 % DMC, that is, about ±1.5 % DMC.

# 9. Robustness and sensitivity (RQ4)

| Condition | m=0 | m=5 | m=10 | m=20 |
|---|---:|---:|---:|---:|
| Main setting | 0.894 / 5.39 | 0.918 / 3.56 | 0.919 / 3.45 | 0.918 / 3.28 |
| Reference error SD 0.25 % DMC | 0.894 / 5.39 | 0.918 / 3.59 | 0.920 / 3.48 | 0.920 / 3.33 |
| Reference error SD 0.5 % DMC | 0.894 / 5.39 | 0.919 / 3.68 | 0.923 / 3.57 | 0.928 / 3.47 |
| Provider-flagged outliers removed | 0.897 / 5.24 | 0.921 / 3.49 | 0.920 / 3.31 | 0.920 / 3.18 |
| 10 past lots for calibration | 0.975 / 8.74 | 0.988 / 6.71 | 0.989 / 6.32 | 0.996 / 14.30 |
| 20 past lots for calibration | 0.910 / 5.70 | 0.945 / 4.04 | 0.946 / 3.84 | 0.949 / 3.79 |
| 40 past lots for calibration | 0.902 / 5.52 | 0.929 / 3.72 | 0.929 / 3.55 | 0.931 / 3.47 |
| 80 past lots for calibration | 0.895 / 5.43 | 0.922 / 3.61 | 0.924 / 3.49 | 0.920 / 3.32 |
| 5 episodes per lot | 0.894 / 5.39 | 0.918 / 3.56 | 0.921 / 3.45 | 0.920 / 3.35 |
| 10 episodes per lot | 0.894 / 5.39 | 0.917 / 3.55 | 0.920 / 3.44 | 0.919 / 3.33 |
| 100 episodes per lot | 0.894 / 5.39 | 0.918 / 3.56 | 0.920 / 3.44 | 0.921 / 3.35 |
| Fixed pseudo-count ν₀ = 5 | 0.894 / 5.39 | 0.922 / 3.61 | 0.922 / 3.46 | 0.919 / 3.31 |
| Fixed pseudo-count ν₀ = 20 | 0.894 / 5.39 | 0.922 / 3.70 | 0.924 / 3.54 | 0.923 / 3.37 |
| Fixed pseudo-count ν₀ = 80 | 0.894 / 5.39 | 0.923 / 3.77 | 0.924 / 3.64 | 0.924 / 3.49 |
| Source: two preceding seasons only | 0.891 / 6.42 | 0.914 / 4.39 | 0.917 / 4.29 | 0.918 / 3.99 |
| Unseen growing region | 0.908 / 5.15 | 0.912 / 3.37 | 0.912 / 3.26 | 0.913 / 3.19 |
| Unseen cultivar | 0.911 / 4.83 | 0.906 / 3.26 | 0.907 / 3.16 | 0.905 / 3.10 |

Table: Table 9. Robustness and sensitivity of LotCP-S (PLS, nominal 0.90). Each cell: lot-macro coverage / mean width.


![Fig. 8. Robustness of LotCP-S coverage (PLS, nominal 0.90): (a) Gaussian error added to the reference values of the m reference samples; (b) number of past lots available for calibration; (c) other source–target shifts.](figures/fig8_robustness.png){width=6.5in}

*Error in the reference values.* Oven-drying has its own error, and the $m$ reference values carry it. Adding Gaussian error with a standard deviation of 0.25 or 0.5 % DMC to the reference samples at deployment (not to the calibration lots) leaves coverage at or slightly above nominal (0.923 at $m=10$ for 0.5 % DMC) and widens the intervals by 4 % (Table 9). The noisier references inflate the estimated lot scale, which errs on the conservative side.

*Outlier screening.* Removing the scans flagged by the data provider from calibration and evaluation leaves coverage unchanged (0.920) and narrows the intervals by 4 %.

*Number of past lots.* With only 10 past lots the lot-balanced quantile is close to the largest calibration score and the intervals are very wide; with 20 lots coverage is 0.946 and with 40 lots 0.929, at widths 12 % and 3 % above those obtained with all lots. The method is always conservative when lots are few, which follows from the $1/(K_m+1)$ mass at infinity in Eq. (6), and some 40 past lots are needed before the conservatism becomes small.

*Tuning constants.* The number of episodes (5 to 100) and the pseudo-count of the scale estimate (5 to 80) change coverage by less than 0.002 and 0.006 respectively.

*Nominal level.* Table 10 gives the results for nominal levels 0.80 and 0.95. The pattern is the same: sample-fold split conformal prediction under-covers and LotCP-S with $m\ge5$ covers slightly above the nominal level.

| Nominal | Method | Coverage | Width |
|---|---:|---:|---:|
| 0.80 | Split CP (sample folds) (m=0) | 0.716 | 2.94 |
| 0.80 | Split CP (season folds) (m=0) | 0.820 | 3.92 |
| 0.80 | Target-only CP, centred (m=20) | 0.832 | 2.58 |
| 0.80 | LotCP-S (m=5) | 0.832 | 2.69 |
| 0.80 | LotCP-S (m=20) | 0.835 | 2.55 |
| 0.90 | Split CP (sample folds) (m=0) | 0.823 | 3.83 |
| 0.90 | Split CP (season folds) (m=0) | 0.900 | 5.26 |
| 0.90 | Target-only CP, centred (m=20) | 0.932 | 3.58 |
| 0.90 | LotCP-S (m=5) | 0.918 | 3.56 |
| 0.90 | LotCP-S (m=20) | 0.918 | 3.29 |
| 0.95 | Split CP (sample folds) (m=0) | 0.889 | 4.63 |
| 0.95 | Split CP (season folds) (m=0) | 0.940 | 6.78 |
| 0.95 | Target-only CP, centred (m=20) | 0.981 | 5.54 |
| 0.95 | LotCP-S (m=5) | 0.962 | 4.54 |
| 0.95 | LotCP-S (m=20) | 0.963 | 4.13 |

Table: Table 10. Other nominal levels (PLS, forward chaining).


*Other shifts.* When only the two seasons before the target are used as source, LotCP-S still covers 0.917 at $m=10$, with wider intervals (4.29 % DMC) because fewer and less diverse past lots are available. When a whole growing region or a whole cultivar is held out, coverage at $m=10$ is 0.912 and 0.907. In these two protocols the source contains all seasons, so they test a region or cultivar shift without a season shift.

# 10. Computational analysis (RQ5)

| Component | Time | Per 1000 scans at deployment |
|---|---:|---:|
| PLS fit (final model) | 1.1 s | 6.6 ms |
| LightGBM fit | 2.0 s | 11.2 ms |
| 1D-CNN fit (20 epochs) | 147.6 s | 58.3 ms |
| LotCP calibration, m = 10 | 0.5 s | < 0.1 ms (one bias, one scale per lot) |
| LotCP-S calibration, m = 10 | 2.1 s | < 0.1 ms (one bias, one scale per lot) |
| LotCP-S calibration, m = 30 | 1.2 s | < 0.1 ms (one bias, one scale per lot) |

Table: Table 11. Computing time on a 4-core CPU without GPU (mean over target seasons; CNN fits used one thread each).


The cost of the method is dominated by the season-held-out fits, one per source season, which are done once when the calibration is built (Table 11). The episodic calibration itself takes about 2.1 s for 187 past lots and 30 episodes, and the deployment step is a bias and a scale per lot, which is negligible on the embedded processor of a handheld instrument. The relevant cost is the number of destructive reference measurements. Fig. 4 expresses the trade-off: with LotCP-S and PLS, three reference samples per lot give a mean width of 3.76 % DMC, ten give 3.45, and thirty give 3.28; most of the gain is obtained with the first five to ten samples.

# 11. Error analysis (RQ5)

![Fig. 9. Error analysis at m = 10 (PLS). (a) Lot coverage against the absolute lot bias. (b) Lot coverage against the ratio of the lot's residual standard deviation to the prior scale. (c) Coverage by reference DMC range.](figures/fig9_error_analysis.png){width=6.5in}

We examined coverage at the level of the lot and of the scan for $m=10$ (Fig. 9). Of the 137 target lots, 38 have coverage below 0.80 under sample-fold split conformal prediction, 13 under LotCP and 4 under LotCP-S. For split conformal prediction, lot coverage is governed by the absolute lot bias (Spearman correlation -0.79). After bias correction the bias no longer matters much, and the remaining failures are lots whose residual spread exceeds what past lots suggest: the correlation between lot coverage and the ratio of the lot's residual standard deviation to the prior scale is -0.95 for LotCP and -0.84 for LotCP-S. The scale estimate of LotCP-S reduces the number of badly covered lots but cannot identify a wide lot reliably from ten reference samples and the repeated scans; the lot with the lowest coverage has a residual spread of 2.2 times the prior scale.

By subgroup, LotCP-S coverage is 0.93 for fruit at the green stage and 0.90 for fruit at the ripening stage; 0.91, 0.90 and 0.89 for the low, medium and high fruit-temperature classes; 0.92 for instrument units present in the source seasons and 0.92 for units that are new in the target season; and 0.91 and 0.96 for cultivars present in and absent from the source seasons. The lower coverage at the ripening stage is in line with the finding of the data set's authors that physiological stage affects model performance more than cultivar, season or region [@anderson2020]. Among cultivars the lowest coverage is 0.85 for Keitt. Scans carrying the provider's first outlier flag are covered at 0.80 (0.50 under sample-fold split conformal prediction). Coverage is lower at the extremes of the DMC range (Fig. 9c), a known limitation of scores that do not adapt to the predicted value. These figures are a reminder that the guarantee is marginal: a lot of ripening fruit, or a lot measured with atypical scatter, can be covered below the nominal level even when coverage is nominal on average.


# 12. Discussion

**What the user of a handheld instrument should take from this.** An error bar derived from the calibration set, by cross-validation, by a conformal quantile on held-out samples or by the predictive variance of a neural network, describes the past lots. On the lots of a later season it was too narrow in every one of the five seasons we could test and for every predictor. The size of the shortfall, six to fourteen coverage points at a nominal 90 % depending on the method and the predictor, is large enough to matter for a decision against a specification, and it is concentrated in a minority of lots that are covered very badly (Fig. 5).

**Without reference samples there is no cheap repair.** Season-held-out calibration is the honest label-free option and should replace sample-fold calibration when intervals are quoted for a future season. It restores coverage on average, at the price of intervals about a third wider, and its per-season coverage still ranged from 0.82 to 0.99. This is not a defect of the procedure. With four to six past seasons there is little information about how different the next one will be, and no reweighting of unlabelled spectra recovers a bias in the residual.

**A few reference samples are worth more than any modelling choice we tried.** Three destructive measurements per lot moved every bias-correcting method to at least nominal coverage and brought the width back to that of the invalid intervals. This supports, with coverage figures, the long-standing practice of checking a calibration against a few fruit of the new population. LotCP-S then answers the follow-up question of how to turn those samples into the narrowest interval that remains valid: it was the best of the compared methods for 3 to 20 samples per lot with PLS, its coverage was stable across predictors where that of the common bias-correction shortcut was not, and it converts additional reference samples into narrower intervals. When 20 to 30 samples per lot are available, calibration on those samples alone is as good and has the stronger, lot-conditional guarantee; the past lots then add nothing.

**Which parts of the method earn their place.** The ablation gives a sober answer. The lot-specific scale and, without reference samples, the season-level hold-out carry the result. Empirical-Bayes shrinkage of the bias, which motivated the design, is immaterial here because lot biases are large compared with the noise of a sample mean. Season-held-out residuals are essential without reference samples but not with them: once the bias is corrected, lot-fold residuals gave slightly narrower intervals at coverage no lower by season, and a practitioner who always collects reference samples can use them and save the season-wise refits.

**Relation to concurrent work.** Kayaoğlu and Erdem [@kayaoglu2026] report that split conformal coverage is lost under instrument transfer and quantify the labelled target samples needed to restore it. Our findings for harvest seasons agree in direction. The settings differ in that a multi-season calibration set contains many past lots, which lets the few-shot correction be calibrated before the new lot is seen.

**Practical procedure.** (1) Build the calibration with season-grouped cross-validation and store the season-held-out residuals with their lot and sample identifiers. (2) For a new lot, scan the fruit, with repeated scans where possible, and measure 5 to 10 randomly chosen fruit destructively. (3) Report $f(x)+\hat b\pm \hat q_m\hat s$. (4) After the season, add the lot to the calibration set.

# 13. Limitations

*One data set, one commodity, one instrument family.* All results come from one public data set of mango fruit scanned with handheld units of one model in two Australian regions. We know of no other public NIR data set with a comparable lot and season structure, so the generality of the numbers to other fruit, attributes and instruments is untested. The qualitative mechanism, lot effects that are invisible to within-lot calibration, is not specific to mango.

*Few seasons.* Five target seasons are a small sample at the level that matters most. Lot-level confidence intervals and tests treat lots within a season as independent, which they are not entirely; per-season results are reported for that reason, and the season-to-season range of coverage should be read as the realistic uncertainty.

*Marginal guarantee and approximate assumptions.* The guarantee of Section 4.7 is marginal over lots and assumes exchangeable lots. Lots of ripening fruit, of some cultivars and with unusually large scatter were covered below the nominal level. The calibration residuals come from season-held-out models rather than from the deployed model, which made the method conservative when only two source seasons were available.

*Reference sampling.* We assume that reference samples are drawn at random from the lot and that their reference values are as accurate as those of the calibration set. Sampling only the fruit that is easy to reach would bias the correction. In the data set a reference sample is a tissue sample with repeated scans; in an orchard the reference fruit would be scanned on the tree before being picked.

*Protocol deviation.* The scale-adaptive variant was designed after inspecting one predictor on one target season. The other seasons and predictors support it, but it was not pre-specified.

*Scores.* The score does not adapt to the predicted DMC, and coverage was lower at the extremes of the DMC range. One-sided bounds, which are what a minimum-DMC specification needs, were not studied.

*Details taken from the data description.* The measurement geometry and reference method are described here as in the publications that accompany the data set; we did not collect the data, and we interpret the file's "population" field as a harvest lot following those publications.

# 14. Conclusion

Prediction intervals for mango dry matter content that are calibrated inside the training seasons, by any of the nine procedures we tested, do not keep their nominal coverage on the lots of a later season. Calibrating on season-held-out residuals repairs coverage on average but with much wider intervals and substantial variation between seasons. Three to ten destructively measured reference fruit per lot, used through a lot-exchangeable conformal calibration with a lot-specific scale, give intervals that cover close to the nominal level across predictors and are narrower than those of the alternatives; with twenty or more reference fruit, calibration on those fruit alone is sufficient. The number of reference fruit, more than the choice of model, determines how informative a valid error bar can be.

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

# Appendix A. Supplementary material

Supplementary tables S1–S9 (complete machine-generated result tables, including all paired tests and per-seed results), figure S1 and the pre-specified protocol with its deviation log accompany this article.

# References

::: {#refs}
:::
