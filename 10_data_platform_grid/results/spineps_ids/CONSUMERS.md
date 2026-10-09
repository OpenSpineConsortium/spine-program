# Every reader of a SPINEPS output: how it names a level, and what a raw instance id does to it

2026-09-23, code at 421138c. Task F3 of the SPINEPS-id workflow. Nothing here is committed and no consumer was
edited. Evidence for the stores comes from the id census (grid jobs 40424774 + 40424775 →
`/rs/rs_grp_oschome/go2432/data/or_ready/spineps_ids/census.json`, copied to `census.json` here) and from
`veridah_check.json` here, written by `tools/spineps_veridah_check.py` from the census rows. That tool reads json
and csv only and can be re-run.

## 0. The defect, in one paragraph

Before commit 147428d (2026-09-21 18:20), `benchmark/run_spineps_cases.py` `harvest()` kept *the last file whose
name holds `seg-vert`*. SPINEPS writes two: the VERIDAH-named derivative, and
`output_raw_*/…seg-vert-raw_msk`, which has instance ids 1..N on SPINEPS's own cropped grid and no names. Every
store harvested before the fix holds the RAW mask. The centroid file (`*_ctd.json`) was the only ctd candidate in
every run, so it always carries VERIDAH's own ordered names. After the fix, `_rank` (l.24) prefers the non-raw
derivative. Every `_harvest.json` that chose a seg-vert file (801 CTSP, 534 TS/TSV3) names
`derivatives_seg/mod-ct_seg-vert_msk.nii.gz`.
The fixed `_rank` still **accepts a raw-only candidate silently** (l.45 takes `sorted(...)[0]` and nothing
refuses it).

