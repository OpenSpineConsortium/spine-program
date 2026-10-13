# MANIFEST_LOCAL: every file copied into this folder, and every valuable file deliberately not copied

Written by the builder on 2026-10-08 from the copy record of the build (293 files, 36,351,975 bytes). The source
column is a laptop path of that day written with the handoff prefixes; **this section is history, not a**
**dependency**: nothing in this folder reads a laptop path, and every source below also lives in a repository at the
commit named or on the grid (`MANIFEST_CODE.md`, `MANIFEST_GRID.md`). `sha` is the first 16 hex characters of the
source file's SHA-256 at copy time; a text copy that carries a redaction (section 3) differs from its source by
exactly that redaction, for the memory notes by the status header line, and for every file under `docs/handoff/`
by the one-line banner prepended in the fix pass of 2026-10-08 (section 3).

## 0. Prefixes used in the source column

| prefix | laptop path on 2026-10-08 |
|---|---|
| `ssn:` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/ (private repository, branch L6_Class, commit 097933a)` |
| `sn:` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/SchwingNet/ (the same repository)` |
| `ctsp:` | `C:/Users/grego/OneDrive/Desktop/CTSpinoPelvic1K-1/ (public repository, master, 7ddfe38; working tree modified)` |
| `Desktop/` | `C:/Users/grego/OneDrive/Desktop/` |
| `ssn:HANDOFF/context/` | the handoff's redacted memory copies (copy time 2026-10-08 16:39); the live notes under `C:/Users/grego/.claude/projects/c--Users-grego-OneDrive-Desktop-CTSpinoPelvic1K-1/memory/` were not read |

## 1. Files copied (293)

Disposition rows (`../_plan/DISPOSITION.tsv`, project_folder = 08_render_devices, action = copy): carm r24, r25,
r26; ssn r66, r79, r94, r95, r104, r106, r164, r165; mem r24, r26, r28, r29, r45, r64, r69, r80, r86, r93, r94, r95,
r96, r135, r136 and the 22 standing-rule notes tagged `all`; the HANDOFF section pointers mem r195, r196, r197, r209,
r223, r224, r274 (satisfied by the whole-file copies under `docs/handoff/`, PLAN.md section 2 rule 3).

### `results/devices/` (38 files, 1,484,567 bytes)

| copied to | from | bytes | sha | redaction |
|---|---|---:|---|---|
| `results/devices/bv_pulsera.3free.json` | `ssn:docs/devices/bv_pulsera.3free.json` | 91,049 | `079e2012bbfac93f` |  |
| `results/devices/bv_pulsera.frames.csv` | `ssn:docs/devices/bv_pulsera.frames.csv` | 82,733 | `5b697c75c6568fda` |  |
| `results/devices/bv_pulsera.json` | `ssn:docs/devices/bv_pulsera.json` | 85,691 | `deb5953fc4477fa1` |  |
| `results/devices/cios_fusion.3free.json` | `ssn:docs/devices/cios_fusion.3free.json` | 80,718 | `c0801e5f2873e456` |  |
| `results/devices/cios_fusion.frames.csv` | `ssn:docs/devices/cios_fusion.frames.csv` | 252,476 | `3c7c42cd235297fe` |  |
| `results/devices/cios_fusion.json` | `ssn:docs/devices/cios_fusion.json` | 76,061 | `97e23bf59fd76b97` |  |
| `results/devices/elekta_xvi.frames.csv` | `ssn:docs/devices/elekta_xvi.frames.csv` | 222,385 | `1b0752c2deacc2e2` |  |
| `results/devices/elekta_xvi.json` | `ssn:docs/devices/elekta_xvi.json` | 80,764 | `75c1af42d578c3a1` |  |
| `results/devices/pixium_4600.frames.csv` | `ssn:docs/devices/pixium_4600.frames.csv` | 13,156 | `78c44b29b8bd7d36` |  |
| `results/devices/pixium_4600.json` | `ssn:docs/devices/pixium_4600.json` | 69,670 | `23a37d73857f849a` |  |
| `results/devices/census/GE_MEDICAL_SYSTEMS___FLUOROSTAR__frames.csv` | `ssn:docs/devices/census/GE_MEDICAL_SYSTEMS___FLUOROSTAR__frames.csv` | 8,471 | `b02bda528e10b1df` |  |
| `results/devices/census/GE_MEDICAL_SYSTEMS___FLUOROSTAR__headers.json` | `ssn:docs/devices/census/GE_MEDICAL_SYSTEMS___FLUOROSTAR__headers.json` | 5,044 | `d2be8559fecaa5d2` |  |
| `results/devices/census/GE_MEDICAL_SYSTEMS___FLUOROSTAR__headers.md` | `ssn:docs/devices/census/GE_MEDICAL_SYSTEMS___FLUOROSTAR__headers.md` | 2,371 | `606ff4a0e13a2401` |  |
| `results/devices/census/Philips_Medical_Systems___AlluraXper__frames.csv` | `ssn:docs/devices/census/Philips_Medical_Systems___AlluraXper__frames.csv` | 89,921 | `a95d3c5e0997d9ee` |  |
| `results/devices/census/Philips_Medical_Systems___AlluraXper__headers.json` | `ssn:docs/devices/census/Philips_Medical_Systems___AlluraXper__headers.json` | 13,690 | `4c4664615c67cef3` |  |
| `results/devices/census/Philips_Medical_Systems___AlluraXper__headers.md` | `ssn:docs/devices/census/Philips_Medical_Systems___AlluraXper__headers.md` | 6,610 | `d0a9297bf330cc39` |  |
| `results/devices/census/SIEMENS_Healthineers______frames.csv` | `ssn:docs/devices/census/SIEMENS_Healthineers______frames.csv` | 5,423 | `7cfd7069ea0bd2e3` |  |
| `results/devices/census/SIEMENS_Healthineers______headers.json` | `ssn:docs/devices/census/SIEMENS_Healthineers______headers.json` | 3,934 | `ea02336e7cd389fb` |  |
| `results/devices/census/SIEMENS_Healthineers______headers.md` | `ssn:docs/devices/census/SIEMENS_Healthineers______headers.md` | 2,048 | `339e7e63c96f7734` |  |
| `results/devices/census/SIEMENS___Fluorospot_Compact_S1__frames.csv` | `ssn:docs/devices/census/SIEMENS___Fluorospot_Compact_S1__frames.csv` | 571 | `f57463b98a86c78a` |  |
| `results/devices/census/SIEMENS___Fluorospot_Compact_S1__headers.json` | `ssn:docs/devices/census/SIEMENS___Fluorospot_Compact_S1__headers.json` | 20,387 | `a338819871e08e4d` |  |
| `results/devices/census/SIEMENS___Fluorospot_Compact_S1__headers.md` | `ssn:docs/devices/census/SIEMENS___Fluorospot_Compact_S1__headers.md` | 10,251 | `480984064f9f7951` |  |
| `results/devices/census/SKANRAY_TECHNOLOGIES______frames.csv` | `ssn:docs/devices/census/SKANRAY_TECHNOLOGIES______frames.csv` | 11,271 | `8bc8751a96c7a062` |  |
| `results/devices/census/SKANRAY_TECHNOLOGIES______headers.json` | `ssn:docs/devices/census/SKANRAY_TECHNOLOGIES______headers.json` | 9,083 | `ae2c867b8a2157ac` |  |
| `results/devices/census/SKANRAY_TECHNOLOGIES______headers.md` | `ssn:docs/devices/census/SKANRAY_TECHNOLOGIES______headers.md` | 3,816 | `8ae695ac70390471` |  |
| `results/devices/census/_______frames.csv` | `ssn:docs/devices/census/_______frames.csv` | 9,352 | `e01f3c2cf3af0608` |  |
| `results/devices/census/_______headers.json` | `ssn:docs/devices/census/_______headers.json` | 3,938 | `859955df1dcf5582` |  |
| `results/devices/census/_______headers.md` | `ssn:docs/devices/census/_______headers.md` | 1,855 | `1195a39a88a82bcc` |  |
| `results/devices/census/surgio_b51__frames.csv` | `ssn:docs/devices/census/surgio_b51__frames.csv` | 150,917 | `28e9ec10b3c81999` |  |
| `results/devices/census/surgio_b51__headers.json` | `ssn:docs/devices/census/surgio_b51__headers.json` | 19,892 | `82b093c5b3fc7ebd` |  |
| `results/devices/census/surgio_b51__headers.md` | `ssn:docs/devices/census/surgio_b51__headers.md` | 6,874 | `66837dd00b6ec565` |  |
| `results/devices/census/ziehm_imaging___ZiehmNetPort__frames.csv` | `ssn:docs/devices/census/ziehm_imaging___ZiehmNetPort__frames.csv` | 1,377 | `c1761c6beb58b5a2` |  |
| `results/devices/census/ziehm_imaging___ZiehmNetPort__headers.json` | `ssn:docs/devices/census/ziehm_imaging___ZiehmNetPort__headers.json` | 5,045 | `50736911d8adbcc2` |  |
| `results/devices/census/ziehm_imaging___ZiehmNetPort__headers.md` | `ssn:docs/devices/census/ziehm_imaging___ZiehmNetPort__headers.md` | 2,478 | `cd2e3eeb3a347fc1` |  |
| `results/devices/eval_gate/bv_pulsera.json` | `ssn:docs/devices/eval_gate/bv_pulsera.json` | 9,691 | `4f3ac275ebb81cbc` |  |
| `results/devices/eval_gate/cios_fusion.json` | `ssn:docs/devices/eval_gate/cios_fusion.json` | 7,940 | `e808cda758c3a559` |  |
| `results/devices/eval_gate/elekta_xvi.json` | `ssn:docs/devices/eval_gate/elekta_xvi.json` | 7,871 | `36cc271e0a4bb5f2` |  |
| `results/devices/eval_gate/pixium_4600.json` | `ssn:docs/devices/eval_gate/pixium_4600.json` | 9,743 | `71a6c1daa990789b` |  |

### `docs/` (14 files, 237,530 bytes)

