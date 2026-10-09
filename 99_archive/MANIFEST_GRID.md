# MANIFEST_GRID for 99_archive

Every grid path this folder names, with what it holds, its size where a file records one, its migration state and
whether a job verified it. HOME = `/wsu/home/go/go24/go2432`; Ceph = `/rs/rs_grp_oschome/go2432`. Sources: the one
read-only grid pass of 2026-10-08 22:20 UTC (`10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` in this repository, 3,213 lines;
"GRIDLS line N" below is a line of that file), `data_platform/DATA_MANIFEST.md`, `MIGRATION_PLAN.md`, `LAYOUT.md`, `plan/batch_items/*.tsv` and `dedup/` of
spinesurg-ct-nnunet at 097933a, `docs/handoff/INFRASTRUCTURE.md`, `docs/handoff/DATASET_USAGE.md`, and the memory notes. `grid_manifest.tsv` row N and `grid_manifest.md` section N are
`../_plan/inventories/grid_manifest.tsv` and `.md` (row N = TSV row N counted from 1 after the header).
Migration state words: VERIFIED (a batch job compared files and bytes), copying (no STATUS yet at 22:20 UTC), stay (batch
B14 keeps it on HOME), not in a batch, deleted. Nothing in this folder reads the grid except with `ls`, `stat`, `cat` of
small files and `squeue`, in a job or through `wsl -e bash -lc 'ssh grid ...'`; nothing is written there.

## 1. Paths this archive owns (DISPOSITION rows grid r84, r124, r199, r208, r209, r211)

