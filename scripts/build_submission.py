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
    ("S13", "table13_soil", "External validation on OSSL soil vis-NIR spectra: all methods and m."),
    ("S13b", "table13b_soil_point", "Soil data: point-prediction error in the source (cross-validation) and on the target."),
    ("S13c", "table13c_soil_tests", "Soil data: paired Wilcoxon tests of LotCP-S against competing methods."),
    ("S16", "table16_harvest_fruit", "Harvest simulator, fruit level: every rule, confidence level, specification (14, 15, 16 % DMC), number of reference fruit and predictor (PLS, CNN)."),
    ("S17", "table17_economics", "Expected cost per fruit under assumed costs for every rule, cost ratio, lot size, specification and predictor."),
    ("S17b", "table17b_regret", "Relative regret of the cost-derived confidence level α* against the best level in hindsight."),
    ("S18", "table18_lot_decisions", "Harvest simulator, lot level: premature harvests and delays for every rule and setting."),
    ("S19", "table19_planner", "Reference-sampling planner: planned and realised widths, lot-level coverage and reference cost."),
    ("S20", "table20_tests_main", None),
    ("S21", "table21_generalisation_main", None),
    ("S22", "table22_robustness_main", None),
    ("S23", "table23_alpha_main", None),
    ("S24", "table24_cost_main", None),
    ("S15", "table15_planning", "Reference-budget planning: relative difference between realised and planned interval width, by predictor and variant."),
    ("S15b", "table15b_planning_by_season", "Reference-budget planning: relative difference by target season."),
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
    notes = sdir / "Supplementary_Notes.md"
    if notes.exists():
        md.append(notes.read_text())
    md.append("\n# Supplementary tables\n")
    for tag, name, cap in SUPP_TABLES:
        if cap is None:                       # table already formatted with caption by the manuscript builder
            q = ROOT / "tables" / f"{name}.md"
            if q.exists():
                md.append("\n" + q.read_text())
            continue
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


AUTHORS = "P N Bhargav Teja, Ragavan K"
CORR = "Ragavan K"


def _doc(size=11):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name, st.font.size = FONT, Pt(size)
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Cm(2.5)
    return doc


def _paras(doc, paras, spacing=1.15):
    for t in paras:
        p = doc.add_paragraph(t)
        p.paragraph_format.space_after = Pt(9)
        p.paragraph_format.line_spacing = spacing


def cover_letter(r):
    doc = _doc()
    _paras(doc, [
        f"{CORR}\n[Department, Institution, City, Postal code, Country]\n[E-mail address] · [Telephone]",
        "[Date]",
        f"To the Editor-in-Chief\n{JOURNAL}",
        "Dear Editor,",
        f"On behalf of my co-author, I submit the manuscript “{TITLE}” by {AUTHORS} for consideration as a research article in {JOURNAL}.",
        "Mango growers decide when to harvest a block by scanning fruit with handheld near-infrared (NIR) spectrometers and "
        "comparing the predicted dry matter content with a maturity specification. The calibrations behind these readings are "
        "built on past seasons, and so are their error bars. Using a public data set with seven harvest seasons "
        f"and {r.V['n_lots']} harvest lots, we audit such error bars lot by lot on later seasons: at a nominal 90 % they covered only "
        f"{100*min(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}–"
        f"{100*max(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f} % of the reference values.",
        "We then study a few-shot conformal calibration in which a few fruit per lot are tested destructively. With five to ten "
        f"reference fruit it raised coverage in every target season, to {r.ss('lotcp_s',10):.3f} pooled ({r.ss('lotcp_s',10,'coverage_ex2017'):.3f} "
        "without the first, over-covered target season). Matched comparisons show which parts of the calibration matter, and "
        "where it falls short: shifts between seasons that past seasons do not span leave coverage slightly below nominal, and "
        "a lot-level guarantee held pooled but not season by season. In an exploratory harvest simulation under explicitly "
        "assumed costs, deciding on a calibrated lower bound instead of the point value lowered the expected cost in every "
        "season; additional reference fruit gave no detectable further saving. We report these limits, including an "
        "efficiency endpoint that was not confirmed on independent handheld-NIR data, as findings rather than footnotes.",
        f"We believe the work fits the scope of {JOURNAL} because it gives users of handheld NIR instruments an evidence-based "
        "account of when an error bar can be trusted for a harvest decision, and a practical procedure for checking it. The "
        "evaluation is retrospective, the costs are assumed and labelled as such, and a prospective orchard validation remains to be done.",
        "The manuscript is original, has not been published, and is not under consideration elsewhere. [Both authors have "
        "approved the submission — to be confirmed by the authors.] The study uses public data sets and involves no human participants or animals. The authors "
        "declare no competing interests, and the research received no specific funding. The use of generative AI in the "
        "research and in preparing the manuscript is declared in the manuscript. The data are publicly available at the links given in the data "
        "availability statement, and the code is available from the corresponding author on reasonable request.",
        "Thank you for considering our manuscript.",
        f"Yours sincerely,\n\n{CORR}\nCorresponding author, on behalf of both authors",
    ])
    out = ROOT / "manuscript" / "cover_letter.docx"
    doc.save(str(out))
    return out


