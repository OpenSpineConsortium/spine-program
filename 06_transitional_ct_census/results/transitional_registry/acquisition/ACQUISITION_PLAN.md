# Acquisition plan for anomalous CT (2026-09-23; updated 2026-09-24)

Greg's worry was that any CT on the internet could be segmented, which makes the search feel endless. This plan
answers it with a rule. A CT is worth fetching only if it can produce a **count**. A count needs both junction
references in the field of view, so the question for any collection is how many new people it would add whose spine
can be counted, times how often such a spine is transitional, per terabyte. That turns the open-ended search into a
finite, ranked list with a stopping point. The top of the open list is already downloading, and each download is
chained to the two-labeller screen.

| | collections | new CTs (people, at most) | expected transitional people, E_low / E_high | what the mask screen can call without a reader (E_count) | TB |
|---|---:|---:|---:|---:|---:|
| **tier 1: open, fetching since 2026-09-23** | 45 routes + the NLST pilot | 15,233 | **831 / 1,703** | **460** | 1.45 |
| **tier 1, late: open, found and submitted 2026-09-24 (section 4b)** | 10 | 3,365 | **163 / 336** | **91** | 0.41 |
| tier 2: open, fetched once tier 1 has measured the priors | 17 | 30,486 | 153 / 456 | 144 | 3.06 |
| deferred (a route not yet written) or unresolved overlap (section 4b) | 7 | 3,536 | 187 / 387 (if every person were new) | 105 | 0.98 |
| gated: a form stands between us and the data (section 7) | 7 | 70,764 | 1,791 / 3,848 | 1,066 | n/a |
| below the stopping threshold, excluded, or no new countable people | 59 | | 4 | | |

For scale, `SchwingNet/results/rare_class/transitional_subtypes.md` currently holds about 190 distinct
transitional patients across all sources: L6 110, T13 7, Castellvi I-II 31, lumbar rib 14, sacralised L5 28. Tier 1
could add about 550 people with a count anomaly (L6, four lumbar, T13): 460 from the first launch and 91 from the late
additions. These are **expected values** from cited prevalences and measured field-of-view rates. They are not calls.
Section 9 lists what could make them wrong. **One of them already has:** only 723 of AMOS's 2,364 CTs are 3 mm or
thinner. The first census assumed every AMOS CT was thin, so AMOS will yield about a third of its predicted people
(section 9). **And a second:** the NLST pilot's 9.3 % T13 rate was five to fifteen times its prior and was wrong; the
check that caught it and the rule it forced are in section 11. Section 10 states what Greg's acquisition-space
review of 2026-09-24 changes in this plan, and what it does not.

Files here:

- `ranking.csv`: every collection, one row each, with all the columns below. The `added` column marks the 2026-09-24
  rows.
- `census.json`: every parameter, prior and per-class P.
- `census_addendum.json`: the header measurements behind the 2026-09-24 rows.
- `fov_calibration.json`: the measurement behind P.
- `manifests/`: the series the tier-1 fetch jobs read.
- `sweep/zenodo_ge5GB_ct.tsv`: the Zenodo sweep of 2026-09-24.
- `validation_cases.csv`: the outside check on the screen.
- `REVIEW_RUN.md`: the scoping review's run.
- `collections/<name>/`: each finished collection's `SUMMARY.md`, `rows.csv/json` and `registry_rows.csv/json` in the
  shared schema, copied from the grid. So far these are csi2014 and ctpelvic1k_clinic; the rest land as their chains
  finish.
- `jobs.txt`: every job submitted.
- `t13_check/`: the outside check of VERIDAH's T13 on the NLST pilot and on the 70 outside-labelled CTs (section 11).

---

## 1. The criterion: five tests that shrink "the internet" to a list

A CT enters the ranking only if all five hold:

1. **Coverage can hold a count.** The lumbosacral question (L6, sacralised L5, four lumbar) needs the last
   rib-bearing vertebra **and** the sacrum in the field. The T13 question needs the rib cage counted from T1, which
   means a rib-free C7 above the first rib-bearing body. A cut field means no count, never "normal".
2. **Slices ≤ 3 mm.** This is measured from the slice positions at conversion, not read from a tag.
3. **The licence allows derived labels.** CC BY, BY-SA, BY-NC and BY-NC-SA qualify. ND does not
   (`licence_tiers.csv`: re-annotation is a derivative use), and neither does a DUA that forbids derivative works.
   This excluded NMDID (15,243 whole-body post-mortem CTs) and Glocker's spine CT (CC BY-NC-ND).
4. **The source names a person,** so duplicates can be removed and patient keys can be formed.
5. **A catalogue lists what the source holds.** That lets the fetch be verified against it: a DICOM series must
   match the catalogue's instance count, and an archive must match the repository's md5 or sha256.

These five tests rule out most of what the internet holds. Radiopaedia-derived sets (M3D, RadGenome) are resampled
8-bit stacks with no HU and no person key. DeepLesion and ULS23 are key-slice crops. BLSA and Health ABC are single
slices. OAI, UK Biobank and NAKO have no CT. `tools/CT_MINE_REPORT.md` Part 1 lists the verified negatives.
What remains is a set of catalogues, and those were read exhaustively rather than crawled:

- **NCI Imaging Data Commons v24.** It mirrors every open TCIA collection plus NLST and CPTAC. `idc-index` reads
  every CT series in it, 266,232 series in 98 collections, with BodyPartExamined, SliceThickness, image type,
  geometry, licence and size. `tools/acquisition_census.py` applies tests 1–5 to each series and keeps one series
  per patient: the widest coverage, then the thickness closest to 1.25 mm.
- **TCIA outside IDC** (FDG-PET-CT-Lesions / autoPET), through the NBIA REST catalogue.
- **HuggingFace, Zenodo and AWS Open Data,** through their APIs. AbdomenAtlas 3.0 Mini's metadata gives the spacing
  and shape of every one of its 9,262 CTs.
- **The aggregators,** each checked against its own source list: CADS (its HF tree has 40 source folders),
  AbdomenAtlas 1.1 (arXiv 2407.16697, Table 1), CTSpine1K (its HF tree) and CTPelvic1K (its Zenodo record).
  PanTSMini was added on 2026-09-24, checked against its `metadata.xlsx`.
- **Zenodo, swept by size (2026-09-24).** Every open record of at least 5 GB with a CT term that 29 body-region
  queries return. Each human CT collection was measured from its archives' headers before anything was downloaded
  (section 4b).

## 2. Expected transitional people: formula, priors and the measured term

    E = Σ over new people [ P(both LS references | coverage) × p_LSTV  +  P(cage from T1 | coverage) × p_T13 ]

**Prevalence priors** (all cited in `tools/acquisition_census.py`; the full references are in
`SchwingNet/LEVELCHECK_CLAIM.md` and `tools/CT_MINE_REPORT.md`):

