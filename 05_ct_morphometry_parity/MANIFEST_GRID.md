# MANIFEST_GRID.md: every grid path this project uses or produced

`HOME` = `/wsu/home/go/go24/go2432` (Panasas, 4.3 TB soft quota, 4,050 GB used on 2026-10-07 per
`data_platform/DATA_MANIFEST.md` line 28). `RS` = `/rs/rs_grp_oschome/go2432` (CephFS, 20 TB, group `oschome`). Login
`go2432@grid.wayne.edu`; CPU partition `reqp --qos=requeue`; Python `HOME/mambaforge/envs/spineps/bin/python` (3.11.16;
nibabel 5.4.2, numpy 2.2.6, scipy 1.15.3, scikit-image 0.25.2, pandas 2.3.2, scikit-learn 1.7.2, matplotlib 3.11.1; no
pyarrow, lightgbm, xgboost or shap: `results/reader_e/CODE_MAP.md` section 1). Nothing runs on the login node.

Sources of every row: the one read-only grid pass of 2026-10-08 22:20 UTC (`ls`, `cat` of small files; the transcript is
`../10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`, its `=== ls HOME` block at lines 24-1353 and its
`=== STATUS files` block at lines 2052-2135; called "the pass" below, cited by line), `../_plan/PLAN.md` section 3 (05)
"Grid paths it owns",
`spinesurg-ct-nnunet` 097933a `data_platform/{DATA_MANIFEST,MIGRATION_PLAN,LAYOUT}.md` and `plan/batch_items/*.tsv`,
`results/reader_e/CODE_MAP.md` (2026-09-24), and the memory notes. "VERIFIED" means the batch's `STATUS` file on the grid
(`HOME/spinesurg-ct-nnunet/data_platform/plan/runs/<B>/STATUS`, read in the pass) carries `VERIFY_OK` with matching file and
byte counts. "Not recorded" means no file read says.

## 1. The release this project measures

| path | holds | size | migration state | verified |
|---|---|---|---|---|
| `HOME/data/CTSpinoPelvic1K` -> `RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` | release v11: `labels/` 802 files (2026-09-16 09:21), `labels_v10/` 802 (2026-09-07), `ct/` 802 (2026-09-23 03:03, after the 0533 repair), `labels.zip`, `manifest.json`, `splits_5fold.json`, `dataset_labels.json` (v11, 2026-09-11), `dataset_labels_v10.json`, `SHA256SUMS.txt`, `KNOWN_ISSUES.md`, `README.md`, `fetch_from_tcia.py`, `reconstruct_ct.py` (the pass, `ls ~/data/CTSpinoPelvic1K`) | `labels.zip` 883,912,953 B; `manifest.json` 1,100,037 B; `splits_5fold.json` 247,222 B; `SHA256SUMS.txt` 73,633 B; label and CT folders not sized | on Ceph; the HOME path became a symlink on 2026-10-08 08:11; `HOME/data/CTSpinoPelvic1K.pre-ceph` (2026-09-16) still beside it | VERIFIED: B02 item 001, `VERIFY_OK`, files 2,417 / 2,417, bytes 196,195,055,488 / 196,195,055,488, sampled 200, flags `hardlink_group,irreplaceable` (the pass, line 2063) |
| `HOME/CTSpinoPelvic1K` | git clone of CTSpinoPelvic1K, `master` at a0c5139 (2026-09-07) with 133 dirty status lines; `scripts/` line-identical to the laptop for `extract_transition_morphometrics.py` (507 lines), `measure_sacral_ala.py` (233), `measure_tp_height.py` (243); `extract_level_gradients.py` differs (430 vs 423) and must not be imported from there (`results/reader_e/CODE_MAP.md` section 1) | 1,945.6 GB for the whole tree including `data/` (listing 2026-09-13, `DATA_MANIFEST.md` line 18857) | HOME; its `data/` subtree moves in batch B02 (`plan/batch_items/B02.tsv`: `hf_export_*`, `v5_final`, `s1_recarve`, `zenodo_*` to `RS/data/ctspinopelvic1k_build_tree/derived/`) | B02 items 002-024, 026 and 030 (`hf_export_*`, `placed`, `zenodo_*`, `v5_final`, `s1_recarve`, `hardware_*`, `fix_0816*`, `hip_*_backup`, `v5_smoke`, `thoracic_fix`) read ABSENT at 22:20 UTC 2026-10-08, not yet copied; items 025 and 027-029 (`0816_label_v4.nii.gz`, `build_archive*`) VERIFIED (the pass, lines 2064-2092) |
| `HOME/CTSpinoPelvic1K/morphometrics` | the committed tables plus files not in the laptop copy: `fig_anatomical_report.png`, `fig_foramina_sweep.png`, `fig_transition_landscape.png`, `foramina_param_sweep.csv`; no `label_census_v11.csv` there (the pass, `ls`) | not sized (plain `ls`) | HOME | whether `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv` were recomputed on v11 here is not shown (`OPEN_QUESTIONS.md` B27): read the mtimes with `ls -l` first |

