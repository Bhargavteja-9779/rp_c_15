"""Stage 5: publication figures, all drawn from machine-generated result files."""
from __future__ import annotations

from pathlib import Path

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
import pandas as pd

from src.data.dataset import load_data
from src.statistics.analysis import LABEL, seed_average, summarise
from src.training.crossfit import pred_path
from src.utils import get_logger, out_dir

# categorical palette (validated for colour-vision deficiency); colour follows the method, never its rank
C = {"blue": "#2a78d6", "orange": "#eb6834", "aqua": "#1baf7a", "yellow": "#eda100", "magenta": "#e87ba4",
     "green": "#008300", "violet": "#6250d6", "red": "#e34948", "ink": "#0b0b0b", "muted": "#52514e", "grid": "#dddcd6"}
STYLE = {  # method -> (colour, marker, linestyle)
    "scp_sample": (C["red"], "s", "--"), "scp_lot": (C["yellow"], "D", "--"), "scp_season": (C["orange"], "^", "--"),
    "biascorr_naive": (C["magenta"], "v", "-"), "target_only_centred": (C["violet"], "P", "-"),
    "lotcp_a": (C["violet"], "D", "-"), "lotcp_a20": (C["violet"], "D", "--"), "lotcp_shrink": (C["aqua"], "X", "-"), "lotcp_s_shrink": (C["aqua"], "X", "--"), "lotcp": (C["green"], "o", "-"), "lotcp_s": (C["blue"], "o", "-"),
    "pooled": (C["yellow"], "D", "-"), "aci": (C["orange"], "^", "-"), "target_only": (C["red"], "s", "-"),
}


def _setup():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
                         "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": C["muted"],
                         "axes.grid": True, "grid.color": C["grid"], "grid.linewidth": 0.5, "legend.frameon": False,
                         "legend.fontsize": 7, "xtick.color": C["muted"], "ytick.color": C["muted"], "figure.dpi": 150,
                         "savefig.dpi": 300, "savefig.bbox": "tight", "lines.linewidth": 1.6, "lines.markersize": 5})


def _save(fig, fdir, name):
    fig.savefig(fdir / f"{name}.png")
    fig.savefig(fdir / f"{name}.pdf")
    plt.close(fig)


def fig_workflow(fdir):
    """Risk-aware harvest workflow (schematic, no data)."""
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 46)

    def box(x, y, w, h, text, fc, bold=False):
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=C["muted"], lw=0.8))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=6.8, color=C["ink"], fontweight="bold" if bold else None)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9))

    blue, orange, green, grey = "#e8f1fc", "#fdeee6", "#e6f6ee", "#f0efec"
    ax.text(1, 44, "Before the season (past seasons only)", fontsize=7.2, color=C["muted"])
    box(1, 31, 19, 11, "Past lots: scans +\nreference DMC", blue)
    box(24, 31, 21, 11, "Season-held-out\nresiduals of the\nNIR model", blue)
    box(49, 31, 22, 11, "Replay m-shot\ncalibration on\npast lots", blue)
    box(75, 31, 24, 11, "Planner: expected\nerror-bar width for\nm = 0, 3, 5, 10, 20", blue, bold=True)
    arrow(20, 36.5, 24, 36.5); arrow(45, 36.5, 49, 36.5); arrow(71, 36.5, 75, 36.5)
    ax.text(1, 26, "In the orchard (new lot)", fontsize=7.2, color=C["muted"])
    box(1, 13, 15, 11, "1  Scan fruit\nwith handheld\nNIR", orange)
    box(19, 13, 15, 11, "2  Predict DMC\n(PLS, LightGBM\nor CNN)", orange)
    box(37, 13, 18, 11, "3  Test m fruit\ndestructively;\ncorrect lot bias\nand scale", orange)
    box(58, 13, 17, 11, "4  Lower bound\nper fruit\nŷ + b̂ − q·ŝ", orange)
    box(79, 18.5, 20, 6, "HARVEST\n(bound ≥ spec)", green, bold=True)
    box(79, 11.5, 20, 6, "WAIT / RE-TEST", grey, bold=True)
    arrow(16, 18.5, 19, 18.5); arrow(34, 18.5, 37, 18.5); arrow(55, 18.5, 58, 18.5)
    arrow(75, 19.5, 79, 21.5); arrow(75, 17.5, 79, 14.5)
    arrow(60, 31, 46, 24); arrow(87, 31, 50, 24)
    ax.text(50, 6.5, "Calibrated level α* = c_D / (c_I + c_D) sets the bound from the relative cost of withholding a mature fruit (c_D)\n"
            "and of accepting an immature one (c_I); the planner chooses m before any fruit of the new season is tested.",
            ha="center", va="center", fontsize=6.3, color=C["muted"])
    _save(fig, fdir, "fig1_workflow")


