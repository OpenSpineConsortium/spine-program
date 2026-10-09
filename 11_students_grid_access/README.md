# 11_students_grid_access: students on the grid

Beethoven, onboarding, the lab recipe and the medical-education record. Project 11 of 12 in `spine-program`, a
support project: it produces no finding; its product is students producing work under the recipe. Built 2026-10-08
from the plan in `../_plan/PLAN.md` (section 3, "11") and the 44 rows of `../_plan/DISPOSITION.tsv` whose
`project_folder` is `11_students_grid_access`.

**Reader.** Greg-only until Greg confirms the reader split of the handoff (`docs/handoff/OPEN_QUESTIONS.md` A29,
A30) and whether the six redacted Beethoven notes stay in `memory/` (`../_plan/PLAN.md` section 5). After that the
guides, the recipe, the templates and the tutorials are student-safe; the compliance, licensing, store and roster
material (`docs/beethoven/store/`, `docs/beethoven_vscode/LICENSING.md`, `legal/`, `research/`, the six notes) is
not handed out.

## What this project is

A medical student with a Wayne State grid account, a Claude Pro or Max subscription, Chrome and Google Authenticator
installs Beethoven from a private Chrome Web Store listing, signs in to the grid's Open OnDemand portal (or, since
12.0.0, by ssh with password and code through a bundled script bridge), and the extension starts a Claude Code worker
as a Slurm job in the student's own account, inside the lab's shared container, and opens it in claude.ai through
Claude Code Remote Control. The lab's shared copy of the framework lives on the Ceph volume; approval is a named-user
ACL entry on the volume root kept equal to the access service's roster. From there the student follows the lab recipe
(`code/student_projects_3f1cf04/RECIPE.md`): pre-register, run everything as jobs, bring numbers into a manuscript
only through a manifest key, hand over by pull request. The medical-education study that describes the programme is
published (Schehr A, Kim J, Schwing G, Cureus 2026;18(7):e112661, 2026-07-14, `manuscripts/`).

## Goal

Keep that path working: the browser extension and `hpcworker` framework (release 14.0.0, 2026-10-03,
`OpenSpineConsortium/beethoven` main 2f90319), the VS Code edition and the access service
(`OpenSpineConsortium/beethoven-vscode` main 8d7fc65), the onboarding one-liner and `Student_Projects` (local commit
3f1cf04, not on the remote), the review Spaces and annotator tooling, the access-list gate on `/rs/rs_grp_oschome`,
and the medical-education record. Fix the two open field failures, push or hold the unpushed recipe, settle the
duplicate med-ed submission, and bring the stale student-facing documents to the current rules and label scheme.

## State on 2026-10-08

