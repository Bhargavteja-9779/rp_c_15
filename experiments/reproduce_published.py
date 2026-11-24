"""G4: reproduce published point-prediction baselines on the provider's published split (MangoDMC_NIR_Data_v3.csv).

Train = Set in {Cal, Tuning} (n = 10,243); test = "Val Ext" (n = 1,448, season 4) and "Val Ext 2" (n = 320).
  pls_published : mean-centred SG 2nd derivative (17 pt, 2nd order), 684-990 nm, LVs by population-grouped CV  (Anderson et al. 2020)
  pls_ours      : our pipeline (SNV + SG 2nd derivative), same LV selection
  cnn_ours      : our 1D-CNN, SEEDS_EXPLORE = 0, 1, 2, no augmentation, 20 epochs
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import GroupKFold

from src.models.point import CNNModel, PLSModel
from src.utils import ROOT, get_logger, load_config, out_dir, save_json

V3 = ROOT / "data" / "raw" / "MangoDMC_NIR_Data_v3.csv"
URL_V3 = "https://data.mendeley.com/public-files/datasets/46htwnp833/files/10975117-717b-4504-a372-7845b4c42237/file_downloaded"


def load_v3():
    if not V3.exists():
        import urllib.request

        urllib.request.urlretrieve(URL_V3, V3)
    d = pd.read_csv(V3)
    wl = [c for c in d.columns if c.isdigit() and 684 <= int(c) <= 990]
    return d, wl


class PLSPublished:
    def __init__(self, n_components):
        self.nc = n_components

    def _prep(self, X):
        return savgol_filter(X, 17, 2, deriv=2, axis=1)

    def fit(self, X, y):
        self.m = PLSRegression(self.nc, scale=False).fit(self._prep(X), y)          # PLSRegression mean-centres
        return self

    def predict(self, X):
        return self.m.predict(self._prep(X)).ravel()


def _select_lv(make, X, y, groups, grid):
    f = np.empty(len(y), int)
    for i, (_, te) in enumerate(GroupKFold(5).split(X, y, groups)):
        f[te] = i
    cv = {}
    for nc in grid:
        o = np.empty(len(y))
        for k in range(5):
            o[f == k] = make(nc).fit(X[f != k], y[f != k]).predict(X[f == k])
        cv[nc] = float(np.sqrt(np.mean((y - o) ** 2)))
    return min(cv, key=cv.get), cv


def stats(y, p):
    r = y - p
    return dict(n=len(y), rmsep=float(np.sqrt(np.mean(r ** 2))), bias=float(np.mean(p - y)), sep=float(np.std(r, ddof=1)))


def run(cfg):
    log = get_logger("reproduce", cfg)
    d, wl = load_v3()
    X, y = d[wl].to_numpy(float), d["DM"].to_numpy(float)
    tr = d["Set"].isin(["Cal", "Tuning"]).to_numpy()
    tests = {"val_ext": (d["Set"] == "Val Ext").to_numpy(), "val_ext2": (d["Set"] == "Val Ext 2").to_numpy()}
    groups = d["Pop"].astype(str).to_numpy()
    out, rows = {"n_train": int(tr.sum())}, []
    grid = list(range(6, 31, 2))
    for name, make in (("pls_published", PLSPublished), ("pls_ours", lambda nc: PLSModel(n_components=nc))):
        nc, cv = _select_lv(make, X[tr], y[tr], groups[tr], grid)
        m = make(nc).fit(X[tr], y[tr])
        out[name] = {"n_components": nc, "rmsecv": cv[nc]}
        for t, mask in tests.items():
            rows.append(dict(model=name, seed=None, test=t, **stats(y[mask], m.predict(X[mask]))))
    mc = {k: v for k, v in cfg["models"]["cnn"].items() if k != "seeds"}
    for seed in (0, 1, 2):                       # SEEDS_EXPLORE
        m = CNNModel(seed=seed, **mc).fit(X[tr], y[tr])
        for t, mask in tests.items():
            rows.append(dict(model="cnn_ours", seed=seed, test=t, **stats(y[mask], m.predict(X[mask]))))
    df = pd.DataFrame(rows)
    rdir = out_dir(cfg, "results/reproduction")
    df.to_csv(rdir / "reproduction.csv", index=False)
    save_json(out, rdir / "reproduction_meta.json")
    log.info("reproduction finished\n%s", df.to_string(index=False))


if __name__ == "__main__":
    import sys

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
