# Adversarial verification — Statistical Interspace Models (SIMs)

Candidate under test: Castro-Mateos I, Pozo JM, Pereañez M, Lekadir K, Lazary A, Frangi AF.
"Statistical Interspace Models (SIMs): Application to Robust 3D Spine Segmentation."
*IEEE Trans Med Imaging* 2015;34(8):1663–1675.

Verified 2026-09-23. Verdict: **REJECT** for our requirement (labelled spine CT in → new
labelled, renderable spine CT out). Keep one idea from it; do not adopt the method.

---

## 0. Bibliographic ambiguity — RESOLVED

The candidate summary carried two DOIs and could not choose. Both exist and they are
different objects:

| DOI | What it actually is |
|---|---|
| `10.1109/TMI.2015.2443912` | **the SIMs paper**, TMI 34(8):1663–1675, PMID 26080379 |
| `10.1109/TMI.2015.2456376` | the *guest editorial* for that issue's spine special section, TMI 34(8):1625–1626, PMID 26465019 |

Use `10.1109/TMI.2015.2443912`. PMID 26080379. 70 citations (Semantic Scholar), 61
(OpenAlex), as of 2026-09-23.

## 1. How the full text was obtained (and what that limits)

IEEE Xplore is closed; OpenAlex reports `oa_status: closed`, `any_repository_has_fulltext:
false`; the White Rose record (eprint 90968) and the Manchester Research Explorer record
carry metadata only, no file.

The full text used here is the first author's PhD thesis, which is open access under
CC BY-NC-ND 2.5:

- Castro Mateos I. *Statistical anatomical modelling for efficient and personalised spine
  biomechanical models.* PhD thesis, University of Sheffield, 2016.
  https://etheses.whiterose.ac.uk/id/eprint/13802/
  (supervisors Frangi, Taylor, Pozo Soler; EThOS uk.bl.ethos.692445)

Thesis Chapter 4 states at p. 47: *"This chapter was adapted from the publication of the
author of this thesis et al. [109]"*, and reference [109] is the TMI 2015 SIMs paper. The
chapter carries the same three datasets, the same model, and numbered result tables.

**What is not known:** I did not see the IEEE-typeset PDF. The tables below are the thesis
tables. They should be the same numbers, but a table could have been re-run or re-typeset
between the June 2015 journal version and the August 2016 thesis, and I cannot rule that
out. Every number below is cited to the thesis, not to TMI.

---

## 2. Point-by-point against the candidate summary

### 2.1 "Generates: a model of the INTERSPACE … Not a generator in itself; a constraint" — **CONFIRMED, and stronger than stated**

The SIM is built from the relative position vector **d** between a landmark `s_d` on one
object and its nearest facing landmark on the neighbouring object. **d** is split as
`d = ‖d‖ · d̂`, mapping ℝ³ → ℝ⁺ × S². ℝ⁺ is given its Lie-group/log metric (so the gap
cannot reach zero — the log diverges) and the direction is a tangent-space Gaussian at the
Fréchet mean on S². The statistics stored are the mean and covariance **per point pair**.

There are **no modes of variation across pairs**. It cannot be sampled to produce a new
inter-vertebral configuration. This is not my inference — it is the author's own future
work, thesis §8.3.3, titled *"Statistical interspace model with generation ability"*:

> "The SIM … contains the covariance matrix and the mean values of the relative position
> vectors between pairs of points … A future line of research is to study the possibility of
> creating a model with a similar procedure to that of the SSM. This model will combine the
> information of multiple points and will require the use of a dimensionality reduction
> technique to acquire its possible modes of variation."

So: generation was explicitly listed as **not done**. The summary's "a component, not a
method" is right; the component is a *penalty term*, not a samplable distribution.

For completeness, the thesis is clear about where generation lives in this framework
(§4.4 opening): *"individual SSMs together with an SPM provide a complete set of parameters
to generate instances"* — SSM + statistical pose model generate; SIM only vetoes.

### 2.2 "Validation: segmentation accuracy on spine CT" — **CONFIRMED**, and here are the numbers the summary was missing

Three datasets, all small (thesis §4.6):

