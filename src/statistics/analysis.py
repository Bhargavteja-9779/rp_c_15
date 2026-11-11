"""Stage 4: statistics and machine-generated tables. Nothing in tables/ is typed by hand."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

from src.data.dataset import load_data
from src.training.crossfit import pred_path
from src.utils import get_logger, out_dir, save_json

LABEL = {
    "gauss": "Gaussian ±z·RMSECV", "scp_sample": "Split CP (sample folds)", "scp_lot": "Split CP (lot folds)",
    "scp_season": "Split CP (season folds)", "wcp": "Weighted CP (covariate shift)", "cqr_sample": "CQR (sample folds)",
    "cqr_season": "CQR (season folds)", "qrf": "Quantile regression forest", "ensemble": "Deep ensemble",
    "mc_dropout": "MC dropout", "target_only": "Target-only CP", "target_only_centred": "Target-only CP, centred",
    "biascorr_naive": "Bias corr. + source CP", "pooled": "Pooled recalibration", "aci": "ACI on references",
    "lotcp": "LotCP", "lotcp_s": "LotCP-S", "lotcp_noshrink": "HCP-mean (LotCP w/o shrinkage)",
    "lotcp_noepisodic": "LotCP w/o episodic quantile", "lotcp_lotfold": "LotCP, lot-fold residuals",
    "lotcp_samplefold": "LotCP, sample-fold residuals", "lotcp_pooled": "LotCP, spectrum-pooled weights",
    "lotcp_s_support": "LotCP-S, reference scale only", "lotcp_s_lotfold": "LotCP-S, lot-fold residuals", "lotcp_s_rep": "LotCP-S, replicate scale only",
}
M0 = ["gauss", "scp_sample", "scp_lot", "scp_season", "wcp", "cqr_sample", "cqr_season", "qrf", "ensemble", "mc_dropout", "lotcp", "lotcp_s"]
MK = ["biascorr_naive", "pooled", "aci", "target_only", "target_only_centred", "lotcp_noshrink", "lotcp", "lotcp_s"]
ABL = ["lotcp_s", "lotcp_s_support", "lotcp_s_rep", "lotcp_s_lotfold", "lotcp", "lotcp_noshrink", "lotcp_noepisodic", "lotcp_lotfold", "lotcp_samplefold", "lotcp_pooled"]


def seed_average(df):
    """Average stochastic-model seeds within lot so that the lot stays the unit of analysis."""
    keys = ["model", "protocol", "target", "alpha", "lot", "method", "m"]
    num = ["coverage", "width", "iscore", "under", "n_samples", "frac_infinite"]
    d = df.copy()
    d[["width", "iscore"]] = d[["width", "iscore"]].replace(np.inf, np.nan)
    return d.groupby(keys, as_index=False)[num].mean()


def boot_ci(values, strata, n_boot, seed, fn=np.mean):
    """Percentile CI from a bootstrap that resamples lots within season (stratum)."""
    rng = np.random.default_rng(seed)
    values, strata = np.asarray(values, float), np.asarray(strata)
    idx_by = [np.flatnonzero(strata == s) for s in np.unique(strata)]
    stats = np.empty(n_boot)
    for b in range(n_boot):
        idx = np.concatenate([rng.choice(i, len(i)) for i in idx_by])
        stats[b] = fn(values[idx])
    return np.nanpercentile(stats, [2.5, 97.5])


def summarise(d, cfg, methods=None):
    """One row per (method, m): lot-macro metrics with bootstrap CI of coverage."""
    rows = []
    for (method, m), g in d.groupby(["method", "m"]):
        if methods is not None and method not in methods:
            continue
        lo, hi = boot_ci(g["coverage"], g["target"], cfg["stats"]["n_boot"], cfg["stats"]["seed"])
        fin = g["width"].notna()
        rows.append(dict(method=method, label=LABEL.get(method, method), m=m, n_lots=len(g), coverage=g["coverage"].mean(),
                         cov_lo=lo, cov_hi=hi, under=g["under"].mean(),
                         width=g.loc[fin, "width"].mean() if fin.any() else np.nan,
                         iscore=g.loc[fin, "iscore"].mean() if fin.any() else np.nan,
                         frac_infinite=g["frac_infinite"].fillna(0).mean()))
    return pd.DataFrame(rows)


def holm(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    adj = np.empty(len(p))
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (len(p) - rank) * p[i])
        adj[i] = min(run, 1.0)
    return adj


def rank_biserial(diff):
    """Matched-pairs rank-biserial correlation (Kerby, 2014): (R+ - R-) / (R+ + R-)."""
    diff = diff[diff != 0]
    if len(diff) == 0:
        return 0.0
    ranks = pd.Series(np.abs(diff)).rank().to_numpy()
    return float((ranks[diff > 0].sum() - ranks[diff < 0].sum()) / ranks.sum())


def paired_tests(d, cfg, ref="lotcp_s", alpha_nom=0.1):
    """Wilcoxon signed-rank tests (unit = target lot) of `ref` against every other method at equal m.

    Two outcomes: interval score (lower is better) and |coverage - nominal| (lower is better).
    Holm correction is applied within each outcome family."""
    rows = []
    piv = {k: d.pivot_table(index=["target", "lot", "m"], columns="method", values=k) for k in ("iscore", "coverage")}
    for m in sorted(d["m"].unique()):
        for other in [c for c in piv["iscore"].columns if c != ref]:
            for outcome in ("iscore", "abs_cov_err"):
                if outcome == "iscore":
                    tab = piv["iscore"].xs(m, level="m")[[ref, other]] if other in piv["iscore"] else None
                else:
                    tab = (piv["coverage"].xs(m, level="m")[[ref, other]] - (1 - alpha_nom)).abs()
                tab = tab.dropna()
                if len(tab) < 10:
                    continue
                diff = (tab[ref] - tab[other]).to_numpy()
                try:
                    p = wilcoxon(diff, zero_method="wilcox", alternative="two-sided").pvalue
                except ValueError:
                    p = 1.0
                seasons = tab.index.get_level_values("target")
                lo, hi = boot_ci(diff, seasons, cfg["stats"]["n_boot"], cfg["stats"]["seed"])
                per_season = pd.Series(diff).groupby(np.asarray(seasons)).mean()
                rows.append(dict(m=m, reference=ref, other=other, outcome=outcome, n_lots=len(tab), mean_diff=diff.mean(),
                                 median_diff=float(np.median(diff)), ci_lo=lo, ci_hi=hi, p=p, rank_biserial=rank_biserial(diff),
                                 seasons_ref_better=int((per_season < 0).sum()), n_seasons=len(per_season)))
    t = pd.DataFrame(rows)
    if len(t):
        t["p_holm"] = np.nan
        for outcome, g in t.groupby("outcome"):
            t.loc[g.index, "p_holm"] = holm(g["p"].to_numpy())
    return t


def point_table(cfg):
    """Accuracy of the point predictors on each target season (spectrum level) and the lot-bias spread."""
    d = load_data(cfg)
    rows = []
    for target in cfg["protocols"]["forward"]["targets"]:
        for model in ("pls", "gbm", "cnn"):
            seeds = [0] if model == "pls" else cfg["models"][model]["seeds"]
            for seed in seeds:
                p = pred_path(cfg, model, seed, "forward", target)
                if not p.exists():
                    continue
                P = np.load(p)
                y, yh = d.y[P["tgt_idx"]], P["pred_tgt"]
                r = y - yh
                lot_bias = pd.Series(r).groupby(d.lot[P["tgt_idx"]]).mean()
                ys = d.y[P["src_idx"]]
                info = json.load(open(p.with_suffix(".json")))
                rows.append(dict(target=target, model=model, seed=seed, n_spectra=len(y), rmse=np.sqrt(np.mean(r ** 2)), bias=r.mean(),
                                 r2=1 - np.sum(r ** 2) / np.sum((y - y.mean()) ** 2), sd_lot_bias=lot_bias.std(),
                                 rmse_cv_sample=np.sqrt(np.mean((ys - P["oof_sample"]) ** 2)),
                                 rmse_cv_lot=np.sqrt(np.mean((ys - P["oof_lot"]) ** 2)) if "oof_lot" in P.files else np.nan,
                                 rmse_cv_season=np.sqrt(np.mean((ys - P["oof_season"]) ** 2)),
                                 fit_seconds=info["fit_seconds_final"], predict_ms_per_1000=info["predict_seconds_per_1000"] * 1000,
                                 n_params=info.get("n_params", np.nan), n_components=info.get("n_components", np.nan)))
    return pd.DataFrame(rows)


def dataset_table(cfg):
    m = load_data(cfg).meta
    g = m.groupby("season")
    t = g.agg(spectra=("dry_matter", "size"), samples=("reference_no", "nunique"), lots=("population", "nunique"),
              cultivars=("cultivar", "nunique"), instruments=("instrument", "nunique"),
              dm_mean=("dry_matter", "mean"), dm_sd=("dry_matter", "std")).reset_index()
    per_lot = m.groupby(["season", "population"])["reference_no"].nunique().groupby("season").median()
    t["median_samples_per_lot"] = per_lot.to_numpy()
    tot = dict(season="All", spectra=len(m), samples=m["reference_no"].nunique(), lots=m["population"].nunique(),
               cultivars=m["cultivar"].nunique(), instruments=m["instrument"].nunique(), dm_mean=m["dry_matter"].mean(),
               dm_sd=m["dry_matter"].std(), median_samples_per_lot=m.groupby("population")["reference_no"].nunique().median())
    return pd.concat([t, pd.DataFrame([tot])], ignore_index=True)


def _md(df, path, floatfmt="%.3f"):
    path.with_suffix(".csv").write_text(df.to_csv(index=False, float_format=floatfmt))
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join((floatfmt % v) if isinstance(v, (float, np.floating)) else str(v) for v in r) + " |")
    path.with_suffix(".md").write_text("\n".join(lines) + "\n")


def run(cfg):
    log = get_logger("analysis", cfg)
    rdir, tdir = out_dir(cfg, "results"), out_dir(cfg, "tables")
    raw = pd.read_csv(rdir / "raw_results.csv")
    d = seed_average(raw)
    a0 = cfg["eval"]["primary_alpha"]
    main = d[(d.model == "pls") & (d.protocol == "forward") & np.isclose(d.alpha, a0)]
    metrics, stats = {}, {}

    _md(dataset_table(cfg), tdir / "table1_dataset")
    pt = point_table(cfg)
    _md(pt, tdir / "table2_point_models_by_seed")
    pt_avg = pt.groupby(["target", "model"], as_index=False)[["rmse", "bias", "r2", "sd_lot_bias", "rmse_cv_sample", "rmse_cv_lot", "rmse_cv_season"]].mean()
    _md(pt_avg, tdir / "table2_point_models")

    s_main = summarise(main, cfg, set(M0) | set(MK))
    order = {k: i for i, k in enumerate(M0 + [x for x in MK if x not in M0])}
    s_main = s_main.sort_values(["m", "method"], key=lambda c: c.map(order) if c.name == "method" else c).reset_index(drop=True)
    _md(s_main, tdir / "table3_main_intervals")
    per_season = main[main.method.isin(["scp_sample", "scp_lot", "scp_season", "lotcp", "lotcp_s", "target_only_centred", "biascorr_naive"])] \
        .groupby(["method", "m", "target"])[["coverage", "width", "iscore"]].mean().reset_index()
    _md(per_season, tdir / "table4_per_season")
    _md(summarise(main, cfg, set(ABL)), tdir / "table5_ablation")
    tests = paired_tests(main, cfg, alpha_nom=a0)
    _md(tests, tdir / "table6_tests", floatfmt="%.4g")

    # generalisation: other predictors (forward) and the leave-one-season-out protocol
    gen = []
    for (model, protocol), g in d[np.isclose(d.alpha, a0)].groupby(["model", "protocol"]):
        s = summarise(g, cfg, {"scp_sample", "scp_season", "lotcp", "lotcp_s", "target_only_centred", "biascorr_naive"})
        s.insert(0, "protocol", protocol); s.insert(0, "model", model)
        gen.append(s)
    gen = pd.concat(gen, ignore_index=True)
    _md(gen, tdir / "table7_generalisation")
    # seed-to-seed spread of lot-macro metrics for stochastic predictors
    sd_rows = []
    r0 = raw[np.isclose(raw.alpha, a0) & (raw.protocol == "forward") & raw.model.isin(["gbm", "cnn"])].replace(np.inf, np.nan)
    for (model, method, m), g in r0.groupby(["model", "method", "m"]):
        per_seed = g.groupby("seed")[["coverage", "width", "iscore"]].mean()
        sd_rows.append(dict(model=model, method=method, m=m, n_seeds=len(per_seed), **{f"{k}_mean": per_seed[k].mean() for k in per_seed},
                            **{f"{k}_sd": per_seed[k].std() for k in per_seed}))
    _md(pd.DataFrame(sd_rows), tdir / "table7b_seed_spread")
    # other nominal levels
    al = []
    for alpha, g in d[(d.model == "pls") & (d.protocol == "forward")].groupby("alpha"):
        s = summarise(g, cfg, {"scp_sample", "scp_season", "lotcp", "lotcp_s", "target_only_centred"})
        s.insert(0, "nominal", 1 - alpha)
        al.append(s)
    _md(pd.concat(al, ignore_index=True), tdir / "table8_alpha")
    # point prediction after bias correction
    pr = pd.read_csv(rdir / "point_results.csv")
    pr = pr[(pr.model == "pls") & (pr.protocol == "forward") & np.isclose(pr.alpha, a0)]
    pc = pr.groupby(["m", "correction"]).agg(rmse=("mse", lambda x: float(np.sqrt(x).mean())), abs_bias=("abs_bias", "mean"), n_lots=("lot", "size")).reset_index()
    _md(pc, tdir / "table9_point_correction")

    # ------------- headline numbers for the manuscript ---------------------------------------
    def get(method, m, col, table=s_main):
        r = table[(table.method == method) & (table.m == m)]
        return float(r[col].iloc[0]) if len(r) else None

    for method in set(M0) | set(MK) | set(ABL):
        src = summarise(main, cfg, {method})
        for _, r in src.iterrows():
            metrics[f"{method}|m{int(r.m)}"] = {k: r[k] for k in ("n_lots", "coverage", "cov_lo", "cov_hi", "under", "width", "iscore", "frac_infinite")}
    metrics["_meta"] = dict(primary_alpha=a0, n_target_lots=int(main[main.m == 0].lot.nunique()),
                            n_target_seasons=int(main.target.nunique()))
    stats["paired_tests"] = tests.to_dict(orient="records")
    save_json(metrics, rdir / "metrics.json")
    save_json(stats, rdir / "statistics.json")
    log.info("analysis finished: %d summary rows, %d tests", len(s_main), len(tests))


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
