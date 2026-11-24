"""plan_v4 E3: share of lots meeting 0.90 coverage vs mean width — LotCP-S over α ∈ {0.05, 0.10, 0.20} vs LotCP-A (δ = 0.10, 0.20).

Descriptive (SNV PLS, forward, seed 0). Question: does LotCP-A reach its lot-level target at lower width than LotCP-S at
the α that reaches it? Estimand: share of lots whose coverage AVERAGED over reference draws is >= 0.90 (one definition for every method and α).
This differs from the per-draw 'meets' column of raw_results.csv, which is evaluated against each method's own 1 - α.
"""
import pandas as pd

d = pd.read_csv("results/raw_results.csv")
d = d[(d.model == "pls") & (d.protocol == "forward") & (d.seed == 0) & d.m.isin([3, 5, 10, 20])]
rows = []
for (meth, a, m), g in d[d.method.isin(["lotcp_s", "lotcp_a", "lotcp_a20"])].groupby(["method", "alpha", "m"]):
    cov90 = (g.coverage >= 0.90)
    s = g.assign(c90=cov90).groupby("target")[["c90", "width"]].mean()
    rows.append(dict(method=meth if meth != "lotcp_s" else f"lotcp_s_a{a:g}", alpha=a, m=m, share_ge_090=cov90.mean(),
                     share_ge_090_ex2017=cov90[g.target != 2017].mean(), seasons_ge_090=int((s.c90 >= 0.9).sum()),
                     width=g.width.mean(), width_ex2017=g.width[g.target != 2017].mean()))
out = pd.DataFrame(rows)
out = out[~((out.method.str.startswith("lotcp_a")) & (out.alpha != 0.1))]
out.to_csv("results/cycle3/assurance_frontier.csv", index=False)
print(out.round(3).to_string(index=False))
