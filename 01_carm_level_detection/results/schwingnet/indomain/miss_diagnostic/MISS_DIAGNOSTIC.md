# Per-vertebra miss diagnostic, C-ArmLSpine test split (2026-09-25 14:33)

287 truth vertebrae in 56 frames ({'AP': 143, 'LAT': 138, 'OBL': 6}); 45 detector dumps re-matched with tools/lcurve_score.load unchanged. Self-check against det_fill.json: 135 of 135 cell x view recalls reproduced to 0.1 pp.

## 1. Is it the same vertebrae every time? (both-view arms N >= 24, body rule, conf 0.74)

- ALL: never hit 30, sometimes 49, always 208
- AP: never hit 12, sometimes 21, always 110
- LAT: never hit 17, sometimes 27, always 94
- OBL: never hit 1, sometimes 1, always 4

- misses per arm: {'N24_s0': 44, 'N24_s1': 45, 'N24_s2': 49, 'N50_s0': 49, 'N50_s1': 55, 'N50_s2': 47, 'N100_s0': 48, 'N100_s1': 52, 'N200_s0': 53, 'N200_s1': 47}
- missed by EVERY core arm: 30; by ANY: 79; Jaccard of the miss sets over all arms 0.38, pairwise median 0.705; if misses were independent across arms, 0.0 vertebrae would be missed by all.

## 2. Why the never-hit vertebrae are missed

- 15: found by centre rule at 0.25 in >= half the core arms (localisation / convention / confidence)
- 10: found under some rule at 0.25 in some core arm
- 5: not found under any rule at 0.25 by any core arm (invisible or mis-projected truth)

## 3. Miss rate by stratum

Columns: vertebrae in the stratum; misses / trials over vertebra x arm (pooled over the arms), % with a Wilson interval (arms are not independent, so it is too narrow); share of the stratum's vertebrae never hit by any arm.

### both-view arms N >= 24, body rule, conf 0.74 (the reported convention)

**view**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| AP | 143 | 221 / 1430 | 15.5 [13.7, 17.4] | 8.4 |
| LAT | 138 | 249 / 1380 | 18.0 [16.1, 20.2] | 12.3 |
| OBL | 6 | 19 / 60 | 31.7 [21.3, 44.2] | 16.7 |

**visible_frac**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| 0.95-1 | 36 | 154 / 360 | 42.8 [37.8, 47.9] | 22.2 |
| 1.0 | 233 | 211 / 2330 | 9.1 [8.0, 10.3] | 5.6 |
| <0.8 | 7 | 38 / 70 | 54.3 [42.7, 65.4] | 28.6 |
| 0.8-0.95 | 11 | 86 / 110 | 78.2 [69.6, 84.9] | 63.6 |

**complete (not cut by the CBCT)**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| incomplete | 66 | 340 / 660 | 51.5 [47.7, 55.3] | 34.8 |
| complete | 221 | 149 / 2210 | 6.7 [5.8, 7.9] | 3.2 |

**box_source**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| spineps_corpus | 281 | 429 / 2810 | 15.3 [14.0, 16.6] | 8.5 |
| whole_vertebra | 6 | 60 / 60 | 100.0 [94.0, 100.0] | 100.0 |

**level**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| L1 | 42 | 200 / 420 | 47.6 [42.9, 52.4] | 28.6 |
| L2 | 54 | 40 / 540 | 7.4 [5.5, 9.9] | 5.6 |
| L3 | 54 | 9 / 540 | 1.7 [0.9, 3.1] | 0.0 |
| L4 | 54 | 12 / 540 | 2.2 [1.3, 3.8] | 0.0 |
| L5 | 50 | 28 / 500 | 5.6 [3.9, 8.0] | 0.0 |
| disagree:T12/L1 | 6 | 31 / 60 | 51.7 [39.3, 63.8] | 33.3 |
| T12 | 4 | 39 / 40 | 97.5 [87.1, 99.6] | 75.0 |
| disagree:L5/sacrum | 2 | 20 / 20 | 100.0 [83.9, 100.0] | 100.0 |
| disagree:L5/L4 | 2 | 16 / 20 | 80.0 [58.4, 91.9] | 50.0 |
| disagree:T12/L2 | 2 | 15 / 20 | 75.0 [53.1, 88.8] | 50.0 |
| disagree:L1/L2 | 7 | 39 / 70 | 55.7 [44.1, 66.8] | 42.9 |
| disagree:L2/L3 | 2 | 1 / 20 | 5.0 [0.9, 23.6] | 0.0 |
| disagree:L3/L4 | 2 | 0 / 20 | 0.0 [0.0, 16.1] | 0.0 |
| disagree:L4/L5 | 2 | 0 / 20 | 0.0 [0.0, 16.1] | 0.0 |
| disagree:L5/L6 | 2 | 19 / 20 | 95.0 [76.4, 99.1] | 50.0 |
| disagree:L1/sacrum | 2 | 20 / 20 | 100.0 [83.9, 100.0] | 100.0 |

**level agreed**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| agreed | 258 | 328 / 2580 | 12.7 [11.5, 14.1] | 7.0 |
| disagree | 29 | 161 / 290 | 55.5 [49.8, 61.1] | 41.4 |

**distance to panel edge**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| <=40 px | 51 | 214 / 510 | 42.0 [37.8, 46.3] | 25.5 |
| >40 px | 216 | 119 / 2160 | 5.5 [4.6, 6.6] | 2.3 |
| <=2 px (cut) | 20 | 156 / 200 | 78.0 [71.8, 83.2] | 60.0 |

