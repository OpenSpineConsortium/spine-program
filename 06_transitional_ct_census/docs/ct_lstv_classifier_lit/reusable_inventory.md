# Reusable inventory for a CT-segmentation transitional-phenotype classifier

Written 2026-09-24 from the files named below (read-only; nothing on the grid was run, nothing edited).
Purpose: what already exists to build and validate a classifier of the transitional phenotype from a
CT segmentation WITHOUT new human reads, so the design reuses rather than rebuilds. Paths are absolute
on Windows (`<spinesurg-ct-nnunet repository at 097933a>/` = REPO; `...\CTSpinoPelvic1K-1` = CTSP;
`...\OpenSpineToolkit` = OSTK) or on the grid (`~` = `/wsu/home/go/go24/go2432`, `RS` =
`/rs/rs_grp_oschome/go2432/data`).

## 0. Bottom line

- Section 14 already fused three automated readers (A SPINEPS ctd names, B TotalSegmentator geometry,
  C direct CT rib count) by Dawid-Skene and calibrated them on 945 human-read persons. **Only `ordinary`
  reached the PPV lower bound 0.90.** L6 reached 1.000 [0.785, 1.0] under unanimity (14/14) and 0.79-0.81
  under 2-of-3 / DS; T13 had n_truth = 4; four_lumbar PPV 0.14-0.25 (5 true, 14-35 called). A classifier
  enters as **reader E** in the same fusion; the calibration harness, the truth tables, the split and the
  per-vertebra evidence records exist and are named below.
- Every reader already writes **per-body and per-rib records** (body length/volume/centroid along the
  column, rib length / lateral reach / head presence / joint level, stump flags, L5-S1 contact and gap,
  S1-sacrum fusion tests, junction-in-FOV flags). Those are the features; the classifier does not need a
  new segmentation pass on CTSP, VerSe, COBRA, C-ArmLSpine or TS v2.
- The **human-read phenotype counts** are small and fixed: CTSP two-reader Castellvi (34 graded records,
  `castellvi_consensus.csv`) + release L6/lumbar-rib ids; VerSe Loffler 2021 read (171 of 374 series carry
  a read subtype: L6 87, castellvi_I_II 28, unassigned 24, lumbar_rib 13, sacralised_L5_fused 13, T13 6).
  G1 table: 196 rows / 194 persons; G3 split per subtype (train/val/test): L6 53/11/43, T13 3/1/3,
  sacralised_L5_fused 14/3/11, castellvi_I_II 16/3/12, lumbar_rib 7/1/6, unassigned 1/1/2. Test persons
  must not touch training of anything that feeds Figure 6.
- **Traps that already bit**: raw SPINEPS ids 1..N in every pre-147428d harvest (2,437 masks, 2,714
  body masks); two CTSP label maps; VERIDAH skips T12 in 54/801 CTSP ctds; TS `sacrum` and `vertebrae_S1`
  are disjoint; VerSeFusion unified masks carry no sacrum id and many read-L6 persons carry no id 25;
  a maximum extent is not a diameter; render the mask.

## 1. The section-14 automated reference (what exists, where, what it found)

### 1.1 Governing text
`REPO\SchwingNet\LEVELCHECK_MODEL.md` lines 733-779 (s14; R1 readers, R2 rule chosen on calibration data
only, R3 use). Not edited. Key sentences: L746-753 define A/B/C/D; L763-764 "highest calibration coverage
whose per-subtype PPV has a Wilson lower bound >= 0.90"; L771-772 a person with no human read enters only if
the frozen rule assigns a subtype and every lumbar name.

### 1.2 Frozen outputs
- `REPO\SchwingNet\results\fig6\frozen\auto_reference.json` (sha in `auto_reference.sha256`; git_head
  749bc94, UTC 2026-09-24T19:46:05Z; prespecification commit b511985). `rule.mode` =
  "per_subtype (no rule reached a PPV lower bound of 0.90 for every subtype it assigns)";
  `per_class = {ordinary: dawid_skene}`; `assignable_subtypes = [ordinary]`; `ds_posterior_threshold 0.95`.
- `REPO\SchwingNet\results\fig6\frozen\auto_truth.csv` (1,998 rows, one per person, 33 columns incl.
  `call_A call_B call_C n_rib_bearing_{A,B,C} unanimity two_of_three dawid_skene status assigned_subtype
  lumbar_names reader_D human_truth_subtype human_truth_class human_truth_source in_calibration g3_side`).
- Report: `REPO\SchwingNet\results\auto_reference\CALIBRATION.md` + `calibration.json`.
- Reader tables: `REPO\SchwingNet\results\auto_reference\readersAB\tables\{ctsp,verse,cobra_ct,cobra_cbct,carmlspine}.csv`,
  `readersAB\SUMMARY.md`; `REPO\SchwingNet\results\auto_reference\readerC\{ctsp,verse,cobra_ct,cobra_cbct,carmlspine,ts12}.csv`.
  Per-case JSON evidence lives on the grid: `RS/or_ready/auto_reference/readersAB/{a,b}/<corpus>/*.json`,
  `RS/or_ready/auto_reference/readerC/<corpus>/json/<case>.json` (+ `render/<case>.jpg`).

