# SpineSurg-CT: Progress Update
**To:** [PI Name]
**From:** Gregory Schwing
**Date:** March 20, 2026
**Re:** HPC Training Infrastructure — Status Update

---

## Summary

The full training infrastructure for SpineSurg-CT is now operational on the Wayne State warrior HPC cluster and a training run is currently active on an NVIDIA H200 GPU. Dataset acquisition, quality audit, preprocessing pipeline, LSTV augmentation stack, and model architecture are complete. Registration-based sacralization synthesis is queued as a follow-up augmentation job.

---

## Dataset

CTSpine1K (~150GB, 784 COLONOG cases) and CTPelvic1K (pelvic masks) were downloaded and validated on warrior. A pre-training audit across 2,010 cases confirmed the COLONOG subset as the appropriate training cohort: 784 cases with complete L1-L5 lumbar coverage, 16 lumbarization cases (L6 present, raw label 25), and 9 confirmed sacralization cases (L5 absent with remaining lumbar coverage) — 3.2% LSTV prevalence across 25 total LSTV cases. COVID-19 and HNSCC-3DCT subsets were excluded due to truncated field of view, confirmed by absence of lumbar labels in the audit output.

CTPelvic1K dataset1 yielded 35 COLONOG pelvic masks, of which 33 were matched to spine cases using DICOM UID patient number extraction. The pelvic masks cover only the pelvic FOV (~100–200 axial slices) against full-torso CT acquisitions (~500–600 slices), which is why Li et al. adopted a two-stage training strategy. Stage 1 training proceeds on all 784 spine cases; the 33 matched cases additionally receive fused sacrum/hip labels via online resampling into spine CT space. Pelvic fine-tuning using CTPelvic1K datasets 2–7 is deferred to stage 2.

The dataset was split with stratification across three strata — LSTV cases, normal spine cases, and pelvic cases — independently, guaranteeing LSTV representation in all three sets: **552 train / 116 val / 116 test**, with 19 LSTV cases in training.

---

## Architecture

The model implements CTSpineSegNet (Li et al., *Scientific Reports* 2025) — a 3D ResUNet with cross-scale feature fusion modules (CFFM) applied at encoder skip connections between layers 1→2 and 2→3, and a linear self-attention bottleneck reducing complexity from O(n²) to O(kn), k=64. Key preprocessing follows the paper specification: 1mm isotropic resampling, PIR orientation (posterior-inferior-right, corrected from an initial RAS error), HU clipping to [-1000, 1000] normalized to [0,1], and center-cropping to 256³.

Three novel extensions beyond Li et al. are implemented for LSTV detection:

1. **10-class unified output** including L6 (lumbarization, raw CTSpine1K label 25), extending the paper's 5-class spine head
2. **Multi-task LSTV classification head** branching from the bottleneck, predicting Normal / Lumbarization / Sacralization as a secondary task with loss weight α=0.5
3. **Multi-strategy class imbalance mitigation** — described in detail below

---

## LSTV Augmentation Strategy

Addressing the severe class imbalance (16 lumbarization, 9 sacralization cases out of 784 total) is the central methodological challenge. Four complementary strategies are implemented:

**WeightedRandomSampler** — LSTV cases are oversampled at 10× frequency in the training DataLoader, ensuring approximately one LSTV case per batch even at batch size 8.

**Class-weighted loss** — L6 receives a 20× loss weight, sacrum/hip classes receive 2× weight. For sacralization samples, the sacrum CE weight is further boosted by 2× (the sacralization boost factor) because the fused L5 territory anatomically enlarges the sacrum volume.

**CopyPaste augmentation (lumbarization)** — Before training begins, the 11 lumbarization training cases are preprocessed and loaded into RAM as a source pool. During training, 30% of normal spine scans receive a synthetic L6 transplant: a random lumbarization case is selected from the pool, the L6 vertebral patch is extracted with 8-voxel padding, elastically deformed, and pasted into the lumbosacral junction zone of the target scan with simultaneous label update. This generates continuous synthetic lumbarization variety throughout training from a small real case pool.

