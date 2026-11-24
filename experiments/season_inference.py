"""plan_v4 E1: season-level reporting and inference (review round 1, R1-C1/C2/C6).

Lots within a season share the season effect, so lot-level Wilcoxon tests overstate the evidence. Here every
headline comparison is reported (i) pooled over lots, (ii) as the average of season means, (iii) excluding 2017 (two
source seasons, over-covered) and (iv) excluding 2018 (used to design deviation D1), with
  * a two-stage season-cluster bootstrap CI (seasons resampled, then lots within each resampled season),
  * an exact sign test over the five season-mean differences (smallest attainable two-sided p = 0.0625),
  * a linear mixed model diff ~ 1 + (1 | season) on lot-level differences (REML; Wald CI of the intercept). With 4-5
    seasons the season variance is often estimated at the boundary; the mixed-model p is kept in the CSV but not used
    for claims (decision rule of plan_v4 E1 uses the cluster bootstrap).
Inputs: results/raw_results.csv (SNV PLS) and results/published_pls/published_pls.csv, α = 0.10, seed 0.
"""
import json
import warnings

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from src.utils import load_config, out_dir

B = 2000
NOM = 0.90
METHODS = ["scp_sample", "scp_season", "biascorr_naive", "target_only_centred", "lotcp", "lotcp_s", "lotcp_a",
           "biascorr_rep", "biascorr_full"]
# (reference, comparator, outcome, comparator at m=0?) ; outcome 'iscore' lower better, 'coverage' / 'meets' higher better
COMPARISONS = [("lotcp_s", "scp_sample", "coverage", True), ("lotcp_s", "scp_season", "coverage", True),
               ("lotcp_s", "biascorr_naive", "iscore", False), ("lotcp_s", "biascorr_naive", "coverage", False),
               ("lotcp_s", "target_only_centred", "iscore", False), ("lotcp_s", "biascorr_rep", "iscore", False),
               ("lotcp_s", "biascorr_rep", "coverage", False), ("lotcp_s", "biascorr_full", "iscore", False),
               ("lotcp_s", "biascorr_full", "coverage", False),
               ("lotcp_a", "biascorr_naive", "meets", False), ("lotcp_a", "target_only_centred", "meets", False),
               ("lotcp_a", "lotcp_s", "meets", False)]


def load():
    cfg = load_config("full")
    a = pd.read_csv("results/raw_results.csv")
    a = a[(a.model == "pls") & (a.protocol == "forward") & (a.alpha == 0.1) & (a.seed == 0)]
    b = pd.read_csv("results/published_pls/published_pls.csv")
    parts = [a, b]
    try:
        c = pd.read_csv("results/cycle3/matched_baseline.csv")
        c = c[c.method.isin(["biascorr_rep", "biascorr_full"])]
        parts.append(c)
    except FileNotFoundError:
        pass
    d = pd.concat(parts, ignore_index=True)
    d = d[d.alpha == 0.1].replace([np.inf, -np.inf], np.nan)
    return cfg, d


def season_boot(df, col, rng):
    """Two-stage cluster bootstrap of the lot-weighted mean of `col` (df has columns target, col)."""
    groups = [g[col].to_numpy() for _, g in df.groupby("target")]
    out = np.empty(B)
    for i in range(B):
        pick = rng.integers(0, len(groups), len(groups))
        vals = [groups[k][rng.integers(0, len(groups[k]), len(groups[k]))] for k in pick]
        out[i] = np.concatenate(vals).mean()
    return np.percentile(out, [2.5, 97.5])


def mixed(df):
    import statsmodels.formula.api as smf
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            r = smf.mixedlm("diff ~ 1", df, groups=df["target"]).fit(reml=True)
            lo, hi = r.conf_int().loc["Intercept"].tolist()
            return float(r.params["Intercept"]), float(lo), float(hi), float(r.pvalues["Intercept"])
        except Exception:
            return (np.nan,) * 4