| copied to | from | bytes | sha | redaction |
|---|---|---:|---|---|
| `docs/DEEPFLUORO_FORMATION.md` | `ssn:docs/DEEPFLUORO_FORMATION.md` | 36,102 | `0db43fe7ed7e6961` |  |
| `docs/PHYSICS_LINKING.md` | `ssn:docs/PHYSICS_LINKING.md` | 36,601 | `34689b053f20514e` |  |
| `docs/HANDOFF_PHYSICS.md` | `ssn:docs/HANDOFF_PHYSICS.md` | 30,048 | `c6594eb75df52fa2` |  |
| `docs/SIMULATION_FIDELITY.md` | `ssn:docs/SIMULATION_FIDELITY.md` | 8,656 | `6f402b459b7d6ceb` |  |
| `docs/DEVICE_PARAM_AUDIT.md` | `ssn:docs/DEVICE_PARAM_AUDIT.md` | 13,348 | `bef0c794a7342309` |  |
| `docs/DEVICE_SPREAD_SWEEP.md` | `ssn:docs/DEVICE_SPREAD_SWEEP.md` | 3,192 | `932fb612be5e99e3` |  |
| `docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md` | `ssn:docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md` | 5,216 | `5a59d8497c9c8f41` |  |
| `docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md` | `ssn:docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md` | 8,206 | `d35d2a2604982d09` |  |
| `docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md` | `ssn:docs/MORPHOLOGY_SYNTHESIS_PRIOR_ART.md` | 25,163 | `41a2f1ee5f15d05a` |  |
| `docs/or_ready_audit_track_2026-09-22.json` | `ssn:docs/or_ready_audit_track_2026-09-22.json` | 13,741 | `474691b970034210` |  |
| `docs/path_census.json` | `ssn:docs/path_census.json` | 1,959 | `8d9edd36ef33d6e7` |  |
| `docs/polypose_reference_envelope.json` | `ssn:docs/polypose_reference_envelope.json` | 8,262 | `b81f2459c3956e2c` |  |
| `docs/polypose_segmental_rom.csv` | `ssn:docs/polypose_segmental_rom.csv` | 3,344 | `91503e01b27fa501` |  |
| `docs/Synthetic real ratio X-ray detectors.md` | `ssn:reports/Synthetic real ratio X-ray detectors.md` | 43,692 | `d150fc956b77d536` |  |

### `figures/` (3 files, 1,251,828 bytes)

| copied to | from | bytes | sha | redaction |
|---|---|---:|---|---|
| `figures/fig_device_params.png` | `ssn:docs/fig_device_params.png` | 521,818 | `af83190baaccb8da` |  |
| `figures/fig_device_spread.png` | `ssn:docs/fig_device_spread.png` | 199,615 | `597c51ec7584044c` |  |
| `figures/docs_figures/fig_device_params.png` | `ssn:docs/figures/fig_device_params.png` | 530,395 | `ff290ad5727c46b7` |  |

### `results/manifold/` (30 files, 15,089,691 bytes)

| copied to | from | bytes | sha | redaction |
|---|---|---:|---|---|
| `results/manifold/MANIFOLD.md` | `sn:results/manifold/MANIFOLD.md` | 39,974 | `fede2b6c3d2cbcc6` |  |
| `results/manifold/deep_index.csv` | `sn:results/manifold/deep_index.csv` | 1,434,534 | `18561c81a983aab7` |  |
| `results/manifold/deep_info.json` | `sn:results/manifold/deep_info.json` | 308 | `4ebac07c28173465` |  |
| `results/manifold/embedding.csv` | `sn:results/manifold/embedding.csv` | 4,162,247 | `e3aa69f35c36bde5` |  |
| `results/manifold/features.csv` | `sn:results/manifold/features.csv` | 7,364,605 | `114cb70e8d2d1839` |  |
| `results/manifold/fig1_row4_manifold.png` | `sn:results/manifold/fig1_row4_manifold.png` | 480,422 | `6204477578559a05` |  |
| `results/manifold/fig_corpus_manifold.png` | `sn:results/manifold/fig_corpus_manifold.png` | 511,269 | `1e05c0998ec916f2` |  |
| `results/manifold/overlap.json` | `sn:results/manifold/overlap.json` | 18,399 | `9a941dcde5f9ca50` |  |
| `results/manifold/pairwise_deep_logistic.csv` | `sn:results/manifold/pairwise_deep_logistic.csv` | 2,460 | `b3dbb58e92cfd72d` |  |
| `results/manifold/pairwise_deep_svm.csv` | `sn:results/manifold/pairwise_deep_svm.csv` | 2,460 | `8cdc9fa4f1b50ef2` |  |
| `results/manifold/pairwise_stats_logistic.csv` | `sn:results/manifold/pairwise_stats_logistic.csv` | 2,460 | `954a72233afcddec` |  |
| `results/manifold/pairwise_stats_svm.csv` | `sn:results/manifold/pairwise_stats_svm.csv` | 2,460 | `0dcdd06290a4cb4a` |  |
| `results/manifold/probes.json` | `sn:results/manifold/probes.json` | 212,590 | `58c2035551bc28e2` |  |
| `results/manifold/examples/cios_fusion/examples.json` | `sn:results/manifold/examples/cios_fusion/examples.json` | 1,184 | `d793952d944eb5a9` |  |
| `results/manifold/examples/cios_fusion/real.png` | `sn:results/manifold/examples/cios_fusion/real.png` | 63,233 | `46414e9ffe65cd80` |  |
| `results/manifold/examples/cios_fusion/styled.png` | `sn:results/manifold/examples/cios_fusion/styled.png` | 105,960 | `6988a3dba21f09a3` |  |
| `results/manifold/examples/cios_fusion/unstyled.png` | `sn:results/manifold/examples/cios_fusion/unstyled.png` | 57,404 | `5efa7bb49078d656` |  |
| `results/manifold/examples/cios_fusion/vanilla.png` | `sn:results/manifold/examples/cios_fusion/vanilla.png` | 36,200 | `c2ff8d88c7492925` |  |
| `results/manifold/examples/elekta_xvi/examples.json` | `sn:results/manifold/examples/elekta_xvi/examples.json` | 1,173 | `6aba79c6d16694f6` |  |
| `results/manifold/examples/elekta_xvi/real.png` | `sn:results/manifold/examples/elekta_xvi/real.png` | 72,088 | `0cf4a93446e2d0d8` |  |
| `results/manifold/examples/elekta_xvi/styled.png` | `sn:results/manifold/examples/elekta_xvi/styled.png` | 44,324 | `1200c2179efc8a19` |  |
| `results/manifold/examples/elekta_xvi/unstyled.png` | `sn:results/manifold/examples/elekta_xvi/unstyled.png` | 44,147 | `ff5500e9c2260288` |  |
| `results/manifold/examples/elekta_xvi/vanilla.png` | `sn:results/manifold/examples/elekta_xvi/vanilla.png` | 36,200 | `c2ff8d88c7492925` |  |
| `results/manifold/examples/surgio_b51_dr/examples.json` | `sn:results/manifold/examples/surgio_b51_dr/examples.json` | 1,201 | `7ef98ca18fe21c5e` |  |
| `results/manifold/examples/surgio_b51_dr/real.png` | `sn:results/manifold/examples/surgio_b51_dr/real.png` | 157,038 | `5c5f1097e2d6ab52` |  |
| `results/manifold/examples/surgio_b51_dr/styled.png` | `sn:results/manifold/examples/surgio_b51_dr/styled.png` | 124,713 | `76b4c1ef041f2e73` |  |
| `results/manifold/examples/surgio_b51_dr/unstyled.png` | `sn:results/manifold/examples/surgio_b51_dr/unstyled.png` | 36,603 | `0c0de4fdf4fc662c` |  |
| `results/manifold/examples/surgio_b51_dr/vanilla.png` | `sn:results/manifold/examples/surgio_b51_dr/vanilla.png` | 36,200 | `c2ff8d88c7492925` |  |
| `results/manifold/formation_gap/FORMATION_GAP.md` | `sn:results/manifold/formation_gap/FORMATION_GAP.md` | 4,629 | `9169af640077d74c` |  |
| `results/manifold/formation_gap/formation_gap.json` | `sn:results/manifold/formation_gap/formation_gap.json` | 33,206 | `5c31008dc2e2d396` |  |

### `results/polypose/` (111 files, 15,997,363 bytes)

