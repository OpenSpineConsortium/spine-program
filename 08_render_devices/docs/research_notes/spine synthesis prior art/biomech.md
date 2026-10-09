# Biomechanical and articulated models for generating spine CT variation — prior art

Angle: patient-specific FE spine models, multibody/articulated models, musculoskeletal platforms
(ArtiSynth / OpenSim / AnyBody), and anything validated against real post-op or in-vivo geometry.
Searched 2026-09-23; resumed and extended the same day (corrections and four new entries marked
**[added on resume]**). Nothing implemented; this is an evidence file.

Requirement being judged against (restated): in = CT + per-vertebra labels; out = NEW volumes WITH
aligned labels that still render as radiographs; control = target lordosis / kyphosis / transitional
phenotype; variation must be population-plausible and must not fabricate anatomy that does not occur.

---

## Headline

**The specific thing being proposed — per-vertebra rigid transforms blended into one smooth,
invertible displacement field — is not a hack. It is the log-Euclidean poly-rigid / polyaffine
framework of Arsigny, Pennec and Ayache (2003–2009), and it has already been instantiated on the
spine three times (Drobny 2020, Bukas 2021, and the Nijmegen scoliosis simulation).** Under that
name it is citable, it has a proof rather than a Jacobian check (invertibility is guaranteed by
construction: the blend happens in the log/velocity domain and the transform is the exponential of a
weighted-average stationary velocity field, so it is a diffeomorphism by definition — you do not have
to hope the Jacobian stayed positive), and it has an accepted validation protocol. What is genuinely
missing from the literature is not the mechanism but the *bound*: nobody has published a generator
that clips per-level perturbation to Panjabi's segmental ROM. That is a defensible small
contribution; the warp itself should be cited, not invented.

**The one measured downstream gain in spine comes from this family, not from finite elements.**
The Nijmegen DIAG scoliosis simulation (A6) deforms CT *and* mask by an interpolated displacement
field and reports segmentation Dice 61.5% → 93.6% and labelling accuracy 71.8% → 100% after
retraining — with a serious caveat about what that was measured on (see A6). It is the single
strongest piece of evidence in this whole angle, and it is a geometric deformation model, not
biomechanics.

**Finite element modelling, in contrast, is the wrong tool for this job, and the numbers say so.**
The best-validated patient-specific spine FE models reproduce a real spine to ~5° Cobb and ~2.5 mm
per vertebra; material-property choice alone moves predicted Cobb by up to 6.2°. No FE spine model
places a spine at a commanded lordosis more precisely than that, none produces an image without a
separate warping step bolted on afterwards, and exactly one paper in the literature has ever
converted FE spine output into a CT volume — with no anatomical fidelity metric and no downstream
result.

**Nothing in this angle can make a transitional vertebra.** L6, T13, sacralised L5 and four-lumbar
are changes of segment *count and identity*, not deformations of an existing topology. Every method
below deforms a fixed topology. For the 86-subject scarcity problem specifically, this whole family
is the wrong family — it can broaden the lordosis/kyphosis/PI distribution around the transitional
cases we already have, which is worth something, but it cannot manufacture one.

---

## A. The articulated-warp family (produces a warped CT + warped labels) — the relevant one

### A1. Log-Euclidean poly-rigid / polyaffine transforms — Arsigny, Pennec, Ayache
- Arsigny V, Pennec X, Ayache N. *Polyrigid and Polyaffine Transformations: A New Class of
  Diffeomorphisms for Locally Rigid or Affine Registration.* MICCAI 2003.
  DOI 10.1007/978-3-540-39903-2_101
- Arsigny V, Commowick O, Pennec X, Ayache N. *A Log-Euclidean Polyaffine Framework for Locally
  Rigid or Affine Registration.* WBIR 2006. DOI 10.1007/11784012_15
- Arsigny V, Commowick O, Ayache N, Pennec X. *A Fast and Log-Euclidean Polyaffine Framework for
  Locally Linear Registration.* J Math Imaging Vis 2009;33(2):222–238. DOI 10.1007/s10851-008-0135-9
- **Current implementation with code (citation corrected on resume):** Legouhy A, Callaghan R,
  Azadbakht H, Zhang H. *POLAFFINI: Efficient Feature-Based Polyaffine Initialization for Improved
  Non-linear Image Registration.* IPMI 2023, LNCS; DOI 10.1007/978-3-031-34048-2_47;
  arXiv:2407.03922. Extended journal version *Polaffini: a feature-based approach for robust affine
  and polyaffine image registration*, arXiv:2602.17337.
  Code: **https://github.com/CIG-UCL/polaffini** — Python + SimpleITK, runs on CPU with
  multi-threading, no GPU. It exposes `rigid`, `affine`, **`polyrigid` and `polyaffine`** transform
  types directly, and takes a fine-grained segmentation as the region definition — which is exactly
  the interface we have (per-vertebra labels). A LICENSE.md exists in the repo; **I could not read
  which licence it is from the search tooling — check the file before depending on it.**

