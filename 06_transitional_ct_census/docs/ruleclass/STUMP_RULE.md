# STUMP_RULE: how Möller et al. define a stump rib, what their code returns, and the rule arm B will run

Written 2026-09-27 for the SUPER DETECTOR RUN (arm B = SPINEPS + VERIDAH + Möller ribs + Dataset803 pelvis).
Sources were read in full: the journal article, the arXiv preprint, every Python file in the repository, the
TPTBox label constants, and the Zenodo record with its zip listings. Nothing was run. Every number from the paper is
quoted, with its section. Local copies are in `ruleclass/src/`.

---

## 0. In brief

1. **A stump rib is defined by length alone.** It is a rib of 38 mm or less, measured along the rib's
   path from the head outward. The threshold is Wigh 1980. The code applies it as
   `stump_rib_threshold_in_mm: float = 38.0`. A rib of 38 mm or less that touches the crop border gets `sr = None`
   (undecidable), not `True`.
2. **Möller has no ratio rule and no bimodal distribution.** Neither version of the paper compares the last
   rib with the rib above it, and "bimodal" appears in neither. The paper publishes no histogram of rib lengths. Its
   own threshold sweep finds **no transition at 38 mm**: "the relationship may be more continuous rather than
   reflecting a strict biological threshold" (journal, App. D).
3. **The bimodal ratio Greg remembers comes from CTSpinoPelvic1K's own paper** (`paper/mpda/main.tex`): "The
   lowest-rib length ratio is bimodal, its lower mode lying below 0.33 of the rib above". That ratio uses a
   **PCA extent** (`extract_transition_morphometrics._pca_length`), not Möller's path length. It compares the ribs
   TotalSegmentator numbered 12 and 11, not "the last rib and the one above". It is a CTSP-native rule. On Möller
   lengths its cut has to be derived again (section 8, rule S3).
4. **The morphology features describe the ribs and feed a classifier.** Stump ribs start further back (PDRC),
   are thinner (volume per length), and point outward and downward over the first ~7 mm (2-PPR). A classifier on
   the first four path points plus DRC reaches "an F1-score of 0.84 and an AUC of 0.98" (journal abstract). That was
   measured on **simulated** partial views: the first path points of ribs whose full length was known. **No classifier
   code or weights are released.**
5. **The Zenodo record holds only binary rib masks and the nnU-Net weights.** It has no lengths, no stump labels and
   no features. Calibration therefore means running `run_all_steps` on VerSe ourselves and comparing against two
   outside references: (i) the paper's reported distributions and (ii) the stump-rib column of Löffler 2021, read by
   two neuroradiologists. The VerSe masks and the weights are **already on the grid** (section 10).
6. **Four code problems decide whether arm B works at all** (section 11). (a) Rib assignment skips T13 (id 28),
   the level where a T13 spine's stump would sit. (b) Our wrapper would write the 0.5 mm debug array (`darr`) into JSON,
   tens of MB per rib. (c) The feature step builds a dense rib-to-corpus distance matrix; the paper says it needed
   "more than 100 GB of available RAM". (d) Our wrapper never saves the rib-to-vertebra instance mask, which the
   rib-free count needs.
7. **Units.** PDRC is in mm (the journal says so). The journal labels volume-to-length as "mm2". The code's
   `rib_volume` is a **voxel count at 0.5 mm isotropic**, however, so the ratio is most likely voxels per mm. In mm² that
   would be ×0.125: about 32.6 against 70.5 mm². This is inferred and unverified; step C5 settles it.

---

## 1. Sources read

| source | version / date | local copy (`ruleclass/src/`) |
|---|---|---|
| Möller H, Dima A, Keinert-Weth B, Graf R, Atad M, Paetzold J, Jungmann F, Braren R, Kofler F, Menze B, Rueckert D, Kirschke JS, Schön H. *Automated Thoracolumbar Stump Rib Detection and Analysis in a Large CT Cohort.* **AI (MDPI) 2026;7(6):224**, doi:10.3390/ai7060224 | received 12 May 2026, published 16 June 2026; 21 pp. incl. App. A–G. **Authoritative** | `mdpi.pdf`, `mdpi.txt`, page renders `mdpi_p10.png` (Fig. 6), `mdpi_p11.png` (Fig. 7, Table 5), `mdpi_p17.png` (Figs. A3/A4), `mdpi_fig1.png` (data flow) |
| same, arXiv:2505.05004**v1** | 8 May 2025 (only version) | `arxiv_2505.05004v_latest.html`, `arxiv.txt`, `arxiv.pdf` |
| github.com/Hendrik-code/rib-segmentation | `main` @ 10998cdb32 (2025-06-11, "fixed some type hints and updated to newest TPTBox version") | `code/*.py`, `code/README.md` |
| TPTBox (Hendrik-code/TPTBox) | `main` (latest tag v1.0.0); the journal used "TPTBox v0.4.2" (§2.8) | `tptbox/vert_constants.py`, `nii_wrapper.py`, `np_utils.py`, `poi.py`, `init.py` |
| Zenodo concept 10.5281/zenodo.14850928 → record **14864106** (the only files-bearing version), CC-BY-4.0 | 2025-02-10 | `zenodo_14850928.json`, `zenodo_versions.json`, zip listings `zenodo_preview_*.html` → `zenodo_listing.json` |

MDPI's CDN serves a JavaScript proof-of-work page to plain `curl`. `src/fetch_mdpi.py` answers it (curl_cffi with a
Chrome fingerprint) and fetched the journal PDF. The earlier notes (`SchwingNet/lit/CITABLE_CLAIMS.md` row 57) say
the journal body was unreadable. That is no longer true, and the journal text differs from arXiv v1 in places
(section 6).

---

## 2. How a stump rib is defined

**The definition is length only, from Wigh 1980.**
- Journal §1: "These so-called stump ribs, by common definition, have a length of ≤38 mm and can only appear at the
  lowest thoracic level [3]." [3] = Wigh RE, *The thoracolumbar and lumbosacral transitional junctions*, Spine
  1980;5:215–222.
