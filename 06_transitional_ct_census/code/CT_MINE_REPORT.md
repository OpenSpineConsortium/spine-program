<!-- copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/CT_MINE_REPORT.md; tracked at commit 097933a. The banned word, where it occurred, is rewritten as origin. -->

# CT mine — what we could still get, and what is already sitting in our own labels

Two halves. Part 1 is prior art: image collections that could supply transitional or
numerical spinal anatomy and are **not** in `docs/DATASETS_ROADMAP.md`. Part 2 is a mine of
the three CT collections we actually hold on disk, with every anomaly flag derived from the
label volumes themselves and nothing read from a published table.

Run 2026-09-15. Code: `tools/mine_spine_anomaly.py` (per-case features),
`tools/mine_spine_validate.py` (signature testing against an external table),
`tools/mine_spine_final.py` (flags, cross-check, candidate list). Features and candidates
under `/home/gschwing/ct_mine/`.

---

# Part 2 first, because it is the shorter answer

## What we actually hold

Checked on the grid. The roadmap lists nine external collections; **three are on disk.**

| Collection | On disk | Size | Path | Cases |
|---|---|---|---|---|
| CTSpinoPelvic1K (release labels) | yes | 227 GB | `~/data/CTSpinoPelvic1K/{ct,labels}` | 802 |
| TotalSegmentator v2.0.1 | yes | 82 GB | `~/data/TotalSegmentator/s*/segmentations` | 1,228 |
| VerSe 19+20 (VerSeFusion unified) | yes | 139 GB | `~/VerSeFusion/data/unified/scan-*` | 374 |
| CTSpine1K | **no** | — | — | — |
| CTPelvic1K | **no** | — | — | — |
| RibSeg v2 / RibFrac | **no** | — | — | — |
| CADS | **no** | — | — | — |
| VertebralBodiesCT-Labels | **no** (the table now is, see below) | — | — | — |
| Möller stump-rib masks | **no** (only the derived CSV, in the label table) | — | — | — |

Also on the grid and derived from the three above, so adding no new subjects:
`~/implant_ct` (427 GB, 1,518 CTSpinoPelvic1K-derived label volumes), `~/implant_verse`
(187 GB, 1,119), `~/implant_ts` (39 GB), `~/bench/ct_by_case` (the 802 CTSpinoPelvic1K CTs,
all COLONOG-sourced), `~/vf_813`, `~/vf_v10`, `~/rib-segmentation`.

The label table we compare against, `~/lstv_flag/sources/TRANSITIONAL_LABELS.csv`, has 4,245
rows: VerSe 325, Möller 320, BUU-LSPINE 3,600. **It contains no CTSpinoPelvic1K rows and no
TotalSegmentator rows at all**, so every flag raised on those two is new to it by
construction; the interesting number is what is new to the table *and* to the external
tables, and that is what the counts below report.

## Label schemes read, per dataset

Named because getting this wrong is how this project has lost time three times.

- **CTSpinoPelvic1K** — v10, read from the release: 8–19 = T1–T12, 20–24 = L1–L5, 25 = L6,
  26 = sacrum, 29 = S1, ribs 34–46 left and 47–59 right (index 13 = the T13 rib), lumbar
  ribs 60/61, hips 30/31, femurs 32/33.
- **VerSe** — VerSe-native ids in `scan-*_msk.nii.gz`: 1–7 = C, 8–19 = T1–T12, 20–24 = L1–L5,
  **25 = L6**, 26 = sacrum, 28 = T13.
- **TotalSegmentator v2.0.1** — one binary mask per structure *name*: `vertebrae_C1`…`C7`,
  `T1`…`T12`, `L1`…`L5`, `vertebrae_S1`, `sacrum`, `rib_left_1`…`12`, `rib_right_1`…`12`.
  **There is no name for an L6 and no name for a T13.** That is the whole point of the
  TotalSegmentator part of this exercise.

All volumes canonicalised to RAS with `nibabel.as_closest_canonical` for analysis only.
Nothing was written back.

## Field of view — so an absent structure is never read as a missing one

Every flag below is gated on the field actually covering the question. Counts are cases.

| | CTSpinoPelvic1K (802) | TotalSegmentator (1,228) | VerSe (374) |
|---|---|---|---|
| sacrum labelled | **802** | 604 | **0** |
| L1 labelled | 802 | 780 | 298 |
| T12 labelled | 800 | 861 | 272 |
| rib 1 labelled | — (out of field by design) | 731 | **0** |
| rib 12 labelled | 789 | 740 | **0** |
| lumbosacral junction answerable | 802 | 509 | **0** |
| whole presacral column in field | 0 | **43** | 0 |

Three facts here matter more than the flags:

1. **The VerSe masks carry no sacrum and no ribs at all** — 0 of 374 on both. Every
   lumbosacral and every rib question is unanswerable in VerSe from the masks. VerSe's
   contribution is the vertebra labels and nothing else.
2. **TotalSegmentator can answer the lumbosacral question on only 509 of 1,228 cases.** The
   rest are chest, head-and-neck or limb fields. Any TotalSegmentator prevalence quoted
   against 1,228 is wrong by a factor of two and a half.