**edge_ncc (frame registration), AP tertiles 0.322 / 0.384**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 52 | 94 / 520 | 18.1 [15.0, 21.6] | 5.8 |
| mid | 46 | 51 / 460 | 11.1 [8.5, 14.3] | 10.9 |
| high | 45 | 76 / 450 | 16.9 [13.7, 20.6] | 8.9 |

**edge_ncc (frame registration), LAT tertiles 0.176 / 0.235**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| mid | 47 | 99 / 470 | 21.1 [17.6, 25.0] | 17.0 |
| high | 41 | 49 / 410 | 12.0 [9.2, 15.4] | 4.9 |
| low | 50 | 101 / 500 | 20.2 [16.9, 23.9] | 14.0 |

**body height, px, AP tertiles 121 / 134**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 152 / 480 | 31.7 [27.7, 36.0] | 20.8 |
| mid | 47 | 31 / 470 | 6.6 [4.7, 9.2] | 2.1 |
| high | 48 | 38 / 480 | 7.9 [5.8, 10.7] | 2.1 |

**body height, px, LAT tertiles 124 / 134**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 46 | 151 / 460 | 32.8 [28.7, 37.2] | 23.9 |
| mid | 47 | 42 / 470 | 8.9 [6.7, 11.9] | 6.4 |
| high | 45 | 56 / 450 | 12.4 [9.7, 15.8] | 6.7 |

**centre y (0 top .. 1 bottom), AP tertiles 0.163 / 0.477**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 183 / 480 | 38.1 [33.9, 42.5] | 22.9 |
| mid | 47 | 0 / 470 | 0.0 [0.0, 0.8] | 0.0 |
| high | 48 | 38 / 480 | 7.9 [5.8, 10.7] | 2.1 |

**centre y (0 top .. 1 bottom), LAT tertiles 0.155 / 0.467**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 46 | 187 / 460 | 40.7 [36.3, 45.2] | 30.4 |
| mid | 46 | 15 / 460 | 3.3 [2.0, 5.3] | 0.0 |
| high | 46 | 47 / 460 | 10.2 [7.8, 13.3] | 6.5 |

**body/outline area ratio, AP tertiles 0.518 / 0.588**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 131 / 480 | 27.3 [23.5, 31.4] | 14.6 |
| mid | 47 | 17 / 470 | 3.6 [2.3, 5.7] | 0.0 |
| high | 48 | 73 / 480 | 15.2 [12.3, 18.7] | 10.4 |

**body/outline area ratio, LAT tertiles 0.323 / 0.378**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 47 | 122 / 470 | 26.0 [22.2, 30.1] | 17.0 |
| mid | 45 | 38 / 450 | 8.4 [6.2, 11.4] | 4.4 |
| high | 46 | 89 / 460 | 19.3 [16.0, 23.2] | 15.2 |

**body-outline IoU, AP tertiles 0.508 / 0.577**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 150 / 480 | 31.2 [27.3, 35.5] | 16.7 |
| mid | 47 | 21 / 470 | 4.5 [2.9, 6.7] | 0.0 |
| high | 48 | 50 / 480 | 10.4 [8.0, 13.5] | 8.3 |

**body-outline IoU, LAT tertiles 0.308 / 0.355**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 47 | 161 / 470 | 34.3 [30.1, 38.7] | 25.5 |
| mid | 45 | 30 / 450 | 6.7 [4.7, 9.4] | 2.2 |
| high | 46 | 58 / 460 | 12.6 [9.9, 16.0] | 8.7 |

### both-view arms N >= 24, centre rule, conf 0.25 (convention-free, default threshold)

**view**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| AP | 143 | 110 / 1430 | 7.7 [6.4, 9.2] | 4.2 |
| LAT | 138 | 132 / 1380 | 9.6 [8.1, 11.2] | 5.8 |
| OBL | 6 | 10 / 60 | 16.7 [9.3, 28.0] | 16.7 |

**visible_frac**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| 0.95-1 | 36 | 51 / 360 | 14.2 [10.9, 18.1] | 5.6 |
| 1.0 | 233 | 111 / 2330 | 4.8 [4.0, 5.7] | 3.4 |
| <0.8 | 7 | 59 / 70 | 84.3 [74.0, 91.0] | 71.4 |
| 0.8-0.95 | 11 | 31 / 110 | 28.2 [20.6, 37.2] | 0.0 |

**complete (not cut by the CBCT)**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| incomplete | 66 | 166 / 660 | 25.2 [22.0, 28.6] | 12.1 |
| complete | 221 | 86 / 2210 | 3.9 [3.2, 4.8] | 3.2 |

**box_source**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| spineps_corpus | 281 | 207 / 2810 | 7.4 [6.5, 8.4] | 5.3 |
| whole_vertebra | 6 | 45 / 60 | 75.0 [62.8, 84.2] | 0.0 |

