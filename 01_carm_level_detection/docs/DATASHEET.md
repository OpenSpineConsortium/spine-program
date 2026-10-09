# Datasheet — the corpora behind C-arm level naming

Written 2026-09-22, in the Gebru et al. headings, for every dataset the RSNA AI manuscript
(`paper/rsnai/main_v2.tex`) depends on: the real X-ray and fluoroscopy corpora, the synthetic device
corpus built from them, and the plain-film corpora the level model was developed on.

**Every count carries the file it was read from.** Counts marked *not recorded* are not available in any
release or any file on disk, and are marked so rather than approximated. The model side is
`docs/MODEL_CARD.md`; the machine-generated dataset table is `docs/RSNAI_TABLE1_DATASETS.md`
(`tools/rsnai_table1.py`); the hashed file inventory is `docs/RSNAI_DATA_MANIFEST.json`
(`tools/data_manifest.py`, built on the grid 2026-09-22 06:49, host hao1).

---

## 1. Motivation

### Why were these datasets assembled?

To ask whether a vertebral level can be named from operating-room C-arm exposures alone, with no
preoperative 3-D scan and no tracked instrument. That question needs three things no single public release
provides: (a) real intraoperative fluoroscopy with 3-D truth, (b) several *different* C-arms with paired
frames and CT so that each device's image formation can be fitted rather than assumed, and (c) enough
labelled vertebrae to teach a network what a level looks like rather than how to count to it.

No dataset was created by acquiring new patient images. Every corpus here is a public release, or is
synthesised from one.

### Who assembled it and who paid

Gregory Schwing, Department of General Surgery, Wayne State University School of Medicine / Detroit Medical
Center. Compute on the Wayne State grid. The author has a commercial interest in a level-confirmation
product under development, as stated on the manuscript title page.

---

## 2. Composition

### 2.1 The real device corpora

From `docs/RSNAI_DATA_MANIFEST.json` (`roots`, with a SHA-256 over each file list) and
`docs/RSNAI_TABLE1_DATASETS.md`:

| dataset | device | detector pitch | frames / subjects | 3-D pairing | files, bytes | licence |
|---|---|---|---|---|---|---|
| **C-ArmLSpine** | FIRST/Yiying Surgio-B51 flat panel | 0.15 mm at 2048 native (`docs/RSNAI_TABLE1_DATASETS.md`); the export is 1024², `px_mm_detector` 0.2930, **`px_mm` 0.1915** at the object plane (SID 1140, SOD 745 mm) | 296 frames (148 AP + 148 lateral), 148 cases, + 2 raw sweeps | CBCT per case; pose by registration | 59,609 files, 23.3 GB | CC BY 4.0 |
| **DeepFluoro** | Siemens Cios Fusion, CsI flat panel | 0.194 mm | 366 frames, **6 cadaveric pelves** | CT + C-arm pose per frame | 2 files, 2.5 GB (+ 94,626 vendor DICOMs, 72.7 GB) | CC BY-NC-SA 4.0 |
| **COBRA2026 (Elekta)** | Elekta XVI kV imager, centres A–D | 0.8 mm, 504² | projection sweeps; A 120, B 107, C 120, D 120 public cases (467); 152 fetched before the analysis, the rest fetching (array 40416296) | planning CT, deformably registered, + RTK geometry | 988 files, 42.2 GB | CC BY-NC 4.0 |
| **COBRA2026 (Varian)** | Varian OBI, centres F–G | *not recorded in the release headers read so far* | F 92, G 133 public cases (225); 26 fetched before the analysis (F 14, G 12), each with all five files, the rest fetching (array 40416296) | planning CT + RTK geometry | (in the same root) | CC BY-NC 4.0 |
| **Geneva hip** | Philips BV Pulsera, image intensifier | 0.2904 mm | 116 frames, 19 poses, **resin phantom** | CT + gold-standard pose | 69 files, 0.1 GB | CC BY-SA 4.0 |
| **Ljubljana 2D-3D-GS** | Trixell PIXIUM 4600, **turntable radiograph, not a C-arm** | 0.286 mm | 18 frames, **cadaver L1–L5** | CT + gold-standard pose | 181 files, 0.3 GB | CC BY-NC-ND |
| **SpineSAC** | six C-arms (Philips Allura Xper, GE Fluorostar, Ziehm NetPort, a Siemens model the headers do not name, Skanray, Siemens Fluorospot Compact S1) | *not recorded* | raw frames of **one sawbone phantom** | phantom CT + shipped poses; **no bone truth built** | 5,490 files, 4.1 GB | see repository |

