# Review round 7 — Reviewer #7 (writing, logic, notation, figures, references, author guidelines)

| # | Severity | Issue | Outcome |
|---|---|---|---|
| 7.1 | MAJOR | Abstract exceeded 250 words and contained an unsupported superlative. | Rewritten: 249 words, superlative removed, all figures generated from result files. |
| 7.2 | MAJOR | Several sentences in the first draft stated numbers by hand ("about twice the prior", "seven to fourteen points"). | Replaced by generated values or corrected ("six to fourteen", now qualified by method and predictor). Remaining hand-written quantities in the discussion ("about a third wider", "0.82 to 0.99") were checked against Tables 3 and 5. |
| 7.3 | MODERATE | "LotCP-S covers 0.919–0.914" (range written in the order of m). | Now min–max. |
| 7.4 | MODERATE | Notation: r, r̃, r̄ and the three levels (lot k, sample i, scan j) must be used consistently; Eq. (4) used x_ij without the lot index. | Checked. Eq. (4) refers to the new lot, where the lot index is dropped by design; stated in the text ("in the new lot"). |
| 7.5 | MODERATE | Terminology drift: "population", "lot", "block"; "reference sample", "reference fruit", "label". | "Lot" and "reference sample" are used throughout the methods and results; "reference fruit" only in title, abstract, highlights and discussion where the practical meaning is intended; "population" only when describing the data file. |
| 7.6 | MODERATE | Physiological-stage labels were paraphrased ("hard green") beyond what the data file says. | Now "green stage" and "ripening stage", the file's categories. |
| 7.7 | MODERATE | Highlights must be ≤ 85 characters. | Checked automatically by `scripts/build_submission.py` (longest: 85). |
| 7.8 | MODERATE | Figure quality: colour-only encoding. | Every series also has a distinct marker or line style; palette checked with a colour-vision-deficiency validator; figures saved at 300 dpi PNG and vector PDF. |
| 7.9 | MODERATE | Reference list: three preprints/archives (SSRN ×2, Zenodo) and one arXiv paper are cited. | Kept because they are the closest related work; each is marked as preprint/archive in the list. Bibliographic data of all 44 entries were checked against Crossref (or arXiv/Zenodo/Mendeley records); NeurIPS/ICML/JMLR entries without DOI were entered from the proceedings records. |
| 7.10 | MINOR | LibreOffice PDF rendering dropped all equations before the Math component and symbol fonts were installed. | Fixed in the build environment; README lists the requirement. The DOCX contains native Word equations (169 inline, 7 display). |
| 7.11 | MINOR | Body text follows tables without spacing in places. | Cosmetic; left for copy-editing. |
| 7.12 | MINOR | The manuscript is long (≈ 12,700 words with tables). | No length limit could be verified for the journal (guide not retrievable). If a limit applies, Sections 9–11 can move to the supplement. |

Guideline compliance could only be checked against generic Elsevier requirements (see `journal_selection/`).