- Journal §2.4: "By definition, thoracolumbar stump ribs (SR) are shorter than or equal to 38 mm [3]. We compare this
  threshold to the length computed by our RLMA. This yields a binary label (SR or not-SR) for each rib."
- Code, `rib_length_measurement/rib_length_measurement_algorithm.py` L21 and L259–264:
  ```python
  stump_rib_threshold_in_mm: float = 38.0
  ...
  if rib_length > stump_rib_threshold_in_mm:
      stump_rib = False
  else:
      # stump_rib if not segmentation at border, else None (not determinable)
      stump_rib = True if not seg_at_border else None
  ```
  So `sr` has three states: `False` (longer than 38 mm, even if cut by the field edge), `True` (38 mm or less and clear
  of the edge) and `None` (38 mm or less and touching the edge).
- **Which ribs are measured.** Journal §2.6: "the rib-length measuring algorithm (RLMA) on the lowest two vertebrae
  with ribs present". The code can take up to three levels (section 3).
- **When a label counts as known.** Journal §2.6: "we only used ribs marked with (4) and (5) and those with (3) where
  the length of the visible part already exceeded the SR threshold." Likert (3) means "the segmentation touches the
  border of the image and thus the length of the visible section is correct but incomplete". That is the same logic
  as `sr = None`.

**No ratio, no bimodal distribution, no data-driven cut.** A search of both texts finds "ratio" only in
"volume-to-length ratio" and finds no "bimodal". The only distribution plots are Fig. 6 (volume/length against PDRC)
and Fig. 7 (2-PPR components). Both overlap: "Although not separated, we observe a clear trend" (Fig. 6 caption).
The threshold sweep argues against a natural cut at 38 mm:
- Journal App. D: "Although the 38 mm stump rib threshold has been adopted from prior literature as a clinically
  relevant cutoff, we cannot demonstrate a distinct peak or transition at this value. This suggests that the
  relationship may be more continuous rather than reflecting a strict biological threshold. Nevertheless, we retained
  the 38 mm cutoff to ensure comparability with previous studies".
- arXiv A.2: "There seem to be small peaks at around the threshold of 41 mm, for which we can offer no explanation."
  In Figs. A3/A4 the DRC + 4-PPR F1 falls from about 0.93 at a 30 mm cut to about 0.8 at 80 mm, with no step at 38
  (read off the plot, approximate).

**Where the ratio and the bimodality come from: CTSpinoPelvic1K's own paper.**
- `paper/mpda/main.tex` L806–808: "The lowest-rib length ratio is bimodal, its lower mode lying below 0.33 of the rib
  above. Its lower mode marks a stump twelfth rib in 98 of the 789 records with a measurable pair (12.4\%), and a
  lumbar rib is present in 16 (2.0\%), against 12.6\% and 1.5\% in a whole-spine CT series that reports both
  [nagata2025]."
- `docs/LAB_JOURNAL.md` L77–79: "Rib 12 length as a fraction of rib 11 splits into two modes — a main population near
  0.68 and a distinct hypoplastic one near 0.32, with 67 cases below 0.30."
- How it was measured, from `scripts/extract_transition_morphometrics.py` L99–108 and L440–448:
  - The length is `_pca_length`, the "extent along the structure's own long axis". That is a chord, not the arc.
  - The ribs are the label-named rib 12 and rib 11 (TS numbering, hand-corrected in v11).
  - The ratio is `rib12_11_ratio_min`, the minimum over the two sides.
  - `scripts/six_lumbar_readings.py` L43 sets `STUMP_RATIO = 0.33`.
- The same paper shows that length alone does not separate a lumbar rib from a stump twelfth rib. `main.tex` L606–607:
  "the sixteen ribs labeled lumbar running a median 45 mm and 0.32 of the rib above them against 38 mm and 0.28 for
  the 98 labeled stump twelfth ribs." The ratio-defined stumps therefore have a **median of 38 mm**. Roughly half of
  them would be `sr = False` under Möller's rule, if a PCA extent approximates a path length for a short, straight rib.
  This has not been checked.
- Open item from the lab journal (L148–153, marked "Blocking"): "Re-run the bimodality restricted to cases where ribs
  11 and 12 are both untruncated. If the second mode survives it is anatomy; if it collapses, the headline was
  framing." I found no record that this was done.

**What this means for the rule.** The primary stump call is Möller's 38 mm rule on his path length. The ratio stays
as a second, CTSP-native rule. Its cut is re-derived on Möller lengths, with truncated ribs excluded (step C6). A
PCA-extent cut of 0.33 is not carried over to path lengths. A curved full rib's chord is shorter than its arc while a
stump's chord is close to its length, so the same anatomy gives a higher ratio on chords than on arcs.

---

## 3. The length measurement (RLMA): parameters and the ribs it covers

| step | paper (journal) | code |
|---|---|---|
| crop + rescale | §2.4: "We started by cropping a single rib combined with its corresponding vertebra. ... we rescaled the cropped segmentation mask to a fixed resolution of 0.5 mm for each dimension." | `run_algorithm.measure_one_rib_length`: `compute_crop(dist=8)`, `rescale((0.5,0.5,0.5), mode="nearest")` |
| fill | §2.4: "We filled 3D holes" | dilate/erode/dilate/erode by 1 voxel (`do_dilateerode=True`), a closing, not a hole fill |
| start point | §2.4: "We select the closest point on the segmentation surface to the center of mass of the corresponding vertebra corpus. We refine the location by averaging all surrounding segmented voxels and projecting the result onto the segmentation surface" | the rib voxel nearest the COM of label 49 (corpus; 50 is mapped to 49), refined by the centre of mass of a ±20-voxel patch in that L/R slice |
| step | §2.4: "candidate points within a circular distance of 14.5 to 15.5 mm from the previous path point ... Moving from the latest point halfway along that direction vector" | `interpolation_distance_mm=15.0`, tolerance = voxel size 0.5, `max_iterations=150` |
| end | §2.4: "we shoot a cone of ray-casts from the latest path point along the vector of the previous path point and find the point in those ray-casts that is furthest away" | `get_possible_end_points`: 1 + 3 × 9 perturbed rays, bisection ray-cast |
| length | §2.4: "we take the path points and sum the distances between them" | `rib_length = sum(prior_distance)`, in mm |
| step length | §3.3: 2-PPR "is roughly the beginning 7 mm of a rib"; §4: "the first four path points have an average total length of around 22 mm"; "the initial 15 mm (required for 3-PPR)" | consistent with ~7.5 mm per step |
| edge flag | Likert (3) | `seg_at_border`: the rib's box within 2 voxels of the crop edge. The crop has an 8-native-voxel margin clamped at the image, so in practice this means the rib reaches the field edge |