| copied to | from | bytes | sha | redaction |
|---|---|---:|---|---|
| `results/polypose/POLYPOSE_API.md` | `sn:results/polypose/POLYPOSE_API.md` | 18,098 | `6fb6f69771ac04e1` |  |
| `results/polypose/REPRODUCIBILITY.md` | `sn:results/polypose/REPRODUCIBILITY.md` | 14,653 | `d10836dd15988587` |  |
| `results/polypose/REPRODUCTION.json` | `sn:results/polypose/REPRODUCTION.json` | 35,847 | `856b13058e56e509` |  |
| `results/polypose/REPRODUCTION.md` | `sn:results/polypose/REPRODUCTION.md` | 7,590 | `3242041c24e6a4e7` |  |
| `results/polypose/REPRODUCTION_attempt1_noflip.md` | `sn:results/polypose/REPRODUCTION_attempt1_noflip.md` | 6,073 | `da037c5be26f9bd9` |  |
| `results/polypose/SAMPLING_SPEC.md` | `sn:results/polypose/SAMPLING_SPEC.md` | 42,051 | `6fc8ae5168086b31` |  |
| `results/polypose/cohort_ctsp_release.json` | `sn:results/polypose/cohort_ctsp_release.json` | 469,580 | `6d80670dad27a505` |  |
| `results/polypose/cohort_sagittal.json` | `sn:results/polypose/cohort_sagittal.json` | 994,405 | `fb03312ed9fdb292` |  |
| `results/polypose/cohort_sagittal.png` | `sn:results/polypose/cohort_sagittal.png` | 750,737 | `3e16ad4abd7702a1` |  |
| `results/polypose/forward_test.json` | `sn:results/polypose/forward_test.json` | 17,731 | `723446a87890de92` |  |
| `results/polypose/joint_model_numbers.json` | `sn:results/polypose/joint_model_numbers.json` | 1,154 | `09888d8d1f8cdbb3` |  |
| `results/polypose/render_subject1_view0.png` | `sn:results/polypose/render_subject1_view0.png` | 240,893 | `183b4bc2d3e11954` |  |
| `results/polypose/rom_cine.json` | `sn:results/polypose/rom_cine.json` | 8,846 | `508f73bd2eaec796` |  |
| `results/polypose/sampling_spec.json` | `sn:results/polypose/sampling_spec.json` | 114,732 | `192c264ba22fd888` |  |
| `results/polypose/sampling_spec.v1.json` | `sn:results/polypose/sampling_spec.v1.json` | 36,583 | `2755b6a3c65dbf44` |  |
| `results/polypose/subject01_render.png` | `sn:results/polypose/subject01_render.png` | 353,807 | `063362abfabb88aa` |  |
| `results/polypose/cohort_rows/cohort_grid.json` | `sn:results/polypose/cohort_rows/cohort_grid.json` | 1,165,467 | `06fa10c40d5036b4` |  |
| `results/polypose/cohort_rows/cohort_grid.md` | `sn:results/polypose/cohort_rows/cohort_grid.md` | 5,615 | `a45c5fc9881727a2` |  |
| `results/polypose/cohort_rows/rows_00.jsonl` | `sn:results/polypose/cohort_rows/rows_00.jsonl` | 167,682 | `43d32999423aafa7` |  |
| `results/polypose/cohort_rows/rows_01.jsonl` | `sn:results/polypose/cohort_rows/rows_01.jsonl` | 167,612 | `4e22eb71f6669890` |  |
| `results/polypose/cohort_rows/rows_02.jsonl` | `sn:results/polypose/cohort_rows/rows_02.jsonl` | 169,490 | `3f60cb01d9178799` |  |
| `results/polypose/cohort_rows/rows_03.jsonl` | `sn:results/polypose/cohort_rows/rows_03.jsonl` | 166,970 | `343cf2a2b9c47989` |  |
| `results/polypose/cohort_rows/rows_04.jsonl` | `sn:results/polypose/cohort_rows/rows_04.jsonl` | 165,397 | `5c6328dd9d14b0db` |  |
| `results/polypose/cohort_rows/rows_05.jsonl` | `sn:results/polypose/cohort_rows/rows_05.jsonl` | 168,288 | `015c9f2b94b0cded` |  |
| `results/polypose/cohort_rows/rows_06.jsonl` | `sn:results/polypose/cohort_rows/rows_06.jsonl` | 165,287 | `ba7f01c907259a06` |  |
| `results/polypose/cohort_rows/rows_07.jsonl` | `sn:results/polypose/cohort_rows/rows_07.jsonl` | 167,621 | `d1de2d8dfde3d0de` |  |
| `results/polypose/cohort_rows/rows_08.jsonl` | `sn:results/polypose/cohort_rows/rows_08.jsonl` | 167,420 | `e84514d120df5cb1` |  |
| `results/polypose/cohort_rows/rows_09.jsonl` | `sn:results/polypose/cohort_rows/rows_09.jsonl` | 167,353 | `0544fd7c24ba05ff` |  |
| `results/polypose/cohort_rows/rows_10.jsonl` | `sn:results/polypose/cohort_rows/rows_10.jsonl` | 164,977 | `6c3d458912fc5ac9` |  |
| `results/polypose/cohort_rows/rows_11.jsonl` | `sn:results/polypose/cohort_rows/rows_11.jsonl` | 168,977 | `f3ee94c7e81a3217` |  |
| `results/polypose/cohort_rows/rows_12.jsonl` | `sn:results/polypose/cohort_rows/rows_12.jsonl` | 166,981 | `b362a0cafd800034` |  |
| `results/polypose/cohort_rows/rows_13.jsonl` | `sn:results/polypose/cohort_rows/rows_13.jsonl` | 167,580 | `e6f45a56860394ee` |  |
| `results/polypose/cohort_rows/rows_14.jsonl` | `sn:results/polypose/cohort_rows/rows_14.jsonl` | 169,283 | `0fc307289104c1a9` |  |
| `results/polypose/cohort_rows/rows_15.jsonl` | `sn:results/polypose/cohort_rows/rows_15.jsonl` | 167,280 | `113f64f2f1019b2f` |  |
| `results/polypose/cohort_rows/rows_16.jsonl` | `sn:results/polypose/cohort_rows/rows_16.jsonl` | 43,778 | `8a56e5c2538bd79f` |  |
| `results/polypose/cohort_rows/rows_17.jsonl` | `sn:results/polypose/cohort_rows/rows_17.jsonl` | 84,682 | `582a8bf0276bc0f5` |  |
| `results/polypose/cohort_rows/rows_18.jsonl` | `sn:results/polypose/cohort_rows/rows_18.jsonl` | 61,318 | `866eb31f6b1923bf` |  |
| `results/polypose/cohort_rows/rows_19.jsonl` | `sn:results/polypose/cohort_rows/rows_19.jsonl` | 35,698 | `3a03c694ca10818e` |  |
| `results/polypose/cohort_rows/rows_20.jsonl` | `sn:results/polypose/cohort_rows/rows_20.jsonl` | 59,520 | `2536eb46c4a8f103` |  |
| `results/polypose/cohort_rows/rows_21.jsonl` | `sn:results/polypose/cohort_rows/rows_21.jsonl` | 61,815 | `6172b739cc64ac3a` |  |
| `results/polypose/cohort_rows/rows_22.jsonl` | `sn:results/polypose/cohort_rows/rows_22.jsonl` | 66,634 | `d3a7369b3eca54e2` |  |
| `results/polypose/cohort_rows/rows_23.jsonl` | `sn:results/polypose/cohort_rows/rows_23.jsonl` | 56,449 | `ed7e27590c348468` |  |
| `results/polypose/diag/drr_diag.json` | `sn:results/polypose/diag/drr_diag.json` | 2,762 | `b797c2314a86083b` |  |
| `results/polypose/diag/drr_diag.png` | `sn:results/polypose/diag/drr_diag.png` | 358,596 | `6b28a76a26336636` |  |
| `results/polypose/diag/drr_diag2.json` | `sn:results/polypose/diag/drr_diag2.json` | 1,082 | `33678d989d5c1e27` |  |
| `results/polypose/diag/drr_diag2.png` | `sn:results/polypose/diag/drr_diag2.png` | 146,767 | `7e936b0a10fdab7b` |  |
| `results/polypose/diag/drr_diag3.json` | `sn:results/polypose/diag/drr_diag3.json` | 2,207 | `9de3daec4d6cefdc` |  |
| `results/polypose/diag/drr_diag3.png` | `sn:results/polypose/diag/drr_diag3.png` | 1,103,181 | `3e15d7822a0385b7` |  |
| `results/polypose/inputs/TRANSITIONAL_LABELS.csv` | `sn:results/polypose/inputs/TRANSITIONAL_LABELS.csv` | 2,437,973 | `6d34c7554e59b1ca` |  |
| `results/polypose/inputs/buu3600_lstv_labels.csv` | `sn:results/polypose/inputs/buu3600_lstv_labels.csv` | 1,546,797 | `c7ed1bcb4da7e3ef` |  |
| `results/polypose/inputs/buu400_lstv_labels.csv` | `sn:results/polypose/inputs/buu400_lstv_labels.csv` | 181,161 | `c2c88cba1cb87b42` |  |
| `results/polypose/inputs/lstv_flag_labels_v2.csv` | `sn:results/polypose/inputs/lstv_flag_labels_v2.csv` | 249,475 | `e939da769bf848a2` |  |
| `results/polypose/inputs/verse_suppl_table1.csv` | `sn:results/polypose/inputs/verse_suppl_table1.csv` | 18,534 | `5cbcea45dd625ab1` |  |
| `results/polypose/report/REPRODUCTION.json` | `sn:results/polypose/report/REPRODUCTION.json` | 35,847 | `856b13058e56e509` |  |
| `results/polypose/report/REPRODUCTION.md` | `sn:results/polypose/report/REPRODUCTION.md` | 7,590 | `3242041c24e6a4e7` |  |
| `results/polypose/report/hf_vs_h5.json` | `sn:results/polypose/report/hf_vs_h5.json` | 10,263 | `b7c4dcb6f57a0d27` |  |
| `results/polypose/report/attempt1_noflip/REPRODUCTION.json` | `sn:results/polypose/report/attempt1_noflip/REPRODUCTION.json` | 31,308 | `81c158483f56dc96` |  |
| `results/polypose/report/attempt1_noflip/REPRODUCTION.md` | `sn:results/polypose/report/attempt1_noflip/REPRODUCTION.md` | 6,073 | `da037c5be26f9bd9` |  |
| `results/polypose/report/attempt1_noflip/1/polypose.sha256` | `sn:results/polypose/report/attempt1_noflip/1/polypose.sha256` | 256 | `0acb1735674fa29b` |  |
| `results/polypose/report/attempt1_noflip/1/polypose.txt` | `sn:results/polypose/report/attempt1_noflip/1/polypose.txt` | 6 | `297d62f39fae64ee` |  |
| `results/polypose/report/attempt1_noflip/1/polypose_run.json` | `sn:results/polypose/report/attempt1_noflip/1/polypose_run.json` | 918 | `ed3164e1cec145ed` |  |
| `results/polypose/report/attempt1_noflip/2/polypose.sha256` | `sn:results/polypose/report/attempt1_noflip/2/polypose.sha256` | 256 | `e54dd3ae61e72ec5` |  |
| `results/polypose/report/attempt1_noflip/2/polypose.txt` | `sn:results/polypose/report/attempt1_noflip/2/polypose.txt` | 6 | `297d62f39fae64ee` |  |
| `results/polypose/report/attempt1_noflip/2/polypose_run.json` | `sn:results/polypose/report/attempt1_noflip/2/polypose_run.json` | 919 | `b738bd3c2e96a903` |  |
| `results/polypose/report/attempt1_noflip/3/polypose.sha256` | `sn:results/polypose/report/attempt1_noflip/3/polypose.sha256` | 256 | `b4528b240a63bbfb` |  |
| `results/polypose/report/attempt1_noflip/3/polypose.txt` | `sn:results/polypose/report/attempt1_noflip/3/polypose.txt` | 6 | `297d62f39fae64ee` |  |
| `results/polypose/report/attempt1_noflip/3/polypose_run.json` | `sn:results/polypose/report/attempt1_noflip/3/polypose_run.json` | 918 | `6c806a193d6b2bd2` |  |
| `results/polypose/report/attempt1_noflip/4/polypose.sha256` | `sn:results/polypose/report/attempt1_noflip/4/polypose.sha256` | 256 | `d9345913e8f4a60b` |  |
| `results/polypose/report/attempt1_noflip/4/polypose.txt` | `sn:results/polypose/report/attempt1_noflip/4/polypose.txt` | 6 | `297d62f39fae64ee` |  |
| `results/polypose/report/attempt1_noflip/4/polypose_run.json` | `sn:results/polypose/report/attempt1_noflip/4/polypose_run.json` | 918 | `9398ff6c9740d8ef` |  |
| `results/polypose/report/attempt1_noflip/5/polypose.sha256` | `sn:results/polypose/report/attempt1_noflip/5/polypose.sha256` | 256 | `22171d7fd39b8c49` |  |
| `results/polypose/report/attempt1_noflip/5/polypose.txt` | `sn:results/polypose/report/attempt1_noflip/5/polypose.txt` | 6 | `297d62f39fae64ee` |  |
| `results/polypose/report/attempt1_noflip/5/polypose_run.json` | `sn:results/polypose/report/attempt1_noflip/5/polypose_run.json` | 918 | `f9576177886ab1ed` |  |
| `results/polypose/report/attempt1_noflip/6/polypose.sha256` | `sn:results/polypose/report/attempt1_noflip/6/polypose.sha256` | 256 | `4aad67732e716bbf` |  |
| `results/polypose/report/attempt1_noflip/6/polypose.txt` | `sn:results/polypose/report/attempt1_noflip/6/polypose.txt` | 6 | `297d62f39fae64ee` |  |
| `results/polypose/report/attempt1_noflip/6/polypose_run.json` | `sn:results/polypose/report/attempt1_noflip/6/polypose_run.json` | 916 | `118dce43af8831d7` |  |
| `results/polypose/report/attempt1_noflip/eval/metrics_views.csv` | `sn:results/polypose/report/attempt1_noflip/eval/metrics_views.csv` | 22,562 | `2a2a6118cebac103` |  |
| `results/polypose/report/attempt1_noflip/eval/render_subject1_view0.png` | `sn:results/polypose/report/attempt1_noflip/eval/render_subject1_view0.png` | 145,786 | `4a64538e6369854d` |  |
| `results/polypose/report/attempt1_noflip/eval/summary.json` | `sn:results/polypose/report/attempt1_noflip/eval/summary.json` | 11,211 | `b7a9dd6c9efbb52d` |  |
| `results/polypose/report/diag/drr_diag.json` | `sn:results/polypose/report/diag/drr_diag.json` | 2,762 | `b797c2314a86083b` |  |
| `results/polypose/report/diag/drr_diag.png` | `sn:results/polypose/report/diag/drr_diag.png` | 358,596 | `6b28a76a26336636` |  |
| `results/polypose/report/diag2/drr_diag2.json` | `sn:results/polypose/report/diag2/drr_diag2.json` | 1,082 | `33678d989d5c1e27` |  |
| `results/polypose/report/diag2/drr_diag2.png` | `sn:results/polypose/report/diag2/drr_diag2.png` | 146,767 | `7e936b0a10fdab7b` |  |
| `results/polypose/report/diag3/drr_diag3.json` | `sn:results/polypose/report/diag3/drr_diag3.json` | 2,207 | `9de3daec4d6cefdc` |  |
| `results/polypose/report/diag3/drr_diag3.png` | `sn:results/polypose/report/diag3/drr_diag3.png` | 1,103,181 | `3e15d7822a0385b7` |  |
| `results/polypose/validation/inspect/0008_sag.png` | `sn:results/polypose/validation/inspect/0008_sag.png` | 13,126 | `ca0d7be9e72a25cc` |  |
| `results/polypose/validation/inspect/0033_sag.png` | `sn:results/polypose/validation/inspect/0033_sag.png` | 13,680 | `ec7e3096bda795d1` |  |
| `results/polypose/validation/inspect/0049_sag.png` | `sn:results/polypose/validation/inspect/0049_sag.png` | 13,038 | `7b445feeceacce69` |  |
| `results/polypose/validation/inspect/0153_sag.png` | `sn:results/polypose/validation/inspect/0153_sag.png` | 14,688 | `4ced06a9605972ea` |  |
| `results/polypose/validation/inspect/0170_sag.png` | `sn:results/polypose/validation/inspect/0170_sag.png` | 13,294 | `e1befb4101aade2b` |  |
| `results/polypose/validation/inspect/0244_sag.png` | `sn:results/polypose/validation/inspect/0244_sag.png` | 12,504 | `c38dd328d165be64` |  |
| `results/polypose/validation/inspect/0277_sag.png` | `sn:results/polypose/validation/inspect/0277_sag.png` | 13,021 | `90636913702231d0` |  |
| `results/polypose/validation/inspect/0285_sag.png` | `sn:results/polypose/validation/inspect/0285_sag.png` | 14,196 | `048e8d4bb1b0e1f3` |  |
| `results/polypose/validation/inspect/0302_sag.png` | `sn:results/polypose/validation/inspect/0302_sag.png` | 15,616 | `168f4242a4eebe08` |  |
| `results/polypose/validation/inspect/0376_sag.png` | `sn:results/polypose/validation/inspect/0376_sag.png` | 14,095 | `89ffc40d0d5bfa25` |  |
| `results/polypose/validation/inspect/0399_sag.png` | `sn:results/polypose/validation/inspect/0399_sag.png` | 13,883 | `33f934201a6d1a07` |  |
| `results/polypose/validation/inspect/0428_sag.png` | `sn:results/polypose/validation/inspect/0428_sag.png` | 12,802 | `d00d4ed955004463` |  |
| `results/polypose/validation/inspect/0473_sag.png` | `sn:results/polypose/validation/inspect/0473_sag.png` | 13,417 | `a924cd68f756e3b3` |  |
| `results/polypose/validation/inspect/0765_sag.png` | `sn:results/polypose/validation/inspect/0765_sag.png` | 14,520 | `4bd3da5afaee91b5` |  |
| `results/polypose/validation/inspect/0801_sag.png` | `sn:results/polypose/validation/inspect/0801_sag.png` | 12,993 | `c9f148749933c13e` |  |
| `results/polypose/validation/inspect/0874_sag.png` | `sn:results/polypose/validation/inspect/0874_sag.png` | 14,128 | `b77f3b04d542a8d8` |  |
| `results/polypose/validation/inspect/0901_sag.png` | `sn:results/polypose/validation/inspect/0901_sag.png` | 12,059 | `73d3658c966ee667` |  |
| `results/polypose/validation/inspect/0931_sag.png` | `sn:results/polypose/validation/inspect/0931_sag.png` | 12,703 | `2cf8ccd004453df0` |  |
| `results/polypose/validation/inspect/0950_sag.png` | `sn:results/polypose/validation/inspect/0950_sag.png` | 12,193 | `38dbbada2365ec06` |  |
| `results/polypose/validation/inspect/1004_sag.png` | `sn:results/polypose/validation/inspect/1004_sag.png` | 12,456 | `f8533c104f4cee5f` |  |
| `results/polypose/validation/inspect/1065_sag.png` | `sn:results/polypose/validation/inspect/1065_sag.png` | 13,285 | `f6e0a623e5e25978` |  |
| `results/polypose/validation/inspect/1123_sag.png` | `sn:results/polypose/validation/inspect/1123_sag.png` | 13,197 | `f2065b160a6f8823` |  |
| `results/polypose/validation/inspect/inspect.json` | `sn:results/polypose/validation/inspect/inspect.json` | 30,056 | `3a80f594ed63c7b8` |  |
| `results/polypose/validation/smoke/pp_ctsp_0874_v000_ap.png` | `sn:results/polypose/validation/smoke/pp_ctsp_0874_v000_ap.png` | 138,687 | `df101e3c0a07a962` |  |
| `results/polypose/validation/smoke/pp_ctsp_0874_v000_lat.png` | `sn:results/polypose/validation/smoke/pp_ctsp_0874_v000_lat.png` | 124,755 | `61d92b31c1e611ab` |  |
| `results/polypose/validation/smoke/pending/pp_ctsp_0874_v000.json` | `sn:results/polypose/validation/smoke/pending/pp_ctsp_0874_v000.json` | 36,168 | `1223565c5d51ad2a` |  |

