#!/usr/bin/env python
"""Kill a hung compute run (no heartbeat for 20 min) so that `run_all.py --resume` can restart it."""
import os
import signal
import time
from pathlib import Path

S = Path(__file__).resolve().parents[1] / "state"
lock, hb = S / "run.lock", S / "heartbeat"
if lock.exists() and hb.exists() and time.time() - hb.stat().st_mtime > 1200:
    pid = int(lock.read_text().split()[0])
    try:
        os.kill(pid, signal.SIGTERM); print("killed hung run", pid)
    except ProcessLookupError:
        pass
    lock.unlink(missing_ok=True)
