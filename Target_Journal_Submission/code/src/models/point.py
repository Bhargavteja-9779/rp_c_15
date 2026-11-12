"""Point predictors. Every model exposes fit(X, y) and predict(X) on raw window absorbance."""
from __future__ import annotations

import numpy as np
from sklearn.cross_decomposition import PLSRegression

from src.preprocessing.spectral import snv, snv_sg
from src.utils import get_device, set_seed


class PLSModel:
    """SNV + Savitzky-Golay derivative followed by PLS regression (chemometric reference model)."""

    def __init__(self, n_components: int = 14, sg_window: int = 17, sg_poly: int = 2, sg_deriv: int = 2, **_):
        self.n_components = n_components
        self.sg = (sg_window, sg_poly, sg_deriv)

    def _prep(self, X):
        return snv_sg(X, *self.sg)

    def fit(self, X, y):
        self.model = PLSRegression(n_components=self.n_components, scale=False)
        self.model.fit(self._prep(X), y)
        return self

    def predict(self, X):
        return np.asarray(self.model.predict(self._prep(X))).ravel()

    def scores(self, X):
        """Latent scores, used as low-dimensional features by other components."""
        return self.model.transform(self._prep(X))


class GBMModel:
    """Gradient-boosted trees (LightGBM) on SNV + SG-derivative spectra."""

    def __init__(self, seed: int = 0, objective: str = "regression", alpha: float | None = None,
                 sg_window: int = 17, sg_poly: int = 2, sg_deriv: int = 2, **params):
        self.seed, self.objective, self.alpha = seed, objective, alpha
        self.sg = (sg_window, sg_poly, sg_deriv)
        self.params = {k: v for k, v in params.items() if k != "seeds"}

    def fit(self, X, y):
        import lightgbm as lgb

        kw = dict(objective=self.objective, random_state=self.seed, subsample_freq=1, verbose=-1, n_jobs=4, **self.params)
        if self.objective == "quantile":
            kw["alpha"] = self.alpha
        self.model = lgb.LGBMRegressor(**kw)
        self.model.fit(snv_sg(X, *self.sg), y)
        return self

    def predict(self, X):
        return self.model.predict(snv_sg(X, *self.sg))


def _build_cnn(p: int, dropout: float, n_out: int):
    import torch.nn as nn

    def out_len(n, k, s):
        return (n - k) // s + 1

    n = out_len(out_len(out_len(p, 7, 1), 5, 2), 3, 2)
    return nn.Sequential(
        nn.Conv1d(1, 16, 7), nn.ELU(),
        nn.Conv1d(16, 32, 5, stride=2), nn.ELU(),
        nn.Conv1d(32, 64, 3, stride=2), nn.ELU(),
        nn.Flatten(), nn.Linear(64 * n, 64), nn.ELU(), nn.Dropout(dropout), nn.Linear(64, n_out),
    )


class CNNModel:
    """Compact 1D-CNN on SNV spectra. `nll=True` adds a log-variance head (deep-ensemble member)."""

    def __init__(self, seed: int = 0, epochs: int = 30, batch_size: int = 256, lr: float = 1e-3,
                 weight_decay: float = 1e-4, dropout: float = 0.1, nll: bool = False, device: str | None = None, **_):
        self.seed, self.epochs, self.bs, self.lr, self.wd, self.dropout, self.nll = seed, epochs, batch_size, lr, weight_decay, dropout, nll
        self.device = device or get_device()

    def _prep(self, X):
        return ((snv(X) - self.mu) / self.sd).astype(np.float32)[:, None, :]

    def fit(self, X, y):
        import torch

        set_seed(self.seed)
        Z = snv(X)
        self.mu, self.sd = Z.mean(0), Z.std(0) + 1e-8
        self.ymu, self.ysd = float(np.mean(y)), float(np.std(y))
        Xt = torch.from_numpy(self._prep(X))
        yt = torch.from_numpy(((np.asarray(y) - self.ymu) / self.ysd).astype(np.float32))
        net = _build_cnn(X.shape[1], self.dropout, 2 if self.nll else 1).to(self.device)
        opt = torch.optim.AdamW(net.parameters(), lr=self.lr, weight_decay=self.wd)
        steps = self.epochs * int(np.ceil(len(Xt) / self.bs))
        sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=self.lr, total_steps=steps)
        g = torch.Generator().manual_seed(self.seed)
        self.history = []
        net.train()
        for _ in range(self.epochs):
            perm = torch.randperm(len(Xt), generator=g)
            tot = 0.0
            for i in range(0, len(Xt), self.bs):
                idx = perm[i:i + self.bs]
                xb, yb = Xt[idx].to(self.device), yt[idx].to(self.device)
                out = net(xb)
                if self.nll:
                    mean, logvar = out[:, 0], out[:, 1].clamp(-8, 6)
                    loss = (0.5 * (logvar + (yb - mean) ** 2 / logvar.exp())).mean()
                else:
                    loss = ((out[:, 0] - yb) ** 2).mean()
                opt.zero_grad()
                loss.backward()
                opt.step()
                sched.step()
                tot += loss.item() * len(idx)
            self.history.append(tot / len(Xt))
        self.net = net.eval()
        return self

    def _forward(self, X):
        import torch

        outs = []
        with torch.no_grad():
            Xt = torch.from_numpy(self._prep(X))
            for i in range(0, len(Xt), 4096):
                outs.append(self.net(Xt[i:i + 4096].to(self.device)).cpu().numpy())
        return np.concatenate(outs)

    def predict(self, X):
        return self._forward(X)[:, 0] * self.ysd + self.ymu

    def predict_dist(self, X):
        """Mean and variance in the original unit (only for nll=True)."""
        out = self._forward(X)
        return out[:, 0] * self.ysd + self.ymu, np.exp(np.clip(out[:, 1], -8, 6)) * self.ysd ** 2

    def predict_mc_dropout(self, X, passes: int = 30, seed: int = 0):
        """MC-dropout predictive mean and variance (Gal & Ghahramani, 2016); needs nll=True."""
        import torch

        torch.manual_seed(seed)
        self.net.train()                      # keeps dropout active; the network has no batch-norm
        means, vars_ = [], []
        for _ in range(passes):
            m, v = self.predict_dist(X)
            means.append(m); vars_.append(v)
        self.net.eval()
        means, vars_ = np.stack(means), np.stack(vars_)
        return means.mean(0), vars_.mean(0) + means.var(0)

    def n_params(self) -> int:
        return int(sum(p.numel() for p in self.net.parameters()))


def make_model(name: str, cfg: dict, seed: int = 0, **override):
    mc = dict(cfg["models"].get(name, {}))
    mc.update(override)
    if name == "pls":
        mc.pop("n_components_grid", None)
        return PLSModel(**mc)
    if name == "cnn":
        return CNNModel(seed=seed, **mc)
    if name == "gbm":
        return GBMModel(seed=seed, **mc)
    raise ValueError(name)
