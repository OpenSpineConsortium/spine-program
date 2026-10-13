# Handoff: spine-program, the board and the grid, as of 2026-10-12

For any Claude session that picks up Greg's spine and data-platform work. Read this, then the root `CLAUDE.md`, then the
folder you are working in. The facts below were checked against GitHub, the grid and the files on 2026-10-12 (times are
Detroit time unless marked UTC).

## 1. What spine-program is

- `OpenSpineConsortium/spine-program`, private, default branch `main`. One repository, 13 project folders
  (`01_carm_level_detection` to `12_website_pacs_demo`, and `99_archive`), each self-contained: `CLAUDE.md`, `README.md`,
  `DATA.md`, `TODO.md`, `STATUS.md`, `MEMORY.md` with `memory/`, and three manifests (`MANIFEST_GRID.md`,
  `MANIFEST_CODE.md`, `MANIFEST_LOCAL.md`). `_plan/` holds how the tree was built. Greg's local clone:
  `C:\Users\grego\OneDrive\Desktop\spine-program`.
- Greg's goal: students, and Greg first, add the repository to a Claude Code project, choose a project folder, and work
  its issues. Greg, 2026-10-12: "anyone can read anything". Every collaborator with Write reads every folder; "Greg-only"
  and the label `greg-first` govern who claims and hand-outs, not who reads.
- Do not do a project's research unless Greg asks for it. The research tasks are issues on the board.

## 2. How work happens here: the Symphony claim protocol

