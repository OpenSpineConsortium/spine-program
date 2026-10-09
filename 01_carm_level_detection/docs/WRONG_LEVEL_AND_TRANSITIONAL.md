# Wrong-level spine surgery, transitional anatomy, and rare-class learning: what is known, what we test

Written 2026-09-14. Two questions drive this note: which imaging facts cause a surgeon to operate at the wrong
level, and whether a classifier that names a vertebra from its own appearance still names it correctly when
the count is wrong. The second is the thesis of this project; transitional anatomy is its hardest test.

## 1. How wrong-level surgery happens (imaging causes)

- **It is common.** In Mody et al.'s survey of spine surgeons (Spine, 2008) half reported having operated at the
  wrong level at least once; Longo et al.'s review (JBJS, 2012) and Groff and colleagues' later surveys give
  similar orders of magnitude. NASS's "Sign, Mark and X-ray" protocol and the Joint Commission Universal
  Protocol exist because of it, and both rely on an intra-operative radiograph being READ correctly.
- **Lumbosacral transitional vertebrae (LSTV).** Prevalence 4-30% depending on definition and population;
  Castellvi's classification (Spine, 1984) grades the enlarged transverse process (I), articulation (II),
  fusion (III) and mixed (IV). Konin and Walz (AJNR, 2010) review the imaging findings and the clinical
  relevance, and state the mechanism that matters here: with a sacralised L5 or a lumbarised S1, counting from
  the sacrum names a different vertebra than counting from C2, and MRI (which rarely sees C2) and the
  intra-operative film (which rarely sees T12's rib) can disagree with each other and with the CT.
- **Numbering conventions disagree.** Carrino et al. (Radiology, 2011) found spinal segment variants in about
  12% of lumbar MRI and showed that the numbering depends on the reference used (last rib, iliolumbar ligament,
  sacrum). Hughes and Saifuddin (Clinical Radiology, 2006) and Tins and Balain (2016) document the numerical
  variants: 4 or 6 lumbar-type vertebrae, 11 or 13 rib-bearing vertebrae, cervical ribs. The iliolumbar ligament
  marks L5 in most but not all cases.
- **Thoracic localisation.** Thoracic levels have no reliable intra-operative landmark; counting ribs on a
  portable AP film fails in obese patients and with a 13th or an absent 12th rib. Pre-operative marking
  (methylene blue, fiducial screws, CT-guided coils) and intra-operative CT are the published mitigations
  (Upadhyaya and colleagues; Paolini and colleagues), all of which are what a level classifier would replace.
- **Other causes**: poor fluoroscopy in large patients, parallax from an oblique beam, counting from the
  skull on a cervical film that does not show C2, previous fusion or vertebroplasty distorting the count,
  osteoporotic collapse, hemivertebrae and block vertebrae (Klippel-Feil in the cervical spine).

## 2. Why transitional anatomy is the decisive test for local morphology

A sacralised L5 (Castellvi III/IV) is still an L5 by morphology: the body, pedicles and facets above it look
like a normal L4 and L3. A counting method that starts at the sacrum calls that L4 an L5. A morphology
classifier that has learned what L4 looks like should call it L4 regardless. Conversely, with six lumbar-type
vertebrae the classifier has a real ambiguity (is the sixth an L6 or a lumbarised S1?), which is exactly the
case where naming must fall back to anchors (ribs above, sacrum below) and say so.

The danger the user named is real: a classifier that learned "the vertebra above the sacrum is L5" would
rubber-stamp a miscounted pre-operative plan in the operating room. The tests below are designed so that a
model that counts implicitly (from its context band, from the sacrum in the crop) is caught.

## 3. Prior art on learning rare classes (the long tail)

- Class-balanced loss by effective number of samples (Cui et al., CVPR 2019); LDAM with deferred
  re-weighting (Cao et al., NeurIPS 2019); logit adjustment (Menon et al., ICLR 2021), which corrects the
  softmax for the label prior and is the principled version of "re-weight the rare class"; decoupling
  representation and classifier (Kang et al., ICLR 2020: classifier re-training and tau-normalisation) —
  train the backbone on the natural distribution, then rebalance only the last layer.
- Surveys: Zhang et al., "Deep long-tailed learning" (TPAMI 2023). In medical imaging the same recipes plus
  synthetic oversampling (rendering or generating the rare class) are the standard.
- What we already saw in this project: L6 Dice stayed at zero despite 12x duplication in the 3-D
  segmentation, because there were too few DISTINCT cases; a rule decoder on the 4-class output found 6 of 6
  L6. The lesson is that duplication does not create information, and that a decoder with anatomical
  constraints beats a classifier on a class it has barely seen.

## 4. What we build and measure

1. **Transitional test set from CT (no counting possible).** CTSpinoPelvic1K carries `lstv_class`,
   `castellvi_type`, `has_l6` per case (62 cases with L6); VerSeFusion carries L6 (id 25) and T13 (id 28)
   cases; TotalSegmentator's set is unlabelled for variants but will be scanned by label counts. Renders
   (parallel and physics) of these cases, with per-vertebra boxes, form `transitional_eval`, stratified into
   normal / Castellvi I-II / Castellvi III-IV / L6 / T13 / cervical rib. `tools/eval_transitional.py` scores
   the level model on single-vertebra crops (n=1 context, so nothing in the crop can be counted) and with the
   run decoder without caption, and reports per-stratum accuracy for every level, with the confusion between
   L4/L5/L6 and T12/T13/L1 shown explicitly.
2. **Counting trap.** The same crops of L4 from normal and from L6 spines, and of L5 from normal and from
   sacralised spines; if the accuracy on the variant spines drops, the model was counting from the sacrum.
3. **Real-image subgroup.** FluoroCap panels whose caption names a transitional vertebra, wrong-level
   surgery, sacralisation, lumbarisation, Castellvi, Bertolotti, L6, a 13th rib or a cervical rib: a dedicated
   search across every route (Europe PMC full text, OpenAlex, YouTube, patents, archives) with those terms,
   and a `transitional` subgroup flag that the readers adjudicate first. Two panels carried the flag before
   this search.
4. **Training-side measures.** Rare levels (T13, L6, C1, C2, sacrum) get logit adjustment and class-balanced
   sampling in the level model; the DRR banks from all three CT sources are rendered with every transitional
   case kept (never dropped for being "non-standard"); implants are placed at C2 (odontoid), cervical lateral
   masses, thoracic and lumbar pedicles and S1 so no region is hardware-free in the synthetic data.

## 5. Scan of the literature (OpenAlex, top cited per query; reviews and off-topic rows left in for transparency)

See `prior_art_wrong_level.md` produced by `tools/prior_art_wrong_level.py` for the raw tables. The named
papers above are the ones that matter; the scan mostly surfaces reviews, which is a known weakness of
citation-sorted search for a narrow question.
