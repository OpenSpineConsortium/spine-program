# PREFIXES — where the handoff's path prefixes point when read from this folder

Written 2026-10-08 for `03_ctspinopelvic1k_dataset` (the second pass). The copied HANDOFF files (`README.md` section 0,
`RESULTS_CATALOG.md` "Path prefixes", `working_notes/topic6_...` section 0) define their prefixes as folders on Greg's
laptop. This table resolves each one to a repository at the commit named in `../../MANIFEST_CODE.md`, to a path inside
this folder, or to a grid path from `../../MANIFEST_GRID.md`. A reader with this folder, grid access and the repositories
needs nothing else; the laptop paths that remain in copied files are listed in `../../MANIFEST_LOCAL.md` section 3.6.

## 1. Repository prefixes

| prefix (also written) | the handoff defines it as | read it as | what of it is in this folder |
|---|---|---|---|
| `ssn:` (`sscn/`, `[SSN]`, `S/`) | the laptop checkout `Desktop/spinesurg-ct-nnunet/` | the private repository https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch `L6_Class`, commit 097933a (`MANIFEST_CODE.md` section 2); the grid checkout `/wsu/home/go/go24/go2432/spinesurg-ct-nnunet` is at 4e3fe93 and cannot fetch the remote | `ssn:HANDOFF/{README,GLOSSARY,RECIPES,RESULTS_CATALOG,DATASET_USAGE,LEAKAGE,OPEN_QUESTIONS,INFRASTRUCTURE}.md` -> this folder (`docs/handoff/`); `ssn:HANDOFF/working_notes/topic6_...` -> `working_notes/`; `ssn:HANDOFF/context/<note>.md` -> `../../memory/<note>.md` for the 55 notes `../../MEMORY.md` lists; `ssn:benchmark/` -> `../../code/benchmark/`; `ssn:scripts/` -> `../../code/spinesurg_scripts/`; `ssn:containers/build_container.sh`, `ssn:docker/Dockerfile` -> `../../code/containers/`, `../../code/docker/`; `ssn:docs/{BENCHMARK_PROTOCOL,COMPETITOR_BENCHMARK,ablations,xrsp1k_seg}.md`, `ssn:data/README.md` -> `../../docs/spinesurg_ct_nnunet/`. Everything else (`tools/`, `slurm/`, `docs/ruleclass/`, `docs/grid_records/`, `data_platform/`) stays in the repository |
| `sn:` | `ssn:SchwingNet/` | the SchwingNet folder of the same private repository: project 01, Greg-only | nothing; no file of it was copied here |
| `ctsp:` (`ctsp/`, `[CTSP]`, `C/`; bare `paper/mpda/`, `scripts/`, `morphometrics/`, `zenodo/`) | the laptop checkout `Desktop/CTSpinoPelvic1K-1/` | the public repository https://github.com/OpenSpineConsortium/CTSpinoPelvic1K (`osc`, the copy the article cites) and https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K (`origin`), branch `master`, commit 7ddfe38 (`MANIFEST_CODE.md` section 1); the grid checkout `/wsu/home/go/go24/go2432/CTSpinoPelvic1K` is behind, at a0c5139 | `ctsp:paper/mpda/` -> `../../manuscripts/mpda/` (text, scripts, figures, PDFs; `_others/`, `_schehr/`, `_upd/` by reference); `ctsp:CAMERA_READY_NEURIPS/` -> `../../manuscripts/neurips_camera_ready/` (the working tree of 2026-09-27, not the commit); `ctsp:paper/cns2026/` -> `../../manuscripts/talks/cns2026/`; `ctsp:docs/` -> `../../docs/ctsp/`; the root `README.md`, `CLAUDE.md`, `STATUS.md`, `REVIEWERS_*.md`, `CITATION.cff`, `LICENSE`, `NOTICE`, `Makefile`, `pyproject.toml`, `requirements.txt`, `ci.yml` -> `../../docs/ctsp_root/`; `ctsp:zenodo/{README,KNOWN_ISSUES,hf_dataset_card}.md` and `ctsp:data/zenodo_deposit/{manifest.json,splits_5fold.json,dataset_labels.json,SHA256SUMS.txt,KNOWN_ISSUES.md}` -> `../../docs/release/`; `ctsp:results/`, `hardware_review/`, `qc_final/`, `qc_hardware/` -> `../../results/`; `ctsp:Lumbosac.csv` and the root QC tables -> `../../results/root_qc_tables/`; `ctsp:_review_0816/`, `_verify_0816/`, `thoracic_fix/` -> `../../code/case_fixes/`. `ctsp:scripts/`, `morphometrics/`, `slurm/`, `zenodo/*.py`, `tests/`, `review_service/` stay in the repository |
| `ostk:` (`ostk/`, `[OSTK]`) | the laptop checkout `Desktop/OpenSpineToolkit/` | https://github.com/OpenSpineConsortium/OpenSpineToolkit (`osc`) and https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit (`origin`), branch `main`, commit cb43197 (`MANIFEST_CODE.md` section 3); grid copy `/wsu/home/go/go24/go2432/OpenSpineToolkit` | nothing; project 04 owns it |
| `students:` (`students/`, `templates/`) | `ctsp:Student_Projects/` | the nested repository https://github.com/OpenSpineConsortium/Student_Projects, head 3f1cf04 (whether pushed is not verified, `OPEN_QUESTIONS.md` A25) | nothing; project 11 owns it, and its board names students |
| `bth:` (`bth/`) | the laptop folder `Desktop/ashley-bridge/` (Beethoven) | the Beethoven repositories of project 11 (`11_students_grid_access/MANIFEST_CODE.md`) | nothing; no file here depends on it |
| `np:` | the laptop folder `Desktop/NextPaper/` | not a repository; its parts resolve one by one: `np:AR/` -> `../../manuscripts/nextpaper_ar_2026-09-08/`; `np:RadAI/` -> `../../manuscripts/nextpaper_radai/`; `np:manifest.csv`, `ACRIN-6664_protocol.pdf`, the TCIA polyp table -> `../../results/nextpaper/`; `np:flip18_review/` -> `../../results/flip18_review/` (forms and renders; the volumes were not copied); `np:spinopelvic-seg/` -> https://github.com/OpenSpineConsortium/spinopelvic-seg, `main`, c105981 (`MANIFEST_CODE.md` section 4); `np:VerSeFusion/` -> https://github.com/Gregory-Schwing-MD-PhD/VerSeFusion, `master`, 2b21cc4 (section 5); `np:bibm-spinopelvic/` -> project 05, not here | as listed |
| `Desktop/` | the laptop's desktop folder | not one place; the parts this folder absorbed: `Desktop/NeurIPS/{bm,ens,pred,audit}/` -> `../../results/neurips_2026-05/`; `Desktop/NeurIPS/lstv_review/` -> `../../code/lstv_review_tool/`; `Desktop/NeurIPS/Lumbosac_Castelvii_Class.csv` -> not copied (`MANIFEST_LOCAL.md` section 4; the IIIb 19 sheet, stale); `Desktop/CTSpinoPelvic1K_submission/` -> `../../manuscripts/mpda_as_submitted_2026-09-07/`; `Desktop/openspineconsortium.github.io/` -> project 12; `Desktop/private_ip`, `Desktop/ERAS_2026` -> excluded by rule (personal); everything else named with this prefix is in `MANIFEST_LOCAL.md` sections 1 and 4 | as listed |

