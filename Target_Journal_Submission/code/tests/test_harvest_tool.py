import numpy as np
import pandas as pd

from src.tool.harvest_tool import decide


def _cal():
    lev = {"q_lower": 1.3, "q_two_sided": 1.6, "planned_width": 3.2}
    const = {"mu": 0.0, "sigma2": 0.5, "e0": 0.2, "nu0": 10}
    return {"alpha": 0.1, "delta": 0.1,
            "levels": {str(m): {"marginal": lev, "assured": dict(lev, q_lower=1.8), "constants": const} for m in (0, 3, 5, 10)}}


def test_decide_corrects_bias_and_flags_fruit():
    rng = np.random.default_rng(0)
    truth = rng.normal(16.0, 1.0, 40)
    pred = truth + 2.0                                   # instrument over-predicts by 2 % DMC
    scans = pd.DataFrame({"fruit_id": np.repeat(np.arange(40), 2), "prediction": np.repeat(pred, 2) + rng.normal(0, 0.1, 80)})
    refs = pd.DataFrame({"fruit_id": np.arange(10), "dry_matter": truth[:10]})
    out, summary = decide(_cal(), scans, refs, spec=15.0)
    assert summary["reference_fruit_used"] == 10 and summary["calibration_level_m"] == 10
    assert abs(summary["lot_bias_correction"] + 2.0) < 0.2           # bias recovered from the references
    assert len(out) == 30 and set(out["decision"]) <= {"HARVEST", "WAIT-RETEST"}
    assert (out["lower_bound"] < out["corrected_prediction"]).all()
    _, s2 = decide(_cal(), scans, refs, spec=15.0, mode="assured")       # assured bound is more cautious
    assert float(s2["fruit_cleared_for_harvest"].rstrip(" %")) <= float(summary["fruit_cleared_for_harvest"].rstrip(" %"))