**Which levels the code measures** (`run_algorithm.measure_rib_length_subject`, L34–46):
```python
last_vertebrae = [i for i in inst_seg.unique() if (7 < i and i < 21) or i == 28]   # T1..L1 and T13
last_vertebrae.sort()                                                                # numeric: 28 sorts after L1
last_two_vertebrae = [Vertebra_Instance(v) for v in last_vertebrae[-3:] if Vertebra_Instance(v).RIB in rib_labels]
if len(last_two_vertebrae) == 0 or last_two_vertebrae[0].value <= 16: return results   # needs T10 or lower
```
It measures up to **three** levels (the lowest three vertebrae present, kept if they carry a rib) and only when the
highest of them is T10 or lower. Measurement **does** consider T13 (28). Assignment does not (section 11, D1), so a
T13 rib never reaches the measurement. The numeric sort puts T13 after L1, so `is_last_v` would be wrong in the rare
spine with both a T13 rib and an L1 rib.

**Reliability.** Journal §3.2: "98.2% of the lowest two ribs in both public data sets were correctly segmented and
measured (see Table 4)". Table 4: rated (5) 69.3 %, (4) 16.7 %, (3) 12.2 %, (2) 1.2 %, (1) 0.6 %. App. C: "Most
differences are below 1 mm. There is only one sample where the difference would change the stump rib label"
(predicted against reference masks on the 45 test subjects). §4: "Only severe errors, such as merged ribs, large
missing segments, split ribs, or structural anomalies (e.g., bone tumors or partially resected ribs), will result in
measurable deviations due to algorithm design." A **split rib** (a fracture, and RibFrac is a fracture cohort) gives a
short proximal piece that the length rule will call a stump.

---

## 4. Morphological features: definitions, units and frames

| feature | paper definition | code key (in `d["features"]`) | units / frame |
|---|---|---|---|
| **DRC** | §2.5: "the spatial relation vector between the rib's start point and the corresponding vertebra corpus center (DRC)"; Glossary: "Direction Rib Corpus" | `49_start_to_com_direction` (= corpus COM − start, 3-vector). Classifier input per §3.3 is "the relation between the rib start and the vertebra corpus surface and center", so it also uses `49_start_to_subregion_direction` (start → nearest corpus voxel). The exact vector set is not stated | mm; image axes **P, I, R** after `reorient_()` (TPTBox default `("P","I","R")`) |
| **PDRC** | §2.5: "the posterior distance between the rib and the corpus center, which we denote PDRC"; §3.3: "the distance in the posterior direction between the corresponding vertebra corpus center and the closest point on the rib" | P component (index 0) of `49_start_to_com_direction`. It is negative when the start lies behind the corpus centre, which matches the reported negative means. Alternative reading: `49_closest_to_com_direction[0]` (the rib voxel nearest the COM within ±20 mm of the start). Step C3 decides | **mm**: journal abstract "(−19.2 ± 3.8 vs. −13.8 ± 2.5 mm" |
| **volume-to-length ("thinness")** | §2.5: "From the RLMA, we have the rib's length; using the segmentation mask, we can calculate the volume-to-length ratio." | not computed in the released code. The only volume field is `rib_volume = rib_seg_cropped.volumes()[1]`, and TPTBox `volumes()` "Returns a dict stating how many pixels are present for each label" (voxel count, `in_mm3=False` by default) on the 0.5 mm grid after closing | journal says "mm2". If the ratio is `rib_volume / rib_length`, the unit is **voxels(0.5 mm)/mm**, and mm² = value × 0.125: stump ≈ 32.6 ± 12.9, regular ≈ 70.5 ± 15.9 mm². A 563.6 mm² mean section would be a solid bar ~27 mm across, which is implausible for a lower rib. **Unverified**; step C5 settles it |
| **n-PPR** | §2.5: "We denote n-PPR as the spatial relation vector for the first n path points. For example, 2-PPR means the direction vector from the rib's start point to its next path point." Fig. 7: "normalized to a unit vector" | built from `path_points_relative_to_start` (each path point − start, mm, P/I/R, start first) or from `fixed_points_along_path`. Whether 4-PPR means three successive unit steps or three start-relative vectors is **not stated** | unit vectors (dimensionless) |
| rotation + mirroring | §2.5: "we use the orientation of each vertebra and multiply the inverted rotation matrix by the measured features to obtain rotations relative to each vertebra. Additionally, to be consistent, we mirror the left ribs onto the right side. This means that the right dimension always points away from the vertebra." | **not in the released code.** `calc_orientation=True` returns `vert_ori_rel_to_corpus` (unit vectors corpus → Direction_Posterior/Inferior/Right POIs); the rotation and the left-side R-sign flip have to be applied by us | — |

**The "articulation angle" is not an angle.** "Stump ribs articulate more posteriorly" is the PDRC, a distance in
mm. The paper has no rib-articulation angle feature. The code's `vert_ori_angle_degrees_PIR` gives the angles between
the **vertebra's** direction vectors and the image axes. It describes the vertebra's pose and nothing about the rib.

**The orientation features are the 2-PPR unit-vector components** (P, I, R; left ribs mirrored). There are no angle
features.