| prior | value | source |
|---|---:|---|
| p_LSTV, low | 0.09 | Castellvi II–IV = 32 % of the 29 % LSTV in 3,855 consecutive abdominal CTs (Hanhivaara 2020, Eur Radiol 30:3409). Type I does not change a count. |
| p_LSTV, high | 0.18 | Nardo 2012, Radiology 265:497 (18.1 % of 4,636 films). Nagata 2025, Skeletal Radiol 54:2169 (16.3 % on whole-spine CT, n = 551) falls inside the band. |
| p_count (E_count) | 0.048 | What a mask count can see with no reader: L6 3.2 % + four lumbar 1.6 % in 500 unselected UK Biobank controls (Sun 2025, Commun Biol 8:1614). |
| p_T13, low | 0.0064 | 7 of 1,088 TotalSegmentator scans marked T13 in fhofmann/VertebralBodiesCT-Labels `data.csv`. |
| p_T13, high | 0.020 | L1 ribs 2.0 % (Sun 2025). A rib on the first lumbar-type body is a 13-rib-bearing count. |

E_count is the number to plan the screen around. The 9–18 % band includes Castellvi II articulations on
five-lumbar spines, and the screen reports those as "no call" until someone reads them.

**P(countable) is measured, not assumed** (`tools/acquisition_calibrate_fov.py`, job 40425064,
`fov_calibration.json`). It was measured on the mask field-of-view flags of the 2026-09-15 CT mine, using
TotalSegmentator v2's own stated `study_type` (1,228 CTs) and CTSpinoPelvic1K (802 colonography CTs). "Both" means
sacrum + a 12th rib + T12 or L1 labelled. "Cage" means 1st rib + 12th rib labelled.

| coverage class | TotalSegmentator study types pooled | n | P(both LS refs) | P(cage from T1) |
|---|---|---:|---:|---:|
| WB | whole body, polytrauma, neck-thorax-abdomen-pelvis, angio neck-to-leg | 218 | 0.665 | 0.707 |
| CAP | thorax-abdomen-pelvis (+ angio) | 160 | 0.794 | 0.787 |
| AP | abdomen-pelvis (+ angio) | 114 | 0.763 | 0.018 |
| ABD | abdomen | 60 | 0.800 | 0.000 |
| CA | thorax-abdomen | 54 | 0.519 | 0.463 |
| CHEST | thorax, thorax-chest, thorax-neck, angio thorax, chest | 151 | 0.053 | 0.696 |
| CHEST_SCREEN | lung screening / COVID / rib fracture / CTPA: 0 by protocol (caudal limit at the adrenals) | 151 | **0 (stated)** | 0.696 |
| PELVIS | pelvis, angio pelvis-leg | 76 | 0.118 | 0.000 |
| SPINE | spine | 41 | 0.293 | 0.293 |
| colonography (CTSP) | measured separately | 802 | 0.984 | 0.000 |

By craniocaudal extent (TotalSegmentator), P(both) is ≤ 0.07 below 350 mm, 0.34 at 350–400 mm, 0.64 at
400–450 mm and 0.84–0.94 at 450–800 mm. AbdomenAtlas's per-CT P uses those extent bins. IDC series use the class P
of their DICOM BodyPartExamined and descriptions. Two collections take a collection-level class because their
header says less than their description: PSMA-PET-CT-Lesions → WB, Pediatric-CT-SEG → CAP.

## 3. Stopping rule (stated before any fetch; constants in `tools/acquisition_census.py`)

1. **Yield per TB.** Open collections are fetched in descending order of E_low per TB. No collection is added below
   **20 expected transitional people per TB** (one per 50 GB).
2. **Space.** No fetch starts a unit while the oschome group quota has less than **5 TB** free.
   `tools/acquisition_fetch.py` reads `df-ceph oschome` before every unit, because statvfs reports the whole Ceph
   pool (6,318 TB), not our quota. The quota was 20 TB with 1.25 TB used at launch. This plan also caps itself at
   **8 TB** of the volume, because other workflows share it.
3. **Measure, then commit.** Tier 2 (2.9 TB, mostly NLST) starts only after tier 1's screen has replaced the priors
   with measured rates: P(count) per coverage class and calls per subtype. The 500-person NLST pilot in tier 1
   exists to measure the cage-from-T1 rate and the T13 rate on screening chest CT before 2.3 TB is committed. If a
   collection's measured yield falls under half its predicted yield, it is re-ranked. The fetch is per unit and
   resumable, so stopping one mid-way loses nothing.
4. **GPU.** Nothing beyond tier 1 is added while more than 5,000 fetched CTs are still unscreened. Tier 1 itself,
   about 15,000 CTs, was launched at once, because its fetches finish long before the GPU screen does. The validation
   timings are about 1.5 GPU-min per CT for TotalSegmentator and 3–5 GPU-min per gated CT for SPINEPS.

Tier 1 is every open row with E_low/TB ≥ 100. Tier 2 is 20–100. Both fit inside the 8 TB cap (4.9 TB together
after the additions of 2026-09-24).

**Applied on 2026-09-24.**

- **Rule 1.** Ten collections found that day clear the tier-1 bar on header-measured coverage. They were submitted
  (section 4b).
- **Rule 2.** At submission the quota showed 3 TB used of 20.
- **Rule 3, AMOS.** AMOS measured under half its prediction (section 9). It is already fully fetched, so it is
  reported rather than re-ranked.
- **Rule 4.** More than 5,000 fetched CTs are still unscreened. Tier 2 therefore stays unsubmitted, and so does
  everything deferred. The late tier-1 chains run at the lowest priority (`nice 200`), because the paper's Figure 6
  training has the longest GPU time.

## 4. The ranking (top of `ranking.csv`; E per TB orders the open list, E_low orders the gated one)

Ranks are those of the merged ranking of 2026-09-24. The 2026-09-24 rows (section 4b) were ranked by the same rule,
so some of the first launch's ranks moved down.

