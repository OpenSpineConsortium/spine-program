# 10_data_platform_grid: working context

**Reader.** Student-safe. Greg answered the reader split (`docs/handoff/OPEN_QUESTIONS.md` A29) on 2026-10-12:
every Write holder may read all 13 folders (issue #68); the contact data withheld under A30 stays out (root `CLAUDE.md`
rule 12). Credential names may appear here, never values.

## The goal in one paragraph

Keep one record of where every imaging source of the programme came from (211 cards in
`code/data_platform/DATA_MANIFEST.md`), where each sits on the grid (HOME `/wsu/home/go/go24/go2432` against Ceph
`/rs/rs_grp_oschome/go2432`), its migration and verification state batch by batch (B00 to B14,
`code/data_platform/MIGRATION_PLAN.md`), the identity and leakage rules every bank must pass
(`docs/handoff/LEAKAGE.md`, `docs/PATIENT_IDENTITY_SPEC.md`), the model registry (`docs/MODEL_REGISTRY.md`), the
environments (`code/env/`) and the grid operating rules; then finish batches B04 to B11, build the holding index,
FINALIZE batch by batch on Greg's word, and repair the records that contradict each other (the TCIA CT Colonography raw
DICOM and NIfTI trees, 1,057 GB, are on neither volume and nothing records their deletion: `docs/handoff/OPEN_QUESTIONS.md`
B30). This is support work, not a hypothesis. Every other project folder depends on it, and its first three steps
(`TODO.md` steps 1 to 3) run in week one.

## Where things are

- **This folder.** `README.md` (what and why, state on 2026-10-08), `STATUS.md` (results in hand with numbers and
  files), `TODO.md` (ordered steps with gates), `MANIFEST_GRID.md` (every grid path, size, migration state),
  `MANIFEST_CODE.md` (repositories, commits, the files that matter), `MANIFEST_LOCAL.md` (what was copied here and from
  where; what was not and why), `MEMORY.md` + `memory/` (the notes that bind this project, each with its status),
  `docs/handoff/` (the eight student-readable handoff files, whole; extracts of the Greg-only ones under
  `docs/handoff/extracts/`), `docs/grid_read_2026-10-08/` (the one read-only grid pass of 2026-10-08 22:20 UTC and the
  laptop copies of the census: no folder needs to re-run it), `code/data_platform/` (the platform itself, relative paths
  intact), `code/tools/` (accounting, leak, identity and SPINEPS-id tools with their tests), `code/spine_data_review/`
  (the PRISMA-ScR scoping review of public spine datasets), `results/spineps_ids/` (the SPINEPS instance-id census and
  repair).
- **The grid.** HOME `/wsu/home/go/go24/go2432` (Panasas; 4,050.75 GB of a 4,294.97 GB soft limit on 2026-10-08,
  `docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` "pan_quota") and Ceph `/rs/rs_grp_oschome/go2432` (7 of 20 TB,
  same file, "df-ceph"). The platform's own records on the grid:
  `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/data_platform/plan/runs/<B>/STATUS` (per-batch truth), `plan/logs/`,
  `dedup/hash_results/`, and the census at `/rs/rs_grp_oschome/go2432/data/inventory/census_2026-10-07/`. Every path
  is spelled in full in `MANIFEST_GRID.md`.
- **The repositories.** `spinesurg-ct-nnunet` (private, branch `L6_Class`, commit 097933a) holds `data_platform/`,
  `tools/`, `slurm/`, `docs/` and `HANDOFF/`; the grid checkout of it is at 4e3fe93
  (`docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` "grid checkout HEAD") and cannot fetch (`docs/handoff/RECIPES.md`
  section 0 item 2). The others, with URL and commit, are in `MANIFEST_CODE.md`. The copied
  handoff files use the prefixes `ssn:`, `sn:`, `ctsp:`, `ostk:`, `mem:` defined in `docs/handoff/README.md` section 0;
  read them as those repositories at the stated commits (`ssn:` = spinesurg-ct-nnunet 097933a, `sn:` = its
  `SchwingNet/`, `ctsp:` = CTSpinoPelvic1K 7ddfe38, `ostk:` = OpenSpineToolkit cb43197, `mem:` = `memory/` here), never
  as a folder on a laptop.

