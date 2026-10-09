# Does synthetic anatomical variation actually help?

Angle: measured downstream evidence. Compiled 2026-09-23. Every number here was read off the
cited source in this session; where a source would not render, that is said plainly rather than
filled in from memory.

The question is narrow on purpose: not "can a model generate a plausible spine" but "did anyone
train a detector or segmenter with generated or deformed **anatomy** and measure a gain on real
held-out data". Intensity jitter, noise, gamma, blur, rotation, scaling, flips are the control
condition, not the intervention.

> Two passes. Sections 1-7 are the first pass; sections 8-13 are a second pass that corrects
> section 1 (Payer DID use random elastic deformation, parameters in 8.1), adds the one challenge
> won with generative augmentation together with the same group ablation showing it hurt, and adds
> the only spine-specific downstream result. Where they differ, the second pass is the later reading.

---

## Headline

**The pragmatic state of the art for spine networks is affine + intensity augmentation and
nothing else.** Every spine challenge winner and every widely used spine model I could check
(VerSe'19 Payer, VerSe'20 Chen, AASCE'19 Seg4Reg, TotalSegmentator, nnU-Net-derived SPINEPS
lineage, VERIDAH) trains on rotation / scaling / mirroring / intensity transforms. None of them
generates anatomy. The single most-validated framework in the field, nnU-Net, **deliberately
turned elastic deformation off** and its successor never reinstated it.

**Where anatomy-level synthesis has been measured, the gains are small (1–2 Dice points, ~5%
more lesions) and the strongest results in our own modality came from *not* deforming anatomy
at all.** SyntheX, the best-validated DRR-to-real-X-ray transfer result in the literature, used
20 CTs, no anatomical deformation, and beat a real-data-trained model — by randomising
intensity, pose and projection.

**The one measured lever for rare anatomy is having real rare cases and oversampling them.**
VERIDAH's ablation is the cleanest number in this whole file: remove labelled anomalous cases
from training and thoracic-anomaly recall collapses from 87.80% to 32.93% (MRI) and 96.30% to
25.93% (CT). Nobody has published a synthesis method that recovers that.

---

## 1. What the spine challenge winners actually used

### VerSe'19 / VerSe'20 (MICCAI)
Sekuboyina A, Husseini ME, Bayat A, et al. *VerSe: A Vertebrae labelling and segmentation
benchmark for multi-detector CT images.* Med Image Anal 2021;73:102166.
doi:10.1016/j.media.2021.102166 · PMID 34340104 · arXiv:2001.09193