def summary(d):
    rows = []
    for (model, meth, m), g in d[d.method.isin(METHODS)].groupby(["model", "method", "m"]):
        s = g.groupby("target")[["coverage", "meets", "width", "iscore"]].mean()
        row = dict(model=model, method=meth, m=m, n_lots=len(g))
        for k in ("coverage", "meets", "width", "iscore"):
            row[f"{k}_pooled"] = g[k].mean()
            row[f"{k}_season_avg"] = s[k].mean()
            row[f"{k}_ex2017"] = g.loc[g.target != 2017, k].mean()
            row[f"{k}_ex2018"] = g.loc[g.target != 2018, k].mean()
        row["seasons_meeting_assurance"] = int((s["meets"] >= NOM).sum())
        row["seasons_cov_ge_nominal"] = int((s["coverage"] >= NOM).sum())
        row["n_seasons"] = len(s)
        for t, v in s["coverage"].items():
            row[f"cov_{t}"] = v
        for t, v in s["meets"].items():
            row[f"meets_{t}"] = v
        rows.append(row)
    return pd.DataFrame(rows)


def tests(d, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for model in sorted(d.model.unique()):
        dm = d[d.model == model]
        for ref, oth, out, at0 in COMPARISONS:
            for m in (3, 5, 10, 20):
                a = dm[(dm.method == ref) & (dm.m == m)][["target", "lot", out]]
                b = dm[(dm.method == oth) & (dm.m == (0 if at0 else m))][["target", "lot", out]]
                j = a.merge(b, on=["target", "lot"], suffixes=("_r", "_o")).dropna()   # drops infinite (uninformative) intervals
                if len(j) < 10:
                    continue
                sign = -1.0 if out == "iscore" else 1.0          # positive diff = reference better
                j["diff"] = sign * (j[f"{out}_r"] - j[f"{out}_o"])
                for subset, jj in (("all", j), ("ex2017", j[j.target != 2017])):
                    smeans = jj.groupby("target")["diff"].mean()
                    k = int((smeans > 0).sum()); n = int((smeans != 0).sum())
                    lo, hi = season_boot(jj, "diff", rng)
                    est, mlo, mhi, mp = mixed(jj)
                    rows.append(dict(model=model, reference=ref, comparator=oth + ("@m0" if at0 else ""), outcome=out,
                                     m=m, subset=subset, n_lots=len(jj), n_seasons=len(smeans), mean_diff=jj["diff"].mean(),
                                     season_avg_diff=smeans.mean(), boot_lo=lo, boot_hi=hi,
                                     seasons_ref_better=k, sign_p=binomtest(k, n, 0.5).pvalue if n else np.nan,
                                     mixed_est=est, mixed_lo=mlo, mixed_hi=mhi, mixed_p=mp,
                                     boot_excludes_0=bool(lo > 0 or hi < 0)))
    t = pd.DataFrame(rows)
    return t


def main():
    cfg, d = load()
    od = out_dir(cfg, "results/cycle3")
    s = summary(d)
    s.to_csv(od / "season_summary.csv", index=False)
    t = tests(d)
    t.to_csv(od / "season_tests.csv", index=False)
    keep = t[(t.subset == "all")]
    json.dump(dict(n_tests=len(t), n_boot_excl0=int(t.boot_excludes_0.sum()),
                   n_boot_excl0_all=int(keep.boot_excludes_0.sum()), n_all=len(keep)), open(od / "season_tests_meta.json", "w"), indent=1)
    cols = ["model", "method", "m", "coverage_pooled", "coverage_season_avg", "coverage_ex2017", "coverage_ex2018",
            "meets_pooled", "meets_ex2017", "seasons_meeting_assurance", "seasons_cov_ge_nominal", "width_pooled"]
    print(s[s.m.isin([0, 5, 10, 20])][cols].round(3).to_string(index=False))
    print(t[["model", "reference", "comparator", "outcome", "m", "subset", "season_avg_diff", "boot_lo", "boot_hi",
             "seasons_ref_better", "sign_p", "mixed_p"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