## The rules that bind all work here (restated in this folder's own words)

1. **Words.** Never use the French-derived word for where data came from; write origin, lineage, source, or "where it
   came from". No fractional version numbers: changes fold into the next integer version. Figure captions at most 60
   words, the argument in the text. Plain sentences. The affiliation is General Surgery (Wayne State University School of
   Medicine / Detroit Medical Center), never Neurosurgery. Ashley Schehr is a person, never a product name.
2. **Every number carries its file.** A count, a date, a path, a size or a claim names the file it came from; what no
   file records is written "not recorded". Say plainly what is not known.
3. **Check outside the computation.** The recurring failure in this programme is a number that is wrong but plausible.
   A verify pass that passes is not a check of the plan's sizes (the plan's 2026-09-01 sizes were stale by a month;
   the census of jobs 40578909, 40580051 and 40580052 is what decides). Compare against an independent listing, a
   published count, a second census, the spread not the median; render a mask before believing a label repair.
4. **Labels.** Two label schemes exist (v11 VerSe-native: L1 = 20, sacrum = 26, hips 30/31, femora 32/33; the legacy
   ostk map with L1 = 1 and femora 11/12) and mixing them does not raise: call `ostk.labels.labels_for(volume)`, never
   import a fixed map. Identifier 29 (the carved S1) is retired in release v11; code that gates on 29 goes with it.
   Zero-pad case ids with `zfill(4)`. Canonicalise to RAS to analyse; never reorient when writing a label.
5. **Held out means the person was never seen** by the checkpoint or any ancestor; a render inherits its CT's person;
   unknown is not clean. Every quoted score goes through `tools/eval_gate.py` of spinesurg-ct-nnunet. Never quote
   the leaked banks (allspine v2, v6, v7, v8 for VerSe, `anchor_drr`, `vindrps`). Identity comes from metadata first
   (DICOM, manifest, annotation fields) and the file name last (`memory/key-patients-from-metadata-not-filenames.md`).
6. **Pre-register, then score.** The rule and its success number are written before a run; numbers enter text through
   a manifest key, never typed.
7. **The grid.** Nothing runs on the login node (warrior kills python, rsync, node, pip, conda, md5sum by name; no
   container command there; nothing of ours under its `/tmp`). Every step is `sbatch -D <dir>`; chain with
   `afterany`, never `afterok`; IPC under `/dev/shm`; large outputs on Ceph; write job scripts for bash 4.2 (a quoted
   replacement in `${var/pat/"$new"}` keeps its quotes: `memory/grid-bash-4-2-quoting.md`); submit, estimate the wall
   time, record the job id, stop; never poll `squeue` in a loop. CPU work on `reqp --qos=requeue`; GPU on
   `gmsap`/`gvohp`/`galhp`. Never `ln -sf` a model; use `tools/model_registry.py link`.
8. **Private.** SchwingNet and all level-identification code, text, figures and weights stay private; so do the
   `spinesurg-ct-nnunet` and `XRSpinoPelvic1K` repositories. This folder holds none of the level-identification
   models; it names them only as registry entries.
9. **Data.** Use all of a public dataset; a download budget is not a criterion; every truncation is fixed or justified
   in writing before a rerun; a leak is fixed by retraining, never disclosed as a caveat; VinDr-SpineXR (DUA) and
   BUU-LSPINE (EULA) and every bank holding their pixels stay owner-only (`code/data_platform/plan/publish_visibility.sh`).
10. **Network and credentials.** On Greg's laptop, network goes through WSL (`wsl -e bash -lc '...'`). Tokens are read from files, never
    echoed, never on a command line or in `sbatch --export`; this folder names credential files (for example
    `/wsu/home/go/go24/go2432/github`, `/wsu/home/go/go24/go2432/CTSpinoPelvic1K/.token`) only so that Greg rotates and deletes them. In the code repositories
    this folder names, commit only when Greg asks; push CTSpinoPelvic1K to both `origin` and `osc`. In spine-program itself
    the account doing the work pushes only its claim branch `claude/<issue>` and Greg merges (root `CLAUDE.md` rule 10).

## Traps that bind this project

