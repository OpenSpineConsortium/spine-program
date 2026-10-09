# Age and sex by source

Generated 2026-09-24 20:34:35 by `tools/age_sex_by_source.py` over the persons of the frozen G3 split (`split_final.json`, generated 2026-09-23 20:18:48). Persons, not images. Median [IQR] age in years; % female over persons with a recorded female/male sex.

| source | persons | with age | median [IQR] | with sex | % female | metadata file (sha256[:12]) |
|---|---:|---:|---:|---:|---:|---|
| CTSpinoPelvic1K (abdominopelvic CT) | 802 | 709 | 59 [52–63] | 738 | 53.3 | `manifest.json` (6f25aac0ea6f) |
| TotalSegmentator v2 and v3 (whole-body CT; scans) | 1,867 | 1,853 | 61 [44–73] | 1,852 | 42.5 | `ts_v300_meta.csv` (b9ca9a5ce940); `ts_v201_meta.csv` (83fa5844fc23) |
| VerSe 19/20 (spine CT) | 355 | 337 | 60 [49–73] | 337 | 51.0 | `verse_demographics.csv` (7b42cb3b4092) |
| CSXA (cervical lateral radiographs) | 4,963 | 4,963 | 36 [30–46] | 4,963 | 64.5 | `csxa_datasets.xlsx` (09e9ccf23005) |
| BUU-LSPINE (lumbar AP and lateral radiographs) | 3,598 | 3,598 | 57 [41–67] | 3,598 | 63.3 | `buu_KIOM2022_dataset_report.xlsx` (a0464bd22084) |
| NHANES II (lateral survey films): every sample person keyed in the split | 9,581 | 9,581 | 55 [37–65] | 9,581 | 51.8 | `nhanes2_DU5301.txt` (0abf548e2722); `nhanes2_DU5301.sas` (4cc8a3c105fe) |
| NHANES II: the 364 persons with released level annotations (the level-bank people of Table 1) | 364 | 364 | 65 [62–69] | 364 | 55.2 | `nhanes2_DU5301.txt` (0abf548e2722); `nhanes2_DU5301.sas` (4cc8a3c105fe) |
| VinDr-SpineXR (AP and lateral radiographs; studies) | 4,981 | 1,746 | 49 [38–59] | 4,913 | 62.3 | `vindr_age_sex.csv` (01db2b968774); `vindr_train.csv` (26733bb6bd5c); `vindr_test.csv` (c58df0b3ca33) |
| COBRA2026 (radiotherapy kV imager): all 692 public cases | 692 | 347 | 68 [58–75] | 319 | 43.9 | `cobra_meta_age_sex.txt` (4b5b01105a8f) |
| COBRA2026: the 145 Elekta cases the detector trained on | 145 | 115 | 66 [56–73] | 75 | 54.7 | `cobra_meta_age_sex.txt` (4b5b01105a8f); `cobra_elekta_splits.json` (85ecf8cbc373) |
| C-ArmLSpine (intraoperative mobile C-arm) | 149 | 0 | none | 0 | none | `idcensus_carmlspine.json` (3aa5cf44bbb4) |
| DeepFluoro (cadaveric specimens, mobile C-arm) | 6 | 0 | none | 0 | none | `idscan_deepfluoro.json` (99f7f75114e9) |
| Geneva hip (BV Pulsera, phantom) | 1 | 0 | none | 0 | none | none |
| Ljubljana 2D-3D-GS (PIXIUM 4600, cadaveric L1-L5) | 1 | 0 | none | 0 | none | none |

## Notes per source

- **ctsp** — Age and sex are the release manifest's per-record fields, populated where the source TCIA collection published them (descriptor: 393 female, 345 male, 11 'other', 53 none; age on 709). Ages of 89 are the TCIA top-code (n=31 at 89). 'other' is a recorded DICOM value and is excluded from the female/male denominator.
  - release manifest, fields age / sex per volume_id: `CTSpinoPelvic1K:data\zenodo_deposit\manifest.json` sha256 `6f25aac0ea6f4b46801d372f3d4762f05cd0dceb05da04ac73a3ad54dd427c55`