A raw id read as a VerSe id gives a finite, plausible name that nothing checks: `TS_s1089` id 25 is a cervical
body at the top of the column (census row; VERIDAH's ctd for the same CT names C2..L6 in order). In these masks
"id 25 present" means "SPINEPS found at least 25 instances". It never meant L6.

## 1. What each store holds (census verdicts, per mask)

| store | written by | masks | census verdict | read as names by |
|---|---|---:|---|---|
| `~/bench/spineps/native` (CTSP one-shot benchmark, COLONOG_*) | `benchmark/run_spineps.sh`, 2026-09-08..10, pre-fix | 800 | **800 scrambled, 800 raw** | `benchmark/spineps_to_oneshot.py` |
| `~/bench_ts/spineps/native` TS_* + VERSE_* | `slurm/spineps_ts_verse.sh` 2026-09-19 (pre-fix) + `spineps_ts_retry.sh` 2026-09-23 (post-fix, 83) | 1,518 (1,144 TS, 374 VERSE) | **1,469 raw**; 1,434 scrambled; 26 verse_ok | `anomalous_inventory.py`, `transitional_mask_census.py`, `rare_class_ts_drr.sh` (pass 1) |
| `/rs/…/spineps/tsv3` | `spineps_ts_v3.sh`; 1,116 are **symlinks into bench_ts** made by `tools/ts_v3_link_reused.py` l.46 | 1,616 | 1,105 raw (1,101 of them links); 259 verse_ok | `body_masks.py` |
| `/rs/…/spineps/ctsp` | `spineps_ctsp.sh` 2026-09-23, post-fix | 801 | 686 verse_ok, 105 ctd-concordant non-monotonic, 10 one-centroid misnamed, **0 raw** | `body_masks.py` |
| `/rs/…/spineps/bodies` (A28 bodies) | `tools/body_masks.py` over bench_ts + ctsp + tsv3 | 3,935 (CTSP 801, TS 1,144, TSV3 1,616, VERSE 374) | source mask **scrambled for 2,523**; every CTSP body traces to a VerSe-coded mask | `make_drr_dataset --body-mask-dir` (no run yet), PolyPose (CTSP only) |
| `/rs/…/cobra2026/seg/spineps` (Elekta v1) | pre-fix | 146 | **146 raw**, 141 scrambled | `realxray_cobra_compare.sh` → `seg/levels.json`; `cobra_varian_bodies.sh` |
| `/rs/…/spineps/bodies_cobra` | `body_masks.py` over Elekta v1 + Varian | 246 | Elekta 137 raw / 141 scrambled; Varian (F, G) 99 verse_ok | bodybox_rescore (by overlap), `cobra_varian_geometry.py overlay` |
| `/rs/…/cobra2026/seg/spineps_v2` (+ `_veridah`) | post-fix, then POI relabel | 290 | 0 raw; 244 verse_ok | `dual_seg_compare` → `levels_v2.json` |
| `/rs/…/or_ready/crossdev/levels/spineps_v1_relabel` | POI relabel of v1 | 291 | plain 146 raw; `_veridah` 144 verse_ok | `levels_v1relabel.json` |
| `/rs/…/spineps/cobra_varian` | post-fix | 101 | 74 verse_ok, 27 ctd-concordant, 0 raw | `cobra_lstv_screen.py`, bodies_cobra |
| `/rs/…/cobra2026/lstv/seg` | `cobra_lstv_screen.py` own runs, post-fix harvest | 580 | 392 verse_ok, 182 ctd-concordant, 5 one-centroid misnamed, 1 scrambled (D034, stray id 80), 0 raw | `cobra_lstv_screen.py` |
| `/rs/…/carmlspine/spineps` (+ `_veridah`) | 2026-09-21 18:50, **post-fix** (job 40410374) | 149 + 148 | 0 raw; 285 verse_ok; case134 = VERIDAH's own C1-C5 + S | `dual_seg_compare`, `carmlspine_labels.py` |
| `realxray_work/deepfluoro`, `geneva_hip` | pre-fix, POI relabel | 6+6, 1+1 | plain masks raw; every `_veridah` verse_ok | the `_veridah` mask only |
| `/rs/…/spineps/spinesac` | post-fix | 2 | ctd-concordant, 0 raw | `spinesac_bind_bodies.py` |

In every post-fix tree, the L6/T13/none call made from mask ids matches VERIDAH's ctd call on every mask
(`veridah_check.json#id_call_vs_ctd_call_by_tree`: ctsp 801/801, cobra lstv 580/580, cobra_varian 101/101,
carmlspine 149/149). In the raw trees the two calls are unrelated. In the TS v2 bench, 13 masks carry id 25:
3 are VERIDAH L6, 3 are VERIDAH T13 and 7 are ordinary spines. A further 89 TS subjects that VERIDAH calls
L6 (37), T13 (51) or both (1) carry neither 25 nor 28. Two more (s0109 L6, s0086 T13) have post-fix masks,
written 03:52 and 03:55 on 2026-09-23. That is after `anomalous_inventory.json` was made (committed 01:15), so
the inventory never saw them.

## 2. Consumers

Risk classes: **none** = no SPINEPS id is ever turned into a name, or the name is gated by an outside labeller.
**every name** = an id is read as a VerSe level. **sacrum-only** = only the {vertebra, sacrum} class of a box
can go wrong.

| # | consumer: where the name is assigned | naming method | store it reads | risk today | downstream results | manuscript quotes it? |
|---|---|---|---|---|---|---|
| 1 | `tools/anomalous_inventory.py` `ts_cases` l.84-94: `l6=L6 in ids` | **id as VerSe label**, on raw masks | bench_ts TS_* | **every name**: the 12 "L6" are the subjects with ≥25 raw instances. VERIDAH itself calls 2 of them L6, 3 T13 and 7 ordinary, and calls 91 other TS v2 subjects transitional that were missed (89 raw masks with neither 25 nor 28, plus s0109 and s0086, whose masks came after the inventory) | `results/anomalous_inventory.{json,md}` TS row 12 (9 train, 3 absent) | **yes**: Table 4, results.tex l.15-17, NUMBERS.md l.155/202, Figure 6d, power_table.json (section 3) |
| 2 | `tools/transitional_subtypes.py` l.261-268 | inherits #1; also writes the false statement `mask_representation="SPINEPS mask carries L6 as id 25"` | anomalous_inventory.json | **every name** (inherited) | `results/rare_class/transitional_subtypes.{csv,json,md}` (L6 121 cases / 119 patients includes TS 12; `by_mask_repr` "L6 own label 83") | **yes**: Table 4 rows and the by-mask-representation sentence |
| 3 | `tools/rare_class_stratify.py` l.63-80 | **ctd** (ts12_ctd_subtypes.json) corrects the 12 only | transitional_subtypes.csv | the 12 now carry VERIDAH's own call. The 89 missed subjects are absent | `results/rare_class/stratify.json` → `make_context_crops --stratify-json`, `rare_final_keys.sh` (40424738, pending) | no |
| 4 | `SchwingNet/slurm/rare_class_ts_drr.sh` l.71 `assert 25 in ids`, then `render_physics_drr --scheme verse` | **id as VerSe label** | bench_ts raw, resampled onto the CT | **every name** on the pass-1 frames (job 40419557). Purged by `rare_class_ts_drr2.sh`, which re-renders with ctd ids (40424662/40424677, running) | `/rs/…/rare_class/totalsegmentator_drr` | no |
| 5 | `tools/rare_class_ts_fixids.py` l.58-91 | **ctd**: centroid z-rank match, 25 mm (45 mm sacrum) tolerance, fails loudly; checked independently by `tools/ts12_verify_ids.py` (POI-in-mask) | bench_ts | none from ids. The subtype is VERIDAH pseudo-truth (section 4) | pass-2 frames; `subtype_fix.json` → `rare_class_ts_annotate.py --subtype-override` | no |
| 6 | `tools/rare_class_ts_annotate.py` l.80-87 | subtype from the CSV **unless `--subtype-override`**: without it, the pass-2 frames would again be labelled L6 | transitional_subtypes.csv | every name if run without the override | frame anns | no |
| 7 | `tools/transitional_mask_census.py` NAMES l.37, TS path tagged `spineps_veridah` l.50, `lumbar` l.91 | **id as VerSe label** | bench_ts raw (TS rows); carm plain + `_veridah` | **every name** for TS rows | `/rs/…/rare_class/mask_census/mask_census.json`: nothing reads it | no |
| 8 | `tools/body_masks.py` l.46 (`body = np.where(corpus, vi, 0)`), l.51 keys `levels` by id | none of its own: **passes the id through** while its docstring (l.14) and `body.json` assert VerSe ids | bench_ts + tsv3 + ctsp → `bodies`; Elekta v1 + Varian → `bodies_cobra` | inherited: every name for the **2,523 of 3,935** bodies whose source mask is scrambled (the TS/TSV3/VERSE bodies built from raw masks); all 801 CTSP bodies are clean | see #9, #10, #11, #12, #19 | the A28 convention is quoted. No quoted number reads a raw-id body as a name (#10, #12) |
| 9 | `tools/make_drr_dataset.py` `body_boxes` l.260-266 (`vid = inv.get(nm)`, `m = body_pir == vid`) | **id as VerSe label**: release name → VerSe id → body id | `bodies` | **every name**, and for a {vertebra, sacrum} detector the boxes land on the wrong bodies (duplicates, misses, a sacrum box on the 26th instance). Today it is blocked only by the **shape** test in `body_mask_for` l.245: raw bodies sit on SPINEPS's crop grid. The affine is never compared, and l.431 maps the body with the *label's* affine | no bank has been built with `--body-mask-dir` yet (`ctsp0533_renders.sh` l.15-19: the body corpus is the G4 rebuild) | not yet: every G4 body-box bank would be |
| 10 | bodybox_rescore COBRA truth (grid-only `/rs/…/or_ready/bodybox_rescore/bin/`, record `bodybox_rescore/grid/truth_build.json`) | **position match**: each TotalSegmentator vertebra → the SPINEPS body instance covering ≥0.3 of it in world space, one-to-one. The maps show raw ids (A053: L4=1, L2=2, L3=4, L1=5, L5=6, T12=7) | `bodies_cobra` Elekta (raw) | **none**: names come from TotalSegmentator and the sacrum is the whole TotalSegmentator sacrum | `bodybox_rescore/RESCORE.md` (855 of 893; 35.8 % BODY control) | the rescore rows, if quoted: unaffected |
| 11 | `tools/cobra_varian_geometry.py overlay` l.66, l.443-444 | **id as VerSe label** (drawn text + `rows[].level`) | `bodies_cobra` | none for Varian (VerSe ids). **Every name** if pointed at an Elekta case (A-D bodies are raw) | `/rs/…/cobra2026/varian/proof/*.png` + summary | no (QC) |
| 12 | `tools/polypose_invariants.py` `body_mask_consistent`; `tools/polypose_manifest.py` l.844 | uses body id *i* only inside release label *i* (CTSP v11 is VerSe-native). This is an outside check: a raw id would fail it | `bodies/CTSP_*` only | none (CTSP bodies clean, and checked) | PolyPose bank | PolyPose methods |
| 13 | `tools/spinesac_bind_bodies.py` l.65 `VERSE_NAME`, l.211; sacrum = id 26 (l.48) | **id as VerSe label**; refuses a mask off the CT grid (l.185) | `spineps/spinesac` (post-fix) | none today (ctd-concordant). A raw mask would be refused by the grid test | `spinesac_truth.py` truth boxes | no |
| 14 | `tools/dual_seg_compare.py` l.80 `lvl_sp = NAME.get(best)`, gate l.81, flags l.88-90 | **id as VerSe label**, bone by overlap, **name only where TotalSegmentator agrees** (dice ≥ 0.5) | `_veridah` masks (carm 148, DF 6, Geneva 1, COBRA v2), plain mask for case134 and for COBRA v1 | none for agreed names: a raw id can only turn an agreement into null. A raw mask with ≥25/28 instances would fire a **false "VERIDAH calls L6/T13" flag** | `levels.json` / `levels_v2.json` | via #15-#17 |
| 15 | `tools/spineps_relabel_from_poi.py` l.60-88 | **ctd** → the instance holding the POI (position match); refuses a non-one-to-one mapping | raw or post-fix plain masks | none | `*_seg-vert_msk_veridah.nii.gz` (all verse_ok except one in `spineps_v1_relabel` that has no ctd to test against) | via #14 |
| 16 | `tools/carmlspine_labels.py` l.176-181, bone by overlap l.218-237, name l.272 | **position match** for the bone; **name from TS + VERIDAH agreement** (ctd-relabelled) | `carmlspine/spineps` (post-fix) | none | C-ArmLSpine truth: Tables 2-3, 814/910 agreed, lcurve, contribution matrix, counting, coupling | **yes**, unaffected |
| 17 | `tools/realxray_cobra_export.py` `level_info` l.248-256; `realxray_deepfluoro_export.py` l.256-310; `realxray_geneva_export.py` l.460-490 | boxes and class from TotalSegmentator; `level` = the agreed name from #14 | COBRA `levels_v2.json` (pinned in `realxray_cobra_export_v3.sh` l.31); DF/Geneva `_veridah` | none, **but `realxray_cobra_export.py` l.677 defaults `--levels` to `seg/levels.json`**, the v1 file built on raw ids. A rebuild without the pin zeroes every agreed level (already happened once: `v3_eval right=0 wrong=0`) and can raise false variant flags | COBRA/DF/Geneva meta and test sets (Table 2) | Table 2 detection is class-only: unaffected |
| 18 | `tools/cobra_lstv_screen.py` `call_subtype` l.127-154 | **id as VerSe label**, on post-fix harvests only; the raw v1 tree is excluded (l.161-164) and jsons made from it are redone (l.192-198). **No ctd cross-check** | own `lstv/seg` + `cobra_varian` | ids correct today (580/580 and 101/101 agree with the ctd). The calls are VERIDAH pseudo-truth (section 4) | `results/cobra_lstv_screen.{md,json}` (104 screened at 13:38: 6 L6, 4 T13) | no (Table 4 says COBRA is not yet screened) |
| 19 | `benchmark/spineps_to_oneshot.py` l.32, l.66; `benchmark/mappings/spineps.json`; `run_spineps_ribs.py` l.78-83 (ribs assigned to the vertebra *instance*) | **id as VerSe label** | `~/bench/spineps/native` (800, all raw) | **every name**. `~/bench/spineps/score/summary.json` reads Dice 0.000 on every class and a rib-free count error of −4..−6 on all 800: the scored SPINEPS column is void. SPINEPS-VERIDAH was **never scored on TS or VerSe**: no scorer reads bench_ts, and the "scored on VerSe first" in `spineps_ts_verse.sh` was not built | `~/bench/spineps/{oneshot,score}` | no (`collect.py` "to write"; `tab_capabilities.tex` lists capabilities, not scores) |
| 20 | `tools/rare_class_carmlspine_drr.py` l.141-163 | `_veridah` ids as names (**ctd**) | carmlspine | none from ids | `/rs/…/rare_class/carmlspine_cbct_drr` | no |
| 21 | `SchwingNet/tools/coupling_report.py` l.38; `SchwingNet/slurm/coupling.sh` l.30 | three cases **hard-coded** from `levels.json` "VERIDAH calls L6", itself from the `_veridah` (ctd) masks. The census confirms that VERIDAH's ctd names L6 on exactly these 3 | carmlspine | none from ids (the truth is a VERIDAH read, already disclosed) | `results/coupling.json` `cells_with_veridah_l6`, `l6_patients` | **yes**: Table 3 row, Figure 5c, NUMBERS.md l.201. Unaffected |
| 22 | `tools/or_crossdev_levels_report.py` l.21, l.71, l.98; `tools/case134_sweep.py` l.231-233; `tools/pelvis_landmarks.py` l.208 (carries `level_spineps` as a QC flag) | `_veridah` ids (ctd) for overlay text; levels.json agreement | COBRA v2, carm | none | overlays, `arc/case134_sweep.md`, landmark flags | no |
| 23 | `tools/lcurve_score.py`, `tools/lcurve_report.py`, `tools/carmlspine_eval.py`, `tools/or_crossdev_score.py`, `SchwingNet/tools/counting_report.py` | never read a SPINEPS id. They read the truth `box` / `outline_box` / `level` written by #16 and #17 | meta | none | lcurve, counting, crossdev | yes, unaffected |
| 24 | `tools/ts_spineps_diagnose.py`, `ts_spineps_failure_classes.py`, `spineps_label_census.py` | read the release labels and the runner logs, and count ids. No naming | bench_ts, tsv3 | none. `ts_diagnose/label_census.json` (03:19) already showed the bench_ts masks as {1..N} with no 26 and no discs, 40 of 40 | `ts_diagnose/*` | no |
| 25 | `SchwingNet/tools/fig_claim.py` l.40-42; `tools/polypose/check_sampling_spec.py` l.197 | read #1's TS count | anomalous_inventory.json; `sampling_spec.json` `L6_spineps_called` | **every name** (inherited) | Figure 6d, power_table.json; PolyPose `N_rare_real_ct` 86 | **yes** (Figure 6d); PolyPose spec |
| 26 | level banks (`allspine_v8/v9`, ctsp/verse/physics/physics_rare/ts_drr/ts_drr_v3 renders), learning (`learning_*`), `tools/anomaly_manifest.py` + `lstv_flag_labels.py` (the 749-spine manifest) | names from **release labels** (or films); no SPINEPS path and no `--body-mask-dir` in any bank script | none | **none** | Table 3 accuracies, LEARNING.md, anomaly manifest | yes, unaffected |

## 3. Sentences and numbers that must change (owned by other workflows, so they are named here and not edited)

The inputs to these numbers are wrong now. What to replace them with depends on a decision that section 4
informs. Three readings, all computed from `anomalous_inventory.json` splits and the ctd calls:

| | today | A: the 12 by VERIDAH's ctd | B: TS by ctd over the whole v2 bench | C: no TS row (no reader) |
|---|---|---|---|---|
| TS persons (L6 / T13 / both) | 12 (12 / 0 / 0) | 5 (2 / 3 / 0) | 96 (40 / 55 / 1) | 0 |
| L6 row, Table 4 (CTSP / VerSe / TS / C-Arm) | 83 (18 / 50 / 12 / 3) | 73 (18 / 50 / 2 / 3) | 111 (18 / 50 / 40 / 3) | 71 (18 / 50 / 0 / 3) |
| T13 row | 6 (0 / 6 / 0 / 0) | 9 (0 / 6 / 3 / 0) | 61 (0 / 6 / 55 / 0) | 6 |
| any transitional | 198 (48 / 135 / 12 / 3) | 191 (… / 5 / …) | 282 (… / 96 / …) | 186 |
| count-changing | 89 (83 L6, 6 T13) | 82 (73, 9) | not a truth set (section 4) | 77 (71, 6) |
| in the training half of the v8 bank | 65 | 60 (TS 4: s1089, s0616, s1088, s1123; s1178 absent) | unknown (bank keys needed) | 56 |
| CT subjects → test persons, 40 % | 86 → 3 + 34 = 37 | 79 → 3 + 32 = **35** | — | 74 → 3 + 30 = **33** |
| 50 % rule | 46 | 43 | — | 40 |
| Wilson lower bound at k = 0 / k = 1 | 90.6 / 86.2 % | 90.1 / 85.5 % | — | **89.6 / 84.7 %**: under 90 % even with zero errors |

Places that carry a number from the "today" column:

- `SchwingNet/sections/results.tex` l.15-17: "198 (48 CTSpinoPelvic1K, 135 VerSe, 12 TotalSegmentator, three
  intraoperative), 89 count-changing (83 sixth lumbar, six thirteenth thoracic), 65 in the training half".