| path | what it holds | size | migration state | verified |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/rsna_2022_cspine/raw/rsna_cspine` | the RSNA 2022 cervical-spine fracture CT archive: the Kaggle zip (2,019 train studies; per-level fracture labels C1-C7; 87 segmentations), one `.nii.zip`, `sample_submission.csv`, `fetch.log`; never unpacked; used by nothing; a header census refused every study (longest craniocaudal extent 334 mm, below the 350 mm a junction count needs; `SchwingNet/results/transitional_registry/other_ct/SUMMARY.md` lines 30, 36, 112). Fetched 2026-09-19 on the login node (now forbidden) with the Kaggle token from `/wsu/home/go/go24/go2432/.fluorocap/credentials.env` (never read; the token is in a chat transcript and must be rotated: `DATASET_USAGE.md` section 5) | 4 files, 203,321,991,870 B (B08 STATUS row 001); zip 203,318,086,447 B; 236.8 GB of HOME before the move (`DATASET_USAGE.md` section 7) | batch B08 VERIFIED; HOME `/wsu/home/go/go24/go2432/data/rsna_cspine` is now a link to the Ceph path (GRIDLS line 2190, dated 2026-10-08 08:12) and `/wsu/home/go/go24/go2432/data/rsna_cspine.pre-ceph` (2026-09-19; GRIDLS line 2191) is still present; deletion candidate | yes: VERIFY_OK files 4/4, bytes 203,321,991,870 / 203,321,991,870, sampled 4 (GRIDLS line 2116). Keep or delete is `docs/handoff/OPEN_QUESTIONS.md` A19 (Greg); whether HPR 2026-269 covers it (competition rules, not a DUA) is not recorded |
| `/wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` | a backup of the annotator (the April 2026 `spinesurg-ct-annotator` repository, 1083c4f), dated 2026-08-10; role beyond the name not recorded | directory entry 4,096 B (GRIDLS line 1134); contents size not recorded | not in a batch (not recorded in `plan/batch_items/`) | listed by `ls` on 2026-10-08; contents not read |
| `/wsu/home/go/go24/go2432/Multi-View-Vertebra` | a clone of the MICCAI 2023 Multi-View-Vertebra reference code (the published multi-view sequence loss that the parity ladder excludes because it re-injects the counting prior; `RESEARCH_DIRECTIONS.md` section 3.5 of the handoff); upstream URL not recorded | directory entry 4,096 B, dated 2026-09-13 (GRIDLS line 133) | B14 stay (`../_plan/inventories/grid_manifest.tsv` row 199) | listed by `ls` on 2026-10-08 |
| `/wsu/home/go/go24/go2432/docs` | ten documents of 2026-02-12 from an earlier weak-label project (titles not recorded) | not recorded | B14 stay (`../_plan/inventories/grid_manifest.tsv` row 208) | listed in the 2026-10-08 pass; contents not read |
| `/wsu/home/go/go24/go2432/_adv_510.py` and about 300 loose audit scripts and outputs in the HOME root | the identity-audit scratch of 2026-08-28, 2026-09-20 and 2026-09-22: `_adv_*.py`, `_v*_*.py`, `verify_*.py`, `ts_*.py`, `df_*.py`, `fc*.py`, `nh_*.py`, `mend_*.py`, `vprobe*.py`, `*.json`, `*.png`; their conclusions are `docs/PATIENT_IDENTITY_SPEC.md` and `docs/DATA_COMPLETENESS_AUDIT.md` in spinesurg-ct-nnunet (owned by 10) | `_adv_510.py` 1,610 B (2026-09-22; GRIDLS line 145); `dicom_identity.json` 975,717 B; `df_ident2.json` 3,522,392 B; `_v_vindr_hdr.json` 1,606,544 B (`../_plan/inventories/grid_manifest.tsv` row 209); the rest names only | not in a batch | names listed on 2026-10-08; nothing read |
| `/wsu/home/go/go24/go2432/logs` | HOME job logs: `slurm_logs`, `tmp`, `runs`, `track5`, `reg`, `selective`, `proto_test`, `lstv_eval`, `contours`, `ct_mine`, `ctr_smoke`, `plm`, `rx_cobra_scratch`, `orient_v2`, `audit_out`, `filmid_out`, `spai_verify`, `ts_verify_out`, `ts_dupscan_out`, `idscan_out`, `tabcheck`, `space_backup`, `gridtree_backup_20260924_1741`, `mpda_build`, `user`, `wedge`; roles beyond name and date not recorded | directory entry 94,208 B; `slurm_logs` 90,112 B (directory entries, not contents) | not in a batch; whether any of it is a deletion candidate is Greg's call (OQ A26) | listed on 2026-10-08; nothing read |

## 2. FluoroCap on the grid (owned by `02_transitional_naming_truth` as test material; recorded here as the dormant line)

| path | what it holds | size | migration state | verified |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/FluoroCap` | the literature fluoroscopy harvest: `releases/FluoroCap_v0.1_A` and `_B` (the frozen release of 2026-09-13, named as on disk; A 2,531 included panels, B 991 licence-clean), `articles/` and captions jsonl, `annotate/` (the reader pages, of which 3 of 64 reading and 2 of 104 screening pages exist on the laptop), `archives/`, anchor and consistency JSONs, `PROTOCOL.md`, `CORPUS_MANIFEST.*`, `LEVEL_COUNTS.*`, and the weights registered from it on 2026-09-15 (`detect_v5z_final_best.pt` 42,233,939 B, sha 797de71a; `detect_v5z_epoch25_best.pt`; `detect_v6f_best.pt`; `anchor_det_v1.pt`; `orientation_net*.pt`; `hardware_det_v1/v2.pt`; `panel_classifier.pt`; `finetune_v3`; GRIDLS lines 2577-2647 in the `aliases` listing that starts at line 2569, and 2660-2691 in `registry.jsonl`, which starts at line 2652) | 367 entries; 316 GB by `du` on 2026-09-19 (`../_plan/inventories/grid_manifest.tsv` row 185) | batch B09, copying at 22:20 UTC on 2026-10-08 with no STATUS file; HOME tree is the deletion candidate once VERIFIED | directory listed on 2026-10-08 (GRIDLS line 129, dated 2026-09-20); not verified |
| `/rs/rs_grp_oschome/go2432/data/fluorocap/raw` | the B09 landing folder | 1 entry at 22:20 UTC | copying | no |
| `/wsu/home/go/go24/go2432/REPORT.md` and `REPORT_interim.md` | the FluoroCap reports of 2026-09-13 | 20,227 B and 16,115 B (GRIDLS lines 137-138) | not in a batch; not in any repository | listed on 2026-10-08; fetch with `scp` in a job when Greg allows |
| `/wsu/home/go/go24/go2432/FluoroCap_lstv2` | the transitional harvest arm of FluoroCap (named in `../_plan/inventories/spinesurg_ct_nnunet.md` section 5; `memory/fluorocap-prototype-and-lstv-arm.md`) | not recorded | not recorded | not re-verified on 2026-10-08 |
| `/wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` | the body detector of the reported SchwingNet stack (alias `detector_v5z_final`), the same file as `/wsu/home/go/go24/go2432/FluoroCap/detect_v5z_final_best.pt` (`DATASET_USAGE.md` section 1); owned by 01 | 42,233,939 B | registry (`docs/MODEL_REGISTRY.md` in spinesurg-ct-nnunet; owned by 10) | sha recorded in `/wsu/home/go/go24/go2432/model_registry/registry.jsonl` 2026-09-15 |