### 1.3 Calibration table (CALIBRATION.md; n = 945 = CTSP 707 + VerSe 238; sides train 846 / val 99; 0 test persons)
Truth classes: ordinary 873, L6 63, four_lumbar 5, T13 4 (alt convention own-id sacralised = four_lumbar: 863/63/15/4).

| rule | coverage | class | n truth | assigned | correct | PPV [Wilson 95%] | LB >= 0.90? |
|---|---:|---|---:|---:|---:|---|---|
| unanimity | 0.605 | ordinary | 873 | 554 | 549 | 0.991 [0.979, 0.996] | yes |
| unanimity | | L6 | 63 | 14 | 14 | 1.000 [0.785, 1.000] | **no** (n too small: needs >= 35 correct of 35 for LB 0.90) |
| unanimity | | T13 | 4 | 0 | 0 | n/a | no |
| unanimity | | four_lumbar | 5 | 4 | 1 | 0.250 [0.046, 0.699] | no |
| two_of_three | 0.839 | ordinary | 873 | 746 | 729 | 0.977 [0.964, 0.986] | yes |
| two_of_three | | L6 | 63 | 32 | 26 | 0.812 [0.647, 0.911] | no |
| two_of_three | | T13 | 4 | 1 | 1 | 1.000 [0.207, 1.000] | no |
| two_of_three | | four_lumbar | 5 | 14 | 2 | 0.143 [0.040, 0.399] | no |
| dawid_skene | 0.886 | ordinary | 873 | 792 | 769 | 0.971 [0.957, 0.981] | yes (chosen: highest coverage) |
| dawid_skene | | L6 | 63 | 29 | 23 | 0.793 [0.616, 0.902] | no |
| dawid_skene | | T13 | 4 | 2 | 1 | 0.500 [0.095, 0.905] | no |
| dawid_skene | | four_lumbar | 5 | 14 | 2 | 0.143 [0.040, 0.399] | no |

Each reader alone (same set): A ordinary PPV 0.975, L6 0.750 (24/32), T13 0.333 (3/9), four_lumbar 0.143
(5/35); B ordinary 0.962, L6 0.596 (28/47), four_lumbar 0.077; C ordinary 0.972, L6 0.674 (29/43),
four_lumbar 0.133. Per corpus, L6 PPV is 1.000 on VerSe under every rule (12/12, 19/19, 16/16) and
0.538 on CTSP (7/13): the CTSP false L6 are the release-named five-lumbar spines the two-labeller count calls
six (see 3.1, the ten held CTSP cases). DS confusion (auto_reference.json L455-575): A calls a true L6
"ordinary" 0.49 of the time; B calls a true T13 "ordinary" 0.53 / "L6" 0.46; C calls a true T13 "L6" 0.40.

Wilson arithmetic the design needs: with zero errors the lower bound reaches 0.90 at n = 35 (n/(n+3.84) >= 0.90
needs n >= 34.6). L6 has 63 calibration truths, so a reader E that calls >= 35 of them with 0 errors on
calibration would certify L6; T13 (4) and four_lumbar (5) cannot be certified on the present read set by any
reader.

Reader D (COBRA CBCT): A and B abstained on 691/692 and 692/692 CBCTs (readersAB SUMMARY "Calls per corpus");
D is vacuous. T2 (COBRA, 159 test persons): 56 assigned ordinary, 103 excluded (88 "no reader could count",
9 uncalibrated subtype, 6 disagree). T3 (C-ArmLSpine 13): all excluded (lumbar-only CBCT).

