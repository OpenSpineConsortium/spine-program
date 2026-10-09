# C-ArmLSpine detection denominator repair (2026-09-25 14:49)

Rule: keep a truth vertebra iff complete (not cut by the CBCT) and not a whole-vertebra fallback box and visible_frac >= 0.8 and body area <= outline area. Label agreement is not a criterion. Sacrum boxes untouched.

Released denominator 287 -> repaired 214 (dropped 73: body_larger_than_outline 11, cut_by_cbct 66, fallback_box 6, visible_lt_0.8 7; reasons overlap). Per view: AP: 143 -> 107; LAT: 138 -> 102; OBL: 6 -> 5

Self-check of the released re-score against det_fill.json: 135 of 135 cell x view recalls agree.

## Seed-pooled groups, both denominators (k / n, %, 95 % case-clustered interval)

| group | view | rule | released | repaired | delta pp |
|---|---|---|---|---|---:|
| both_view_N0 | ALL | body@0.74 | 66/861 = 7.7 % [4.9, 10.8] | 61/642 = 9.5 % [6.3, 12.9] | 1.8 |
| both_view_N0 | ALL | centre@0.25 | 772/861 = 89.7 % [85.4, 93.4] | 624/642 = 97.2 % [94.3, 99.4] | 7.5 |
| both_view_N0 | AP | body@0.74 | 65/429 = 15.2 % [9.9, 21.3] | 61/321 = 19.0 % [12.8, 25.5] | 3.8 |
| both_view_N0 | AP | centre@0.25 | 393/429 = 91.6 % [87.6, 95.4] | 315/321 = 98.1 % [96.2, 100.0] | 6.5 |
| both_view_N0 | LAT | body@0.74 | 1/414 = 0.2 % [0.0, 0.7] | 0/306 = 0.0 % [0.0, 0.0] | -0.2 |
| both_view_N0 | LAT | centre@0.25 | 363/414 = 87.7 % [81.2, 93.3] | 294/306 = 96.1 % [90.4, 100.0] | 8.4 |
| both_view_N4 | ALL | body@0.74 | 623/861 = 72.4 % [67.9, 76.7] | 533/642 = 83.0 % [78.8, 87.0] | 10.6 |
| both_view_N4 | ALL | centre@0.25 | 744/861 = 86.4 % [82.5, 90.0] | 621/642 = 96.7 % [93.9, 99.1] | 10.3 |
| both_view_N4 | AP | body@0.74 | 319/429 = 74.4 % [69.5, 79.1] | 277/321 = 86.3 % [81.4, 90.8] | 11.9 |
| both_view_N4 | AP | centre@0.25 | 373/429 = 86.9 % [83.2, 90.2] | 314/321 = 97.8 % [95.3, 99.7] | 10.9 |
| both_view_N4 | LAT | body@0.74 | 297/414 = 71.7 % [64.4, 78.3] | 249/306 = 81.4 % [73.5, 88.3] | 9.7 |
| both_view_N4 | LAT | centre@0.25 | 356/414 = 86.0 % [80.8, 90.8] | 292/306 = 95.4 % [90.5, 99.0] | 9.4 |
| both_view_N10 | ALL | body@0.74 | 654/861 = 76.0 % [71.9, 80.3] | 572/642 = 89.1 % [85.6, 92.4] | 13.1 |
| both_view_N10 | ALL | centre@0.25 | 762/861 = 88.5 % [84.7, 92.3] | 627/642 = 97.7 % [95.3, 99.5] | 9.2 |
| both_view_N10 | AP | body@0.74 | 337/429 = 78.6 % [74.3, 82.8] | 297/321 = 92.5 % [88.8, 95.8] | 13.9 |
| both_view_N10 | AP | centre@0.25 | 386/429 = 90.0 % [86.5, 93.1] | 317/321 = 98.8 % [96.5, 100.0] | 8.8 |
| both_view_N10 | LAT | body@0.74 | 305/414 = 73.7 % [67.9, 79.9] | 263/306 = 85.9 % [80.1, 91.7] | 12.2 |
| both_view_N10 | LAT | centre@0.25 | 361/414 = 87.2 % [81.8, 92.3] | 295/306 = 96.4 % [92.9, 99.3] | 9.2 |
| both_view_N24 | ALL | body@0.74 | 723/861 = 84.0 % [80.1, 87.8] | 614/642 = 95.6 % [92.9, 98.0] | 11.6 |
| both_view_N24 | ALL | centre@0.25 | 780/861 = 90.6 % [87.0, 93.9] | 635/642 = 98.9 % [97.0, 100.0] | 8.3 |
| both_view_N24 | AP | body@0.74 | 363/429 = 84.6 % [80.9, 88.3] | 312/321 = 97.2 % [94.1, 99.7] | 12.6 |
| both_view_N24 | AP | centre@0.25 | 391/429 = 91.1 % [87.4, 94.5] | 317/321 = 98.8 % [96.3, 100.0] | 7.7 |
| both_view_N24 | LAT | body@0.74 | 348/414 = 84.1 % [79.0, 89.3] | 290/306 = 94.8 % [91.2, 97.8] | 10.7 |
| both_view_N24 | LAT | centre@0.25 | 374/414 = 90.3 % [86.2, 94.1] | 303/306 = 99.0 % [97.0, 100.0] | 8.7 |
| both_view_N50 | ALL | body@0.74 | 710/861 = 82.5 % [78.5, 86.5] | 612/642 = 95.3 % [92.3, 97.9] | 12.8 |
| both_view_N50 | ALL | centre@0.25 | 782/861 = 90.8 % [87.4, 94.2] | 634/642 = 98.8 % [96.8, 100.0] | 8.0 |
| both_view_N50 | AP | body@0.74 | 361/429 = 84.1 % [80.0, 88.3] | 313/321 = 97.5 % [94.5, 99.7] | 13.4 |
| both_view_N50 | AP | centre@0.25 | 395/429 = 92.1 % [88.3, 95.3] | 317/321 = 98.8 % [96.3, 100.0] | 6.7 |
| both_view_N50 | LAT | body@0.74 | 337/414 = 81.4 % [76.5, 86.5] | 287/306 = 93.8 % [89.5, 97.7] | 12.4 |
| both_view_N50 | LAT | centre@0.25 | 372/414 = 89.9 % [85.4, 94.0] | 302/306 = 98.7 % [96.5, 100.0] | 8.8 |
| both_view_N100 | ALL | body@0.74 | 474/574 = 82.6 % [78.5, 86.7] | 409/428 = 95.6 % [92.4, 98.1] | 13.0 |
| both_view_N100 | ALL | centre@0.25 | 529/574 = 92.2 % [88.5, 95.4] | 423/428 = 98.8 % [96.8, 100.0] | 6.6 |
| both_view_N100 | AP | body@0.74 | 243/286 = 85.0 % [80.7, 89.3] | 209/214 = 97.7 % [94.6, 100.0] | 12.7 |
| both_view_N100 | AP | centre@0.25 | 269/286 = 94.1 % [90.3, 97.1] | 212/214 = 99.1 % [97.1, 100.0] | 5.0 |
| both_view_N100 | LAT | body@0.74 | 222/276 = 80.4 % [75.5, 85.6] | 191/204 = 93.6 % [89.2, 97.6] | 13.2 |
| both_view_N100 | LAT | centre@0.25 | 250/276 = 90.6 % [86.5, 94.4] | 201/204 = 98.5 % [96.1, 100.0] | 7.9 |
| both_view_N200 | ALL | body@0.74 | 474/574 = 82.6 % [78.4, 86.7] | 406/428 = 94.9 % [91.3, 97.9] | 12.3 |
| both_view_N200 | ALL | centre@0.25 | 527/574 = 91.8 % [88.1, 95.5] | 423/428 = 98.8 % [96.7, 100.0] | 7.0 |
| both_view_N200 | AP | body@0.74 | 242/286 = 84.6 % [80.1, 89.3] | 208/214 = 97.2 % [93.6, 100.0] | 12.6 |
| both_view_N200 | AP | centre@0.25 | 265/286 = 92.7 % [88.6, 96.4] | 211/214 = 98.6 % [96.2, 100.0] | 5.9 |
| both_view_N200 | LAT | body@0.74 | 224/276 = 81.2 % [75.9, 86.5] | 190/204 = 93.1 % [88.1, 97.5] | 11.9 |
| both_view_N200 | LAT | centre@0.25 | 252/276 = 91.3 % [87.2, 95.1] | 202/204 = 99.0 % [97.0, 100.0] | 7.7 |
| one_view_N25_AP | ALL | body@0.74 | 246/574 = 42.9 % [40.9, 44.7] | 209/428 = 48.8 % [47.4, 50.0] | 5.9 |
| one_view_N25_AP | ALL | centre@0.25 | 529/574 = 92.2 % [88.6, 95.4] | 424/428 = 99.1 % [97.2, 100.0] | 6.9 |
| one_view_N25_AP | AP | body@0.74 | 245/286 = 85.7 % [81.8, 89.6] | 209/214 = 97.7 % [94.8, 100.0] | 12.0 |
| one_view_N25_AP | AP | centre@0.25 | 264/286 = 92.3 % [88.7, 95.4] | 212/214 = 99.1 % [97.1, 100.0] | 6.8 |
| one_view_N25_AP | LAT | body@0.74 | 1/276 = 0.4 % [0.0, 1.1] | 0/204 = 0.0 % [0.0, 0.0] | -0.4 |
| one_view_N25_AP | LAT | centre@0.25 | 255/276 = 92.4 % [88.5, 95.9] | 202/204 = 99.0 % [97.0, 100.0] | 6.6 |
| one_view_N25_LAT | ALL | body@0.74 | 333/574 = 58.0 % [54.7, 61.8] | 294/428 = 68.7 % [64.5, 73.2] | 10.7 |
| one_view_N25_LAT | ALL | centre@0.25 | 504/574 = 87.8 % [83.8, 91.7] | 410/428 = 95.8 % [93.3, 97.9] | 8.0 |
| one_view_N25_LAT | AP | body@0.74 | 97/286 = 33.9 % [27.6, 39.8] | 93/214 = 43.5 % [35.5, 50.9] | 9.6 |
| one_view_N25_LAT | AP | centre@0.25 | 248/286 = 86.7 % [81.4, 91.7] | 199/214 = 93.0 % [89.0, 96.6] | 6.3 |
| one_view_N25_LAT | LAT | body@0.74 | 229/276 = 83.0 % [78.5, 87.7] | 194/204 = 95.1 % [91.1, 98.5] | 12.1 |
| one_view_N25_LAT | LAT | centre@0.25 | 246/276 = 89.1 % [84.3, 93.6] | 201/204 = 98.5 % [96.1, 100.0] | 9.4 |
| one_view_N50_AP | ALL | body@0.74 | 249/574 = 43.4 % [41.5, 45.3] | 213/428 = 49.8 % [48.4, 51.1] | 6.4 |
| one_view_N50_AP | ALL | centre@0.25 | 517/574 = 90.1 % [86.0, 93.7] | 415/428 = 97.0 % [93.5, 99.8] | 6.9 |
| one_view_N50_AP | AP | body@0.74 | 247/286 = 86.4 % [82.8, 90.3] | 211/214 = 98.6 % [96.2, 100.0] | 12.2 |
| one_view_N50_AP | AP | centre@0.25 | 267/286 = 93.4 % [89.7, 96.6] | 212/214 = 99.1 % [97.1, 100.0] | 5.7 |
| one_view_N50_AP | LAT | body@0.74 | 0/276 = 0.0 % [0.0, 0.0] | 0/204 = 0.0 % [0.0, 0.0] | 0.0 |
| one_view_N50_AP | LAT | centre@0.25 | 239/276 = 86.6 % [80.1, 92.4] | 193/204 = 94.6 % [87.8, 99.5] | 8.0 |
| one_view_N50_LAT | ALL | body@0.74 | 357/574 = 62.2 % [58.5, 66.4] | 312/428 = 72.9 % [68.6, 77.6] | 10.7 |
| one_view_N50_LAT | ALL | centre@0.25 | 526/574 = 91.6 % [87.7, 95.0] | 418/428 = 97.7 % [95.0, 99.5] | 6.1 |
| one_view_N50_LAT | AP | body@0.74 | 113/286 = 39.5 % [32.4, 46.4] | 105/214 = 49.1 % [39.9, 57.7] | 9.6 |
| one_view_N50_LAT | AP | centre@0.25 | 264/286 = 92.3 % [87.8, 96.1] | 206/214 = 96.3 % [92.5, 99.1] | 4.0 |
| one_view_N50_LAT | LAT | body@0.74 | 236/276 = 85.5 % [81.3, 89.9] | 199/204 = 97.5 % [94.6, 100.0] | 12.0 |
| one_view_N50_LAT | LAT | centre@0.25 | 252/276 = 91.3 % [87.0, 95.2] | 202/204 = 99.0 % [97.0, 100.0] | 7.7 |
| heldout_lodo_carm | ALL | body@0.74 | 14/287 = 4.9 % [2.1, 8.1] | 12/214 = 5.6 % [2.3, 9.8] | 0.7 |
| heldout_lodo_carm | ALL | outline@0.74 | 236/287 = 82.2 % [76.7, 87.3] | 201/214 = 93.9 % [90.4, 97.1] | 11.7 |
| heldout_lodo_carm | ALL | centre@0.25 | 267/287 = 93.0 % [89.3, 96.4] | 212/214 = 99.1 % [97.1, 100.0] | 6.1 |
| heldout_lodo_carm | AP | body@0.74 | 13/143 = 9.1 % [4.1, 15.3] | 12/107 = 11.2 % [4.5, 19.6] | 2.1 |
| heldout_lodo_carm | AP | outline@0.74 | 118/143 = 82.5 % [76.2, 88.4] | 100/107 = 93.5 % [88.9, 97.2] | 11.0 |
| heldout_lodo_carm | AP | centre@0.25 | 134/143 = 93.7 % [89.7, 97.1] | 106/107 = 99.1 % [97.1, 100.0] | 5.4 |
| heldout_lodo_carm | LAT | body@0.74 | 1/138 = 0.7 % [0.0, 2.2] | 0/102 = 0.0 % [0.0, 0.0] | -0.7 |
| heldout_lodo_carm | LAT | outline@0.74 | 113/138 = 81.9 % [74.8, 89.0] | 96/102 = 94.1 % [88.8, 98.1] | 12.2 |
| heldout_lodo_carm | LAT | centre@0.25 | 128/138 = 92.8 % [88.6, 96.5] | 101/102 = 99.0 % [97.0, 100.0] | 6.2 |