### `docs/research_notes/` (14 files, 499,986 bytes)

| copied to | from | bytes | sha | redaction |
|---|---|---:|---|---|
| `docs/research_notes/spine synthesis prior art/biomech.md` | `ssn:research_notes/spine synthesis prior art/biomech.md` | 36,403 | `864a6c4117fd30c3` |  |
| `docs/research_notes/spine synthesis prior art/diffusion.md` | `ssn:research_notes/spine synthesis prior art/diffusion.md` | 32,378 | `6480d5ae51ce4780` |  |
| `docs/research_notes/spine synthesis prior art/downstream.md` | `ssn:research_notes/spine synthesis prior art/downstream.md` | 52,917 | `1ec3a4b655424ec9` |  |
| `docs/research_notes/spine synthesis prior art/rare-variant.md` | `ssn:research_notes/spine synthesis prior art/rare-variant.md` | 45,855 | `7cd1fc8f08b1ce41` |  |
| `docs/research_notes/spine synthesis prior art/registration.md` | `ssn:research_notes/spine synthesis prior art/registration.md` | 47,889 | `601d96dae1b6dd7f` |  |
| `docs/research_notes/spine synthesis prior art/ssm-verify-meng2020.md` | `ssn:research_notes/spine synthesis prior art/ssm-verify-meng2020.md` | 22,714 | `6aed63d23edc9871` | e-mail withheld |
| `docs/research_notes/spine synthesis prior art/ssm-verify-schmid2023.md` | `ssn:research_notes/spine synthesis prior art/ssm-verify-schmid2023.md` | 13,643 | `6adcd92d1bc526cc` |  |
| `docs/research_notes/spine synthesis prior art/ssm.md` | `ssn:research_notes/spine synthesis prior art/ssm.md` | 87,286 | `972553efb4ec0a14` |  |
| `docs/research_notes/spine synthesis prior art/verify-SIM-castro-mateos-2015.md` | `ssn:research_notes/spine synthesis prior art/verify-SIM-castro-mateos-2015.md` | 16,671 | `d7853d1c33c3bf3a` |  |
| `docs/research_notes/spine synthesis prior art/verify-gpmm.md` | `ssn:research_notes/spine synthesis prior art/verify-gpmm.md` | 10,950 | `9c11700a189fc88a` |  |
| `docs/research_notes/Synthetic real ratio X-ray detectors/fidelity_vs_ratio.md` | `ssn:research_notes/Synthetic real ratio X-ray detectors/fidelity_vs_ratio.md` | 34,643 | `762e61e1520c920d` |  |
| `docs/research_notes/Synthetic real ratio X-ray detectors/mixing_ratios.md` | `ssn:research_notes/Synthetic real ratio X-ray detectors/mixing_ratios.md` | 32,823 | `408b65b170e4d180` |  |
| `docs/research_notes/Synthetic real ratio X-ray detectors/rare_class_oversampling.md` | `ssn:research_notes/Synthetic real ratio X-ray detectors/rare_class_oversampling.md` | 36,701 | `219496688ae95945` |  |
| `docs/research_notes/Synthetic real ratio X-ray detectors/scaling_and_curricula.md` | `ssn:research_notes/Synthetic real ratio X-ray detectors/scaling_and_curricula.md` | 29,113 | `413776424b824b4c` |  |

