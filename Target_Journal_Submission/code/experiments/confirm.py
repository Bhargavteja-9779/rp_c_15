"""E6 confirmation of the FROZEN method (plan_v2), SEEDS_CONFIRM = 100..104.

C1: mango forward chaining (target lots already seen in cycle 1 -> re-draw confirmation).
C2: NeoSpectra handheld-NIR soil library (not opened before plan_v2): 5-fold CV over 1-degree cells.
Each seed sets the RNG of the reference draws and of the replay episodes. Per lot, outcomes are averaged over seeds x draws.
"""
from __future__ import annotations

import copy
from types import SimpleNamespace

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from src.evaluation.run_eval import LOTCP_VARIANTS, evaluate
from src.utils import ROOT, get_logger, load_config, out_dir

SEEDS_CONFIRM = (100, 101, 102, 103, 104)
FROZEN = {k: LOTCP_VARIANTS[k] for k in ("lotcp_s", "lotcp_a")}
M_GRID = [5, 10, 20]
NS = ROOT / "data" / "raw" / "neospectra" / "ns_soil_site_nir.csv"
NS_URL = "https://zenodo.org/api/records/13122321/files/Neospectra_WoodwellKSSL_soil+site+NIR.csv/content"


def _cfg(seed):
    cfg = load_config("full")
    cfg = copy.deepcopy(cfg)
    cfg["eval"]["seed"] = seed
    return cfg


def c1(seed, target):
    rows, _, _ = evaluate(_cfg(seed), "pls", 0, "forward", target, 0.1, variants=FROZEN, m_grid=M_GRID, n_draws=20)
    for r in rows:
        r.update(dataset="mango", confirm_seed=seed)
    return rows


def load_neospectra():
    if not NS.exists():
        import urllib.request

        NS.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(NS_URL, NS)
    d = pd.read_csv(NS, low_memory=False)
    spec = [c for c in d.columns if c.replace(".", "", 1).isdigit()]
    wl = np.array([float(c) for c in spec])
    order = np.argsort(wl)
    R = d[spec].to_numpy(float)[:, order]
    if np.nanmedian(R) > 1.5:
        R = R / 100.0
    X = np.log10(1.0 / np.clip(R, 1e-4, None)).astype(np.float32)
    lat = d["latitude.std.decimal.degrees"].fillna(d["lat.ycntr"]).to_numpy(float)
    lon = d["longitude.std.decimal.degrees"].fillna(d["long.xcntr"]).to_numpy(float)
    ok = np.isfinite(X).all(1) & np.isfinite(lat) & np.isfinite(lon) & d["eoc_tot_c"].notna().to_numpy()
    cell = np.array([f"{int(np.floor(a))}_{int(np.floor(b))}" if (np.isfinite(a) and np.isfinite(b)) else "na" for a, b in zip(lat, lon)], dtype=object)
    meta = pd.DataFrame({"population": pd.factorize(cell)[0], "reference_no": pd.factorize(d["lay_id"].astype(str))[0],
                         "y": np.log1p(np.clip(d["eoc_tot_c"].to_numpy(float), 0, None))})
    return X[ok], meta[ok].reset_index(drop=True), wl[order]


def c2_fold_predictions():
    from experiments.soil_external import _gkf, crossfit

    X, meta, _ = load_neospectra()
    lot, smp, y = meta.population.to_numpy(), meta.reference_no.to_numpy(), meta.y.to_numpy()
    fold = _gkf(lot, 5, 7)
    out = []
    for k in range(5):
        src, tgt = fold != k, fold == k
        P, info = crossfit(X, y, lot, smp, src, tgt)          # sample-grouped and lot-grouped folds inside the source
        out.append((k, P, info))
    return SimpleNamespace(y=y, lot=lot, sample=smp, meta=meta), out


def c2(seed, data, k, P):
    rows, _, _ = evaluate(_cfg(seed), "pls", 0, "neospectra", 9000 + k, 0.1, variants=FROZEN, m_grid=M_GRID, n_draws=20, data=data, P=P)
    for r in rows:
        r.update(dataset="neospectra", confirm_seed=seed, fold=k)
    return rows


def run(n_jobs=4):
    log = get_logger("confirm", load_config("full"))
    rdir = out_dir(load_config("full"), "results/confirmation")
    if not (rdir / "c1_mango.csv").exists():
        res = Parallel(n_jobs=n_jobs)(delayed(c1)(s, t) for s in SEEDS_CONFIRM for t in (2017, 2018, 2019, 2020, 2021))
        pd.DataFrame([r for x in res for r in x]).to_csv(rdir / "c1_mango.csv", index=False)
        log.info("C1 done")
    if not (rdir / "c2_neospectra.csv").exists():
        data, folds = c2_fold_predictions()
        pd.DataFrame([dict(fold=k, **{kk: vv for kk, vv in info.items() if kk != "cv_rmse_lot"},
                           n_source=int(len(P["src_idx"])), n_target=int(len(P["tgt_idx"])),
                           rmse_target=float(np.sqrt(np.mean((data.y[P["tgt_idx"]] - P["pred_tgt"]) ** 2))))
                      for k, P, info in folds]).to_csv(rdir / "c2_point.csv", index=False)
        res = Parallel(n_jobs=n_jobs)(delayed(c2)(s, data, k, P) for s in SEEDS_CONFIRM for k, P, _ in folds)
        pd.DataFrame([r for x in res for r in x]).to_csv(rdir / "c2_neospectra.csv", index=False)
        log.info("C2 done")


if __name__ == "__main__":
    run()
