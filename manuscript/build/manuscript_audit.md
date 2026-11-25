---
title: "Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons"
---

**P N Bhargav Teja^a^, Ragavan K^a,\*^**

^a^ [Department, Institution, City, Postal code, Country]

\* Corresponding author: Ragavan K, [e-mail address], [postal address]

# Abstract

A handheld near-infrared (NIR) prediction of mango dry matter content (DMC) supports a harvest decision only if its error is known for the lot being picked, yet error bars are calibrated on past seasons. Predicting each season of a public mango data set (⟦199⟧ harvest lots, seven seasons) from earlier seasons, six standard error bars at a nominal 90 % covered ⟦77⟧–⟦84⟧ % of reference values on ⟦137⟧ later-season lots. A few-shot conformal calibration that tests five to ten fruit per lot and corrects the lot bias and scale raised coverage in every season but reached 90 % in only two of five, because seasons differ by more than past lots suggest. We therefore calibrate within each past season, treating seasons as exchangeable units, and take an upper order statistic across seasons; this gives a season-level guarantee whose strength grows with the number of past seasons. In exploratory analyses this season-robust replay reached 90 % coverage in all five seasons for four predictors at ⟦7⟧–⟦11⟧ % more width, against ⟦24⟧–⟦26⟧ % for a fixed higher confidence level, and its lot-level form met a nine-lots-in-ten target in ⟦4⟧–⟦5⟧ of five seasons, against ⟦1⟧–⟦2⟧. Learning the shift from earlier lots of the same season and spectral warning signs did not help. Under assumed costs, deciding on a calibrated lower bound rather than the point value lowered the cost of harvest decisions. A prospective orchard trial remains necessary.

**Keywords:** near-infrared spectroscopy; harvest decision; fruit maturity; dry matter; conformal prediction; uncertainty quantification; calibration maintenance

# Highlights

- NIR error bars calibrated on past seasons under-covered later-season mango lots.
- A few reference fruit per lot restored coverage on average but not every season.
- Calibrating within each past season gives a season-level coverage guarantee.
- Season-robust calibration met 90 % coverage every season at half the extra width.
- Calibrated lower bounds, not point predictions, lowered assumed harvest costs.


# 1. Introduction

Handheld near-infrared (NIR) spectrometers are a routine tool for deciding when to harvest fruit. In mango, dry matter content (DMC) at harvest is the accepted index of eating quality: fruit picked below a cultivar-specific DMC does not ripen to acceptable quality, so growers scan fruit on the tree and compare the predicted DMC with a specification before a block is picked [@walshsubedi2016; @anderson2017; @walsh2020review]. A reading of 15.2 % against a 15 % specification supports a harvest only if its error is known to be small for the lot in hand. The calibration behind the reading, however, was built on earlier seasons and is applied to a new season, a new block and often a different instrument unit. Work on fruit NIR spectroscopy has shown repeatedly that biological variability between seasons and orchards degrades models built on other populations [@peirs2003; @bobelyn2010; @nicolai2007; @walsh2020review]. For mango DMC this was documented on a multi-season data set, where the loss depended on season, cultivar and fruit temperature [@anderson2020; @anderson2021; @sun2020]. Current practice still quotes one root-mean-square error and, implicitly, the same band around every prediction.

Conformal prediction turns any point predictor into intervals with a finite-sample coverage guarantee [@vovk2022; @lei2018; @angelopoulos2023] and has begun to be used for spectroscopic quantification [@jovic2025; @sun2026]. Its guarantee rests on exchangeability between calibration and test data, which a new harvest season breaks. Two features of the orchard setting offer a partial way out. First, the data are nested: scans within fruit, fruit within harvest lots (one orchard block on one date), lots within seasons. A multi-season calibration set therefore contains many past lots in which lot-to-lot variation of the error can be observed. Second, adjusting a calibration with a few reference samples of the new population, as in slope/bias correction with transfer samples, is a standard element of calibration transfer [@fearn2001; @feudale2002], and sampling protocols for guiding mango harvest decisions with handheld NIR have been described [@anderson2019harvest]. What is missing is evidence on how far error bars fail lot by lot across real seasons, a procedure that turns a few reference fruit into an error bar with a stated coverage, and an honest account of what such error bars change in a harvest decision.

This paper evaluates a risk-aware harvest workflow built on these two features (Fig. 1). Fruit of a lot are scanned, *m* of them are tested destructively, a few-shot conformal calibration corrects the lot bias and scale, and each fruit receives a lower bound that is compared with the specification at a confidence level set by the cost ratio of the two possible errors.

![Fig. 1. Risk-aware harvest workflow. Before the season, past lots are used to calibrate the few-shot correction and to plan the number of reference fruit. In the orchard, fruit of a new lot are scanned, m of them are tested destructively, and each fruit receives a calibrated lower bound that is compared with the dry-matter specification.](figures/fig1_workflow.png){width=6.5in}

## 1.1 Related work

*Robust fruit calibrations.* Robustness across seasons, regions, cultivars and temperatures has been pursued with larger and more diverse calibration sets [@anderson2020], local and nonlinear models [@anderson2021], temperature-robust modelling [@sun2020], convolutional networks [@mishra2021; @walsh2024; @passos2023; see also @cui2018], semi-supervised learning [@mishra2023], domain-invariant PLS that adapts to a new season from unlabelled spectra [@mishra2020dipls] and new cross-cultivar models [@ma2026]. Calibration transfer, standardisation and model updating address instrument and population differences [@fearn2001; @feudale2002; @mishra2021transfer]; spiking a library with local samples is the corresponding practice in soil spectroscopy [@guerrero2010; @guerrero2014]. This work targets the point prediction.

*Uncertainty for spectroscopic models.* Methods for estimating prediction intervals in NIR spectroscopy have been compared [@bouckaert2011], and uncertainty calibration for latent-variable regression has been revisited recently [@duma2025]. Quantile regression forests [@meinshausen2006], deep ensembles [@lakshminarayanan2017] and Monte-Carlo dropout [@gal2016] are model-based alternatives; simple uncertainty methods for neural networks have been applied to mango DMC (preprint) [@metz2025]. Wadoux and Ramirez-Lopez modelled prediction uncertainty in absorption spectroscopy with quantile regression forests [@wadoux2025]. Conformal prediction has been applied to mid-infrared adulteration data [@jovic2025] NIR quantification of botanicals (preprint) [@sun2026] and deep-learning soil spectral models [@huang2025soilcp]. None of these studies audits coverage lot by lot on later seasons. The closest work measures the loss of split-conformal coverage under instrument transfer and the labelled target samples needed to restore it [@kayaoglu2026]. Our setting differs in the shift (seasons and lots rather than paired instruments) and in using past lots to calibrate the few-shot correction before the new lot is seen.

*Conformal prediction under shift and for groups.* Weighted conformal prediction handles covariate shift with a known or estimated likelihood ratio [@tibshirani2019] but not a change in the residual distribution, which is what a lot bias is. Adaptive conformal inference tracks a labelled stream [@gibbs2021], non-exchangeable conformal prediction down-weights less relevant points [@barber2023], and cross-conformal methods reuse training data [@vovk2015; @barber2021]. For grouped data, Dunn et al. [@dunn2023] and Lee et al. [@lee2023] replace exchangeability of observations by exchangeability of groups. Lee et al. prove marginal coverage for a group-balanced quantile and note that a score centred on a few observed outcomes of the test group can be used; Fisch et al. [@fisch2021] and Park et al. [@park2022] calibrate few-shot predictors across tasks, and recent work meta-learns few-shot conformal calibration [@park2024metaxb], recalibrates at a new site from a few local labels [@nasir2026], audits coverage under shift with a label budget [@moussa2026], reports that recalibration parameters often fail to transfer [@neyigapula2026] (these three are preprints), recalibrates conformal predictors at test time from unlabelled examples [@yilmaz2022] or handles shift for spectral classification [@khairbek2026]. Coverage that holds across several source distributions has been obtained by max-type aggregation [@yang2026mdcp; @tsibulsky2025] and by adapting to unknown subpopulation shifts [@wang2025subpop]; these guarantee coverage for test points from the source distributions, not for an unseen season. Most directly, generalized hierarchical conformal prediction [@mallick2026ghcp] gives valid intervals for an unseen group of which a few outcomes are observed, and symmetry-based predictive inference covers partially observed hierarchical data [@dobriban2023symmpi]. The coverage theory used here is that of Lee et al.; replaying an *m*-shot procedure across past groups is not itself new. What this paper adds is a third level: calibration within each past season and an order statistic across seasons, which gives a guarantee for an unseen season and, on real harvest seasons, restores the coverage that pooled hierarchical calibration loses. It also supplies the parts specific to NIR calibration maintenance: season-held-out residuals inside the replay and a label-free lot scale from repeated scans.

