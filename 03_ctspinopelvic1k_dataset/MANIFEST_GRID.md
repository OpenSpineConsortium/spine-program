# MANIFEST_GRID — what this project holds on the grid, and what is not there

Written 2026-10-08 from the read-only grid listing of 2026-10-08 22:20 UTC (kept in project 10 as
`grid_ls_2026-10-08.out`; no folder re-runs it), the migration records `ssn:data_platform/{DATA_MANIFEST,
MIGRATION_PLAN,LAYOUT}.md` and `plan/runs/<B>/STATUS` as read in that pass, `docs/handoff/INFRASTRUCTURE.md`,
`docs/handoff/RECIPES.md` section 9 and the memory notes named per row. Sizes are quoted as the file that
recorded them gives them (bytes from a STATUS file; GB from the 2026-10-08 census); "not sized" means no
file records a size. "VERIFIED" means a migration job checked the copy (sampled hashes and link counts);
"listed only" means the 2026-10-08 `ls` saw the path and nothing checked its content.

`HOME` = `/wsu/home/go/go24/go2432`. `$RS` = `/rs/rs_grp_oschome/go2432`. Login `go2432@grid.wayne.edu`;
nothing runs on the login node (`CLAUDE.md` rule 7). `~/data/CTSpinoPelvic1K` is a symlink to the Ceph
copy; in a student's shell `~` is the student's HOME, so write the full path.

## 1. The release and its build (Ceph)

