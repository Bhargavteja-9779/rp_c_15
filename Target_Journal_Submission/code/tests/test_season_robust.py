"""Season-level statement of the season-robust replay (Appendix A, Proposition 3), checked by simulation."""
import numpy as np

from src.evaluation.lotcp import LotCP


def _season(rng, season_id, n_lots=12, n_s=25, n_rep=2):
    c = np.exp(rng.normal(0, 0.35))              # season-specific error scale (the shift that past seasons do not span)
    r, lot, smp, grp = [], [], [], []
    for l in range(n_lots):
        b = rng.normal(0, 1.0 * c)
        for i in range(n_s):
            u = rng.normal(0, 0.8 * c)
            for _ in range(n_rep):
                r.append(b + u + rng.normal(0, 0.3 * c)); lot.append(season_id * 100 + l)
                smp.append((season_id * 100 + l) * 1000 + i); grp.append(season_id)
    return np.array(r), np.array(lot), np.array(smp), np.array(grp)


def test_kth_largest_season_quantile_covers_new_season():
    # 150 repetitions; the constants are fitted on the past seasons only, a small asymmetry that can put the rate a few
    # points below the exchangeable bound (over 600 repetitions the rate was 0.74 for a bound of 0.75)
    S, k, reps, hits = 3, 1, 150, 0
    for rep in range(reps):
        rng = np.random.default_rng(1000 + rep)
        parts = [_season(rng, s) for s in range(S + 1)]
        r, lot, smp, grp = (np.concatenate([p[j] for p in parts]) for j in range(4))
        src = grp < S
        cp = LotCP(m=5, alpha=0.1, n_episodes=5, min_query=10).fit(r[src], lot[src], smp[src])
        q_all = cp.group_quantiles(r, lot, smp, None, grp, seed=rep)
        past = sorted(q_all[s] for s in range(S))
        hits += q_all[S] <= past[-k]
    bound = (S + 1 - k) / (S + 1)
    assert hits / reps >= bound - 0.10, (hits / reps, bound)
