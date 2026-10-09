# Registration-, atlas- and interpolation-based augmentation — prior art

Angle: the "interpolate morphology between subjects" family. Zhao 2019 (CVPR) and its successors,
diffeomorphic interpolation and geodesic shooting (LDDMM, ANTs, Deformetrica, VoxelMorph-based
augmentation), atlas building and template deformation, and biomechanically/anatomically
constrained registration. Searched 2026-09-23. Nothing implemented; this is an evidence file.

Requirement being judged against (restated): in = CT + per-vertebra labels; out = NEW volumes WITH
aligned labels that still render as radiographs; control = target lordosis / kyphosis / transitional
phenotype; variation must be population-plausible and must not fabricate anatomy that does not
occur.

---

## Headline

**This family solves the label problem completely and the anatomy problem not at all.** A single
displacement field warps the CT and the label map together, so labels stay aligned by construction —
that is the one part of the requirement this family satisfies exactly and for free. Everything else
is weaker than it looks.

**Three things are true and decide the verdict.**

1. **A diffeomorphism cannot create a vertebra.** Every method in this angle — Zhao's learned
   transforms, LDDMM geodesic interpolation, atlas deformation, poly-rigid warps — produces a
   smooth invertible map. Such a map preserves the number of connected components and the label
   set. Warping an 5-lumbar spine can never yield an L6, a T13, or a sacralised L5; it yields a
   distorted 5-lumbar spine wearing the same 5 labels. For the 86-subject transitional scarcity
   that is the point of this workflow, this family is structurally incapable, and no amount of
   conditioning or control changes that. This is a mathematical fact about the method class, not an
   empirical gap someone might close.

2. **The measured downstream gains are all in the one-shot to n≈60 regime, and they shrink as data
   grows.** Zhao 2019 gains +4.5 Dice points over single-atlas segmentation from *one* labelled
   brain. Shen 2020 gains ~1.5–3 Dice points at 5–60 training subjects and the curves converge as
   n rises. We hold ~2,900 labelled CTs. **No paper in this family has ever demonstrated a gain at
   n in the thousands**, and the published evidence gives no reason to expect one for the ordinary
   classes. The honest read: registration augmentation is a small-data technique, and on our
   ordinary-class problem we are not in small data. Where we *are* in small data is the
   transitional subset — which is exactly the subset point 1 says this family cannot serve.

3. **Nobody has validated anatomical plausibility of the generated volumes, in any paper in this
   family.** Plausibility is *argued* from the diffeomorphism property and then *evidenced* by
   downstream Dice. Shen 2020 — the flagship "generates anatomically meaningful images via
   interpolation" paper — reports no anatomical-fidelity metric at all. And Rohlfing's 2012 result
   (below) says the downstream/overlap evidence they do report is not valid evidence of a correct
   deformation. So the literature's answer to "does interpolating between two subjects produce
   anatomy that exists?" is: **not measured, anywhere, by anyone.**

**And the VerSe benchmark already published the negative result for our exact task.** Sekuboyina
2021 (MedIA, PMID 34340104), 374 CTs, 4,505 vertebrae, 25 benchmarked algorithms: *"the performance
of an algorithm in labelling and segmenting a spine scan hinges on its ability to correctly identify
vertebrae in cases of rare anatomical variations"*, and the VerSe 2019 iteration found that
atlas- and shape-based methods perform well on normal anatomy **and fail on variants not frequently
present in the training data**. The family under review here is the family that was documented
failing on the phenotype we care about.

**What is worth taking from this angle** is not a generator. It is (a) the poly-rigid/articulated
warp as the citable mechanism for re-posing a labelled spine (PolyPose, §D2 — and the same framework
biomech.md reaches from the other direction), (b) Boisvert's articulated statistics as the published
source of *how much* inter-vertebral pose actually varies (§C1), and (c) a validation vocabulary —
generalisation and specificity — that this family invented and then stopped applying to generators.

---

## A. Methods that produce an image **and** an aligned label map (the deliverable shape)

### A1. Zhao 2019 — "brainstorm", the reference point for this whole angle
- Zhao A, Balakrishnan G, Durand F, Guttag JV, Dalca AV. *Data Augmentation Using Learned
  Transformations for One-Shot Medical Image Segmentation.* CVPR 2019. arXiv:1902.09383.
  openaccess.thecvf.com/content_CVPR_2019/html/Zhao_Data_Augmentation_Using_Learned_Transformations_for_One-Shot_Medical_Image_Segmentation_CVPR_2019_paper.html

- **Generates:** full images + aligned label maps. Two learned models, applied independently: a
  **spatial** transform model (a VoxelMorph registration network trained atlas→unlabelled subject,
  NCC loss) and an **appearance/intensity** transform model. A synthetic example = take the one
  labelled atlas, apply a spatial field sampled from subject *i* and an intensity field sampled from
  subject *j*, warp the atlas label map by the same field.
- **Controlled by:** nothing. Sampling is unconditional — pick a random unlabelled subject's field.
  There is no axis, no target value, no conditioning variable. **This is a hard miss against our
  "control" requirement.**
- **Validated how:** downstream Dice only, on one task. T1 brain MRI pooled from eight public
  databases (ADNI, OASIS, ABIDE, ADHD200, MCIC, PPMI, HABS, Harvard GSP); 101 training scans
  (1 labelled atlas + 100 unlabelled), 50 validation, 100 test; 30 FreeSurfer labels.
  - Single-atlas segmentation (SAS) **0.759**; SAS-aug 0.775; hand-tuned random aug 0.765;
    ours-coupled 0.795; **ours-indep 0.804**; ours-indep + random aug 0.815;
    fully supervised upper bound **0.849**.
  - So: +4.5 Dice points over SAS, closing about half the gap to full supervision, **from a single
    labelled scan.**
- **No anatomical validation** of the synthesised brains. No FID, no landmark check, no
  radiologist read, no distributional comparison against a real cohort.
