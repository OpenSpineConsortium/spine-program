# Prior art: synthesis of rare anatomical variants (angle: transitional vertebrae)

Compiled 2026-09-23. Literature only — nothing implemented, nothing run.
Requirement being judged against: CT + per-vertebra labels in, NEW anatomically plausible
labelled volumes out, realistic enough to cast a DRR, controllable to a target phenotype
(L6 / T13 / sacralised L5 / four-lumbar) or a target sagittal parameter, population-plausible.

---

## 0. The headline, stated plainly

**No published work has synthesised a transitional vertebra, an L6, a T13, a sacralised L5,
or any numerical vertebral variant, in any modality.** I searched CT, radiograph and MRI,
GAN / diffusion / shape-model / FE / registration framings, and the LSTV-specific AI
literature. Every paper that handles enumeration anomalies uses naturally occurring cases:

- **VERIDAH** (arXiv 2601.14066) — anomaly-aware vertebra labelling across sequences;
  multiple classification heads + weighted sequence prediction. 98.30% of subjects fully
  correct on T2w (vs 94.24%), 99.18% on CT (vs 77.26%), p<0.001; anomaly detection 87.80%
  thoracic / 94.48% lumbar on T2w, 96.30% / 97.22% on CT. Code with SPINEPS.
  **No synthesis, no simulated anomaly.**
- **Transformer-enhanced vertebrae segmentation and anatomical variation recognition**
  (Sci Rep 2025, PMC12491412) — the paper that most loudly claims T13/L6 handling. Its
  augmentation is, verbatim, "random affine transformations (rotation ±15°, scaling
  0.9–1.1), Gaussian noise σ=0.01, histogram equalization, contrast normalization." VerSe
  2019+2020, 374 CTs / 355 subjects; it does not state how many T13 or L6 cases it has and
  does not address class imbalance. Reported: L6 accuracy 85% (AUC 0.96), T13 80%
  (AUC 0.93); variant-alert precision 0.914 falling to 0.802 under scanner shift.
- **LSTV detection on radiographs** (PMID 41227066 / PMC12610351) — 3,116 standing laterals,
  DINOv2 / CLIP / ResNet-50, ResNet-50 best. Real data only.

So the prior art for this angle is **by analogy**: rare-variant synthesis in other organs,
and the generic machinery that could be pointed at the spine. What follows is that, with
the validation stated honestly.

---

## 1. The closest validated analogue: conditional shape generation across a topology change

### SDF4CHD — Kong, Shadden et al., *Medical Image Analysis* 2024 (PMC11372630, doi 10.1016/j.media.2024.103293)

The single most relevant published method. Generates whole-heart anatomies **with congenital
defects** as signed distance fields, and — the part that matters — **disentangles "type"
(the CHD-specific topology, from a binary diagnosis vector) from "shape" (patient-specific
variation, a latent code)**. That is structurally the thing we need: *phenotype = L6 /
Castellvi III / four-lumbar* is the type vector; *this person's L4* is the shape code.

- Generates: 3D shapes (SDF → mesh), and paired CT images with segmentations.
- Control: binary diagnosis vector over 6 primary CHD types + 14 combinations.
- Validation: reconstruction Dice on unseen cases — whole heart **88.8 ± 2.0**; LV 91.4±2.7,
  RV 88.3±7.9, LA 85.5±4.7, RA 91.9±2.1, myocardium 90.0±3.8, aorta 83.0±8.6, PA 76.7±14.3.
  **Type correctness on 50 generated anatomies: 47/50 correct, vs 2/50 for conditional
  DeepSDF.** That is the number that matters — it is an *external* check that the generated
  anatomy actually carries the phenotype it was asked for, which is exactly the check our
  project needs and exactly the check most generative papers skip.
- Data: ImageCHD, 110 CT (67 train / 8 val / 34 test), expert-cleaned segmentations.
- Downstream gain, measured: 3D U-Net with 420 synthetic added — whole-heart Dice
  84.7±6.0 → **86.3±5.3**; LV 85.3±8.0 → 88.2±5.1; RA 87.3±8.3 → 88.8±7.9. VSD median
  diameter error 54% → 38%, area error 72% → 59%.
- Code: authors state they will share the trained generator; repository URL not given in
  the paper text I could reach. Compute not reported.
- **Adversarial read**: n=67 training hearts. The whole-heart Dice gain is +1.6 points —
  modest. The strong result is the *type correctness*, not the segmentation number.

### SV-Cine — arXiv 2609.12997 (2026), the downstream application of SDF4CHD

SDF4CHD geometry → SPADE conditional GAN → 2D short-axis cine MRI; segmentation network
conditioned on diagnosis through FiLM layers.

- Training: 58 real HVSMR patients + **500 synthetic** = 558. Test: 20 UCLA + 19 CHOC.
- Ablation, and this is the strongest measured rare-anatomy synthesis result I found
  anywhere: **RV Dice 0.36 without synthetic → 0.72 with**; hypoplastic-ventricle EF error
  **35.98 pp → 14.5 pp**. Removing *diagnosis conditioning* (keeping the synthetic data)
  drops RV Dice to **0.14** — i.e. unconditional generation was actively worse than
  conditional, by a wide margin. vs nnU-Net 2D: RV Dice 0.72 vs 0.33, HD95 17.03 → 3.85 mm.
- Compute: one RTX 4070. Code not mentioned.
- **Adversarial read**: the base RV Dice of 0.36 is a near-empty class, so the headroom is
  enormous; this is the honest shape of the argument for us too (86 transitional subjects).
  External cohort degrades (LV 0.89 → 0.76), which is the usual story.

### PhyloSDF — arXiv 2604.25371 (2026), Zenodo 19922966

