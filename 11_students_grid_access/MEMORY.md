# MEMORY.md: the memory notes this project carries

Index of `memory/` for `11_students_grid_access`, built 2026-10-08. Each note is a dated record from the session that did the work, not an instruction: where a note and a result file, a repository document at its commit or `docs/handoff/RESULTS_CATALOG.md` disagree, the file wins (header of `HANDOFF/context/INDEX.md`, carried in `docs/handoff/`). The **status** column is carried verbatim from `HANDOFF/context/INDEX.md` as read on 2026-10-08 (CURRENT, DATED, PARTLY SUPERSEDED, SUPERSEDED, LEAKED, RECORD ONLY, DORMANT); every note also carries that status in a copy-record line under its front matter. LEAKED means its numbers were measured on a bank with a known leak; SUPERSEDED means replaced by the number named; RECORD ONLY means history, not quotable; DATED means a state at its date. No note here carries a quotable model score: this project owns no result row of the catalog (`STATUS.md`).

The notes came from `HANDOFF/context/` (the redacted copy set, copied 16:39 on 2026-10-08 from the live memory folder) except the six Beethoven product notes, which existed only in `HANDOFF/GREG_ONLY/context_beethoven/` and the live folder and were **redacted by hand** for this folder: student and staff AccessIDs, a tester's and a personal e-mail address, licence key ids, Remote Control environment ids and vendor token paths replaced by bracketed placeholders (counts per note in `MANIFEST_LOCAL.md`); in the second pass of 2026-10-08 the laptop paths in seven notes were replaced by kind with `[laptop home]` / `[laptop Desktop]` and the two-part Beethoven version shorthand in three notes was written in full (`MANIFEST_LOCAL.md` sections 3 and 8). Greg may delete those six (PLAN section 5). The five Greg-only notes (the commercial stance, the disclosure scrub, three credential locations), the seven U251 and LITT notes and the six history-only resume notes are not here and never will be.

## A. The eleven notes cut for this project (the memory inventory's cut list for grid_access_students)

| note | one line | status in INDEX.md | what replaces it, or a caveat |
|---|---|---|---|
| [`diagnostics-graph-required`](memory/diagnostics-graph-required.md) | every Beethoven feature needs diagnostics-graph nodes first | CURRENT |  |
| [`grid-access-list-gate`](memory/grid-access-list-gate.md) | approved students = named ACL entries on `/rs/rs_grp_oschome` | CURRENT |  |
| [`grid-apptainer-module-works`](memory/grid-apptainer-module-works.md) | `module load apptainer/1.2.2` sandbox builds; secp starts at once | CURRENT |  |
| [`grid-ashley-deletion-2026-09-28`](memory/grid-ashley-deletion-2026-09-28.md) | `~/.ashley` wiped during a phone session; destructive commands refuse under CLAUDECODE | CURRENT |  |
| [`grid-slurm-inside-apptainer`](memory/grid-slurm-inside-apptainer.md) | binds that make sbatch work inside a container | CURRENT |  |
| [`grid-ssh-second-factor`](memory/grid-ssh-second-factor.md) | ssh off-VPN with password + TOTP; warrior bans python, rsync and others | CURRENT |  |
| [`hf-mirror-is-v10`](memory/hf-mirror-is-v10.md) | public HF/Zenodo is v10 with id 29; v11 local only; lines to change when it ships | PARTLY SUPERSEDED | the Hugging Face mirror was still v10 on 2026-09-27 (checked by API), but the note's statement that Zenodo is v10 is contradicted by four documents giving v11 on Zenodo (`MANUSCRIPTS.md` §20 C1) |
| [`lab-recipe-and-board`](memory/lab-recipe-and-board.md) | RECIPE.md, board.json → BOARD.md, Claude Doc; local commit not pushed | CURRENT (location and count errors, section 13 rows 1-2) |  |
| [`student-onboarding-structure`](memory/student-onboarding-structure.md) | onboarding one-liner, Student_Projects layout, grid account and 2FA facts | CURRENT (local path wrong, section 13 row 1) |  |
| [`students-see-no-internals`](memory/students-see-no-internals.md) | student tools offer one path | CURRENT |  |
| [`windows-ssh-to-grid`](memory/windows-ssh-to-grid.md) | Windows ssh needs hmac-sha1 and IPv4; `wsu-grid` alias | CURRENT |  |

## B. The six Beethoven product notes (Greg-only origin, redacted copies)