The code computes other features that the paper does not use: the same four families (`start_to_subregion`,
`closest_to_subregion`, `start_to_com`, `closest_to_com`, each direction + distance) for arcus (41), spinous process
(42) and inferior articular processes (47, 48); and `relative_mm_change_PIR`, the rib's bounding box relative to the
start, in mm.

---

## 5. Reported distributions (journal wording; arXiv identical unless noted)

| quantity | stump ribs | regular ribs | source |
|---|---|---|---|
| cohort | "2464 individual ribs across 648 subjects, all of which were the subject's lowest or second-lowest rib" | | §3.3 |
| stump count | "Of the 2464 ribs that we analyzed, 159 were stump ribs" (6.5 %) | | §3.3 |
| subjects with ≥1 stump | "Of the 648 subjects, 133 had at least one SR (20.5%), according to the 38mm length threshold" | | §3.3 |
| PDRC | −19.2 ± 3.8 mm | −13.8 ± 2.5 mm | §3.3: "(−19.2 ± 3.8 vs. −13.8 ± 2.5 mm, p-value < 0.01)" |
| volume/length | 260.6 ± 103.4 | 563.6 ± 127.1 ("mm2"; see section 4) | §3.3: "(260.6 ± 103.4 vs. 563.6 ± 127.1 mm2, p-value < 0.01, see Figure 6)" |
| 2-PPR posterior | 0.39 ± 0.17 | 0.64 ± 0.13 | §3.3: "The posterior component of stump ribs is smaller (0.39 ± 0.17 vs. 0.64 ± 0.13" |
| 2-PPR inferior | 0.32 ± 0.23 | 0.15 ± 0.30 | §3.3: "the inferior component is higher (0.32 ± 0.23 vs. 0.15 ± 0.30" |
| 2-PPR right (lateral) | 0.81 ± 0.11 | 0.68 ± 0.11 | §3.3: "right component of 2-PPR 0.81 ± 0.11 vs. 0.68 ± 0.11" |

All comparisons used the Wilcoxon rank-sum test (§2.7). The authors warn against reading PDRC as rib shape. §3.3: "most
samples' vertebrae had an enlarged fovea pushing the rib's beginning posteriorly, or an anomaly in the corpus region,
shifting the corpus center to an unnatural position. This indicates that the higher posterior distance is not due to
the morphology of the rib but rather to that of the vertebra."

**Cohort make-up** (journal Fig. 1, `mdpi_fig1.png`):
- The analysis set is "n=389|281" (RibFrac | VerSe). Excluded: "n=22". Final: "n=648". All of it is public data.
- The in-house data served "solely for training rib segmentation".
- The text gives a different exclusion count: "36 subjects in which the last rib is not visible in the image, 78 ribs
  for which the corresponding vertebra segmentation was missing, and two subjects with imaging artifacts" (§2.6). The
  paper does not reconcile 36 + 2 with 22.
- The paper does not give the stump share per dataset.
- The authors note the cohorts are enriched. §4: "they do not represent the general population ... we observe more
  stump ribs in our data." Their 20.5 % of subjects compares with 12.4 % stump twelfth ribs in CTSP (ratio rule) and
  12.6 % in Nagata 2025.

---

## 6. Classifiers and their scores

**Setup.** Journal §2.6:
- Features: "we use the DRC features as input for a Support Vector Machine (SVM) ... We also used n-PPR ... with n set
  to 2, 3, and 4 ... Going beyond n = 4 would yield a measured length close to or beyond the SR threshold".
- Validation: "10 different fixed seeds and a random 70/30 train/test subject-wise split ... We report the F1,
  balanced accuracy, and AUC scores averaged over the 10 runs. Additionally, we compare this setup to logistic
  regression (LoRe) and multilayer perceptron (MLP). We did not address class imbalance for this, other than ensuring
  approximately equal numbers of SR cases across splits. Input features were always normalized based on the mean and
  standard deviation across the training samples of a split."
- Not stated: the SVM C, the polynomial degree (arXiv: "polynomial kernel of degree 5") and the MLP architecture.
- The repository contains **no classifier code or weights**. The labels are the 38 mm rule on full-length ribs.

**Journal Table 5 and Table A3** (mean ± SD over 10 seeds):

| features | linear SVM F1 | poly SVM F1 | LoRe F1 | MLP F1 | linear SVM AUC | linear SVM bal. acc. | linear SVM precision / recall |
|---|---|---|---|---|---|---|---|
| DRC | 0.61 ± 0.06 | 0.59 ± 0.05 | 0.63 ± 0.08 | 0.62 ± 0.06 | 0.94 ± 0.02 | 0.73 ± 0.03 | 0.89 ± 0.09 / 0.47 ± 0.07 |
| 2-PPR | 0.37 ± 0.07 | 0.51 ± 0.04 | 0.56 ± 0.05 | 0.57 ± 0.04 | 0.92 ± 0.02 | 0.61 ± 0.03 | 0.98 ± 0.03 / 0.23 ± 0.05 |
| 3-PPR | 0.7 ± 0.04 | 0.67 ± 0.05 | 0.72 ± 0.03 | 0.71 ± 0.03 | 0.97 ± 0.02 | 0.81 ± 0.03 | 0.8 ± 0.08 / 0.62 ± 0.06 |
| 4-PPR | 0.84 ± 0.02 | 0.77 ± 0.04 | 0.83 ± 0.04 | 0.84 ± 0.02 | 0.98 ± 0.01 | 0.88 ± 0.01 | 0.95 ± 0.04 / 0.76 ± 0.02 |
| DRC + 2-PPR | 0.7 ± 0.06 | 0.63 ± 0.06 | 0.7 ± 0.04 | 0.67 ± 0.06 | 0.96 ± 0.02 | 0.79 ± 0.03 | 0.86 ± 0.07 / 0.59 ± 0.06 |
| DRC + 3-PPR | 0.77 ± 0.06 | 0.69 ± 0.06 | 0.77 ± 0.05 | 0.75 ± 0.04 | 0.97 ± 0.02 | 0.86 ± 0.04 | 0.82 ± 0.08 / 0.74 ± 0.08 |
| **DRC + 4-PPR** | **0.84 ± 0.03** | 0.76 ± 0.05 | 0.83 ± 0.04 | **0.84 ± 0.04** | **0.98 ± 0.02** | 0.89 ± 0.02 | **0.91 ± 0.06 / 0.78 ± 0.03** |

