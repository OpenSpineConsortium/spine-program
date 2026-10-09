# Literature angle "ct_lstv_automation" — automated LSTV / enumeration-anomaly detection on CT

Compiled 2026-09-24. Every number below was read on the page or PDF named in the row; sources that
could not be opened are marked as such. Reviews are listed only as pointers, never as the source of a number.
Modality is stated for every entry (CT / radiograph / MRI). Positives are counted from each paper's own
reference standard, never from a segmenter's names.

Already in `SchwingNet/lit/CITABLE_CLAIMS.md`: `liebrand2026` (the ASReview systematic review on spinal level
determination, PMID 42009915) is planned there. Nothing else in CITABLE_CLAIMS.md or `refs_additions.bib`
touches LSTV, VerSe, SPINEPS/VERIDAH, Payer/Anduin or TotalSegmentator (grep on 2026-09-24 returned no hits).

## Bottom line for the design note

1. **There is no published CT-based LSTV classifier validated against radiologist Castellvi reads.** The only
   peer-reviewed LSTV-specific deep-learning detector (Kwak 2025) is on lateral **radiographs**, binary,
   single-site, no external validation, test accuracy 76.4 %.
2. What exists on CT is **enumeration-anomaly labelling** (L4/L6, T11/T13): Hanaoka 2017 (statistical
   model, 300 CTs), Netherton 2020 (spacing rule, 5/6 flagged), Meng 2023 (graph prior, VerSe'20),
   VERIDAH 2026 (SPINEPS group; CT LEA recall 97.22 % on 365 test scans, internal split, weights public,
   CT data private). None reports Castellvi type; VERIDAH explicitly collapses every Castellvi anomaly to
   "sacralized lumbar vertebra regardless of the Castellvi type".
3. The **rib-side** partner exists: Möller 2025 stump-rib pipeline (CT, 648 public subjects, 133 with a stump
   rib, F1 0.84 from the first 22 mm of rib), weights and masks public.
4. The **inter-reader ceiling on CT** for Castellvi grading is κ 0.63–0.71 (four readers, Hanhivaara 2024).
   Any "classifier agrees with reader" number must be read against that.
5. **Public positives with a Castellvi label**: VerSe'20 (Liebl 2021 Table 2): 2a 35, 2b 25, 3a 14, 3b 28,
   4 7 (image series; 252 series with the lumbosacral region visible), plus 6 series with 13 thoracic and 3
   with 4 lumbar. Note the internal inconsistency on L6 (Liebl Table 2: 85 series with six lumbar
   vertebrae; Sekuboyina 2021 §5.2: 47 cases with an L6, 15/15/17) — resolve from the masks, not the text.
6. **No FDA-cleared vertebra-naming tool documents LSTV handling.** HealthOST (K213944) names T1–L4 with
   91.49 % agreement against three radiologists on 150 CTs; its summary never mentions transitional anatomy.
   Anduin (research tool) and its commercial successor spineR document nothing on L6/T13. TotalSegmentator
   has no L6/T13 class at all.

## Claims (verified)

### C1. Kwak 2025 — deep learning LSTV detector, lateral RADIOGRAPHS (not CT)
- Kwak D, Ro DH, Kang DH. Automated Detection of Lumbosacral Transitional Vertebrae on Plain Lumbar
  Radiographs Using a Deep Learning Model. *J Clin Med* 2025;14(21):7671. PMID 41227066, PMC12610351,
  doi:10.3390/jcm14217671. Opened: PubMed efetch (citation) and PMC full text.
- Task: binary LSTV present/absent. Modality: standing lateral lumbar radiograph.
- Cohort: 3,116 radiographs; LSTV 1,941 (62.3 %), normal 1,175 (37.7 %); train 2,803 / test 313.
- Reference standard: presence established from whole-spine imaging, CT or MRI; the PMC text describes an MRI
  conclusion "that explicitly mentioned transitional vertebra, lumbarized, sacralized, lumbarization, or
  sacralization"; one orthopaedic specialist read the test radiographs for the human comparison. No Castellvi
  subtypes.
- Result (test, ResNet-50 partial fine-tune): accuracy 76.4 %, sensitivity 85.1 %, specificity 61.9 %,
  AUC 0.84; 166 TP, 73 TN, 29 FN, 45 FP. Five-fold CV accuracy 81.8 ± 1.9 %.
- External validation: none. Public data: no ("cannot be shared publicly"). Code: not stated.
- Relevance: the only LSTV-specific DL detector in PubMed; radiograph-only, so it does not pre-empt a CT
  classifier. Its 62 % prevalence is an enriched surgical cohort, not a census.

### C2. VERIDAH 2026 (SPINEPS group) — enumeration-anomaly-aware labelling, CT + T2w MRI
- Möller H, Schoen H, Graf R, Atad M, Molinier N, Sekuboyina A, … Kirschke JS. VERIDAH: Solving Enumeration
  Anomaly Aware Vertebra Labeling across Imaging Sequences. arXiv:2601.14066 (20 Jan 2026). Not peer
  reviewed as of 2026-09-24. Opened: arXiv abs, arXiv HTML, and the PDF (text-extracted; lines cited below
  are from `veridah.txt` in `<session scratchpad, not kept>`).
- Task: label vertebrae given centroids; anomalies = TEA (11 or 13 thoracic) and LEA (4 or 6 lumbar).
  L6/T13 are never predicted as classes: "we replace the T13 and L6 labels in the reference annotation with
  T12 and L5" and detect the anomaly as two consecutive L5s (PDF l.252–258, 364–371).
- CT cohort: in-house, 1,536 scans (train 1,171 / test 365), all with T1 present "necessary to manually
  assess TEA"; TEA rate 5.5 % (test 6.8 %), LEA rate 7.3 % (test 7.9 %) → ≈29 LEA and ≈25 TEA test cases
  (my arithmetic from the rates; the paper gives rates only). MRI: NAKO T2w, 6,291 subjects, test 1,000,
  LEA 14.6 % in test.
- Reference standard (CT): segmentation annotations "supervised by an expert with 24 years of experience";
  thoracolumbar junction rated after Park et al.; lumbosacral: "In the presence of a lumbosacral transitional
  Castellvi anomaly, we defined the vertebra with this anomaly as a sacralized lumbar vertebra regardless of
  the Castellvi type" (PDF l.181–183). MRI: one expert with 3 years' experience corrected SPINEPS output.
- Results (CT, Table 3): perfect-label percentage 99.18 % vs Meng et al. 77.81 %; TEA recall 96.30 % vs
  11.11 %; LEA recall 97.22 % vs 61.11 %. (MRI, Table 4: 98.30 % / 87.80 % / 94.48 %.)
- External validation: none (internal splits). Code/weights: github.com/Hendrik-code/spineps. CT data:
  private. Requires vertebral centroids from another tool.
- Relevance: the strongest existing CT baseline for L6/L4 detection; it does not grade Castellvi and its
  CT test set is not released, so it cannot be compared head-to-head without running its weights on our data.

### C3. Möller 2025 — automated thoracolumbar stump-rib detection, CT
- Möller H, Schön H, Dima A, Keinert-Weth B, Graf R, Atad M, … Kirschke JS. Automated Thoracolumbar Stump
  Rib Detection and Analysis in a Large CT Cohort. arXiv:2505.05004 (8 May 2025). Not peer reviewed as of
  2026-09-24. Opened: arXiv abs, arXiv HTML, PDF (text in `stump.txt` in `<session scratchpad, not kept>`).
- Data: VerSe (323 subjects) + RibFrac (420) public; in-house (413, 27 used) only for segmentation
  training. Final analysis set 648 subjects; 45 randomly chosen VerSe/RibFrac subjects held out as the
  segmentation test set.
- Reference standard: rib masks corrected by "an expert (H.M.) with two years of experience supervised by two
  experts (H.S., J.S.K.) of three and 23 years"; the stump-rib label itself is the length rule "≤ 38 mm",
  applied to the automatic segmentation, plus a five-point Likert review of segmentation quality by two
  experts. There is no independent radiologist read of TLTV.
- Results: "Of the 2464 ribs that we analyzed, 159 were stump ribs. Of the 648 subjects, 133 had at least
  one SR (20.5%)." Rib Dice 0.997 (vs 0.779 for the comparator), length-measurement success 98.2 %.
  Morphology-only SVM on the first four path points + corpus distance: F1 0.84 (random 70/30 splits, 10 runs;
  Table 5: 0.84 ± 0.04), i.e. a stump rib is recognisable from the first ≈22 mm of rib.
- External validation: none. Code: github.com/Hendrik-code/rib-segmentation. Masks: doi 10.5281/zenodo.14850928.
- Relevance: the rib-count partner for an LSTV adjudication tier; the 20.5 % is a fracture-enriched cohort
  (authors say so), not a prevalence.

### C4. Sekuboyina 2021 — VerSe benchmark: how 25 algorithms handled T13/L6, CT
- Sekuboyina A, Husseini ME, Bayat A, Löffler M, Liebl H, Li H, … Kirschke JS. VerSe: A Vertebrae labelling
  and segmentation benchmark for multi-detector CT images. *Med Image Anal* 2021;73:102166. PMID 34340104,
  doi:10.1016/j.media.2021.102166. ScienceDirect returned 403; opened the arXiv v6 PDF (2001.09193v6,
  5 Apr 2022; text in `verse.txt` in `<session scratchpad, not kept>`, line numbers below).
- Cohort: 374 scans / 355 patients / 4,505 vertebrae; labels 1–24 plus 25 = L6 and 28 = T13 (l.255–257).
- Transitional counts: "VerSe'19 included two cases with L6 in the train set … almost every algorithm fails
  to segment the one L6 in the Hidden set … VerSe'20 included six cases with T13 (2/2/2 in
  Train/Public/Hidden) and 47 cases with an L6 (15/15/17)" (l.917–920).
