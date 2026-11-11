"""Stage 5: publication figures, all drawn from machine-generated result files."""
from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
    "lotcp_noshrink": (C["aqua"], "X", "-"), "lotcp": (C["green"], "o", "-"), "lotcp_s": (C["blue"], "o", "-"),
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
    """Method schematic (no data)."""
    fig, ax = plt.subplots(figsize=(7.2, 2.9))
    ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 40)

    def box(x, y, w, h, text, fc):
        ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=C["muted"], lw=0.8))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7, color=C["ink"])

    def arrow(x0, y0, x1, y1):
        ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", color=C["muted"], lw=0.9))

    box(1, 24, 20, 13, "Past seasons\n(lots × samples × scans)\nwith reference DMC", "#e8f1fc")
    box(26, 24, 21, 13, "Season-held-out\nresiduals\n(leave-one-season-out)", "#e8f1fc")
    box(52, 28, 21, 9, "Variance components\nτ², σ², e₀", "#e8f1fc")
    box(52, 16, 21, 9, "Replay m-shot protocol\non every past lot", "#e8f1fc")
    box(78, 20, 21, 13, "Lot-balanced\nconformal quantile\nq(m)", "#e8f1fc")
    box(1, 3, 20, 13, "New lot, later season:\nall fruit scanned,\nm reference samples", "#fdeee6")
    box(26, 3, 21, 13, "Shrunk bias b̂\nlot scale ŝ\n(references + replicate scans)", "#fdeee6")
    box(78, 3, 21, 13, "Interval\nŷ + b̂ ± q(m)·ŝ", "#e6f6ee")
    arrow(21, 30.5, 26, 30.5); arrow(47, 32, 52, 32.5); arrow(47, 28, 52, 21.5); arrow(73, 32.5, 78, 29); arrow(73, 20.5, 78, 24)
    arrow(21, 9.5, 26, 9.5); arrow(47, 9.5, 78, 9.5); arrow(88.5, 20, 88.5, 16); arrow(62.5, 28, 40, 16)
    ax.text(1, 38.5, "Calibration (source information only)", fontsize=7.5, color=C["muted"])
    ax.text(1, 17, "Deployment", fontsize=7.5, color=C["muted"])
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
    for method in ("biascorr_naive", "target_only_centred", "lotcp_noshrink", "lotcp", "lotcp_s"):
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
    ax.set_xticklabels([f"{LABEL[k]}\n(m = {m})" for k, m in items], fontsize=6.5)
    ax.set(ylabel="Coverage within lot", title="Lot-wise coverage on later-season lots (each dot = one lot; bar = mean)")
    fig.tight_layout(); _save(fig, fdir, "fig5_lot_coverage")


def fig_ablation(cfg, fdir, d):
    a0 = cfg["eval"]["primary_alpha"]
    main = d[(d.model == "pls") & (d.protocol == "forward") & np.isclose(d.alpha, a0)]
    order = ["lotcp_s", "lotcp_s_support", "lotcp_s_rep", "lotcp", "lotcp_noshrink", "lotcp_noepisodic", "lotcp_lotfold", "lotcp_samplefold", "lotcp_pooled"]
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
    r = pd.read_csv(p).replace(np.inf, np.nan)
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
            g = g.assign(level=g["level"].str.split(":").str[0])
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
    fig_ablation(cfg, fdir, d); fig_generalisation(cfg, fdir, d); fig_robustness(cfg, fdir); fig_error(cfg, fdir); fig_training(cfg, fdir)
    log.info("figures written to %s", fdir)


if __name__ == "__main__":
    import sys

    from src.utils import load_config

    run(load_config(sys.argv[1] if len(sys.argv) > 1 else "full"))
