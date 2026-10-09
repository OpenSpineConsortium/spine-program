# Pooled fit: accuracy ~ f(N) against f(N) + g H* (generated 2026-09-25 10:03)

Nested comparison over every (training set, accuracy) pair with a known N and a known H*_lat: the film N-curve cells (H* = 0 by protocol), the C-ArmLSpine naming cells (H* fixed per protocol), the same-device detection cells (H* from the census) and the matched-N render arms (H* varies at fixed N). M0: acc = A_c - B_c N^-C per corpus with one exponent; M1 adds one shared g H*_lat. One Gaussian likelihood weighted by each point's interval; AICc; likelihood-ratio test (1 df). Points: 99 (arm_surgio_b51_dr 6, carm_det_AP 16, carm_det_LAT 16, carm_name_AP 11, carm_name_LAT 11, film_buu_full 13, film_csxa 13, film_nhanes 13).

**Verdict:** N plus coverage: g's interval excludes 0 and AICc prefers M1 by >= 2; g identified only by within-corpus H* spread in ['arm_surgio_b51_dr']

## Which points identify g

| corpus | points | within-corpus H* spread | identifies g |
|---|---:|---:|---|
| arm_surgio_b51_dr | 6 | 0.7537 | yes |
| carm_det_AP | 16 | 0.0139 | no |
| carm_det_LAT | 16 | 0.0139 | no |
| carm_name_AP | 11 | 0.0000 | no |
| carm_name_LAT | 11 | 0.0000 | no |
| film_buu_full | 13 | 0.0000 | no |
| film_csxa | 13 | 0.0000 | no |
| film_nhanes | 13 | 0.0000 | no |

## M0 (N only)

exponent C = 0.274; weighted RSS 137.857; AICc 77.3; RMSE 3.20 points

| corpus | A_c (asymptote) | SE | B_c | N range | points |
|---|---:|---:|---:|---|---:|
| arm_surgio_b51_dr | 71.5 % | 18.5 | 0.315 | 2646-5290 | 6 |
| carm_det_AP | 90.7 % | 3.1 | 0.199 | 4-200 | 16 |
| carm_det_LAT | 88.6 % | 3.7 | 0.215 | 4-200 | 16 |
| carm_name_AP | 100.0 % | 3.2 | 0.114 | 5-87.6 | 11 |
| carm_name_LAT | 99.2 % | 2.6 | 0.043 | 5-87 | 11 |
| film_buu_full | 100.0 % | 4.8 | 0.554 | 5-2967 | 13 |
| film_csxa | 100.0 % | 1.8 | 0.101 | 5-4114 | 13 |
| film_nhanes | 100.0 % | 3.6 | 0.325 | 5-264 | 13 |

## M1 (N plus coverage)

g = +24.21 points per unit H*_lat (SE 4.35; 95 % +15.69 to +32.74); exponent C = 0.273; AICc 45.3
dAICc(M0 - M1) = +32.01; LR = 35.08, p = 3.17e-09 (known-variance form: 41.13, p = 1.42e-10)

## Admissibility

| film corpus | asymptote | acc(all) - asymptote | plateau inside the grid |
|---|---:|---:|---|
| nhanes | 95.9 % | -3.22 pp | no |
| buu_full | 100.0 % | -3.08 pp | no |
| csxa | 100.0 % | -0.24 pp | yes |

## Film N-curve summary (from film_ncurve.json)

| corpus | N = 5 | N = 25 | N = all (persons) | fitted asymptote | first grid N within 2 pt | best transfer to |
|---|---:|---:|---:|---:|---:|---|
| nhanes | 77.8 | 87.8 | 92.7 (264) | 95.9 % | not reached on the grid | buu_full 73.2 % at N = all s0; csxa 74.3 % at N = 200 s0 |
| buu_full | 65.0 | 76.7 | 96.9 (2967) | 100.0 % | not reached on the grid | nhanes 59.8 % at N = 5 s0; csxa 13.4 % at N = 10 s2 |
| csxa | 94.2 | 96.4 | 99.8 (4114) | 100.0 % | 200 | nhanes 43.7 % at N = all s0; buu_full 17.9 % at N = 25 s2 |

## Matched-N render arms (unseen sweep, own card, conf 0.25; status: PARTIAL: 6 of 12 arms enter the fit (6 below val mAP50 0.3))

Recall = n-weighted over every (tilt, lat) bin of the unseen sweep; near-AP = tilt 0, |lat| <= 10 deg; oblique = tilt 0, 20-70 deg; case134 = pooled body recall on the real 301-frame spin at the same conf; real own test = vertebra recall on the device's own real test split at conf 0.25 (render-only arm; never trained on a real frame). val mAP50 = the arm's own final-epoch validation (results.csv): whether it trained.