- 25 algorithms across two iterations. **Winners:** Payer C. (VerSe'19, hidden set ID rate
  94.25, Dice 89.80); Chen D. (VerSe'20, hidden set ID rate 96.58, Dice 91.23).
- **The benchmark paper does not report the augmentation of any participating algorithm.** The
  methods sections cover architecture, training scheme and post-processing only. That absence is
  itself informative — the organisers did not consider augmentation a differentiator.
- Payer's own method paper (Payer C, Štern D, Bischof H, Urschler M. *Coarse to Fine Vertebrae
  Localization and Segmentation with SpatialConfiguration-Net and U-Net.* VISAPP 2020;
  code: https://github.com/christianpayer/MedicalDataAugmentationTool-VerSe) describes "strong
  intensity and spatial augmentation … to account for domain shift towards domains unknown
  during training". Spatial = translation/rotation/scale/elastic in his MedicalDataAugmentationTool.
  **No generated anatomy.** I could not render the VISAPP PDF to recover the exact parameter
  ranges; they are in the repo's config files.
- **The rare-anatomy result that matters to us:** "None of the methods in VerSe'19 identified the
  presence of L6" on the hidden test set, despite two L6 training examples. For T13, identification
  rate "widely varies between the Public and Hidden phases for all teams" except one. Performance
  on rare anatomy was uniformly below normal anatomy. Cross-iteration, Payer's method was the
  robust one when VerSe'19 methods met VerSe'20 L6 cases; Lessmann's and Chen M.'s dropped.
- Read this as the honest baseline: conventional augmentation did **not** solve the transitional
  vertebra. It also means nobody has shown that anything else does.

### AASCE 2019 (Cobb angle from AP radiographs)
Winner: Lin Y, Zhou H-Y, Ma K, Yang X, Zheng Y. *Seg4Reg Networks for Automated Spinal Curvature
Estimation.* MICCAI 2019 CSI workshop, LNCS 11963:69–74. SMAPE 21.71 on the test set.
Code: https://github.com/hust-linyi/Seg4Reg
Augmentation (as stated in the Seg4Reg+ follow-up, arXiv:2208.12462): "randomly flipping,
rotating (−45°, 45°), and rescaling with the factor between (0.85, 1.25)". A domain-adaptation
module handled the train/test shift. **No generated anatomy.**

### RSNA 2022 Cervical Spine Fracture Detection (Kaggle)
1st place (Qishen Ha): two-stage, 3D U-Net segmentation of C1–C7 (trained on the 87 cases with
3D masks) then a 2.5D CNN+LSTM classifier over 15 sampled slices. Augmentation reported in the
writeup: standard 2D transforms plus **mixup**; ensembling worth ~0.02 CV.
Writeup: kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/writeups/qishen-ha-1st-place-solution
Winning-algorithm evaluation: Lin M, Ball RL, Gillberg J, et al. *Performance of the Winning
Algorithms of the RSNA 2022 Cervical Spine Fracture Detection Challenge.* Radiol Artif Intell
2024;6(1):e230256. doi:10.1148/ryai.230256 · PMID 38169426. (The RSNA site returned 403 to me;
I did not read the full text, so I cannot say whether it discusses augmentation.)
**No generated anatomy in any writeup I could read.**

### RSNA 2024 Lumbar Spine Degenerative Classification (Kaggle)
1st place writeup exists at
kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/writeups/avengers-1st-place-solution
but Kaggle served me only the page title; **I could not read the augmentation list.** Flagged as
unknown rather than guessed. Publicly summarised solutions in this competition are
detector→crop→2.5D classifier pipelines with conventional augmentation; I did not verify that.

### TotalSegmentator
Wasserthal J, Breit H-C, Meyer MT, et al. *TotalSegmentator: Robust Segmentation of 104 Anatomic
Structures in CT Images.* Radiol Artif Intell 2023;5(5):e230024. arXiv:2208.05868.
Two deviations from nnU-Net defaults, both stated: **mirroring removed** (so left/right structures
stay distinguishable) and epochs raised from 1000 to 4000. Nothing else. **No generated anatomy.**

### SPINEPS
Möller H, Graf R, Schmitt J, et al. *SPINEPS — automatic whole spine segmentation of T2-weighted
MR images using a two-phase approach to multi-class semantic and instance segmentation.*
Eur Radiol 2025;35:1178–1189. arXiv:2402.16368 · PMC11836161. Beats an nnU-Net baseline on every
structure (vertebra instances: Dice 0.933 vs 0.911, p<0.001; ASSD 0.21 vs 0.435, p<0.001) by
**architecture** (semantic then instance phase), not by data synthesis.

### VERIDAH — the one that measured the rare-class question
Möller H, Schoen H, Graf R, Atad M, Molinier N, Sekuboyina A, et al. *VERIDAH: Solving
Enumeration Anomaly Aware Vertebra Labeling across Imaging Sequences.* arXiv:2601.14066 (2026).

- Handles L6/T13 by relabelling them as a duplicated T12/L5 pair, four classification heads
  (label, region, transition, visibility) and a dynamic-programming sequence decoder constrained
  to 11–13 thoracic and 4–6 lumbar.
- Augmentation: RandCut (p=0.20), RandAffine (p=0.40), RandGaussianSmooth, RandGaussianNoise,
  intensity adjustment. **No synthesis.** Rare-class handling = anomalous cases "sampled four
  times during each epoch".
- Data: NAKO MRI 6,291 subjects (5,291 train / 1,000 test; test TEA rate 8.2%, LEA 14.6%);
  CT 1,536 (1,171 / 365; test TEA 6.8%, LEA 7.9%).
- Results: perfect-labelling 98.30% (T2w MRI) / 99.18% (CT); TEA recall 87.80% / 96.30%;
  LEA recall 94.48% / 97.22%.
- **The ablation:** trained without labelled anomalies, TEA recall falls to **32.93%** (MRI) and
  **25.93%** (CT). Real labelled rare anatomy plus 4× oversampling is what carries the result.

**Answer to the pragmatic question in the brief: yes — the winners used nothing more than affine
and intensity augmentation, and that is the answer to report.**

---

## 2. nnU-Net turned elastic deformation off

This is load-bearing, so it is stated with the source lines.

- nnU-Net v1 `default_3D_augmentation_params` does contain `"do_elastic": True` with
  `elastic_deform_alpha: (0., 900.)`, `elastic_deform_sigma: (9., 13.)` — but that dict is the
  legacy default.
- `nnUNetTrainerV2.setup_DA_params` (v1.7.1) overrides it:
  `self.data_aug_params["do_elastic"] = False`, with the docstring line **"we don't do elastic
  deformation anymore"**. Rotations widened to ±30° on all three axes, `scale_range = (0.7, 1.4)`.
  https://github.com/MIC-DKFZ/nnUNet/blob/v1.7.1/nnunet/training/network_training/nnUNetTrainerV2.py
- nnU-Net v2 `nnUNetTrainer.get_training_transforms` calls
  `SpatialTransform(..., p_elastic_deform=0, p_rotation=0.2, rotation=..., p_scaling=0.2,
  scaling=(0.7, 1.4), ...)`. Elastic deformation is **absent by default**. The rest of the
  pipeline is Gaussian noise (var 0–0.1, p=0.1), Gaussian blur (σ 0.5–1.0, p=0.2), multiplicative
  brightness 0.75–1.25 (p=0.15), contrast 0.75–1.25 (p=0.15), simulate-low-resolution (p=0.25),
  gamma 0.7–1.5 inverted (p=0.1) and non-inverted (p=0.3), mirroring on all axes.
  https://github.com/MIC-DKFZ/nnUNet/blob/master/nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py

The group that has won more medical segmentation challenges than anyone removed the one
deformation-based augmentation it had, and the framework got better. **What is not known:** the
nnU-Net papers do not publish the ablation table that justified removing it, so this is an
argument from revealed preference, not from a measured number. Say that out loud if it is used
in the manuscript.

---

## 3. Anatomy-level augmentation that WAS measured downstream

Ranked by how close the evidence is to what we need.

### 3.1 Anatomy-informed deformation (prostate MRI) — closest published analogue, small gain
Kovacs B, Netzer N, Baumgartner M, Eith C, Bounias D, … Isensee F, … Maier-Hein KH.
*Anatomy-informed Data Augmentation for Enhanced Prostate Cancer Detection.* MICCAI 2023,
LNCS 14220:531–540. doi:10.1007/978-3-031-43990-2_50 · arXiv:2309.03652
Code: https://github.com/MIC-DKFZ/anatomy_informed_DA — **Apache-2.0**, ships as an nnU-Net v2
trainer (`nnUNetTrainer_AnatInf.py`).

- Mechanism: uses segmentations of *adjacent* organs (rectum, bladder) to simulate the
  physiological soft-tissue deformation they impose on the prostate, deforming image and lesion
  label together so the pathological label survives. Explicitly motivated by the observation that
  "simplistic spatial transformations … do not substantially increase the organ as well as tumor
  shape variability".
- Data: 774 biopsy-confirmed examinations. Backbone: nnU-Net (nnDetection lineage).
- **Measured gain: at 0.32 false positives per scan it found 4 more lesions out of 76 (+5.3%).**
  Authors report the lesion-level and patient-level F1 improvement as significant by t-test.
- **Be adversarial about this one.** The MICCAI reviews, which are public, say the "reported
  performance improvements in Table 1 were highly variable", the meta-reviewer called the
  improvement "even if marginal", and a reviewer criticised testing on "only one backbone
  segmentation model". The authors themselves note "simplifications in the biomechanical
  properties of the human pelvis". This is the best-engineered anatomy-deformation augmentation
  in the literature and it bought ~5% more lesions on one backbone, one dataset, one centre.
- Generalisability to spine: the repo is pelvis-specific (rectum/bladder priors). The *idea*
  transfers; the code does not.

### 3.2 Statistical shape + intensity model augmentation (hip bone CT) — +2 Dice points
Schmid J, Assassi L, Chênes C. *A novel image augmentation based on statistical shape and
intensity models: application to the segmentation of hip bones from CT images.*
Eur Radiol Exp 2023;7:39. doi:10.1186/s41747-023-00357-6 · PMC10406777

- Mechanism: sample an instance from a statistical shape+intensity model (tetrahedral mesh,
  Bernstein polynomials), pick the nearest real training image as template, erase the original
  bone via signed distance map, warp the sampled bone in with a thin-plate spline and paint its
  intensities. Generates **shape + intensity + label** together, offline.
- Data: 232 patients. External test: CTPelvic1K, 31 hip bone images.
- **Numbers: no augmentation DSC 0.93 [0.90–0.95]; SSIM augmentation alone 0.93 [0.91–0.95];
  basic + SSIM 0.95 [0.93–0.96]** (stated significant). External set 0.95 ± 0.054.
- Read it honestly: **SSIM augmentation alone was worth nothing** (0.93 → 0.93). It only helped
  stacked on top of conventional augmentation, and then by 2 points on an already-saturated task.
  The authors note the external set lacked the pathology present in training.
- **Code not released.** Data restricted by ethics committee. This is the closest thing to a
  "proven, validated" shape-model augmentation pipeline and you cannot download it.

### 3.3 Registration- and generation-based deformation fields, scaling-law study
Chu Y, Han Z, Luo G, Gao X. *Revisiting Data Scaling in Medical Image Segmentation via
Topology-Aware Augmentation.* arXiv:2511.13883v2 (preprint, last revised Feb 2026).
- Compares Random Elastic Deformation (RED), **RegDA** (diffeomorphic deformations harvested by
  LDDMM registration between real subjects) and **GenDA** (conditional GAN generating deformation
  fields) across 15 tasks in CT, X-ray (including spine), MRI and retinal imaging.
- **"RED introduces only minor changes to the fitted parameters, indicating that random
  deformation provides limited improvement in effective data utilization."** GenDA reported as
  outperforming RegDA in most scenarios and cheaper.
- **Weakness to state:** the paper reports binary cross-entropy scaling curves, not Dice, and does
  not give per-case counts. It supports "learned/anatomically-constrained deformation beats random
  elastic" directionally. It does not give a Dice number anyone can quote. Preprint, not peer
  reviewed.

### 3.4 Learned spatial + intensity transforms, one-shot (brain MRI) — large gain, extreme regime
Zhao A, Balakrishnan G, Durand F, Guttag JV, Dalca AV. *Data augmentation using learned
transformations for one-shot medical image segmentation.* CVPR 2019:8543–8553. arXiv:1902.09383
Code: https://github.com/xamyzhao/brainstorm
- Mechanism: learn a spatial deformation model and an intensity model from unlabelled scans by
  registration to one labelled atlas, then synthesise labelled examples by composing them. This is
  the canonical "learn anatomical variation from your own cohort and replay it" method.
- Reported as "significant improvements over state-of-the-art methods for one-shot biomedical
  image segmentation". **I could not retrieve the Dice table** — the CVPR open-access PDF returned
  403 and the arXiv abstract carries no numbers. Do not quote a figure for this paper without
  reading the table.
- **The regime is the catch:** one labelled scan. Gains from synthesis are largest exactly where
  real labels are near zero. We have 802 + 1,228 + 374 labelled CTs. The published evidence does
  not say the method still pays at n≈2,900.

### 3.5 Adversarial deformation + bias field (cardiac/prostate MRI) — large gain, low-shot only
Chen C, Qin C, Ouyang C, Li Z, Wang S, Qiu H, Chen L, Tarroni G, Bai W, Rueckert D.
*Enhancing MR image segmentation with realistic adversarial data augmentation.* Med Image Anal
2022;82:102597. doi:10.1016/j.media.2022.102597 · PMID 36095907 · arXiv:2108.03429
Code: https://github.com/cherise215/advchain
- Chained differentiable transforms (deformation, bias field, noise, affine) optimised
  adversarially against the current segmenter. No generative network.
- Cardiac ACDC, one-shot (N=1, M=25 unlabelled): 0.3882 → **0.5861** Dice. Three-shot:
  0.7487 → **0.8083**. Prostate (MSD), three-shot: 0.5486 → **0.6492**; eleven-shot:
  0.6548 → **0.7325**. Low-shot supervised, no unlabelled data, cardiac N=1: 0.5155 → **0.6093**.
- Same catch as 3.4: every headline number is from a 1–11 labelled subject regime.

### 3.6 Generative CT with masks (MAISI) — +1.3 Dice
Guo P, Zhao C, Yang D, Xu Z, Nath V, Tang Y, et al. *MAISI: Medical AI for Synthetic Imaging.*
WACV 2025. arXiv:2409.11169. Code/weights via MONAI
(https://github.com/Project-MONAI/tutorials/tree/main/generation/maisi) and
https://huggingface.co/nvidia/NV-Generate-CT.
- 3D latent diffusion + ControlNet conditioned on segmentation of up to 127 structures, so it
  emits image **and** mask, up to 512×512×768, voxel spacing 0.5–5.0 mm, with organ/tumour size
  control. This is the most capable "generate a labelled CT" system that exists.
- **Downstream: AMOS organ segmentation, 50 synthetic volumes added. Dice 0.876 → 0.889
  (+1.3 points).** The paper states anatomical fidelity remains a constraint.
- For us: 50 volumes and +1.3 points on a well-posed abdominal organ task. It is not evidence that
  a diffusion model can put an L6 where there was none and have a detector learn from it.

### 3.7 GAN/VAE augmentation for vertebral compression fracture classification — large claimed gain, weak design
"Augmenting a spine CT scans dataset using VAEs, GANs, and transfer learning for improved
detection of vertebral compression fractures." Comput Biol Med 2024 (ScienceDirect
S0010482524015312 — the publisher returned 403 to me; **I did not read the full text**).
Reported via secondary sources: real-image test accuracy 73% → 89% (+16 points), F1 0.90; VAE-GAN
had FID ~5× lower than alternatives.
- Related: spine fracture type identification with PGGAN augmentation reaching 93.68% accuracy
  (Sci Rep 2025;15, PMC12022092); a clinical Turing test where three spine surgeons scored 50.13%
  distinguishing synthetic from real fracture CT (Cogent Eng 2023, doi:10.1080/23311916.2023.2295645).
- **Be adversarial.** These are 2D slice-level *classification* tasks on small datasets, the
  baselines are weak (73% accuracy), and I could not verify patient-level separation of the test
  set from the generator's training set. A Turing test passed by surgeons is a realism claim, not
  an anatomical-validity claim, and the literature below shows realism does not predict downstream
  utility. Do not cite the +16 points as evidence for our use case without reading the paper.

---

## 4. The negative results — and they are the stronger literature

### 4.1 Realism does not predict utility
Skandarani Y, Jodoin P-M, Lalande A. *GANs for Medical Image Synthesis: An Empirical Study.*
arXiv:2105.05318 (2021); J Imaging 2023;9(3):69.
- Multi-GAN (DCGAN → style-based), three modalities (cardiac cine-MRI, liver CT, retinal RGB).
  Top GANs reach FID scores that "can fool trained experts in a visual Turing test".
- Conclusion verbatim: **"segmentation results suggests that no GAN is capable of reproducing the
  full richness of a medical datasets."**
- This is the citation for "looks real" ≠ "trains a network". It is directly relevant to our
  validation plan, where "do the DRRs still look like real renders when you look at them" is one
  of four gates — that gate is the weakest of the four and this paper is why.

### 4.2 The cleanest negative numbers: synthetic brain MRI for tumour segmentation
Akbar MU, Larsson M, Blystad I, Eklund A. *Brain tumor segmentation using synthetic MR images —
A comparison of GANs and diffusion models.* Sci Data 2024;11:259.
doi:10.1038/s41597-024-03073-x · PMID 38424097 · PMC10904731.
Data: https://datahub.aida.scilifelab.se/10.23698/aida/synthetic/brgandi (CC BY 4.0).

Dice, trained on synthetic only, tested on real (BraTS 2020; 313 training subjects, 56 test):

| Generator | U-Net | % of real | Swin | % of real |
|---|---|---|---|---|
| Real images (baseline) | 0.729 ± 0.004 | 100 | 0.743 ± 0.008 | 100 |
| Progressive GAN | 0.581 ± 0.026 | 79.7 | 0.607 ± 0.003 | 81.7 |
| StyleGAN 1 | 0.089 ± 0.048 | 12.2 | 0.065 ± 0.004 | 8.7 |
| StyleGAN 2 | 0.678 ± 0.009 | 93.0 | 0.629 ± 0.004 | 84.7 |
| StyleGAN 3 | 0.640 ± 0.041 | 87.8 | 0.603 ± 0.005 | 81.2 |
| Diffusion | 0.730 ± 0.004 | 100.1 | 0.684 ± 0.006 | 92.1 |

- Synthetic-only reaches 80–90% of real-data Dice (one architecture collapses to 9%).
- **The line that matters: "adding synthetic images only provides minor improvements or even
  results in worse performance"** compared with real images alone. Real + synthetic did not
  reliably beat real.
- Same group: diffusion models **memorise** training images (Akbar MU, Wang W, Eklund A, *Beware
  of diffusion models for synthesizing medical images*, arXiv:2305.07644). For us that is a leak
  hazard on top of a utility question — a memorised synthetic copy of a patient is that patient,
  which is the same rule we already apply to warped variants.

### 4.3 Review-level verdict
Chlap P, Min H, Vandenberg N, Dowling J, Holloway L, Haworth A. *A review of medical image data
augmentation techniques for deep learning applications.* J Med Imaging Radiat Oncol
2021;65(5):545–563. doi:10.1111/1754-9485.13261 · PMID 34145766.
Garcea F, Serra A, Lamberti F, Morra L. *Data augmentation for medical imaging: A systematic
literature review.* Comput Biol Med 2023;152:106391. PMID 36549032.
Both conclude the same thing and it is unsatisfying: too many confounds to say which transform
helps which task; the field has not run the controlled experiment. Recent reviews of generative
augmentation specifically report it is "architecture- and ratio-sensitive" and that value
"materialises only when generator coverage, filtering strategy, synthetic ratio, and downstream
model capacity align", with mixed and negative outcomes common.

**What is not known, stated plainly:** there is no published head-to-head, spine, held-out-real,
with-and-without experiment for anatomy-level synthetic augmentation. If we run one, it is new.

---

## 5. The modality-matched positive result — and it did not deform anatomy

Gao C, Killeen BD, Hu Y, Grupp RB, Taylor RH, Armand M, Unberath M.
*SyntheX: Scaling Up Learning-based X-ray Image Analysis Through In Silico Experiments.*
arXiv:2206.06127 → published as *Synthetic data accelerates the development of generalizable
learning-based algorithms for X-ray image analysis*, Nat Mach Intell 2023;5:294–308.
doi:10.1038/s42256-023-00629-1 · PMID 38523605.
Renderer: DeepDRR, https://github.com/arcadelab/deepdrr

- **Hip landmark detection and pelvis segmentation, evaluated on real X-rays:**
  real-data training 8.15 ± 15.30 mm landmark error / 0.759 ± 0.248 Dice;
  **SyntheX synthetic training 6.29 ± 6.29 mm / 0.818 ± 0.221.** Synthetic beat real.
- **From 20 CT scans** (New Mexico Decedent Image Database) they rendered 18,000 training and
  2,000 validation images.
- **The domain randomisation was intensity-only** — Gaussian noise, gamma, cropping, then a
  "strong" tier of inversion, impulse/salt-pepper noise, affine warping, contrast, blur, box
  corruption, dropout, sharpening, pooling, brightness, local distortion. Pose and projection
  variation came from the rendering geometry, not from deforming the patient.
- Also evaluated on surgical tool detection and COVID-19 lung lesion segmentation.

This is the strongest evidence in the file and it points away from anatomical deformation. Twenty
patients' worth of anatomy, rendered thousands of ways, outperformed real data. The bottleneck it
solved was appearance and pose coverage, not anatomical diversity.

Our own measured findings agree: the DRR→fluoro levers we found were fidelity, strong domain
randomisation and scale; CycleGAN and ADDA were refuted; pretrain-on-DRR and film-noise were
refuted; the v5 pseudolabels cost 19 points of anomalous accuracy.

Consistent with this, the newest spine-specific augmentation work is entirely appearance-based:
Molinier N, Möller H, Dagonneau T, Curto-Vilalta A, Graf R, Atad M, Rueckert D, Kirschke JS,
Cohen-Adad J. *One Sequence to Segment Them All: Efficient Data Augmentation for CT and MRI
Cross-Domain 3D Spine Segmentation.* arXiv:2605.03098 (2026, preprint). Intensity inversion,
Scharr filtering, segmentation-driven intensity redistribution, random 3D convolutions, histogram
equalisation, bias field, unsharp masking, random nonlinear functions — **geometry left at nnU-Net
defaults, no anatomical deformation**. Trained on 602 subjects (MM 240 CT, SPIDER 218 MRI, SG 144),
evaluated on seven out-of-distribution sequences: reported average Dice gain of 155% out of domain
for an in-domain Dice decrease of 0.008%, and ~10% faster epochs. Released as an open toolbox for
nnU-Net and MONAI.

---

## 6. The mechanism Greg described already exists, validated — as registration, not augmentation

Worth recording here because it changes the framing of "hacked together".

Arsigny V, Commowick O, Ayache N, Pennec X. *A fast and log-Euclidean polyaffine framework for
locally linear registration.* J Math Imaging Vis 2009;33:222–238. doi:10.1007/s10851-008-0135-9
(earlier: MICCAI/ECCV 2006, LNCS 4057:120–127). Fuses a finite set of rigid or affine components
into a **globally invertible** transformation; the log-Euclidean form fixes the two defects of
earlier polyaffine fusion (inverse not polyaffine, not invariant to change of coordinates).

Gopalakrishnan V, Dey N, Golland P. *PolyPose: Deformable 2D/3D Registration via Polyrigid
Transformations.* arXiv:2505.19256 (2025). https://polypose.csail.mit.edu, CC BY 4.0.
- T̄(x) = exp( Σ w_k(x) log T_k / Σ w_k(x) ), T_k ∈ SE(3) per bone, with a hyperparameter-free
  weight w_k(x) = m_k / (1 + d_k²(x)), m_k the normalised bone volume. Bones stay rigid by
  construction; the field between them interpolates; diffeomorphic by construction.
- Validated: Head&Neck (31 patients), **DeepFluoro (6 cadaveric subjects, real X-rays, 24–111
  images each, 30° viewing cone)**, ThoraxCBCT (13 patients). DeepFluoro with 2 X-rays:
  pelvis 0.99 Dice / 1.00 mm HD95, femurs 0.99 / 1.02 mm and 0.98 / 1.43 mm, and **0% voxels with
  negative Jacobian** versus 0.43–44% for baselines (anatomix 3.01%).
- **It contains no augmentation claim.** Nobody has used a polyrigid field to manufacture training
  spines and measured a downstream gain. That is the gap — and it means the deformation machinery
  can be adopted off the shelf with a citation and a licence, while the *augmentation* claim
  remains ours to earn or refute.

---

## 7. What I would tell the PI

1. **The honest baseline is affine + intensity.** Every spine challenge winner, TotalSegmentator,
   SPINEPS and VERIDAH. nnU-Net removed elastic deformation on purpose. If we ship anything more,
   the paper owes a with/without number on real held-out data, because the field's default is
   "nothing".
2. **The measured gains from anatomy-level synthesis are 1–2 Dice points or ~5% more lesions**
   (MAISI +1.3; SSIM hip +2 and only on top of basic augmentation, zero on its own; anatomy-informed
   prostate +4 lesions of 76, called marginal by its own meta-reviewer). The large gains
   (Zhao, AdvChain) all come from 1–11 labelled subject regimes we are nowhere near.
3. **The best sim-to-real result in our own modality used no anatomical deformation at all.**
   SyntheX beat real-data training from 20 CTs with intensity randomisation and projection
   geometry. Our fallback — pose and projection augmentation — is not a fallback, it is the
   published state of the art, and it has a Nature Machine Intelligence result behind it.
4. **For the transitional vertebra specifically, the only thing measured to work is real rare
   cases plus oversampling.** VERIDAH: 87.80% → 32.93% TEA recall when the labelled anomalies are
   removed. We have 86 transitional subjects. The literature's answer to scarcity here is
   4× oversampling and an anomaly-aware decoder, not synthesis. That is also the cheapest thing
   we have not yet exhausted.
5. **Do not let "the DRRs look right" be a gate.** Skandarani: top GANs pass a visual Turing test
   with experts and still fail to train a segmenter. The only gate that means anything is
   downstream accuracy on real held-out data, and for us on real C-arm frames.
6. **If we do build the warp, the defensible framing is:** adopt log-Euclidean polyrigid
   (Arsigny 2009 / PolyPose 2025) as the deformation model — published, validated, 0% fold-over on
   real fluoroscopy, CC BY 4.0 — bound it by Panjabi's ranges, and then report the augmentation
   result as a **measured, possibly negative** experiment, because nobody has run it.

---

## Sources

- https://pubmed.ncbi.nlm.nih.gov/34340104/ · https://doi.org/10.1016/j.media.2021.102166 · https://arxiv.org/abs/2001.09193
- https://github.com/christianpayer/MedicalDataAugmentationTool-VerSe
- https://github.com/hust-linyi/Seg4Reg · https://arxiv.org/abs/2208.12462
- https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection/writeups/qishen-ha-1st-place-solution · https://pubmed.ncbi.nlm.nih.gov/38169426/
- https://www.kaggle.com/competitions/rsna-2024-lumbar-spine-degenerative-classification/writeups/avengers-1st-place-solution (not readable to me)
- https://arxiv.org/abs/2208.05868 · https://pubs.rsna.org/doi/full/10.1148/ryai.230024
- https://arxiv.org/abs/2402.16368 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11836161/
- https://arxiv.org/abs/2601.14066
- https://github.com/MIC-DKFZ/nnUNet/blob/v1.7.1/nnunet/training/network_training/nnUNetTrainerV2.py · https://github.com/MIC-DKFZ/nnUNet/blob/master/nnunetv2/training/nnUNetTrainer/nnUNetTrainer.py
- https://arxiv.org/abs/2309.03652 · https://github.com/MIC-DKFZ/anatomy_informed_DA · https://conferences.miccai.org/2023/papers/065-Paper1594.html
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10406777/ · https://doi.org/10.1186/s41747-023-00357-6
- https://arxiv.org/html/2511.13883
- https://arxiv.org/abs/1902.09383 · https://github.com/xamyzhao/brainstorm
- https://arxiv.org/abs/2108.03429 · https://github.com/cherise215/advchain · https://pubmed.ncbi.nlm.nih.gov/36095907/
- https://arxiv.org/abs/2409.11169 · https://huggingface.co/nvidia/NV-Generate-CT
- https://www.sciencedirect.com/science/article/pii/S0010482524015312 (403 to me) · https://pmc.ncbi.nlm.nih.gov/articles/PMC12022092/ · https://doi.org/10.1080/23311916.2023.2295645
- https://arxiv.org/abs/2105.05318
- https://www.nature.com/articles/s41597-024-03073-x · https://pmc.ncbi.nlm.nih.gov/articles/PMC10904731/ · https://arxiv.org/abs/2305.07644
- https://onlinelibrary.wiley.com/doi/10.1111/1754-9485.13261 · https://pubmed.ncbi.nlm.nih.gov/36549032/
- https://arxiv.org/abs/2206.06127 · https://www.nature.com/articles/s42256-023-00629-1 · https://github.com/arcadelab/deepdrr
- https://arxiv.org/abs/2605.03098
- https://link.springer.com/article/10.1007/s10851-008-0135-9 · https://arxiv.org/abs/2505.19256 · https://polypose.csail.mit.edu
- https://www.nature.com/articles/s41746-025-02288-5 (Du et al., spine CT domain generalisation: elastic + intensity augmentation, no synthesis; Dice 89.3% vs 88.1%, ID 85.6% vs 79.5%; L1–L5 only, no transitional handling)

---

# Second pass (resumed from checkpoint, 2026-09-23)

The sections above were written in a first pass and several items were left open because a
source would not render. This pass closed four of them, refuted one thing the first pass
implied, and added five studies that carry the numbers the angle actually asks for. Where an
item below contradicts something above, this section is the later reading.

---

## 8. Corrections to section 1

### 8.1 Payer DID use elastic deformation — the parameters, verbatim

The first pass could not read the VISAPP paper and said the parameters were "in the repo's
config files". They are, and they are now read. `verse2020/dataset.py` in
https://github.com/christianpayer/MedicalDataAugmentationTool-VerSe (the VerSe'19 winner's
released code; `verse2020/training/dataset.py` is a symlink to it):

