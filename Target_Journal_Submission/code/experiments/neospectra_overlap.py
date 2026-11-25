"""plan_v4 E7: overlap between the NeoSpectra confirmation soils and the KSSL soils used in development.

Development used the KSSL layers that have a complete vis-NIR spectrum (400-2500 nm, 10 nm) and total carbon in the
OSSL (src/data/soil.py; 19,807 rows). NeoSpectra rows carry the KSSL layer id `lay_id`; OSSL site rows carry it as
`id.layer_local_c`. We report the overlap with (a) the whole KSSL catalogue in the OSSL and (b) the development layers.
"""
import json

import numpy as np
import pandas as pd

from experiments.confirm import NS
from src.data.soil import FILES, RAW


def _lid(s):
    return s.astype(str).str.replace(r"\.0$", "", regex=True)


def main():
    head = pd.read_csv(RAW / FILES[2], nrows=1)
    spec = [c for c in head.columns if c.startswith("scan_visnir.")]
    wl = np.array([int(c.split(".")[1].split("_")[0]) for c in spec])
    keep = [c for c, w in zip(spec, wl) if 400 <= w <= 2500 and w % 10 == 0]
    v = pd.read_csv(RAW / FILES[2], usecols=["dataset.code_ascii_txt", "id.layer_uuid_txt"] + keep, low_memory=False)
    v = v[v["dataset.code_ascii_txt"] == "KSSL.SSL"]
    site = pd.read_csv(RAW / FILES[0], usecols=["dataset.code_ascii_txt", "id.layer_uuid_txt", "id.layer_local_c"], low_memory=False)
    lab = pd.read_csv(RAW / FILES[1], usecols=["id.layer_uuid_txt", "c.tot_usda.a622_w.pct"], low_memory=False)
    dev = v.dropna(subset=keep)[["id.layer_uuid_txt"]].merge(lab, on="id.layer_uuid_txt", how="left")
    dev = dev[dev["c.tot_usda.a622_w.pct"].notna()].merge(site, on="id.layer_uuid_txt", how="left")
    cat = set(_lid(site.loc[site["dataset.code_ascii_txt"] == "KSSL.SSL", "id.layer_local_c"]))
    dev_ids = set(_lid(dev["id.layer_local_c"]))
    ns = set(_lid(pd.read_csv(NS, usecols=["lay_id"])["lay_id"]))
    ov_cat, ov_dev = ns & cat, ns & dev_ids
    out = dict(neospectra_layers=len(ns), kssl_catalogue_layers=len(cat), overlap_with_catalogue=len(ov_cat),
               overlap_share_catalogue=len(ov_cat) / len(ns), kssl_development_layers=len(dev_ids),
               overlap_with_development=len(ov_dev), overlap_share_development=len(ov_dev) / len(ns))
    json.dump(out, open("results/cycle3/neospectra_overlap.json", "w"), indent=1)
    pd.Series(sorted(ov_dev), dtype=str).to_csv("results/cycle3/neospectra_overlap_ids.csv", index=False, header=["lay_id"])
    print(out)


if __name__ == "__main__":
    main()
