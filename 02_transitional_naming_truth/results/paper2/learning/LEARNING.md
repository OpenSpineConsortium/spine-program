# What the level encoder learned about a vertebra

Stream B of the 2026-09-23 figure request. Everything here is read off HELD-OUT crops: the validation split of
the v9 crop bank (never a training crop) and real intraoperative bodies the encoder never saw (the C-ArmLSpine
TEST cases and the COBRA Elekta-XVI TEST cases). Every number carries its denominator and a 2,000-resample
percentile interval clustered by person (the bank's patient key; the case for real frames). Chance for any
accuracy is 1/27 = 3.7 % uniform, and the majority share of the set is printed beside it.

Files: `embeddings.npz` (512-d features and 27 logits of every held-out crop), `map.npz` (PCA, t-SNE),
`analysis.json`, `gradient_regression.json`, `zones.json`, `l6_confound.json`, `census.json`, `bank_census.json`,
`gradcam_summary.{npz,json}` (mean maps), `gradcam.npz` (per-crop maps), `exemplars.npz`,
`embeddings_cpu_replicate.npz` (a second run of the same script on CPU: 16,418 rows, cosine to the GPU run
>= 0.999999, relative L2 <= 5.6e-6, identical argmax on every row). Grid jobs 40416675 (GPU) and 40416700
(CPU); outputs under `/rs/rs_grp_oschome/go2432/data/or_ready/learning{,_cpu}/`.

## What was run

- Encoder: `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt` (ResNet-18, two-channel stem, rung 1: a band of
  three bodies in view, target scaled to 96 px on a 320 px canvas, marker channel on the target; cross-entropy,
  40 epochs, augment 2). Its detached `fc` is the single-crop classifier the prototype reads. Its held-out exact
  accuracy here, 0.784 [0.764, 0.804] on 15,898 crops, equals the training run's own validation number (0.7837 in
  `result_rung_1_aug2.json`), which is the check that the crops were read and fed as the trainer fed them.
- Crops: the bank's `split == "val"` rows, streamed from the compressed bank so the 21 GB array never
  materialises; real frames cut with the prototype's own path (film histogram match against `~/films_drr`, the
  truth boxes, `crops_for_run` at 96 px / 320 px / rung 1). A truth box less than 90 % inside the frame, or cut by
  the CT, is context only and never a target, as in the bank builder.
- Scripts: `tools/learning_embed.py` (embeddings, Grad-CAM, occlusion, exemplars, census),
  `tools/learning_analyse.py` (PCA, t-SNE, ordering, silhouettes, neighbour composition, held-out `fc`),
  `tools/learning_gradients.py` (published gradients), `tools/learning_zones.py` (area-normalised attribution),
  `tools/learning_l6_confound.py` (the style confound), `tools/learning_bank_census.py`, `tools/fig_learning.py`
  (the figure). Grid wrappers `slurm/learning.sh` (GPU) and `slurm/learning_cpu.sh`.
- Intervals: percentile intervals over 2,000 cluster resamples. For a statistic recomputed from crops (Spearman,
  centroid positions, accuracies) the crops of a resampled person are taken whole. For per-sample quantities
  (silhouette, neighbour composition) the per-sample values are fixed and their mean is resampled by person.
  The gradient regression resamples people (for the centroids) and CT records (for the medians) jointly.
  UMAP is not installed in the grid env; the map is t-SNE (perplexity 30, PCA-50 init, seed 0).

## 0. What the held-out set contains (census.json, bank_census.json)

| set | crops | people / cases | levels present |
|---|---|---|---|
| bank validation (v9, `split == val`) | 15,898 | 1,804 people | C1-C7, T1-T12, L1-L6, sacrum: L6 150 (134 cases), sacrum 138, T12 680, L5 1,429, L4 1,556; **T13: 0** |
| C-ArmLSpine test (28 cases, 56 frames) | 228 bodies | 28 cases | L1 4, L2 42, L3 54, L4 54, L5 50, sacrum 24 (29 bodies unnamed because the two labellers disagree, 86 clipped, never targets) |
| COBRA Elekta XVI test (27 cases, six frames per case spread over the sweep) | 292 bodies | 27 cases | L3 10, L4 44, L5 114, sacrum 124 |

Sources of the bank validation crops: physics_drr 5,925, csxa 3,745, buu_full 2,664, physics_rare 1,195,
ctsp_drr 1,021, verse_drr 895, nhanes 453. The 150 held-out L6 crops are physics_rare 116, physics_drr 21,
verse_drr 10, ctsp_drr 3: renders, all of them.