**level**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| L1 | 42 | 43 / 420 | 10.2 [7.7, 13.5] | 2.4 |
| L2 | 54 | 6 / 540 | 1.1 [0.5, 2.4] | 0.0 |
| L3 | 54 | 0 / 540 | 0.0 [0.0, 0.7] | 0.0 |
| L4 | 54 | 0 / 540 | 0.0 [0.0, 0.7] | 0.0 |
| L5 | 50 | 3 / 500 | 0.6 [0.2, 1.7] | 0.0 |
| disagree:T12/L1 | 6 | 60 / 60 | 100.0 [94.0, 100.0] | 100.0 |
| T12 | 4 | 24 / 40 | 60.0 [44.6, 73.7] | 25.0 |
| disagree:L5/sacrum | 2 | 10 / 20 | 50.0 [29.9, 70.1] | 0.0 |
| disagree:L5/L4 | 2 | 20 / 20 | 100.0 [83.9, 100.0] | 100.0 |
| disagree:T12/L2 | 2 | 20 / 20 | 100.0 [83.9, 100.0] | 100.0 |
| disagree:L1/L2 | 7 | 48 / 70 | 68.6 [57.0, 78.2] | 42.9 |
| disagree:L2/L3 | 2 | 0 / 20 | 0.0 [0.0, 16.1] | 0.0 |
| disagree:L3/L4 | 2 | 0 / 20 | 0.0 [0.0, 16.1] | 0.0 |
| disagree:L4/L5 | 2 | 0 / 20 | 0.0 [0.0, 16.1] | 0.0 |
| disagree:L5/L6 | 2 | 1 / 20 | 5.0 [0.9, 23.6] | 0.0 |
| disagree:L1/sacrum | 2 | 17 / 20 | 85.0 [64.0, 94.8] | 0.0 |

**level agreed**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| agreed | 258 | 76 / 2580 | 2.9 [2.4, 3.7] | 0.8 |
| disagree | 29 | 176 / 290 | 60.7 [55.0, 66.1] | 44.8 |

**distance to panel edge**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| <=40 px | 51 | 151 / 510 | 29.6 [25.8, 33.7] | 23.5 |
| >40 px | 216 | 36 / 2160 | 1.7 [1.2, 2.3] | 0.9 |
| <=2 px (cut) | 20 | 65 / 200 | 32.5 [26.4, 39.3] | 5.0 |

**edge_ncc (frame registration), AP tertiles 0.322 / 0.384**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 52 | 55 / 520 | 10.6 [8.2, 13.5] | 9.6 |
| mid | 46 | 33 / 460 | 7.2 [5.2, 9.9] | 2.2 |
| high | 45 | 22 / 450 | 4.9 [3.3, 7.3] | 0.0 |

**edge_ncc (frame registration), LAT tertiles 0.176 / 0.235**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| mid | 47 | 51 / 470 | 10.9 [8.4, 14.0] | 4.3 |
| high | 41 | 27 / 410 | 6.6 [4.6, 9.4] | 2.4 |
| low | 50 | 54 / 500 | 10.8 [8.4, 13.8] | 10.0 |

**body height, px, AP tertiles 121 / 134**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 65 / 480 | 13.5 [10.8, 16.9] | 4.2 |
| mid | 47 | 30 / 470 | 6.4 [4.5, 9.0] | 6.4 |
| high | 48 | 15 / 480 | 3.1 [1.9, 5.1] | 2.1 |

**body height, px, LAT tertiles 124 / 134**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 46 | 81 / 460 | 17.6 [14.4, 21.4] | 8.7 |
| mid | 47 | 22 / 470 | 4.7 [3.1, 7.0] | 4.3 |
| high | 45 | 29 / 450 | 6.4 [4.5, 9.1] | 4.4 |

**centre y (0 top .. 1 bottom), AP tertiles 0.163 / 0.477**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 95 / 480 | 19.8 [16.5, 23.6] | 10.4 |
| mid | 47 | 0 / 470 | 0.0 [0.0, 0.8] | 0.0 |
| high | 48 | 15 / 480 | 3.1 [1.9, 5.1] | 2.1 |

**centre y (0 top .. 1 bottom), LAT tertiles 0.155 / 0.467**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 46 | 113 / 460 | 24.6 [20.9, 28.7] | 15.2 |
| mid | 46 | 0 / 460 | 0.0 [0.0, 0.8] | 0.0 |
| high | 46 | 19 / 460 | 4.1 [2.7, 6.4] | 2.2 |

**body/outline area ratio, AP tertiles 0.518 / 0.588**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 40 / 480 | 8.3 [6.2, 11.1] | 2.1 |
| mid | 47 | 0 / 470 | 0.0 [0.0, 0.8] | 0.0 |
| high | 48 | 70 / 480 | 14.6 [11.7, 18.0] | 10.4 |

**body/outline area ratio, LAT tertiles 0.323 / 0.378**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 47 | 36 / 470 | 7.7 [5.6, 10.4] | 2.1 |
| mid | 45 | 10 / 450 | 2.2 [1.2, 4.0] | 2.2 |
| high | 46 | 86 / 460 | 18.7 [15.4, 22.5] | 13.0 |

**body-outline IoU, AP tertiles 0.508 / 0.577**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 89 / 480 | 18.5 [15.3, 22.3] | 12.5 |
| mid | 47 | 1 / 470 | 0.2 [0.0, 1.2] | 0.0 |
| high | 48 | 20 / 480 | 4.2 [2.7, 6.3] | 0.0 |

**body-outline IoU, LAT tertiles 0.308 / 0.355**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 47 | 106 / 470 | 22.6 [19.0, 26.5] | 17.0 |
| mid | 45 | 0 / 450 | 0.0 [0.0, 0.8] | 0.0 |
| high | 46 | 26 / 460 | 5.7 [3.9, 8.2] | 0.0 |

### both-view arms N >= 24, whole-vertebra outline rule, conf 0.74

