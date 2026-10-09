# Sources for every cell of Table 2 (`tab4_transitional.tex` / `tab4_transitional.md`), rewritten 2026-09-23

Files (repo-relative):

- **SUB** `SchwingNet/results/rare_class/transitional_subtypes.csv` (196 rows, 194 distinct `patient_key`; written 2026-09-23 18:54, sha256 ec5fc0d2d601…) and its report `transitional_subtypes.md`. Persons = distinct `patient_key` per (`subtype`, `source`); four-lumbar = `four_lumbar_mask == True`. The same file Figure 5 draws (`figures/figure5.record.json#counts_dated/subtype_table`).
- **SPLIT** `SchwingNet/results/rare_class/split_plan.md` ("Transitional people per side, per subtype (G1 table, verified)" and "Real transitional subjects"; `tools/make_split.py` plan 20:02:12, apply 20:18:48, seed 0, leak audit PASS; `results/spineps_ids/g3_split/split_leak_report.json#verdict` PASS). **Owned by the split workflow; read, not written.**
- **COBRA** `SchwingNet/results/power/inputs/cobra_lstv_screen.grid.json` (692 of 692 cases, generated on the grid 2026-09-23 18:46) as drawn in Figure 5 (`figure5.record.json` rows `real_with_cobra_calls`); the split plan's "COBRA screen transitional calls: 91 — L6 38, T13 45, four_lumbar 8" and `reread_candidate` 3.
- **PPV** `SchwingNet/results/spineps_ids/IMPACT.md` §5 ("CTSP: 10 of 24 L6 calls are reader L6").
- **TS12** `SchwingNet/results/spineps_ids/TS12_VERIFY.md`, `results/rare_class/ts12_subtype_override.json`: of twelve TS spines once selected by raw id 25, four transitional (s0616 T13; s1088, s1089, s1123 L6), eight normal.
- **W** Wilson 95 % lower bound at k = n, z = 1.959964 (recomputed; equals `figures/figure5.record.json` panel d and `results/power/power.json#panel_d_best_case_intervals`): n = 3 43.85, 5 56.55, 6 60.97, 12 75.75, 43 91.80.

## Rows

| row | cell | value | file → field |
|---|---|---|---|
| L6 | persons | 110 (18 / 86 / 3 / 3) | SUB: L6 × ctsp 18, verse 86, totalsegmentator 3, carmlspine_real 3 |
| | audit read alone | 38 | SUB `truth_source` = "lstv_flag_labels_v2.csv verse audit" (no raw-mask id check); `figure5.record.json#discrepancies_stated[1]` |
| | test CT + real | 43 + 3 | SPLIT L6 test 43 (ctsp 7, ts 2, verse 34); real: carmlspine case121, case136, case42 |
| | trained on | 49 of 54 | SPLIT "val+test people in v8 or v9 train" |
| | COBRA calls (supported) | 38 (11) | COBRA L6; supported = `figures/figure5.record.json` panel c `cobra_calls_supported` (27 L6 calls with no L1 in the field dropped, `results/rare_class/split_plan.md`) |
| | Wilson | 91.8 (43 CT); 74.1 (11 calls) | W n = 43, 11 (`power.json#panel_d_best_case_intervals` L6 rows). The 43.9 (3 real) of 2026-09-23 is withdrawn: the three C-ArmLSpine L6 are scored in paper 1 only in cross-validation (Table 3, agreement with one labeller's read; note c), and paper 2's pre-specification excludes them from its primary analysis in advance (`LEVELCHECK_MODEL.md` §4; `figure5.record.json#not_drawn/carmlspine_real_L6`) |
| T13 | persons | 7 (0 / 6 / 1 / 0) | SUB: T13 × verse 6, totalsegmentator 1 (s0616) |
| | test; trained on; COBRA (supported); Wilson | 3 + 0; 4 of 4; 45 (38); 43.9 (3 CT), 90.8 (38 calls) | SPLIT; SPLIT; COBRA T13, supported = `figure5.record.json` panel c (7 T13 calls over L1–L4 only dropped); W n = 3, 38 |
| Sacralised L5, four lumbar | persons | 12 (9 / 3 / 0 / 0) | SUB: sacralised_L5_fused with four_lumbar_mask True × ctsp 9, verse 3 |
| | test; COBRA (supported); Wilson | 5; 8 (8); 56.6 (5 CT), 67.6 (8 calls) | SPLIT mask strata merged_into_sacrum 4 + four_lumbar_unchecked 1; COBRA four_lumbar 8, all supported (`figure5.record.json` panel c, sacralised row); W n = 5, 8 |
| Sacralised L5, five lumbar | persons | 16 (3 / 13 / 0 / 0) | SUB: sacralised_L5_fused with four_lumbar_mask False × ctsp 3, verse 13 |
| | test; Wilson | 6; 61.0 | SPLIT mask stratum own_id 6; W n = 6 |
| both sacralised rows | trained on | 14 of 14 | SPLIT sacralised_L5_fused |
| Castellvi I/II | persons; test; trained on; Wilson | 31 (4 / 27 / 0 / 0); 12; 15 of 15; 75.8 | SUB; SPLIT; SPLIT; W n = 12 |
| Lumbar rib | persons; test; trained on; Wilson | 14 (14 / 0 / 0 / 0); 6; 7 of 7; 61.0 | SUB; SPLIT; SPLIT; W n = 6 |
| Unassigned | persons; test; trained on | 4 (4 / 0 / 0 / 0); 2; 3 of 3 | SUB (CTSP 0801, 0931, 1043, 1123: four lumbar ids, normal source read); SPLIT |
| L6 and T13 in one spine | persons | 0 | SUB report "both_L6_T13: zero cases in every source"; SPLIT |
| Any subtype | persons | 194 (52 / 135 / 4 / 3) | SUB distinct patient_key 194; per source ctsp 18+4+14+12+4, verse 86+6+27+16, ts 3+1, carmlspine 3 |
| | test | 77 + 3 | sum of the CT test cells; SPLIT real 3 |
| | trained on | 92 of 97 | sum of the SPLIT cells (49 + 4 + 14 + 15 + 7 + 3 of 54 + 4 + 14 + 15 + 7 + 3) |
| | COBRA calls (supported) | 91 (57) | COBRA 38 + 45 + 8; supported 11 + 38 + 8 (`figure5.record.json` panel c pooled row `cobra_calls_supported` 57) |
| | Wilson, L6 + T13 + sacralised | 93.7 (57 CT); 93.7 (57 calls) | W n = 57 (`power.json#panel_d_best_case_intervals` pooled row: `ct_test` 57, `cobra_calls_supported` 57, both 93.69) |
| footnote (e) | PPV | 10 of 24 | PPV |
| footnote (f) | 35 persons; 22 carriers | Wilson k = n ≥ 90 % at n = 35, ≥ 85 % at n = 22 | `results/stats_review/recompute.json#R4_wilson/min_n_zero_errors`; `figures/figure5.record.json#numbers_on_figure/n_needed` |
