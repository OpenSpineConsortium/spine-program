# Checkpoint lineage: what every scored checkpoint, and everything it was initialised from, saw

Written by `tools/checkpoint_lineage.py` on sfx9 at 2026-09-23T19:53:07 (git 6e1cf8d), from `touched.json` in this directory. Nothing in this file is typed by hand.

**The rule.** An evaluation item is HELD OUT for a checkpoint only if its patient key (tools/patient_keys.key_any; a render inherits its source CT subject) is in neither the train nor the val/selection set of that checkpoint nor of any ancestor in its initialisation chain. Public ImageNet/COCO pretraining is the only exempt ancestor, and only when declared. A non-empty `unresolved` makes touched_keys a lower bound.

**Census.** 306 checkpoints: 304 named by a result or a launch script, the rest reached only as ancestors. Families: level_encoder 90, lstv_flag 5, missing 7, public_root 1, recurrent_head 64, ultralytics 100, unknown 39. **133** carry at least one unresolved link, so their touched set is a lower bound.

## Checkpoints named by a SchwingNet result or NUMBERS.md (75)

| checkpoint | family | initialised from (nearest first) | train keys | val keys | touched (chain) | unresolved |
|---|---|---|---:|---:|---:|---:|
| `~/FluoroCap/anchor_det_v1.pt` | ultralytics | - <- public:ultralytics/yolo11m.pt | 2144 | 546 | 2384 | 0 |
| `~/allspine_v8_fov96_ctx/runs/model_rung_1_aug2.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 9612 | 1784 | 11204 | 0 |
| `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/carm_cvmix0_fov96_ctx/runs/model_rung_1_ft_cv0_aug2.pt` | level_encoder | ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6986 | 23 | 7009 | 1 |
| `~/carm_cvmix1_fov96_ctx/runs/model_rung_1_ft_cv1_aug2.pt` | level_encoder | ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6994 | 27 | 7021 | 1 |
| `~/carm_cvmix2_fov96_ctx/runs/model_rung_1_ft_cv2_aug2.pt` | level_encoder | ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6981 | 36 | 7017 | 1 |
| `~/carm_cvmix3_fov96_ctx/runs/model_rung_1_ft_cv3_aug2.pt` | level_encoder | ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6984 | 24 | 7008 | 1 |
| `~/carm_cvmix4_fov96_ctx/runs/model_rung_1_ft_cv4_aug2.pt` | level_encoder | ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6985 | 35 | 7020 | 1 |
| `~/lstv_flag/models/lstv_flag_v2.pt` | lstv_flag | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 1070 | 0 | 1070 | 0 |
| `~/lstv_flag/models/tltv_flag_v2.pt` | lstv_flag | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 1078 | 0 | 1078 | 0 |
| `~/model_night/heads_carm/head_cv0.pt` | recurrent_head | ~/carm_cvmix0_fov96_ctx/runs/model_rung_1_ft_cv0_aug2.pt <- ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6986 | 23 | 7009 | 1 |
| `~/model_night/heads_carm/head_cv1.pt` | recurrent_head | ~/carm_cvmix1_fov96_ctx/runs/model_rung_1_ft_cv1_aug2.pt <- ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6994 | 27 | 7021 | 1 |
| `~/model_night/heads_carm/head_cv2.pt` | recurrent_head | ~/carm_cvmix2_fov96_ctx/runs/model_rung_1_ft_cv2_aug2.pt <- ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6981 | 36 | 7017 | 1 |
| `~/model_night/heads_carm/head_cv3.pt` | recurrent_head | ~/carm_cvmix3_fov96_ctx/runs/model_rung_1_ft_cv3_aug2.pt <- ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6984 | 24 | 7008 | 1 |
| `~/model_night/heads_carm/head_cv4.pt` | recurrent_head | ~/carm_cvmix4_fov96_ctx/runs/model_rung_1_ft_cv4_aug2.pt <- ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6985 | 35 | 7020 | 1 |
| `~/model_night/heads_mixed/head_allspine_v8_mixed_kmax4_seed0.pt` | recurrent_head | ~/allspine_v8_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9612 | 1784 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha0.3_seed0.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha0.3_seed1.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha0.3_seed2.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha0_seed0.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha0_seed1.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha0_seed2.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha1.0_seed0.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha1.0_seed1.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_alpha1.0_seed2.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed1.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed2.pt` | recurrent_head | ~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9592 | 1776 | 11204 | 0 |
| `~/model_night/runs/model_r18_ce.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `~/model_registry/e8376cfdff7c5fd6/hardware_det_v1.pt` | ultralytics | - <- public:ultralytics/yolo11m.pt | 857 | 214 | 1071 | 0 |
| `devcorpus/dc_A_held_cios_fusion` | ultralytics | - <- public:ultralytics/yolo11m.pt | 340 | 40 | 380 | 0 |
| `devcorpus/dc_A_held_cios_fusion_1dev_elekta_xvi` | ultralytics | - <- public:ultralytics/yolo11m.pt | 235 | 25 | 260 | 0 |
| `devcorpus/dc_A_held_cios_fusion_1dev_surgio_b51_dr` | ultralytics | - <- public:ultralytics/yolo11m.pt | 230 | 32 | 262 | 0 |
| `devcorpus/dc_A_held_cios_fusion_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 340 | 40 | 380 | 0 |
| `devcorpus/dc_A_held_elekta_xvi` | ultralytics | - <- public:ultralytics/yolo11m.pt | 234 | 33 | 267 | 0 |
| `devcorpus/dc_A_held_elekta_xvi_1dev_cios_fusion` | ultralytics | - <- public:ultralytics/yolo11m.pt | 129 | 18 | 147 | 0 |
| `devcorpus/dc_A_held_elekta_xvi_1dev_surgio_b51_dr` | ultralytics | - <- public:ultralytics/yolo11m.pt | 230 | 32 | 262 | 0 |
| `devcorpus/dc_A_held_elekta_xvi_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 234 | 33 | 267 | 0 |
| `devcorpus/dc_A_held_surgio_b51_dr` | ultralytics | - <- public:ultralytics/yolo11m.pt | 239 | 26 | 265 | 0 |
| `devcorpus/dc_A_held_surgio_b51_dr_1dev_cios_fusion` | ultralytics | - <- public:ultralytics/yolo11m.pt | 129 | 18 | 147 | 0 |
| `devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi` | ultralytics | - <- public:ultralytics/yolo11m.pt | 235 | 25 | 260 | 0 |
| `devcorpus/dc_A_held_surgio_b51_dr_1dev_elekta_xvi_eq238` | ultralytics | - <- public:ultralytics/yolo11m.pt | 135 | 25 | 160 | 0 |
| `devcorpus/dc_A_held_surgio_b51_dr_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 239 | 26 | 265 | 0 |
| `devcorpus/dc_B_held_cios_fusion` | ultralytics | - <- public:ultralytics/yolo11m.pt | 340 | 40 | 380 | 0 |
| `devcorpus/dc_B_held_cios_fusion_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 340 | 40 | 380 | 0 |
| `devcorpus/dc_B_held_elekta_xvi` | ultralytics | - <- public:ultralytics/yolo11m.pt | 234 | 33 | 267 | 0 |
| `devcorpus/dc_B_held_surgio_b51_dr_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 239 | 26 | 265 | 0 |
| `devcorpus/dc_P_pooled` | ultralytics | - <- public:ultralytics/yolo11m.pt | 344 | 41 | 385 | 0 |
| `lcurve/lc_cios_fusion_N0_s0` | ultralytics | devcorpus/dc_B_held_cios_fusion <- public:ultralytics/yolo11m.pt | 339 | 1 | 381 | 0 |
| `lcurve/lc_cios_fusion_N100_s0` | ultralytics | devcorpus/dc_B_held_cios_fusion <- public:ultralytics/yolo11m.pt | 342 | 1 | 384 | 0 |
| `lcurve/lc_cios_fusion_N100_s1` | ultralytics | devcorpus/dc_B_held_cios_fusion <- public:ultralytics/yolo11m.pt | 341 | 1 | 383 | 0 |
| `lcurve/lc_cios_fusion_N200_s0` | ultralytics | devcorpus/dc_B_held_cios_fusion <- public:ultralytics/yolo11m.pt | 343 | 1 | 385 | 0 |
| `lcurve/lc_cios_fusion_N200_s1` | ultralytics | devcorpus/dc_B_held_cios_fusion <- public:ultralytics/yolo11m.pt | 342 | 1 | 384 | 0 |
| `lcurve/lc_cios_fusion_N50_s0` | ultralytics | devcorpus/dc_B_held_cios_fusion <- public:ultralytics/yolo11m.pt | 340 | 1 | 382 | 0 |
| `lcurve/lc_elekta_xvi_N0_s0` | ultralytics | devcorpus/dc_B_held_elekta_xvi <- public:ultralytics/yolo11m.pt | 233 | 8 | 275 | 0 |
| `lcurve/lc_elekta_xvi_N100_s0` | ultralytics | devcorpus/dc_B_held_elekta_xvi <- public:ultralytics/yolo11m.pt | 237 | 8 | 279 | 0 |
| `lcurve/lc_elekta_xvi_N100_s1` | ultralytics | devcorpus/dc_B_held_elekta_xvi <- public:ultralytics/yolo11m.pt | 237 | 8 | 279 | 0 |
| `lcurve/lc_elekta_xvi_N200_s0` | ultralytics | devcorpus/dc_B_held_elekta_xvi <- public:ultralytics/yolo11m.pt | 241 | 8 | 283 | 0 |
| `lcurve/lc_elekta_xvi_N400_s0` | ultralytics | devcorpus/dc_B_held_elekta_xvi <- public:ultralytics/yolo11m.pt | 250 | 8 | 292 | 0 |
| `lcurve/lc_elekta_xvi_N400_s1` | ultralytics | devcorpus/dc_B_held_elekta_xvi <- public:ultralytics/yolo11m.pt | 250 | 8 | 292 | 0 |
| `lcurve/lc_elekta_xvi_N50_s0` | ultralytics | devcorpus/dc_B_held_elekta_xvi <- public:ultralytics/yolo11m.pt | 235 | 8 | 277 | 0 |
| `lcurve/lc_surgio_b51_dr_N0_s0` | ultralytics | devcorpus/dc_B_held_surgio_b51_dr_s1 <- public:ultralytics/yolo11m.pt | 239 | 14 | 279 | 0 |
| `lcurve/lc_surgio_b51_dr_N100_s0` | ultralytics | devcorpus/dc_B_held_surgio_b51_dr_s1 <- public:ultralytics/yolo11m.pt | 289 | 14 | 329 | 0 |
| `lcurve/lc_surgio_b51_dr_N100_s1` | ultralytics | devcorpus/dc_B_held_surgio_b51_dr_s1 <- public:ultralytics/yolo11m.pt | 289 | 14 | 329 | 0 |
| `lcurve/lc_surgio_b51_dr_N200_s0` | ultralytics | devcorpus/dc_B_held_surgio_b51_dr_s1 <- public:ultralytics/yolo11m.pt | 339 | 14 | 379 | 0 |
| `lcurve/lc_surgio_b51_dr_N200_s1` | ultralytics | devcorpus/dc_B_held_surgio_b51_dr_s1 <- public:ultralytics/yolo11m.pt | 339 | 14 | 379 | 0 |
| `lcurve/lc_surgio_b51_dr_N50_s0` | ultralytics | devcorpus/dc_B_held_surgio_b51_dr_s1 <- public:ultralytics/yolo11m.pt | 264 | 14 | 304 | 0 |
| `pose/anchor_none_v2_17-1882` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `realxray/rx_lodo_carmlspine_1024` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 123 | 28 | 199 | 0 |
| `realxray/rx_lodo_cobra_elekta_1024` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 126 | 29 | 203 | 0 |
| `realxray/rx_lodo_deepfluoro_1024` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 239 | 55 | 342 | 0 |
| `realxray/rx_only_carmlspine_1024` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 106 | 15 | 169 | 0 |
| `realxray/rx_only_carmlspine_multi_1024` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 105 | 15 | 168 | 0 |
| `realxray/rx_pooled_1024` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 220 | 24 | 292 | 0 |