- **Data fitted on:** brain MRI. Not spine. Not CT.
- **Code:** github.com/xamyzhao/brainstorm — **MIT**, 405 stars, last commit 2020-07-14 (dead; TF1/
  Keras era).
- **Compute:** not reported in the paper.
- **Downstream gain measured:** yes, the numbers above. Brain MRI, one-shot.
- **Fit to our requirement:** labels ✔ aligned; images ✔; control ✘ (none); population plausibility
  ✘ (unmeasured); transitional ✘ (impossible, §Headline 1); regime ✘ (one-shot, we are not).

### A2. Shen 2020 — fluid-based/LDDMM geodesic interpolation ("the interpolate-between-subjects" method proper)
- Shen Z, Xu Z, Olut S, Niethammer M. *Anatomical Data Augmentation via Fluid-based Image
  Registration.* MICCAI 2020, LNCS 12263:318–328. arXiv:2007.02447. PMID 39253359; PMC11381936.
  DOI 10.1007/978-3-030-59716-0_31

- **Generates:** images + segmentations, by interpolating **along geodesics in an LDDMM shape
  space**. Register a source image to K targets, get initial momenta m₀ⱼ; take a convex combination
  Σλⱼm₀ⱼ (λⱼ≥0, Σλⱼ=1); shoot along the resulting geodesic to time t; warp image and label map.
  t∈[0,1] interpolates, t∉[0,1] extrapolates.
- **Controlled by:** λ (which subjects you mix and in what proportion) and t (how far). This is
  *more* controllable than Zhao — you can aim at a specific target subject — but the control is in
  subject space, not in a clinical measurement. **There is no published way to say "give me
  55° lordosis".**
- **Validated how:** downstream Dice only, two datasets.
  - LPBA40 brain (40 subjects; train 5/10/15/20/25, val 5, test 10; K=2). Fluid augmentation beats
    no-augmentation across sizes; **comparable to plain B-spline augmentation on this dataset** —
    i.e. on brain, the expensive geodesic machinery bought nothing over random B-spline warps.
  - OAI knee MRI (train 10/20/30/40/60, val 25, test 52; K=1). Fluid beats both no-augmentation and
    B-spline "by a large margin" — roughly +2–3 Dice points off the figure; the paper gives curves,
    not a table.
  - One-shot atlas segmentation, OAI: Brainstorm **79.94** (2.22) → Fluid-Aug **80.81** (2.35);
    with real appearance, Brainstorm-real **86.83** (2.21) → Fluid-Aug-real (t=1) **87.74** (1.82)
    → Fluid-Aug-real (randomised t) **88.31** (1.56); upper bound **90.01**.
- **Anatomical validation: none.** The PMC text states plausibility follows from diffeomorphisms
  providing "realistic intermediate images" and from retaining the population's appearance
  differences. No metric. **This is the paper whose title claims "anatomical" and whose evidence for
  anatomy is a theoretical property of the transform class.** Say so.
- **Data fitted on:** brain MRI and knee MRI. **Neither spine nor CT is mentioned anywhere in the
  paper.**
- **Code:** github.com/uncbiag/easyreg — licence reported by GitHub as NOASSERTION (i.e. a licence
  file exists but is not a recognised SPDX licence: **check before use**), 176 stars, last push
  2023-01-08.
- **Compute:** the authors name it as the open problem — *"computing the geodesic subspaces is
  costly if they are not approximated by a registration network."* No runtime figures given. LDDMM
  shooting on 3-D CT at our volume sizes is the expensive part, and it is per-pair.
- **Downstream gain measured:** yes, above. Brain and knee MRI, n≤60.
- **Fit:** labels ✔; images ✔; control ~ (subject-space only); plausibility ✘ (unmeasured);
  spine ✘; CT ✘; transitional ✘.

### A3. Olut 2020 — adversarial data augmentation via deformation statistics (AdvEigAug)
- Olut S, Shen Z, Xu Z, Gerber S, Niethammer M. *Adversarial Data Augmentation via Deformation
  Statistics.* ECCV 2020, LNCS 12374:643–659. DOI 10.1007/978-3-030-58526-6_38.
  PDF: ecva.net/papers/eccv_2020/papers_ECCV/papers/123740630.pdf
- **Generates:** deformed images + labels. PCA on deformation fields obtained by deep registration
  over *unlabelled* pairs → a statistical deformation space; perturb labelled samples along
  principal directions, choosing magnitudes adversarially.
- **Controlled by:** eigen-direction and magnitude. The paper's stated selling point is exactly the
  thing we want — *"intuitive control over plausible deformation magnitudes via the statistical
  model"* — i.e. the population supplies the bound, so you are not guessing how far to warp. That
  is the right *idea* for population-plausibility, and nobody has instantiated it on the spine.
- **Validated how:** downstream Dice, knee cartilage from 3-D MRI (OAI). Reported as favourable
  versus state-of-the-art augmentation. No anatomical metric.
- **Data:** knee MRI. Not spine, not CT.
- **Code:** not located in this search. State that plainly rather than assume.
- **Downstream gain:** yes, knee cartilage segmentation; magnitudes not captured here.

### A4. He 2024 — statistical deformation model data augmentation, on CT
- He W, Zhang C, Dai J, Liu L, Wang T, Liu X, Jiang Y, Li N, Xiong J, Wang L, Xie Y, Liang X.
  *A statistical deformation model-based data augmentation method for volumetric medical image
  segmentation.* Med Image Anal 2024 Jan;91:102984. PMID 37837690.
  DOI 10.1016/j.media.2023.102984
- **Generates:** deformed CT + labels. Registration network learns inter-patient deformations; KL
  (Karhunen–Loève) transform of the deformation population; sample new fields from it.
- **Controlled by:** KL mode coefficients. Again no clinical axis.
- **Validated how:** downstream organ-at-risk segmentation Dice on three radiotherapy datasets
  covering head, neck, chest and abdomen; claimed state of the art on several OAR challenges.
  Exact numbers are behind the Elsevier paywall and **were not verified in this search** — the
  abstract carries no figures.