| path | holds | size | migration state | verified | notes |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` | the v11 working copy: `ct/` (802), `labels/` (802, written 2026-09-16), `labels_v10/` (802), `labels.zip` 883,912,953 B, `manifest.json` 1,100,037 B, `splits_5fold.json` 247,222 B, `dataset_labels.json` 4,100 B, `dataset_labels_v10.json`, `KNOWN_ISSUES.md` 8,894 B, `README.md` 20,159 B, `SHA256SUMS.txt` 73,633 B, `LICENSE`, `fetch_from_tcia.py`, `reconstruct_ct.py` | 196,195,055,488 B, 2,417 files (B02 STATUS) | B02 cut over 2026-10-08; `~/data/CTSpinoPelvic1K` is the symlink; the HOME original `.pre-ceph` is kept | VERIFIED (200 sampled, link counts; `labels/` checked file by file against Zenodo's SHA256SUMS per `dp:dedup/DEDUP_PLAN.md` section 7 row 5) | **the only grid copy of the 802 CTs and of the v11 labels**; the HF mirror still serves v10 (`memory/hf-mirror-is-v10.md`); set `D=/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` for every recipe in `docs/handoff/RECIPES.md` section 9 |
| `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K.pre-ceph` | the HOME original of the v11 working copy | 196 GB (census) | kept until FINALIZE, which is Greg's call and the only step that frees HOME | — | `OPEN_QUESTIONS.md` A26 |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive` | staging of the published build archive, Zenodo 10.5281/zenodo.22647933 (tag `v10-build-archive`; `docs/ctsp/BUILD_CHAIN.md`) | 13 files, 6,236,530,062 B (B02 STATUS) | B02 cut over | VERIFIED | deletion candidate in the migration plan but the only grid copy of the archive |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_stage` | build-archive staging tree | 2,474 files, 3,035,170,658 B | B02 cut over | VERIFIED | deletion candidate |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` | one file | 592 B | B02 cut over | VERIFIED | owner-only (`LAYOUT.md` rule 8) |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` | **the v11 build workspace with the Zenodo v11 upload state**; `out/v11_labels` = the release labels byte for byte (dedup A07: 802 identical, 1.19 GB) | 835 files, 1,189,924,200 B (B14 STATUS) | B14 cut over; restricted in the plan until 2026-10-12, irreplaceable | VERIFIED | readable by approved students since visibility job 40602925 of 2026-10-12: Greg opened it without the token check (A26; issue #69) |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz` (`~/qc.tar.gz` symlink) | pelvis-propagation QC renders of 2026-06-12 | 196,147,947 B | B14 | VERIFIED | possibly the only copy (`MIGRATION_PLAN.md` section 8); the laptop twin `Desktop/CTSpinoPelvic1K/qc.tar.gz` (344 MB) was not copied |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/` | `pitest` (10 files, 13,899,387 B), `pdwtest` (2 files, 2,710,749 B), `ostk_level_morphometry.csv` 302,994 B, `pi_ostk2.csv` 662 B, `pdw_why.py` 1,761 B: the 2026-09-10 spinopelvic and pedicle-width scratch | as listed (B14 STATUS) | B14 | VERIFIED | owned by project 05; the pedicle-width question is `OPEN_QUESTIONS.md` D2 |
| `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/0816_label_v4.nii.gz` | a superseded build intermediate of case 0816 | 1,106,588 B | B02 | VERIFIED | the 0816 scripts are in `code/case_fixes/_review_0816/` |
| `/rs/rs_grp_oschome/go2432/data/ctsp0533_repair` | the CT 0533 rebuild work tree including `0533_ct.TRUNCATED.20e673dc6c2a.nii.gz` | 0.604 GB (census) | Ceph-native | sha recorded in `memory/grid-ct-0533-truncated.md`; dedup A09: release file = repair candidate | repaired 2026-09-23 (job 40416624) and the HF file replaced (40419665); `KNOWN_ISSUES.md` still lacks it (`STATUS.md` F.19) |
| `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/meta` | `patient_db.json` 9,909,285 B, `patient_db.pkl` 2,409,446 B, `patient_db_summary.txt` 663 B (May 2026) | 12.3 MB | B01 cut over | VERIFIED | **the only TCIA material left on either volume**: the raw DICOM (721 GB) and `tcia_nifti` (336 GB) were found on neither HOME nor Ceph by the dedup census, and nothing records what removed them (`OPEN_QUESTIONS.md` B30); re-acquisition route `tcia_ctsp_download` in project 10 |
| `/rs/rs_grp_oschome/go2432/data/ctsp_april` | the April 2026 release inputs (1,153 records) used for the NeurIPS SPINEPS appendix | 86.883 GB (census) | Ceph-native | listed only | world-writable (`drwxrwxrwx`; `DATA_MANIFEST.md` family A hazard 5); no byte copy of a release CT (dedup A10) |

## 2. The NeurIPS appendix chains (Ceph), cancelled 2026-09-27

| path | holds | size | state | verified | notes |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/neurips_v11` | the v11 summaries chain for Appendix J: `out/{ts,ens}/SUMMARY.md` were the targets; jobs 40480728/31/32 and 40480730/33 | 10.174 GB (census) | cancelled 2026-09-27 15:50 with everything outside `ruleclass/` (`ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`); `nv11_ts` had 6 of 16 shards done and resumes per shard | listed only | `OPEN_QUESTIONS.md` A7: resubmit or cut Appendices I-J; `TODO.md` step 2 |
| `/rs/rs_grp_oschome/go2432/neurips_tsv3` | the TotalSegmentator v3 chain (jobs 40481824-26); `total_v3` itself was never run, no job submitted (`CAMERA_READY_CHANGES.md` item 20) | 2.250 GB (census) | cancelled | listed only | run it (the 33 LSTV patients' records and the 174 held-out records, TotalSegmentator at or above its upstream release 2.15.0 with its `v3.0.0-weights` pre-release tag; both strings are TotalSegmentator's own version tags quoted as they read, not versions of this project) or cut the column |
| `/rs/rs_grp_oschome/go2432/neurips_spineps` | the SPINEPS-on-April chain for Appendix I: `score_v212/REPORT.md` was the target; jobs 40481323 -> 40481314 -> 40481315; usable only with 0 ground-truth-gate mismatches | 36 files (census) | cancelled | listed only | `CAMERA_READY_CHANGES.md` item 19 |

## 3. nnU-Net datasets, results and the benchmark (HOME)

