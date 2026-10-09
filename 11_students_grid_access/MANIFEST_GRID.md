# MANIFEST_GRID.md: every grid path this project uses or produced

Host `grid.wayne.edu` (login node `warrior`, Slurm). HOME = `/wsu/home/go/go24/go2432` (Panasas, 4.3 TB soft quota;
4,050.75 GB used of 4,294.97 on 2026-10-08). Ceph = `/rs/rs_grp_oschome/go2432` (20 TB, group `oschome`; 7 TB used,
39.39 %, on 2026-10-08). Sizes are from the Ceph census job 40580051 and the read-only listing pass of 2026-10-08
22:20 UTC (the grid inventory's "GRIDLS", copied whole into `10_data_platform_grid`); "unsized" means no census row.
None of these paths is an item of the data-migration batches B00 to B14 (`10_data_platform_grid`), so "migration
state" below is "outside the batches" unless said otherwise; nothing here was finalised, cut over or deleted by the
migration. "Verified" means a job or a person checked the contents; a listing checks names only. Nothing was read
beyond names on 2026-10-08. A student's `~` is the student's own HOME, not this one (`docs/handoff/RECIPES.md`
section 0 item 9); for that reason every HOME path below is spelled in full, and `$USER` or `$HOME` appears only
where it is the literal text of `code/beethoven_framework_profiles/wayne.json`, said so in the row.

## 1. The lab's shared Beethoven tree (Ceph, outside Greg's folder)

| path | what it holds | size | state | verified | source |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome` (the volume root; a link to the physical folder) | owned by go2432, `drwxrws--T`, `other::---`, sticky since 2026-10-02; entries `go2432/` (closed, `drwxr-s---`), `shared/`, and one folder per approved student named by AccessID; the approved list = the `user:<AccessID>:rwx` ACL entries on this root | n/a | the gate; must keep `other::---` and sticky | modes measured 2026-10-02 by `getfacl` / `ls -ld` | `memory/grid-access-list-gate.md`; `docs/beethoven/guides/LAB_LEAD.md` section 9 |
| `/rs/rs_grp_oschome/shared` | `o+rx`; the lab's shared trees | unsized | other-readable since 2026-10-02 | listed 2026-10-08 | same |
| `/rs/rs_grp_oschome/shared/beethoven` | the lab's read-only shared Beethoven framework: `hpcworker/current` (a link to `v<N>/`; framework 14 published 2026-10-03; `deploy_shared.sh` keeps older versions, never deletes, and refuses to move `current` from version 11 or later back below 11), `containers/claude-node22` (the worker image, an Apptainer sandbox with Node 22 and Claude Code, shared with the VS Code edition), `npm-claude-node22/bin/claude`, the deploy log (0644); `chmod -R o+rX` plus default `o::r-x` done by hand 2026-10-02 (34,000 files, 23 s) | unsized | the only install mode at Wayne State since 5.0.0 ("Claude Code is the gas, the Beethoven code is the car"); published from the laptop with `tools/deploy_shared.sh` over ssh (on the login node only tar, chmod, setfacl and one link) | names listed 2026-10-08; version in `hpcworker/current/VERSION` not read today | `code/beethoven_framework_profiles/wayne.json` (`shared_install`, `image_store`, `claude_bin`); `docs/beethoven/repo_root/CLAUDE.md`; `docs/beethoven/V12_STATUS.md` section 8 |
| `/rs/rs_grp_oschome/shared/ashley` | a link to `shared/beethoven` kept for builds older than Beethoven 8.0.0 and Beethoven for VS Code 4.0.0 | link | keep until those builds retire | listed | `docs/beethoven/repo_root/CLAUDE.md` |
| `/rs/rs_grp_oschome/shared/access` | the access service's closed folder | small | stays closed (`o::---`); excluded from every copy | listed | the grid inventory row; `memory/grid-access-list-gate.md` |
| `/rs/rs_grp_oschome/<AccessID>/hpcworker` (`wayne.json` writes the literal `/rs/rs_grp_oschome/$USER/hpcworker` as `shared_state_dir`; `<AccessID>` is the student's own account, so no single full path exists; Greg's is `/rs/rs_grp_oschome/go2432/hpcworker`, section 2) | each approved student's own state (profile, consent marker, log, run directories `hpcworker_<id>` / `hpcw_<id>`), a folder the student creates; the framework's removers accept only these per-job directories | per student | belongs to the student | the one entry seen to work was set 2026-10-02 | `wayne.json` (`shared_state_dir`); `memory/grid-ashley-deletion-2026-09-28.md` |
| the three CephFS scaffold folders above the volume (`/.rs/volumes/...`) | world-writable without sticky, owned by root or another lab on 2026-10-02; framework 12 reports them as notes for C&IT; the `/rs/...` spelling is the one to use, never `/.rs/volumes/...` | n/a | C&IT's to fix (TODO step 13 item 3) | measured 2026-10-02 | `memory/ashley-bridge-project.md`; `memory/grid-ceph-volume-oschome.md` |

## 2. Greg's Beethoven state on Ceph

| path | what it holds | size | state | verified | source |
|---|---|---|---|---|---|
| `/rs/rs_grp_oschome/go2432/hpcworker` | Greg's worker state: `worker/`, `wayne-worker/`, `workspaces/`, `probe/`, `bptest/`, `.gate` | 1.076 GB | in use (worker 40580248 RUNNING on 2026-10-08) | census 40580051; names listed | the grid inventory section 3.8 |
| `/rs/rs_grp_oschome/go2432/hpcworker-ci` | Beethoven CI runs | 0.010 GB | in use | census | same |
| `/rs/rs_grp_oschome/go2432/ashley` | the VS Code edition's grid state: `containers/` (1.13 GB), `npm/`, `npm-cache/`, `cache/`, `tmp/`, `workspaces/` | 2.136 GB | old (the shared image replaced the per-user container) | census; names listed | same; the other-folders inventory section 2.8 |
| `/rs/rs_grp_oschome/go2432/tmp` | `hpcworker` temp folders of 2026-10-03 | 30.278 GB, 117,813 files | keep or delete is Greg's (TODO step 23); the grid inventory marks it exclude | census | the grid inventory TSV row |

## 3. Greg's Beethoven state in HOME

| path | what it holds | size | state | verified | source |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/.beethoven` | the Beethoven client state; `/wsu/home/go/go24/go2432/.beethoven/claude` is Greg's Claude Code sign-in on the grid (`wayne.json` writes it as the literal `$HOME/.beethoven/claude`, `claude_config_dir`; also the `CLAUDE_CONFIG_DIR` of the VS Code edition); the data manifest's symlink section lists `.ashley -> .beethoven` as the only link in HOME and no HOME entry that points at Ceph | unsized | in use; the Claude login inside it was lost once on 2026-09-28 at 22:34 local and had to be redone | listed | `wayne.json`; `memory/grid-ashley-deletion-2026-09-28.md`; the data manifest's symlink section |
| `/wsu/home/go/go24/go2432/.ashley` | a link to `/wsu/home/go/go24/go2432/.beethoven` for builds older than 8.0.0 / VS Code 4.0.0 | link | keep until those builds retire | listed | `docs/beethoven/repo_root/CLAUDE.md` |
| `/wsu/home/go/go24/go2432/.hpcworker` | the launcher, the marker `shared` and the profile that `hpcworker install --shared` writes; no framework code | small | in use | listed | `docs/beethoven/repo_root/CLAUDE.md` "Layout" |
| `/wsu/home/go/go24/go2432/hpcworker_src`, `/wsu/home/go/go24/go2432/ashley-bridge`, `/wsu/home/go/go24/go2432/ashley-test`, `/wsu/home/go/go24/go2432/hpcworker-access-20261007-*`, `/wsu/home/go/go24/go2432/hpcw_probe_97845` | development checkouts, a test tree, the access reconciler's working folders (dated 2026-10-07) and one probe run | unsized | development leftovers; roles beyond the names not recorded | listed only | the grid inventory section 3.8 |
| `/wsu/home/go/go24/go2432/.beethoven-vendor` | **never read, never copied, listed by name only** (the vendor's signing keys and tokens); the grid inventory of 2026-10-08 (`grid_manifest.tsv`) carries it as kind `other`, size small, state `exclude`, "GRIDLS lists it only" | n/a | a credential store | no (the name was listed; nothing was read) | the grid inventory row; `docs/handoff/README.md` section 5; the dataset repository's CLAUDE.md |

## 4. The review Space material in HOME (this project's by family; never copied)

| path | what it holds | size | state | verified | source |
|---|---|---|---|---|---|
| `/wsu/home/go/go24/go2432/CTSpinoPelvic1K-review` (2026-05-26) | review Space material of the single older Space | unsized | listed; may hold reviewer usernames: never copy | listed only | the grid inventory section 3 |
| `/wsu/home/go/go24/go2432/ctspinopelvic1k-review-triaged` (2026-06-01) | the triaged Space's material | unsized | same | listed only | same |
| `/wsu/home/go/go24/go2432/spinesurg-ct-annotator.backup` (2026-08-10) | a backup of the April annotator app | unsized | superseded (`review_service/`); role not recorded | listed only | same |

## 5. Jobs this project ran or runs

| job | what | when | state | source |
|---|---|---|---|---|
| 40496445 (asx15) | the proof that Remote Control registers from an `sbatch` job | 2026-09-29 02:22 UTC | done | `docs/beethoven/repo_root/CLAUDE.md` |
| 40487595, 40487596 (asx1) | the VS Code edition's workers `default` and `peer` | 2026-09-28 | done | `docs/beethoven_vscode/CHECKPOINT_2026-09-28.md` |
| 40501098, 40501100 (asx1) | probe jobs seen by the reviewers | 2026-09-29 09:56 UTC | done | `docs/beethoven/OPEN_QUESTIONS.md` row f |
| 40523644 | Greg's first worker as a student (6 min in the `reqp` queue) | 2026-10-01 | done | `memory/beethoven-first-run-ux.md` |
| 40523658 | the worker renewal that sat PENDING more than 12 h on `reqp` | 2026-10-02 | the preemption evidence | `memory/ashley-bridge-project.md` |
| 40552222, 40552237, 40552239, 40552241, 40552343, 40552346 | the four VPN-route sittings that died at about 4 min 20 s (exit 3) | 2026-10-02 | the sitting-death evidence | `memory/beethoven-2026-10-02-field-failures.md` |
| 40554211 | Greg's framework-13 worker whose resumed-session link was not parsed | 2026-10-03 07:50 to 08:00 EDT | the 14.0.0 fix's evidence | `docs/beethoven/release_14.0.0/README.md` |
| 40580248, 40581552, 40584406 | `hpcw_worker` RUNNING, its chained successor PENDING (Dependency), `hpcw_access` PENDING (BeginTime) | 2026-10-08 22:20 UTC | live | the read-only pass in `10_data_platform_grid` |

## 6. Grid facts a student's setup depends on (not paths)

- Partitions: `secp --qos=secondary` (priority 200, 90-day MaxWall) for interactive and test allocations and, by the
  open recommendation, for workers; `reqp --qos=requeue` (priority 100) for long batch work, which preempts;
  `gmsap` / `gvohp` for GPU (`wayne.json`; `docs/handoff/INFRASTRUCTURE.md` section 2.4).
- The login node is CentOS 7 with python3 3.6; `$TMPDIR` there points at CephFS, not the node; the 20-process
  login-node cap is Wayne State's published policy; the 60 s polling floor and the wall-time rule are the product's
  own etiquette (`wayne.json` notes; `docs/beethoven/repo_root/CLAUDE.md` "Grid etiquette").
- The portal `https://ondemand.grid.wayne.edu` (VPN only; HTTP Basic sign-in; its Shell app opens a login-node shell
  that is used for one `sbatch` and closed; the shell's inactivity timer is 300 s on real input).
- What is missing from the grid for this project: a second working student entry on the gate (only one ever seen);
  a `JOBS_RECORD` of the two failure tests; the roster (it lives in the access service, not on the grid). See
  `TODO.md` steps 26 and 27.
