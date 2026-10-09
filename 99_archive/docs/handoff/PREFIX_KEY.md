# Prefix key for the handoff copies in this folder

The eight files beside this note (`README.md`, `GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`, `DATASET_USAGE.md`,
`LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md`) are whole, unedited copies of the student-readable handoff
written on 2026-10-08 in `HANDOFF/` of spinesurg-ct-nnunet at 097933a (`../../MANIFEST_CODE.md`), copied into every
project folder by rule 3 of `../../../_plan/PLAN.md` section 2. Their own prefix tables (`README.md` section 0, lines
34-42; `RESULTS_CATALOG.md` lines 12-14; `INFRASTRUCTURE.md` line 5; `RECIPES.md` lines 29 and 76-77) spell the laptop
roots of 2026-10-08 (drive-letter paths of one laptop). Those spellings are history. In this repository every prefix resolves
to a repository at a commit or to a grid path, as below, and nothing in this folder depends on a laptop. The other
places a laptop root is spelled in the eight copies (`RESULTS_CATALOG.md` line 637, `INFRASTRUCTURE.md` line 114,
`OPEN_QUESTIONS.md` lines 143 and 161) are listed in `../../MANIFEST_LOCAL.md` section 3.

| prefix or token in the copies | resolves to |
|---|---|
| `ssn:`, `sscn/`, `[SSN]`, `S/` | the private repository spinesurg-ct-nnunet, branch `L6_Class`, commit 097933a (`../../MANIFEST_CODE.md`) |
| `sn:` | `SchwingNet/` inside that repository (private; nothing of it is copied here) |
| `ctsp:`, `ctsp/`, `[CTSP]`, `C/` | the public repository CTSpinoPelvic1K, branch `master`, commit 7ddfe38 (`../../MANIFEST_CODE.md`); its untracked files that this folder copied are in `../../MANIFEST_LOCAL.md` section 1 |
| `ostk:`, `ostk/`, `[OSTK]` | the public repository OpenSpineToolkit, branch `main`, commit cb43197 |
| `xrsp:` | the private repository XRSpinoPelvic1K, branch `main`, commit 4f22935 |
| `bth:`, `bth/` | the private repository OpenSpineConsortium/beethoven (owned by `11_students_grid_access`) |
| `students:`, `students/` | `Student_Projects/` inside CTSpinoPelvic1K (owned by 11) |
| `np:` | the laptop folder NextPaper, which has no repository; what this folder took from it is `docs/early_scratch_2026-05/` (`../../MANIFEST_LOCAL.md` section 1) |
| `Desktop/` | the laptop Desktop root; files kept by path are in `../../MANIFEST_LOCAL.md` section 2 and in `../../../_plan/ROOT_FILES.md` and `EXCLUDED.md` |
| `context/`, `mem:`, `memory/`, `[MEM]`, `M/` | the memory notes; the ones this folder carries are in `../../memory/`, each with its `HANDOFF/context/INDEX.md` status on the first line (`../../MEMORY.md`); the live memory folder named in `README.md` line 42 is laptop-only and never copied |
| the Temp scratchpad (`RESULTS_CATALOG.md` line 637; `RECIPES.md` line 76; `OPEN_QUESTIONS.md` F2) | a laptop-only temporary folder that is swept; the NeurIPS recomputation scripts it held are open question F2, owned by `03_ctspinopelvic1k_dataset`; nothing here depends on it |
| `[laptop session folder of the day]`, `[laptop scratchpad of the day]`, `[laptop home of the day]` (in `../checkpoints/`) | the same laptop-only locations, tokenised on copy (`../../MANIFEST_LOCAL.md` section 3) |
| `~`, `$HOME` | the grid HOME `/wsu/home/go/go24/go2432` |
| `$RS` | the grid Ceph volume `/rs/rs_grp_oschome/go2432` |
| `$RC` | `/rs/rs_grp_oschome/go2432/ruleclass` |
| `D` (`RECIPES.md` section 9) | `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K`, batch B06 VERIFIED to `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` (GRIDLS line 2063 in `10_data_platform_grid/docs/grid_read_2026-10-08/grid_ls_2026-10-08.out`); whether the HOME path is now a link is `10_data_platform_grid/MANIFEST_GRID.md` |
| `GREG_ONLY/` | `HANDOFF/GREG_ONLY/` in spinesurg-ct-nnunet at 097933a: never copied into spine-program; the sections assigned to this folder are restated in `GREG_ONLY_SECTION_EXTRACTS.md` beside this file |
| row ids `ssn rNN`, `carm rNN`, `ctsp rNN`, `desk rNN`, `inv3 rNN`, `mem rNN`, `grid rNN` | rows of `../../../_plan/DISPOSITION.tsv` and of the seven inventory TSVs in `../../../_plan/inventories/` (row N = TSV row N counted from 1 after the header; `../../../_plan/inventories/README.md`) |
| the identifier namespaces (catalog rows A to F, OQ, MAN, DD, G0 to G7, B00 to B14, T1 to T6) | defined in `README.md` section 0 beside this file |

Bare paths without a prefix follow `README.md` section 0: `docs/`, `tools/`, `slurm/`, `paper/rsnai/`,
`paper/qi_universal_protocol/`, `data_platform/` mean spinesurg-ct-nnunet; `paper/mpda/`, `scripts/`, `morphometrics/`,
`zenodo/`, `CAMERA_READY_NEURIPS/` mean CTSpinoPelvic1K.

This key is this folder's. On 2026-10-08 folders 06 and 09 carry their own versions (`README_PREFIXES.md`, `PREFIX_KEY.md`),
05 and 12 an `ABOUT_THESE_COPIES.md`, and the others none; one shared text for all thirteen is `../../TODO.md` step 16.
