# The handoff copies in this folder, and what their path prefixes mean here

The eight files beside this note (`README.md`, `GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`, `DATASET_USAGE.md`,
`LEAKAGE.md`, `OPEN_QUESTIONS.md`, `INFRASTRUCTURE.md`) and `working_notes/topic2_scaling_samples_anomaly_power.md` are
whole copies of the student-readable handoff written on 2026-10-08 in the `HANDOFF/` folder of the spinesurg-ct-nnunet
repository at commit 097933a (`../../MANIFEST_CODE.md`). They are copied into every project folder of `spine-program`
by rule 3 of `../../../_plan/PLAN.md` section 2, so that a reader with one folder has the catalog, the recipes and the
open questions. Two edits were made to the copies: one Hugging Face username was withheld, and laptop folder paths were
replaced by the placeholders below (`../../MANIFEST_LOCAL.md` records both).

The handoff files define short prefixes for paths. In this folder they resolve to repositories and commits, never to a
laptop:

| prefix in the handoff | resolves to |
|---|---|
| `ssn:` | the spinesurg-ct-nnunet repository, branch `L6_Class`, commit 097933a |
| `sn:` | `SchwingNet/` inside that repository |
| `ctsp:` | the CTSpinoPelvic1K repository, `master`, commit 7ddfe38 |
| `ostk:` | the OpenSpineToolkit repository, `main`, commit cb43197 |
| `xrsp:` | the XRSpinoPelvic1K repository, `main`, commit 4f22935 (private; project 07) |
| `dp:` | `data_platform/` inside spinesurg-ct-nnunet (project 10) |
| `bth:` | the OpenSpineConsortium/beethoven repository (project 11) |
| `mem:` or `context/` | a memory note; the ones that bind this project are in `../../memory/` with their status; the full status index is `../../memory/HANDOFF_CONTEXT_INDEX.md` |
| `~` | the grid HOME `/wsu/home/go/go24/go2432` |
| `$RS` | the grid Ceph volume `/rs/rs_grp_oschome/go2432` |
| `<spinesurg-ct-nnunet repository at 097933a>/`, `<CTSpinoPelvic1K repository at 7ddfe38>/`, `<OpenSpineToolkit repository at cb43197>/` | a laptop checkout path in the original, rewritten to the repository |
| `<laptop Desktop>/`, `<laptop home>/`, `<session scratchpad, not kept>`, `<live memory folder; copies in memory/>/` | other laptop locations in the original; nothing in this folder depends on them |

`HANDOFF/GREG_ONLY/`, `MANUSCRIPTS.md`, `CONTEXT_EXPORT.md`, `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md` and the other
`working_notes/` are Greg-only and are not copied into this student-safe folder; the sections of them that bear on this
project are extracted with their ids into `../../STATUS.md` and `../../TODO.md` (RESEARCH_DIRECTIONS CT-3, CT-4, CT-8,
CT-9, FLU-1; LITERATURE_STATE sections 1.2, 2B and 5; RESULTS_CATALOG Part D and A16.6-A16.8 are in the catalog here).


Final pass of 2026-10-08: `working_notes/topic2_scaling_samples_anomaly_power.md` was removed from this folder (Greg-only under PLAN.md rule 3); it lives whole in `../../../01_carm_level_detection/docs/handoff/working_notes/` and in spinesurg-ct-nnunet 097933a `HANDOFF/working_notes/`. References to it in the copied handoff files above are to that location.
