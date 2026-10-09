# Protocol: a scoping review of publicly described human spine CT and projection-radiography datasets, with programmatic availability probing and a download recipe

Version 1.0 — 2026-09-19 — data-engineer draft. Written before any search is executed.
Reporting standard: PRISMA-ScR (Tricco 2018). Structure: JBI Manual for Evidence Synthesis,
chapter 11 (scoping reviews). Registration: Open Science Framework, to be registered before
the first search run; the OSF DOI is entered in the deviations log, section 14, and nowhere
else is it typed by hand.

This document is written from the harvester's side. Each information source is described by
what its API can and cannot express, what is recorded per request, and how a record travels
from a raw response body to a number in the manuscript. Anything that cannot be traced along
that path is not reported.

---

## 1. Rationale

The authors' level-identification project uses CTSpinoPelvic1K, VerSe, TotalSegmentator,
NHANES, BUU-LSPINE, CSXA, VinDr-SpineXR, AASCE and a literature-mined fluoroscopy corpus
(FluoroCap). Each of these was discovered late, by chance, and none of the enumerations that
exist (dataset tables in method papers, Papers with Code, awesome-lists) states three things
the project needs on the first day: where the annotation came from, whether the variant
anatomy that the project's error analysis turns on (L6, T13, lumbosacral transitional
vertebra) is labelled, and whether the data can be obtained today. Whole-spine radiographs and
thoracic images are the scarcest inputs for the frame-stitching work and the ones an ad hoc
search is least likely to surface.

A scoping review is the right form because the question is "what exists and what is it like",
not "what is the effect of X". The availability question is empirical and changes over time,
so it is answered by an HTTP probe on a recorded date, not by reading the paper.

## 2. Objectives and review questions

Primary.
- Q1. What publicly described datasets of human spine CT and projection radiography exist
  (2000–2026), and what are their size, region, projection and format?
- Q2. How is each annotated (per-vertebra level names, segmentation, landmarks/boxes,
  pathology labels, none), and where did the annotation come from (expert manual,
  model-generated, counting-inferred, report-derived, unknown)?
- Q3. Does the dataset label variant anatomy: L6, T13, LSTV — yes / no / unknown, with counts
  where reported?
- Q4. Under what licence, and by what access route established programmatically on a recorded
  date: open-download / registration / data-use-agreement / request-to-authors / unavailable /
  commercial?

Secondary.
- Q5. A predefined 0–20 quality score per dataset and a boolean "fit for level identification".
- Q6. Pooled descriptive statistics, pooled variant prevalence, pooled inter-rater agreement.
- Q7. A reproducible download recipe for every dataset with route open-download or registration,
  and the share of datasets already on the authors' grid.

## 3. Eligibility criteria (fixed; changes go to the deviations log)

Population/concept/context (JBI PCC): human subjects; spine imaging datasets; any country,
language, clinical setting, 2000-01-01 to 2026-12-31 by first public description.

Include a record if all of the following hold:
- I1. It describes a dataset (a named or nameable collection intended for reuse) of human spine
  images. A method paper that releases its data is included; a method paper that only uses a
  dataset already charted is linked to that dataset as a "use" record, not charted again.
- I2. Modality is CT (any kV, any reconstruction, cone-beam included) or projection
  radiography: plain radiograph (CR/DX), fluoroscopy or C-arm, DXA vertebral fracture
  assessment, EOS biplanar. Multimodal datasets qualify if at least one eligible modality has
  at least 10 subjects.
- I3. At least 10 subjects in the eligible modality.
- I4. Described in a journal article, preprint, challenge page or repository record.
- I5. With or without annotations.
- I6. Figure-derived collections assembled from the literature qualify; they are flagged
  `figure-derived` and n_subjects is charted as "unknown" unless the collection states it.
- I7. Datasets derived from another public dataset qualify; flagged `derived` with the parent id.

Exclude if any of the following holds:
- E1. MRI-only, ultrasound-only, nuclear-medicine-only.
- E2. Non-human, phantom-only, cadaver-only.
- E3. Purely synthetic with no public parent CT/radiograph.
- E4. Single case or fewer than 10 subjects.
- E5. Images are not subject-level medical images (only extracted features, only landmarks
  without pixels, only statistics).
