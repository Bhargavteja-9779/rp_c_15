"""Additional cross-fits needed by the robustness / generalisation experiments (PLS only)."""
from __future__ import annotations

from src.training.crossfit import SCHEMES, run_task
from src.utils import get_logger, load_config

EXTRA = (
    [("recent2", t) for t in (2018, 2019, 2020, 2021)]
    + [("region", r) for r in ("NT", "QLD")]
    + [("cultivar", c) for c in ("caly", "kp", "r2e2", "hg", "keitt")]
)


def run(cfg):
    log = get_logger("extra_runs", cfg)
    extra = EXTRA if cfg["mode"] == "full" else EXTRA[:1]
    for protocol, target in extra:
        run_task(cfg, "pls", 0, protocol, target, SCHEMES)
        log.info("done %s/%s", protocol, target)


if __name__ == "__main__":
    import sys

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
