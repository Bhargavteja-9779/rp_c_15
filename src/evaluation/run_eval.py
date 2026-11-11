"""Stage 3: evaluate every interval method on every target lot.

For each (model, seed, protocol, target season, alpha) the script
  * calibrates all methods on source-season information only,
  * for each target lot and each number m of reference samples draws R random reference sets,
  * records lot-level coverage, width, interval score and point-prediction error.
Output: one CSV row per (model, seed, protocol, target, alpha, lot, method, m).
"""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

from src.data.dataset import load_data
from src.evaluation.conformal import (aci_alpha, density_ratio_weights, gaussian_halfwidth, hier_weights,
                                      interval_score, sample_weights, split_quantile, weighted_cp_halfwidths,
                                      weighted_quantile)
from src.evaluation.lotcp import LotCP, replicate_variance
from src.training.crossfit import pred_path
from src.training.uq_models import QRF_LEVELS, uq_path
from src.utils import get_logger, out_dir

# LotCP variants: name -> (residual scheme, constructor overrides).  'lotcp' is the full method.
LOTCP_VARIANTS = {
    "lotcp": ("season", {}),
    "lotcp_noshrink": ("season", {"shrink": False}),
    "lotcp_noepisodic": ("season", {"episodic": False}),
    "lotcp_lotfold": ("lot", {}),
    "lotcp_samplefold": ("sample", {}),
    "lotcp_pooled": ("season", {"lot_balanced": False}),
    "lotcp_s": ("season", {"scale": "full"}),               # LotCP-S: + lot-specific scale
    "lotcp_s_support": ("season", {"scale": "support"}),    # scale from reference samples only
    "lotcp_s_rep": ("season", {"scale": "rep"}),            # scale from replicate scans only
}


def _lot_struct(r, sample):
    """Per-lot cache: sample index per spectrum, per-sample mean residual and query weights."""
    _, inv, cnt = np.unique(sample, return_inverse=True, return_counts=True)
    return inv, np.bincount(inv, weights=r) / cnt, cnt


def _metrics(r, b, q, w, alpha, margin):
    """r: residuals of query spectra; interval = [yhat + b - q, yhat + b + q]; w sums to 1."""
    e = r - b
    cov = float(np.sum(w * (np.abs(e) <= q)))
    isc = float(np.sum(w * (2 * q + (2 / alpha) * np.maximum(np.abs(e) - q, 0))))
    return cov, 2 * q, isc


