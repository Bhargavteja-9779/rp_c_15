"""Stage 1: fit point predictors and store (i) target-season predictions of the final model and
(ii) out-of-fold source predictions under sample-, lot- and season-grouped folds."""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np
from joblib import Parallel, delayed

from src.data.dataset import load_data
from src.models.point import make_model
from src.training.splits import fold_ids, protocol_masks
from src.utils import get_logger, out_dir, save_json

SCHEMES = ("sample", "lot", "season")


def pred_path(cfg, model, seed, protocol, target) -> Path:
    return out_dir(cfg, "results/predictions") / f"{model}_s{seed}_{protocol}_{target}.npz"


def _oof(model_name, cfg, seed, X, y, folds, **override):
    oof = np.full(len(y), np.nan)
    for f in np.unique(folds):
        te = folds == f
        oof[te] = make_model(model_name, cfg, seed, **override).fit(X[~te], y[~te]).predict(X[te])
    return oof


def run_task(cfg, model_name, seed, protocol, target, schemes=SCHEMES):
    path = pred_path(cfg, model_name, seed, protocol, target)
    if path.exists():
        return str(path)
    if model_name == "cnn":
        import torch

        torch.set_num_threads(1)
    d = load_data(cfg)
    src, tgt = protocol_masks(d.season, protocol, target)
    src_idx, tgt_idx = np.flatnonzero(src), np.flatnonzero(tgt)
    if cfg.get("quick_subsample") and len(src_idx) > cfg["quick_subsample"]:
        src_idx = np.sort(np.random.default_rng(0).choice(src_idx, cfg["quick_subsample"], replace=False))
    Xs, ys = d.X[src_idx], d.y[src_idx]
    t0 = time.time()
    info = {"model": model_name, "seed": seed, "protocol": protocol, "target": target, "n_source": len(src_idx), "n_target": len(tgt_idx)}
    folds = {s: fold_ids(s, d.sample[src_idx], d.lot[src_idx], d.season[src_idx],
                         cfg["folds"]["k_sample" if s == "sample" else "k_lot"], seed=1000 + target) for s in schemes}
    override = {}
    out = {"src_idx": src_idx, "tgt_idx": tgt_idx}
    if model_name == "pls":
        # number of latent variables: leave-one-season-out CV inside the source data only
        grid, best = cfg["models"]["pls"]["n_components_grid"], None
        cv = {}
        for nc in grid:
            o = _oof("pls", cfg, seed, Xs, ys, folds["season"], n_components=nc)
            cv[nc] = float(np.sqrt(np.mean((ys - o) ** 2)))
            if best is None or cv[nc] < cv[best]:
                best, out["oof_season"] = nc, o
        override, info["pls_cv_rmse"], info["n_components"] = {"n_components": best}, cv, best
    for s in schemes:
        if f"oof_{s}" not in out:
            out[f"oof_{s}"] = _oof(model_name, cfg, seed, Xs, ys, folds[s], **override)
        out[f"fold_{s}"] = folds[s]
    t1 = time.time()
    final = make_model(model_name, cfg, seed, **override).fit(Xs, ys)
    info["fit_seconds_final"] = time.time() - t1
    t2 = time.time()
    out["pred_tgt"] = final.predict(d.X[tgt_idx])
    info["predict_seconds_per_1000"] = (time.time() - t2) / max(len(tgt_idx), 1) * 1000
    if model_name == "pls":           # latent scores feed the covariate-shift weights and the QRF baseline
        np.savez_compressed(out_dir(cfg, "data/processed") / f"plsscores_{protocol}_{target}.npz",
                            src=final.scores(Xs).astype(np.float32), tgt=final.scores(d.X[tgt_idx]).astype(np.float32))
    if model_name == "cnn":
        info["n_params"], info["train_loss_curve"] = final.n_params(), final.history
    info["total_seconds"] = time.time() - t0
    np.savez_compressed(path, **out)
    save_json(info, path.with_suffix(".json"))
    return str(path)


def task_list(cfg, protocols=("forward", "loso")):
    tasks = []
    for protocol in protocols:
        for target in cfg["protocols"][protocol]["targets"]:
            tasks.append(("pls", 0, protocol, target, SCHEMES))
            if protocol == "forward":
                for name in ("gbm", "cnn"):
                    for seed in cfg["models"][name]["seeds"]:
                        tasks.append((name, seed, protocol, target, SCHEMES))
            else:                                   # robustness protocol: one CNN seed, season folds only
                tasks.append(("cnn", cfg["models"]["cnn"]["seeds"][0], protocol, target, ("season",)))
    return tasks


def run(cfg, n_jobs: int = 4):
    log = get_logger("crossfit", cfg)
    tasks = task_list(cfg)
    light = [t for t in tasks if t[0] != "cnn"]
    heavy = [t for t in tasks if t[0] == "cnn"]
    log.info("%d light tasks (sequential), %d CNN tasks (parallel x%d)", len(light), len(heavy), n_jobs)
    for t in light:
        run_task(cfg, *t)
    Parallel(n_jobs=n_jobs)(delayed(run_task)(cfg, *t) for t in heavy)
    log.info("cross-fitting finished")


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
