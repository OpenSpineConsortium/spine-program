# Prefix key for the handoff copies in this folder

The files under `docs/handoff/` are the handoff of 2026-10-08 (`spinesurg-ct-nnunet` 097933a `HANDOFF/`), copied
whole with three kinds of change recorded in `MANIFEST_LOCAL.md`: laptop paths replaced by the tokens below, e-mail
addresses withheld, and student names, a second grid username and reader initials withheld. The files' own prefix
tables (`README.md` section 0; the "Roots" paragraph of `literature_state/topic1_bibliography.md`; the key tables of
`LITERATURE_STATE.md` and `RESEARCH_DIRECTIONS.md`) still apply; this key says what each prefix now resolves to, so
that nothing in this folder depends on a laptop path.

| prefix or token in the copies | resolves to |
|---|---|
| `ssn:`, `S/`, `sscn/`, `[SSN]`, `<spinesurg-ct-nnunet 097933a>` | the private repository `spinesurg-ct-nnunet`, branch `L6_Class`, commit 097933a (`MANIFEST_CODE.md`) |
| `sn:` | `SchwingNet/` inside that repository (private; nothing of it is copied here) |
| `ctsp:`, `C/`, `ctsp/`, `[CTSP]`, `<CTSpinoPelvic1K 7ddfe38>` | the public repository `CTSpinoPelvic1K`, branch `master`, commit 7ddfe38 (`MANIFEST_CODE.md`); its untracked and gitignored files are recorded in `MANIFEST_LOCAL.md` |
| `ostk:`, `ostk/`, `[OSTK]`, `<OpenSpineToolkit cb43197>` | the public repository `OpenSpineToolkit`, branch `main`, commit cb43197 |
| `<XRSpinoPelvic1K 4f22935>` | the private repository `XRSpinoPelvic1K`, branch `main`, commit 4f22935 (not used by this project) |
| `bth:`, `<OpenSpineConsortium/beethoven 2f90319>` | the private repository `OpenSpineConsortium/beethoven` at 2f90319 (see `11_students_grid_access`) |
| `students:` | `Student_Projects/` inside `CTSpinoPelvic1K` (a nested public repository; see `11_students_grid_access`) |
| `np:`, `<laptop NextPaper folder; see MANIFEST_LOCAL.md>` | a laptop folder with no single repository; what matters from it is in `03_ctspinopelvic1k_dataset` and `05_ct_morphometry_parity` |
| `Desktop/`, `<laptop Desktop root; see MANIFEST_LOCAL.md>` | the laptop's Desktop root; files kept by path are recorded in the owning folder's `MANIFEST_LOCAL.md` and in `_plan/ROOT_FILES.md`, `_plan/EXCLUDED.md` |
| `<laptop home; see MANIFEST_LOCAL.md>`, `<laptop scratchpad; see MANIFEST_LOCAL.md>`, `<laptop WSL home; see MANIFEST_LOCAL.md>` | laptop-only locations (home, the Claude scratchpad, the WSL home); nothing here depends on them; the WSL home holds the review corpora this folder references (`MANIFEST_GRID.md` "Not on the grid") |
| `context/`, `mem:`, `memory/`, `[MEM]`, `M/`, `<the memory folder; ...>` | the memory notes: the ones this project carries are in `memory/`; the status of every note is `docs/handoff/context/INDEX.md`; the notes carried by other projects are in their `memory/` folders |
| `~`, `$HOME` | the grid HOME `/wsu/home/go/go24/go2432` |
| `$RS` | the grid Ceph volume `/rs/rs_grp_oschome/go2432` |
| `$RC` | `/rs/rs_grp_oschome/go2432/ruleclass` |
| `D` (in `RECIPES.md` section 9) | `/wsu/home/go/go24/go2432/data/CTSpinoPelvic1K`, now a symlink to `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` (`MANIFEST_GRID.md`) |
| `GREG_ONLY/` | `HANDOFF/GREG_ONLY/` inside `spinesurg-ct-nnunet` at 097933a: never copied into `spine-program`; referenced by path from `01_carm_level_detection` and `_plan/EXCLUDED.md` |
| T1 to T6 | the six reader notes in `docs/handoff/working_notes/` |
| CAT-, OQ-, MAN-, RIG-, LEAK-, DIR-, PLAN-, G0 to G7, B00 to B14 | identifier namespaces, defined in `docs/handoff/README.md` section 0 |

Bare paths without a prefix follow `docs/handoff/README.md` section 0: `docs/`, `tools/`, `slurm/`, `paper/rsnai/`,
`paper/qi_universal_protocol/` mean `spinesurg-ct-nnunet`; `paper/mpda/`, `scripts/`, `morphometrics/`, `zenodo/` mean
`CTSpinoPelvic1K`.
