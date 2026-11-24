# G1 verification attempt — cycle 2 (2026-11-24)

Requirement (master prompt §4): submission → final acceptance ≤ 72 days, verified from the official metrics page and/or
Received/Accepted dates of ≥ 10 recent articles, with median and range computed by us and DOIs listed.

| Route | Result |
|---|---|
| Crossref REST API, ISSN 2772-3755, 800 journal articles published 2025-06 to 2026-10 (`evidence/sat_crossref_raw.json`) | 0 of 800 records carry `received`/`accepted` assertions. Not usable. |
| Article page via doi.org → linkinghub → ScienceDirect (web-fetch tool) | HTTP 403 from ScienceDirect. Not usable. |
| Search-engine snippets of article pages | No article-level history dates returned. |
| journalmetrics.org (PubMed-based) | States that received→accepted is "Not available" for this journal (too few PubMed records). |
| ScienceDirect journal page / Insights page, as quoted by search results on 2026-11-10 | Publisher-reported average submission → acceptance 69 days (journal page) and 72 days (Insights page). These pages were not opened directly (403); figures are from search-tool quotations. |

**Status: the per-article verification rule could not be met from this environment (UNVERIFIED).** The only evidence is
the publisher-reported average of 69–72 days, which is at the limit and is an average, not a median of our own
computation. G1 is recorded as "pass with stated failure" as the gate definition allows; the human authors should open
ten recent articles in a browser and record Received/Accepted dates before relying on the 72-day criterion.
JCR quartile/impact factor: from JCR-derived listings, not from Clarivate (UNVERIFIED in JCR itself).
