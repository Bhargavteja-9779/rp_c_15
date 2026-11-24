---
title: "Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons"
---

**P N Bhargav Teja^a^, Ragavan K^a,\*^**

^a^ [Department, Institution, City, Postal code, Country]

\* Corresponding author: Ragavan K, [e-mail address], [postal address]

# Abstract

A handheld near-infrared (NIR) reading of mango dry matter content (DMC) supports a harvest decision only if its error is known for the lot being picked, yet calibration error bars come from past seasons. Predicting each season of a public mango data set (199 harvest lots, seven seasons) from earlier seasons, standard error bars at a nominal 90 % (conformal, quantile-model, deep-ensemble, Monte-Carlo-dropout) covered 77–84 % of the reference values on 137 later-season lots. We propose a risk-aware workflow: a few fruit per lot are tested destructively, a few-shot conformal calibration (LotCP) corrects the lot bias and scale and gives every fruit a lower bound with a coverage guarantee, and fruit are harvested when the bound meets the specification at a level set by the cost ratio of the two errors. With 3–30 reference fruit, coverage was 91–92 %, and a lot-level variant kept 92 % of lots at the stated coverage. In a retrospective harvest simulation at 15 % DMC, immature fruit among those accepted fell from 13 % with point predictions to 1 % with ten reference fruit, and premature lot harvests roughly halved at an unchanged delay rate. Under assumed cost ratios, expected cost fell by 29–71 % relative to point decisions. A planner forecasts the error-bar width for each number of reference fruit (median error 7 %). In a pre-registered confirmation on an untouched handheld-NIR soil library, the lot-level guarantee held (95 vs 88 % of lots); an efficiency gain over simple bias correction did not.

**Keywords:** near-infrared spectroscopy; harvest decision; fruit maturity; dry matter; conformal prediction; uncertainty quantification; decision support

# Highlights

- Standard NIR error bars for mango dry matter under-cover on later harvest seasons.
- A few reference fruit per lot restore calibrated, lot-level error bars.
- Calibrated lower bounds cut immature fruit among those harvested from 13 % to 1 %.
- Pre-registered test on untouched data confirmed the lot-level guarantee.
- A cost-based confidence level turns the error bar into a harvest decision.


# 1. Introduction

Handheld near-infrared (NIR) spectrometers are now a routine tool for deciding when to harvest fruit. In mango, dry matter content (DMC) at harvest is the accepted index of eating quality: fruit picked below a cultivar-specific DMC does not ripen to an acceptable eating quality, and growers therefore scan fruit on the tree and compare the predicted DMC with a specification before a block is picked [@walshsubedi2016; @anderson2017; @walsh2020review]. Every such reading feeds four practical questions. Is this fruit, or this block, mature enough to harvest? Can the instrument's prediction be trusted this season? How many fruit should be cut and oven-dried to check the instrument before its readings are acted on? And how can immature fruit be kept out of the harvest without holding back fruit that is ready?

The difficulty is that the calibration behind the reading is built on previous seasons and then applied to a new season, a new orchard block and often a different instrument unit. Three decades of work on fruit NIR spectroscopy show that accuracy estimated within the calibration set overstates the accuracy obtained on a later, independent population [@nicolai2007; @walsh2020review]. For mango DMC this was documented on a multi-season data set: models that looked excellent in cross-validation lost accuracy on the following season, by an amount that depended on season, cultivar and fruit temperature [@anderson2020; @anderson2021; @sun2020]. A reading of 15.2 % against a 15 % specification then supports a harvest only if its error bar is known to be small for *this* lot. Current practice reports a single root-mean-square error of cross-validation or of a past validation set and, implicitly, the same Gaussian band around every prediction.

Conformal prediction turns any point predictor into intervals with a finite-sample coverage guarantee and no distributional assumption [@vovk2022; @lei2018; @angelopoulos2023], and it has begun to be used for spectroscopic quantification [@jovic2025; @sun2026]. Its guarantee rests on exchangeability between calibration and test data, which is exactly the assumption a new harvest season breaks; a concurrent study reports the corresponding loss of coverage under transfer between NIR instruments [@kayaoglu2026]. Two features of the orchard setting offer a way out that generic remedies for distribution shift do not use. First, the data are nested: scans within fruit, fruit within harvest lots (an orchard block picked on one date), lots within seasons, so a multi-season calibration set contains many past lots in which the lot-to-lot variation of the model error can be observed. Second, checking a calibration against a few destructively measured fruit of the new population is already part of calibration maintenance [@fearn2001; @feudale2002]. What is missing is a procedure that turns those few reference fruit into an error bar with a stated coverage, a rule that turns the error bar into a harvest decision, and an answer to how many reference fruit are worth taking.

This paper develops and evaluates such a risk-aware harvest-decision workflow (Fig. 1). The grower scans the fruit of a lot with a handheld NIR instrument, the calibration predicts DMC, *m* fruit are tested destructively, and a few-shot conformal calibration (LotCP) corrects the lot bias and scale and returns a lower bound for every scanned fruit. A fruit, or a lot, is harvested when the lower bound meets the specification, and otherwise it waits or is re-tested; the confidence level of the bound is set from the relative cost of the two possible errors, and the number of reference fruit is chosen beforehand with a planner computed from past lots. We evaluate the workflow retrospectively on a large public mango NIR data set (85,401 spectra, 10,560 reference samples, 199 harvest lots, seven seasons, 31 instrument units) [@mangodata] under forward chaining, so that every season is predicted only from the seasons before it, and we repeat the central comparisons on two public soil spectral libraries [@safanelli2025]. The evaluation is a simulation on historical data; it shows what the workflow would have done, not what it has done in an orchard.

![Fig. 1. Risk-aware harvest workflow. Before the season, past lots are used to calibrate the few-shot correction and to plan the number of reference fruit. In the orchard, fruit of a new lot are scanned, m of them are tested destructively, and each fruit receives a calibrated lower bound that is compared with the dry-matter specification.](figures/fig1_workflow.png){width=6.5in}

Our first idea did not work. We expected that correcting each new lot's bias from a few reference fruit, with the correction shrunk towards past lots and its error calibrated on past lots, would be enough. On the first season we examined it was not: coverage was 0.86 at a nominal 0.90 with ten reference fruit, because lots of the new season differed from past lots in the spread of their errors, not only in their offset. The spread could be estimated in part without any reference value, from the scatter between repeated scans of the same fruit, and adding it repaired coverage. A second component we had designed in, the shrinkage of the bias towards past lots, later failed outright on soil spectra from a new survey campaign and was removed. And when we confirmed the frozen method on a data set we had not used before, the efficiency gain over a simple bias correction did not reach significance, whereas the lot-level guarantee did. Section 3 summarises these failures, because they define what the method can and cannot claim.

The contributions are:

1. **Evidence that standard error bars fail across seasons.** Split-conformal, Gaussian, conformalised-quantile-regression, quantile-forest, deep-ensemble, Monte-Carlo-dropout and covariate-shift-weighted conformal intervals are audited lot by lot on later seasons for three point predictors; the same audit on soil spectra shows a larger failure across survey campaigns.
2. **A few-shot calibration with stated guarantees.** LotCP-S corrects the lot bias from *m* reference fruit, rescales the conformity score by a lot-specific scale that also uses the label-free variance of repeated scans, and obtains the half-width by replaying the *m*-shot procedure on past lots with season-held-out residuals. LotCP-A calibrates instead on the lot-wise quantiles of past lots so that the stated share of fruit is covered within the lot for nine lots in ten. Both guarantees are stated and proved for random reference sets, three nested levels and lots of unequal size (Appendix A).
3. **A harvest-decision simulator and an economic analysis.** Fruit-level and lot-level harvest decisions against a DMC specification are simulated on 137 later-season lots, and their expected cost is evaluated under explicitly assumed cost ratios, with the confidence level of the bound derived from those costs.
4. **A reference-sampling planner.** From past lots alone, the calibration forecasts the error-bar width and lot-level coverage obtainable with 3, 5, 10 or 20 reference fruit, and the cost analysis gives the number of reference fruit that minimises expected cost for a given lot size.
5. **A decision-support prototype.** A small command-line tool takes the NIR predictions of a lot, the reference values and the specification, and returns per-fruit lower bounds, a lot recommendation and the planner output.

The coverage guarantees build on hierarchical conformal prediction [@lee2023]; what is new is the calibration procedure for this problem, its lot-level variant, the decision rule, the planner and the evidence on how far the guarantees carry across real seasons and survey campaigns. The guarantees require lots to be exchangeable, which seasons make doubtful, and a central aim of the experiments is to measure the consequences.