Journal §3.3: "We achieved the best F1 performance of 0.84 by using both 4-PPR and DRC as inputs to an MLP or linear SVM."

**Differences from arXiv v1** (cite the journal):
- arXiv reports SVMs only and F1 only.
- Polynomial SVM on 4-PPR: "0.82 ± 0.04" in arXiv, 0.77 ± 0.04 in the journal.
- Polynomial 3-PPR: "0.7 ± 0.04" in arXiv, 0.67 ± 0.05 in the journal.
- DRC: "0.62 ± 0.05" in arXiv, 0.59 ± 0.05 in the journal.
- DRC + 4-PPR linear: "0.84 ± 0.04" in arXiv, 0.84 ± 0.03 in the journal.
- The in-house cohort is 143 subjects in the arXiv Table 1 and 413 in the journal.
- Appendices C and E–G appear only in the journal.

**What "partial view" means here.** The 0.84 comes from the first 4 path points (about 22 mm) of ribs whose label
came from their whole length. Ribs cut by the field below 38 mm were excluded from evaluation (Likert 3 kept only
above threshold). **No experiment tests the classifier on ribs that are actually truncated.** Journal App. F: a 3D
CNN on the grey-scale image reaches F1 0.84 ± 0.03 on a cut rib and 0.90 ± 0.02 on the whole rib. App. E: regressing
whole-rib length from the same features gives "the best MAE of 2.33 ± 0.07" cm: "we are more than half a stump rib's
length wrong ... we cannot recommend this approach."

---

## 7. `run_all_steps`: inputs and returned fields

```python
run_all_steps(rib_mask: NII, vertebra_instance_mask: NII, vertebra_semantic_mask: NII,
              poi: POI | None = None, calc_orientation: bool = False, verbose: bool = False) -> list[dict]
```

The function runs three steps:
1. `assign_ribs_to_vert_segmentation`: rib connected components are matched to vertebrae 7–20. For each vertebra and
   side, the candidate box is the costal process + arcus + superior articular process, upper half, widened 10 voxels
   laterally. Dominance = component volume / box distance; greedy, one rib per vertebra side.
2. `measure_rib_length_subject`: the lowest ≤3 levels.
3. `calc_rib_features` per rib.

**Input conventions (TPTBox; verified in `vert_constants.py`):**
- Vertebra ids: C1–C7 = 1–7, T1–T12 = 8–19, **T13 = 28**, L1–L5 = 20–24, **L6 = 25**, S1 = 26, coccyx = 27.
  VERIDAH writes these ids.
- Rib instance id = vertebra + 32. That gives C6 38, C7 39, T1 40 … T12 51, L1 52, and T13 53 (special-cased). **One
  id covers both sides.** Side lives only in the semantic mask: Rib_Left 63, Rib_Right 64. L2–L6 have no rib id.
- Semantic subregions (SPINEPS `seg-spine_msk`): arcus 41, spinous 42, costal process L/R 43/44, superior articular
  L/R 45/46, inferior articular L/R 47/48, corpus border 49, corpus 50.
- The rib mask must be binary 1. All three masks need the **same affine** (`assert_affine`), and all are reoriented
  to PIR internally.

**Each dict in the returned list is one (vertebra, side) rib:**

| key | set by | content |
|---|---|---|
| `vertebra` | measure_rib_length_subject | VerSe/TPTBox vertebra id the rib was assigned to |
| `side` | 〃 | `"left"` / `"right"` |
| `is_last_v` | 〃 | True for the lowest measured level (numeric order; see D2) |
| `vert_ori_rel_to_corpus` | 〃 | dict {128 posterior, 129 inferior, 130 right: unit vector from corpus}, or None if `calc_orientation=False` |
| `vert_ori_angle_degrees_PIR` | 〃 | angles (deg) of those vectors to the image P, I, R axes, or None |
| `orig_zoom` | measure_one_rib_length | native voxel size |
| `rib_length` | rib_length_algorithm | path length, mm |
| `sr` | 〃 | True / False / None (section 2) |
| `seg_at_border` | 〃 | rib reaches the crop (≈ field) edge |
| `rib_volume` | 〃 | **voxel count** at 0.5 mm after closing |
| `start_point`, `end_point` | 〃 | voxel coords in the 0.5 mm **crop** (world coordinates need `rib_seg_cropped.affine`) |
| `fixed_points_along_path` | 〃 | ordered dict idx → {`coord`, `prior`, `prior_distance` (mm), `endpoint`} |
| `darr` | 〃 | full 0.5 mm debug array of the crop (large) |
| `debug` | 〃 | None unless `return_debug_data` |
| `rib_seg_cropped`, `sem_vert_cropped` | 〃 | NII objects (0.5 mm crop of rib and vertebra subregions) |
| `features` | calc_rib_features | dict: `path_points_relative_to_start` (list of (P,I,R) mm); `relative_mm_change_PIR` (3 × (min,max) mm); for each s in {41, 42, 47, 48, 49} present: `{s}_start_to_subregion_direction/_distance`, `{s}_closest_to_subregion_direction/_distance`, `{s}_start_to_com_direction/_distance`, `{s}_closest_to_com_direction/_distance` (mm) |

`run_all_steps` does **not** return the combined rib + vertebra instance or semantic masks, although
`assign_ribs_to_vert_segmentation` produces both. It also **mutates its inputs**: it binarises the rib mask, and
`vert_seg.apply_mask(..., inplace=True)` removes vertebra voxels under ribs before writing rib ids into the vertebra
mask. Pass copies.

---

## 8. What the rule uses, and the rule (a proposal, to be frozen in `PREREG_rules.md` after calibration)

