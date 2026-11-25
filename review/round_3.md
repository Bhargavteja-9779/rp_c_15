# Review round 3 — merged triage, 2026-11-25
Scores: R1 5/10 major; R2 5/10 major, blind novelty 12/25 (differentiation 2, mechanism 3, evidence 2, breadth 2, significance 3); R3 6/10 major.
Novelty trajectory (blind): 15 → 11 → 12. Author's target > 23/25 not reached.

## MAJOR, all addressed in text/analysis
| id | concern | action |
|---|---|---|
| R2-1 | Duchi et al. 2024 (arXiv 2403.16336) multi-environment conformal anticipates LotCP-A and the season-level step | verified, cited, contribution restated as application + few-shot replay parts; "third level" novelty claim withdrawn |
| R1-1, R2-2 | Prop. 3 coverage claim unproven | corrected to union bound 1−α−k/(S+1); conditional claim withdrawn; predictor asymmetry listed |
| R1-2, R3-2 | bound quoted for R, headline R2 | R2 bound (S−1)/(S+1) stated in 2.7 and limitations |
| R1-3 | R2 promoted after R failed width rule, undisclosed | disclosed in 4.5, Table 5 caption, limitations |
| R1-4 | fixed-α comparison not width-matched | fine α grid (0.06–0.09) run: R2 ≈ fixed α 0.08 in width and worst-season coverage → efficiency claim retracted; benefit = data-driven level choice |
| R1-5, R3-1 | season counts knife-edge, inconsistent across tables | five draw seeds: R2 5/5 in all 20 model×seed runs (min 0.901); LotCP-S 1–3/5; abstract uses range; Table 5 caption notes shared draws |
| R1-6, R3-7, R2-6 | decision comparator weak | abstract/conclusion: point rule weak comparator; no detectable saving from reference fruit |
| R3-3 | stale highlights docx | regenerated with package |
| R3-6, R2-5 | leverage PLS not reported | reported in 4.3 (Faber & Kowalski cited) |
| R3-4/5 | code on request; placeholders; CRediT | author decisions (code on request by author instruction; affiliations to be supplied by author) |
| R2-3 | Wadoux 2025 described generically; reviewer says it used the same mango data | NOT changed: content could not be verified (no abstract available via Crossref/Semantic Scholar; publisher blocked) |
## MINOR: Table 6→7 ref, 0.08–0.11 range (now 3 decimals), P4 relabel stated as post hoc, AR m=5 width stated, multipliers grow with seasons discussed.

## Decision
The novelty bottleneck is structural: the methodological ideas tried are anticipated by GHCP (2026) and Duchi et al. (2024),
and breadth/evidence are capped by one fruit data set with five target seasons. Three pivots (MAX_PIVOTS) used. Honest exit
from the novelty loop recommended; paper positioned as an applied audit with an honest method evaluation.