## 1.2 Contributions

1. **A lot-by-lot coverage audit across harvest seasons.** Six families of error bars, two PLS recipes and two machine-learning predictors are evaluated on ⟦137⟧ later-season lots under forward chaining, with season-level as well as lot-level inference.
2. **A few-shot calibration adapted to NIR maintenance, and what each part buys.** Building on hierarchical conformal prediction [@lee2023; @mallick2026ghcp], LotCP-S corrects a lot's bias from *m* reference fruit, scales the score by a lot scale that also uses the label-free variance of repeated scans, and obtains the half-width from the *m*-shot score on past lots with season-held-out residuals. Matched baselines, added after an internal review, isolate the replay step: it protects coverage at small *m* and does not make intervals narrower.
3. **Season-robust replay with a season-level guarantee.** Pooled calibration and a lot-level variant (LotCP-A) both fall short when a new season differs from past ones. Calibrating within each past season and taking an upper order statistic across seasons yields a guarantee one level up, for an unseen season, whose strength is set by the number of past seasons. We show that it restores season-by-season coverage for four predictors at a fraction of the width of a fixed higher level, explain the mechanism by a sensitivity analysis, and report two plausible alternatives that failed (within-season learning, spectral warning signs).
4. **A planner and an exploratory decision analysis.** A planner forecasts the width for each *m* from past lots. Fruit- and lot-level harvest decisions are simulated post hoc, under explicitly assumed costs, with season-cluster confidence intervals at an operating point fixed before those intervals were computed. The analysis shows that the saving comes from using a calibrated bound at all, not from the reference fruit.

The evaluation is a retrospective simulation on public data. It shows what the workflow would have done, not what it has done in an orchard.


# 2. Method

## 2.1 Setting and a model of the failure

A *lot* $k$ is the fruit harvested from one orchard block on one date. It contains $n_k$ reference *samples* $i$ (a piece of fruit tissue with one oven-dried DMC value $y_{ki}$), and sample $i$ has $J_{ki}\ge1$ *scans* $x_{kij}$. Lots are nested in seasons. A point predictor $f$ gives residuals $r_{kij}=y_{ki}-f(x_{kij})$. For a new lot the user scans the fruit and measures $m\ge0$ randomly chosen samples destructively; for every other scan an interval $C(x)$ with $\mathbb{P}\{y\in C(x)\}\ge1-\alpha$ is wanted. Split conformal prediction [@lei2018] returns $f(x)\pm q$, with $q$ the $\lceil(n+1)(1-\alpha)\rceil/n$ empirical quantile of held-out absolute residuals, and is valid when test and calibration residuals are exchangeable. We describe a residual by

$$r_{kij}=b_k+u_{ki}+e_{kij},\qquad b_k\sim(\mu,\tau^2),\quad u_{ki}\sim(0,\sigma_k^2),\quad e_{kij}\sim(0,\varepsilon_k^2), \qquad\text{(1)}$$

with a lot bias $b_k$, a sample effect and scan-to-scan variation. Eq. (1) motivates the estimators; coverage does not depend on it. If calibration residuals are held out at random, each calibration scan has lot-mates in the training set, the predictor has partly absorbed $b_k$, and the residuals are too small. Holding out lots exposes the between-lot variance of the training seasons; holding out seasons also exposes the part of $b_k$ shared by a season.

## 2.2 Season-held-out residuals and bias correction

For each source season $s$ the predictor is refitted without $s$ and predicts the scans of $s$, giving season-held-out residuals $\tilde r_{kij}$ for every source scan; the deployed predictor uses all source seasons. This is cross-conformal calibration [@vovk2015] with seasons as folds. From these residuals the one-way random-effects moments $\hat\mu$, $\hat\sigma^2$ (between samples within lots) and $\hat\tau^2$ (between lots) are estimated by the method of moments. For a new lot with reference set $A$, $|A|=m$, the bias is the mean reference residual,

$$\hat b=\bar r_A\quad(m\ge1),\qquad \hat b=\hat\mu\quad(m=0). \qquad\text{(2)}$$

Empirical-Bayes shrinkage [@efron1975] of $\bar r_A$ towards $\hat\mu$ was part of the pre-specified design; it was immaterial on mango and harmful under a large campaign shift on soil spectra, and it is reported only as an ablation (Supplementary Note S5).

## 2.3 Lot scale (LotCP-S)

Lots differ in residual spread as well as bias. LotCP-S divides the score by

$$\hat s^2=\hat u^2+\hat e^2,\qquad \hat u^2=\frac{\nu_0\hat\sigma^2+(m-1)s_A^2}{\nu_0+m-1},\qquad \hat e^2=\frac{\sum_i\sum_j\big(f(x_{ij})-\bar f_i\big)^2}{\sum_i(J_i-1)}, \qquad\text{(3)}$$

where $s_A^2$ is the variance of the $m$ reference residual means, shrunk towards $\hat\sigma^2$ with pseudo-count $\nu_0\in\{5,10,20,40\}$ (chosen as the value giving the narrowest calibrated source intervals), and $\hat e^2$ is the pooled within-sample variance of the *predictions* of repeated scans of the new lot. $\hat e^2$ needs no reference value. When a lot has no repeated scans it is replaced by its mean over the source lots. LotCP without the suffix uses $\hat s\equiv1$.

## 2.4 Replaying the m-shot procedure on past lots

The half-width must reflect that $\hat b$ and $\hat s$ come from only $m$ samples. We obtain it by replaying deployment on the past. For each source lot $k$ with at least $m+10$ samples and each episode $e=1,\dots,E$, a reference set $A_{ke}$ of $m$ samples is drawn, $\hat b_{ke}$ and $\hat s_{ke}$ are computed from it by Eqs. (2)–(3), and the remaining scans give scores

$$S_{keij}=|\tilde r_{kij}-\hat b_{ke}|/\hat s_{ke},\qquad i\notin A_{ke}. \qquad\text{(4)}$$

The multiplier $\hat q_m$ is the $(1-\alpha)$ quantile of the lot-balanced score distribution

$$\hat q_m=Q_{1-\alpha}\Big(\sum_{k=1}^{K_m}\frac{1}{K_m+1}\sum_{e=1}^{E}\frac1E\sum_{i\notin A_{ke}}\frac{1}{n_k-m}\sum_{j}\frac{1}{J_{ki}}\delta_{S_{keij}}+\frac{1}{K_m+1}\delta_{+\infty}\Big), \qquad\text{(5)}$$

in which every lot carries equal weight, every sample equal weight within its lot and every scan equal weight within its sample. The interval for a scan of the new lot is $C(x)=f(x)+\hat b\pm\hat q_m\hat s$. For $m=0$ and $\hat s\equiv1$, Eq. (5) is the hierarchical conformal quantile of Lee et al. [@lee2023] on season-held-out residuals; for $m\ge1$ it is the mean-centred score that Lee et al. propose when a few outcomes of the test group are observed (their Remark 1), and generalized hierarchical conformal prediction addresses the same few-shot setting by other means [@mallick2026ghcp]; related symmetry-based inference covers partially observed hierarchical data [@dobriban2023symmpi]. What the replay changes, relative to a plug-in alternative that standardises each past lot by its own full-information bias and scale, is that the estimation error of $\hat b$ and $\hat s$ at the deployed $m$ enters the quantile. Section 4.3 measures what this buys.

## 2.5 What is guaranteed

If the predictor and the constants are fixed, the calibration lots and the new lot are exchangeable, and samples are exchangeable within lots, the score of a random non-reference scan of the new lot, computed with a random reference set, is exchangeable with the calibration scores, and $\mathbb{P}\{y\in C(x)\}\ge1-\alpha$ for every $m$, with the probability taken over lots, reference draws and scans (Appendix A, Proposition 1, which covers random reference sets, three levels and unequal lot sizes). In our use these conditions hold only approximately. Calibration residuals come from season-held-out predictors; the constants are estimated from the calibration lots; lots of a new season are not exchangeable with past lots when the season differs systematically; and the guarantee is marginal over lots, not conditional on the lot [@barber2021limits]. The third gap is the one that matters, and Section 4 measures it season by season.

