# Statistical shape and shape-intensity models of the spine — prior art

Angle: point-distribution models, statistical shape + intensity models (SSIM/SSAM) that carry grey
values, articulated spine models, vertebra-level SSMs, and the general-purpose toolkits.
Searched 2026-09-23. Nothing implemented; this is an evidence file.

Requirement being judged against (restated): in = CT + per-vertebra labels; out = NEW volumes WITH
aligned labels that still render as radiographs; control = target lordosis / kyphosis / transitional
phenotype; variation must be population-plausible and must not fabricate anatomy that does not occur.

---

## Headline — the four questions, answered up front

**1. Does any published spine SSM generate a full CT (intensities), rather than a surface? No.**
Not one. Every spine SSM found here outputs surfaces, meshes, particles or FE elements. The one
paper that put grey values inside a *vertebra* (Day 2022) built its appearance field from 14 µCT
specimens and used it to drive an FE stiffness prediction, not to write an image. The only
image-producing shape-*and*-intensity model on bone CT in the literature is Schmid 2023, and it is
**hip**, not spine. That model is the strongest candidate in this whole angle, and it would have to
be ported to the spine by us.

**2. Generalisation and specificity: reported, but rarely credible and almost never comparable.**
The 2026 scoping review of 85 lumbar-spine SSM studies (Wai 2026) states the metrics were "applied
inconsistently and rarely accompanied by acceptability thresholds", and that **none of the 85
studies demonstrated a change to clinical practice**. The best-reported numbers in the field are
sub-millimetre (Rasouligandomani 2024: generalisation RMSE 0.36 ± 0.24 mm, specificity 0.45 ± 0.21 mm)
— but see the adversarial note in §B10: those were computed against sterEOS template reconstructions,
not against raw segmentations, so they largely measure how well a template refits its own family.

**3. Is any spine SSM trained on enough subjects to sample genuinely new plausible spines?**
Barely. Scoping-review mean training set = **153 participants** (range 3–2,520); 55% of studies used
10–99. The largest spine model that includes the sacrum and pelvis was built on **42** subjects. The
only public full-spine surface model (Meng 2020) was learned from VerSe 2019 partial views.
**This project holds ~2,900 labelled CTs. By the standards of this literature that is an order of
magnitude more than anyone has ever fitted a spine SSM to.** That is a real opportunity, and it is
also the one thing that could make a spine SSM here better than the published ones.

**4. Has anyone modelled the whole lumbosacral junction, sacrum and pelvis together? Once.**
Rasouligandomani 2024 (Sci Data) — T1 through S1 plus sacrum, pelvis and femoral head — n=42, EOS
not CT, meshes only, released CC BY 4.0. Everything else is lumbar-only, or sacrum-only, or
pelvis-only, and the separate sacrum/pelvis SSMs were never joined to a spine SSM.

**5. Is there any SSM that represents a variable NUMBER of vertebrae? No. Nothing. Anywhere.**
This is the cleanest negative result in the whole angle. A PDM is a fixed-length vector of
corresponding points; correspondence is the entire premise. An L6 spine has no correspondence with
an L5 spine at the lumbosacral junction, so it cannot enter the same model. The nearest work in the
wider SSM literature is multi-organ modelling with shared boundaries and multi-level component
analysis (Iyer & Elhabian 2023) — which handles several objects, not a variable count of them. If we
want transitional anatomy from an SSM, we would have to fit **separate models per phenotype**
(5-lumbar, 6-lumbar, sacralised, 4-lumbar) and we would then be back to the 86-subject scarcity that
started this, split four ways. **This family cannot manufacture a transitional vertebra.**

**Bottom line for the requirement.** As a *whole* solution, no. As a *component*, one candidate is
strong: a spine SSIM in the Schmid 2023 mould — tetrahedral mesh + Bernstein-encoded intensities,
sampled under a χ² plausibility constraint — is the only published, validated route in this family
from "labelled bone CT" to "new CT volume with aligned labels". It is the only method here with a
measured downstream gain on bone CT. It is also the only one where the labels come out for free,
because the sample *is* a labelled mesh before it is an image.

---

## A. What an SSM can and cannot output (and why that decides most of this)

A point-distribution model is Procrustes-aligned corresponding points → PCA → sample
`x = x̄ + Σ bᵢ√λᵢ φᵢ`. Three consequences that matter here:

- **A sample is a shape, not an image.** To get a CT you need an additional intensity model, or you
  warp a real CT onto the sampled shape (which is then a registration method, not an SSM — see the
  polyaffine family in `biomech.md`).
- **Labels are free.** If the model is a labelled mesh or a labelled tetrahedral volume, a sample is
  labelled by construction. No alignment can drift. This is the single strongest property of this
  family against our requirement, and it is the property that diffusion models lack.
- **Plausibility has an accepted operational definition.** Constrained sampling — `bᵢ ∈ [−2.5√λᵢ,
  +2.5√λᵢ]` plus a Mahalanobis/χ² bound `Σ bᵢ²/λᵢ ≤ M` — is the standard way the field says "do not
  fabricate anatomy that does not occur". It is a *distributional* guarantee, not an anatomical one:
  it keeps you inside the ellipsoid the training set spans. It cannot tell you whether the training
  set spanned the anatomy. That distinction matters for us because our tails (lordosis, PI,
  transitional) are exactly the thin places.

Reviews: Sarkalkan N, Weinans H, Zadpoor AA. *Statistical shape and appearance models of bones.*
Bone 2014;60:129–140. DOI 10.1016/j.bone.2013.12.006, PMID 24334169. Still the standard reference for
the shape-vs-appearance distinction.

---

## B. Shape-only spine SSMs (surfaces / meshes)

### B1. Boisvert — articulated statistical model of the scoliotic spine
Boisvert J, Cheriet F, Pennec X, Labelle H, Ayache N. *Geometric variability of the scoliotic spine
using statistics on articulated shape models.* IEEE Trans Med Imaging 2008;27(4):557–568.
DOI 10.1109/TMI.2007.911474, PMID 18390352.
- **Generates:** a vector of relative rigid poses between neighbouring vertebral coordinate systems —
  i.e. *alignment*, not vertebral shape and not intensity. Because rigid transforms are not a vector
  space, the mean is a Fréchet mean and the covariance a generalised covariance on the Lie group.
- **Data:** 295 scoliotic patients (3-D reconstructions from bi-planar radiographs), plus deformation
  sub-studies: 33 Cotrel-Dubousset surgeries, 39 Boston brace, 26 untreated progression.
- **Validation:** descriptive. Modes of variability are reported and interpreted anatomically
  (lumbar inter-vertebral poses more variable than thoracic). **No generalisation or specificity
  error is reported, and the model is not validated as a generator.** This is a variability-analysis
  paper, not a synthesis paper — worth being explicit about, because it is routinely cited as though
  it were the latter.
- **Code:** none released. Book-chapter treatment: Boisvert J, *Articulated Statistical Shape Models
  of the Spine*, in Li & Yao (eds), Spinal Imaging and Image Analysis, Springer 2015,
  DOI 10.1007/978-3-319-12508-4_10.
- **Fit:** gives the right *formalism* for controlling alignment (lordosis/kyphosis live in the pose
  vector), on a scoliotic population, from radiographs. No intensities, no sacrum, no pelvis.
- **Verified adversarially 2026-09-23 against the full text: see section V at the end of this file. Verdict REJECT as a synthesis method; two parts worth keeping.**

### B2. Kadoury — articulated spine models and manifold ensembles
- Kadoury S, Labelle H, Paragios N. *Automatic inference of articulated spine models in CT images
  using high-order Markov Random Fields.* Med Image Anal 2011;15(4):426–437.
  DOI 10.1016/j.media.2011.01.006.
- Kadoury S, Labelle H, Parent S. *3D spine reconstruction of postoperative patients from multi-level
  manifold ensembles.* MICCAI 2014, DOI 10.1007/978-3-319-10443-0_46; and *Postoperative 3D spine
  reconstruction by navigating partitioning manifolds*, Med Phys 2016;43(3):1045–1056.
  DOI 10.1118/1.4940792.
- **Generates:** an articulated spine configuration inferred from images; the manifold is a *prior for
  inference*, used as a search space, not sampled to make new datasets.
- **Validation (read from abstracts, not full text — flag):** radiographic phantom RMS 3-D landmark
  reconstruction error 2.0 mm; vertebra localisation ~0.5 mm; orientation to 1.5° except axial
  rotation (3.3° moderate, 4.4° severe cases). These are *reconstruction* accuracies — they say the
  manifold is a good prior, they say nothing about whether samples from it are plausible spines.
- **Code:** none found.

### B3. Rasoulian — statistical multi-vertebrae shape + pose model
Rasoulian A, Rohling R, Abolmaesumi P. *Lumbar spine segmentation using a statistical multi-vertebrae
anatomical shape+pose model.* IEEE Trans Med Imaging 2013;32(10):1890–1900.
DOI 10.1109/TMI.2013.2268424, PMID 23771318. Extended to thoracic in MICCAI-CSI 2014
(DOI 10.1007/978-3-319-14148-0_19) and to ultrasound/CT registration (Int J CARS 2016, PMID 26984554).
- **Generates:** L1–L5 surfaces *and* their relative poses in one joint model — the cleanest published
  factorisation of "what a vertebra looks like" from "where it sits", which is exactly the
  factorisation our lordosis-control requirement needs.
- **Validation:** the TMI 2013 paper reports **32 subjects, mean error below 2 mm** (segmentation task).
  The **1.17 ± 0.38 mm over 16 subjects** often quoted here is the SPIE 2013 conference paper
  (Proc SPIE 8671, DOI 10.1117/12.2007448), not the journal paper — see the verification section at the
  end of this file, which also records that the method came **last of five** in the CSI2014 benchmark.
- **Code:** none released that I could find.
- **Adversarial:** again a segmentation paper. Generalisation/specificity of the generator are not
  reported, and 16 test subjects is not a population.

### B4. Klinder — articulated shape + gradient + appearance models of all presacral vertebrae
Klinder T, Ostermann J, Ehm M, Franz A, Kneser R, Lorenz C. *Automated model-based vertebra detection,
identification, and segmentation in CT images.* Med Image Anal 2009;13(3):471–482.
DOI 10.1016/j.media.2009.02.004, PMID 19285910. Earlier: *Spine segmentation using articulated shape
models*, MICCAI 2008, DOI 10.1007/978-3-540-85988-8_28.
- **Generates:** triangulated vertebra surfaces in a two-scale (global spine / local vertebra) frame,
  with *learned gradient and appearance profiles* attached to the mesh.
