# HANDOFF extracts for 11_students_grid_access

Extracted 2026-10-08 from the eight student-readable HANDOFF files copied whole beside this file (spinesurg-ct-nnunet, branch L6_Class, commit 097933a working tree; `HANDOFF/` itself was untracked that day except `LITERATURE_STATE.md`, `literature_state/` and `RESEARCH_DIRECTIONS.md`). The map of which sections belong to this family is the "HANDOFF sections by family" table of the memory inventory: README 4, 8, 9, 10; INFRASTRUCTURE 2, 8, 11; GLOSSARY "Grid and operations"; OPEN_QUESTIONS A18, A21, A25, A29, A30, B34, E18, F10. The text below is verbatim from the copies (already redacted by kind); path prefixes (`ssn:`, `ctsp:`, `bth:`, `students:`) are defined in `README.md` section 0 of the same folder and are the source's own shorthand, not dependencies of this folder.

---

## From README.md

## 4. How to get on the grid

Use Beethoven; do not re-document it. Student guides (version 14.0.0, 2026-10-03): `bth:docs/guides/INSTALL.md`,
`USE.md`, `ACCOUNTS.md`, and the one-page `bth:release/14.0.0/guides/STUDENT_QUICKSTART.md` (its title still says 12.0.0).
A student needs a WSU grid account (sponsor Greg), Claude Pro or Max, Chrome, Google Authenticator for the grid code, and
GlobalProtect once; Greg approves the student, which adds a named ACL entry on `/rs/rs_grp_oschome` (`INFRASTRUCTURE.md`
§2; `bth:docs/guides/LAB_LEAD.md` §9). What a student account can and cannot run: `RECIPES.md` §0 item 9.

---

## 8. A student's first week

| day | do | done when |
|---|---|---|
| 1 | Read this README, `ctsp:CLAUDE.md`, `ssn:CLAUDE.md` (its login-node `pipeline_state.py` line is outdated: run it in a job), `students:RECIPE.md`. Request a WSU grid account and follow the Beethoven `INSTALL.md` and `USE.md`. Get repository access (§9). | you can open a worker on the grid |
| 2 | Read `ssn:data_platform/README.md` and `DATA_MANIFEST.md` §1, then `DATASET_USAGE.md` and `LEAKAGE.md` here. | you can say which bank trained the encoder and why VinDr is a problem |
| 3 | On the laptop (no grid; environment in §9): run the self-tests `python -m pytest tests/test_eval_gate.py -v`, `python tools/test_patient_keys.py`, `python tools/test_stats_compare.py`, `python tools/test_leak_check.py` in `ssn:`, and `python -m pytest` in `ostk:`. Re-derive the power numbers with `python HANDOFF/working_notes/t2_wilson_check.py` and compare with `RESULTS_CATALOG.md` part E. | the results match those of 2026-10-08 (§12): `test_eval_gate` 58 passed; `test_patient_keys` and `test_stats_compare` 0 failures; **`test_leak_check` fails on one known stale fixture** ("30 real names, 1 wrong": the Geneva phantom is now keyed as one person, `sn:results/eval_gate/EVAL_LEAKS.md` item 3; OQ-F17); **ostk 1 failed, 100 passed** (`tests/test_cobb.py::test_cobb_falls_back_gracefully_without_femurs`, OQ-F18); 35 / 22 persons reproduce. Any other failure is new: report it |
| 4 | Read `sn:results/eval_gate/EVAL_LEAKS.md`, `sn:results/coverage/PER_LEVEL_DOMAIN_ANGLE.md` and `RESULTS_CATALOG.md` parts A and D. Rebuild one figure from committed files in `ctsp:` without touching the committed copies: copy `morphometrics/level_atlas.csv` aside (the script always rewrites it, `paper/mpda/make_levelatlas_fig.py` L475), run `python paper/mpda/make_levelatlas_fig.py --out <scratch dir>`, then compare (`git diff --stat -- morphometrics/level_atlas.csv`; look at the new PNG beside `paper/mpda/figures/fig_levelatlas.png`) and put the copied CSV back. Its inputs `degenerative.csv` and `opportunistic.csv` were written before v11 (topic 6 flag F4). | the CSV shows no diff and the figure looks the same; commit nothing |
| 5 | With Greg, pick one item from `OPEN_QUESTIONS.md` or `students:BOARD.md`; write its `PREREG.md` (rule, success criterion, inputs) before running anything; submit nothing on the login node. | Greg has signed the PREREG |

