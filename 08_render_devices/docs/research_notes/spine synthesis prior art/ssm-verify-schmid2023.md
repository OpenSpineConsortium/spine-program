# Adversarial verification — Schmid 2023 SSIM augmentation

Verified 2026-09-23 against the primary source (PMC10406777, open access, CC BY 4.0) and against
the external dataset's own published baseline. This file corrects `ssm.md` §C1 in two places and
confirms it in the rest. Nothing implemented; evidence only.

Citation as given, checked: Schmid J, Assassi L, Chenes C. *A novel image augmentation based on
statistical shape and intensity models: application to the segmentation of hip bones from CT
images.* Eur Radiol Exp 2023;7:39. DOI 10.1186/s41747-023-00357-6, PMID 37550543, PMC10406777.
All three identifiers resolve to this paper. Licence CC BY 4.0 (the article; there is no code).

---

## 1. Confirmed, verbatim from the paper

| Claim in the candidate summary | Status |
|---|---|
| Degree-3 Bernstein, "m=20 Bernstein coefficients per tetrahedron" | CONFIRMED, exact wording |
| Femur 8,734 vertices / 52,220 tets; hipbone 20,626 / 116,062 | CONFIRMED |
| Modes at 95%: femur 17 SSM / 71 SIM; hipbone 50 SSM / 151 SIM | CONFIRMED |
| Intensity fidelity "An error below 10% was obtained", absolute relative error between CT intensities and the Bernstein encoding | CONFIRMED |
| Constrained sampling b_i in [-2.5*lambda_i, 2.5*lambda_i], sum(b_i^2/lambda_i) <= M from chi-squared | CONFIRMED (note: the paper prints the interval in terms of lambda, not sqrt(lambda); the summary's sqrt is the conventional reading, but the paper as printed says lambda) |
| 232 patients, 112 M / 120 F, mean 74.4 / median 75.4 years; 25% metal artefact; >65% osteophytes; not public (ethics committee) | CONFIRMED |
| Results table: none 0.93 [0.90-0.95] / 8.06 [5.83-11.36]; basic 0.93 [0.90-0.95] / 7.35 [5.48-9.90]; SSIM 0.93 [0.91-0.95] / 7.81 [5.83-10.36]; basic+SSIM 0.95 [0.93-0.96] / 6.16 [4.90-8.08] | CONFIRMED, exact |
| External validation CTPelvic1K, 31 images, Dice 0.95 +/- 0.054, HD 7.0 +/- 5.8 mm | CONFIRMED. The subset is MSD_T10; the model used was an ensemble of the five folds trained with Basic + SSIM |
| Two-sided Mann-Whitney-Wilcoxon, Bonferroni, alpha 0.05 | CONFIRMED |
| 4x V100 SXM2 32 GB, 50 epochs, residual U-Net (MONAI) | CONFIRMED |
| No code released; only MONAI and PyTorch named | CONFIRMED — no code availability statement, no repository, no licence. TetGen *is* named as a third dependency (the summary omitted it; see the licence note in §4) |
| Unconditional as published | CONFIRMED — no conditioning mechanism anywhere in the paper |
| Hip, not spine | CONFIRMED. No spine port exists by these authors or anyone else as of today |

Cross-validation design, additionally confirmed: 4/5 of patients train, 1/5 test (~186/46 per
fold), 10% of the training set held for validation. Four classes (left/right proximal femur,
left/right hipbone). Separate SSIM models per structure, rebuilt per fold from that fold's
training data only — so the augmentation does not leak across folds.

---

## 2. REFUTED — the method does not synthesise a whole volume, and that is good news

The summary says it "generates a FULL CT-LIKE VOLUME". The output *is* a full volume, but not
because the model writes one. The four published steps are:

1. constrained random sampling of a tetrahedral mesh with embedded intensities from the SSIM;
2. selection of **the closest image in the training set** by an affine distance criterion between
   the sampled mesh and that image's mesh;
3. **cleaning** that real image by removing the bone's intensities — via a signed distance map,
   "we replace the intensity of v by the intensity of the exterior point r";
4. TPS + rigid warping of the cleaned image with **painting** of the sampled synthetic intensities.

So an augmented image is **a real host CT, warped, with a synthetic bone painted into a hole left
by the old one**. Two consequences, both material:

**(a) The DRR objection in the candidate summary is wrong.** The summary says soft tissue, bowel
gas and table "are absent, and a DRR is a line integral through all of it". They are not absent —
they are inherited from the host CT. An ordinary Siddon DRR can be cast from a Schmid output with
the existing renderer, no new machinery. This removes the single largest stated obstacle to using
this family for our purpose, and `ssm.md` §"whether an SSIM built on spine CT would render as a
radiograph" should be read with that correction.

**(b) A new objection replaces it, and it is worse.** Because the host is the *nearest* real
training image, every sample is a local perturbation of an existing case. The method is built for
realism, not for reach. For our problem the thin places in the cohort distribution (lordosis,
pelvic incidence, transitional phenotypes) are exactly where there is no nearby host to warp. A
nearest-neighbour-anchored augmenter cannot populate a tail it has no neighbour in.

The authors themselves name the failure mode of the warp: cleaning exists "to reduce the risk that
some intensities of the original structure remain after painting ... especially in the vicinity of
its border, causing some kind of 'ghosting' effect." Ghosting at a bone border is a per-voxel
nuisance in a segmentation task and a visible artefact in a line integral. Nobody has measured it
in projection.

---

## 3. REFUTED — "externally validated" does not mean what it sounds like

Schmid's external number is Dice 0.95 +/- 0.054, HD 7.0 +/- 5.8 mm on 31 MSD_T10 volumes.

The dataset's own published baseline (Liu P, Han H, Du Y, et al. *Deep learning to segment pelvic
bones: large-scale CT datasets and baseline models.* Int J CARS 2021;16:749-756. DOI
10.1007/s11548-021-02363-8, PMID 33864189, arXiv 2012.08721) reports, on **the same 31 MSD_T10
test volumes**, nnU-Net at **Dice 0.987, HD 3.11 voxels**, with per-class Dice left hip 0.989,
right hip 0.991, sacrum 0.984, lumbar spine 0.984.

