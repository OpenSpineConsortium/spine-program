# About the handoff copies in this folder

The eight files beside this note (`README.md`, `GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`, `DATASET_USAGE.md`,
`LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md`) are the student-readable half of the handoff written on
2026-10-08 in `HANDOFF/` of the private repository `spinesurg-ct-nnunet` at commit 097933a (branch `L6_Class`). Every
project folder of this seed carries the same eight (`../../../_plan/PLAN.md` section 2 rule 3), so a reader with one
folder has the results catalog, the recipes and the open questions. The Greg-only handoff files (`RESEARCH_DIRECTIONS.md`,
`MANUSCRIPTS.md`, `LITERATURE_STATE.md`, `CONTEXT_EXPORT.md`, `working_notes/`, `GREG_ONLY/`) are not in this folder; the
parts that bear on this project are extracted with their ids into `../../STATUS.md` and `../../TODO.md`
(`RESEARCH_DIRECTIONS.md` sections 1.3, 3, 4 and 6; `MANUSCRIPTS.md` sections 6 and 11). This note was written for this
folder on 2026-10-08 and is not a copy of anything (`../../MANIFEST_LOCAL.md` section 4).

## The rows that are this project's

`RESULTS_CATALOG.md` Part F2 rows F.21-F.45 (the spinopelvic estimator, the per-level atlas, transitional anatomy), F.5-F.7
(the S1 carve audit and the v11 merge), F.16, and Part G rows G.2-G.5 (the ostk defects this folder waits on);
`OPEN_QUESTIONS.md` rows B27, B29, C8, C9, C22, D2, D4, D5, E9, F8, F9, F18; `RECIPES.md` section 9 (the CTSpinoPelvic1K
extractors) and section 0 (how work reaches the grid); `LEAKAGE.md` for the rule that keeps every 2-D number out of this
folder until 02's clean encoder exists. `../../STATUS.md` restates each row with its file and rigor mark.

## How to read their paths

The copies use the path prefixes defined in `README.md` section 0. In this seed they resolve to repositories at named
commits, not to a laptop:

| prefix in the copies | means here |
|---|---|
| `ssn:` and bare `docs/`, `tools/`, `slurm/`, `SchwingNet/` | the private repository `spinesurg-ct-nnunet`, branch `L6_Class`, commit 097933a (`../../MANIFEST_CODE.md`) |
| `sn:` | `SchwingNet/` inside that repository (private; this folder holds reader E's results under `../../results/reader_e/`, never its classifier) |
| `ctsp:` and bare `scripts/`, `morphometrics/`, `paper/mpda/`, `zenodo/` | the public repository `CTSpinoPelvic1K`, `master`, 7ddfe38 (`../../MANIFEST_CODE.md`); its `morphometrics/` tables are copied in `../../results/morphometrics/` |
| `ostk:` | the public repository `OpenSpineToolkit`, `main`, cb43197 (`../../MANIFEST_CODE.md`) |
| `bth:` | the private repository `OpenSpineConsortium/beethoven` (not this folder's; see 11) |
| `students:` | `Student_Projects/` of `CTSpinoPelvic1K` |
| `np:`, `Desktop/` | loose laptop folders at the time of the handoff; what was worth keeping is in a project folder of this seed (`../../results/nextpaper/`, `../../code/ldi/`, `../../docs/external/` here) and `../../../_plan/DISPOSITION.tsv` says which |
| `context/`, `mem:` | the memory notes; this folder's 25 are in `../../memory/` with their `INDEX.md` status on line 1, the rest in the owning folders |
| `~`, `$HOME` | the grid HOME `/wsu/home/go/go24/go2432` (a student's own `~` is different: `RECIPES.md` section 0 item 9) |
| `$RS` | the grid Ceph volume `/rs/rs_grp_oschome/go2432` |
| `<laptop Desktop>/`, `<laptop home>/`, `<laptop memory folder>/`, `<laptop vendor folder, never read>`, `<laptop Temp scratchpad, swept>/` | markers that replace the absolute laptop paths the originals spelled out (the task's self-containment rule); `../../MANIFEST_LOCAL.md` section 2 counts the substitutions per file |

## What was changed in the copies

- Absolute laptop paths were replaced by the markers above on 2026-10-08: 17 substitutions, 8 in `README.md` (the six
  Desktop prefixes of the section 0 table at lines 34, 36-38, 40-41; the live memory folder at line 42; the vendor folder at
  line 241), 4 in `RESULTS_CATALOG.md` (the three prefix definitions at lines 12-14; the Temp scratchpad path of row F.48 at
  line 637), 3 in `INFRASTRUCTURE.md` (lines 5, 114, 380), 2 in `RECIPES.md` (the WSL mount path at line 29; the Desktop root
  at line 77); none in the other four. `OPEN_QUESTIONS.md` rows E10 and F2 name the laptop's temporary scratchpad in words,
  not by path, and are unchanged; nothing in this folder depends on it.
- One account username (not Greg's) in `INFRASTRUCTURE.md` was replaced by `<username withheld>` at the copy.
- Nothing else: the texts, numbers, ids and line numbers are the originals'. `INFRASTRUCTURE.md` section 9 (credentials)
  had already been moved out of the handoff before the copy; the section is a pointer.

## Two citations the copies carry that this folder corrects

- `RESULTS_CATALOG.md` F.7 cites the 155,093,558 returned voxels to the docstring of `scripts/merge_s1_into_sacrum.py`;
  the number is printed at run time (line 115) and is in no tracked file of CTSpinoPelvic1K 7ddfe38. `../../STATUS.md` F.7
  names the run and the log folder.
- `OPEN_QUESTIONS.md` D5 (221 against 222 degenerate S1 carves) is settled in `../../STATUS.md` F.5: a comparison operator
  and one record at exactly 0.500. The row stays in the copy; `../../TODO.md` step 22 carries the upstream edit.

## Institutional addresses that remain

`hpc@wayne.edu` (the grid's support desk) and `IRBQuestions@wayne.edu` (the IRB office) are institutional service
addresses and stay. No researcher's or student's address, name or username is in these copies; Greg's grid login is the
one every grid path already carries.
