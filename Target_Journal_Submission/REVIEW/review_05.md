# Review round 5 — Reviewer #5 (data validity, generalisation, deployment)

Aim: invalidate the central claims.

| # | Severity | Attack | Experiment / check | Result |
|---|---|---|---|---|
| 5.1 | MAJOR | In the data a lot is scanned by several instrument units (median 4) and each sample many times. A grower uses one unit. Lot-level bias averaged over units is easier to estimate than the bias of one unit, so the benefit of reference samples may be overstated. | New protocol: deployment unit = one instrument unit within a lot (558 units); reference and query scans from that unit only. | Claims hold in direction: split CP 0.833; LotCP-S 0.914 at m = 10 with best interval score at m = 10 (4.04 vs 4.32 for centred target-only) and a tie at m = 20. But the share of badly covered unit-draws is higher (11 % vs 8 % at lot level). Reported in Section 9. |
| 5.2 | MAJOR | The under-coverage could be an artefact of the lot-balanced weighting. | Scan-level coverage with every scan weighted equally. | 0.820 for sample-fold split CP: same shortfall. Added to Section 6.2. |
| 5.3 | MAJOR | Outliers flagged by the provider inflate the failure. | Flagged scans removed from calibration and evaluation. | Coverage of LotCP-S unchanged (0.920); split CP coverage among unflagged scans is 0.84 (subgroup table), still far from 0.90. |
| 5.4 | MAJOR | Results depend on having five to six source seasons. | Source restricted to the two preceding seasons. | LotCP-S 0.917 at m = 10, intervals 24 % wider. Reported. |
| 5.5 | MODERATE | Unseen cultivar or region. | Leave-one-region-out and leave-one-cultivar-out protocols. | LotCP-S 0.912 and 0.907 at m = 10; split CP 0.80–0.89 depending on the held-out group. |
| 5.6 | MODERATE | Reference values contain laboratory error. | Gaussian error (SD 0.25, 0.5 % DMC) added to reference samples at deployment. | Coverage ≥ nominal, width +4 % at SD 0.5. |
| 5.7 | MODERATE | Random reference sampling is assumed; in practice sampling is convenience-based. | Not testable with this data (no position/accessibility information). | Limitation stated. |
| 5.8 | MODERATE | "Population" = harvest lot is the authors' reading of the data file. | The data providers describe harvest populations and used them as cross-validation groups (Anderson et al., 2020, abstract). | Stated as an interpretation in Limitations. |
| 5.9 | MODERATE | Subgroups: is anything systematically under-covered after calibration? | Scan-level subgroup analysis at m = 10. | Ripening-stage fruit 0.90 vs 0.93 green; Keitt 0.85; provider outlier flag 1: 0.80; extremes of the DMC range lower. Reported in Section 11 as failures. |
| 5.10 | MINOR | Lots with fewer than 20 samples are excluded. | Count checked. | No target lot is excluded (all 137 have ≥ 20 samples); at m = 30 only 112 lots are evaluable, stated in Table S3. |

The central empirical claim (loss of coverage) survived all attacks. The claim of advantage for LotCP-S survived in
weakened form (see round 3, item 3.9, and item 5.1 here).
