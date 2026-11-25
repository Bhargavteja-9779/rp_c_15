# Response to review round 1 (internal), 2026-11-25
Evidence for every action: plan_v4 (experiments/plan_v4.yaml, written before running), results/cycle3/, journal entries 2026-11-24_10 … _15.

| Concern | Action | Where |
|---|---|---|
| R1-C1 pooled headline driven by 2017 | Verified (LotCP-S m=10: 0.919 pooled, 0.893 excl. 2017). Every headline now pooled, season-mean and excl. 2017; abstract states 0.893; LotCP-A met target in 2/5 seasons | Abstract, Table 3, §4.3–4.4 |
| R1-C2 lot-level inference | Season-cluster bootstrap, seasons-favouring counts, note that a 5-season sign test cannot reach p<0.05; Wilcoxon moved to supplement; mixed models degenerate, not used | §3.5, Table 4 |
| R1-C3 confirmation weak | Mango arm relabelled "re-draw check"; P4 "uninformative"; P3 described as width-unconstrained; NeoSpectra described as no-shift data | Table 5, §4.5 |
| R1-C4 matched baselines, selective tables | New baselines (b) and (b′) sharing the lot scale without replay; replay buys coverage at small m, not width; efficiency claim withdrawn from headline; decision table shows all main rules incl. withhold-all | §3.4, §4.3, Table 6 |
| R1-C5, R3-2/4/5 decision claims | Operating point fixed in advance; season-cluster CIs; comparator = cheapest rule without reference fruit; α by leave-one-season-out; rerun with published PLS. Result: reference fruit give no further cost saving; claim restated | §3.7, §4.6, Table 6 |
| R1-C6, R3-6 multiplicity / "pre-registered" | "pre-specified (internal git commit)", not publicly registered; all post-hoc analyses labelled exploratory; excl.-2018 figure reported | §3.8, §4.3 |
| R1-C7 weak predictor | Published PLS recipe reported in all main tables | Tables 3, 4, 6 |
| R1-C8 replicate structure | Efficiency gain stated to depend on repeated scans; single-unit analysis in Note S1 | §4.3, §6 item 6 |
| R1-C9 planner error | Planner error by number of source seasons | §4.7 |
| R1-C10 NeoSpectra overlap | Rebutted with evidence: 1976/2106 layers in KSSL catalogue, 0 among the 19,807 development layers | §3.6, results/cycle3/neospectra_overlap.json |
| R1 number checks | 5.02 vs 5.01 is rounding of 5.015 in two machine-filled sources (supplement only); replay-ablation draws disclosed; ledger v015 corrected | Note S5, state/variants_tried.csv |
| R2-1 novelty framed too broadly | Contributions restated: audit; calibration with measured value of each part; LotCP-A/planner with limits; exploratory decisions | §1.2 |
| R2-2/3/6/7 missing literature | wadoux2025, bouckaert2011, duma2025, mishra2021transfer, yilmaz2022 cited (descriptions limited to what their titles support). Sample-specific PLS interval baseline (plan_v4 E5) NOT run: not implemented within the cycle; stated as omission here | §1.1 |
| R2-4 breadth | Search for second fruit data set (E6) found none; claims restricted to mango | §6 item 2 |
| R2-5/8/9 | Kayaoğlu & Erdem updated; α* named as newsvendor/Bayes threshold; prototype moved to Note S6 | §2.8 |
| R3-1 length | Main text ~7.9k words; Secs 10–14 → Notes S5–S6; full decision analysis → S7; failure story once (S8) | — |
| R3-3 exploratory labels | Abstract, §3.7, §3.8, §4.6, Table 6 caption | — |
| R3-7 data/code | NeoSpectra DOI added; code, results and protocol history "on request" consistently; "released repository" removed | Data availability |
| R3-8 AI disclosure | Methods subsection §3.8 + declaration broadened to research use | §3.8 |
| R3-9 README | Title, cycle 2–3 commands, data sources, stale decision.py reference removed, pytest testpaths | README.md |
| R3-10/11/12 | n and overlap stated; tool caveat on season shift; limitations ranked | §4.5, tool, §6 |

Open item carried to round 2: plan_v4 E5 (sample-specific PLS intervals) not done.