| device | arm | seed | N | H*_lat | val mAP50 | unseen recall | near-AP | oblique | case134 | real own test | in fit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| elekta_xvi | low | 0 | 1972 | 0.619 | 0.16 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | no (untrained) |
| elekta_xvi | low | 1 | 1972 | 0.619 | 0.18 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | no (untrained) |
| elekta_xvi | high | 0 | 1972 | 0.998 | 0.13 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | no (untrained) |
| elekta_xvi | high | 1 | 1972 | 0.998 | 0.14 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | no (untrained) |
| elekta_xvi | low2n | 0 | 3944 | 0.619 | 0.22 | 0.9 | 1.1 | 0.8 | 0.0 | 1.6 | no (untrained) |
| elekta_xvi | low2n | 1 | 3944 | 0.619 | 0.22 | 0.9 | 3.8 | 1.7 | 3.3 | 0.4 | no (untrained) |
| surgio_b51_dr | low | 0 | 2646 | 0.240 | 0.61 | 55.3 | 76.9 | 38.7 | 7.8 | 4.9 | yes |
| surgio_b51_dr | low | 1 | 2646 | 0.240 | 0.62 | 61.0 | 80.1 | 49.7 | 7.0 | 9.1 | yes |
| surgio_b51_dr | high | 0 | 2646 | 0.993 | 0.67 | 78.9 | 72.2 | 77.8 | 11.0 | 0.7 | yes |
| surgio_b51_dr | high | 1 | 2646 | 0.993 | 0.58 | 76.1 | 70.0 | 75.8 | 10.6 | 1.0 | yes |
| surgio_b51_dr | low2n | 0 | 5290 | 0.240 | 0.78 | 68.6 | 87.4 | 56.4 | 4.2 | 1.4 | yes |
| surgio_b51_dr | low2n | 1 | 5290 | 0.240 | 0.80 | 68.3 | 86.2 | 56.1 | 8.1 | 2.4 | yes |

Matched contrasts (arm minus low, points of recall):

| device | seed | contrast | N low -> arm | H* low -> arm | unseen | oblique | case134 low -> arm | real own low -> arm |
|---|---:|---|---|---|---:|---:|---|---|
| elekta_xvi | 0 | high (arc poses) vs low at matched N | 1972 -> 1972 | 0.62 -> 1.00 | +0.0 | +0.0 | 0.0 -> 0.0 | 0.0 -> 0.0 |
| elekta_xvi | 1 | high (arc poses) vs low at matched N | 1972 -> 1972 | 0.62 -> 1.00 | +0.0 | +0.0 | 0.0 -> 0.0 | 0.0 -> 0.0 |
| elekta_xvi | 0 | 2N same bins vs N | 1972 -> 3944 | 0.62 -> 0.62 | +0.9 | +0.8 | 0.0 -> 0.0 | 0.0 -> 1.6 |
| elekta_xvi | 1 | 2N same bins vs N | 1972 -> 3944 | 0.62 -> 0.62 | +0.9 | +1.7 | 0.0 -> 3.3 | 0.0 -> 0.4 |
| surgio_b51_dr | 0 | high (arc poses) vs low at matched N | 2646 -> 2646 | 0.24 -> 0.99 | +23.6 | +39.1 | 7.8 -> 11.0 | 4.9 -> 0.7 |
| surgio_b51_dr | 1 | high (arc poses) vs low at matched N | 2646 -> 2646 | 0.24 -> 0.99 | +15.1 | +26.0 | 7.0 -> 10.6 | 9.1 -> 1.0 |
| surgio_b51_dr | 0 | 2N same bins vs N | 2646 -> 5290 | 0.24 -> 0.24 | +13.3 | +17.7 | 7.8 -> 4.2 | 4.9 -> 1.4 |
| surgio_b51_dr | 1 | 2N same bins vs N | 2646 -> 5290 | 0.24 -> 0.24 | +7.3 | +6.3 | 7.0 -> 8.1 | 9.1 -> 2.4 |

Seed spread of the own-card unseen recall (max - min, points): elekta_xvi/high 0.0, elekta_xvi/low2n 0.0, elekta_xvi/low 0.0, surgio_b51_dr/high 2.8, surgio_b51_dr/low2n 0.3, surgio_b51_dr/low 5.7

Excluded as untrained (val mAP50 below the sensitivity floor): cov_elekta_xvi_high_s0, cov_elekta_xvi_high_s1, cov_elekta_xvi_low2n_s0, cov_elekta_xvi_low2n_s1, cov_elekta_xvi_low_s0, cov_elekta_xvi_low_s1