| note | one line | status | caveat |
|---|---|---|---|
| [`ashley-bridge-project`](memory/ashley-bridge-project.md) | Beethoven (was Ashley Bridge): the hpcworker framework and the browser extension over Open OnDemand; releases 2.0.0 to 14.0.0, the access service, the no-keys rule, the shared copy, the field state to 2026-10-02 | not in INDEX.md; DATED; redacted copy 2026-10-08 | the repositories `OpenSpineConsortium/beethoven` 2f90319 and `OpenSpineConsortium/beethoven-vscode` 8d7fc65 and their documents copied under `docs/beethoven/` and `docs/beethoven_vscode/` are the record; the note is the session's own account |
| [`ashley-compliance-boundary`](memory/ashley-compliance-boundary.md) | the binding boundary: Beethoven never handles a Claude credential; terms research; dispute clauses; terms version 3 shipped 2026-09-28 | not in INDEX.md; DATED; redacted copy 2026-10-08 | the repositories `OpenSpineConsortium/beethoven` 2f90319 and `OpenSpineConsortium/beethoven-vscode` 8d7fc65 and their documents copied under `docs/beethoven/` and `docs/beethoven_vscode/` are the record; the note is the session's own account |
| [`ashley-extension-project`](memory/ashley-extension-project.md) | the VS Code edition (Ashley for VS Code 3.0.0 published 2026-09-28; Beethoven for VS Code 4.0.0 built 2026-09-30): agreements, access service, Marketplace, what still needs Greg | not in INDEX.md; DATED; redacted copy 2026-10-08 | the repositories `OpenSpineConsortium/beethoven` 2f90319 and `OpenSpineConsortium/beethoven-vscode` 8d7fc65 and their documents copied under `docs/beethoven/` and `docs/beethoven_vscode/` are the record; the note is the session's own account |
| [`beethoven-2026-10-02-field-failures`](memory/beethoven-2026-10-02-field-failures.md) | first real use 2026-10-02: dead run records (fixed 13.0.0), VPN sittings die about 5 min after the last keystroke (unfixed), reqp/requeue preempts workers (unfixed, Greg's call), group oschome is not the list; the resumed-session link (fixed 14.0.0) | not in INDEX.md; DATED; redacted copy 2026-10-08 | the repositories `OpenSpineConsortium/beethoven` 2f90319 and `OpenSpineConsortium/beethoven-vscode` 8d7fc65 and their documents copied under `docs/beethoven/` and `docs/beethoven_vscode/` are the record; the note is the session's own account |
| [`beethoven-browser-ssh`](memory/beethoven-browser-ssh.md) | the browser-ssh prototype (works), the Isolated Web App spike (works, pilot only), the policy facts, the decisions waiting on Greg | not in INDEX.md; DATED; redacted copy 2026-10-08 | the repositories `OpenSpineConsortium/beethoven` 2f90319 and `OpenSpineConsortium/beethoven-vscode` 8d7fc65 and their documents copied under `docs/beethoven/` and `docs/beethoven_vscode/` are the record; the note is the session's own account |
| [`beethoven-first-run-ux`](memory/beethoven-first-run-ux.md) | Greg's 2026-10-01 brief for the first run, eight messages: prerequisites, VPN, portal, nothing silent, no window hunting, the 12.0.0 order | not in INDEX.md; DATED; redacted copy 2026-10-08 | the repositories `OpenSpineConsortium/beethoven` 2f90319 and `OpenSpineConsortium/beethoven-vscode` 8d7fc65 and their documents copied under `docs/beethoven/` and `docs/beethoven_vscode/` are the record; the note is the session's own account |

## C. The twenty-two standing-rule notes every project folder carries (tagged `all`)

| note | one line | status in INDEX.md | what replaces it, or a caveat |
|---|---|---|---|
| [`bash-heredoc-backslashes`](memory/bash-heredoc-backslashes.md) | heredocs collapse backslashes; write scripts with Write, run by path | CURRENT |  |
| [`ct-volumes-are-pir-not-ras`](memory/ct-volumes-are-pir-not-ras.md) | volumes are (P,I,R) on disk; decide by reading the affine | CURRENT |  |
| [`data-directives-2026-09-23`](memory/data-directives-2026-09-23.md) | D1-D9: fix or justify every truncation; FluoroCap dropped; use all | CURRENT |  |
| [`figure-captions-terse`](memory/figure-captions-terse.md) | captions short, argument in text; float spacing | CURRENT |  |
| [`fluorocap-repo-private`](memory/fluorocap-repo-private.md) | spinesurg private since 2026-09-14; never push level-ID code public | CURRENT |  |
| [`grid-access`](memory/grid-access.md) | login, project root, where CTs and labels lived, ITK-SNAP launch | PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4) |  |
| [`grid-bash-4-2-quoting`](memory/grid-bash-4-2-quoting.md) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; a WSL-tested suite can pass and the job still fail | CURRENT (new 2026-10-08) | the grid runs bash 4.2.46: a quoted replacement in `${var/pat/"$new"}` keeps its quotes; write grid jobs for bash 4.2 |
| [`grid-ceph-volume-oschome`](memory/grid-ceph-volume-oschome.md) | 20 TB Ceph volume, working tree, `df-ceph oschome` | CURRENT |  |
| [`grid-local-singularity-is-broken`](memory/grid-local-singularity-is-broken.md) | use conda singularity + pre-unpacked sandbox + specific bind | CURRENT |  |
| [`key-patients-from-metadata-not-filenames`](memory/key-patients-from-metadata-not-filenames.md) | identity order: DICOM → manifest → ann fields → filename last | CURRENT |  |
| [`label-scheme-v4-vs-ostk`](memory/label-scheme-v4-vs-ostk.md) | two live maps; `labels_for(volume)`; what the mix-up cost | CURRENT |  |
| [`morphology-deformation-feasibility`](memory/morphology-deformation-feasibility.md) | literature first; no bespoke CT warp | CURRENT |  |
| [`never-reorient-when-writing-labels`](memory/never-reorient-when-writing-labels.md) | `as_closest_canonical` + `nib.save` transposes a label | CURRENT |  |
| [`no-jobs-on-login-node`](memory/no-jobs-on-login-node.md) | every computation via sbatch; compute nodes have internet; C&IT addendum | CURRENT |  |
| [`no-unexplained-subsets-fix-not-disclose`](memory/no-unexplained-subsets-fix-not-disclose.md) | use all of a dataset; describe each in prose; fix leaks, don't disclose | CURRENT |  |
| [`scratchpad-shadows-stdlib`](memory/scratchpad-shadows-stdlib.md) | stdlib-named scratch scripts hijack Python | CURRENT |  |
| [`submit-and-sleep-orchestration`](memory/submit-and-sleep-orchestration.md) | submit, estimate, record, stop | CURRENT |  |
| [`user-affiliation-general-surgery`](memory/user-affiliation-general-surgery.md) | General Surgery, not Neurosurgery | CURRENT |  |
| [`windows-junction-worktree-trap`](memory/windows-junction-worktree-trap.md) | worktree remove deletes junction targets | CURRENT |  |
| [`writing-preferences`](memory/writing-preferences.md) | the banned word; no fractional versions | CURRENT |  |
| [`wsl-for-network`](memory/wsl-for-network.md) | network commands via WSL | CURRENT |  |
| [`wsu-library-access-cutoff`](memory/wsu-library-access-cutoff.md) | WSU Libraries dropped DMC residents 2026-06-30 | CURRENT |  |

