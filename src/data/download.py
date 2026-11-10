"""Download the public mango NIR data set (Mendeley Data, CC BY 4.0) and verify its checksum."""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

from src.utils import ROOT, get_logger, load_config


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_raw(cfg: dict) -> Path:
    log = get_logger("download")
    path = ROOT / cfg["data"]["raw_file"]
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        log.info("downloading %s", cfg["data"]["url"])
        urllib.request.urlretrieve(cfg["data"]["url"], path)
    digest = sha256_of(path)
    if digest != cfg["data"]["sha256"]:
        raise RuntimeError(
            f"checksum mismatch for {path}: got {digest}, expected {cfg['data']['sha256']}. "
            "The data provider may have released a new version; results would not be comparable."
        )
    return path


if __name__ == "__main__":
    print(ensure_raw(load_config()))
