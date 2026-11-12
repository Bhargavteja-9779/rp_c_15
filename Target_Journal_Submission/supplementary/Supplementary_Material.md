---
title: "Supplementary material: How many reference fruit does a valid error bar need? Lot-exchangeable few-shot conformal calibration of near-infrared dry-matter predictions across harvest seasons"
---

All tables in this file are written by `src/statistics/analysis.py` from the raw result files; the same tables are provided as CSV files.


| season | spectra | samples | lots | cultivars | instruments | dm_mean | dm_sd | median_samples_per_lot |
|---|---|---|---|---|---|---|---|---|
| 2015 | 15200 | 1152 | 25 | 4 | 8 | 16.465 | 2.664 | 40.000 |
| 2016 | 15310 | 1697 | 37 | 5 | 17 | 15.209 | 1.907 | 40.000 |
| 2017 | 27312 | 2322 | 56 | 9 | 16 | 15.802 | 2.387 | 40.000 |
| 2018 | 16133 | 2894 | 38 | 8 | 23 | 16.530 | 2.510 | 60.500 |
| 2019 | 5604 | 860 | 14 | 6 | 18 | 15.836 | 2.442 | 40.000 |
| 2020 | 4452 | 1073 | 18 | 8 | 15 | 14.895 | 2.622 | 40.000 |
| 2021 | 1390 | 562 | 11 | 5 | 11 | 14.987 | 2.771 | 40.000 |
| All | 85401 | 10560 | 199 | 10 | 31 | 15.893 | 2.467 | 40.000 |

Table: Table S1. Data set by season.


| target | model | seed | n_spectra | rmse | bias | r2 | sd_lot_bias | rmse_cv_sample | rmse_cv_lot | rmse_cv_season | fit_seconds | predict_ms_per_1000 | n_params | n_components |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2017 | pls | 0 | 27312 | 1.261 | -0.028 | 0.721 | 0.817 | 1.203 | 1.329 | 2.083 | 0.459 | 3.378 | nan | 16.000 |
| 2017 | gbm | 0 | 27312 | 1.319 | 0.001 | 0.695 | 0.811 | 0.957 | 1.203 | 1.782 | 1.180 | 9.679 | nan | nan |
| 2017 | gbm | 1 | 27312 | 1.327 | -0.003 | 0.691 | 0.820 | 0.957 | 1.208 | 1.810 | 1.240 | 10.265 | nan | nan |
| 2017 | gbm | 2 | 27312 | 1.327 | -0.003 | 0.691 | 0.818 | 0.963 | 1.208 | 1.799 | 1.162 | 9.715 | nan | nan |
| 2017 | cnn | 0 | 27312 | 1.227 | -0.429 | 0.736 | 0.746 | 0.983 | 1.147 | 2.308 | 88.731 | 66.954 | 103265.000 | nan |
| 2017 | cnn | 1 | 27312 | 1.203 | -0.365 | 0.746 | 0.737 | 0.982 | nan | 2.198 | 62.501 | 61.236 | 103265.000 | nan |
| 2017 | cnn | 2 | 27312 | 1.201 | -0.372 | 0.747 | 0.752 | 0.994 | nan | 2.325 | 64.671 | 66.626 | 103265.000 | nan |
| 2018 | pls | 0 | 16133 | 1.683 | -0.265 | 0.550 | 1.256 | 1.199 | 1.240 | 1.380 | 0.593 | 3.117 | nan | 12.000 |
| 2018 | gbm | 0 | 16133 | 1.578 | 0.131 | 0.605 | 0.929 | 0.927 | 1.094 | 1.302 | 1.748 | 10.200 | nan | nan |
| 2018 | gbm | 1 | 16133 | 1.626 | 0.086 | 0.580 | 0.974 | 0.929 | 1.096 | 1.304 | 1.845 | 10.593 | nan | nan |
| 2018 | gbm | 2 | 16133 | 1.614 | 0.108 | 0.587 | 0.964 | 0.928 | 1.093 | 1.308 | 1.930 | 10.569 | nan | nan |
| 2018 | cnn | 0 | 16133 | 1.238 | 0.213 | 0.757 | 0.687 | 0.895 | 1.056 | 1.292 | 122.699 | 56.040 | 103265.000 | nan |
| 2018 | cnn | 1 | 16133 | 1.268 | 0.288 | 0.745 | 0.667 | 0.895 | nan | 1.279 | 115.763 | 62.253 | 103265.000 | nan |
| 2018 | cnn | 2 | 16133 | 1.259 | 0.142 | 0.749 | 0.727 | 0.909 | nan | 1.291 | 117.680 | 51.464 | 103265.000 | nan |
| 2019 | pls | 0 | 5604 | 1.769 | 0.714 | 0.475 | 1.184 | 1.254 | 1.281 | 1.454 | 0.644 | 2.744 | nan | 12.000 |
| 2019 | gbm | 0 | 5604 | 1.831 | 1.109 | 0.438 | 1.032 | 0.957 | 1.105 | 1.316 | 2.191 | 10.846 | nan | nan |
| 2019 | gbm | 1 | 5604 | 1.822 | 1.114 | 0.443 | 1.017 | 0.960 | 1.106 | 1.330 | 2.226 | 11.161 | nan | nan |
| 2019 | gbm | 2 | 5604 | 1.818 | 1.107 | 0.445 | 1.026 | 0.960 | 1.105 | 1.326 | 2.202 | 12.910 | nan | nan |
| 2019 | cnn | 0 | 5604 | 1.711 | 1.019 | 0.509 | 0.945 | 0.911 | 1.011 | 1.243 | 178.864 | 58.353 | 103265.000 | nan |
| 2019 | cnn | 1 | 5604 | 1.695 | 1.005 | 0.518 | 0.959 | 0.909 | nan | 1.270 | 171.672 | 65.484 | 103265.000 | nan |
| 2019 | cnn | 2 | 5604 | 1.687 | 1.002 | 0.523 | 0.951 | 0.919 | nan | 1.293 | 174.157 | 60.056 | 103265.000 | nan |
| 2020 | pls | 0 | 4452 | 1.583 | -0.391 | 0.636 | 1.216 | 1.245 | 1.302 | 1.470 | 2.786 | 3.663 | nan | 20.000 |
| 2020 | gbm | 0 | 4452 | 1.435 | 0.027 | 0.700 | 1.244 | 1.003 | 1.168 | 1.368 | 2.372 | 12.629 | nan | nan |
| 2020 | gbm | 1 | 4452 | 1.428 | 0.022 | 0.703 | 1.236 | 1.005 | 1.171 | 1.371 | 2.253 | 11.390 | nan | nan |
| 2020 | gbm | 2 | 4452 | 1.442 | 0.004 | 0.697 | 1.256 | 1.004 | 1.168 | 1.356 | 2.312 | 10.379 | nan | nan |
| 2020 | cnn | 0 | 4452 | 1.337 | -0.193 | 0.740 | 1.063 | 0.951 | 1.080 | 1.281 | 192.659 | 60.823 | 103265.000 | nan |
| 2020 | cnn | 1 | 4452 | 1.357 | -0.272 | 0.732 | 1.073 | 0.952 | nan | 1.297 | 183.511 | 60.555 | 103265.000 | nan |
| 2020 | cnn | 2 | 4452 | 1.356 | -0.258 | 0.733 | 1.062 | 0.958 | nan | 1.287 | 187.651 | 77.033 | 103265.000 | nan |
| 2021 | pls | 0 | 1390 | 1.602 | -0.686 | 0.666 | 1.210 | 1.266 | 1.322 | 1.476 | 1.180 | 19.988 | nan | 20.000 |
| 2021 | gbm | 0 | 1390 | 1.728 | -0.953 | 0.611 | 1.106 | 1.012 | 1.175 | 1.350 | 2.457 | 11.852 | nan | nan |
| 2021 | gbm | 1 | 1390 | 1.733 | -0.958 | 0.609 | 1.092 | 1.013 | 1.177 | 1.349 | 2.415 | 13.132 | nan | nan |
| 2021 | gbm | 2 | 1390 | 1.716 | -0.933 | 0.616 | 1.101 | 1.015 | 1.177 | 1.348 | 2.974 | 11.995 | nan | nan |
| 2021 | cnn | 0 | 1390 | 1.537 | -0.955 | 0.692 | 0.976 | 0.960 | 1.070 | 1.276 | 187.675 | 51.654 | 103265.000 | nan |
| 2021 | cnn | 1 | 1390 | 1.505 | -0.919 | 0.705 | 0.965 | 0.963 | nan | 1.298 | 177.757 | 23.596 | 103265.000 | nan |
| 2021 | cnn | 2 | 1390 | 1.518 | -0.923 | 0.700 | 0.987 | 0.972 | nan | 1.293 | 188.102 | 51.741 | 103265.000 | nan |

Table: Table S2. Point predictors: every seed and target season (RMSE, bias, R², cross-validation errors, fit time).


