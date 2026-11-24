# Review round 1 — merged triage (cycle 2 → cycle 3), 2026-11-24
Scores: R1 (methods/statistics) 4/10 major; R2 (novelty) 6/10 major, blind novelty 15/25; R3 (clarity/reproducibility) 5/10 major.
Verdict: not clean. G10 fail. Triage types: W = writing/claim fix; E = needs evidence (plan_v4); R = rebuttal.

## Verified before triage
R1-C1 recomputed by the agent from results/raw_results.csv (pls, forward, α=0.10, seed 0):
LotCP-S coverage m=10 pooled 0.919, excluding 2017 0.893, season-average 0.911; LotCP-A share of lot-draws meeting 0.90
at m=10: 2017 0.980, 2018 0.862, 2019 0.855, 2020 0.886, 2021 0.927 (target 0.90 missed in 3/5 seasons). CONFIRMED.

## MAJOR
| id | concern | type | action |
|---|---|---|---|
| R1-C1 | pooled headline driven by over-covered 2017 (41 % of lots) | W+E | E1: report season-average and 2017-excluded figures for every headline; abstract/highlights state LotCP-A missed the lot-level target in 3/5 seasons |
| R1-C2 | lot-level tests ignore season effect | E | E1: season-cluster bootstrap CIs; season-level exact sign test and mixed model (season random intercept) for the 4 primary endpoints; lot-level Wilcoxon kept as secondary |
| R1-C3 | confirmation weak: mango arm re-draws, NeoSpectra unshifted, P3/P4 reward width | W+E | W: Table 7 relabelled "re-draw check" for mango; NeoSpectra arm called a no-shift sanity check; P4 marked uninformative. E3: width-vs-assurance frontier (LotCP-S over α grid vs LotCP-A) to show whether LotCP-A buys assurance more cheaply than lowering α |
| R1-C4 | no matched baseline with the replicate scale; Table 9 selective | E+W | E2: new baseline `biascorr_rep` = bias correction + source quantile of replicate-scaled residuals without replay (lotcp_s_noepisodic with rep scale); W: economics table shows all m and all rules incl. withhold-all; "further saving" claims dropped |
| R1-C5, R3-2, R3-4, R3-5 | decision/economics: no CIs, post-hoc operating point, in-sample regret, weak comparator, weaker PLS | E+W | E4: season-cluster bootstrap CIs; pre-stated α=0.10 operating point; α chosen by leave-one-season-out; savings vs best m=0 bound; rerun with published PLS; all labelled exploratory |
| R1-C6, R3-6 | multiplicity; "pre-registered" overstated | W+E | W: "pre-specified (internal git commit)"; exploratory labels; E1 adds LotCP-S results excluding 2018 |
| R2-1 | novelty framed too broadly | W | reframe contributions: (i) lot-by-lot seasonal coverage audit, (ii) m-shot replay calibration with lot-level assurance option and planner; LotCP-S as adaptation |
| R2-2, R2-3, R2-6, R2-7 | missing literature, classical PLS intervals | W+E | cite wadoux2025, bouckaert2011, duma2025, mishra2021transfer, yilmaz2022; E5: sample-specific PLS interval baseline (leverage-based) if feasible within budget, else justified omission |
| R2-4 | breadth: one fruit data set | E | E6: bounded search for a second public fruit NIR set with season/lot structure; if none, restrict claims (title/abstract say mango) |
| R3-1 | length ~20k words | W | cut to ≤10k: merge Secs 2/3, move 11–14 to supplement, failure story stated once |
| R3-3 | decision framing post hoc | W | "exploratory" in abstract, highlights, Secs 8–9 |
| R3-7, R3-8 | data/code statement; AI disclosure | W | list Mendeley, OSSL, NeoSpectra DOIs; code availability statement consistent; Methods subsection on AI involvement and human verification |

## MINOR
R1-C7 published PLS primary → report both predictors in main tables (E4 covers decisions). R1-C8 single-instrument analysis → main text with tests (E1). R1-C9 planner error by number of source seasons (E4). R1-C10 NeoSpectra/KSSL overlap → E7 quantify and rerun excluding overlap. R1 number inconsistencies (5.02 vs 5.01; replay-ablation draws; ledger v015 m value) → fix text, disclose different draws, correct ledger. R2-5 kayaoglu2026 updated; R2-8 α* = newsvendor threshold; R2-9 prototype folded into availability. R3-9 README; R3-10 n and overlap stated; R3-11 LotCP-A default in tool or caveat; R3-12 rank limitations.

## Rebuttals
None of the MAJOR concerns is judged invalid.
