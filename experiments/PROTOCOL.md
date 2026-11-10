# Pre-specified experimental protocol (written before any model was trained)

Date fixed: 2026-11-10. Changes after this date are logged at the bottom under "Deviations".

## Target journal (selected first, see `Target_Journal_Submission/journal_selection/`)
Smart Agricultural Technology (Elsevier).

## Problem
A near-infrared (NIR) calibration for mango dry-matter content (DMC) trained on past seasons is
deployed on a new harvest lot ("population" in the data set) in a later season. For every scanned
fruit the user wants a prediction interval with coverage 1 - alpha. The user can afford `m`
destructive reference measurements in the new lot (m = 0, 3, 5, 10, 20, 30).

## Hypotheses
* H1. Split-conformal intervals calibrated on held-out samples from the training seasons
  under-cover on lots of a later season (coverage below nominal by > 5 points at 1 - alpha = 0.9).
* H2. The unit at which calibration residuals are held out matters: sample-held-out <
  lot-held-out < season-held-out in achieved next-season coverage.
* H3. With m > 0 reference samples, a shrinkage bias correction whose conformal quantile is
  calibrated by replaying the m-shot protocol on past lots (LotCP) attains near-nominal
  lot-marginal coverage for every m, with narrower intervals than (i) m = 0 season-held-out
  calibration and (ii) target-only conformal calibration at the same m.
* H4. Each LotCP component (season-held-out residuals, shrinkage, episodic quantile) contributes;
  removing a component degrades coverage or interval score.

## Research questions -> experiments
* RQ1 (H1, H2): How far does coverage fall on next-season lots, and which hold-out unit repairs it? -> E1, E3
* RQ2 (H3): Coverage/width of LotCP against strong baselines as a function of m. -> E1, E2
* RQ3 (H4): Component ablation. -> E3
* RQ4: Robustness (alpha, protocol, source size, label noise, outlier filtering, shift type) and
  generalisation across point predictors. -> E4, E5, E7
* RQ5: Cost (compute, number of reference samples) and failure modes. -> E6, E8

## Data
Mango DMC and NIR spectra, Mendeley Data doi:10.17632/46htwnp833 version 6, file
`MangoDMC_NIR_Data_v4.csv` (CC BY 4.0). 85,401 spectra, 7 seasons (2015-2021), 199 lots.
All spectra are kept in the main analysis (the provider's outlier flags are used only in a
sensitivity analysis because we do not know whether they were derived from reference residuals).
Spectral window 684-990 nm (3 nm step).

## Splitting / leakage rules
* Primary protocol (forward chaining): target season T in {2017,...,2021}; training data are all
  seasons < T. No information from season >= T is used for training, model selection,
  preprocessing statistics or calibration, except the m labelled reference samples of the lot
  under test.
* Secondary protocol: leave-one-season-out over all 7 seasons (non-causal, robustness only).
* The same physical sample (`reference_no`) is scanned repeatedly; all folds are grouped so that a
  sample never straddles a split. Reference draws are made at sample level and all spectra of a
  drawn sample are removed from the evaluation set of that draw.
* Hyper-parameters are selected on source data only (leave-one-season-out CV inside the source).

## Point predictors
PLS regression (SNV + Savitzky-Golay 2nd derivative), 1D-CNN, LightGBM. Seeds for stochastic
models: 0, 1, 2 (fixed in advance; all reported, mean +- SD).

## Interval methods
m = 0: Gaussian +-z*RMSECV; split/cross-conformal with sample-, lot- and season-grouped folds;
weighted conformal for covariate shift (density ratio from unlabelled target spectra);
conformalised quantile regression; quantile regression forest; deep ensemble (Gaussian NLL).
m > 0: target-only split conformal; mean bias correction + source quantile; pooling target
residuals into the source calibration set; adaptive conformal inference run over the reference
samples; LotCP (proposed) and its ablations.

## Evaluation
Unit of analysis: target lot (lots with >= 20 samples so that at least 10 samples remain for
evaluation at the largest m that the lot admits; a lot is evaluated at a given m only when it has
>= m + 10 samples). R = 100 random reference draws per lot and m (seeded).
Metrics: coverage (lot-macro and pooled), share of lot-draws with coverage < 1 - alpha - 0.10,
mean interval width, Winkler interval score, RMSE and bias of the (corrected) point prediction.
Nominal level: 1 - alpha = 0.90 (primary); 0.80 and 0.95 (sensitivity).

## Statistics
Paired Wilcoxon signed-rank tests across target lots on per-lot interval score and per-lot
|coverage - nominal| (LotCP vs each baseline at each m), Holm correction within family, matched-pairs
rank-biserial effect size, lot-level cluster bootstrap 95% CIs (2,000 resamples); per-season
results are always shown because seasons (n = 5) are the top-level cluster.

## Deviations
(none yet)