| method | label | m | n_lots | coverage | cov_lo | cov_hi | under | width | iscore | frac_infinite |
|---|---|---|---|---|---|---|---|---|---|---|
| gauss | Gaussian ±z·RMSECV | 0 | 137 | 0.840 | 0.806 | 0.871 | 0.241 | 4.005 | 6.714 | 0.000 |
| scp_sample | Split CP (sample folds) | 0 | 137 | 0.823 | 0.787 | 0.855 | 0.277 | 3.828 | 6.811 | 0.000 |
| scp_lot | Split CP (lot folds) | 0 | 137 | 0.846 | 0.813 | 0.877 | 0.234 | 4.082 | 6.708 | 0.000 |
| scp_season | Split CP (season folds) | 0 | 137 | 0.900 | 0.869 | 0.926 | 0.139 | 5.258 | 7.046 | 0.000 |
| wcp | Weighted CP (covariate shift) | 0 | 137 | 0.909 | 0.883 | 0.931 | 0.161 | 7.124 | 8.544 | 0.050 |
| cqr_sample | CQR (sample folds) | 0 | 137 | 0.794 | 0.758 | 0.827 | 0.380 | 3.869 | 7.271 | 0.000 |
| cqr_season | CQR (season folds) | 0 | 137 | 0.907 | 0.881 | 0.931 | 0.146 | 5.581 | 7.033 | 0.000 |
| qrf | Quantile regression forest | 0 | 137 | 0.841 | 0.813 | 0.866 | 0.292 | 4.281 | 6.758 | 0.000 |
| ensemble | Deep ensemble | 0 | 137 | 0.766 | 0.731 | 0.796 | 0.460 | 3.031 | 6.196 | 0.000 |
| mc_dropout | MC dropout | 0 | 137 | 0.775 | 0.740 | 0.805 | 0.431 | 3.085 | 6.142 | 0.000 |
| lotcp | LotCP | 0 | 137 | 0.899 | 0.868 | 0.926 | 0.124 | 5.448 | 7.293 | 0.000 |
| lotcp_s | LotCP-S | 0 | 137 | 0.894 | 0.862 | 0.922 | 0.139 | 5.394 | 7.260 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 0 | 137 | 0.899 | 0.868 | 0.926 | 0.124 | 5.448 | 7.293 | 0.000 |
| lotcp | LotCP | 3 | 137 | 0.923 | 0.909 | 0.936 | 0.114 | 4.181 | 5.322 | 0.000 |
| lotcp_s | LotCP-S | 3 | 137 | 0.919 | 0.908 | 0.929 | 0.093 | 3.765 | 4.860 | 0.000 |
| biascorr_naive | Bias corr. + source CP | 3 | 137 | 0.921 | 0.908 | 0.934 | 0.090 | 3.828 | 4.957 | 0.000 |
| pooled | Pooled recalibration | 3 | 137 | 0.823 | 0.787 | 0.855 | 0.279 | 3.829 | 6.808 | 0.000 |
| aci | ACI on references | 3 | 137 | 0.873 | 0.856 | 0.890 | 0.208 | 4.056 | 5.943 | 0.018 |
| target_only | Target-only CP | 3 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| target_only_centred | Target-only CP, centred | 3 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 3 | 137 | 0.924 | 0.910 | 0.937 | 0.111 | 4.255 | 5.398 | 0.000 |
| lotcp | LotCP | 5 | 137 | 0.925 | 0.911 | 0.937 | 0.107 | 4.063 | 5.155 | 0.000 |
| lotcp_s | LotCP-S | 5 | 137 | 0.918 | 0.907 | 0.927 | 0.087 | 3.565 | 4.629 | 0.000 |
| biascorr_naive | Bias corr. + source CP | 5 | 137 | 0.931 | 0.918 | 0.943 | 0.069 | 3.828 | 4.797 | 0.000 |
| slopebias_naive | Slope/bias corr. + source CP | 5 | 137 | 0.915 | 0.902 | 0.928 | 0.118 | 3.828 | 5.464 | 0.000 |
| pooled | Pooled recalibration | 5 | 137 | 0.823 | 0.788 | 0.855 | 0.276 | 3.829 | 6.805 | 0.000 |
| aci | ACI on references | 5 | 137 | 0.894 | 0.882 | 0.905 | 0.158 | 4.078 | 5.777 | 0.056 |
| target_only | Target-only CP | 5 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| target_only_centred | Target-only CP, centred | 5 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 5 | 137 | 0.925 | 0.911 | 0.938 | 0.108 | 4.087 | 5.177 | 0.000 |
| lotcp | LotCP | 10 | 137 | 0.926 | 0.912 | 0.939 | 0.104 | 3.966 | 5.015 | 0.000 |
| lotcp_s | LotCP-S | 10 | 137 | 0.919 | 0.909 | 0.928 | 0.077 | 3.446 | 4.460 | 0.000 |
| biascorr_naive | Bias corr. + source CP | 10 | 137 | 0.938 | 0.926 | 0.949 | 0.052 | 3.828 | 4.685 | 0.000 |
| slopebias_naive | Slope/bias corr. + source CP | 10 | 137 | 0.941 | 0.929 | 0.951 | 0.059 | 3.828 | 4.746 | 0.000 |
| pooled | Pooled recalibration | 10 | 137 | 0.823 | 0.788 | 0.855 | 0.278 | 3.830 | 6.801 | 0.000 |
| aci | ACI on references | 10 | 137 | 0.914 | 0.905 | 0.922 | 0.093 | 4.159 | 5.625 | 0.091 |
| target_only | Target-only CP | 10 | 137 | 0.957 | 0.954 | 0.960 | 0.027 | 5.645 | 6.083 | 0.000 |
| target_only_centred | Target-only CP, centred | 10 | 137 | 0.956 | 0.953 | 0.959 | 0.029 | 4.634 | 5.118 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 10 | 137 | 0.927 | 0.912 | 0.939 | 0.102 | 3.972 | 5.015 | 0.000 |
| lotcp | LotCP | 20 | 129 | 0.930 | 0.917 | 0.942 | 0.106 | 3.895 | 4.860 | 0.000 |
| lotcp_s | LotCP-S | 20 | 129 | 0.918 | 0.910 | 0.926 | 0.056 | 3.285 | 4.255 | 0.000 |
| biascorr_naive | Bias corr. + source CP | 20 | 129 | 0.945 | 0.934 | 0.954 | 0.039 | 3.821 | 4.577 | 0.000 |
| slopebias_naive | Slope/bias corr. + source CP | 20 | 129 | 0.953 | 0.944 | 0.962 | 0.034 | 3.821 | 4.505 | 0.000 |
| pooled | Pooled recalibration | 20 | 129 | 0.822 | 0.784 | 0.856 | 0.279 | 3.824 | 6.806 | 0.000 |
| aci | ACI on references | 20 | 129 | 0.917 | 0.911 | 0.923 | 0.070 | 4.176 | 5.503 | 0.095 |
| target_only | Target-only CP | 20 | 129 | 0.931 | 0.929 | 0.933 | 0.030 | 4.717 | 5.391 | 0.000 |
| target_only_centred | Target-only CP, centred | 20 | 129 | 0.932 | 0.930 | 0.933 | 0.030 | 3.577 | 4.286 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 20 | 129 | 0.930 | 0.917 | 0.941 | 0.108 | 3.898 | 4.860 | 0.000 |
| lotcp | LotCP | 30 | 112 | 0.921 | 0.907 | 0.935 | 0.127 | 3.738 | 4.856 | 0.000 |
| lotcp_s | LotCP-S | 30 | 112 | 0.914 | 0.906 | 0.923 | 0.059 | 3.277 | 4.315 | 0.000 |
| biascorr_naive | Bias corr. + source CP | 30 | 112 | 0.941 | 0.930 | 0.952 | 0.047 | 3.809 | 4.636 | 0.000 |
| slopebias_naive | Slope/bias corr. + source CP | 30 | 112 | 0.952 | 0.942 | 0.962 | 0.035 | 3.809 | 4.526 | 0.000 |
| pooled | Pooled recalibration | 30 | 112 | 0.827 | 0.791 | 0.861 | 0.277 | 3.813 | 6.778 | 0.000 |
| aci | ACI on references | 30 | 112 | 0.914 | 0.909 | 0.919 | 0.076 | 4.164 | 5.447 | 0.096 |
| target_only | Target-only CP | 30 | 112 | 0.921 | 0.919 | 0.922 | 0.037 | 4.527 | 5.328 | 0.000 |
| target_only_centred | Target-only CP, centred | 30 | 112 | 0.921 | 0.919 | 0.922 | 0.037 | 3.402 | 4.251 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 30 | 112 | 0.921 | 0.907 | 0.935 | 0.131 | 3.741 | 4.856 | 0.000 |

Table: Table S3. All interval methods, all m (PLS, forward chaining, nominal 0.90), with bootstrap CIs.


**Table S4.** Coverage, width and interval score by target season. (125 rows; provided as `table4_per_season.csv` only.)


| method | m | coverage | jackknife_min | jackknife_max | season_min | season_max | season_mean_unweighted |
|---|---|---|---|---|---|---|---|
| biascorr_naive | 3 | 0.921 | 0.910 | 0.936 | 0.883 | 0.942 | 0.925 |
| biascorr_naive | 5 | 0.931 | 0.921 | 0.945 | 0.894 | 0.950 | 0.935 |
| biascorr_naive | 10 | 0.938 | 0.929 | 0.952 | 0.904 | 0.956 | 0.942 |
| biascorr_naive | 20 | 0.945 | 0.937 | 0.955 | 0.920 | 0.956 | 0.948 |
| biascorr_naive | 30 | 0.941 | 0.929 | 0.951 | 0.918 | 0.956 | 0.940 |
| lotcp | 0 | 0.899 | 0.840 | 0.929 | 0.821 | 0.985 | 0.877 |
| lotcp | 3 | 0.923 | 0.881 | 0.950 | 0.853 | 0.984 | 0.912 |
| lotcp | 5 | 0.925 | 0.884 | 0.951 | 0.855 | 0.984 | 0.914 |
| lotcp | 10 | 0.926 | 0.886 | 0.953 | 0.857 | 0.984 | 0.916 |
| lotcp | 20 | 0.930 | 0.889 | 0.954 | 0.868 | 0.984 | 0.917 |
| lotcp | 30 | 0.921 | 0.874 | 0.950 | 0.859 | 0.980 | 0.903 |
| lotcp_s | 0 | 0.894 | 0.835 | 0.915 | 0.786 | 0.980 | 0.865 |
| lotcp_s | 3 | 0.919 | 0.887 | 0.935 | 0.878 | 0.966 | 0.906 |
| lotcp_s | 5 | 0.918 | 0.890 | 0.932 | 0.880 | 0.958 | 0.908 |
| lotcp_s | 10 | 0.919 | 0.893 | 0.933 | 0.882 | 0.957 | 0.910 |
| lotcp_s | 20 | 0.918 | 0.899 | 0.927 | 0.894 | 0.944 | 0.910 |
| lotcp_s | 30 | 0.914 | 0.896 | 0.922 | 0.882 | 0.936 | 0.904 |
| scp_sample | 0 | 0.823 | 0.781 | 0.843 | 0.760 | 0.884 | 0.806 |
| scp_season | 0 | 0.900 | 0.839 | 0.931 | 0.819 | 0.987 | 0.877 |
| target_only_centred | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| target_only_centred | 5 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| target_only_centred | 10 | 0.956 | 0.949 | 0.958 | 0.930 | 0.966 | 0.950 |
| target_only_centred | 20 | 0.932 | 0.928 | 0.933 | 0.919 | 0.936 | 0.929 |
| target_only_centred | 30 | 0.921 | 0.919 | 0.921 | 0.911 | 0.923 | 0.919 |

Table: Table S4b. Leave-one-season-out jackknife of the pooled lot-macro coverage and per-season extremes.