**Registration-based sacralization synthesis (in preparation)** — For sacralization, simple label deletion is anatomically incorrect because real sacralization has distinct morphological features: enlarged L5 transverse processes, absent L4-S1 disc space, and an elongated sacrum. A deformable registration approach using ANTs SyN is implemented: for each of the 9 real sacralization training cases, we register it to a reference normal spine, cache the inverse deformation field, and apply that field on-the-fly to normal training scans during training. The inverse field warps the CT image to produce collapsed disc space and enlarged transverse processes, while the simultaneous label warp plus an L5-to-sacrum fusion post-processing step produces anatomically correct sacralization labels. With 9 stored fields applied to 533 normal training cases, this provides effectively unlimited unique synthetic sacralization variants per epoch. Registration runs once at startup (~45 minutes) with fields cached to disk for subsequent runs.

**Future augmentation directions** — The registration approach, while anatomically principled, is limited by the morphological diversity of the 9 source cases. Two more powerful approaches are identified for future work. First, **ControlNet conditioned on segmentation masks**: a ControlNet fine-tuned on the 784 spine CT/label pairs could generate novel CT appearances conditioned on a sacralization label map, producing both image and label simultaneously with greater appearance diversity than registration alone. Second, **3D latent diffusion in CT space**: a small DDPM trained directly on 256³ spine volumes conditioned on the label map (using the sacralization cases to seed the conditioning distribution) would learn the full joint distribution of sacralization CT appearance and anatomy. The latter approach would constitute a standalone methodological contribution and is the strongest long-term solution to the data scarcity problem.

---

## Training Configuration

| Parameter | Value |
|---|---|
| Hardware | NVIDIA H200 (141GB VRAM), Wayne State warrior HPC |
| Partition | gmsap |
| Batch size | 8 |
| Precision | FP16 mixed (bf16 available) |
| Optimizer | AdamW, lr=1e-3, weight_decay=1e-5 |
| LR schedule | Linear warmup (5 epochs) → cosine annealing |
| Max epochs | 300 with early stopping (patience=30 on val/dsc) |
| Workers | 8 data loading workers |
| Augmentation | Flip, rotation ±30°, zoom 0.7–1.4×, Gaussian noise, contrast/brightness jitter |
| Gradient clipping | 1.0 |
| Wall time | 72 hours |

Visual monitoring via TensorBoard (all loss components logged separately: Dice, CE, LSTV classification) and Weights & Biases with auto-loaded API key. Per-class DSC logged for all 9 foreground classes; L6 DSC surfaced as a primary dashboard metric.

Automated Bayesian hyperparameter optimization is implemented via Ray Tune with Optuna TPE search and ASHA early stopping, sweeping lr, batch size, weight decay, architecture width, dropout, LSTV loss weight, and sacrum boost factor. HPO can be launched across up to 4 H200 GPUs simultaneously on the gmsap partition.

---

## Evaluation Plan

Primary evaluation benchmarks SpineSurg-CT against TotalSegmentator (CT) on the held-out test set (116 cases) using DSC, HD95, and mIOU. The central result is L6 DSC on lumbarization cases: TotalSegmentator has no L6 class and will score 0.0 by design, while SpineSurg-CT predicts L6 explicitly. This is an architectural capability gap rather than a performance margin. Secondary metrics include LSTV classification F1 across all three classes (Normal / Lumbarization / Sacralization), for which no CT segmentation baseline currently exists in the literature. Benchmark outputs include `per_case_metrics.csv`, `l6_comparison.csv` (lumbarization cases only), and `lstv_type_breakdown.csv` (per-LSTV-type mean DSC for both models).

---

## Next Steps

1. Current training run completion (~72hr wall time on H200)
2. Rebuild container with antspyx and run `slurm/run_sacral_registration.sh` (primary queue, ~4hr)
3. Retrain with registration-based sacralization synthesis active
4. Evaluate checkpoint; generate benchmark outputs
5. If L6 DSC is satisfactory, run HPO on 4×H200 to optimize hyperparameters
6. Stage 2: pelvic fine-tuning using CTPelvic1K datasets 2–7
