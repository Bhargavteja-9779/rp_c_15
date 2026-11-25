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
    ap.add_argument("--resume", action="store_true", help="skip stages already marked done in state/queue.json")
    ap.add_argument("--cycle", type=int, default=None, help="cycle number for the budget ledger (default: state/agent_state.json)")
    args = ap.parse_args()
    cfg = load_config(args.mode)
    log = get_logger("run_all", cfg)
    log.info("mode=%s device=%s python=%s", args.mode, get_device(), platform.python_version())
    timing = {}
    from src.runstate import STATE, Heartbeat, Lock, budget_hours, job_status, read_json, set_job

    agent = read_json(STATE / "agent_state.json", {})
    cycle = args.cycle or agent.get("cycle", 1)
    ceiling = agent.get("config", {}).get("COMPUTE_PER_CYCLE_H", 15)
    with Lock(), Heartbeat(cycle):
        _run(args, cfg, log, timing, cycle, ceiling, set_job, job_status, budget_hours)
    save_json(dict(mode=args.mode, device=get_device(), seconds=timing), out_dir(cfg, "results") / "run_timing.json")


def _run(args, cfg, log, timing, cycle, ceiling, set_job, job_status, budget_hours):
    for stage in STAGES[STAGES.index(args.start):]:
        job = f"{args.mode}:{stage}"
        if args.resume and job_status(job) == "done":
            log.info("stage %-10s already done (resume)", stage)
            continue
        if args.mode == "full" and budget_hours(cycle) >= ceiling:
            set_job(job, "skipped_budget")
            log.warning("cycle %s compute budget (%.1f h) reached; %s skipped", cycle, ceiling, stage)
            continue
        from src.runstate import read_json, STATE
        if read_json(STATE / "queue.json", {"jobs": {}})["jobs"].get(job, {}).get("status") == "failed_permanent":
            log.warning("stage %s permanently failed earlier; skipped", stage)
            continue
        set_job(job, "running")
        t = time.time()
        try:
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
                from experiments import harvest, soil_external
                harvest.run(cfg, args.jobs)
                if args.mode == "full":
                    from src.tool import harvest_tool
                    harvest_tool.save_demo()
                soil_external.run(cfg)
            elif stage == "analysis":
                from experiments import planning
                planning.run(cfg)
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
        except Exception as exc:                      # mark, retry at most twice via --resume, then give up on the stage
            attempts = read_json(STATE / "queue.json", {"jobs": {}})["jobs"].get(job, {}).get("attempts", 1)
            set_job(job, "failed_permanent" if attempts >= 3 else "failed", error=repr(exc)[:300])
            log.exception("stage %s failed (attempt %d)", stage, attempts)
            raise
        timing[stage] = time.time() - t
        set_job(job, "done", seconds=round(timing[stage], 1))
        log.info("stage %-10s %.0f s", stage, timing[stage])


if __name__ == "__main__":
    main()
