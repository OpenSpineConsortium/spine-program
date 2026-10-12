# DATA.md: the grid paths of this folder, reached through Beethoven

This file lists every grid path of `MANIFEST_GRID.md` sections 1 to 4, spelled as the manifest spells it, with its
volume, what it holds, its size and migration state as recorded, and one read-only check line per path. The access
facts are Greg's, dated 2026-10-11 (issue #12). Every number below restates `MANIFEST_GRID.md`, which names the file
each one comes from (the read-only grid listing of 2026-10-08 22:20 UTC, the two size censuses, the `data_platform`
plan files of the private repository at 097933a, the handoff catalog); where a size or a fact is in no file, this
file writes "not recorded". `MANIFEST_GRID.md` section 5 lists the jobs of record and section 6 what is known missing
or never there.

**Who reads this folder.** Greg only (`CLAUDE.md` first paragraph: SchwingNet and level-identification content); a
student claims work here only after Greg confirms a hand-out. The access facts below are recorded anyway, because
they decide which check lines an approved student could run if Greg hands any of this out, and which only Greg can.

**How to run a check line.** Every check runs from the Beethoven worker (`../11_students_grid_access`), never python
or `du` on the login node (`CLAUDE.md`, the grid rule). A directory gets `ls -ld <path>`; a file gets
`head -c 200 <file>`. A check line written with `{a,b}` expands in bash and covers each member; the braces carry no
spaces. A check on a path recorded as absent is expected to answer "No such file or directory" — that answer is the
check. One exception: `/wsu/home/go/go24/go2432/.fluorocap` holds credentials and is never read (`MANIFEST_GRID.md`
section 3); it gets `ls -ld` only, never `head`.

**Volumes.** HOME = `/wsu/home/go/go24/go2432` (Panasas, 4.3 TB soft quota, was 93 % full). Ceph =
`/rs/rs_grp_oschome/go2432` (CephFS, 20 TB, group `oschome`). Every path below is spelled in full, so a copy never
depends on this line (`MANIFEST_GRID.md` header).