Generates: a dense, smooth, **provably invertible** displacement field from N local rigid/affine
transforms plus per-region weight functions. Apply it to the CT and to the label map and you get
exactly the deliverable. Region weights are typically Gaussian around anchor points; for a spine the
natural anchors are the labelled vertebral bodies we already have.

Validation: this is a registration framework, validated as such — the published claim is that it
fuses local rigid deformations into a global invertible transformation without introducing artifacts,
independently of how the local deformations were estimated. POLAFFINI adds an empirical registration
result (better alignment than affine initialisation for both classical and learned non-linear
registration, and faster and more robust than FSL FLIRT) — but that is brain MRI, and it measures
*registration accuracy*, not anatomical plausibility of a synthesised spine. **Adversarial note: a
framework proof is not evidence that the resulting anatomy is plausible. Arsigny validates the
*transform*; nobody validates the *spine*.**

Compute: seconds per volume on CPU.

Fit: **best in this angle.** Directly produces CT + labels, controllable per level, cheap, carries a
named citation that answers "what proven method is this", and now has a maintained public
implementation whose input is a label map.

### A2. Drobny et al. 2020 — locally rigid CT-to-X-ray spine registration (the spine instantiation)
Drobny D, Ranzini M, Isaac A, Vercauteren T, Ourselin S, Choi D, Modat M. *Towards Automated Spine
Mobility Quantification: A Locally Rigid CT to X-ray Registration Framework.* WBIR 2020, LNCS 12120.
DOI 10.1007/978-3-030-50120-4_7. PMC7279937.

Generates: warped spine CT. Per-vertebra rigid transforms, weight maps, combined **in velocity space**
("the weighted average of the downscaled transformations is computed, then upscaled") — i.e. exactly
A1, applied to vertebrae, explicitly chosen for invertibility and to avoid topology breaking.

Validation: **synthetic CT with known flexion/extension angles.** 3D–3D 0.12° (extension) / 0.16°
(flexion) mean absolute angle error; 3D–2D 0.59° / 0.42°. **Adversarial note: this is circular.** The
ground truth was generated by the same deformation model being tested, so the numbers measure solver
convergence, not anatomical realism. There is no cadaver, no in-vivo flexion-extension comparison, no
reader study, and no measurement of whether end plates survive.

Code: none stated. Downstream gain: none measured.

Fit: proves the mechanism has been done on spine CT and published. Its validation is not the
validation we need.

### A3. Bukas et al. 2021 — virtual spine straightening and vertebra inpainting
Bukas C, Jian B, Rodriguez Venegas LF, De Benetti F, Ruehling S, Sekuboyina A, Gempt J, Kirschke JS,
Piraud M, Oberreuter J, Navab N, Wendler T. *Patient-specific virtual spine straightening and
vertebra inpainting: an automatic framework for osteoplasty planning.* arXiv:2103.07279 (2021).

Generates: a warped CT volume — CNN segmentation, then **per-vertebra rigid registration to a healthy
spine atlas** to restore curvature, then GAN inpainting of the fractured body. So: the same
per-vertebra-rigid idea, driven by an atlas target rather than by a commanded angle.

Validation: 10 patients; virtual vertebra volume vs healthy equivalent, mean error 3.88 ± 7.63%.
**Adversarial note: a ±7.6% volume error on n=10 is a weak result**, and volume is a poor surrogate
for the thing we care about (end-plate sharpness, cortical continuity, morphometric measurability).

Code: none. Downstream gain: none.

Fit: second spine precedent; also shows the atlas-target variant, which is the obvious way to
*condition* an articulated warp on a target sagittal shape.

### A4. Zhang H, Zhao B, Unberath M, 2026 — Patient-Specific Articulated Digital Twins from a Single
Full-Body CT Scan. arXiv:2607.02156 (submitted 2 July 2026).

Generates: SMPL-rigged, pose-deformable CT representation — bones and organs bound to an
anatomy-aware rig, repositionable while preserving skeletal geometry, then rendered as pose-dependent
DRRs. This is the most recent and most ambitious "articulate a real CT" work, and it is Unberath's
group (DeepDRR), so the rendering end is taken seriously. The paper's own framing is the same gap we
are in: conventional DRR rendering varies the *viewpoint* while the anatomy stays frozen in the
acquisition pose.