## 2.6 Lot-level assurance (LotCP-A)

A grower harvests one lot at a time, so a statement about the lot is more useful than one averaged over lots. For a lot $k$ and draw $e$ let $Q_{ke}$ be the weighted $(1-\alpha)$ quantile of the scores of Eq. (4) over the non-reference scans of that lot. A multiplier $q$ covers at least $1-\alpha$ of those scans exactly when $q\ge Q_{ke}$. LotCP-A therefore takes

$$\hat q^{\,A}_m=Q_{1-\delta}\Big(\sum_{k=1}^{K_m}\frac{1}{K_m+1}\sum_{e=1}^{E}\frac1E\delta_{Q_{ke}}+\frac{1}{K_m+1}\delta_{+\infty}\Big). \qquad\text{(6)}$$

Under exchangeable lots, the realised coverage within the new lot is at least $1-\alpha$ with probability at least $1-\delta$ (Appendix A, Proposition 2), a statement of the probably-approximately-correct type [@park2022]. We use $1-\alpha=0.90$ and $\delta=0.10$. LotCP-A and LotCP-S at a smaller $\alpha$ lie on the same family of intervals. LotCP-A does not buy assurance more cheaply. It chooses, from past lots and without target labels, the level that delivers the requested assurance.

## 2.7 Season-robust replay (LotCP-R, LotCP-AR)

Sections 2.5 and 2.6 assume that the lots of a new season are exchangeable with the pooled lots of past seasons. Seasons differ, and a quantile pooled over past lots is dominated by the seasons that contributed most lots. LotCP-R keeps the score function of LotCP-S (the fitted bias, scale and constants are frozen) but replays the $m$-shot procedure separately within each past season $s=1,\dots,S$, giving per-season conformal multipliers

$$\hat q_{m,s}=Q_{1-\alpha}\Big(\sum_{k\in s}\frac{1}{K_s+1}\sum_{e}\frac1E\sum_{i\notin A_{ke}}\frac{1}{n_k-m}\sum_j\frac{1}{J_{ki}}\delta_{S_{keij}}+\frac{1}{K_s+1}\delta_{+\infty}\Big), \qquad\text{(7)}$$

the multiplier that would be valid for a new lot exchangeable with the $K_s$ lots of season $s$. LotCP-R uses the largest of the $S$ values and LotCP-R2 the second largest. LotCP-AR does the same with the lot-level quantile of Eq. (6). If seasons are exchangeable, the $k$-th largest of $S$ past-season multipliers is at least the corresponding multiplier of the new season with probability at least $(S+1-k)/(S+1)$, so a new lot of the new season is then covered with probability at least $1-\alpha$ (Appendix A, Proposition 3). The statement turns the number of past seasons into a design quantity: with four past seasons and $k=1$ the season-level probability is at least 0.8, with nine at least 0.9. Max-type aggregation over source distributions has been used to guarantee coverage for test points from one of the *source* distributions [@yang2026mdcp; @tsibulsky2025]; here the target season is unseen, and the guarantee is obtained by treating seasons, in turn, as exchangeable units.

## 2.8 Planning the number of reference fruit

The replay yields, for every $m$ and from past lots alone, the multiplier and the mean lot scale $\bar s_m$ over episodes, and hence a planned width $2\hat q_m\bar s_m$. The curve of planned width against $m$ can be drawn before the season and turns the choice of $m$ into an explicit trade between laboratory effort and precision. Calibration costs one extra model fit per source season, done offline; deployment computes two means and one variance per lot.

## 2.9 From a bound to a harvest decision

Let $t$ be the minimum DMC a fruit must reach, $c_I$ the cost of accepting an immature fruit and $c_D$ the cost of withholding a mature one. If the probability that a fruit is below $t$ were known, expected cost would be minimised by accepting it when that probability is at most $\alpha^\ast=c_D/(c_I+c_D)$, the familiar newsvendor or Bayes threshold. A lower bound $L_{\alpha}(x)=f(x)+\hat b-\hat q^-_m\hat s$, with $\hat q^-_m$ calibrated as in Eq. (5) on the signed score $(\hat b-r)/\hat s$, gives the rule *harvest if* $L_{\alpha^\ast}(x)\ge t$, *otherwise wait or re-test*. Because the guarantee is marginal, not conditional on the spectrum, this rule is a calibrated approximation to the cost-optimal rule. A lot is harvested when at least a share $p$ of its scanned fruit is accepted, and it is called ready when at least a share $p$ of its fruit truly meets $t$ ($p=0.8$).


# 3. Experimental setup

## 3.1 Data

We use the public "Mango DMC and NIR spectra" data set, version 6 [@mangodata] (CC BY 4.0), which extends the data of Anderson et al. [@anderson2020; @anderson2021] and Walsh et al. [@walsh2024]. It contains ⟦85,401⟧ spectra of intact fruit from handheld spectrometers in interactance geometry, each paired with the oven-dry DMC of the tissue under the scanned position, and identifies the season (⟦7⟧ seasons, 2015–2021), region, cultivar (⟦10⟧), instrument unit (⟦31⟧), reference sample (⟦10,560⟧) and population (⟦199⟧). A population is the fruit of one orchard block and harvest date; we call it a lot. Every sample was scanned repeatedly (median ⟦6⟧ scans; several instrument units and, for a subset, three fruit temperatures). We use 684–990 nm at 3 nm steps [@anderson2020] and retain all spectra (Table 1).

⟦| Season | Spectra | Samples | Lots | Cultivars | Instrument units | DMC mean (%) | DMC SD (%) | Median samples per lot |
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
⟧

## 3.2 Protocols and leakage control

For each target season $T\in\{2017,\dots,2021\}$ the source data are all earlier seasons (forward chaining). Nothing from season $T$ enters training, preprocessing, model selection or calibration except the $m$ reference samples of the lot under test. This gives ⟦137⟧ target lots with at least 20 samples; 2017, with two source seasons, contributes ⟦56⟧ of them. All folds are grouped by sample, lot or season, so repeated scans of a sample never straddle a fold; reference samples are drawn at sample level and all their scans leave the evaluation set; pre-treatments are row-wise. Leave-one-season-out, two-season, region and cultivar shifts are robustness checks (Supplementary Note S5).

## 3.3 Point predictors

*SNV PLS*, developed for this study: standard normal variate [@barnes1989], Savitzky–Golay second derivative (17 points, second order) [@savitzky1964] and PLS [@wold2001] with 8–20 latent variables chosen by leave-one-season-out cross-validation in the source. *Published PLS*: the recipe of the data providers (mean-centred Savitzky–Golay second derivative without SNV, 6–30 latent variables chosen in the same way), which reproduced the published accuracy (Section 4.1) and is reported alongside SNV PLS in every main table. LightGBM [@ke2017] and a compact 1D-CNN [@cui2018; @walsh2024] with three fixed seeds are reported in the supplement.

## 3.4 Interval methods

*Without reference samples* ($m=0$): Gaussian band $\pm z_{1-\alpha/2}\,$RMSECV; split conformal prediction with residuals held out by sample, lot or season; weighted conformal prediction for covariate shift [@tibshirani2019]; conformalised quantile regression [@romano2019] with sample or season folds; quantile regression forest [@meinshausen2006]; deep ensemble [@lakshminarayanan2017]; Monte-Carlo dropout [@gal2016].

*With $m$ reference samples*: (a) bias correction + source CP, the mean reference residual subtracted and the sample-fold split-conformal half-width kept (current practice made conformal); (b) **bias correction + lot scale without replay**, the same bias and lot scale as LotCP-S, but with the half-width taken from past lots standardised by their own full-information bias and scale, so that only the replay of Eq. (5) differs from LotCP-S; (b′) as (b) with the replicate-scan scale only; (c) target-only CP, centred, split conformal on the leave-one-out-centred reference residuals alone, which is valid within the lot but needs $m\ge9$; (d) LotCP-S; (e) LotCP-A; (f) LotCP-R, LotCP-R2 and LotCP-AR (Section 2.7), with seasons of fewer than five lots merged with the next season, compared with (g) LotCP-S at a fixed level $\alpha=0.05$ and with a sensitivity variant that uses plain per-season quantiles. Methods (f)–(g) were planned in writing before they were run and are exploratory. Baselines (b) and (b′) were added after an internal, AI-simulated review of an earlier draft (Section 3.8). Slope/bias correction, pooled recalibration, adaptive conformal inference [@gibbs2021] and spiking are in the supplement.