| rank | tier | collection | route | licence | new people | coverage | E_low | E_high | E_count | GB | E_low/TB |
|---:|---|---|---|---|---:|---|---:|---:|---:|---:|---:|
| 1 | 1 | AMOS22 unlabelled CT (ids 5000–6899) | Zenodo 7262757, 7295661 | CC BY 4.0 | 1,900 | abdomen | 136.8 | 273.6 | 73.0 | 78 | 1,787 |
| 7 | 1 | AMOS22 labelled CT (300 not already in AbdomenAtlas) | Zenodo 7262581 | CC BY 4.0 | 300 | abdomen | 21.6 | 43.2 | 11.5 | 24 | 914 |
| 9 | 1 | AbdomenAtlas 3.0 Mini (= AbdomenAtlas 1.1 images) | HF, ungated | CC BY-NC-SA 4.0 | 7,835 (≤ 3 mm) | per-CT extent | 425.2 | 871.7 | 235.6 | 571 | 763 |
| 15 | 1 | EAY131 (NCI-MATCH) | IDC | CC BY 4.0 | 376 | CAP/abdomen/chest | 21.3 | 43.8 | 11.9 | 36 | 599 |
| 24 | 1 | Pediatric-CT-SEG | IDC | CC BY 4.0 | 352 | CAP | 26.9 | 55.8 | 15.2 | 56 | 495 |
| 32 | 1 | PSMA-PET-CT-Lesions (autoPET III) | IDC | CC BY 4.0 | 374 | whole body | 24.1 | 50.1 | 13.6 | 62 | 400 |
| 55 | 1 | FDG-PET-CT-Lesions (autoPET) | TCIA NBIA | CC BY 4.0 | 900 | whole body | 57.9 | 120.5 | 32.8 | 251 | 237 |
| 2–74 | 1 | 36 more IDC collections (TCGA-\*, CPTAC-\*, CMB-\*, HCC-TACE-Seg, Colorectal-Liver-Metastases, COVID-19-NY-SBU, Lung-PET-CT-Dx, ...) | IDC | CC BY / BY-NC | 2,498 | mixed | 112.1 | 232.2 | 62.7 | 310 | 112–1,557 |
| 62, 68 | 1 | CSI 2014 spine CT; CTPelvic1K clinical sets 6–7 | Zenodo | ODC-By; CC BY 4.0 | 198 | spine; pelvis | 2.5 | 5.0 | 1.3 | 18 | 131–171 |
| pilot | 1 | NLST, a seeded 500-person pilot | IDC | CC BY 4.0 | 500 | chest | 2.2 | 7.0 | 2.2 | 46 | 49 |
| 10–69 | 1, late | ten collections found 2026-09-24 (section 4b) | Zenodo | CC BY / BY-NC / BY-NC-SA / CC0 | 3,365 | header-measured | 163.3 | 335.5 | 90.7 | 424 | 126–756 |
| 75–92 | 2 | NLST (24,713), LIDC-IDRI (997), STOIC2021 (2,000), RibFrac (660), Spine-Mets-CT-SEG, Spinal-Multiple-Myeloma-SEG, NSCLC sets, VSDFullBody, MedPelvis3D, LumVBCanSeg, UniToChest, ... | IDC / AWS / Zenodo | CC BY / BY-NC | 30,486 | mostly chest (T13 only) | 153.3 | 456.3 | 143.8 | 3,133 | 34–95 |
| 139 | gated | Merlin abdominal CT (18,317 patients / 25,494 CT) | Stanford AIMI | AIMI research-use DUA | 18,317 | abdomen-pelvis | **1,259.9** | 2,522.3 | 673.0 | n/a | |
| 140 | gated | RSNA RATIC abdominal trauma (3,147 patients / 4,711 series) | RSNA MIRA / Kaggle | non-commercial, no redistribution | 3,147 | CAP | 240.7 | 499.3 | 135.8 | n/a | |
| 141 | gated | CT-RATE (21,304 patients) | HF gated form | CC BY-NC-SA 4.0 | 21,304 | chest | 94.9 | 296.6 | 94.9 | n/a | |
| 142 | gated | INSPECT CTPA (~19,400 patients) | Stanford AIMI | AIMI research-use DUA | 19,402 | chest | 86.4 | 270.1 | 86.4 | n/a | |
| 143 | gated | CADS parts reachable nowhere else (CT-TRI 586, VISCERAL 167) | HF gated checkbox | per component | 753 | whole body | 48.5 | 100.8 | 27.4 | 123 | 403 |
| 144 | gated | RSNA-STR Pulmonary Embolism CT, RSPECT (7,279 studies) | Kaggle / RSNA | RSNA terms, non-commercial | 7,279 | chest (CTPA) | 32.4 | 101.3 | 32.4 | n/a | |
| 145 | gated | MAGIC-CT (562 patients, tumour CT, NRRD) | Zenodo, with a data-use agreement | CC0 label + DUA | 562 | chest-abdomen (unmeasured) | 27.9 | 57.7 | 15.7 | 39 | |

The IDC census also refused series, and those refusals are in `ranking.csv` `refused_series`. StageII-Colorectal-CT
fails on thickness (all 230 series are 5 mm). CT-Lymph-Nodes has no SliceThickness. Most of EAY131 is refused: of
13,166 series, 3,754 are over 3 mm, 2,790 are not regular volumes, and 1,249 have fewer than 60 slices.

## 4b. Collections found on 2026-09-24, and how they were measured before any download

The first census read IDC exhaustively and the aggregators by their own source lists. It did not sweep the general
repositories. The scoping review cannot fill that gap: its frozen scope is spine datasets (REVIEW_RUN.md section 4).
So on 2026-09-24 three further passes were made:

- **A Zenodo sweep.** Twenty-nine body-region × CT queries against the Zenodo API, keeping open records of at least
  5 GB with a CT term: 157 records (`sweep/zenodo_ge5GB_ct.tsv`, mostly micro-CT and non-human).
- **A Hugging Face search** for AMOS, PANORAMA, PanTS, AbdomenAtlas, BodyMaps, FLARE, CT-RATE, Merlin and RSPECT, and
  for abdominal, pelvic and whole-body CT.
- **The review's own records.** A keyword pass over them (REVIEW_RUN.md section 4) added ENHANCE.PET 1.6k and LUMOS.

Each human CT collection was triaged from its record and from its archives' **central directories, read through HTTP
range requests, with nothing downloaded**:

- **People.** Member names give the patient ids. PANORAMA, for example, has 2,238 volumes and 2,224 distinct patients.
- **Coverage.** For the collections that were fetched, a seeded sample of image headers was read (NIfTI-1 or MHA,
  10–40 per archive). The headers give slice spacing and craniocaudal extent. The same TotalSegmentator extent-bin
  rates the census used for AbdomenAtlas then give P per CT, with the ≤ 3 mm fraction folded in
  (`census_addendum.json`).
- **Anatomy overrides the bin.** Where the field cannot hold T1 (a lumbar-only or pelvic series), P(cage) is 0 rather
  than the extent bin's rate, which comes from chest CTs of the same length.

The rows were merged into `ranking.csv` by `tools/acquisition_census_addendum.py`. It applies the census's own order
and stopping rule and does not re-query IDC or touch the manifests under running jobs. The first launch's tiers are
unchanged.

**Tier 1, late: submitted 2026-09-24** (`acquisition_submit.sh tier1_late`; `jobs.txt`):

