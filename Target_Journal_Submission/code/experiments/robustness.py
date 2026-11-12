"""Robustness, sensitivity, shift-type, subgroup, error and cost analyses (PLS predictor unless stated).

Every block writes a tidy CSV into results/robustness/; tables and figures are built from them."""
from __future__ import annotations

import copy
import time

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from experiments.extra_runs import EXTRA
from src.data.dataset import load_data
from src.evaluation.conformal import split_quantile
from src.evaluation.lotcp import LotCP, replicate_variance
from src.evaluation.run_eval import LOTCP_VARIANTS, evaluate
from src.training.crossfit import pred_path
from src.utils import get_logger, out_dir, save_json

CORE = {k: LOTCP_VARIANTS[k] for k in ("lotcp", "lotcp_s")}


def _ev(cfg, tag, value, *args, **kw):
    """One robustness job, cached on disk so that an interrupted grid can resume."""
    import hashlib
    import pickle

    key = hashlib.md5(repr((tag, value, args, sorted((k, repr(v)) for k, v in kw.items() if k != "keep_mask"),
                            cfg["eval"]["n_episodes"])).encode()).hexdigest()[:16]
    cache = out_dir(cfg, "results/eval_cache") / f"rob_{tag}_{key}.pkl"
    if cache.exists():
        with open(cache, "rb") as fh:
            return pickle.load(fh)
    rows, _, _ = evaluate(cfg, *args, **kw)
    for r in rows:
        r["factor"], r["level"] = tag, value
    with open(cache, "wb") as fh:
        pickle.dump(rows, fh)
    return rows


