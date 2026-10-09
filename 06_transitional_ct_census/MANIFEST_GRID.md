# MANIFEST_GRID.md — every grid path this project uses or produced

HOME = `/wsu/home/go/go24/go2432`; `$RS` = `/rs/rs_grp_oschome/go2432` (Ceph, 20 TB, group `oschome`); every path in the
tables below is spelled in full, so a copy never depends on this line. Sizes are
"census" = the Ceph census of job 40580051 and the HOME census of jobs 40578909 / 40580052 (apparent GB, 2026-10-07/08),
"STATUS" = bytes in `~/spinesurg-ct-nnunet/data_platform/plan/runs/<B>/STATUS`, or "du <date>" from
`data_platform/plan/layout_map.csv`. "Verified" = a `verify_transfer` pass recorded in a STATUS file or a sha256 record
named in the cited file; "listed only" = seen in a listing. The one read-only grid pass of 2026-10-08 22:20 UTC is
recorded in `../10_data_platform_grid/`; nothing here re-ran it. Sources: the grid manifest inventory of 2026-10-08
sections 2, 3.3 and 6; `data_platform/{DATA_MANIFEST,MIGRATION_PLAN,LAYOUT}.md` and `plan/batch_items/*.tsv` in
spinesurg-ct-nnunet 097933a; `docs/handoff/INFRASTRUCTURE.md`; the memory notes named.

Rules for touching any of it: nothing on the login node; `sbatch -D <dir>` with `--qos=requeue` on `reqp` for CPU work,
`gmsap` / `gvohp` for GPU; `afterany`; IPC under `/dev/shm`; outputs on Ceph; bash 4.2; the spineps environment is
`~/mambaforge/envs/spineps` (spineps 2.1.1, TPTBox 0.8.2, torch 2.6.0+cu124) and does not run on the Blackwell nodes
ymh3 / ymh4 (`docs/handoff/RECIPES.md` section 3.2).

## 1. The ruleclass census (Ceph-native; this project's own output)