Conditional SDF generation of 3D skull morphology conditioned on a **discrete taxon label**,
via residual conditional flow matching + a phylogenetic consistency loss. Included because
it is the only published evidence I found on *how few specimens per discrete anatomical
class* a conditional shape generator needs, and on the failure mode to test for.

- Data: 100 micro-CT skulls, 24 species, **~4 specimens per species**.
- Validation: generated meshes reach **88–129% of real intra-species variation**; all 180
  generated meshes verified non-memorised; latent–evolutionary-distance Pearson r = 0.993.
- **Denoising diffusion fails entirely at this scale; plain flow matching mode-collapses to
  3–6% of real variation.** If we build a conditional generator on 86 transitional subjects,
  mode collapse is the thing to measure, and "% of real intra-class variation reproduced" is
  the metric that catches it.
- Non-spine, non-clinical, very new. Treat as a methodological pointer, not a citation to
  lean on.

---

## 2. Mask → image: the half that paints HU into an edited label map

These take a label map you supply and render an image. None of them invents the variant;
you must produce the edited labels yourself. Paired with §1 or with a hand-built label edit,
they are the only published route to "new volume WITH labels that stay aligned" by
construction (the labels are the input, so alignment is exact — no resampling question).

### Segmentation-guided diffusion — Konz, Chen, Dong, Mazurowski, MICCAI 2024 (arXiv 2402.05210)

- Multi-class mask conditioning injected at **every sampling step**, plus a random
  mask-ablation training scheme so you can constrain some structures and leave others free.
- Validation: SOTA on **faithfulness of generated images to the input mask**, beating SPADE
  and ControlNet; "on par" for general anatomical realism. Datasets: Duke Breast MRI,
  CT-Organ (neck-to-pelvis).
- Code + checkpoints: `github.com/mazurowski-lab/segmentation-guided-diffusion`, paper CC BY 4.0.
- **Adversarial read for us**: 2D slice-wise; validated on soft tissue, not cortical bone;
  no spine data; no downstream segmentation gain reported in the paper. Cortical/trabecular
  detail is precisely what a DRR is made of, and nothing here says it survives.

### MAISI / NV-Generate-CT — Guo, Zhao et al., NVIDIA, WACV 2025 (arXiv 2409.11169)

- 3D, **512×512×512 at 1.0 mm isotropic**, latent diffusion + ControlNet conditioning on
  organ masks, **127 anatomical classes including vertebrae**, emits image + mask.
- Licence: Apache 2.0 in MONAI; weights on HuggingFace `nvidia/NV-Generate-CT`. This is the
  only production-grade, openly licensed, genuinely 3D mask-conditioned CT generator.
- Downstream, measured: +2.5% to +4.5% Dice across five tumour types with Auto3DSeg.
- **Adversarial read**: validation is organ-level; nothing per-vertebra, nothing about
  cortical sharpness, nothing about DRRs. The +2.5–4.5% is tumours, not bone.

### SynthSeg — Billot et al., *Medical Image Analysis* 2023 (arXiv 2107.09559)

The proof that "edit the label map, synthesise the image, train on it" works — and the
clearest statement of why it would not work for us unmodified. SynthSeg samples intensities
per label from randomised Gaussians (domain randomisation), deliberately abandoning
realistic contrast, and matches supervised CNNs across contrasts without retraining.
Code `github.com/BBillot/SynthSeg`. Brain MRI only.
**For us: the images are not radiographically realistic by design, so a DRR cast from them
is not a radiograph.** Cite as the mechanism, not the method.

---

## 3. Physics-based deformation (the family Greg rejected — reported honestly)

### FE spine model → scoliotic CT volume — Tapp et al., *Computational Biomechanics for Medicine* (MICCAI 2021 workshop), Springer 2022, doi 10.1007/978-3-031-09327-2_6

Cervical, thoracolumbar and lumbar FE spine models deformed by FE analysis, then converted
into CT volumes with "authentic Hounsfield units" plus ground-truth bone and soft-tissue
segmentations. Companion data repository: arXiv 2402.13041, "Data Repository of Finite
Element Models of Normal and Deformed Thoracolumbar Spine."

- **Validation, in full: the volumes were "tested in a pre-trained vertebral segmentation
  deep learning neural network to prove compatibility with image analysis methods."** That
  is a smoke test — it shows a network does not choke, not that the anatomy is right. No
  anatomical fidelity metric, no reader study, **no downstream training gain measured**.
- This is the published, peer-reviewed version of the deformation approach, and its
  validation is exactly the weak kind. Worth saying out loud: adopting it does not buy
  "proven and validated"; it buys a citation with a smoke test behind it.

### Anatomy-informed data augmentation — Kovacs et al., MICCAI 2023 (arXiv 2309.03652)

Deformation field driven by *adjacent organs* (rectum/bladder filling) to simulate real
physiological soft-tissue deformation of the prostate, preserving the lesion label.
Code: `github.com/MIC-DKFZ/anatomy_informed_DA`.

- Validation worth copying: **a clinician failed to detect the deformation in 92% of rectum
  and 93% of bladder cases** — a reader study, not a re-measurement. Plus a measured
  prostate-cancer detection gain.
- The closest published relative of a smooth-displacement-field augmentation, from the group
  behind nnU-Net. Note what they validated: *did a human notice*. Not *did the volume
  re-measure the number it was asked for*.

---

## 4. Object-level and tail-class machinery with measured gains

### TumorCP — MICCAI 2021 (arXiv 2107.09843), `github.com/YaoZhang93/TumorCP`

