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