def evaluate(cfg, model, seed, protocol, target, alpha, variants=None, m_grid=None, label_noise_sd=0.0,
             keep_mask=None, lot_filter=None, n_draws=None, cal_lots_k=None, cal_rep=0, baselines=True):
    """Return (interval rows, point rows, calibration info) for one configuration."""
    ev = cfg["eval"]
    d = load_data(cfg)
    P = np.load(pred_path(cfg, model, seed, protocol, target))
    src, tgt = P["src_idx"], P["tgt_idx"]
    y_s, y_t = d.y[src], d.y[tgt]
    lot_s, smp_s = d.lot[src], d.sample[src]
    lot_t, smp_t = d.lot[tgt], d.sample[tgt]
    r_t = y_t - P["pred_tgt"]
    res = {s: y_s - P[f"oof_{s}"] for s in ("sample", "lot", "season") if f"oof_{s}" in P.files}
    ks, kt = np.ones(len(src), bool), np.ones(len(tgt), bool)
    if keep_mask is not None:                       # sensitivity analyses on row subsets
        ks, kt = keep_mask[src], keep_mask[tgt]
    variants = LOTCP_VARIANTS if variants is None else variants
    m_grid = ev["m_grid"] if m_grid is None else m_grid
    n_draws = ev["n_draws"] if n_draws is None else n_draws
    rng = np.random.default_rng([ev["seed"], target if isinstance(target, (int, np.integer)) else sum(map(ord, str(target))), seed, int(alpha * 1000)])
    z = norm.ppf(1 - alpha / 2)
    info = {}

    # ---------------- calibration on source information only --------------------------------
    q0 = {}
    if "sample" in res:
        q0["gauss"] = gaussian_halfwidth(res["sample"][ks], alpha)
        q0["scp_sample"] = split_quantile(np.abs(res["sample"][ks]), alpha)
        cal_sorted = np.sort(np.abs(res["sample"][ks]))
    if "lot" in res:
        q0["scp_lot"] = split_quantile(np.abs(res["lot"][ks]), alpha)
    q0["scp_season"] = split_quantile(np.abs(res["season"][ks]), alpha)
    kl = ks.copy()                                   # rows available to LotCP calibration
    if cal_lots_k is not None:                        # sensitivity: only k random past lots
        lots_u = np.unique(lot_s[ks])
        pick = np.random.default_rng([cal_rep, target if isinstance(target, int) else 0]).choice(lots_u, min(cal_lots_k, len(lots_u)), replace=False)
        kl = ks & np.isin(lot_s, pick)
    lotcp = {}
    for name, (scheme, kw) in variants.items():
        if scheme not in res:
            continue
        for m in m_grid:
            cp = LotCP(m=m, alpha=alpha, n_episodes=ev["n_episodes"], min_query=ev["min_query_samples"],
                       seed=ev["seed"] + m, **kw).fit(res[scheme][kl], lot_s[kl], smp_s[kl], P[f"oof_{scheme}"][kl])
            lotcp[(name, m)] = cp
            if name == "lotcp":
                info[f"m{m}"] = dict(cp.info)
    full_models = baselines and model == "pls" and seed == 0 and protocol == "forward" and keep_mask is None and label_noise_sd == 0
    U = np.load(uq_path(cfg, protocol, target)) if full_models and uq_path(cfg, protocol, target).exists() else None
    Zs = np.load(out_dir(cfg, "data/processed") / f"plsscores_{protocol}_{target}.npz") if full_models else None

    rows, prow = [], []
    key = dict(model=model, seed=seed, protocol=protocol, target=target, alpha=alpha)
    for lot in np.unique(lot_t[kt]):
        if lot_filter is not None and lot not in lot_filter:
            continue
        li = np.flatnonzero((lot_t == lot) & kt)
        r, smp = r_t[li], smp_t[li]
        inv, smean, scnt = _lot_struct(r, smp)
        rep_var = replicate_variance(P["pred_tgt"][li], inv)
        n_s = len(smean)
        if n_s < ev["min_lot_samples"]:
            continue
        w_all = 1.0 / (n_s * scnt[inv])

        def add(method, m, cov, width, isc, under, **extra):
            rows.append(dict(key, lot=int(lot), n_samples=n_s, method=method, m=m, coverage=cov, width=width,
                             iscore=isc, under=under, **extra))

        # ---- m = 0 methods with constant half-width ----------------------------------------
        for name, q in q0.items():
            c, wd, isc = _metrics(r, 0.0, q, w_all, alpha, ev["undercover_margin"])
            add(name, 0, c, wd, isc, float(c < 1 - alpha - ev["undercover_margin"]))
        # ---- m = 0 methods with per-spectrum intervals (primary model only) ----------------
        if Zs is not None and "sample" in res:
            ws, wt = density_ratio_weights(Zs["src"], Zs["tgt"][li])
            hw = weighted_cp_halfwidths(np.abs(res["sample"]), ws, wt, alpha)
            cov = np.sum(w_all * (np.abs(r) <= hw))
            fin = np.isfinite(hw)
            hw_f = np.where(fin, hw, np.nanmax(np.where(fin, hw, np.nan)) if fin.any() else np.nan)
            isc = np.sum(w_all * interval_score(-hw_f, hw_f, r, alpha))
            add("wcp", 0, float(cov), float(np.sum(w_all * 2 * hw_f)), float(isc),
                float(cov < 1 - alpha - ev["undercover_margin"]), frac_infinite=float(1 - fin.mean()))
        if U is not None:
            y = y_t[li]
            ivs = {}
            if abs(alpha - 0.1) < 1e-9:
                for scheme in ("sample", "season"):
                    conf = np.maximum(U[f"cqr_lo_oof_{scheme}"] - y_s, y_s - U[f"cqr_hi_oof_{scheme}"])
                    qc = split_quantile(conf, alpha)
                    ivs[f"cqr_{scheme}"] = (U["cqr_lo_tgt"][li] - qc, U["cqr_hi_tgt"][li] + qc)
            lv = list(QRF_LEVELS)
            ivs["qrf"] = (U["qrf_q"][li, lv.index(alpha / 2)], U["qrf_q"][li, lv.index(1 - alpha / 2)])
            sd = np.sqrt(U["ens_var"][li])
            ivs["ensemble"] = (U["ens_mean"][li] - z * sd, U["ens_mean"][li] + z * sd)
            sd = np.sqrt(U["mcd_var"][li])
            ivs["mc_dropout"] = (U["mcd_mean"][li] - z * sd, U["mcd_mean"][li] + z * sd)
            for name, (lo, hi) in ivs.items():
                cov = float(np.sum(w_all * ((y >= lo) & (y <= hi))))
                add(name, 0, cov, float(np.sum(w_all * (hi - lo))), float(np.sum(w_all * interval_score(lo, hi, y, alpha))),
                    float(cov < 1 - alpha - ev["undercover_margin"]))
        # ---- methods that use m reference samples -------------------------------------------
        for m in m_grid:
            if n_s < m + ev["min_query_samples"]:
                continue
            nd = 1 if m == 0 else n_draws
            acc = {}
            pt = np.zeros((nd, 3, 2))                  # [draw, correction, (sq err, abs bias)]
            for dr in range(nd):
                sup = rng.choice(n_s, m, replace=False)
                qmask = np.ones(n_s, bool); qmask[sup] = False
                rowq = qmask[inv]
                rq = r[rowq]
                wq = 1.0 / (qmask.sum() * scnt[inv][rowq])
                eps = rng.normal(0, label_noise_sd, m) if label_noise_sd > 0 else np.zeros(m)
                sup_means = smean[sup] + eps                 # (noisy) per-sample mean residuals
                cand = {}
                for name in variants:
                    if (name, m) in lotcp:
                        cand[name] = lotcp[(name, m)].predict(sup_means, rep_var)
                if m > 0 and "sample" in res and baselines:
                    pos = np.full(n_s, -1); pos[sup] = np.arange(m)
                    rows_sup = ~rowq
                    p_sup = pos[inv[rows_sup]]                # support-sample position of each support spectrum
                    r_sup = r[rows_sup] + eps[p_sup]
                    w_sup = 1.0 / scnt[inv][rows_sup]         # every reference sample has unit mass
                    bm = float(np.mean(sup_means))
                    # (a) chemometric practice: mean bias correction, half-width from in-season CV residuals
                    cand["biascorr_naive"] = (bm, q0["scp_sample"])
                    # (b) target-only split conformal on the reference samples
                    cand["target_only"] = (0.0, weighted_quantile(np.abs(r_sup), w_sup, 1 - alpha, inf_mass=1.0))
                    # (c) target-only, bias-corrected: leave-one-sample-out centred reference scores
                    if m >= 2:
                        loo_mean = (sup_means.sum() - sup_means) / (m - 1)
                        cand["target_only_centred"] = (bm, weighted_quantile(np.abs(r_sup - loo_mean[p_sup]), w_sup, 1 - alpha, inf_mass=1.0))
                    # (d) pooling the reference residuals into the source calibration set
                    cand["pooled"] = (0.0, split_quantile(np.r_[np.abs(res["sample"][ks]), np.abs(r_sup)], alpha))
                    # (e) adaptive conformal inference run over the reference samples
                    cand["aci"] = (0.0, aci_alpha(cal_sorted, [np.abs(r_sup[p_sup == j]) for j in range(m)], alpha))
                for name, (b, q) in cand.items():
                    if np.isfinite(q):
                        c, wd, isc = _metrics(rq, b, q, wq, alpha, ev["undercover_margin"])
                    else:
                        c, wd, isc = 1.0, np.inf, np.inf
                    acc.setdefault(name, []).append((c, wd, isc))
                # point prediction after bias correction: none / plain mean / shrinkage
                bs = [0.0, float(np.mean(sup_means)) if m > 0 else 0.0,
                      lotcp[("lotcp", m)].predict(sup_means)[0] if ("lotcp", m) in lotcp else 0.0]
                for j, b in enumerate(bs):
                    e = rq - b
                    pt[dr, j] = (np.sum(wq * e ** 2), abs(np.sum(wq * e)))
            for name, v in acc.items():
                v = np.array(v)
                fin = np.isfinite(v[:, 1])
                add(name, m, float(v[:, 0].mean()), float(v[fin, 1].mean()) if fin.any() else np.inf,
                    float(v[fin, 2].mean()) if fin.any() else np.inf,
                    float(np.mean(v[:, 0] < 1 - alpha - ev["undercover_margin"])),
                    cov_sd=float(v[:, 0].std()), frac_infinite=float(1 - fin.mean()))
            for j, corr in enumerate(("none", "mean", "shrinkage")):
                prow.append(dict(key, lot=int(lot), n_samples=n_s, m=m, correction=corr,
                                 mse=float(pt[:, j, 0].mean()), abs_bias=float(pt[:, j, 1].mean())))
    return rows, prow, info


