# Patient identity: how a case becomes a person

Status: specification for a metadata-first replacement of `tools/patient_keys.py`.
Written 2026-09-22 from a discovery pass over every bank on `grid.wayne.edu`, with every claim
put through an adversarial re-derivation. Counts that survived two independent routes are stated
plainly; counts that did not are marked **[UNCERTAIN]** and say what would settle them.

## Why this file exists, restated

The split is drawn per source directory. Two directories holding one person under two names split
independently, the person lands on both sides, and no score can show it. It has happened four times
now (NHANES II, CTSpinoPelvic1K, VerSe series-vs-patient, VinDr image-vs-study), and the current
keyer is itself a cause: it reads the file NAME first and only three `ann` fields, so it refused
three whole banks — `aasce_drr` (457), `anchor_drr` (7,842), `fluorocap_drr` (2,385) — while the
identity for all three was sitting in metadata on disk the whole time.

The brief is the correction: **read identity from headers and tables; the file name is the last
resort, never the first.**

---

## 1. THE RESOLUTION ORDER

One ordered list, tried per case, most authoritative first. The first layer that returns a person
wins. Every key records which layer produced it, so a reviewer can count how many cases rest on a
file name.

**L0 — Corpus resolution (precondition, not a key).**
A person id is only meaningful inside a corpus, so the corpus must be fixed before identity is read.
Resolve it from, in order: the ann's `source` / `scheme` field; the bank root's declared corpus in
the bank registry (see §5); the *second* field of the case name. Never the first field, and never the
bank's directory name: `ctsp_drr_obl` and `ctsp_drr_obl2` hold 3,767 anns named
`CTSP_VERSE_verse###_p#` which are **VerSe** subjects, and `carm_drr` contains real intraoperative
frames although `CT_INVENTORY.md` calls it CBCT (`tools/ct_inventory.py:39`).

**L1 — A DICOM identity tag, or a cached index built by reading them.**
Top of the list because it is the only identifier assigned by the institution that made the image.
Used by: CTSpinoPelvic1K (`patient_db.json`, built by `scripts/tcia_index.py` which reads
`(0010,0020) PatientID` off one DICOM per series), VinDr-SpineXR (`StudyInstanceUID`), DeepFluoro
(CT `PatientID`), C-ArmLSpine (private `(0029,0016)`).
Two standing warnings, both measured: a DICOM identity tag can be **wrong** (DeepFluoro's fluoro
`PatientID` splits all six cadavers and merges two of them), and it can be **absent**
(C-ArmLSpine `PatientID` is `''` on 59,307 of 59,609 instances). L1 is authoritative only where a
per-corpus rule in §2 says which tag, on which modality.

**L2 — The originating release's own published subject table.**
The dataset authors' statement of who is who, where no header survives. Used by: VerSe
(`verse_demographics.csv` → `manifest.csv` `patient_id`), BUU-LSPINE
(`KIOM2022_dataset_report.xlsx`), TCIA's NBIA API (external corroboration for CTSP), the COBRA2026
paper (the *only* warrant that a COBRA case is a patient). Below L1 because it is the authors'
grouping, not the scanner's — if the table missed a repeat scan, nothing on disk detects it.

**L3 — The release manifest row shipped with the derived dataset.**
`~/data/CTSpinoPelvic1K/manifest.json`: 802 rows, `volume_id` → `token`, and `token` is the tail of
the DICOM PatientID. This is L1 evidence already distilled; it sits below L1 only because it can
drift from the headers it was built from (9 records carry a non-UID `..._orientation_fixed` string
in `spine_series_uid` / `pelvic_series_uid`, which is how a naive join silently loses 5 records).

**L4 — A crosswalk that maps one released id space onto another.**
Dataset813 `imagesTr/COLONOG_<token>_0000.nii.gz` → `<release_id>_ct.nii.gz` (802 links, injective
and surjective onto the release, re-derived independently); VinDr `annotations/{train,test}.csv`
(`image_id` → `study_id`, agrees with the DICOM on 10,466/10,466); FluoroCap `s2_works.jsonl` and
`openalex_works.jsonl` (route id → pmcid/doi); the TotalSegmentator v201→v300 renumber table (§3).
Symlink **names** are read, never followed — the targets are container paths that dangle on the host.

**L5 — Structured ann identity fields: `scheme` + `source_case`.**
A field pair, not a string to be regexed: `{"scheme":"implant","source_case":"0001_v0"}`. It names
the source corpus and the source case, so it can be routed back through L2–L4. Present in
`physics_drr`, `physics_drr_film`, `physics_rare`, `cut_*`; **absent** in `anchor_drr` and
`anchor_drr_c2`, whose anns hold only `case, view, shape, levels, n_boxes, hardware, implant_boxes`.

**L6 — The ann's `patient_id` string. DEMOTED from first place to sixth.**
It is a bank-local convenience string, not an identity, and today's keyer trusting it first is the
single largest defect in the file. Named failures:
- `mendeley_drr`: `MEND_N24-Olisthesis-L4-5-F-35-Yrs` and `MEND_N24-S-64-M_1001_0` both carry
  `patient_id: "mendeley_N24"` — a 35-year-old woman and a 64-year-old man under one key. Built by
  `tools/mendeley_to_render.py:296-297`, a plain `orig.split('-')[0]`.
- `vindr_det_drr`: `patient_id = "vindr_<image_id>"` — image level, so one study is up to ten people.
- `ctsp_drr_obl`: `patient_id = "CTSP_VERSE_gl279"`, which today's regex
  `^([a-zA-Z]+)_?(\w+)$` turns into corpus `ctsp`, person `VERSE_gl279` — a VerSe subject filed as a
  CTSpinoPelvic1K patient.
- `spinalai_drr`: `patient_id = "sim_000237"` is a structural-similarity nearest neighbour, not a
  person at all.
L6 is used only when the corpus rule in §2 marks `patient_id` as corpus-native (BUU, NHANES, CSXA),
and never for a corpus on the L6 denylist (mendeley, vindr, ctsp_drr_obl*, spinalai, carm).

