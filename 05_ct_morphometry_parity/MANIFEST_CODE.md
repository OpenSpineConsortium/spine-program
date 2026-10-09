# MANIFEST_CODE.md: the code repositories this project uses

Nothing that lives in a repository at a named commit is copied into this folder; it is referenced here. Commits were read
from the laptop clones on 2026-10-08 (`git rev-parse HEAD`). Line numbers are as read at those commits.

| repository | URL | branch | commit | visibility |
|---|---|---|---|---|
| CTSpinoPelvic1K | https://github.com/OpenSpineConsortium/CTSpinoPelvic1K (remote `osc`, the one the paper cites) and https://github.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K (remote `origin`) | `master` | 7ddfe38 (working tree had uncommitted edits in `CAMERA_READY_NEURIPS/`, `.gitignore`, `paper/mpda/CTSpinoPelvic1K_reprint_check.pdf`; none in `morphometrics/` or `scripts/`) | public |
| OpenSpineToolkit (ostk) | https://github.com/OpenSpineConsortium/OpenSpineToolkit (`osc`) and https://github.com/Gregory-Schwing-MD-PhD/OpenSpineToolkit (`origin`) | `main` | cb43197 (2026-09-25) | public |
| spinesurg-ct-nnunet | https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet | `L6_Class` | 097933a | private; stays private (SchwingNet and level identification) |
| openspineconsortium.github.io | https://github.com/OpenSpineConsortium/openspineconsortium.github.io | `master` | local clone at c1800f8 (2026-10-02), behind `origin` by 10 commits (a17ea39, 2026-10-07): pull before editing | public |
| XRSpinoPelvic1K | private GitHub repository `XRSpinoPelvic1K` | `main` | 4f22935 | private; no file of this project lives there; its lateral render bank (`xrsp1k`, end-plate corners) is a PAR-2 input owned by 08 |

## CTSpinoPelvic1K at 7ddfe38: the files that matter

