"""plan_v4 E4: harvest decisions and assumed-cost economics with season-level uncertainty (exploratory).

Answers review round 1 (R1-C5, R3-2/4/5):
  * operating point fixed in advance: specification 15 % DMC, lot rule p = 0.8, alpha = 0.10 (c_D = 1/9), lot size 1000;
  * two-stage season-cluster bootstrap 95 % CIs (seasons, then lots within season) for every rate and cost, and for the
    cost DIFFERENCE between each rule and the cheapest rule that uses no reference fruit (point / split-CP bound / withhold all);
  * alpha chosen by leave-one-season-out cost minimisation (no hindsight on the evaluated season);
  * both point predictors: SNV PLS ('pls') and the published recipe ('plspub', harvest simulator rerun here);
  * planner forecast error by number of source seasons.
"""
import json

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from experiments.harvest import ALPHAS, _target
from src.statistics.harvest_analysis import C_D, C_R
from src.utils import load_config, out_dir

T, P_LOT, A0, N = 15.0, 0.8, 0.1, 1000
B = 2000
RULES = ["point", "scp_lower", "point_bc", "bc_lower", "lotcp_s_lower", "lotcp_a_lower"]


def run_plspub(cfg, od):
    f = od / "harvest_plspub_fruit.csv.gz"
    if f.exists():
        return
    res = Parallel(n_jobs=4)(delayed(_target)(cfg, "plspub", t, 20) for t in cfg["protocols"]["forward"]["targets"])
    fc = ["model", "target", "lot", "m", "draw", "rule", "alpha", "threshold", "accepted", "compliant", "false_accept", "false_withhold"]
    lc = ["model", "target", "lot", "m", "draw", "rule", "alpha", "threshold", "p", "harvest", "ready"]
    fr = pd.DataFrame([r for x in res for r in x[0]], columns=fc).fillna({"alpha": -1})
    fr.groupby(["model", "rule", "alpha", "threshold", "m", "target", "lot"], as_index=False)[
        ["accepted", "compliant", "false_accept", "false_withhold"]].mean().to_csv(f, index=False)
    pd.DataFrame([r for x in res for r in x[1]], columns=lc).fillna({"alpha": -1}).to_csv(od / "harvest_plspub_lots.csv.gz", index=False)


def lot_tables(od):
    fr = pd.concat([pd.read_csv("results/harvest/fruit_by_lot.csv.gz"), pd.read_csv(od / "harvest_plspub_fruit.csv.gz")])
    lo = pd.concat([pd.read_csv("results/harvest/lot_decisions.csv.gz"), pd.read_csv(od / "harvest_plspub_lots.csv.gz")])
    fr = fr[(fr.threshold == T) & fr.model.isin(["pls", "plspub"])]
    lo = lo[(lo.threshold == T) & (lo.p == P_LOT) & lo.model.isin(["pls", "plspub"])]
    lo = lo.groupby(["model", "rule", "alpha", "m", "target", "lot"]).agg(h=("harvest", "mean"), ready=("ready", "mean")).reset_index()
    lo["ready_lot"] = lo.ready >= 0.5
    return fr, lo


def boot(df, col, rng, stat=np.mean):
    """Two-stage season-cluster bootstrap CI of stat(df[col])."""
    g = [x[col].to_numpy() for _, x in df.groupby("target")]
    out = np.empty(B)
    for i in range(B):
        v = np.concatenate([g[k][rng.integers(0, len(g[k]), len(g[k]))] for k in rng.integers(0, len(g), len(g))])
        out[i] = stat(v) if len(v) else np.nan
    return np.nanpercentile(out, [2.5, 97.5])


def cost(df, cd, m):
    return df.false_accept + cd * df.false_withhold + m * C_R / N