def fig_data(cfg, fdir):
    d = load_data(cfg)
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.3))
    seasons = np.unique(d.season)
    axes[0].boxplot([d.y[d.season == s] for s in seasons], tick_labels=seasons, widths=0.6, showfliers=False,
                    medianprops=dict(color=C["blue"]), boxprops=dict(color=C["muted"]), whiskerprops=dict(color=C["muted"]), capprops=dict(color=C["muted"]))
    axes[0].set(xlabel="Season", ylabel="Dry matter content (%)", title="(a) Reference values")
    lots = d.meta.groupby("season")["population"].nunique()
    axes[1].bar(lots.index.astype(str), lots.values, color=C["blue"], width=0.6)
    for x, v in zip(range(len(lots)), lots.values):
        axes[1].text(x, v + 1, str(v), ha="center", fontsize=7)
    axes[1].set(xlabel="Season", ylabel="Harvest lots", title="(b) Lots per season"); axes[1].grid(axis="x", visible=False)
    for s, col in zip((2015, 2018, 2021), (C["blue"], C["orange"], C["aqua"])):
        axes[2].plot(d.wl, d.X[d.season == s].mean(0), color=col, label=str(s))
    axes[2].set(xlabel="Wavelength (nm)", ylabel="Mean absorbance", title="(c) Mean spectra"); axes[2].legend()
    fig.tight_layout(); _save(fig, fdir, "fig2_data")


def fig_lot_bias(cfg, fdir):
    """Why split conformal fails: in-season CV residuals vs next-season residuals and lot biases."""
    d = load_data(cfg)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.6))
    biases, seas = [], []
    r_cv, r_next = [], []
    for t in cfg["protocols"]["forward"]["targets"]:
        P = np.load(pred_path(cfg, "pls", 0, "forward", t))
        r = d.y[P["tgt_idx"]] - P["pred_tgt"]
        b = pd.Series(r).groupby(d.lot[P["tgt_idx"]]).mean()
        biases.append(b.to_numpy()); seas.append(t)
        r_cv.append(d.y[P["src_idx"]] - P["oof_sample"]); r_next.append(r)
    bins = np.linspace(-6, 6, 61)
    axes[0].hist(np.concatenate(r_cv), bins=bins, density=True, color=C["muted"], alpha=0.35, label="Sample-fold CV residuals (source seasons)")
    axes[0].hist(np.concatenate(r_next), bins=bins, density=True, histtype="step", color=C["blue"], lw=1.5, label="Residuals on the next season")
    axes[0].set(xlabel="Residual (% DMC)", ylabel="Density", title="(a) Residual distributions, PLS"); axes[0].legend(loc="upper left", fontsize=6)
    rng = np.random.default_rng(0)
    for i, (b, s) in enumerate(zip(biases, seas)):
        axes[1].scatter(i + rng.uniform(-0.18, 0.18, len(b)), b, s=10, color=C["blue"], alpha=0.7, lw=0)
        axes[1].hlines(b.mean(), i - 0.3, i + 0.3, color=C["orange"], lw=1.5)
    axes[1].axhline(0, color=C["muted"], lw=0.8)
    axes[1].set_xticks(range(len(seas))); axes[1].set_xticklabels(seas)
    axes[1].set(xlabel="Target season", ylabel="Lot mean residual (% DMC)", title="(b) Lot-level bias (bar = season mean)")
    fig.tight_layout(); _save(fig, fdir, "fig3_lot_bias")


def _curve(ax, s, method, col, x="m", label=None):
    g = s[s.method == method].sort_values(x)
    c, mk, ls = STYLE[method]
    ax.plot(g[x], g[col], color=c, marker=mk, ls=ls, label=label or LABEL[method])


def fig_main(cfg, fdir, d):
    a0 = cfg["eval"]["primary_alpha"]
    main = d[(d.model == "pls") & (d.protocol == "forward") & np.isclose(d.alpha, a0)]
    s = summarise(main, cfg)
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.7))
    for method in ("biascorr_naive", "target_only_centred", "lotcp", "lotcp_s"):
        g = s[(s.method == method) & (s.frac_infinite < 0.5)]
        for ax, col in zip(axes, ("coverage", "width", "iscore")):
            _curve(ax, g, method, col)
    for method in ("scp_sample", "scp_season"):
        g = s[(s.method == method) & (s.m == 0)]
        c, mk, ls = STYLE[method]
        for ax, col in zip(axes, ("coverage", "width", "iscore")):
            ax.axhline(float(g[col].iloc[0]), color=c, ls=ls, lw=1.2, label=LABEL[method] + " (m = 0)")
    axes[0].axhline(1 - a0, color=C["ink"], lw=0.8, ls=":")
    axes[0].text(30, 1 - a0 + 0.004, "nominal", ha="right", fontsize=6.5, color=C["ink"])
    axes[0].set(xlabel="Reference samples per lot, m", ylabel="Lot-macro coverage", title="(a) Coverage")
    axes[1].set(xlabel="Reference samples per lot, m", ylabel="Mean interval width (% DMC)", title="(b) Width")
    axes[2].set(xlabel="Reference samples per lot, m", ylabel="Interval score (lower is better)", title="(c) Interval score")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout(); _save(fig, fdir, "fig4_main")


