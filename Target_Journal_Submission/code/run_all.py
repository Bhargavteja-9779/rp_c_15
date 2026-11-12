#!/usr/bin/env python
"""Reproduce the whole study.

    python run_all.py --mode quick    # minutes; reduced computation, checks that the pipeline runs
    python run_all.py --mode full     # the reported experiment (hours on a 4-core CPU)

Stages are idempotent: finished cross-fits in results/predictions/ are reused, so
`python run_all.py --mode full --from eval` regenerates every number, table and figure of the
manuscript from the stored predictions in a few minutes. Quick-mode outputs go to quick_outputs/.
"""
import argparse
import platform
import time

from src.utils import get_device, get_logger, load_config, out_dir, save_json

STAGES = ["crossfit", "extra", "uq", "eval", "robustness", "analysis", "figures", "manuscript"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--from", dest="start", choices=STAGES, default=STAGES[0], help="first stage to run")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    cfg = load_config(args.mode)
    log = get_logger("run_all", cfg)
    log.info("mode=%s device=%s python=%s", args.mode, get_device(), platform.python_version())
    timing = {}
    for stage in STAGES[STAGES.index(args.start):]:
        t = time.time()
        if stage == "crossfit":
            from src.training import crossfit
            crossfit.run(cfg, args.jobs)
        elif stage == "extra":
            from experiments import extra_runs
            extra_runs.run(cfg)
        elif stage == "uq":
            from src.training import uq_models
            uq_models.run(cfg)
        elif stage == "eval":
            from src.evaluation import run_eval
            run_eval.run(cfg, args.jobs)
        elif stage == "robustness":
            from experiments import robustness
            robustness.run(cfg, args.jobs)
            from experiments import spiking
            spiking.run(cfg, args.jobs)
        elif stage == "analysis":
            from src.statistics import analysis
            analysis.run(cfg)
        elif stage == "figures":
            from src.visualization import figures
            figures.run(cfg)
        elif stage == "manuscript" and args.mode == "full":
            try:
                from manuscript import build_manuscript
                build_manuscript.main()
            except ImportError as exc:
                log.warning("manuscript not built: %s", exc)
        timing[stage] = time.time() - t
        log.info("stage %-10s %.0f s", stage, timing[stage])
    save_json(dict(mode=args.mode, device=get_device(), seconds=timing), out_dir(cfg, "results") / "run_timing.json")


if __name__ == "__main__":
    main()
