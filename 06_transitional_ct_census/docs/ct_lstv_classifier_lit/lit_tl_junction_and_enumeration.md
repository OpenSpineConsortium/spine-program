# Literature angle: thoracolumbar junction and enumeration on CT

Checked 2026-09-24 against live records. Routes that worked: PubMed E-utilities (`esearch`, `efetch` text abstracts),
PMC article pages at `pmc.ncbi.nlm.nih.gov` (the old `www.ncbi.nlm.nih.gov/pmc` host 301-redirects), arXiv abstract
pages, arXiv HTML (`arxiv.org/html/<id>`), ar5iv (for the 2020 VerSe preprint whose PDF exceeds the fetch limit), the
Europe PMC REST search (only with `EXT_ID:<pmid> AND SRC:MED`; `PMID:` and `DOI:` queries returned empty), the
TotalSegmentator GitHub README, and the KoreaMed/Anesth Pain Med reader. Routes that failed: pubmed.gov article pages
(cookie wall), ScienceDirect, SAGE, JNS and the Radboud repository PDF (all 403), the arXiv PDF of VerSe (10 MB cap).

Nothing in `../CITABLE_CLAIMS.md` or `../refs_additions.bib` covers this angle (those files are registration,
rendering and DICOM). Every claim below is new. The word "already in CITABLE_CLAIMS" applies to none of them.

Reading rule applied: numbers quoted below were read from an abstract returned by `efetch` (verbatim), or from a
full text summarised by the fetch tool's extractor. Where the extractor did the reading, the row says so; those
numbers are second-hand and should be re-read from the PDF before they print.

## Summary table

| # | Source | Modality / cohort | n atypical | Reference standard | Number that matters | Code / data | Standing |
|---|---|---|---|---|---|---|---|
| 1 | Liebl 2021, Sci Data 8:284 | CT, VerSe'20, 300 subjects / 319 series | T13 6, T11 8, L6 85, L4 3, stump ribs 90, LSTV II-IV 161 | two neuroradiologists, consensus | 13 thoracic 6/145 (4.1 %); 6 lumbar 85/253 (33.7 %); enriched, not prevalence | osf.io/t98fz, github anjany/verse | PMC full text, extractor-read |
| 2 | Sekuboyina 2021, Med Image Anal 73:102166 | CT, VerSe'19+'20, 374 scans / 355 patients | VerSe'19: L6 2 train + 1 hidden; VerSe'20: T13 2/2/2, L6 15/15/17 | same annotations | "None of the methods in VerSe'19 identified the presence of L6"; one of the VerSe'20 entries got every T13 | github anjany/verse | ar5iv HTML of arXiv 2001.09193, extractor-read; journal paywalled |
| 3 | Möller 2026, VERIDAH, arXiv 2601.14066 (preprint) | CT in-house 1,536 images (1,171/365) + NAKO MRI 6,291 | CT: TEA 5.5 %, LEA 7.3 % (test 6.8 % / 7.9 %) | expert with 24 y | baseline Meng et al. 77.81 % of CT subjects all-correct, thoracic-anomaly recall 11.11 %; VERIDAH 99.18 %, 96.30 %, 97.22 % | github Hendrik-code/spineps | arXiv abstract + HTML, extractor-read; NOT peer reviewed |
| 4 | Jin 2023/2024, RibSeg v2, IEEE TMI | CT, 660 RibFrac scans, 15,466 ribs, 420/80/160 | 99 "challenging" (47/19/33) incl. missing/vague floating ribs and a possible 13th pair | expert-inspected labels | 25 classes (24 ribs + rest): no 13th-rib class; best label accuracy 91.5 % overall, 79.6 % on challenging cases | github M3DV/RibSeg | efetch abstract verbatim; full-text numbers extractor-read from arXiv 2210.09309v4 |
| 5 | Nagata 2025, Skeletal Radiol 54(10):2169 | whole-spine CT, 551 patients | LSTV 16.3 %, rib anomalies 14.0 % | count from cervical: 8th = T1, 20th = L1, 25th = S1 | hypoplastic 12th rib 12.6 %, lumbar rib 1.5 %; all hypoplastic 12ths in sacralisation, all lumbar ribs in lumbarisation (p < 0.001) | none stated | efetch abstract verbatim |
| 6 | Hanhivaara 2024, Acta Radiol 65(12):1515 | 100 LSTV patients (of 852) read on CR, CT, MRI by 4 blinded readers | 100 | fellowship-trained radiologist, all three modalities | Castellvi typing: CT sens/spec/acc/bal-acc 76/93/77/84 %; MRI 54/88/56/68 %; CR 32/85/42/59 %; kappa CT 0.63-0.71, CR 0.16-0.32 | none | efetch abstract verbatim |
| 7 | Schinz 2026, Eur Spine J 35(4):2195 | CT, 1,242 subjects, complete thoracolumbar spine | anatomical variants included (count not in abstract) | nerve morphology; inter-rater | shape-based TL-junction labelling agreed with nerve morphology 100 % vs rib-based 97.2 %, rib-length 96.3 %, counting 92.6 %; kappa 0.61 vs 0.59 | none stated | efetch abstract verbatim |

