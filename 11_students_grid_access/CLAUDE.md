# 11_students_grid_access: working context

Students on the grid: Beethoven, onboarding, the lab recipe and the medical-education record. Rank 11 of 12 in
`spine-program` (a support project, not a hypothesis). Reader: Greg-only until Greg confirms the redacted Beethoven
notes may stay (PLAN section 5); student-safe afterwards for the guides, the recipe and the tutorials, never for the
compliance, licensing and roster material.

## The goal in one paragraph

Keep the path by which a medical student reaches the Wayne State grid and produces work under the lab recipe
working. The path is Beethoven (a Chrome extension plus the `hpcworker` framework that starts the student's own
Claude Code worker as a Slurm job in the student's own grid account and opens it in claude.ai through Remote
Control; release 14.0.0 of 2026-10-03, `OpenSpineConsortium/beethoven` main 2f90319; the VS Code edition and the
access service, `OpenSpineConsortium/beethoven-vscode` main 8d7fc65), the one-line onboarding and
`Student_Projects` (RECIPE.md, the board, the templates; local commit 3f1cf04, not on the remote), the review Spaces
and annotator tooling, the access-list gate on `/rs/rs_grp_oschome` (named-user ACL entries, not group membership),
and the medical-education study, published in Cureus on 2026-07-14 (DOI 10.7759/cureus.112661; a JEEHP version on
disk would duplicate it). Beethoven worked in the field on 2026-10-02 with two failures still open: VPN-route
sign-in sittings die about five minutes after the student's last keystroke, and `reqp --qos=requeue` preempts
workers. No finding is expected from this project; its product is students producing work under the recipe.

## Read first

1. `README.md` (state on 2026-10-08, success criteria, how this folder relates to the others), then `STATUS.md`
   and `TODO.md`.
2. `docs/handoff/EXTRACTS_11.md`: the sections of the 2026-10-08 handoff that bind this project (how to get on the
   grid, a student's first week, getting access, people and roles, the grid, the tools a student touches first, the
   lab recipe and the board). The eight whole handoff files are beside it.
3. `docs/beethoven/repo_root/CLAUDE.md` (the product's own working context, 22 KB, with its non-negotiable rules),
   `docs/beethoven/guides/LAB_LEAD.md` (sections 8 to 12: the gate, the shared copy, 14.0.0), then
   `docs/beethoven/V12_STATUS.md` ("Decisions for Greg", section 7, and the three dated entries after section 8:
   2026-10-02 evening, 2026-10-03 morning, 2026-10-03 later).
4. `code/student_projects_3f1cf04/RECIPE.md` (the lab method; 12 sections and 2 appendices) and `MEMORY.md`.

## Where things are

- **This folder.** `docs/beethoven/` and `docs/beethoven_vscode/` hold the two repositories' documents at their
  commits (redacted by kind); `code/student_projects_3f1cf04/` holds the recipe, templates and commands of the
  unpushed commit; `code/beethoven_framework_profiles/wayne.json` is the Wayne State site profile (the partition lever
  for the preemption failure is its `partition_cpu_batch` / `qos_batch` pair); `manuscripts/` holds the Cureus article
  and the CNS poster decks; `docs/outreach/` the two redacted outreach drafts; `docs/survey_protocol.md` the PACS-demo
  usability survey protocol (not the med-ed survey: see `STATUS.md`); `regulatory/openresearch/` the seven prompts
  that specified the product; `memory/` 39 notes with statuses (`MEMORY.md`).
- **The grid** (`MANIFEST_GRID.md`). HOME `/wsu/home/go/go24/go2432`; Ceph `/rs/rs_grp_oschome/go2432`. The lab's
  shared Beethoven copy is `/rs/rs_grp_oschome/shared/beethoven/hpcworker/current` (a link to `v<N>/`; framework 14
  published 2026-10-03), the worker image `/rs/rs_grp_oschome/shared/beethoven/containers/claude-node22`, a student's
  state `/rs/rs_grp_oschome/$USER/hpcworker`, a student's Claude sign-in `$HOME/.beethoven/claude` (both are the
  literal values `shared_state_dir` and `claude_config_dir` in `wayne.json`; for Greg they resolve to
  `/rs/rs_grp_oschome/go2432/hpcworker` and `/wsu/home/go/go24/go2432/.beethoven/claude`). The volume root
  behind `/rs/rs_grp_oschome` is `drwxrws--T`, `other::---`, and a student reaches anything under it only through a
  `user:<AccessID>:rwx` entry on that root.
