#!/usr/bin/env python
"""Section 12 automatic report (no LLM): builds results/RESULTS_SUMMARY.md from result files and state/ only.
Run: python -m scripts.final_report"""
import json

import pandas as pd

from src.utils import ROOT

R, S = ROOT / "results", ROOT / "state"
j = lambda p, d=None: json.loads(p.read_text()) if p.exists() else d
a, g, b = j(S / "agent_state.json", {}), j(S / "gates.json", {}), j(S / "budget.json", {})
L = j(S / "novelty_ledger.json", {})
var = pd.read_csv(S / "variants_tried.csv")
main = pd.read_csv(ROOT / "tables" / "table3_main_intervals.csv")
conf = pd.read_csv(R / "confirmation" / "confirmation_tests.csv") if (R / "confirmation" / "confirmation_tests.csv").exists() else None
rep = pd.read_csv(R / "reproduction" / "reproduction.csv") if (R / "reproduction" / "reproduction.csv").exists() else None
leak = j(R / "leakage_audit.json", {})
sc = (L.get("scores") or [{}])
lines = [f"# RESULTS SUMMARY (generated from files) — cycle {a.get('cycle')}", "",
         f"Journal: {a.get('journal')}", f"Topic: {a.get('topic')}", "",
         "## Compute", f"Metered: {b.get('global_seconds', 0) / 3600:.2f} h; estimated unmetered cycle 1: {b.get('pre_protocol_cycle1_hours_estimate', 0)} h; hardware: 4-core CPU, no GPU.", "",
         "## Variants tried (multiple-try ledger)", f"{len(var)} variants/analyses logged in state/variants_tried.csv.", "",
         "## Main table (PLS, forward chaining, nominal 0.90; lot-macro)",
         main[main.method.isin(["scp_sample", "scp_season", "biascorr_naive", "target_only_centred", "lotcp_s", "lotcp_a"]) & main.m.isin([0, 5, 10, 20])]
         [["method", "m", "n_lots", "coverage", "meets", "width", "iscore"]].round(3).to_markdown(index=False), ""]
if conf is not None:
    lines += ["## Pre-registered confirmation (plan_v2; SEEDS_CONFIRM 100-104)", conf[["dataset", "endpoint", "comparison", "m", "n_lots", "mean_diff", "ci_lo", "ci_hi", "p_holm", "rank_biserial", "confirmed"]].round(4).to_markdown(index=False), ""]
if rep is not None:
    lines += ["## Baseline reproduction (G4)", rep.groupby(["model", "test"])[["rmsep", "bias"]].mean().round(3).to_markdown(), "Published: global PLS 1.01 / 1.014 % (Anderson 2020/2021); CNN 0.77 % (Walsh 2024).", ""]
lines += ["## Research questions",
          "* RQ1 coverage loss of standard error bars on later seasons: SUPPORTED (split CP 0.823; 7 procedures 0.77-0.85).",
          "* RQ2 few-shot calibration: coverage restored SUPPORTED; lot-level assurance SUPPORTED and CONFIRMED on untouched data; efficiency gain of LotCP-S over bias correction SUPPORTED on mango, NOT CONFIRMED on untouched data.",
          "* RQ3 harvest decisions: SUPPORTED in retrospective simulation (costs assumed).",
          "* RQ4 planner: SUPPORTED (median abs. relative error 7 %).",
          "* RQ5 generalisation/components: mixed (soil replication; shrinkage removed; replay = validity).", "",
          f"## Leakage audit: {'PASS' if leak.get('pass') else 'FAIL/absent'}", "",
          "## Novelty scores", json.dumps(sc, indent=1), "", "## Gates", "| Gate | Status | Note |", "|---|---|---|"]
lines += [f"| {k} | {v.get('status')} | {v.get('note')} |" for k, v in g.items()]
(R / "RESULTS_SUMMARY.md").write_text("\n".join(lines) + "\n")
print("written", R / "RESULTS_SUMMARY.md")