# 2. Related work

**Robust NIR calibrations for fruit.** Calibration robustness across seasons, growing regions, cultivars and temperatures has been pursued by enlarging and diversifying the calibration set [@anderson2020], by local and nonlinear models [@anderson2021], by temperature-robust modelling [@sun2020], by convolutional networks [@cui2018; @mishra2021; @walsh2024; @passos2023] and by semi-supervised modelling [@mishra2023]. Calibration transfer and standardisation address the related problem of instrument differences [@fearn2001; @feudale2002]. All of this work targets the point prediction and reports aggregate error statistics; none provides per-prediction intervals with stated coverage on a new season.

**Uncertainty quantification for spectroscopic models.** Model-based approaches include quantile regression forests [@meinshausen2006], deep ensembles [@lakshminarayanan2017] and Monte-Carlo dropout [@gal2016]; the latter family has been applied to mango DMC prediction with neural networks [@metz2025]. Conformal prediction has been applied to mid-infrared adulteration data, where normalised scores gave narrower intervals than absolute residuals [@jovic2025], and to NIR quantification of botanical adulterants, where aggregated and cross-validated variants were compared [@sun2026]. These studies do not address a shift between harvest seasons or lots. The closest work to ours is the concurrent study of Kayaoğlu and Erdem, available as a code and results archive, which measures the loss of split-conformal coverage under instrument transfer on four paired-instrument data sets and the number of labelled target samples needed to restore it [@kayaoglu2026]. Our study differs in the type of shift (harvest seasons and lots rather than paired instruments), in the data structure that it exploits (many past lots), and in proposing a calibration that uses the past lots to price the few-shot correction rather than recalibrating from the target labels alone. Related ideas in other fields support this positioning: few-shot conformal calibration meta-learned across tasks [@park2024metaxb], class-conditional recalibration at a new hospital from a few local labels with shrinkage towards the home site [@nasir2026], an audit of conformal coverage under shift with a prospective label budget for recalibration [@moussa2026], evidence that recalibration parameters often fail to transfer under shift [@neyigapula2026], and shift-aware conformal classification of reflectance spectra [@khairbek2026]. None of them addresses a regression calibration maintained across harvest seasons with many past lots available, and robust point models for mango dry matter across cultivars and years continue to be developed [@ma2026].

**Conformal prediction under distribution shift.** Weighted conformal prediction restores validity under covariate shift when the likelihood ratio between test and calibration covariates is known or estimated [@tibshirani2019]; it cannot repair a change in the conditional distribution of the residual, which is what a lot-specific bias is. Adaptive conformal inference adjusts the miscoverage level online from a stream of labelled outcomes [@gibbs2021], and non-exchangeable conformal prediction down-weights calibration points that are less relevant [@barber2023]. Cross-conformal and jackknife+ methods reuse the training data for calibration [@vovk2015; @barber2021]. For grouped data, Dunn et al. [@dunn2023] and Lee et al. [@lee2023] replace exchangeability of observations by exchangeability of groups; Lee et al. prove marginal coverage for a group-balanced split-conformal quantile (HCP) and remark that, when a few outcomes of the test group are observed, a score centred on their mean can be used. Fisch et al. [@fisch2021] calibrate few-shot predictors across exchangeable auxiliary tasks. LotCP builds directly on these results. What it adds is specific to calibration maintenance: residuals that are held out by season so that past lots look like future lots, a score scale that uses the reference residuals and repeated scans, and a replay of the reference-sampling protocol that handles lots of unequal size.

# 3. Research gap and questions

What exists: (i) evidence that point accuracy of mango DMC calibrations degrades on a new season; (ii) uncertainty methods for spectroscopy evaluated within one population; (iii) concurrent evidence that conformal coverage degrades under instrument transfer; (iv) hierarchical conformal theory for grouped data. What is missing is an assessment of interval coverage at the level of the harvest lot across real seasons, a calibration procedure that uses the lot structure of multi-season calibration sets together with a few reference samples, and a quantified trade-off between the number of reference samples and the width of a valid interval. This matters because the lot is the unit on which a harvest decision is taken, and because reference sampling is the only label source a grower has.

The work is positioned as follows.

- *Robust fruit calibrations* [@anderson2020; @anderson2021; @mishra2023] improve the point prediction across seasons. This paper adds per-prediction intervals whose coverage is measured on later seasons, lot by lot.
- *Uncertainty for spectroscopic models* has been proposed with Bayesian approximations for mango networks [@metz2025] and with conformal prediction for food and botanical quantification [@jovic2025; @sun2026]. This paper audits such estimates lot by lot against a nominal level on later seasons and campaigns, and shows that those calibrated within the training population fail there.
- *Conformal prediction under instrument transfer* [@kayaoglu2026] measures the loss of coverage between paired instruments and the labelled samples needed to restore it by recalibration. This paper treats seasons, lots and campaigns, and uses past lots to calibrate the few-shot correction before the new lot is seen.
- *Hierarchical and few-shot conformal prediction* [@lee2023; @dunn2023; @fisch2021; @park2022] provides the theory for grouped data. This paper supplies a calibration procedure for calibration maintenance (bias and scale from reference samples and repeated scans, season-held-out residuals, replay of the reference protocol), a lot-level assurance, a sampling planner, and their empirical limits.
- *Bias adjustment and spiking* [@fearn2001; @feudale2002; @guerrero2010; @guerrero2014] are the maintenance practices in use. This paper gives them an interval with stated coverage and compares them directly.

*What did not work first, and why.* Four results from our own work shaped the method and the claims (journal entries in the released repository). (i) The pre-specified location-only correction under-covered on the first season examined, because the residual scale of new lots exceeded that of past lots; a lot-specific scale was added, partly estimated from repeated scans (protocol deviation D1). (ii) Empirical-Bayes shrinkage of the bias estimate, part of the original design, gave no benefit on mango and failed on the soil survey's campaign shift (coverage 0.70 instead of 0.87 for pH at five reference samples); it was removed. (iii) The point predictor we used throughout, PLS after standard normal variate correction, proved 0.35 % DMC worse in RMSEP than the published PLS recipe on the published split (Section 6.1); the interval conclusions were therefore re-checked with the published recipe. (iv) In the pre-registered confirmation on a data set not used during development, the lot-level assurance was confirmed but the efficiency gain of LotCP-S over a simple bias correction was not (Section 7.3).

We ask five questions. RQ1: how far does the coverage of standard error bars fall on later-season lots, and which hold-out unit for calibration residuals repairs it? RQ2: with *m* reference fruit per lot, what coverage, width and lot-level assurance does the few-shot calibration achieve relative to strong alternatives? RQ3: what does this change in fruit-level and lot-level harvest decisions, and at what expected cost under plausible cost ratios? RQ4: can the error-bar width for a given number of reference fruit be planned before the season? RQ5: do the findings hold for other predictors, protocols, nominal levels, noisy reference values, unseen regions and cultivars, and soil spectra, and which components of the method matter?


# 4. Proposed method

## 4.1 Setting and notation

Data are nested. A *lot* $k$ is a set of fruit harvested from one orchard block on one date; it contains $n_k$ reference *samples* $i$ (a piece of fruit tissue with one oven-dried DMC value $y_{ki}$), and sample $i$ has $J_{ki}\ge 1$ *scans* with spectra $x_{kij}$. Lots are nested in seasons. A point predictor $f$ maps a spectrum to a DMC estimate, and $r_{kij}=y_{ki}-f(x_{kij})$ is the residual of a scan. For a new lot the user scans all fruit of interest and measures $m\ge 0$ randomly chosen reference samples destructively. For each remaining scan we want an interval $C(x)$ such that $\mathbb{P}\{y\in C(x)\}\ge 1-\alpha$. Fig. 1 shows where the procedure developed below enters the harvest workflow.

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

The corrected point prediction is $f(x)+\hat b$. The protocol originally specified an empirical-Bayes shrinkage of this mean towards $\hat\mu$ [@efron1975], $\hat b=\hat\mu+w_m(\bar r_A-\hat\mu)$ with $w_m=\hat\tau^2/(\hat\tau^2+\hat\sigma^2/m)$. It is evaluated as an ablation ("+ shrinkage"). We do not use it in the reported method, because it brought no benefit on the mango data and is unsafe when the new population is shifted by more than the between-lot variation seen in the past (Sections 11 and 13). The variance components of Eq. (2) remain in use for the scale estimate below.

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