### 1.4 Code that produced it
| file | role | notes |
|---|---|---|
| `REPO\tools\auto_reference_readers_ab.py` (906 lines) | readers A and B, one implementation for every corpus; `lists`, `a`, `b`, `table` subcommands | input roots L76-99 (CTSP_A `RS/spineps/ctsp`, CTSP_B `~/bench/totalsegmentator/native`, VERSE_A `RS/spineps/ctd_relabel/bench_ts_native`, VERSE_B `RS/anomaly_harvest/verse/ts`, COBRA_SCREEN `RS/cobra2026/lstv`, COBRA_B_CT `RS/anomaly_harvest/cobra/ts`, CARM_A `RS/carmlspine/spineps`, CARM_B `RS/or_ready/auto_reference/ts/carmlspine`). `reader_a` L358-416; `reader_b` L453-493; `subtype_call(nT, nL)` L524-560 (the subtype vocabulary from two counts); `b_assignment` L616 (rib->body seq2:skip+same); `_rank` L793 (one series per VerSe person). ROW_FIELDS L92-94. |
| `REPO\tools\rib_count_reader.py` (1,398 lines) | reader C (and D on CBCT): bodies along a curve through TS body centres, ribs traced through bone >= 150 HU to the costovertebral joint, 38 mm rib rule | parameters L96-128 (RIB_HU 200, RIB_LEN_MM 38, RIB_LAT_MM 30, STUMP_MIN_MM 12, MAX_DISC_MM 20, MERGE_RATIO 1.6, LAT_MM 65, SAC_MIN_MM 25); `read_one` L714; `find_ribs` L515; `class_contact` L625 / `runs_contact` L667 (L5-S1 and S1-sacrum fusion tests in a 14 mm cylinder); `render` L1225; per-case R keys: `runs, ribs, rib_cage_levels, rib_levels_outside_cage, stump_levels, rib_components_per_side, junction_tl, junction_ls, junction_tests, fused_evidence, sacrum_fused_evidence, sacrum_run_mm, ts_s1_mm_on_column, lumbar_lower_bound, n_rib_bearing, n_rib_free, subtype_call, refusals, thoracic_refusals, anchors (CBCT HU anchors)`. CBCT is put on a HU-like scale by muscle -> 40 HU, vertebra -> 250 HU (L122-128). |
| `REPO\tools\auto_reference_calibrate.py` (702 lines) | truth build, three rules, `class DawidSkene` L228, `metrics` L313, `qualifies` L331, `--freeze` refuses to overwrite | `truth_ctsp` L151 (release labels + `transitional_subtypes.csv`), `truth_verse` L167 (`transitional_registry/verse/screened.csv`), `truth_class` L196 (own-id sacralised = ordinary; alt table), `norm_call` L84 (sacralised_fused -> four_lumbar), `collapse_c` L98. Reader E slot: `READERS = ["A","B","C"]` L56 and `load_readers` L115 are the two places to extend. |
| `REPO\tools\auto_reference_ab_summary.py` | builds readersAB/SUMMARY.md | |
| `REPO\tools\rib_count_ts_prep.py`, `rib_count_summary.py`, `rib_count_recall.py`, `rib_count_lastrib.py` | TS `total` for CBCT/C-Arm (GPU), collect, recall vs release ribs | |
| `REPO\tools\harvest_verse_census.py::labeller_b` L183-680 | B's evidence: TS vertebra classes as objects (MIN_BODY_ML), S1-sacrum contact (`s1_info` contact_mm2 / contact_mid_mm2), spacing, gaps, `ls_gap_mm`, per-body dicts `{ts, ml, z, c, zmin, zmax, rib, ribs, split, merged, partial}` L674, per-rib `ribs_all` dicts `{ts, side, k, ml, len, cut, z, body, d, head_z, head_dz, head_dx, votes, k_centroid, rule, head_present}` L571-575 | |
| `REPO\tools\harvest_verse_registry.py::call_a` L154, `count_b` L239, `rib_type` L233 (thoracic if ml >= MIN_THOR_RIB_ML and len > STUMP_MM; stump 8-38 mm), `sub_from` L408, `agree_ab` L438 | A's count rule (two thoracic names above a lumbar; sacrum name; C7+T1 for a thoracic count; wide spacing gap voids the count) | |
| `REPO\tools\ctsp_registry_build.py`, `ctsp_registry_census.py`, `ctsp_registry_ts.py` | CTSP stream: three body segmentations (release / SPINEPS instances / TS components) counted with the release ribs; TIERS read / two-labeller / single-labeller; T13 impossible on CTSP (no FOV reaches T1) | |
| slurm | `REPO\slurm\auto_reference_ab.sh` (reqp, arrays MODE=a/b per corpus), `REPO\SchwingNet\slurm\rc_read.sh` (reqp, 48 GB, --array per corpus shard), `rc_ts.sh` (GPU TS for CBCT), `rc_prep.sh`, `rc_collect.sh`; `SchwingNet\slurm\fig6_eval.sh` consumes `auto_truth.csv` via `SchwingNet\tools\fig6_truth_join.py` (sha check; TRUTH_JOIN_FAILED exit 9) | |

### 1.5 Per-vertebra features the readers already compute (consumable by a classifier)
From reader C per-case JSON (`RS/or_ready/auto_reference/readerC/<corpus>/json/<case>.json`):
- per body run: `k, len_mm, s=[i0,i1], z, class (TS major class), cut_top/cut_bot, fold/split/merge notes`
  (`R["runs"]` L992); occupancy and mean-CT profile every 1 mm along the column (`profile` L303) is the raw
  1-D signal a sequence model could take directly.
- per rib: traced length from the joint, lateral reach, medial-end position, `hu_mean`, `ts_rib_frac`, `ml`,
  `chord_mm`, `stump`, `rib_like`, `level`, `contact_xyz` (L940-960).
- lumbosacral junction: `junction_tests` (L5-S1 disc/joined; S1-sacrum separate/joined; `d_min`,
  `contact_mm2`, gap occupancy), `fused_evidence`, `sacrum_fused_evidence`, `sacrum_run_mm`, `ts_s1_mm_on_column`.
- thoracolumbar: `rib_cage_levels`, `rib_levels_outside_cage`, `stump_levels`, `rib_components_per_side`.
From reader B (labeller_b): per-body `ml, zmin, zmax, rib type, ribs[]`, `spacing_mm[]`, `gaps[]`,
`ls_gap_mm`, `s1.contact_mm2 / contact_mid_mm2`, `doubled_objects`, `halves_merged`, `n_ribs_unattached`.
From reader A: VERIDAH names top-to-bottom, ctd world points (L392-395), `id_ml` of ids 25/28 (the L6/T13
sliver test, CENSUS.md defect 1), `has25/has28`, `skipped`, `wide`.
None of these is a diameter or a plane-defined chord; they are counts, lengths along principal axes, contact
areas and gaps. See s4 for the morphometric measures with a published definition.