def fig_lot_coverage(cfg, fdir, d):
    """Distribution of lot-wise coverage: marginal validity hides lot-to-lot failures."""
    a0 = cfg["eval"]["primary_alpha"]
    main = d[(d.model == "pls") & (d.protocol == "forward") & np.isclose(d.alpha, a0)]
    items = [("scp_sample", 0), ("scp_season", 0), ("biascorr_naive", 10), ("target_only_centred", 10), ("lotcp", 10), ("lotcp_s", 10)]
    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    data = [main[(main.method == k) & (main.m == m)]["coverage"].to_numpy() for k, m in items]
    parts = ax.violinplot(data, showextrema=False, widths=0.8)
    for body, (k, _) in zip(parts["bodies"], items):
        body.set_facecolor(STYLE[k][0]); body.set_alpha(0.35); body.set_edgecolor(STYLE[k][0])
    rng = np.random.default_rng(1)
    for i, (v, (k, _)) in enumerate(zip(data, items), start=1):
        ax.scatter(i + rng.uniform(-0.12, 0.12, len(v)), v, s=6, color=STYLE[k][0], alpha=0.7, lw=0)
        ax.hlines(v.mean(), i - 0.25, i + 0.25, color=C["ink"], lw=1.2)
    ax.axhline(1 - a0, color=C["ink"], lw=0.8, ls=":")
    ax.set_xticks(range(1, len(items) + 1))
    short = {"scp_sample": "Split CP\nsample folds", "scp_season": "Split CP\nseason folds", "biascorr_naive": "Bias corr.\n+ source CP",
             "target_only_centred": "Target-only CP\ncentred", "lotcp": "LotCP", "lotcp_s": "LotCP-S"}
    ax.set_xticklabels([f"{short[k]}\n(m = {m})" for k, m in items], fontsize=6.5)
    ax.set(ylabel="Coverage within lot", title="Lot-wise coverage on later-season lots (each dot = one lot; bar = mean)")
    fig.tight_layout(); _save(fig, fdir, "fig5_lot_coverage")


def fig_ablation(cfg, fdir, d):
    a0 = cfg["eval"]["primary_alpha"]
    main = d[(d.model == "pls") & (d.protocol == "forward") & np.isclose(d.alpha, a0)]
    order = ["lotcp_s", "lotcp_s_shrink", "lotcp_s_support", "lotcp_s_rep", "lotcp_s_lotfold", "lotcp", "lotcp_shrink", "lotcp_noepisodic", "lotcp_lotfold", "lotcp_samplefold", "lotcp_pooled"]
    s = summarise(main, cfg, set(order))
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    for ax, m in zip(axes, (5, 20)):
        g = s[s.m == m].set_index("method").reindex(order)
        y = np.arange(len(order))[::-1]
        ax.errorbar(g["coverage"], y, xerr=[g["coverage"] - g["cov_lo"], g["cov_hi"] - g["coverage"]], fmt="o", color=C["blue"], ecolor=C["muted"], elinewidth=1, capsize=2)
        ax.axvline(1 - a0, color=C["ink"], lw=0.8, ls=":")
        for yi, (cov, isc) in zip(y, zip(g["coverage"], g["iscore"])):
            ax.text(g["cov_hi"].max() + 0.004, yi, f"IS {isc:.2f}", va="center", fontsize=6.5, color=C["muted"])
        ax.set_yticks(y); ax.set_yticklabels([LABEL[k] for k in order], fontsize=6.5)
        ax.set(xlabel="Lot-macro coverage (95% bootstrap CI)", title=f"m = {m}")
        ax.set_xlim(g["cov_lo"].min() - 0.01, g["cov_hi"].max() + 0.035)
    fig.tight_layout(); _save(fig, fdir, "fig6_ablation")


