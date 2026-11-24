# Published results used for baseline reproduction (G4) — verified from abstracts opened via the Semantic Scholar API on 2026-11-24

| Paper | DOI | Protocol (as stated) | Reported result |
|---|---|---|---|
| Anderson, Walsh, Subedi, Hayes 2020, Postharvest Biol. Technol. 168:111202 | 10.1016/j.postharvbio.2020.111202 | 4675 samples, 4 seasons, 10 cultivars, 2 regions; harvest populations as CV groups; 4th season = independent test; mean-centred SG 2nd derivative (2nd-order, 17 points), 684–990 nm | Global PLSR RMSEP 1.01 %; specific PLSR 0.88 %; global ANN 0.89 % |
| Anderson, Walsh, Flynn, Walsh 2021, Postharvest Biol. Technol. 171:111358 | 10.1016/j.postharvbio.2020.111358 | trained on 3 seasons (n = 10,243), tested on a 4th season (n = 1,448) | Global PLS RMSEP 1.014 %, SEP 1.012 %; LOVR 0.881 %; ensemble 0.839 % |
| Walsh, Neupane, Li 2024, Spectrochim. Acta A 311:124003 | 10.1016/j.saa.2024.124003 | same training and independent test set as above; also a new season | CNN RMSEP 0.77 % (benchmark); on a new season RMSEP CNN 1.18, ANN 2.62, PLS 1.87; bias 0.16, 2.36, 1.56 %FW; SD of RMSEP over 50 seeds 0.02 (CNN), 0.03 (ANN) |

The data provider's file MangoDMC_NIR_Data_v3.csv (same Mendeley record) labels these sets: Cal 7,413 + Tuning 2,830 = 10,243 training spectra; "Val Ext" 1,448 (season 4, the independent test set); "Val Ext 2" 320 (an additional season, which we take to be the "new season" of Walsh et al. 2024 — an assumption, see decisions.md).
Full texts were not accessible (ScienceDirect 403); only the abstract statements above are used.
