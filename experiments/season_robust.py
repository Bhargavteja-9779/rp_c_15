"""plan_v7: season-robust replay (LotCP-R / LotCP-AR), exploratory. Same evaluation weights as the main study."""
import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from experiments.seq_calibration import LotStruct, build
from src.data.dataset import load_data
from src.evaluation.lotcp import LotCP
from src.training.crossfit import pred_path
from src.utils import load_config, out_dir

ALPHA, N_DRAWS = 0.10, 20


def season_groups(sea, lot):
    """Seasons with < 5 lots are merged with the next season (in time order). (A group needs >= 9 usable lots for a finite
    conformal quantile at alpha = 0.10; all source groups in this study had at least 11.)"""
    seasons = sorted(np.unique(sea))
    nl = {s: len(np.unique(lot[sea == s])) for s in seasons}
    groups, cur = [], []
    for s in seasons:
        cur.append(s)
        if sum(nl[x] for x in cur) >= 5:
            groups.append(cur); cur = []
    if cur:
        if groups:
            groups[-1] += cur
        else:
            groups.append(cur)
    return groups


def one(model, target, m):
    cfg = load_config("full")
    ev = cfg["eval"]
    d = load_data(cfg)
    P = np.load(pred_path(cfg, model, 0, "forward", target))  # seed 0 for every predictor
    src, tgt = P["src_idx"], P["tgt_idx"]
    res, pred, lot, smp, sea = d.y[src] - P["oof_season"], P["oof_season"], d.lot[src], d.sample[src], d.season[src]
    kw = dict(m=m, alpha=ALPHA, n_episodes=ev["n_episodes"], min_query=ev["min_query_samples"], scale="full", seed=ev["seed"] + m)
    cpS = LotCP(**kw).fit(res, lot, smp, pred)
    cpA = LotCP(**kw, assure=0.10).fit(res, lot, smp, pred)
    kw05 = dict(kw, alpha=0.05)
    cpS05 = LotCP(**kw05).fit(res, lot, smp, pred)        # matched baseline: a fixed smaller alpha (plan_v7 addendum)
    # season groups (seasons with < 5 lots merged with the next); per-group replay with the pooled fit's constants frozen
    grp = np.zeros(len(sea), dtype=int)
    groups = season_groups(sea, lot)
    for i, g in enumerate(groups):
        grp[np.isin(sea, g)] = i
    qS = cpS.group_quantiles(res, lot, smp, pred, grp, seed=ev["seed"] + 101 * m)
    qA = cpA.group_quantiles(res, lot, smp, pred, grp, seed=ev["seed"] + 101 * m)
    qSp = cpS.group_quantiles(res, lot, smp, pred, grp, seed=ev["seed"] + 101 * m, plain=True)   # sensitivity: plain quantiles
    qAp = cpA.group_quantiles(res, lot, smp, pred, grp, seed=ev["seed"] + 101 * m, plain=True)
    info = [dict(seasons="+".join(map(str, groups[g])), q_S=qS[g], q_A=qA.get(g, np.nan), q_S_pooled=cpS.q, q_A_pooled=cpA.q) for g in qS]
    qS_s, qA_s = sorted(qS.values()), sorted(qA.values())
    S = len(qS_s)
    mult = {"R": qS_s[-1] / cpS.q, "R2": (qS_s[-2] if S > 1 else qS_s[-1]) / cpS.q,
            "AR": qA_s[-1] / cpA.q, "AR2": (qA_s[-2] if len(qA_s) > 1 else qA_s[-1]) / cpA.q,
            "Rplain": max(qSp.values()) / cpS.q, "ARplain": max(qAp.values()) / cpA.q}
    lots_t = build(d.y[tgt] - P["pred_tgt"], P["pred_tgt"], d.lot[tgt], d.sample[tgt])
    rng = np.random.default_rng([41, target, m])
    rows = []
    for l, L in lots_t.items():
        if L.ns < m + ev["min_query_samples"]:
            continue
        acc = {}
        for e in range(N_DRAWS):
            sup = rng.choice(L.ns, m, replace=False)
            q = ~np.isin(L.inv, sup)
            w = 1.0 / ((L.ns - m) * L.cnt[L.inv][q])
            for name, cp, f in (("S", cpS, 1.0), ("R", cpS, mult["R"]), ("R2", cpS, mult["R2"]), ("A", cpA, 1.0), ("AR", cpA, mult["AR"]), ("AR2", cpA, mult["AR2"]), ("S05", cpS05, 1.0),
                                ("Rplain", cpS, mult["Rplain"]), ("ARplain", cpA, mult["ARplain"])):
                b, hw = cp.predict(L.smean[sup], L.rv)
                hw = hw * f
                e_ = L.r[q] - b
                cov = float(np.sum(w * (np.abs(e_) <= hw)))
                isc = float(np.sum(w * (2 * hw + (2 / ALPHA) * np.maximum(np.abs(e_) - hw, 0))))
                acc.setdefault(name, []).append((cov, 2 * hw, isc))
        for name, v in acc.items():
            v = np.array(v)
            rows.append(dict(model=model, target=target, m=m, lot=l, method=name, coverage=v[:, 0].mean(), width=v[:, 1].mean(),
                             iscore=v[:, 2].mean(), meets=float(np.mean(v[:, 0] >= 1 - ALPHA))))
    return rows, [dict(model=model, target=target, m=m, n_groups=S, mult_R=mult["R"], mult_R2=mult["R2"], mult_AR=mult["AR"], mult_AR2=mult["AR2"], **i) for i in info]


if __name__ == "__main__":
    import sys
    models = sys.argv[1:] or ["pls", "plspub"]
    jobs = [(mo, t, m) for mo in models for t in (2017, 2018, 2019, 2020, 2021) for m in (5, 10)]
    res = Parallel(n_jobs=4)(delayed(one)(*j) for j in jobs)
    od = out_dir(load_config("full"), "results/cycle4")
    tag = "" if models == ["pls", "plspub"] else "_" + "_".join(models)
    df = pd.DataFrame([r for x in res for r in x[0]]); df.to_csv(od / f"robust_lots{tag}.csv", index=False)
    pd.DataFrame([r for x in res for r in x[1]]).to_csv(od / f"robust_quantiles{tag}.csv", index=False)
    rows = []
    for (mo, m, meth), g in df.groupby(["model", "m", "method"]):
        s = g.groupby("target")[["coverage", "meets"]].mean()
        rows.append(dict(model=mo, m=m, method=meth, cov=g.coverage.mean(), cov_ex2017=g[g.target != 2017].coverage.mean(),
                         seasons_cov90=int((s.coverage >= 0.9).sum()), meets=g.meets.mean(), meets_ex2017=g[g.target != 2017].meets.mean(),
                         seasons_meets90=int((s.meets >= 0.9).sum()), width=g.width.mean(), iscore=g.iscore.mean()))
    out = pd.DataFrame(rows); out.to_csv(od / f"robust_summary{tag}.csv", index=False)
    print(out.round(3).to_string(index=False))
