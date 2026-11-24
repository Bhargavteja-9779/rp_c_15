"""Run-time persistence: lock file, heartbeat, compute-budget ledger and job queue (Section 3, Layer A).

All writes are atomic (temp file + rename). Compute time is counted only while a stage is actually running
and is persisted every minute, so it survives restarts and excludes downtime.
"""
from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

from src.utils import ROOT

STATE = ROOT / "state"
LOCK = STATE / "run.lock"


def _atomic_write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, path)


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path: Path, obj):
    _atomic_write(path, json.dumps(obj, indent=1, default=str))


class Lock:
    """Refuse to run twice. A lock whose PID is dead is stale and is taken over."""

    def __enter__(self):
        if LOCK.exists():
            pid = int(LOCK.read_text().split()[0] or 0)
            try:
                os.kill(pid, 0)
                raise SystemExit(f"another run is active (pid {pid}); see state/run.lock")
            except ProcessLookupError:
                pass
        _atomic_write(LOCK, f"{os.getpid()} {time.strftime('%Y-%m-%dT%H:%M:%S')}\n")
        return self

    def __exit__(self, *exc):
        LOCK.unlink(missing_ok=True)


class Heartbeat:
    """Touch state/heartbeat every `period` s and add elapsed compute seconds to state/budget.json."""

    def __init__(self, cycle: int, period: int = 60):
        self.cycle, self.period = cycle, period
        self._stop = threading.Event()
        self._last = time.time()

    def _flush(self):
        now = time.time()
        dt, self._last = now - self._last, now
        b = read_json(STATE / "budget.json", {"global_seconds": 0.0, "per_cycle_seconds": {}})
        b["global_seconds"] = b.get("global_seconds", 0.0) + dt
        key = str(self.cycle)
        b.setdefault("per_cycle_seconds", {})[key] = b["per_cycle_seconds"].get(key, 0.0) + dt
        b["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        write_json(STATE / "budget.json", b)
        _atomic_write(STATE / "heartbeat", time.strftime("%Y-%m-%dT%H:%M:%S") + "\n")

    def _loop(self):
        while not self._stop.wait(self.period):
            self._flush()

    def __enter__(self):
        self._flush()
        self._t = threading.Thread(target=self._loop, daemon=True)
        self._t.start()
        return self

    def __exit__(self, *exc):
        self._stop.set()
        self._flush()


def budget_hours(cycle: int | None = None) -> float:
    b = read_json(STATE / "budget.json", {"global_seconds": 0.0, "per_cycle_seconds": {}})
    s = b["global_seconds"] if cycle is None else b.get("per_cycle_seconds", {}).get(str(cycle), 0.0)
    return s / 3600.0


def set_job(job: str, status: str, **extra):
    q = read_json(STATE / "queue.json", {"jobs": {}})
    j = q["jobs"].setdefault(job, {"status": "pending", "attempts": 0})
    if status == "running":
        j["attempts"] = j.get("attempts", 0) + 1
    j.update(status=status, updated=time.strftime("%Y-%m-%dT%H:%M:%S"), **extra)
    write_json(STATE / "queue.json", q)


def job_status(job: str) -> str:
    return read_json(STATE / "queue.json", {"jobs": {}})["jobs"].get(job, {}).get("status", "pending")