- `translation.Random(dim, [random_translation]*dim)` — **30 mm** per axis
- `rotation.Random(dim, [random_rotate]*dim)` — **0.25 rad** (~14.3°) per axis
- `scale.RandomUniform(dim, random_scale)` and `scale.Random(...)` — **0.15**
- `flip.Random(dim, [0.5, 0, 0])` — p=0.5, one axis
- `deformation.Output(dim, [6, 6, 6], [random_deformation]*dim, ...)` — **6×6×6 control-point
  grid, 25 mm magnitude**
- intensity: `random_intensity_shift` 0.25, `random_intensity_scale` 0.25, gamma
  `float_uniform(0.9, 1.1)`

So the honest form of the headline is **not** "the winners used no deformation". It is: the
VerSe'19 winner used a *random* B-spline deformation on a coarse grid (25 mm is large — of the
order of a vertebral body), nnU-Net turned its own random elastic deformation off, and **neither
of them generated or deformed anatomy in a way that respects what a spine can do**. Random
elastic on a 6×6×6 grid is free to fold a pedicle into a lamina; it is not a population-plausible
sample. The distinction the manuscript needs is *random deformation* versus *anatomically
constrained deformation*, not *no deformation* versus *deformation*.

### 8.2 RSNA 2024 Lumbar, 2nd place — read; 1st place still unread