Online stochastic intra- and inter-patient copy-paste of tumour objects + spatial/gamma/blur
transforms, inside nnU-Net. **+7.12 Dice on kidney tumour over a strong baseline; +2.32 over
SOTA when combined with image-level augmentation; +21.87 Dice with only 10% labelled data.**
The cheapest analogue of transplanting a donor L6 into a recipient spine.
**Adversarial read**: a lesion floats in parenchyma. A vertebra must articulate — facets,
disc space, pedicles, the sacral ala. Copy-paste has never been validated on a structure
with articular constraints, and the failure would look plausible on a slice.

### LoGex — arXiv 2409.01317, `github.com/mueller-mp/logex`

Extremely rare histopathology classes: **10 samples per tail class**, LoRA-finetuned
Stable Diffusion + classifier guidance, 100 synthetic per class.
Tail detection FPR **25.05% → 16.25%**, AUC 95.01 → **96.27**, head accuracy held at 96.97%.
Direct precedent that generation helps at n≈10. 2D, classification, not anatomy.

### Long-tail synthetic augmentation, skin lesions — arXiv 2605.03221 (2026)

Inpainting diffusion + OOD post-selection on ISIC2019; **>28% improvement on the rarest
class**; authors state rebalanced losses and handcrafted augmentation give "only marginal
improvements." Useful as the general claim that generation beats oversampling on tails —
but it is dermoscopy classification, and I would not carry the number into a spine paper.

---

## 5. Spine-specific generative work, and why none of it meets the requirement

| Work | What it does | Validation | Verdict |
|---|---|---|---|
| Galbusera et al., *Front Bioeng Biotechnol* 2018 6:53 | pix2pix: operator draws vertebral-body quadrilaterals L1–L5 + sacrum → synthetic sagittal lumbar radiograph. 1,352 radiographs (1,252 train); second task 1,602 CTs | **Authors state: "the quality of the outputs ... has been judged qualitatively only ... no quantitative evaluation has been performed."** They list spinous processes and distal sacrum "indistinct", thoracic vertebrae "approximate", pelvis "rather indistinct", femurs "inaccurately represented", lumbar vertebrae "asymmetrical and generally unrealistic" | The cautionary precedent. The one "draw the spine, get the radiograph" result, and it failed on exactly the structures we need (sacrum, femurs) |
| Synthetic cervical spine radiographs, 2025 (PMC13185266) | Unconditional DDPM on CSXA (4,963 radiographs); 20,063 synthetic released on figshare, CC BY 4.0 | **8 clinicians (6 neuroradiologists, 2 spine neurosurgeons) picked the real image in 29.0% of trials** — below chance; Fleiss κ 0.061; realism ratings not significantly different. Transfer: MSE 31.78 vs 84.33 de novo at n=100; 4.37 vs 7.42 at n=700 | Proves the 2-D realism bar is reachable for spine. **Zero anatomical control** — cannot place a phenotype |
| Spine-fracture GAN augmentation (Sci Rep 2025, s41598-025-98518-7); VAE-GAN augmentation (Comput Biol Med 2024) | DCGAN/PGGAN and VAE-GAN synthetic vertebral compression fractures | Ensemble accuracy 89.98% → 93.68%; VAE-GAN: real-image classification 73% → 89%, "FID 5× lower than other architectures" | **Weak.** Classification accuracy on small sets, FID as the only fidelity measure, no anatomical validation at all |
| HealthiVert-GAN (arXiv 2503.05990, PMID 40402696) | Synthesises the *pseudo-healthy pre-fracture* vertebra to grade height loss | Height-loss grading task | Edits one vertebra in place — mechanically the nearest thing to "edit this vertebra", but the target is restoration, not a new phenotype |
| Statistical shape / shape+pose models: Rasoulian *IEEE TMI* 2013;32(10):1890–1900 (32 subjects); Learning a Statistical Full Spine Model from Partial Observations, MICCAI 2020; Nicolella & Campbell *J Biomech* 2016 (18 cadaveric L1–L5, virtual FE population); deep implicit SSM MICCAI 2024 (lumbar Dice 87.2±2.9%, HD95 2.81±0.99 mm) | Generate new plausible spine shapes from a learned population | Standard SSM generalisation/specificity; segmentation accuracy | **Structurally cannot do our job.** Every one is built on a fixed point correspondence across a *fixed number of vertebrae*. An SSM cannot add a vertebra. This is precisely why SDF4CHD's type/shape split matters |

---

## 6. What a synthesis MUST get right — the LSTV morphology requirement

### Castellvi (1984) — the label is decided by measurable geometry

- **Type I**: dysplastic transverse process, **vertical dimension ≥ 19 mm** (some sources
  state "at least 19 mm in width"). Ia unilateral, Ib bilateral.
- **Type II**: incomplete sacralisation/lumbarisation — a **diarthrodial pseudoarticulation**
  between the enlarged TP and the sacral ala: a joint space, opposed cortical surfaces,
  usually subchondral sclerosis. IIa unilateral, IIb bilateral.
- **Type III**: complete — **osseous fusion** TP↔ala. IIIa unilateral, IIIb bilateral.
- **Type IV**: type II on one side, type III on the other.

Three consequences for any generator:

1. **19 mm is a hard threshold that decides the class label.** The method must control a
   single linear dimension to millimetre precision, and must be able to report it.
2. **Type II is a joint, not a bulge.** Generating a big transverse process that merely
   touches the ala produces something that is not type II and not type III. A pseudarthrosis
   needs two cortical surfaces and a gap.
3. **Type IV requires asymmetry.** A left-right symmetric generator cannot produce it, and
   type IV is 3–5.8% of LSTV. Any shape model built on mirrored/averaged anatomy will
   silently be unable to make this class.

### Other features a reader (and therefore a network) uses

