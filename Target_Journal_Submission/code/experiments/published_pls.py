"""plan_v3 E7: main interval comparison with the published PLS recipe as point predictor (exploratory)."""
import pandas as pd
from joblib import Parallel, delayed

from src.evaluation.run_eval import LOTCP_VARIANTS, evaluate
from src.training.crossfit import SCHEMES, run_task
from src.utils import load_config, out_dir

V = {k: LOTCP_VARIANTS[k] for k in ("lotcp_s", "lotcp_a")}


def one(t):
    cfg = load_config("full")
    run_task(cfg, "plspub", 0, "forward", t, SCHEMES)
    rows, prow, _ = evaluate(cfg, "plspub", 0, "forward", t, 0.1, variants=V, m_grid=[0, 3, 5, 10, 20])
    return rows


if __name__ == "__main__":
    res = Parallel(n_jobs=2)(delayed(one)(t) for t in (2017, 2018, 2019, 2020, 2021))
    df = pd.DataFrame([r for x in res for r in x])
    df.to_csv(out_dir(load_config("full"), "results/published_pls") / "published_pls.csv", index=False)
    d = df.replace(float("inf"), float("nan"))
    print(d.groupby(["method", "m"])[["coverage", "meets", "width", "iscore"]].mean().round(3).to_string())
