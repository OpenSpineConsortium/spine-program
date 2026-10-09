# Adversarial verification — Gaussian Process Morphable Models (GPMM)

Verified 2026-09-23. Candidate came from `ssm.md` entry **E2** (lines 413-418, 488-489).
Everything below was read from the source (arXiv full text, Crossref, GitHub, Springer abstract
pages); nothing is carried over from the angle note.

## Verdict: REJECT for our requirement

Not because the formalism is bad — it is quantitatively validated, permissively licensed and
still maintained — but because for *our* requirement it fails the two halves that matter and
has no evidence for the third:

1. it models **deformation only**, so the "CT" it emits is a warped copy of a source CT, and
   nobody has measured whether such a warp survives DRR rendering;
2. it deforms a **fixed reference topology**, so it cannot add or remove a vertebra — the
   transitional scarcity (86 subjects) is exactly what it cannot fix;
3. **no downstream gain has ever been measured with it**, on spine or on anything else.

## Citation — CONFIRMED exactly

Lüthi M, Gerig T, Jud C, Vetter T. *Gaussian Process Morphable Models.*
IEEE Trans Pattern Anal Mach Intell 2018;40(8):1860-1873.
DOI 10.1109/TPAMI.2017.2739743. PMID 28816655. Preprint arXiv:1603.07254 (23 Mar 2016).
(arXiv lists the author order Lüthi, Jud, Gerig, Vetter; the journal record has Gerig before
Jud. Same paper.)

## What it generates — CONFIRMED, with one correction

A shape is `s = {x + u(x) | x ∈ Γ_R}` for a deformation `u` on a fixed reference `Γ_R`
(Sec 2.2). The prior over `u` is a Gaussian process whose covariance is *any* admissible
kernel — the empirical sample covariance, an analytic kernel (Gaussian, multiscale,
anisotropic), or a sum of both (Sec 3.1, 3.3.2). Represented by the leading terms of a
Karhunen-Loève expansion computed with a Nyström approximation.

**Correction to the candidate summary.** "Surfaces/images via registration; no intensity
synthesis of its own" understates it. There is no intensity *model* — true — but the framework
deforms **images**: the paper's own experiments include 3-D CT image-to-image registration over
the whole forearm domain and model-based segmentation of CT. So a sampled deformation applied
to a source CT *and its label map* does yield a new labelled volume. That is the only route by
which GPMM could meet our requirement at all, and the candidate summary hides it.

## Validation — CONFIRMED as "methods paper, no spine", and weaker than it sounds

- Data: **forearm (ulna + radius)** — 36 segmented images derived from 27 CT images. That is
  the entire evaluation corpus of the paper.
- Tasks: surface registration; active-shape-model segmentation of CT; image-to-image
  registration.
- Metrics: generalisation / specificity / compactness per Styner et al. Reported values
  (full model): Gaussian kernel 5.8 specificity / 299.1 compactness; isotropic multiscale
  6.1 / 317.0; anisotropic multiscale **2.9 / 137.1**. Lower is better.
- **No spine or vertebra data appears anywhere in the paper.**
- **The honest negative the candidate omits:** in the image-registration comparison,
  multi-resolution B-spline registration "yields more accurate results on average than our
  method". GPMM's claim there is parsimony — 500 parameters against 37,926 — not accuracy.
- **There is no small-N ablation.** The "escape hatch when the training set is too small for
  PCA" reading is the authors' *motivation* (Sec 3.3.2: combine the sample covariance kernel
  with a wide-bandwidth Gaussian kernel "to reduce the bias"), not a measured result. Nobody
  quantified how much a kernel-augmented model recovers at small N.

## The 2026 IJCARS lumbar application — REFUTED as evidence for GPMM

Benady A, Zeng H, Zhang S, Chen X, Zhao L, Quarrington RD, Diwan A, Wu L. *Statistical shape
modeling and Gaussian process-based reconstruction of the lumbar spine from partial data: a
proof-of-concept study.* Int J Comput Assist Radiol Surg 2026. DOI 10.1007/s11548-026-03757-2.
PMID 42566161. Paywalled; **the abstract is public and carries numbers**, so the candidate's
"no spine numbers" claim is wrong on the facts.

What it actually did: 13 high-resolution CT datasets of healthy adult lumbar spines; rigid +
3D-3D embedded-deformation non-rigid registration; **PCA** to build the SSM; **Gaussian Process
Regression** to reconstruct a full shape from a partial surface; leave-one-out.

Numbers: first 8 principal modes = 92.7% of variance (on a model with at most 12 modes, so
this is close to vacuous); Average Distance **1.23-3.64 mm** depending on input sparsity;
30.67% of the surface per vertebra sufficient for "clinically acceptable" reconstruction.
Generalisation / specificity / compactness are **not** reported. Code is not stated. Not open
access.

Why this refutes the candidate's framing: this is **plain PCA on n = 13** plus posterior
regression. It is not a GP kernel prior reaching beyond the training data — it is the exact
thing GPMM is supposed to be the escape hatch *from*. It cites no Scalismo use in the abstract.
And an average surface distance of 3.64 mm on a vertebral body ~30 mm across is asserted
"clinically acceptable" without an external criterion; at that error the posterior elements
that name a level are gone, and a DRR cast from it would not be usable for our task.

## Code — CONFIRMED, with one status update

