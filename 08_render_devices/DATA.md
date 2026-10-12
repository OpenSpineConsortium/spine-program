# DATA.md: the grid paths of this folder, reached through Beethoven

This file lists every grid path of `MANIFEST_GRID.md` sections 1 and 2, spelled as the manifest spells it (`~` and
`$RS` kept), with its volume, what it holds, its size, its migration state and one read-only check line per path; then
the terms, the access facts of 2026-10-11, the way in through Beethoven and the first experiment (`TODO.md` step 1).
This folder is Greg-only until Greg confirms a hand-out (`CLAUDE.md` "Reader"); a student claims work here only after
that. Every number below restates `MANIFEST_GRID.md`, which names the file each one comes from (the read-only pass of
2026-10-08 22:20 UTC, the census of jobs 40580051 and 40580052, a batch STATUS file); where no file records a fact,
this file writes "not recorded". `MANIFEST_GRID.md` section 3 lists what is known missing; section 4 names credential
files that sit in HOME beside the banks, and no check line here reads them.

**Volumes.** HOME = `/wsu/home/go/go24/go2432` (written `~` in the manifest); Ceph = `/rs/rs_grp_oschome/go2432`
(written `$RS`; 20 TB, group `oschome`). `~` in the path column is Greg's HOME, not the reader's, so the check lines
spell it `$H`. Set once, then paste a check line:

```
H=/wsu/home/go/go24/go2432; RS=/rs/rs_grp_oschome/go2432
```

**How to run a check line.** From the Beethoven worker (section 2), never python or `du` on the login node
(`CLAUDE.md` rule 7). A directory gets `ls -ld <path>`; a file gets `head -c 200 <file>`. A check line written with
`{a,b}` expands in bash and covers each member; the braces carry no spaces. A check on a path recorded as absent is
expected to answer "No such file or directory"; that answer is the check.

**Migration words** (`MANIFEST_GRID.md` header, from `MIGRATION_PLAN.md` section 3): VERIFIED = copied and checked; cut
over = the HOME path is a symlink into Ceph with a `<path>.pre-ceph` twin beside it; FINALIZE (deleting the twin) had
run on no batch as of 2026-10-08. The states below are those of the read-only pass of 2026-10-08 22:20 UTC: **B00 and
B06 VERIFIED; B07 and B09 copying; B10 and B11 not started**. The state of each batch since is
`../10_data_platform_grid/MANIFEST_GRID.md` section 2; no STATUS file for any batch after 2026-10-08 is in this folder.
Truth for a batch is its STATUS file, `data_platform/plan/runs/<B>/STATUS`, read in a job or with `cat`.

## 1. Access on 2026-10-11 (Greg, issue #14)

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students: a named ACL entry on the
  volume root, other-read bits on folders and files. That includes `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds the
  PhysioNet credential and the VinDr and BUU agreements.
- On 2026-10-12 the VinDr and BUU items inside those folders opened too. Until then the plan's `restricted` flag
  still closed them item by item, mode `drwx--S---` (`vindr/raw`, `buu_full`, `buu_v1`, BUU-LSPINE 2000, the VinDr and
  BUU banks of B10 and B11, `dis_renders`); the script was fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs
  40599886 (the B04, B05, B10 and B14 folders) and 40599867 (after B13's finalize, every chain folder including
  `multisource_banks`) open them (issue #65).
- Two paths stay closed (owner-only):
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, private build material
  and not a dataset, and `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`, until Greg reads
  its Zenodo upload scripts for a token (issue #65;
  `../10_data_platform_grid/code/data_platform/plan/publish_visibility.sh`, from spinesurg-ct-nnunet d9b388d).
- Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students. Items still there are moved to
  the Ceph volume by the data-platform plan, whose batch-by-batch state is `../10_data_platform_grid/MANIFEST_GRID.md`
  section 2. Every such item in section 3 is marked **on HOME, not reachable until migrated**; Greg runs those check
  lines until the batches land.
- `$RS/model_night` sits at the Ceph root, not under `data/`, and the access facts above do not speak for it: whether
  a student can read it is not recorded. If its check is refused, Greg runs it.

## 2. Through Beethoven

Beethoven is the way a reader reaches these paths. The guides are
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (pages at https://openspineconsortium.com/beethoven/).

A reader needs: a WSU AccessID with a grid account, the Google Authenticator grid code, Claude Pro or Max, and Chrome
on the invited Google account. Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`
(issue #14).

The two access facts again, because they decide what a check line can answer:

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named ACL entry on the
  volume root; other-read bits on folders and files), including `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus` and, since 2026-10-12, the VinDr and BUU
  items inside them; two paths stay closed,
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (private build material,
  not a dataset) and `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` (until Greg reads its
  Zenodo upload scripts for a token).
- Nothing on `/wsu/home/go/go24/go2432` is readable by students; items still there are marked **on HOME, not
  reachable until migrated** below, and Greg runs the HOME check lines until the data-platform batches move them
  (`../10_data_platform_grid/MANIFEST_GRID.md` section 2).