| path | holds | size | state | verified | notes |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/raw` | `Dataset802_SpineSurgCTFull`, `Dataset803_SpineSurgCTFullMerged`, `Dataset804_SpineSurgCTFusedOnly`, `Dataset810_SpineSurgLSTVOneShot`, `Dataset813_SpineSurgLSTVFullRibs`, `Dataset815_SpineSurgLSTVVerSe` (links + `labelsTr`) | not sized | stays on HOME (B12 dropped) | listed only | `imagesTr` links are container paths: never repair them on the host (`memory/dataset813-image-links-are-container-paths.md`); Dataset815 (1,176 cases, 62 L6 by manifest) was never preprocessed (CT-6) |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/results` | results for Dataset802, Dataset810, Dataset813 | 348.6 GB (`du` 2026-09-20) | HOME; B13 optional | listed only | **no Dataset815 results** (never trained); whether the Dataset813 folds finished and were scored is not shown by the listing (`OPEN_QUESTIONS.md` C19); no evaluated single-shot model is recorded anywhere (`STATUS.md` C5.3) |
| `/wsu/home/go/go24/go2432/ablate` | the nnU-Net ablation arms `v5_all`, `v5_minus_all`, `v5_minus_extras`, `v5_minus_obl`, `v5_minus_pseudo` | 201.563 GB (census; 202-235 GB in other records) | HOME; B13 optional | listed only | outcome never read or recorded (`OPEN_QUESTIONS.md` B16; `STATUS.md` C5.1); `docs/spinesurg_ct_nnunet/ablations.md` describes the six arms |
| `/wsu/home/go/go24/go2432/bench` | the benchmark harness: `ct_by_case` (802 links), `gt`, `spineps`, `totalsegmentator`, `vista3d`, `robust`, `xr_fov`, `fov`, `patch_context*`, `latency.json`, `runtime_cost_workstation.json`, `fig_runtime_workstation.pdf`, `model_registry.csv` | 35.845 GB (census) | HOME; B13 optional | listed only | the CT competitor benchmark of `code/benchmark/` (CT-10); the C-arm files in the same folder belong to project 01 |
| `/wsu/home/go/go24/go2432/spinopelvic-seg` | the Dataset803 pseudolabeller checkout; `nnunet/raw` inspect-only in B14 | 27 GB (`du`, `MIGRATION_PLAN.md` section 10) | HOME | — | Dataset803 has no `results/` tree on the grid; its five checkpoints are on Hugging Face `OpenSpineConsortium/spinopelvic-seg-checkpoints` (`docs/handoff/RECIPES.md` section 3.2) and were read by `ctsp:scripts/extract_pseudolabel_dice.py` (`STATUS.md` F.4) |
| `/wsu/home/go/go24/go2432/NV-Segment-CTMR` | the VISTA3D-lineage competitor checkout (2026-09-08) | not sized | HOME | listed only | benchmark arm; environment built, smoke test pending (`docs/handoff/RECIPES.md` section 8) |

## 4. Repository checkouts and review material (HOME)