The episodic replay has a by-product that is useful in its own right. For every $m$ it yields, from past lots alone, the multiplier $\hat q_m$ (or $\hat q_m^{A}$) and the average lot scale $\bar s_m$ over the replayed episodes, and therefore a *planned width* $2\hat q_m\bar s_m$: the interval width that the user should expect in the coming season if $m$ reference samples are taken per lot. The curve of planned width against $m$ can be drawn before any fruit of the new season is scanned, and it turns the choice of the number of reference samples into an explicit trade between laboratory effort and the precision of the error bar. Section 9 compares planned and realised widths.

## 4.10 Computational cost

Calibration needs one additional model fit per source season, which is done once and offline. The episodic quantile costs $O(K E N)$ score evaluations for $N$ scans per lot. At deployment the method computes two means and one variance per lot.

## 4.11 From a calibrated bound to a harvest decision

Let $t$ be the minimum DMC a fruit must reach. The grower can make two errors: accepting a fruit whose true DMC is below $t$, at cost $c_I$ (an immature fruit enters the harvest), or withholding a fruit whose DMC is at least $t$, at cost $c_D$ (a ready fruit is left for a later pass or re-tested). If the probability that a fruit is below specification were known, the expected cost would be minimised by accepting it whenever that probability is at most $\alpha^\ast=c_D/(c_I+c_D)$. A lower bound $L(x)$ with $\mathbb{P}\{y<L(x)\}\le\alpha^\ast$ therefore yields the rule

$$\text{harvest if } L_{\alpha^\ast}(x)\ge t,\qquad \text{otherwise wait or re-test}, \qquad\text{(9)}$$

with $L_{\alpha}(x)=f(x)+\hat b-\hat q_m^{-}\hat s$, where $\hat q_m^{-}$ is calibrated as in Eq. (6) but on the signed score $(\hat b-r)/\hat s$, so that only under-estimates of DMC count as misses. The rule uses the cost ratio only through $\alpha^\ast$, so a grower who cannot state costs in money can still state that withholding a mature fruit is, say, a ninth as bad as accepting an immature one ($\alpha^\ast=0.10$). Two qualifications apply. The conformal guarantee is marginal over fruit and lots, not conditional on the spectrum, so Eq. (9) is a calibrated approximation to the cost-optimal rule, not the rule itself. And it is only as good as the calibration: with an uncalibrated bound, $\alpha^\ast$ no longer corresponds to the realised risk.

At the level of a lot, the grower decides whether to pick the block now. We use the simple rule "harvest the lot when at least a share $p$ of its scanned fruit are accepted by Eq. (9)", and call a lot ready when at least a share $p$ of its fruit truly meets the specification ($p=0.8$ in the main analysis, 0.9 in the supplement).


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

We use the 684–990 nm window at 3 nm steps (103 variables), the range that gave the best PLS results in the original study [@anderson2020]. All spectra are retained. The provider's outlier flags are not applied in the main analysis because we cannot establish that they were assigned without reference to prediction residuals; their effect is examined in Supplementary Note S1.

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

The unit of analysis is the target lot. For every lot and every $m\in\{0,3,5,10,20,30\}$ we draw 100 random reference sets and evaluate on the scans of the remaining samples; a lot is evaluated at a given $m$ only if it has at least $m+10$ samples. Within a lot every sample has equal weight and every scan equal weight within its sample, matching Eq. (6). We report: *coverage*, the weighted share of scans whose reference value lies in the interval, averaged over draws and then over lots (lot-macro coverage); the share of lot-draws with coverage below $1-\alpha-0.10$ (*under-covered lots*); the mean interval *width*; and the Winkler *interval score* [@winkler1972; @gneiting2007], $(u-l)+\tfrac{2}{\alpha}(l-y)_+ +\tfrac{2}{\alpha}(y-u)_+$, a proper score that rewards narrow intervals and penalises misses. The nominal level is $1-\alpha=0.90$; 0.80 and 0.95 are examined in Supplementary Note S1. LotCP uses $E=30$ episodes per lot.

## 5.6 Statistical analysis

Methods are compared on the same lots, so tests are paired. For each $m$ and each competing method we apply the Wilcoxon signed-rank test [@wilcoxon1945] to the per-lot differences in interval score and in absolute coverage error $|\text{coverage}-0.90|$. The test assumes that the paired differences of lots are independent and symmetric under the null; independence across lots of the same season is an approximation, and we therefore also report in how many of the five target seasons the mean difference favours the reference method. P-values are adjusted by Holm's procedure [@holm1979] within each outcome family. The effect size is the matched-pairs rank-biserial correlation [@kerby2014]. Confidence intervals for lot-macro coverage and for mean differences are 95 % percentile intervals from 2,000 bootstrap resamples of lots, stratified by season. Because the season is the top-level cluster and there are only five target seasons, per-season results are always shown alongside pooled ones.

The experimental protocol, including hypotheses, splits, methods and metrics, was written and committed to the repository before any model was trained. Deviations are listed in Section 5.8.

## 5.7 External validation, harvest-decision simulator and economic analysis

*Untouched confirmation data.* The NeoSpectra handheld NIR soil library (Zenodo record 13122321; 1350–2550 nm; nine handheld units; 20 evaluable target lots) was used only for the pre-registered confirmation of Section 7.3. Following the pre-registered rule, lots are 1-degree latitude–longitude cells, because fewer than 20 survey projects had at least 20 samples. The target is the KSSL estimated organic carbon, modelled as log(1 + %). Each sample has repeated scans from several units. Five-fold cross-validation over cells defines source and target, and PLS (Savitzky–Golay first derivative after SNV, 10–30 latent variables chosen by lot-grouped cross-validation) is the predictor. Its soils overlap in part with the KSSL samples of the vis–NIR analysis below, which were measured with a laboratory instrument.

*Soil vis–NIR spectra.* To test whether the findings are specific to mango, the main comparisons are repeated on visible–near-infrared spectra of soils from the Open Soil Spectral Library, version 1.2 [@safanelli2025]. Prediction of soil properties from a spectral library, adjusted with a few locally analysed samples, is an established practice in soil spectroscopy known as spiking [@guerrero2010; @guerrero2014], so the reference-sample setting is native to that field. Two subsets with a nested structure are used. (i) LUCAS, the European Union topsoil survey [@orgiazzi2018]: the model is trained on the 2009 campaign (18,393 samples) and tested on the 2015 campaign (21,782 samples); a lot is a one-degree grid cell, which stands for a region in which a few local samples would be analysed. Targets are organic carbon and pH in water. (ii) KSSL, the library of the Kellogg Soil Survey Laboratory of the United States Department of Agriculture: 19,807 samples with total carbon; a lot is a survey project, and five-fold cross-validation over projects makes held-out projects the target. Carbon is modelled as $\log(1+\%)$. Spectra (400–2500 nm, thinned to 10 nm) are converted to absorbance and pre-treated by SNV and a Savitzky–Golay first derivative (11 points); PLS with 10 to 30 latent variables, chosen by lot-grouped cross-validation in the source, is the predictor. Each soil sample has one spectrum, so the replicate-scan term of Eq. (4) is not available and LotCP-S uses the reference-sample variance only. Each source set contains a single campaign or a set of projects, so there is no season level, and calibration residuals are held out by lot. Thirty reference draws per lot are used.

*Harvest-decision simulator.* For each target season, each lot and each $m\in\{0,3,5,10,20\}$, twenty random reference sets are drawn, and every non-reference fruit is classified by six rules against specifications of 14, 15 and 16 % DMC, which bracket the mean DMC of the data (15.9 %): (i) the point prediction, $f(x)\ge t$; (ii) the bias-corrected point prediction, $f(x)+\bar r_A\ge t$; (iii) a split-conformal lower bound from sample-fold residuals ($m=0$); (iv) bias correction plus the same source margin, $f(x)+\bar r_A-q\ge t$; (v) the one-sided LotCP-S bound of Eq. (9); (vi) the one-sided LotCP-A bound. Rules (iii)–(v) are evaluated at $\alpha\in\{0.02,0.05,0.10,0.20,1/3,0.5\}$ so that complete trade-off curves can be compared, and LotCP-A at $\alpha=\delta=0.10$. Outcomes are the share of mature fruit accepted, the share of immature fruit among those accepted, the share of lots in which more than 10 % of the accepted fruit is immature, and, at lot level, the shares of not-ready lots harvested and of ready lots delayed. PLS is the primary predictor; the CNN (seed 0) is reported in the supplement.