def configurations(cfg):
    """All (model, seed, protocol, target, alpha) combinations of the main study."""
    out = []
    for protocol in ("forward", "loso"):
        for target in cfg["protocols"][protocol]["targets"]:
            models = [("pls", 0)]
            if protocol == "forward":
                models += [("gbm", s) for s in cfg["models"]["gbm"]["seeds"]] + [("cnn", s) for s in cfg["models"]["cnn"]["seeds"]]
            else:
                models += [("cnn", cfg["models"]["cnn"]["seeds"][0])]
            for model, seed in models:
                alphas = cfg["eval"]["alphas"] if (model == "pls") else [cfg["eval"]["primary_alpha"]]
                for alpha in alphas:
                    out.append((model, seed, protocol, target, alpha))
    return out


def _one(cfg, c):
    full = c[0] == "pls" and c[2] == "forward"
    variants = None if full else {k: LOTCP_VARIANTS[k] for k in ("lotcp", "lotcp_s")}
    rows, prow, info = evaluate(cfg, *c, variants=variants)
    return rows, prow, dict(model=c[0], seed=c[1], protocol=c[2], target=c[3], alpha=c[4], calib=info)


def run(cfg, n_jobs: int = 4):
    from joblib import Parallel, delayed

    from src.utils import save_json

    log = get_logger("eval", cfg)
    t = time.time()
    confs = [c for c in configurations(cfg) if pred_path(cfg, c[0], c[1], c[2], c[3]).exists()]
    missing = len(configurations(cfg)) - len(confs)
    if missing:
        log.warning("%d configurations skipped because predictions are missing", missing)
    res = Parallel(n_jobs=n_jobs)(delayed(_one)(cfg, c) for c in confs)
    rdir = out_dir(cfg, "results")
    pd.DataFrame([r for x in res for r in x[0]]).to_csv(rdir / "raw_results.csv", index=False)
    pd.DataFrame([r for x in res for r in x[1]]).to_csv(rdir / "point_results.csv", index=False)
    save_json([x[2] for x in res], rdir / "calibration_info.json")
    log.info("evaluation finished: %d configurations in %.0f s", len(confs), time.time() - t)


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
