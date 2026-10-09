# PREREG_rules — the transitional-vertebra screen over the CT census

**Status: DRAFT v1, 2026-09-27, awaiting Greg's sign-off. Not frozen.** Until the freeze line at the end is filled,
every number this document produces is calibration, not a result. Once frozen, its SHA-256 is written into every
output row of `tools/anomaly_rules.py`, and a change is a new dated version, never an edit.

This document states, before any census row is scored, what each rule measures, from which segmentation, with which
threshold, what it is meant to catch, how the rules combine into a flag, what the sensitivity / specificity sweet spot
is defined to be, and what outside the computation each result is checked against. It supersedes nothing: the rule set
as Greg stated it on 2026-09-26 23:00 is `docs/RESUME_2026-09-22_PM.md` L116-122 (three rules); the lowest-rib ratio
and the MDPA thoraco-lumbar AUC were added on 2026-09-27. The design behind rules 2 and 3 is `ARM_B_pelvis.md` §7-8
and `STUMP_RULE.md` §8 beside this file; the sixth-body morphology is `MORPH_API.md` §6.

## 0. Population, inputs, and the traps

- **Population.** The SUPER DETECTOR RUN census, `/rs/rs_grp_oschome/go2432/ruleclass/tiers/` (tier 1 5,094, tier 2
  12,217, untiered 4,311; 21,622 rows; `CORPUS.md` says 21,655 and the 33-CT difference is unexplained and must be
  resolved before the census table is final). PANORAMA's 1,495 masks and 131 review calls of 2026-09-27 12:23 are not
  in the tiers; the tier lists are rebuilt before scoring.
- **Paired subset.** Only 850 CTs have a radiograph of the same person: COBRA 692 (kV projection sweeps + RTK
  geometry; every mask lives on the deformed `ct_def`, not `ct_original`), C-ArmLSpine 149 (2 spot frames + CBCT;
  poses on disk), 9 cadaver / phantom. Every other census CT is CT-only.
- **Inputs, per CT, all already on disk or being written by the arms:**
  1. SPINEPS + VERIDAH instance (`seg-vert`) and semantic (`seg-spine`) masks, VerSe-coded (L6 = 25, sacrum = 26,
     T13 = 28). Stores harvested before 147428d carry raw ids 1..N and are read only through
     `tools/spineps_ids.relabel_by_ctd`, or refused.
  2. Möller rib nnU-Net (arm B, config fast): `<case>_rib-inst_msk.nii.gz` (rib id = vertebra id + 32; 255 =
     unassigned), `<case>_rib_measurements.csv` (`rib_length` along the path in mm, `sr`, `seg_at_border`,
     `vertebra`, `side`, `is_last_v`), `_done/<case>.measure.json` (`levels_<variant>.rib_bearing`).
  3. TotalSegmentator 2.18.0 `total` (arm A): sacrum 25, `vertebrae_S1` 26 (the sacrum is their UNION), hips 77/78,
     femora 75/76, ribs 92-115 (rib heads often missing: TS ribs alone are not a count).
  4. Dataset803 pelvis (arm B pelvis, after `pelvis_post.py`): sacrum 26, hips 30/31 in VerSe-native ids; the raw
     prediction under `_work/` (1-9) is never read.
  5. CTSpinoPelvic1K v11 labels for the 802 release records (identifier 29 retired; `labels_v10/` carries it and is
     not read).
- **Label-scheme rule.** A mask is resolved through `ostk.labels.labels_for(volume)` only if it is a CTSP or
  Dataset803-post output; SPINEPS, TPTBox and TS masks have their own maps and are never passed through it. Case ids
  are `zfill(4)` for CTSP joins. Nothing is reoriented when written.
- **Field gate ("both in field").** A rule that needs the lumbosacral junction requires the sacrum in field
  (>= 5 mL, not touching the caudal slice); a rule that needs the thoraco-lumbar junction requires the lowest
  rib-bearing vertebra with a whole rib. A CT that fails the gate a rule needs is `no_count` for that rule, never
  ordinary.

## 1. Rule 1 — the rib-free lumbar count

**Definition.** The number of free presacral vertebral bodies strictly between the lowest rib-bearing vertebra and the
cranial end of the sacrum. Five is ordinary; six is L6 or a T12 that has lost its rib; four is a fused L5 / four-lumbar
spine or a lumbar rib on L1.