## Checkpoints named only by a launch script, or reached as an ancestor (231)

| checkpoint | family | initialised from (nearest first) | train keys | val keys | touched (chain) | unresolved |
|---|---|---|---:|---:|---:|---:|
| `rs:/data/or_ready/controls/head_permute_true_seed0.pt` | missing | - | 0 | 0 | 0 | 1 |
| `~/FluoroCap/anchor_det_c2_v1.pt` | ultralytics | - <- public:ultralytics/yolo11m.pt | 2584 | 467 | 3046 | 0 |
| `~/FluoroCap/detect_v5z_epoch25_best.pt` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `~/FluoroCap/detect_v5z_final_best.pt` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `~/FluoroCap/detect_v6f_best.pt` | ultralytics | ~/FluoroCap/detect_v5z_epoch25_best.pt <- pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 10776 | 1258 | 12011 | 0 |
| `~/FluoroCap/hardware_det_v1.pt` | ultralytics | - <- public:ultralytics/yolo11m.pt | 857 | 214 | 1071 | 0 |
| `~/FluoroCap/hardware_det_v2.pt` | ultralytics | ~/FluoroCap/hardware_det_v1.pt <- public:ultralytics/yolo11m.pt | 1493 | 335 | 1828 | 0 |
| `~/FluoroCap/orientation_net.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/allspine_fov96_ctx/runs/model_rung_1_aug2.pt` | level_encoder | - | 8737 | 1678 | 10083 | 1 |
| `~/allspine_v2_fov96_ctx/runs/model_rung_1_aug2.pt` | missing | - | 0 | 0 | 0 | 1 |
| `~/carm_cvdaymix0_fov96_ctx/runs/model_rung_1_ft_cvday0_aug2.pt` | level_encoder | ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6966 | 12 | 6978 | 1 |
| `~/carm_cvdaymix1_fov96_ctx/runs/model_rung_1_ft_cvday1_aug2.pt` | level_encoder | ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6985 | 17 | 7002 | 1 |
| `~/carm_cvdaymix2_fov96_ctx/runs/model_rung_1_ft_cvday2_aug2.pt` | level_encoder | ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6992 | 15 | 7007 | 1 |
| `~/carm_fov96_ctx/runs/model_rung_1_ft_mix_aug2.pt` | missing | - | 0 | 0 | 0 | 1 |
| `~/carm_mix_fov96_ctx/runs/model_rung_1_ft_mix_aug2.pt` | level_encoder | - | 7002 | 14 | 7016 | 1 |
| `~/cut_v1/G_last.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/films_all2_fov96_ctx/runs/model_rung_0.pt` | level_encoder | - | 8074 | 1597 | 9671 | 1 |
| `~/films_all2_fov96_ctx/runs/model_rung_1_aug2.pt` | level_encoder | - | 8074 | 1597 | 9671 | 1 |
| `~/films_all3_fov96_ctx/runs/model_rung_0_aug2.pt` | missing | - | 0 | 0 | 0 | 1 |
| `~/films_all4_fov96_ctx/runs/model_rung_0_aug3.pt` | missing | - | 0 | 0 | 0 | 1 |
| `~/films_ann_fov48_ctx/runs/model_rung_2.pt` | missing | - | 0 | 0 | 0 | 1 |
| `~/films_ann_fov96_ctx/runs/model_rung_0.pt` | level_encoder | - | 3730 | 1597 | 5327 | 1 |
| `~/fluorogen/lora_film_v1/pytorch_lora_weights.safetensors` | unknown | - | 0 | 0 | 0 | 1 |
| `~/lstv_flag/models/lstv_flag_v1.pt` | lstv_flag | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 269 | 0 | 269 | 3 |
| `~/lstv_flag/models/sex_control_v1.pt` | lstv_flag | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 0 | 0 | 0 | 1 |
| `~/lstv_flag/models/tltv_flag_v1.pt` | lstv_flag | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 277 | 0 | 277 | 3 |
| `~/model_night/buu_baseline/v1` | ultralytics | - <- public:ultralytics/yolo11s.pt | 8850 | 1632 | 10482 | 0 |
| `~/model_night/heads/allspine_v2/head_k3.pt` | recurrent_head | ~/model_night/runs/model_r18_ce.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads/films_all2/head_k3.pt` | recurrent_head | ~/films_all2_fov96_ctx/runs/model_rung_1_aug2.pt | 8074 | 1597 | 9671 | 1 |
| `~/model_night/heads/r18_ce_v5/head_k3.pt` | recurrent_head | ~/model_night/runs/model_r18_ce_v5.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads/r18_corn_v5/head_k3.pt` | recurrent_head | ~/model_night/runs/model_r18_corn_v5.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_carm/head_cvday0.pt` | recurrent_head | ~/carm_cvdaymix0_fov96_ctx/runs/model_rung_1_ft_cvday0_aug2.pt <- ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6966 | 12 | 6978 | 1 |
| `~/model_night/heads_carm/head_cvday1.pt` | recurrent_head | ~/carm_cvdaymix1_fov96_ctx/runs/model_rung_1_ft_cvday1_aug2.pt <- ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6985 | 17 | 7002 | 1 |
| `~/model_night/heads_carm/head_cvday2.pt` | recurrent_head | ~/carm_cvdaymix2_fov96_ctx/runs/model_rung_1_ft_cvday2_aug2.pt <- ~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 6992 | 15 | 7007 | 1 |
| `~/model_night/heads_carm/head_mix.pt` | recurrent_head | ~/carm_mix_fov96_ctx/runs/model_rung_1_ft_mix_aug2.pt | 7002 | 14 | 7016 | 1 |
| `~/model_night/heads_mixed/head_abl_v5_all_abl.pt` | recurrent_head | ~/model_night/runs/model_abl_v5_all.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 18180 | 4405 | 22176 | 0 |
| `~/model_night/heads_mixed/head_abl_v5_minus_all_abl.pt` | recurrent_head | ~/model_night/runs/model_abl_v5_minus_all.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 9528 | 4405 | 13596 | 0 |
| `~/model_night/heads_mixed/head_abl_v5_minus_extras_abl.pt` | recurrent_head | ~/model_night/runs/model_abl_v5_minus_extras.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 17045 | 4405 | 21113 | 0 |
| `~/model_night/heads_mixed/head_abl_v5_minus_obl_abl.pt` | recurrent_head | ~/model_night/runs/model_abl_v5_minus_obl.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 17862 | 4405 | 21858 | 0 |
| `~/model_night/heads_mixed/head_abl_v5_minus_pseudo_abl.pt` | recurrent_head | ~/model_night/runs/model_abl_v5_minus_pseudo.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 10981 | 4405 | 14977 | 0 |
| `~/model_night/heads_mixed/head_allspine_v2_fov96_ctx_fixed_kmax4_seed0.pt` | recurrent_head | ~/model_night/runs/model_r18_ce.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_allspine_v2_fov96_ctx_mixed_kmax4_seed0.pt` | recurrent_head | ~/model_night/runs/model_r18_ce.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_allspine_v2_fov96_ctx_mixed_kmax4_seed1.pt` | recurrent_head | ~/model_night/runs/model_r18_ce.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_allspine_v2_fov96_ctx_mixed_kmax4_seed2.pt` | recurrent_head | ~/model_night/runs/model_r18_ce.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_allspine_v8_mixed_kmax4_seed1.pt` | recurrent_head | ~/allspine_v8_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9612 | 1784 | 11204 | 0 |
| `~/model_night/heads_mixed/head_allspine_v8_mixed_kmax4_seed2.pt` | recurrent_head | ~/allspine_v8_fov96_ctx/runs/model_rung_1_aug2.pt <- public:torchvision/resnet18/IMAGENET1K_V1 | 9612 | 1784 | 11204 | 0 |
| `~/model_night/heads_mixed/head_r18_ce_v2fm_v2fm.pt` | recurrent_head | ~/model_night/runs/model_r18_ce_v2fm.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_ce_v3_prod.pt` | recurrent_head | ~/model_night/runs/model_r18_ce_v3.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_ce_v4_prod.pt` | recurrent_head | ~/model_night/runs/model_r18_ce_v4.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_ce_v5_v5.pt` | recurrent_head | ~/model_night/runs/model_r18_ce_v5.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_ce_v5c_v5c.pt` | recurrent_head | ~/model_night/runs/model_r18_ce_v5c.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_ce_v6_v6.pt` | recurrent_head | ~/model_night/runs/model_r18_ce_v6.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 9576 | 1997 | 11204 | 0 |
| `~/model_night/heads_mixed/head_r18_ce_v7_v7.pt` | recurrent_head | ~/model_night/runs/model_r18_ce_v7.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 0 |
| `~/model_night/heads_mixed/head_r18_corn_prod.pt` | recurrent_head | ~/model_night/runs/model_r18_corn.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_corn_v3_prod.pt` | recurrent_head | ~/model_night/runs/model_r18_corn_v3.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_corn_v5_v5.pt` | recurrent_head | ~/model_night/runs/model_r18_corn_v5.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_corn_v5c_v5c.pt` | recurrent_head | ~/model_night/runs/model_r18_corn_v5c.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_corn_v6_v6.pt` | recurrent_head | ~/model_night/runs/model_r18_corn_v6.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 9576 | 1997 | 11204 | 0 |
| `~/model_night/heads_mixed/head_r18_la_cv0.pt` | recurrent_head | ~/model_night/runs/model_r18_la_cv0.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 1 |
| `~/model_night/heads_mixed/head_r18_la_cv1.pt` | recurrent_head | ~/model_night/runs/model_r18_la_cv1.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 1 |
| `~/model_night/heads_mixed/head_r18_la_cv2.pt` | recurrent_head | ~/model_night/runs/model_r18_la_cv2.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 1 |
| `~/model_night/heads_mixed/head_r18_la_v2_la_v2.pt` | recurrent_head | ~/model_night/runs/model_r18_la_v2.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_r18_la_v6_la_v6.pt` | recurrent_head | ~/model_night/runs/model_r18_la_v6.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 9576 | 1997 | 11204 | 0 |
| `~/model_night/heads_mixed/head_r18_la_v7_v7.pt` | recurrent_head | ~/model_night/runs/model_r18_la_v7.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 0 |
| `~/model_night/heads_mixed/head_scal_anchored_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_anchored.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_scal_crest_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_crest.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/heads_mixed/head_scal_pt_ft_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_pt_ft.pt <- ~/model_night/runs/model_scal_pt_render.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 7637 | 1873 | 11204 | 0 |
| `~/model_night/heads_mixed/head_scal_s000_r100_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_s000_r100.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 7637 | 1873 | 9414 | 0 |
| `~/model_night/heads_mixed/head_scal_s025_r100_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_s025_r100.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 8771 | 1873 | 10393 | 0 |
| `~/model_night/heads_mixed/head_scal_s050_r100_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_s050_r100.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 9258 | 1873 | 10834 | 0 |
| `~/model_night/heads_mixed/head_scal_s100_r025_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_s100_r025.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 4066 | 1873 | 5634 | 0 |
| `~/model_night/heads_mixed/head_scal_s100_r050_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_s100_r050.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 5986 | 1873 | 7530 | 0 |
| `~/model_night/heads_mixed/head_scal_s100_r100_scal.pt` | recurrent_head | ~/model_night/runs/model_scal_s100_r100.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 9700 | 1873 | 11204 | 0 |
| `~/model_night/refiners/full_masked_v2_17-1882.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_masked_v2_17-1905.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_masked_v2_18-0725.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_masked_v2_18-1109.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_masked_v2_18-2799.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_masked_v2_18-2800.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_unmasked_v2_17-1882.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_unmasked_v2_17-1905.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_unmasked_v2_18-0725.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_unmasked_v2_18-1109.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_unmasked_v2_18-2799.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/full_unmasked_v2_18-2800.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_masked_v2_17-1882.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_masked_v2_17-1905.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_masked_v2_18-0725.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_masked_v2_18-1109.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_masked_v2_18-2799.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_masked_v2_18-2800.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_unmasked_v2_17-1882.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_unmasked_v2_17-1905.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_unmasked_v2_18-0725.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_unmasked_v2_18-1109.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_unmasked_v2_18-2799.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/refiners/highpass_unmasked_v2_18-2800.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/roles/role_head_v3.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/roles/role_head_v6.pt` | unknown | - | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_abl_v5_all.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 18180 | 4405 | 22176 | 0 |
| `~/model_night/runs/model_abl_v5_minus_all.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 9528 | 4405 | 13596 | 0 |
| `~/model_night/runs/model_abl_v5_minus_extras.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 17045 | 4405 | 21113 | 0 |
| `~/model_night/runs/model_abl_v5_minus_obl.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 17862 | 4405 | 21858 | 0 |
| `~/model_night/runs/model_abl_v5_minus_pseudo.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 10981 | 4405 | 14977 | 0 |
| `~/model_night/runs/model_corpus_ft.pt` | level_encoder | ~/model_night/runs/model_r18_ce.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/runs/model_corpus_ft_frozen.pt` | level_encoder | ~/model_night/runs/model_r18_ce.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 2 |
| `~/model_night/runs/model_dinov3_frozen.pt` | level_encoder | - <- public:dinov3 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_dinov3_ft.pt` | level_encoder | - <- public:dinov3 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_exp3_fluoro.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 102 | 18 | 120 | 0 |
| `~/model_night/runs/model_exp3_radiograph.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 102 | 18 | 120 | 0 |
| `~/model_night/runs/model_r18_ce_8ep.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_ce_v2fm.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_ce_v3.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_ce_v4.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_ce_v5.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_ce_v5c.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_ce_v6.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 9576 | 1997 | 11204 | 0 |
| `~/model_night/runs/model_r18_ce_v7.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 0 |
| `~/model_night/runs/model_r18_ce_v7nofluoro.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 16175 | 3359 | 19165 | 0 |
| `~/model_night/runs/model_r18_corn.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_corn_v3.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_corn_v4.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_corn_v5.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_corn_v5c.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_corn_v6.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 9576 | 1997 | 11204 | 0 |
| `~/model_night/runs/model_r18_frozen.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_la_cv0.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 1 |
| `~/model_night/runs/model_r18_la_cv1.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 1 |
| `~/model_night/runs/model_r18_la_cv2.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 1 |
| `~/model_night/runs/model_r18_la_v2.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_la_v6.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 9576 | 1997 | 11204 | 0 |
| `~/model_night/runs/model_r18_la_v7.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 17857 | 3359 | 20782 | 0 |
| `~/model_night/runs/model_r18_la_v7nofluoro.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 16175 | 3359 | 19165 | 0 |
| `~/model_night/runs/model_r18_ordfocal.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_r18_ordfocal_v3.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_raddino_frozen.pt` | level_encoder | - <- public:raddino release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_raddino_ft.pt` | level_encoder | - <- public:raddino release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_scal_anchored.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_scal_crest.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 0 | 0 | 0 | 1 |
| `~/model_night/runs/model_scal_pt_ft.pt` | level_encoder | ~/model_night/runs/model_scal_pt_render.pt <- public:resnet18 release weights as train_level_backbone.py builds them | 7637 | 1873 | 11204 | 0 |
| `~/model_night/runs/model_scal_pt_render.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 2063 | 1873 | 3663 | 0 |
| `~/model_night/runs/model_scal_s000_r100.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 7637 | 1873 | 9414 | 0 |
| `~/model_night/runs/model_scal_s025_r100.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 8771 | 1873 | 10393 | 0 |
| `~/model_night/runs/model_scal_s050_r100.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 9258 | 1873 | 10834 | 0 |
| `~/model_night/runs/model_scal_s100_r025.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 4066 | 1873 | 5634 | 0 |
| `~/model_night/runs/model_scal_s100_r050.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 5986 | 1873 | 7530 | 0 |
| `~/model_night/runs/model_scal_s100_r100.pt` | level_encoder | - <- public:resnet18 release weights as train_level_backbone.py builds them | 9700 | 1873 | 11204 | 0 |
| `~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 0 | 0 | 0 | 1 |
| `~/runs/anchor_c2/v1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 2584 | 467 | 3046 | 0 |
| `detect/anchor_v1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 2144 | 546 | 2384 | 0 |
| `detect/hw_v1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 857 | 214 | 1071 | 0 |
| `detect/hw_v2` | ultralytics | ~/FluoroCap/hardware_det_v1.pt <- public:ultralytics/yolo11m.pt | 1493 | 335 | 1828 | 0 |
| `pose/anchor_none_r2` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_r2_17-1905` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_r2_18-0725` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_r2_18-1109` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_r2_18-2799` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_r2_18-2800` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_r2_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_r2_s2` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_17-1882_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_17-1882_s2` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_17-1905_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_17-1905_s2` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-0725_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-0725_s2` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-1109` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-1109_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-1109_s2` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-2799_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-2799_s2` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-2800_s1` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/anchor_none_v2_18-2800_s2` | ultralytics | - <- public:ultralytics/yolo11m.pt | 42 | 6 | 48 | 0 |
| `pose/detect_v6f` | ultralytics | ~/FluoroCap/detect_v5z_epoch25_best.pt <- pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 10776 | 1258 | 12011 | 0 |
| `pose/dr_s00f00` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `pose/dr_s00f05` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `pose/dr_s08f00` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `pose/dr_s08f05` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `pose/dr_s08f05x2` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 11293 | 1100 | 12393 | 0 |
| `pose/runs/pose/runs/detect_v3` | ultralytics | - <- public:ultralytics/yolo11m-pose.pt | 7973 | 996 | 8969 | 0 |
| `pose/v5f_p00` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `pose/v5f_p05` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `pose/v5f_p08` | ultralytics | pose/runs/pose/runs/detect_v3 <- public:ultralytics/yolo11m-pose.pt | 9633 | 1100 | 10733 | 0 |
| `pose` | missing | - | 0 | 0 | 0 | 1 |
| `realxray/rx_lodo_carmlspine_1024/weights/last.pt` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 123 | 28 | 199 | 0 |
| `realxray/rx_lodo_cobra_elekta_1024/weights/last.pt` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 126 | 29 | 203 | 0 |
| `realxray/rx_lodo_deepfluoro_1024/weights/last.pt` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 239 | 55 | 342 | 0 |
| `realxray/rx_only_carmlspine_1024/weights/last.pt` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 106 | 15 | 169 | 0 |
| `realxray/rx_only_carmlspine_multi_1024/weights/last.pt` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 105 | 15 | 168 | 0 |
| `realxray/rx_pooled_1024/weights/last.pt` | ultralytics | pose/anchor_none_v2_17-1882 <- public:ultralytics/yolo11m.pt | 220 | 24 | 292 | 0 |
| `realxray/rx_pooled_1024_init18` | ultralytics | pose/anchor_none_v2_18-1109 <- public:ultralytics/yolo11m.pt | 219 | 24 | 291 | 0 |
| `realxray/rx_pooled_1024_init18/weights/last.pt` | ultralytics | pose/anchor_none_v2_18-1109 <- public:ultralytics/yolo11m.pt | 219 | 24 | 291 | 0 |
| `wholespine/ws_mixed` | ultralytics | - <- public:ultralytics/yolo11m.pt | 10402 | 1441 | 11829 | 0 |
| `wholespine/ws_real` | ultralytics | - <- public:ultralytics/yolo11m.pt | 7815 | 968 | 8783 | 0 |
| `wholespine/ws_render` | ultralytics | - <- public:ultralytics/yolo11m.pt | 2587 | 473 | 3046 | 0 |
| `~/spine-detector/yolo11m.pt` | public_root | - <- public:ultralytics/yolo11m.pt | 0 | 0 | 0 | 0 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_0/checkpoint_best.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_0/checkpoint_final.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_1/checkpoint_best.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_1/checkpoint_final.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_2/checkpoint_best.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_2/checkpoint_final.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_3/checkpoint_best.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_3/checkpoint_final.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_4/checkpoint_best.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_4/checkpoint_final.pth` | unknown | - | 0 | 0 | 0 | 1 |
| `~/verse_ctx/runs/model_rung_0.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_0_convnext_tiny.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_0_convnext_tiny_lr1e4.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_0_resnet50.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_1.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_2.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_2_convnext_tiny.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_2_resnet50.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_3.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_4.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_6.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_8.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_ctx/runs/model_rung_full.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 530 | 133 | 657 | 0 |
| `~/verse_only_ctx/runs/model_rung_0.pt` | level_encoder | - <- public:torchvision/resnet18/IMAGENET1K_V1 | 283 | 73 | 355 | 0 |
| `~/verse_only_ctx/runs/model_rung_0_ep80.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_0_ep80_lr1e3.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_0_lr1e3.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_0_noaug.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_1.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_2.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_3.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_4.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_6.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_8.pt` | level_encoder | - | 283 | 73 | 355 | 1 |
| `~/verse_only_ctx/runs/model_rung_full.pt` | level_encoder | - | 283 | 73 | 355 | 1 |

## Cross-check: the recall-vs-angle subjects against the weights that scored them

The 17 subjects of `/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep/SET_INFO.json` keyed `ts:<subject>`, located in each scored checkpoint's own lists and in its ancestors'. SchwingNet/results/arc/ARC_CHECK.md item 4 found the same thing by a regex over file names (P/A/B: all 17 are val subjects; rx_lodo_carmlspine_1024: five in its parent's train, one in its parent's val); agreement is the check.

| arm | checkpoint | in own train | in own val | in an ancestor's train/val | held out under the rule |
|---|---|---:|---:|---:|---:|
| pooled | `devcorpus/dc_P_pooled` | 0 | 17 | 0  | 0 |
| lodoA | `devcorpus/dc_A_held_surgio_b51_dr` | 0 | 17 | 0  | 0 |
| lodoB | `devcorpus/dc_B_held_surgio_b51_dr_s1` | 0 | 17 | 0  | 0 |
| real_lodo | `realxray/rx_lodo_carmlspine_1024` | 0 | 0 | 6 (s0585, s0970, s1045, s1062, s1159, s1384) | 11 |

## Unresolved links, per checkpoint

Each row is a link the tool could not make from disk. It is carried into every descendant, so a gate that finds any of these on a checkpoint must treat its touched set as incomplete.

- `rs:/data/or_ready/controls/head_permute_true_seed0.pt`
    - **checkpoint file** -- not on disk; nothing it recorded can be read
- `~/FluoroCap/orientation_net.pt`
    - **checkpoint family** -- no reader for orientation_net.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/allspine_fov96_ctx/runs/model_rung_1_aug2.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/allspine_v2_fov96_ctx/runs/model_rung_1_aug2.pt`
    - **checkpoint file** -- not on disk; nothing it recorded can be read