*Economic analysis under assumed costs.* No cost data accompany the public data set, and we do not invent monetary values. Costs are expressed in units of the value $V$ of one marketable fruit: accepting an immature fruit costs $c_I=1$; withholding a mature fruit costs $c_D\in\{1/19,1/9,1/4,1/2\}$, which corresponds to $\alpha^\ast\in\{0.05,0.10,0.20,1/3\}$; each destructive reference test costs $c_R=1.5$ (the fruit plus laboratory effort of half its value); and the reference tests are spread over lots of $N\in\{200,1000,5000\}$ fruit. The expected cost per fruit of a rule is $c_I\cdot$(share of fruit immature and accepted) $+\,c_D\cdot$(share mature and withheld) $+\,m\,c_R/N$. Every number in the economic analysis is conditional on these assumptions; they are scenarios for comparing rules, not an estimate of losses in a real orchard. To check whether the cost-derived level is sensible, we also report the regret of using $\alpha^\ast$ relative to the best level on the grid chosen in hindsight.

*Decision-support prototype.* The workflow is implemented as a command-line tool (Section 10) and run on one lot of the 2021 season, chosen as the lot of median size before its result was seen.

## 5.8 Pre-specification and deviations

The experimental protocol, including hypotheses, splits, methods and metrics, was committed to the code repository before any model was trained. The main deviations are: the lot-specific scale of LotCP-S was added after inspecting one predictor on one target season (2018, which remained its worst season); the empirical-Bayes shrinkage of the bias estimate was removed after it failed on the external soil data; and the external validation, the lot-level variant LotCP-A, the harvest-decision simulator, the economic analysis, the planner and the prototype were added after the main interval results were known. Every deviation, with its timing and reason, is listed in Supplementary Note S4.


# 6. How far standard error bars fail on later seasons

## 6.1 Point accuracy and the structure of the error

*Reproduction of published baselines.* On the data provider's published split (three seasons for training, n = 10243; the fourth season as independent test set, n = 1448), PLS with the published recipe (mean-centred Savitzky–Golay second derivative, 684–990 nm) reached an RMSEP of 1.045 % DMC, against 1.01 % reported by Anderson et al. [@anderson2020] and 1.014 % by Anderson et al. [@anderson2021]. Our CNN without augmentation reached 1.07–1.08 % (three seeds) against the 0.77 % of a tuned and augmented CNN [@walsh2024], a gap we attribute to augmentation and tuning that we did not perform. Our own PLS pipeline with standard normal variate correction reached 1.392 %, worse than the published recipe; we therefore repeated the main interval comparison with the published recipe as point predictor (end of Section 7.1).

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


The hold-out unit orders coverage as hypothesised (H2): sample folds 0.823, lot folds 0.846, season folds 0.900, and the ordering holds in each of the five target seasons (Table 4). Holding out lots repairs only a small part of the gap, which shows that the lot effect within the training seasons is smaller than the lot effect of a new season. Season-held-out residuals bring the pooled coverage to the nominal level, for split conformal prediction and for conformalised quantile regression alike (0.907). Two qualifications are needed. First, the price is width: intervals are 37 % wider than with sample folds, and the interval score is not better (7.05 against 6.81). Second, the pooled figure hides season-to-season variation: coverage by season ranges over 0.82–0.99 (Table 4), with over-coverage in 2017, when only two source seasons were available and the season-held-out models were weak, and coverage below nominal in each of the four later seasons. With a handful of past seasons, the next season is simply not exchangeable with them to within a few coverage points. LotCP and LotCP-S at $m=0$ behave like season-fold split conformal prediction, as expected.

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

Table: Table 4. Lot-macro coverage by target season (PLS, nominal 0.90).


# 7. Few-shot calibration with reference fruit

## 7.1 Intervals with reference samples (RQ2)

Table 5 and Fig. 4 show what $m$ reference samples per lot buy. Three samples are enough to change the picture: every method that corrects the lot bias then covers at least 0.90 with intervals of about the same width as the invalid sample-fold split conformal intervals. The corrected point prediction improves accordingly: the lot-level RMSE of PLS falls from 1.36 % DMC without correction to 1.06 with three and 0.98 with ten reference samples.

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

Table: Table 5. Intervals with m reference samples per lot (PLS, nominal 0.90). Each cell: lot-macro coverage / mean width / interval score. n/a: the method returns unbounded intervals at this m. ACI returned unbounded intervals in up to 10% of lot-draws; its width and score are over the finite ones.


![Fig. 4. Lot-macro coverage, mean width and interval score as a function of the number of reference samples per lot (PLS, forward chaining, 137 target lots, nominal 0.90). Dashed lines: split conformal prediction without reference samples.](figures/fig4_main.png){width=6.5in}

*Methods that do not correct the bias.* Pooling the reference residuals into the source calibration set has no visible effect (coverage 0.823 at $m=10$): a few target residuals among tens of thousands of source residuals do not move the quantile. Adaptive conformal inference over the reference samples raises coverage to 0.914 at $m=10$ but does so by widening the interval, and returns unbounded intervals in 9 % of lot-draws.

*Target-only calibration.* Split conformal prediction on the reference samples alone is valid within each lot, which shows in its tight distribution of lot-wise coverage (Fig. 5). It cannot return a bounded 90 % interval for $m<9$, and at $m=10$ it is conservative (coverage 0.956) and wide: the centred version is 34 % wider than LotCP-S. By $m=20$ the centred version reaches the interval score of LotCP-S (4.29 against 4.25) and at $m=30$ it is marginally better (4.25 against 4.31).

*Bias correction with the source quantile.* Subtracting the mean reference residual and keeping the sample-fold half-width is a strong baseline with PLS. Its coverage is above nominal (0.931–0.945) because two errors partly cancel: the sample-fold residuals contain a remnant of the lot effect, which widens the interval, and the uncertainty of the estimated bias is ignored, which should narrow it. The half-width does not depend on $m$, so the method cannot turn additional reference samples into narrower intervals, and Section 12 shows that the cancellation does not carry over to other predictors.

*Slope-and-bias correction and spiking.* Two further maintenance practices were tested. Regressing the reference values of the $m$ samples on their predictions and applying the fitted slope and intercept is worse than the mean correction at $m=5$ (interval score 5.46 against 4.80), because five points do not determine a slope, and is comparable from $m=10$ (4.75 against 4.68). Refitting the PLS model with ten reference samples added to the training set ("spiking") barely changes the predictions when the samples are added once (lot-level RMSE 1.34 % DMC against 1.36 without any correction) and remains clearly worse than the mean bias correction when they are replicated twenty times (1.16 against 0.98; supplementary table S11).

*LotCP and LotCP-S.* LotCP covers 0.921–0.930, somewhat above nominal, with a half-width that shrinks as $m$ grows. LotCP-S covers 0.914–0.921 for $m\ge3$ and has the lowest interval score of all methods for $m$ from 3 to 20 (Table 5). At $m=10$ its intervals are 10 % narrower than those of bias correction with the source quantile and 13 % narrower than those of LotCP. By season, its coverage at $m=10$ ranges over 0.88–0.96 (Table 4). Leaving out one target season at a time moves the pooled figure between 0.893 and 0.934, and the unweighted mean over seasons is 0.911 (supplementary table S4b); for sample-fold split conformal prediction the corresponding figures are 0.781–0.843 and 0.806. The 2018 value is below nominal even though 2018 served as development data for the scale estimator; we return to this in Supplementary Note S3.

![Fig. 5. Coverage within each of the 137 target lots (PLS, nominal 0.90, dotted line). Marginal coverage near the nominal level can coexist with many badly covered lots.](figures/fig5_lot_coverage.png){width=6.5in}

*Paired tests.* Supplementary table S20 compares the per-lot interval score of LotCP-S with its competitors. Against bias correction with the source quantile the difference is not significant at $m=3$ (Holm-adjusted p = 1.000) and is significant from $m=5$ on (p = 0.002 at $m=5$, p < 0.001 at $m=10$), with the mean difference favouring LotCP-S in all five seasons from $m=5$. Against the centred target-only method LotCP-S is better at $m=10$ (p < 0.001), marginally better at $m=20$ (p = 0.036, mean difference -0.03) and not different at $m=30$ (p = 1.000). On absolute coverage error the centred target-only method is better than LotCP-S at $m=20$ and $m=30$ (mean difference 0.014 and 0.020; all tests are in the supplementary table S6), which reflects its lot-conditional validity. The conclusion for RQ2 is therefore bounded: LotCP-S is the best of the compared methods when few reference samples are available, roughly $3\le m\le 10$, and offers no advantage over target-only calibration once 20 to 30 samples per lot can be afforded.


