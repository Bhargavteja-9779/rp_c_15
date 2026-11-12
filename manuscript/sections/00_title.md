---
title: "How many reference fruit does a valid error bar need? Lot-exchangeable few-shot conformal calibration of near-infrared dry-matter predictions across harvest seasons"
---

**[Author One]^a,\*^, [Author Two]^a^, [Author Three]^b^**

^a^ [Department, Institution, City, Country]

^b^ [Department, Institution, City, Country]

\* Corresponding author: [name], [e-mail address], [postal address]

# Abstract

Handheld near-infrared (NIR) spectrometers guide fruit harvest decisions, yet their calibrations are built on past seasons and report no error bar that holds on a new one. Using a public mango data set ({{V:n_spectra}} spectra, {{V:n_lots}} harvest lots, seven seasons), we train on earlier seasons and measure interval coverage for dry matter content on {{V:n_target_lots}} later-season lots. At a nominal 90 %, split conformal prediction covers {{f"{100*r.m('scp_sample',0):.0f}"}} % and leaves {{r.u('scp_sample',0)}} % of lots below 80 %; Gaussian bands, quantile forests, conformalised quantile regression, deep ensembles and Monte-Carlo dropout cover {{f"{100*min(r.m(k,0) for k in ('gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}}–{{f"{100*max(r.m(k,0) for k in ('gauss','qrf','cqr_sample','ensemble','mc_dropout')):.0f}"}} %. Holding calibration residuals out by season restores pooled coverage but widens intervals by {{r.pct(r.m('scp_season',0,'width'), r.m('scp_sample',0,'width'))}} % and still varies between {{f"{100*r.season_cov('scp_season',0).min():.0f}"}} % and {{f"{100*r.season_cov('scp_season',0).max():.0f}"}} % by season. We propose LotCP, a lot-exchangeable few-shot conformal calibration that corrects a new lot's bias from *m* destructively measured reference samples, rescales the score by a lot-specific scale that also uses repeated scans, and calibrates the half-width by replaying this procedure on past lots. With 3 to 30 reference samples per lot the scale-adaptive variant covers {{f"{100*min(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}}–{{f"{100*max(r.m('lotcp_s',m) for m in (3,5,10,20,30)):.0f}"}} %, stays within {{f"{100*min(r.gen(a,b,'lotcp_s',10) for a,b in [('pls','forward'),('gbm','forward'),('cnn','forward'),('pls','loso'),('cnn','loso')]):.0f}"}}–{{f"{100*max(r.gen(a,b,'lotcp_s',10) for a,b in [('pls','forward'),('gbm','forward'),('cnn','forward'),('pls','loso'),('cnn','loso')]):.0f}"}} % across three predictors and two protocols, and has the best interval score for 3 to 20 samples; at 10 samples its intervals are {{r.pct(r.m('lotcp_s',10,'width'), r.m('biascorr_naive',10,'width'))}} % narrower than bias correction with a source quantile and {{r.pct(r.m('lotcp_s',10,'width'), r.m('target_only_centred',10,'width'))}} % narrower than target-only calibration. Beyond 20 samples target-only calibration is equally good. The gain comes from the lot-specific scale, at few samples mainly from its repeated-scan term; shrinkage of the bias estimate adds nothing.

**Keywords:** near-infrared spectroscopy; conformal prediction; uncertainty quantification; distribution shift; fruit maturity; calibration maintenance; mango

# Highlights

- Conformal intervals for mango dry matter cover {{f"{100*r.m('scp_sample',0):.0f}"}} %, not 90 %, on later seasons.
- Deep ensembles, MC dropout and quantile models under-cover as well.
- Season-held-out calibration restores coverage only on average and at {{r.pct(r.m('scp_season',0,'width'), r.m('scp_sample',0,'width'))}} % more width.
- Three to ten reference fruit per lot give near-nominal, narrower intervals.
- A lot-specific scale from repeated scans, not shrinkage, drives the gain.
