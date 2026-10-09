# Adversarial verification — Meng et al. 2020, full-spine statistical surface model

Angle: statistical shape / shape-intensity models of the spine.
Verified 2026-09-23 against the paper PDF and the live repository, not against a summary.

**Citation.** Di Meng, Marilyn Keller, Edmond Boyer, Michael J. Black, Sergi Pujades.
"Learning a Statistical Full Spine Model from Partial Observations." Shape in Medical Imaging
(ShapeMI @ MICCAI 2020), LNCS 12474, Springer, pp. 122–133.
DOI 10.1007/978-3-030-61056-2_10. HAL hal-02983880. No PMID (workshop paper, not indexed in PubMed).
Semantic Scholar CorpusId 222179860; 10 citations as of 2026-09-23.

**Sources actually read.**
- Full PDF: `https://inria.hal.science/hal-02983880/file/spine_surface_model.pdf` (13 pp incl. HAL cover).
  HAL and gitlab.inria.fr are both behind Anubis, which challenges any `Mozilla/*` User-Agent.
  `curl -A "curl/8.4.0"` is served normally. This is a different block from the JA3/Cloudflare
  case already in the notes — the fix is the opposite one (look *less* like a browser, not more).
- Repository: `https://gitlab.inria.fr/spine/spine_model` — README.md, Licence.md, Install.md,
  QuickStart.md, requirements.txt, full file tree and commit log via the GitLab API.

---

## 1. What it actually generates — CONFIRMED, with two corrections

Confirmed from the paper:

- 24 vertebrae, C1–L5 (7 cervical, 12 thoracic, 5 lumbar). Full-spine mesh = **127,294 vertices,
  254,636 faces** across the 24 parts.
- **Surfaces only.** No intensities, no HU, no CT. Nothing to render a DRR from without a separate
  surface→volume→attenuation step that the paper does not provide or discuss.
- **No sacrum, no pelvis, no ribs, no discs.** The model stops at L5. Confirmed by exhaustion: the
  word "sacrum" does not appear in the paper, and the artist templates are 24, one per vertebra.
- Architecture is SMPL-style: a "graphical model mesh architecture" with shape parameters β adding
  additive offsets to a mean template Tµ, plus per-vertebra rotation and translation applied rigidly.
  The released model file is literally named `vertebra_smpl_v10.pkl`.

Two corrections to the candidate summary:

**(a) The "global/local rotation model" is not statistical.** The paper is explicit: they fit a
Gaussian to the *relative translation* of each of the 23 neighbouring vertebra pairs — and
*"as the relative rotation between vertebrae highly depends on the patient posture, we do not learn
a pose prior on the relative rotations."* So the model has a learned distribution over
inter-vertebral **spacing** (disc thickness) and **none at all** over inter-vertebral **angulation**.
Lordosis, kyphosis and sagittal alignment live entirely in the rotations. This is the single most
important fact for us and it was not in the summary: **the released model cannot tell you what a
population-plausible lumbar lordosis is.** Posing it to a target lordosis is possible mechanically
(the demo exposes `-R` global and `-r` local rotations) but the plausibility is on you, not on the
model. For a project whose requirement is "place the sample at a target lordosis or kyphosis",
that is the wrong half of the parameterisation.

**(b) The shape space is per-spine, not per-vertebra-conditioned.** β is a single global vector over
the concatenated 24-vertebra mesh. You cannot independently perturb L5 while holding T12 fixed
within the model; the strong inter-vertebral correlation the paper celebrates is exactly what
prevents that.

## 2. Validation — the summary is WRONG in one direction and RIGHT in another

The candidate summary says the completion result is "a COMPLETION test, not a specificity test, and
no generalisation/specificity/compactness table was reported." Point by point:

- **Compactness: REPORTED.** Fig. 2 left. First 10 shape components capture **85 %** of variance;
  first 20 capture **90 %**. Per-component variances are released in `code/models/pca_variances.txt`
  specifically so the plot can be reproduced. The summary is wrong here.
- **Generalisation: REPORTED.** Fig. 2 right, 8-fold cross-validation, learn the shape space on
  train, project unseen test registrations and reconstruct: **1.80 mm** mean vertex-to-vertex error
  at 10 components, **1.68 mm** at 20. The summary is wrong here too.
- **Specificity: NOT REPORTED.** Confirmed absent — no sampling from the model, no distance from
  random draws to the nearest training shape, nothing. The summary is right, and this is the one
  that matters for us: specificity is the metric that asks "does a sample from this model look like
  a real spine", which is the entire question for generative augmentation.