- **Operational, with two unfixed field failures.** First real use 2026-10-02 (`memory/beethoven-2026-10-02-field-
  failures.md`): the dead-run-record hang was fixed in 13.0.0 (commit e11ae27, 2026-10-03) and the resumed-session
  link in 14.0.0 (2f90319); still open are the VPN-route sign-in sitting that dies about 4 min 20 s after the job
  starts (about 5 min after the last keystroke; Open OnDemand's shell idle sweep, 300 s, resets on real client input
  only; four times, jobs 40552222, 40552237, 40552239, 40552241, 40552343, 40552346, exit 3) and `reqp --qos=requeue`
  preempting running workers (the renewal job 40523658 sat PENDING more than 12 h at priority 100 while `secp`
  had 45 to 47 idle nodes at priority 200; the profile change to `secp/secondary` is Greg's call).
- **The gate works.** Measured 2026-10-02: group `oschome` has two members and is C&IT's; the volume root is
  `drwxrws--T` with `other::---`; `shared/` and `shared/beethoven` were made other-readable (34,000 files, 23 s);
  approval = `user:<AccessID>:rwx` on the root; one entry set by hand that day is the only one seen to work
  (`memory/grid-access-list-gate.md`; `docs/beethoven/guides/LAB_LEAD.md` section 9).
- **The roster is not on disk.** The approved list lives in the access service (`docs/handoff/OPEN_QUESTIONS.md`
  B34); nothing in this folder names its members.
- **Student_Projects is one commit ahead of its remote.** Local `main` 3f1cf04 (2026-09-27, the recipe, the board,
  the templates) against `origin/main` fd60c58 (`git status -sb` on 2026-10-08: "ahead 1"); pushing a public
  repository is Greg's call (OPEN_QUESTIONS A25). The recipe and templates are therefore copied here under
  `code/student_projects_3f1cf04/`.
- **The med-ed study is published**; the JEEHP version on disk (14 to 15 June 2026, same 16 respondents, same
  six-domain table) would duplicate it (OPEN_QUESTIONS A21; the Greg-only `MANUSCRIPTS.md` section 12). The CNS 2026
  abstract "Beyond the Cadaver Lab" was selected as a printed poster (the abstract number 66639 is in the Greg-only
  `MANUSCRIPTS.md` section 12; the decks carry the title and "Ten sub-projects span 16 contributors", not the number);
  both decks are in `manuscripts/talks/`.
- **Stale entry documents.** `templates/CLAUDE.md` still gives v10 identifiers with S1 = 29 (line 54); `templates/CLAUDE.md`
  (lines 39 to 44, 68, 81 to 82), the root `CLAUDE.md` (lines 26 to 27, 61) and `.claude/commands/onboard.md` (line 72)
  tell students to `rsync` results and `git pull` on the login node (`GETTING_STARTED.md` carries none of these texts,
  grep 2026-10-08); the Beethoven quick
  start and two guides still say 12.0.0 (OPEN_QUESTIONS F10; `docs/handoff/INFRASTRUCTURE.md` section 13 rows 5
  and 21).
- **Not recorded on 2026-10-08:** whether 2f90319 and 8d7fc65 are pushed to GitHub (no local remotes; the push goes
  through `tools/push_org.sh`); whether any build after 9.0.0 was submitted to the Chrome Web Store (10.0.0 "has not
  been submitted as far as I know", `memory/ashley-bridge-project.md`); whether Beethoven for VS Code 4.0.0 reached
  the Marketplace (3.0.0 was published 2026-09-28 20:24 UTC as `OpenSpineConsortium.ashley`); whether `git` is
  tolerated on warrior (OPEN_QUESTIONS E18); the current roster.

## Success criteria

Pre-stated, from the plan's first five steps (`../_plan/PLAN.md` section 3, "11") and carried into `TODO.md`:

1. A grep for `@`, key ids, account names and usernames over `memory/` returns nothing personal (done for this
   build: `MANIFEST_LOCAL.md` section 5; Greg still decides whether the six notes travel at all).
2. A worker survives 30 minutes idle on the VPN route in a test; a two-hour test job is not preempted after the
   profile change; one student completes the first-week recipe (`docs/handoff/EXTRACTS_11.md`, "A student's first
   week") end to end.
3. `Student_Projects` 3f1cf04 is pushed, or its hold is recorded, and the remote's HEAD is written into
   `MANIFEST_CODE.md`.
4. The JEEHP decision (drop, or a follow-up with new data, Ashley Schehr leading) is written into `STATUS.md`.
5. No student-facing document instructs python or rsync on the login node; every one names v11 once the public
   mirror ships v11; the README of the gate describes named ACL entries, never people.

## How this folder relates to the others

| folder | relation |
|---|---|
| `10_data_platform_grid` | owns the Ceph volume, the migration and grid operations; this project owns the gate on the volume root and the shared Beethoven tree under it; the one read-only grid pass of 2026-10-08 22:20 UTC is copied there, not here |
| `03_ctspinopelvic1k_dataset` | the dataset documents students read first (README, KNOWN_ISSUES, the v11 scheme), the review Spaces' ledgers and guides, the committed annotation tally; step 5 here waits on its step 4 |
| `12_website_pacs_demo` | the public site renders the Beethoven pages from the two repositories' texts and hosts `onboard.sh`, `onboard.ps1`, the onboarding primer and the six tutorials; its step 5 re-checks those pages against this project's step 5 |
| `06_transitional_ct_census` | needs readers; the recipe's roles (Ashley Schehr screens, "Dr Tech" confirms) come from `RECIPE.md` section 0 |
| `01_carm_level_detection` | Greg-only; students do not touch it; the hospital-testing IRB letters live in its `regulatory/`, and the student umbrella determination HPR 2026-269 (2 September 2026) is cited from there |
| `99_archive` | the 6.0.0 tester package and the unpacked tester folder, superseded by release 14.0.0, are listed there by path |

## Layout

```
CLAUDE.md  README.md  MEMORY.md  MANIFEST_GRID.md  MANIFEST_CODE.md  MANIFEST_LOCAL.md  STATUS.md  TODO.md
memory/                     39 notes with their statuses (MEMORY.md)
docs/handoff/               the eight student-readable handoff files, whole, plus EXTRACTS_11.md
docs/beethoven/             the Beethoven repository's documents at 2f90319 (repo_root/, guides/, store/, release_14.0.0/)
docs/beethoven_vscode/      the VS Code edition's documents at 8d7fc65 (repo_root/, manual/, legal/, research/)
docs/outreach/              two outreach drafts, redacted
docs/survey_protocol.md     the PACS-demo usability survey protocol (CROSS / CHERRIES); not the med-ed survey
docs/*.pdf                  the two HPC-orchestration write-ups; the Lab Recipe as a 14-page export of 2026-09-27
code/student_projects_3f1cf04/   the recipe, templates, tools, commands and the demo study of the unpushed commit
code/beethoven_framework_profiles/wayne.json   the Wayne State site profile (the partition lever)
figures/beethoven_vscode/   the six figures of the VS Code edition's documents
manuscripts/                the Cureus article; the JEEHP draft; talks/ the two CNS poster decks
regulatory/openresearch/    the seven prompts of 2026-09-27 that specified the product
```