3. **The whole presacral column is in field on 43 TotalSegmentator cases and nowhere else we
   hold.** Counting down from C2 is possible on 43 cases out of 2,404. That is the
   quantitative version of the local-identity argument, measured on our own disks.

## The TotalSegmentator question, answered

The premise was right. TotalSegmentator labels C1–L5 plus sacrum and cannot express an L6,
so a six-lumbar patient is silently mislabelled. **Of the 28 TotalSegmentator cases an
external table independently marks as L6, 27 carry exactly five lumbar labels.** The scheme
does not drop the extra segment; it renames the column around it.

Where does the extra body go? I tested six candidate signatures against those 28 external
positives and 1,060 external negatives. Three of them — the ones a person would reach for
first — do not work:

| candidate signature | L6 positives (median) | negatives (median) | positives above the negatives' p95 |
|---|---|---|---|
| L5 body height | 54.0 mm | 49.5 mm | 5 / 28 |
| L5 voxel count | 19,172 | 18,634 | 2 / 28 |
| sacrum height | 136.5 mm | 139.5 mm | 0 / 27 |
| sacrum / L5 height ratio | 2.56 | 2.80 | 0 / 27 |
| L5 / L4 height ratio | 1.026 | 1.029 | 0 / 28 |
| **span, lowest rib-bearing vertebra to sacrum** | **180.5 mm** | **160.5 mm** | **13 / 26** |
| **step between the five named lumbar** | **35.4 mm** | **32.5 mm** | **11 / 28** |

TotalSegmentator does **not** absorb the extra vertebra into a fat L5 or a long sacrum. It
spreads five names over six bodies: the lumbar column gets longer and the apparent step
between consecutive named lumbar gets bigger. Both follow from one extra body and neither is
visible in any single label's size.

A scale-free version — span divided by step, i.e. "how many segments fit between the lowest
rib and the sacrum" — is **worse** (8/26 rather than 13/26), because the step is itself
inflated by the same mechanism and the division cancels the signal. That is worth writing
down: the obvious normalisation destroys the thing being measured.

**The detector actually used** is the union of two rules, both cohort-calibrated on the data
rather than on a textbook:

- *span* from the lowest rib-bearing vertebra down to the top of the sacrum above the
  cohort's 95th percentile (183.4 mm) **and** the median step between the five named lumbar
  above its 95th percentile (36.8 mm) — "five names spread over six bodies";
- the 12th rib articulating with the vertebra named **T11 on both sides** — "the names run
  one ahead of the rib count".

Union: **28 TotalSegmentator cases flagged, 14 confirmed by the external table, 50 %
precision against a 3.2 % base rate — a sixteen-fold enrichment — and 14 new.**

## Counts, per dataset, per anomaly

`held` = already in `TRANSITIONAL_LABELS.csv`. `external` = already in
`fhofmann/VertebralBodiesCT-Labels` (`data.csv`, 1,088 TotalSegmentator + 372 VerSe rows,
per-case `L6` and `T13`). `new` = in neither.

### TotalSegmentator (1,228 cases; 0 in our label table)

| anomaly | flagged | confirmed external | **new** | confidence |
|---|---|---|---|---|
| six lumbar — span + step rule | 16 | 8 | **8** | medium |
| six lumbar — span alone | 9 | 2 | **7** | low |
| numbering shift — 12th rib on T11 bilaterally | 12 | 6 | **6** | medium |
| *union of the two medium rules* | *28* | *14* | *14* | *medium* |
| thirteenth rib — 12th rib on L1 **bilaterally** | 5 | 0 | **5** | medium |
| thirteenth rib — one side only | 41 | — | — | **rejected, see below** |
| lumbosacral contact, mostly one-sided | 20 | — | **20** | low |
| unequal rib count left vs right, cage in field | 10 | — | **10** | low |
| presacral count ≠ 24 with the whole column in field | 2 (`s1178` = 20, `s1310` = 23) | — | **2** | medium |
| four lumbar between a rib-bearing T12 and the sacrum | 1 (`s0171`) | — | **1** | medium |

### CTSpinoPelvic1K (802 cases; 0 in our label table)

| anomaly | flagged | **new to the label table** | confidence |
|---|---|---|---|
| six lumbar — explicit L6 label (25) | 18 | 18 | high |
| six lumbar — span + step rule, five lumbar labels | 13 | 13 | medium |
| six lumbar — span alone | 15 | 15 | low |
| lumbar rib — explicit labels 60/61 | 16 | 16 | high |
| thirteenth rib — 12th rib on L1 bilaterally | 3 | 3 | medium |
| numbering shift — 12th rib on T11 bilaterally | 2 | 2 | medium |
| four lumbar between a rib-bearing T12 and the sacrum | 9 | 9 | medium |
| lumbosacral contact, mostly one-sided | 5 | 5 | low |

The 18 explicit L6 labels and the 16 lumbar-rib labels reproduce
`~/lstv_flag/ANOMALY_INVENTORY.md` exactly, from the label volumes, with no table consulted.
The four-lumbar count is 9 rather than the inventory's 13 because this rule additionally
requires a rib-bearing T12 in field; 13 cases carry four lumbar labels, 9 of them with the
rib anchor present to make the count mean something.

### VerSe (374 cases; 325 in our label table)