- Symphony (`OpenSpineConsortium/symphony-protocol`) was adopted through its GitHub Apps on the evening of 2026-10-11
  (pull request #1, merged by the Symphony App at 01:09 UTC on 2026-10-12). Rules: `docs/agents/PROTOCOL.md`.
- The board is `STATE.md` on the branch `board`, rewritten by `.github/workflows/board.yml` when an issue is opened,
  edited, closed, reopened, labelled or unlabelled, when a pull request is opened, pushed to, reopened or closed, when a
  branch is made or deleted, on a push to main, and every six hours. A comment, or marking a pull request ready, does not
  start it; the label `in-review` does. Read it with
  `git fetch origin +refs/heads/board:refs/remotes/origin/board && git show origin/board:STATE.md`, or `/board`.
- **Never edit main by hand, never push to main, never merge.** Every change is: an issue labelled `todo`; a claim (first
  push of branch `claude/<N>` whose only commit adds `docs/agents/claims/<N>.md`); the labels `claimed` and the account's
  label (`account:main` is Greg's) on the issue and the claim file posted as a comment
  (`gh issue comment N --body-file docs/agents/claims/N.md`); a draft pull request with "Closes #N"; the work; the claim
  file deleted; the pull request marked ready; the label `in-review`. Greg merges. GitHub does not enforce that: the
  ruleset needs a pull request but zero approvals and no check, auto-merge is allowed, and a session on Greg's machine acts
  as Greg's own GitHub account. So a session never merges and never turns on auto-merge unless Greg says so. Opening
  issues, labels and comments is fine; that is the board, not the tree.
- origin has three branches, `main`, `board` and `metrics`, and a `claude/<N>` branch only while a claim is open
  (`git ls-remote origin 'refs/heads/claude/*'`). Workflows force-push `board` and `metrics` (`metrics` shares anonymous
  aggregates daily, switched by `.github/symphony-metrics`); never edit them or put them under a ruleset.
- Committed under `.claude/` so a cloud session has them: the skills `/claim`, `/remember` and `/checkpoint` (posts a
  comment on the claim's pull request) in `.claude/skills/`, and the command `/board` in `.claude/commands/board.md`. The
  `symphony` plugin (`claude plugin install symphony@symphony-marketplace --scope project`; already installed at user
  scope on Greg's machine) adds the board at session start and a push guard; use the unprefixed skills, not
  `/symphony:*`, whose copies name files this repository does not have.
- No CI check exists. `docs/agents/PROTOCOL.md` describes a required check that is not here; trust the root `CLAUDE.md`.
  Before marking a pull request ready, check by hand: claim file deleted, "Closes #N", every acceptance line met, only the
  issue's files changed.
- A claude.ai Project thread or cloud session reaches only the clone and GitHub: no grid, ssh, sbatch, WSL, Greg's HOME
  or the other repositories (root `CLAUDE.md`, "What a cloud session reaches"). A change to another repository lands as
  `<folder>/patches/<N>-<slug>.patch` in the claim's pull request; Greg applies it.

## 3. The board on 2026-10-12

- Merged: #1 adoption; #3 student start; #43 to #61 one `DATA.md` per folder plus the migration refresh and the skills
  fixes; #73 to #78 the readiness fixes (CLAUDE.md rules, README route, skills, personal-data redaction, student python
  environment, data state); #79, which records Greg's answers of 2026-10-12 and closed #68 to #71.
- Open and labelled `todo`, unclaimed, in the board's queue:
  - 26 research or maintenance tasks, two per folder: 10 (#17, #18), 11 (#19, #20), 03 (#21, #22), 04 (#23, #24),
    05 (#25, #26), 06 (#27, #28), 12 (#29, #30), 01 (#31, #32), 02 (#33, #34), 07 (#35, #36), 08 (#37, #38),
    09 (#39, #40), 99 (#41, #42). #31 to #42 carry `greg-first`.
  - #72, Greg's (`greg-first`): install the Claude GitHub App on the repository, uninstall the Symphony Setup App,
    invite each student with Write and make their `account:<login>` label, try the student route once, and record what
    is done in `11_students_grid_access/STATUS.md`. Its python-environment step is done (job 40602926) though its box is
    unticked. No student has Write or a pending invitation yet. Whether either App is installed cannot be read with the
    stored token (it lacks `admin:org`).
  - #80: commit this handoff and the headless-claim scripts under `_ops/headless/`. #81: withhold the other datasets'
    patient header values that main still quotes (a phantom CT's personal name and a public C-arm collection's patient
    IDs in `01_carm_level_detection/docs/research/research_datasets_fourth_pass_verified_2026-09-22.json`; DeepFluoro
    accessions in `10_data_platform_grid/docs/PATIENT_IDENTITY_SPEC.md`).
- #17, #23 to #26, #28 to #30, #32 and #41 end with a section "Note added 2026-10-12 (readiness review)" in the issue
  body: #26 depends on #24, #32 on #31, #41 waits for the CLAUDE.md and README issues (both merged), #23, #24, #28, #29
  and #30 give the patch route, #25 and #41 set scope. #17's note predates the chain's end: A14 was linked after it, so
  A14's files are expected census mismatches too.

## 4. The grid on 2026-10-12

- Account `go2432@grid.wayne.edu`. HOME `/wsu/home/go/go24/go2432` (Panasas): 520 GB of the 4,295 GB soft limit, down
  from 4,051 GB on 2026-10-08. Ceph `/rs/rs_grp_oschome/go2432`: 9 of 20 TB.
- **The Ceph migration is complete.** Every batch with data was copied, verified, cut over and finalized (B00 to B11,
  B13, B14; B03 had nothing to move). The chain's last job ended at 07:28; nothing of it is queued. Earlier refusals
  (B02 twice; the B04 and B14 finalizes on read-only Mendeley copies) were fixed and re-run; the last chain (B05, B10,
  B11, B13) logged none. B12 was dropped: nnU-Net's containers bind no Ceph path, so `~/spinesurg-ct-nnunet/nnunet/raw`
  is still a real folder on HOME. The other HOME spellings are links into Ceph. Code and logs:
  `Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet` (private, branch `L6_Class`) `data_platform/`, on the grid at
  `~/spinesurg-ct-nnunet/data_platform`.
- **Who reads what.** Approved students are named-user ACL entries on `/rs/rs_grp_oschome` (give access only that way;
  the group `oschome` has no rights on the VinDr, BUU and s1v11 folders, so a member of the group is refused there).
  Below it, approved students read every folder under `/rs/rs_grp_oschome/go2432/data/`: VinDr-SpineXR (`vindr_spinexr`
  and the older `vindr`, reopened 2026-10-12), BUU-LSPINE, Mendeley and every bank built from their pixels (every
  approved student holds the PhysioNet credential and the VinDr and BUU agreements), and s1v11 (opened without a token
  check). The shared python `/rs/rs_grp_oschome/go2432/envs/spineps212` and `/rs/rs_grp_oschome/go2432/results` are
  open. **One data path stays owner-only:** `data/ctspinopelvic1k_build_tree/derived/build_archive_private`, whose one
  file is the annotator map (students' identities). Also owner-only, by design and not data: `private_ip`, `u251_meth`,
  four `hpcworker` folders and `singularity_cache/cache` under `/rs/rs_grp_oschome/go2432`. `data/ctsp_april` was mode
  777; since 2026-10-12 no one but Greg can write there.
- Greg's HOME is mode 750 with group `advcomp`; the approved student is not in `advcomp`, so HOME is closed to them. Its
  credential files are mode 600 or 700.
- The visibility script is `data_platform/plan/publish_visibility.sh` at spinesurg-ct-nnunet `0ab783f`: the plan's
  `restricted` flag no longer closes anything (`HONOUR_PLAN_RESTRICTED=0`); `FIXED_RESTRICTED_PATHS` holds the one path.
- Dedup: links applied for groups A01, A05, A06, A11, A14 and A15. Deleted on 2026-10-12: the TotalSegmentator v3.0.0
  zip (37.4 GB), the v2.0.1 zip (23.6 GB) and the NHANES extracted pickles (159 GB; the 1.0 GB zip that regenerates them
  stays). Groups A12, A17, A18, A19, A22 and A23 are being hashed on their finalized copies (job 40603158; read its
  result in `data_platform/dedup/hash_results/`). About 134 GB of deletion candidates and 218 GB of conditional ones wait
  on Greg (`data_platform/dedup/DEDUP_PLAN.md`); A04, A07 and A13 too.
- Students: `11_students_grid_access/STUDENT_ENV.md` (which python; code reaches the Beethoven worker by
  `git archive | ssh tar`). Every folder's `DATA.md` lists its grid paths with a read-only check line.

## 5. Greg's answers of 2026-10-12

- "anyone can read anything": every folder of the repository; on Ceph, everything under `data/` except the annotator map,
  plus the shared python environment and results. HOME and the non-data folders above stay closed.
- "dont worry about tokens": no credential rotation planned; s1v11 opened without reading its upload scripts.
- History of main kept (no rewrite). Main no longer holds the C-ArmLSpine case134 console patient name, patient IDs or
  the (0029,0016) values (#73); they remain in the seed commit's history. #81 covers the other datasets' values.
- "delete those last zips": done (section 4).

## 6. Traps

- **Windows network.** Most https calls to GitHub from Windows stall about 11 s in the DNS lookup (curl to
  api.github.com 11.3 s; with `curl -4`, 0.17 s); a git call over https takes about 20 s, and on 2026-10-12 one Windows
  `git fetch` failed with "Could not resolve host: github.com". Run gh and `git fetch` through WSL
  (`wsl -e bash -lc '...'`; gh is `~/.local/bin/gh` there; set
  `GH_TOKEN=$(printf 'protocol=https\nhost=github.com\n' | git credential fill | sed -n 's/^password=//p')` per command
  and never print it; scopes `repo` and `workflow` only). But push the claim branch with a plain `git push` from Claude
  Code's Bash tool (root `CLAUDE.md` rule 10), and never run `git status`, `add` or `commit` from WSL in the Windows
  clone: line endings make every tracked file look modified there.
- **The plugin's session-start board is stale on Windows**: its fetch is cut at 10 s. Read the board with `/board` or a
  WSL fetch before claiming.
- **Headless Claude sessions** on Windows: the VS Code extension's binary,
  `C:\Users\grego\.vscode\extensions\anthropic.claude-code-<version>-win32-x64\resources\native-binary\claude.exe`,
  run as `-p --model claude-opus-5-5 --dangerously-skip-permissions --max-turns <N>` with stdin from `/dev/null`. There is
  no `claude` on the Windows PATH, and the WSL install is not signed in. One worktree per claim at a short path
  (`C:\Users\grego\spc\<N>`; `core.longpaths true`). Put a real `python3` first on PATH: the Microsoft Store stub makes
  the plugin's push guard silently do nothing. A 24-file issue needed more than 80 turns. The scripts are in
  `_ops/headless/` (issue #80).
- **Redaction wording.** "Replace every value of Patient's Name" made a session also overwrite 760 pseudonymous case
  labels. Name exactly what to remove, and check the removed values' shapes by count before merging.
- **sbatch copies the script at submission**: editing a script does not change a queued job; cancel and requeue. Never
  `cd "$(dirname "$0")"` in an sbatch script: it lands in the spool folder.
- **Login node (warrior)**: no python, no heavy `find`; submit jobs, read with `ls`, `cat`, `tail`, `sacct`.
- Write scripts as files and run them by path; inline heredocs on this machine collapse backslashes.

## 7. Where the record is

- Memory (sessions opened in `CTSpinoPelvic1K-1`): `symphony-spine-program-adoption.md`,
  `spine-program-no-manual-edits.md`, `data-platform-migration-2026-10.md`, `windows-dns-ipv6-stall.md`.
- The repository: `README.md` (student route, "Choosing a project"), `INDEX.md`, each folder's `STATUS.md` (one dated line
  for 2026-10-12), `10_data_platform_grid/STATUS.md` and `DATA.md` for the grid.
- Never the banned word (root `CLAUDE.md` rule 1); whole-number versions only; Greg's affiliation is General Surgery; no student name or
  username in any file.
