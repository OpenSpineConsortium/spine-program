# Protocol: a scoping review of publicly described human spine CT and projection-radiography datasets, with programmatic access verification and a download recipe

**Protocol version 1.0 — frozen 2026-09-19, before any search is executed.**
Reporting standard: PRISMA-ScR (Tricco 2018), structured after the JBI Manual for Evidence
Synthesis, chapter 10 (scoping reviews), with Cochrane Handbook practice for search reporting,
duplicate screening and the analysis plan. Registration: the frozen protocol is deposited on the
Open Science Framework (Registries, "Generalized Systematic Review Registration" template) before
the first search runs; the registration DOI is entered in the deviations log (section 17) and in
the manuscript. PROSPERO does not accept scoping reviews, so it is not used.

Companion documents in this directory, all part of the protocol and frozen with it:

| File | What it fixes |
|---|---|
| `information_sources.md` | every source, endpoint, authentication, rate limit, paging cap, and the verbatim query string(s) |
| `charting_schema.json` | the charting form as a JSON Schema (draft-07); one record per dataset |
| `quality_rubric.md` | ten items scored 0/1/2 with the rule for each score, and the "fit for level identification" rule |
| `statistical_analysis_plan.md` | every analysis, its inputs, its estimator, and the file each number is written to |
| `PRISMA-ScR_checklist.md` | the 27 reporting items and where each is reported |

---

## 1. Background and rationale

Vertebral level identification from a limited field of view — the problem this group works on
in fluoroscopy and radiography — depends on training and test data in which the level names are
right, the origin of each label is known, and variant anatomy (a sixth lumbar vertebra, a
thirteenth rib-bearing vertebra, a lumbosacral transitional vertebra) is labelled rather than
silently normalised. The group already uses CTSpinoPelvic1K, VerSe, TotalSegmentator, NHANES II,
BUU-LSPINE, CSXA, VinDr-SpineXR, AASCE and a literature-mined fluoroscopy collection (FluoroCap),
and has repeatedly found a relevant dataset only after a model had been trained without it.

No published enumeration of spine CT and radiograph datasets states, for each one, how its
annotations were produced, whether variant anatomy is labelled, what the licence permits, and
whether the data can actually be downloaded today. Existing lists (dataset roadmaps, challenge
overviews, "awesome" lists) are unsystematic, undated, and do not verify access. Whole-spine
radiographs and thoracic-spine images are the scarcest class and the most valuable for the
frame-stitching work, so a review that finds even a few more matters.

## 2. Objectives and review questions

Primary questions (each answered per dataset and in aggregate):

- **RQ1** What publicly described datasets of human spine CT and projection radiography exist
  (2000–2026), with or without annotations?
- **RQ2** How is each annotated — per-vertebra level names, segmentation, landmarks or boxes,
  pathology labels, none — and what is the origin of the annotation (expert manual, model
  generated, counting inferred, report derived, other)?
- **RQ3** Is variant anatomy (L6, T13, LSTV) labelled, and with what counts?
- **RQ4** Under what licence is each released?
- **RQ5** What is the access route today, established by a recorded probe: open download,
  registration, data-use agreement, request to authors, unavailable, commercial?

Secondary objectives:

- **SO1** Score each dataset on a predefined ten-item quality rubric and a boolean fitness rule
  for level identification.
- **SO2** Pool what can be pooled: counts by modality, region, annotation type and origin, access
  route and licence tier; pooled prevalence of L6, T13 and LSTV where per-subject counts are
  reported; pooled inter-rater agreement where three or more datasets report a comparable
  statistic; the share of datasets described as public that actually download.
- **SO3** Produce a download recipe for every dataset with an open-download or registration route,
  a manifest of every dataset with its route, and a stub for a patient-grouped split.
- **SO4** Report which included datasets are already on the authors' compute grid.

The review is first a review with predefined methods. The recipe is a product of the charting
records, not the reason for the eligibility criteria.

## 3. Design

Framework (JBI "PCC"):

- **Population**: images of the human spine (any region, any age).
- **Concept**: a dataset — a named, bounded collection of subject-level images, with or without
  annotations, that has a description someone else can read.