| anomaly | flagged | in our table | in the external table | **new** |
|---|---|---|---|---|
| six lumbar — explicit L6 label (25) | 50 | 47 | 41 | **3 to our table, 1 to both** (`gl279`) |
| T13 vertebra — explicit label 28 | 6 | 6 | 6 | 0 |
| anything rib- or sacrum-derived | — | — | — | **not askable; the masks have neither** |

The three-way disagreement is the useful part. Our derived count is 50, our table says 47,
the external table says 41. Nine VerSe cases carry an L6 label of ≥200 voxels that the
external table calls negative. Its authors count only a *free* transitional vertebra as
lumbar and call a fused one sacrum, so a Castellvi III/IV case is an external negative and a
VerSe-label positive. That is a definition difference, not an error in either, and it is the
same substitution trap the project has hit before: two finite, plausible numbers from two
different definitions of the same word.

## New candidates, beside what we already have

| anomaly | already held (ANOMALY_INVENTORY) | **new from this mine** | where the new ones are |
|---|---|---|---|
| six lumbar | 118 | **+24 medium, +22 low** | medium: TotalSegmentator 8, CTSpinoPelvic1K 13, VerSe 3. low: TotalSegmentator 7, CTSpinoPelvic1K 15 |
| four lumbar | 145 | **+1** | TotalSegmentator `s0171`. The 9 CTSpinoPelvic1K four-lumbar cases are a subset of the 13 already counted |
| thirteenth rib | 0 | **+8** | TotalSegmentator 5, CTSpinoPelvic1K 3 |
| lumbar rib | 16 | **0 new** (the 16 reproduced independently) | — |
| numbering shift / names ahead of the rib count | not previously flagged | **+14** | TotalSegmentator 12, CTSpinoPelvic1K 2 |
| presacral count ≠ 24 | not previously flagged | **+2** | TotalSegmentator |
| rib count asymmetry | not previously flagged | **+10** | TotalSegmentator |
| lumbosacral bar, one-sided | Castellvi II–IV 140 | **+25 ranked, unconfirmed** | TotalSegmentator 20, CTSpinoPelvic1K 5 |
| T13 vertebra | 6 | 0 new | — |
| Castellvi I | 0 separable | **still 0** | — |

Full list with per-case evidence: `/home/gschwing/ct_mine/new_candidates.csv`
(dataset, case id, anomaly, evidence, confidence, in_our_label_table, in_external_table, path).

## How reliable each derived flag is, and what would confirm it

- **Explicit label present (L6, T13, lumbar rib 60/61)** — high. It is the source's own
  statement. The only risk is the label being small or spurious; the 200-voxel floor handles
  specks. Confirmed by reproducing the inventory counts exactly.
- **Six lumbar by span + step** — medium; measured 50 % precision at a 3.2 % base rate on the
  only subset where an external per-case label exists. Confirm by rendering the lumbar column
  of each candidate and counting bodies. Fifty per cent precision means half the list is
  wrong and the render is not optional.
- **Six lumbar by span alone** — low; 2 of 9 confirmed. Keep as a ranked worklist, not a label.
- **Twelfth rib on L1, bilaterally** — medium. This is the one flag checked against something
  fully outside: bilateral gives 0.73 % of TotalSegmentator cases with both 12th ribs in
  field, against a published CT-based lumbar-rib prevalence of 1.6 % of which 65 % are
  bilateral, so about 1.0 % expected. Agreement. **The unilateral version gives 6.0 %, eleven
  times the published unilateral rate, so the one-sided reading is dominated by rib heads
  flipping across the T12/L1 boundary and is reported as rejected rather than as 41 cases.**
  That check is the only reason the count is 5 and not 46.
- **Numbering shift (12th rib on T11 bilaterally)** — medium; 6 of 12 carry an externally
  labelled enumeration variant. Confirm by counting from the top on the 43 cases where that
  is possible, and by rendering the rest.
- **Rib-to-vertebra assignment generally** — this was wrong on the first pass and the symptom
  was a plausible number: 252 of 802 CTSpinoPelvic1K cases read as "names ahead of the rib
  count", which is 31 % and cannot be true. Two causes, both fixed: the medial 15 % of rib
  voxels drags the shaft in and moves the answer a level, and "the first vertebra whose
  z-range contains this point" is biased superiorly because adjacent vertebra ranges overlap
  through the spinous process. With the head taken as the medial 3 % and the assignment made
  to the nearest vertebra centroid, ribs 10, 11 and 12 land on T10, T11 and T12 on both sides
  in the normal case, and the flag count fell from 252 to 2.
- **Lumbosacral bar / fusion by contact and asymmetry** — low, and it is a ranking, not a
  detection. Label-to-label contact under a one-voxel dilation cannot distinguish a true
  osseous bridge from two surfaces that the segmentation left touching. Confirm by rendering.
  **A Castellvi I case has no bony contact at all and will never appear here**, which is the
  same blind spot the inventory already records.
- **Rib count asymmetry** — low. A missing rib is at least as often a segmentation miss as an
  anatomical absence.
- **Field-of-view gating** — the top/bottom cropping test uses whether a structure's mask
  touches the volume's boundary slice. That is reliable for gross truncation and unreliable
  where a structure is present but thin at the edge.

## What is not known

