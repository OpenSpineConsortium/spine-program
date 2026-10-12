# DATA.md: what a student can and cannot reach on the grid

This folder holds no imaging data and no dataset; it holds the access path itself (README.md; issue #5). The paths
below are every path of `MANIFEST_GRID.md` sections 1 to 4, spelled as the manifest spells them, each with its
volume, what it holds, who may read it, and one read-only check line. Run every check line from the Beethoven
worker (a compute-node job): nothing runs on the login node (`CLAUDE.md` "Standing rules"). The two volumes are
Ceph, `/rs/rs_grp_oschome` (20 TB, group `oschome`), and Greg's HOME, `/wsu/home/go/go24/go2432` (Panasas, 4.3 TB
soft quota) (`MANIFEST_GRID.md` header). Modes and sizes carry the manifest's dates (measured 2026-10-02, census
and listing 2026-10-08); the access facts of 2026-10-11 are Greg's, from issue #5. Like the rest of the folder,
this file is Greg-only until Greg confirms the reader split (`CLAUDE.md` "Reader"; OPEN_QUESTIONS A29, A30).

## 1. The lab's shared Beethoven tree (Ceph)

| path | volume | what it holds | who may read it | read-only check (from the Beethoven worker) |
|---|---|---|---|---|
| `/rs/rs_grp_oschome` | Ceph (the volume root; a link to the physical folder) | owned by go2432, `drwxrws--T`, `other::---`, sticky since 2026-10-02; entries `go2432/` (closed, `drwxr-s---` on 2026-10-02), `shared/`, and one folder per approved student named by AccessID | approved students only, each through a named ACL entry `user:<AccessID>:rwx` on this root; the approved list is those entries, not group `oschome` (`MANIFEST_GRID.md` section 1; `STATUS.md` section B) | `ls -ld /rs/rs_grp_oschome` |
| `/rs/rs_grp_oschome/shared` | Ceph | the lab's shared trees | other-readable (`o+rx` since 2026-10-02): any approved student (`MANIFEST_GRID.md` section 1) | `ls -ld /rs/rs_grp_oschome/shared` |
| `/rs/rs_grp_oschome/shared/beethoven` | Ceph | the lab's read-only shared Beethoven framework: `hpcworker/current` (a link to `v<N>/`; framework 14 published 2026-10-03), `containers/claude-node22` (the worker image), `npm-claude-node22/bin/claude`, the deploy log | other-readable (`chmod -R o+rX` plus default `o::r-x`, done 2026-10-02): any approved student, read-only (`MANIFEST_GRID.md` section 1) | `ls -ld /rs/rs_grp_oschome/shared/beethoven` |
| `/rs/rs_grp_oschome/shared/ashley` | Ceph | a link to `shared/beethoven`, kept for builds older than Beethoven 8.0.0 and Beethoven for VS Code 4.0.0 | the same readers as its target (`MANIFEST_GRID.md` section 1) | `ls -ld /rs/rs_grp_oschome/shared/ashley` |
| `/rs/rs_grp_oschome/shared/access` | Ceph | the access service's closed folder | closed (`o::---`); students never; excluded from every copy (`MANIFEST_GRID.md` section 1) | `ls -ld /rs/rs_grp_oschome/shared/access` (a student expects "Permission denied" on its contents; what `ls -ld` itself returns for a student is not recorded) |
| `/rs/rs_grp_oschome/<AccessID>/hpcworker` | Ceph | each approved student's own state (profile, consent marker, log, run directories `hpcworker_<id>` / `hpcw_<id>`), a folder the student creates; `wayne.json` writes the literal `/rs/rs_grp_oschome/$USER/hpcworker` as `shared_state_dir` | the student's own; Greg's is `/rs/rs_grp_oschome/go2432/hpcworker` (section 2 below) (`MANIFEST_GRID.md` section 1) | `ls -ld /rs/rs_grp_oschome/<AccessID>/hpcworker` (each student puts their own AccessID) |
| the three CephFS scaffold folders above the volume (`/.rs/volumes/...`) | Ceph (above the volume root) | world-writable without sticky, owned by root or another lab on 2026-10-02; framework 12 reports them as notes for C&IT | C&IT's to fix; no check line here: the `/rs/...` spelling is the one to use, never `/.rs/volumes/...` (`MANIFEST_GRID.md` section 1) | none |

## 2. Greg's Beethoven state on Ceph

All four sit under `/rs/rs_grp_oschome/go2432`, which the manifest records as closed (`drwxr-s---`, measured
2026-10-02; `MANIFEST_GRID.md` section 1). They are Greg's, not a student's. The student-readable subtree
`/rs/rs_grp_oschome/go2432/data/` of the 2026-10-11 access facts (below) is not a path of this manifest.