*Published PLS recipe as point predictor.* With the published PLS recipe in place of our pipeline (exploratory, same target lots), the pattern is unchanged: split conformal prediction with sample folds covers 0.843, LotCP-S covers 0.910 at m = 5 and 0.912 at m = 10 with interval scores of 3.85 and 3.72 against 4.10 and 4.02 for bias correction with the source quantile, and LotCP-A brings 91 % of lot-draws to at least 0.90 coverage at m = 10 against 67 % for LotCP-S (results/published_pls/).

## 7.2 Lot-level assurance

The marginal method leaves a minority of lots badly covered (Section 14 and Supplementary Note S3), and near-nominal average coverage means that in a large share of lots the realised coverage is below the nominal level: with LotCP-S and ten reference samples only 69 % of lot-draws reach 0.90. Table 6 and Fig. 6 show what LotCP-A (Section 4.8) achieves when it is asked for 0.90 coverage in at least 90 % of lots.

| Method | m=5 | m=10 | m=20 | m=30 |
|---|---:|---:|---:|---:|
| Bias corr. + source CP | 74 % / 0.931 / 3.83 | 77 % / 0.938 / 3.83 | 78 % / 0.945 / 3.82 | 77 % / 0.941 / 3.81 |
| Target-only CP, centred | n/a | 88 % / 0.956 / 4.63 | 78 % / 0.932 / 3.58 | 71 % / 0.921 / 3.40 |
| LotCP-S | 70 % / 0.920 / 3.60 | 69 % / 0.919 / 3.45 | 68 % / 0.918 / 3.29 | 65 % / 0.914 / 3.28 |
| LotCP-A (δ = 0.20) | 81 % / 0.944 / 4.01 | 81 % / 0.941 / 3.77 | 80 % / 0.938 / 3.57 | 82 % / 0.941 / 3.65 |
| LotCP-A (δ = 0.10) | 91 % / 0.964 / 4.61 | 92 % / 0.964 / 4.30 | 90 % / 0.958 / 3.97 | 91 % / 0.958 / 4.02 |

Table: Table 6. Lot-level assurance (PLS, forward chaining, 137 target lots, 1 − α = 0.90). Each cell: share of lot-draws whose realised coverage is at least 0.90 / lot-macro coverage / mean width (% DMC). The target share is 90 % for δ = 0.10 and 80 % for δ = 0.20.


![Fig. 6. Lot-level assurance (PLS, forward chaining). (a) Share of lot-draws in which at least 90 % of the fruit is covered; dotted lines mark the targets of LotCP-A for δ = 0.10 and δ = 0.20. (b) Mean interval width.](figures/fig12_assurance.png){width=6.3in}

With $\delta=0.10$, the share of lot-draws that reach 0.90 coverage is 92 %, 91 %, 92 %, 90 % and 91 % for $m=3$, 5, 10, 20 and 30, against a target of 90 %; with $\delta=0.20$ it is 81 % and 81 % at $m=5$ and 10, against a target of 80 %. The share of lot-draws with coverage below 0.80 falls from 8 % under LotCP-S to 1 % at $m=10$. By target season the share reaching 0.90 at $m=10$ ranges over 86–98 % (50–91 % for LotCP-S), so the assurance, like the marginal coverage, is met on average over seasons and missed by a few points in the less favourable ones. Across the other predictors and the leave-one-season-out protocol the share at $m=10$ is 90–91 %. Without reference samples the assurance is not attained (88 %) and the intervals are very wide (7.19 % DMC).

The price is width. At $m=10$ the LotCP-A interval is 25 % wider than that of LotCP-S (4.30 against 3.45 % DMC) and at $m=20$ it is 21 % wider. None of the alternatives offers the property. Bias correction with the source quantile reaches 0.90 in 77 % of lot-draws at $m=10$. Target-only calibration is valid within each lot only on average over reference draws, so the realised coverage of a given draw scatters around the nominal level: the centred version reaches 0.90 in 88 % of lot-draws at $m=10$, where it is conservative and 8 % wider than LotCP-A, and in only 78 % and 71 % at $m=20$ and 30. At twenty reference samples LotCP-A is the only method examined that keeps nine lots in ten at the stated coverage, which is the regime in which the marginal comparison of Section 7.1 found no advantage for LotCP-S over target-only calibration.

On the soil data the share of lots reaching 0.90 at $m=10$ is 93 % for held-out KSSL projects, where lots are exchangeable, and 87 % and 83 % for LUCAS organic carbon and pH, where the between-campaign change of residual scale again costs a few points; for LotCP-S the corresponding shares are 70 %, 56 % and 47 % (supplementary table S13).

LotCP-S and LotCP-A answer different questions with the same calibration data. The first gives the narrowest interval that is right on average over lots; the second gives an interval that is right for the lot in hand in nine cases out of ten. For a decision that is taken lot by lot, the second statement is the one that corresponds to the risk the grower carries.

## 7.3 Confirmation on fresh seeds and an untouched data set

All results above were obtained during development on lots we had examined, and many variants were tried along the way (supplementary ledger). We therefore froze the method and its configuration, wrote down four primary endpoints and a success rule, and committed this plan before loading a data set we had not used (experiments/plan_v2.yaml). The endpoints are the interval score of LotCP-S against bias correction with the source quantile at m = 5 and 10, and the share of reference draws in which a lot reaches 0.90 coverage for LotCP-A against the better of the two strongest baselines at m = 10 and 20. The confirmation uses five seeds fixed in advance. It was run on the mango data (fresh reference draws on lots already examined, so not a test on new data) and on the NeoSpectra handheld NIR soil library (Section 5.7), which we had not opened before the plan was committed.

| Data set | Endpoint | Comparison | Outcome | m | Lots | Mean difference | 95% CI | Holm p | r | Confirmed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Mango (re-draw; lots seen during development) | P1 | LotCP-S - bias corr. + source CP | interval score | 5 | 137 | -0.165 | -0.269 to -0.058 | <0.001 | -0.37 | yes |
| Mango (re-draw; lots seen during development) | P2 | LotCP-S - bias corr. + source CP | interval score | 10 | 137 | -0.248 | -0.352 to -0.137 | <0.001 | -0.53 | yes |
| Mango (re-draw; lots seen during development) | P3 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 10 | 137 | +0.037 | +0.010 to +0.064 | <0.001 | +0.40 | yes |
| Mango (re-draw; lots seen during development) | P4 | LotCP-A - bias corr. + source CP | share of lots ≥ 0.90 | 20 | 129 | +0.121 | +0.072 to +0.175 | <0.001 | +0.44 | yes |
| NeoSpectra soil (untouched) | P1 | LotCP-S - bias corr. + source CP | interval score | 5 | 20 | -0.049 | -0.086 to -0.013 | 0.066 | -0.54 | no |
| NeoSpectra soil (untouched) | P2 | LotCP-S - bias corr. + source CP | interval score | 10 | 20 | -0.028 | -0.079 to +0.023 | 0.294 | -0.28 | no |
| NeoSpectra soil (untouched) | P3 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 10 | 20 | +0.073 | +0.033 to +0.116 | 0.015 | +0.71 | yes |
| NeoSpectra soil (untouched) | P4 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 20 | 10 | +0.207 | +0.178 to +0.235 | 0.008 | +1.00 | yes |

Table: Table 7. Pre-registered confirmation of the frozen method (experiments/plan_v2.yaml) on five seeds fixed in advance (100–104), 20 reference draws per seed, lot and m. Unit of analysis: target lot; Wilcoxon signed-rank test, Holm correction over the four endpoints per data set; 95 % CI: bootstrap over lots; r: matched-pairs rank-biserial correlation. An endpoint is confirmed when Holm p < 0.05, the CI excludes 0 and |r| ≥ 0.2 in the expected direction. Negative interval-score differences and positive share differences favour the proposed method.