- **Context**: CT (including cone-beam CT) and projection radiography (plain radiograph,
  fluoroscopy / C-arm, DXA vertebral fracture assessment, EOS biplanar); described in a journal
  article, preprint, challenge page or repository record dated 2000–2026; any language; any
  country.

Unit of analysis: the dataset. Records (articles, preprints, repository entries, challenge pages)
are the unit of screening; several records may describe one dataset and one record may describe
several datasets. The record-to-dataset mapping is explicit (section 7.6).

## 4. Eligibility criteria

All criteria are decided on the record's title, abstract or description, and on the dataset's
own documentation when the record points to it. Each criterion has a code that is recorded in
the screening CSV. A record is included when every I-criterion holds and no E-criterion holds.

### 4.1 Inclusion

| Code | Criterion | Decision rule |
|---|---|---|
| I1 | Human spine imaging | The description says the images show the human spine or a named vertebral region (cervical, thoracic, lumbar, sacrum, whole spine), or the spine is a labelled structure in a body-region dataset (e.g., a whole-body CT dataset with vertebra masks). Datasets of chest or abdomen CT with no spine annotation and no spine-specific description are **not** included merely because vertebrae appear in the field of view. |
| I2 | Modality | At least one of: CT, CBCT, plain radiograph (CR/DR/film), fluoroscopy or C-arm frames, DXA vertebral fracture assessment images, EOS biplanar radiographs. Multi-modal datasets are included when at least one eligible modality is present; the ineligible modalities are recorded but not counted. |
| I3 | Size | At least 10 distinct subjects (patients or, for figure-derived collections, source articles as a proxy when the subject count is not stated). "At least 10" is read from the description; when only an image count is given and the subject count is unknown, the record passes to charting with `n_subjects_basis = unknown`. |
| I4 | Described | At least one of: journal article, preprint, challenge web page, data-repository record (Zenodo, Figshare, PhysioNet, TCIA, Kaggle, Hugging Face, GitHub, institutional repository). A bare download link with no text describing the content fails I4. |
| I5 | Date | The earliest describing record is dated 2000-01-01 to 2026-12-31. |
| I6 | Annotation status | Any: with annotations or without. |
| I7 | Figure-derived collections | Collections assembled from published figures (e.g., from PMC, Open-i, MultiCaRe, Open-PMC-18M, Wikimedia Commons) are eligible when I1–I5 hold and are flagged `figure_derived = true`. |
| I8 | Derived datasets | Datasets built by re-annotating, re-labelling, subsetting or converting another public dataset are eligible, flagged `derived = true`, with the parent recorded in `parent_ids`. |

### 4.2 Exclusion

| Code | Criterion | Decision rule |
|---|---|---|
| E1 | MRI only | No eligible modality is present. |
| E2 | Non-human | Animal, veterinary or comparative-anatomy imaging. A dataset that mixes human and animal subjects is included with the human count only if it is stated; otherwise excluded. |
| E3 | Phantom or cadaver only | All images are of phantoms, cadavers, ex-vivo specimens or printed models. A dataset that mixes living subjects and cadavers is included with the living count. |
| E4 | Purely synthetic | Images generated (DRR, GAN, diffusion, simulation) with no public parent CT or radiograph dataset. Synthetic datasets rendered from a public parent are included as `derived`. |
| E5 | Single case | Fewer than 10 subjects (see I3). |
| E6 | Not subject-level images | The release contains only extracted features, measurements, embeddings, reports or metadata without the images. |
| E7 | Duplicate | The record describes a dataset already represented by another included record (versions of one dataset collapse to one dataset with the versions listed; a derived dataset is not a duplicate of its parent). |
| E8 | Not a dataset | The record is a method paper that uses a private dataset without describing it as available, or a review, editorial, protocol, or a model/software release without images. A method paper that describes and releases its data passes. |

### 4.3 Operational definitions

- **Subject**: one person. Where a description reports "scans" or "studies" and not subjects,
  `n_subjects` is null and `n_images_or_volumes` carries the count with its unit.
- **Described as public**: the record states the images are publicly, freely or openly
  available, or gives a repository DOI or URL for the images. This is recorded independently of
  the access probe so that the two can be compared (SAP section 6).