| path | volume | what it holds | who may read it | read-only check (from the Beethoven worker) |
|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/hpcworker` | Ceph | Greg's worker state: `worker/`, `wayne-worker/`, `workspaces/`, `probe/`, `bptest/`, `.gate`; 1.076 GB (census 40580051) | Greg (go2432) only | `ls -ld /rs/rs_grp_oschome/go2432/hpcworker` |
| `/rs/rs_grp_oschome/go2432/hpcworker-ci` | Ceph | Beethoven CI runs; 0.010 GB (census 40580051) | Greg only | `ls -ld /rs/rs_grp_oschome/go2432/hpcworker-ci` |
| `/rs/rs_grp_oschome/go2432/ashley` | Ceph | the VS Code edition's grid state: `containers/` (1.13 GB), `npm/`, `npm-cache/`, `cache/`, `tmp/`, `workspaces/`; 2.136 GB; old (the shared image replaced the per-user container) | Greg only | `ls -ld /rs/rs_grp_oschome/go2432/ashley` |
| `/rs/rs_grp_oschome/go2432/tmp` | Ceph | `hpcworker` temp folders of 2026-10-03; 30.278 GB, 117,813 files; keep or delete is Greg's (TODO step 23) | Greg only | `ls -ld /rs/rs_grp_oschome/go2432/tmp` |

## 3. Greg's Beethoven state in HOME

Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students (access facts of 2026-10-11,
issue #5). Each path below is therefore marked **on HOME, not reachable until migrated**; whether any one of them
moves in a data-platform batch is not recorded in this folder (the state of each batch is
`../10_data_platform_grid/MANIFEST_GRID.md` section 2), and the manifest's header records that none of its paths was a
batch item as of 2026-10-08 (`MANIFEST_GRID.md` header).
A student's check line on these paths tests the closure itself; the exact error a student sees is not recorded.

| path | volume | what it holds | who may read it | read-only check (from the Beethoven worker) |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/.beethoven` | HOME (Panasas) | the Beethoven client state; `/wsu/home/go/go24/go2432/.beethoven/claude` is Greg's Claude Code sign-in on the grid (`wayne.json`, `claude_config_dir`) | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/.beethoven` |
| `/wsu/home/go/go24/go2432/.ashley` | HOME | a link to `/wsu/home/go/go24/go2432/.beethoven` for builds older than 8.0.0 / VS Code 4.0.0 | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/.ashley` |
| `/wsu/home/go/go24/go2432/.hpcworker` | HOME | the launcher, the marker `shared` and the profile that `hpcworker install --shared` writes; no framework code | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/.hpcworker` |
| `/wsu/home/go/go24/go2432/hpcworker_src` | HOME | a development checkout (roles beyond the names not recorded) | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/hpcworker_src` |
| `/wsu/home/go/go24/go2432/ashley-bridge` | HOME | a development checkout (roles beyond the names not recorded) | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/ashley-bridge` |
| `/wsu/home/go/go24/go2432/ashley-test` | HOME | a test tree (roles beyond the names not recorded) | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/ashley-test` |
| `/wsu/home/go/go24/go2432/hpcworker-access-20261007-*` | HOME | the access reconciler's working folders, dated 2026-10-07 | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/hpcworker-access-20261007-*` |
| `/wsu/home/go/go24/go2432/hpcw_probe_97845` | HOME | one probe run | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/hpcw_probe_97845` |
| `/wsu/home/go/go24/go2432/.beethoven-vendor` | HOME | **named only, never read, never copied** (the vendor's signing keys and tokens); a credential store (`MANIFEST_GRID.md` section 3) | nobody reads it; on HOME, not reachable until migrated | none: this path is named only, never read (`MANIFEST_GRID.md` section 3) |

## 4. The review Space material in HOME

This project's by family; never copied. The same HOME closure and marker as section 3 apply.

| path | volume | what it holds | who may read it | read-only check (from the Beethoven worker) |
|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K-review` | HOME | review Space material of the single older Space (2026-05-26); may hold reviewer usernames: never copy | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/CTSpinoPelvic1K-review` |
| `/wsu/home/go/go24/go2432/ctspinopelvic1k-review-triaged` | HOME | the triaged Space's material (2026-06-01); may hold reviewer usernames: never copy | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/ctspinopelvic1k-review-triaged` |
| `/wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` | HOME | a backup of the April annotator app (2026-08-10); superseded (`review_service/`); role not recorded | Greg only; on HOME, not reachable until migrated | `ls -ld /wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` |

## Terms