- **Scalismo**, github.com/unibas-gravis/scalismo. **Apache 2.0** — read directly from the
  repository `LICENSE` file, not from the badge. Scala. Latest release **v0.92.0, 4 Jul 2024**
  (v0.91.0 May 2024 moved to Scala 3; v0.92.0 dropped native HDF5 for hdf5-json). Seven listed
  maintainers, University of Basel with Shapemeans GmbH. No release in ~14 months as of today.
- **No Python API exists.** Our entire pipeline is Python (nibabel / scipy / nnU-Net). The
  Python alternative, `pyssam` (arXiv 2301.04416), is a PCA SSAM library, not GPMM.
- **Statismo**, github.com/statismo/statismo: BSD — and stronger than the candidate said. The
  repository was **archived read-only on 29 Jan 2026** and the README states "This repository is
  no longer maintained", pointing at the fork github.com/kenavolic/statismo.
- Error-controlled approximation: Dölz J, Gerig T, Lüthi M, Harbrecht H, Vetter T. *J Math
  Imaging Vis* **2019**;61(4):443-457, DOI 10.1007/s10851-018-0854-5. The candidate said 2018 —
  that is the online-first year; print is 2019.

## Downstream gain — CONFIRMED absent, and absent more broadly than claimed

The candidate says "None measured on spine". The stronger true statement: **no measured
downstream gain from GPMM augmentation exists anywhere.** The one GPMM-as-augmentation paper —
Nbonsou Tegang N, Fouefack JR, Borotikar B, Burdin V, Douglas TS, Mutsvangwa TEM. *A Gaussian
Process Model Based Generative Framework for Data Augmentation of Multi-modal 3D Image Volumes*,
SASHIMI @ MICCAI 2020, DOI 10.1007/978-3-030-59520-3_10 — synthesises co-registered CT/MR pairs
from a single matching pair and evaluates only the consistency between the generated pairs. **No
downstream network is trained; no accuracy-with-and-without number is reported.** No code stated.

Related but *not* GPMM: Uzunova H, Wilms M, Handels H, Ehrhardt J. *Training CNNs for Image
Registration from Few Samples with Model-based Data Augmentation*, MICCAI 2017,
DOI 10.1007/978-3-319-66182-7_26 — statistical *appearance* models, brain/cardiac, and it does
measure a downstream registration gain. That is the paper the angle should chase for
shape-model-based augmentation evidence, not this one.

## Transitional anatomy — no prior art at all

Searched for SSM/GPMM generation of L6 / T13 / sacralised L5. Nothing. The only computational
work on number-variant lumbosacral anatomy is finite-element: models built from CTs of subjects
with 23, 24 and 25 presacral vertebrae (see `biomech.md`), which are hand-built from real scans,
not generated. A GPMM cannot help here in principle: the reference topology is fixed, so an
L5-referenced model and an L6-referenced model are two different models with no path between
them. At most it widens the shape prior *around* the 86 transitional cases we already hold.

## Effort to run on ~2,900 labelled CTs

- **Correspondence is the whole cost.** One reference mesh per level, then non-rigid
  registration of every labelled structure to it: ~17 bony structures per CT x 2,900 CTs
  ≈ 50,000 fits. Scalismo GP fitting is CPU/JVM, minutes per surface → roughly
  **2,000-8,000 CPU-hours**. No GPU. On `reqp` that is days of wall clock, not weeks.
- **Engineering: 4-8 weeks** to a first rendered DRR (mesh extraction from voxel labels,
  JVM↔Python bridge, warp CT + label with one field, round-trip back to NIfTI), then
  **4-6 weeks** to validate anything (per-level generalisation/specificity, DRR realism,
  a downstream with-and-without).
- **What goes wrong, in order of likelihood:**
  1. marching-cubes surfaces from voxel labels are noisy and non-manifold exactly at the
     rib-vertebra and facet contacts — i.e. correspondence fails at the posterior elements that
     carry level identity;
  2. per-vertebra deformations sampled independently interpenetrate their neighbours; a
     multi-object GP model is extra unvalidated work (arXiv 2001.07904);
  3. warping the CT blurs trabecular texture, and a DRR is a line integral through exactly that
     texture — nobody has measured how much deformation a DRR tolerates;
  4. label warping needs nearest-neighbour resampling, which staircases boundaries the DRR will
     show;
  5. our own orientation trap: every mesh↔volume conversion is another place to transpose a
     label away from its CT (CLAUDE.md, "never reorient when writing labels");
  6. thoracic FOV varies across the cohort, so the reference topology is not constant — the
     same blocker as transitional anatomy, arriving through a different door;
  7. Scalismo v0.92 changed the model file format; older tutorial models will not load.

## If someone insists on salvaging it

The one defensible narrow use: **posterior shape models** (condition the GP on observed
landmark positions) to warp an *existing* labelled CT toward a target lordosis by constraining
end-plate landmarks — controlled deformation augmentation within a fixed vertebra count. That
is a real capability of the framework and would give the lordosis/kyphosis control the
requirement asks for. But it is a landmark-driven warping pipeline, for which Python-native,
spine-validated alternatives exist, and GPMM brings no measured advantage over them. It does
nothing for the transitional class.

## Not known

- Whether a GP kernel prior widens a 86-subject transitional stratum usefully. No paper.
- Whether a GPMM-warped CT still renders as a plausible radiograph. No paper, on any anatomy.
- What the IJCARS 2026 paper's full text says about Scalismo/GPMM — only the abstract was read.
