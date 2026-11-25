---
title: "Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons"
---

**P N Bhargav Teja^a^, Ragavan K^a,\*^**

^a^ [Department, Institution, City, Postal code, Country]

\* Corresponding author: Ragavan K, [e-mail address], [postal address]

# Abstract

A handheld near-infrared (NIR) prediction of mango dry matter content (DMC) supports a harvest decision only if its error is known for the lot being picked, yet error bars are calibrated on past seasons. Predicting each season of a public mango data set ({{V:n_lots}} harvest lots, seven seasons) from earlier seasons, six standard error bars at a nominal 90 % covered {{f"{100*min(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}}–{{f"{100*max(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}} % of reference values on {{V:n_target_lots}} later-season lots. A few-shot conformal calibration that tests five to ten fruit per lot and corrects the lot bias and scale raised coverage in every season but reached 90 % in only two of five, because seasons differ by more than past lots suggest. We therefore calibrate within each past season, treating seasons as exchangeable units, and take an upper order statistic across seasons; this gives a season-level guarantee whose strength grows with the number of past seasons. In exploratory analyses this season-robust replay reached 90 % coverage in all five seasons for four predictors at {{f"{100*r.rbr('R2',10,'width_inc',min):.0f}"}}–{{f"{100*r.rbr('R2',10,'width_inc',max):.0f}"}} % more width, against {{f"{100*r.rbr('S05',10,'width_inc',min):.0f}"}}–{{f"{100*r.rbr('S05',10,'width_inc',max):.0f}"}} % for a fixed higher confidence level, and its lot-level form met a nine-lots-in-ten target in {{r.rbr('AR',10,'seasons_meets',min)}}–{{r.rbr('AR',10,'seasons_meets',max)}} of five seasons, against {{r.rbr('A',10,'seasons_meets',min)}}–{{r.rbr('A',10,'seasons_meets',max)}}. Learning the shift from earlier lots of the same season and spectral warning signs did not help. Under assumed costs, deciding on a calibrated lower bound rather than the point value lowered the cost of harvest decisions. A prospective orchard trial remains necessary.

**Keywords:** near-infrared spectroscopy; harvest decision; fruit maturity; dry matter; conformal prediction; uncertainty quantification; calibration maintenance

# Highlights

- NIR error bars calibrated on past seasons under-covered later-season mango lots.
- A few reference fruit per lot restored coverage on average but not every season.
- Calibrating within each past season gives a season-level coverage guarantee.
- Season-robust calibration met 90 % coverage every season at half the extra width.
- Calibrated lower bounds, not point predictions, lowered assumed harvest costs.
