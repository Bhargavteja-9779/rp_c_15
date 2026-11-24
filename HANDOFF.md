# HANDOFF — read this first

Updated 2026-11-24 19:42:54 · git HEAD `c56708f cycle2: confirmation results (C1 mango re-draw, C2 untouched NeoSpectra), gates update, plan_v3 (published-PLS predictor)` · branch `claude/autonomous-research-project-qua0qp` (remote: origin)

## Where we are
* **Cycle 2 of 12**, phase `cycle2-setup`, status **RUNNING**, pivots used 0/3
* **NEXT ACTION:** Cycle 2: run the blind 3-reviewer panel (fresh context) on manuscript/build/manuscript.md + results; triage into review/round_1.md; then decide cycle-3 plan (G3 novelty 17/25 and G5 partial are the open gates).
* Journal: Smart Agricultural Technology (Elsevier) -- G1 verification pending in cycle 2
* Topic: Few-shot conformal calibration of NIR fruit-maturity predictions across harvest seasons (risk-aware mango harvest decisions)
* Hypothesis: a few destructively measured reference fruit per lot, used through a lot-exchangeable few-shot conformal calibration (LotCP-S / LotCP-A) calibrated on past lots, give NIR dry-matter error bars that keep their coverage on later harvest seasons and support better harvest decisions than error bars calibrated within the training seasons.

## Running now
* Compute lock: none · running jobs: none
* Compute used: cycle 0.00 h / 15 h · global 6.00 h / 120 h (includes 6.0 h estimated, unmetered cycle-1 compute) · hardware: 4-core CPU, no GPU

## Gates
| Gate | Status | Evidence | Note |
|---|---|---|---|
| G1 | pass-with-stated-failure | journal_selection/verification_cycle2.md | per-article dates unverifiable (403/Crossref empty); publisher average 69-72 d |
| G2 | pass | state/novelty_ledger.json, literature/claims_table.md | 80 logged queries; 39 papers opened (abstract level); close new works now cited and differentiated in Section 2 |
| G3 | fail (own score 17/25; blind score pending) | state/novelty_ledger.json scores | needs >= 20 with no dimension < 3 |
| G4 | pass-partial | results/reproduction/reproduction.csv, literature/reported_results.md | published PLS RMSEP 1.01 reproduced (1.045); published CNN 0.77 not reproduced (ours 1.07, no augmentation/tuning); our SNV-PLS pipeline 0.35 worse than the published recipe |
| G5 | partial | results/confirmation/confirmation_tests.csv | untouched data: LotCP-A assurance confirmed (P3); LotCP-S efficiency NOT confirmed (P1 Holm p=0.066, P2 0.29); mango re-draw all 4 confirmed but data seen |
| G6 | pass-with-note | tables/table5_ablation.csv, results/ablation_cycle2/replay_ablation.csv | bias correction, scale, replay (validity at small m), season residuals (m=0) all contribute; shrinkage removed (did nothing/harmful); lot-balanced weighting ~no empirical effect, kept for the guarantee |
| G7 | pass | tables/table13_soil.csv, tables/table7_generalisation.csv | mango + 2 soil libraries, 3 predictors, 2 protocols |
| G8 | pass | results/leakage_audit.json, scripts/leakage_audit.py | no shared samples/lots, no identical spectra, no split groups, row-wise preprocessing |
| G9 | pass | journal/ENTRIES/2026-11-24_08_RESULT.md | fresh clone: download+checksum, 17 tests, quick mode, 25 tables regenerated identical (after fixing a 403 in the downloader) |
| G10 | fail |  | panel not yet run with fresh context |
| G11 | pass | scripts/audit_numbers.py, scripts/audit_allowlist.txt | 0 untraced numbers in the manuscript |

## Last decisions
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

## Last failures (journal/ENTRIES)
* 2026-11-10_03_FAILURE.md
* 2026-11-14_01_FAILURE.md
* 2026-11-24_03_FAILURE.md
* 2026-11-24_05_FAILURE.md

## Commands
* Status: `python scripts/status.py`
* Logs: `ls results/experiment_logs/` · `tail -f logs/supervisor.log`
* Resume compute: `tmux new -d -s research-compute 'python run_all.py --mode full --resume'`
* Stop compute: `tmux kill-session -t research-compute` (the lock is released; resume later with the command above)
* Agent supervisor (headless restarts after usage limits): `tmux new -d -s research-supervisor scripts/supervisor.sh` · stop: `touch state/STOP`
  (the supervisor runs `claude -p` with `--dangerously-skip-permissions`; only use it on a machine and repository you are willing to give the agent full control of)
* Autostart on your machine: `scripts/install_autostart.sh` · remove: `scripts/remove_autostart.sh`
* Move to a new account/machine: `git clone` the branch above (or copy the folder), download the data (`python -m src.data.download`; soil files download on first use), then paste `BOOTSTRAP_PROMPT.txt` into the new agent.

## Known problems
* This project was developed in an ephemeral cloud container: autostart services were NOT installed there; persistence is the git branch. Raw data are not in git (re-download; checksums in config).
* ScienceDirect returns 403 to automated access: journal acceptance times cannot be verified per article from here (G1).
* No untouched test set remains for the mango or LUCAS/KSSL data (used in cycle 1); confirmation must use data pre-registered in experiments/plan_v2.yaml.

## Where things are
HANDOFF.md, MASTER_PROMPT.md, BOOTSTRAP_PROMPT.txt · state/ (agent_state, queue, budget, heartbeat, gates, variants_tried.csv, decisions.md, novelty_ledger.json) · journal/ENTRIES/ (research diary) · journal_selection/ · literature/ · experiments/ (PROTOCOL.md, plan_v*.yaml) · src/, scripts/, tests/, config/ · results/, tables/, figures/ · manuscript/ (paper sources; builder) · review/ (review rounds) · Smart_Agricultural_Technology_Submission.zip (last packaged submission)
