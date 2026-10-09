# About the handoff copies in this folder

The eight files beside this note (`README.md`, `GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`, `DATASET_USAGE.md`,
`LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md`) are the student-readable half of the handoff written on
2026-10-08 in `HANDOFF/` of the private repository `spinesurg-ct-nnunet` at commit 097933a. Every project folder of this
seed carries the same eight (`_plan/PLAN.md` section 2 rule 3), so a reader with one folder has the results catalog, the
recipes and the open questions. `EXTRACT_MANUSCRIPTS_12.md` is the one section of a Greg-only handoff file that bears on
this project. The remaining handoff files are Greg-only and are not in this folder.

## How to read their paths

The copies use the path prefixes defined in `README.md` section 0. In this seed they resolve to repositories, not to a
laptop:

| prefix in the copies | means here |
|---|---|
| `ssn:` and bare `docs/`, `tools/`, `slurm/`, `service/` | the private repository `spinesurg-ct-nnunet`, branch `L6_Class`, commit 097933a (`MANIFEST_CODE.md` section 3) |
| `sn:` | `SchwingNet/` inside that repository (private; nothing of it is in this folder) |
| `ctsp:` and bare `paper/mpda/`, `scripts/`, `morphometrics/`, `zenodo/` | the public repository `CTSpinoPelvic1K`, `master`, 7ddfe38 (`MANIFEST_CODE.md` section 4) |
| `ostk:` | the public repository `OpenSpineToolkit`, `main`, cb43197 (`MANIFEST_CODE.md` section 2) |
| `bth:` | the private repository `OpenSpineConsortium/beethoven` (`MANIFEST_CODE.md` section 6) |
| `students:` | `Student_Projects/` of `CTSpinoPelvic1K` |
| `np:`, `Desktop/` | loose laptop folders at the time of the handoff; whatever of them was worth keeping is in a project folder of this seed, and `_plan/DISPOSITION.tsv` says which |
| `context/`, `mem:` | the memory notes; this folder's 27 are in `memory/`, the rest in the owning folders |
| `~`, `$HOME` | the grid HOME `/wsu/home/go/go24/go2432` |
| `$RS` | the grid Ceph volume `/rs/rs_grp_oschome/go2432` |
| `<laptop Desktop>/`, `<laptop home>/`, `<laptop memory folder>/`, `<laptop vendor folder, never read>`, `<laptop Temp scratchpad, swept>/` | markers that replace the absolute laptop paths the originals spelled out (the task's self-containment rule); `MANIFEST_LOCAL.md` section 2 counts the substitutions per file |

## What was changed in the copies

- Absolute laptop paths were replaced by the markers above: 19 substitutions, 8 in `README.md` (lines 34, 36-38, 40-42,
  241), 3 in `RECIPES.md` (line 29; line 77 twice, the second pass reducing a marker that still carried the laptop's
  sync-folder name to `<laptop Desktop>`), 5 in `RESULTS_CATALOG.md` (lines 12-14; line 637 twice, the second pass reducing the whole
  scratchpad path to `<laptop Temp scratchpad, swept>/neurips_fixes/cr_apply/`), 3 in `INFRASTRUCTURE.md` (lines 5,
  114, 380); none in the other four. `MANIFEST_LOCAL.md` section 2 carries the same counts.
- One C&IT administrator's username in `INFRASTRUCTURE.md` section 2 was replaced by the role.
- Five phrases that cited a CV through its application system (three in `OPEN_QUESTIONS.md` row A1, including its file
  column, which now reads "a CV in an application folder (laptop only, never copied)"; one in `README.md` section 7; one
  in `RECIPES.md` section 0) now say "a CV" or "an application folder". No application folder is named anywhere in this
  folder. Lines that name another study only to say it is a different project and outside the handoff stay as they are.
- Nothing else: the texts, numbers and ids are the originals'. `INFRASTRUCTURE.md` section 9 (credentials) had already
  been moved out of the handoff before the copy; the section is a pointer.

## Institutional addresses that remain

`hpc@wayne.edu` (the grid's support desk) and `IRBQuestions@wayne.edu` (the IRB office) are institutional service
addresses and stay. No researcher's or student's address, name or username is in these copies.