| path | what it is for here |
|---|---|
| `scripts/test_morphometric_separability.py` | the T12-vs-L1 shape test (AUC 0.990 within patient; F.28). PAR-1 is a copy that drops the five case-median features and keeps the six ratios |
| `scripts/six_lumbar_readings.py`, `scripts/shift_hypothesis_test.py` | the 18 six-lumbar spines and the seven-level shape model on the 643 ordinary records (the report prints 643; the docstring says 644) |
| `scripts/extract_surgical_morphometrics.py` (commit 2232bde for the released numbers) | the spinopelvic angles, canal depth (`_canal_column`, `_canal_ap`), pedicle width, end-plate width, crest, lordosis -> `surgical_morphometrics.csv` |
| `scripts/extract_level_gradients.py` | per-level heights, widths, process span -> `level_gradients.csv` (bit-for-bit identical across v10 and v11) |
| `scripts/extract_pelvic_shape.py`, `extract_transition_morphometrics.py`, `extract_degenerative.py`, `extract_opportunistic.py`, `extract_proximal_femur.py` | the five extractors whose outputs must be recomputed on v11 (F.44); `extract_proximal_femur.py` needs about 220 GB RAM at 8 workers (`docs/handoff/RECIPES.md` section 9) |
| `scripts/measure_sacral_ala.py`, `scripts/measure_tp_height.py`, `scripts/label_scheme.py` | the Castellvi screen inputs (`sacral_ala.csv`, `tp_height.csv`); the shipped-scheme constants (`SACRUM_ID = 26`, rib bases 33 / 46, lumbar ribs 60 / 61) |
| `scripts/height_probe.py`, `scripts/edge_probe.py`, `scripts/render_height.py` | the body-height investigation (F.35): estimator comparison, label edge against CT intensity, renders |
| `scripts/compare_v10_v11_spinopelvic.py`, `scripts/audit_s1_carve.py`, `scripts/merge_s1_into_sacrum.py`, `scripts/check_s1_merge.py` | the S1 carve audit and the v11 merge (F.5-F.7) |
| `scripts/sweep_foramina_params.py` | the refuted sacral-foramina count (F.39) |
| `scripts/demo_pelvic_width_dimorphism.py`, `results/pelvic_width/report.txt` | the student pelvic-width demo; the report is stale (F.45) |
| `scripts/make_measure_diagrams.py` | generates `figures/measure_diagrams/` |
| `scripts/select_anchor_cases.py`, `scripts/make_fig_anchors.py`, `scripts/render_anchors.py` | Figure 2 of the article; the retired check on identifier 29 lived in `select_anchor_cases.py` |
| `scripts/check_release_invariants.py`, `scripts/qc_rib_vertebra_incidence.py` | the release gates that stop the chain before any extractor runs |
| `scripts/compare_ctspine1k_pathcsv.py` | made `results/morphometrics/ctspine1k_pathcsv_agreement.csv` (F.2) |
| `scripts/spineps_ct_pipeline.py` | produces the SPINEPS subregion mask with the vertebral corpus as its own class (CT-5's input) |
| `morphometrics/make_reference_table.py` | writes `level_references.csv` (365 rows); Panjabi 1991 Table 3 values since commit 83f7f95 (copied here under `results/morphometrics/`) |
| `paper/mpda/make_levelatlas_fig.py` | Figure 3 of the article; also writes `morphometrics/level_atlas.csv` (L5 withheld for end-plate and pedicle width) |
| `paper/mpda/audit_ms.py`, `audit_artifacts.py`, `REPRODUCE.md` | every number in the text against its CSV; every artefact regenerated; the reproduction guide (its section 0 still says v10 and its section 2 still says the Panjabi values were digitised: stale) |
| `paper/mpda/main.tex` | the dataset article (Medical Physics); the spinopelvic table and Figure 3 |
| `paper/clinical/main.tex` | the iliac-crest clinical draft (v5-era numbers; recompute on v11 before use; owned by 09) |
| `slurm/level_gradients.sh`, `morphometrics.sh`, `pelvic_shape.sh`, `degenerative.sh`, `opportunistic.sh`, `proximal_femur.sh`, `finalize_release.sh` | the batch wrappers; they still point at `data/v5_final` and `-q primary`: edit before reuse |
| `docs/SPINOPELVIC_ESTIMATOR.md`, `LEVEL_MORPHOMETRY.md`, `OSTK_VS_EXTRACTION.md`, `BODY_HEIGHT_INVESTIGATION.md` | copied here under `docs/` |
| `docs/CASTELLVI_SCREEN_BLIND_SPOT.md`, `docs/LAB_JOURNAL.md`, `docs/ANCHOR_ORDINAL_DESIGN.md`, `docs/COUNTING_PRIOR_ART.md`, `docs/NEXT_PAPER_REFERENCES.md`, `docs/RELEASE_CHECKLIST.md` | the screen's blind spot (F.40), the negative results, the anchor-ordinal design (CT-7), the counting prior art, the reference list behind `level_references.csv` |
| `results/six_lumbar_readings/report.txt`, `.png` | F.27 |
| `CLAUDE.md` | the project's own working context (the traps restated in this folder's `CLAUDE.md`) |

## OpenSpineToolkit at cb43197: the files that matter

| path | what it is for here |
|---|---|
| `ostk/labels.py` | `detect_scheme` (line 106), `labels_for` (line 135): decides v4 vs v10/v11 on pelvis voxel mass; raises `SchemeError` when close; returns the default silently when no pelvis exists. `LABELS_V10` still maps `"S1": 29` (line 64; G.3) |
| `ostk/spine.py` | `endplate_from_label(..., "S1", ...)` falls back to the whole sacrum on a v11 volume with no flag (lines 473-474; G.3) |
| `ostk/vertebral_body.py` | `canal_mask` (line 98): the 1b7005c ring closing and `min_vox = 20` (G.2); `body_mask_by_canal` |
| `ostk/morphometry.py` | `canal_dimensions` (line 151), `pedicle_widths` (line 256, opt-in, four recorded failures), `level_morphometry` (line 380; VBHa, VBHp, EPWu, EPWl, EPDu, EPDl, SCW, SCD, PDW) |
| `ostk/metrics.py`, `ostk/metrics2d.py` | plausibility gates with their sources; the 2-D port of the spinopelvic angles (reproduces the 3-D angles on identical geometry) |
| `ostk/cobb.py` | lordosis (the comparator for `code/ldi/`) |
| `ostk/surgery.py` | post-operative synthesis (labels only; G.5) |
| `tests/` | 94 test functions; `test_labels.py` covers scheme detection; `python -m pytest` at cb43197 gives 1 failed, 100 passed (`tests/test_cobb.py::test_cobb_falls_back_gracefully_without_femurs`, cause not investigated; `OPEN_QUESTIONS.md` F18) |
| commits | 90a27a7 (the committed `ostk_level_morphometry.csv`, before the regression); 1b7005c 2026-09-10 22:52 (the regression); ba82e1a (six-point vertebral morphometry); cb43197 (head) |

