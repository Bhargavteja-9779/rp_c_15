"""Load the raw CSV once, keep the analysis window and cache a compact array file."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.data.download import ensure_raw
from src.utils import ROOT, get_logger

META_COLS = [
    "population", "date", "season", "region", "cultivar", "physio_stage", "temp",
    "reference_no", "dry_matter", "instrument", "outlier_flag_1", "subsequent_flag_1", "origin",
]


@dataclass
class MangoData:
    X: np.ndarray            # (n, p) absorbance, float32
    wl: np.ndarray           # (p,) wavelengths in nm
    meta: pd.DataFrame       # one row per spectrum, index 0..n-1

    @property
    def y(self) -> np.ndarray:
        return self.meta["dry_matter"].to_numpy(np.float64)

    @property
    def lot(self) -> np.ndarray:
        return self.meta["population"].to_numpy()

    @property
    def sample(self) -> np.ndarray:
        return self.meta["reference_no"].to_numpy()

    @property
    def season(self) -> np.ndarray:
        return self.meta["season"].to_numpy()


def load_data(cfg: dict) -> MangoData:
    log = get_logger("data")
    cache = ROOT / cfg["data"]["processed"]
    meta_path = cache.with_suffix(".meta.csv")
    if not cache.exists():
        raw = pd.read_csv(ensure_raw(cfg), low_memory=False)
        wl_cols = [c for c in raw.columns if c.isdigit() and cfg["data"]["wl_min"] <= int(c) <= cfg["data"]["wl_max"]]
        X = raw[wl_cols].to_numpy(np.float32)
        ok = np.isfinite(X).all(1) & np.isfinite(raw["dry_matter"].to_numpy(float))
        log.info("raw rows %d, dropped (non-finite) %d, wavelengths %d", len(raw), int((~ok).sum()), len(wl_cols))
        cache.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(cache, X=X[ok], wl=np.array([int(c) for c in wl_cols]))
        raw.loc[ok, META_COLS].reset_index(drop=True).to_csv(meta_path, index=False)
    z = np.load(cache)
    meta = pd.read_csv(meta_path)
    return MangoData(X=z["X"], wl=z["wl"], meta=meta)