def title_page():
    doc = _doc(12)
    h = doc.add_paragraph(); run = h.add_run(TITLE); run.bold = True; run.font.size = Pt(14)
    _paras(doc, [
        "Article type: Research article",
        "P N Bhargav Teja (a), Ragavan K (a, *)",
        "(a) [Department, Institution, City, Postal code, Country]",
        f"* Corresponding author: {CORR}, [e-mail address], [postal address], [telephone]",
        "E-mail addresses: P N Bhargav Teja, [e-mail address]; Ragavan K, [e-mail address]",
        "Author contributions (CRediT): P N Bhargav Teja: Conceptualization, Methodology, Software, Validation, Formal analysis, "
        "Investigation, Data curation, Visualization, Writing – original draft, Writing – review & editing. Ragavan K: Supervision.",
        "Funding: This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.",
        "Declaration of competing interest: The authors declare that they have no known competing financial interests or personal "
        "relationships that could have appeared to influence the work reported in this paper.",
        "Acknowledgements: The authors thank the creators of the mango data set at Central Queensland University and the developers "
        "of the Open Soil Spectral Library for making their data public.",
    ])
    doc.save(str(ROOT / "manuscript" / "title_page.docx"))


def competing_interest():
    doc = _doc(12)
    h = doc.add_paragraph(); h.add_run("Declaration of interests").bold = True
    _paras(doc, ["☒ The authors declare that they have no known competing financial interests or personal relationships that could have "
                 "appeared to influence the work reported in this paper.",
                 "☐ The authors declare the following financial interests/personal relationships which may be considered as potential competing interests:",
                 f"Manuscript: {TITLE}", f"Authors: {AUTHORS}"])
    doc.save(str(ROOT / "manuscript" / "declaration_of_competing_interest.docx"))


def anonymised_manuscript():
    """Same manuscript without author names, affiliations, contributions and acknowledgements (for double-anonymised review)."""
    import re as _re

    from manuscript.build_manuscript import to_docx

    md = (ROOT / "manuscript" / "build" / "manuscript.md").read_text()
    a = md.index("---", 3) + 3
    b = md.index("# Abstract")
    md = md[:a] + "\n\n" + md[b:]
    md = _re.sub(r"(# CRediT authorship contribution statement\n\n).*?(?=\n# )", r"\1[Removed for anonymised review; see title page.]\n", md, flags=_re.S)
    md = _re.sub(r"(# Acknowledgements\n\n).*?(?=\n# )", r"\1[Removed for anonymised review; see title page.]\n", md, flags=_re.S)
    out = ROOT / "manuscript" / "build" / "manuscript_anonymised.md"
    out.write_text(md)
    to_docx(out, ROOT / "manuscript" / "Manuscript_anonymised.docx")


def export_figures(dst: Path):
    """Copy every manuscript figure under its final number (Figure_N.png at 300 dpi and Figure_N.pdf)."""
    import re as _re

    md = (ROOT / "manuscript" / "build" / "manuscript.md").read_text()
    dst.mkdir(parents=True, exist_ok=True)
    captions = []
    for mo in _re.finditer(r"!\[Fig\. (\d+)\. ([^\]]*)\]\((figures/[^)]+)\.png\)", md):
        n, cap, stem = mo.group(1), mo.group(2), mo.group(3)
        for ext in ("png", "pdf"):
            shutil.copy2(ROOT / f"{stem}.{ext}", dst / f"Figure_{n}.{ext}")
        captions.append(f"Fig. {n}. {cap}")
    (dst / "Figure_captions.txt").write_text("\n\n".join(captions) + "\n")
    return len(captions)


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


