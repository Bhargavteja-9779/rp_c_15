#!/usr/bin/env python
"""G8 leakage audit (writes results/leakage_audit.json). Checks, for every forward-chaining target season:
  1. no physical sample (reference_no) appears in both source and target,
  2. no lot (population) appears in both source and target, and no season >= target in the source,
  3. exact-duplicate spectra shared between source and target (counted; reported),
  4. inside the source, sample-, lot- and season-grouped folds never split a group,
  5. preprocessing is row-wise (SNV, Savitzky-Golay): verified by recomputing a subset row by row.
"""
import hashlib
import json

import numpy as np

from src.data.dataset import load_data
from src.preprocessing.spectral import snv_sg
from src.training.crossfit import pred_path
from src.utils import ROOT, load_config

cfg = load_config()
d = load_data(cfg)
out = {}
h = np.array([hashlib.md5(r.tobytes()).hexdigest() for r in np.round(d.X, 6)])
for t in cfg["protocols"]["forward"]["targets"]:
    P = np.load(pred_path(cfg, "pls", 0, "forward", t))
    s, g = P["src_idx"], P["tgt_idx"]
    res = {
        "shared_samples": int(len(np.intersect1d(d.sample[s], d.sample[g]))),
        "shared_lots": int(len(np.intersect1d(d.lot[s], d.lot[g]))),
        "max_source_season": int(d.season[s].max()),
        "identical_spectra_source_target": int(len(np.intersect1d(h[s], h[g]))),
    }
    for scheme, groups in (("sample", d.sample[s]), ("lot", d.lot[s]), ("season", d.season[s])):
        f = P[f"fold_{scheme}"]
        split = 0
        for gid in np.unique(groups):
            split += len(np.unique(f[groups == gid])) > 1
        res[f"groups_split_by_{scheme}_folds"] = int(split)
    out[str(t)] = res
X = d.X[:200]
out["preprocessing_rowwise"] = bool(np.allclose(snv_sg(X)[:50], snv_sg(X[:50])))
ok = all(v["shared_samples"] == 0 and v["shared_lots"] == 0 and v["max_source_season"] < int(k) and
         all(v[f"groups_split_by_{s}_folds"] == 0 for s in ("sample", "lot", "season")) for k, v in out.items() if k.isdigit())
out["pass"] = bool(ok and out["preprocessing_rowwise"])
(ROOT / "results" / "leakage_audit.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
