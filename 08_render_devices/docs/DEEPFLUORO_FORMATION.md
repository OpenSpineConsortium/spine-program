# Learning image formation from DeepFluoro, and applying it to the whole spine

Written 2026-09-21. What was asked, what was measured, what the literature settled, and the design
that follows from both. Reproduce every number here with the tools named beside it.

**The proposal.** DeepFluoro pairs 366 real fluoroscopic frames with the CT and the exact pose that
produced each one. So the map from *projected volume* to *what the detector produced* can be fitted
rather than guessed, and then applied to other CTs — whole-spine volumes with per-vertebra masks — to
produce fluoroscopy-realistic training images whose labels are exact by projection. The question was
whether that map can be *learned*, and whether what is learned on a pelvis transfers to a thoracic or
cervical spine.

**The answer, in one line.** The map decomposes into a part that is exact and anatomy-agnostic by
construction (geometry, polyenergetic attenuation), a part that is a property of the *device* and can
be **calibrated** from the pairs with a handful of parameters (vignette, heel gradient, receptor
kernel, scatter, noise, display curve), and a per-frame remainder that no published learned model has
turned into a downstream gain. Build the first two; do not learn the third.

---

## 1. The geometry is exact, and it was tested, not read

`tools/deepfluoro_convention.py` scores every candidate convention by reprojecting the 14 shipped 3-D
landmarks into the 14 shipped 2-D ones. One candidate wins at **0.00 px median, 0.00 px p90** over
111 projections; the rest are hundreds of pixels off:

```
p_cam = ext @ inv(cam-to-pelvis-vol) @ p_vol      ext = proj-params/extrinsic, REQUIRED
uv    = K @ p_cam / z                              K focal -5257.7 px kept signed; (col, row)
                                                   rot-180-for-up is NOT applied to the landmark coords
```

The volume is indexed **(z, y, x)** — decided by the segmentation label found at each landmark's index
(6/6 correct that way, 1/6 the other, on two specimens), after a range check on a single landmark had
said (x, y, z) by coincidence. Focal × 0.194 mm = **1020 mm SID**, a CIOS Fusion. The stored image is
transmission-like (bright = more photons), decided by correlating under both signs.

`slurm/deepfluoro_pairs.sh` renders all 366 projections from their own CT at their own pose
(`tools/deepfluoro_render.py`: the repo's water/bone basis and six-energy spectrum, **no detector
physics**), and the landmark reprojection is 0.00 px on every one of the six specimens. One render
failed on a transient torch import race and was redone.

## 2. How much of a real frame the physics already explains — measured on all 366

`tools/deepfluoro_residual_all.py`, corrected NCC floor applied uniformly, border ring eroded:

| specimen | n | NCC median | p10 | explained | 0–1 px | 1–2 | 2–4 | 4–8 | 8–16 | 16–32 | >32 px |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 17-1882 | 111 | 0.894 | 0.835 | 79.9 % | 0.31 | 0.54 | 0.66 | 0.73 | 0.34 | 0.20 | 0.20 |
| 17-1905 | 24 | 0.917 | 0.888 | 84.1 % | 0.19 | 0.47 | 0.68 | 0.78 | 0.43 | 0.18 | 0.47 |
| 18-0725 | 24 | 0.917 | 0.856 | 84.1 % | 0.34 | 0.63 | 0.76 | 0.85 | 0.37 | 0.13 | 0.06 |
| 18-1109 | 104 | 0.844 | 0.739 | 71.2 % | 0.26 | 0.55 | 0.74 | 0.80 | 0.44 | 0.21 | 0.37 |
| 18-2799 | 48 | 0.916 | 0.893 | 83.8 % | 0.19 | 0.38 | 0.50 | 0.59 | 0.36 | 0.24 | 0.56 |
| 18-2800 | 55 | 0.908 | 0.889 | 82.4 % | 0.33 | 0.59 | 0.74 | 0.79 | 0.42 | 0.27 | 0.13 |
| **all** | **366** | **0.899** | **0.804** | **80.9 %** | 0.27 | 0.53 | 0.69 | **0.75** | 0.38 | 0.20 | 0.31 |

Exact geometry plus the repo's attenuation model, with no detector term at all, explains **81 %** of a
real frame's attenuation variance, and the shape of the curve is the same in every specimen: a peak at
the bone scale (4–8 px, r = 0.75), falling below 2 px and above 16 px. What is missing lives at the two
ends.

**The high-frequency end** (`tools/deepfluoro_residual.py`, frame 000, seen not inferred): a red/blue
doublet on every cortical edge — an unsharp-mask halo — plus texture and noise.

