"""Harvest decision-support prototype (command line).

Step 1 (once per season, by the calibration owner): export a calibration file from past lots.
    python -m src.tool.harvest_tool export --target-season 2021 --out calibration_2021.json
Step 2 (per lot, in the field or packhouse):
    python -m src.tool.harvest_tool decide --calibration calibration_2021.json \
        --scans lot_scans.csv --references lot_refs.csv --spec 15 --mode marginal|assured
  lot_scans.csv : columns fruit_id, prediction   (one row per scan; repeated scans of a fruit allowed)
  lot_refs.csv  : columns fruit_id, dry_matter   (oven-dry reference value of the m destructively tested fruit)
Output: per-fruit lower bound and decision (HARVEST / WAIT-RETEST), a lot recommendation, and the
planned interval width for other numbers of reference fruit (reference-sampling planner).
Step 3 (demonstration on a real held-out lot of the public data set):
    python -m src.tool.harvest_tool demo --target-season 2021 --spec 15 --m 10
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from src.evaluation.lotcp import LotCP, replicate_variance

M_GRID = (0, 3, 5, 10, 20, 30)


def export(target_season: int, out: Path, alpha: float = 0.1, delta: float = 0.1):
    """Calibrate on all seasons before `target_season` using stored season-held-out residuals."""
    from src.data.dataset import load_data
    from src.training.crossfit import pred_path
    from src.utils import load_config

    cfg = load_config()
    d = load_data(cfg)
    P = np.load(pred_path(cfg, "pls", 0, "forward", target_season))
    src = P["src_idx"]
    r = d.y[src] - P["oof_season"]
    cal = {"model": "PLS (SNV + SG 2nd derivative), trained on seasons before %d" % target_season, "alpha": alpha, "delta": delta, "levels": {}}
    for m in M_GRID:
        entry = {}
        for mode, kw in (("marginal", {}), ("assured", {"assure": delta})):
            cp = LotCP(m=m, alpha=alpha, scale="full", side="lower", seed=11 + m, **kw).fit(r, d.lot[src], d.sample[src], P["oof_season"])
            two = LotCP(m=m, alpha=alpha, scale="full", seed=11 + m, **kw).fit(r, d.lot[src], d.sample[src], P["oof_season"])
            entry[mode] = {"q_lower": cp.q, "q_two_sided": two.q, "planned_width": two.planned_width}
        entry["constants"] = {"mu": cp.mu, "sigma2": cp.sigma2, "e0": cp.e0, "nu0": cp.nu0}
        cal["levels"][str(m)] = entry
    out.write_text(json.dumps(cal, indent=1))
    return cal


def _scale(const, m, sup_means, rep_var):
    u2 = const["sigma2"]
    if m >= 2 and const["nu0"] is not None:
        ss = float(np.var(sup_means, ddof=1)) * (m - 1)
        u2 = (const["nu0"] * const["sigma2"] + ss) / (const["nu0"] + m - 1)
    e2 = rep_var if np.isfinite(rep_var) else const["e0"]
    return float(np.sqrt(u2 + e2))


def decide(cal: dict, scans: pd.DataFrame, refs: pd.DataFrame, spec: float, mode: str = "marginal", lot_share: float = 0.8):
    """Return (per-fruit table, lot summary dict)."""
    scans = scans.copy()
    fid, inv = np.unique(scans["fruit_id"].astype(str), return_inverse=True)
    rep_var = replicate_variance(scans["prediction"].to_numpy(float), inv)
    fruit = scans.groupby(scans["fruit_id"].astype(str))["prediction"].mean().rename("mean_prediction").reset_index()
    refs = refs.copy()
    refs["fruit_id"] = refs["fruit_id"].astype(str)
    sup = fruit.merge(refs, on="fruit_id", how="inner")
    m = len(sup)
    level = str(max([k for k in map(int, cal["levels"]) if k <= m]))
    lev = cal["levels"][level]
    resid = (sup["dry_matter"] - sup["mean_prediction"]).to_numpy(float)
    b = float(resid.mean()) if m > 0 else lev["constants"]["mu"]
    s_hat = _scale(lev["constants"], int(level), resid, rep_var)
    q = lev[mode]["q_lower"]
    query = fruit[~fruit["fruit_id"].isin(refs["fruit_id"])].copy()
    query["corrected_prediction"] = query["mean_prediction"] + b
    query["lower_bound"] = query["corrected_prediction"] - q * s_hat
    query["decision"] = np.where(query["lower_bound"] >= spec, "HARVEST", "WAIT-RETEST")
    share = float((query["decision"] == "HARVEST").mean()) if len(query) else 0.0
    summary = {
        "reference_fruit_used": m, "calibration_level_m": int(level), "mode": mode,
        "statement": (f"Each lower bound holds for at least {100 * (1 - cal['alpha']):.0f} % of fruit "
                      + ("on average over lots" if mode == "marginal" else f"in at least {100 * (1 - cal['delta']):.0f} % of lots")
                      + " (retrospective calibration; assumes the lot resembles past lots)."),
        "lot_bias_correction": round(b, 3), "lot_scale": round(s_hat, 3),
        "fruit_cleared_for_harvest": f"{100 * share:.0f} %",
        "lot_recommendation": "HARVEST" if share >= lot_share else "WAIT / RE-TEST",
        "planner_two_sided_width_by_m": {k: round(v[mode]["planned_width"], 2) for k, v in cal["levels"].items()},
    }
    return query, summary


def demo(target_season: int, spec: float, m: int, seed: int = 1, mode: str = "marginal"):
    """Run the tool on a real lot of `target_season` from the public data and compare with truth."""
    from src.data.dataset import load_data
    from src.training.crossfit import pred_path
    from src.utils import ROOT, load_config

    cfg = load_config()
    d = load_data(cfg)
    path = ROOT / "results" / f"calibration_{target_season}.json"
    cal = json.loads(path.read_text()) if path.exists() else export(target_season, path)
    P = np.load(pred_path(cfg, "pls", 0, "forward", target_season))
    tgt = P["tgt_idx"]
    lots, sizes = np.unique(d.lot[tgt], return_counts=True)
    lot = lots[np.argsort(-sizes)][len(lots) // 2]                       # a typical-size lot, chosen by rule, not by result
    li = tgt[d.lot[tgt] == lot]
    scans = pd.DataFrame({"fruit_id": d.sample[li], "prediction": P["pred_tgt"][d.lot[tgt] == lot]})
    ids = np.unique(d.sample[li])
    chosen = np.random.default_rng(seed).choice(ids, m, replace=False)
    truth = pd.DataFrame({"fruit_id": d.sample[li].astype(str), "dry_matter": d.y[li]}).drop_duplicates("fruit_id")
    refs = truth[truth["fruit_id"].isin(chosen.astype(str))]
    out, summary = decide(cal, scans, refs, spec, mode)
    out = out.merge(truth, on="fruit_id")
    acc = out["decision"] == "HARVEST"
    summary["demo_lot"] = int(lot)
    summary["demo_truth"] = {
        "fruit_evaluated": int(len(out)), "truly_compliant": f"{100 * (out.dry_matter >= spec).mean():.0f} %",
        "immature_among_harvested": f"{100 * (out.dry_matter[acc] < spec).mean():.0f} %" if acc.any() else "n/a",
        "lower_bound_coverage": f"{100 * (out.dry_matter >= out.lower_bound).mean():.0f} %",
    }
    return out, summary


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export"); e.add_argument("--target-season", type=int, required=True); e.add_argument("--out", type=Path, required=True)
    k = sub.add_parser("decide")
    for a in ("--calibration", "--scans", "--references"):
        k.add_argument(a, type=Path, required=True)
    k.add_argument("--spec", type=float, required=True); k.add_argument("--mode", default="marginal", choices=["marginal", "assured"])
    k.add_argument("--out", type=Path)
    dm = sub.add_parser("demo"); dm.add_argument("--target-season", type=int, default=2021); dm.add_argument("--spec", type=float, default=15.0)
    dm.add_argument("--m", type=int, default=10); dm.add_argument("--mode", default="marginal", choices=["marginal", "assured"])
    a = ap.parse_args()
    if a.cmd == "export":
        export(a.target_season, a.out); print("written", a.out)
    elif a.cmd == "decide":
        out, summary = decide(json.loads(a.calibration.read_text()), pd.read_csv(a.scans), pd.read_csv(a.references), a.spec, a.mode)
        if a.out:
            out.to_csv(a.out, index=False)
        print(json.dumps(summary, indent=1))
    else:
        out, summary = demo(a.target_season, a.spec, a.m, mode=a.mode)
        print(out.head(8).round(2).to_string(index=False)); print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
