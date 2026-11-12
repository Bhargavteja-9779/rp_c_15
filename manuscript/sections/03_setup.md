# 5. Experimental setup

## 5.1 Data

We use the public "Mango DMC and NIR spectra" data set, version 6 [@mangodata] (CC BY 4.0), which extends the data of Anderson et al. [@anderson2020; @anderson2021] and Walsh et al. [@walsh2024] with further seasons and instrument units. It contains {{V:n_spectra}} spectra of intact mango fruit acquired with handheld spectrometers in interactance geometry [@anderson2021], each paired with the oven-dry DMC of the tissue under the scanned position. The file identifies the harvest season ({{V:n_seasons}} seasons, 2015–2021), the growing region (Northern Territory or Queensland, Australia), the cultivar ({{V:n_cultivars}} cultivars), the physiological stage, the fruit temperature class, the instrument unit ({{V:n_instruments}} units), the reference sample ({{V:n_samples}} samples) and the population ({{V:n_lots}} populations). A population is a set of fruit from one orchard block and harvest date; we call it a lot. Every sample was scanned repeatedly (median {{V:median_scans}} scans per sample; different instrument units, and for a subset three fruit temperatures). Table 1 summarises the data by season and Fig. 2 shows the distribution of reference values, the number of lots and the mean spectra.

{{T:dataset}}

![Fig. 2. The data set. (a) Reference dry matter content by season. (b) Number of harvest lots by season. (c) Mean absorbance spectra of three seasons in the analysis window.](figures/fig2_data.png){width=6.3in}

We use the 684–990 nm window at 3 nm steps (103 variables), the range that gave the best PLS results in the original study [@anderson2020]. All spectra are retained. The provider's outlier flags are not applied in the main analysis because we cannot establish that they were assigned without reference to prediction residuals; their effect is examined in Section 9.

## 5.2 Protocols and leakage control

*Forward chaining (primary).* For each target season $T\in\{2017,\dots,2021\}$ the source data are all seasons before $T$. Nothing from season $T$ or later enters training, preprocessing, hyper-parameter selection or calibration, except the $m$ reference samples of the lot under test. This gives {{V:n_target_lots}} target lots with at least 20 samples.

*Leave-one-season-out (secondary).* Each of the seven seasons is the target in turn and all other seasons are the source. This protocol uses later seasons to predict earlier ones and is reported as a robustness check only.

*Further shifts.* (i) Only the two seasons preceding $T$ as source; (ii) one growing region as target and the other as source; (iii) one cultivar as target and all others as source (five cultivars with enough lots).

Repeated scans of a sample share one reference value, so a random split of spectra would place near-duplicates on both sides. All folds are grouped: a sample never straddles a fold in the sample-grouped scheme, a lot never does in the lot-grouped scheme, and a season never does in the season-grouped scheme. The data provider's warning against random splitting is thereby respected. Reference samples are drawn at the sample level, and all scans of a drawn sample are removed from the evaluation set of that draw. Spectral pre-treatments are row-wise and learn nothing from other spectra; scaling constants of the neural network are computed on the training fold only.

## 5.3 Point predictors

*PLS.* Standard normal variate [@barnes1989] followed by a Savitzky–Golay second derivative (17-point window, second-order polynomial) [@savitzky1964] and partial least squares regression [@wold2001]. The number of latent variables is chosen from $\{8,10,\dots,20\}$ by leave-one-season-out cross-validation inside the source data.

*LightGBM.* Gradient-boosted trees [@ke2017] on the same pre-treated spectra (400 trees, learning rate 0.05, 31 leaves, minimum 40 samples per leaf, row subsampling 0.8, column subsampling 0.5).

*1D-CNN.* Three convolution layers (16, 32 and 64 filters; kernel sizes 7, 5 and 3; strides 1, 2 and 2; ELU activations), a 64-unit dense layer with dropout 0.1 and a linear output ({{V:cnn_params}} parameters), in the spirit of compact networks used for NIR regression [@cui2018; @walsh2024]. Inputs are SNV spectra standardised per wavelength. Training uses AdamW (weight decay $10^{-4}$), a one-cycle learning-rate schedule peaking at $10^{-3}$, batch size 256 and 20 epochs. No early stopping is used, so no validation split is needed.

LightGBM and the CNN are run with three seeds fixed before the experiments (0, 1, 2). All results are reported for every seed or as mean and standard deviation over seeds; no seed was selected. Hyper-parameters of LightGBM and the CNN were set once from common defaults and not tuned on any target season. PLS is the primary predictor because it is the reference method of the field and is deterministic.

## 5.4 Interval methods compared

