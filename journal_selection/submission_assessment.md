---
title: "FOR THE AUTHORS ONLY (do not upload): journal suggestion, title and desk-rejection assessment"
---

# 1. Suggested journal

**Smart Agricultural Technology** (Elsevier, gold open access; eISSN 2772-3755).

| Item | Value | Status |
|---|---|---|
| Quartile | Q1 (Agricultural Engineering) | From JCR-derived listings; not checked inside Clarivate JCR |
| Impact factor | 7.1 (publisher page, 2026 release); 5.7 on an older snapshot | Publisher page via search snapshots |
| Index | Web of Science, ESCI edition (not SCIE) | Single source; check if your institution requires SCIE |
| Submission → acceptance | 69–72 days (publisher-reported average) | Average over accepted papers, not a promise; a major revision will take longer |
| Acceptance rate | 41 % | Publisher "Insights" page snapshot |
| APC | about USD 2,050 (one aggregator: USD 1,800) | Confirm on the journal page |
| Guide for Authors | Could not be opened from the research environment | **Check every item yourself before uploading** |

Why this journal: its scope covers smart systems that combine computing with electronic instrumentation for agricultural planning and production. The paper is about how far the error bars of a handheld NIR instrument can be trusted for an orchard harvest decision, with a practical procedure for growers. That is applied sensing plus decision support, which is the journal's core. It was the only Q1 journal found with a reported average under the 72-day limit and a real scope fit (full comparison in `journal_selection/journal_comparison.md`).

# 2. Suggested title

> **How far do near-infrared error bars hold across harvest seasons? Season-aware conformal calibration for mango harvest decisions**

Why this title: two independent simulated reviewers judged the previous title ("Risk-aware mango harvest decisions using few-shot conformal calibration…") to overstate the role of the few-shot method, because the evidence shows that the main findings are the season-by-season coverage audit and the season-level calibration. The new title leads with the question the paper answers and keeps the keywords an editor screens for (near-infrared, mango, harvest decisions). The previous title can be restored in one line (`manuscript/build_manuscript.py`, `TITLE`) if you prefer it.

# 3. Recently published papers in Smart Agricultural Technology on comparable topics

All entries below were returned by the Crossref API for ISSN 2772-3755 (published 2024–2026) and exist with these DOIs. They show that the journal publishes NIR/spectroscopic quality prediction for crops and fruit, handheld spectrometers, and uncertainty quantification. They are comparable in **topic**; their quality and review history were not assessed.

| Year | Title | DOI |
|---|---|---|
| 2026 | Predicting potato dry matter content by incorporating spectral statistical features | 10.1016/j.atech.2026.101854 |
| 2026 | Development of non-contact grape quality assessment method using a VIS-NIR spectroscopic device | 10.1016/j.atech.2026.102440 |
| 2026 | The value of satellite time series and uncertainty quantification for field-scale wheat yield prediction in a multi-climate … | 10.1016/j.atech.2026.101934 |
| 2026 | Graph-based spatio-temporal soil moisture imputation with uncertainty quantification | 10.1016/j.atech.2026.102455 |
| 2025 | Few-shot learning for avocado ripeness detection: a transformer-based NIR approach | 10.1016/j.atech.2025.101448 |
| 2025 | Ranking-guided coreset selection for NIRS-based nutrient prediction in liquid organic manures | 10.1016/j.atech.2025.101577 |
| 2025 | Comparing the handheld Stenon FarmLab soil sensor with a Vis-NIR multi-sensor soil sensing platform | 10.1016/j.atech.2024.100717 |
| 2024 | SSC and pH prediction and maturity classification of grapes based on hyperspectral imaging | 10.1016/j.atech.2024.100457 |
| 2024 | Enhancing corn quality prediction: variable selection and explainable AI in spectroscopic analysis | 10.1016/j.atech.2024.100458 |
| 2024 | Early plant disease diagnosis through handheld UV–Vis transmittance spectrometer with DD-SIMCA one-class classification | 10.1016/j.atech.2024.100631 |

A Crossref search of the journal for "conformal prediction" returned no conformal-prediction paper (searched 2026-11-25; not exhaustive). If that holds, this would be among the first conformal-prediction papers in the journal, a point worth one sentence in the cover letter only after you have confirmed it on the journal site.

# 4. Why it should pass desk screening — and why that is not guaranteed

No one can guarantee that a manuscript will not be desk-rejected. Editors decide on scope, perceived novelty, quality of presentation and journal load. What can be said is which common desk-rejection reasons this manuscript avoids and which risks remain.

**Common desk-rejection reasons the manuscript avoids**

1. *Out of scope* — it is a handheld-sensing and decision-support study for an orchard operation, squarely in scope, and close in topic to the recent papers in Section 3.
2. *Incomplete submission* — all Elsevier components are present: cover letter, title page, highlights (5 × ≤ 85 characters), abstract (≤ 250 words), keywords, numbered figures and tables, CRediT, competing-interest, funding, generative-AI and data-availability statements, supplementary material, anonymised version.
3. *Weak or unvalidated evaluation* — forward-chaining evaluation on seven harvest seasons, four predictive models, season-level statistics, matched baselines, repeated reference draws, an independent data set for the pre-specified confirmation, a leakage audit and an automated check that every number comes from result files.
4. *Overclaiming* — exploratory analyses are labelled, failed endpoints and negative results are reported, and the limitations are ranked.
5. *Unavailable data* — all data are public with DOIs.

**Remaining desk-rejection risks (honest)**

1. *Novelty judged incremental.* The methods build on hierarchical and multi-environment conformal prediction (Lee et al.; Duchi et al.), which the paper cites. In blind simulated review the novelty was scored 12/25. An applied journal weighs the agricultural evidence more than methodological novelty, but an editor may still see it as incremental.
2. *One fruit data set, retrospective only.* No orchard trial. This is stated as the first limitation.
3. *Length and density.* About 8,800 words of main text with seven tables; editors of applied journals sometimes ask for shorter papers.
4. *Extensive AI involvement.* The AI declaration is broad (literature search, code, experiments, drafting, simulated review). Elsevier permits AI assistance with disclosure, but an editor may scrutinise a study largely carried out by AI. Read and verify the analysis yourselves before submitting, and confirm that your institution and the journal accept this level of AI use.
5. *Code on request only.* Many journals now prefer a public code deposit; "available on request" is acceptable at Elsevier but weakens the reproducibility claims.
6. *Placeholders.* Affiliations, e-mail addresses and the approval statement in the cover letter must be completed; a submission with placeholders would be returned.

**Realistic expectation.** If sent to review, the most likely outcome is major revision (all three simulated review panels said so). A major revision would very probably take the total time beyond 72 days.