- Findings: "None of the methods in VerSe'19 identified the presence of L6" (l.725); in VerSe'20 "almost all
  algorithms identify at least a fraction of the L6 vertebrae"; only Xiangshang Z. identified all T13
  instances in both phases (l.923). Worst case of VerSe'20 "due to the presence of a transitional L6
  vertebra" (l.706–707). Lessmann N. "depends on identifying the last vertebra. In cases with L6, this
  affects the entire scan" (l.864). Fig. 9 shows lower Dice on transitional scans for all but Payer C.
  (Hidden). No per-method L6 identification rate is tabulated.
- Reference standard: human-hybrid annotation, five medical students then neuroradiologist review; no
  inter-rater data (acknowledged limitation). Public data: yes. Code: participants' dockers.
- Relevance: establishes that counting-based labelling fails at the LS junction and that the fix in the
  field was enrichment (L6 15 % of VerSe'20), not a morphology classifier.

### C5. Liebl 2021 — VerSe'20 data descriptor with the Castellvi table, CT
- Liebl H, Schinz D, Sekuboyina A, Malagutti L, Löffler MT, Bayat A, … Kirschke JS. A computed tomography
  vertebral segmentation dataset with anatomical variations and multi-vendor scanner data. *Sci Data*
  2021;8:284. PMID 34711848, PMC8553749, doi:10.1038/s41597-021-01060-0. Opened: PMC full text.
- Cohort: 300 subjects, 319 series, 4,142 vertebrae; enriched "with cases that exhibit anatomical variants
  such as enumeration abnormalities (n = 77) and transitional vertebrae (n = 161)".
- Table 2 (image series; Private test / Public validation / Public training / All): cervical ribs 18;
  12 thoracic 131, 11 thoracic 8 (1/4/3), 13 thoracic 6 (2/2/2); 5 lumbar 165, 4 lumbar 3 (1/2/0),
  6 lumbar 85 (29/38/28); stump rib 90 (28/28/34); Castellvi 0/1 146, 2a 35 (10/8/17), 2b 25 (10/8/7),
  3a 14 (5/7/2), 3b 28 (8/8/12), 4 7 (3/2/2). Denominator: 252 series with the complete lumbosacral
  anatomy.
- Method: rib-centred nomenclature ("a consistent enumeration was achieved in almost all cases, while only
  2 cases … remained ambiguous"); Castellvi grading "mainly based on the morphology of the transverse
  process"; masks by medical students, "reviewed, corrected, and finally approved by a neuroradiologist".
  Single reader for Castellvi; no κ.
- Discrepancy to record: 85 series with six lumbar vertebrae here vs 47 L6 cases in Sekuboyina 2021 §5.2.
  The two papers describe the same release; the difference is probably counting convention (series vs
  cases, or lumbar count vs presence of a label-25 mask). Count from the masks.
- Relevance: the only public CT source of Castellvi-typed positives; 74 series of type 2–4 in total, 35 of
  them in the private test split that is not downloadable.

### C6. Hanaoka 2017 — first automated CT detector of vertebral-number anomalies
- Hanaoka S, Nakano Y, Nemoto M, Nomura Y, Takenaga T, Miki S, Yoshikawa T, Hayashi N, Masutani Y,
  Shimizu A. Automatic detection of vertebral number abnormalities in body CT images. *Int J Comput Assist
  Radiol Surg* 2017;12(5):719–732. PMID 28063076, doi:10.1007/s11548-016-1516-y. Opened: PubMed efetch
  abstract (Springer page redirected to a cookie wall; full text not read).
- Method: landmark point distribution model, five landmarks per vertebra; five hypotheses (normal, 11 or 13
  thoracic, 4 or 6 lumbar) chosen by posterior likelihood. Modality: body CT.
- Cohort and results (abstract): 300 CTs; "the vertebrae of 211/217 (97.2%) of the subjects were
  successfully determined as normal"; abnormal number without transitional vertebrae "9/10 (90%)";
  with transitional vertebrae "71/73 (97.3%) … judged as partially successfully determined".
- Reference standard, external validation, code: not stated in the abstract (not verified).
- Relevance: the earliest CT precedent; note the 73/300 (24 %) "transitional" share, and that transitional
  cases were only "partially" resolved, i.e. the count was right but the naming of the junction was not
  adjudicated.

### C7. HealthOST K213944 — the FDA-cleared CT vertebra-naming tool, no LSTV handling documented
- FDA 510(k) K213944, HealthOST (NanoxAI Ltd.), decision letter dated April 22, 2022, product code JAK,
  21 CFR 892.1750; predicate AI-Rad Companion (Musculoskeletal) K193267. Opened: the 510(k) summary PDF
  from accessdata.fda.gov (text in `healthost.txt` in `<session scratchpad, not kept>`, l.264–285).
- Validation: 150 CTs (1,425 vertebrae) from two institutions, ground truth by "three US board-certified
  radiologists"; "overall agreement for vertebral naming of 91.49% (95% CI: [89.91%, 92.89%])"; axial-scan
  subset 92.19 % (95% CI [89.31%, 95.07%]). Labels T1–L4 only.
- The summary contains no occurrence of "transitional", "lumbosacral", "L5", "sacrum", "variant" or
  "anomaly" (grep of the extracted text). Indication requires ≥4 vertebrae in T1–L4, so the lumbosacral
  junction is outside the device's scope.
- Relevance: the regulatory precedent for "vertebral naming agreement" as an endpoint, with a three-reader
  truth panel; a 510(k) for LSTV flagging would need the junction inside the indication.

## Supporting entries (verified; not promoted to claims)

- **Hanhivaara 2024** (CT reader ceiling). Hanhivaara J, Määttä JH, Kinnunen P, Niinimäki J, Nevalainen MT.
  Castellvi classification of LSTV: comparison between conventional radiography, CT, and MRI. *Acta Radiol*
  2024;65(12):1515–1520. PMID 39444351, doi:10.1177/02841851241289355. Abstract (efetch): 852 screened,
  100 LSTV patients, four readers per modality, gold standard one experienced radiologist; CT sensitivity
  76 %, specificity 93 %, accuracy 77 %, balanced accuracy 84 %; inter-reader κ CT 0.63–0.71, CR 0.16–0.32,
  MRI 0.24–0.56. Same group's prevalence series: Hanhivaara 2020 *Eur Radiol* 30(6):3409, PMID 32072261,
  3,855 abdominal CTs, LSTV 1,101 (29 %): type I 68 %, II 16 %, III 13 %, IV 3 %. (Prevalence angle is
  covered in `lit_prevalence_and_definitions.md`; listed here only as the reader-agreement baseline.)
- **Netherton 2020** (CT, spacing rule). Netherton TJ, et al. Evaluation of a multiview architecture for
  automatic vertebral labeling of palliative radiotherapy simulation CT images. *Med Phys* 2020;47(11).
  PMID 33459402, doi:10.1002/mp.14415. Abstract (efetch): X-Net trained on 803 scans; test outlier group
  n = 20 with abnormalities, normative n = 74; identification rate 94.2 %, localisation error 2.2 mm; the
  intervertebral-spacing rule "flagged five of six patients with atypical vertebral counts (additional
  thoracic (T13), additional lumbar (L6) or only four lumbar vertebrae)". Six positives only.
- **Meng 2023** (CT, graph prior). Meng D, Boyer E, Pujades S. Vertebrae localization, segmentation and
  identification using a graph optimization and an anatomic consistency cycle. *Comput Med Imaging Graph*
  2023;107:102235. PMID 37130486, doi:10.1016/j.compmedimag.2023.102235; arXiv 2110.12177. Abstract
  (efetch + arXiv): "transitional and pathological vertebrae are still plaguing most existing approaches";
  transitional configurations encoded in a graphical model; "outperforms all methods on transitional
  vertebrae" on VerSe'20; code public. No number for transitional cases in the abstract. On VERIDAH's
  private CT test set it scored LEA recall 61.11 %, TEA recall 11.11 % (VERIDAH Table 3).
- **Payer 2020** (CT, VerSe'19 winner). Payer C, Štern D, Bischof H, Urschler M. Coarse to fine vertebrae
  localization and segmentation with SpatialConfiguration-Net and U-Net. VISAPP 2020, doi:10.5220/0008975201240133.
  Opened: scitepress PDF (text in `payer.txt` in `<session scratchpad, not kept>`). "As some subjects contain the additional vertebra
  L6, at maximum N = 25 vertebrae are annotated" (l.421); Table: lumbar (L1…L6) id rate 90.45 % (284 of
  314), all 89.79 % (774 of 862). No explicit L6 handling beyond allowing the 25th landmark. Sekuboyina 2021
  (l.857–866) reports that Payer C. and Zhang A. identified L6 in VerSe'20 while no 2019 method did.
- **Lessmann 2019** (CT + MR, iterative). Lessmann N, van Ginneken B, de Jong PA, Išgum I. *Med Image Anal*
  2019;53:142–155. PMID 30771712, doi:10.1016/j.media.2019.02.005. Abstract (efetch): labels by counting
  "independently of the number of visible vertebrae" with maximum-likelihood refinement; identification
  accuracy 93 %. Sekuboyina 2021 l.864: "depends on identifying the last vertebra. In cases with L6, this
  affects the entire scan." No transitional handling.
- **Elton 2020** (CT, L1 finder). Elton DC, Sandfort V, Pickhardt PJ, Summers RM. Accurately identifying
  vertebral levels in large datasets. *Proc SPIE* 2020 Medical Imaging; arXiv 2001.10503. Opened: arXiv PDF
  (text in tool-results `elton.txt`). Names LSTV as the reason "L5 is not a reliable transitional vertebra to
  use as a reference landmark" (citing 10 % LSTV, 6 % lumbarization, 4 % sacralization from French et al.);
  achieves 98 % L1 identification on 40 CTC scans after 249 pseudo-segmented training scans; instance
  approach hypothesised "useful when there are vertebral anomalies … additional or missing vertebra" but
  not evaluated on them. No LSTV numbers.
- **SPINEPS** (T2w MRI). Möller H, Graf R, Schmitt J, et al. *Eur Radiol* 2025;35(3):1178–1189. PMID
  39470797, PMC11836161, doi:10.1007/s00330-024-11155-y. Opened: PMC. Verbatim: "the instance labels are
  counted from top to bottom regardless of the field of view or the presence of enumeration abnormalities,
  such as 13 thoracic vertebrae." No labelling step; VERIDAH is the fix.
- **Yang 2025** (CT, VerSe, low standing). Yang C, Huang L, Sucharit W, Xie H, Huang X, Li Y.
  Transformer-enhanced vertebrae segmentation and anatomical variation recognition from CT images. *Sci Rep*
  2025;15:34329. PMID 41038867, PMC12491412, doi:10.1038/s41598-025-16689-9. Opened: PMC. Three-class
  per-vertebra classifier (Normal/T13/L6) on VerSe'19+'20 only; "a hold-out test set of 300 samples with
  known variation annotations, evenly sampled across the three classes"; accuracies Normal 87 %, L6 85 %,
  T13 80 %; AUC 0.96/0.93/0.95; labels "extracted from the VerSe 2020 dataset annotations"; code link given
  is https://github.com/anjany/verse, i.e. the VerSe challenge repository, not the authors' code. VerSe has
  six T13 scans, so ~100 T13 "samples" cannot be independent cases. Do not cite for a number.
- **VerTE-MT 2026** (CT, VerSe). Aydogdu S, et al. *IEEE J Biomed Health Inform* 2026, PMID 42213570,
  doi:10.1109/jbhi.2026.3698274. Abstract: L6 Dice 81.03 % / 75.96 % on VerSe'20 public/hidden; entropy-guided
  sampling of rare cases. Segmentation quality on L6, not detection of L6.
- **Anduin / Bonescreen** (research tool). https://www.bonescreen.de/anduin: "a freely available research
  tool designed for segmenting vertebrae in CT scans", CC-BY-SA 4.0, ERC PoC; Btrfly-Net labelling; the page
  says nothing about L6/T13/transitional anatomy, gives no validation number, and names a commercial
  successor "spineR" (no regulatory claim on the page).
- **TotalSegmentator** class list (README, wasserth/TotalSegmentator master): vertebrae S1, L5–L1, T12–T1,
  C7–C1, sacrum; no L6, T13 or transitional class. (Wasserthal 2023 *Radiol AI* doi:10.1148/ryai.230024 is
  the paper; not re-opened.)
- **Kim 2024** (radiograph). Kim JK, et al. Identification of L5 vertebra on lumbar spine radiographs using
  deep learning. *J Int Med Res* 2024;52(1). PMID 38206194. YOLOv5x on 150 radiographs; mAP0.5 99.2 %;
  not an LSTV method (surfaced by the search terms only).
- **Liebrand 2026** systematic review (already `liebrand2026` in CITABLE_CLAIMS). PMID 42009915,
  doi:10.1007/s00586-026-09925-x. Abstract: 29 studies; "In the studies involving transitional vertebrae no
  100% was achieved"; five "advanced" (navigation/ML) studies. A review; cite primaries for numbers.
- **Andrade-Andrade 2026** systematic review, *Pain Pract* 26(3):e70138, PMID 41800527: CT as gold standard
  for LSTV diagnosis; no accuracy numbers in the abstract. Review only.

## Dead ends and things not found

- PubMed ("transitional vertebra*"[tiab] AND deep learning/automated/…): Count 3 → Kwak 2025 (radiograph),
  Hanaoka 2017, and a stress-fracture review (PMID 42532102, irrelevant).
- PubMed broad enumeration query (25 hits) triaged by esummary: relevant ones are listed above; the rest
  (dose/reconstruction/ophthalmology/ontology papers) are term collisions.
- PubMed (Castellvi OR Bertolotti) AND (deep learning/automated/segmentation): 3 hits, none automated
  (Becker 2021 musculature, Ropars 2019 psoas landmark MRI, Vining 2014 prevalence).
- Europe PMC 2023–2026 "transitional vertebra" AND DL (87 hits) triaged from titles: no additional CT or MRI
  LSTV classifier; Fu 2026 *Tomography* (PMID 41893829) is VerSe segmentation without transitional handling.
- **No MRI LSTV deep-learning classifier found** in PubMed/Europe PMC as of 2026-09-24 (searched "lumbosacral
  transitional vertebra MRI deep learning"). MSKai (FDA 510(k), May 2025) is lumbar MRI labelling; no LSTV
  documentation located (press releases only; the 510(k) summary was not opened).
- FDA: K241029 turned out to be SpineUs (tracked ultrasound), irrelevant. No 510(k) summary mentioning
  transitional vertebrae was found; Bonescreen/spineR and CoLumbo did not surface in the search.
- Löffler 2020 *Radiol AI* 2(4):e190138 (PMID 33937831, PMC8082364; VerSe'19 descriptor) was opened at PMC:
  160 series / 141 patients / 1,725 vertebrae; **no mention of transitional vertebrae or Castellvi**. The
  Castellvi table is in Liebl 2021 (VerSe'20), not in Löffler 2020. RSNA's own page returned 403.
- Sekuboyina 2021 at ScienceDirect: 403; used arXiv v6 (same text, journal reference confirmed on the arXiv
  abs page).
- Springer page for Hanaoka 2017 redirected to a cookie wall; full text not read, abstract only.
- Payer's GitHub README (verse2019/verse2020) does not discuss L6; the scitepress PDF does (used).
- Windsor 2020 (MICCAI, whole-spine MRI, arXiv 2007.02606): abstract has no transitional-vertebra statement;
  not pursued further (MRI).

## Files

- Extracted texts used for line citations: `<session scratchpad, not kept>`
  (session scratch; regenerate from the arXiv/FDA/scitepress PDFs with `extract_pdfs.py` in the same folder).