- `SchwingNet/tables/tab4_transitional.{tex,md}`: rows "L6, mobile 83 (18 / 50 / 12 / 3)", "T13 6", "Any
  transitional subtype 198 (48 / 135 / 12 / 3)", "37 projected for the 89 L6 and T13 persons". Also footnote (c)
  "89 persons; 65 … training half", footnote (d) "3 real subjects plus round(0.40 × 86) … 37 … 90.6 % … 86.2 %",
  the by-mask-representation sentence "L6 own label 83" (from `transitional_subtypes.json#counts/*/by_mask_repr`,
  where the 12 TS rows are the false "SPINEPS mask carries L6 as id 25"), and the v8 split sentence "L6 16
  validation, 61 train, 3 leaking, 3 absent; T13 1 validation, 5 train".
- `SchwingNet/NUMBERS.md` l.155 (Figure 6d inventory marker: 89, TotalSegmentator 12, 37 / 46, 90.6 / 86.2) and
  l.202 (Table 4 persons).
- `SchwingNet/results/power_table.json#inventory_today` (`by_source.totalsegmentator` 12, `ct` 86, `total` 89,
  37 / 46) and Figure 6d, regenerated by `SchwingNet/tools/fig_claim.py` once `anomalous_inventory.json` is
  corrected.