- **Annotation origin** categories: *expert-manual* (drawn or named by a clinician or trained
  annotator, whatever the tool); *expert-corrected-model* (model output corrected by an expert);
  *model-generated* (uncorrected model output); *counting-inferred* (level names assigned by
  counting from a landmark such as C2 or the sacrum rather than by direct reading);
  *report-derived* (labels parsed from radiology reports); *crowd-or-trainee* (non-expert
  annotators without documented expert review); *caption-derived* (labels parsed from figure
  captions); *unknown*; *none*.
- **Variant anatomy**: L6 = a sixth lumbar-type vertebra; T13 = a thirteenth rib-bearing
  vertebra; LSTV = lumbosacral transitional vertebra (Castellvi types I–IV or equivalent,
  including sacralisation and lumbarisation). "Labelled" means present per subject in the
  released labels or metadata; "reported" means counts appear in text only.

## 5. Information sources

All sources are queried by code with the exact query string, endpoint, timestamp and hit count
recorded. The full table — endpoint, authentication, rate limit, paging cap, syntax notes and the
verbatim query per source — is `information_sources.md`. Summary:

- **Literature indexes (7)**: PubMed (E-utilities), Europe PMC, OpenAlex, Semantic Scholar,
  arXiv, bioRxiv/medRxiv, Crossref.
- **Data repositories and indexes (14)**: Zenodo, Figshare, Dryad, OSF, Mendeley Data, DataCite,
  PhysioNet, TCIA/NBIA, Kaggle, Hugging Face, grand-challenge.org, GitHub, Papers with Code,
  OpenDataLab.
- **Figure-derived routes (8)**: NLM Open-i, MultiCaRe, Open-PMC-18M, Wikimedia Commons,
  J-STAGE, KoreaMed Synapse, SciELO, Redalyc. These serve two purposes: each is itself a
  candidate figure-derived dataset (charted under I7 with its spine subset counted), and the
  hit counts quantify the size of the figure-derived pool by modality (SAP section 4.4).
- **Other methods**: the known-item set (section 6.4); reference lists and "related datasets"
  sections of every included data descriptor and of any review of spine imaging datasets found
  by the searches (one round of backward chasing, recorded per record as `found_via`).

Sources considered and excluded, with reasons: Google Dataset Search (no API; terms of service
forbid automated querying), YouTube, Instagram, Reddit, Flickr, Facebook (media platforms, not
dataset sources; images there are not datasets under I4), Common Crawl (a web crawl, not a
dataset index; screening it is not reproducible at record level), patents (describe methods, not
released datasets). Google Scholar is excluded for the same reason as Google Dataset Search.

## 6. Search strategy

### 6.1 Concept blocks

Every query is the conjunction of three blocks, translated into each source's syntax:

- **Block S (spine)**: spine, spinal, vertebra/vertebrae/vertebral, lumbar, thoracolumbar,
  lumbosacral, "cervical spine", "thoracic spine", scoliosis, spondylolisthesis. *Cervical* and
  *sacral* alone are not used (cervix; sacral nerve stimulation); *scoliosis* and
  *spondylolisthesis* are included because their radiograph datasets often omit the word
  "spine" from the title.
- **Block M (modality)**: "computed tomography", CT, radiograph*, X-ray(s), roentgen*,
  fluoroscop*, C-arm, DXA, DEXA, "vertebral fracture assessment", EOS, biplanar. MRI is not in
  the block; MRI-only records fail E1 at screening.
- **Block D (dataset)**: dataset(s), "data set(s)", database, benchmark*, challenge, "publicly
  available", "public data", "open data", "open source", "data descriptor", corpus, "image
  collection". "Segmentation" and "annotated" are deliberately not in Block D: they retrieve the
  whole method literature; the datasets those methods release are reached through Block D terms
  in their abstracts, through the repository sources, and through backward chasing.

Sources that do not accept boolean queries (Crossref, Dryad, OSF, GitHub, Hugging Face, Kaggle,
Open-i, Commons, J-STAGE, KoreaMed, SciELO, Redalyc) receive a fixed list of term pairs drawn
from S × M (and S × D where the source is a dataset index), enumerated in
`information_sources.md`; the union of their results is deduplicated. Sources with no query
interface (bioRxiv/medRxiv, PhysioNet, TCIA collection list, MultiCaRe, Open-PMC-18M) are
harvested in full over their listing endpoint and filtered locally with the prescreen regexes
(section 7.2), which is recorded as the "query".