| method | label | m | n_lots | coverage | cov_lo | cov_hi | under | width | iscore | frac_infinite |
|---|---|---|---|---|---|---|---|---|---|---|
| lotcp | LotCP | 0 | 137 | 0.899 | 0.868 | 0.926 | 0.124 | 5.448 | 7.293 | 0.000 |
| lotcp | LotCP | 3 | 137 | 0.923 | 0.909 | 0.936 | 0.114 | 4.181 | 5.322 | 0.000 |
| lotcp | LotCP | 5 | 137 | 0.925 | 0.911 | 0.937 | 0.107 | 4.063 | 5.155 | 0.000 |
| lotcp | LotCP | 10 | 137 | 0.926 | 0.912 | 0.939 | 0.104 | 3.966 | 5.015 | 0.000 |
| lotcp | LotCP | 20 | 129 | 0.930 | 0.917 | 0.942 | 0.106 | 3.895 | 4.860 | 0.000 |
| lotcp | LotCP | 30 | 112 | 0.921 | 0.907 | 0.935 | 0.127 | 3.738 | 4.856 | 0.000 |
| lotcp_lotfold | LotCP, lot-fold residuals | 0 | 137 | 0.846 | 0.813 | 0.877 | 0.241 | 4.114 | 6.777 | 0.000 |
| lotcp_lotfold | LotCP, lot-fold residuals | 3 | 137 | 0.886 | 0.870 | 0.901 | 0.174 | 3.300 | 4.886 | 0.000 |
| lotcp_lotfold | LotCP, lot-fold residuals | 5 | 137 | 0.888 | 0.872 | 0.903 | 0.167 | 3.215 | 4.727 | 0.000 |
| lotcp_lotfold | LotCP, lot-fold residuals | 10 | 137 | 0.891 | 0.875 | 0.906 | 0.164 | 3.133 | 4.585 | 0.000 |
| lotcp_lotfold | LotCP, lot-fold residuals | 20 | 129 | 0.893 | 0.878 | 0.908 | 0.176 | 3.071 | 4.439 | 0.000 |
| lotcp_lotfold | LotCP, lot-fold residuals | 30 | 112 | 0.884 | 0.868 | 0.901 | 0.208 | 3.023 | 4.554 | 0.000 |
| lotcp_noepisodic | LotCP w/o episodic quantile | 0 | 137 | 0.782 | 0.746 | 0.817 | 0.394 | 3.778 | 7.884 | 0.000 |
| lotcp_noepisodic | LotCP w/o episodic quantile | 3 | 137 | 0.902 | 0.887 | 0.917 | 0.175 | 3.799 | 5.230 | 0.000 |
| lotcp_noepisodic | LotCP w/o episodic quantile | 5 | 137 | 0.911 | 0.896 | 0.925 | 0.152 | 3.799 | 5.082 | 0.000 |
| lotcp_noepisodic | LotCP w/o episodic quantile | 10 | 137 | 0.918 | 0.903 | 0.931 | 0.135 | 3.799 | 4.960 | 0.000 |
| lotcp_noepisodic | LotCP w/o episodic quantile | 20 | 129 | 0.925 | 0.912 | 0.937 | 0.125 | 3.800 | 4.822 | 0.000 |
| lotcp_noepisodic | LotCP w/o episodic quantile | 30 | 112 | 0.918 | 0.904 | 0.932 | 0.142 | 3.673 | 4.833 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 0 | 137 | 0.899 | 0.868 | 0.926 | 0.124 | 5.448 | 7.293 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 3 | 137 | 0.924 | 0.910 | 0.937 | 0.111 | 4.255 | 5.398 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 5 | 137 | 0.925 | 0.911 | 0.938 | 0.108 | 4.087 | 5.177 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 10 | 137 | 0.927 | 0.912 | 0.939 | 0.102 | 3.972 | 5.015 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 20 | 129 | 0.930 | 0.917 | 0.941 | 0.108 | 3.898 | 4.860 | 0.000 |
| lotcp_noshrink | HCP-mean (LotCP w/o shrinkage) | 30 | 112 | 0.921 | 0.907 | 0.935 | 0.131 | 3.741 | 4.856 | 0.000 |
| lotcp_pooled | LotCP, spectrum-pooled weights | 0 | 137 | 0.897 | 0.867 | 0.924 | 0.124 | 5.327 | 7.173 | 0.000 |
| lotcp_pooled | LotCP, spectrum-pooled weights | 3 | 137 | 0.927 | 0.913 | 0.940 | 0.101 | 4.154 | 5.237 | 0.000 |
| lotcp_pooled | LotCP, spectrum-pooled weights | 5 | 137 | 0.930 | 0.916 | 0.942 | 0.090 | 4.048 | 5.071 | 0.000 |
| lotcp_pooled | LotCP, spectrum-pooled weights | 10 | 137 | 0.931 | 0.917 | 0.944 | 0.084 | 3.952 | 4.937 | 0.000 |
| lotcp_pooled | LotCP, spectrum-pooled weights | 20 | 129 | 0.935 | 0.922 | 0.946 | 0.080 | 3.883 | 4.786 | 0.000 |
| lotcp_pooled | LotCP, spectrum-pooled weights | 30 | 112 | 0.930 | 0.917 | 0.943 | 0.092 | 3.881 | 4.885 | 0.000 |
| lotcp_s | LotCP-S | 0 | 137 | 0.894 | 0.862 | 0.922 | 0.139 | 5.394 | 7.260 | 0.000 |
| lotcp_s | LotCP-S | 3 | 137 | 0.919 | 0.908 | 0.929 | 0.093 | 3.765 | 4.860 | 0.000 |
| lotcp_s | LotCP-S | 5 | 137 | 0.918 | 0.907 | 0.927 | 0.087 | 3.565 | 4.629 | 0.000 |
| lotcp_s | LotCP-S | 10 | 137 | 0.919 | 0.909 | 0.928 | 0.077 | 3.446 | 4.460 | 0.000 |
| lotcp_s | LotCP-S | 20 | 129 | 0.918 | 0.910 | 0.926 | 0.056 | 3.285 | 4.255 | 0.000 |
| lotcp_s | LotCP-S | 30 | 112 | 0.914 | 0.906 | 0.923 | 0.059 | 3.277 | 4.315 | 0.000 |
| lotcp_s_lotfold | LotCP-S, lot-fold residuals | 0 | 137 | 0.861 | 0.826 | 0.892 | 0.190 | 4.422 | 6.797 | 0.000 |
| lotcp_s_lotfold | LotCP-S, lot-fold residuals | 3 | 137 | 0.902 | 0.890 | 0.913 | 0.118 | 3.457 | 4.724 | 0.000 |
| lotcp_s_lotfold | LotCP-S, lot-fold residuals | 5 | 137 | 0.906 | 0.896 | 0.916 | 0.098 | 3.368 | 4.527 | 0.000 |
| lotcp_s_lotfold | LotCP-S, lot-fold residuals | 10 | 137 | 0.908 | 0.898 | 0.917 | 0.082 | 3.256 | 4.355 | 0.000 |
| lotcp_s_lotfold | LotCP-S, lot-fold residuals | 20 | 129 | 0.909 | 0.900 | 0.918 | 0.071 | 3.171 | 4.232 | 0.000 |
| lotcp_s_lotfold | LotCP-S, lot-fold residuals | 30 | 112 | 0.908 | 0.900 | 0.918 | 0.071 | 3.206 | 4.305 | 0.000 |
| lotcp_s_rep | LotCP-S, replicate scale only | 0 | 137 | 0.894 | 0.862 | 0.922 | 0.139 | 5.394 | 7.260 | 0.000 |
| lotcp_s_rep | LotCP-S, replicate scale only | 3 | 137 | 0.920 | 0.907 | 0.932 | 0.101 | 3.925 | 5.049 | 0.000 |
| lotcp_s_rep | LotCP-S, replicate scale only | 5 | 137 | 0.922 | 0.909 | 0.933 | 0.095 | 3.805 | 4.876 | 0.000 |
| lotcp_s_rep | LotCP-S, replicate scale only | 10 | 137 | 0.924 | 0.910 | 0.935 | 0.095 | 3.708 | 4.739 | 0.000 |
| lotcp_s_rep | LotCP-S, replicate scale only | 20 | 129 | 0.926 | 0.914 | 0.937 | 0.091 | 3.619 | 4.594 | 0.000 |
| lotcp_s_rep | LotCP-S, replicate scale only | 30 | 112 | 0.920 | 0.907 | 0.933 | 0.103 | 3.546 | 4.642 | 0.000 |
| lotcp_s_support | LotCP-S, reference scale only | 0 | 137 | 0.899 | 0.868 | 0.926 | 0.124 | 5.448 | 7.293 | 0.000 |
| lotcp_s_support | LotCP-S, reference scale only | 3 | 137 | 0.924 | 0.912 | 0.935 | 0.111 | 3.998 | 5.090 | 0.000 |
| lotcp_s_support | LotCP-S, reference scale only | 5 | 137 | 0.926 | 0.915 | 0.936 | 0.091 | 3.809 | 4.825 | 0.000 |
| lotcp_s_support | LotCP-S, reference scale only | 10 | 137 | 0.926 | 0.916 | 0.935 | 0.080 | 3.609 | 4.581 | 0.000 |
| lotcp_s_support | LotCP-S, reference scale only | 20 | 129 | 0.925 | 0.916 | 0.934 | 0.068 | 3.448 | 4.387 | 0.000 |
| lotcp_s_support | LotCP-S, reference scale only | 30 | 112 | 0.925 | 0.917 | 0.934 | 0.049 | 3.455 | 4.399 | 0.000 |
| lotcp_samplefold | LotCP, sample-fold residuals | 0 | 137 | 0.830 | 0.795 | 0.862 | 0.270 | 3.927 | 6.847 | 0.000 |
| lotcp_samplefold | LotCP, sample-fold residuals | 3 | 137 | 0.881 | 0.864 | 0.896 | 0.185 | 3.247 | 4.892 | 0.000 |
| lotcp_samplefold | LotCP, sample-fold residuals | 5 | 137 | 0.884 | 0.868 | 0.899 | 0.178 | 3.169 | 4.729 | 0.000 |
| lotcp_samplefold | LotCP, sample-fold residuals | 10 | 137 | 0.887 | 0.871 | 0.902 | 0.175 | 3.086 | 4.583 | 0.000 |
| lotcp_samplefold | LotCP, sample-fold residuals | 20 | 129 | 0.890 | 0.874 | 0.905 | 0.186 | 3.027 | 4.434 | 0.000 |
| lotcp_samplefold | LotCP, sample-fold residuals | 30 | 112 | 0.880 | 0.864 | 0.898 | 0.222 | 2.981 | 4.554 | 0.000 |

Table: Table S5. Ablation variants, all m.


**Table S6.** All paired Wilcoxon tests of LotCP-S against every other method (interval score and absolute coverage error). (182 rows; provided as `table6_tests.csv` only.)


