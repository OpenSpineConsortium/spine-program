# MANIFEST_GRID: every grid path this project uses or produced

HOME = `/wsu/home/go/go24/go2432` (Panasas, 4.3 TB soft quota, was 93 % full); Ceph = `/rs/rs_grp_oschome/go2432`
(CephFS, 20 TB, group `oschome`). Sources of every row: the read-only grid listing of 2026-10-08 22:20 UTC
(GRIDLS = `../10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`; its section markers are in
`grid_ls_markers.txt` beside it), the two size censuses taken from that read (CENSUS-CEPH =
`../10_data_platform_grid/docs/grid_read_2026-10-08/census/ceph/census.tsv`; CENSUS-HOME =
`.../census/home_after_F/census.tsv`; `.../census/_du_home.txt` is a partial `du` list of 189 HOME entries),
`data_platform/{DATA_MANIFEST,MIGRATION_PLAN,LAYOUT}.md`
and `data_platform/plan/batch_items/B09.tsv`, `B10.tsv`, `B11.tsv` of the private repository at 097933a,
`docs/handoff/INFRASTRUCTURE.md`, `docs/handoff/RESULTS_CATALOG.md` (RC), the result files copied into this folder,
and the memory notes. "Verified" means a job or a file check proved the content; "listed only" means the name was
seen in GRIDLS and nothing else was read. Sizes are the census or `du` figure the named file gives; "not sized"
means no file records one. Nothing on the grid was written for this manifest.

## 1. Paper 2's gate material (Ceph)