**Fields used, per rib row:** `vertebra`, `side`, `is_last_v`, `rib_length`, `sr`, `seg_at_border`, `rib_volume`,
`fixed_points_along_path`, `features.path_points_relative_to_start`, `features.49_start_to_com_direction`,
`features.49_start_to_subregion_direction`, `features.relative_mm_change_PIR`, `vert_ori_rel_to_corpus`.

**Per person, from the saved instance mask (patch P8):** the list of vertebrae carrying an assigned rib on each side,
their rib component volumes, and the unassigned rib components (id 255).

- **S1, length (primary, Möller/Wigh).** For each rib at the lowest rib-bearing level:
  - STUMP if `rib_length ≤ 38.0` and not `seg_at_border`.
  - FULL if `rib_length > 38.0`.
  - UNDECIDED otherwise.
  - Also report the level above (run_all_steps measures it), because a unilateral T12 stump beneath a normal T11 is
    the common form.
- **S2, morphology (only for UNDECIDED ribs).** The DRC + 4-PPR linear SVM (or LoRe) retrained on the calibration set
  (C8). Apply it only when the rib has at least 4 path points (about 22 mm visible). Otherwise the rib stays
  UNDECIDED. Report its score, not only the class. Its published precision/recall (0.91 / 0.78) came from 6.5 %
  prevalence and simulated partial views.
- **S3, ratio (secondary, CTSP-native).**
  - `rib_length(last level, side) / rib_length(level above, same side)`, only when neither rib is `seg_at_border`.
  - Cut = the valley of the calibrated distribution, if C6 finds two modes. If it does not, S3 is dropped and the
    report says so.
  - Report S1 × S3 disagreements for rendering.
- **Descriptive only** (not decision rules; Fig. 6 and Fig. 7 overlap): volume/length, PDRC, the 2-PPR components.
  These go to the renders and to Greg's T13 question ("stump rib combined with some weird shape vertebra").
- **Guards**
  - G1, broken rib: an unassigned component (255) within 10 mm of the measured rib's `end_point`, in world
    coordinates → BROKEN?, no stump call. Split ribs are the paper's named failure mode; RibFrac is a fracture cohort.
  - G2, false rib: a "rib" on L1 that touches the costal process over most of its length → COSTAL-PROCESS?. Journal
    App. B (D): "the segmentation model confused the costal process with a rib".
  - G3, level: the rib's `vertebra` must be the VERIDAH level the count uses. Disagreement with arm A's TS rib number
    is logged, not overridden.
  - G4, missing corpus: no label 49/50 for that vertebra → no measurement. The upstream code asserts and aborts the case.
- **Output per person.** `last_rib_level` (VERIDAH id, including 28), `stump_left`/`stump_right` ∈ {STUMP, FULL,
  UNDECIDED, BROKEN?, ABSENT}, `stump_bilateral`, the S2 score, the S3 ratio, the descriptive features. ABSENT means
  there is no rib on that side at a level whose other side has one, and the side is not at the field edge; it is the
  aplastic candidate.
- **What the rule does not decide.** Naming, i.e. T12 stump vs L1 lumbar rib vs T13 stump. CTSP's own figure: "Nothing
  in the rib decided that" (`main.tex` L605). The level comes from the rib-free count against the Dataset803 sacrum
  and from local vertebral morphology.

---

## 9. Inputs arm B needs for this rule, per CT

1. **Rib mask.** Möller's nnU-Net, weights `~/CTSpinoPelvic1K/models/moller_ribseg/ribseg_model_weights/`
   (`dataset.json`, `plans.json`, `fold_0..2/checkpoint_final.pth`; already on the grid per `CORPUS.md`).
   - Trained at 0.8 mm isotropic, patch 192³ (journal §2.2).
   - Our scripts default to **fold 0, mirroring off**: `slurm/spineps_bench.sh` `RIB_FOLDS=0`, and
     `build_v4_ribs.py`/`spineps_ct_pipeline.py` set `use_mirroring=False`.
   - The paper does not say how folds were combined; nnU-Net's default ensembles all folds with mirroring. For "best
     fidelity" use folds 0,1,2 with mirroring. At minimum, measure the difference on the 41 manual VerSe masks (C1)
     before choosing.
2. **Vertebra instance mask.** SPINEPS + VERIDAH `*_seg-vert_msk.nii.gz`, VerSe-coded. Raw-id masks from before
   147428d are relabelled first (`tools/spineps_ids.py`).
3. **Vertebra semantic mask.** SPINEPS `*_seg-spine_msk.nii.gz` (subregions 41–50).
4. **POIs for orientation.** Computed by us with TPTBox `calc_poi_from_subreg_vert(inst, sem,
   subreg_id=[Vertebra_Corpus, Vertebra_Direction_Posterior, Vertebra_Direction_Inferior, Vertebra_Direction_Right])`
   and passed as `poi=` (see D5).
5. **Code.** The rib-segmentation clone at a pinned commit (10998cd) with patches P1–P8 in
   `/rs/rs_grp_oschome/go2432/ruleclass/code/`. The TPTBox version is recorded (the journal used 0.4.2; `main` is
   1.0.0). `calc_poi_labeled_buffered` is still exported as an alias of `calc_poi_from_two_segs`, so imports resolve.
6. **Container.** `ctspinopelvic1k-spineps.sif` is absent (TOOLCHAIN AUDIT). Build or pull it inside an sbatch job
   (mksquashfs is not on the login node), or run from `~/mambaforge/envs/spineps` with the clone on `PYTHONPATH`.
7. **Memory.** Journal §2.9: "more than 100 GB of available RAM". The per-rib `cdist` between rib voxels (±20 mm
   window, 0.5 mm) and the whole corpus (0.5 mm) is the likely reason. P4 replaces it.

**Label-scheme traps (CLAUDE.md: mixing schemes returns a plausible wrong answer):**
- TPTBox rib ids 38–53 overlap CTSP v11 rib ids 34–59 with different meanings. TPTBox 51 is the T12 rib, both sides;
  CTSP 51 is a right rib by v11's own numbering.