**Only C-ArmLSpine is intraoperative human data.** Everything else is cadaver, phantom, radiotherapy
setup imaging, or a non-spine anatomy. The manuscript's Discussion says this; it belongs here too.

### 2.2 What is in an instance

Each real frame becomes one row in the common layout
`/rs/rs_grp_oschome/go2432/data/realxray/<dataset>/`, specified in `docs/REAL_XRAY_DATASETS_SPEC.md`:

- `images/<split>/<stem>.png` — 8-bit, converted to attenuation first and then windowed identically
  across devices (field percentiles 1/5/50/95/99 mapped onto 27/47/126/216/239, the FluoroCap operating
  room medians). Bone is bright.
- `labels/<split>/<stem>.txt` — YOLO boxes, class 0 vertebra, 1 sacrum, projected from the registered
  CT/CBCT through the frame's pose.
- `meta/<stem>.json` — device make/model/kVp/mAs, `px_mm`, view angles, the pose and its QC, every box
  with its level and `visible_frac`, and how the stored value was converted.

### 2.3 Labels, and what they are not

Level names on the intraoperative cases come from **two automatic labellers on the CBCT**,
TotalSegmentator and SPINEPS+VERIDAH, with only agreed levels scored.
`/rs/rs_grp_oschome/go2432/data/carmlspine/levels.json` `summary`:

| field | value |
|---|---|
| cases | 148 |
| vertebrae compared | 910 |
| agree | **814 (89.5 %)** |
| name disagreements | 41 |
| unmatched | 55 |
| SPINEPS missing | 3 |
| variant-flagged cases | 22 |

**The agreement filter is a selection, not a quality guarantee.** From
`/rs/rs_grp_oschome/go2432/data/realxray/carmlspine/summary.json`, boxes carrying an agreed name:

| level | boxes | named | share |
|---|---|---|---|
| T11 | 3 | 0 | 0 % |
| T12 | 63 | 6 | 10 % |
| L1 | 265 | 209 | 79 % |
| L2 | 296 | 284 | 96 % |
| L3 | 296 | 286 | 97 % |
| L4 | 296 | 286 | 97 % |
| L5 | 296 | 278 | 94 % |
| sacrum | 292 | 274 | 94 % |

What the filter removes is the thoracolumbar junction — the population the project exists for.
**No level truth in this study was established by a human**, and both labellers name a level by counting
from the sacrum, which is the anchor the system under test uses, so their errors may be correlated with
its errors.

### 2.4 Patient attributes

**Not available.** The C-ArmLSpine DICOMs carry no `PatientAge`, `PatientSex`, `PatientID` or
`PatientBirthDate` tag; `/rs/rs_grp_oschome/go2432/data/carmlspine/tags_case1.txt` (392 lines) carries
`Manufacturer` (一影医疗 / yiying Imaging), `Manufacturer's Model Name Surgio-B51`, `KVP` and
`Exposure Time` and nothing identifying. DeepFluoro is six cadaveric specimens, identified by accession
(`17-1882`, `17-1905`, `18-0725`, `18-1109`, `18-2799`, `18-2800`). Geneva and SpineSAC are phantoms.