Supporting rows (not among the seven claims, verified to the same standard):

| Source | What it gives | Standing |
|---|---|---|
| Sabri 2025, Neurosurg Focus 58(6):E13, PMID 40450886 | 3,147 full-length RADIOGRAPHS: 24 presacral segments 2,868 (91.1 %); 25 segments 174 (5.5 %); 23 segments 104 (3.3 %); 26 in 1; 12 ribbed vertebrae 2,976 (94.6 %), 11 ribs 143 (4.5 %), 13 ribs 28 (0.88 %); both anomalies 56 (1.8 %) | efetch abstract verbatim |
| Doo 2020, Anesth Pain Med (Seoul) 15(1):103, PMID 33329798 | whole-spine 3-D CT, 1,340 adults, counted from C1: TLTV 150 (11.2 %); LSTV 111 (8.3 %; sacralisation 68, lumbarisation 43); 12 ribs 1,228 (91.6 %), 11 ribs 107, 13 ribs 5; TLTV vs abnormal rib count OR 117.26; TLTV vs LSTV OR 7.38; two pain physicians read independently | efetch abstract verbatim + journal reader |
| Hanhivaara 2020, Eur Radiol, PMID 32072261 | 3,855 abdominal CT: LSTV 1,101 (28.6 %) with type I 754, II 171, III 143, IV 33; intra/inter-rater kappa 0.928 / 0.855; "The last ribs were used to define the Th12 vertebra"; no whole-spine coverage | PMC full text, extractor-read |
| Möller 2025, stump ribs, arXiv 2505.05004 (preprint) | 648 subjects analysed (VerSe, RibFrac, in-house), 2,464 ribs, 159 stump ribs; 133 subjects with at least one stump rib (20.5 %) at a 38 mm threshold; rib-segmentation Dice 0.997 vs 0.779; stump-vs-normal F1 0.84 (SVM); vertebrae from Bonescreen SpineR; 45-subject manual test set; weights github Hendrik-code/rib-segmentation, masks 10.5281/zenodo.14850928 | arXiv HTML, extractor-read; the three cohort sizes quoted (323 + 420 + 143) exceed 648, so the extractor mixed available and analysed counts: re-read Table 1 |
| Wasserthal 2023, TotalSegmentator, Radiol Artif Intell 5(5):e230024, PMID 37795137 | classes vertebrae_C1..L5, vertebrae_S1, sacrum, rib_left/right_1..12; 117 classes in the v2 "total" task; NO class for T13, L6, a 13th rib or a lumbar rib; paper text says nothing about transitional anatomy | README read directly; paper via PMC, extractor-read |
| Netherton 2022, IJROBP 114(3):516, PMID 35787928 | RT planning CT; mislabel classifier AUC 0.82; "All contouring and labeling errors within treatment regions (11 of 11), including errors from patient plans with atypical anatomy (eg, T13, L6) were detected" | efetch abstract verbatim |
| Netherton 2025, Phys Imaging Radiat Oncol 34:100738, PMID 40129727, PMC11932639 | external validation 40 + 41 CTs: identification 83 % / 92 % → 87 % / 96 %; "did struggle with atypical patients such as those with fused cervical spines, extra T13, variations in the number of lumbar spine levels"; no counts | PMC full text, extractor-read |
| Yang 2025, Sci Rep 15(1):34329, PMID 41038867 | VerSe 374 scans; ViT variant classifier: accuracy normal 87 %, L6 85 %, T13 80 %; AUC L6 0.96, T13 0.93; reference = VerSe annotations; "code" link is github anjany/verse (the challenge repo, not the authors' code) | PMC full text, extractor-read |
| Kwak 2025, J Clin Med 14(21):7671, PMID 41227066 | RADIOGRAPH LSTV detector: 3,116 laterals, reference = whole-spine imaging/CT/MRI; test 313: acc 76.4 %, sens 85.1 %, spec 61.9 %, AUC 0.84 (166/195 LSTV, 73/118 normal) | efetch abstract verbatim; already in memory as the only 2-D LSTV model |

## Per-source notes, in the order opened

### Liebl 2021 (claim 1)
- PMID 34711848 (esearch by DOI), DOI 10.1038/s41597-021-01060-0, PMC8553749, Sci Data 2021 Oct 28;8:284.
- Extractor read of PMC full text: 300 subjects, 319 CT series, 4,142 vertebrae (581 cervical, 2,255 thoracic,
  1,306 lumbar). Table 2: 12 thoracic 131 (90.3 %), 11 thoracic 8 (5.5 %), 13 thoracic 6 (4.1 %); 5 lumbar 165
  (65.5 %), 4 lumbar 3 (1.2 %), 6 lumbar 85 (33.7 %); stump ribs 90 (T12 37, T13 5, L1 48); cervical ribs 18;
  LSTV Castellvi II-IV 161. "Anatomical ratings were carried out by two neuroradiologists in a consensus reading."
  Segmentations: human-machine hybrid, corrected by trained medical students, approved by a neuroradiologist.
- Denominators: the percentages imply 145 subjects with the thoracolumbar junction rated and 253 with the
  lumbosacral junction rated. The 33.7 % L6 figure is enrichment by design ("enriched with cases that exhibit
  anatomical variants"), not prevalence. Abstract counts: enumeration abnormalities n = 77, transitional n = 161.
- Note the labelling convention: this is the set where an L6 label exists and stump ribs sit at T12, T13 and L1.
  The project's `versefusion-t13-flag-wrong` memory (manifest says 18, truth 6) matches the 6 T13 here.
- Statement on failures: only the general "fail in variants not frequently present in the training dataset";
  no per-variant rates in this paper (they are in Sekuboyina 2021).

### Sekuboyina 2021, VerSe (claim 2)
- PMID 34340104, DOI 10.1016/j.media.2021.102166, Med Image Anal 2021;73:102166. Europe PMC: not open access,
  not in PMC. arXiv 2001.09193 (v6 PDF > 10 MB, unreadable here); ar5iv HTML read by the extractor.
- Abstract (efetch, verbatim): "374 multi-detector CT scans from 355 patients ... 4505 vertebrae ... 25 algorithms
  were benchmarked ... The principal takeaway from VerSe: the performance of an algorithm in labelling and
  segmenting a spine scan hinges on its ability to correctly identify vertebrae in cases of rare anatomical
  variations."
- Full text (extractor): "VerSe'20 included six cases with T13 (2/2/2 in Train/Public/Hidden) and 47 cases with
  an L6 (15/15/17)." VerSe'19: two L6 in training, one in the hidden set. "None of the methods in VerSe'19
  identified the presence of L6." "In VerSe'20, almost all algorithms identify at least a fraction of the L6
  vertebrae." "Xiangshang Z. is the only approach that successfully identifies all T13 instances in both test
  phases." Top entries: Payer C. 94.25 % id-rate / 89.80 % Dice (VerSe'19 hidden); Chen D. 96.58 % / 91.23 %
  (VerSe'20 hidden).
- Discrepancy to record: the Sci Data paper counts 85 L6 subjects in VerSe'20; the benchmark paper counts 47
  L6 "cases" across train/public/hidden. Different denominators (subjects rated vs scans in the challenge
  splits, and Liebl counts every six-lumbar spine whereas the challenge counted labelled L6 instances); do not
  quote one as the other.

### VERIDAH, Möller 2026 (claim 3)
- arXiv 2601.14066, submitted January 20, 2026. Not peer reviewed; no PubMed record (esearch on Möller +
  Kirschke + enumeration returned only Schinz 2026). Code: github.com/Hendrik-code/spineps.
- Abstract (arXiv page): T2w sagittal 98.30 % vs 94.24 % of subjects with all vertebrae correctly labelled; CT
  99.18 % vs 77.26 %; thoracic enumeration anomalies labelled correctly in 87.80 % (T2w) and 96.30 % (CT);
  lumbar 94.48 % and 97.22 %.
- Full text (arXiv HTML, extractor): CT cohort "an in-house cohort consisting of images from various scanners",
  1,536 images (1,171 train / 365 test), TEA rate 5.5 % (6.8 % test), LEA 7.3 % (7.9 % test), mean 16.7 +/- 3.6
  visible vertebrae; annotations supervised by an expert with 24 years' experience. NAKO MRI 6,291 (5,291/1,000),
  TEA 5.8 %, LEA 9.7 %. Table 3 (CT): Meng et al. [16] 77.81 % all-correct, TEA recall 11.11 %, LEA recall
  61.11 %; Meng et al. zero-penalty 77.26 %, 14.81 %, 61.11 %. Table 4 (MRI): SpineNetV2 91.49 %, TEA 0.0 %,
  LEA 83.72 %; Warszawer et al. 94.24 %, 27.63 %, 83.04 %. Quote: "almost none of them consider TEA or LEA, as
  the existing systems can only predict a maximum of 12 thoracic and five lumbar vertebrae." Anomaly
  definition: thoracic vertebra = one with a true rib regardless of length; T11/T13 and L4/L6 counts.
- What it does NOT contain: TotalSegmentator and SPINEPS-on-CT are not among the CT baselines; the CT cohort is
  private. The 77 % baseline is Meng et al. (a graph-optimisation labeller), so it cannot be quoted as a
  TotalSegmentator or SPINEPS error rate.

### RibSeg v2, Jin 2023 (claim 4)
- PMID 37695967, DOI 10.1109/TMI.2023.3313627; efetch record says IEEE Trans Med Imaging 2023;PP (ahead of print);
  IEEE Xplore lists vol 43 no 1, January 2024 (search-result metadata, not opened). arXiv 2210.09309 v1 Oct 18
  2022 - v4 Aug 1 2023.
- Abstract (efetch, verbatim): "660 CT scans (15,466 individual ribs in total) and annotations manually inspected
  by experts for rib labeling and anatomical centerline extraction ... Our dataset, code, and model are available
  online ... https://github.com/M3DV/RibSeg."
- Full text (arXiv HTML v4, extractor): "24 classes for 24 ribs and 1 class for other bones and backgrounds";
  660 chest-abdomen CTs from RibFrac split 420/80/160; 6 cases "unqualified" from incomplete scanning; "99 cases
  in RibSeg v2 are categorized as challenging cases (47/19/33 in training/development/test)" (the search snippet
  said 121; the HTML says 99: re-read before quoting); challenge categories include metal, scoliosis, "floating
  ribs are missing or too vague to segment" and "might also exist a third stubby little floating rib (the 13th
  pair of ribs)". Best method (two-stage DGCNN) on test: Dice_avg(L) 90.5 %, label accuracy (A/F/I/T) 91.5 % /
  60.7 % / 96.3 % / 89.4 %; on challenging cases Dice 78.2 %, label accuracy 79.6 %. The A/F/I/T column meanings
  were not resolved by the extractor; do not expand them without the PDF.
- Decision relevance: a 24-label scheme has nowhere to put a 13th rib, so a 13-pair spine is labelled by
  displacement. Same structural limit as TotalSegmentator (rib_1..12).

### Nagata 2025, whole-spine CT (claim 5)
- PMID 40381031, DOI 10.1007/s00256-025-04952-z, Skeletal Radiol 2025;54(10):2169-2177. Not open access.
- Abstract (efetch, verbatim): counting "caudally from the cervical vertebra, based on the eighth being the first
  thoracic vertebra, the twentieth as the first lumbar vertebra, and the twenty-five being the first sacral
  vertebra"; sacralisation = 23 vertebrae, lumbarisation = 25; 551 patients (407 F, 144 M); LSTV 16.3 %
  (sacralisation 12.3 %, lumbarisation 4.0 %); rib abnormalities 14.0 % (twelfth hypoplastic rib 12.6 %, lumbar
  rib 1.5 %); "In patients with LSTV, all twelfth hypoplastic ribs were found in the sacralization group and all
  lumbar ribs were found in the lumbarization group (p < 0.001)."
- This is the cleanest published statement that the two junction anomalies are coupled in a fixed direction,
  which is the basis for using rib morphology as an independent route to the lumbosacral phenotype.

### Hanhivaara 2024, CR vs CT vs MRI (claim 6)
- PMID 39444351, DOI 10.1177/02841851241289355, Acta Radiol 2024;65(12):1515-1520. Not open access; SAGE 403.
- Abstract (efetch, verbatim): 852 patients screened on CT, 100 with LSTV anatomy; four blinded independent
  readers per modality; gold standard = experienced fellowship-trained radiologist using all three; CT
  sensitivity/specificity/accuracy/balanced accuracy 76/93/77/84 %; MRI 54/88/56/68 %; CR 32/85/42/59 %; kappa
  CT 0.63-0.71, CR 0.16-0.32, MRI 0.24-0.56.
- It measures Castellvi TYPE agreement, not vertebra numbering. It is the radiograph-vs-CT disagreement number
  that exists; a radiograph-vs-CT numbering-discrepancy series was not found (see Not found).

### Schinz 2026, thoracolumbar junction labelling on CT (claim 7)
- PMID 41003722, DOI 10.1007/s00586-025-09364-0, Eur Spine J 2026 Apr;35(4):2195-2203. Authors include Möller,
  Sekuboyina, Kirschke.
- Abstract (efetch, verbatim): 1,242 subjects (mean age 63 +/- 12; 771 women), CT 2005-2018 covering the complete
  thoracolumbar spine; three classifications compared: continuous counting (CCBC), rib-length/rib-based
  (RLBC/RBC), vertebra-shape-based (VSBC). "Only the VSBC perfectly complied with the nerve morphology (VSBC,
  100%; RBC, 97.2%, RLBC, 96.3%; CCBC, 92.6%)." Inter-rater 0.61 vs 0.59. "even for anatomical variants or
  incompletely visualized spines."
- Decision relevance: an independent group measured that shape beats rib counting and beats counting for naming
  the TL junction on CT, with nerve morphology as the external check. Directly supports the local-morphology
  thesis and gives the third-route check (nerve roots) the project has not used.

### Dead ends and partial reads
- pubmed.ncbi.nlm.nih.gov article pages: cookie wall, no content (37695967, 40381031). efetch used instead.
- ScienceDirect S2405631625000430 (Netherton 2025) and S2773157X25002450 (Indian TLTV CT cross-sectional, TLTV
  11.1 %, absent 12th rib the commonest type per the search snippet): 403. The Netherton paper was reached via PMC;
  the Indian TLTV paper was not opened and is not cited.
- SAGE (Hanhivaara 2024) and JNS (Sabri 2025): 403; abstracts via efetch.
- arXiv PDF 2001.09193v6: exceeded 10 MB; ar5iv HTML used. Radboud repository PDF: 403.
- Europe PMC REST: `PMID:` and `DOI:` query forms returned hitCount 0; `EXT_ID:<pmid> AND SRC:MED` works.
- TotalSegmentator paper text (PMC10546353): no class list in the body; class list taken from the GitHub README
  ("total" task, 117 classes, vertebrae_C1..L5, vertebrae_S1, sacrum, rib_left/right_1..12).
- Yang 2025 (Sci Rep): extractor could not find per-variant case counts; the code link is the VerSe challenge
  repository, so no author code is confirmed.
- Möller 2025 stump ribs: cohort sizes as extracted do not sum; re-read Table 1 before quoting anything beyond
  the abstract's Dice 0.997 / 0.779, 98.2 % length-assessment success and F1 0.84.
- Kwak 2025: radiograph only; already known to the project.

## Not found
- A peer-reviewed measurement of TotalSegmentator's or SPINEPS's vertebra- or rib-mislabelling rate on LSTV / T13
  / L6 spines. VERIDAH (preprint) measures a graph labeller (Meng et al.) at 77.8 % all-correct and 11 % thoracic
  anomaly recall on a private CT cohort; nobody has published the same for TotalSegmentator or SPINEPS on CT.
  The nearest statements are structural: both tools' label sets stop at rib 12 / L5 (README; RibSeg v2 25 classes).
- A CT-based LSTV/TLTV classifier validated against radiologist reads with a Castellvi-type output. VERIDAH gives
  count anomalies (L4/L6, T11/T13), not Castellvi types; Yang 2025 gives T13/L6 presence on VerSe labels.
- A primary series measuring radiograph-versus-CT vertebra NUMBERING disagreement (as opposed to Castellvi type
  agreement) in the same patients. Sabri 2025 is radiograph-only; Hanhivaara 2024 is type agreement.
- An automated rib-counting method evaluated on spines with 11 or 13 rib pairs with a stated per-case accuracy.
  RibSeg v2's "challenging" subset mixes metal, scoliosis and rib anomalies, so its 79.6 % is not a 13-rib number.
