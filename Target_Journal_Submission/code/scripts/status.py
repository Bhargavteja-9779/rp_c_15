#!/usr/bin/env python
"""Print the current state of the autonomous research loop (no LLM needed)."""
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "state"


def j(name, default):
    try:
        return json.loads((S / name).read_text())
    except Exception:
        return default


a, b, q = j("agent_state.json", {}), j("budget.json", {}), j("queue.json", {"jobs": {}})
cfg = a.get("config", {})
print(f"cycle {a.get('cycle')}  phase {a.get('phase')}  step {a.get('step')}  status {a.get('status')}")
print(f"topic: {a.get('topic')}\njournal: {a.get('journal')}")
used = b.get("global_seconds", 0) / 3600 + b.get("pre_protocol_cycle1_hours_estimate", 0)
cyc = b.get("per_cycle_seconds", {}).get(str(a.get("cycle")), 0) / 3600
print(f"compute: cycle {cyc:.2f} h / {cfg.get('COMPUTE_PER_CYCLE_H')} h; global {used:.2f} h / {cfg.get('GLOBAL_COMPUTE_CEILING_H')} h "
      f"(incl. {b.get('pre_protocol_cycle1_hours_estimate', 0)} h estimated cycle-1 compute)")
hb = S / "heartbeat"
if hb.exists():
    age = time.time() - hb.stat().st_mtime
    print(f"heartbeat: {hb.read_text().strip()} ({age / 60:.1f} min ago)")
lock = S / "run.lock"
if lock.exists():
    pid = int(lock.read_text().split()[0])
    try:
        os.kill(pid, 0); print(f"RUNNING: pid {pid}")
    except ProcessLookupError:
        print(f"stale lock (pid {pid} not alive)")
else:
    print("no compute run active")
for k, v in sorted(q.get("jobs", {}).items()):
    print(f"  job {k:28s} {v.get('status'):16s} attempts={v.get('attempts')} {v.get('updated', '')}")
gates = j("gates.json", {})
if gates:
    print("gates: " + "  ".join(f"{k}:{v.get('status')}" for k, v in gates.items()))
sys.exit(0)