Consequently the manuscript **cannot** state the age and sex of its intraoperative, cadaveric or phantom
populations, and that gap is real rather than an omission from this document. The only per-case attributes
recoverable from those releases are exposure parameters (kVp 73–111 on C-ArmLSpine, 120 on COBRA Elekta, 65–90
on Geneva) and the view angle.

**Correction, 2026-09-24.** An earlier reading of this section (and a draft sentence of the manuscript) said the
radiotherapy set releases no age or sex. It does: COBRA2026 ships `ct.PatientAge` and `ct.PatientSex` in each
case's `metadata.yaml` — age on 115 and sex (F/M) on 75 of the 145 Elekta detector cases (347 and 319 of the 692
public cases; centres D, F and G strip them). The manuscript now quotes age and sex per source from each
release's own metadata (`SchwingNet/results/age_sex_by_source.json`, `tools/age_sex_by_source.py`; supplement
Table S3) and names only the intraoperative, cadaveric and phantom sets as without.

### 2.5 Known duplication and contamination inside the releases

| finding | measured | file |
|---|---|---|
| **COBRA Elekta near-duplicates across splits**: 74,364 cross-case pairs at NCC32 ≥ threshold, max 0.998; 40 of the top 40 confirmed at 64² | different patients imaged at the same gantry angle; **0 same-case pairs**, so the by-case split holds | `/rs/.../or_ready/audit/AUDIT.md` (b) |
| C-ArmLSpine and DeepFluoro cross-split near-duplicates | **0** | same |
| realxray frames against the film corpus, FluoroCap panels, yolo_v6f | **0** pairs above threshold | same |
| **FluoroCap** literature panels | 29,484 panels (audit count); **72.8 % have zero pixel residual against another panel** — the same figure republished across papers, so the identity is the image and not a patient | `docs/DATA_ACCOUNTING.md` rows "FluoroCap literature"; `docs/HANDOFF_PHYSICS.md` |
| **BUU-LSPINE** | ships three duplicated `… (1).jpg` files; grouped by release `patient_id`, which absorbs them, and AP + LA are two items of one patient | `docs/DATA_ACCOUNTING.md` rows "BUU-LSPINE" |
| **BUU Drive mirror** | 5,495 films, byte-identical subset of BUU-LSPINE; excluded | same |
| **CTSpinoPelvic1K CT 0533** | truncated in the PUBLIC RELEASE, not locally: the HuggingFace object carries the same sha256 `20e673dc…d6e23`, and a short file has a valid hash so only size records it. Rebuilt from TCIA and swapped in 2026-09-23 (`478a74e9…a164d5`, 250,067,995 B, nine gates). Banks built before that hold **801 of 802**, after it 802 | `docs/DATA_COMPLETENESS_AUDIT.md` § Repairs |

### 2.6 The plain-film corpora the level model was developed on