def fig_generalisation(cfg, fdir, d):
    a0 = cfg["eval"]["primary_alpha"]
    fig, axes = plt.subplots(1, 4, figsize=(7.2, 2.4), sharey=True)
    panels = [("pls", "forward", "PLS, forward"), ("gbm", "forward", "LightGBM, forward"), ("cnn", "forward", "1D-CNN, forward"), ("pls", "loso", "PLS, leave-one-season-out")]
    for ax, (model, protocol, title) in zip(axes, panels):
        g = d[(d.model == model) & (d.protocol == protocol) & np.isclose(d.alpha, a0)]
        if g.empty:
            continue
        s = summarise(g, cfg, {"scp_sample", "scp_season", "lotcp", "lotcp_s"})
        for method in ("lotcp", "lotcp_s"):
            _curve(ax, s, method, "coverage")
        for method in ("scp_sample", "scp_season"):
            r = s[(s.method == method) & (s.m == 0)]
            if len(r):
                ax.axhline(float(r["coverage"].iloc[0]), color=STYLE[method][0], ls="--", lw=1.2, label=LABEL[method] + " (m = 0)")
        ax.axhline(1 - a0, color=C["ink"], lw=0.8, ls=":")
        ax.set(title=title, xlabel="m")
    axes[0].set_ylabel("Lot-macro coverage")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout(); _save(fig, fdir, "fig7_generalisation")


def fig_robustness(cfg, fdir):
    p = out_dir(cfg, "results/robustness") / "robustness_raw.csv"
    if not p.exists():
        return
    r = pd.read_csv(p, low_memory=False).replace(np.inf, np.nan)
    a0 = cfg["eval"]["primary_alpha"]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.5), sharey=True)
    base = seed_average(pd.read_csv(out_dir(cfg, "results") / "raw_results.csv"))
    base = base[(base.model == "pls") & (base.protocol == "forward") & np.isclose(base.alpha, a0) & (base.method == "lotcp_s")]
    b = base.groupby("m")["coverage"].mean()
    for ax, (factor, title, fmt) in zip(axes, (("label_noise_sd", "(a) Noise in reference values", "SD {} % DMC"),
                                               ("n_cal_lots", "(b) Past lots used for calibration", "{} lots"),
                                               ("protocol", "(c) Other shifts", "{}"))):
        g = r[(r.factor == factor) & (r.method == "lotcp_s")]
        ax.plot(b.index, b.values, color=C["ink"], marker="o", label="Main setting")
        cols = [C["blue"], C["orange"], C["aqua"], C["violet"], C["magenta"], C["yellow"], C["green"]]
        if factor == "protocol":
            g = g.assign(level=g["level"].astype(str).str.split(":").str[0])
        else:
            g = g.assign(level=pd.to_numeric(g["level"]))
        for (lvl, gg), col, mk in zip(g.groupby("level"), cols, "s^DvPX*"):
            c = gg.groupby("m")["coverage"].mean()
            lab = {"recent2": "Two most recent seasons", "region": "Unseen region", "cultivar": "Unseen cultivar"}.get(lvl, fmt.format(int(lvl) if float(lvl).is_integer() else lvl) if factor != "protocol" else lvl)
            ax.plot(c.index, c.values, color=col, marker=mk, label=lab)
        ax.axhline(1 - a0, color=C["ink"], lw=0.8, ls=":")
        ax.set(title=title, xlabel="m"); ax.legend(fontsize=6)
    axes[0].set_ylabel("Lot-macro coverage, LotCP-S")
    fig.tight_layout(); _save(fig, fdir, "fig8_robustness")


def fig_error(cfg, fdir):
    p = out_dir(cfg, "results/robustness") / "spectrum_level.csv.gz"
    if not p.exists():
        return
    s = pd.read_csv(p)
    lot = s.groupby(["target", "lot"]).apply(lambda g: pd.Series({
        "cov_scp": np.average(g.cov_scp_sample, weights=g.w), "cov_lotcp": np.average(g.cov_lotcp, weights=g.w),
        "cov_lotcp_s": np.average(g.cov_lotcp_s, weights=g.w), "abs_bias": abs(g.lot_bias.iloc[0]),
        "scale_ratio": g.lot_sd.iloc[0] / g.prior_sd.iloc[0]}), include_groups=False).reset_index()
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.5))
    axes[0].scatter(lot.abs_bias, lot.cov_scp, s=9, color=C["red"], alpha=0.7, lw=0, label="Split CP (sample folds)")
    axes[0].scatter(lot.abs_bias, lot.cov_lotcp_s, s=9, color=C["blue"], alpha=0.7, lw=0, label="LotCP-S (m = 10)")
    axes[0].set(xlabel="|lot bias| (% DMC)", ylabel="Coverage within lot", title="(a) Bias drives split-CP failure"); axes[0].legend(fontsize=6)
    axes[1].scatter(lot.scale_ratio, lot.cov_lotcp, s=9, color=C["green"], alpha=0.7, lw=0, label="LotCP")
    axes[1].scatter(lot.scale_ratio, lot.cov_lotcp_s, s=9, color=C["blue"], alpha=0.7, lw=0, label="LotCP-S")
    axes[1].axvline(1, color=C["muted"], lw=0.8)
    axes[1].set(xlabel="Lot residual SD / prior SD", ylabel="Coverage within lot", title="(b) Scale drives residual failure"); axes[1].legend(fontsize=6)
    s["dm_bin"] = pd.cut(s.dm, [0, 13, 15, 17, 19, 40], labels=["<13", "13–15", "15–17", "17–19", ">19"])
    g = s.groupby("dm_bin", observed=True).apply(lambda x: pd.Series({k: np.average(x[f"cov_{k}"], weights=x.w) for k in ("scp_sample", "lotcp", "lotcp_s")}), include_groups=False)
    x = np.arange(len(g)); wbar = 0.26
    for i, (k, col) in enumerate((("scp_sample", C["red"]), ("lotcp", C["green"]), ("lotcp_s", C["blue"]))):
        axes[2].bar(x + (i - 1) * wbar, g[k], wbar - 0.03, color=col, label=LABEL[k])
    axes[2].axhline(1 - cfg["eval"]["primary_alpha"], color=C["ink"], lw=0.8, ls=":")
    axes[2].set_xticks(x); axes[2].set_xticklabels(g.index)
    axes[2].set(xlabel="Reference DMC (%)", ylabel="Coverage", title="(c) Coverage by DMC range", ylim=(0.5, 1.0)); axes[2].legend(fontsize=6); axes[2].grid(axis="x", visible=False)
    fig.tight_layout(); _save(fig, fdir, "fig9_error_analysis")