- E6. Duplicate of an included record (handled by de-duplication, section 7, not by screening).

Eligibility is decided on title/abstract/description in two stages: a recorded regex prescreen
(section 8.1) and a reviewer decision with reason per record (section 8.2). A reviewer never
overrides a prescreen exclusion silently: an override is a row with reason `prescreen-override`.

## 4. Information sources

Full API-level detail (endpoint, auth, rate limit, field syntax, paging cap, verbatim query
strings) is in `information_sources.md`. Summary:

| Group | Sources |
|---|---|
| Literature | PubMed (E-utilities), Europe PMC, OpenAlex, Semantic Scholar Graph (bulk), arXiv, bioRxiv + medRxiv, Crossref |
| Data repositories and indexes | Zenodo, Figshare, Dryad, OSF, Mendeley Data (via DataCite prefix when the search API needs credentials), DataCite, PhysioNet, TCIA/NBIA, Kaggle (credentialed) , Hugging Face Hub, grand-challenge.org, GitHub search, Papers with Code (probe; retired-endpoint fallback), OpenDataLab (probe) |
| FluoroCap literature routes (figure-derived collections and non-English literature) | NLM Open-i, MultiCaRe (Zenodo 10079370), Open-PMC-18M (Hugging Face), Wikimedia Commons, J-STAGE, KoreaMed/Synapse, SciELO, Redalyc |
| Supplementary | Springer Nature Meta API (keyed; Scientific Data and Data in Brief venue sweep), Unpaywall (open-access copy of a source article for charting; never for datasets) |
| Excluded, with reason | Google Dataset Search (no API; terms of service forbid scraping); YouTube, Instagram, Reddit, Flickr, Facebook (not dataset sources: no subject-level medical images described as datasets, no stable record); Common Crawl (web text, not a dataset index); patents (drawings, not datasets) |

Every source is queried by code. A source that cannot be queried by code without a credential
that is not present is run in credential-free mode if one exists, else recorded as
`needs-credentials` with zero hits, and this is reported in the PRISMA flow, never hidden.

Credentials live in `~/.fluorocap/credentials.env` on the WSL host and are read by
`sdr/creds.py`; a key's presence is logged, its value never. Optional: `~/.kaggle/kaggle.json`,
`HF_TOKEN`, `GITHUB_TOKEN`, `OSF_TOKEN`.

## 5. Search strategy

Term sets. Three fixed sets are combined as (SPINE) AND (MODALITY) AND (DATASET). The sets are
defined once in `sdr/terms.py` and each source's query is rendered from them by that source's
adapter so that the same concepts are searched everywhere the syntax allows; where a source has
no boolean OR (Wikimedia Commons, J-STAGE, Dryad, OSF, Crossref, Hugging Face, Kaggle) the
adapter issues one request per term combination and the union is recorded with per-request
counts.

- SPINE: spine, spinal, vertebra, vertebrae, vertebral, lumbar, thoracic, cervical,
  lumbosacral, sacrum, sacral, scoliosis, spondylolisthesis, "vertebral fracture".
  Reasoning: region words catch datasets named by region ("lumbar spine X-ray"), the
  pathology words catch datasets named by task (AASCE is "scoliosis", not "spine"). "cervical"
  imports cervical cancer, handled at prescreen. "rib" is deliberately absent: rib datasets
  without a spine claim are out of scope.
- MODALITY: CT, "computed tomography", tomography, radiograph, radiographs, radiography,
  "x-ray", "x ray", xray, roentgen, fluoroscopy, fluoroscopic, "C-arm", "image intensifier",
  DXA, DEXA, absorptiometry, "vertebral fracture assessment", EOS, biplanar, "plain film",
  "cone-beam". Reasoning: each named modality in I2 has at least two surface forms; DXA VFA
  datasets never say "radiograph". MRI is not excluded at search time because multimodal
  datasets would be lost; it is excluded at screening.