| m | reference | other | outcome | n_lots | mean_diff | median_diff | ci_lo | ci_hi | p | rank_biserial | seasons_ref_better | n_seasons | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | lotcp_s_support | biascorr_naive | iscore | 137 | 0.1327 | 0.0174 | 0.054 | 0.2046 | 0.0106 | 0.2517 | 4 | 5 | 0.05299 |
| 3 | lotcp_s_support | biascorr_naive | abs_cov_err | 137 | 0.004758 | 0.008184 | -0.0005223 | 0.00991 | 0.05159 | 0.1938 | 3 | 5 | 0.258 |
| 3 | lotcp_s_support | target_only_centred | abs_cov_err | 137 | -0.02664 | -0.02514 | -0.03329 | -0.0189 | 1.247e-14 | -0.7794 | 5 | 5 | 1.621e-13 |
| 5 | lotcp_s_support | biascorr_naive | iscore | 137 | 0.02776 | 0.1217 | -0.04628 | 0.09201 | 0.1681 | 0.1357 | 4 | 5 | 0.3362 |
| 5 | lotcp_s_support | biascorr_naive | abs_cov_err | 137 | 0.0001766 | 0.004086 | -0.005141 | 0.005115 | 0.3609 | 0.09063 | 3 | 5 | 0.5283 |
| 5 | lotcp_s_support | slopebias_naive | iscore | 137 | -0.6388 | -0.6097 | -0.8136 | -0.4787 | 2.641e-09 | -0.5862 | 4 | 5 | 2.905e-08 |
| 5 | lotcp_s_support | slopebias_naive | abs_cov_err | 137 | 0.002515 | 0.005183 | -0.003454 | 0.008236 | 0.2607 | 0.1108 | 4 | 5 | 0.5283 |
| 5 | lotcp_s_support | target_only_centred | abs_cov_err | 137 | -0.03199 | -0.0288 | -0.03813 | -0.025 | 1.008e-16 | -0.8299 | 5 | 5 | 1.411e-15 |
| 10 | lotcp_s_support | biascorr_naive | iscore | 137 | -0.1038 | 0.0673 | -0.1701 | -0.04412 | 0.2861 | -0.105 | 4 | 5 | 0.3362 |
| 10 | lotcp_s_support | biascorr_naive | abs_cov_err | 137 | -0.005267 | -0.0003667 | -0.01009 | -0.0006837 | 0.1761 | -0.1342 | 4 | 5 | 0.5283 |
| 10 | lotcp_s_support | slopebias_naive | iscore | 137 | -0.165 | -0.1184 | -0.2688 | -0.05939 | 0.005204 | -0.2752 | 4 | 5 | 0.03643 |
| 10 | lotcp_s_support | slopebias_naive | abs_cov_err | 137 | -0.006796 | -0.0032 | -0.01248 | -0.001478 | 0.03654 | -0.2074 | 4 | 5 | 0.2193 |
| 10 | lotcp_s_support | target_only_centred | iscore | 137 | -0.5372 | -0.4942 | -0.7872 | -0.3513 | 8.129e-11 | -0.6399 | 5 | 5 | 9.754e-10 |
| 10 | lotcp_s_support | target_only_centred | abs_cov_err | 137 | 0.006043 | 0.009114 | -0.0003324 | 0.01326 | 0.1193 | 0.1534 | 2 | 5 | 0.4772 |
| 20 | lotcp_s_support | biascorr_naive | iscore | 129 | -0.1897 | -0.1123 | -0.2535 | -0.1287 | 2.514e-05 | -0.4275 | 5 | 5 | 0.0002262 |
| 20 | lotcp_s_support | biascorr_naive | abs_cov_err | 129 | -0.007431 | -0.005167 | -0.01214 | -0.002848 | 0.003573 | -0.3003 | 4 | 5 | 0.02501 |
| 20 | lotcp_s_support | slopebias_naive | iscore | 129 | -0.1178 | -0.2475 | -0.246 | 0.01165 | 0.008267 | -0.268 | 3 | 5 | 0.0496 |
| 20 | lotcp_s_support | slopebias_naive | abs_cov_err | 129 | -0.01287 | -0.009773 | -0.01846 | -0.006951 | 1.663e-05 | -0.4421 | 5 | 5 | 0.000133 |
| 20 | lotcp_s_support | target_only_centred | iscore | 129 | 0.1014 | -0.003332 | 0.03728 | 0.1705 | 0.0785 | 0.1785 | 1 | 5 | 0.2355 |
| 20 | lotcp_s_support | target_only_centred | abs_cov_err | 129 | 0.02616 | 0.02474 | 0.02061 | 0.03234 | 2.534e-12 | 0.7104 | 0 | 5 | 2.787e-11 |
| 30 | lotcp_s_support | biascorr_naive | iscore | 112 | -0.2371 | -0.1726 | -0.3122 | -0.1687 | 2.446e-07 | -0.5619 | 5 | 5 | 2.446e-06 |
| 30 | lotcp_s_support | biascorr_naive | abs_cov_err | 112 | -0.01444 | -0.01116 | -0.01969 | -0.009343 | 2.054e-06 | -0.5239 | 4 | 5 | 1.849e-05 |
| 30 | lotcp_s_support | slopebias_naive | iscore | 112 | -0.1264 | -0.2571 | -0.2622 | 0.00363 | 0.01439 | -0.2664 | 4 | 5 | 0.05757 |
| 30 | lotcp_s_support | slopebias_naive | abs_cov_err | 112 | -0.02021 | -0.0155 | -0.02536 | -0.0154 | 1.423e-10 | -0.7045 | 5 | 5 | 1.423e-09 |
| 30 | lotcp_s_support | target_only_centred | iscore | 112 | 0.1478 | 0.05347 | 0.09454 | 0.2036 | 5.728e-05 | 0.4381 | 1 | 5 | 0.0004583 |
| 30 | lotcp_s_support | target_only_centred | abs_cov_err | 112 | 0.02838 | 0.02581 | 0.02323 | 0.03355 | 6.733e-14 | 0.8157 | 0 | 5 | 8.079e-13 |

Table: Table S6b. Paired tests for LotCP-S without replicate-scan information against the bias-correction and target-only baselines.