| path | holds | size | migration state | verified | notes and source |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/ruleclass` | `CORPUS.md` 30,381 B, `ARM_B.md` 19,613 B, `corpus_counts.json` 20,963 B, `arms/{ts, moller_fast, moller, pelvis}`, `tiers/` (8 entries), `code/` (21 entries: `ts_arm_gpu.sh`, `ts_arm_collect.sh`, `armb/*.sh`, `pelvis/*.sh`, `probe_t2.sh`, `probe_t3.sh`, `check_paths.sh`), `logs/` (802), `moller_masks/` (7), `containers/` 7.719 GB | 48.579 GB census, 163,587 files | Ceph-native; grows | listed only | `memory/ruleclass-super-detector-run.md`; `CORPUS.md` says 21,655 CTs against the tiers' 21,622 (OQ B3, unexplained); the arm scripts exist on the grid only, not in any repository |
| `/rs/rs_grp_oschome/go2432/ruleclass/tiers/` | `tier1.txt` + `tier1.tsv` (5,094 CTs, 5,075 persons), `tier2.txt` + `tier2.tsv` (12,217), `untiered.tsv` (4,311), `TIERS.md`, `build_tiers.py` | small | Ceph-native | `check_paths.sh` stat-tested every path: 0 missing (`docs/ruleclass/TIERS.md` section 0) | the local copy of `TIERS.md` is `docs/ruleclass/TIERS.md` |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/ts/STATUS.md` | arm A (TotalSegmentator 2.18.0 `total`) at 2026-09-29 04:23:52: tier 1 done 3,166 + exists 1,927 + failed 1 of 5,094; tier 2 done 10,398 + exists 968 + failed 3 + pending 848 of 12,217 (19.7 GPU-h remaining at the measured mean) | — | — | read in the 2026-10-08 pass | answers OQ B1 for arm A; the pending CTs: kidney_thoraxabdomen 176, nlst_pilot 484, panorama 155, idc 22, aortaseg60 2, quadra_hc 4, abdomenatlas 3, fdg 2 |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/pelvis/_timing/DECISION.json` | 621 B, 2026-09-29 08:21: `mode tta`, `n_timing 0`, `tier2_go false`, "tier 2 ready, NOT submitted: no projection"; beside it `SUMMARY.md` 429 B, `agree_timing20.tsv` 3,569 B, `census.tsv` 2,989,732 B, `renders/` (20) | — | — | read in the 2026-10-08 pass | answers OQ B1 for the pelvis arm: the gate file was written from zero timing CTs; the production array never ran (`TODO.md` step 3) |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/pelvis/<collection>` | per-collection folders (abdomenatlas3_mini, amos22, aortaseg60, barts_crl, cobra, ctsp, ctspine1k, idc, kidney_thoraxabdomen, ribfrac, tcia_fdg_pet_ct_lesions, ts, verse, waw_tace) plus `_agree`, `_model`, `_work` | inside 48.6 GB | Ceph-native | listed only | contents not recorded (`TODO.md` step 1) |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/moller_fast` | arm B Moller rib masks, fast pass, 23 collection folders + `JOBS_ACCEL.txt`, `_claims_measure`, `_claims_predict` | inside 48.6 GB | Ceph-native | listed only | fast pass was 1,801 of 5,094 tier-1 CTs at 17:00 on 2026-09-27 (`STATUS.md` D.20); later counts not recorded |
| `/rs/rs_grp_oschome/go2432/ruleclass/arms/moller` | arm B full configuration (20-25x slower), 15 entries | inside 48.6 GB | Ceph-native | listed only | not recorded as finished |
| `/rs/rs_grp_oschome/go2432/review_tree` | the two-stage review tree the code writes to | — | **does not exist** | — | never built; `code/transitional_review/` untracked; PREREG unsigned |
| `/rs/rs_grp_oschome/go2432/cns2026_posterior` | three sbatch and two python files of 2026-09-26 | 5 files | Ceph-native | listed only | the CNS 2026 posterior-element scripts; not in a repository as far as recorded |

## 2. The harvest and the acquisitions (Ceph-native)

| path | holds | size | migration state | verified | notes and source |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest` | 24 entries: `acquisition/`, `other_ct/`, `verse/`, `ctsp/`, `totalsegmentator/`, `validation_ts/`, `cobra/`, and one screen folder per fetched collection (`panorama/` holds `calls/`, `rows.csv`, `registry_rows.csv`, `gate*.csv`, `SUMMARY.md`, `review/`) | 325.817 GB census, 1,063,032 files | Ceph-native | listed only | the two-labeller screens per collection; PANORAMA's row counts not read (OQ B2) |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/acquisition` | `jobs.txt`, logs, manifests, `alias_pairs.csv`, `alias_pairs_all.csv` (1,186 near-duplicate candidates) | inside the above | Ceph-native | listed only | the laptop copies of the plan, census, ranking and manifests are `results/transitional_registry/acquisition/` |
| `/rs/rs_grp_oschome/go2432/data/anomaly_harvest/other_ct/rsna/rsna_headers.jsonl` | the RSNA 2022 cervical census headers; 2,022 study directories against 2,019 train studies | — | Ceph-native | listed only | OQ B25 |
| `/rs/rs_grp_oschome/go2432/data/idc` | 39 IDC tier-1 collections, 3,600 series, 3,499 usable CTs | 706.083 GB census | Ceph-native | `fetch/verified.jsonl` per collection (not read) | archives deleted after unpack |
| `/rs/rs_grp_oschome/go2432/data/abdomenatlas3_mini` | AbdomenAtlas 3.0 Mini, 7,649 usable CTs of 9,262 | 570.557 GB | Ceph-native | as above | matched its prediction (7,835 predicted) |
| `/rs/rs_grp_oschome/go2432/data/tcia_fdg_pet_ct_lesions` | FDG-PET-CT-Lesions, 900 CTs | 393.872 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/panorama` | PANORAMA, 2,024 CTs; screen incomplete (1,114 pending in the tiers) | 194.439 GB | Ceph-native | as above | the only collection whose census counts were not one high |
| `/rs/rs_grp_oschome/go2432/data/ctspine1k` | the Ceph copy of CTSpine1K (`raw_data/`, `metadata/`, `hf_listing.json` 618,236 B, `fetch_status.json`); 782 COLONOG volumes are CTSpinoPelvic1K people and were folded in the tiers | 162.350 GB | Ceph-native; HOME copy ABSENT (B03) | sha-verified 2026-09-23 | |
| `/rs/rs_grp_oschome/go2432/data/amos22` | AMOS22, 723 CTs kept of 2,364 (1,564 refused as thicker than 3 mm; 67 duplicates) | 102.615 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/pengwin2026` | PENGWIN 2026, 340 CTs (308 after folding; 32 folded onto CTPelvic1K clinic) | 83.499 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/ribfrac` | RibFrac 660 chest CTs (`images/`) plus `raw/ribs` from HOME (B08, VERIFIED 89 files 78,699,138,633 B) | 78.200 GB | B08 cut over | VERIFIED | registry T13 4 single-labeller, L6 1 morphology-only |
| `/rs/rs_grp_oschome/go2432/data/kidney_thoraxabdomen` | 215 CTs | 75.938 GB | Ceph-native | as above | 176 tier-2 arm A CTs pending |
| `/rs/rs_grp_oschome/go2432/data/nlst_pilot` | NLST pilot 500 CTs | 73.544 GB | Ceph-native | as above | the T13 9.3 % that fell to 1.4 % (`STATUS.md` D.12); 484 tier-2 arm A CTs pending |
| `/rs/rs_grp_oschome/go2432/data/waw_tace` | 228 CTs | 47.151 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/curvas` | 70 of 90 CTs (`training_set.zip` unresolved) | 29.994 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/deep_psma` | 53 CTs | 24.253 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/quadra_hc` | 48 CTs | 20.413 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/barts_crl` | 212 CTs | 20.313 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/curvas_pdacvi` | 101 CTs | 16.879 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/aortaseg60` | 55 CTs | 15.929 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/ctpelvic1k_clinic` | CTPelvic1K datasets 6-7 (172 CTs) | 14.832 GB | Ceph-native | as above | CTPelvic1K datasets 1-5 are on neither volume (B03 row 002 ABSENT): re-download in a job if needed |
| `/rs/rs_grp_oschome/go2432/data/csi2014` | CSI 2014, 20 CTs | 6.641 GB | Ceph-native | as above | |
| `/rs/rs_grp_oschome/go2432/data/spineps` | SPINEPS harvest masks | 8.834 GB census | Ceph-native | listed only | masks before commit 147428d carry raw ids (`memory/spineps-ids-can-be-scrambled.md`) |
| `/rs/rs_grp_oschome/go2432/data/validation_ts` | the 70 externally labelled TotalSegmentator CTs as links into `~/data/TotalSegmentator` | 0 (links) | Ceph-native; targets move with B07 | listed only | `results/transitional_registry/acquisition/validation/VALIDATION.md` |
| `/rs/rs_grp_oschome/go2432/data/rare_class` | rare-class renders (MAXIMIZE) | 5.797 GB census | Ceph-native | listed only | `STATUS.md` D.10 |
| `/rs/rs_grp_oschome/go2432/data/d815_repair` | the Dataset815 flag repair of 2026-09-23 | 0.001 GB | Ceph-native | listed only | `TODO.md` step 11 |

## 3. The VerSeFusion line

| path | holds | size | migration state | verified | notes and source |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/versefusion/raw/VerSeFusion_data` | VerSe 19/20 raw, unified, canonical, corrected, tables, HF staging; the raw masks under `unified/scan-*/` (id 25 = L6, id 28 = T13) | 194,191,642,435 B STATUS (6,951 files); 139 GB du 2026-09-01 (raw 71, canonical 67) | B06 cut over | VERIFIED (14/14) | `TODO.md` step 5 counts ids here, never in `vf_813` |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/vf_813` | the Dataset815 input conversion (C1-T9 sent to ignore) | 49,427,512,778 B STATUS (1,130 files) | B06 cut over | VERIFIED | never for whole-spine work (`MEMORY.md`, sibling note `vf813-drops-c1-t9`) |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/vf_813_probe` | unknown probe output of 2026-09-12 | 139,428,370 B STATUS (4 files) | B06 cut over | VERIFIED | role not recorded |
| `/rs/rs_grp_oschome/go2432/data/versefusion/derived/verse_drr` | VerSe renders; holds 13 `glgl*` byte twins | 477,053,118 B (1,492 files) | B06 cut over | VERIFIED | `STATUS.md` D.25; dedup A04 removal_preferred |
| `/wsu/home/go/go24/go2432/VerSeFusion` | the VerSeFusion pipeline checkout (`.git`); `data` is a symlink to `/rs/rs_grp_oschome/go2432/data/versefusion/raw/VerSeFusion_data` since 2026-10-08 10:39; `data.pre-ceph` still present (no batch is finalized) | checkout small; `data.pre-ceph` 139 GB | B06 cut over, not finalized | VERIFIED | `results/nextpaper/Makefile` is the 2026-05-14 Makefile, longer than the committed one |
| `/wsu/home/go/go24/go2432/VerseFusion` (file, 24,769 B) and `/wsu/home/go/go24/go2432/VerSeFusion.tar.gz` | unknown | small | HOME | listed only | contents not recorded |

## 4. Labellers, weights and benches (HOME)

| path | holds | size | migration state | verified | notes and source |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/bench_ts` | SPINEPS+VERIDAH over 1,228 TS v2 + 374 VerSe CTs (`cases.csv`, `spineps/native/`) | 1.511 GB census | HOME; B11 not started | listed only | 31 "relabelled" masks are links back to raw masks (`docs/handoff/RECIPES.md` section 3.5) |
| `/wsu/home/go/go24/go2432/totalseg_weights` | TotalSegmentator weights | not sized | HOME | listed only | labeller B |
| `/wsu/home/go/go24/go2432/spineps_models` | SPINEPS model weights | not sized | HOME | listed only | labeller A |
| `/wsu/home/go/go24/go2432/rib-segmentation` | the Moller rib nnU-Net checkout (Zenodo 14864106, folds 0-2) | not sized | HOME | listed only | arm B |
| `/wsu/home/go/go24/go2432/model_night/anomaly_manifest` | `anomaly_manifest.csv`, `spine_classes.json`, `summary.json` (2026-09-17) | not sized | HOME | listed (folder) | `STATUS.md` D.1 |
| `/wsu/home/go/go24/go2432/lstv_flag` | `LEARNING_CURVE.md`, `LSTV_FLAG_RESULTS.md`, `ANOMALY_INVENTORY.md`, `_lstv_phenotypes.csv`, `models/` (registered flag models), the master flag table `lstv_flag_labels_v2.csv` (not seen in the `head -30` of the pass) | not sized | HOME; B11 | the flag models are registered | `memory/anomaly-manifest-sources.md` |
| `/wsu/home/go/go24/go2432/data/TotalSegmentator` (the v2 release, 1,228 CTs), `/wsu/home/go/go24/go2432/data/TotalSegmentator_v3` (1,939) | the two TS releases | 82.0 / 89.8 GB du (B07.tsv) | B07 copying on 2026-10-08 (no STATUS yet) | not yet | `/rs/rs_grp_oschome/go2432/data/validation_ts/raw/*` links point into the v2 tree |
| `/wsu/home/go/go24/go2432/lstv-detector` | the MRI lstv-detector tree | — | **ABSENT** on 2026-10-08 | — | its results survive only in `results/aaca_lstv_mri/` |
| `/wsu/home/go/go24/go2432/split_final.json`, `split_leak_report.json` | the frozen G3 person split (apply 2026-09-23 20:18:48, seed 0, job 40426793) | small | HOME; B11 | leak audit PASS | never rerun in place (`docs/handoff/RECIPES.md` section 3.1 step 4) |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` | the grid checkout, behind the laptop (4e3fe93 against 097933a) and unable to fetch | — | HOME | — | ship by `git archive | ssh tar` (`docs/handoff/RECIPES.md` section 0) |

## 5. Known missing or never there

| item | evidence | what to do |
|---|---|---|
| the review tree | no `/rs/rs_grp_oschome/go2432/review_tree` | `TODO.md` steps 2, 7 |
| the pelvis arm production run; arm A tier 2 remainder (848); Moller full configuration | `DECISION.json` n_timing 0; `arms/ts/STATUS.md` | `TODO.md` step 3; the held jobs 40481415-16, 40481574, 40481679 were cancelled on 2026-09-27 |
| the arm scripts in a repository | `/rs/rs_grp_oschome/go2432/ruleclass/code/` only | copy into spinesurg-ct-nnunet `slurm/ruleclass/` in a job and commit when Greg asks |
| human verdicts (446 registry review cases: verse 71, ctsp 72, totalsegmentator 137, cobra 79, other_ct 87, plus 103 labeller-validation renders = 549 contact-sheet tiles; the Castellvi whole-cohort read) | `REGISTRY.md` "Review queues" | readers (`TODO.md` steps 4, 5) |
| Dataset815 training | raw exists; `nnunet/results` has no Dataset815; both prep jobs died on a missing singularity path | `TODO.md` step 11 |
| Dataset803 `results/` tree | not on the grid | Hugging Face `OpenSpineConsortium/spinopelvic-seg-checkpoints` (`CLASSIFIERS.md` R36) |
| CTPelvic1K datasets 1-5 | B03 row 002 ABSENT; no `/rs/rs_grp_oschome/go2432/data/ctpelvic1k` | re-download in a job (Zenodo 4588403) if a count needs them |
| the seven gated collections and the 23 tier-2 / deferred collections | no agreement; the stopping rule | `TODO.md` steps 12, 13 |
| the lstv-detector grid tree | `~/lstv-detector` absent | the laptop results are in `results/aaca_lstv_mri/`; the code is on GitHub |
