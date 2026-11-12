"""Conformal primitives shared by all interval methods.

Conventions: residual r = y - yhat; an interval is [yhat + b - q, yhat + b + q] with bias
correction b and half-width q, so a point is covered iff |r - b| <= q.
"""
from __future__ import annotations

import numpy as np
from scipy.stats import norm


def weighted_quantile(scores: np.ndarray, weights: np.ndarray, level: float, inf_mass: float = 0.0) -> float:
    """Smallest s with sum_{s_i <= s} w_i >= level * (sum_i w_i + inf_mass); +inf if not attainable.

    With unit weights and inf_mass = 1 this is the usual split-conformal quantile
    ceil((n + 1) * level) / n; `inf_mass` is the mass placed on the unknown test score.
    """
    scores, weights = np.asarray(scores, float), np.asarray(weights, float)
    order = np.argsort(scores, kind="mergesort")
    cw = np.cumsum(weights[order])
    need = level * (cw[-1] + inf_mass)
    i = np.searchsorted(cw, need * (1 - 1e-12), side="left")
    return float(scores[order][i]) if i < len(scores) else float("inf")


def split_quantile(scores: np.ndarray, alpha: float) -> float:
    return weighted_quantile(scores, np.ones(len(scores)), 1 - alpha, inf_mass=1.0)


def hier_weights(lot: np.ndarray, sample: np.ndarray) -> np.ndarray:
    """Row weights for three-level data (lot > sample > spectrum): every lot has total mass 1,
    split equally over its samples and then over each sample's spectra (Lee et al. pooling)."""
    _, lot_inv = np.unique(lot, return_inverse=True)
    key = lot_inv.astype(np.int64) * (int(np.max(sample)) + 1) + sample.astype(np.int64)
    _, s_inv, s_cnt = np.unique(key, return_inverse=True, return_counts=True)
    first = np.zeros(len(s_cnt), dtype=np.int64)
    first[s_inv] = lot_inv                                    # lot of each (lot, sample) cell
    n_samples_per_lot = np.bincount(first)
    return 1.0 / (n_samples_per_lot[lot_inv] * s_cnt[s_inv])


def sample_weights(sample: np.ndarray) -> np.ndarray:
    """Within one lot: each sample has equal mass, split over its spectra; sums to 1."""
    _, inv, cnt = np.unique(sample, return_inverse=True, return_counts=True)
    return 1.0 / (len(cnt) * cnt[inv])


def gaussian_halfwidth(residuals: np.ndarray, alpha: float) -> float:
    """Chemometric practice: +- z * RMSECV."""
    return float(norm.ppf(1 - alpha / 2) * np.sqrt(np.mean(np.square(residuals))))


def interval_score(lo, hi, y, alpha):
    """Winkler interval score (lower is better); proper for central (1 - alpha) intervals."""
    return (hi - lo) + (2 / alpha) * np.maximum(lo - y, 0) + (2 / alpha) * np.maximum(y - hi, 0)


def weighted_cp_halfwidths(cal_scores, cal_w, test_w, alpha):
    """Weighted split conformal under covariate shift (Tibshirani et al., 2019).

    cal_w, test_w are likelihood-ratio weights; returns one half-width per test point."""
    order = np.argsort(cal_scores, kind="mergesort")
    s, cw = np.asarray(cal_scores)[order], np.cumsum(np.asarray(cal_w, float)[order])
    need = (1 - alpha) * (cw[-1] + np.asarray(test_w, float))
    i = np.searchsorted(cw, need, side="left")
    return np.where(i < len(s), s[np.minimum(i, len(s) - 1)], np.inf)


def density_ratio_weights(Z_src, Z_tgt, clip: float = 1e3):
    """Likelihood ratio w(x) = p_tgt(x) / p_src(x) from a probabilistic source-vs-target classifier."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    Z = np.vstack([Z_src, Z_tgt])
    lab = np.r_[np.zeros(len(Z_src)), np.ones(len(Z_tgt))]
    sc = StandardScaler().fit(Z)
    clf = LogisticRegression(C=1.0, class_weight="balanced", max_iter=500).fit(sc.transform(Z), lab)
    p = np.clip(clf.predict_proba(sc.transform(Z))[:, 1], 1e-6, 1 - 1e-6)
    w = np.clip(p / (1 - p), 1 / clip, clip)                 # balanced classes -> odds = density ratio
    return w[: len(Z_src)], w[len(Z_src):]


def aci_alpha(cal_scores_sorted, support_abs_resid_by_sample, alpha, gamma=0.05):
    """Adaptive conformal inference (Gibbs & Candes, 2021) run over the m reference samples.

    Starting from alpha, after every reference sample: alpha_t <- alpha_t + gamma * (alpha - err_t),
    where err_t is the share of that sample's spectra outside the current interval. Returns the
    half-width implied by the final alpha_t on the source calibration scores."""
    a, n = alpha, len(cal_scores_sorted)

    def q(a_):
        if a_ <= 0:
            return np.inf
        if a_ >= 1:
            return 0.0
        k = int(np.ceil((n + 1) * (1 - a_)))
        return cal_scores_sorted[k - 1] if k <= n else np.inf

    for s_abs in support_abs_resid_by_sample:
        err = float(np.mean(s_abs > q(a)))
        a = a + gamma * (alpha - err)
    return q(a)