def fig_soil(cfg, fdir):
    p = out_dir(cfg, "results/soil") / "soil_raw.csv"
    if not p.exists():
        return
    r = pd.read_csv(p, low_memory=False).replace(np.inf, np.nan)
    a0 = cfg["eval"]["primary_alpha"]
    names = {"lucas_oc": "LUCAS organic C\n2009 → 2015", "lucas_ph": "LUCAS pH\n2009 → 2015", "kssl_oc": "KSSL total C\nheld-out projects"}
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    for ax, (task, title) in zip(axes, names.items()):
        g = r[r.task == task]
        if g.empty:
            continue
        for method in ("biascorr_naive", "target_only_centred", "lotcp_s_shrink", "lotcp", "lotcp_s"):
            x = g[g.method == method].groupby("m").agg(c=("coverage", "mean"), inf=("frac_infinite", "mean")).reset_index()
            x = x[x.inf.fillna(0) < 0.5]
            c, mk, ls = STYLE[method]
            ax.plot(x.m, x.c, color=c, marker=mk, ls=ls, label=LABEL[method])
        v = g[(g.method == "scp_sample") & (g.m == 0)].coverage.mean()
        ax.axhline(v, color=STYLE["scp_sample"][0], ls="--", lw=1.2, label=LABEL["scp_sample"] + " (m = 0)")
        ax.axhline(1 - a0, color=C["ink"], lw=0.8, ls=":")
        ax.set(title=title, xlabel="Reference samples per lot, m")
    axes[0].set_ylabel("Lot-macro coverage")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.16))
    fig.tight_layout(); _save(fig, fdir, "fig10_soil")


def fig_decision(cfg, fdir):
    p = out_dir(cfg, "results/robustness") / "decision_summary.csv"
    if not p.exists():
        return
    d = pd.read_csv(p)
    d = d[np.isclose(d.threshold, 15.0)]
    items = [("point", 0, "Point prediction", C["red"]), ("scp_lower", 0, "Split-CP lower bound", C["orange"]), ("point_bc", 10, "Bias-corrected point (m = 10)", C["magenta"]),
             ("lotcp_s_lower", 5, "LotCP-S lower bound (m = 5)", C["aqua"]), ("lotcp_s_lower", 10, "LotCP-S lower bound (m = 10)", C["blue"])]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.5))
    for ax, (col, lab) in zip(axes, (("false_accept_share", "Non-compliant share\nof accepted fruit"), ("lots_over_10pct", "Lots with > 10 % non-compliant\namong accepted"), ("yield", "Share of compliant\nfruit accepted"))):
        vals = [float(d[(d.rule == k) & (d.m == m)][col].iloc[0]) for k, m, _, _ in items]
        ax.barh(range(len(items))[::-1], vals, color=[c for *_, c in items], height=0.6)
        for y, v in zip(range(len(items))[::-1], vals):
            ax.text(v + 0.01 * max(vals), y, f"{100 * v:.0f} %", va="center", fontsize=7, color=C["ink"])
        ax.set_yticks(range(len(items))[::-1]); ax.set_yticklabels([lab_ for _, _, lab_, _ in items] if ax is axes[0] else [], fontsize=6.5)
        ax.set_title(lab, fontsize=8); ax.set_xlim(0, max(vals) * 1.25); ax.grid(axis="y", visible=False); ax.set_axisbelow(True)
        ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    fig.tight_layout(); _save(fig, fdir, "fig11_decision")


