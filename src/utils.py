"""Shared utilities: configuration, seeding, device detection, logging."""
from __future__ import annotations

import copy
import json
import logging
import os
import random
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]


def _deep_update(base: dict, upd: dict) -> dict:
    for k, v in upd.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_update(base[k], v)
        else:
            base[k] = v
    return base


def load_config(mode: str = "full") -> dict:
    """Load `config/default.yaml`; in quick mode overlay `config/quick.yaml`."""
    with open(ROOT / "config" / "default.yaml") as fh:
        cfg = yaml.safe_load(fh)
    if mode == "quick":
        with open(ROOT / "config" / "quick.yaml") as fh:
            cfg = _deep_update(copy.deepcopy(cfg), yaml.safe_load(fh))
    cfg["mode"] = mode
    return cfg


def out_dir(cfg: dict, name: str) -> Path:
    """Output directory; quick-mode outputs are kept apart from the reported results."""
    base = ROOT if cfg["mode"] == "full" else ROOT / "quick_outputs"
    p = base / name
    p.mkdir(parents=True, exist_ok=True)
    return p


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import torch

        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:  # torch is only needed for the CNN models
        pass


def get_device() -> str:
    """CUDA > Apple-silicon MPS > CPU, detected at run time."""
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
            return "mps"
    except ImportError:
        pass
    return "cpu"


def get_logger(name: str, cfg: dict | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    if cfg is not None:
        fh = logging.FileHandler(out_dir(cfg, "results/experiment_logs") / f"{name}.log")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


def save_json(obj, path: Path) -> None:
    def _default(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1, default=_default)