Questions only Greg can answer (ask in week one): was SchwingNet uploaded; was the Medical Physics packet uploaded and
under what number; (the VinDr determination number was a question here until 2026-10-20: it is HPR 2026-330 of 29 September 2026); is the NeurIPS camera-ready deadline past; does Greg want the
ratio sweep, the per-level supplement table and seeds above N = 25 (`OPEN_QUESTIONS.md` part A); is the reader split of
this folder confirmed (A29). Greg's own questions are in `GREG_ONLY/PRIVATE_STATE.md` §3.

---

## 9. Getting access

**The repositories.** Clone each folder from its remote (`git remote -v`, 2026-10-08; `INFRASTRUCTURE.md` §1):

| laptop folder | clone from | branch | visibility | who grants access |
|---|---|---|---|---|
| `ssn:` | `github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` | `L6_Class` | private | Greg (how a student is added is not recorded) |
| `ctsp:` | `github.com/OpenSpineConsortium/CTSpinoPelvic1K` (also `Gregory-Schwing-MD-PhD/CTSpinoPelvic1K`) | `master` | public | — |
| `students:` | `github.com/OpenSpineConsortium/Student_Projects` (project work in the private `OpenSpineConsortium/Projects`) | `main` | public / private | Greg |
| `ostk:` | `github.com/OpenSpineConsortium/OpenSpineToolkit` (also `Gregory-Schwing-MD-PhD/OpenSpineToolkit`) | `main` | public | — |
| `bth:` | `github.com/OpenSpineConsortium/beethoven` | `main` | private | Greg; students install the extension from its private Chrome listing instead (`INFRASTRUCTURE.md` §2.2) |

**This folder is not in a clone yet.** On 2026-10-08 only `HANDOFF/LITERATURE_STATE.md`, `HANDOFF/literature_state/` and
`HANDOFF/RESEARCH_DIRECTIONS.md` are committed; every other file here is untracked (`git status`). Greg decides when to
commit it, and whether `GREG_ONLY/` is committed to the same repository at all (commit only when Greg asks).

**A laptop environment for the tests.** No environment file targets a laptop (`ssn:env/*.yml` are the grid's). The tests
of §8 day 3 ran on 2026-10-08 under Python 3.12.4 with numpy 2.5.3, scipy 1.18.1, pytest 9.0.3 and nibabel 5.4.2; ostk
declares numpy >= 1.24, scipy >= 1.10, nibabel >= 5 and, for its tests, pytest >= 7 (`ostk:pyproject.toml`). A student
needs Python 3.12 with those four packages; `HANDOFF/literature_state/power_calc.py` also needs scipy.

**Code to the grid.** The grid can no longer fetch the private repository; the route that worked for Greg is a
`git archive` of a committed tree piped over ssh (`RECIPES.md` §0 item 2). A student works in a grid checkout of the
public repositories; how a student gets private SchwingNet code onto the grid is not recorded (Greg decides).

---

## 10. People and roles

| who | role | source |
|---|---|---|
| Greg Schwing | resident physician (`MANUSCRIPTS.md` §20 C6), Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center (never Neurosurgery); owns grid account `go2432`; signs off on every freeze and submission | `context/user-affiliation-general-surgery.md`; `students:RECIPE.md` §0 |
| Ashley Schehr | a person (never a product name): senior scientist and co-PI; stage-1 screener of the transitional review; first author of the med-ed study; annotation lead | `students:RECIPE.md` §0; `MANUSCRIPTS.md` §0, §12; `RECIPES.md` §3.3 |
| "Dr Tech" | senior clinical PI; stage-2 confirmer of clinical reads; full name and e-mail recorded nowhere on disk | `students:RECIPE.md` §0; `OPEN_QUESTIONS.md` A18 |
| NeurIPS 3474 co-authors | Gregory John Schwing, Patrick Schwing (LSU Health Sciences Center New Orleans, School of Medicine), Miraziz Ismoilov, Nizar Alnabahneh, Loren Schwiebert | `ctsp:CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.txt` (via `MANUSCRIPTS.md` §7); `ctsp:` commit 38b0cb9 |
| MPDA authors | 14 authors on the title page (Loren Schwiebert not among them) | `MANUSCRIPTS.md` §20 C11 |
| Castellvi readers | two radiology residents, columns `read_1_NA` and `read_2_MI` of `ctsp:docs/castellvi_consensus.csv`; PGY year not recorded | `RESULTS_CATALOG.md` F.14; `OPEN_QUESTIONS.md` A27 |
| student annotators | 11 student usernames in the committed tally `ctsp:morphometrics/annotation_counts.csv` | `INFRASTRUCTURE.md` §11 |
| hpc@wayne.edu | grid accounts (sponsor Greg, about two business days) | `INFRASTRUCTURE.md` §2.1 |
| C&IT | owns group `oschome`; issued the grid etiquette of 2026-09-28 (no container commands on warrior, nothing under its `/tmp`); the contact person is not recorded | `ctsp:CLAUDE.md` "Grid"; `INFRASTRUCTURE.md` §2.2 |
| IRBQuestions@wayne.edu | where the VinDr-SpineXR HPR determination request goes | `OPEN_QUESTIONS.md` A5 |
| how to reach Greg | not recorded in any handoff file | — |

---


---

## From INFRASTRUCTURE.md

## 2. The grid

### 2.1 Accounts and sign-in

- Host `grid.wayne.edu`, login node `warrior`, Slurm; Greg's account `go2432`; HOME `/wsu/home/go/go24/go2432`
  (`context/grid-access.md`; `ctsp:CLAUDE.md` "Grid").
- A student needs a WSU grid account (request through the tech.wayne.edu knowledge base, sponsor Greg, about two business
  days; hpc@wayne.edu) (`context/student-onboarding-structure.md`; `bth:docs/guides/ACCOUNTS.md` §1, WSU KB 20199).
- Second factor: Google Authenticator TOTP enrolled once in Open OnDemand's **2FA Setup** app (needs the GlobalProtect VPN,
  `protect.wayne.edu`); running 2FA Setup again destroys the existing code; an ssh key skips password and code; ssh to
  `grid.wayne.edu:22` works off-VPN with password + code (`context/grid-ssh-second-factor.md`).