**view**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| AP | 143 | 305 / 1430 | 21.3 [19.3, 23.5] | 18.2 |
| LAT | 138 | 1348 / 1380 | 97.7 [96.7, 98.4] | 92.8 |
| OBL | 6 | 50 / 60 | 83.3 [72.0, 90.7] | 83.3 |

**visible_frac**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| 0.95-1 | 36 | 252 / 360 | 70.0 [65.1, 74.5] | 66.7 |
| 1.0 | 233 | 1290 / 2330 | 55.4 [53.3, 57.4] | 51.1 |
| <0.8 | 7 | 60 / 70 | 85.7 [75.7, 92.1] | 85.7 |
| 0.8-0.95 | 11 | 101 / 110 | 91.8 [85.2, 95.6] | 90.9 |

**complete (not cut by the CBCT)**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| incomplete | 66 | 532 / 660 | 80.6 [77.4, 83.4] | 77.3 |
| complete | 221 | 1171 / 2210 | 53.0 [50.9, 55.1] | 48.9 |

**box_source**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| spineps_corpus | 281 | 1643 / 2810 | 58.5 [56.6, 60.3] | 54.4 |
| whole_vertebra | 6 | 60 / 60 | 100.0 [94.0, 100.0] | 100.0 |

**level**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| L1 | 42 | 341 / 420 | 81.2 [77.2, 84.6] | 76.2 |
| L2 | 54 | 269 / 540 | 49.8 [45.6, 54.0] | 48.1 |
| L3 | 54 | 303 / 540 | 56.1 [51.9, 60.2] | 53.7 |
| L4 | 54 | 268 / 540 | 49.6 [45.4, 53.8] | 46.3 |
| L5 | 50 | 240 / 500 | 48.0 [43.7, 52.4] | 40.0 |
| disagree:T12/L1 | 6 | 60 / 60 | 100.0 [94.0, 100.0] | 100.0 |
| T12 | 4 | 40 / 40 | 100.0 [91.2, 100.0] | 100.0 |
| disagree:L5/sacrum | 2 | 20 / 20 | 100.0 [83.9, 100.0] | 100.0 |
| disagree:L5/L4 | 2 | 20 / 20 | 100.0 [83.9, 100.0] | 100.0 |
| disagree:T12/L2 | 2 | 20 / 20 | 100.0 [83.9, 100.0] | 100.0 |
| disagree:L1/L2 | 7 | 60 / 70 | 85.7 [75.7, 92.1] | 85.7 |
| disagree:L2/L3 | 2 | 10 / 20 | 50.0 [29.9, 70.1] | 50.0 |
| disagree:L3/L4 | 2 | 10 / 20 | 50.0 [29.9, 70.1] | 50.0 |
| disagree:L4/L5 | 2 | 10 / 20 | 50.0 [29.9, 70.1] | 50.0 |
| disagree:L5/L6 | 2 | 12 / 20 | 60.0 [38.7, 78.1] | 0.0 |
| disagree:L1/sacrum | 2 | 20 / 20 | 100.0 [83.9, 100.0] | 100.0 |

**level agreed**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| agreed | 258 | 1461 / 2580 | 56.6 [54.7, 58.5] | 52.7 |
| disagree | 29 | 242 / 290 | 83.4 [78.7, 87.3] | 79.3 |

**distance to panel edge**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| <=40 px | 51 | 391 / 510 | 76.7 [72.8, 80.1] | 72.5 |
| >40 px | 216 | 1121 / 2160 | 51.9 [49.8, 54.0] | 47.7 |
| <=2 px (cut) | 20 | 191 / 200 | 95.5 [91.7, 97.6] | 95.0 |

**edge_ncc (frame registration), AP tertiles 0.322 / 0.384**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 52 | 144 / 520 | 27.7 [24.0, 31.7] | 23.1 |
| mid | 46 | 62 / 460 | 13.5 [10.7, 16.9] | 13.0 |
| high | 45 | 99 / 450 | 22.0 [18.4, 26.1] | 17.8 |

**edge_ncc (frame registration), LAT tertiles 0.176 / 0.235**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| mid | 47 | 465 / 470 | 98.9 [97.5, 99.5] | 95.7 |
| high | 41 | 400 / 410 | 97.6 [95.6, 98.7] | 95.1 |
| low | 50 | 483 / 500 | 96.6 [94.6, 97.9] | 88.0 |

**body height, px, AP tertiles 121 / 134**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 193 / 480 | 40.2 [35.9, 44.7] | 37.5 |
| mid | 47 | 56 / 470 | 11.9 [9.3, 15.2] | 10.6 |
| high | 48 | 56 / 480 | 11.7 [9.1, 14.8] | 6.2 |

**body height, px, LAT tertiles 124 / 134**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 46 | 452 / 460 | 98.3 [96.6, 99.1] | 93.5 |
| mid | 47 | 468 / 470 | 99.6 [98.5, 99.9] | 97.9 |
| high | 45 | 428 / 450 | 95.1 [92.7, 96.7] | 86.7 |

**centre y (0 top .. 1 bottom), AP tertiles 0.163 / 0.477**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 224 / 480 | 46.7 [42.2, 51.1] | 43.8 |
| mid | 47 | 35 / 470 | 7.4 [5.4, 10.2] | 6.4 |
| high | 48 | 46 / 480 | 9.6 [7.3, 12.5] | 4.2 |

**centre y (0 top .. 1 bottom), LAT tertiles 0.155 / 0.467**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 46 | 458 / 460 | 99.6 [98.4, 99.9] | 97.8 |
| mid | 46 | 456 / 460 | 99.1 [97.8, 99.7] | 95.7 |
| high | 46 | 434 / 460 | 94.3 [91.8, 96.1] | 84.8 |

