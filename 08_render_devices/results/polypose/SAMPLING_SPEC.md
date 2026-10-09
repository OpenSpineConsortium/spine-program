# PolyPose sampling spec — the global sagittal compensation model

**spec_version 2, 2026-09-23.** This document is the readable rendition of
[`sampling_spec.json`](sampling_spec.json), which is the machine-read truth. Every number here
carries an author-year key that resolves in [References](#references) with PMID/DOI and a
verification status. `tools/polypose/check_sampling_spec.py` recomputes the model algebra, the
share tables, the variant arithmetic and every quoted cohort number against
`cohort_sagittal.json` / `cohort_rows/cohort_grid.json` / `joint_model_numbers.json`, and exits
non-zero on any mismatch or any citation key that does not resolve. Last clean run 2026-09-23.

v1 (`sampling_spec.v1.json`) is superseded: its single LL target became a joint draw
(SS, LL, TK | PI) with a supine conversion, a Roussouly shape rule, an in-field thoracolumbar
coupling, an explicit rejection envelope and an envelope-covering fill-in; the cohort is now the
grid re-measurement (one code path), not the release CSV.

---

## 1. What this is

Per-level sampling distribution, junction rules and checks for **generative** use of the
PolyPose polyrigid transform on labelled spine CT. The transform is published — Gopalakrishnan,
Dey, Golland, *PolyPose: Deformable 2D/3D registration via polyrigid transformations*, NeurIPS
2025, arXiv:2505.19256, PMID 40492249, MIT [polypose] — and validated on DeepFluoro at pelvis
Dice 0.99, femurs 0.98, HD95 1.48/1.56 mm, 0.00 % folds. Only the sampling distribution, the
junction rules and the checks are ours, and the sampling distribution is itself assembled from
the literature. Transform mechanics as read from the pinned source (commit `909a9bb2`):
[`POLYPOSE_API.md`](POLYPOSE_API.md).

## 2. Conventions

- **Sign.** delta > 0 = more lordosis at that segment (extension direction). Kyphosis-positive
  quantities (TLK) are reported with the opposite sign by `measure_sagittal.py` and converted
  at the boundary.
- **Segment.** Named upper-lower (L4-L5); its delta is the relative rotation of the upper body
  about the segment hinge with the lower body held. Hinge = centre of the disc below the moving
  body (midpoint of the two plate centroids from `measure_sagittal.py`); rotation axis = the
  patient left-right axis (bicoxofemoral vector where femoral heads exist, else image x).
- **Chain.** Absolute pose of body k = product of the relative hinge rotations of every mobile
  segment between k and the pelvis; the pelvis (sacrum, hips, femora, and any body fused to the
  sacrum) is the identity.
- **Frames.** STANDING = the published normative cohorts; SUPINE = this cohort and every warped
  output; IMAGE = the CT with the pelvis fixed. PI is the same in all three.
- **Volumes.** Analysis in the RAS canonical frame of `nib.as_closest_canonical`; volumes are
  **never** reoriented when written; axcodes are read and recorded.
- **Labels.** Resolved with `ostk.labels.labels_for(volume)`, never a fixed map. VerSe-native:
  L1=20 … L6=25, sacrum=26, T13=28, hips 30/31, femora 32/33; id 29 is retired in v11 and never
  gated on.

## 3. The joint sagittal model — (LL, TK, SS) | PI

One multivariate normal over (PI, LL, TK, SS) in the **standing** frame of the asymptomatic
normative literature. The sampler never draws PI: PI is the patient's, measured on the source
CT and invariant under the warp. It draws (LL\*, TK\*, SS\*) from the conditional given PI and
sets PT\* = PI − SS\*.

### 3.1 Means and SDs (standing)

| parameter | mean ± SD | source |
|---|---|---|
| PI | 52.0 ± 10.7 | sardar2022 (MEANS, n=468, age 40.4 ± 14.8, multi-ethnic) |
| LL (L1-S1) | 57.4 ± 11.3 | sardar2022 |
| TK (T4-T12) | 37.4 ± 10.9 | sardar2022 |
| SS | 39.5 ± 8.2 | sardar2022 |
| PT | 12.5 ± 7.3 | sardar2022 |
| PI − LL | −5.4 ± 10.7 | sardar2022 |

MEANS is used because it is the only series with all five parameters, SDs, a PI−LL SD, a
multi-ethnic sample and a published LL regression on PI, TK and age
(LL = 14.6 + 0.57 PI + 0.57 TK − 0.2 age [sardar2022]). Alternates kept beside it:
yukawa2018 (n=626: PI 53.7 ± 10.9, LL_T12-S1 49.7 ± 11.2, TK_T1-T12 36.0 ± 10.1, SS 39.4 ± 8.0,
PT 14.5 ± 8.4, SVA 3.1 ± 12.6 mm), vialle2005 (n=300: PI 55.0 ± 10.6, LL_max 60 ± 10,
SS 41 ± 8.4, PT 13 ± 6), wang2022 (n=385: PI 46.8 ± 9.7, LL 55.9 ± 9.1, TK 40.3 ± 8.7).

### 3.2 Correlation matrix (order PI, LL, TK, SS)

```
        PI     LL     TK     SS
PI    1.00   0.60   0.10   0.80
LL    0.60   1.00   0.45   0.86
TK    0.10   0.45   1.00   0.35
SS    0.80   0.86   0.35   1.00
```

| entry | value | source |
|---|---|---|
| PI-SS | 0.80 | vialle2005, n=300 |
| SS-LL | 0.86 | vialle2005 (maximal lordosis) |
| PI-LL | 0.60 | vialle2005 regression LL = 0.54 PI + 27.6 implies 0.57; wang2022 rs 0.663; hyun2019 R² 0.348 → 0.59; this cohort 0.64 |
| LL-TK | 0.45 | wang2022 rs 0.370; pan2024 T10-L1 R² 0.201 → 0.45 (T4-L1 R² 0.457 → 0.68 includes T12-L1) |
| PI-TK | 0.10 | wang2022 rs 0.051 n.s. |
| SS-TK | 0.35 | **not published as a pair**; set so TK relates to SS through LL (0.86 × 0.45 = 0.39, rounded down); the matrix is then positive definite (eigenvalues 6.83, 36.16, 109.11, 276.12) |

### 3.3 Conditional given PI

mean_i = μ_i + β_i (PI − 52.0), with (recomputed and enforced by the checker):

| | β on PI | residual SD | residual correlations |
|---|---|---|---|
| LL | 0.6336 | 9.04 | LL-TK 0.49 |
| TK | 0.1019 | 10.85 | LL-SS 0.79 |
| SS | 0.6131 | 4.92 | TK-SS 0.45 |

Reading: at a given PI, one degree of PI buys 0.63° of LL (Vialle 0.54 [vialle2005], Hyun 0.62
[hyun2019]), 0.61° of SS (Vialle 0.54) and 0.10° of TK; the residual spread of LL around its
PI-conditional mean is 9.0°. Exported for the sampler as `joint_model_numbers.json`.

### 3.4 Outside checks of the assembled matrix

The matrix is assembled from four cohorts, not estimated on one, so it is checked against
quantities it was not fitted to:

- **Implied PT** (= PI − SS): 12.5 ± 6.43 against published 12.5 ± 7.3 [sardar2022].
- **Implied PI − LL**: −5.4 ± 9.85 against published −5.4 ± 10.7 [sardar2022].
- **Implied PT regression on (PI, LL, TK)**: 0.65 PI − 0.41 LL − 0.04 TK, residual 3.0°,
  against the ISSG predictor (r = 0.93, SE 4.4° [lafage2011]; its coefficients
  PT = 1.14 + 0.71 PI − 0.52 LL − 0.19 TK circulate only in secondary quotations and are used
  for nothing).
- The SS-TK entry remains an assumption and is flagged as such (§18).

### 3.5 Compensation slopes at fixed PI (the cascade)

dSS/dLL = +0.43, dPT/dLL = −0.43, dSS/dTK at fixed LL = +0.04. Loss of one degree of lordosis
retroverts the pelvis by 0.43° on average (Lafage secondary-quoted −0.52; the vertical-trunk
identity with TK ≈ 0.45 LL gives −0.55; this cohort's unconditional SS-on-LL slope 0.56). This
is the sign pattern of the published cascade — loss of LL → PT up, SS down at fixed PI,
thoracic hypokyphosis, knee flexion beyond [barrey2011, diebo2015]; knee and ankle are outside
the CT.

### 3.6 Balance identity

c = SS − LL + TK: mean 19.5, SD 10.3 under the model. For a vertical trunk c is a constant plus
the trunk's tilt; the published correlations give it an SD of 10.3°, far looser than the 3.1°
SD of Vialle's T9 offset — TK definitions differ between series, and cervical spine and T1
slope absorb the rest. The gate (§11) uses the model's own band; a 3-degree identity would
reject most of the literature's own cohort.

## 4. Supine conversion

The normative cohorts stand; every CT here is supine; the sampler's targets and checks live in
the supine frame. Published standing→supine offsets (degrees):

| parameter | offset | source (n) |
|---|---|---|
| LL | −4.6 | chevillotte2018 (15, asymptomatic <50 y) |
| LL | +2.1 | bouaicha2014 (52, trauma w/o fracture; **sign not established by the abstract**) |
| LL | 0.0 | fan2023 (64, degenerative, MRI) |
| LL | −6.2 at LL 55 | izatt2012 (30, AIS; the equation LL_supine = 0.71 LL + 9.7 is not in the abstract) |
| SS | +3.9 | chevillotte2018 |
| SS | +2.0 | fan2023 |
| SS | +0.9 | banitalebi2026 (211, stenosis) |
| SS | +7.1 | hasegawa2018 (24, ASD — not normative) |
| TK | −2.5 | hasegawa2018 (T4-T12) |
| TK | −2.0 | fan2023 (TJK) |
| TK | −6.1 at TK 40 | izatt2012 |

The direction of the LL offset is **not consistent across series** (−6 to +2; +11.3 in
deformity); the magnitude is a few degrees except in deformity. The sampler therefore draws the
offset, once per output, records it, and holds PI fixed (PI identical in all positions
[chevillotte2018]; Hasegawa's −4.3 in ASD is a landmark effect and is not modelled):

- dLL ~ N(−2.5, 3.0); dSS ~ N(+3.5, 2.5); dTK ~ N(−2.5, 2.0); dPI = 0. PT_supine = PI − SS_supine.

Cohort check: ordinary CTSP supine (n=710) has PI 51.98 ± 11.05, SS 36.44 ± 10.62,
PT 15.54 ± 7.85, LL 51.13 ± 14.04, TLK_T10-L2 3.97 ± 12.27. PI matches MEANS to 0.02° and
Veilleux's automated supine CT to 0.07° [veilleux2020]; SS sits 6.6° below the supine model and
PT 6.5° above it — the older, symptomatic, table-with-bolsters population effect documented in
`docs/SPINOPELVIC_ESTIMATOR.md` (Hasegawa's older supine cohort PI 53.4 / SS 34.1 / PT 19.2 is
within 2-4° of this one [hasegawa2018]). The cohort's LL SD (14.0) is 1.24× the widest
published (11.3): wider on both tails.

## 5. Image-space realisation — where the pelvic tilt goes

The pelvis is **fixed in image space** (§9 pelvis rule), so PI, SS_image and PT_image are
invariant by construction and re-measured as such. SS and PT are the pelvis' orientation
against the vertical; with the pelvis held, the only image-space trace of a different standing
PT\* is the orientation of the trunk relative to the sacrum — the sum of the segmental angles:
d(trunk vs sacrum) = dLL − dTK. **The pelvic-tilt compensation is realised by the segmental
deltas themselves and by nothing else.** A separate rigid rotation of the column on the sacrum
would double-count it and change measured LL by the same amount. The task rule "the junction
rotation IS the pelvic-tilt compensation" is honoured in this sense: the junction carries its
share of dLL (zero when fused), and the drawn PT\* is the standing tilt the resulting relative
geometry corresponds to — recorded in the manifest, checked through the balance gate, never
applied as a rotation.

Applied: dLL over the mobile lumbar segments by type-modulated shares (§6-7); the in-field part
of dTK over T10-T11 / T11-T12 / T12-L1 (§7); small lateral-bending and axial-rotation draws
(§10); nothing on the pelvis, the sacrum, any fused body, or the femora. Recorded but not
applied: dTK above T10 (out of field), SS\*/PT\* (standing, virtual), the supine offsets drawn.
Re-measured after warp: LL, TLK, junction angle, PI/SS_image/PT_image, every body's wedge (§15).

## 6. Roussouly shape rule

Types from the drawn standing SS\* [roussouly2005; wording per tu2023; 3AP per laouissat2018]:

| type | SS\* | shape |
|---|---|---|
| 1 | < 35 | apex at the centre of L5, short lordosis (≤ 3 bodies), long thoracolumbar kyphosis |
| 2 | < 35 | apex at the base of L4, flat back, few lordotic segments |
| 3 | 35-45 | apex at the centre of L4 / L3-L4 disc, ~4 lordotic bodies, inflection at the TL junction |
| 4 | > 45 | apex at the base of L3 or higher, ≥ 5 lordotic bodies, largest TK |
| 3AP | > 35 with PT ≈ 4 ± 3 | anteverted pelvis, PI 48 ± 6, 16 % of laouissat2018's 296; treated as type 3 for shape; sets the anteverted PT\* floor |

Types 1 and 2 are not separable by SS alone; the sampler assigns type 1 when the in-field TLK
target is above its conditional mean (the long TL kyphosis is type 1's defining trait), else 2.
Frequency checks for the generated set: PI by current type 40.8 / 43.6 / 52.4 / 62.4 / 43.7
(1/2/3/4/3AP), 34.7 % change type between current and theoretical [shen2024]; per-type PI
39 / 41 / 53 / 62 / 48 and PT 10 / 10 / 13 / 12 / 4 [laouissat2018]. This cohort by standing
SS = supine SS − 3.9 [chevillotte2018]: 60.6 % type 1/2, 26.1 % type 3, 13.4 % type 4 (n=710) —
older than Laouissat's type-3-heavy young cohort.

**Lower-arc share of LL (L4-S1) by type**: 0.834 / 0.652 / 0.647 / 0.615 for types 1/2/3/4
[chung2020, n=160]. Within-arc split from milele2022's segmental contributions
(2.3 / 11.7 / 18.1 / 25.2 / 42.7 % of L1-S1, n=324): lower arc L4-L5 0.371, L5-S1 0.629; upper
arc L1-L2 0.072, L2-L3 0.366, L3-L4 0.563. Resulting shares (checker-verified = lower_arc ×
within_arc):

| type | L1-L2 | L2-L3 | L3-L4 | L4-L5 | L5-S1 |
|---|---|---|---|---|---|
| 1 | 0.012 | 0.061 | 0.093 | 0.309 | 0.525 |
| 2 | 0.025 | 0.127 | 0.196 | 0.242 | 0.410 |
| 3 | 0.025 | 0.129 | 0.199 | 0.240 | 0.407 |
| 4 | 0.028 | 0.141 | 0.217 | 0.228 | 0.387 |

**How applied.** The *increment* dLL is distributed by the target type's shares; the source's
own per-segment angles are not re-targeted, because the cohort's per-segment measurements carry
8-12° SD of plate-fit noise (§17) and targeting absolute segment angles would inject that noise
into the warp. The warp changes the amount of lordosis with a type-consistent distribution of
the change; it does not re-shape a type-2 spine into a type-4 spine.

## 7. Per-level distribution and the thoracolumbar coupling

Population segment shares of L1-S1 lordosis (the type-3 row up to rounding): L1-L2 0.023,
L2-L3 0.117, L3-L4 0.181, L4-L5 0.252, L5-S1 0.427 [milele2022]. Cross-checks: L4-S1 = 0.679 of
LL; apex at L4 in 56.6 % [shen2023]; lordosis starts at L1-2 and increases caudally
[bernhardt1989]. Fused segments get share 0 and the rest renormalise.

**Thoracolumbar coupling.** Abdominopelvic CT holds T9/T10 down; T4-T12 kyphosis is not in the
image; the in-field thoracic compensation is T10-L1. Published: T10-L1 = −3.6 − 0.2 LL
(kyphosis-negative; R² 0.201, n=280) and T4-L1 = 3.4 − 0.5 LL (R² 0.457) [pan2024] — so T10-L1
carries 0.2/0.5 = 40 % of the LL-coupled thoracolumbar change. T10-L2 is for practical purposes
straight in normals [bernhardt1989]; T10-T12 kyphosis 9.5-12.9 by age [korean2020]; TL junction
kyphosis 11 ± 9 standing, 9 ± 7 supine in degenerative patients [fan2023].

The draw: dTLK_T10-L1 = 0.2 × dLL + N(0, 2.0), split over T10-T11 / T11-T12 / T12-L1 as
0.340 / 0.283 / 0.377 (proportional to each segment's mean cap), clipped to §8. The full TK\* is
drawn for the envelope and the balance gate; only its 40 % in-field share is realised.
**Caveat, measured:** the supine cohort shows *no* TLK-LL coupling (r = −0.03, n=648) where the
standing literature has a weak one (R² 0.20). The coupling is applied at its published strength
because the target profile is a standing patient's; it is flagged as unverified in supine (§18).

## 8. Segmental ROM caps

Hard caps on the relative rotation of one segment, per direction, from the neutral supine pose
(degrees; flex = lordosis-reducing, ext = lordosis-increasing; lb/ar one-sided). In vitro at
7.5-10 N·m; the in vivo totals (~14° flex+ext per lumbar joint, ~2° ar, lb 10/6/3 upper/L4-L5/
L5-S1 [pearcy1984a, pearcy1984b]) bracket the in vitro sums.

| segment | flex | ext | lb | ar | source |
|---|---|---|---|---|---|
| T10-T11 | 3.07 | 3.07 | 3.99 | 4.04 | wilke2017 (S1 per-specimen means, n=6; corrected 2026-09-26 from 1.75/1.75/2.1/2.4, which halved per-direction values) |
| T11-T12 | 2.7 | 2.4 | 3.5 | 1.8 | oxland1992 |
| T12-L1 | 2.9 | 3.9 | 3.7 | 1.2 | oxland1992 |
| L1-L2 | 5.8 | 4.3 | 4.9 | 2.3 | yamamoto1989 |
| L2-L3 | 6.5 | 4.3 | 7.0 | 2.6 | yamamoto1989 |
| L3-L4 | 7.5 | 3.7 | 5.7 | 2.6 | yamamoto1989 |
| L4-L5 | 8.9 | 5.8 | 5.7 | 2.2 | yamamoto1989 |
| L5-S1 | 10.0 | 7.8 | 5.5 | 1.4 | yamamoto1989 |

White & Panjabi's textbook Tables 2-2/2-3 are listed as secondary and **unverified** (no scan
on hand) and are not used as a bound [whitepanjabi1990]. The machine copy
`docs/polypose_segmental_rom.csv` — the by-name backstop bound `polypose_manifest.py` records
and re-checks per row — is generated from `sampling_spec.json:rom_deg` by
`tools/polypose/gen_rom_csv.py` (flex_ext = flex + ext, lb/ar one side; the transitional
segments carry the §9 anchoring rows), and the checker fails if the two ever differ.

**On "Panjabi 1991 Table 3".** Panjabi 1991's Table 3 (p. 892, image-only scan on disk, read by
eye 2026-09-23) is vertebral-body **morphometry** (EPWu, EPDu, VBHp, end-plate inclinations),
*not* segmental range of motion; the task text conflates it with the ROM papers above. It is
used here only for the thoracic body-wedge reference (EPIt T10 1.7°, T11 4.5°, T12 4.0°)
[panjabi1991]; the lumbar analogue gives body wedges L1 6.7° … L5 4.0° [panjabi1992]. Segmental
ROM comes from yamamoto1989 / oxland1992 / wilke2017 (all Panjabi-lab or successor protocols).

## 9. Junction rules by subtype

**Pelvis rule.** Rigid body = sacrum, coccyx, both hips, both femora, and any body with
multiplier 0 at its caudal junction; motion = identity; PI, SS_image, PT_image unchanged within
0.5° (re-measured).

**Castellvi multiplier** on the named junction's caps (grade from the anomaly tables —
`lstv_flag_labels_v2.csv` for CTSP, Löffler Suppl. Table 1 for VerSe — never inferred from
label ids):

| grade | multiplier | basis |
|---|---|---|
| 0, I (a/b) | 1.0 | enlarged transverse process only, no articulation [castellvi1984, konin2010] |
| II (a/b), unknown | 0.45 | pseudo-articulation: pooled II-IV L5/S1 flexion-extension ROM 3.3 ± 3.8 vs 7.3 ± 3.8 in controls [kuoppala2025]; an upper bound for II alone |
| III (a/b), IV | **0.0** | osseous fusion by definition [castellvi1984]; III/IV protect the transitional disc [cheng2022]. weng2025's residual FE motion comes from a modelled disc and is not used |

IIIa (one side fused) counts as fused — a bony bridge blocks sagittal motion; IIa counts as II.

**Subtypes:**

- **ordinary** — mobile T10-T11 … L5-S1; caps §8; shares §6-7; junction = L5-S1 × multiplier.
- **L6** (six lumbar bodies, label 25) — mobile chain extends to L6-S1. Caps and shares
  **anchored at the sacrum**: L6-S1 ← L5-S1, L5-L6 ← L4-L5, …, top cap reused; shares
  renormalised (÷1.023). Junction = L6-S1 × multiplier at L6. *Evidence gap:* no published
  segmental ROM for six-lumbar spines; anchoring at the sacrum is a decision (lumbosacral
  mechanics are set by the pelvis), stated as such.
- **sacralised_L5** (four mobile lumbar bodies; Castellvi III/IV at L5-S1 or release
  n_lumbar 4) — L5 joins the pelvis rigid body; multiplier 0; L4-L5 keeps its own caps
  (no excess at the adjacent level [kuoppala2025]); shares renormalised to L1-L2 0.040,
  L2-L3 0.204, L3-L4 0.316, L4-L5 0.440. A partial (II) sacralisation is handled by the
  multiplier, not this subtype.
- **T13** (thirteen rib-bearing vertebrae, label 28) — extra segment takes thoracolumbar caps:
  T12-T13 ← T11-T12, T13-L1 ← T12-L1 [oxland1992], T11-T12 ← T10-T11 [wilke2017]; lumbar as
  ordinary. *Evidence gap:* no published ROM or sagittal series for T13 spines.
- **lumbar_rib_L1** — ordinary; no evidence of altered motion.
- **four_lumbar_count_without_fusion** (rare; count anomaly, not fusion) — ordinary caps with
  L4-S1 ← L5-S1; flagged for manual review.
- **both LSTV and TLTV** — apply the lumbosacral subtype rule and the T13 rule together.

**Adjacent-level hypermobility above a fusion: NOT modelled.** Total lumbar ROM in LSTV 33.5 vs
38.3 (n.s.) with compensation spread over the superior segments, not the adjacent level
[kuoppala2025]; degeneration above III/IV is a long-term load effect, not a ROM value to sample
[cheng2022]. What *is* retained: the requested dLL redistributes over the remaining mobile
segments (caps unchanged), so a fused spine reaches ordinary lordosis with fewer segments —
the population finding (LL n.s. [yokoyama2016]; +7 [jacob2023]).

The only asymptomatic normative series reporting sagittal parameters by vertebral **count** is
yan2022 (n=389: 11T+5L n=12, 11T+6L n=8, 12T+4L n=8, 12T+6L n=15; variant groups differ,
p<0.05; per-group means paywalled — only group sizes used).

## 10. Per-segment draw

Truncated normals. Mean = share_i(type\*) × dLL for lumbar segments, the §7 split of
dTLK_T10-L1 for the three thoracolumbar segments. SD = 0.4 × cap in the direction of the mean.
Bounds = [−cap_flex, +cap_ext] after the junction multiplier. A draw beyond its bound is
clipped and the remainder redistributed once over the other mobile lumbar segments in
proportion to their shares; any residue is recorded as `dLL_shortfall` and the tolerance check
compares against the clipped request. Lateral bending ~ N(0, 1.0) bounded ± 0.5 lb_i; axial
rotation ~ N(0, 0.5) bounded ± 0.5 ar_i. No translation is drawn: every translation follows
from the hinge rotations. Invariant by construction: PI (pelvis is identity), per-body wedge
(bodies move rigidly), vertebral count and every label id.

## 11. Rejection envelope

Applies to every drawn standing profile **before** anything is rendered; a rejected draw is
redrawn with the next sub-seed and counted in the manifest row.

Marginal bounds (standing, degrees):

| quantity | bounds | basis |
|---|---|---|
| LL\* | 25 … 88 | MEANS 2.5 SD = 29-86 [sardar2022], widened for the supine side and the cohort's own 95 % band (28-72 supine) |
| TK\* | 10 … 65 | MEANS 2.5 SD [sardar2022] |
| SS\* | 15 … 65 | MEANS 2.5 SD = 19-60; Vialle 41 ± 8.4 [vialle2005]; cohort supine SS reaches 60 |
| PT\* | −8 … 35 | 3AP floor PT 4 ± 3 [laouissat2018]; Schwab ++ at 30 plus model 2.5 SD = 30.8; ASD mean 29.2 [diebo2015] |
| PI − LL\* | −30 … 20 | MEANS −5.4 ± 10.7 → 2.5 SD [sardar2022]; Schwab ++ beyond 20; cohort supine 95 % band −15…+16 |

Joint bounds: the residual (LL\*, TK\*, SS\*) − conditional mean inside the 99 % ellipsoid of
the conditional covariance (χ²₃ ≤ 11.34); |c\* − 19.5| ≤ 25.8 (§3.6); Roussouly consistency
(SS\* < 35 with LL\* > 70, or SS\* > 45 with LL\* < 40, is rejected — table corners, since no
per-type LL mean is published with an SD).

Per-level: after distribution and one redistribution, |dLL_shortfall| ≤ 3° and every segment
inside cap × multiplier; otherwise the draw is rejected, not clipped further.

Source sanity: a source whose own measurement fails any of LL ∈ [10, 85], |junction disc| ≤ 30°,
|TLK_T10-L2| ≤ 40°, S1 plate accepted, PI available, is **not a source** (29 CTSP cases
excluded, §17); a fused-junction source additionally needs its Castellvi read.

## 12. Fill-in rule — cover the whole envelope

Goal: every anatomical profile the literature describes exists in the bank, not only the thin
bins. Strata = PI bins of 5° from 25 to 80 (11) × conditional-LL deciles (10) × implied
Roussouly type; targets drawn from the supine-converted conditional model within each stratum;
strata filled to a common count, so the low- and high-lordosis corners get as many outputs as
the centre. Source choice per target: seeded uniform draw among plate-sane ordinary cases with
PI in the bin and |LL\* − LL_source| ≤ 0.8 × the summed directional caps (38.7° flexion, 25.9°
extension over five lumbar segments); nearest PI bin tried once; else recorded unreachable.

For the record, the cohort's deficits depend on the reference (all n=710, checker-verified
against `cohort_grid.json`): vs Chevillotte-supine, 129 cases short, thin at LL 35-60; vs
Yukawa-shifted, 152 short, thin at LL 15-45; vs MEANS-shifted, 60 short, thin at 55-60 and
long below 35; PI vs Yukawa 60 short at 65-75. The three references disagree by 8° in the mean,
so the fill-in covers the envelope **uniformly by stratum** instead of chasing one reference's
deficit.

**Rare-class rule.** For L6 / T13 / sacralised variants the target LL is drawn from the SAME
reference distribution as ordinary spines (truncated ± 2.5 SD), so lordosis does not separate
the classes in the render bank. Rationale: 2-D angles separate LSTV from ordinary at AUC
0.665-0.831 in real life — segmented lordotic angles on EOS: LSTV-vs-none cVPVA 0.797 / dVPVA
0.782, type II 0.665-0.718, III-IV 0.797-0.831 [albano2020]; a 2025 deep-learning radiograph
model reaches AUC 0.84 [dl_radiograph2025]. **Geometry is weakly informative; the network must
learn the COUNT at the junction.** Leaving the angle association in place would hand it a
shortcut for a decision that is a count. PI, which the warp cannot change, keeps its real class
association — and this cohort reproduces it: L6 PI 60.9 (n=14) vs ordinary 52.0 vs sacralised
47.9 (n=17); published: six-lumbar PI 64.8 vs 51.3 [yokoyama2016], 65.3 at true S1
[haffer2021], LSTV 58.5 vs 50 [jacob2023], 52.1 vs 47.8 [ouchida2024]; LL n.s. [yokoyama2016];
sacralisation measured at the first non-mobile plate gives LL 30.2 [muller2024] because the
plate moves down a level (~27° between upper and lower plate choice [karabag2024]).

## 13. Variants per case and scale

Real rare CT inventory: VerSe L6 50, T13 6 (Castellvi IIa 35, IIb 25, IIIa 14, IIIb 28, IV 7);
CTSP L6 18, sacralised/4-lumbar 20, T13/lumbar-rib 14, fused III/IV 25; TS L6 called 12 —
**N_rare = 86** (VerSe L6+T13 + CTSP L6 + TS L6; sources `anomalous_inventory.json`,
`cohort_ctsp_release.json`, Löffler Suppl. Table 1). Real rare films: BUU 15 L6 patients /
30 films, 129+7 four-lumbar patients. C-ArmLSpine's 3 L6 cases / 6 real frames are **test only**.

Evidence caps [ratio_report]: variants in 25-35 % of rendered CTs; synthetic : real rare
≤ 10:1; 4× epoch oversampling of real transitional renders; 200-500 renders per CT (flattening
window), value 300.

v2 counting rule (checker-verified): CTs carrying a synthetic anatomy = rare variants
(N_rare × V) + ordinary fill-in (N_fill); their share of rendered CTs must be 25-35 %.

| bank | V | rare variants | N_fill | share | rare ratio |
|---|---|---|---|---|---|
| full (TS v3), 2,911 CTs | 10 | 860 | 500 | 0.318 | 10:1 (the cap binds) |
| CTSP+VerSe, 1,176 CTs | 4 | 344 | 150 | 0.296 | 4:1 |

Corpus estimate, full bank: 4,271 CTs rendered × 300 = **1,281,300 frames per device card**;
0.4-0.6 MB per 1024-px frame → 0.5-0.8 TB per card; the 20 TB volume holds ~25-40 card-corpora.
Warp cost: PolyPose forward on a 512×512×600 grid is tens of seconds on one GPU plus ~1-2 min
of checks; 1,360 outputs × 3 seeds is a few GPU-days on one card, hours on 16 H200s — to be
replaced by the measured number.

Film-level caveat: against the 30 real BUU L6 films the existing physics_rare bank already
holds 845 L6 crops (28:1), so a literal 10:1 per real rare film cannot be honoured without
discarding renders; the real-film lever is the 4× epoch oversampling, applied unchanged.

**Measured arm:** train with and without the PolyPose variants at identical real-frame content
and epoch counts; per-class recall, PR-AUC and common-class precision on real held-out C-arm
frames, paired bootstrap; reported either way — nobody has ever measured anatomical-variant
augmentation [ratio_report].

## 14. Seeding and the manifest row

master_seed 20260923; per-variant seed = int(sha256(f"{master_seed}|{source_patient_key}|
{variant_index}").hexdigest()[:16], 16); rng = numpy PCG64. Draw order is part of the spec (a
row is reproducible): PI measured, not drawn → (LL\*, TK\*, SS\*) | PI as one draw →
supine offsets → Roussouly type from SS\* → T10-L1 share of dTK → per segment cranial to
caudal (sagittal, lb, ar).

Every output keeps its source patient key and is reproducible from its manifest row
(41 fields, `sampling_spec.json:manifest_row`): source case/collection/patient key, variant
index, seed, subtype, Castellvi grade, junction multipliers, rigid-body lists, the drawn
standing and supine profiles, the supine offsets, Roussouly type, per-segment requested and
clipped deltas with shortfall, lb/ar draws, PolyPose commit, env hash, sha256 of output CT /
label / body mask, the re-measured `measure_sagittal.py` row, every check and envelope result
with values, rejections before accept, and the source's plate-sanity gates.

## 15. Automatic invariants (exit non-zero on any failure)

1. **Jacobian** > 0 at every voxel (`Warp.jacdet`); tolerance 0.
2. **Per-vertebra Dice** ≥ 0.98 against the rigidly transformed original label (NN resampling
   of a rigid motion is the noise floor).
3. **Fused junction**: multiplier-0 bodies carry identical se(3) parameters to the sacrum;
   re-measured junction change ≤ 0.25°.
4. **Pelvis**: |ΔPI| ≤ 0.5°, same for SS and PT.
5. **Lordosis**: |dLL_measured − dLL_clipped_request| ≤ 2.0° (noise floor measured at 0.5°).
6. **Thoracolumbar**: |dTLK_measured − requested| ≤ 2.0°, both TL_T11-L1 and TLK_T10-L2 moving
   in the requested direction.
7. **Wedge**: per-body wedge unchanged within 0.5° (rigidity).
8. **Junction share**: junction angle moves by share_L5S1(type\*) × dLL within 2°; ≤ 0.25°
   when fused.
9. **Body mask** warped through the same field (NN); Dice vs re-run mask ≥ 0.95.
10. **Render**: one AP + one lateral DRR per output with the bone term present
    (`make_drr_dataset --paths2-only`); bone-pixel fraction within the source's range; every
    vertebra's projected box non-empty.
11. **Envelope before render** (§11), every rejection recorded.
12. **Source sanity** (§11) before any warp.
13. **Population**: KS test of supine LL, TLK and junction angle against the supine-converted
    model per PI bin; SDs beside the model SDs; Roussouly type shares beside laouissat2018 /
    shen2024.

## 16. Environment

Pinned env "polypose" from the repository's requirements at commit `909a9bb2` (uv `--frozen`);
export = conda `--no-builds` + pip freeze into the run directory, env_hash = sha256 of both.
Grid modules `apptainer/1.2.2` / `singularity/3.5.2` (no `/usr/bin/singularity` — that killed
the earlier prep). GPU nodes gvohp/galhp (cupy needs one). No network at run time; everything
staged. Outputs `/rs/rs_grp_oschome/go2432/data/polypose/`. Labels never reoriented on write;
axcodes read and recorded. Cohort measurement env: grid spineps python 3.11.16, numpy 2.2.6,
scipy 1.15.3, nibabel 5.4.2.

## 17. The cohort, measured (one code path, on the grid)

Array 40416793 + reduce 40416794 (third attempt; the first died in 3-6 s on the sbatch
environment, the second ran the release script from a stale tree whose
`extract_surgical_morphometrics` predated the sacral-plate fix and was cancelled). 1,176 rows:
973 measured, 203 refused — VerSe unified masks in the legacy map (L1=1) are **refused rather
than measured against the wrong map**. Code `tools/polypose/measure_sagittal.py` +
`cohort_reduce.py` (grid), `cohort_sagittal.py` (local clouds/envelopes/outside checks).
Outputs: `cohort_sagittal.{json,png}` (the PI-LL and TK-LL clouds with published envelopes,
SS-PT on PI isolines, the segmental profile; transitional cases marked, fused junctions
ringed).

Findings (full statistics in `sampling_spec.json:cohort_measurement`):

- PI, SS, PT reproduce the release CSV to 0.0° (consistency, not truth) and Veilleux's
  automated supine CT to < 0.1° on all three (n=200; truth outside the computation)
  [veilleux2020].
- Per-level means match the published standing profile after the supine shift (L3-L4 9.9,
  L4-L5 14.4, L5-S1 23.7 vs shares × LL: 9.2 / 12.9 / 21.8 [milele2022]) but every per-segment
  SD is 1.5-2× the widest published series and the LL SD is 1.24× MEANS. **Spread is the
  finding**; the sampler takes its shape from the literature, not from the cohort.
- The standing TLK-LL coupling (R² 0.20 [pan2024]) is absent supine (r = −0.03, n=648).
- T9, the field-edge body, is unusable (wedge −8.9 ± 16.2): the topmost in-field body is
  excluded from the mobile chain and every check.
- L6 PI 60.9 vs ordinary 52.0 vs sacralised 47.9: the published class association of PI is
  present in this cohort [yokoyama2016, haffer2021, muller2024].
- 66.5 % of ordinary spines sit inside Schwab |PI−LL| < 10 and 95.4 % inside 20; 72 % have
  PT < 20; 61 / 26 / 13 % are Roussouly 1-2 / 3 / 4 by supine SS − 3.9.

Defects found and their disposition: the T9 field-edge defect (a half body passes MIN_VOX);
15 cases with |junction disc| > 30° and 14 with broken TLK or LL plate fits — excluded as
sources, rows flagged, **not fixed**; 203 VerSe legacy-map scans refused (the bank build must
resolve both maps through `ostk.labels.labels_for` or those scans cannot be warped); the
supine LL offset sign disagreement (§4) is drawn, not assumed.

## 18. What is not known

Stated plainly, per the house rule:

1. No published series gives a per-type Roussouly LL mean with an SD; the consistency gate
   uses table corners, not a distribution.
2. The SS-TK correlation is not published as a pair; 0.35 is an assumption (checked only
   through positive definiteness and the outside checks in §3.4).
3. The Lafage 2011 PT coefficients were seen only in secondary quotations; the spec cites the
   abstract's r and SE and uses the coefficients for nothing.
4. No paper predicts LSTV from spinopelvic angles ALONE with a stated AUC; the closest are
   albano2020 (segmented lordotic angles, AUC 0.665-0.831 by type) and dl_radiograph2025
   (image-based, AUC 0.84). Geometry is weakly informative; the count must be learned.
5. No published segmental ROM exists for six-lumbar or thirteen-thoracic spines; the anchoring
   rule (§9) is a stated decision.
6. Whether the standing TLK-LL coupling should be imposed on a supine source at all: the
   cohort says it is absent supine.
7. The T9 field-edge defect and the 29 plate-fit failures are excluded, not fixed.

## References

Every key used above. Verification status is quoted from `sampling_spec.json:citations`;
"earlier session's reading" means the paper's identity was confirmed against PubMed on
2026-09-23 but the specific table values were carried over without a same-day re-read.

| key | citation | verification |
|---|---|---|
| albano2020 | Albano D et al. Segmented lordotic angles to assess LSTV on EOS. Eur Spine J 2020;29(10):2470-6. PMID 32783082, doi 10.1007/s00586-020-06565-7 | abstract read verbatim 2026-09-23 |
| banitalebi2026 | Banitalebi A et al. Clin Spine Surg 2026;39(2):E104-11. PMID 40298377 | citation confirmed; +0.9 from earlier reading |
| barrey2011 | Barrey C, Roussouly P, Perrin G, Le Huec JC. Eur Spine J 2011;20 S5:626-33. PMID 21796393 | abstract read verbatim; mechanism list quoted |
| bernhardt1989 | Bernhardt M, Bridwell KH. Spine 1989;14(7):717-21. PMID 2772721 | abstract read |
| bouaicha2014 | Bouaicha S et al. Biomed Res Int 2014:967178. PMID 25003134 | verified; sign of group-B offset NOT established |
| castellvi1984 | Castellvi AE, Goldstein LA, Chan DP. Spine 1984;9(5):493-5. PMID 6495013 | citation, title and pages confirmed via PubMed 2026-09-23; type definitions per Konin & Walz (on disk) |
| chen2019 | Chen HF et al. J Orthop Surg Res 2019;14:13. PMID 30630533 | verified; 44.97 ± 8.52 is a pooling of two printed strata |
| cheng2022 | Cheng L et al. J Clin Med 2022;11(9):2339. PMID 35566465 | full text read |
| chevillotte2018 | Chevillotte T et al. OTSR 2018;104(5):565-8. PMID 30009961 | abstract read verbatim |
| chung2020 | Chung NS, Lee HD, Jeon CH. Spine Deform 2020;8(2):227-32. PMID 31925766 | citation confirmed; shares from earlier reading |
| diebo2015 | Diebo BG et al. Clin Neurol Neurosurg 2015;139:295-301. PMID 26562194 | citation + abstract confirmed |
| dl_radiograph2025 | Kwak D, Ro DH, Kang DH. Automated detection of LSTV on plain lumbar radiographs (deep learning). J Clin Med 2025;14(21):7671. PMID 41227066, doi 10.3390/jcm14217671 | abstract read verbatim 2026-09-23; AUC 0.84 confirmed |
| fan2023 | Fan X et al. Front Surg 2023;10:1103952. PMID 36911604 | abstract read verbatim; all three offsets match |
| haffer2021 | Haffer H et al. Diagnostics 2021;11(1):59. PMID 33401698 | tables read |
| hasegawa2018 | Hasegawa K et al. BMC Musculoskelet Disord 2018;19:437. PMID 30522465 | design confirmed; offsets from earlier table reading |
| hyun2019 | Hyun SJ et al. Eur Spine J 2019;28(9):1906-13. PMID 30903294 | citation confirmed; formula from earlier reading |
| izatt2012 | Izatt MT et al. Scoliosis 2012;7:15. PMID 22913616 | verified; the supine equation is NOT in the abstract |
| jacob2023 | Jacob AM et al. Am J Neurodegener Dis 2023;12(4):123-32. PMID 37736164 | abstract read |
| karabag2024 | Karabag H, Iplikcioglu AC. World Neurosurg 2024;183:e900-8. PMID 38218445 | abstract read |
| konin2010 | Konin GP, Walz DM. AJNR 2010;31(10):1778-86 | on disk (MANUAL_REFS/KONIN_WALZ.pdf) |
| korean2020 | Park JH, Kim YB, Hyun SJ, Kang KB, Park PS. Asian Spine J 2020;14(2):192-7. PMID 31575109, doi 10.31616/asj.2019.0060 | full text read 2026-09-23; T10-T12 by decade 9.5 / 12.9 / 12.2 verbatim |
| kuoppala2025 | Kuoppala A et al. Int Orthop 2025. PMID 40801985, PMC12488840 | full text read |
| lafage2011 | Lafage V et al. Spine 2011;36(13):1037-45. PMID 21217459 | citation confirmed; coefficients secondary-quoted, unused |
| laouissat2018 | Laouissat F, Sebaaly A, Gehrchen M, Roussouly P. Eur Spine J 2018;27(8):2002-11. PMID 28455623 | 3AP definition confirmed; per-type rows from earlier reading |
| lee2016 | Lee SK et al. Clin Orthop Surg 2016;8(1):65-70. PMID 26929801 | abstract read |
| mahato2011 | Mahato NK. Spine J 2011;11(10):961-5. PMID 21924685 | no PI/LL values; Mahato 2019 (PMID 30805281) is FE ROM |
| milele2022 | Mi Le JR et al. Sci Rep 2022;12:18965. PMID 36347920 | abstract read |
| muller2024 | Muller JA et al. J Anat 2024;244(4):594-600. PMID 38030157 | confirmed; supersedes the muller2023 key |
| ouchida2024 | Ouchida J et al. Eur Spine J 2024;33(8):2952-9. PMID 38922415 | citation confirmed; PI values from earlier reading |
| oxland1992 | Oxland TR, Lin RM, Panjabi MM. J Orthop Res 1992;10(4):573-80. PMID 1613631 | abstract read verbatim (both segments, four directions, with SDs) |
| panjabi1991 | Panjabi MM et al. Spine 1991;16(8):888-901. PMID 1948374 | Table 3 read by eye (image-only scan); morphometry, not ROM |
| panjabi1992 | Panjabi MM et al. Spine 1992;17(3):299-306. doi 10.1097/00007632-199203000-00010 | Table 2 read by eye |
| pearcy1984a | Pearcy M, Portek I, Shepherd J. Spine 1984;9(3):294-7. PMID 6374922 | abstract read verbatim |
| pearcy1984b | Pearcy MJ, Tibrewal SB. Spine 1984;9(6):582-7. PMID 6495028 | abstract read verbatim |
| peterson1995 | Peterson MD et al. Spine 1995;20(12):1419-24. PMID 7676342 | abstract read |
| polypose | Gopalakrishnan V, Dey N, Golland P. NeurIPS 2025. arXiv:2505.19256, PMID 40492249. MIT, commit 909a9bb2 | source code read through the GitHub API |
| ratio_report | reports/Synthetic real ratio X-ray detectors.md, this repo | internal, measured |
| roussouly2005 | Roussouly P, Gollogly S, Berthonnaud E, Dimnet J. Spine 2005;30(3):346-53. PMID 15682018 | confirmed; abstract does not print the SS thresholds |
| sardar2022 | Sardar ZM et al. (MEANS). Spine 2022;47(19):1382-90. PMID 35797462 | abstract read verbatim (alias: means2022) |
| shen2023 | Shen Y et al. Spine 2023;48(11):758-65. PMID 36944088 | abstract read |
| shen2024 | Shen Y et al. Global Spine J 2025;15(2):1295-1305. PMID 38417069 | every value confirmed verbatim from PMC full text |
| tini1977 | Tini PG, Wieser C, Zinn WM. Rheumatol Rehabil 1977;16(3):180-5. PMID 143714 | prevalence only; no angles |
| tu2023 | Tu Z et al. Quant Imaging Med Surg 2023;13(3):1375-83. PMID 36915337, doi 10.21037/qims-22-365 | four type definitions read verbatim 2026-09-23 (PMC) |
| veilleux2020 | Veilleux NJ et al. JBJS Am 2020;102(17):e130. PMID 32881722 | all three values confirmed verbatim |
| vialle2005 | Vialle R et al. JBJS Am 2005;87(2):260-7. PMID 15687145 | abstract read |
| vrtovec2012 | Vrtovec T et al. Spine 2012;37(8):E479-85. PMID 21971132 | verified; the inline "Eur Spine J" attribution was corrected |
| wang2022 | Wang J et al. Front Surg 2022;9:912357. PMID 36248369 | full text read; Tables 1 and 4 quoted verbatim |
| weng2025 | Weng R et al. Front Bioeng Biotechnol 2025. doi 10.3389/fbioe.2025.1700758 | full text read; single-subject FE, not used as a bound |
| whitepanjabi1990 | White AA, Panjabi MM. Clinical Biomechanics of the Spine, 2nd ed. 1990 | **NOT verified**; listed secondary, not used |
| wilke2017 | Wilke HJ, Herkommer A, Werner K, Liebsch C. PLoS One 2017;12(5):e0177823. PMID 28520819, doi 10.1371/journal.pone.0177823 | citation + DOI confirmed 2026-09-23; T10-T11 recomputed 2026-09-26 from the S1 Dataset per-specimen rows (per direction) |
| yamamoto1989 | Yamamoto I, Panjabi MM, Crisco T, Oxland T. Spine 1989;14(11):1256-60. PMID 2603060 | abstract read verbatim (all five segments, four directions) |
| yan2022 | Yan YZ et al. Orthop Surg 2022;14(2):341-8. PMID 34935276 | group sizes confirmed verbatim; per-group means paywalled |
| yokoyama2016 | Yokoyama K et al. Eur Spine J 2016;25(11):3583-8. PMID 26482498 | abstract read |
| yukawa2018 | Yukawa Y et al. Eur Spine J 2018;27(2):426-32. PMID 27771788 | every value confirmed verbatim (supersedes yukawa2017 key) |

Superseded keys kept so old rows resolve: means2022 → sardar2022, muller2023 → muller2024,
yukawa2017 → yukawa2018. Additional context sources not load-bearing: boisvert2008 (scoliotic
pose variability), lee2016 / peterson1995 (intraoperative prone lordosis), mahato2011,
tini1977.