- **Iliolumbar ligament**: arises from the L5 transverse process to the posteromedial iliac
  crest; on axial MRI a single/double low-signal band (Hughes & Saifuddin, *AJR* 2006,
  doi 10.2214/AJR.05.0415 — 46 of 67 LSTV numbered as L5 transitions, 21 as S1). Garg et al.
  report **85% sensitivity, 100% specificity** for identifying L5. **Carrino et al. dissent:
  the ILL marks the lowest lumbar vertebra, which is not always L5.** For CT and DRR work
  the ligament is not visible, so the synthesis must carry the bony correlates instead.
- **S1–S2 disc morphology**: O'Driscoll classification, four types on sagittal MR by disc
  material and AP diameter. A lumbarised S1 is squared, with facet joints and a full disc;
  a sacralised L5 is wedged, with hypoplastic/absent facets and a hypoplastic/absent disc.
- **"Squaring"**: anterior:posterior endplate height ratio **1.37** (Wigh & Anthony 1981).
  The 2025 systematic review calls squaring/wedging **unreliable** as an identifier.
- **Rib correlates** — important for us because our labels carry ribs. Hanhivaara et al.,
  *Skeletal Radiology* 2025 (doi 10.1007/s00256-025-04952-z, PMID 40381031), whole-spine CT,
  n=551: **sacralisation predisposes to a hypoplastic 12th rib; lumbarisation to a lumbar
  rib.** A synthesis that changes the lumbosacral junction and leaves the ribs alone
  produces a spine that contradicts the published co-occurrence.
- **The variant is not a local edit.** *World Neurosurgery* 2024 (PMID 38843967), 110 LSTV
  columns vs 60 sex-balanced controls, digital Vernier caliper on dried bone: the LSTV
  cohort has **longer transverse processes at every lumbar level, most at L3**, left > right.
  So an LSTV spine differs from a normal spine above the junction too. Editing only L5/S1
  makes a spine that is wrong in a way the morphology classifier could plausibly learn.
- **The pelvis changes too**: LSTV influences acetabular orientation and pelvic tilt
  (PMC9457479). Directly relevant to our PI/SS/PT pipeline — a synthetic LSTV that leaves
  the pelvis at the donor's geometry is not a population-plausible sample.
- **Ferguson view** (30° cranially angled AP) is the standard radiographic detection method
  — the projection geometry itself is part of what makes the variant visible.

### Reliability of the *human* label — the number that should shape our validation

- Plain radiograph vs CT for Castellvi typing (PMC7260820): **35.2% of types misclassified
  (32/91)**; κ = 0.502 and 0.493 across two readings. By type: IIa 76.9% correct, **IIb 29.4%**,
  IIIa 100%, IIIb 100%, **IV 15.4%**. Authors: CT is the gold standard.
- Hanhivaara et al., *Acta Radiologica* 2024 (doi 10.1177/02841851241289355, PMID 39444351):
  CT has the highest diagnostic performance on every metric with good inter-reader
  reliability; **MRI and conventional radiography show "fairly poor sensitivity and accuracy."**

**Implication**: a synthesis validated against a *radiographic* Castellvi grade is validated
against a label that is wrong a third of the time, and wrong 70–85% of the time for types
IIb and IV. Validate the geometry against CT, and against the measurable definitions
(19 mm, joint present/absent, unilateral/bilateral), not against a reader's grade.

---

## 7. Prevalence — how much variation exists, and why "match the published distribution" is not yet a well-posed target

| Source | Population, n | Overall LSTV | Type distribution |
|---|---|---|---|
| Systematic review 2025 (PMC12549404) | pooled, 28,106 | **15.3%** (4,290), range **4.5–35.6%** | not poolable — "variations in standardized reporting ... prevented meta-analysis" |
| Hanhivaara, whole-spine CT 2025 (PMID 40381031) | 551 | **16.3%** | 12.3% sacralisation, 4.0% lumbarisation |
| Abdominal CT (Eur Radiol 2020, PMC7248049) | 3,855 | **28.6–29%** | I 68%, II 16%, III 13%, IV 3% |
| Osteoarthritis Initiative cohort | — | — | I 41.7%, II 41.4%, III 11.5%, IV 5.2% |
| South African radiographs (*Transl Res Anat* 2025, S2214854X25000421) | 3,096 | **10%** | II 67.9%, III 27.6%, IV 4.5% |
| Low back pain (PMC10198219) | 4,816 | **8.1%** | — |
| Paik 2013 | 8,280 LBP | types II–IV **10.6%** | sacralisation 5.3%, lumbarisation 5.3% |
| Adolescent idiopathic scoliosis, Chiu 2024 | 998 | **25.1%** | — |
| Bornstein & Peterson 1966, *Am J Phys Anthropol* 25(2) | 1,239 skeletons | numerical variation **11%** | **6% with 23 presacral, 5% with 25 presacral**; sex difference (males more 25, females more 23); significant differences between population groups |

**The spread is the finding.** 4.5% to 35.6% overall, and type I at 68% in one cohort and
41.7% in another, 0% in a third (the South African series found no type I at all — II 67.9%,
III 27.6%, IV 4.5%). The type distribution is not stable across cohorts, imaging modality,
or definition. So "sample the synthetic population to match published prevalence" is
under-determined: **you must name the cohort you are matching and say why.** Our own
distribution across CTSpinoPelvic1K / TotalSegmentator / VerSe is a fourth cohort with a
fourth referral pattern.

Also: LSTV and numerical variation are not the same variable. 11% of skeletons have 23 or
25 presacral vertebrae (Bornstein), while LSTV runs 8–29% depending on definition — the
Castellvi types I and II do not necessarily change the count, and the count can change
without a Castellvi-gradable junction. Any conditioning vector needs both axes.

---

## 8. What is not known

- **Nobody has measured whether synthesising a rare anatomical variant improves vertebra
  *naming*.** Every measured downstream gain in this note is segmentation, detection or
  classification Dice/accuracy. The nearest is SV-Cine's RV Dice 0.36 → 0.72.
