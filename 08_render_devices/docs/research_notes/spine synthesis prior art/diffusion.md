# Anatomically-conditioned deep generative CT synthesis — prior art

Angle: diffusion / GAN models that generate 3-D CT under a mask or label condition. Question asked of
every paper: could it take our per-vertebra label map, let us EDIT it (insert an L6, sacralise an L5),
paint a CT that obeys the edit, and survive DRR casting well enough to train a C-arm detector?

First pass 2026-09-23. **Second pass 2026-09-23 (resumed from checkpoint)** closed five of the six
open items and changed the conclusion. All numbers below are the authors' own; where a number is not in
the paper I say so rather than estimating it.

---

## Bottom line first (REVISED on the second pass)

1. **No spine-specific anatomically-conditioned 3-D CT generative model exists.** Unchanged after a
   second sweep. Searches for a vertebra-mask-conditioned CT generator return segmentation papers,
   MR→CT translation, and X-ray→CT reconstruction. The nearest bone-specific conditional generator is
   trabecular *microstructure* at micro-CT scale (candidate 11), two orders of magnitude off our scale.

2. **The edited-mask question is no longer untested — it was tested and it FAILED.** This is the
   headline change from the first pass, which recorded it as open. seg2med (candidate 2) conditioned
   its CT generator on a composite "Frankenstein" mask built by merging segmentations and body contours
   from three different patients. FSIM fell to **0.45 ± 0.02** against **0.82 ± 0.08** for real-patient
   masks, and the authors state plainly that the image synthesised from the merged phantom does not
   preserve realistic anatomy. A mask-conditioned diffusion model handed anatomy that does not occur in
   its training population painted something that is not anatomy. That is our exact use case, run, with
   a negative result. MedSyn2 (candidate 5) shows the weak version working — translate or flip a
   *nodule* mask and the CT follows — but that is moving an existing blob inside a lung, and the
   evidence is one qualitative figure, no number.

3. **MAISI's mask faithfulness on BONE has now been measured by a third party, and it is 15.20 Dice.**
   Foundation VAE (candidate 4) segmented MAISI's synthesised volumes with VISTA3D/TotalSegmentator and
   scored them against the conditioning masks: lung 75.94, heart 66.86, **vessel 13.50, rib 15.20**
   (IoU 8.88). Thin structures are not followed at all. Put beside Konz's head-to-head, where a
   ControlNet scored **0.1132 Dice on CT** against segmentation-guided diffusion's 0.8980, there are now
   two independent measurements saying that ControlNet-style conditioning of a CT diffusion model
   ignores bone. The first pass flagged "MAISI's controllability is asserted, not measured" as a gap;
   it is now measured, by someone else, and it fails on exactly the structure we care about.

4. **The one paper that ran our experiment end to end found the 3-D-generative route LOST** — generate
   CT with a diffusion model, cast DRRs, train an interventional X-ray model, test on real fluoroscopy,
   on the DeepFluoro specimens we already use (candidate 3). Unchanged, and now better explained: the
   generator whose DRRs lost is exactly the sort of model whose bone adherence measures 15.

5. **Bone is almost never the evaluated structure, and where it is, it is the worst one.** MAISI: no
   bone number in its own paper, 15.20 from outside. GuideGen: image–mask DSC 0.61 overall. Killeen:
   0.727 ± 0.115 over 16 merged classes. seg2med is the only paper in this literature that publishes a
   **per-vertebra** number, and its lumbar spread is L1 0.74 ± 0.31, L2 0.80 ± 0.18, L3 0.91 ± 0.00,
   **L4 0.72 ± 0.02** — on a 2-D model, on real-patient masks, with no L5 reported at all.

6. **Net read for the project: this angle is weaker than the first pass recorded, and the cheap
   decisive test is now a cheap confirmatory test.** It is still worth one day, because MAISI is
   downloadable and the number would be ours, but the prior is now quantified and it is bad.

---

## Candidate 1 — MAISI / NV-Generate-CT (NVIDIA + MONAI). Still the lead, now with a bad number attached.

Guo P, Zhao C, Yang D, et al. *MAISI: Medical AI for Synthetic Imaging.* WACV 2025. arXiv:2409.11169.
MAISI-v2: Guo P, et al. *MAISI-v2: Accelerated 3D High-Resolution Medical Image Synthesis with
Rectified Flow and Region-specific Contrastive Loss.* arXiv:2508.05772 (Aug 2025).
Code https://github.com/NVIDIA-Medtech/NV-Generate-CTMR and
https://github.com/Project-MONAI/tutorials/tree/main/generation/maisi (CC BY 4.0).
Weights https://huggingface.co/nvidia/NV-Generate-CT

