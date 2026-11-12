"""Assemble Target_Journal_Submission/ from the generated outputs (nothing is typed by hand).

    python -m scripts.build_submission
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pandas as pd
from docx import Document
from docx.shared import Cm, Pt

from manuscript.build_manuscript import TITLE
from manuscript.docx_format import FONT, make_reference_doc, postprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Target_Journal_Submission"
JOURNAL = "Smart Agricultural Technology"

SUPP_TABLES = [
    ("S1", "table1_dataset", "Data set by season."),
    ("S2", "table2_point_models_by_seed", "Point predictors: every seed and target season (RMSE, bias, R², cross-validation errors, fit time)."),
    ("S3", "table3_main_intervals", "All interval methods, all m (PLS, forward chaining, nominal 0.90), with bootstrap CIs."),
    ("S4", "table4_per_season", "Coverage, width and interval score by target season."),
    ("S4b", "table4b_season_jackknife", "Leave-one-season-out jackknife of the pooled lot-macro coverage and per-season extremes."),
    ("S5", "table5_ablation", "Ablation variants, all m."),
    ("S6", "table6_tests", "All paired Wilcoxon tests of LotCP-S against every other method (interval score and absolute coverage error)."),
    ("S6b", "table6b_tests_no_replicates", "Paired tests for LotCP-S without replicate-scan information against the bias-correction and target-only baselines."),
    ("S7", "table7_generalisation", "Predictors and protocols."),
    ("S7b", "table7b_seed_spread", "Seed-to-seed spread of lot-macro metrics (LightGBM, CNN)."),
    ("S8", "table8_alpha", "Nominal levels 0.80, 0.90, 0.95."),
    ("S9", "table9_point_correction", "Point-prediction error after bias correction as a function of m."),
    ("S10", "table11b_crossfit_cost", "Cross-fitting time per target season (three fold schemes plus final model)."),
    ("S11", "table12_spiking", "Spiking baseline (refit with the reference samples added) at m = 10."),
]


def _copy(src: Path, dst: Path, patterns=("*",)):
    dst.mkdir(parents=True, exist_ok=True)
    for pat in patterns:
        for f in src.glob(pat):
            if f.is_file():
                shutil.copy2(f, dst / f.name)


def supplementary():
    sdir = ROOT / "supplementary"
    sdir.mkdir(exist_ok=True)
    md = [f"---\ntitle: \"Supplementary material: {TITLE}\"\n---\n",
          "All tables in this file are written by `src/statistics/analysis.py` from the raw result files; "
          "the same tables are provided as CSV files.\n"]
    for tag, name, cap in SUPP_TABLES:
        p = ROOT / "tables" / f"{name}.csv"
        if not p.exists():
            continue
        df = pd.read_csv(p)
        if len(df) > 120:
            md.append(f"\n**Table {tag}.** {cap} ({len(df)} rows; provided as `{name}.csv` only.)\n")
            continue
        md.append("\n" + (ROOT / "tables" / f"{name}.md").read_text() + f"\nTable: Table {tag}. {cap}\n")
    md.append("\n![Fig. S1. Training loss of the 1D-CNN (seed 0) for the five target seasons.](figures/figS1_cnn_training.png){width=3.5in}\n")
    md.append("\n# Pre-specified protocol and deviation log\n\n" + (ROOT / "experiments" / "PROTOCOL.md").read_text().replace("\n# ", "\n## "))
    (sdir / "Supplementary_Material.md").write_text("\n".join(md))
    ref = make_reference_doc(ROOT / "manuscript" / "build" / "reference.docx")
    out = sdir / "Supplementary_Material.docx"
    subprocess.run(["pandoc", str(sdir / "Supplementary_Material.md"), "-o", str(out), "--reference-doc", str(ref),
                    "--resource-path", str(ROOT), "--from", "markdown+pipe_tables+table_captions"], check=True, cwd=ROOT)
    doc = Document(str(out))
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = 1.0
                    for r in p.runs:
                        r.font.size = Pt(7)
    for p in doc.paragraphs:
        p.paragraph_format.line_spacing = 1.15
    doc.save(str(out))


def cover_letter():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name, st.font.size = FONT, Pt(11)
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.5)
    sec.top_margin = sec.bottom_margin = Cm(2.5)
    paras = [
        "[Corresponding author name]\n[Institution, address]\n[E-mail] · [Telephone]",
        "[Date]",
        f"To the Editor-in-Chief\n{JOURNAL}",
        "Dear Editor,",
        f"We submit the manuscript “{TITLE}” for consideration as a research article in {JOURNAL}.",
        "Handheld near-infrared spectrometers are used in orchards to decide when to harvest fruit. The calibrations behind "
        "them are built on previous seasons, and the error bars that accompany their predictions are derived from those same "
        "seasons. Using a public mango data set with seven harvest seasons and 199 harvest lots, we measure what happens to "
        "such error bars on later seasons: at a nominal 90 %, seven common interval procedures, including split conformal "
        "prediction, quantile models, deep ensembles and Monte-Carlo dropout, cover between about 77 % and 85 % of the "
        "reference values, and the failures are concentrated in individual lots.",
        "The manuscript then asks the operational question of how many destructively measured reference fruit per lot are "
        "needed for a valid and useful interval, and how they should be used. We describe a calibration, LotCP, that applies "
        "hierarchical conformal prediction to the lot structure of multi-season calibration sets, corrects the lot bias from a "
        "few reference samples, adapts the interval to a lot-specific scale that also uses repeated scans, and prices the "
        "estimation error by replaying the procedure on past lots. With three to ten reference samples per lot it gave "
        "close-to-nominal coverage across three predictors and narrower intervals than the alternatives; with twenty or more, "
        "calibration on the reference samples alone was equally good. The manuscript reports these boundaries, an ablation in "
        "which one motivating component (shrinkage) turned out not to matter, and the lots on which the method still fails.",
        f"We believe the work fits the scope of {JOURNAL} because it concerns the reliable use of a sensing instrument in "
        "agricultural production and leads to a concrete sampling recommendation. The experimental protocol was written "
        "before any model was trained, deviations from it are listed in the manuscript, and the code, stored predictions and "
        "all result files are provided so that every table and figure can be regenerated.",
        "The manuscript is original, has not been published, and is not under consideration elsewhere. All authors have "
        "approved the submission. The study uses a public data set (CC BY 4.0) and involves no human participants or animals. "
        "The authors declare no competing interests. The use of generative AI in preparing the work is declared in the "
        "manuscript. [Authors: confirm each statement in this paragraph before sending.]",
        "Closely related concurrent work that the editor may wish to be aware of is cited in the manuscript (a study of "
        "conformal coverage under instrument transfer, available as a code archive).",
        "Thank you for considering our manuscript.",
        "Yours sincerely,\n\n[Corresponding author name]\non behalf of all authors",
    ]
    for t in paras:
        p = doc.add_paragraph(t)
        p.paragraph_format.space_after = Pt(9)
        p.paragraph_format.line_spacing = 1.15
    out = ROOT / "manuscript" / "cover_letter.docx"
    doc.save(str(out))
    return out


def highlights_file():
    md = (ROOT / "manuscript" / "build" / "manuscript.md").read_text()
    a = md.index("# Highlights"); b = md.index("# 1. Introduction")
    lines = [l[2:].strip() for l in md[a:b].splitlines() if l.startswith("- ")]
    too_long = [l for l in lines if len(l) > 85]
    if too_long:
        raise SystemExit(f"highlights longer than 85 characters: {too_long}")
    doc = Document()
    doc.styles["Normal"].font.name, doc.styles["Normal"].font.size = FONT, Pt(12)
    doc.add_paragraph("Highlights").runs[0].bold = True
    doc.add_paragraph(TITLE)
    for l in lines:
        doc.add_paragraph(l, style="List Bullet")
    doc.save(str(ROOT / "manuscript" / "highlights.docx"))


def main():
    supplementary(); cover_letter(); highlights_file()
    for sub in ("manuscript", "code", "results", "figures", "tables", "supplementary"):
        shutil.rmtree(OUT / sub, ignore_errors=True)
    _copy(ROOT / "manuscript", OUT / "manuscript", ("Final_Manuscript.docx", "Final_Manuscript.pdf", "cover_letter.docx", "highlights.docx"))
    code = OUT / "code"
    for d in ("src", "experiments", "tests", "config", "scripts"):
        shutil.copytree(ROOT / d, code / d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(ROOT / "manuscript", code / "manuscript", ignore=shutil.ignore_patterns("__pycache__", "build", "*.docx", "*.pdf"))
    for f in ("run_all.py", "requirements.txt", "requirements-lock.txt", "environment.yml", "README.md", "LICENSE"):
        shutil.copy2(ROOT / f, code / f)
    res = OUT / "results"
    _copy(ROOT / "results", res, ("raw_results.csv", "point_results.csv", "metrics.json", "statistics.json", "calibration_info.json", "run_timing.json"))
    _copy(ROOT / "results" / "robustness", res / "robustness")
    _copy(ROOT / "results" / "experiment_logs", res / "experiment_logs")
    (res / "README.md").write_text("Stored model predictions (results/predictions/, ~50 MB) are in the repository root, not duplicated here.\n")
    _copy(ROOT / "figures", OUT / "figures")
    _copy(ROOT / "tables", OUT / "tables")
    _copy(ROOT / "supplementary", OUT / "supplementary")
    shutil.copy2(ROOT / "experiments" / "PROTOCOL.md", OUT / "supplementary" / "PROTOCOL.md")
    print("submission package written to", OUT)


if __name__ == "__main__":
    main()