**L7 — The enclosing specimen / case / article directory.**
DeepFluoro `..._cadaver_<accession>` and the H5 top-level group; C-ArmLSpine `case<N>`; COBRA
`<centre><nnn>`; FluoroCap `panels/<document id>/`. Below the ann because it is a packaging artefact,
above the file name because it is the unit the distributor asserts ("No file contains information
for multiple cadavers", DeepFluoro Readme p. 4).

**L8 — The file name.** Last. A regex over a stem, used only when L0–L7 produced nothing.

**L9 — Content identity, as a MERGE pass over the keys L1–L8 produced, never as a first reading.**
md5 of the source volume, or of the int16 voxel array, or a perceptual hash of a 2-D panel. It can
prove two files are the same bytes; it cannot prove two acquisitions are the same person, and it
breaks on re-export (TS `s0254`/`s0927` are one scan whose bytes differ). It is nevertheless the
**only** identity TotalSegmentator has, so §2 promotes it to L1 for that corpus by explicit override.

> The order above is the default. Per-corpus overrides are declared in the table in §2 and nowhere
> else; a corpus may not silently reorder it.

**Key format.** `"<corpus>:<person>"`, e.g. `ctsp:100`, `verse:verse400`, `ts:s1943`,
`vindr:00403a30acf99250cfc4c56010be9ba0`, `fluorocap:pmc:PMC3488645`, `deepfluoro:18-2800`.
Alongside each key the keyer records `layer` (L1…L9), `scheme` (the rule that fired) and `root`.
Keys are stored under **`(root, case)`**, not `case` — today's flat dict silently merged 161
case-name collisions between banks.

---

## 2. PER-CORPUS RULES

`n cases` counts ann files (or frames where a bank has no ann). `before` is what the shipped
`tools/patient_keys.py` + `docs/CT_INVENTORY.md` produce today.

| corpus | identity unit | source of truth (path + field) | rule | n cases | n persons after keying | before |
|---|---|---|---|---|---|---|
| **ctsp** (CTSpinoPelvic1K) | one TCIA PatientID; one release id = one person, verified 802/802 by two routes | L1 `~/CTSpinoPelvic1K/data/patient_db.json` → `patients.<uid>.patient_uid` / `.patient_token` (825 patients, 3,451 series); L3 `~/data/CTSpinoPelvic1K/manifest.json` → `volume_id`,`token`; L4 Dataset813 `imagesTr/COLONOG_<token>_0000.nii.gz` → `<rel>_ct.nii.gz` | `CTSP_COLONOG_<token>[_s<k>]` → token direct. `ctsp_<rel>_(ap\|lat)[_p<k>][_s<j>]` and `implant_<rel>_v<k>_(ap\|lat)[_p<n>][_s<j>]` → rel → manifest `token`. Key `ctsp:<token>`. Match the token as `[A-Za-z0-9-]+`, **not** `\d+` — 34 of 802 are `CTC-<10 digits>`. Strip `_v\d+` before keying; an implant render is the same person as its clean render | 12,078 CTSP-named anns over ≥10 banks (ctsp_drr 801, ctsp_drr_film 801, anchor_drr 1,602, anchor_drr_c2 1,602, physics_drr 2,430, physics_drr_film 2,430, physics_rare 603, physics_rare_film 603, cut_rare 603, cut_rare_v2 603) **plus** 6,877 implant renders (anchor_drr 3,036, physics_drr 1,321, physics_drr_film 1,321, cut_physics 570, cut_physics_v2 570, physics_smoke 14, postop_render 45) | **801** (0533 is in no bank; its CT on the grid is a truncated download, 16.5 MiB, gzip EOFError). physics_* additionally lack 0721, 0919, 1020 → 798 there | 801 via the d813 crosswalk on `ctsp_drr` only; `anchor_drr` entirely refused (`CT_INVENTORY.md` prints it as 7,842 subjects); implant renders keyed as a separate corpus `implant:<rel>_v<k>` — 828 keys for 558 people |
| **ts** (TotalSegmentator v2.0.1 + v3.0.0) | one CT scan. **No patient identifier exists** — `meta.csv` is `image_id;age;gender;institute;study_type;split;manufacturer;scanner_model;kvp;pathology;pathology_location` (+`convolution_kernel;slice_thickness` in v3); no DICOM, no accession, no study UID; NIfTI `descrip`/`db_name`/`aux_file` empty on all 3,167 volumes | **L9 override**: md5 of `ct.nii.gz` (or of the int16 array), plus a `(shape, affine)` union for re-exports. Table at `~/ts_dupscan_out/ct_fingerprints.json` (3,167 records) | Resolve `(release, sid)`: release from the bank registry, **never** from `ann["source"]`, which says `TotalSegmentator_v201` on all 1,735 `ts_drr_v3` anns. Accept four name forms: `TS_(s\d+)`, `totalseg_(s\d+)_(ap\|lat)`, `..._p\d+`, `..._p\d+_s\d+`. Apply the 24-row v201→v300 alias table and the three intra-v300 dedup groups. Key `ts:<canonical v300 id>` | ts_drr 1,170; ts_drr_v3 1,735; anchor_drr 2,456; anchor_drr_c2 3,779; physics_drr 1,831; physics_drr_film 1,831 | **1,935** distinct scans over the two releases (1,939 v300 folders − 4 duplicate ids; all 1,228 v201 folders map in). Persons ≤ 1,935, unknown | `ts:s####`, release-blind. Merges 15 pairs of different people and splits 24 people. `ts_drr_v3` is not among the keyer's roots at all |
| **verse** (VerSe 19/20) | one TUM **subject**; 374 series belong to 355 subjects | L2 `~/VerSeFusion/configs/verse_demographics.csv` (`subject`, `split`, `CT_image_series`; note the series id sits in the `split` column for multi-series rows) → distilled to L2 `~/VerSeFusion/data/manifest/manifest.csv` `series_id`,`patient_id`,`patient_pos` and to `~/VerSeFusion/data/unified/scan-<sid>/scan-<sid>_meta.json` `patient_id` | Strip any `^CTSP_VERSE_` prefix and any doubled `gl` prefix; take the **last** `(gl\|verse)\d+[a-z]?` token of the stem (covers `gl003`, `glgl017`, `verse090`, `gl003_p0`, `gl016_s0`, `verse_scan-gl003_lat_p2`, `CTSP_VERSE_gl279_p0`); map series → patient. Key `verse:<patient_id>` | verse_drr 387, verse_drr_film 374, verse_drr_obl 1,494, verse_drr_obl2 2,989, verse_soft_drr 374, ctsp_drr_obl 1,256, ctsp_drr_obl2 2,511, physics_drr 1,463, physics_rare 879, anchor_drr 748, anchor_drr_c2 ~ (see registry) | **355** over the whole corpus; 312 for `ctsp_drr_obl`'s 314 series; 263 for `physics_drr`'s 282 series | `verse:<series id>` — 374 believed people, 19 phantoms, 18 people split. `verse_drr_obl`, `verse_drr_obl2`, `verse_drr_film` (4,857 anns) refused outright by the anchored `verse_any` suffix group |
| **nhanes** (NHANES II) | one 5-digit CDC sample-person number; at most one cervical and one lumbar film | L2 the annotation pickles themselves: `~/spine-detector/data/raw/nhanes_annotated/extracted/nhanes/*.pkl`, scalar field `sample_id` (543 pkls → 364 ids, 179 shared by one C and one L) | `NHANES_nhanes_(cervical\|lumbar)_(\d+)`, `NH_(\d+)_[cl]`, **and a new scheme `NHANESPS_([CL])(\d+)`**. `int()`-normalise, zero-pad to 5. c/l is a REGION. Key `nhanes:<00160>` | films_drr 543, nhanes_drr 543, films_drr_buucorr 543, **nhanes_pseudo 16,234** | **364** annotated people; nhanes_pseudo covers 9,579 numbers, 362 of the 364 among them | c/l already collapses correctly; `nhanes_pseudo`'s 16,234 all refused (no scheme, no `patient_id`). 96 of 364 numbers straddled the v6/v7/v7nofluoro splits |
| **buu** (BUU-LSPINE v1) | one 4-digit case number; digit after `Y` is the VIEW (0=AP, 1=LA), not a visit | L2 `~/spine-detector/data/raw/buu_full/BUU-LSPINEv1/KIOM2022_dataset_report.xlsx` (sheets `Pos_AP`, `Pos_LA`, `Normal-Disorder` keyed `0001-F-037Y`); `~/lstv_flag/sources/buu3600_lstv_labels.csv` (`patient`,`file_AP`,`file_LA`) | `BUU_FULL_buu_(\d{4})-[MF]-\d+Y[01](\(\d\))?` and `MEND_(\d{4})-...`; strip `(1)`. Key `buu:<NNNN>`. No DICOM exists — JPEG only | films_drr 3,603, films_ap_drr 3,600, films_drr_buucorr 3,603, mendeley_drr 500 | **3,600** by the released table; **[UNCERTAIN] ≤3,598** — `0140`/`0719` have byte-identical AP *and* LA jpgs (sha1 `30deecee0e40`, `4e87389c2349`, both M/24/0.140 mm) and `0449`/`0629` share an AP jpg (`c87e1387b435`). L9 should merge them | keyed correctly via `patient_id`, but `films_ap_drr` (3,600 people) is not among the keyer's roots and has never been audited |
| **csxa** | one 4-digit sequence number; 4,963 images = 4,963 individuals per the descriptor | L2 `~/spine-detector/data/raw/csxa/datasets.xlsx` sheet `Basic information` (5,002 rows = 2 header + 5,000 slots, 4,963 filled); naming rule stated verbatim in `s41597-024-03383-0.pdf` | `CSXA_csxa_(\d{4})\d{3}` → key `csxa:<SSSS>`. The `<G><AA>` tail must stay OUT of the key: it disagrees with the table on `0873166` and `3556142` | films_drr 4,963, films_drr_buucorr 4,963 | **4,963** | 4,963 (current `csxa_film` keeps the full 7 digits; still injective, so harmless) |
| **vindr** (VinDr-SpineXR) | one **StudyInstanceUID**. `PatientID`, `PatientName`, `AccessionNumber`, `StudyDate` are absent from all 10,466 headers, so the study is the finest recoverable unit and is a lower bound on the person | L4 `~/spine-detector/data/raw/vindr/1.0.0/annotations/{train,test}.csv` → `study_id,series_id,image_id` (agrees with the DICOM `StudyInstanceUID` on 10,466/10,466; no pydicom needed). L1 fallback: `.../{train,test}_images/<sop>.dicom` | Any case whose stem or `patient_id` tail is a 32-hex VinDr `image_id` → `vindr:<study_id>`, under **any** prefix: `VINDR_vindr_`, `VINDRPS_`, `MEND_`. Never key on the image id | vindr_det_drr 2,328; vindr_pseudo 10,274; `~/vindr_pseudo_drr` 744 (**recounted 2026-09-23, job 40416442: both are right and are different objects** — 10,274 pseudo-label files over the release, 744 anns of the superseded lateral-only route, a subset of vindr_det_drr's 2,328); mendeley_drr 13 | vindr_det_drr's 2,328 → **2,118** studies (158 studies with >1 case, 368 cases involved, 210 removable). Whole corpus 10,466 images → **5,000** studies | image-level `vindr:<image_id>` from `patient_id`; `VINDRPS_*` refused entirely. `vindrps_fov96_ctx` leaks 1,199 of 1,541 val cases (77.8 %) to a same-study sibling in train |
| **mendeley** (Mendeley-716) | resolves to another corpus; it is a redistribution, not a cohort | L4/L2 as above; `duplicate_of` field on 500 of 584 anns | BUU-form stem → `buu:<NNNN>` (500). 32-hex stem → `vindr:<study_id>` (13). Everything else (`N<k>-Olisthesis-*`, `Screenshot-2022-07-31-*`, `*_jumbo_jpeg`, `PARS_*`) → **REFUSE** (71) | 584 | **≈500 buu + 12 vindr persons** (`f2072260…` and `f4dd04fb…` are one study `b830a545…`) + 71 refused | `mendeley:<first hyphen token>` — 84 non-BUU cases → 51 keys, `mendeley_Screenshot` covering 33 films and `mendeley_N24` covering two different people |
| **aasce** | **unknown.** The trailing index groups films; whether an index is one person is not established | L8 only. `~/spine-detector/data/raw/aasce/{train,test,train_txt}` — 579 jpg, 4 csv, 483 mat, zero DICOM, zero EXIF entries | `AASCE_sunhl-1th-<DD-Mon-YYYY>-(\d+)_[A-Z]_AP` (and the `_AP2`/`_AP_(2)` re-export variants) → `aasce:<int index>`. **Do not include the date**: 11 indices span two dates, and `10-Jan-2017-254_C` vs `11-Jan-2017-254_F` are closer in landmark shape (0.0077) than any known duplicate pair. The 17 `...-coronal<n>` names carry no index → **REFUSE** | aasce_drr 457 (440 keyable + 17 coronal) | **217** index groups — an upper bound on films, a lower bound on people, and **[UNCERTAIN]** as a person count (index 254 holds 16 films with first-column Cobb 18.9°–67.2°) | all 457 refused |
| **spinalai** (Spinal-AI2024) | **there is no person.** The films are machine-generated; `patient_id` is column B (`Top1-Image`) of `image_similarity_checklist.xlsx`, a similarity audit | L6 (flagged non-person). `~/spine-detector/data/raw/spinal_ai2024/repo/image_similarity_checklist.xlsx`, 20,440 data rows, 52 distinct `Top1-Image` | Key `spinalai:<sim group>` with corpus flag `person_key = false`. The splitter must place the **entire corpus** on one side. The grouping is an artefact: column H (perceptual Top1) gives 100 groups instead of 44 and agrees with column B on 32 of 20,440 rows; `SPAI_001956` (Cobb sum 6.7) and `SPAI_015376` (sum 179.0) share a key | spinalai_drr 8,358 | **44 groups, 0 persons** | 44 keys `sim:<n>` presented as people |
| **fluorocap** | the **source document** — one journal article, or one YouTube video. No patient identifier exists and cannot: `patient_identifier_present` = `no` on all 1,616 matched rows; `metadata_removed` = "yes (panel re-encoded as PNG…; no EXIF or DICOM metadata carried)" | L4/L7 `~/FluoroCap/manifest.csv` (21,603 rows × 112 cols, join on `panel_path`), `video_panels.jsonl` (1,095) + `video_panels_med.jsonl` (366) → `video_id`, `~/FluoroCap/s2_works.jsonl` (6,287) and `openalex_works.jsonl` (9,780) → route id → pmcid/doi, `articles.csv`, `duplicate_groups.jsonl` (11,446) | (a) `^(?:panels/)?video_panels(?:_med)?/(.+?)_(\d{5})__` → `fluorocap:yt:<video id>`. (b) else `pmcid` → `pmc:<id>`; else a `PMC\d{5,9}` in `source_article_url`/`url_doi`/`url_article_europepmc`/`figure_path`/`source_image_url`; else a DOI, **resolved through `s2_works.jsonl` + `openalex_works.jsonl`, not `articles.csv`** (which resolves 0 of the 123 doi keys); else the route-id directory resolved through the same two files; else `fig:<aggregator>/<figure slug>` — never the aggregator directory itself (`pmc18m` holds 134 panels from 85 articles). (c) union-merge by perceptual hash | fluorocap_drr 2,385; fluorocap_drr_smoke 137 (a strict, byte-identical subset — never split independently); fluorocap_pack 1,500 (939 shared with fluorocap_drr, 44 with smoke) | **[UNCERTAIN] ≈1,197 documents.** 1,214 keys before merge; 1,201 after the shipped 0.98 pixel union; the s2/OpenAlex crosswalk collapses at least 4 more (`art:s2_367843b7…`→`pmc:PMC3488645`, `art:s2_b74ec088…`→`pmc:PMC4130957`, `doi:10.1186/1749-799x-9-2`→`pmc:PMC3898569`, `doi:10.1186/1754-9493-5-33`→`pmc:PMC3259034`). Recompute and freeze | all 2,385 refused |
| **carmlspine** (C-ArmLSpine) | one `case<N>` folder = one acquisition session. **Not provably one person** | L1 private tag `(0029,0016)` — the un-stripped console PatientID, present on all 149 cases, 149 distinct values, zero cross-case collision (`case1/C-arm/0001.dcm` → `[withheld]`). L7 the `case<N>` folder, which is 1:1 with `PatientName` on 149/149 | Key `carmlspine:case<N>`. Map `case<N>_AP`/`case<N>_LAT` (the `carm_drr` ann `case` field) to the same key; read `patient_id` in the DRR banks, which does carry `case101`. **Never** key on `PatientID` (empty on 59,307 files), `StudyInstanceUID`, `SeriesInstanceUID` or `SOPInstanceUID` (one UID per file, 58,911 distinct over 148 cases) | 149 case folders; realxray/carmlspine 148 cases / 296 frames; carm_drr 120 patients / 240 anns; carm_cv0..cv4_drr the same people under different split labels | **149** acquisitions; **persons ≤149, unknown** | refused (`case101` → corpus `case`, person `101` under the current `patient_id` regex — a degenerate corpus name). realxray banks are invisible to the keyer entirely: it globs `<root>/ann/*.json` and they store `meta/` |
| **deepfluoro** | one cadaver, by Johns Hopkins autopsy accession | L7 the H5 top-level group `/17-1882` in `ipcai_2020_full_res_data.h5`, equivalently the `..._cadaver_<acc>` directory. L1 the **CT** `PatientID`, first whitespace token only (`"18-2800 post opo".split()[0]`) | Key `deepfluoro:<accession>`. `ipcai_2020_ds_8x.h5` names the same six `01`–`06` and must be crosswalked, not parsed: 01=17-1882, 02=18-1109, 03=18-0725, 04=18-2799, 05=18-2800, 06=17-1905. `09_ftrac_fiducial` and `10_sawbones` are objects → refuse a person key | 366 registered frames; 2,545 vendor cadaver DICOM files (1,344 image frames, 6 files are multi-frame video) | **6** | no scheme; refused (correct). Downstream `realxray/deepfluoro/splits.json` already splits by specimen |
| **cobra** (COBRA 2026) | one `<centre><nnn>` case = one patient, on the dataset paper's authority ("A unique identifier was assigned to each case consisting of a center identifier followed by a three-digit case number, for example, D152"; 867 patients / 867 cases) | L2 the paper. L7 the case folder. No DICOM anywhere; `~/data/cobra2026/meta/<case>/metadata.yaml` carries only `ct.PatientAge`, `ct.PatientSex`, `ct.StudyDate` and no patient id | Key `cobra:<case id>`. Use (age, sex, date) as a **collision check only**, and only for centres A/B/C (347 cases, currently zero collisions) | 692 in the catalogue, 178 fetched, 145 in the four frame banks (+A004 in `cobra_elekta_smoke`, which is a 146th case); `pelvis_landmarks/cobra_elekta` carries the same 145-case `splits.json` while holding 130 | **145 (+1)** | refused (realxray banks not read) |
| **geneva_hip** | ONE object. `p01…p25` are 19 camera VIEWS of a single phantom (`README_2DDataset.md`) | L7 | Key `geneva_hip:phantom`. Corpus flag `test_only = true` — a split over one object carries no information | 116 frames | **1** | refused; `realxray/geneva_hip/splits.json` already has train 0 / val 0 / test 1 |
| **ljubljana** | ONE specimen: a cadaveric L1–L5 from one 80-year-old female (`Documents/Miccai2002_paper.pdf` §2) | L7 `pairs/manifest.json` `"spec": "LJ-L1L5"` | Key `ljubljana:LJ-L1L5`. `im000…im017` are views; the manifest field literally named `pid` (000–017) is the X-ray index, **not** a person | 18 X-rays, 1 CT, 1 MR; no bank yet | **1** | n/a |
| **devcorpus** | a TotalSegmentator v3 subject — not its own corpus | L5/L8 stem `<subject>_<k>_<pose>.npz`; `~/model_night/ts_clean_subjects.txt` (142); `STYLE_INFO.json` `val_subjects` (17) | Key `ts:<subject>` after the TS alias fold. Its 17 held-out subjects are the same people as `TS_s0585` / `totalseg_s0585_ap` / `totalseg_s0585_ap_p0` in five other banks | 142 subjects × poses × devices | **142** (ts corpus) | not in the keyer; the 17 held-out subjects sit unkeyed in up to 5 CT render banks |

---

## 3. THE ALIASES THAT MUST COLLAPSE

Ordered by people affected.

| # | alias | people affected | cases | status today |
|---|---|---|---|---|
| 1 | **BUU across banks.** `films_drr` / `films_drr_buucorr` (3,603 anns, LA) and `films_ap_drr` (3,600 anns, AP) carry the same 3,600 `patient_id`s — overlap 3,600/3,600, AP-only 0, LA-only 0. `films_ap_drr` is not among the keyer's roots | **3,600** | 10,806 | unaudited; collapses correctly *if* `films_ap_drr` is added as a root |
| 2 | **VinDr image vs study**, across three prefixes: `VINDR_vindr_<image_id>` (vindr_det_drr), `VINDRPS_<image_id>` (vindr_pseudo), `MEND_<image_id>` (mendeley_drr). 10,466 images → 5,000 studies; within `vindr_det_drr`, 158 studies over 368 cases | **2,882 phantom people** over the vindr family (2,879 keys today vs 2,658 studies across det+pseudo+mendeley = 221 phantom; 5,000 vs 10,466 corpus-wide) | ≥13,000 | image-level key; `VINDRPS_*` refused; a live 77.8 % val leak in `vindrps_fov96_ctx` |
| 3 | **CTSP cross-naming.** Four shapes for one person: `CTSP_COLONOG_<token>[_s<k>]`, `ctsp_<rel>_(ap\|lat)`, `ctsp_<rel>_(ap\|lat)_p<k>`, `ctsp_<rel>_<view>_p<k>_s<j>`. Token ≠ release id (release 0145 = token 100). Confirmed by CONTENT: the `ctsp_drr` render shape equals the `anchor_drr` `ctsp_<rel>_lat` shape 801/801, against 8/801 for a deliberately shifted pairing over 234 distinct shapes | **801** | 12,078 | `anchor_drr` and the `_s<j>` film banks refused; `ctsp_drr` ↔ `physics_drr` already collapses |
| 4 | **CTSP implant variants.** `implant_<rel>_v<k>_<view>` is the same person as `ctsp_<rel>_<view>`. `make_implant_ct.py:268` writes `<cid>_v<v>`; `make_anchor_drr.py:189` then seeds the split with `random.Random(cid)` on the variant-bearing stem — three independent draws for one person | **799** (558 in physics_drr) | 6,877 renders | **live leak**: 301 of 801 CTSP people are on both sides of `anchor_drr`'s own train/val split (e.g. `ctsp_0003_*` train, `implant_0003_v0_*` val, `implant_0003_v1_*` train). `anchor_det_v1` was trained on it |
| 5 | **NHANES third scheme.** `NHANESPS_C00160` / `NHANESPS_L00160` (nhanes_pseudo, 16,234 films, images byte-identical to the raw tiffs) = `NH_00160_c/l` = `NHANES_nhanes_cervical_00160`. The alias is written out in `tools/filter_pseudolabels.py:39` | **362 of 364** | 17,320 | `NHANESPS_*` refused; the c/l pair already collapses |
| 6 | **TotalSegmentator v2↔v3 renumber.** v201 `s1406…s1429` are byte-identical to v300 `s1463, s1504, s1641, s1725, s1736, s1775, s1785, s1806, s1834, s1854, s1932, s1933, s1943, s1951, s1997, s2036, s2040, s2060, s2073, s2119, s2123, s2133, s2137, s2139`; the vacated numbers were reissued to different people. Both halves of all 24 pairs are live across `ts_drr`/`anchor_drr`/`physics_drr` (v201) and `ts_drr_v3`/`anchor_drr_c2` (v300) | **24 split + 15 merged** | ~80 renders | `ts:s####` does both wrongs at once |
| 7 | **VerSe series vs subject.** 18 subjects own 37 series: verse400[090,155] 401[201,253] 402[202,251] 403[208,255] 404[209,256] 405[212,258,259] 406[214,261] 407[215,262] 408[223,265] 409[226,266] 410[227,267] 411[232,270] 412[235,290] 413[239,272] 414[241,273] 415[243,275] 416[247,279] 417[277,278] | **18 (19 phantom keys)** | ~200 renders | **live leak**: 5 patients on both sides of `allspine_v8_fov96_ctx` — verse401, verse406, verse407, verse408, verse416 — 367 of 3,502 VerSe val entries (10.5 %) against 269 train entries, and their labelled levels OVERLAP (verse214 labels 1–9 / verse261 7–22) |
| 8 | **VerSe `CTSP_VERSE_` prefix.** `ctsp_drr_obl` + `ctsp_drr_obl2` name 314 VerSe series `CTSP_VERSE_gl279_p0`; the same scans are `gl279_p0` in `verse_drr_obl`, `gl279` in `verse_drr`, `gl279_s0` in `verse_drr_film`, and in `verse_soft_drr` — 314/314 overlap with each | **312** | 3,767 + 4,857 | keyed as corpus `ctsp` today via the `patient_id` regex |
| 9 | **VerSe doubled prefix.** `glgl003…glgl146` (13 cases in `verse_drr`, byte-identical re-renders); `verse_drr/path/` additionally holds 344 `glverse*` byte-identical duplicates | 13 (+344 path entries) | 357 filenames | `verse_any` already collapses the 13 |
| 10 | **Mendeley redistribution.** 500 BUU laterals (16 of 16 Test images byte-identical to the BUU originals; 500 more confirmed at r = 1.0000 on 48×48 correlation, best non-match 0.9593) and 13 VinDr images | 500 buu + 12 vindr | 513 | BUU half already correct via `duplicate_of` + `patient_id`; VinDr half split |
| 11 | **FluoroCap route aliasing.** One article under `pmc:`, `art:s2_<sha1>`, `art:W<n>`, `art:oa_W<n>`, `art:ia_pubmed-PMC<n>`, `doi:` and an undocumented `url:` fallback | ≥4 documents by id + 13 by pixel union **[UNCERTAIN]** | ~40 panels | shipped `~/fluorocap_patient_keys.json` writes the PRE-merge key (1,214 keys), so even the 13 computed merges are absent from the file |
| 12 | **FluoroCap frame duplication.** 38 basenames byte-identical across `video_panels/` and `video_panels_med/`; a third family `panels/video_panels/<vid>_<frame>__<tag>__<letter>.png` under FLUO ids re-names 56 of 65; 93 (video, frame, window) triples carry 2–3 case names | 187 of 834 cases | 187 | absorbed for free by `yt:<video_id>`; refused entirely today |
| 13 | **FluoroCap panel vs video.** 834 video panels come from 338 videos — file-level keying misplaces 496 cases (59.5 %) | 338 | 834 | refused |
| 14 | **AASCE letter/date.** 440 films over 217 indices; 11 indices span two dates; 3 re-export pairs (`138_D_AP`/`138_D_AP2`, `142_A_AP`/`142_A_AP_(2)`, `159_A_AP`/`159_A_AP2`) | 217 groups | 440 | refused |
| 15 | **DeepFluoro fluoro `PatientID`.** Splits 17-1882 into 2, 18-0725 into 3, 18-1109 into 4, gives 17-1905 no accession at all (`E_64` / `Emergency^64`), and MERGES 18-2799 with 18-2800 on one file (`08_cadaver_18-2800/.../fluoro/dicom/0_1`, documented in the dataset Readme p. 13). CT `PatientID` also carries session suffixes (`18-2800 post opo`) | 6 of 6 | 2,545 files | refused; the registered pipeline already keys by specimen |
| 16 | **C-ArmLSpine case vs case_view.** `case101` (realxray `meta/`, `splits.json`) vs `case101_AP`/`case101_LAT` (`carm_drr` ann `case`, with `patient_id: case101`). Plus `case134/ori/` (302 XA frames, no `.dcm` extension, real `PatientID` `[withheld]` and real name `[withheld]`) which a `*.dcm` walk misses entirely | 148–149 | 296 + 240 + CV banks | refused |
| 17 | **devcorpus held-out subjects.** 17 TS v3 subjects in `P_pooled/val.txt` also appear as `TS_s0585` / `totalseg_s0585_ap` / `totalseg_s0585_ap_p0` in up to 5 CT render banks (6 of the 17 reach 5 banks, the other 11 reach 2) | 17 | ~170 | 2 of the 4 name forms unkeyable |
| 18 | **Byte-duplicate cases inside one release.** TS v300 `s1445`=`s1446` (and TS's own `meta.csv` puts them train/test), `s2107`=`s2109`=`s2110`, `s2093`≈`s2094`; BUU `0140`/`0719` and `0449`/`0629`; BUU `(1)` unzip collisions (3 reach `films_drr`) | ~8 | ~20 | none collapse |
| 19 | **Whole-bank subsets.** `fluorocap_drr_smoke` ⊂ `fluorocap_drr` (137, byte-identical ann and .npy); `vindr_pseudo_drr` ⊂ `vindr_det_drr` (744) **[CONFIRMED 2026-09-23, job 40416442: 744 of 744 image ids are in the 2,328]**; `films_drr_buucorr` = `films_drr` (identical 9,109 case names); `cobra_elekta*` × 4 share 145 ids; `carm_cv{0..4}_drr` restate the same 148 people with different split labels (up to 50 disagreements vs `carm_drr`) | — | ~11,000 | names match, so a name key catches them — but only if both banks are keyed at all |

---

## 4. WHAT REMAINS UNKNOWN

Per corpus. No guesses.

- **ctsp.** Whether two distinct TCIA PatientIDs are the same human (re-enrolment across the CT
  COLONOGRAPHY collection, or an overlap between the 768 numeric-id records and the 34 `CTC-` records
  that entered via the CTSpine1K subset). *What has been ruled out:* the same acquisition under two
  ids — over 1,728 CT-quality acquisitions, zero (origin, spacing, direction, nz) signatures are
  shared by two patients; 784 CTSpine1K COLONOG masks give 784 distinct (shape, affine) signatures
  with zero shared between a CTC mask and an OID mask; the six geometry hits across namespaces are
  all 1–2 slice localisers at scanner-default geometry, two of them matched by two different CTC
  patients at once. Voxel checks on the five candidate pairs differ substantially (e.g. 2,757,288 vs
  3,300,433 bone voxels >200 HU). TCIA's own API lists 825 distinct PatientIds in one collection,
  785 OID-style and 40 CTC-style, and `patient_db.json`'s 825 are exactly that set.
  *What would settle it:* TCIA confirming whether the numeric-id batch and the `CTC-` subset are
  disjoint subjects — one query or one email; or a body-habitus match of the 34 CTC CTs against the
  768 numeric CTs (34 feature extractions, one sbatch job), which is a heuristic with no calibrated
  threshold and would be weaker than TCIA's answer.
- **ts.** Whether two different scans in the release are one patient. TotalSegmentator ships no
  patient, accession or study field in either release, `descrip`/`db_name`/`aux_file` are empty on all
  3,167 volumes, and demographics cannot substitute — age is jittered between releases (992 of 1,228
  shared ids differ, ±4 years) and institute letters were remapped (I→J on 881, J→K on 8, with v3
  reusing `I` for a different institution). 43 v201 and 115 v300 groups share a full
  (age, gender, institute, study_type, scanner_model, kvp) tuple; the strongest candidate examined,
  v201 `s1304`/`s1314` (same shape, same x/y origin), is male 67 vs female 62 — not one person.
  *What would settle it:* nothing on disk. Only the TotalSegmentator authors could say.
- **verse.** `verse400`–`verse417` are grouping keys assigned by the organisers' demographics table,
  not hospital MRNs. If the table missed a repeat scan, this key silently splits that person and the
  data cannot detect it — 315 of 375 subjects sit in a (sex, age) bucket shared with another subject,
  so demographics cannot audit it. There is no DICOM under `~/VerSeFusion` and the NIfTI text header
  fields are null bytes. *What would settle it:* the TUM organisers.
- **nhanes.** Nothing material. The pickle `sample_id` is the corpus's own statement and the raw film
  numbers match the NHANES II sample-person sequence (ids sparse over 00156–27796 against 27,801
  enrolled; 7,375 of 7,406 lumbar ids also carry a cervical film, against ~2,591 expected if the two
  were independent enumerations).
- **buu.** Whether `0140`/`0719` and `0449`/`0629` are re-annotations of one patient or two patients
  photographed identically. The images are byte-identical and the report lists two rows with slightly
  different landmark coordinates. *What would settle it:* the KIOM authors, or a policy decision to
  merge on content (the safe direction).
- **vindr.** Whether one patient owns two `study_id`s. `PatientID`, `PatientName`,
  `AccessionNumber`, `StudyDate`, `StudyID` are absent from all 10,466 headers (27 distinct tags in
  total, no private tags). Within-study consistency is clean (0 of 5,000 studies disagree on age or
  sex), but only 791 studies carry weight AND size and those degenerate to 205 distinct tuples with
  mostly placeholder zeros. *What would settle it:* a cross-study pixel-duplicate scan over all
  10,466 images (submitted once as job 40415286 and cancelled at ~1,000 images, ~4 h projected) — or
  the VinDr authors.
- **mendeley.** Whether the 33 `Screenshot-2022-07-31-*` films are 33 people. They are 33 distinct
  images (distinct md5, no pair above r=0.95 against a corpus 99.9th percentile of 0.919), captured
  within about an hour with gaps as short as 7 s. `Dataset.zip` holds 714 jpg + 484 json + 214 txt
  and no README, CSV, manifest or DICOM. *Suggestive and unproven:* `MEND_N10-Olisthesis-L4-5-F-35-Yrs`
  and `MEND_N24-Olisthesis-L4-5-F-35-Yrs` share level, sex and age and correlate at 0.928.
- **aasce.** Whether an index is a person. Index 156 appears on 22-Nov-2016 and 29-Dec-2016, five
  weeks apart — a return visit or a reused index, undecidable from the files. Index 254 holds 16 films
  with Cobb 18.9°–67.2° and its `10-Jan-2017 A/B/C/D` do not read as one person when rendered at full
  size. The 99 `test/` images are anonymised to `01-July-2019-<n>.jpg` and cannot be checked against
  train at all. `download_sources.py:18` records AASCE as behind a request form and not reachable,
  so nothing beyond the images was ever fetched. *What would settle it:* the SpineWeb/AASCE
  organisers, or a radiologist reading the 16 films of index 254.
- **fluorocap.** Which patient a panel shows. `patient_identifier_present` = `no` on all 1,616 matched
  rows; PROTOCOL.md §11 states it. Only 119 of 1,616 panels have a caption naming a case number and
  only 13 keys name more than one distinct number (47 panels) **[UNCERTAIN — an earlier pass counted
  97/10/35 with the same regex; recount]**. Document keying therefore over-merges, demonstrably:
  `pmc:PMC10475679` covers a woman with a type-IIA fracture and a man with a type-IB, and
  `pmc:PMC11012415` covers cases 1–4. For YouTube, `yt:<video_id>` over-merges every lecture
  (`MWMYNnQ5E-g` spans 252–1462 s; 44 multi-frame videos exceed 300 s, 239 panels) and under-merges
  re-uploads (`Myv_AG9VYqI`/`xLFs6AhvoEQ` r=0.9998; 12 video-id pairs at native r≥0.98). At full bank
  scale, 170 video pairs share ≥5 dhashes and 37 share ≥20, with components of 3–5 ids — but
  same-channel components can be driven by shared intro frames, so 170 is a candidate count, not a
  verified same-patient count. `duplicate_groups.jsonl` (a dhash clustering) and the 0.98 thumbnail
  union disagree sharply (`FLUO-002925` vs `FLUO-008106`: same dhash group, r=+0.34), and the 0.98
  threshold is unjustified (0.95 → 16 merges, 0.99 → 8). *What would settle it:* nothing. Accept the
  over-merge as the safe direction and never report a patient count.
- **carmlspine.** Whether 149 cases are 149 people. The de-identification left nothing: `PatientID`
  empty on 59,307 of 59,609 instances, `PatientIdentityRemoved=YES`, `PatientBirthDate` a placeholder,
  UIDs regenerated per FILE. Ruled out: the same acquisition filed twice — all 296 frame PNGs have
  distinct md5s, all 149 CBCT volumes are distinct on an 8× hash, `(0029,0016)` is distinct across
  148 cases and shared by a case's two frames, and no two cases share (StudyDate, StudyTime).
  Against it: 149 cases fall on five dates (66 on 2023-12-11, 43 on 12-12, 38 on 11-18, 1 on 11-12, 1 on 11-11) at
  a median 224 s apart, console records were created in batches of 5–12 within a minute, and five
  cases carry hand-typed bare integers (`case145`='8', `case118`='10', `case33`='4', `case119`='12',
  `case69`='5') — so `(0029,0016)` is operator free text keying an ACQUISITION, not a person.
  *What would settle it:* the SMU authors. Conservative fallback available now: split on the five
  acquisition dates.
- **cobra.** For centres D (120), F (92) and G (133) every identity remnant is stripped, so nothing on
  disk can tell whether two case ids are one person; centre F has 15 sex+date collision groups
  (F054/F063/F153 all M, 20250922). A per-slice mean/bone-area signature over all 178 `ct_def.mha` has
  no discriminating power (top cross-case correlation 0.9927 was F018 vs C203, different centres).
  Case-level identity rests on the paper's 867 patients = 867 cases.
- **deepfluoro / geneva / ljubljana.** Nothing unknown that matters: 6 named cadavers, 1 phantom,
  1 specimen.
- **spinalai.** Nothing to know — no patient was ever radiographed.

---

## 5. FAILURE BEHAVIOUR

**Refusal stays.** A case whose corpus or person cannot be resolved must NOT be given a key, and must
NOT be treated as a unique person. That is the one thing the current file gets right, and it is why
`aasce_drr`, `anchor_drr` and `fluorocap_drr` showed up as a problem rather than as silent leakage.

Changes to how refusal is expressed and consumed:

1. **Refusals carry a reason code, not just a name.** Replace the flat `unmatched: [str]` with
   `refused: [{root, case, reason}]` where `reason` is one of `no_corpus`, `no_person`,
   `crosswalk_miss`, `table_miss`, `policy_non_person`. `crosswalk_miss` (a Dataset813 stem with no
   entry) must stay distinct from `no_person`, because it means a table is stale rather than a name
   being unknown.
2. **The keyer exits 0 with refusals; the split builder exits non-zero.** Keying is an audit and must
   complete over everything. `tools/make_context_crops.py` and any pooled list builder must abort if
   **any** case in the pool is refused, naming the first ten, and must abort if any key appears on two
   sides. The existing list builder already refuses to write when a CT subject or a real specimen
   falls on both sides; extend that to refusals.
3. **A corpus may be declared non-person and train-only.** `spinalai` (no person exists),
   `geneva_hip` and `ljubljana` (one object) get `person_key=false` / `test_only=true` in the bank
   registry. The splitter places the whole corpus on one side rather than refusing it. This must be a
   registry entry, never an inference from a case name.
4. **Keys are stored per `(root, case)`.** The current flat dict merged 161 case-name collisions
   between banks; within VerSe they happened to resolve to the same person, which is luck.
5. **A bank registry replaces the ad-hoc `--drr` list.** `tools/identity/banks.json`: one row per bank
   root with `corpus_default`, `release` (e.g. `ts:v201` vs `ts:v300` — the one fact no ann carries),
   `subset_of` (smoke/pseudo subsets), `person_key`, `test_only`. Release must come from here: all
   1,735 `ts_drr_v3` anns claim `TotalSegmentator_v201`. A bank not in the registry is refused whole.
6. **Frozen tables ship with the repo** so the keyer and its tests run off the grid:
   `tools/identity/ctsp_token_map.json` (802 rows), `tools/identity/ts_alias.json` (24 renumbers +
   3 dedup groups), `tools/identity/verse_series_to_patient.json` (374 rows → 355),
   `tools/identity/vindr_image_to_study.json` (10,466 rows), `tools/identity/fluorocap_doc_keys.json`
   (2,385 rows), `tools/identity/deepfluoro_h5_alias.json` (6 rows). Each carries `n_rows` and a
   sha256 of the source it was derived from, and the keyer refuses (`table_miss`) rather than falling
   through to a name when a table is absent or its row count has moved.
7. **Layer accounting is printed and stored.** `by_layer: {L1: n, …, L8: n}`. A rise in L8 between
   runs is the signal that a new bank arrived with no metadata, which is exactly the condition that
   produced every leak in this list.

Known-defective code to retire in the same change: the `patient_id`-first branch; the
`^([a-zA-Z]+)_?(\w+)$` normaliser (it turns `case101` into corpus `case` and `CTSP_VERSE_gl279` into
corpus `ctsp`); `CORPUS_OF["implant"] = "implant"`; the `_p\d+$` anchors on `ctsp_release`,
`ts_render` and `implant`; the `verse_any` suffix group `(?:_(?:lat|ap)_p\d+)?`; and
`("mendeley_film", r"^MENDELEY_mendeley_...")`, which matches nothing on disk — the stems are `MEND_*`.
Note that `buu_film`, `csxa_film` and `nhanes_film` are today **dead code**: `patient_id` returns
first on all 9,109 `films_drr` anns (`patient_keys.json` `by_scheme` = `{patient_id: 9109, …}`), so a
test that exercises those regexes is testing a path production never takes.

---

## 6. TEST PLAN

`tools/test_patient_keys.py`, extended in its present style: a table of
`(case, ann, root, expected key)`, then explicit collapse and separation assertions. Table-backed
cases are gated on the frozen tables in `tools/identity/` and fail loudly, never skip silently, when a
table is missing.

### 6.1 Fixtures

```python
CTSP  = {"COLONOG_100": "0145", "COLONOG_1": "0001", "COLONOG_378": "0533",
         "COLONOG_CTC-1018399231": "1121"}      # d813 stem -> release id
TOKEN = {"0145": "100", "0001": "1", "0533": "378", "1121": "CTC-1018399231"}
TSALIAS  = {("v201","s1418"): "s1943", ("v300","s1446"): "s1445",
            ("v300","s2109"): "s2107", ("v300","s2110"): "s2107",
            ("v300","s2094"): "s2093"}
VERSE = {"verse090": "verse400", "verse155": "verse400", "verse201": "verse401",
         "verse253": "verse401", "verse259": "verse405", "gl003": "gl003"}
VINDR = {"f2072260f8a9cd2c166e7795f8f28daa": "b830a545f876c6c79e417eb65da6e936",
         "f4dd04fb042aa0f4f7249283bc3972d8": "b830a545f876c6c79e417eb65da6e936",
         "41ad0981c920271384ffa541799842fe": "00403a30acf99250cfc4c56010be9ba0",
         "6299447e14a3392a1e3c75f06aa44005": "00403a30acf99250cfc4c56010be9ba0"}
```

### 6.2 Positive table (`case, ann, root, want`)

```
# ctsp — one person, every shape
("CTSP_COLONOG_100",            {},                                     "ctsp_drr",        "ctsp:100")
("CTSP_COLONOG_100_s0",         {},                                     "ctsp_drr_film",   "ctsp:100")
("ctsp_0145_ap",                {},                                     "anchor_drr",      "ctsp:100")
("ctsp_0145_lat",               {},                                     "anchor_drr_c2",   "ctsp:100")
("ctsp_0145_ap_p0",             {"scheme":"ctsp","source_case":"0145"}, "physics_drr",     "ctsp:100")
("ctsp_0145_ap_p0_s0",          {},                                     "physics_drr_film","ctsp:100")
("implant_0145_v0_ap",          {},                                     "anchor_drr",      "ctsp:100")
("implant_0145_v1_lat_p0",      {"scheme":"implant","source_case":"0145_v1"}, "physics_drr","ctsp:100")
("CTSP_COLONOG_CTC-1018399231", {},                                     "ctsp_drr",        "ctsp:CTC-1018399231")
# verse
("gl003",                       {},                                     "verse_drr",       "verse:gl003")
("glgl003",                     {},                                     "verse_drr",       "verse:gl003")
("gl003_p0",                    {},                                     "verse_drr_obl",   "verse:gl003")
("gl003_s0",                    {},                                     "verse_drr_film",  "verse:gl003")
("verse_scan-verse090_ap_p0",   {},                                     "physics_drr",     "verse:verse400")
("CTSP_VERSE_verse155_p0",      {"patient_id":"CTSP_VERSE_verse155"},   "ctsp_drr_obl",    "verse:verse400")
# ts — release comes from the root, never from ann["source"]
("TS_s1418",                    {"source":"TotalSegmentator_v201"},     "ts_drr",          "ts:s1943")
("TS_s1943",                    {"source":"TotalSegmentator_v201"},     "ts_drr_v3",       "ts:s1943")
("totalseg_s1418_ap",           {},                                     "anchor_drr",      "ts:s1943")
("totalseg_s0585_ap_p0_s0",     {"scheme":"totalseg","source_case":"s0585"}, "physics_drr_film","ts:s0585")
("TS_s1446",                    {},                                     "ts_drr_v3",       "ts:s1445")
("s0585_00_17-1882-015",        {},                                     "devcorpus",       "ts:s0585")
# nhanes
("NH_00160_c",                  {},                                     "nhanes_drr",      "nhanes:00160")
("NHANES_nhanes_lumbar_00160",  {"patient_id":"nhanes_00160"},          "films_drr",       "nhanes:00160")
("NHANESPS_C00160",             {"source":"NHANESPS"},                  "nhanes_pseudo",   "nhanes:00160")
# buu / csxa / mendeley
("BUU_FULL_buu_1673-F-064Y1",   {"patient_id":"buu_1673"},              "films_drr",       "buu:1673")
("BUU_FULL_buu_1673-F-064Y1(1)",{"patient_id":"buu_1673"},              "films_drr",       "buu:1673")
("BUU_FULL_buu_1673-F-064Y0",   {"patient_id":"buu_1673"},              "films_ap_drr",    "buu:1673")
("MEND_2662-F-044Y1", {"patient_id":"buu_2662","duplicate_of":"BUU_FULL_buu_2662-F-044Y1"},
                                                                        "mendeley_drr",    "buu:2662")
("CSXA_csxa_0001035",           {"patient_id":"csxa_0001035"},          "films_drr",       "csxa:0001")
# vindr — three prefixes, one study
("VINDR_vindr_41ad0981c920271384ffa541799842fe", {"patient_id":"vindr_41ad…"}, "vindr_det_drr",
                                                       "vindr:00403a30acf99250cfc4c56010be9ba0")
("VINDRPS_6299447e14a3392a1e3c75f06aa44005", {},        "vindr_pseudo",
                                                       "vindr:00403a30acf99250cfc4c56010be9ba0")
("MEND_f2072260f8a9cd2c166e7795f8f28daa", {},           "mendeley_drr",
                                                       "vindr:b830a545f876c6c79e417eb65da6e936")
# aasce / fluorocap / carm / deepfluoro / cobra / geneva / ljubljana
("AASCE_sunhl-1th-03-Jan-2017-165_A_AP", {},            "aasce_drr",      "aasce:165")
("AASCE_sunhl-1th-04-Jan-2017-165_C_AP", {},            "aasce_drr",      "aasce:165")
("AASCE_sunhl-1th-21-Nov-2016-138_D_AP2",{},            "aasce_drr",      "aasce:138")
("FLUO-013874", {"panel_path":"panels/ia_pubmed-PMC3488645/p003_x11__a.png"},
                                                        "fluorocap_drr",  "fluorocap:pmc:PMC3488645")
("FLUO-018669", {"panel_path":"panels/s2_367843b7db05be55c093f5b8407de635b5c86f50/p003_x11__a.png"},
                                                        "fluorocap_drr",  "fluorocap:pmc:PMC3488645")
("video_panels:dVBbXxjyaHk_00014__right",
   {"panel_path":"video_panels/dVBbXxjyaHk_00014__right.png"},
                                                        "fluorocap_drr",  "fluorocap:yt:dVBbXxjyaHk")
("FLUO-016377", {"panel_path":"panels/video_panels/9YHrICE2XgE_00115__left__a.png"},
                                                        "fluorocap_drr",  "fluorocap:yt:9YHrICE2XgE")
("case101_AP",  {"patient_id":"case101"},               "carm_drr",       "carmlspine:case101")
("case101",     {},                                     "realxray/carmlspine", "carmlspine:case101")
("17-1882_000", {},                                     "realxray/deepfluoro", "deepfluoro:17-1882")
("A002_ap",     {},                                     "cobra_elekta",   "cobra:A002")
("phantom_p07", {},                                     "realxray/geneva_hip", "geneva_hip:phantom")
```

### 6.3 Collapse assertions — one per confirmed alias in §3

```python
def same(a, b): assert key(*a) == key(*b), (a, b)

same(("BUU_FULL_buu_1673-F-064Y1", "films_drr"), ("BUU_FULL_buu_1673-F-064Y0", "films_ap_drr"))   # #1
same(("VINDR_vindr_41ad…", "vindr_det_drr"), ("VINDRPS_6299…", "vindr_pseudo"))                   # #2
same(("CTSP_COLONOG_100", "ctsp_drr"), ("ctsp_0145_ap", "anchor_drr"))                            # #3
same(("ctsp_0145_ap", "anchor_drr"), ("implant_0145_v0_ap", "anchor_drr"))                        # #4
same(("implant_0145_v0_ap", "anchor_drr"), ("implant_0145_v1_ap", "anchor_drr"))                  # #4
same(("NH_00160_c", "nhanes_drr"), ("NHANESPS_L00160", "nhanes_pseudo"))                          # #5
same(("TS_s1418", "ts_drr"), ("TS_s1943", "ts_drr_v3"))                                           # #6
same(("verse_scan-verse201_ap_p0", "physics_drr"), ("verse253", "verse_drr"))                     # #7
same(("CTSP_VERSE_gl279_p0", "ctsp_drr_obl"), ("gl279_p0", "verse_drr_obl"))                      # #8
same(("glgl017", "verse_drr"), ("gl017", "verse_drr"))                                            # #9
same(("MEND_2662-F-044Y1", "mendeley_drr"), ("BUU_FULL_buu_2662-F-044Y1", "films_drr"))           # #10
same(("FLUO-013874", "fluorocap_drr"), ("FLUO-018669", "fluorocap_drr"))                          # #11
same(("FLUO-016377", "fluorocap_drr"), ("video_panels:9YHrICE2XgE_00115__left", "fluorocap_drr")) # #12
same(("AASCE_sunhl-1th-10-Jan-2017-254_C_AP", "aasce_drr"),
     ("AASCE_sunhl-1th-11-Jan-2017-254_F_AP", "aasce_drr"))                                       # #14
same(("case101_AP", "carm_drr"), ("case101", "realxray/carmlspine"))                              # #16
same(("TS_s0585", "ts_drr"), ("s0585_00_17-1882-015", "devcorpus"))                               # #17
same(("TS_s1445", "ts_drr_v3"), ("TS_s1446", "ts_drr_v3"))                                        # #18
```

### 6.4 Separation assertions — the merges that must NOT happen

These are the half of the problem a collapse test cannot see. Each one is a named pair that today's
rule or a naive fix would wrongly join.

```python
def diff(a, b): assert key(*a) != key(*b), (a, b)

diff(("TS_s1406", "ts_drr"), ("TS_s1406", "ts_drr_v3"))          # 47M facial C1-C2 vs 3F thoracic
diff(("MEND_N24-Olisthesis-L4-5-F-35-Yrs", "mendeley_drr"),
     ("MEND_N24-S-64-M_1001_0", "mendeley_drr"))                 # 35F vs 64M, one patient_id today
diff(("CTSP_VERSE_gl279_p0", "ctsp_drr_obl"), ("CTSP_COLONOG_100", "ctsp_drr"))  # verse must not key as ctsp
diff(("CTSP_COLONOG_100", "ctsp_drr"), ("ctsp_0100_ap", "anchor_drr"))           # token 100 != release 0100
assert key("CTSP_VERSE_gl279_p0", "ctsp_drr_obl").startswith("verse:")
assert key("case101_AP", "carm_drr") != "case:101"               # degenerate corpus name
# 0_1 must follow its folder, not its header
assert key("deepfluoro/08_cadaver_18-2800/.../fluoro/dicom/0_1") == "deepfluoro:18-2800"
```

### 6.5 Corpus-level invariants (run against the frozen tables, no grid access)

```python
assert n_persons("ctsp")       == 801           # 0533 in no bank
assert n_persons("verse")      == 355
assert n_persons("ts")         == 1935
assert n_persons("nhanes")     == 364
assert n_persons("csxa")       == 4963
assert n_persons("buu")        in (3598, 3600)  # UNCERTAIN, see §2
assert n_studies("vindr")      == 5000
assert n_persons("deepfluoro") == 6
assert n_persons("geneva_hip") == 1 and corpus_flag("geneva_hip","test_only")
assert corpus_flag("spinalai", "person_key") is False
assert refused_count("aasce_drr") == 17         # the coronal* names only
assert refused_count("mendeley_drr") == 71
assert refused_count("anchor_drr") == 0         # was 7842
assert refused_count("fluorocap_drr") == 0      # was 2385
assert token_map_injective() and d813_crosswalk_bijective()
assert len(ts_alias()) == 24 and len(ts_dedup_groups()) == 3
```

### 6.6 Regression guards on live banks (run on the grid, not in CI)

```
# these are assertions about the world, not about the code; each has a job id in the record
allspine_v8_fov96_ctx : patient-level both-sides == 0        # currently 5 (verse401/406/407/408/416)
anchor_drr            : patient-level both-sides == 0        # currently 301 of 801 CTSP
vindrps_fov96_ctx     : val cases with a same-study sibling in train == 0   # currently 1,199 of 1,541
films_ap_drr          : every patient_id also present in films_drr, and one split side only
fluorocap_drr_smoke   : never split independently of fluorocap_drr
carm_drr + carm_cv*   : never pooled (up to 50 people disagree on split)
```

A test that only proves aliases collapse is half a test. The §6.4 block is the half that catches the
next `ts:s1406`.
