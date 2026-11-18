| Predictor, protocol | Method | Lots | Coverage | Under-covered lots (%) | Width | Interval score |
|---|---:|---:|---:|---:|---:|---:|
| PLS, forward | Split CP (sample folds) (m=0) | 137 | 0.823 | 28 | 3.83 | 6.81 |
| PLS, forward | Split CP (season folds) (m=0) | 137 | 0.900 | 14 | 5.26 | 7.05 |
| PLS, forward | Bias corr. + source CP (m=10) | 137 | 0.938 | 5 | 3.83 | 4.68 |
| PLS, forward | Target-only CP, centred (m=10) | 137 | 0.956 | 3 | 4.63 | 5.12 |
| PLS, forward | LotCP (m=10) | 137 | 0.927 | 10 | 3.97 | 5.01 |
| PLS, forward | LotCP-S (m=10) | 137 | 0.919 | 8 | 3.45 | 4.46 |
| LightGBM, forward | Split CP (sample folds) (m=0) | 137 | 0.759 | 51 | 3.09 | 7.12 |
| LightGBM, forward | Split CP (season folds) (m=0) | 137 | 0.902 | 18 | 4.98 | 6.69 |
| LightGBM, forward | Bias corr. + source CP (m=10) | 137 | 0.882 | 19 | 3.09 | 4.60 |
| LightGBM, forward | Target-only CP, centred (m=10) | 137 | 0.957 | 3 | 4.62 | 5.03 |
| LightGBM, forward | LotCP (m=10) | 137 | 0.915 | 11 | 3.60 | 4.74 |
| LightGBM, forward | LotCP-S (m=10) | 137 | 0.914 | 8 | 3.43 | 4.41 |
| 1D-CNN, forward | Split CP (sample folds) (m=0) | 137 | 0.789 | 42 | 3.07 | 6.00 |
| 1D-CNN, forward | Split CP (season folds) (m=0) | 137 | 0.928 | 11 | 5.02 | 6.05 |
| 1D-CNN, forward | Bias corr. + source CP (m=10) | 137 | 0.909 | 12 | 3.07 | 4.03 |
| 1D-CNN, forward | Target-only CP, centred (m=10) | 137 | 0.959 | 3 | 4.11 | 4.46 |
| 1D-CNN, forward | LotCP (m=10) | 137 | 0.929 | 14 | 3.95 | 4.77 |
| 1D-CNN, forward | LotCP-S (m=10) | 137 | 0.914 | 7 | 3.06 | 3.87 |
| PLS, leave-one-season-out | Split CP (sample folds) (m=0) | 198 | 0.849 | 23 | 4.07 | 6.57 |
| PLS, leave-one-season-out | Split CP (season folds) (m=0) | 198 | 0.896 | 16 | 4.69 | 6.43 |
| PLS, leave-one-season-out | Bias corr. + source CP (m=10) | 198 | 0.949 | 3 | 4.07 | 4.79 |
| PLS, leave-one-season-out | Target-only CP, centred (m=10) | 198 | 0.957 | 3 | 4.63 | 5.11 |
| PLS, leave-one-season-out | LotCP (m=10) | 198 | 0.908 | 12 | 3.37 | 4.58 |
| PLS, leave-one-season-out | LotCP-S (m=10) | 198 | 0.907 | 8 | 3.26 | 4.36 |
| 1D-CNN, leave-one-season-out | Split CP (season folds) (m=0) | 198 | 0.923 | 11 | 4.34 | 5.39 |
| 1D-CNN, leave-one-season-out | LotCP (m=10) | 198 | 0.914 | 11 | 3.02 | 4.00 |
| 1D-CNN, leave-one-season-out | LotCP-S (m=10) | 198 | 0.908 | 7 | 2.87 | 3.75 |

Table: Table S21. Generalisation across point predictors and protocols (nominal 0.90). LightGBM and CNN under forward chaining: metrics averaged over three seeds within lot.
