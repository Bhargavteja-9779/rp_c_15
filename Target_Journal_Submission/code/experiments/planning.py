"""Reference-budget planning: the episodic replay yields, from past lots only, the interval width
that LotCP-S / LotCP-A will deliver for each number m of reference samples. This script compares
that *planned* width (available before the season starts) with the width *realised* on the lots
of the target season (forward chaining; PLS, LightGBM seed 0, CNN seed 0)."""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.data.dataset import load_data
from src.evaluation.lotcp import LotCP
from src.training.crossfit import pred_path
from src.utils import get_logger, out_dir

VARIANTS = {"lotcp_s": {"scale": "full"}, "lotcp_a": {"scale": "full", "assure": 0.10}}


def run(cfg):
    log = get_logger("planning", cfg)
    d = load_data(cfg)
    a, ev = cfg["eval"]["primary_alpha"], cfg["eval"]
    raw = pd.read_csv(out_dir(cfg, "results") / "raw_results.csv")
    raw = raw[(raw.protocol == "forward") & np.isclose(raw.alpha, a) & (raw.seed == 0)]
    rows = []
    for model in ("pls", "gbm", "cnn"):
        for t in cfg["protocols"]["forward"]["targets"]:
            p = pred_path(cfg, model, 0, "forward", t)
            if not p.exists():
                continue
            P = np.load(p)
            src = P["src_idx"]
            r = d.y[src] - P["oof_season"]
            for name, kw in VARIANTS.items():
                for m in ev["m_grid"]:
                    cp = LotCP(m=m, alpha=a, n_episodes=ev["n_episodes"], min_query=ev["min_query_samples"], seed=ev["seed"] + m, **kw) \
                        .fit(r, d.lot[src], d.sample[src], P["oof_season"])
                    g = raw[(raw.model == model) & (raw.target == t) & (raw.method == name) & (raw.m == m)]
                    if g.empty:
                        continue
                    rows.append(dict(model=model, target=t, method=name, m=m, planned_width=cp.planned_width,
                                     realised_width=float(g.width.mean()), realised_coverage=float(g.coverage.mean()), n_lots=len(g)))
    df = pd.DataFrame(rows)
    df["rel_error"] = (df.realised_width - df.planned_width) / df.planned_width
    df.to_csv(out_dir(cfg, "results/robustness") / "planning.csv", index=False)
    log.info("planning: %d rows, median |relative error| %.3f", len(df), df.rel_error.abs().median())


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