- `~/carm_fov96_ctx/runs/model_rung_1_ft_mix_aug2.pt`
    - **checkpoint file** -- not on disk; nothing it recorded can be read
- `~/carm_mix_fov96_ctx/runs/model_rung_1_ft_mix_aug2.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/cut_v1/G_last.pt`
    - **checkpoint family** -- no reader for G_last.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/films_all2_fov96_ctx/runs/model_rung_0.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/films_all2_fov96_ctx/runs/model_rung_1_aug2.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/films_all3_fov96_ctx/runs/model_rung_0_aug2.pt`
    - **checkpoint file** -- not on disk; nothing it recorded can be read
- `~/films_all4_fov96_ctx/runs/model_rung_0_aug3.pt`
    - **checkpoint file** -- not on disk; nothing it recorded can be read
- `~/films_ann_fov48_ctx/runs/model_rung_2.pt`
    - **checkpoint file** -- not on disk; nothing it recorded can be read
- `~/films_ann_fov96_ctx/runs/model_rung_0.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/fluorogen/lora_film_v1/pytorch_lora_weights.safetensors`
    - **checkpoint family** -- no reader for pytorch_lora_weights.safetensors: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/lstv_flag/models/lstv_flag_v1.pt`
    - **folds csv rewritten after the model** -- /wsu/home/go/go24/go2432/lstv_flag/folds_LSTV_flag.csv is newer than lstv_flag_v1.pt
    - **folds csv vs the model's sidecar** -- /wsu/home/go/go24/go2432/lstv_flag/folds_LSTV_flag.csv lists 1070 patients; the sidecar says the model saw 801
    - **801 of 1070 train items could not be keyed** -- no rule in tools/patient_keys.py or tools/leak_check.RULES matches them; they are NOT treated as unique patients. Examples: 0001: no rule matches '0001' (no cohort recorded for this case); 0003: no rule matches '0003' (no cohort recorded for this case); 0004: no rule matches '0004' (no cohort recorded for this case); 0005: no rule matches '0005' (no cohort recorded for this case)