**Inputs and computation.**
- Bodies: SPINEPS/VERIDAH instances 19-25 and 28.
- Rib-bearing: a vertebra is rib-bearing if Möller assigns it a rib of `rib_length > 38.0` mm on at least one side
  (Löffler et al. 2021 Suppl. Table 1 rule; Wigh 1980). A vertebra whose only ribs are <= 38 mm is **not** rib-bearing
  for the count and is passed to rule 3.
- Anchor: the cranial end of the Dataset803 sacrum — the SPINEPS sacral end-plate (subregion 74) where it lies inside
  the Dataset803 sacrum, else `sacrum_top_S_mm`. Until Dataset803 exists for a CT, the anchor is the TS sacrum ∪ S1,
  and the row says so (`anchor_source`).
- Per instance, `f = |instance ∩ sacrum| / |instance|`: `f < 0.10` free (counted); `0.10 <= f < 0.50` contact
  (counted, flagged `castellvi_II_IV_candidate`); `f >= 0.50` absorbed (not counted, flagged
  `complete_sacralisation_candidate`). A free body wholly below the anchor is flagged `lumbarisation_candidate`.
- `no_anchor` when the sacrum is absent or < 5 mL, touches the caudal slice, or the Dataset803 and TS anchors differ
  by more than 20 mm with no ground truth; such a CT goes to adjudication, not to a guess.
- The SPINEPS-vs-TotalSegmentator confusion signal Greg proposed for sacralisation and lumbar ribs is operationalised
  as: `absorbed` under the Dataset803 anchor differs from `absorbed` under the TS anchor.

**Output.** `count ∈ {4, 5, 6, no_count}`, `anchor_source`, the per-body `f`, the flags above, and the level id of the
most cranial rib-free body.

**What it cannot decide alone.** Six: L6 versus a rib-less T12 (rule 1b). Four: fused L5 versus a lumbar rib on L1
(rule 2 and rule 3).

**Existing implementations it replaces on the census:** `tools/acquisition_screen.py` (labeller B, TS geometry,
short rib 40 mm), `tools/rib_count_reader.py` (reader C, 38 mm), `tools/harvest_verse_registry.py`,
`tools/cobra_lstv_screen.py`, `scripts/extract_transition_morphometrics.py` (CTSP labels). Their calls are kept as
comparators in the census table, not discarded.

## 1b. Rule 1b — the shape of the sixth rib-free body (thoracic or lumbar)

Applied only when rule 1 returns six. The most cranial rib-free body is classified thoracic (-> TL-11, an ordinary
lumbosacral count with an aplastic twelfth rib) or lumbar (-> LS-L6) or intermediate (-> TLTV, reported not forced),
after Schinz et al. 2026 (Eur Spine J 35:2195).