Validation (**corrected on resume — the cohort is three subjects, not fifteen**): full-body CT from
**n = 3** subjects; fitted scaffold 15.8 ± 4.0 mm chamfer distance; 95.9 ± 1.8% skeletal enclosure at
the acquisition pose; 94.4 ± 0.4% enclosure across unseen target poses; recomposition at the
acquisition pose SSIM 0.872 ± 0.016 and PSNR 18.5 ± 1.4 dB across paired DRRs. The authors call it a
proof of concept and a feasibility demonstration, and the abstract claims only feasibility.

**Adversarial note: n = 3, and 15.8 mm chamfer is whole-body limb-posing accuracy — an order of
magnitude too coarse for vertebra-level morphometry.** PSNR 18.5 dB on a DRR is low; SSIM 0.872 is a
*self*-comparison (re-rendering the pose it was built from), so it is an upper bound on fidelity, not
an estimate of it. This is about arms and legs, not about lumbar lordosis.

Code: not stated in the abstract or listing. Downstream gain: none.

### A5. Morfeus / biomechanical deformable image registration — the one warp validated on real landmarks
Velec M, Moseley JL, Svensson S, Hårdemark B, Jaffray DA, Brock KK. *Validation of biomechanical
deformable image registration in the abdomen, thorax, and pelvis in a commercial radiotherapy
treatment planning system.* Med Phys 2017;44(7):3407–3417. PMID 28453911. DOI 10.1002/mp.12307.

Generates: a warped CT/MR, driven by a genuine FE solve with assigned material properties on
contoured organs. **The only biomechanical CT warp in this review validated at scale against real
anatomical landmarks.** 74 patients; mean distance-to-agreement ≤1.0 mm for controlling structures,
1.0–3.5 mm for implicitly deformed structures; TRE 2.0 mm (prostate MR) to 5.1 mm (lung MR) —
"accuracy similar to the image voxel resolution on average."

Code/licence: commercial, RayStation (RaySearch). Not open.

**Adversarial note: spine is not one of the validated sites**, and this is a registration engine —
it solves for the deformation that matches a second real image. It is not a generator; there is no
mode where you ask for a lordosis and get a volume.

Fit: useful as the *standard of evidence*. It shows what a credible validation of a warped CT looks
like — real landmarks, TRE in mm, n=74 — and none of the spine papers above meet it.

### A6. **[added on resume] Nijmegen DIAG — "Scoliosis simulation for improving a segmentation and labelling algorithm"**
Diagnostic Image Analysis Group / AI for Health, Radboudumc, Nijmegen (Lessmann group). Project ran
Feb 2021 – Jul 2022. Pages: https://www.diagnijmegen.nl/projects/scoliosis-simulation/ and
https://www.ai-for-health.nl/projects/scoliosis-simulation/.
**No peer-reviewed publication, DOI or PMID was found for this work.** What is public is a project
page, a linked project report and a Grand Challenge demo. Treat every number below as unrefereed.

Generates: **a deformed CT volume AND its deformed segmentation mask.** Method as described: build a
scan-specific 3-D spinal model, deform it to follow a 2-D clinical scoliosis curve, interpolate the
resulting displacement vectors per voxel, and apply that field to both the image and the mask. That
is the A-family mechanism again — a spine-driven displacement field applied jointly to intensities
and labels — reached independently and stated in exactly the terms our proposal uses.

Control: a target clinical scoliosis curve. This is *conditional* generation on a curve shape, which
is the closest published analogue to "place this spine at a commanded lordosis".

**Downstream gain — the only measured one in spine, and the reason this entry matters:**
54 simulated scoliosis cases created, split 42 train / 12 test. After retraining the segmentation and
labelling network:
- segmentation Dice **61.5% → 93.6%** (p < 0.001)
- labelling accuracy **71.8% → 100%** (p < 0.001)
- on 30 *clinical* scoliosis cases, qualitative reader evaluation: vertebrae with small segmentation
  errors **14.3% → 7.6%** (p = 0.02); vertebrae with severe segmentation errors **12.7% → 3.3%**
  (p < 0.001).

**Adversarial notes, and they are load-bearing:**
1. **The headline 61.5 → 93.6 and 71.8 → 100 are measured on 12 SIMULATED test cases produced by the
   same generator that made the 42 training cases.** That is train-on-generator, test-on-generator.
   It proves the network can learn the generator; it does not prove the generator is realistic. Read
   alone it is the same circularity as Drobny (A2).