**body/outline area ratio, AP tertiles 0.518 / 0.588**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 214 / 480 | 44.6 [40.2, 49.1] | 37.5 |
| mid | 47 | 10 / 470 | 2.1 [1.2, 3.9] | 0.0 |
| high | 48 | 81 / 480 | 16.9 [13.8, 20.5] | 16.7 |

**body/outline area ratio, LAT tertiles 0.323 / 0.378**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 47 | 466 / 470 | 99.1 [97.8, 99.7] | 95.7 |
| mid | 45 | 447 / 450 | 99.3 [98.1, 99.8] | 95.6 |
| high | 46 | 435 / 460 | 94.6 [92.1, 96.3] | 87.0 |

**body-outline IoU, AP tertiles 0.508 / 0.577**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 255 / 480 | 53.1 [48.7, 57.5] | 47.9 |
| mid | 47 | 19 / 470 | 4.0 [2.6, 6.2] | 0.0 |
| high | 48 | 31 / 480 | 6.5 [4.6, 9.0] | 6.2 |

**body-outline IoU, LAT tertiles 0.308 / 0.355**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 47 | 466 / 470 | 99.1 [97.8, 99.7] | 95.7 |
| mid | 45 | 448 / 450 | 99.6 [98.4, 99.9] | 97.8 |
| high | 46 | 434 / 460 | 94.3 [91.8, 96.1] | 84.8 |

### N = 0 arms (no frame of the device), centre rule, conf 0.25

**view**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| AP | 143 | 36 / 429 | 8.4 [6.1, 11.4] | 5.6 |
| LAT | 138 | 51 / 414 | 12.3 [9.5, 15.8] | 8.0 |
| OBL | 6 | 2 / 18 | 11.1 [3.1, 32.8] | 0.0 |

**visible_frac**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| 0.95-1 | 36 | 23 / 108 | 21.3 [14.6, 29.9] | 13.9 |
| 1.0 | 233 | 40 / 699 | 5.7 [4.2, 7.7] | 3.4 |
| <0.8 | 7 | 14 / 21 | 66.7 [45.4, 82.8] | 57.1 |
| 0.8-0.95 | 11 | 12 / 33 | 36.4 [22.2, 53.4] | 18.2 |

**complete (not cut by the CBCT)**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| incomplete | 66 | 56 / 198 | 28.3 [22.5, 34.9] | 18.2 |
| complete | 221 | 33 / 663 | 5.0 [3.6, 6.9] | 3.2 |

**box_source**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| spineps_corpus | 281 | 83 / 843 | 9.8 [8.0, 12.0] | 6.0 |
| whole_vertebra | 6 | 6 / 18 | 33.3 [16.3, 56.3] | 33.3 |

**level**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| L1 | 42 | 23 / 126 | 18.3 [12.5, 25.9] | 7.1 |
| L2 | 54 | 6 / 162 | 3.7 [1.7, 7.8] | 1.9 |
| L3 | 54 | 3 / 162 | 1.9 [0.6, 5.3] | 0.0 |
| L4 | 54 | 2 / 162 | 1.2 [0.3, 4.4] | 0.0 |
| L5 | 50 | 5 / 150 | 3.3 [1.4, 7.6] | 2.0 |
| disagree:T12/L1 | 6 | 18 / 18 | 100.0 [82.4, 100.0] | 100.0 |
| T12 | 4 | 6 / 12 | 50.0 [25.4, 74.6] | 0.0 |
| disagree:L5/sacrum | 2 | 0 / 6 | 0.0 [0.0, 39.0] | 0.0 |
| disagree:L5/L4 | 2 | 5 / 6 | 83.3 [43.6, 97.0] | 50.0 |
| disagree:T12/L2 | 2 | 6 / 6 | 100.0 [61.0, 100.0] | 100.0 |
| disagree:L1/L2 | 7 | 12 / 21 | 57.1 [36.5, 75.5] | 57.1 |
| disagree:L2/L3 | 2 | 0 / 6 | 0.0 [0.0, 39.0] | 0.0 |
| disagree:L3/L4 | 2 | 0 / 6 | 0.0 [0.0, 39.0] | 0.0 |
| disagree:L4/L5 | 2 | 0 / 6 | 0.0 [0.0, 39.0] | 0.0 |
| disagree:L5/L6 | 2 | 0 / 6 | 0.0 [0.0, 39.0] | 0.0 |
| disagree:L1/sacrum | 2 | 3 / 6 | 50.0 [18.8, 81.2] | 50.0 |

**level agreed**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| agreed | 258 | 45 / 774 | 5.8 [4.4, 7.7] | 1.9 |
| disagree | 29 | 44 / 87 | 50.6 [40.3, 60.8] | 48.3 |

**distance to panel edge**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| <=40 px | 51 | 50 / 153 | 32.7 [25.8, 40.5] | 27.5 |
| >40 px | 216 | 18 / 648 | 2.8 [1.8, 4.3] | 0.9 |
| <=2 px (cut) | 20 | 21 / 60 | 35.0 [24.2, 47.6] | 15.0 |

**edge_ncc (frame registration), AP tertiles 0.322 / 0.384**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 52 | 16 / 156 | 10.3 [6.4, 16.0] | 7.7 |
| mid | 46 | 15 / 138 | 10.9 [6.7, 17.2] | 6.5 |
| high | 45 | 5 / 135 | 3.7 [1.6, 8.4] | 2.2 |

