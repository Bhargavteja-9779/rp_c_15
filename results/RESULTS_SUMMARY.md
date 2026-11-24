# RESULTS SUMMARY (generated from files) — cycle 2

Journal: Smart Agricultural Technology (Elsevier) -- G1 verification pending in cycle 2
Topic: Few-shot conformal calibration of NIR fruit-maturity predictions across harvest seasons (risk-aware mango harvest decisions)

## Compute
Metered: 0.00 h; estimated unmetered cycle 1: 6.0 h; hardware: 4-core CPU, no GPU.

## Variants tried (multiple-try ledger)
19 variants/analyses logged in state/variants_tried.csv.

## Main table (PLS, forward chaining, nominal 0.90; lot-macro)
| method              |   m |   n_lots |   coverage |   meets |   width |   iscore |
|:--------------------|----:|---------:|-----------:|--------:|--------:|---------:|
| scp_sample          |   0 |      137 |      0.823 |   0.474 |   3.828 |    6.811 |
| scp_season          |   0 |      137 |      0.9   |   0.73  |   5.258 |    7.046 |
| lotcp_s             |   0 |      137 |      0.894 |   0.766 |   5.394 |    7.26  |
| lotcp_a             |   0 |      137 |      0.946 |   0.876 |   7.194 |    8.032 |
| lotcp_s             |   5 |      137 |      0.92  |   0.698 |   3.603 |    4.62  |
| biascorr_naive      |   5 |      137 |      0.931 |   0.735 |   3.828 |    4.797 |
| target_only_centred |   5 |      137 |      1     |   1     | nan     |  nan     |
| lotcp_a             |   5 |      137 |      0.964 |   0.908 |   4.611 |    5.112 |
| lotcp_s             |  10 |      137 |      0.919 |   0.691 |   3.451 |    4.457 |
| biascorr_naive      |  10 |      137 |      0.938 |   0.771 |   3.828 |    4.685 |
| target_only_centred |  10 |      137 |      0.956 |   0.875 |   4.634 |    5.118 |
| lotcp_a             |  10 |      137 |      0.964 |   0.918 |   4.303 |    4.774 |
| lotcp_s             |  20 |      129 |      0.918 |   0.676 |   3.286 |    4.252 |
| biascorr_naive      |  20 |      129 |      0.945 |   0.782 |   3.821 |    4.577 |
| target_only_centred |  20 |      129 |      0.932 |   0.778 |   3.577 |    4.286 |
| lotcp_a             |  20 |      129 |      0.958 |   0.903 |   3.967 |    4.48  |

## Pre-registered confirmation (plan_v2; SEEDS_CONFIRM 100-104)
| dataset                               | endpoint   | comparison                    |   m |   n_lots |   mean_diff |   ci_lo |   ci_hi |   p_holm |   rank_biserial | confirmed   |
|:--------------------------------------|:-----------|:------------------------------|----:|---------:|------------:|--------:|--------:|---------:|----------------:|:------------|
| mango (re-draw, lots seen in cycle 1) | P1         | LotCP-S - biascorr_naive      |   5 |      137 |     -0.1653 | -0.2693 | -0.058  |   0.0004 |         -0.3689 | True        |
| mango (re-draw, lots seen in cycle 1) | P2         | LotCP-S - biascorr_naive      |  10 |      137 |     -0.2476 | -0.3523 | -0.1374 |   0      |         -0.5282 | True        |
| mango (re-draw, lots seen in cycle 1) | P3         | LotCP-A - target_only_centred |  10 |      137 |      0.0369 |  0.0099 |  0.0637 |   0.0003 |          0.3952 | True        |
| mango (re-draw, lots seen in cycle 1) | P4         | LotCP-A - biascorr_naive      |  20 |      129 |      0.1212 |  0.0722 |  0.1748 |   0.0007 |          0.4399 | True        |
| NeoSpectra (untouched)                | P1         | LotCP-S - biascorr_naive      |   5 |       20 |     -0.0486 | -0.0864 | -0.013  |   0.0655 |         -0.5429 | False       |
| NeoSpectra (untouched)                | P2         | LotCP-S - biascorr_naive      |  10 |       20 |     -0.0283 | -0.079  |  0.0232 |   0.2943 |         -0.2762 | False       |
| NeoSpectra (untouched)                | P3         | LotCP-A - target_only_centred |  10 |       20 |      0.073  |  0.033  |  0.1165 |   0.0152 |          0.7143 | True        |
| NeoSpectra (untouched)                | P4         | LotCP-A - target_only_centred |  20 |       10 |      0.207  |  0.178  |  0.235  |   0.0078 |          1      | True        |