2. **The only result that escapes the circle is the clinical one — and it is qualitative and much
   smaller.** Severe errors 12.7% → 3.3% on 30 real scoliosis cases is the honest effect size, it is
   a reader judgement rather than a Dice against ground truth, and n = 30.
3. Labelling accuracy reaching exactly 100% on 12 cases is a ceiling artefact of a tiny test set, not
   a meaningful number.
4. No DRR or radiographic-realism check anywhere — the deformed volumes were only ever consumed as
   3-D CT by a segmentation network. **Whether these warps survive projection is untested.**

Fit: **the single most useful precedent in this angle.** It is a published-in-public demonstration
that (a) the warp-image-and-mask-together design works end to end on spine CT, (b) it moves a real
downstream metric, and (c) the honest, non-circular part of that movement is modest. Design our
evaluation to avoid its flaw: the test set must be REAL cases, never our own synthetic ones.

---

## B. Patient-specific FE spine models (geometry only, validated against real patients)

### B1. Aubin's S3 spine surgery simulator — validated against real post-operative spines
Aubin CE, Labelle H, Chevrefils C, Desroches G, Clin J, Eng AB. *Preoperative planning simulator for
spinal deformity surgeries.* Spine 2008;33(20):2143–2152. PMID 18794755.
DOI 10.1097/BRS.0b013e31817bd89f.

Kinetic/flexible-mechanism model of patient-specific spine geometry and flexibility; simulates each
substep of instrumentation. **Validated against real post-op results on 10 scoliotic cases: average
Cobb differences 3.5°–4.6° frontal, 3.6°–4.7° sagittal.** Screw position agreement <0.5 mm in the
intraoperative simulator follow-up (PMID 22744520).

Generates: geometry only — vertebral poses. **No image.** Not open source; commercialised (patents
US 10463433 / 11576727 / 11903655, Spinologics). Per-patient build needs a 3-D reconstruction from
biplanar radiographs plus a flexibility personalisation (bending films).

Fit: this is the best "how close did the predicted spine come to the real one" number in the whole
literature — and it is ~4°. Cite it for the honest statement of what biomechanics can promise.

### B2. Vergari / Skalli / Aubert FE trunk model for brace simulation
Vergari C, Ribes G, Aubert B, Adam C, Miladi L, Ilharreborde B, Abelin-Genevois K, Rouch P, Skalli W.
*Evaluation of a patient-specific finite-element model to simulate conservative treatment in
adolescent idiopathic scoliosis.* Spine Deform 2015;3(1):4–11. PMID 27927450.
DOI 10.1016/j.jspd.2014.06.014.

10 patients, geometry from biplanar radiographs, brace pad displacements imposed. **Cobb RMSE 5.7°,
rib hump 5.6°, vertebral orientation 4.8°, vertebral position 2.5 mm** vs in-brace radiographs.

Generates: geometry. No image. Not open.

### B3. Material sensitivity — the reason not to trust FE for fine placement
Wei W, Zhang T, Yang J, Qian Y, Dong Y. *Material sensitivity of patient-specific finite element
models in the brace treatment of scoliosis.* Front Bioeng Biotechnol 2023;11:1111449.
DOI 10.3389/fbioe.2023.1111449. PMC9978187.

Varying material properties alone moved predicted Cobb by up to **4.7° thoracic / 6.2° lumbar**, and
in-brace correction by **18% / 15.5%**. n = 1 patient. Build pipeline described step by step: CT at
0.625 mm → Mimics thresholding/region-growing → reverse engineering → CAD disc splitting → Hypermesh
tet/hex meshing → ligaments as springs.

**Consequence for us: a patient-specific FE model cannot place a spine at a commanded lordosis to
better than roughly 5°, and that is before any question of whether the warped image is measurable.**

### B4. Phellan Aro R, Hachem B, Clin J, Mac-Thiong JM, Duong L, 2024 — the one spine case of FE-as-data-generator
*Real-time prediction of postoperative spinal shape with machine learning models trained on finite
element biomechanical simulations.* Int J Comput Assist Radiol Surg 2024;19(10):1983–1990.
PMID 39044037. DOI 10.1007/s11548-024-03237-5.

**6,400 FE simulations from the spine geometries of 64 patients** used as the training set for a
surrogate (PCA + linear regression, also autoencoders). Result: average vertebral position error
3.75 mm, orientation error <2.74° on all three axes, in 3 ms vs seconds-to-minutes for the FEM.