| | n | source | split | ground truth |
|---|---|---|---|---|
| D1 healthy lumbar | 30 CT (13 M / 17 F, mean age 40) | National Center for Spinal Disorders, Budapest; EC MySpine project | 25 test / 5 feature-training; SSM+SIM leave-one-out (29 vertebrae per model) | authors, ITK-SNAP |
| D2 pathological lumbar | 10 CT | SpineWeb "DataSet 3", selected for scoliosis; 4 with a fracture, 3 with calcification | all test; models trained on D1 | **authors, ITK-SNAP** (the source had none) |
| D3 thoracolumbar healthy | 15 CT | MICCAI CSI 2014 challenge / SpineWeb "Dataset 2" | organisers' 10 train / 5 test | organisers (train set "corrected" by the authors; test left alone) |

Accuracy, without → with SIM (thesis Tables 4.1–4.3, global/segment columns):

| dataset | mean DSI % | MASD mm | 95-p mm | HD mm |
|---|---|---|---|---|
| D1 lumbar | 93.8 → **94.8** | 0.51 → **0.48** | 1.10 → **1.03** | 4.8 → **4.5** |
| D2 pathological lumbar | 84.4 → **88.2** | 1.44 → **0.98** | 4.2 → **2.65** | 9.9 → **6.2** |
| D3 lumbar | 92.1 → **92.7** | 0.57 → **0.49** | 1.39 → **1.28** | 4.8 → **4.8** |
| D3 thoracic | 89.6 → **89.7** | 0.66 → **0.58** | 1.66 → **1.56** | 4.8 → **4.8** |

Overlap, the headline claim (thesis Table 4.4), mean inter-process overlap per spine
segment, no-SIM → with-SIM:

| | voxels | mm³ |
|---|---|---|
| D1 L1–L5 | 897.2 → **0** | 200.26 → **0** |
| D2 L1–L5 | 2554.9 → **0** | 574.8 → **0** |
| D3 T1–T12 | 530 → **0** | 132.5 → **0** |
| D3 L1–L5 | 0 → 0 | 0 → 0 |

Compute (thesis §4.8.2): C++ / ITK, Xeon E5620 2.40 GHz, 8 GB RAM, Windows 8.1 — **~50 s per
vertebra** to segment, 1 s to initialise all vertebrae after the user clicks the disc
centres. Removing the SIM saves ~1 s/vertebra, so the SIM itself is cheap; the gradient-
descent framework around it is what costs.

### 2.3 Where the summary was too generous — the adversarial findings

**(a) "Completely eliminated the overlap" is partly a tautology, and the authors say the
guarantee does not exist.** Thesis §4.8: *"the SIM does not guaranteed zero overlap
mathematically speaking. However, the likelihood of happening is so small that it never
occurred in the experiments."* The energy being minimised directly penalises small and
negative interspace; reporting that the overlap went to zero on ~50 spines is the constraint
reporting on itself. It is a real and useful engineering result for segmentation. It is not
evidence that the SIM captures the *population distribution* of inter-vertebral geometry,
which is what we would need it for.

**(b) On the only dataset with a genuinely independent held-out split, the SIM buys almost
nothing.** D3 is the MICCAI CSI 2014 challenge with the organisers' split and the
organisers' test ground truth. Thoracic DSI moves 89.6 → 89.7; HD 4.8 → 4.8. The authors
concede it (§4.8): *"the accuracy of the results does not change greatly by the addition of
the SIM when segmenting healthy subjects."* The large gains (D2, +3.8 DSI, MASD −32 %) come
from **n = 10** images with **ground truth the authors drew themselves** because the source
dataset had none, under no blinding.

**(c) No statistical test anywhere in the SIM chapter.** The thesis uses two-sample t-tests
in Chapter 3 and score tests in Chapters 5–6, but the with/without-SIM ablation in Chapter 4
is reported as bare means with 2×SD and no test, no confidence interval, no paired
comparison — although the design is naturally paired (same images, same framework, one
energy toggled).