- **Registration accuracy: REPORTED.** Table 1, per-vertebra point-to-mesh error. Weighted mean
  **0.24 mm**, SD **0.20 mm** on 1×1×1 mm voxels — sub-voxel. Range C6 0.18 mm to L5 0.29 mm;
  error rises monotonically head-to-tail, i.e. worst exactly at the lumbosacral end we care about.
- **Completion accuracy: REPORTED, and "under 3 mm" is CONFIRMED verbatim.** Masking 1/2/3/4/5
  vertebrae and reconstructing from the rest:
  - C1: **1.61 / 1.65 / 1.68 / 1.72 / 1.75 mm**
  - L5: **2.57 / 2.65 / 2.70 / 2.73 / 2.74 mm**
  Every value is under 3 mm. L5 is ~60 % worse than C1 at every masking depth.

Three adversarial notes on that validation that the abstract does not surface:

1. **The ground truth is the model's own registration, not the CT.** "We measure the vertex to
   vertex distance between the reconstructed vertebrae and the original registration." And those
   registrations were themselves produced by a *PCA-guided* fit constrained to a 10-dimensional
   per-vertebra shape space (Sec. 2.2, Eq. 4) before free-vertex refinement. So the completion
   error is measured against a target that already lives inside a low-dimensional shape space.
   The separate 0.24 mm registration-to-scan error bounds how far that target can be from the real
   bone, so this is not fatal — but the 1.6–2.7 mm is not an error against segmented anatomy.
2. **Whether the mirrored copies leak across folds is not stated.** The PPCA matrix is N × 160,
   where 160 = 80 volumes plus their medial-plane mirrors. The 8-fold split is described as balanced
   on a "junction volume" label (C5–T2 observed). The paper never says whether a subject's mirror
   is held in the same fold as the subject. If it is not, every test subject has its own mirror in
   train and the generalisation and completion numbers are optimistic. **This is not known and the
   paper does not answer it.**
3. **n = 80 subjects, 57 % of the data matrix missing.** Not 160 independent spines. And the
   selection is not neutral: vertebrae carrying metal implants were *manually removed*, and meshes
   were reduced to the largest connected component. The population is therefore implant-free
   VerSe'19, which is already a hospital CT cohort.

## 3. Data — CONFIRMED, with a correction of scale

Summary says "VerSe 2019". Precisely: the **80 annotated training CT volumes** of the MICCAI 2019
VerSe challenge (the challenge also provides 40 unlabelled volumes, which were not used).
Resampled to 1×1×1 mm. Plus **24 artist-created template meshes**, one per vertebra — these are an
input, not learned, and the paper does not say where they came from or release the raw templates
separately.

No subject in the training set shows a full spine; Fig. 1 shows the coverage matrix. The
cervicothoracic junction is described as "critically sparse".

## 4. Code — EXISTS, RUNS ONLY IN A DEAD RUNTIME, AND IS INFERENCE-ONLY

The repository is real, public and reachable. GitLab project id 22851, created 2020-08-20,
**last activity 2021-09-21**, 0 stars, 0 forks, default branch `master`.

Complete file tree (14 entries, verified via the API — this is everything):

```
README.md  Licence.md  Install.md  QuickStart.md  requirements.txt
code/spine_model_demo.py
code/spine_completion_demo.py
code/spine_model_utils.py
code/verse_colors.py
code/models/vertebra_smpl_v10.pkl              (>1 GB)
code/models/vertebra_smpl_v10_metadata.pkl
code/models/vertebra_smpl_v10_ppca_metadata.pkl
code/models/pca_variances.txt
```

**There is no training code and no registration code.** Sections 2.1 and 2.2 of the paper — the
non-rigid template-to-scan registration with the point-to-mesh energies, the Rodrigues rotation
initialisation, the edge-coupling regulariser taken from Bogo et al. 2015 Eq. 8, and the free-form
vertex optimisation — are not in the repository. Neither is the PPCA fit (the paper points at a
third-party implementation, `github.com/shergreen/pyppca`). **You cannot refit this model to
CTSpinoPelvic1K with what is released.** You can only pose and sample the model they fitted to
VerSe'19, and complete a spine you have already registered by some other means.

Runtime, from `Install.md` and `requirements.txt`:

- **Python 2.7.16** (pyenv), end-of-life since January 2020.
- `numpy==1.11.1` (released 2016), `chumpy==0.70`, `opencv-python==4.1.0.25`.
- MPI-IS `psbody-mesh` **v0.1**, available only as precompiled `cp27` wheels for macOS 10.11 and
  manylinux x86_64. **No Windows wheel.** This will not install on the workstation; it needs WSL
  or the grid.
- The SMPL `smpl_webuser` serialization module, which must be downloaded after registering at
  `smpl.is.tue.mpg.de` — i.e. **a second licence in the chain**, and the academic SMPL licence is
  itself non-commercial.

I downloaded the whole release. Actual sizes:

| file | bytes |
|---|---|
| `vertebra_smpl_v10.pkl` | 1,103,309,681 (1.10 GB) |
| `vertebra_smpl_v10_ppca_metadata.pkl` | 729,346,730 (729 MB) |
| `vertebra_smpl_v10_metadata.pkl` | 10,059,284 |
| `pca_variances.txt` | 2,197 |

**1.84 GB of model for a 24-vertebra surface basis.** Loading it needs several GB of RAM, and
`spine_model_utils.load_model_metadata` is `pickle.load(open(fname))` — no `'rb'`, so **Python 2
only**, confirmed in source, not just inferred from `Install.md`.

### 4a. What reading the released source adds

`spine_model_utils.py` and `spine_completion_demo.py` are short enough to read in full, and they
settle three things the paper leaves implicit:

- **A `J_regressor` is present** and `get_bone_joint` regresses one joint per vertebra from that
  vertebra's own vertex block. So the "per-vertebra joint locations" in the candidate summary are
  real, confirmed in code.
- **The PPCA vector is shape + translation and nothing else.** `Y_from_model_mesh` lays out
  381,855 vertex coordinates (= 127,285 vertices) followed by 23 inter-vertebral translation
  triplets, C1 excluded because it has no parent. Its own docstring says *"the ppca was computed
  with the individual vertebrae unposed to the template shape"* — every vertebra is rigidly
  unposed to the mean before the statistics are taken. **Rotation is removed from the model by
  construction, in code, not just omitted from the prior.** This is the hardest confirmation of
  §1(a) available.
  (Minor: 127,285 vertices in the code against 127,294 in the paper. Nine vertices. Not worth
  chasing, but noted rather than smoothed over.)
- **The usable latent dimension is 10, and it is hard-coded.** `proj_ppca` opens with
  `assert(nb_latent == 10)`. The 20-component generalisation number in Fig. 2 is not reachable
  with the released completion code.

### 4b. Independent check of the compactness claim — CONFIRMED

`pca_variances.txt` holds **144** component variances summing to 0.5889. Computing the cumulative
fraction myself:

| components | share of total variance |
|---|---|
| 1 | 25.8 % |
| 5 | 64.1 % |
| **10** | **88.4 %** |
| 11 | 88.9 % |
| **20** | **91.9 %** |
| 50 | 96.4 % |
| 144 | 100 % |

The paper claims 85 % at 10 and 90 % at 20. The released variances give 88.4 % and 91.9 % — the
claim reproduces, and is if anything conservative. This is the one number in the paper I could
check against something outside it, and it holds.

It also exposes the real dimensionality. Components 1–10 are each ≥ 0.0208; component 11 is
0.00298 — **a 7× cliff**. Everything past 10 is residual noise, which is why the demo hard-codes
10. So the generative space is **10 dimensions fitted to 80 subjects**. Sampling it produces
interpolations among 80 spines. For beating a scarcity of 86 transitional subjects, that is not a
source of new anatomy.

## 5. Licence — worse than the summary says

`Licence.md` (note the British spelling; there is no `LICENSE` file, a plain `-/raw/master/LICENSE`
fetch 404s):

> The Spine Model is released under the **CC BY-NC-SA 2.0** licence.
> It is derived data from the Verse19 Challenge Dataset released under the CC BY-SA 2.0 licence.

So it is **NC *and* ShareAlike**, not merely NC. Two consequences:

- The NonCommercial term blocks the 510(k) track outright, as the summary said.
- The **ShareAlike** term is the part the summary missed. Any derivative work — and a corpus of
  synthetic spines generated from this model is on its face a derivative work — would have to be
  released under the same BY-NC-SA licence. That does not merely block commercial use of the model;
  it would attach a viral non-commercial licence to the augmented dataset, and arguably to anything
  distributed with it. Given this project's two-track no-crossing rule, that is a
  contaminate-on-contact risk, not a downstream inconvenience.
**And the release contradicts itself about its own licence.** Every source file carries this header:

```
# Derived work Spine Model, Di Meng, Marilyn Keller, Edmond Boyer, Michael J. Black, Sergi Pujades,
# Copyright © Inria and Max Planck Institute, CC BY-NC v2.0 license, 2019-2020 v1.0
# Based on Verse19 Challenge Dataset, ... CC BY v2.0 license, 2019-2020 v3
```

`CC BY-NC v2.0` — no ShareAlike — against `Licence.md`'s `CC BY-NC-SA 2.0`; and `CC BY v2.0` for
VerSe against `Licence.md`'s `CC BY-SA 2.0`. Two disagreements inside one 14-file repository, never
reconciled in five years and no commit touching them since 2021. The practical effect is that you
cannot rely on the *more permissive* reading: a licence that says two different things is a licence
you have to ask the authors about before shipping anything derived from it, and `README.md` gives
a contact address for exactly that ([e-mail withheld], [e-mail withheld]). Either
reading still carries NonCommercial, so the 510(k) track is blocked under both.

- Separately worth noting, without overclaiming: CC BY-SA 2.0 (VerSe'19) requires derivative works
  to be licensed under the same or a compatible licence. Re-licensing derived data as BY-**NC**-SA
  adds a restriction BY-SA does not permit. Whether the trained model is legally a "derivative work"
  of the data is the open question, and nobody has answered it in public. Flagging it as unresolved
  rather than guessing.

## 6. Downstream gain — NONE, and none by anyone since

The paper measures no downstream task. Its conclusion lists synthetic data generation, 2-D X-ray
registration, and segmentation/identification explicitly as **future work**.

I checked all 10 citing papers (Semantic Scholar, 2026-09-23):

| Year | Venue | Paper |
|---|---|---|
| 2021 | MLMI@MICCAI | Vertebrae Localization, Segmentation and Identification Using a Graph Optimization and an Anatomic Consistency Cycle |
| 2022 | Tomography | Anatomy-Aware Inference of the 3D Standing Spine Posture from 2D Radiographs |
| 2023 | IEEE TBME | 3D Spine Model Reconstruction Based on RGBD Images of Unclothed Back Surface |
| 2023 | Comput. Biol. Med. | BOSS: Bones, Organs and Skin Shape Model |
| 2023 | Medical Image Analysis | Multi-Target Landmark Detection with Incomplete Images via RL and Shape Prior |
| 2023 | ShapeMI@MICCAI | Anatomy Completor: A Multi-class Completion Framework for 3D Anatomy Reconstruction |
| 2023 | MICCAI | Optimizing the 3D Plate Shape for Proximal Humerus Fractures |
| 2024 | MICCAI | AutoSkull: Learning-Based Skull Estimation for Automated Pipelines |
| 2024 | arXiv | SurgPointTransformer: Vertebrae Shape Completion with RGB-D Data |
| 2025 | Computer Assisted Surgery | SurgPointTransformer (journal version) |

None of these measures a segmentation or detection accuracy with and without this model as
augmentation. The uses are as a shape prior for reconstruction or completion, which is the opposite
direction of what we want. **Downstream-gain evidence: zero, six years after release.**

## 7. The "only public whole-spine SSM" premise

Weakly true in 2020, and the authors' own later work supersedes it for our purpose. From the same
two labs:

- **OSSO** (Keller, Zuffi, Black, Pujades, CVPR 2022, arXiv 2204.10129,
  `github.com/MarilynKeller/OSSO`) infers a full skeleton — which **does** include pelvis and rib
  cage — from a body surface, fitted to paired DXA/skin data from UK Biobank. Also
  **non-commercial** ("available for non-commercial scientific research purposes"), also
  **inference-only** in the public release. Better anatomical coverage, same licence wall.
- **BOSS** (Comput. Biol. Med. 2023) extends to bones, organs and skin.

Neither adds intensities and neither adds a transitional vertebra. So the premise "the only public
whole-spine SSM" is stale but the successors do not fix our blockers.

## 8. Against OUR requirement

| Requirement | Verdict |
|---|---|
| labelled spine CT in | **No.** No public code to register the model to a CT. Sec. 2.1–2.2 must be reimplemented. |
| labelled plausible spine CT out | **No.** Surfaces only. No HU, no soft tissue, no cortical/trabecular distinction. A DRR needs attenuation, and a binary surface cast to a DRR is a silhouette, not a radiograph. |
| controllable to a target lordosis/kyphosis | **No.** The paper explicitly declines to model relative rotation, which is exactly where lordosis lives. It gives a Gaussian on inter-vertebral spacing only. |
| controllable to a transitional phenotype | **No.** Fixed 24-part topology and a fixed 23-link chain. L6, T13, a sacralised L5 and a four-lumbar spine are all outside the model's structure, not merely outside its training set. Adding one is a retrain with new artist templates, and the training code is not released. |
| covers the lumbosacral junction | **No.** Stops at L5. The sacrum, the S1 end plate and the pelvis — the entire object of this project — are absent. |
| population-plausible variation | **Unmeasured.** No specificity metric. Compactness and generalisation are reported; neither tells you whether a *draw* from the model is anatomical. |
| licence permits our use | **No.** CC BY-NC-SA 2.0, plus an SMPL registration dependency that is itself non-commercial. |

## 9. Verdict: REJECT

Rejected because it produces no intensities and therefore nothing to render, stops at L5 so it omits
the lumbosacral junction this project exists to study, has a fixed 24-vertebra topology that cannot
represent a transitional variant, models inter-vertebral translation but explicitly not rotation so
it cannot be aimed at a target lordosis, offers a generative space of only 10 effective dimensions
fitted to 80 subjects, was never measured for specificity or for downstream gain by anyone in six
years, ships no training or registration code, runs only under Python 2.7, and carries a
non-commercial licence that the release states two incompatible ways.

Note that no single one of those would be decisive on its own — the licence could be negotiated,
the registration could be rewritten. What makes it a reject is that the two that cannot be
negotiated or rewritten (no intensities, no sacrum) are the two the requirement is built on.

It is not a *bad* paper — the sub-voxel registration, the honest 8-fold cross-validation and the
released variances are better practice than most of this literature. It answers a different
question: given part of a spine, what do the missing vertebrae look like. That is completion, not
synthesis.

**Where it could still be used, if ever:** as a shape *prior* or a sanity check — e.g. "is this
reconstructed T12 within the plausible shape space" — never as a generator. And even that use is
gated by the licence and by the missing registration code.

## 10. What it would cost to run on ~2,900 labelled CTs (if one ignored the verdict)

Not recommended; recorded so the number exists.

- **Reimplement Sec. 2.1–2.2 registration**: 3–5 weeks. Point-to-mesh energies, Rodrigues rotation
  init, Bogo Eq. 8 edge coupling, PCA-guided second pass. None of it is released. The chumpy
  autodiff stack it was written against is dead; a modern PyTorch3D or libigl reimplementation is
  the realistic route and will not reproduce their numbers exactly.
- **Port or containerise the released model**: 1 week. Either a py2.7 + psbody-mesh v0.1 container
  (Linux only — this will not run on the Windows workstation, so it is a WSL or grid job), or
  convert the >1 GB chumpy pickle to plain numpy under py3, which is the better bet.
- **Register 2,900 CTs × 24 vertebrae**: marching cubes + three-stage non-rigid fit per vertebra.
  At roughly 1–3 CPU-minutes per vertebra that is 1,200–3,500 CPU-hours — one to three days on a
  few hundred `reqp` cores, so the compute is not the problem. Essentially no GPU need; a PyTorch
  reimplementation would be GPU-friendly but this is not a GPU-bound task.
- **Retrain to add a 25th part for L6 / T13**: additional artist templates plus a PPCA refit with
  ~86 transitional subjects against a 24-part prior fitted to none. Unbounded; I would not quote it.

**What would go wrong, in the order I expect it.**
1. The **template-to-scan correspondence breaks on exactly the cases we care about.** A sacralised
   L5 or an L6 has no template. The registration will silently fit the nearest ordinary template and
   return a finite, plausible-looking, wrong mesh. This is the project's recurring failure mode and
   this method invites it structurally.
2. **The 1×1×1 mm assumption.** VerSe'19 was resampled to isotropic 1 mm. CTSpinoPelvic1K is
   abdominopelvic CT with anisotropic slice spacing in places; the rotation initialisation
   `r = [-2, 0, 2]` is hard-coded to the VerSe acquisition frame and will be wrong for any other
   orientation convention. Given this project's PIR/RAS history, that is a live trap.
3. **Surfaces do not render.** Even with perfect registrations you still have no volume. Converting
   a surface back to a labelled CT with credible HU is a second project, and it is the one that
   actually determines whether a DRR looks like a radiograph.
4. **Licence contamination** discovered after a corpus has been generated, which is the expensive
   time to discover it.