- **The migration as of 2026-10-12.** Every batch with data was copied, verified, cut over and finalized on 2026-10-11
  (B00, B01, B02, B04, B06, B07, B08, B09, B14; B03 had nothing to move; B12 was dropped; HOME went from 4,051 GB to
  1,902 GB: `MANIFEST_GRID.md` section 2, Greg's record in issue #49). B05, B10 and B11 were copied, verified, cut over
  and finalized on 2026-10-12; B13 is cut over and finalizing (Greg, issue #62). HOME's size after the 2026-10-12
  finalizes is not recorded. The `.pre-ceph` twins and the 4,050.75 GB of the 2026-10-08 listing are history. Only
  `cutover.sh` with `FINALIZE=1`, after Greg looks, frees quota (`MIGRATION_PLAN.md` section 3 step g); do not delete a
  `.pre-ceph` copy by hand.
- **"B01 cut over" means three metadata files.** The 721 GB raw DICOM and 336 GB NIfTI are ABSENT in
  `plan/runs/B01/STATUS` and `/rs/rs_grp_oschome/go2432/data/tcia_ct_colonography` holds `meta/` only; nothing records
  what removed them (`/wsu/home/go/go24/go2432/cleanup_v1v3_tcia.sh`, 1,136 B, 2026-09-01, is the likely script, unread). Re-acquisition route
  `tcia_ctsp_download` in `code/data_platform/reacquire/`.
- **The plan's sizes are stale in both directions.** 157 items unsized; some listed folders already deleted; the
  measured sizes in a STATUS file win (VerSeFusion/data is 194.2 GB measured, not 138.1 from the 2026-09-01 du).
  Regenerate with `plan/build_plan.py --census` from the census TSV before relying on a total.
- **The grid cannot fetch the private repository.** Ship committed trees with `git archive | ssh tar`; the grid
  checkout is at 4e3fe93 (`docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` "grid checkout HEAD"); `make physics*` hard-resets it and must not be used (`docs/handoff/RECIPES.md` section 0).
- **A rerun of a bank in place destroys it.** `slurm/allspine_v9_bank.sh` line 21 runs `rm -rf` on the bank it builds;
  back up `/wsu/home/go/go24/go2432/split_final.json`, `/wsu/home/go/go24/go2432/patient_keys*.json`, `/wsu/home/go/go24/go2432/bank_splits.json` to Ceph before B11 moves them.
- **The holdout trap.** An unreadable holdout bank once let evaluations run on training cases with no error;
  `tools/holdout.py` now raises; 57 references were repointed to `allspine_v7_fov96_ctx`
  (`memory/grid-quota-and-deleted-banks.md`). Check the holdout right after any bank cut-over.
- **SPINEPS masks harvested before commit 147428d carry raw instance ids 1..N**, not vertebra labels;
  `tools/spineps_ids.py` guards every consumer; VERIDAH output is not truth (`memory/spineps-ids-can-be-scrambled.md`).
- **The login-node instructions in old documents are wrong.** `docs/MODEL_REGISTRY.md` ("sync from the login node",
  "mlflow ui on the login node"), the repository's `CLAUDE.md`, `PIPELINE_RESUME.md` and `containers/build_container.sh`
  predate the ban; `docs/MODEL_REGISTRY_CORRECTION.md` gives the `sbatch` forms (`OPEN_QUESTIONS.md` F10).
- **Identity keys depend on path fragments.** `tools/patient_keys.py` lines 210 to 212 key on `"/vindr"`,
  `"lateral236"`, `"/raw/lateral_236/"`; after the Ceph move the old HOME paths resolve through symlinks, but a tool
  given the new `/rs/...` spelling may key differently. Test with `tools/test_patient_keys.py` after each cut-over.
- **Windows side.** Write scripts as files and run them by path (heredocs collapse backslashes); never name a scratch
  script after a standard-library module; `git worktree remove --force` deletes junction targets.

## How to be useful here

Read `README.md`, then `STATUS.md`, then `TODO.md` step 1. Before touching the grid, read
`docs/grid_read_2026-10-08/grid_ls_2026-10-08.out` for the state at 22:20 UTC on 2026-10-08, and then read the
`plan/runs/<B>/STATUS` files on the grid for anything later (`ls`, `cat` of small files and `squeue` through the login
node are the only reads allowed there). When a tidy explanation presents itself (for example "B01 is cut over, so the
TCIA trees are safe"), test it against a second listing before believing it.
