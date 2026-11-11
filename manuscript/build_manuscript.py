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
TITLE = ("How many reference fruit does a valid error bar need? Lot-exchangeable few-shot conformal "
         "calibration of near-infrared dry-matter predictions across harvest seasons")
SHORT_TITLE = "Few-shot conformal calibration of NIR predictions across seasons"


# --------------------------------------------------------------------------- result access
class R:
    """Read-only accessors used inside {{...}} placeholders."""

    def __init__(self):
        self.metrics = json.load(open(ROOT / "results" / "metrics.json"))
        self.t = {p.stem: pd.read_csv(p) for p in (ROOT / "tables").glob("*.csv")}
        rob = ROOT / "results" / "robustness"
        self.rob = pd.read_csv(rob / "robustness_raw.csv", low_memory=False).replace(np.inf, np.nan) if (rob / "robustness_raw.csv").exists() else None
        self.cost = json.load(open(rob / "cost.json")) if (rob / "cost.json").exists() else {}
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

    def worst_lot_ratio(self):
        return f"{self._lotcov().sort_values('lotcp_s').ratio.iloc[0]:.1f}"

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

    order = ["biascorr_naive", "pooled", "aci", "target_only", "target_only_centred", "lotcp_noshrink", "lotcp", "lotcp_s"]
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
    for k in ["lotcp_s", "lotcp_s_support", "lotcp_s_rep", "lotcp_s_lotfold", "lotcp", "lotcp_noshrink", "lotcp_noepisodic", "lotcp_lotfold", "lotcp_samplefold", "lotcp_pooled"]:
        row = {"Variant": LABEL[k]}
        for m in (0, 3, 10, 30):
            g = ab[(ab.method == k) & (ab.m == m)]
            row[f"m={m}"] = f"{g.coverage.iloc[0]:.3f} / {g.width.iloc[0]:.2f} / {g.iscore.iloc[0]:.2f}" if len(g) else "–"
        rows.append(row)
    T["ablation"] = _pipe(pd.DataFrame(rows), "Table 6. Ablation of LotCP components (PLS, nominal 0.90). Each cell: coverage / width / interval score.")

    tt = r.t["table6_tests"]
    rows = []
    for other in ("biascorr_naive", "target_only_centred", "lotcp_noshrink", "lotcp"):
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

    p2 = r.t["table2_point_models_by_seed"]
    cost = p2.groupby("model").agg(fit=("fit_seconds", "mean"), pred=("predict_ms_per_1000", "mean")).reindex(["pls", "gbm", "cnn"])
    rows = [{"Component": {"pls": "PLS fit (final model)", "gbm": "LightGBM fit", "cnn": "1D-CNN fit (20 epochs)"}[k], "Time": f"{v.fit:.1f} s",
             "Per 1000 scans at deployment": f"{v.pred:.1f} ms"} for k, v in cost.iterrows()]
    for key, lab in (("lotcp_m10", "LotCP calibration, m = 10"), ("lotcp_s_m10", "LotCP-S calibration, m = 10"), ("lotcp_s_m30", "LotCP-S calibration, m = 30")):
        if key in r.cost:
            rows.append({"Component": lab, "Time": f"{r.cost[key]['calibration_seconds']:.1f} s", "Per 1000 scans at deployment": "< 0.1 ms (one bias, one scale per lot)"})
    T["cost"] = _pipe(pd.DataFrame(rows), "Table 11. Computing time on a 4-core CPU without GPU (mean over target seasons; CNN fits used one thread each).")
    return T


# --------------------------------------------------------------------------- assembly
def render(text: str, r: R, T: dict) -> str:
    ns = {"r": r, "V": r.V, "T": T, "np": np}

    def sub(mo):
        expr = mo.group(1).strip()
        if expr.startswith("V:"):
            return str(r.V[expr[2:]])
        if expr.startswith("T:"):
            return T[expr[2:]]
        return str(eval(expr, {"__builtins__": {"abs": abs, "round": round, "min": min, "max": max, "float": float, "int": int, "len": len}, **ns}))

    return re.sub(r"\{\{(.+?)\}\}", sub, text)


def build_markdown() -> Path:
    r = R()
    T = tables(r)
    parts = [(MS / "sections" / name).read_text() for name in sorted(p.name for p in (MS / "sections").glob("*.md"))]
    body = render("\n\n".join(parts), r, T)
    out = MS / "build" / "manuscript.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(body)
    return out


def main():
    from manuscript.docx_format import make_reference_doc, postprocess

    md = build_markdown()
    ref = make_reference_doc(MS / "build" / "reference.docx")
    docx = MS / "Final_Manuscript.docx"
    subprocess.run(["pandoc", str(md), "-o", str(docx), "--from", "markdown+pipe_tables+table_captions+tex_math_dollars+implicit_figures",
                    "--citeproc", "--bibliography", str(MS / "references.bib"), "--csl", str(MS / "elsevier-with-titles.csl"),
                    "--reference-doc", str(ref), "--resource-path", str(ROOT), "--metadata", "link-citations=false"], check=True, cwd=ROOT)
    postprocess(docx, TITLE)
    if shutil.which("soffice"):
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(MS), str(docx)], check=True, capture_output=True)
    print("built", docx)


if __name__ == "__main__":
    main()