def fig_assurance(cfg, fdir, d):
    """Lot-level assurance: share of lots whose realised coverage reaches the nominal level."""
    a0 = cfg["eval"]["primary_alpha"]
    main = d[(d.model == "pls") & (d.protocol == "forward") & np.isclose(d.alpha, a0)]
    if "meets" not in main or "lotcp_a" not in set(main.method):
        return
    s = summarise(main, cfg, {"biascorr_naive", "target_only_centred", "lotcp_s", "lotcp_a", "lotcp_a20"})
    style = {"biascorr_naive": STYLE["biascorr_naive"], "target_only_centred": (C["orange"], "P", "-"), "lotcp_s": STYLE["lotcp_s"],
             "lotcp_a20": STYLE["lotcp_a20"], "lotcp_a": STYLE["lotcp_a"]}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.7))
    for method, (c, mk, ls) in style.items():
        g = s[(s.method == method) & (s.frac_infinite < 0.5) & (s.m > 0)].sort_values("m")
        axes[0].plot(g.m, g.meets, color=c, marker=mk, ls=ls, label=LABEL[method])
        axes[1].plot(g.m, g.width, color=c, marker=mk, ls=ls)
    axes[0].axhline(0.9, color=C["ink"], lw=0.8, ls=":"); axes[0].axhline(0.8, color=C["ink"], lw=0.8, ls=":")
    axes[0].text(17, 0.888, "target for δ = 0.10", ha="center", fontsize=6.5); axes[0].text(15, 0.788, "target for δ = 0.20", ha="center", fontsize=6.5)
    axes[0].set(xlabel="Reference samples per lot, m", ylabel="Share of lot-draws with\ncoverage ≥ 0.90", title="(a) Lots reaching the nominal coverage")
    axes[1].set(xlabel="Reference samples per lot, m", ylabel="Mean interval width (% DMC)", title="(b) Price in width")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout(); _save(fig, fdir, "fig12_assurance")


def fig_planning(cfg, fdir):
    p = out_dir(cfg, "results/robustness") / "planning.csv"
    if not p.exists():
        return
    z = pd.read_csv(p)
    z = z[z.m > 0]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    lim = (min(z.planned_width.min(), z.realised_width.min()) - 0.2, max(z.planned_width.max(), z.realised_width.max()) + 0.2)
    for model, (col, mk) in {"pls": (C["blue"], "o"), "gbm": (C["orange"], "s"), "cnn": (C["aqua"], "^")}.items():
        g = z[z.model == model]
        axes[0].scatter(g.planned_width, g.realised_width, s=14, color=col, marker=mk, alpha=0.8, lw=0,
                        label={"pls": "PLS", "gbm": "LightGBM", "cnn": "1D-CNN"}[model])
    axes[0].plot(lim, lim, color=C["ink"], lw=0.8, ls=":")
    axes[0].set(xlim=lim, ylim=lim, xlabel="Width planned from past lots (% DMC)", ylabel="Width realised on the target season (% DMC)",
                title="(a) Planned against realised width"); axes[0].legend()
    g = z[(z.model == "pls")]
    for method, (c, mk, ls) in {"lotcp_s": STYLE["lotcp_s"], "lotcp_a": STYLE["lotcp_a"]}.items():
        x = g[g.method == method].groupby("m")[["planned_width", "realised_width"]].mean()
        axes[1].plot(x.index, x.planned_width, color=c, ls="--", marker=mk, mfc="white", label=LABEL[method] + ", planned")
        axes[1].plot(x.index, x.realised_width, color=c, ls="-", marker=mk, label=LABEL[method] + ", realised")
    axes[1].set(xlabel="Reference samples per lot, m", ylabel="Mean interval width (% DMC)", title="(b) Budget curve, PLS"); axes[1].legend(fontsize=6)
    fig.tight_layout(); _save(fig, fdir, "fig13_planning")


