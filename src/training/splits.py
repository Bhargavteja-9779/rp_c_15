"""Protocol splits and grouped fold assignment (a physical sample never straddles a split)."""
from __future__ import annotations

import numpy as np
from sklearn.model_selection import GroupKFold


def protocol_masks(season: np.ndarray, protocol: str, target: int):
    """Boolean (source, target) masks. forward: seasons < T train; loso: all other seasons train."""
    tgt = season == target
    if protocol == "forward":
        src = season < target
    elif protocol == "loso":
        src = season != target
    else:
        raise ValueError(protocol)
    return src, tgt


def fold_ids(scheme: str, sample: np.ndarray, lot: np.ndarray, season: np.ndarray, k: int, seed: int = 0) -> np.ndarray:
    """Fold index per row. scheme: 'sample' | 'lot' (shuffled GroupKFold) | 'season' (leave-one-season-out)."""
    if scheme == "season":
        _, f = np.unique(season, return_inverse=True)
        return f
    groups = sample if scheme == "sample" else lot
    uniq = np.unique(groups)
    rng = np.random.default_rng(seed)
    relabel = dict(zip(uniq, rng.permutation(len(uniq))))     # shuffle group order deterministically
    g = np.array([relabel[x] for x in groups])
    f = np.empty(len(g), dtype=int)
    for i, (_, te) in enumerate(GroupKFold(n_splits=k).split(g, groups=g)):
        f[te] = i
    return f
