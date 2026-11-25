"""plan_v5 analysis: LotCP-Seq with the n0 pre-selected on source seasons, against LotCP-S / LotCP-A; success rule of plan_v5."""
import numpy as np
import pandas as pd
from scipy.stats import t as tdist


def selected(d, key):
    name = d.n0_selected.map(lambda v: f"{key}_seq_n0={float(v):g}" if np.isfinite(float(v)) else key)
    x = d[d.method == name].copy()
    x["method"] = f"{key}_seq"
    return x


def main():
    d = pd.read_csv("results/cycle4/seq_lots.csv")
    base = d[d.method.isin(["S", "A", "S_seq_n0=0", "S_seq_n0=10", "S_seq_n0=30", "A_seq_n0=10", "A_seq_n0=30"])]
    d2 = pd.concat([base, selected(d, "S"), selected(d, "A")])
    rows = []
    for (mo, m, meth), g in d2.groupby(["model", "m", "method"]):
        s = g.groupby("target")[["coverage", "meets", "width", "iscore"]].mean()
        r = dict(model=mo, m=m, method=meth, n_lots=len(g), cov=g.coverage.mean(), cov_seasonmean=s.coverage.mean(),
                 cov_ex2017=g[g.target != 2017].coverage.mean(), seasons_cov90=int((s.coverage >= 0.9).sum()),
                 cov_min_season=s.coverage.min(), cov_max_season=s.coverage.max(),
                 meets=g.meets.mean(), meets_ex2017=g[g.target != 2017].meets.mean(), seasons_meets90=int((s.meets >= 0.9).sum()),
                 width=g.width.mean(), iscore=g.iscore.mean())
        for t, v in s.coverage.items():
            r[f"cov_{t}"] = v
        for t, v in s.meets.items():
            r[f"meets_{t}"] = v
        rows.append(r)
    summ = pd.DataFrame(rows)
    summ.to_csv("results/cycle4/seq_summary.csv", index=False)
    # paired season-level comparison and success rule
    tests = []
    for (mo, m), g in d2.groupby(["model", "m"]):
        for ref, oth, out in (("S_seq", "S", "coverage"), ("S_seq", "S", "iscore"), ("A_seq", "A", "meets"), ("A_seq", "A", "coverage"), ("S_seq", "S", "abs_err")):
            a = g[g.method == ref].set_index(["target", "lot"])
            b = g[g.method == oth].set_index(["target", "lot"])
            j = a.join(b, lsuffix="_r", rsuffix="_o", how="inner")
            if out == "abs_err":     # closeness of each season's coverage to 0.90 (season level)
                sr = j.groupby(level=0).coverage_r.mean(); so = j.groupby(level=0).coverage_o.mean()
                sm = (so - 0.9).abs() - (sr - 0.9).abs()
            else:
                sign = -1 if out == "iscore" else 1
                sm = (sign * (j[f"{out}_r"] - j[f"{out}_o"])).groupby(level=0).mean()
            se = sm.std(ddof=1) / np.sqrt(len(sm)); tq = tdist.ppf(0.975, len(sm) - 1)
            tests.append(dict(model=mo, m=m, reference=ref, comparator=oth, outcome=out, season_mean_diff=sm.mean(),
                              lo=sm.mean() - tq * se, hi=sm.mean() + tq * se, seasons_favouring=int((sm > 0).sum()),
                              **{f"d_{t}": v for t, v in sm.items()}))
    tests = pd.DataFrame(tests)
    tests.to_csv("results/cycle4/seq_tests.csv", index=False)
    s = summ.set_index(["model", "m", "method"])
    ok = []
    for mo in ("pls", "plspub"):
        for m in (5, 10):
            ex_up = s.loc[(mo, m, "S_seq"), "cov_ex2017"] > s.loc[(mo, m, "S"), "cov_ex2017"]
            t = tests[(tests.model == mo) & (tests.m == m) & (tests.reference == "S_seq") & (tests.outcome == "abs_err")].iloc[0]
            wid = s.loc[(mo, m, "S_seq"), "width"] / s.loc[(mo, m, "S"), "width"] - 1
            ok.append(dict(model=mo, m=m, ex2017_up=bool(ex_up), seasons_closer=int(t.seasons_favouring), width_change=wid,
                           success=bool(ex_up and t.seasons_favouring >= 4 and wid < 0.10)))
    ok = pd.DataFrame(ok)
    ok.to_csv("results/cycle4/seq_success.csv", index=False)
    cols = ["model", "m", "method", "cov", "cov_seasonmean", "cov_ex2017", "seasons_cov90", "cov_min_season", "cov_max_season",
            "meets", "meets_ex2017", "seasons_meets90", "width", "iscore"]
    print(summ[cols].round(3).to_string(index=False))
    print(tests.round(3).to_string(index=False))
    print(ok.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
