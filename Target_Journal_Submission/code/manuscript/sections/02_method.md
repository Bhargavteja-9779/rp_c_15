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

the multiplier that would be valid for a new lot exchangeable with the $K_s$ lots of season $s$. LotCP-R uses the largest of the $S$ values and LotCP-R2 the second largest. LotCP-AR does the same with the lot-level quantile of Eq. (6). If seasons are exchangeable, the $k$-th largest of $S$ past-season multipliers is at least the corresponding multiplier of the new season with probability at least $(S+1-k)/(S+1)$, and a new lot of the new season is covered with probability at least $1-\alpha-k/(S+1)$ (Appendix A, Proposition 3). With few seasons this is weak: for LotCP-R2 ($k=2$) the season-level probability is $(S-1)/(S+1)$, one third with two past seasons and five sevenths with six. Calibrating within environments and then across them was introduced for multi-environment prediction by Duchi et al. [@duchi2024multienv], whose two-level construction and $(\alpha,\delta)$ coverage also anticipate LotCP-A; max-type aggregation over source distributions guarantees coverage for points from the *source* distributions [@yang2026mdcp; @tsibulsky2025], and distributionally robust calibration offers another way to inflate intervals under shift [@cauchois2024robust]. What is specific here is the *m*-shot replay inside each season, with season-held-out residuals and the lot scale, and the evaluation on real harvest seasons.

## 2.8 Planning the number of reference fruit

The replay yields, for every $m$ and from past lots alone, the multiplier and the mean lot scale $\bar s_m$ over episodes, and hence a planned width $2\hat q_m\bar s_m$. The curve of planned width against $m$ can be drawn before the season and turns the choice of $m$ into an explicit trade between laboratory effort and precision. Calibration costs one extra model fit per source season, done offline; deployment computes two means and one variance per lot.

## 2.9 From a bound to a harvest decision

Let $t$ be the minimum DMC a fruit must reach, $c_I$ the cost of accepting an immature fruit and $c_D$ the cost of withholding a mature one. If the probability that a fruit is below $t$ were known, expected cost would be minimised by accepting it when that probability is at most $\alpha^\ast=c_D/(c_I+c_D)$, the familiar newsvendor or Bayes threshold. A lower bound $L_{\alpha}(x)=f(x)+\hat b-\hat q^-_m\hat s$, with $\hat q^-_m$ calibrated as in Eq. (5) on the signed score $(\hat b-r)/\hat s$, gives the rule *harvest if* $L_{\alpha^\ast}(x)\ge t$, *otherwise wait or re-test*. Because the guarantee is marginal, not conditional on the spectrum, this rule is a calibrated approximation to the cost-optimal rule. A lot is harvested when at least a share $p$ of its scanned fruit is accepted, and it is called ready when at least a share $p$ of its fruit truly meets $t$ ($p=0.8$).
