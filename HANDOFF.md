# HANDOFF — read this first

Updated 2026-11-24 19:11:50 · git HEAD `6a8ea6d Reposition as risk-aware harvest-decision workflow; new title, authors, declarations; submission zip for Smart Agricultural Technology` · branch `claude/autonomous-research-project-qua0qp` (remote: origin)

## Where we are
* **Cycle 2 of 12**, phase `cycle2-setup`, status **RUNNING**, pivots used 0/3
* **NEXT ACTION:** Cycle 2: (1) G4 — reproduce the published PLS baseline of Anderson et al. 2020 on their own split; (2) write experiments/plan_v2.yaml pre-registering the confirmation (SEEDS_CONFIRM, frozen LotCP config, untouched dataset) and commit it BEFORE loading that dataset; (3) leakage audit, number audit, fresh-clone test; (4) blind 3-reviewer panel.
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
| G2 | fail | state/novelty_ledger.json (to be built) | ~48 references verified by record/abstract; full texts mostly not opened; ledger with queries not yet built |
| G3 | unknown |  | needs own + blind score |
| G4 | fail |  | published baselines not yet reproduced |
| G5 | fail |  | no frozen confirmation on SEEDS_CONFIRM / untouched data yet |
| G6 | unknown | tables/table5_ablation.csv | shrinkage removed; season folds matter only at m=0; need LotCP-S ablation w/o episodic |
| G7 | pass | tables/table13_soil.csv, tables/table7_generalisation.csv | mango + 2 soil libraries, 3 predictors, 2 protocols |
| G8 | fail | tests/test_splits.py | needs documented leakage audit script (duplicates, group overlap) |
| G9 | fail |  | fresh-clone test not run |
| G10 | fail |  | panel not yet run with fresh context |
| G11 | fail |  | scripts/audit_numbers.py missing |

## Last decisions
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

## Last failures (journal/ENTRIES)
* 2026-11-10_03_FAILURE.md
* 2026-11-14_01_FAILURE.md

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
