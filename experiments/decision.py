"""Harvest-decision analysis: one-sided lower prediction bounds against a minimum dry-matter
specification (PLS, forward chaining).

A fruit is "accepted" when the decision statistic is at least the specification t:
  point            : yhat >= t                                  (no uncertainty, no reference samples)
  point_bc         : yhat + mean reference residual >= t        (bias-corrected point prediction)
  scp_lower        : yhat - q >= t, q = one-sided split-conformal quantile of sample-fold residuals
  lotcp_s_lower    : yhat + b_hat - q_m * s_hat >= t            (one-sided LotCP-S)
Reported per lot: coverage of the lower bound P(y >= L), the share of accepted fruit whose true DMC
is below t (false accepts), and the share of truly compliant fruit that is accepted (yield).
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
M_GRID = (0, 5, 10, 20)


def _target(cfg, target, n_draws):
    d = load_data(cfg)
    a = cfg["eval"]["primary_alpha"]
    P = np.load(pred_path(cfg, "pls", 0, "forward", target))
    src, tgt = P["src_idx"], P["tgt_idx"]
    y_t, yh_t = d.y[tgt], P["pred_tgt"].astype(float)
    q_scp = split_quantile(-(d.y[src] - P["oof_sample"]), a)            # over-prediction quantile
    cps = {m: LotCP(m=m, alpha=a, n_episodes=cfg["eval"]["n_episodes"], scale="full", side="lower", seed=3 + m)
           .fit(d.y[src] - P["oof_season"], d.lot[src], d.sample[src], P["oof_season"]) for m in M_GRID}
    rng = np.random.default_rng([17, target])
    rows = []
    for lot in np.unique(d.lot[tgt]):
        li = np.flatnonzero(d.lot[tgt] == lot)
        _, inv, cnt = np.unique(d.sample[tgt][li], return_inverse=True, return_counts=True)
        y, yh = y_t[li], yh_t[li]
        r = y - yh
        smean = np.bincount(inv, weights=r) / cnt
        rv = replicate_variance(yh, inv)
        for m in M_GRID:
            if len(cnt) < m + cfg["eval"]["min_query_samples"]:
                continue
            for dr in range(1 if m == 0 else n_draws):
                sup = rng.choice(len(cnt), m, replace=False)
                q = ~np.isin(inv, sup)
                w = 1.0 / ((len(cnt) - m) * cnt[inv][q])
                b, hw = cps[m].predict(smean[sup], rv)
                stats = {"lotcp_s_lower": yh[q] + b - hw}
                if m == 0:
                    stats["point"], stats["scp_lower"] = yh[q], yh[q] - q_scp
                else:
                    stats["point_bc"] = yh[q] + smean[sup].mean()
                for name, L in stats.items():
                    for t in THRESHOLDS:
                        acc, good = L >= t, y[q] >= t
                        rows.append(dict(target=target, lot=int(lot), m=m, draw=dr, rule=name, threshold=t,
                                         lower_cov=float(np.sum(w * (y[q] >= L))), accepted=float(np.sum(w * acc)),
                                         false_accept=float(np.sum(w * (acc & ~good))), compliant=float(np.sum(w * good)),
                                         true_accept=float(np.sum(w * (acc & good)))))
    return rows


def run(cfg, n_jobs=4):
    log = get_logger("decision", cfg)
    nd = 30 if cfg["mode"] == "full" else 3
    res = Parallel(n_jobs=n_jobs)(delayed(_target)(cfg, t, nd) for t in cfg["protocols"]["forward"]["targets"])
    df = pd.DataFrame([r for x in res for r in x])
    lot = df.groupby(["rule", "m", "threshold", "target", "lot"], as_index=False)[["lower_cov", "accepted", "false_accept", "compliant", "true_accept"]].mean()
    # pooled over lots (each lot equal weight): share of accepted fruit that is non-compliant, and yield
    g = lot.groupby(["rule", "m", "threshold"])
    out = g.agg(n_lots=("lot", "size"), lower_cov=("lower_cov", "mean"), accepted=("accepted", "mean"),
                false_accept=("false_accept", "mean"), compliant=("compliant", "mean"), true_accept=("true_accept", "mean")).reset_index()
    out["false_accept_share"] = out["false_accept"] / out["accepted"]
    out["yield"] = out["true_accept"] / out["compliant"]
    # lots in which more than 10 % of the accepted fruit is non-compliant (lots with any accepted fruit)
    lot["bad"] = (lot["false_accept"] / lot["accepted"].where(lot["accepted"] > 0)) > 0.10
    out = out.merge(lot[lot.accepted > 0].groupby(["rule", "m", "threshold"])["bad"].mean().rename("lots_over_10pct").reset_index(), how="left")
    rdir = out_dir(cfg, "results/robustness")
    out.to_csv(rdir / "decision_summary.csv", index=False)
    lot.to_csv(rdir / "decision_by_lot.csv", index=False)
    log.info("decision analysis finished")


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