This is the closest thing in spine to "a biomechanical model generated training data and somebody
measured the result" — **but the network predicts spine SHAPE, not an image**, and the measured
quantity is surrogate fidelity to the FEM, not clinical accuracy. No imaging network involved. No
code stated.

### B5. Rasouligandomani M, del Arco A, Chemorion FK, Bisotti MA, Galbusera F, Noailly J,
Gonzalez Ballester MA, 2024 — 16,807-model open FE repository
*Dataset of Finite Element Models of Normal and Deformed Thoracolumbar Spine.* Sci Data 2024;11:549.
DOI 10.1038/s41597-024-03351-8. arXiv:2402.13041. PMC11137096.

Built from **42 non-operated patients (50/50 M/F, ages 50–75) imaged with EOS**; a hexahedral SSM
morphs one template; **first 5 shape modes × 7 standard deviations (−3…+3) = 7^5 = 16,807 models**;
SSM deformation fields adapted to sagittal balance measurements — i.e. **this is the only work in
this angle with an explicit conditional handle on sagittal alignment.**

Validation: 0% invalid elements across all 16,807; Jacobian ratio 0.40–0.90; ROM within 7.41%
(thoracic flexion) to **30.76% (lumbar axial rotation)** of in-vitro data; L4–L5 intradiscal pressure
0.47 MPa vs 0.50 MPa in vivo (6.18% difference); thoracic IDP within 11.76%.

Availability: Zenodo, **CC-BY 4.0**, 694 GB, 12.70 billion nodes (e.g. zenodo.org/records/8103154 for
part 1). Needs Abaqus 2019+ or another .inp reader. **Contents are STL + .inp meshes and spinopelvic
parameter spreadsheets — no CT intensities.** Web platform: thc.spineview.upf.edu.

**Adversarial notes:** a 5-mode PCA on 42 elderly EOS patients is a thin basis and a grid over ±3 SD
of 5 modes is a lattice, not a population sample — the "cohort" is combinatorial, not statistical, so
the density of the 16,807 does not represent the density of real spines. Lumbar axial-rotation ROM
off by 30.76% is a real miss. And 42 patients aged 50–75 is not our cohort.

Fit: as a *source of plausible spine shapes* conditioned on sagittal balance, this is genuinely
useful and openly licensed. As a source of CT, it is nothing — the gap from mesh to image is the
entire problem and this dataset does not cross it.

### B6. Tapp et al. 2022 — the only FE→CT-volume paper
*Generating Scoliotic Computed Tomography Volumes from Finite Element Spine Models.* In:
Computational Biomechanics for Medicine (Nielsen, Nash, Li, Miller, Wittek eds.), Springer 2022.
DOI 10.1007/978-3-031-09327-2_6.

Cervical, thoracic and lumbar FE spine models are deformed by FE analysis and **converted into CT
volumes with authentic Hounsfield units, with ground-truth segmentations of bone and selected soft
tissue.** On paper this is the closest published precedent to the whole proposal.

Validation: the volumes were **"tested in a pre-trained vertebral segmentation deep learning network
to prove compatibility with image analysis methods."** That is the entire validation.
**Adversarial note: this is the weak result the brief warns about.** "A pre-trained net still
segments it" is a smoke test, not anatomical fidelity. There is no morphometric comparison to real
CT, no reader assessment, no DRR realism check, no measured downstream training gain, no stated
code or data release, and the paper has attracted very little citation.

### B7. **[added on resume] Campbell JQ, Petrella AJ, 2016 — SSM-driven virtual population of lumbar FE models**
*Automated finite element modeling of the lumbar spine: Using a statistical shape model to generate a
virtual population of models.* J Biomech 2016;49(13):2593–2599. PMID 27270207.
DOI 10.1016/j.jbiomech.2016.05.014. Companion verification paper: *Automated finite element meshing
of the lumbar spine: Verification and validation with 18 specimen-specific models*, J Biomech 2016
(DOI 10.1016/j.jbiomech.2016.11.005).

Training set: **18 cadaveric specimens**, segmented CT, L1–L5; automatic landmark identification
placing **6,530 landmarks per specimen (1,306 per vertebra)**; **17 shape modes**; functional FE
models generated at the mean shape and at ±3 SD of every mode. The SSM was assessed on the standard
triad — compactness, generalisation, specificity.

**This is the direct ancestor of B5 and the earliest clean statement of the "SSM → virtual population
of spines" idea.** I could not retrieve the numeric generalisation/specificity values (ScienceDirect
returns 403 and the PubMed page would not render); **treat the numbers as unread, not as absent.**