def fig_harvest(cfg, fdir):
    tdir = out_dir(cfg, "tables")
    if not (tdir / "table16_harvest_fruit.csv").exists():
        return
    s = pd.read_csv(tdir / "table16_harvest_fruit.csv")
    lots = pd.read_csv(tdir / "table18_lot_decisions.csv")
    z = s[(s.model == "pls") & (s.threshold == 15)]
    L = lots[(lots.model == "pls") & (lots.threshold == 15) & (lots.p == 0.8)]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    fam = [("scp_lower", 0, "Split-CP lower bound (m = 0)", C["red"], "s", "--"), ("bc_lower", 10, "Bias corr. + source margin (m = 10)", C["magenta"], "v", "-"),
           ("lotcp_s_lower", 0, "LotCP-S lower bound (m = 0)", C["aqua"], "o", "--"), ("lotcp_s_lower", 10, "LotCP-S lower bound (m = 10)", C["blue"], "o", "-")]
    for rule, m, lab, col, mk, ls in fam:
        g = z[(z.rule == rule) & (z.m == m)].sort_values("alpha")
        axes[0].plot(100 * g.compliant_accepted, 100 * g.immature_among_accepted, color=col, marker=mk, ls=ls, label=lab, ms=4)
        h = L[(L.rule == rule) & (L.m == m)].sort_values("alpha")
        axes[1].plot(100 * h.delayed, 100 * h.premature, color=col, marker=mk, ls=ls, ms=4)
    for rule, m, lab, mk in (("point", 0, "Point prediction", "X"), ("point_bc", 10, "Bias-corrected point (m = 10)", "P")):
        g = z[(z.rule == rule) & (z.m == m)]
        axes[0].scatter(100 * g.compliant_accepted, 100 * g.immature_among_accepted, color=C["ink"], marker=mk, s=40, zorder=5, label=lab)
        h = L[(L.rule == rule) & (L.m == m)]
        axes[1].scatter(100 * h.delayed, 100 * h.premature, color=C["ink"], marker=mk, s=40, zorder=5)
    a10 = z[(z.rule == "lotcp_s_lower") & (z.m == 10) & np.isclose(z.alpha, 0.1)]
    axes[0].annotate("α = 0.10", (100 * a10.compliant_accepted.iloc[0], 100 * a10.immature_among_accepted.iloc[0]), xytext=(-6, 14),
                     textcoords="offset points", fontsize=6.5, arrowprops=dict(arrowstyle="-", color=C["muted"], lw=0.6))
    axes[0].set(xlabel="Mature fruit accepted (%)", ylabel="Immature fruit among accepted (%)", title="(a) Fruit-level decision, spec 15 % DMC")
    axes[1].set(xlabel="Ready lots delayed (%)", ylabel="Immature lots harvested (%)", title="(b) Lot-level decision (≥ 80 % mature)")
    h_, l_ = axes[0].get_legend_handles_labels()
    fig.legend(h_, l_, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.12), fontsize=6.5)
    fig.tight_layout(); _save(fig, fdir, "fig14_harvest_frontier")


def fig_economics(cfg, fdir):
    tdir = out_dir(cfg, "tables")
    if not (tdir / "table17_economics.csv").exists():
        return
    e = pd.read_csv(tdir / "table17_economics.csv")
    z = e[(e.model == "pls") & (e.threshold == 15)]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    x = sorted(z.c_D.unique())
    for rule, m, lab, col, mk, ls in (("accept_all", 0, "Harvest all", C["muted"], "x", ":"), ("point", 0, "Point prediction", C["red"], "X", "-"),
                                      ("point_bc", 10, "Bias-corrected point (m = 10)", C["magenta"], "P", "-"), ("scp_lower", 0, "Split-CP lower bound", C["orange"], "s", "--"),
                                      ("lotcp_s_lower", 5, "LotCP-S lower bound (m = 5)", C["blue"], "o", "-")):
        g = z[(z.rule == rule) & (z.m == m) & (z.lot_size == 1000)].sort_values("c_D")
        axes[0].plot(range(len(g)), 100 * g.cost.to_numpy(), color=col, marker=mk, ls=ls, label=lab)
    axes[0].set_xticks(range(len(x))); axes[0].set_xticklabels(["1/19", "1/9", "1/4", "1/2"])
    axes[0].set(xlabel="Assumed cost of withholding a mature fruit, c_D\n(relative to accepting an immature fruit, c_I = 1)", ylabel="Expected cost per 100 fruit\n(units of fruit value)",
                title="(a) Cost by decision rule (lot of 1000 fruit)"); axes[0].legend(fontsize=6)
    for N, col, mk in ((200, C["orange"], "s"), (1000, C["blue"], "o"), (5000, C["aqua"], "^")):
        g = z[(z.rule == "lotcp_s_lower") & np.isclose(z.alpha_star, 0.1) & (z.lot_size == N)].sort_values("m")
        axes[1].plot(g.m, 100 * g.cost, color=col, marker=mk, label=f"{N} fruit per lot")
        best = g.loc[g.cost.idxmin()]
        axes[1].scatter([best.m], [100 * best.cost], s=90, facecolors="none", edgecolors=col, lw=1.4)
    axes[1].set(xlabel="Reference fruit per lot, m", ylabel="Expected cost per 100 fruit", title="(b) Choosing m (c_D = 1/9; circle = optimum)"); axes[1].legend(fontsize=6)
    fig.tight_layout(); _save(fig, fdir, "fig15_economics")


