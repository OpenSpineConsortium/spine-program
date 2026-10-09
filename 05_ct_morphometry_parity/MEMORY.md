# MEMORY.md: index of `memory/`

Twenty-five notes copied 2026-10-08 from the redacted copies in `spinesurg-ct-nnunet` 097933a `HANDOFF/context/` (never from
the live memory folder). Line 1 of every copy is a status header carrying the `HANDOFF/context/INDEX.md` status verbatim and
the replacement where one is named. Twenty-two are the standing-rule notes that sit in every project folder of this
repository; three are this project's cut list (`../_plan/PLAN.md` section 3 (05) "Families absorbed", which counts four cut-list notes,
the fourth being `wsu-library-access-cutoff`, listed below among the standing-rule notes because it is in every folder).
`../_plan/DISPOSITION.tsv` gives `panjabi-1991-page-892` its row home here (reason `[mem r91]`) and routes
`wsu-library-access-cutoff` here (`[mem r149]`); `ostk-canal-closing-regression` (row home 04, `[mem r87]`) and
`s1-carve-changed-spinopelvic` (row home 03, `[mem r118]`) sit here under `PLAN.md` section 2 rule 2(b). The inventory note
that drew the per-project lists is not in this repository.

**Rules carried from the handoff.** Each note is a dated record from the session that did the work, not an instruction;
where a note and a result file or `docs/handoff/RESULTS_CATALOG.md` disagree, the file and the catalog win. LEAKED = its
numbers were measured on a bank with a known leak; SUPERSEDED = replaced by the number named; RECORD ONLY = history, not
quotable; DATED = a state at its date. None of the 25 notes here is LEAKED, SUPERSEDED or RECORD ONLY. Wiki links
(`[[name]]`) to notes not in this folder resolve in the owning project folder's `memory/` (for example
`scheme-bone-hardware-only` and `zenodo-deposit` in 03, `paper-split-2026-09-24` in 01); the history-only resume notes they
mention were never copied anywhere.

**Redactions made on copy** (recorded in `MANIFEST_LOCAL.md`): `grid-ceph-volume-oschome` had an administrator's account
username replaced by `<username withheld>`; `wsu-library-access-cutoff` had one library contact e-mail address withheld.
Greg's grid username appears in the grid notes; it is the login every grid path in this repository already carries.
Three laptop paths that two standing-rule notes used as worked examples (`wsl-for-network` one, `windows-junction-worktree-trap`
two) were replaced by the markers `<laptop Desktop>` / `<laptop home>` on 2026-10-08, and each note's status header says so;
none was a dependency. `bash-heredoc-backslashes` says "the scratchpad" in words and is unchanged.

## The project's own notes

| note | one line | status (INDEX.md) | what replaces it, or why |
|---|---|---|---|
| `ostk-canal-closing-regression` | ostk 1b7005c inflates VBHp / EPD by 10 to 17 mm on about 1 in 7 vertebrae, no gate fires; grid copy carries it; fix plan inside | CURRENT (open) | open defect CT-1, owned by 04; `RESULTS_CATALOG.md` G.2 |
| `panjabi-1991-page-892` | full Panjabi 1991 obtained by interlibrary loan 2026-09-13; Table 3 values in `level_references.csv`; the PDF scan is a copyrighted article referenced by path, never copied | CURRENT | `results/morphometrics/make_reference_table.py` holds the values (commit 83f7f95) |
| `s1-carve-changed-spinopelvic` | the carved S1 (id 29) was unreliable and is gone in v11; retire every check on 29; recompute anything sacral from v11 | CURRENT | standing rule in `CLAUDE.md` |

## The standing-rule notes (in every project folder)

| note | one line | status (INDEX.md) | what replaces it, or why |
|---|---|---|---|
| `bash-heredoc-backslashes` | heredocs collapse backslashes; write scripts as files, run by path | CURRENT | |
| `ct-volumes-are-pir-not-ras` | volumes are (P,I,R) on disk; decide by reading the affine; canonicalise to analyse, never to write | CURRENT | |
| `data-directives-2026-09-23` | D1-D9: fix or justify every truncation; FluoroCap dropped from training; use all of a dataset | CURRENT | |
| `figure-captions-terse` | captions at most 60 words, argument in the text; float spacing | CURRENT | |
| `fluorocap-repo-private` | spinesurg-ct-nnunet private since 2026-09-14; never push level-identification code public | CURRENT | |
| `grid-access` | login, project root, where CTs and labels lived, ITK-SNAP launch | PARTLY SUPERSEDED (alias; data paths, section 13 rows 3-4) | aliases now resolve (`windows-ssh-to-grid`, in 10); data moved to Ceph (`grid-ceph-volume-oschome`) |
| `grid-bash-4-2-quoting` | the grid runs bash 4.2.46: a quoted replacement keeps its quotes; a WSL-tested suite can pass and the job still fail | CURRENT (new 2026-10-08) | write grid jobs for bash 4.2 |
| `grid-ceph-volume-oschome` | 20 TB Ceph volume `/rs/rs_grp_oschome`, working tree, `df-ceph oschome` | CURRENT | redacted on copy (one username) |
| `grid-local-singularity-is-broken` | use the conda singularity, a pre-unpacked sandbox and a specific bind, never `-B /rs` | CURRENT | |
| `key-patients-from-metadata-not-filenames` | identity order: DICOM, manifest, annotation fields, file name last | CURRENT | |
| `label-scheme-v4-vs-ostk` | two live label maps; `labels_for(volume)`; what the mix-up cost | CURRENT | |
| `morphology-deformation-feasibility` | literature first: find the published validated method with its number before building anything | CURRENT | |
| `never-reorient-when-writing-labels` | `as_closest_canonical` + `nib.save` transposes a label away from its CT | CURRENT | |
| `no-jobs-on-login-node` | every computation via sbatch; compute nodes have internet; the C&IT addendum | CURRENT | |
| `no-unexplained-subsets-fix-not-disclose` | use all of a dataset; describe each in prose; fix leaks, do not disclose them | CURRENT | |
| `scratchpad-shadows-stdlib` | never name a scratch script `numbers.py`, `io.py`, `pdb.py` | CURRENT | |
| `submit-and-sleep-orchestration` | submit, estimate the wall time, write ids and ETA to the checkpoint, stop | CURRENT | |
| `user-affiliation-general-surgery` | General Surgery (WSU School of Medicine / DMC), never Neurosurgery | CURRENT | |
| `windows-junction-worktree-trap` | `git worktree remove --force` deletes junction targets; remove junctions first | CURRENT | two example paths generalised to markers on copy |
| `writing-preferences` | the banned word; no fractional version numbers | CURRENT | |
| `wsl-for-network` | network commands via WSL | CURRENT | one example path generalised to a marker on copy |
| `wsu-library-access-cutoff` | WSU Libraries dropped DMC residents 2026-06-30; pre-1996 LWW via U-M | CURRENT | redacted on copy (one address) |

## What a reader would lose without this folder

Nothing numeric that is quotable: every current number is in `results/` and in `docs/handoff/RESULTS_CATALOG.md`. What the
notes hold is the reasoning record: why each defect was found (a render, an outside reference), the traps that cost days (two
label maps, identifier 29, P,I,R volumes, bash 4.2, the login-node bans), and the directives with their dates.