Generates: meshes. **No image, no intensities, no labels in image space.** 18 cadaveric specimens is
a thin and old basis, and ±3 SD extremes of single modes are again a lattice rather than a sample.

### B8. **[added on resume] Ahmadi M, Chen H, Lin M, et al., 2025 — the build-time answer**
*Streamlined and efficient patient-specific modeling for lumbar spine segmentation and finite element
analysis.* Sci Rep 2025;15:35619. DOI 10.1038/s41598-025-19664-6. PMC12518766.

Pipeline: TotalSegmentator v2.7.0 (nnU-Net) segmentation → cortical/cancellous separation by inward
vertex displacement + Laplacian smoothing → nucleus geometry by PCA → ligament attachment by
spherical coordinates → meshing with GIBBON + MATLAB PDE Toolbox → solve in FEBio 2.5.

**This partially closes the "how long does it take" gap.** The authors state the automated route cuts
preparation "from days to just hours", and cite prior work achieving a **97.9% reduction, from over
24 h to about 30 min**. Elsewhere in this literature, automated per-structure times of ~4.4 min per
vertebra and ~31 s per disc are reported. So: **manual patient-specific FE build is a multi-day job;
the best automated 2025 pipelines get one lumbar spine down to roughly half an hour to a few hours.**
For ~2,900 CTs that is still 1,450–8,700 CPU-hours of model building before a single simulation runs,
and it produces no image at the end of it.

Validation: **n = 1 subject**, one CT from the VerSe challenge; L2/L3 and L3/L4 ROM under extension
compared qualitatively against Pearcy 1994 cadaveric data and three prior FE studies — "align closely"
/ "within the range reported", with the values only in a figure. **Adversarial note: this is a
single-subject plausibility check, not a validation.**

Code: **no repository given.** Component tools (TotalSegmentator, nnU-Net, MONAI Apache-2.0, GIBBON,
FEBio) are open; the pipeline itself needs commercial MATLAB R2024b and is not released.

---

## C. Musculoskeletal / multibody platforms (no image, and they do not deform bone)

### C1. OpenSim full thoracolumbar spine and rib cage — Bruno AG, Bouxsein ML, Anderson DE, 2015
*Development and Validation of a Musculoskeletal Model of the Fully Articulated Thoracolumbar Spine
and Rib Cage.* J Biomech Eng 2015;137(8):081003. PMID 25901907. DOI 10.1115/1.4030408. PMC5101035.

T1–L5, ribs 1–10, sternum, sacrum; 76+ muscle fascicles; ball joints at intervertebral articulations,
pin joints costovertebrally; muscle CSA adjusted from CT of a community cohort.

Validation (against in vivo): intradiscal pressure r = 0.91 lumbar, r = 0.87 thoracic; L1
telemeterised implant loads r = 0.88; erector spinae tension vs EMG r = 0.98 (T4), r = 0.91 (L1–L5);
predicted-vs-measured slope and intercept not different from 1 and 0.

Code: OpenSim is free and open (Apache 2.0); the model is distributed via SimTK.

**Fit: none for our purpose.** It validates *loads*, not geometry. Vertebrae are rigid bodies with
ball joints — there is no soft tissue geometry, no image, and nothing that resamples a CT.
Its only usable output for us is a kinematically legal set of intervertebral poses, which is what
Panjabi's table already gives us more cheaply.

### C2. ArtiSynth — the one platform that is genuinely hybrid FE + multibody and genuinely open
Lloyd JE, Stavness I, Fels S. *ArtiSynth: A Fast Interactive Biomechanical Modeling Toolkit Combining
Multibody and Finite Element Simulation.* In: Soft Tissue Biomechanical Modeling for Computer Assisted
Surgery, Springer 2012. DOI 10.1007/8415_2012_126. Java; **two-clause BSD**; github.com/artisynth/artisynth_core.

Spine model: Remus R, Lipphaus A, Neumann M, Bender B. *Calibration and validation of a novel hybrid
model of the lumbosacral spine in ArtiSynth — the passive structures.* PLOS ONE 2021;16(5):e0250456.
DOI 10.1371/journal.pone.0250456.
- L1–S1, rigid vertebrae + deformable discs/ligaments/facets; stepwise calibration on L4/5.
- Validated against in-vitro ROM, intradiscal pressure at 250–1000 N, facet contact forces,
  instantaneous centres of rotation, disc bulge, motion coupling.
- **Fully open: Zenodo 10.5281/zenodo.4453702 and github.com/RemusR9/artisynth_lumbosacralSpineModel.**
- Compute: ~0.40 time steps/s; ~19 s of wall clock per simulated second on a laptop-class machine.