| path | holds | size | migration state | verified | source |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/fig6` | paper 2 Figure 6 (LevelCheck) material: 17 subdirectories, 22 entries, dir mtime 2026-09-25 00:22: `bank_g3_v2`, `detector_g3`, `frozen_v1`, `eval_v2_g3`, `gatecheck_v2_g3_pre`, `unblinding/`, `HOLD_README.txt`, `EVAL_SUBMITTED.json`, `RELEASE_OPEN_GATE.json`, `G5_MANIFEST.json` | 13.920 GB census | Ceph-native, stays | listed only; `G5_MANIFEST.json` identical here and in the grid checkout at release (`results/paper2/fig6/RELEASE_OPEN_GATE.json`) | GRIDLS `ls RS/data`; CENSUS-CEPH row `/rs/rs_grp_oschome/go2432/data/fig6` (13.920 GB, 86,277 files, newest 2026-09-25); RC B.6 |
| `/rs/rs_grp_oschome/go2432/data/fig6/bank_g3_v2` | the G3 clean crop bank: 134,975 crops (116,706 train / 18,269 val; 8,950 / 1,079 persons), `meta.json` sha256 f78dd1ee...; `runs/model_rung_1_g3clean_aug2.pt` (the ImageNet-root G3 encoder, sha256 629f0e05...) | not sized | Ceph-native | BANK_CHECK PASS before every D1 job (`results/paper2/dual_loss/RUN_d1.json`) | RUN_d1.json; registry alias `bank_g3_v2_rung_1_g3clean_aug2` |
| `/rs/rs_grp_oschome/go2432/data/fig6/frozen_v1` | the frozen snapshot: `strata.json` sha256 c7199d2d..., `split_final.json` sha256 65a57eb0..., `auto_reference.json` sha256 57782cad..., `auto_truth.csv` sha256 aa306deb..., `SHA256SUMS.json` | not sized | Ceph-native | `sha256sum -c OK` on the grid checkout at release (`RELEASE_OPEN_GATE.json#frozen_reference`) | RUN_d1.json; RELEASE_OPEN_GATE.json; laptop twin `SchwingNet/results/fig6/frozen/v1` in the repository (62 MB, not in this folder) |
| `/rs/rs_grp_oschome/go2432/data/fig6/eval_v2_g3` | the open gate's outputs: `<head>/<set>/open/<variant>/proto/` prototype dumps for six heads (lam0 and lam1.0, seeds 0-2) over T1 renders, T2 COBRA, T3 C-ArmLSpine; re-scorable without a model re-run (TODO step 4) | not sized | Ceph-native | job 40438004 ran 2026-09-25 04:22-06:02 UTC, F6EVAL_END gate=open | `manuscripts/paper2_levelcheck/open_gate_40438004/README.md` |
| `/rs/rs_grp_oschome/go2432/data/fig6/gatecheck_v2_g3_pre` | leak-gate pre-check verdicts, job 40438053: total 108, pass 108, fail 0 (2026-09-24 21:55:45 UTC) | not sized | Ceph-native | by the job's summary line | RELEASE_OPEN_GATE.json |
| `/rs/rs_grp_oschome/go2432/data/fig6/unblinding/RELEASE_v2.json` | **does not exist.** Must be written by a person naming the committed G5 manifest (a6cc8a11e7303bbf4abb666b7c1760f3831a4dd5), a frozen human truth file with its sha256, `prespec_commit_is_ancestor` true and `released_by`; the blinded gate refuses to run without it (exit 6) | — | — | absent at release (`human_truth_file: none`) | `results/paper2/fig6/HOLD_README.txt`; RC B.6 |
| `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference` | the automated reference runs: readers A / B / C on CTSP, VerSe, COBRA CT and CBCT, C-ArmLSpine, ts12 (9 subdirectories, 14 entries, 2026-09-24 23:34); the SPINEPS CBCT cpu patch | inside `or_ready` (867.951 GB, 340,064 files; CENSUS-CEPH row `/rs/rs_grp_oschome/go2432/data/or_ready`) | Ceph-native | listed only; the laptop copy is `results/paper2/auto_reference/` | GRIDLS `ls RS/data/or_ready`; RC B.3 |
| `/rs/rs_grp_oschome/go2432/data/or_ready/dual_loss` | D1 heads, the learning-curve heads, coverage and self-test outputs (3 subdirectories, 27 entries, 2026-09-24 10:51); `d1_selftest_4042985{1}.out`, `40430077.out`, `40430433.out` at the `or_ready` root | inside `or_ready` | Ceph-native | heads registered (21 aliases, section 4) | GRIDLS; `results/paper2/dual_loss/` |
| `/rs/rs_grp_oschome/go2432/data/or_ready/alphabet_loss` | the alphabet-loss arm (12 entries, 2026-09-23 01:22): the 56.1-72.4 % L6 recall [SEL-SPLIT] of `SchwingNet/results/ALPHABET_LOSS.md` | inside `or_ready` | Ceph-native | listed only | GRIDLS; RD section 1.2 |
| `/rs/rs_grp_oschome/go2432/data/or_ready/v9` | 3 entries, 2026-09-23 00:39 (`v9_chain_jobs.txt` 55 B beside it) | inside `or_ready` | Ceph-native | listed only | GRIDLS |
| `/rs/rs_grp_oschome/go2432/data/or_ready/learning`, `learning_cpu`, `learning_lat`, `learning_lat_cpu` | the Figure 2 analyses (jobs 40416675 GPU, 40416700 CPU; 9 / 10 / 7 / 0 entries, 2026-09-23 03:57-04:13) | inside `or_ready` | Ceph-native | CPU replicate cosine >= 0.999999 to the GPU run (`results/paper2/learning/LEARNING.md`) | GRIDLS; RC A1 |
| `/rs/rs_grp_oschome/go2432/data/rare_class` | the rare-class render banks (16 subdirectories, 17 entries, 2026-09-24 16:31): C-ArmLSpine CBCT renders, CTSP, TotalSegmentator, VerSe rare-anatomy renders with subtype truth; built by `tools/rare_class_maximize.py` and `SchwingNet/slurm/rare_max_{stage,verse,verify}.sh` (MAXIMIZE 2026-09-24 16:55) | 5.797 GB census | Ceph-native | listed only; reports in `results/paper2/rare_class/` | GRIDLS; CENSUS-CEPH row `/rs/rs_grp_oschome/go2432/data/rare_class` (5.797 GB, 44,150 files); RECIPES section 3.1 row 7 |

## 2. The real-frame transitional sources (Ceph; shared with 01)