- **Why it matters here:** this is **the closest thing to our setting — CT, volumetric, inter-patient
  deformation statistics — and it is soft-tissue OARs, not bone.** Soft-tissue OAR contours tolerate
  warp blur in a way cortical bone does not (§F4).
- **Code:** not stated in the abstract; not located.

### A5. Uzunova 2017 — model-based augmentation from statistical appearance models
- Uzunova H, Wilms M, Handels H, Ehrhardt J. *Training CNNs for Image Registration from Few Samples
  with Model-based Data Augmentation.* MICCAI 2017, LNCS 10433:223–231.
  DOI 10.1007/978-3-319-66182-7_26
- **Generates:** synthetic image pairs **with dense ground-truth correspondence** — i.e. the
  deformation field itself is the label. Statistical appearance model (shape + intensity) learned
  from few samples, sampled to produce large synthetic training sets.
- **Why it is here:** it is the cleanest statement of the family's real strength — when the label you
  need *is* the deformation, synthesis is exact. For us the label is a segmentation, so this
  advantage partly carries (labels warp exactly) and partly does not (the *anatomy* is still not
  validated).
- **Validated on:** brain and cardiac. Not spine.

### A6. Chaitanya 2021 — semi-supervised task-driven augmentation
- Chaitanya K, Karani N, Baumgartner CF, Erdil E, Becker A, Donati O, Konukoglu E.
  *Semi-supervised task-driven data augmentation for medical image segmentation.*
  Med Image Anal 2021;68:101934. DOI 10.1016/j.media.2020.101934
- **Generates:** images + labels via two learned generators — one **deformation** field generator,
  one **additive intensity** generator — trained adversarially *and* driven by the segmentation
  loss (the augmentation is optimised to help the task, not to look real).
- **Adversarial note:** "optimised to help the task" is the opposite of "anatomically plausible".
  This method will happily produce a deformation no human has, if that deformation lowers the
  segmentation loss. It is a good augmentation method and a **bad population model**, and our
  requirement is a population model.
- **Validated on:** cardiac and prostate MRI, few-labelled-subject regime. Not spine, not CT.

### A7. Kumar 2023 — object-centric diffeomorphic augmentation ("Difeo")
- Kumar N, Gyawali PK, Ghimire S, Wang L. *Learning Transferable Object-Centric Diffeomorphic
  Transformations for Data Augmentation in Medical Image Segmentation.* MICCAI 2023, LNCS
  14222:251–260. arXiv:2307.13645. DOI 10.1007/978-3-031-43895-0_24
- **Generates:** warps **only the object of interest** in place, leaving the rest of the image alone.
  This is the only paper in the family whose mechanism naturally suits "change one vertebra, leave
  the scan alone".
- **Validated how:** kidney tumour segmentation. At 25 % of the data: baseline **0.467**,
  TumorCP **0.568**, TumorCP + Difeo **0.581**. Learned shape variation beat random warping.
- **Adversarial note:** the gain over an existing copy-paste augmentation is **+1.3 Dice points** on
  one organ at one data fraction. That is the size of effect this family delivers once you are past
  the one-shot regime.
- **Data:** abdominal CT (KiTS-type). CT ✔, spine ✘.

### A8. Zheng 2026 — Deformation-Recovery Diffusion Model (DRDM)
- Zheng J-Q, Mo Y, Sun Y, Li J, Wu F, Wang Z, Vincent T, Papież BW. *Deformation-Recovery Diffusion
  Model (DRDM): Instance Deformation for Image Manipulation and Synthesis.* Med Image Anal 2026.
  DOI 10.1016/j.media.2026.103987. arXiv:2407.07295. Project: jianqingzheng.github.io/def_diff_rec/
- **Generates:** deformation fields (not images directly) by a diffusion process that learns to
  *recover* realistic deformation from randomly-deformed input; multi-scale deformation velocity
  fields with a stated topology-preserving generation strategy; deformation scale >10 % of image
  size. Apply the field to image and labels.
- **Why it is in this angle and not the diffusion one:** it is registration-free but it is still a
  *warp generator* — same capability ceiling, same topology constraint.
- **Validated on:** cardiac MRI and pulmonary CT. Gains reported on 2-D segmentation and 3-D
  registration; **the project page and abstract give no numbers**, and the numbers were not
  retrieved here. Treat as unquantified until the MedIA paper is read.
- **Code:** github.com/jianqingzheng/def_diff_rec. Licence not stated on the project page.

### A9. Hierarchical encoding of deformation fields between CT images
- Anon./see record: *Data Augmentation Using the Hierarchical Encoding of Deformation Fields Between
  CT Images.* IEEE Trans Radiat Plasma Med Sci 2024;8:939–949. IEEE Xplore document 10547219.
- Encodes deformation fields into hierarchical latent variables; editing a chosen layer changes the
  scale of the synthesised variation; claims **CT values are preserved patient-specifically** while
  shape varies — which is the property we need for DRR casting.
- **Not verified:** the Xplore page would not render in this session. Anatomy, cohort size and all
  quantitative results are **unknown to me**. Flagged as worth one paid retrieval; do not cite its
  numbers until read.

### A10. SynthSeg / SynthMorph — random diffeomorphic warping of label maps + intensity sampling
- Billot B, Greve DN, Puonti O, Thielscher A, Van Leemput K, Fischl B, Dalca AV, Iglesias JE.
  *SynthSeg: Segmentation of brain MRI scans of any contrast and resolution without retraining.*
  Med Image Anal 2023;86:102789. PMID 36857946. Code github.com/BBillot/SynthSeg.
- Hoffmann M, Billot B, Greve DN, Iglesias JE, Fischl B, Dalca AV. *SynthMorph: learning
  contrast-invariant registration without acquired images.* IEEE Trans Med Imaging 2022;41(3):543–558.
  arXiv:2004.10282.