## 3.5 Evaluation and statistics

For every lot and $m\in\{0,3,5,10,20,30\}$, ⟦100⟧ reference sets are drawn and the scans of the other samples are evaluated; a lot enters at a given $m$ only if it has at least $m+10$ samples. Within a lot, samples have equal weight and scans equal weight within their sample. We report lot-macro *coverage*, the share of lot-draws whose coverage reaches 0.90, mean *width*, and the Winkler *interval score* [@winkler1972; @gneiting2007]. LotCP uses $E=⟦30⟧$ episodes per lot.

*Terms used below.* A *lot-draw* is one lot evaluated with one random set of reference fruit. *Replay* (or an *episode*) is one rehearsal, on a past lot, of what happens at deployment: drawing *m* reference fruit, correcting, and scoring the other fruit. The *interval score* adds the width of an interval to a penalty for each miss, so lower is better and an interval cannot win by being narrow and wrong. A *season interval* is computed from the five season means, and a *season-cluster bootstrap* resamples whole seasons, not single lots; both reflect that lots of one season share the same shift.

The season is the top-level cluster and there are five target seasons. Every headline figure is therefore reported pooled over lots, as the mean of the five season values, and pooled without 2017, the season with two source seasons. Comparisons of methods are summarised by the mean of the five season differences with a descriptive t-interval (4 degrees of freedom) and by the number of seasons in which the difference favours a method. Decision rates and costs, which are pooled over lots, use a two-stage season-cluster bootstrap (seasons resampled, then lots within each resampled season; ⟦2,000⟧ resamples). An exact sign test over five seasons cannot reach $p<0.05$, so no season-level p-value is claimed; mixed models with a season random intercept were fitted but are degenerate with four or five groups and are not used. Lot-level Wilcoxon signed-rank tests [@wilcoxon1945] with Holm correction [@holm1979] and rank-biserial effect sizes [@kerby2014], the original analysis, are in the supplement.

## 3.6 Confirmation data

Before opening a further data set we froze LotCP-S and LotCP-A and committed four endpoints and a success rule to the internal repository (plan file available on request): the interval score of LotCP-S against bias correction + source CP at $m=5$ and 10 (P1, P2), and the share of lot-draws at ≥ 0.90 coverage for LotCP-A against the better of two baselines at $m=10$ and 20 (P3, P4), with five seeds fixed in advance. The data set was the NeoSpectra handheld NIR soil library (Zenodo 10.5281/zenodo.13122321; nine handheld units; organic carbon as log(1 + %); lots are one-degree cells; ⟦20⟧ evaluable lots). Its soil layers belong to the KSSL catalogue, but none of them (⟦0⟧ of ⟦2,106⟧) was among the ⟦19,807⟧ KSSL layers used in our development analyses of soil vis–NIR spectra (Supplementary Note S5). Fresh reference draws on the mango lots were run under the same plan but are not an independent test.

## 3.7 Harvest-decision simulation (exploratory)

For each target lot, each $m\in\{0,3,5,10,20\}$ and twenty reference draws, every non-reference fruit is classified against a specification of 15 % DMC (14 and 16 % in the supplement) by: the point prediction; the bias-corrected point prediction; a split-conformal lower bound from sample-fold residuals ($m=0$); bias correction plus the same source margin; the one-sided LotCP-S bound; and the one-sided LotCP-A bound. No cost data accompany the data set, so costs are *assumed* and expressed in units of the value of one marketable fruit: $c_I=1$, $c_D=1/9$ (so $\alpha^\ast=0.10$), a reference test $c_R=1.5$, and lots of 1000 fruit. The operating point, $\alpha=0.10$, $p=0.8$ and the comparison against the cheapest rule without reference fruit were fixed before the confidence intervals were computed. The level $\alpha$ is also chosen by leave-one-season-out cost minimisation to check the cost-derived level without hindsight. These are scenarios for comparing rules, not estimates of orchard losses.

## 3.8 What was pre-specified, and the role of AI tools

The protocol (hypotheses, splits, methods, metrics) was committed to an internal git repository before any model was trained; it was not deposited with a public registry, so its timing can be verified only from the repository history, which is available on request. The lot scale of LotCP-S was added after inspecting one predictor on 2018; shrinkage was removed after the soil analysis; LotCP-A, the planner, the decision simulation, the published-PLS analysis, the matched baselines and the season-robust replay were added after the main results. For each later addition, including two ideas that failed (Section 4.6), a short plan with a success rule was committed before the analysis was run. All of these are exploratory. Only P1–P4 of Section 3.6 were confirmatory, and of these only the NeoSpectra arm is independent. Supplementary Note S4 lists every deviation with its date and reason, and Supplementary Note S8 tells how the method changed.

The study was carried out with extensive use of an AI assistant (Claude, Anthropic). It searched and screened the literature, wrote and ran the analysis code, proposed and ran experiments, drafted and revised the text, and simulated peer review; analyses added in response to the simulated review (the matched baselines, season-level inference, decision intervals and leverage-based PLS intervals) are marked as such. The authors set the aims and constraints of the study and take full responsibility for its content. Cited references were checked against Crossref, Semantic Scholar or arXiv records during the study, and every number in the text and tables is filled in by a script from the result files and checked by an automated audit for numbers typed by hand.


# 4. Results

## 4.1 Point accuracy and the structure of the error

On the data providers' published split (three seasons for training, n = ⟦10243⟧; the fourth season as test set, n = ⟦1448⟧), the published PLS recipe reached an RMSEP of ⟦1.045⟧ % DMC, against 1.01 % reported by Anderson et al. [@anderson2020]. Our SNV PLS reached ⟦1.392⟧ %, and the CNN without augmentation ⟦1.07⟧–⟦1.08⟧ % against 0.77 % for a tuned and augmented CNN [@walsh2024]. In this reproduction both PLS recipes chose their number of latent variables from 6–30 by grouped cross-validation; the published recipe chose the upper edge of the grid. On the providers' second test set (n = ⟦320⟧) every model had a large negative bias (published PLS ⟦-1.29⟧, SNV PLS ⟦-1.26⟧ % DMC; RMSEP ⟦1.67⟧ and ⟦1.66⟧), the kind of population shift this paper is about. Both PLS recipes are reported below.

Under forward chaining, the error on the next season exceeded the sample-fold cross-validation estimate in every target season (Table 2). The standard deviation of the lot mean residual within a target season was ⟦0.82⟧–⟦1.26⟧ % DMC, of the same order as the within-lot error. Lots scatter around season-specific offsets (Fig. 2). The season-held-out variance components put the between-lot standard deviation at ⟦0.91–1.51⟧ % DMC and the within-lot, between-sample standard deviation at ⟦0.80–1.18⟧ % DMC.

⟦| Target season | RMSECV sample folds | RMSECV lot folds | RMSECV season folds | RMSEP PLS | RMSEP LightGBM | RMSEP 1D-CNN | Bias PLS | SD of lot bias, PLS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2017 | 1.20 | 1.33 | 2.08 | 1.26 | 1.32 | 1.21 | -0.03 | 0.82 |
| 2018 | 1.20 | 1.24 | 1.38 | 1.68 | 1.61 | 1.25 | -0.27 | 1.26 |
| 2019 | 1.25 | 1.28 | 1.45 | 1.77 | 1.82 | 1.70 | 0.71 | 1.18 |
| 2020 | 1.25 | 1.30 | 1.47 | 1.58 | 1.44 | 1.35 | -0.39 | 1.22 |
| 2021 | 1.27 | 1.32 | 1.48 | 1.60 | 1.73 | 1.52 | -0.69 | 1.21 |

Table: Table 2. Point-prediction error (% DMC) under forward chaining. RMSECV: cross-validation inside the source seasons with PLS under three fold units. RMSEP: error on the target season (LightGBM and CNN: mean of three seeds). The last column is the standard deviation of the lot mean residuals in the target season.
⟧

![Fig. 2. Why calibration on held-out samples fails (SNV PLS, forward chaining). (a) Residuals of sample-fold cross-validation in the source seasons and residuals on the following season. (b) Mean residual of each target lot; the bar marks the season mean.](figures/fig3_lot_bias.png){width=6.3in}

