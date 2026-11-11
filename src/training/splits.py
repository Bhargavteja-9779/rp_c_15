"""Protocol splits and grouped fold assignment (a physical sample never straddles a split)."""
from __future__ import annotations

import numpy as np
from sklearn.model_selection import GroupKFold


def protocol_masks(season: np.ndarray, protocol: str, target, meta=None):
    """Boolean (source, target) masks.

    forward : seasons < T train, season T test (primary, deployment-realistic)
    loso    : all other seasons train (non-causal robustness check)
    recent2 : only the two seasons preceding T train
    region  : target = all lots of one growing region, source = the other region
    cultivar: target = all lots of one cultivar, source = all other cultivars
    """
    if protocol == "forward":
        return season < target, season == target
    if protocol == "loso":
        return season != target, season == target
    if protocol == "recent2":
        return (season < target) & (season >= target - 2), season == target
    if protocol in ("region", "cultivar"):
        col = meta[protocol].astype(str).to_numpy()
        return col != str(target), col == str(target)
    raise ValueError(protocol)


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