**(d) Against the field, the method with SIM is mid-table.** Thesis Table 4.6, all on D3:
Hammernik et al. 95 DSI / 0.38 MASD; Korez et al. 95 / 0.37; the authors' own *earlier*
method 93 / 0.55; **proposed method with SIM 91 / 0.55**, HD 4.8. The SIM's honest claim is
tail control (HD, 95-p), not mean accuracy — the authors say so.

**(e) The comparison table changes the training regime.** Table 4.5 (vs. state of the art)
re-trains SSM+SIM leave-one-out *on D2 itself*, not on D1 as in Table 4.2. Two different
protocols, same dataset, and the more favourable one is the one used for the comparison.

**(f) "Far less training data than a joint multi-object SSM" is argued, never measured.**
There is no experiment comparing SIM to a joint multi-object SSM at matched or varying n.
What *is* shown is that a usable SIM was built from 30 (D1) and from 10 (D3) spines. That is
a real small-n demonstration; the comparative claim is not.

**(g) SIM was never independently evaluated.** I checked the obvious route — Yao J, Burns
JE, Forsberg D, Seitel A, Rasoulian A, Abolmaesumi P, Hammernik K, Urschler M, Ibragimov B,
Korez R, Vrtovec T, Castro-Mateos I, et al. "A multi-center milestone study of clinical
vertebral CT segmentation." *Comput Med Imaging Graph* 2016;49:16–28, PMID 26878138, open
at https://escholarship.org/uc/item/5dj0636d. The Sheffield entry there is "Method 5",
which the paper's reference [33] identifies as the **CSI 2014 workshop** method (the
feature-selection ASM of thesis Chapter 3), lumbar only — **not** the SIM. So no third party
has ever scored the SIM.

**(h) No code. No licence. Nothing to run.** The paper and thesis claim no repository.
GitHub search returns nothing for "statistical interspace model"; the group's GIMIAS
platform exists in community mirrors (e.g. `bouncingprimary/GnuGIMIAS`, GPL-3.0) but I found
no SIM plugin in it. The CISTIB download page lists no SIM release. The summary's "None
found" is confirmed. **Reimplementation from the paper is the only path, and the paper's
gradient (thesis eq. 4.25–4.27, with two rotation matrices recomputed every iteration on a
4000-landmark mesh per vertebra) is not a weekend.**

**(i) No downstream-gain measurement of any kind.** Confirmed. Of the ~70 citing works I
listed, none uses the SIM as an augmentation or synthesis component; they cite it as prior
art in segmentation surveys. The summary's "None measured" is correct.

### 2.4 The limitation that kills it for *us*, which the summary did not surface

Two independent, decisive problems, both from the paper's own text.

**The SIM cannot exist at the lumbosacral junction as published, and the authors know it.**
Thesis §4.8.1: *"an SIM is created to model the variations of the space between two
surfaces. Therefore, the external objects in the structure, which are vertebrae T1 and L5 …
may over-segment to external structures that are not considered in the model … A feasible
solution may be to include a part of objects that are outside the structure, vertebrae C6,
S1, to model the interspace."* The model covers T1–L5 only. There is **no sacrum, no pelvis,
no rib**. The terminal vertebra is exactly where it leaks, and the terminal vertebra is
exactly our subject. The fix was proposed, not done, and never published since.

**The SIM's magnitude prior structurally forbids the transitional phenotype we most need.**
The magnitude lives on ℝ⁺ under the log map, and the thesis states the consequence
explicitly: *"the gap between the objects cannot be zero. Thus, two landmarks from different
objects cannot share the same position."* A sacralised L5 with a fused or bridged
transitional articulation has a gap of zero across part of the interface — the log map sends
that to −∞ and the energy will push the surfaces apart. A SIM fitted on ordinary spines
would **actively repel** the anatomy we are trying to synthesise. Separately, an L6 or a
four-lumbar spine changes the *object count and the pairing topology*, and the SIM is built
by propagating a fixed landmark-pair correspondence across the whole training set — so a
transitional case cannot even enter the training set without a separate model per
phenotype, at n ≈ 86 split across four phenotypes.