- **Mechanism, and why it belongs here:** the generator is *exactly* the augmentation machinery of
  this angle — take a label map, apply an affine plus a **diffeomorphic warp obtained by integrating
  a smooth random stationary velocity field (scaling-and-squaring)**, then paint intensities from a
  randomised GMM. Image and labels are aligned by construction.
- **Validated how:** 5,000 scans, six modalities, ten resolutions; generalisation to unseen domains
  far beyond supervised CNNs, domain adaptation and Bayesian segmentation. This is by far the
  **best-validated** method in the whole angle — but what it validates is *robustness of a
  downstream network*, not realism of the synthesised images. The intensities are deliberately
  unrealistic; realism is explicitly not the goal.
- **Fit to us:** directly hostile to our requirement. We need the DRR to look like a radiograph.
  SynthSeg's whole thesis is that you get better generalisation by making the images *not* look
  real. Worth knowing as the counter-hypothesis to the entire realism programme; worth nothing as a
  realism method.

---

## B. Atlas building and template deformation

### B1. ANTs / SyN — the reference implementation
- Avants BB, Epstein CL, Grossman M, Gee JC. *Symmetric diffeomorphic image registration with
  cross-correlation.* Med Image Anal 2008;12(1):26–41.
- Klein A, Andersson J, Ardekani BA, et al. *Evaluation of 14 nonlinear deformation algorithms
  applied to human brain MRI registration.* NeuroImage 2009;46(3):786–802. PMID 19195496.
  — 14 algorithms, 8 error measures, >45,000 registrations between 80 manually labelled brains;
  SyN among the top performers. **This is the strongest external validation any tool in this angle
  has, and it is brain MRI registration accuracy — not generation.**
- Avants BB, Yushkevich P, Pluta J, et al. *The optimal template effect in hippocampus studies of
  diseased populations.* NeuroImage 2010;49(3):2457–2466. PMID 19818860.
  — template *choice* measurably changes the answer you get. Relevant warning: an atlas is not
  neutral; building one from our cohort bakes our cohort's biases into everything sampled from it.
- **Code:** github.com/ANTsX/ANTs — **Apache-2.0**, 1,501 stars, actively maintained (push 2026-09-23).
  `antsMultivariateTemplateConstruction2.sh` is the atlas builder.
- **Compute:** SyN on a full abdominopelvic CT is minutes to tens of minutes per pair on CPU;
  template construction is O(n × iterations) pairs. For 802 CTs this is a grid job, not a laptop job.
- **Downstream augmentation gain on spine: none published.**

### B2. Deformetrica 4 — LDDMM atlas, geodesic regression, parallel transport
- Bône A, Louis M, Martin B, Durrleman S. *Deformetrica 4: An Open-Source Software for Statistical
  Shape Analysis.* ShapeMI @ MICCAI 2018, LNCS 11167:3–13. DOI 10.1007/978-3-030-04747-4_1
- **Why it is the most interesting tool in §B for us:** it ships **geodesic regression** and
  **parallel transport** — the published machinery for "move this subject along a trajectory
  estimated from a population", i.e. the closest thing that exists to "interpolate along a clinical
  axis" in a principled shape space.
- **Code/licence:** gitlab.com/icm-institute/aramislab/deformetrica, reported **MIT** on the
  repository page (verify in-tree before relying on it; the project site was unreachable from here).
- **Validated on:** craniofacial surgery, Alzheimer classification, cranioplasty planning. Shape
  meshes primarily. **No spine CT application located.**
- **Adversarial note:** it operates on shapes/meshes and currents, not on CT intensity. Getting a
  renderable CT out the other end is our problem, not the tool's.

### B3. Dalca 2019 — conditional deformable templates (the control hook)
- Dalca AV, Rakic M, Guttag J, Sabuncu MR. *Learning Conditional Deformable Templates with
  Convolutional Networks.* NeurIPS 2019:804–816. arXiv:1908.02738.
- **Generates:** a template **conditioned on an attribute** (their demonstration: age, sex), plus a
  network that aligns any image to it. This is the one paper in the angle that gets the *control*
  requirement structurally right: condition the template on a continuous covariate and you can ask
  for the template at a given value.
- **Validated on:** neuroimaging. Sharpness/centrality of the learned templates and registration
  accuracy; **no generation study, no plausibility metric, no downstream augmentation experiment.**
- **Direct relevance:** replace "age" with "lumbar lordosis" or "pelvic incidence" and you have the
  published skeleton of a conditional spine template. **Nobody has done this on the spine.** It
  would still not make an L6.
- **Code:** in the VoxelMorph repository, github.com/voxelmorph/voxelmorph — **Apache-2.0**, 2,754
  stars, actively maintained (push 2026-09-11).

### B4. Aladdin — joint atlas building and diffeomorphic registration
- Ding Z, Niethammer M. *Aladdin: Joint Atlas Building and Diffeomorphic Registration Learning with
  Pairwise Alignment.* CVPR 2022:20784–20793. arXiv:2202.03563.
  Code github.com/uncbiag/Aladdin — **Apache-2.0**, 18 stars, last push 2022-07-04 (stale).
- Adds a pairwise image-similarity loss because a fuzzy atlas has no clear structures to align to.
  Brain MRI. No generation study.
- Related: Sinclair M, et al. *Atlas-ISTN: Joint segmentation, registration and atlas construction
  with image-and-spatial transformer networks.* Med Image Anal 2022;78:102383. arXiv:2012.10533.

### B5. Multi-atlas registration on spine CT — the one place this family has real spine numbers
- Forsberg D. *Atlas-Based Registration for Accurate Segmentation of Thoracic and Lumbar Vertebrae
  in CT Data.* In: Recent Advances in Computational Methods and Clinical Applications for Spine
  Imaging, LNCVB 20:49–59, 2015. DOI 10.1007/978-3-319-14148-0_5
  — CSI 2014 challenge, 10 test sets: **mean Dice 0.94 ± 0.03, point-to-surface 1.05 ± 0.65 mm.**