- **Validation:** mean point-to-surface error 1.12 mm (MedIA 2009); 1.0 mm mean over ten thoracic CTs
  (MICCAI 2008).
- **Note:** the appearance component here is a 1-D intensity profile *along the surface normal* for
  boundary detection. It is not a volumetric intensity field and cannot write a CT. Anyone citing
  Klinder as "an appearance model of the spine" is overclaiming; I nearly did.

### B5. Castro-Mateos — Statistical Interspace Models
Castro-Mateos I, Pozo JM, Pereañez M, Lekadir K, Lazáry A, Frangi AF. *Statistical Interspace Models
(SIMs): application to robust 3D spine segmentation.* IEEE Trans Med Imaging 2015;34(8):1663–1675.
(Two DOIs surfaced in indexing — 10.1109/TMI.2015.2443912 and 10.1109/TMI.2015.2456376; **I could not
resolve which is correct.**)
- **Generates:** a model of the *interspace* between adjacent structures — relative position vectors
  between facing point pairs — so that independently-modelled vertebrae do not interpenetrate.
- **Why it is relevant to us:** it is the published answer to the exact problem that will bite any
  per-vertebra generator: sample five vertebrae independently and the articular processes overlap.
  SIMs solve that with far less training data than a joint multi-object SSM needs.
- **Validation:** segmentation accuracy on spine CT; I did not obtain the numeric table.
- **Code:** none found.

### B6. Meng / Keller / Pujades — the only public full-spine statistical surface model
Meng D, Keller M, Boyer E, Black M, Pujades S. *Learning a Statistical Full Spine Model from Partial
Observations.* ShapeMI @ MICCAI 2020, LNCS 12474:122–133. DOI 10.1007/978-3-030-61056-2_10.
HAL hal-02983880.
- **Generates:** surfaces of all 24 presacral vertebrae (C7 + T12 + L5) with per-vertebra joints and a
  shape space — learned *from partial views*, which is the trick, because no public dataset images the
  whole spine.
- **Data:** VerSe 2019.
- **Validation:** given a partial observation (a few vertebrae), predicts the shape of unseen vertebrae
  with **mean error under 3 mm**. That is a genuine held-out generative test — better evidence than
  most of this angle offers — but it is a *completion* test, not a specificity test.
- **Code:** https://gitlab.inria.fr/spine/spine_model — **non-commercial licence**. Given this
  project's standing commercialization track, that licence is a hard blocker for anything downstream
  of the two-track rule, and should be treated as such from the start.
- **No sacrum, no pelvis, no intensities.**

### B7. Hollenbeck — lumbar shape *and alignment* SSM from CT
Hollenbeck JFM, Cain CM, Fattor JA, Rullkoetter PJ, Laz PJ. *Statistical shape modeling characterizes
three-dimensional shape and alignment variability in the lumbar spine.* J Biomech 2018;69:146–155.
PMID 29402403.
- **Data:** 52 patient CTs. **Finding relevant to control:** scaling dominates mode 1 in every model;
  vertebral size tracks stature, sex and age; lumbar *curvature* tracks stature and age; later modes of
  the whole-spine model describe disc height and lordosis. So lordosis is reachable as a shape mode —
  but it is entangled with size and is not an independent control knob.

### B8. Clouthier — morphable lumbar model with *named* control parameters (best control story here)
Clouthier AL, Wenghofer J, Wai EK, Graham RB. *Morphable models of the lumbar spine to vary geometry
based on pathology, demographics, and anatomical measurements.* J Biomech 2023;146:111421.
DOI 10.1016/j.jbiomech.2022.111421, PMID 36603365.
- **Generates:** lumbar vertebral surfaces, morphed along **19 named parameters** (disc herniation,
  spondylolisthesis, sex, age, vertebral body dimensions, facet angles, canal depth …) using partial
  least squares regression rather than raw PCA modes.
- **Data:** 87 patients.
- **Validation — and this is the good part:** the pathology/sex models were tested **against random
  permutation models** (herniation p<0.04, spondylolisthesis p<0.001, sex p<0.01), which is a proper
  null, not an eyeball test. Control fidelity was measured by asking for a target and measuring what
  came out: RMSE **< 0.8°, < 0.3 cm², < 0.7 mm** between desired and resulting measurement. Age
  prediction RMSE 14.1 years.
- **Code:** https://github.com/aclouthier/morphable-lumbar-model — **MIT licence**, MATLAB and Python,
  the model ships with the repo. Mirror at UOttawa-Biomechanics-and-Analytics/morphable-lumbar-model.
- **Fit:** the only published spine shape model that lets you *ask for a number and get it back*, with
  the error on that round-trip measured. Surfaces only; no sacrum; no intensities; n=87.
- **Downstream gain:** none measured.

### B9. Campbell & Petrella — SSM → virtual population of lumbar FE models
Campbell JQ, Petrella AJ. *Automated finite element modeling of the lumbar spine: using a statistical
shape model to generate a virtual population of models.* J Biomech 2016;49(13):2593–2599.
PMID 27270207.
- **Data:** 18 cadaveric specimens. That is too few to sample a population from and the paper is
  routinely cited as if it were not.
- **Generates:** FE meshes. No images.

### B10. Rasouligandomani — thoracolumbar spine **+ sacrum + pelvis + femoral head**, 16,807 models
Rasouligandomani M, et al. *Dataset of Finite Element Models of Normal and Deformed Thoracolumbar
Spine.* Sci Data 2024;11:549. DOI 10.1038/s41597-024-03351-8. PMC11137096.
- **Generates:** T1–S1 plus sacrum, pelvis and femoral head, as triangulated surfaces (.stl) and
  hexahedral FE meshes (.inp, Abaqus). **16,807 virtual models** = first 5 PCs × 7 levels
  (−3σ … +3σ) = 7⁵. Spinopelvic parameters (PI, PT, SS …) annotated on every model.
- **Data:** **42** non-operated adult-spine-deformity patients, age 50–75, **EOS biplanar radiographs**
  reconstructed with sterEOS — not CT.
- **Validation:** compactness (5 modes = 95% variance); **generalisation RMSE 0.36 ± 0.24 mm;
  specificity RMSE 0.45 ± 0.21 mm**; FE range-of-motion compared against in-vitro/in-vivo experiments
  with up to **28.57%** maximum difference.
- **Availability:** Zenodo, 694 GB, **CC BY 4.0**. BCPD++ registration code on GitHub.
- **Adversarial:** the sub-half-millimetre generalisation and specificity are not what they look like.
  The training shapes are themselves sterEOS *template* reconstructions — smooth, already
  parameterised, already from one generative family. Fitting a template SSM to template
  reconstructions and then measuring how well the template refits them is close to circular. The
  honest reading is that 0.36 mm measures mesh-morphing fidelity, not anatomical coverage. Separately:
  the 16,807 models are a **deterministic grid** over 5 modes, not a sample from the distribution, so
  their joint density is uniform-on-a-lattice and bears no relation to the population density — they
  are a design-of-experiments sweep, and calling the collection a cohort would be wrong. The 28.57%
  ROM discrepancy is the only external check, and it is large.
- **Fit:** nonetheless, *the* closest published thing to our anatomical scope, released under a usable
  licence, with spinopelvic parameters attached. Worth reading in full before building anything.

### B11. Sacrum and pelvis SSMs (never joined to a spine model)
- Van Hauwermeiren L, Audenaert E, Van Houcke J, Matthews H, Claes P, Delrue L, Achten E, Adriaens D,
  Van Hoof T. *A statistical shape model of the human female sacrum: an integrative analysis of form.*
  J Anat 2026. DOI 10.1111/joa.70148, PMID 42046330. **109 female CTs**; two dominant components =
  sacral size and sagittal curvature.
- Wagner D, et al. *Morphometry of the sacrum and its implication on trans-sacral corridors using a CT
  data-based 3-D statistical model.* Spine J 2017, PMID 28373081. 92 intact pelves, mean age 61.5.
  Includes **bone-mass distribution** as well as shape — one of the very few spine-region models that
  carries a density field at all.
- Hemipelvis SSM, 200 CTs (100 M / 100 F), first 15 PCs = 90% of variance. PMC10253964.
- Pelvis morphometric model, 132 adult CTs, sparse PCA; sacral curvature 31.9% and length 15.2% of
  variance. DOI 10.1016/j.jbiomech.2021.110646 (J Biomech 2021).
- **None of these connects to a lumbar model.** A sacrum SSM and a lumbar SSM fitted separately will
  not articulate; that is precisely what Castro-Mateos's interspace models exist to fix.

### B12. Other lumbar SSMs worth knowing
- *A statistical lumbar spine geometry model accounting for variations by age, sex, stature and BMI.*
  J Biomech 2021, DOI 10.1016/j.jbiomech.2021.110848 — demographic control, surfaces only.
- Pavlova A, et al. *Statistical shape modelling of hip and lumbar spine morphology and their
  relationship in the MRC National Survey of Health and Development.* J Anat 2017, PMC5522893,
  PMID 28561274 — **1,511 individuals**, DXA (2-D), the largest spine SSM cohort I could confirm.
- Foltz M, et al. *Application of statistical shape models to standard lumbar MRI for stenosis
  treatment stratification.* JOR Spine 2026, DOI 10.1002/jsp2.70189.
- Bourigault E, Jamaludin A, Zisserman A. *3D spine shape estimation from single 2D DXA.* MICCAI 2024
  (oral), DOI 10.1007/978-3-031-72086-4_1; code https://github.com/EmmanuelleB985/DXA-to-3D.
  Trained on >30k paired DXA/MRI (UK Biobank app. 17295). 3-D curve deviation **3.12 mm**, 3-D spine
  mask IoU **83.8**. Inference, not synthesis, but it is the largest-scale 3-D spine shape work here.

---

## C. Shape **and intensity** models — the only ones that can write an image

### C1. Schmid — SSIM augmentation for hip-bone CT segmentation ★ the strongest candidate in this angle
Schmid J, Assassi L, Chênes C. *A novel image augmentation based on statistical shape and intensity
models: application to the segmentation of hip bones from CT images.* Eur Radiol Exp 2023;7:39.
DOI 10.1186/s41747-023-00357-6, PMID 37550543. PMC10406777.
- **Generates:** a **full CT-like volume with an aligned label**, not a surface. A reference triangular
  mesh is non-rigidly registered to each training segmentation, converted to a volumetric tetrahedral
  mesh (TetGen) and warped by thin-plate spline; image intensity *inside* each tetrahedron is encoded
  with **barycentric Bernstein polynomials of degree 3 (20 coefficients per tetrahedron)**. PCA over
  shape and over density gives an SSM and an SIM; sampling both and rasterising gives a new image.
  Mesh sizes: proximal femur 8,734 vertices / 52,220 tets; hipbone 20,626 vertices / 116,062 tets.
  Modes kept to 95% variance: femur 17 SSM / 71 SIM; hipbone 50 SSM / 151 SIM.