| path | holds | size | state | verified | notes |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` | the public repository checkout, `master` at a0c51390970f57011fdd05123745bd2d79944c91 (behind the laptop's 7ddfe38); `morphometrics/` (26 CSV/PNG), `data/` remnants (`l6_audit.json` 68,138 B, `l6_truth.json` 71,737 B, `hip_crossover_*.json`, ITK-SNAP descriptors, `qc_dashboard/`), `docs/`, `configs/`, `hardware_review/`, `gallery_*`, `fov_check/` | 7.699 GB (census) | stays on HOME | — | **flags**: `.token` (38 B, 2026-05-20) is a credential file inside the checkout, never copy; a stray directory literally named `"\` with a file `md5sum \` (2026-09-10) is a heredoc-backslash leftover; whether the sacrum-adjacent CSVs were recomputed on v11 here is not shown by names alone (`OPEN_QUESTIONS.md` B27); whether `data/v5_final` and `data/zenodo_deposit` still exist here (the `ctsp:slurm/*.sh` defaults) is not recorded (B28) |
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K-review` (2026-05-26), `/wsu/home/go/go24/go2432/ctspinopelvic1k-review-triaged` (2026-06-01), `/wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` (2026-08-10) | review Space material and ledgers | not sized | HOME | listed only | may hold reviewer usernames: **never copy** into this folder |

## 5. What is NOT on the grid, or not yet there

- The TCIA CT COLONOGRAPHY raw DICOM (721 GB) and the NIfTI conversion (336 GB): absent from both volumes;
  only `tcia_ct_colonography/meta` remains (section 1). The CTs can be rebuilt from TCIA with
  `ctsp:zenodo/fetch_from_tcia.py` and `reconstruct_ct.py` (SeriesInstanceUID in `manifest.json`).
- The v11 Croissant file: v11 carries no `croissant.json`, only v6 does (`CAMERA_READY_CHANGES.md` item 10);
  `ctsp:zenodo/make_croissant.py` regenerates it.
- The April 2026 release's 1,153-record manifests with the record-to-series map and the evaluated
  174-record split (`splits_final`): at no public location the NeurIPS paper cites; they survive in a
  Hugging Face repository history (the 1 May 2026 revision) (`CAMERA_READY_CHANGES.md` items 9, 16).
- The nnU-Net ablation results as numbers (`~/ablate` holds outputs; no table was ever aggregated; C5.1).
- Any evaluated single-shot (Dataset810/813) model; any Dataset815 training (C5.3; section 3).
- The outputs of the cancelled appendix chains (section 2), except the 6 of 16 `nv11_ts` shards.
- A v11-era `KNOWN_ISSUES.md` and `README.md` for the deposit: the laptop sidecars in `docs/release/` are
  the v10 ones (`dataset_labels.json` names "v10" and maps S1 to 29); the v11 README on Zenodo still
  carries the August Castellvi paragraph (`CAMERA_READY_CHANGES.md` item 11).
- The grid cannot fetch the private `spinesurg-ct-nnunet` remote (2026-10-08; cause not recorded,
  `docs/handoff/RECIPES.md` section 0 item 2); ship code by `git archive | ssh tar`.
- The laptop-only material of this project that has no grid copy: the CNS 2026 generators
  (`manuscripts/talks/cns2026/`), the NeurIPS camera-ready working tree (uncommitted 2026-09-27 edits and
  the untracked `src/appendix/`), the 2026-09-07 as-submitted package, the 0816 and 0068 case-fix
  scripts, the LSTV review tool packet, the 2026-05 NeurIPS benchmark outputs (`results/neurips_2026-05/`).
  All of these are now in this folder (`MANIFEST_LOCAL.md`).

## 6. Jobs named in this project's records

| job ids | what | source |
|---|---|---|
| 40220664 | the rib QC stages behind `results/ctsp_results/rib_qc_v4_vs_release/` (Table II of the article) | `results/ctsp_results/rib_qc_v4_vs_release/README.md` |
| 40416624, 40419665 | CT 0533 repair and the HF replacement, 2026-09-23 | `memory/grid-ct-0533-truncated.md` |
| 40480728, 40480731, 40480732, 40480730, 40480733 | the v11 summaries chain (Appendix J), cancelled | `manuscripts/neurips_camera_ready/CAMERA_READY_CHANGES.md` item 19 |
| 40481323 -> 40481314 -> 40481315 | SPINEPS under the protocol (Appendix I), cancelled | same |
| 40481824-26 | TotalSegmentator v3 chain, cancelled | `docs/handoff/EXTRACTS.md` M7 |

Partition for CPU work: `--partition=reqp --qos=requeue`; GPU: `--partition=gmsap,gvohp,galhp --qos=gpu
--gres=gpu:1`; Python `~/mambaforge/envs/spineps/bin/python` with `PYTHONNOUSERSITE=1` (`docs/handoff/RECIPES.md`
section 0 items 4-5). The grid's TeX carries revtex4-1 and cannot build the article; the build runs in WSL
with TinyTeX and revtex4-2 (`manuscripts/mpda/build.sh` header).