- Whether the 14 new TotalSegmentator six-lumbar candidates are real. Fifty per cent
  precision on the labelled half says roughly seven of them are. Which seven is not known
  and will not be known without rendering.
- Why 9 VerSe cases carry an L6 label that the external table calls negative. The
  free-versus-fused definition explains it plausibly and has not been tested. The project's
  own record on tidy explanations that arrive unprompted is poor.
- Whether the 20 TotalSegmentator one-sided lumbosacral contacts are Castellvi bars,
  degenerative bridging, or segmentation adjacency. Nothing in the label volume separates
  these three.
- Castellvi I remains not separable anywhere, in any collection we hold or found. It is
  roughly two thirds of all transitional anatomy and it contaminates every negative set we
  have. Nothing in Part 1 changes this.

---

# Part 1 — prior art: what the roadmap is missing

The roadmap's inventory is nine CT collections. The search below covers TCIA in full
(enumerated through the NBIA API rather than by search), large public abdominal and
whole-body segmentation sets, screening and biobank cohorts, forensic and post-mortem
archives, paediatric collections, vertebra-labelling challenges, and radiograph collections.

## The one finding that changes what to mine

**`fhofmann/VertebralBodiesCT-Labels` carries a per-case L6 and T13 column for 1,088
TotalSegmentator scans and 372 VerSe scans.** The roadmap lists this dataset as an "optional
bodies-only aux" source. It is not: its `data.csv` is a free per-case enumeration label for
two collections we already hold. 28 L6 and 7 T13 in TotalSegmentator; 41 L6 and 7 T13 in
VerSe. It is the external check used throughout Part 2 and it should be promoted in the
roadmap from optional to a labels source.

Caveats before trusting it: it counts only a *free* transitional vertebra as lumbar and calls
a fused one sacrum, so `L6=1` is a lumbar-count flag and not a Castellvi grade; and where T1
is outside the field it *assumes* twelve thoracic and defines L1 by a 4 cm rib rule — the
same "a first-slice-that-works is not a plane" substitution recorded in `CLAUDE.md`. Its
`suppl/2_errors.md` also lists roughly 450 TotalSegmentator cases whose original spine labels
the authors judged wrong.

Downloaded to `/home/gschwing/ct_mine/ext/vbct_data.csv` (127 KB).

## CT — the short list, in order of value