Kaggle serves me the page title only for the 1st-place (Avengers) writeup; after four attempts
it is still unread, and I am not guessing it. The 2nd-place solution is public in full:
https://github.com/brendanartley/RSNA-2024-Competition — two-stage sagittal pipeline, augmentation
is sequence-order flipping, combining left/right sides from different sequences, **manifold mixup
on the embeddings**, nine-angle rotation TTA, plus confident-learning label denoising.
**No synthetic or generated data.**

### 8.3 VerSe'20 winner (Chen D.) — method still not publicly documented

Searched again. The benchmark paper does not report it, no method paper is indexed, no repository
is linked. **Not known**, and nothing in the record fills it.

### 8.4 Molinier 2026 ablation — the number the first pass did not have

"One Sequence to Segment Them All" (arXiv:2605.03098) Table 5, training on synthetic-ground CT
and testing on synthetic-ground water images: **best single transformation 0.27 Dice
(RedistributeSeg alone) versus 0.71 with all augmentations combined.** Out-of-domain average
Dice gain 155%, in-domain change −0.008%. CT→MRI transfer reaches ~85% of in-domain MRI
performance, MRI→CT ~91%. Trained on 144 subjects, 80/10/10 subject-wise. The authors state
explicitly that "standard geometric transformations (e.g. rotations and flips) and other baseline
augmentations … are kept with the same configuration as the normal nnUNet trainer" — **all of
that 155% is appearance, none of it is anatomy.** The synergy result is worth carrying: no single
transform did much; the stack did everything.

