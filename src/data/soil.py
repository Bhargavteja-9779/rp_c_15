"""External data: Open Soil Spectral Library (OSSL v1.2) vis-NIR subsets, used to test whether the
findings on the mango data carry over to another agricultural NIR application.

Two subsets with a nested structure are built:
  * LUCAS (EU topsoil survey): campaigns 2009 and 2015; "lot" = 1-degree grid cell (a region).
  * KSSL  (USDA NRCS):         "lot" = survey project; "sample group" = pedon (site).
Spectra: reflectance 400-2500 nm thinned to 10 nm, converted to absorbance.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from src.utils import ROOT, get_logger

BASE = "https://storage.googleapis.com/soilspec4gg-public/"
FILES = ("ossl_soilsite_L0_v1.2.csv.gz", "ossl_soillab_L0_v1.2.csv.gz", "ossl_visnir_L0_v1.2.csv.gz")
RAW = ROOT / "data" / "raw" / "ossl"
CACHE = ROOT / "data" / "processed" / "ossl_visnir.npz"


@dataclass
class SoilData:
    X: np.ndarray
    wl: np.ndarray
    meta: pd.DataFrame          # columns: dataset, population (lot), reference_no (sample), group (pedon/point), season, targets

    def target(self, name: str) -> np.ndarray:
        return self.meta[name].to_numpy(np.float64)

    @property
    def lot(self):
        return self.meta["population"].to_numpy()

    @property
    def sample(self):
        return self.meta["reference_no"].to_numpy()

    @property
    def season(self):
        return self.meta["season"].to_numpy()


def _download():
    import urllib.request

    RAW.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        if not (RAW / f).exists():
            get_logger("soil").info("downloading %s", f)
            urllib.request.urlretrieve(BASE + f, RAW / f)


def load_soil() -> SoilData:
    meta_path = CACHE.with_suffix(".meta.csv")
    if not CACHE.exists():
        _download()
        head = pd.read_csv(RAW / FILES[2], nrows=1)
        spec = [c for c in head.columns if c.startswith("scan_visnir.")]
        wl_all = np.array([int(c.split(".")[1].split("_")[0]) for c in spec])
        keep = [c for c, w in zip(spec, wl_all) if 400 <= w <= 2500 and w % 10 == 0]
        v = pd.read_csv(RAW / FILES[2], usecols=["dataset.code_ascii_txt", "id.layer_uuid_txt"] + keep, low_memory=False)
        v = v[v["dataset.code_ascii_txt"].isin(["LUCAS.SSL", "KSSL.SSL"])].dropna(subset=keep)
        site = pd.read_csv(RAW / FILES[0], low_memory=False)
        lab = pd.read_csv(RAW / FILES[1], low_memory=False)
        m = v[["dataset.code_ascii_txt", "id.layer_uuid_txt"]].merge(site.drop(columns=["dataset.code_ascii_txt"]), on="id.layer_uuid_txt", how="left") \
            .merge(lab.drop(columns=["dataset.code_ascii_txt"]), on="id.layer_uuid_txt", how="left")
        assert (m["id.layer_uuid_txt"].to_numpy() == v["id.layer_uuid_txt"].to_numpy()).all()
        R = np.clip(v[keep].to_numpy(np.float64), 1e-4, None)
        if np.nanmedian(R) > 1.5:                      # stored in percent
            R = R / 100.0
        X = np.log10(1.0 / np.clip(R, 1e-4, None)).astype(np.float32)
        is_lucas = (m["dataset.code_ascii_txt"] == "LUCAS.SSL").to_numpy()
        lat, lon = m["latitude.point_wgs84_dd"].to_numpy(float), m["longitude.point_wgs84_dd"].to_numpy(float)
        year = pd.to_datetime(m["observation.date.begin_iso.8601_yyyy.mm.dd"], errors="coerce").dt.year.to_numpy()
        cell = np.array([f"{int(np.floor(a)) + 90}_{int(np.floor(b)) + 180}" if np.isfinite(a) and np.isfinite(b) else "na"
                         for a, b in zip(lat, lon)], dtype=object)
        lot = np.where(is_lucas, np.array(["cell_" + c for c in cell], dtype=object), ("proj_" + m["id.project_ascii_txt"].astype(str)).to_numpy(dtype=object))
        group = np.where(is_lucas, m["id.location_olc_txt"].astype(str).to_numpy(dtype=object), m["id.dataset.site_ascii_txt"].astype(str).to_numpy(dtype=object))
        out = pd.DataFrame({
            "dataset": np.where(is_lucas, "lucas", "kssl"),
            "population": pd.factorize(lot)[0], "lot_name": lot,
            "reference_no": np.arange(len(m)), "group": pd.factorize(group)[0], "season": year,
            "lat": lat, "lon": lon,
            "oc_log": np.where(is_lucas, np.log1p(m["oc_iso.10694_w.pct"].to_numpy(float)), np.log1p(m["c.tot_usda.a622_w.pct"].to_numpy(float))),
            "ph": np.where(is_lucas, m["ph.h2o_iso.10390_index"].to_numpy(float), np.nan),
        })
        ok = np.isfinite(X).all(1) & np.isfinite(out["oc_log"].to_numpy()) & (~is_lucas | (np.isfinite(lat) & np.isfinite(year.astype(float))))
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(CACHE, X=X[ok], wl=np.array([int(c.split(".")[1].split("_")[0]) for c in keep]))
        out[ok].reset_index(drop=True).to_csv(meta_path, index=False)
    z = np.load(CACHE)
    return SoilData(z["X"], z["wl"], pd.read_csv(meta_path))
