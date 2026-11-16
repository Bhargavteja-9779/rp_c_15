---
title: "Lot-level valid error bars for near-infrared predictions across harvest seasons: few-shot conformal calibration with a per-lot assurance and a reference-sampling planner"
---

**[Author One]^a,\*^, [Author Two]^a^, [Author Three]^b^**

^a^ [Department, Institution, City, Country]

^b^ [Department, Institution, City, Country]

\* Corresponding author: [name], [e-mail address], [postal address]

# Abstract

Handheld near-infrared (NIR) spectrometers guide fruit harvest decisions, yet their calibrations are built on past seasons and carry no error bar that holds on a new one. On a mango data set ({{V:n_lots}} harvest lots, seven seasons) we train on earlier seasons and measure interval coverage for dry matter content on {{V:n_target_lots}} later-season lots. At a nominal 90 %, split conformal prediction covers {{f"{100*r.m('scp_sample',0):.0f}"}} %; Gaussian bands, quantile models, deep ensembles and Monte-Carlo dropout cover {{f"{100*min(r.m(k,0) for k in ('gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}}–{{f"{100*max(r.m(k,0) for k in ('gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}} %. Season-held-out calibration restores average coverage only with {{r.pct(r.m('scp_season',0,'width'), r.m('scp_sample',0,'width'))}} % wider intervals. We introduce a few-shot conformal calibration with proven guarantees: bias and scale of a new lot are estimated from *m* reference samples and repeated scans, and the half-width is calibrated by replaying this procedure on past lots. With 3–30 reference samples the marginal variant (LotCP-S) covers {{f"{100*min(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}}–{{f"{100*max(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}} % ({{f"{100*min(r.gen(a,b,'lotcp_s',10) for a,b in [('pls','forward'),('gbm','forward'),('cnn','forward'),('pls','loso'),('cnn','loso')]):.0f}"}}–{{f"{100*max(r.gen(a,b,'lotcp_s',10) for a,b in [('pls','forward'),('gbm','forward'),('cnn','forward'),('pls','loso'),('cnn','loso')]):.0f}"}} % across three predictors and two protocols) and has the best interval score for 3–20 samples. A second variant (LotCP-A) targets the stated coverage within the lot for nine lots in ten: {{r.meet('lotcp_a',10)}} % of lots reach it with ten samples, against {{r.meet('lotcp_s',10)}} % for LotCP-S, at {{r.pct(r.m('lotcp_a',10,'width'), r.m('lotcp_s',10,'width'))}} % more width. The replay also forecasts the width for each *m* before the season (median error {{f"{100*r.plan.rel_error.abs().median():.0f}"}} %). As a lower bound against a 15 % specification, the calibration cuts non-compliant fruit among those accepted from {{r.decp('point',0,15,'false_accept_share')}} % to {{r.decp('lotcp_s_lower',10,15,'false_accept_share')}} %. On two soil vis–NIR libraries the loss is larger (coverage {{f"{100*r.soil('lucas_ph','scp_sample',0):.0f}"}}–{{f"{100*r.soil('kssl_oc','scp_sample',0):.0f}"}} %), and five local samples restore {{f"{100*min(r.soil(t,'lotcp_s',5) for t in ('lucas_oc','lucas_ph','kssl_oc')):.0f}"}}–{{f"{100*max(r.soil(t,'lotcp_s',5) for t in ('lucas_oc','lucas_ph','kssl_oc')):.0f}"}} %. 

**Keywords:** near-infrared spectroscopy; conformal prediction; uncertainty quantification; distribution shift; fruit maturity; soil spectral library; calibration maintenance

# Highlights

- Conformal intervals for mango dry matter cover {{f"{100*r.m('scp_sample',0):.0f}"}} %, not 90 %, on later seasons.
- On soil spectra across survey campaigns coverage falls to {{f"{100*r.soil('lucas_ph','scp_sample',0):.0f}"}}–{{f"{100*r.soil('lucas_oc','scp_sample',0):.0f}"}} %.
- Few-shot calibration with proofs restores coverage from three reference samples.
- A lot-level variant keeps nine lots in ten at the stated coverage.
- A planner forecasts interval width for each sampling effort before the season.