**And there is no image.** SIM + per-vertebra SSM produce triangulated **meshes**. There is
no intensity, appearance or HU model anywhere in the pipeline. Voxelising the meshes would
give us labels, but a DRR needs attenuation. Our requirement is "realistic enough that a DRR
cast from them looks like a radiograph" — this method produces nothing that can be cast.

---

## 3. Judged against our requirement

| requirement | SIM as published |
|---|---|
| labelled spine CT in | needs **dense point correspondence** across meshes, which the paper does not provide and which is the expensive part; also needs a manual click on every disc centre |
| new labelled plausible volume out | **no** — meshes only, no intensity, no CT, nothing to render |
| controllable (target lordosis / kyphosis / PI / phenotype) | **no** — no conditioning of any kind, and no samplable latent |
| population-plausible variation | unmeasured; the model is a per-pair prior, never validated as a population distribution (no generalisation/specificity/compactness curves anywhere) |
| transitional variants representable | **actively hostile** — zero gap is at −∞ in the magnitude prior; object count/topology is fixed |
| covers the lumbosacral junction | **no** — T1–L5 only, and L5 is the documented failure case |

## 4. Verdict

**REJECT.** It is a segmentation regulariser with no generative mode (the author lists
"generation ability" as future work), no code, no independent evaluation, no downstream
measurement, and a magnitude prior that structurally forbids the fused lumbosacral interface
that defines the phenotype we are short of.

**The one idea worth keeping** (and this was the summary's real insight, correctly placed):
when parts are generated independently, something must make the assembly valid, and a
learned model of the *space between* facing surfaces is a better object than a spring.
If we ever build a per-vertebra generator, we will need that piece. We should not build it
from this paper. The live, generative version of the same idea is Frangi's own later work —
Dou H, Virtanen S, Ravikumar N, Frangi AF, "A Generative Shape Compositional Framework to
Synthesise Populations of Virtual Chimaeras", arXiv:2210.01607, IEEE TNNLS — which
synthesises each part and then uses a graph-convolutional composition network to place the
parts by an affine transform and then deform the nodes *at the interfaces between adjacent
parts*. That is the SIM's job done generatively. **It is cardiac, not spine**, and that gap
has to be stated honestly rather than assumed away. It belongs in the SSM angle's shortlist;
SIM does not.

## 5. If someone insisted on running it on ~2,900 labelled CTs

Not recommended; costed for completeness.

- **Reimplementation:** 6–10 weeks for one competent person. The SIM statistics themselves
  are a fortnight; the surrounding machinery is not. It needs (i) a per-vertebra SSM with
  established dense correspondence, (ii) the B-spline shape instance with the ~5×10×10
  control grid, (iii) the four-energy steepest-descent optimiser with the analytic gradient
  of eq. 4.25–4.27, two reference frames recomputed every iteration. No reference code to
  diff against, and no published output to reproduce and check — which, in this project, is
  precisely the condition under which a finite, plausible, wrong number ships.
- **Correspondence over 2,900 CTs:** the real cost and it is *not* in the paper. Roughly
  2,900 × ~17–24 vertebrae ≈ 50–70 k meshes needing 4,000 corresponding landmarks each.
  Budget a full pipeline (ShapeWorks / Deformetrica) and 2–4 weeks of wall-clock CPU, plus a
  human pass, before a single SIM statistic can be computed.
- **GPU hours: zero.** Nothing here is a neural network. It is CPU, embarrassingly parallel
  per case; at the paper's ~50 s/vertebra on 2010 hardware, a full segmentation pass over
  2,900 cases is ~600–1,000 core-hours, trivial on `reqp`. But we do not need their
  segmentation — we already have labels — so this cost is mostly irrelevant.
- **What goes wrong, in order of likelihood:** (1) correspondence fails or drifts at the
  transitional cases, which are the ones we care about, and the failure is silent; (2) the
  L5 terminal-object leak, documented by the authors, lands exactly on our junction; (3) a
  SIM fitted on our 2,900 will be dominated by ordinary spines and will penalise the 86
  transitional ones as improbable — the model will read our target phenotype as an error;
  (4) at the end of all of it there is still no CT and nothing to render, so the DRR
  requirement is untouched.
