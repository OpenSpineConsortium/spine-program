# NHANES II is in the level-model banks twice, split independently (found 2026-09-22)

## What is true

The context-crop banks are built by `tools/make_context_crops.py` from several `--drr` directories. The film
directory `~/films_drr` already holds the annotated NHANES II subset (source `nhanes`, 543 cases, `patient_id`
such as `nhanes_00160`, so a patient's cervical and lumbar films are grouped). The chains ALSO pass
`~/nhanes_drr`, which holds the same 543 films again (`NH_00160_c`, `NH_00160_l`; `source_file`
`C00160_cervical_masks_4.pkl`, the same Zenodo pickles), with no `source` field, so it becomes a second source
named `nhanes_drr`, grouped by name.

The split is drawn per source with one random stream. The two copies of one patient therefore land on the two
sides of the split independently.

| bank | NHANES val patients (films copy) | of those, other copy in TRAINING | render-dir copy val patients | of those, other copy in training |
|---|---:|---:|---:|---:|
| allspine_v6_fov96_ctx | 54 | 48 (89 %) | 54 | 48 |
| allspine_v7_fov96_ctx | 54 | 48 (89 %) | 54 | 48 |
| allspine_v2_fov96_ctx | deleted 2026-09-20; its build log (`logs/allspine_v2_bank_40275088.out`) shows both sources (nhanes 80 val, nhanes_drr 79 val cases), so the same construction applies |

Computed from each bank's `meta.json` `val_cases` (copied down and parsed locally).

## What it affects

- Every `real_film` pooled figure from `tools/head_mixed_length.py` on these banks: the pool is buu_full + csxa
  + nhanes + nhanes_drr (7,339 vertebrae), so NHANES is counted twice and is mostly leaked. Example, v2 seed 0,
  random window: pooled 99.02 %; nhanes 98.95 % (n 476), nhanes_drr 97.98 % (n 445).
- The encoder under the head (`model_night/runs/model_r18_ce.pt` for v2) was trained on the same split, so the
  leak reaches both networks.
- Unaffected: CSXA (one source, one group per image) and BUU-LSPINE (one source, grouped by `patient_id`,
  including its three duplicated "(1)" files); every C-ArmLSpine, COBRA, DeepFluoro and render result.

## What the manuscripts now say

`paper/rsnai/main_v2.tex` reports CSXA and BUU-LSPINE separately and states why NHANES is not reported. The
pooled claims were withdrawn from `docs/RSNAI_CLAIMS.json` (history entry 2026-09-22 13:10).

## Not done

- No bank was rebuilt. A clean bank needs either one NHANES directory, or a split drawn over patients across
  sources (a cross-source patient key: `nhanes_00160` and `NH_00160_*` are one person).
- Earlier memory and handoff notes quote pooled real-film numbers (for example "99.02 % shortcut-free"); they
  include the leaked NHANES rows and should be re-read as CSXA + BUU + (leaked) NHANES.
- CSXA's release does not give patient identity; one image is treated as one patient. If a patient contributed
  several images, the CSXA split could leak too; this was not tested.