## 4.2 Error bars without reference fruit

Split conformal prediction with sample-grouped folds covered ⟦0.823⟧ of reference values on later-season lots at a nominal 0.90 (⟦0.781⟧ without 2017) and reached 0.90 in none of the five seasons (Table 3). The Gaussian band, the quantile forest and conformalised quantile regression with sample folds behaved alike (⟦0.840⟧, ⟦0.841⟧, ⟦0.794⟧). The deep ensemble and Monte-Carlo dropout gave the lowest coverage (⟦0.766⟧, ⟦0.775⟧), because their predictive variance describes the training seasons. With the published PLS recipe, sample-fold split conformal prediction covered ⟦0.843⟧.

Holding out whole seasons is the honest label-free option: pooled coverage became ⟦0.900⟧, at ⟦37⟧ % more width. The pooled figure, however, is carried by 2017. Coverage by season ranged over ⟦0.82–0.99⟧, the season mean was ⟦0.877⟧, and without 2017 it was ⟦0.839⟧. In 2017 only two source seasons were available, the season-held-out models were weak and the intervals were too wide. With four to six past seasons, the next one is not exchangeable with them to within a few coverage points. Weighting calibration points by the likelihood ratio of the unlabelled target spectra reached ⟦0.909⟧ coverage but returned unbounded intervals for ⟦5⟧ % of scans; the shift that matters is a bias in the residual, which reweighting spectra does not repair.

⟦| Predictor | Method | m | Coverage, pooled | Season mean | Excl. 2017 | Seasons ≥ 0.90 | Lot-draws ≥ 0.90 (%) | Width | Interval score |
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
⟧

## 4.3 Error bars with reference fruit

With five to ten reference fruit per lot, LotCP-S raised coverage over sample-fold split conformal prediction by ⟦0.08⟧–⟦0.10⟧ (season mean) in all five seasons, with season intervals excluding zero for both PLS recipes (Table 4, Fig. 3). Its pooled coverage at $m=10$ was ⟦0.919⟧, its season mean ⟦0.911⟧, and without 2017 ⟦0.893⟧. By season, coverage was ⟦0.957⟧, ⟦0.882⟧, ⟦0.902⟧, ⟦0.897⟧ and ⟦0.914⟧ for 2017–2021. LotCP-S therefore removed most of the shortfall but stayed slightly below nominal in the seasons with an adequate source set, and its gain over season-fold split conformal prediction without reference fruit was not distinguishable at season level (Table 4). Excluding 2018, the season used to design the lot scale, the pooled coverage of LotCP-S at $m=10$ is ⟦0.934⟧. In practical terms, with ten fruit cut per lot the SNV PLS error bar is about ±⟦1.7⟧ % DMC (±⟦1.5⟧ % with the published recipe) and contains the true value for roughly nine fruit in ten on average, somewhat fewer in seasons unlike the past ones.

⟦| Comparison | Outcome | PLS | m | Season-mean difference | 95% season interval | Seasons favouring |
|---|---:|---:|---:|---:|---:|---:|
| LotCP-S vs split CP (sample folds, m = 0) | coverage | SNV | 5 | +0.104 | +0.056 to +0.153 | 5/5 |
| LotCP-S vs split CP (sample folds, m = 0) | coverage | SNV | 10 | +0.105 | +0.056 to +0.153 | 5/5 |
| LotCP-S vs split CP (sample folds, m = 0) | coverage | Pub. | 5 | +0.081 | +0.011 to +0.152 | 5/5 |
| LotCP-S vs split CP (sample folds, m = 0) | coverage | Pub. | 10 | +0.086 | +0.013 to +0.158 | 5/5 |
| LotCP-S vs split CP (season folds, m = 0) | coverage | SNV | 5 | +0.033 | -0.020 to +0.086 | 4/5 |
| LotCP-S vs split CP (season folds, m = 0) | coverage | SNV | 10 | +0.034 | -0.020 to +0.087 | 4/5 |
| LotCP-S vs split CP (season folds, m = 0) | coverage | Pub. | 5 | +0.023 | -0.044 to +0.090 | 3/5 |
| LotCP-S vs split CP (season folds, m = 0) | coverage | Pub. | 10 | +0.027 | -0.041 to +0.095 | 3/5 |
| LotCP-S vs bias corr. + source CP | interval score | SNV | 5 | +0.214 | -0.033 to +0.461 | 5/5 |
| LotCP-S vs bias corr. + source CP | interval score | SNV | 10 | +0.269 | +0.050 to +0.488 | 5/5 |
| LotCP-S vs bias corr. + source CP | interval score | Pub. | 5 | +0.218 | +0.047 to +0.388 | 4/5 |
| LotCP-S vs bias corr. + source CP | interval score | Pub. | 10 | +0.264 | +0.084 to +0.445 | 5/5 |
| LotCP-S vs bias corr. + source CP | coverage | SNV | 5 | -0.025 | -0.059 to +0.009 | 1/5 |
| LotCP-S vs bias corr. + source CP | coverage | SNV | 10 | -0.032 | -0.061 to -0.002 | 1/5 |
| LotCP-S vs bias corr. + source CP | coverage | Pub. | 5 | -0.033 | -0.056 to -0.010 | 0/5 |
| LotCP-S vs bias corr. + source CP | coverage | Pub. | 10 | -0.038 | -0.057 to -0.018 | 0/5 |
| LotCP-S vs same scale without replay | interval score | SNV | 5 | +0.004 | -0.075 to +0.083 | 3/5 |
| LotCP-S vs same scale without replay | interval score | SNV | 10 | -0.053 | -0.133 to +0.027 | 1/5 |
| LotCP-S vs same scale without replay | interval score | Pub. | 5 | +0.015 | -0.053 to +0.083 | 4/5 |
| LotCP-S vs same scale without replay | interval score | Pub. | 10 | -0.028 | -0.081 to +0.025 | 2/5 |
| LotCP-S vs same scale without replay | coverage | SNV | 5 | +0.024 | +0.014 to +0.034 | 5/5 |
| LotCP-S vs same scale without replay | coverage | SNV | 10 | +0.014 | +0.004 to +0.023 | 5/5 |
| LotCP-S vs same scale without replay | coverage | Pub. | 5 | +0.023 | +0.018 to +0.028 | 5/5 |
| LotCP-S vs same scale without replay | coverage | Pub. | 10 | +0.011 | +0.003 to +0.019 | 5/5 |
| LotCP-A vs LotCP-S | lot-draws ≥ 0.90 | SNV | 5 | +26.1 | +13.7 to +38.5 | 5/5 |
| LotCP-A vs LotCP-S | lot-draws ≥ 0.90 | SNV | 10 | +26.9 | +12.9 to +41.0 | 5/5 |
| LotCP-A vs LotCP-S | lot-draws ≥ 0.90 | Pub. | 5 | +26.8 | +14.4 to +39.1 | 5/5 |
| LotCP-A vs LotCP-S | lot-draws ≥ 0.90 | Pub. | 10 | +29.0 | +14.1 to +43.9 | 5/5 |

Table: Table 4. Season-level comparisons (all exploratory; Section 3.8). Differences are oriented so that positive values favour the first method (lower interval score, higher coverage or share). Season-mean difference: mean of the five season differences; season interval: descriptive t-interval on those five values (4 df). With five seasons an exact sign test cannot reach p < 0.05 (smallest two-sided p = 0.0625); all lot-level tests are in the supplementary tables.
⟧

![Fig. 3. Lot-macro coverage, mean width and interval score against the number of reference fruit per lot (SNV PLS, forward chaining, ⟦137⟧ target lots, nominal 0.90). Dashed lines: split conformal prediction without reference fruit.](figures/fig4_main.png){width=6.5in}

*What the replay buys.* The matched baseline (b) uses the same bias and lot scale as LotCP-S and differs only in how the multiplier is calibrated. It covered ⟦0.899⟧ at $m=5$ and ⟦0.908⟧ at $m=10$ (⟦0.883⟧ without 2017), ⟦3.7⟧, ⟦2.4⟧ and ⟦1.4⟧ points less than LotCP-S at $m=3$, 5 and 10, with season intervals excluding zero for both PLS recipes. Its interval score was equal or slightly lower (by ⟦0.05⟧ at $m=10$; season interval for the advantage of LotCP-S ⟦-0.13 to +0.03⟧). Replaying the $m$-shot procedure on past lots thus prices the error of estimating the bias and scale from a few fruit. It protects coverage when $m$ is small. It does not make intervals narrower. The lot scale is what narrows them. Against the replicate-scan scale alone (b′), LotCP-S had a lower interval score in at least four of five seasons at every $m$ and at least equal coverage.