- **Read this correctly.** It validates registration *as a segmentation method*, on normal-ish
  anatomy, at n=10. It does not validate any warp as a *generator*, and the VerSe result (Headline)
  says this class breaks on variants. Using 0.94 Dice as evidence that inter-subject spine warps are
  anatomically faithful would be exactly the mistake Rohlfing 2012 (§E1) documents.

---

## C. Spine-specific shape/pose models — and the only work that interpolates along a clinical axis

### C1. Boisvert 2008 — articulated statistics of the spine on a Riemannian manifold ⟵ **the one to cite for "how much pose variation is real"**
- Boisvert J, Cheriet F, Pennec X, Labelle H, Ayache N. *Geometric variability of the scoliotic spine
  using statistics on articulated shape models.* IEEE Trans Med Imaging 2008;27(4):557–568.
  PMID 18390352. DOI 10.1109/TMI.2007.911474
- **Represents** a spine as a vector of **relative poses between neighbouring vertebrae** — rigid
  transforms, which do not live in a vector space, so they use the **Fréchet mean and a generalised
  covariance in the exponential chart**, then PCA on that covariance.
- **Fitted on 295 scoliotic patients**, plus deformation analyses of Cotrel-Dubousset surgery (33),
  Boston brace (39) and untreated progression (26).
- **Findings that directly bound a generator:** inter-vertebral pose variability is
  **inhomogeneous** (lumbar more variable than thoracic) and **anisotropic** (maximal rotational
  variability about the coronal axis; maximal translational variability axially). Brace and surgery
  shift both the Fréchet mean and the covariance in specific regions.
- **Why it matters to us:** this is a published, population-derived answer to "how far may I rotate
  L4 on L5 before I have left the human population?", per level and per axis — and it is on 295
  spines. It is the statistical complement to the Panjabi ROM bound in biomech.md. Combine them and
  a per-level pose sampler has an external bound rather than a guessed one.
- **What it does not do:** it never emits an image, or a label map, or a volume. It is a model of
  landmark-derived poses from biplanar radiograph reconstructions. **Cohort is scoliotic
  adolescents, not our abdominopelvic adults** — the covariance is not ours and should not be
  reused unchecked.
- **Code:** none published.

### C2. Kadoury 2017 — the only published interpolation *along a clinical axis*
- Kadoury S, Mandel W, Roy-Beaudry M, Nault M-L, Parent S. *3-D Morphology Prediction of Progressive
  Spinal Deformities From Probabilistic Modeling of Discriminant Manifolds.* IEEE Trans Med Imaging
  2017;36(5):1194–1204. PMID 28129153. DOI 10.1109/TMI.2017.2657225
- Discriminant probabilistic manifold embedding of 3-D spine reconstructions; a spatiotemporal
  regression built from **parallel transport curves** inferred from neighbouring exemplars; navigate
  the geodesic and read off the spine at any time point by exponential mapping.
- **Validated on 745 longitudinal reconstructions from 133 subjects:** 81 % classification of
  progressive vs non-progressive, and **2.1° mean prediction difference in main curve angulation**
  against the real follow-up.
- **This is the strongest validation in the entire angle for "the interpolated shape is the shape
  that actually occurred"** — because the target existed and was measured. It is, however, *temporal*
  progression in adolescent idiopathic scoliosis, on biplanar-X-ray reconstructions, producing
  landmark models and not images.
- No code; no CT; no labels; no volume.
- Precursor: Boisvert J, et al. *Principal spine shape deformation modes using Riemannian geometry
  and articulated models.* AMDO 2006, LNCS 4069:346–355.

### C3. Rasoulian 2013 — statistical multi-vertebrae shape **+ pose** model, on CT
- Rasoulian A, Rohling R, Abolmaesumi P. *Lumbar spine segmentation using a statistical
  multi-vertebrae anatomical shape+pose model.* IEEE Trans Med Imaging 2013;32(10):1890–1900.
  PMID 23771318. DOI 10.1109/TMI.2013.2268424
- **Separates shape from pose across the lumbar vertebrae in one model** — the structurally right
  factorisation for our problem: change pose (lordosis) without changing shape, or vice versa.
- **Fitted and validated on CT from 32 subjects; mean segmentation error < 2 mm.** Validated as a
  *segmentation* method, on 32 subjects, lumbar only.
- Extended: Rasoulian A, et al. *Lumbar and thoracic spine segmentation using a statistical
  multi-object shape+pose model.* LNCVB 20, 2015. DOI 10.1007/978-3-319-14148-0_19
- No code located. Generation was never attempted or measured.

### C4. Meng 2020 — statistical full-spine surface model, fitted on VerSe
- Meng D, Keller M, Boyer E, Black M, Pujades S. *Learning a Statistical Full Spine Model from
  Partial Observations.* ShapeMI @ MICCAI 2020, LNCS 12474:122–133. DOI 10.1007/978-3-030-61056-2_10
  HAL hal-02983880.
- PPCA over C1–L5 surfaces learned from **partial** views — the honest solution to the fact that no
  public dataset images the whole spine. **Trained on VerSe 2019**, which is one of the datasets we
  hold.
- **Code/model:** gitlab.inria.fr/spine/spine_model, released **for non-commercial use** — note the
  standing commercialization stance in memory; a non-commercial licence is a hard blocker for the
  product track even if it is fine for a paper.
- Validated by low-dimensional reconstruction error of the population. Surfaces only; no intensities,
  no CT, no downstream task.

### C5. Campbell & Petrella 2016 — SSM-generated *virtual population* of lumbar spines
- Campbell JQ, Petrella AJ. *Automated finite element modeling of the lumbar spine: Using a
  statistical shape model to generate a virtual population of models.* J Biomech
  2016;49(13):2593–2599. PMID 27270207. DOI 10.1016/j.jbiomech.2016.05.013
- **The only spine paper in this angle that explicitly generates a population** — mean shape and
  ±3 SD along each of **17 shape modes**, each turned into a working FE model.
- **Evaluated with compactness, generalisation ability and specificity** — i.e. it is the one spine
  paper that applies the correct metric for "is a generated shape close to a real one" (§E2).