- `SchwingNet/LEVELCHECK_CLAIM.md` l.128-139; `SchwingNet/CLAIMS_LEDGER.md` l.209 ("TotalSegmentator 12").
- `SchwingNet/results/anomalous_inventory.{json,md}` TS row; `results/rare_class/transitional_subtypes.{csv,json,md}`
  (L6 121 cases / 119 patients, "totalsegmentator 12"). Upstream fix: `tools/anomalous_inventory.py` `ts_cases`
  must read the ctd (`ctd_labels` ∋ 25/28), not `np.unique(mask)`.
- PolyPose (`results/polypose/` is owned by that workflow): `sampling_spec.json`
  `real_rare_ct_inventory.totalsegmentator.L6_spineps_called` 12 (`in_bank` 9), `N_rare_real_ct` 86 → 76 under
  A counting TS L6 only (79 counting the 3 T13), 74 under C. `SAMPLING_SPEC.md` l.407. The V / share arithmetic
  checked by `check_sampling_spec.py` l.197 follows.

Not affected: the C-ArmLSpine truth (814 of 910 agreed; ids verse_ok and the name gated by TS), the three
C-ArmLSpine L6 patients (VERIDAH's ctd names exactly these three), every detection number (class-only boxes from
TotalSegmentator or the C-ArmLSpine body chosen by overlap), bodybox_rescore (bridged by overlap), lcurve, and
the 749-spine anomaly manifest (reads no SPINEPS output).

