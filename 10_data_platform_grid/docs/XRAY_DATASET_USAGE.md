# X-ray datasets on the grid, and how each one is used

Computed by `tools/xray_dataset_usage.py`. Counts of films in a bank are DISTINCT FILMS, not crops,
and are taken from the bank's own case array rather than from any written record.

`in the shipped bank` is the level bank the reported model was trained on (allspine_v9, v8 before
the VerSe re-key). `films in any bank` is the largest count over every crop bank on the machine,
most of which are superseded or were never trained on -- the two columns are different questions.

| dataset | view | on disk | in the shipped bank | films in any bank | that bank | annotation |
|---|---|---:|---:|---:|---|---|
| CSXA cervical | lateral | 4,963 | 4,963 | 4,963 | allspine_fov96_ctx | per-vertebra, released with the dataset |
| BUU-LSPINE | AP + lateral | 7,204 | 3,603 | 3,603 | allspine_fov96_ctx | endplate lines, L1-L5 plus S1 |
| BUU Drive mirror | AP + lateral | missing | 0 | 0 | - | same as BUU-LSPINE |
| NHANES II | lateral | 17,073 | 543 | 15,746 | nhanesps_fov96_ctx | 543 films have landmarks; the rest have none |
| VinDr-SpineXR | AP + lateral | 10,466 | 0 | 7,625 | allspine_v7_fov96_ctx | lesion boxes, NOT per-vertebra levels; 10,466 images in 5,000 studies |
| AASCE / BoostNet | AP | 579 | 0 | 457 | aasce_fov96_ctx | 68 landmarks, 17 vertebrae T1-L5 |
| Mendeley 5jdfdgp762 | lateral | 714 | 0 | 0 | - | 4 corners per body, class-agnostic |
| IEEE DataPort lateral full-spine | lateral | 236 | 0 | 0 | - | none in the release |
| Spinal-AI2024 (machine generated) | AP | 20,001 | 0 | 0 | - | machine generated, 17 landmarks |
| AASCE test split | AP + lateral | 4,000 | 0 | 0 | - | report spreadsheet only |

## Converted label sets, and whether they reached a bank

A render directory holds films with per-vertebra level labels. A row where `films in a bank` is 0
is a label set that exists and is not being trained on, which is the cheapest gap to close.

| render directory | labelled films | films in a bank |
|---|---:|---:|
| `/wsu/home/go/go24/go2432/nhanes_drr` | 543 | 543 |
| `/wsu/home/go/go24/go2432/aasce_drr` | 457 | 457 |
| `/wsu/home/go/go24/go2432/mendeley_drr` | 584 | 584 |
| `/wsu/home/go/go24/go2432/spinalai_drr` | 8,358 | 0 |
| `/wsu/home/go/go24/go2432/films_drr` | 9,109 | 9,109 |
| `/wsu/home/go/go24/go2432/nhanes_pseudo` | 16,234 | 15,746 |
| `/wsu/home/go/go24/go2432/vindr_pseudo` | 10,274 | 7,625 |
| `/wsu/home/go/go24/go2432/lateral236_pseudo` | 236 | 212 |

## Crop banks

| bank | distinct films |
|---|---:|
| `allspine_v7_fov96_ctx` | 29,105 |
| `allspine_v7nofluoro_fov96_ctx` | 27,077 |
| `allspine_v6_fov96_ctx` | 19,095 |
| `allspine_v8_fov96_ctx` | 18,565 |
| `allspine_v9_fov96_ctx` | 18,565 |
| `nhanesps_fov96_ctx` | 15,746 |
| `allspine_fov96_ctx` | 14,395 |
| `films_all2_fov96_ctx` | 9,853 |
| `carm_cvmix1_fov96_ctx` | 9,641 |
| `carm_cvmix4_fov96_ctx` | 9,639 |
| `carm_cvmix2_fov96_ctx` | 9,633 |
| `carm_mix_fov96_ctx` | 9,631 |
| `carm_cvmix0_fov96_ctx` | 9,617 |
| `carm_cvmix3_fov96_ctx` | 9,615 |
| `carm_cvdaymix2_fov96_ctx` | 9,613 |
| `carm_cvdaymix1_fov96_ctx` | 9,603 |
| `carm_cvdaymix0_fov96_ctx` | 9,555 |
| `sd_fov96_ctx` | 9,443 |
| `vindrps_fov96_ctx` | 7,625 |
| `mv_bands` | 5,517 |
| `films_ann_fov96_ctx` | 5,506 |
| `obl2_fov96_ctx` | 5,500 |
| `extra_fov96_ctx` | 4,347 |
| `buu_fov96_ctx` | 3,603 |
| `fluorocap_fov96_ctx` | 2,385 |
| `m_fov96_ctx` | 1,175 |
| `m_mask22_scale_ctx` | 1,175 |
| `merged_ctx` | 1,175 |
| `exp3_ctx_fluoro` | 1,058 |
| `exp3_ctx_radiograph` | 1,058 |
| `verse_only_ctx_plus_nh` | 917 |
| `vindr_fov96_ctx` | 744 |
| `verse_ctx` | 676 |
| `mendeley_fov96_ctx` | 584 |
| `nhanes_ctx` | 543 |
| `nhanes_split_ctx` | 543 |
| `aasce_fov96_ctx` | 457 |
| `verse_only_ctx` | 374 |
| `carm_cv1_fov96_ctx` | 244 |
| `carm_cv4_fov96_ctx` | 242 |
| `carm_cv2_fov96_ctx` | 236 |
| `carm_fov96_ctx` | 234 |
| `carm_cv0_fov96_ctx` | 220 |
| `carm_cv3_fov96_ctx` | 218 |
| `carm_cvday2_fov96_ctx` | 216 |
| `lat236ps_fov96_ctx` | 212 |
| `carm_cvday1_fov96_ctx` | 206 |
| `carm_cvday0_fov96_ctx` | 158 |
