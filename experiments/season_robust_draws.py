"""Draw sensitivity of the season counts (review round 3): the season-robust evaluation repeated with five reference-draw
seeds (calibration unchanged). Reports, per predictor and method, the distribution of the number of seasons reaching 0.90
and each season's coverage range across seeds."""
import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from experiments.season_robust import one
from src.utils import load_config, out_dir

SEEDS = (41, 42, 43, 44, 45)

if __name__ == "__main__":
    jobs = [(mo, t, 10, sd) for mo in ("pls", "plspub", "gbm", "cnn") for t in (2017, 2018, 2019, 2020, 2021) for sd in SEEDS]
    res = Parallel(n_jobs=4)(delayed(one)(*j) for j in jobs)
    rows = []
    for (mo, t, m, sd), (r, _) in zip(jobs, res):
        for x in r:
            x["draw_seed"] = sd
            rows.append(x)
    df = pd.DataFrame(rows)
    od = out_dir(load_config("full"), "results/cycle4")
    df.to_csv(od / "robust_draws_lots.csv.gz", index=False)
    s = df.groupby(["model", "method", "draw_seed", "target"])[["coverage", "meets"]].mean().reset_index()
    s.to_csv(od / "robust_draws_seasons.csv", index=False)
    cnt = s.groupby(["model", "method", "draw_seed"]).agg(seasons_cov=("coverage", lambda c: int((c >= 0.9).sum())),
                                                          seasons_meets=("meets", lambda c: int((c >= 0.9).sum())),
                                                          min_cov=("coverage", "min")).reset_index()
    cnt.to_csv(od / "robust_draws_counts.csv", index=False)
    print(cnt.groupby(["model", "method"]).agg(cov_counts=("seasons_cov", lambda v: sorted(v)), meets_counts=("seasons_meets", lambda v: sorted(v)),
                                               min_cov_lo=("min_cov", "min"), min_cov_hi=("min_cov", "max")).to_string())