---

## 9. The strongest new evidence: a challenge WAS won with generative augmentation — and the
## same group's next paper shows it made the ensemble worse

This is the most important addition, because it is the counterexample to "challenge winners use
nothing", and it comes with its own refutation.

Ferreira A, Magalhães R, Jesus T, Puladi B, Kleesiek J, Alves V, Egger J. *How we won BraTS 2023
Adult Glioma challenge? Just faking it! Enhanced Synthetic Data Augmentation and Model Ensemble
for brain tumour segmentation.* arXiv:2402.17317v2 (MICCAI BrainLes 2023 proceedings).

- **Winner of BraTS 2023 Task 1.** Three synthesis strategies feeding three architectures
  (nnU-Net, Swin UNETR, the BraTS'21 winner's net): **G** = GliGAN, a Swin-UNETR-generator GAN
  that paints synthetic tumours into healthy brain at random locations; **rG** = a second GAN
  that first generates synthetic *labels* (64³) which GliGAN then renders; **R** = synthesis by
  registration between subjects.
- Validation set, legacy DSC mean: GAN ensemble 0.8853, label-GAN ensemble 0.8850, all-models
  0.8842, registration ensemble 0.8772. **The 2022 winner scored 0.8821 and the 2021 winner
  0.8836 on the same set.** The winning margin over the previous two years' winners is
  **0.0006–0.0017 Dice**.
