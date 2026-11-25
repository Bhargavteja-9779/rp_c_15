<!-- Reviewer 2 (novelty/related work), fresh-context agent, round 3, 2026-11-25 -->

**Reviewer 2: novelty, related work and significance**

**(1) Score: 5/10. Recommendation: major revision.**

The audit is careful and candid. It checks coverage lot by lot on later seasons of a real multi-season mango NIR data set. That is useful to the fruit-NIR community, and the paper reports its negative results honestly (within-season learning, spectral warnings, the failed soil efficiency endpoints). The main methodological claim, however, is that calibrating within past seasons and taking an order statistic across them is a new third level of hierarchical conformal prediction. That claim overlaps with prior work the paper does not cite. The paper also states the season-level guarantee more strongly than its own Proposition 3 supports.

**(2) Novelty score: 12/25**

- **Differentiation from prior work: 2/5.** LotCP-A (Eq. 6) and the per-season quantile-of-quantiles in LotCP-R/AR closely match the multi-environment split conformal method and the (α, δ)-coverage of Duchi et al. (2024), which is not cited.
- **Mechanism/insight: 3/5.** The sensitivity analysis gives a clear mechanism: the gain comes from the per-season conformal term plus the cross-season order statistic, while pooled quantiles are dominated by the largest seasons.
- **Strength of evidence: 2/5.** All of the following weaken the evidence:
  - five target seasons;
  - every season-robust result is exploratory, and was developed and evaluated on the same seasons;
  - the choice of R2 over R was made post hoc;
  - the one independent confirmation found no efficiency gain and no seasonal shift to test.
- **Breadth of evidence: 2/5.** There is one fruit data set and one trait; the soil data have no season level and little shift.
- **Significance for practice: 3/5.** The practical message stands, but the decision benefit comes from using any calibrated bound against a point rule that costs more than withholding every fruit, not from the proposed method.

**(3) Concerns**

1. **MAJOR: a closely overlapping prior work is missing.** Duchi, Gupta, Jiang and Sur, "Predictive inference in multi-environment scenarios", arXiv:2403.16336 (2024). It assumes environments that are exchangeable with each other and observations exchangeable within each environment, which is the same structure as the paper's lots and seasons. It defines hierarchical coverage and (α, δ)-coverage for a new environment, the latter meaning a share 1−α of the new environment is covered with probability 1−δ. Its multi-environment split conformal takes the 1−α quantile within each environment and then a quantile across environments. It also resizes the sets using limited labels from the test environment.
   - This anticipates LotCP-A almost exactly. LotCP-A is currently credited only to PAC meta-learning (Park et al., 2022).
   - It also anticipates the core of the "third level" claimed in Sections 1.1, 1.2 (item 3) and 2.7.
   - **Fix:** cite this work and compare against it, including in Table 5. Restate what is actually new: the m-shot replay inside each season, season-held-out residuals, the lot scale from repeated scans, and the empirical NIR evidence.

2. **MAJOR: the season-level guarantee is overstated.** Section 2.7 says that a new lot "is then covered with probability at least 1−α". Proposition 3 gives this only on the event {T_{S+1} ≤ T_(k)}. Without that conditioning the bound is about (1−α)(S+1−k)/(S+1).
   - LotCP-R2 is the variant the paper recommends, and it uses k = 2. That gives (S−1)/(S+1): 1/3 for 2017 (S = 2) and 5/7 at best.
   - The figures in Discussion (2/3 to 6/7) and Limitation 3 (0.67–0.86) are for LotCP-R (k = 1), not R2.
   - Merging seasons with fewer than five lots also changes S.
   - **Fix:**
     - State the unconditional bound in the abstract, highlights and Section 2.7.
     - Give the R2-specific bound.
     - Say plainly that the 5/5 empirical success is far above what the theory guarantees, so it is evidence of conservatism or luck, not of the guarantee.