**Repository tags of the topic-6 working note** (its section 0 table): `[CTSP]` = `ctsp:`; `[OSTK]` = `ostk:`; `[SSN]` =
`ssn:`; `[SEG]` = spinopelvic-seg at c105981; `[SEGM]` = its MLHC-anonymised twin `anonymous-mlhc/spinopelvic-seg`
(master 91b7e9e; not referenced by anything current); `[AR]` = `np:AR/` -> `../../manuscripts/nextpaper_ar_2026-09-08/`;
`[BIBM]` = `np:bibm-spinopelvic/` (project 05); `[WEB]` = the website repository (project 12); `[MEM]` = the live memory
folder, see section 2.

## 2. Memory, grid and laptop-only prefixes

| prefix (also written) | the handoff defines it as | read it as |
|---|---|---|
| `context/`, `mem:`, `memory/`, `[MEM]`, `M/` | `ssn:HANDOFF/context/` (the redacted copies of the session's memory notes) or the live memory folder on the laptop | `../../memory/<note>.md` for the 55 notes `../../MEMORY.md` lists, each carrying its 2026-10-08 status line; a note not among the 55 is in `ssn:HANDOFF/context/` (private repository) and was judged not to bear on this project |
| `~`, `$HOME` | go2432's grid home | `/wsu/home/go/go24/go2432` (write it in full: a student's `~` is different) |
| `$RS` | the grid Ceph volume | `/rs/rs_grp_oschome/go2432` |
| `$RC` | `$RS/ruleclass` | `/rs/rs_grp_oschome/go2432/ruleclass` (project 06; `RECIPES.md` and `INFRASTRUCTURE.md` only) |
| `D` (`RECIPES.md` section 9) | `~/data/CTSpinoPelvic1K` | `/rs/rs_grp_oschome/go2432/data/ctspinopelvic1k/converted/CTSpinoPelvic1K` (`MANIFEST_GRID.md` section 1; `~/data/CTSpinoPelvic1K` is a symlink to it since the B02 cut-over of 2026-10-08) |
| `Temp` scratchpads (the session scratchpad folders under the laptop's local Temp) | session folders on Greg's laptop | laptop only, Greg's; nothing of them is here. The NeurIPS recomputation scripts named in `RESULTS_CATALOG.md` F.48 live only there (`../../TODO.md` step 2 b) |
| `model_night/sweep_v3` (a laptop mirror of `~/model_night/sweep_v3`) | the sweep records behind the CNS talk's level chart | project 01, Greg-only data; `manuscripts/talks/cns2026/sweep_per_level.py` reads it through its `MIRROR` constant |
| `/mnt/c/...` | the WSL spelling of a laptop path | the same folder as the `C:` spelling; resolve it by the rows above |
| T1-T6 | the six working notes | only T6 is here (`working_notes/topic6_ctspinopelvic1k_and_toolkit.md`); T1-T5 are Greg-only in `ssn:HANDOFF/working_notes/` |

Citation keys inside the handoff files (`RESULTS_CATALOG.md` ids such as F.14 and C5.1; `OPEN_QUESTIONS.md` rows such as
A30 and E7) are unchanged by the copy and are the ids `../../STATUS.md` and `../../TODO.md` cite.


Final pass of 2026-10-08: `working_notes/topic6_ctspinopelvic1k_and_toolkit.md` was removed from this folder (Greg-only under PLAN.md rule 3); it lives whole in `../../../01_carm_level_detection/docs/handoff/working_notes/` and in spinesurg-ct-nnunet 097933a `HANDOFF/working_notes/`. References to it in the copied handoff files above are to that location.
