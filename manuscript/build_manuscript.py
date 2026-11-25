"""Build the manuscript (Markdown -> DOCX -> PDF) with every number taken from result files.

Text lives in manuscript/sections/*.md. Placeholders of the form {{expression}} are evaluated
against helper functions that read results/ and tables/, so no result is typed by hand.
Usage:  python -m manuscript.build_manuscript
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript"
TITLE = ("Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons")
SHORT_TITLE = "Risk-aware mango harvest decisions with few-shot conformal NIR calibration"


# --------------------------------------------------------------------------- result access
class R:
    """Read-only accessors used inside {{...}} placeholders."""

    def __init__(self):
        self.metrics = json.load(open(ROOT / "results" / "metrics.json"))
        self.t = {p.stem: pd.read_csv(p) for p in (ROOT / "tables").glob("*.csv")}
        rob = ROOT / "results" / "robustness"
        self.rob = pd.read_csv(rob / "robustness_raw.csv", low_memory=False).replace(np.inf, np.nan) if (rob / "robustness_raw.csv").exists() else None
        self.cost = json.load(open(rob / "cost.json")) if (rob / "cost.json").exists() else {}
        self.plan = pd.read_csv(rob / "planning.csv") if (rob / "planning.csv").exists() else None
        if self.plan is not None:
            self.plan = self.plan[self.plan.m > 0]
        self.spec = pd.read_csv(rob / "spectrum_level.csv.gz") if (rob / "spectrum_level.csv.gz").exists() else None
        self.cfg = __import__("yaml").safe_load(open(ROOT / "config" / "default.yaml"))
        self.timing = json.load(open(ROOT / "results" / "run_timing.json")) if (ROOT / "results" / "run_timing.json").exists() else {}
        d1 = self.t["table1_dataset"]
        tot = d1[d1.season == "All"].iloc[0]
        meta = pd.read_csv(ROOT / "data" / "processed" / "mango_v4.meta.csv") if (ROOT / "data" / "processed" / "mango_v4.meta.csv").exists() else None
        self.V = dict(
            n_spectra=f"{int(tot.spectra):,}", n_samples=f"{int(tot['samples']):,}", n_lots=int(tot.lots), n_seasons=len(d1) - 1,
            n_cultivars=int(tot.cultivars), n_instruments=int(tot.instruments),
            n_target_lots=int(self.metrics["_meta"]["n_target_lots"]), n_draws=self.cfg["eval"]["n_draws"],
            n_episodes=self.cfg["eval"]["n_episodes"], n_boot=f"{self.cfg['stats']['n_boot']:,}",
        )
        if meta is not None:
            self.V["median_scans"] = int(meta.groupby("reference_no").size().median())
        p2 = self.t["table2_point_models_by_seed"]
        self.V["cnn_params"] = f"{int(p2[p2.model == 'cnn'].n_params.iloc[0]):,}"

        c3 = ROOT / "results" / "cycle3"
        self.c3 = {n: pd.read_csv(c3 / f"{n}.csv") for n in ("season_summary", "season_tests", "decisions_ci", "decisions_vs_best_m0",
                                                           "alpha_loso", "planner_by_sources", "assurance_frontier")
                   if (c3 / f"{n}.csv").exists()}
        rr = pd.read_csv(ROOT / "results" / "raw_results.csv", usecols=["model", "protocol", "alpha", "seed", "method", "m", "target", "lot"])
        rr = rr[(rr.model == "pls") & (rr.protocol == "forward") & (rr.alpha == 0.1) & (rr.seed == 0) & (rr.method == "scp_sample")]
        self.lots_by_target = rr.groupby("target").lot.nunique().to_dict()
        self.c3j = {n: json.load(open(c3 / f"{n}.json")) for n in ("neospectra_overlap", "decisions_meta", "season_tests_meta") if (c3 / f"{n}.json").exists()}

    # ---- cycle 3 (review round 1): season-level summaries, tests, decisions with CIs -------------------------
    def ss(self, method, m, field="coverage_pooled", model="pls"):
        t = self.c3["season_summary"]
        return float(t[(t.model == model) & (t.method == method) & (t.m == m)][field].iloc[0])

    def st(self, ref, comp, outcome, m, field="season_avg_diff", model="pls", subset="all"):
        t = self.c3["season_tests"]
        return t[(t.model == model) & (t.reference == ref) & (t.comparator == comp) & (t.outcome == outcome) & (t.m == m) & (t.subset == subset)][field].iloc[0]

    def stci(self, ref, comp, outcome, m, model="pls", subset="all", digits=3):
        lo, hi = (float(self.st(ref, comp, outcome, m, f, model, subset)) for f in ("boot_lo", "boot_hi"))
        return f"{lo:+.{digits}f} to {hi:+.{digits}f}"

    def dc(self, rule, m, field="cost100", model="pls"):
        t = self.c3["decisions_ci"]
        return float(t[(t.model == model) & (t.rule == rule) & (t.m == m)][field].iloc[0])

    def dd(self, rule, m, field="diff100", model="pls"):
        t = self.c3["decisions_vs_best_m0"]
        return t[(t.model == model) & (t.rule == rule) & (t.m == m)][field].iloc[0]

    def al(self, rule, m, a_star, field, model="pls"):
        t = self.c3["alpha_loso"]
        return float(t[(t.model == model) & (t.rule == rule) & (t.m == m) & np.isclose(t.alpha_star, a_star)][field].iloc[0])

    def pbs(self, n_source, method="lotcp_s", field="mean_rel_error"):
        t = self.c3["planner_by_sources"]
        return float(t[(t.method == method) & (t.n_source == n_source)][field].iloc[0])

    def af(self, method, m, field="share_ge_090"):
        t = self.c3["assurance_frontier"]
        return float(t[(t.method == method) & (t.m == m)][field].iloc[0])

    # main table (PLS, forward, alpha = 0.1)
    def m(self, method, m, field="coverage"):
        return self.metrics[f"{method}|m{m}"][field]

    def c(self, method, m):
        return f"{self.m(method, m):.3f}"

    def ci(self, method, m):
        return f"{self.m(method, m, 'cov_lo'):.3f}–{self.m(method, m, 'cov_hi'):.3f}"

    def w(self, method, m):
        return f"{self.m(method, m, 'width'):.2f}"

    def i(self, method, m):
        return f"{self.m(method, m, 'iscore'):.2f}"

    def u(self, method, m):
        return f"{100 * self.m(method, m, 'under'):.0f}"

    def pct(self, a, b, digits=0):
        """Relative change of a with respect to b in percent (positive number)."""
        return f"{abs(100 * (a - b) / b):.{digits}f}"

    def season_cov(self, method, m):
        t = self.t["table4_per_season"]
        g = t[(t.method == method) & (t.m == m)].sort_values("target")
        return g.coverage.to_numpy()

    def season_range(self, method, m):
        v = self.season_cov(method, m)
        return f"{v.min():.2f}–{v.max():.2f}"

    def gen(self, model, protocol, method, m, field="coverage"):
        t = self.t["table7_generalisation"]
        r = t[(t.model == model) & (t.protocol == protocol) & (t.method == method) & (t.m == m)]
        return float(r[field].iloc[0])

    def test(self, other, m, outcome="iscore"):
        t = self.t["table6_tests"]
        r = t[(t.other == other) & (t.m == m) & (t.outcome == outcome)]
        return r.iloc[0]

    def p(self, other, m, outcome="iscore"):
        v = float(self.test(other, m, outcome).p_holm)
        return "< 0.001" if v < 0.001 else f"= {v:.3f}"

    def robcov(self, factor, level, method, m, field="coverage"):
        g = self.rob[(self.rob.factor == factor) & (self.rob.method == method) & (self.rob.m == m)]
        g = g[g.level.astype(str).str.startswith(str(level))] if factor == "protocol" else g[np.isclose(g.level.astype(float), float(level))]
        return float(g[field].mean())

    def sub(self, col, val, method):
        g = self.spec[self.spec[col].astype(str) == str(val)]
        return f"{np.average(g['cov_' + method], weights=g.w):.2f}"

    def _lotcov(self):
        if not hasattr(self, "_lc"):
            self._lc = self.spec.groupby(["target", "lot"]).apply(lambda g: pd.Series({
                "scp_sample": np.average(g.cov_scp_sample, weights=g.w), "lotcp": np.average(g.cov_lotcp, weights=g.w),
                "lotcp_s": np.average(g.cov_lotcp_s, weights=g.w), "abs_bias": abs(g.lot_bias.iloc[0]),
                "ratio": g.lot_sd.iloc[0] / g.prior_sd.iloc[0]}), include_groups=False)
        return self._lc

    def lotfail(self, method, thr=0.8):
        return int((self._lotcov()[method] < thr).sum())

    def nlot_err(self):
        return len(self._lotcov())

    def rho(self, a, b):
        return f"{self._lotcov()[[a, b]].corr(method='spearman').iloc[0, 1]:.2f}"

    def tau_sigma(self):
        """Range over target seasons of the estimated SD components (tau, sigma) of LotCP, PLS."""
        info = json.load(open(ROOT / "results" / "calibration_info.json"))
        rows = [x["calib"]["m10"] for x in info if x["model"] == "pls" and x["protocol"] == "forward" and abs(x["alpha"] - 0.1) < 1e-9]
        tau = np.sqrt([x["tau2"] for x in rows]); sig = np.sqrt([x["sigma2"] for x in rows]); w3 = [x["tau2"] / (x["tau2"] + x["sigma2"] / 3) for x in rows]
        return dict(tau=f"{tau.min():.2f}–{tau.max():.2f}", sigma=f"{sig.min():.2f}–{sig.max():.2f}", w3=f"{min(w3):.2f}–{max(w3):.2f}")

    def season_min(self, method, m):
        """Lowest per-season lot-macro coverage (PLS, forward, primary alpha) from the raw results."""
        if not hasattr(self, "_raw"):
            raw = pd.read_csv(ROOT / "results" / "raw_results.csv")
            self._raw = raw[(raw.model == "pls") & (raw.protocol == "forward") & np.isclose(raw.alpha, 0.1)]
        g = self._raw[(self._raw.method == method) & (self._raw.m == m)]
        return f"{g.groupby('target').coverage.mean().min():.2f}"

    def unweighted(self, method):
        """Scan-level coverage with every scan weighted equally (m = 10 reference draws excluded)."""
        return f"{self.spec['cov_' + method].mean():.3f}"

    def worst_lot_ratio(self):
        return f"{self._lotcov().sort_values('lotcp_s').ratio.iloc[0]:.1f}"

    def robf(self_, factor, method, m, field="coverage"):
        g = self_.rob[(self_.rob.factor == factor) & (self_.rob.method == method) & (self_.rob.m == m)]
        return float(g[field].mean())

    def spk(self, method, field="rmse"):
        t = self.t["table12_spiking"]
        return float(t[t.method == method][field].iloc[0])

    def jk(self, method, m, field):
        t = self.t["table4b_season_jackknife"]
        return float(t[(t.method == method) & (t.m == m)][field].iloc[0])

    def test_b(self, other, m):
        t = self.t["table6b_tests_no_replicates"]
        return t[(t.other == other) & (t.m == m) & (t.outcome == "iscore")].iloc[0]

    def pb(self, other, m):
        v = float(self.test_b(other, m).p_holm)
        return "< 0.001" if v < 0.001 else f"= {v:.3f}"

    def xfit(self, model, field="total_seconds"):
        t = self.t["table11b_crossfit_cost"]
        return float(t[t.model == model][field].iloc[0])

    def meet(self, method, m):
        t = self.t["table3_main_intervals"]                 # same rounded source as Table 14
        return f"{100 * float(t[(t.method == method) & (t.m == m)].meets.iloc[0]):.0f}"

    def season_meets(self, method, m):
        if not hasattr(self, "_raw"):
            self.season_min(method, m)
        g = self._raw[(self._raw.method == method) & (self._raw.m == m)].groupby("target")["meets"].mean()
        return f"{100 * g.min():.0f}–{100 * g.max():.0f}"

    # ---- external soil data -----------------------------------------------------------------
    def soil(self, task, method, m, field="coverage"):
        t = self.t["table13_soil"]
        g = t[(t.task == task) & (t.method == method) & (t.m == m)]
        return float(g[field].iloc[0])

    def soilp(self, task, field):
        t = self.t["table13b_soil_point"]
        g = t[t.task == task]
        return float(g[field].mean()) if field not in ("n_source", "n_target", "target_lots", "source_lots") else int(g[field].sum() if task == "kssl_oc" and field in ("n_target", "target_lots") else g[field].mean())

    def soiltest(self, task, other, m):
        t = self.t["table13c_soil_tests"]
        return t[(t.task == task) & (t.other == other) & (t.m == m) & (t.outcome == "iscore")].iloc[0]

    def soilpv(self, task, other, m):
        v = float(self.soiltest(task, other, m).p_holm)
        return "< 0.001" if v < 0.001 else f"= {v:.3f}"

    # ---- decision analysis ------------------------------------------------------------------
    def dec(self, rule, m, thr, field):
        t = self.t["table14_decision"]
        g = t[(t.rule == rule) & (t.m == m) & np.isclose(t.threshold, thr)]
        return float(g[field].iloc[0])

    def decp(self, rule, m, thr, field):
        return f"{100 * self.dec(rule, m, thr, field):.0f}"

    # ---- cycle-2 confirmation, reproduction, replay ablation, published-PLS predictor ------------
    def conf(self, dataset_prefix, endpoint, field):
        t = pd.read_csv(ROOT / "results" / "confirmation" / "confirmation_tests.csv")
        g = t[t.dataset.str.startswith(dataset_prefix) & (t.endpoint == endpoint)]
        return g[field].iloc[0]

    def confp(self, dataset_prefix, endpoint):
        v = float(self.conf(dataset_prefix, endpoint, "p_holm"))
        return "< 0.001" if v < 0.001 else f"= {v:.3f}"

    def csum(self, dataset_prefix, method, m, field):
        t = pd.read_csv(ROOT / "results" / "confirmation" / "confirmation_summary.csv")
        g = t[t.dataset.str.startswith(dataset_prefix) & (t.method == method) & (t.m == m)]
        return float(g[field].iloc[0])

    def repro(self, model, test, field="rmsep", agg="mean"):
        t = pd.read_csv(ROOT / "results" / "reproduction" / "reproduction.csv")
        g = t[(t.model == model) & (t.test == test)][field]
        return float(getattr(g, agg)())

    def repro_n_train(self):
        return int(json.load(open(ROOT / "results" / "reproduction" / "reproduction_meta.json"))["n_train"])

    def season_cov_t(self, method, m, target, field="coverage"):
        if not hasattr(self, "_raw"):
            self.season_min(method, m)
        g = self._raw[(self._raw.method == method) & (self._raw.m == m) & (self._raw.target == target)]
        return float(g[field].mean())

    def replay(self, method, m, field):
        t = pd.read_csv(ROOT / "results" / "ablation_cycle2" / "replay_ablation.csv").replace(np.inf, np.nan)
        return float(t[(t.method == method) & (t.m == m)][field].mean())

    def pubpls(self, method, m, field):
        t = pd.read_csv(ROOT / "results" / "published_pls" / "published_pls.csv").replace(np.inf, np.nan)
        return float(t[(t.method == method) & (t.m == m)][field].mean())

    # ---- harvest decisions, economics, planner, prototype --------------------------------------
    def hv(self, rule, m, alpha=None, field="immature_among_accepted", t=15.0, model="pls"):
        z = self.t["table16_harvest_fruit"]
        g = z[(z.model == model) & (z.rule == rule) & (z.m == m) & np.isclose(z.threshold, t)]
        g = g[np.isclose(g.alpha, -1)] if alpha is None else g[np.isclose(g.alpha, alpha, atol=1e-3)]
        return float(g[field].iloc[0])

    def hvp(self, *a, digits=0, **k):
        return f"{100 * self.hv(*a, **k):.{digits}f}"

    def lotd(self, rule, m, alpha=None, field="premature", t=15.0, p=0.8, model="pls"):
        z = self.t["table18_lot_decisions"]
        g = z[(z.model == model) & (z.rule == rule) & (z.m == m) & np.isclose(z.threshold, t) & np.isclose(z.p, p)]
        g = g[np.isclose(g.alpha, -1)] if alpha is None else g[np.isclose(g.alpha, alpha, atol=1e-3)]
        return float(g[field].iloc[0])

    def lotdp(self, *a, **k):
        return f"{100 * self.lotd(*a, **k):.0f}"

    def econ(self, rule, m, a_star, N=1000, t=15.0, model="pls"):
        z = self.t["table17_economics"]
        g = z[(z.model == model) & (z.rule == rule) & (z.m == m) & np.isclose(z.alpha_star, a_star, atol=1e-3) & (z.lot_size == N) & np.isclose(z.threshold, t)]
        return float(g.cost.iloc[0])

    def econ_best_m(self, a_star, N, t=15.0, model="pls"):
        z = self.t["table17_economics"]
        g = z[(z.model == model) & (z.rule == "lotcp_s_lower") & np.isclose(z.alpha_star, a_star, atol=1e-3) & (z.lot_size == N) & np.isclose(z.threshold, t)]
        return int(g.loc[g.cost.idxmin(), "m"])

    def econ_saving(self, a_star, m=5, N=1000, model="pls", base="point"):
        """Range over thresholds of the relative cost reduction of LotCP-S lower (m) versus a baseline rule."""
        vals = []
        for t in (14.0, 15.0, 16.0):
            b = self.econ(base, 0 if base in ("point", "accept_all") else m, a_star, N, t, model)
            vals.append(1 - self.econ("lotcp_s_lower", m, a_star, N, t, model) / b)
        return vals

    def regret(self, model, rule, m):
        z = self.t["table17b_regret"]
        g = z[(z.model == model) & (z.rule == rule) & (z.m == m)]
        return float(g.rel_regret.mean()), float(g.rel_regret.max())

    def plannerv(self, m, col):
        z = self.t["table19_planner"]
        return float(z[z.m == m][col].iloc[0])

    @property
    def demo(self):
        return json.load(open(ROOT / "results" / "tool_demo.json"))

    def point(self, m, correction, field="rmse"):
        t = self.t["table9_point_correction"]
        return float(t[(t.m == m) & (t.correction == correction)][field].iloc[0])


# --------------------------------------------------------------------------- tables
def _pipe(df, caption, fmt=None):
    fmt = fmt or {}
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" if i == 0 else "---:" for i in range(len(cols))) + "|"]
    for k in range(len(df)):
        cells = []
        for c in cols:
            v = df[c].iloc[k]
            if isinstance(v, (float, np.floating)):
                cells.append("–" if not np.isfinite(v) else fmt.get(c, "{:.3f}").format(v))
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out) + f"\n\nTable: {caption}\n"


def tables(r: R) -> dict:
    from src.statistics.analysis import LABEL

    T = {}
    d = r.t["table1_dataset"].copy()
    d = d.rename(columns={"season": "Season", "spectra": "Spectra", "samples": "Samples", "lots": "Lots", "cultivars": "Cultivars",
                          "instruments": "Instrument units", "dm_mean": "DMC mean (%)", "dm_sd": "DMC SD (%)", "median_samples_per_lot": "Median samples per lot"})
    d["Median samples per lot"] = d["Median samples per lot"].astype(int)
    T["dataset"] = _pipe(d, "Table 1. The data set by harvest season.", {"DMC mean (%)": "{:.2f}", "DMC SD (%)": "{:.2f}"})

    p = r.t["table2_point_models"]
    rows = []
    for t, g in p.groupby("target"):
        g = g.set_index("model")
        rows.append({"Target season": int(t), "RMSECV sample folds": g.loc["pls", "rmse_cv_sample"], "RMSECV lot folds": g.loc["pls", "rmse_cv_lot"],
                     "RMSECV season folds": g.loc["pls", "rmse_cv_season"], "RMSEP PLS": g.loc["pls", "rmse"], "RMSEP LightGBM": g.loc["gbm", "rmse"],
                     "RMSEP 1D-CNN": g.loc["cnn", "rmse"], "Bias PLS": g.loc["pls", "bias"], "SD of lot bias, PLS": g.loc["pls", "sd_lot_bias"]})
    T["point"] = _pipe(pd.DataFrame(rows), "Table 2. Point-prediction error (% DMC) under forward chaining. RMSECV: cross-validation inside the source "
                       "seasons with PLS under three fold units. RMSEP: error on the target season (LightGBM and CNN: mean of three seeds). "
                       "The last column is the standard deviation of the lot mean residuals in the target season.", {c: "{:.2f}" for c in rows[0] if c != "Target season"})

    s = r.t["table3_main_intervals"]
    from src.statistics.analysis import M0
    a = s[(s.m == 0) & s.method.isin(M0)].copy()
    a["Method"] = a.method.map(LABEL)
    a["CI"] = [f"{lo:.3f}–{hi:.3f}" for lo, hi in zip(a.cov_lo, a.cov_hi)]
    a["Under-covered lots (%)"] = 100 * a.under
    a = a.rename(columns={"coverage": "Coverage", "CI": "95% CI", "width": "Width", "iscore": "Interval score"})
    T["main0"] = _pipe(a[["Method", "Coverage", "95% CI", "Under-covered lots (%)", "Width", "Interval score"]],
                       f"Table 3. Intervals without reference samples (m = 0) on {r.V['n_target_lots']} later-season lots; nominal coverage 0.90, PLS predictor "
                       "unless the method has its own model. Coverage is the lot-macro mean with a bootstrap 95% CI; under-covered lots have coverage below 0.80. "
                       "Width and interval score in % DMC.", {"Under-covered lots (%)": "{:.0f}", "Width": "{:.2f}", "Interval score": "{:.2f}"})

    order = ["biascorr_naive", "slopebias_naive", "pooled", "aci", "target_only", "target_only_centred", "lotcp", "lotcp_s"]
    rows = []
    for k in order:
        row = {"Method": LABEL[k]}
        for m in (3, 5, 10, 20, 30):
            g = s[(s.method == k) & (s.m == m)]
            if g.empty or g.frac_infinite.iloc[0] > 0.5:
                row[f"m={m}"] = "n/a"
            else:
                row[f"m={m}"] = f"{g.coverage.iloc[0]:.3f} / {g.width.iloc[0]:.2f} / {g.iscore.iloc[0]:.2f}"
        rows.append(row)
    T["mainm"] = _pipe(pd.DataFrame(rows), "Table 4. Intervals with m reference samples per lot (PLS, nominal 0.90). Each cell: lot-macro coverage / mean width / "
                       "interval score. n/a: the method returns unbounded intervals at this m. ACI returned unbounded intervals in up to 10% of lot-draws; "
                       "its width and score are over the finite ones.")

    ps = r.t["table4_per_season"]
    rows = []
    for k, m in (("scp_sample", 0), ("scp_lot", 0), ("scp_season", 0), ("lotcp_s", 0), ("biascorr_naive", 10), ("target_only_centred", 10), ("lotcp", 10), ("lotcp_s", 10)):
        g = ps[(ps.method == k) & (ps.m == m)].sort_values("target")
        rows.append({"Method": f"{LABEL[k]} (m={m})", **{str(int(t)): c for t, c in zip(g.target, g.coverage)}})
    T["season"] = _pipe(pd.DataFrame(rows), "Table 5. Lot-macro coverage by target season (PLS, nominal 0.90).")

    ab = r.t["table5_ablation"]
    rows = []
    for k in ["lotcp_s", "lotcp_s_shrink", "lotcp_s_support", "lotcp_s_rep", "lotcp_s_lotfold", "lotcp", "lotcp_shrink", "lotcp_noepisodic", "lotcp_lotfold", "lotcp_samplefold", "lotcp_pooled"]:
        row = {"Variant": LABEL[k]}
        for m in (0, 3, 10, 30):
            g = ab[(ab.method == k) & (ab.m == m)]
            row[f"m={m}"] = f"{g.coverage.iloc[0]:.3f} / {g.width.iloc[0]:.2f} / {g.iscore.iloc[0]:.2f}" if len(g) else "–"
        rows.append(row)
    T["ablation"] = _pipe(pd.DataFrame(rows), "Table 6. Ablation of LotCP components (PLS, nominal 0.90). Each cell: coverage / width / interval score.")

    tt = r.t["table6_tests"]
    rows = []
    for other in ("biascorr_naive", "target_only_centred", "lotcp_s_shrink", "lotcp"):
        for m in (3, 5, 10, 20, 30):
            g = tt[(tt.other == other) & (tt.m == m) & (tt.outcome == "iscore")]
            if g.empty:
                continue
            g = g.iloc[0]
            rows.append({"LotCP-S versus": LABEL[other], "m": m, "Lots": int(g.n_lots), "Mean difference": g.mean_diff,
                         "95% CI": f"{g.ci_lo:.2f} to {g.ci_hi:.2f}", "Holm p": "<0.001" if g.p_holm < 0.001 else f"{g.p_holm:.3f}",
                         "Rank-biserial r": g.rank_biserial, "Seasons favouring LotCP-S": f"{int(g.seasons_ref_better)}/{int(g.n_seasons)}"})
    T["tests"] = _pipe(pd.DataFrame(rows), "Table 7. Paired comparison of the per-lot interval score of LotCP-S with competing methods (Wilcoxon signed-rank test, "
                       "Holm-adjusted over all comparisons of the family; negative differences favour LotCP-S).", {"Mean difference": "{:.2f}", "Rank-biserial r": "{:.2f}"})

    g7 = r.t["table7_generalisation"]
    rows = []
    for (model, protocol, name) in (("pls", "forward", "PLS, forward"), ("gbm", "forward", "LightGBM, forward"), ("cnn", "forward", "1D-CNN, forward"),
                                    ("pls", "loso", "PLS, leave-one-season-out"), ("cnn", "loso", "1D-CNN, leave-one-season-out")):
        for k, m in (("scp_sample", 0), ("scp_season", 0), ("biascorr_naive", 10), ("target_only_centred", 10), ("lotcp", 10), ("lotcp_s", 10)):
            g = g7[(g7.model == model) & (g7.protocol == protocol) & (g7.method == k) & (g7.m == m)]
            if g.empty:
                continue
            rows.append({"Predictor, protocol": name, "Method": f"{LABEL[k]} (m={m})", "Lots": int(g.n_lots.iloc[0]), "Coverage": g.coverage.iloc[0],
                         "Under-covered lots (%)": 100 * g.under.iloc[0], "Width": g.width.iloc[0], "Interval score": g.iscore.iloc[0]})
    T["gen"] = _pipe(pd.DataFrame(rows), "Table 8. Generalisation across point predictors and protocols (nominal 0.90). LightGBM and CNN under forward chaining: "
                     "metrics averaged over three seeds within lot.", {"Under-covered lots (%)": "{:.0f}", "Width": "{:.2f}", "Interval score": "{:.2f}"})

    if r.rob is not None:
        rows = []

        def add(label, g):
            row = {"Condition": label}
            for m in (0, 5, 10, 20):
                x = g[g.m == m]
                row[f"m={m}"] = f"{x.coverage.mean():.3f} / {x.width.mean():.2f}" if len(x) else "–"
            rows.append(row)

        base = pd.read_csv(ROOT / "results" / "raw_results.csv").replace(np.inf, np.nan)
        base = base[(base.model == "pls") & (base.protocol == "forward") & np.isclose(base.alpha, 0.1) & (base.method == "lotcp_s")]
        add("Main setting", base)
        rb = r.rob[r.rob.method == "lotcp_s"]
        for sd in (0.25, 0.5):
            add(f"Reference error SD {sd} % DMC", rb[(rb.factor == "label_noise_sd") & (pd.to_numeric(rb.level, errors="coerce") == sd)])
        add("Provider-flagged outliers removed", rb[rb.factor == "outliers_removed"])
        for k in (10, 20, 40, 80):
            add(f"{k} past lots for calibration", rb[(rb.factor == "n_cal_lots") & (pd.to_numeric(rb.level, errors="coerce") == k)])
        for ne in (5, 10, 100):
            add(f"{ne} episodes per lot", rb[(rb.factor == "n_episodes") & (pd.to_numeric(rb.level, errors="coerce") == ne)])
        for nu in (5, 20, 80):
            add(f"Fixed pseudo-count ν₀ = {nu}", rb[(rb.factor == "nu0") & (pd.to_numeric(rb.level, errors="coerce") == nu)])
        add("Constants and quantile from disjoint halves of the past lots", rb[rb.factor == "split_constants"])
        add("Deployment unit: one instrument unit within a lot", rb[rb.factor == "unit"])
        for key, lab in (("recent2", "Source: two preceding seasons only"), ("region", "Unseen growing region"), ("cultivar", "Unseen cultivar")):
            add(lab, rb[(rb.factor == "protocol") & rb.level.astype(str).str.startswith(key)])
        T["robust"] = _pipe(pd.DataFrame(rows), "Table 9. Robustness and sensitivity of LotCP-S (PLS, nominal 0.90). Each cell: lot-macro coverage / mean width.")

        al = r.t["table8_alpha"]
        rows = []
        for nominal in (0.8, 0.9, 0.95):
            for k, m in (("scp_sample", 0), ("scp_season", 0), ("target_only_centred", 20), ("lotcp_s", 5), ("lotcp_s", 20)):
                g = al[np.isclose(al.nominal, nominal) & (al.method == k) & (al.m == m)]
                if len(g) and g.frac_infinite.iloc[0] < 0.5:
                    rows.append({"Nominal": f"{nominal:.2f}", "Method": f"{LABEL[k]} (m={m})", "Coverage": g.coverage.iloc[0], "Width": g.width.iloc[0]})
        T["alpha"] = _pipe(pd.DataFrame(rows), "Table 10. Other nominal levels (PLS, forward chaining).", {"Width": "{:.2f}"})

    if "table13_soil" in r.t:
        so, rows = r.t["table13_soil"], []
        names = {"lucas_oc": "LUCAS organic C, 2009 → 2015", "lucas_ph": "LUCAS pH, 2009 → 2015", "kssl_oc": "KSSL total C, held-out projects"}
        for task, name in names.items():
            for k, m in (("scp_sample", 0), ("scp_lot", 0), ("lotcp_s", 5), ("biascorr_naive", 10), ("slopebias_naive", 10),
                         ("target_only_centred", 10), ("lotcp_s_shrink", 10), ("lotcp_s", 10), ("lotcp_s", 20)):
                g = so[(so.task == task) & (so.method == k) & (so.m == m)]
                if g.empty:
                    continue
                rows.append({"Data set and task": name, "Method": f"{LABEL[k]} (m={m})", "Lots": int(g.n_lots.iloc[0]), "Coverage": g.coverage.iloc[0],
                             "Under-covered lots (%)": 100 * g.under.iloc[0], "Width": g.width.iloc[0], "Interval score": g.iscore.iloc[0]})
        T["soil"] = _pipe(pd.DataFrame(rows), "Table 12. External validation on vis–NIR soil spectra (PLS, nominal 0.90). Carbon is modelled as log(1 + %); widths and "
                          "interval scores are in the units of the modelled quantity. Calibration residuals are held out by lot (grid cell or project). All methods and m: supplementary table S13.",
                          {"Under-covered lots (%)": "{:.0f}", "Width": "{:.2f}", "Interval score": "{:.2f}"})
    if "table14_decision" in r.t:
        dc, rows = r.t["table14_decision"], []
        lab = {"point": "Point prediction ≥ t", "scp_lower": "Split-CP lower bound ≥ t", "point_bc": "Bias-corrected point prediction ≥ t", "lotcp_s_lower": "LotCP-S lower bound ≥ t"}
        for k, m in (("point", 0), ("scp_lower", 0), ("lotcp_s_lower", 0), ("point_bc", 5), ("lotcp_s_lower", 5), ("point_bc", 10), ("lotcp_s_lower", 10), ("lotcp_s_lower", 20)):
            g = dc[(dc.rule == k) & (dc.m == m) & np.isclose(dc.threshold, 15.0)]
            if g.empty:
                continue
            g = g.iloc[0]
            rows.append({"Acceptance rule": f"{lab[k]} (m={m})", "Coverage of lower bound": g.lower_cov if k not in ("point", "point_bc") else np.nan,
                         "Accepted (%)": 100 * g.accepted, "Non-compliant among accepted (%)": 100 * g.false_accept_share,
                         "Lots with > 10 % non-compliant (%)": 100 * g.lots_over_10pct, "Compliant fruit accepted (%)": 100 * g["yield"]})
        T["decision"] = _pipe(pd.DataFrame(rows), "Table 13. Harvest decision against a minimum dry-matter specification t = 15 % (PLS, forward chaining, one-sided nominal level 0.90). "
                              "A fruit is accepted when the rule's statistic is at least t; it is compliant when its reference DMC is at least t.",
                              {c: "{:.0f}" for c in ("Accepted (%)", "Non-compliant among accepted (%)", "Lots with > 10 % non-compliant (%)", "Compliant fruit accepted (%)")})
    s3, rows = r.t["table3_main_intervals"], []
    for k in ("biascorr_naive", "target_only_centred", "lotcp_s", "lotcp_a20", "lotcp_a"):
        row = {"Method": LABEL[k]}
        for m in (5, 10, 20, 30):
            g = s3[(s3.method == k) & (s3.m == m)]
            row[f"m={m}"] = "n/a" if g.empty or g.frac_infinite.iloc[0] > 0.5 else f"{100 * g.meets.iloc[0]:.0f} % / {g.coverage.iloc[0]:.3f} / {g.width.iloc[0]:.2f}"
        rows.append(row)
    T["assure"] = _pipe(pd.DataFrame(rows), "Table 14. Lot-level assurance (PLS, forward chaining, 137 target lots, 1 − α = 0.90). Each cell: share of lot-draws whose "
                        "realised coverage is at least 0.90 / lot-macro coverage / mean width (% DMC). The target share is 90 % for δ = 0.10 and 80 % for δ = 0.20.")
    if "table16_harvest_fruit" in r.t:
        rows = []
        spec = (("point", 0, None, "Point prediction ≥ t"), ("scp_lower", 0, 0.1, "Split-CP lower bound ≥ t"),
                ("lotcp_s_lower", 0, 0.1, "LotCP-S lower bound ≥ t"), ("point_bc", 10, None, "Bias-corrected point ≥ t"),
                ("bc_lower", 10, 0.1, "Bias corr. + source margin ≥ t"), ("lotcp_s_lower", 5, 0.1, "LotCP-S lower bound ≥ t"),
                ("lotcp_s_lower", 10, 0.1, "LotCP-S lower bound ≥ t"), ("lotcp_a_lower", 10, 0.1, "LotCP-A lower bound ≥ t"))
        for rule, m, a, lab in spec:
            rows.append({"Decision rule": lab, "m": m, "Mature fruit accepted (%)": 100 * r.hv(rule, m, a, "compliant_accepted"),
                         "Immature among accepted (%)": 100 * r.hv(rule, m, a), "Lots > 10 % immature among accepted (%)": 100 * r.hv(rule, m, a, "lots_over_10pct"),
                         "Immature lots harvested (%)": 100 * r.lotd(rule, m, a), "Ready lots delayed (%)": 100 * r.lotd(rule, m, a, "delayed")})
        f1 = {c: "{:.1f}" for c in ("Mature fruit accepted (%)", "Immature among accepted (%)", "Lots > 10 % immature among accepted (%)", "Immature lots harvested (%)", "Ready lots delayed (%)")}
        T["harvest"] = _pipe(pd.DataFrame(rows), "Table 106. Harvest decisions against a 15 % DMC specification on 137 later-season lots (PLS, forward chaining; bounds at α = 0.10). "
                             "Fruit level: a fruit is accepted when the rule's statistic is at least t. Lot level: a lot is harvested when at least 80 % of its scanned fruit are accepted; "
                             "it is ready when at least 80 % of its fruit have reference DMC ≥ t (55 ready and 82 not-ready lots). Specifications of 14 and 16 % and the CNN predictor: supplementary table S16.", f1)
        rows = []
        labels = (("accept_all", 0, "Harvest all fruit"), ("point", 0, "Point prediction ≥ t"), ("point_bc", 10, "Bias-corrected point ≥ t (m = 10)"),
                  ("scp_lower", 0, "Split-CP lower bound at α*"), ("bc_lower", 5, "Bias corr. + source margin at α* (m = 5)"),
                  ("lotcp_s_lower", 3, "LotCP-S lower bound at α* (m = 3)"), ("lotcp_s_lower", 5, "LotCP-S lower bound at α* (m = 5)"), ("lotcp_s_lower", 10, "LotCP-S lower bound at α* (m = 10)"))
        a_list = (0.05, 0.1, 0.2, 1 / 3)
        heads = {0.05: "c_D = 1/19 (α* = 0.05)", 0.1: "c_D = 1/9 (α* = 0.10)", 0.2: "c_D = 1/4 (α* = 0.20)", 1 / 3: "c_D = 1/2 (α* = 0.33)"}
        for rule, m, lab in labels:
            rows.append({"Decision rule": lab, **{heads[a]: f"{100 * r.econ(rule, m, a):.2f}" for a in a_list}})
        for N in (200, 1000, 5000):
            rows.append({"Decision rule": f"Cost-optimal m for LotCP-S, {N} fruit per lot", **{heads[a]: str(r.econ_best_m(a, N)) for a in a_list}})
        T["econ"] = _pipe(pd.DataFrame(rows), "Table 107. Expected cost per 100 fruit in units of the value of one marketable fruit, under ASSUMED costs (PLS, specification 15 % DMC, lots of 1000 fruit "
                          "unless stated). Accepting an immature fruit costs c_I = 1; withholding a mature fruit costs c_D; each destructive reference test costs 1.5. α* = c_D/(c_I + c_D). "
                          "The last three rows give the number of reference fruit that minimises the cost of LotCP-S. These are illustrative scenarios, not measured costs; other "
                          "specifications, lot sizes and the CNN: supplementary table S17.", {h: "{:.2f}" for h in heads.values()})
        pl = r.t["table19_planner"]
        rows = []
        for _, x in pl.iterrows():
            rows.append({"Reference fruit per lot, m": int(x.m), "LotCP-S planned width": x.planned_width_lotcp_s, "LotCP-S realised width": x.realised_width_lotcp_s,
                         "LotCP-A planned width": x.planned_width_lotcp_a, "LotCP-A realised width": x.realised_width_lotcp_a,
                         "Lots ≥ 90 % covered, LotCP-S (%)": 100 * x.lots_reaching_090_lotcp_s, "Lots ≥ 90 % covered, LotCP-A (%)": 100 * x.lots_reaching_090_lotcp_a,
                         "Reference cost per 100 fruit (1000-fruit lot)": x.reference_cost_per_100_fruit_N1000})
        T["planner"] = _pipe(pd.DataFrame(rows), "Table 108. The reference-sampling planner (PLS, mean over the five target seasons). Planned widths are computed from past lots before the season; "
                             "realised widths are those obtained on the lots of the target season. Widths in % DMC; reference cost in units of fruit value (assumed 1.5 per test).",
                             {"LotCP-S planned width": "{:.2f}", "LotCP-S realised width": "{:.2f}", "LotCP-A planned width": "{:.2f}", "LotCP-A realised width": "{:.2f}",
                              "Lots ≥ 90 % covered, LotCP-S (%)": "{:.0f}", "Lots ≥ 90 % covered, LotCP-A (%)": "{:.0f}", "Reference cost per 100 fruit (1000-fruit lot)": "{:.2f}"})
    ct = ROOT / "results" / "confirmation" / "confirmation_tests.csv"
    if ct.exists():
        c = pd.read_csv(ct)
        rows = []
        for _, x in c.iterrows():
            rows.append({"Data set": "Mango (re-draw; lots seen during development)" if x.dataset.startswith("mango") else "NeoSpectra soil (untouched)",
                         "Endpoint": x.endpoint, "Comparison": x.comparison.replace("biascorr_naive", "bias corr. + source CP").replace("target_only_centred", "target-only CP, centred"),
                         "Outcome": "interval score" if x.metric == "interval score" else "share of lots ≥ 0.90", "m": int(x.m), "Lots": int(x.n_lots),
                         "Mean difference": f"{x.mean_diff:+.3f}", "95% CI": f"{x.ci_lo:+.3f} to {x.ci_hi:+.3f}",
                         "Holm p": "<0.001" if x.p_holm < 0.001 else f"{x.p_holm:.3f}", "r": f"{x.rank_biserial:+.2f}",
                         "Criterion met": ("yes (re-draw check)" if x.confirmed else "no (re-draw check)") if x.dataset.startswith("mango")
                         else ("uninformative" if x.endpoint == "P4" else ("yes" if x.confirmed else "no"))})
        T["confirm"] = _pipe(pd.DataFrame(rows), "Table 109. Pre-registered confirmation of the frozen method (experiments/plan_v2.yaml) on five seeds fixed in advance (100–104), "
                             "20 reference draws per seed, lot and m. Unit of analysis: target lot; Wilcoxon signed-rank test, Holm correction over the four endpoints per data set; "
                             "95 % CI: bootstrap over lots; r: matched-pairs rank-biserial correlation. An endpoint is confirmed when Holm p < 0.05, the CI excludes 0 and |r| ≥ 0.2 "
                             "in the expected direction. Negative interval-score differences and positive share differences favour the proposed method. The mango rows are fresh "
                             "reference draws on lots examined during development and are not an independent confirmation. P3 and P4 compare coverage shares without a width "
                             "constraint (Section 6.3); P4 had too few lots and is counted as uninformative.")
    # ---- cycle 3 main tables ----------------------------------------------------------------------------
    if "season_summary" in r.c3:
        lab = dict(LABEL, biascorr_full="Bias corr. + lot scale, no replay", biascorr_rep="Bias corr. + replicate scale, no replay")
        rows = []
        for model, mlab in (("pls", "SNV PLS"), ("plspub", "Published PLS")):
            for meth, ms in (("scp_sample", (0,)), ("scp_season", (0,)), ("biascorr_naive", (5, 10)), ("biascorr_full", (5, 10)),
                             ("target_only_centred", (10, 20)), ("lotcp_s", (5, 10)), ("lotcp_a", (5, 10))):
                for m in ms:
                    rows.append({"Predictor": mlab, "Method": lab[meth], "m": m,
                                 "Coverage, pooled": r.ss(meth, m, "coverage_pooled", model), "Season mean": r.ss(meth, m, "coverage_season_avg", model),
                                 "Excl. 2017": r.ss(meth, m, "coverage_ex2017", model),
                                 "Seasons ≥ 0.90": f"{int(r.ss(meth, m, 'seasons_cov_ge_nominal', model))}/5",
                                 "Lot-draws ≥ 0.90 (%)": 100 * r.ss(meth, m, "meets_pooled", model),
                                 "Width": r.ss(meth, m, "width_pooled", model), "Interval score": r.ss(meth, m, "iscore_pooled", model)})
        T["c3main"] = _pipe(pd.DataFrame(rows), "Table 3. Intervals on later-season lots (forward chaining, 137 target lots in five seasons, nominal 0.90). Coverage is "
                            "the lot-macro coverage pooled over lots, the mean of the five season values, and the pooled value without 2017 (56 lots, two source "
                            "seasons). Seasons ≥ 0.90: seasons whose lot-macro coverage reaches 0.90. Lot-draws ≥ 0.90: share of lot × reference-draw pairs with "
                            "coverage ≥ 0.90. Width and interval score in % DMC (pooled). Target-only CP cannot give a bounded interval for m < 9.",
                            {"Lot-draws ≥ 0.90 (%)": "{:.0f}", "Width": "{:.2f}", "Interval score": "{:.2f}"})
    if "season_tests" in r.c3:
        comps = [("lotcp_s", "scp_sample@m0", "coverage", "LotCP-S vs split CP (sample folds, m = 0)", "coverage"),
                 ("lotcp_s", "scp_season@m0", "coverage", "LotCP-S vs split CP (season folds, m = 0)", "coverage"),
                 ("lotcp_s", "biascorr_naive", "iscore", "LotCP-S vs bias corr. + source CP", "interval score"),
                 ("lotcp_s", "biascorr_naive", "coverage", "LotCP-S vs bias corr. + source CP", "coverage"),
                 ("lotcp_s", "biascorr_full", "iscore", "LotCP-S vs same scale without replay", "interval score"),
                 ("lotcp_s", "biascorr_full", "coverage", "LotCP-S vs same scale without replay", "coverage"),
                 ("lotcp_a", "lotcp_s", "meets", "LotCP-A vs LotCP-S", "lot-draws ≥ 0.90")]
        rows = []
        for ref, comp, out, labc, labo in comps:
            for model, mlab in (("pls", "SNV"), ("plspub", "Pub.")):
                for m in (5, 10):
                    d = 100 if out == "meets" else 1
                    lo, hi = float(r.st(ref, comp, out, m, "boot_lo", model)), float(r.st(ref, comp, out, m, "boot_hi", model))
                    rows.append({"Comparison": labc, "Outcome": labo, "PLS": mlab, "m": m,
                                 "Season-mean difference": f"{d * float(r.st(ref, comp, out, m, 'season_avg_diff', model)):+.3f}" if d == 1 else f"{d * float(r.st(ref, comp, out, m, 'season_avg_diff', model)):+.1f}",
                                 "95% season-cluster CI": f"{d*lo:+.3f} to {d*hi:+.3f}" if d == 1 else f"{d*lo:+.1f} to {d*hi:+.1f}",
                                 "Seasons favouring": f"{int(r.st(ref, comp, out, m, 'seasons_ref_better', model))}/5"})
        T["c3tests"] = _pipe(pd.DataFrame(rows), "Table 4. Season-level comparisons (exploratory except where Section 6.4 states otherwise). Differences are "
                             "oriented so that positive values favour the first method (lower interval score, higher coverage or share). CI: two-stage bootstrap that "
                             "resamples seasons and then lots within seasons (2,000 resamples). With five seasons an exact sign test cannot reach p < 0.05 "
                             "(smallest two-sided p = 0.0625); all lot-level tests are in the supplementary tables.")
    if "decisions_ci" in r.c3:
        lab = {"point": "Point prediction", "scp_lower": "Split-CP lower bound", "point_bc": "Bias-corrected point", "bc_lower": "Bias corr. + source margin",
               "lotcp_s_lower": "LotCP-S lower bound", "lotcp_a_lower": "LotCP-A lower bound", "withhold_all": "Withhold all"}
        rows = []
        for model, mlab in (("pls", "SNV"), ("plspub", "Pub.")):
            for rule, m in (("point", 0), ("scp_lower", 0), ("point_bc", 5), ("bc_lower", 5), ("lotcp_s_lower", 3), ("lotcp_s_lower", 5), ("lotcp_s_lower", 10), ("lotcp_a_lower", 5), ("withhold_all", 0)):
                g = lambda f: r.dc(rule, m, f, model)
                row = {"PLS": mlab, "Rule": lab[rule], "m": m, "Cost / 100 fruit [95% CI]": f"{g('cost100'):.2f} [{g('cost100_lo'):.2f}, {g('cost100_hi'):.2f}]"}
                if rule != "scp_lower":
                    row["Δ vs split-CP bound [95% CI]"] = f"{float(r.dd(rule, m, 'diff100', model)):+.2f} [{float(r.dd(rule, m, 'lo', model)):+.2f}, {float(r.dd(rule, m, 'hi', model)):+.2f}]"
                else:
                    row["Δ vs split-CP bound [95% CI]"] = "reference"
                if rule != "withhold_all":
                    row["Premature lots (%) [CI]"] = f"{g('premature_lots'):.1f} [{g('premature_lo'):.1f}, {g('premature_hi'):.1f}]"
                    row["Ready lots delayed (%) [CI]"] = f"{g('delayed_lots'):.0f} [{g('delayed_lo'):.0f}, {g('delayed_hi'):.0f}]"
                else:
                    row["Premature lots (%) [CI]"] = "0"
                    row["Ready lots delayed (%) [CI]"] = "100"
                rows.append(row)
        T["c3dec"] = _pipe(pd.DataFrame(rows), "Table 5. Harvest decisions at the operating point fixed before this analysis (exploratory; specification 15 % DMC, "
                           "bounds at α = 0.10, lot harvested when ≥ 80 % of its scanned fruit are accepted, ASSUMED costs c_I = 1, c_D = 1/9, c_R = 1.5 per reference "
                           "fruit, lots of 1000 fruit; 137 target lots). Cost in units of the value of one marketable fruit, including reference tests. Δ: cost "
                           "difference to the split-conformal lower bound, the cheapest rule without reference fruit. 95 % CIs: two-stage season-cluster bootstrap.")
    p2 = r.t["table2_point_models_by_seed"]
    cost = p2.groupby("model").agg(fit=("fit_seconds", "mean"), pred=("predict_ms_per_1000", "mean")).reindex(["pls", "gbm", "cnn"])
    rows = [{"Component": {"pls": "PLS fit (final model)", "gbm": "LightGBM fit", "cnn": "1D-CNN fit (20 epochs)"}[k], "Time": f"{v.fit:.1f} s",
             "Per 1000 scans at deployment": f"{v.pred:.1f} ms"} for k, v in cost.iterrows()]
    for k, lab in (("pls", "PLS: all cross-fits for one target season"), ("cnn", "1D-CNN: all cross-fits for one target season")):
        rows.append({"Component": lab, "Time": f"{r.xfit(k):.0f} s", "Per 1000 scans at deployment": "–"})
    for key, lab in (("lotcp_m10", "LotCP calibration, m = 10"), ("lotcp_s_m10", "LotCP-S calibration, m = 10"), ("lotcp_s_m30", "LotCP-S calibration, m = 30")):
        if key in r.cost:
            rows.append({"Component": lab, "Time": f"{r.cost[key]['calibration_seconds']:.1f} s", "Per 1000 scans at deployment": "< 0.1 ms (one bias, one scale per lot)"})
    T["cost"] = _pipe(pd.DataFrame(rows), "Table 11. Computing time on a 4-core CPU without GPU (mean over target seasons; CNN fits used one thread each).")
    return T


# --------------------------------------------------------------------------- assembly
MARK_OPEN, MARK_CLOSE = "\u27e6", "\u27e7"      # brackets used only in the audit rendering


def render(text: str, r: R, T: dict, audit: bool = False) -> str:
    """Fill {{...}} placeholders from result files. With audit=True every filled value is wrapped in markers so that
    scripts/audit_numbers.py can tell machine-filled numbers from numbers typed in the text."""
    ns = {"r": r, "V": r.V, "T": T, "np": np}

    def wrap(v):
        return f"{MARK_OPEN}{v}{MARK_CLOSE}" if audit else v

    def sub(mo):
        expr = mo.group(1).strip()
        if expr.startswith("V:"):
            return wrap(str(r.V[expr[2:]]))
        if expr.startswith("T:"):
            return wrap(T[expr[2:]]) if audit else T[expr[2:]]
        return wrap(str(eval(expr, {"__builtins__": {"abs": abs, "round": round, "min": min, "max": max, "float": float, "int": int, "len": len}, **ns})))

    return re.sub(r"\{\{(.+?)\}\}", sub, text)


def renumber(md: str, prefix: str = "") -> str:
    """Number tables and figures in order of their captions and update every in-text reference (prefix, e.g. "S-", for the supplement)."""
    out = md
    for kind, cap_re, ref_word in (("Table", r"Table: Table (\d+)\.", r"Tables?"), ("Fig", r"!\[Fig\. (\d+)\.", r"Figs?\.")):
        order = []
        for mo in re.finditer(cap_re, out):
            if mo.group(1) not in order:
                order.append(mo.group(1))
        mapping = {old: prefix + str(i + 1) for i, old in enumerate(order)}

        def fix(mo):
            body = re.sub(r"\d+", lambda n: mapping.get(n.group(0), n.group(0)), mo.group(3))
            return mo.group(1) + mo.group(2) + body

        out = re.sub(r"(%s)(\s)(\d+[a-z]?(?:(?:, and |, | and | or |–)\d+[a-z]?)*)" % ref_word, fix, out)
    return out


def build_markdown() -> Path:
    r = R()
    T = tables(r)
    parts = [(MS / "sections" / name).read_text() for name in sorted(p.name for p in (MS / "sections").glob("*.md"))]
    body = renumber(render("\n\n".join(parts), r, T))
    supp_dir = MS / "sections_supp"
    if supp_dir.exists():                     # supplementary notes: same number-filling, own numbering (S...)
        notes = "\n\n".join((supp_dir / n).read_text() for n in sorted(p.name for p in supp_dir.glob("*.md")))
        (ROOT / "supplementary").mkdir(exist_ok=True)
        (ROOT / "supplementary" / "Supplementary_Notes.md").write_text(renumber(render(notes, r, T), prefix="S-"))
    out = MS / "build" / "manuscript.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(body)
    (MS / "build" / "manuscript_audit.md").write_text(render("\n\n".join(parts), r, T, audit=True))
    return out


def to_docx(md: Path, docx: Path, title: str = TITLE, pdf: bool = True):
    """Markdown -> journal-formatted DOCX (and PDF via LibreOffice)."""
    from manuscript.docx_format import make_reference_doc, postprocess

    ref = make_reference_doc(MS / "build" / "reference.docx")
    subprocess.run(["pandoc", str(md), "-o", str(docx), "--from", "markdown+pipe_tables+table_captions+tex_math_dollars+implicit_figures",
                    "--citeproc", "--bibliography", str(MS / "references.bib"), "--csl", str(MS / "elsevier-with-titles.csl"),
                    "--reference-doc", str(ref), "--resource-path", str(ROOT), "--metadata", "link-citations=false"], check=True, cwd=ROOT)
    postprocess(docx, title)
    if pdf and shutil.which("soffice"):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(docx.parent), str(docx)], check=True, capture_output=True)


def main():
    md = build_markdown()
    # tables moved to the supplement are written, with their captions, next to the machine-generated tables
    r_ = R()
    T_ = tables(r_)
    for key, name, tag in (("tests", "table20_tests_main", "S20"), ("gen", "table21_generalisation_main", "S21"), ("robust", "table22_robustness_main", "S22"),
                           ("alpha", "table23_alpha_main", "S23"), ("cost", "table24_cost_main", "S24")):
        if key in T_:
            txt = re.sub(r"Table: Table \d+\. ", f"Table: Table {tag}. ", T_[key])
            (ROOT / "tables" / f"{name}.md").write_text(txt)
    to_docx(md, MS / "Final_Manuscript.docx")
    print("built", MS / "Final_Manuscript.docx")


if __name__ == "__main__":
    main()
