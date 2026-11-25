"""plan_v6 stage A: do label-free lot statistics predict lot bias? Indicator chosen on source lots, tested on target lots."""
import json

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

from src.data.dataset import load_data
from src.evaluation.lotcp import replicate_variance
from src.models.point import make_model
from src.training.crossfit import pred_path
from src.utils import load_config, out_dir

IND = ["T2", "Q", "rep_var", "pred_offset"]


def lot_features(model, X, pred, lot, smp, Ttr, mu_pred):
    Xp = model._prep(X)
    T = model.model.transform(Xp)
    G = np.linalg.inv(np.cov(Ttr, rowvar=False))
    t2 = np.einsum("ij,jk,ik->i", T, G, T)
    rec = model.model.inverse_transform(T)
    q = ((Xp - rec) ** 2).sum(1)
    rows = []
    for l in np.unique(lot):
        k = lot == l
        _, inv = np.unique(smp[k], return_inverse=True)
        rows.append(dict(lot=int(l), T2=float(np.median(t2[k])), Q=float(np.median(q[k])), rep_var=replicate_variance(pred[k], inv),
                         pred_offset=float(abs(pred[k].mean() - mu_pred))))
    return pd.DataFrame(rows)


def main():
    cfg = load_config("full")
    d = load_data(cfg)
    out = []
    for target in (2017, 2018, 2019, 2020, 2021):
        P = np.load(pred_path(cfg, "pls", 0, "forward", target))
        nc = json.load(open(str(pred_path(cfg, "pls", 0, "forward", target)).replace(".npz", ".json")))["n_components"]
        src, tgt = P["src_idx"], P["tgt_idx"]
        final = make_model("pls", cfg, 0, n_components=nc).fit(d.X[src], d.y[src])
        Ttr = final.model.transform(final._prep(d.X[src]))
        mu = float(final.predict(d.X[src]).mean())
        fs = lot_features(final, d.X[src], P["oof_season"], d.lot[src], d.sample[src], Ttr, mu)
        rs = pd.Series(d.y[src] - P["oof_season"]).groupby(d.lot[src]).mean().abs()
        fs["abs_bias"] = fs.lot.map(rs); fs["set"] = "source"
        ft = lot_features(final, d.X[tgt], P["pred_tgt"], d.lot[tgt], d.sample[tgt], Ttr, mu)
        rt = pd.Series(d.y[tgt] - P["pred_tgt"]).groupby(d.lot[tgt]).mean().abs()
        ft["abs_bias"] = ft.lot.map(rt); ft["set"] = "target"
        for f in (fs, ft):
            f["target"] = target
        out += [fs, ft]
    df = pd.concat(out)
    df.to_csv(out_dir(cfg, "results/cycle4") / "shift_indicators.csv", index=False)
    res = []
    for s in ("source", "target"):
        g = df[df.set == s]
        for i in IND:
            rho = spearmanr(g[i], g.abs_bias, nan_policy="omit").correlation
            per = [spearmanr(x[i], x.abs_bias, nan_policy="omit").correlation for _, x in g.groupby("target")]
            res.append(dict(set=s, indicator=i, spearman_pooled=rho, spearman_by_target_mean=float(np.nanmean(per))))
    res = pd.DataFrame(res)
    src_best = res[res.set == "source"].assign(a=lambda x: x.spearman_by_target_mean.abs()).sort_values("a").indicator.iloc[-1]
    tgt_row = res[(res.set == "target") & (res.indicator == src_best)].iloc[0]
    srow = res[(res.set == "source") & (res.indicator == src_best)].iloc[0]
    go = abs(tgt_row.spearman_by_target_mean) >= 0.30 and np.sign(tgt_row.spearman_by_target_mean) == np.sign(srow.spearman_by_target_mean)
    res.to_csv(out_dir(cfg, "results/cycle4") / "shift_indicators_screen.csv", index=False)
    json.dump(dict(chosen_on_source=src_best, target_spearman=float(tgt_row.spearman_by_target_mean), go=bool(go)),
              open("results/cycle4/shift_indicators_decision.json", "w"), indent=1)
    print(res.round(3).to_string(index=False)); print("chosen", src_best, "GO" if go else "NO-GO")


if __name__ == "__main__":
    main()