- **ts** — No patient identifier exists in TotalSegmentator; the person key is the canonical v3.0.0 scan id after the v2->v3 alias fold, so these are scans, not persons. meta.csv carries age (years, may be blank) and gender (m/f, blank on some rows); rows read: {'v3.0.0 meta.csv': 1939, 'v2.0.1 meta.csv': 1228}.
  - v3.0.0 meta.csv: `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\ts_v300_meta.csv` sha256 `b9ca9a5ce9407f9caad1d039c7574cba154efe93f3a5802bc1aed2e05a732922`
  - v2.0.1 meta.csv: `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\ts_v201_meta.csv` sha256 `83fa5844fc238c9453e64cddfee5964bc59bbdb994c274b8b931e948a44538ed`
- **verse** — VerSe organisers' demographics table (one row per subject; multi-series subjects verse400-417 fold to one row). Sex coded 0 = f, 1 = m in the column header.
  - verse_demographics.csv (subject, sex, age): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\verse_demographics.csv` sha256 `7b42cb3b409200cce95502c8e70f0d819bde173aebe62f2d3d369bddaf566a24`
- **csxa** — CSXA descriptor table 'Basic information': column 'Gender: female-1, male-0' and 'Age', one row per individual (Number = the 4-digit sequence in the file name). The table, not the file-name tail, is the source; the tail disagrees with it on 2 individuals (['0873166', '3556142']).
  - datasets.xlsx sheet 'Basic information': `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\csxa_datasets.xlsx` sha256 `09e9ccf23005dfbcc5eead7cf4dd66892197282af071ce976c57413608bc8c48`
- **buu** — BUU-LSPINE v1 dataset report, sheet Pos_LA (filename, gender, age; the AP sheet agrees). Person = the 4-digit case number; the two byte-identical case pairs of the split (0140/0719, 0449/0629) are one person each, so 3,598 persons for 3,600 cases. The report's own Summary sheet counts F 2280 / M 1320 over the 3,600 cases.
  - KIOM2022_dataset_report.xlsx sheets Pos_LA / Pos_AP: `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\buu_KIOM2022_dataset_report.xlsx` sha256 `a0464bd220849b4f41573a925efb08e27d772f9ae53990e78d483a6b96b19c62`
- **nhanes** — NHANES II releases no demographics with the films; the SEQN in the file name (CDC: 'can be used to access data from the main NHANES II public use datasets') joins tape 5301 (Anthropometry, examined persons), cols 1-5 SEQN, col 55 Q4 SEX, cols 190-191 AGE YEARS AT EXAMINATION (layout from DU5301.sas). Sex code 1 = male, 2 = female, checked by median standing height at 25+ years: code 1 1743 mm, code 2 1608.0 mm (consistent). Ages are integer years at examination; the survey enrolled to 74 years at interview, so age at examination tops out at 75.
  - CDC NHANES II tape 5301 data (DU5301.txt): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\nhanes2_DU5301.txt` sha256 `0abf548e27225f1568f45e587e776f110cba8a75ab32f5d6840c2bd5da8c9a21`
  - CDC layout DU5301.sas: `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\nhanes2_DU5301.sas` sha256 `4cc8a3c105fe1013b0f5c9a8e0ea0ea839bee950671910bf647e05e6904e2665`
- **nhanes_annotated** — Subset of the row above: the sample persons whose films carry the Zenodo 10223910 annotations (543 films; these are the NHANES persons in the level bank and in Table 1).
  - CDC NHANES II tape 5301 data (DU5301.txt): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\nhanes2_DU5301.txt` sha256 `0abf548e27225f1568f45e587e776f110cba8a75ab32f5d6840c2bd5da8c9a21`
  - CDC layout DU5301.sas: `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\nhanes2_DU5301.sas` sha256 `4cc8a3c105fe1013b0f5c9a8e0ea0ea839bee950671910bf647e05e6904e2665`
- **vindr** — PatientAge / PatientSex read from every DICOM header (job 40438307); person = StudyInstanceUID. Raw PatientSex values over images: {'F': 6499, 'M': 3837, 'O': 128, 'U': 2}; studies whose images disagree on age or sex: 0.
  - per-image PatientAge/PatientSex from the DICOM headers (job 40438307): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\vindr_age_sex.csv` sha256 `01db2b968774f2795b8538b19f2518556d646102002ed1997f81211c7d718a2a`
  - release annotations/train.csv (image -> study): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\vindr_train.csv` sha256 `26733bb6bd5cc03a9267a944a9d1678e82c650bbc90c5db0b1abbef3f6e8c34b`
  - release annotations/test.csv (image -> study): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\vindr_test.csv` sha256 `c58df0b3ca3363238e657402b502f2537c7d674ff0a9f067e0a510ae5a144918`