- **Control / plausibility:** constrained sampling, `bᵢ ∈ [−2.5√λᵢ, 2.5√λᵢ]` and `Σ bᵢ²/λᵢ ≤ M` (χ²).
  This is *unconditional but bounded*. There is no mechanism to ask for a target parameter — that
  would have to be added (Clouthier's PLS or Boutillon's ANAT-SSM, §E3, are the published ways).
- **Intensity fidelity, measured:** absolute relative error between real CT intensities and the
  Bernstein encoding **< 10%**. This is the one anatomical-fidelity number in the family that is about
  grey values rather than surfaces.
- **Data:** 232 preoperative THA patients (112 M / 120 F, mean age 74.4) from several institutions;
  25% carry metal artefact, >65% osteophytes. **Not public** (ethics restriction).
- **DOWNSTREAM GAIN — measured, and modest. Residual U-Net (MONAI), 5-fold CV, Dice+CE, Adam 1e-4,
  50 epochs on 4× V100:**

  | augmentation | Dice (median [IQR]) | Hausdorff mm (median [IQR]) |
  |---|---|---|
  | none | 0.93 [0.90–0.95] | 8.06 [5.83–11.36] |
  | basic (flips, 90° rot, ±10% intensity) | 0.93 [0.90–0.95] | 7.35 [5.48–9.90] |
  | **SSIM alone** | **0.93 [0.91–0.95]** | **7.81 [5.83–10.36]** |
  | basic + SSIM | **0.95 [0.93–0.96]** | **6.16 [4.90–8.08]** |

  External validation on CTPelvic1K (31 images, hipbone): Dice 0.95 ± 0.054, HD 7.0 ± 5.8 mm.
  Significance by Mann–Whitney with Bonferroni, α=0.05.
- **Read this adversarially, because it is the number the whole angle rests on.** SSIM **alone did not
  beat basic augmentation** — same Dice, *worse* Hausdorff (7.81 vs 7.35 mm). The gain appears only in
  combination: +0.02 Dice and −1.9 mm HD over no augmentation, +0.02 Dice and −1.2 mm over basic. On a
  task already at 0.93 Dice. That is a real, statistically tested, externally validated result and it
  is also a *small* one, obtained on an easy task where the ceiling was close. Whether it transfers to
  a hard task (naming a vertebra from one rendered frame) is completely unevidenced.
- **Code:** **not released.** Only MONAI (Apache 2.0) and PyTorch (BSD) are named. Reimplementation
  would be needed: TetGen + TPS + Bernstein encoding + two PCAs. Days-to-weeks of work, not novel.
- **Compute:** 4× V100 32 GB, 50 epochs; offline pre-augmentation. Wall clock not disclosed.
- **Fit against our requirement:** the only published method in this family that satisfies
  *out = new volume with aligned label*. Spine-specific? No — hip. Conditional? No, not as published.
  Handles a transitional vertebra? No.

### C2. Day — SSAM of lumbar vertebrae carrying bone density (the only spine shape+intensity model)
Day GA, Jones AC, Wilcox RK. *Using Statistical Shape and Appearance Modelling to characterise the 3D
shape and material properties of human lumbar vertebrae: a proof of concept study.* J Mech Behav
Biomed Mater 2022;126:105047. DOI 10.1016/j.jmbbm.2021.105047. White Rose eprints 183110.
- **Generates:** vertebral geometry **plus a bone-density field**, as an FE model.
- **Data:** **14** human lumbar vertebrae, µCT, with experimental mechanical validation.
- **Validation:** mean error between input specimens and generated models — volume **10%**, mean
  density **3%**, FE compressive stiffness **10%**. PC1 captured most of the density variation; later
  PCs were geometric.
- **Adversarial:** the authors call it a proof of concept themselves and say the input set is limited.
  Fourteen specimens cannot span a population; the density field is µCT-derived, not clinical-CT HU;
  and the output is an FE model, **not an image**. It is the right *idea* on the right *anatomy* at
  1/16th the sample size of Schmid and with no image ever produced.

### C3. La Mattina — virtual cohort from a statistical anatomy atlas (how to validate plausibility)
La Mattina AA, Baruffaldi F, Taylor M, Viceconti M. *Statistical properties of a virtual cohort for
in silico trials generated with a statistical anatomy atlas.* Ann Biomed Eng 2022;51(1):117–124.
DOI 10.1007/s10439-022-03050-8, PMID 36066781. PMC9832093.
- **Generates:** synthetic proximal femurs as tetrahedral FE meshes with **element-wise Young's moduli
  mapped from CT via Bonemat V3** — i.e. shape + density, like Schmid but for biomechanics.
- **Data:** 94 post-menopausal women (47 fractured / 47 not, pair-matched). **1,080 synthetic femurs
  generated, 1,044 usable** (rest failed on element distortion / convergence).
- **Sampling:** inverse-transform sampling on **all 93 PCs** so the marginal distributions are
  preserved — notably *not* a Gaussian ellipsoid, and not a lattice sweep. Heights and weights
  assigned by regression to preserve their weak correlation with density.
- **HOW PLAUSIBILITY WAS VALIDATED — this is the part worth stealing.** They did not say "looks
  realistic". They ran the downstream biomechanical pipeline on the virtual cohort and compared
  *distributions* against the real cohort: absolute risk of fracture stayed bimodal, low-risk
  component 28 ± 12% virtual vs 29 ± 12% physical, high-risk 63 ± 15% vs 55 ± 13%; the real cohort's
  classification threshold (39%) split the virtual cohort 50.9% / 49.1% against the physical 48.9%;
  T-scores, heights, weights and BMIs not significantly different (p > 0.05, Kolmogorov–Smirnov).
  **That is the template for how we should validate any generator we build** — and it maps directly
  onto our own instruction to check against something outside the computation. Our analogue: sample,
  then push the samples through the *spinopelvic estimator* and the *level-morphometry* pipeline and
  compare the resulting PI / SS / LL / canal-depth / end-plate-width distributions, spread included,
  against the real cohort and against published normative series.
- **Data availability:** http://doi.org/10.6092/unibo/amsacta/6891, **CC BY-NC-SA 4.0**. MATLAB 2019b,
  NumPy/SciPy/scikit-learn.
- **Femur, not spine. No image is produced.**

---

## D. SSM-driven *image* synthesis in the spine — one instance, and it is 2-D MRI

### D1. SSMSpine / SymTC
Chen J, Qian L, Ma L, Urakov T, Gu W, Liang L. *SymTC: a symbiotic Transformer-CNN net for instance
segmentation of lumbar spine MRI.* Comput Biol Med 2024;179:108795.
DOI 10.1016/j.compbiomed.2024.108795, PMID 38955128. arXiv 2401.09627.
- **Generates:** synthetic **mid-sagittal lumbar spine MR images** with instance masks, from an SSM of
  disc and vertebra contours **combined with biomechanics** to deform them.
- **Size:** the repository states **12,500 synthetic 512×512 images** (raw, intensity-corrected and
  intensity-equalised versions, masks and landmarks, PyTorch tensors). The paper describes splits of
  7,000 train / 250 val / 2,500 test. **Those do not add to 12,500 and I could not reconcile them** —
  the full-text PDF would not extract. Flagging rather than guessing.
- **Downstream:** SymTC reaches **Dice 96.169%** on SSMSpine, best of 17 methods compared. **This is a
  performance number ON the synthetic set, not a measured gain FROM adding it to real training.** I
  could not obtain a with/without-synthetic ablation on the real dataset, and I will not assert one.
  As evidence for augmentation value it is therefore weak — it shows the synthetic set is learnable,
  which is not the same as useful.
- **Code / data:** https://github.com/jiasongchen/SymTC and .../SSMSpine — "research purposes only",
  **no formal open-source licence**, which is not the same as permissive.
- **Fit:** 2-D, sagittal, MRI. Nothing about it survives the jump to a 3-D CT that has to be rendered
  from arbitrary angles. Cited here because it is the *only* published spine SSM→image pipeline.

### D2. Artificial enlargement of the SSM training set (a sideways answer to scarcity)
- Ghaffari M, et al. *Artificially enriching the training dataset of statistical shape models via
  constrained cage-based deformation.* Phys Eng Sci Med 2019;42(2):539–551. PMID 31087232.
  Two-step cage handle displacement transferred to mesh vertices; reported to beat other
  data-generating methods **on generalisation and specificity**.
- Koikkalainen J, et al. *Methods of artificial enlargement of the training set for statistical shape
  models.* IEEE Trans Med Imaging 2008;27(11):1643–1654. PMID 18955179. The original systematic
  comparison of these methods.
- **Relevance:** if we build an SSM on a thin stratum (86 transitional subjects), this is the published
  literature on whether you can inflate it — and the honest answer is that these methods improve the
  *model's* generalisation/specificity metrics without adding any real anatomical information. They
  fix a fitting problem, not a data problem.

---

## E. Toolkits

| tool | licence | what it gives | URL |
|---|---|---|---|
| **ShapeWorks** (Univ. of Utah, SCI) | **MIT** | particle-based / entropy-optimised correspondence; no parameterisation, handles open surfaces and arbitrary topology; Studio GUI + Python API | github.com/SCIInstitute/ShapeWorks, sciinstitute.github.io/ShapeWorks |
| **Deformetrica** (ICM / Aramis) | **MIT** | LDDMM: atlas estimation, geodesic regression, parallel transport, shape generation | gitlab.com/icm-institute/aramislab/deformetrica, deformetrica.org |
| **Scalismo** (Univ. Basel, Gravis) | **Apache 2.0** | Gaussian Process Morphable Models; Scala; model-based image analysis | github.com/unibas-gravis/scalismo, scalismo.org |
| **Statismo** | **BSD** | C++/ITK/VTK PCA shape+image models | github.com/statismo/statismo — **the repository states it is no longer maintained** |
| **SlicerSALT** | 3D Slicer (BSD-style) | SPHARM-PDM, shape regression, populations analysis, as a Slicer custom app | salt.slicer.org |

