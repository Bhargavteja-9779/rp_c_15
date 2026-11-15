"""External validation on the Open Soil Spectral Library (vis-NIR): does the coverage loss of
within-population calibration, and its repair with a few local reference samples, carry over to
another agricultural NIR application?

Tasks
  lucas_oc, lucas_ph : train on the LUCAS 2009 campaign, test on the 2015 campaign; lot = 1-degree cell.
  kssl_oc            : five-fold cross-validation over survey projects; lot = project.
Organic/total carbon is modelled as log(1 + %). PLS only. The top-level hold-out unit available for
calibration is the lot (one source campaign; projects), so "season-fold" residuals are lot-fold here.
"""
from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.model_selection import GroupKFold

from src.data.soil import load_soil
from src.evaluation.run_eval import LOTCP_VARIANTS, evaluate
from src.models.point import PLSModel
from src.utils import get_logger, out_dir, save_json

GRID = (10, 15, 20, 25, 30)
SG = dict(sg_window=11, sg_poly=2, sg_deriv=1)
VARIANTS = {k: LOTCP_VARIANTS[k] for k in ("lotcp", "lotcp_s", "lotcp_shrink", "lotcp_s_shrink", "lotcp_a")}


def _gkf(groups, k, seed):
    u = np.unique(groups)
    perm = dict(zip(u, np.random.default_rng(seed).permutation(len(u))))
    g = np.array([perm[x] for x in groups])
    f = np.empty(len(g), int)
    for i, (_, te) in enumerate(GroupKFold(k).split(g, groups=g)):
        f[te] = i
    return f


def _oof(X, y, folds, nc):
    o = np.full(len(y), np.nan)
    for f in np.unique(folds):
        te = folds == f
        o[te] = PLSModel(n_components=nc, **SG).fit(X[~te], y[~te]).predict(X[te])
    return o


def crossfit(X, y, lot, group, src, tgt, seed=0, grid=GRID):
    Xs, ys = X[src], y[src]
    f_lot, f_smp = _gkf(lot[src], 5, seed), _gkf(group[src], 5, seed + 1)
    best, cv = None, {}
    for nc in grid:                                  # latent variables: lot-grouped CV inside the source
        o = _oof(Xs, ys, f_lot, nc)
        cv[nc] = float(np.sqrt(np.mean((ys - o) ** 2)))
        if best is None or cv[nc] < cv[best]:
            best, oof_lot = nc, o
    P = dict(src_idx=np.flatnonzero(src), tgt_idx=np.flatnonzero(tgt), oof_lot=oof_lot, oof_season=oof_lot,
             oof_sample=_oof(Xs, ys, f_smp, best), pred_tgt=PLSModel(n_components=best, **SG).fit(Xs, ys).predict(X[tgt]))
    return P, dict(n_components=best, cv_rmse_lot=cv)


def _task(cfg, name, quick):
    d = load_soil()
    m = d.meta
    ds, col = name.split("_")
    y_all = m["oc_log" if col == "oc" else "ph"].to_numpy(float)
    sel = (m["dataset"] == ds).to_numpy() & np.isfinite(y_all)
    if quick:
        sel &= np.random.default_rng(0).random(len(sel)) < 0.15
    lot, grp = m["population"].to_numpy(), m["group"].to_numpy()
    if ds == "lucas":
        splits = [("2015", sel & (m["season"] == 2009).to_numpy(), sel & (m["season"] == 2015).to_numpy())]
    else:
        fold = _gkf(lot, 5, 7)
        splits = [(f"fold{k}", sel & (fold != k), sel & (fold == k)) for k in range(5 if not quick else 1)]
    data = SimpleNamespace(y=y_all, lot=lot, sample=m["reference_no"].to_numpy(), meta=m)
    rows, points = [], []
    for tag, src, tgt in splits:
        P, info = crossfit(d.X, y_all, lot, grp, src, tgt, grid=GRID if not quick else (10,))
        r_t = y_all[tgt] - P["pred_tgt"]
        points.append(dict(task=name, split=tag, n_source=int(src.sum()), n_target=int(tgt.sum()), n_components=info["n_components"],
                           rmse_cv_sample=float(np.sqrt(np.mean((y_all[src] - P["oof_sample"]) ** 2))),
                           rmse_cv_lot=float(np.sqrt(np.mean((y_all[src] - P["oof_lot"]) ** 2))),
                           rmse_target=float(np.sqrt(np.mean(r_t ** 2))), bias_target=float(r_t.mean()),
                           sd_lot_bias=float(pd.Series(r_t).groupby(lot[tgt]).mean().std()),
                           source_lots=int(len(np.unique(lot[src]))), target_lots=int(len(np.unique(lot[tgt])))))
        res, _, _ = evaluate(cfg, "pls", 0, f"soil_{name}", sum(map(ord, tag)), cfg["eval"]["primary_alpha"], variants=VARIANTS,
                             n_draws=30 if not quick else 3, data=data, P=P)
        for r in res:
            r.update(task=name, split=tag)
        rows += res
    return rows, points


def run(cfg, n_jobs=3):
    log = get_logger("soil", cfg)
    quick = cfg["mode"] != "full"
    tasks = ("lucas_oc", "lucas_ph", "kssl_oc") if not quick else ("kssl_oc",)
    res = Parallel(n_jobs=n_jobs)(delayed(_task)(cfg, t, quick) for t in tasks)
    rdir = out_dir(cfg, "results/soil")
    pd.DataFrame([r for x in res for r in x[0]]).to_csv(rdir / "soil_raw.csv", index=False)
    pd.DataFrame([r for x in res for r in x[1]]).to_csv(rdir / "soil_point.csv", index=False)
    log.info("soil external validation finished")


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