- `~/lstv_flag/models/sex_control_v1.pt`
    - **training patients** -- no folds_SEX_CONTROL_flag.csv beside the run's --out ['/wsu/home/go/go24/go2432/lstv_flag']; the final model trains on every patient listed there
- `~/lstv_flag/models/tltv_flag_v1.pt`
    - **folds csv rewritten after the model** -- /wsu/home/go/go24/go2432/lstv_flag/folds_TLTV_flag.csv is newer than tltv_flag_v1.pt
    - **folds csv vs the model's sidecar** -- /wsu/home/go/go24/go2432/lstv_flag/folds_TLTV_flag.csv lists 1078 patients; the sidecar says the model saw 801
    - **801 of 1078 train items could not be keyed** -- no rule in tools/patient_keys.py or tools/leak_check.RULES matches them; they are NOT treated as unique patients. Examples: 0001: no rule matches '0001' (no cohort recorded for this case); 0003: no rule matches '0003' (no cohort recorded for this case); 0004: no rule matches '0004' (no cohort recorded for this case); 0005: no rule matches '0005' (no cohort recorded for this case)
- `~/model_night/heads/allspine_v2/head_k3.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/heads/r18_ce_v5/head_k3.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads/r18_corn_v5/head_k3.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_allspine_v2_fov96_ctx_fixed_kmax4_seed0.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/heads_mixed/head_allspine_v2_fov96_ctx_mixed_kmax4_seed0.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/heads_mixed/head_allspine_v2_fov96_ctx_mixed_kmax4_seed1.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/heads_mixed/head_allspine_v2_fov96_ctx_mixed_kmax4_seed2.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/heads_mixed/head_r18_ce_v2fm_v2fm.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2fm_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_r18_ce_v3_prod.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v3_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_r18_ce_v4_prod.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v4_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_r18_ce_v5_v5.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_r18_ce_v5c_v5c.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5c_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_r18_corn_prod.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/heads_mixed/head_r18_corn_v3_prod.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v3_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_r18_corn_v5_v5.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_r18_corn_v5c_v5c.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5c_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_r18_la_v2_la_v2.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/heads_mixed/head_scal_anchored_scal.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2anchored_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/heads_mixed/head_scal_crest_scal.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2crest_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/refiners/full_masked_v2_17-1882.pt`
    - **checkpoint family** -- no reader for full_masked_v2_17-1882.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_masked_v2_17-1905.pt`
    - **checkpoint family** -- no reader for full_masked_v2_17-1905.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_masked_v2_18-0725.pt`
    - **checkpoint family** -- no reader for full_masked_v2_18-0725.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_masked_v2_18-1109.pt`
    - **checkpoint family** -- no reader for full_masked_v2_18-1109.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_masked_v2_18-2799.pt`
    - **checkpoint family** -- no reader for full_masked_v2_18-2799.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_masked_v2_18-2800.pt`
    - **checkpoint family** -- no reader for full_masked_v2_18-2800.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_unmasked_v2_17-1882.pt`
    - **checkpoint family** -- no reader for full_unmasked_v2_17-1882.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_unmasked_v2_17-1905.pt`
    - **checkpoint family** -- no reader for full_unmasked_v2_17-1905.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_unmasked_v2_18-0725.pt`
    - **checkpoint family** -- no reader for full_unmasked_v2_18-0725.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_unmasked_v2_18-1109.pt`
    - **checkpoint family** -- no reader for full_unmasked_v2_18-1109.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_unmasked_v2_18-2799.pt`
    - **checkpoint family** -- no reader for full_unmasked_v2_18-2799.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/full_unmasked_v2_18-2800.pt`
    - **checkpoint family** -- no reader for full_unmasked_v2_18-2800.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_masked_v2_17-1882.pt`
    - **checkpoint family** -- no reader for highpass_masked_v2_17-1882.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_masked_v2_17-1905.pt`
    - **checkpoint family** -- no reader for highpass_masked_v2_17-1905.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_masked_v2_18-0725.pt`
    - **checkpoint family** -- no reader for highpass_masked_v2_18-0725.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_masked_v2_18-1109.pt`
    - **checkpoint family** -- no reader for highpass_masked_v2_18-1109.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_masked_v2_18-2799.pt`
    - **checkpoint family** -- no reader for highpass_masked_v2_18-2799.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_masked_v2_18-2800.pt`
    - **checkpoint family** -- no reader for highpass_masked_v2_18-2800.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_unmasked_v2_17-1882.pt`
    - **checkpoint family** -- no reader for highpass_unmasked_v2_17-1882.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_unmasked_v2_17-1905.pt`
    - **checkpoint family** -- no reader for highpass_unmasked_v2_17-1905.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_unmasked_v2_18-0725.pt`
    - **checkpoint family** -- no reader for highpass_unmasked_v2_18-0725.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_unmasked_v2_18-1109.pt`
    - **checkpoint family** -- no reader for highpass_unmasked_v2_18-1109.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_unmasked_v2_18-2799.pt`
    - **checkpoint family** -- no reader for highpass_unmasked_v2_18-2799.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/refiners/highpass_unmasked_v2_18-2800.pt`
    - **checkpoint family** -- no reader for highpass_unmasked_v2_18-2800.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/roles/role_head_v3.pt`
    - **checkpoint family** -- no reader for role_head_v3.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/roles/role_head_v6.pt`
    - **checkpoint family** -- no reader for role_head_v6.pt: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/model_night/runs/model_corpus_ft.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/model_night/runs/result_corpus_ft.json names no bank
- `~/model_night/runs/model_corpus_ft_frozen.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/model_night/runs/result_corpus_ft_frozen.json names no bank
- `~/model_night/runs/model_dinov3_frozen.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_dinov3_ft.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_r18_ce.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_r18_ce_8ep.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_r18_ce_v2fm.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2fm_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_ce_v3.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v3_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_ce_v4.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v4_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_ce_v5.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_ce_v5c.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5c_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_corn.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_r18_corn_v3.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v3_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_corn_v4.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v4_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_corn_v5.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_corn_v5c.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v5c_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_r18_frozen.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_r18_la_cv0.pt`
    - **bank split vs the run's own record** -- result_r18_la_cv0.json recorded n_train 136098 / n_val 28063; the bank now holds 138838 / 25323 (a rebuilt bank, or a --fold file that moved cases to val and is not recorded)