- **Fitted on 18 cadaveric specimens of unknown demographics.** Eighteen. Any covariance estimated
  from 18 subjects over a 17-mode space is very close to interpolating its own training set, and
  ±3 SD along a mode estimated from 18 cadavers is an extrapolation with no population behind it.
  Say this plainly if the paper is cited.
- Surfaces/meshes → FE models. No CT volume, no labels, no image.

### C6. Bayat 2020/2022 — supine CT re-posed to standing, driven by radiographs
- Bayat A, Sekuboyina A, Paetzold JC, Payer C, Štern D, Urschler M, Kirschke JS, Menze BH.
  *Inferring the 3D Standing Spine Posture from 2D Radiographs.* MICCAI 2020, LNCS 12266:775–784.
  arXiv:2007.06612. DOI 10.1007/978-3-030-59725-2_75
- Bayat A, et al. *Anatomy-Aware Inference of the 3D Standing Spine Posture from 2D Radiographs.*
  Tomography 2022;8(1):479–496. PMC8879677.
- **This is the closest published thing to "control the lordosis of an existing labelled spine".**
  TransVert takes orthogonal radiographs plus the per-vertebra 3-D shapes from a supine CT and
  assembles an upright spine: **per-vertebra affine (scale + 3-D rotation, chosen with regard to the
  global spinal shape) plus a local deformable component on the vertebral surface.** That is an
  articulated re-posing of a labelled spine — our §D2 mechanism, driven by a real target instead of
  a sampled one.
- **Fitted on ~954 CT scans / ~12,000 vertebrae** (800 from a public lung-nodule set + 154 in-house),
  5-fold CV; evaluated on DRRs at **Dice 0.9510, Hausdorff 5.70 mm, nWESD 0.1797**; clinical check on
  **30 patients** with real standing radiographs, and the rotation-invariant comparison
  (nWESD 0.13 vs 0.15) rests on **2 patients / 32 vertebrae**.
- **The output is voxel maps / shape models — not a CT intensity volume.** To render a DRR you would
  still have to carry the intensities through the same per-vertebra transforms yourself.
- **Code: not reported.**
- **Adversarial:** the headline Dice is measured on DRRs, i.e. on synthetic inputs from the same
  pipeline; the real-radiograph evidence is two patients.

---

## D. Biomechanically / anatomically constrained registration of the spine

### D1. Jian 2022 — weakly-supervised biomechanically-constrained CT/MRI spine registration
- Jian B, Azampour MF, De Benetti F, Oberreuter J, Bukas C, Gersing AS, Foreman SC, Dietrich A-S,
  Rischewski J, Kirschke JS, Navab N, Wendler T. *Weakly-supervised Biomechanically-constrained
  CT/MRI Registration of the Spine.* MICCAI 2022, LNCS 13436:227–236. arXiv:2205.07568.
  DOI 10.1007/978-3-031-16446-0_22
- Four losses enforce per-vertebra rigidity and volume: rigid Dice, rigid field (SVD-derived average
  rigid transform inside each vertebra), Jacobian-determinant properness, orthonormality of the
  rotation part.
- **In-house cohort of 167 patients, 1,280 vertebrae** (117/25/25 train/val/test).
- Test numbers — **read the folding column:**

  | | proposed (pc+rigid-dice) | learned baseline | conventional |
  |---|---|---|---|
  | Dice | 0.78 (0.11) | 0.78 (0.10) | 0.77 (0.13) |
  | rigid Dice | **0.90 (0.05)** | 0.86 (0.06) | 0.89 (0.03) |
  | volume change % | 5.12 (6.13) | 10.21 (8.91) | **2.02 (1.65)** |
  | folding voxels | **18.30 (63.20)** | 0.04 (0.20) | **0** |
  | runtime (s) | 3.4 (1.1) | 3.5 (1.3) | 243 |

  The anatomy-aware losses buy **zero** overall Dice, buy +4 points of rigid Dice, and **introduce
  folding where the baseline and the conventional method had essentially none** — 18 folded voxels
  on average, with an SD of 63, means some cases fold badly. A field that folds is not invertible and
  is not a valid anatomy. **Penalty-based rigidity is a soft constraint that can be violated; the
  poly-rigid construction in D2 cannot.** This is the concrete argument for construction over penalty.
- **Code:** github.com/BailiangJ/spine-ct-mr-registration — **MIT**, 29 stars, last push 2023-04-25.

### D2. PolyPose 2025 — polyrigid deformable 2D/3D registration ⟵ **the mechanism to adopt**
- Gopalakrishnan V, Dey N, Golland P. *PolyPose: Deformable 2D/3D Registration via Polyrigid
  Transformations.* arXiv:2505.19256 (v5, Oct 2025). polypose.csail.mit.edu
- Parameterises the deformation as a **convex combination of rigid transforms in the tangent space
  𝔰𝔢(3)**, weighted per bone; Lie exp/log makes the field **smooth, invertible and fold-free by
  construction**, not by penalty.
- **Produces warped 3-D CT volumes and the deformation fields** — so labels ride along.
- Validated: Head&Neck **31 patients** (rigid structures Dice >0.90; soft tissue highest of the
  compared methods); **DeepFluoro, 6 cadavers** — pelvis Dice **0.99**, femurs **0.98**,
  HD95 1.48 / 1.56 mm, **0.00 % topological folds**; ThoraxCBCT 13 patients.
- **Never used or evaluated as a data-augmentation generator.** Zero downstream numbers. It is a
  registration method whose transform parameterisation happens to be exactly what a spine re-poser
  needs.
- **We already hold DeepFluoro** (see memory: deepfluoro-convention), so the validation cohort
  overlaps ours — unusually easy to reproduce their numbers before trusting them.
- Licence: paper CC BY 4.0; check the code repository licence separately.

### D3. The older constraint literature, for citation completeness
- Little JA, Hill DLG, Hawkes DJ. *Deformations incorporating rigid structures.* Comput Vis Image
  Underst 1997;66(2):223–232. — the original "rigid bones in deformable soft tissue" warp.