Every computation this folder sends to the grid is an `sbatch -D <dir>` job on a compute node, chained with
`afterany`, with the job id and a timestamp written to the project's `JOBS.txt` (`docs/handoff/RECIPES.md` section 0
item 3) — never a command on the login node (`CLAUDE.md` rule 7).

## 3. HOME: the single-source render banks and the HOME trees (`MANIFEST_GRID.md` section 1)

Every row is **on HOME, not reachable until migrated**, except where the item is a link whose target is on Ceph.

| path | volume | what it holds | size | migration state (2026-10-08) | check line |
|---|---|---|---|---|---|
| `~/physics_drr` (dir 2026-09-14), `~/physics_drr_film` (2026-09-17) | HOME | 7,045 physics annotations (ctsp 2,430, totalseg 1,831, verse 1,463, implant 1,321; `ann/`, `img/`) and the film-styled twin; the same card's location notes say 7,048 (OQ B12) | not sized | on HOME, not reachable until migrated; B11 -> `$RS/data/multisource_banks/derived/physics_drr` and `_film`; not started | `ls -ld $H/{physics_drr,physics_drr_film}` |
| `~/physics_rare` (2026-09-14), `~/physics_rare_film` (2026-09-18) | HOME | 1,482 rare-anatomy annotations (34 CTSP ids 603 + 47 VerSe series 879); 9 of 56 VerSe rare series missing | not sized | on HOME, not reachable until migrated; B11; not started | `ls -ld $H/{physics_rare,physics_rare_film}` |
| `~/physics_smoke` (2026-09-14) | HOME | smoke test | not sized | on HOME, not reachable until migrated; B10 -> `$RS/data/ctspinopelvic1k/derived/physics_smoke`; candidate for deletion | `ls -ld $H/physics_smoke` |
| `~/ctsp_drr` (2026-09-22), `~/ctsp_drr_film` (2026-09-17) | HOME | 801 CTSP lateral parallel-beam DRRs, respaced 2026-09-19; 0533 re-rendered 2026-09-23 (job 40416626) and in no trained bank; 7,161 level instances, 18 L6 | 0.686 GB (`ctsp_drr`); `_film` not sized | on HOME, not reachable until migrated; B10 -> `$RS/data/ctspinopelvic1k/derived/ctsp_drr`; not started | `ls -ld $H/{ctsp_drr,ctsp_drr_film}` |
| `~/anchor_drr` (2026-09-23), `~/anchor_drr_c2` | HOME | 7,842 AP and lateral anchor renders (6,650 train / 1,192 val); 6,129 in `_c2`; the split puts 301 of 801 people on both sides: **a leaked bank, never quoted** (`CLAUDE.md` rule 5) | 0.713 GB and 0.377 GB (census 2026-10-08, job 40580052) against 2.6 GB and 1.7 GB (`DATA_MANIFEST.md`, listing 2026-09-23); the method behind the older figures is not recorded; not resolved | on HOME, not reachable until migrated; B10; not started | `ls -ld $H/{anchor_drr,anchor_drr_c2}` |
| `~/ts_drr` (2026-09-20) | HOME | TotalSegmentator v2.0.1 lateral DRRs: 1,170 ann + 1,170 img + 1,160 path; 58 of 1,228 skipped; path maps computed from the v3 root; not held out from the v9 encoder | not sized | on HOME, not reachable until migrated; B07 -> `$RS/data/totalsegmentator_v201/derived/ts_drr`; copying at 22:20 UTC | `ls -ld $H/ts_drr` |
| `~/ts_drr_v3` (2026-09-19) | HOME | TotalSegmentator v3.0.0 lateral DRRs: 1,735 anns, 204 skipped, no `path/`; read by nothing; its anns claim the v201 source string | not sized | on HOME, not reachable until migrated; B07 (candidate); copying | `ls -ld $H/ts_drr_v3` |
| `~/implant_ts` (2026-09-14) | HOME | synthetic hardware CTs over TotalSegmentator: 1,629 over 817 subjects; 355 subjects never processed | 39.0 GB (du 2026-09-01) | on HOME, not reachable until migrated; B07 -> `$RS/data/totalsegmentator_v201/derived/implant_ts` (candidate); copying | `ls -ld $H/implant_ts` |
| `~/implant_ct_smoke`, `~/implant_verse_smoke` | HOME | smoke tests | not sized | on HOME, not reachable until migrated; B11; deletion candidates | `ls -ld $H/{implant_ct_smoke,implant_verse_smoke}` |
| `~/cut_physics`, `~/cut_physics_v2` | HOME | CUT translations of `physics_drr`, 3,000 each; translator weights `cut_drr2fluoro_G`, `cut_drr2fluoro_G_v2` (47,787,714 B each) | 1.236 GB each, 6,000 files each (census 2026-10-08, job 40580052) | on HOME, not reachable until migrated; B11 -> `$RS/data/multisource_banks/derived/cut_physics*`; not started | `ls -ld $H/{cut_physics,cut_physics_v2}` |
| `~/cut_rare`, `~/cut_rare_v2` | HOME | CUT translations of `physics_rare`, 1,482 each | 0.610 GB each, 2,964 files each (census 2026-10-08, job 40580052) | on HOME, not reachable until migrated; B11; not started | `ls -ld $H/{cut_rare,cut_rare_v2}` |
| `~/cut_v1`, `~/cut_v2` | HOME | the CUT training runs (`G_last.pt`, previews); v1 invalid (MRI slices and photographs in the target domain); v2 restricted to classifier-verified spine panels | not sized | on HOME, not reachable until migrated; B11; not started | `ls -ld $H/{cut_v1,cut_v2}` |
| `~/fluorogen` | HOME | FluoroGen: env clone, LoRA `lora_v1`, `dataset_v1`, `synth_v1`, `synth_rare` (12,929 restyled renders over 2,844 cases; in no bank), `synth_rare_lowstrength/preview` | `synth_rare` 9.0 GB; the rest not sized | on HOME, not reachable until migrated; B09 -> `$RS/data/fluorocap/raw` and `fluorogen_synthetic` (absent at 22:20); copying | `ls -ld $H/fluorogen` |
| `~/exp3_fluoro`, `~/exp3_radiograph`, `~/exp3_ctx_fluoro`, `~/exp3_ctx_radiograph` | HOME | exp3 renders: 1,058 over 120 cases, and their context banks | not sized | on HOME, not reachable until migrated; B10 -> `$RS/data/ctspinopelvic1k/derived/exp3_*`; not started | `ls -ld $H/{exp3_fluoro,exp3_radiograph,exp3_ctx_fluoro,exp3_ctx_radiograph}` |
| `~/film_style_ds` | HOME | the film-style dataset; **restricted: real film pixels** | not sized | on HOME, not reachable until migrated; B11 -> `$RS/data/multisource_banks/derived/film_style_ds` (restricted in the plan; readable by approved students after job 40599867); not started | `ls -ld $H/film_style_ds` |
| `~/polypose` (2026-09-23) | HOME | the PolyPose HOME working directory | not sized | on HOME, not reachable until migrated; B10 -> `$RS/data/polypose/derived/polypose_home`; not started | `ls -ld $H/polypose` |
| `~/deepfluoro` -> `$RS/data/deepfluoro_h5/raw/deepfluoro` | HOME link to Ceph | the DeepFluoro H5 release (76 files; `unpacked_full` 2.54 GB) | 5,272,150,583 B (STATUS) | B00 **VERIFIED** 76/76, 76 sampled; cut over 2026-10-08 05:52. The HOME link is not readable by students; its target, under `data/`, is | `ls -ld $RS/data/deepfluoro_h5/raw/deepfluoro` |
| `~/data/TotalSegmentator` (dir 2026-09-14, 1,230 entries) | HOME | TotalSegmentator v2.0.1, 1,228 CTs, zip + unpacked | 82.0 GB (du, B07.tsv) | on HOME, not reachable until migrated; B07 -> `$RS/data/totalsegmentator_v201/raw/TotalSegmentator` (candidate); copying; `$RS/data/totalsegmentator_v201` absent at 22:20 | `ls -ld $H/data/TotalSegmentator` |
| `~/data/TotalSegmentator_v3` (2026-09-19) | HOME | TotalSegmentator v3.0.0, 1,939 CTs incl. 291 paediatric (37,415,622,057 B zip) | 89.8 GB (du) | on HOME, not reachable until migrated; B07 -> `$RS/data/totalsegmentator_v300/raw/TotalSegmentator_v3`; that `raw` exists with 1 entry at 22:20 | `ls -ld $H/data/TotalSegmentator_v3` |
| `~/spine-detector/runs/devcorpus/` | HOME | the styled-corpus detectors `dc_A_held_*`, `dc_B_held_*`, `*_1dev_*`, `*_s1`, `dc_P_pooled` (19 runs per the C-arm inventory, 21 arms per the grid inventory; not settled, `TODO.md` step 25); `scores.json` per run; `dc_P_pooled/weights/best.pt` 40,601,765 B 2026-09-23; no registry alias | about 40 MB per run (one file sized) | on HOME, not reachable until migrated; stays on HOME (code and runs) in the manifest, the B13 results batch not run on 2026-10-08 | `ls -ld $H/spine-detector/runs/devcorpus` |
| `~/model_night/` | HOME | `PIPELINE_STATE.md`, `ts_clean_subjects.txt` (the 142 clean TS subjects of the device corpus), `anchor_<dr>_r2/` arms, `sweep_v3/`, `scaling/SCALING_CURVE.json` (superseded) | not sized | on HOME, not reachable until migrated; stays on HOME (jobs in flight) | `head -c 200 $H/model_night/PIPELINE_STATE.md` |
| `~/model_registry/` | HOME | the content-addressed weights store; aliases that bear on this folder: `anchor_detector_v1`, `cut_drr2fluoro_G`, `cut_drr2fluoro_G_v2`, `fluorogen_lora_v1`; the `dc_*` detectors are NOT registered | ledger 106 lines, 79 aliases | on HOME, not reachable until migrated; no batch recorded | `ls -ld $H/model_registry` |
| `~/FluoroCap/` | HOME | `rare_cases_ctsp.txt` (34), `rare_cases_verse.txt` (56) that select `physics_rare`; `anchor_det_v1.pt`; `cut_eval_{films,allspine}_*_v2.json`; FluoroCap is private and out of training | not sized | on HOME, not reachable until migrated; B09 copying | `ls -ld $H/FluoroCap` |
| `~/spinesurg-ct-nnunet/` | HOME | the grid checkout at 4e3fe93 (behind 097933a); a refit writes the cards into its `docs/devices/`; `make physics` hard-resets it; it cannot fetch | not sized | on HOME, not reachable until migrated; stays on HOME (code) | `ls -ld $H/spinesurg-ct-nnunet/docs/devices` |