- **E1. Benchmark between them.** Goparaju A, Iyer K, Bône A, Hu N, Henninger HB, Anderson AE,
  Durrleman S, Jacxsens M, Morris A, Csecs I, Marrouche N, Elhabian SY. *Benchmarking off-the-shelf
  statistical shape modeling tools in clinical applications.* Med Image Anal 2022;76:102271.
  PMID 34974213, arXiv 2009.02878. **ShapeWorks and Deformetrica are more consistent than SPHARM-PDM**
  (groupwise correspondence estimation) and better capture clinically relevant population-level
  variability. I did **not** obtain the per-tool compactness/generalisation/specificity tables from the
  abstract — they are in the full text and should be read before choosing a tool. **No spine anatomy
  in the benchmark** as far as I could confirm.
- **E2. GPMM — the formalism that unifies the above.** Lüthi M, Gerig T, Jud C, Vetter T. *Gaussian
  Process Morphable Models.* IEEE Trans Pattern Anal Mach Intell 2018;40(8):1860–1873. PMID 28816655.
  Generalises PDMs so the deformation prior is a GP kernel rather than only the sample covariance —
  which is the standard escape hatch when the training set is too small for PCA to span the space, and
  therefore the standard escape hatch for our 86 transitional subjects. Implemented in Scalismo.
  Applied to the lumbar spine in a 2026 IJCARS proof of concept (DOI 10.1007/s11548-026-03757-2),
  which I could not read past the paywall.
- **E3. Making an SSM conditional on named measurements.** Boutillon A, Salhi A, Burdin V, Borotikar B.
  *Anatomically Parameterized Statistical Shape Model.* IEEE Trans Biomed Eng 2022.
  DOI 10.1109/TBME.2022.3152833, arXiv 2202.08580. Learns a linear map between shape coefficients and
  chosen anatomical parameters and inverts it, with orthogonality constraints so the controls are
  independent. Demonstrated on **femur and scapula, not spine**. This plus Clouthier's PLS are the two
  published routes to the conditional control our requirement asks for.
- **E4. Multi-object without exploding the parameter count.** Iyer K, Elhabian SY. *Statistical
  multi-level shape models for scalable modeling of multi-organ anatomies.* Front Bioeng Biotechnol
  2023;11:1089113, PMC9978224; and *Statistical shape modeling of multi-organ anatomies with shared
  boundaries*, PMC9886138. Within-organ and between-organ subspaces held orthogonal. Relevant if we
  ever model L1–L5 + sacrum + both hemipelves jointly — **but it still requires a fixed set of
  objects.**

---

## F. Downstream gain from SSM-based augmentation — the complete honest tally

| study | anatomy | modality | with/without numbers | verdict |
|---|---|---|---|---|
| Schmid 2023 | hip bones | **CT** | Dice 0.93→0.95, HD 8.06→6.16 mm (basic+SSIM vs none); SSIM alone 0.93 / 7.81 | **the only quantified downstream gain on bone CT in this family.** Real, tested, externally validated, and small. SSIM alone did not beat basic aug. |
| Chen 2024 (SSMSpine) | lumbar spine | 2-D MRI | Dice 96.169% **on the synthetic set** | not a with/without gain. No ablation obtained. Weak as augmentation evidence. |
| Ghaffari 2019 | — | — | improves SSM generalisation/specificity | improves the *model's* metrics, not a downstream task |
| everything else in §B | spine | — | none | **no downstream number at all** |

That is the whole tally. One number, on the wrong anatomy, worth two Dice points.

---

## G. Adversarial notes on validation in this field

1. **"Produces realistic shapes" is the norm and it is not a result.** Most spine SSM papers report
   modes of variation with anatomical narration and stop. Wai 2026 says so across 85 studies.
2. **Generalisation and specificity are not comparable across papers.** They depend on the
   correspondence method, the mesh density, the metric (RMS point-to-point vs point-to-surface) and
   whether the "ground truth" was a raw segmentation or another template fit. Rasouligandomani's
   0.36 mm and a raw-segmentation 1.1 mm are not the same quantity.
3. **Specificity in particular is usually computed against the *training* set.** Specificity is
   conventionally "distance from a random sample to its nearest training shape". A model that
   overfits scores *well*. It is not a test of anatomical plausibility; it is a test of not wandering
   off the training manifold. No spine paper I found had a clinician or an independent morphometric
   pipeline judge the samples.
4. **A deterministic ±σ lattice is not a cohort.** 16,807 grid points over 5 modes have nothing to do
   with the population density; using them as a training distribution would systematically
   over-represent the tails.
5. **The only validation design here worth copying is La Mattina's** — run the samples through the
   downstream measurement pipeline and compare *distributions* (including the shape of the
   distribution and a KS test) against the real cohort. That is checking against something outside
   the computation.
6. **Metal, osteophytes and pathology.** Schmid's training data was 25% metal-artefacted and >65%
   osteophytic and the model still worked; that is genuinely reassuring for a clinical CT corpus, and
   it is the exception — most SSM papers train on clean anatomy and never say what happens otherwise.

---

## H. What is not known

- **Whether an SSIM built on spine CT would render as a radiograph.** Schmid's <10% intensity error is
  a per-voxel statistic inside bone. A DRR is a *line integral* through the whole volume, and Schmid's
  model encodes intensity only inside the meshed structures — soft tissue, bowel gas, the table and
  the rest of the abdomen are not part of the model. Nobody has cast a DRR from an SSIM sample and
  nobody has reported what it looks like. This is the single largest unknown for our requirement and
  it is cheap to settle: build one SSIM sample and render it.
- **The per-tool numeric tables in Goparaju 2022.** Not obtained; full text needed.
- **The SSMSpine with/without ablation.** Not obtained; PDF would not extract.
- **The correct DOI for Castro-Mateos 2015.** Two candidates in indexing.
- **Whether the Meng/Pujades non-commercial licence can be negotiated.** Not asked.
- **The Kadoury accuracy numbers were read from abstracts,** not from the full texts, and they come
  from three different papers with different phantoms and cohorts. Do not quote them side by side.
- **Whether GPMM kernels can bridge the 86-subject transitional stratum.** Plausible in principle
  (that is what GPMM is for), completely untested on transitional spine anatomy — there is no paper.

---

## I. Verdict for this project

**Do not adopt an SSM as the generator.** It cannot make the thing we are actually short of: an extra
vertebra. Nothing in this literature represents a variable segment count, and the reason is
structural, not incidental.

**Do consider an SSM/SSIM as a bounded, label-safe *augmenter* of the spines we already have**, and if
so, port Schmid 2023 — it is the only validated shape-*and-intensity* route from labelled bone CT to a
new labelled CT volume, and it is the only one with a downstream number. Two things would have to be
established first, cheaply, before any of it is built:

1. **Render one.** Build a single SSIM sample and cast a DRR from it. If the frame does not look like
   a radiograph — and the soft-tissue gap above is a real reason it might not — the whole family is
   ruled out in an afternoon rather than a month. This is the project's own standing lesson: three
   analytically reasonable fixes were wrong and one render settled it.
2. **Check the distribution, not the median.** Sample a few hundred, push them through the spinopelvic
   estimator and the level-morphometry pipeline, and compare PI / SS / LL / canal depth / end-plate
   width **spreads** against the real cohort and against published normative series, La Mattina style.
   A generator that reproduces the median and narrows the SD is exactly the failure mode this project
   has already hit twice.

The one genuinely novel thing available here: **nobody has fitted a spine SSM to anything near 2,900
labelled CTs, and nobody has fitted one to the lumbosacral junction with sacrum and pelvis from CT at
all** (the only such model is n=42 from EOS). If an SSM is built here it would be the largest and the
only CT-based one, which makes it publishable on its own terms — but it would still be a model of
*ordinary* spines, and the transitional problem would remain exactly where it is.

---

## Verification pass — B8 Clouthier 2023 (adversarial, 2026-09-23)

Sources checked: Europe PMC record for PMID 36603365 (full abstract), GitHub
`aclouthier/morphable-lumbar-model` (tree, README, LICENSE, `LumbarMorphableModel.py`),
Semantic Scholar + OpenAlex citation records, model files downloaded and the published
generation math executed locally. Paywalled at Elsevier; no OA copy exists (Unpaywall
`is_oa: false`, OpenAlex `any_repository_has_fulltext: false`), so nothing below rests on
the full text.

**Confirmed, exactly as claimed.** n = 87 patients; CT (The Ottawa Hospital, Jan 2013 –
Dec 2018); PLS regression; classification compared against models built from *random labels*
— disc herniation p < 0.04, spondylolisthesis p < 0.001, sex p < 0.01; age RMSE 14.1 years;
round-trip RMSE < 0.8°, < 0.3 cm², < 0.7 mm between desired and resulting measurement. Repo
is real, MIT licence (Copyright 2022 Allison Clouthier), MATLAB + Python, the model data
ships (~250 MB of CSV), README lists the 19 named parameters, levels are L2–L5.

**Refuted or materially qualified.**
1. *Not 19 parameters — 20 models ship.* The `SSM/` tree carries an extra `L45slip`
   (L4–L5 slip, observed range 0.0019–0.278) not in the README's 19.
2. *"Independently specifiable" is wrong on two counts.* Each parameter is its **own**
   separate PLS model morphing from the same mean mesh; there is no joint model, so you
   cannot ask for two parameters at once. And the published round trip only certifies the
   **requested** measurement — it says nothing about the other 18 holding still. Running the
   repo's own code: asking for `meanVBwidth` at the top of its observed range (58.8 mm) moves
   the mesh by up to 14.3 mm and grows the whole L2–L5 block from 93.4 × 95.1 × 145.5 mm to
   107.2 × 113.3 × 167.8 mm — a ~15 % craniocaudal growth from a request about *width*. It is
   close to a global size mode.
3. *It cannot sample a population.* `createSpine()` is
   `pts = mean + ((y − ȳ)/‖YL‖²) · YL·XLᵀ` — one scalar score along one fixed direction,
   deterministic and linear in y. One y gives exactly one mesh. There is no residual
   distribution, no eigenvalues, no way to draw a random plausible instance, and no general
   shape basis in which an arbitrary new subject could be reconstructed.
4. *No fitting code.* The repo generates from the model; it has nothing that takes a CT or a
   segmentation *in*. The correspondence and segmentation methods are not in the repo and are
   not in the abstract — **not known** without the full text.
5. *Standard SSM validation is absent from the abstract.* No compactness, generalisation or
   specificity. The 2026 Frontiers scoping review of lumbar SSM names those three as its
   minimum reporting standard. Whether the round trip was measured on held-out subjects or
   on the 87 used to fit is **not known** from the abstract.
6. *Downstream gain: none, by anyone.* 9 citations, 0 influential (Semantic Scholar,
   OpenAlex agrees at 9). Not one is an augmentation, segmentation or detection study.

