# CTSpinoPelvic1K -- Lumbosacral Transitional Vertebra Annotation Package

## 1. Purpose

### 1.1 Delivery objective

The CTSpinoPelvic1K dataset and the nnU-Net model trained from it
are intended for direct deployment as **3D Slicer's default spinal-
CT segmentation backend**, replacing the spinopelvic output of
TotalSegmentator. TotalSegmentator's documented LSTV failure mode
(see accompanying paper) propagates from Slicer-based clinical
workflows directly to spine surgical planning, where it reproduces
the canonical mechanism of wrong-level surgery. Closing the LSTV
gap at the level of Slicer's default tool is the deliverable of
this work, and your annotations directly enable it.

The trained model will ship as a 3D Slicer extension, complete
with an automated spinopelvic-parameter measurement module trained
from the landmark annotations gathered through this package.

### 1.2 Scope of this package

This package contains 33 lumbosacral transitional vertebra (LSTV)-
positive cases from the CTSpinoPelvic1K dataset, programmatically
identified by combining vertebral counting from CTSpine1K and
filename morphological qualifiers from CTPelvic1K. The programmatic
labels have known limitations and require expert radiologist
verification before public release.

This document describes a standardized landmark-based annotation
protocol designed to permit objective, deterministic derivation of:

1. Castellvi (1984) classification of the lumbosacral junction.
2. Mahato (2020) lumbosacral transitional spectrum grade.
3. Mahato (2020) sacral morphometric measurements.
4. Standard spinopelvic parameters (sacral slope, pelvic tilt,
   pelvic incidence, L1-S1 lumbar lordosis), where the relevant
   landmarks are within the CT field of view.

The radiologist's role is to place anatomical landmarks; categorical
classification is performed by post-processing software from the
landmark coordinates. Expert observation is encoded by the
placement (or deliberate non-placement) of each landmark.

---

## 2. Authorship contribution

Co-authorship on the dataset paper is offered to reviewers who
complete, for each of the 33 LSTV cases:

1. Confirmation or proposed reclassification of the programmatic
   subtype (in `review.txt`).
2. Placement of the 26 required landmarks (Castellvi observation,
   Castellvi measurement, sacral foramina, and Mahato anatomical
   groups) in 3D Slicer, saved as `landmarks.mrk.json` in the token
   directory.

Reviewers who additionally place the 5 optional spinopelvic
landmarks enable computation of pelvic incidence, pelvic tilt,
sacral slope, and L1-S1 lumbar lordosis -- providing the basis for
a follow-up paper on automated spinopelvic measurement, with
continuing co-authorship for participating reviewers.

Reviewers who decline the landmark placement work but provide
written subtype confirmations only will be acknowledged in the
data card.

---

## 3. Workflow in 3D Slicer

The reviewer requires only **3D Slicer 5.x** (free, available at
slicer.org). No command-line tools, no Python, and no manual JSON
editing are needed. 3D Slicer's Markups module automatically reads
and writes the `.mrk.json` files used in this protocol; the
radiologist interacts only with the standard graphical interface.

### 3.0 Recommended: install the LSTVReviewer Slicer module

A custom Slicer module, **`LSTVReviewer.py`**, is included at the
top level of this package along with a **printable install guide,
`LSTVReviewer_install_guide.pdf`**. The module collapses the
per-case workflow to three clicks (Load -> place fiducials ->
Save) and tracks completion progress across all 33 cases.
Installation takes about 2 minutes and requires no coding.

**To install:** open `LSTVReviewer_install_guide.pdf` in this
directory and follow the numbered steps. In short:

1. In Slicer: `Edit` -> `Application Settings` -> `Modules`
2. Add the directory containing `LSTVReviewer.py` (i.e., this
   directory) to "Additional module paths".
3. Restart Slicer.
4. The "LSTV Reviewer" module appears under
   `Modules` -> `Annotation`.

Once installed, you can ignore Sections 3.2-3.4 below and use
the module's three-button interface. Sections 3.2-3.4 remain as
the fallback manual procedure if you prefer the standard
Slicer workflow without the helper module.

### 3.1 One-time setup