- **Nobody has validated that any generative CT output survives a DRR.** Not MAISI, not
  segmentation-guided diffusion, not the FE→CT pipeline. Bone realism is assessed on slices
  everywhere I looked. This is a real gap and a real risk: a volume can look right in
  axial slices and cast a wrong-looking radiograph, which is precisely this project's
  recurring failure mode in another costume.
- **No spine method exists that can change the vertebral count.** SDF4CHD is the only
  published method anywhere that generates across a topology change conditioned on a
  discrete phenotype, and it is cardiac, n=67.
- **Castellvi type distribution across cohorts is unexplained**, not merely variable — the
  reviews say so themselves and decline to pool.
- **Whether 86 transitional subjects is enough** for a conditional generator: PhyloSDF got
  usable variation from ~4 per class in 24 classes, LoGex from 10 per class; neither is 3-D
  clinical CT with articulated bone. Unknown.
- Compute cost is unreported for SDF4CHD and for the FE→CT pipeline; code URL is unstated
  for SDF4CHD and SV-Cine.

---

## 9. Reading of the evidence for this project (not a recommendation to implement)

The only published, validated design that matches our requirement — discrete phenotype in,
anatomically plausible labelled volume out, across a change in structure count — is the
**SDF4CHD two-stage pattern**: a type-conditioned implicit shape generator for the geometry,
then a mask-conditioned image generator to paint it. Both halves have open, validated
implementations (SDF4CHD's type-correctness 47/50; MAISI Apache-2.0 3-D mask→CT; Konz et al.
for mask faithfulness). The gap nobody has closed is the DRR: no published work validates
that generated bone survives projection. That gap is simultaneously the contribution and
the risk, and it is the thing to test first, cheaply, before anything is built.

The deformation-field family is not disqualified but it is not "proven and validated"
either: its peer-reviewed spine instance (Tapp et al.) was validated by a smoke test, and
its best-validated relative (Kovacs et al.) was validated by a reader study, not by
re-measurement. If that family is used, the honest framing is that we would be extending a
method whose published validation is weaker than the numbers we would need.

---

## Citations

- Kong F, Shadden S, et al. SDF4CHD: Generative modeling of cardiac anatomies with congenital heart defects. *Med Image Anal* 2024. doi 10.1016/j.media.2024.103293. PMC11372630
- SV-Cine: Diagnosis-Conditioned Segmentation of Single Ventricle Physiology via Generative Data Augmentation. arXiv:2609.12997
- Konz N, Chen Y, Dong H, Mazurowski MA. Anatomically-Controllable Medical Image Generation with Segmentation-Guided Diffusion Models. MICCAI 2024. arXiv:2402.05210. github.com/mazurowski-lab/segmentation-guided-diffusion
- Guo P, Zhao C, et al. MAISI: Medical AI for Synthetic Imaging. WACV 2025. arXiv:2409.11169. Apache-2.0 in MONAI; huggingface.co/nvidia/NV-Generate-CT
- Billot B, Greve DN, et al. SynthSeg: Segmentation of brain MRI scans of any contrast and resolution without retraining. *Med Image Anal* 2023. arXiv:2107.09559. github.com/BBillot/SynthSeg
- Tapp A, et al. Generating Scoliotic Computed Tomography Volumes from Finite Element Spine Models. *Computational Biomechanics for Medicine* (MICCAI 2021 workshop), Springer 2022. doi 10.1007/978-3-031-09327-2_6. Data repository arXiv:2402.13041
- Kovacs B, et al. Anatomy-informed Data Augmentation for Enhanced Prostate Cancer Detection. MICCAI 2023. arXiv:2309.03652. github.com/MIC-DKFZ/anatomy_informed_DA
- Zhang Y, et al. TumorCP: A Simple but Effective Object-Level Data Augmentation for Tumor Segmentation. MICCAI 2021. arXiv:2107.09843. github.com/YaoZhang93/TumorCP
- Mueller MP, et al. LoGex: Improved tail detection of extremely rare histopathology classes via guided diffusion. arXiv:2409.01317. github.com/mueller-mp/logex
- Synthetic Data Generation for Long-Tail Medical Image Classification: A Case Study in Skin Lesions. arXiv:2605.03221
- PhyloSDF: Phylogenetically-Conditioned Neural Generation of 3D Skull Morphology via Residual Flow Matching. arXiv:2604.25371; Zenodo 19922966
- Galbusera F, et al. Exploring the Potential of Generative Adversarial Networks for Synthesizing Radiological Images of the Spine to be Used in In Silico Trials. *Front Bioeng Biotechnol* 2018;6:53
- Synthetic cervical spine radiographs: expert validation and transfer learning for low-data settings. 2025. PMC13185266
- HealthiVert-GAN: Pseudo-Healthy Vertebral Image Synthesis for Interpretable Compression Fracture Grading. arXiv:2503.05990. PMID 40402696
- Rasoulian A, Rohling R, Abolmaesumi P. Lumbar spine segmentation using a statistical multi-vertebrae anatomical shape+pose model. *IEEE Trans Med Imaging* 2013;32(10):1890–1900. PMID 23771318
- Nicolella DP, Campbell N, et al. Automated finite element modeling of the lumbar spine: Using a statistical shape model to generate a virtual population of models. *J Biomech* 2016. PMID 27270207
- VERIDAH: Solving Enumeration Anomaly Aware Vertebra Labeling across Imaging Sequences. arXiv:2601.14066
- Transformer-enhanced vertebrae segmentation and anatomical variation recognition from CT images. *Sci Rep* 2025. PMID 41038867, PMC12491412
- Automated Detection of Lumbosacral Transitional Vertebrae on Plain Lumbar Radiographs Using a Deep Learning Model. PMID 41227066, PMC12610351
- Konin GP, Walz DM. Lumbosacral transitional vertebrae: classification, imaging findings, and clinical relevance. *AJNR* 2010;31(10):1778–86. PMID 20203111
- Castellvi AE, Goldstein LA, Chan DPK. Lumbosacral transitional vertebrae and their relationship with lumbar extradural defects. *Spine* 1984;9(5):493–5
- Hughes RJ, Saifuddin A. Numbering of lumbosacral transitional vertebrae on MRI: role of the iliolumbar ligaments. *AJR* 2006. doi 10.2214/AJR.05.0415
- Hanhivaara J, Määttä JH, Kinnunen P, Niinimäki J, Nevalainen MT. Castellvi classification of lumbosacral transitional vertebrae: comparison between conventional radiography, CT, and MRI. *Acta Radiol* 2024. doi 10.1177/02841851241289355. PMID 39444351
- Lumbosacral transitional vertebra on whole-spine CT: prevalence and association with rib abnormalities. *Skeletal Radiol* 2025. doi 10.1007/s00256-025-04952-z. PMID 40381031
- Lumbosacral transitional vertebrae are associated with lumbar degeneration: retrospective evaluation of 3855 consecutive abdominal CT scans. *Eur Radiol* 2020. PMC7248049
- Prevalence, diagnosis, and clinical significance of lumbosacral transitional vertebrae: A systematic review and narrative analysis. 2025. PMC12549404
- Radiologic Insights: Diagnosing Lumbosacral Transitional Vertebrae. Systematic Review of the Literature. PMC12969546
- Lumbar plain radiograph is not reliable to identify lumbosacral transitional vertebra types according to Castellvi classification principle. PMC7260820
- Redefining lumbosacral transitional vertebrae classification: Morphological variation in a South African population. *Transl Res Anat* 2025;40. doi 10.1016/j.tria.2025.100421 (S2214854X25000421)
- Jenkins AL, et al. Redefining the Classification for Bertolotti Syndrome: Anatomical Findings in Lumbosacral Transitional Vertebrae Guide Treatment Selection. *World Neurosurg* 2023. PMID 36965661
- The Clinical Significance of Lumbar Transverse Process Lengths Associated with Lumbosacral Transitional Vertebrae: A Landmark for Lumbar Spine Enumeration. *World Neurosurg* 2024. PMID 38843967
- Bornstein PE, Peterson RR. Numerical variation of the presacral vertebral column in three population groups in North America. *Am J Phys Anthropol* 1966;25(2):139–46
- Lumbosacral Transitional Vertebrae Influence on Acetabular Orientation and Pelvic Tilt. PMC9457479