**The low-frequency end** (`smooth_decomp.py`): a planar-plus-radial fit `a + b·r² + c·u + d·v` takes a
median 49 % of each frame's smooth residual. The radial coefficient `b` has the **same sign in 89 % of
frames** (corners denser than the DRR predicts): a vignette or flat-field remainder, device-fixed. The
lateral coefficient `c` **reverses sign with `rot-180-for-up`** (−0.019 for rot = 0, +0.011 for
rot = 1): an anode-heel gradient that the flag rotates. What remains after that fit is only weakly
consistent within a specimen (same-rot pairs r = 0.07–0.67) and not at all across specimens — a
per-frame, view-dependent term, in the range where scatter that follows thickness and a per-frame
automatic window would live.

So the residual has three parts, and only the third is not a small parametric field.

## 3. What the literature settled (107 agents, adversarially verified, 2026-09-21)

Full record with citations in the research output; the operative results:

- **No learned formation model has beaten a physics renderer on a real-image downstream task by a
  margin that matters.** Paired, view-conditioned diffusion trained on five DeepFluoro specimens and
- **Paired diffusion on these six specimens** (Rapuri, Ko, Killeen, Taylor, Unberath, arXiv:2606.21414, verified
  2026-09-21 against the paper's Table 1): trained on five, tested on the sixth, precisely matched views —
  landmark error at NCC > 0.60: diffusion 4.40 ± 1.87, real frames 4.89 ± 6.42, physics DRR of the real CT
  7.83 ± 25.67; at NCC > 0.20: diffusion 25.40, real 18.94, DRR 17.92 (**+7.5 mm worse than the DRR**). The
  DRRs with ±2.5° view augmentation were the best arm at every threshold (4.87 / 6.02 / 9.73). On the
  matched single specimen the DRR equalled real-frame training (4.37 vs 4.38). No statement about
  hallucinated anatomy appears in the paper.
- **Where the physics gain comes from**: ~82 % of the 78 → 25 mm real-image improvement is
  polyenergetic multi-material attenuation; learned decomposition ~14 % (mostly removing eight
  catastrophic failures); learned scatter ~4 %, not significant. The authors attribute the remaining
  gap to *vendor post-processing, finite CT resolution under magnification, and reference labels*
  (Unberath et al., IJCARS 2019).
- **Paired pix2pix refinement** reaches SSIM 0.96 from 800 pairs on two patients, was never tested on a
  downstream task, reports image-similarity gains over a conventional renderer on one held-out patient per region, no
  downstream task (full text paywalled; abstract verified), and **hallucinated
  geometry** with too few patients — the failure that would corrupt projected labels. Its authors
  recommend per-region training (RealDRR, Dhont et al., 2020).
- **DeepFluoro's poses are hip-centred**; the one specimen imaged outside the cluster collapsed to
  10 mm / 30 % false negatives / 29 % registration success against 86 % overall (Grupp et al., 2020).
  Anything fitted on these pairs inherits that pose distribution.
- **Neural attenuation fields and Gaussian splatting** learn a per-object *volume* under a monoenergetic
  Beer–Lambert forward model with no detector term: not a transferable formation function.
- **Grafting** vertebrae onto a pelvic volume is unnecessary and argued against: the only component
  shown to transfer across anatomy is the physics, which needs no anatomical continuity; a graft adds a
  seam to acquire tissue already owned unspliced.

Two open questions the record could not close, and which this pipeline will therefore measure rather
than assume: whether a small-receptive-field learned residual transfers across anatomy on one device
(untested anywhere), and whether passing an appearance test predicts downstream detector gain (no
source measured both on the same synthetic set).

## 4. The design, determined by §2 and §3 together

```
f  =  exact geometry                        settled, 0.00 px               anatomy-agnostic
    + polyenergetic attenuation             render_physics_drr             anatomy-agnostic
    + CALIBRATED device terms, fitted leave-one-specimen-out on the 366 pairs:
        radial vignette      b·r²                       1 parameter
        heel gradient        c·u, sign by rot-180       1 parameter
        scatter / SPR        conditioned on water path  fluoro_physics already has it; fit 1–2
        receptor kernel      MTF + unsharp halo         separable, ~6 parameters
        noise                photon budget to match measured grain, NPS shape
        display              monotone LUT / auto-window
    + STRONG domain randomisation around the fitted values
   → applied to CONTINUOUS whole-spine volumes, at poses drawn from the 366 real ones and widened
```

Every calibrated term is a property of the detector or the beam, not of the anatomy, which is the
property the rostral extension needs. Nothing in it can move a label.

**The anatomy source is TotalSegmentator, not VerSe.** VerSe raw (`~/VerSeFusion/data/unified`, 374
CT+mask pairs at ~0.3 × 1.25 mm, LPS) is mostly regional: of 120 masks, 31 contain C2 and **one** runs
from C2 to the lumbar spine; the common spans are L1–L5, T8–L5 and C1–T3. TotalSegmentator's
whole-body CTs are the whole-spine source: **156 of 1939 subjects** carry both `vertebrae_C2` and
`sacrum`, at 1.5 mm isotropic (`~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300`).

## 5. What the calibration measured (2026-09-21, `slurm/deepfluoro_calibrate.sh`)

Nine terms, leave-one-specimen-out, 40 training frames per fold, optimiser in normalised units:

| held out | n | physics | + 9 terms | gain |
|---|---:|---:|---:|---:|
| 17-1882 | 111 | 80.1 % | 86.6 % | +6.4 |
| 17-1905 | 24 | 84.1 % | 87.5 % | +3.5 |
| 18-0725 | 24 | 86.5 % | 83.4 % | −3.1 |
| 18-1109 | 104 | 69.3 % | 77.4 % | +8.0 |
| 18-2799 | 48 | 84.4 % | 87.8 % | +3.4 |
| 18-2800 | 55 | 83.7 % | 86.0 % | +2.3 |
| **AP → lateral** (≤8° → ≥15°, max 36.5°) | 68 | 80.9 % | 85.5 % | **+4.6** |
| lateral → AP | 198 | 80.0 % | 85.0 % | +5.0 |

Median held-out gain **+4.1**. Stable across folds, i.e. properties of the device: receptor blur
σ_r = 0.81 px (spread 0.13), edge-enhancement width σ_u = 3.06 px (0.22), vignette b = −0.133 (0.05),
heel c = +0.045 (0.05), tilt d = −0.036 (0.03). **Unstable**: the scatter fraction and width (σ_s
4.9–60 px across folds) — poorly identified at 384², and the cause of the over-smoothing below. **At
its bound in every fold**: the bone-path scale kb = 2.5 — the bone/spectrum model itself is off, not
the bound; a physical reparameterisation (kVp) is the fix, not a wider bound.

**The ceiling** (`tools/deepfluoro_noise_floor.py`, 120 frames): 0.3–0.5 % of a real frame's
attenuation variance is stochastic, so no deterministic model can exceed **99.5 %**. Physics alone
80.5 %; nine terms 85.4 %; with a **per-frame quadratic surface** (window, scatter pedestal, heel — twelve
coefficients, no image content) physics 92.3 %, calibrated **93.9 %** (p10 88.0 %). After that the bands at
and below 8 px are at the floor; what remains is at 8 px and coarser, overwhelmingly above 16 px. There is
nothing local left for a network to learn; a regional denoiser would have 0.4 % of the variance to work on.

**The bowel question** (`tools/deepfluoro_show_calibrated.py`, measured inside the exposed field after the
collimator ring bled into a first attempt): the raw DRR carries **1.03–1.05×** the real frame's 8–32 px
energy at r = 0.92–0.95. The bowel in the DRR is right. What makes a real frame read as bone is crisp
cortical edges and grain, which the calibrated frames have. The calibrated model is **over-smooth** at
8–32 px (0.2–0.3× real): the free scatter blur.

**Emitting whole-spine frames** (`tools/spine_project.py --calibration`): the nine terms with a quantum
draw, the scanner table stripped (largest connected body component above −300 HU), the rotation flag
honoured on frame and boxes. s0224 under a real AP pose: T9→L5, every box projected; under the most
lateral real pose (36.5°): T10→L5.

### The open items, taken (2026-09-21 02:11, `slurm/deepfluoro_calibrate_v2.sh`, four six-minute fits)

| fit | held-out gain, median (min, max) | what moved |
|---|---:|---|
| nine terms as first fitted | +4.1 (−3.1, +8.0) | σ_s 5–60 px across folds; kb at 2.5 |
| **scatter width boxed to 6–16 px** | **+4.3 (−3.1, +8.2)** | σ_s **15.8 px, spread 0.4**; every term stable; kb at 2.5 |
| scatter dropped (s = 0) | +4.1 (−3.3, +9.3) | receptor blur destabilises (0.43–1.37 px) — scatter carries something real |
| kb opened to 6 | +3.5 (−3.9, +8.5) | kb runs to 3.0 (2.7–3.5), scatter unstable again; held-out gain FALLS |

The scatter-constrained fit is the calibration now (`calibration_best.json`): the only one in which all
nine terms are stable across folds and the held-out gain is highest. kb stays at its bound of 2.5 on
purpose — letting it run trades held-out gain for a term that then varies by 0.7 across specimens. The
bone/spectrum model is still off (the bound is active), but a wider box is not the fix; a physical
reparameterisation remains open and is no longer first.

**Regressing the terms on view angle** (Greg's request; `--angle-bins`): nine terms fitted inside
|lateral tilt| bins of ≤8° (n=198), 8–15° (100) and ≥15° (68), scored on each bin's remaining frames
against the global terms on the same frames: **+0.0, −0.2, −0.4 points**. Per-angle terms do not beat
global ones anywhere in the measured range. The only term with a large excursion across bins is the
scatter width (−85 px over 36.5°), which is the unidentified term, not a trend; the identified terms move
by less than their fold spread (σ_r +0.15 px, b +0.31, c +0.13 over the full range). So the terms are not
regressed on angle; the calibration is applied unchanged, which is what the AP→lateral fold (+4.6) said.

**The photon budget** (`tools/deepfluoro_photons.py`, 56 frames): the count at which the calibrated model,
with its quantum draw after scatter and before receptor blur, reproduces the real frame's fine-band
variance in its flattest regions — median **2,934 per 0.78 mm pixel**, IQR 1,593–3,828, p10–p90
788–4,767; by specimen 1,221 (18-2799) to 3,821 (17-1882). The assumed 4,000 sat at the 79th percentile
and the builder's first range, 1,500–8,000, put half its draws above anything the device produces. The
builder now draws on the fitted p10–p90. The draw itself had been in the wrong place: `spine_project.py`
and the builder drew white noise on the finished frame; `forward_noisy` puts it where the detector
counts it (variance scales 4.13, 4.03 per fourfold count; lag-1 autocorrelation 0.66, not 0).

**The first synthetic set, looked at before a detector trained on it** (02:20). It was wrong two ways,
neither visible in any number the build printed. A pixel that counted zero photons became an attenuation
of 13.8 against anatomy at 2–5, and a percentile window on that squeezed whole frames into featureless
white or black; the transmission is now clipped at the same 2 % of the exposed range that bounds a real
frame in `load_pair` (`forward_noisy(..., floor=0.02)`). And the *aggressive* randomisation tier built
for the film detector put grid stripes on 45 % of frames and blotches on most, burying the calibrated
physics it was meant to complement. Rendered again with the floor and no randomisation, the frames read
as fluoroscopy beside the real ones: bone bright, fine grain, crisp cortex, the sacrum box on the sacrum.
Two more mismatches fixed on the same look: the synthetic window (inner percentiles of the exposed
region) sat a hundred grey levels brighter than the real writer's (1st–99th of the whole frame) — both
now use the real rule; and every real test frame is pelvis-centred with a sacrum while the synthetic set
had one in 39 % — targets re-weighted to L3/L4/L5/L5/sacrum×3.

The randomisation tier is therefore an **arm**, not an assumption. Three chains, one calibration
(`calibration_best.json`), one photon range (773–4,767), same 48 subjects × 14 poses, same real test:

| arm | randomisation | dataset root / run name |
|---|---|---|
| none | the calibrated physics alone | `~/model_night/anchor_none`, `anchor_none` |
| mild | plausible window, gamma, bias field and blur on half the frames | `anchor_mild` |
| strong | the aggressive film-detector tier on 80 % | `anchor_strong` |

Result per arm in `eval_anchor_<arm>.json`: sacrum recall, anchor-called rate, false sacra per frame,
vertebra-region hit, at confidences 0.05/0.10/0.25/0.40, on 17-1882's 111 real frames.

### The first per-vertebra recall on real fluoroscopy (2026-09-21, 02:36–03:20)

YOLO11m from COCO weights, 40 epochs, on 597 calibrated synthetic frames (48 subjects × 14 real poses, no
randomisation; synthetic-validation mAP50 0.91–0.97), one model per held-out specimen, tested on that
specimen's real frames against the shipped 2-D segmentation. Sacrum recall at confidence 0.05 (a called
sacrum box with its centre in, or IoU ≥ 0.3 with, the truth box):

| held-out specimen | real frames | sacrum recall | anchor called | false sacra / frame | vertebra-region hit |
|---|---:|---:|---:|---:|---:|
| 17-1882 (seeds 0 / 1 / 2) | 111 | 51.4 / **77.5** / 56.8 % | 98–100 % | 0.65–0.72 | 88–89 % |
| 17-1905 | 23 | 47.8 % | 95.8 % | 0.96 | 80.0 % |
| 18-0725 | 24 | 95.8 % | 100 % | 0.33 | 70.8 % |
| 18-1109 | 104 | 96.2 % | 98.1 % | 0.40 | 95.2 % |
| 18-2799 | 48 | 77.1 % | 93.8 % | 0.44 | 56.2 % |
| 18-2800 | 55 | 74.5 % | 100 % | 0.87 | 92.7 % |
| **pooled** (seeds averaged within a fold) | **365** | **76.9 %** | 98.2 % | 0.64 | 82.6 % |

Single-seed arms on 17-1882, same test: round 1 (whole-frame window) none 47.7, mild 55.0, strong 47.7;
round 2 (central-ROI window) mild 30.6, strong 53.2, none on 142 subjects 47.7, mild on 142 subjects 58.6.

**What this says.** 76.9 % over six specimens is the honest first number, and it is nowhere near
counting-grade. **Three seeds of one dataset span 51.4–77.5 %** — 26 points from the seed alone — so no
single-seed difference between arms is a difference: not the window rule, not mild randomisation, not the
aggressive tier, not threefold data. Remedies can only be ranked with seeds averaged and specimens as
folds; `tools/deepfluoro_anchor_report.py` prints the spread beside every mean.

**The trap the drawn calls exposed.** The first scores were ~40 % (37.8 none, 41.4 mild, 9.0 strong; 36.9 /
57.7 / 45.0 over seeds). `--dump` drew the calls on the real frames, and in some of them the truth boxes sat
at the *bottom* of the field: **160 of the 366 real frames are stored upside down** (`rot-180-for-up`; all
24 of 17-1905, 39 of 17-1882's 111). The synthetic frames are turned up when the borrowed pose carries
the flag; the real test frames had been written as stored. A third of 17-1882's test was inverted pelves
the detector had never seen. `write_real` now rotates frame and segmentation together; `--real-only`
rewrites a root's test set; `EVAL_ONLY=1` re-scores trained weights on it; `slurm/deepfluoro_anchor_rescore.sh`
did both for every arm. No printed number showed any of this.

**Where the rest goes.** In the corrected dump the sacrum is found in the upright anteroposterior frames.
The oblique frames, where the lumbosacral region saturates, collect clusters of low-confidence vertebra
calls on the saturated region — the renderer has no automatic exposure control, so the oblique synthetic
views were slabs too, and "white slab = vertebra" was learned.

**Domain gaps to state, not to explain away.** DeepFluoro's specimens are cadaveric pelves with air
around them; the synthetic set is living abdomens that fill the field. The test specimens' vertebrae are
one merged class, so only the sacrum has a per-structure truth. The renderer has no exposure control.

### The learned arms (2026-09-21, requested: "try learning it, I don't mind risking hallucination")

RealDRR (Dhont et al., Radiother Oncol 2020; full text and supplement on hand): ray tracer → conditional
GAN (enlarged pix2pix generator, full-image discriminator, loss = GAN + 50·L1), 800 (DRR, CBCT
projection) pairs of two patients, 200 epochs; on a third patient SSIM 0.96 (pelvis) / 0.93 (cranium),
template-matching error 1.0–1.5 mm against 1.6–3.3 (DeepDRR) and 41–49 (raw ray tracer) on the pelvis.
Supplement Appendix B: trained on ONE patient the generator moved anatomical landmarks 1.8–2.1 mm ("learns
to correct the anatomical differences between the planning CT and CBCT"); with two or more, < 1 mm. That
is the precedent, and the quantified risk, for learning the correction from pairs and applying it to
new CTs.

Three arms, each six folds × three seeds against the v2 TotalSegmentator arm (`slurm/deepfluoro_refine_arm.sh`):

| arm | what | where |
|---|---|---|
| rffull | RealDRR's recipe on the five training specimens' (calibrated render, real) pairs, applied to the TS renders | `tools/deepfluoro_refine.py train/apply`, `anchor_rffull_v2_<spec>` |
| rfhp | the same generator allowed only the σ ≥ 8 px high-pass of its residual: sharpen and texture, never re-window | `anchor_rfhp_v2_<spec>` |
| fda | Fourier Domain Adaptation: the lowest amplitude band (7 bins at 384 px) of a random real training frame, phase kept, training-free | `deepfluoro_anchor.fda_swap`, `anchor_fda_v2_<spec>` |

The refiner pairs (`build --refiner-pairs`) are written with the held-out fold's terms and never include
the held-out specimen; the FDA pool is checked for it and refuses. Refiner triplets (render | refined |
real | residual) are dumped per fold to `~/model_night/refiners/dump_<mode>_<spec>.png` and must be
looked at before the numbers are believed.

What the arms can and cannot say. The pairs control already puts renders of the test population at
96–98 %, so on that population a refiner has two points to add. Applied to living-abdomen renders, a
refiner trained on cadaveric pairs may move the appearance toward the test population — that is population
transfer, not projection fidelity, and it is the confound the reviewer named; the FDA arm, which can only
move the low band, is the control that separates the two.

### Where the render is wrong, by region (2026-09-21, `slurm/deepfluoro_residual_regions.sh`, job 40405687)

> **Correction (2026-09-21 15:20 EDT).** The thin-bone deficit below (+62/+81/+48 grey at 0.5–2 cm of bone) and the
> cortical-edge bias of +8.7 grey were measurement artifacts. The bone mask was intersected with the exposed field, so
> wherever bone crossed the collimator border the border was counted as a bone edge, and at that border the real frame
> falls off through the penumbra while the render stops at a hard edge. Measured 23 px inside the field
> (`tools/deepfluoro_edge_bias.py --erode 23`, linear reading, rebuilt roots), the thin-bone bias is +5.8/+3.0/+0.8
> grey; with the ring reported as its own region (`tools/deepfluoro_residual_regions.py --erode 23`), the ring is
> 22.5 % of the field and 68.6 % of the residual energy (bias +23.3 grey), and inside it cortical edges hold 3.4 %
> (bias −7.4 under a whole-field match). The refuted remedies below were chasing the artifact. What remains real: the
> log-image finding and the collimator border.


The coloured residual of one specimen (Figure 3 of the manuscript: calibrated render | real frame | refined
render, each render's signed residual on its outer side, red where the render is too dark, blue where it is
too bright) shows the same pattern on every row: blue inside the pelvic ring, red at the flanks and over the
iliac wings, red along cortical edges. Measured over all 366 held-out frames of the six folds in the display
domain (the 8-bit frames the detector sees), the field partitioned from each pair's own ray maps into
truncated rays, a ±2 px cortical-edge band (any ray through ≥ 3 mm of bone), bone interior, soft tissue the
closed bone ring encloses, and soft tissue outside it (`residual_regions.json`):

| region | area | share of residual energy | bias, grey (+ = render too dark) | rms, grey |
|---|---|---|---|---|
| cortical edge | 7.1 % | 12.5 % | +8.7 (p10–p90 −1.4 to +19.8) | 56 |
| bone interior | 45.4 % | 34.1 % | −2.0 | 35 |
| enclosed soft tissue | 4.2 % | 1.7 % | −7.2 | 23 |
| outside soft tissue (flanks) | 32.7 % | 50.4 % | +3.8 | 53 |
| truncated rays | 0.0 % | 0.0 % | — | — |

Calibrated render, per-frame linear match; explained 69.3 %, rms 41.5 grey. Three readings:

1. **A smooth field is not the problem.** A per-frame quadratic gain-and-offset field (twelve coefficients:
   window, scatter pedestal, heel, vignette) removes a median 22 % of the residual energy, in the display
   domain, for the calibrated render and 22 % for the refined one. The rest is content and grain.
2. **The one systematic, learnable error is at the cortical edge**: the render's edges are too dark by a
   median 8.7 grey (+7.0 after the field), on 7 % of the field carrying 12.5 % of the energy. That is the
   "hypointense bone" a reader sees, and it is what a display unsharp mask does on the device. The
   high-pass refiner (rfhp) is the arm that addressed it and the one that gained most (+11 detection points).
3. **The flanks carry half the residual energy on a third of the field, with a small bias** (+3.8, +1.6 after
   the field) and a large rms (53): texture and soft-tissue position, not a tone error. The CT holds tissue to
   the field edge on the anteroposterior frames (`water_cm` ≈ 15 cm at the edge; `tmp/water_check.py`), so
   this is not truncation; it is the cadaver's soft tissue lying differently on the C-arm table than in the
   scanner, and grain. Nothing fed the CT can know it. The enclosed soft tissue where bowel gas moved is
   4 % of the field and under 2 % of the energy; on anteroposterior frames the inlet is mostly sacrum and is
   counted as bone interior.

The refiner (rffull) leaves every one of these numbers where it found them (edge +9.0, flanks +1.9, interior
−0.3; explained 68.1 %) and adds a bias of its own inside the ring (−11.2). So a region-weighted or
attention loss would spend its capacity on the flanks and the inlet, exactly the regions whose truth is not
in the input; the region where the truth is in the CT and the error is systematic is the edge band, and the
cheapest fix for it is a two-parameter display sharpening term fitted on the pairs, not a network.

### The thin-bone deficit, chased to the conversion (2026-09-21 afternoon)

> **Correction (2026-09-21 15:20 EDT).** The thin-bone deficit below (+62/+81/+48 grey at 0.5–2 cm of bone) and the
> cortical-edge bias of +8.7 grey were measurement artifacts. The bone mask was intersected with the exposed field, so
> wherever bone crossed the collimator border the border was counted as a bone edge, and at that border the real frame
> falls off through the penumbra while the render stops at a hard edge. Measured 23 px inside the field
> (`tools/deepfluoro_edge_bias.py --erode 23`, linear reading, rebuilt roots), the thin-bone bias is +5.8/+3.0/+0.8
> grey; with the ring reported as its own region (`tools/deepfluoro_residual_regions.py --erode 23`), the ring is
> 22.5 % of the field and 68.6 % of the residual energy (bias +23.3 grey), and inside it cortical edges hold 3.4 %
> (bias −7.4 under a whole-field match). The refuted remedies below were chasing the artifact. What remains real: the
> log-image finding and the collimator border.


Three remedies for the thin-bone edge bias were measured on held-out frames in the attenuation domain
(`tools/deepfluoro_bandgain.py`, `tools/deepfluoro_pedestal.py`, `tools/deepfluoro_edge_bias.py`):

| remedy | what it is | held-out field variance | thin-bone edge bias |
|---|---|---|---|
| four-band linear enhancement, σ 1/2/4/8 px, fitted per frame / pooled / on edges only | the device's small-structure boost as a linear filter | 87.3 → 87.1–87.2 % | unchanged |
| wide scatter pedestal p·⟨T⟩ before the log | scatter the 16 px kernel cannot represent | 85.1 → 74.7 % at p = 0.4, monotone down | worse |
| display exponent a^γ on the model attenuation | a display curve | 85.1 → **88.3 % at γ = 1.8**, per-fold optimum 1.6–3.0 | 1.5–2 cm bin +10.6 → +7.2; thick-bone bias +6.4 → −3.9 |

The first two are refuted. The third works, and a power of two on a log image is not a device term anyone
builds; it is the signature of a wrong conversion. So the conversion was tested directly
(`tools/deepfluoro_transfer.py`, `transfer.json`, `transfer.png`): the stored DeepFluoro intensity against
the model attenuation, binned by quantile on every frame, fitted by three forms. **The stored intensity is a
nearly straight, slightly concave decreasing function of the model attenuation.** The transmission form
`A exp(−B a) + C` fits only with B = 0.15 (transmission would give B = 1); the power form wins on 78 % of
frames under the calibrated terms with γ = 0.98 and on 97 % under the physics-only terms with γ = 1.27. The
device stores a log-compressed display image, and `raw_to_atten`'s −log of it was a log of a log. Every
calibration, the photon budget, every real test frame the detectors were scored on, and the edge-bias
numbers above were made against that bent target; the exponent of two lifting held-out variance by three
points was the symptom.

What changed in the code: `deepfluoro_calibrate.CONVERSION` (`"log"`, the old reading, default so that every
earlier number reproduces; `"linear"`, (p98 − r)/(p98 − p2)); `real_to_atten` is what `load_pair` and the
anchor builder's real-frame writer and evaluator now call; the synthetic side still takes −log of its
transmission; `DF_CONVERSION=linear` in the environment switches every tool, `--conversion` on the
calibration switches the fit and is recorded in its JSON. `slurm/deepfluoro_linear.sh` refits the terms and
the photons under the linear reading, rebuilds the six pairs roots under `/rs/rs_grp_oschome/go2432/
model_night/anchor_pairs_lin_<spec>`, and re-measures the region residual, the edge bias, the exponent sweep
(which should now centre on one) and the transfer curve; results land as `*_linear.json`. Until it finishes,
the thin-bone finding above stands only under the old reading.

Two further sets Greg supplied were checked and are not usable here: the Goswami 2020 IOERT set is a pig
lower limb with an applicator on an Elekta Synergy kV imager (no spine); the Liu 2019 Medical Physics set is
megavoltage portal images against bone DRRs (not kilovoltage fluoroscopy). The Ljubljana gold standard
(Tomaževič 2002) is one cadaveric L1–L5 segment in a water tube on a Trixell flat panel with exact
geometry and an 8-bit CT: a device-transfer test for the terms, not an appearance target.

### Still open

1. Physical reparameterisation of the bone term (kVp / effective energy) — the bound is active, and
   opening it is not the answer.
2. Carry the per-frame quadratic into generation as a randomised smooth field (strong DR randomises a
   version of it already).
3. Beyond 36.5° from anteroposterior there are no real frames; a true lateral remains unmeasured.

## 6. Validation, in the order it is being run

1. **Held-out-specimen agreement.** Does calibration raise the 81 % explained variance, and by how
   much, on the specimen it was not fitted on? (`deepfluoro_residual_all.py` on calibrated renders.)
2. **Anatomy-matched discriminator, reported but not trusted.** Identical pose rendered from the same
   CT, so real and synthetic are anatomy- and geometry-matched; a *patch* discriminator with a
   receptive field of tens of pixels (a full-image one is what would let a generator invent structure);
   leave-one-specimen-out; pass = held-out AUC whose CI includes 0.5. The literature has no accepted
   threshold and no evidence that passing predicts downstream gain, so this is a diagnostic, not a
   gate.
3. **The test that matters.** A detector trained on calibrated synthetic frames, scored for
   **sacrum / L5 recall on the held-out real specimen** — the anchor detection that failed at 97 %
   refusal in the C2 arm, on real fluoroscopy, with exact labels. That is the first per-vertebra recall
   on real fluoroscopy anyone will have measured.

## 7. Tools

| tool | does |
|---|---|
| `tools/dl_deepfluoro.py` | fetch past Cloudflare's TLS-fingerprint block |
| `tools/deepfluoro_convention.py` | settle the projection convention by reprojection |
| `tools/deepfluoro_render.py` | exact-pose DRR + real, landmarks on both, NCC |
| `slurm/deepfluoro_pairs.sh` | all 366 pairs, 32-way |
| `tools/deepfluoro_residual.py` | one pair's residual by frequency band, rendered |
| `tools/deepfluoro_residual_all.py` | all pairs; device-fixed vs per-frame test |
| `tools/deepfluoro_poses.py` | the real C-arm as a parameter distribution |
| `tools/deepfluoro_calibrate.py` | fit the nine device terms leave-one-specimen-out and by view angle; `slurm/deepfluoro_calibrate.sh` runs it |
| `tools/deepfluoro_noise_floor.py` | the stochastic ceiling; per-frame quadratic; residual by band |
| `tools/deepfluoro_photons.py` | the photon budget fitted to the real grain; `slurm/deepfluoro_photons.sh` |
| `slurm/deepfluoro_calibrate_v2.sh` | the four follow-up fits: scatter boxed, scatter dropped, kb opened, angle bins |
| `tools/deepfluoro_show_calibrated.py` | real vs raw DRR vs calibrated, bowel band isolated |
| `tools/spine_project.py` | a whole-spine CT under a real pose, calibrated, table stripped, labels by projection |
| `tools/ts_clean_subjects.py` | whole-spine subjects with every level and no metal |
| `tools/deepfluoro_anchor.py` | build the synthetic set and evaluate on the held-out specimen's real frames (`--dump` draws the calls); `slurm/deepfluoro_anchor.sh` chains build→train→eval per arm (`DR`, `TAG`, `SEED`, `REUSE`, `SUBJECTS`, `HELD`) |
| `tools/deepfluoro_anchor_report.py` | every evaluation in one table, grouped by arm, mean with min–max over seeds and folds |
| `slurm/deepfluoro_anchor_rescore.sh` | rewrite every arm's real test set and re-score its trained weights (`EVAL_ONLY=1`) |
| `tools/deepfluoro_anchor_baseline.py` | the constant-box location prior a detector must beat (5–60 % on real frames) |
| `tools/deepfluoro_refine.py` | the RealDRR-style refiner: train (full / highpass), apply, dump triplets |
| `tools/deepfluoro_explain_residual.py` | real, render, residual, the smooth surface, what is left, residual by scale — on real frames |
| `tools/deepfluoro_best_synthetic.py` | Figure 3: calibrated render, real frame, refined render, signed coloured residuals (`--all-stats` scores every held-out frame → `refiner_stats.json`) |
| `tools/deepfluoro_residual_regions.py` | the residual by region (edge, bone, enclosed, flanks, truncated) over every held-out frame, calibrated and refined; `slurm/deepfluoro_residual_regions.sh` |
| `tools/deepfluoro_edge_bias.py` | the edge-band residual binned by the bone path at the edge: thin bone against thick |
| `tools/deepfluoro_bandgain.py`, `tools/deepfluoro_pedestal.py` | the refuted linear enhancement; the pedestal and display-exponent sweeps |
| `tools/deepfluoro_transfer.py` | what function of the model attenuation the stored real frame is (transmission, log, power) |
| `tools/fluorocap_display_stats.py` | display-window statistics of published operating-room frames beside ours |
| `slurm/deepfluoro_linear.sh` | the whole chain under the linear reading of the real frame |
| `slurm/deepfluoro_v2.sh`, `deepfluoro_v2_crosseval.sh`, `deepfluoro_refine_arm.sh` | round v2: both arms rebuilt after the review with three seeds per fold; control B; the learned arms |
| `tools/make_formation_figure.py` | the manuscript figure, every number read from the files above |
