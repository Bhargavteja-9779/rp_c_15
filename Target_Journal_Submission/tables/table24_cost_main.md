| Component | Time | Per 1000 scans at deployment |
|---|---:|---:|
| PLS fit (final model) | 1.1 s | 6.6 ms |
| LightGBM fit | 2.0 s | 11.2 ms |
| 1D-CNN fit (20 epochs) | 147.6 s | 58.3 ms |
| PLS: all cross-fits for one target season | 40 s | – |
| 1D-CNN: all cross-fits for one target season | 1395 s | – |
| LotCP calibration, m = 10 | 0.5 s | < 0.1 ms (one bias, one scale per lot) |
| LotCP-S calibration, m = 10 | 1.8 s | < 0.1 ms (one bias, one scale per lot) |
| LotCP-S calibration, m = 30 | 1.1 s | < 0.1 ms (one bias, one scale per lot) |

Table: Table S24. Computing time on a 4-core CPU without GPU (mean over target seasons; CNN fits used one thread each).
