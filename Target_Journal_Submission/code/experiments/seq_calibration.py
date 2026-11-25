"""plan_v5: season-sequential calibration (LotCP-Seq), exploratory.

Within a target season, lots are processed in harvest-date order. The reference fruit of EARLIER lots of the same season
give leave-one-out (LOO) scores; their (1 - alpha) quantile relative to the same quantile on past-season lots is a
season inflation factor rho, shrunk towards 1 (log rho_hat = n / (n + n0) log rho, n = LOO scores seen), which multiplies
the LotCP-S / LotCP-A half-width of the next lot. n0 is chosen by replaying the procedure inside the source seasons only.
Outputs: results/cycle4/seq_lots.csv (lot level), seq_n0.csv (tuning), printed summary.
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from src.data.dataset import load_data
from src.evaluation.conformal import weighted_quantile
from src.evaluation.lotcp import LotCP, replicate_variance
from src.training.crossfit import pred_path
from src.utils import load_config, out_dir

ALPHA = 0.10
N0_GRID = (3.0, 10.0, 30.0, 100.0, np.inf)
N_DRAWS = 20


def lot_dates(d):
    dt = pd.to_datetime(d.meta["date"], format="%Y-%m-%d", errors="coerce")
    first = dt.groupby(d.lot).min()
    return {int(k): (v if pd.notna(v) else pd.Timestamp.max) for k, v in first.items()}


def _scale(cp, sup_means, rv):
    k = len(sup_means)
    u2 = cp.sigma2
    if k >= 2:
        u2 = (cp.nu0 * cp.sigma2 + float(np.var(sup_means, ddof=1)) * (k - 1)) / (cp.nu0 + k - 1)
    e2 = rv if np.isfinite(rv) else cp.e0
    return float(np.sqrt(u2 + e2))


def loo_scores(cp, sup_means, rv):
    out = []
    for j in range(len(sup_means)):
        oth = np.delete(sup_means, j)
        out.append(abs(sup_means[j] - oth.mean()) / _scale(cp, oth, rv))
    return np.array(out)


class LotStruct:
    def __init__(self, r, pred, smp):
        _, self.inv, self.cnt = np.unique(smp, return_inverse=True, return_counts=True)
        self.r = r
        self.smean = np.bincount(self.inv, weights=r) / self.cnt
        self.rv = replicate_variance(pred, self.inv)
        self.ns = len(self.cnt)


def build(r, pred, lot, smp):
    return {int(l): LotStruct(r[lot == l], pred[lot == l], smp[lot == l]) for l in np.unique(lot)}


def past_quantile(cp, lots, m, rng, reps=10):
    sc, wt = [], []
    for L in lots.values():
        if L.ns < m:
            continue
        for _ in range(reps):
            sup = rng.choice(L.ns, m, replace=False)
            s = loo_scores(cp, L.smean[sup], L.rv)
            sc.append(s); wt.append(np.full(len(s), 1.0 / (reps * len(s))))
    return weighted_quantile(np.concatenate(sc), np.concatenate(wt), 1 - ALPHA)


def run_season(cps, qpast, lots, dates, m, n0s, rng_seed, n_draws, min_query=10):
    """Simulate n_draws runs of one season. cps: {'S': LotCP-S, 'A': LotCP-A}. Returns lot-level rows."""
    order = sorted(lots, key=lambda l: (dates[l], l))
    groups = []
    for l in order:
        if groups and dates[groups[-1][0]] == dates[l]:
            groups[-1].append(l)
        else:
            groups.append([l])
    acc = {}
    for e in range(n_draws):
        rng = np.random.default_rng([rng_seed, e])
        pool, pw = [], []
        pos = 0
        for g in groups:
            new_scores = []
            n = len(np.concatenate(pool)) if pool else 0
            rho = 1.0
            if n:
                rho = weighted_quantile(np.concatenate(pool), np.concatenate(pw), 1 - ALPHA) / qpast
            for l in g:
                L = lots[l]
                if L.ns < max(m, 2):
                    continue
                sup = rng.choice(L.ns, m, replace=False)
                new_scores.append(loo_scores(cps["S"], L.smean[sup], L.rv))
                if L.ns < m + min_query:
                    continue
                q = ~np.isin(L.inv, sup)
                w = 1.0 / ((L.ns - m) * L.cnt[L.inv][q])
                for key, cp in cps.items():
                    b, hw = cp.predict(L.smean[sup], L.rv)
                    variants = {f"{key}": hw}
                    for n0 in n0s:
                        f = 1.0 if (n == 0 or not np.isfinite(n0)) else np.exp(n / (n + n0) * np.log(rho))
                        variants[f"{key}_seq_n0={n0:g}"] = hw * f
                    e_ = L.r[q] - b
                    for name, h in variants.items():
                        cov = float(np.sum(w * (np.abs(e_) <= h)))
                        isc = float(np.sum(w * (2 * h + (2 / ALPHA) * np.maximum(np.abs(e_) - h, 0))))
                        acc.setdefault((l, name), []).append((cov, 2 * h, isc, pos, n))
            for s in new_scores:
                pool.append(s); pw.append(np.full(len(s), 1.0 / len(s)))
            pos += len(g)
    rows = []
    for (l, name), v in acc.items():
        v = np.array(v)
        rows.append(dict(lot=l, method=name, coverage=v[:, 0].mean(), width=v[:, 1].mean(), iscore=v[:, 2].mean(),
                         meets=float(np.mean(v[:, 0] >= 1 - ALPHA)), position=int(v[0, 3]), n_prior_scores=float(v[:, 4].mean())))
    return rows


def fit_cps(cfg, res, lot, smp, pred, m, seed):
    ev = cfg["eval"]
    kw = dict(m=m, alpha=ALPHA, n_episodes=ev["n_episodes"], min_query=ev["min_query_samples"], scale="full", seed=seed)
    return {"S": LotCP(**kw).fit(res, lot, smp, pred), "A": LotCP(**kw, assure=0.10).fit(res, lot, smp, pred)}


def one(model, target, m):
    cfg = load_config("full")
    d = load_data(cfg)
    dates = lot_dates(d)
    P = np.load(pred_path(cfg, model, 0, "forward", target))
    src, tgt = P["src_idx"], P["tgt_idx"]
    res_s, pred_s = d.y[src] - P["oof_season"], P["oof_season"]
    lot_s, smp_s, sea_s = d.lot[src], d.sample[src], d.season[src]
    # ---- tuning of n0 by replay inside the source seasons (pseudo-targets) ----
    tune = []
    for s in np.unique(sea_s):
        k = sea_s != s
        if len(np.unique(sea_s[k])) < 1:
            continue
        cps = fit_cps(cfg, res_s[k], lot_s[k], smp_s[k], pred_s[k], m, seed=7)
        cps = {"S": cps["S"]}
        lots_c = build(res_s[k], pred_s[k], lot_s[k], smp_s[k])
        qp = past_quantile(cps["S"], lots_c, m, np.random.default_rng([11, int(s), m]))
        lots_p = build(res_s[~k], pred_s[~k], lot_s[~k], smp_s[~k])
        rows = run_season(cps, qp, lots_p, dates, m, N0_GRID, rng_seed=int(s) * 7 + m, n_draws=5)
        df = pd.DataFrame(rows)
        for name, g in df.groupby("method"):
            tune.append(dict(model=model, target=target, m=m, pseudo_season=int(s), method=name, coverage=g.coverage.mean(), width=g.width.mean()))
    tune = pd.DataFrame(tune)
    agg = tune.groupby("method").agg(cov_err=("coverage", lambda c: np.mean(np.abs(c - 0.9))), width=("width", "mean")).reset_index()
    agg["n0"] = agg.method.str.extract(r"n0=(.*)$")[0]
    agg.loc[agg.method == "S", "n0"] = "inf_baseline"
    cand = agg[agg.method.str.startswith("S_seq")].sort_values(["cov_err", "width"])
    best = cand.n0.iloc[0]
    # ---- target season ----
    cps = fit_cps(cfg, res_s, lot_s, smp_s, pred_s, m, seed=cfg["eval"]["seed"] + m)
    lots_src = build(res_s, pred_s, lot_s, smp_s)
    qp = past_quantile(cps["S"], lots_src, m, np.random.default_rng([13, target, m]))
    lots_t = build(d.y[tgt] - P["pred_tgt"], P["pred_tgt"], d.lot[tgt], d.sample[tgt])
    rows = run_season(cps, qp, lots_t, dates, m, N0_GRID + (0.0,), rng_seed=target * 31 + m, n_draws=N_DRAWS)
    for r in rows:
        r.update(model=model, target=target, m=m, n0_selected=best)
    tune["n0_selected"] = best
    return rows, tune


if __name__ == "__main__":
    models = sys.argv[1:] or ["pls", "plspub"]
    jobs = [(mo, t, m) for mo in models for t in (2017, 2018, 2019, 2020, 2021) for m in (5, 10)]
    res = Parallel(n_jobs=4)(delayed(one)(*j) for j in jobs)
    od = out_dir(load_config("full"), "results/cycle4")
    lots = pd.DataFrame([r for x in res for r in x[0]])
    lots.to_csv(od / "seq_lots.csv", index=False)
    pd.concat([x[1] for x in res]).to_csv(od / "seq_n0.csv", index=False)
    print(lots.groupby(["model", "m"]).n0_selected.agg(lambda v: sorted(set(v))))
