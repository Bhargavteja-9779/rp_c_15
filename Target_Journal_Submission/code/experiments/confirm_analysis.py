"""Pre-registered analysis of the E6 confirmation (experiments/plan_v2.yaml): P1-P4, Holm over 4 per dataset."""
import json

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon

from src.statistics.analysis import holm, rank_biserial
from src.utils import ROOT

RD = ROOT / "results" / "confirmation"


def boot_ci(x, n=2000, seed=7):
    rng = np.random.default_rng(seed)
    m = [rng.choice(x, len(x)).mean() for _ in range(n)]
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def per_lot(df):
    keys = ["target", "lot", "method", "m"] + (["fold"] if "fold" in df else [])
    d = df.replace(np.inf, np.nan)
    return d.groupby(keys, as_index=False)[["coverage", "iscore", "meets", "width"]].mean()


def analyse(df, name):
    d = per_lot(df)
    piv = {k: d.pivot_table(index=["target", "lot"], columns=["method", "m"], values=k) for k in ("iscore", "meets", "coverage", "width")}
    res = []
    for pid, m in (("P1", 5), ("P2", 10)):
        a, b = piv["iscore"][("lotcp_s", m)], piv["iscore"][("biascorr_naive", m)]
        diff = (a - b).dropna().to_numpy()
        res.append(dict(endpoint=pid, metric="interval score", m=m, comparison="LotCP-S - biascorr_naive", expected="< 0", diff=diff))
    for pid, m in (("P3", 10), ("P4", 20)):
        cands = {k: piv["meets"][(k, m)].mean() for k in ("biascorr_naive", "target_only_centred") if (k, m) in piv["meets"]}
        best = max(cands, key=cands.get)
        diff = (piv["meets"][("lotcp_a", m)] - piv["meets"][(best, m)]).dropna().to_numpy()
        res.append(dict(endpoint=pid, metric="share of draws with lot coverage >= 0.90", m=m, comparison=f"LotCP-A - {best}", expected="> 0", diff=diff))
    for r in res:
        x = r.pop("diff")
        r["n_lots"] = int(len(x))
        r["mean_diff"] = float(x.mean()) if len(x) else np.nan
        r["ci_lo"], r["ci_hi"] = boot_ci(x) if len(x) > 1 else (np.nan, np.nan)
        r["p"] = float(wilcoxon(x).pvalue) if len(x) > 5 and np.any(x != 0) else np.nan
        r["rank_biserial"] = rank_biserial(x) if len(x) else np.nan
    t = pd.DataFrame(res)
    t["p_holm"] = holm(t["p"].fillna(1).to_numpy())
    sign = np.where(t.expected == "< 0", -1, 1)
    t["confirmed"] = (t.p_holm < 0.05) & (np.sign(t.ci_lo) == sign) & (np.sign(t.ci_hi) == sign) & (t.rank_biserial * sign >= 0.2)
    t.insert(0, "dataset", name)
    # descriptive summary of every method
    summ = d.groupby(["method", "m"]).agg(n_lots=("lot", "size"), coverage=("coverage", "mean"), meets=("meets", "mean"), width=("width", "mean"), iscore=("iscore", "mean")).reset_index()
    summ.insert(0, "dataset", name)
    return t, summ


def run():
    out, summ = [], []
    for f, name in (("c1_mango.csv", "mango (re-draw, lots seen in cycle 1)"), ("c2_neospectra.csv", "NeoSpectra (untouched)")):
        if (RD / f).exists():
            t, s = analyse(pd.read_csv(RD / f), name)
            out.append(t); summ.append(s)
    T = pd.concat(out, ignore_index=True)
    T.to_csv(RD / "confirmation_tests.csv", index=False)
    pd.concat(summ, ignore_index=True).to_csv(RD / "confirmation_summary.csv", index=False)
    (RD / "confirmation_tests.json").write_text(T.to_json(orient="records", indent=1))
    print(T.round(4).to_string(index=False))


if __name__ == "__main__":
    run()