### 6.2 Limits

Date 2000–2026 where the source supports it, else applied locally. No language limit. No
document-type limit at search time, except that repository searches are restricted to dataset
records where the source has such a type and a second, unrestricted pass is run for
repositories known to type datasets inconsistently (Zenodo, Figshare).

### 6.3 Recording

For each query execution: source, query_id, verbatim string as sent, endpoint URL (secrets
removed), parameters, retrieval timestamp (UTC), reported total, number retrieved, paging cap
reached (yes/no), credential used (name only, never the value). Raw responses are cached by SHA-1
so the run can be replayed offline. The search is run once for the review, on a date recorded as
`--run-date`, and rerun once before submission; differences between runs are reported as a
search-update in the flow diagram.

### 6.4 Search validation: the known-item set

Before the search runs, a set of datasets already known to the authors is frozen (section 16).
After the search, known-item recall = share of the set retrieved by at least one automated
source. A recall below 0.80 triggers a documented revision of the query strings (deviations log)
and a rerun; the known items are included through the "other methods" arm regardless, so recall
measures the search, not the review. The set is not used to tune the prescreen regexes after
they are frozen.

## 7. Selection of sources of evidence

### 7.1 De-duplication of records

Records are merged when any key matches, in this order: DOI (lower-cased, prefix stripped);
PMID; PMCID; arXiv id (version stripped); Zenodo concept DOI (versions collapse); normalised
title (lower-case, ASCII-folded, alphanumerics only) plus first-author family name normalised
the same way, requiring exact equality. Fuzzy title matching is not used; near-duplicates that
survive are caught at screening under E7. The retained record keeps every source and query_id
that found it (`found_via`), which is what the per-source flow counts are computed from.

### 7.2 Rule-based prescreen (recorded, not final)

Each deduplicated record's title + abstract + description is tested against three
case-insensitive regexes (Appendix A). A record passes when all three match. Passing records go
to human screening. Failing records are not screened, except a simple random sample of 200
failing records (seed 20260919) that one reviewer screens blind to the prescreen outcome; the
sample's inclusion rate estimates the prescreen false-negative rate and is reported with a
Wilson interval. Records from sources harvested in full (section 6.1) are prescreened the same
way, and for them the prescreen is the search.

### 7.3 Human screening

Title/abstract/description screening by one reviewer against I1–I8 and E1–E8, recording one
decision (include / exclude / unclear) and one or more criterion codes per record in
`screening/decisions.csv` (columns: record_id, reviewer, date, decision, codes, reason_free_text,
llm_suggestion, llm_agreed). A second reviewer independently screens a simple random 10 % of
prescreen-passing records (minimum 100; seed 20260919); Cohen's kappa is reported and
disagreements are resolved by discussion, with the resolution recorded. "Unclear" records go to
description review (7.5).

### 7.4 LLM-assisted step

An LLM may propose a decision and criterion codes for each record before the human decides. The
step is named as such in the manuscript; the model identifier, the prompt template (hash and
full text), and every input and output are stored under `screening/llm/`. The human decision is
recorded independently and the agreement between the LLM suggestion and the human decision is
reported. The LLM never makes a final decision, never charts a field without a human verifier,
and is not used on the 10 % dual-screened sample's second reviewer.

### 7.5 Description review

For every record marked include or unclear, the reviewer reads the dataset's own documentation
(repository landing page, README, data descriptor full text where open). Full text is obtained
through the record's open-access link or Unpaywall (contact e-mail from the credential store);
paywalled articles are read through the institution's subscription when available; when no
full text can be obtained, the record is charted from its abstract and repository record and
`notes` says so.

### 7.6 Record-to-dataset mapping

Included records are clustered into datasets by: identical dataset name or alias; identical data
DOI or repository URL; or an explicit statement that one record describes another's dataset.
Each dataset receives an `id` and the list of `record_ids` behind it. Versions of one dataset
(VerSe'19 and VerSe'20; TotalSegmentator v1 and v2) are one dataset with versions listed in
`aliases` and `notes`, unless the versions differ in subjects by more than 50 %, in which case
they are separate datasets linked by `parent_ids`.

### 7.7 Flow