def run(cfg, n_jobs=4):
    log = get_logger("robustness", cfg)
    rdir = out_dir(cfg, "results/robustness")
    targets = cfg["protocols"]["forward"]["targets"]
    a = cfg["eval"]["primary_alpha"]
    d = load_data(cfg)
    jobs = []
    # (a) noisy reference values for the m reference samples (SD in % DM)
    for sd in (0.25, 0.5):
        jobs += [delayed(_ev)(cfg, "label_noise_sd", sd, "pls", 0, "forward", t, a, variants=CORE, label_noise_sd=sd) for t in targets]
    # (b) provider-flagged outliers removed from calibration and evaluation rows
    keep = (d.meta["outlier_flag_1"].to_numpy() == 0)
    jobs += [delayed(_ev)(cfg, "outliers_removed", 1, "pls", 0, "forward", t, a, variants=CORE, keep_mask=keep) for t in targets]
    # (c) number of past lots available for calibration
    for k in (10, 20, 40, 80):
        for rep in range(5 if cfg["mode"] == "full" else 1):
            jobs += [delayed(_ev)(cfg, "n_cal_lots", k, "pls", 0, "forward", t, a, variants=CORE, cal_lots_k=k, cal_rep=rep,
                                  baselines=False, n_draws=30) for t in targets]
    # (d) number of calibration episodes
    for ne in (5, 10, 100):
        c2 = copy.deepcopy(cfg); c2["eval"]["n_episodes"] = ne
        jobs += [delayed(_ev)(c2, "n_episodes", ne, "pls", 0, "forward", t, a, variants=CORE, baselines=False, n_draws=30) for t in targets]
    # (e) pseudo-count grid of the scale estimate
    for grid in ((5,), (20,), (80,)):
        v = {"lotcp_s": ("season", {"scale": "full", "nu_grid": grid})}
        jobs += [delayed(_ev)(cfg, "nu0", grid[0], "pls", 0, "forward", t, a, variants=v, baselines=False, n_draws=30) for t in targets]
    # (e2) constants estimated on one half of the past lots, quantile on the other half
    v = {"lotcp_s": ("season", {"scale": "full", "split_constants": True}), "lotcp": ("season", {"split_constants": True})}
    jobs += [delayed(_ev)(cfg, "split_constants", 1, "pls", 0, "forward", t, a, variants=v, baselines=False, n_draws=30) for t in targets]
    # (e3) deployment unit = one instrument unit within a lot (reference fruit scanned by that unit only)
    jobs += [delayed(_ev)(cfg, "unit", "lot_instrument", "pls", 0, "forward", t, a, variants=CORE, unit="lot_instrument", n_draws=30) for t in targets]
    # (f) other shift protocols
    extra = [e for e in EXTRA if pred_path(cfg, "pls", 0, *e).exists()]
    jobs += [delayed(_ev)(cfg, "protocol", f"{p}:{t}", "pls", 0, p, t, a, variants=CORE) for p, t in extra]
    if cfg["mode"] != "full":
        jobs = jobs[:3] + jobs[-1:]
    t0 = time.time()
    res = Parallel(n_jobs=n_jobs)(jobs)
    pd.DataFrame([r for x in res for r in x]).to_csv(rdir / "robustness_raw.csv", index=False)
    log.info("robustness grid: %d jobs, %.0f s", len(jobs), time.time() - t0)

    # (g) spectrum-level coverage for subgroup and error analysis -------------------------------
    sub = []
    m, n_draws = 10, 30
    for t in targets:
        P = np.load(pred_path(cfg, "pls", 0, "forward", t))
        src, tgt = P["src_idx"], P["tgt_idx"]
        r_t = d.y[tgt] - P["pred_tgt"]
        res_season, res_sample = d.y[src] - P["oof_season"], d.y[src] - P["oof_sample"]
        q_scp = split_quantile(np.abs(res_sample), a)
        cp = {name: LotCP(m=m, alpha=a, n_episodes=cfg["eval"]["n_episodes"], seed=1, **kw).fit(
            res_season, d.lot[src], d.sample[src], P["oof_season"]) for name, (_, kw) in CORE.items()}
        seen_inst = set(d.meta["instrument"].to_numpy()[src]); seen_cult = set(d.meta["cultivar"].to_numpy()[src])
        rng = np.random.default_rng([11, t])
        meta_t = d.meta.iloc[tgt].reset_index(drop=True)
        for lot in np.unique(d.lot[tgt]):
            li = np.flatnonzero(d.lot[tgt] == lot)
            _, inv, cnt = np.unique(d.sample[tgt][li], return_inverse=True, return_counts=True)
            if len(cnt) < m + cfg["eval"]["min_query_samples"]:
                continue
            smean = np.bincount(inv, weights=r_t[li]) / cnt
            rv = replicate_variance(P["pred_tgt"][li], inv)
            hit = {k: np.zeros(len(li)) for k in ("scp_sample", "lotcp", "lotcp_s")}
            n_q = np.zeros(len(li))
            hw = {k: [] for k in ("lotcp", "lotcp_s")}
            for _ in range(n_draws):
                sup = rng.choice(len(cnt), m, replace=False)
                q = ~np.isin(inv, sup)
                n_q += q
                hit["scp_sample"] += q & (np.abs(r_t[li]) <= q_scp)
                for name in ("lotcp", "lotcp_s"):
                    b, h = cp[name].predict(smean[sup], rv)
                    hit[name] += q & (np.abs(r_t[li] - b) <= h)
                    hw[name].append(h)
            mt = meta_t.iloc[li]
            f = pd.DataFrame({
                "target": t, "lot": lot, "sample": d.sample[tgt][li], "dm": d.y[tgt][li], "resid": r_t[li],
                "cultivar": mt["cultivar"].to_numpy(), "region": mt["region"].to_numpy(), "temp": mt["temp"].to_numpy(),
                "physio_stage": mt["physio_stage"].to_numpy(), "instrument": mt["instrument"].to_numpy(),
                "inst_seen": mt["instrument"].isin(seen_inst).to_numpy(), "cult_seen": mt["cultivar"].isin(seen_cult).to_numpy(),
                "outlier_flag": mt["outlier_flag_1"].to_numpy(), "w": 1.0 / (len(cnt) * cnt[inv]),
                "lot_bias": smean.mean(), "lot_sd": np.sqrt(np.average((r_t[li] - smean.mean()) ** 2)), "rep_sd": np.sqrt(rv) if np.isfinite(rv) else np.nan,
                "hw_lotcp": np.mean(hw["lotcp"]), "hw_lotcp_s": np.mean(hw["lotcp_s"]), "hw_scp": q_scp,
                "prior_sd": np.sqrt(cp["lotcp_s"].sigma2 + cp["lotcp_s"].e0), "tau": np.sqrt(cp["lotcp_s"].tau2),
            })
            for k in hit:
                f[f"cov_{k}"] = hit[k] / np.maximum(n_q, 1)
            sub.append(f[n_q > 0])
    pd.concat(sub).to_csv(rdir / "spectrum_level.csv.gz", index=False)

    # (h) cost of calibration and prediction ----------------------------------------------------
    t = targets[-1]
    P = np.load(pred_path(cfg, "pls", 0, "forward", t)); src = P["src_idx"]
    res_season = d.y[src] - P["oof_season"]
    cost = {}
    for name, (_, kw) in CORE.items():
        for m in (0, 10, 30):
            t0 = time.perf_counter()
            cp = LotCP(m=m, alpha=a, n_episodes=cfg["eval"]["n_episodes"], **kw).fit(res_season, d.lot[src], d.sample[src], P["oof_season"])
            fit_s = time.perf_counter() - t0
            t0 = time.perf_counter()
            for _ in range(1000):
                cp.predict(np.zeros(m), 0.1)
            cost[f"{name}_m{m}"] = {"calibration_seconds": fit_s, "predict_microseconds": (time.perf_counter() - t0) * 1e3,
                                    "n_cal_lots": cp.info["n_cal_lots"]}
    save_json(cost, rdir / "cost.json")
    log.info("robustness finished")


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