1. Download and install 3D Slicer 5.x from
   [https://www.slicer.org](https://www.slicer.org).
2. Launch Slicer. The default modules (Volumes, Segmentations,
   Markups) are sufficient; no extensions need to be installed.
3. Optional: in **Edit > Application Settings > Markups**, increase
   the default glyph size if the default fiducial markers are too
   small to see clearly on the CT slices.

### 3.2 Per-case annotation procedure

For each token directory (e.g. `sacralization/token_167/`):

#### Step 1. Load the CT volume

- **File > Add Data > Choose File(s) to Add**
- Select `ct.nii.gz` (or, in separate-mode cases,
  `ct_separate_spine.nii.gz` -- the spine mask corresponds to this
  acquisition).
- Confirm the "Description" column shows "Volume".
- Click **OK**.

#### Step 2. Load the segmentation masks as overlays

- **File > Add Data > Choose File(s) to Add**
- Select `label.nii.gz` (or, in separate-mode cases,
  `label_spine.nii.gz` and `label_pelvic.nii.gz`)
  (Ctrl/Cmd+click to multi-select).
- For each row in the dialog, change the "Description" from
  "LabelMapVolume" to "Segmentation". This enables transparency
  control over the masks.
- Click **OK**. The masks now overlay the CT in the slice viewers
  and can be toggled or made semi-transparent in the Data module.

#### Step 3. Load the landmark template

- **File > Add Data > Choose File(s) to Add**
- Select `landmarks_template.mrk.json`.
- Confirm the "Description" reads "Markups Fiducial".
- Click **OK**. A list of 31 named fiducials appears in
  the Markups module, each in **"preview" status** (unplaced).

#### Step 4. Switch to the Markups module

- In the top-left **Module** dropdown, select **Markups**.
- The control points list shows all 31 fiducials with their
  anatomical descriptions visible when each is selected.

#### Step 5. Place the landmarks

For each fiducial:

- Click on the fiducial's row in the **Control Points** list to
  highlight it.
- Read the description in the bottom panel for the anatomical
  definition.
- Press the **Place** button (the cursor-with-target icon at the
  top of the Markups module), or use hotkey **Ctrl+Shift+A**.
- In the slice viewers (Red / Yellow / Green panes), navigate to
  the anatomical location using mouse-wheel or scrollbars.
- **Click** on the location. The fiducial is placed, its status
  changes from "preview" to "defined", and Slicer automatically
  advances to the next fiducial in the list.

#### Step 6. Skip a landmark that does not apply

For [OBSERVATION] landmarks (Castellvi articulation and fusion)
when the structure is absent on a side, OR for [FORAMEN] landmarks
S4/S5 when the sacrum has fewer segments:

- In the Control Points list, **right-click** the fiducial.
- Choose **"Unset position"**. The fiducial's status reverts to
  "preview" and is treated as "absent" by the processing software.
- If the fiducial was never placed, it is already in "preview"
  status and no action is needed -- simply skip past it.

#### Step 7. Save the landmark file

3D Slicer writes the JSON automatically based on your placements.

- Press **Ctrl+S** (or **File > Save**).
- A dialog lists all data nodes in the scene.
- Find the row for the markup node (originally named after the
  template).
- In the **File Name** column, click and edit to
  `landmarks.mrk.json` (drop the `_template` suffix; do not
  overwrite the template file).
- In the **File Directory** column, browse to the same token
  directory.
- Ensure the markup node's checkbox is ticked. The other rows
  (CT, masks) can be unchecked.
- Click **Save**.

#### Step 8. Fill in the review form

- Open `review.txt` in any plain text editor (Notepad, TextEdit,
  VS Code, BBEdit). The form is a few lines of `Field: value`
  text.
- Complete the fields and save.

#### Step 9. Move to the next case

- **File > Close Scene** (or restart Slicer) to clear loaded data.
- Repeat from Step 1 for the next token directory.

### 3.3 What gets generated automatically

Three things you do NOT type by hand:

| Output                          | Generated by                                 |
|---------------------------------|----------------------------------------------|
| `landmarks.mrk.json`            | 3D Slicer's Markups module on Save           |
| Castellvi grade (Ia/Ib/IIa/...) | Post-processing from your landmark placements |
| Mahato spectrum grade (B/C/D/E) | Post-processing from your landmark placements |
| All linear / angular morphometrics | Post-processing geometry from coordinates |

The only file you edit by hand is `review.txt`, which is plain
text.

### 3.4 Returning your work

When you have annotated all cases (or as many as you choose to
review), archive the entire `lstv_review/` folder
(`tar -czvf lstv_review.tar.gz lstv_review/` on macOS/Linux, or
right-click > "Send to > Compressed (zipped) folder" on Windows)
and return to the corresponding author.

---

## 4. Classification systems

### 4.1 Castellvi (1984) -- L5/S1 junction morphology

Castellvi describes the lumbosacral junction. It does NOT
distinguish lumbarization (4-segment sacrum) from sacralization
(6-segment sacrum); the Mahato spectrum (Section 4.2) supplies
that distinction.

| Type     | Anatomical criterion                                                                  | Subtypes      |
|----------|---------------------------------------------------------------------------------------|---------------|
| Type I   | Dysplastic transverse process(es) >=19 mm craniocaudal dimension; no articulation     | Ia / Ib       |
| Type II  | Diarthrodial pseudoarticulation between transverse process and sacral ala             | IIa / IIb     |
| Type III | Complete osseous fusion of transverse process to sacral ala                           | IIIa / IIIb   |
| Type IV  | Type II on one side AND Type III on the contralateral side                            | (no subtypes) |

Subtype suffix: `a` = unilateral, `b` = bilateral.

### 4.2 Mahato (2020) -- LSTV spectrum

The Mahato spectrum places the case on the
lumbarization-to-sacralization axis based on the number of sacral
segments and the symmetry of any articulation or fusion.

**The original Mahato (2020) paper is included in this package as
`Mahato_2020_LSTV_classification.pdf`.** Refer to Fig. 1 of the
paper for visual depictions of the lumbarization spectrum
(panels B-D), Fig. 2 for the sacralization spectrum (panels B-E),
Tables 3-4 for the morphometric measurement definitions, and the
auricular surface position classification (Section 4.3 below).

#### 4.2.1 Lumbarization spectrum (Mahato Fig. 1, panels B-D)

| Grade | Sacral segments | Description                                                          |
|-------|-----------------|----------------------------------------------------------------------|
| B     | 5               | Incomplete lumbarization: partial unilateral S1-S2 separation        |
| C     | 4               | 4-segment sacrum with bilateral L6-S1 accessory articulation         |
| D     | 4               | Complete lumbarization: 4-segment sacrum, no accessory articulation |

#### 4.2.2 Sacralization spectrum (Mahato Fig. 2, panels B-E)

| Grade | Sacral segments | Description                                                          |
|-------|-----------------|----------------------------------------------------------------------|
| B     | 5               | Unilateral L5-S1 accessory articulation                              |
| C     | 5               | Bilateral L5-S1 accessory articulation                               |
| D     | 6               | Incomplete sacralization: 6-segment sacrum, one side unfused at L5-S1 |
| E     | 6               | Complete sacralization: 6-segment sacrum, bilateral fusion           |

### 4.3 Auricular surface position (Mahato 2010)

Three-class system based on the position of the upper border of
the sacral auricular surface relative to S1:

- Type I / normal: AS upper border within the upper half of S1
- Type II / high:  AS upper border above the sacral promontory
- Type III / low:  AS upper border below the midpoint of S1

This is computed automatically from auricular surface and foramen
landmarks; the radiologist does not assign it manually.

---

## 5. How landmark placement determines classification

The downstream processing software (`process_reviews.py`) derives
classifications from landmark coordinates as follows.

### 5.1 Sacral segment count

Determined by the number of placed ventral foramen pairs:

- 3 pairs (S1, S2, S3 placed; S4 and S5 unplaced) -> 4-segment
  sacrum (lumbarization morphology)
- 4 pairs (S1-S4 placed; S5 unplaced) -> 5-segment sacrum
  (normal morphology)
- 5 pairs (S1-S5 all placed) -> 6-segment sacrum
  (sacralization morphology)

Asymmetric counts (e.g., 4 pairs left, 5 pairs right) generate a
warning in the validation report and use the more conservative
count.

### 5.2 Castellvi grade (per side, then combined)

For each side independently, the algorithm assigns:

1. Type III if `castellvi_fusion_bridge_<side>` is placed.
2. Type II if `castellvi_articulation_<side>` is placed and no
   fusion is present.
3. Type I if neither articulation nor fusion is present, but the
   craniocaudal distance between `transitional_TP_cranial_<side>`
   and `transitional_TP_caudal_<side>` is >= 19 mm.
4. None if none of the above conditions is met.

The two sides are then combined:

- Bilateral identical types -> Ib, IIb, or IIIb.
- Unilateral (one side typed, other not) -> Ia, IIa, or IIIa.
- Type II on one side + Type III on contralateral -> Type IV.
- Atypical mixed combinations (e.g., I left + II right) are
  reported with explicit per-side notation.

### 5.3 Mahato spectrum grade

Determined from the joint observation of lumbar body count
(extracted from `label.nii.gz`), sacral segment count
(Section 5.1), and articulation / fusion landmark presence:

- 5 lumbar bodies + 5-segment sacrum + no articulation, no fusion
  -> **A** (normal)
- 6 lumbar bodies + 5-segment sacrum -> Lumbarization **B**
  (incomplete; partial S1-S2 separation)
- 6 lumbar bodies + 4-segment sacrum + bilateral articulation
  -> Lumbarization **C**
- 6 lumbar bodies + 4-segment sacrum + no articulation
  -> Lumbarization **D** (complete)
- 5 lumbar bodies + 5-segment sacrum + unilateral articulation
  -> Sacralization **B**
- 5 lumbar bodies + 5-segment sacrum + bilateral articulation
  -> Sacralization **C**
- 4 lumbar bodies + 6-segment sacrum + unilateral fusion
  -> Sacralization **D** (incomplete)
- 4 lumbar bodies + 6-segment sacrum + bilateral fusion
  -> Sacralization **E** (complete)

Configurations that do not fit any grade are flagged
"indeterminate" with a description of the observed combination,
for case-by-case adjudication.

### 5.4 Mahato morphometric measurements

Computed deterministically from the placed landmark coordinates
(LPS, mm), as defined in Mahato (2020) Table 3 and Table 4:

- **SH** (sacral height): Euclidean distance from
  sacral_promontory_midpoint to sacral_base_midpoint.
- **AH** (auricular surface height, per side): distance from
  auricular_surface_upper to auricular_surface_lower.
- **IFD** (inter-facet distance): distance between left and right
  S1_facet_dorsal.
- **IAD** (inter-auricular distance): distance between left and
  right auricular_surface_upper.
- **BW** (S1 body width): distance between left and right
  ventral_foramen_S1.
- **AW** (alar width): IAD - BW.
- **S1O** (S1 transverse element obliquity, per side, coronal
  plane, degrees): angle between the vector from sacral_promontory
  to auricular_surface_upper and the horizontal reference (line
  through left and right ventral_foramen_S2).
- **S1T** (S1 corridor thickness, per side, mm): craniocaudal
  distance from ventral_foramen_S1 to ventral_foramen_S2.
- **S2T** (S2 corridor thickness, per side, mm): craniocaudal
  distance from ventral_foramen_S2 to ventral_foramen_S3.
- **AS position type**: I / II / III, derived from the z-position
  of auricular_surface_upper relative to the S1 segment z-extent
  (sacral_promontory_midpoint to mean of ventral_foramen_S2 z).

### 5.5 Standard spinopelvic measurements (optional)

Computed in the sagittal plane from the optional spinopelvic
landmarks, when placed:

- **Sacral slope**: angle between the S1 superior endplate
  (sacral_promontory_midpoint to S1_endplate_posterior_midline)
  and the horizontal.
- **Pelvic tilt**: angle between the vertical and the line from
  the S1 endplate midpoint to the bicoxofemoral axis (midpoint of
  the two femoral_head_center landmarks).
- **Pelvic incidence**: angle between the S1 endplate normal at
  its midpoint and the line to the bicoxofemoral axis.
- **L1-S1 lumbar lordosis**: angle between the L1 superior
  endplate (L1_endplate_anterior to L1_endplate_posterior) and
  the S1 superior endplate.

---

## 6. Landmark catalogue

The Slicer template `landmarks_template.mrk.json` contains 31
named fiducials, each with its anatomical description visible in
the Markups module's "Description" field.

### 6.1 Castellvi observation (n=4) -- place IF present

| Label                          | Indicates             |
|--------------------------------|-----------------------|
| castellvi_articulation_left    | Castellvi II, left    |
| castellvi_articulation_right   | Castellvi II, right   |
| castellvi_fusion_bridge_left   | Castellvi III, left   |
| castellvi_fusion_bridge_right  | Castellvi III, right  |

### 6.2 Castellvi measurement (n=4) -- TP dysplasia assessment

| Label                          | Definition                                       |
|--------------------------------|--------------------------------------------------|
| transitional_TP_cranial_left   | Most superior point of left transitional-vertebra TP |
| transitional_TP_cranial_right  | Same, right                                      |
| transitional_TP_caudal_left    | Most inferior point of left TP at the same level |
| transitional_TP_caudal_right   | Same, right                                      |

The transitional vertebra is L5 in sacralization and L6 in
lumbarization. Craniocaudal length >=19 mm without articulation or
fusion satisfies Castellvi Type I.

### 6.3 Sacral foramina (n=10) -- segment count

Place every ventral (anterior) foramen visible. Foramina S4 and
S5 may legitimately be absent depending on segment count:

| Label                       | Present in sacrum of segment count |
|-----------------------------|------------------------------------|
| ventral_foramen_S1_left/right | >=2 segments (always)             |
| ventral_foramen_S2_left/right | >=3 segments (always)             |
| ventral_foramen_S3_left/right | >=4 segments (always)             |
| ventral_foramen_S4_left/right | 5 or 6 segments                   |
| ventral_foramen_S5_left/right | 6 segments only (sacralization)   |

### 6.4 Mahato anatomical (n=8) -- always place if visible

| Label                              | Definition                                  |
|------------------------------------|---------------------------------------------|
| sacral_promontory_midpoint         | Midline midpoint of superior anterior S1    |
| sacral_base_midpoint               | Midline caudal apex of sacrum               |
| auricular_surface_upper_left/right | Midpoint of superior margin of AS, per side |
| auricular_surface_lower_left/right | Most inferior extent of AS, per side        |
| S1_facet_dorsal_left/right         | Dorsal edge of S1 superior articular facet  |

### 6.5 Spinopelvic optional (n=5) -- bonus landmarks

| Label                            | Used for                          |
|----------------------------------|-----------------------------------|
| S1_endplate_posterior_midline    | Sacral slope, pelvic incidence    |
| femoral_head_center_left/right   | Pelvic incidence, pelvic tilt     |
| L1_endplate_anterior_midline     | L1-S1 lumbar lordosis             |
| L1_endplate_posterior_midline    | L1-S1 lumbar lordosis             |

If L1 or the femoral heads are outside the CT field of view,
leave the corresponding landmark in "preview" status. The
spinopelvic measurements requiring those landmarks are then
omitted for that case; other measurements are unaffected.

---

## 7. Subtype definitions (programmatic; awaiting verification)

The directory structure groups cases by the programmatic subtype.
Your landmark placements determine the algorithmically-derived
classification, which will be compared with the programmatic
label.

- **lumb** (n=14): 6 lumbar bodies labeled in `label.nii.gz`
  (mask value 6 = L6 present).
- **sacralization** (n=6): pelvic source filename carried
  `_sacralization_` qualifier; expected Castellvi III.
- **semisacralization** (n=2, REVIEW PRIORITY): pelvic filename
  carried `_semisacralization_` qualifier; expected Castellvi
  I or II.
- **sacr_count** (n=9): 4 lumbar bodies labeled in spine mask;
  L5 inferred fused to sacrum. May represent true sacralization
  OR under-annotation; landmark placement will adjudicate.
- **ambiguous** (n=2, REVIEW PRIORITY): cross-source disagreement
  not reconcilable programmatically.

---

## 8. Reference normal case

`reference_normal/token_<id>/` contains one fused-mode normal
case for visual calibration. No annotation is requested for this
case; use it to configure your Slicer display settings (window
level, segment color, fiducial size) before beginning LSTV cases.

---

## 9. Output files per token

After your annotation:

| File                          | Source        | Purpose                            |
|-------------------------------|---------------|------------------------------------|
| ct[_<match_type>].nii.gz      | provided      | CT volume(s)                       |
| label[_<match_type>].nii.gz   | provided      | Segmentation (10 classes: L1-L6, sacrum, hips) |
| landmarks_template.mrk.json   | provided      | Template; do not modify            |
| landmarks.mrk.json            | reviewer      | Your landmark placements           |
| review.txt                    | reviewer      | Categorical confirmation + notes   |

---

## 10. References

1. Castellvi AE, Goldstein LA, Chan DPK. Lumbosacral transitional
   vertebrae and their relationship with lumbar extradural
   defects. *Spine (Phila Pa 1976)* 1984;9(5):493-495.
2. Konin GP, Walz DM. Lumbosacral transitional vertebrae:
   classification, imaging findings, and clinical relevance.
   *AJNR Am J Neuroradiol* 2010;31(10):1778-1786.
3. Mahato NK. Variable positions of the sacral auricular surface:
   classification and importance. *Neurosurg Focus* 2010;28:E12.
4. Mahato NK. Re-examining the spectrum of lumbosacral
   transitional dysmorphisms: quantifying joint asymmetries and
   evaluating the anatomy of screw fixation corridors.
   *Neurospine* 2020;17(1):294-303.
   doi:10.14245/ns.1938102.051
5. Sekharappa V, Amritanand R, Krishnan V, David KS. Lumbosacral
   transition vertebra: prevalence and its significance.
   *Asian Spine J* 2014;8(1):51-58.
6. Lumbosacral transitional vertebra. *Radiopaedia.org* (last
   revised 10 March 2026).