- `~/model_night/runs/model_r18_la_cv1.pt`
    - **bank split vs the run's own record** -- result_r18_la_cv1.json recorded n_train 135549 / n_val 28612; the bank now holds 138838 / 25323 (a rebuilt bank, or a --fold file that moved cases to val and is not recorded)
- `~/model_night/runs/model_r18_la_cv2.pt`
    - **bank split vs the run's own record** -- result_r18_la_cv2.json recorded n_train 135389 / n_val 28772; the bank now holds 138838 / 25323 (a rebuilt bank, or a --fold file that moved cases to val and is not recorded)
- `~/model_night/runs/model_r18_la_v2.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_r18_ordfocal.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_r18_ordfocal_v3.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v3_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_raddino_frozen.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_raddino_ft.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `~/model_night/runs/model_scal_anchored.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2anchored_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_night/runs/model_scal_crest.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2crest_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. No make_context_crops.py launch line in slurm/*.sh writes this bank, so nothing bounds what it held.
- `~/model_registry/00e84a90afa7ec52/model_rung_1_aug2.pt`
    - **training bank** -- /wsu/home/go/go24/go2432/allspine_v2_fov96_ctx is not on disk (deleted or never here); what this model trained on cannot be read. Its build lines (/wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/allspine_v2_chain.sh:17, /wsu/home/go/go24/go2432/spinesurg-ct-nnunet/slurm/reproduce_all.sh:131) drew it from 6 roots, which key today to 11205 patients in buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355; roots changed after the fit (cases may have left them): ['/wsu/home/go/go24/go2432/ctsp_drr', '/wsu/home/go/go24/go2432/physics_drr', '/wsu/home/go/go24/go2432/verse_drr']. That upper bound is NOT complete, for the reasons listed.
- `pose`
    - **checkpoint file** -- not on disk; nothing it recorded can be read
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_0/checkpoint_best.pth`
    - **checkpoint family** -- no reader for checkpoint_best.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_0/checkpoint_final.pth`
    - **checkpoint family** -- no reader for checkpoint_final.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_1/checkpoint_best.pth`
    - **checkpoint family** -- no reader for checkpoint_best.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_1/checkpoint_final.pth`
    - **checkpoint family** -- no reader for checkpoint_final.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_2/checkpoint_best.pth`
    - **checkpoint family** -- no reader for checkpoint_best.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_2/checkpoint_final.pth`
    - **checkpoint family** -- no reader for checkpoint_final.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_3/checkpoint_best.pth`
    - **checkpoint family** -- no reader for checkpoint_best.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_3/checkpoint_final.pth`
    - **checkpoint family** -- no reader for checkpoint_final.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_4/checkpoint_best.pth`
    - **checkpoint family** -- no reader for checkpoint_best.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/spinesurg-ct-nnunet/nnunet/results/Dataset802_SpineSurgCTFull/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_4/checkpoint_final.pth`
    - **checkpoint family** -- no reader for checkpoint_final.pth: not an Ultralytics checkpoint, no .arch.json or .flag.json sidecar, not a registered level model; what it trained on is not recorded anywhere this tool knows
- `~/verse_only_ctx/runs/model_rung_0_ep80.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_0_ep80_lr1e3.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_0_lr1e3.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_0_noaug.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_1.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_2.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_3.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_4.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_6.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_8.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere
- `~/verse_only_ctx/runs/model_rung_full.pt`
    - **initialisation** -- train_level_classifier.py did not record --init before 2026-09-23 and no slurm/*.sh line writes this exact file, so what it was initialised from is not recorded anywhere

## Names no keying rule recognises, by family

Every unkeyed train/val item across all checkpoints, its digits collapsed to `#`. None of these is counted as a patient; each is an unresolved row on the checkpoints that read it.

| name family | items | checkpoints | e.g. |
|---|---:|---:|---|
| `#` | 1602 | 2 | `~/lstv_flag/models/lstv_flag_v1.pt` |

## Deleted banks: what their build lines say they could have held

A bank a checkpoint trained on that is no longer on disk leaves its split unreadable. Its build launch line (make_context_crops.py --drr ... --dst <bank>) still names the roots it drew from; the patients those roots hold today bound the bank from above, unless a root changed after the fit. The rows stay unresolved; bounds.json has the keys.

| bank | built by | roots | patients (corpora) | unkeyed | roots gone |
|---|---|---|---|---:|---|
| `~/allspine_v2_fov96_ctx` | allspine_v2_chain.sh:17, reproduce_all.sh:131 | ~/ctsp_drr, ~/films_drr, ~/nhanes_drr, ~/physics_drr, ~/physics_rare, ~/verse_drr | 11205 (buu 3600, csxa 4963, ctsp 802, nhanes 364, ts 1121, verse 355) | 0 | - |
| `~/allspine_v2anchored_fov96_ctx` | **none found** |  | 0 () | 0 | - |
| `~/allspine_v2crest_fov96_ctx` | **none found** |  | 0 () | 0 | - |
| `~/allspine_v2fm_fov96_ctx` | **none found** |  | 0 () | 0 | - |
| `~/allspine_v3_fov96_ctx` | **none found** |  | 0 () | 0 | - |
| `~/allspine_v4_fov96_ctx` | **none found** |  | 0 () | 0 | - |
| `~/allspine_v5_fov96_ctx` | **none found** |  | 0 () | 0 | - |
| `~/allspine_v5c_fov96_ctx` | **none found** |  | 0 () | 0 | - |

## Implant builds declared by launch scripts

An implant render is keyed to its source CT through make_implant_ct's hardware record; where a build's records are gone, through the one declared build whose case-id format its name fits.

- `ctsp` -> `~/implant_ct` (fluorocap_v2.sh:39); hardware records **not on disk**
- `verse` -> `~/implant_verse` (fluorocap_v2.sh:40); hardware records on disk
- `totalseg` -> `~/implant_ts` (fluorocap_v2.sh:41); hardware records on disk

## Declared public roots (the only exempt ancestors)

- public:dinov3 release weights as train_level_backbone.py builds them (fine-tuned: patch-embedding conv rebuilt for 2 channels, RGB averaged into channel 0, marker filter initialised at zero; crops resized 320 -> 512 px inside the model)
- public:dinov3 release weights as train_level_backbone.py builds them (frozen: encoder untouched, image replicated to 3 channels at 512 px; marker enters as marker-weighted pooling of the patch-token grid, concatenated with CLS and mean)
- public:raddino release weights as train_level_backbone.py builds them (fine-tuned: patch-embedding conv rebuilt for 2 channels, RGB averaged into channel 0, marker filter initialised at zero; crops resized 320 -> 518 px inside the model)
- public:raddino release weights as train_level_backbone.py builds them (frozen: encoder untouched, image replicated to 3 channels at 518 px; marker enters as marker-weighted pooling of the patch-token grid, concatenated with CLS and mean)
- public:resnet18 release weights as train_level_backbone.py builds them (fine-tuned: conv1 rebuilt for 2 channels, RGB averaged into channel 0, marker filter initialised at zero)
- public:resnet18 release weights as train_level_backbone.py builds them (frozen: encoder untouched at 3-channel ImageNet stem; marker enters as marker-weighted pooling of the conv feature map)
- public:torchvision/resnet18/IMAGENET1K_V1 (used when cached on the node; random init otherwise)
- public:ultralytics/yolo11m-pose.pt (COCO release; verified at /wsu/home/go/go24/go2432/spine-detector/yolo11m-pose.pt: train_args.data = '/ultralytics/ultralytics/cfg/datasets/coco-pose.yaml')
- public:ultralytics/yolo11m.pt (COCO release; verified at /wsu/home/go/go24/go2432/spine-detector/yolo11m.pt: train_args.data = '/ultralytics/ultralytics/cfg/datasets/coco.yaml')
- public:ultralytics/yolo11m.pt (the file itself; train_args.data = '/ultralytics/ultralytics/cfg/datasets/coco.yaml')
- public:ultralytics/yolo11s.pt (COCO release; file not located; declared by its Ultralytics release name)

## What the seed could not turn into a file

Launch-script paths with a variable the script does not set (an array index, a loop variable, an argument):
- matches nothing on disk: `/wsu/home/go/go24/go2432/allspine_v2_fov96_ctx/runs/model_rung_1*.pt` at slurm/allspine_v2_chain.sh:27
- matches nothing on disk: `/wsu/home/go/go24/go2432/allspine_v2_fov96_ctx/runs/model_rung_1*.pt` at slurm/allspine_v2_chain.sh:28
- matches nothing on disk: `/wsu/home/go/go24/go2432/allspine_v2_fov96_ctx/runs/model_rung_1*.pt` at slurm/allspine_v2_chain.sh:32
- matches nothing on disk: `/wsu/home/go/go24/go2432/allspine_v2_fov96_ctx/runs/model_rung_1*.pt` at slurm/allspine_v2_chain.sh:35
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvdaymix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cvday{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_day_v9.sh:34
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvdaymix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cvday{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_day_v9.sh:35
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvdaymix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cvday{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_day_v9.sh:37
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvdaymix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cvday{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_day_v9.sh:37
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvdaymix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cvday{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_day_v9.sh:38
- matches nothing on disk: `/wsu/home/go/go24/go2432/model_night/heads_carm/head_cvday{SLURM_ARRAY_TASK_ID}_v9.pt` at slurm/carmlspine_cv_day_v9.sh:39
- matches nothing on disk: `/wsu/home/go/go24/go2432/model_night/heads_carm/head_cvday{SLURM_ARRAY_TASK_ID}_v9.pt` at slurm/carmlspine_cv_day_v9.sh:40
- matches nothing on disk: `/wsu/home/go/go24/go2432/model_night/heads_carm/head_cvday{SLURM_ARRAY_TASK_ID}_v9.pt` at slurm/carmlspine_cv_day_v9.sh:40
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvdaymix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cvday{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_day_v9.sh:44
- matches nothing on disk: `/wsu/home/go/go24/go2432/model_night/heads_carm/head_cvday{SLURM_ARRAY_TASK_ID}_v9.pt` at slurm/carmlspine_cv_day_v9.sh:44
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvmix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cv{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_v9.sh:35
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvmix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cv{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_v9.sh:36
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvmix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cv{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_v9.sh:38
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvmix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cv{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_v9.sh:38
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvmix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cv{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_v9.sh:39
- matches nothing on disk: `/wsu/home/go/go24/go2432/model_night/heads_carm/head_cv{SLURM_ARRAY_TASK_ID}_v9.pt` at slurm/carmlspine_cv_v9.sh:40
- matches nothing on disk: `/wsu/home/go/go24/go2432/model_night/heads_carm/head_cv{SLURM_ARRAY_TASK_ID}_v9.pt` at slurm/carmlspine_cv_v9.sh:41
- matches nothing on disk: `/wsu/home/go/go24/go2432/model_night/heads_carm/head_cv{SLURM_ARRAY_TASK_ID}_v9.pt` at slurm/carmlspine_cv_v9.sh:41
- matches nothing on disk: `/wsu/home/go/go24/go2432/carm_cvmix{SLURM_ARRAY_TASK_ID}_v9_fov96_ctx/runs/model_rung_1_ft_cv{SLURM_ARRAY_TASK_ID}_v9_aug2.pt` at slurm/carmlspine_cv_v9.sh:45
- matches nothing on disk: `/wsu/home/go/go24/go2432/model_night/heads_carm/head_cv{SLURM_ARRAY_TASK_ID}_v9.pt` at slurm/carmlspine_cv_v9.sh:45
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/*/fold_*/checkpoint_*.pth` at slurm/convert_hf_to_nnet.sh:239
- matches nothing on disk: `{CTX}/runs/model_rung_{r}.pt` at slurm/ctx_arm_evalnh.sh:33
- matches nothing on disk: `{CTX}/runs/model_rung_{r}.pt` at slurm/ctx_arm_evalnh.sh:34
- matches nothing on disk: `{CTX}/runs/model_rung_{r}.pt` at slurm/ctx_arm_evalnh.sh:36
- matches nothing on disk: `{FILMS}/runs/model_rung_1_aug2.pt` at slurm/cut_drr2fluoro.sh:36
- matches nothing on disk: `{ALL}/runs/model_rung_1_aug2.pt` at slurm/cut_drr2fluoro.sh:37
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgLSTVOneShot/nnUNetTrainerWandB_500ep_LSTVOversample__{PLANS}__3d_fullres/fold_{FOLD__set_FOLD}/checkpoint_best.pth` at slurm/eval_fold_checkpoint.sh:54
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgLSTVOneShot/nnUNetTrainerWandB_500ep_LSTVOversample__{PLANS}__3d_fullres/fold_{FOLD__set_FOLD}/checkpoint_best.pth` at slurm/eval_fold_checkpoint.sh:55
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgLSTVOneShot/nnUNetTrainerWandB_500ep_LSTVOversample__{PLANS}__3d_fullres/fold_{FOLD__set_FOLD}/checkpoint_best.pth` at slurm/eval_fold_checkpoint.sh:55
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgLSTVOneShot/nnUNetTrainerWandB_500ep_LSTVOversample__{PLANS}__3d_fullres/fold_{FOLD__set_FOLD}/checkpoint_best.pth` at slurm/eval_fold_checkpoint.sh:62
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgLSTVOneShot/nnUNetTrainerWandB_500ep_LSTVOversample__{PLANS}__3d_fullres/fold_{FOLD__set_FOLD}/eval_{CHECKPOINT__pth}_{cmd}/checkpoint_best.pth` at slurm/eval_fold_checkpoint.sh:62
- matches nothing on disk: `/wsu/home/go/go24/go2432/allspine_v7_fov96_ctx/runs/model_rung_1*.pt` at slurm/eval_shortcut_controls.sh:89
- matches nothing on disk: `/wsu/home/go/go24/go2432/FluoroCap/finetune_v3/*.pt` at slurm/fluorocap_finetune_chain.sh:20
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_{DATASET_NAME}/{TRAINER}__{PLANS}__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_ablation.sh:245
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_{DATASET_NAME}/{TRAINER}__{PLANS}__3d_fullres/fold_0/checkpoint_latest.pth` at slurm/spine_ablation.sh:246
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_{DATASET_NAME}/{TRAINER}__{PLANS}__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_ablation.sh:249
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_{DATASET_NAME}/{TRAINER}__{PLANS}__3d_fullres/fold_0/checkpoint_latest.pth` at slurm/spine_ablation.sh:252
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_eval_single.sh:51
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_eval_single.sh:52
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_eval_single.sh:53
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_{arith}/checkpoint_best.pth` at slurm/spine_pred_803_best_array.sh:245
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_{F}/checkpoint_best.pth` at slurm/spine_predict_803_best.sh:148
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_{SLURM_ARRAY_TASK_ID}/checkpoint_final.pth` at slurm/spine_train_array.sh:240
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_{SLURM_ARRAY_TASK_ID}/checkpoint_latest.pth` at slurm/spine_train_array.sh:241
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_{SLURM_ARRAY_TASK_ID}/checkpoint_final.pth` at slurm/spine_train_array.sh:243
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_{SLURM_ARRAY_TASK_ID}/checkpoint_latest.pth` at slurm/spine_train_array.sh:249
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_{SLURM_ARRAY_TASK_ID}/checkpoint_final.pth` at slurm/spine_train_array.sh:656
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFullMerged/nnUNetTrainerWandB_500ep_LSTVOversample__nnUNetResEncUNetPlans_100G__3d_fullres/fold_{SLURM_ARRAY_TASK_ID}/checkpoint_*.pth` at slurm/spine_train_array.sh:669
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__{PLANS}__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_train_fold.sh:109
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__{PLANS}__3d_fullres/fold_0/checkpoint_latest.pth` at slurm/spine_train_fold.sh:110
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__{PLANS}__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_train_fold.sh:115
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__{PLANS}__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_train_fold.sh:118
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__{PLANS}__3d_fullres/fold_0/checkpoint_latest.pth` at slurm/spine_train_fold.sh:128
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__{PLANS}__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_train_fold.sh:306
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__{PLANS}__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_train_fold.sh:320
- matches nothing on disk: `{SLURM_SUBMIT_DIR}/nnunet/results/Dataset{cmd}_SpineSurgCTFull/nnUNetTrainerWandB_1000ep_LSTVOversample__{PLANS}__3d_fullres/fold_0/checkpoint_final.pth` at slurm/spine_train_fold.sh:323