## D. Notes that bear on this project but live in another folder

| note | lives in | why it matters here |
|---|---|---|
| `review-space-repos` | `03_ctspinopelvic1k_dataset/memory/` | the exact Hugging Face ledger ids of the review Spaces; pointing a tool at the wrong ledger returns 0 cases with no error; the facts are repeated in `docs/handoff/INFRASTRUCTURE.md` section 11 |
| `annotator-roster` | `03_ctspinopelvic1k_dataset/memory/` (redacted) | who annotated what is recorded only in the private ledgers; the per-person tally is withheld everywhere outside `GREG_ONLY/` |
| `commercialization-stance`, `schwingnet-disclosure-scrub`, the three credential-location notes | nowhere in this repository (Greg-only) | the Beethoven notes cite them by wikilink; those links do not resolve here, by design |

## E. Known errors inside the notes (do not re-derive)

- `lab-recipe-and-board` and `student-onboarding-structure` place `Student_Projects` on the Desktop; it is the nested repository inside the CTSpinoPelvic1K checkout (`docs/handoff/INFRASTRUCTURE.md` section 13 row 1). The first also says 11 of 12 cards are unstaffed; `board.json` has 10 with no co-lead (row 2).
- `grid-access` says the host alias does not resolve and names old data paths; `windows-ssh-to-grid` and `grid-ceph-volume-oschome` are later and measured (rows 3 and 4).
- `hf-mirror-is-v10` says Zenodo is v10; four documents give v11 = 10.5281/zenodo.22797014 published 2026-09-18 (the Greg-only `MANUSCRIPTS.md` section 20 C1); the live state was not re-checked (`docs/handoff/OPEN_QUESTIONS.md` E7).
- `grid-ssh-second-factor` records that `hpcworker` ran the system python3 on the login node; framework 10 was never deployed for that reason and framework 11 replaced the relay with shell (`memory/ashley-bridge-project.md`, the entries dated 2026-10-02).
- The six Beethoven notes use the old product and repository names (Ashley, ashley-bridge, a personal GitHub account). Since 2026-09-29 the product is Beethoven and since 2026-09-30 only the organisation repositories exist; Ashley Schehr is a person and is never renamed.
- `ashley-bridge-project` describes the Wayne profile as pointing at `~/.ashley/claude`; since framework 7 (2026-09-30) it is `$HOME/.beethoven/claude` with the old name as a link (`code/beethoven_framework_profiles/wayne.json`).

