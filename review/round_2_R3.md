<!-- Reviewer 3 (clarity/reproducibility/declarations), fresh-context agent, round 2, 2026-11-25 -->

**Reviewer 3: clarity, reproducibility, journal fit and declarations**

**(1) Score: 6/10. Recommendation: major revision (mostly presentation and declarations; the analysis itself is careful and candid).**

Main text, Introduction to Conclusion: about 6,200 words of prose, about 9,000 with Tables 2–6. Abstract: 221 words. Highlights: all 85 characters or fewer. The length is acceptable. Section 4.3 and Tables 3, 4 and 6 are dense and use a lot of statistical shorthand ("lot-draws", "replay", "season-cluster", "assurance") for an agricultural-engineering reader. Table 3 (24 rows) and Table 4 (28 rows) could be halved by moving the m = 5 rows or the published-PLS rows to the supplement.

**(2) Concerns**

1. **MAJOR. Exploratory labelling is incomplete.** Section 3.8 says the lot scale (designed on 2018), LotCP-A, the planner, the decision simulation, the published-PLS analysis and the matched no-replay baselines are all exploratory. Only the harvest simulation is labelled as such in the Abstract, Highlights (only "assumed-cost") and Conclusion. Highlight 3, the Abstract sentence "The same correction without the replay covered 1–4 points less", Highlight 5 and the Conclusion's "replays the procedure ... kept it at small numbers" all present post hoc results as findings. Fix: add "exploratory"/"post hoc" to these claims. State in the Abstract that the one confirmatory efficiency endpoint (P1/P2 on NeoSpectra) failed.

2. **MAJOR. Code and protocol availability statements are inconsistent.**
   - The Data availability section says the code, derived results and protocol history are "available on request".
   - Appendix B says the pre-specified protocol "accompanies this article".
   - Section 3.6 and Table 5 cite a repository path (experiments/plan_v2.yaml) the reader cannot open.
   - The README describes a public MIT-licensed repository with stored predictions (58 MB).

   Fix: deposit the repository (code, results/predictions, plan_v*.yaml, PROTOCOL.md and its git history) in an archive with a DOI, e.g. Zenodo, and cite it in Data/Code availability and in Section 3.8. "On request" undercuts both the pre-specification claim and the "every number filled in by script" claim.

3. **MAJOR. "Pre-registered" is misleading.** The Table 5 caption says "Pre-registered confirmation", but Section 3.8 and Limitation 4 say the protocol was not publicly registered. Fix: use "pre-specified (internally committed)" throughout.

4. **MAJOR. "In response to review" and "internal review" are unexplained.** Section 3.4 says baselines (b)/(b′) were added "in response to review", and Supplementary Note S8 refers to "internal review". On a first submission, readers will assume external peer review. Section 3.8 says the AI acted as simulated reviewers. Fix: say "in response to an internal (AI-simulated) review", and make the AI declaration list this explicitly with the analyses it triggered.

5. **MAJOR. The README overstates the shortcut.** "Reproducing the manuscript numbers without retraining" claims that `run_all.py --from eval` recomputes "every ... statistic, table, figure and the manuscript". It does not run the cycle 2–3 scripts behind Table 4, Table 5, Table 6 with CIs, the published-PLS rows of Table 3 or Section 4.7. In addition, run_all.py reads orchestration state (state/agent_state.json, queue.json, a compute-budget ceiling) and can silently skip stages ("skipped_budget", "failed_permanent"). Fix: make one documented command run the full chain (including the cycle 2–3 scripts and audit_numbers), remove the agent-state and budget logic from the public entry point (or document it), and give expected runtimes. Also reconcile the data file name `MangoDMC_NIR_Data_v4.csv` with "version 6".

6. **MINOR. Broken cross-references.**
   - Table 4 caption: "Section 6.4" (no such section; probably 3.8).
   - Table 5 caption: "Section 6.3" (should be Section 4.4).
   - Supplementary S2: "Fig. 4 expresses the trade-off" (it is Fig. 3).
   - Supplementary S5.3: OSSL subsets "(Section 3)", which the main Section 3 does not describe.
   - Supplementary S8 refers to itself ("Supplementary Note S8 summarises these failures").
   - Supplementary S7: "RQ3", which is never defined.

7. **MINOR. Text errors in Results.**
   - Section 4.3: "raised coverage ... by 0.10–0.10 ... for both PLS recipes". Table 4 gives +0.081 to +0.105, so it should read 0.08–0.11.
   - Section 4.6: "3.69 [2.11, 5.16], The difference" is a broken sentence missing the other bounds.
   - Section 4.3: "Excluding 2018 ... gives 0.934" does not say which metric or m.
   - Mixed styles: "2 of five", and "87.5 %" next to integer percentages.

8. **MINOR. The main text and supplement disagree on whether reference fruit pay off.** The main text and Highlight 4 say reference fruit gave no further saving. Supplementary S7.2 says reference fruit "roughly halve the rate of premature harvest" and S7.3 says they "add a further, smaller saving". These come from different operating points (α = 1/3, the α\* sweep) than the fixed one. Fix: label the S7 operating points as post hoc and align the wording with Section 4.6.

9. **MINOR. Highlight 1 overstates.** "Under-covered ... in every season" holds for SNV-PLS sample-fold CP. With the published PLS (Table 3), sample-fold CP reached 0.90 in 1/5 seasons. Fix: qualify with "sample-fold split CP" or "in at least four of five seasons".

10. **MINOR. Supplement numbering is confusing.** Notes appear in the order S5–S8 then S1–S4. Tables use two schemes ("Table S-1…S-5" and "supplementary table S1–S24", e.g. "S6b"). Fix: one ordered numbering, and cite every supplementary table in the order it appears.

11. **MINOR. Title page and CRediT.**
    - The affiliation, e-mail and postal address are placeholders.
    - The corresponding author is credited only with Supervision. Confirm this is accurate, and consider adding "Writing – review & editing" if applicable.
    - The AI-use declaration ("design and run experiments") and Section 3.8 ("proposed and ran experiments") should use identical wording.
    - State explicitly who verified the AI-generated code and analyses.
    - The Funding and Competing-interest statements are complete and consistent.

12. **MINOR. Contribution 4: "operating point fixed in advance".** The operating point was fixed before the CIs were computed, but the decision analysis itself was post hoc (Section 3.8). Reword to avoid implying it was pre-specified.

13. **MINOR. Discussion: "by 6 to 13 coverage points".** This range does not match Table 3 (sample-fold CP falls 7.7 points pooled and 11.9 without 2017; the other methods fall 6–13). Name the methods and aggregation the range refers to.

14. **MINOR. Jargon.** Define "lot-draw", "replay", "episode", "interval score" and "season-cluster bootstrap" in one plain-language box or glossary early in Section 3.5. Add a one-sentence practical reading of Table 3 for growers, e.g. "with 10 cut fruit, the error bar is about ±1.7 % DMC and holds in roughly 9 of 10 fruit".