**Generates.** Full 3-D CT volume *and* a paired segmentation mask, up to 512 × 512 × 768 voxels, voxel
size selectable 0.5–5.0 mm, six body regions including pelvis. v1 latent DDPM; v2 latent rectified
flow, ~33× faster.

**Control — and a correction to the first pass.** The first pass wrote that "the interface we would
need literally exists in the released code". That is half right and the distinction matters. The
packaged NV-Generate-CT model card describes conditioning by **body region + an optional anatomy class
list (127 classes) + controllable sizes for 10 organs** (liver, gallbladder, stomach, pancreas, colon,
lung tumour, bone lesion, hepatic tumour, colon cancer, pancreatic tumour) — no vertebra among the ten —
and states the model "does not require an organ/label mask as input; it generates them as output". The
dense-mask-in interface lives in the **ControlNet** path of the MONAI tutorial, which does take a label
volume and is documented as fine-tunable on new classes. The label dictionary
(`configs/label_dict.json`, 132 entries) does contain `vertebrae L5 … C1`, `vertebrae S1`, `sacrum`,
`left/right rib 1–12`, `left/right hip`, `left/right femur`, `spinal cord`. So the interface exists, but
in the auxiliary path, not the headline pipeline. **Verify by running it before quoting it.**

**Data.** VAE 37,243 CT + 17,887 MRI. Diffusion 10,277 CT from 24 public datasets. ControlNet 6,330 CT
(5,058 train / 1,272 val) over 20 datasets. v2 reports "over 107k images generated from 11k scans".

**Validation.**
- Realism v1: FID 6.083 vs DDPM 22.608 and LDM 12.379; chest FID 4.349–8.346 vs HA-GAN 98.064–116.260.
  VAE reconstruction LPIPS 0.038–0.046, SSIM 0.970–0.978, PSNR 36.6–39.0 dB.