- DATASET: dataset, datasets, "data set", database, benchmark, challenge, corpus, collection,
  "publicly available", "open access", "open-access", "open source", "data descriptor",
  annotated. Reasoning: "challenge" and "benchmark" are how MICCAI-era datasets are titled;
  "data descriptor" is the Scientific Data article type; "publicly available" is the phrase
  by which a method paper announces a release.

Constraints applied at search time: publication year 2000–2026 where the API supports a date
field; no language limit; no publication-type limit (reviews are retained because their
tables enumerate datasets and are used for citation chasing, then excluded at charting).

Supplementary search methods: (a) reference and citation chasing of every included source
record through OpenAlex `referenced_works` and `cited_by` (one hop; recorded as source
`chase`); (b) the dataset tables of every included review article, extracted by the reviewer
into `screen/chase_manual.csv` with the page number; (c) parent/derived links from charting.

Dates. Every run passes `--run-date`; the retrieval timestamp of every request is recorded. The
search is executed once in full and the run directory is frozen; a re-run for the manuscript
revision is a new run directory with its own PRISMA counts, compared in the deviations log.

## 6. What is recorded per request and per record

`<run-dir>/requests.log.jsonl`, one line per HTTP attempt:
`{ts, source, query_id, attempt, method, url, params, status, elapsed_ms, bytes, cache_sha1, from_cache, error}`.
`url` and `params` are secret-stripped: any parameter named `api_key`, `apikey`, `key`,
`token`, `access_token`, `email`, `mailto` and any `Authorization` header is replaced by
`<redacted>` before logging. The `mailto` value is public but is redacted anyway so that the log
can be published without review.

`<run-dir>/raw/<source>/<sha1>.json`: the raw response body, where sha1 is over
`method + canonical secret-stripped URL + sorted params + body`. A replay run (`--replay`)
never touches the network and fails loudly on a cache miss.

`<run-dir>/records/<source>.jsonl`: one line per returned item, sorted by record id:
`{record_id, source, query_id, retrieved_at, ids: {doi, pmid, pmcid, arxiv, url, repo_id},
title, abstract_or_description, year, type, raw}`. `raw` is the source's own fields, untouched.

`<run-dir>/queries.json`: for every query_id the verbatim string sent, the endpoint, the date,
the total hit count reported by the API, the count actually retrieved, and the paging cap hit,
if any. This file is the appendix table.

## 7. Identification and de-duplication

Record id: `lit:` or `repo:` plus the first 12 hex characters of sha1 over the strongest
identifier available, tried in order: DOI (lowercased, `https://doi.org/` stripped), PMID,
PMCID, arXiv id (version stripped), repository canonical URL (scheme and trailing slash
normalised, query string dropped), else `source:native_id`.

Cross-source merge, in order, each pass recorded with the rule that fired:
1. Exact DOI.
2. Exact PMID or PMCID (via the id map returned by NCBI id-converter and Europe PMC).
3. arXiv id ↔ DOI via the arXiv record's `doi` field and OpenAlex `ids`.
4. Normalised title (NFKC, lowercase, alphanumerics only) identical AND first-author surname
   identical AND |year difference| ≤ 1. Titles shorter than 25 characters never merge by rule 4.
5. Repository record ↔ article by DataCite/Crossref `relatedIdentifiers` (IsSupplementTo,
   IsDescribedBy, IsReferencedBy) and by DOI strings found in the repository description.

A merged cluster is a "source record". A dataset (charting unit) is created by the reviewer
from one or more source records; the link table `charting/dataset_sources.csv` maps every
source record used to its dataset id with the role (`primary-description`, `repository`,
`version`, `use`, `derived-from`). Dataset ids are `ds_<slug>` assigned at charting and never
renumbered.

Version handling: versions of one dataset (VerSe'19/'20, TotalSegmentator v1/v2) are one dataset
with a `versions` list; the charted counts are for the latest version unless stated.

## 8. Selection of sources of evidence

### 8.1 Regex prescreen (recorded)
`sdr/prescreen.py` applies the rules in `screen/prescreen_rules.yaml` to title + abstract/
description. Output per record: `prescreen_include`, `prescreen_exclude:<rule>`, or
`prescreen_uncertain`. Rules, all case-insensitive:
- X-MRI: matches MRI terms (`\bMRI\b|magnetic resonance|\bT1[- ]weighted|\bT2[- ]weighted`)
  AND matches no MODALITY term → exclude.
