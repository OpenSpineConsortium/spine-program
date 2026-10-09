# MANIFEST_LOCAL — every file copied into this folder, where it came from, and what was left out

Written 2026-10-08 by the build of project 03 from the disposition rows of `../_plan/DISPOSITION.tsv` with
`project_folder = 03_ctspinopelvic1k_dataset` (169 rows: 93 copy, 64 reference, 12 exclude). No separate copy or
redaction log exists on disk: this file is the record. Section 3.6 records the second pass of 2026-10-08 (the
verifier's nine findings).

**This record is history, not a dependency.** The laptop paths below say where each copy came from on
2026-10-08. Nothing in this folder needs them: a file either sits here, or in a repository at the commit named in
`MANIFEST_CODE.md`, or on the grid at a path in `MANIFEST_GRID.md`. Of the eight documents written for this folder
(`CLAUDE.md`, `README.md`, `MEMORY.md`, `STATUS.md`, `TODO.md`, `MANIFEST_GRID.md`, `MANIFEST_CODE.md` and this
file) only this one carries laptop paths; the copied notes, HANDOFF files and scripts that still quote one are listed
in section 3.6 with the line to change, and `docs/handoff/PREFIXES.md` resolves every path prefix the copied HANDOFF
files use. Prefixes: `ctsp:` = `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/` (the public
CTSpinoPelvic1K repository, master 7ddfe38, working tree); `ssn:` = `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/`
(private, L6_Class 097933a); `HANDOFF/context/` = `ssn:HANDOFF/context/` (the redacted memory copies);
`Desktop/` = `C:/Users/grego/OneDrive/Desktop/`.

## 0. Totals

| what | number |
|---|---|
| files copied and present | 1020 |
| bytes on disk (after redaction) | 133,268,961 |
| files the copy rules skipped at the source (section 2) | 151 |
| files deleted after copy (section 3) | 6 |
| files edited after copy for redaction (section 3) | 13 (10 in the build, 3 in the second pass: section 3.2) |
| files given a prefix pointer line or a laptop-path header in the second pass (section 3.6) | 32 (10 + 22) |
| files written for this folder in the second pass | 1 (`docs/handoff/PREFIXES.md`) |
| files in which the banned word was rewritten (section 3) | 13 |
| code files given a source header (section 3) | 50 |
| memory notes given a status line | 55 |

The copy rules applied (the task's list): never imaging data (`.nii`, `.nii.gz`, `.dcm`, `.npz`, `.npy`, `.h5`,
`.mha`, large png sets, zips of data), model weights, anything under `.git`, environments, caches, logs over 2 MB,
any file over 25 MB, credential or token files, LaTeX build intermediates (`.aux`, `.bbl`, `.blg`, `.fls`,
`.fdb_latexmk`; the `.log` and `.out` files were kept on purpose, see below), personal or administrative material,
student names and usernames, researcher and personal e-mail addresses; symbolic links and junctions never
followed. One zip was allowed by name: `LaTeX_source_CTSpinoPelvic1K.zip` (the as-submitted TeX source, 863,471 B).

**LaTeX `.log` and `.out` files were kept on purpose**: 11 `.log` and 6 `.out`, every one under 40 KB
(`manuscripts/mpda/{main,reprint_check,supplementary,title_page,tp,fig_pipeline_standalone}.log`, the five
`manuscripts/neurips_camera_ready/src/latexmk_*.log` and `neurips_2026.log`, `manuscripts/nextpaper_ar_2026-09-08/neurips_2026.log`,
`manuscripts/nextpaper_radai/main.log`; `.out` beside `main`, `reprint_check`, `supplementary`, `title_page`, `neurips_2026` twice
and `nextpaper_radai/main`), plus three small non-LaTeX logs (`code/case_fixes/_review_0816/_sym.log` 543 B,
`manuscripts/nextpaper_ar_2026-09-08/build.log` 51 B, `results/neurips_2026-05/ens/eval.log` 15,765 B). The `.log` is the whole
build output that the page-limit trap in `CLAUDE.md` says to read: `manuscripts/mpda/reprint_check.log` line 795 is the
LaTeX page total of the reprint build (`build.sh` line 84 prints its own `PAGES:` count from the PDF), and the five
`latexmk_*.log` are the only record of the camera-ready builds of 25-27 September. The `.out` files are hyperref
bookmark lists (two are empty) and were kept with their logs.

## 1. Files copied, by destination

Each row: destination (relative to this folder), source on 2026-10-08, size in bytes, and any post-copy edit.
A row marked **redacted** was edited as section 3 says; **word** means the banned word was rewritten; **header**
means a source header was prepended.

### `code/benchmark/` (69 files, 2,391,451 B)

| destination | source | bytes | note |
|---|---|---|---|
| `code/benchmark/README.md` | `ssn:benchmark/README.md` | 4,297 |  |
| `code/benchmark/architecture_figure.py` | `ssn:benchmark/architecture_figure.py` | 6,453 | **header** |
| `code/benchmark/capability_matrix.py` | `ssn:benchmark/capability_matrix.py` | 4,812 | **header** |
| `code/benchmark/cases.csv` | `ssn:benchmark/cases.csv` | 184,114 |  |
| `code/benchmark/collect.py` | `ssn:benchmark/collect.py` | 4,167 | **header** |
| `code/benchmark/data/bench/gt/score/summary.json` | `ssn:benchmark/data/bench/gt/score/summary.json` | 2,508 |  |
| `code/benchmark/data/latency_v100.json` | `ssn:benchmark/data/latency_v100.json` | 2,182 |  |
| `code/benchmark/data/model_registry.csv` | `ssn:benchmark/data/model_registry.csv` | 36,504 |  |
| `code/benchmark/data/model_registry.md` | `ssn:benchmark/data/model_registry.md` | 17,540 |  |
| `code/benchmark/data/patch_context_summary.json` | `ssn:benchmark/data/patch_context_summary.json` | 960 |  |
| `code/benchmark/data/robustness/all2_aug2_rung_0.json` | `ssn:benchmark/data/robustness/all2_aug2_rung_0.json` | 5,420 |  |
| `code/benchmark/data/robustness/all2_aug2_rung_2.json` | `ssn:benchmark/data/robustness/all2_aug2_rung_2.json` | 5,492 |  |
| `code/benchmark/data/robustness/all2_aug3_rung_0.json` | `ssn:benchmark/data/robustness/all2_aug3_rung_0.json` | 5,466 |  |
| `code/benchmark/data/robustness/all2_aug3_rung_1.json` | `ssn:benchmark/data/robustness/all2_aug3_rung_1.json` | 5,369 |  |
| `code/benchmark/data/robustness/all2_aug3_rung_2.json` | `ssn:benchmark/data/robustness/all2_aug3_rung_2.json` | 5,493 |  |
| `code/benchmark/data/robustness/all2_base_rung_0.json` | `ssn:benchmark/data/robustness/all2_base_rung_0.json` | 5,396 |  |
| `code/benchmark/data/robustness/all2_base_rung_1.json` | `ssn:benchmark/data/robustness/all2_base_rung_1.json` | 5,482 |  |
| `code/benchmark/data/robustness/all2_base_rung_2.json` | `ssn:benchmark/data/robustness/all2_base_rung_2.json` | 5,435 |  |
| `code/benchmark/data/robustness/detector_robustness.json` | `ssn:benchmark/data/robustness/detector_robustness.json` | 3,350 |  |
| `code/benchmark/data/training_series.csv` | `ssn:benchmark/data/training_series.csv` | 27,889 |  |
| `code/benchmark/debug_split.py` | `ssn:benchmark/debug_split.py` | 4,222 | **header** |
| `code/benchmark/debug_split.sh` | `ssn:benchmark/debug_split.sh` | 991 | **header** |
| `code/benchmark/extract_training_series.py` | `ssn:benchmark/extract_training_series.py` | 4,001 | **header** |
| `code/benchmark/fetch_weights.sh` | `ssn:benchmark/fetch_weights.sh` | 2,104 | **header** |
| `code/benchmark/figs/fig_architecture.pdf` | `ssn:benchmark/figs/fig_architecture.pdf` | 23,036 |  |
| `code/benchmark/figs/fig_architecture.png` | `ssn:benchmark/figs/fig_architecture.png` | 190,755 |  |
| `code/benchmark/figs/fig_capabilities.pdf` | `ssn:benchmark/figs/fig_capabilities.pdf` | 20,060 |  |
| `code/benchmark/figs/fig_capabilities.png` | `ssn:benchmark/figs/fig_capabilities.png` | 109,408 |  |
| `code/benchmark/figs/fig_patch_context_0376.pdf` | `ssn:benchmark/figs/fig_patch_context_0376.pdf` | 29,583 |  |
| `code/benchmark/figs/fig_patch_context_0376.png` | `ssn:benchmark/figs/fig_patch_context_0376.png` | 161,941 |  |
| `code/benchmark/figs/fig_pipeline_oneshot.pdf` | `ssn:benchmark/figs/fig_pipeline_oneshot.pdf` | 41,948 |  |
| `code/benchmark/figs/fig_pipeline_oneshot.png` | `ssn:benchmark/figs/fig_pipeline_oneshot.png` | 150,219 |  |
| `code/benchmark/figs/fig_training.pdf` | `ssn:benchmark/figs/fig_training.pdf` | 27,798 |  |
| `code/benchmark/figs/fig_training.png` | `ssn:benchmark/figs/fig_training.png` | 169,326 |  |
| `code/benchmark/figs/level_heatmap.png` | `ssn:benchmark/figs/level_heatmap.png` | 438,391 |  |
| `code/benchmark/figs/level_heatmap_faults.png` | `ssn:benchmark/figs/level_heatmap_faults.png` | 348,590 |  |
| `code/benchmark/figs/smoke/fig_bench_count.pdf` | `ssn:benchmark/figs/smoke/fig_bench_count.pdf` | 13,670 |  |
| `code/benchmark/figs/smoke/fig_bench_count.png` | `ssn:benchmark/figs/smoke/fig_bench_count.png` | 32,989 |  |
| `code/benchmark/figs/smoke/fig_bench_dice.pdf` | `ssn:benchmark/figs/smoke/fig_bench_dice.pdf` | 14,789 |  |
| `code/benchmark/figs/smoke/fig_bench_dice.png` | `ssn:benchmark/figs/smoke/fig_bench_dice.png` | 57,362 |  |
| `code/benchmark/figs/smoke/fig_bench_rare.pdf` | `ssn:benchmark/figs/smoke/fig_bench_rare.pdf` | 13,160 |  |
| `code/benchmark/figs/smoke/fig_bench_rare.png` | `ssn:benchmark/figs/smoke/fig_bench_rare.png` | 34,727 |  |
| `code/benchmark/figs/smoke/fig_bench_ribs.pdf` | `ssn:benchmark/figs/smoke/fig_bench_ribs.pdf` | 13,947 |  |
| `code/benchmark/figs/smoke/fig_bench_ribs.png` | `ssn:benchmark/figs/smoke/fig_bench_ribs.png` | 38,814 |  |
| `code/benchmark/figs/tab_capabilities.tex` | `ssn:benchmark/figs/tab_capabilities.tex` | 1,190 |  |
| `code/benchmark/install_envs.sh` | `ssn:benchmark/install_envs.sh` | 2,796 | **header** |
| `code/benchmark/make_case_table.py` | `ssn:benchmark/make_case_table.py` | 3,700 | **header** |
| `code/benchmark/make_figures.py` | `ssn:benchmark/make_figures.py` | 7,936 | **header** |
| `code/benchmark/mappings/spineps.json` | `ssn:benchmark/mappings/spineps.json` | 766 |  |
| `code/benchmark/mappings/totalsegmentator.json` | `ssn:benchmark/mappings/totalsegmentator.json` | 1,540 |  |
| `code/benchmark/mappings/vista3d.json` | `ssn:benchmark/mappings/vista3d.json` | 971 |  |
| `code/benchmark/patch_context.py` | `ssn:benchmark/patch_context.py` | 12,180 | **header** |
| `code/benchmark/patch_context.sh` | `ssn:benchmark/patch_context.sh` | 1,333 | **header** |
| `code/benchmark/pipeline_figure.py` | `ssn:benchmark/pipeline_figure.py` | 4,151 | **header** |
| `code/benchmark/plot_training.py` | `ssn:benchmark/plot_training.py` | 5,494 | **header** |
| `code/benchmark/run_spineps.sh` | `ssn:benchmark/run_spineps.sh` | 2,969 | **header** |
| `code/benchmark/run_spineps_cases.py` | `ssn:benchmark/run_spineps_cases.py` | 7,428 | **header** |
| `code/benchmark/run_spineps_patched.py` | `ssn:benchmark/run_spineps_patched.py` | 4,154 | **header** |
| `code/benchmark/run_spineps_retry.py` | `ssn:benchmark/run_spineps_retry.py` | 12,693 | **header** |
| `code/benchmark/run_spineps_ribs.py` | `ssn:benchmark/run_spineps_ribs.py` | 8,868 | **header** |
| `code/benchmark/run_spineps_ribs.sh` | `ssn:benchmark/run_spineps_ribs.sh` | 2,299 | **header** |
| `code/benchmark/run_totalsegmentator.sh` | `ssn:benchmark/run_totalsegmentator.sh` | 3,320 | **header** |
| `code/benchmark/run_ts_cases.py` | `ssn:benchmark/run_ts_cases.py` | 3,436 | **header** |
| `code/benchmark/run_vista3d.sh` | `ssn:benchmark/run_vista3d.sh` | 3,331 | **header** |
| `code/benchmark/score.sh` | `ssn:benchmark/score.sh` | 4,152 | **header** |
| `code/benchmark/spineps_cc3d_patched.py` | `ssn:benchmark/spineps_cc3d_patched.py` | 4,563 | **header** |
| `code/benchmark/spineps_to_oneshot.py` | `ssn:benchmark/spineps_to_oneshot.py` | 5,321 | **header** |
| `code/benchmark/test_decoder.sh` | `ssn:benchmark/test_decoder.sh` | 1,636 | **header** |
| `code/benchmark/to_oneshot.py` | `ssn:benchmark/to_oneshot.py` | 5,064 | **header** |

### `code/case_fixes/` (56 files, 10,721,643 B)

| destination | source | bytes | note |
|---|---|---|---|
| `code/case_fixes/_review_0816/0816_completion_report.json` | `ctsp:_review_0816/0816_completion_report.json` | 1,533 |  |
| `code/case_fixes/_review_0816/0816_ribs_qc.json` | `ctsp:_review_0816/0816_ribs_qc.json` | 472 |  |
| `code/case_fixes/_review_0816/_sym.log` | `ctsp:_review_0816/_sym.log` | 543 |  |
| `code/case_fixes/_review_0816/itksnap_s1_review.txt` | `ctsp:_review_0816/itksnap_s1_review.txt` | 5,255 |  |
| `code/case_fixes/_review_0816/itksnap_v6_labels.txt` | `ctsp:_review_0816/itksnap_v6_labels.txt` | 5,421 |  |
| `code/case_fixes/_review_0816/recarve_s1.py` | `ctsp:_review_0816/recarve_s1.py` | 5,770 | **header** |
| `code/case_fixes/_review_0816/recarve_s1_sym.py` | `ctsp:_review_0816/recarve_s1_sym.py` | 6,068 | **header** |
| `code/case_fixes/_verify_0816/analyse_0816_hardware.py` | `ctsp:_verify_0816/analyse_0816_hardware.py` | 4,495 | **header** |
| `code/case_fixes/_verify_0816/discriminate_0816.py` | `ctsp:_verify_0816/discriminate_0816.py` | 3,874 | **header** |
| `code/case_fixes/_verify_0816/fragments_0816.py` | `ctsp:_verify_0816/fragments_0816.py` | 4,084 | **header** |
| `code/case_fixes/_verify_0816/itksnap_v6_labels_ignore_hidden.txt` | `ctsp:_verify_0816/itksnap_v6_labels_ignore_hidden.txt` | 5,318 |  |
| `code/case_fixes/_verify_0816/look_native_0816.py` | `ctsp:_verify_0816/look_native_0816.py` | 3,402 | **header** |
| `code/case_fixes/_verify_0816/render_0816.py` | `ctsp:_verify_0816/render_0816.py` | 3,589 | **header** |
| `code/case_fixes/_verify_0816/renders/comp1_1.png` | `ctsp:_verify_0816/renders/comp1_1.png` | 899,274 |  |
| `code/case_fixes/_verify_0816/renders/comp2_2.png` | `ctsp:_verify_0816/renders/comp2_2.png` | 882,800 |  |
| `code/case_fixes/_verify_0816/renders/mip_all.png` | `ctsp:_verify_0816/renders/mip_all.png` | 688,702 |  |
| `code/case_fixes/_verify_0816/renders/native_ax_series.png` | `ctsp:_verify_0816/renders/native_ax_series.png` | 422,410 |  |
| `code/case_fixes/_verify_0816/renders/native_cor_sweep.png` | `ctsp:_verify_0816/renders/native_cor_sweep.png` | 462,095 |  |
| `code/case_fixes/_verify_0816/renders/native_sag_sweep.png` | `ctsp:_verify_0816/renders/native_sag_sweep.png` | 174,548 |  |
| `code/case_fixes/_verify_0816/renders/shape3d.png` | `ctsp:_verify_0816/renders/shape3d.png` | 167,787 |  |
| `code/case_fixes/_verify_0816/renders/zoom_lumbar.png` | `ctsp:_verify_0816/renders/zoom_lumbar.png` | 828,040 |  |
| `code/case_fixes/_verify_0816/shape3d_0816.py` | `ctsp:_verify_0816/shape3d_0816.py` | 3,435 | **header** |
| `code/case_fixes/_verify_0816/test_grouping_0816.py` | `ctsp:_verify_0816/test_grouping_0816.py` | 3,130 | **header** |
| `code/case_fixes/_verify_0816/va/_panel4.png` | `ctsp:_verify_0816/va/_panel4.png` | 615,248 |  |
| `code/case_fixes/_verify_0816/va/panels/0068_v5.png` | `ctsp:_verify_0816/va/panels/0068_v5.png` | 418,402 |  |
| `code/case_fixes/_verify_0816/va/panels/0068_v6.png` | `ctsp:_verify_0816/va/panels/0068_v6.png` | 439,703 |  |
| `code/case_fixes/_verify_0816/va/panels/0231_v4.png` | `ctsp:_verify_0816/va/panels/0231_v4.png` | 614,169 |  |
| `code/case_fixes/_verify_0816/va/panels/0231_v6.png` | `ctsp:_verify_0816/va/panels/0231_v6.png` | 624,275 |  |
| `code/case_fixes/_verify_0816/va/panels/markers.json` | `ctsp:_verify_0816/va/panels/markers.json` | 839 |  |
| `code/case_fixes/_verify_0816/va/panels/markers_0068.json` | `ctsp:_verify_0816/va/panels/markers_0068.json` | 835 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_13.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_13.png` | 11,356 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_15.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_15.png` | 70,242 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_2.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_2.png` | 104,351 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_21.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_21.png` | 37,627 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_23.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_23.png` | 40,515 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_25.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_25.png` | 69,289 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_27.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_27.png` | 14,172 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_32.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_32.png` | 116,342 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_5.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_5.png` | 84,625 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_6.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_6.png` | 697,201 |  |
| `code/case_fixes/_verify_0816/va/pptx_imgs/Picture_7.png` | `ctsp:_verify_0816/va/pptx_imgs/Picture_7.png` | 126,584 |  |
| `code/case_fixes/_verify_0816/va/render_0068_panels.py` | `ctsp:_verify_0816/va/render_0068_panels.py` | 4,117 | **header** |
| `code/case_fixes/_verify_0816/va/render_0231_panels.py` | `ctsp:_verify_0816/va/render_0231_panels.py` | 4,650 | **header** |
| `code/case_fixes/_verify_0816/va/spine_qc.py` | `ctsp:_verify_0816/va/spine_qc.py` | 1,083 | **header** |
| `code/case_fixes/_verify_0816/va/spine_qc_0068.py` | `ctsp:_verify_0816/va/spine_qc_0068.py` | 1,145 | **header** |
| `code/case_fixes/_verify_0816/va/visual_abstract.pdf` | `ctsp:_verify_0816/va/visual_abstract.pdf` | 734,374 |  |
| `code/case_fixes/_verify_0816/va/visual_abstract.png` | `ctsp:_verify_0816/va/visual_abstract.png` | 1,281,992 |  |
| `code/case_fixes/_verify_0816/va/visual_abstract.py` | `ctsp:_verify_0816/va/visual_abstract.py` | 16,486 | **header** |
| `code/case_fixes/thoracic_fix_0068/0068_hardware.json` | `ctsp:thoracic_fix/0068/0068_hardware.json` | 822 |  |
| `code/case_fixes/thoracic_fix_0068/0068_label_v6_mixing.json` | `ctsp:thoracic_fix/0068/0068_label_v6_mixing.json` | 802 |  |
| `code/case_fixes/thoracic_fix_0068/0068_renumber.json` | `ctsp:thoracic_fix/0068/0068_renumber.json` | 359 |  |
| `code/case_fixes/thoracic_fix_0068/0068_thoracic.json` | `ctsp:thoracic_fix/0068/0068_thoracic.json` | 907 |  |
| `code/case_fixes/thoracic_fix_0068/hu2500/0068_hardware.json` | `ctsp:thoracic_fix/0068/hu2500/0068_hardware.json` | 824 |  |
| `code/case_fixes/thoracic_fix_0068/hu2500b/0068_hardware.json` | `ctsp:thoracic_fix/0068/hu2500b/0068_hardware.json` | 994 |  |
| `code/case_fixes/thoracic_fix_0068/hu3000/0068_hardware.json` | `ctsp:thoracic_fix/0068/hu3000/0068_hardware.json` | 821 |  |
| `code/case_fixes/thoracic_fix_0068/itksnap_v5_labels.txt` | `ctsp:thoracic_fix/0068/itksnap_v5_labels.txt` | 4,447 |  |

### `code/containers/` (1 files, 4,360 B)

| destination | source | bytes | note |
|---|---|---|---|
| `code/containers/build_container.sh` | `ssn:containers/build_container.sh` | 4,360 | **header** |

### `code/docker/` (1 files, 4,927 B)

| destination | source | bytes | note |
|---|---|---|---|
| `code/docker/Dockerfile` | `ssn:docker/Dockerfile` | 4,927 |  |

### `code/lstv_review_tool/` (71 files, 843,852 B)

| destination | source | bytes | note |
|---|---|---|---|
| `code/lstv_review_tool/LSTVReviewer.py` | `Desktop/NeurIPS/lstv_review/lstv_review/LSTVReviewer.py` | 20,721 | **header** |
| `code/lstv_review_tool/LSTVReviewer_install_guide.pdf` | `Desktop/NeurIPS/lstv_review/lstv_review/LSTVReviewer_install_guide.pdf` | 7,676 |  |
| `code/lstv_review_tool/README.md` | `Desktop/NeurIPS/lstv_review/lstv_review/README.md` | 23,457 |  |
| `code/lstv_review_tool/ambiguous/token_4/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/ambiguous/token_4/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/ambiguous/token_4/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/ambiguous/token_4/review.txt` | 1,490 |  |
| `code/lstv_review_tool/ambiguous/token_67/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/ambiguous/token_67/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/ambiguous/token_67/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/ambiguous/token_67/review.txt` | 1,491 |  |
| `code/lstv_review_tool/lumb/token_149/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_149/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_149/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_149/review.txt` | 1,489 |  |
| `code/lstv_review_tool/lumb/token_167/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_167/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_167/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_167/review.txt` | 1,484 |  |
| `code/lstv_review_tool/lumb/token_175/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_175/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_175/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_175/review.txt` | 1,487 |  |
| `code/lstv_review_tool/lumb/token_189/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_189/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_189/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_189/review.txt` | 1,484 |  |
| `code/lstv_review_tool/lumb/token_215/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_215/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_215/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_215/review.txt` | 1,487 |  |
| `code/lstv_review_tool/lumb/token_261/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_261/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_261/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_261/review.txt` | 1,487 |  |
| `code/lstv_review_tool/lumb/token_267/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_267/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_267/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_267/review.txt` | 1,487 |  |
| `code/lstv_review_tool/lumb/token_344/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_344/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_344/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_344/review.txt` | 1,489 |  |
| `code/lstv_review_tool/lumb/token_401/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_401/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_401/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_401/review.txt` | 1,487 |  |
| `code/lstv_review_tool/lumb/token_587/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_587/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_587/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_587/review.txt` | 1,487 |  |
| `code/lstv_review_tool/lumb/token_666/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_666/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_666/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_666/review.txt` | 1,487 |  |
| `code/lstv_review_tool/lumb/token_672/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_672/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_672/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_672/review.txt` | 1,487 |  |
| `code/lstv_review_tool/lumb/token_699/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_699/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_699/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_699/review.txt` | 1,484 |  |
| `code/lstv_review_tool/lumb/token_737/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_737/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/lumb/token_737/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_737/review.txt` | 1,489 |  |
| `code/lstv_review_tool/manifest.csv` | `Desktop/NeurIPS/lstv_review/lstv_review/manifest.csv` | 4,423 |  |
| `code/lstv_review_tool/module/LSTVReviewer.py` | `Desktop/NeurIPS/lstv_review/lstv_review/module/LSTVReviewer.py` | 21,847 | **header** |
| `code/lstv_review_tool/sacr_count/token_104/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_104/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_104/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_104/review.txt` | 1,493 |  |
| `code/lstv_review_tool/sacr_count/token_107/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_107/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_107/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_107/review.txt` | 1,490 |  |
| `code/lstv_review_tool/sacr_count/token_110/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_110/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_110/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_110/review.txt` | 1,493 |  |
| `code/lstv_review_tool/sacr_count/token_537/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_537/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_537/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_537/review.txt` | 1,493 |  |
| `code/lstv_review_tool/sacr_count/token_554/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_554/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_554/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_554/review.txt` | 1,493 |  |
| `code/lstv_review_tool/sacr_count/token_555/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_555/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_555/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_555/review.txt` | 1,493 |  |
| `code/lstv_review_tool/sacr_count/token_615/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_615/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_615/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_615/review.txt` | 1,490 |  |
| `code/lstv_review_tool/sacr_count/token_64/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_64/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_64/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_64/review.txt` | 1,494 |  |
| `code/lstv_review_tool/sacr_count/token_721/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_721/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacr_count/token_721/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_721/review.txt` | 1,493 |  |
| `code/lstv_review_tool/sacralization/token_123/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_123/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacralization/token_123/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_123/review.txt` | 1,496 |  |
| `code/lstv_review_tool/sacralization/token_125/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_125/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacralization/token_125/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_125/review.txt` | 1,493 |  |
| `code/lstv_review_tool/sacralization/token_140/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_140/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacralization/token_140/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_140/review.txt` | 1,499 |  |
| `code/lstv_review_tool/sacralization/token_15/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_15/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacralization/token_15/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_15/review.txt` | 1,495 |  |
| `code/lstv_review_tool/sacralization/token_32/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_32/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacralization/token_32/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_32/review.txt` | 1,492 |  |
| `code/lstv_review_tool/sacralization/token_6/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_6/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/sacralization/token_6/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_6/review.txt` | 1,494 |  |
| `code/lstv_review_tool/semisacralization/token_120/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/semisacralization/token_120/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/semisacralization/token_120/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/semisacralization/token_120/review.txt` | 1,500 |  |
| `code/lstv_review_tool/semisacralization/token_22/landmarks_template.mrk.json` | `Desktop/NeurIPS/lstv_review/lstv_review/semisacralization/token_22/landmarks_template.mrk.json` | 21,713 |  |
| `code/lstv_review_tool/semisacralization/token_22/review.txt` | `Desktop/NeurIPS/lstv_review/lstv_review/semisacralization/token_22/review.txt` | 1,502 |  |

### `code/spinesurg_scripts/` (5 files, 32,294 B)

| destination | source | bytes | note |
|---|---|---|---|
| `code/spinesurg_scripts/_env_probe.sh` | `ssn:scripts/_env_probe.sh` | 1,146 | **header** |
| `code/spinesurg_scripts/build_and_push.sh` | `ssn:scripts/build_and_push.sh` | 4,025 | **header** |
| `code/spinesurg_scripts/download_dataset.py` | `ssn:scripts/download_dataset.py` | 5,187 | **header** |
| `code/spinesurg_scripts/export_env.sh` | `ssn:scripts/export_env.sh` | 3,242 | **header** |
| `code/spinesurg_scripts/generate_5fold_splits.py` | `ssn:scripts/generate_5fold_splits.py` | 18,694 | **header** |

### `docs/` (1 files, 150,247 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/LAB_JOURNAL_2026-08-19.pdf` | `ctsp:LAB_JOURNAL_2026-08-19.pdf` | 150,247 |  |

### `docs/ctsp/` (62 files, 3,951,655 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/ctsp/22_sagittal.png` | `ctsp:docs/22_sagittal.png` | 308,120 |  |
| `docs/ctsp/ANCHOR_ORDINAL_DESIGN.md` | `ctsp:docs/ANCHOR_ORDINAL_DESIGN.md` | 22,676 |  |
| `docs/ctsp/BODY_HEIGHT_INVESTIGATION.md` | `ctsp:docs/BODY_HEIGHT_INVESTIGATION.md` | 4,432 |  |
| `docs/ctsp/BUILD_CHAIN.md` | `ctsp:docs/BUILD_CHAIN.md` | 7,537 |  |
| `docs/ctsp/CASTELLVI_SCREEN_BLIND_SPOT.md` | `ctsp:docs/CASTELLVI_SCREEN_BLIND_SPOT.md` | 11,594 |  |
| `docs/ctsp/CLASSFIX_REVIEW.md` | `ctsp:docs/CLASSFIX_REVIEW.md` | 2,111 |  |
| `docs/ctsp/COLLABORATOR_TASKS.md` | `ctsp:docs/COLLABORATOR_TASKS.md` | 9,378 |  |
| `docs/ctsp/CORRECTIONS.md` | `ctsp:docs/CORRECTIONS.md` | 16,821 |  |
| `docs/ctsp/COUNTING_PRIOR_ART.md` | `ctsp:docs/COUNTING_PRIOR_ART.md` | 17,006 |  |
| `docs/ctsp/DATASETS_ROADMAP.md` | `ctsp:docs/DATASETS_ROADMAP.md` | 13,442 | **word** (2) |
| `docs/ctsp/DATASET_PRINCIPLES.md` | `ctsp:docs/DATASET_PRINCIPLES.md` | 4,484 |  |
| `docs/ctsp/DEFERRED_CASES.md` | `ctsp:docs/DEFERRED_CASES.md` | 8,361 |  |
| `docs/ctsp/EMAIL_CM_SPINE_REQUEST.md` | `ctsp:docs/EMAIL_CM_SPINE_REQUEST.md` | 5,006 | **redacted**: eleven researcher e-mail addresses in the author table and the three in the To / Cc lines withheld; author names and roles kept |
| `docs/ctsp/HARDWARE_CLASSES.md` | `ctsp:docs/HARDWARE_CLASSES.md` | 7,218 |  |
| `docs/ctsp/LABELING_GUIDE.md` | `ctsp:docs/LABELING_GUIDE.md` | 8,535 |  |
| `docs/ctsp/LAB_JOURNAL.md` | `ctsp:docs/LAB_JOURNAL.md` | 10,978 |  |
| `docs/ctsp/LEVEL_MORPHOMETRY.md` | `ctsp:docs/LEVEL_MORPHOMETRY.md` | 14,541 |  |
| `docs/ctsp/METHODS_REFERENCES.md` | `ctsp:docs/METHODS_REFERENCES.md` | 14,704 |  |
| `docs/ctsp/NEXT_PAPER_REFERENCES.md` | `ctsp:docs/NEXT_PAPER_REFERENCES.md` | 2,932 |  |
| `docs/ctsp/OSTK_VS_EXTRACTION.md` | `ctsp:docs/OSTK_VS_EXTRACTION.md` | 3,793 |  |
| `docs/ctsp/RELEASE_CHECKLIST.md` | `ctsp:docs/RELEASE_CHECKLIST.md` | 19,251 | **word** (1) |
| `docs/ctsp/REVIEW.md` | `ctsp:docs/REVIEW.md` | 10,263 |  |
| `docs/ctsp/RIB_ANCHOR_RATIONALE.md` | `ctsp:docs/RIB_ANCHOR_RATIONALE.md` | 6,185 |  |
| `docs/ctsp/RIB_ANCHOR_REVIEW_GUIDE.md` | `ctsp:docs/RIB_ANCHOR_REVIEW_GUIDE.md` | 5,793 |  |
| `docs/ctsp/RIB_REVIEW_GUIDE.md` | `ctsp:docs/RIB_REVIEW_GUIDE.md` | 12,137 |  |
| `docs/ctsp/ROADMAP.md` | `ctsp:docs/ROADMAP.md` | 8,867 |  |
| `docs/ctsp/SEGMENTATION_ARCHITECTURE.md` | `ctsp:docs/SEGMENTATION_ARCHITECTURE.md` | 11,260 |  |
| `docs/ctsp/SPINEPS_BENCHMARK.md` | `ctsp:docs/SPINEPS_BENCHMARK.md` | 5,610 |  |
| `docs/ctsp/SPINE_REVIEW.md` | `ctsp:docs/SPINE_REVIEW.md` | 8,975 |  |
| `docs/ctsp/SPINOPELVIC_ESTIMATOR.md` | `ctsp:docs/SPINOPELVIC_ESTIMATOR.md` | 18,145 |  |
| `docs/ctsp/STUDENT_ANNOTATION_PROTOCOL.md` | `ctsp:docs/STUDENT_ANNOTATION_PROTOCOL.md` | 7,718 |  |
| `docs/ctsp/VERSION_PROGRESSION.md` | `ctsp:docs/VERSION_PROGRESSION.md` | 3,549 |  |
| `docs/ctsp/annotation/README.md` | `ctsp:docs/annotation/README.md` | 5,071 |  |
| `docs/ctsp/annotation/figs/README.md` | `ctsp:docs/annotation/figs/README.md` | 715 |  |
| `docs/ctsp/annotation/iliolumbar.md` | `ctsp:docs/annotation/iliolumbar.md` | 3,481 |  |
| `docs/ctsp/annotation/ls_nerves.md` | `ctsp:docs/annotation/ls_nerves.md` | 4,156 |  |
| `docs/ctsp/annotation/ribs.md` | `ctsp:docs/annotation/ribs.md` | 3,185 |  |
| `docs/ctsp/castellvi_consensus.csv` | `ctsp:docs/castellvi_consensus.csv` | 1,851 | **redacted** (second pass): reader columns renamed `read_1_A`, `read_2_B` |
| `docs/ctsp/castellvi_readers_2026-09-04.csv` | `ctsp:docs/castellvi_readers_2026-09-04.csv` | 2,044 | **redacted**: reader initials and names replaced by A/B/C |
| `docs/ctsp/castellvi_reread_queue.csv` | `ctsp:docs/castellvi_reread_queue.csv` | 1,436 |  |
| `docs/ctsp/castellvi_type1_queue.csv` | `ctsp:docs/castellvi_type1_queue.csv` | 12,595 |  |
| `docs/ctsp/ctspine1k_corrections.csv` | `ctsp:docs/ctspine1k_corrections.csv` | 14,430 |  |
| `docs/ctsp/dataset_card.md` | `ctsp:docs/dataset_card.md` | 17,560 |  |
| `docs/ctsp/email_student_onboarding.md` | `ctsp:docs/email_student_onboarding.md` | 1,761 |  |
| `docs/ctsp/email_update.md` | `ctsp:docs/email_update.md` | 6,435 |  |
| `docs/ctsp/expert_reread_candidates.csv` | `ctsp:docs/expert_reread_candidates.csv` | 30,995 |  |
| `docs/ctsp/figures/0001_L3_height.png` | `ctsp:docs/figures/0001_L3_height.png` | 81,387 |  |
| `docs/ctsp/figures/0004_L1_height.png` | `ctsp:docs/figures/0004_L1_height.png` | 99,963 |  |
| `docs/ctsp/ids.txt` | `ctsp:docs/ids.txt` | 36 |  |
| `docs/ctsp/lstv_reread_queue.csv` | `ctsp:docs/lstv_reread_queue.csv` | 497 |  |
| `docs/ctsp/pipeline.md` | `ctsp:docs/pipeline.md` | 8,444 |  |
| `docs/ctsp/qc/fig2_anchors_aligned.png` | `ctsp:docs/qc/fig2_anchors_aligned.png` | 545,071 |  |
| `docs/ctsp/qc/fig2_rerender_0428_failure.png` | `ctsp:docs/qc/fig2_rerender_0428_failure.png` | 878,205 |  |
| `docs/ctsp/qc/fig3_hardware.png` | `ctsp:docs/qc/fig3_hardware.png` | 420,217 |  |
| `docs/ctsp/qc/fig4_validation.png` | `ctsp:docs/qc/fig4_validation.png` | 64,640 |  |
| `docs/ctsp/qc/s1_carve_0428_vs_0704.png` | `ctsp:docs/qc/s1_carve_0428_vs_0704.png` | 69,366 |  |
| `docs/ctsp/rib_review_example_0007_mislabel.png` | `ctsp:docs/rib_review_example_0007_mislabel.png` | 65,163 |  |
| `docs/ctsp/rib_review_example_0008_hyperplastic_TP.png` | `ctsp:docs/rib_review_example_0008_hyperplastic_TP.png` | 859,106 |  |
| `docs/ctsp/rib_review_example_0231_cage.png` | `ctsp:docs/rib_review_example_0231_cage.png` | 47,121 |  |
| `docs/ctsp/rib_review_example_0231_split.png` | `ctsp:docs/rib_review_example_0231_split.png` | 79,967 |  |
| `docs/ctsp/survey_protocol.md` | `ctsp:docs/survey_protocol.md` | 10,625 |  |
| `docs/ctsp/troubleshooting.md` | `ctsp:docs/troubleshooting.md` | 4,710 |  |

### `docs/ctsp_root/` (18 files, 155,781 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/ctsp_root/CITATION.cff` | `ctsp:CITATION.cff` | 1,187 |  |
| `docs/ctsp_root/CLAUDE.md` | `ctsp:CLAUDE.md` | 7,267 | **word** (1) |
| `docs/ctsp_root/LICENSE` | `ctsp:LICENSE` | 11,931 |  |
| `docs/ctsp_root/Makefile` | `ctsp:Makefile` | 42,398 |  |
| `docs/ctsp_root/NOTICE` | `ctsp:NOTICE` | 162 |  |
| `docs/ctsp_root/README.md` | `ctsp:README.md` | 26,180 |  |
| `docs/ctsp_root/REVIEWERS.md` | `ctsp:REVIEWERS.md` | 4,117 |  |
| `docs/ctsp_root/REVIEWERS_AI_EDITING.md` | `ctsp:REVIEWERS_AI_EDITING.md` | 7,827 |  |
| `docs/ctsp_root/REVIEWERS_CHEATSHEET.md` | `ctsp:REVIEWERS_CHEATSHEET.md` | 2,893 |  |
| `docs/ctsp_root/REVIEWERS_FIXING.md` | `ctsp:REVIEWERS_FIXING.md` | 9,488 |  |
| `docs/ctsp_root/REVIEWERS_LINUX.md` | `ctsp:REVIEWERS_LINUX.md` | 8,158 |  |
| `docs/ctsp_root/REVIEWERS_MAC.md` | `ctsp:REVIEWERS_MAC.md` | 6,656 |  |
| `docs/ctsp_root/REVIEWERS_WINDOWS.md` | `ctsp:REVIEWERS_WINDOWS.md` | 6,368 |  |
| `docs/ctsp_root/STATUS.md` | `ctsp:STATUS.md` | 6,168 |  |
| `docs/ctsp_root/_README_hf.md` | `ctsp:_README_hf.md` | 10,694 |  |
| `docs/ctsp_root/ci.yml` | `ctsp:.github/workflows/ci.yml` | 1,926 |  |
| `docs/ctsp_root/pyproject.toml` | `ctsp:pyproject.toml` | 1,894 |  |
| `docs/ctsp_root/requirements.txt` | `ctsp:requirements.txt` | 467 |  |

### `docs/handoff/` (9 files, 487,868 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/handoff/DATASET_USAGE.md` | `ssn:HANDOFF/DATASET_USAGE.md` | 37,254 |  |
| `docs/handoff/GLOSSARY.md` | `ssn:HANDOFF/GLOSSARY.md` | 25,368 |  |
| `docs/handoff/INFRASTRUCTURE.md` | `ssn:HANDOFF/INFRASTRUCTURE.md` | 48,550 |  |
| `docs/handoff/LEAKAGE.md` | `ssn:HANDOFF/LEAKAGE.md` | 25,299 |  |
| `docs/handoff/OPEN_QUESTIONS.md` | `ssn:HANDOFF/OPEN_QUESTIONS.md` | 28,532 |  |
| `docs/handoff/README.md` | `ssn:HANDOFF/README.md` | 42,567 |  |
| `docs/handoff/RECIPES.md` | `ssn:HANDOFF/RECIPES.md` | 73,593 | **redacted**: one student username withheld |
| `docs/handoff/RESULTS_CATALOG.md` | `ssn:HANDOFF/RESULTS_CATALOG.md` | 110,438 |  |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | `ssn:HANDOFF/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | 96,267 | **redacted**: per-person username tally withheld |

### `docs/itksnap_review_2026-08/` (5 files, 707,493 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/itksnap_review_2026-08/0008_0179_0344.png` | `Desktop/itksnap_review/0008_0179_0344.png` | 300,175 |  |
| `docs/itksnap_review_2026-08/0008_sacrum.png` | `Desktop/itksnap_review/0008_sacrum.png` | 47,545 |  |
| `docs/itksnap_review_2026-08/0389_0412_0720_1153.png` | `Desktop/itksnap_review/0389_0412_0720_1153.png` | 351,297 |  |
| `docs/itksnap_review_2026-08/README.md` | `Desktop/itksnap_review/README.md` | 3,990 |  |
| `docs/itksnap_review_2026-08/labels_review.txt` | `Desktop/itksnap_review/labels_review.txt` | 4,486 |  |

### `docs/labnotebook_2026-03/` (5 files, 365,602 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/labnotebook_2026-03/3_19_26.txt` | `Desktop/SpineSurg-CT/labnotebook/3_19_26.txt` | 1,790 |  |
| `docs/labnotebook_2026-03/sci_comm_update_3_19_26.md` | `Desktop/SpineSurg-CT/labnotebook/sci_comm_update_3_19_26.md` | 4,274 |  |
| `docs/labnotebook_2026-03/sci_comm_update_3_20_26.md` | `Desktop/SpineSurg-CT/labnotebook/sci_comm_update_3_20_26.md` | 8,563 |  |
| `docs/labnotebook_2026-03/sci_comm_update_3_20_26_final.md.pdf` | `Desktop/SpineSurg-CT/labnotebook/sci_comm_update_3_20_26_final.md.pdf` | 336,903 |  |
| `docs/labnotebook_2026-03/sci_comm_update_3_21_26_final.md` | `Desktop/SpineSurg-CT/labnotebook/sci_comm_update_3_21_26_final.md` | 14,072 |  |

### `docs/release/` (11 files, 1,481,651 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/release/KNOWN_ISSUES.md` | `ctsp:data/zenodo_deposit/KNOWN_ISSUES.md` | 11,199 |  |
| `docs/release/README.md` | `ctsp:zenodo/README.md` | 19,987 |  |
| `docs/release/SHA256SUMS.txt` | `ctsp:data/zenodo_deposit/SHA256SUMS.txt` | 73,633 |  |
| `docs/release/dataset_labels.json` | `ctsp:data/zenodo_deposit/dataset_labels.json` | 4,004 |  |
| `docs/release/hf_dataset_card.md` | `ctsp:zenodo/hf_dataset_card.md` | 5,454 |  |
| `docs/release/itksnap_v4_labels.txt` | `ctsp:data/itksnap_v4_labels.txt` | 3,735 |  |
| `docs/release/itksnap_v5_labels.txt` | `ctsp:data/itksnap_v5_labels.txt` | 3,713 |  |
| `docs/release/itksnap_v6_labels.txt` | `ctsp:data/itksnap_v6_labels.txt` | 3,713 |  |
| `docs/release/manifest.json` | `ctsp:data/zenodo_deposit/manifest.json` | 1,100,037 |  |
| `docs/release/splits_5fold.json` | `ctsp:data/zenodo_deposit/splits_5fold.json` | 247,222 |  |
| `docs/release/zenodo_KNOWN_ISSUES.md` | `ctsp:zenodo/KNOWN_ISSUES.md` | 8,954 |  |

### `docs/review_reports/` (4 files, 44,232 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/review_reports/CLASSFIX_REVIEW.md` | `ctsp:scratchpad/CLASSFIX_REVIEW.md` | 2,111 |  |
| `docs/review_reports/REPORT_final.md` | `ctsp:scratchpad/REPORT_final.md` | 20,227 |  |
| `docs/review_reports/REPORT_interim.md` | `ctsp:scratchpad/REPORT_interim.md` | 16,115 |  |
| `docs/review_reports/SPINE_REVIEW.md` | `ctsp:scratchpad/SPINE_REVIEW.md` | 5,779 |  |

### `docs/spinesurg_ct_nnunet/` (5 files, 22,367 B)

| destination | source | bytes | note |
|---|---|---|---|
| `docs/spinesurg_ct_nnunet/BENCHMARK_PROTOCOL.md` | `ssn:docs/BENCHMARK_PROTOCOL.md` | 7,045 |  |
| `docs/spinesurg_ct_nnunet/COMPETITOR_BENCHMARK.md` | `ssn:docs/COMPETITOR_BENCHMARK.md` | 6,919 |  |
| `docs/spinesurg_ct_nnunet/ablations.md` | `ssn:docs/ablations.md` | 2,993 |  |
| `docs/spinesurg_ct_nnunet/data_README.md` | `ssn:data/README.md` | 2,935 | **redacted**: old-scheme warning prepended |
| `docs/spinesurg_ct_nnunet/xrsp1k_seg.md` | `ssn:docs/xrsp1k_seg.md` | 2,475 |  |

### `figures/` (1 files, 2,444,805 B)

| destination | source | bytes | note |
|---|---|---|---|
| `figures/spinopelvic_rotation.mp4` | `ctsp:spinopelvic_rotation.mp4` | 2,444,805 |  |

### `manuscripts/` (2 files, 4,649,322 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/3474_Not_All_Spines_Are_Create.pdf` | `ctsp:3474_Not_All_Spines_Are_Create.pdf` | 3,181,182 |  |
| `manuscripts/arxiv_final_draft_9_19_2026.pdf` | `ctsp:arxiv_final_draft_9_19_2026.pdf` | 1,468,140 |  |

### `manuscripts/mlhc_2026_rejected/` (5 files, 1,199,072 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/mlhc_2026_rejected/MLHC_2026_Research_Track_Paper.pdf` | `ctsp:MLHC_2026_Research_Track_Paper.pdf` | 1,136,762 |  |
| `manuscripts/mlhc_2026_rejected/_paper_text.txt` | `ctsp:_paper_text.txt` | 53,581 | **word** (10) |
| `manuscripts/mlhc_2026_rejected/_rebuttal_f65r.txt` | `ctsp:_rebuttal_f65r.txt` | 2,993 | **word** (1) |
| `manuscripts/mlhc_2026_rejected/_rebuttal_r2.txt` | `ctsp:_rebuttal_r2.txt` | 2,973 |  |
| `manuscripts/mlhc_2026_rejected/_rebuttal_r3.txt` | `ctsp:_rebuttal_r3.txt` | 2,763 |  |

### `manuscripts/mpda/` (145 files, 12,270,773 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/mpda/ARXIV_SUBMISSION.md` | `ctsp:paper/mpda/ARXIV_SUBMISSION.md` | 5,262 |  |
| `manuscripts/mpda/CITATION_CHECK.md` | `ctsp:paper/mpda/CITATION_CHECK.md` | 34,604 | **word** (1) |
| `manuscripts/mpda/CTSpinoPelvic1K_dataset_article.pdf` | `ctsp:paper/mpda/CTSpinoPelvic1K_dataset_article.pdf` | 960,208 |  |
| `manuscripts/mpda/CTSpinoPelvic1K_reprint.pdf` | `ctsp:paper/mpda/CTSpinoPelvic1K_reprint.pdf` | 1,453,129 |  |
| `manuscripts/mpda/CTSpinoPelvic1K_reprint_check.pdf` | `ctsp:paper/mpda/CTSpinoPelvic1K_reprint_check.pdf` | 1,030,374 |  |
| `manuscripts/mpda/PLAN.md` | `ctsp:paper/mpda/PLAN.md` | 6,054 |  |
| `manuscripts/mpda/REFERENCE_DOWNLOADS.md` | `ctsp:paper/mpda/REFERENCE_DOWNLOADS.md` | 9,551 |  |
| `manuscripts/mpda/REPRODUCE.md` | `ctsp:paper/mpda/REPRODUCE.md` | 9,243 |  |
| `manuscripts/mpda/STUDENT_REVIEW_RESPONSE.md` | `ctsp:paper/mpda/STUDENT_REVIEW_RESPONSE.md` | 7,897 | **redacted** (second pass): five student reviewers -> `student reviewer 1-5` |
| `manuscripts/mpda/_geomNotes.bib` | `ctsp:paper/mpda/_geomNotes.bib` | 70 |  |
| `manuscripts/mpda/_lenNotes.bib` | `ctsp:paper/mpda/_lenNotes.bib` | 70 |  |
| `manuscripts/mpda/_schehr_crossref/acr2021.bib` | `ctsp:paper/mpda/_schehr/crossref/acr2021.bib` | 828 |  |
| `manuscripts/mpda/_schehr_crossref/castellvi1984.bib` | `ctsp:paper/mpda/_schehr/crossref/castellvi1984.bib` | 459 |  |
| `manuscripts/mpda/_schehr_crossref/colonog.bib` | `ctsp:paper/mpda/_schehr/crossref/colonog.bib` | 523 |  |
| `manuscripts/mpda/_schehr_crossref/ctpelvic1k.bib` | `ctsp:paper/mpda/_schehr/crossref/ctpelvic1k.bib` | 601 |  |
| `manuscripts/mpda/_schehr_crossref/ctspine1k.bib` | `ctsp:paper/mpda/_schehr/crossref/ctspine1k.bib` | 658 |  |
| `manuscripts/mpda/_schehr_crossref/desilva2016.bib` | `ctsp:paper/mpda/_schehr/crossref/desilva2016.bib` | 748 |  |
| `manuscripts/mpda/_schehr_crossref/duplessis2018.bib` | `ctsp:paper/mpda/_schehr/crossref/duplessis2018.bib` | 393 |  |
| `manuscripts/mpda/_schehr_crossref/epstein2021.bib` | `ctsp:paper/mpda/_schehr/crossref/epstein2021.bib` | 351 |  |
| `manuscripts/mpda/_schehr_crossref/fea2026.bib` | `ctsp:paper/mpda/_schehr/crossref/fea2026.bib` | 522 |  |
| `manuscripts/mpda/_schehr_crossref/hughes2006.bib` | `ctsp:paper/mpda/_schehr/crossref/hughes2006.bib` | 419 |  |
| `manuscripts/mpda/_schehr_crossref/koninwalz2010.bib` | `ctsp:paper/mpda/_schehr/crossref/koninwalz2010.bib` | 422 |  |
| `manuscripts/mpda/_schehr_crossref/lian2018.bib` | `ctsp:paper/mpda/_schehr/crossref/lian2018.bib` | 430 |  |
| `manuscripts/mpda/_schehr_crossref/lo2015.bib` | `ctsp:paper/mpda/_schehr/crossref/lo2015.bib` | 827 |  |
| `manuscripts/mpda/_schehr_crossref/mody2008.bib` | `ctsp:paper/mpda/_schehr/crossref/mody2008.bib` | 463 |  |
| `manuscripts/mpda/_schehr_crossref/moller2026.bib` | `ctsp:paper/mpda/_schehr/crossref/moller2026.bib` | 765 |  |
| `manuscripts/mpda/_schehr_crossref/nagata2025.bib` | `ctsp:paper/mpda/_schehr/crossref/nagata2025.bib` | 579 |  |
| `manuscripts/mpda/_schehr_crossref/nass2013.bib` | `ctsp:paper/mpda/_schehr/crossref/nass2013.bib` | 590 |  |
| `manuscripts/mpda/_schehr_crossref/nnunet.bib` | `ctsp:paper/mpda/_schehr/crossref/nnunet.bib` | 486 |  |
| `manuscripts/mpda/_schehr_crossref/osc2026.bib` | `ctsp:paper/mpda/_schehr/crossref/osc2026.bib` | 402 |  |
| `manuscripts/mpda/_schehr_crossref/otake2012.bib` | `ctsp:paper/mpda/_schehr/crossref/otake2012.bib` | 545 |  |
| `manuscripts/mpda/_schehr_crossref/panjabi1991.bib` | `ctsp:paper/mpda/_schehr/crossref/panjabi1991.bib` | 498 |  |
| `manuscripts/mpda/_schehr_crossref/panjabi1992.bib` | `ctsp:paper/mpda/_schehr/crossref/panjabi1992.bib` | 494 |  |
| `manuscripts/mpda/_schehr_crossref/pickhardt2013.bib` | `ctsp:paper/mpda/_schehr/crossref/pickhardt2013.bib` | 573 |  |
| `manuscripts/mpda/_schehr_crossref/poolman2023.bib` | `ctsp:paper/mpda/_schehr/crossref/poolman2023.bib` | 478 |  |
| `manuscripts/mpda/_schehr_crossref/ribsegv2.bib` | `ctsp:paper/mpda/_schehr/crossref/ribsegv2.bib` | 603 |  |
| `manuscripts/mpda/_schehr_crossref/schinz2026.bib` | `ctsp:paper/mpda/_schehr/crossref/schinz2026.bib` | 626 |  |
| `manuscripts/mpda/_schehr_crossref/spineps2025.bib` | `ctsp:paper/mpda/_schehr/crossref/spineps2025.bib` | 828 |  |
| `manuscripts/mpda/_schehr_crossref/tcia.bib` | `ctsp:paper/mpda/_schehr/crossref/tcia.bib` | 619 |  |
| `manuscripts/mpda/_schehr_crossref/totalsegmentator.bib` | `ctsp:paper/mpda/_schehr/crossref/totalsegmentator.bib` | 609 |  |
| `manuscripts/mpda/_schehr_crossref/veridah2026.bib` | `ctsp:paper/mpda/_schehr/crossref/veridah2026.bib` | 834 |  |
| `manuscripts/mpda/_schehr_crossref/verse2021.bib` | `ctsp:paper/mpda/_schehr/crossref/verse2021.bib` | 1,703 |  |
| `manuscripts/mpda/_schehr_crossref/versedata2021.bib` | `ctsp:paper/mpda/_schehr/crossref/versedata2021.bib` | 708 |  |
| `manuscripts/mpda/_schehr_crossref/vialle2005.bib` | `ctsp:paper/mpda/_schehr/crossref/vialle2005.bib` | 529 |  |
| `manuscripts/mpda/_schehr_crossref/zindrick1987.bib` | `ctsp:paper/mpda/_schehr/crossref/zindrick1987.bib` | 571 |  |
| `manuscripts/mpda/_t3.py` | `ctsp:paper/mpda/_t3.py` | 1,536 |  |
| `manuscripts/mpda/_try1Notes.bib` | `ctsp:paper/mpda/_try1Notes.bib` | 70 |  |
| `manuscripts/mpda/apply_compliance.py` | `ctsp:paper/mpda/apply_compliance.py` | 15,224 | **redacted** (second pass): eleven-name co-author list withheld; **header** |
| `manuscripts/mpda/apply_figure_style.py` | `ctsp:paper/mpda/apply_figure_style.py` | 5,666 |  |
| `manuscripts/mpda/arxiv/census_table.tex` | `ctsp:paper/mpda/arxiv/census_table.tex` | 1,940 |  |
| `manuscripts/mpda/arxiv/figure_captions.tex` | `ctsp:paper/mpda/arxiv/figure_captions.tex` | 1,008 |  |
| `manuscripts/mpda/arxiv/figures/fig_anchors.pdf` | `ctsp:paper/mpda/arxiv/figures/fig_anchors.pdf` | 658,476 |  |
| `manuscripts/mpda/arxiv/figures/fig_fov.pdf` | `ctsp:paper/mpda/arxiv/figures/fig_fov.pdf` | 16,349 |  |
| `manuscripts/mpda/arxiv/figures/fig_hardware.pdf` | `ctsp:paper/mpda/arxiv/figures/fig_hardware.pdf` | 386,861 |  |
| `manuscripts/mpda/arxiv/figures/fig_levelatlas.pdf` | `ctsp:paper/mpda/arxiv/figures/fig_levelatlas.pdf` | 31,443 |  |
| `manuscripts/mpda/arxiv/figures/fig_validation.pdf` | `ctsp:paper/mpda/arxiv/figures/fig_validation.pdf` | 25,953 |  |
| `manuscripts/mpda/arxiv/main.tex` | `ctsp:paper/mpda/arxiv/main.tex` | 81,003 |  |
| `manuscripts/mpda/arxiv/supplement_body.tex` | `ctsp:paper/mpda/arxiv/supplement_body.tex` | 3,149 |  |
| `manuscripts/mpda/arxiv_abstract.txt` | `ctsp:paper/mpda/arxiv_abstract.txt` | 1,913 |  |
| `manuscripts/mpda/audit_artifacts.py` | `ctsp:paper/mpda/audit_artifacts.py` | 8,959 |  |
| `manuscripts/mpda/audit_ms.py` | `ctsp:paper/mpda/audit_ms.py` | 7,553 |  |
| `manuscripts/mpda/audit_pdfs.py` | `ctsp:paper/mpda/audit_pdfs.py` | 1,890 |  |
| `manuscripts/mpda/baseline_checkNotes.bib` | `ctsp:paper/mpda/baseline_checkNotes.bib` | 70 |  |
| `manuscripts/mpda/build.sh` | `ctsp:paper/mpda/build.sh` | 4,277 |  |
| `manuscripts/mpda/build_review_copy.py` | `ctsp:paper/mpda/build_review_copy.py` | 4,780 |  |
| `manuscripts/mpda/census_table.tex` | `ctsp:paper/mpda/census_table.tex` | 1,940 |  |
| `manuscripts/mpda/compress.py` | `ctsp:paper/mpda/compress.py` | 10,321 |  |
| `manuscripts/mpda/cover_letter.md` | `ctsp:paper/mpda/cover_letter.md` | 4,343 |  |
| `manuscripts/mpda/ctspinopelvic1k.bib` | `ctsp:paper/mpda/ctspinopelvic1k.bib` | 30,974 |  |
| `manuscripts/mpda/fig_pipeline_standalone.log` | `ctsp:paper/mpda/fig_pipeline_standalone.log` | 18,477 |  |
| `manuscripts/mpda/fig_pipeline_standalone.pdf` | `ctsp:paper/mpda/fig_pipeline_standalone.pdf` | 29,253 |  |
| `manuscripts/mpda/fig_pipeline_standalone.tex` | `ctsp:paper/mpda/fig_pipeline_standalone.tex` | 5,076 |  |
| `manuscripts/mpda/figure_captions.tex` | `ctsp:paper/mpda/figure_captions.tex` | 1,008 |  |
| `manuscripts/mpda/figures/fig_anchors.pdf` | `ctsp:paper/mpda/figures/fig_anchors.pdf` | 658,476 |  |
| `manuscripts/mpda/figures/fig_countfree.pdf` | `ctsp:paper/mpda/figures/fig_countfree.pdf` | 42,571 |  |
| `manuscripts/mpda/figures/fig_fov.pdf` | `ctsp:paper/mpda/figures/fig_fov.pdf` | 16,349 |  |
| `manuscripts/mpda/figures/fig_fov.png` | `ctsp:paper/mpda/figures/fig_fov.png` | 23,759 |  |
| `manuscripts/mpda/figures/fig_hardware.pdf` | `ctsp:paper/mpda/figures/fig_hardware.pdf` | 386,861 |  |
| `manuscripts/mpda/figures/fig_hardware.png` | `ctsp:paper/mpda/figures/fig_hardware.png` | 166,063 |  |
| `manuscripts/mpda/figures/fig_levelatlas.pdf` | `ctsp:paper/mpda/figures/fig_levelatlas.pdf` | 31,443 |  |
| `manuscripts/mpda/figures/fig_levelatlas.png` | `ctsp:paper/mpda/figures/fig_levelatlas.png` | 101,713 |  |
| `manuscripts/mpda/figures/fig_opportunistic.pdf` | `ctsp:paper/mpda/figures/fig_opportunistic.pdf` | 26,206 |  |
| `manuscripts/mpda/figures/fig_phenotypes.pdf` | `ctsp:paper/mpda/figures/fig_phenotypes.pdf` | 651,037 |  |
| `manuscripts/mpda/figures/fig_phenotypes.png` | `ctsp:paper/mpda/figures/fig_phenotypes.png` | 736,102 |  |
| `manuscripts/mpda/figures/fig_pipeline.pdf` | `ctsp:paper/mpda/figures/fig_pipeline.pdf` | 28,912 |  |
| `manuscripts/mpda/figures/fig_priorart.pdf` | `ctsp:paper/mpda/figures/fig_priorart.pdf` | 23,739 |  |
| `manuscripts/mpda/figures/fig_validation.pdf` | `ctsp:paper/mpda/figures/fig_validation.pdf` | 25,953 |  |
| `manuscripts/mpda/figures/hardware_stats.json` | `ctsp:paper/mpda/figures/hardware_stats.json` | 509 |  |
| `manuscripts/mpda/figures/table_hardware.tex` | `ctsp:paper/mpda/figures/table_hardware.tex` | 674 |  |
| `manuscripts/mpda/fix_blinding.py` | `ctsp:paper/mpda/fix_blinding.py` | 2,365 |  |
| `manuscripts/mpda/fix_lineno.py` | `ctsp:paper/mpda/fix_lineno.py` | 1,635 |  |
| `manuscripts/mpda/fix_table_rows.py` | `ctsp:paper/mpda/fix_table_rows.py` | 1,092 |  |
| `manuscripts/mpda/inline_bbl.py` | `ctsp:paper/mpda/inline_bbl.py` | 2,931 |  |
| `manuscripts/mpda/levelatlas.py` | `ctsp:paper/mpda/levelatlas.py` | 5,529 |  |
| `manuscripts/mpda/main.log` | `ctsp:paper/mpda/main.log` | 37,391 |  |
| `manuscripts/mpda/main.out` | `ctsp:paper/mpda/main.out` | 5,134 |  |
| `manuscripts/mpda/main.pdf` | `ctsp:paper/mpda/main.pdf` | 1,125,203 |  |
| `manuscripts/mpda/main.tex` | `ctsp:paper/mpda/main.tex` | 81,038 |  |
| `manuscripts/mpda/main.tex.pre_schehr` | `ctsp:paper/mpda/main.tex.pre_schehr` | 72,360 |  |
| `manuscripts/mpda/mainNotes.bib` | `ctsp:paper/mpda/mainNotes.bib` | 70 |  |
| `manuscripts/mpda/main_OL.tex` | `ctsp:paper/mpda/main_OL.tex` | 82,025 |  |
| `manuscripts/mpda/make_abstract_text.py` | `ctsp:paper/mpda/make_abstract_text.py` | 2,333 |  |
| `manuscripts/mpda/make_arxiv.sh` | `ctsp:paper/mpda/make_arxiv.sh` | 5,822 |  |
| `manuscripts/mpda/make_bibtest.py` | `ctsp:paper/mpda/make_bibtest.py` | 2,530 |  |
| `manuscripts/mpda/make_coauthor_docs.py` | `ctsp:paper/mpda/make_coauthor_docs.py` | 4,888 |  |
| `manuscripts/mpda/make_figures.py` | `ctsp:paper/mpda/make_figures.py` | 25,165 |  |
| `manuscripts/mpda/make_fov_fig.py` | `ctsp:paper/mpda/make_fov_fig.py` | 5,346 |  |
| `manuscripts/mpda/make_levelatlas_fig.py` | `ctsp:paper/mpda/make_levelatlas_fig.py` | 27,894 |  |
| `manuscripts/mpda/make_overleaf.py` | `ctsp:paper/mpda/make_overleaf.py` | 1,885 |  |
| `manuscripts/mpda/make_priorart_figure.py` | `ctsp:paper/mpda/make_priorart_figure.py` | 5,910 |  |
| `manuscripts/mpda/make_submission.py` | `ctsp:paper/mpda/make_submission.py` | 17,522 |  |
| `manuscripts/mpda/mdpa_extra.bib` | `ctsp:paper/mpda/mdpa_extra.bib` | 4,360 |  |
| `manuscripts/mpda/medphy.bst` | `ctsp:paper/mpda/medphy.bst` | 61,573 |  |
| `manuscripts/mpda/overleaf/ctspinopelvic1k.bib` | `ctsp:paper/mpda/overleaf/ctspinopelvic1k.bib` | 29,930 |  |
| `manuscripts/mpda/overleaf/figure_captions.tex` | `ctsp:paper/mpda/overleaf/figure_captions.tex` | 1,499 |  |
| `manuscripts/mpda/overleaf/figures/fig_anchors.pdf` | `ctsp:paper/mpda/overleaf/figures/fig_anchors.pdf` | 658,696 |  |
| `manuscripts/mpda/overleaf/figures/fig_countfree.pdf` | `ctsp:paper/mpda/overleaf/figures/fig_countfree.pdf` | 42,571 |  |
| `manuscripts/mpda/overleaf/figures/fig_fov.pdf` | `ctsp:paper/mpda/overleaf/figures/fig_fov.pdf` | 16,349 |  |
| `manuscripts/mpda/overleaf/figures/fig_hardware.pdf` | `ctsp:paper/mpda/overleaf/figures/fig_hardware.pdf` | 386,861 |  |
| `manuscripts/mpda/overleaf/figures/fig_levelatlas.pdf` | `ctsp:paper/mpda/overleaf/figures/fig_levelatlas.pdf` | 31,583 |  |
| `manuscripts/mpda/overleaf/figures/fig_validation.pdf` | `ctsp:paper/mpda/overleaf/figures/fig_validation.pdf` | 25,953 |  |
| `manuscripts/mpda/overleaf/main.tex` | `ctsp:paper/mpda/overleaf/main.tex` | 68,848 |  |
| `manuscripts/mpda/overleaf/medphy.bst` | `ctsp:paper/mpda/overleaf/medphy.bst` | 61,573 |  |
| `manuscripts/mpda/overleaf_README.md` | `ctsp:paper/mpda/overleaf_README.md` | 3,407 |  |
| `manuscripts/mpda/page_estimate.py` | `ctsp:paper/mpda/page_estimate.py` | 4,037 |  |
| `manuscripts/mpda/reorder_bib.py` | `ctsp:paper/mpda/reorder_bib.py` | 1,253 |  |
| `manuscripts/mpda/reprint_check.log` | `ctsp:paper/mpda/reprint_check.log` | 38,871 |  |
| `manuscripts/mpda/reprint_check.out` | `ctsp:paper/mpda/reprint_check.out` | 4,898 |  |
| `manuscripts/mpda/reprint_check.pdf` | `ctsp:paper/mpda/reprint_check.pdf` | 852,760 |  |
| `manuscripts/mpda/reprint_checkNotes.bib` | `ctsp:paper/mpda/reprint_checkNotes.bib` | 70 |  |
| `manuscripts/mpda/supplement_body.tex` | `ctsp:paper/mpda/supplement_body.tex` | 3,149 |  |
| `manuscripts/mpda/supplementary.log` | `ctsp:paper/mpda/supplementary.log` | 22,277 |  |
| `manuscripts/mpda/supplementary.out` | `ctsp:paper/mpda/supplementary.out` | 0 |  |
| `manuscripts/mpda/supplementary.pdf` | `ctsp:paper/mpda/supplementary.pdf` | 508,847 |  |
| `manuscripts/mpda/supplementary.tex` | `ctsp:paper/mpda/supplementary.tex` | 3,540 |  |
| `manuscripts/mpda/supplementaryNotes.bib` | `ctsp:paper/mpda/supplementaryNotes.bib` | 70 |  |
| `manuscripts/mpda/title_page.log` | `ctsp:paper/mpda/title_page.log` | 11,186 |  |
| `manuscripts/mpda/title_page.out` | `ctsp:paper/mpda/title_page.out` | 0 |  |
| `manuscripts/mpda/title_page.pdf` | `ctsp:paper/mpda/title_page.pdf` | 52,250 |  |
| `manuscripts/mpda/title_page.tex` | `ctsp:paper/mpda/title_page.tex` | 7,344 |  |
| `manuscripts/mpda/tools/aggregate_spinopelvic.py` | `ctsp:paper/mpda/tools/aggregate_spinopelvic.py` | 4,259 |  |
| `manuscripts/mpda/tools/digitize_panjabi_fig4a.py` | `ctsp:paper/mpda/tools/digitize_panjabi_fig4a.py` | 11,030 |  |
| `manuscripts/mpda/tools/render_pi_construction.py` | `ctsp:paper/mpda/tools/render_pi_construction.py` | 4,707 |  |
| `manuscripts/mpda/tp.log` | `ctsp:paper/mpda/tp.log` | 13,859 |  |
| `manuscripts/mpda/typeset_previewNotes.bib` | `ctsp:paper/mpda/typeset_previewNotes.bib` | 70 |  |

### `manuscripts/mpda_ai_text_scans/` (1 files, 124,498 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/mpda_ai_text_scans/MDPA_AI.pdf` | `Desktop/MDPA_AI.pdf` | 124,498 |  |

### `manuscripts/mpda_as_submitted_2026-09-07/` (12 files, 2,966,995 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/mpda_as_submitted_2026-09-07/Cover_Letter.md` | `Desktop/CTSpinoPelvic1K_submission/Cover_Letter.md` | 2,344 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/LaTeX_source_CTSpinoPelvic1K.zip` | `Desktop/CTSpinoPelvic1K_submission/LaTeX_source_CTSpinoPelvic1K.zip` | 863,471 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/Main_Document_CTSpinoPelvic1K.pdf` | `Desktop/CTSpinoPelvic1K_submission/Main_Document_CTSpinoPelvic1K.pdf` | 1,121,940 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/Supporting_Information_CTSpinoPelvic1K.pdf` | `Desktop/CTSpinoPelvic1K_submission/Supporting_Information_CTSpinoPelvic1K.pdf` | 29,969 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/Title_Page_CTSpinoPelvic1K.pdf` | `Desktop/CTSpinoPelvic1K_submission/Title_Page_CTSpinoPelvic1K.pdf` | 52,115 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/figures/Figure_1.pdf` | `Desktop/CTSpinoPelvic1K_submission/figures/Figure_1.pdf` | 29,253 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/figures/Figure_2.pdf` | `Desktop/CTSpinoPelvic1K_submission/figures/Figure_2.pdf` | 429,929 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/figures/Figure_3.pdf` | `Desktop/CTSpinoPelvic1K_submission/figures/Figure_3.pdf` | 322,211 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/figures/Figure_4.pdf` | `Desktop/CTSpinoPelvic1K_submission/figures/Figure_4.pdf` | 42,618 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/figures/Figure_5.pdf` | `Desktop/CTSpinoPelvic1K_submission/figures/Figure_5.pdf` | 24,132 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/figures/Figure_6.pdf` | `Desktop/CTSpinoPelvic1K_submission/figures/Figure_6.pdf` | 32,670 |  |
| `manuscripts/mpda_as_submitted_2026-09-07/figures/Figure_7.pdf` | `Desktop/CTSpinoPelvic1K_submission/figures/Figure_7.pdf` | 16,343 |  |

### `manuscripts/mpda_as_submitted_2026-09-21/` (1 files, 962,263 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/mpda_as_submitted_2026-09-21/MDPA_FINAL.pdf` | `Desktop/MDPA_FINAL.pdf` | 962,263 |  |

### `manuscripts/neurips_camera_ready/` (33 files, 5,988,001 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/neurips_camera_ready/.gitignore` | `ctsp:CAMERA_READY_NEURIPS/.gitignore` | 211 |  |
| `manuscripts/neurips_camera_ready/CAMERA_READY_CHANGES.md` | `ctsp:CAMERA_READY_NEURIPS/CAMERA_READY_CHANGES.md` | 80,406 |  |
| `manuscripts/neurips_camera_ready/NEURIPS_CURRENT_PDF.pdf` | `ctsp:CAMERA_READY_NEURIPS/NEURIPS_CURRENT_PDF.pdf` | 3,181,182 |  |
| `manuscripts/neurips_camera_ready/NEURIPS_CURRENT_PDF.txt` | `ctsp:CAMERA_READY_NEURIPS/NEURIPS_CURRENT_PDF.txt` | 79,106 | **word** (1) |
| `manuscripts/neurips_camera_ready/REVIEWER_CRITIQUES.pdf` | `ctsp:CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.pdf` | 529,524 |  |
| `manuscripts/neurips_camera_ready/REVIEWER_CRITIQUES.txt` | `ctsp:CAMERA_READY_NEURIPS/REVIEWER_CRITIQUES.txt` | 36,345 | **word** (2) |
| `manuscripts/neurips_camera_ready/neurips2025.bib` | `ctsp:CAMERA_READY_NEURIPS/neurips2025.bib` | 322 |  |
| `manuscripts/neurips_camera_ready/neurips2026.bib` | `ctsp:CAMERA_READY_NEURIPS/neurips2026.bib` | 496 |  |
| `manuscripts/neurips_camera_ready/src/appendix/appendix.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/appendix.tex` | 1,960 |  |
| `manuscripts/neurips_camera_ready/src/appendix/background.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/background.tex` | 12,724 |  |
| `manuscripts/neurips_camera_ready/src/appendix/castellvi_history.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/castellvi_history.tex` | 2,858 |  |
| `manuscripts/neurips_camera_ready/src/appendix/construction_figure.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/construction_figure.tex` | 2,159 |  |
| `manuscripts/neurips_camera_ready/src/appendix/dataset_comparison.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/dataset_comparison.tex` | 8,010 |  |
| `manuscripts/neurips_camera_ready/src/appendix/intervals.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/intervals.tex` | 3,259 |  |
| `manuscripts/neurips_camera_ready/src/appendix/release_split.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/release_split.tex` | 5,906 |  |
| `manuscripts/neurips_camera_ready/src/appendix/spineps.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/spineps.tex` | 8,057 |  |
| `manuscripts/neurips_camera_ready/src/appendix/training_details.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/training_details.tex` | 950 |  |
| `manuscripts/neurips_camera_ready/src/appendix/unmerged_control.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/unmerged_control.tex` | 2,636 |  |
| `manuscripts/neurips_camera_ready/src/appendix/v11_results.tex` | `ctsp:CAMERA_READY_NEURIPS/src/appendix/v11_results.tex` | 6,191 |  |
| `manuscripts/neurips_camera_ready/src/bib/references.bib` | `ctsp:CAMERA_READY_NEURIPS/src/bib/references.bib` | 34,315 |  |
| `manuscripts/neurips_camera_ready/src/checklist.tex` | `ctsp:CAMERA_READY_NEURIPS/src/checklist.tex` | 38,637 |  |
| `manuscripts/neurips_camera_ready/src/figs/fig_app_construction.pdf` | `ctsp:CAMERA_READY_NEURIPS/src/figs/fig_app_construction.pdf` | 42,493 |  |
| `manuscripts/neurips_camera_ready/src/figs/lstv_lumbarization_215_spine_only.png` | `ctsp:CAMERA_READY_NEURIPS/src/figs/lstv_lumbarization_215_spine_only.png` | 631,555 |  |
| `manuscripts/neurips_camera_ready/src/latexmk_20260925_affil.log` | `ctsp:CAMERA_READY_NEURIPS/src/latexmk_20260925_affil.log` | 27,974 |  |
| `manuscripts/neurips_camera_ready/src/latexmk_20260927.log` | `ctsp:CAMERA_READY_NEURIPS/src/latexmk_20260927.log` | 22,649 |  |
| `manuscripts/neurips_camera_ready/src/latexmk_20260927b.log` | `ctsp:CAMERA_READY_NEURIPS/src/latexmk_20260927b.log` | 22,631 |  |
| `manuscripts/neurips_camera_ready/src/latexmk_20260927c.log` | `ctsp:CAMERA_READY_NEURIPS/src/latexmk_20260927c.log` | 24,060 |  |
| `manuscripts/neurips_camera_ready/src/latexmk_cr.log` | `ctsp:CAMERA_READY_NEURIPS/src/latexmk_cr.log` | 14,520 |  |
| `manuscripts/neurips_camera_ready/src/neurips_2026.log` | `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.log` | 26,807 |  |
| `manuscripts/neurips_camera_ready/src/neurips_2026.out` | `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.out` | 4,456 |  |
| `manuscripts/neurips_camera_ready/src/neurips_2026.pdf` | `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.pdf` | 1,071,520 |  |
| `manuscripts/neurips_camera_ready/src/neurips_2026.sty` | `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.sty` | 13,462 |  |
| `manuscripts/neurips_camera_ready/src/neurips_2026.tex` | `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.tex` | 50,620 |  |

### `manuscripts/nextpaper_ar_2026-09-08/` (20 files, 2,508,569 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/nextpaper_ar_2026-09-08/REVISION_PLAN.md` | `Desktop/NextPaper/AR/REVISION_PLAN.md` | 5,899 |  |
| `manuscripts/nextpaper_ar_2026-09-08/bib/references.bib` | `Desktop/NextPaper/AR/bib/references.bib` | 10,251 |  |
| `manuscripts/nextpaper_ar_2026-09-08/build.log` | `Desktop/NextPaper/AR/build.log` | 51 |  |
| `manuscripts/nextpaper_ar_2026-09-08/checklist.tex` | `Desktop/NextPaper/AR/checklist.tex` | 26,167 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/fig_anchors.pdf` | `Desktop/NextPaper/AR/figs/fig_anchors.pdf` | 429,929 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/fig_architecture.pdf` | `Desktop/NextPaper/AR/figs/fig_architecture.pdf` | 23,036 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/fig_capabilities.pdf` | `Desktop/NextPaper/AR/figs/fig_capabilities.pdf` | 20,060 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/fig_countfree.pdf` | `Desktop/NextPaper/AR/figs/fig_countfree.pdf` | 42,618 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/fig_patch_context_0376.pdf` | `Desktop/NextPaper/AR/figs/fig_patch_context_0376.pdf` | 29,583 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/fig_pipeline_oneshot.pdf` | `Desktop/NextPaper/AR/figs/fig_pipeline_oneshot.pdf` | 41,948 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/fig_training.pdf` | `Desktop/NextPaper/AR/figs/fig_training.pdf` | 27,798 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/lstv_lumbarization_215_spine_only.png` | `Desktop/NextPaper/AR/figs/lstv_lumbarization_215_spine_only.png` | 631,555 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/six_lumbar_readings.pdf` | `Desktop/NextPaper/AR/figs/six_lumbar_readings.pdf` | 19,454 |  |
| `manuscripts/nextpaper_ar_2026-09-08/figs/tab_capabilities.tex` | `Desktop/NextPaper/AR/figs/tab_capabilities.tex` | 1,190 |  |
| `manuscripts/nextpaper_ar_2026-09-08/full-paper-template.tex` | `Desktop/NextPaper/AR/full-paper-template.tex` | 68,330 | **word** (10) |
| `manuscripts/nextpaper_ar_2026-09-08/neurips_2026.log` | `Desktop/NextPaper/AR/neurips_2026.log` | 30,291 |  |
| `manuscripts/nextpaper_ar_2026-09-08/neurips_2026.out` | `Desktop/NextPaper/AR/neurips_2026.out` | 2,585 |  |
| `manuscripts/nextpaper_ar_2026-09-08/neurips_2026.pdf` | `Desktop/NextPaper/AR/neurips_2026.pdf` | 1,021,740 |  |
| `manuscripts/nextpaper_ar_2026-09-08/neurips_2026.sty` | `Desktop/NextPaper/AR/neurips_2026.sty` | 13,462 |  |
| `manuscripts/nextpaper_ar_2026-09-08/neurips_2026.tex` | `Desktop/NextPaper/AR/neurips_2026.tex` | 62,622 | **word** (1) |

### `manuscripts/nextpaper_radai/` (17 files, 917,852 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/nextpaper_radai/README.md` | `Desktop/NextPaper/RadAI/README.md` | 3,073 |  |
| `manuscripts/nextpaper_radai/claim_checklist.md` | `Desktop/NextPaper/RadAI/claim_checklist.md` | 3,856 |  |
| `manuscripts/nextpaper_radai/figs/fig_anchors.pdf` | `Desktop/NextPaper/RadAI/figs/fig_anchors.pdf` | 429,929 |  |
| `manuscripts/nextpaper_radai/figs/fig_architecture.pdf` | `Desktop/NextPaper/RadAI/figs/fig_architecture.pdf` | 23,036 |  |
| `manuscripts/nextpaper_radai/figs/fig_capabilities.pdf` | `Desktop/NextPaper/RadAI/figs/fig_capabilities.pdf` | 20,060 |  |
| `manuscripts/nextpaper_radai/figs/fig_countfree.pdf` | `Desktop/NextPaper/RadAI/figs/fig_countfree.pdf` | 42,618 |  |
| `manuscripts/nextpaper_radai/figs/fig_patch_context_0376.pdf` | `Desktop/NextPaper/RadAI/figs/fig_patch_context_0376.pdf` | 29,583 |  |
| `manuscripts/nextpaper_radai/figs/fig_pipeline_oneshot.pdf` | `Desktop/NextPaper/RadAI/figs/fig_pipeline_oneshot.pdf` | 41,948 |  |
| `manuscripts/nextpaper_radai/figs/fig_training.pdf` | `Desktop/NextPaper/RadAI/figs/fig_training.pdf` | 27,798 |  |
| `manuscripts/nextpaper_radai/figs/six_lumbar_readings.pdf` | `Desktop/NextPaper/RadAI/figs/six_lumbar_readings.pdf` | 19,454 |  |
| `manuscripts/nextpaper_radai/figs/tab_capabilities.tex` | `Desktop/NextPaper/RadAI/figs/tab_capabilities.tex` | 1,190 |  |
| `manuscripts/nextpaper_radai/main.log` | `Desktop/NextPaper/RadAI/main.log` | 19,082 |  |
| `manuscripts/nextpaper_radai/main.out` | `Desktop/NextPaper/RadAI/main.out` | 428 |  |
| `manuscripts/nextpaper_radai/main.pdf` | `Desktop/NextPaper/RadAI/main.pdf` | 225,032 |  |
| `manuscripts/nextpaper_radai/main.tex` | `Desktop/NextPaper/RadAI/main.tex` | 18,413 |  |
| `manuscripts/nextpaper_radai/refs.bib` | `Desktop/NextPaper/RadAI/refs.bib` | 10,251 |  |
| `manuscripts/nextpaper_radai/tables_src.tex` | `Desktop/NextPaper/RadAI/tables_src.tex` | 2,101 |  |

### `manuscripts/spinesurgct_arxiv_2026-03/` (4 files, 467,271 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/spinesurgct_arxiv_2026-03/Arxiv_draft.pdf` | `Desktop/SpineSurg-CT/Arxiv_draft.pdf` | 194,814 |  |
| `manuscripts/spinesurgct_arxiv_2026-03/SPINESURG_CT_Arxiv.pdf` | `Desktop/SpineSurg-CT/SPINESURG_CT_Arxiv.pdf` | 218,747 |  |
| `manuscripts/spinesurgct_arxiv_2026-03/SpineSurgCT_arxiv.tex` | `Desktop/SpineSurg-CT/SpineSurgCT_arxiv.tex` | 46,594 |  |
| `manuscripts/spinesurgct_arxiv_2026-03/SpineSurgCT_references.bib` | `Desktop/SpineSurg-CT/SpineSurgCT_references.bib` | 7,116 |  |

### `manuscripts/talks/` (173 files, 53,037,004 B)

| destination | source | bytes | note |
|---|---|---|---|
| `manuscripts/talks/cns2026/CNS2026_Schwing_LSTV.pptx` | `Desktop/CNS2026_Schwing_LSTV.pptx` | 2,276,047 |  |
| `manuscripts/talks/cns2026/CNS2026_Schwing_NotAllSpines_public_v12.pptx` | `Desktop/CNS2026_Schwing_NotAllSpines_public_v12.pptx` | 6,945,073 |  |
| `manuscripts/talks/cns2026/chart_level_sweep.py` | `ctsp:paper/cns2026/chart_level_sweep.py` | 12,286 |  |
| `manuscripts/talks/cns2026/figs/fig_anchors.png` | `ctsp:paper/cns2026/figs/fig_anchors.png` | 317,041 |  |
| `manuscripts/talks/cns2026/figs/fig_architecture.png` | `ctsp:paper/cns2026/figs/fig_architecture.png` | 190,755 |  |
| `manuscripts/talks/cns2026/figs/fig_capabilities.png` | `ctsp:paper/cns2026/figs/fig_capabilities.png` | 109,408 |  |
| `manuscripts/talks/cns2026/figs/fig_countfree.png` | `ctsp:paper/cns2026/figs/fig_countfree.png` | 104,545 |  |
| `manuscripts/talks/cns2026/figs/fig_fov.png` | `ctsp:paper/cns2026/figs/fig_fov.png` | 22,880 |  |
| `manuscripts/talks/cns2026/figs/fig_hardware.png` | `ctsp:paper/cns2026/figs/fig_hardware.png` | 260,576 |  |
| `manuscripts/talks/cns2026/figs/fig_levelatlas.png` | `ctsp:paper/cns2026/figs/fig_levelatlas.png` | 128,992 |  |
| `manuscripts/talks/cns2026/figs/fig_patch_context_0376.png` | `ctsp:paper/cns2026/figs/fig_patch_context_0376.png` | 161,941 |  |
| `manuscripts/talks/cns2026/figs/fig_pipeline.png` | `ctsp:paper/cns2026/figs/fig_pipeline.png` | 143,146 |  |
| `manuscripts/talks/cns2026/figs/fig_pipeline_oneshot.png` | `ctsp:paper/cns2026/figs/fig_pipeline_oneshot.png` | 150,219 |  |
| `manuscripts/talks/cns2026/figs/fig_training.png` | `ctsp:paper/cns2026/figs/fig_training.png` | 169,326 |  |
| `manuscripts/talks/cns2026/figs/fig_validation.png` | `ctsp:paper/cns2026/figs/fig_validation.png` | 53,356 |  |
| `manuscripts/talks/cns2026/figs/pelvic_width.png` | `ctsp:paper/cns2026/figs/pelvic_width.png` | 165,529 |  |
| `manuscripts/talks/cns2026/figs/reading_sheet_0376.png` | `ctsp:paper/cns2026/figs/reading_sheet_0376.png` | 679,108 |  |
| `manuscripts/talks/cns2026/figs/six_lumbar_readings.png` | `ctsp:paper/cns2026/figs/six_lumbar_readings.png` | 125,369 |  |
| `manuscripts/talks/cns2026/figs_cited/ajnr2023_fig1.jpg` | `ctsp:paper/cns2026/figs_cited/ajnr2023_fig1.jpg` | 95,905 |  |
| `manuscripts/talks/cns2026/figs_cited/bettis2026_fig1.png` | `ctsp:paper/cns2026/figs_cited/bettis2026_fig1.png` | 442,001 |  |
| `manuscripts/talks/cns2026/figs_cited/bettis2026_fig1_digitised.csv` | `ctsp:paper/cns2026/figs_cited/bettis2026_fig1_digitised.csv` | 954 |  |
| `manuscripts/talks/cns2026/figs_cited/bettis2026_fig2.png` | `ctsp:paper/cns2026/figs_cited/bettis2026_fig2.png` | 4,059 |  |
| `manuscripts/talks/cns2026/figs_cited/bettis2026_fig3.png` | `ctsp:paper/cns2026/figs_cited/bettis2026_fig3.png` | 4,059 |  |
| `manuscripts/talks/cns2026/figs_cited/childers2018_fig1.jpg` | `ctsp:paper/cns2026/figs_cited/childers2018_fig1.jpg` | 45,497 |  |
| `manuscripts/talks/cns2026/figs_cited/desilva2016_fig1.jpg` | `ctsp:paper/cns2026/figs_cited/desilva2016_fig1.jpg` | 139,527 |  |
| `manuscripts/talks/cns2026/figs_cited/desilva2016_fig4.jpg` | `ctsp:paper/cns2026/figs_cited/desilva2016_fig4.jpg` | 126,670 |  |
| `manuscripts/talks/cns2026/figs_cited/machin2018_fig1.png` | `ctsp:paper/cns2026/figs_cited/machin2018_fig1.png` | 96,770 |  |
| `manuscripts/talks/cns2026/figs_cited/machin2018_fig2.png` | `ctsp:paper/cns2026/figs_cited/machin2018_fig2.png` | 133,415 |  |
| `manuscripts/talks/cns2026/figs_cited/machin2018_fig2_digitised.csv` | `ctsp:paper/cns2026/figs_cited/machin2018_fig2_digitised.csv` | 870 |  |
| `manuscripts/talks/cns2026/figs_cited/manbachi2018_fig2.jpg` | `ctsp:paper/cns2026/figs_cited/manbachi2018_fig2.jpg` | 135,546 |  |
| `manuscripts/talks/cns2026/figs_cited/manbachi2018_fig6.jpg` | `ctsp:paper/cns2026/figs_cited/manbachi2018_fig6.jpg` | 85,150 |  |
| `manuscripts/talks/cns2026/figs_cited/otake2012_fig14.jpg` | `ctsp:paper/cns2026/figs_cited/otake2012_fig14.jpg` | 35,232 |  |
| `manuscripts/talks/cns2026/figs_cited/otake2012_fig6.jpg` | `ctsp:paper/cns2026/figs_cited/otake2012_fig6.jpg` | 38,087 |  |
| `manuscripts/talks/cns2026/figs_cited/sabri2025_article.html` | `ctsp:paper/cns2026/figs_cited/sabri2025_article.html` | 2,263 |  |
| `manuscripts/talks/cns2026/figs_cited/strong2021_fig2.jpg` | `ctsp:paper/cns2026/figs_cited/strong2021_fig2.jpg` | 363,123 |  |
| `manuscripts/talks/cns2026/figs_cited/strong2021_fig3.jpg` | `ctsp:paper/cns2026/figs_cited/strong2021_fig3.jpg` | 221,711 |  |
| `manuscripts/talks/cns2026/figs_public/chart_pub_castellvi.png` | `ctsp:paper/cns2026/figs_public/chart_pub_castellvi.png` | 84,413 |  |
| `manuscripts/talks/cns2026/figs_public/chart_pub_gain.png` | `ctsp:paper/cns2026/figs_public/chart_pub_gain.png` | 118,511 |  |
| `manuscripts/talks/cns2026/figs_public/chart_pub_l6.png` | `ctsp:paper/cns2026/figs_public/chart_pub_l6.png` | 85,308 |  |
| `manuscripts/talks/cns2026/figs_public/chart_pub_levels.png` | `ctsp:paper/cns2026/figs_public/chart_pub_levels.png` | 133,462 |  |
| `manuscripts/talks/cns2026/figs_public/mpda/fig_hardware.png` | `ctsp:paper/cns2026/figs_public/mpda/fig_hardware.png` | 514,601 |  |
| `manuscripts/talks/cns2026/figs_public/mpda/fig_pipeline.png` | `ctsp:paper/cns2026/figs_public/mpda/fig_pipeline.png` | 192,600 |  |
| `manuscripts/talks/cns2026/figs_public/mpda/fig_validation.png` | `ctsp:paper/cns2026/figs_public/mpda/fig_validation.png` | 76,001 |  |
| `manuscripts/talks/cns2026/figs_public/public_numbers.json` | `ctsp:paper/cns2026/figs_public/public_numbers.json` | 978 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig1_ct_row.png` | `ctsp:paper/cns2026/figs_v2/big_fig1_ct_row.png` | 865,770 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig1_ct_vs_film.png` | `ctsp:paper/cns2026/figs_v2/big_fig1_ct_vs_film.png` | 928,785 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig2_a.png` | `ctsp:paper/cns2026/figs_v2/big_fig2_a.png` | 500,287 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig2_ab_side.png` | `ctsp:paper/cns2026/figs_v2/big_fig2_ab_side.png` | 924,933 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig2_b.png` | `ctsp:paper/cns2026/figs_v2/big_fig2_b.png` | 273,876 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig4_ab.png` | `ctsp:paper/cns2026/figs_v2/big_fig4_ab.png` | 602,540 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig4_c.png` | `ctsp:paper/cns2026/figs_v2/big_fig4_c.png` | 271,896 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig4_cd.png` | `ctsp:paper/cns2026/figs_v2/big_fig4_cd.png` | 545,156 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig4_d.png` | `ctsp:paper/cns2026/figs_v2/big_fig4_d.png` | 280,832 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig5_a.png` | `ctsp:paper/cns2026/figs_v2/big_fig5_a.png` | 129,590 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig5_b.png` | `ctsp:paper/cns2026/figs_v2/big_fig5_b.png` | 88,140 |  |
| `manuscripts/talks/cns2026/figs_v2/big_fig5_cd.png` | `ctsp:paper/cns2026/figs_v2/big_fig5_cd.png` | 266,984 |  |
| `manuscripts/talks/cns2026/figs_v2/big_figS1_a.png` | `ctsp:paper/cns2026/figs_v2/big_figS1_a.png` | 368,261 |  |
| `manuscripts/talks/cns2026/figs_v2/big_figS1_legend.png` | `ctsp:paper/cns2026/figs_v2/big_figS1_legend.png` | 11,395 |  |
| `manuscripts/talks/cns2026/figs_v2/big_figS5_a.png` | `ctsp:paper/cns2026/figs_v2/big_figS5_a.png` | 695,090 |  |
| `manuscripts/talks/cns2026/figs_v2/big_figS5_a_grid.png` | `ctsp:paper/cns2026/figs_v2/big_figS5_a_grid.png` | 702,987 |  |
| `manuscripts/talks/cns2026/figs_v2/big_figS5_ab.png` | `ctsp:paper/cns2026/figs_v2/big_figS5_ab.png` | 836,151 |  |
| `manuscripts/talks/cns2026/figs_v2/big_figS5_b.png` | `ctsp:paper/cns2026/figs_v2/big_figS5_b.png` | 127,530 |  |
| `manuscripts/talks/cns2026/figs_v2/big_gallery_trio.png` | `ctsp:paper/cns2026/figs_v2/big_gallery_trio.png` | 389,883 |  |
| `manuscripts/talks/cns2026/figs_v2/board_wrongsite_cost.png` | `ctsp:paper/cns2026/figs_v2/board_wrongsite_cost.png` | 640,656 |  |
| `manuscripts/talks/cns2026/figs_v2/cartoon_sweep.png` | `ctsp:paper/cns2026/figs_v2/cartoon_sweep.png` | 119,849 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_bettis_redrawn.png` | `ctsp:paper/cns2026/figs_v2/chart_bettis_redrawn.png` | 351,672 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_census.png` | `ctsp:paper/cns2026/figs_v2/chart_census.png` | 139,702 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_census_cumulative.png` | `ctsp:paper/cns2026/figs_v2/chart_census_cumulative.png` | 317,676 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_census_map.png` | `ctsp:paper/cns2026/figs_v2/chart_census_map.png` | 287,716 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_corpus.png` | `ctsp:paper/cns2026/figs_v2/chart_corpus.png` | 258,325 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_costs.png` | `ctsp:paper/cns2026/figs_v2/chart_costs.png` | 220,603 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_coupling.png` | `ctsp:paper/cns2026/figs_v2/chart_coupling.png` | 282,213 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_coverage.png` | `ctsp:paper/cns2026/figs_v2/chart_coverage.png` | 117,209 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_fig5a_census.png` | `ctsp:paper/cns2026/figs_v2/chart_fig5a_census.png` | 484,884 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_fov_lines.png` | `ctsp:paper/cns2026/figs_v2/chart_fov_lines.png` | 179,797 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_headline.png` | `ctsp:paper/cns2026/figs_v2/chart_headline.png` | 170,866 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_l6.png` | `ctsp:paper/cns2026/figs_v2/chart_l6.png` | 138,243 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_level_accuracy.png` | `ctsp:paper/cns2026/figs_v2/chart_level_accuracy.png` | 245,873 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_level_sweep.png` | `ctsp:paper/cns2026/figs_v2/chart_level_sweep.png` | 363,325 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_machin_redrawn.png` | `ctsp:paper/cns2026/figs_v2/chart_machin_redrawn.png` | 340,585 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_power_with_census.png` | `ctsp:paper/cns2026/figs_v2/chart_power_with_census.png` | 480,735 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_priorart.png` | `ctsp:paper/cns2026/figs_v2/chart_priorart.png` | 184,325 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_rates.png` | `ctsp:paper/cns2026/figs_v2/chart_rates.png` | 253,229 |  |
| `manuscripts/talks/cns2026/figs_v2/chart_testset.png` | `ctsp:paper/cns2026/figs_v2/chart_testset.png` | 167,268 |  |
| `manuscripts/talks/cns2026/figs_v2/cited_bettis_fig1.png` | `ctsp:paper/cns2026/figs_v2/cited_bettis_fig1.png` | 448,161 |  |
| `manuscripts/talks/cns2026/figs_v2/cited_cost_composite.png` | `ctsp:paper/cns2026/figs_v2/cited_cost_composite.png` | 1,060,842 |  |
| `manuscripts/talks/cns2026/figs_v2/cited_levelcheck_composite.png` | `ctsp:paper/cns2026/figs_v2/cited_levelcheck_composite.png` | 1,076,681 |  |
| `manuscripts/talks/cns2026/figs_v2/cited_strong2022_fig3.png` | `ctsp:paper/cns2026/figs_v2/cited_strong2022_fig3.png` | 318,941 |  |
| `manuscripts/talks/cns2026/figs_v2/claims.json` | `ctsp:paper/cns2026/figs_v2/claims.json` | 3,226 |  |
| `manuscripts/talks/cns2026/figs_v2/diagram_disclosure.png` | `ctsp:paper/cns2026/figs_v2/diagram_disclosure.png` | 150,610 |  |
| `manuscripts/talks/cns2026/figs_v2/fig2_wide.png` | `ctsp:paper/cns2026/figs_v2/fig2_wide.png` | 1,121,039 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_anchors.png` | `ctsp:paper/cns2026/figs_v2/fig_anchors.png` | 618,745 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_countfree.png` | `ctsp:paper/cns2026/figs_v2/fig_countfree.png` | 119,091 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_fov.png` | `ctsp:paper/cns2026/figs_v2/fig_fov.png` | 27,509 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_hardware.png` | `ctsp:paper/cns2026/figs_v2/fig_hardware.png` | 414,779 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_levelatlas.png` | `ctsp:paper/cns2026/figs_v2/fig_levelatlas.png` | 112,579 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_opportunistic.png` | `ctsp:paper/cns2026/figs_v2/fig_opportunistic.png` | 98,903 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_phenotypes.png` | `ctsp:paper/cns2026/figs_v2/fig_phenotypes.png` | 430,104 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_pipeline.png` | `ctsp:paper/cns2026/figs_v2/fig_pipeline.png` | 166,708 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_priorart.png` | `ctsp:paper/cns2026/figs_v2/fig_priorart.png` | 163,489 |  |
| `manuscripts/talks/cns2026/figs_v2/fig_validation.png` | `ctsp:paper/cns2026/figs_v2/fig_validation.png` | 65,056 |  |
| `manuscripts/talks/cns2026/figs_v2/fov_lines.json` | `ctsp:paper/cns2026/figs_v2/fov_lines.json` | 1,064 |  |
| `manuscripts/talks/cns2026/figs_v2/gallery_case83.png` | `ctsp:paper/cns2026/figs_v2/gallery_case83.png` | 94,454 |  |
| `manuscripts/talks/cns2026/figs_v2/l6_result.json` | `ctsp:paper/cns2026/figs_v2/l6_result.json` | 328 |  |
| `manuscripts/talks/cns2026/figs_v2/level_accuracy.json` | `ctsp:paper/cns2026/figs_v2/level_accuracy.json` | 1,420 |  |
| `manuscripts/talks/cns2026/figs_v2/nas_gt_vs_ts.png` | `ctsp:paper/cns2026/figs_v2/nas_gt_vs_ts.png` | 532,422 |  |
| `manuscripts/talks/cns2026/figs_v2/nas_lumbarization_215.png` | `ctsp:paper/cns2026/figs_v2/nas_lumbarization_215.png` | 631,555 |  |
| `manuscripts/talks/cns2026/figs_v2/occlusion_2x2.png` | `ctsp:paper/cns2026/figs_v2/occlusion_2x2.png` | 950,320 |  |
| `manuscripts/talks/cns2026/figs_v2/occlusion_grid.png` | `ctsp:paper/cns2026/figs_v2/occlusion_grid.png` | 1,189,462 |  |
| `manuscripts/talks/cns2026/figs_v2/osc_logo.png` | `ctsp:paper/cns2026/figs_v2/osc_logo.png` | 53,444 |  |
| `manuscripts/talks/cns2026/figs_v2/osc_mark.png` | `ctsp:paper/cns2026/figs_v2/osc_mark.png` | 11,049 |  |
| `manuscripts/talks/cns2026/figs_v2/pictogram_census.png` | `ctsp:paper/cns2026/figs_v2/pictogram_census.png` | 205,465 |  |
| `manuscripts/talks/cns2026/figs_v2/render_case42_L6.png` | `ctsp:paper/cns2026/figs_v2/render_case42_L6.png` | 578,647 |  |
| `manuscripts/talks/cns2026/figs_v2/render_case42_check.png` | `ctsp:paper/cns2026/figs_v2/render_case42_check.png` | 547,172 |  |
| `manuscripts/talks/cns2026/figs_v2/render_case42_find.png` | `ctsp:paper/cns2026/figs_v2/render_case42_find.png` | 521,646 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_carmlspine_gallery.png` | `ctsp:paper/cns2026/figs_v2/sn_carmlspine_gallery.png` | 887,539 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_carmlspine_results.png` | `ctsp:paper/cns2026/figs_v2/sn_carmlspine_results.png` | 152,953 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_fig2_ab.png` | `ctsp:paper/cns2026/figs_v2/sn_fig2_ab.png` | 970,170 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_fig4_a_img.png` | `ctsp:paper/cns2026/figs_v2/sn_fig4_a_img.png` | 292,763 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_fig4_ab.png` | `ctsp:paper/cns2026/figs_v2/sn_fig4_ab.png` | 728,668 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_fig4_ab_img.png` | `ctsp:paper/cns2026/figs_v2/sn_fig4_ab_img.png` | 590,432 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_fig4_b_img.png` | `ctsp:paper/cns2026/figs_v2/sn_fig4_b_img.png` | 283,913 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_fig5_a.png` | `ctsp:paper/cns2026/figs_v2/sn_fig5_a.png` | 192,276 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_fig5_ab.png` | `ctsp:paper/cns2026/figs_v2/sn_fig5_ab.png` | 305,875 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_fig5_cd.png` | `ctsp:paper/cns2026/figs_v2/sn_fig5_cd.png` | 291,750 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_figS1_ab.png` | `ctsp:paper/cns2026/figs_v2/sn_figS1_ab.png` | 757,764 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_figS5_abc.png` | `ctsp:paper/cns2026/figs_v2/sn_figS5_abc.png` | 904,665 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_figure1.png` | `ctsp:paper/cns2026/figs_v2/sn_figure1.png` | 2,037,289 |  |
| `manuscripts/talks/cns2026/figs_v2/sn_table3_rotated.png` | `ctsp:paper/cns2026/figs_v2/sn_table3_rotated.png` | 509,882 |  |
| `manuscripts/talks/cns2026/figs_v2/sweep_curve.json` | `ctsp:paper/cns2026/figs_v2/sweep_curve.json` | 6,366 |  |
| `manuscripts/talks/cns2026/figs_v2/sweep_per_level.json` | `ctsp:paper/cns2026/figs_v2/sweep_per_level.json` | 22,397 |  |
| `manuscripts/talks/cns2026/figs_v2/table_census.png` | `ctsp:paper/cns2026/figs_v2/table_census.png` | 731,137 |  |
| `manuscripts/talks/cns2026/figs_v2/table_claims.png` | `ctsp:paper/cns2026/figs_v2/table_claims.png` | 385,027 |  |
| `manuscripts/talks/cns2026/figs_v2/table_corpus.png` | `ctsp:paper/cns2026/figs_v2/table_corpus.png` | 147,187 |  |
| `manuscripts/talks/cns2026/figs_v2/table_fov.png` | `ctsp:paper/cns2026/figs_v2/table_fov.png` | 194,259 |  |
| `manuscripts/talks/cns2026/figs_v2/table_levelcheck.png` | `ctsp:paper/cns2026/figs_v2/table_levelcheck.png` | 187,036 |  |
| `manuscripts/talks/cns2026/figs_v2/table_modalities.png` | `ctsp:paper/cns2026/figs_v2/table_modalities.png` | 150,217 |  |
| `manuscripts/talks/cns2026/figs_v2/table_result1.png` | `ctsp:paper/cns2026/figs_v2/table_result1.png` | 333,446 |  |
| `manuscripts/talks/cns2026/make_cns_deck.py` | `ctsp:paper/cns2026/make_cns_deck.py` | 25,600 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v10.py` | `ctsp:paper/cns2026/make_cns_deck_v10.py` | 33,807 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v11_public.py` | `ctsp:paper/cns2026/make_cns_deck_v11_public.py` | 22,176 | **word** (1) |
| `manuscripts/talks/cns2026/make_cns_deck_v12_public.py` | `ctsp:paper/cns2026/make_cns_deck_v12_public.py` | 26,709 | **word** (1) |
| `manuscripts/talks/cns2026/make_cns_deck_v2.py` | `ctsp:paper/cns2026/make_cns_deck_v2.py` | 30,009 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v3.py` | `ctsp:paper/cns2026/make_cns_deck_v3.py` | 34,474 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v4.py` | `ctsp:paper/cns2026/make_cns_deck_v4.py` | 28,125 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v5.py` | `ctsp:paper/cns2026/make_cns_deck_v5.py` | 25,052 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v6.py` | `ctsp:paper/cns2026/make_cns_deck_v6.py` | 26,429 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v7.py` | `ctsp:paper/cns2026/make_cns_deck_v7.py` | 27,852 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v8.py` | `ctsp:paper/cns2026/make_cns_deck_v8.py` | 31,160 |  |
| `manuscripts/talks/cns2026/make_cns_deck_v9.py` | `ctsp:paper/cns2026/make_cns_deck_v9.py` | 32,226 |  |
| `manuscripts/talks/cns2026/make_v3_charts.py` | `ctsp:paper/cns2026/make_v3_charts.py` | 16,425 |  |
| `manuscripts/talks/cns2026/posterior/analyze.py` | `ctsp:paper/cns2026/posterior/analyze.py` | 10,517 |  |
| `manuscripts/talks/cns2026/posterior/analyze.sbatch` | `ctsp:paper/cns2026/posterior/analyze.sbatch` | 814 |  |
| `manuscripts/talks/cns2026/posterior/fetch.sbatch` | `ctsp:paper/cns2026/posterior/fetch.sbatch` | 2,707 |  |
| `manuscripts/talks/cns2026/posterior/predict.sbatch` | `ctsp:paper/cns2026/posterior/predict.sbatch` | 2,689 |  |
| `manuscripts/talks/cns2026/posterior/submit.sh` | `ctsp:paper/cns2026/posterior/submit.sh` | 1,994 |  |
| `manuscripts/talks/cns2026/prep_bettis.py` | `ctsp:paper/cns2026/prep_bettis.py` | 8,274 |  |
| `manuscripts/talks/cns2026/prep_big_panels.py` | `ctsp:paper/cns2026/prep_big_panels.py` | 3,710 |  |
| `manuscripts/talks/cns2026/prep_cited_figs.py` | `ctsp:paper/cns2026/prep_cited_figs.py` | 3,536 |  |
| `manuscripts/talks/cns2026/prep_v10_figs.py` | `ctsp:paper/cns2026/prep_v10_figs.py` | 8,978 |  |
| `manuscripts/talks/cns2026/prep_v11_figs.py` | `ctsp:paper/cns2026/prep_v11_figs.py` | 10,878 |  |
| `manuscripts/talks/cns2026/prep_v12_figs.py` | `ctsp:paper/cns2026/prep_v12_figs.py` | 9,739 |  |
| `manuscripts/talks/cns2026/prep_v13_figs.py` | `ctsp:paper/cns2026/prep_v13_figs.py` | 6,939 |  |
| `manuscripts/talks/cns2026/prep_v14_figs.py` | `ctsp:paper/cns2026/prep_v14_figs.py` | 18,678 |  |
| `manuscripts/talks/cns2026/prep_v15_figs.py` | `ctsp:paper/cns2026/prep_v15_figs.py` | 7,619 |  |
| `manuscripts/talks/cns2026/prep_v16_public_figs.py` | `ctsp:paper/cns2026/prep_v16_public_figs.py` | 6,772 |  |
| `manuscripts/talks/cns2026/prep_v5_figs.py` | `ctsp:paper/cns2026/prep_v5_figs.py` | 8,348 |  |
| `manuscripts/talks/cns2026/prep_v6_figs.py` | `ctsp:paper/cns2026/prep_v6_figs.py` | 9,581 |  |
| `manuscripts/talks/cns2026/prep_v7_figs.py` | `ctsp:paper/cns2026/prep_v7_figs.py` | 6,700 |  |
| `manuscripts/talks/cns2026/prep_v8_table.py` | `ctsp:paper/cns2026/prep_v8_table.py` | 7,851 |  |
| `manuscripts/talks/cns2026/prep_v9_claims.py` | `ctsp:paper/cns2026/prep_v9_claims.py` | 6,559 |  |
| `manuscripts/talks/cns2026/render_case42.py` | `ctsp:paper/cns2026/render_case42.py` | 3,176 |  |
| `manuscripts/talks/cns2026/sweep_per_level.py` | `ctsp:paper/cns2026/sweep_per_level.py` | 5,832 |  |

### `memory/` (55 files, 134,016 B)

| destination | source | bytes | note |
|---|---|---|---|
| `memory/annotator-roster.md` | `HANDOFF/context/annotator-roster.md` | 1,487 | status line added |
| `memory/bash-heredoc-backslashes.md` | `HANDOFF/context/bash-heredoc-backslashes.md` | 1,218 | status line added |
| `memory/canonical-rib-triage.md` | `HANDOFF/context/canonical-rib-triage.md` | 1,640 | status line added |
| `memory/chart-preferences.md` | `HANDOFF/context/chart-preferences.md` | 3,071 | status line added |
| `memory/cns-deck-v2-2026-09-25.md` | `HANDOFF/context/cns-deck-v2-2026-09-25.md` | 13,497 | status line added |
| `memory/commit-directly-to-master.md` | `HANDOFF/context/commit-directly-to-master.md` | 1,038 | status line added |
| `memory/competitor-benchmark.md` | `HANDOFF/context/competitor-benchmark.md` | 4,606 | status line added |
| `memory/ct-volumes-are-pir-not-ras.md` | `HANDOFF/context/ct-volumes-are-pir-not-ras.md` | 2,226 | status line added |
| `memory/ctspine1k-selection-code-deleted.md` | `HANDOFF/context/ctspine1k-selection-code-deleted.md` | 2,428 | status line added |
| `memory/data-directives-2026-09-23.md` | `HANDOFF/context/data-directives-2026-09-23.md` | 2,342 | status line added |
| `memory/dataset813-image-links-are-container-paths.md` | `HANDOFF/context/dataset813-image-links-are-container-paths.md` | 1,639 | status line added |
| `memory/figure-captions-terse.md` | `HANDOFF/context/figure-captions-terse.md` | 1,486 | status line added |
| `memory/fluorocap-repo-private.md` | `HANDOFF/context/fluorocap-repo-private.md` | 1,631 | status line added |
| `memory/grid-access.md` | `HANDOFF/context/grid-access.md` | 1,708 | status line added |
| `memory/grid-bash-4-2-quoting.md` | `HANDOFF/context/grid-bash-4-2-quoting.md` | 1,606 | status line added |
| `memory/grid-ceph-volume-oschome.md` | `HANDOFF/context/grid-ceph-volume-oschome.md` | 1,492 | status line added |
| `memory/grid-ct-0533-truncated.md` | `HANDOFF/context/grid-ct-0533-truncated.md` | 3,321 | status line added |
| `memory/grid-local-singularity-is-broken.md` | `HANDOFF/context/grid-local-singularity-is-broken.md` | 2,577 | status line added |
| `memory/hf-identity.md` | `HANDOFF/context/hf-identity.md` | 853 | status line added |
| `memory/hf-mirror-is-v10.md` | `HANDOFF/context/hf-mirror-is-v10.md` | 2,112 | status line added |
| `memory/journal-figure-and-style-rules.md` | `HANDOFF/context/journal-figure-and-style-rules.md` | 2,401 | status line added |
| `memory/key-patients-from-metadata-not-filenames.md` | `HANDOFF/context/key-patients-from-metadata-not-filenames.md` | 2,368 | status line added |
| `memory/l6-sample-count-and-counting-decoder.md` | `HANDOFF/context/l6-sample-count-and-counting-decoder.md` | 2,199 | status line added |
| `memory/label-scheme-v4-vs-ostk.md` | `HANDOFF/context/label-scheme-v4-vs-ostk.md` | 2,648 | status line added |
| `memory/local-level-identity-thesis.md` | `HANDOFF/context/local-level-identity-thesis.md` | 1,952 | status line added |
| `memory/lstv-oneshot-training-run.md` | `HANDOFF/context/lstv-oneshot-training-run.md` | 6,712 | status line added |
| `memory/lstv-reread-queue.md` | `HANDOFF/context/lstv-reread-queue.md` | 1,545 | status line added |
| `memory/morphology-deformation-feasibility.md` | `HANDOFF/context/morphology-deformation-feasibility.md` | 2,476 | status line added |
| `memory/never-reorient-when-writing-labels.md` | `HANDOFF/context/never-reorient-when-writing-labels.md` | 2,117 | status line added |
| `memory/nninteractive-colab-versions.md` | `HANDOFF/context/nninteractive-colab-versions.md` | 4,114 | status line added |
| `memory/no-jobs-on-login-node.md` | `HANDOFF/context/no-jobs-on-login-node.md` | 2,357 | status line added |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | `HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md` | 2,306 | status line added |
| `memory/panjabi-1991-page-892.md` | `HANDOFF/context/panjabi-1991-page-892.md` | 3,260 | status line added |
| `memory/prone-supine-flexibility-future.md` | `HANDOFF/context/prone-supine-flexibility-future.md` | 1,452 | status line added |
| `memory/publication-roadmap.md` | `HANDOFF/context/publication-roadmap.md` | 4,362 | status line added |
| `memory/push-both-github-remotes.md` | `HANDOFF/context/push-both-github-remotes.md` | 1,195 | status line added |
| `memory/review-space-repos.md` | `HANDOFF/context/review-space-repos.md` | 2,118 | status line added |
| `memory/rib-approach-ts-trust.md` | `HANDOFF/context/rib-approach-ts-trust.md` | 3,132 | status line added |
| `memory/rib-auto-engulf-post-correction-only.md` | `HANDOFF/context/rib-auto-engulf-post-correction-only.md` | 1,958 | status line added |
| `memory/rib-qc-gates-never-block-lstv.md` | `HANDOFF/context/rib-qc-gates-never-block-lstv.md` | 2,011 | **redacted**: two student usernames withheld; status line added |
| `memory/s1-carve-changed-spinopelvic.md` | `HANDOFF/context/s1-carve-changed-spinopelvic.md` | 3,274 | status line added |
| `memory/scheme-bone-hardware-only.md` | `HANDOFF/context/scheme-bone-hardware-only.md` | 2,801 | status line added |
| `memory/scratchpad-shadows-stdlib.md` | `HANDOFF/context/scratchpad-shadows-stdlib.md` | 1,573 | status line added |
| `memory/splits-origin-and-v3-resplit.md` | `HANDOFF/context/splits-origin-and-v3-resplit.md` | 2,342 | status line added |
| `memory/spondylolysis-and-border-anomaly-findings.md` | `HANDOFF/context/spondylolysis-and-border-anomaly-findings.md` | 2,247 | status line added |
| `memory/submit-and-sleep-orchestration.md` | `HANDOFF/context/submit-and-sleep-orchestration.md` | 2,097 | status line added |
| `memory/tables-black-not-colour.md` | `HANDOFF/context/tables-black-not-colour.md` | 1,361 | status line added |
| `memory/thoracic-gt-fov-limited.md` | `HANDOFF/context/thoracic-gt-fov-limited.md` | 1,318 | status line added |
| `memory/ts-sacrum-excludes-s1.md` | `HANDOFF/context/ts-sacrum-excludes-s1.md` | 1,796 | status line added |
| `memory/user-affiliation-general-surgery.md` | `HANDOFF/context/user-affiliation-general-surgery.md` | 1,725 | status line added |
| `memory/windows-junction-worktree-trap.md` | `HANDOFF/context/windows-junction-worktree-trap.md` | 1,699 | status line added |
| `memory/writing-preferences.md` | `HANDOFF/context/writing-preferences.md` | 997 | status line added |
| `memory/wsl-for-network.md` | `HANDOFF/context/wsl-for-network.md` | 1,648 | status line added |
| `memory/wsu-library-access-cutoff.md` | `HANDOFF/context/wsu-library-access-cutoff.md` | 1,687 | status line added |
| `memory/zenodo-deposit.md` | `HANDOFF/context/zenodo-deposit.md` | 2,790 | status line added |

### `results/ctsp_results/` (28 files, 2,734,099 B)

| destination | source | bytes | note |
|---|---|---|---|
| `results/ctsp_results/pelvic_width/pelvic_width.csv` | `ctsp:results/pelvic_width/pelvic_width.csv` | 36,445 |  |
| `results/ctsp_results/pelvic_width/pelvic_width.pdf` | `ctsp:results/pelvic_width/pelvic_width.pdf` | 31,683 |  |
| `results/ctsp_results/pelvic_width/pelvic_width.png` | `ctsp:results/pelvic_width/pelvic_width.png` | 146,263 |  |
| `results/ctsp_results/pelvic_width/report.txt` | `ctsp:results/pelvic_width/report.txt` | 345 |  |
| `results/ctsp_results/pseudolabel_dice/README.md` | `ctsp:results/pseudolabel_dice/README.md` | 2,989 |  |
| `results/ctsp_results/pseudolabel_dice/dataset803_fold_validation_dice.csv` | `ctsp:results/pseudolabel_dice/dataset803_fold_validation_dice.csv` | 1,457 |  |
| `results/ctsp_results/pseudolabel_dice/dataset803_fold_validation_dice_summary.csv` | `ctsp:results/pseudolabel_dice/dataset803_fold_validation_dice_summary.csv` | 390 |  |
| `results/ctsp_results/reading_sheets/0068_reading_sheet.png` | `ctsp:results/reading_sheets/0068_reading_sheet.png` | 742,577 |  |
| `results/ctsp_results/reading_sheets/0376_reading_sheet.png` | `ctsp:results/reading_sheets/0376_reading_sheet.png` | 679,108 |  |
| `results/ctsp_results/reading_sheets/1053_reading_sheet.png` | `ctsp:results/reading_sheets/1053_reading_sheet.png` | 885,605 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/README.md` | `ctsp:results/rib_qc_v4_vs_release/README.md` | 3,871 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/fragments_release/rib_fragments_release.csv` | `ctsp:results/rib_qc_v4_vs_release/fragments_release/rib_fragments_release.csv` | 879 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/fragments_release/summary.json` | `ctsp:results/rib_qc_v4_vs_release/fragments_release/summary.json` | 286 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/fragments_v4/rib_fragments_release.csv` | `ctsp:results/rib_qc_v4_vs_release/fragments_v4/rib_fragments_release.csv` | 32,974 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/fragments_v4/summary.json` | `ctsp:results/rib_qc_v4_vs_release/fragments_v4/summary.json` | 296 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/gates_v4_vs_release.json` | `ctsp:results/rib_qc_v4_vs_release/gates_v4_vs_release.json` | 955 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/incidence_release.json` | `ctsp:results/rib_qc_v4_vs_release/incidence_release.json` | 321 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/incidence_v4.json` | `ctsp:results/rib_qc_v4_vs_release/incidence_v4.json` | 339 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/misnumbered_release.csv` | `ctsp:results/rib_qc_v4_vs_release/misnumbered_release.csv` | 42 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/misnumbered_v4.csv` | `ctsp:results/rib_qc_v4_vs_release/misnumbered_v4.csv` | 1,701 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/remap_v4.py` | `ctsp:results/rib_qc_v4_vs_release/remap_v4.py` | 1,803 |  |
| `results/ctsp_results/rib_qc_v4_vs_release/rib_qc_stages.py` | `ctsp:results/rib_qc_v4_vs_release/rib_qc_stages.py` | 7,491 |  |
| `results/ctsp_results/six_lumbar_readings/report.txt` | `ctsp:results/six_lumbar_readings/report.txt` | 2,154 |  |
| `results/ctsp_results/six_lumbar_readings/shift_hypothesis.csv` | `ctsp:results/six_lumbar_readings/shift_hypothesis.csv` | 5,552 |  |
| `results/ctsp_results/six_lumbar_readings/shift_hypothesis_report.txt` | `ctsp:results/six_lumbar_readings/shift_hypothesis_report.txt` | 1,924 |  |
| `results/ctsp_results/six_lumbar_readings/six_lumbar_readings.csv` | `ctsp:results/six_lumbar_readings/six_lumbar_readings.csv` | 1,826 |  |
| `results/ctsp_results/six_lumbar_readings/six_lumbar_readings.pdf` | `ctsp:results/six_lumbar_readings/six_lumbar_readings.pdf` | 19,454 |  |
| `results/ctsp_results/six_lumbar_readings/six_lumbar_readings.png` | `ctsp:results/six_lumbar_readings/six_lumbar_readings.png` | 125,369 |  |

### `results/flip18_review/` (19 files, 8,454,334 B)

| destination | source | bytes | note |
|---|---|---|---|
| `results/flip18_review/L6_review_form.csv` | `Desktop/NextPaper/flip18_review/L6_review_form.csv` | 2,573 |  |
| `results/flip18_review/castellvi_addendum.csv` | `Desktop/NextPaper/flip18_review/castellvi_addendum.csv` | 1,615 |  |
| `results/flip18_review/pngs/10_AP_.4.10410.png` | `Desktop/NextPaper/flip18_review/pngs/10_AP_.4.10410.png` | 420,287 |  |
| `results/flip18_review/pngs/10_AP_.4.10412.png` | `Desktop/NextPaper/flip18_review/pngs/10_AP_.4.10412.png` | 415,771 |  |
| `results/flip18_review/pngs/180_AP_4.202942.png` | `Desktop/NextPaper/flip18_review/pngs/180_AP_4.202942.png` | 457,579 |  |
| `results/flip18_review/pngs/180_AP_4.203499.png` | `Desktop/NextPaper/flip18_review/pngs/180_AP_4.203499.png` | 459,458 |  |
| `results/flip18_review/pngs/1_1.3.6.1.4.1.9328.50.4.2_propagation.png` | `Desktop/NextPaper/flip18_review/pngs/1_1.3.6.1.4.1.9328.50.4.2_propagation.png` | 530,960 |  |
| `results/flip18_review/pngs/247_AP_4.275513.png` | `Desktop/NextPaper/flip18_review/pngs/247_AP_4.275513.png` | 435,733 |  |
| `results/flip18_review/pngs/247_AP_4.276061.png` | `Desktop/NextPaper/flip18_review/pngs/247_AP_4.276061.png` | 436,667 |  |
| `results/flip18_review/pngs/277_lateral_4.308104.png` | `Desktop/NextPaper/flip18_review/pngs/277_lateral_4.308104.png` | 330,611 |  |
| `results/flip18_review/pngs/277_lateral_4.308649.png` | `Desktop/NextPaper/flip18_review/pngs/277_lateral_4.308649.png` | 331,184 |  |
| `results/flip18_review/pngs/307_AP_4.343468.png` | `Desktop/NextPaper/flip18_review/pngs/307_AP_4.343468.png` | 600,710 |  |
| `results/flip18_review/pngs/30_lateral_.4.31182.png` | `Desktop/NextPaper/flip18_review/pngs/30_lateral_.4.31182.png` | 497,315 |  |
| `results/flip18_review/pngs/30_lateral_.4.31755.png` | `Desktop/NextPaper/flip18_review/pngs/30_lateral_.4.31755.png` | 582,831 |  |
| `results/flip18_review/pngs/4_1.3.6.1.4.1.9328.50.4.4371_propagation.png` | `Desktop/NextPaper/flip18_review/pngs/4_1.3.6.1.4.1.9328.50.4.4371_propagation.png` | 509,720 |  |
| `results/flip18_review/pngs/6_1.3.6.1.4.1.9328.50.4.5980_propagation.png` | `Desktop/NextPaper/flip18_review/pngs/6_1.3.6.1.4.1.9328.50.4.5980_propagation.png` | 693,022 |  |
| `results/flip18_review/pngs/7_1.3.6.1.4.1.9328.50.4.7198_propagation.png` | `Desktop/NextPaper/flip18_review/pngs/7_1.3.6.1.4.1.9328.50.4.7198_propagation.png` | 549,575 |  |
| `results/flip18_review/pngs/8_1.3.6.1.4.1.9328.50.4.7889_propagation.png` | `Desktop/NextPaper/flip18_review/pngs/8_1.3.6.1.4.1.9328.50.4.7889_propagation.png` | 657,769 |  |
| `results/flip18_review/pngs/90_lateral_.4.96540.png` | `Desktop/NextPaper/flip18_review/pngs/90_lateral_.4.96540.png` | 540,954 |  |

### `results/hardware_review/` (109 files, 134,619 B)

| destination | source | bytes | note |
|---|---|---|---|
| `results/hardware_review/0023_hardware.json` | `ctsp:hardware_review/0023_hardware.json` | 1,134 |  |
| `results/hardware_review/0023_hardware_geometry.json` | `ctsp:hardware_review/0023_hardware_geometry.json` | 1,137 |  |
| `results/hardware_review/0027_hardware.json` | `ctsp:hardware_review/0027_hardware.json` | 878 |  |
| `results/hardware_review/0027_hardware_geometry.json` | `ctsp:hardware_review/0027_hardware_geometry.json` | 801 |  |
| `results/hardware_review/0068_hardware.json` | `ctsp:hardware_review/0068_hardware.json` | 945 |  |
| `results/hardware_review/0068_hardware_geometry.json` | `ctsp:hardware_review/0068_hardware_geometry.json` | 828 |  |
| `results/hardware_review/0100_hardware.json` | `ctsp:hardware_review/0100_hardware.json` | 1,140 |  |
| `results/hardware_review/0100_hardware_geometry.json` | `ctsp:hardware_review/0100_hardware_geometry.json` | 1,142 |  |
| `results/hardware_review/0101_hardware.json` | `ctsp:hardware_review/0101_hardware.json` | 491 |  |
| `results/hardware_review/0101_hardware_geometry.json` | `ctsp:hardware_review/0101_hardware_geometry.json` | 434 |  |
| `results/hardware_review/0140_hardware.json` | `ctsp:hardware_review/0140_hardware.json` | 533 |  |
| `results/hardware_review/0140_hardware_geometry.json` | `ctsp:hardware_review/0140_hardware_geometry.json` | 434 |  |
| `results/hardware_review/0150_hardware.json` | `ctsp:hardware_review/0150_hardware.json` | 538 |  |
| `results/hardware_review/0150_hardware_geometry.json` | `ctsp:hardware_review/0150_hardware_geometry.json` | 433 |  |
| `results/hardware_review/0158_hardware.json` | `ctsp:hardware_review/0158_hardware.json` | 1,158 |  |
| `results/hardware_review/0188_hardware.json` | `ctsp:hardware_review/0188_hardware.json` | 1,313 |  |
| `results/hardware_review/0188_hardware_geometry.json` | `ctsp:hardware_review/0188_hardware_geometry.json` | 1,139 |  |
| `results/hardware_review/0247_hardware.json` | `ctsp:hardware_review/0247_hardware.json` | 1,974 |  |
| `results/hardware_review/0247_hardware_geometry.json` | `ctsp:hardware_review/0247_hardware_geometry.json` | 1,842 |  |
| `results/hardware_review/0302_hardware.json` | `ctsp:hardware_review/0302_hardware.json` | 811 |  |
| `results/hardware_review/0302_hardware_geometry.json` | `ctsp:hardware_review/0302_hardware_geometry.json` | 776 |  |
| `results/hardware_review/0317_hardware.json` | `ctsp:hardware_review/0317_hardware.json` | 1,140 |  |
| `results/hardware_review/0317_hardware_geometry.json` | `ctsp:hardware_review/0317_hardware_geometry.json` | 1,146 |  |
| `results/hardware_review/0334_hardware.json` | `ctsp:hardware_review/0334_hardware.json` | 531 |  |
| `results/hardware_review/0334_hardware_geometry.json` | `ctsp:hardware_review/0334_hardware_geometry.json` | 452 |  |
| `results/hardware_review/0342_hardware.json` | `ctsp:hardware_review/0342_hardware.json` | 534 |  |
| `results/hardware_review/0342_hardware_geometry.json` | `ctsp:hardware_review/0342_hardware_geometry.json` | 453 |  |
| `results/hardware_review/0345_hardware.json` | `ctsp:hardware_review/0345_hardware.json` | 531 |  |
| `results/hardware_review/0345_hardware_geometry.json` | `ctsp:hardware_review/0345_hardware_geometry.json` | 434 |  |
| `results/hardware_review/0355_hardware.json` | `ctsp:hardware_review/0355_hardware.json` | 531 |  |
| `results/hardware_review/0355_hardware_geometry.json` | `ctsp:hardware_review/0355_hardware_geometry.json` | 430 |  |
| `results/hardware_review/0371_hardware.json` | `ctsp:hardware_review/0371_hardware.json` | 534 |  |
| `results/hardware_review/0371_hardware_geometry.json` | `ctsp:hardware_review/0371_hardware_geometry.json` | 431 |  |
| `results/hardware_review/0375_hardware.json` | `ctsp:hardware_review/0375_hardware.json` | 533 |  |
| `results/hardware_review/0375_hardware_geometry.json` | `ctsp:hardware_review/0375_hardware_geometry.json` | 436 |  |
| `results/hardware_review/0391_hardware.json` | `ctsp:hardware_review/0391_hardware.json` | 537 |  |
| `results/hardware_review/0391_hardware_geometry.json` | `ctsp:hardware_review/0391_hardware_geometry.json` | 432 |  |
| `results/hardware_review/0394_hardware.json` | `ctsp:hardware_review/0394_hardware.json` | 874 |  |
| `results/hardware_review/0394_hardware_geometry.json` | `ctsp:hardware_review/0394_hardware_geometry.json` | 806 |  |
| `results/hardware_review/0421_hardware.json` | `ctsp:hardware_review/0421_hardware.json` | 844 |  |
| `results/hardware_review/0421_hardware_geometry.json` | `ctsp:hardware_review/0421_hardware_geometry.json` | 803 |  |
| `results/hardware_review/0428_hardware.json` | `ctsp:hardware_review/0428_hardware.json` | 537 |  |
| `results/hardware_review/0428_hardware_geometry.json` | `ctsp:hardware_review/0428_hardware_geometry.json` | 438 |  |
| `results/hardware_review/0441_hardware.json` | `ctsp:hardware_review/0441_hardware.json` | 538 |  |
| `results/hardware_review/0441_hardware_geometry.json` | `ctsp:hardware_review/0441_hardware_geometry.json` | 436 |  |
| `results/hardware_review/0442_hardware.json` | `ctsp:hardware_review/0442_hardware.json` | 493 |  |
| `results/hardware_review/0442_hardware_geometry.json` | `ctsp:hardware_review/0442_hardware_geometry.json` | 434 |  |
| `results/hardware_review/0443_hardware.json` | `ctsp:hardware_review/0443_hardware.json` | 1,631 |  |
| `results/hardware_review/0443_hardware_geometry.json` | `ctsp:hardware_review/0443_hardware_geometry.json` | 1,478 |  |
| `results/hardware_review/0469_hardware.json` | `ctsp:hardware_review/0469_hardware.json` | 531 |  |
| `results/hardware_review/0469_hardware_geometry.json` | `ctsp:hardware_review/0469_hardware_geometry.json` | 437 |  |
| `results/hardware_review/0485_hardware.json` | `ctsp:hardware_review/0485_hardware.json` | 988 |  |
| `results/hardware_review/0485_hardware_geometry.json` | `ctsp:hardware_review/0485_hardware_geometry.json` | 794 |  |
| `results/hardware_review/0493_hardware.json` | `ctsp:hardware_review/0493_hardware.json` | 886 |  |
| `results/hardware_review/0493_hardware_geometry.json` | `ctsp:hardware_review/0493_hardware_geometry.json` | 774 |  |
| `results/hardware_review/0509_hardware.json` | `ctsp:hardware_review/0509_hardware.json` | 534 |  |
| `results/hardware_review/0509_hardware_geometry.json` | `ctsp:hardware_review/0509_hardware_geometry.json` | 436 |  |
| `results/hardware_review/0515_hardware.json` | `ctsp:hardware_review/0515_hardware.json` | 1,040 |  |
| `results/hardware_review/0515_hardware_geometry.json` | `ctsp:hardware_review/0515_hardware_geometry.json` | 798 |  |
| `results/hardware_review/0527_hardware.json` | `ctsp:hardware_review/0527_hardware.json` | 533 |  |
| `results/hardware_review/0527_hardware_geometry.json` | `ctsp:hardware_review/0527_hardware_geometry.json` | 436 |  |
| `results/hardware_review/0550_hardware.json` | `ctsp:hardware_review/0550_hardware.json` | 535 |  |
| `results/hardware_review/0550_hardware_geometry.json` | `ctsp:hardware_review/0550_hardware_geometry.json` | 438 |  |
| `results/hardware_review/0577_hardware.json` | `ctsp:hardware_review/0577_hardware.json` | 536 |  |
| `results/hardware_review/0577_hardware_geometry.json` | `ctsp:hardware_review/0577_hardware_geometry.json` | 435 |  |
| `results/hardware_review/0646_hardware.json` | `ctsp:hardware_review/0646_hardware.json` | 3,009 |  |
| `results/hardware_review/0646_hardware_geometry.json` | `ctsp:hardware_review/0646_hardware_geometry.json` | 3,213 |  |
| `results/hardware_review/0671_hardware.json` | `ctsp:hardware_review/0671_hardware.json` | 1,018 |  |
| `results/hardware_review/0671_hardware_geometry.json` | `ctsp:hardware_review/0671_hardware_geometry.json` | 795 |  |
| `results/hardware_review/0750_hardware.json` | `ctsp:hardware_review/0750_hardware.json` | 1,152 |  |
| `results/hardware_review/0750_hardware_geometry.json` | `ctsp:hardware_review/0750_hardware_geometry.json` | 1,127 |  |
| `results/hardware_review/0763_hardware.json` | `ctsp:hardware_review/0763_hardware.json` | 567 |  |
| `results/hardware_review/0763_hardware_geometry.json` | `ctsp:hardware_review/0763_hardware_geometry.json` | 457 |  |
| `results/hardware_review/0816_hardware.json` | `ctsp:hardware_review/0816_hardware.json` | 2,906 |  |
| `results/hardware_review/0816_hardware_geometry.json` | `ctsp:hardware_review/0816_hardware_geometry.json` | 3,228 |  |
| `results/hardware_review/0831_hardware.json` | `ctsp:hardware_review/0831_hardware.json` | 522 |  |
| `results/hardware_review/0831_hardware_geometry.json` | `ctsp:hardware_review/0831_hardware_geometry.json` | 446 |  |
| `results/hardware_review/0855_hardware.json` | `ctsp:hardware_review/0855_hardware.json` | 531 |  |
| `results/hardware_review/0855_hardware_geometry.json` | `ctsp:hardware_review/0855_hardware_geometry.json` | 430 |  |
| `results/hardware_review/0878_hardware.json` | `ctsp:hardware_review/0878_hardware.json` | 6,011 |  |
| `results/hardware_review/0878_hardware_geometry.json` | `ctsp:hardware_review/0878_hardware_geometry.json` | 6,240 |  |
| `results/hardware_review/0885_hardware.json` | `ctsp:hardware_review/0885_hardware.json` | 571 |  |
| `results/hardware_review/0885_hardware_geometry.json` | `ctsp:hardware_review/0885_hardware_geometry.json` | 435 |  |
| `results/hardware_review/0895_hardware.json` | `ctsp:hardware_review/0895_hardware.json` | 531 |  |
| `results/hardware_review/0895_hardware_geometry.json` | `ctsp:hardware_review/0895_hardware_geometry.json` | 433 |  |
| `results/hardware_review/0948_hardware.json` | `ctsp:hardware_review/0948_hardware.json` | 567 |  |
| `results/hardware_review/0948_hardware_geometry.json` | `ctsp:hardware_review/0948_hardware_geometry.json` | 434 |  |
| `results/hardware_review/0972_hardware.json` | `ctsp:hardware_review/0972_hardware.json` | 531 |  |
| `results/hardware_review/0972_hardware_geometry.json` | `ctsp:hardware_review/0972_hardware_geometry.json` | 438 |  |
| `results/hardware_review/0974_hardware.json` | `ctsp:hardware_review/0974_hardware.json` | 1,675 |  |
| `results/hardware_review/0974_hardware_geometry.json` | `ctsp:hardware_review/0974_hardware_geometry.json` | 1,475 |  |
| `results/hardware_review/1003_hardware.json` | `ctsp:hardware_review/1003_hardware.json` | 633 |  |
| `results/hardware_review/1003_hardware_geometry.json` | `ctsp:hardware_review/1003_hardware_geometry.json` | 442 |  |
| `results/hardware_review/1010_hardware.json` | `ctsp:hardware_review/1010_hardware.json` | 880 |  |
| `results/hardware_review/1010_hardware_geometry.json` | `ctsp:hardware_review/1010_hardware_geometry.json` | 790 |  |
| `results/hardware_review/1035_hardware.json` | `ctsp:hardware_review/1035_hardware.json` | 1,062 |  |
| `results/hardware_review/1035_hardware_geometry.json` | `ctsp:hardware_review/1035_hardware_geometry.json` | 848 |  |
| `results/hardware_review/1048_hardware.json` | `ctsp:hardware_review/1048_hardware.json` | 845 |  |
| `results/hardware_review/1048_hardware_geometry.json` | `ctsp:hardware_review/1048_hardware_geometry.json` | 773 |  |
| `results/hardware_review/1111_hardware.json` | `ctsp:hardware_review/1111_hardware.json` | 526 |  |
| `results/hardware_review/1111_hardware_geometry.json` | `ctsp:hardware_review/1111_hardware_geometry.json` | 449 |  |
| `results/hardware_review/1128_hardware.json` | `ctsp:hardware_review/1128_hardware.json` | 985 |  |
| `results/hardware_review/1128_hardware_geometry.json` | `ctsp:hardware_review/1128_hardware_geometry.json` | 787 |  |
| `results/hardware_review/README.md` | `ctsp:hardware_review/README.md` | 4,233 |  |
| `results/hardware_review/applied.json` | `ctsp:hardware_review/applied.json` | 2,132 |  |
| `results/hardware_review/hardware_manifest.csv` | `ctsp:hardware_review/hardware_manifest.csv` | 6,074 |  |
| `results/hardware_review/hardware_manifest.json` | `ctsp:hardware_review/hardware_manifest.json` | 17,196 |  |
| `results/hardware_review/review_index.csv` | `ctsp:hardware_review/review_index.csv` | 7,680 |  |
| `results/hardware_review/review_log.csv` | `ctsp:hardware_review/review_log.csv` | 1,133 |  |

### `results/neurips_2026-05/` (32 files, 8,067,132 B)

| destination | source | bytes | note |
|---|---|---|---|
| `results/neurips_2026-05/audit/benchmark_per_case.csv` | `Desktop/NeurIPS/audit/benchmark_per_case.csv` | 261,385 |  |
| `results/neurips_2026-05/audit/benchmark_per_case_record_level.csv` | `Desktop/NeurIPS/audit/benchmark_per_case_record_level.csv` | 295,208 |  |
| `results/neurips_2026-05/audit/benchmark_results.json` | `Desktop/NeurIPS/audit/benchmark_results.json` | 2,048,357 |  |
| `results/neurips_2026-05/audit/benchmark_summary.json` | `Desktop/NeurIPS/audit/benchmark_summary.json` | 47,137 |  |
| `results/neurips_2026-05/audit/benchmark_summary_record_level.json` | `Desktop/NeurIPS/audit/benchmark_summary_record_level.json` | 47,023 |  |
| `results/neurips_2026-05/audit/paper_tables.txt` | `Desktop/NeurIPS/audit/paper_tables.txt` | 5,097 |  |
| `results/neurips_2026-05/audit/paper_tables_record_level.txt` | `Desktop/NeurIPS/audit/paper_tables_record_level.txt` | 5,142 |  |
| `results/neurips_2026-05/audit/per_case_partial.jsonl` | `Desktop/NeurIPS/audit/per_case_partial.jsonl` | 1,233,526 |  |
| `results/neurips_2026-05/bm/benchmark_per_case.csv` | `Desktop/NeurIPS/bm/benchmark_per_case.csv` | 261,385 |  |
| `results/neurips_2026-05/bm/benchmark_per_case_record_level.csv` | `Desktop/NeurIPS/bm/benchmark_per_case_record_level.csv` | 295,208 |  |
| `results/neurips_2026-05/bm/benchmark_results.json` | `Desktop/NeurIPS/bm/benchmark_results.json` | 2,048,357 |  |
| `results/neurips_2026-05/bm/benchmark_summary.json` | `Desktop/NeurIPS/bm/benchmark_summary.json` | 47,137 |  |
| `results/neurips_2026-05/bm/benchmark_summary_record_level.json` | `Desktop/NeurIPS/bm/benchmark_summary_record_level.json` | 47,023 |  |
| `results/neurips_2026-05/bm/neurips_2026.tex` | `Desktop/NeurIPS/bm/neurips_2026.tex` | 47,349 | **word** (4) |
| `results/neurips_2026-05/bm/paper_tables.txt` | `Desktop/NeurIPS/bm/paper_tables.txt` | 5,097 |  |
| `results/neurips_2026-05/bm/paper_tables_record_level.txt` | `Desktop/NeurIPS/bm/paper_tables_record_level.txt` | 5,142 |  |
| `results/neurips_2026-05/bm/per_case_partial.jsonl` | `Desktop/NeurIPS/bm/per_case_partial.jsonl` | 1,233,526 |  |
| `results/neurips_2026-05/ens/confusion_blocks.json` | `Desktop/NeurIPS/ens/confusion_blocks.json` | 3,170 |  |
| `results/neurips_2026-05/ens/cross/cross_fold_confusion.json` | `Desktop/NeurIPS/ens/cross/cross_fold_confusion.json` | 3,016 |  |
| `results/neurips_2026-05/ens/cross/cross_fold_headline.json` | `Desktop/NeurIPS/ens/cross/cross_fold_headline.json` | 6,094 |  |
| `results/neurips_2026-05/ens/cross/cross_fold_summary.csv` | `Desktop/NeurIPS/ens/cross/cross_fold_summary.csv` | 2,542 |  |
| `results/neurips_2026-05/ens/cross/cross_fold_summary.md` | `Desktop/NeurIPS/ens/cross/cross_fold_summary.md` | 3,492 |  |
| `results/neurips_2026-05/ens/eval.log` | `Desktop/NeurIPS/ens/eval.log` | 15,765 |  |
| `results/neurips_2026-05/ens/headline.json` | `Desktop/NeurIPS/ens/headline.json` | 1,105 |  |
| `results/neurips_2026-05/ens/per_case_dice.csv` | `Desktop/NeurIPS/ens/per_case_dice.csv` | 52,191 |  |
| `results/neurips_2026-05/ens/subgroup_summary.csv` | `Desktop/NeurIPS/ens/subgroup_summary.csv` | 2,187 |  |
| `results/neurips_2026-05/ens/subgroup_summary.md` | `Desktop/NeurIPS/ens/subgroup_summary.md` | 2,975 |  |
| `results/neurips_2026-05/pred/croissant.json` | `Desktop/NeurIPS/pred/croissant.json` | 7,786 |  |
| `results/neurips_2026-05/pred/headline.json` | `Desktop/NeurIPS/pred/headline.json` | 533 |  |
| `results/neurips_2026-05/pred/per_case_dice.csv` | `Desktop/NeurIPS/pred/per_case_dice.csv` | 29,495 |  |
| `results/neurips_2026-05/pred/subgroup_summary.csv` | `Desktop/NeurIPS/pred/subgroup_summary.csv` | 1,910 |  |
| `results/neurips_2026-05/pred/subgroup_summary.md` | `Desktop/NeurIPS/pred/subgroup_summary.md` | 1,772 |  |

### `results/nextpaper/` (3 files, 956,181 B)

| destination | source | bytes | note |
|---|---|---|---|
| `results/nextpaper/ACRIN-6664_protocol.pdf` | `Desktop/NextPaper/ACRIN-6664_protocol.pdf` | 568,106 |  |
| `results/nextpaper/TCIA-CTC-large-10-mm-polyps.xls` | `Desktop/NextPaper/TCIA-CTC-large-10-mm-polyps.xls` | 25,088 |  |
| `results/nextpaper/manifest.csv` | `Desktop/NextPaper/manifest.csv` | 362,987 |  |

### `results/nextpaper_viz/` (3 files, 50,571 B)

| destination | source | bytes | note |
|---|---|---|---|
| `results/nextpaper_viz/1647658981_report.html` | `Desktop/NextPaper/viz/1647658981_report.html` | 18,134 |  |
| `results/nextpaper_viz/2413888034_report.html` | `Desktop/NextPaper/viz/2413888034_report.html` | 18,084 |  |
| `results/nextpaper_viz/index.html` | `Desktop/NextPaper/viz/index.html` | 14,353 |  |

### `results/qc/` (19 files, 3,555,135 B)

| destination | source | bytes | note |
|---|---|---|---|
| `results/qc/qc_final/break_fixes.csv` | `ctsp:qc_final/break_fixes.csv` | 25,924 |  |
| `results/qc/qc_final/break_fixes_pass2.csv` | `ctsp:qc_final/break_fixes_pass2.csv` | 20,015 |  |
| `results/qc/qc_final/deposit_audit.csv` | `ctsp:qc_final/deposit_audit.csv` | 820,856 |  |
| `results/qc/qc_final/deposit_audit_full.csv` | `ctsp:qc_final/deposit_audit_full.csv` | 1,174,965 |  |
| `results/qc/qc_final/detached_causes.csv` | `ctsp:qc_final/detached_causes.csv` | 12,097 |  |
| `results/qc/qc_final/envelope_violations.csv` | `ctsp:qc_final/envelope_violations.csv` | 33,138 |  |
| `results/qc/qc_final/gap_closures.csv` | `ctsp:qc_final/gap_closures.csv` | 13,616 |  |
| `results/qc/qc_final/label_dust.csv` | `ctsp:qc_final/label_dust.csv` | 494,059 |  |
| `results/qc/qc_final/label_dust_after.csv` | `ctsp:qc_final/label_dust_after.csv` | 166,870 |  |
| `results/qc/qc_final/qc_invariants.csv` | `ctsp:qc_final/qc_invariants.csv` | 6,433 |  |
| `results/qc/qc_final/rib_incidence.csv` | `ctsp:qc_final/rib_incidence.csv` | 657,488 |  |
| `results/qc/qc_final/speckle_cleanup.csv` | `ctsp:qc_final/speckle_cleanup.csv` | 80,702 |  |
| `results/qc/qc_final/summary.json` | `ctsp:qc_final/summary.json` | 282 |  |
| `results/qc/qc_final/v5_drift.csv` | `ctsp:qc_final/v5_drift.csv` | 329 |  |
| `results/qc/qc_final/v5pre_percase.csv` | `ctsp:qc_final/v5pre_percase.csv` | 33,799 |  |
| `results/qc/qc_final/version_progression.csv` | `ctsp:qc_final/version_progression.csv` | 504 |  |
| `results/qc/qc_hardware/consolidation.csv` | `ctsp:qc_hardware/consolidation.csv` | 3,917 |  |
| `results/qc/qc_hardware/hardware_scan.csv` | `ctsp:qc_hardware/hardware_scan.csv` | 3,105 |  |
| `results/qc/qc_hardware/verdicts.csv` | `ctsp:qc_hardware/verdicts.csv` | 7,036 |  |

### `results/root_qc_tables/` (15 files, 281,026 B)

| destination | source | bytes | note |
|---|---|---|---|
| `results/root_qc_tables/Lumbosac.csv` | `ctsp:Lumbosac.csv` | 2,044 | **redacted**: reader initials and names replaced by A/B/C |
| `results/root_qc_tables/Path.csv` | `ctsp:Path.csv` | 84,426 |  |
| `results/root_qc_tables/_lstv_phenotypes.csv` | `ctsp:_lstv_phenotypes.csv` | 1,684 |  |
| `results/root_qc_tables/adjudication_list.csv` | `ctsp:adjudication_list.csv` | 148 | **redacted**: student review handles replaced by annotator_NN (map withheld; Greg's own public handle kept) |
| `results/root_qc_tables/auto_finalize_manifest.csv` | `ctsp:auto_finalize_manifest.csv` | 776 | **redacted**: student review handles replaced by annotator_NN (map withheld; Greg's own public handle kept) |
| `results/root_qc_tables/lumbar_ribs.csv` | `ctsp:lumbar_ribs.csv` | 847 |  |
| `results/root_qc_tables/missing_vertebra.csv` | `ctsp:missing_vertebra.csv` | 1,082 |  |
| `results/root_qc_tables/qc_fail_candidates.csv` | `ctsp:qc_fail_candidates.csv` | 1,179 |  |
| `results/root_qc_tables/rib_qc_fail.csv` | `ctsp:rib_qc_fail.csv` | 86,307 |  |
| `results/root_qc_tables/rib_worklist.json` | `ctsp:rib_worklist.json` | 38,963 |  |
| `results/root_qc_tables/spine_pelvis_mixing.csv` | `ctsp:spine_pelvis_mixing.csv` | 24,853 |  |
| `results/root_qc_tables/spine_restored_manifest.csv` | `ctsp:spine_restored_manifest.csv` | 6,345 | **redacted**: student review handles replaced by annotator_NN (map withheld; Greg's own public handle kept) |
| `results/root_qc_tables/stray_vertebrae.csv` | `ctsp:stray_vertebrae.csv` | 2,485 |  |
| `results/root_qc_tables/stray_vertebrae.done.txt` | `ctsp:stray_vertebrae.done.txt` | 4,812 |  |
| `results/root_qc_tables/stump_rib_candidates.csv` | `ctsp:stump_rib_candidates.csv` | 25,075 |  |

## 2. Valuable files inside the copied folders that the rules skipped (reference by path)

These sat inside a folder whose other files were copied. They are listed so a reader knows they exist and why
they are not here. Imaging volumes stay where they are (the release copies of the same records are on the grid,
`MANIFEST_GRID.md` section 1).

### LaTeX build intermediate (21 files, 202,396 B)

| source | bytes | job |
|---|---|---|
| `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.aux` | 31,569 | `manuscripts/neurips_camera_ready` |
| `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.bbl` | 17,179 | `manuscripts/neurips_camera_ready` |
| `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.blg` | 925 | `manuscripts/neurips_camera_ready` |
| `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.fdb_latexmk` | 20,699 | `manuscripts/neurips_camera_ready` |
| `ctsp:CAMERA_READY_NEURIPS/src/neurips_2026.fls` | 24,483 | `manuscripts/neurips_camera_ready` |
| `ctsp:paper/mpda/arxiv/main.bbl` | 332 | `manuscripts/mpda` |
| `ctsp:paper/mpda/bibtest.aux` | 2,556 | `manuscripts/mpda` |
| `ctsp:paper/mpda/bibtest.bbl` | 13,599 | `manuscripts/mpda` |
| `ctsp:paper/mpda/bibtest.blg` | 915 | `manuscripts/mpda` |
| `ctsp:paper/mpda/fig_pipeline_standalone.aux` | 32 | `manuscripts/mpda` |
| `ctsp:paper/mpda/main.aux` | 11,697 | `manuscripts/mpda` |
| `ctsp:paper/mpda/reprint_check.aux` | 14,152 | `manuscripts/mpda` |
| `ctsp:paper/mpda/supplementary.aux` | 3,089 | `manuscripts/mpda` |
| `ctsp:paper/mpda/title_page.aux` | 162 | `manuscripts/mpda` |
| `ctsp:paper/mpda/typeset_preview.aux` | 11,403 | `manuscripts/mpda` |
| `Desktop/NextPaper/AR/neurips_2026.aux` | 24,970 | `manuscripts/nextpaper_ar_2026-09-08` |
| `Desktop/NextPaper/AR/neurips_2026.bbl` | 10,168 | `manuscripts/nextpaper_ar_2026-09-08` |
| `Desktop/NextPaper/AR/neurips_2026.blg` | 922 | `manuscripts/nextpaper_ar_2026-09-08` |
| `Desktop/NextPaper/RadAI/main.aux` | 5,086 | `manuscripts/nextpaper_radai` |
| `Desktop/NextPaper/RadAI/main.bbl` | 7,561 | `manuscripts/nextpaper_radai` |
| `Desktop/NextPaper/RadAI/main.blg` | 897 | `manuscripts/nextpaper_radai` |

### excluded by job rule (25 files, 21,222,903 B)

| source | bytes | job |
|---|---|---|
| `ctsp:paper/cns2026/abs418_tables.json` | 1,873 | `manuscripts/talks/cns2026` |
| `ctsp:paper/mpda/CTSP_OTHERSTUDENTS.docx` | 1,829,032 | `manuscripts/mpda` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_arxiv_preview.pdf` | 1,461,407 | `manuscripts/mpda` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_coauthor_draft.docx` | 1,794,286 | `manuscripts/mpda` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_coauthor_draft.pdf` | 1,121,454 | `manuscripts/mpda` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_coauthor_single_column.docx` | 886,222 | `manuscripts/mpda` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_review.docx` | 860,380 | `manuscripts/mpda` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_review.pdf` | 1,249,194 | `manuscripts/mpda` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_schehr revisions + sources notes.docx` | 2,318,428 | `manuscripts/mpda` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_single_column.docx` | 1,129,740 | `manuscripts/mpda` |
| `ctsp:paper/mpda/DUPLICATE_THORACIC.pdf` | 861,004 | `manuscripts/mpda` |
| `ctsp:paper/mpda/EMAIL_ASHLEY.md` | 4,237 | `manuscripts/mpda` |
| `ctsp:paper/mpda/FROM_ARXIV.pdf` | 1,179,922 | `manuscripts/mpda` |
| `ctsp:paper/mpda/_len.pdf` | 816,374 | `manuscripts/mpda` |
| `ctsp:paper/mpda/bibtest.log` | 8,496 | `manuscripts/mpda` |
| `ctsp:paper/mpda/bibtest.pdf` | 88,240 | `manuscripts/mpda` |
| `ctsp:paper/mpda/bibtest.tex` | 989 | `manuscripts/mpda` |
| `ctsp:paper/mpda/reprint_check.tex` | 69,928 | `manuscripts/mpda` |
| `ctsp:paper/mpda/typeset_preview.log` | 38,169 | `manuscripts/mpda` |
| `ctsp:paper/mpda/typeset_preview.out` | 4,894 | `manuscripts/mpda` |
| `ctsp:paper/mpda/typeset_preview.pdf` | 1,161,340 | `manuscripts/mpda` |
| `ctsp:paper/mpda/typeset_preview.tex` | 69,543 | `manuscripts/mpda` |
| `ctsp:paper/mpda/updated references.docx` | 2,321,351 | `manuscripts/mpda` |
| `Desktop/NeurIPS/lstv_review/lstv_review/Mahato_2020_LSTV_classification.pdf` | 1,911,676 | `code/lstv_review_tool` |
| `Desktop/NextPaper/AR/elsarticle-template-harv.tex` | 34,724 | `manuscripts/nextpaper_ar_2026-09-08` |

### imaging data, weights or archive (102 files, 9,713,579,414 B)

| source | bytes | job |
|---|---|---|
| `ctsp:_review_0816/0816_ct.nii.gz` | 161,823,090 | `code/case_fixes/_review_0816` |
| `ctsp:_review_0816/0816_label_completed.nii.gz` | 1,087,700 | `code/case_fixes/_review_0816` |
| `ctsp:_review_0816/0816_label_v4.nii.gz` | 1,106,588 | `code/case_fixes/_review_0816` |
| `ctsp:_review_0816/0816_label_v5.nii.gz` | 1,106,910 | `code/case_fixes/_review_0816` |
| `ctsp:_review_0816/0816_label_v6.nii.gz` | 1,107,035 | `code/case_fixes/_review_0816` |
| `ctsp:_verify_0816/0816_ct.nii.gz` | 161,823,090 | `code/case_fixes/_verify_0816` |
| `ctsp:_verify_0816/0816_label.nii.gz` | 1,126,001 | `code/case_fixes/_verify_0816` |
| `ctsp:_verify_0816/va/0068_ct.nii.gz` | 257,988,016 | `code/case_fixes/_verify_0816` |
| `ctsp:_verify_0816/va/0068_label_v5.nii.gz` | 2,324,575 | `code/case_fixes/_verify_0816` |
| `ctsp:_verify_0816/va/0068_label_v6.nii.gz` | 2,362,972 | `code/case_fixes/_verify_0816` |
| `ctsp:_verify_0816/va/0231_ct.nii.gz` | 192,318,582 | `code/case_fixes/_verify_0816` |
| `ctsp:_verify_0816/va/0231_label_v4.nii.gz` | 1,894,501 | `code/case_fixes/_verify_0816` |
| `ctsp:_verify_0816/va/0231_label_v6.nii.gz` | 1,892,158 | `code/case_fixes/_verify_0816` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_arxiv.tar.gz` | 1,105,131 | `manuscripts/mpda` |
| `ctsp:thoracic_fix/0068/0068_ct.nii.gz` | 257,988,016 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/0068_hardware_only.nii.gz` | 1,325,314 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/0068_label_FULL.nii.gz` | 2,365,404 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/0068_label_RENUMBERED.nii.gz` | 2,365,381 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/0068_label_hardware.nii.gz` | 2,362,429 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/0068_label_hardware_reassigned.nii.gz` | 2,365,774 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/0068_label_proposed.nii.gz` | 2,362,429 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/0068_label_v6.nii.gz` | 2,362,981 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu2500/0068_hardware_only.nii.gz` | 1,324,342 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu2500/0068_label_hardware.nii.gz` | 2,362,429 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu2500/0068_label_hardware_reassigned.nii.gz` | 2,365,404 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu2500b/0068_hardware_only.nii.gz` | 1,324,342 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu2500b/0068_label_hardware.nii.gz` | 2,362,429 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu2500b/0068_label_hardware_reassigned.nii.gz` | 2,365,404 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu3000/0068_hardware_only.nii.gz` | 1,323,543 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu3000/0068_label_hardware.nii.gz` | 2,362,429 | `code/case_fixes/thoracic_fix_0068` |
| `ctsp:thoracic_fix/0068/hu3000/0068_label_hardware_reassigned.nii.gz` | 2,364,851 | `code/case_fixes/thoracic_fix_0068` |
| `Desktop/NeurIPS/lstv_review/lstv_review/ambiguous/token_4/ct_separate.nii.gz` | 232,997,741 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/ambiguous/token_4/label_separate.nii.gz` | 1,391,070 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/ambiguous/token_67/ct_separate.nii.gz` | 264,101,710 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/ambiguous/token_67/label_separate.nii.gz` | 1,753,903 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_149/ct.nii.gz` | 278,423,328 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_149/label.nii.gz` | 1,528,227 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_167/ct.nii.gz` | 283,369,883 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_167/label.nii.gz` | 1,899,324 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_175/ct_separate.nii.gz` | 195,718,988 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_175/label_separate.nii.gz` | 1,441,556 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_189/ct.nii.gz` | 232,534,394 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_189/label.nii.gz` | 2,119,963 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_215/ct_separate.nii.gz` | 282,367,737 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_215/label_separate.nii.gz` | 1,609,103 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_261/ct_separate.nii.gz` | 269,159,239 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_261/label_separate.nii.gz` | 1,566,755 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_267/ct_separate.nii.gz` | 324,340,684 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_267/label_separate.nii.gz` | 1,672,569 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_344/ct.nii.gz` | 236,263,685 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_344/label.nii.gz` | 1,397,013 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_401/ct_separate.nii.gz` | 280,503,051 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_401/label_separate.nii.gz` | 1,636,455 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_587/ct_separate.nii.gz` | 263,571,344 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_587/label_separate.nii.gz` | 1,559,289 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_666/ct_separate.nii.gz` | 178,017,793 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_666/label_separate.nii.gz` | 1,285,496 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_672/ct_separate.nii.gz` | 213,677,791 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_672/label_separate.nii.gz` | 1,622,664 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_699/ct.nii.gz` | 268,649,094 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_699/label.nii.gz` | 2,090,945 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_737/ct.nii.gz` | 253,690,947 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/lumb/token_737/label.nii.gz` | 1,437,598 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/reference_normal/token_10/ct.nii.gz` | 290,165,931 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/reference_normal/token_10/label.nii.gz` | 2,055,132 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_104/ct_separate.nii.gz` | 214,347,130 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_104/label_separate.nii.gz` | 1,635,109 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_107/ct.nii.gz` | 201,452,348 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_107/label.nii.gz` | 1,723,172 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_110/ct_separate.nii.gz` | 271,891,158 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_110/label_separate.nii.gz` | 1,832,529 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_537/ct_separate.nii.gz` | 244,559,174 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_537/label_separate.nii.gz` | 1,760,496 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_554/ct_separate.nii.gz` | 229,501,659 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_554/label_separate.nii.gz` | 1,635,944 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_555/ct_separate.nii.gz` | 227,758,561 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_555/label_separate.nii.gz` | 1,610,912 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_615/ct.nii.gz` | 233,489,065 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_615/label.nii.gz` | 1,881,497 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_64/ct.nii.gz` | 237,625,972 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_64/label.nii.gz` | 1,357,814 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_721/ct_separate.nii.gz` | 187,247,058 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacr_count/token_721/label_separate.nii.gz` | 1,310,045 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_123/ct_separate.nii.gz` | 304,570,535 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_123/label_separate.nii.gz` | 1,990,814 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_125/ct.nii.gz` | 292,966,061 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_125/label.nii.gz` | 2,198,292 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_140/ct.nii.gz` | 237,839,770 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_140/label.nii.gz` | 1,592,205 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_15/ct_separate.nii.gz` | 218,802,552 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_15/label_separate.nii.gz` | 1,263,154 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_32/ct.nii.gz` | 186,266,118 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_32/label.nii.gz` | 1,647,858 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_6/ct_separate.nii.gz` | 215,537,678 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/sacralization/token_6/label_separate.nii.gz` | 1,236,323 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/semisacralization/token_120/ct_separate.nii.gz` | 231,434,383 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/semisacralization/token_120/label_separate.nii.gz` | 1,599,058 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/semisacralization/token_22/ct.nii.gz` | 207,512,573 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/semisacralization/token_22/label.nii.gz` | 1,679,628 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/techex/lumb/ct.nii.gz` | 283,369,883 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/techex/lumb/gt/0167_label.nii.gz` | 2,008,832 | `code/lstv_review_tool` |
| `Desktop/NeurIPS/lstv_review/lstv_review/techex/lumb/ts/segmentation.nii.gz` | 1,104,402 | `code/lstv_review_tool` |

### over 25 MB (1 files, 31,304,759 B)

| source | bytes | job |
|---|---|---|
| `Desktop/NeurIPS/lstv_review/lstv_review/techex/lumb/113758629_lstv_3d.html` | 31,304,759 | `code/lstv_review_tool` |

### zip (2 files, 1,827,014 B)

| source | bytes | job |
|---|---|---|
| `ctsp:CAMERA_READY_NEURIPS/Formatting_Instructions_For_NeurIPS_2026.zip` | 648,325 | `manuscripts/neurips_camera_ready` |
| `ctsp:paper/mpda/CTSpinoPelvic1K_MDPA_overleaf.zip` | 1,178,689 | `manuscripts/mpda` |

## 3. Edits made after copying (redactions, deletions, the banned word, headers)

### 3.1 Deleted after copy

| file | why |
|---|---|
| `manuscripts/talks/cns2026/figs_cited/bettis2026_article.html` | a saved third-party journal article page (Springer Nature) carrying author e-mail addresses; third-party literature is reference-by-path; the figure crops in `figs_cited/` that the deck uses are kept |
| `manuscripts/talks/cns2026/figs_cited/furuya2026_article.html` | same |
| `manuscripts/talks/cns2026/figs_cited/machin2018_article.html` | same |
| `docs/ctsp/HANDOFF_2026-09-21_PM.md` | the 2026-09-22 C-arm audit-track note (SchwingNet numbers); it belongs to project 01 (Greg-only) and must not sit in a student-safe folder; source `ctsp:docs/HANDOFF_2026-09-21_PM.md` (untracked) |
| `docs/ctsp/ajnr.html` | a saved third-party web page (untracked in the repository) |
| `docs/ctsp/ukb.html` | a saved third-party web page (untracked in the repository) |

### 3.2 Redacted in place (by kind, never by value)

| file | what was changed |
|---|---|
| `memory/rib-qc-gates-never-block-lstv.md` | two student usernames withheld |
| `docs/handoff/RECIPES.md` | one student username withheld |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | per-person username tally withheld |
| `docs/ctsp/EMAIL_CM_SPINE_REQUEST.md` | eleven researcher e-mail addresses in the author table and the three in the To / Cc lines withheld; author names and roles kept |
| `results/root_qc_tables/adjudication_list.csv` | student review handles replaced by annotator_NN (map withheld; Greg's own public handle kept) |
| `results/root_qc_tables/auto_finalize_manifest.csv` | student review handles replaced by annotator_NN (map withheld; Greg's own public handle kept) |
| `results/root_qc_tables/spine_restored_manifest.csv` | student review handles replaced by annotator_NN (map withheld; Greg's own public handle kept) |
| `docs/ctsp/castellvi_readers_2026-09-04.csv` | reader initials and names replaced by A/B/C |
| `results/root_qc_tables/Lumbosac.csv` | reader initials and names replaced by A/B/C |
| `docs/spinesurg_ct_nnunet/data_README.md` | old-scheme warning prepended |
| `docs/ctsp/castellvi_consensus.csv` | second pass: columns `read_1_NA`, `read_2_MI` renamed `read_1_A`, `read_2_B` (the same A / B as the two reader sheets above: first reader A, second reader B); `ctsp:scripts/apply_castellvi_consensus.py` in the repository reads the original column names, so this copy is data on record, not that script's input |
| `manuscripts/mpda/STUDENT_REVIEW_RESPONSE.md` | second pass: the five student reviewers' names (one a nickname) replaced by `student reviewer 1-5` (1 = 13 comments, 2 = 8, 3 = 5, 4 = 3, 5 = 2; the map is not written here), two pronouns neutralised, a note at the top points at the named original |
| `manuscripts/mpda/apply_compliance.py` | second pass: the eleven student co-author names on its lines 77-79 withheld (an empty list and a comment pointing at the repository line); the blinding loop is a no-op in this copy |

The student handles were mapped to `annotator_01` ... `annotator_11` consistently across the three tables; the map
is not written anywhere in this folder. Greg's own public Hugging Face handle (`memory/hf-identity.md`) is kept.
The two Castellvi readers are the article's co-authors; in the reader tables here they are Reader A and Reader B,
as the plan requires (`../_plan/PLAN.md` section 2 rule 7). Institutional service addresses (the HPC desk, the IRB
office, the library's interlibrary-loan desk) and Greg's institutional address on the manuscripts' own title pages
and cover letters were kept; every other e-mail address was struck.

**The manuscript author blocks keep the public author list: an exception, written here, not silent.** Twenty-three
copied files carry the fourteen names of the dataset article's author list (`manuscripts/mpda/title_page.tex` lines
42-55; the author blocks of `main.tex`, `main_OL.tex`, `main.tex.pre_schehr`, `arxiv/main.tex`, `overleaf/main.tex`;
`ARXIV_SUBMISSION.md` line 37; the `osc2026` entries of `ctspinopelvic1k.bib`, `overleaf/ctspinopelvic1k.bib`,
`_schehr_crossref/osc2026.bib` and `manuscripts/neurips_camera_ready/src/bib/references.bib`; the acknowledgement
strings of the twelve `manuscripts/talks/cns2026/make_cns_deck*.py`). They were kept because they are the article,
its preprint and its bibliography entries: the fourteen names are the published author list of arXiv 2609.22760 and
of the Zenodo deposit, and cutting them would alter the manuscript this folder exists to correct. The names rule was
applied where a name is an attribution of work rather than an authorship record (the notes, the review tables, the
review response and the compliance script above). Greg's answer to `OPEN_QUESTIONS.md` A30 can reverse this; the
files to edit are the twenty-three named. Under the same question: the copied HANDOFF files name the two Castellvi
readers and the NeurIPS co-authors (`docs/handoff/README.md` line 347, `working_notes/topic6_ctspinopelvic1k_and_toolkit.md`
line 327, as the handoff's student-readable text does), and Ashley Schehr is named in 34 files, including the folder
names `manuscripts/mpda/_schehr_crossref/` and the file `main.tex.pre_schehr`. None of that was changed.

### 3.3 The banned word

Rewritten as origin / Origin in every copied text file that carried it (13 files, 36 occurrences), including the
verbatim reviewer text in `manuscripts/neurips_camera_ready/REVIEWER_CRITIQUES.txt` and the PDF text dump
`NEURIPS_CURRENT_PDF.txt`, the MLHC text and rebuttal, and the two public deck generators. The PDFs and the `.pptx`
were not edited; a PDF of the 2026-09-08 NeurIPS draft and the MLHC paper still carry the word inside their binary text.
The repository's own tracked files still carry it (29 files; `TODO.md` step 5).

| file | occurrences rewritten |
|---|---|
| `docs/ctsp/DATASETS_ROADMAP.md` | 2 |
| `docs/ctsp/RELEASE_CHECKLIST.md` | 1 |
| `docs/ctsp_root/CLAUDE.md` | 1 |
| `manuscripts/mlhc_2026_rejected/_paper_text.txt` | 10 |
| `manuscripts/mlhc_2026_rejected/_rebuttal_f65r.txt` | 1 |
| `manuscripts/mpda/CITATION_CHECK.md` | 1 |
| `manuscripts/neurips_camera_ready/NEURIPS_CURRENT_PDF.txt` | 1 |
| `manuscripts/neurips_camera_ready/REVIEWER_CRITIQUES.txt` | 2 |
| `manuscripts/nextpaper_ar_2026-09-08/full-paper-template.tex` | 10 |
| `manuscripts/nextpaper_ar_2026-09-08/neurips_2026.tex` | 1 |
| `manuscripts/talks/cns2026/make_cns_deck_v11_public.py` | 1 |
| `manuscripts/talks/cns2026/make_cns_deck_v12_public.py` | 1 |
| `results/neurips_2026-05/bm/neurips_2026.tex` | 4 |

### 3.4 Headers on code files

Every `.py`, `.sh` and `.sbatch` under `code/` (50 files) carries two leading comment lines naming its repository
path and commit (or "gitignored", "untracked", "working tree, uncommitted edit", or "not a repository") and
this folder. `docs/spinesurg_ct_nnunet/data_README.md` carries a scheme warning as its first paragraph (its label
table is the old ten-class scheme).

### 3.5 Affiliation

`manuscripts/spinesurgct_arxiv_2026-03/SpineSurgCT_arxiv.tex` line 56 reads "Department of Neurosurgery"; it is the
March 2026 draft kept as history and was not edited. The affiliation is the Department of General Surgery, Wayne
State University School of Medicine / Detroit Medical Center. Every other "Neurosurgery" in the copied files is a
journal title or a survey option.

### 3.6 The second pass of 2026-10-08: laptop paths that remain in copied files, and what was added

The eight documents written for this folder carry no laptop path except this file. The copied files below still do;
each is a record of where something was on 2026-10-08, and the column on the right says what to change before the
file is run or trusted as an address. Line numbers are those after the headers and pointer lines of this pass.

| file | line(s) | what the path is | what to change |
|---|---|---|---|
| `code/case_fixes/_verify_0816/va/spine_qc.py`, `spine_qc_0068.py` | 5 | `sys.path` to the laptop's `CTSpinoPelvic1K-1\scripts` | the `scripts/` of a CTSpinoPelvic1K checkout at 7ddfe38 |
| `code/case_fixes/_verify_0816/va/render_0068_panels.py` | 29 | `SCHEME`, the laptop's `data/itksnap_v6_labels.txt` | `docs/release/itksnap_v6_labels.txt` in this folder |
| `code/case_fixes/_verify_0816/va/render_0231_panels.py` | 30 | same | same |
| `manuscripts/mpda/audit_ms.py` | 179 | a WSL path to `paper/mpda` inside a subprocess command | the `paper/mpda` of the checkout the script runs in |
| `manuscripts/mpda/audit_pdfs.py` | 11 | `ROOT`, the repository root on the laptop | the checkout root |
| `manuscripts/mpda/build_review_copy.py` | 32 | `WSL`, the WSL spelling of `paper/mpda` | same |
| `manuscripts/mpda/make_coauthor_docs.py` | 27 | `WSL_HERE`, same | same |
| `manuscripts/talks/cns2026/make_cns_deck.py` 384, `_v2.py` 377, `_v3.py` 370, `_v4.py` 498, `_v5.py` 353, `_v6.py` 354, `_v7.py` 347, `_v8.py` 377, `_v9.py` 378, `_v10.py` 379, `_v11_public.py` 314, `_v12_public.py` 376 | as listed | the `--out` default, a `.pptx` under the laptop's `OneDrive/Desktop` | pass `--out` |
| `manuscripts/talks/cns2026/sweep_per_level.py` | 4, 23 | the docstring record and `MIRROR`: the laptop mirror `C:/Users/grego/model_night/sweep_v3` of the grid's `~/model_night/sweep_v3` (project 01, Greg-only data) | set `MIRROR` to a copy of the sweep_v3 records; the data is not in this folder |
| `manuscripts/talks/cns2026/posterior/submit.sh` | 7-8 | `L` (the laptop's `paper/cns2026/posterior`) and `V` (`nnunet_wandb_variant.py` in the laptop's spinopelvic-seg checkout) | this folder's `manuscripts/talks/cns2026/posterior/` and `tools/nnunet_wandb_variant.py` of spinopelvic-seg at c105981 (`MANIFEST_CODE.md` section 4) |
| `manuscripts/talks/cns2026/figs_v2/sweep_per_level.json` | 876, 950, 1024 | `"arm"` fields recording which sweep file was read | a record, not an input |
| `memory/wsl-for-network.md` 17, `memory/windows-junction-worktree-trap.md` 16 and 26, `memory/cns-deck-v2-2026-09-25.md` 13, 15, 50, 52 | as listed | dated session notes (the WSL mount of the repository; the Ashley extension and worktree folders; where the CNS decks were written) | records; the decks are in `manuscripts/talks/cns2026/` |
| `docs/handoff/README.md` | 36-44 (the prefix table), 243 | the handoff's prefix definitions as laptop folders; the Beethoven vendor folder | `docs/handoff/PREFIXES.md` |
| `docs/handoff/RESULTS_CATALOG.md` | 14-16, 639 | the prefix paragraph; F.48's Temp scratchpad (the recomputation scripts, `TODO.md` step 2 b) | `PREFIXES.md`; the scripts are on Greg's laptop only |
| `docs/handoff/RECIPES.md` | 31, 79 | the WSL spelling of the private repository in the `git archive` recipe; "every laptop path starts at ..." | the checkout the recipe runs from |
| `docs/handoff/INFRASTRUCTURE.md` | 7, 116, 382 | `bth:` defined as the laptop's `ashley-bridge`; the Beethoven vendor folder; a portable Node install under the laptop's `tools/` | project 11; nothing here depends on it |
| `docs/ctsp_root/REVIEWERS_LINUX.md` | 47, 56 | `/mnt/c/Users/<YourWindowsName>/Downloads/` and `/mnt/c/Users/*/Downloads/`: generic placeholders in the reviewer guide, not Greg's machine | nothing |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | 18-26 (the tag table), 762 | the nine repository tags as laptop folders; Beethoven | `PREFIXES.md` (tag rows) |
| `docs/handoff/EXTRACTS.md` 65-66, `OPEN_QUESTIONS.md` 145, 163, `manuscripts/neurips_camera_ready/CAMERA_READY_CHANGES.md` 11, 158, 384 | as listed | `Desktop/NeurIPS/...` and "scratchpad" references without a drive letter (the audit reports, `INTEGRATE.md`, `OPENREVIEW_NOTE.md`, the facts files: lost or on Greg's laptop, E10 and F2) | nothing to set; `results/neurips_2026-05/` holds the per-case tables |
| `manuscripts/neurips_camera_ready/src/appendix/{background,construction_figure,dataset_comparison,spineps,v11_results}.tex`, `src/bib/references.bib` 406, `manuscripts/talks/cns2026/prep_cited_figs.py` 3 | comment lines | `scratchpad/neurips_promises/...` draft and scout files named in TeX and docstring comments | records; the drafts were integrated into the files that cite them |

The handoff's laptop-dependent instructions that a reader would act on are two: the `git archive | ssh tar` recipe
(`RECIPES.md` line 31; run it from any checkout of the private repository) and `TODO.md` step 2 b (Greg's laptop only).

**Added in this pass.** (1) `docs/handoff/PREFIXES.md`, written for this folder: every prefix and tag the copied HANDOFF
files use, resolved to a repository URL and commit from `MANIFEST_CODE.md`, to a path in this folder, or to a grid path
from `MANIFEST_GRID.md`. (2) A two-line pointer under the title of the nine copied HANDOFF files (`README.md`,
`GLOSSARY.md`, `RECIPES.md`, `RESULTS_CATALOG.md`, `DATASET_USAGE.md`, `LEAKAGE.md`, `OPEN_QUESTIONS.md`,
`INFRASTRUCTURE.md`, `working_notes/topic6_ctspinopelvic1k_and_toolkit.md`) and of `EXTRACTS.md`, so their line numbers
are two higher than in the repository's copies. (3) Headers on the 22 copied scripts that carry a laptop path: the four
`code/case_fixes/_verify_0816/va/` scripts got a third header line (`# laptop path on line N: set before running`); the
four `manuscripts/mpda/` scripts, the twelve `make_cns_deck*.py`, `sweep_per_level.py` and `posterior/submit.sh` got
the two-line source header they lacked plus that line (the `paper/cns2026/` files are excluded from every commit of
the public repository through `.git/info/exclude`, and their headers say so). (4) `manuscripts/mpda/apply_compliance.py`
got the same header with its withheld list noted (section 3.2). (5) A 1,014 B `grep.exe.stackdump` written into the
folder root at 21:25 on 2026-10-08 by a crashed `grep` (after the build; not a copy) was deleted.

## 4. Valuable material NOT copied, and why (the disposition's reference and exclude rows)

Rows whose `action` is `reference` live in a repository (`MANIFEST_CODE.md`), on the grid (`MANIFEST_GRID.md`) or
stay on the laptop by path; rows whose `action` is `exclude` fall under a copy rule. The reason column is the
disposition's own, with its inventory row ids.

| source | action | reason |
|---|---|---|
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1 (repo CTSpinoPelvic1K, master 7ddfe38, remotes origin=Gregory-Schwing-MD-PhD/CTSpinoPelvic1K osc=OpenSpineConsortium/CTSpinoPelvic1K)` | reference -> MANIFEST_CODE.md | [ctsp r1; inventory: ctsp_dataset/reference] public repository; everything tracked is reachable by URL+commit |
| `CTSpinoPelvic1K-1/paper/mpda/_others/, _schehr/, _upd/ (280 tracked files: coauthor Word comment dumps, apply_*.py, tighten*.py, crossref/*.bib, main.tex.before*)` | reference -> MANIFEST_LOCAL.md | [ctsp r3; inventory: ctsp_dataset/reference] coauthor-revision workings; superseded by main.tex; Word people.xml and comments carry reviewer names |
| `CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_coauthor_draft.docx/.pdf, CTSpinoPelvic1K_single_column.docx, CTSpinoPelvic1K_review.docx/.pdf, CTSpinoPelvic1K_coauthor_single_column.docx, CTSP_OTHERSTUDENTS.docx, references.docx, updated references.docx, notes.docx, CTSpinoPelvic1K_schehr revisions + sources notes.docx` | reference -> MANIFEST_LOCAL.md | [ctsp r5; inventory: ctsp_dataset/reference] circulation copies generated by make_coauthor_docs.py; superseded by the tex |
| `CTSpinoPelvic1K-1/paper/mpda/EMAIL_ASHLEY.md` | exclude -> MANIFEST_LOCAL.md | [ctsp r6; inventory: ctsp_dataset/exclude] e-mail to a coauthor; personal correspondence |
| `CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_MDPA_overleaf.zip, CTSpinoPelvic1K_MDPA_overleaf/, CTSpinoPelvic1K_arxiv.tar.gz, CTSpinoPelvic1K_arxiv_preview.pdf, FROM_ARXIV.pdf, DUPLICATE_THORACIC.pdf, _len.pdf, bibtest.*, typeset_preview.*, reprint_check.tex` | reference -> MANIFEST_LOCAL.md | [ctsp r7; inventory: ctsp_dataset/reference] bundles regenerated by make_overleaf.py / make_arxiv.sh |
| `CTSpinoPelvic1K-1/scripts/ (267 tracked; label_scheme.py, extract_*.py, qc_*.py, build_v3_totalseg.py, build_v4_ribs.py, build_v6.py, build_final_dataset.py, benchmark_{totalseg,spineps,moller}.py, render_*.py, select_anchor_cases.py, six_lumbar_readings.py, shift_hypothesis_test.py, fill_hpr_determination.py, adhoc/)` | reference -> MANIFEST_CODE.md | [ctsp r17; inventory: ctsp_dataset/reference] all in the repository at 7ddfe38 |
| `CTSpinoPelvic1K-1/slurm/ (129 tracked .sh), tests/ (25), zenodo/ (18: assemble_deposit.py, new_version.py, upload.py, KNOWN_ISSUES.md, README.md, hf_dataset_card.md, make_croissant.py, reconstruct_ct.py, fetch_from_tcia.py), hf/push_v9.py, review_service/ (9), reviewtool/ (4), configs/ (3), containers/ (2), docker/Dockerfile, docker/Dockerfile.totalsegmentator, data/README.md, data/itksnap_v4_labels.txt` | reference -> MANIFEST_CODE.md | [ctsp r18; inventory: ctsp_dataset/reference] in the repository |
| `CTSpinoPelvic1K-1/ribseg_v2.zip (608 MB)` | reference -> MANIFEST_LOCAL.md | [ctsp r62; inventory: ctsp_dataset/reference] RibSeg v2 download; data |
| `CTSpinoPelvic1K-1/ckpt_mirror/Dataset803_SpineSurgCTFullMerged/ (nnUNetTrainerWandB_500ep_LSTVOversample, folds 0-3 with ~1.9 MB training logs)` | reference -> MANIFEST_LOCAL.md | [ctsp r63; inventory: ctsp_dataset/reference] nnU-Net checkpoints mirrored from the grid; weights |
| `CTSpinoPelvic1K-1/data/ (hf_export_v5/labels 802, zenodo_deposit/labels 802 + manifest.json + splits_5fold.json + dataset_labels.json + SHA256SUMS.txt + KNOWN_ISSUES.md, ala_test 173, tp_check 12, tp_near, v5_pre_break_backup 303, v5_pre_gap_backup, v5_pre_speckle_backup)` | reference -> MANIFEST_LOCAL.md | [ctsp r64; inventory: ctsp_dataset/reference] label volumes; data |
| `CTSpinoPelvic1K-1/dist/ (overleaf/, overleaf.zip, CTSpinoPelvic1K_overleaf.zip, submission/ with Main_Document tex+pdf, Supporting_Information, Title_Page, Figure_1-3.pdf, Abstract.txt, Cover_Letter.md)` | reference -> MANIFEST_LOCAL.md | [ctsp r65; inventory: ctsp_dataset/reference] build outputs of make_submission.py; regenerable |
| `CTSpinoPelvic1K-1/scratchpad/*.csv (hip_agreement, sagittal_tilt, pca_bias, break_diagnosis, census3, dust_probe, tp_smoke*, ala_smoke*), scratchpad/*.py (fix_*.py, tighten*.py, census_into_paper.py, local_morphology.py, prior_art.py, pca_bias.py, sagittal_tilt.py, render_*.py, ...), scratchpad/grid_sums.txt, local_sums.txt, dist_backup.json` | reference -> MANIFEST_CODE.md | [ctsp r70; inventory: ctsp_dataset/reference] one-off paper-edit and probe scripts; their effects are in main.tex and the morphometrics tables |
| `CTSpinoPelvic1K-1/scratchpad/brk/, gapt/, one0631/, probecases/, case22/, tp_test/ (label nii.gz + small csv)` | exclude -> MANIFEST_LOCAL.md | [ctsp r71; inventory: ctsp_dataset/exclude] label volumes for single-case probes |
| `CTSpinoPelvic1K-1/scratchpad/drr/ (16 png), scratchpad/*.png (fig previews, anchors, hough, detached examples, cervical_pred_*)` | reference -> MANIFEST_LOCAL.md | [ctsp r72; inventory: ctsp_dataset/reference] figure previews |
| `CTSpinoPelvic1K-1/scratchpad_*.txt, scratchpad_*.log, scratchpad_resweep_stats.json, scratchpad_gapcheck/ (root)` | exclude -> MANIFEST_LOCAL.md | [ctsp r73; inventory: ctsp_dataset/exclude] session logs of the review sweeps; scratchpad_sweep.log 650 KB |
| `CTSpinoPelvic1K-1/rib_fix_work/ (8 case dirs: ct+label nii + descriptor), spine_fix_work/ (27 empty case dirs + TODO.csv), hardware_review/verify/` | exclude -> MANIFEST_LOCAL.md | [ctsp r77; inventory: ctsp_dataset/exclude] per-case fix volumes |
| `CTSpinoPelvic1K-1/v3_qc/, v4_qc/, v4_qc_gaps/, v4_qc_union/, v4_rib_examples/, rib_qc_renders/, qc_hardware_render/, adjudication_renders/, wedge_renders/wedge_check.png` | reference -> MANIFEST_LOCAL.md | [ctsp r78; inventory: ctsp_dataset/reference] QC render PNGs |
| `CTSpinoPelvic1K-1/spine_tampering.csv` | exclude -> MANIFEST_LOCAL.md | [ctsp r81; inventory: ctsp_dataset/exclude] per-case voxel-change table keyed by reviewer usernames |
| `CTSpinoPelvic1K-1/student_vertebra_work.csv, spine_worklist.json, spine_needs_human.csv, spine_extend_worklist.json, class_mixing_worklist.json, auto_accept_spine_manifest.csv, verify_thoracic_edit.py, chk_case_lstv.py (tracked at repo root)` | reference -> MANIFEST_LOCAL.md | [ctsp r84; inventory: ctsp_dataset/reference] review worklists; in the repository |
| `CTSpinoPelvic1K-1/_desc.py, _roster5.py, _trim1.py, chk0816.py, chk_coverage.py, chk_finals.py, chk_native.py, flag_0068.py, map_tokens.py, mk_worklist_add.py` | reference -> MANIFEST_CODE.md | [ctsp r85; inventory: ctsp_dataset/reference] ad-hoc scripts; most duplicated under scripts/adhoc/ in the repo |
| `CTSpinoPelvic1K-1/MDPA.pdf (anonymized, dated 2026-09-16), MDPA_OL.zip (overleaf export 2026-09-06), GPTZero AI Scan - CTSpinoPelvic1K_single_column.docx.pdf` | exclude -> MANIFEST_LOCAL.md | [ctsp r91; inventory: ctsp_dataset/exclude] earlier builds and an AI-scan report |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K (older clone, master 4fb4a62 2026-04-28, origin only)` | reference -> MANIFEST_CODE.md | [ctsp r106; inventory: ctsp_dataset/reference] 4fb4a62 is an ancestor of 7ddfe38 (git merge-base); nothing tracked here is missing from the main repository |
| `CTSpinoPelvic1K/placed_manifest_orientation_fixed.json (1.2 MB), patch_size_comparison.png, patch_size_comparison - Copy.png, qc_audit_210_pelvic_native.png, qc_audit_210_spine_only.png, qc_audit_5_fused.png, data/lstv_*png (35 renders), data/qc_figures_orifix/` | reference -> MANIFEST_LOCAL.md | [ctsp r108; inventory: ctsp_dataset/reference] April 2026 placement manifest and QC renders; superseded by the v10/v11 manifests |
| `CTSpinoPelvic1K/qc.tar.gz (344 MB)` | exclude -> MANIFEST_LOCAL.md | [ctsp r109; inventory: ctsp_dataset/exclude] April QC bundle |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_MDPA_overleaf (main.tex 2026-09-10, ctspinopelvic1k.bib, figure_captions.tex, medphy.bst, figures/ 6 pdf)` | exclude -> MANIFEST_LOCAL.md | [ctsp r116; inventory: ctsp_dataset/exclude] overleaf export older than the repo's own copy (501 diff lines against paper/mpda/CTSpinoPelvic1K_MDPA_overleaf/main.tex; 1,492 against main.tex of 2026-09-25) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_overleaf (main.tex 2026-09-04, census_table.tex, supplementary.tex, title_page.tex, README.md, figures/)` | exclude -> MANIFEST_LOCAL.md | [ctsp r117; inventory: ctsp_dataset/exclude] first overleaf export (revtex preprint); 2,398 diff lines against the current main.tex |
| `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/SpineSurg-CT (git, origin Gregory-Schwing-MD-PhD/SpineSurg-CT, 0051074 2026-04-09, 136 commits: scripts/ COLONOG matching and mask fusion, src/ train/eval, metadata_colonog.csv/.xlsx, metadata_hnscc.xlsx, data_split.txt, path.csv, tokens/qc_figures, cit.bib, LSTV final citations.docx)` | reference -> MANIFEST_CODE.md | [ctsp r119; inventory: ctsp_dataset/reference] the project's first repository (March-April 2026), replaced by CTSpinoPelvic1K |
| `SpineSurg-CT/Status_of_dataset.xlsx, TODO.docx, pipeline_alignment_fix.py, token_1-5_qc.png, lastclaude.docx, sample.bib, citation.ris, files.zip, Cover Letter.pdf, Spine Segmentation Dataset Research.pdf` | reference -> MANIFEST_LOCAL.md | [ctsp r123; inventory: ctsp_dataset/reference] April 2026 status sheet and odds and ends |
| `C:/Users/grego/OneDrive/Desktop/NeurIPS/main.tex (2026-05-06), bib.tex, NeurIPS_Paper_Draft.pdf, Paper.pdf, 3474_Not_All_Spines_Are_Create.pdf, Formatting_Instructions_For_NeurIPS_2026*` | reference -> MANIFEST_LOCAL.md | [ctsp r127; inventory: ctsp_dataset/reference] May 2026 NeurIPS draft; superseded by CAMERA_READY_NEURIPS |
| `C:/Users/grego/OneDrive/Desktop/rib_review (4 png, morph_test.csv, morph_test2.csv, 2026-08-17)` | reference -> MANIFEST_LOCAL.md | [ctsp r139; inventory: ctsp_dataset/reference] rib review renders and a 3 KB morphometry test |
| `C:/Users/grego/OneDrive/Desktop/fov_check (17 *_fov.png, 2026-08-19)` | reference -> MANIFEST_LOCAL.md | [ctsp r140; inventory: ctsp_dataset/reference] FOV check renders made by slurm/fov_check.sh |
| `C:/Users/grego/OneDrive/Desktop/new_repo (README.md, docs_pipeline.md, docs_ablations.md, docs_troubleshooting.md, spinesurg-ct.def, build_container.sh, download_dataset.py, spinesurg-ct-nnunet.tar.gz 65 KB, 2026-04-18)` | exclude -> MANIFEST_LOCAL.md | [ctsp r144; inventory: ctsp_dataset/exclude] April scaffold of spinesurg-ct-nnunet; the live private repo supersedes it |
| `C:/Users/grego/OneDrive/Desktop/3474_Not_All_Spines_Are_Create.pdf` | reference -> MANIFEST_LOCAL.md | [desk r12; inventory: anomaly_scan_census/reference] NeurIPS 2026 submission 3474 as submitted (19 pages, anonymous; 'Not All Spines Are Created Equal: How TotalSegmentator Fails on LSTV'); byte-identical untracked copy in CTSpinoPelvic1K-1 root; Desktop/NeurIPS holds a different 932 KB build; source is CTSpinoPelvic1K-1/CAMERA_READY_NEURIPS/src \|\| decision: byte-identical twin of the NeurIPS submission PDF copied under ctsp r92 |
| `C:/Users/grego/OneDrive/Desktop/74_1.3.6.1.4.1.9328.50.4.80461_propagation.png` | reference -> MANIFEST_LOCAL.md | [desk r13; inventory: ctsp_dataset/reference] QC render of hip-label propagation for token 74 (accept=0, overlap 73.0% before, 24.8% after, reg_failed_drop=48.2pp), 2026-06-12; near-identical variants in Desktop/new/, Desktop/new/new/ and Desktop/CASE_HIEBER/qc/ |
| `C:/Users/grego/OneDrive/Desktop/arxiv_prev.pdf` | reference -> MANIFEST_LOCAL.md | [desk r16; inventory: ctsp_dataset/reference] arXiv final draft 2026-09-19 (14 pages, named authors, 'Department of Surgery, DMC and WSU'); byte-identical to CTSpinoPelvic1K-1/arxiv_final_draft_9_19_2026.pdf (untracked) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_arxiv.tar.gz` | reference -> MANIFEST_LOCAL.md | [desk r23; inventory: ctsp_dataset/reference] arXiv source bundle 2026-09-07 (main.tex, figure_captions.tex, six figure PDFs); superseded by CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_arxiv.tar.gz (larger, later, untracked) and by the tracked paper/mpda sources |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_arxiv_preview.pdf` | reference -> MANIFEST_LOCAL.md | [desk r24; inventory: ctsp_dataset/reference] arXiv preview 2026-09-07 (11 pages); superseded by tracked CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_arxiv_preview.pdf (later, larger) and by arxiv_prev.pdf of 2026-09-19 |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_coauthor_draft.docx` | reference -> MANIFEST_LOCAL.md | [desk r25; inventory: ctsp_dataset/reference] byte-identical to tracked CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_coauthor_draft.docx |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_coauthor_draft.pdf` | reference -> MANIFEST_LOCAL.md | [desk r26; inventory: ctsp_dataset/reference] byte-identical to tracked CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_coauthor_draft.pdf (2026-09-07, 24 pages, named authors) |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_MDPA_overleaf.zip` | reference -> MANIFEST_LOCAL.md | [desk r27; inventory: ctsp_dataset/reference] Overleaf bundle 2026-09-10 (main.tex, bib, medphy.bst, six figures); superseded by tracked CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_MDPA_overleaf.zip (later, larger) and by the Desktop folder of the same name |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_overleaf.zip` | reference -> MANIFEST_LOCAL.md | [desk r28; inventory: ctsp_dataset/reference] Overleaf bundle 2026-09-06 (main, supplementary, title page, census table, six figures); superseded by CTSpinoPelvic1K-1/dist/CTSpinoPelvic1K_overleaf.zip (later, untracked) and the Desktop folder of the same name |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_submission.zip` | reference -> MANIFEST_LOCAL.md | [desk r29; inventory: ctsp_dataset/reference] submission package 2026-09-07 (Cover_Letter.md, LaTeX source zip, Main Document, Supporting Information, Title Page, Figures 1-7); the unzipped Desktop/CTSpinoPelvic1K_submission folder is the copy to take; superseded by the 2026-09-21 MDPA_FINAL submission |
| `C:/Users/grego/OneDrive/Desktop/Lumbosac.csv` | reference -> MANIFEST_LOCAL.md | [desk r33; inventory: anomaly_scan_census/reference] single-reviewer LSTV read sheet (2026-06-08, 41 lines): Castellvi type per CTSP 'Token' with comments, grouped ambiguous / lumbarised / sacral count 4 / sacralised / semi-sacralised / reference; superseded by CTSpinoPelvic1K-1/Lumbosac.csv (2026-09-04, 47 lines, adds 2nd and 3rd reviewer columns; untracked) \|\| decision: the 2026-06-08 single-reviewer sheet; superseded by CTSpinoPelvic1K-1/Lumbosac.csv (three reviewer columns, 2026-09-04), copied under ctsp r80 with reader initials renamed |
| `C:/Users/grego/OneDrive/Desktop/MDPA.pdf` | reference -> MANIFEST_LOCAL.md | [desk r34; inventory: ctsp_dataset/reference] double-anonymized build dated 12 September 2026 (11 pages); superseded by CTSpinoPelvic1K-1/MDPA.pdf (2026-09-16, untracked, different bytes) and by MDPA_FINAL.pdf (2026-09-21) |
| `C:/Users/grego/OneDrive/Desktop/MLHC_2026_Research_Track_Paper.pdf` | reference -> MANIFEST_LOCAL.md | [desk r35; inventory: ctsp_dataset/reference] MLHC 2026 research-track submission (20 pages, anonymous; 'CTSpinoPelvic1K: A Unified CT Benchmark for Lumbosacral Transitional Vertebra Segmentation', 2026-06-08); byte-identical untracked copy in CTSpinoPelvic1K-1 root, same-size copy in Desktop/SpineSurg-CT; sources in CTSpinoPelvic1K-1/mlhc |
| `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K_coauthor_signoff.xlsx` | exclude -> MANIFEST_LOCAL.md | [desk r90; inventory: ctsp_dataset/exclude] personal or administrative material, classified from the file name and not opened; stays out under the task's rule |
| `C:/Users/grego/OneDrive/Desktop/NextPaper/flip18_review (CT and label nii.gz); flip18_review.zip` | exclude -> MANIFEST_LOCAL.md | [inv3 r20; inventory: ctsp_dataset/exclude] 18 CT+label pairs pulled for an L6 review (zip 4.26 GB) |
| `C:/Users/grego/OneDrive/Desktop/NextPaper/spinopelvic-seg` | reference -> MANIFEST_CODE.md | [inv3 r35; inventory: ctsp_dataset/reference] public repo origin anonymous-neurips-ED/spinopelvic-seg + osc OpenSpineConsortium/spinopelvic-seg, main c105981 2026-06-23, clean; the Dataset803 merged-label nnU-Net pipeline cited by the camera-ready |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/CITATION.cff` | reference -> MANIFEST_LOCAL.md | [ssn r4; inventory: ctsp_dataset/reference] citation metadata of the April nnU-Net pipeline; ORCID placeholder; its `version` field reads `0.1.0` as written in the file |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/pyproject.toml` | reference -> MANIFEST_CODE.md | [ssn r7; inventory: ctsp_dataset/reference] host-side package metadata (packages = tools) |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/requirements.txt` | reference -> MANIFEST_LOCAL.md | [ssn r8; inventory: ctsp_dataset/reference] host-side deps only; nnU-Net lives in the container |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/{convert_hf_to_nnunet,aggregate_folds,compare_ablations,eval_full,eval_ensemble_test,eval_ensemble_test_sep_hips,eval_subgroups,eval_oneshot,enumerate_decoder,lstv_biased_dataloader,nnunet_wandb_variant,preflight_lstv,reshape_patch,visualize_patch_sizes,sync_splits_to_nnunet,fast_scan,l6_report,dx,d815_flags_and_integrity,ds813_to_v10,make_halved_dataset,make_quaternary_dataset,check_countfree_disc,split_column,test_dataset_803_pipeline,xrsp1k_to_nnunet,eval_xrsp1k_seg}.py` | reference -> MANIFEST_CODE.md | [ssn r140; inventory: ctsp_dataset/reference] the April-June nnU-Net era: HF -> nnU-Net conversion, LSTV-aware dataloader, ablation aggregation, Dataset803/810/813/815 evaluation, the counting decoder; two XRSpinoPelvic1K converters |
| `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/slurm/{spine_prep,spine_train_fold,spine_train_array,spine_eval_*(3),spine_predict_803_best*,spine_pred_803_best_array,spine_ensemble_803_best,spine_ablation,spine_convert,launch_*(10),relaunch_fullribs,switch_to_fullribs,resubmit_round2,push99_chain,queue_surgio_chain,queue_all_2026-09-22,spineps_cases,spineps_ctsp,spineps_ts_v3,spineps_ts_verse,competitor_ensemble,xr_bench,mv_bench,sync_to_nnunet,convert_hf_to_nnet,decoder_oracle,product_select}.sh + README_fused_only_ablation.md` | reference -> MANIFEST_CODE.md | [ssn r153; inventory: ctsp_dataset/reference] nnU-Net preprocess/train/eval/ablate arrays for Dataset802-815 and the CT competitor runs |

Grid rows (`reference -> MANIFEST_GRID.md`) are in `MANIFEST_GRID.md`; the HANDOFF section rows
(`copy -> docs/handoff/`) became the whole-file copies in `docs/handoff/` and the extracts in
`docs/handoff/EXTRACTS.md`, `STATUS.md` and `TODO.md`.

## 5. Decisions taken by this build beyond the disposition

- `ctsp:zenodo/README.md`, `zenodo/KNOWN_ISSUES.md`, `zenodo/hf_dataset_card.md` and the five deposit sidecars
  (`data/zenodo_deposit/{manifest.json,splits_5fold.json,dataset_labels.json,SHA256SUMS.txt,KNOWN_ISSUES.md}`) were
  copied into `docs/release/` although their disposition rows say reference, because the plan's project section
  lists them among the material this folder absorbs and `TODO.md` step 4 edits them. **They are the v10 deposit**
  (`dataset_labels.json` names the scheme "v10" and maps `S1` to 29; `KNOWN_ISSUES.md` is headed v10); the v11
  staging is on the grid (`MANIFEST_GRID.md` section 1, `s1v11`).
- Two different `KNOWN_ISSUES.md` exist in the repository: the tracked `ctsp:zenodo/KNOWN_ISSUES.md` (8,954 B) and
  the deposit folder's `ctsp:data/zenodo_deposit/KNOWN_ISSUES.md` (11,199 B); they differ from line 24. Both are
  kept: `docs/release/KNOWN_ISSUES.md` is the deposit folder's, `docs/release/zenodo_KNOWN_ISSUES.md` the tracked
  one. The grid's v11 tree carries a third size (8,894 B, `MANIFEST_GRID.md` section 1); which text is on Zenodo v11
  is not recorded.
- `ctsp:docs/castellvi_readers_2026-09-04.csv` and `ctsp:Lumbosac.csv` are byte-identical sources (same header and
  rows); both copies were redacted the same way and kept at their two destinations because two disposition rows
  name them.
- `results/neurips_2026-05/bm/` and `audit/` hold the same `benchmark_results.json` (2,048,357 B) and
  `per_case_partial.jsonl` (1,233,526 B) twice because the source folders do; both copied as found.
- The eight student-readable HANDOFF files were copied whole (plan rule 3); `MANUSCRIPTS.md`,
  `RESEARCH_DIRECTIONS.md`, `LITERATURE_STATE.md` and `CONTEXT_EXPORT.md` were not, and appear only as the
  redacted extracts in `docs/handoff/EXTRACTS.md`. `HANDOFF/GREG_ONLY/` was never read for this folder.
- `Desktop/NeurIPS/lstv_review/lstv_review/Mahato_2020_LSTV_classification.pdf` (a copyrighted article, 1,911,676 B)
  was left out of `code/lstv_review_tool/` by the third-party-literature rule; `ctsp:PANJABI_1991_FULL*.pdf` likewise
  (`memory/panjabi-1991-page-892.md`).
- `ssn:benchmark/data/fluorocap_v0.1/` (the dormant FluoroCap freeze) was left out of `code/benchmark/`; it belongs to
  project 99.
- `ctsp:paper/mpda/_schehr/crossref/*.bib` (the 37 verified entries) were copied to `manuscripts/mpda/_schehr_crossref/`;
  the rest of the three coauthor-revision folders (280 tracked files of Word comment dumps with reviewer names)
  stay in the repository by reference.
- The disposition's memory rows name 32 notes; the per-project cut list of the memory inventory names 36
  (adding `dataset813-image-links-are-container-paths`, `panjabi-1991-page-892`, `publication-roadmap`,
  `ts-sacrum-excludes-s1`); the 22 standing-rule notes tagged for every folder were added; 55 distinct notes in all,
  every one from `HANDOFF/context/` (the redacted copies), none from the live memory folder.
- The NeurIPS recomputation scripts named in `STATUS.md` F.48 were looked for only through the handoff's record;
  the Temp scratchpad that holds them was not read by this build, so they are not here (`TODO.md` step 2 b).


## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Salvaged: the May 2026 NeurIPS submission source and the co-author review files

Section 4 held the May 2026 NeurIPS tex by path as 'superseded by CAMERA_READY_NEURIPS' and section 2 held the Word files of `paper/mpda/` as co-author dumps that stay out. The critic separated two things from those groups: (1) `NeurIPS/main.tex` of 2026-05-06 is the source of the paper that was scored and accepted as NeurIPS 2026 Evaluations and Datasets 3474 (the PDF of record `manuscripts/3474_Not_All_Spines_Are_Create.pdf` is here, its source was not; the camera-ready tex is a later working copy with 134 `[pending]` slots and `results/neurips_2026-05/bm/neurips_2026.tex` is an earlier draft under another title); whether the CTSpinoPelvic1K git history holds this May tex is not recorded. (2) Two Word files hold the substantive co-author revision notes with the sources behind each change, which `TODO.md` step 3 (the MPDA corrections and rebuild) needs; the folders that hold reviewer identities (`_others/`, `_schehr/`, `_upd/`, `people.xml`) stay out as before.

| destination | source (laptop, 2026-10-08) | bytes | sha1 | note |
|---|---|---:|---|---|
| `manuscripts/neurips_as_submitted_2026-05/main.tex` | `C:/Users/grego/OneDrive/Desktop/NeurIPS/main.tex` | 40,960 | f885151aea203032 | byte-identical; the submission is anonymised (`Anonymous Author(s)`, lines 31-34 of main.tex) |
| `manuscripts/neurips_as_submitted_2026-05/bib.tex` | `C:/Users/grego/OneDrive/Desktop/NeurIPS/bib.tex` | 411 | a638b116b3f134cf | byte-identical; the submission is anonymised (`Anonymous Author(s)`, lines 31-34 of main.tex) |
| `manuscripts/neurips_as_submitted_2026-05/NeurIPS_Paper_Draft.pdf` | `C:/Users/grego/OneDrive/Desktop/NeurIPS/NeurIPS_Paper_Draft.pdf` | 266,927 | 088c5b9507642e39 | byte-identical; the submission is anonymised (`Anonymous Author(s)`, lines 31-34 of main.tex) |
| `manuscripts/mpda/coauthor_review/CTSpinoPelvic1K_coauthor_revisions_and_sources_notes.docx` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_schehr revisions + sources notes.docx` | 2,312,388 | f9b4571cd814e076 | docx re-written on copy: `docProps/core.xml` creator and lastModifiedBy emptied; one university AccessID e-mail address in the body replaced by `[corresponding author's university address]`; the tracked-change author (a published co-author, a person) kept |
| `manuscripts/mpda/coauthor_review/CTSpinoPelvic1K_review.docx` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_review.docx` | 860,207 | 5a587627717ae704 | docx re-written on copy: `docProps/core.xml` creator, which carried the full 14-author list including ten students, emptied; body unchanged (no e-mail address found) |
| `manuscripts/mpda/coauthor_review/CTSpinoPelvic1K_review.pdf` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/paper/mpda/CTSpinoPelvic1K_review.pdf` | 1,249,194 | 5ab3339abb412e8a | byte-identical; the reviewed draft the notes were made on; not text-scanned (PDF) |

The `.tex` and `.bib` copies carry no e-mail address and no laptop path (scan on copy). The revisions file was renamed on copy (the source name carried the co-author's surname; the co-author is a published author and a person, kept in the text, struck from the file name only for consistency with the other copies).

### Shared copies, recorded as such

| file | twins | owner | why both exist |
|---|---|---|---|
| `manuscripts/neurips_camera_ready/src/figs/lstv_lumbarization_215_spine_only.png` (631,555 B, sha1 a739a8774ff63907) | `manuscripts/nextpaper_ar_2026-09-08/figs/` (same bytes) and `../06_transitional_ct_census/results/neurips_2026-05/` (same bytes) | this folder (the camera-ready figure tree) | each manuscript source tree must build on its own; 06 keeps the figure beside the May 2026 result files it came from and records it as shared |

The visual-abstract files under `code/case_fixes/_verify_0816/va/` that are still byte-identical to files in `../12_website_pacs_demo/figures/visual_abstract/` (owner 12; kept here because they are part of the 0816 case-fix verification set):

| here (under `va/`) | bytes | sha1 | in 12 |
|---|---:|---|---|
| `visual_abstract.pdf` | 734,374 | cd0c20bc2342a963 | `OSC_visual_abstract.pdf` |
| `visual_abstract.png` | 1,281,992 | c80184fddcd4ac60 | `OSC_visual_abstract.png` |
| `panels/0068_v5.png` | 418,402 | 32c3ab44b6cf0cd0 | `panels/0068_v5.png` |
| `panels/0068_v6.png` | 439,703 | d08a73277a5eab00 | `panels/0068_v6.png` |
| `panels/0231_v4.png` | 614,169 | 1ca428f3b30ee193 | `panels/0231_v4.png` |
| `panels/0231_v6.png` | 624,275 | 9207da963a9a0a8a | `panels/0231_v6.png` |
| `panels/markers.json` | 839 | eeaaf793da626387 | `panels/markers.json` |
| `panels/markers_0068.json` | 835 | 2a3b8edf65ce0d9a | `panels/markers_0068.json` |
| `pptx_imgs/Picture_6.png` | 697,201 | 39d59c7d2f90bb25 | `ORIGINAL_center_Picture_6.png` |

### Removed: Greg-only HANDOFF material (working note topic 6)

PLAN.md section 2 rule 3 confines the Greg-only HANDOFF files and working notes to folders 01, 02, 07, 08 and 09; student-safe folders get extracts in `STATUS.md` and `TODO.md`, not the notes. The critic found the files below here whole. Removed in the final pass; the extracts stay; the whole files live in the owning Greg-only folder named in the last column and in spinesurg-ct-nnunet at 097933a (`HANDOFF/`).

| removed | bytes | sha1 | where it lives |
|---|---:|---|---|
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | 96,690 | 7f55e69a36dc83e9 | `../01_carm_level_detection/docs/handoff/working_notes/` |

### Student names withheld in the superseded deck generators

The acknowledgement string of the early CNS deck generators listed the ten student annotators by name; it now reads `[ten student annotator names withheld]` (the current generators v5 to v12 never carried the list). The author lists inside the manuscript sources (`manuscripts/mpda/title_page.tex`, `main.tex`, `ARXIV_SUBMISSION.md`, the `.bib` files) are the record of authorship of a submitted or public manuscript and are kept unchanged; that keep is Greg's to confirm (PLAN.md section 5).

- `manuscripts/talks/cns2026/make_cns_deck.py`
- `manuscripts/talks/cns2026/make_cns_deck_v2.py`
- `manuscripts/talks/cns2026/make_cns_deck_v3.py`
- `manuscripts/talks/cns2026/make_cns_deck_v4.py`

### E-mail address withheld

`memory/wsu-library-access-cutoff.md`: the library contact address replaced by `[library e-mail withheld]` (the library's public phone numbers kept), the same as 08's copy already read.

### Laptop paths rewritten to markers (self-containment)

The critic's tree-wide scan still found laptop spellings in copied files of this folder outside `MANIFEST_LOCAL.md`. They are now the markers the other folders use: `<laptop:Desktop>` for the Desktop root that held every repository checkout (`<laptop:Desktop>/spinesurg-ct-nnunet` = spinesurg-ct-nnunet at 097933a, `<laptop:Desktop>/CTSpinoPelvic1K-1` = CTSpinoPelvic1K at 7ddfe38, `<laptop:Desktop>/OpenSpineToolkit` = OpenSpineToolkit at cb43197, `<laptop:Desktop>/XRaySpinoPelvic1K` = XRSpinoPelvic1K at 4f22935), `<laptop:Temp scratchpad>` for the swept session scratchpad (nothing there is a dependency), `<laptop memory folder>` for the live memory notes (copied redacted into `memory/`), `<laptop vendor folder, never read>` and `<laptop home>`. The marker is a spelling of where the file came from, not a path to resolve; the repository and commit are the dependency. Scripts among these copies (`.py`, `.sh`) hard-coded laptop roots and did not run anywhere else before this change either; they are records of how a document was built.

| file | laptop spellings rewritten | left |
|---|---:|---:|
| `code/case_fixes/_verify_0816/va/render_0068_panels.py` | 2 | 0 |
| `code/case_fixes/_verify_0816/va/render_0231_panels.py` | 2 | 0 |
| `code/case_fixes/_verify_0816/va/spine_qc.py` | 2 | 0 |
| `code/case_fixes/_verify_0816/va/spine_qc_0068.py` | 2 | 0 |
| `code/lstv_review_tool/LSTVReviewer.py` | 1 | 0 |
| `code/lstv_review_tool/module/LSTVReviewer.py` | 1 | 0 |
| `docs/ctsp_root/REVIEWERS_LINUX.md` | 2 | 0 |
| `docs/handoff/INFRASTRUCTURE.md` | 4 | 0 |
| `docs/handoff/README.md` | 14 | 0 |
| `docs/handoff/RECIPES.md` | 4 | 0 |
| `docs/handoff/RESULTS_CATALOG.md` | 8 | 0 |
| `manuscripts/mpda/audit_ms.py` | 2 | 0 |
| `manuscripts/mpda/audit_pdfs.py` | 2 | 0 |
| `manuscripts/mpda/build_review_copy.py` | 2 | 0 |
| `manuscripts/mpda/make_coauthor_docs.py` | 2 | 0 |
| `manuscripts/talks/cns2026/figs_v2/sweep_per_level.json` | 3 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v10.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v11_public.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v12_public.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v2.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v3.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v4.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v5.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v6.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v7.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v8.py` | 1 | 0 |
| `manuscripts/talks/cns2026/make_cns_deck_v9.py` | 1 | 0 |
| `manuscripts/talks/cns2026/posterior/submit.sh` | 4 | 0 |
| `manuscripts/talks/cns2026/sweep_per_level.py` | 2 | 0 |
| `memory/cns-deck-v2-2026-09-25.md` | 6 | 0 |
| `memory/windows-junction-worktree-trap.md` | 3 | 0 |
| `memory/wsl-for-network.md` | 2 | 0 |

### The banned word in the salvaged May 2026 tex

`manuscripts/neurips_as_submitted_2026-05/main.tex` carried the banned word 1 time(s) (line 492, a paragraph heading 'dual-...'); rewritten to 'lineage' in this copy as the first build did in 13 other files (section 3.3). The submitted PDF beside it is unchanged (a PDF of record). The file is therefore not byte-identical to the laptop source any more; the salvage row above records the source's sha1.

### Student names withheld in the later deck generators too

The acknowledgement string of the v5 to v12 generators also listed the ten student annotators (after 'and the annotators Ashley Schehr, ', the last two joined by 'and'); it now reads `[ten student annotator names withheld]`. Files: `manuscripts/talks/cns2026/make_cns_deck_v10.py`, `manuscripts/talks/cns2026/make_cns_deck_v11_public.py`, `manuscripts/talks/cns2026/make_cns_deck_v12_public.py`, `manuscripts/talks/cns2026/make_cns_deck_v5.py`, `manuscripts/talks/cns2026/make_cns_deck_v6.py`, `manuscripts/talks/cns2026/make_cns_deck_v7.py`, `manuscripts/talks/cns2026/make_cns_deck_v8.py`, `manuscripts/talks/cns2026/make_cns_deck_v9.py`. The statement a few rows above that v5 to v12 never carried the list was wrong and is withdrawn.

### The two CNS decks: core properties emptied; the acknowledgement slide kept for Greg

`manuscripts/talks/cns2026/CNS2026_Schwing_LSTV.pptx` and `CNS2026_Schwing_NotAllSpines_public_v12.pptx` were re-written in place in the final pass with `docProps/core.xml` creator and lastModifiedBy emptied (the second carried a third party's name, the template's author). Both decks' acknowledgement slide names the ten student annotators beside the published co-author and the two radiology residents; the slide text was not changed. DELIBERATE KEEP for Greg (PLAN.md section 5, co-author names): the deck is the one he presents, and a redacted deck is his call, as with the two decks in `11_students_grid_access/manuscripts/talks/`. The salvaged co-author review files in `manuscripts/mpda/coauthor_review/` carry the article's 14-author list in their body as any copy of the manuscript does; same keep, same owner of the decision.
