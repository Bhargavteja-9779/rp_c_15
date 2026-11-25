"""plan_v4 E5: sample-specific PLS prediction intervals (leverage-scaled), the classical chemometric alternative.

Half-width = q * sqrt(1 + h(x)), with h the leverage of x in the PLS score space of the model that predicted it
(h = t' (T'T)^-1 t + 1/n). q is the conformal (1 - alpha) quantile of normalised residuals |r| / sqrt(1 + h):
  lev_sample   : sample-fold residuals (within-population calibration, as classical intervals assume), m = 0
  lev_season   : season-held-out residuals, m = 0
  lev_bc       : bias correction from m reference fruit + quantile of |r - own lot mean| / sqrt(1 + h) on
                 season-held-out residuals (no replay), m in {5, 10}
SNV PLS, forward chaining, alpha = 0.10, same lot/sample/scan weights as the main evaluation, 20 draws per lot and m.
Exploratory (added after review). Output: results/cycle3/pls_leverage.csv (lot level) and pls_leverage_summary.csv.
"""
import json

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from src.data.dataset import load_data
from src.evaluation.conformal import weighted_quantile
from src.models.point import make_model
from src.training.crossfit import pred_path
from src.utils import load_config, out_dir

ALPHA, M_GRID, N_DRAWS = 0.10, (0, 5, 10), 20


def _lev(model, X, Ttr):
    T = model.model.transform(model._prep(X))
    G = np.linalg.inv(Ttr.T @ Ttr)
    return np.einsum("ij,jk,ik->i", T, G, T) + 1.0 / len(Ttr)


def _oof_lev(cfg, nc, Xs, ys, folds):
    h, pred = np.full(len(ys), np.nan), np.full(len(ys), np.nan)
    for f in np.unique(folds):
        te = folds == f
        mdl = make_model("pls", cfg, 0, n_components=nc).fit(Xs[~te], ys[~te])
        Ttr = mdl.model.transform(mdl._prep(Xs[~te]))
        h[te], pred[te] = _lev(mdl, Xs[te], Ttr), mdl.predict(Xs[te])
    return h, pred


def one(target):
    cfg = load_config("full")
    d = load_data(cfg)
    P = np.load(pred_path(cfg, "pls", 0, "forward", target))
    nc = json.load(open(str(pred_path(cfg, "pls", 0, "forward", target)).replace(".npz", ".json")))["n_components"]
    src, tgt = P["src_idx"], P["tgt_idx"]
    Xs, ys = d.X[src], d.y[src]
    h_smp, p_smp = _oof_lev(cfg, nc, Xs, ys, P["fold_sample"])
    h_sea, p_sea = _oof_lev(cfg, nc, Xs, ys, P["fold_season"])
    final = make_model("pls", cfg, 0, n_components=nc).fit(Xs, ys)
    h_t = _lev(final, d.X[tgt], final.model.transform(final._prep(Xs)))
    yh_t = final.predict(d.X[tgt])
    lot_s, smp_s = d.lot[src], d.sample[src]

    def w_src(lot, smp):                    # lot-balanced, sample-balanced, scan-balanced source weights
        df = pd.DataFrame({"lot": lot, "smp": smp})
        ns = df.groupby("lot").smp.transform("nunique").to_numpy()
        nj = df.groupby(["lot", "smp"]).smp.transform("size").to_numpy()
        return 1.0 / (ns * nj)

    ws = w_src(lot_s, smp_s)
    q_smp = weighted_quantile(np.abs(ys - p_smp) / np.sqrt(1 + h_smp), ws, 1 - ALPHA, inf_mass=1.0 / (len(np.unique(lot_s)) + 1))
    r_sea = ys - p_sea
    q_sea = weighted_quantile(np.abs(r_sea) / np.sqrt(1 + h_sea), ws, 1 - ALPHA, inf_mass=1.0 / (len(np.unique(lot_s)) + 1))
    lm = pd.Series(r_sea).groupby(lot_s).transform("mean").to_numpy()
    q_bc = weighted_quantile(np.abs(r_sea - lm) / np.sqrt(1 + h_sea), ws, 1 - ALPHA, inf_mass=1.0 / (len(np.unique(lot_s)) + 1))
    rng = np.random.default_rng([31, target])
    rows = []
    y_t, r_t = d.y[tgt], d.y[tgt] - yh_t
    for lot in np.unique(d.lot[tgt]):
        li = np.flatnonzero(d.lot[tgt] == lot)
        _, inv, cnt = np.unique(d.sample[tgt][li], return_inverse=True, return_counts=True)
        smean = np.bincount(inv, weights=r_t[li]) / cnt
        s = np.sqrt(1 + h_t[li])
        for m in M_GRID:
            if len(cnt) < m + 10:
                continue
            acc = {}
            for dr in range(1 if m == 0 else N_DRAWS):
                sup = rng.choice(len(cnt), m, replace=False)
                q = ~np.isin(inv, sup)
                w = 1.0 / ((len(cnt) - m) * cnt[inv][q])
                cands = {"lev_sample": (0.0, q_smp), "lev_season": (0.0, q_sea)} if m == 0 else {"lev_bc": (float(smean[sup].mean()), q_bc)}
                for k, (b, qq) in cands.items():
                    e, hw = r_t[li][q] - b, qq * s[q]
                    cov = float(np.sum(w * (np.abs(e) <= hw)))
                    isc = float(np.sum(w * (2 * hw + (2 / ALPHA) * np.maximum(np.abs(e) - hw, 0))))
                    acc.setdefault(k, []).append((cov, float(np.sum(w * 2 * hw)), isc))
            for k, v in acc.items():
                v = np.array(v)
                rows.append(dict(model="pls", target=target, lot=int(lot), method=k, m=m, coverage=v[:, 0].mean(),
                                 width=v[:, 1].mean(), iscore=v[:, 2].mean(), meets=float(np.mean(v[:, 0] >= 1 - ALPHA))))
    return rows


if __name__ == "__main__":
    res = Parallel(n_jobs=3)(delayed(one)(t) for t in (2017, 2018, 2019, 2020, 2021))
    df = pd.DataFrame([r for x in res for r in x])
    od = out_dir(load_config("full"), "results/cycle3")
    df.to_csv(od / "pls_leverage.csv", index=False)
    main = pd.read_csv("results/raw_results.csv")
    main = main[(main.model == "pls") & (main.protocol == "forward") & (main.alpha == 0.1) & (main.seed == 0)
                & main.method.isin(["scp_sample", "scp_season", "biascorr_naive", "lotcp_s"]) & main.m.isin(M_GRID)]
    allr = pd.concat([df, main[df.columns.intersection(main.columns)]]).replace(np.inf, np.nan)
    rows = []
    for (meth, m), g in allr.groupby(["method", "m"]):
        s = g.groupby("target").coverage.mean()
        rows.append(dict(method=meth, m=m, n_lots=len(g), coverage=g.coverage.mean(), coverage_ex2017=g[g.target != 2017].coverage.mean(),
                         seasons_ge_090=int((s >= 0.9).sum()), meets=g.meets.mean(), width=g.width.mean(), iscore=g.iscore.mean()))
    out = pd.DataFrame(rows)
    out.to_csv(od / "pls_leverage_summary.csv", index=False)
    print(out.round(3).to_string(index=False))