| path | holds | size | migration state | verified | source |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/cobra2026` | COBRA2026: 692 public cases of 867, 375,618 projections, `cases/` 42.16 GB; the planning-CT screen (91 calls: L6 38, T13 45, four-lumbar 8; 57 field-supported); Elekta frames exported from 145 cases (3,480 frames); Varian 225 cases never exported; validation and test 175 cases embargoed to 2032-03-01; CC BY-NC 4.0 | 808.615 GB census | Ceph-native | per the `cobra2026` card of `data_platform/DATA_MANIFEST.md`; listed only on 2026-10-08 (11 subdirectories, 39 entries, 2026-09-23 13:32) | GRIDLS; CENSUS-CEPH row `/rs/rs_grp_oschome/go2432/data/cobra2026` (808.615 GB, 30,350 files); RD section 2.4; RC A16.6 |
| `/rs/rs_grp_oschome/go2432/data/cobra2026/derived/rx_cobra_scratch` | B10 target for HOME `/wsu/home/go/go24/go2432/rx_cobra_scratch` (directory, 2026-09-21 17:47, GRIDLS `ls HOME`) | not sized | B10 not started | — | `plan/batch_items/B10.tsv` |
| `/rs/rs_grp_oschome/go2432/data/carmlspine` | C-ArmLSpine (Zenodo 22768651): `C-ArmLSpine.zip` 15,581,614,253 B with `.ok` marker, `cases.csv` 11,266 B, `catalogue.json` 294,678 B, `compare_veridah{,2}.csv`, `headers_dossier.json` 1,863,754 B, `dossier_look/` | 86.834 GB census | Ceph-native, stays | zip `.ok` marker; sha not read | GRIDLS `ls RS/data/carmlspine`; CENSUS-CEPH row `/rs/rs_grp_oschome/go2432/data/carmlspine` (86.834 GB, 330,098 files) |
| `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine` (+ `carmlspine_crops`, `_cv`, `_cv_prerepair`, `_cvday`, `_cvday_prerepair`, `_cvfill`, `_multi`, `_pre_repair_2026-09-23(_crops)`, `_sweep`) | the real-frame banks: 149 cases, 299 spot frames after the 2026-09-23 repair; the three one-labeller L6 persons case42, case121, case136 (all G3 test); `cobra_elekta_v3`, `cobra_elekta_g3test` beside them | 3.408 GB, 67,732 files (CENSUS-CEPH row `/rs/rs_grp_oschome/go2432/data/realxray`); LAYOUT says 3.86 GB | Ceph-native (`realxray_layout`) | listed only (dir dates 2026-09-21 to 09-24) | GRIDLS `ls RS/data/realxray`; `split_plan.md` "Real transitional subjects"; OQ B19 |

## 3. HOME paths this project reads or produced (all still on HOME on 2026-10-08)

| path | holds | size | migration state | verified | source |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/split_final.json` | the frozen G3 person split (apply 2026-09-23 20:18:48, seed 0, job 40426793, leak audit PASS); frozen sha256 65a57eb0... | 8,065,646 B (GRIDLS, mtime 2026-09-23 20:18) | B11 (irreplaceable) -> `/rs/rs_grp_oschome/go2432/data/multisource_banks/meta/split_final.json`; B11 not started; `multisource_banks` absent on Ceph | sha matches the frozen snapshot (RUN_d1.json) | GRIDLS; `plan/batch_items/B11.tsv`; **trap:** `SchwingNet/slurm/g3_split.sh` rewrites it in place with no backup (RECIPES section 10) |
| `/wsu/home/go/go24/go2432/patient_keys_final.json` (+ `.20260923_191858`, `.20260923_193933`) | the identity table the split reads | 5,913,937 B (+ 1,170,983 and 4,301,704 B) | B11 | listed only | GRIDLS `ls HOME` (three files, 2026-09-23 18:29, 19:25 and 19:47) |
| `/wsu/home/go/go24/go2432/physics_rare`, `physics_rare_film` | 1,482 rare-anatomy renders (34 CTSP and 47 VerSe series; T13 2 of 6 scans missing): the only labelled L6 and T13 at scale | not sized | B11 -> `/rs/rs_grp_oschome/go2432/data/multisource_banks/derived/physics_rare{,_film}`; not started | listed only (`ann/`, `img/`; dirs 2026-09-14 17:48 and 2026-09-18 04:34) | GRIDLS; `plan/batch_items/B11.tsv`; RD section 2.4 **Owner: project 08** (PLAN.md section 3; its `MANIFEST_GRID.md`); read here for the labelled L6 and T13 renders. |
| `/wsu/home/go/go24/go2432/lstv_flag` | the refuted 2-D flag line: `LEARNING_CURVE.md`, `LSTV_FLAG_RESULTS.md`, `ANOMALY_INVENTORY.md`, `_lstv_phenotypes.csv`, `models/` (`lstv_flag_v1/v2.pt`, `tltv_flag_v1/v2.pt`, `sex_control_v1.pt`), `curve/`, `buu_diag/`, `buu_scores{,_v2}_{AP,LA}.{csv,txt}`, `eval_*.txt`, `folds_*.csv`, `examples/`, `renders*`, `smoke/`; dir 2026-09-15 22:15 | not sized | `renders`, `renders_verse`, `renders_ctrl` -> B11 `/rs/rs_grp_oschome/go2432/data/multisource_banks/derived/lstv_flag/{renders,renders_verse,renders_ctrl}`; `smoke` -> `.../derived/lstv_flag/smoke`, B11 candidate for deletion (`B11.tsv` lines 62-65); `models/` and results stay on HOME | flag models registered (aliases `lstv_flag_v1/v2`, 2026-09-15 21:01 / 22:16) | GRIDLS `ls ~/lstv_flag`; `plan/batch_items/B11.tsv`; RC C1.12 (AUC 0.577: REFUTED); OQ B15 (the learning-curve table is not on the laptop) |
| `/wsu/home/go/go24/go2432/lstv_flag_derive_verse.py` | a HOME-root script of the flag line (3,016 B, 2026-09-15) | small | not in any batch | listed only | GRIDLS |
| `/wsu/home/go/go24/go2432/model_night/anomaly_manifest` | `anomaly_manifest.csv`, `spine_classes.json`, `summary.json` (2026-09-17; 749 anomalous spines) | not sized | HOME | listed (folder) | RC D.1 |
| `/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` | the v9 level bank (`rung_1.npz` 5,449,315,625 B; the SchwingNet encoder `runs/model_rung_1_aug2.pt` 44,824,746 B); holds BUU pixels (owner-only); the encoder that saw 49 of 54 G3 L6 val+test persons | 5.494 GB census | B11 (restricted) | encoder registered (`allspine_v9_fov96_ctx_rung_1_aug2`) | CENSUS-HOME row `/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` (5.494 GB, 4 files; `runs/` 0.045 GB); `split_plan.md` |
| `/wsu/home/go/go24/go2432/bench_ts` | SPINEPS + VERIDAH over 1,228 TS v2 + 374 VerSe CTs (labeller A inputs); 31 "relabelled" masks are links back to raw masks | 1.511 GB census | B11 | listed only | CENSUS-HOME row `/wsu/home/go/go24/go2432/bench_ts` (1.511 GB, 4,815 files, 3,077 `.nii.gz`); RECIPES section 3.5 |
| `/wsu/home/go/go24/go2432/FluoroCap` | the literature fluoroscopy harvest (test set only, directive D1): `releases/FluoroCap_v0.1_{A,B}` (2026-09-13 22:35), `articles.jsonl`, `captions_*.jsonl`, `annotate/` (the 64 reading and 104 screening pages), `archives/`, `commons/`, `CORPUS_MANIFEST.{json,md}`, `LEVEL_COUNTS*.{json,md}`, `PROTOCOL.md`, `README.md`, `MORNING_REPORT.md`, `allspine_chain.log`, marker files; the weights `detect_v5z_final_best.pt` (42,233,939 B, same file as registry 797de71a9e0e42f7), `anchor_det_v1.pt` (registry 8df40e7f..., 40,489,317 B; 71.67 % on real film, below the 0.80 floor), `anchor_det_c2_v1.pt`; 34 subdirectories, dir 2026-09-20 21:07 | 316.0 GB (LAYOUT line 291 and `B09.tsv` line 2; `youtube/` 181.0, `pdf/` 19.77, `panels/` 4.68, `raw/` 2.27 GB from LAYOUT lines 292-295, which cite `DATA_COMPLETENESS_AUDIT.md` lines 757-761); no row in CENSUS-HOME | B09 -> `/rs/rs_grp_oschome/go2432/data/fluorocap/raw/FluoroCap`; copying on 2026-10-08 (one of three `dp_migrate` jobs, inferred by elimination); flagged irreplaceable | not yet | GRIDLS section `ls ~/FluoroCap` (the HOME path `/wsu/home/go/go24/go2432/FluoroCap`); `plan/batch_items/B09.tsv` line 2; LAYOUT lines 291-295 |
| `/wsu/home/go/go24/go2432/fluorocap_drr`, `fluorocap_drr_smoke`, `fluorocap_fov96_ctx`, `fluorocap_pack` | FluoroCap render and crop banks (2026-09-18) | not sized | B09 -> `/rs/rs_grp_oschome/go2432/data/fluorocap/derived/{fluorocap_drr,fluorocap_drr_smoke,fluorocap_fov96_ctx,fluorocap_pack}` | listed only | GRIDLS; `B09.tsv` lines 3-6 |
| `/wsu/home/go/go24/go2432/fluorocap_patient_keys.json` | FluoroCap identity table (112,088 B, 2026-09-22) | small | B09 -> `/rs/rs_grp_oschome/go2432/data/fluorocap/meta/fluorocap_patient_keys.json` (irreplaceable) | listed only | GRIDLS; `B09.tsv` line 7 |
| `/wsu/home/go/go24/go2432/REPORT.md`, `REPORT_interim.md` | the FluoroCap night reports of 2026-09-13 (20,227 B and 16,115 B) | small | not in any batch; not in a repository as far as recorded | listed only | GRIDLS |
| `/wsu/home/go/go24/go2432/.fluorocap` | harvester credentials | — | never read, never moved | — | LAYOUT line 137 |
| `/wsu/home/go/go24/go2432/verify_fluorocap.{py,sh}` | FluoroCap verification scripts at the HOME root (2026-09-22) | small | not in any batch | listed only | GRIDLS |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` | the grid checkout of the private repository, branch `L6_Class` at 4e3fe93862673e28613f7521d4c146c03a9dd405 on 2026-10-08; it can no longer fetch the repository (code ships by `git archive` over ssh, `SHIPPED_COMMITS.txt`); `SchwingNet/results/fig6/G5_MANIFEST.json` identical to the Ceph copy at release | — | stays | HEAD read in GRIDLS | GRIDLS "grid checkout HEAD"; RECIPES section 0 item 2 |

## 4. Model registry aliases this project owns (`/wsu/home/go/go24/go2432/model_registry`, GRIDLS "aliases")

| alias | target (content-addressed store) | date | what |
|---|---|---|---|
| `bank_g3_v2_rung_1_g3clean_aug2` | `model_registry/629f0e058649ca1d/model_rung_1_g3clean_aug2.pt` | 2026-09-24 07:54 | the G3 clean encoder (ImageNet root only) |
| `det_g3_primary_s0` | `model_registry/fe00a1732032e81a/best.pt` | 2026-09-24 16:47 | the section 15 primary detector (trained on the G3 TRAIN side of every device) |
| `head_fig6_g3clean_lam0_seed{0,1,2}`, `head_fig6_g3clean_lam1.0_seed{0,1,2}` | `model_registry/{5e1e4c3b..., f83336ee..., 7d9533cc..., b150a58e..., 1f6daa7d..., a838629a...}` | 2026-09-24 08:01-08:17 | the six open-gate heads |
| `head_fig6_g3clean_dual_seed{0,1,2}` | `model_registry/{05ca6d6a..., 4207521f..., b2dedeca...}` | 2026-09-24 08:14-08:58 | D1 dual-loss heads |
| `head_fig6_g3clean_dual_f{0.0625,0.125,0.25,0.5}_seed{0,1,2}` | twelve store entries (GRIDLS lines 2622-2633) | 2026-09-24 10:41-10:46 | the learning-curve heads (A17) |
| `lstv_flag_v1`, `lstv_flag_v2`, `tltv_flag_v1`, (`tltv_flag_v2`, `sex_control_v1` registered, GRIDLS `registry.jsonl`) | `model_registry/5c14968b7081b2c3/lstv_flag_v1.pt` (44,785,396 B), `1c6c63ec3b3a59b0/lstv_flag_v2.pt` | 2026-09-15 21:01-22:16 | the refuted flag models |
| `detector_v5z_final`, `anchor_detector_v1` | `797de71a9e0e42f7/detect_v5z_final_best.pt` (42,233,939 B), `8df40e7f.../anchor_det_v1.pt` (40,489,317 B) | 2026-09-15 05:55 | the FluoroCap-era naming detector and render-trained anchor detector |

Whether `/wsu/home/go/go24/go2432/model_night/heads_mixed/` and
`/wsu/home/go/go24/go2432/model_night/ensemble/ensemble.json` exist is not known: GRIDLS lists `/wsu/home/go/go24/go2432/model_night` only as
a `head` (section `ls ~/model_night (head)`; `../_plan/PLAN.md` section 7).

## 5. Jobs of record (Slurm ids; `docs/handoff/RESULTS_CATALOG.md`, the copied gate records)

| job | what | outcome |
|---|---|---|
| 40426793 | G3 split apply (`SchwingNet/slurm/g3_split.sh`), 2026-09-23 20:18:48 | done; leak audit PASS |
| 40416675 / 40416700 | Figure 2 embeddings, GPU and CPU replicate | done |
| 40416205 | anomalous inventory (`anomalous_inventory.sh`) | done (81 persons, superseded by the subtypes) |
| 40429851 / 40430077 / 40430433 | D1 self-tests | done |
| 40430499, 40436434 (arrays of 3) | D1 training | done 2026-09-24 08:14-08:58 |
| 40436887 (array of 12), 40436997 | D1 learning curve, coverage | done (`saturation.json`) |
| 40438053 | leak-gate pre-check | F6GATEPRE_OK, 108 of 108 |
| 40438004 | the open gate (ordinary persons only) | ran 2026-09-25 04:22-06:02 UTC; reference score never written (F3) |
| 40438005 | the blinded gate (`afterany:40438004`) | held; cancelled 2026-09-27 15:50 with every non-ruleclass job; must not be released before `RELEASE_v2.json` |
| 40429882, 40431765, 40431766 | earlier held gate jobs with pre-section-15 detectors | cancelled 2026-09-24 17:55 |
| 40436876 / 40436877 | the NLST pilot T13 recount (9.3 % to 1.5 %) | done (06's record) |

## 6. What is NOT on the grid, or not yet there

| item | state | source |
|---|---|---|
| `/rs/rs_grp_oschome/go2432/review_tree` | does not exist; the transitional review tree was never built; `tools/transitional_review/` is untracked in the repository | GRIDLS section `ls RS` (27 entries, none named `review_tree`); RECIPES section 3.1 row 11 |
| `/rs/rs_grp_oschome/go2432/data/fig6/unblinding/RELEASE_v2.json`; `SchwingNet/results/fig6/verification/truth_frozen.csv` | do not exist; a human truth is a precondition of both | `HOLD_README.txt`; `RELEASE_OPEN_GATE.json` |
| human reads: `greg_verdict` on 546 registry review cases; FluoroCap reader verdicts; a whole-cohort Castellvi read | none on disk | RC D.9; `DATA_MANIFEST.md` section 4 #35 |
| the reference-standard score of the open gate (`fig6_score_open.json`) | never written for any head (path defect F3) | `open_gate_40438004/README.md` |
| `/rs/rs_grp_oschome/go2432/data/multisource_banks` (B11 target for `split_final.json`, `physics_rare`, `lstv_flag/renders*`, the v9 bank) | absent; B10 and B11 not started on 2026-10-08 | GRIDLS section `ls RS/data B04 B05 B07 B09 B10 B11 targets` (`multisource_banks`: "No such file or directory") |
| `/rs/rs_grp_oschome/go2432/data/fluorocap/raw` | exists with 1 entry, `raw` (2026-10-08 05:52); B09 still copying; no STATUS file yet | GRIDLS, same section (`ls /rs/rs_grp_oschome/go2432/data/fluorocap`) |
| `/rs/rs_grp_oschome/go2432/data/fluorogen_synthetic` | absent (B09's second item) | GRIDLS |
| the LSTV flag learning-curve table (date, job id, cells) | on the grid in `/wsu/home/go/go24/go2432/lstv_flag/LEARNING_CURVE.md` (GRIDLS section `ls ~/lstv_flag`); not on the laptop | OQ B15 |
| which held job carries the post-section-15 detector | not recorded | OQ B11; RC B.6 |
| what the ruleclass arms finished after 2026-09-27 (06's) | not recorded on the laptop; arm A tier 1 complete but one CT, tier 2 848 pending at 2026-09-29 04:23; the pelvis production array never ran | GRIDLS sections `ruleclass ts STATUS.md` and `pelvis DECISION` (`/rs/rs_grp_oschome/go2432/ruleclass/arms/ts/STATUS.md`, `arms/pelvis/_timing/DECISION.json`) |
| the 148 vs 149 C-ArmLSpine cases: whether they are that many people | cannot be established from any file | OQ E1 |
| sizes on 2026-10-08 of `/wsu/home/go/go24/go2432/FluoroCap`, `physics_rare`, `physics_rare_film`, `lstv_flag`, `fluorocap_drr`, `fluorocap_drr_smoke`, `fluorocap_fov96_ctx`, `fluorocap_pack` and `rx_cobra_scratch` | not recorded (no `du` allowed on the login node); CENSUS-HOME and `_du_home.txt` carry no row for any of them; the FluoroCap 316.0 GB is LAYOUT's earlier figure | CENSUS-HOME; `census/_du_home.txt` (189 rows) |