| model | protocol | method | label | m | n_lots | coverage | cov_lo | cov_hi | under | width | iscore | frac_infinite |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cnn | forward | biascorr_naive | Bias corr. + source CP | 3 | 137 | 0.890 | 0.874 | 0.904 | 0.171 | 3.068 | 4.315 | 0.000 |
| cnn | forward | biascorr_naive | Bias corr. + source CP | 5 | 137 | 0.901 | 0.886 | 0.914 | 0.144 | 3.068 | 4.147 | 0.000 |
| cnn | forward | biascorr_naive | Bias corr. + source CP | 10 | 137 | 0.909 | 0.895 | 0.922 | 0.124 | 3.068 | 4.030 | 0.000 |
| cnn | forward | biascorr_naive | Bias corr. + source CP | 20 | 129 | 0.918 | 0.906 | 0.929 | 0.105 | 3.069 | 3.892 | 0.000 |
| cnn | forward | biascorr_naive | Bias corr. + source CP | 30 | 112 | 0.913 | 0.899 | 0.926 | 0.122 | 3.072 | 3.971 | 0.000 |
| cnn | forward | lotcp | LotCP | 0 | 137 | 0.918 | 0.894 | 0.939 | 0.129 | 4.882 | 6.076 | 0.000 |
| cnn | forward | lotcp | LotCP | 3 | 137 | 0.926 | 0.913 | 0.939 | 0.140 | 4.039 | 4.933 | 0.000 |
| cnn | forward | lotcp | LotCP | 5 | 137 | 0.928 | 0.914 | 0.940 | 0.142 | 3.978 | 4.837 | 0.000 |
| cnn | forward | lotcp | LotCP | 10 | 137 | 0.929 | 0.915 | 0.941 | 0.137 | 3.934 | 4.759 | 0.000 |
| cnn | forward | lotcp | LotCP | 20 | 129 | 0.935 | 0.923 | 0.946 | 0.122 | 3.937 | 4.648 | 0.000 |
| cnn | forward | lotcp | LotCP | 30 | 112 | 0.932 | 0.919 | 0.945 | 0.131 | 3.993 | 4.769 | 0.000 |
| cnn | forward | lotcp_s | LotCP-S | 0 | 137 | 0.915 | 0.889 | 0.937 | 0.122 | 4.605 | 5.849 | 0.000 |
| cnn | forward | lotcp_s | LotCP-S | 3 | 137 | 0.911 | 0.901 | 0.922 | 0.100 | 3.235 | 4.160 | 0.000 |
| cnn | forward | lotcp_s | LotCP-S | 5 | 137 | 0.913 | 0.903 | 0.922 | 0.088 | 3.144 | 4.016 | 0.000 |
| cnn | forward | lotcp_s | LotCP-S | 10 | 137 | 0.913 | 0.904 | 0.922 | 0.071 | 3.055 | 3.875 | 0.000 |
| cnn | forward | lotcp_s | LotCP-S | 20 | 129 | 0.917 | 0.909 | 0.925 | 0.052 | 3.005 | 3.744 | 0.000 |
| cnn | forward | lotcp_s | LotCP-S | 30 | 112 | 0.917 | 0.909 | 0.924 | 0.044 | 3.040 | 3.798 | 0.000 |
| cnn | forward | scp_sample | Split CP (sample folds) | 0 | 137 | 0.789 | 0.759 | 0.817 | 0.418 | 3.068 | 5.999 | 0.000 |
| cnn | forward | scp_season | Split CP (season folds) | 0 | 137 | 0.928 | 0.904 | 0.949 | 0.112 | 5.018 | 6.052 | 0.000 |
| cnn | forward | target_only_centred | Target-only CP, centred | 3 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| cnn | forward | target_only_centred | Target-only CP, centred | 5 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| cnn | forward | target_only_centred | Target-only CP, centred | 10 | 137 | 0.959 | 0.956 | 0.962 | 0.027 | 4.110 | 4.463 | 0.000 |
| cnn | forward | target_only_centred | Target-only CP, centred | 20 | 129 | 0.932 | 0.931 | 0.934 | 0.024 | 3.237 | 3.783 | 0.000 |
| cnn | forward | target_only_centred | Target-only CP, centred | 30 | 112 | 0.922 | 0.921 | 0.924 | 0.027 | 3.131 | 3.774 | 0.000 |
| cnn | loso | lotcp | LotCP | 0 | 198 | 0.913 | 0.895 | 0.931 | 0.126 | 4.189 | 5.359 | 0.000 |
| cnn | loso | lotcp | LotCP | 3 | 198 | 0.912 | 0.902 | 0.923 | 0.128 | 3.172 | 4.211 | 0.000 |
| cnn | loso | lotcp | LotCP | 5 | 198 | 0.913 | 0.902 | 0.924 | 0.122 | 3.088 | 4.103 | 0.000 |
| cnn | loso | lotcp | LotCP | 10 | 198 | 0.914 | 0.903 | 0.925 | 0.112 | 3.013 | 3.998 | 0.000 |
| cnn | loso | lotcp | LotCP | 20 | 184 | 0.915 | 0.904 | 0.926 | 0.110 | 2.953 | 3.902 | 0.000 |
| cnn | loso | lotcp | LotCP | 30 | 161 | 0.916 | 0.903 | 0.928 | 0.121 | 3.001 | 3.956 | 0.000 |
| cnn | loso | lotcp_s | LotCP-S | 0 | 198 | 0.910 | 0.890 | 0.929 | 0.131 | 4.234 | 5.398 | 0.000 |
| cnn | loso | lotcp_s | LotCP-S | 3 | 198 | 0.911 | 0.902 | 0.919 | 0.092 | 3.090 | 4.030 | 0.000 |
| cnn | loso | lotcp_s | LotCP-S | 5 | 198 | 0.909 | 0.901 | 0.917 | 0.087 | 2.968 | 3.895 | 0.000 |
| cnn | loso | lotcp_s | LotCP-S | 10 | 198 | 0.908 | 0.901 | 0.915 | 0.064 | 2.869 | 3.751 | 0.000 |
| cnn | loso | lotcp_s | LotCP-S | 20 | 184 | 0.908 | 0.902 | 0.915 | 0.062 | 2.797 | 3.662 | 0.000 |
| cnn | loso | lotcp_s | LotCP-S | 30 | 161 | 0.908 | 0.901 | 0.914 | 0.059 | 2.812 | 3.662 | 0.000 |
| cnn | loso | scp_season | Split CP (season folds) | 0 | 198 | 0.923 | 0.906 | 0.939 | 0.106 | 4.341 | 5.392 | 0.000 |
| gbm | forward | biascorr_naive | Bias corr. + source CP | 3 | 137 | 0.858 | 0.839 | 0.875 | 0.253 | 3.087 | 5.011 | 0.000 |
| gbm | forward | biascorr_naive | Bias corr. + source CP | 5 | 137 | 0.871 | 0.852 | 0.888 | 0.217 | 3.087 | 4.771 | 0.000 |
| gbm | forward | biascorr_naive | Bias corr. + source CP | 10 | 137 | 0.882 | 0.864 | 0.898 | 0.187 | 3.087 | 4.600 | 0.000 |
| gbm | forward | biascorr_naive | Bias corr. + source CP | 20 | 129 | 0.891 | 0.875 | 0.906 | 0.167 | 3.082 | 4.428 | 0.000 |
| gbm | forward | biascorr_naive | Bias corr. + source CP | 30 | 112 | 0.887 | 0.870 | 0.904 | 0.182 | 3.079 | 4.532 | 0.000 |
| gbm | forward | lotcp | LotCP | 0 | 137 | 0.895 | 0.868 | 0.919 | 0.192 | 4.986 | 6.832 | 0.000 |
| gbm | forward | lotcp | LotCP | 3 | 137 | 0.912 | 0.896 | 0.925 | 0.127 | 3.775 | 5.035 | 0.000 |
| gbm | forward | lotcp | LotCP | 5 | 137 | 0.913 | 0.898 | 0.927 | 0.119 | 3.675 | 4.885 | 0.000 |
| gbm | forward | lotcp | LotCP | 10 | 137 | 0.914 | 0.899 | 0.928 | 0.114 | 3.584 | 4.750 | 0.000 |
| gbm | forward | lotcp | LotCP | 20 | 129 | 0.918 | 0.903 | 0.931 | 0.111 | 3.536 | 4.595 | 0.000 |
| gbm | forward | lotcp | LotCP | 30 | 112 | 0.913 | 0.897 | 0.928 | 0.128 | 3.505 | 4.671 | 0.000 |
| gbm | forward | lotcp_s | LotCP-S | 0 | 137 | 0.898 | 0.870 | 0.922 | 0.168 | 4.968 | 6.703 | 0.000 |
| gbm | forward | lotcp_s | LotCP-S | 3 | 137 | 0.913 | 0.901 | 0.923 | 0.106 | 3.686 | 4.790 | 0.000 |
| gbm | forward | lotcp_s | LotCP-S | 5 | 137 | 0.913 | 0.902 | 0.923 | 0.097 | 3.547 | 4.599 | 0.000 |
| gbm | forward | lotcp_s | LotCP-S | 10 | 137 | 0.912 | 0.902 | 0.921 | 0.085 | 3.398 | 4.409 | 0.000 |
| gbm | forward | lotcp_s | LotCP-S | 20 | 129 | 0.914 | 0.906 | 0.922 | 0.064 | 3.320 | 4.227 | 0.000 |
| gbm | forward | lotcp_s | LotCP-S | 30 | 112 | 0.915 | 0.907 | 0.922 | 0.056 | 3.343 | 4.264 | 0.000 |
| gbm | forward | scp_sample | Split CP (sample folds) | 0 | 137 | 0.759 | 0.724 | 0.792 | 0.511 | 3.087 | 7.115 | 0.000 |
| gbm | forward | scp_season | Split CP (season folds) | 0 | 137 | 0.902 | 0.875 | 0.925 | 0.178 | 4.980 | 6.687 | 0.000 |
| gbm | forward | target_only_centred | Target-only CP, centred | 3 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| gbm | forward | target_only_centred | Target-only CP, centred | 5 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| gbm | forward | target_only_centred | Target-only CP, centred | 10 | 137 | 0.957 | 0.953 | 0.960 | 0.029 | 4.621 | 5.026 | 0.000 |
| gbm | forward | target_only_centred | Target-only CP, centred | 20 | 129 | 0.931 | 0.929 | 0.932 | 0.031 | 3.643 | 4.281 | 0.000 |
| gbm | forward | target_only_centred | Target-only CP, centred | 30 | 112 | 0.921 | 0.920 | 0.922 | 0.036 | 3.496 | 4.253 | 0.000 |
| pls | forward | biascorr_naive | Bias corr. + source CP | 3 | 137 | 0.921 | 0.908 | 0.934 | 0.090 | 3.828 | 4.957 | 0.000 |
| pls | forward | biascorr_naive | Bias corr. + source CP | 5 | 137 | 0.931 | 0.918 | 0.943 | 0.069 | 3.828 | 4.797 | 0.000 |
| pls | forward | biascorr_naive | Bias corr. + source CP | 10 | 137 | 0.938 | 0.926 | 0.949 | 0.052 | 3.828 | 4.685 | 0.000 |
| pls | forward | biascorr_naive | Bias corr. + source CP | 20 | 129 | 0.945 | 0.934 | 0.954 | 0.039 | 3.821 | 4.577 | 0.000 |
| pls | forward | biascorr_naive | Bias corr. + source CP | 30 | 112 | 0.941 | 0.930 | 0.952 | 0.047 | 3.809 | 4.636 | 0.000 |
| pls | forward | lotcp | LotCP | 0 | 137 | 0.899 | 0.868 | 0.926 | 0.124 | 5.448 | 7.293 | 0.000 |
| pls | forward | lotcp | LotCP | 3 | 137 | 0.923 | 0.909 | 0.936 | 0.114 | 4.181 | 5.322 | 0.000 |
| pls | forward | lotcp | LotCP | 5 | 137 | 0.925 | 0.911 | 0.937 | 0.107 | 4.063 | 5.155 | 0.000 |
| pls | forward | lotcp | LotCP | 10 | 137 | 0.926 | 0.912 | 0.939 | 0.104 | 3.966 | 5.015 | 0.000 |
| pls | forward | lotcp | LotCP | 20 | 129 | 0.930 | 0.917 | 0.942 | 0.106 | 3.895 | 4.860 | 0.000 |
| pls | forward | lotcp | LotCP | 30 | 112 | 0.921 | 0.907 | 0.935 | 0.127 | 3.738 | 4.856 | 0.000 |
| pls | forward | lotcp_s | LotCP-S | 0 | 137 | 0.894 | 0.862 | 0.922 | 0.139 | 5.394 | 7.260 | 0.000 |
| pls | forward | lotcp_s | LotCP-S | 3 | 137 | 0.919 | 0.908 | 0.929 | 0.093 | 3.765 | 4.860 | 0.000 |
| pls | forward | lotcp_s | LotCP-S | 5 | 137 | 0.918 | 0.907 | 0.927 | 0.087 | 3.565 | 4.629 | 0.000 |
| pls | forward | lotcp_s | LotCP-S | 10 | 137 | 0.919 | 0.909 | 0.928 | 0.077 | 3.446 | 4.460 | 0.000 |
| pls | forward | lotcp_s | LotCP-S | 20 | 129 | 0.918 | 0.910 | 0.926 | 0.056 | 3.285 | 4.255 | 0.000 |
| pls | forward | lotcp_s | LotCP-S | 30 | 112 | 0.914 | 0.906 | 0.923 | 0.059 | 3.277 | 4.315 | 0.000 |
| pls | forward | scp_sample | Split CP (sample folds) | 0 | 137 | 0.823 | 0.787 | 0.855 | 0.277 | 3.828 | 6.811 | 0.000 |
| pls | forward | scp_season | Split CP (season folds) | 0 | 137 | 0.900 | 0.869 | 0.926 | 0.139 | 5.258 | 7.046 | 0.000 |
| pls | forward | target_only_centred | Target-only CP, centred | 3 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| pls | forward | target_only_centred | Target-only CP, centred | 5 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| pls | forward | target_only_centred | Target-only CP, centred | 10 | 137 | 0.956 | 0.953 | 0.959 | 0.029 | 4.634 | 5.118 | 0.000 |
| pls | forward | target_only_centred | Target-only CP, centred | 20 | 129 | 0.932 | 0.930 | 0.933 | 0.030 | 3.577 | 4.286 | 0.000 |
| pls | forward | target_only_centred | Target-only CP, centred | 30 | 112 | 0.921 | 0.919 | 0.922 | 0.037 | 3.402 | 4.251 | 0.000 |
| pls | loso | biascorr_naive | Bias corr. + source CP | 3 | 198 | 0.934 | 0.924 | 0.943 | 0.064 | 4.069 | 5.019 | 0.000 |
| pls | loso | biascorr_naive | Bias corr. + source CP | 5 | 198 | 0.942 | 0.933 | 0.951 | 0.046 | 4.069 | 4.889 | 0.000 |
| pls | loso | biascorr_naive | Bias corr. + source CP | 10 | 198 | 0.949 | 0.941 | 0.957 | 0.032 | 4.069 | 4.785 | 0.000 |
| pls | loso | biascorr_naive | Bias corr. + source CP | 20 | 184 | 0.954 | 0.947 | 0.962 | 0.025 | 4.068 | 4.731 | 0.000 |
| pls | loso | biascorr_naive | Bias corr. + source CP | 30 | 161 | 0.954 | 0.946 | 0.961 | 0.027 | 4.068 | 4.702 | 0.000 |
| pls | loso | lotcp | LotCP | 0 | 198 | 0.901 | 0.879 | 0.922 | 0.146 | 4.847 | 6.483 | 0.000 |
| pls | loso | lotcp | LotCP | 3 | 198 | 0.906 | 0.895 | 0.917 | 0.131 | 3.558 | 4.850 | 0.000 |
| pls | loso | lotcp | LotCP | 5 | 198 | 0.907 | 0.895 | 0.918 | 0.128 | 3.456 | 4.710 | 0.000 |
| pls | loso | lotcp | LotCP | 10 | 198 | 0.908 | 0.897 | 0.919 | 0.122 | 3.361 | 4.570 | 0.000 |
| pls | loso | lotcp | LotCP | 20 | 184 | 0.909 | 0.897 | 0.920 | 0.122 | 3.285 | 4.473 | 0.000 |
| pls | loso | lotcp | LotCP | 30 | 161 | 0.909 | 0.897 | 0.921 | 0.124 | 3.293 | 4.448 | 0.000 |
| pls | loso | lotcp_s | LotCP-S | 0 | 198 | 0.902 | 0.880 | 0.923 | 0.152 | 4.936 | 6.472 | 0.000 |
| pls | loso | lotcp_s | LotCP-S | 3 | 198 | 0.905 | 0.897 | 0.914 | 0.105 | 3.477 | 4.675 | 0.000 |
| pls | loso | lotcp_s | LotCP-S | 5 | 198 | 0.905 | 0.896 | 0.913 | 0.097 | 3.349 | 4.514 | 0.000 |
| pls | loso | lotcp_s | LotCP-S | 10 | 198 | 0.905 | 0.898 | 0.913 | 0.080 | 3.235 | 4.345 | 0.000 |
| pls | loso | lotcp_s | LotCP-S | 20 | 184 | 0.906 | 0.899 | 0.913 | 0.071 | 3.152 | 4.237 | 0.000 |
| pls | loso | lotcp_s | LotCP-S | 30 | 161 | 0.905 | 0.898 | 0.912 | 0.074 | 3.130 | 4.193 | 0.000 |
| pls | loso | scp_sample | Split CP (sample folds) | 0 | 198 | 0.849 | 0.824 | 0.874 | 0.232 | 4.069 | 6.567 | 0.000 |
| pls | loso | scp_season | Split CP (season folds) | 0 | 198 | 0.896 | 0.874 | 0.917 | 0.157 | 4.694 | 6.430 | 0.000 |
| pls | loso | target_only_centred | Target-only CP, centred | 3 | 198 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| pls | loso | target_only_centred | Target-only CP, centred | 5 | 198 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| pls | loso | target_only_centred | Target-only CP, centred | 10 | 198 | 0.957 | 0.955 | 0.960 | 0.028 | 4.633 | 5.105 | 0.000 |
| pls | loso | target_only_centred | Target-only CP, centred | 20 | 184 | 0.932 | 0.930 | 0.933 | 0.031 | 3.615 | 4.328 | 0.000 |
| pls | loso | target_only_centred | Target-only CP, centred | 30 | 161 | 0.921 | 0.920 | 0.922 | 0.039 | 3.368 | 4.175 | 0.000 |