- **Be adversarial, and this is the point: Table 1 contains no model trained without synthetic
  data.** Every row is SG, SrG or SR. The paper therefore reports no with/without ablation and
  cannot attribute any of its result to the synthesis. A challenge win is not a measurement.

Ferreira A, Jesus T, Puladi B, Kleesiek J, Alves V, Egger J. *Improved Multi-Task Brain Tumour
Segmentation with Synthetic Data Augmentation.* arXiv:2411.04632 (BraTS 2024: winner of Task 1,
third in Task 3). **This one does run the ablation, and it goes the other way.**

Task 1 validation, both ensembles at identical thresholding (0,0,0,0):

| Ensemble | ET | NETC | RC | SNFH | TC | WT |
|---|---|---|---|---|---|---|
| **All real** (models trained on real data only) | 0.7506 | 0.7715 | **0.7050** | **0.8715** | 0.7366 | **0.8759** |
| **All fake** (models trained on real + synthetic) | 0.7416 | **0.7764** | 0.6826 | 0.8278 | 0.7327 | 0.8381 |

**Adding synthetic data made the ensemble worse on five of six regions** — SNFH −0.044,
WT −0.038, RC −0.022 — and better on one (+0.005). The submitted entry was the ensemble of
everything (0.7557 / 0.7868 / 0.7053 / 0.8704 / 0.7500 / 0.8734), i.e. the gain came from
ensembling real-trained and synthetic-trained models together, not from the synthetic data.

The authors' own diagnosis, verbatim, is the sentence this project should paste into its methods
section: *"The models trained with synthetic data, when tested individually, have a lower number
of FN, however a considerably higher number of FP which heavily penalises the results. The random
generation of synthetic tumours anywhere in the brain might therefore potentially make the
training process for the segmentation very unstable and the model very prone to FP, as too many
non-existent tumours are predicted."*

And the flip side, from the same paper's Task 3, where the metric does **not** penalise false
positives: the synthetic-trained MedNeXt was the best single model (DSC 0.8214 vs 0.8032 for its
real-trained twin), *because* "the randomness of the locations where the synthetic tumour was
located made the network more sensible and robust, avoiding FN".

**Read this straight across to us.** Manufacturing a rare structure and putting it where it does
not belong buys recall of the rare class and pays for it in precision. Whether that trade is a
gain or a loss is decided entirely by whether the metric punishes false positives. For a
level-naming product where a false L6 call is the failure mode we are trying to prevent, the
BraTS Task 1 column is the relevant one, and it is negative.