None recorded in this folder: no dataset lives here (issue #5; README.md). Three boundaries stand in a dataset's
place. The vendor folder `/wsu/home/go/go24/go2432/.beethoven-vendor` is named only, never read or copied
(`MANIFEST_GRID.md` section 3). The review-Space material of section 4 may hold reviewer usernames and is never
copied (`MANIFEST_GRID.md` section 4). The roster lives in the access service, not in any file (`STATUS.md`
section B; `docs/handoff/OPEN_QUESTIONS.md` B34).

## Greg's access facts of 2026-10-11 (issue #5)

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students (named ACL entry on the
  volume root; other-read bits on folders and files), including `vindr_spinexr`, `buu_lspine_3600`,
  `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`, because every approved student holds
  the PhysioNet credential and the VinDr and BUU agreements.
- On 2026-10-12 the VinDr and BUU items inside those folders opened too. Until then the plan's `restricted` flag
  still closed them item by item, mode `drwx--S---` (`vindr/raw`, `buu_full`, `buu_v1`, BUU-LSPINE 2000, the VinDr
  and BUU banks of B10 and B11, `dis_renders`); the script was fixed (spinesurg-ct-nnunet d9b388d) and visibility
  jobs 40599886 (the B04, B05, B10 and B14 folders) and 40599867 (after B13's finalize, every chain folder including
  `multisource_banks`) open them (issue #65).
- Two paths stay closed (owner-only):
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private`, private build material
  and not a dataset, and `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11`, until Greg reads
  its Zenodo upload scripts for a token (issue #65;
  `../10_data_platform_grid/code/data_platform/plan/publish_visibility.sh`, from spinesurg-ct-nnunet d9b388d).
  Nothing on Greg's home directory `/wsu/home/go/go24/go2432` is readable by students; items still there are moved to
  the Ceph volume by the data-platform plan, whose batch-by-batch state is `../10_data_platform_grid/MANIFEST_GRID.md`
  section 2, and this file marks each such item "on HOME, not reachable until migrated" (sections 3 and 4 above).

The manifest's row of 2026-10-02 records `go2432/` itself as closed (`drwxr-s---`; `MANIFEST_GRID.md` section 1);
the mode that lets a student pass through `go2432/` to `data/` on 2026-10-11 is not recorded in this folder.

## Through Beethoven

The way in is Beethoven; do not re-document it. The student guides are `docs/beethoven/guides/INSTALL.md` and
`docs/beethoven/guides/USE.md` in this folder (version 14.0.0, 2026-10-03), published as pages at
https://openspineconsortium.com/beethoven/ (`docs/handoff/EXTRACTS_11.md` section 4). A student needs four things:
a WSU AccessID with a grid account, the Google Authenticator grid code, Claude Pro or Max, and Chrome on the
invited Google account. Approved means a named ACL entry `user:<AccessID>:rwx` on `/rs/rs_grp_oschome`
(`MANIFEST_GRID.md` section 1; `STATUS.md` section B). What approval opens, the two bullets above say again here:

- Every folder under `/rs/rs_grp_oschome/go2432/data/` is readable by approved students, including
  `vindr_spinexr`, `buu_lspine_3600`, `buu_lspine_v1_smoke`, `mendeley_5jdfdgp762` and `spine_detector_corpus`,
  because every approved student holds the PhysioNet credential and the VinDr and BUU agreements (2026-10-11,
  issue #5).
- Since 2026-10-12 the VinDr and BUU items inside those folders are open too (visibility jobs 40599886 and
  40599867, issue #65). Two paths stay closed,
  `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/build_archive_private` (private build material,
  not a dataset) and `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k_build_tree/derived/s1v11` (until Greg reads its
  Zenodo upload scripts for a token), and nothing on `/wsu/home/go/go24/go2432` is readable by students; what is still
  there is marked "on HOME, not reachable until migrated" (2026-10-11, issue #5; 2026-10-12, issue #65).

## First experiment: the first week

The first experiment is the first-week recipe of `docs/handoff/EXTRACTS_11.md` section 8, followed as written.

- **Day 1 is done when the student can open a worker on the grid** (the recipe's day-1 "done when"): read the
  handoff README, follow `INSTALL.md` and `USE.md`, request the grid account, get repository access.
- **Day 3 runs on the laptop only, no grid** (environment in `EXTRACTS_11.md` section 9): the four
  `spinesurg-ct-nnunet` self-tests (`python -m pytest tests/test_eval_gate.py -v`,
  `python tools/test_patient_keys.py`, `python tools/test_stats_compare.py`, `python tools/test_leak_check.py`)
  and `python -m pytest` in OpenSpineToolkit. The recorded expected results of 2026-10-08
  (`docs/handoff/EXTRACTS_11.md` section 8, day 3): `test_eval_gate` 58 passed; `test_patient_keys` and
  `test_stats_compare` 0 failures; `test_leak_check` fails on one known stale fixture ("30 real names, 1 wrong":
  the Geneva phantom is now keyed as one person); ostk 1 failed, 100 passed
  (`tests/test_cobb.py::test_cobb_falls_back_gracefully_without_femurs`). Any other failure is new: report it.