## 4. What VERIDAH's ctd call is worth as truth (outside check)

Switching from ids to the ctd fixes which name the tool gave. It says nothing about whether that name is right.
Two collections here carry a reader's truth beside a VERIDAH ctd (`veridah_check.json`):

- **CTSpinoPelvic1K** (801 CTs; release labels + two-reader Castellvi consensus). VERIDAH calls L6 on 24 and
  **10 of them are reader L6**. The other 14 are ordinary spines. Of the 18 reader L6, VERIDAH calls 10 L6, 6
  T13 (the same extra segment placed at the other junction) and 2 ordinary. VERIDAH calls **T13 on 52 CTs**:
  37 ordinary, 6 sacralised L5, 6 reader L6, 2 Castellvi I/II and 1 lumbar rib. CTSP has no reader T13. Only
  **16 of 76 count-changing calls land on a reader L6**. 51 of 749 ordinary spines get one.
- **VerSe**, VERIDAH's home ground (374 volumes, raw-mask truth). L6 calls 42, of which 34 are VerSe L6;
  34 of 50 VerSe L6 are called L6. T13 calls 26, of which 4 are VerSe T13. Part of the T13 excess is the known
  VerSe/VERIDAH convention dispute (verse509/512/513 are in `VerSeFusion/configs/veridah_corrections.csv`).

