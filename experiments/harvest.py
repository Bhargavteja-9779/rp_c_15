"""Harvest-decision simulator (forward chaining, retrospective).

Fruit-level decision: a scanned fruit is ACCEPTED (harvest / pack) when its decision statistic is at
least the dry-matter specification t, otherwise WITHHELD (wait / re-test). Rules:
  point            yhat >= t                          (no uncertainty, no reference fruit)
  point_bc         yhat + b >= t                      (bias-corrected with m reference fruit)
  scp_lower        yhat - q_src(alpha) >= t           (split-conformal lower bound, sample folds)
  bc_lower         yhat + b - q_src(alpha) >= t       (bias correction + source quantile)
  lotcp_s_lower    yhat + b - q_m(alpha) * s_hat >= t (proposed, one-sided LotCP-S)
  lotcp_a_lower    as above with lot-level assurance delta = 0.10
Lot-level decision: HARVEST the lot when the share of its scanned fruit accepted by the rule is at
least p; the lot is truly READY when the share of its fruit with reference DMC >= t is at least p.

Every quantity is computed on the target season's real reference values. Costs are applied
afterwards in src/statistics/analysis.py under explicitly ASSUMED cost ratios.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from src.data.dataset import load_data
from src.evaluation.conformal import split_quantile
from src.evaluation.lotcp import LotCP, replicate_variance
from src.training.crossfit import pred_path
from src.utils import get_logger, out_dir

THRESHOLDS = (14.0, 15.0, 16.0)
ALPHAS = (0.02, 0.05, 0.1, 0.2, 1 / 3, 0.5)
M_GRID = (0, 3, 5, 10, 20)
LOT_SHARES = (0.8, 0.9)


def _target(cfg, model, target, n_draws):
    d = load_data(cfg)
    ev = cfg["eval"]
    P = np.load(pred_path(cfg, model, 0, "forward", target))
    src, tgt = P["src_idx"], P["tgt_idx"]
    y_t, yh_t = d.y[tgt], P["pred_tgt"].astype(float)
    r_smp = d.y[src] - P["oof_sample"]
    q_src = {a: split_quantile(-r_smp, a) for a in ALPHAS}
    res_season = d.y[src] - P["oof_season"]
    cps = {}
    for m in M_GRID:
        for a in ALPHAS:
            cps[("lotcp_s_lower", m, a)] = LotCP(m=m, alpha=a, n_episodes=ev["n_episodes"], min_query=ev["min_query_samples"],
                                                 scale="full", side="lower", seed=ev["seed"] + m).fit(res_season, d.lot[src], d.sample[src], P["oof_season"])
        cps[("lotcp_a_lower", m, 0.1)] = LotCP(m=m, alpha=0.1, n_episodes=ev["n_episodes"], min_query=ev["min_query_samples"],
                                               scale="full", side="lower", assure=0.1, seed=ev["seed"] + m).fit(res_season, d.lot[src], d.sample[src], P["oof_season"])
    rng = np.random.default_rng([23, target, len(model)])
    fruit, lots = [], []
    for lot in np.unique(d.lot[tgt]):
        li = np.flatnonzero(d.lot[tgt] == lot)
        _, inv, cnt = np.unique(d.sample[tgt][li], return_inverse=True, return_counts=True)
        y, yh = y_t[li], yh_t[li]
        smean = np.bincount(inv, weights=y - yh) / cnt
        rv = replicate_variance(yh, inv)
        for m in M_GRID:
            if len(cnt) < m + ev["min_query_samples"]:
                continue
            for dr in range(1 if m == 0 else n_draws):
                sup = rng.choice(len(cnt), m, replace=False)
                q = ~np.isin(inv, sup)
                w = 1.0 / ((len(cnt) - m) * cnt[inv][q])
                b = float(smean[sup].mean()) if m > 0 else 0.0
                stats = {}
                if m == 0:
                    stats[("point", np.nan)] = yh[q]
                    for a in ALPHAS:
                        stats[("scp_lower", a)] = yh[q] - q_src[a]
                else:
                    stats[("point_bc", np.nan)] = yh[q] + b
                    for a in ALPHAS:
                        stats[("bc_lower", a)] = yh[q] + b - q_src[a]
                for a in ALPHAS:
                    bb, hw = cps[("lotcp_s_lower", m, a)].predict(smean[sup], rv)
                    stats[("lotcp_s_lower", a)] = yh[q] + bb - hw
                bb, hw = cps[("lotcp_a_lower", m, 0.1)].predict(smean[sup], rv)
                stats[("lotcp_a_lower", 0.1)] = yh[q] + bb - hw
                for (rule, a), L in stats.items():
                    for t in THRESHOLDS:
                        acc, good = L >= t, y[q] >= t
                        acc_sh, good_sh = float(np.sum(w * acc)), float(np.sum(w * good))
                        fa, fr = float(np.sum(w * (acc & ~good))), float(np.sum(w * (~acc & good)))
                        fruit.append((model, target, int(lot), m, dr, rule, a, t, acc_sh, good_sh, fa, fr))
                        for p in LOT_SHARES:
                            lots.append((model, target, int(lot), m, dr, rule, a, t, p, acc_sh >= p, good_sh >= p))
    return fruit, lots


def run(cfg, n_jobs=4):
    log = get_logger("harvest", cfg)
    full = cfg["mode"] == "full"
    models = ("pls", "cnn") if full else ("pls",)
    jobs = [delayed(_target)(cfg, mo, t, 20 if full else 2) for mo in models for t in cfg["protocols"]["forward"]["targets"]]
    res = Parallel(n_jobs=n_jobs)(jobs)
    fc = ["model", "target", "lot", "m", "draw", "rule", "alpha", "threshold", "accepted", "compliant", "false_accept", "false_withhold"]
    lc = ["model", "target", "lot", "m", "draw", "rule", "alpha", "threshold", "p", "harvest", "ready"]
    fruit = pd.DataFrame([r for x in res for r in x[0]], columns=fc)
    lots = pd.DataFrame([r for x in res for r in x[1]], columns=lc)
    keys = ["model", "rule", "alpha", "threshold", "m", "target", "lot"]
    fl = fruit.fillna({"alpha": -1}).groupby(keys, as_index=False)[["accepted", "compliant", "false_accept", "false_withhold"]].mean()
    rdir = out_dir(cfg, "results/harvest")
    fl.to_csv(rdir / "fruit_by_lot.csv.gz", index=False)
    ll = lots.fillna({"alpha": -1})
    ll.to_csv(rdir / "lot_decisions.csv.gz", index=False)
    log.info("harvest simulator finished: %d fruit-level lot rows, %d lot decisions", len(fl), len(ll))


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