## 1. Access on 2026-10-11 (Greg, issue #12)

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students: a named ACL entry on the
  volume root, other-read bits on folders and files. That includes `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds the
  PhysioNet credential and the VinDr and BUU agreements.
- The one closed path is `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`.
- Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students. Items still there are being
  moved to the Ceph volume by the data-platform plan (batches B05, B10, B11, B13 running on 2026-10-12). Every such
  item in the tables below is marked **on HOME, not reachable until migrated**; Greg runs those check lines until the
  batches land.
- Every Ceph path this folder uses sits under `/rs/rs_grp_oschome/go2432/data/` (sections 3 and 4 below), so the
  first bullet covers them all; this folder has no path at the Ceph root.

## 2. Through Beethoven

Beethoven is the way a student reaches these paths. The guides are
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md` (pages at https://openspineconsortium.com/beethoven/).

A student needs: a WSU AccessID with a grid account, the Google Authenticator grid code, Claude Pro or Max, and
Chrome on the invited Google account. Approved means a named ACL entry `user:<AccessID>:rwx` on
`/rs/rs_grp_oschome` (issue #12).

The two access facts again, because they decide what a check line can answer:

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named ACL entry on the
  volume root; other-read bits on folders and files), including `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`; the one closed path is
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`.
- Nothing on `/wsu/home/go/go24/go2432` is readable by students; items still there are marked **on HOME, not
  reachable until migrated** below, and Greg runs the HOME check lines until batches B05, B10, B11 and B13 land.

## 3. Paper 2's gate material (`MANIFEST_GRID.md` section 1; Ceph, under `data/`, readable by approved students)

| path (as the manifest spells it) | volume | holds | state | check, from the Beethoven worker |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/fig6` | Ceph | paper 2 Figure 6 (LevelCheck) material: 17 subdirectories, 22 entries, dir mtime 2026-09-25 00:22: `bank_g3_v2`, `detector_g3`, `frozen_v1`, `eval_v2_g3`, `gatecheck_v2_g3_pre`, `unblinding/`, `HOLD_README.txt`, `EVAL_SUBMITTED.json`, `RELEASE_OPEN_GATE.json`, `G5_MANIFEST.json`; 13.920 GB census, 86,277 files, newest 2026-09-25 | Ceph-native, stays; `G5_MANIFEST.json` identical here and in the grid checkout at release | `ls -ld /rs/rs_grp_oschome/go2432/data/fig6` |
| `/rs/rs_grp_oschome/go2432/data/fig6/bank_g3_v2` | Ceph | the G3 clean crop bank: 134,975 crops (116,706 train / 18,269 val; 8,950 / 1,079 persons), `meta.json` sha256 f78dd1ee...; `runs/model_rung_1_g3clean_aug2.pt` (the ImageNet-root G3 encoder, sha256 629f0e05...); not sized on its own | Ceph-native; BANK_CHECK PASS before every D1 job (`results/paper2/dual_loss/RUN_d1.json`) | `ls -ld /rs/rs_grp_oschome/go2432/data/fig6/bank_g3_v2` |
| `/rs/rs_grp_oschome/go2432/data/fig6/frozen_v1` | Ceph | the frozen snapshot: `strata.json` sha256 c7199d2d..., `split_final.json` sha256 65a57eb0..., `auto_reference.json` sha256 57782cad..., `auto_truth.csv` sha256 aa306deb..., `SHA256SUMS.json`; not sized on its own | Ceph-native; `sha256sum -c OK` on the grid checkout at release (`RELEASE_OPEN_GATE.json#frozen_reference`) | `ls -ld /rs/rs_grp_oschome/go2432/data/fig6/frozen_v1` |
| `/rs/rs_grp_oschome/go2432/data/fig6/eval_v2_g3` | Ceph | the open gate's outputs: `<head>/<set>/open/<variant>/proto/` prototype dumps for six heads (lam0 and lam1.0, seeds 0-2) over T1 renders, T2 COBRA, T3 C-ArmLSpine; re-scorable without a model re-run (`TODO.md` step 4); not sized on its own | Ceph-native; job 40438004 ran 2026-09-25 04:22-06:02 UTC, F6EVAL_END gate=open (`manuscripts/paper2_levelcheck/open_gate_40438004/README.md`) | `ls -ld /rs/rs_grp_oschome/go2432/data/fig6/eval_v2_g3` |
| `/rs/rs_grp_oschome/go2432/data/fig6/gatecheck_v2_g3_pre` | Ceph | leak-gate pre-check verdicts, job 40438053: total 108, pass 108, fail 0 (2026-09-24 21:55:45 UTC); not sized on its own | Ceph-native | `ls -ld /rs/rs_grp_oschome/go2432/data/fig6/gatecheck_v2_g3_pre` |
| `/rs/rs_grp_oschome/go2432/data/fig6/unblinding/RELEASE_v2.json` | Ceph | **does not exist.** Must be written by a person naming the committed G5 manifest (a6cc8a11e7303bbf4abb666b7c1760f3831a4dd5), a frozen human truth file with its sha256, `prespec_commit_is_ancestor` true and `released_by`; the blinded gate refuses to run without it (exit 6) | absent at release (`human_truth_file: none`; `results/paper2/fig6/HOLD_README.txt`) | `head -c 200 /rs/rs_grp_oschome/go2432/data/fig6/unblinding/RELEASE_v2.json` (expect: no such file — that answer is the check) |
| `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference` | Ceph | the automated reference runs: readers A / B / C on CTSP, VerSe, COBRA CT and CBCT, C-ArmLSpine, ts12 (9 subdirectories, 14 entries, 2026-09-24 23:34); the SPINEPS CBCT cpu patch; inside `or_ready` (867.951 GB, 340,064 files, CENSUS-CEPH), not sized on its own | Ceph-native; the laptop copy is `results/paper2/auto_reference/` | `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/auto_reference` |
| `/rs/rs_grp_oschome/go2432/data/or_ready/dual_loss` | Ceph | D1 heads, the learning-curve heads, coverage and self-test outputs (3 subdirectories, 27 entries, 2026-09-24 10:51); `d1_selftest_4042985{1}.out`, `40430077.out`, `40430433.out` at the `or_ready` root; inside `or_ready`, not sized on its own | Ceph-native; heads registered (21 aliases, section 6 below) | `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/dual_loss` |
| `/rs/rs_grp_oschome/go2432/data/or_ready/alphabet_loss` | Ceph | the alphabet-loss arm (12 entries, 2026-09-23 01:22): the 56.1-72.4 % L6 recall of `SchwingNet/results/ALPHABET_LOSS.md`, marked [SEL-SPLIT] and never quotable as held out (`CLAUDE.md` trap 5); inside `or_ready`, not sized on its own | Ceph-native; listed only | `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/alphabet_loss` |
| `/rs/rs_grp_oschome/go2432/data/or_ready/v9` | Ceph | 3 entries, 2026-09-23 00:39 (`v9_chain_jobs.txt` 55 B beside it); inside `or_ready`, not sized on its own | Ceph-native; listed only | `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/v9` |
| `/rs/rs_grp_oschome/go2432/data/or_ready/learning`, `learning_cpu`, `learning_lat`, `learning_lat_cpu` | Ceph | the Figure 2 analyses (jobs 40416675 GPU, 40416700 CPU; 9 / 10 / 7 / 0 entries, 2026-09-23 03:57-04:13); inside `or_ready`, not sized on their own | Ceph-native; CPU replicate cosine >= 0.999999 to the GPU run (`results/paper2/learning/LEARNING.md`) | `ls -ld /rs/rs_grp_oschome/go2432/data/or_ready/{learning,learning_cpu,learning_lat,learning_lat_cpu}` |
| `/rs/rs_grp_oschome/go2432/data/rare_class` | Ceph | the rare-class render banks (16 subdirectories, 17 entries, 2026-09-24 16:31): C-ArmLSpine CBCT renders, CTSP, TotalSegmentator, VerSe rare-anatomy renders with subtype truth; built by `tools/rare_class_maximize.py` and `SchwingNet/slurm/rare_max_{stage,verse,verify}.sh` (MAXIMIZE 2026-09-24 16:55); 5.797 GB census, 44,150 files | Ceph-native; listed only; reports in `results/paper2/rare_class/` | `ls -ld /rs/rs_grp_oschome/go2432/data/rare_class` |

## 4. The real-frame transitional sources (`MANIFEST_GRID.md` section 2; Ceph, under `data/`; shared with 01)

| path (as the manifest spells it) | volume | holds | state | check, from the Beethoven worker |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/data/cobra2026` | Ceph | COBRA2026: 692 public cases of 867, 375,618 projections, `cases/` 42.16 GB; the planning-CT screen (91 calls: L6 38, T13 45, four-lumbar 8; 57 field-supported); Elekta frames exported from 145 cases (3,480 frames); Varian 225 cases never exported; 808.615 GB census, 30,350 files | Ceph-native; per the `cobra2026` card of `data_platform/DATA_MANIFEST.md`; listed only on 2026-10-08 (11 subdirectories, 39 entries, 2026-09-23 13:32); terms in section 7 below | `ls -ld /rs/rs_grp_oschome/go2432/data/cobra2026` |
| `/rs/rs_grp_oschome/go2432/data/cobra2026/derived/rx_cobra_scratch` | Ceph | B10 target for HOME `/wsu/home/go/go24/go2432/rx_cobra_scratch` (directory, 2026-09-21 17:47, GRIDLS `ls HOME`); not sized | B10 not started on 2026-10-08; whether the target exists on 2026-10-11 is not recorded (B10 among the batches running on 2026-10-12, section 1) | `ls -ld /rs/rs_grp_oschome/go2432/data/cobra2026/derived/rx_cobra_scratch` ("No such file or directory" is an admissible answer while B10 has not landed) |
| `/rs/rs_grp_oschome/go2432/data/carmlspine` | Ceph | C-ArmLSpine (Zenodo 22768651): `C-ArmLSpine.zip` 15,581,614,253 B with `.ok` marker, `cases.csv` 11,266 B, `catalogue.json` 294,678 B, `compare_veridah{,2}.csv`, `headers_dossier.json` 1,863,754 B, `dossier_look/`; 86.834 GB census, 330,098 files | Ceph-native, stays; zip `.ok` marker; sha not read | `ls -ld /rs/rs_grp_oschome/go2432/data/carmlspine` |
| `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine` (+ `carmlspine_crops`, `_cv`, `_cv_prerepair`, `_cvday`, `_cvday_prerepair`, `_cvfill`, `_multi`, `_pre_repair_2026-09-23(_crops)`, `_sweep`) | Ceph | the real-frame banks: 149 cases, 299 spot frames after the 2026-09-23 repair; the three one-labeller L6 persons case42, case121, case136 (all G3 test); `cobra_elekta_v3`, `cobra_elekta_g3test` beside them; 3.408 GB, 67,732 files (CENSUS-CEPH row `/rs/rs_grp_oschome/go2432/data/realxray`); LAYOUT says 3.86 GB | Ceph-native (`realxray_layout`); listed only (dir dates 2026-09-21 to 09-24) | `ls -ld /rs/rs_grp_oschome/go2432/data/realxray/carmlspine; ls /rs/rs_grp_oschome/go2432/data/realxray` (the listing covers the variant banks without expanding the manifest's abbreviated spellings) |

## 5. HOME paths this project reads or produced (`MANIFEST_GRID.md` section 3; all still on HOME on 2026-10-08)

Everything in this table sits on HOME, which no student can read (section 1); each item a batch is moving is marked
**on HOME, not reachable until migrated**. Greg runs every check line in this table until the batches land. Where no
batch is named, none is recorded.

| path (as the manifest spells it) | volume | holds | state | check, from the Beethoven worker (Greg runs it) |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/split_final.json` | HOME | the frozen G3 person split (apply 2026-09-23 20:18:48, seed 0, job 40426793, leak audit PASS); frozen sha256 65a57eb0...; 8,065,646 B (GRIDLS, mtime 2026-09-23 20:18) | B11 (irreplaceable) -> `/rs/rs_grp_oschome/go2432/data/multisource_banks/meta/split_final.json`; B11 not started on 2026-10-08, `multisource_banks` absent on Ceph; B11 among the batches running on 2026-10-12 (section 1); on HOME, not reachable until migrated; **never redrawn in place** (section 7 below) | `head -c 200 /wsu/home/go/go24/go2432/split_final.json` |
| `/wsu/home/go/go24/go2432/patient_keys_final.json` (+ `.20260923_191858`, `.20260923_193933`) | HOME | the identity table the split reads; 5,913,937 B (+ 1,170,983 and 4,301,704 B; three files, 2026-09-23 18:29, 19:25 and 19:47) | B11; on HOME, not reachable until migrated | `head -c 200 /wsu/home/go/go24/go2432/patient_keys_final.json{,.20260923_191858,.20260923_193933}` |
| `/wsu/home/go/go24/go2432/physics_rare`, `physics_rare_film` | HOME | 1,482 rare-anatomy renders (34 CTSP and 47 VerSe series; T13 2 of 6 scans missing): the only labelled L6 and T13 at scale (`ann/`, `img/`; dirs 2026-09-14 17:48 and 2026-09-18 04:34); not sized | B11 -> `/rs/rs_grp_oschome/go2432/data/multisource_banks/derived/physics_rare{,_film}`, not started on 2026-10-08; on HOME, not reachable until migrated; **owner: project 08**, read here for the labelled L6 and T13 renders | `ls -ld /wsu/home/go/go24/go2432/{physics_rare,physics_rare_film}` |
| `/wsu/home/go/go24/go2432/lstv_flag` | HOME | the refuted 2-D flag line: `LEARNING_CURVE.md`, `LSTV_FLAG_RESULTS.md`, `ANOMALY_INVENTORY.md`, `_lstv_phenotypes.csv`, `models/` (`lstv_flag_v1/v2.pt`, `tltv_flag_v1/v2.pt`, `sex_control_v1.pt`), `curve/`, `buu_diag/`, `buu_scores{,_v2}_{AP,LA}.{csv,txt}`, `eval_*.txt`, `folds_*.csv`, `examples/`, `renders*`, `smoke/`; dir 2026-09-15 22:15; not sized | `renders`, `renders_verse`, `renders_ctrl` -> B11 `/rs/rs_grp_oschome/go2432/data/multisource_banks/derived/lstv_flag/{renders,renders_verse,renders_ctrl}`; `smoke` -> `.../derived/lstv_flag/smoke`, B11 candidate for deletion (`B11.tsv` lines 62-65); `models/` and results stay on HOME; on HOME, not reachable until migrated; AUC 0.577: REFUTED (RC C1.12); the learning-curve table is not on the laptop (OQ B15) | `ls -ld /wsu/home/go/go24/go2432/lstv_flag` |
| `/wsu/home/go/go24/go2432/lstv_flag_derive_verse.py` | HOME | a HOME-root script of the flag line (3,016 B, 2026-09-15) | not in any batch; on HOME, not reachable until migrated (no batch recorded) | `head -c 200 /wsu/home/go/go24/go2432/lstv_flag_derive_verse.py` |
| `/wsu/home/go/go24/go2432/model_night/anomaly_manifest` | HOME | `anomaly_manifest.csv`, `spine_classes.json`, `summary.json` (2026-09-17; 749 anomalous spines); not sized | HOME; on HOME, not reachable until migrated (no batch recorded) | `ls -ld /wsu/home/go/go24/go2432/model_night/anomaly_manifest` |
| `/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` | HOME | the v9 level bank (`rung_1.npz` 5,449,315,625 B; the SchwingNet encoder `runs/model_rung_1_aug2.pt` 44,824,746 B); holds BUU pixels (owner-only); the encoder that saw 49 of 54 G3 L6 val+test persons; 5.494 GB census, 4 files (`runs/` 0.045 GB) | B11 (restricted); on HOME, not reachable until migrated, and restricted after it: the BUU pixels are owner-only (section 7 below) | `ls -ld /wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` |
| `/wsu/home/go/go24/go2432/bench_ts` | HOME | SPINEPS + VERIDAH over 1,228 TS v2 + 374 VerSe CTs (labeller A inputs); 31 "relabelled" masks are links back to raw masks (`docs/handoff/RECIPES.md` section 3.5); 1.511 GB census, 4,815 files, 3,077 `.nii.gz` | B11; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/bench_ts` |
| `/wsu/home/go/go24/go2432/FluoroCap` | HOME | the literature fluoroscopy harvest (test set only, directive D1): `releases/FluoroCap_v0.1_{A,B}` (2026-09-13 22:35), `articles.jsonl`, `captions_*.jsonl`, `annotate/` (the 64 reading and 104 screening pages), `archives/`, `commons/`, `CORPUS_MANIFEST.{json,md}`, `LEVEL_COUNTS*.{json,md}`, `PROTOCOL.md`, `README.md`, `MORNING_REPORT.md`, `allspine_chain.log`, marker files; the weights `detect_v5z_final_best.pt` (42,233,939 B, same file as registry 797de71a9e0e42f7), `anchor_det_v1.pt` (registry 8df40e7f..., 40,489,317 B; 71.67 % on real film, below the 0.80 floor), `anchor_det_c2_v1.pt`; 34 subdirectories, dir 2026-09-20 21:07; 316.0 GB (LAYOUT line 291 and `B09.tsv` line 2: `youtube/` 181.0, `pdf/` 19.77, `panels/` 4.68, `raw/` 2.27 GB); no row in CENSUS-HOME | B09 -> `/rs/rs_grp_oschome/go2432/data/fluorocap/raw/FluoroCap`; copying on 2026-10-08 (one of three `dp_migrate` jobs, inferred by elimination); flagged irreplaceable; `/rs/rs_grp_oschome/go2432/data/fluorocap` had 1 entry, `raw`, on 2026-10-08 05:52 and no STATUS file yet (`MANIFEST_GRID.md` section 6); B09's state on 2026-10-11 is not recorded (B09 is not among the four batches section 1 names); on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/FluoroCap; ls -ld /rs/rs_grp_oschome/go2432/data/fluorocap/raw` |
| `/wsu/home/go/go24/go2432/fluorocap_drr`, `fluorocap_drr_smoke`, `fluorocap_fov96_ctx`, `fluorocap_pack` | HOME | FluoroCap render and crop banks (2026-09-18); not sized | B09 -> `/rs/rs_grp_oschome/go2432/data/fluorocap/derived/{fluorocap_drr,fluorocap_drr_smoke,fluorocap_fov96_ctx,fluorocap_pack}`; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/{fluorocap_drr,fluorocap_drr_smoke,fluorocap_fov96_ctx,fluorocap_pack}` |
| `/wsu/home/go/go24/go2432/fluorocap_patient_keys.json` | HOME | FluoroCap identity table (112,088 B, 2026-09-22) | B09 -> `/rs/rs_grp_oschome/go2432/data/fluorocap/meta/fluorocap_patient_keys.json` (irreplaceable); on HOME, not reachable until migrated | `head -c 200 /wsu/home/go/go24/go2432/fluorocap_patient_keys.json` |
| `/wsu/home/go/go24/go2432/REPORT.md`, `REPORT_interim.md` | HOME | the FluoroCap night reports of 2026-09-13 (20,227 B and 16,115 B) | not in any batch; not in a repository as far as recorded; on HOME, not reachable until migrated (no batch recorded) | `head -c 200 /wsu/home/go/go24/go2432/{REPORT.md,REPORT_interim.md}` |
| `/wsu/home/go/go24/go2432/.fluorocap` | HOME | harvester credentials | never read, never moved | `ls -ld /wsu/home/go/go24/go2432/.fluorocap` only — never `head` (header rule above) |
| `/wsu/home/go/go24/go2432/verify_fluorocap.{py,sh}` | HOME | FluoroCap verification scripts at the HOME root (2026-09-22); small | not in any batch; on HOME, not reachable until migrated (no batch recorded) | `head -c 200 /wsu/home/go/go24/go2432/verify_fluorocap.{py,sh}` |
| `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` | HOME | the grid checkout of the private repository, branch `L6_Class` at 4e3fe93862673e28613f7521d4c146c03a9dd405 on 2026-10-08; it can no longer fetch the repository (code ships by `git archive` over ssh, `SHIPPED_COMMITS.txt`); `SchwingNet/results/fig6/G5_MANIFEST.json` identical to the Ceph copy at release | stays; on HOME, not reachable by students; the repository itself is private (root `CLAUDE.md` rule 8) | `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-nnunet` |

## 6. Model registry aliases this project owns (`MANIFEST_GRID.md` section 4; on HOME)

The registry root is `/wsu/home/go/go24/go2432/model_registry` (GRIDLS "aliases"). It sits on HOME, so no student can
read it; no batch for it is recorded; Greg runs every check line here. Where the manifest abbreviates a store hash
("..."), the full store path is not recorded in this folder (GRIDLS holds it): the check is then
`ls /wsu/home/go/go24/go2432/model_registry` and a match of the printed prefix.

| alias | target (as the manifest spells it) | date | what | check (Greg runs it) |
|---|---|---|---|---|
| (the registry root) | `/wsu/home/go/go24/go2432/model_registry` | — | the content-addressed store and the alias records (`registry.jsonl`) | `ls -ld /wsu/home/go/go24/go2432/model_registry` |
| `bank_g3_v2_rung_1_g3clean_aug2` | `model_registry/629f0e058649ca1d/model_rung_1_g3clean_aug2.pt` | 2026-09-24 07:54 | the G3 clean encoder (ImageNet root only) | `head -c 200 /wsu/home/go/go24/go2432/model_registry/629f0e058649ca1d/model_rung_1_g3clean_aug2.pt` |
| `det_g3_primary_s0` | `model_registry/fe00a1732032e81a/best.pt` | 2026-09-24 16:47 | the section 15 primary detector (trained on the G3 TRAIN side of every device) | `head -c 200 /wsu/home/go/go24/go2432/model_registry/fe00a1732032e81a/best.pt` |
| `head_fig6_g3clean_lam0_seed{0,1,2}`, `head_fig6_g3clean_lam1.0_seed{0,1,2}` | `model_registry/{5e1e4c3b..., f83336ee..., 7d9533cc..., b150a58e..., 1f6daa7d..., a838629a...}` (hashes abbreviated by the manifest; full paths not recorded in this folder) | 2026-09-24 08:01-08:17 | the six open-gate heads | `ls /wsu/home/go/go24/go2432/model_registry` and match the six prefixes |
| `head_fig6_g3clean_dual_seed{0,1,2}` | `model_registry/{05ca6d6a..., 4207521f..., b2dedeca...}` (hashes abbreviated; full paths not recorded in this folder) | 2026-09-24 08:14-08:58 | D1 dual-loss heads | `ls /wsu/home/go/go24/go2432/model_registry` and match the three prefixes |
| `head_fig6_g3clean_dual_f{0.0625,0.125,0.25,0.5}_seed{0,1,2}` | twelve store entries (GRIDLS lines 2622-2633; not spelled in this folder) | 2026-09-24 10:41-10:46 | the learning-curve heads (A17) | `ls /wsu/home/go/go24/go2432/model_registry` (the twelve entries are named only in GRIDLS) |
| `lstv_flag_v1`, `lstv_flag_v2`, `tltv_flag_v1` (`tltv_flag_v2`, `sex_control_v1` registered, GRIDLS `registry.jsonl`) | `model_registry/5c14968b7081b2c3/lstv_flag_v1.pt` (44,785,396 B), `1c6c63ec3b3a59b0/lstv_flag_v2.pt`; the other targets are not spelled in this folder | 2026-09-15 21:01-22:16 | the refuted flag models (RC C1.12: AUC 0.577; do not rebuild) | `head -c 200 /wsu/home/go/go24/go2432/model_registry/{5c14968b7081b2c3/lstv_flag_v1.pt,1c6c63ec3b3a59b0/lstv_flag_v2.pt}` |
| `detector_v5z_final`, `anchor_detector_v1` | `797de71a9e0e42f7/detect_v5z_final_best.pt` (42,233,939 B), `8df40e7f.../anchor_det_v1.pt` (40,489,317 B; hash abbreviated, full path not recorded in this folder) | 2026-09-15 05:55 | the FluoroCap-era naming detector and render-trained anchor detector | `head -c 200 /wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt`; for `anchor_det_v1.pt`, `ls /wsu/home/go/go24/go2432/model_registry` and match the prefix |
| — | `/wsu/home/go/go24/go2432/model_night/heads_mixed/`, `/wsu/home/go/go24/go2432/model_night/ensemble/ensemble.json` | — | whether they exist is not known: GRIDLS lists `model_night` only as a `head` (`MANIFEST_GRID.md` section 4; `../_plan/PLAN.md` section 7) | `ls -ld /wsu/home/go/go24/go2432/model_night/heads_mixed /wsu/home/go/go24/go2432/model_night/ensemble/ensemble.json` (either answer is the news; record it) |

## 7. Terms, where the folder records them

- **COBRA2026** (`/rs/rs_grp_oschome/go2432/data/cobra2026`): CC BY-NC 4.0, and its 175 validation and test cases
  are embargoed to 2032-03-01, so "COBRA2026" on the grid means the 692-case public side of 867
  (`MANIFEST_GRID.md` section 2; issue #12).
- **FluoroCap** (`/wsu/home/go/go24/go2432/FluoroCap` and its derived banks): a test set at most, out of training by
  directive D1 (`MANIFEST_GRID.md` section 3; `CLAUDE.md`); the harvest never trains anything.
- **BUU**: `/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx` holds BUU pixels, owner-only, and no weight trained with
  BUU laterals leaves the grid until Greg has read the BUU licence (`MANIFEST_GRID.md` section 3; `TODO.md`
  section D).
- **The split trap.** `/wsu/home/go/go24/go2432/split_final.json` (on HOME) is never redrawn in place:
  `SchwingNet/slurm/g3_split.sh` re-globs today's annotation roots and rewrites it with `os.replace` and no backup,
  although the file's own `_about` says "never redraw" (`MANIFEST_GRID.md` section 3; `docs/handoff/RECIPES.md`
  section 10). To re-verify, copy the script with `--split-out` and `--out-dir` on a scratch Ceph path and diff
  `side_of_person` against the frozen file (`CLAUDE.md` trap 3).
- For every other path above, the terms are **not recorded in the folder**.

## 8. First experiment (`TODO.md` step 1): the one-hour COBRA coverage render

One `sbatch -D <dir>` job — nothing on the login node; submit, estimate the wall time, write the job ids and the ETA
to the resume file, stop (`TODO.md` header; `CLAUDE.md`, the grid rule):

- Project the Dataset803 sacrum and L5 labels of ten COBRA planning CTs in
  `/rs/rs_grp_oschome/go2432/data/cobra2026` through their RTK geometry onto their own Elekta projections and render
  the result (`TODO.md` step 1; `docs/handoff/RESEARCH_DIRECTIONS.md` section 2.7;
  `memory/lstv-tltv-detection-goal.md`).
- The Dataset803 weights come from Hugging Face `OpenSpineConsortium/spinopelvic-seg-checkpoints`
  (`docs/handoff/RECIPES.md` section 3.2). The download is itself a job, never the login node (root `CLAUDE.md`
  rule 7).
- The ten CTs must be among the 145 of 692 cases with exported Elekta frames (3,480 frames; section 4 above); which
  ten is not pre-specified in the folder.
- **Gate, by eye: the sacrum and L5 inside the field on the exported frames**, or COBRA is not spine data for the
  sacrum anchor (`TODO.md` step 1).
- Reference: the development detector found the sacrum on 21 of 609 COBRA frames (3.4 %), `power.md` after row 17,
  as `TODO.md` step 1 cites it.
- Depends on project 10 (the collections on Ceph: `data/cobra2026` 808.615 GB; the Elekta export 145 of 692 cases);
  who decides: engineering (`TODO.md` step 1).
- The python with nibabel and scipy is `~/mambaforge/envs/spineps/bin/python`; partition per the root rules
  (`reqp --qos=requeue` for CPU, `gmsap` / `gvohp` for GPU) — whether this render needs a GPU is not recorded.

## 9. Not recorded

The state of any grid path after 2026-10-08 beyond the access facts of 2026-10-11 (section 1); the outcome of
batches B05, B10, B11 and B13 said to run on 2026-10-12, and B09's state on 2026-10-11 (no STATUS for any of them is
in this folder); whether `/rs/rs_grp_oschome/go2432/data/cobra2026/derived/rx_cobra_scratch` exists yet (B10); the
sizes marked "not sized" above, and the sizes on 2026-10-08 of `/wsu/home/go/go24/go2432/FluoroCap`, `physics_rare`,
`physics_rare_film`, `lstv_flag`, `fluorocap_drr`, `fluorocap_drr_smoke`, `fluorocap_fov96_ctx`, `fluorocap_pack` and
`rx_cobra_scratch` (no `du` allowed on the login node; CENSUS-HOME and `_du_home.txt` carry no row for any of them;
the FluoroCap 316.0 GB is LAYOUT's earlier figure); the full store hashes of the six open-gate heads, the three dual
heads, the twelve learning-curve heads, `tltv_flag_v1/v2`, `sex_control_v1` and `anchor_det_v1` (the manifest
abbreviates them; GRIDLS holds them); whether `/wsu/home/go/go24/go2432/model_night/heads_mixed/` and
`ensemble/ensemble.json` exist; which ten COBRA planning CTs the first experiment uses; whether the 148 against 149
C-ArmLSpine cases are that many people (OQ E1); which held job carries the post-section-15 detector (OQ B11); the
terms of every path section 7 does not name.