**edge_ncc (frame registration), LAT tertiles 0.176 / 0.235**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| mid | 47 | 13 / 141 | 9.2 [5.5, 15.1] | 4.3 |
| high | 41 | 9 / 123 | 7.3 [3.9, 13.3] | 7.3 |
| low | 50 | 29 / 150 | 19.3 [13.8, 26.4] | 12.0 |

**body height, px, AP tertiles 121 / 134**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 21 / 144 | 14.6 [9.7, 21.3] | 10.4 |
| mid | 47 | 10 / 141 | 7.1 [3.9, 12.6] | 4.3 |
| high | 48 | 5 / 144 | 3.5 [1.5, 7.9] | 2.1 |

**body height, px, LAT tertiles 124 / 134**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 46 | 28 / 138 | 20.3 [14.4, 27.8] | 13.0 |
| mid | 47 | 8 / 141 | 5.7 [2.9, 10.8] | 4.3 |
| high | 45 | 15 / 135 | 11.1 [6.9, 17.5] | 6.7 |

**centre y (0 top .. 1 bottom), AP tertiles 0.163 / 0.477**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 30 / 144 | 20.8 [15.0, 28.2] | 16.7 |
| mid | 47 | 3 / 141 | 2.1 [0.7, 6.1] | 0.0 |
| high | 48 | 3 / 144 | 2.1 [0.7, 5.9] | 0.0 |

**centre y (0 top .. 1 bottom), LAT tertiles 0.155 / 0.467**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 46 | 39 / 138 | 28.3 [21.4, 36.3] | 19.6 |
| mid | 46 | 4 / 138 | 2.9 [1.1, 7.2] | 0.0 |
| high | 46 | 8 / 138 | 5.8 [3.0, 11.0] | 4.3 |

**body/outline area ratio, AP tertiles 0.518 / 0.588**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 15 / 144 | 10.4 [6.4, 16.5] | 4.2 |
| mid | 47 | 2 / 141 | 1.4 [0.4, 5.0] | 0.0 |
| high | 48 | 19 / 144 | 13.2 [8.6, 19.7] | 12.5 |

**body/outline area ratio, LAT tertiles 0.323 / 0.378**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 47 | 16 / 141 | 11.3 [7.1, 17.6] | 2.1 |
| mid | 45 | 6 / 135 | 4.4 [2.1, 9.4] | 2.2 |
| high | 46 | 29 / 138 | 21.0 [15.0, 28.6] | 19.6 |

**body-outline IoU, AP tertiles 0.508 / 0.577**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 48 | 30 / 144 | 20.8 [15.0, 28.2] | 14.6 |
| mid | 47 | 2 / 141 | 1.4 [0.4, 5.0] | 0.0 |
| high | 48 | 4 / 144 | 2.8 [1.1, 6.9] | 2.1 |

**body-outline IoU, LAT tertiles 0.308 / 0.355**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| low | 47 | 35 / 141 | 24.8 [18.4, 32.6] | 17.0 |
| mid | 45 | 5 / 135 | 3.7 [1.6, 8.4] | 0.0 |
| high | 46 | 11 / 138 | 8.0 [4.5, 13.7] | 6.5 |

### one-view arms read on their own view, body rule, conf 0.74

**view**

| stratum | vertebrae | misses / trials | miss % [95 %] | never hit, % of vertebrae |
|---|---:|---:|---|---:|
| AP | 143 | 80 / 572 | 14.0 [, ] | 8.4 |
| LAT | 138 | 87 / 552 | 15.8 [, ] | 11.6 |

## 4. The never-hit vertebrae (body rule, conf 0.74, both-view arms N >= 24)