## 2. Guards and label tools

| tool | what it guarantees | line evidence |
|---|---|---|
| `REPO\tools\spineps_ids.py` (926 lines) | `assert_verse_monotonic(mask, ctd="auto", require_ctd=True)` L394: ids in VerSe alphabet (C1..L5 = 1..24, L6 25, sacrum 26, coccyx 27, T13 28), cranio-caudal in world S through the affine, agree with the ctd (>= 2 disagreements and >= 30 % = raw), ctd names in order, "cervical" not lumbar-sized. `relabel_by_ctd` L475 writes a NEW file, never overwrites; a mask relabelled from a raw tree carries NO sacrum ("d." in the docstring). `KNOWN_VERIDAH_ERRORS` (TS_s1178). `veridah_skipped_names`: VERIDAH skips T12 in 54/801 CTSP, 47/1,144 TS v2, 36/374 VerSe ctds; reproduced and flagged, `--refuse-skipped-names` refuses. | docstring L1-99 |
| `OSTK\ostk\labels.py` | `detect_scheme(volume)` L106 decides v4 (legacy, L1=1) vs v10/v11 (L1=20, sacrum 26, hips 30/31, femora 32/33) on pelvis voxel mass and RAISES `SchemeError` when ambiguous; `labels_for(volume)` L135; `lid()` L150 kept for compatibility, "the thing to avoid in new code". | |
| `REPO\tools\patient_keys.py` (500 lines) | one key per PERSON across naming schemes (`SCHEMES` L36+, `key_any` L376, `canon_key` L250); CTSP COLONOG_<n> <-> release id only through the Dataset813 symlink TARGET NAME (`d813_crosswalk` L74, never followed). Unmatched cases are written to `unmatched`, not keyed. Oblique stems `_obl_p<k>` and `ctspine1k_<stem>` are NOT yet in SCHEMES (MAXIMIZE.md "Identity note"). | |
| `REPO\tools\checkpoint_lineage.py` (2,215 lines) | `touched.json`: train + val/selection keys over the whole initialisation chain; unresolved ancestor is never treated as empty; v8/v9 banks trained on 1,040/1,046 G3 test persons (split_plan.md L211-212) so nothing descending from them may score Figure 6 persons. | |
| `REPO\tools\eval_gate.py` (1,411 lines) | `assert_unseen(items, weights, where=..., eval_set=...)` L662 raises `SeenInEvaluation`, `UnresolvedLineage`, `UnkeyedEvalItem`, `UngatedInput`, `UnverifiedDump`; only `--not-held-out "<reason>"` passes; `stamp()` L776 binds the verdict to `weights_sha256` and `eval_digest`. What a leak-free grouped split needs: every item keyed by `patient_keys.key_any`, the checkpoint's lineage resolved, and NO test-side key in train or val of any ancestor. | |
| `REPO\tools\make_split.py` (1,162 lines) | G3: person split, seeded; transitional persons 50/10/40 per subtype (exact largest-remainder, small-cell guarantees); real transitional subjects (C-ArmLSpine L6 x3, COBRA calls) TEST outside quotas; everyone else `sha256("g3|<seed>|<key>")`; aliases merged first (TS v201<->v300 by CT md5, VerSe series -> subject, VinDr image -> study, implant/PolyPose render -> source CT); a merged group takes its most held-out side. Output `~/split_final.json` = frozen `REPO\SchwingNet\results\fig6\frozen\v1\split_final.json` (sha256 65a57eb0...; identical bytes on the grid, checked 2026-09-24). Keys `side_of_person`, `group_of`, `raw_to_group`, `item_side`. | docstring L1-70; `split_plan.md` L20-35 (per-subtype sides) |

For the classifier's folds: the calibration set is exactly `auto_truth.csv` rows with `in_calibration == True`
(945 persons, sides train 846 / val 99); a k-fold inside those persons, grouped by `person_key`, with the
G3 val side as the tau-setting set (as s12/s13 do) keeps the 93 CTSP + 68 VerSe test persons untouched.
COBRA and C-ArmLSpine are real-frame TEST persons and cannot be training or calibration material.

## 3. Census: every CT collection with a segmentation on the grid

Counts are `ls | wc -l` from the login node on 2026-09-24 (no compute). "raw ids" = SPINEPS instance ids
1..N from a pre-147428d harvest (CENSUS.md per-tree table); "named" = VERIDAH names confirmed by the ctd.

