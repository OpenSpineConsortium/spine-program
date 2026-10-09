# SpineSurg-CT: Progress Update
**To:** [PI Name]
**From:** Gregory Schwing
**Date:** March 20, 2026
**Re:** HPC Training Infrastructure — Status Update

---

## Clinical Significance

Wrong-level spine surgery is a recognized sentinel event in neurosurgery. Although reported incidence varies by setting, large series consistently place rates below 1% of spinal procedures — a figure that, given the volume of lumbar spine operations performed annually in the United States, represents a substantial absolute burden of preventable harm with profound medicolegal consequences [1]. Among anatomical risk factors, lumbosacral transitional vertebrae (LSTV) — either lumbarization of S1 (creating a supernumerary sixth lumbar segment) or sacralization of L5 (fusing it to the sacrum) — are consistently cited as a primary precipitant [1,2]. In a study of 550 consecutive patients undergoing lumbar surgery, Ishida et al. found LSTV in 12.9% and documented vertebral miscounting at the initial outpatient evaluation in 54% of LSTV cases — with 15% of cases requiring intraoperative level revision after true vertebral counting was established [3].

The prevalence of clinically significant LSTV (Castellvi types II–IV) in the general population is approximately 4–18%, depending on imaging modality and definition [4,5]. CT is the reference standard for LSTV classification: Hanhivaara et al. (2024) demonstrated that CT achieves 76% sensitivity and 93% specificity for LSTV detection, while routine MRI without coronal sequences achieves only 54% sensitivity — meaning nearly half of LSTV cases are missed on the most common preoperative imaging modality [6]. The clinical implication is direct: a surgeon planning a lumbosacral procedure from a standard MRI report has a substantial probability of operating on a patient with unidentified LSTV and a miscounted level.

**The gap in existing automated tools is architectural, not incremental.** TotalSegmentator (Wasserthal et al., *Radiology: Artificial Intelligence* 2023) — the most widely used automated CT segmentation tool, trained on 1,204 CT examinations segmenting 104 anatomical structures — segments L1 through L5 and sacrum but has no L6 class [7]. This is a design limitation: TotalSegmentator assumes a fixed five-lumbar anatomy and therefore cannot represent, detect, or flag lumbarization by construction. Its L5 DSC on a lumbarization case is meaningless — it will label the L6 as either L5 or sacrum depending on the prior. SpineSurg-CT will score TotalSegmentator on lumbarization test cases as a head-to-head benchmark; its L6 DSC will be 0.0 by architectural necessity.

The only existing automated LSTV detection system in the CT/radiograph literature is a ResNet-50 classifier trained on plain radiographs (Kwak et al., *J Clin Med* 2025), which achieves 76.4% accuracy, 85.1% sensitivity, and 61.9% specificity for binary LSTV detection [8]. This is a detection-only approach: it flags whether LSTV is present but provides no vertebral segmentation, no Castellvi classification, and no level-specific label that a surgeon could use for surgical planning. Commercial vertebral numbering tools (e.g., Siemens Spine Dot Engine) identify vertebral bodies but are not trained to handle LSTV as a distinct anatomical entity [9].

**SpineSurg-CT advances the field in three distinct ways.** First, it provides the only automated CT segmentation model with an explicit L6 class, directly enabling level counting in lumbarization cases where all current tools fail. Second, it adds a secondary LSTV classification head (Normal / Lumbarization / Sacralization) that goes beyond detection to provide the specific anatomical diagnosis — distinguishing lumbarization, which adds a level, from sacralization, which removes one. Third, by grounding the output in a dense 3D segmentation label rather than a binary classification flag, it provides the spatial precision needed for surgical planning: a surgeon can visualize exactly where L6 begins and ends, verify the lumbosacral junction anatomy, and plan instrumentation accordingly.

The clinical and medicolegal case for this tool is straightforward: it converts a known, preventable category of wrong-level surgery from a vigilance problem into an automated detection problem.

---

## References

