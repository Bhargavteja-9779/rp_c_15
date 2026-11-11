import numpy as np
import pandas as pd

from src.preprocessing.spectral import snv, snv_sg
from src.training.splits import fold_ids, protocol_masks


def _toy(n=600, seed=0):
    rng = np.random.default_rng(seed)
    season = rng.integers(2015, 2019, n)
    lot = season * 100 + rng.integers(0, 6, n)
    sample = lot * 100 + rng.integers(0, 15, n)
    return season, lot, sample


def test_forward_protocol_never_uses_future_seasons():
    season, _, _ = _toy()
    src, tgt = protocol_masks(season, "forward", 2017)
    assert season[src].max() < 2017 and set(season[tgt]) == {2017} and not (src & tgt).any()
    src, tgt = protocol_masks(season, "recent2", 2018)
    assert set(season[src]) == {2016, 2017}
    src, tgt = protocol_masks(season, "loso", 2016)
    assert 2016 not in set(season[src])


def test_group_protocols():
    meta = pd.DataFrame({"region": ["NT", "QLD", "NT"], "cultivar": ["kp", "kp", "caly"]})
    src, tgt = protocol_masks(np.zeros(3), "region", "QLD", meta)
    assert tgt.tolist() == [False, True, False] and src.tolist() == [True, False, True]


def test_folds_are_grouped():
    season, lot, sample = _toy()
    for scheme, groups in (("sample", sample), ("lot", lot), ("season", season)):
        f = fold_ids(scheme, sample, lot, season, k=5, seed=3)
        per_group = pd.Series(f).groupby(groups).nunique()
        assert per_group.max() == 1, scheme            # a group never straddles two folds
    # a sample-grouped split also never splits the repeated scans of one sample
    f = fold_ids("sample", sample, lot, season, k=5, seed=3)
    assert len(np.unique(f)) == 5
    assert (fold_ids("sample", sample, lot, season, 5, seed=3) == f).all()   # deterministic


def test_snv_is_rowwise():
    X = np.random.default_rng(0).random((4, 40))
    Z = snv(X)
    assert np.allclose(Z.mean(1), 0) and np.allclose(Z.std(1), 1)
    assert np.allclose(snv(X[:2]), Z[:2])               # no statistics shared between rows
    assert snv_sg(X).shape == X.shape
