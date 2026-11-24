#!/usr/bin/env python
"""Regenerate HANDOFF.md from state/ (run after every step):  python scripts/handoff.py "NEXT ACTION text" """
import json
import subprocess
import sys
import time
from pathlib import Path

R = Path(__file__).resolve().parents[1]
S = R / "state"
j = lambda n, d: json.loads((S / n).read_text()) if (S / n).exists() else d
a, b, g, q = j("agent_state.json", {}), j("budget.json", {}), j("gates.json", {}), j("queue.json", {"jobs": {}})
if len(sys.argv) > 1:
    a["next_action"] = sys.argv[1]
    a["last_action"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    (S / "agent_state.json").write_text(json.dumps(a, indent=1))
cfg = a.get("config", {})
dec = [l for l in (S / "decisions.md").read_text().splitlines() if l.startswith("- ")][-10:]
fails = sorted(p.name for p in (R / "journal" / "ENTRIES").glob("*FAILURE*"))[-10:]
running = [k for k, v in q["jobs"].items() if v.get("status") == "running"]
lock = (S / "run.lock").read_text().strip() if (S / "run.lock").exists() else "none"
glob_h = b.get("global_seconds", 0) / 3600 + b.get("pre_protocol_cycle1_hours_estimate", 0)
cyc_h = b.get("per_cycle_seconds", {}).get(str(a.get("cycle")), 0) / 3600
try:
    head = subprocess.run(["git", "log", "--oneline", "-1"], cwd=R, capture_output=True, text=True).stdout.strip()
except Exception:
    head = "?"
txt = f"""# HANDOFF — read this first

Updated {time.strftime('%Y-%m-%d %H:%M:%S')} · git HEAD `{head}` · branch `claude/autonomous-research-project-qua0qp` (remote: origin)

## Where we are
* **Cycle {a.get('cycle')} of {cfg.get('MAX_CYCLES')}**, phase `{a.get('phase')}`, status **{a.get('status')}**, pivots used {a.get('pivots_used', 0)}/{cfg.get('MAX_PIVOTS')}
* **NEXT ACTION:** {a.get('next_action', '(not set)')}
* Journal: {a.get('journal')}
* Topic: {a.get('topic')}
* Hypothesis: a few destructively measured reference fruit per lot, used through a lot-exchangeable few-shot conformal calibration (LotCP-S / LotCP-A) calibrated on past lots, give NIR dry-matter error bars that keep their coverage on later harvest seasons and support better harvest decisions than error bars calibrated within the training seasons.

## Running now
* Compute lock: {lock} · running jobs: {', '.join(running) or 'none'}
* Compute used: cycle {cyc_h:.2f} h / {cfg.get('COMPUTE_PER_CYCLE_H')} h · global {glob_h:.2f} h / {cfg.get('GLOBAL_COMPUTE_CEILING_H')} h (includes {b.get('pre_protocol_cycle1_hours_estimate', 0)} h estimated, unmetered cycle-1 compute) · hardware: 4-core CPU, no GPU

## Gates
| Gate | Status | Evidence | Note |
|---|---|---|---|
""" + "\n".join(f"| {k} | {v.get('status')} | {v.get('evidence')} | {v.get('note')} |" for k, v in g.items()) + f"""

## Last decisions
""" + "\n".join(dec) + """

## Last failures (journal/ENTRIES)
""" + "\n".join(f"* {f}" for f in fails) + """

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
"""
(R / "HANDOFF.md").write_text(txt)
print("HANDOFF.md written")