Stated fairly: these are not like for like. Liu's nnU-Net was trained on CTPelvic1K including 93
MSD_T10 volumes, so it is in-domain; Schmid's model never saw the dataset, so it is a genuine
cross-dataset transfer, and a 0.95 transfer is respectable. But the comparison still matters,
because of what it says about the baseline the gain was measured against:

- the downstream experiment used a plain residual U-Net, and the authors state "we did not attempt
  to optimize the segmentation approach (type of model architecture, training parameters, etc.)";
- they did **not** compare against nnU-Net anywhere;
- nnU-Net's own default augmentation is substantial (elastic, scaling, rotation, gamma, noise,
  mirroring) and is part of what gets it to 0.987 on this anatomy.

So the headline "+0.02 Dice from SSIM augmentation" was obtained by moving an unoptimised U-Net
from 0.93 to 0.95, on anatomy where a self-configuring off-the-shelf pipeline reaches 0.987. The
demonstrated gain does not survive contact with a strong baseline, and nothing in the paper shows
it would add anything on top of one. **This is the most important finding in this verification.**

---

## 4. Confirmed and sharpened — the adversarial reading of the downstream result

The summary's adversarial note is right and the paper is more explicit than the summary:
"statistical significance on both DSC and HD metrics was only observed with the fully augmented
approach Basic + SSIM." So **SSIM alone is not significantly better than no augmentation on either
metric**, and it is numerically worse than basic augmentation on Hausdorff (7.81 vs 7.35 mm). The
two p-values printed are for basic vs no-aug on HD (p = 0.0004) and Basic+SSIM vs SSIM on HD
(p < 0.0001).

Minor discrepancy, unresolved: the Results prose gives the no-augmentation HD median as 8.6 mm
while the table gives 8.06 mm. Not load-bearing; noted so nobody re-derives it and thinks they
have found something.

**Licence gap the summary missed.** TetGen is named in the paper and is not MONAI or PyTorch.
TetGen 1.5.0-1.6.0 is **AGPLv3**; 1.4.3 is MIT with a non-commercial clause. Neither is a blocker
for offline data generation we never distribute or serve over a network, and the generated volumes
are not derivative works of the mesher — but given the commercialisation track, use a permissive
mesher (fTetWild, MPL-2.0) rather than inheriting an AGPL dependency by default.

**Also unstated in the paper: how the label of the augmented image is produced.** There is no
sentence describing mask generation, rasterisation, or ground truth for the synthetic images. The
obvious reading is that the sampled tetrahedral mesh *is* the structure, so rasterising it gives
the mask for free — but that is our inference, not the paper's statement. The training obviously
required labels, so labels exist; the mechanism is simply not written down. Say so plainly rather
than cite the paper for it.

---

## 5. Adjacent check — has anyone cast a DRR from an SSIM?