**Mesh, measured locally.** 65,478 vertices, 130,956 faces, **4 connected components** =
L2, L3, L4, L5. Full vertebrae including spinous processes. No L1, no sacrum, no pelvis, no
ribs, no intensities. Per-level labels are recoverable from the connected components ordered
by z, which is the one thing that would have been fiddly and is not.

**Against our requirement.** Input is not a CT and there is no path to make it one; output is
a surface with no grey values, so nothing can be cast as a DRR without a separate synthesis
step; the model spans L2–L5 so the lumbosacral junction — the whole point here — is outside
it; and a 1-D linear morph from an L2–L5 mean cannot express L6, T13 or a sacralised L5.
Verdict **REJECT as a generator**. Keep it as the published precedent for named-parameter
conditional control of a shape model, which is a ten-line technique we would re-implement,
not an artifact we would adopt.

---

## Verification of C1 (Schmid 2023)

Section C1 was checked against the primary source on 2026-09-23 and two of its claims were
corrected: the method warps a real host CT rather than synthesising a volume (so soft tissue is
NOT absent and the DRR objection falls), and its external-validation Dice sits below the same test
set published in-domain baseline. See ssm-verify-schmid2023.md in this directory.

---

## V. Adversarial verification of B1 — Boisvert TMI 2008 (checked 2026-09-23)

Full text read: preprint PDF at `https://www-sop.inria.fr/asclepios/Publications/Xavier.Pennec/Boisvert.TMI08.pdf`
(13 pp., identical in substance to IEEE TMI 2008;27(4):557-568, DOI 10.1109/TMI.2007.911474,
PMID 18390352 — citation confirmed against the EuropePMC record: journal, volume, issue, pages and DOI
all as cited). Two companion papers were pulled in full as well, because the B1 summary silently mixes
them in: AMDO 2006 (`Boisvert.AMDO06.pdf`, DOI 10.1007/11789239_36) and IEEE TBME 2008;55(11):2565-2574
(`Boisvert-TBME08.pdf`, DOI 10.1109/TBME.2008.2001125, PMID 18990626).