Counts are reported in a PRISMA 2020 two-arm flow diagram: records per source → after
deduplication → prescreen pass/fail → screened → excluded by code → description review →
excluded by code → included records → datasets; second arm: known items and backward chasing.

## 8. Data charting process

- **Form**: `charting_schema.json`; one JSON file per dataset under `charting/<id>.json`,
  validated against the schema on every commit.
- **Pilot**: five datasets spanning modalities and routes (VerSe, NHANES II, VinDr-SpineXR,
  FluoroCap, one TCIA collection) are charted by both reviewers before the main charting; form
  ambiguities are fixed and the fixes logged as protocol deviations.
- **Process**: one reviewer charts; a second verifies every field of every dataset against the
  quotes; disagreements resolved by discussion; `charted_by`, `verified_by` and dates recorded.
  The LLM may draft a chart from the documentation (7.4 rules apply); the verifier treats a
  drafted chart as unverified until each field has a quote or a probe result.
- **Quotes**: every charted value that is not computed (annotation origin, validation, variant
  labels, licence, counts) carries a verbatim sentence with its source and locator.
- **Access probe** (RQ5): performed by code on the run date and repeated once at least two days
  later; both results stored; the classification rules are in Appendix B. The probe fetches at
  most 64 KiB of any URL (`Range: bytes=0-65535`) and never downloads a dataset file.
- **On-grid check**: for each included dataset, the grid paths recorded in the group's
  inventory (`docs/XRAY_DATASET_USAGE.md`, `tools/CT_MINE_REPORT.md`) are tested by a listing
  command; `on_grid.status` is yes / partial / no with the path.
- **Contacting authors**: for datasets whose route is "request to authors" the review does not
  send requests; the route is the outcome. For datasets whose description is contradictory on a
  charted field, one e-mail to the corresponding author is permitted and recorded in `notes`.

## 9. Data items

Exactly the fields of `charting_schema.json`. In brief: identity (id, name, aliases, year,
country, source_record); content (modality, projection, region, n_subjects,
n_images_or_volumes, pediatric_included, format, size_gb); annotation (annotation_types,
annotation_origin, annotation_validation, per_vertebra_level_names, variant_labels); rights and
access (licence with tier, described_as_public, access_route, access_probe); data hygiene
(split_defined, patient_level_dedup, image_quality_reported); flags (figure_derived, derived,
parent_ids); local status (on_grid); audit (quotes, notes, charted_by, charted_date,
verified_by, eligibility).

## 10. Critical appraisal

Scoping reviews do not require appraisal; this one does it because the secondary objective is a
usable ranking. The instrument is `quality_rubric.md`: ten items, each 0/1/2 by rule, total
0–20, scored from charted fields only, by both reviewers independently, with item-level
weighted kappa reported. A boolean "fit for level identification" is computed from charted
fields by a fixed rule and is not a judgement. Scores do not influence inclusion.

## 11. Synthesis of results

`statistical_analysis_plan.md` fixes every table, figure and estimator. Every number in the
manuscript is generated by code into `results/numbers.json` and `results/tables/*.tex`; the
manuscript includes them and a build check fails on any numeric literal typed into the Results
section.

## 12. Outputs

```
spine_data_review/
  README.md                     purpose, venue choice, how to run
  protocol/                     this directory's files, frozen at v1.0
  sdr/                          Python package: one module per source, screen, chart, probe, stats, report
  runs/<run-date>/              requests.log.jsonl, raw/<source>/<sha1>.json, records.jsonl, counts.json
  screening/                    decisions.csv, dual_sample.csv, prescreen_sample.csv, llm/
  charting/<id>.json            one record per dataset
  results/                      numbers.json, tables/, figures/
  manuscript/                   LaTeX, build.sh
  recipe/                       download_all.sh, datasets/<id>.sh, manifest.csv, prepare_splits.py
```

Target venue and reason are stated in the README (the methodologist's recommendation: a
journal that publishes protocol-driven scoping reviews with code and does not restrict
authorship to health-outcome questions).

## 13. Engineering constraints that are part of the method

- All network runs go through WSL; every HTTP request is logged (URL without secrets,
  parameters, timestamp, status, elapsed) and every raw body is cached by SHA-1.
