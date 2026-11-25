# Review round 2 — merged triage, 2026-11-25
Scores: R1 6/10 major; R2 5/10 major, blind novelty 11/25 (differentiation 2, mechanism 3, evidence 2, breadth 2, significance 2); R3 6/10 major.
Verdict: not clean. G10 fail.

## MAJOR
| id | concern | type | action |
|---|---|---|---|
| R1-1 | season CIs bootstrapped the pooled mean, estimate was season mean | E (bug) | experiments/season_inference.py: descriptive t-interval (4 df) on the five season differences; pooled bootstrap kept separately; conclusions unchanged except published-PLS score gain now from m=5, (b′) gain not resolved at every m |
| R1-2 | "every season" false | W | Highlight 1 "most seasons"; Discussion gives pooled method range and per-season range for sample-fold split CP |
| R1-3 | "no further saving" too strong; point rule weak comparator | W | "no detectable further saving at the assumed operating point"; zero-cost reference tests bound reported; CI half-width stated; comparator rationale and weakness of point rule stated |
| R1-4, R3-1 | failed confirmation absent from abstract; exploratory labels | W | Abstract states the efficiency gain was not confirmed on independent data; post hoc labels in abstract, highlights, conclusion, contribution 4 |
| R2-1 | few-shot hierarchical score is prior work; GHCP missing | W | GHCP (arXiv 2608.15500) and SymmPI (arXiv 2312.16160) verified and cited; contribution narrowed (replay not new; additions: season-held-out residuals, label-free lot scale, lot-level variant, season audit). No empirical comparison with GHCP (no code; would need reimplementation) — limitation |
| R2-2 | practical significance vs bias correction | W | Results and Practical procedure now say bias correction + sample-fold half-width is the safer simple option when coverage matters; when LotCP-S is preferable. Title change suggested by R2 NOT made: the title was specified by the author |
| R3-2 | availability inconsistent | W | Author instruction: code on request. Made consistent: protocol files, code, results on request; repository paths removed from text and captions |
| R3-3 | "pre-registered" | W | removed everywhere |
| R3-4 | "in response to review" unexplained | W | "internal, AI-simulated review"; AI declaration lists the analyses it triggered |
| R3-5 | README overstates --from eval | W | README corrected: --from eval regenerates main results only; cycle 2–3 scripts listed; run-state logic documented; data file name explained |

## MINOR (done unless noted)
R1-6 averaging named; R1-7 comparator rationale; R1-8 LOSO costs defined as season means without reference cost; R1-9 LV grid and second test set reported; R1-11 typos fixed. R2-3/4/5 references added (anderson2019harvest, peirs2003, bobelyn2010, mishra2020dipls, huang2025soilcp; all verified on Crossref); R2-6 citation wording fixed; R2-7 preprints labelled, Wilcoxon/Holm/Kerby/Efron cited where used; R2-8 ex-2017 values in abstract; R2-9 no external support for shift repair stated. R3-6 cross-references fixed; R3-7 typos; R3-8 S7 aligned with main text; R3-10 supplement order + guide; R3-11 affiliation placeholders need author input (not fabricated); R3-12/13/14 done.

## Not fixable within the study
G3 novelty (blind 11/25 < 20): breadth limited by data availability (no second fruit set), differentiation limited by GHCP/Lee et al. A higher score needs a new data source or a different contribution (pivot decision).
