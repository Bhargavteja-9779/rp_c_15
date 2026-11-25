---
title: "How far do near-infrared error bars hold across harvest seasons? Season-aware conformal calibration for mango harvest decisions"
---

**P N Bhargav Teja^a^, Ragavan K^a,\*^**

^a^ [Department, Institution, City, Postal code, Country]

\* Corresponding author: Ragavan K, [e-mail address], [postal address]

# Abstract

A handheld near-infrared (NIR) prediction of mango dry matter content (DMC) supports a harvest decision only if its error is known for the lot being picked, yet error bars are calibrated on past seasons. Predicting each season of a public mango data set ({{V:n_lots}} harvest lots, seven seasons) from earlier seasons, six standard error bars at a nominal 90 % covered {{f"{100*min(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}}–{{f"{100*max(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}} % of reference values on {{V:n_target_lots}} later-season lots. A few-shot conformal calibration that tests five to ten fruit per lot and corrects the lot bias and scale raised coverage in every season but reached 90 % in only {{r.rd('S')}} to {{r.rd('S',fn=max)}} of five, depending on the fruit drawn, because seasons differ by more than past lots suggest. Calibrating within each past season and across seasons, as in multi-environment conformal prediction, reached 90 % coverage in all five seasons for four predictors and repeated reference draws (exploratory), at {{f"{100*r.rbr('R2',10,'width_inc',min):.0f}"}}–{{f"{100*r.rbr('R2',10,'width_inc',max):.0f}"}} % more width, about the width of a fixed level α = 0.08; its gain is choosing that level from past seasons, with a weak explicit season-level guarantee. Learning the shift from earlier lots of the same season and spectral warning signs did not help. Under assumed costs, a calibrated lower bound was cheaper than the point value, and reference fruit gave no detectable further saving (exploratory). A prospective orchard trial remains necessary.

**Keywords:** near-infrared spectroscopy; harvest decision; fruit maturity; dry matter; conformal prediction; uncertainty quantification; calibration maintenance

# Highlights

- NIR error bars calibrated on past seasons under-covered later-season mango lots.
- A few reference fruit per lot restored coverage on average but not every season.
- Calibrating within and across past seasons met 90 % in every season (exploratory).
- That gain equals choosing a slightly higher fixed level, set from past seasons.
- Spectral warning signs and within-season learning did not predict or fix the shift.