- X-ANIMAL: matches `\b(rat|rats|mouse|mice|murine|porcine|pig|ovine|sheep|canine|dog|bovine|rabbit|zebrafish|primate|macaque)\b` AND does not match `\b(human|patient|patients|subject|subjects|volunteer)\b` → exclude.
- X-PHANTOM: matches `phantom|cadaver` AND no `patient|subject|volunteer` → exclude.
- X-NOTSPINE: cervical cancer / cervical lymph / cervical carotid patterns AND no other SPINE term → exclude.
- X-NOMODALITY: no MODALITY term in title or abstract → uncertain (not exclude, because repository descriptions are short).
- Everything else → include (goes to the reviewer).
The rule file is versioned; rule counts per source are a PRISMA flow row.

### 8.2 Reviewer screening
Every `prescreen_include` and `prescreen_uncertain` record is screened on title/abstract/
description by a reviewer using `sdr/screen.py`, which presents records in record-id order and
writes `screen/decisions.csv`: `record_id, decision (include|exclude|full-text), reason_code,
reason_text, reviewer, date`. Reason codes are the E1–E6 codes plus `not-a-dataset`,
`out-of-range-year`, `cannot-determine`. Full-text step: `full-text` decisions are resolved
after reading the article (Unpaywall or publisher) or the repository page, with a second row.

A 10% random sample (seed 20260919) is screened independently by a second reviewer; Cohen's
kappa is reported. Disagreements are resolved by discussion and the resolution recorded.

### 8.3 LLM-assisted step (named as such)
If used, an LLM is used only to draft a prescreen suggestion and a one-line summary for the
reviewer, never to decide. Model id, prompt file (`screen/llm_prompts/<version>.txt`) and every
output (`screen/llm_outputs.jsonl` with record_id, model, prompt sha1, output) are stored. The
manuscript reports how many suggestions the reviewer reversed.

## 9. Data charting

One JSON per dataset under `charting/datasets/<id>.json`, validated against
`charting_schema.json` (draft-07) by `sdr/validate.py` in the build. Fields as in the schema.
Charting is done by one reviewer and verified by a second on every record that will enter a
pooled analysis (variant counts, agreement statistics) and on a 20% random sample of the rest.
Every non-trivial field has a `quotes` entry: the verbatim sentence, its source (DOI/URL) and
location (section, table, page or repository field). "Unknown" is a value, not a blank.

Repository-derived fields are filled by code, not by hand: `sdr/enrich.py` pulls licence,
file list, sizes and checksums from Zenodo, Figshare, Dryad, DataCite, Hugging Face and TCIA
APIs into `charting/enrichment/<id>.json`, and the charted value records which came from the
API (`"source": "api:zenodo"`) and which from the paper.

## 10. Availability probe

`sdr/probe.py` runs on a recorded date against each dataset's `access_url` and, when known,
one file URL. Method: HEAD, then GET with `Range: bytes=0-0`, following at most five redirects,
custom User-Agent with the contact e-mail, 20 s timeout, three attempts with backoff. Recorded:
final URL, every status in the redirect chain, content-type, content-length,
`www-authenticate`, and the first 64 KB of an HTML body (kept in raw cache, searched by rule).

Classification rules, applied in order, first match wins, rule id recorded:
- P1. Repository API says open (Zenodo `access_right=open`; Figshare `is_public` and not
  embargoed; Hugging Face `gated=false, private=false`; Dryad any published version; TCIA
  collection not marked limited-access; PhysioNet "Open Access") AND a file URL answers
  200/206 with a non-HTML content-type → `open-download`.
- P2. Hugging Face `gated=auto` → `registration`; `gated=manual` → `data-use-agreement`.
- P3. Zenodo `restricted` → `request-to-authors`; `embargoed` → `unavailable` (embargo date recorded).
- P4. PhysioNet "Credentialed" or "Restricted" → `data-use-agreement`.
- P5. TCIA limited-access, Kaggle, grand-challenge.org, OpenDataLab, any endpoint answering 401
  with a login redirect and no DUA text → `registration`.
