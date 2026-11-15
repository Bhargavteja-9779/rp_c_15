---
title: "How many reference fruit does a valid error bar need? Lot-exchangeable few-shot conformal calibration of near-infrared dry-matter predictions across harvest seasons"
---

**[Author One]^a,\*^, [Author Two]^a^, [Author Three]^b^**

^a^ [Department, Institution, City, Country]

^b^ [Department, Institution, City, Country]

\* Corresponding author: [name], [e-mail address], [postal address]

# Abstract

Handheld near-infrared (NIR) spectrometers guide fruit harvest decisions, yet their calibrations are built on past seasons and carry no error bar that holds on a new one. On a public mango data set ({{V:n_spectra}} spectra, {{V:n_lots}} harvest lots, seven seasons) we train on earlier seasons and measure interval coverage for dry matter content on {{V:n_target_lots}} later-season lots. At a nominal 90 %, split conformal prediction covers {{f"{100*r.m('scp_sample',0):.0f}"}} % and leaves {{r.u('scp_sample',0)}} % of lots below 80 %; Gaussian bands, quantile models, deep ensembles and Monte-Carlo dropout cover {{f"{100*min(r.m(k,0) for k in ('gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}}–{{f"{100*max(r.m(k,0) for k in ('gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}} %. Season-held-out calibration restores average coverage only with {{r.pct(r.m('scp_season',0,'width'), r.m('scp_sample',0,'width'))}} % wider intervals. We propose LotCP-S, a lot-exchangeable few-shot conformal calibration: the bias of a new lot is corrected from *m* destructively measured reference samples, the score is rescaled by a lot-specific scale that also uses repeated scans, and the half-width is calibrated by replaying this procedure on past lots. With 3–30 reference samples it covers {{f"{100*min(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}}–{{f"{100*max(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}} % ({{f"{100*min(r.gen(a,b,'lotcp_s',10) for a,b in [('pls','forward'),('gbm','forward'),('cnn','forward'),('pls','loso'),('cnn','loso')]):.0f}"}}–{{f"{100*max(r.gen(a,b,'lotcp_s',10) for a,b in [('pls','forward'),('gbm','forward'),('cnn','forward'),('pls','loso'),('cnn','loso')]):.0f}"}} % across three predictors and two protocols) and has the best interval score for 3–20 samples; beyond 20, calibration on the reference samples alone is as good. Used as a lower bound against a 15 % specification, it cuts non-compliant fruit among those accepted from {{r.decp('point',0,15,'false_accept_share')}} % to {{r.decp('lotcp_s_lower',10,15,'false_accept_share')}} %. On two soil vis–NIR libraries the loss is larger (coverage {{f"{100*r.soil('lucas_ph','scp_sample',0):.0f}"}}–{{f"{100*r.soil('kssl_oc','scp_sample',0):.0f}"}} %), and five local samples restore {{f"{100*min(r.soil(t,'lotcp_s',5) for t in ('lucas_oc','lucas_ph','kssl_oc')):.0f}"}}–{{f"{100*max(r.soil(t,'lotcp_s',5) for t in ('lucas_oc','lucas_ph','kssl_oc')):.0f}"}} %. A pre-specified shrinkage of the bias estimate failed under a survey-campaign shift and was dropped.

**Keywords:** near-infrared spectroscopy; conformal prediction; uncertainty quantification; distribution shift; fruit maturity; soil spectral library; calibration maintenance

# Highlights

- Conformal intervals for mango dry matter cover {{f"{100*r.m('scp_sample',0):.0f}"}} %, not 90 %, on later seasons.
- On soil spectra across survey campaigns coverage falls to {{f"{100*r.soil('lucas_ph','scp_sample',0):.0f}"}}–{{f"{100*r.soil('lucas_oc','scp_sample',0):.0f}"}} %.
- Three to ten reference samples per lot restore near-nominal coverage.
- A lot-specific scale gives narrower valid intervals; shrinkage is unsafe.
- Calibrated lower bounds cut immature fruit among those accepted from {{r.decp('point',0,15,'false_accept_share')}} % to {{r.decp('lotcp_s_lower',10,15,'false_accept_share')}} %.