- SPINEPS semantic 60/61 are spinal cord and canal; CTSP v11 60/61 are lumbar ribs L/R.
- Never resolve a Möller/TPTBox mask through `ostk.labels.labels_for` unless a `tptbox` scheme is added to it.
- Keep case ids `zfill(4)` for CTSP joins.
- Never reorient when writing: TPTBox `reorient_()` works in place and `assign_ribs_to_vert` returns
  `reorient_(ori)`. Any mask we save goes back through the source CT's affine and is checked.

---

## 10. Calibration with the Zenodo record

**What is in record 14864106** (sizes and md5 from the Zenodo API; counts from the zip listings):

| file | bytes | md5 | contents | on the grid? (`CORPUS.md`) |
|---|---|---|---|---|
| `verse_rib_manual.zip` | 6,433,167 | 46ab8987e476cc5da23920e27a9c6e67 | 41 masks, 41 subjects (`sub-verseNNN[_dir-iso/ax/sag]_seg-rib_msk.nii.gz`); verse006 is empty per CORPUS.md | yes: `~/data/ribs/verse_rib_manual.zip`, unpacked at `~/data/ribs/x/verse_rib_manual/` |
| `verse_rib_predictions.zip` | 82,776,945 | 4ad34c16682d3572681757d966ccccb4 | 337 masks, 319 subjects; 36 `split-verseMMM` masks for the 18 multi-series subjects; none for the 30 VerSe'19 `gl*` series or for verse006/048/116/146/202/707/756 | yes, `~/data/ribs/verse_rib_predictions.zip`, **not unpacked** |
| `ribfrac_rib_manual.zip` | 14,195,070 | 61ebb5fa09d67edacb506b1e0230a946 | 31 masks, 31 subjects | 31 manual masks noted as on disk (path not recorded in CORPUS.md) |
| `ribfrac_rib_predictions.zip` | 199,464,174 | db2dc940c35faeaf71554ab293205ca6 | 420 masks, 420 subjects | **no**: download |
| `ribseg_model_weights.zip` | 695,671,169 | a3fa6ac14de2c23c6299f61c36ce0fad | `dataset.json`, `plans.json`, `dataset_fingerprint.json`, `inference_config.json`, `fold_0..2/checkpoint_final.pth` (249.8 MB each) | yes, unzipped |

Zenodo description: "The segmentation masks are binary and differentiate between rib (1) and background (0)."
The manual sets match the paper: "Manually corrected (n=31|42)" (Fig. 1).

**Not in the record:**
- per-rib lengths, stump labels or features;
- vertebra masks (VerSe's own GT is used for VerSe; RibFrac "ships no vertebra masks"; the paper used Bonescreen SpineR
  there);
- the Likert ratings;
- the classifier.

`docs/DATASETS_ROADMAP.md` L145 says the record holds "stump-rib masks". That is wrong: it holds rib masks only.

**Download (only the RibFrac predictions are missing).** Run as an sbatch job on `reqp --qos=requeue`, because the
login node does no work and compute nodes have internet. Write to `/rs/rs_grp_oschome/go2432/ruleclass/moller_zenodo/`:
`curl -L -o ribfrac_rib_predictions.zip https://zenodo.org/api/records/14864106/files/ribfrac_rib_predictions.zip/content`,
then check the md5 above and unzip. Do the same for any zip found missing, and re-check the md5 of the three already
on disk. Unpack `verse_rib_predictions.zip` there too, about 83 MB. Total new data ≈ 285 MB.

**Calibration steps** (VerSe first; everything is sbatch; outputs under `ruleclass/calib/`):

- **C0, join.** Map `sub-verseNNN[_dir-*]` and `split-verseMMM` to VerSeFusion `scan-<sid>` via
  `~/VerSeFusion/data/manifest/manifest.csv`. Check the rib mask's affine against the VerSe CT and against the SPINEPS
  outputs; resample the rib mask (nearest) to the vertebra grid only if the shapes differ, as `spineps_ct_pipeline.py`
  does.
- **C1, the paper's cohort.**
  - Run patched `run_all_steps` with `calc_orientation` through our own POIs.
  - Inputs: Möller **predicted** masks on the ~281 VerSe subjects **not** in the manual set (the paper's analysis set
    excluded the manually corrected subjects), VerSe GT instance masks (as the paper did: "The VerSe data already
    contained expert-level annotations"), and SPINEPS semantic masks.
  - Repeat with the VERIDAH instance mask. The difference between the two runs measures what the labeler does to
    assignment and level.
  - On the 40 subjects with both a manual and a predicted mask, compare lengths. Target, App. C: "Most differences are
    below 1 mm".
- **C2, the paper's reference numbers** (pooled VerSe + RibFrac in the paper; VerSe-only numbers may differ, so do
  not force them). Compare **mean and SD**, not the median:
  - share of stump ribs among the lowest-two ribs: 159/2464 = 6.5 %;
  - share of subjects with ≥1 stump: 20.5 %;
  - share of ribs at the edge: Likert (3) 12.2 %;
  - PDRC −19.2 ± 3.8 vs −13.8 ± 2.5 mm;
  - 2-PPR P 0.39 ± 0.17 vs 0.64 ± 0.13, I 0.32 ± 0.23 vs 0.15 ± 0.30, R 0.81 ± 0.11 vs 0.68 ± 0.11.

  Proposed pass bar: each class mean within 0.25 of the paper's SD, and each SD within ±25 %. A miss is rendered (rib
  mask + path points over the CT) before any explanation is believed.
- **C3, PDRC key.** Settle whether PDRC is `49_start_to_com_direction[0]` or `49_closest_to_com_direction[0]` by
  which one reproduces −19.2/−13.8 after rotation into the vertebra frame.
- **C4, reader standard (outside the computation).**
  - Reference: the stump-rib column of Löffler et al. 2021 Suppl. Table 1 (two neuroradiologists in consensus; level
    T12/L1/T13; `~/lstv_flag/sources/verse_suppl_table1.csv`, 325 subjects; classifier R7). Compute subject-level
    sensitivity and precision of S1.
  - Bar to beat: our re-implementation R27 (`~/lstv_flag/sources/moller_stump_ribs.csv`), "sensitivity 65.7 % on 210
    comparable, precision 90.2 %".
  - CLASSIFIERS.md notes that Löffler's table follows the same 38 mm rule, and a both-sides convention that R27 did
    not enforce. Score it both ways.