### Confirmed, point by point
- **What it generates.** Confirmed exactly. Section II-A: six anatomical landmarks per vertebra are
  triangulated from a PA and a lateral radiograph, a high-resolution *template* is deformed by dual
  kriging for 16 more landmarks, then "each vertebra is rigidly registered to its first upper
  neighbour and the resulting rigid transforms were recorded", giving S = [T1 ... TN]. The model is
  that pose vector and nothing else. Vertebral shape is a fixed template used for drawing pictures
  (Sec. II-C: "reconstructing a 3D spine model with standard surface models of vertebrae separated by
  the associated mean inter-vertebral transforms"). No intensities anywhere. The AMDO companion says
  it outright: "the current method takes only into account the shape of the spine and not the shape of
  the individual vertebrae."
- **Extent.** T1 to L5 only, reference frame at L5. No sacrum, no pelvis, no femora — confirmed.
- **Formalism.** Confirmed: left-invariant distance on SE(3) via the rotation-vector representation,
  Frechet mean, generalised covariance in the tangent space at the mean, lambda = 0.05 weighting
  rotation against translation (results insensitive over 0.01 to 1).
- **Data.** Confirmed to the patient: group I n = 295; Boston brace n = 39; Cotrel-Dubousset n = 33;
  untreated controls n = 26. Bi-planar radiographs of adolescent idiopathic scoliosis patients at
  Sainte-Justine, Montreal. Not CT — confirmed.
- **Not validated as a generator.** Confirmed. No generalisation, no specificity, no compactness and no
  leave-one-out reconstruction error appears anywhere in the paper. Nothing is ever sampled from the
  model. The word "validated" in the paper refers to the *landmark reconstruction* accuracy of the
  upstream stereo-radiographic method (2.6 mm, ref. [28]), not to the shape model.
- **Code.** Confirmed absent. No availability statement in the paper, and no repository was found for
  the articulated spine model itself.
- **Downstream gain.** Confirmed absent. No augmentation experiment, in this paper or in anything
  found citing it.

### Refuted or materially corrected
- **"Modes of variability are reported" is wrong for this paper.** TMI 2008 reports per-level
  *covariance ellipsoids*, not modes. It states that the covariance it visualises is "a six by six
  matrix" per inter-vertebral transform, and its own conclusion says: "In this study the correlations
  between the motions of non-adjacent vertebrae were not analyzed ... one of the future directions ...
  will be to study the global motions of the spine using joint covariances."
  **Consequence for us:** the published TMI model carries no joint covariance across levels, so drawing
  a whole spine from it means drawing each level independently, which accumulates into globally
  implausible alignment. The modes live in the *other* paper.
- **The modes paper is AMDO 2006**, on a *different and larger* cohort: 307 untreated scoliotic
  patients (not 295), PCA on the generalised covariance in the tangent space. Four modes are narrated:
  (1) growth/elongation with a mild thoracic curve, (2) double thoraco-lumbar curve, (3) a longer
  thoracic curve, (4) lumbar lordosis. Reconstructions are drawn at +/- 1 and +/- 3 sqrt(lambda_k) —
  i.e. the pose vector *is* re-synthesised, deterministically along single modes. Compactness appears
  only as an unlabelled cumulative-variance *figure* running out to 100 components; no percentage is
  stated in the text. The authors close with "it might be interesting to validate the method using an
  high accuracy imaging apparus and a deformable spine phantom" — they say themselves it is
  unvalidated.
- **"Descriptive only" undersells it slightly.** TMI 2008 does carry quantitative work, just not
  generator metrics: (a) a noise-floor simulation — landmark errors simulated from 0.25 to 5 mm give
  translational SD 0.1 to 2 mm and rotational SD 0.2 to 3.9 deg for the shape model (0.1 to 2.5 mm and
  0.2 to 5.3 deg for the deformation model), all "way below the variabilities observed from scoliotic
  patients"; (b) Hotelling T2 and Box M tests per level between treated and untreated groups with a
  false-positive-proportion correction (PFP 0.00167 at alpha = 0.01); (c) Table II, reduction in
  distance to a healthier shape, 3 to 34 % for Cotrel-Dubousset (total 23.3 %, p = 2.5e-4) and -12 to
  +11 % for the brace (total 3.3 %, not significant).
- **The same statistical model *was* validated quantitatively, in the TBME companion**, as an
  *inference prior* rather than as a generator: 291 AIS patients, 242 to fit the distribution and a
  disjoint 49 to test ("no patient was ever used both for the estimation of the statistical
  distribution of the articulated spine descriptions and for validation"). Completion of a partial 3-D
  spine: landmarks within 1 mm of measured values with at least 50 % of vertebrae present, within 2 mm
  with at least 25 %; mean difference 0.8 mm with one vertebra missing rising to 3.25 mm with fourteen
  missing; reconstruction from a PA plus a lateral radiograph, mean difference 1.1 mm. So the formalism
  is not unvalidated — it is validated for a different job.
- **Internal inconsistency worth knowing before anyone quotes the axis.** The abstract (and the
  EuropePMC record) says maximal rotational variability is "around the coronal axis"; the body and the
  conclusion both say "around the anterior-posterior axis" ("as it could be expected for scoliosis").
  Those are different axes — rotation about the AP axis is lateral bending, rotation about the
  mediolateral axis is flexion-extension. Cite the body, not the abstract, and say which you mean.

### Two findings that decide it against our requirement
1. **The model under-disperses, by the authors' own statement.** TBME 2008: "The variability of the
   resulting models is likely to underestimate the true variability of the shapes of patients' spines
   ... This underestimation, if uncorrected, could bias statistical hypothesis tests", and models with
   a large portion of information missing "will be biased toward the mean". Our stated need is
   population-plausible variation *in the thin parts of the distribution*. A Gaussian tangent model
   fitted to 295 scoliotic adolescents, known to shrink toward its own mean, is the wrong instrument
   for filling a thin tail. The Gaussian assumption is itself contested within this same line of work:
   Lecron et al., IEEE TBME 2013;60(11):3256-3264, DOI 10.1109/TBME.2013.2272657, PMID 23864145,
   replace the Mahalanobis regulariser with a one-class SVM precisely because "when a shape differs
   significantly from the statistical model, the associated Mahalanobis distance often overstates the
   need for statistical regularization".
2. **A transitional variant is a change of topology, not a point in this space.** The pose vector has
   one element per inter-vertebral link and a fixed length. An L6, a T13 or a sacralised L5 changes the
   *number* of links, so those cases cannot be samples of one model; they would need a separate model
   per phenotype, fitted on the 86 subjects we are short of in the first place. Nothing in this method
   creates the rare class.

### Cost if we tried it on ~2,900 labelled CTs
- Fitting the pose model itself is cheap and CPU-only: derive a local frame per labelled vertebra,
  compose inter-vertebral SE(3) transforms, Frechet mean plus tangent PCA. Geomstats (MIT licence,
  `github.com/geomstats/geomstats`) implements SE(3), the Frechet mean and tangent PCA, and its own
  documentation uses the articulated spine as the motivating example, so no new mathematics is needed.
  Estimate one to two weeks to a fitted model over the whole holding, minutes of compute, zero GPU
  hours.
- Everything after that is the actual project. To get a *labelled CT* out rather than a stick figure
  you must warp intensities and labels along the re-posed skeleton: piecewise-rigid per vertebra plus a
  regularised field for discs and soft tissue. That step is in none of these papers, and we have local
  evidence it is the hard part — `ostk.surgery.simulate_correction` already re-poses segments about a
  fixed pelvis and its end plates come out too rough to re-measure automatically (post-op jaggedness
  note). A DRR is unforgiving about exactly those seams.
- What would go wrong, in rough order of likelihood: frame definition drifts between subjects and the
  "variability" measured is partly our own landmarking; independent per-level sampling produces spines
  that are locally fine and globally absurd (the joint covariance is the fix and is not published);
  samples regress to the mean and the tails we need stay empty; a scoliotic-adolescent covariance gets
  transported onto adult abdominopelvic CT where it does not belong; and the disc and soft-tissue warp
  leaves seams that are invisible on a slice and obvious in a render. Render the mask before believing
  any of it.

**Verdict: REJECT as a synthesis method** — it generates no intensities, no labels and no vertebral
shape, the covariance in the cited paper is per-level with the joint structure explicitly deferred, it
is validated descriptively rather than as a generator, and a transitional variant is not representable
in a fixed-length pose vector at all. **Keep two pieces of it**: the inter-vertebral SE(3) pose vector
is the right parameterisation in which to *state* a target lordosis or kyphosis for whatever generator
we do adopt, and the same vector is a ready-made plausibility metric for auditing generated spines
(distance to a Frechet mean fitted on our own 2,900). If a spine-completion prior is ever wanted, the
artifact with held-out millimetre numbers is the TBME 2008 companion, not this paper.

---

# VERIFICATION — E3, ANAT-SSM (Boutillon 2022), read in full and checked adversarially (2026-09-23)

Read: the arXiv PDF in full, 17 pages including the supplementary material (main paper 12 pp,
supplementary SI–SVII). Bibliographic record confirmed against PubMed: **IEEE Trans Biomed Eng
2022;69(9):2733–2744, PMID 35192459, DOI 10.1109/TBME.2022.3152833, arXiv 2202.08580.**

**Correction to §E3 above: the claim "I did not obtain hard round-trip error numbers" was half wrong
and half right in an important way.** There are hard numbers (Table I). They are not round-trip
numbers. They measure the opposite direction from the one our requirement needs.

## What it actually is (confirmed, exactly as summarised)

- `BASESSM = µ + PDα` built with **Scalismo** (Apache-2.0, Scala, actively maintained) via the
  IMCP-GMM pipeline: iterative-median-closest-point rigid alignment, CPD non-rigid alignment for dense
  point-to-point correspondence, then a GPMM.
- A **synthetic population of 1,000 shapes** is drawn from the base SSM with `α ~ N(0, I_{n-1})`,
  landmarks are tracked into each sample through the established correspondence, and the anatomical
  measures are computed automatically. A least-squares fit gives `Q` (shape coefficients -> anatomical
  parameters); `ANATSSM = µ + PDQ⁺β` (Moore-Penrose); an orthogonal Procrustes solve gives `K` with
  `KKᵀ = I`, and `OC-ANATSSM = µ + PDKᵀβ̃` has *independent* controls.
- 1,000 samples was chosen from a curve: the matrix error falls 0.08 -> 0.03 between 100 and 1,000
  synthetic shapes, steeply between 100 and 300 (Fig S2). Compute is trivial, as summarised.
- Output is a **surface mesh** — femur 17,000 points, scapula 15,000. No intensities, no labels, no
  volume, no topology change.

## Data (the summary said subject counts were not given — they are)

- **Femur n = 50** whole-body CTs from the public SMIR repository (smir.ch), SOMATOM Force,
  0.99 x 0.99 x 0.50 mm, right femur only, segmented by one annotator (12 y experience).
- **Scapula n = 76** CTs from CHRU de Brest (dry bones scanned, per the acknowledgement), SOMATOM
  Definition AS, 0.96 x 0.96 x 0.60 mm, segmented by two radiologists (19 y and 12 y).
- Femur parameters m = 5 (NSA, FV, BW, HD, FL) from 18 landmarks; scapula m = 6 (CSA, GI, GV, GH, GW,
  SL) from 20 landmarks, all placed once on the mean shape and transferred by correspondence.

## What Table I actually measures — the point that decides this candidate

Section III-E, verbatim: *"The predictive performance of ANATSSM and OC-ANATSSM were assessed at each
iteration of the leave-one-out evaluation by computing the absolute error between anatomical measures
derived from manual landmarking and those obtained by both models on the retained shape."*

So: take a held-out **real** shape, fit it with the model, transfer the landmarks, measure it, and
compare against an expert's manual landmarking. That is the **analysis** direction (shape -> named
numbers). It is a statement about the model as a *measuring instrument*. Our requirement needs the
**generation** direction (named numbers -> shape), and Table I says nothing about it.

Table I, mean ± SD absolute error, BASESSM / ANATSSM / OC-ANATSSM:

| parameter | BASESSM | ANATSSM | OC-ANATSSM |
|---|---|---|---|
| NSA (deg) | 1.7 ± 1.3 | 2.1 ± 1.5 | 2.0 ± 1.6 |
| FV (deg) | 1.7 ± 1.4 | 2.7 ± 2.2 | 3.1 ± 2.6 |
| BW (mm) | 0.7 ± 0.5 | 1.1 ± 0.9 | **3.4 ± 2.5** |
| HD (mm) | 0.5 ± 0.3 | 1.0 ± 0.8 | **2.2 ± 1.6** |
| FL (cm) | 0.1 ± 0.1 | 0.1 ± 0.1 | **1.4 ± 1.0** |
| CSA (deg) | 1.6 ± 1.1 | 2.0 ± 1.8 | 2.4 ± 2.0 |
| GI (deg) | 2.0 ± 1.5 | 2.4 ± 2.1 | (see paper) |

Two readings the abstract does not give you:

1. **Every anatomical model is worse than the plain SSM at every parameter.** The authors say so and
   explain it: the ANAT models are fitted on synthetic measures used as a proxy for real ones, so they
   can only equal or lose. Anatomical parameterisation is a cost, paid for interpretability.
2. **The orthogonal variant — the one you would actually want, because it is the one whose controls
   move independently — is the one that degrades.** Femur length error goes from 1 mm (BASESSM and
   ANATSSM) to **14 mm**; bicondylar width 0.7 -> 3.4 mm; head diameter 0.5 -> 2.2 mm. Supplementary
   SVI shows the penalty is a function of how many parameters you constrain: drop parameters one at a
   time and the error falls, and an OC model with a *single* parameter matches the unconstrained
   ANATSSM. In other words, independent named control of several correlated measurements at once is
   the expensive case, and several correlated measurements at once is exactly our case.

## Is there a generate-and-re-measure experiment? Partly, and only qualitatively

The summary said no. There is one, in the supplementary, and the summary missed it — but it does not
give the number we need. **SIV**: shapes are generated by sweeping one parameter over ±3σ and *all*
parameters are re-measured on the generated shapes (Fig S3). The reported result is a slope read off a
graph — "an (approximately) linear relation ... with a slope corresponding to the covariance", and for
OC-ANATSSM "all its anatomical parameters remained unchanged (null slope)". Only one sweep per bone
(FL for femur, SL for scapula). The purpose is to demonstrate *independence*, not target fidelity.
**Commanded β versus measured β on the generated shape is never reported as a number, for any
parameter.** The rest of the generative assessment is a "visual comparison of the shape variation
patterns" (III-E, Figs 4 and S4) plus the κ variability percentages.

## "Realistic statistics" — internal check circular, external check weaker than claimed

The Results (IV-B) support is internal and partly circular: Shapiro-Wilk normality of each marginal
(p > 0.01) and confirmation that the synthetic means match the measures of the base SSM's *mean shape*
and the variances match the model's own variability. That is true by construction of Gaussian sampling.

But the Discussion (V-A) does compare to published population values, which the earlier summary missed.
I did that comparison myself rather than accept "comparable" — synthetic (Fig 3) vs the literature
values the paper cites:

| parameter | synthetic µ ± σ | literature µ ± σ | difference |
|---|---|---|---|
| NSA | 126.8 ± 2.4 deg | 121.8 ± 3.9 deg | **+5.0 deg**, SD 62% of literature |
| FV | 13.4 ± 8.7 deg | 13.9 ± 6.5 deg | mean close, SD 34% wider |
| BW | 82.2 ± 6.4 mm | 83.9 ± 6.3 mm | close |
| HD | 47.8 ± 3.8 mm | 52.1 ± 4.4 mm | **−4.3 mm (−8%)** |
| FL | 45.0 ± 3.1 cm | 42.8 ± 2.9 cm | **+2.2 cm (+5%)** |
| CSA | 29.3 ± 4.3 deg | 33.1 ± 2.1 deg | **−3.8 deg**, SD 2x |
| GI | 8.5 ± 4.1 deg | 11.0 ± 4.0 deg | −2.5 deg |
| GV | −4.7 ± 6.8 deg | −7.0 ± 4.0 deg | +2.3 deg, SD 70% wider |
| GH | 36.7 ± 3.4 mm | 36.4 ± 3.6 mm | close |
| GW | 26.8 ± 2.5 mm | 28.6 ± 3.3 mm | −1.8 mm, SD narrower |
| SL | 152.8 ± 12.8 mm | 155.0 ± 16.0 mm | close |

No test, no interval, no per-parameter difference computed by the authors; the numbers are printed
side by side and called comparable. Half the parameters are offset by more than the leave-one-out
measurement error of the same parameter (NSA off by 5.0 deg against a 1.7–2.1 deg measurement error;
CSA off by 3.8 deg against 1.6–2.4 deg). This is not misconduct — it is what a 50- or 76-subject
cohort does: **the synthetic population inherits its cohort's mean and covariance and cannot leave
them.** The paper reports exactly that failure at the extremes ("maximum error for extreme measures,
e.g. SL = 180 mm, which were scarce in the synthetically generated population"). The thin tail is the
part of our problem this family does not fix.

## Reach of the named controls

Femur: the 5 parameters span **98.7%** of the base SSM's total shape variability (90.3% with
orthogonality). Scapula: the 6 parameters span **63.1%** (61.2%). The authors' own limitation: more
parameters would be needed for the scapula. A geometrically complex structure is not covered by a
handful of named measures, and the lumbosacral junction is more scapula than femur.

Base-SSM robustness (Fig S1): femur 4 PCs for 95% variance, generality 1.0–2.4 mm, specificity
1.7–2.3 mm ("average"); scapula 15 PCs for 95%, generality 0.8–1.6 mm, specificity 1.3–1.6 mm. Note
specificity here is distance to the nearest *training* shape — see §G3 above; it is not a plausibility
test.

## Code, licence, downstream gain

- **No code and no data-availability statement anywhere in the paper or the supplementary.** The only
  released artefacts are two demo videos (SVII, `demo_bone_base_ssm.avi`, `demo_bone_anat_ssm.avi`) and
  the femur CTs, which are public at smir.ch. The base toolkit, Scalismo, is Apache-2.0 and maintained;
  the ANAT layer itself is a least-squares fit, a pseudo-inverse and an orthogonal Procrustes solve —
  perhaps twenty lines. **Absent code is not the obstacle here.**
- **No downstream gain of any kind is measured.** There is no segmentation, detection or any other
  task experiment in the paper. Confirmed by reading it end to end.
- **Not spine, and still not spine.** Femur and scapula only. No spine application has appeared since.
  The only follow-up is femur: Gheflati B, Mirzaei M, Rottoo S, Rivaz H. *Leveraging deep learning for
  nonlinear shape representation in anatomically parameterized statistical shape models.* IJCARS
  2025;20(5):1035–1046, PMID 39953355, DOI 10.1007/s11548-025-03330-3. It replaces the linear map with
  an MLP, trains on a synthetic population and fine-tunes on real bone, and reports beating the linear
  ANATSSM at **predicting 3-D bone shape from anatomical parameters on an unseen femur dataset** —
  i.e. the one direction our requirement cares about, in which the linear ANAT-SSM is the published
  loser. **The numbers are behind a paywall; the abstract carries none and there is no preprint. What
  the margin is, is not known.**

## Judged against our requirement

- **Labelled CT in, labelled CT out:** fails at both ends. It consumes correspondence-established
  surface meshes and emits surface meshes. Nothing to cast a DRR from — a rasterised binary bone mesh
  renders as a cartoon, not a radiograph. The intensity half would have to come from elsewhere
  (Schmid's SSIM, §C1).
- **Controllable:** yes, and this is the only thing ANAT-SSM adds to a PCA model. But the control has
  no measured fidelity in the direction it would be used, and the orthogonal variant needed to set,
  say, lordosis and pelvic incidence independently is the variant that degrades most.
- **Transitional variants:** structurally impossible, for the same reason given in §B of this note. A
  PDM carries a fixed number of points on a fixed number of objects with fixed topology. An L6 is an
  extra object. No β can count vertebrae. Sweeping a length parameter makes a spine longer, not a
  spine with another bone in it.
- **Population-plausible tails:** no. Gaussian sampling inside a fitted covariance, with the authors'
  own evidence of failure at the extremes.

**Verdict: REJECT** as a method to adopt for this requirement — it emits bare meshes with no
intensities and no labels, it cannot represent a variable vertebra count, and its only relevant
validation is a slope read off a supplementary figure. **Keep the trick, not the paper**: if a spine
SSIM is ever built here, the twenty lines that turn its coefficients into named controls are worth
having, and this is the reference for them.

## If we tried it on ~2,900 labelled CTs anyway — cost and what breaks

- **The ANAT layer: ~2 days.** Least squares, pseudo-inverse, Procrustes, and a sweep to pick the
  synthetic-population size. No GPU.
- **The prerequisite we do not have: ~6–12 weeks.** A spine SSM needs dense point-to-point
  correspondence per object over the cohort: 2,900 CTs x up to 24 objects is on the order of 70,000
  mesh extractions plus rigid and non-rigid registrations. CPD at 15–17k points is minutes per object
  on CPU, so roughly 2,000–12,000 CPU-hours — embarrassingly parallel, fine on `reqp`, and the
  compute is not the cost. The QC is.
- **An intensity model is separate work again** (Schmid 2023, §C1) before anything can be rendered.

What could go wrong, in the order I would expect it:

1. **Silent correspondence failure.** A CPD fit that slides along the bone still produces a smooth,
   plausible mesh, and the landmark it carries is then in the wrong place, and the "measured" lordosis
   computed from it is finite, reasonable and wrong. This is this project's canonical failure mode,
   three times over. It has to be checked against something outside the fit, and it has to be
   *rendered*.
2. **`Q` must be full rank m, and our parameters are rank-deficient by construction.** PI = SS + PT is
   an identity. Put all three in β and the pseudo-inverse silently returns a minimum-norm solution
   rather than raising. The paper states the full-rank condition (V-B) but nothing enforces it.
3. **The parameters we care about are not single-bone shape.** PI, SS, LL and kyphosis are inter-object
   *pose* quantities. `Q` is a map from one bone's shape coefficients. Controlling them requires an
   articulated multi-object model with pose in the latent space, which is a different model from the
   one validated here, and the validation does not carry over.
4. **The tails stay thin.** The synthetic population is drawn from our own covariance, so it cannot
   widen the part of the distribution that is thin. Sampling more does not add information.
5. **Storage**: ~70,000 meshes plus models belongs on the CephFS volume, not the home directory.

---

# Adversarial verification: B3, Rasoulian shape+pose (2026-09-23)

Target of the check: the candidate card that says *"Mean surface distance error 1.17 ± 0.38 mm over 16 CT
subjects"* for **Rasoulian A, Rohling R, Abolmaesumi P. Lumbar spine segmentation using a statistical
multi-vertebrae anatomical shape+pose model. IEEE Trans Med Imaging 2013;32(10):1890–1900,
DOI 10.1109/TMI.2013.2268424, PMID 23771318.**

## What could and could not be read

- **TMI 2013 full text: not obtainable.** Unpaywall `is_oa: false`, `oa_status: closed`; Semantic
  Scholar `openAccessPdf` empty. The abstract was read verbatim from Europe PMC.
- **Rasoulian's PhD thesis** (*Statistical models of the spine for image analysis and image-guided
  interventions*, UBC 2014, DOI 10.14288/1.0166855, hdl 2429/45759) **could not be downloaded** — UBC
  Open Collections serves a JavaScript browser-verification challenge to every request, including
  `curl_cffi impersonate="chrome"`, and the item is not in Unpaywall. So the TMI chapter's tables were
  never seen. Everything below about the TMI paper's *internals* is therefore unknown, and is said to
  be unknown rather than guessed.
- **SPIE 2013 landing page**: also blocked (returns a 1 KB stub). Its abstract was read only through
  three independent search-engine renderings, which agreed.
- **The CSI2014 challenge report is free full text** (PMC5527557) and was read in full. It is the only
  independent evaluation of this method and it carries most of the weight below.

## Point by point

**1. Citation — CONFIRMED exactly.** Europe PMC: Rasoulian A, Rohling R, Abolmaesumi P, *IEEE Trans
Med Imaging* 2013;32(10):1890–1900, PMID 23771318, DOI 10.1109/TMI.2013.2268424. 154 citations
(Semantic Scholar).

**2. The validation numbers — REFUTED as attributed.** The TMI abstract, verbatim:

> "We validate our technique in terms of accuracy and robustness of multi-vertebrae segmentation of CT
> images acquired from lumbar vertebrae of **32 subjects**. The mean error of the proposed technique is
> **below 2 mm**, which is sufficient for many spinal needle injection procedures, such as facet joint
> injections."

**1.17 ± 0.38 mm over 16 subjects is the SPIE conference paper**, not the journal paper:
Rasoulian A, Rohling RN, Abolmaesumi P. *A statistical multi-vertebrae shape+pose model for
segmentation of CT images.* Proc SPIE 8671, Medical Imaging 2013: Image-Guided Procedures, Robotic
Interventions, and Modeling, DOI 10.1117/12.2007448. Both numbers are real and both are the authors'.
They belong to different papers with different n. Quoting the tighter conference number under the
journal citation would be the project's standing failure mode — a number that is right somewhere else.

**3. "This is a segmentation accuracy, not a generator validation" — CONFIRMED.** Both abstracts frame
the whole contribution as registration-based segmentation. The independent benchmark (below) also
treats it purely as a segmentation entry.

**4. "No generalisation or specificity reported" — UNVERIFIED, but nothing supports the contrary.**
Without the full text this cannot be settled. No citing source located reports a generalisation,
specificity or compactness curve for this model, and the abstract advertises none.

**5. Attribution of the extension — CORRECTED.** The thoracic extension is
**Seitel A**, Rasoulian A, Rohling R, Abolmaesumi P. *Lumbar and Thoracic Spine Segmentation Using a
Statistical Multi-object Shape+Pose Model*, Lecture Notes in Computational Vision and Biomechanics 20
(Recent Advances in Computational Methods and Clinical Applications for Spine Imaging), pp. 221–225,
2015 (Crossref). Seitel is first author, not Rasoulian, and it is a five-page workshop paper.

**6. NEW and decisive — the method was independently benchmarked and came last.**
Yao J, Burns JE, Forsberg D, Seitel A, Rasoulian A, Abolmaesumi P, Hammernik K, Urschler M,
Ibragimov B, Korez R, Vrtovec T, Castro-Mateos I, Pozo JM, Frangi AF, Summers RM, Li S.
*A multi-center milestone study of clinical vertebral CT segmentation.* Comput Med Imaging Graph
2016;49:16–28. PMID 26878138, PMC5527557 (free). The shape+pose method is **Method 2**, entered by its
own authors, on 20 CT sets (10 train / 5 healthy test / 5 osteoporotic test), 17 vertebrae each,
340 vertebrae per algorithm.

Facts from that paper, all quotable:
- *"Method 2 uses a statistical shape+pose model built from **87 training volumes** incorporating
  variations of both shape and pose across the population."* T1–L5, **sub-models of three neighbouring
  vertebrae**, EM registration to a bone-edge point cloud.
- **Manual initialization required** — the operator clicks the vertebral body centre. Runtime
  **10 minutes per case**.
- Across the five teams on healthy cases: **DC 0.868–0.947, ASD 0.373–1.086 mm**. The stated ranking on
  healthy cases is *"Method 4, Method 3, Method 1, Method 5, and Method 2"* — **Method 2 is last of
  five**, i.e. the 0.868 DC / 1.086 mm ASD end of both ranges.
- On osteoporotic cases Method 2 ranks 4th of 5. Its healthy→osteoporotic DC drop is **0.138
  (z = 12.8, p ≈ 0)**, the second-largest of the five, putting it near **0.730 DC** on abnormal spines.
- Verbatim qualitative verdicts: *"The segmentation in Method 2 is off-mark although the location of
  the vertebra and the overall shape are correct. Another stage of local segmentation should be
  conducted."* and *"Method 2 had trouble locating the endplates in the thoracic spine."*
- One line reads as a positive and is not: *"All methods except Method 2 had better performance on
  non-fractured vertebrae than fractured vertebrae."* Method 2 was uniformly poor, so the comparison
  was flat — that is not robustness to fracture.
- **Fair caveat, stated by the paper itself:** Method 2 (and 5) trained on their own data, and *"the
  difference in imaging protocols and type of population between their own training set and the
  challenge data set may have decreased the accuracy."* True — and it is also exactly the
  cross-cohort generalisation test that matters for us, since we would be fitting on our cohorts and
  generating for others.

Read against our requirement, this is the damning number: the fitted shape space, driven by EM onto a
real bone-edge cloud, could not reach real vertebral surfaces closer than ~1.1 mm mean and lost
0.138 DC the moment the anatomy left the healthy mean. A shape space that cannot *fit* abnormal
vertebrae will not *sample* them either.

**7. Code — CONFIRMED absent.** No repository is named in any of the papers. GitHub API search returned
`total_count: 0` for `spine shape pose statistical model`, `vertebrae statistical shape pose model`
and `multi-vertebrae shape pose`. Nothing in Semantic Scholar, Unpaywall or the lab's citing papers.
There is **no licence to evaluate because there is no code**. The 87-volume training set is also not
public.

**8. IP flag, stated narrowly.** US 10,105,120 B2, *Methods of, and apparatuses for, producing
augmented images of a spine* — inventors Rasoulian, Rohling, Abolmaesumi, Pesteie; assignee **The
University of British Columbia**; **Active, expires 2036-12-11**. Claim 1 as read requires *"receiving
a first ultrasonic volumetric dataset"*, so on its face it does not read on CT→DRR work. I read claim 1
only, not the full claim set. Recorded because the group patents this line of work and the project has
a standing commercialization track.

**9. Downstream gain — none, for this method or anything descended from it.** No paper was found in
which a spine shape+pose model generated training data and a segmentation or detection score was
measured with and without it. The nearest measured anchor in the whole SSM family is on hip bone, not
spine: Schmid 2023 (Eur Radiol Exp 7:39) — shape+**intensity** model augmentation gave **0.93 → 0.93
DSC alone** and 0.95 only when stacked on conventional augmentation. That is the honest ceiling to
expect, and it came from a model that also synthesised intensities, which this one does not.

## Against our requirement

| requirement | verdict |
|---|---|
| labelled spine CT in | yes, CT-fitted, surfaces derived from labelled vertebrae |
| labelled plausible CT **out** | **no** — surfaces only, no intensity field anywhere in this line; nothing to cast a DRR from without inventing a whole CT-synthesis stage |
| controllable | the pose subspace *is* separable from the shape subspace (confirmed in the milestone paper's description), but **no paper maps a pose coefficient to a lordosis angle** and no target-conditioned sampling is demonstrated |
| renderable as a radiograph | **no** — see above; a smooth PDM surface filled with constant HU does not render like bone |
| transitional variants representable | **no, structurally.** Fixed point correspondence over a fixed vertebra count (L1–L5, or T1–L5 in three-vertebra sub-models). It cannot add an L6 or delete a lumbar level, and the sacrum and pelvis are absent — so the lumbosacral junction, the exact locus of our phenotypes, is outside the model |
| population-plausible | unmeasured: no generalisation, no specificity, no compactness curve published; and the one external fit test put it last of five |

## Verdict: **REJECT**

One sentence: it is a segmentation prior, never validated as a generator, with no intensities, no
sacrum, a fixed vertebra count that structurally excludes the transitional phenotypes we are short of,
no code, and an independent benchmark that ranked it last of five on healthy spines and showed its
shape space collapsing (−0.138 DC) on abnormal ones.

The *idea* survives the rejection: factorising shape from pose is the right structure for a lordosis
control, and that idea should be carried into whichever method is adopted. This implementation should
not be.

## If someone insisted on adapting it to ~2,900 labelled CTs

- **Work:** everything is a reimplementation — group-wise GMM point-set correspondence (Rasoulian TMI
  2012, PMID 22692899), the shape+pose PDM, and the EM fit. Call it 8–14 weeks for one person to a
  *generator* (not a segmenter), and that is before the two pieces that do not exist in this line at
  all: an intensity/CT-synthesis stage, and a sacrum + pelvis model.
- **Compute:** no GPU needed for the model itself. ~2,900 CTs × ~20–25 labelled bones is ~60–70k
  surfaces; group-wise correspondence is the bottleneck and is CPU-bound — low thousands of
  CPU-core-hours, comfortably a `reqp` job, with the caveat that group-wise GMM scales badly and may
  need per-level batching.
- **What goes wrong, most likely first:** (a) correspondence fails on exactly the 86 transitional
  subjects, and the standard fix is to exclude them, which deletes the point of the exercise;
  (b) mode 1 of every lumbar SSM is scale (Hollenbeck 2018, PMID 29402403), so a "lordosis knob" comes
  out entangled with stature; (c) independently sampled neighbours interpenetrate at the facets — the
  problem Castro-Mateos's Statistical Interspace Models exist to solve; (d) the surface→volume→DRR
  chain has no published recipe here, and a DRR is a projection *through* trabecular and cortical
  texture, which a PDM does not carry.

---

## VERIFICATION PASS — B10 Rasouligandomani 2024 (independent check, 2026-09-23)

Sources read: PMC11137096 full text (HTML pulled and grepped locally), arXiv:2402.13041 preprint
(PDF text-extracted), Zenodo API records 8108354 / 10371461 / 10396267 / 10994164, GitHub API for
the three repositories, and the released `Descriptive_List.xlsx` (3.5 MB, downloaded and analysed).

### Confirmed
- 16,807 = 7^5, first 5 PCs at w in {-3,-2,-1,0,1,2,3}. **Recovered empirically**: writing (ID-1) in
  base 7 and subtracting 3 gives a design matrix that predicts the released PI at R2 = 0.990, PT at
  0.989 and LL at 0.996. The released IDs *are* the lattice index. Deterministic DOE sweep, not a sample.
- Compactness 5 modes = 95% (31/19/18/11/5), 10 modes = 98%. Generalisation RMSE 0.36 +/- 0.24 mm,
  specificity RMSE 0.45 +/- 0.21 mm.
- n = 42, EOS biplanar + sterEOS, age 50-75, 50/50 M/F, height 1.72 +/- 0.22 m, weight 86 +/- 23 kg,
  IRCCS Galeazzi Milan. Composition: 7 aligned (GAP 0-2), 15 moderate (GAP 3-6), 20 severe (GAP 7-13).
- No intensity data, and none is obtainable: "The DICOM images were not shared due to an ethical
  approval ... sharing the DICOM files of patients was not allowed."
- Zenodo CC BY 4.0 (checked via API on four records), 694 GB, 12.70 billion nodes; per-model files are
  point coordinates only plus one `Mean_Model (Template).inp`.
- Spinopelvic parameters annotated per model (PI, PT, SS, LL, LL-PI, GT, RPV, RLL, LDI, RSA, TPA, Cobb, GAP).
- Code: github.com/ohirose/bcpd (MIT, active), github.com/zoemarschner/SOS-hex (MIT, MATLAB, needs the
  commercial MOSEK 9.3 solver), github.com/SpineView1/SpineViewer (AGPL-3.0, JavaScript browser),
  platform live at thc.spineview.upf.edu. 0% invalid Jacobians after SOS repair.
- Downstream gain: none. Semantic Scholar lists 11 citing papers, all FE/biomechanics; not one is an
  imaging or machine-learning study.

### Refuted / corrected
- **"up to 28.57% maximum difference" understates it.** 28.57% is lumbar lateral bending. The worst
  reported figure is **30.76%** (lumbar axial rotation, both in the segmental and multi-segmental
  comparisons). Full set: thoracic F/LB/AR 7.41/5.26/6.25%, lumbar F/LB/AR 15.38/28.57/30.76%,
  thoracic multi-segment 11.76/8.33/4.44%, thoracolumbar flexion 7.14%, ligament stress 18.18%,
  IDP lumbar 6.18% and thoracic 11.76%.
- **"T1-S1" is loose.** 17 vertebrae T1-L5 and 17 IVDs (so an L5/S1 disc exists), but the sacrum,
  pelvis and femoral head are *triangulated surfaces* only, as are the posterior elements of T1-T12.
  Only the 15 anterior bodies T1-L3 are hexahedral; L1-L3 posterior and **all of L4 and L5** are
  quadrilateral shells, and the paper says why: "we assumed that the entirety of L4 and L5 remains
  fixed, as lower fused levels are not of interest". Our entire question lives in the region this
  model explicitly declares out of scope.
- **Not all 42 are deformed** — 7 are GAP 0-2.

### Strengthened
- The circularity is worse than stated, and the authors say so themselves: *"Ground-truth validation
  involves comparing models generated by SSM with models segmented and generated from CT images. This
  step is beyond the scope of this manuscript and may need to be addressed in future works."*
  Correspondence is not computed at all — "all the points in the 42 models are correspondent to each
  other thanks to EOS imaging system", i.e. sterEOS emits one fixed-topology template per patient from
  **eight control points per vertebra** plus contour nudging in two projections. Generalisation is
  leave-one-out refit to those template instances; specificity is distance to the nearest training
  shape. Both are internal to the template family.

### New measurements on the released parameter table (external check, 16,807 rows)
- Marginals are *not* uniformly tail-heavy: PI 59.30 +/- 15.89 vs the 42 real at 59.26 +/- 15.73;
  SS, LL and Cobb match similarly. PT is 1.33x over-dispersed (13.62 vs 10.26) and **TPA 2.9x**
  (30.97 vs 10.59). So the "over-represents the tails" claim holds for PT and TPA and fails for
  PI/SS/LL — the marginals were built to look right.
- The joint is where it breaks. With w in SD units (the paper's own Equation 4), Mahalanobis M2 =
  sum(w^2) over the lattice has mean **20.0** against a population expectation of 5:
  **85.3% of the released models lie outside the 95% ellipsoid of their own training distribution,
  69.2% outside the 99%, 46.4% outside the 99.9%.** 32 models sit at +/-3 SD in all five modes at once,
  a configuration with population probability around 1e-13. PI's excess kurtosis is -0.85: a flat-topped
  box wearing a plausible mean and SD. This is the project's standard failure mode in a published dataset.
- Anatomically impossible members, by the dataset's own annotations: **TPA > 90 deg in 5.8%** (972
  models) and > 60 deg in 7.2%; LDI > 1000 in 1.6% (max 258,769, for a quantity that is normally
  50-80%); PI > 85 deg in 6.2% and > 75 deg in 18.9%; PT < 0 in 0.9%; LL >= 0 (kyphotic lumbar) in 3.4%.
  Either the shapes are wrong or the shipped index is wrong; either way the table cannot be used as a
  selection key without filtering. PI = PT + SS holds to 1e-12 throughout, which — per this project's
  own history — proves nothing, since all three come from the same two landmarks.

### Verdict for our requirement: REJECT
Fails at input (consumes sterEOS template reconstructions, not labelled CT; no fitting pipeline is
released — only BCPD++, a third-party registration binary), fails at output (no intensities, and the
source images are legally unshareable EOS radiographs, so a renderable volume can never come from
here), and fails at transitional anatomy (a 17-vertebra fixed correspondence cannot host an L6, and
42 ASD patients aged 50-75 contain no documented variant). The control claim is real but is post-hoc
selection over a lattice that is mostly outside its own plausibility ellipsoid.

Narrow salvage, worth about a day and nothing more: the 42 patient STLs (87.3 MB, CC BY 4.0) and the
42-row parameter sheet are an *external* cohort against which our spinopelvic estimator's PI/PT/SS/LL
can be cross-checked — outside our computation, which is the check this project keeps needing. The
16,807 are not training data.
