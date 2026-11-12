import numpy as np

from src.evaluation.conformal import (hier_weights, interval_score, sample_weights, split_quantile,
                                      weighted_cp_halfwidths, weighted_quantile)
from src.evaluation.lotcp import LotCP, variance_components, _build_lots


def test_split_quantile_matches_definition():
    rng = np.random.default_rng(0)
    s = rng.normal(size=99)
    assert split_quantile(s, 0.1) == np.sort(s)[int(np.ceil(100 * 0.9)) - 1]
    assert np.isinf(split_quantile(s[:5], 0.1))          # too few points -> infinite interval


def test_weighted_quantile_uniform_equals_split():
    s = np.random.default_rng(1).normal(size=200)
    assert weighted_quantile(s, np.full(200, 3.0), 0.9, inf_mass=3.0) == split_quantile(s, 0.1)


def test_weights_sum():
    lot = np.array([1, 1, 1, 2, 2, 2, 2]); sample = np.array([1, 1, 2, 5, 6, 6, 6])
    w = hier_weights(lot, sample)
    assert np.allclose([w[lot == 1].sum(), w[lot == 2].sum()], 1.0)
    assert np.allclose(w, [0.25, 0.25, 0.5, 0.5, 1 / 6, 1 / 6, 1 / 6])
    assert np.isclose(sample_weights(sample[lot == 2]).sum(), 1.0)


def test_interval_score():
    assert interval_score(np.array([0.0]), np.array([1.0]), np.array([2.0]), 0.1)[0] == 1 + 20


def test_weighted_cp_reduces_to_split_with_unit_weights():
    s = np.random.default_rng(2).random(50)
    assert np.allclose(weighted_cp_halfwidths(s, np.ones(50), np.ones(3), 0.1), split_quantile(s, 0.1))


def _simulate(rng, n_lots, tau, sigma, n_s=30, n_rep=2):
    r, lot, sample = [], [], []
    sid = 0
    for l in range(n_lots):
        b = rng.normal(0, tau)
        for _ in range(n_s):
            e = b + rng.normal(0, sigma)
            for _ in range(n_rep):
                r.append(e + rng.normal(0, 0.2)); lot.append(l); sample.append(sid)
            sid += 1
    return np.array(r), np.array(lot), np.array(sample)


def test_variance_components_recover_truth():
    r, lot, sample = _simulate(np.random.default_rng(3), 400, tau=1.0, sigma=0.5)
    mu, tau2, sigma2 = variance_components(_build_lots(r, lot, sample))
    assert abs(mu) < 0.15 and abs(tau2 - 1.0) < 0.2 and abs(sigma2 - (0.25 + 0.04 / 2)) < 0.05


def test_lotcp_marginal_coverage_on_exchangeable_lots():
    """Monte-Carlo check of the guarantee: coverage >= 1 - alpha for new exchangeable lots, all m."""
    rng = np.random.default_rng(4)
    alpha = 0.1
    for m in (0, 3, 10):
        cov = []
        for rep in range(40):
            r, lot, sample = _simulate(rng, 60, tau=1.0, sigma=0.6)
            cp = LotCP(m=m, alpha=alpha, n_episodes=10, seed=rep).fit(r, lot, sample)
            rt, lt, st = _simulate(rng, 40, tau=1.0, sigma=0.6)
            for l in np.unique(lt):
                L = _build_lots(rt[lt == l], lt[lt == l], st[lt == l])[0]
                sup = rng.choice(len(L.s_mean), m, replace=False)
                b, q = cp.predict(L.s_mean[sup])
                qrows = ~np.isin(L.s_inv, sup)
                cov.append(np.mean(np.abs(L.r[qrows] - b) <= q))
        assert np.mean(cov) > 1 - alpha - 0.01, (m, np.mean(cov))
        assert np.mean(cov) < 1 - alpha + 0.04, (m, np.mean(cov))       # not grossly conservative