- Staring M, Klein S, Pluim JPW. *A rigidity penalty term for nonrigid registration.* Med Phys
  2007;34(11):4098–4108. — implemented in **elastix** (github.com/SuperElastix/elastix,
  **Apache-2.0**, 586 stars, actively maintained). A ready-made, widely-used soft rigidity
  constraint; same soft-constraint caveat as D1.
- Arsigny V, Commowick O, Pennec X, Ayache N — log-Euclidean polyaffine framework; see biomech.md
  §A1 for the full citation chain. PolyPose is its learned 2D/3D instantiation.
- *MAIRNet: weakly supervised anatomy-aware multimodal articulated image registration network.*
  Int J Comput Assist Radiol Surg 2023. DOI 10.1007/s11548-023-03056-0 — articulated spine
  registration; not read in detail here.

### D4. LiftReg — the only place DRRs and a statistical deformation model meet
- Wang L, Shen Z, Greer H, Niethammer M. *LiftReg: Limited Angle 2D/3D Deformable Registration.*
  MICCAI 2022, LNCS 13436:207–216. arXiv:2203.05565. Code github.com/uncbiag/LiftReg.
- Trained on **DRR/CT pairs** so that a high-quality CT–CT similarity can supervise a 2D/3D
  deformable registration; uses a **statistical deformation model** to constrain the space.
- Validated on **DirLab lung**; beats existing learned pairwise 2D/3D deformable registration.
- Relevance: it is the existing proof that a statistical deformation space and DRR rendering compose
  in one pipeline. It is **lung, not spine**, and the DRRs are the *input*, not the thing whose
  realism is being judged.

---

## E. How this family validates itself — and the two results that undercut it

### E1. Overlap and image similarity are not evidence of a correct deformation
- Rohlfing T. *Image similarity and tissue overlaps as surrogates for image registration accuracy:
  widely used but unreliable.* IEEE Trans Med Imaging 2012;31(2):153–163. PMID 21827972.
  PMC3274625.
- He constructs a deliberately **wrong** registration algorithm that scores **extremely well** on
  tissue overlap, image similarity, image difference and inverse-consistency. Conclusion, verbatim:
  *"tissue overlap and image similarity, whether used alone or together, do not provide valid
  evidence for accurate registrations and should thus not be reported or accepted as such."* Only
  overlap of **localised** anatomical regions distinguishes reasonable from inaccurate.
- **Consequence for this whole angle:** almost every number quoted above is a Dice. Dice on a warped
  label map tells you the warp moved the label to where the label is. It does not tell you the warp
  moved the *bone* the way bone moves. Any adoption here must carry an external check — landmark
  error, a measured angle, or a comparison to a published distribution.

### E2. The right metric for "is this generated shape a real shape" exists, and this family stopped using it
- Davies' pair: **generalisation** (can the model fit unseen real shapes?) and **specificity** (are
  the shapes the model generates close to real ones?). Specificity is precisely the "average that is
  nobody" test, and it is standard in statistical shape modelling.
- Goparaju A, Iyer K, Bône A, et al. *Benchmarking off-the-shelf statistical shape modeling tools in
  clinical applications.* Med Image Anal 2022;76:102271. PMID 34974213. arXiv:2009.02878.
  — head-to-head of ShapeWorks, Deformetrica and SPHARM-PDM; the groupwise-correspondence tools
  (ShapeWorks, Deformetrica) are more consistent and capture clinically relevant variability better
  than SPHARM-PDM; ShapeWorks gives the most consistent anatomical measurements.
- **Campbell & Petrella 2016 (C5) is the only spine paper in this file that reports specificity.**
  Zhao, Shen, Olut, He, Chaitanya, Kumar and DRDM report none. The generator literature adopted the
  transform machinery of shape modelling and dropped its evaluation protocol.

### E3. What "validated" therefore means in this angle, stated bluntly
- **Validated as registration:** SyN/ANTs (Klein 2009, 14 algorithms, 80 brains), Forsberg on spine
  CT (Dice 0.94, 1.05 mm, n=10), Rasoulian on spine CT (<2 mm, n=32), PolyPose (Dice 0.99, 0 % folds,
  DeepFluoro).
- **Validated as augmentation, by downstream accuracy, in small-data regimes:** Zhao (+4.5 Dice,
  brain, one-shot), Shen (+~2–3 Dice, knee, n≤60; one-shot 86.83→88.31), Kumar (+1.3 Dice, kidney
  tumour at 25 % data), He (OAR CT, numbers unread), Olut (knee, numbers not captured).
- **Validated as a generator of anatomy that exists:** *nothing, on any anatomy.* The closest is
  Kadoury 2017's 2.1° prediction of a real follow-up curve — and that is a landmark model of
  scoliosis progression, not an image.
- **Validated on spine CT as a generator:** nothing. Not one paper.
- **Validated as producing volumes that render as radiographs:** nothing. Not one paper in this
  angle renders its output.

---

## F. The failure modes, for our requirement specifically

**F1. Topology is a hard wall.** A diffeomorphism is a smooth invertible map with smooth inverse. It
cannot split a label, merge two, or add a sixth lumbar body. The transitional phenotypes are changes
of segment count and identity. **This family cannot make them, ever.** Anything that claims to has
left the diffeomorphic setting (and with it the invertibility guarantee the family's plausibility
argument rests on).

**F2. "An average that is nobody" — genuinely unresolved, and the literature is quiet about it.**
Two facts frame it. (a) Convex interpolation in an LDDMM geodesic subspace (Shen 2020) is not
averaging in image space, so the classic blurry-average artefact does not apply directly. (b) But
*no one has measured whether the interpolant is a shape a person has.* The one test designed for
this — specificity — is not reported by any generator in §A. On the spine there is a specific reason
to worry: Boisvert 2008 found inter-vertebral pose variability is **inhomogeneous and anisotropic**,
so a warp field that is smooth and isotropic by construction will distribute variation in a pattern
the population does not have. Whether that produces a spine nobody has is **not known** and would
have to be measured here.

