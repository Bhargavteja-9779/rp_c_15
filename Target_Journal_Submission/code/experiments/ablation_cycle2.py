"""plan_v2 E2: LotCP-S with and without the episodic replay (mango, PLS, forward chaining, SEEDS_EXPLORE draw seeds 0-2)."""
import copy

import pandas as pd
from joblib import Parallel, delayed

from src.evaluation.run_eval import LOTCP_VARIANTS, evaluate
from src.utils import load_config, out_dir

V = {k: LOTCP_VARIANTS[k] for k in ("lotcp_s", "lotcp_s_noepisodic", "lotcp", "lotcp_noepisodic")}


def one(seed, t):
    cfg = copy.deepcopy(load_config("full")); cfg["eval"]["seed"] = seed
    rows, _, _ = evaluate(cfg, "pls", 0, "forward", t, 0.1, variants=V, m_grid=[0, 3, 5, 10, 20], n_draws=20, baselines=False)
    for r in rows:
        r["explore_seed"] = seed
    return rows


if __name__ == "__main__":
    res = Parallel(n_jobs=2)(delayed(one)(s, t) for s in (0, 1, 2) for t in (2017, 2018, 2019, 2020, 2021))
    df = pd.DataFrame([r for x in res for r in x])
    df.to_csv(out_dir(load_config("full"), "results/ablation_cycle2") / "replay_ablation.csv", index=False)
    print(df.replace(float("inf"), float("nan")).groupby(["method", "m"])[["coverage", "meets", "width", "iscore"]].mean().round(3).to_string())