| collection | n CT | CT path (grid) | segmenter / mask path | SPINEPS ids | junction / FOV note | phenotype truth source |
|---|---:|---|---|---|---|---|
| CTSpinoPelvic1K (CTSP) v11 | 802 CT, 802 labels | `~/data/CTSpinoPelvic1K/ct/<id>_ct.nii.gz` | release v11 label `~/data/CTSpinoPelvic1K/labels/<id>_label.nii.gz` (L1..L6 = 20..25, sacrum 26, ribs 34..59, lumbar ribs 60/61; id 29 retired); SPINEPS post-fix `RS/spineps/ctsp` (3,216 files, 801 masks; 791/801 ctd-confirmed) + retries `RS/anomaly_harvest/ctsp/spineps_retry` (6); TS `total` `~/bench/totalsegmentator/native/COLONOG_<n>.nii.gz` (804 files) + `RS/anomaly_harvest/ctsp/ts_retry/native` (0533, 0921); crosswalk `~/bench/ct_by_case` (802 links) | named (post-fix); `~/bench/spineps/native` is 800/800 RAW: never read | abdominopelvic: LS junction in FOV 747-800/802 (A/B), TL reference (rib-bearing body + one above) 720-741; no CTSP FOV reaches T1, so T13 is uncountable (ctsp_registry_build docstring) | two-reader Castellvi `CTSP\docs\castellvi_consensus.csv` (34 rows: volume_id, token, read_1, read_2, consensus); release ids (L6 = 25 in 18 records; lumbar rib 60/61); `CTSP\morphometrics\castellvi_grades.csv` (34); `REPO\SchwingNet\results\rare_class\transitional_subtypes.csv` ctsp rows 52 (L6 18, lumbar_rib 14, sacralised_L5_fused 12, castellvi_I_II 4, unassigned 4); registry ctsp stream rows 64 |
| VerSe / VerSeFusion | 375 entries in `~/VerSeFusion/data/unified` (374 series, 355 persons) | `~/VerSeFusion/data/unified/scan-<id>/` | VerSe expert mask `scan-<id>_msk.nii.gz` (raw VerSe ids, **no sacrum id**; many read-L6 persons carry NO id 25: 36-40 held, MAXIMIZE.md "verse held"); SPINEPS ctd-relabelled `RS/spineps/ctd_relabel/bench_ts_native/VERSE_<cid>` (5,984 files incl. TS v2; `~/bench_ts/spineps/native_ctd` same content); TS 2.18.0 `RS/anomaly_harvest/verse/ts` (388) | `~/bench_ts/spineps/native` (4,814 files) is RAW for 1,468 of 1,484 masks: never read; use `native_ctd` / `ctd_relabel` | mixed: TL in FOV 258/374 (A), LS 254-290; thoracic anchored (T1) 130 (A) | Loffler 2021 two-neuroradiologist read via `REPO\SchwingNet\results\transitional_registry\verse\screened.csv` (374 rows; `read_subtype`: normal 173, L6 87, castellvi_I_II 28, unassigned 24, lumbar_rib 13, sacralised_L5_fused 13, T13 6; 30 no read; `read_structure` e.g. 7/12/6/5); `~/lstv_flag/sources/TRANSITIONAL_LABELS.csv` on the grid; VerSe table cannot separate Castellvi I from 0 (lstv_flag_labels_v2.py docstring) |
| TotalSegmentator v2 (v201) / v3 (v300) | v201 1,228 subjects under `~/data/TotalSegmentator/s####/` (1,235 entries); v300 1,940 entries `~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300` (1,939 folders, 1,935 distinct scans after 4 duplicate folds) | same | dataset's own TS masks (per-structure); SPINEPS via `~/bench_ts/spineps/native_ctd` (relabelled) and `RS/spineps/tsv3` (6,033 files: 1,116 symlinks into bench_ts are RAW, 416/500 fresh runs named) + `RS/spineps/tsv3_ctd` (6,199); TS `total` for reader B: `RS/anomaly_harvest/totalsegmentator/{v201,v300}` | mixed; guard required per mask | 162 scans have no vertebra; TL junction in field 770, LS 815, both 725; labeller B lumbar count 685, thoracic (C7-T1) 185 (TS stream SUMMARY) | NO radiologist read; stream rows 1,935 (L6 22 [14 two-labeller], T13 4, unassigned 26, unresolved 74); `ts12_ctd_subtypes.json` corrected by `SchwingNet\results\spineps_ids\TS12_VERIFY.md` (s1178 refuted; s1088/s1123 rib-less 20th vertebra) |
| COBRA2026 planning CT + CBCT | 692 cases | `RS/cobra2026/cases/<case>/` (ct_def; `cbct_clinical.mha` / `cbct_rtk.mha`) | SPINEPS post-fix `RS/cobra2026/lstv` (696 entries; `lstv/seg` 575/580 named), `cobra2026/seg/spineps_v2` (288/290 named), `RS/spineps/cobra_varian` (101/101); patched ladder `RS/or_ready/auto_reference/readersAB/spineps/cobra_{ct,cbct}_patch`; TS `RS/anomaly_harvest/cobra/ts` (716); CBCT TS `RS/or_ready/auto_reference/ts/cobra_cbct` | `RS/cobra2026/seg/spineps` (Elekta v1) is RAW 146/141: never read | LS junction in field 692/692; TL reference established only 198 (494 junction-only); T1 in field 3; CBCT: A/B no_count on 691-692 | none human; screen calls (VERIDAH) unverified: 91 transitional test persons (L6 38, T13 45, four_lumbar 8) of which 27 L6 see no L1 and 7 T13 name L1-L4 only (split_plan.md L40-41); ALL persons are real-frame TEST |
| C-ArmLSpine CBCT | 149 | `RS/carmlspine/nifti` (298 files) | SPINEPS `RS/carmlspine/spineps` (751 files; 296/297 named) + `spineps_retry134`; TS `RS/carmlspine/ts` (149), `ts_s1` (149) | named | lumbar-only CBCT: TL 0/149, LS 6-145 depending on reader; no rib in field; all readers no_count | CBCT labels: case42, case121, case136 L6 (real-frame TEST) |
| CTSpine1K (HF mirror) | 1,005 volumes on disk (782 are CTSP persons by TCIA PatientID crosswalk; 223 screened: MSD-T10 150, COVID-19 40, HNSCC 31, COLONOG 2) | `RS/ctspine1k/raw_data/{volumes,labels}` (4 subfolders each) | CTSpine1K release annotation (VerSe-like ids, no sacrum id); other_ct stream SPINEPS + TS under `RS/anomaly_harvest/other_ct/` | other_ct harvest post-fix | MSD-T10 abdominal: LS countable 138, TL 93 of 223; HNSCC 31/31 no count | README expert lists "Sacral Lumbarization"/"Lumbar Sacralization" -> `other_ct/ctspine1k_release_reads.csv` (tier read: L6 1, sacralised_L5_fused 2); two-labeller L6 2 |
| RibFrac | 660 chest CT | `RS/ribfrac/images` | other_ct stream (SPINEPS 655, TS 660) | post-fix | cage countable from T1 in 626; sacrum reached in 9 | none; T13 4 single-labeller, L6 1 morphology-only |
| RSNA 2022 cervical | 2,022 | (headers only) | none segmented | -- | max craniocaudal 334 mm: no junction ever | -- |
| DeepFluoro / Geneva / SpineSAC / Ljubljana | 6 / 1 / 3 / 1 | `RS/deepfluoro_vendor`, `RS/geneva_hip_src`, `RS/spinesac`, `RS/ljubljana` | SPINEPS `_veridah` relabels (plain masks RAW) | mixed | no junction (pelvis / phantom / isolated vertebrae) | real-frame TEST, not persons (phantoms) |
| validation_ts (outside-labelled 70 CTs) | 70 | `RS/validation_ts/raw` | acquisition_screen (SPINEPS 270 files, TS, labeller_b 70, calls 70) | post-fix | -- | `RS/anomaly_harvest/validation_ts/VALIDATION.md`, `t13_check` (outside check of VERIDAH T13) |