From `docs/XRAY_DATASET_USAGE.md` (`tools/xray_dataset_usage.py`; counts are distinct films read from
each bank's own case array). The column is the level bank the reported model was trained on, not "some
bank on the machine": several corpora sit in a crop bank that was superseded or never trained on, and
conflating the two is how one dataset came to be printed with three different counts.

| corpus | view | on disk | in the level bank (v8/v9) | annotation |
|---|---|---|---|---|
| CSXA cervical | lateral | 4,963 | 4,963 | per-vertebra levels, released with the dataset |
| BUU-LSPINE | AP + lateral | 7,204 | 3,603 | endplate lines L1–L5 + S1; **levels assigned by position** |
| NHANES II | lateral | 17,073 of 17,075 | 543 | 543 films have landmarks (275 cervical + 268 lumbar, 364 persons); one of them, L00452, has no TIFF on disk and enters the bank from the pickle, so **16,531** films on disk carry no landmarks |
| VinDr-SpineXR | AP + lateral | 10,466 (5,000 studies) | 0 | **lesion boxes, not levels**; levels pseudo-labelled, no film in the bank the model was trained on |
| AASCE / BoostNet | AP | 579 | 0 | 68 landmarks, T1–L5; the 457 films are in `aasce_fov96_ctx`, which the reported model was not trained on |
| Mendeley 5jdfdgp762 | lateral | 714 | 0 | 4 corners per body, class-agnostic |
| Spinal-AI2024 | AP | 20,001 | 0 | machine generated; held out of the main corpus |

NHANES II is a **digitised national survey film corpus, not a clinical one**. FluoroCap is train-only
because a republished figure is the same patient.

**NHANES II, the two entries that are not on disk.** The CDC index lists 17,075 files; 17,073 are held.
`L00452.tiff` and `L00456.tiff` are served by `ftp.cdc.gov` as HTTP 200 with `Content-Length: 0` and are
listed at size 0 in the index (Last-Modified 2025-08-14), confirmed by HEAD and GET from a compute node on
two occasions (jobs 40416367 and 40416535). The shortfall is at the source; 17,073 is the whole fetchable
release. `L00452` is one of the 543 annotated films and its pixels survive inside the Zenodo pickle, so the
annotated set is complete. The download loop now carries a `.download_complete` marker stating this, because
its non-empty test could never pass over two empty files.

That one film is also why the unannotated count is **16,531 and not 16,530**: 17,073 films are on disk and
542 of them carry landmarks, the 543rd annotated film having no TIFF. Every figure of 16,530 subtracted 543
from 17,073 and so counted L00452 twice. The level bank is unaffected and still holds 543 NHANES films,
because that film reaches it from the pickle rather than from the TIFF.

**VinDr-SpineXR: one number per object.** Three counts were in circulation — 744, 2,632 and 10,274 — and they
are three different things. Read from each object itself (job 40416442 over the bank case arrays; job 40416535
per released image):

| object | count | what it is |
|---|---|---|
| the release, on disk | 10,466 images / 5,000 studies | 8,389 train (4,000 studies) + 2,077 test (1,000); every SHA-256 verified, 0 mismatches |
| `~/vindr_pseudo/ann` | 10,274 ann files | pseudo-labelled over the release; 192 images were never pseudo-labelled |
| of those, with a named level | 7,625 | the other 2,649 carry an empty levels dict and become no crop |
| `vindrps_fov96_ctx`, `allspine_v7` | 7,625 films (43,244 crops) | superseded banks |
| `carm_mix` and the C-ArmLSpine fold banks | 2,071 films (**2,632 crops**) | the 2,632 is a crop count of a capped mixed bank, never a film count |
| `vindr_fov96_ctx` (the old lateral-only route) | 744 films (3,679 crops) | view classifier → `vindr_det_drr` 2,328 → 744 |
| `allspine_v8`, `allspine_v9` — the level bank the model was trained on | **0** | VinDr is in no bank the manuscript reports |

Two defects sit behind those numbers and are not yet repaired: the 744-film route was computed over the
**5,136 images that carry a lesion box**, because the detector manifest ingests only rows with a box, so the
normal films never reached the view classifier; and the release's designated test split was consumed for
training pseudo-labels, which forecloses VinDr as a held-out benchmark. Both are recorded in
`docs/DATA_COMPLETENESS_AUDIT.md`; using all 10,466 images (directive D3) is a bank rebuild and is not done.

### 2.7 The synthetic device corpus

`/rs/rs_grp_oschome/go2432/data/devcorpus` (4,551 files, 2.4 GB in the manifest). Whole-spine CTs from
TotalSegmentator v2 (228,803 files, 52.3 GB; subject list `~/model_night/ts_clean_subjects.txt`, SHA-256
`2f96f917…`) are ray-cast under a device's real poses and styled through that device's nine fitted terms
(`docs/devices/<device>.json`). One training arm, from
`~/spine-detector/runs/devcorpus/dc_A_held_elekta_xvi/scores.json`: 5,408 synthetic entries, 896 real
entries (`real_rep: 2`), 794 validation entries.

**Synthetic frames stay with their CT.** All five styled corpora record the same 17 validation subjects
in their `STYLE_INFO.json`, so a subject is on the same side of the split under every geometry and every
noise card (`docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`, "What was also checked and is CLEAN").

---

## 3. Collection

### How the data were acquired

Not by this project. Every corpus was downloaded from its public source: Zenodo (C-ArmLSpine
10.5281/zenodo.22768651; COBRA2026 10.5281/zenodo.21322350), the JHU Dataverse (DeepFluoro vendor DICOMs,
doi:10.7281/T1/IFSXNV), Yareta (Geneva, 10.26037/yareta:2kw5s2jadbbv3ngtkzsovihtnu), the Ljubljana
laboratory page, and a Google Drive share (SpineSAC). Download dates, file counts, total bytes and a
SHA-256 over each file list are in `docs/RSNAI_DATA_MANIFEST.json`.

Poses were not supplied for C-ArmLSpine and were computed by 2-D/3-D registration
(`tools/carmlspine_pose.py`, 913 files). Pose quality is recorded per frame; the median edge NCC is
**0.370 (AP)** and **0.207 (lateral)** — `/rs/.../realxray/carmlspine/summary.json` `edge_ncc_median`.
Whether accuracy tracks pose quality is **not measured**.

### Sampling

COBRA2026: 152 Elekta cases of 692 public, plus 26 Varian cases (centres F 14, G 12, each with all five
files: `projections.mha`, `geometry.xml`, `ct_def.mha`, `fov_cbct.mha`, `metadata.yaml`), were fetched before
the analysis. The cut was download volume (42 GB for the 152 Elekta cases) and no criterion; the release has
six centres (A–D Elekta, F–G Varian; there is no centre E). The per-centre public counts, listed 2026-09-23
with the offset-paged `tools/cobra_fetch.py --list`, are A 120, B 107, C 120, D 120, F 92, G 133 = 692, exactly
the release count (`/rs/.../cobra2026/centre_<C>_cases_full.txt`). An earlier listing printed only the first
40 names per centre (a display truncation, not the API), so array 40416154 fetched 40 per centre; array
40416296 (`slurm/cobra_fetch_all.sh`, one task per centre letter, the E task a no-op, resumable) fetches the
remainder and the final analysis uses all of it. Job ids: `SchwingNet/results/JOBS_cobra.txt`. C-ArmLSpine: 148 of 149 released cases were built (one failed conversion: `case134`, which ships
no AP or lateral frame, only a raw 302-frame cone-beam sweep under `case134/ori/`). TotalSegmentator:
a clean whole-spine subject list, not the whole release.

### Reading traps recorded during collection

- C-ArmLSpine ships a **per-slice series UID** and a **placeholder `PixelSpacing` of 1.0**; the real pitch
  is 307.2 mm / 2048 (`docs/RSNAI_TABLE1_DATASETS.md`).
- 160 of 366 DeepFluoro frames are **stored upside down** (memory record
  `learned-formation-refuted-calibrate-instead`).
- COBRA case `B000` has 41 frames the CT never covers (registration failure) and is dropped.
- CT volumes in the wider project are P,I,R, not RAS; canonicalise to analyse, never to write.

---

## 4. Preprocessing, cleaning and labelling

1. **Stored value → attenuation**, per device, with the choice recorded in each frame's meta
   (`stored_value`, `conversion`).
2. **One display window for every device** (§2.2), so a detector is not learning a vendor's tone curve.
3. **Boxes by projection**: every mask voxel (subsampled to ≤ 20k points) through `K·ext`, 2nd–98th
   percentile extent, clipped; kept when `visible_frac ≥ 0.5` and both sides ≥ 8 px.
4. **Two labellers, agreed levels only** (§2.3). Boxes with a null level are kept for detection training
   and excluded from naming scores.
5. **Splits by case**, `int(md5(case), 16) % 10` → 0–6 train, 7 val, 8–9 test, deterministic. Audited:
   `/rs/.../or_ready/audit/AUDIT.md` (a) records 0 cases in more than one split for every dataset, 0
   meta/splits disagreements and 0 images in the wrong split directory.
6. **Look at the contact sheets before reporting**: `qc/` per dataset. This is a rule in
   `docs/REAL_XRAY_DATASETS_SPEC.md` because a flipped frame or an inverted polarity makes every
   downstream number plausible and wrong.

The raw downloads are kept; nothing is deleted in place.

### Two split defects that shipped, and are not repaired yet

`tools/make_context_crops.py` drew its split **per source directory**, so one person under two names got
two independent draws:

| pair | the two names | measured leak |
|---|---|---|
| NHANES II | `films_drr` `nhanes_00160` vs `nhanes_drr` `NH_00160_c` | 48 of 54 validation patients had their other copy in training (banks v2, v6, v7) |
| CTSpinoPelvic1K | `ctsp_drr` `CTSP_COLONOG_<n>` vs `physics_drr` `ctsp_<release id>_…` | **357 people** on both sides of v6 and v7 |

`docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md`, `docs/SPLIT_LEAK_CROSS_NAMING_2026-09-22.md`. The fix is
`tools/patient_keys.py` (one key per person across every naming scheme) plus a split drawn over people;
the clean rebuild `slurm/allspine_v8_clean.sh` → `allspine_v8_bank.sh` → `allspine_v8_train.sh` has not
landed. **CSXA's one-image-one-patient assumption is untested**, and both leak documents say so.

---

## 5. Uses

### What these data have been used for

Training and evaluating the four models in `docs/MODEL_CARD.md`; fitting the per-device image-formation
cards in `docs/devices/*.json`; the corpus manifold analysis in `tools/corpus_manifold.py`.

### What they should not be used for

- **Clinical decisions.** Nothing here is cleared, and the level truth is machine-generated (§2.3).
- **Claiming a population.** No age, sex, habitus, indication or pathology mix is recoverable for the
  intraoperative, cadaveric or phantom sets (§2.4; COBRA2026 releases age and sex for part of its cases, and
  nothing else), so no statement about who the 148 intraoperative cases are is supportable.
- **A thoracolumbar-junction or transitional-anatomy benchmark.** The agreement filter withholds exactly
  those levels (§2.3), and only 3 of 148 cases carry a VERIDAH L6, so the transitional rate in the test
  set is essentially unverified.
- **Testing on COBRA Elekta without reading §2.5.** 74,364 near-duplicate cross-split pairs means the
  test frames resemble training frames closely even though no case crosses the split.
- **FluoroCap as a test set.** 72.8 % of its panels are republished figures; it is train-only.

### What could go wrong for a data subject

The releases are already de-identified and public; this project adds no identifiers and re-derives none.
The risk that does exist is **downstream**: a level named wrongly with high confidence (see
`docs/MODEL_CARD.md` §5.3, T13 at 0 % accuracy and 0.804 mean posterior) is the failure a datasheet reader
should carry away.

---

## 6. Distribution

The derived layout (`/rs/rs_grp_oschome/go2432/data/realxray/`) is **not distributed**. Every source is
public under its own licence (§2.1), and the licences differ: CC BY 4.0 (C-ArmLSpine), CC BY-NC 4.0
(COBRA2026), CC BY-NC-SA 4.0 (DeepFluoro), CC BY-SA 4.0 (Geneva), CC BY-NC-ND (Ljubljana). **A merged
redistribution is not possible under those terms**; a reader reproduces the layout by downloading each
source and running the exporters (`tools/realxray_*_export.py`).

FluoroCap panels are figure-reuse only and are never redistributed. Radiopaedia was never scraped (its
terms forbid AI training and are non-commercial).

The manifest with its file-list hashes (`docs/RSNAI_DATA_MANIFEST.json`) is released with the code so a
reader can check they downloaded the same files.

---

## 7. Maintenance

| item | status |
|---|---|
| owner | Gregory Schwing (`[e-mail withheld]`) |
| manifest rebuild | `tools/data_manifest.py`, `slurm/`; last built 2026-09-22 06:49 on host hao1 |
| drift check on every quoted number | `tools/claims_check.py` against `docs/RSNAI_CLAIMS.json`; exits non-zero when a number moves. **Its 54 claims cover the manuscript, not this datasheet**: no count in §2 or §8 is keyed in that ledger, so nothing re-checks them when a bank is rebuilt |
| leakage audit | `tools/or_audit_splits.py`, `tools/or_audit_dupes.py`, `tools/leak_check.py`, `tools/patient_keys.py` |
| known unrepaired defects | the two split leaks (§4); COBRA Varian header fields; SpineSAC has no bone truth; CT 0533 repaired on disk 2026-09-23 but still truncated in the published release until it is re-uploaded |
| erratum policy | a correction goes in a dated document under `docs/` and a `history` entry in `docs/RSNAI_CLAIMS.json`; `expect` is never edited to match a moved value without that note |

`or_ready` and `devcorpus` are **output** roots that drift by design; the paper-time manifest check must
be run on the input roots only (`docs/RSNAI_PLAN.md` box E1).

---

## 8. A CONSORT-style flow is missing, and what it would contain

Five denominators for one dataset appear in the manuscript's own numbers and none is defined where it is
used. The pieces are on disk and are assembled here as the flow a reader should be given:

```
C-ArmLSpine   149 released -> 148 built -> 296 frames (148 AP + 148 lateral)
              CBCT vertebrae:  910 compared by the two labellers -> 814 agreed (89.5 %)
              projected boxes: 1,807 truth boxes -> 1,623 carry an agreed level name
              lateral scoring: 676 agreed vertebrae in 143 cases (oracle boxes, complete coverage)
                               -> 617 matched by the detector in 141 cases (the 98.2 % denominator)
              AP scoring:      673 agreed -> 631 matched
              fixed test split: 28 cases / 56 frames / 287 truth vertebrae
COBRA2026     692 public (A 120, B 107, C 120, D 120, F 92, G 133) -> 152 Elekta + 26 Varian fetched before the
              analysis (full fetch: array 40416296) -> 145 Elekta cases in splits
              -> 41 B000 frames dropped (the CT never covers them)
DeepFluoro    6 specimens -> 366 frames -> 1 test specimen (104 frames)
CTSpinoPelvic1K  802 cases -> 801 rendered (0533's CT was truncated in the release; repaired 2026-09-23, so banks rebuilt after that hold 802)
```

The box counts are `boxes_per_level` and `named_per_level` summed from
`/rs/.../realxray/carmlspine/summary.json` (1,807 and 1,623); the scoring counts are
`oracle/LAT/kfull`, `det/LAT/kfull`, `oracle/AP/kfull` and `det/AP/kfull` in
`docs/carmlspine_cv5_mixed_2026-09-21.json`. **The three denominators 1,623, 676 and 617 are all in use
in the project's own documents and none of them is defined where it is used**, which is how a
detector-conditioned rate came to be described as "scorable vertebrae (both segmentation tools agree)".

Sources: `/rs/.../realxray/carmlspine/summary.json`, `/rs/.../carmlspine/levels.json`,
`/rs/.../or_ready/audit/AUDIT.md`, `docs/carmlspine_cv5_mixed_2026-09-21.json`,
`docs/RSNAI_DATA_MANIFEST.json`. **The figure itself does not exist yet**; `tools/fig_data_flow.py` draws
a lineage graph and would have to carry the drop counts.