On mango all four endpoints were confirmed (Table 7). On the untouched data set the lot-level assurance was confirmed at m = 10: LotCP-A brought 95 % of lot-draws to at least 0.90 coverage against 88 % for centred target-only calibration (Holm p = 0.015), at a mean width of 1.19 against 1.13. The m = 20 endpoint was formally confirmed but is uninformative: only 10 target lots were large enough, the replay had few past lots, and LotCP-S and LotCP-A returned intervals about twice as wide as the baselines. The efficiency endpoints were not confirmed. At m = 5 the mean difference in interval score favoured LotCP-S (-0.049, 95 % CI -0.086 to -0.013), but the Holm-adjusted p was 0.066. At m = 10 the difference was -0.028 with p = 0.294. The untouched data also showed little to repair: split conformal prediction already covered 0.930 because lots defined as location cells within one survey programme are close to exchangeable. We therefore claim the lot-level assurance as confirmed and the efficiency gain of LotCP-S as observed on mango and on the soil survey's campaign shift, but not confirmed on independent data.



# 8. Risk-aware harvest decisions

This section asks what the calibrated bounds change in the decision they are meant to support (RQ3). Table 8 and Fig. 7 give the outcomes of the six decision rules for a specification of 15 % DMC; the specifications of 14 and 16 % and the CNN predictor lead to the same conclusions (supplementary tables S16–S18).

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

Table: Table 8. Harvest decisions against a 15 % DMC specification on 137 later-season lots (PLS, forward chaining; bounds at α = 0.10). Fruit level: a fruit is accepted when the rule's statistic is at least t. Lot level: a lot is harvested when at least 80 % of its scanned fruit are accepted; it is ready when at least 80 % of its fruit have reference DMC ≥ t (55 ready and 82 not-ready lots). Specifications of 14 and 16 % and the CNN predictor: supplementary table S16.


![Fig. 7. Trade-off between harvesting immature fruit and holding back mature fruit (PLS, specification 15 % DMC, 137 later-season lots). Each curve traces one rule as its confidence level α varies from 0.02 to 0.5; crosses are rules without a confidence level. (a) Fruit-level decision. (b) Lot-level decision: a lot is harvested when at least 80 % of its scanned fruit are accepted.](figures/fig14_harvest_frontier.png){width=6.5in}

## 8.1 Fruit-level decisions

Accepting a fruit when its predicted DMC reaches the specification, the decision that a handheld reading invites, accepts 90 % of the mature fruit but lets through 13.4 % immature fruit among those accepted, and in 43 % of lots more than one accepted fruit in ten is immature. Correcting the lot bias with ten reference fruit lowers the immature share to 7.7 %, but leaves 37 % of lots above the 10 % mark, because a decision on the point value ignores the scatter of individual fruit around it.

A lower bound at α = 0.10 changes the picture. Without reference fruit, the split-conformal bound reduces the immature share to 2.9 % while accepting 58 % of mature fruit. With ten reference fruit, the LotCP-S bound reduces it to 1.2 %, leaves 5 % of lots above the 10 % mark, and accepts 65 % of mature fruit, more than the split-conformal bound although its risk is lower. The reference fruit remove the lot bias, so the bound can sit closer to the prediction for the same protection. LotCP-A at the same level is more cautious (0.6 % immature among accepted, 56 % of mature fruit accepted), as its lot-level guarantee requires.

The curves in Fig. 7a make the comparison independent of the chosen level. Over its whole range, every bound that uses ten reference fruit lies below the curves of the bounds without reference fruit: for a similar share of mature fruit accepted, it lets through about half as many immature fruit or fewer. The curve of LotCP-S lies on top of that of bias correction with a source margin; at fruit level, once the bias is corrected and the level is free, the two make practically the same decisions. The bias-corrected point decision is simply the end of the same curve (α = 0.5), where most mature fruit are accepted and the immature share is highest. The value of the reference fruit for the harvest decision is therefore large and robust, while the additional value of LotCP-S over the simpler margin lies elsewhere: in calibration, which matters when the level is set from costs (Section 8.3), and in the lot-level assurance.

## 8.2 Lot-level decisions

Whether a block is picked now is decided per lot. Of the 137 target lots, 55 were ready by the criterion of Section 4.11 (at least 80 % of fruit at or above 15 % DMC). Deciding on point predictions harvested 7 % of the 82 lots that were not ready and delayed 20 % of the ready ones (Table 8). With five to ten reference fruit and a calibrated bound at α = 1/3, premature harvests fall to 4–3 % at the same rate of delay (20–21 %), and at α = 0.20 to 1 % with 38 % of ready lots delayed (Fig. 7b). Without reference fruit, no conformal bound reaches this frontier: the split-conformal bound harvests 6 % of not-ready lots while delaying 35 % of ready ones at α = 1/3. As at fruit level, LotCP-S and bias correction with a source margin trace nearly the same lot-level curve. A lot decision is therefore where the reference fruit pay off most: they roughly halve the rate of premature harvest at an unchanged rate of delay.

## 8.3 Expected cost under assumed cost ratios

Table 9 and Fig. 8 weigh the two errors and the reference tests under the cost assumptions of Section 5.7. Harvesting every fruit costs 42 units per 100 fruit, because 42 % of the fruit is below 15 % DMC. Deciding on point predictions costs 8.4–11.0 units across the four cost ratios. A LotCP-S lower bound at the cost-derived level α\* with five reference fruit costs 2.4–7.8 units, including the cost of the reference tests; relative to point decisions this is a reduction of 29–71 % at the 15 % specification and 15–80 % across the three specifications. Most of this reduction comes from using a bound instead of a point value: without any reference fruit, the split-conformal bound at α\* already costs 2.3–9.4 units. The reference fruit add a further, smaller saving when withholding a mature fruit is relatively expensive.

The cost-derived level works for LotCP-S because its bound is calibrated. Using α\* instead of the best level on the grid chosen in hindsight raises the cost of LotCP-S with ten reference fruit by 1.4 % on average (at most 5 %) with PLS and by 0.0 % with the CNN (supplementary table S17b). The two simpler bounds are well tuned for one predictor and not for the other: for bias correction with a source margin the average regret is 4.4 % with PLS, and for the split-conformal bound it is 12.6 % with the CNN. In other words, with LotCP-S a grower can translate a cost ratio into a confidence level and expect the decision to be close to the best one available, whichever predictor the instrument uses.

![Fig. 8. Expected cost under assumed cost ratios (PLS, specification 15 % DMC). (a) Cost per 100 fruit, in units of the value of one marketable fruit, for five decision rules as the assumed cost of withholding a mature fruit varies; the LotCP-S bound uses five reference fruit and the cost-derived level α*. (b) Cost of the LotCP-S rule as a function of the number of reference fruit for three lot sizes at c_D = 1/9; circles mark the minimum.](figures/fig15_economics.png){width=6.5in}

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

Table: Table 9. Expected cost per 100 fruit in units of the value of one marketable fruit, under ASSUMED costs (PLS, specification 15 % DMC, lots of 1000 fruit unless stated). Accepting an immature fruit costs c_I = 1; withholding a mature fruit costs c_D; each destructive reference test costs 1.5. α* = c_D/(c_I + c_D). The last three rows give the number of reference fruit that minimises the cost of LotCP-S. These are illustrative scenarios, not measured costs; other specifications, lot sizes and the CNN: supplementary table S17.


*How many reference fruit?* Each reference test costs one and a half fruit, so its value depends on how many fruit share it. For lots of 1000 fruit the cost-minimising number is 3–5 across the cost ratios, for lots of 5000 fruit 5–10, and for lots of 200 fruit it is 0 at c_D = 1/9: on small lots under these assumptions destructive testing does not pay for itself and the bound without reference fruit is preferable (Table 9, Fig. 8b). These optima rest on the assumed costs and on the retrospective simulation; they illustrate how the planner and the cost model combine, and a grower would substitute local values.


# 9. Planning the reference budget before the season

Fig. 9 compares the width planned from the source seasons (Section 4.9) with the width realised on the lots of the target season, for the five target seasons, three predictors, five values of $m$ and both variants.

![Fig. 9. Reference-budget planning. (a) Interval width planned from past lots against the mean width realised on the lots of the following season; each point is one target season, predictor, number of reference samples and variant. (b) Planned and realised budget curves for PLS, averaged over target seasons.](figures/fig13_planning.png){width=6.3in}