Acquisition (scoping-review) collections, `RS/<collection>/{fetch,raw[,nifti]}` with the two-labeller screen in
`RS/anomaly_harvest/<collection>/` (`tools/acquisition_screen.py`: convert -> ts -> gate -> spineps -> call ->
summary). SPINEPS here is post-fix (harvest by `acquisition_screen.py`, 2026-09-24). Screens still running:
`squeue` showed `acq_ts_abdomenatlas3_mini` x10 running 12.6 h, `acq_ts_tcia_fdg_pet_ct_l` 3 running / 3 pending,
`acq_sps_idc` x4 running; 103 jobs in the queue (all acq_* at Nice 100000).

| collection | cases.csv rows | TS / labeller_b | SPINEPS files | calls | rows.csv | state |
|---|---:|---|---:|---:|---:|---|
| amos22 | 723 | labeller_b 723 | 2,884 | 723 | 723 | complete (SUMMARY.md; review 46) |
| nlst_pilot | 500 (nifti 500) | 500 | 1,960 | 500 | 500 | complete (T13 9.3 % rate refuted: ACQUISITION_PLAN s11) |
| ctpelvic1k_clinic | 172 | 172 | 25 | 172 | 172 | complete |
| csi2014 | 20 (nifti 20) | 20 | 81 | 20 | 20 | complete |
| curvas | 70 | 70 | 209 | 52 | -- | calls partial |
| curvas_pdacvi | 101 | 101 | 289 | -- | -- | gate done, calls pending |
| aortaseg60 | 55 | 55 | 117 | -- | -- | gate done |
| deep_psma | 53 | 53 | 97 | -- | -- | gate done |
| quadra_hc | 48 | 48 | 45 | -- | -- | gate done |
| waw_tace | 228 | 228 | -- | -- | -- | gate done, no SPINEPS yet |
| barts_crl | 212 | 159 | -- | -- | -- | TS partial |
| pengwin2026 | 340 (nifti 340) | 210 | -- | -- | -- | TS partial |
| idc | 3,499 (nifti 3,507) | 3,499 | 218 | -- | -- | SPINEPS running |
| kidney_thoraxabdomen | 215 (nifti 215) | -- | -- | -- | -- | converted only |
| tcia_fdg_pet_ct_lesions | 900 (nifti 900) | -- | -- | -- | -- | TS running |
| abdomenatlas3_mini | 7,649 | -- | -- | -- | -- | TS running (x10 GPU) |

Registry state: `REPO\SchwingNet\results\transitional_registry\registry.csv` (6,113 rows, one per person;
subtype L6 146, T13 14, sacralised_L5_fused 27, castellvi_I_II 31, lumbar_rib 26, unassigned 62, unresolved 129;
truth_tier read 360, two-labeller 1,401, single-labeller 238, morphology-only 4, none 4,110; `junction_ls_in_fov`
True 2,010 / `junction_tl_in_fov` True 2,049). `REGISTRY.md` table A gives persons per subtype x tier x CT-only/real.
`maximize/MAXIMIZE.md` (from `REPO\tools\rare_class_maximize.py`): 196 rendered transitional CTs; 54 held by the
ID guard (10 CTSP two-labeller L6 whose v11 label stops at 24/26: 0090 0105 0359 0474 0544 0552 0672 0895 1151
1153; 2 CTSP four-lumbar 0349 1000; 37 VerSe read-L6 with no id 25; verse559; 2 CTSpine1K MSD-T10) awaiting
Greg's relabel decision; `waiting.csv` 52 persons (single-labeller / morphology-only / real-frame).