---

# RESUMED 2026-09-23 (second pass) — gaps the first pass left open

The first pass covered conditional shape generation, mask-to-image, deformation, tail-class
machinery, spine-specific generative work, LSTV morphology and prevalence. Three families
named in the task were not covered and are covered here: **counterfactual / causal anatomy
editing**, **vertebra-level inpainting in spine CT**, and **computational phantoms and
virtual imaging trials** — the last being the only family in this whole note with a
regulatory-grade external validation, and the only one whose output is a projection image
by design.

---

## 10. Counterfactual / causal editing — "change this attribute, leave the rest alone"

This is the family that formalises exactly our hardest sub-problem: *edit the lumbosacral
junction and do not silently change T12*. It is worth reading not for its results, which are
not on bone, but because it has already named and measured the failure mode.

### Evaluation of 3D Counterfactual Brain MRI Generation — MICCAI 2025, arXiv 2508.02880, PMID 41890356, PMC13012881, doi 10.1007/978-3-032-05472-2_5

- Generates: full 3-D brain MRI volumes under an intervention on an attribute (age, disease).
- Control: structural causal model — abduction (invert the structural equations for the
  exogenous noise), action (intervene), prediction (propagate).
- **Validation metric triad, which is the thing to steal**: *effectiveness* (did the
  intervened attribute actually change, measured by an independent predictor), *minimality*
  (did anything else change), *composition* (does a null intervention return the original).
- **The reported finding is a negative one and it is the relevant one: every model evaluated
  scores poorly on minimality.** The authors state the models "frequently induce unintended
  changes in other anatomical regions", i.e. inadequate disentanglement. Effectiveness was
  reasonable; locality was not.
- **Adversarial read**: brain MRI, soft tissue, no labels emitted. But it is direct published
  evidence that a conditional 3-D generator asked to change one anatomical thing changes
  others too — which in our setting means a requested L6 arriving alongside an unrequested
  change at T12 or in the pelvis. Any spine version must report minimality, and none has.

### Seg-CFT — Segmentor-Guided Counterfactual Fine-Tuning, arXiv 2509.24913; positional variant arXiv 2603.21213

- The published fix for the minimality failure: a segmentor supervises the fine-tuning so
  edits stay inside a named region.
- Code: `github.com/biomedia-mira/seg-cft` (BioMedIA, Imperial — the group behind the
  structural-causal-model line in medical imaging).
- Evaluated on chest radiographs with effectiveness / minimality / composition. I could not
  extract the numeric table from the PDF, so I quote no numbers from it.
- **Relevance**: the only published mechanism I found for *localising* a counterfactual edit
  using a segmentation the pipeline already has — and we hold per-vertebra segmentations for
  every CT. That combination is the honest reason to read it.

### "To do(x) or not to do(x): Medical Image Counterfactuals for Dataset Augmentation" — arXiv 2609.14124 (2026)

The only paper in this family that measures a **downstream gain from counterfactual
augmentation**, and it compares three conditioning designs head to head.

- Data: Morpho-MNIST (synthetic, known ground-truth conditionals), CheXpert (187k
  radiographs, 70/20/10), MIMIC as the shift test.
