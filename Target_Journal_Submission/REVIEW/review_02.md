# Review round 2 — Reviewer #2 (novelty and prior art)

Focus: is the contribution new, and is the research gap real?

## Prior-art map used for this review

| Work | What it contributes | Overlap with the submission |
|---|---|---|
| Lee, Barber, Willett (2023), arXiv:2306.06342 | Hierarchical exchangeability; HCP quantile with group-balanced weights (their Eq. 6, Theorem 1); Remark 1: with M observed outcomes of the test group, use a score centred on their mean. | **High.** LotCP's guarantee is their Theorem 1; "LotCP without shrinkage" is their Remark 1 applied to model residuals. |
| Dunn, Wasserman, Ramdas (2023), JASA | Prediction sets for two-layer hierarchical models (pooling, subsampling, repeated subsampling). | Same setting. |
| Fisch et al. (2021), ICML | Few-shot conformal prediction calibrated across exchangeable auxiliary tasks. | Same idea of calibrating a few-shot procedure across tasks. |
| Tibshirani et al. (2019); Gibbs & Candès (2021); Barber et al. (2023) | Covariate-shift weighting; online adaptation; non-exchangeable weighting. | Baselines. |
| Kayaoğlu & Erdem (2026), Zenodo 10.5281/zenodo.23955251 (article submitted elsewhere) | Split-conformal coverage loss under NIR *instrument transfer* on four paired-instrument data sets; labelled target samples needed to restore validity. | **High in spirit** (conformal + NIR + shift + labelled target samples), different shift type and data structure. |
| Jović (2025), Food Chemistry; Sun et al. (2026), SSRN | Conformal prediction for MIR / NIR quantification within one population. | Application area only. |
| Metz et al. (2025), SSRN | MC dropout / SWAG uncertainty for mango DMC networks. | Same data family, model-based uncertainty. |
| Anderson et al. (2020, 2021); Mishra & Woltering (2023) | Robust point models across seasons. | Problem setting. |

## Issues

| # | Severity | Issue | Outcome |
|---|---|---|---|
| 2.1 | MAJOR | The first internal outline presented LotCP as a new conformal method. It is an instantiation of HCP with a data-dependent few-shot score, which Lee et al. already sketch. | **Fixed in framing**: Sections 1, 2 and 4.6–4.7 now say so explicitly ("We do not claim a new conformal theory"); the HCP-mean variant is reported under that name as a baseline/ablation. |
| 2.2 | MAJOR | Empirical-Bayes shrinkage was a headline design element. Does it do anything? | **Tested (ablation)**: no measurable effect from m = 10, small effect at m = 3. Reported as a negative result in Section 7, the abstract and the highlights. |
| 2.3 | MAJOR | With the concurrent instrument-transfer study, is "conformal coverage fails under shift in NIR" still a gap? | **Partly.** The submission cites the study in the introduction, related work and discussion and defines its own contribution as (i) season/lot shift in orchard practice, (ii) use of many past lots to calibrate a few-shot correction, (iii) lot-level evaluation. Only the Zenodo description of the concurrent work was read (the article itself is not public), so its content is described no further than that description allows. Residual risk: if that article is published first with a similar few-shot analysis, novelty is reduced. |
| 2.4 | MODERATE | What is actually new in the method? | The label-free replicate-scan scale and the season-held-out residuals. The ablation shows the first matters for m > 0 and the second for m = 0 only. The paper now states this division plainly, including that season-held-out residuals are *not* needed once reference samples exist. |
| 2.5 | MODERATE | Is the gap "artificially constructed"? | No: lot-level coverage on later seasons had not been reported for this or, to our knowledge, any fruit NIR data set; searches (Crossref, web, Zenodo; terms: conformal + NIR/spectroscopy/chemometrics/mango/dry matter/distribution shift/few-shot/hierarchical) returned only the works above. The phrase "has not been examined" is kept but limited to the season/lot setting. |
| 2.6 | MINOR | The claim that weighted conformal prediction "cannot repair" a residual bias should be a statement about its assumptions, not an empirical generalisation. | Wording retained as a statement about covariate-shift assumptions, supported by the experiment. |

## Assessment
Incremental in theory, original in application and evidence. Appropriate for an applied journal if framed as
such, which the revised text does.