Test-set numbers for completeness (organisers' evaluation, BraTS 2024 Task 1): ET 0.7900,
NETC 0.8076, RC 0.7760, SNFH 0.8926, TC 0.7874, WT 0.8938.

---

## 10. The one spine-and-X-ray downstream result, read in full

Rangwani/— (authors not resolved from the PMC render; cite by DOI). *Synthetic cervical spine
radiographs: expert validation and transfer learning for low-data settings.* BMC Med Inform Decis
Mak 2026. doi:10.1186/s12911-026-03479-0 · PMC13185266 · companion preprint arXiv:2510.22166.

- DDPM trained on the **Cervical Spine X-ray Atlas (CSXA), 4,963 lateral cervical radiographs**
  (the same CSXA this project already uses); released synthetic set **20,063 radiographs** after
  manual review. Images at 256×256.
- Labels for the synthetic images are **pseudolandmarks**: a heatmap-regression detector trained
  on real CSXA annotations was run over the synthetic set, and "no manual or algorithmic
  quality-control filtering of the pseudolandmarks was applied".
- Expert validation: eight clinicians (six neuroradiologists, two neurosurgeons) picked the real
  image in **29.0%** of trials (below chance), Fleiss' κ **0.061**; realism ratings 3.323 real vs
  3.228–3.320 synthetic, not significantly different.
- **Downstream, on the external CLX-34 test set (n=374), landmark-localisation MSE, synthetic-
  pretrained-then-fine-tuned vs de novo, by size of the real training set:**

| real training images | synthetic-pretrained | de novo |
|---|---|---|
| 100 | **31.78** | 84.33 |
| 200 | **12.97** | 55.84 |
| 300 | **10.10** | 34.30 |
| 400 | **9.74** | 27.21 |
| 500 | **7.49** | 14.17 |
| 600 | 8.56 | **7.42** |
| 700 | **4.37** | 7.42 |

- This is the only result I found where a spine-specific generative pipeline is measured
  downstream on real held-out data, and the advantage is largest where real labels are scarcest —
  the same shape as every other result in this file.
- **Be adversarial.** (i) **No repeated runs, no seeds, no confidence intervals, no statistical
  test** — every cell is a single point estimate. (ii) The curve is not monotone: de novo wins at
  600 and then fails to improve at all from 600 to 700 (7.42 both times), which is the signature
  of run-to-run noise larger than the effect at the right-hand end. The "still helps at full data"
  claim rests on one unreplicated pair. (iii) The synthetic labels are pseudolabels from a
  detector trained on the same real data, so the pipeline cannot add label information the real
  set did not already carry. (iv) It generates 2-D radiographs, not labelled 3-D anatomy, so it
  does not meet the requirement at the top of this brief. (v) The authors state manual review was
  still needed to exclude anatomically implausible synthetic images — i.e. the generator does
  fabricate anatomy that does not occur, and a human caught it.

---

## 11. Synthesis of the anatomy itself (label maps), measured both ways

### 11.1 brainSPADE — synthetic labels + synthetic images, full Dice tables

Fernandez V, Pinaya WHL, Borges P, Tudosiu P-D, Graham MS, Vercauteren T, Cardoso MJ. *Can
segmentation models be trained with fully synthetically generated data?* SASHIMI @ MICCAI 2022,
LNCS 13570:79–90. arXiv:2209.08256. Code: https://github.com/virginiafdez/brainSPADE_MICCAI
(the repo link is given in the paper; I did not verify its licence).

Mechanism, and it is exactly the shape of what this project is contemplating: a **latent
diffusion label generator** (VAE + LDM) samples synthetic partial-volume *anatomy maps* — the
anatomy is generated, not deformed — and a SPADE-style VAE-GAN then renders an image in an
arbitrary style conditioned on that map. Lesions are conditioned on, so the rare class can be
balanced by construction. Segmenter: 2D nnU-Net, default parameters. All models tested on **real**
data.

| experiment | trained on real | trained on synthetic |
|---|---|---|
| In-distribution healthy tissue (SABRE, 25 holdout volumes) CSF / GM / WM | **0.953 / 0.952 / 0.965** | 0.919 / 0.925 / 0.945 |
| Near-OoD (ABIDE T1, 25 volumes) CSF / GM / WM | 0.782 / 0.774 / 0.652 | 0.825 / 0.881 / 0.873 |
| Far-OoD (OASIS FLAIR, 25 volumes) CSF / GM / WM | 0.711 / 0.531 / 0.447 | 0.736 / 0.592 / 0.433 |

Style-conditioned synthetic training (using unpaired target-domain images only as style) reaches
0.841 / 0.895 / 0.891 near-OoD and 0.792 / 0.784 / 0.809 far-OoD, against 0.914 / 0.971 / 0.973
and 0.830 / 0.826 / 0.862 for models trained on five *paired* real volumes from the target — so
synthetic closes most, never all, of the gap.

Tumour segmentation (BRATS holdout sites, 30 test volumes), and this is the row that matters:

| | real only (5 subjects, 1,064 slices) | synthetic only (20,000 slices) | **real + synthetic** |
|---|---|---|---|
| Dice on tumour | 0.813 ± 0.174 | 0.760 ± 0.187 | **0.876 ± 0.094** |
| Recall | 0.773 ± 0.209 | 0.713 ± 0.238 | **0.852 ± 0.137** |

**+6.3 Dice points and +7.9 recall points from adding synthetic data to real, significant on
recall.** It is the cleanest positive hybrid result in this file. Caveats, stated: the real arm
is five subjects, the synthetic label generator was trained on the same institution's data, the
task is 2-D slice-wise, and in-distribution the synthetic arm *lost* significantly (p<0.05) on
every tissue class.

### 11.2 SynthSeg — the industrial version, and what it says about anatomical variability

Billot B, Greve DN, Puonti O, Thielscher A, Van Leemput K, Fischl B, Dalca AV, Iglesias JE.
*SynthSeg: Segmentation of brain MRI scans of any contrast and resolution without retraining.*
Med Image Anal 2023;86:102789. doi:10.1016/j.media.2023.102789 · PMC10154424 · arXiv:2107.09559.
Code https://github.com/BBillot/SynthSeg, shipped inside FreeSurfer.

- Training images are generated from **520 label maps** (20 T1-39, 500 HCP, 500 ADNI — the paper's
  own count) by: affine transform, **diffeomorphic non-linear deformation from a stationary
  velocity field**, GMM intensity sampling, bias field, gamma, and blur/downsample/resample to
  simulate resolution. Anatomy comes from real label maps; the *variation* in anatomy is the
  random diffeomorphic warp. Evaluated on **5,000 scans, 8 datasets, 6 modalities (incl. CT),
  10 resolutions**.
- Dice: SynthSeg 0.88 / 0.84 / 0.87 (T1-39 / ADNI / T1mix) versus a supervised T1 CNN
  0.91 / 0.83 / 0.86 — i.e. it matches supervised training *in* domain and generalises across
  modality without retraining, which supervised CNNs do not.
- **The line relevant to our rare-anatomy problem:** adding automated label maps from different
  populations improved robustness, worth **4.7 Dice points on highly atrophied ADNI subjects** —
  the atypical-morphology subgroup. That is the closest published analogue to "put more variant
  anatomy in the pool and the variant cases improve", and it came from *more real label maps*,
  not from a generative model inventing morphology.

### 11.3 anatomix — synthesis with no real images at all

Dey N, Billot B, Wong HE, Wang CJ, Ren M, Grant PE, Dalca AV, Golland P. *Learning General-Purpose
Biomedical Volume Representations using Randomized Synthesis.* ICLR 2025. arXiv:2411.02372.
Code https://github.com/neel-dey/anatomix.

- Pretrains a 3D U-Net contrastively on synthetic volumes assembled from ~45,000 binary organ
  volumes from **TotalSegmentator**, randomly sampled as templates, deformed, and assigned random
  intensities and artefacts. No real images in pretraining.
- Few-shot segmentation, 1–3 labelled volumes, Dice (ours / random init / Models Genesis / SMIT):
  MSD-Heart .89/.85/.84/.88 · PROMISE12 .85/.80/.73/.72 · L2RAb-MRI .86/.85/.81/.84 ·
  FeTA .80/.78/.79/.76 · AMOS-CT .61/.56/.55/.58 · WUFetal .76/.73/.66/.73.
- **Gain over random init is 1–5 Dice points, at 1–3 labelled volumes.** Same regime caveat as
  Zhao and AdvChain. It is also the strongest existence proof that synthetic *shape* variation
  transfers — and note what it implies: the useful signal was generic shape statistics, not
  correct anatomy, since the synthetic volumes are not anatomically valid at all.

### 11.4 AnyCXR — CT-rendered X-rays, our exact rendering setup, no anatomical randomisation

*AnyCXR: Human Anatomy Segmentation of Chest X-ray at Any Acquisition Position using Multi-stage
Domain Randomized Synthetic Data…* arXiv:2512.17263 (2025 preprint, authors not resolved).

- **2,982 CT scans → 126,410 synthetic radiographs** across PA, lateral and oblique views, 54
  structures, evaluated zero-shot on real ChestX-ray14 / CheXpert / MIMIC-CXR / Shenzhen with
  40 expert-refined radiographs.
- Ablation, mean DSC: plain baseline 91.62 (PA) / 85.98 (LA) → post-hoc 2-D augmentation 93.75 /
  89.16 → MSDR only 94.03 / 87.60 → **full 94.53 / 91.35**.
- **Every randomised term is attenuation, geometry or detector response** — bone-to-soft-tissue
  attenuation scaling, inter- and intra-bone attenuation, soft-tissue attenuation with polarity
  inversion, SDD/ODD drift ±10%, noise, window/level. **Nothing deforms the patient.** This is
  SyntheX's recipe at 150× the scale, in 2025, and it still contains no anatomical variation.

---

## 12. Two more measured-augmentation anchors

- **BigAug.** Zhang L, Wang X, Yang D, Sanford T, Harmon S, Turkbey B, Wood BJ, Roth H, Myronenko
  A, Xu D, Xu Z. *Generalizing Deep Learning for Medical Image Segmentation to Unseen Domains via
  Deep Stacked Transformation.* IEEE Trans Med Imaging 2020;39(7):2531–2540. PMID 32070947.
  Nine stacked transforms (intensity, noise, blur, sharpen, rotation, scaling, deformation),
  three tasks (prostate, left atrium, left ventricle), eight public datasets. **Dice degradation
  from source domain to unseen domain: 11% with BigAug, 39% with conventional augmentation, 25%
  for CycleGAN domain adaptation.** Augmentation beat a generative domain-adaptation method by
  14 points of degradation. Still random deformation, not anatomy.
- **Kaggle RSNA 2022 cervical fracture, 1st place**, already in §1: mixup was the only unusual
  ingredient. Nothing generative.

---

## 13. What the second pass changes in the recommendation

The first pass's six points stand. Three things are now sharper:

1. **Stop saying "the winners used no deformation".** Say: the winners used *random* affine,
   intensity and (in Payer's case, 6×6×6 grid, 25 mm) elastic deformation; nnU-Net dropped its
   elastic term; and **nobody in the spine literature has used anatomically constrained
   deformation or generated anatomy at all**. The gap is real, but it is narrower and better
   defined than "nobody deforms anything".
2. **There is now one challenge won with generative augmentation, and its own sequel measures the
   effect as negative on five of six regions.** BraTS 2023/2024, same group. If the manuscript
   cites the win, it must cite the ablation, and the FP/FN mechanism the authors give is precisely
   the risk of manufacturing L6s: recall up, precision down, and the sign of the net effect is set
   by whether the metric penalises false positives. Ours does.
3. **The one positive hybrid result with a real ablation is brainSPADE** (+6.3 Dice on tumour from
   real+synthetic over real alone, with synthetic-alone *worse* than real alone), and it worked by
   generating the **label map** — the anatomy — with a diffusion model and conditioning on the rare
   class. That is the closest published thing to what this project would build. It was measured on
   five real subjects in the real arm, in 2-D, in brain MRI. Nobody has done it in 3-D bone, and
   nobody has done it for a structure whose identity is defined by its position in a chain.

**Still not known after two passes:** the RSNA 2024 Lumbar 1st-place augmentation; the VerSe'20
winner's method; the exact Dice table of Zhao et al. CVPR 2019 (both the CVF PDF and the RSNA
site return 403 to this session); and the full text of the Comput Biol Med 2024 VAE/GAN vertebral
fracture paper. None of these is quoted above beyond what was actually read.

---

## Sources added in the second pass

- https://github.com/christianpayer/MedicalDataAugmentationTool-VerSe/blob/master/verse2020/dataset.py
- https://github.com/brendanartley/RSNA-2024-Competition
- https://arxiv.org/abs/2402.17317 · https://arxiv.org/abs/2411.04632
- https://pmc.ncbi.nlm.nih.gov/articles/PMC13185266/ · https://doi.org/10.1186/s12911-026-03479-0 · https://arxiv.org/abs/2510.22166
- https://arxiv.org/abs/2209.08256
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10154424/ · https://arxiv.org/abs/2107.09559 · https://github.com/BBillot/SynthSeg
- https://arxiv.org/abs/2411.02372 · https://github.com/neel-dey/anatomix
- https://arxiv.org/abs/2512.17263
- https://pubmed.ncbi.nlm.nih.gov/32070947/ · https://ieeexplore.ieee.org/document/8995481/
- https://arxiv.org/html/2605.03098 (ablation table 5)