## 2. What this project produced on the grid (2026-09-10 and after)

| path | holds | size | migration state | verified |
|---|---|---|---|---|
| `RS/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/` | `ostk_level_morphometry.csv` (the ostk per-level run, commit 90a27a7, before the regression), `pi_ostk2.csv`, `pdw_why.py`, `pitest/` (10 release label copies: 0024, 0182, 0375, 0401, 0569, 0624, 0760, 1043, 1084, 1129), `pdwtest/` (2: 0010, 0038); what `pitest` and `pdwtest` stand for is not recorded (`MIGRATION_PLAN.md` section 5) | 302,994 B; 662 B; 1,761 B; 13,899,387 B; 2,710,749 B | batch B14, cut over 2026-10-08 11:02; HOME-root symlinks `~/ostk_level_morphometry.csv`, `~/pi_ostk2.csv`, `~/pdw_why.py`, `~/pitest`, `~/pdwtest` point here; `~/pdw_why.py.pre-ceph` and `~/pi_ostk2.csv.pre-ceph` remain | VERIFIED: B14 items 003-007, `VERIFY_OK`, bytes matched, every file sampled (the pass, B14 STATUS). `pitest`/`pdwtest` are deletion candidates not yet compared with the release labels |
| `HOME/spinopelvic_all.csv` | the spinopelvic table of 2026-09-10 13:27 | 63,562 B | HOME root; listed among the 24 family-E entries of `DATA_MANIFEST.md` line 628, in no batch item file | no |
| `HOME/agg_spinopelvic.py` 4,259 B, `show_pi.py` 276 B, `ss_probe.py` 2,671 B, `disc_probe.py` 1,873 B, `disc_probe2.py` 2,955 B, `height_probe.py` 5,198 B, `cmp_pdw.py` 1,480 B, `lm_probe.py` 762 B (all 2026-09-10) | the spinopelvic estimator probe scripts; in no repository as far as recorded (`../_plan/PLAN.md` section 3 (05) "Grid paths it owns"); listed in the pass at lines 329, 1116, 1141, 564, 565, 703, 470 and 748. `height_probe.py` is also tracked in CTSpinoPelvic1K `scripts/` (whether the two are identical is not recorded) | as listed | HOME root; not scheduled | no |
| `HOME/ostk.tgz` (2026-09-10 04:10), `HOME/ostk_run/` (06:03; holds a second scratch copy of OpenSpineToolkit, `CODE_MAP.md` section 1), `HOME/ostk_shards/` (12:26, 12 entries), `HOME/ostk_morph_out/` (04:11) | the 2026-09-10 shard run of per-level morphometry and pedicle width: the run whose `PDW` column came back empty (`OPEN_QUESTIONS.md` D2) | `ostk.tgz` 186,470 B; folders not sized | HOME root; family-E entries, no batch; role beyond name not recorded (`DATA_MANIFEST.md` unknown row 6) | no |
| `HOME/logs_ostkmorph_40183643.{out,err}` (11,438 B / 0 B), `logs_ostkmorph_40183680.{out,err}` (32 B / 81 B); `logs_ostkext_40183713_*`, `logs_peddev_*`, `logs_pedbatch_*`, `logs_rheight_*` (the pass: lines 856-859; `logs_ostkext_40183713_*` 96 files at lines 760-855, `logs_pedbatch_*` 2 at 860-861, `logs_peddev_*` 20 at 862-881, `logs_rheight_*` 2 at 888-889) | the job logs of that day | small | HOME root | no |
| `HOME/height_renders/` (2026-09-10 03:25), `HOME/ped_renders/` (04:42) | the body-height renders behind `docs/BODY_HEIGHT_INVESTIGATION.md` and the pedicle renders | not sized | batch B10 -> `RS/data/ctspinopelvic1k/derived/height_renders`, `.../ped_renders` (`plan/batch_items/B10.tsv` lines 39, 49); `RS/data/ctspinopelvic1k/derived` did not exist at 22:20 UTC on 2026-10-08 (`ls` error in the pass): B10 not run | no |
| `RS/data/ctspinopelvic1k_build_tree/derived/s1v11/` | the v11 build workspace (2026-09-11 to 18): copies of `merge_s1_into_sacrum.py`, `audit_s1_carve.py`, `check_s1_merge.py`, `extract_surgical_morphometrics.py`, `compare_v10_v11_spinopelvic.py`; logs of jobs 40198228 (s1_v11), 40198880 (v11_morph), 40309073 (verify_v11), 40309160 (package_v11); `out/v11_labels`, `out/s1_carve_audit.csv`, `morphometrics/surgical_morphometrics.csv`, `out/dataset_labels_v11.json`; the Zenodo v11 upload scripts and state (`DATA_MANIFEST.md` line 815; `MIGRATION_PLAN.md` line 248) | 835 files, 1,189,924,200 B | B14, cut over 2026-10-08; owner-only (`drwx--S---`) until its upload scripts are read for a token (Greg) | VERIFIED: B14 item 008, sampled 200; restricted, irreplaceable |
| `RS/data/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz` | pelvis-propagation QC renders (03's; listed because it sits beside the scratch) | 196,147,947 B | B14 | VERIFIED (item 001) |

## 3. Reader E (ostk as a reader over five mask families; 2026-09-24/25)

| path | holds | size | migration state | verified |
|---|---|---|---|---|
| `RS/data/or_ready/auto_reference/readerE/` | J0 (60 CT-segmenter pairs), J0bis, J1 (`j1/_collect/features_j1.csv` 38,432 instance rows, `features_index.csv` 3,524 pairs), `j1v3/_collect/` (the features v3 rerun), `j2/mask_bits_j1.csv.gz`; made by jobs 40438613, 40438806, 40438897, 40443093, 40443305-08, 40443310, 40448877 (`results/reader_e/sacct_*.txt`, `j2/J2_GATE.md`, `j2v3/J2_GATE.md`) | `features_j1.csv` 40,334,008 B on the laptop copy; the rest not sized | Ceph-native (made under `RS`); no migration | the J2 jobs read them and returned rc 0; no VERIFY line applies |
| `RS/data/or_ready/auto_reference/lists/{ctsp,verse,ts12,cobra_ct,cobra_cbct,carmlspine}.csv`; `readerC/<corpus>/json/`; `readersAB/{a,b}/<corpus>/<case>.json` | reader E's inputs: the CT and mask lists, reader C's calls, readers A/B's guard records (`CODE_MAP.md` section 1) | not sized | Ceph-native | n/a |
| `RS/data/spineps/ctsp/CTSP_<case>_{seg-vert_msk,seg-spine_msk}.nii.gz` + `_ctd.json` (801 masks); `RS/data/spineps/ctd_relabel/bench_ts_native/VERSE_<cid>_*`; `HOME/bench/spineps/native_ctd/COLONOG_<n>_*` (796) | the SPINEPS post-fix stores: the corpus (subregion) label CT-5 needs; every id passes `tools/spineps_ids.py assert_verse_monotonic` first | not sized | owned by 10 and 06 | n/a |
| `HOME/bench/totalsegmentator/native/COLONOG_<n>.nii.gz` (804) + `class_map.json`; `RS/data/anomaly_harvest/verse/ts/<cid>.nii.gz` + `class_map.json` | TotalSegmentator v2 `total` outputs; the COLONOG number is not the case id (map in `tools/rib_count_ts_prep.py`); TS `sacrum` and `vertebrae_S1` are disjoint | not sized | owned by 10 | n/a |
| `HOME/VerSeFusion/data/unified/scan-<cid>/scan-<cid>_{ct,msk}.nii.gz` | VerSeFusion expert masks (VerSe alphabet, no sacrum id) | 139.0 GB raw (listing 2026-05-13) | batch B06 (`RS/data/versefusion/raw/VerSeFusion_data` exists, 2026-10-08 07:18) | B06 finalisation unrecorded (`RESEARCH_DIRECTIONS.md` 5.2) |

## 4. VerSeFusion measurement derivatives

| path | holds | size | migration state | verified |
|---|---|---|---|---|
| `RS/data/versefusion/derived/vf_v10/` (`HOME/vf_v10` is a symlink since 2026-10-08 12:35; `HOME/vf_v10.pre-ceph` remains) | `vf_813` relabelled to the CTSP v10 ids for measurement; regenerable; v10 ids include 29, so any sacral column from it needs the v11 semantics; used by `slurm/tp_morphology.sh`, `versefusion_qc.sh`, `versefusion_tl_morphometrics.sh` (`MIGRATION_PLAN.md` line 339) | 374 files, 319,212,368 B | B06 | VERIFIED: B06 item 014, 374/374 files, bytes matched |
| `HOME/vf_morphometrics/` | VerSeFusion morphometrics output (mtime 2026-09-12; `DATA_MANIFEST.md` lines 1473, 1498, 1528) | not sized | HOME; batch not recorded in what the pass read | no |

## 5. Code on the grid that this project calls

| path | holds | state |
|---|---|---|
| `HOME/OpenSpineToolkit/` | an rsync copy of ostk; no `.git` (`cat .git/HEAD` failed in the pass); commit unknown; whether the 1b7005c regression is in it is `OPEN_QUESTIONS.md` B29; not installed in the spineps env: `export PYTHONPATH=$HOME/OpenSpineToolkit:$HOME/spinesurg-ct-nnunet/tools${PYTHONPATH:+:$PYTHONPATH}` (pattern in `slurm/polypose_check.sh` lines 37-38) | refresh from OpenSpineToolkit `main` after 04's fix; never trust its VBHp / EPD until then |
| `HOME/spinesurg-ct-nnunet/` | git, `L6_Class`; at `c0b752a4` on 2026-09-24 (three commits behind the laptop then); ship by commit, push and `git pull --ff-only`, never scp | the reader E tools and `tools/spineps_ids.py` run from here |

## 6. What is NOT on the grid, or not done there

- No v11 recompute of `pelvic_shape.csv`, `transition_morphometrics.csv`, `degenerative.csv`, `opportunistic.csv`,
  `proximal_femur.csv` is recorded anywhere (`OPEN_QUESTIONS.md` B27, F9; `RESULTS_CATALOG.md` F.44).
- No anterior-pelvic-plane fit exists (C8); no LSTV-stratified pelvic-incidence analysis (C9).
- No ratio-only single-vertebra separability result (PAR-1) is on disk anywhere.
- No projected-landmark bank carries pedicle, canal, process, rib facet or the S1 plate (PAR-2 step 1); the `xrsp1k`
  lateral render bank sits on dangling symlinks to a deleted export and must be rebuilt from v11
  (`RESEARCH_DIRECTIONS.md` 3.3).
- Reader E J3 was never submitted; after the features v3 rerun the gate still fails on EPWl for want of a lower-plate
  yardstick (`results/reader_e/j2v3/J2_GATE.md`).
- The 2026-09-10 shard run's pedicle columns: produced for about 2 of 5,600 level-instances; cause not established (D2).
- Batch B10 (`height_renders`, `ped_renders`, `postop_render`, `rib_fragments_*`) had not run at 22:20 UTC 2026-10-08.
- The HOME-root probe scripts and `spinopelvic_all.csv` are in no repository; whether `~/height_probe.py` equals the tracked
  `scripts/height_probe.py` is not recorded.