Yes, once, and it does not help. Oh J, Koo S. *Fast digitally reconstructed radiograph generation
using particle-based statistical shape and intensity model.* J Med Imaging 2024;11(3):033503.
DOI 10.1117/1.JMI.11.3.033503, PMC11192206. It renders a DRR directly from a particle-based SSIM,
0.245 s vs 3.10 s for Siddon and 174.8 s for tetrahedral projection (12.6x and ~600x). But it was
validated on **the Stanford dragon with sine-function intensities** — RMSE 0.0136 +/- 0.0040, PSNR
37.59 +/- 2.46 dB, SSI 0.9918 +/- 0.0049 against Siddon as reference — with no patient CT, no bone
density, bone only with no soft tissue, no labels, and no code. It is a speed result for a
renderer, not evidence that an SSIM sample of real anatomy projects like a radiograph. The open
question in `ssm.md` stands: **nobody has cast a DRR from a shape-and-intensity sample of real
anatomy and shown the frame looks like a radiograph.** For Schmid specifically the question is
cheaper than it looked, because the host CT carries the soft tissue (§2a).

---

## 6. Verdict against our requirement

ADAPT, narrowly, and not for the reason the project wants a method.

| our requirement | Schmid 2023 |
|---|---|
| in: labelled CT | met; and our ~2,900 is 12x his 232 |
| out: new volume with aligned label | met, uniquely in this family, mechanism as in §2 |
| renderable as a radiograph | plausible and untested; soft tissue is inherited, ghosting unmeasured |
| conditional control (target lordosis / kyphosis / PI) | **not met**, no mechanism exists in the paper |
| transitional phenotype (L6, T13, sacralised L5) | **not met and not reachable** — a PDM is a fixed-length correspondence vector; an L6 spine has no correspondence with an L5 spine at the junction |
| population-plausible tails | **not met** — nearest-host anchoring is a local perturbation, and the tails have no near host |

It fails the two requirements that motivated the search. It cannot touch the 86-subject
transitional scarcity, and it cannot be asked for a target lordosis. What it can be is a bounded,
label-safe augmenter of ordinary vertebral shape and grey-level variation, whose only measured
benefit is +0.02 Dice against a baseline that off-the-shelf nnU-Net beats by 0.04. If it is
adopted, it should be adopted as that and described as that.

### The cheap decisive tests, in order, before any porting

1. **Two vertebrae, one warp.** Schmid's four bones are far apart and warped independently.
   Vertebrae are stacked and articulated. Independent per-vertebra TPS will interpenetrate or open
   gaps at the disc space. Test on two adjacent levels in one case before anything else — this is
   the structural risk, and it is not mentioned anywhere in the paper because hips do not have it.
2. **Render one.** Cast a Siddon DRR from a single hybrid volume and look at the frame, for
   ghosting at the painted border and for the soft-tissue halo left where the old bone was cleaned
   by nearest-exterior-intensity extrapolation.
3. **Only then** ask whether a 0.93-to-0.95 result on hip segmentation says anything about naming
   a vertebra from one rendered frame. It does not, yet; that transfer is unevidenced.

### What it would take on ~2,900 labelled CTs

- **Correspondence is the whole cost.** One reference vertebra mesh non-rigidly registered to every
  labelled vertebra: ~2,900 x ~20 levels = ~50,000-60,000 registrations. At 1-2 min each that is
  ~1,000-2,000 CPU-hours — a week of grid wall-clock on `reqp`, not a GPU problem.
- **The SIM does not fit in memory the naive way.** At Schmid's density a vertebra is ~20,000 tets
  = 400,000 coefficients. Per level across 2,900 subjects that is ~4.6 GB as float32 — fine. A
  single whole-spine joint SIM is ~24x that, ~110 GB, and a plain PCA on it will not run. Per-level
  models, or a Gram-matrix / randomised PCA, are required. This is the concrete scaling trap and it
  is invisible at n=232.
- **Output storage.** An abdominopelvic volume is ~200 MB. 5,000 augmented volumes is ~1 TB —
  fits on the 20 TB CephFS at `/rs/rs_grp_oschome/go2432/`, does not fit in home.
- **Work:** 3-6 weeks to a first rendered sample, assuming the articulation test in (1) passes.
  Add conditional control on top of that — the published routes are PLS regression or ANAT-SSM —
  and it is longer, on a component nobody has validated for the spine.
- **What goes wrong:** articulated interpenetration at the disc (most likely); ghosting visible in
  projection; correspondence failure on exactly the anomalous cases we care about, because a
  reference vertebra mesh registered to a transitional level is the one registration with no right
  answer; and the whole effort buying a gain that a properly configured baseline already has.
