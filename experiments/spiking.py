"""Baseline requested in review: 'spiking' = refit the calibration with the m reference samples of
the new lot added to the training set (optionally up-weighted by replication), then use the
source split-conformal half-width. Compared, on identical reference draws, with mean bias
correction of the unchanged model. PLS only, m = 10, few draws (one refit per lot and draw)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from src.data.dataset import load_data
from src.evaluation.conformal import split_quantile
from src.models.point import make_model
from src.training.crossfit import pred_path
from src.utils import get_logger, out_dir


def _target(cfg, target, m, n_draws, weights):
    d = load_data(cfg)
    P = np.load(pred_path(cfg, "pls", 0, "forward", target))
    nc = json.load(open(pred_path(cfg, "pls", 0, "forward", target).with_suffix(".json")))["n_components"]
    src, tgt = P["src_idx"], P["tgt_idx"]
    Xs, ys = d.X[src], d.y[src]
    q0 = split_quantile(np.abs(ys - P["oof_sample"]), cfg["eval"]["primary_alpha"])
    rng = np.random.default_rng([5, target])
    rows = []
    for lot in np.unique(d.lot[tgt]):
        li = tgt[d.lot[tgt] == lot]
        _, inv, cnt = np.unique(d.sample[li], return_inverse=True, return_counts=True)
        if len(cnt) < m + cfg["eval"]["min_query_samples"]:
            continue
        base = P["pred_tgt"][d.lot[tgt] == lot].astype(float)
        for dr in range(n_draws):
            sup = rng.choice(len(cnt), m, replace=False)
            is_sup = np.isin(inv, sup)
            q = ~is_sup
            wq = 1.0 / ((len(cnt) - m) * cnt[inv][q])
            yq = d.y[li][q]

            def rec(name, pred):
                e = yq - pred
                rows.append(dict(target=target, lot=int(lot), draw=dr, method=name, mse=float(np.sum(wq * e ** 2)),
                                 bias=float(np.sum(wq * e)), coverage=float(np.sum(wq * (np.abs(e) <= q0))), width=2 * q0))

            r_sup = d.y[li][is_sup] - base[is_sup]
            b = np.mean(np.bincount(inv[is_sup], weights=r_sup, minlength=len(cnt))[sup] / cnt[sup])
            rec("none", base[q])
            rec("bias_correction", base[q] + b)
            for w in weights:
                Xa = np.vstack([Xs] + [d.X[li][is_sup]] * w)
                ya = np.concatenate([ys] + [d.y[li][is_sup]] * w)
                rec(f"spiking_x{w}", make_model("pls", cfg, n_components=nc).fit(Xa, ya).predict(d.X[li][q]))
    return rows


def run(cfg, n_jobs=4):
    log = get_logger("spiking", cfg)
    full = cfg["mode"] == "full"
    res = Parallel(n_jobs=n_jobs)(delayed(_target)(cfg, t, 10, 3 if full else 1, (1, 20) if full else (1,))
                                  for t in cfg["protocols"]["forward"]["targets"])
    df = pd.DataFrame([r for x in res for r in x])
    df.to_csv(out_dir(cfg, "results/robustness") / "spiking_raw.csv", index=False)
    log.info("spiking baseline finished: %d rows", len(df))


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