The planned width is a usable forecast. Over all 150 combinations the median absolute relative difference between realised and planned width is 7 %, and the mean difference is -2 %. For PLS and LightGBM the median absolute difference is 8 % and 7 %; for the CNN it is 12 %. By target season the mean difference ranges from -21 % to 7 %: the forecast is too wide for 2017, when the calibration rested on two source seasons whose season-held-out models were weak, and within 8 % for the four later seasons (supplementary table S15). The shape of the curve is reproduced (Fig. 9b): most of the reduction in width is obtained with the first five reference samples, and beyond ten both curves flatten. The largest deviations in Fig. 9a are the CNN in 2017, where the planned width is well above the realised one. Table 10 puts the planner in the form a grower would use: for each number of reference fruit, the width of the error bar to expect, the share of lots in which it will hold for at least 90 % of the fruit, and the cost of the tests. Going from no reference fruit to three narrows the LotCP-S interval from 5.1 to 3.8 % DMC; going from ten to twenty narrows it only from 3.5 to 3.4 % DMC, at twice the laboratory effort. A grower who needs the error bar to hold within nine lots in ten chooses LotCP-A and accepts a wider interval (4.4 % DMC at m = 10). Combined with the cost model of Section 8.3, the planner turns the question "how many fruit should we cut?" into a calculation that can be made before the season from the calibration set.

| Reference fruit per lot, m | LotCP-S planned width | LotCP-S realised width | LotCP-A planned width | LotCP-A realised width | Lots ≥ 90 % covered, LotCP-S (%) | Lots ≥ 90 % covered, LotCP-A (%) | Reference cost per 100 fruit (1000-fruit lot) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 5.14 | 5.05 | 6.86 | 6.74 | 77 | 88 | 0.00 |
| 3 | 3.76 | 3.66 | 5.01 | 4.87 | 71 | 92 | 0.45 |
| 5 | 3.59 | 3.49 | 4.61 | 4.47 | 70 | 91 | 0.75 |
| 10 | 3.48 | 3.36 | 4.37 | 4.21 | 69 | 92 | 1.50 |
| 20 | 3.36 | 3.24 | 4.12 | 3.96 | 68 | 90 | 3.00 |
| 30 | 3.27 | 3.30 | 4.00 | 4.11 | 65 | 91 | 4.50 |

Table: Table 10. The reference-sampling planner (PLS, mean over the five target seasons). Planned widths are computed from past lots before the season; realised widths are those obtained on the lots of the target season. Widths in % DMC; reference cost in units of fruit value (assumed 1.5 per test).



# 10. A decision-support prototype

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

In this lot the calibration over-predicted DMC by about 2.9 % points. The ten reference fruit exposed the bias and the tool recommended waiting. The reference values, unknown to the tool, confirm that none of the fruit had reached the specification. A single lot proves nothing about performance, which is the subject of Section 8; the box shows the form in which the result would reach a user. The prototype is a research tool. Its use in practice would need an interface on the instrument or a phone, a calibration file maintained by the instrument provider or packhouse, and the prospective validation discussed in Section 16.


# 11. Ablation study

Table 11 and Fig. 10 remove or replace one component at a time.

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

Table: Table 11. Ablation of LotCP components (PLS, nominal 0.90). Each cell: coverage / width / interval score.


![Fig. 10. Ablation: lot-macro coverage with bootstrap 95 % CI for m = 5 and m = 20; the interval score (IS) is printed next to each variant.](figures/fig6_ablation.png){width=6.3in}

*Scale.* The lot-specific scale is the component that matters most once $m>0$. Removing it (LotCP) raises the interval score at $m=10$ from 4.46 to 5.02. The two sources of scale information both contribute: with the reference-sample variance alone the score is 4.58, with the replicate-scan variance alone 4.74. The replicate-scan term is the only one available at $m\le1$ and costs no reference measurement. It is also what separates LotCP-S from the bias-correction shortcut when reference samples are few. Without the replicate-scan term, the per-lot interval score of the reference-scale-only variant is worse than that of bias correction with the source quantile at $m=3$ (mean difference 0.19, Holm-adjusted p = 0.004), because a scale estimated from three samples is noisy, does not differ from it at $m=5$ or 10 (p = 0.347 and = 0.421) and is better only from $m=20$ (p < 0.001; supplementary table S6b). A user who takes a single scan per fruit should therefore not expect an efficiency gain over that shortcut with fewer than about twenty reference samples; what remains is the stability of coverage across predictors shown in Section 12.

*Fold unit.* At $m=0$, residuals held out by lot or by sample give coverage 0.846 and 0.830; season-held-out residuals are needed to reach the nominal level. With $m>0$ the picture changes. After the lot bias has been corrected, what is left to calibrate is the within-lot residual, and lot-fold residuals describe it well: LotCP on lot-fold residuals covers 0.892 at $m=10$, slightly below nominal, with narrower intervals than LotCP on season-fold residuals, which over-covers (0.927). LotCP-S on lot-fold residuals covers 0.908 with an interval score of 4.36, against 0.919 and 4.46 for season-fold residuals. The lot-fold variant of LotCP-S is therefore the more efficient one, and it is not less safe by season: its lowest per-season coverage at $m=10$ is 0.89, against 0.88 for season-fold residuals. Season-held-out residuals are thus needed without reference samples and are not needed with them. We keep the season-fold variant as the reported method because it was fixed before this comparison was made, and note that the choice costs about 6 % in width at $m=10$.

*Shrinkage.* The pre-specified empirical-Bayes shrinkage of the bias estimate has a small effect at $m=3$ (interval score 5.32 against 5.40 for the plain mean with the location-only method, 4.86 against 4.91 with LotCP-S) and none from $m=10$ (4.46 against 4.46). The reason is visible in the variance components: the lot bias is large relative to the sample noise, so the shrinkage weight is already 0.79–0.83 at $m=3$. On the soil data of Section 13 shrinkage is harmful. The part of H4 that concerns shrinkage is not supported, and the reported method uses the plain mean.

*Episodic replay for LotCP-S.* A pre-registered ablation (plan_v2) removed the replay from LotCP-S, standardising each past lot with its own full-information bias and scale. Coverage then fell to 0.757 at m = 0, 0.888 at m = 3 and 0.908 at m = 10, against 0.894, 0.920 and 0.921 with replay. The share of lots reaching 0.90 fell from 71 % to 56 % at m = 3. The interval score was not better with the replay (4.44 against 4.38 at m = 10): the replay buys validity at small m, not efficiency.

*Episodic quantile.* Replacing the replayed quantile by the quantile of within-lot residuals centred on the true lot mean, which ignores the estimation error of the bias, gives coverage 0.899 at $m=3$ and 0.917 at $m=10$ for the location-only method, and it fails at $m=0$ (0.782). Because season-fold residuals are conservative for $m>0$, the omission is not punished in this data set. The replay is nevertheless what makes the scale-adaptive score calibratable at all, since the distribution of $|r-\hat b|/\hat s$ depends on $m$ through both estimates.

*Weighting.* Giving every scan rather than every lot the same weight changes little (0.932 against 0.927 at $m=10$), because lot sizes are fairly homogeneous here.

In summary, H4 holds for the scale component and, at $m=0$, for the fold unit. It does not hold for shrinkage, which was therefore removed from the method, and holds only at very small $m$ for the episodic quantile of the location-only method.

# 12. Generalisation across predictors and protocols

Fig. 11 and supplementary table S21 repeat the comparison for LightGBM and the CNN, and for the leave-one-season-out protocol. The seed-to-seed standard deviation of lot-macro coverage is at most 0.002 for the LotCP variants (supplementary table S7b).


![Fig. 11. Lot-macro coverage of LotCP and LotCP-S for three point predictors and two protocols (nominal 0.90).](figures/fig7_generalisation.png){width=6.5in}

The failure of sample-fold split conformal prediction is larger for the more flexible predictors: coverage is 0.759 for LightGBM and 0.789 for the CNN, against 0.823 for PLS, because flexible models absorb more of the lot effects of their training lots. For the same reason, bias correction with the source quantile, which over-covers with PLS, under-covers with LightGBM (0.882 at $m=10$) and sits at 0.909 with the CNN. Its coverage depends on how strongly the predictor fits its training lots, which the user does not control. LotCP-S covers 0.914 and 0.914 at $m=10$ with these predictors, and 0.907 and 0.908 under leave-one-season-out with PLS and the CNN. Across the five predictor–protocol combinations its coverage at $m=10$ stays within 0.907–0.919. With the CNN, whose point error is lowest, LotCP-S at $m=10$ gives a mean width of 3.06 % DMC, that is, about ±1.5 % DMC.

# 13. External validation on soil vis–NIR spectra

The experiments so far use one fruit and one instrument family. We therefore repeated the central comparisons on two soil subsets of the Open Soil Spectral Library (Section 5.7), a different material, spectral range, instrument and reference chemistry, in a field where adjusting a library model with a few local samples is established practice. Table 12 and Fig. 12 give the results.

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