## Dropped boxes

| frame | j | level | source | visible | complete | reasons |
|---|---:|---|---|---:|---|---|
| case100_AP | 0 | L1 | spineps_corpus | 0.988 | n | cut_by_cbct |
| case100_LAT | 0 | L1 | spineps_corpus | 0.96 | n | cut_by_cbct |
| case10_AP | 0 | ? | spineps_corpus | 0.55 | n | cut_by_cbct, visible_lt_0.8, body_larger_than_outline |
| case10_AP | 1 | L1 | spineps_corpus | 0.992 | n | cut_by_cbct |
| case10_LAT | 0 | ? | spineps_corpus | 1.0 | n | cut_by_cbct, body_larger_than_outline |
| case10_LAT | 1 | L1 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case112_AP | 0 | L1 | spineps_corpus | 0.896 | n | cut_by_cbct |
| case112_LAT | 0 | L1 | spineps_corpus | 0.863 | n | cut_by_cbct |
| case114_AP | 0 | L1 | spineps_corpus | 0.849 | n | cut_by_cbct |
| case114_LAT | 0 | L1 | spineps_corpus | 0.994 | n | cut_by_cbct |
| case116_AP | 0 | L1 | spineps_corpus | 0.978 | n | cut_by_cbct |
| case116_LAT | 0 | L1 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case118_AP | 0 | T12 | spineps_corpus | 0.841 | n | cut_by_cbct |
| case118_OBL | 0 | T12 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case11_AP | 0 | L1 | spineps_corpus | 0.866 | n | cut_by_cbct |
| case11_LAT | 0 | L1 | spineps_corpus | 0.952 | n | cut_by_cbct |
| case122_AP | 0 | L2 | spineps_corpus | 0.963 | n | cut_by_cbct |
| case122_LAT | 0 | L2 | spineps_corpus | 0.998 | n | cut_by_cbct |
| case125_AP | 0 | L1 | spineps_corpus | 0.971 | n | cut_by_cbct |
| case125_LAT | 0 | L1 | spineps_corpus | 0.975 | n | cut_by_cbct |
| case132_AP | 0 | T12 | spineps_corpus | 0.969 | n | cut_by_cbct |
| case132_AP | 5 | ? | whole_vertebra | 1.0 | y | fallback_box |
| case132_LAT | 0 | T12 | spineps_corpus | 0.951 | n | cut_by_cbct |
| case132_LAT | 5 | ? | whole_vertebra | 1.0 | y | fallback_box |
| case133_AP | 0 | ? | spineps_corpus | 0.998 | y | body_larger_than_outline |
| case133_AP | 1 | L1 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case133_LAT | 0 | ? | spineps_corpus | 0.998 | y | body_larger_than_outline |
| case133_LAT | 1 | L1 | spineps_corpus | 0.986 | n | cut_by_cbct |
| case135_AP | 0 | L1 | spineps_corpus | 0.944 | n | cut_by_cbct |
| case135_LAT | 0 | L1 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case136_AP | 0 | ? | spineps_corpus | 0.712 | n | cut_by_cbct, visible_lt_0.8, body_larger_than_outline |
| case136_AP | 1 | ? | spineps_corpus | 0.995 | n | cut_by_cbct |
| case136_LAT | 0 | ? | spineps_corpus | 1.0 | n | cut_by_cbct, body_larger_than_outline |
| case136_LAT | 1 | ? | spineps_corpus | 1.0 | n | cut_by_cbct |
| case139_AP | 0 | L1 | spineps_corpus | 0.958 | n | cut_by_cbct |
| case139_LAT | 0 | L1 | spineps_corpus | 0.952 | n | cut_by_cbct |
| case23_AP | 0 | ? | whole_vertebra | 0.867 | n | cut_by_cbct, fallback_box |
| case23_AP | 1 | L2 | spineps_corpus | 0.999 | n | cut_by_cbct |
| case23_LAT | 0 | ? | whole_vertebra | 0.974 | n | cut_by_cbct, fallback_box |
| case23_LAT | 1 | L2 | spineps_corpus | 0.989 | n | cut_by_cbct |
| case25_AP | 0 | L1 | spineps_corpus | 0.895 | n | cut_by_cbct |
| case25_LAT | 0 | L1 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case32_AP | 0 | L1 | spineps_corpus | 0.883 | n | cut_by_cbct |
| case32_LAT | 0 | L1 | spineps_corpus | 0.999 | n | cut_by_cbct |
| case37_AP | 0 | L1 | spineps_corpus | 0.993 | n | cut_by_cbct |
| case37_LAT | 0 | L1 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case47_AP | 0 | L1 | spineps_corpus | 0.963 | n | cut_by_cbct |
| case47_LAT | 0 | L1 | spineps_corpus | 0.62 | n | cut_by_cbct, visible_lt_0.8 |
| case49_AP | 0 | L1 | spineps_corpus | 0.966 | n | cut_by_cbct |
| case49_LAT | 0 | L1 | spineps_corpus | 0.974 | n | cut_by_cbct |
| case56_AP | 0 | L1 | spineps_corpus | 0.986 | n | cut_by_cbct |
| case56_LAT | 0 | L1 | spineps_corpus | 0.982 | n | cut_by_cbct |
| case5_AP | 0 | ? | spineps_corpus | 0.551 | y | visible_lt_0.8, body_larger_than_outline |
| case5_AP | 1 | L1 | spineps_corpus | 0.955 | n | cut_by_cbct |
| case5_LAT | 0 | ? | spineps_corpus | 1.0 | y | body_larger_than_outline |
| case5_LAT | 1 | L1 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case60_AP | 0 | ? | whole_vertebra | 0.692 | n | cut_by_cbct, fallback_box, visible_lt_0.8 |
| case60_AP | 1 | L2 | spineps_corpus | 0.998 | n | cut_by_cbct |
| case60_LAT | 0 | ? | whole_vertebra | 1.0 | n | cut_by_cbct, fallback_box |
| case60_LAT | 1 | L2 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case6_AP | 0 | L1 | spineps_corpus | 0.944 | n | cut_by_cbct |
| case6_LAT | 0 | L1 | spineps_corpus | 0.985 | n | cut_by_cbct |
| case78_AP | 0 | ? | spineps_corpus | 0.656 | n | cut_by_cbct, visible_lt_0.8, body_larger_than_outline |
| case78_AP | 1 | L2 | spineps_corpus | 0.998 | n | cut_by_cbct |
| case78_LAT | 0 | ? | spineps_corpus | 1.0 | n | cut_by_cbct, body_larger_than_outline |
| case78_LAT | 1 | L2 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case82_AP | 0 | L2 | spineps_corpus | 0.796 | n | cut_by_cbct, visible_lt_0.8 |
| case82_LAT | 0 | ? | spineps_corpus | 1.0 | y | body_larger_than_outline |
| case82_LAT | 1 | L2 | spineps_corpus | 1.0 | n | cut_by_cbct |
| case86_AP | 0 | L2 | spineps_corpus | 0.972 | n | cut_by_cbct |
| case86_LAT | 0 | L2 | spineps_corpus | 0.999 | n | cut_by_cbct |
| case96_AP | 0 | L1 | spineps_corpus | 0.91 | n | cut_by_cbct |
| case96_LAT | 0 | L1 | spineps_corpus | 0.999 | n | cut_by_cbct |