*Current practice.* Bias correction with the sample-fold half-width over-covered (⟦0.938⟧ at $m=10$) because a remnant of the lot effect in sample-fold residuals offsets the ignored estimation error of the bias. Its half-width cannot shrink with $m$, and LotCP-S had a lower interval score from $m=10$ with SNV PLS (season interval ⟦+0.05 to +0.49⟧) and from $m=5$ with the published recipe, at the price of lower coverage: bias correction covered more in four or five of five seasons and reached 0.90 in more seasons (Table 3). On these data it is the safer simple option when coverage matters more than width. In the pre-specified confirmation on independent soil data, the interval-score advantage over this baseline was not confirmed (Section 4.7). Target-only calibration on the reference fruit alone needs $m\ge9$, was conservative and ⟦34⟧ % wider than LotCP-S at $m=10$, and matched its interval score by $m=20$ (⟦4.29⟧ against ⟦4.25⟧). The other predictors, protocols, nominal levels, reference-value noise and the component ablation are in Supplementary Note S5. Without repeated scans per fruit, LotCP-S and bias correction did not differ significantly in interval score (supplementary table S6b).

## 4.4 Lot-level assurance

Near-nominal average coverage still leaves many lots below the nominal level: with LotCP-S at $m=10$ only ⟦69⟧ % of lot-draws reached 0.90 (Fig. 4). LotCP-A, asked for 0.90 coverage in nine lots of ten, brought this share to ⟦92⟧ % pooled at $m=10$, but ⟦87⟧ % without 2017. By season it was ⟦98⟧, ⟦86⟧, ⟦86⟧, ⟦89⟧ and ⟦93⟧ % for 2017–2021: the target was met in ⟦2⟧ of 5 seasons with SNV PLS and in ⟦2⟧ with the published recipe. The lot-level guarantee rests on exchangeable lots, and season shift breaks it in the same way as it breaks the marginal one. LotCP-A did raise the share relative to LotCP-S in all five seasons (Table 4), at ⟦25⟧ % more width at $m=10$.

The extra width buys no efficiency. Measured as the share of lots whose draw-averaged coverage reaches 0.90, LotCP-A at $m=10$ (⟦96.4⟧ %, width ⟦4.30⟧) is matched by LotCP-S run at $\alpha=0.05$ (⟦94.9⟧ %, width ⟦4.29⟧). LotCP-A is a way of choosing that level from past lots without target labels. It is not a cheaper route to assurance.

![Fig. 4. Lot-level assurance (SNV PLS, forward chaining). (a) Share of lot-draws in which at least 90 % of the fruit is covered; dotted lines mark the targets of LotCP-A for δ = 0.10 and δ = 0.20. (b) Mean interval width.](figures/fig12_assurance.png){width=6.3in}

## 4.5 Season-robust replay

Table 110 shows what calibrating within each past season changes (exploratory; plan stated before running). With ten reference fruit, LotCP-R2 brought lot-macro coverage to at least 0.90 in all five target seasons for all four predictors, at ⟦7⟧–⟦11⟧ % more width than LotCP-S, which reached 0.90 in two seasons. The lowest season coverage across predictors was ⟦0.904⟧, and without 2017 the pooled coverage was ⟦0.923⟧ for SNV PLS (LotCP-S ⟦0.893⟧). LotCP-R, the more conservative largest multiplier, did the same at ⟦15⟧–⟦18⟧ % more width. The obvious alternative, running LotCP-S at a fixed smaller level ($\alpha=0.05$), also reached 0.90 in every season but cost ⟦24⟧–⟦26⟧ % more width: the season-robust replay obtained season-level validity at less than half that price, because the inflation it applies is set by how much the past seasons actually disagree rather than fixed in advance. The multipliers grew with the number of past seasons (LotCP-R2, SNV PLS: from ⟦0.98⟧ with two source seasons to ⟦1.25⟧ with six).

⟦| Predictor | LotCP-S | LotCP-R2 | LotCP-R | LotCP-S at α = 0.05 | R, plain quantiles | LotCP-A | LotCP-AR | AR, plain quantiles |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SNV PLS | 2/5 | 5/5 (+7 %) | 5/5 (+16 %) | 5/5 (+24 %) | 4/5 (+1 %) | 2/5 | 5/5 (+8 %) | 3/5 (+2 %) |
| Published PLS | 2/5 | 5/5 (+11 %) | 5/5 (+18 %) | 5/5 (+25 %) | 3/5 (+0 %) | 2/5 | 5/5 (+12 %) | 4/5 (+6 %) |
| LightGBM | 2/5 | 5/5 (+9 %) | 5/5 (+15 %) | 5/5 (+26 %) | 3/5 (+0 %) | 2/5 | 5/5 (+9 %) | 3/5 (+3 %) |
| 1D-CNN | 2/5 | 5/5 (+8 %) | 5/5 (+16 %) | 5/5 (+25 %) | 4/5 (+0 %) | 1/5 | 4/5 (+8 %) | 4/5 (+4 %) |

Table: Table 110. Season-robust replay (forward chaining, five target seasons, m = 10, nominal 0.90; exploratory). Columns LotCP-S to 'R, plain quantiles': number of target seasons whose lot-macro coverage reaches 0.90. Columns LotCP-A to 'AR, plain quantiles': number of seasons in which at least 90 % of lot-draws reach 0.90 coverage (the lot-level target). In brackets: change of mean width relative to LotCP-S (marginal columns) or LotCP-A (lot-level columns). LotCP-R/R2: largest/second-largest per-season conformal multiplier; plain: per-season empirical quantile without the conformal correction (sensitivity analysis). Results for m = 5 are in results/cycle4.
⟧

At lot level, LotCP-AR met the target of 0.90 coverage in nine lots of ten in ⟦4⟧–⟦5⟧ of five seasons across predictors, against ⟦1⟧–⟦2⟧ for LotCP-A, at ⟦8⟧–⟦12⟧ % more width. The same held at $m=5$ (results/cycle4).

The sensitivity analysis locates the mechanism. With plain per-season quantiles, that is without the conformal term for the next lot of a season, the marginal gain disappeared (coverage of 0.90 in ⟦3⟧–⟦4⟧ seasons, width unchanged), while most of the lot-level gain remained (⟦3⟧–⟦4⟧ seasons at ⟦2⟧–⟦6⟧ % more width). Past seasons contain fourteen to fifty-six lots each, so each season pins down its own quantile only loosely; accounting for that within each season, and then taking an upper order statistic across seasons, is what restores season-level coverage. A pooled quantile hides both effects behind the largest seasons.

## 4.6 Two ideas that did not help

*Learning the season shift within the season.* Lots of a season are harvested in date order, and the reference fruit of earlier lots could reveal how the current season differs from past ones. We inflated the next lot's half-width by the ratio of leave-one-out reference scores in the current season to those in past seasons, shrunk towards one by an amount tuned on the source seasons only. The rule stated in advance (closer to 0.90 in at least four of five seasons for both predictors) failed in all four configurations; without 2017, coverage moved from ⟦0.894⟧ to ⟦0.900⟧ (SNV PLS, $m=10$). The reference fruit of a few earlier lots estimate a tail quantile too noisily to correct it.

*Label-free warning signs.* If unusual spectra flagged biased lots, reference fruit could be concentrated where they are needed. Hotelling's $T^2$, the spectral residual $Q$, the replicate-scan variance and the offset of the lot's mean prediction were computed for every lot without reference values. The indicator chosen on source lots correlated with the absolute lot bias on target lots at Spearman ⟦0.20⟧, below the threshold of 0.30 set in advance, so adaptive budgets were not pursued. In these data a lot's bias cannot be read from its spectra; it has to be measured, which is the premise of the reference-fruit approach.

## 4.7 Pre-specified confirmation