- **The repositories** (`MANIFEST_CODE.md`): the two Beethoven repositories (private; pushed with `tools/push_org.sh`
  from WSL; whether 2f90319 and 8d7fc65 are on GitHub is not recorded), `OpenSpineConsortium/Student_Projects`
  (public; origin/main fd60c58, local main 3f1cf04 ahead by one), `OpenSpineConsortium/CTSpinoPelvic1K` 7ddfe38
  (`review_service/`, `reviewtool/`, the review guides), `Gregory-Schwing-MD-PhD/spinesurg-ct-annotator` 1083c4f
  (superseded), `OpenSpineConsortium/openspineconsortium.github.io` (tutorials, `onboard.sh`, `onboard.ps1`, the
  Beethoven pages; the local clone was ten commits behind on 2026-10-08), `spinesurg-ct-nnunet` 097933a (the handoff),
  `OpenSpineToolkit` cb43197 and `XRSpinoPelvic1K` 4f22935 (referenced only).

## Standing rules, in this folder's words

- Never use the French-derived word for where data came from; write origin, lineage, source, or "where it came
  from". Version numbers are integers (13.0.0, 14.0.0), never fractional. Figure captions at most 60 words; the
  argument goes in the text. Plain sentences.
- Every number, date, path and claim names the file it came from; what no file records is written "not recorded".
- Check outside the computation. The recurring failure of this programme is a number that is wrong but plausible, and
  here the same failure wears a different coat: a panel state that is wrong but plausible. "In line for a computer",
  "Connecting to Claude..." and "the grid didn't accept the code" each appeared on 2026-10-02 with nothing wrong on
  the grid. Read `sacct -u <id> -S <today>`, the run's `status.json`, the gate's caps file and `last -F <id>` before
  touching code: the grid tells the truth and the panel may not (`memory/beethoven-2026-10-02-field-failures.md`).
- Two label schemes exist and mixing them does not raise: call `ostk.labels.labels_for(volume)`, never a fixed map.
  Identifier 29 (the carved S1) is retired in v11 and code that gates on it goes with it; the student template
  `templates/CLAUDE.md` still lists S1 = 29 under v10 and must be brought to v11 when the public mirror ships v11.
  Case ids are `zfill(4)`. Canonicalise to RAS to analyse; never reorient when writing a label.
- Held out means the person was never seen by the checkpoint or any ancestor; every quoted score goes through the
  evaluation gate of the private repository; the leaked banks are never quoted. Pre-register, then score; a number
  enters a manuscript only through a manifest key. This project quotes no model score at all.
- Nothing runs on the login node (warrior). Every analysis, render, smoke test and download is an `sbatch` job, even
  a one-minute one; warrior kills python, node, pip, rsync, conda, md5sum and others by name. `sbatch -D <dir>`;
  chain with `afterany` and let the child check a marker; IPC and small scratch under `/dev/shm`; large outputs on
  Ceph, never HOME; the grid's bash is 4.2.46, so write jobs for bash 4.2 and test them there. No container command on
  warrior and nothing of ours under its `/tmp` (C&IT, 2026-09-28). `$TMPDIR` on Wayne State points at CephFS, not
  the node: never trust it blindly (`code/beethoven_framework_profiles/wayne.json`, `tmpdir_is_node_local: false`).
- SchwingNet and every piece of level-identification code, text, figure and weight stays private. Nothing in this
  folder is SchwingNet, and nothing from the private repository beyond its handoff files is copied here. Students
  work in grid checkouts of the public repositories; how a student gets private code onto the grid is not recorded.
