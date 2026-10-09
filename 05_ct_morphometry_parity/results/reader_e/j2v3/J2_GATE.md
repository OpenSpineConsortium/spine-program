# Reader E J2: QC gate on J1

Generated 2026-09-25T18:42:18Z (job 40448877); inputs: `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/readerE/j1v3/_collect/features_j1.csv` (38,432 instance rows), `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/readerE/j1v3/_collect/features_index.csv` (3,524 pairs), `SchwingNet/results/reader_e/j1_pairs.json`; ranges `reader_e_ranges.json`. Families: ctspine1k 3, spineps 1169, ts 1176, v11 802, versefusion 374.

**Rule.** A feature fails when, in any (family, level) cell with n >= 30 gate-passing values, the SD of the gate-passing values exceeds the widest published living-cohort SD by more than 1.5x, or the flagged share exceeds 40 %. SCD also carries the prevalence check: share below 11.07 mm among mask-passing values against the 2.62 % published prevalence of congenital absolute stenosis, outside its window above 2.0x. The anatomical level is keyed on the instance's position from the sacral plateau (0 = L5 ... 6 = T11), or, without a plateau in field, from the last rib-bearing body (rib-keyed; such cells are reported as information, not as verdicts, because a rib-keyed level is not the atlas level); never on J1's range tag, which clamps every position above T11 into T11 (2,615 morph rows carry the tag T11; 9,071 instance rows sit at position 7 or higher). Where the release atlas row sits more than one published SD from the published pooled mean (Bonczar 2024), the flagged share is judged on an envelope centred on the published mean instead (published means: /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/SchwingNet/results/reader_e/level_references.csv).

## Verdict (numbers)

- features failing: **EPWl**
- features without a published SD on file (cannot pass): **EPDu, EPDl**
- numbers pass: **False**; render verdict: see 'Renders looked at' (hand-written); overall pass requires both.

- EPWl: ts/L2: FAIL: flagged 43 %; ts/L1: FAIL: flagged 41 %
- rib-keyed cells outside the rule (information): VBHa versefusion/T11: info (rib-keyed level, not the atlas level): FAIL: SD 4.21 > 1.5x2.8

## (a) Mask bits, defined and counted per family

Bits are per instance unless marked pair-level. A value under a voiding bit is not a gate-passing value here and is masked (NaN + bit) in J3:

