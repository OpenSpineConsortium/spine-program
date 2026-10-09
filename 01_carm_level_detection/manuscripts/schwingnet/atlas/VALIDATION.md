# Validation of the ATLAS cards

Run: `python SchwingNet/atlas/validate_cards.py` from the repository root (2026-09-22; rerun 2026-09-23 after
`update_cards_2026-09-23.py` brought both cards to the six-figure manuscript: 0 errors, 5 warnings, the same five;
rerun 2026-09-24 after `update_cards.py` removed five duplicate references per card and the validator gained a
duplicate-reference check, which the 2026-09-23 cards fail with 20 errors: 0 errors, the same 5 warnings).

Result: **0 errors, 5 warnings** for `model.json` and `dataset.json` together.

## What was checked

Against the 2025-11 schema summary recorded in the task brief (the live schema was not fetched):

- both files parse as JSON; `$schema` is the 2025-11 model / dataset URL;
- required fields: `Name` (4-256 chars) and `Link` (a URI) — present in both; `Summary` <= 2,500 chars
  (model 2,017; dataset 1,810);
- every key in every object is one the summary lists (the real schema has `additionalProperties: false`
  everywhere): root, Indexing, Descriptors, Authors, Organizations, References, Date, License, Model
  properties, Output, Regulatory information, Use, User, EHR compatibility, Imaging, Procedures, Model
  performance, Dataset properties, Partitions, Total, Subsets;
- enum values: `Use.*` in {Detection, Decision support, Image processing, Other}; `User.*` in {Physician,
  Subspecialist diagnostic radiologist, Interventional radiologist, Radiology technologist, Researcher};
  `File format` in {DICOM, JPEG, NiFTI, PNG, Other}; `Model performance.Metrics` in {accuracy, sensitivity,
  F1 score, other}; `Burned-in PHI` in {Yes, No, Unknown}; `Partition` in {Training, Optimization,
  Validation, Internal testing, External testing, Tuning, Hold-out, Development, Test, Other};
- `Date.*` and `References[].Date` are YYYY-MM-DD or a year; `Content` codes are two capital letters;
  `RadLex` entries match `RID\d+`; `SNOMED` entries are ints; keywords are 2-64 chars; `CDEs` match
  `RDE\d+`; `FDA cleared` / `CE marked` are booleans; count fields are non-negative ints; `Age range` is
  `[[value, unit], [value, unit]]`.

Also checked by grep: the cards contain no banned word, no product name, no regulatory pathway name and no
mention of the counting heuristic evaluated in docs/ANOMALY_RULE_EVALUATION.md.

## Fields whose enum value could NOT be confirmed

These are correct in form but their exact vocabulary was not verified against the live schema or an
external terminology server in this session. A reviewer should confirm them before submission.

| file | field | value used | why unconfirmed |
|---|---|---|---|
| both | `Imaging.Modalities[]` | `"Fluoroscopy (RID10361)"` | RadLex RID recalled from memory; not verified against radlex.org |
| dataset | `Imaging.Modalities[]` | `"Computed tomography (RID10321)"` | same |
| dataset | `Imaging.Modalities[]` | `"Radiography (RID10345)"` | same |
| dataset | `Imaging.Modalities[]` | `"Cone-beam computed tomography"` | given by name only; RID not known to me with confidence |
| both | `Imaging.Procedures[].Name` | free text | no RadLex `RPID` and no LOINC code supplied; the schema summary lists them as optional |
| both | `Indexing.Content` | `["MK", "NR"]` | RSNA two-letter content codes chosen by the card author; the summary gives them only as examples |
| both | `Indexing.RadLex`, `Indexing.SNOMED` | `[]` | left empty rather than guessed |
| model | `Model properties.Use.*` and `User.*` | values listed above | the summary says the enum contains values "such as" these; other members of the enum may exist, and `Excluded` was filled with the same values as `Out-of-scope` on the assumption that both accept the same enum |
| model | `Model properties.EHR compatibility` | `{"Other": ...}` only | the enum of `List` is not in the summary, so `List` was omitted |
| model | `Model performance.Metrics` | `["accuracy", "sensitivity", "other"]` | the summary gives these as examples ("e.g."); the full enum was not seen |
| model | `Regulatory information.Authorization status` | free text | the summary does not say whether this is an enum or free text |
| both | `Descriptors.Date.Created` / `Updated` | `"2026-09-22"` / `"2026-09-23"` | format per the summary; the schema may require a full date rather than a year, which this satisfies either way |
| dataset | `Partitions[].Total.Sex` / `Demographic` / `Criterion` | free text | the summary does not state their types; strings were used |
| dataset | `Partitions[].Total.Age range` unit | `"years"` | the unit vocabulary is not in the summary |
| dataset | `Partitions[].Partition` | `"Tuning"` for the detector's checkpoint-selection sets and `"Optimization"` for the device-card fitting frames | both are enum members; whether ATLAS intends them this way is a judgement |
| dataset | `Imaging.Burned-in PHI` | `"Unknown"` | an enum member; chosen because no frame-by-frame audit exists |

## Things a schema check cannot see, stated here so they are not silently wrong

- `Patient count` is omitted, not zeroed, wherever a corpus cannot give one (C-ArmLSpine, FluoroCap,
  TotalSegmentator persons, AASCE). The Geneva subset carries `Patient count: 0` because it is a phantom.
- The `Tuning` partition's `Patient count` (27) counts COBRA cases only; the DeepFluoro specimen is a cadaver
  and is in `Exam count` (28), not in the patient count.
- The `Training` partition for the level bank reports crops (31,396), not films; the subsets' `Patient
  count` values are corpus-level upper bounds from `docs/PATIENT_IDENTITY_SPEC.md` §6.5, not the number of
  people behind those crops, and the card says so in each `Comments`.
- The TotalSegmentator age range `[0, 118]` is what the v3.0.0 `meta.csv` records for the 142 subjects; the
  release jitters ages and the two extremes are almost certainly artefacts of that, but they are reported as
  released rather than trimmed.
- The detector numbers (2026-09-23) are the manuscript's: whole-vertebra boxes at the cross-device confidence 0.74
  (`results/a1.json`), with the 0.25 figures beside. The vertebral-body convention, under which the same predictions
  read far lower (the 2026-09-22 card quoted it as the headline), is named as a pending recompute (G5), not quoted.
- The 2026_269 IRB determination (an image-only scan) was read page by page on 2026-09-23: the WSU IRB
  Administration Office's signed notice of 2 September 2026, HPR Number 2026-269, not human participant research.
  Its scope excludes any source behind a data use agreement; VinDr-SpineXR (PhysioNet Restricted Health Data Use
  Agreement) is therefore outside it, and both cards say so. No schema check can see this; it is an author decision.