| frame | level (agreed) | source | visible | complete | edge px | NCC | h px | cy | body/outline area | centre@0.25 core | any rule@0.25 core | zero centre@0.25 | N200 s0 body conf | N200 s0 centre conf |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| case10_AP | L1 (y) | spineps_corpus | 0.992 | n | 9.5 | 0.38 | 111.6 | 0.064 | 0.63 | 1.0 | 1.0 | 1.0 |  | 0.89 |
| case114_AP | L1 (y) | spineps_corpus | 0.849 | n | 0.5 | 0.43 | 23.0 | 0.012 | 0.334 | 0.6 | 0.6 | 0.0 | 0.46 | 0.46 |
| case116_LAT | L1 (y) | spineps_corpus | 1.0 | n | 15.4 | 0.16 | 82.8 | 0.055 | 0.286 | 1.0 | 1.0 | 1.0 | 0.69 | 0.69 |
| case118_AP | T12 (y) | spineps_corpus | 0.841 | n | 0.2 | 0.37 | 22.6 | 0.011 | 0.39 | 0.1 | 0.1 | 0.333 | 0.17 | 0.17 |
| case118_OBL | T12 (y) | spineps_corpus | 1.0 | n | 14.7 | 0.16 | 54.0 | 0.041 | 0.316 | 0.0 | 0.0 | 0.333 |  |  |
| case11_AP | L1 (y) | spineps_corpus | 0.866 | n | 0.7 | 0.35 | 22.3 | 0.012 | 0.307 | 0.9 | 0.9 | 1.0 | 0.3 | 0.3 |
| case11_LAT | L1 (y) | spineps_corpus | 0.952 | n | 0.4 | 0.23 | 29.5 | 0.015 | 0.128 | 1.0 | 1.0 | 0.667 | 0.49 | 0.49 |
| case122_LAT | L2 (y) | spineps_corpus | 0.998 | n | 3.3 | 0.12 | 77.7 | 0.041 | 0.241 | 0.6 | 0.6 | 0.0 | 0.67 | 0.67 |
| case132_AP | ? (n) | whole_vertebra | 1.0 | y | 115.5 | 0.40 | 187.2 | 0.796 | 1.0 | 0.8 | 0.8 | 1.0 | 0.63 | 0.63 |
| case132_LAT | T12 (y) | spineps_corpus | 0.951 | n | 0.5 | 0.20 | 35.3 | 0.018 | 0.169 | 0.5 | 0.5 | 0.333 | 0.32 | 0.32 |
| case132_LAT | ? (n) | whole_vertebra | 1.0 | y | 117.7 | 0.20 | 192.8 | 0.791 | 1.0 | 0.2 | 0.2 | 1.0 |  | 0.42 |
| case133_AP | ? (n) | spineps_corpus | 0.998 | y | 34.7 | 0.25 | 127.4 | 0.096 | 2.499 | 0.0 | 0.4 | 0.0 |  |  |
| case133_LAT | ? (n) | spineps_corpus | 1.0 | y | 320.6 | 0.13 | 140.9 | 0.618 | 0.333 | 0.0 | 0.0 | 0.0 |  |  |
| case135_AP | L1 (y) | spineps_corpus | 0.944 | n | 4.6 | 0.31 | 23.4 | 0.016 | 0.306 | 0.7 | 0.7 | 0.667 | 0.5 | 0.5 |
| case135_LAT | L1 (y) | spineps_corpus | 1.0 | n | 17.7 | 0.18 | 22.8 | 0.028 | 0.095 | 0.3 | 0.3 | 0.667 |  | 0.61 |
| case136_LAT | ? (n) | spineps_corpus | 1.0 | n | 23.8 | 0.12 | 126.1 | 0.085 | 2.228 | 0.0 | 0.1 | 0.0 |  |  |
| case136_LAT | ? (n) | spineps_corpus | 1.0 | y | 164.4 | 0.12 | 154.3 | 0.764 | 0.478 | 1.0 | 1.0 | 1.0 | 0.29 | 0.66 |
| case23_AP | ? (n) | whole_vertebra | 0.867 | n | 0.7 | 0.48 | 45.2 | 0.023 | 1.0 | 0.1 | 0.1 | 1.0 | 0.06 | 0.06 |
| case23_LAT | ? (n) | whole_vertebra | 0.974 | n | 3.3 | 0.26 | 61.9 | 0.033 | 1.0 | 0.1 | 0.1 | 0.0 |  | 0.05 |
| case32_AP | L1 (y) | spineps_corpus | 0.883 | n | 0.3 | 0.40 | 14.6 | 0.007 | 0.171 | 0.5 | 0.5 | 0.333 | 0.2 | 0.2 |
| case47_AP | L1 (y) | spineps_corpus | 0.963 | n | 1.0 | 0.38 | 32.0 | 0.017 | 0.35 | 0.6 | 0.6 | 0.0 | 0.44 | 0.44 |
| case47_LAT | L1 (y) | spineps_corpus | 0.62 | n | 0.1 | 0.15 | 17.0 | 0.008 | 0.036 | 0.0 | 0.0 | 0.333 |  | 0.03 |
| case5_LAT | ? (n) | spineps_corpus | 1.0 | y | 18.6 | 0.24 | 122.2 | 0.078 | 9.946 | 0.0 | 0.0 | 0.0 |  |  |
| case60_AP | ? (n) | whole_vertebra | 0.692 | n | 0.5 | 0.36 | 51.5 | 0.026 | 1.0 | 0.1 | 0.1 | 1.0 | 0.14 | 0.14 |
| case60_LAT | ? (n) | whole_vertebra | 1.0 | n | 15.9 | 0.26 | 67.8 | 0.049 | 1.0 | 0.2 | 0.2 | 0.0 |  | 0.18 |
| case6_AP | L1 (y) | spineps_corpus | 0.944 | n | 1.5 | 0.30 | 35.5 | 0.019 | 0.429 | 1.0 | 1.0 | 0.667 | 0.61 | 0.61 |
| case6_LAT | L1 (y) | spineps_corpus | 0.985 | n | 2.0 | 0.18 | 58.3 | 0.03 | 0.212 | 0.2 | 0.2 | 0.333 | 0.01 | 0.15 |
| case6_LAT | L2 (y) | spineps_corpus | 1.0 | y | 71.1 | 0.18 | 134.1 | 0.135 | 0.315 | 0.8 | 0.9 | 1.0 | 0.54 | 0.54 |
| case78_LAT | ? (n) | spineps_corpus | 1.0 | n | 35.5 | 0.16 | 130.5 | 0.098 | 1.748 | 0.0 | 0.0 | 0.0 |  |  |
| case82_LAT | L2 (y) | spineps_corpus | 1.0 | n | 17.5 | 0.18 | 122.8 | 0.077 | 0.336 | 1.0 | 1.0 | 1.0 |  | 0.86 |

## 5. Renders

green = truth body box (SPINEPS corpus, projected); yellow = whole-vertebra outline box; red = predictions of arm N200_s0 at conf >= 0.25 (thick >= 0.74) with confidence written

