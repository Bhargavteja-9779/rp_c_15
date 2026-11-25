"""plan_v4 E2: matched baseline with the same label-free replicate scale as LotCP-S but no m-shot replay.

biascorr_rep  = mean bias from the m references; half-width = source quantile of residuals standardised by each
                past lot's own (full-information) mean and replicate/between-sample scale  (LotCP(scale='rep', episodic=False))
biascorr_full = same with the full scale (reference + replicate)  (= lotcp_s_noepisodic)
LotCP-S and LotCP-A are re-evaluated in the same call so all methods share the reference draws.
"""
import pandas as pd
from joblib import Parallel, delayed

from src.evaluation.run_eval import LOTCP_VARIANTS, evaluate
from src.utils import load_config, out_dir

V = {"lotcp_s": LOTCP_VARIANTS["lotcp_s"], "lotcp_a": LOTCP_VARIANTS["lotcp_a"],
     "biascorr_rep": ("season", {"scale": "rep", "episodic": False}),
     "biascorr_full": ("season", {"scale": "full", "episodic": False})}


def one(model, t):
    cfg = load_config("full")
    rows, _, _ = evaluate(cfg, model, 0, "forward", t, 0.1, variants=V, m_grid=[3, 5, 10, 20], baselines=True)
    return rows


if __name__ == "__main__":
    res = Parallel(n_jobs=4)(delayed(one)(mo, t) for mo in ("pls", "plspub") for t in (2017, 2018, 2019, 2020, 2021))
    df = pd.DataFrame([r for x in res for r in x])
    df.to_csv(out_dir(load_config("full"), "results/cycle3") / "matched_baseline.csv", index=False)
    d = df.replace(float("inf"), float("nan"))
    print(d[d.method.isin(list(V) + ["biascorr_naive", "target_only_centred"])]
          .groupby(["model", "method", "m"])[["coverage", "meets", "width", "iscore"]].mean().round(3).to_string())