- Use all of a public dataset; fix or justify every truncation.
- Network goes through WSL (`wsl -e bash -lc '...'`) for git push, ssh and rsync; tokens are read from files only
  and never echoed, never on a command line, never in a job file. Commit only when Greg asks, directly to `main` or
  `master` as each repository does it.
- Ashley Schehr is a person (senior scientist and co-PI, first author of the medical-education study, annotation
  lead, the first tester); she is never renamed and never a product name. The product is Beethoven. Student names
  and usernames, researcher e-mail addresses and Greg's personal e-mail appear nowhere in this folder's text;
  placeholders in brackets mark where they were struck. Three deliberate exceptions, recorded in `MANIFEST_LOCAL.md`
  sections 2 and 3 and reserved to Greg (PLAN section 5): the published Cureus article in `manuscripts/` carries its
  author list and the corresponding author's university address as printed; the two accepted CNS poster decks in
  `manuscripts/talks/` name their 16 contributors on the slide; the JEEHP draft's corresponding address was struck
  and the three Office files' core properties (creator, last modified by) were emptied.
- The affiliation is the Department of General Surgery, Wayne State University School of Medicine / Detroit Medical
  Center, never Neurosurgery. One outreach draft said "neurosurgery resident"; the copy here says surgical resident,
  General Surgery, and `MANIFEST_LOCAL.md` records the edit.

## Traps that bind this project

- **Beethoven never reads, stores, copies, prints or relays a Claude credential.** The student signs in with
  `claude auth login` on a compute node; the framework only starts Claude Code where that credential already is and
  reads `claude auth status`; `claude auth logout` is never run. Any feature that would read, cache, relay or refresh
  a Claude credential, run work on a student's account for the vendor's benefit, or run a process on the login node
  is out (`memory/ashley-compliance-boundary.md`; `docs/beethoven/repo_root/CLAUDE.md`).
- **The approved list is the named-user ACL on the volume root, not group `oschome`.** The group is C&IT's and had
  two members on 2026-10-02; `tools/grid_access.sh` in the Beethoven repository keeps the ACL equal to the access
  service's roster (`admin.mjs roster`) about every fifteen minutes while Greg's PC is on. By hand:
  `setfacl -m u:<id>:rwx /rs/rs_grp_oschome`, remove with `setfacl -x u:<id>`. A student not on the list sees
  exit 126 "Permission denied" on `.../shared/beethoven/hpcworker/current/bin/hpcworker`. The roster itself lives
  only in the access service (OPEN_QUESTIONS B34); nothing here names its members.
- **Nothing is deleted outside the framework's own run directories.** On 2026-09-28 at 22:34 local the whole
  `~/.ashley` folder on the grid (the Claude login inside it) vanished while a phone Remote Control session was open;
  the cause is unproven. Destructive subcommands refuse when `CLAUDECODE`, `BEETHOVEN_REQUEST_ID` or a similar agent
  marker is set, or when stdin is not a terminal (`memory/grid-ashley-deletion-2026-09-28.md`).
- **Every Beethoven feature needs nodes in the diagnostics graph before it integrates** (id, depends_on, assumption,
  check, failure signatures, auto_repair, manual_fix, future_risk), because Wayne State and the vendors change under
  the students (`memory/diagnostics-graph-required.md`). **Students see one path and no internals**: no container,
  runtime or QoS options in anything a student reads (`memory/students-see-no-internals.md`).
- **The public name is Beethoven; the old names survive only as links and wire values.** `~/.ashley -> ~/.beethoven`,
  `shared/ashley -> shared/beethoven`, the kill-list tag `ASHLEYREV1` (the verifier also accepts `BEETHOVENREV1`),
  the wire value `product: "bridge"`, the Worker name `ashley-service` beside `beethoven-access`. Keep the links until
  builds older than Beethoven 8.0.0 and Beethoven for VS Code 4.0.0 retire. Do not run Ashley for VS Code 3.0.0's
  "Install on the grid" or "repair" on the grid again (it writes old scripts through the links).