- Credentials are read from `~/.fluorocap/credentials.env` by name; every route runs without
  credentials at reduced rate or yield and says so in its log. No credential value is ever
  printed, logged or committed.
- Rate limits: NCBI 10/s with key else 3/s; Semantic Scholar 1/s; OpenAlex and Crossref in the
  polite pool with `mailto`; all others 2/s with exponential back-off on 429 and 5xx;
  Commons with `maxlag=5`; arXiv one request per 3 s.
- Deterministic output: sorted keys, sorted records, the run date passed as `--run-date`, the
  only wall-clock values being retrieval timestamps.
- Nothing is written outside `spine_data_review/`; no dataset is downloaded by the review code.

## 14. Ethics, funding, competing interests

No human participants; only published descriptions and public metadata are processed. Funding
and competing interests are stated in the manuscript; the authors maintain several of the
datasets under review (CTSpinoPelvic1K, FluoroCap), which is disclosed, and those datasets are
charted and scored by the verifier rather than by their author.

## 15. Timeline

Protocol frozen 2026-09-19 → registration → search run (recorded date) → prescreen and
screening → charting and probes → second probe (≥ 2 days later) → appraisal → analysis →
manuscript → search update before submission → submission.

## 16. Known-item set (frozen with the protocol)

Datasets already known to the authors, used for search validation (6.4) and included through the
other-methods arm. Modality: CT or XR (projection radiography).

| Known item | Modality | Note |
|---|---|---|
| VerSe (2019, 2020) | CT | vertebra masks, L6/T13 in the label scheme |
| CTSpine1K | CT | vertebra masks |
| TotalSegmentator (v1, v2) | CT | whole-body masks, no L6/T13 name |
| CTSpinoPelvic1K | CT | authors' own |
| CTPelvic1K | CT | pelvis with sacrum |
| RibFrac | CT | rib fractures |
| RibSeg (v1, v2) | CT | rib masks derived from RibFrac |
| SpineWeb collections (CSI 2014, xVertSeg 2016, Dataset 15 lumbar CT) | CT | historic challenge sets |
| RSNA 2022 Cervical Spine Fracture Detection | CT | Kaggle |
| CT-ORG | CT | bone class |
| AbdomenCT-1K, FLARE22/23, AMOS 2022, autoPET, SAROS, LIDC-IDRI | CT | spine visible; included only if I1 holds (spine annotation or spine-specific description) — they test I1, not recall |
| CADS | CT | whole-body |
| NHANES II lumbar and cervical films | XR | landmarks on a subset |
| BUU-LSPINE | XR | AP + lateral lumbar, end-plate lines |
| CSXA (cervical spine X-ray atlas) | XR | per-vertebra |
| VinDr-SpineXR | XR | lesion boxes |
| AASCE 2019 / BoostNet | XR | AP whole-spine landmarks |
| Mendeley 5jdfdgp762 | XR | lateral lumbar corners |
| IEEE DataPort lateral full-spine | XR | unannotated |
| Spinal-AI2024 | XR | machine-generated landmarks (E4 unless parent public) |
| FluoroCap | XR (fluoroscopy) | figure-derived, authors' own |
| MultiCaRe, Open-PMC-18M | XR/CT figures | figure-derived parents |

## 17. Deviations log

Every departure from this protocol is entered here before the affected step is rerun, with the
same entry reproduced in the manuscript's Methods. Entries are never deleted.

| Date | Section | As written in v1.0 | Change | Reason | Entered by |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

---

## Appendix A. Prescreen regexes (Python `re`, flags `re.I`)

```
SPINE_RE    = r"\b(spine|spinal|vertebr\w*|lumbar|lumbo-?sacral|thoraco-?lumbar|cervical spine|thoracic spine|scoliosis|spondylo\w*|intervertebral|pedicle)\b"
MODALITY_RE = r"(\bcomputed tomograph\w*|\bCT\b|\bCBCT\b|cone-?beam|radiograph\w*|\bx-?rays?\b|roentgen\w*|fluoroscop\w*|\bc-?arm\b|image intensifier|\bDXA\b|\bDEXA\b|dual-energy x-?ray|vertebral fracture assessment|\bEOS\b|biplanar)"
DATASET_RE  = r"\b(data\s?sets?|database|benchmark\w*|challenge|publicly available|public(ly)? (data|release)|open(-| )?(access|source|data)|data descriptor|corpus|image collection|repository|zenodo|figshare|physionet|kaggle|hugging ?face|grand-?challenge|github|download)\b"
```