![Fig. 12. Lot-macro coverage on the soil data as a function of the number of local reference samples (PLS, nominal 0.90, dotted line). Dashed line: split conformal prediction with sample folds and no reference samples.](figures/fig10_soil.png){width=6.5in}

*The coverage loss is larger than for mango.* A model trained on the 2009 LUCAS campaign and applied to the 2015 campaign has a prediction error on the target of 0.57 log-units for organic carbon, against 0.32 in cross-validation, with a mean offset of 0.43; for pH the error is 1.36 against 0.61, with an offset of -1.15 pH units. We do not know the origin of this between-campaign offset; whatever its cause, it is the kind of batch effect a user of a spectral library can meet. Split conformal intervals calibrated within the 2009 campaign then cover 0.63 (organic carbon) and 0.40 (pH) of the 2015 values in 467 grid cells, at a nominal 0.90. Holding residuals out by lot does not help (0.64 and 0.40), because the shift is between campaigns and the source contains only one. This is the situation in which no label-free repair exists. For held-out KSSL projects, which are exchangeable with the calibration projects by construction, sample-fold split conformal prediction covers 0.881 and lot-fold calibration 0.895: with exchangeable lots and no campaign effect, the loss is small and holding out lots removes it, as hierarchical conformal theory predicts.

*A few local reference samples repair most of it.* With five reference samples per cell, LotCP-S covers 0.888 for organic carbon and 0.872 for pH; with twenty, 0.899 and 0.885. Coverage stays up to three points below nominal, because the residual scale of the 2015 campaign also differs from that of the 2009 cells that calibrate the half-width; the method does not fully absorb a shift in scale between campaigns. For KSSL projects it covers 0.914–0.916.

*Comparison with the alternatives.* On LUCAS organic carbon LotCP-S has a lower interval score than bias correction with the source quantile and slope/bias correction at $m=5$, 10 and 20, and than centred target-only calibration at $m=10$ and 20 (Holm-adjusted p ≤ 0.003 against the first two; p < 0.001 and < 0.001 against the third; supplementary table S13c). On LUCAS pH it is better than bias correction at $m=5$ and 10 (p < 0.001 and = 0.021) and not different at $m=20$ (p = 0.204); slope/bias correction has a numerically lower score from $m=10$, a difference that is not significant. On KSSL it does not differ from bias correction at $m=5$ and 10 (p = 1.000 and = 1.000) and is better at $m=20$ (p = 0.024); slope/bias correction has the numerically best score there at $m=20$. Bias correction with the source quantile under-covers on all three soil tasks (0.878, 0.891 and 0.872 at $m=10$), where it over-covered with PLS on mango: its coverage is again not under control. Centred target-only calibration is valid and wider, as before. Since soil samples have a single spectrum, these comparisons involve no replicate-scan information; the advantage of LotCP-S on LUCAS comes from calibrating the half-width for the estimation error and from the reference-sample scale.

*Shrinkage fails under a campaign shift.* The pre-specified shrinkage variant covers only 0.70 for pH and 0.85 for organic carbon at $m=5$, against 0.87 and 0.89 with the plain mean (supplementary table S13). The between-lot variance estimated inside the 2009 campaign is small, so the shrinkage weight is low and the estimate is pulled towards the 2009 mean, which the 2015 campaign has left. On KSSL, where lots are exchangeable, shrinkage gives a small gain at $m=5$ (interval score 2.05 against 2.10). Shrinkage thus helps a little when its assumption holds and fails badly when it does not, and the user cannot know in advance which case applies. This is why the reported method does not use it.

Taken together, the soil data reproduce the three main findings on independent material: intervals calibrated within the source population lose coverage on a new population, drastically so across survey campaigns; a handful of local reference samples restores most of the coverage; and LotCP-S is not significantly worse than any competing method at $m\le10$ and is significantly better where the shift is large. They also show a limit: under a between-campaign change of residual scale, coverage remains a few points short of nominal.

# 14. Robustness, computational cost and failure analysis

The detailed analyses are in Supplementary Notes S1–S3; the main results are these. *Robustness* (Note S1, Fig. S2, table S22). Adding Gaussian error with a standard deviation of 0.5 % DMC to the reference values left LotCP-S coverage at 0.923 at $m=10$ and widened the intervals by 4 %. Removing provider-flagged outliers changed coverage by 0.001. With only 20 past lots the method was conservative (0.947, intervals 12 % wider), and about 40 past lots were needed before the conservatism became small. Episode count and pseudo-count were immaterial. When the deployment unit was a single instrument unit within a lot, coverage was 0.919. When only the two preceding seasons were available it was 0.918, and for a held-out region or cultivar 0.913 and 0.907. Results at nominal levels 0.80 and 0.95 follow the same pattern (table S23). *Cost* (Note S2, table S24). The episodic calibration takes about 1.8 s for 187 past lots, and deployment computes one bias and one scale per lot. The binding cost is the number of destructive reference tests, which Sections 8.3 and 9 address. *Failures* (Note S3, Fig. S3). At $m=10$, 38 of the 137 target lots had coverage below 0.80 under sample-fold split conformal prediction, 13 under LotCP and 4 under LotCP-S. After bias correction the remaining failures were lots whose residual spread exceeded what past lots suggested (Spearman correlation of lot coverage with the ratio of lot to prior residual standard deviation, -0.84). Coverage was lower for fruit at the ripening stage (0.90 against 0.93), for the cultivar Keitt (0.86) and at the extremes of the DMC range.


# 15. Discussion

**From an error bar to a harvest decision.** The professional question behind a handheld NIR reading is not "what is the DMC?" but "can this fruit, or this block, be picked now?". The simulation shows that the answer depends less on the point predictor than on how its uncertainty is handled. Deciding on the point value let through 13 % immature fruit among those accepted, and in 43 % of lots more than one accepted fruit in ten was immature. A calibrated lower bound, with ten fruit of the lot tested destructively, brought these figures to 1.2 % and 5 % of lots. In exchange, more mature fruit was held back (65 % accepted instead of 90 %), a trade the grower can set explicitly through the cost ratio. At lot level, the reference fruit reduced premature harvests from 7 % to 4 % of not-ready lots at an unchanged rate of delay. Under every cost scenario we examined, any calibrated bound was far cheaper than a decision on the point value. The few-shot calibration added a further saving when withholding mature fruit is relatively costly, and a confidence level derived from the cost ratio that stayed close to the best one across predictors.

**What the method adds over a simple margin, and what it does not.** At fruit level, once the bias of a lot is corrected and the confidence level is free, LotCP-S and the simpler "bias correction plus a margin from past residuals" make nearly the same decisions. We report this plainly, because it locates the contribution: the large gain comes from using reference fruit and a bound at all, and the calibration of LotCP determines whether the bound means what it says. That matters in three places: when the level is set from costs, where the uncalibrated margin is well tuned for one predictor and not for another; when a statement about the lot itself is wanted, which only LotCP-A provides; and when the number of reference fruit must be planned before the season, which needs a calibration of how the width depends on *m*.

**What the user of a handheld instrument should take from this.** An error bar derived from the calibration set, by cross-validation, by a conformal quantile on held-out samples or by the predictive variance of a neural network, describes the past lots. On the lots of a later season it was too narrow in every one of the five seasons we could test and for every predictor. The size of the shortfall, 5 to 14 coverage points at a nominal 90 % depending on the method and the predictor, is large enough to matter for a decision against a specification, and it is concentrated in a minority of lots that are covered very badly (Fig. 5).

**Without reference samples there is no cheap repair.** Season-held-out calibration is the honest label-free option and should replace sample-fold calibration when intervals are quoted for a future season. It restores coverage on average, at the price of intervals 37 % wider, and its per-season coverage still ranged over 0.82–0.99. This is not a defect of the procedure. With four to six past seasons there is little information about how different the next one will be, and no reweighting of unlabelled spectra recovers a bias in the residual.

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

*Efficiency not confirmed on independent data.* The interval-score advantage of LotCP-S over bias correction with a source quantile was confirmed on fresh draws of the mango lots, but not on the untouched NeoSpectra data (Section 7.3), where the test had about 20 lots and the baselines already covered well. The advantage should be regarded as data-dependent until confirmed elsewhere.

*Point predictor.* Our main PLS pipeline was weaker than the published recipe on the published split; the interval conclusions held with the published recipe, but the absolute widths reported for PLS would be smaller with a better predictor.

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