### `docs/handoff/` (43 files, 1,689,292 bytes)

| copied to | from | bytes | sha | redaction |
|---|---|---:|---|---|
| `docs/handoff/README.md` | `ssn:HANDOFF/README.md` | 42,567 | `9db77ff0bea0fe4b` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/GLOSSARY.md` | `ssn:HANDOFF/GLOSSARY.md` | 25,368 | `a01539499ebb2e0a` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/RECIPES.md` | `ssn:HANDOFF/RECIPES.md` | 73,585 | `e611bed3135db715` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/RESULTS_CATALOG.md` | `ssn:HANDOFF/RESULTS_CATALOG.md` | 110,438 | `7fcb5ab36518fc98` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/DATASET_USAGE.md` | `ssn:HANDOFF/DATASET_USAGE.md` | 37,254 | `8a3e0de6e956b142` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/LEAKAGE.md` | `ssn:HANDOFF/LEAKAGE.md` | 25,299 | `121631d92d5463a8` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/OPEN_QUESTIONS.md` | `ssn:HANDOFF/OPEN_QUESTIONS.md` | 28,532 | `51c87379d06ae779` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/INFRASTRUCTURE.md` | `ssn:HANDOFF/INFRASTRUCTURE.md` | 48,550 | `fd90e68d8c16ab09` | name/username -> 'go2432 and the C&IT administrator'; banner prepended (fix pass 2026-10-08) |
| `docs/handoff/MANUSCRIPTS.md` | `ssn:HANDOFF/MANUSCRIPTS.md` | 67,604 | `d802a8b1751198b8` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/CONTEXT_EXPORT.md` | `ssn:HANDOFF/CONTEXT_EXPORT.md` | 34,696 | `add69838139a04ed` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/RESEARCH_DIRECTIONS.md` | `ssn:HANDOFF/RESEARCH_DIRECTIONS.md` | 133,695 | `6bbb807287077766` | e-mail withheld; banner prepended (fix pass 2026-10-08) |
| `docs/handoff/LITERATURE_STATE.md` | `ssn:HANDOFF/LITERATURE_STATE.md` | 170,864 | `cc34b58004cb655f` | e-mail withheld; banner prepended (fix pass 2026-10-08) |
| `docs/handoff/literature_state/assemble.py` | `ssn:HANDOFF/literature_state/assemble.py` | 2,233 | `9523271f08d33220` | do-not-run header prepended (fix pass 2026-10-08) |
| `docs/handoff/literature_state/biblio_sorted.py` | `ssn:HANDOFF/literature_state/biblio_sorted.py` | 2,213 | `47ec6799a5f07ec7` |  |
| `docs/handoff/literature_state/calc_addendum.json` | `ssn:HANDOFF/literature_state/calc_addendum.json` | 308 | `7f4e48540d5c93dd` |  |
| `docs/handoff/literature_state/calc_addendum.py` | `ssn:HANDOFF/literature_state/calc_addendum.py` | 1,589 | `d3d3a8841eae8e06` |  |
| `docs/handoff/literature_state/calc_review.json` | `ssn:HANDOFF/literature_state/calc_review.json` | 1,381 | `dcd1521601b49d36` |  |
| `docs/handoff/literature_state/calc_review.py` | `ssn:HANDOFF/literature_state/calc_review.py` | 3,098 | `71236a1aac4059c8` |  |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | `ssn:HANDOFF/literature_state/dataset_landscape_by_task.md` | 61,579 | `348a8419ab2de29f` | e-mail withheld; banner prepended (fix pass 2026-10-08) |
| `docs/handoff/literature_state/join_ranking.py` | `ssn:HANDOFF/literature_state/join_ranking.py` | 4,319 | `cb8b7569a32c3766` | do-not-run header prepended (fix pass 2026-10-08) |
| `docs/handoff/literature_state/power.md` | `ssn:HANDOFF/literature_state/power.md` | 36,598 | `4dddfd135447b13c` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/literature_state/power_calc.json` | `ssn:HANDOFF/literature_state/power_calc.json` | 14,819 | `dd648e5cb58d11eb` |  |
| `docs/handoff/literature_state/power_calc.py` | `ssn:HANDOFF/literature_state/power_calc.py` | 8,151 | `20d6af37f5b3e8b1` |  |
| `docs/handoff/literature_state/ranking_joined.csv` | `ssn:HANDOFF/literature_state/ranking_joined.csv` | 23,589 | `649207a3f3f6cfaf` |  |
| `docs/handoff/literature_state/t3_ratios.py` | `ssn:HANDOFF/literature_state/t3_ratios.py` | 3,918 | `d1fb03625a1b167f` |  |
| `docs/handoff/literature_state/topic1_bibliography.md` | `ssn:HANDOFF/literature_state/topic1_bibliography.md` | 92,083 | `90b268c8f6eead56` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/literature_state/topic3_size_relative_to_studies.md` | `ssn:HANDOFF/literature_state/topic3_size_relative_to_studies.md` | 41,506 | `4bc9160da7cac295` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/t2_wilson_check.py` | `ssn:HANDOFF/working_notes/t2_wilson_check.py` | 905 | `8aada271a5d46a23` |  |
| `docs/handoff/working_notes/topic1_schwingnet_carm_results.md` | `ssn:HANDOFF/working_notes/topic1_schwingnet_carm_results.md` | 87,350 | `8d70ae5976fe0ec1` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md` | `ssn:HANDOFF/working_notes/topic2_scaling_samples_anomaly_power.md` | 97,413 | `5e875537890d859b` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/topic3_dataset_usage_leakage_rsna.md` | `ssn:HANDOFF/working_notes/topic3_dataset_usage_leakage_rsna.md` | 59,464 | `8bca1c0f312f1501` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/topic4_manuscripts.md` | `ssn:HANDOFF/working_notes/topic4_manuscripts.md` | 87,391 | `8142ee75ecc8958a` | faculty surname in a file name -> '[faculty-surname]_IRB.pdf' (fix pass 2026-10-08); banner prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/topic5_operating_here.md` | `ssn:HANDOFF/working_notes/topic5_operating_here.md` | 86,160 | `c314cbbfc74aa6b8` | name/username -> 'go2432 and the C&IT administrator'; banner prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | `ssn:HANDOFF/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | 96,339 | `c8e31814712ebc47` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/builders/build_context_export.py` | `ssn:HANDOFF/working_notes/builders/build_context_export.py` | 12,480 | `649bc9770ce666b6` | do-not-run header prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/builders/build_context_index.py` | `ssn:HANDOFF/working_notes/builders/build_context_index.py` | 7,545 | `d20959d6cc1ea5a6` |  |
| `docs/handoff/working_notes/builders/check_paths.py` | `ssn:HANDOFF/working_notes/builders/check_paths.py` | 9,628 | `e7c691972e60026d` | do-not-run header prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/builders/check_refs.py` | `ssn:HANDOFF/working_notes/builders/check_refs.py` | 1,974 | `5472758445cd02a0` |  |
| `docs/handoff/working_notes/builders/copy_context.py` | `ssn:HANDOFF/working_notes/builders/copy_context.py` | 5,168 | `0d42f71eae7ec363` | do-not-run header prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/builders/patch_helper.py` | `ssn:HANDOFF/working_notes/builders/patch_helper.py` | 1,613 | `a1fb03f1e651b600` | do-not-run header prepended (fix pass 2026-10-08) |
| `docs/handoff/working_notes/builders/refresh_context.py` | `ssn:HANDOFF/working_notes/builders/refresh_context.py` | 6,796 | `7811234389ab3e11` | do-not-run header prepended (fix pass 2026-10-08) |
| `docs/handoff/context_INDEX.md` | `ssn:HANDOFF/context/INDEX.md` | 25,948 | `8c0a96f86cfaca84` | banner prepended (fix pass 2026-10-08) |
| `docs/handoff/context_COPIED_AT.txt` | `ssn:HANDOFF/context/COPIED_AT.txt` | 7,282 | `10438c4abc5b87b9` | banner line prepended (fix pass 2026-10-08) |

### `memory/` (40 files, 101,718 bytes)

| copied to | from | bytes | sha | redaction |
|---|---|---:|---|---|
| `memory/acquisition-space-saturation.md` | `ssn:HANDOFF/context/acquisition-space-saturation.md` | 2,936 | `428d0781eeb1fae0` | status header prepended |
| `memory/deepfluoro-convention.md` | `ssn:HANDOFF/context/deepfluoro-convention.md` | 3,119 | `b250c96245f3ec8a` | status header prepended |
| `memory/device-sampling-audit.md` | `ssn:HANDOFF/context/device-sampling-audit.md` | 3,368 | `d8708f2a8d46f289` | status header prepended |
| `memory/drr-row-spacing-defect.md` | `ssn:HANDOFF/context/drr-row-spacing-defect.md` | 2,312 | `f27d014b0bca8381` | status header prepended |
| `memory/drr-to-fluoro-levers.md` | `ssn:HANDOFF/context/drr-to-fluoro-levers.md` | 3,196 | `40b585263f768e2b` | status header prepended |
| `memory/film-fluoro-boundary-not-transferable.md` | `ssn:HANDOFF/context/film-fluoro-boundary-not-transferable.md` | 1,657 | `6d01b06476acec5c` | status header prepended |
| `memory/fluorogen-synthetic.md` | `ssn:HANDOFF/context/fluorogen-synthetic.md` | 4,230 | `3811bb3192c8cc88` | status header prepended |
| `memory/k-devices-one-network.md` | `ssn:HANDOFF/context/k-devices-one-network.md` | 4,478 | `101129fd0eafe51a` | status header prepended |
| `memory/learned-formation-refuted-calibrate-instead.md` | `ssn:HANDOFF/context/learned-formation-refuted-calibrate-instead.md` | 19,027 | `3a034d98b4fd7bcb` | name/username -> "a DMC clinician's fluoroscopy [name withheld]"; name/username -> '[DMC clinician; name withheld]'; status header prepended; staff member and faculty member -> roles (fix pass 2026-10-08) |
| `memory/oblique-angles-and-sweep-vision.md` | `ssn:HANDOFF/context/oblique-angles-and-sweep-vision.md` | 2,552 | `e27bba2c32b38321` | status header prepended |
| `memory/physics-three-defects-measured.md` | `ssn:HANDOFF/context/physics-three-defects-measured.md` | 1,859 | `58be67ba3582e690` | status header prepended |
| `memory/polypose-decision.md` | `ssn:HANDOFF/context/polypose-decision.md` | 2,881 | `a1eeac4a1d94ff05` | status header prepended |
| `memory/polypose-generator-build.md` | `ssn:HANDOFF/context/polypose-generator-build.md` | 2,338 | `39518e526f5c6d6b` | status header prepended |
| `memory/pooled-vs-lodo-device-designs.md` | `ssn:HANDOFF/context/pooled-vs-lodo-device-designs.md` | 2,127 | `db772015c4a1787b` | status header prepended |
| `memory/sweep-physics-no-bone.md` | `ssn:HANDOFF/context/sweep-physics-no-bone.md` | 2,369 | `711849d22d3566ef` | status header prepended |
| `memory/synthetic-real-ratio-evidence.md` | `ssn:HANDOFF/context/synthetic-real-ratio-evidence.md` | 3,092 | `acda38ca2be764da` | status header prepended |
| `memory/ts-sacrum-excludes-s1.md` | `ssn:HANDOFF/context/ts-sacrum-excludes-s1.md` | 1,530 | `f169cf7581e18da5` | status header prepended |
| `memory/vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md` | `ssn:HANDOFF/context/vf813-drops-c1-t9-use-raw-verse-for-whole-spine.md` | 1,483 | `6dfd9d50ca8b5756` | status header prepended |
| `memory/bash-heredoc-backslashes.md` | `ssn:HANDOFF/context/bash-heredoc-backslashes.md` | 1,009 | `84165cce6eb68c95` | status header prepended |
| `memory/ct-volumes-are-pir-not-ras.md` | `ssn:HANDOFF/context/ct-volumes-are-pir-not-ras.md` | 2,001 | `fc948502fb4ab149` | status header prepended |
| `memory/data-directives-2026-09-23.md` | `ssn:HANDOFF/context/data-directives-2026-09-23.md` | 2,133 | `42fd20828c0a9441` | status header prepended |
| `memory/figure-captions-terse.md` | `ssn:HANDOFF/context/figure-captions-terse.md` | 1,277 | `170527ecc66f77e6` | status header prepended |
| `memory/fluorocap-repo-private.md` | `ssn:HANDOFF/context/fluorocap-repo-private.md` | 1,422 | `2c180d4433bc3d66` | status header prepended |
| `memory/grid-access.md` | `ssn:HANDOFF/context/grid-access.md` | 1,342 | `800a66caaa358be1` | status header prepended |
| `memory/grid-bash-4-2-quoting.md` | `ssn:HANDOFF/context/grid-bash-4-2-quoting.md` | 1,380 | `a7043d3e97d48fba` | status header prepended |
| `memory/grid-ceph-volume-oschome.md` | `ssn:HANDOFF/context/grid-ceph-volume-oschome.md` | 1,283 | `5e15222bc3fbf76c` | name/username -> 'the C&IT administrator created it'; status header prepended |
| `memory/grid-local-singularity-is-broken.md` | `ssn:HANDOFF/context/grid-local-singularity-is-broken.md` | 2,368 | `bbec055095bdf788` | status header prepended |
| `memory/key-patients-from-metadata-not-filenames.md` | `ssn:HANDOFF/context/key-patients-from-metadata-not-filenames.md` | 2,159 | `2a9147ddcb72199c` | status header prepended |
| `memory/label-scheme-v4-vs-ostk.md` | `ssn:HANDOFF/context/label-scheme-v4-vs-ostk.md` | 2,423 | `c979bf79dbbfd77f` | status header prepended |
| `memory/morphology-deformation-feasibility.md` | `ssn:HANDOFF/context/morphology-deformation-feasibility.md` | 2,267 | `f926837cc76fcf7a` | status header prepended |
| `memory/never-reorient-when-writing-labels.md` | `ssn:HANDOFF/context/never-reorient-when-writing-labels.md` | 1,892 | `0db5423e6957fa4c` | status header prepended |
| `memory/no-jobs-on-login-node.md` | `ssn:HANDOFF/context/no-jobs-on-login-node.md` | 2,148 | `72aac50bba75f126` | status header prepended |
| `memory/no-unexplained-subsets-fix-not-disclose.md` | `ssn:HANDOFF/context/no-unexplained-subsets-fix-not-disclose.md` | 2,097 | `80b1330323c629ce` | status header prepended |
| `memory/scratchpad-shadows-stdlib.md` | `ssn:HANDOFF/context/scratchpad-shadows-stdlib.md` | 1,364 | `20198fa83b6ee476` | status header prepended |
| `memory/submit-and-sleep-orchestration.md` | `ssn:HANDOFF/context/submit-and-sleep-orchestration.md` | 1,888 | `4470ef6ad18e2246` | status header prepended |
| `memory/user-affiliation-general-surgery.md` | `ssn:HANDOFF/context/user-affiliation-general-surgery.md` | 1,516 | `0cb5e3cc0cd0a773` | status header prepended |
| `memory/windows-junction-worktree-trap.md` | `ssn:HANDOFF/context/windows-junction-worktree-trap.md` | 1,490 | `2a9e3af0f49db5fc` | status header prepended; laptop paths -> prefixes (fix pass 2026-10-08) |
| `memory/writing-preferences.md` | `ssn:HANDOFF/context/writing-preferences.md` | 788 | `c2fad51d21a1def5` | status header prepended |
| `memory/wsl-for-network.md` | `ssn:HANDOFF/context/wsl-for-network.md` | 1,439 | `219c0a64367caf58` | status header prepended; laptop paths -> prefixes (fix pass 2026-10-08) |
| `memory/wsu-library-access-cutoff.md` | `ssn:HANDOFF/context/wsu-library-access-cutoff.md` | 1,478 | `8642e6f642d4fa4d` | e-mail withheld; status header prepended |

## 2. Valuable files NOT copied, with the reason

| source (laptop, 2026-10-08) | what it is | why not copied | where it lives instead |
|---|---|---|---|
| `sn:results/manifold/deep.npy` | the 2048-d ResNet-50 feature array behind `results/manifold/` (15,154 frames) | 124,141,696 bytes: over the 25 MB rule; `.npy` is excluded by extension; disposition ssn r67 `exclude` | regenerable by `tools/corpus_manifold.py` (spinesurg-ct-nnunet 097933a; grid job 40414107); `deep_index.csv` and `deep_info.json` (copied) index it |
| `ssn:docs/figures/fig_device_spread.png` | the spread figure | byte-identical to `ssn:docs/fig_device_spread.png` (md5 6afb13362198e2d84c2083d5ab7ad71f), copied once as `figures/fig_device_spread.png` | this folder |
| `ctsp:infobot/` (`images.zip` 288 MB, 2,404 files of 2019 pelvic DR + bone-DRR pairs; `infogan.pdf`) | paired DR/DRR images; origin not recorded | imaging data in a zip; 288 MB; untracked in the CTSpinoPelvic1K checkout; disposition ctsp r54 `reference` | the laptop folder only; no grid copy is recorded; whether it is worth keeping is for Greg (its origin is not recorded) |
| `Desktop/Panjabi_1976_JBJS_thoracic.pdf` (11 pages) | Panjabi, Brand, White 1976, J Bone Joint Surg Am 58-A:642, the thoracic load-displacement curves the PolyPose generator cites for thoracic ranges | third-party copyrighted scan; disposition desk r36 `reference`; library access for DMC residents ended 2026-06-30 | cite it; the ROM values it supports are transcribed with their source in `docs/polypose_segmental_rom.csv` and `results/polypose/SAMPLING_SPEC.md` (Wilke 2017 is the thoracic source there) |
| `ctsp:panjabi_1976.pdf` | a different Panjabi 1976 paper (J Biomech, flexibility and stiffness), untracked at the CTSpinoPelvic1K root | third-party copyrighted scan | cite it |
| `ssn:recept_out.json` (156 bytes, 2026-09-20) | eight numbers keyed `none|fix` x `ii|cmos|fpd|mix`: `none|ii` 0.0, `none|cmos` 0.45, `none|fpd` 0.4, `none|mix` 0.15, `fix|ii` 0.6, `fix|cmos` 0.65, `fix|fpd` 0.65, `fix|mix` 0.75 (receptor-type fractions); no document names it | disposition ssn r18 `reference`: purpose not recorded, so it is quoted here in full rather than carried as a file | the repository root at 097933a |
| `ctsp:2D-3D-GS.zip` (79 MB: CT .raw/.sta, Tomazevic MSc, MICCAI 2002 paper, 157 files) and `ctsp:2D-3D-GS_UG.pdf` | the Ljubljana 2D/3D registration gold-standard set behind the PIXIUM 4600 card and `tools/ljubljana_pairs.py` | over 25 MB and imaging data; the user guide is copied by project 01 (disposition ctsp rows) | `$RS/data/ljubljana` (0.31 GB) on the grid |
| `ctsp:PIG/*.zip` (CBCT and CT of the Goswami pig study, 43 to 48 MB each; `PIG_LEVELCHECK.pdf`) | third-party registration data and paper | data over 25 MB; third-party; disposition ctsp rows `reference` (project 01) | the laptop folder only |
| `ssn:tools/`, `ssn/slurm/`, `ssn:tools/polypose/` (about 90 + 28 + 127 files) | the renderers, cards, calibration, PolyPose and job scripts | every file is tracked at 097933a; disposition ssn r132, r133, r150 `reference` | `MANIFEST_CODE.md` |
| `ssn:tools/polypose/cine_render.py` | the flexion-extension cine reader | untracked on 2026-10-08 and not in any disposition copy row; `TODO.md` step 2 commits it | the laptop checkout only |
| `ssn:slurm/polypose_cine.sh` (7,237 B, 2026-09-26) | the job script of the flexion-extension cine: five stages (plan, warp, rgt, check) chained with `afterany` on the whole-spine VerSe CT `verse823`; refuses the cervical and whole regions until `rom_cine.json` is filled | untracked on 2026-10-08 and in no disposition copy row; code is referenced, not copied; `TODO.md` step 2 commits it | the laptop checkout only; `MANIFEST_CODE.md` sections 1 and 1.6 |
| `ssn:HANDOFF/GREG_ONLY/` (`PRIVATE_STATE.md`, `README.md`, `context/` with the five moved notes and the three full copies, `context_beethoven/`) | Greg's private state, credential locations, the unredacted notes | never copied into any project folder (PLAN.md section 2 rule 3 and 5) | the laptop checkout; referenced from project 01 and `../_plan/EXCLUDED.md` |
| `ssn:HANDOFF/context/` notes not on this folder's cut list (101 of 141) | other projects' notes | each lives in the folder of its family (`MEMORY.md` section 3) | the other project folders; the index is `docs/handoff/context_INDEX.md` |
| `ssn:results/physics/` (86 tracked files, 736 KB) | the physics line's result files behind `docs/PHYSICS_LINKING.md` and `docs/HANDOFF_PHYSICS.md` (`make physics` reproduces them) | disposition puts the physics results with project 01 (carm_detection; `PHYSICS_LINKING.md` is copied into both 01 and 08) | project 01; the repository at 097933a |
| `sn:results/coverage/`, `sn:results/power/`, `sn:results/arc/`, `sn:results/a1.json`, `a2.json`, `a6.json`, `sn:results/eval_gate/leaks/*.json`, `sn:figures/*.record.json` | the result files that STATUS.md cites for A6, A7, A10 to A14 | they are SchwingNet paper-1 results and belong to project 01 by disposition | project 01; the repository at 097933a |
| `ssn:docs/MODEL_CARD.md`, `DATASHEET.md`, `RSNAI_PLAN.md`, `RSNAI_CLAIMS.json`, `DATA_COMPLETENESS_AUDIT.md`, `PATIENT_IDENTITY_SPEC.md`, `NHANES_DOUBLE_INCLUSION_2026-09-22.md`, `SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`, `CONTINUANCE_2026-09-19.md`, `RESUME_2026-09-22_PM.md`, `FLUORO_DATASET_STRATEGY.md`, `CARM_DEPLOYMENT_EVIDENCE.md`, `SWEEP_TIME_EVIDENCE.md`, `GUIDED_ACQUISITION.md`, `SWEEP_PROTOCOL.md`, `COUNTING_EVIDENCE.md` | documents STATUS.md and the copied notes cite | disposition routes them to projects 01, 02 or 10 | those folders; the repository at 097933a |
| `ssn:data_platform/` (`DATA_MANIFEST.md` 939 KB, `MIGRATION_PLAN.md`, `LAYOUT.md`, `sources.json`, `plan/`, `dedup/`, `reacquire/`) | the data platform | project 10 owns it; the rows that bear on this folder are quoted in `MANIFEST_GRID.md` | project 10; the repository at 097933a |
| `ssn:docs/devices/` on the grid checkout (`surgio_b51_dr.json`, `varian_halcyon` under `$RS/data/or_ready/devices`) | the two grid-only cards | not on the laptop; nothing was written to or fetched from the grid in this build | `MANIFEST_GRID.md` section 2 |
| `Desktop/CNS2026_Schwing_NotAllSpines_public_v12.pptx` and the CNS decks | talks | project 03 by disposition | project 03 |
| any `.nii`, `.nii.gz`, `.npz`, `.npy`, `.pt`, `.h5`, `.zip` under the sources | imaging data and weights | the copy rules (never copied) | the grid (`MANIFEST_GRID.md`) |

## 3. Redactions applied on copy (by kind, never by value)

| copy | what was changed | rule |
|---|---|---|
| `memory/learned-formation-refuted-calibrate-instead.md` | two clinicians' names in the 2026-09-21 deliverables paragraph replaced by "[DMC clinician; name withheld]" and "a DMC clinician's fluoroscopy [name withheld]"; the handoff copy had already withheld a staff contact and a phone number | PLAN.md section 2 rule 5 (strike the DMC clinician); the task's rule on personal data |
| `memory/grid-ceph-volume-oschome.md` | the C&IT administrator's username replaced by the role | student usernames are not copied |
| `memory/wsu-library-access-cutoff.md` | a named library contact's e-mail replaced by "[e-mail withheld]" (the library's public phone numbers kept) | e-mail addresses are not copied |
| `docs/handoff/INFRASTRUCTURE.md` (section 2.1) and `docs/handoff/working_notes/topic5_operating_here.md` | the same administrator username replaced by the role | as above |
| `docs/handoff/LITERATURE_STATE.md` (23 addresses in section 2 A and C), `docs/handoff/RESEARCH_DIRECTIONS.md` (one, section 5.5), `docs/handoff/literature_state/dataset_landscape_by_task.md` (one), `docs/research_notes/spine synthesis prior art/ssm-verify-meng2020.md` (two) | corresponding-author and dataset-contact e-mail addresses replaced by "[e-mail withheld]"; the institution and the paper stay, so the request can still be addressed through the paper | researcher e-mail addresses are not copied |
| `memory/learned-formation-refuted-calibrate-instead.md` (fix pass 2026-10-08) | a staff member's full name (the WSU body-bequest contact) replaced by "the WSU body-bequest coordinator"; a faculty surname in "<surname>'s WSU eProtocol format", in the file name `<SURNAME>S_IRB.pdf` and in a scratchpad file name replaced by "a WSU faculty member's eProtocol format", `[faculty-surname]_IRB.pdf` and "a scratchpad text file"; the status header says so. The first copy left these two names in place; the verifier found them | personal names are not copied; roles stand in for them |
| `docs/handoff/working_notes/topic4_manuscripts.md` (one row, fix pass 2026-10-08) | the same faculty surname in the file name `ctsp/<SURNAME>S_IRB.pdf` replaced by `ctsp/[faculty-surname]_IRB.pdf` | as above |
| `memory/windows-junction-worktree-trap.md`, `memory/wsl-for-network.md` (fix pass 2026-10-08) | three laptop paths rewritten as prefixes: the Beethoven extension checkout as `Desktop/ashley/extension` (repository `OpenSpineConsortium/beethoven`), a worktree folder as "a worktree folder outside the checkout", the WSL mount of the CTSpinoPelvic1K checkout as `/mnt/c/<WSL mount of the ctsp: checkout>`; the status header of each says so | self-containment: no laptop path outside the copied handoff and this manifest |
| every file under `docs/handoff/` (23 `.md`, 1 `.txt`, 7 `.py`; fix pass 2026-10-08) | one banner prepended: an HTML comment on the `.md` copies and a first text line on `context_COPIED_AT.txt` naming the source file at 097933a and pointing to `CLAUDE.md` "Prefixes in the copied documents"; a four-line "LAPTOP-ONLY, DO NOT RUN" comment on the seven scripts that hard-code laptop roots (`literature_state/assemble.py`, `join_ranking.py`, `working_notes/builders/build_context_export.py`, `check_paths.py`, `copy_context.py`, `patch_helper.py`, `refresh_context.py`). The other `.py`, `.json` and `.csv` files under `docs/handoff/` carry no laptop path and are untouched | self-containment: 106 laptop-path hits in 26 of these files on 2026-10-08 are history |
| `docs/or_ready_audit_track_2026-09-22.json` (9 hits: five `path_local` scratchpad paths and four tool paths), `results/polypose/cohort_ctsp_release.json` (3 input paths), `results/polypose/cohort_sagittal.json` (2 input paths) | nothing: laptop spellings retained as data. These are result records and are not edited; the paths name `ctsp:morphometrics/{surgical_morphometrics,castellvi_grades}.csv`, `sn:results/polypose/inputs/`, `ssn:tools/or_audit_*.py`, `ssn:slurm/or_audit*.sh` and a session scratchpad that may be swept | result files are never edited; read them through `CLAUDE.md` "Prefixes in the copied documents" |
| every text copy | the role addresses `hpc@wayne.edu` and `IRBQuestions@wayne.edu` and the ssh target `go2432@grid.wayne.edu` were kept: they are institutional addresses the grid access and the hospital-testing plan need, not personal addresses | |

Not redacted and stated so: the copied handoff and research documents still name journal titles and expert panels
that contain the word "neurosurgeons" or "World Neurosurgery" (third-party citations, not an affiliation), and
`docs/handoff/MANUSCRIPTS.md` records which manuscript files carry the wrong affiliation (a defect record, not a
statement). The banned word appears in no copied file (grep of the built folder, 2026-10-08). The copied handoff
files keep their `ssn:`, `sn:`, `ctsp:` prefixes and, in `docs/handoff/README.md` section 0 and in their own path keys, the
laptop spellings of those prefixes (106 hits in 26 files under `docs/handoff/` on 2026-10-08); since the fix pass each
opens with a banner line that says so: read them through `CLAUDE.md` "Prefixes in the copied documents". The three
result JSONs that keep laptop paths as data are listed in the table above.

## 4. Counts

Files copied 293; bytes 36,351,975; skipped by rule 2 (section 2 rows 1 and 2); text copies redacted 9 on copy and 2 more in the fix pass of 2026-10-08 (the learned-formation note again, `topic4_manuscripts.md`); handoff copies with a banner or do-not-run header 31 of 43; memory notes with laptop paths rewritten 2; memory notes 40;
largest copied file `results/manifold/features.csv` 7,364,605 bytes; no file over 25 MB was copied; no symlink was followed;
nothing under a `.git`, an environment or a cache was read.


## Final pass of 2026-10-08 (after the critic's check of the whole tree)

Rows added by the final pass; the sections above are the first build and the verifier's fix pass as they were. Sources are laptop paths of 2026-10-08 (history, not dependencies). sha1 is the first 16 hex digits of the copy.

### Salvaged and copied: the nine planned scripts, the two untracked cine files, the SpineSurg-CT synthesis line

`../_plan/PLAN.md` section 3 ('08, Families absorbed') promised nine scripts in `code/`; the first build followed the disposition rows ssn r132, r133, r150 ('reference') and left `code/` with a README only. The plan wins (the critic's finding); the copies are below. The two untracked cine files (`tools/polypose/cine_render.py`, `slurm/polypose_cine.sh`) are laptop-only and were recorded in section 2 as not copied; they are now copied so that `TODO.md` step 2 has something to commit even if the laptop checkout is lost. The SpineSurg-CT augmentation line (March-April 2026) was in no inventory row: the loose `SpineSurg-CT/augmentation/metrics/` folder and the `src/augmentation`, `src/utils` scripts of the nested clone at 0051074 were never given a row (family tag `ctsp_dataset`, read from the dataset side only).

| destination | source (laptop, 2026-10-08) | bytes | sha1 | note |
|---|---|---:|---|---|
| `results/superseded/sacralization_synthesis_2026-04/augmentation_quality_report.csv` | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/augmentation/metrics/augmentation_quality_report.csv` | 1,488 | b28b99535ba8479a | laptop-only QC result (outside the nested clone); byte-identical |
| `results/superseded/sacralization_synthesis_2026-04/augmentation_quality_summary.txt` | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/augmentation/metrics/augmentation_quality_summary.txt` | 1,023 | b59edeb751096278 | laptop-only QC result (outside the nested clone); byte-identical |
| `code/spinesurg_ct_0051074/src/augmentation/sacralization_synthesis.py` | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/SpineSurg-CT/src/augmentation/sacralization_synthesis.py` | 22,908 | 7e75816032b55b52 | byte-identical to the tracked file at SpineSurg-CT 0051074 |
| `code/spinesurg_ct_0051074/src/utils/augmentation_qc.py` | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/SpineSurg-CT/src/utils/augmentation_qc.py` | 43,384 | 7fa48b87027e5eeb | byte-identical to the tracked file at SpineSurg-CT 0051074 |
| `code/spinesurg_ct_0051074/src/utils/pelvic_alignment_qc.py` | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/SpineSurg-CT/src/utils/pelvic_alignment_qc.py` | 28,049 | b1b29bb4710b10cf | byte-identical to the tracked file at SpineSurg-CT 0051074 |
| `code/spinesurg_ct_0051074/src/utils/pelvic_grid_panel.py` | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/SpineSurg-CT/src/utils/pelvic_grid_panel.py` | 29,067 | a24c304136eadea1 | byte-identical to the tracked file at SpineSurg-CT 0051074 |
| `code/spinesurg_ct_0051074/slurm/run_augmentation_qc.sh` | `C:/Users/grego/OneDrive/Desktop/SpineSurg-CT/SpineSurg-CT/slurm/run_augmentation_qc.sh` | 3,937 | 27325482da237c11 | byte-identical to the tracked file at SpineSurg-CT 0051074 |
| `code/ssn_097933a/tools/device_fit.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/device_fit.py` | 120,524 | c3b1f68108b13ae7 | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_097933a/tools/device_style.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/device_style.py` | 28,809 | 636f3283fcc1df34 | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_097933a/tools/device_spread_sweep.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/device_spread_sweep.py` | 11,447 | a0234e64a7a64be7 | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_097933a/tools/deepfluoro_calibrate.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/deepfluoro_calibrate.py` | 25,461 | b2cb685f3e301573 | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_097933a/tools/make_drr_dataset.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/make_drr_dataset.py` | 28,297 | f4295a7964ebbb7d | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_097933a/tools/render_physics_drr.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/render_physics_drr.py` | 18,934 | 2b483c2b2edd8101 | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_097933a/tools/polypose_sample.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/polypose_sample.py` | 89,612 | 760032ac9fd5b739 | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_097933a/tools/polypose_warp.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/polypose_warp.py` | 19,690 | a271c6446ddcf2be | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_097933a/tools/spine_project.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/spine_project.py` | 10,988 | 67b27d9f7ef2bbc2 | byte-identical to the tracked file at spinesurg-ct-nnunet 097933a |
| `code/ssn_untracked_2026-10-08/tools/polypose/cine_render.py` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/tools/polypose/cine_render.py` | 104,995 | 9b9e1c1beb7967bc | untracked in the working tree at 097933a; this is the only copy outside the laptop |
| `code/ssn_untracked_2026-10-08/slurm/polypose_cine.sh` | `C:/Users/grego/OneDrive/Desktop/spinesurg-ct-nnunet/slurm/polypose_cine.sh` | 7,237 | 4e88016c26e5f69c | untracked in the working tree at 097933a; this is the only copy outside the laptop |

No laptop path and no e-mail address in any text copy (regular-expression scan on copy). `code/README.md` describes the three groups.

### Ownership of files that were duplicated in 01

`docs/HANDOFF_PHYSICS.md`, `docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md`, `docs/PHYSICS_THREE_DEFECTS_MEASURED_2026-09-22.md` and `docs/SIMULATION_FIDELITY.md` are owned here; 01 held byte-identical copies outside PLAN.md rule 2d and removed them in the final pass, citing this folder. `results/manifold/overlap.json` is a shared copy of 01's `results/schwingnet/corpus_manifold/overlap.json` (owner 01; the tracked file at 097933a); kept here because the corpus manifold is this folder's topic.

### Redaction made the same in every folder

The one Hugging Face handle quoted beside a published co-author's name was withheld in some folders and kept in others for the same source line (the critic's finding). It now reads `(HF username withheld)` everywhere (one occurrence per file below); the person's name stays (a person, never renamed). Greg may restore it; it is his decision (PLAN.md section 5).

- `docs/handoff/RECIPES.md`
- `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md`

### Student names withheld (the same redaction 01 and 02 already carried)

The 14-author list of the dataset article (ten students), the two CNS abstract rows with student presenters, and (topic 6) the per-student username tally were still spelled out in the copies below; they now carry the placeholders used in 01 and 02. The two radiology residents and the published co-author stay (public co-authors of NeurIPS 3474 and the dataset article).

- `docs/handoff/MANUSCRIPTS.md`
- `docs/handoff/working_notes/topic4_manuscripts.md`
- `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md`

### Laptop paths rewritten to markers (self-containment)

The critic's tree-wide scan still found laptop spellings in copied files of this folder outside `MANIFEST_LOCAL.md`. They are now the markers the other folders use: `<laptop:Desktop>` for the Desktop root that held every repository checkout (`<laptop:Desktop>/spinesurg-ct-nnunet` = spinesurg-ct-nnunet at 097933a, `<laptop:Desktop>/CTSpinoPelvic1K-1` = CTSpinoPelvic1K at 7ddfe38, `<laptop:Desktop>/OpenSpineToolkit` = OpenSpineToolkit at cb43197, `<laptop:Desktop>/XRaySpinoPelvic1K` = XRSpinoPelvic1K at 4f22935), `<laptop:Temp scratchpad>` for the swept session scratchpad (nothing there is a dependency), `<laptop memory folder>` for the live memory notes (copied redacted into `memory/`), `<laptop vendor folder, never read>` and `<laptop home>`. The marker is a spelling of where the file came from, not a path to resolve; the repository and commit are the dependency. Scripts among these copies (`.py`, `.sh`) hard-coded laptop roots and did not run anywhere else before this change either; they are records of how a document was built.

| file | laptop spellings rewritten | left |
|---|---:|---:|
| `docs/handoff/CONTEXT_EXPORT.md` | 3 | 0 |
| `docs/handoff/INFRASTRUCTURE.md` | 4 | 0 |
| `docs/handoff/LITERATURE_STATE.md` | 5 | 0 |
| `docs/handoff/MANUSCRIPTS.md` | 4 | 0 |
| `docs/handoff/README.md` | 14 | 0 |
| `docs/handoff/RECIPES.md` | 4 | 0 |
| `docs/handoff/RESEARCH_DIRECTIONS.md` | 13 | 0 |
| `docs/handoff/RESULTS_CATALOG.md` | 8 | 0 |
| `docs/handoff/context_COPIED_AT.txt` | 1 | 0 |
| `docs/handoff/literature_state/assemble.py` | 3 | 0 |
| `docs/handoff/literature_state/dataset_landscape_by_task.md` | 5 | 0 |
| `docs/handoff/literature_state/join_ranking.py` | 3 | 0 |
| `docs/handoff/literature_state/power.md` | 5 | 0 |
| `docs/handoff/literature_state/topic1_bibliography.md` | 5 | 0 |
| `docs/handoff/literature_state/topic3_size_relative_to_studies.md` | 1 | 0 |
| `docs/handoff/working_notes/builders/build_context_export.py` | 7 | 0 |
| `docs/handoff/working_notes/builders/check_paths.py` | 13 | 0 |
| `docs/handoff/working_notes/builders/copy_context.py` | 6 | 0 |
| `docs/handoff/working_notes/builders/patch_helper.py` | 3 | 0 |
| `docs/handoff/working_notes/builders/refresh_context.py` | 2 | 0 |
| `docs/handoff/working_notes/topic1_schwingnet_carm_results.md` | 3 | 0 |
| `docs/handoff/working_notes/topic2_scaling_samples_anomaly_power.md` | 7 | 0 |
| `docs/handoff/working_notes/topic3_dataset_usage_leakage_rsna.md` | 3 | 0 |
| `docs/handoff/working_notes/topic4_manuscripts.md` | 11 | 0 |
| `docs/handoff/working_notes/topic5_operating_here.md` | 17 | 0 |
| `docs/handoff/working_notes/topic6_ctspinopelvic1k_and_toolkit.md` | 19 | 0 |
| `docs/or_ready_audit_track_2026-09-22.json` | 18 | 0 |
| `results/polypose/cohort_ctsp_release.json` | 6 | 0 |
| `results/polypose/cohort_sagittal.json` | 4 | 0 |

### Student presenters withheld in the CNS 2026 abstract table

The abstract table (section 12 of `MANUSCRIPTS.md` and its twin in topic 4) still named student presenters in four rows; each author cell now reads `[n student names withheld]` as 02's copy already did. Files: `docs/handoff/MANUSCRIPTS.md`, `docs/handoff/working_notes/topic4_manuscripts.md`.

## Redactions of 2026-10-12 (issue #67)

The values of private tag (0029,0016) in the Surgio-B51 header census of the C-ArmLSpine release are replaced by `[withheld]`; this section gives kinds and counts, never values. The history of main before this change still holds the values, and it stays: Greg chose on 2026-10-12 to keep the history of main as it is, with no rewrite (issue #71, option (a)). Where a table above gives one of these files' bytes or sha1, it is the file before this edit.

- `results/devices/census/surgio_b51__headers.json`: the six listed (0029,0016) values replaced by `[withheld]`, the header count beside each kept; the file still parses as JSON.
- `results/devices/census/surgio_b51__headers.md`: the four listed (0029,0016) values replaced by `[withheld]` and their count.