Flags recorded but not used to exclude at prescreen (they inform the human screener):

```
MRI_RE      = r"\b(MRI?|magnetic resonance|T[12]\*?-?weighted)\b"
ANIMAL_RE   = r"\b(rats?|mice|mouse|murine|porcine|pigs?|swine|ovine|sheep|bovine|canine|dogs?|rabbits?|goats?|macaques?|primates?|zebrafish)\b"
PHANTOM_RE  = r"\b(phantoms?|cadaver\w*|ex[- ]vivo|sawbones?)\b"
SYNTH_RE    = r"\b(synthetic|simulated|DRR|digitally reconstructed|GAN|diffusion model)\b"
```

## Appendix B. Access-probe classification rules

Applied by code in this order to the dataset's data URL (the URL the description gives for the
images; when several, the first that is not the article itself). Repository API fields take
precedence over generic HTTP signals. `classification_machine` is what the code writes;
`access_route` is the final value after the verifier confirms it, and a difference between the
two is reported.

| Order | Signal | classification_machine |
|---|---|---|
| 1 | Zenodo `access_right` = open with files listed | open-download |
| 1 | Zenodo `access_right` = restricted | request-authors |
| 1 | Zenodo `access_right` = embargoed or closed | unavailable |
| 2 | Hugging Face `gated` = false and `private` = false | open-download |
| 2 | Hugging Face `gated` = "auto" | registration |
| 2 | Hugging Face `gated` = "manual" | dua |
| 3 | PhysioNet access policy open | open-download |
| 3 | PhysioNet restricted or credentialed | dua |
| 3 | PhysioNet contributor-review | request-authors |
| 4 | TCIA collection public in NBIA `getCollectionValues` and no "limited access" flag | open-download (via NBIA Data Retriever or REST) |
| 4 | TCIA limited-access collection | dua |
| 5 | Kaggle dataset or competition | registration (competition rules noted) |
| 6 | grand-challenge.org archive | registration; dua when the page says access must be requested |
| 7 | Figshare / Dryad / OSF / Mendeley public record with files | open-download; embargoed → unavailable; restricted files → request-authors |
| 8 | GitHub repository reachable with data files or release assets | open-download; with a link elsewhere → follow once and classify the target |
| 9 | Generic URL, HTTP 200, content-type not `text/html` or `Content-Disposition: attachment` | open-download |
| 10 | Generic URL, HTTP 200 HTML, page text matches `DUA_RE` | dua |
| 10 | … matches `PAY_RE` | commercial |
| 10 | … matches `REG_RE` | registration |
| 10 | … matches `REQ_RE` | request-authors |
| 10 | … contains an anchor to an archive extension (`zip|tar|gz|7z|nii|dcm`) that returns 200 on HEAD | open-download |
| 10 | … none of the above | unknown (verifier decides) |
| 11 | HTTP 401 or 403 | auth-required (verifier assigns registration or dua from page text) |
| 12 | HTTP 404, 410, DNS failure, or timeout on both probes | unavailable |
| 13 | No URL; description says "available on request" or similar | request-authors (method = none) |
| 14 | No URL and no statement | unknown |

```
DUA_RE = r"data[- ]use (agreement|policy)|data (usage|access|sharing) agreement|\bDUA\b|end[- ]user (licen[cs]e )?agreement|must (sign|complete) .{0,40}(agreement|application)|apply for access|access request form|credential(ed|ing) access"
REG_RE = r"sign in|log ?in|register(ed)? (user|account)|create (an|a free) account|account (is )?required|log in to download"
REQ_RE = r"contact the (corresponding )?authors?|(up)?on (reasonable )?request|available (from the authors )?on request|e-?mail .{0,60} to (obtain|request)"
PAY_RE = r"\bpurchase\b|\bpricing\b|add to cart|buy now|subscription required|\blicen[cs]e fee\b"
```

Each probe stores: url, final_url after redirects, method, http_status, content_type,
content_length, date, attempt count, the matched regex name, and a 200-character evidence
snippet from the page text.