- Realism v2: FID_avg 2.322 on AutoPET2023 OOD at 512³ vs MAISI-DDPM 2.441 and MAISI-DDIM 4.776.
- Anatomy in the generated image (v1, authors' own): VISTA3D on synthetic gives liver Dice 0.93 vs 0.95
  real; paper concedes a "more pronounced performance gap … for smaller organs".
- **Mask adherence, measured by a third party (Foundation VAE Table 4, 80 test volumes): lung 75.94,
  heart 66.86, vessel 13.50, rib 15.20 Dice.** Neither MAISI paper reports a mask-adherence number of
  its own; v2 substitutes downstream segmentation deltas. No vertebra number exists anywhere.
- No reader study in either paper.
- Downstream: v1 tumour segmentation via Auto3DSeg +2.5 % to +4.5 % DSC over five tumour types
  (mean +4 %), inpainting variant +6.5 %. v2 5-fold CV: liver tumour 0.695 Dice (+3.3 % over real-only),
  pancreatic 0.497 (+6.4 %), plus colon, lung and an in-house **bone-lesion** set at 0.537. Authors'
  rule of thumb: synthetic set the same size as the real set. **All gains are lesion segmentation.
  None is bone anatomy, none is detection, none is 2-D.**

**Compute.** v1 inference 48–87 s per 512³; peak 22.8–45.3 GB reported by the tutorial; bundle card
≥58 GB for 512³ inference, ≥60 GB training; HF card 80 GB A100/H100 for 512³. v2 at 512³ with 30 steps
on an H100: 6 s LDM + 15 s VAE decode = 21 s; 80 GB training, 40 GB inference.

**Licence.** Tutorial code CC BY 4.0 / Apache 2.0. Weights under the NVIDIA Open Model License
Agreement; the model card states "intended for research purposes only and not for clinical usage".
Commercial terms sit in https://docs.nvidia.com/ai-foundation-models-community-license.pdf — **still not
read by me.** For the 510(k) track this needs a lawyer, not a subagent.

**Fit.** Best available on interface and availability; worst-in-class on the one number that decides it.
Rib adherence 15.20 is not a tuning problem, it is a "does not follow the mask" problem.

---

## Candidate 2 — seg2med (Yang et al. 2025). NEW on the second pass. The only paper that conditioned on artificial anatomy, and the only per-vertebra numbers in the field.

Yang Z, et al. *seg2med: a bridge from artificial anatomy to multimodal medical images.* Phys Med Biol
2025;70(24), DOI 10.1088/1361-6560/ae2738 (published 15 Dec 2025). Preprint arXiv:2504.09182 (CC BY
4.0). Demo https://huggingface.co/spaces/Zeyu0601/frankenstein — **no GitHub repository and no
downloadable weights that I could find.**

**Generates.** CT and MR (GRE, SPACE, VIBE) conditioned on an anatomical mask. **2-D, slice by slice**,
1.0 × 1.0 mm² axial. The authors themselves write that "the reliance on 2D image generation leads to
non-smooth reconstructions across sagittal and coronal planes" — which is disqualifying for DRR casting
for the same reason SegGuidedDiff is.

**Control.** Conditional DDPM, two-channel input z_t = concat(x_t, y) with y the anatomical prior;
Diffusion-UNet backbone, 500 timesteps, 300 epochs, Adam 2e-4, batch 8 on A6000. Masks come from
TotalSegmentator, **up to 117 classes, with per-vertebra classes present** (Vertebrae L1 … T12 appear
in their Table VII, alongside ribs, scapula and sternum).

**The three mask sources — this is why the paper matters to us.**
- Real patient masks.
- **XCAT digital phantoms**: 56 adults (33 M / 23 F), heights 153–186.4 cm, weights 52–120 kg, ages
  18–78. Mean FSIM **0.78 ± 0.04**, most above 0.75. A phantom is anatomy the model never saw as an
  image, and it worked.
- **"seg2med-assembled" composite anatomy**: one phantom built by merging segmentations and body
  contours from three different patients. FSIM **0.45 ± 0.02** against 0.82 ± 0.08 for real-patient CT,
  and the paper states the synthesised image does not preserve realistic anatomy.

  Read that pair carefully, because it is the most informative result on this angle. A *coherent*
  synthetic anatomy (XCAT, built by anatomists to be self-consistent) is painted well. An *incoherent*
  one (organs from different people stitched together) is not. An inserted L6 is somewhere between the
  two: it is a real anatomical phenotype, but the mask we would hand the model is an edit, and whether
  the edit reads as coherent to the model is exactly what is untested. The one data point we have says
  the failure mode is real and the metric drops by half when the mask stops being self-consistent.

**Validation.** CT: SSIM 0.94 ± 0.02, FSIM 0.78 ± 0.04 (XCAT), FID 3.62, PSNR 27.58 ± 3.48. MR: SSIM
0.89 ± 0.04 (SynthRAD) but 0.56 ± 0.07 (M2OLIE), FID 4.64 / 36.66. Modality conversion SSIM 0.91
(MR→CT), 0.77 (CT→MR). Baselines: Attention-UNet, Pix2Pix, CycleGAN.
**Anatomical fidelity, TotalSegmentator re-read of the generated CT, 58 test cases: Dice > 0.90 for 11
organs, > 0.80 for 34 of 59.** Per-bone (their Table VII):

| structure | Dice |
|---|---|
| Vertebrae L1 | 0.74 ± 0.31 |
| Vertebrae L2 | 0.80 ± 0.18 |
| Vertebrae L3 | 0.91 ± 0.00 |
| Vertebrae L4 | 0.72 ± 0.02 |
| Vertebrae T6 | 0.69 ± 0.00 |
| Vertebrae T7 | 0.58 ± 0.36 |
| Vertebrae T8 | 0.74 ± 0.18 |
| Vertebrae T9 | 0.88 ± 0.07 |
| Vertebrae T10 | 0.92 ± 0.05 |
| Vertebrae T11 | 0.91 ± 0.03 |
| Vertebrae T12 | 0.89 ± 0.14 |
| Rib left 11 | 0.90 ± 0.06 |
| Rib left 12 | 0.88 ± 0.02 |
| Scapula right | 0.96 ± 0.01 |
| Sternum | 0.72 ± 0.25 |

No L5, no sacrum, no hip, no femur in the reported table. Adversarially: the SDs are enormous
(L1 ± 0.31, T7 ± 0.36), several levels are single-case (± 0.00), and this is the *best-case* condition —
a real patient's own mask, re-read by the same tool that made it. At L4 = 0.72 no level-naming or
end-plate morphometry can ride on this output.

**Data.** SynthRAD2023 Pelvis 170 train / 10 test CT; internal abdomen 153 train / 10 test; M2OLIE 48
test CT; XCAT 56. Totals 323 CT train / 59 CT test. Small.

**Downstream gain.** **None measured.** Experiment V checks anatomical consistency only; no segmentation
or detection model was trained on the output. No DRR, no projection, anywhere in the paper.

**Fit.** Wrong dimensionality, small fit, no weights — unusable as a tool. Indispensable as evidence:
it is the only paper that ran the edited-anatomy experiment, and the only one that publishes
per-vertebra fidelity. Both of its answers are discouraging.

---

## Candidate 3 — the decisive negative: DiffCT-DRR vs 2-D X-ray diffusion (Rapuri et al. 2026).

Rapuri S, Ko J, Killeen BD, Taylor RH, Unberath M. *2D Versus 3D Diffusion for In Silico Training of
Interventional X-ray AI Models.* arXiv:2606.21414 (19 Jun 2026), CC BY 4.0.

The experiment this workflow is contemplating, already run, by the DeepFluoro group, on DeepFluoro
(366 fluoroscopic frames, 6 cadaveric specimens; segmentations of semi-pelves, sacrum, femurs,
**vertebrae**). Four training-data sources for pelvic landmark detection, tested on **real** X-rays:

| source | precisely matched, ℓ₂ mm | specimen 6, ℓ₂ mm |
|---|---|---|
| RealXray (real films) | 4.89 ± 6.42 | 4.38 ± 1.84 |
| RealCT-DRR (real CT → DRR) | 7.83 ± 25.67 | 4.37 ± 2.08 |
| **DiffCT-DRR (generated CT → DRR)** | **5.82 ± 13.72** | **8.00 ± 10.80** |
| DiffXray (2-D X-ray diffusion) | 4.40 ± 1.87 | 4.84 ± 1.45 |

Generated-CT→DRR is worst of four on the held-out specimen; the 2-D route matches real films. Authors'
stated reason: "there are few models available for CT image synthesis, conditional or otherwise, and the
model from Killeen et al. has limited spatial resolution and conditioning signal." No FID, no reader
study, no quantitative realism metric for the DRRs — realism is judged only through downstream error.
Six synthetic CTs in the matched comparison; no code release stated.

**Read for us.** It used an *unconditional*, 3 mm-slice generator, so it does not close the question for
a mask-conditioned 1 mm one. But anyone proposing generated CT → DRR for C-arm work has to answer this
table, and candidate 1's rib Dice of 15.20 suggests the conditional version would not rescue it.

---

## Candidate 4 — Foundation VAE (Chen et al., ICML 2026). NEW weight on the second pass: the source of the MAISI bone number.

Chen Q, Ding S, Gu Y, et al. *Foundation VAEs for 3D CT Reconstruction, Augmentation, and Generation.*
ICML 2026; arXiv:2605.30893. Code and demo https://github.com/qic999/Foundation-VAE.

**Generates.** 3-D CT, 512 × 512 per slice, 100–600 slices, intensities clipped to [−1000, 1000] HU,
from a conditional latent diffusion model built on a frozen natural-image/video VAE latent space.

**Control.** Whole-body anatomical mask (VISTA3D + TotalSegmentator, **126 classes**) injected by
concatenating a mask embedding z_m with the noised latent z_t along the channel dimension — i.e. the
SegGuidedDiff-style mechanism rather than a ControlNet. Trained on 4,961 volumes (CT-RATE +
ReXGroundingCT overlap); evaluated on 80 test volumes over 18 disease categories.

**Validation — the table that matters.** Organ-mask adherence, pre-trained segmenters re-read on
synthesised volumes:

| structure | MAISI Dice / IoU | Foundation VAE Dice / IoU |
|---|---|---|
| Lung | 75.94 / 62.97 | 79.48 / 75.46 |
| Heart | 66.86 / 52.20 | 80.36 / 77.09 |
| Vessel | 13.50 / 7.27 | 63.38 / 48.11 |
| **Rib** | **15.20 / 8.88** | **70.23 / 61.40** |

Also +3.9 % NSD on pancreatic and lung tumour segmentation from training on reconstructions; −3.9 % FVD
and +2.76 % AUC multi-disease faithfulness for the conditional LDM. 22 GB GPU for the proposed method.
arXiv perpetual non-exclusive licence on the paper; repo licence not read.

**Fit.** Chest-centric and rib-level, not vertebra-level, and the evaluation is still on real patients'
own masks. But it is the strongest published evidence that (a) concatenation conditioning beats
ControlNet conditioning on thin bone by ~55 Dice points, and (b) 70 Dice on ribs is where the state of
the art sits when someone actually tries. 70 is not enough for us either.

---

## Candidate 5 — MedSyn / MedSyn2 (Batmanghelich lab). Best control interface; no spine.

**MedSyn.** Xu Y, Sun L, Peng W, et al. *MedSyn: Text-Guided Anatomy-Aware Synthesis of High-Fidelity
3-D CT Images.* IEEE Trans Med Imaging, Oct 2024; PMID 38900619; arXiv:2310.03559; code
https://github.com/batmanlab/MedSyn (public, pretrained model).
256³ chest CT generated **jointly with lung-lobe, airway and vessel masks**, conditioned on a radiology
report; supports fixing one anatomical structure and resampling the rest. 8,752 chest CTs (7,728 train)
+ 209,683 unpaired reports. FID 0.009 vs Medical Diffusion 0.013 and HA-GAN 0.023; MMD 0.019. Airway
Dice 0.75 ± 0.10, lobe Dice 0.77 ± 0.12 on generated volumes. **10 board-certified radiologists**,
blinded: airway realism statistically indistinguishable from real (p = 0.1), lobes better than the
Medical Diffusion baseline (p < 0.05). Downstream: pleural effusion accuracy 90.7 → 94.0 %, F1 0.79 →
0.84. Four A6000, 40k iterations.

**MedSyn2** — Dai W, Wang C, Li B, Ghosh S, Zandifar A, LeBedis C, Batmanghelich K. arXiv:2606.00967
(31 May 2026). **Resolved on the second pass: code IS released** at
https://github.com/batmanlab/MedSynV2 — source Apache 2.0, model weights under a "Custom Academic
License for Model Weights", components on Dropbox/HuggingFace.
Diffusion transformer, **448 × 448 × 448 at 0.7 mm isotropic**, latent 112 × 56 × 56 × 4, trained on
25,692 CT + report pairs from CT-RATE with masks from LungMask / TotalSegmentator / MedPSeg. Takes
*partial* segmentation prompts whose meaning is supplied by an accompanying text string — you condition
on one structure and name it, no full-organ annotation required. FID 9.59 vs Text2CT 12.58 on the lung
window (≈24 % relative mean improvement over GenerateCT, MedSyn, Text2CT). CLIP T2I 14.74 % (CT-CLIP) /
27.61 % (Pillar-0); I2I 83.00 % / 46.79 %. Two radiologists (4 and 17 years) on 150 cases: synthetic
Match/Partial-Match distributions similar to real, low Not-Match rate — **no numeric breakdown given**.
Tokenizer reconstruction Dice heart 97.50 %, airway 84.89 %, vessel 62.31 % — note these measure the
tokenizer, **not** the generated image's fidelity to the conditioning mask, and no such
generated-image-vs-mask Dice is published. Downstream: ground-glass-opacity segmentation Dice 68.13 %
with real + synthetic vs 58.78 % real-only, beating MedPSeg's 65.20 %. 24 h on a single A100; a 48 GB
GPU handles only mask-encoding batches 0–5.
**Edited masks:** Figure 4 spatially modifies nodule masks (flipping, translating) with the report
unchanged and shows the CT following — the closest published demonstration of mask editing, but
qualitative, on a blob inside a lung, with no metric.
*Why neither fits:* **chest only, supported structures are lobes, airways, vessels, heart and five
pathologies. No spine, no vertebra, no bone conditioning in either model or repo.** MedSyn2 is the
control interface we would want — one structure's mask plus the word naming it — pointed at the wrong
organ system.

---

## Candidate 6 — SegGuidedDiff (Konz et al., MICCAI 2024). The measurement protocol to copy.

Konz N, Chen Y, Dong H, Mazurowski MA. *Anatomically-Controllable Medical Image Generation with
Segmentation-Guided Diffusion Models.* MICCAI 2024, LNCS; arXiv:2402.05210; DOI
10.1007/978-3-031-72104-5_9. Code https://github.com/mazurowski-lab/segmentation-guided-diffusion
(CC BY 4.0), checkpoints released for Duke Breast MRI and CT-Organ.

**Generates.** 2-D slices, 256 × 256. **Not 3-D** — disqualifying for DRR casting; a stack of
independently sampled slices does not ray-cast into a coherent radiograph. A 3-D volumetric extension is
listed as future work and has not appeared.

**Control.** Multi-class mask injected at every sampling step, plus a random mask-ablation training
scheme so you can condition on a subset of structures and let the rest vary — the closest published
thing to "hold the spine fixed, let the rest of the abdomen move".

**Data.** Breast MRI 100 patients (~12,000 train / 2,500 test slices). CT-Organ 40 patients (~11,000
train / 2,100 test slices); labels liver, bladder, lungs, kidney, **bone** (one lumped class).

**Validation.** Mask faithfulness, Dice between conditioning mask and a segmentation of the generated
image: **SegGuidedDiff 0.8980 (CT) / 0.9027 (breast MRI); SPADE 0.8771 / 0.8473; ControlNet 0.1132 (CT)
/ 0.3636 (MRI)**. Downstream: a segmentation network trained on synthetic comes within ≤0.04 Dice of one
trained on real. Compute ~26 h on 4 × A6000 48 GB.

**Fit.** Wrong dimensionality; right measurement. If we test MAISI, this is the metric and the baseline
to copy. And its ControlNet column is the first of the two independent warnings about candidate 1.

---

## Candidate 7 — Killeen et al. 2025, conditional whole-body CT for virtual clinical trials.

Killeen BD, Wan B, Kulkarni AV, Drenkow N, Oberst M, Yi PH, Unberath M. *Towards Virtual Clinical Trials
of Radiology AI with Conditional Generative Modeling.* arXiv:2502.09688 (Feb 2025, 35 pp).

Whole-body CT generated **jointly with anatomical segmentations** (128 TotalSegmentator organs collapsed
to 16 classes, plus bone/adipose/muscle tissue classes). **Control is demographic only** — sex, age band,
height band, weight band. Not a mask; you cannot ask it for a vertebral phenotype. 798 whole-body CTs
from the New Mexico Decedent Image Database, 1 × 1 mm in-plane and **3 mm slice thickness** — too coarse
for end-plate morphometry, marginal for a lumbar DRR. FID 5.97 (10.26 without post-processing).
**Dice between the generated image's own anatomy and TotalSegmentator's reading of it 0.727 ± 0.115.**
Organ-volume Pearson r 0.911, centroid r 0.956 against the real cohort; conditioning fidelity 0.61–0.66
SD off target; sex-correct anatomy 98/100 by manual inspection. Downstream: body-fat and muscle-mass
regression on synthetic matched real in and out of distribution (BFP MAE 1.22 % vs 1.20 % ID, 3.86 % vs
3.66 % OOD), feature-importance correlation 0.993 / 0.919. Weights not released — "available upon
request to and approval by" NMDID. Compute 4 × A10 (20 GB) + 1 × A5000.

**Fit.** Poor control, coarse labels, and it is the model whose DRRs lost in candidate 3. But it is the
only paper that checked whether a synthetic cohort's anatomy tracks the conditioning variables at
population level, which is the "population-plausible" half of our requirement.

---

## Candidates 8–12 — the rest, and why each falls

**GenerateCT** — Hamamci IE, Er S, Almas E, et al. ECCV 2024; arXiv:2305.16037; code and weights public
(https://github.com/ibrahimethemhamamci/GenerateCT, HF `generatect/GenerateCT`). Text-conditional 3-D
chest CT. Strongest *downstream* result in the field: a multi-abnormality classifier trained on 100,000
synthetic CTs beat one trained on all real data by 8 %, and real + generated gave +7 % on unseen
prompts. **Text-only conditioning, chest only, no masks, no anatomical-geometry validation.** The
control channel we need is absent.

**Medical Diffusion / Khader et al.** — Khader F, Müller-Franzes G, Tayebi Arasteh S, et al. *Denoising
diffusion probabilistic models for 3D medical image generation.* Sci Rep 2023;13:7303; DOI
10.1038/s41598-023-34341-2; preprint arXiv:2211.03364; code public. 3-D latent DDPM over MRI and CT,
**unconditional**. Reader study: two medical experts rated realistic image appearance, anatomical
correctness and consistency between slices — **the numeric ratings are still not retrieved** (Nature
paywall redirect; PMC record for this DOI resolves to an unrelated article). Resolved on the second
pass: **breast segmentation Dice 0.91 without vs 0.95 with synthetic pre-training in the scarce-data
regime.** Unconditional generation is worth little to us regardless.

**HA-GAN** — Sun L, Chen J, Xu Y, Gong M, Yu K, Batmanghelich K. IEEE J Biomed Health Inform 2022; PMID
35522642; code https://github.com/batmanlab/HA-GAN. Memory-efficient 3-D GAN, 256³ thorax CT and brain
MRI, unconditional. Superseded — MAISI reports HA-GAN FID 98–116 against its own 4.3–8.3 on the same
chest sets. Listed only as the standard baseline.

**GuideGen** — arXiv:2403.07247. Text → **anatomical mask and CT together**, 19 torso structures
including a `Vertebra` class, 128³, 4,534 training cases from 12 TCIA collections + 1 private. FID 20.5,
LPIPS 0.24, **image–mask DSC 0.61**, multi-organ segmentation DSC 0.79, tumour 0.48. ~26 s per volume on
4 × RTX 4090. Code "released should the paper be accepted", CC BY-NC-ND 4.0. 0.61 agreement at 128³ is
unusable for per-level work; it is evidence of how hard joint mask + CT generation still is.

**Sketch2CT** — CVPR 2026; arXiv:2603.22509; code https://github.com/adlsn/Sketch2CT. Two stages:
generate a 3-D organ mask from a 2-D sketch + a text description of 3-D geometry, then paint the CT on
that mask. **128³**, liver / aorta / heart only (CHAOS 20, AVT 56, Decathlon liver 131, Decathlon heart
MRI 20), **no bone or spine**; the authors name "limited to a few organs" as a limitation. FID 33.7–65.1,
mask-faithfulness Dice 0.642–0.912, downstream segmentation on real test data 0.711–0.904. Two experts,
qualitative only. H200, 300 epochs. Architecturally the closest to "draw the anatomy you want, get a
CT" — at a quarter of our needed resolution and on organs we do not care about.

**3D MedDiffusion** — Wang H, Liu Z, Sun K, Wang X, Shen D, Cui Z; arXiv:2412.13059 (rev Nov 2025); code
+ checkpoints at https://github.com/ShanghaiTech-IMPACT/3D-MedDiffusion. Up to 512³, CT and MRI, head to
leg, released weights, ≥40 GB for inference, 4× and 8× compression variants. **Resolved on the second
pass: the documented conditioning modes are class-conditional generation, sparse-view CT reconstruction
and accelerated MRI. Dense anatomical-label-map conditioning is not documented in the repo, and the
licence is not stated.** Rank below candidates 1 and 4 until someone runs it.

**AbdomenGen** — arXiv:2604.12969. Sequential volume-conditioned generation of **masks only** for 11
abdominal organs, controlled by a "Volume Control Scalar" that decouples organ size from body habitus;
liver Dice 0.83 ± 0.05, stable calibration over VCS [−3, +3], Wasserstein-based selection cuts the
training distribution distance by 73.6 % on a hepatomegaly cohort. No image synthesis, no bone. Listed
because the VCS idea — a standardised residual as the control knob, chosen to fill a thin part of the
cohort distribution — is directly transferable to "sample a target lordosis", whatever generator sits
downstream.

---

## Adjacent, and possibly the better route

**Expert-validated synthetic cervical spine radiographs** — Barr AA, et al. arXiv:2510.22166 (25 Oct
2025). DDPM on 4,963 images from the Cervical Spine X-ray Atlas; 20,063 synthetic radiographs released.
**8 experts (6 neuroradiologists, 2 spine neurosurgeons)** on 50 quartets picked the real image in only
**29 %** of trials (chance 25 %), Fleiss κ 0.061; realism 3.323 (real) vs synthetic with no significant
difference. The strongest *spine* human-validation result in the whole generative literature — and it is
2-D, unconditional, and **produces no labels**, so it cannot train a level detector. It is the
spine-domain analogue of the DiffXray arm that beat DiffCT-DRR, and it points the same way.

**DiffusionXRay** — arXiv:2603.01686; Springer chapter DOI 10.1007/978-3-032-08009-7_4 (2026). Does not
generate CT at all: it takes a **DRR that already carries known labels** (they insert lung nodules) and
restores it toward real-radiograph appearance, via a two-stage pipeline (DDPM-LQ or MUNIT-LQ makes the
degraded pair, then a DDPM learns the restoration). Claims preservation of "subtle yet clinically
significant artifacts" and reports "quantitative metrics and expert radiological assessment" — **no FID,
SSIM, PSNR or downstream detection numbers retrievable from the abstract or the arXiv page.** Weak
validation as published, but the *shape* of the method is the one the rest of this literature keeps
pointing at: keep the geometry exact by casting from a real labelled CT, and spend the generative model
on appearance in 2-D, where our labels cannot be broken.

**Conditional diffusion for trabecular bone** — Johns Hopkins group. J Med Imaging, Feb 2026, PMID
41704846; SPIE Medical Imaging 2025 version DOI 10.1117/12.3049125, PMID 40735600. Latent DiT with a
dedicated VAE, generating 3-D trabecular bone tunable to prescribed **BV/TV, Tb.Th and Tb.Sp**, with
shifting-slab inference for extended volumes; 3,551 VOIs from 20 femoral specimens for training, 2,000
synthetic samples across a wide range of target metrics for testing; validation is agreement between
prescribed and achieved morphometry. **The only bone-specific conditional 3-D generative model with real
quantitative control that I found** — and it is micro-CT microstructure, not vertebral morphology. Cited
as the existence proof that bone generation with a measurable control variable is achievable, at a scale
two orders of magnitude below ours.

---

## What is NOT known (stated plainly)

Closed on the second pass:
- ~~Whether anyone conditioned on an edited mask~~ — seg2med did, on a merged-patient composite, and
  FSIM halved (0.45 vs 0.82); MedSyn2 did it qualitatively for a translated nodule.
- ~~Whether MAISI's ControlNet follows a bone mask~~ — rib Dice 15.20 (Foundation VAE, third party).
- ~~MedSyn2 code status~~ — released, Apache 2.0 code, custom academic licence on weights.
- ~~Khader's downstream delta~~ — breast segmentation 0.91 → 0.95 with synthetic pre-training.
- ~~Whether 3D MedDiffusion takes a dense label map~~ — not documented; class-conditional, sparse-view
  CT and accelerated MRI are what the repo describes.

Still open:
- Whether a mask-conditioned generator paints a coherent CT for a mask containing a **plausible but
  absent** phenotype — an inserted L6, a sacralised L5. seg2med's two results bracket the question
  (coherent synthetic anatomy works, incoherent does not) without answering it.
- Whether **any** generator's per-vertebra mask adherence clears 0.9 in 3-D. The only per-vertebra
  numbers in existence are seg2med's 2-D ones, and L4 is 0.72.
- Whether a DRR cast from a mask-conditioned, 1 mm, bone-focused generated CT is usable for C-arm level
  work. The only related experiment used an unconditional 3 mm generator and lost.
- Khader 2023's exact reader-study rating values — not retrieved (paywall; PMC record mismatched).
- MedSyn2's generated-image-vs-conditioning-mask Dice — not published; only tokenizer reconstruction
  Dice is.
- Whether the NVIDIA Open Model License permits the commercial track. Not read, and not a decision I
  should make.

## If we go this way, the cheap decisive test (unchanged, but now confirmatory)

MAISI is downloadable and its label dictionary is our label dictionary. The test costs a day: take N of
our CTSpinoPelvic1K cases, feed the MAISI ControlNet the *unedited* v11 label map, and measure
(a) Dice between the conditioning vertebra labels and TotalSegmentator's reading of the generated CT —
the Konz metric, **per level, not lumped**, and quote it beside Foundation VAE's rib 15.20 and
seg2med's L4 0.72; (b) whether a DRR cast from the generated volume is called correctly by our existing
detector. Then repeat with an L5 relabelled as an L6 and an extra body inserted, and **look at the
render**. If (a) is below ~0.9 per vertebra, or the DRR does not look like a render, the angle is dead
and we have a number to say so with.

Given rib 15.20 and vessel 13.50, the honest expectation is that (a) comes back low and this test is
how we close the angle rather than how we open it. That is still worth a day — it converts "the
literature is discouraging" into "we measured it on our own data" — but it should be scoped as a
disproof, not as a pilot.