- Measured, on a deliberately biased CheXpert subset (pleural effusion correlated with sex):
  no augmentation **78.90 AUC** → deterministic conditional sampling **80.65** → **causal
  counterfactuals 81.67**. Gains largest at 1–20% label fractions.
- Fairness: the undirected (non-causal) design *widened* the age fairness gap (0.0774 vs
  0.0667 for causal) — getting the causal direction wrong actively hurt.
- Validation of the counterfactuals: exact log-likelihood against true conditionals on
  Morpho-MNIST; reverse-predictor proxies on CheXpert; FID/MMD/SSIM/LPIPS for image quality;
  L2 / covariance / nearest-neighbour for diversity.
- Code: not stated in the text I read.
- **Adversarial read**: 2-D classification, disease attributes not anatomy, +2.8 AUC points.
  It supports "conditional beats unconditional" (SV-Cine supports that far more strongly) and
  "get the causal direction right". It says nothing about 3-D bone.

---

## 11. Vertebra-level inpainting in spine CT — the only published machinery that deletes and regrows a whole vertebra with its label

### Bukas, Jian, Rodriguez Venegas, De Benetti, Ruehling, Sekuboyina, Gempt, Kirschke, Piraud, Oberreuter, Navab, Wendler — MICCAI 2021, doi 10.1007/978-3-030-87202-1_51, arXiv 2103.07279

Built for osteoplasty planning: take a patient CT plus the label of a *fractured* vertebra,
and produce the virtual healthy spine.

- Pipeline: three-step CNN segmentation → per-vertebra **rigid** registration to a healthy
  spine atlas (the "straightening" — vertebrae are re-posed, not deformed) → the target
  vertebra is masked out of **both the CT and the segmentation** using a binary mask built
  from its label → a coarse GAN generator, then a U-shaped refinement network whose **final
  layer emits both the inpainted image and the inpainted mask**.
- **This is the exact interface our requirement asks for — voxels and labels leave the same
  head, so they cannot drift apart.** It is the nearest published relative of "remove S1 from
  the sacrum and regrow it as an L6", and the only such method operating on vertebrae.
- Validation, in full: virtual vertebra volumes for **ten patients** against their healthy
  equivalents, **average error 3.88 ± 7.63 %**. That is an anatomical measurement against an
  external reference, which is more than most of this literature offers — but n=10, one
  scalar (volume), no shape metric, no HU fidelity, no reader study, **no downstream training
  gain**, and an SD twice the mean.
- Kirschke / Sekuboyina / Navab — the VerSe group, so the segmentation half is sound.
- Code: not stated on the abstract page; I found no repository.
- **Adversarial read**: it regenerates a vertebra *of the type that belongs there*, learned
  from the neighbours and an atlas. Asking it for a vertebra of a **different** type at that
  position is outside everything it was trained and validated to do, and there is no
  conditioning input with which to ask. Adapting it is new method work, not adoption.

### Related, weaker: "Inpainting Pathology in Lumbar Spine MRI with Latent Diffusion" (arXiv 2406.02477)

Voxel-wise noise scheduling to paint pathology onto healthy lumbar MRI. MRI, pathology not
anatomy, validation numbers not verified by me. Listed so the search is complete.

### HealthiVert-GAN (already in section 5) is the same mechanic in the other direction

Fracture → pseudo-healthy. Same "edit one vertebra in place", same absence of any
conditioning that could name a *different* vertebra type.

---

## 12. Computational phantoms and virtual imaging trials — the only family validated by replicating a real clinical trial, and the only one whose native output is a projection

Absent from the first pass and it should not have been. Not "generative" in the deep-learning
sense: the anatomy is an explicit geometric model and the image comes from simulating the
physics. Two properties put it directly on-requirement. **The labels are the model** — every
voxel's structure is known by construction, so alignment is exact and there is no resampling
question at all. And **the pipeline exists to produce projection images**, which is the half
no deep generative method has validated.

### VICTRE — Badano A, Graff CG, Badal A, et al. *JAMA Netw Open* 2018;1(7):e185474; FDA CDRH regulatory science tool; `github.com/DIDSR/VICTRE`, `github.com/DIDSR/VICTRE_MCGPU`, `didsr.github.io/VICTRE`; phantoms on TCIA

- Generates: stochastic 3-D anthropomorphic breast phantoms → Monte Carlo x-ray transport
  (MC-GPU) → digital mammography and tomosynthesis projections, plus a simulated reader.
- **Validation — the strongest external check in this entire note**: the in-silico trial was
  built to replicate a comparative DM-vs-DBT trial from a prior regulatory submission.
  **2,986 synthetic subjects, 31,055 DM and 27,960 DBT images; mean ΔAUC 0.0587 (SE 0.0062)
  favouring DBT; masses 0.090 (0.008), calcifications 0.027 (0.004) — consistent with the
  human trial** (>400 women, radiologist readers). The claim validated is not "the images
  look real"; it is "**the same regulatory decision comes out**". That is an external check
  of exactly the kind this project keeps asking for.
- Licence: FDA open source, phantoms public on TCIA.
- **Adversarial read, and it is severe for us**: breast, not bone. The anatomy comes from a
  stochastic tissue-growth procedure with no counterpart for a vertebral column. Nothing
  transfers except the *evidentiary standard* — it shows what a validated synthesis pipeline
  looks like, and sets a bar no spine work has met.

### XCAT 3.0 — Segars group / Duke CVIT, *Medical Image Analysis* 2025, doi 10.1016/j.media.2025.103636, PMID 40347915; preprint arXiv 2405.11133; `xcat-3.github.io`; library at cvit.duke.edu (request form)