| Name | Size | Modality | Labelled | Transitional / numbering label | Licence | Route | Verdict |
|---|---|---|---|---|---|---|---|
| **autoPET / FDG-PET-CT-Lesions** | 900 subjects, 1,014 studies | Diagnostic CT **skull base → mid-thigh**, 2–3 mm | lesions only | derivable, and the only open source where C2 **and** the sacrum are in the same volume | CC BY 4.0 | cancerimagingarchive.net/collection/fdg-pet-ct-lesions/ · 10.7937/gkr0-xv29 | **TODAY**, 419 GB |
| **PSMA-PET-CT-Lesions** | 378 patients, 597 whole-body studies | CT skull base → mid-thigh, 2.5–5 mm | lesions | same; male only | CC BY 4.0 | 10.7937/R7EP-3X37 | **TODAY**, 117 GB |
| **Merlin Abdominal CT** (Stanford AIMI) | **25,494 CT / 18,317 patients** | Abdomen **and pelvis**, emergency department 2012–18, NIfTI | reports, no segmentations | derivable; unselected ED population, the right sampling frame for prevalence | Stanford AIMI DUA, non-commercial | stanfordaimi.azurewebsites.net → AzCopy | **REQUEST** (one form) |
| **NMDID** | **15,243 decedents**, head-to-toe PMCT, 1 mm | PMCT | 59 metadata variables | derivable, unselected population, both label routes on one case | custom DUA — **forbids derivative works, redistribution and commercial use**, 1-year term | nmdid.unm.edu | **REQUEST**; see the licence note below |
| **EAY131 (NCI-MATCH)** | **2,813 patients**, 796 GB | CT/MR/PET; SPINE, TSPINE, CHESTABDOMEN, ABDOMENPELVIS series | none | derivable | **CC BY 4.0, public download, no application** | cancerimagingarchive.net/collection/eay131/ | **TODAY** |
| **Spinal-Multiple-Myeloma-SEG** | 67 patients / 72 scans | dual-energy CT | **individual vertebrae segmented and typed** | label already exists | CC BY 4.0 | 10.7937/k4qv-hh78 | **TODAY** |
| **Spine-Mets-CT-SEG** | 55 scans | CT | **per-vertebral-level masks** + lesion class | label already exists | CC BY 4.0 | 10.7937/kh36-ds04 | **TODAY** |
| **NLST** | **26,254 subjects**, 11.3 TB | low-dose chest CT | clinical subset | **ribs only** — cervical rib, 13th rib, hypoplastic 12th, at n=26k. No sacrum | CC BY 4.0, no application for images | 10.7937/TCIA.HMQ8-J677 | **TODAY** |
| **CT-RATE** | 25,692 chest CT / 21,304 patients | chest CT + reports | abnormality labels | ribs only | CC BY-NC-SA 4.0, gated | huggingface.co/datasets/ibrahimhamamci/CT-RATE | **REQUEST** (click-through) |
| **RSNA 2023 Abdominal Trauma** | 4,711 series, 23 sites, 14 countries | trauma abdominopelvic CT | injury labels; organ masks on 206 | derivable; broadest demographics of any trauma corpus | Kaggle non-commercial | kaggle.com/competitions/rsna-2023-abdominal-trauma-detection | **REQUEST** |
| **Pediatric-CT-SEG** | **359**, 5 days–16 y | CT chest-abdomen-pelvis | 29 RTSTRUCTs; skeleton is one "Bones" class, **no vertebrae** | derivable; the only open paediatric CAP CT | CC BY 4.0 | 10.7937/TCIA.X0H0-1706 | **TODAY** |
| **CT COLONOGRAPHY (ACRIN 6664)** | 825 subjects, **prone and supine each** | abdominopelvic, screening | polyps | derivable | CC BY 3.0 | 10.7937/K9/TCIA.2015.NWTESAY1 | **TODAY**, but see the dedupe note |
| **AMOS22** | 500 labelled + 2,000 unlabelled | CT | 15 organs incl. bladder, prostate | derivable | CC BY 4.0 | zenodo.org/record/7262581 | **TODAY** |
| **PENGWIN** | 100 CT (2024), 170+480 (2026) | pelvic CT | **sacrum + hipbones as fracture fragments** | partial; pelvic FOV usually reaches L4/L5 | CC BY 4.0 / CC BY-NC 4.0 | 10.5281/zenodo.10927452 | **TODAY** |
| **AbdomenAtlas 1.1 / 3.0** | 9,262 CT | CT + reports | 25 structures; **no vertebrae, no sacrum, no ribs** | derivable from images | CC BY-NC-SA 4.0 | huggingface.co/datasets/AbdomenAtlas | **REQUEST** / TODAY (3.0Mini) |
| **MSD Task03/06/07/09/10** | 131/63/281/41/126 | CT | organ + tumour | derivable where the field allows | CC BY-SA 4.0, no account | `aws s3 ls --no-sign-request s3://msd-for-monai/` | **TODAY** |
| **TotalSegmentator-MRI** | 616 subjects | **MRI** | per-level vertebrae, sacrum | labels exist | Apache-2.0 | zenodo 11367004 | **TODAY** |
| **StageII-Colorectal-CT** | 230 | abdomen + pelvis, 5 mm | none | countable, too thick to measure | CC BY 4.0 | 10.7937/p5k5-tg43 | **TODAY** |
| **CMB-\*** (Cancer Moonshot Biobank) | ~550 and growing | WHOLEBODY, LSPINE, TSPINE CT | none | derivable; the only *growing* open source | CC BY 4.0 | cancerimagingarchive.net/collection/cmb-mml/ etc. | **TODAY** |
| **NCI Imaging Data Commons** | mirrors TCIA + NLST + CPTAC | — | — | **an access route, not a dataset** — no registration, queryable by `BodyPartExamined` in BigQuery | per-dataset | portal.imaging.datacommons.cancer.gov | **TODAY** |
| **VIFM (Melbourne)** | ~100,000 full-body PMCT | PMCT | none | derivable | VIFM/Justice HREC | vifm.org | **REQUEST** (months, needs a local co-investigator) |
| **NAKO** (German National Cohort) | ~30,000 imaged | MRI; MSK block has a **composed whole-spine sagittal** | none | the only population cohort with a sequence you can count on | TransferHub, EU/EEA + GDPR countries — a US applicant is a live risk | nako.de | **REQUEST** |
| **SHIP** (Pomerania) | whole-body MRI | MRI | none | spine sequence content unverified | **free**, FAIRequest form | transfer.ship-med.uni-greifswald.de | **REQUEST** |
| **UK Biobank** | ~100,000 | **no CT**; Dixon MRI + iDXA lateral spine T4–L4 | none | weak for Castellvi (needs the transverse-process/ala articulation) | AMS application, Tier 3 for bulk imaging | biobank.ndph.ox.ac.uk | **REQUEST**, low yield |
| **Glocker spine CT** (SpineWeb #3) | 125 patients / 242 scans | CT, pathological | **named centroids C1→L5/S** in `.lml` — the enumeration ground truth | names, no variant flag | CC BY-NC-ND 4.0 | biomedia.doc.ic.ac.uk/data/spine → Box `UWSpineCT` | **TODAY** |
| **xVertSeg** | 25 CT | lumbar CT | L1–L5 + fracture grades | names only | CC BY-NC-ND | lit.fe.uni-lj.si (moved; old path 404s) | **TODAY** |
| **CSI 2014** | 20 CT | CT | labels 8 = T1 … 24 = L5 | names only | ODC-BY | zenodo.org/records/7049844 | **TODAY** |
| **SPIDER** | 447 series / 218 patients | **lumbar MRI** | vertebrae, discs, canal, gradings | **explicitly not derivable** — see the note below | CC BY 4.0 | zenodo.org/records/10159290 | **TODAY** |

**Verified negatives worth not re-searching:** Soft-tissue-Sarcoma (limb only), LIDC-IDRI and
LUNA16 (no lumbar, no sacrum), DeepLesion and ULS23 (crops and key slices), SegTHOR, MELA,
MedShapeNet, Stanford COCA, MosMedData, BLSA and Health ABC (a *single* 2-D slice each —
cannot number a spine at any price), China Kadoorie (no CT or MRI pixels), OAI (knee, pelvis,
hand — zero spine), PLCO (chest **radiographs**, not CT), Visible Human (n = 2), SMIR
(repository closed 2025-02-26), VISCERAL (host gone), Virtopsy (domain does not resolve),
Hamann-Todd (closed, explicitly including existing digital datasets), Terry and Bass and
Coimbra and DHOC (dry bone, no vertebral columns digitised), HiP-CT (organs only), UTSW
whole-body TG-430 (committee members only), AREN0532/0533/0534 (1,077 paediatric abdominal
CT, access points "Unavailable", route is the NCTN Data Archive).

**SpineWeb is dead.** `spineweb.digitalimaginggroup.ca` is NXDOMAIN and the parent domain has
been re-registered. The index held 16 datasets, not 18; four survive because third parties
re-host them, listed above. `spinesegmentation-challenge.com` (MRSpineSeg, 215 cases) is also
NXDOMAIN.

## Published prevalence on a named public dataset — free labels

This is the category the VerSe variant table exemplifies. Ranked by usefulness.

| Paper | Dataset named | Variant and count | Per-case ids? |
|---|---|---|---|
| **Hofmann et al., VertebralBodiesCT-Labels** (HF, CC BY-SA 4.0, paper under submission) | **TotalSegmentator 1,088 + VerSe 372** | **69 L6** (28 / 41) and **14 T13** (7 / 7) | **yes — `data.csv`, one row per case, ids `tseg-sXXXX` / `verse-XXX`** |
| Möller et al. 2025/2026, *AI* 7(6); arXiv 2505.05004 | **VerSe 323 + RibFrac 420** | **133/648 subjects (20.5 %) with ≥1 stump rib** | partly — no CSV, but per-case masks on Zenodo 14850928 plus the length algorithm, so reconstructible exactly |
| Jin et al. 2023, *IEEE TMI* 42(11), RibSeg v2 | **RibFrac/RibSeg v2, 660 CT** | 74 flagged; **37 bilateral + 5 unilateral "missing floating rib — 12th" without "partly scanned"** — i.e. 11-rib candidates, not field-edge artefacts | **yes — public Google Sheet, one row per `RibFracNNN.npz`** |
| Sun et al. 2025, *Communications Biology* 8:1614 | **UK Biobank**, 500 unselected controls | L6 3.2 %, four lumbar 1.6 %, complete sacralisation 3.6 %, transitional S1 3.8 %, 11 rib pairs 2.6 %, hypoplastic 12th 3.4 %, L1 ribs 2.0 % | no — aggregate; per-participant annotations only via a UKB application |
| Zenodo 4270094, "Segmented lordotic angles to assess LSTV on EOS" | 906 EOS patients | **172 LSTV (19 %)**, Castellvi I 52 % / II 24 % / III 19 % / IV 5 % | ids yes, **images no** — a 70 KB spreadsheet |

The roadmap's claim that the RibSeg v2 challenging-case sheet flags T13 does not hold up: the
sheet has 74 rows and the recurring description is "missing floating ribs — 12th". Where that
appears *without* "partly scanned" it is an 11-rib or hypoplastic-12th candidate, which maps
directly onto the field-edge rule the rib table already uses. Worth correcting in the roadmap.

**Outside checks, no data attached** — these are the values to test derived rates against:
Nagata et al. 2025, *Skeletal Radiology* 54:2169, whole-spine CT n=551: LSTV **16.3 %**
(sacralisation 12.3 %, lumbarisation 4.0 %), rib abnormality 14.0 %, and **every hypoplastic
12th rib fell in the sacralisation group and every lumbar rib in the lumbarisation group** —
a directional prediction our own labels can be tested against. Yoon et al. 2024, *AJNR*
45:119, 450 asymptomatic young adults: atypical presacral segment count 23.8 %, cervical rib
4.2 %, thoracolumbar transitional 15.3 %, LSTV 26.4 %. Osiowski et al. 2024, *Surg Radiol
Anat* 46:2057, meta-analysis: lumbar rib **2.1 % pooled, 1.6 % in CT-based studies, bilateral
in 65.4 %** — the figure the bilateral rib rule above was checked against. Poolman et al.
2023, *J Anat* 243:311, Pretoria Bone Collection n=187: thoracolumbar transitional **35 %**,
70 % of those carrying numeric variation elsewhere. Müller et al. 2024, *J Anat* 244:594:
in sacralised spines, pelvic incidence measured at the conventional first non-mobile segment
is **30.2°** against **58.6°** at the true S1 — the same one-bad-landmark failure recorded in
`docs/SPINOPELVIC_ESTIMATOR.md`, quantified by someone else.

**Searched and empty.** No published variant-prevalence audit exists for CTSpine1K,
CTPelvic1K, AMOS, FLARE, AbdomenCT-1K, AbdomenAtlas, DeepLesion, LIDC-IDRI, NLST, CT
Colonography, BUU-LSPINE, VinDr-SpineXR, NHANES II, MrOS, Rotterdam, SHIP or Framingham.
NMDID has 26 indexed papers and none on vertebral or rib numerical variation. Zenodo
full-text "Castellvi" returns 70 records and 12 datasets, of which the only imaging ones are
CTSpinoPelvic1K and its build archive; HuggingFace returns 0 for `Castellvi`, `lumbosacral`
and `transitional vertebra`; Kaggle returns an empty list for both; figshare returns
veterinary canine LSTV. **There is no second Castellvi-annotated imaging dataset in public
existence.**

## Radiographs we have missed

We hold BUU-LSPINE (3,600), NHANES II lumbar (7,408, unlabelled), VinDr-SpineXR, CSXA, the
Mendeley landmark set and AASCE. Genuinely new:

| Name | Size | View | Labelled | Enumeration possible? | Licence | Route | Verdict |
|---|---|---|---|---|---|---|---|
| **NHANES II cervical films** | **9,667 films** | lateral cervical in maximum flexion, 16-bit TIFF | nothing | **yes** — C2 in frame on every film | US public domain | wwwn.cdc.gov/nchs/data/nhanes2/NH2_Xray.htm, re-released Aug 2025 | **TODAY** — the half of NHANES II not on our list |
| **VertXNet reference-vertebra labels** | 600 films, 445 usable | over NHANES II cervical + lumbar | **C2 and S1 reference-vertebra coordinates** | yes — level-anchoring metadata for films we already hold | CC BY 4.0 | zenodo.org/records/10223910 | **TODAY** |
| **Curated AASCE annotations** | 609 AP films | annotations only | 4 corners per vertebra **with level names**, plus a correction log for AASCE's own label noise (documents "L5 at the position of T1") | **yes — named levels, which raw AASCE does not give** | open | zenodo.org/records/4413665 | **TODAY** |
| **VinDr-RibCXR** | 245 films | frontal CXR | **20 individually numbered ribs, R1–R10 and L1–L10**, pixel masks | yes, but **stops at rib 10** — short of where the 11/13-pair signal lives | code MIT, data by signed DUA | github.com/vinbigdata-medical/MIDL2021-VinDr-RibCXR | **REQUEST** (not on PhysioNet) |
| **PadChest** | >160,000 images, 6 view positions | PA / lateral / AP-horizontal / paediatric | 174 findings, 104 anatomical locations; ontology verified to hold `rib`, `anterior rib`, `posterior rib`, `dorsal/cervical/lumbar vertebrae`, `scoliosis` | derivable; cheapest route to a real-film supernumerary-rib cohort **if** the dictionary carries "cervical rib" — unconfirmed | research RUA | bimcv.cipf.es/bimcv-projects/padchest/ | **REQUEST** |
| **PAXRay++** | 7,377 images, 157 classes | **CT forward-projections, not real films** | `rib_anterior_1…12`, `rib_posterior_1…12`, T1–T12 | fully enumerated, on projections | CC BY-NC 4.0 | zenodo.org/records/16920313 | **TODAY** — DRR pretraining only |
| **RadGenome-Anatomy** | 25,692 studies, 10.79M masks | **synthetic PA + LL projections from CT-RATE**, 384² | 93 skeletal classes incl. ribs 1–12 L/R, T1–T12 | yes, at 30× PAXRay's scale — but not real radiographs | CC BY 4.0 | huggingface.co/datasets/EvidenceAIResearch/radgenome-anatomy | **TODAY** — the HF card's claim that these are real films is wrong; the method is a line integral with no scatter, grid or heel effect |
| **MIMIC-CXR (DICOM)** | 377,110 images | PA/AP/lateral | reports + labels | derivable; largest source of laterals at full bit depth | PhysioNet credentialed | physionet.org/content/mimic-cxr/2.1.0/ | **REQUEST** — prefer DICOM over the JPG release, which is windowed for parenchyma and loses the vertebrae |
| **BRAX** | 40,967 images, 8 view positions incl. oblique and decubitus | CXR DICOM | 14 labels from Portuguese reports | derivable; the obliques are a genuine robustness arm | PhysioNet credentialed | physionet.org/content/brax/1.1.0/ | **REQUEST** |
| **VinDr-CXR** | 18,000 DICOM | frontal | 22 local boxes, 3 readers each | derivable; the source pool for VinDr-RibCXR | PhysioNet credentialed | physionet.org/content/vindr-cxr/1.0.0/ | **REQUEST** |
| **JSRT** | 247, **12-bit, 2048², 0.175 mm** | PA | nodules | yes — the only classic set with enough latitude to window the thoracic spine | JSRT terms | jsrt.or.jp | **REQUEST** — db.jsrt.or.jp fails TLS today |
| **Whole-spine lateral, C2–L5 + pelvis (Taiwan)** | 2,210 films | whole-spine lateral | **45 landmarks incl. vertebral centres C2→L5 plus pelvic and femoral** | yes — exactly the spinopelvic geometry we compute on CT | PHI-restricted, on request | PMC8027006 | **REQUEST** |
| **SpineHRNet+ multicentre AIS** | **3,899 full-spine radiographs**, 7 hospitals | full-spine AP | Cobb + severity | derivable | not released | doi 10.2196/78396 | **REQUEST** — largest non-public full-spine series found |
| **UK Biobank DXA field 20158** | **94,678 participants** | GE iDXA: whole body, AP lumbar, **lateral thoraco-lumbar T4–L4**, hips | none per-vertebra | **the interesting case** — the lateral field is T4–L4, no C2 anchor and no sacrum, so counting down is impossible by construction, while the AP lumbar and whole-body scans from the same visit *do* carry a sacral anchor. Paired anchored and unanchored views of the same person | UKB MTA | biobank.ndph.ox.ac.uk/ukb/field.cgi?id=20158 | **REQUEST** |
| **CLSA IVA lateral spine** | ~30,000, 3 waves | DICOM 1248×402 with real mm spacing, no report overlay, "intended for vertebral morphometry" | none released | yes, same T4–L4 window | CLSA DAA + REB | clsa-elcv.ca/data-access | **REQUEST** — **$10,000 USD** non-Canadian, ~6 months |
| **NHANES 2013–14 VFA (`DXXVFA_H`)** | 3,330 scanned | Hologic IVA lateral thoraco-lumbar | **Genant grade + validity code for each of 13 named vertebrae T4–L4** | yes in the labels | US public domain (tabular) | wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2013/DataFiles/DXXVFA_H.htm | **scores TODAY, images NO** — worth one email to the NCHS RDC |
| **MrOS / SOF** | 5,994 men / ~9,700 women | lateral spine films, serial | SQ reads | yes if obtained | NIA / CPMC DUA | agingresearchbiobank.nia.nih.gov | **REQUEST** — tabular is self-serve, images are not; MrOS Online is currently offline |
| **VertebraeKeypoints50** | ~50 studies | plain X-ray sagittal | 4 endplate keypoints per vertebra, **C2–S1** on full-length | yes | ODbL (Kaggle field) | kaggle.com/datasets/c3ls1y/vertebraekeypoints50 | **TODAY**, tiny |
| **Roboflow `geisinger/vertebrae`** | 176–430 images | spine radiograph (modality not stated) | boxes, 26 classes **C2–C7, T1–T12, L1–L6, sacrum** | yes — **and it carries an L6 class** | CC BY 4.0 | universe.roboflow.com/geisinger/vertebrae | **TODAY**, source unverified |
| **AI Hub #611 (Korea)** | >1.39M images | X-ray + CT + MRI | JSON boxes with **named levels** | yes | Korean nationals, secure enclave | aihub.or.kr | **NO** |

**Radiograph negatives:** RSNA Pediatric Bone Age is hand-only; GRAZPEDWRI-DX is wrist-only;
no paediatric spine radiograph release with vertebral identity exists. CheXmask is lungs and
heart only. The SCR masks for JSRT are clavicles only and the host 404s. PhysioNet holds
exactly one spine project (VinDr-SpineXR). Grand Challenge holds exactly two spine challenges
(AASCE, VerSe) out of 264. No public EOS *image* release exists — the "AI EOS database"
(Zenodo 19690774) is 12 tabular spinopelvic parameters and no pixels. Several Kaggle and
HuggingFace uploads are relicensed re-uploads of sets we hold: `siddhale/…spinal-lesions`
(tagged MIT) and `Borel237/vindr-spinexr-npz` are VinDr-SpineXR (CC BY-NC-SA, credentialed);
`ddatad/cervical-x-ray` is CSXA; `parralex/lumbar-vertebrae-segmentation` says outright it is
BUU-LSPINE, though it adds custom per-vertebra masks that may be worth lifting.

## Three things to carry into the writing

**The field states this blind spot in print, three times independently.** SPIDER's *Scientific
Data* paper says its lowest lumbar label "should not be interpreted as an anatomical label as
this vertebra is not necessarily L5, due to possible anatomical variations and irregular
number of lumbar vertebrae", and that the anatomical-label head "was not used… since no
accurate anatomical labels regarding lumbosacral transitional vertebrae were present in our
dataset". The Sudirman Mendeley set annotates "the lowest three vertebrae". CSI 2014 uses
ordinal labels 100/200/300. Three large releases chose ordinal labels because anatomical ones
were not safely derivable, and none shipped the variant flag.

**Deduplicate before pooling anything, and note that the symptom of failing to would be a
plausible number.** CTSpine1K = 825 COLONOG + HNSCC-3DCT-RT + 201 MSD-Task03 + 40 COVID.
AbdomenCT-1K = LiTS + KiTS + MSD + NIH-Pancreas. FLARE23 = FLARE22 + TCIA + LiTS + MSD + KiTS
+ autoPET + TotalSegmentator + AbdomenCT-1K. SAROS samples 28 TCIA collections. **Our own
CTSpinoPelvic1K is COLONOG**, so CT Colonography is not new data to us — its untapped half is
the second (prone) acquisition, which CTSpine1K discarded by taking one series per patient.
Note also that HNSCC-3DCT-RT, a CTSpine1K source, has moved to NIH controlled access.

**NMDID's licence is the decision, not the application.** 15,243 head-to-toe decedent CTs at
1 mm is the best-fitting population in existence for this question, the application is a
paragraph and it is free. But the DUA reads "shall not duplicate, distribute, transfer,
transmit, copy, sell, exploit for commercial purposes, create derivative works from, or
otherwise make available the Database", with no third-party redistribution and a one-year
term. Read plainly that blocks releasing an NMDID-derived labelled subset the way
CTSpinoPelvic1K was released. Publishing findings is fine and expected. A derived release
needs a written carve-out first.
