"""Tables for the harvest-decision simulator, the assumed-cost economic analysis and the planner.

ASSUMED COSTS (not measured; all in units of the value V of one marketable fruit):
  c_I = 1     cost of accepting an immature fruit (lost value / downgrade)
  c_D in {1/19, 1/9, 1/4, 1/2}  cost of withholding a mature fruit (delay, re-scan, quality loss)
  c_R = 1.5   cost of one destructive reference test (the fruit itself plus laboratory effort 0.5 V)
  N   in {200, 1000, 5000}      fruit per lot over which reference tests are spread
For a calibrated lower bound the decision-theoretic level is alpha* = c_D / (c_I + c_D), i.e.
0.05, 0.10, 0.20 and 1/3 for the four c_D values.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

C_I, C_R = 1.0, 1.5
C_D = {0.05: 1 / 19, 0.1: 1 / 9, 0.2: 0.25, 1 / 3: 0.5}
LOT_SIZES = (200, 1000, 5000)


def fruit_summary(rdir):
    f = pd.read_csv(rdir / "harvest" / "fruit_by_lot.csv.gz")
    f["bad_lot"] = (f.false_accept / f.accepted.where(f.accepted > 0)) > 0.10
    s = f.groupby(["model", "rule", "alpha", "threshold", "m"]).agg(
        lots=("lot", "size"), accepted=("accepted", "mean"), compliant=("compliant", "mean"),
        false_accept=("false_accept", "mean"), false_withhold=("false_withhold", "mean"),
        lots_over_10pct=("bad_lot", "mean")).reset_index()
    s["immature_among_accepted"] = s.false_accept / s.accepted
    s["compliant_accepted"] = (s.accepted - s.false_accept) / s.compliant
    return s


def economics(s):
    rows = []
    for (model, t), z in s.groupby(["model", "threshold"]):
        comp = float(z[z.rule == "point"].compliant.iloc[0])
        for a, cd in C_D.items():
            for N in LOT_SIZES:
                def cost(r):
                    return float(r.false_accept + cd * r.false_withhold + r.m * C_R / N)

                base = dict(model=model, threshold=t, alpha_star=a, c_D=cd, lot_size=N)
                rows.append(dict(base, rule="accept_all", m=0, cost=1 - comp))
                rows.append(dict(base, rule="accept_none", m=0, cost=cd * comp))
                for _, r in z.iterrows():
                    if r.rule in ("point", "point_bc") or np.isclose(r.alpha, a):
                        rows.append(dict(base, rule=r.rule, m=int(r.m), cost=cost(r)))
    e = pd.DataFrame(rows)
    # regret of using alpha* instead of the best grid level in hindsight (no reference cost: it is alpha-independent)
    reg = []
    for (model, t, rule, m), z in s[s.rule.isin(["scp_lower", "bc_lower", "lotcp_s_lower"])].groupby(["model", "threshold", "rule", "m"]):
        for a, cd in C_D.items():
            c = z.false_accept + cd * z.false_withhold
            at = float(c[np.isclose(z.alpha, a)].iloc[0])
            reg.append(dict(model=model, threshold=t, rule=rule, m=m, alpha_star=a, cost_at_alpha_star=at, best_cost=float(c.min()),
                            rel_regret=(at - float(c.min())) / float(c.min()), best_alpha=float(z.alpha[c.idxmin()])))
    return e, pd.DataFrame(reg)


def lot_summary(rdir):
    l = pd.read_csv(rdir / "harvest" / "lot_decisions.csv.gz")
    g = l.groupby(["model", "rule", "alpha", "threshold", "p", "m", "target", "lot"]).agg(h=("harvest", "mean"), ready=("ready", "mean")).reset_index()
    g["ready_lot"] = g.ready >= 0.5
    out = []
    for k, z in g.groupby(["model", "rule", "alpha", "threshold", "p", "m"]):
        nr, rd = z[~z.ready_lot], z[z.ready_lot]
        out.append(dict(zip(["model", "rule", "alpha", "threshold", "p", "m"], k), lots=len(z), ready_lots=len(rd), not_ready_lots=len(nr),
                        premature=float(nr.h.mean()) if len(nr) else np.nan, delayed=float(1 - rd.h.mean()) if len(rd) else np.nan))
    return pd.DataFrame(out)


def planner_table(rdir, main_summary):
    p = pd.read_csv(rdir / "robustness" / "planning.csv")
    p = p[p.model == "pls"]
    t = p.groupby(["method", "m"]).agg(planned_width=("planned_width", "mean"), realised_width=("realised_width", "mean")).reset_index()
    t = t.pivot(index="m", columns="method", values=["planned_width", "realised_width"])
    t.columns = [f"{a}_{b}" for a, b in t.columns]
    t = t.reset_index()
    ms = main_summary.set_index(["method", "m"])
    t["lots_reaching_090_lotcp_s"] = [float(ms.loc[("lotcp_s", m), "meets"]) if ("lotcp_s", m) in ms.index else np.nan for m in t.m]
    t["lots_reaching_090_lotcp_a"] = [float(ms.loc[("lotcp_a", m), "meets"]) if ("lotcp_a", m) in ms.index else np.nan for m in t.m]
    for N in LOT_SIZES:
        t[f"reference_cost_per_100_fruit_N{N}"] = 100 * t.m * C_R / N
    return t