## 3. The roots of the superseded numbers (names only; nothing here is quotable; the catalog row is given)

| path | catalog row | what it was | state |
|---|---|---|---|
| `/wsu/home/go/go24/go2432/tmp/ladder_summary.json` | C1.1 | the context ladder on the cervical-dominated `films_ann` bank (96.7 % at one vertebra) | RECORD ONLY; not re-verified |
| `/wsu/home/go/go24/go2432/bench/xr_fov/recurrent.json` | C1.2 | the recurrent head 98.69 / 99.13 / 99.41 / 99.48 % at 3 / 5 / 7 / 9 vertebrae; job 40215812 (2026-09-13); the bank was `films_ann_fov96_ctx`, not `films_all2` | RECORD ONLY [WRONG-BANK]; the attribution in `slurm/recurrent_head.sh` line 16 and `tools/recurrent_order.py` line 56 is uncorrected (OQ F5) |
| `/wsu/home/go/go24/go2432/bench/xr_fov/recurrent_all2.json` | C1.3 | the `films_all2` head | RECORD ONLY |
| `/wsu/home/go/go24/go2432/model_night/runs/result_r18_ce.json` | C1.4 | whole-spine 27-class single crop 78.74 % on allspine_v2 | RECORD ONLY [LEAK] |
| `/wsu/home/go/go24/go2432/model_night/recurrent_allspine_v2.json` | C1.5 | the restored recurrent head on allspine_v2; job 40293790 | RECORD ONLY [LEAK] |
| `/wsu/home/go/go24/go2432/model_night/stc/` | C1.7 | Star Temporal Classification against cross-entropy | REFUTED |
| `/wsu/home/go/go24/go2432/selective/SELECTIVE.md` | C1.8 | selective prediction, 99 % at 35.7 % coverage; job 40291753 | NOT QUOTABLE [LEAK][SEL-REP] |
| `/wsu/home/go/go24/go2432/bench/robust/*.json` | C1.10 | the corruption suite on `films_all2` | RECORD ONLY |
| `/wsu/home/go/go24/go2432/model_night/panel_stats/` | C1.11 | FluoroCap panel agreement 19.7 %, n 7,065 | not an accuracy |
| `/wsu/home/go/go24/go2432/lstv_flag/LSTV_FLAG_RESULTS.md`, `LEARNING_CURVE.md`, `lstv_flag_labels_v2.csv` | C1.12, C1.13 | the 2-D LSTV / TLTV flags (CTSP AUC 0.577, interval containing 0.5) and their learning curve | REFUTED as a flag; RECORD ONLY |
| `/wsu/home/go/go24/go2432/model_night/interior_windows/` | C1.14 | the feasibility interior windows on v2 / v5 / v6; job 40321368 | RECORD ONLY [LEAK] |
| `/wsu/home/go/go24/go2432/model_night/ensemble/ensemble.json` | C1.17 | the re-implemented competitor ensemble | NOT RECORDED in any repository document; whether the file exists is unknown (the 2026-10-08 listing of `/wsu/home/go/go24/go2432/model_night` was truncated; `PLAN.md` section 7) |
| `/wsu/home/go/go24/go2432/model_night/scaling/SCALING_CURVE.json` and `/wsu/home/go/go24/go2432/scaling` | C2.1 | the 2026-09-17 synthetic / real fraction sweep on subsets of the v2 bank; the subset banks | SUPERSEDED [LEAK] [SEL-SPLIT]; the v2 bank it was cut from was deleted 2026-09-20 |
| `/wsu/home/go/go24/go2432/allspine_v2` to `/wsu/home/go/go24/go2432/allspine_v5c` | C1.4, C1.5, C1.14, C2.1 | the leaked crop banks (NHANES II twice; CTSP under two names) | deleted 2026-09-20 for quota (206.5 GB; `memory` note grid-quota-and-deleted-banks, owned by 10); hold-out runs silently fell back to fitted cases until `holdout.py` raised |
| `/wsu/home/go/go24/go2432/model_night/sweep_v3/` | C3.1 | the overlapping-exposure sweep on 120 held-out CTSP spines; job 40384843; owned by 01 as private history | RECORD ONLY; only sweep_v3 counts (earlier sweeps used the wrong field size) |
| `/wsu/home/go/go24/go2432/ablate` | C5.1 | five arm directories (`v5_all`, `v5_minus_all`, `v5_minus_extras`, `v5_minus_obl`, `v5_minus_pseudo`) of the CTSpinoPelvic1K nnU-Net ablations; catalog row C5.1 lists six ablation runs (fused_only, no_partial, no_lstv_oversample, short 100 epochs, ResEnc L, fused-only test), and which run wrote which directory is not recorded (runs and directories are different counts); owned by 03 | 201.6 GB; outcome never recorded (OQ B16) |