- **cobra** — COBRA2026 ships no DICOM but a metadata.yaml per case whose ct block carries PatientAge and PatientSex (and StudyDate). Over the 692 public cases the raw PatientSex values are {'F': 140, 'M': 179, 'U': 120, 'null': 253} ('U' = unknown, not counted as a recorded sex) and the age field is {'int': 120, 'NNNY': 227, 'null': 345} (integer years, 'NNNY', or null). The Results sentence's 'no age or sex is released for the radiotherapy set' is therefore not true of COBRA: it releases them for about two thirds of cases.
  - grep of PatientAge/PatientSex/StudyDate over meta/<case>/metadata.yaml (692 cases): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\cobra_meta_age_sex.txt` sha256 `4b5b01105a8fbb315ca180b5376354b8cb523b7bf27030bf32d156a0e423ec6b`
- **cobra_detector** — Subset of the row above: the case ids of realxray/cobra_elekta/splits.json (train/val/test).
  - grep of PatientAge/PatientSex/StudyDate over meta/<case>/metadata.yaml (692 cases): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\cobra_meta_age_sex.txt` sha256 `4b5b01105a8fbb315ca180b5376354b8cb523b7bf27030bf32d156a0e423ec6b`
  - realxray/cobra_elekta/splits.json: `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\cobra_elekta_splits.json` sha256 `85ecf8cbc373cbda2e4cdfeb7448ff539f4852aa9b8be085a3baa98f959bfb0b`
- **carmlspine** — None released. Tag census over 58,911 DICOM files of 149 cases: PatientSex top values [['', 58312], ['M', 426]] (4 distinct), PatientBirthDate top values [['20200101', 58312], ['20231112', 304]] (a 2020-01-01 placeholder on 58,312 files); no PatientAge tag. The residual 'M' on a few hundred files is not a per-case field and is not used.
  - DICOM tag census (idcensus_carmlspine.json): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\idcensus_carmlspine.json` sha256 `3aa5cf44bbb4c89d62777f23f8ae151d68e8d5ecf2ad5aa5c9dcc6a71ea19397`
- **deepfluoro** — None released. The vendor DICOMs carry placeholders: CT PatientAge {'022Y': 81, '000D': 3} on every object including the sawbones and the fiducial phantom, fluoro PatientAge 000Y, and a PatientSex that is 'F' on the sawbones and 'O' on the fiducial (fluoro values over all objects: {'M': 859, 'O': 366, '': 647, 'F': 787}). Not usable as specimen age or sex.
  - DICOM tag census per specimen (idscan_out/deepfluoro.json): `spinesurg-ct-nnunet:SchwingNet\results\age_sex_cache\idscan_deepfluoro.json` sha256 `99f7f75114e99c066897488b8f3635faca4eed8267dc4c50692ad508e9a834e1`
- **geneva** — One phantom (the 19 split keys are camera views of one object); no person, no age or sex.
- **ljubljana** — One specimen; nothing in the release files. The accompanying paper describes it as from an 80-year-old female; that is a statement in a paper, not released metadata, and is not counted here.

## Not rows here
- CTSpine1K is not a Table 1 source: CTSpinoPelvic1K's records were drawn from its COLONOG series and the CTSP manifest carries the demographics; nothing is trained on CTSpine1K directly.
- FluoroCap, Mendeley-716, AASCE, Spinal-AI2024 and lateral_236 are excluded from the release or used by no trained component (Table 1 footnote k); none releases age or sex.
- lat236 (236 films, in the split, in no live bank) and AASCE key to films, not persons; no metadata.