- `VBHa` voided by: partial, tiny, plate_not_ok, merged, VBHa_out_of_range
- `VBHp` voided by: partial, tiny, plate_not_ok, merged, body_cut_fallback, VBHp_out_of_range
- `EPWu` voided by: partial, tiny, plate_not_ok, merged, epw_withheld, EPWu_out_of_range
- `EPWl` voided by: partial, tiny, plate_not_ok, merged, epw_withheld, body_cut_fallback, EPWl_out_of_range
- `EPDu` voided by: partial, tiny, plate_not_ok, merged, body_cut_fallback, EPDu_out_of_range
- `EPDl` voided by: partial, tiny, plate_not_ok, merged, body_cut_fallback, EPDl_out_of_range
- `SCW` voided by: partial, tiny, plate_not_ok, merged, body_cut_fallback, SCW_out_of_range
- `SCD` voided by: partial, tiny, plate_not_ok, merged, body_cut_fallback, SCD_out_of_range
- `partial` = partial_top or partial_bottom (instance cut by the field): voids morph on that instance; `tiny` < 1 ml
- `plate_not_ok` = morph_plate_ok false, or morphometry selected and no fit: voids every plate-derived value (heights, plate dimensions, the frame the canal is read in)
- `body_cut_fallback` = morph.body_cut == ostk_body_mask_fallback (the 1b7005c corner): voids VBHp, EPDu, EPDl, EPWl, and SCW/SCD (fallback rows read the canal on the pocket: 78-100 % of them sit under the 11.07 mm floor)
- `merged` = doubled or half or fragment (labeller B's spacing rules): two bodies under one name or a split body
- `<key>_out_of_range` = the LEVEL_MORPHOMETRY envelope bit, recomputed here with the level bit dropped on positions 7+ (0 J1 bits flip; a J1 re-run with the fixed range_check writes them that way)
- `scd_below_published_floor` (< 11.07 mm), `tp_body_half_invalid` (tp_metrics baseline swallowed the transverse processes), `epw_withheld` (value > 60 mm or the two lowest presacral), `epw_position_unverified`, `rib_chord_out_of_range`, `level_tag_clamped`
- pair-level: `sacrum_unverified`, `no_sacrum` (sacrum source none: every plateau-keyed feature absent), `guard_misnamed` (SPINEPS guard misnamed_1_2_levels), `reader_c_blank` (no reader C call)

| bit | total | ctspine1k | spineps | ts | v11 | versefusion |
|---|---|---|---|---|---|---|
| partial | 5864 | 7 | 1461 | 2503 | 1812 | 81 |
| tiny | 1362 | 2 | 62 | 744 | 554 | 0 |
| plate_not_ok | 1819 | 0 | 575 | 677 | 73 | 494 |
| body_cut_fallback | 3682 | 2 | 1204 | 1372 | 842 | 262 |
| doubled | 228 | 0 | 58 | 119 | 2 | 49 |
| fragment | 158 | 0 | 43 | 112 | 0 | 3 |
| half | 333 | 0 | 75 | 256 | 0 | 2 |
| gap_below | 249 | 0 | 35 | 130 | 84 | 0 |
| merged | 582 | 0 | 141 | 386 | 2 | 53 |
| tp_body_half_invalid | 373 | 0 | 137 | 107 | 33 | 96 |
| epw_withheld | 6654 | 0 | 2107 | 2437 | 1716 | 394 |
| epw_position_unverified | 7429 | 30 | 3343 | 757 | 0 | 3299 |
| scd_below_published_floor | 166 | 0 | 43 | 75 | 7 | 41 |
| level_tag_clamped | 9071 | 0 | 1828 | 4739 | 2504 | 0 |
| VBHa_out_of_range | 5429 | 0 | 1824 | 2097 | 889 | 619 |
| VBHp_out_of_range | 7827 | 2 | 2832 | 2811 | 1385 | 797 |
| EPWu_out_of_range | 947 | 0 | 275 | 404 | 223 | 45 |
| EPWl_out_of_range | 2302 | 0 | 672 | 958 | 603 | 69 |
| EPDu_out_of_range | 1491 | 0 | 472 | 525 | 184 | 310 |
| EPDl_out_of_range | 2019 | 0 | 649 | 704 | 216 | 450 |
| SCW_out_of_range | 698 | 1 | 216 | 295 | 99 | 87 |
| SCD_out_of_range | 839 | 2 | 230 | 369 | 126 | 112 |
| rib_chord_out_of_range | 208 | 0 | 86 | 44 | 3 | 75 |
| sacrum_unverified | 0 | 0 | 0 | 0 | 0 | 0 |
| no_sacrum | 10476 | 55 | 4865 | 1008 | 0 | 4548 |
| guard_misnamed | 98 | 0 | 98 | 0 | 0 | 0 |
| reader_c_blank | 280 | 0 | 264 | 13 | 0 | 3 |
| has_morph | 31316 | 30 | 10471 | 10467 | 7049 | 3299 |
| morph_selected | 31323 | 30 | 10473 | 10471 | 7050 | 3299 |

## (b) Spread per feature, family and level: gate-passing values against the atlas and the widest published SD

n_meas = values present; n_pre = after the mask bits (before the range bit); n_pass = gate-passing; SD_pre / SD_pass likewise; atlas = CTSpinoPelvic1K release level_atlas.csv (median, own SD); pub SD = widest living-cohort SD in level_references.csv; flagged = 1 - n_pass / n_meas. 'pooled' pools L5..T11 (between-level spread included; information only). rib% = share of the cell keyed on the last rib instead of the plateau.

### VBHa -- pass (widest published SD 2.8 (Busscher 2010 L2 M (n=6, fresh-frozen cadaver, male)))

| family | level | n_measured | n_prebit | n_pass | median_pass | sd_pass | sd_prebit | atlas_median | atlas_sd | pub_mean | pub_sd | sd_ratio | flagged(atlas) | flagged(pub) | rib% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctspine1k | L4 | 1 | 1 | 1 | 29.69 | - | - | 31.20 | 2.18 | 26.86 | 2.80 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L3 | 1 | 1 | 1 | 28.91 | - | - | 30.40 | 2.12 | 26.83 | 2.80 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L2 | 1 | 1 | 1 | 28.03 | - | - | 30.40 | 2.40 | 25.75 | 2.80 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L1 | 2 | 2 | 2 | 28.05 | - | - | 28.80 | 2.80 | 24.54 | 2.80 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | T12 | 3 | 3 | 3 | 27.29 | 3.86 | 3.86 | 27.20 | 2.25 | 22.78 | 2.80 | 1.38 | 0.000 | 0.333 | 1.00 | n<30 |
| ctspine1k | T11 | 3 | 3 | 3 | 31.14 | 5.45 | 5.45 | 25.60 | 2.48 | - | 2.80 | 1.94 | 0.000 | - | 1.00 | n<30 |
| ctspine1k | aboveT11 | 19 | 19 | 19 | 22.83 | 3.93 | 3.93 | - | - | - | 2.80 | 1.40 | 0.000 | - | 1.00 | info (no atlas row above T11) |
| ctspine1k | pooled | 11 | 11 | 11 | 28.91 | 3.26 | 3.26 | - | - | - | 2.80 | 1.16 | 0.000 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| spineps | L5 | 872 | 819 | 751 | 30.20 | 2.51 | 3.80 | 32.00 | 2.63 | 27.44 | 2.80 | 0.898 | 0.139 | 0.085 | 0.125 | pass [published-centred envelope] |
| spineps | L4 | 941 | 904 | 864 | 30.25 | 2.63 | 2.95 | 31.20 | 2.18 | 26.86 | 2.80 | 0.938 | 0.082 | 0.063 | 0.143 | pass [published-centred envelope] |
| spineps | L3 | 961 | 925 | 887 | 30.37 | 2.60 | 3.06 | 30.40 | 2.12 | 26.83 | 2.80 | 0.927 | 0.077 | 0.071 | 0.161 | pass [published-centred envelope] |
| spineps | L2 | 999 | 955 | 910 | 29.41 | 2.68 | 3.35 | 30.40 | 2.40 | 25.75 | 2.80 | 0.958 | 0.089 | 0.078 | 0.193 | pass [published-centred envelope] |
| spineps | L1 | 1023 | 974 | 865 | 27.47 | 2.47 | 3.48 | 28.80 | 2.80 | 24.54 | 2.80 | 0.883 | 0.154 | 0.073 | 0.213 | pass [published-centred envelope] |
| spineps | T12 | 1150 | 1037 | 935 | 25.56 | 2.43 | 3.77 | 27.20 | 2.25 | 22.78 | 2.80 | 0.868 | 0.187 | 0.126 | 0.302 | pass [published-centred envelope] |
| spineps | T11 | 1135 | 962 | 925 | 23.92 | 2.77 | 3.53 | 25.60 | 2.48 | - | 2.80 | 0.990 | 0.185 | - | 0.304 | pass |
| spineps | aboveT11 | 3289 | 2223 | 1827 | 22.30 | 3.03 | 5.09 | - | - | - | 2.80 | 1.08 | 0.445 | - | 0.529 | info (no atlas row above T11) |
| spineps | pooled | 7081 | 6576 | 6137 | 28.25 | 3.50 | 4.21 | - | - | - | 2.80 | 1.25 | 0.133 | - | 0.212 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| ts | L5 | 1111 | 984 | 882 | 30.22 | 2.29 | 4.42 | 32.00 | 2.63 | 27.44 | 2.80 | 0.817 | 0.206 | 0.143 | 0.015 | pass [published-centred envelope] |
| ts | L4 | 1118 | 1043 | 957 | 30.47 | 2.25 | 6.54 | 31.20 | 2.18 | 26.86 | 2.80 | 0.804 | 0.144 | 0.119 | 0.022 | pass [published-centred envelope] |
| ts | L3 | 1124 | 1001 | 906 | 30.54 | 2.35 | 6.56 | 30.40 | 2.12 | 26.83 | 2.80 | 0.838 | 0.194 | 0.166 | 0.029 | pass [published-centred envelope] |
| ts | L2 | 1134 | 1035 | 946 | 29.44 | 2.32 | 5.61 | 30.40 | 2.40 | 25.75 | 2.80 | 0.830 | 0.166 | 0.135 | 0.041 | pass [published-centred envelope] |
| ts | L1 | 1144 | 1061 | 884 | 27.39 | 2.17 | 4.17 | 28.80 | 2.80 | 24.54 | 2.80 | 0.776 | 0.227 | 0.097 | 0.048 | pass [published-centred envelope] |
| ts | T12 | 1145 | 1033 | 898 | 25.30 | 1.96 | 3.57 | 27.20 | 2.25 | 22.78 | 2.80 | 0.700 | 0.216 | 0.120 | 0.054 | pass [published-centred envelope] |
| ts | T11 | 1117 | 916 | 885 | 23.43 | 2.30 | 3.21 | 25.60 | 2.48 | - | 2.80 | 0.822 | 0.208 | - | 0.067 | pass |
| ts | aboveT11 | 2532 | 1552 | 1325 | 22.00 | 2.63 | 4.90 | - | - | - | 2.80 | 0.938 | 0.477 | - | 0.159 | info (no atlas row above T11) |
| ts | pooled | 7893 | 7073 | 6358 | 28.47 | 3.43 | 5.80 | - | - | - | 2.80 | 1.22 | 0.194 | - | 0.040 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| v11 | L5 | 802 | 759 | 688 | 30.17 | 2.15 | 3.97 | 32.00 | 2.63 | 27.44 | 2.80 | 0.768 | 0.142 | 0.084 | 0.000 | pass [published-centred envelope] |
| v11 | L4 | 802 | 793 | 748 | 30.54 | 2.16 | 3.78 | 31.20 | 2.18 | 26.86 | 2.80 | 0.773 | 0.067 | 0.049 | 0.000 | pass [published-centred envelope] |
| v11 | L3 | 802 | 794 | 750 | 30.78 | 2.13 | 2.95 | 30.40 | 2.12 | 26.83 | 2.80 | 0.760 | 0.065 | 0.050 | 0.000 | pass [published-centred envelope] |
| v11 | L2 | 802 | 793 | 751 | 29.75 | 2.05 | 2.34 | 30.40 | 2.40 | 25.75 | 2.80 | 0.731 | 0.064 | 0.039 | 0.000 | pass [published-centred envelope] |
| v11 | L1 | 802 | 796 | 690 | 27.55 | 1.87 | 2.76 | 28.80 | 2.80 | 24.54 | 2.80 | 0.668 | 0.140 | 0.022 | 0.000 | pass [published-centred envelope] |
| v11 | T12 | 800 | 768 | 689 | 25.45 | 1.86 | 2.44 | 27.20 | 2.25 | 22.78 | 2.80 | 0.663 | 0.139 | 0.050 | 0.000 | pass [published-centred envelope] |
| v11 | T11 | 783 | 672 | 665 | 23.66 | 2.20 | 2.42 | 25.60 | 2.48 | - | 2.80 | 0.785 | 0.151 | - | 0.000 | pass |
| v11 | aboveT11 | 1456 | 813 | 804 | 22.46 | 2.50 | 2.58 | - | - | - | 2.80 | 0.894 | 0.448 | - | 0.000 | info (no atlas row above T11) |
| v11 | pooled | 5593 | 5375 | 4981 | 28.73 | 3.27 | 3.92 | - | - | - | 2.80 | 1.17 | 0.109 | - | 0.000 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| versefusion | L5 | 112 | 93 | 89 | 30.69 | 3.01 | 5.30 | 32.00 | 2.63 | 27.44 | 2.80 | 1.07 | 0.205 | 0.214 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | L4 | 137 | 120 | 113 | 30.62 | 2.87 | 5.43 | 31.20 | 2.18 | 26.86 | 2.80 | 1.03 | 0.175 | 0.182 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | L3 | 170 | 144 | 140 | 30.30 | 3.01 | 4.01 | 30.40 | 2.12 | 26.83 | 2.80 | 1.07 | 0.176 | 0.194 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | L2 | 199 | 165 | 161 | 29.39 | 3.27 | 4.33 | 30.40 | 2.40 | 25.75 | 2.80 | 1.17 | 0.191 | 0.221 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | L1 | 234 | 199 | 185 | 28.32 | 3.59 | 5.07 | 28.80 | 2.80 | 24.54 | 2.80 | 1.28 | 0.209 | 0.244 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | T12 | 358 | 300 | 278 | 27.41 | 3.79 | 5.36 | 27.20 | 2.25 | 22.78 | 2.80 | 1.36 | 0.223 | 0.291 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | T11 | 347 | 308 | 284 | 26.72 | 4.21 | 6.04 | 25.60 | 2.48 | - | 2.80 | 1.50 | 0.182 | - | 1.00 | info (rib-keyed level, not the atlas level): FAIL: SD 4.21 > 1.5x2.8 |
| versefusion | aboveT11 | 1609 | 1371 | 1152 | 23.95 | 3.85 | 5.93 | - | - | - | 2.80 | 1.38 | 0.284 | - | 1.00 | info (no atlas row above T11) |
| versefusion | pooled | 1557 | 1329 | 1250 | 28.78 | 3.89 | 5.50 | - | - | - | 2.80 | 1.39 | 0.197 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |

### VBHp -- pass (widest published SD 3.8 (Busscher 2010 L5 M (n=6, fresh-frozen cadaver, male)))

| family | level | n_measured | n_prebit | n_pass | median_pass | sd_pass | sd_prebit | atlas_median | atlas_sd | pub_mean | pub_sd | sd_ratio | flagged(atlas) | flagged(pub) | rib% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctspine1k | L4 | 1 | 1 | 1 | 27.11 | - | - | 29.60 | 2.13 | 25.76 | 3.80 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L3 | 1 | 1 | 1 | 26.93 | - | - | 30.40 | 2.04 | 26.67 | 3.80 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L2 | 1 | 1 | 1 | 26.59 | - | - | 30.40 | 2.07 | 27.02 | 3.80 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L1 | 2 | 2 | 2 | 27.86 | - | - | 30.40 | 2.52 | 26.57 | 3.80 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | T12 | 3 | 3 | 3 | 25.38 | 1.22 | 1.22 | 28.80 | 2.35 | 24.66 | 3.80 | 0.321 | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | T11 | 3 | 3 | 3 | 27.25 | 0.362 | 0.362 | 26.40 | 2.41 | - | 3.80 | 0.095 | 0.000 | - | 1.00 | n<30 |
| ctspine1k | aboveT11 | 19 | 17 | 15 | 25.47 | 2.37 | 2.73 | - | - | - | 3.80 | 0.624 | 0.211 | - | 1.00 | info (no atlas row above T11) |
| ctspine1k | pooled | 11 | 11 | 11 | 27.11 | 1.37 | 1.37 | - | - | - | 3.80 | 0.361 | 0.000 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| spineps | L5 | 872 | 801 | 531 | 26.20 | 2.39 | 3.11 | 30.40 | 3.29 | 24.11 | 3.80 | 0.628 | 0.391 | 0.092 | 0.125 | pass [published-centred envelope] |
| spineps | L4 | 941 | 865 | 772 | 27.47 | 2.22 | 2.63 | 29.60 | 2.13 | 25.76 | 3.80 | 0.585 | 0.180 | 0.082 | 0.143 | pass [published-centred envelope] |
| spineps | L3 | 961 | 863 | 794 | 28.23 | 2.26 | 2.78 | 30.40 | 2.04 | 26.67 | 3.80 | 0.595 | 0.174 | 0.104 | 0.161 | pass |
| spineps | L2 | 999 | 807 | 722 | 28.63 | 2.48 | 3.25 | 30.40 | 2.07 | 27.02 | 3.80 | 0.652 | 0.277 | 0.197 | 0.193 | pass |
| spineps | L1 | 1023 | 837 | 749 | 28.68 | 2.72 | 3.60 | 30.40 | 2.52 | 26.57 | 3.80 | 0.717 | 0.268 | 0.188 | 0.213 | pass [published-centred envelope] |
| spineps | T12 | 1150 | 912 | 810 | 27.25 | 2.78 | 3.82 | 28.80 | 2.35 | 24.66 | 3.80 | 0.732 | 0.296 | 0.214 | 0.302 | pass [published-centred envelope] |
| spineps | T11 | 1135 | 916 | 834 | 25.78 | 2.41 | 3.28 | 26.40 | 2.41 | - | 3.80 | 0.635 | 0.265 | - | 0.304 | pass |
| spineps | aboveT11 | 3289 | 2046 | 1331 | 24.26 | 2.17 | 4.46 | - | - | - | 3.80 | 0.571 | 0.595 | - | 0.529 | info (no atlas row above T11) |
| spineps | pooled | 7081 | 6001 | 5212 | 27.53 | 2.68 | 3.43 | - | - | - | 3.80 | 0.704 | 0.264 | - | 0.212 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| ts | L5 | 1111 | 955 | 584 | 26.39 | 1.83 | 3.69 | 30.40 | 3.29 | 24.11 | 3.80 | 0.482 | 0.474 | 0.150 | 0.015 | pass [published-centred envelope] |
| ts | L4 | 1118 | 989 | 865 | 27.78 | 1.99 | 5.16 | 29.60 | 2.13 | 25.76 | 3.80 | 0.524 | 0.226 | 0.134 | 0.022 | pass [published-centred envelope] |
| ts | L3 | 1124 | 926 | 825 | 28.70 | 1.98 | 5.51 | 30.40 | 2.04 | 26.67 | 3.80 | 0.521 | 0.266 | 0.198 | 0.029 | pass |
| ts | L2 | 1134 | 847 | 754 | 28.95 | 2.06 | 5.26 | 30.40 | 2.07 | 27.02 | 3.80 | 0.543 | 0.335 | 0.272 | 0.041 | pass |
| ts | L1 | 1144 | 878 | 772 | 29.01 | 2.20 | 4.23 | 30.40 | 2.52 | 26.57 | 3.80 | 0.579 | 0.325 | 0.244 | 0.048 | pass [published-centred envelope] |
| ts | T12 | 1145 | 882 | 788 | 27.77 | 2.33 | 3.79 | 28.80 | 2.35 | 24.66 | 3.80 | 0.613 | 0.312 | 0.240 | 0.054 | pass [published-centred envelope] |
| ts | T11 | 1117 | 869 | 820 | 25.97 | 2.35 | 3.24 | 26.40 | 2.41 | - | 3.80 | 0.617 | 0.266 | - | 0.067 | pass |
| ts | aboveT11 | 2532 | 1454 | 1046 | 23.74 | 2.03 | 4.62 | - | - | - | 3.80 | 0.534 | 0.587 | - | 0.159 | info (no atlas row above T11) |
| ts | pooled | 7893 | 6346 | 5408 | 27.89 | 2.40 | 4.72 | - | - | - | 3.80 | 0.630 | 0.315 | - | 0.040 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| v11 | L5 | 802 | 736 | 476 | 26.26 | 2.15 | 2.83 | 30.40 | 3.29 | 24.11 | 3.80 | 0.566 | 0.406 | 0.089 | 0.000 | pass [published-centred envelope] |
| v11 | L4 | 802 | 761 | 686 | 27.71 | 1.92 | 2.78 | 29.60 | 2.13 | 25.76 | 3.80 | 0.505 | 0.145 | 0.054 | 0.000 | pass [published-centred envelope] |
| v11 | L3 | 802 | 729 | 679 | 28.62 | 1.91 | 2.18 | 30.40 | 2.04 | 26.67 | 3.80 | 0.502 | 0.153 | 0.091 | 0.000 | pass |
| v11 | L2 | 802 | 660 | 609 | 29.06 | 2.05 | 2.38 | 30.40 | 2.07 | 27.02 | 3.80 | 0.541 | 0.241 | 0.177 | 0.000 | pass |
| v11 | L1 | 802 | 665 | 605 | 29.29 | 2.20 | 2.55 | 30.40 | 2.52 | 26.57 | 3.80 | 0.580 | 0.246 | 0.171 | 0.000 | pass [published-centred envelope] |
| v11 | T12 | 800 | 661 | 615 | 27.95 | 2.27 | 2.59 | 28.80 | 2.35 | 24.66 | 3.80 | 0.597 | 0.231 | 0.174 | 0.000 | pass [published-centred envelope] |
| v11 | T11 | 783 | 644 | 626 | 26.09 | 2.33 | 2.54 | 26.40 | 2.41 | - | 3.80 | 0.614 | 0.201 | - | 0.000 | pass |
| v11 | aboveT11 | 1456 | 757 | 671 | 24.08 | 2.03 | 2.33 | - | - | - | 3.80 | 0.534 | 0.539 | - | 0.000 | info (no atlas row above T11) |
| v11 | pooled | 5593 | 4856 | 4296 | 27.99 | 2.39 | 2.86 | - | - | - | 3.80 | 0.630 | 0.232 | - | 0.000 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| versefusion | L5 | 112 | 93 | 87 | 26.54 | 2.74 | 4.51 | 30.40 | 3.29 | 24.11 | 3.80 | 0.722 | 0.223 | 0.196 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | L4 | 137 | 113 | 108 | 27.99 | 2.77 | 3.86 | 29.60 | 2.13 | 25.76 | 3.80 | 0.729 | 0.212 | 0.197 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | L3 | 170 | 138 | 136 | 28.56 | 2.90 | 3.53 | 30.40 | 2.04 | 26.67 | 3.80 | 0.762 | 0.200 | 0.200 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L2 | 199 | 154 | 146 | 28.20 | 2.99 | 4.13 | 30.40 | 2.07 | 27.02 | 3.80 | 0.788 | 0.266 | 0.241 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L1 | 234 | 183 | 170 | 28.55 | 2.74 | 4.26 | 30.40 | 2.52 | 26.57 | 3.80 | 0.722 | 0.274 | 0.239 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | T12 | 358 | 289 | 248 | 27.46 | 2.83 | 4.23 | 28.80 | 2.35 | 24.66 | 3.80 | 0.744 | 0.307 | 0.198 | 1.00 | info (rib-keyed level, not the atlas level): pass [published-centred envelope] |
| versefusion | T11 | 347 | 287 | 252 | 27.31 | 2.50 | 4.13 | 26.40 | 2.41 | - | 3.80 | 0.658 | 0.274 | - | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | aboveT11 | 1609 | 1291 | 960 | 25.81 | 3.08 | 5.33 | - | - | - | 3.80 | 0.812 | 0.403 | - | 1.00 | info (no atlas row above T11) |
| versefusion | pooled | 1557 | 1257 | 1147 | 27.81 | 2.82 | 4.19 | - | - | - | 3.80 | 0.741 | 0.263 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |

### EPWu -- pass (widest published SD 5.54 (Yadav 2020 L5 M (n=302, adults, Indian)))

| family | level | n_measured | n_prebit | n_pass | median_pass | sd_pass | sd_prebit | atlas_median | atlas_sd | pub_mean | pub_sd | sd_ratio | flagged(atlas) | flagged(pub) | rib% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctspine1k | L4 | 1 | 1 | 1 | 44.88 | - | - | 47.00 | 5.61 | 47.50 | 5.54 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L3 | 1 | 1 | 1 | 42.40 | - | - | 44.10 | 5.19 | 44.82 | 5.54 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L2 | 1 | 1 | 1 | 41.68 | - | - | 42.20 | 4.54 | 42.98 | 5.54 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L1 | 2 | 2 | 2 | 44.57 | - | - | 40.70 | 4.71 | 41.09 | 5.54 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | T12 | 3 | 3 | 3 | 43.19 | 0.426 | 0.426 | 39.90 | 4.97 | 35.63 | 5.54 | 0.077 | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | T11 | 3 | 3 | 3 | 43.38 | 3.46 | 3.46 | 37.60 | 4.67 | - | 5.54 | 0.624 | 0.000 | - | 1.00 | n<30 |
| ctspine1k | aboveT11 | 19 | 19 | 19 | 33.78 | 3.16 | 3.16 | - | - | - | 5.54 | 0.571 | 0.000 | - | 1.00 | info (no atlas row above T11) |
| ctspine1k | pooled | 11 | 11 | 11 | 43.24 | 1.97 | 1.97 | - | - | - | 5.54 | 0.355 | 0.000 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| spineps | L5 | 61 | 53 | 53 | 49.81 | 5.90 | 5.90 | - | - | 48.81 | 5.54 | 1.07 | 0.131 | 0.131 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| spineps | L4 | 117 | 103 | 102 | 49.18 | 4.88 | 5.40 | 47.00 | 5.61 | 47.50 | 5.54 | 0.881 | 0.128 | 0.128 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| spineps | L3 | 892 | 862 | 840 | 46.12 | 4.75 | 5.09 | 44.10 | 5.19 | 44.82 | 5.54 | 0.857 | 0.058 | 0.034 | 0.147 | pass |
| spineps | L2 | 944 | 907 | 871 | 44.07 | 4.67 | 5.11 | 42.20 | 4.54 | 42.98 | 5.54 | 0.843 | 0.077 | 0.042 | 0.181 | pass |
| spineps | L1 | 981 | 942 | 899 | 43.05 | 4.63 | 5.34 | 40.70 | 4.71 | 41.09 | 5.54 | 0.836 | 0.084 | 0.048 | 0.192 | pass |
| spineps | T12 | 1053 | 967 | 932 | 43.51 | 5.20 | 5.49 | 39.90 | 4.97 | 35.63 | 5.54 | 0.939 | 0.115 | 0.140 | 0.244 | pass |
| spineps | T11 | 1084 | 920 | 886 | 40.80 | 5.06 | 5.36 | 37.60 | 4.67 | - | 5.54 | 0.914 | 0.183 | - | 0.279 | pass |
| spineps | aboveT11 | 3167 | 2153 | 2133 | 39.07 | 6.97 | 7.09 | - | - | - | 5.54 | 1.26 | 0.326 | - | 0.515 | info (no atlas row above T11) |
| spineps | pooled | 5132 | 4754 | 4583 | 43.74 | 5.24 | 5.60 | - | - | - | 5.54 | 0.946 | 0.107 | - | 0.239 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| ts | L5 | 16 | 7 | 6 | 37.58 | 8.73 | 10.95 | - | - | 48.81 | 5.54 | 1.58 | 0.625 | 0.750 | 1.00 | n<30 |
| ts | L4 | 24 | 10 | 9 | 39.28 | 8.85 | 9.26 | 47.00 | 5.61 | 47.50 | 5.54 | 1.60 | 0.625 | 0.708 | 1.00 | n<30 |
| ts | L3 | 1035 | 929 | 901 | 46.41 | 4.75 | 5.33 | 44.10 | 5.19 | 44.82 | 5.54 | 0.857 | 0.129 | 0.107 | 0.031 | pass |
| ts | L2 | 1087 | 994 | 930 | 44.28 | 4.37 | 5.17 | 42.20 | 4.54 | 42.98 | 5.54 | 0.788 | 0.144 | 0.089 | 0.040 | pass |
| ts | L1 | 1124 | 1042 | 967 | 43.31 | 4.50 | 5.31 | 40.70 | 4.71 | 41.09 | 5.54 | 0.811 | 0.140 | 0.079 | 0.047 | pass |
| ts | T12 | 1135 | 1025 | 966 | 43.37 | 4.69 | 5.39 | 39.90 | 4.97 | 35.63 | 5.54 | 0.846 | 0.149 | 0.149 | 0.053 | pass |
| ts | T11 | 1102 | 904 | 857 | 40.39 | 4.29 | 4.97 | 37.60 | 4.67 | - | 5.54 | 0.774 | 0.222 | - | 0.062 | pass |
| ts | aboveT11 | 2469 | 1521 | 1496 | 37.14 | 6.34 | 6.62 | - | - | - | 5.54 | 1.15 | 0.394 | - | 0.142 | info (no atlas row above T11) |
| ts | pooled | 5523 | 4911 | 4636 | 43.55 | 4.94 | 5.59 | - | - | - | 5.54 | 0.892 | 0.161 | - | 0.054 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| v11 | L3 | 747 | 741 | 727 | 45.85 | 4.70 | 5.07 | 44.10 | 5.19 | 44.82 | 5.54 | 0.849 | 0.027 | 0.011 | 0.000 | pass |
| v11 | L2 | 774 | 766 | 724 | 44.06 | 4.27 | 4.88 | 42.20 | 4.54 | 42.98 | 5.54 | 0.770 | 0.065 | 0.010 | 0.000 | pass |
| v11 | L1 | 790 | 785 | 742 | 42.76 | 4.17 | 5.01 | 40.70 | 4.71 | 41.09 | 5.54 | 0.752 | 0.061 | 0.011 | 0.000 | pass |
| v11 | T12 | 796 | 764 | 722 | 43.24 | 4.46 | 5.01 | 39.90 | 4.97 | 35.63 | 5.54 | 0.804 | 0.093 | 0.090 | 0.000 | pass |
| v11 | T11 | 777 | 666 | 639 | 40.01 | 4.02 | 4.53 | 37.60 | 4.67 | - | 5.54 | 0.725 | 0.178 | - | 0.000 | pass |
| v11 | aboveT11 | 1449 | 809 | 809 | 37.35 | 4.88 | 4.88 | - | - | - | 5.54 | 0.882 | 0.442 | - | 0.000 | info (no atlas row above T11) |
| v11 | pooled | 3884 | 3722 | 3554 | 43.29 | 4.73 | 5.22 | - | - | - | 5.54 | 0.854 | 0.085 | - | 0.000 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| versefusion | L5 | 60 | 55 | 54 | 49.93 | 5.09 | 5.21 | - | - | 48.81 | 5.54 | 0.918 | 0.100 | 0.083 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L4 | 111 | 97 | 97 | 48.81 | 5.43 | 5.43 | 47.00 | 5.61 | 47.50 | 5.54 | 0.980 | 0.126 | 0.135 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L3 | 143 | 121 | 121 | 46.93 | 5.43 | 5.43 | 44.10 | 5.19 | 44.82 | 5.54 | 0.980 | 0.154 | 0.154 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L2 | 166 | 141 | 141 | 46.21 | 5.40 | 5.40 | 42.20 | 4.54 | 42.98 | 5.54 | 0.975 | 0.151 | 0.151 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L1 | 204 | 177 | 175 | 45.26 | 6.29 | 6.58 | 40.70 | 4.71 | 41.09 | 5.54 | 1.14 | 0.142 | 0.142 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | T12 | 295 | 254 | 249 | 45.49 | 7.52 | 7.91 | 39.90 | 4.97 | 35.63 | 5.54 | 1.36 | 0.156 | 0.261 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | T11 | 317 | 280 | 278 | 43.25 | 7.25 | 7.42 | 37.60 | 4.67 | - | 5.54 | 1.31 | 0.123 | - | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | aboveT11 | 1518 | 1309 | 1293 | 40.58 | 7.54 | 7.69 | - | - | - | 5.54 | 1.36 | 0.148 | - | 1.00 | info (no atlas row above T11) |
| versefusion | pooled | 1296 | 1125 | 1115 | 45.93 | 6.81 | 7.04 | - | - | - | 5.54 | 1.23 | 0.140 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |

### EPWl -- FAIL (widest published SD 5.54 (Yadav 2020 L5 M (n=302, adults, Indian)))

| family | level | n_measured | n_prebit | n_pass | median_pass | sd_pass | sd_prebit | atlas_median | atlas_sd | pub_mean | pub_sd | sd_ratio | flagged(atlas) | flagged(pub) | rib% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctspine1k | L4 | 1 | 1 | 1 | 51.73 | - | - | 47.00 | 5.61 | 47.50 | 5.54 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L3 | 1 | 1 | 1 | 48.78 | - | - | 44.10 | 5.19 | 44.82 | 5.54 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L2 | 1 | 1 | 1 | 45.70 | - | - | 42.20 | 4.54 | 42.98 | 5.54 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L1 | 2 | 2 | 2 | 45.62 | - | - | 40.70 | 4.71 | 41.09 | 5.54 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | T12 | 3 | 3 | 3 | 45.45 | 3.00 | 3.00 | 39.90 | 4.97 | 35.63 | 5.54 | 0.542 | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | T11 | 3 | 3 | 3 | 45.29 | 2.09 | 2.09 | 37.60 | 4.67 | - | 5.54 | 0.377 | 0.000 | - | 1.00 | n<30 |
| ctspine1k | aboveT11 | 19 | 17 | 17 | 36.55 | 3.85 | 3.85 | - | - | - | 5.54 | 0.695 | 0.105 | - | 1.00 | info (no atlas row above T11) |
| ctspine1k | pooled | 11 | 11 | 11 | 45.45 | 2.85 | 2.85 | - | - | - | 5.54 | 0.514 | 0.000 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| spineps | L5 | 61 | 51 | 50 | 50.13 | 4.84 | 4.98 | - | - | 48.81 | 5.54 | 0.874 | 0.180 | 0.164 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| spineps | L4 | 117 | 98 | 98 | 51.67 | 5.74 | 5.74 | 47.00 | 5.61 | 47.50 | 5.54 | 1.04 | 0.162 | 0.171 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| spineps | L3 | 892 | 805 | 760 | 49.28 | 4.37 | 4.76 | 44.10 | 5.19 | 44.82 | 5.54 | 0.789 | 0.148 | 0.098 | 0.147 | pass |
| spineps | L2 | 944 | 766 | 628 | 46.77 | 4.36 | 5.22 | 42.20 | 4.54 | 42.98 | 5.54 | 0.787 | 0.335 | 0.193 | 0.181 | pass |
| spineps | L1 | 981 | 810 | 676 | 45.60 | 4.59 | 5.48 | 40.70 | 4.71 | 41.09 | 5.54 | 0.828 | 0.311 | 0.194 | 0.192 | pass |
| spineps | T12 | 1053 | 845 | 773 | 45.04 | 5.11 | 5.57 | 39.90 | 4.97 | 35.63 | 5.54 | 0.922 | 0.266 | 0.296 | 0.244 | pass |
| spineps | T11 | 1084 | 876 | 752 | 43.57 | 5.33 | 5.77 | 37.60 | 4.67 | - | 5.54 | 0.962 | 0.306 | - | 0.279 | pass |
| spineps | aboveT11 | 3167 | 1985 | 1980 | 42.08 | 6.53 | 6.60 | - | - | - | 5.54 | 1.18 | 0.375 | - | 0.515 | info (no atlas row above T11) |
| spineps | pooled | 5132 | 4251 | 3737 | 46.27 | 5.29 | 5.73 | - | - | - | 5.54 | 0.956 | 0.272 | - | 0.239 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| ts | L5 | 16 | 4 | 4 | 38.20 | 9.43 | 9.43 | - | - | 48.81 | 5.54 | 1.70 | 0.750 | 0.812 | 1.00 | n<30 |
| ts | L4 | 24 | 10 | 8 | 37.74 | 7.44 | 8.87 | 47.00 | 5.61 | 47.50 | 5.54 | 1.34 | 0.667 | 0.667 | 1.00 | n<30 |
| ts | L3 | 1035 | 861 | 785 | 49.20 | 4.38 | 5.16 | 44.10 | 5.19 | 44.82 | 5.54 | 0.791 | 0.242 | 0.170 | 0.031 | pass |
| ts | L2 | 1087 | 813 | 623 | 46.60 | 3.94 | 5.29 | 42.20 | 4.54 | 42.98 | 5.54 | 0.711 | 0.427 | 0.258 | 0.040 | FAIL: flagged 43 % |
| ts | L1 | 1124 | 863 | 664 | 45.45 | 4.11 | 5.52 | 40.70 | 4.71 | 41.09 | 5.54 | 0.742 | 0.409 | 0.250 | 0.047 | FAIL: flagged 41 % |
| ts | T12 | 1135 | 874 | 770 | 44.72 | 4.61 | 5.49 | 39.90 | 4.97 | 35.63 | 5.54 | 0.832 | 0.322 | 0.317 | 0.053 | pass |
| ts | T11 | 1102 | 857 | 697 | 42.58 | 4.13 | 5.29 | 37.60 | 4.67 | - | 5.54 | 0.746 | 0.368 | - | 0.062 | pass |
| ts | aboveT11 | 2469 | 1425 | 1405 | 39.83 | 5.53 | 5.85 | - | - | - | 5.54 | 0.998 | 0.431 | - | 0.142 | info (no atlas row above T11) |
| ts | pooled | 5523 | 4282 | 3551 | 45.89 | 4.91 | 5.79 | - | - | - | 5.54 | 0.886 | 0.357 | - | 0.054 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| v11 | L3 | 747 | 680 | 636 | 48.77 | 4.22 | 4.73 | 44.10 | 5.19 | 44.82 | 5.54 | 0.762 | 0.149 | 0.090 | 0.000 | pass |
| v11 | L2 | 774 | 638 | 494 | 46.25 | 3.67 | 5.17 | 42.20 | 4.54 | 42.98 | 5.54 | 0.662 | 0.362 | 0.177 | 0.000 | pass |
| v11 | L1 | 790 | 654 | 531 | 45.09 | 3.71 | 4.98 | 40.70 | 4.71 | 41.09 | 5.54 | 0.669 | 0.328 | 0.191 | 0.000 | pass |
| v11 | T12 | 796 | 657 | 584 | 44.14 | 4.25 | 5.14 | 39.90 | 4.97 | 35.63 | 5.54 | 0.767 | 0.266 | 0.264 | 0.000 | pass |
| v11 | T11 | 777 | 638 | 525 | 42.13 | 3.91 | 5.22 | 37.60 | 4.67 | - | 5.54 | 0.706 | 0.324 | - | 0.000 | pass |
| v11 | aboveT11 | 1449 | 755 | 754 | 41.34 | 5.06 | 5.10 | - | - | - | 5.54 | 0.914 | 0.480 | - | 0.000 | info (no atlas row above T11) |
| v11 | pooled | 3884 | 3267 | 2770 | 45.53 | 4.60 | 5.44 | - | - | - | 5.54 | 0.831 | 0.287 | - | 0.000 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| versefusion | L5 | 60 | 55 | 55 | 51.09 | 4.73 | 4.73 | - | - | 48.81 | 5.54 | 0.853 | 0.083 | 0.083 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L4 | 111 | 91 | 91 | 52.09 | 4.71 | 4.71 | 47.00 | 5.61 | 47.50 | 5.54 | 0.850 | 0.180 | 0.180 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L3 | 143 | 117 | 116 | 50.79 | 5.26 | 5.31 | 44.10 | 5.19 | 44.82 | 5.54 | 0.949 | 0.189 | 0.182 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L2 | 166 | 131 | 129 | 49.97 | 5.08 | 5.82 | 42.20 | 4.54 | 42.98 | 5.54 | 0.917 | 0.223 | 0.223 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L1 | 204 | 162 | 161 | 48.36 | 6.56 | 6.76 | 40.70 | 4.71 | 41.09 | 5.54 | 1.19 | 0.211 | 0.240 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | T12 | 295 | 243 | 237 | 47.61 | 7.58 | 8.31 | 39.90 | 4.97 | 35.63 | 5.54 | 1.37 | 0.197 | 0.349 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | T11 | 317 | 265 | 260 | 46.84 | 7.37 | 7.75 | 37.60 | 4.67 | - | 5.54 | 1.33 | 0.180 | - | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | aboveT11 | 1518 | 1237 | 1213 | 41.99 | 7.29 | 7.68 | - | - | - | 5.54 | 1.32 | 0.201 | - | 1.00 | info (no atlas row above T11) |
| versefusion | pooled | 1296 | 1064 | 1049 | 48.70 | 6.83 | 7.28 | - | - | - | 5.54 | 1.23 | 0.191 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |

### EPDu -- NO_YARDSTICK (no atlas row and no published SD for end-plate depth in level_references.csv; own p1/p99 only, and the high side is permissive because the release table carries the displaced inferior-posterior corner on some records (VBHp p99 44 mm at L1) | )

| family | level | n_measured | n_prebit | n_pass | median_pass | sd_pass | sd_prebit | atlas_median | atlas_sd | pub_mean | pub_sd | sd_ratio | flagged(atlas) | flagged(pub) | rib% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctspine1k | L4 | 1 | 1 | 1 | 31.35 | - | - | 34.66 | 5.16 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | L3 | 1 | 1 | 1 | 29.97 | - | - | 32.12 | 5.42 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | L2 | 1 | 1 | 1 | 27.54 | - | - | 29.64 | 6.23 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | L1 | 2 | 2 | 2 | 28.02 | - | - | 28.05 | 6.08 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | T12 | 3 | 3 | 3 | 34.39 | 5.10 | 5.10 | 28.45 | 6.18 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | T11 | 3 | 3 | 3 | 31.78 | 6.13 | 6.13 | - | - | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | aboveT11 | 19 | 17 | 17 | 27.25 | 2.44 | 2.44 | - | - | - | - | - | 0.105 | - | 1.00 | info (no atlas row above T11) |
| ctspine1k | pooled | 11 | 11 | 11 | 31.35 | 4.68 | 4.68 | - | - | - | - | - | 0.000 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| spineps | L5 | 872 | 801 | 795 | 36.57 | 3.75 | 3.97 | 36.27 | 4.89 | - | - | - | 0.088 | - | 0.125 | NO_YARDSTICK |
| spineps | L4 | 941 | 865 | 857 | 34.81 | 4.32 | 4.56 | 34.66 | 5.16 | - | - | - | 0.089 | - | 0.143 | NO_YARDSTICK |
| spineps | L3 | 961 | 863 | 851 | 32.66 | 4.44 | 4.80 | 32.12 | 5.42 | - | - | - | 0.114 | - | 0.161 | NO_YARDSTICK |
| spineps | L2 | 999 | 807 | 799 | 30.41 | 4.83 | 5.01 | 29.64 | 6.23 | - | - | - | 0.200 | - | 0.193 | NO_YARDSTICK |
| spineps | L1 | 1023 | 837 | 833 | 28.91 | 4.79 | 4.96 | 28.05 | 6.08 | - | - | - | 0.186 | - | 0.213 | NO_YARDSTICK |
| spineps | T12 | 1150 | 912 | 901 | 29.96 | 5.35 | 5.51 | 28.45 | 6.18 | - | - | - | 0.217 | - | 0.302 | NO_YARDSTICK |
| spineps | T11 | 1135 | 916 | 906 | 30.77 | 5.29 | 5.57 | - | - | - | - | - | 0.202 | - | 0.304 | NO_YARDSTICK |
| spineps | aboveT11 | 3289 | 2046 | 1948 | 31.46 | 5.04 | 5.92 | - | - | - | - | - | 0.408 | - | 0.529 | info (no atlas row above T11) |
| spineps | pooled | 7081 | 6001 | 5942 | 32.27 | 5.35 | 5.56 | - | - | - | - | - | 0.161 | - | 0.212 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| ts | L5 | 1111 | 955 | 946 | 36.98 | 3.90 | 4.12 | 36.27 | 4.89 | - | - | - | 0.149 | - | 0.015 | NO_YARDSTICK |
| ts | L4 | 1118 | 989 | 976 | 35.30 | 4.37 | 4.79 | 34.66 | 5.16 | - | - | - | 0.127 | - | 0.022 | NO_YARDSTICK |
| ts | L3 | 1124 | 926 | 912 | 32.47 | 4.48 | 4.91 | 32.12 | 5.42 | - | - | - | 0.189 | - | 0.029 | NO_YARDSTICK |
| ts | L2 | 1134 | 847 | 835 | 30.18 | 4.55 | 4.76 | 29.64 | 6.23 | - | - | - | 0.264 | - | 0.041 | NO_YARDSTICK |
| ts | L1 | 1144 | 878 | 868 | 28.86 | 4.37 | 4.60 | 28.05 | 6.08 | - | - | - | 0.241 | - | 0.048 | NO_YARDSTICK |
| ts | T12 | 1145 | 882 | 868 | 29.13 | 4.73 | 5.01 | 28.45 | 6.18 | - | - | - | 0.242 | - | 0.054 | NO_YARDSTICK |
| ts | T11 | 1117 | 869 | 856 | 30.50 | 4.97 | 5.29 | - | - | - | - | - | 0.234 | - | 0.067 | NO_YARDSTICK |
| ts | aboveT11 | 2532 | 1454 | 1367 | 31.13 | 5.47 | 6.45 | - | - | - | - | - | 0.460 | - | 0.159 | info (no atlas row above T11) |
| ts | pooled | 7893 | 6346 | 6261 | 32.18 | 5.35 | 5.63 | - | - | - | - | - | 0.207 | - | 0.040 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| v11 | L5 | 802 | 736 | 732 | 36.29 | 3.79 | 3.97 | 36.27 | 4.89 | - | - | - | 0.087 | - | 0.000 | NO_YARDSTICK |
| v11 | L4 | 802 | 761 | 747 | 34.75 | 4.31 | 4.91 | 34.66 | 5.16 | - | - | - | 0.069 | - | 0.000 | NO_YARDSTICK |
| v11 | L3 | 802 | 729 | 719 | 32.29 | 4.47 | 4.77 | 32.12 | 5.42 | - | - | - | 0.103 | - | 0.000 | NO_YARDSTICK |
| v11 | L2 | 802 | 660 | 656 | 29.61 | 4.54 | 4.71 | 29.64 | 6.23 | - | - | - | 0.182 | - | 0.000 | NO_YARDSTICK |
| v11 | L1 | 802 | 665 | 663 | 27.95 | 4.56 | 4.69 | 28.05 | 6.08 | - | - | - | 0.173 | - | 0.000 | NO_YARDSTICK |
| v11 | T12 | 800 | 661 | 655 | 28.29 | 4.75 | 4.91 | 28.45 | 6.18 | - | - | - | 0.181 | - | 0.000 | NO_YARDSTICK |
| v11 | T11 | 783 | 644 | 638 | 29.84 | 5.11 | 5.28 | - | - | - | - | - | 0.185 | - | 0.000 | NO_YARDSTICK |
| v11 | aboveT11 | 1456 | 757 | 755 | 31.45 | 5.11 | 5.22 | - | - | - | - | - | 0.481 | - | 0.000 | info (no atlas row above T11) |
| v11 | pooled | 5593 | 4856 | 4810 | 31.95 | 5.39 | 5.59 | - | - | - | - | - | 0.140 | - | 0.000 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| versefusion | L5 | 112 | 93 | 92 | 37.19 | 4.41 | 4.93 | 36.27 | 4.89 | - | - | - | 0.179 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | L4 | 137 | 113 | 111 | 36.22 | 4.93 | 5.52 | 34.66 | 5.16 | - | - | - | 0.190 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | L3 | 170 | 138 | 138 | 34.81 | 5.22 | 5.22 | 32.12 | 5.42 | - | - | - | 0.188 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | L2 | 199 | 154 | 152 | 33.62 | 5.51 | 5.79 | 29.64 | 6.23 | - | - | - | 0.236 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | L1 | 234 | 183 | 179 | 32.15 | 5.36 | 5.77 | 28.05 | 6.08 | - | - | - | 0.235 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | T12 | 358 | 289 | 277 | 33.02 | 6.05 | 6.65 | 28.45 | 6.18 | - | - | - | 0.226 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | T11 | 347 | 287 | 275 | 32.67 | 5.69 | 6.47 | - | - | - | - | - | 0.207 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | aboveT11 | 1609 | 1291 | 1171 | 31.14 | 5.19 | 6.61 | - | - | - | - | - | 0.272 | - | 1.00 | info (no atlas row above T11) |
| versefusion | pooled | 1557 | 1257 | 1224 | 33.83 | 5.70 | 6.25 | - | - | - | - | - | 0.214 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |

### EPDl -- NO_YARDSTICK (no atlas row and no published SD for end-plate depth in level_references.csv; own p1/p99 only, and the high side is permissive because the release table carries the displaced inferior-posterior corner on some records (VBHp p99 44 mm at L1) | )

| family | level | n_measured | n_prebit | n_pass | median_pass | sd_pass | sd_prebit | atlas_median | atlas_sd | pub_mean | pub_sd | sd_ratio | flagged(atlas) | flagged(pub) | rib% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctspine1k | L4 | 1 | 1 | 1 | 26.69 | - | - | 33.30 | 4.86 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | L3 | 1 | 1 | 1 | 28.56 | - | - | 35.47 | 5.50 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | L2 | 1 | 1 | 1 | 31.07 | - | - | 36.28 | 6.28 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | L1 | 2 | 2 | 2 | 28.35 | - | - | 35.03 | 6.36 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | T12 | 3 | 3 | 3 | 29.18 | 0.444 | 0.444 | 33.80 | 5.68 | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | T11 | 3 | 3 | 3 | 31.04 | 2.43 | 2.43 | - | - | - | - | - | 0.000 | - | 1.00 | n<30 |
| ctspine1k | aboveT11 | 19 | 17 | 17 | 28.31 | 2.31 | 2.31 | - | - | - | - | - | 0.105 | - | 1.00 | info (no atlas row above T11) |
| ctspine1k | pooled | 11 | 11 | 11 | 29.18 | 2.01 | 2.01 | - | - | - | - | - | 0.000 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| spineps | L5 | 872 | 801 | 795 | 29.46 | 4.11 | 4.26 | 29.69 | 5.27 | - | - | - | 0.088 | - | 0.125 | NO_YARDSTICK |
| spineps | L4 | 941 | 865 | 854 | 33.10 | 3.81 | 4.20 | 33.30 | 4.86 | - | - | - | 0.092 | - | 0.143 | NO_YARDSTICK |
| spineps | L3 | 961 | 863 | 848 | 35.04 | 4.06 | 4.40 | 35.47 | 5.50 | - | - | - | 0.118 | - | 0.161 | NO_YARDSTICK |
| spineps | L2 | 999 | 807 | 799 | 36.03 | 4.37 | 4.66 | 36.28 | 6.28 | - | - | - | 0.200 | - | 0.193 | NO_YARDSTICK |
| spineps | L1 | 1023 | 837 | 824 | 34.97 | 4.46 | 4.79 | 35.03 | 6.36 | - | - | - | 0.195 | - | 0.213 | NO_YARDSTICK |
| spineps | T12 | 1150 | 912 | 895 | 33.84 | 4.22 | 4.67 | 33.80 | 5.68 | - | - | - | 0.222 | - | 0.302 | NO_YARDSTICK |
| spineps | T11 | 1135 | 916 | 897 | 33.59 | 4.73 | 5.37 | - | - | - | - | - | 0.210 | - | 0.304 | NO_YARDSTICK |
| spineps | aboveT11 | 3289 | 2046 | 1911 | 33.85 | 5.08 | 6.51 | - | - | - | - | - | 0.419 | - | 0.529 | info (no atlas row above T11) |
| spineps | pooled | 7081 | 6001 | 5912 | 33.86 | 4.68 | 5.02 | - | - | - | - | - | 0.165 | - | 0.212 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| ts | L5 | 1111 | 955 | 949 | 29.78 | 4.14 | 4.26 | 29.69 | 5.27 | - | - | - | 0.146 | - | 0.015 | NO_YARDSTICK |
| ts | L4 | 1118 | 989 | 975 | 33.67 | 3.80 | 4.24 | 33.30 | 4.86 | - | - | - | 0.128 | - | 0.022 | NO_YARDSTICK |
| ts | L3 | 1124 | 926 | 904 | 35.50 | 4.02 | 4.93 | 35.47 | 5.50 | - | - | - | 0.196 | - | 0.029 | NO_YARDSTICK |
| ts | L2 | 1134 | 847 | 833 | 36.78 | 4.23 | 4.75 | 36.28 | 6.28 | - | - | - | 0.265 | - | 0.041 | NO_YARDSTICK |
| ts | L1 | 1144 | 878 | 854 | 35.63 | 4.50 | 5.18 | 35.03 | 6.36 | - | - | - | 0.253 | - | 0.048 | NO_YARDSTICK |
| ts | T12 | 1145 | 882 | 859 | 34.32 | 4.24 | 4.91 | 33.80 | 5.68 | - | - | - | 0.250 | - | 0.054 | NO_YARDSTICK |
| ts | T11 | 1117 | 869 | 852 | 34.08 | 4.61 | 5.20 | - | - | - | - | - | 0.237 | - | 0.067 | NO_YARDSTICK |
| ts | aboveT11 | 2532 | 1454 | 1318 | 33.39 | 5.28 | 7.19 | - | - | - | - | - | 0.479 | - | 0.159 | info (no atlas row above T11) |
| ts | pooled | 7893 | 6346 | 6226 | 34.19 | 4.72 | 5.18 | - | - | - | - | - | 0.211 | - | 0.040 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| v11 | L5 | 802 | 736 | 729 | 29.52 | 4.11 | 4.30 | 29.69 | 5.27 | - | - | - | 0.091 | - | 0.000 | NO_YARDSTICK |
| v11 | L4 | 802 | 761 | 755 | 33.18 | 3.75 | 4.10 | 33.30 | 4.86 | - | - | - | 0.059 | - | 0.000 | NO_YARDSTICK |
| v11 | L3 | 802 | 729 | 718 | 35.23 | 3.84 | 4.33 | 35.47 | 5.50 | - | - | - | 0.105 | - | 0.000 | NO_YARDSTICK |
| v11 | L2 | 802 | 660 | 654 | 36.40 | 4.24 | 4.44 | 36.28 | 6.28 | - | - | - | 0.185 | - | 0.000 | NO_YARDSTICK |
| v11 | L1 | 802 | 665 | 662 | 35.23 | 4.53 | 4.57 | 35.03 | 6.36 | - | - | - | 0.175 | - | 0.000 | NO_YARDSTICK |
| v11 | T12 | 800 | 661 | 658 | 33.88 | 4.20 | 4.23 | 33.80 | 5.68 | - | - | - | 0.177 | - | 0.000 | NO_YARDSTICK |
| v11 | T11 | 783 | 644 | 644 | 33.69 | 4.72 | 4.72 | - | - | - | - | - | 0.178 | - | 0.000 | NO_YARDSTICK |
| v11 | aboveT11 | 1456 | 757 | 757 | 34.16 | 4.80 | 4.80 | - | - | - | - | - | 0.480 | - | 0.000 | info (no atlas row above T11) |
| v11 | pooled | 5593 | 4856 | 4820 | 33.88 | 4.71 | 4.87 | - | - | - | - | - | 0.138 | - | 0.000 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| versefusion | L5 | 112 | 93 | 89 | 31.70 | 4.22 | 5.21 | 29.69 | 5.27 | - | - | - | 0.205 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | L4 | 137 | 113 | 111 | 33.20 | 4.83 | 5.34 | 33.30 | 4.86 | - | - | - | 0.190 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | L3 | 170 | 138 | 136 | 34.83 | 5.12 | 5.40 | 35.47 | 5.50 | - | - | - | 0.200 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | L2 | 199 | 154 | 148 | 35.09 | 4.74 | 5.87 | 36.28 | 6.28 | - | - | - | 0.256 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | L1 | 234 | 183 | 176 | 35.11 | 4.66 | 5.75 | 35.03 | 6.36 | - | - | - | 0.248 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | T12 | 358 | 289 | 260 | 33.52 | 4.72 | 6.74 | 33.80 | 5.68 | - | - | - | 0.274 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | T11 | 347 | 287 | 259 | 33.81 | 4.42 | 6.45 | - | - | - | - | - | 0.254 | - | 1.00 | info (rib-keyed level, not the atlas level): NO_YARDSTICK |
| versefusion | aboveT11 | 1609 | 1291 | 1117 | 33.72 | 5.09 | 7.64 | - | - | - | - | - | 0.306 | - | 1.00 | info (no atlas row above T11) |
| versefusion | pooled | 1557 | 1257 | 1179 | 33.99 | 4.74 | 6.16 | - | - | - | - | - | 0.243 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |

### SCW -- pass (widest published SD 5.9 (Chaudhary 2015 L5 M (n=300, adults, Indian)))

| family | level | n_measured | n_prebit | n_pass | median_pass | sd_pass | sd_prebit | atlas_median | atlas_sd | pub_mean | pub_sd | sd_ratio | flagged(atlas) | flagged(pub) | rib% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctspine1k | L4 | 1 | 1 | 1 | 23.17 | - | - | 26.20 | 3.02 | 23.19 | 5.90 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L3 | 1 | 1 | 1 | 22.18 | - | - | 25.00 | 2.61 | 22.62 | 5.90 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L2 | 1 | 1 | 1 | 21.18 | - | - | 24.20 | 2.38 | 22.15 | 5.90 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | L1 | 2 | 2 | 2 | 24.99 | - | - | 23.90 | 2.46 | 22.04 | 5.90 | - | 0.000 | 0.000 | 1.00 | n<30 |
| ctspine1k | T12 | 3 | 3 | 3 | 23.01 | 2.22 | 2.22 | 23.10 | 2.47 | - | 5.90 | 0.376 | 0.000 | - | 1.00 | n<30 |
| ctspine1k | T11 | 3 | 3 | 3 | 20.04 | 3.80 | 3.80 | 20.30 | 2.46 | - | 5.90 | 0.645 | 0.000 | - | 1.00 | n<30 |
| ctspine1k | aboveT11 | 17 | 17 | 16 | 17.13 | 2.69 | 2.83 | - | - | - | 5.90 | 0.457 | 0.059 | - | 1.00 | info (no atlas row above T11) |
| ctspine1k | pooled | 11 | 11 | 11 | 22.18 | 2.98 | 2.98 | - | - | - | 5.90 | 0.506 | 0.000 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| spineps | L5 | 848 | 801 | 788 | 29.76 | 3.69 | 4.07 | 30.00 | 3.75 | 26.46 | 5.90 | 0.626 | 0.071 | 0.060 | 0.124 | pass |
| spineps | L4 | 893 | 865 | 844 | 26.56 | 2.81 | 3.14 | 26.20 | 3.02 | 23.19 | 5.90 | 0.477 | 0.055 | 0.032 | 0.141 | pass |
| spineps | L3 | 891 | 863 | 850 | 25.43 | 2.61 | 2.90 | 25.00 | 2.61 | 22.62 | 5.90 | 0.443 | 0.046 | 0.033 | 0.165 | pass |
| spineps | L2 | 838 | 807 | 793 | 24.23 | 2.60 | 2.77 | 24.20 | 2.38 | 22.15 | 5.90 | 0.441 | 0.054 | 0.037 | 0.205 | pass |
| spineps | L1 | 870 | 837 | 828 | 23.99 | 2.65 | 2.79 | 23.90 | 2.46 | 22.04 | 5.90 | 0.448 | 0.048 | 0.038 | 0.224 | pass |
| spineps | T12 | 999 | 912 | 902 | 23.44 | 3.27 | 3.35 | 23.10 | 2.47 | - | 5.90 | 0.554 | 0.097 | - | 0.313 | pass |
| spineps | T11 | 1052 | 916 | 903 | 20.70 | 3.33 | 3.43 | 20.30 | 2.46 | - | 5.90 | 0.564 | 0.142 | - | 0.296 | pass |
| spineps | aboveT11 | 2794 | 2046 | 1985 | 18.95 | 3.63 | 3.74 | - | - | - | 5.90 | 0.615 | 0.290 | - | 0.545 | info (no atlas row above T11) |
| spineps | pooled | 6391 | 6001 | 5908 | 24.66 | 3.98 | 4.18 | - | - | - | 5.90 | 0.674 | 0.076 | - | 0.214 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| ts | L5 | 1062 | 955 | 934 | 30.00 | 3.76 | 4.46 | 30.00 | 3.75 | 26.46 | 5.90 | 0.637 | 0.121 | 0.108 | 0.010 | pass |
| ts | L4 | 1043 | 989 | 969 | 26.14 | 2.92 | 3.30 | 26.20 | 3.02 | 23.19 | 5.90 | 0.495 | 0.071 | 0.053 | 0.016 | pass |
| ts | L3 | 1021 | 926 | 915 | 25.20 | 2.60 | 2.79 | 25.00 | 2.61 | 22.62 | 5.90 | 0.441 | 0.104 | 0.093 | 0.026 | pass |
| ts | L2 | 914 | 847 | 823 | 24.22 | 2.40 | 2.84 | 24.20 | 2.38 | 22.15 | 5.90 | 0.407 | 0.100 | 0.073 | 0.040 | pass |
| ts | L1 | 943 | 878 | 851 | 24.00 | 2.54 | 2.93 | 23.90 | 2.46 | 22.04 | 5.90 | 0.431 | 0.098 | 0.069 | 0.048 | pass |
| ts | T12 | 956 | 882 | 852 | 22.66 | 2.59 | 3.03 | 23.10 | 2.47 | - | 5.90 | 0.439 | 0.109 | - | 0.053 | pass |
| ts | T11 | 1014 | 869 | 852 | 20.00 | 2.64 | 2.79 | 20.30 | 2.46 | - | 5.90 | 0.448 | 0.160 | - | 0.064 | pass |
| ts | aboveT11 | 2126 | 1454 | 1387 | 18.00 | 3.08 | 3.28 | - | - | - | 5.90 | 0.522 | 0.348 | - | 0.159 | info (no atlas row above T11) |
| ts | pooled | 6953 | 6346 | 6196 | 24.43 | 4.03 | 4.34 | - | - | - | 5.90 | 0.683 | 0.109 | - | 0.036 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| v11 | L5 | 775 | 736 | 725 | 30.08 | 3.63 | 3.99 | 30.00 | 3.75 | 26.46 | 5.90 | 0.615 | 0.065 | 0.054 | 0.000 | pass |
| v11 | L4 | 767 | 761 | 748 | 26.37 | 2.74 | 3.04 | 26.20 | 3.02 | 23.19 | 5.90 | 0.465 | 0.025 | 0.009 | 0.000 | pass |
| v11 | L3 | 735 | 729 | 722 | 25.23 | 2.32 | 2.50 | 25.00 | 2.61 | 22.62 | 5.90 | 0.393 | 0.018 | 0.008 | 0.000 | pass |
| v11 | L2 | 662 | 660 | 651 | 24.27 | 2.19 | 2.37 | 24.20 | 2.38 | 22.15 | 5.90 | 0.371 | 0.017 | 0.003 | 0.000 | pass |
| v11 | L1 | 669 | 665 | 658 | 23.91 | 2.29 | 2.39 | 23.90 | 2.46 | 22.04 | 5.90 | 0.388 | 0.016 | 0.006 | 0.000 | pass |
| v11 | T12 | 682 | 661 | 652 | 23.13 | 2.32 | 2.43 | 23.10 | 2.47 | - | 5.90 | 0.393 | 0.044 | - | 0.000 | pass |
| v11 | T11 | 735 | 644 | 636 | 20.23 | 2.32 | 2.43 | 20.30 | 2.46 | - | 5.90 | 0.393 | 0.135 | - | 0.000 | pass |
| v11 | aboveT11 | 1183 | 757 | 741 | 17.97 | 2.12 | 2.19 | - | - | - | 5.90 | 0.360 | 0.374 | - | 0.000 | info (no atlas row above T11) |
| v11 | pooled | 5025 | 4856 | 4792 | 24.61 | 3.89 | 4.07 | - | - | - | 5.90 | 0.659 | 0.046 | - | 0.000 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| versefusion | L5 | 112 | 93 | 93 | 28.73 | 3.83 | 3.83 | 30.00 | 3.75 | 26.46 | 5.90 | 0.650 | 0.170 | 0.170 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L4 | 128 | 113 | 113 | 26.81 | 3.53 | 3.53 | 26.20 | 3.02 | 23.19 | 5.90 | 0.598 | 0.117 | 0.117 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L3 | 163 | 138 | 136 | 25.85 | 3.37 | 3.78 | 25.00 | 2.61 | 22.62 | 5.90 | 0.571 | 0.166 | 0.153 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L2 | 182 | 154 | 152 | 24.64 | 3.77 | 3.96 | 24.20 | 2.38 | 22.15 | 5.90 | 0.639 | 0.165 | 0.154 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L1 | 211 | 183 | 183 | 24.00 | 3.48 | 3.48 | 23.90 | 2.46 | 22.04 | 5.90 | 0.589 | 0.133 | 0.133 | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | T12 | 335 | 289 | 289 | 24.00 | 4.57 | 4.57 | 23.10 | 2.47 | - | 5.90 | 0.775 | 0.137 | - | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | T11 | 321 | 287 | 287 | 22.00 | 3.99 | 3.99 | 20.30 | 2.46 | - | 5.90 | 0.676 | 0.106 | - | 1.00 | info (rib-keyed level, not the atlas level): pass |
| versefusion | aboveT11 | 1470 | 1291 | 1243 | 20.24 | 3.99 | 4.21 | - | - | - | 5.90 | 0.677 | 0.154 | - | 1.00 | info (no atlas row above T11) |
| versefusion | pooled | 1452 | 1257 | 1253 | 24.55 | 4.32 | 4.37 | - | - | - | 5.90 | 0.732 | 0.137 | - | 1.00 | info (pooled over L1-T11: between-level spread included, not a verdict) |

### SCD -- pass (widest published SD 3.76 (Griffith 2016 L5 M (n=1080, adults, Hong Kong Chinese)))

| family | level | n_measured | n_prebit | n_pass | median_pass | sd_pass | sd_prebit | atlas_median | atlas_sd | pub_mean | pub_sd | sd_ratio | flagged(atlas) | flagged(pub) | rib% | below11.07(maskpass) | below11.07(all) | x2.62% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ctspine1k | L4 | 1 | 1 | 1 | 16.55 | - | - | 16.60 | 2.01 | 15.06 | 3.76 | - | 0.000 | 0.000 | 1.00 | 0.000 | 0.000 | 0.000 | n<30 |
| ctspine1k | L3 | 1 | 1 | 1 | 15.23 | - | - | 16.40 | 1.71 | 14.69 | 3.76 | - | 0.000 | 0.000 | 1.00 | 0.000 | 0.000 | 0.000 | n<30 |
| ctspine1k | L2 | 1 | 1 | 1 | 13.90 | - | - | 17.20 | 1.72 | 15.08 | 3.76 | - | 0.000 | 0.000 | 1.00 | 0.000 | 0.000 | 0.000 | n<30 |
| ctspine1k | L1 | 2 | 2 | 2 | 14.77 | - | - | 17.70 | 1.66 | 16.02 | 3.76 | - | 0.000 | 0.000 | 1.00 | 0.000 | 0.000 | 0.000 | n<30 |
| ctspine1k | T12 | 3 | 3 | 3 | 14.23 | 2.29 | 2.29 | 17.80 | 1.55 | 16.26 | 3.76 | 0.608 | 0.000 | 0.000 | 1.00 | 0.000 | 0.000 | 0.000 | n<30 |
| ctspine1k | T11 | 3 | 3 | 3 | 14.56 | 3.05 | 3.05 | 16.60 | 1.57 | - | 3.76 | 0.810 | 0.000 | - | 1.00 | 0.000 | 0.000 | 0.000 | n<30 |
| ctspine1k | aboveT11 | 17 | 17 | 15 | 14.58 | 2.20 | 2.31 | - | - | - | 3.76 | 0.586 | 0.118 | - | 1.00 | 0.000 | 0.000 | 0.000 | info (no atlas row above T11) |
| ctspine1k | pooled | 11 | 11 | 11 | 14.56 | 1.84 | 1.84 | - | - | - | 3.76 | 0.490 | 0.000 | - | 1.00 | 0.000 | 0.000 | 0.000 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| spineps | L5 | 848 | 801 | 783 | 17.11 | 2.39 | 2.84 | 17.40 | 2.74 | 15.69 | 3.76 | 0.635 | 0.077 | 0.066 | 0.124 | 0.001 | 0.004 | 0.048 | pass |
| spineps | L4 | 893 | 865 | 848 | 16.41 | 1.82 | 2.00 | 16.60 | 2.01 | 15.06 | 3.76 | 0.484 | 0.050 | 0.032 | 0.141 | 0.001 | 0.001 | 0.044 | pass |
| spineps | L3 | 891 | 863 | 848 | 16.45 | 1.62 | 1.74 | 16.40 | 1.71 | 14.69 | 3.76 | 0.430 | 0.048 | 0.031 | 0.165 | 0.002 | 0.002 | 0.088 | pass |
| spineps | L2 | 838 | 807 | 793 | 17.23 | 1.65 | 1.80 | 17.20 | 1.72 | 15.08 | 3.76 | 0.439 | 0.054 | 0.037 | 0.205 | 0.004 | 0.006 | 0.142 | pass |
| spineps | L1 | 870 | 837 | 824 | 17.77 | 1.51 | 1.66 | 17.70 | 1.66 | 16.02 | 3.76 | 0.403 | 0.053 | 0.038 | 0.224 | 0.001 | 0.002 | 0.046 | pass |
| spineps | T12 | 999 | 912 | 898 | 17.71 | 1.58 | 1.70 | 17.80 | 1.55 | 16.26 | 3.76 | 0.419 | 0.101 | 0.088 | 0.313 | 0.000 | 0.001 | 0.000 | pass |
| spineps | T11 | 1052 | 916 | 897 | 16.48 | 1.57 | 1.78 | 16.60 | 1.57 | - | 3.76 | 0.418 | 0.147 | - | 0.296 | 0.001 | 0.003 | 0.042 | pass |
| spineps | aboveT11 | 2794 | 2046 | 1997 | 15.62 | 1.74 | 1.89 | - | - | - | 3.76 | 0.463 | 0.285 | - | 0.545 | 0.004 | 0.009 | 0.149 | info (no atlas row above T11) |
| spineps | pooled | 6391 | 6001 | 5891 | 17.09 | 1.81 | 2.01 | - | - | - | 3.76 | 0.481 | 0.078 | - | 0.214 | 0.001 | 0.003 | 0.057 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| ts | L5 | 1062 | 955 | 930 | 17.54 | 2.47 | 3.02 | 17.40 | 2.74 | 15.69 | 3.76 | 0.657 | 0.124 | 0.112 | 0.010 | 0.005 | 0.007 | 0.200 | pass |
| ts | L4 | 1043 | 989 | 959 | 16.41 | 1.93 | 2.20 | 16.60 | 2.01 | 15.06 | 3.76 | 0.513 | 0.081 | 0.053 | 0.016 | 0.003 | 0.004 | 0.116 | pass |
| ts | L3 | 1021 | 926 | 893 | 16.62 | 1.63 | 1.91 | 16.40 | 1.71 | 14.69 | 3.76 | 0.434 | 0.125 | 0.094 | 0.026 | 0.002 | 0.002 | 0.082 | pass |
| ts | L2 | 914 | 847 | 818 | 17.77 | 1.67 | 2.00 | 17.20 | 1.72 | 15.08 | 3.76 | 0.444 | 0.105 | 0.073 | 0.040 | 0.005 | 0.011 | 0.180 | pass |
| ts | L1 | 943 | 878 | 847 | 18.00 | 1.54 | 1.96 | 17.70 | 1.66 | 16.02 | 3.76 | 0.410 | 0.102 | 0.070 | 0.048 | 0.006 | 0.008 | 0.217 | pass |
| ts | T12 | 956 | 882 | 854 | 17.97 | 1.51 | 1.68 | 17.80 | 1.55 | 16.26 | 3.76 | 0.401 | 0.107 | 0.077 | 0.053 | 0.000 | 0.002 | 0.000 | pass |
| ts | T11 | 1014 | 869 | 837 | 16.41 | 1.56 | 1.74 | 16.60 | 1.57 | - | 3.76 | 0.415 | 0.175 | - | 0.064 | 0.001 | 0.006 | 0.044 | pass |
| ts | aboveT11 | 2126 | 1454 | 1394 | 15.18 | 1.60 | 1.83 | - | - | - | 3.76 | 0.425 | 0.344 | - | 0.159 | 0.011 | 0.016 | 0.420 | info (no atlas row above T11) |
| ts | pooled | 6953 | 6346 | 6138 | 17.19 | 1.88 | 2.20 | - | - | - | 3.76 | 0.499 | 0.117 | - | 0.036 | 0.003 | 0.006 | 0.120 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| v11 | L5 | 775 | 736 | 724 | 17.23 | 2.35 | 2.64 | 17.40 | 2.74 | 15.69 | 3.76 | 0.624 | 0.066 | 0.055 | 0.000 | 0.001 | 0.003 | 0.052 | pass |
| v11 | L4 | 767 | 761 | 747 | 16.65 | 1.87 | 2.04 | 16.60 | 2.01 | 15.06 | 3.76 | 0.497 | 0.026 | 0.009 | 0.000 | 0.000 | 0.000 | 0.000 | pass |
| v11 | L3 | 735 | 729 | 715 | 16.60 | 1.56 | 1.67 | 16.40 | 1.71 | 14.69 | 3.76 | 0.415 | 0.027 | 0.008 | 0.000 | 0.000 | 0.000 | 0.000 | pass |
| v11 | L2 | 662 | 660 | 645 | 17.52 | 1.54 | 1.75 | 17.20 | 1.72 | 15.08 | 3.76 | 0.410 | 0.026 | 0.003 | 0.000 | 0.002 | 0.002 | 0.058 | pass |
| v11 | L1 | 669 | 665 | 654 | 17.93 | 1.44 | 1.55 | 17.70 | 1.66 | 16.02 | 3.76 | 0.382 | 0.022 | 0.006 | 0.000 | 0.000 | 0.000 | 0.000 | pass |
| v11 | T12 | 682 | 661 | 650 | 17.81 | 1.42 | 1.53 | 17.80 | 1.55 | 16.26 | 3.76 | 0.377 | 0.047 | 0.031 | 0.000 | 0.000 | 0.000 | 0.000 | pass |
| v11 | T11 | 735 | 644 | 630 | 16.80 | 1.47 | 1.58 | 16.60 | 1.57 | - | 3.76 | 0.392 | 0.143 | - | 0.000 | 0.000 | 0.001 | 0.000 | pass |
| v11 | aboveT11 | 1183 | 757 | 742 | 15.62 | 1.46 | 1.52 | - | - | - | 3.76 | 0.387 | 0.373 | - | 0.000 | 0.000 | 0.003 | 0.000 | info (no atlas row above T11) |
| v11 | pooled | 5025 | 4856 | 4765 | 17.19 | 1.77 | 1.93 | - | - | - | 3.76 | 0.470 | 0.052 | - | 0.000 | 0.000 | 0.001 | 0.016 | info (pooled over L1-T11: between-level spread included, not a verdict) |
| versefusion | L5 | 112 | 93 | 91 | 17.43 | 2.78 | 2.87 | 17.40 | 2.74 | 15.69 | 3.76 | 0.740 | 0.188 | 0.170 | 1.00 | 0.000 | 0.000 | 0.000 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L4 | 128 | 113 | 110 | 16.94 | 2.14 | 2.26 | 16.60 | 2.01 | 15.06 | 3.76 | 0.570 | 0.141 | 0.117 | 1.00 | 0.000 | 0.000 | 0.000 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L3 | 163 | 138 | 133 | 17.00 | 2.11 | 2.43 | 16.40 | 1.71 | 14.69 | 3.76 | 0.562 | 0.184 | 0.160 | 1.00 | 0.007 | 0.006 | 0.277 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L2 | 182 | 154 | 148 | 16.92 | 2.09 | 2.86 | 17.20 | 1.72 | 15.08 | 3.76 | 0.555 | 0.187 | 0.159 | 1.00 | 0.013 | 0.022 | 0.496 | info (rib-keyed level, not the atlas level): pass |
| versefusion | L1 | 211 | 183 | 181 | 17.09 | 1.83 | 2.09 | 17.70 | 1.66 | 16.02 | 3.76 | 0.487 | 0.142 | 0.137 | 1.00 | 0.005 | 0.005 | 0.209 | info (rib-keyed level, not the atlas level): pass |
| versefusion | T12 | 335 | 289 | 288 | 17.00 | 2.04 | 2.11 | 17.80 | 1.55 | 16.26 | 3.76 | 0.543 | 0.140 | 0.137 | 1.00 | 0.000 | 0.000 | 0.000 | info (rib-keyed level, not the atlas level): pass |
| versefusion | T11 | 321 | 287 | 286 | 16.77 | 1.78 | 1.80 | 16.60 | 1.57 | - | 3.76 | 0.475 | 0.109 | - | 1.00 | 0.000 | 0.003 | 0.000 | info (rib-keyed level, not the atlas level): pass |
| versefusion | aboveT11 | 1470 | 1291 | 1252 | 16.00 | 1.86 | 2.09 | - | - | - | 3.76 | 0.495 | 0.148 | - | 1.00 | 0.009 | 0.020 | 0.355 | info (no atlas row above T11) |
| versefusion | pooled | 1452 | 1257 | 1237 | 17.00 | 2.06 | 2.27 | - | - | - | 3.76 | 0.548 | 0.148 | - | 1.00 | 0.003 | 0.005 | 0.121 | info (pooled over L1-T11: between-level spread included, not a verdict) |

## (c) Body-cut fallback rate by family, slice thickness and in-plane pitch

| family | axis | bin | n | n_fallback | rate |
|---|---|---|---|---|---|
| ctspine1k | slice_thickness_mm(zoom_S) | <=0.7 | 10 | 0 | 0.000 |
| ctspine1k | slice_thickness_mm(zoom_S) | 0.7-0.9 | 20 | 2 | 0.100 |
| ctspine1k | in_plane_max_mm | <=0.7 | 10 | 0 | 0.000 |
| ctspine1k | in_plane_max_mm | 0.7-0.9 | 20 | 2 | 0.100 |
| ctspine1k | all | all | 30 | 2 | 0.067 |
| spineps | slice_thickness_mm(zoom_S) | <=0.7 | 662 | 26 | 0.039 |
| spineps | slice_thickness_mm(zoom_S) | 0.7-0.9 | 7608 | 825 | 0.108 |
| spineps | slice_thickness_mm(zoom_S) | 0.9-1.3 | 2108 | 320 | 0.152 |
| spineps | slice_thickness_mm(zoom_S) | 1.3-2.1 | 60 | 5 | 0.083 |
| spineps | slice_thickness_mm(zoom_S) | >3.1 | 35 | 28 | 0.800 |
| spineps | in_plane_max_mm | <=0.7 | 2420 | 351 | 0.145 |
| spineps | in_plane_max_mm | 0.7-0.9 | 5722 | 576 | 0.101 |
| spineps | in_plane_max_mm | 0.9-1.3 | 1244 | 187 | 0.150 |
| spineps | in_plane_max_mm | 1.3-2.1 | 671 | 77 | 0.115 |
| spineps | in_plane_max_mm | 2.1-3.1 | 406 | 13 | 0.032 |
| spineps | in_plane_max_mm | >3.1 | 10 | 0 | 0.000 |
| spineps | all | all | 10473 | 1204 | 0.115 |
| ts | slice_thickness_mm(zoom_S) | <=0.7 | 657 | 32 | 0.049 |
| ts | slice_thickness_mm(zoom_S) | 0.7-0.9 | 7609 | 1023 | 0.134 |
| ts | slice_thickness_mm(zoom_S) | 0.9-1.3 | 2110 | 282 | 0.134 |
| ts | slice_thickness_mm(zoom_S) | 1.3-2.1 | 60 | 7 | 0.117 |
| ts | slice_thickness_mm(zoom_S) | >3.1 | 35 | 28 | 0.800 |
| ts | in_plane_max_mm | <=0.7 | 2402 | 399 | 0.166 |
| ts | in_plane_max_mm | 0.7-0.9 | 5713 | 717 | 0.126 |
| ts | in_plane_max_mm | 0.9-1.3 | 1270 | 174 | 0.137 |
| ts | in_plane_max_mm | 1.3-2.1 | 672 | 71 | 0.106 |
| ts | in_plane_max_mm | 2.1-3.1 | 404 | 11 | 0.027 |
| ts | in_plane_max_mm | >3.1 | 10 | 0 | 0.000 |
| ts | all | all | 10471 | 1372 | 0.131 |
| v11 | slice_thickness_mm(zoom_S) | <=0.7 | 36 | 4 | 0.111 |
| v11 | slice_thickness_mm(zoom_S) | 0.7-0.9 | 6712 | 764 | 0.114 |
| v11 | slice_thickness_mm(zoom_S) | 0.9-1.3 | 267 | 41 | 0.154 |
| v11 | slice_thickness_mm(zoom_S) | >3.1 | 35 | 33 | 0.943 |
| v11 | in_plane_max_mm | <=0.7 | 1810 | 282 | 0.156 |
| v11 | in_plane_max_mm | 0.7-0.9 | 4943 | 533 | 0.108 |
| v11 | in_plane_max_mm | 0.9-1.3 | 297 | 27 | 0.091 |
| v11 | all | all | 7050 | 842 | 0.119 |
| versefusion | slice_thickness_mm(zoom_S) | <=0.7 | 605 | 13 | 0.021 |
| versefusion | slice_thickness_mm(zoom_S) | 0.7-0.9 | 868 | 47 | 0.054 |
| versefusion | slice_thickness_mm(zoom_S) | 0.9-1.3 | 1767 | 201 | 0.114 |
| versefusion | slice_thickness_mm(zoom_S) | 1.3-2.1 | 59 | 1 | 0.017 |
| versefusion | in_plane_max_mm | <=0.7 | 592 | 60 | 0.101 |
| versefusion | in_plane_max_mm | 0.7-0.9 | 748 | 36 | 0.048 |
| versefusion | in_plane_max_mm | 0.9-1.3 | 934 | 114 | 0.122 |
| versefusion | in_plane_max_mm | 1.3-2.1 | 631 | 49 | 0.078 |
| versefusion | in_plane_max_mm | 2.1-3.1 | 384 | 3 | 0.008 |
| versefusion | in_plane_max_mm | >3.1 | 10 | 0 | 0.000 |
| versefusion | all | all | 3299 | 262 | 0.079 |
| spineps | corpus | ctsp | 7070 | 832 | 0.118 |
| ts | corpus | ctsp | 7044 | 1000 | 0.142 |
| v11 | corpus | ctsp | 7050 | 842 | 0.119 |
| ctspine1k | corpus | ctspine1k | 30 | 2 | 0.067 |
| spineps | corpus | verse | 3403 | 372 | 0.109 |
| ts | corpus | verse | 3427 | 372 | 0.109 |
| versefusion | corpus | verse | 3299 | 262 | 0.079 |

## (d) Rib evidence sanity

Chord = the longer of the two sides' CT-trace chords (mm). On the ts family reader C's rib call (`rib_bearing_c`, from the TS rib labels) is independent of the trace; elsewhere the trace call is compared with the anatomical level.

- ts: reader C vs trace agreement 93.5 % (both 5160, C only 0, trace only 868, neither 32404); chord on C-bearing p5/p50/p95 = 57.8 / 125.0 / 189.7 (share >= 38: 1.000); chord on C-free with a chord: 10.4 / 30.2 / 160.5 (n 2257, share >= 38: 0.385)
- ctspine1k: 55 instances, 50 with a chord; trace-bearing 40, C-bearing 0, stump (any side) 1, is_rib 0, cut 7; chord on trace-bearing p5/p50/p95 56.5/161.8/207.9 (n 40), on trace-free 11.4/21.2/33.4 (n 10, share 12-38 0.900)
- spineps: 12327 instances, 7539 with a chord; trace-bearing 5400, C-bearing 0, stump (any side) 201, is_rib 0, cut 660; chord on trace-bearing p5/p50/p95 47.8/126.0/193.2 (n 5400), on trace-free 12.0/26.5/35.8 (n 2139, share 12-38 0.950)
- ts: 13391 instances, 7417 with a chord; trace-bearing 6028, C-bearing 5160, stump (any side) 261, is_rib 5160, cut 925; chord on trace-bearing p5/p50/p95 50.0/123.9/190.0 (n 6028), on trace-free 9.5/19.8/35.6 (n 1389, share 12-38 0.845)
- v11: 8111 instances, 4188 with a chord; trace-bearing 3393, C-bearing 2931, stump (any side) 113, is_rib 2931, cut 562; chord on trace-bearing p5/p50/p95 61.7/126.2/183.1 (n 3393), on trace-free 10.0/19.4/34.7 (n 795, share 12-38 0.860)
- versefusion: 4548 instances, 2922 with a chord; trace-bearing 2383, C-bearing 0, stump (any side) 131, is_rib 0, cut 74; chord on trace-bearing p5/p50/p95 44.8/121.4/210.9 (n 2383), on trace-free 11.1/24.0/36.6 (n 539, share 12-38 0.935)

| family | level | n | rib_bearing_trace | stump | is_rib | chord_p50 | chord_n |
|---|---|---|---|---|---|---|---|
| ctspine1k | aboveT11 | 44 | 0.818 | 0.023 | 0.000 | 157.70 | 42 |
| spineps | L5 | 916 | 0.063 | 0.010 | 0.000 | 28.05 | 366 |
| spineps | L4 | 942 | 0.052 | 0.008 | 0.000 | 28.90 | 291 |
| spineps | L3 | 965 | 0.027 | 0.008 | 0.000 | 27.90 | 270 |
| spineps | L2 | 1002 | 0.016 | 0.007 | 0.000 | 27.05 | 264 |
| spineps | L1 | 1027 | 0.018 | 0.033 | 0.000 | 26.50 | 301 |
| spineps | T12 | 1162 | 0.904 | 0.046 | 0.000 | 104.00 | 1084 |
| spineps | T11 | 1145 | 0.818 | 0.016 | 0.000 | 134.45 | 1046 |
| spineps | aboveT11 | 5066 | 0.641 | 0.012 | 0.000 | 122.10 | 3876 |
| ts | L5 | 1115 | 0.046 | 0.043 | 0.017 | 17.75 | 496 |
| ts | L4 | 1122 | 0.043 | 0.004 | 0.006 | 26.75 | 186 |
| ts | L3 | 1133 | 0.043 | 0.006 | 0.007 | 26.00 | 193 |
| ts | L2 | 1144 | 0.041 | 0.005 | 0.007 | 25.10 | 189 |
| ts | L1 | 1148 | 0.056 | 0.034 | 0.015 | 24.40 | 262 |
| ts | T12 | 1168 | 0.941 | 0.061 | 0.920 | 106.60 | 1135 |
| ts | T11 | 1157 | 0.932 | 0.011 | 0.899 | 139.90 | 1088 |
| ts | aboveT11 | 5344 | 0.670 | 0.012 | 0.558 | 122.10 | 3851 |
| v11 | L5 | 802 | 0.076 | 0.036 | 0.019 | 24.70 | 307 |
| v11 | L4 | 802 | 0.054 | 0.002 | 0.004 | 22.15 | 196 |
| v11 | L3 | 802 | 0.031 | 0.004 | 0.005 | 21.30 | 127 |
| v11 | L2 | 802 | 0.020 | 0.001 | 0.005 | 17.95 | 116 |
| v11 | L1 | 802 | 0.027 | 0.025 | 0.020 | 22.10 | 144 |
| v11 | T12 | 801 | 0.931 | 0.061 | 0.928 | 108.40 | 777 |
| v11 | T11 | 796 | 0.948 | 0.005 | 0.920 | 142.70 | 758 |
| v11 | aboveT11 | 2504 | 0.689 | 0.002 | 0.565 | 125.70 | 1763 |
| versefusion | L5 | 112 | 0.000 | 0.036 | 0.000 | 20.60 | 33 |
| versefusion | L4 | 137 | 0.000 | 0.029 | 0.000 | 24.15 | 40 |
| versefusion | L3 | 170 | 0.000 | 0.029 | 0.000 | 24.95 | 38 |
| versefusion | L2 | 199 | 0.000 | 0.015 | 0.000 | 19.20 | 51 |
| versefusion | L1 | 235 | 0.000 | 0.072 | 0.000 | 26.90 | 74 |
| versefusion | T12 | 360 | 1.00 | 0.064 | 0.000 | 93.25 | 360 |
| versefusion | T11 | 349 | 0.544 | 0.032 | 0.000 | 88.00 | 238 |
| versefusion | aboveT11 | 2853 | 0.642 | 0.022 | 0.000 | 118.70 | 2073 |

## (e) Segmenter invariance, CTSP x {v11, spineps, ts}

Per person: n_below_last_rib = instances below the last rib-bearing instance (CT trace / reader C cage), n_rib_bearing = rib-bearing instances in field, sacrum = a sacrum source present. Agreement = the three families equal; Wilson 95 % interval.

| set | quantity | persons | with_3 | comparable | agree | rate | lo | hi |
|---|---|---|---|---|---|---|---|---|
| all_ctsp | n_below_last_rib | 802 | 801 | 769 | 587 | 0.763 | 0.732 | 0.792 |
| all_ctsp | n_rib_bearing | 802 | 801 | 801 | 252 | 0.315 | 0.283 | 0.348 |
| all_ctsp | n_rib_bearing_whole | 802 | 801 | 801 | 530 | 0.662 | 0.628 | 0.694 |
| all_ctsp | sacrum | 802 | 801 | 801 | 801 | 1.00 | 0.995 | 1.000 |
| all_ctsp | n_below_last_rib v11_vs_spineps | 802 |  | 769 | 619 | 0.805 | 0.775 | 0.831 |
| all_ctsp | n_below_last_rib v11_vs_ts | 802 |  | 796 | 737 | 0.926 | 0.906 | 0.942 |
| all_ctsp | n_below_last_rib spineps_vs_ts | 802 |  | 770 | 598 | 0.777 | 0.746 | 0.805 |
| disagree27 | n_below_last_rib | 27 | 26 | 22 | 4 | 0.182 | 0.073 | 0.385 |
| disagree27 | n_rib_bearing | 27 | 26 | 26 | 10 | 0.385 | 0.224 | 0.575 |
| disagree27 | n_rib_bearing_whole | 27 | 26 | 26 | 20 | 0.769 | 0.579 | 0.890 |
| disagree27 | sacrum | 27 | 26 | 26 | 26 | 1.00 | 0.871 | 1.00 |
| disagree27 | n_below_last_rib v11_vs_spineps | 27 |  | 22 | 12 | 0.545 | 0.347 | 0.731 |
| disagree27 | n_below_last_rib v11_vs_ts | 27 |  | 23 | 9 | 0.391 | 0.222 | 0.592 |
| disagree27 | n_below_last_rib spineps_vs_ts | 27 |  | 22 | 10 | 0.455 | 0.269 | 0.653 |
| read33 | n_below_last_rib | 34 | 34 | 31 | 9 | 0.290 | 0.161 | 0.466 |
| read33 | n_rib_bearing | 34 | 34 | 34 | 12 | 0.353 | 0.215 | 0.521 |
| read33 | n_rib_bearing_whole | 34 | 34 | 34 | 23 | 0.676 | 0.508 | 0.809 |
| read33 | sacrum | 34 | 34 | 34 | 34 | 1.00 | 0.898 | 1.00 |
| read33 | n_below_last_rib v11_vs_spineps | 34 |  | 31 | 22 | 0.710 | 0.534 | 0.839 |
| read33 | n_below_last_rib v11_vs_ts | 34 |  | 33 | 13 | 0.394 | 0.247 | 0.563 |
| read33 | n_below_last_rib spineps_vs_ts | 34 |  | 31 | 11 | 0.355 | 0.211 | 0.531 |

The 27 CTSP records where release and SPINEPS disagree on the count (ctsp/build_state.json A != B or one refused): 0005, 0038, 0090, 0097, 0150, 0179, 0208, 0227, 0231, 0268, 0331, 0344, 0349, 0376, 0419, 0486, 0487, 0527, 0601, 0665, 0696, 0787, 1000, 1053, 1090, 1106, 1129. n_rib_bearing counts rib-bearing instances in field and depends on which top instance each segmenter lists (not comparable across families); n_rib_bearing_whole counts only uncut instances. Difference of the rib-based count, spineps minus v11: {0: 619, -4: 35, -3: 7, 1: 40, -5: 55, -1: 3, -2: 3, -6: 2, 2: 2, 3: 1, 5: 2}; ts minus v11: {0: 736, -1: 36, 2: 4, 1: 14, -3: 1, 5: 3, 3: 1}.
Disagreements on n_below_last_rib over all CTSP (case: v11 / spineps / ts): 0004: 5/1/5; 0005: 6/6/5; 0007: 5/2/5; 0010: 5/1/5; 0012: 5/1/5; 0023: 5/1/5; 0027: 5/6/5; 0031: 5/1/5; 0033: 6/6/5; 0038: 5/6/5; 0041: 5/0/5; 0045: 3/0/5; 0049: 5/6/5; 0055: 6/2/6; 0064: 5/0/5; 0065: 6/1/6; 0068: 6/7/5; 0074: 5/2/5; 0079: 5/1/5; 0085: 5/6/5; 0090: 5/6/5; 0094: 5/2/6; 0097: 6/6/5; 0107: 5/0/5; 0119: 5/1/5; 0120: 5/0/5; 0130: 5/0/5; 0133: 5/6/5; 0134: 5/1/5; 0137: 5/6/5; 0138: 5/1/5; 0142: 5/0/5; 0150: 5/6/5; 0151: 4/4/5; 0156: 4/4/5; 0157: 6/6/5; 0158: 5/6/5; 0166: 5/0/5; 0172: 4/4/5; 0179: 6/6/5; 0188: 5/1/5; 0194: 5/1/5; 0196: 5/6/5; 0206: 5/0/5; 0208: 6/6/5; 0211: 5/6/5; 0229: 5/6/5; 0231: 4/5/5; 0234: 6/6/5; 0236: 5/5/4; 0249: 5/1/5; 0251: 5/5/4; 0255: 5/0/5; 0259: 5/0/5; 0260: 5/0/5; 0268: 6/5/5; 0269: 5/0/5; 0271: 5/3/5; 0272: 5/6/5; 0278: 6/1/6 ...

## (f) Label join for J3 (labels_j3.csv)

One row per J1 person; read tier from the plan's truth pools (positives_table.md table B for CTSP, registry.csv + verse/rows.csv for VerSe), the seven contradicted CTSP records and 0068 excluded, VerSe reads contradicted by the scan excluded from that phenotype and listed as label noise, CTSP non-row records presumed ordinary, registry candidates (two-labeller / single-labeller) neither truth nor presumed.

| tier | ls_class | n |
|---|---|---|
| candidate | - | 29 |
| excluded | - | 44 |
| presumed | ordinary | 735 |
| read | LS-4L | 2 |
| read | LS-II | 25 |
| read | LS-L6 | 88 |
| read | LS-SAC | 24 |
| read | ordinary | 182 |

| tier | tl_class | n |
|---|---|---|
| candidate | TL-NA | 29 |
| excluded | TL-NA | 44 |
| presumed | TL-NA | 735 |
| read | TL-0 | 95 |
| read | TL-11 | 8 |
| read | TL-13 | 4 |
| read | TL-H12 | 17 |
| read | TL-LR | 11 |
| read | TL-NA | 186 |

Label noise (excluded from truth): ctsp:0008 ? (read count != release count); ctsp:0021 ? (read count != release count); ctsp:0033 ? (read count != release count); ctsp:0049 ? (read count != release count); ctsp:0176 ? (read count != release count); ctsp:0179 ? (read count != release count); ctsp:0196 ? (read count != release count); verse:verse026 L6 (contradicted (verse/rows.csv)); verse:verse512 L6 (contradicted (verse/rows.csv)); verse:verse540 L6 (contradicted (verse/rows.csv)); verse:verse571 L6 (contradicted (verse/rows.csv)); verse:verse612 L6 (contradicted (verse/rows.csv)); verse:verse765 L6 (contradicted (verse/rows.csv)); verse:verse814 L6 (contradicted (verse/rows.csv)); verse:verse588 T13 (contradicted (verse/rows.csv)); verse:verse601 T13 (contradicted (verse/rows.csv)); verse:verse417 castellvi_I_II (contradicted (verse/rows.csv)); verse:verse507 castellvi_I_II (contradicted (verse/rows.csv)); verse:verse615 castellvi_I_II (contradicted (verse/rows.csv)); verse:verse149 lumbar_rib (contradicted (verse/rows.csv)); verse:verse559 unassigned (contradicted (verse/rows.csv))

## Renders to review

Groups (renders/<group>/, contact_sheets/<group>_NN.jpg, sagittal tiles): random20 20 pairs, held_candidates 153 pairs, contradicted_ctsp 21 pairs, contradicted_verse 42 pairs, guard_misnamed 10 pairs, reader_c_blank 31 pairs. Held candidates in J1: 52 of 54 in held_all.json (not in J1: liver_119, liver_95). Copied 554 PNGs, 0 missing.

## Renders looked at

(written by hand after the renders are looked at; the gate is not complete until this section says what was seen)