| collection | route, licence | people | ≤ 3 mm | median extent | P(both) / P(cage) per CT | E_low / E_high | E_count | GB | E_low/TB |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|
| PANORAMA (Radboudumc + UMCG pancreatic CECT) | Zenodo ×4, CC BY-NC 4.0 | 1,950 of 2,224 | 89 % | 445 mm | 0.505 / 0.311 (160 headers) | 92.5 / 189.4 | 51.1 | 194 | 488 |
| Kidney abnormality, thorax-abdomen CT (institution not stated) | Zenodo, CC BY 4.0 | 215 | 100 % | 657 mm | 0.926 / 0.882 | 19.1 / 39.6 | 10.8 | 38 | 510 |
| Barts CRL (CRC staging CT, London) | Zenodo, CC BY 4.0 | 220 | 100 % | 457 mm | 0.732 / 0.386 | 15.0 / 30.7 | 8.3 | 20 | 756 |
| CURVAS 2024 | Zenodo, CC BY 4.0 | 90 | 100 % | 932 mm | 0.895 / 0.822 | 7.7 / 16.0 | 4.3 | 29 | 268 |
| CURVAS-PDACVI | Zenodo, CC BY 4.0 | 109 | 93 % | 471 mm | 0.683 / 0.409 | 7.0 / 14.3 | 3.9 | 15 | 465 |
| WAW-TACE (HCC multiphase, Warsaw) | Zenodo, CC BY 4.0 | 233 | 96 % | 285 mm | 0.271 / 0.240 (phase-mixed; a floor) | 6.0 / 12.5 | 3.4 | 47 | 130 |
| AortaSeg-60 (CTA aorta) | Zenodo, CC0 | 60 | 100 % | 661 mm | 0.935 / 0.925 | 5.4 / 11.2 | 3.0 | 16 | 348 |
| QUADRA_HC (total-body PET/CT, healthy) | Zenodo, CC BY 4.0 | 48 | 100 % | 1,062 mm | 0.889 / 0.806 | 4.1 / 8.5 | 2.3 | 20 | 208 |
| DEEP-PSMA (PSMA + FDG PET/CT) | Zenodo, CC BY-NC 4.0 | 100 | 48 % | 1,095 mm | 0.427 / 0.387 (per CT; a floor) | 4.1 / 8.5 | 2.3 | 24 | 174 |
| PENGWIN 2026 (peripelvic fracture CT) | Zenodo, CC BY-NC-SA 4.0 | 340 | 100 % | 252 mm | 0.078 / 0 (pelvic) | 2.4 / 4.8 | 1.3 | 20 | 126 |

What the late rows change in the chain:

- **One CT per person.** `acquisition_screen.py cases --one-per-person` keeps the widest usable field per patient
  key. This matters for the multiphase, test-retest and two-tracer releases (WAW-TACE has 854 phases for 233 people).
  The others are recorded as refusals naming the case kept.
- **Deflate64.** The fetcher now unpacks archives that Python's zipfile cannot read (CURVAS `training_set.zip`, 20 CTs)
  with unzip, then 7z, checking every CRC. The first attempt used the grid's p7zip, which failed with "Headers Error"
  after the md5 had verified. The fetcher now tries each tool in turn and keeps the verified download. A repair
  chain (`tier1_late 40430934 curvas`) runs after the first pass; if every tool fails again, those 20 CTs stay a
  recorded failed unit.
- **Priority.** Every late job runs at `nice 200`, below the paper's GPU work.
- **Dedupe.** `acq_dedupe2` (40430971, repeated as 40436046 after the CURVAS repair) compares every acquired
  collection, the late ones included, by pixel hash and thumbnail. It is expected to find PANORAMA's 274 MSD and NIH Pancreas-CT cases among AbdomenAtlas, and any overlap
  between the two CURVAS editions.

**Deferred or unresolved: open and ranked, not fetched.**

- **ENHANCE.PET 1.6k.**
  - What it is: 1,683 whole- or total-body FDG-PET/CT studies from Vienna, UC Davis, Careggi, Leipzig and Tübingen,
    CC BY 4.0, 286 GB, on Science Data Bank. The review's DataCite search found it.
  - Yield: E_low ≤ 108, or 387 per TB if every CT is ≤ 3 mm, which its `CT-details.xlsx` would settle.
  - Why not fetched: the Science Data Bank download route is not scripted, and whether it needs a login is
    unconfirmed. The Tübingen part may be autoPET and the Vienna healthy controls may be QUADRA_HC.
  - **This is the largest open addition still pending.**
- **TMTV benchmark (60) and LUMOS (280 lumbar CT).** Both are DICOM series inside zips, which need a convert route
  that does not exist yet. TMTV's NIfTI copies are resampled to the PET grid.
- **TotalSegmentator task data.** `liver_lesions` (842 CT, E_low 60.6 if the people were new, 1,597 per TB),
  `pleural_pericard_effusion` (600) and `hip_implant` (71).
  - The problem: they come from the same institution as TotalSegmentator v2/v3, which is on disk, and their case
    names are random hashes. A pixel match would catch a re-released scan, but not the same person scanned twice.
  - What would settle it: ask the TotalSegmentator authors whether the task-data subjects overlap the public release.
    That is a question for Greg to send.
- **AbdomenAtlas 2.0 Mini (10,135 CT, 620 GB).** It has no card and no metadata. The line it belongs to aggregates the
  public sets already fetched as AbdomenAtlas 3.0 Mini (9,262), so it is not fetched until an id map exists.

**Resolved as no new people or excluded:**

