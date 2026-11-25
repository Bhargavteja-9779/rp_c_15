<!-- Reviewer 3 (clarity/reproducibility/declarations), fresh-context agent, round 3, 2026-11-25 -->

**Reviewer 3 (clarity, reproducibility, journal fit, declarations)**

**(1) Score: 6/10. Recommendation: major revision.** The audit itself is careful and is reported honestly. Most numbers trace back to result files. But the headline season-level results are not consistent across tables, the season-level guarantee is overstated for the recommended variant, and the submitted front matter and highlights files are stale or incomplete. Main text is about 8,300 words (Sections 1–7, without tables or captions), plus 7 tables, 6 figures and a 1,000-word appendix. The abstract is about 245 words, at the limit. The manuscript is too dense for an agricultural-engineering readership.

**(2) Concerns**

1. **MAJOR – the LotCP-S season count differs between Table 3 and Table 5.** In Table 3 (SNV PLS, m=10), LotCP-S reaches 0.90 in 3/5 seasons. Section 4.3 gives the season values 0.957/0.882/0.902/0.897/0.914. In Table 5, Section 4.5 and the abstract ("two of five") it reaches 2/5. `results/cycle4/robust_lots.csv` gives 2019 = 0.898, so a different set of reference draws moves 2019 from just above 0.90 to just below. Two problems follow. A reader sees contradictory counts. And the "seasons ≥ 0.90" metric flips on draws near the threshold. That weakens the "5/5 for LotCP-R2" claim, whose lowest season is 0.904. *Fix:* use one set of draws for every table. Report the season coverages behind every count, with Monte-Carlo spread across draws. Soften the "every season" wording.

2. **MAJOR – the season-level guarantee is overstated for the recommended variant.** Section 2.7, the Discussion ("at least 2/3 … 6/7") and Limitation 3 ("0.67–0.86") give the bound for LotCP-R (k=1). The practical procedure, Table 5 and highlight 4 promote LotCP-R2 (k=2). For R2, (S+1−k)/(S+1) is 1/3 with two past seasons and 5/7 with six. *Fix:* state the R2 bound in Sections 2.7 and 5 and in Limitation 3. Make clear in the abstract and highlights that the strong 5/5 result is empirical and exploratory, not guaranteed.

3. **MAJOR – the highlights in the submission package do not match the manuscript.** `manuscript/highlights.docx` (and `03_Highlights.docx`) list five different highlights, for example "lot-level assurance … only 2 of 5 seasons". They make no mention of season-robust replay. The manuscript highlights also drop the "post hoc/exploratory" labels that the docx version carries. Highlight 4 ("met 90 % … every season at half the extra width") is exploratory and holds only for R2, not R. *Fix:* regenerate one set of highlights and label the exploratory ones.

4. **MAJOR – code availability conflicts with the reproducibility claims.** Data availability says the code, results and protocol history are available "on request". Yet Section 3.8 and the README rely on the git history to verify pre-specification, the README describes a full MIT-licensed repository, and the AI statement relies on the scripted number audit. Under "on request", neither reproducibility nor the timing of pre-specification can be checked. *Fix:* deposit the code, stored predictions, `experiments/PROTOCOL.md`, the `plan_v*.yaml` files and the git history in an archive with a DOI (e.g. Zenodo), and cite it. Do the same for the confirmation plan in Section 3.6.

5. **MAJOR – front matter and declarations are incomplete.** The title page and manuscript still contain placeholders ("[Department, Institution…]", "[e-mail address]"). The title-page acknowledgements leave out NeoSpectra, which the manuscript includes. In CRediT, the corresponding author is credited only with Supervision. Elsevier expects each author's role to be justified, and the corresponding author usually reviews and edits the text. *Fix:* complete the affiliations and contacts, align the acknowledgements, and review CRediT (e.g. add Writing – review & editing and Project administration if true).

6. **MAJOR – an analysis declared in the AI statement is not reported.** Section 3.8 and Supplementary Note S8 list "leverage-based PLS intervals" among the analyses added after the simulated review and say they are "marked as such". They appear nowhere in the results or supplement. *Fix:* report them (e.g. one row in a supplementary table) or remove the claim.

7. **MAJOR (decision framing) – the comparator for the cost saving is weak, and the headline omits this.** The abstract and highlight 5 present the lower bound as lowering cost relative to point predictions. Section 4.8 admits that the point rule costs more than withholding every fruit (8.69 vs 6.44). The split-CP bound also delays 69 % of ready lots. *Fix:* in the abstract, compare against "withhold all" as well. Say plainly that the reference fruit gave no detectable saving and that delays roughly tripled. Label the sentence "exploratory".

8. **MINOR – wrong table cross-reference in Section 4.8.** "whereas Table 6 pools over lots" should read Table 7.

9. **MINOR – repository paths in the paper.** The Table 5 caption and Section 4.5 cite "results/cycle4" for the m=5 results. *Fix:* move these to a numbered supplementary table.

10. **MINOR – "What the replay buys" (Section 4.3) mixes statistics.** The sentence quotes pooled coverage (0.899/0.908), then gives differences of 3.7/2.4/1.4 points that are season means; the pooled differences are 2.1/1.1. In addition, m=3 is not shown in Table 3. *Fix:* use one statistic throughout and add the m=3 row.

11. **MINOR – the abstract range does not match Table 4.** The abstract and Section 4.3 say "0.08–0.10"; Table 4 gives +0.081 to +0.105. Write 0.08–0.11.

12. **MINOR – endpoint terminology in Table 6 vs Section 4.7.** Table 6 says "share of lots ≥ 0.90"; the text says "lot-draws". Use one term and define it.

13. **MINOR – the season-merge rule may be dead code.** Section 3.4 merges seasons with fewer than five lots, but every season in Table 1 has at least 11 lots. State whether the rule ever applied.

14. **MINOR – soil development analyses are hard to follow.** Sections 2.2 and 3.6 refer to soil "development analyses" (OSSL/KSSL/LUCAS) that are described only in Supplementary Note S5.3. *Fix:* add one sentence in Section 3 describing them.

15. **MINOR – README gaps.**
    - The README's "Reproducing … without retraining" section mentions only the cycle 2–3 add-on scripts. It does not say that the cycle-4 scripts (`season_robust`, `seq_*`, `shift_indicators`), which produce Table 5 and Section 4.6, must also be run.
    - The layout section lists `plan_v2–v4.yaml`, but v5–v7 exist.
    - The README references `review/`, `state/` and `journal/` (autonomous-loop artefacts). Say whether these are part of the public deposit.
    - Give total compute time for the full pipeline.

16. **MINOR – readability for agricultural engineers.**
    - Terms such as exchangeability, order statistic, lot-macro, "replay/episode" and PAC appear before the glossary in Section 3.5. Move the glossary into Section 2, or add a plain-language box.
    - Section 1.1 (about 700 words, many 2025–2026 preprints) could be halved.
    - Six interval-method families plus variants R/R2/AR/A/S/(b)/(b′) are hard to track. Add a method-summary table (name, uses m, guarantee level, pre-specified or exploratory).
    - Consider trimming the main text to about 7,000 words.

17. **MINOR – data availability.** Add licences for NeoSpectra and OSSL, and the date the data were accessed. The Mendeley file name ("v4" inside version 6) and its checksum should appear in the paper, not only in the README.

18. **MINOR – AI-use declaration.** The declaration and Section 3.8 are consistent and appropriately detailed. Add the model version, and state that the "simulated peer review" was not external peer review. The cover letter should say the same.