def test_lotcp_intervals_shrink_with_m():
    r, lot, sample = _simulate(np.random.default_rng(5), 150, tau=1.0, sigma=0.5)
    q = [LotCP(m=m, alpha=0.1, n_episodes=10).fit(r, lot, sample).q for m in (0, 5, 20)]
    assert q[0] > q[1] > q[2]


def test_lotcp_s_coverage_with_heteroscedastic_lots():
    """Lots differ in scan noise; LotCP-S must keep marginal coverage and reduce the spread of
    lot-wise coverage relative to the location-only variant."""
    rng = np.random.default_rng(6)

    def sim(n_lots):
        r, p, lot, sample, sid = [], [], [], [], 0
        for l in range(n_lots):
            b, noise = rng.normal(0, 1.0), rng.choice([0.2, 1.2])
            for _ in range(30):
                u = rng.normal(0, 0.5)
                for _ in range(3):
                    e = rng.normal(0, noise)
                    r.append(b + u + e); p.append(-e); lot.append(l); sample.append(sid)   # pred = y - r
                sid += 1
        return map(np.array, (r, p, lot, sample))

    r, p, lot, sample = sim(200)
    rt, pt, lt, st = sim(200)
    out = {}
    for mode in ("none", "full"):
        cp = LotCP(m=5, alpha=0.1, n_episodes=10, scale=mode).fit(r, lot, sample, p)
        cov = []
        for l in np.unique(lt):
            k = lt == l
            L = _build_lots(rt[k], lt[k], st[k], pt[k])[0]
            sup = rng.choice(len(L.s_mean), 5, replace=False)
            b, q = cp.predict(L.s_mean[sup], L.rep_var)
            cov.append(np.mean(np.abs(L.r[~np.isin(L.s_inv, sup)] - b) <= q))
        out[mode] = np.array(cov)
    assert abs(out["full"].mean() - 0.9) < 0.03 and abs(out["none"].mean() - 0.9) < 0.03
    assert out["full"].std() < 0.6 * out["none"].std()


def test_eval_metrics_and_aci():
    from src.evaluation.conformal import aci_alpha
    from src.evaluation.run_eval import _metrics

    r = np.array([0.0, 1.0, -3.0, 0.5]); w = np.full(4, 0.25)
    cov, width, isc = _metrics(r, 0.0, 1.0, w, 0.1, 0.1)
    assert cov == 0.75 and width == 2.0
    assert np.isclose(isc, 2.0 + 0.25 * (2 / 0.1) * 2.0)           # one miss by 2 units
    cov_b, _, _ = _metrics(r + 5.0, 5.0, 1.0, w, 0.1, 0.1)         # a bias correction shifts the interval
    assert cov_b == cov
    cal = np.sort(np.abs(np.random.default_rng(0).normal(size=500)))
    wide = aci_alpha(cal, [np.array([10.0])] * 20, 0.1)             # always missed -> interval must grow
    narrow = aci_alpha(cal, [np.array([0.0])] * 20, 0.1)            # always covered -> interval shrinks
    assert wide > split_quantile(cal, 0.1) > narrow


def test_split_constants_keeps_coverage():
    rng = np.random.default_rng(8)
    r, lot, sample = _simulate(rng, 200, tau=1.0, sigma=0.6)
    cp = LotCP(m=5, alpha=0.1, n_episodes=10, split_constants=True).fit(r, lot, sample)
    assert cp.info["n_cal_lots"] == 100
    rt, lt, st = _simulate(rng, 200, tau=1.0, sigma=0.6)
    cov = []
    for l in np.unique(lt):
        L = _build_lots(rt[lt == l], lt[lt == l], st[lt == l])[0]
        sup = rng.choice(len(L.s_mean), 5, replace=False)
        b, q = cp.predict(L.s_mean[sup])
        cov.append(np.mean(np.abs(L.r[~np.isin(L.s_inv, sup)] - b) <= q))
    assert abs(np.mean(cov) - 0.9) < 0.03