**Adversarial note:** L1–S1 only, no thoracic, no image, and it simulates *response to load*. To use
it as a generator you would have to search over load cases until the spine lands at the lordosis you
wanted — which is slower and less controllable than just commanding the angles directly, and buys
you nothing the ROM table does not already bound.

### C3. AnyBody lumbar spine model
Validated for L4/L5 loads against in vivo intradiscal pressure — Han KS et al. / Actis JA et al.,
PMID 28521951 ("Validation of the AnyBody full body musculoskeletal model in computing lumbar spine
loads at L4L5 level"): calculated pressures agreed positively with in vivo measurements.
**Commercial licence (AnyBody Technology).** Loads only, no image, no geometry generation.

### C4. IT'IS Virtual Population Poser (ViP3 / ViP4)
Posable whole-body voxel phantoms, >300 tissues (V3.1) to >1000 regions (V4.0) at 0.5 mm isotropic.
Two posing routes: a volume-preserving skeleton/influence-region blend (real-time — i.e. a skinning
weight blend, the same idea as A1 without the log-Euclidean guarantee), and a physics-based passive
soft-tissue simulation for realistic joint regions.

**Validation: "reviewed and verified by independent external anatomical experts" — that is the only
validation stated. No quantitative geometric or morphometric numbers.** Commercial licence via
IT'IS / Sim4Life. Output is a tissue-labelled voxel grid, not HU; a CT would require an assignment
step. Built for EM-exposure dosimetry, not for radiographic realism.

### C5. XCAT / XCAT-3.0
Segars WP et al., *Realistic CT simulation using the 4D XCAT phantom*, Med Phys 2008 (PMID 18777939);
*Population of anatomically variable 4D XCAT adult phantoms for imaging research and optimization*,
Med Phys 2013 (PMID 23556927), 58 phantoms (35 M / 23 F);
Dahal L, ..., Abadi E, Samei E, Lo JY, Segars WP. *XCAT-3.0: A Comprehensive Library of Personalized
Digital Twins Derived from CT Scans.* arXiv:2405.11133 (2024) — **>2,500 phantoms, 140 structures,
voxelised and mesh, coupled to an in-house CT scanner simulator that produces realistic CT images.**
CC-BY 4.0, request via cvit.duke.edu/resources, xcat-3.github.io.

**This is the only entry in this angle that reliably produces an IMAGE.** But: the anatomical
variation comes from segmenting real CTs, not from any biomechanics; no per-vertebra morphometric
validation is reported; and the spine is represented at a level of detail built for dosimetry and
scanner-design studies, not for telling L5 from L6.

---

## D. Adjacent evidence — has model-generated data ever trained an imaging network, measurably?

In spine, once — **A6 (Nijmegen), and it is a displacement-field deformation model, not biomechanics.**
No finite-element or musculoskeletal spine model has ever been shown to improve an imaging network.
The other measured cases are outside spine, and set the bar:

- **Kovacs B, Netzer N, Baumgartner M, ..., Bonekamp D, Maier-Hein KH.** *Anatomy-informed Data
  Augmentation for Enhanced Prostate Cancer Detection.* MICCAI 2023. arXiv:2309.03652.
  DOI 10.1007/978-3-031-43990-2_50. A lightweight anatomy-driven deformation (dilating bladder and
  rectum to simulate physiological deformation of the prostate), warping image and label together.
  **774 biopsy-confirmed examinations; +4 of 76 lesions found (5.3% relative) at 0.32 FP/scan,
  bootstrap- and t-test-significant.** Code Apache-2.0, an nnU-Net v2 fork:
  github.com/MIC-DKFZ/anatomy_informed_DA. **This is the template for the validation design we
  should copy — and note how modest the honest gain is.** It is not FEM despite occasional
  description as such; it is a directional dilation.
- **Gilbert A, Marciniak M, Rodero C, Lamata P, Samset E, McLeod K.** *Generating Synthetic Labeled
  Data From Existing Anatomical Models: An Example With Echocardiography Segmentation.* IEEE Trans
  Med Imaging 2021;40(10):2783–2794. PMID 33444134. Networks trained on **synthetic data only**
  reached median Dice 91 / 90 / 88 / 87 on four unseen real datasets — matching inter-observer
  agreement and comparable to training on real images. The strongest "model-generated data works"
  result anywhere. **Caveat: the realism came from a CycleGAN, not from the mechanics.**
- **Prakosa A, Sermesant M, Delingette H, et al.** *Generation of synthetic but visually realistic
  time series of cardiac images combining a biophysical model and clinical images.* IEEE TMI 2013.
  PMID 23014716. **Duchateau N, et al.** *Model-Based Generation of Large Databases of Cardiac
  Images: Synthesis of Pathological Cine MR Sequences From Real Healthy Cases.* IEEE TMI
  2018;37(3):755–766. PMID 28613164. 465 synthetic sequences (15 healthy, 450 pathological).
  Both generate images by warping *real* intensity data with a simulated displacement field — the
  same architecture being proposed here, and evidence that it is an accepted design.

---

## E. What is not known, stated plainly

1. **Build time for a patient-specific spine FE model is now partly known and is still prohibitive.**
   Ahmadi 2025 (B8) gives "days → hours" for an automated lumbar pipeline and cites 24 h → 30 min
   elsewhere; per-structure figures of ~4.4 min/vertebra and ~31 s/disc circulate. Nothing reports an
   end-to-end wall-clock number for a *thoracolumbar* patient-specific model, and nothing reports the
   human time inside those hours.
2. **No biomechanical or articulated spine model has been shown to produce a warped CT whose
   end plates remain measurable by a morphometry pipeline.** Nobody has asked the question. Our
   proposed end-plate-sharpness gate would be, as far as this search found, novel — and that is a
   reason for suspicion about the method, not a selling point.
3. **No published work uses Panjabi's segmental ROM as a generative bound.** ROM is used to
   *validate* FE models (B5, B8 compare against it); it has never been used to clip a synthesis.
4. **No spine paper measures a downstream imaging-network gain from FE or musculoskeletal
   generation.** Tapp 2022 ran a compatibility smoke test; Phellan Aro 2024 measured a surrogate
   against its own FEM. The only spine downstream result of any kind (A6) is from a geometric
   displacement model, is unrefereed, and its headline numbers are measured on its own synthetic
   output.
5. **Nothing here can create a transitional vertebra.** Not one method in this angle changes segment
   count or segment identity.
6. **Whether an articulated warp preserves DRR realism is unmeasured.** Zhang 2026 (A4) reports
   SSIM 0.872 / PSNR 18.5 dB for whole-body re-posing on n = 3, and that is a self-comparison at the
   acquisition pose. A6 never projected its volumes at all. Nobody has reported DRR fidelity for a
   spine warp.
7. **POLAFFINI's licence was not read.** The repository has a LICENSE.md; its contents were not
   retrievable through search. Check before depending on it.
8. **Campbell & Petrella's generalisation/specificity values were not retrieved** (paywall). They are
   reported in the paper; I have not seen them.

---

## F. Recommendation from this angle

1. **Do not build a finite element model.** The evidence says it costs hours to days of per-patient
   work even in the best 2025 automated pipeline, its own best-case fidelity to a real spine is
   ~4–6° and ~2.5 mm, its predictions move by up to 6° on material choice alone, it produces no
   image, and the single paper that turned FE output into CT validated it with a smoke test.
2. **Do adopt the log-Euclidean poly-rigid framework by name** (Arsigny 2003/2006/2009), cite the
   three spine instantiations (Drobny 2020, Bukas 2021, Nijmegen scoliosis simulation), and use
   POLAFFINI (github.com/CIG-UCL/polaffini, CPU-only, label-map input, exposes `polyrigid`) as the
   reference implementation rather than writing the blend from scratch. State the contribution as the
   *bound and the validation*, not the warp. The invertibility is a theorem, so the Jacobian check
   becomes a numerical assertion rather than the safety argument.
3. **Take the bound from Panjabi (already on hand) and the shape targets, if wanted, from the
   Rasouligandomani CC-BY repository** — the only openly licensed source of sagittal-balance-
   conditioned plausible thoracolumbar shapes.
4. **Copy the Kovacs validation design, and specifically avoid the Nijmegen flaw:** paired, one
   working point, bootstrap CI, honest small effect, **and a test set of REAL cases only.** A6's
   61.5 → 93.6 is what happens when the test set comes out of the generator; its 12.7% → 3.3% on real
   clinical scans is what the honest effect looks like.
5. **Say in the paper that this is not biomechanics.** Call it articulated (poly-rigid) morphological
   augmentation bounded by published segmental range of motion. The literature supports that phrase
   exactly and supports nothing stronger.
6. **Do not expect this family to solve the 86-subject transitional scarcity.** It broadens the
   sagittal-shape distribution around the transitional cases we already have. Segment count and
   identity have to come from somewhere else.