def main():
    cfg = load_config("full")
    od = out_dir(cfg, "results/cycle3")
    run_plspub(cfg, od)
    fr, lo = lot_tables(od)
    rng = np.random.default_rng(0)
    cd = C_D[A0]
    rows, diffs, best = [], [], {}
    for model in ("pls", "plspub"):
        f = fr[fr.model == model].copy()
        comp = f[(f.rule == "point") & (f.m == 0)][["target", "lot", "compliant"]]
        cand = {}                                                        # rule@m -> per-lot cost at the fixed operating point
        for rule in RULES:
            for m in sorted(f[f.rule == rule].m.unique()):
                z = f[(f.rule == rule) & (f.m == m) & ((f.alpha == -1) | np.isclose(f.alpha, A0))].copy()
                if z.empty:
                    continue
                z["cost"] = cost(z, cd, m)
                cand[(rule, int(m))] = z[["target", "lot", "cost", "false_accept", "false_withhold", "accepted"]]
        wn = comp.copy(); wn["cost"] = cd * wn.compliant                 # withhold everything
        cand[("withhold_all", 0)] = wn[["target", "lot", "cost"]]
        m0 = {k: v for k, v in cand.items() if k[1] == 0}
        best0 = min(m0, key=lambda k: m0[k].cost.mean())
        best[model] = f"{best0[0]}@m0"
        for (rule, m), z in cand.items():
            lz = lo[(lo.model == model) & (lo.rule == rule) & (lo.m == m) & ((lo.alpha == -1) | np.isclose(lo.alpha, A0))]
            nr, rd = lz[~lz.ready_lot], lz[lz.ready_lot]
            r = dict(model=model, rule=rule, m=m, n_lots=len(z), cost100=100 * z.cost.mean(),
                     cost100_lo=100 * boot(z, "cost", rng)[0], cost100_hi=100 * boot(z, "cost", rng)[1])
            if "false_accept" in z:
                r.update(immature_accepted=100 * z.false_accept.mean(), mature_withheld=100 * z.false_withhold.mean())
            if len(nr):
                lo_, hi_ = boot(nr, "h", rng)
                r.update(premature_lots=100 * nr.h.mean(), premature_lo=100 * lo_, premature_hi=100 * hi_, not_ready_lots=len(nr))
            if len(rd):
                rd2 = rd.assign(d=1 - rd.h)
                lo_, hi_ = boot(rd2, "d", rng)
                r.update(delayed_lots=100 * rd2.d.mean(), delayed_lo=100 * lo_, delayed_hi=100 * hi_, ready_lots=len(rd))
            rows.append(r)
            j = z.merge(m0[best0], on=["target", "lot"], suffixes=("", "_b"))
            j["d"] = 100 * (j.cost - j.cost_b)
            if len(j) and (rule, m) != best0:
                lo_, hi_ = boot(j, "d", rng)
                sm = j.groupby("target").d.mean()
                diffs.append(dict(model=model, rule=rule, m=m, comparator=f"{best0[0]}@m0", diff100=j.d.mean(), lo=lo_, hi=hi_,
                                  seasons_cheaper=int((sm < 0).sum()), n_seasons=len(sm)))
    pd.DataFrame(rows).to_csv(od / "decisions_ci.csv", index=False)
    pd.DataFrame(diffs).to_csv(od / "decisions_vs_best_m0.csv", index=False)

    # leave-one-season-out choice of alpha (for each cost ratio) vs the decision-theoretic alpha*
    lo_rows = []
    for model in ("pls", "plspub"):
        f = fr[(fr.model == model) & fr.rule.isin(["scp_lower", "bc_lower", "lotcp_s_lower"])]
        for (rule, m), z in f.groupby(["rule", "m"]):
            for a_star, cdv in C_D.items():
                z = z.assign(c=z.false_accept + cdv * z.false_withhold)
                tot_star, tot_loso, tot_best = [], [], []
                for t in sorted(z.target.unique()):
                    tr, te = z[z.target != t], z[z.target == t]
                    a_sel = tr.groupby("alpha").c.mean().idxmin()
                    tot_loso.append(te[np.isclose(te.alpha, a_sel)].c.mean())
                    tot_star.append(te[np.isclose(te.alpha, a_star)].c.mean())
                    tot_best.append(te.groupby("alpha").c.mean().min())
                lo_rows.append(dict(model=model, rule=rule, m=int(m), alpha_star=a_star, cost_alpha_star=100 * np.mean(tot_star),
                                    cost_loso=100 * np.mean(tot_loso), cost_hindsight=100 * np.mean(tot_best)))
    pd.DataFrame(lo_rows).to_csv(od / "alpha_loso.csv", index=False)

    # planner forecast error by number of source seasons (first season 2015 -> target T has T-2015 source seasons)
    p = pd.read_csv("results/robustness/planning.csv")
    p = p[p.model == "pls"].assign(n_source=lambda x: x.target - 2015)
    pl = p.groupby(["method", "n_source"]).agg(mean_rel_error=("rel_error", "mean"), mean_abs_rel_error=("rel_error", lambda v: np.mean(np.abs(v)))).reset_index()
    pl.to_csv(od / "planner_by_sources.csv", index=False)

    d = pd.DataFrame(rows)
    print(d[d.rule.isin(RULES + ["withhold_all"])].round(2).to_string(index=False))
    print(pd.DataFrame(diffs).round(2).to_string(index=False))
    print(pd.DataFrame(lo_rows).query("m in [0,5,10]").round(2).to_string(index=False))
    print(pl.round(3).to_string(index=False))
    json.dump(dict(best_m0=best, operating_point=dict(spec=T, lot_share=P_LOT, alpha=A0, c_D=cd, lot_size=N), B=B), open(od / "decisions_meta.json", "w"), indent=1)


if __name__ == "__main__":
    main()