def graphical_abstract(cfg, fdir):
    """Graphical abstract: workflow strip and coverage by harvest season (from result files; SNV PLS, m = 10)."""
    ss, rl = Path("results/cycle3/season_summary.csv"), Path("results/cycle4/robust_lots.csv")
    if not (ss.exists() and rl.exists()):
        return
    s = pd.read_csv(ss)
    r = pd.read_csv(rl)
    r = r[(r.model == "pls") & (r.m == 10)]
    seasons = [2017, 2018, 2019, 2020, 2021]
    base = s[(s.model == "pls") & (s.method == "scp_sample") & (s.m == 0)].iloc[0]
    series = {"Standard error bar\n(split CP, no reference fruit)": [100 * base[f"cov_{t}"] for t in seasons],
              "Few-shot calibration\n(LotCP-S, 10 reference fruit)": [100 * r[(r.method == "S") & (r.target == t)].coverage.mean() for t in seasons],
              "Season-aware calibration\n(LotCP-R2, 10 reference fruit)": [100 * r[(r.method == "R2") & (r.target == t)].coverage.mean() for t in seasons]}
    fig = plt.figure(figsize=(7.0, 3.4))
    ax = fig.add_axes([0, 0.64, 1, 0.36]); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 20)
    steps = ["Scan mangoes\n(handheld NIR)", "Predict dry\nmatter (DMC)", "Test 5–10 fruit;\ncorrect lot\nbias & scale", "Season-aware\nconformal\nlower bound", "Harvest or\nwait / re-test"]
    cols = ["#fdeee6", "#fdeee6", "#e8f1fc", "#e8f1fc", "#e6f6ee"]
    for i, (t, c) in enumerate(zip(steps, cols)):
        x = 2 + i * 19.6
        ax.add_patch(plt.Rectangle((x, 3), 16.5, 14, fc=c, ec=C["muted"], lw=0.8))
        ax.text(x + 8.25, 10, t, ha="center", va="center", fontsize=7.5)
        if i < 4:
            ax.annotate("", (x + 19.4, 10), (x + 16.7, 10), arrowprops=dict(arrowstyle="-|>", color=C["muted"]))
    a1 = fig.add_axes([0.08, 0.12, 0.62, 0.44])
    w = 0.26
    for j, ((lab, v), col) in enumerate(zip(series.items(), [C["red"], C["muted"], C["blue"]])):
        a1.bar(np.arange(5) + (j - 1) * w, v, width=w, color=col, label=lab)
    a1.axhline(90, color=C["ink"], ls=":", lw=0.8, label="Target coverage, 90 %")
    a1.set_xticks(range(5)); a1.set_xticklabels([str(t) for t in seasons], fontsize=7); a1.set_ylim(70, 100)
    a1.set_ylabel("Coverage (%)", fontsize=7); a1.tick_params(labelsize=7)
    a1.set_title("Coverage on each later harvest season", fontsize=7.5); a1.grid(axis="x", visible=False)
    a1.legend(fontsize=6.3, frameon=False, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.text(0.5, -0.04, "Retrospective, forward-chaining evaluation on 137 later-season lots of a public mango NIR data set (SNV PLS).\n"
             "Season-aware calibration is exploratory; its width is about that of a fixed 92 % level chosen from past seasons.",
             ha="center", fontsize=6.5, color=C["muted"])
    fig.savefig(fdir / "graphical_abstract.png", dpi=300, bbox_inches="tight"); fig.savefig(fdir / "graphical_abstract.pdf", bbox_inches="tight")
    plt.close(fig)


def fig_training(cfg, fdir):
    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    cols = [C["blue"], C["orange"], C["aqua"], C["violet"], C["magenta"]]
    for t, col in zip(cfg["protocols"]["forward"]["targets"], cols):
        p = pred_path(cfg, "cnn", cfg["models"]["cnn"]["seeds"][0], "forward", t).with_suffix(".json")
        if p.exists():
            h = json.load(open(p)).get("train_loss_curve")
            ax.plot(range(1, len(h) + 1), h, color=col, label=f"target {t}")
    ax.set(xlabel="Epoch", ylabel="Training MSE (standardised)", title="1D-CNN training curves (seed 0)"); ax.set_yscale("log"); ax.legend()
    fig.tight_layout(); _save(fig, fdir, "figS1_cnn_training")


def run(cfg):
    log = get_logger("figures", cfg)
    _setup()
    fdir = out_dir(cfg, "figures")
    d = seed_average(pd.read_csv(out_dir(cfg, "results") / "raw_results.csv"))
    fig_workflow(fdir); fig_data(cfg, fdir); fig_lot_bias(cfg, fdir); fig_main(cfg, fdir, d); fig_lot_coverage(cfg, fdir, d)
    fig_ablation(cfg, fdir, d); fig_generalisation(cfg, fdir, d); fig_robustness(cfg, fdir); fig_error(cfg, fdir); fig_soil(cfg, fdir); fig_assurance(cfg, fdir, d); fig_planning(cfg, fdir); fig_harvest(cfg, fdir); fig_economics(cfg, fdir); graphical_abstract(cfg, fdir); fig_training(cfg, fdir)
    log.info("figures written to %s", fdir)


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
