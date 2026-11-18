---
title: "Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons"
---

**P N Bhargav Teja^a^, Ragavan K^a,\*^**

^a^ [Department, Institution, City, Postal code, Country]

\* Corresponding author: Ragavan K, [e-mail address], [postal address]

# Abstract

A handheld near-infrared (NIR) reading of mango dry matter content (DMC) supports a harvest decision only if its error is known for the lot being picked, yet calibrations are built on past seasons and their error bars come from those seasons. On a public mango data set ({{V:n_lots}} harvest lots, seven seasons) we predicted each season from the seasons before it. At a nominal 90 %, standard error bars, including conformal, quantile-model, deep-ensemble and Monte-Carlo-dropout intervals, covered {{f"{100*min(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}}–{{f"{100*max(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}} % of the reference values on {{V:n_target_lots}} later-season lots. We propose a risk-aware workflow: a few fruit per lot are tested destructively, a few-shot conformal calibration (LotCP) corrects the lot bias and scale and gives every scanned fruit a lower bound with proven coverage, and a fruit or lot is harvested when the bound meets the specification at a confidence level set by the cost ratio of the two possible errors. With 3–30 reference fruit, coverage was {{f"{100*min(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}}–{{f"{100*max(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}} %, and a lot-level variant kept {{r.meet('lotcp_a',10)}} % of lots at the stated coverage. In a retrospective harvest simulation at 15 % DMC, immature fruit among those accepted fell from {{r.hvp('point',0,None)}} % with point predictions to {{r.hvp('lotcp_s_lower',10,0.1)}} % with ten reference fruit, and premature lot harvests roughly halved at an unchanged delay rate. Under assumed cost ratios, expected cost fell by {{f"{100*min(r.econ_saving(a)[1] for a in (0.05,0.1,0.2,1/3)):.0f}"}}–{{f"{100*max(r.econ_saving(a)[1] for a in (0.05,0.1,0.2,1/3)):.0f}"}} % relative to point decisions. A planner forecasts from past lots the error-bar width for each number of reference fruit (median error {{f"{100*r.plan.rel_error.abs().median():.0f}"}} %). The findings replicated on two soil spectral libraries.

**Keywords:** near-infrared spectroscopy; harvest decision; fruit maturity; dry matter; conformal prediction; uncertainty quantification; decision support

# Highlights

- Standard NIR error bars for mango dry matter under-cover on later harvest seasons.
- A few reference fruit per lot restore calibrated, lot-level error bars.
- Calibrated lower bounds cut immature fruit among those harvested from {{r.hvp('point',0,None)}} % to {{r.hvp('lotcp_s_lower',10,0.1)}} %.
- A planner forecasts error-bar width for each number of reference fruit.
- A cost-based confidence level turns the error bar into a harvest decision.
