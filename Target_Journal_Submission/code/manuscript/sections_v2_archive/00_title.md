---
title: "Risk-aware mango harvest decisions using few-shot conformal calibration of near-infrared spectroscopy across harvest seasons"
---

**P N Bhargav Teja^a^, Ragavan K^a,\*^**

^a^ [Department, Institution, City, Postal code, Country]

\* Corresponding author: Ragavan K, [e-mail address], [postal address]

# Abstract

A handheld near-infrared (NIR) reading of mango dry matter content (DMC) supports a harvest decision only if its error is known for the lot being picked, yet calibration error bars come from past seasons. Predicting each season of a public mango data set ({{V:n_lots}} harvest lots, seven seasons) from earlier seasons, standard error bars at a nominal 90 % (conformal, quantile-model, deep-ensemble, Monte-Carlo-dropout) covered {{f"{100*min(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}}–{{f"{100*max(r.m(k,0) for k in ('scp_sample','gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}} % of the reference values on {{V:n_target_lots}} later-season lots. We propose a risk-aware workflow: a few fruit per lot are tested destructively, a few-shot conformal calibration (LotCP) corrects the lot bias and scale and gives every fruit a lower bound with a coverage guarantee, and fruit are harvested when the bound meets the specification at a level set by the cost ratio of the two errors. With 3–30 reference fruit, coverage was {{f"{100*min(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}}–{{f"{100*max(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}} %, and a lot-level variant kept {{r.meet('lotcp_a',10)}} % of lots at the stated coverage. In a retrospective harvest simulation at 15 % DMC, immature fruit among those accepted fell from {{r.hvp('point',0,None)}} % with point predictions to {{r.hvp('lotcp_s_lower',10,0.1)}} % with ten reference fruit, and premature lot harvests roughly halved at an unchanged delay rate. Under assumed cost ratios, expected cost fell by {{f"{100*min(r.econ_saving(a)[1] for a in (0.05,0.1,0.2,1/3)):.0f}"}}–{{f"{100*max(r.econ_saving(a)[1] for a in (0.05,0.1,0.2,1/3)):.0f}"}} % relative to point decisions. A planner forecasts the error-bar width for each number of reference fruit (median error {{f"{100*r.plan.rel_error.abs().median():.0f}"}} %). In a pre-registered confirmation on an untouched handheld-NIR soil library, the lot-level guarantee held ({{f"{100*r.csum('Neo','lotcp_a',10,'meets'):.0f}"}} vs {{f"{100*r.csum('Neo','target_only_centred',10,'meets'):.0f}"}} % of lots); an efficiency gain over simple bias correction did not.

**Keywords:** near-infrared spectroscopy; harvest decision; fruit maturity; dry matter; conformal prediction; uncertainty quantification; decision support

# Highlights

- Standard NIR error bars for mango dry matter under-cover on later harvest seasons.
- A few reference fruit per lot restore calibrated, lot-level error bars.
- Calibrated lower bounds cut immature fruit among those harvested from {{r.hvp('point',0,None)}} % to {{r.hvp('lotcp_s_lower',10,0.1)}} %.
- Pre-registered test on untouched data confirmed the lot-level guarantee.
- A cost-based confidence level turns the error bar into a harvest decision.