- **>2,500 personalised phantoms, ~140 segmented structures each**, built by automated
  large-scale organ segmentation plus quality control over clinical CT — so the population
  variation is inherited from real patients rather than sampled from a model.
- Voxelised **and surface-mesh (NURBS)** representations; paired with **DukeSim**, a
  scanner-specific physics simulator, to emit synthetic CT.
- The NURBS representation is the interesting part: structures are defined by 3-D control
  points on non-uniform rational B-splines and can be non-rigidly deformed by moving them.
  Earlier XCAT work (Segars et al., **PMID 23556927**, "Population of anatomically variable
  4D XCAT adult phantoms") built an anatomically variable population this way; target
  phantoms are reached from a template by multichannel LDDMM.
- **What I could not confirm and am therefore not asserting**: whether XCAT 3.0 labels the
  spine *per vertebra*, and whether phantom bone carries trabecular texture or is a smooth
  material fill. Both decide everything for a DRR — a smooth-filled vertebra projects to a
  flat shape, and our task is naming a vertebra from its projected texture and outline. The
  existence of separate "textured XCAT phantom" work (ORNL, virtual clinical trial noise
  characterisation) suggests texture is an addition, not the default.
- **Downstream gain from XCAT-derived training data**: not established in what I read. The
  stated uses are system assessment, protocol optimisation and virtual reader studies — not
  network training gains with numbers.
- **The honest observation for this angle**: in a NURBS phantom, *adding a vertebra is an
  editing operation, not a research problem* — duplicate a body, place it, re-space the
  discs, and edit the ribs and sacrum as the separate surfaces they already are. It is the
  only representation in this note where the topology change is trivial. **Nobody has
  published it.** What is then owed is the hard part: show a DRR from a phantom looks like a
  radiograph of bone, and show the phantom lands inside the real population distribution of
  lordosis, pelvic incidence and transverse-process dimension.

---

## 13. Addendum to section 6 — a threshold the literature does not state consistently

The 19 mm that decides Castellvi type I is reported in two incompatible ways:

- **AJNR** (Konin & Walz 2010, 31(10):1778–86): enlarged transverse processes measuring at
  least **19 mm craniocaudally**.
- Several secondary sources and review figures: at least **19 mm in width**; "large,
  triangular transverse process measuring at least 19 mm in width".

These are different dimensions of the same process and they will not agree on the same bone.
Any generator claiming to place a case at type I must say **which axis it controls** and
measure it the way the source it cites measured it. This is the same substitution this
project has already been burned by — a maximum extent is not a named dimension — except that
here it is in the literature rather than in our code. Treat the AJNR craniocaudal reading as
primary and state the axis explicitly.

---

## 14. Added to "what is not known"

- **Nobody has measured minimality for a spine edit.** The one paper that measured it at all
  (3-D brain counterfactuals) found every model failed it. For us the untested question is
  whether making an L6 leaves T12 and the pelvis alone — and the published morphometry
  (LSTV columns have longer transverse processes at *every* lumbar level, most at L3;
  LSTV alters acetabular orientation and pelvic tilt) says the right answer is that it should
  **not**. So minimality is the wrong target and "did the whole column move the way LSTV
  columns move" is the right one. No published work states that target, let alone measures it.
- **No spine synthesis has been validated by replicating an external result.** VICTRE shows
  what that looks like and it exists only for breast.
- **Whether phantom-class bone survives a DRR is unknown to me.** I could not confirm whether
  XCAT vertebrae carry trabecular texture, and that answer decides whether the phantom route
  is viable here at all.
- **Bukas et al.'s inpainter has no conditioning input.** There is no published way to ask a
  vertebra inpainter for a vertebra of a type other than the one that belongs at that level.

---

## Citations added in the second pass

- Evaluation of 3D Counterfactual Brain MRI Generation. MICCAI 2025. arXiv:2508.02880. PMID 41890356. PMC13012881. doi 10.1007/978-3-032-05472-2_5
- Segmentor-Guided Counterfactual Fine-Tuning for Locally Coherent and Targeted Image Synthesis (Seg-CFT). arXiv:2509.24913. github.com/biomedia-mira/seg-cft
- Positional Segmentor-Guided Counterfactual Fine-Tuning for Spatially Localized Image Synthesis. arXiv:2603.21213
- To do(x) or not to do(x): Medical Image Counterfactuals for Dataset Augmentation. arXiv:2609.14124
- Bukas C, Jian B, Rodriguez Venegas LF, De Benetti F, Ruehling S, Sekuboyina A, Gempt J, Kirschke JS, Piraud M, Oberreuter J, Navab N, Wendler T. Patient-specific virtual spine straightening and vertebra inpainting: an automatic framework for osteoplasty planning. MICCAI 2021. doi 10.1007/978-3-030-87202-1_51. arXiv:2103.07279
- Inpainting Pathology in Lumbar Spine MRI with Latent Diffusion. arXiv:2406.02477
- Badano A, Graff CG, Badal A, et al. Evaluation of digital breast tomosynthesis as replacement of full-field digital mammography using an in silico imaging trial. JAMA Netw Open 2018;1(7):e185474. github.com/DIDSR/VICTRE; github.com/DIDSR/VICTRE_MCGPU
- Abadi E, Segars WP, et al. XCAT 3.0: a comprehensive library of personalized digital twins derived from CT scans. Med Image Anal 2025. doi 10.1016/j.media.2025.103636. PMID 40347915. arXiv:2405.11133. xcat-3.github.io
- Segars WP, et al. Population of anatomically variable 4D XCAT adult phantoms for imaging research and optimization. Med Phys 2013. PMID 23556927
- Konin GP, Walz DM. Lumbosacral transitional vertebrae: classification, imaging findings, and clinical relevance. AJNR 2010;31(10):1778-86 — re-cited for the "19 mm craniocaudally" wording