- /rs/rs_grp_oschome/go2432/data/or_ready/indomain/miss_diagnostic/never_hit_body074_sheet1.png
- /rs/rs_grp_oschome/go2432/data/or_ready/indomain/miss_diagnostic/never_hit_body074_sheet2.png
- /rs/rs_grp_oschome/go2432/data/or_ready/indomain/miss_diagnostic/always_hit_sample.png

LOOK at the sheets before believing any row above; write what they show under this line by hand.

### Renders looked at (2026-09-25 14:45, both never-hit sheets and the always-hit sample)

The 30 never-hit vertebrae are three kinds, and none of them is a clearly visible, complete, well-registered vertebra
that the detectors simply failed to find.

1. **Top-edge slivers (the majority).** L1, or T12, at the very top of the collimated field: the truth body box is a
   strip 15-35 px high sitting on the panel edge (case114_AP, case118_AP, case11_AP, case11_LAT, case135_AP, case32_AP,
   case47_AP, case47_LAT, case6_AP, case6_LAT L1, case23_AP, case60_AP, case132_LAT T12, case135_LAT). The detector
   boxes the vertebra below at 0.8-0.9 and sometimes draws a low-confidence box over the strip; IoU 0.5 with a strip
   is not reachable. These are counted because the box rule keeps a structure with >= 50 % of its projected points in
   the frame, and the CBCT-cut flag marks most of them.
2. **Garbage truth boxes.** The `whole_vertebra` fallback boxes (case132_AP, case132_LAT, case23_AP, case23_LAT,
   case60_AP, case60_LAT: level disagreed, no SPINEPS corpus instance overlapped) and the boxes with body/outline area
   ratios of 1.7-9.9 (case133_AP, case136_LAT, case5_LAT, case78_LAT) are not vertebral bodies at all: one spans the
   whole lumbosacral region, one sits on soft tissue with no bone under it (case133_LAT), several are larger than the
   whole-vertebra outline they should sit inside. They come from the labeller-disagreement cases and from the geometric
   instance lookup falling back.
3. **Registration shift on laterals.** case82_LAT L2, case122_LAT L2, case116_LAT L1, case6_LAT L2 (complete, agreed,
   away from the edge): the green truth box sits half a body above or beside the red box the detector drew on the
   visible body. The frame's edge NCC is 0.12-0.18 (the lowest tertile of the lateral registrations). This is the one
   kind that is a real vertebra the truth mislocates.

The always-hit sample is what a clean case looks like: complete bodies, boxes centred on bone, red and green
coincident at 0.83-0.90. The strata tables agree with the pictures: cut-by-CBCT vertebrae carry most of the misses
(51.5 % missed against 6.7 % for complete ones), bodies within 40 px of the panel edge 42 % against 5.5 % beyond it,
disagreed-level boxes 55.5 % against 12.7 %, and the registration score has no gradient on AP and a weak one on
lateral. One row I could not read from the picture: case10_AP L1 shows a 0.89 box nearly coincident with the truth
yet no body-rule match; the truth is cut (edge 9.5 px) and the greedy match may have given that prediction to the
neighbouring outline, so I leave it in the sliver group with a question mark.

**Recall on clean truth subsets** (plateau arms N >= 24, both views; mean over the ten arms; computed from
miss_diagnostic.json `vertebrae[].core_*_frac`):

| truth subset | n | body rule, conf 0.74 | centre rule, conf 0.25 |
|---|---:|---:|---:|
| all test vertebrae | 287 | 83.0 % | 91.2 % |
| complete (not cut by the CBCT) | 221 | 93.3 % | 96.1 % |
| complete and > 40 px from the panel edge | 216 | 94.5 % | 98.3 % |
| complete, agreed level, SPINEPS body box (= away from the edge) | 204 | 96.9 % | 99.8 % |
| the complement: cut, near the edge, disagreed or fallback box | 83 | 48.7 % | 70.2 % |
| clean subset, anteroposterior only | 102 | 98.7 % | |
| clean subset, lateral only | 97 | 95.8 % | |

Of the 30 never-hit vertebrae, 18 are top-edge slivers (centre within 5 % of the frame top), 6 carry the
whole-vertebra fallback box, 12 have a disagreed level (overlapping groups), and exactly one is complete, agreed and
away from the edge (case6_LAT L2, the registration-shift case). CBCT-cut vertebrae carry 340 of the 489 misses.

**Reading for the question asked** ("is it my pseudolabels or the extra degrees of freedom?"): on this device the
plateau is the denominator and the labels. Recall on complete, agreed, SPINEPS-boxed vertebrae is 96.9 % under the
reported rule (98.7 % anteroposterior, 95.8 % lateral), against 83.0 % on everything. The
extra degrees of freedom (view, angle) cost transfer to cells never trained on (Figure 5 b-d), not the within-cell
ceiling. The remaining real failures are lateral frames whose 2-D/3-D registration is poor, which is a truth-quality
problem too, not a detector one.

## Rules

- matching: tools/lcurve_score.load unchanged: greedy one-to-one by confidence; body IoU >= 0.5 with the SPINEPS body box; outline IoU >= 0.5 with the whole-vertebra box; centre = mutual centre containment; hit at op = matched confidence >= op
- intervals: Wilson on vertebra x arm trials (arms of one vertebra are not independent; the interval is narrower than the truth); the per-vertebra 'never hit' share carries no interval
- truth: C-ArmLSpine truth as rebuilt 2026-09-23 (realxray/carmlspine/meta); boxes kept when >= 50 % of projected points fall in the frame; 'complete' = not cut by the CBCT boundary