- P6. Landing page HTML (200) matching `data use agreement|data-use agreement|\bDUA\b|
  request access|apply for access|access request form` → `data-use-agreement`.
- P7. Landing page or paper stating `available (up)?on (reasonable )?request|contact the
  corresponding author|by request to` and no resolving download URL → `request-to-authors`.
- P8. Page matching `purchase|pricing|licen[cs]e fee|commercial licen[cs]e` → `commercial`.
- P9. 404/410/451, DNS failure, or timeout on all three attempts on both probe days → `unavailable`.
- P10. Otherwise → `unresolved`, sent to the reviewer, whose classification and reason are recorded.

The probe is run twice, at least 24 h apart; the classification is the agreement, and any
disagreement is `unresolved` for the reviewer. Nothing beyond the first byte of any file is ever
downloaded by the probe.

Secondary outcome "described as public that actually downloads": denominator = datasets whose
source record matches `publicly available|freely available|open(-| )access|available at
https?://` (regex recorded); numerator = those classified `open-download` or `registration`
with a file URL that answered 200/206.

## 11. Critical appraisal

`quality_rubric.md`: ten items scored 0/1/2 by rule, total 0–20, plus the boolean fit-for-level-
identification with its rule. Scored by code from charted fields (`sdr/quality.py`) so that a
score change is always a charting change; the reviewer never edits a score directly.

## 12. Synthesis

`statistical_analysis_plan.md`. Everything is computed by `sdr/analyse.py` into
`analysis/*.json` and `tables/*.tex`; figures by `sdr/figures.py` into `figures/*.pdf`.

## 13. How every manuscript number traces to a file

- The manuscript contains no typed digits that describe the review's data. `tables/numbers.tex`
  defines one macro per number (`\numIncludedDatasets`, `\numOpenDownload`, ...) generated by
  `sdr/numbers.py` from `analysis/*.json`.
- Every value in `analysis/*.json` is an object `{value, derived_from: [paths], rule}`, where
  paths are the files it was computed from (charting JSONs, `queries.json`, probe results).
- `sdr.trace <macro-name>` prints the chain from macro to raw files, and `build.sh` fails if
  (a) any `\num...` macro used in the .tex is undefined, (b) any macro defined is unused, or
  (c) the .tex contains a bare number of two or more digits outside a macro, citation, or
  `\label`/`\ref` (regex check, allow-list in `build/allowed_literals.txt` with a reason each).
- Figures embed the sha1 of the JSON they were drawn from in their PDF metadata.

## 14. Deviations log

Every departure from this protocol is a row here, added before the deviating step is run
where possible, otherwise on discovery. Format: date, section, what changed, why, effect on
results. The manuscript's Methods cites this log verbatim in an appendix.

| Date | Section | Deviation | Reason | Effect |
|---|---|---|---|---|
| 2026-09-19 | — | Protocol 1.0 written. No deviations yet. | — | — |
| (to fill) | 4 | OSF registration DOI: | registered after protocol freeze | none |

Known points where the plan depends on run-time facts and a deviation is likely:
- Papers with Code: the site was retired in 2025; if the API answers 404 or redirects, the
  static datasets dump or Hugging Face papers listing is used and the log says so.
- Mendeley Data, OpenDataLab, KoreaMed, Redalyc, SciELO, grand-challenge.org: search endpoints
  are undocumented or credentialed; the credential-free behaviour in `information_sources.md`
  is what runs, and the deviation row records what actually answered.
- Kaggle: without `~/.kaggle/kaggle.json` the source is `needs-credentials`.

## 15. Roles, funding, conflicts

Reviewer 1 (charting, screening): the PI. Reviewer 2 (verification, 10% double screen, 20%
charting check): named at registration. The authors created some of the datasets under review
(CTSpinoPelvic1K); those are charted by reviewer 2 and the conflict is stated. Funding as in
the manuscript.

## 16. Venue

One venue is named and justified in the directory README (not here); the manuscript follows
PRISMA-ScR headings so that it can be reformatted for any of Systematic Reviews, BMJ Open, JBI
Evidence Synthesis or Scientific Data (Analysis).
