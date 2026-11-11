"""Stage 2: model-based uncertainty baselines that need their own fits
(conformalised quantile regression, quantile regression forest, deep ensemble)."""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np
from joblib import Parallel, delayed

from src.data.dataset import load_data
from src.models.point import CNNModel, GBMModel
from src.training.crossfit import pred_path
from src.utils import get_logger, out_dir, save_json

QRF_LEVELS = (0.025, 0.05, 0.1, 0.9, 0.95, 0.975)


def uq_path(cfg, protocol, target) -> Path:
    return out_dir(cfg, "results/predictions") / f"uq_{protocol}_{target}.npz"


def _ens_member(cfg, Xs, ys, Xt, seed):
    import torch

    torch.set_num_threads(1)
    mc = {k: v for k, v in cfg["models"]["cnn"].items() if k != "seeds"}
    model = CNNModel(seed=seed, nll=True, **mc).fit(Xs, ys)
    mean, var = model.predict_dist(Xt)
    mcd = model.predict_mc_dropout(Xt) if seed == 100 else None     # MC dropout on the first member
    return mean, var, mcd


def run_target(cfg, protocol, target, n_jobs=4):
    path = uq_path(cfg, protocol, target)
    if path.exists():
        return
    d = load_data(cfg)
    base = np.load(pred_path(cfg, "pls", 0, protocol, target))      # reuse identical rows and folds
    src_idx, tgt_idx = base["src_idx"], base["tgt_idx"]
    Xs, ys, Xt = d.X[src_idx], d.y[src_idx], d.X[tgt_idx]
    out, info = {}, {}
    # --- conformalised quantile regression (LightGBM pinball loss), alpha = 0.1 only ---------
    t = time.time()
    gp = {k: v for k, v in cfg["models"]["gbm"].items() if k != "seeds"}
    for tag, a in (("lo", 0.05), ("hi", 0.95)):
        for scheme in ("sample", "season"):
            folds, oof = base[f"fold_{scheme}"], np.full(len(ys), np.nan)
            for f in np.unique(folds):
                te = folds == f
                oof[te] = GBMModel(objective="quantile", alpha=a, **gp).fit(Xs[~te], ys[~te]).predict(Xs[te])
            out[f"cqr_{tag}_oof_{scheme}"] = oof
        out[f"cqr_{tag}_tgt"] = GBMModel(objective="quantile", alpha=a, **gp).fit(Xs, ys).predict(Xt)
    info["cqr_seconds"] = time.time() - t
    # --- quantile regression forest on PLS scores ------------------------------------------
    t = time.time()
    from quantile_forest import RandomForestQuantileRegressor

    sc = np.load(out_dir(cfg, "data/processed") / f"plsscores_{protocol}_{target}.npz")
    qrf = RandomForestQuantileRegressor(n_estimators=cfg["models"]["qrf"]["n_estimators"],
                                        min_samples_leaf=cfg["models"]["qrf"]["min_samples_leaf"], n_jobs=n_jobs, random_state=0)
    qrf.fit(sc["src"], ys)
    out["qrf_q"] = qrf.predict(sc["tgt"], quantiles=list(QRF_LEVELS))
    out["qrf_mean"] = qrf.predict(sc["tgt"], quantiles="mean")
    info["qrf_seconds"] = time.time() - t
    # --- deep ensemble of heteroscedastic CNNs ----------------------------------------------
    t = time.time()
    res = Parallel(n_jobs=n_jobs)(delayed(_ens_member)(cfg, Xs, ys, Xt, 100 + i) for i in range(cfg["models"]["ensemble"]["members"]))
    mu = np.stack([r[0] for r in res]); var = np.stack([r[1] for r in res])
    out["ens_mean"] = mu.mean(0)
    out["ens_var"] = (var + mu ** 2).mean(0) - mu.mean(0) ** 2
    out["mcd_mean"], out["mcd_var"] = res[0][2]
    info["ensemble_seconds"] = time.time() - t
    np.savez_compressed(path, **out)
    save_json(info, path.with_suffix(".json"))


def run(cfg):
    log = get_logger("uq_models", cfg)
    for target in cfg["protocols"]["forward"]["targets"]:
        run_target(cfg, "forward", target)
        log.info("uq baselines done for forward/%s", target)


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