⟦| Data set | Endpoint | Comparison | Outcome | m | Lots | Mean difference | 95% CI | Holm p | r | Criterion met |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Mango (re-draw; lots seen during development) | P1 | LotCP-S - bias corr. + source CP | interval score | 5 | 137 | -0.165 | -0.269 to -0.058 | <0.001 | -0.37 | yes (re-draw check) |
| Mango (re-draw; lots seen during development) | P2 | LotCP-S - bias corr. + source CP | interval score | 10 | 137 | -0.248 | -0.352 to -0.137 | <0.001 | -0.53 | yes (re-draw check) |
| Mango (re-draw; lots seen during development) | P3 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 10 | 137 | +0.037 | +0.010 to +0.064 | <0.001 | +0.40 | yes (re-draw check) |
| Mango (re-draw; lots seen during development) | P4 | LotCP-A - bias corr. + source CP | share of lots ≥ 0.90 | 20 | 129 | +0.121 | +0.072 to +0.175 | <0.001 | +0.44 | yes (re-draw check) |
| NeoSpectra soil (untouched) | P1 | LotCP-S - bias corr. + source CP | interval score | 5 | 20 | -0.049 | -0.086 to -0.013 | 0.066 | -0.54 | no |
| NeoSpectra soil (untouched) | P2 | LotCP-S - bias corr. + source CP | interval score | 10 | 20 | -0.028 | -0.079 to +0.023 | 0.294 | -0.28 | no |
| NeoSpectra soil (untouched) | P3 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 10 | 20 | +0.073 | +0.033 to +0.116 | 0.015 | +0.71 | yes |
| NeoSpectra soil (untouched) | P4 | LotCP-A - target-only CP, centred | share of lots ≥ 0.90 | 20 | 10 | +0.207 | +0.178 to +0.235 | 0.008 | +1.00 | uninformative |

Table: Table 109. Pre-specified confirmation of the frozen method (internally committed plan, available on request) on five seeds fixed in advance (100–104), 20 reference draws per seed, lot and m. Unit of analysis: target lot; Wilcoxon signed-rank test, Holm correction over the four endpoints per data set; 95 % CI: bootstrap over lots; r: matched-pairs rank-biserial correlation. An endpoint is confirmed when Holm p < 0.05, the CI excludes 0 and |r| ≥ 0.2 in the expected direction. Negative interval-score differences and positive share differences favour the proposed method. The mango rows are fresh reference draws on lots examined during development and are not an independent confirmation. P3 and P4 compare coverage shares without a width constraint (Section 4.4); P4 had too few lots and is counted as uninformative.
⟧

On the independent NeoSpectra data (Table 109), the efficiency endpoints failed: the interval-score difference to bias correction + source CP at $m=5$ was ⟦-0.049⟧ (95 % CI ⟦-0.086⟧ to ⟦-0.013⟧, Holm p ⟦0.066⟧) and at $m=10$ ⟦-0.028⟧ (p ⟦= 0.294⟧). The assurance endpoint P3 met its criterion: ⟦95⟧ % of lot-draws at ≥ 0.90 for LotCP-A against ⟦88⟧ % for target-only CP, at a width of ⟦1.19⟧ against ⟦1.13⟧. As Section 4.4 shows, a share endpoint without a width constraint favours the wider method, so P3 confirms that LotCP-A delivers its requested share on exchangeable lots, not that it does so efficiently. P4 is uninformative (⟦10⟧ lots). Split conformal prediction already covered ⟦0.930⟧ on these data: cells within one survey programme are close to exchangeable, so the confirmation could not test a seasonal shift. The mango rows are fresh draws on development lots and are not independent.

## 4.8 Harvest decisions (exploratory)

At the operating point fixed before the intervals were computed, deciding on point predictions cost ⟦8.7⟧ units per 100 fruit under the assumed costs (SNV PLS; Table 5). Any conformal lower bound cost about ⟦5⟧ units less: the split-conformal bound without reference fruit cost ⟦3.69⟧ units (95 % CI ⟦2.11⟧ to ⟦5.16⟧). The difference to point decisions had a confidence interval excluding zero and favoured the bound in all five seasons, for both PLS recipes. No further saving from reference fruit was detectable at this operating point. The LotCP-S bound with $m=3$, 5 and 10 differed from the bound without reference fruit by ⟦-0.28⟧, ⟦-0.12⟧ and ⟦+0.53⟧ units, all with intervals including zero, and bias correction with a source margin behaved alike. Even if reference tests cost nothing, the difference for LotCP-S at $m=5$ would be ⟦-0.87⟧ units (interval ⟦-2.11⟧ to ⟦+0.07⟧). The intervals of about ±⟦1.1⟧ units cannot exclude a modest saving. The split-conformal bound was named as comparator because it was the cheapest rule without reference fruit for both predictors; the point rule is a weak comparator, more costly than withholding every fruit under these costs. The bound accepted far fewer immature fruit than the point prediction (⟦0.5⟧ against ⟦8.0⟧ per 100 fruit at $m=5$) and withheld more mature fruit (⟦21⟧ against ⟦6⟧).

At lot level the point rule harvested ⟦7.3⟧ % of not-ready lots [⟦0.0⟧, ⟦22.4⟧] and delayed ⟦20⟧ % of ready lots. The bound without reference fruit harvested ⟦3.7⟧ % of not-ready lots and delayed ⟦69⟧ % of ready lots; with five reference fruit, LotCP-S harvested ⟦0.2⟧ % and delayed ⟦59⟧ %. The intervals overlap: ⟦82⟧ not-ready and ⟦55⟧ ready lots in five seasons cannot resolve differences of this size. Choosing $\alpha$ by leave-one-season-out cost minimisation was not better than the cost-derived level $\alpha^\ast$ (LotCP-S, $m=10$: ⟦2.70⟧ against ⟦2.47⟧ units at $\alpha^\ast=0.10$; these are means over the five seasons, excluding the cost of reference tests, which does not depend on $\alpha$, whereas Table 6 pools over lots and includes it). Full trade-off curves are in Fig. 5 and Supplementary Note S7.

⟦| PLS | Rule | m | Cost / 100 fruit [95% CI] | Δ vs split-CP bound [95% CI] | Premature lots (%) [CI] | Ready lots delayed (%) [CI] |
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

Table: Table 5. Harvest decisions at the operating point fixed before this analysis (exploratory; specification 15 % DMC, bounds at α = 0.10, lot harvested when ≥ 80 % of its scanned fruit are accepted, ASSUMED costs c_I = 1, c_D = 1/9, c_R = 1.5 per reference fruit, lots of 1000 fruit; 137 target lots). Cost in units of the value of one marketable fruit, including reference tests. Δ: cost difference to the split-conformal lower bound, the cheapest rule without reference fruit. 95 % CIs: two-stage season-cluster bootstrap of the pooled values.
⟧

![Fig. 5. Trade-off between harvesting immature fruit and holding back mature fruit (SNV PLS, specification 15 % DMC, ⟦137⟧ later-season lots; exploratory). Each curve traces one rule as its level α varies from 0.02 to 0.5; crosses are rules without a level. (a) Fruit-level decision. (b) Lot-level decision: a lot is harvested when at least 80 % of its scanned fruit are accepted.](figures/fig14_harvest_frontier.png){width=6.5in}

## 4.9 Planning the number of reference fruit

The width planned from past lots matched the realised width with a median absolute relative difference of ⟦7⟧ % over all predictors, seasons and values of $m$ (Fig. 6). The error depended on the number of source seasons: LotCP-S widths were over-forecast by ⟦17⟧ % with two source seasons (2017) and within ⟦8⟧ % with three to six. Most of the reduction in width came from the first five reference fruit; beyond ten the curve was flat.

![Fig. 6. Reference-budget planning. (a) Width planned from past lots against the mean width realised on the following season; each point is one target season, predictor, number of reference fruit and variant. (b) Planned and realised curves for SNV PLS, averaged over target seasons.](figures/fig13_planning.png){width=6.3in}


# 5. Discussion

**What the audit shows.** An error bar calibrated inside the training seasons, whether by cross-validation, a conformal quantile on held-out samples or the predictive variance of a neural network, describes past lots. On later-season mango lots it was too narrow: pooled over lots, by ⟦6⟧ to ⟦13⟧ coverage points at a nominal 90 % across the Gaussian band, sample-fold split CP and CQR, the quantile forest, the deep ensemble and MC dropout; for sample-fold split CP with SNV PLS the shortfall by season ranged from ⟦1.6⟧ to ⟦14.0⟧ points, and the shortfall was concentrated in a minority of badly covered lots. Holding out whole seasons is the honest repair without reference fruit, but with four to six past seasons it reached nominal coverage only in the season that happened to be over-covered. These findings agree in direction with the loss of coverage reported under instrument transfer [@kayaoglu2026] and with the long-standing observation that NIR accuracy degrades on new populations [@nicolai2007; @anderson2020]; the audit adds the lot-by-lot, season-by-season picture that a decision against a specification needs.