So reading A puts 5 VERIDAH calls in a table labelled "persons with their own truth". Reading B puts 96 there.
On the one reader-truthed abdominal CT collection here, 14 of VERIDAH's 24 L6 calls (58 %) fell on spines
the readers call ordinary. None of its 52 T13 calls matched a reader T13; 6 fell on a reader L6. The same caveat covers the COBRA LSTV screen (#18), which is VERIDAH
by construction, and the three C-ArmLSpine "L6 patients" (already disclosed as a VERIDAH read).

## 5. Guards that are missing (recommendations, not applied: the files are shared)

1. `benchmark/run_spineps_cases.py` `harvest()` l.45: refuse, and record, a case whose only `seg-vert` candidate
   is raw. Today `sorted(..., key=_rank)[0]` returns it.
2. Every reader that turns an id into a name (#1, #7, #9, #11, #13, #18, #19) should check the mask against its
   ctd before naming. This is the test `spineps_id_census.py` already implements (the instance holding each ctd
   centroid carries that centroid's label).
3. `tools/body_masks.py`: carry the source mask's census verdict (or run the ctd test) into `<case>_body.json`
   and refuse a raw source. Raw-source bodies should also be moved out of `bodies/` before the G4
   `--body-mask-dir` rebuild. The shape test in `make_drr_dataset.body_mask_for` should compare affines too.
4. `tools/realxray_cobra_export.py` l.677: default `--levels` to `levels_v2.json`, or refuse the raw v1 file
   (`levels_v1_rawinstance_backup.json` holds the same content).
5. `tools/ts_v3_link_reused.py`: link only masks whose census verdict is VerSe-coded. The 1,101 raw links under
   `tsv3/` are the same raw files as bench_ts.
6. Re-harvest is cheap: the derivative mask was deleted with the /dev/shm stage, but the ctd survived. For a
   store where the ctd must supply names, `spineps_relabel_from_poi.py` (position match) is the proven route.
   `rare_class_ts_fixids.py` (z-rank) is the route for the 12, and `ts12_verify_ids.py` checks it independently.

## 6. Not known

- Whether any render or bank outside the local repo's scripts was built with `--body-mask-dir` (grep finds none,
  `ctsp0533_renders.sh` says none yet). Only the shape test stood between the raw bodies and a render.
- The bodybox_rescore builder lives only on the grid (`/rs/…/or_ready/bodybox_rescore/bin/`). Its matching rule is
  read from `truth_build.json` and the job log, not from source.
- Reading B's training-half count needs the v8 bank keys for the 96 TS subjects. It was not computed.
- Whether VERIDAH's T13 calls on CTSP are wrong or a convention CTSP's labels cannot express: CTSP carries no
  T13 class, so its 52 T13 calls have no reader to settle them.