*Without reference samples* ($m=0$). (1) Gaussian band $\pm z_{1-\alpha/2}\cdot$RMSECV, the implicit practice in chemometrics. (2–4) Split conformal prediction with residuals held out by sample, by lot or by season (cross-conformal with the respective folds). (5) Weighted conformal prediction for covariate shift [@tibshirani2019], with the likelihood ratio between the scans of the target lot and the source scans estimated by logistic regression on the PLS scores; it uses the unlabelled spectra of the target lot. (6–7) Conformalised quantile regression [@romano2019] with LightGBM quantile models, calibrated with sample folds or with season folds. (8) Quantile regression forest [@meinshausen2006] on PLS scores (200 trees, minimum leaf size 10). (9) Deep ensemble of five heteroscedastic CNNs trained with the Gaussian negative log-likelihood [@lakshminarayanan2017]. (10) Monte-Carlo dropout with 30 passes on one such network [@gal2016]. (11–12) LotCP and LotCP-S with $m=0$.

*With $m$ reference samples.* (a) Bias correction + source CP: the mean reference residual is subtracted and the split-conformal half-width from sample-fold residuals is kept, which combines current practice with a naive use of conformal prediction. (b) Pooled recalibration: the reference residuals are added to the source calibration set. (c) Adaptive conformal inference [@gibbs2021] run over the reference samples (step size 0.05) starting from the source quantile. (d) Target-only CP: split conformal on the reference residuals alone; it is valid within the lot but requires $m\ge 1/\alpha-1$. (e) Target-only CP, centred: as (d) with scores centred on the leave-one-sample-out mean of the other reference residuals, which removes the lot bias. (f) HCP-mean: the mean-centred hierarchical score of Lee et al. [@lee2023] on season-held-out residuals, equal to LotCP without shrinkage. (g) LotCP. (h) LotCP-S.

Methods (5)–(10) are evaluated with their own point predictions. All other methods are wrapped around the same point predictor, so differences between them are differences in calibration only.

## 5.5 Evaluation

The unit of analysis is the target lot. For every lot and every $m\in\{0,3,5,10,20,30\}$ we draw {{V:n_draws}} random reference sets and evaluate on the scans of the remaining samples; a lot is evaluated at a given $m$ only if it has at least $m+10$ samples. Within a lot every sample has equal weight and every scan equal weight within its sample, matching Eq. (6). We report: *coverage*, the weighted share of scans whose reference value lies in the interval, averaged over draws and then over lots (lot-macro coverage); the share of lot-draws with coverage below $1-\alpha-0.10$ (*under-covered lots*); the mean interval *width*; and the Winkler *interval score* [@winkler1972; @gneiting2007], $(u-l)+\tfrac{2}{\alpha}(l-y)_+ +\tfrac{2}{\alpha}(y-u)_+$, a proper score that rewards narrow intervals and penalises misses. The nominal level is $1-\alpha=0.90$; 0.80 and 0.95 are examined in Section 9. LotCP uses $E={{V:n_episodes}}$ episodes per lot.

## 5.6 Statistical analysis

Methods are compared on the same lots, so tests are paired. For each $m$ and each competing method we apply the Wilcoxon signed-rank test [@wilcoxon1945] to the per-lot differences in interval score and in absolute coverage error $|\text{coverage}-0.90|$. The test assumes that the paired differences of lots are independent and symmetric under the null; independence across lots of the same season is an approximation, and we therefore also report in how many of the five target seasons the mean difference favours the reference method. P-values are adjusted by Holm's procedure [@holm1979] within each outcome family. The effect size is the matched-pairs rank-biserial correlation [@kerby2014]. Confidence intervals for lot-macro coverage and for mean differences are 95 % percentile intervals from {{V:n_boot}} bootstrap resamples of lots, stratified by season. Because the season is the top-level cluster and there are only five target seasons, per-season results are always shown alongside pooled ones.

The experimental protocol, including hypotheses, splits, methods and metrics, was written and committed to the repository before any model was trained. Deviations are listed in Section 5.7.

## 5.7 Deviations from the pre-specified protocol

(D1) LotCP-S was added after the first run on one predictor and one target season (PLS, 2018) showed that the pre-specified LotCP under-covered because the residual scale of that season's lots exceeded that of the source lots. The scale estimator of Eq. (4) was developed on source-season residuals only. Results for PLS on 2018 should therefore be read as development data for LotCP-S; the other four target seasons and the other two predictors had not been evaluated when the design was fixed. Both variants are reported everywhere. (D2) The centred target-only baseline (e) was added to give target-only calibration its strongest form. (D3) For computational reasons the CNN was trained for 20 rather than 30 epochs; lot-grouped folds were computed for one CNN seed only; and in the leave-one-season-out protocol the CNN uses one seed with season folds. These choices were made before any CNN result existed.