The bank's training split holds 44 T13 crops from 37 cases and 652 L6 crops from 567 cases, against 3,654 T12
and 8,221 L5. **The validation split holds no T13 crop**, so nothing about T13 can be read from held-out data:
every T13 statement below is "not measurable", not a number, and T13 is in the figure's legend only as that
statement. No real held-out body is an L6 or a T13 (C-ArmLSpine's truth is the TotalSegmentator read, which
names L1-L5 only; the three C-ArmLSpine L6 patients in NUMBERS.md are a VERIDAH read and their bodies are
`level: null` here).

## 1. Does the space order the levels?

Not along any one axis; yes locally.

- PCA fitted on the 15,898 bank validation crops: PC1 explains 17.2 % of the variance, PC1-3 37.3 %.
  Spearman of PC1 with the level index over crops: **0.354 [0.311, 0.398]** (n = 15,898, 1,804 people); over the
  26 level centroids with five or more crops, rho 0.41, Kendall tau 0.27. The centroid order along PC1 is not the
  spine: cervical bodies sit low (C3 -9.3 to C7 -6.0), thoracic rise to T9 (+9.7), lumbar fall from L1 (+3.5)
  to L5 (-1.1), the sacrum sits at -1.5 and L6 at +3.7. The first principal axis separates regions and reverses
  inside them; it is not a craniocaudal coordinate. The best t-SNE axis reaches |rho| 0.73, again region
  structure rather than a line.
- The order IS there between neighbours: the nearest crop from another person is the **same level for 72.0 %**
  of the 15,898 crops and **within one level for 93.3 % [92.4, 94.2]** (level gap 0: 11,451; 1: 3,389; 2: 678;
  3: 155; 4 or more: 225). The space is a chain of neighbouring levels, folded, not a ruler.
- Real bodies (520 from 55 cases): Spearman of PC1 with level 0.445 [0.344, 0.530]; over the five real centroids
  with five or more bodies (L2, L3, L4, L5, sacrum) rho 0.90, tau 0.80.
- Style is also in the space. Within L5 crops alone, the silhouette of SOURCE is 0.099 (buu_full 0.26, ctsp_drr
  0.18, nhanes 0.15, the physics-styled renders about 0): films and renders of the same level form
  sub-clusters, visible in the map as the split cervical and lumbar clouds.

## 2. Where do L6 and T13 fall?

**T13: not measurable** (no held-out crop; 44 training crops from 37 cases).

**L6 sits beside L5, one ordinary inter-level distance away, and not between L5 and the sacrum.** On the 150
held-out L6 crops (134 cases) against 1,429 L5 and 138 sacrum crops:

- Fractional position of the L6 centroid along the L5 (0) to sacrum (1) line, in the full 512-d space:
  **-0.03 [-0.06, -0.01]**; in the ten-PC space -0.15 [-0.22, -0.06]. Along PC1 alone the quantity is undefined
  (L5 and the sacrum have nearly the same PC1; point -12 with interval [-138, 92]) and is reported only to say so.
- Distance of the L6 centroid from the L5 centroid, as a multiple of the L5-L4 distance: **1.07 [1.00, 1.17]**.
- Silhouette (cosine, full space) of L6 crops against L5: **0.322 [0.289, 0.352]**; the ordinary neighbour pairs
  are L5 vs L4 0.192 [0.174, 0.208], L4 vs L3 0.129, L3 vs L2 0.125, T12 vs T11 0.150, T12 vs L1 0.222; L5 vs
  sacrum 0.459 and L6 vs sacrum 0.620. L6 is more separable from L5 than L5 is from L4.
- Of the ten nearest other-person crops of an L6 crop, 0.60 [0.55, 0.64] are L5 and 0.34 [0.29, 0.40] are L6,
  against an L6 base rate of 0.9 % of the bank (9.5 % of L5-plus-L6): a 36-fold enrichment. Of an L5 crop's ten,
  0.78 are L5, 0.13 L4, 0.056 L6.
- The detached classifier names **0.800 [0.653, 0.922]** of the 150 held-out L6 crops L6 (0.187 called L5, 0.013
  L4); L5 0.770 [0.729, 0.812] of 1,429 (0.114 called L6); the sacrum 1.00 of 138.

**The tidy explanation was tested and does not hold.** Three quarters of the held-out L6 crops are physics-styled
renders, and style is in the space (above), so the separation could have been source rather than anatomy.
Recomputed within each source that holds both classes (`l6_confound.json`):

