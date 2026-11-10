"""LotCP: lot-exchangeable few-shot conformal calibration (the proposed method).

Given residuals of *past* lots that were produced by models which had not seen the lot's season
(season-held-out residuals), LotCP
  1. estimates between-lot (tau^2) and within-lot (sigma^2) variance components of the bias,
  2. corrects a new lot's bias by an empirical-Bayes shrinkage of the mean residual of m
     reference samples:  b_hat = mu + w_m * (rbar_support - mu),  w_m = tau^2 / (tau^2 + sigma^2 / m),
  2b. (LotCP-S) rescales the score by a lot-specific scale built from the variance of the m
     reference residuals (shrunk to the prior) and the label-free variance of repeated-scan
     predictions in the lot,
  3. obtains the interval half-width by *replaying* exactly that m-shot procedure on every past
     lot (episodes) and taking a lot-balanced conformal quantile of |r - b_hat|.
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
    shrink: bool = True        # False: plain mean bias correction (w = 1)
    episodic: bool = True      # False: quantile of oracle-centred within-lot residuals
    lot_balanced: bool = True  # False: every spectrum weighted equally
    scale: str = "none"        # 'none' | 'support' | 'rep' | 'full' (lot-specific score scale)
    nu_grid: tuple = (5, 10, 20, 40)
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
        self.mu, self.tau2, self.sigma2 = variance_components(lots)
        rv = np.array([L.rep_var for L in lots])
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
            sc = np.concatenate([np.abs(L.r - L.s_mean.mean()) for L in usable])
            wt = np.concatenate([self._w_query(L, np.ones(len(L.s_mean), bool)) for L in usable])
            self.nu0, self.q = None, weighted_quantile(sc, wt, 1 - self.alpha, inf_mass=1.0)
            return self
        rng = np.random.default_rng(self.seed)
        episodes = []                               # (lot object, support sample indices)
        for L in usable:
            n_ep = 1 if self.m == 0 else self.n_episodes
            for _ in range(n_ep):
                episodes.append((L, rng.choice(len(L.s_mean), self.m, replace=False), 1.0 / n_ep))
        best = None
        scaled = self.scale != "none"
        for nu0 in (self.nu_grid if self.scale in ("support", "full") and self.m >= 2 else (None,)):
            sc, wt, scales = [], [], []
            for L, sup, ep_w in episodes:
                qmask = np.ones(len(L.s_mean), bool)
                qmask[sup] = False
                b = self.bias(L.s_mean[sup])
                s_hat = self.lot_scale(L.s_mean[sup], L.rep_var, nu0) if scaled else 1.0
                rows = qmask[L.s_inv]
                sc.append(np.abs(L.r[rows] - b) / s_hat)
                wt.append(self._w_query(L, qmask)[rows] * ep_w)
                scales.append(s_hat)
            q = weighted_quantile(np.concatenate(sc), np.concatenate(wt), 1 - self.alpha, inf_mass=1.0)
            width = q * float(np.mean(scales))
            if best is None or width < best[0]:
                best = (width, nu0, q)
        _, self.nu0, self.q = best
        self.info.update(q=self.q, nu0=self.nu0, e0=self.e0)
        return self

    def _w_query(self, L: _Lot, qmask: np.ndarray) -> np.ndarray:
        """Row weights for one lot (total mass 1 over the query spectra)."""
        if self.lot_balanced:
            return 1.0 / (qmask.sum() * L.s_cnt[L.s_inv])
        return np.ones(len(L.r))                      # ablation: every spectrum has unit mass

    # ---- deployment ------------------------------------------------------------------------
    def predict(self, support_sample_means: np.ndarray, rep_var: float = np.nan):
        """Return (bias correction, half-width) for a new lot given its m reference residual means
        and, optionally, the replicate-prediction variance of the lot's scans."""
        b = self.bias(support_sample_means)
        s_hat = self.lot_scale(support_sample_means, rep_var, self.nu0) if self.scale != "none" else 1.0
        return b, self.q * s_hat