- **C5, volume/length unit.** Compute `rib_volume / rib_length` as is and ×0.125. The version that reproduces
  260.6/563.6 fixes the unit. Neither reproducing it means the paper's volume was computed another way, and the doc is
  corrected.
- **C6, the ratio.**
  - On VerSe, and on CTSP 801 once arm B has run, compute the last/above length ratio for untruncated same-side pairs.
  - Test for two modes: a 1- against 2-component Gaussian mixture by BIC, plus a KDE valley with Silverman bandwidth.
  - Take the cut at the valley.
  - Compare with CTSP's PCA-extent ratio on the same ribs; the chord-vs-arc bias should show as a shift.
  - This is also the lab journal's untested truncation check, now on untruncated pairs only.
- **C7, RibFrac.**
  - Inputs: 420 predicted masks + SPINEPS/VERIDAH (655 of 660 have SPINEPS). RibFrac is the paper's other 389
    subjects and mostly thoracic, so it serves the T13 question.
  - Run guard G1 there: fractures split ribs.
  - RibSeg v2 per-rib labels (660, zipped) can check the assigned level.
- **C8, classifier.**
  - Data: the C1 + C7 rows labelled by S1 on untruncated ribs.
  - Retrain DRC + 4-PPR linear SVM and LoRe: 10 seeds, 70/30 split by subject, z-scored on the training split,
    no rebalancing (the paper's setup).
  - Targets: F1 ≈ 0.84, AUC ≈ 0.98.
  - Freeze the model and record it in `PREREG_rules.md` before any corpus row is scored.

---

## 11. Code defects and traps found (upstream `rib-segmentation` @10998cd, and our wrapper)

- **D1. T13 is never assigned a rib.** `assign_ribs_to_vert.py` L78: `if v >= 21 or v < 7: continue` skips 28. A T13's
  rib stays unassigned (255), or, if it falls in L1's box, is written as L1's rib (52), a "lumbar rib". Measurement
  then never sees the T13 stump. **P1:** allow 28 in the loop.
- **D2. Numeric sort** (`run_algorithm.py` L36) places T13 after L1. **P2:** sort by `Vertebra_Instance.order()`.
- **D3. One bad rib kills the case.** An empty crop makes `rib_length_algorithm` return `{"debug": ...}`, and
  `measure_one_rib_length` then raises `KeyError: 'sr'`. A vertebra with no corpus label fails the
  `assert Location.Vertebra_Corpus_border.value in sem_vr_labels`. `spineps_ct_pipeline.measure_ribs` catches this
  per case, so all ribs of the CT are lost. **P3:** try/except per rib; record the reason.
- **D4. Memory.** `calc_rib_features` L54 runs `fast_cdist(rib_point_arr_mm, subreg_point_arr_mm)`: a dense matrix of
  rib voxels in a ±40-voxel window × every voxel of the subregion at 0.5 mm. For the corpus that is roughly 10⁴ × 10⁵
  pairs, which is gigabytes per rib. **P4:** `scipy.spatial.cKDTree` nearest-neighbour query, same argmin. Verify
  equality on 20 ribs.
- **D5. Orientation path.** `run_algorithm.py` L63–67 computes the POIs with
  `out_path=__file__.join("poi.json")`. That is `str.join`, which yields a nonsense relative path (`p/opt/ribseg/...pyo/opt/...`).
  TPTBox saves the POI there, and the parent directory does not exist. It asks only for Corpus + Direction_Posterior,
  while `calc_orientation_from_poi` asserts that Inferior and Right are present. Untested; it probably fails. **P6:**
  compute the POIs ourselves and pass `poi=`.
- **D6. Our wrapper writes `darr` into JSON.** `spineps_ct_pipeline._jsonable` turns every ndarray into a list, and
  `darr` is the whole 0.5 mm crop, on the order of 10⁷ voxels per rib. The JSON would reach hundreds of MB per CT;
  `TIERS.md` budgets "about 0.1 MB". **P5:** drop `darr`, `debug`, `rib_seg_cropped`, `sem_vert_cropped`; add
  `rib_seg_cropped.affine` so path points can be drawn in world coordinates.
- **D7. The instance mask is never saved.** `spineps_ct_pipeline.py`'s docstring promises
  `<case>_rib-{inst,sem}_msk.nii.gz`, but `measure_ribs` only creates the directory. **P8:** call
  `assign_ribs_to_vert_segmentation` directly, save both masks (source CT affine, no reorientation), then call
  `measure_rib_length_subject` and `calc_rib_features`. These three calls are exactly `run_all_steps`.
- **D8. Inputs are mutated in place** (section 7). Use copies.
- **D9. Rib inference settings** (section 9, item 1): fold 0 without mirroring is not the published configuration.
- **D10. Paper vs code on the fill step.** The paper says "filled 3D holes"; the code runs a 1-voxel closing. This
  matters only for `rib_volume`.

---

## 12. What is not known

- The unit of the volume-to-length ratio: the journal says mm², the code suggests voxels/mm (C5).
- Which feature key the PDRC and the classifier's DRC use, and whether 4-PPR is step vectors or start-relative vectors
  (C3, C8).
- How the three folds were combined at inference in the paper.
- The stump share per dataset (VerSe vs RibFrac). The paper pools them.
- The paper's exclusion count: 36 + 2 subjects in the text against 22 in Fig. 1.
- Why F1 peaks near 41 mm in arXiv A.2. The authors: "for which we can offer no explanation."
- Whether CTSP's PCA-extent bimodality survives on untruncated ribs, and whether it survives on path lengths (C6).
- Runtime per CT for the rib nnU-Net and the features on our hardware. The paper reports only "approximately 30 h"
  of training on an A40. Measure on a tier-1 pilot before sizing tier 2.