def make_zip():
    """Assemble the journal submission folder and zip (manuscript files only; code is available on request)."""
    import zipfile

    name = "Smart_Agricultural_Technology_Submission"
    d = ROOT / name
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir()
    M = ROOT / "manuscript"
    files = {"01_Cover_Letter.docx": M / "cover_letter.docx", "02_Title_Page.docx": M / "title_page.docx",
             "03_Highlights.docx": M / "highlights.docx", "04_Manuscript_with_author_details.docx": M / "Final_Manuscript.docx",
             "04_Manuscript_with_author_details.pdf": M / "Final_Manuscript.pdf", "05_Manuscript_anonymised.docx": M / "Manuscript_anonymised.docx",
             "05_Manuscript_anonymised.pdf": M / "Manuscript_anonymised.pdf", "06_Graphical_Abstract.png": ROOT / "figures" / "graphical_abstract.png",
             "06_Graphical_Abstract.pdf": ROOT / "figures" / "graphical_abstract.pdf", "08_Supplementary_Material.docx": ROOT / "supplementary" / "Supplementary_Material.docx",
             "09_Declaration_of_Competing_Interest.docx": M / "declaration_of_competing_interest.docx"}
    for k, v in files.items():
        shutil.copy2(v, d / k)
    nfig = export_figures(d / "07_Figures")
    (d / "00_README_Submission_Checklist.txt").write_text(f"""Submission package for {JOURNAL} (Elsevier)
Manuscript: {TITLE}
Authors: {AUTHORS} (corresponding author: {CORR})

Contents
  01 Cover letter                     02 Title page (author details, CRediT, funding, declarations)
  03 Highlights (5 bullets, <= 85 characters each)
  04 Manuscript with author details (DOCX + PDF)   05 Anonymised manuscript (use if the journal requests double-anonymised review)
  06 Graphical abstract (PNG 300 dpi + PDF)        07 Figures 1-{nfig}, separate files (PNG 300 dpi + vector PDF) and captions
  08 Supplementary material (notes S1-S8, tables S1-S24, figure S1)
  09 Declaration of competing interest

Before uploading, complete and verify:
  [ ] Affiliations, e-mail addresses and postal address of both authors (placeholders in square brackets in 01, 02, 04)
  [ ] Check every item against the journal's current Guide for Authors (it could not be retrieved while preparing the package)
  [ ] Confirm the bracketed statement in 01 that both authors approved the submission
  [ ] Confirm the review model (single- or double-anonymised) and upload 04 or 05 accordingly
  [ ] Read and verify the analysis, the code and every reference: the authors take full responsibility for the content
  [ ] Confirm that the generative-AI declaration in the manuscript accurately describes how AI was used, and that this use
      is acceptable under the journal's current policy
  [ ] Data: public links are given in the Data availability statement; code is stated as available on reasonable request
""")
    z = ROOT / f"{name}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(d.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(ROOT))
    return z


def main():
    from manuscript.build_manuscript import R

    r = R()
    supplementary(); cover_letter(r); highlights_file(); title_page(); competing_interest(); anonymised_manuscript()
    for sub in ("manuscript", "code", "results", "figures", "tables", "supplementary"):
        shutil.rmtree(OUT / sub, ignore_errors=True)
    _copy(ROOT / "manuscript", OUT / "manuscript", ("Final_Manuscript.docx", "Final_Manuscript.pdf", "Manuscript_anonymised.docx", "Manuscript_anonymised.pdf",
                                                    "cover_letter.docx", "highlights.docx", "title_page.docx", "declaration_of_competing_interest.docx"))
    code = OUT / "code"
    for d in ("src", "experiments", "tests", "config", "scripts"):
        shutil.copytree(ROOT / d, code / d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(ROOT / "manuscript", code / "manuscript", ignore=shutil.ignore_patterns("__pycache__", "build", "*.docx", "*.pdf"))
    for f in ("run_all.py", "requirements.txt", "requirements-lock.txt", "environment.yml", "README.md", "LICENSE"):
        shutil.copy2(ROOT / f, code / f)
    res = OUT / "results"
    _copy(ROOT / "results", res, ("raw_results.csv", "point_results.csv", "metrics.json", "statistics.json", "calibration_info.json", "run_timing.json", "tool_demo.json"))
    for sub in ("robustness", "harvest", "soil", "experiment_logs"):
        _copy(ROOT / "results" / sub, res / sub)
    (res / "README.md").write_text("Stored model predictions (results/predictions/, ~50 MB) are in the repository root, not duplicated here.\n")
    _copy(ROOT / "figures", OUT / "figures")
    _copy(ROOT / "tables", OUT / "tables")
    _copy(ROOT / "supplementary", OUT / "supplementary")
    shutil.copy2(ROOT / "experiments" / "PROTOCOL.md", OUT / "supplementary" / "PROTOCOL.md")
    z = make_zip()
    print("submission package written to", OUT, "and", z)


if __name__ == "__main__":
    main()