## 4. Named only, never copied, never read

`/rs/rs_grp_oschome/go2432/private_ip` (0.634 GB, 9 files; Greg's private records); the credential files on HOME
(`/wsu/home/go/go24/go2432/.fluorocap/`, `/wsu/home/go/go24/go2432/.hf_org_token`, `/wsu/home/go/go24/go2432/.hf_osc_token`, `/wsu/home/go/go24/go2432/.zenodo_token`, `/wsu/home/go/go24/go2432/.kaggle/`, `/wsu/home/go/go24/go2432/.netrc`, `/wsu/home/go/go24/go2432/github`,
`/wsu/home/go/go24/go2432/CTSpinoPelvic1K/.token`, `/wsu/home/go/go24/go2432/XRSpinoPelvic1K/*.ica`; contents never read; `PLAN.md` section 6 lists what Greg rotates).

## 5. What is not on the grid (for this folder)

- No human-read FluoroCap test set: no panel has a human level read (`docs/fluorocap/FLUOROCAP_QC_2026-09-14.md`
  section 8, line 166: "No panel has been read by a human"); the "about 200" is the FluoroCap row of
  `RESEARCH_DIRECTIONS.md` section 5, restated in `docs/handoff/GREG_ONLY_SECTION_EXTRACTS.md`.
- No clean re-run of selective prediction on the v9 lineage (OQ C13); no re-run of the 2026-09-17 refutations on a clean
  bank (`RESEARCH_DIRECTIONS.md` section 8 unknown 24).
- No Ceph copy of `/wsu/home/go/go24/go2432/FluoroCap` with a STATUS yet (B09 copying at 22:20 UTC on 2026-10-08).
- No repository copy of `/wsu/home/go/go24/go2432/REPORT.md` and `/wsu/home/go/go24/go2432/REPORT_interim.md`.
