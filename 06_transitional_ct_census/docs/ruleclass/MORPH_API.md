# MORPH_API: the morphology the SUPER DETECTOR RUN can measure, and what has to be added

Written 2026-09-27 for the RULECLASS / SUPER DETECTOR RUN workflow (two arms: A = TotalSegmentator; B = SPINEPS +
VERIDAH + Möller ribs + Dataset803 pelvis only). Read-only survey of `OpenSpineToolkit/ostk` (local HEAD cb43197),
the reader E extractor (`spinesurg-ct-nnunet/SchwingNet/tools/reader_e_features.py`, schema v3, 65609fd), reader C
(`tools/rib_count_reader.py`), `tools/tp_morphology.py`, the CTSpinoPelvic1K extraction scripts, Möller's
`rib-segmentation` repository (read on GitHub today), Schinz 2026 (full text on disk) and the Lee 2019 case report.
Every "verified" below was run or read today; everything else is marked as not checked.

## 0. The short version

1. **ostk measures the vertebral BODY and CANAL only**: VBHa/VBHp, EPWu/EPWl, EPDu/EPDl, SCW/SCD, PDW (pedicle),
   plus Genant six-point ratios when corners are supplied. It has **no** transverse-process, facet, costal-facet,
   pedicle-angle, sacral-dimension or rib function. Body and canal measures encode POSITION more than identity
   (T12 vs L1: end-plate width d = 0.14, canal depth d = 0.00, per `tools/tp_morphology.py` docstring).
2. **Do not call ostk `level_morphometry` directly on the corpus.** The grid copy (and local HEAD) still carry the
   1b7005c ring-closing defect: VBHp and EPD inflated 10-17 mm on about one vertebra in seven, SCD collapsing
   onto an interlaminar pocket (15.8 % of J1 instances under the 11.07 mm floor vs 2.62 % published). Reader E's
   `ostk_level()` wraps ostk with the closed-ring-column body cut and canal (verified within 0.36-1 mm of the release
   rows on 0097/0234/1138). **The J1 v3 per-instance table already exists on the grid** (below); use it.
3. **What separates a thoracic from a lumbar vertebra is on the posterior arch, not the body.** Schinz et al. 2026
   (Eur Spine J 35:2195; `SchwingNet/lit/ct_lstv_classifier/sources/schinz2025_*.txt`) score three features:
   (I) superior-facet-joint (SFJ) orientation, (II) position of the transverse/costal process relative to the SFJ,
   (III) a costal fovea on the body. Their Fig. 3D is exactly Greg's case: a rib-less vertebra with thoracic SFJ and
   transverse processes is T12, and counting it as lumbar produces a false 11/6.
4. **SPINEPS already segments the parts those criteria need** (TPTBox `Location`, verified in the grid spineps env):
   41 arcus, 42 spinous, **43/44 costal (transverse) process L/R, 45/46 superior articular process L/R, 47/48
   inferior articular process L/R**, 49 corpus border (the body), 50 corpus, **52/53 body end-plate superior/
   inferior**, 100 disc, and the sacrum's own subregions **70/71 sacral ala L/R, 72 posterior sacral elements,
   73 sacral body, 74 sacral end-plate**. These live in every harvested `*_seg-spine_msk.nii.gz` (Arm B inputs).
   Nothing in any repository reads 45-48, 52/53 or 70-74 yet.
5. **A three-case probe says the SFJ and costal-process features work on SPINEPS masks** (section 6.3): averaged
   over the two sides, T10-T12 joints read 72-83 degrees from sagittal and L1-L4 joints 21-47; the costal process
   sits 5-8 mm posterior of the superior articular process at T9-T12 and 2-6 mm anterior on lumbar bodies. On CTSP
   0005 (read L6) VERIDAH names a "T13" whose joint and process are lumbar-shaped, which is what the read says it is
   (L1 of a six-lumbar spine). Three cases, not rendered: a feasibility signal, not a result.
6. **The "bimodal last-rib ratio" Greg remembers is CTSpinoPelvic1K's own finding**, not (as far as any file shows)
   Möller's: rib 12 / rib 11 length has modes near 0.68 and 0.32, 67 cases below 0.30 (`docs/LAB_JOURNAL.md` l.77),
   with the scan-edge truncation check still listed as blocking (l.149-152). Möller's code defines a stump by absolute
   path length: `stump_rib_threshold_in_mm = 38.0`.
7. **T13 is not decidable in an abdominopelvic field.** Without T1 the rib-bearing count is unknown, so a stump rib
   on a thoracic-shaped body followed by five lumbar-type bodies is either a hypoplastic 12th rib (12.6 % of whole-
   spine CTs, Nagata 2025) or a T13 (0.37 % CT, Doo 2020). Only whole-cage CTs (VerSe whole spine, TS whole body)
   can call T13; everywhere else it is a candidate with its prior stated.

---

## 1. Label maps and loaders (the trap that has shipped three times)

`ostk.labels.labels_for(volume)` decides between the legacy v4 map and the release v10 map **by pelvis voxel mass
under each hypothesis** (ids 9-12 vs 30-33). It is correct for CTSpinoPelvic1K release volumes and **wrong, silently,
for every other family**. Verified today on synthetic masks with the local ostk:

| mask family | what `labels_for` does | consequence |
|---|---|---|
| CTSP v11 release | returns `LABELS_V10` (v11 = v10 with 29 dissolved into 26) | correct; but `L["S1"]` is 29, which is empty on v11 |
| VerSe / SPINEPS whole-spine (VerSe alphabet; T2-T5 = ids 9-12 present) | **returns "v4"**: `L["sacrum"]` = 8 (= T1), `L["L1"]` = 1 (= C1) | finite, plausible, wrong bone; no error |
| Dataset803 prediction (1-4 L1-L4, 5 last_lumbar, **6 sacrum, 7 left_hip, 8 right_hip**) | no pelvis under either map, returns default v10: `L["sacrum"]` = 26, absent | every sacrum lookup empty; callers return None quietly |
| TotalSegmentator `total` (lungs at 10-12, hips 77/78) | raised `SchemeError` on my synthetic volume; on a real volume it can equally pick "v4" (sacrum = 8 = adrenal gland right) | raise or wrong organ, depending on voxel counts |

Rules for the run (reader E's loader table, `CT_LSTV_CLASSIFIER_PLAN.md` section 4, already implements 1-4):

1. **CTSP release:** `labels_for(lab)`, then assert id 29 absent, sacrum 26 mass > 0, hips 30/31 present. Never ask
   for `"S1"` on v11: `spine.endplate_from_label(..., "S1")` silently falls back to the whole sacrum, whose surface fit
   the docstring itself says drives PI "far too low"; the S1 plate is `extract_surgical_morphometrics._sacral_plate`
   (the plate under the lowest lumbar footprint) or SPINEPS 74 (below).
2. **SPINEPS vert mask:** `tools/spineps_ids.assert_verse_monotonic(img, ctd=<ctd.json>)` (raw pre-147428d trees carry
   ids 1..N); then the VerSe alphabet directly: C1-C7 1-7, T1-T12 8-19, L1-L6 20-25, sacrum 26, coccyx 27, T13 28.
   **Disc instances are 100 + X where X is the vertebra ABOVE the disc** (checked on 0001/0005/0097 today: 124 sits
   under L5, 120 under L1, 128 under T13). Semantic subregions as in section 0 point 4. Never `labels_for`.
3. **TotalSegmentator:** the run's own `class_map.json`; vertebra instances = `vertebrae_*` except `vertebrae_S1`;
   **sacrum = `sacrum` UNION `vertebrae_S1`** (disjoint in TS v2); TS has no L6, no T13, no 13th or lumbar rib class.
4. **VerSeFusion / CTSpine1K expert masks:** VerSe alphabet, **no sacrum id**: sacrum features NaN with a mask bit.
   Whole-spine counts read the raw VerSeFusion masks (25 = L6, 28 = T13), not the 813 renders; the manifest's
   `has_T13` is wrong (18 claimed, 6 true).
5. **Dataset803 (Arm B's caudal anchor):** read its own map (`NextPaper/spinopelvic-seg/tools/convert_hf_to_nnunet.py`
   `LABEL_NAMES`): keep **6 -> 26 sacrum, 7 -> 30 left_hip, 8 -> 31 right_hip**, drop 1-5 (last_lumbar 5 is L5+L6
   merged). Only after that remap may ostk be called, and `labels_for` on the remapped array then doubles as the
   self-check (it must return v10 with hip mass > 0). If the prediction grid differs from the SPINEPS grid, resample
   the prediction (nearest) onto SPINEPS for ANALYSIS; never write a reoriented or resampled label.
6. **Always:** `nib.as_closest_canonical` for analysis only; `str(case).zfill(4)` before joining CTSP rows; id 29
   is retired and any gate on it is a bug; lumbar-rib ids are 60/61 in v10/v11 but **74/75 in the older scheme that
   `docs/SPINEPS_BENCHMARK.md` l.106 still cites**; resolve per volume.

---

## 2. What ostk measures per vertebra

All in world millimetres through the affine; `level_morphometry(label, affine, level_id: int)` takes an INTEGER id,
so the caller resolves the id per family (section 1).

| function (`ostk/...`) | returns | definition | status / trap |
|---|---|---|---|
| `vertebral_body.body_mask` | bool body | canal found as a per-section topological hole (after a 2 mm ring closing), body = mask anterior to the canal's anterior edge per section; watershed on the distance transform as fallback | **1b7005c defect**: the closing creates a pocket between the laminae 14-15 mm behind the wall on 2-3 sections below the pedicles; every section below inherits it; pedicle roots and inferior articular processes become "body". `min_vox=20` also admits 3 mm "canals". Unfixed in ostk; fixed in reader E (`canal_column_hole` + `body_from_hole`: hole >= 18 mm2, centroid within 8 mm of the column axis, wall within 8 mm of the median wall, longest run) |
| `vertebral_body.endplate_corners_body` | (anterior, posterior, rms, n) per plate | RANSAC plate on the body's disc-facing surface, re-fitted to the rim, robust quadratic profile, corners = plate tangent x cortical wall (Frobin), bounded to 8 mm outward | the rms is the only gate; it cannot see that the wrong points were chosen (docstring, 0003 L1) |
| `morphometry.vertebra_frame` | {ap, sup, lat} | AP = mean of the two plates' anterior-posterior chords; sup = world superior orthogonalised; lat completes | frame of the vertebra, not the scanner; `lr` fixes only the sign |
| `morphometry.body_heights` | VBHa, VBHp | corner-to-corner wall heights | VBHp inherits the body-cut defect |
| `morphometry.endplate_dimensions` | EPD, EPW per plate (u/l) | EPD = corner chord; EPW = lateral extent of body points within +-3 mm of the plate, in the plate's own left-right | **EPW at L5 (often L4) includes the transverse-process shoulders** (70-86 mm vs 50-60): withheld > 60 mm and on the two lowest presacral bodies; the J2 v3 gate fails EPWl (ts L1/L2 41-43 % flagged) for lack of a LOWER-plate yardstick; EPD has no published SD on file |
| `morphometry.canal_dimensions` | SCW, SCD | SCW = median transverse width per section over the central half of the closed-ring column; SCD = median midsagittal chord on a +-1.5 mm strip | the ostk version reads its slab on `canal_mask`'s solid (pocket-contaminated); reader E replaces it with `canal_from_column` and keeps ostk's as `SCD_ostk` |
| `morphometry.pedicle_widths` | PDW l/r/mean | isthmus = least-area section perpendicular to the pedicle's PCA axis inside Kumar's initial pedicle region; PDW = transverse extent of that section | 30-60 s per level (SDF resample to 0.35 mm); **assumes array axis 2 = superior and axis 0 = left-right** (`_fill`, the `for k in range(V.shape[2])` loop, `lat_dir = [1,0,0]`), so it is only valid on an RAS-canonical array; never populated in the 2026-09-10 shard run; L5 withheld in the release |
| `morphometry.level_morphometry` | all of the above | drops the level if < 200 voxels, body < 100, or plate rms > 2.0 mm | direct use carries the 1b7005c defect |
| `genant.six_points / heights / ratios / wedge_angle / genant_grade` | Ha, Hm, Hp, Ha/Hp, Hm/Hp, wedge angle, grade | from four supplied corners (middles constructed) | corners from a mask are post-osteophyte: `pre_osteophyte=False`, never compared with Genant norms |
| `spine.fit_endplate` / `endplate_from_label` / `pi_anchor_point` | plate plane / anchor | "corner" for vertebral bodies, "surface" for S1/sacrum | surface fit is bimodal (28.3 % on the ventral sacral ramp, SPINOPELVIC_ESTIMATOR); `endplate_corners_anatomic` raises `NameError: return_rms` on every call (verified today; no caller) |
| `metrics.*_from_label` | PI/SS/PT/LL | femoral-head axis as patient left-right | spinopelvic, not morphology; v11 needs femurs 32/33 |

**How to call it on one CTSP v11 volume** (analysis only; nothing written):

```python
import nibabel as nib, numpy as np
from ostk.labels import labels_for, LABELS_V10
from ostk.morphometry import level_morphometry
img = nib.as_closest_canonical(nib.load(path))            # RAS for ANALYSIS; never nib.save(img)
lab, A = np.asarray(img.dataobj).astype(np.int32), img.affine
L = labels_for(lab)                                       # raises SchemeError when ambiguous
assert L is LABELS_V10 and not (lab == 29).any() and (lab == L["sacrum"]).any()
r = level_morphometry(lab, A, L["L1"])                    # carries 1b7005c: prefer reader E below
```

**The preferred path** is reader E, one (CT, mask, family) pair per call, name-free, every value with a spread bit:

```
python SchwingNet/tools/reader_e_features.py --ct CT.nii.gz --mask LABEL.nii.gz \
    --family {v11|spineps|ts|versefusion|ctspine1k} [--ctd CTD.json] [--class-map class_map.json] \
    --out-json out/features.json --out-png-prefix out/render
```

Median 34.5 s per pair (J1: mean 54.6, max 517; 12 whole-spine VerSe pairs need 32 GB). **Already computed on the
grid**: `/rs/rs_grp_oschome/go2432/data/or_ready/auto_reference/readerE/j1v3/_collect/features_j1.csv` (38,432
instance rows x ~194 columns; 3,524 pairs: v11 802, spineps 1,169, ts 1,176, versefusion 374, ctspine1k 3). J2 v3
(40448877): SCD passes; EPWl fails (lower-plate yardstick missing); EPDu/EPDl have no published SD; J3 not submitted.
Per instance it carries: centroid, ml, S-I/L-R/A-P extent, partial/tiny/merged flags, rib chords left/right from
reader C's CT trace (`rib_*_trace_chord_mm`, `_is_rib`, `_stump`, `_cut`), `rib_bearing_trace`,
`pos_from_plateau_inst` and `pos_from_last_rib_inst` (name-free positions), spacing ratios, TP reach/thickness/
slenderness (tp_metrics), VBHa/VBHp/EPWu/EPWl/EPDu/EPDl/SCW/SCD/wedge ratio/body ml with range bits, and a junction
block (TP tip height and gap, TP-ala contact area, disc heights, ala rise, iliac crest level, S1-S2 gap proxy).
**What it does not carry**: facet orientation, transverse-process position relative to the facet, costal fovea,
SPINEPS subregions of any kind, sacral dimensions, Möller rib lengths.

---

## 3. Other per-vertebra measures already in the repositories

| measure | code | definition | trap |
|---|---|---|---|
| TP reach, thickness, slenderness, AP / SI spread per side | `spinesurg-ct-nnunet/tools/tp_morphology.py` `tp_metrics` | reach = 99.5th pct lateral distance minus the body half-width (97th pct of the anterior third); thickness = sqrt(area) of the root slab; slenderness = reach/thickness (lumbar blade high, thoracic club low) | the "anterior third" is taken by raw index with no A-P sign: on an RAS array it is the arch (reader E flips to P-first); invalid when body_half >= 30 mm (0097 L6: 48.9 mm, the TPs are anterior), i.e. exactly at the lowest lumbar |
| TP span tip to tip | `CTSpinoPelvic1K-1/scripts/extract_level_gradients.py` (`level_gradients.csv` `tp_span_<L>_mm`) | left-right extent of the largest component along array axis 0 of the canonical volume | scanner axis, not the vertebra frame; it was the dominant feature of `scripts/test_morphometric_separability.py`: logistic regression on case-median-normalised shape features, grouped CV, T12 vs L1 AUC 0.990, accuracy 97.3 % (`docs/LSTV_BENCHMARK.md` l.20-26) - on T12s that all carry ribs |
| TP craniocaudal height (Castellvi I >= 19 mm), TP tip-to-sacrum and tip-to-ilium gap, lowest-lumbar lateral span | `extract_transition_morphometrics.py` one() l.351-410 (`transition_morphometrics.csv`, `tp_height.csv`) | tip = lateral 12 mm; height of the largest tip component | fixed v10 ids (20-25, 26, 29, 30/31); the minimum-distance history (a "gap" that measured the facet joint) is in its docstring |
| costal-process height and contact with the sacrum from SPINEPS 43/44 | `tools/harvest_cobra.py` l.219-246 | height of 43/44 inside the lowest lumbar instance; gap = EDT to sacrum | the one existing reader of SPINEPS subregions; COBRA only |
| body masks from SPINEPS 49/50 | `tools/body_masks.py` | corpus border + corpus inside each instance | the LEVEL_MORPHOMETRY "still open" route to an end-plate width without TP shoulders; 52/53 end-plates are unused |

---

## 4. The sacrum: what exists and what must be added

Conventions differ by family, and the sacral-shape rule depends on them: **CTSP v11 puts a fused L5 inside sacrum 26**
(the 9 LS-SAC reads); **VerSe leaves a fused body unlabelled**; **TS `sacrum` excludes S1 and can absorb an L6**
(v11 vs TS rib-based count agreement on the 34 read CTSP records is 39 %, reader E J1); **SPINEPS can swallow the lowest mobile body**: on CTSP
0005 (read L6) its "L5" is an 810-voxel fragment, the sacrum instance starts 8 mm above the fragment's top, and disc
124 (L5-S1) lies inside the sacrum's S-range. On CTSP 0001 SPINEPS's sacrum instance also holds a stray piece at the
top of the field (S -70 mm, about 290 mm above the sacral plateau, with a disc 126 under it), so **every sacral measure takes the component
under the lumbar column, never the whole instance**. Dataset803's sacrum was trained on CTSP labels and so carries the
CTSP convention (fused L5 inside).

| measure | exists? | where / definition | trap |
|---|---|---|---|
| S1 superior plate (orientation, anchor) | yes | `extract_surgical_morphometrics._sacral_plate` (columns under the lowest lumbar body's footprint, then a height bound); ostk `endplate_from_label("S1")` falls back to the whole sacrum on v11; **SPINEPS 74 = sacral end-plate** (3.9-8.5 k voxels on the three probe cases) | the ostk surface fit is bimodal (28.3 % land on the ventral ramp) |
| sacral width / height / aspect | yes, weak | `transition_morphometrics.csv` `sacrum_width/height/aspect` and `surgical_morphometrics.csv` `sacral_width_mm/height_mm/width_ratio`: bounding extents along array axes | scanner axes; height includes more than the sacrum inferiorly (label runs to 140 mm on 105-115 mm sacra, `extract_pelvic_shape.py` l.105) |
| sacral base (ala-to-ala) width | yes | `pelvic_shape.csv` `sacral_base_width_mm`: left-right extent of the top 15 % of the sacral voxels by scanner z | scanner z, not the S1 level; **SPINEPS 70/71 give the alae directly** |
| ala rise per side | yes | `measure_sacral_ala.py` (vendored in reader E `ala_rise`): top of the lateral third minus top at the midline, anterior half only | the whole-depth version measured the S1 superior articular process (AUC 0.450) |
| TP-ala contact area, TP tip gap | yes | reader E junction block (EDT of the sacral complex, tip voxels within 1.05 voxel, x face area) | contact area in a named site, not a minimum distance |
| L5-S1 disc presence and height | yes | reader C `class_contact` / `runs_contact` (joined vs disc in a 14 mm cylinder; TS masks); `_disc_height_mm` (columns through the central plate; `disc_low_mm`, `disc_ratio`); **SPINEPS disc instance 100+X under the lowest lumbar X** | a near-zero disc also arises from surgical or osteophytic fusion |
| sacral foramina per side | yes, weak | `extract_transition_morphometrics.count_foramina` (8 mm coronal slab slid A-P, holes 8-700 mm2, max over slabs) | documented 0/0 and 4/3 on normal sacra: never a gate |
| S1-S2 gap (immaturity) | yes | reader E `immaturity_proxies` in the sacral occupancy profile | proxy only |
| **number of fused segments** | **no** | ADD: a 1-mm profile along the sacral midline curve inside SPINEPS 73 (sacral body) or the sacral mask, reading mean HU and the anterior-cortex contour; vestigial discs are low-HU bands / anterior notches; count bands between the plate and the apex (normal 4 between 5 segments) | a six-segment sacrum can come from Co1 fusion as well as L5: report where the extra segment sits (top vs bottom) |
| **S1 body width / depth / height in the sacrum's frame** | **no** | ADD: frame from the S1 plate normal (SPINEPS 74 or `_sacral_plate`); width = extent of 73 within +-3 mm of the plate along the plate's left-right; depth = plate corner chord; height = plate to the first vestigial disc | a fused L5 moves the "S1" plate up one segment: its width then matches the presacral body's inferior plate, the discriminating ratio |
| **top-plate width / lowest presacral inferior-plate width** | **no** | ADD: EPW of 74 (or the plate) over EPWl of the lowest presacral body (reader E morph) | EPWl has no published yardstick; this is a within-person ratio, which removes that problem |
| **sacral length along the curve, curvature** | **no** | ADD: arc length of the midline curve from the plate to the apex, over the lowest presacral body height; angle between the S1 and S3 segment axes | the mask's inferior extent is unreliable (above) |
| **lumbosacral angle** | **no** | ADD: angle between the S1 plate and the lowest presacral inferior plate (disc wedge) | a sacral-table-type angle exists in the literature; no source in the repo, so no threshold is quoted |
| **sacrum instance absorbed a mobile body** | **no** | ADD (SPINEPS): a disc instance (100+X) or a low-HU disc band lying between sacral voxels above and below it; the 0005 signature | a render per positive |

---

## 5. Ribs

**Möller / Hendrik toolchain (Arm B)**, read on GitHub today (`github.com/Hendrik-code/rib-segmentation`):

- `run.run_all_steps(rib_mask, vertebra_instance_mask, vertebra_semantic_mask, poi=None, calc_orientation=False)`:
  (1) `assign_ribs_to_vert_segmentation` joins the binary rib mask to the SPINEPS instances; (2)
  `measure_rib_length_subject` (`rib_length_measurement/rib_length_measurement_algorithm.py`): start = the rib voxel
  closest to the vertebra corpus (refined), then an iterative path through the rib (interpolation distance 15 mm,
  step half-way to the mean of candidate voxels, at most 150 iterations); **length = sum of the segment lengths
  along the path**; **stump = length <= `stump_rib_threshold_in_mm = 38.0`**; (3) `calc_rib_features`
  (`rib_features/calc_rib_features.py`): `path_points_relative_to_start`, `relative_mm_change_PIR` (direction change
  along the path, the "turns down or sideways within the first centimetres"), and for SPINEPS subregions 41, 42, 47,
  48, 49 (arcus, spinous, inferior articular L/R, corpus border) the start-to-subregion and closest-to-subregion
  direction and distance and start-to-centre-of-mass direction and distance (the "articulates more posteriorly").
  **No classifier or threshold is in `calc_rib_features`**: the paper's stump classifier (F1 0.84 on partial views)
  and the meaning and units of "-19.2 +- 3.8 vs -13.8 +- 2.5" and "260.6 vs 563.6" must come from the full text
  (the STUMP_RULE step).
- Our wrapper `CTSpinoPelvic1K-1/scripts/spineps_ct_pipeline.py` `measure_ribs()` writes
  `<out>/ribs/<case>_ribmask.nii.gz`, `<case>_rib-{inst,sem}_msk.nii.gz`, `rib_measurements_shard<k>.csv` (one row
  per case x vertebra x side; `rib_length`, `sr` first) and `rib_features/<case>.json`. It needs `/opt/ribseg`
  (the clone) on `sys.path`, the weights at `models/moller_ribseg/ribseg_model_weights` (flattened nnU-Net dir) and
  the `ctspinopelvic1k-spineps.sif` container, which is not in `~/CTSpinoPelvic1K/containers/`.

**Mask-based alternatives already on disk, and how each is biased against Möller's 38 mm path:**

| measure | code | what it is | bias |
|---|---|---|---|
| `rib_*_trace_chord_mm`, `is_rib`, `stump` | reader C `find_ribs` (in reader E J1) | CT trace through bone >= 150 HU from the costovertebral contact; chord = farthest traced voxel from the contact; rib >= 38 mm and >= 30 mm lateral; stump 12-38 mm, >= 15 mm lateral, attached | a chord is <= the path: a stump that curves in its first centimetres reads shorter, so chord-based stumps are a superset of Möller's near 38 mm; `_cut` flags truncation |
| `rib11/12_len_{left,right}_mm`, `rib12_11_ratio_*` | `extract_transition_morphometrics.py` (`_pca_length`) | extent along the rib label's first principal axis, TS-numbered ribs 1-12 on v10 ids | underestimates a curved full rib (fine for a 0.3 vs 0.7 ratio, not for 38 mm); ignores the 13th-rib ids 46/59; **FOV truncation not carried** (LAB_JOURNAL blocking item 1) |
| lowest-rib length | `scripts/detect_stump_ribs.py` `_rib_length_mm` | max pairwise distance over <= 300 subsampled voxels | a maximum extent, not a length |
| `lumbar_rib_len_mm` | same file | PCA extent of 60/61 | as above |

TS numbering trap: TotalSegmentator numbered cages from the bottom, so before the lumbar-rib class existed a rib on
L1 consumed the T12 id in 14 CTSP cases (LAB_JOURNAL "Rib numbering, finished").

---

## 6. Proposal A: the sixth rib-free body, L6 or T12 without its rib

### 6.1 The question, stated so it can be tested

Count the bodies between the lowest rib-bearing body and the sacral plateau. Five is ordinary. Six has two readings
the count cannot separate in an abdominopelvic field (no T1, so the rib-bearing count is unknown):

- **LS-L6**: 12 rib-bearing, 6 lumbar-type, 25 presacral. The top rib-free body is L1 and is lumbar-shaped.
- **TL-11**: 11 rib-bearing, the 12th thoracic body has no rib (aplastic), 24 presacral. The top rib-free body is
  T12 and is thoracic-shaped (Schinz Fig. 3D). The lumbar count below it is an ordinary five.

The classifier looks at **the most cranial rib-free body** and asks: thoracic or lumbar shape? Thoracic -> TL-11
(normal lumbosacral count). Lumbar -> LS-L6. Intermediate -> TLTV (Schinz's "mixed feature scores"), reported, not
forced. Clinical stake, in print: Lee et al., *Anesth Pain Med* 2019;14:331-334
(`CTSpinoPelvic1K-1/CaseReports_T12_hypoplastic_rib.pdf`) describe two patients whose absent 12th rib pair was read
on fluoroscopy as a lumbarised L6, and both transforaminal injections landed one level high; they cite costal facets
on T12 in 96.9 % of normal and 91.7 % of lumbarisation patients (Jagannathan, *Asian Spine J* 2017;11:365), which is
Schinz's criterion III.

### 6.2 Features, in the order Schinz's criteria rank them (all per side, in the vertebra's own frame)

Arm B (SPINEPS subregions) supports F1-F3 directly; Arm A (TS, no subregions) supports only F3 via `tp_metrics`
and F5.

| id | feature | operational definition | criterion |
|---|---|---|---|
| F1 | **SFJ angle** | the superior-facet joint of body k is the interface between its superior articular process (45/46) and the inferior articular process (47/48) of body k-1: take the 45/46 voxels within 2.5 mm of 47/48, fit a plane (smallest PCA axis), report the angle between the plane normal's axial projection and the left-right axis. ~0 deg = sagittal joint (lumbar), ~90 deg = coronal joint (thoracic). Keep the per-side values and the asymmetry (tropism). Needs body k-1 in the field | Schinz I |
| F2 | **process position relative to the SFJ** | AP offset of the 43/44 centroid from the 45/46 centroid (+ = anterior; lumbar costal process lies anterior of the SFJ, thoracic TP at or behind it); SI offset of the 43/44 top from the SFJ centre (thoracic TP at the SFJ's level, "overriding facet"; lumbar SFJ "free", no bone below it); direction of the process's long axis in the axial plane (lateral vs posterolateral) | Schinz II |
| F3 | **process shape** | reach, thickness, slenderness (`tp_metrics`, P-first), or on SPINEPS the length of 43/44 along its own axis; tip-to-tip span over the case's median span | Schinz II; the separability test's dominant feature |
| F4 | **costal fovea proxy (experimental)** | in axial sections through the pedicle root, the angle between the lateral body wall (49) and the root of 43/44: lumbar ~90 deg corner; thoracic a notch. Or a cortical pit in CT HU at the pedicle-body junction | Schinz III; no implementation anywhere; lowest priority; render every value |
| F5 | body and canal shape ratios | EPWu/EPDu, VBHa/VBHp (wedge), SCW/SCD, each over the case's own median (`test_morphometric_separability.py`) | weak; encodes position |

Never features: the list position or `pos_from_*` index, raw millimetres (size is position), rib presence or the
rib head's contact (the thing a rib-less T12 lacks by definition), any segmenter's level NAME.

### 6.3 Feasibility probe, three CTSP SPINEPS masks (not rendered; a signal, not a result)

`probe_subregions.py`, output `probe_out.txt` (both in `<session scratchpad, not kept>`); masks copied read-only from
`/rs/rs_grp_oschome/go2432/data/spineps/ctsp/`. SPINEPS labels 43-48 on thoracic as well as lumbar bodies; only 49
(no 50) carries the body on these masks.

| instances (SPINEPS names) | SFJ angle, per side (mean of sides), deg from sagittal | costal process AP offset from SAP, per side (mean) |
|---|---|---|
| T10-T12, 8 instances, cases 0001/0005/0097 | 64-87 (72-83) | -4 to -9 mm (-5 to -8), posterior |
| SPINEPS L1-L4 (0001 L1-L4, 0005 L1-L4, 0097 L2-L4; 11 instances) | 10-54 (21-47) | 0 to +8 mm (+2 to +6), anterior |
| L5, 0001 and 0097 | 34/62, 64/13 (48, 39) | +4/+6, +8/+4 mm |
| **0005 "T13"** (VERIDAH; the read says six lumbar) | **35 / 25 (30)** | **+3 / +2 mm** |
| **0097 "L1"** (read L6, IIb; first rib-free body) | **60 / 88 (74)** | +4 / -4 mm (0) |

On the mean of the two sides the thoracic (72-83) and upper-lumbar (21-47) joints do not overlap on these three
spines; single sides do overlap at L5 (0097 L5 left 64 vs 0001 T10 right 64), which is the lower lumbar joints
turning coronal and does not bear on the thoracolumbar body. The process offset separates on every instance but
0097's first rib-free body. 0005's VERIDAH "T13" is lumbar by both features, agreeing with the read (L1 of an L6
spine) against VERIDAH. 0097's first rib-free body sits under a thoracic-type joint with a process level with its
facet, which would make it a TLTV or put the facet transition a level low: n = 1, unrendered, not interpreted. The
process's long-axis direction is unstable at T12 (the small T12 process gives a near-AP PCA axis, 67-89 deg), so
F2 uses the centroid offset, not the axis. Tropism (left-right differences up to 51 deg, 0097 L5) is large
enough that both sides and their mean have to be kept.

### 6.4 Training set, model, validation

- **Unambiguous thoracic bodies**: T11 and T12 bearing a rib >= 38 mm on both sides (Möller path length in Arm B;
  reader C chord or the labelled rib in Arm A / v11), in spines with exactly five lumbar-type rib-free bodies above a
  sacrum in field, no merged/partial/fragment flag, sacrum source verified. **Unambiguous lumbar bodies**: L1-L5 of the
  same spines. Every CTSP v11 record, every VerSe whole-spine mask (ribs from the CT trace), every TS / SPINEPS pair
  with both junctions in field. Order of magnitude from J1: ~800 CTSP + ~1,100 SPINEPS + ~1,100 TS pairs.
- **The boundary pair is what is scored**: train thoracic {T11, T12} vs lumbar {L1..L5}, report T12 vs L1 separately
  (the decision the ambiguous body faces), all features over the case's own median.
- **Model**: logistic regression on F1-F3 (+F5), then `HistGradientBoostingClassifier` as the second arm (the spineps
  env has sklearn, no lightgbm/xgboost/shap); grouped by person (`tools/patient_keys.py`), StratifiedGroupKFold K = 5,
  5 seeds, out-of-fold probabilities; decision on P(thoracic): >= 0.8 thoracic, <= 0.2 lumbar, between = TLTV.
  Also report the **F1-only (SFJ) model** on its own: it is the one feature a missing rib cannot change.
- **The threat, stated**: every training T12 carries a rib, and a rib articulating with the transverse process shapes
  it (costotransverse facet). A rib-less T12 may have lumbar-like processes (Schinz Fig. 3C: long costal processes on a
  thoracic-SFJ vertebra). If F2/F3 are learned from rib-bearing T12s they may call a genuinely thoracic rib-less T12
  lumbar. So: F1 carries the call when F1 and F2/F3 disagree, and the disagreement is reported as TLTV.
- **Checks outside the computation** (none of them the classifier's own labels):
  1. LS-L6 truth (88 persons; `CT_LSTV_CLASSIFIER_PLAN.md` section 1a): their six rib-free bodies should all be lumbar;
     the top one is L1 by the count from C1 where the whole spine is in view.
  2. TL-11 read truth (VerSe verse544 581 606 626 636 642 765 814, + verse559): the top rib-free body is T12 by the
     count from C1; shape should say thoracic unless the body is a TLTV.
  3. The CTSP rib-convention candidates (0090 0105 0150 0359 0474 0544 0552 0672 0895 1151 1153; no reader) are the
     application set, not truth.
  4. Spread: SFJ angles per level against a published facet-angle series (not in the repo: pull one before quoting a
     threshold); the share of "TLTV" calls against Schinz's rate.
  5. Render every call on the ambiguous body and 20 random training bodies (axial through the SFJ, sagittal through
     the process) before any number is believed.

---

## 7. Proposal B: stump ribs and T13

- **Stump rib (primary)**: Möller path length <= 38 mm from the start point nearest the corpus (his code's rule;
  Löffler/Liebl 2021 and Schinz 2026 use the same 38 mm). Report both published conventions, because they number the
  vertebra differently: RBC (Wigh) keeps a < 38 mm rib's vertebra thoracic (TLTV); RLBC calls a vertebra with both
  ribs < 38 mm lumbar with stump ribs (Schinz p. 2197). Schinz's VSBC then overrides both with shape.
- **Stump rib (secondary, this corpus)**: lowest rib / rib above < 0.30, the valley of CTSP's bimodal ratio (modes
  0.68 and 0.32). Before it is used: re-run the bimodality on ribs 11 and 12 both untruncated (reader C `_cut` /
  `qc_rib_vertebra_incidence` flags), and recompute it on Möller path lengths instead of principal-axis extents.
- **Morphology of the stump (Möller)**: start position relative to 41/42/47/48/49 and the early turn
  (`relative_mm_change_PIR`) from `calc_rib_features`; thresholds only from the full text.
- **Decision table in an abdominopelvic field** (VSBC of the stump-bearing body = section 6 classifier):

| stump on | bodies below it before the sacrum | reading | T13 decidable? |
|---|---|---|---|
| thoracic-shaped body | 5 lumbar-type | hypoplastic 12th rib (TL-H12) **or** T13 | no: prior 12.6 % (Nagata 2025, CT) vs 0.37 % (Doo 2020, CT) |
| lumbar-shaped body | 4 more lumbar-type | lumbar rib on L1 (TL-LR), count unaffected | n/a |
| thoracic-shaped body | 4 lumbar-type | T12 with hypoplastic rib and four lumbar, or sacralised L5 | sacral-shape rule decides |
| lumbar-shaped body | 5 more lumbar-type | lumbar rib on L1 of an L6 spine | n/a |

- **T13 proper** needs the whole cage (13 rib-bearing from a rib-free C7): VerSe whole-spine (6 true T13: verse547
  582 588 601 602 631), TS whole-body CTs, RibFrac chest CTs (sacrum out of field on 651/660, so no lumbar count).
  Reader C's thoracic count from C7 is a TS-family capability only (reader E records `t1_not_cervical` otherwise).
  Prevalence windows for the census check: 13 rib-bearing 0.37-0.88 %, 11 rib-bearing 4.5-8.0 %, lumbar rib CT
  1.6 % (0.6-4.3) (`SchwingNet/lit/CITABLE_CLAIMS.md` rows 63, 68, 69).

## 8. Proposal C, briefly: sacral shape for complete sacralisation

If a completely sacralised L5 is absorbed into the sacrum label (CTSP convention, and Dataset803's by training), the
sacrum carries: one extra segment at the TOP (a vestigial disc band between the plate and S1), five foramina pairs
(weak), a top plate as narrow as the presacral body's inferior plate, ala rise on one or both sides (IIIa/IIIb), and
four lumbar-type bodies above it. Features: section 4 rows marked ADD, plus ala rise and TP-ala contact. Training:
CTSP LS-SAC 9 (fused body inside 26) + VerSe LS-SAC 13 (fused body background: sacral features computed on the TS or
Dataset803 sacrum of the same CT, never on the VerSe mask) against read ordinary spines; 24 positives cannot reach a
PPV lower bound of 0.90 (plan section 2), so this is a candidate tier with its interval.

## 9. What has to be written, in order

1. `anomaly_rules` subregion block (Arm B): F1 SFJ angle, F2 process offsets, F3 process length, on the SPINEPS
   `seg-spine` mask cropped to each instance pair (the full-volume EDT took > 5 min per case; the crop runs three
   cases in seconds). Output per instance beside the reader E row, same NaN-plus-bit rule.
2. Sacral block: plate from 74 (fallback `_sacral_plate`), S1 width/depth in the plate frame, top-plate over
   presacral EPWl ratio, midline-curve profile (vestigial disc count, arc length), disc-inside-sacrum flag, largest
   component under the column.
3. Dataset803 remap + grid alignment + sacrum Dice against SPINEPS 26 / TS sacrum union (the agreement is itself a
   reported number).
4. Möller rib stage on tier 1 (container pull inside an sbatch job; `mksquashfs` is absent on the login node).
5. Only then the classifier of section 6.4, and renders.

Not to be used as is: ostk `level_morphometry` / `canal_dimensions` / `body_mask` on the corpus (1b7005c),
`pedicle_widths` on a non-RAS array, `endplate_corners_anatomic` (NameError), `endplate_from_label("S1")` on v11,
EPW at the two lowest presacral bodies, any `labels_for` call on a non-CTSP mask.

## Sources read for this note

`OpenSpineToolkit/ostk/{labels,masks,morphometry,vertebral_body,spine,genant,io,geometry,cli,metrics}.py`, `README.md`,
`ostk/README.md`, `CLAUDE.md`; `CTSpinoPelvic1K-1/docs/{LEVEL_MORPHOMETRY,SPINEPS_BENCHMARK,SPINOPELVIC_ESTIMATOR,
LAB_JOURNAL}.md`; `CTSpinoPelvic1K-1/scripts/{extract_transition_morphometrics,extract_level_gradients,
extract_surgical_morphometrics,extract_pelvic_shape,measure_sacral_ala,detect_stump_ribs,test_morphometric_separability,
spineps_ct_pipeline}.py`; `spinesurg-ct-nnunet/docs/{CT_LSTV_CLASSIFIER_PLAN,LSTV_BENCHMARK,RESUME_2026-09-22_PM}.md`;
`tools/{rib_count_reader,tp_morphology,harvest_cobra,body_masks}.py`; `SchwingNet/tools/reader_e_features.py`;
`SchwingNet/results/reader_e/J3_NOT_SUBMITTED.md`; grid `readerE/j2v3/J2_GATE.md`; TPTBox `vert_constants.py` (grid
spineps env); `NextPaper/spinopelvic-seg/tools/convert_hf_to_nnunet.py`; GitHub `Hendrik-code/rib-segmentation`
(`run.py`, `rib_features/calc_rib_features.py`, `rib_length_measurement/rib_length_measurement_algorithm.py`);
Schinz 2026 full text; Lee 2019 (CaseReports_T12_hypoplastic_rib.pdf); memory notes on the canal regression, label
schemes, TS sacrum, SPINEPS ids, VerSe T13, R+C=22.
