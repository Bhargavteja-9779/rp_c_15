# Review round 6 — Reviewer #6 (cost, scalability, deployment feasibility)

Question: is the improvement worth what it costs?

| # | Severity | Issue | Outcome |
|---|---|---|---|
| 6.1 | MAJOR | The real cost is destructive sampling, not CPU time. The paper must express the benefit per reference fruit and say when the method is *not* worth it. | Section 10 and Fig. 4 give width as a function of m (3.76, 3.45, 3.28 % DMC at m = 3, 10, 30 for PLS) and Section 6.3 states that from 20–30 reference samples per lot, calibration on those samples alone is as good. The discussion gives 5–10 as the practical range. **Addressed.** |
| 6.2 | MAJOR | Season-held-out cross-fitting multiplies training cost by the number of seasons; for a CNN this is the dominant cost and was not reported. | Table 11 now reports total cross-fitting time per target season (PLS ≈ 40 s; CNN ≈ 23 min on one CPU thread per fit) and Table S10 gives the breakdown. The ablation additionally shows that with reference samples lot-fold residuals suffice, which removes the season-wise refits. **Addressed.** |
| 6.3 | MODERATE | Energy and memory are not measured. | Not measured (no power meter in the environment). Stated in Section 10. Model sizes: CNN 103,265 parameters; PLS ≤ 20 latent variables on 103 wavelengths. Memory of the calibration: one residual per past scan. |
| 6.4 | MODERATE | Scalability in the number of past lots. | The episodic quantile is O(K·E·N); measured 1.8 s for 187 lots × 30 episodes. With 10 episodes results are unchanged (Table 9), so the cost can be cut by three. **Addressed.** |
| 6.5 | MODERATE | The method needs lot and sample identifiers and repeated scans stored with the calibration set; many legacy calibration sets lack them. | Added to the practical procedure in the discussion (store residuals with lot and sample identifiers). Deployment feasibility on legacy data remains a limitation. |
| 6.6 | MINOR | The CNN fit time in Table 11 is for one thread. | Stated in the table caption. |

Verdict: computational cost is negligible at deployment; the paper is now explicit that the binding cost is
reference sampling and gives the range in which the method pays off.