**F3. Label carrying is the family's one clean win.** The same field warps CT and labels; a
nearest-neighbour (or one-hot-then-argmax) resample of the label map keeps the correspondence exact.
Two caveats worth stating: nearest-neighbour resampling of a thin structure under a large warp
aliases and can break continuity at the lamina and the rib heads — the same structures the LCC
postprocessing already deletes in this project (memory: spondylolysis-and-border-anomaly-findings);
and warping a label map through a field derived from a *different* subject's anatomy propagates that
subject's segmentation errors into the new case.

**F4. CT intensities are the unaddressed part, and the spine is the worst case.** Every resample
trilinearly interpolates HU. Cortical bone is one to two voxels thick and is a step of ~1,500 HU;
interpolation blurs that step, and a DRR integrates along rays so a blurred cortex becomes a
low-contrast cortex in the render. **Nobody in this literature has measured what a warp does to the
DRR.** The TRPMS 2024 paper (A9) claims patient-specific CT values are preserved while shape varies
and is the only candidate that even states the concern — and its numbers are unread. Given this
project's own record (memory: "Render the mask"; and the DRR row-spacing defect), the right response
to "does a warped CT still render like a radiograph?" is to render one, not to reason about it.

**F5. The regime mismatch is the quietest and strongest objection.** Every measured gain in §A is at
n ≤ 101 labelled subjects. We have ~2,900 labelled CTs. The published evidence does not say
registration augmentation helps at our scale; it says nothing about our scale at all. Presenting a
+4.5-Dice one-shot brain result as support for augmenting a 2,900-CT corpus would be the kind of
plausible-but-wrong move this project keeps getting caught by.

---

## G. Downstream gains actually measured (the whole table, so the size of the effect is visible)

| Method | Task / anatomy / modality | Train size | Without | With | Δ |
|---|---|---|---|---|---|
| Zhao 2019 | brain MRI seg, 30 labels | 1 labelled + 100 unlabelled | 0.759 (SAS) | **0.804** | +4.5 |
| Zhao 2019 (+ random aug) | same | same | 0.759 | 0.815 | +5.6 (vs 0.849 supervised) |
| Shen 2020 one-shot | knee MRI (OAI) | 1 atlas | 86.83 (Brainstorm-real) | **88.31** | +1.5 (ceiling 90.01) |
| Shen 2020 aug | knee MRI (OAI) | 10–60 | ~76–88 | ~79–90 | ~+2–3, from figure |
| Shen 2020 aug | brain MRI (LPBA40) | 5–25 | baseline | ≈ B-spline aug | ~0 vs cheap baseline |
| Kumar 2023 | kidney tumour CT | 25 % of data | 0.568 (TumorCP) | **0.581** | +1.3 |
| He 2024 | OAR CT, head/neck/chest/abdomen | not read | — | — | claimed SOTA, **numbers unverified** |
| Olut 2020 | knee cartilage MRI | not captured | — | — | "favourable", **numbers unverified** |
| DRDM 2026 | cardiac MRI, lung CT | not read | — | — | "notable gains", **numbers unverified** |
| **any of the above** | **spine, any task** | — | — | — | **none published** |

---

## H. What is not known

- Whether interpolating between two spine CTs produces a spine that a person has. No specificity
  measurement exists for any of these generators, on any anatomy.
- Whether a warped CT still casts a radiograph-like DRR. Not measured by anyone in this family.
- Whether registration augmentation helps at all at n ≈ 2,900. Untested; all evidence is n ≤ 101.
- The contents of the TRPMS 2024 hierarchical-deformation paper (A9) — the one CT-and-HU-preserving
  candidate — anatomy, cohort and results all unread here.
- He 2024 (MedIA) numbers, Olut 2020 numbers, DRDM numbers: all behind paywalls or not retrieved.
- Whether Boisvert's scoliotic-adolescent pose covariance transfers to our abdominopelvic adult
  cohort. Almost certainly not directly; nobody has published the equivalent for a normal adult CT
  cohort.
- Deformetrica's exact in-tree licence (reported MIT by the GitLab page; the project site was
  unreachable from here), and easyreg's (GitHub reports NOASSERTION).

---

## I. Verdict for this project

**Do not adopt any §A augmentation method as the generator.** They were built for the one-shot
regime, they cannot be steered to a clinical target, they cannot make a transitional vertebra, none
was validated on spine or CT as a generator, and none was validated for anatomical plausibility at
all. Zhao 2019 is the canonical citation for the idea and a dead 2020 TF1 repository; Shen 2020 is
the strongest instantiation and its own authors call the compute prohibitive and offer no
plausibility metric.

**Take three things from this angle instead.**

1. **The warp.** PolyPose's 𝔰𝔢(3) convex-combination parameterisation (D2) — invertible and fold-free
   *by construction*, validated to Dice 0.99 and 0.00 % folds on DeepFluoro, which we already hold.
   It converges with biomech.md's independent conclusion (log-Euclidean polyaffine). Jian 2022 (D1)
   is the published demonstration that the *penalty* alternative fails: no Dice gain and it
   introduces folding.
2. **The bound.** Boisvert 2008 (C1) is a published, per-level, per-axis, anisotropic covariance of
   inter-vertebral pose over 295 spines — an **external** source for how far a level may be moved,
   to sit alongside Panjabi's ROM. Neither is our cohort; both are outside our computation, which is
   the point.
3. **The evaluation.** Generalisation and specificity (E2), plus a rendered DRR check (F4), plus an
   external distributional comparison of the generated lordosis/kyphosis/PI against published
   normative series. This is the part the literature dropped, and supplying it is a real
   contribution rather than a reimplementation.

**And state the limit up front in anything we write:** this family broadens the pose and shape
distribution around the cases we already have. It cannot manufacture an L6. For the 86-subject
transitional scarcity, the answer is not here.