- **Features, per side, in the vertebra's own frame, from SPINEPS subregions:** F1 superior-facet-joint angle
  (45/46 vs 47/48; probe: thoracic 72-83°, upper lumbar 21-47° on the mean of sides); F2 costal-process AP offset
  from the superior articular process (43/44 vs 45/46; thoracic 5-8 mm posterior, lumbar 2-6 mm anterior); F3 process
  shape (`tp_metrics`: reach, thickness, slenderness; tip-to-tip span over the case's median span). Never a feature:
  list position, raw millimetres, rib presence, any segmenter's level name.
- **Decision.** A logistic model on F1-F3 trained on named T12 and L1 bodies of the reference set (CTSP read
  levels + VerSe), frozen before scoring. `P(thoracic) >= 0.80` thoracic; `<= 0.20` lumbar; between = TLTV.
- **CTSP fallback** where subregions are unavailable: `scripts/six_lumbar_readings.py` z-scores (tp_height_max,
  tp_gap_ilium_min, disc_low, sacrum_height; ratio < 0.33 -> stump; shift <= -5 -> aplastic; sacral z >= 1.5 or
  sacrum-height z <= -2 -> lumbarised S1). On the 18 CTSP six-lumbar spines this gave A 11 / C 4 / B 1 / B-or-C 2.
- **Not yet done:** the three-case probe is unrendered; no SPINEPS-mask version of the classifier exists.

## 2. Rule 2 — pelvis and sacral morphology

Meant to catch complete sacralisation (a fused L5 absorbed into the sacrum label), a lumbarised S1, and to separate a
four-count from a lumbar rib.

- **Inputs:** the Dataset803 sacrum (largest component) and hips, in world mm; SPINEPS 70/71 (alae) and 74 (plate)
  inside it; the TS sacrum ∪ S1 and hips as the second labeller.
- **Features:** (a) sacral top relative to the iliac crests (`sacrum_top_S` minus the mean crest top; an absorbed
  L5 raises the base toward the crest line, a free S1 lowers it); (b) ala-to-ala width at the top plate; (c) fused-
  segment count under the plate (vestigial disc bands along the midline curve); (d) top-plate width over the lowest
  presacral body's inferior plate width; (e) the A-vs-B `absorbed` disagreement of rule 1.
- **Normal.** The central 95 % of each feature on the **reference half**: adults (children excluded — an unfused S1
  is normal in a child) whose rule-1 count is five with every existing labeller agreeing, split by person into a
  reference half and a test half. Thresholds are frozen on the reference half before anything else is classified.
- **What is on file and what is not.** Every previously tried pelvic cue on CTSP was falsified or weak (ala rise AUC
  0.450 / 0.415, sacral bulk 0.551, asymmetry 0.599; `docs/CASTELLVI_SCREEN_BLIND_SPOT.md`). No published accuracy
  exists for the intercrestal line in this project. **This rule has no validated threshold yet;** it is scored, its
  distribution reported, and it gates nothing until the reference-half freeze.
- **In-sample warning.** Dataset803 was trained on CTSpine1K + CTPelvic1K + COLONOG (979 CTs) and 440 of the 802
  CTSP pelvis labels are its own out-of-fold pseudo-labels, so on CTSP and CTPelvic1K its agreement with "GT" is
  model-vs-model. The outside check for rule 2 is agreement with the TS pelvis on every other collection
  (`pelvis_agree`), and the 54 held-out CTSP records with a manual pelvis.

## 3. Rule 3 — the lowest rib against the rib above (stump rib)

Meant to catch a hypoplastic twelfth rib (which turns a six into an ordinary count) and a lumbar rib on L1 (which
turns a four into an ordinary count). It does not name the level.

- **S1, length (primary; Möller / Wigh / Löffler).** At the lowest rib-bearing level, per side: STUMP if
  `rib_length <= 38.0` and not `seg_at_border`; FULL if `> 38.0`; UNDECIDED otherwise. The level above is reported
  too (a unilateral T12 stump under a normal T11 is the common form).
- **S3, ratio (secondary; CTSP-native).** `rib_length(last, side) / rib_length(above, same side)`, both untruncated.
  The cut is **the valley of the calibrated distribution on Möller path lengths** (1- vs 2-component Gaussian
  mixture by BIC, plus a KDE valley with Silverman bandwidth), on VerSe and on CTSP 801 once arm B has run. The
  CTSP PCA-extent cut (0.33 in `six_lumbar_readings.py`, 0.30 in `MORPH_API.md`; modes 0.68 and 0.32) is **not**
  carried over: a chord under-reads a curved full rib and not a straight stump. If no bimodality is found, S3 is
  dropped and the report says so.
- **Guards.** G1 broken rib (an unassigned component within 10 mm of the measured end -> BROKEN?, no call; RibFrac
  is a fracture cohort); G2 false rib (a "rib" on L1 that runs along the costal process -> COSTAL-PROCESS?); G3 level
  (the rib's vertebra must be the VERIDAH level the count uses; TS disagreement logged, not overriding); G4 no corpus
  label -> no measurement.
- **Output per person.** `last_rib_level`, `stump_left`/`stump_right` ∈ {STUMP, FULL, UNDECIDED, BROKEN?, ABSENT},
  `stump_bilateral`, the S3 ratio, S1 × S3 disagreements (rendered).
- **Both published conventions are reported** because they number differently: RBC (Wigh) keeps a < 38 mm rib's
  vertebra thoracic; RLBC calls a vertebra with both ribs < 38 mm lumbar with stump ribs.

## 4. Rule 4 — the MDPA thoraco-lumbar shape score

From `paper/mpda/main.tex` L335-341: "Separating T12 from L1 on shape alone gives an area under the curve of 0.990
and 97.3 % accuracy over 1485 vertebrae ... a logistic regression on five released per-level measures and six ratios
between them. Each measure was divided by the patient's median across their levels ... Folds are grouped by case and
the curve is taken on pooled out-of-fold scores (`test_morphometric_separability.py`)." Dominant feature:
transverse-process span.

- **Use here.** The frozen model is applied to the most cranial rib-free body (and the body above it) as a second
  thoracic-versus-lumbar opinion beside rule 1b. Operating threshold: Youden's point on the CTSP out-of-fold scores,
  computed and recorded here before any census row is scored.
- **Caveats that keep it a candidate, not a gate.** It was fitted on radiologist-named levels of the CTSP release;
  it has never been applied to an unnamed body, to a SPINEPS or TS segmentation, or to a rib-less T12 — the case it
  would need to decide. Its canal features must not be computed through OpenSpineToolkit at or after 1b7005c
  (`canal_mask` closing inflates VBHp/EPD by 10-17 mm on ~1 in 7 vertebrae, unfixed in both copies); either the fix
  lands first or the model is refit without canal terms.

## 5. Combining the rules into a flag, and the sweet spot

- Each rule emits its own row per CT (value, decision, reasons, `no_count`/`no_anchor` where it cannot run). The
  **flag** is the union of: rule 1 count ≠ 5; rule 1 `absorbed` or `lumbarisation_candidate`; rule 2 outside the
  central 95 % on any feature; rule 3 STUMP or ABSENT at the lowest level; rule 4 thoracic on the sixth body. Every
  flag carries the rules that raised it.
- **Truth for the sweep.** The read tiers only: CTSP two-radiologist Castellvi consensus and read levels; the VerSe
  Löffler Suppl. Table 1 reads (325); the registry's read tier; nothing machine-made counts as truth.
- **Sweet spot, defined before the sweep:** the flag configuration with the highest specificity subject to
  sensitivity >= 0.95 on read-tier positives, reported pooled and per subtype (L6, T13, four-lumbar / fused L5,
  Castellvi II-IV, lumbar rib, stump rib). The per-rule contribution table reports, for each rule, the flagged share
  with and without it and the positives only it catches.
- **Prevalence windows as an outside check** (the census rate must fall inside, or the rule is suspect before it is
  believed): thirteen rib-bearing 0.37-0.88 %; eleven rib-bearing 4.5-8.0 %; lumbar rib 1.6 % (0.6-4.3); stump
  twelfth rib 12.6 % (Nagata 2025) / subjects with >= 1 stump 20.5 % (Möller 2026); L6 by CT reads ~2-5 %
  (`SchwingNet/lit/CITABLE_CLAIMS.md` rows 63, 68, 69). Möller's reference statistics (PDRC -19.2 ± 3.8 vs
  -13.8 ± 2.5 mm; stump share 159/2,464) are the calibration bar for rule 3 (`STUMP_RULE.md` §10 C2).

## 6. The paired corpora

On C-ArmLSpine, T12 is in field on 12.8 % of cases, L1 on 78.5 %, the sacrum on 97.3 %, both hips on 100 %, femora on
0 %. So rules 1, 3 and 4 are computable on at most ~19 of 149 cases; rule 2 on ~145. On COBRA the thoraco-lumbar
junction is in field on 198 of 692. The review tree therefore holds, for the paired cases, mostly rule-2 evidence plus
the registry's L6 calls (C-ArmLSpine case42, case121, case136 by VERIDAH only; COBRA A270, B127, D238), and says so
per case. Every C-ArmLSpine AP/LAT pose in use was fit at a 300 mm panel (0.1465 mm/px) while the code now says 307.2 mm
(0.150); poses are refit at 0.150 before any matrix is exported.

## 7. Review

Stage 1, screen: Ashley Schehr (HF username withheld) records per case accept / reject / unsure with a reason and a time
stamp, seeing the CT, the masks, the radiographs where they exist, and the rule evidence, but not the registry's
prior call. Stage 2, confirm: the senior clinical reviewer sees only stage-1 accepts and unsures, blinded to stage 1's
verdict and identity, and records confirm / overturn / unsure with a reason. A per-case audit table joins both
verdicts, reasons and times. The existing `review_service` (claim -> submit -> IRR -> adjudicate) has none of these
fields; they are additions, not configuration.

## 8. Calibration that must finish before the freeze

C0-C8 of `STUMP_RULE.md` §10 for rule 3 (join, Möller cohort reproduction, reference numbers, PDRC key, reader
standard, ratio bimodality on path lengths, RibFrac, classifier); the reference-half freeze for rule 2; the rule-1b
classifier on named T12/L1; the rule-4 operating threshold; the PANORAMA tier rebuild; the 33-CT census
reconciliation; the C-ArmLSpine pose refit.

## 9. Freeze

    frozen by:            ____________________  (Greg)
    date:                 ____________________
    sha256 of this file:  ____________________
    calibration outputs:  ruleclass/calib/<date>/ (listed by path and sha256 in FREEZE.md beside this file)

Every row `tools/anomaly_rules.py` writes after this line carries `prereg_sha256` equal to the value above.