## 4. Ceph: the VerSe banks, the device corpus, PolyPose, the result tree (`MANIFEST_GRID.md` section 2)

Every row under `$RS/data/` is readable by approved students (section 1). `$RS/model_night` is at the Ceph root: its
access is not recorded.

| path | volume | what it holds | size | migration state (2026-10-08) | check line |
|---|---|---|---|---|---|
| `$RS/data/versefusion/derived/implant_verse` | Ceph | synthetic hardware CTs over VerSe, 1,119 = 373 x 3; regenerable by `tools/make_implant_ct.py` | 2,254 files, 159,368,901,079 B (STATUS) | B06 **VERIFIED**; cut over; deletion candidate | `ls -ld $RS/data/versefusion/derived/implant_verse` |
| `$RS/data/versefusion/derived/verse_drr` | Ceph | 387 VerSe lateral DRRs = 374 + 13 byte-identical `glgl*` twins; the bank the v9 encoder trains on | 1,492 files, 477,053,118 B | B06 **VERIFIED**; cut over | `ls -ld $RS/data/versefusion/derived/verse_drr` |
| `$RS/data/versefusion/derived/verse_drr_film` | Ceph | film-styled twin, 374 | 757 files, 98,040,685 B | B06 **VERIFIED** | `ls -ld $RS/data/versefusion/derived/verse_drr_film` |
| `$RS/data/versefusion/derived/verse_drr_obl`, `verse_drr_obl2` | Ceph | oblique VerSe renders, 4 poses (1,494) and 8 poses (2,989) | 2,988 files, 386,300,026 B; 5,978 files, 773,608,215 B | B06 **VERIFIED** | `ls -ld $RS/data/versefusion/derived/{verse_drr_obl,verse_drr_obl2}` |
| `$RS/data/versefusion/derived/verse_soft_drr` | Ceph | soft-tissue lateral DRRs, 374; row spacing wrong on 181; read only by `vsoft_fov48_ctx` | 748 files, 97,063,296 B | B06 **VERIFIED** (candidate: re-render or retire) | `ls -ld $RS/data/versefusion/derived/verse_soft_drr` |
| `$RS/data/versefusion/derived/ctsp_drr_obl`, `ctsp_drr_obl2` | Ceph | misnamed: VerSe renders under a CTSP prefix (1,256 and 2,511 renders of 314 series); retire | 2,512 files, 365,536,630 B; 5,022 files, 729,979,464 B | B06 **VERIFIED** (candidates) | `ls -ld $RS/data/versefusion/derived/{ctsp_drr_obl,ctsp_drr_obl2}` |
| `$RS/data/versefusion/derived/obl2_fov96_ctx`, `verse_only_ctx` | Ceph | context crop banks built from the oblique renders | 9 files, 13,327,845,295 B; 42 files, 743,721,823 B | B06 **VERIFIED** | `ls -ld $RS/data/versefusion/derived/{obl2_fov96_ctx,verse_only_ctx}` |
| `$RS/data/versefusion/derived/vf_813`, `vf_813_probe`, `vf_v10` | Ceph | the nnU-Net conversion of VerSeFusion (C1 to T9 sent to ignore: never for whole-spine renders), its probe and the v10 variant; HOME `~/vf_813` and `~/vf_v10` are symlinks | 1,130 files, 49,427,512,778 B; 4 files, 139,428,370 B; 374 files, 319,212,368 B | B06 **VERIFIED**; cut over | `ls -ld $RS/data/versefusion/derived/{vf_813,vf_813_probe,vf_v10}` |
| `$RS/data/versefusion/raw/VerSeFusion_data` | Ceph | the fused VerSe'19+'20 corpus (`data/unified`, the render source) | 6,951 files, 194,191,642,435 B | B06 **VERIFIED** | `ls -ld $RS/data/versefusion/raw/VerSeFusion_data` |
| `$RS/data/devcorpus` (dir 2026-09-22, 4 entries: `lists`, `poses`, `render`, `styled`) | Ceph | the styled device corpus: 142 TotalSegmentator v3 whole spines, 4,551 files; five styled corpora, each with a `__typicality` twin | 18.280 GB, 99,389 files (census 2026-10-08, job 40580051) against 2.45 GB (`LAYOUT.md`; `DATA_MANIFEST.md` line 1660, listing 2026-09-22); not resolved | Ceph-native | `ls -ld $RS/data/devcorpus` |
| `$RS/data/devcorpus_arc` (2026-09-24, 6 entries) | Ceph | the device-corpus arc renders (the coverage arms of A11.1) | not sized | Ceph-native | `ls -ld $RS/data/devcorpus_arc` |
| `$RS/data/polypose` (2026-09-23, 11 entries) | Ceph | PolyPose: `env/venv`, `sif/polypose_base.sif`, `hf/hub` (the DeepFluoro Hugging Face re-host), `forward_test/`, the cohort bank, `validation/smoke`, `validation/bank_{gravity,invdf1}` (not confirmed in the listing); `VALIDATION.{json,md}` does not exist | 87.713 GB, 114,371 files (census 2026-10-08, job 40580051); 82.0 GB (`CENSUS_TABLE_2026-09-25.md`); the cohort alone not sized | Ceph-native | `ls -ld $RS/data/polypose` |
| `$RS/data/or_ready/devices` (8 entries, names not in the project 10 listing), `devices_refit`, `devices_refit_constrained`, `devices_refit_v2` | Ceph | the fitted cards with their figures and `FIT_DONE` markers; the two grid-only cards (`surgio_b51_dr`, `varian_halcyon` by the C-arm inventory's `ls`); whether the refits were under `DF_CONVERSION=linear` is OQ B9 (section 7) | inside `or_ready` (867.951 GB, 340,064 files whole; census 2026-10-08, job 40580051) | Ceph-native | `ls -ld $RS/data/or_ready/{devices,devices_refit,devices_refit_constrained,devices_refit_v2}` |
| `$RS/data/or_ready/{lodo, corpus_manifold, coverage, arc, devlodo, devpool, crossdev, indomain, lcurve, audit, eval_gate, auto_reference, story_rows_f3, story_rows_f6}` | Ceph | the OR-readiness result tree shared with project 01: `lodo/rescore_outline.md` (the 90.6 / 83.9 % baseline), `corpus_manifold/overlap.json` (A13.5), `devlodo/<design>_held_<dev>_DONE` markers, the coverage experiment | the same 867.951 GB `or_ready` whole | Ceph-native | `head -c 200 $RS/data/or_ready/lodo/rescore_outline.md` |
| `$RS/data/deepfluoro_vendor` (`unpacked` 72.71 GB), `$RS/data/deepfluoro_h5` | Ceph | the vendor deposit (DOI C304HZ) and the H5 release (IFSXNV): one dataset with the HF re-host; key by specimen across all three | 104.0 GB; 5.27 GB | Ceph-native; B00 **VERIFIED** (`deepfluoro_h5`) | `ls -ld $RS/data/{deepfluoro_vendor,deepfluoro_h5}` |
| `$RS/data/geneva_hip_src`, `$RS/data/ljubljana` (0.31 GB), `$RS/data/spinesac` (`drive` 4.15 GB), `$RS/data/realxray` (3.86 GB), `realxray_work` | Ceph | the frame sources of the BV Pulsera (Geneva phantom), PIXIUM 4600 (Ljubljana) and SpineSAC cards and the header census (2 to 901 DICOM headers per device under `spinesac/drive` and `carmlspine/unpacked`) | as given; `geneva_hip_src` and `realxray_work` not sized | Ceph-native | `ls -ld $RS/data/{geneva_hip_src,ljubljana,spinesac,realxray,realxray_work}` |
| `$RS/data/totalsegmentator_v300/raw` (1 entry at 22:20) | Ceph | the B07 landing folder for v3.0.0 | not sized (copying) | B07 copying | `ls -ld $RS/data/totalsegmentator_v300/raw` |
| `$RS/model_night` | Ceph (root, not `data/`) | anchor rounds (`anchor_*`, refiners) | 0.831 GB, 33,507 files (census 2026-10-08, job 40580051) | Ceph-native | `ls -ld $RS/model_night` |
| `$RS/data/morphdef` | Ceph | three empty folders (`logs/`, `out/`, `src/`, 2026-09-23 02:15): the scaffold of the stopped morphology-deformation line; remove with `rmdir` in a job | 0 | removal candidate | `ls -ld $RS/data/morphdef` |

## 5. Terms

- **TotalSegmentator v2.0.1** is CC BY 4.0 (Zenodo 10.5281/zenodo.10047292; `MANIFEST_GRID.md` section 1 row
  `~/data/TotalSegmentator`). It covers `~/data/TotalSegmentator` and the banks rendered from it (`ts_drr`,
  `implant_ts`, the totalseg rows of `physics_drr`).
- **TotalSegmentator v3.0.0** (Zenodo 10.5281/zenodo.22688904): the folder records it as "open"
  (`docs/handoff/literature_state/dataset_landscape_by_task.md` line 107) and names no licence: not recorded in the
  folder. The same holds for what inherits from it (`ts_drr_v3`, `$RS/data/devcorpus`, `devcorpus_arc`).
- **The render banks derive from NC-licensed data** (`CLAUDE.md` "Reader"). The NC sources the folder names are
  CTSpine1K (CC BY-NC-SA 4.0) and the CTSpinoPelvic1K labels (CC BY-NC-SA 4.0)
  (`docs/handoff/literature_state/dataset_landscape_by_task.md` lines 101 and 102), behind `ctsp_drr`, `exp3_*` and the
  CTSP rows of `physics_drr` and `physics_rare`.
- **`$RS/data/ljubljana` is read-only under its ND licence**: "CC BY-NC-ND or a signed agreement"
  (`docs/handoff/literature_state/dataset_landscape_by_task.md` line 180). Nothing derived from it is redistributed.
  The shipped PIXIUM 4600 card records `fit.pairs_dir` `/rs/rs_grp_oschome/go2432/data/ljubljana/pairs`
  (`results/devices/pixium_4600.json`), so an earlier fit wrote inside that folder; whether the licence allows that
  is not recorded in the folder.
- **DeepFluoro is non-commercial** (`../01_carm_level_detection/CLAUDE.md` "Data": "CTSpine1K derivatives,
  DeepFluoro and COBRA are non-commercial"). That covers `~/deepfluoro`, `$RS/data/deepfluoro_vendor`,
  `$RS/data/deepfluoro_h5`, the Hugging Face re-host under `$RS/data/polypose/hf/hub`, and the Cios Fusion card fitted
  on it; COBRA, the source of the Elekta XVI card's frames, is non-commercial by the same line.
- **`~/film_style_ds` holds real film pixels** and is restricted in the plan (`MANIFEST_GRID.md` section 1); its B11
  copy was owner-only until 2026-10-12 and is readable by approved students after visibility job 40599867 (section 1).
- Recorded for the other card sources: the Geneva hip gold standard is CC BY-SA 4.0, though its paper says BY-NC
  (`dataset_landscape_by_task.md` line 179); SpineSAC has no data licence (`docs/handoff/DATASET_USAGE.md` line 133);
  VerSe is "CC BY-SA 4.0 or CC BY 4.0, quoted both ways" (`dataset_landscape_by_task.md` line 104). FluoroCap is
  private and out of training (`CLAUDE.md` rules 8 and 9).
- Otherwise: not recorded in the folder. That includes the PolyPose environment and container, the CUT and FluoroGen
  outputs as such, and the terms for redistributing any render bank.

**The bank traps of `CLAUDE.md`, repeated** (every one binds a reader of the tables above):

- The A-P voxel size was once written as the S-I row spacing: every sweep before `sweep_v3` rendered the wrong field
  size; `ctsp_drr` was respaced 2026-09-19; 181 of 374 `verse_soft_drr` renders still carry the defect
  (`memory/drr-row-spacing-defect.md`).
- Physics-perturbed sweeps once rendered with no bone: anything measured under `--perturb physics` before the
  bone-path fix is not quotable; use `make_drr_dataset --paths2-only` (`memory/sweep-physics-no-bone.md`, its causal
  reading superseded by `memory/physics-three-defects-measured.md`).
- DeepFluoro frames were once converted as a log of a log; the fix is `DF_CONVERSION=linear`, and whether the cards
  were refitted afterwards is not confirmed (OQ B9, section 7). 160 of 366 frames were stored upside down; the focal
  length -5257.7 px stays signed; the volume is indexed (z, y, x). The H5 release, the vendor deposit and the Hugging
  Face re-host are one dataset in three copies: key by specimen across all three.
- The exposure clip saturates: `device_style.SPREAD = 0.2` pins a term on 94.9 to 98.3 % of styled frames; the
  typicality gate is written but the clip is the default until an A/B on real frames decides
  (`docs/DEVICE_SPREAD_SWEEP.md`).
- Cards are written in the grid repository copy: a refit overwrites `docs/devices/<device>.json` in
  `~/spinesurg-ct-nnunet`; copy the shipped card aside first. The Surgio-B51 and Varian Halcyon cards exist only on the
  grid. `make physics` hard-resets that checkout; only `make physics-tables` is safe (`docs/handoff/RECIPES.md`
  sections 0 and 6).
- Bank names lie: `ctsp_drr_obl` and `ctsp_drr_obl2` are VerSe renders; `verse_drr` holds 13 byte-identical `glgl*`
  duplicates; `ts_drr`'s path maps were computed from the v3 root; `ts_drr_v3` is read by nothing; `anchor_drr`'s own
  split puts 301 of 801 people on both sides; `vf_813` maps C1 to T9 to ignore, so whole-spine work reads the raw
  VerSeFusion masks.
- Two counts for one bank: `physics_drr` is 7,045 in `contents.items` and 7,048 in the location notes (OQ B12, G1).
- TotalSegmentator's `sacrum` excludes S1; the whole sacrum is the union. The device corpus calls its source "v2"
  while the path is v3 (OQ F6).
- Only design P's list builder refuses a subject on two sides; designs A and B do not, and design A renders every card
  under the Cios Fusion pose pool, which includes DeepFluoro test specimen 18-1109 (`docs/handoff/LEAKAGE.md`
  section 3; OQ C15).
- Never quote from `anchor_drr`; `ts_drr` is not held out from the v9 encoder (`CLAUDE.md` rule 5).

## 6. The cards on disk that bear on B9 (read 2026-10-12 from this folder, nothing on the grid)

The six JSON files in `results/devices/` stamp `fit.code_sha` 6e1cf8d and `fit.date` 2026-09-22 (06:32 BV Pulsera,
06:43 Cios Fusion, 06:55 PIXIUM 4600, 07:57 Elekta XVI). The Cios Fusion card, the DeepFluoro one, records
`fit.pairs_dir` `/wsu/home/go/go24/go2432/model_night/deepfluoro/pairs`. No card's `fit` block carries a conversion
field. The fix is dated 2026-09-21 15:10 (`memory/learned-formation-refuted-calibrate-instead.md` line 109), but the
code kept `"log"` as the default "so that every earlier number reproduces"; the calibration records `--conversion` in
its JSON, and the linear refit was to rebuild the pairs under
`/rs/rs_grp_oschome/go2432/model_night/anchor_pairs_lin_<spec>` with results `*_linear.json`
(`docs/DEEPFLUORO_FORMATION.md` lines 395 to 401). A fit date after the fix therefore does not answer B9; a recorded
conversion value or a `_lin` pairs root does. Whether the grid copies match these files is not recorded.

## 7. First experiment (`TODO.md` step 1): one read-only job answers B9 and B10

One `sbatch -D <dir>` job on `reqp --qos=requeue` (`docs/handoff/RECIPES.md` section 0 item 4) reads
`$RS/data/or_ready/devices_refit`, `devices_refit_constrained`, `devices_refit_v2` (and `devices` beside them) and
`~/spine-detector/runs/devcorpus/*/scores.json`. It lists, greps and prints; it writes nothing but its own log.

- **B9**: were the DeepFluoro cards refitted under `DF_CONVERSION=linear`? Yes only if a refit records the
  conversion as linear or names a `_lin` pairs root; a refit that records `log` is a no; a refit that records neither
  is "not recorded", not a no (section 6).
- **B10**: which box convention the `scores.json` rows use, and why `dc_B_held_cios_fusion_s1` has no row. The three
  conventions are outline, body and centre: `rescore_outline.md` scores "6 arms x 3 sets x 16 thresholds x 3 box
  conventions" and its quoted cells are `lodo_carm_heldout_vert_outline_025`, `_vert_body_025` and
  `_vert_centre_025` (`../01_carm_level_detection/results/schwingnet/RIGOR_FIXES.md` line 46). C7's 97 % is fixed on
  the outline convention (`ssn:docs/MODEL_CARD.md` 4.6, point 1; copy at `../01_carm_level_detection/docs/MODEL_CARD.md`
  line 287).
- **Who runs it.** `~/spine-detector/runs/devcorpus`, the grid checkout's cards and the python named below are on
  HOME, so Greg runs it until those paths move; the `$RS/data/or_ready` reads alone would answer for an approved
  student, whose environment is `../11_students_grid_access/STUDENT_ENV.md` (issue #66).
- **Against** `MODEL_CARD.md` section 4.6 (`ssn:docs/MODEL_CARD.md`, read 2026-09-22; the rows whose `status` is
  `DEVICE-HELD-OUT`):

| run | design | held-out device | test set | frames | vertebra recall | sacrum found |
|---|---|---|---|---:|---:|---:|
| `dc_A_held_cios_fusion` | A | Cios Fusion | deepfluoro/test | 104 | 0.9157 | 1.0000 |
| `dc_A_held_cios_fusion_s1` | A (seed 1) | Cios Fusion | deepfluoro/test | 104 | 0.9157 | 1.0000 |
| `dc_B_held_cios_fusion` | B | Cios Fusion | deepfluoro/test | 104 | 0.9398 | 1.0000 |
| `dc_A_held_elekta_xvi` | A | Elekta XVI | cobra_elekta/test | 648 | 0.3024 | 0.3415 |
| `dc_A_held_elekta_xvi_s1` | A (seed 1) | Elekta XVI | cobra_elekta/test | 648 | 0.3135 | 0.2989 |
| `dc_B_held_elekta_xvi` | B | Elekta XVI | cobra_elekta/test | 648 | 0.3270 | 0.3645 |
| `dc_A_held_elekta_xvi_1dev_surgio_b51_dr` | A, one training device | Elekta XVI | cobra_elekta/test | 648 | 0.1221 | 0.0805 |
| `dc_A_held_surgio_b51_dr_s1` | A (seed 1) | Surgio-B51 | carmlspine/test | 56 | 0.1429 | 0.8214 |
| `dc_B_held_surgio_b51_dr_s1` | B (seed 1) | Surgio-B51 | carmlspine/test | 56 | 0.1498 | 0.8571 |
| `dc_B_held_cios_fusion_s1` | B (seed 1) | Cios Fusion | | | no row | |

These rows are SUPERSEDED for the paper by the contribution-matrix scoring and wait on B10 (`STATUS.md` section 4,
C4.6); the job reconciles them, it does not make them quotable.

**The two files.** Save both in one directory you own (the folder records no output directory for this job: not
recorded), then submit from there:

`read_b9_b10.sh`

```bash
#!/bin/bash
#SBATCH --job-name=b9b10_read
#SBATCH --partition=reqp
#SBATCH --qos=requeue
#SBATCH --no-requeue
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:30:00
#SBATCH --output=b9b10_read_%j.out
# TODO.md step 1 (OQ B9, B10). Read-only: lists, greps and prints; writes nothing but this log.
export PYTHONNOUSERSITE=1
H=/wsu/home/go/go24/go2432
RS=/rs/rs_grp_oschome/go2432
OR=$RS/data/or_ready
PY=$H/mambaforge/envs/spineps/bin/python
TS='%TY-%Tm-%Td %TH:%TM %12s %p\n'

echo "== B9: the card folders and the refits"
for d in devices devices_refit devices_refit_constrained devices_refit_v2; do
  echo "-- $OR/$d"
  ls -la --time-style=full-iso "$OR/$d" 2>&1
  find "$OR/$d" -maxdepth 3 \( -name '*.json' -o -name 'FIT_DONE' -o -name '*.log' -o -name '*.out' \) -printf "$TS" 2>&1 | sort | head -300
  grep -rIn -E 'conversion|DF_CONVERSION|_linear|anchor_pairs_lin|"pairs_dir"|"code_sha"|"date"' --include='*.json' --include='*.md' --include='*.log' --include='*.out' --include='*.txt' "$OR/$d" 2>&1 | cut -c1-300 | head -300
done
echo "-- the linear rebuild named in docs/DEEPFLUORO_FORMATION.md"
ls -ld "$RS"/model_night/anchor_pairs_lin_* 2>&1
find "$RS/model_night" "$H/model_night/deepfluoro" -maxdepth 3 \( -name '*_linear.json' -o -name 'calibration_*.json' \) -printf "$TS" 2>&1 | sort
echo "-- the grid checkout's cards"
ls -la --time-style=full-iso "$H/spinesurg-ct-nnunet/docs/devices" 2>&1
grep -Hno -E '"(date|code_sha|pairs_dir|conversion)" *: *"[^"]*"' "$H"/spinesurg-ct-nnunet/docs/devices/*.json 2>&1

echo "== B10: the box convention of the scores.json rows"
echo "-- the conventions file"
head -c 4000 "$OR/lodo/rescore_outline.md" 2>&1
R=$H/spine-detector/runs/devcorpus
ls -la --time-style=full-iso "$R" 2>&1
for f in "$R"/*/scores.json; do
  echo "-- $f $(stat -c '%s B %y' "$f")"
  grep -o -i -E '"[a-z_]*(conv|box|truth|outline|body|centre|center|iou|conf)[a-z_]*" *: *[^,}]{0,80}' "$f" | sort | uniq -c | head -40
done
"$PY" held_out_rows.py "$R"/*/scores.json 2>&1
echo "-- the run with no row"
ls -la --time-style=full-iso "$R/dc_B_held_cios_fusion_s1" "$R/dc_B_held_cios_fusion_s1/weights" 2>&1
echo "== done"
```

`held_out_rows.py`

```python
# Print every DEVICE-HELD-OUT row of each scores.json given (TODO.md step 1, OQ B10). Read-only.
import json
import sys


def walk(node, where):
    if isinstance(node, dict):
        if node.get("status") == "DEVICE-HELD-OUT":
            print(where or "/", json.dumps(node, sort_keys=True)[:2000])
        for key, value in node.items():
            walk(value, where + "/" + str(key))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            walk(value, where + "[" + str(i) + "]")


for path in sys.argv[1:]:
    with open(path) as fh:
        doc = json.load(fh)
    keys = sorted(doc) if isinstance(doc, dict) else type(doc).__name__
    print("==", path, "top-level:", keys)
    walk(doc, "")
```

**Submit, record, stop.** `sbatch -D <that directory> read_b9_b10.sh`; the `--output` resolves against that directory.
Write the job id with a timestamp into the project's `JOBS.txt` (`docs/handoff/RECIPES.md` section 0 item 3). The
wall time is not recorded; 30 minutes is the job's limit, not a measured duration.

**Gate** (`TODO.md` step 1; `README.md` S1 and S2): `MODEL_CARD.md` section 4.6 reconciled with every `scores.json`
row, value by value against the table above; the box convention named with the file and key that says it; the missing
`dc_B_held_cios_fusion_s1` row explained from its folder; the B9 answer read from a recorded conversion or pairs root;
both answers written into `STATUS.md` section 4 with the file and the job id. If no refit under the linear conversion
is found, `TODO.md` step 10 refits the Cios Fusion card after copying the shipped card aside; step 3 (the paired
bootstrap) waits on the convention.

## 8. Not recorded

The STATUS lines of any batch after the read-only pass of 2026-10-08 (no STATUS for B07, B09, B10, B11 or B13 after
that date is in this folder; their state is `../10_data_platform_grid/MANIFEST_GRID.md` section 2); the outcome of
visibility jobs 40599886 and 40599867; whether a student can read
`$RS/model_night`; the sizes marked "not sized" above, and which of the two sizes is right for `anchor_drr`,
`anchor_drr_c2` and `$RS/data/devcorpus`; the eight entry names of `$RS/data/or_ready/devices` and the run count under
`~/spine-detector/runs/devcorpus` (19 against 21; `TODO.md` step 25); the licence of TotalSegmentator v3.0.0 and of
everything section 5 does not name; whether the grid copies of the cards match `results/devices/`; the box convention
of the `scores.json` rows and the refit conversion (the first experiment reads them); an output directory and a wall
time for the first experiment.
