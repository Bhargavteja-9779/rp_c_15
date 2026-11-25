# Decisions log (append only)

Entries before 2026-11-24 are RECONSTRUCTED from git history, experiments/PROTOCOL.md (deviations D1–D7) and the review files; they were not written in this file at the time.

- 2026-11-10 [cycle 1, reconstructed] Target journal: Smart Agricultural Technology (Elsevier) — only Q1-listed candidate found with a publisher-reported average submission→acceptance ≤ 72 days (69–72 d). Per-article Received/Accepted dates were NOT verified then.
- 2026-11-10 [cycle 1, reconstructed] Topic: conformal error bars for NIR mango dry matter across harvest seasons; data Mendeley 10.17632/46htwnp833 v6.
- 2026-11-10 [cycle 1, reconstructed] Protocol committed before training (commit a90a8bd).
- 2026-11-10 [cycle 1, reconstructed] D1: LotCP-S scale added after PLS/2018 smoke test showed under-coverage.
- 2026-11-10 [cycle 1, reconstructed] D3: CNN 20 epochs (compute), lot folds for one CNN seed only.
- 2026-11-14 [cycle 1, reconstructed] D5: shrinkage removed after it failed on LUCAS soil data; all mango results recomputed.
- 2026-11-15 [cycle 1, reconstructed] D7: LotCP-A added after main results known.
- 2026-11-18 [cycle 1, reconstructed] Repositioned as harvest-decision workflow on supervisor's advice; authors P N Bhargav Teja / Ragavan K.
- 2026-11-24 [cycle 2] Adopt all cycle-1 work as cycle 1 of the master-prompt-v2 loop instead of restarting; reason: rule "do not restart finished work"; the topic satisfies Section 5 criteria and pivoting without evidence of failure would waste the budget.
- 2026-11-24 [cycle 2] The later-season mango lots and the LUCAS/KSSL vis-NIR tasks were all seen during cycle-1 development, so none can serve as an untouched TEST SET (rule 5). Decision: the G5 confirmation will be run (i) on mango with SEEDS_CONFIRM for the reference draws/episodes (fresh randomness, same lots — reported as a re-draw confirmation, not a fresh-data test) and (ii) on a dataset NOT opened in cycle 1, pre-registered in experiments/plan_v2.yaml before any of its data are loaded.
- 2026-11-24 [cycle 2] Persistence: repository root plays the role of "project/"; remote = origin branch claude/autonomous-research-project-qua0qp. Supervisor scripts are provided for the user's machine; not installed as a boot service in this ephemeral cloud container.
- 2026-11-24 [cycle 2] plan_v2 committed (5a045c5) before loading the NeoSpectra confirmation data; confirmation endpoints P1–P4 fixed.
- 2026-11-24 [cycle 2] C2 lot rule applied as pre-registered: only 16 projects have >= 20 samples (< 20 required) -> lot = 1-degree cell; 20 cells have >= 20 samples (structure-only count). Target: `eoc_tot_c` (KSSL estimated organic carbon) as "soil organic carbon", log(1 + %). Expect low power (~20 evaluable target lots at m <= 10, ~10 at m = 20); accepted as pre-registered.
- 2026-11-24 [cycle 2] C2 crashed (NaN coordinates in cell construction, a coding bug); fixed by building cells only for samples with coordinates (they were already excluded by the 'ok' mask). No results had been produced; no plan change.

## 2026-11-24 — cycle 3 (review round 1)
- Ledger v015 corrected: single-instrument LotCP-S coverage is 0.919 at m=10 (results/robustness, factor=unit); the logged 0.914 was not traceable (R1 number check).
- Manuscript restructured (≤10k words): old sections archived in manuscript/sections_v2_archive/; Secs 10–14 and the full decision analysis moved to Supplementary Notes S5–S7; development history to S8.
- Claims changed by plan_v4 evidence: efficiency of LotCP-S no longer a headline (replay buys validity, E2); decision savings credited to calibrated bounds, not reference fruit (E4); LotCP-A assurance stated as met in 2/5 seasons (E1); "pre-registered" → "pre-specified (internal git commit)".
- R1-C10 rebutted with evidence: NeoSpectra layers disjoint from KSSL development layers (E7).
- No second commodity found (E6): breadth stays limited; claims restricted to mango.

## 2026-11-25 — cycle 4, pivot 1 (plan_v5) closed as negative
Author asked for more novelty (option a), target blind novelty > 23/25. Pivot 1 (season-sequential calibration) failed
its pre-stated success rule; kept as a negative result (results/cycle4). Next: pivot 2 (plan_v6), label-free
lot-shift indicators and adaptive reference budgets.
- 2026-11-25 plan_v7: group_quantiles briefly changed to plain quantiles after a degenerate simulation (8 lots/season);
  reverted to the pre-specified conformal per-season quantile; plain variant kept as sensitivity (Rplain, ARplain).
  Test simulation uses 12 lots/season (finite quantiles), 150 repetitions.
