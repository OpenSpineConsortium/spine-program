# SpineSurg-CT: Progress Update
**To:** [PI Name]
**From:** Gregory Schwing
**Date:** March 19, 2026
**Re:** HPC Training Infrastructure — Status Update

---

## Summary

The full training infrastructure for SpineSurg-CT is now operational on the Wayne State warrior HPC cluster. Dataset acquisition, quality audit, preprocessing pipeline, and model architecture are complete. Training is queued.

---

## Dataset

CTSpine1K (~150GB, 784 COLONOG cases) and CTPelvic1K (pelvic masks) were downloaded and validated on warrior. A pre-training audit across 2,010 cases across all CTSpine1K subsets confirmed that the COLONOG subset is the appropriate training cohort: 784 cases with complete L1-L5 lumbar coverage, 16 lumbarization cases (L6 present, raw label 25), and 12 sacralization cases (L5 absent) — 1.8% LSTV prevalence, consistent with published estimates. COVID-19 and HNSCC-3DCT subsets were excluded due to truncated field of view (chest and head/neck CTs respectively), confirmed by the absence of lumbar labels in the audit output.

CTPelvic1K dataset1 yielded 35 COLONOG pelvic masks (33 matched to spine cases). Consistent with Li et al.'s two-stage strategy, we identified that the pelvic masks cover only the pelvic FOV (~100–200 slices) without paired full-torso CT images, making joint spine-pelvis training from the same cases infeasible at this stage. Stage 1 training proceeds on the 784 spine-only cases. Pelvic fine-tuning is deferred to stage 2.

---

## Architecture

The model implements CTSpineSegNet (Li et al., *Scientific Reports* 2025) — a 3D ResUNet with cross-scale feature fusion modules (CFFM) at encoder skip connections and a linear self-attention bottleneck reducing complexity from O(n²) to O(kn), k=64. Three novel extensions are added for LSTV detection:

1. **10-class unified output** including L6 (lumbarization), extending the paper's 5-class spine head
2. **Multi-task LSTV classification head** branching from the bottleneck, predicting Normal / Lumbarization / Sacralization
3. **Class-imbalance mitigation stack:** L6 loss weight ×20, WeightedRandomSampler (LSTV ×10), CopyPaste augmentation synthesizing lumbarization by transplanting L6 patches from real cases into normal spines, and Delete-L5 augmentation synthesizing sacralization by zeroing L5 labels in normal cases

A key preprocessing correction was made following close reading of the paper: orientation resampling was updated from RAS to PIR (posterior-inferior-right) per Li et al.'s specification, which is expected to improve L5/sacrum boundary performance given the model's positional sensitivity at the lumbosacral junction.

---

## Training Infrastructure

Training runs on warrior GPU nodes via SLURM with a 72-hour wall time. The pipeline includes:

- **TensorBoard** logging of all loss components separately (Dice, CE, LSTV classification) plus per-class DSC for all 9 foreground classes, with L6 DSC surfaced as a primary metric
- **Weights & Biases** integration with auto-loaded API key, enabling real-time remote monitoring and run comparison
- **Automated Bayesian HPO** via Ray Tune with Optuna TPE search and ASHA early stopping, sweeping learning rate, batch size, weight decay, architecture width, dropout, LSTV loss weight, and sacrum boost factor across configurable GPU allocations

---

## Evaluation Plan

Primary evaluation benchmarks SpineSurg-CT against TotalSegmentator (CT) on the held-out test set using DSC, HD95, and mIOU. The central result is L6 DSC on lumbarization cases: TotalSegmentator has no L6 class and will score 0.0 by design, while SpineSurg-CT predicts L6 explicitly. This architectural gap — and its clinical relevance to wrong-level surgery prevention — is the core contribution. Secondary metrics include LSTV classification F1 (Normal / Lumbarization / Sacralization), for which no CT segmentation baseline currently exists in the literature.

---

## Next Steps

1. Training run completion (~72hr wall time)
2. Evaluate checkpoint on held-out test set; generate `l6_comparison.csv`
3. If L6 DSC is acceptable, run HPO to optimize hyperparameters
4. Consider stage 2 pelvic fine-tuning using CTPelvic1K datasets 2–7 (CLINIC, CLINIC-metal, MSD subsets) which have paired CT images and pelvic masks