Frozen inputs the classifier must reuse verbatim: `REPO\SchwingNet\results\fig6\frozen\v1\{split_final.json,
transitional_subtypes.csv, stratify.json, patient_keys_final.json, ts12_subtype_override.json,
transitional_registry\verse\screened.csv}` (SHA256SUMS.json).

## 4. Existing morphometry code that measures vertebral geometry from masks

| code | measures | frame / definition | status and traps |
|---|---|---|---|
| `OSTK\ostk\morphometry.py::level_morphometry(label, affine, level_id)` L380 | VBHa/VBHp, EPWu/EPWl, EPDu/EPDl, SCW/SCD, PDW_l/PDW_r/PDW, plate_rms_mm (Panjabi 1991/1992 nomenclature) | vertebra's OWN frame from fitted end-plates (`vertebra_frame` L77); landmark to landmark; plate RMS > 2 mm drops the level | output for CTSP: `CTSP\morphometrics\ostk_level_morphometry.csv` (4,744 rows: case, level, 12 measures). Canal closes the ring before finding the hole; obliquity correction only here, not in the extraction script. Uses `labels_for` scheme detection. |
| `OSTK\ostk\vertebral_body.py` | `body_mask` L535 (cut at the canal's anterior wall), `canal_mask` L98, `endplate_corners_body` L318, `body_quad_corners` L602 | | at L4/L5 the canal cut keeps TP/pedicle shoulders (LEVEL_MORPHOMETRY.md s2): end-plate width and pedicle width at L5 withheld from the atlas |
| `CTSP\scripts\extract_surgical_morphometrics.py` | canal AP (`_canal_column` L240, `_canal_ap` L337: pedicle slab = central half of the closed-ring column, +/-1.5 mm midsagittal chord, median over slab), pedicle widths, crest, LL, bi-iliac | scanner axes (obliquity not corrected) | `CTSP\morphometrics\surgical_morphometrics.csv` (802); rib bases read from `dataset_labels.json` per worker (hardcoded base once moved rib12_to_crest in 237/802) |
| `CTSP\scripts\extract_level_gradients.py` | endplate_width, body_height (ant/post), canal_width, tp_span, wedge_ratio for T11-L5 | body isolated by the canal wall | `CTSP\morphometrics\level_gradients.csv` (802); bit-identical between v10 and v11 |
| `CTSP\scripts\extract_transition_morphometrics.py` | sacral foramina count (thin coronal slab; 4 pairs normal, 5 = absorbed L5), non-rib-bearing count, Castellvi proxies (lowest lumbar lateral span, TP-to-ala gap per side), L5-S1 / L4-5 disc ratio (`_disc_height_mm` L180, a column-restricted height, NOT a minimum distance), rib 12 / rib 11 length (PCA axis, `_pca_length` L99) | label-independent where possible | `CTSP\morphometrics\transition_morphometrics.csv`. Docstring records two defects: `tp_gap` as a min distance read the L5-S1 facet (3.4 mm) and a Castellvi screen on it recovered 0 % of positives; `disc_above` as min distance between whole vertebrae read the facets (1.7-4.9 mm). "The minimum distance between two bones is almost never the measurement you wanted." |
| `CTSP\scripts\screen_castellvi_type1.py` + `tp_height.csv` (802; `tp_height_{left,right}_mm`, `tp_height_slab_*`, `tp_tip_components_*`) | Castellvi I metric criterion (>= 19 mm rostrocaudal TP) | largest connected component, not slab max-min (case 0512: 43.2 vs 16.0 mm) | 34.1 % of cohort >= 19 mm vs Hanhivaara 19.7 % Type I: a high-sensitivity pre-filter (769 -> 214), not a classifier (two of Castellvi's three conditions unmeasured) |
| `CTSP\scripts\screen_missed_castellvi.py` + `docs\CASTELLVI_SCREEN_BLIND_SPOT.md` | PU ranking on TP span / gap features against 33 graded cases | | recovers grades with a surviving free process (IIb median LOO rank 4, IIIa 25, IIa 58) and misses IIIb (442) / IV (378): a fused process is labelled SACRUM, so the free vertebra looks ordinary. Sacral width/height do not show fusion (z -0.16 / +0.11). Proposed fix: S1 ala left-right asymmetry (`CTSP\morphometrics\sacral_ala.csv` exists: `ala_rise_{left,right,max,asym}_mm`, 802 rows). |
| `CTSP\scripts\test_morphometric_separability.py` | T11/T12 vs L1-L5 on per-level features normalised by the case's own median; grouped CV by case | | premise test for "shape, not size"; `REPO\tools\tp_morphology.py` states the atlas separates T12 from L1 hardly at all (VBHa d=0.80, PDW 0.54, EPW 0.14, canal AP 0.00) |
| `REPO\tools\tp_morphology.py` (`tp_metrics` L65) | per side: TP `reach_mm` lateral to the body edge, `thickness_mm` (sqrt area at the pedicle), `slenderness` = reach/thickness (lumbar blade high, thoracic club low) | axes from the affine, never array order | the one existing feature aimed at IDENTITY rather than position; sides separate (unilateral lumbar rib is a phenotype) |
| `CTSP\scripts\detect_stump_ribs.py` (`_rib_length_mm` L54, `analyze` L68) | rib on L1 (id 20) or lowest rib <= 38 mm = stump/TLTV marker; whole v4 dataset | Moller 38 mm | release-label based; QC blind to a rib TS never numbered |
| `REPO\tools\lstv_flag_labels.py` / `lstv_flag_labels_v2.py` -> `REPO\SchwingNet\results\polypose\inputs\lstv_flag_labels_v2.csv` (1,112 rows, cohort ctsp + verse) | per-case label-derived facts: has_L6, n_lumbar_labelled, n_presacral_mobile, has_lumbar_rib, has_T13_vertebra/rib, n_rib_bearing, ribs per side, sacrum/S1 voxels, fov_has_{sacrum,T12,L1,rib12,femur}, z landmarks; joined `lstv_label`, `castellvi_type`, `LSTV_flag` (164 pos), `TLTV_flag` (113 pos) | v10 ids (note S1 = 29 there: pre-v11) | labels from the LABEL SOURCE (manifest read / Loffler table), not a segmenter's names; verse707 dropped as a table/mask conflict; VerSe negatives contaminated with Castellvi I |
| `REPO\tools\lstv_flag_train.py` / `lstv_flag_eval.py` | existing 2-D flag: 5-fold PATIENT-level CV, ResNet-18/50 on renders, OOF pooled, tau + abstention in eval | | the fold and operating-point machinery a CT-feature classifier can copy (patient-grouped folds, val-set tau, coverage beside accuracy) |
| `REPO\tools\transitional_mask_census.py` | per label voxel count, S-I extent, centroid; sacrum components; gap lowest presacral body -> sacrum top; midsagittal PNG | canonical RAS for analysis only | the "render the mask" tool; `fused_mask_representation` column in the registry |

Documented traps that apply to any new feature (`CTSP\docs\LEVEL_MORPHOMETRY.md`, `CTSP\CLAUDE.md`):
1. A maximum extent is not a diameter (trefoil L5 canal read 21.0 vs published 15.6-19.7); a first-slice-that-works
   is not a plane (473 -> 12 records under 11 mm after fixing). Reproduce the published DEFINITION.
2. Spread, not the median, catches a broken per-level measurement: compare the SD against the widest published
   living-cohort SD and the share past a threshold against the published prevalence of the condition it defines.
   For this classifier that is the prevalence check on the census (LSTV 4-30 % by definition; L6 ~3 %; four lumbar
   ~1.6 %; T13 0.6-2 %: `tools/acquisition_census.py` priors with citations).
3. Render the mask: three analytically reasonable L5 end-plate fixes were all wrong; one render settled it.
4. Two label schemes and mixing does not raise; `labels_for(volume)`, never a fixed map. Id 29 retired in v11.
5. Minimum distance between two bones finds a facet, not the disc or the ala gap.
6. A fused transverse process is labelled sacrum: a Castellvi III/IV measured on the free vertebra looks ordinary.
7. `as_closest_canonical` + `nib.save` transposes a label; canonicalise to ANALYSE, never to WRITE.

## 5. What is NOT there (gaps a design must state)

- No human read exists for TotalSegmentator, COBRA, C-ArmLSpine, RibFrac or any acquisition collection; the only
  read sets are CTSP (34 Castellvi + release ids) and VerSe (Loffler table, 171 read-subtype series). T13 truth is
  n = 4 (VerSe 6 read persons, 4 in calibration); four_lumbar n = 5 (alt 15). No automated reader can be certified
  on those two phenotypes with the present reads; the design must say so and route them to the candidate tier.
- VerSe's table cannot separate Castellvi I from grade 0 (181-subject shared cell) and CTSP's Castellvi I screen
  measures one of three criteria: a "Castellvi I" phenotype has no clean truth anywhere.
- Reader D is vacuous (CBCT); COBRA has 494 junction-only fields and T1 in 3 CTs, so COBRA cannot yield a T13
  phenotype at all and its lumbosacral calls are unverified.
- TS `sacrum` excludes S1 (memory ts-sacrum-excludes-s1); VerSeFusion unified masks carry no sacrum id; CTSpine1K
  annotations carry no sacrum id. A sacrum-dependent feature must name its sacrum source per collection.
- `patient_keys.SCHEMES` lacks the oblique-render and `ctspine1k_<stem>` rules; every ann carries `patient_key`
  explicitly, so a bank must key on the ann field until the table is extended.
- No per-case reject rule for a morphometric measure exists in the literature (LEVEL_MORPHOMETRY.md "Still open");
  the gates here are constructed over cited numbers.
- The 10 CTSP + 37 VerSe + 2 CTSpine1K L6 persons whose masks lack id 25, and the 2 CTSP four-lumbar, are HELD
  pending Greg's decision; they are exactly the L6 positives a classifier would most want.