- Server facts (2026-10-01): OpenSSH 7.4, RSA host key only (SHA256:kLTz1xK6anQ1denM+31kDEryQtgan2P76r9aLno+K3s), aes-ctr
  ciphers, MAC hmac-sha1 only.
- From Windows: `ssh wsu-grid` (alias also `grid`) with `MACs +hmac-sha1` and `AddressFamily inet` (13 s -> 2 s per
  connection); key `~/.ssh/id_ed25519_wsu` on Windows and WSL; a compute node is `<node>.nas.grid.wayne.edu`
  (`context/windows-ssh-to-grid.md`). Greg's older WSL key is `~/.ssh/id_ed25519` (`context/grid-access.md`).
- Network from Windows goes through WSL: `wsl -e bash -lc '...'` for git push, ssh, rsync and Hugging Face (Windows
  sockets exhaust: the Phone Link handle leak) (`context/wsl-for-network.md`). Exception: `ctsp:paper/mpda/make_submission.py`
  shells out to `wsl` and must run from Windows.
- Local ITK-SNAP: `C:\Program Files\ITK-SNAP 4.4\bin\ITK-SNAP.exe -g CT -s LABEL -l DESCRIPTOR`, launched with PowerShell
  `Start-Process` (`context/grid-access.md`).

### 2.2 Beethoven: how students reach the grid (pointer; not re-documented)

Beethoven is the lab's Chrome extension plus the `hpcworker` framework; it starts a Claude Code worker as a Slurm job in
the student's own grid account and opens it in claude.ai through Claude Code Remote Control (`bth:CLAUDE.md`;
`bth:docs/guides/USE.md`). Guides for 14.0.0 (2026-10-03): `bth:docs/guides/INSTALL.md`, `USE.md`, `ACCOUNTS.md` (header
says 12.0.0), `LAB_LEAD.md` (header says 12.0.0; §11-12 cover 14.0.0) and the one-page
`bth:release/14.0.0/guides/STUDENT_QUICKSTART.md` (title still says 12.0.0; no copy under `docs/guides/`).

A student needs a WSU AccessID with a grid account, Claude Pro or Max (paid by the student), Chrome signed in to the
Google account the private-listing invitation went to, Google Authenticator, GlobalProtect once.

