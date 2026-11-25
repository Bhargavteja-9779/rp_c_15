"""LotCP: lot-exchangeable few-shot conformal calibration (the proposed method).

Given residuals of *past* lots that were produced by models which had not seen the lot's season
(season-held-out residuals), LotCP
  1. estimates between-lot (tau^2) and within-lot (sigma^2) variance components of the bias,
  2. corrects a new lot's bias by the mean residual of m reference samples, b_hat = rbar_support
     (optionally, shrink=True, by the empirical-Bayes shrinkage
     b_hat = mu + w_m * (rbar_support - mu),  w_m = tau^2 / (tau^2 + sigma^2 / m); this pre-specified
     variant proved immaterial on the mango data and harmful under a large campaign shift),
  2b. (LotCP-S) rescales the score by a lot-specific scale built from the variance of the m
     reference residuals (shrunk to the prior) and the label-free variance of repeated-scan
     predictions in the lot,
  3. obtains the interval half-width by *replaying* exactly that m-shot procedure on every past
     lot (episodes) and taking a lot-balanced conformal quantile of |r - b_hat|.
With `assure=delta` (LotCP-A) step 3 instead takes the (1 - delta) quantile over past lots of each
lot's own (1 - alpha) score quantile, so that the realised coverage *within* a new lot is at least
1 - alpha with probability >= 1 - delta over lots.
Under exchangeability of lots (and of samples within lots) step 3 yields marginal coverage
>= 1 - alpha for a random sample of a new lot, for every m, because the m-shot score of the test
lot is exchangeable with the m-shot scores of the calibration lots.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from src.evaluation.conformal import weighted_quantile


@dataclass
class _Lot:
    r: np.ndarray            # spectrum-level residuals
    s_inv: np.ndarray        # sample index (0..n_s-1) of every spectrum
    s_mean: np.ndarray       # per-sample mean residual
    s_cnt: np.ndarray        # spectra per sample
    rep_var: float = np.nan  # label-free: pooled within-sample variance of repeated-scan predictions


def replicate_variance(pred: np.ndarray, s_inv: np.ndarray) -> float:
    """Pooled within-sample variance of the predictions of repeated scans (needs no reference value)."""
    cnt = np.bincount(s_inv)
    mean = np.bincount(s_inv, weights=pred) / cnt
    dof = int((cnt - 1).sum())
    return float(((pred - mean[s_inv]) ** 2).sum() / dof) if dof > 0 else float("nan")


def _build_lots(r, lot, sample, pred=None):
    lots = []
    for l in np.unique(lot):
        idx = np.flatnonzero(lot == l)
        _, inv, cnt = np.unique(sample[idx], return_inverse=True, return_counts=True)
        rv = replicate_variance(pred[idx], inv) if pred is not None else np.nan
        lots.append(_Lot(r[idx], inv, np.bincount(inv, weights=r[idx]) / cnt, cnt, rv))
    return lots


def variance_components(lots):
    """One-way random-effects moments on per-sample mean residuals: (mu, tau2, sigma2)."""
    lots = [L for L in lots if len(L.s_mean) >= 2]
    means = np.array([L.s_mean.mean() for L in lots])
    n = np.array([len(L.s_mean) for L in lots])
    sigma2 = sum(((L.s_mean - L.s_mean.mean()) ** 2).sum() for L in lots) / (n - 1).sum()
    tau2 = max(means.var(ddof=1) - sigma2 * np.mean(1.0 / n), 0.0)
    return float(means.mean()), float(tau2), float(sigma2)


@dataclass
class LotCP:
    m: int
    alpha: float
    n_episodes: int = 30
    min_query: int = 10
    shrink: bool = False       # True: empirical-Bayes shrinkage of the bias (ablation; see protocol deviation D5)
    episodic: bool = True      # False: quantile of oracle-centred within-lot residuals
    lot_balanced: bool = True  # False: every spectrum weighted equally
    scale: str = "none"        # 'none' | 'support' | 'rep' | 'full' (lot-specific score scale)
    nu_grid: tuple = (5, 10, 20, 40)
    assure: float | None = None     # delta: calibrate so that a lot's realised coverage is >= 1 - alpha with prob. >= 1 - delta
    side: str = "two"               # 'two': |r - b| / s (interval);  'lower': (b - r) / s (one-sided lower bound)
    split_constants: bool = False   # True: constants from one random half of the lots, quantile from the other
    seed: int = 0
    info: dict = field(default_factory=dict)

    # ---- pieces used both in calibration episodes and at deployment -------------------------
    def bias(self, support_sample_means: np.ndarray) -> float:
        if self.m == 0:
            return self.mu
        return self.mu + self.w * (float(np.mean(support_sample_means)) - self.mu)

    def lot_scale(self, support_sample_means: np.ndarray, rep_var: float, nu0: float | None) -> float:
        """Lot-specific residual scale s_hat with s_hat^2 = u2 + e2.

        u2: between-sample variance; prior sigma^2, updated with the variance of the m reference
            residual means (pseudo-count nu0) when scale in {'support', 'full'} and m >= 2.
        e2: scan-level variance; the lot's own replicate-prediction variance (label-free) when
            scale in {'rep', 'full'} and the lot has repeated scans, else the prior e0.
        """
        u2 = self.sigma2
        if self.scale in ("support", "full") and self.m >= 2:
            ss = float(np.var(support_sample_means, ddof=1)) * (self.m - 1)
            u2 = (nu0 * self.sigma2 + ss) / (nu0 + self.m - 1)
        e2 = rep_var if (self.scale in ("rep", "full") and np.isfinite(rep_var)) else self.e0
        return float(np.sqrt(u2 + e2))

    # ---- calibration ---------------------------------------------------------------------
    def fit(self, r, lot, sample, pred=None):
        lots = _build_lots(np.asarray(r, float), np.asarray(lot), np.asarray(sample), pred)
        const_lots = lots
        if self.split_constants:                    # sample splitting removes any reuse of calibration lots
            perm = np.random.default_rng(self.seed + 991).permutation(len(lots))
            const_lots = [lots[i] for i in perm[: len(lots) // 2]]
            lots = [lots[i] for i in perm[len(lots) // 2:]]
        self.mu, self.tau2, self.sigma2 = variance_components(const_lots)
        rv = np.array([L.rep_var for L in const_lots])
        self.e0 = float(np.nanmean(rv)) if np.isfinite(rv).any() else 0.0
        if self.m == 0:
            self.w = 0.0
        elif not self.shrink:
            self.w = 1.0
        else:
            self.w = self.tau2 / (self.tau2 + self.sigma2 / self.m) if self.tau2 > 0 else 0.0
        usable = [L for L in lots if len(L.s_mean) >= self.m + self.min_query]
        self.info.update(n_cal_lots=len(usable), mu=self.mu, tau2=self.tau2, sigma2=self.sigma2, w=self.w)
        if not self.episodic:
            # ablation: no replay of the m-shot procedure; each past lot is standardised with its OWN full-information
            # bias (and, if scaled, its own scale from all samples), i.e. the estimation error at m is ignored
            sc, wt = [], []
            self.nu0 = 10 if self.scale in ("support", "full") else None
            for L in usable:
                s_hat = self.lot_scale(L.s_mean, L.rep_var, self.nu0) if self.scale != "none" else 1.0
                sc.append(np.abs(L.r - L.s_mean.mean()) / s_hat)
                wt.append(self._w_query(L, np.ones(len(L.s_mean), bool)))
            sc, wt = np.concatenate(sc), np.concatenate(wt)
            self.q = weighted_quantile(sc, wt, 1 - self.alpha, inf_mass=1.0)
            self.planned_width = 2.0 * self.q
            return self
        rng = np.random.default_rng(self.seed)
        episodes = []                               # (lot object, support sample indices)
        for L in usable:
            n_ep = 1 if self.m == 0 else self.n_episodes
            for _ in range(n_ep):
                episodes.append((L, rng.choice(len(L.s_mean), self.m, replace=False), 1.0 / n_ep))
        best = None
        scaled = self.scale != "none"
        grid = self.nu_grid if not self.split_constants else (10,)      # no data-driven choice when splitting
        for nu0 in (grid if self.scale in ("support", "full") and self.m >= 2 else (None,)):
            sc, wt, scales, lotq, lotw = [], [], [], [], []
            for L, sup, ep_w in episodes:
                qmask = np.ones(len(L.s_mean), bool)
                qmask[sup] = False
                b = self.bias(L.s_mean[sup])
                s_hat = self.lot_scale(L.s_mean[sup], L.rep_var, nu0) if scaled else 1.0
                rows = qmask[L.s_inv]
                e = L.r[rows] - b
                sc.append((np.abs(e) if self.side == "two" else -e) / s_hat)
                wt.append(self._w_query(L, qmask)[rows] * ep_w)
                scales.append(s_hat)
                if self.assure is not None:          # the lot's own (1 - alpha) score quantile in this episode
                    lotq.append(weighted_quantile(sc[-1], wt[-1], 1 - self.alpha))
                    lotw.append(ep_w)
            if self.assure is None:
                q = weighted_quantile(np.concatenate(sc), np.concatenate(wt), 1 - self.alpha, inf_mass=1.0)
            else:                                    # (1 - delta) quantile over lots of the lot-wise quantiles
                q = weighted_quantile(np.array(lotq), np.array(lotw), 1 - self.assure, inf_mass=1.0)
            width = q * float(np.mean(scales))
            if best is None or width < best[0]:
                best = (width, nu0, q)
        _, self.nu0, self.q = best
        self.planned_width = 2.0 * best[0]          # expected interval width at this m, known before deployment
        self.info.update(q=self.q, nu0=self.nu0, e0=self.e0)
        return self

    def _w_query(self, L: _Lot, qmask: np.ndarray) -> np.ndarray:
        """Row weights for one lot (total mass 1 over the query spectra)."""
        if self.lot_balanced:
            return 1.0 / (qmask.sum() * L.s_cnt[L.s_inv])
        return np.ones(len(L.r))                      # ablation: every spectrum has unit mass

    def group_quantiles(self, r, lot, sample, pred, group, n_episodes=None, seed=0, plain=False):
        """Season-robust replay (plan_v7): with the FITTED constants (mu, sigma2, e0, nu0, scale) frozen, replay the m-shot
        procedure separately within each group of calibration lots (e.g. a harvest season) and return
        {group: multiplier}. For assure=None the multiplier is the group's lot-balanced (1 - alpha) score quantile;
        for assure=delta it is the group's (1 - delta) quantile of lot-wise (1 - alpha) quantiles. Groups are thereby
        scored with one common score function, so under exchangeable groups the k-th largest of S group multipliers
        exceeds a new group's multiplier with probability >= (S + 1 - k) / (S + 1) (Appendix A, Proposition 3)."""
        rng = np.random.default_rng(seed)
        n_ep = n_episodes or self.n_episodes
        out = {}
        r, lot, sample, group = np.asarray(r, float), np.asarray(lot), np.asarray(sample), np.asarray(group)
        for g in np.unique(group):
            k = group == g
            lots = [L for L in _build_lots(r[k], lot[k], sample[k], None if pred is None else np.asarray(pred)[k])
                    if len(L.s_mean) >= self.m + self.min_query]
            if not lots:
                continue
            sc, wt, lotq, lotw = [], [], [], []
            for L in lots:
                ne = 1 if self.m == 0 else n_ep
                for _ in range(ne):
                    sup = rng.choice(len(L.s_mean), self.m, replace=False)
                    qmask = np.ones(len(L.s_mean), bool); qmask[sup] = False
                    b = self.bias(L.s_mean[sup])
                    s_hat = self.lot_scale(L.s_mean[sup], L.rep_var, self.nu0) if self.scale != "none" else 1.0
                    rows = qmask[L.s_inv]
                    e = L.r[rows] - b
                    s_ = (np.abs(e) if self.side == "two" else -e) / s_hat
                    w_ = self._w_query(L, qmask)[rows] / ne
                    sc.append(s_); wt.append(w_)
                    if self.assure is not None:
                        lotq.append(weighted_quantile(s_, w_, 1 - self.alpha)); lotw.append(1.0 / ne)
            # default: the group's own CONFORMAL quantile (one extra lot of mass at +inf), i.e. the multiplier that would be
            # valid for a new lot exchangeable with the lots of that group (pre-specified, plan_v7). plain=True gives the
            # plain empirical quantile (sensitivity analysis). Both satisfy Proposition 3; the default is more conservative.
            im = 0.0 if plain else 1.0
            if self.assure is None:
                out[g] = weighted_quantile(np.concatenate(sc), np.concatenate(wt), 1 - self.alpha, inf_mass=im)
            else:
                out[g] = weighted_quantile(np.array(lotq), np.array(lotw), 1 - self.assure, inf_mass=im)
        return out

    # ---- deployment ------------------------------------------------------------------------
    def predict(self, support_sample_means: np.ndarray, rep_var: float = np.nan):
        """Return (bias correction, half-width) for a new lot given its m reference residual means
        and, optionally, the replicate-prediction variance of the lot's scans."""
        b = self.bias(support_sample_means)
        s_hat = self.lot_scale(support_sample_means, rep_var, self.nu0) if self.scale != "none" else 1.0
        return b, self.q * s_hat