| source | n L6 / n L5 | silhouette L6 vs L5 | control: L5 vs L4 in the same source | L6 share of ten nearest (base rate) | d(L6,L5)/d(L5,L4) | classifier L6 exact |
|---|---|---|---|---|---|---|
| physics_rare | 116 / 140 | 0.281 [0.236, 0.325] | 0.173 | 0.81 [0.76, 0.88] (0.097) | 1.30 | 0.81 [0.68, 0.93] |
| physics_drr | 21 / 554 | 0.171 [0.127, 0.217] | 0.213 | 0.09 [0.06, 0.13] (0.004) | 0.61 | 0.71 [0.44, 0.96] |
| verse_drr | 10 / 52 | 0.520 [0.453, 0.574] | 0.383 | 0.60 [0.49, 0.71] (0.011) | 0.74 | 0.80 [0.50, 1.00] |

Style-matched, L6 remains apart from L5 in every source (neighbour enrichment 8- to 55-fold over the base rate,
classifier 0.71-0.81), and in two of the three it is more separable than the L5-L4 control. In physics_drr, where
L6 is 21 crops against 554, the silhouette (0.17) is below the control (0.21): with that few, the margin is thin.

**What this does and does not say about the 44.9 % L6 number.** That number (feasibility work, memory
`feasibility-claims-measured`) was measured on a different bank and protocol and is not comparable to the 0.80
here, which is on renders only. What the held-out data say is that the encoder does hold a distinct L6 region,
next to L5, and reads it at 0.80 [0.65, 0.92] when the crop is a render. Whether that region receives a real
L6 body is not measurable here: no held-out real L6 exists. One real-frame number points the other way: on the
24 real C-ArmLSpine test sacra the single-crop classifier says sacrum for 0.375 [0.25, 0.46] and **L6 for
0.417**; the L6 column absorbs real sacra. That is the blindness a decoder that counts from the sacrum has to
guard against, and it is a defect of the single-crop reading on real frames, not of the render space.

Single-crop accuracy on real bodies, for the record: C-ArmLSpine test 0.548 [0.490, 0.605] (n = 228, majority
0.237; L3 0.815 [0.704, 0.907] of 54, L4 0.574 [0.481, 0.667] of 54, L5 0.46 [0.38, 0.54] of 50); COBRA test
0.226 [0.153, 0.285] (n = 292, majority 0.425: below the majority rate; oblique gantry projections the encoder
never saw the like of).

## 3. What part of the crop the name depends on

Ten held-out crops per level from distinct people, seed 0, drawn at random from the validation split (so mixed AP
and lateral projections and mixed styles), Grad-CAM at layer3 (stride 16) and layer4 (stride 32) for the TRUE
class, and occlusion sensitivity (32 px patch, stride 16, drop in the true-class logit) as the hook-free check.
The crop is divided by its marker box into four zones: the body above, the target body, the body below, and
lateral to the target in its own rows. A raw share means little without the zone's size (the target box is 9-18 %
of the visible band), so `zones.json` reports **enrichment = share of attribution mass / share of band area**
(1 = uniform), with intervals over the ten crops.

Occlusion, enrichment target / above / below / lateral (bank validation, ten crops each):

| level | target | above | below | lateral | named right |
|---|---|---|---|---|---|
| T12 | 2.09 [1.71, 2.53] | 0.74 [0.40, 1.09] | 1.02 [0.69, 1.35] | 0.74 [0.45, 1.08] | 8/10 |
| L3 | 1.11 [0.76, 1.50] | 0.63 [0.43, 0.82] | 1.26 [1.06, 1.51] | 1.00 [0.74, 1.25] | 7/10 |
| L4 | 1.19 [0.87, 1.48] | 0.71 [0.48, 0.93] | 1.10 [0.91, 1.27] | 1.19 [0.85, 1.59] | 7/10 |
| L5 | 1.49 [1.18, 1.91] | 0.70 [0.52, 0.91] | 1.06 [0.84, 1.28] | 1.13 [0.77, 1.52] | 7/10 |
| L6 | 1.45 [1.15, 1.77] | 1.25 [0.87, 1.56] | 0.44 [0.16, 0.77] | 1.04 [0.72, 1.45] | 6/10 |
| sacrum | 3.48 [2.78, 4.29] | 1.25 [1.06, 1.42] | 0.30 [0.22, 0.38] | 0.78 [0.60, 0.94] | 10/10 |