3. **MAJOR: the related-work description is inaccurate, and the "closest work" is misidentified.** Wadoux and Ramirez-Lopez (2025, CILS 265:105473, doi:10.1016/j.chemolab.2025.105473) used the same Anderson et al. mango DMC data. They validated quantile regression forest intervals by coverage probability and found them too wide, i.e. over-covering. The manuscript describes this study only generically. It is the most directly comparable prior result, and its conclusion is the opposite of this paper's (0.841 coverage for QRF on later seasons).
   - **Fix:** describe that study accurately and attribute the contrast to random versus season-held-out validation. This sharpens the paper's key message.
   - Also call Duchi et al. (concern 1), not Kayaoğlu and Erdem (2026; verified to exist, Applied Sciences 16:11417), the closest methodological work.

4. **MINOR: a related shift-robust conformal method is missing.** Cauchois, Gupta, Ali and Duchi, "Robust validation: confident predictions even when distributions shift", JASA 119 (2024) 3033–3044, doi:10.1080/01621459.2023.2298037. It is a natural alternative to the fixed α = 0.05 inflation.
   - **Fix:** cite it, and ideally estimate the robustness radius from past seasons as a baseline.

5. **MINOR: classical PLS prediction intervals are mentioned but not shown.** Section 3.8 says "leverage-based PLS intervals" were added after the simulated review, but no result appears in the main text or the Notes. The chemometric standard is also uncited, e.g. Faber and Kowalski (1997), J. Chemometrics 11:181–238, doi:10.1002/(SICI)1099-128X(199705)11:3<181::AID-CEM459>3.0.CO;2-7.
   - **Fix:** report these intervals in Table 3 and cite the source.

6. **MINOR: the significance of the decision analysis is framed loosely.** At c_I/c_D = 9 the point rule costs more than withholding every fruit, so the roughly 5-unit saving mostly restates the cost ratio. The reference fruit gave no detectable saving.
   - **Fix:** in the Abstract and Highlight 5, compare against a bias-corrected point rule with a cost-tuned offset (a non-conformal threshold shift). Present the decision result as an illustration.

7. **MINOR: the contribution of LotCP-S is thin relative to the baselines.**
   - Simple bias correction with the source half-width covered more and reached 0.90 in more seasons.
   - The interval-score advantage of LotCP-S failed confirmation on the independent soil data.
   - That advantage also vanished without repeated scans per fruit, which routine practice does not take.
   - **Fix:** demote LotCP-S in the Highlights and Contributions, and lead with the audit plus the season-robust variant.

8. **MINOR: generality is not shown.** The work covers one fruit data set and one trait. The method also depends on lot metadata that commercial NIR deployments rarely record.
   - **Fix:** discuss what metadata a packhouse or orchard would need to record. Temper "calibration maintenance" claims to mango DMC.

9. **MINOR: the citation base leans on unrefereed work.** Many key positioning references are 2026 preprints: the GHCP paper (arXiv:2608.15500, verified, explicitly few-shot for an unseen group), Moussa, Nasir, Neyigapula and Sun.
   - **Fix:** state which claims rest on unrefereed work. Explain in a sentence how LotCP-S differs from GHCP's donated reference-size construction, since both target the same few-shot setting.

10. **MINOR: the title and abstract overstate the method's role.** "Few-shot conformal calibration" makes it the headline, but the paper's own results attribute the gains to bias correction and the season-level step.
    - **Fix:** retitle around the coverage audit and season-robust calibration.

**Verification notes**
- All the missing references above were confirmed on arXiv, Crossref or the publisher's site.
- Kayaoğlu and Erdem (2026), Metz et al. (SSRN 2025), Sun et al. (SSRN 2026), Ma et al. (2026) and Anderson et al. (2019, Acta Hortic.) all exist with the metadata given in the bibliography.
- I found no prior study that applies conformal prediction to fruit NIR dry matter or soluble solids, so applying it in that domain does appear to be new.
