<!-- Reviewer 2 (novelty/related work), fresh-context agent, round 2, 2026-11-25 -->

**Reviewer 2: novelty, related work and significance**

**(1) Overall score: 5/10. Recommendation: major revision.**
The coverage audit is careful and candid: lot by lot, season by season, forward chaining, two PLS recipes. It is useful for the fruit-NIR community. The new methodological content is thinner than the framing suggests, though, and one closely overlapping line of conformal work is missing. Against the simple current-practice baseline, the practical gain from the method is not supported.

**(2) Novelty: 11/25**
- Differentiation from prior work: 2/5
- Mechanism/insight: 3/5. The variance-component explanation of why sample-fold calibration fails is clear and useful.
- Strength of evidence: 2/5. There are five target seasons, the efficiency endpoints failed on the independent data, and 2017 inflates the pooled figures.
- Breadth of evidence: 2/5. There is one fruit data set, and the independent soil set showed almost no shift.
- Significance for practice: 2/5. The cost saving comes from any calibrated bound, not from the method; reference fruit added nothing.

**(3) Concerns**

1. **MAJOR: the few-shot hierarchical score is prior work, and a directly overlapping paper is missing.**
   - **Problem:** I checked Lee, Barber & Willett (arXiv:2306.06342), Remark 1, Section 2.2. It already covers the case where "a few observations from the test group are also available". The test-group score is centred on the mean of its observed outcomes, and the training-group scores are built the same way. That is, in substance, the "replay" of Eq. (5) for LotCP (no scale).
   - The paper itself says Eq. (5) for m ≥ 1 "is their mean-centred few-shot score". Yet Contribution 2 and the claim "our contribution lies in the calibration procedure" present the replay as new.
   - Missing: Mallick, Tchetgen Tchetgen, Dobriban & Lee, "Generalized Hierarchical Conformal Prediction", arXiv:2608.15500 (Aug 2026). It targets exactly this setting: an unseen group with a few observed outcomes, using those outcomes to improve the scores.
   - Also missing: Dobriban & Yu, "SymmPI: Predictive inference for data with group symmetries", arXiv:2312.16160. It covers prediction within partially observed hierarchical branches.
   - **Fix:** Cite and discuss both papers. Restate the contribution precisely:
     - the label-free replicate-scan scale;
     - season-held-out residuals inside the replay;
     - random reference sets across three nested levels;
     - the empirical audit.
     Drop any implication that replaying the m-shot procedure is itself new. If possible, compare against GHCP.

2. **MAJOR: the practical significance relative to current practice is not supported.**
   - **Problem:** "Bias correction + source CP" covered better than LotCP-S:
     - 0.938 against 0.919 at m = 10;
     - nominal in 5/5 seasons against 3/5;
     - 0.929 against 0.893 without 2017.
   - LotCP-S wins only on interval score, and that gain was not confirmed on NeoSpectra (P1, P2 failed) and vanished without repeated scans (Table S6b).
   - LotCP-A buys no efficiency over LotCP-S run at α = 0.05 (Section 4.4).
   - In the decision analysis, neither the reference fruit nor LotCP-S improved cost over a plain split-conformal bound.
   - Even so, the "Practical procedure" (Section 5) and the title recommend the new workflow.
   - **Fix:**
     - Retitle so the claim does not rest on few-shot calibration enabling risk-aware decisions. For example, lead with the audit and calibrated bounds.
     - State plainly that, for a practitioner, bias correction with a source half-width is the safer simple option on these data.
     - Say when LotCP-S is preferable: repeated scans available, flexible predictors (Section S5.2 shows bias correction under-covers with LightGBM, 0.882).

3. **MINOR: prior work on harvest decisions is missing.** Anderson, Subedi & Walsh, "Using hand-held infrared spectroscopy to guide harvest decisions", Acta Horticulturae 1244:123–128 (2019), doi:10.17660/ActaHortic.2019.1244.19. It covers block sampling protocols and harvest-date projection with handheld NIR in mango. Cite it, and relate the m-planner and the 80 % lot rule to existing block-sampling practice.

4. **MINOR: classic work on season and biological variability in fruit NIR is missing.**
   - Peirs et al., "Effect of biological variability on the robustness of NIR models for soluble solids content of apples", Postharvest Biology and Technology (2003), doi:10.1016/s0925-5214(02)00196-5.
   - Bobelyn et al., "Postharvest quality of apple predicted by NIR-spectroscopy: Study of the effect of biological variability on spectra and model performance", Postharvest Biology and Technology 55 (2010), doi:10.1016/j.postharvbio.2009.09.006.
   - Label-free seasonal adaptation in fruit: Mishra & Nikzad-Langerodi, "Partial least square regression versus domain invariant partial least square regression with application to near-infrared spectroscopy of fresh fruit", Infrared Physics & Technology 111:103547 (2020), doi:10.1016/j.infrared.2020.103547. This is the obvious alternative to reference fruit.

5. **MINOR: conformal prediction in soil spectroscopy is missing.** The paper uses soil spectra for external validation, yet omits Huang et al., "Using Monte Carlo conformal prediction to evaluate the uncertainty of deep-learning soil spectral models", SOIL 11:553–563 (2025), doi:10.5194/soil-11-553-2025.

6. **MINOR: some citations claim more than their titles support.**
   - bouckaert2011 is described as comparing methods "within one population"; the title does not support that.
   - metz2025 is described as "Bayesian approximations"; the title says "simple methods" for UQ.
   - cui2018 is a general NIR CNN paper but is listed under "robust fruit calibrations" across seasons.
   - fearn2001 and feudale2002 (transfer/standardisation reviews) are cited for the specific claim that checking against a few destructively measured fruit is routine maintenance.
   - nicolai2007 is cited for the specific claim that in-calibration accuracy overstates independent accuracy.
   - Lee et al.'s Remark 1 is described accurately (I verified it); Kayaoglu & Erdem 2026 is described accurately (abstract checked).
   - Fix: re-word or replace these citations.

7. **MINOR: heavy reliance on unrefereed preprints.**
   - Preprints: sun2026, metz2025, nasir2026, moussa2026, neyigapula2026 (SSRN or Research Square). These are cited as established findings.
   - Bib entries never cited: efron1975, wilcoxon1945, holm1979, kerby2014, orgiazzi2018. Yet the analyses use EB shrinkage, Wilcoxon tests, Holm correction, rank-biserial r and LUCAS data, so these should be cited where used.
   - Fix: label preprints as such, and cite the methods and data actually used.

8. **MINOR: the evidence is dominated by one season.**
   - Headline pooled figures (0.919; 92 % of lot-draws) are carried by 2017, which has only two source seasons. The excluding-2017 values (0.893; 87.5 %) belong in the abstract and highlights as the primary numbers.
   - "Five to ten reference fruit restored coverage on average" overstates 0.893.

9. **MINOR: the independent confirmation could not test the core claim.** NeoSpectra had no seasonal shift (split CP already covered 0.930). Claim no external support for the shift-repair mechanism, and consider a second fruit data set with season structure, for example apple or kiwifruit SSC libraries if they can be obtained.

10. **MINOR: editorial errors.**
    - "by 0.10–0.10 (season mean)" (Section 4.3).
    - "3.69 [2.11, 5.16], The difference" (Section 4.6).
    - "Baselines (b) and (b′) were added in response to review" is development history and does not belong in Methods.
    - The protocol was not publicly registered, so the word "pre-registered" in the Table 5 caption should be "pre-specified".