## Baseline reproduction (G4)
|                               |   rmsep |   bias |
|:------------------------------|--------:|-------:|
| ('cnn_ours', 'val_ext')       |   1.076 | -0.159 |
| ('cnn_ours', 'val_ext2')      |   2.16  | -1.864 |
| ('pls_ours', 'val_ext')       |   1.392 |  0.129 |
| ('pls_ours', 'val_ext2')      |   1.661 | -1.258 |
| ('pls_published', 'val_ext')  |   1.045 | -0.021 |
| ('pls_published', 'val_ext2') |   1.665 | -1.293 |
Published: global PLS 1.01 / 1.014 % (Anderson 2020/2021); CNN 0.77 % (Walsh 2024).

## Research questions
* RQ1 coverage loss of standard error bars on later seasons: SUPPORTED (split CP 0.823; 7 procedures 0.77-0.85).
* RQ2 few-shot calibration: coverage restored SUPPORTED; lot-level assurance SUPPORTED and CONFIRMED on untouched data; efficiency gain of LotCP-S over bias correction SUPPORTED on mango, NOT CONFIRMED on untouched data.
* RQ3 harvest decisions: SUPPORTED in retrospective simulation (costs assumed).
* RQ4 planner: SUPPORTED (median abs. relative error 7 %).
* RQ5 generalisation/components: mixed (soil replication; shrinkage removed; replay = validity).

## Leakage audit: PASS

## Novelty scores
[
 {
  "cycle": 2,
  "date": "2026-11-24",
  "by": "author agent (before blind review)",
  "differentiation": 3,
  "mechanism": 4,
  "evidence": 4,
  "breadth": 3,
  "significance": 3,
  "total": 17,
  "notes": "differentiation limited: guarantee inherited from Lee et al. 2023; PAC-over-tasks exists (Park et al. 2022); few-shot recalibration ideas exist in other fields (Park et al. 2024; Nasir 2026; Moussa 2026). Mechanism: ablations show scale -> efficiency, replay -> validity. Evidence: pre-registered confirmation passed for the lot-level assurance, failed for efficiency on untouched data. Breadth: one fruit + soil (3 tasks + untouched NeoSpectra). Significance: practical but retrospective."
 }
]

## Gates
| Gate | Status | Note |
|---|---|---|
| G1 | pass-with-stated-failure | per-article dates unverifiable (403/Crossref empty); publisher average 69-72 d |
| G2 | pass | 80 logged queries; 39 papers opened (abstract level); close new works now cited and differentiated in Section 2 |
| G3 | fail (own score 17/25; blind score pending) | needs >= 20 with no dimension < 3 |
| G4 | pass-partial | published PLS RMSEP 1.01 reproduced (1.045); published CNN 0.77 not reproduced (ours 1.07, no augmentation/tuning); our SNV-PLS pipeline 0.35 worse than the published recipe |
| G5 | partial | untouched data: LotCP-A assurance confirmed (P3); LotCP-S efficiency NOT confirmed (P1 Holm p=0.066, P2 0.29); mango re-draw all 4 confirmed but data seen |
| G6 | pass-with-note | bias correction, scale, replay (validity at small m), season residuals (m=0) all contribute; shrinkage removed (did nothing/harmful); lot-balanced weighting ~no empirical effect, kept for the guarantee |
| G7 | pass | mango + 2 soil libraries, 3 predictors, 2 protocols |
| G8 | pass | no shared samples/lots, no identical spectra, no split groups, row-wise preprocessing |
| G9 | pass | fresh clone: download+checksum, 17 tests, quick mode, 25 tables regenerated identical (after fixing a 403 in the downloader) |
| G10 | fail | panel not yet run with fresh context |
| G11 | pass | 0 untraced numbers in the manuscript |