Table: Table S7. Predictors and protocols.


| model | method | m | n_seeds | coverage_mean | width_mean | iscore_mean | coverage_sd | width_sd | iscore_sd |
|---|---|---|---|---|---|---|---|---|---|
| cnn | aci | 3 | 3 | 0.843 | 3.313 | 5.223 | 0.003 | 0.022 | 0.097 |
| cnn | aci | 5 | 3 | 0.863 | 3.388 | 5.055 | 0.002 | 0.014 | 0.010 |
| cnn | aci | 10 | 3 | 0.890 | 3.538 | 4.955 | 0.001 | 0.013 | 0.052 |
| cnn | aci | 20 | 3 | 0.903 | 3.643 | 4.784 | 0.000 | 0.009 | 0.008 |
| cnn | aci | 30 | 3 | 0.904 | 3.713 | 4.820 | 0.000 | 0.021 | 0.020 |
| cnn | biascorr_naive | 3 | 3 | 0.890 | 3.068 | 4.315 | 0.003 | 0.020 | 0.041 |
| cnn | biascorr_naive | 5 | 3 | 0.901 | 3.068 | 4.147 | 0.004 | 0.020 | 0.035 |
| cnn | biascorr_naive | 10 | 3 | 0.909 | 3.068 | 4.030 | 0.003 | 0.020 | 0.031 |
| cnn | biascorr_naive | 20 | 3 | 0.918 | 3.069 | 3.892 | 0.004 | 0.020 | 0.031 |
| cnn | biascorr_naive | 30 | 3 | 0.913 | 3.072 | 3.971 | 0.004 | 0.020 | 0.042 |
| cnn | gauss | 0 | 3 | 0.797 | 3.122 | 5.933 | 0.004 | 0.021 | 0.032 |
| cnn | lotcp | 0 | 3 | 0.918 | 4.882 | 6.076 | 0.001 | 0.041 | 0.033 |
| cnn | lotcp | 3 | 3 | 0.926 | 4.039 | 4.933 | 0.002 | 0.071 | 0.034 |
| cnn | lotcp | 5 | 3 | 0.928 | 3.978 | 4.837 | 0.002 | 0.070 | 0.043 |
| cnn | lotcp | 10 | 3 | 0.929 | 3.934 | 4.759 | 0.001 | 0.072 | 0.041 |
| cnn | lotcp | 20 | 3 | 0.935 | 3.937 | 4.648 | 0.002 | 0.064 | 0.032 |
| cnn | lotcp | 30 | 3 | 0.932 | 3.993 | 4.769 | 0.002 | 0.078 | 0.034 |
| cnn | lotcp_s | 0 | 3 | 0.915 | 4.605 | 5.849 | 0.002 | 0.016 | 0.030 |
| cnn | lotcp_s | 3 | 3 | 0.911 | 3.235 | 4.160 | 0.001 | 0.014 | 0.024 |
| cnn | lotcp_s | 5 | 3 | 0.913 | 3.144 | 4.016 | 0.002 | 0.014 | 0.023 |
| cnn | lotcp_s | 10 | 3 | 0.913 | 3.055 | 3.875 | 0.001 | 0.010 | 0.024 |
| cnn | lotcp_s | 20 | 3 | 0.917 | 3.005 | 3.744 | 0.001 | 0.006 | 0.021 |
| cnn | lotcp_s | 30 | 3 | 0.917 | 3.040 | 3.798 | 0.001 | 0.005 | 0.025 |
| cnn | pooled | 3 | 3 | 0.790 | 3.069 | 5.996 | 0.004 | 0.020 | 0.031 |
| cnn | pooled | 5 | 3 | 0.789 | 3.069 | 5.997 | 0.004 | 0.020 | 0.032 |
| cnn | pooled | 10 | 3 | 0.790 | 3.070 | 5.993 | 0.004 | 0.020 | 0.031 |
| cnn | pooled | 20 | 3 | 0.793 | 3.073 | 5.887 | 0.003 | 0.020 | 0.034 |
| cnn | pooled | 30 | 3 | 0.789 | 3.080 | 5.941 | 0.005 | 0.020 | 0.054 |
| cnn | scp_lot | 0 | 1 | 0.845 | 3.548 | 5.636 | nan | nan | nan |
| cnn | scp_sample | 0 | 3 | 0.789 | 3.068 | 5.999 | 0.004 | 0.020 | 0.032 |
| cnn | scp_season | 0 | 3 | 0.928 | 5.018 | 6.052 | 0.001 | 0.065 | 0.055 |
| cnn | target_only | 3 | 3 | 1.000 | nan | nan | 0.000 | nan | nan |
| cnn | target_only | 5 | 3 | 1.000 | nan | nan | 0.000 | nan | nan |
| cnn | target_only | 10 | 3 | 0.959 | 5.056 | 5.409 | 0.001 | 0.024 | 0.019 |
| cnn | target_only | 20 | 3 | 0.932 | 4.233 | 4.802 | 0.000 | 0.007 | 0.004 |
| cnn | target_only | 30 | 3 | 0.922 | 4.117 | 4.783 | 0.000 | 0.016 | 0.020 |
| cnn | target_only_centred | 3 | 3 | 1.000 | nan | nan | 0.000 | nan | nan |
| cnn | target_only_centred | 5 | 3 | 1.000 | nan | nan | 0.000 | nan | nan |
| cnn | target_only_centred | 10 | 3 | 0.959 | 4.110 | 4.463 | 0.000 | 0.035 | 0.035 |
| cnn | target_only_centred | 20 | 3 | 0.932 | 3.237 | 3.783 | 0.000 | 0.018 | 0.023 |
| cnn | target_only_centred | 30 | 3 | 0.922 | 3.131 | 3.774 | 0.000 | 0.021 | 0.030 |
| gbm | aci | 3 | 3 | 0.828 | 3.432 | 6.131 | 0.001 | 0.004 | 0.039 |
| gbm | aci | 5 | 3 | 0.857 | 3.528 | 5.885 | 0.001 | 0.005 | 0.043 |
| gbm | aci | 10 | 3 | 0.892 | 3.721 | 5.705 | 0.001 | 0.006 | 0.028 |
| gbm | aci | 20 | 3 | 0.906 | 3.865 | 5.495 | 0.000 | 0.005 | 0.037 |
| gbm | aci | 30 | 3 | 0.907 | 3.909 | 5.537 | 0.001 | 0.007 | 0.028 |
| gbm | biascorr_naive | 3 | 3 | 0.858 | 3.087 | 5.011 | 0.002 | 0.001 | 0.033 |
| gbm | biascorr_naive | 5 | 3 | 0.871 | 3.087 | 4.771 | 0.002 | 0.001 | 0.024 |
| gbm | biascorr_naive | 10 | 3 | 0.882 | 3.087 | 4.600 | 0.002 | 0.001 | 0.024 |
| gbm | biascorr_naive | 20 | 3 | 0.891 | 3.082 | 4.428 | 0.002 | 0.001 | 0.027 |
| gbm | biascorr_naive | 30 | 3 | 0.887 | 3.079 | 4.532 | 0.001 | 0.001 | 0.028 |
| gbm | gauss | 0 | 3 | 0.770 | 3.160 | 7.016 | 0.001 | 0.005 | 0.046 |
| gbm | lotcp | 0 | 3 | 0.895 | 4.986 | 6.832 | 0.001 | 0.025 | 0.060 |
| gbm | lotcp | 3 | 3 | 0.912 | 3.775 | 5.035 | 0.001 | 0.010 | 0.023 |
| gbm | lotcp | 5 | 3 | 0.913 | 3.675 | 4.885 | 0.001 | 0.007 | 0.020 |
| gbm | lotcp | 10 | 3 | 0.914 | 3.584 | 4.750 | 0.000 | 0.008 | 0.022 |
| gbm | lotcp | 20 | 3 | 0.918 | 3.536 | 4.595 | 0.001 | 0.009 | 0.027 |
| gbm | lotcp | 30 | 3 | 0.913 | 3.505 | 4.671 | 0.000 | 0.007 | 0.031 |
| gbm | lotcp_s | 0 | 3 | 0.898 | 4.968 | 6.703 | 0.001 | 0.034 | 0.058 |
| gbm | lotcp_s | 3 | 3 | 0.913 | 3.686 | 4.790 | 0.000 | 0.013 | 0.014 |
| gbm | lotcp_s | 5 | 3 | 0.913 | 3.547 | 4.599 | 0.001 | 0.005 | 0.022 |
| gbm | lotcp_s | 10 | 3 | 0.912 | 3.398 | 4.409 | 0.001 | 0.014 | 0.013 |
| gbm | lotcp_s | 20 | 3 | 0.914 | 3.320 | 4.227 | 0.002 | 0.041 | 0.030 |
| gbm | lotcp_s | 30 | 3 | 0.915 | 3.343 | 4.264 | 0.003 | 0.038 | 0.020 |
| gbm | pooled | 3 | 3 | 0.760 | 3.089 | 7.110 | 0.002 | 0.001 | 0.047 |
| gbm | pooled | 5 | 3 | 0.760 | 3.089 | 7.112 | 0.002 | 0.002 | 0.053 |
| gbm | pooled | 10 | 3 | 0.760 | 3.091 | 7.107 | 0.002 | 0.002 | 0.050 |
| gbm | pooled | 20 | 3 | 0.759 | 3.089 | 7.048 | 0.002 | 0.002 | 0.059 |
| gbm | pooled | 30 | 3 | 0.760 | 3.090 | 7.138 | 0.002 | 0.002 | 0.071 |
| gbm | scp_lot | 0 | 3 | 0.833 | 3.715 | 6.536 | 0.002 | 0.007 | 0.039 |
| gbm | scp_sample | 0 | 3 | 0.759 | 3.087 | 7.115 | 0.002 | 0.001 | 0.051 |
| gbm | scp_season | 0 | 3 | 0.902 | 4.980 | 6.687 | 0.000 | 0.037 | 0.059 |
| gbm | target_only | 3 | 3 | 1.000 | nan | nan | 0.000 | nan | nan |
| gbm | target_only | 5 | 3 | 1.000 | nan | nan | 0.000 | nan | nan |
| gbm | target_only | 10 | 3 | 0.956 | 5.610 | 6.033 | 0.000 | 0.034 | 0.030 |
| gbm | target_only | 20 | 3 | 0.930 | 4.699 | 5.372 | 0.001 | 0.014 | 0.026 |
| gbm | target_only | 30 | 3 | 0.921 | 4.541 | 5.341 | 0.001 | 0.019 | 0.031 |
| gbm | target_only_centred | 3 | 3 | 1.000 | nan | nan | 0.000 | nan | nan |
| gbm | target_only_centred | 5 | 3 | 1.000 | nan | nan | 0.000 | nan | nan |
| gbm | target_only_centred | 10 | 3 | 0.957 | 4.621 | 5.026 | 0.000 | 0.024 | 0.019 |
| gbm | target_only_centred | 20 | 3 | 0.931 | 3.643 | 4.281 | 0.000 | 0.010 | 0.014 |
| gbm | target_only_centred | 30 | 3 | 0.921 | 3.496 | 4.253 | 0.001 | 0.007 | 0.015 |

