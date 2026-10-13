# DATA — reaching this project's grid data through Beethoven, and the first experiment

Written 2026-10-11 for issue #6. The paths and sizes below are `MANIFEST_GRID.md` sections 1 to 4,
spelled as the manifest spells them (its source is the read-only grid listing of 2026-10-08 and the
migration STATUS files). The access facts are Greg's, dated 2026-10-11, given in issue #6; where they
and an older recorded statement disagree, both are shown with their dates. What no file records is
written "not recorded".

Reader: this folder is student-safe after the redactions in `MANIFEST_LOCAL.md`; Greg answered the
reader split (`docs/handoff/OPEN_QUESTIONS.md` A29) on 2026-10-12: every Write holder may read all 13
folders (issue #68).

Conventions. HOME = `/wsu/home/go/go24/go2432` (Greg's home directory); Ceph = the volume under
`/rs/rs_grp_oschome/go2432`. Write full paths: in a student's shell `~` is the student's own HOME, and
`~/data/CTSpinoPelvic1K` is a symlink in Greg's HOME to the Ceph copy (`MANIFEST_GRID.md` header).
Every check line below is read-only (`ls`, `head`, `wc`, `stat`, `git rev-parse`) and runs **from the
Beethoven worker**, which is a batch job on a compute node
(`../11_students_grid_access/docs/beethoven/extension_README.md`) — never python, and never any of
these on the login node warrior, which kills python, rsync, node, md5sum and others by name
(`CLAUDE.md` rule 7; `docs/handoff/RECIPES.md` section 0 item 1).

## 1. The release and its build (Ceph) — `MANIFEST_GRID.md` section 1

- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` — Ceph;
  196,195,055,488 B, 2,417 files (B02 STATUS). The v11 working copy and **the only grid copy of the
  802 CTs and the v11 labels**: `ct/` (802), `labels/` (802, written 2026-09-16), `labels_v10/` (802),
  `labels.zip` 883,912,953 B, `manifest.json` 1,100,037 B, `splits_5fold.json` 247,222 B,
  `dataset_labels.json` 4,100 B, `dataset_labels_v10.json`, `KNOWN_ISSUES.md` 8,894 B, `README.md`
  20,159 B, `SHA256SUMS.txt` 73,633 B, `LICENSE`, `fetch_from_tcia.py`, `reconstruct_ct.py`.
  Check: `ls /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/labels | head -3`
  then `| wc -l` — 802 files `NNNN_label.nii.gz`;
  `head -c 300 /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K/README.md`
  returns the deposit README.
- `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K.pre-ceph` — HOME; 196 GB (census). The HOME original
  of the v11 working copy. FINALIZE deletes a `.pre-ceph` copy, and B02 was finalized on 2026-10-11
  (`../10_data_platform_grid/MANIFEST_GRID.md` section 2), so it is expected absent and the Ceph path
  above is the only copy. **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/data/CTSpinoPelvic1K.pre-ceph` — expected to
  answer "No such file or directory".
- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive` — Ceph; 13 files,
  6,236,530,062 B (B02 STATUS). Staging of the published build archive, Zenodo 10.5281/zenodo.22647933
  (tag `v10-build-archive`; `docs/ctsp/BUILD_CHAIN.md`); a deletion candidate in the migration plan but
  the only grid copy of the archive.
  Check: `ls /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive | wc -l` — 13.
- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_stage` — Ceph;
  2,474 files, 3,035,170,658 B (B02 STATUS). Build-archive staging tree; deletion candidate.
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_stage`
  — a readable directory (the 2,474 is the B02 STATUS recursive count).
- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` — Ceph;
  one file, 592 B. Owner-only (`LAYOUT.md` rule 8). **The one closed path** under
  `/rs/rs_grp_oschome/go2432/data/`: its one file is the annotator map, students' personal data rather
  than a dataset or a token (Greg, 2026-10-11, issue #6; issue #65; Greg, 2026-10-12, issue #69).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`
  — owner-only mode; a student's `ls` of its contents is refused, and that refusal is the expected result.
- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` — Ceph; 835 files,
  1,189,924,200 B (B14 STATUS). **The v11 build workspace with the Zenodo v11 upload state**;
  `out/v11_labels` is the release labels byte for byte (dedup A07: 802 identical, 1.19 GB). Owner-only
  (`drwx--S---`) when read on 2026-10-12 (issue #65); **readable by approved students since visibility
  job 40602925 of 2026-10-12**, opened without the token check (Greg, issue #69; spinesurg-ct-nnunet
  0ab783f drops it from `FIXED_RESTRICTED_PATHS`; `OPEN_QUESTIONS.md` A26).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` — a readable
  directory.
- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz` — Ceph;
  196,147,947 B (B14 STATUS). Pelvis-propagation QC renders of 2026-06-12; possibly the only copy
  (`MIGRATION_PLAN.md` section 8; the laptop twin was not copied). `~/qc.tar.gz` in Greg's HOME is a
  symlink to it.
  Check: `stat -c '%s' /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/qc_2026-06-12.tar.gz`
  — 196147947.
- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/` — Ceph;
  sizes per entry in `MANIFEST_GRID.md` (B14 STATUS). The 2026-09-10 spinopelvic and pedicle-width
  scratch (`pitest`, `pdwtest`, `ostk_level_morphometry.csv`, `pi_ostk2.csv`, `pdw_why.py`); owned by
  project 05; the pedicle-width question is `OPEN_QUESTIONS.md` D2.
  Check: `ls /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/scratch_2026-09-10/` —
  those five entries.
- `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/0816_label_v4.nii.gz` — Ceph;
  1,106,588 B (B02). A superseded build intermediate of case 0816 (the 0816 scripts are in
  `code/case_fixes/_review_0816/`).
  Check: `stat -c '%s' /rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/0816_label_v4.nii.gz`
  — 1106588.
- `/rs/rs_grp_oschome/go2432/data/ctsp0533_repair` — Ceph; 0.604 GB (census). The CT 0533 rebuild work
  tree including `0533_ct.TRUNCATED.20e673dc6c2a.nii.gz`; repaired 2026-09-23 (job 40416624) and the
  Hugging Face file replaced (job 40419665); `KNOWN_ISSUES.md` still lacks it (`STATUS.md` F.19).
  Check: `ls /rs/rs_grp_oschome/go2432/data/ctsp0533_repair | head -5` — includes the TRUNCATED file.
- `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/meta` — Ceph; 12.3 MB (B01). `patient_db.json`
  9,909,285 B, `patient_db.pkl` 2,409,446 B, `patient_db_summary.txt` 663 B (May 2026): **the only TCIA
  material left on either volume**; the raw DICOM (721 GB) and `tcia_nifti` (336 GB) were found on
  neither HOME nor Ceph, and nothing records what removed them (`OPEN_QUESTIONS.md` B30).
  Check: `ls /rs/rs_grp_oschome/go2432/data/tcia_ct_colonography/meta` — those three files.
- `/rs/rs_grp_oschome/go2432/data/ctsp_april` — Ceph; 86.883 GB (census). The April 2026 release
  inputs (1,153 records) used for the NeurIPS SPINEPS appendix; no byte copy of a release CT
  (dedup A10). **World-writable (`drwxrwxrwx`) — a flag for Greg** (`MANIFEST_GRID.md` section 1;
  `DATA_MANIFEST.md` family A hazard 5).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/data/ctsp_april` — the mode prints `drwxrwxrwx`.

## 2. The NeurIPS appendix chains (Ceph), cancelled 2026-09-27 — `MANIFEST_GRID.md` section 2

These three sit under `/rs/rs_grp_oschome/go2432/` directly, not under `data/`; Greg's 2026-10-11
readable-to-students fact covers only folders under `/rs/rs_grp_oschome/go2432/data/`, so whether a
student can read these is not recorded.

- `/rs/rs_grp_oschome/go2432/neurips_v11` — Ceph; 10.174 GB (census). The v11 summaries chain for
  Appendix J; cancelled 2026-09-27 15:50; `nv11_ts` had 6 of 16 shards done and resumes per shard
  (`OPEN_QUESTIONS.md` A7; `TODO.md` step 2).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/neurips_v11` — the directory exists.
- `/rs/rs_grp_oschome/go2432/neurips_tsv3` — Ceph; 2.250 GB (census). The TotalSegmentator v3 chain
  (jobs 40481824-26), cancelled; `total_v3` itself was never run (`CAMERA_READY_CHANGES.md` item 20).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/neurips_tsv3` — the directory exists.
- `/rs/rs_grp_oschome/go2432/neurips_spineps` — Ceph; 36 files (census). The SPINEPS-on-April chain
  for Appendix I, cancelled (`CAMERA_READY_CHANGES.md` item 19).
  Check: `ls -ld /rs/rs_grp_oschome/go2432/neurips_spineps` — the directory exists.

## 3. nnU-Net datasets, results and the benchmark (HOME) — `MANIFEST_GRID.md` section 3

Every path in this section is on Greg's HOME: **on HOME, not reachable until migrated** (the
2026-10-11 facts below). A check line here runs for Greg, or after migration; a student's `ls` of any
of them is refused today.

- `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/raw` — HOME; not sized. The nnU-Net raw
  datasets `Dataset802_SpineSurgCTFull`, `Dataset803_SpineSurgCTFullMerged`,
  `Dataset804_SpineSurgCTFusedOnly`, `Dataset810_SpineSurgLSTVOneShot`, `Dataset813_SpineSurgLSTVFullRibs`,
  `Dataset815_SpineSurgLSTVVerSe` (links + `labelsTr`). The manifest records it **stays on HOME**
  (B12 dropped); no running batch is recorded to move it. The `imagesTr` links are container paths:
  never repair them on the host (`memory/dataset813-image-links-are-container-paths.md`).
  Check (Greg only): `ls /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/raw` — the six Dataset folders.
- `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/results` — HOME; 348.6 GB (`du` 2026-09-20).
  Results for Dataset802, Dataset810, Dataset813; no Dataset815 results (never trained); whether the
  Dataset813 folds finished and were scored is not shown by the listing (`OPEN_QUESTIONS.md` C19).
  B13 optional in the manifest. **On HOME, not reachable until migrated.**
  Check (Greg only): `ls /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/nnunet/results` — the Dataset802,
  Dataset810, Dataset813 trees.
- `/wsu/home/go/go24/go2432/ablate` — HOME; 201.563 GB (census; 202-235 GB in other records). The
  nnU-Net ablation arms `v5_all`, `v5_minus_all`, `v5_minus_extras`, `v5_minus_obl`, `v5_minus_pseudo`;
  outcome never read or recorded (`OPEN_QUESTIONS.md` B16; `STATUS.md` C5.1). B13 optional.
  **On HOME, not reachable until migrated.**
  Check (Greg only): `ls /wsu/home/go/go24/go2432/ablate` — the five arm folders.
- `/wsu/home/go/go24/go2432/bench` — HOME; 35.845 GB (census). The benchmark harness of
  `code/benchmark/` (CT-10): `ct_by_case` (802 links), `gt`, `spineps`, `totalsegmentator`, `vista3d`,
  `robust`, `xr_fov`, `fov`, `patch_context*`, `latency.json`, `runtime_cost_workstation.json`,
  `fig_runtime_workstation.pdf`, `model_registry.csv`; the C-arm files in the same folder belong to
  project 01. B13 optional. **On HOME, not reachable until migrated.**
  Check (Greg only): `ls /wsu/home/go/go24/go2432/bench | head` — the entries above.
- `/wsu/home/go/go24/go2432/spinopelvic-seg` — HOME; 27 GB (`du`, `MIGRATION_PLAN.md` section 10).
  The Dataset803 pseudolabeller checkout (`nnunet/raw` inspect-only in B14); no `results/` tree on the
  grid; its five checkpoints are on Hugging Face `OpenSpineConsortium/spinopelvic-seg-checkpoints`
  (`docs/handoff/RECIPES.md` section 3.2). Which batch moves it is not recorded.
  **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/spinopelvic-seg` — the directory exists.
- `/wsu/home/go/go24/go2432/NV-Segment-CTMR` — HOME; not sized. The VISTA3D-lineage competitor
  checkout (2026-09-08); environment built, smoke test pending (`docs/handoff/RECIPES.md` section 8).
  Which batch moves it is not recorded. **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld /wsu/home/go/go24/go2432/NV-Segment-CTMR` — the directory exists.

## 4. Repository checkouts and review material (HOME) — `MANIFEST_GRID.md` section 4

- `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` — HOME; 7.699 GB (census). The public repository
  checkout, `master` at a0c51390970f57011fdd05123745bd2d79944c91, behind the laptop's 7ddfe38;
  `morphometrics/` (26 CSV/PNG), `data/` remnants, `docs/`, `configs/`, `hardware_review/`,
  `gallery_*`, `fov_check/`. The manifest records it stays on HOME. Flags: `.token` (38 B, 2026-05-20)
  is a credential file inside the checkout, never copy; a stray directory literally named `"\` with a
  file `md5sum \` is a heredoc-backslash leftover; whether `data/v5_final` and `data/zenodo_deposit`
  still exist here is not recorded (`OPEN_QUESTIONS.md` B28). **On HOME, not reachable until migrated.**
  Check (Greg only): `git -C /wsu/home/go/go24/go2432/CTSpinoPelvic1K rev-parse HEAD` —
  a0c51390970f57011fdd05123745bd2d79944c91.
- `/wsu/home/go/go24/go2432/CTSpinoPelvic1K-review` (2026-05-26),
  `/wsu/home/go/go24/go2432/ctspinopelvic1k-review-triaged` (2026-06-01),
  `/wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` (2026-08-10) — HOME; not sized. Review
  Space material and ledgers; may hold reviewer usernames: **never copy** into this folder.
  **On HOME, not reachable until migrated.**
  Check (Greg only): `ls -ld` each of the three paths — the directories exist.

## Terms

- The release is **CC BY-NC-SA 4.0** on Zenodo, v11 = 10.5281/zenodo.22797014, published 2026-09-18;
  concept DOI 10.5281/zenodo.22139642; build archive 10.5281/zenodo.22647933 (`STATUS.md` "data" row;
  `manuscripts/mpda/cover_letter.md`, `title_page.tex`). Whether the concept DOI resolves to v11 or to
  v10 today is open (`docs/handoff/OPEN_QUESTIONS.md` E7).
- The Hugging Face mirror `OpenSpineConsortium/CTSpinoPelvic1K` **still serves v10 with id 29** (checked
  by API 2026-09-27) and **its card says CC BY-NC 4.0** while Zenodo says CC BY-NC-SA 4.0
  (`memory/hf-mirror-is-v10.md`; `README.md` "Where the data is";
  `manuscripts/neurips_camera_ready/CAMERA_READY_CHANGES.md` item 22).
- `/rs/rs_grp_oschome/go2432/data/ctsp_april` is **world-writable** (`drwxrwxrwx`) — a flag for Greg
  (`MANIFEST_GRID.md` section 1; `DATA_MANIFEST.md` family A hazard 5).
- **`s1v11` is open**: owner-only (`drwx--S---`) when read on 2026-10-12 (issue #65), it was opened to
  approved students the same day without the token check, by Greg's decision (visibility job 40602925,
  issue #69; `OPEN_QUESTIONS.md` A26).
- Any other terms question is **not recorded in the folder**.

## Access — Greg's facts of 2026-10-11 (issue #6)

- **Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students** (a named
  ACL entry on the volume root; other-read bits on folders and files), **including** `vindr_spinexr`,
  `buu_lspine_3600`, `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because
  every approved student holds the PhysioNet credential and the VinDr and BUU agreements.
- **On 2026-10-12 the VinDr and BUU items inside those folders opened too.** Until then the plan's
  `restricted` flag still closed them item by item, mode `drwx--S---` (`vindr/raw`, `buu_full`,
  `buu_v1`, BUU-LSPINE 2000, the VinDr and BUU banks of B10 and B11, `dis_renders`); the script was
  fixed (spinesurg-ct-nnunet d9b388d) and visibility jobs 40599886 (the B04, B05, B10 and B14 folders)
  and 40599867 (after B13's finalize, every chain folder including `multisource_banks`) open them
  (issue #65).
- **One path stays closed (owner-only):**
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, whose
  one file is the annotator map, students' personal data rather than a dataset or a token (Greg,
  issue #69). `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` opened on
  2026-10-12 without the token check (spinesurg-ct-nnunet 0ab783f; visibility job 40602925,
  issue #69).
  **Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students**; items still
  there are moved to the Ceph volume by the data-platform plan, whose batch-by-batch state is
  `../10_data_platform_grid/MANIFEST_GRID.md` section 2, and each such item above is marked "on HOME,
  not reachable until migrated".

These facts are newer than the folder's records and supersede two of them where they disagree:
`docs/handoff/RECIPES.md` section 0 item 9 ("`go2432/` below the Ceph gate stays closed to students",
written 2026-10-08) and project 10's `STATUS.md` M.11 (B05, B10, B11 not started, B13 not run, as of
2026-10-08).

## Through Beethoven

A student reaches the paths above from the Beethoven worker. The guides are
`../11_students_grid_access/docs/beethoven/guides/INSTALL.md` and
`../11_students_grid_access/docs/beethoven/guides/USE.md`; the published pages are at
https://openspineconsortium.com/beethoven/ (issue #6; the request page
`https://openspineconsortium.com/beethoven/request.html` per
`../11_students_grid_access/MANIFEST_CODE.md`).

A student needs: a WSU AccessID with a grid account, the Google Authenticator grid code, a Claude Pro
or Max subscription, and Chrome on the invited Google account
(`../11_students_grid_access/README.md`; issue #6). **Approved** means a named ACL entry
`user:<AccessID>:rwx` on `/rs/rs_grp_oschome` (issue #6).

The two access facts, repeated: every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by an
approved student (the named ACL entry on the volume root; other-read bits on folders and files),
including the VinDr and BUU folders, because every approved student holds the PhysioNet credential and
the VinDr and BUU agreements, and since 2026-10-12 the VinDr and BUU items inside them and
`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`; one path stays closed,
`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (the
annotator map, students' personal data); and nothing on `/wsu/home/go/go24/go2432` is readable by students until the
data-platform batches move it to Ceph.

## First experiment: the two release gates on the v11 labels

The first grid experiment of this folder is `docs/handoff/RECIPES.md` section 9 item 2: the two
release gates, run on `labels/` and `ct/` under
`/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K`. They exist because on
2026-08-20 PI came back 154.6 degrees and SS 82.9 for all 802 records and the run exited zero
(`ctsp:docs/RELEASE_CHECKLIST.md`, quoted in RECIPES.md section 9 item 2): the gates stop the chain.

**Code.** The scripts are `scripts/check_release_invariants.py` and
`scripts/qc_rib_vertebra_incidence.py` in the `CTSpinoPelvic1K` repository at master **7ddfe38**
(`MANIFEST_CODE.md`: `origin` = github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K, `osc` =
github.com/OpenSpineConsortium/CTSpinoPelvic1K). The grid checkout
`/wsu/home/go/go24/go2432/CTSpinoPelvic1K` is at a0c5139, behind 7ddfe38, and is on HOME (section 4
above): bring 7ddfe38 to a readable place first (a student clones the public repository into their own
space from the worker; whether a compute node reaches github.com is not recorded — the recorded fetch
failure of 2026-10-08 concerned the private `spinesurg-ct-nnunet` remote, `docs/handoff/RECIPES.md`
section 0 item 2).

**Before submitting.** The batch wrappers `slurm/*.sh` in that repository still point at
`data/v5_final` and use `-q primary`: edit them off both before reuse (`docs/handoff/RECIPES.md`
section 9 item 3; `CLAUDE.md` rule 7). Set
`D=/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K`
(`MANIFEST_GRID.md` section 1).

**Submission.** Each gate is an `sbatch -D <dir>` job on `--partition=reqp --qos=requeue` (a relative
`#SBATCH --output` resolves against the submit directory and the log folder must exist); chain with
`--dependency=afterany:<id>`, never `afterok`; scratch under `/dev/shm/${USER}_<name>_${SLURM_JOB_ID}`
with a cleanup trap; write each job id with a timestamp into the project's `JOBS.txt`; submit,
estimate the wall time, record the ids and the ETA, stop (`docs/handoff/RECIPES.md` section 0 items
3-4; `CLAUDE.md` rule 7). The recorded python is `~/mambaforge/envs/spineps/bin/python` with
`PYTHONNOUSERSITE=1` — in Greg's HOME (`docs/handoff/RECIPES.md` section 0 item 5), which the
2026-10-11 facts leave unreadable to students; a student's environment is
`../11_students_grid_access/STUDENT_ENV.md` (issue #66).
The gates' own wall time is not recorded (the label-only extractors of the same chain run 15-30
minutes at 20 workers, RECIPES.md section 9 item 3).

**Gate 1 — release invariants.**
`python scripts/check_release_invariants.py --labels $D/labels --ct $D/ct --workers N --out qc_invariants.csv`
— pass means **802 / 802** (`docs/handoff/RECIPES.md` section 9 item 2).

**Gate 2 — rib-vertebra incidence.**
`python scripts/qc_rib_vertebra_incidence.py --labels $D/labels --workers N --out <dir>`
— pass means reproducing `STATUS.md` F.9: **11,560 ribs, 5,796 skipped (own vertebra outside the
field), 11 no contact, 5,753 evaluable, 5,751 match, 2 offset (0.035 %), 0 misnumbered cases**
(`results/ctsp_results/rib_qc_v4_vs_release/incidence_release.json`).
