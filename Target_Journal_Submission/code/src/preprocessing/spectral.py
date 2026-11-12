"""Row-wise spectral pre-treatments (no statistics are learned from data, hence no leakage)."""
from __future__ import annotations

import numpy as np
from scipy.signal import savgol_filter


def snv(X: np.ndarray) -> np.ndarray:
    """Standard normal variate: centre and scale every spectrum by its own mean / SD."""
    X = np.asarray(X, dtype=np.float64)
    mu = X.mean(axis=1, keepdims=True)
    sd = X.std(axis=1, keepdims=True)
    return (X - mu) / np.where(sd > 0, sd, 1.0)


def savgol(X: np.ndarray, window: int = 17, poly: int = 2, deriv: int = 2) -> np.ndarray:
    return savgol_filter(np.asarray(X, dtype=np.float64), window_length=window, polyorder=poly, deriv=deriv, axis=1)


def snv_sg(X: np.ndarray, window: int = 17, poly: int = 2, deriv: int = 2) -> np.ndarray:
    return savgol(snv(X), window, poly, deriv)