Table: Table S7b. Seed-to-seed spread of lot-macro metrics (LightGBM, CNN).


| nominal | method | label | m | n_lots | coverage | cov_lo | cov_hi | under | width | iscore | frac_infinite |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.950 | lotcp | LotCP | 0 | 137 | 0.945 | 0.921 | 0.964 | 0.102 | 7.485 | 9.383 | 0.000 |
| 0.950 | lotcp | LotCP | 3 | 137 | 0.963 | 0.952 | 0.971 | 0.067 | 5.617 | 6.780 | 0.000 |
| 0.950 | lotcp | LotCP | 5 | 137 | 0.964 | 0.954 | 0.972 | 0.058 | 5.437 | 6.559 | 0.000 |
| 0.950 | lotcp | LotCP | 10 | 137 | 0.964 | 0.954 | 0.973 | 0.056 | 5.310 | 6.385 | 0.000 |
| 0.950 | lotcp | LotCP | 20 | 129 | 0.968 | 0.960 | 0.975 | 0.045 | 5.298 | 6.247 | 0.000 |
| 0.950 | lotcp | LotCP | 30 | 112 | 0.962 | 0.953 | 0.971 | 0.060 | 5.018 | 6.169 | 0.000 |
| 0.950 | lotcp_s | LotCP-S | 0 | 137 | 0.938 | 0.912 | 0.959 | 0.124 | 7.050 | 9.068 | 0.000 |
| 0.950 | lotcp_s | LotCP-S | 3 | 137 | 0.961 | 0.953 | 0.968 | 0.051 | 4.844 | 5.950 | 0.000 |
| 0.950 | lotcp_s | LotCP-S | 5 | 137 | 0.962 | 0.955 | 0.968 | 0.041 | 4.539 | 5.589 | 0.000 |
| 0.950 | lotcp_s | LotCP-S | 10 | 137 | 0.962 | 0.957 | 0.967 | 0.030 | 4.270 | 5.265 | 0.000 |
| 0.950 | lotcp_s | LotCP-S | 20 | 129 | 0.963 | 0.957 | 0.968 | 0.025 | 4.135 | 5.109 | 0.000 |
| 0.950 | lotcp_s | LotCP-S | 30 | 112 | 0.964 | 0.959 | 0.968 | 0.024 | 4.158 | 5.153 | 0.000 |
| 0.950 | scp_sample | Split CP (sample folds) | 0 | 137 | 0.889 | 0.858 | 0.915 | 0.197 | 4.632 | 8.306 | 0.000 |
| 0.950 | scp_season | Split CP (season folds) | 0 | 137 | 0.940 | 0.916 | 0.960 | 0.117 | 6.782 | 8.749 | 0.000 |
| 0.950 | target_only_centred | Target-only CP, centred | 3 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| 0.950 | target_only_centred | Target-only CP, centred | 5 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| 0.950 | target_only_centred | Target-only CP, centred | 10 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| 0.950 | target_only_centred | Target-only CP, centred | 20 | 129 | 0.981 | 0.979 | 0.983 | 0.010 | 5.544 | 6.008 | 0.000 |
| 0.950 | target_only_centred | Target-only CP, centred | 30 | 112 | 0.972 | 0.971 | 0.974 | 0.013 | 4.745 | 5.434 | 0.000 |
| 0.900 | lotcp | LotCP | 0 | 137 | 0.899 | 0.868 | 0.926 | 0.124 | 5.448 | 7.293 | 0.000 |
| 0.900 | lotcp | LotCP | 3 | 137 | 0.923 | 0.909 | 0.936 | 0.114 | 4.181 | 5.322 | 0.000 |
| 0.900 | lotcp | LotCP | 5 | 137 | 0.925 | 0.911 | 0.937 | 0.107 | 4.063 | 5.155 | 0.000 |
| 0.900 | lotcp | LotCP | 10 | 137 | 0.926 | 0.912 | 0.939 | 0.104 | 3.966 | 5.015 | 0.000 |
| 0.900 | lotcp | LotCP | 20 | 129 | 0.930 | 0.917 | 0.942 | 0.106 | 3.895 | 4.860 | 0.000 |
| 0.900 | lotcp | LotCP | 30 | 112 | 0.921 | 0.907 | 0.935 | 0.127 | 3.738 | 4.856 | 0.000 |
| 0.900 | lotcp_s | LotCP-S | 0 | 137 | 0.894 | 0.862 | 0.922 | 0.139 | 5.394 | 7.260 | 0.000 |
| 0.900 | lotcp_s | LotCP-S | 3 | 137 | 0.919 | 0.908 | 0.929 | 0.093 | 3.765 | 4.860 | 0.000 |
| 0.900 | lotcp_s | LotCP-S | 5 | 137 | 0.918 | 0.907 | 0.927 | 0.087 | 3.565 | 4.629 | 0.000 |
| 0.900 | lotcp_s | LotCP-S | 10 | 137 | 0.919 | 0.909 | 0.928 | 0.077 | 3.446 | 4.460 | 0.000 |
| 0.900 | lotcp_s | LotCP-S | 20 | 129 | 0.918 | 0.910 | 0.926 | 0.056 | 3.285 | 4.255 | 0.000 |
| 0.900 | lotcp_s | LotCP-S | 30 | 112 | 0.914 | 0.906 | 0.923 | 0.059 | 3.277 | 4.315 | 0.000 |
| 0.900 | scp_sample | Split CP (sample folds) | 0 | 137 | 0.823 | 0.787 | 0.855 | 0.277 | 3.828 | 6.811 | 0.000 |
| 0.900 | scp_season | Split CP (season folds) | 0 | 137 | 0.900 | 0.869 | 0.926 | 0.139 | 5.258 | 7.046 | 0.000 |
| 0.900 | target_only_centred | Target-only CP, centred | 3 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| 0.900 | target_only_centred | Target-only CP, centred | 5 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| 0.900 | target_only_centred | Target-only CP, centred | 10 | 137 | 0.956 | 0.953 | 0.959 | 0.029 | 4.634 | 5.118 | 0.000 |
| 0.900 | target_only_centred | Target-only CP, centred | 20 | 129 | 0.932 | 0.930 | 0.933 | 0.030 | 3.577 | 4.286 | 0.000 |
| 0.900 | target_only_centred | Target-only CP, centred | 30 | 112 | 0.921 | 0.919 | 0.922 | 0.037 | 3.402 | 4.251 | 0.000 |
| 0.800 | lotcp | LotCP | 0 | 137 | 0.809 | 0.773 | 0.842 | 0.190 | 4.038 | 5.797 | 0.000 |
| 0.800 | lotcp | LotCP | 3 | 137 | 0.840 | 0.821 | 0.857 | 0.160 | 2.950 | 4.082 | 0.000 |
| 0.800 | lotcp | LotCP | 5 | 137 | 0.843 | 0.824 | 0.861 | 0.162 | 2.873 | 3.954 | 0.000 |
| 0.800 | lotcp | LotCP | 10 | 137 | 0.845 | 0.827 | 0.863 | 0.164 | 2.801 | 3.843 | 0.000 |
| 0.800 | lotcp | LotCP | 20 | 129 | 0.846 | 0.827 | 0.864 | 0.170 | 2.714 | 3.704 | 0.000 |
| 0.800 | lotcp | LotCP | 30 | 112 | 0.832 | 0.813 | 0.852 | 0.196 | 2.630 | 3.723 | 0.000 |
| 0.800 | lotcp_s | LotCP-S | 0 | 137 | 0.809 | 0.772 | 0.844 | 0.212 | 4.020 | 5.786 | 0.000 |
| 0.800 | lotcp_s | LotCP-S | 3 | 137 | 0.831 | 0.815 | 0.845 | 0.140 | 2.806 | 3.916 | 0.000 |
| 0.800 | lotcp_s | LotCP-S | 5 | 137 | 0.832 | 0.816 | 0.845 | 0.124 | 2.692 | 3.752 | 0.000 |
| 0.800 | lotcp_s | LotCP-S | 10 | 137 | 0.837 | 0.822 | 0.850 | 0.113 | 2.651 | 3.656 | 0.000 |
| 0.800 | lotcp_s | LotCP-S | 20 | 129 | 0.835 | 0.822 | 0.848 | 0.095 | 2.549 | 3.507 | 0.000 |
| 0.800 | lotcp_s | LotCP-S | 30 | 112 | 0.830 | 0.818 | 0.843 | 0.097 | 2.542 | 3.531 | 0.000 |
| 0.800 | scp_sample | Split CP (sample folds) | 0 | 137 | 0.716 | 0.677 | 0.753 | 0.372 | 2.943 | 5.444 | 0.000 |
| 0.800 | scp_season | Split CP (season folds) | 0 | 137 | 0.820 | 0.785 | 0.853 | 0.175 | 3.916 | 5.568 | 0.000 |
| 0.800 | target_only_centred | Target-only CP, centred | 3 | 137 | 1.000 | 1.000 | 1.000 | 0.000 | nan | nan | 1.000 |
| 0.800 | target_only_centred | Target-only CP, centred | 5 | 137 | 0.897 | 0.891 | 0.903 | 0.064 | 3.745 | 4.315 | 0.000 |
| 0.800 | target_only_centred | Target-only CP, centred | 10 | 137 | 0.858 | 0.856 | 0.861 | 0.061 | 2.923 | 3.663 | 0.000 |
| 0.800 | target_only_centred | Target-only CP, centred | 20 | 129 | 0.832 | 0.830 | 0.834 | 0.064 | 2.577 | 3.434 | 0.000 |
| 0.800 | target_only_centred | Target-only CP, centred | 30 | 112 | 0.821 | 0.820 | 0.823 | 0.071 | 2.520 | 3.446 | 0.000 |