Layer4 Grad-CAM agrees on the target (2.72, 1.54, 2.01, 2.24, 2.87, 3.99 for the same rows) and on the sacrum's
and L6's depleted "below" (0.40, 0.56). Layer3 is nearly uniform over the band (0.7-1.3 everywhere) and, on the
sacrum, puts 71 % of its mass in the black field below the pelvis: a receptive-field-edge artefact that the
rendered map shows and the number alone does not. The figure draws occlusion; layer3 is not used.

Reading: the target body is the most concentrated zone at every level, but it carries only 18-29 % of the
attribution mass; most of the evidence lies in the neighbours, and WHICH neighbour is the mechanism. For
L3-L5 the body below is enriched (1.06-1.26) and the body above depleted (0.63-0.71): an ordinary lumbar body is
named from itself and what lies caudal to it. For L6 this flips (above 1.25, below 0.44), and for the sacrum too
(above 1.25, below 0.30): the two bodies at the lumbosacral junction are named from themselves and what lies
cranial. On the ten real C-ArmLSpine crops per level (occlusion, target / above / below / lateral): L3 1.18 /
0.99 / 0.91 / 1.00, L4 1.48 / 0.98 / 0.85 / 0.90, L5 1.79 / 1.11 / 0.86 / 0.66, sacrum 1.85 / 1.27 / 0.11 / 1.32;
the target is again the most concentrated zone and the sacrum again reads from above, but the above/below
asymmetry of L3-L5 is not reproduced on real frames (the intervals include 1).

**The same pass on LATERAL subjects** (grid job 40416820, `lateral/`; `--cam-pool lateral`: one projection,
cleanest sources first, still distinct people and seeded; the ten per level came from ctsp_drr for T12, L3, L4,
L5 and the sacrum, and from verse_drr 7 + ctsp_drr 3 for L6). Occlusion, enrichment target / above / below /
lateral:

| level | target | above | below | lateral | named right |
|---|---|---|---|---|---|
| T12 | 1.75 [1.32, 2.20] | 0.56 [0.41, 0.70] | 1.27 [1.06, 1.52] | 0.68 [0.45, 0.94] | 9/10 |
| L3 | 2.53 [2.30, 2.79] | 0.58 [0.51, 0.65] | 0.98 [0.77, 1.17] | 0.38 [0.23, 0.58] | 9/10 |
| L4 | 1.62 [1.35, 1.89] | 0.58 [0.51, 0.64] | 1.36 [1.15, 1.54] | 0.44 [0.22, 0.70] | 8/10 |
| L5 | 1.43 [1.16, 1.72] | 0.61 [0.54, 0.67] | 1.36 [1.21, 1.52] | 0.54 [0.32, 0.80] | 8/10 |
| L6 | 1.57 [1.33, 1.83] | 0.82 [0.68, 0.96] | 1.01 [0.85, 1.15] | 0.81 [0.65, 0.97] | 9/10 |
| sacrum | 3.85 [3.20, 4.55] | 1.19 [1.02, 1.35] | 0.34 [0.27, 0.42] | 0.73 [0.54, 0.91] | 10/10 |

Layer4 agrees on the target (2.09, 2.21, 2.20, 2.11, 2.39, 4.14) and on the sacrum's depleted "below" (0.46).
This is the pass the figure draws, on the most legible of the ten crops (the crop is a backdrop; the map is the
mean of ten). With one projection the picture is consistent: at T12 and L3-L5 the name is read from the target
body (1.4-2.5 times uniform) and from the body below (1.0-1.4), with the body above (0.56-0.61) and the lateral
field (0.38-0.68) depleted, intervals clear of 1 for the target at every level and for "above" at every level;
the sacrum is read from itself (3.85) and from above (1.19 [1.02, 1.35]), with nothing below it (0.34). On the
rendered maps the hot region lies on the target body and the disc and body beneath it, not on the neighbours'
far ends. **The L6 "read from above" of the random pool does not survive the change of subjects** (above 0.82
[0.68, 0.96], below 1.01 [0.85, 1.15] here): it was a property of the AP physics-styled crops that pool drew, not
of L6. What is stable across both pools and both maps is that the target body is the most concentrated zone
everywhere and that the sacrum, uniquely, reads from what lies cranial to it.

## 4. Exemplars

For each level the five held-out crops (distinct people) nearest the level's prototype (mean unit embedding)
by cosine distance, `exemplars.npz`; in the figure for T12, L3, L4, L5, L6, sacrum. T12 and L3-L5 return lateral
bodies from films and lateral renders, end plates visible, each named right by the classifier. L6 returns
physics-styled AP renders: 116 of its 150 held-out crops are physics_rare, so the prototype is that source's
average, which is what section 2's within-source test was for. The sacrum returns lateral whole-pelvis renders
(ctsp_drr, verse_drr): at rung 1 the crop is three sacrum-heights tall, so "the sacrum" the network learned is the
lumbosacral silhouette at low magnification, and it names it right 138 of 138 times held out.