## spinesurg-ct-nnunet at 097933a: the files that matter (private)

| path | what it is for here |
|---|---|
| `SchwingNet/tools/reader_e_features.py` (v3 at 65609fd), `reader_e_j0_collect.py`, `reader_e_j1_pairs.py`, `reader_e_j1_readback.py`, `reader_e_j2_gate.py` (805331b), `reader_e_diag_corners.py`, `reader_e_render_corners.py`, `reader_e_ranges.json`, `reader_e_ranges_build.py` | reader E: the feature extractor over five mask families, the pair list, the J2 spread gate, the corner renders that exposed the regression |
| `SchwingNet/slurm/reader_e_j0.sh`, `reader_e_j1.sh`, `reader_e_j1_list.sh`, `reader_e_j1_rerun.sh`, `reader_e_j2.sh`, `reader_e_collect.sh`, `reader_e_check_0097.sh`, `reader_e_diag_corners.sh`, `reader_e_render_corners.sh`; `SchwingNet/slurm/rc_read.sh` | the grid jobs (shard plan: 3,524 pairs at median 34.5 s); `rc_read.sh` is the pattern to copy (`reqp --qos=requeue`, `-D`, Ceph logs, `.part` + `os.replace`) |
| `SchwingNet/results/reader_e/` | copied here under `results/reader_e/` (all but the 40 MB `features_j1.csv`) |
| `SchwingNet/results/fig6/frozen/auto_truth.csv` | the G3 split sides (`g3_side`); the test transitional persons that J3 must assert out |
| `tools/spineps_ids.py` (`assert_verse_monotonic` line 394, `check_ids` 256) | the id guard every SPINEPS mask passes |
| `tools/eval_gate.py` | every quoted score passes through it |
| `tools/pelvis_landmarks.py` | pelvic-incidence landmarks on real radiographs (the 2-D side of CT-2's angles) |
| `tools/plan_postop.py` | the post-operative CT synthesis plan around `ostk.surgery` |
| `tools/polypose/measure_sagittal.py` (`measure_image`) | PI / LL measured through the release plate fits (the old ostk-primitive path read PI 3.6 / LL -8.9 on PIR case 0874, truth 53 / 54; G.7) |
| `tools/make_drr_dataset.py`, `tools/render_physics_drr.py`, `tools/render_drr_overlay.py` | the renderers PAR-2 extends (`project_labels` keeps the overlap count; no bank projects pedicle, canal, process, rib facet or S1 plate today) |
| `docs/CT_LSTV_CLASSIFIER_PLAN.md` | the reader E / J0-J3 plan (section 4 feature table, section 8 J0, the J3 rule) |
| `docs/ruleclass/MORPH_API.md` | the 3-D feature inventory with SPINEPS subregion ids (section 6.2) and the facet-angle probe (6.3) |
| `docs/LSTV_BENCHMARK.md` | where F.28 is also recorded |
| `slurm/tp_morphology.sh`, `versefusion_qc.sh`, `versefusion_tl_morphometrics.sh` | the VerSeFusion measurement jobs that read `vf_v10` |
| `slurm/polypose_check.sh` lines 37-38 | the PYTHONPATH pattern that makes ostk importable on the grid |
| `HANDOFF/RESEARCH_DIRECTIONS.md` sections 1.3, 3.1-3.9, 4 (CT-1 to CT-11), 6; `HANDOFF/MANUSCRIPTS.md` sections 6 and 11 | Greg-only files; extracted into `STATUS.md` and `TODO.md` with their ids |

## openspineconsortium.github.io: the files that matter

| path | what it is for here |
|---|---|
| `atlas/level_atlas.csv` | the public per-level atlas (47 data rows on the website copy against 49 in the repository's `morphometrics/level_atlas.csv`, counted 2026-10-08; which rows differ is not checked) |
| `atlas/build_table.py`, `atlas/index.html` | the page carries no hand-typed number; the table is rendered from the CSV |