Checkpoint names written without a directory (cannot be resolved to one file; public release names are exempt roots, the rest are listed so nobody reads their absence as 'none'):
- `checkpoint_best.pth` x26 (e.g. slurm/eval_fold_checkpoint.sh:111, slurm/eval_fold_checkpoint.sh:116)
- `polypose.ckpt` x25 (e.g. SchwingNet/results/polypose/REPRODUCTION.json:114, SchwingNet/results/polypose/REPRODUCTION.json:139)
- `best.pt` x19 (e.g. SchwingNet/results/a1.json:4, SchwingNet/results/arc/ARC_CHECK.md:100)
- `checkpoint_final.pth` x8 (e.g. slurm/spine_pred_803_best_array.sh:242, slurm/spine_predict_803_best.sh:145)
- `checkpoint_latest.pth` x8 (e.g. slurm/spine_pred_803_best_array.sh:242, slurm/spine_predict_803_best.sh:145)
- `yolo11m.pt` x3 (e.g. SchwingNet/results/dc_P_pooled_scores.json:4, slurm/anchor_c2.sh:57)
- `yolo11s.pt` x2 (e.g. slurm/buu_baseline.sh:30, slurm/sacrum_detector.sh:33)
- `dc_B_held_elekta_xvi/weights/best.pt` x1 (e.g. SchwingNet/results/lcurve/JOBS.txt:4)
- `detect_v5z_final_best.pt` x1 (e.g. SchwingNet/NUMBERS.md:170)
- `model_rung_1_aug2.pt` x1 (e.g. slurm/allspine_v2_chain.sh:33)
- `rx_lodo_carmlspine_1024/best.pt` x1 (e.g. SchwingNet/results/COUNTING_CHECK.md:83)
- `segmentations/NNN.pt` x1 (e.g. SchwingNet/results/polypose/POLYPOSE_API.md:19)
- `spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt` x1 (e.g. SchwingNet/results/COUNTING_CHECK.md:59)
- `xrays/NNN.pt` x1 (e.g. SchwingNet/results/polypose/POLYPOSE_API.md:21)

PolyPose `polypose.ckpt` files (SchwingNet/results/polypose/) are per-subject registration fits made from that subject's own frames: they are not population models and carry no held-out claim, so they are listed here and not traced.

