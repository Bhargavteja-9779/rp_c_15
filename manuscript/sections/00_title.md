---
title: "Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons"
---

**P N Bhargav Teja^a^, Ragavan K^a,\*^**

^a^ [Department, Institution, City, Postal code, Country]

\* Corresponding author: Ragavan K, [e-mail address], [postal address]

# Abstract

A handheld near-infrared (NIR) prediction of mango dry matter content (DMC) supports a harvest decision only if its error is known for the lot being picked, yet error bars are calibrated on past seasons. We predicted each season of a public mango data set ({{V:n_lots}} harvest lots, seven seasons) from earlier seasons. Six standard error bars at a nominal 90 % covered {{f"{100*min(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}}–{{f"{100*max(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}} % of reference values on {{V:n_target_lots}} later-season lots. A few-shot conformal calibration (LotCP-S) tests *m* fruit per lot destructively, corrects the lot bias and scale, and sets the half-width by replaying this procedure on past lots. With five to ten reference fruit it raised coverage over standard split conformal prediction in all five target seasons, to {{f"{r.ss('lotcp_s',10):.3f}"}} pooled, but {{f"{r.ss('lotcp_s',10,'coverage_ex2017'):.3f}"}} without the over-covered first target season. In post hoc comparisons, the same correction without the replay covered (season means) {{f"{100*r.st('lotcp_s','biascorr_full','coverage',10):.0f}"}}–{{f"{100*r.st('lotcp_s','biascorr_full','coverage',3):.0f}"}} points less. A lot-level variant (post hoc) kept {{f"{100*r.ss('lotcp_a',10,'meets_pooled'):.0f}"}} % of lot-draws at 90 % coverage overall but met that target in only {{int(r.ss('lotcp_a',10,'seasons_meeting_assurance'))}} of five seasons. In an exploratory harvest simulation under assumed costs, a calibrated lower bound cost {{f"{r.dd('point',0):.1f}"}} units per 100 fruit less than point decisions; no further saving from reference fruit was detectable. In the pre-specified confirmation on independent handheld-NIR soil data, the efficiency gain over simple bias correction was not confirmed. Conclusions held with the published PLS recipe. Shifts between seasons, not the number of reference fruit, limit what can be guaranteed, and a prospective orchard trial is needed before practical use.

**Keywords:** near-infrared spectroscopy; harvest decision; fruit maturity; dry matter; conformal prediction; uncertainty quantification; calibration maintenance

# Highlights

- Standard NIR error bars under-covered later-season mango lots in most seasons.
- Five to ten reference fruit per lot brought coverage close to, not always at, 90 %.
- Post hoc: replaying the correction on past lots protected coverage at small m.
- Calibrated bounds, not reference fruit, drove the assumed-cost savings.
- Post hoc lot-level assurance was met pooled, but in only 2 of 5 seasons.