- **No licence keys in the browser edition since 4.0.0** (Greg, 2026-09-29, binding); the VS Code edition keeps its
  own key flow; verification keys only ever enter a repository, signing keys live in the vendor folder, which is
  never read, never copied and never named beyond its folder name.
- **The two open field failures.** The VPN-route sign-in sitting dies about 4 min 20 s after the job starts (about
  5 min after the last keystroke): Open OnDemand's shell idle sweep (`OOD_SHELL_INACTIVE_TIMEOUT_MS` 300 s) resets on
  real client input only, so keep-alive frames do not count; a terminal `hpcworker claude login` in the OnDemand shell
  works. `reqp --qos=requeue` (priority 100) preempts running workers; `secp --qos=secondary` (priority 200, 90-day
  MaxWall) is where workers should live; the switch is lines 8 to 11 of `wayne.json` and is Greg's call.
- **The student's `~` is not Greg's.** Every handoff recipe writes `~` for `/wsu/home/go/go24/go2432`; a student who
  copies a command must first set `GH=/wsu/home/go/go24/go2432` or point it at their own copy, and `go2432/` below
  the Ceph gate stays closed to students (`docs/handoff/RECIPES.md` section 0 item 9).
- **The review Spaces.** Each per-task Space has its own ledger (`anonymous-mlhc/CTSpinoPelvic1K-reviews-<slug>`,
  slugs spine, ribs, nerve, ili, classfix, triaged); pointing a tool at the wrong one returns 0 cases with no error;
  a plain Restart can reseed from a cached old index, Factory reboot forces a fresh download (`docs/handoff/
  INFRASTRUCTURE.md` section 11; the note `review-space-repos` in folder 03).
- **Stale student-facing text.** `templates/CLAUDE.md` (lines 39 to 44, 54, 68, 81 to 82), the root `CLAUDE.md`
  (lines 26 to 27, 61) and `.claude/commands/onboard.md` (line 72) in the unpushed commit say v10 with S1 = 29, `rsync`
  results back and `git pull` on the grid (`GETTING_STARTED.md` carries none of these texts, grep 2026-10-08); the handoff's allowed login-node list is sbatch, squeue,
  scancel, log reads, ls, scp and small sed, `rsync` is killed by name, and whether `git` is tolerated on warrior is
  not recorded (OPEN_QUESTIONS E18, F10). The Beethoven quick start and `ACCOUNTS.md` / `LAB_LEAD.md` headers still
  say 12.0.0 while `INSTALL.md` / `USE.md` are 14.0.0; the newest dated texts win (INFRASTRUCTURE section 13 row 21).
- **Laptop paths and short prefixes inside copied documents.** The laptop paths (the author's Windows user folder, the
  OneDrive Desktop and the Claude project slug, in their Windows, Git Bash and WSL spellings) were replaced by kind in 26
  copies with `[laptop home]`, `[laptop Desktop]` and `[laptop project slug]` (96 replacements; `MANIFEST_LOCAL.md`
  section 5); the short prefixes (`ssn:`, `ctsp:`, `bth:`, `students:`) are the sources' own wording and are history,
  not dependencies. The live reference is always the repository at the commit named in the copy record at the top of
  each file and in `MANIFEST_CODE.md`; the full path each copy was read from is in `MANIFEST_LOCAL.md` section 4 only.

## How to be useful here

Say plainly what is not known: whether the two Beethoven commits are pushed, whether 10.0.0 or any later build was
ever submitted to the Chrome Web Store, whether Beethoven for VS Code 4.0.0 reached the Marketplace, the current
roster, and whether `git` survives on warrior are all "not recorded" on 2026-10-08. Prefer a measurement on the grid
to a reading of the panel. Before any student receives this folder, Greg confirms the reader split (OPEN_QUESTIONS
A29, A30) and whether the six Beethoven notes stay.