## 5. Which published gradients the space tracks (gradient_regression.json)

Per-level centroid of the held-out crops on PC1 (oriented so it rises from T11 to L5) against the per-level
median of each measure over the 802 CTSpinoPelvic1K records, T11-L5. The medians and record counts reproduce
`morphometrics/level_atlas.csv` exactly (same plausibility gates); end-plate width has no L5 (withheld by the
article). R^2 is the seven-level fit, Q^2 the same fit with each level predicted from the other six, crop-LOO the
ridge from every held-out crop's 512-d embedding to its level's median trained on six levels and applied to the
seventh, real check the bank line applied to the real C-ArmLSpine centroids (L2-L5, sacrum excluded). Joint
2,000-resample intervals over people and CT records; held-out crops per level 568-1,556.

| measure | R^2 (PC1) | Q^2 one level out | Spearman | crop-LOO Q^2 | real check R^2 |
|---|---|---|---|---|---|
| body height, anterior | 0.96 [0.92, 0.97] | 0.91 [0.78, 0.92] | +0.99 | 0.65 [0.64, 0.67] | 0.65 |
| transverse-process span | 0.95 [0.93, 0.96] | 0.89 [0.87, 0.91] | +0.93 | 0.64 [0.62, 0.65] | 0.63 |
| wedge ratio (ant/post) | 0.90 [0.89, 0.92] | 0.84 [0.82, 0.87] | +1.00 | 0.78 [0.76, 0.79] | 0.75 |
| end-plate width (T11-L4) | 0.82 [0.77, 0.85] | 0.59 [0.49, 0.67] | +1.00 | 0.53 [0.51, 0.54] | (three levels; not run) |
| canal width, interpedicular | 0.81 [0.79, 0.84] | 0.54 [0.48, 0.60] | +1.00 | 0.35 [0.33, 0.36] | 0.37 |
| body height, posterior | 0.63 [0.41, 0.68] | 0.03 [-0.41, 0.23] | +0.61 | 0.13 [0.10, 0.16] | -1.76 |
| canal depth, midsagittal | 0.02 [0.00, 0.10] | -1.25 [-1.43, -0.97] | -0.23 | -0.34 [-0.38, -0.31] | -0.11 |

What this can and cannot say. With seven levels, every gradient that is monotone from T11 to L5 is nearly
collinear with the level index, so the regression separates monotone gradients from non-monotone ones and cannot
credit one monotone gradient over another: anterior height, process span, wedge ratio, end-plate width and canal
width all rise caudally and all fit. The two it ignores are the two that do not run monotone: posterior body
height (26.4, 28.8, 30.4, 30.4, 30.4, 29.6, 30.4 mm: a plateau) and midsagittal canal depth (16.6 to 17.8 and
back: flat). The crop-level Q^2 is the more discriminating column because it asks whether a level's value is
interpolated from its neighbours' crops: the wedge ratio, whose profile is closest to a straight line
(0.94, 0.94, 0.97, 1.00, 1.03, 1.05, 1.06), interpolates best (0.78), the plateau and the flat profile not at all.
The encoder never sees a millimetre (every target is 96 px tall), so what it tracks is the shape gradient that
runs with these sizes, not the sizes.

## What is not known

- Anything about T13 held out: the validation split has none, and the training split has 44 crops from 37 cases.
- Whether a real L6 body lands in the L6 region: no real held-out L6 exists. The one real number bearing on the
  L6 column is adverse (real sacra called L6 0.417 of 24).
- Whether the "read from below" asymmetry of T12-L5 holds on real frames: on the lateral render subjects the
  body below is enriched (1.27-1.36 at T12, L4, L5, intervals clear of 1) and the body above depleted at every
  level; on the ten real C-ArmLSpine crops per level the above/below intervals include 1. The real subjects mix
  AP and lateral frames, as the random pool did, and that pool showed how much the subjects matter.
- Which part of the target body the name depends on within the body (end plate, posterior wall, pedicle): the
  occlusion patch is 32 px on a 96 px body and the ten crops are averaged, so the maps resolve the body from
  its neighbours and not the body's parts.
- COBRA single-crop naming is below the majority rate; the COBRA bodies are in the map as real points and in no
  other number here.