- **PanTSMini (9,901 volumes).** An aggregator by its own `metadata.xlsx`:

  | source inside PanTSMini | volumes |
  |---|---:|
  | CT Colonography (= CTSpinoPelvic1K people) | 2,810 |
  | TotalSegmentator | 1,229 |
  | autoPET | 894 |
  | KiTS | 665 |
  | AMOS | 200 |
  | Warsaw (= WAW-TACE, fetched directly) | 293 |
  | other named public sources (MSKCC 966, Gong'an 484, MSD 411, IRCAD 173, ...) | 3,116 |
  | no site | 694 |

  Fetching it would have re-admitted CTSP people under new keys.
- **Excluded by licence (ND):** CancerVerse, and LNDb (its own text says ND).
- **Derived from sets already counted:** the AUC23 re-packs of STOIC and RibFrac, the curated AbdomenCT-1K pancreas
  sets, TAVRP-PL (TotalSegmentator), a merged multi-organ set, and SynthRAD2025 (fields cropped to the paired MR or
  CBCT).
- **Tier 2 by the stopping rule:** VSDFullBody (post-mortem whole body, 56 per TB), MedPelvis3D, LumVBCanSeg,
  UniToChest.

## 5. Deduplication: which collections contain which (counted once, where the widest open route carries them)

- **CT Colonography (TCIA, 825 patients).** 802 of them are CTSpinoPelvic1K people (the manifest token is the tail
  of the DICOM PatientID; PATIENT_IDENTITY_SPEC). The remainder, about 23 people, is **held back**: it will not be
  fetched until the CTSP tokens are matched to IDC PatientIDs and all 802 match. A partial match would re-admit
  CTSP people under a new key.
- **CTSpine1K.** Its COLONOG 784 are CTSP people, and their vertebra masks could serve as a second labeller for
  CTSP. MSD-T10 150 are inside AbdomenAtlas (MSD-CT). HNSCC 31 are neck fields, which cannot be counted. That leaves
  40 new chest CTs, E_low 0.2, below threshold. CTPelvic1K datasets 1–5 are BTCV, COLONOG, MSD-T10, KiTS19 and
  cervix: CTSP or AbdomenAtlas people. Only its clinical sets 6–7 are new.
- **AbdomenAtlas 1.1 / 3.0 Mini (9,262)** carries LiTS, KiTS, AbdomenCT-1K, FLARE'23, Pancreas-CT, CT-ORG, CHAOS,
  MSD-CT, BTCV, AMOS22 (200) and WORD (120) (arXiv 2407.16697 Table 1). Those routes, and IDC's C4KC-KiTS and
  Pancreas-CT, are counted there and not again. Its Table 1 also lists the RSNA trauma set. Whether any trauma
  series are among the public 9,262 has not been published.
- **CADS** is 38 public sources plus two new ones. 33 of its folders are sources listed separately here.
  TotalSegmentator and VerSe are already on disk. NLST, LIDC, TCGA and CPTAC come through IDC, and AMOS, RibFrac and
  AbdomenCT-1K through their own routes. Only CT-TRI 586 and VISCERAL 167 are unique, and both sit behind the gate.
- **SAROS** is a subset of TCIA collections, so it adds no people.
- **At landing**, every converted CT carries a pixel sha1 and a 16³ canonical thumbnail.
  `tools/acquisition_dedupe.py` (job 40426214, after every tier-1 case merge) reports exact duplicates and
  thumbnail NCC ≥ 0.98 pairs within 5 mm of extent, across all acquired collections. The pairs are reported for the
  alias classes in docs/DATA_ACCOUNTING.md §3, not merged silently. Known overlaps to expect include AMOS labelled
  vs AbdomenAtlas, and MSD lung vs the NSCLC collections if tier 2 lands.
- **Patient keys.** `tools/patient_keys.key_any` is tried first. It has no scheme for these corpora yet, so each
  key is `<corpus>:<source subject id>` (the IDC/NBIA DICOM PatientID, the AMOS id, or the AbdomenAtlas BDMAP id),
  and the rule is recorded per case. **AbdomenAtlas BDMAP ids are volumes, not people.** FLARE and KiTS can hold two
  scans of one person, and that has not been established either way.

## 6. What was started, and how each piece is verified

Code (grid clone, shipped by scp): `tools/acquisition_{census,calibrate_fov,fetch,screen,validate,validation_cases,dedupe}.py`
and `slurm/acquisition_{env,fetch,cpu,ts,spineps,validation_prep,submit,fetch_smoke}.sh`. Data land under
`/rs/rs_grp_oschome/go2432/data/<collection>/`. Screen outputs go to `/rs/.../data/anomaly_harvest/<collection>/`.

**Fetch.** Each route was smoke-tested on one unit first (job 40425969: IDC 2/2 series, NBIA 1/1, Zenodo md5 1/1,
HF sha256 1/1). Every chain is resumable: a verified unit is skipped, and IDC uses `s5cmd sync`. A requeue or rerun
of the same command continues where it stopped.

**Screen, per collection:** convert → cases → TotalSegmentator (GPU) → gate → SPINEPS (GPU) → call → summary,
chained with afterany. Each stage checks its own inputs and skips finished work, so a parent that failed for a
trivial reason does not strand the chain.

- **Convert.** Slice spacing is measured from ImagePositionPatient. Non-uniform or > 3 mm spacing is refused.
  Geometry is carried into the NIfTI and read back, and the volume is never reoriented on write.
- **Labeller B (TotalSegmentator 2.18, read geometrically, names unused).** Its vertebral levels are the intervals
  between the intervertebral discs of the `vertebrae_body` task (version b5). Body components are only a
  cross-check, because they merged neighbours wherever a disc was thin, into components of 80–225 ml.
  - **Discs inside the sacrum.** A disc is inside the sacrum when sacrum fills the 12 mm cylinder on the axis just
    above it. The lumbosacral disc must have sacrum directly below it. A z-threshold on the sacrum's top failed here,
    because the promontory rises above the L5/S1 disc.
  - **Rib-bearing levels.** A level is rib-bearing when a rib head falls nearest its centre. The head is the medial
    5 % of a rib component, within 70 mm of the axis.
  - **Refusals.** B refuses the count when a rib is cut by the S-I face at or below the lowest whole rib-bearing
    level (the CTSP stream's finding on release 1106), when the lowest rib-bearing level carries only ribs under
    40 mm (hypoplastic 12th rib or lumbar rib), or when a disc spacing is over 1.6× the median in the counted
    interval.
  - **T13.** A T13 needs a rib-free level with a body above the first rib, and the level count must equal a
    per-side rib count.
  - **Tuning on the outside labels.** Labeller B was tuned in four passes against the 70 outside-labelled cases
    (section 6, the outside check), and each pass fixed one measured defect. Pass 5 on the 70 TotalSegmentator
    cases:
    - L6: 17 of the 19 external-L6 spines that B counted are called L6. The other 2 are called ordinary, and 9 more
      are refused.
    - Negatives: B counted 28 of the external negatives and called 24 of them ordinary. The other 4 are wrong:
      3 four-lumbar and 1 L6.
    - T13: B called none of the 7 external T13. Five had no rib-free level above the first rib in the field, and
      one had 13 levels against 12 ribs per side. **B alone is not a T13 detector at this cut; T13 calls rest on
      whole-body fields and on labeller A.**
  - **Tuning is not testing.** These numbers come from the tuning set itself, not from held-out cases, so read them
    as an upper bound. The combined two-labeller score is `anomaly_harvest/validation_ts/VALIDATION.md`.
- **Gate.** SPINEPS runs only where the sacrum and ribs, or a rib cage, are in the field. A cut field is no count.
- **Labeller A (SPINEPS + VERIDAH).** Names come from the ctd POI json through `tools/spineps_ids.read_ctd`, the
  mask must pass `assert_verse_monotonic` (the one guard), and the ctd names must run cranio-caudally. A skipped
  T12 at normal spacing is read as VERIDAH's 11-thoracic call. **No mask id is ever read as a level.**
- **Call.** Each junction is compared separately. When both labellers count and agree, the call is two-labeller.
  When one counts and the other cannot, it is single-labeller. When both count and disagree, the case goes to the
  review queue with a sagittal slab and coronal MIP carrying both labellings (`review/<case>.png`) for Greg to
  adjudicate. Four lumbar and 11 rib-bearing are `unassigned` with the modifier set: sacralised_L5_fused needs a
  Castellvi read.
- **Rows.** Each collection writes `rows.csv/json` (every CT) and `registry_rows.csv/json` (transitional only) in
  the shared schema. `SUMMARY.md` gives the denominators: units verified, CTs converted, CTs gated, CTs called,
  CTs with an LS count, CTs with a count from T1, calls per subtype and tier, and refusals by reason.
  `real_frames` is False for every acquired source. None of these people has a real projection, so all of them
  can feed renders.

**The outside check was run before trusting the screen** (jobs 40425899–40425908, rescored as 40428080; the
reports are copied to `validation/`). The full screen ran on 70 TotalSegmentator v2 CTs: all 35
VertebralBodiesCT-Labels positives (28 L6, 7 T13) and 35 seeded negatives. That table was read by its own authors,
not by SPINEPS or TotalSegmentator. It counts only a *free* sixth lumbar as lumbar. TotalSegmentator trained on these
CTs, so labeller B's score is optimistic.

| labeller | external L6 called L6 | external T13 called T13 | negatives read ordinary | false L6 / false T13 on negatives | no LS count on negatives |
|---|---|---|---|---|---|
| A: SPINEPS + VERIDAH, ctd names | 12 / 28 (10 read ordinary, 6 no count) | 5 / 7 | 30 / 35 | 2 / 0 (rescored 2026-09-24 under the T13 rib rule of section 11; 2 / 1 before it) | 2 |
| B: TotalSegmentator geometry | 17 / 28 (2 read ordinary, 9 no count) | 0 / 7 | 24 / 35 | 1 / 0 | 7 |

The combined call, which is what reaches the registry:

- **The 28 external L6.** 9 are two-labeller L6 and 2 are single-labeller L6. 9 went to the review queue and 5 had no
  count. 1 was called ordinary by one labeller. The last 2 were called **T13 by VERIDAH alone**. That is the naming
  question the count cannot settle without ribs: 13 thoracic + 5 lumbar against 12 + 6.
- **The 7 external T13.** 5 are single-labeller T13 (from A). 2 were read ordinary by both labellers, which is a
  shared miss.
- **The 35 negatives.** 28 are ordinary (21 two-labeller), 5 went to review, 1 had no count, and 1 is two-labeller
  L6 (vts_s0049).
- **vts_s0049 was rendered** (`validation/vts_s0049.png`). Both labellers find six rib-free bodies between the 12th
  rib-bearing vertebra and the sacrum, and so does the eye, with the lowest body's transverse processes at the
  iliac crests. The external table counts a fused sixth as sacrum. This fits the definition difference its caveat
  names, but no reader has settled whether it is a screen error.
- **What the registry gets from this.** Of the calls that reach the registry automatically, two-labeller L6 is right
  on 9 of 10 (the 10th is s0049), single-labeller L6 on 2 of 2, and single-labeller T13 on 5 of 7 (the other 2 are
  L6/T13 naming swaps). The automatic registry recovers 11 of the 28 external L6. Adjudicating the review queue
  could raise that to 20 of 28.
- **The review load** is 14 of 70 CTs on this enriched set. It should be lower on unselected CT, but it is the price
  of two labellers, and it is Greg's queue (`review/<case>.png`: sagittal slab with B's discs and levels counted up
  from the sacrum, coronal MIP with the ribs, VERIDAH's names beside both).
- **A T13 call from labeller B alone never happens at this cut.** B's T13 needs a rib-free level above the first rib
  and a per-side rib count that agrees. In whole-body fields a mid-thoracic rib head that lands on the neighbouring
  level breaks the second test (`validation/vts_s0616.png`). T13 therefore rests on VERIDAH, at single-labeller tier,
  until that test is revisited.

Every job id is in `jobs.txt`. To resume or extend, run `bash ~/spinesurg-ct-nnunet/slurm/acquisition_submit.sh`
with an argument:

- `tier1` or `tier1_late`: skips whatever is already done.
- `dedupe <cases jobs>`: the landing dedupe over every collection.
- `tier2`: waits for section 3's measurement.

**Changes of 2026-09-24:**

- `--one-per-person` in `cases`.
- The Deflate64 unpack in the fetcher.
- `NICE`/`CASES` in the submit script, and its `tier1_late` and `dedupe` targets.

All of them are backward compatible, so the running chains are unaffected (the grid copy was checked by md5).

**State on 2026-09-24 at about 07:10 EDT** (`jobs.txt`). Every tier-1 chain of 2026-09-23 is alive, and none needed
resubmitting.

- **Finished fetches:** IDC, AbdomenAtlas, AMOS, NLST pilot, CSI and CTPelvic1K.
- **FDG-PET-CT-Lesions:** 550 of 900 series.
- **Screened:** CSI 2014 and CTPelvic1K have finished.
  - CSI: 20 CTs, 19 with a lumbosacral count, 17 ordinary, 2 four-lumbar or 11-rib `unassigned`, no transitional
    call.
  - CTPelvic1K clinical: 171 of 172 no count. Pelvic fields, as its P = 0.118 predicted.
- **In progress:** IDC TotalSegmentator is 2,883 of 3,499 done. AbdomenAtlas TotalSegmentator is running, and SPINEPS
  is running on AMOS and the NLST pilot.

## 7. Gated collections: the exact form each needs (none signed, none registered)

| collection | E_low (E_count) | where | what it asks for |
|---|---:|---|---|
| **Merlin abdominal CT** (Stanford ED 2012–18, 18,317 patients) | **1,260 (673)** | stanfordaimi.azurewebsites.net/datasets/60b9c7ff-877b-48ce-96c3-0194c8205c40 (also stanford.redivis.com/datasets/exfv-e8h3kvfhs) | Sign in to the AIMI portal, then accept the Stanford AIMI non-commercial research-use data-use agreement on the download page. After approval a time-limited Azure Blob URL is issued (AzCopy). Patient-level longitudinal ids for deduplicating scans are open in AbdomenAtlas/MerlinPlus on HF, where the masks are CC BY-NC-ND. |
| **RSNA RATIC abdominal trauma** (3,147 patients) | 241 (136) | mira.rsna.org/dataset/5 (controlled access to s3://abdominal-trauma-detection), or kaggle.com/competitions/rsna-2023-abdominal-trauma-detection/rules | A MIRA or Kaggle account, and acceptance of RSNA's terms: non-commercial, no redistribution of any portion. Derived labels would be for internal use only. |
| **CT-RATE** (21,304 patients, chest) | 95 (95; T13 only) | huggingface.co/datasets/ibrahimhamamci/CT-RATE | An HF account and the gate form: Name, Institution, Email, and a terms checkbox. CC BY-NC-SA 4.0. |
| **INSPECT** (CTPA, ~19,400 patients) | 86 (86; T13 only) | Stanford AIMI shared datasets | The same AIMI research-use agreement as Merlin. |
| **CADS-dataset** unique parts (CT-TRI 586, VISCERAL 167) | 49 (27) | huggingface.co/datasets/mrmrx/CADS-dataset | An HF account and one checkbox: "I confirm that I will review and comply with the license terms of each dataset component". CT-TRI is under CADS's own terms, which must be read for derived labels. The VISCERAL folders carry the VISCERAL data access agreement text. |
| **RSNA-STR Pulmonary Embolism CT, RSPECT** (7,279 training studies, CTPA) | 32 (32; T13 only) | kaggle.com/c/rsna-str-pulmonary-embolism-detection (data tab) | A Kaggle account and acceptance of the competition rules: RSNA's non-commercial research terms. |
| **MAGIC-CT** (562 patients with abdominal or thoracic tumours; NRRD) | 28 (16), class prior | zenodo.org/records/18389015 | The files download without a gate, but the record carries a data-use agreement. It covers: no re-identification; no sharing of access; security; reporting identifying information to the corresponding author; research use only; **proof of completed human-subjects/HIPAA training submitted with an application**; and releasing the code of any disseminated result. Only Greg can make that application. Not fetched. |
| excluded: NMDID; Glocker spine CT; CancerVerse; LNDb | 0 | nmdid.unm.edu; Imperial Box; HF BodyMaps; Zenodo 8348419 | Their licences forbid derivative works (NMDID's custom DUA; CC BY-NC-ND for the other three). No form would fix that. |

Merlin alone is worth more than all of tier 1 (E_low 1,260 vs 831) for one form. It is the single largest open
question in this plan.

Two notes on routes that are not forms:

- **ENHANCE.PET 1.6k** (section 4b) may need a Science Data Bank login. That is unconfirmed, and nothing was
  registered.
- **CT-RATE** has ungated re-uploads on Hugging Face under other accounts (for example `yw3325/CT-RATE-AB`). They were
  not used. The licensor distributes CT-RATE through its own form, and a copy that skips the form is not the route
  the licensor chose.

## 8. The programmatic scoping review, run for run date 2026-09-23

`REVIEW_RUN.md` has the full account, stage by stage. In short:

- **Where it stops.** Every stage ran. The run stops where the protocol puts a person: 26,176 records wait for
  screening, and charting follows.
- **What failed, and was fixed.** The search left about twenty queries unanswered: OpenAlex, Semantic Scholar,
  DataCite, Dryad and Open-i. On top of that:
  - arXiv refuses the WSL address.
  - bioRxiv's API was down on both days.
  - Springer's page size was a premium feature.
  - `check-run` and `stats` each had a defect.

  Each was fixed, re-observed within the run and recorded as a dated deviation (PROTOCOL.md section 19).
- **Its own validation fails.** Known-item recall is 9 of 21 (0.43) against the protocol's 0.80. That requires a
  documented revision of the frozen query strings. The revision is Greg's decision.
- **For this plan, the review adds little and cannot add more.** Its frozen scope is spine datasets, so it cannot
  enumerate body CT, where most anomalous people are. Of what it did surface, ENHANCE.PET 1.6k and LUMOS were new
  (section 4b); the rest was already on disk, fetched or ranked.
- **Why "any CT on the internet" stays finite.** The answer is the criterion of section 1, applied to catalogues read
  whole: IDC, the aggregators' source lists, and a size-filtered Zenodo sweep. The literature search is not that
  mechanism.

## 9. What is not known

- **Whether the priors hold.** The prevalences come from other populations. P(countable) is TotalSegmentator's,
  measured on a resampled release. The tier-1 screen measures both, and section 3 re-ranks on the measurement.
- **AMOS, the first measurement against a prior.** AMOS took the "ct abdomen" class P and was assumed thin.
  - At conversion, only **723 of its 2,364 CTs are ≤ 3 mm**: 1,564 were refused as thicker, and 67 are duplicates
    inside AMOS.
  - Its expected yield is therefore about a third of the ranked E (136.8 + 21.6), well under the half that triggers
    a re-rank (stopping rule 3). AMOS is fully fetched, so nothing is stopped, but its row overstates it.
  - The lesson is built into the 2026-09-24 rows: they were measured from image headers before any download, and
    their ≤ 3 mm fraction is folded into P.
  - AbdomenAtlas matched its prediction: 7,649 of 9,262 usable, against 7,835 predicted from its metadata.
- **Whether the late collections' extents mean what the bins say.** The extent-bin P assumes a CT of a given length
  covers what a TotalSegmentator CT of that length covers. A 450 mm pancreatic CT (PANORAMA) may be centred higher
  than a 450 mm abdomen-pelvis CT. The screen will measure it.
- **The TotalSegmentator task data and AbdomenAtlas 2.0 Mini** stay unresolved until an id map or an answer from
  their authors exists (section 4b). ENHANCE.PET 1.6k waits for its route.
- **Whether the screen's calls are right on the new collections.** The only outside number is the 70-case check in
  section 6. It ran on TotalSegmentator's own training CTs against a table with a narrower L6 definition, and
  labeller B was tuned on those same cases. No held-out outside check exists yet. Labeller B's known blind spots are
  a hypoplastic 12th rib that TotalSegmentator misses (it becomes a false L6 unless the short-rib rule catches it), a
  cervical rib (a false T13), a lumbarised S1 that TotalSegmentator folds into `vertebrae_S1` (an L6 read as
  ordinary), and fused bodies (refused, not miscounted). The review queue exists for these. A shared error, both
  labellers wrong the same way, still passes as two-labeller: the 2 external T13 read ordinary by both, and possibly
  vts_s0049. No acquired CT has a radiologist read.
- **People versus volumes** for AbdomenAtlas (FLARE and KiTS repeats) and for AMOS's unlabelled set.
- **Cross-collection duplicates** until `alias_pairs.csv` (the tier-1 dedupe, 40426214) and `alias_pairs_all.csv`
  (every collection, 40430971) land. That includes whether the RSNA trauma series are inside AbdomenAtlas, and which
  PANORAMA cases are MSD or NIH. A person scanned twice in two collections has no shared pixels, so no dedupe of this
  kind can find them.
- **GPU time.** The validation run measured TotalSegmentator `total` + `vertebrae_body` at 80–113 s per CT (L40S)
  and SPINEPS at 190–320 s per gated CT. For about 15,000 tier-1 CTs, roughly 70 % of them gated, that is about
  400 GPU-hours plus about 1,000 GPU-hours. The late additions add about 3,400 CTs before the one-per-person
  selection (about 90 + 230 GPU-hours), at the lowest priority. The chains ask for 8–12 GPUs each on gvohp/galhp, which other workflows'
  TotalSegmentator jobs are already using, so landing will take days to weeks and its order is not controlled.
  Three of the 69 validation SPINEPS runs failed inside SPINEPS (an affine assertion and a cc3d error). Those CTs have
  no labeller A, and that is recorded, not retried.
- **The CT Colonography remainder** (about 23 people) waits for the token match described in section 5.

## 10. What the acquisition-space review of 2026-09-24 changes here, and what it does not

Greg's uploaded review (`SchwingNet/lit/acquisition_space_review_2026-09-24.{pdf,txt}`; an AI-generated synthesis whose
claims are being verified at their primary sources by the review-integration workflow before any is cited) argues that
a detector's accuracy on C-arm frames saturates with the number of training samples once the dense region of the
acquisition space is filled, and rises only with coverage of the sparse bins. Its coverage measure is bins occupied
over bins that matter, and a normalised entropy over the bin occupancies. That argument is about C-arm poses. Applied
to this plan, which chooses CT collections, it says three things.

**The field of a CT decides which bins its people can occupy at all.** A chest CT can render the rib count (the T13
question) and nothing lumbosacral; an abdomen-pelvis CT the reverse; only a whole-body or chest-abdomen-pelvis field
renders both junctions. Coverage therefore enters this plan through the field, which is already the criterion of
section 1 and the P(both) / P(cage) columns of `ranking.csv`. The pose bins themselves (angles, SID, magnification)
are set at render time from whichever CTs exist, and their coverage is measured by the review-integration workflow
(`results/coverage/`), not here.

**Where the registry is dense and where it is sparse.** Distinct people in the registry rows on disk on 2026-09-24
(`transitional_registry/*/rows.csv`: VerSe, CTSpinoPelvic1K, TotalSegmentator, COBRA, other CT), by subtype, by which
junction the CT holds, by truth tier, and by whether the person has real projections:

| subtype | field | read | two-labeller | single-labeller | morphology-only | people | with real frames |
|---|---|---:|---:|---:|---:|---:|---:|
| L6 | both junctions | 100 | 29 | 10 | 0 | 139 | 3 |
| L6 | one junction or neither | 5 | 0 | 0 | 4 | 9 | 3 |
| T13 | both junctions | 6 | 1 | 1 | 0 | 8 | 0 |
| T13 | thoracolumbar only | 0 | 2 | 4 | 0 | 6 | 0 |
| sacralised L5, fused (Castellvi III/IV) | any | 27 | 0 | 0 | 0 | 27 | 0 |
| Castellvi I/II | any | 32 | 0 | 0 | 0 | 32 | 0 |
| lumbar rib | any | 13 | 9 | 5 | 0 | 27 | 0 |
| unassigned (four lumbar / eleven ribs / no grade) | any | 25 | 17 | 22 | 0 | 64 (+44 untiered) | 7 |

The dense bin is L6 with both junctions in field, read by a radiologist, without real frames. Every sparse bin is one
of: T13 (14 people, of whom 6 are read), anything with real frames (6 L6 and 7 unassigned people, all COBRA or
C-ArmLSpine), and the fused sacralised L5, which no mask screen can add because it needs a Castellvi read. Tier 1
adds mostly to the dense bin: about 460 expected count anomalies, most of them L6 from abdominal fields, none with
real frames. Tier 2 (chest CT, T13 by rib count) adds only to the T13 bin, which is where its whole value lies.

**A fifth clause for the stopping rule, stated now.** Among collections that clear rule 1, those whose expected people
fall in a sparse bin (T13; whole-body fields holding both junctions; pediatric fields) are fetched before those that
add to the L6-abdomen bin, at equal E_low per TB. This is an ordering, not a cut: the number of L6 people at which the
detector stops improving is not known for this task, and the review asserts saturation without measuring it. The
matched-N low- versus high-coverage render experiment of the review-integration workflow is the measurement; until it
reports, no collection is dropped for adding to the dense bin, and none is added for that reason alone below rule 1's
threshold.

**What does not change.** The count criterion, the priors, the two-labeller rules, and every tier-1 chain, which keep
running as submitted. The coordinator's checkpoint of 10:40 EDT lists this stream among the workflows that resume
unchanged.

**The first sparse-bin measurement, and what it found (NLST pilot, T13).** See section 11.

## 11. The NLST pilot's first measurement: a T13 rate that was wrong but plausible, and the rule it forced

The 500-person NLST pilot exists to measure two priors before tier 2 commits 2.3 TB of screening chest CT: the
cage-from-T1 rate and the T13 rate (section 3, rule 3). Its chain finished at 08:03 EDT on 2026-09-24.

**What it measured.** 367 of 500 CTs had a count from T1 by at least one labeller (0.73; the CHEST_SCREEN prior was
0.70). 34 of those 367 were called T13 (9.3 %), every one at single-labeller tier from labeller A alone, because
labeller B cannot count the cage on these CTs: its T1 rule needs a rib-free body above the first rib-bearing level, and
at the lung apices the body components merge and the cervical column is out of field. The prior band is 0.6-2.0 %.
Five to fifteen times the prior, from one labeller, on a field where the second labeller is blind: the number was
not believed.

**How it was checked, outside the computation that produced it** (`tools/acquisition_t13_check.py`, jobs 40436876 and
40436877; `anomaly_harvest/<collection>/t13_check/`). VERIDAH names a body T13 by its appearance. The subtype is
thirteen *rib-bearing* vertebrae. So each body VERIDAH named T13 was placed on labeller B's disc-interval levels by its
ctd point, and B's rib heads were read at that level. No new segmentation, no name from a mask id. The same question
was put to the 70 outside-labelled TotalSegmentator CTs, whose truth is not ours.

| | NLST pilot | validation_ts (outside truth) |
|---|---:|---|
| bodies VERIDAH named T13 | 34 | 9 |
| a whole rib head (B) on that body | 5 | 7: all 5 external T13, plus 2 external-L6 spines whose 20th vertebra carries a rib |
| no rib on that body | 21 | 2: both false (one external L6 where B reads six lumbar bodies, one negative) |
| only a field-edge-cut rib on that body | 2 | 0 |
| A's T13 point below B's last disc (B has no level there) | 6 | 0 |

The renders settle what the table says (`t13_check/<case>.png`, copied to `validation/t13_check/` and
`collections/nlst_pilot/t13_check/`):
vts_s0616, a true T13, has a rib on the body named T13 and thirteen rib-bearing levels; vts_s0899 has twelve rib
pairs and VERIDAH's "T13" is the rib-free first lumbar body of a six-lumbar spine; NLST 104893's "T13" is likewise
rib-free. A test that was tried and dropped: a rib head on the body VERIDAH names C7, meant to catch a one-body shift
at the top of a cut field. It fires on 196 of the 333 ordinary NLST spines too, because B's nearest-centre level rule
puts the first rib's head on the level above T1; it detects nothing and is reported only as a column.

**The rule, in the screen from 10:41 EDT** (`acquisition_screen.confirm_t13_by_rib`, applied at the `call` stage).
Labeller A's T13 stands only when labeller B finds a whole rib head on the body A names T13. It is then kept at
single-labeller tier and rendered into `review/` for adjudication, because a name plus one rib is still not a count
from T1. Otherwise the thoracolumbar call is no count, with the reason recorded in the row's notes (`T13 rib test`).
Every running chain applies it at its own `call` stage. Where `call` had already run, the stage was requeued: nlst_pilot
(call 40436963, summary 40436964, re-measure 40436965) and validation_ts (40436966-40436969, with the outside check
rescored into `VALIDATION.md`). csi2014 and ctpelvic1k_clinic carry no T13 name and were not requeued.

**What the pilot therefore says about tier 2.** After the rule, 338 CTs keep a count from T1 and 5 are T13 at
single-labeller tier (1.5 %, inside the 0.6-2.0 % band; `collections/nlst_pilot/SUMMARY.md`), and every one of the 5
is a single name with one rib, rendered in `collections/nlst_pilot/review/` and waiting for Greg's eye. The cage-from-T1 rate (0.73) matched its prior. Neither triggers a re-rank (rule 3: measured yield is not under
half of predicted). Tier 2 stays unsubmitted on rule 4 alone (more than 5,000 fetched CTs are still unscreened), and
when it is submitted, its T13 yield should be planned on about 1.5 % single-labeller calls that all need adjudication, not
on 9 %. A labeller B that counts the cage on chest CT would change that: the merged apical body components are the
defect, and it is recorded here, not fixed.

**What this changes in the registry rows.** In every collection screened from now on, a `T13` row at single-labeller
tier carries a rib on the named body and a render; a VERIDAH T13 without one is a `no_count` row whose notes say so.
The external-L6-with-a-rib cases (vts_s0362, vts_s1224; TS_s1088 in `transitional_subtypes.md`) remain the open
naming question between the rib convention and the lumbar-shape convention, and no rule here decides it.
