# code/

Three groups of scripts are copied here in the final pass of 2026-10-08, after the critic found that `../../_plan/PLAN.md`
section 3 ("08, Families absorbed") promised nine scripts in this folder while the disposition rows ssn r132, r133 and
r150 marked them "reference" and the first build followed the disposition. The plan wins: the copies are below, the
repository stays the source of truth, and `../MANIFEST_CODE.md` names every other script by path and commit.

## `ssn_097933a/` : nine tracked scripts of spinesurg-ct-nnunet at 097933a (branch `L6_Class`, private)

| file | bytes | role |
|---|---:|---|
| `tools/render_physics_drr.py` | 18,934 | the physics renderer behind `physics_drr` and `physics_rare` |
| `tools/make_drr_dataset.py` | 28,297 | the bank builder (`--paths2-only` after the no-bone sweep defect) |
| `tools/spine_project.py` | 10,988 | the projection of labels through a geometry (the coverage render of 02 step 1 uses the same idea) |
| `tools/device_fit.py` | 120,524 | the nine-term device card fit |
| `tools/device_style.py` | 28,809 | one styled frame = one copula draw; `SPREAD = 0.2`, `SAMPLE_MODE` from `DEVICE_SAMPLE_MODE`, default `clip` |
| `tools/device_spread_sweep.py` | 11,447 | the spread sweep |
| `tools/deepfluoro_calibrate.py` | 25,461 | the DeepFluoro calibration entry point (the other 22 `deepfluoro_*.py` stay in the repository) |
| `tools/polypose_sample.py` | 89,612 | the PolyPose generator |
| `tools/polypose_warp.py` | 19,690 | the forward polyrigid warp |

Byte-identical to the repository files (sha1 recorded in `../MANIFEST_LOCAL.md`, "Final pass"). Edit them in the
repository, never here; a copy that drifts from 097933a is a trap.

## `ssn_untracked_2026-10-08/` : the two laptop-only files that no commit holds

`tools/polypose/cine_render.py` (104,995 B, 2026-09-26) and its job script `slurm/polypose_cine.sh` (7,237 B,
2026-09-26) were untracked in the working tree at 097933a (`git status`, 2026-10-08) and are not on the grid checkout
(4e3fe93). They pair with `../results/polypose/rom_cine.json`. `../TODO.md` step 2 commits all three; until then this
folder is the only copy outside the laptop.

## `spinesurg_ct_0051074/` : the March-April 2026 sacralisation-synthesis line (SpineSurg-CT at 0051074)

`src/augmentation/sacralization_synthesis.py`, `src/utils/augmentation_qc.py`, `src/utils/pelvic_alignment_qc.py`,
`src/utils/pelvic_grid_panel.py` and `slurm/run_augmentation_qc.sh`, tracked in
https://github.com/Gregory-Schwing-MD-PhD/SpineSurg-CT at 0051074 (2026-04-09, the nested clone
`SpineSurg-CT/SpineSurg-CT/` on the laptop). This was the first attempt in the programme to synthesise a transitional
vertebra from a normal mask: the ancestor of CTSpinoPelvic1K-Syn (project 06) and of the PolyPose and
morphology-synthesis work here (`../docs/research_notes/`, `MORPHOLOGY_SYNTHESIS_PRIOR_ART.md`). Its only QC result,
`augmentation_quality_report.csv` and `augmentation_quality_summary.txt` (laptop-only, outside the nested clone), is in
`../results/superseded/sacralization_synthesis_2026-04/`. Superseded; kept so nobody rebuilds it from scratch and so the
lineage of the synthesis idea is on record. Label ids in these scripts are the 2026-04 scheme, not v11: never run them
against the release without `ostk.labels.labels_for(volume)`.

Everything else this project runs (`tools/ts_to_drr.py`, `devcorpus_build.py`, `devcorpus_train.py`, the 22 other
`deepfluoro_*.py`, `tools/polypose/` and the 127 job scripts under `slurm/`) is in spinesurg-ct-nnunet at 097933a and is
listed in `../MANIFEST_CODE.md`.