**The approved list.** Approval is given in the access service (`admin.mjs approve <id>` or `grant <id> extension`;
`admin.mjs roster` prints approved AccessIDs). On the grid "approved" means a named ACL entry `user:<AccessID>:rwx` on
`/rs/rs_grp_oschome` (`drwxrws--T`, `other::---`, sticky). Group `oschome` is NOT the list (C&IT owns it; it holds
go2432 and [C&IT staff AccessID]). Below the gate, `shared/` and `shared/beethoven` are other-readable; `shared/access` and `go2432/`
stay closed. `bth:tools/grid_access.sh` (from WSL, or the Windows scheduled task "Beethoven grid access") keeps the ACL list
equal to the roster about every fifteen minutes while Greg's PC is on. By hand: `setfacl -m u:<id>:rwx /rs/rs_grp_oschome/`,
remove with `setfacl -x u:<id>`. A student not yet on the list sees exit 126 "Permission denied" on
`.../shared/beethoven/hpcworker/current/bin/hpcworker` (`bth:docs/guides/LAB_LEAD.md` §8-9; `context/grid-access-list-gate.md`).

**When the panel hangs**, read `sacct -u <id> -S <today>`, the run's `status.json`, the gate's caps file and `last -F <id>`
before touching code: "the grid tells the truth and the panel may not". Known open items (memory note
`beethoven-2026-10-02-field-failures`, copied to `GREG_ONLY/context_beethoven/`): VPN-route Claude sign-in sittings die about 5 minutes after
the last keystroke (Open OnDemand idle sweep; a terminal `hpcworker claude login` works); `reqp --qos=requeue` preempts
workers (switching the Wayne profile to `secp/secondary` is Greg's call, `bth:framework/profiles/wayne.json` lines 8-11).

**Rules that bind Beethoven work**: never handle a Claude credential (the student signs in through Claude Code's own
flow) (`GREG_ONLY/context_beethoven/ashley-compliance-boundary.md`); every feature needs nodes in the diagnostics graph before it integrates
(`context/diagnostics-graph-required.md`); students see one path, no container or QoS options
(`context/students-see-no-internals.md`); destructive commands refuse under `CLAUDECODE` and removers touch only their own
run directories (`context/grid-ashley-deletion-2026-09-28.md`: `~/.ashley` was wiped during a phone session, cause
unproven); Ashley Schehr is a person, never rename her; nothing under the vendor folder `.beethoven-vendor` is read [the laptop path is struck in this extract; it stands in the whole copy of INFRASTRUCTURE.md beside this file].

### 2.3 Login-node rules

| rule | source |
|---|---|
| Never compute on warrior. Every analysis, render, smoke test, plot and download is an `sbatch` job, even a one-minute one. Compute nodes have internet (job 40409460 reached zenodo.org). Allowed: `sbatch`, `squeue`, `scancel`, reading logs, `ls`, `scp`, small `sed` edits, `~/remote_wait.sh` | `context/no-jobs-on-login-node.md` (Greg, 2026-09-21) |
| Warrior's login notice kills on sight by process name: python, python2, python3, node, pip, md5sum, rsync, conda, gcc, make, R and others | `context/grid-ssh-second-factor.md` (read 2026-10-01) |
| No container command on warrior, ever; nothing of ours under its `/tmp` (C&IT, 2026-09-28: a build left about 7 GB of `rootfs-*`). In jobs, `APPTAINER_TMPDIR` / `APPTAINER_CACHEDIR` (and the `SINGULARITY_*` twins) on the compute node's local `/tmp` or `$SLURM_TMPDIR` with a cleanup trap; shared temp under `/wsu/tmp` | `ctsp:CLAUDE.md` "Grid" |
| Before cancelling anything, record it (job id, state, elapsed, workdir, script, its header as the resume instruction) in `docs/grid_records/JOBS_RECORD_<date>.md` (example `ssn:docs/grid_records/JOBS_RECORD_2026-09-27_1544.md`) | `students:RECIPE.md` §5 rule 12 |
| Submit, estimate, write down, stop: never poll `squeue` in loops; write job ids + ETA + what to collect into the resume checkpoint; on "reactivate", one collect pass | `context/submit-and-sleep-orchestration.md` |

### 2.4 Partitions and QoS

| use | flags | source |
|---|---|---|
| CPU work | `--partition=reqp --qos=requeue` (273 scripts in `ssn:slurm/`); add `--no-requeue` unless re-entrant | `ssn:slurm/paired_sets_properties.sh`; `students:RECIPE.md` §5 rules 6, 10 |
| GPU work | `--partition=gmsap,gvohp,galhp --qos=gpu --gres=gpu:1` (GPU partitions accept only QoS `gpu`; 166 scripts; 9 ask for `gpu:nvidia_h200:1`) | `students:RECIPE.md` §5 rule 6 |
| GPU hardware | gmsap = 4 nodes x 4 H200 (`context/fluorogen-synthetic.md`); gvohp = Tesla (model not recorded); galhp = L40S (`ssn:env/README.md`); the Blackwell nodes ymh3 / ymh4 cannot run the SPINEPS environment | as cited; `ssn:docs/ruleclass/README.md` |
| long-running services | `--partition=secp --qos=secondary` (priority 200, 90-day MaxWall) starts at once when reqp sits pending | `context/grid-apptainer-module-works.md` |
| dependency chains | `--dependency=afterany` and the child checks a marker; `afterok` strands chains and is rejected if the parent already finished | `ctsp:CLAUDE.md`; `students:RECIPE.md` rule 3 |

### 2.5 Storage

| place | what | source |
|---|---|---|
| HOME `/wsu/home/go/go24/go2432` (Panasas) | 4.3 TB soft / 8.6 TB hard quota, read with `pan_quota`, not `df`; 4,050 GB of 4,295 GB on 2026-10-07; `du` is slow (2.5 M files): one `du -sx` per entry through `xargs -P 24`; code checkouts and environments stay here | `context/grid-quota-and-deleted-banks.md`; `ssn:data_platform/DATA_MANIFEST.md` §1; `LAYOUT.md` §3 |
| Ceph `/rs/rs_grp_oschome/go2432` (20 TB, group `oschome`) | `model_night/`, `data/` (the data platform's target layout), `ruleclass/`, `archive/`, `tmp/`; usage `df-ceph oschome`; use the `/rs/...` spelling, never `/.rs/volumes/...` | `context/grid-ceph-volume-oschome.md`; `LAYOUT.md` §4 |
| `/rs/rs_grp_oschome/shared/beethoven` | the lab's read-only shared Beethoven framework (`hpcworker/current`), image and Claude Code | `bth:docs/guides/LAB_LEAD.md` §9 |
| compute-node `/tmp` | node-local and swept (a cleaner deleted the IPC sockets of two 18-hour runs); IPC and per-job scratch under `/dev/shm/${USER}_<name>_${SLURM_JOB_ID}` with `trap 'rm -rf "$W"' EXIT` | `ctsp:CLAUDE.md`; `students:RECIPE.md` rule 4 |
| HOME banks and benches | `~/model_night`, `~/bench`, `~/ablate` (202-235 GB), `~/scaling` (129 GB), `~/*_fov96_ctx` crop banks, `~/*_drr` render banks, `~/data` (624 GB), `~/VerSeFusion` (195 GB); five superseded `allspine_v2..v5c` banks deleted 2026-09-20 (holdout references repointed to `allspine_v7_fov96_ctx`) | `context/grid-quota-and-deleted-banks.md` |
| CTSpinoPelvic1K on the grid | labels `~/data/CTSpinoPelvic1K/labels` (v11; `labels_v10/` beside), CT `.../ct`, `manifest.json` (802 rows); after batch B02 `~/data/CTSpinoPelvic1K` is a symlink to `$RS/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` | `ctsp:CLAUDE.md`; `LAYOUT.md` §4 |

### 2.6 Containers

| route | when | source |
|---|---|---|
| `$HOME/mambaforge/envs/nextflow/bin/singularity exec -B /rs/rs_grp_oschome/go2432 -B $HOME -B $W:/tmp <pre-unpacked sandbox>` | science jobs (every U251 R step used it); a SIF-to-sandbox conversion is what fails; `-B /rs` does not expose the tree; bind a writable `/tmp`; probe the runtime in step 0 | `context/grid-local-singularity-is-broken.md`; `students:RECIPE.md` rule 7 |
| `~/.local/bin/singularity` | broken ("starter not found"); compute nodes have no runtime on PATH (exit 127) | same |
| `module load apptainer/1.2.2` | builds an unprivileged sandbox from `docker://` on a compute node (6 min for node:22-bookworm) and execs it; Claude Code runs inside; used for Beethoven's worker image | `context/grid-apptainer-module-works.md` |
| Slurm inside a container | bind host `/usr/bin` as `/opt/host/bin`, `/usr/lib64/slurm`, libmunge, `/etc/slurm`, `/var/run/munge`, and a passwd / group carrying the slurm and munge users | `context/grid-slurm-inside-apptainer.md` |
| nnU-Net containers | training image `gregoryschwingmdphd/spinesurg-ct` (Docker Hub) -> `.sif`; fifteen nnU-Net scripts bind `${PROJECT_ROOT}/nnunet` | `ssn:docker/Dockerfile`; `ssn:containers/build_container.sh` (its header says run on warrior: now forbidden) |

---

## 8. The tools a student touches first

| tool | what it answers | how to run |
|---|---|---|
| `ssn:tools/pipeline_state.py` | done / running / ready / blocked / failed per stage, from disk + queue | in a job: `~/mambaforge/envs/spineps/bin/python ~/spinesurg-ct-nnunet/tools/pipeline_state.py` (writes `~/model_night/PIPELINE_STATE.md`) |
| `ssn:tools/ct_inventory.py` | every CT collection by distinct subject and its truth | `python tools/ct_inventory.py --out docs/CT_INVENTORY.md --json docs/CT_INVENTORY.json` |
| `ssn:tools/data_manifest.py` | per dataset root: source, licence, device, file counts, a content-list SHA-256; `check` exits 1 on drift | `build --out docs/RSNAI_DATA_MANIFEST.json`; `check --manifest ...` (after migration use `data_platform/plan/RSNAI_DATA_MANIFEST.remapped.json`) |
| `ssn:tools/patient_keys.py` | one key per person across naming schemes | `python tools/patient_keys.py --drr ~/ctsp_drr ... --d813 .../Dataset813_SpineSurgLSTVFullRibs --verse-manifest ... --out ~/patient_keys.json` |
| `ssn:tools/xray_dataset_usage.py` | per X-ray dataset: on disk / labelled / in a bank, with a reason for each gap | `python tools/xray_dataset_usage.py --out ~/model_night/XRAY_DATASET_USAGE.md` |
| `ssn:tools/holdout.py`, `ssn:tools/eval_gate.py` | what a model has seen; the per-person gate every evaluator calls | imported |
| `ssn:tools/claims_check.py` | every main_v2 number against its JSON source | `python tools/claims_check.py` |
| `ssn:tools/model_registry.py` | §5 | — |
| `ssn:tools/spineps_ids.py` | raises on raw SPINEPS instance ids | imported by 13 readers |
| `ssn:tools/disclosure_audit.py` | the public-surface audit | "run it before any submission, talk or release" |
| `ssn:data_platform/db/build_index.py` | the holding index | `sbatch -D "$PWD" build_index.sbatch` |

Self-tests worth running first (laptop): `tools/test_patient_keys.py`, `tools/test_stats_compare.py`, `tools/test_leak_check.py`,
`tools/test_device_gate.py`, `python -m pytest tests/test_eval_gate.py`, and `tools/diagnostics/make_fake_corpus.py` (a
planted leak must fail the chain) (`ssn:README.md` "Reproducing"). On 2026-10-08 `tools/test_leak_check.py` fails on one
stale Geneva fixture (`RECIPES.md` §10; `OPEN_QUESTIONS.md` F17) and ostk's `python -m pytest` has one failure,
`tests/test_cobb.py::test_cobb_falls_back_gracefully_without_femurs` (F18).

---

## 11. The lab recipe, the board and onboarding

- `students:RECIPE.md`: 12 sections + 2 appendices (roles; project shape with `PREREG.md` + `.sha256`, `DEVIATIONS.md`,
  `JOURNAL.md`, `numbers_manifest.json`, `\RESULT{key}`; data rules; refuse-early code and the `run_record()` block; the 14
  grid rules; Nextflow; results to manuscript; checking a number; Claude session checkpoints; handover and credit;
  checklists; SchwingNet as the worked example; what is not yet true). Living copy: Claude Doc "The Lab Recipe"
  https://claude.ai/code/artifact/03a25fb6-b679-4386-bb04-31f0a965e587 (private until Greg shares it).
- Roles above projects: Ashley Schehr (senior scientist, co-PI) screens; "Dr Tech" (senior clinical PI) confirms clinical
  reads; Greg signs off on every freeze and submission (`students:RECIPE.md` §0). Dr Tech's full name and e-mail are not on
  disk.
- Board: `students:board.json` -> `python tools/render_board.py` -> `BOARD.md`. Twelve cards: ctsp1k, schwingnet,
  transitional-review, u251, litt, meded (lead Ashley, co-lead Greg), annotation (co-lead Ashley), toolkit, polypose,
  website, demo-study, fluoro-reading; ten have no co-lead and render UNSTAFFED; every lead assignment is a draft for Greg.
- Onboarding: `curl -fsSL https://openspineconsortium.com/onboard.sh | bash` (or `irm .../onboard.ps1 | iex`) installs
  tools, clones Student_Projects and runs `claude "/onboard"` (resumable: SSH key, grid clone, `templates/make_env.sh` and
  `templates/get_dataset.sh` as Slurm jobs, a demo study, a project from `IDEAS.md`, `/new-project`); primer at
  openspineconsortium.com/onboarding. When the workflow changes, update root `CLAUDE.md`, `templates/CLAUDE.md`, `onboard.md`
  and the primer together (`context/student-onboarding-structure.md`).
- Annotators: the only record is `slots[].reviewer` in the private `anonymous-mlhc/CTSpinoPelvic1K-reviews-*` ledgers;
  committed tallies `ctsp:morphometrics/annotation_counts.csv` (11 student usernames + Greg; the memory note's "13" is not
  supported by a listed file); slots do not establish authorship (`context/annotator-roster.md`, per-person tally
  withheld; full copy in `GREG_ONLY/context/`).
- IRB umbrella for students: HPR 2026-269 covers a dataset only if public, de-identified, downloadable without an
  agreement, not restricted, with no re-identification key; anything else needs its own filing first (`students:RECIPE.md` §3).
- Student-facing CTSP review guides (point students here): `ctsp:docs/RIB_REVIEW_GUIDE.md`, `SPINE_REVIEW.md`,
  `CLASSFIX_REVIEW.md`, `REVIEW.md`, `STUDENT_ANNOTATION_PROTOCOL.md`, `LABELING_GUIDE.md`, `RIB_ANCHOR_REVIEW_GUIDE.md`,
  root `REVIEWERS*.md`. The review service: `ctsp:review_service/` (FastAPI as HF Docker Spaces; per-task Spaces from
  `deploy_v4_spaces.py`; **pointing a tool at the wrong ledger returns 0 cases with no error**; inspect with
  `python3 -m review_service.admin queue`) (`context/review-space-repos.md`).

---


---

## From GLOSSARY.md

## Grid and operations

| term | meaning | source |
|---|---|---|
| the grid, warrior | Wayne State's HPC cluster (`grid.wayne.edu`) and its login node, which runs nothing | `INFRASTRUCTURE.md` §2 |
| reqp / requeue | the preemptible CPU partition and its QoS (most CPU jobs) | same §2.4 |
| secp / secondary | a long-running partition and QoS (priority 200, 90-day MaxWall) | same |
| gmsap, gvohp, galhp, QoS `gpu` | GPU partitions (H200, Tesla, L40S) | same |
| HOME (Panasas), Ceph / oschome, `$RS` | the 4.3 TB home quota; the 20 TB lab volume `/rs/rs_grp_oschome/go2432` | same §2.5 |
| `model_night` | the folder of experiment roots and logs (`~/model_night/logs/` for job output) | same |
| `.pre-ceph`, FINALIZE, batch B00-B14 | the migration's kept originals, the step that deletes them after Greg looks, and the migration batches | same §4 |
| model registry | the content-addressed weights store `~/model_registry`; never `ln -sf` a model | same §5 |
| `pipeline_state.py` | the tool that computes what is done, running, ready or blocked | same §3 |
| JOBS_RECORD | the record written before cancelling jobs (`ssn:docs/grid_records/`) | same §2.3 |
| Beethoven, `hpcworker`, the sitting | the lab's browser extension and worker framework (was "Ashley Bridge"; Ashley Schehr is a person); a sitting is one Claude sign-in session inside a grid job, shown in the panel | `bth:docs/guides/USE.md`, `LAB_LEAD.md` |
| the approved list | named ACL entries on `/rs/rs_grp_oschome` | `context/grid-access-list-gate.md` |
| GlobalProtect, Open OnDemand | WSU's VPN client (`protect.wayne.edu`, needed once to enrol the grid's second factor) and the grid's web portal, where the 2FA Setup app runs | `INFRASTRUCTURE.md` §2.1 |
| HPR 2026-269 | the IRB "not human-participant research" determination covering public de-identified datasets (2 Sep 2026) | `MANUSCRIPTS.md` §19 |
| Part A, Part B | the two halves of the programme as the private records name them: the CT transitional classifier (A) and the single-exposure C-arm naming network (B); CT-side Part A material is public, Part B is private | `INFRASTRUCTURE.md` §1.1; `GREG_ONLY/PRIVATE_STATE.md` §3 |
| "Dr Tech" | the senior clinical reader named on the board; full name recorded nowhere on disk | `ctsp:Student_Projects/RECIPE.md` §0 |
| Claude Docs | living documents on claude.ai (data report, Lab Recipe) | `CONTEXT_EXPORT.md` §4 |
| workflow journals | background multi-agent runs' logs (`wf_<id>/journal.jsonl`) | same |

---

## From OPEN_QUESTIONS.md (the rows named for this family)

| # | question | why it matters | where to look first | from |
|---|---|---|---|---|
| A18 | Who is "Dr Tech" (full name, department, HF user)? | stage-2 reviewer of the transitional review | `ctsp:Student_Projects/BOARD.md`; RESUME L56, L69 | T2, T4, T5 |
| A21 | Drop the JEEHP med-ed manuscript (the study is published in Cureus) or turn it into a follow-up with new data? | duplicate publication | `MANUSCRIPTS.md` §12 | T4 |
| A25 | Push `ctsp:Student_Projects` commit 3f1cf04 (a public repo)? | "pushing a public repo is Greg's call" | `context/lab-recipe-and-board.md` | T5 |
| A29 | Confirm the reader split of this folder (`README.md` top; `GREG_ONLY/PRIVATE_STATE.md` §5); decide whether `HANDOFF/` is committed, and whether `GREG_ONLY/` goes into the same repository | the student-facing files must not state what `GREG_ONLY/` holds; until confirmed, nothing here goes to a student | `GREG_ONLY/PRIVATE_STATE.md` §5-6 | verification |
| A30 | Keep, redact or delete the personal and contact data withheld from the student copies (student usernames with counts; a WSU staff contact; three researchers' e-mail addresses) before any commit | personal data in a repository | `GREG_ONLY/PRIVATE_STATE.md` §4 | verification |

| # | fact | where to look | from |
|---|---|---|---|
| B34 | The current approved Beethoven roster | the access service (not the vendor folder, which is never read) | T5 |
| E18 | Whether `git` is tolerated on warrior | not on the quoted ban list; never tested | T5 |

| # | action | source | from |
|---|---|---|---|
| F8 | Fix ostk: port the lowest-lumbar footprint isolation for S1 on v11 and flag the fallback; fix the 1b7005c canal regression (test: case 0097 within 1 mm); update `SPEC.md` / `README.md` / `CLAUDE.md` | `RESULTS_CATALOG.md` G.2-G.3 | T5, T6 |
| F10 | Update stale entry documents a student reads first: `ctsp:README.md` (v5), `STATUS.md`, `docs/ROADMAP.md`, `paper/mpda/REPRODUCE.md` (§0, §2), `zenodo/README.md`, `zenodo/KNOWN_ISSUES.md` (v10; add mirrored CTs, 0533, COLONOG_299 L5), `ssn:README.md` (dataset link, "under audit"), `sn:README.md`, `sn:figures/FIGURES.md`, `ssn:docs/MODEL_REGISTRY.md` and `ssn:containers/build_container.sh` (login-node instructions); **`ssn:CLAUDE.md`**, which every Claude session in this repository loads: it runs `~/mambaforge/envs/spineps/bin/python .../pipeline_state.py` over ssh on the login node (python is killed there by name) and does not point at `HANDOFF/README.md`: give it the `sbatch` form and the pointer; check `ostk:CLAUDE.md` the same way (F8) | `working_notes/topic5`, `topic6` flags; verification 2026-10-08 | T5, T6 |