**What reference fruit and the calibration add.** A few reference fruit per lot did most of the work: once the lot bias was corrected, every method moved close to or above nominal coverage. Within LotCP-S, the lot scale estimated partly from repeated scans gave narrower intervals than bias correction with a fixed half-width, though this gain was not confirmed on independent soil data and vanished without repeated scans, and the replay of the $m$-shot procedure kept coverage ⟦1⟧–⟦4⟧ points higher than the same correction without replay. Pooled over past lots, however, the calibration still under-covered in seasons unlike the largest past ones: without 2017, LotCP-S covered ⟦0.893⟧.

**Seasons as the unit of calibration.** The season-robust replay changes the unit at which exchangeability is assumed. Each past season is treated as a small calibration set of lots, and the next season as one more draw from the same population of seasons. This explains why pooling failed and why the remedy works: a pooled quantile is dominated by the seasons with most lots and ignores how poorly each season pins down its own tail, whereas calibrating within seasons and taking an upper order statistic across them prices both. The guarantee is modest with few seasons (at least ⟦2⟧/⟦3⟧ for the first target season, ⟦6⟧/⟦7⟧ for the last with the largest multiplier), but it is explicit, and it tells a calibration manager how many seasons of history are needed for a stated season-level confidence. Two cheaper ideas did not help: the reference fruit of earlier lots in the same season were too few to estimate a season's tail, and label-free spectral statistics did not predict which lots were biased. Season-to-season shift has to be priced from the spread of past seasons and from reference fruit; it could not be detected in advance from the spectra.

**What changes in the decision.** In the exploratory simulation, the benefit came from replacing the point value by any calibrated lower bound, which cut the assumed cost by about ⟦5⟧ units per 100 fruit in every season and kept immature fruit out of the harvest. Reference fruit did not lower the expected cost further at the pre-stated operating point. Their value lies in making the bound mean what it says for the lot in hand, which matters when the level is set from costs, and in a lower rate of delayed ready lots that five seasons could not resolve statistically. The cost-derived level $\alpha^\ast$ was as good as a level chosen from other seasons, which supports the newsvendor reading of the rule.

**Practical procedure.** (0) Where coverage must hold season by season, use the season-robust multiplier (LotCP-R2, or LotCP-AR for a lot-level statement). Where only single scans are taken and width matters little, bias correction with a sample-fold half-width was a safe simple option on these data; LotCP-S is preferable when repeated scans are available, when the half-width should shrink with *m*, or with flexible predictors for which that shortcut under-covered (Supplementary Note S5). (1) Build the calibration with season-grouped cross-validation and keep the season-held-out residuals with lot and sample identifiers. (2) Before the season, read the planned width for each $m$ and state the cost ratio, which fixes $\alpha^\ast$. (3) In the orchard, scan the fruit of a lot with two or three scans per fruit, test five to ten randomly chosen fruit, and harvest a fruit or lot when the calibrated lower bound meets the specification. (4) After the season, add the lot to the calibration set and check the realised coverage.

# 6. Limitations

In order of importance:

1. *Retrospective only.* All results replay archived data. The workflow has not been used to decide a harvest, and the paper does not show that it reduces losses in an orchard. A prospective trial that records decisions and verifies them on harvested fruit is the necessary next step.
2. *Few seasons and one fruit data set.* Five target seasons are a small sample at the level that dominates the error, and the confidence intervals reflect this. We found no second public fruit NIR data set with lot and season structure; the soil libraries test the coverage audit and the calibration on another material but have no season level, and the independent soil data showed little shift to repair.
3. *Guarantees hold only approximately, and the season-level one is weak with few seasons.* Pooled guarantees assume exchangeable lots and failed under season shift. The season-robust replay assumes exchangeable seasons, which a trend in climate, cultivars or instruments would violate, and with two to six past seasons its season-level probability is only ⟦0.67⟧–⟦0.86⟧; it was developed and evaluated on seasons already examined, so it needs confirmation on new seasons.
4. *Exploratory components.* The lot scale was designed after inspecting 2018, and LotCP-A, the planner, the decision simulation and the matched baselines were added after the main results. The protocol was committed internally, not publicly registered.
5. *Assumed costs and illustrative decision rules.* Costs are expressed in units of fruit value, the specification of 15 % DMC and the 80 % lot rule are illustrative, and maturity is not determined by DMC alone.
6. *Repeated scans richer than routine practice.* The data contain scans from several instrument units and temperatures per fruit; the efficiency gain of LotCP-S depended on them.
7. *Reference sampling.* Reference fruit are assumed to be drawn at random and measured as accurately as the calibration set.

# 7. Conclusion

Error bars for handheld NIR predictions of mango dry matter, calibrated inside the training seasons, did not keep their coverage on later-season lots. A few reference fruit per lot, with a few-shot conformal calibration that corrects bias and scale, restored coverage on average, but not season by season, because seasons differed by more than past lots suggested. Calibrating within each past season and taking an upper order statistic across seasons gave an explicit season-level guarantee and, in exploratory analyses, restored 90 % coverage in every season for four predictors at less than half the extra width of a fixed higher confidence level. Learning the shift from earlier lots of the season and spectral warning signs did not help. In an exploratory decision analysis, a calibrated lower bound rather than the point value lowered the assumed cost of harvest decisions. Confirmation on new seasons and a prospective orchard trial are the steps that remain.

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

**Proposition 3 (season level, LotCP-R).** Let seasons $1,\dots,S+1$ be exchangeable random collections of lots, with season $S+1$ the new one, and let $T_s$ be the multiplier of Eq. (7) computed with a common, fixed score function from the lots of season $s$. Let $T_{(k)}$ be the $k$-th largest of $T_1,\dots,T_S$. Then $\mathbb{P}\{T_{S+1}\le T_{(k)}\}\ge (S+1-k)/(S+1)$. If, in addition, lots are exchangeable within each season, a new lot $Z$ of season $S+1$ with a random reference set is covered by the interval with multiplier $T_{(k)}$ with probability at least $1-\alpha$ on the event $\{T_{S+1}\le T_{(k)}\}$, conditional on the season.

*Proof.* $T_1,\dots,T_{S+1}$ are exchangeable, because the seasons are and the same function computes each $T_s$. The rank of $T_{S+1}$ among the $S+1$ values is therefore uniform (ties broken at random), and $T_{S+1}$ exceeds $T_{(k)}$ only if it is among the $k$ largest, which has probability at most $k/(S+1)$. For the second claim, condition on season $S+1$: its lots and the new lot $Z$ are exchangeable, so by Proposition 1 applied within the season, the interval with multiplier $T_{S+1}$ covers $Z$ with probability at least $1-\alpha$, and a larger multiplier can only increase coverage. $\square$

*Remark 3.* Replacing $T_s$ by any statistic $T_s'\ge T_s$ computed in the same way for every season keeps the first claim. In particular the plain per-season quantile (without the $+\infty$ mass), used as a sensitivity analysis, satisfies it too, but the coverage step then holds only approximately. In the implementation the fitted constants come from the $S$ past seasons, not from all $S+1$, a small asymmetry; in simulations with exchangeable seasons the event frequency was within Monte-Carlo error of the bound (unit tests of the code).

*Scope of the statements.* Proposition 1 is the hierarchical conformal guarantee of Lee et al. [@lee2023] written for a score that depends on a random reference set, with three nested levels and unequal group sizes; Proposition 2 is a statement of the probably-approximately-correct type [@park2022] at the level of the lot. Both require the predictor and the constants to be fixed independently of the calibration lots and the new lot to be exchangeable with past lots. Section 2.5 lists how the implementation departs from these conditions, and the experiments measure the consequences.

# Appendix B. Supplementary material

Supplementary Notes S1–S8 (robustness, computation, error analysis, deviations, ablation and generalisation, prototype, full decision analysis, development history) and supplementary tables S1–S24 accompany this article; the pre-specified protocol files are available on request with the code.

# References

::: {#refs}
:::