Table: Table S8. Nominal levels 0.80, 0.90, 0.95.


| m | correction | rmse | abs_bias | n_lots |
|---|---|---|---|---|
| 0 | mean | 1.362 | 0.861 | 137 |
| 0 | none | 1.362 | 0.861 | 137 |
| 0 | shrinkage | 1.422 | 0.933 | 137 |
| 3 | mean | 1.057 | 0.382 | 137 |
| 3 | none | 1.362 | 0.861 | 137 |
| 3 | shrinkage | 1.046 | 0.365 | 137 |
| 5 | mean | 1.015 | 0.306 | 137 |
| 5 | none | 1.362 | 0.863 | 137 |
| 5 | shrinkage | 1.012 | 0.301 | 137 |
| 10 | mean | 0.982 | 0.231 | 137 |
| 10 | none | 1.362 | 0.864 | 137 |
| 10 | shrinkage | 0.980 | 0.229 | 137 |
| 20 | mean | 0.958 | 0.191 | 129 |
| 20 | none | 1.365 | 0.880 | 129 |
| 20 | shrinkage | 0.958 | 0.190 | 129 |
| 30 | mean | 0.978 | 0.197 | 112 |
| 30 | none | 1.361 | 0.862 | 112 |
| 30 | shrinkage | 0.977 | 0.196 | 112 |

Table: Table S9. Point-prediction error after bias correction as a function of m.


| model | total_seconds | fit_seconds_final |
|---|---|---|
| cnn | 1395.042 | 147.606 |
| gbm | 37.664 | 2.034 |
| pls | 39.705 | 1.132 |

Table: Table S10. Cross-fitting time per target season (three fold schemes plus final model).


| method | rmse | abs_bias | coverage | width |
|---|---|---|---|---|
| bias_correction | 0.983 | 0.145 | 0.938 | 3.828 |
| none | 1.363 | 0.866 | 0.822 | 3.828 |
| spiking_x1 | 1.344 | 0.845 | 0.828 | 3.828 |
| spiking_x20 | 1.164 | 0.638 | 0.884 | 3.828 |

Table: Table S11. Spiking baseline (refit with the reference samples added) at m = 10.


![Fig. S1. Training loss of the 1D-CNN (seed 0) for the five target seasons.](figures/figS1_cnn_training.png){width=3.5in}


# Pre-specified protocol and deviation log

# Pre-specified experimental protocol (written before any model was trained)

Date fixed: 2026-11-10. Changes after this date are logged at the bottom under "Deviations".

## Target journal (selected first, see `Target_Journal_Submission/journal_selection/`)
Smart Agricultural Technology (Elsevier).

## Problem
A near-infrared (NIR) calibration for mango dry-matter content (DMC) trained on past seasons is
deployed on a new harvest lot ("population" in the data set) in a later season. For every scanned
fruit the user wants a prediction interval with coverage 1 - alpha. The user can afford `m`
destructive reference measurements in the new lot (m = 0, 3, 5, 10, 20, 30).

## Hypotheses
* H1. Split-conformal intervals calibrated on held-out samples from the training seasons
  under-cover on lots of a later season (coverage below nominal by > 5 points at 1 - alpha = 0.9).
* H2. The unit at which calibration residuals are held out matters: sample-held-out <
  lot-held-out < season-held-out in achieved next-season coverage.
* H3. With m > 0 reference samples, a shrinkage bias correction whose conformal quantile is
  calibrated by replaying the m-shot protocol on past lots (LotCP) attains near-nominal
  lot-marginal coverage for every m, with narrower intervals than (i) m = 0 season-held-out
  calibration and (ii) target-only conformal calibration at the same m.
* H4. Each LotCP component (season-held-out residuals, shrinkage, episodic quantile) contributes;
  removing a component degrades coverage or interval score.

## Research questions -> experiments
* RQ1 (H1, H2): How far does coverage fall on next-season lots, and which hold-out unit repairs it? -> E1, E3
* RQ2 (H3): Coverage/width of LotCP against strong baselines as a function of m. -> E1, E2
* RQ3 (H4): Component ablation. -> E3
* RQ4: Robustness (alpha, protocol, source size, label noise, outlier filtering, shift type) and
  generalisation across point predictors. -> E4, E5, E7
* RQ5: Cost (compute, number of reference samples) and failure modes. -> E6, E8

## Data
Mango DMC and NIR spectra, Mendeley Data doi:10.17632/46htwnp833 version 6, file
`MangoDMC_NIR_Data_v4.csv` (CC BY 4.0). 85,401 spectra, 7 seasons (2015-2021), 199 lots.
All spectra are kept in the main analysis (the provider's outlier flags are used only in a
sensitivity analysis because we do not know whether they were derived from reference residuals).
Spectral window 684-990 nm (3 nm step).

## Splitting / leakage rules
* Primary protocol (forward chaining): target season T in {2017,...,2021}; training data are all
  seasons < T. No information from season >= T is used for training, model selection,
  preprocessing statistics or calibration, except the m labelled reference samples of the lot
  under test.
* Secondary protocol: leave-one-season-out over all 7 seasons (non-causal, robustness only).
* The same physical sample (`reference_no`) is scanned repeatedly; all folds are grouped so that a
  sample never straddles a split. Reference draws are made at sample level and all spectra of a
  drawn sample are removed from the evaluation set of that draw.
* Hyper-parameters are selected on source data only (leave-one-season-out CV inside the source).

## Point predictors
PLS regression (SNV + Savitzky-Golay 2nd derivative), 1D-CNN, LightGBM. Seeds for stochastic
models: 0, 1, 2 (fixed in advance; all reported, mean +- SD).

## Interval methods
m = 0: Gaussian +-z*RMSECV; split/cross-conformal with sample-, lot- and season-grouped folds;
weighted conformal for covariate shift (density ratio from unlabelled target spectra);
conformalised quantile regression; quantile regression forest; deep ensemble (Gaussian NLL).
m > 0: target-only split conformal; mean bias correction + source quantile; pooling target
residuals into the source calibration set; adaptive conformal inference run over the reference
samples; LotCP (proposed) and its ablations.

## Evaluation
Unit of analysis: target lot (lots with >= 20 samples so that at least 10 samples remain for
evaluation at the largest m that the lot admits; a lot is evaluated at a given m only when it has
>= m + 10 samples). R = 100 random reference draws per lot and m (seeded).
Metrics: coverage (lot-macro and pooled), share of lot-draws with coverage < 1 - alpha - 0.10,
mean interval width, Winkler interval score, RMSE and bias of the (corrected) point prediction.
Nominal level: 1 - alpha = 0.90 (primary); 0.80 and 0.95 (sensitivity).

## Statistics
Paired Wilcoxon signed-rank tests across target lots on per-lot interval score and per-lot
|coverage - nominal| (LotCP vs each baseline at each m), Holm correction within family, matched-pairs
rank-biserial effect size, lot-level cluster bootstrap 95% CIs (2,000 resamples); per-season
results are always shown because seasons (n = 5) are the top-level cluster.

## Deviations
* D1 (2026-11-10, after the first smoke test on PLS / target season 2018, the only target results
  seen at that time). The pre-specified location-only LotCP under-covered (0.85-0.87 at nominal
  0.90) because the within-lot residual *scale* was larger in 2018 than in the source seasons.
  Hypothesis: residual scale, not only bias, is lot specific. Change: a scale-adaptive variant
  "LotCP-S" was added (score divided by a lot scale built from the shrunk variance of the m
  reference residuals and from the label-free variance of repeated-scan predictions). The
  design of the scale estimate was developed on source-season out-of-fold residuals only
  (seasons <= 2018 of the 2019 configuration). Both the pre-specified LotCP and LotCP-S are
  reported for all seasons and models; 2018/PLS must be read as development data for D1.
* D2. Added baseline `target_only_centred` (bias-corrected target-only conformal with
  leave-one-sample-out centring) as a stronger target-only competitor.
* D3 (compute budget, decided before any CNN result existed). CNN epochs 30 -> 20; lot-grouped
  folds are computed for CNN seed 0 only; in the leave-one-season-out protocol the CNN (seed 0)
  uses season-grouped folds only. The machine is a 4-core CPU without GPU.
* D4 (after the full evaluation). Ablation variant `lotcp_s_lotfold` (LotCP-S calibrated on
  lot-fold instead of season-fold residuals) was added because the location-only ablation
  showed that the fold unit matters much less once m > 0. It is reported as an ablation only;
  the designated method (LotCP-S on season-fold residuals) was not changed.