1. Albano S, Brown NJ, Pennington Z, et al. Risks Associated with Surgical Management of Lumbosacral Transitional Vertebrae: Systematic Review of Surgical Considerations and Illustrative Case. *World Neurosurg.* 2024;186:e54–e64.
2. Karsy M, Harward SC. Preventing Wrong-Level Spine Surgery. In: *Complications in Neurosurgery II*. StatPearls/NCBI Bookshelf. Updated 2024.
3. Ishida T, Nitta A, Tokioka T, et al. Lumbosacral Transitional Vertebrae Cause Spinal Level Misconception in Surgeries for Degenerative Lumbar Spine Disorders. *Asian Spine J.* 2017;11(4):518–524.
4. Apazidis A, Ricart PA, Diefenbach CM, Spivak JM. The prevalence of transitional vertebrae in the lumbar spine. *Spine J.* 2011;11(9):858–862.
5. Nardo L, Alizai H, Virayavanich W, et al. Lumbosacral transitional vertebrae: association with low back pain. *Radiology.* 2012;265(2):497–503.
6. Hanhivaara J, Määttä JH, Kinnunen P, et al. Castellvi classification of lumbosacral transitional vertebrae: comparison between conventional radiography, CT, and MRI. *Acta Radiol.* 2024;65(1):71–78.
7. Wasserthal J, Breit HC, Meyer MT, et al. TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images. *Radiol Artif Intell.* 2023;5(5):e230024.
8. Kwak JH, et al. Automated Detection of Lumbosacral Transitional Vertebrae on Plain Lumbar Radiographs Using a Deep Learning Model. *J Clin Med.* 2025;14(21):7671.
9. Gomes P, et al. The role of Artificial intelligence in the assessment of the spine and spinal cord. *Eur J Radiol.* 2023;161:110726.

---

## Summary

The full training infrastructure for SpineSurg-CT is operational on the Wayne State warrior HPC cluster. A training run is currently active on an NVIDIA H200 GPU. Dataset acquisition, quality audit, preprocessing pipeline, LSTV augmentation stack, stratified data splitting, and model architecture are all complete. Registration-based sacralization synthesis and augmentation quality assessment are queued as follow-up jobs.

---

## Dataset

CTSpine1K (~150GB, 784 COLONOG cases) and CTPelvic1K (pelvic masks) were downloaded and validated on warrior. A pre-training audit across 2,010 cases confirmed the COLONOG subset as the appropriate training cohort: 784 cases with complete L1-L5 lumbar coverage, 16 lumbarization cases (L6 present, raw label 25), and 9 confirmed sacralization cases (L5 absent with remaining lumbar coverage) — 3.2% LSTV prevalence across 25 total LSTV cases. COVID-19 and HNSCC-3DCT subsets were excluded due to truncated field of view, confirmed by absence of lumbar labels in the audit.

CTPelvic1K yielded 35 COLONOG pelvic masks, of which 33 were matched to spine cases using DICOM UID patient number extraction (94% match rate). These 33 matched cases have confirmed zero overlap with the 25 LSTV cases. CTPelvic1K datasets 2–7 (KITS19, CLINIC, MSD subsets) originate from entirely different patient populations with no overlap with CTSpine1K COLONOG.

The pelvic masks cover only the pelvic FOV (~100–200 axial slices) against full-torso CT acquisitions (~500–600 slices). For the 33 matched cases, sacrum/hip labels are fused into the spine CT space at preprocessing time via nearest-neighbour resampling, adding classes 7–9 (sacrum, left hip, right hip) to the unified label.

**Stratified split (552 train / 116 val / 116 test):** Four independent strata ensure critical case types appear in all three sets:

| Stratum | n | train | val | test | Purpose |
|---|---|---|---|---|---|
| LSTV | 25 | 19 | 3 | 3 | Rarest, highest clinical priority |
| Spine + pelvic mask | 33 | 23 | 5 | 5 | Sacrum/hip supervision in val/test |
| Spine only | 726 | 510 | 108 | 108 | Bulk of data |

---

## Architecture

The model implements CTSpineSegNet (Li et al., *Scientific Reports* 2025) — a 3D ResUNet with cross-scale feature fusion modules (CFFM) applied at encoder skip connections between layers 1→2 and 2→3, and a linear self-attention bottleneck reducing complexity from O(n²) to O(kn), k=64. Key preprocessing follows the paper specification: 1mm isotropic resampling, PIR orientation (posterior-inferior-right, corrected from an initial RAS implementation error), HU clipping to [-1000, 1000] normalized to [0,1], and center-cropping to 256³ voxels.

Three novel extensions beyond Li et al. are implemented for LSTV detection:

1. **10-class unified output** including L6 (lumbarization, raw CTSpine1K label 25), extending the paper's 5-class spine head. No existing CT segmentation model has this class.
2. **Multi-task LSTV classification head** branching from the bottleneck, predicting Normal / Lumbarization / Sacralization as a secondary task with loss weight α=0.5.
3. **Multi-strategy class imbalance mitigation** — described below.

---

## LSTV Augmentation Strategy

Addressing the severe class imbalance (25 LSTV out of 784 total, 3.2%) is the central methodological challenge. Five complementary strategies are implemented:

**WeightedRandomSampler** — LSTV cases are oversampled at 10× frequency in the training DataLoader, ensuring approximately one LSTV case per batch at batch size 8.

**Class-weighted loss** — L6 receives a 20× loss weight, sacrum/hip classes receive 2×. For sacralization samples, the sacrum CE weight is further boosted by 2× (sacralization boost factor) because the fused L5 territory anatomically enlarges the sacrum volume.

**CopyPaste augmentation (lumbarization)** — The 11 lumbarization training cases are preprocessed at startup into an in-memory pool. During training, 30% of normal spine scans receive a synthetic L6 transplant: a random pool case is selected, the L6 vertebral patch is extracted with 8-voxel bounding-box padding, elastically deformed for morphological variety, and pasted into the lumbosacral junction zone of the target scan with simultaneous label update.

**Registration-based sacralization synthesis (queued)** — Label deletion alone is anatomically incorrect for sacralization because real sacralization has structurally distinct morphology: enlarged L5 transverse processes, absent L4-S1 disc space, and an elongated sacrum. The implemented approach uses ANTs SyN deformable registration: for each of the 9 real sacralization training cases, it is registered to a reference normal spine and the inverse deformation field is cached to disk. During training, a random cached field is applied on-the-fly to normal spine scans — warping both the CT image and label simultaneously — and L5 voxels adjacent to the sacrum are relabeled as sacrum via binary dilation post-processing.

**DeleteL5Transform (current fallback)** — Until the registration job completes, L5 voxels are zeroed in the label with 20% probability on normal training scans. This is acknowledged as anatomically imprecise but provides a weak sacralization signal.

**Future augmentation directions** — Two more powerful approaches are identified for future work. First, ControlNet conditioned on segmentation masks could generate novel CT appearances from a sacralization label map with greater morphological diversity than registration. Second, a 3D latent diffusion model (DDPM) trained directly on 256³ spine volumes conditioned on LSTV label maps would learn the full joint distribution of sacralization CT appearance and anatomy.

**Augmentation QC** — A dedicated quality assessment pipeline (`src/utils/augmentation_qc.py`) generates visual examples (axial/coronal/sagittal grids with label overlays) and three quantitative metrics: MS-SSIM, normalized cross-correlation, and one-to-all nearest-neighbour cosine distance in radiomics feature space.

---

## Training Configuration

| Parameter | Value |
|---|---|
| Hardware | NVIDIA H200 (141GB VRAM), Wayne State warrior HPC |
| Partition | gmsap (nodes msa1–msa4) |
| Batch size | 8 |
| Precision | FP16 mixed |
| Optimizer | AdamW, lr=1e-3, weight_decay=1e-5 |
| LR schedule | Linear warmup (5 epochs) → cosine annealing to 1e-6 |
| Max epochs | 300 with early stopping (patience=30, monitor: val/dsc) |
| Data workers | 8 per GPU |
| Augmentation | Flip, rotation ±30°, zoom 0.7–1.4×, Gaussian noise σ≤0.1, contrast/brightness jitter (γ 0.7–1.5) |
| Gradient clipping | 1.0 |
| Wall time | 72 hours |

Visual monitoring via TensorBoard and Weights & Biases. Per-class DSC is logged for all 9 foreground classes; L6 DSC and LSTV classification accuracy are primary dashboard metrics. Automated Bayesian HPO is implemented via Ray Tune with Optuna TPE search and ASHA early stopping across up to 4×H200 GPUs.

---

## Evaluation Plan

Primary evaluation benchmarks SpineSurg-CT against TotalSegmentator (CT) [7] on the 116-case held-out test set using DSC, HD95, and mIOU. The central clinical result is L6 DSC on lumbarization test cases: TotalSegmentator scores 0.0 by architectural necessity, while SpineSurg-CT predicts L6 explicitly. Secondary metrics include LSTV classification F1 across all three classes — a task for which the Kwak et al. radiograph classifier [8] provides the only existing comparison point, operating at 76.4% binary accuracy without subtype distinction. Benchmark outputs include `per_case_metrics.csv`, `l6_comparison.csv`, and `lstv_type_breakdown.csv`.

---

## Next Steps

1. Current training run completion (~72hr wall time on H200)
2. Rebuild container with antspyx; run `slurm/run_sacral_registration.sh` (~4hr, primary queue)
3. Run augmentation QC (`slurm/run_augmentation_qc.sh`) to verify both augmentation strategies
4. Retrain with registration-based sacralization synthesis active
5. Evaluate checkpoint; generate benchmark outputs including `l6_comparison.csv`
6. If L6 DSC is satisfactory, run HPO on 4×H200
7. Stage 2: pelvic fine-tuning
