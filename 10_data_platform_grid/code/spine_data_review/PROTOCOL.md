# Protocol: a scoping review of publicly described human spine CT and projection-radiography datasets, with programmatic access verification and a download recipe

**Protocol version 1.0 — frozen 2026-09-19, after the count-only pilot search (`information_sources.md` section 6.0, `runs/pilot-2026-09-19/queries.json`) and before the full search is executed.**

Reporting standard: PRISMA-ScR (Tricco et al., Ann Intern Med 2018), structured after the JBI
Manual for Evidence Synthesis chapter on scoping reviews, with Cochrane Handbook practice for
search reporting, duplicate screening and a pre-specified analysis plan. Registration: the
frozen protocol is deposited on the Open Science Framework (Registries, "Generalized
Systematic Review Registration" template) after the pilot search and before the full search runs; the registration DOI
is entered in the deviations log (section 19) and read from there by the manuscript. PROSPERO
does not accept scoping reviews and is not used.

Companion documents, all part of the protocol and frozen with it:

| File | What it fixes |
|---|---|
| `information_sources.md` | every source: endpoint, authentication, rate ceiling, paging cap, syntax, and the verbatim query strings with a `query_id` each |
| `charting_schema.json` | the charting form as JSON Schema draft-07; one record per dataset |
| `quality_rubric.md` | ten items scored 0/1/2 by rule from charted fields; the fit-for-level-identification rule |
| `statistical_analysis_plan.md` | every analysis, its inputs, estimator, eligibility rule and output key |
| `PRISMA-ScR_checklist.md` | the 27 reporting items and where each is reported |

Wording conventions used throughout: access routes are spelled `open-download`,
`registration`, `data-use-agreement`, `request-to-authors`, `unavailable`, `commercial`;
"unknown" is a value, never a blank; the p-word banned by the project style guide is not used
anywhere in this review; the concepts are "annotation origin" and "where the data came from".

---

## 1. Background and rationale

Vertebral level identification from a limited field of view — the problem this group works on
in fluoroscopy and radiography — depends on training and test data in which the level names are
right, the origin of each label is known, and variant anatomy (a sixth lumbar vertebra L6, a
thirteenth rib-bearing vertebra T13, a lumbosacral transitional vertebra LSTV) is labelled
rather than silently normalised. The group already uses CTSpinoPelvic1K, VerSe,
TotalSegmentator, NHANES II, BUU-LSPINE, CSXA, VinDr-SpineXR, AASCE and a literature-mined
fluoroscopy collection (FluoroCap), and has repeatedly found a relevant dataset only after a
model had been trained without it.

No published enumeration of spine CT and radiograph datasets states, for each one, how its
annotations were produced, whether variant anatomy is labelled, what the licence permits, and
whether the data can be downloaded today. Existing lists (dataset roadmaps, challenge
overviews, "awesome" lists, Papers with Code) are unsystematic, undated and do not verify
access. Whole-spine radiographs and thoracic-spine images are the scarcest class and the most
valuable for the frame-stitching work, so a review that finds even a few more matters.

A scoping review is the right form because the question is "what exists and what is it like",
not "what is the effect of X". The availability question is empirical and changes over time,
so it is answered by an HTTP probe on a recorded date, not by reading the paper.

## 2. Objectives and review questions

Primary (each answered per dataset and in aggregate):

- **RQ1** What publicly described datasets of human spine CT and projection radiography exist
  (2000–2026), with or without annotations, and what are their size, region, projection and
  format?
- **RQ2** How is each annotated — per-vertebra level names, segmentation, landmarks or boxes,
  pathology labels, none — and what is the origin of the annotation (expert manual, model
  generated, counting inferred, report derived, other)?
- **RQ3** Is variant anatomy (L6, T13, LSTV) labelled: yes / no / unknown, with counts where
  reported?
- **RQ4** Under what licence is each released?
- **RQ5** What is the access route today, established by a recorded probe: open-download,
  registration, data-use-agreement, request-to-authors, unavailable, commercial?

Secondary:

- **SO1** Score each dataset on a predefined ten-item quality rubric (0–20) and compute a
  boolean "fit for level identification" by a fixed rule.
- **SO2** Pool what can be pooled: counts and totals by modality, region, projection,
  annotation type and origin, access route, licence tier and year; the share of datasets
  described as public that actually download; pooled prevalence of L6, T13 and LSTV where
  per-subject counts are reported, and pooled inter-rater agreement where at least five
  datasets report a comparable statistic, both as illustrative secondary summaries beneath the
  per-dataset tables (section 3); quality score against access route and year.
- **SO3** Produce a download recipe for every dataset with an open-download or registration
  route, a manifest of every dataset with its route, and a stub for a patient-grouped split.
- **SO4** Report which included datasets are already on the authors' compute grid.

The review is first a review with predefined methods. The recipe is a product of the charting
records, not the reason for the eligibility criteria.

## 3. Design

JBI "PCC" framework:

- **Population**: images of the human spine (any region, any age).
- **Concept**: a dataset — a named or nameable, bounded collection of subject-level images,
  with or without annotations, that has a description someone else can read and is intended
  for reuse.
- **Context**: CT (including cone-beam CT) and projection radiography (plain radiograph,
  fluoroscopy or C-arm, DXA vertebral fracture assessment, EOS biplanar); described in a
  journal article, preprint, challenge page or repository record dated 2000–2026; any language;
  any country; any clinical setting.

Unit of analysis: the dataset. Records (articles, preprints, repository entries, challenge
pages) are the unit of screening; several records may describe one dataset and one record may
describe several datasets. The record-to-dataset mapping is explicit (section 7.6).

**Design choice on pooling, stated once.** The JBI scoping-review chapter maps evidence and
does not pool by meta-analysis; that is the systematic-review design. This review keeps the
scoping frame (the questions are "what exists and what is it like") and reports the variant
prevalence and inter-rater statistics (SO2) as *descriptive per-dataset tables* — per-dataset
proportions with exact intervals — as the primary output. A pooled summary (SAP A5, A6) is
produced only as a clearly labelled secondary, *illustrative* summary, its departure from the
JBI design is stated in Methods and in Limitations, and no conclusion rests on a pooled point
estimate. The checklist header (`PRISMA-ScR_checklist.md`) carries the same statement.

## 4. Eligibility criteria

Fixed; any change is a deviations-log row. All criteria are decided on the record's title,
abstract or description, and on the dataset's own documentation when the record points to it.
Each criterion has a code recorded in the screening CSV. A record is included when every
I-criterion holds and no E-criterion holds. The rationale column is what PRISMA-ScR item 6
asks for.

### 4.1 Inclusion

| Code | Criterion | Decision rule | Rationale |
|---|---|---|---|
| I1 | Human spine imaging | The description says the images show the human spine or a named vertebral region (cervical, thoracic, lumbar, sacrum, whole spine), or the spine is a labelled structure in a body-region dataset (a whole-body CT dataset with vertebra masks passes). Chest, abdomen or pelvis datasets with no spine annotation and no spine-specific description are **not** included merely because vertebrae are in the field of view. | Vertebrae sit in the field of view of most chest, abdomen and pelvis scans; without a spine claim or a spine label such a dataset cannot be found by a spine search or charted for annotation origin, and the count of "spine datasets" would become a count of body CT. |
| I2 | Modality | At least one of: CT, CBCT, plain radiograph (CR/DR/film), fluoroscopy or C-arm frames, DXA vertebral fracture assessment images, EOS biplanar radiographs. Multi-modal datasets are included when at least one eligible modality has at least 10 subjects; ineligible modalities are recorded but not counted. | These are the modalities of the intended use (level identification from projection images and from CT). CBCT is included because intra-operative CBCT is the CT most often paired with fluoroscopy. MRI has its own label conventions and literature and is not part of the question. |
| I3 | Size | I3 holds when a stated `n_subjects` ≥ 10, **or** when `n_subjects` is unknown and a stated `n_images_or_volumes` ≥ 10 (charted `n_subjects_basis = unknown`). Figure-derived collections use source articles as the proxy when the subject count is not stated. | Ten is the smallest set for which a per-subject variant count (RQ3) is a count rather than a case report; the image fallback keeps datasets described only in scans or studies, which repository records often are. |
| I4 | Described | At least one of: journal article, preprint, challenge web page, data-repository record (Zenodo, Figshare, Dryad, OSF, Mendeley Data, PhysioNet, TCIA, Kaggle, Hugging Face, GitHub, institutional repository). A bare download link with no text describing the content fails I4. Authors'-own datasets are no exception: FluoroCap, or any other set an author maintains, enters only if a public describing record exists on the run date; otherwise it is reported as "known item, excluded I4" in the other-methods arm of the flow (section 7.7). | This review charts only public text; a dataset a reader cannot find a description of cannot be charted from it. |
| I5 | Date | The earliest record that describes the *image release* (article, preprint, challenge page or repository record) is dated 2000-01-01 to 2026-12-31. `year` is that record's year; the years in which the images were acquired go in `cohort_year_range` and do not decide I5 (NHANES II films, acquired 1976–80 and released as digital images by NLM in the 2000s, pass I5 on the release record). | 2000 is the first year in which spine image collections were distributed digitally rather than as film libraries; earlier cohorts enter through their digital release. |
| I6 | Annotation status | Any: with annotations or without. | Unannotated datasets are what the project's own pipeline labels; excluding them would answer RQ1 wrongly. |
| I7 | Figure-derived collections | Collections assembled from published figures (PMC, Open-i, MultiCaRe, Open-PMC-18M, Wikimedia Commons, journal APIs) are eligible when I1–I5 hold and are flagged `figure_derived = true`. | The only public source of fluoroscopy at scale, and what FluoroCap was built from. |
| I8 | Derived datasets | Datasets built by re-annotating, re-labelling, subsetting or converting another public dataset are eligible, flagged `derived = true`, with the parent recorded in `parent_ids`. | Re-annotations are where level names and variant labels are most often added to an older release. |

### 4.2 Exclusion

| Code | Criterion | Decision rule | Rationale |
|---|---|---|---|
| E1 | MRI only | No eligible modality is present (MRI-only, ultrasound-only, nuclear-medicine-only). | Out of scope by I2. |
| E2 | Non-human | Animal, veterinary or comparative-anatomy imaging. A dataset mixing human and animal subjects is included with the human count only if that count is stated; otherwise excluded. | Population is the human spine. |
| E3 | Phantom or cadaver only | All images are of phantoms, cadavers, ex-vivo specimens or printed models. A dataset mixing living subjects and cadavers is included with the living count. | Variant prevalence and level naming are questions about living anatomy in clinical images. |
| E4 | Purely synthetic | Images generated (DRR, GAN, diffusion, simulation) with no public parent CT or radiograph dataset. Synthetic datasets rendered from a public parent are included under I8 as `derived`. | A synthetic set with no public parent has no subjects to count and no annotation origin to chart. |
| E5 | Too small | A *stated* subject count below 10. A record with an unknown subject count and at least 10 images or volumes does not fail E5 (see I3). | The complement of I3. |
| E6 | Not subject-level images | The release contains only extracted features, measurements, embeddings, landmarks without pixels, reports or metadata, without the images. | The review is of image datasets. |
| E7 | Duplicate record | **Not a screening code.** A second, third … record about an already included dataset is not excluded at screening: it passes to record-to-dataset mapping (section 7.6) with a role, so that it stays in `record_ids`, in backward chasing and in the source-overlap diagnostic (SAP A9). Versions of one dataset collapse to one dataset with the versions listed; a derived dataset is not a duplicate of its parent. Identical records (same canonical identifier, section 7.1) are removed at de-duplication and counted there. | Dropping later records at screening silently removes the evidence the flow and the overlap diagnostic count. |
| E8 | Not a dataset | A method paper that uses a private dataset without describing it as available; a review, editorial, protocol; a model or software release without images. A method paper that describes and releases its data passes. A method paper that merely *uses* an already public dataset and releases no new images or labels is coded `use-only` (section 7.3): not an included record, counted in that dataset's `n_use_records`. Reviews are retained until charting for backward chasing (section 6.4), then excluded under E8. | Use-only papers (VerSe alone has hundreds) would otherwise inflate the included-record count without adding a dataset. |

### 4.3 Operational definitions

- **Subject**: one person. Where a description reports "scans" or "studies" and not subjects,
  `n_subjects` is null with `n_subjects_basis = unknown` and `n_images_or_volumes` carries the
  count with its unit.
- **Described as public**: a reviewer-charted value (`described_as_public` = yes / no /
  unknown) that requires a quote: the record states that the *images* (not the code, not a
  supplement) are released, or gives a repository DOI or URL for the images. Charted from the
  text before the probe and never updated from it, so the two can be compared (SAP A3.2).
  Independently, code records the flag `described_as_public_regex` from the case-insensitive
  regex

  ```
  PUBLIC_RE = r"(data|dataset|images?|scans?|volumes?|radiographs?|cases) (are|is|were|will be|have been|has been) (made )?(publicly|freely|openly) available|(data|dataset|images?) (is|are) available (at|from|on) https?://|(data|dataset|images?) (is|are) (available|deposited|hosted) (at|from|on|in) (zenodo|figshare|physionet|kaggle|hugging ?face|github|synapse|osf|dryad|mendeley data|the cancer imaging archive|tcia|ieee dataport)"
  ```

  over title + abstract + description. The flag is reported beside the charted value
  (SAP A3.2) and never replaces it. A repository DOI or URL counts only when it is given for
  the images; a DOI for code or supplementary tables does not. `open access` and a bare
  `available at https?://` are deliberately absent: every open-access article carries both.
- **Annotation origin** categories: *expert-manual* (drawn or named by a clinician or a trained
  annotator under documented expert supervision, whatever the tool); *expert-corrected-model*
  (model output corrected by an expert); *model-generated* (uncorrected model output);
  *counting-inferred* (level names assigned by counting from a landmark such as C2 or the
  sacrum rather than by direct reading of each vertebra); *report-derived* (labels parsed from
  radiology reports); *crowd-or-trainee* (non-expert annotators without documented expert
  review); *caption-derived* (labels parsed from figure captions); *unknown*; *none*.
  Counting-inferred is the origin this review exists to expose: a counting-inferred level name
  cannot test a counting-free method.
- **Variant anatomy**: L6 = a sixth lumbar-type vertebra; T13 = a thirteenth rib-bearing
  vertebra; LSTV = lumbosacral transitional vertebra (Castellvi types I–IV or equivalent,
  including sacralisation and lumbarisation). "Labelled" (`status = yes`) means present per
  subject in the released labels or metadata, or counts reported in the text; `no` means the
  description states the variant is absent, excluded or not represented; `unknown` means
  silent. `how_labelled` records the mechanism (explicit-label, derivable-from-labels,
  reported-in-text, excluded-by-design, not-labelled, unknown).
- **Per-vertebra level names**: `yes` when every annotated vertebra carries an anatomical
  level name (C1…S1) in the release; `partial` when only some images or only one region do;
  `no` when labels are class-agnostic or absent.

## 5. Information sources

All sources are queried by code with the exact query string, endpoint, timestamp and hit count
recorded. The full specification is `information_sources.md`. Summary:

- **Literature indexes (7)**: PubMed (E-utilities), Europe PMC, OpenAlex, Semantic Scholar
  Graph (bulk), arXiv, bioRxiv/medRxiv, Crossref.
- **Data repositories and indexes (14)**: Zenodo, Figshare, Dryad, OSF, Mendeley Data (via a
  probed front-end endpoint and the DataCite prefix route), DataCite, PhysioNet, TCIA/NBIA,
  Kaggle (credentialed; credential-free fallback is a URL-mention harvest), Hugging Face,
  grand-challenge.org, GitHub (repositories; code search when a token exists), Papers with
  Code (retired; probe then static dump), OpenDataLab (undocumented endpoints probed).
- **FluoroCap literature routes (8)**: NLM Open-i, MultiCaRe (Zenodo 10079370), Open-PMC-18M
  (`vector-institute/open-pmc-18m`), Wikimedia Commons, J-STAGE, KoreaMed Synapse, SciELO,
  Redalyc. Each is itself a candidate figure-derived dataset (charted under I7 with its spine
  subset counted by `sdr/figure_counts.py` from API-reachable metadata only, section 8) and its
  hit counts size the figure-derived pool by modality (SAP A3.4, outside the flow diagram).
  Every source has a stated coverage (index start date, or "unknown") in the summary table of
  `information_sources.md` and in `queries.json` (PRISMA-ScR item 7).
- **Supplementary (2)**: Springer Nature Meta API (venue sweep of Scientific Data; a recall
  check, keyed, skipped when the key is absent); Unpaywall (full-text location for charting
  only, never a search source).
- **Other methods**: the known-item set (section 6.4); one hop of backward and forward
  citation chasing through OpenAlex for every included source record; the dataset tables of
  every review article retained under E8, extracted by the reviewer into
  `screen/chase_manual.csv` with the page number; parent/derived links found at charting.

Sources considered and excluded, with the reason stated in the manuscript: Google Dataset
Search and Google Scholar (no API; terms of service forbid automated querying); YouTube,
Instagram, Reddit, Flickr, Facebook (media platforms FluoroCap mined for single images; they
hold no subject-level medical-image datasets with a stable record and cannot be screened by
title/abstract); Openverse (aggregates Commons and Flickr; Commons is searched directly);
Common Crawl (raw web text, not a dataset index; record-level screening is not reproducible);
patents (drawings and claims, not released image collections).

Credentials live in `~/.fluorocap/credentials.env` on the WSL host (KEY=value, mode 600) and
are read by name by `sdr/creds.py`: `NCBI_API_KEY`, `S2_API_KEY`, `FLUOROCAP_CONTACT_EMAIL`,
`SPRINGER_API_META_KEY`, `SPRINGER_API_OPEN_ACCESS_KEY` (present, not used: the Meta API
covers the venue sweep), `UNPAYWALL_EMAIL`; optional `~/.kaggle/kaggle.json`, `HF_TOKEN`,
`GITHUB_TOKEN`, `OSF_TOKEN`. A key's presence is logged, its value never. Every route degrades
to credential-free behaviour and says so in its log; a source with no credential-free form is
recorded `needs-credentials` with zero hits and appears as such in the PRISMA flow.

## 6. Search strategy

### 6.0 Pilot search (JBI step 1)

The JBI three-step search is: a limited pilot search with term harvesting; the full search;
chasing. The pilot is described in `information_sources.md` section 6.0 and recorded in
`runs/pilot-2026-09-19/queries.json` with `role: pilot`. It consisted of count-only requests;
no record was retrieved, no title or abstract was read, and no term was added to any block
from it. The one decision it produced — Europe PMC strings are fielded — is recorded there.
The blocks themselves were assembled from the titles of the known-item set (section 18) and
the group's earlier ad-hoc searches, which is stated in Methods.

### 6.1 Concept blocks

Every query is the conjunction (SPINE) AND (MODALITY) AND (DATASET), translated into each
source's syntax. The blocks and every rendered string are fixed in `information_sources.md`
("Term blocks" and the fenced `query_id:` blocks and grid lines), and that file is the single
source of truth: each adapter reads its verbatim block from it at run time, or from the two
materialised files `queries/literature.yaml` and `queries/repositories.yaml`, which carry the
same strings with the endpoint, parameters and expected credential mode of every id and are
what Appendix A prints. `tests/test_queries_yaml.py` fails the build if any entry marked
`verbatim_in_markdown` differs byte-for-byte from its fenced block or grid line, or if a run's
`queries.json` records a string, endpoint, date-filter mode or raw-cache flag other than the
planned one. (v1.0 named `sdr/terms.py` and `tests/test_terms.py`, a generator and its test;
neither was written and the YAML files are materialised by hand: deviations log, 2026-09-19.)

- **BLOCK_S**: spine, spinal, vertebra*, lumbar, thoracolumbar, lumbosacral, sacrum,
  "cervical spine", "thoracic spine", scoliosis, spondylolisthesis. *Cervical*, *thoracic*
  and *sacral* alone are not used (cervix, thoracic surgery, sacral nerve stimulation);
  *scoliosis* and *spondylolisthesis* are included because their radiograph datasets often
  omit "spine" from the title; *rib* is absent because rib datasets without a spine claim are
  out of scope.
- **BLOCK_M**: "computed tomography", "computed tomographic", CT, CBCT, "cone-beam", "cone
  beam", radiograph*, "X-ray", "X-rays", "x ray", xray*, roentgen*, fluoroscop*, "C-arm",
  "image intensifier", DXA, DEXA, absorptiometry, "vertebral fracture assessment", EOS,
  biplanar, "plain film", "plain films". Each named modality in I2 has at least two surface
  forms; DXA VFA datasets never say "radiograph". MRI is not in the block: multimodal datasets
  would be lost; MRI-only records fail E1 at screening.
- **BLOCK_D**: dataset, datasets, "data set", "data sets", database, benchmark*, challenge,
  "publicly available", "public data", "open data", "open access", "open-access", "open
  source", "data descriptor", corpus, "image collection". "Challenge" and "benchmark" are how
  MICCAI-era datasets are titled; "data descriptor" is the Scientific Data article type;
  "publicly available" is how a method paper announces a release. *Annotated* and
  *segmentation* are deliberately absent: they retrieve the whole method literature, whose
  released datasets are reached through BLOCK_D terms in their abstracts, the repository
  sources and backward chasing.

Sources without boolean syntax receive the fixed grid of 35 strings (section G of
`information_sources.md`) or a fixed single-term list, each string its own `query_id`, and the
union is de-duplicated. Sources with no query interface (bioRxiv/medRxiv, PhysioNet, TCIA
collection list, grand-challenge.org, MultiCaRe, Open-PMC-18M record) are harvested in full
over their listing endpoint and filtered locally with the prescreen regexes (Appendix A),
which is recorded as the query. Repository deposits imply BLOCK_D and it is omitted there.

### 6.2 Limits

Year 2000–2026 in the string where the source supports a date field, else applied locally and
recorded as `date_filter: local`. No language limit. No document-type limit at search time,
except that repository searches restricted to dataset records are paired with an unrestricted
second pass where the repository types deposits inconsistently (Zenodo, Figshare), and the
difference is reported.

### 6.3 Recording

For each query execution: source, `query_id`, verbatim string as sent, endpoint (secrets
removed), parameters, retrieval timestamps (UTC), reported total, number retrieved, pages,
paging cap reached (null or the cap), date-filter mode, credential mode (name only, never the
value). Raw responses are cached by SHA-1 so a run can be replayed offline (section 15). The
search is executed once in full on a date passed as `--run-date` and the run directory is
frozen. A search update before submission is a new run directory with its own counts; its
records are de-duplicated against the frozen run, and the new ones are screened, charted and
probed twice by exactly the procedure of sections 7–10. If any dataset is included through the
update, every analysis is regenerated from the union of the two runs and the manuscript's
last-search date is the update date; the deviations log records the delta (records, datasets,
changed numbers). The update appears as its own row in the flow (section 7.7).

### 6.4 Search validation and other methods

**Known-item recall.** The set in section 18 is frozen with the protocol and is machine-readable
in `screen/known_items.csv` (columns `item, role, modality, doi, pmid, url, title_norm, year,
match_rule, note, id_verified`). Each item has a `role`: `recall` (a spine dataset the search
should find), `I1-test` (a body-region dataset entered to test criterion I1 at screening, not
the search) or `excluded-I4` (an authors'-own set with no public record). An item is
*retrieved* when a merged record matches it by its `match_rule`: `doi` (exact, lower-cased) when
a DOI is given; else `title-year` (normalised title as in section 7.1 rule 5 identical and
|year difference| ≤ 1); else `url` (canonical URL as in section 7.1 identical).
Recall = retrieved / items with `role = recall`, with a Wilson interval, overall and per
source; `I1-test` and `excluded-I4` items are outside the denominator and are reported in
their own rows. Before the recall computation every identifier in the CSV is resolved once
(`id_verified` set to yes/no with the date); a non-resolving DOI or URL is corrected in the
deviations log, and the match rule does not change. Recall below 0.80 triggers a documented
revision of the query strings, logged with the items that drove it, and a rerun; the known
items are included through the other-methods arm regardless, so recall measures the search,
not the review. The set is not used to tune the prescreen regexes after they are frozen.

**Chasing.** One hop of backward (`referenced_works`) and forward (`cites:`) chasing through
OpenAlex for every included source record with an OpenAlex id, one request per id keyed
`openalex_03_<openalex_id>` (forward) and `openalex_03r_<openalex_id>` (backward) with grammar
`chase` in `queries.json`, results flagged `found_via = backward-chasing` or
`forward-chasing`; Appendix A reports them as one summary row with the number of ids chased and
the total hits. The dataset tables of retained review articles are extracted by hand into
`screen/chase_manual.csv` with the page number.

## 7. Selection of sources of evidence

### 7.1 Record identity and de-duplication

Record id: `lit:` or `repo:` plus the first 12 hex characters of SHA-1 (UTF-8) over the
*canonical string*, which is the first available of:

1. `doi:<doi>` — the DOI lower-cased, with `https://doi.org/`, `http://dx.doi.org/` and a
   leading `doi:` stripped and trailing punctuation removed;
2. `pmid:<digits>`;
3. `pmcid:PMC<digits>`;
4. `arxiv:<id>` — the arXiv id without any `arXiv:` prefix and without the version suffix;
5. `url:https://<host><path>` — the repository canonical URL with the host lower-cased, `http`
   rewritten to `https`, the path without a trailing slash, and no query string or fragment;
6. `native:<source>:<native_id>` — the source's own identifier (`native:zenodo:10079370`).

The prefix is `repo:` iff the source is R1–R14, or the record's type is `dataset` or `image`
in Crossref, OpenAlex or DataCite; every other record is `lit:`. `sdr/ids.py` implements the
canonical string and `tests/test_ids.py` fixes worked examples.

Cross-source merge, each pass recorded with the rule that fired and counted in the flow:
1. Exact DOI.
2. Exact PMID or PMCID (via the id map returned by the NCBI id-converter and Europe PMC).
3. arXiv id ↔ DOI via the arXiv record's `doi` field and OpenAlex `ids`.
4. Zenodo concept DOI (versions collapse to one record).
5. Normalised title (NFKC, lower-case, alphanumerics only) identical AND first-author family
   name normalised the same way identical AND |year difference| ≤ 1. Titles shorter than 25
   characters never merge by rule 5. No fuzzy matching; near-duplicates that survive are
   caught at mapping (section 7.6).
6. Repository record ↔ article by DataCite/Crossref `relatedIdentifiers` and `relation`
   (IsSupplementTo, IsDescribedBy, IsReferencedBy) and by DOI strings found in the repository
   description.

The retained record keeps every source and `query_id` that found it (`found_by`), which is
what the per-source flow counts and the source-overlap diagnostic (SAP A9) are computed from.

### 7.2 Rule-based prescreen (recorded, not final)

`sdr/prescreen.py` applies `screen/prescreen_rules.yaml` (the regexes of Appendix A,
versioned) to `title + abstract + description`. Outcome per record:
- `pass` when `SPINE_RE`, `MODALITY_RE` and `DATASET_RE` all match. For records from
  repository sources (R1–R14) and from the FluoroCap routes, `DATASET_RE` is not required (the
  source implies it) and a missing `MODALITY_RE` match yields `uncertain` rather than `fail`,
  because repository descriptions are short.
- `fail:<S|M|D>` naming the first block that did not match.
- `uncertain` as above; goes to the reviewer.
- `uncertain` with the rule "no abstract in any source that found this record", decided before
  `MODALITY_RE` is tried, for a record found only by literature sources whose merged abstract is
  empty in every one of them. Semantic Scholar elides the abstract of every paper whose publisher
  forbids redistributing it (406 of the 1,000 records on the first `s2_01` page; 405 of those 406
  fail the three regexes on their title alone), and Spine, Eur Spine J and J Neurosurg Spine sit
  with those publishers. Records also found by PubMed, Europe PMC or Crossref are repaired by the
  merge, which keeps the longest member abstract; records found only by Semantic Scholar —
  conference proceedings, IEEE/CVF, theses, where challenge-dataset papers live — are not.
  Counting them as `fail:M` or `fail:D` would attribute thousands of exclusions to "no modality
  term" or "no dataset term" when the true reason is that no abstract was available to search, so
  they go to the reviewer and are counted as their own flow row
  (`prescreen_uncertain_no_abstract` in `prisma_counts.json`, `prescreen.uncertain_no_abstract` in
  `analysis/flow.json`). `abstract_elided` on a Semantic Scholar record separates "the publisher
  withheld it" from "the paper has none" for the D-fail audit.
- `pass:non-english-route` for every record from the non-English routes F5–F8 (J-STAGE,
  KoreaMed, SciELO, Redalyc): those sets are small and the regexes are English, so they are not
  prescreened and every hit goes to the reviewer. The per-language variants `SPINE_RE_JA`,
  `SPINE_RE_KO`, `SPINE_RE_ES_PT` (Appendix A) are recorded on those records as flags so that
  prescreen outcomes can be reported per language; they never exclude.

The negative flags `MRI_RE`, `ANIMAL_RE`, `PHANTOM_RE`, `SYNTH_RE` are recorded on every record
and shown to the reviewer; they never exclude at prescreen.

**Prescreen audit.** Failing records are not screened, except a stratified audit sample that
one reviewer screens blind to the prescreen outcome. Strata: failing block (S, M, D) × source
class (query-based literature: L1–L5, L7; repository: R1–R14; full-harvest: L6, R7, R8, R11,
R13). Sizes: 150 records from the D-fail stratum, 100 from M-fail, 50 from S-fail, each split
as evenly as the stratum allows across the three source classes (a shortfall in one class is
reallocated to the others), drawn by `sdr/sampling.py` (section 7.8). The inclusion rate per
stratum with a Wilson interval and the implied number of missed records (rate × stratum size)
are reported (SAP A1); the pooled fail set is never sampled as one population, because the
full-harvest sources would dominate it and the estimate would say nothing about the query-based
sources. A record included from the audit enters through the search arm with
`prescreen_outcome = fail` and `prescreen-override` in `codes`. Pre-specified action: if the
D-fail inclusion rate exceeds 2 %, every D-fail record that matched S and M is re-routed to
reviewer screening as `uncertain` and the change is a deviations-log row. Records from sources
harvested in full are prescreened the same way, and for them the prescreen is the search. Rule
counts per source are a PRISMA flow row.

### 7.3 Reviewer screening

Every `pass`, `pass:non-english-route` and `uncertain` record is screened on
title/abstract/description by one reviewer against I1–I8 and E1–E8 using `sdr/screen.py`,
which presents records in record-id order and writes `screen/decisions.csv` with the columns

`record_id, stage, reviewer, date, decision, primary_code, codes, reason_text, llm_suggestion, llm_agreed, prescreen_outcome`

- `stage` ∈ {`title-abstract`, `full-text`, `dual`, `resolution`}.
- `decision` ∈ {`include`, `exclude`, `unclear`}.
- `codes`: one or more of I1–I8, E1–E6, E8, `use-only`, `prescreen-override`, separated by
  `;`. E7 is not a screening code (section 4.2). The former codes `not-a-dataset`,
  `out-of-range-year` and `cannot-determine` are not used: they are E8, I5 and
  `decision = unclear`.
- `primary_code`: the first failing criterion in the order I1, I2, I3, I4, I5, E1, E2, E3, E4,
  E5, E6, E8, `use-only`, equal to the first entry of `codes`; it is the one exclusion reason a
  record carries in the flow (section 7.7).
- `use-only`: the record uses an already included dataset and releases no new images or
  labels. It is not an included record, is not chased, and is counted in that dataset's
  `n_use_records` (role `use` in `charting/dataset_sources.csv`).

A reviewer never overrides a prescreen `fail` silently: an override is a row with
`prescreen-override` in `codes`.

**Dual screening.** A second reviewer independently screens a random sample of the
`pass ∪ uncertain` records, stratified by prescreen outcome (`pass`, `uncertain`,
`pass:non-english-route`) and source class (literature, repository, figure route), of size
k = max(100, ceil(0.10 · N)) drawn by `sdr/sampling.py` (section 7.8) and recorded in
`screen/dual_sample.csv`; in addition, **every** record that reaches description review
(section 7.5) is screened by both reviewers. Agreement (SAP A8) is Cohen's κ on the *binary*
decision include vs {exclude, unclear} (primary), three-class κ (secondary), raw agreement,
and the prevalence-and-bias-adjusted kappa (PABAK) and Gwet's AC1 beside κ, because the
inclusion prevalence in the sample is low and depresses κ. Disagreements are resolved by
discussion, with the resolution recorded as a `stage = resolution` row.

**Departure from JBI, stated.** JBI asks for two independent reviewers at both the
title/abstract and the full-text stage. Here one reviewer screens the full title/abstract set,
and two reviewers screen the stratified sample and the whole description-review stage. The
reason (one PI and one second reviewer against an expected five-figure record count) and the
effect (κ is estimated on the sample, not on the whole set) are stated in Methods and in
Limitations, not only in the checklist.

### 7.4 LLM-assisted step (decided; named as such)

The step **is used**. Model `claude-fable-5-1` (Anthropic), temperature 0, no tools, one
record per call; prompt template v1 at `screen/llm/prompts/v1.txt`, SHA-1
`c0cdc2dfcd3d3e38f5f2999f418f6c6ba7b0942c`, checked by the build. The LLM proposes a
decision, criterion codes and a one-line summary before the human decides. Every input and
output is stored (`screen/llm/outputs.jsonl`: record_id, model, prompt sha1, output, ts). The
human decision is recorded independently; the agreement between the suggestion and the human
decision is reported (SAP A8) and never combined with the human dual-screen κ. The LLM never
makes a final decision, never charts a field without a human verifier, and is not shown to the
second reviewer on the dual-screened sample. Fallback (foreseeable deviation, section 19): if
the named model is unavailable on a screening date, `llm_suggestion` and `llm_agreed` are left
empty for the records screened that day, the A8 line for the LLM is reported with the number
of records it covered, and a different model is never substituted.

### 7.5 Description review

For every record marked `include` or `unclear`, both reviewers independently read the
dataset's own documentation (repository landing page, README, data descriptor full text where
open) and each writes a `stage = full-text` row in `screen/decisions.csv`; disagreement is
resolved as a `stage = resolution` row. Full text is obtained through the record's open-access
link or Unpaywall; paywalled articles are read through the institution's subscription when
available; when no full text can be obtained, the record is charted from its abstract and
repository record, `notes` says so, and the record is counted in the flow's "reports not
retrieved" box (section 7.7) with the reason. Records excluded at this stage are the near-miss
exclusions cited with reasons under PRISMA-ScR item 14.

### 7.6 Record-to-dataset mapping

Included records are clustered into datasets by: identical data DOI or repository URL
(canonicalised as in 7.1); identical name or alias in `charting/aliases.csv`; or an explicit
statement that one record describes another's dataset. `charting/aliases.csv` (columns
`dataset_id, alias, source`) is seeded with the protocol from the known-item set and grows
during mapping; because mapping by alias is circular before the aliases exist, mapping is
iterated: the alias file is extended, mapping is rerun, the number of changed assignments is
logged, and the loop ends when that number is zero. Each dataset receives an `id` (a stable
slug, section 8) and the list of `record_ids` behind it, with each record's role in
`charting/dataset_sources.csv` (`primary-description`, `repository`, `version`, `use`,
`derived-from`, `challenge-page`). Dataset ids are never renamed.

**Versions: one dataset per lineage.** A dataset with named releases (VerSe 2019 and 2020;
TotalSegmentator v1 and v2) is one dataset with `versions[]` listed and the largest version
charted (`charted_version`). A later release is a separate dataset only when its description
states that its subjects are disjoint from the earlier release (quoted in `notes`), in which
case the two are linked by `parent_ids`; where a release is stated to contain the earlier one,
`superset_of_version` names it. There is no percentage rule. Under this rule VerSe is one
dataset (the two releases overlap: the unified set is smaller than their sum) and
TotalSegmentator is one dataset (v2 is described as extending v1).

**Precedence for conflicting values** across a dataset's records: repository API > data
descriptor (an article or preprint whose purpose is the dataset) > challenge page > other
article; the conflicting values are quoted in `notes` with their sources.

### 7.7 Flow

Counts are reported in a PRISMA 2020 two-arm flow diagram drawn by code from
`analysis/flow.json`, with totals in the diagram and the per-source rows in Table 2. The
identity that `sdr/analyse.py --check-flow` asserts, per arm:

```
search arm
  identified (after within-source de-duplication)
  − duplicates removed at cross-source merge (rules 1–6)
  = records after merge
  = fail (not audited) + fail (audited: included + excluded) + pass + uncertain
  screened = pass + uncertain + audit-included
           = excluded (by primary_code) + use-only + unclear→full-text + include→full-text
  sought for full text = unclear→full-text + include→full-text
           = not retrieved (charted from abstract) + retrieved
  after description review = excluded (by primary_code) + included records
other-methods arm
  known items (retrieved by search / not retrieved / excluded-I4)
  + chasing candidates (backward, forward, manual) + search-update records
  → screened → excluded → included records (second arm)
datasets = mapped from (included records, search arm) ∪ (included records, second arm),
           with derived and figure-derived counts and n_use_records per dataset
```

For sources harvested in full (bioRxiv/medRxiv, PhysioNet, TCIA, grand-challenge.org, the
Papers with Code dump) `n_identified` is the post-filter count and the harvest total is a
separate column. Figure-pool sizing (SAP A3.4) is outside the flow; in the flow, Open-i
counts screenable records (distinct articles by PMCID) and Commons counts candidate
categories, not files. Sources run as `needs-credentials`, `html-fallback`, `no-public-api` or
`retired` appear with their hits and the reason.

### 7.8 Random draws

Every random draw uses the same procedure, implemented once in `sdr/sampling.py` and fixed by
a unit test: the population is sorted by record id (or dataset id), a fresh
`random.Random(20260919)` is created for the draw, and `sample(population, k)` is taken.
Sizes: dual-screen sample k = max(100, ceil(0.10 · N)) stratified as in 7.3 (the stratum
sizes proportional to the strata, rounded up); prescreen audit 150 / 100 / 50 by block as in
7.2; re-charting sample k = max(25, ceil(0.20 · N_datasets)). Bootstrap resampling uses
`numpy.random.default_rng(20260919)`. No draw shares a generator with another.

## 8. Data charting process

- **Form**: `charting_schema.json`; one JSON per dataset under `charting/datasets/<id>.json`,
  validated by `sdr/validate.py` on every build. `id` is a lower-case slug (`verse`,
  `ctspinopelvic1k`, `vindr-spinexr`) that is also the name of `recipe/datasets/<id>.sh`.
- **Pilot**: five datasets spanning modalities and routes (VerSe, NHANES II, VinDr-SpineXR,
  CTSpinoPelvic1K, one TCIA collection) are charted by both reviewers before the main
  charting; form ambiguities are fixed and the fixes logged as protocol deviations.
  (FluoroCap is not a pilot dataset: it has no public record and fails I4 unless one exists on
  the run date.)
- **Process and order**: one reviewer charts every dataset. As soon as the dataset list is
  fixed, the re-charting sample of k = max(25, ceil(0.20 · N)) datasets is drawn (section 7.8)
  and the second reviewer re-charts those *blind* — from the documentation only, without
  seeing the first chart — **before** verifying any dataset; `charted_date` on the re-chart and
  `verified_date` are recorded and the build asserts that the re-chart precedes verification
  for every sampled dataset. Only then does the second reviewer verify every field of every
  dataset against the quotes and the enrichment record, recording `verified_by` and
  `verified_date`. The rubric's inter-rater reliability is computed from the blind sample
  (SAP A4.5): per-item exact agreement and linearly weighted κ, reported as "not estimable"
  with raw and prevalence-adjusted agreement when an item has zero variance in the sample;
  ICC(2,1) on the total with the Shrout–Fleiss F-based interval and n stated
  (`sdr/reliability.py`). Disagreements are resolved by discussion and the resolution
  recorded in `notes`. The LLM may draft a chart from the documentation under the rules of
  7.4; a drafted chart is unverified until each field has a quote or an API value.
- **Quotes**: every charted value that is not computed by code carries a verbatim sentence
  with its source and locator in `quotes`, keyed to the field it supports. The fields that
  *require* a quote are enumerated in the schema (`x-requires-quote`), and `sdr/validate.py`
  fails a record when a listed field has neither a quote with a matching `field` nor a
  `field_sources` entry naming an API.
- **Enrichment by code**: `sdr/enrich.py` pulls licence, file list, sizes, checksums, DOI,
  version and access fields from Zenodo, Figshare, Dryad, OSF, DataCite, Hugging Face, TCIA and
  PhysioNet APIs into `charting/enrichment/<id>.json`; `field_sources` in the charting record
  says which value came from which API (`api:zenodo`) and which from the article or page.
- **Access probe** (RQ5): section 10.
- **Figure-derived counts by code**: `sdr/figure_counts.py` computes the spine sub-figure
  counts of the figure-derived parents from API-reachable metadata only. MultiCaRe: one
  download of its `captions_and_labels.csv` through the Zenodo file API (a metadata file, not
  an image download; the review's cap that distinguishes the two is 200 MB per file, and the
  file's sha1 is recorded), then `SPINE_RE` and `MODALITY_RE` over the captions.
  Open-PMC-18M: the Hugging Face datasets-server search route only; if it has no index the
  count is charted `null` with basis `unknown`. No value is read from files on the authors'
  cluster.
- **On-grid check (SO4)**: `spine_data_review/grid_inventory.csv` (columns `dataset_id,
  grid_path, source_doc, n_subjects_listed, note`, copied at the freeze from the group's
  inventories `docs/XRAY_DATASET_USAGE.md` and `tools/CT_MINE_REPORT.md`) lists the paths
  tested by a listing command on a recorded date; `on_grid.status` is yes / partial / no with
  the path and, where countable, the subject count on disk. SO4 is author-specific: a second
  team cannot reproduce it, and the manuscript labels it so.
- **Contacting authors**: the review does not send access requests; `request-to-authors` and
  `unavailable` are therefore *unrequested* outcomes, which is a standing limitation
  (section 16). For a dataset whose description is contradictory on a charted field, one
  e-mail to the corresponding author is permitted and is recorded in `notes` with the date.
- **Own datasets**: datasets a review author maintains (`flags.authors_own = true`, with
  `flags.maintainer_authors` listing their initials; CTSpinoPelvic1K, and FluoroCap only if
  I4 holds) are charted and verified by an author not in `maintainer_authors`, which
  `sdr/validate.py` asserts.

## 9. Data items

Exactly the fields of `charting_schema.json`. In brief: identity (id, name, aliases,
versions, year and its basis, cohort_year_range, country, source_record); content (modality,
projection, region, n_subjects and its basis, n_images_or_volumes and unit, n_per_modality,
pediatric_included, format, size_gb); annotation (annotation_types, annotation_origin,
annotation_validation with comparator and n_categories, per_vertebra_level_names,
variant_labels for L6/T13/LSTV with selection, ascertainment and definition_class);
documentation and metadata elements (read by the rubric); rights and access (licence with
tier from `licence_tiers.csv`, described_as_public and its regex flag, access_url with
access_url_basis and host_type, access_probe list, access_route); data hygiene
(split_defined, patient_level_dedup, image_quality_reported); overlap (subject_overlap);
flags (figure_derived, derived, parent_ids, multi_modal, authors_own, maintainer_authors);
checksums for the recipe; local status (on_grid); audit (quotes, field_sources, notes,
charted_by, charted_date, verified_by, verified_date, eligibility). `year` is the year of the
earliest record describing the image release; `cohort_year_range` is free text for the
acquisition years (section 4.1, I5).

## 10. Availability probe

`sdr/probe.py` runs on a recorded date against each dataset's `access_url` and, when known
from enrichment, one `file_url_probed`.

**Which URL.** `access_url` is the URL the description gives for the images (when several,
the first that is not the article itself). `access_url_basis` records how it was obtained:
`given-in-record`; `resolved-from-named-repository` (the record names a repository and a
dataset name but gives no link, and the charter resolves it to the landing page through that
repository's own search, recording the query and date in `notes`); `resolved-from-doi` (a data
DOI resolved once through doi.org); `none`. A dataset whose paper names TCIA or Zenodo without
a link is therefore probed at the resolved landing page, not classified `unavailable` for want
of a link.

**Host table.** Before any generic HTTP probe the URL is routed by DOI prefix or host.
doi.org, dx.doi.org and hdl.handle.net links are resolved once (HEAD, redirects followed) and
classified by the resolved host. The same table gives `host_type`, charted by code and used
by SAP A3.1 and rubric Q7: `repository-api` for the first eleven rows, `challenge-platform`
for grand-challenge.org and Kaggle competitions, `institutional` for a university, hospital
or agency host, `personal-or-cloud-drive` for drive.google.com, dropbox.com, onedrive,
box.com, pan.baidu.com and personal pages, `unknown` otherwise.

| DOI prefix / host | Route | Rules |
|---|---|---|
| `10.5281` / `zenodo.org` | Zenodo records API by record id | P1–P3 |
| `10.6084` / `figshare.com` / `*.figshare.com` | Figshare articles API | P13 |
| `10.5061` / `datadryad.org` | Dryad API | P13 |
| `10.17605` / `osf.io` | OSF API | P13 |
| `10.17632` / `data.mendeley.com` | DataCite record + landing page | P13 |
| `10.13026` / `physionet.org` | project page access-policy string | P7–P9 |
| `10.7937` / `cancerimagingarchive.net` | NBIA REST | P10–P11 |
| `huggingface.co/datasets` | Hub datasets API | P4–P6 |
| `kaggle.com` | Kaggle | P12 |
| `grand-challenge.org` | grand-challenge | P12 |
| `github.com` | repos API | P14 |
| anything else | generic HTTP | P15–P23 |

**Generic method.** HEAD, then GET with `Range: bytes=0-65535`, following at most five
redirects, the review's User-Agent, 20 s timeout, three attempts with back-off. Recorded per
probe: final URL, every status in the redirect chain, content-type, content-length,
`Content-Disposition`, `WWW-Authenticate`, the first 64 KiB of an HTML body (in the raw cache),
the rule that fired and a ≤ 400-character evidence snippet. Nothing beyond the first 64 KiB of
any landing page or file is ever fetched; no dataset file is downloaded. A repository's own API
answer (a JSON record or file listing, never a dataset file) is read whole, because the fields
the rules read sit anywhere in it (deviations log, 2026-09-19). Repository API fields take
precedence over generic HTTP signals.

**Visible text.** For an HTML body the first 64 KiB is parsed; `script`, `style`, `nav`,
`header`, `footer` and `aside` elements are removed, tags are stripped and whitespace is
collapsed. P16–P19 search this *visible text*, not the raw HTML. A `REG_RE` or `PAY_RE` match
counts only when it lies within 200 characters of `download|data|access|files` in the visible
text, so a navigation bar's "Log in" or a footer's "Pricing" never classifies a page.

The probe is run twice, at least 48 hours apart. The machine classification is the value the
two probes agree on; when they disagree a third probe is run before the verifier decides. Any
disagreement that survives, and any `unresolved` or `auth-required`, is sent to the verifier,
whose final `access_route` and reason are recorded, and the count of verifier overrides is
reported (SAP A3.2). `access_route_rule` records the rule ids of the agreeing probes,
slash-joined when they differ (`P15/P20`), or `verifier: <reason>`.

**Rules.** Applied in the order P1–P15, then **P20 before P16–P19**, then P21–P25; first match
wins; the rule id is recorded in `access_probe[].rule`. Rule ids are stable across the
protocol's files and are not renumbered.

| Rule | Signal | classification_machine |
|---|---|---|
| P1 | Zenodo `access_right = open` with files listed, and a file URL answers 200/206 | open-download |
| P2 | Zenodo `access_right = restricted` | request-to-authors |
| P3 | Zenodo `access_right = embargoed` or `closed` (embargo date recorded) | unavailable |
| P4 | Hugging Face `gated = false` and `private = false` | open-download |
| P5 | Hugging Face `gated = "auto"` | registration |
| P6 | Hugging Face `gated = "manual"` | data-use-agreement |
| P7 | PhysioNet policy Open Access | open-download |
| P8 | PhysioNet Credentialed or Restricted | data-use-agreement |
| P9 | PhysioNet Contributor Review | request-to-authors |
| P10 | TCIA collection public in NBIA and not flagged limited-access | open-download (via NBIA REST or Data Retriever) |
| P11 | TCIA limited-access collection | data-use-agreement |
| P12 | Kaggle dataset or competition; grand-challenge.org archive; OpenDataLab | registration (competition rules noted; grand-challenge → data-use-agreement when the page matches `DUA_RE`) |
| P13 | Figshare (`is_public`, not embargoed), Dryad (published version), OSF or Mendeley public record with files | open-download; embargoed → unavailable; restricted files → request-to-authors |
| P14 | GitHub repository reachable with data files or release assets | open-download; a link elsewhere is followed once and the target classified |
| P15 | Generic URL answering 200/206 whose content-type is in the allow-list `application/zip`, `application/gzip`, `application/x-gzip`, `application/x-tar`, `application/x-7z-compressed`, `application/dicom`, `application/octet-stream`, or `image/*` when the URL path ends in a data extension (`.dcm .nii .nii.gz .nrrd .mha .tif .tiff .png .jpg .jpeg .zip .tar .gz .tgz .7z`), or that carries `Content-Disposition: attachment`; and content-length ≥ 1 MiB when a content-length is given | open-download. A PDF, a JSON document, a small image or an HTML page never fires P15 and falls through |
| P20 | Generic 200 HTML page containing an anchor to `\.(zip\|tar\|gz\|tgz\|7z\|nii\|nii\.gz\|dcm)(\?.*)?$` that answers 200/206 on HEAD or ranged GET (applied before P16–P19) | open-download |
| P16 | Generic 200 HTML, visible text matches `DUA_RE` | data-use-agreement |
| P17 | … visible text matches `PAY_RE` within 200 characters of `download\|data\|access\|files` | commercial |
| P18 | … visible text matches `REG_RE` within 200 characters of `download\|data\|access\|files` | registration |
| P19 | … visible text matches `REQ_RE` | request-to-authors |
| P21 | … none of the above | unresolved (verifier decides) |
| P22 | HTTP 401 or 403 with no rule above matching, or a redirect chain ending at a login page (final URL matching `login\|signin\|sign-in\|auth`, or `WWW-Authenticate` present) | auth-required (verifier assigns registration or data-use-agreement from page text) |
| P23 | Per probe: 404, 410, 451, DNS failure, or timeout on all three attempts | unavailable (disagreement between probe days is handled by the two-probe rule above) |
| P24 | No URL after the `access_url_basis` steps; description matches `REQ_RE` | request-to-authors (method = none) |
| P25 | No URL after the `access_url_basis` steps and no statement | unavailable (a reader cannot obtain the data today; the verifier may change it with a recorded reason) |

```
DUA_RE = r"data[- ]use (agreement|policy)|data (usage|access|sharing) agreement|\bDUA\b|end[- ]user (licen[cs]e )?agreement|must (sign|complete) .{0,40}(agreement|application)|apply for access|access request form|credential(ed|ing) access"
REG_RE = r"log ?in to download|account (is )?required|register(ed)? (user|account)|create (an|a free) account|registration (is )?required"
REQ_RE = r"contact the (corresponding )?authors?|(up)?on (reasonable )?request|available (from the authors )?on request|e-?mail .{0,60} to (obtain|request)"
PAY_RE = r"\bpurchase\b|\bpricing\b|add to cart|buy now|subscription required|\blicen[cs]e fee\b|commercial licen[cs]e"
NEAR_RE = r"download|data|access|files"      # proximity anchor for REG_RE and PAY_RE (200 characters)
```

All five patterns are matched case-insensitively (`re.I`; deviations log, 2026-09-19), so
"END-USER LICENSE AGREEMENT" fires P16. The bare `sign in|log ?in` alternatives are absent from
`REG_RE` on purpose: every page with a navigation bar matches them.

**Secondary outcome "described as public that actually downloads" (SAP A3.2), one definition
in both files.** Denominator = datasets with the reviewer-charted `described_as_public = yes`.
Primary numerator = those with final `access_route = open-download` (the route already encodes
the file evidence of P1, P13–P15, P20 or a repository API's open state, so open datasets on
institutional servers are not failed by construction). Second row: among datasets with a known
`file_url_probed`, the proportion whose file URL answered 200/206 on both probes, with its own
denominator. Third row: route in {open-download, registration} (the recipe-eligible set).
Wilson intervals on each; the regex flag `described_as_public_regex` is cross-tabulated
against the charted value.

## 11. Critical appraisal

Scoping reviews do not require appraisal; this one does it because SO1 is a usable ranking.
The instrument is `quality_rubric.md`: ten items, each 0/1/2 by rule, total 0–20, computed by
`sdr/quality.py` from charted fields only, so that a score change is always a charting change
and every score traces to a quote or an API field. Inter-rater reliability comes from the
blind re-charting of max(25, 20 %) of the datasets, done before verification (section 8). The boolean "fit for level identification" and its derived
booleans are computed by fixed rules and the failing rule is recorded. Scores do not influence
inclusion.

## 12. Synthesis

`statistical_analysis_plan.md` fixes every table, figure, estimator and eligibility rule.
Everything is computed by `sdr/analyse.py` (descriptives, tests) and `sdr/meta.py` (pooling)
into `analysis/*.json`, rendered by `sdr/report.py` into `tables/*.tex`, `tables/numbers.tex`
and `figures/*.pdf`.

## 13. How every manuscript number traces to a file

- The manuscript's Abstract and Results contain no bare digit at all; every number that
  describes the review's data is a macro.
  `tables/numbers.tex` defines one macro per number (`\numIncludedDatasets`,
  `\numOpenDownload`, …) generated by `sdr/numbers.py` from `analysis/*.json`, with a
  `\numword…` variant that spells out values under ten for prose.
- Every value in `analysis/*.json` is an object `{value, derived_from: [paths], rule}` naming
  the files it was computed from.
- `python -m sdr.trace <macro>` prints the chain from macro to raw files. `build.sh` fails if
  (a) any `\num…` macro used in the .tex is undefined, (b) any defined macro is unused, or (c)
  the Results or Abstract source contains a bare number of two or more digits outside a
  macro, citation, `\label`/`\ref`, with an allow-list in `manuscript/allowed_literals.txt`
  carrying a reason per entry.
- Restated for (c): **any** bare digit in the Abstract or Results source fails the build —
  single digits included — unless it is inside a macro, a citation, a label or reference, or
  an allow-listed literal (years, rule ids such as P15, criterion codes such as I3, section
  numbers). Numbers under ten in prose come from `\numword…` macros.
- Figures embed the SHA-1 of the JSON they were drawn from in their PDF metadata.

## 14. Outputs and directory layout

```
spine_data_review/
  README.md                       purpose, venue choice and why, how to run
  PROTOCOL.md and companions      this protocol, frozen at v1.0 (git tag protocol-v1.0)
  sdr/                            Python package: one module per source, prescreen, screen,
                                  enrich, probe, quality, analyse, meta, numbers, report, trace
  runs/<run-date>/                requests.log.jsonl, raw/<source>/<sha1>.json,
                                  records/<source>.jsonl, queries.json, merged.jsonl
  screen/                         prescreen_rules.yaml, known_items.csv, decisions.csv,
                                  dual_sample.csv, prescreen_audit.csv, chase_manual.csv,
                                  llm/prompts/v1.txt, llm/outputs.jsonl
  charting/datasets/<id>.json     one record per dataset
  charting/aliases.csv            dataset_id, alias, source (seeded with the protocol)
  charting/dataset_sources.csv    record → dataset roles
  charting/enrichment/<id>.json   API-derived fields
  licence_tiers.csv               licence text pattern → tier, spdx, standard flag (Q6)
  grid_inventory.csv              grid paths tested by the on-grid check (SO4)
  runs/pilot-2026-09-19/          the count-only pilot search record (section 6.0)
  sdr/sampling.py, sdr/ids.py, sdr/reliability.py, sdr/stats.py, sdr/figure_counts.py
  tests/                          unit tests run by build.sh (ids, terms, sampling, meta,
                                  reliability, stats)
  analysis/*.json                 every number, with derived_from
  tables/*.tex, tables/numbers.tex
  figures/*.pdf
  manuscript/                     main.tex, build.sh (latexmk), allowed_literals.txt
  recipe/                         download_all.sh, datasets/<id>.sh, manifest.csv, prepare_splits.py
```

The target venue and the reason for it are stated in `README.md`; the manuscript follows
PRISMA-ScR headings so it can be reformatted for Systematic Reviews, BMJ Open, JBI Evidence
Synthesis or Scientific Data (Analysis).

## 15. Engineering constraints that are part of the method

- Python 3.12; stdlib plus requests, numpy, scipy, pandas, matplotlib, statsmodels, pyyaml;
  versions pinned in `requirements.txt` and written to `analysis/build_info.json`.
- Every module is an argparse CLI with `--run-dir`, `--limit`, `--dry-run` and `--run-date`.
  All network runs go through WSL. Nothing is written outside `spine_data_review/`; no dataset
  is downloaded by the review code.
- `<run-dir>/requests.log.jsonl`, one line per HTTP attempt: `{ts, source, query_id, attempt,
  method, url, params, status, elapsed_ms, bytes, cache_sha1, from_cache, credential
  (name|none), error}`. `url` and `params` are secret-stripped: any parameter named `api_key`,
  `apikey`, `key`, `token`, `access_token`, `email`, `mailto` and any `Authorization` header is
  replaced by `<redacted>` before logging; the `mailto` value is public but is redacted so the
  log can be published without review.
- `<run-dir>/raw/<source>/<sha1>.json`: the raw response body, sha1 over `method + canonical
  secret-stripped URL + sorted params + body`. `--replay` never touches the network and fails
  loudly on a cache miss.
- `<run-dir>/records/<source>.jsonl`: one line per returned item, sorted by record id:
  `{record_id, source, query_id, retrieved_at, ids: {doi, pmid, pmcid, arxiv, url, repo_id},
  title, abstract_or_description, year, type, raw}`; `raw` holds the source's own fields.
- Rate ceilings and back-off as in `information_sources.md`.
- Deterministic output: sorted keys, sorted records, seed 20260919 for every random draw; the
  only wall-clock values are retrieval and probe timestamps; the run date is `--run-date`.
- Credentials are read by name; no credential value is ever printed, logged or committed.

## 16. Ethics, funding, competing interests, roles, standing limitations

No human participants; only published descriptions and public metadata are processed. Funding
and competing interests are stated in the manuscript. The authors maintain datasets under
review (CTSpinoPelvic1K; FluoroCap if I4 holds); this is disclosed and those datasets are
charted, verified and scored by an author who did not create them.

Standing limitations, written now and reported under PRISMA-ScR item 20 whatever the results:
(1) the pooled summaries of SAP A5 and A6 are not part of the JBI scoping design and are
secondary and illustrative (section 3); (2) no access request is ever sent, so
`request-to-authors` and `unavailable` are unrequested outcomes measured on two days; (3) one
reviewer screens the full title/abstract set, with dual screening on a stratified sample and on
the whole description-review stage (section 7.3); (4) SO4 (grid coverage) is author-specific
and not reproducible by a second team; (5) raw response caches for sources whose terms restrict
redistribution are published as identifiers and hashes only (`information_sources.md`).

Roles. Reviewer 1 (search, prescreen, screening, charting): the PI. Reviewer 2 (dual
screening sample and description review, blind re-charting of max(25, 20 %) of the datasets
before verification, verification): named at registration.

## 17. Timeline

Count-only pilot search 2026-09-19 → protocol frozen 2026-09-19 → OSF registration → full
search run (recorded `--run-date`) → known-item identifier check and recall →
prescreen and screening → description review → charting, enrichment and first probe → second
probe (≥ 48 h later) → appraisal → analysis → manuscript → search update before submission →
submission.

## 18. Known-item set (frozen with the protocol)

Datasets already known to the authors, used for search validation (6.4) and included through
the other-methods arm regardless of retrieval. The machine-readable form with a DOI, PMID or
canonical URL, a normalised title, the year and the match rule for every row is
`screen/known_items.csv`; the table below is its summary. `role` is `recall` (counts in the
recall denominator), `I1-test` (a body-region dataset entered to test criterion I1; outside
the denominator) or `excluded-I4` (no public record; outside the denominator). XR = projection
radiography.

| Known item | Role | Modality | Note |
|---|---|---|---|
| VerSe (2019, 2020) | recall | CT | vertebra masks; L6 and T13 in the label scheme; one lineage |
| CTSpine1K | recall | CT | vertebra masks |
| TotalSegmentator (v1, v2) | recall | CT | whole-body masks; no L6/T13 name; one lineage |
| CTSpinoPelvic1K | recall | CT | authors' own; public record exists |
| CTPelvic1K | recall | CT | pelvis with sacrum |
| RibFrac | I1-test | CT | rib fractures; no spine claim in its description and *rib* is not in BLOCK_S, so it tests I1, not the search |
| RibSeg (v1, v2) | I1-test | CT | rib masks derived from RibFrac; moves to `recall` only if a quoted spine claim is recorded at charting (deviations log) |
| SpineWeb collections (CSI 2014, xVertSeg, Glocker centroids) | recall | CT | historic challenge sets, one row each in the CSV |
| RSNA 2022 Cervical Spine Fracture Detection | recall | CT | Kaggle |
| CT-ORG | recall | CT | bone class |
| CADS | recall | CT | whole-body |
| AbdomenCT-1K, FLARE22, AMOS 2022, autoPET, SAROS, LIDC-IDRI | I1-test | CT | spine visible; included only if I1 holds |
| NHANES II lumbar and cervical films | recall | XR | landmarks on a subset; `year` = digital release |
| BUU-LSPINE | recall | XR | AP + lateral lumbar, end-plate lines |
| CSXA (cervical spine X-ray atlas) | recall | XR | per-vertebra |
| VinDr-SpineXR | recall | XR | lesion boxes |
| AASCE 2019 / BoostNet | recall | XR | AP whole-spine landmarks |
| Mendeley 5jdfdgp762 | recall | XR | lateral lumbar corners |
| IEEE DataPort lateral full-spine | recall | XR | unannotated |
| Spinal-AI2024 | recall | XR | machine-generated landmarks; E4 unless its parent is public |
| FluoroCap | excluded-I4 | XR (fluoroscopy) | figure-derived, authors' own; no public record on the freeze date |
| MultiCaRe, Open-PMC-18M | recall | XR/CT figures | figure-derived parents |

Identifiers the authors could not confirm at the freeze are left blank in the CSV with
`match_rule = title-year` and are filled at the pre-run identifier check (6.4), each fill a
deviations-log row. Any query revision that follows the recall check is logged with the items
that drove it.

## 19. Deviations from protocol

Every departure from this protocol is entered here before the affected step is rerun where
possible, otherwise on discovery, and reproduced verbatim in the manuscript's appendix.
Entries are never deleted. Format: date, section, as written in v1.0, change, reason, effect
on results, entered by.

Dated 2026-09-19 and 2026-09-20. Twenty-seven rows: nine from the first live availability run and
its review, three from the review of the literature-search module before the full search and four
from its second review (2026-09-20), three from the first live repository-search run, one from the
queries-YAML check, one recording a scope decision taken before the first search, and the rest from
integration, the review of the statistics module and the quality rubric. None changes an eligibility
criterion or a query string; the scope row is the record of a widening that was considered and
declined. One changes an analysis:
the no-abstract rule of 7.2 moves records that no source gave an abstract for out of fail:M and
fail:D and into `uncertain`, and adds a row to the PRISMA-ScR flow so the loss is a number rather
than a silent reattribution.

Dated 2026-09-24. Six rows from the search of the review run (run date 2026-09-23), entered by the
agent that ran it and awaiting GS's review: the re-observation of requests that did not answer, the
Springer page size, arXiv from a grid compute node, bioRxiv/medRxiv not answering, two corrections to
how the run is audited, and the interrupted chain. None changes a query string, an eligibility
criterion or an analysis.

| Date | Section | As written in v1.0 | Change | Reason | Effect | Entered by |
|---|---|---|---|---|---|---|
| 2026-09-20 | 4 (I1), 8 (BLOCK_S), title, RQ1 | population is public spine imaging datasets; I1 excludes chest, abdomen and pelvis datasets with no spine annotation and no spine-specific description; `*rib*` is absent from BLOCK_S; RibFrac and RibSeg are frozen `I1-test` negative controls | **no change.** A widening proposed on 2026-09-19 (rib datasets eligible as their own category; population extended to any CT or radiograph whose field of view includes a vertebral body, charted in two tiers; projection stratification; storage-planning fields) was considered and declined before the first search | two of the four proposed amendments reverse this protocol rather than extend it. I1 was written with an argument against exactly this widening ("the count of 'spine datasets' would become a count of body CT"), and `*rib*` was excluded on purpose so that RibFrac and RibSeg could serve as negative controls. Carrying them as amendments would have changed the title, RQ1 and an eligibility criterion, which is a new pre-registration and not an amendment to this one | none. The frozen queries, the 30-item known-item set and the recall denominator all stand. Projection stratification and per-dataset size were already in the charting form and the analysis plan, so they need no amendment. The widening is deferred to a second review with its own registration | GS |
| 2026-09-19 | 10, P22 | final URL matching `login`, `signin`, `sign-in` or `auth` | whole-token match on host, path and query of the final URL, firing only after a redirect or with `WWW-Authenticate` present | the substring form matched `authors`, `authorized` and `author-data` on 2xx pages with no login involved | pages under such paths classify by P15, P20 or P16–P19; the `/authors-dataset/` fixture gives P20, not P22 | GS |
| 2026-09-19 | 10, P16–P19 | "Generic 200 HTML" | the text rules read 2xx HTML only; a 401 or 403 body never classifies and falls to P22 | the code applied the text rules to any HTML body, so a 403 page saying "apply for access" gave P16 | such pages are `auth-required` for the verifier | GS |
| 2026-09-19 | 10, regex block | patterns printed without a flag | DUA_RE, REG_RE, REQ_RE, PAY_RE and NEAR_RE are matched case-insensitively (`re.I`) | the BUU-LSPINE P16 hit ("END-USER LICENSE AGREEMENT") depends on it | none on the pattern strings, which are identical to the module's | GS |
| 2026-09-19 | 10, generic method | every 2xx HTML page runs P20 and P16–P19 | a site root (path `/`, no query) that is not a DOI is `unresolved` (P21) | ieee-dataport.org's homepage was classified `registration` (P18) from its own text | site roots go to the verifier | GS |
| 2026-09-19 | 10, generic method | "Nothing beyond the first 64 KiB of any URL is ever fetched" | a repository's own API answer (JSON record or file listing: Zenodo, Figshare, Dryad, OSF, DataCite, Mendeley, NBIA, Hugging Face, GitHub) is read whole; landing pages and files stay capped | the fields the rules read sit anywhere in the record; one Hugging Face listing was 149 kB | none on classification; no dataset file is fetched | GS |
| 2026-09-19 | 10, generic method; 15, search path | three attempts with back-off | a request that fails on every attempt (transport error, persistent 429 or 5xx) is cached like any other, so `raw_sha1` always names a file and `--replay` reproduces the failure. Extended from the availability probe to every search request (`sdr.common.RateLimitedSession.get`, `sdr.repo_run._get_bytes`): the envelope carries `error` and `attempts` beside the status | failed probes wrote no cache file, and replay of a run holding a P23 raised; on the search path the same hole made a completed run unreplayable altogether, because Figshare's deliberate 500 (the term-ceiling split), OSF's four transport errors and the Papers with Code dump's SSLError were never cached | a fresh observation needs a fresh run dir; `make replay-check` replays a run from its own cache into a fresh directory and diffs the two | GS |
| 2026-09-19 | 10, P13 Mendeley | "DataCite record + landing page" | file evidence comes from Mendeley's public API listing (the landing page is a script shell without anchors); "embargo" in the landing text is `unavailable`; a findable DOI alone never fires P13 | Mendeley mints a findable DOI for embargoed sets too, and P13 requires files that answer | mendeley-5jdfdgp762 is open-download only when a listed file answers 200 or 206 | GS |
| 2026-09-19 | 10, GitHub route | repos API | credential-free runs make one live call per minute (the 60/h anonymous ceiling); an exhausted ceiling is `unresolved` (P21) with the reset time, or waited out when the reset is under 120 s away | a 403 from the limit fell silently to the generic method with a different rule and class | slower runs; the machine class no longer depends on how many GitHub-hosted datasets precede it | GS |
| 2026-09-19 | 6.4 and 18, known items | ct-org DOI 10.7937/tcia.2019.tegm3ic5; csxa URL github.com/CSXA-dataset; ieee-dataport-lateral-full-spine URL ieee-dataport.org/ | ct-org 10.7937/tcia.2019.tt7f4v7o (doi.org 302 to the collection page); csxa github.com/yran888/CSXA-dataset; ieee-dataport-lateral-full-spine DOI 10.21227/pacw-ws92, URL ieee-dataport.org/documents/lateral-full-spine-x-ray-dataset | the written DOI answers 404 at doi.org and DataCite; the GitHub organisation page answers 404; the site root is not a record (identifier check of 6.4, run 2026-09-19) | three probes that read `unavailable` or `registration` from a wrong address now probe the record; match rules unchanged | GS |
| 2026-09-19 | information_sources.md L2 | `resultType=lite` at search, `core` only at charting | `resultType=core` is sent at search time; endpoint, strings, paging and hit counts unchanged | `lite` carries no `abstractText`; the prescreen (7.2) reads title + abstract, so a record found only by Europe PMC (PMC-only articles, `SRC:PPR` preprints, the `HAS_DATA:y` set of `epmc_02`) would have been screened on its title alone and fallen to fail:M or fail:D with nothing in the flow to show it | Europe PMC-only records reach the prescreen with their abstract; records also found elsewhere were already merged with the longest abstract | GS |
| 2026-09-19 | information_sources.md L1 | "If the count exceeds 10,000, the string is re-run with `[dp]` ranges" | the threshold is 9,999: NCBI history paging answers HTTP 400 above `retstart` 9,998 (verified live; 9,999 records per string are addressable); a `[dp]` range still above 9,999 is retrieved to 9,999 and `cap_hit` records it | at 9,999–10,000 hits the last page was one record short with no note, and a range above 9,999 broke at `retstart` 10,000 with only a status line in `notes` | none at the recorded counts (`pubmed_01` 5,948, `pubmed_02` 973); a truncation, should it occur, is now a `cap_hit` | GS |
| 2026-09-19 | information_sources.md L7 | `select=DOI,…,relation,subject` | `author` added to the select list | merge rule 5 (first author + year + title) needs the family name, which the adapter already read; the parameter as sent and as written now agree in Appendix A | none on hit counts or paging; one more field per item | GS |
| 2026-09-19 | 7.3, 14 | `screen/decisions.csv` with the eleven columns of 7.3 | the file is `data/screening/decisions.csv` (`screen/` is still read as a fallback) and carries two further columns, `full_text_retrieved` (`yes`/`no` on a `full-text` row) and `arm` (`search` or `other`) | the flow of 7.7 counts "sought for retrieval, not retrieved" and separates the known-item and citation-chasing arm from the search arm, neither of which the eleven columns record; `data/` collects everything a person types so a diff of it is a diff of human decisions | none on results: the eleven columns are unchanged and `sdr/stats.py` reads the two new ones for the flow only; the header was in place before the first decision | GS |
| 2026-09-19 | 13 (b) | `build.sh` fails if any defined macro is unused | enforced only by `build.sh --strict` (`MANUSCRIPT_FLAGS=--strict` in the Makefile), which the review run passes once every `analysis/*.json` exists; a build with pending markers (the smoke chain, and the review run until the unwritten modules produce their files) runs without it | a macro whose producer is not yet written renders as a red pending marker rather than a number, and 13 (b) would make the manuscript unbuildable until the last module exists; every build prints its pending list | none on the submitted manuscript, which is built with `--strict`; interim builds show pending markers in red | GS |
| 2026-09-19 | 6.1, information_sources.md header | `sdr/terms.py` regenerates the strings and `tests/test_terms.py` fails the build on a one-byte difference | neither was written; `queries/literature.yaml` and `queries/repositories.yaml` are materialised by hand and `tests/test_queries_yaml.py` (run by `make protocol-check`, `make manuscript` and `manuscript/build.sh`) fails on a one-byte difference from information_sources.md for every entry marked verbatim, and on a run whose queries.json records a string, endpoint, date-filter mode or raw-cache flag other than the planned one | the YAML headers claimed a generator that did not exist, and the adapters read the markdown while the appendix printed the YAML with nothing checking that they agreed | none on any string (all 264 verbatim entries were byte-identical when the test was first run) | GS |
| 2026-09-19 | 6.3, information_sources.md "What is recorded" | `hit_count_api` with no unit, and the roles search/pilot/chase/enrich | `unit` ("records", "figures", "files", "harvest") recorded on every query, and the roles `supplement` (the two mention harvests), `fallback` (the Papers with Code dump) and `probe` (the OpenDataLab endpoint probes) added | the sources do not count the same thing: Open-i reports figures (43,095 for 75 articles), Wikimedia Commons files, PhysioNet, TCIA and grand-challenge the size of a listing filtered locally, and those totals were being summed with Zenodo's record counts | `hit_count_api_total`, `flow.json` per-source hits and Table 2's Hits column are summed over `unit == "records"` and `role == "search"` only; other units are reported separately and labelled | GS |
| 2026-09-19 | 6.3, information_sources.md "What is recorded" | `n_requests` per query | `n_failed_requests` and `partial` recorded per query, and the terminal response envelope cached whatever its status | every paging loop reads a failure as end-of-results, so eight failed attempts on `openi_01` were written as a complete search (24 hits against 147 on a second run) and `osf_10`/`osf_14` returned zero records in one run and eight in another, with only requests.log.jsonl to show it; and a raw cache holding only the successes could not replay a run at all | a truncated query is marked partial in queries.json, counts.json, `flow.json` and Table 2; `--replay` reproduces the failure instead of raising ReplayMiss | GS |
| 2026-09-19 | information_sources.md R14 | two candidate endpoints `odl_01`, `odl_02` | a third, `odl_03` (`opendatalab.com/api/datasets/search?keywords=`), probed and recorded by the adapter on the first run, added to the grid and to repositories.yaml | the adapter tried it after the first two failed and queries.json carried an id the protocol did not name | none: it answered 200 with an empty object, so OpenDataLab remains `no-public-api` | GS |
| 2026-09-19 | information_sources.md R9 | without `~/.kaggle/kaggle.json` the adapter records `needs-credentials` with zero hits | `datasets/list` answered 200 with hits to the unauthenticated request; the run records `credential-free` with those hits for `kaggle_g01`–`g35` and `needs-credentials` (401) for `competitions/list` (`kaggle_c01`–`c05`); `kaggle_mention` runs as written; repositories.yaml `credential_mode_expected` updated to match | the endpoint's anonymous behaviour differed from the written expectation | more Kaggle records than v1.0 foresaw without a credential; none on any string | GS |
| 2026-09-20 | 7.2 | prescreen outcome is `pass`, `fail:<S\|M\|D>`, `uncertain` (repository and figure sources) or `pass:non-english-route` | a record found only by literature sources and carrying no abstract in any of them is `uncertain` ("no abstract in any source that found this record"), decided before `MODALITY_RE`, and counted as its own flow row | Semantic Scholar elides the abstract of every closed-access paper (406 of the 1,000 records on the first `s2_01` page, 405 of them failing the regexes on their title alone; `s2_01` reports 11,631 hits), so about 4,700 records would have reached the prescreen with a title only and been recorded as "no modality term" or "no dataset term" — a reason that was never tested. Europe PMC's hole was closable by a parameter (`resultType=core`); this one is not | the records go to reviewer screening; the PRISMA-ScR flow gains one row and loses those exclusions from fail:M and fail:D. Records Semantic Scholar shares with another index were already repaired by the merge | GS |
| 2026-09-20 | information_sources.md L2 | `abstractText` stored as Europe PMC returns it | the JATS-derived markup is stripped before the record is stored, as Crossref's abstracts already were | `resultType=core` returns `<h4>Objectives</h4>…`; the merge keeps the longest member abstract, so the marked-up Europe PMC copy displaced the clean PubMed one for every record both found, and a tag boundary can split a token the regexes would otherwise match (`L<sub>5</sub>`, `<i>in vivo</i>`) | no prescreen verdict changed in the six Europe PMC records of the review run; what reaches the screening sheet, the charting `quotes` and the manuscript is clean text. The raw envelopes keep the markup | GS |
| 2026-09-20 | information_sources.md L5 | one fetch per page; `hit_count_api` is the feed's `<opensearch:totalResults>` | an empty feed is refetched three times under `retry<n>` cache keys while the query has addressed nothing (`start` 0) or `start` is below `totalResults`, and a recovered page's `totalResults` replaces the bad feed's; a page still empty on four attempts at `start` 0 with no count in hand records `hit_count_api` null and a note, not zero | arXiv answers HTTP 200 with a feed carrying no entries, and in one form `totalResults` is zeroed too, so `start >= totalResults` held at 0, no retry was attempted, and the query ended with hits 0, retrieved 0, `cap_hit` null and empty notes — a silent zero that would wipe the whole arXiv row (`arxiv_01`, 185 hits in one page) without failing the run, and be cached for the rest of that run dir | none on a healthy run; a wiped row is now a null count with a note instead of a zero | GS |
| 2026-09-20 | information_sources.md L6 | monthly intervals from 2013-11-01 and 2019-06-01 "both to 2026-12-31" (the two fenced blocks and `queries/literature.yaml` `intervals.to`) | the harvest runs to the month of `--run-date`; the protocol text, both fenced blocks and the YAML now read "to the run date" | the adapter already bounded the interval list by the run date, so up to six months beyond it were being requested and returning nothing, and `queries.json` recorded the truncated list while Appendix A's source said otherwise | none on records retrieved; the protocol text and Appendix A now state the same window | GS |
| 2026-09-19 | 6.3, information_sources.md "What is recorded" | `credential_mode` vocabulary keyed, credential-free, needs-credentials, html-fallback, no-public-api, retired | `not-run` added for a YAML id that has no adapter in this version (MultiCaRe `multicare_01`/`02`, Open-PMC-18M `openpmc_01`–`12`, charting-time routes): the run writes the entry with `hit_count_api` null and the YAML `not_run_reason`, so Methods, Table 2 and Appendix A count the same sources; `n_fetched` (items the API returned before any local filter) recorded beside `n_retrieved` for the literature indexes; Open-i's two image-type runs recorded under the one yaml id (`n_requests` counts both, notes carry each total) instead of `openi_NN_c`/`_xg` | Table 2 had presented unrun ids as executed and the flow could not tell a paging failure from a local filter | none on counts of retrieved records; Table 2 gains no phantom rows | GS |
| 2026-09-19 | quality_rubric.md row 1 (Q4) | score 1 requires at least one variant with `how_labelled` in {`derivable-from-labels`, `reported-in-text`, `excluded-by-design`} | a variant with `how_labelled = explicit-label` but `n_subjects_with` or `n_subjects_assessed` null also scores 1, on the row's own reading "a label scheme that could carry it" | row 2 needs `explicit-label` **and** both counts, and row 0 needs every `how_labelled` in {`not-labelled`, `unknown`}, so an explicit label without a published count fell through both and would have scored 0 — the same score as a dataset that never mentions the variant | Q4 = 1 for such datasets; the Q4 rule string in `analysis/quality.json` names this row, and the rubric's row 0 and row 2 are unchanged | GS |
| 2026-09-20 | information_sources.md line 5 and "What is recorded for every query"; 6.3 | every source "is queried by `sdr/search.py --source <name>`", `sdr/appendix.py` renders the query record "to `tables/search_strings.tex`", and the protocol files name `sdr/prescreen.py`, `screen.py`, `analyse.py`, `numbers.py`, `report.py`, `validate.py`, `meta.py`, `probe.py`, `enrich.py`, `sampling.py`, `reliability.py`, `figure_counts.py` and `terms.py`; the recorded fields are the list given there and `credential_mode` is one of six words | the runners are `sdr/search_literature.py` (L1-L7 and S1), `sdr/search_repositories.py` (R1-R8), `sdr/search_platforms.py` (R9-R14) and `sdr/search_figure_routes.py` (F1, F4-F8, the two mention harvests), sharing `sdr/repo_run.py`; Appendix A is `sdr/manuscript_tables.py::t_search_strings` and Table 2 `::t_sources`, both rendered by `sdr/manuscript.py`, which also writes `tables/numbers.tex`; `prescreen.py` and `screen.py` are `sdr/dedup_prescreen.py`; `analyse.py`, `numbers.py` and `report.py` are `sdr/descriptives.py`, `sdr/stats.py`, `sdr/flow_counts.py` and `sdr/manuscript.py`; `validate.py` is `sdr/chart.py`; `probe.py` is `sdr/availability.py`; `terms.py`, `meta.py` (the primary GLMM of A5.2), `reliability.py` (A4.5), `enrich.py`, `sampling.py` and `figure_counts.py` are not written, and the manuscript prints a pending marker wherever one of them would have produced a number; the recorded-field list gains `n_fetched`, `unit` and `raw_cache_note`, and `credential_mode` gains `not-run` and `mendeley-via-datacite` (R5's front end reports no total and the route of record is DataCite `prefix=10.17632`) | the frozen files named fifteen modules that do not exist, so a reader following the protocol to the code that produced Appendix A found nothing, and three fields and two credential modes that every run writes were absent from the list that says what is recorded | none on any number: names, recorded fields and vocabulary only | GS |
| 2026-09-24 | 15; this section, row of 2026-09-19 on caching failures | a request that failed on every attempt is cached, and "a fresh observation needs a fresh run dir" | within one run dir, a request whose cached envelope records a non-answer (an `error`, status 0, 429 or 5xx, or an edge refusal 401/403/406) is sent again when `SDR_REOBSERVE` names a label and `SDR_REOBSERVE_SOURCES` lists its source (`sdr.common.reobserve`). The failed envelope and its log lines stay where they are; the new answer is cached under the same key salted with `\|reobs:<label>`; label and sources are written to the invocation in `run_meta.json`. A `--replay` with the same two variables serves the new answers, one without them reproduces the first observation | the search of the review run (about 5,400 requests, 4.1 GB of cache, three hours) ended with about twenty queries whose requests did not answer: OpenAlex and Semantic Scholar transport errors, one DataCite page and several Open-i pages timing out, a Dryad 429. A fresh run dir would have re-sent every request and re-drawn every source's answer to repair them | label `second-pass`, 2026-09-24. Recovered: `openalex_01` 200 → 15,059 of 15,058, `openalex_02` 0 → 1,002, `s2_01` 0 → 11,647 of 11,648, `datacite_03` 4,000 → 5,042, `dryad_g31` answered, `openi_04` 2,370 → 3,808, `openi_05` 0 → 1,110 of 3,950. Still partial: `datacite_01` (page 2 timed out again; 1,000 of 2,042) and `openi_05`–`07`, `09`, `12`–`18` (Open-i answered HTTP 200 with its HTML error page). A request first sent and failed during the labelled pass has no salted answer, and a `--replay` serves its failure (found when the first replay raised ReplayMiss on `openi_05`). An offline replay of the whole search into a fresh directory with the label reproduces all 25 record files byte for byte (`tests/diff_runs.py`); `queries.json` and `counts.json` differ only in the host note on `arxiv_01` | Claude (agent), for GS |
| 2026-09-24 | information_sources.md S1 | `p=100` | `p=25` | on this key's plan the Meta API answers `p=100` with 403 "This is a premium feature" whatever the constraints; `p=25` answers 200 with the same total | `springer_01` 432 of 432 in 18 pages; the first observation (403) stays in `raw/` | Claude (agent), for GS |
| 2026-09-24 | 15 | every network run goes through WSL | `arxiv_01` re-observed from a grid compute node (Slurm job 40429469) in a partial copy of the run dir holding the adapter's inputs and the cached 406, then merged back by `tests/merge_reobservation.py`, which records the host on the invocation | `export.arxiv.org` answers the WSL address HTTP 406 for every non-browser client and the grid node 200 (probe job 40429437). A browser TLS fingerprint was also answered from WSL and was not used: it would defeat a refusal the service placed on that address | `arxiv_01` 186 of 186 | Claude (agent), for GS |
| 2026-09-24 | information_sources.md L6 | monthly dumps harvested and filtered locally | no change to the method; a month whose first page has an empty or unparseable body is recorded as not answered, and a query with no answering month has `hit_count_api` null instead of 0 | `api.biorxiv.org` answered HTTP 200 with empty bodies for all 243 monthly intervals on 2026-09-23 and completed no TCP connection from WSL or a grid node on 2026-09-24 | `biorxiv_01` and `medrxiv_01` contribute no records to this run; preprints reach it only through Europe PMC (`SRC:PPR` inside `epmc_02`) and the other indexes, and the L6 cross-check against Europe PMC cannot be computed | Claude (agent), for GS |
| 2026-09-24 | 15 (`check-run`); information_sources.md F1 | the wallclock rule read every field of a record except `raw` and the abstract; an Open-i page that is not JSON ended its paging loop silently | the wallclock rule skips the fields a record copies from its source (`title`, `ids`, `canonical`, `first_author`, `related_identifiers`, `concept_doi`); an Open-i answer that is HTTP 200 but not JSON is counted as a failed request | the first full run failed wallclock on 39 dates inside DOIs, titles and repository names, which are the sources' text, not a clock of ours; Open-i's HTML error page ended eleven figure queries as though complete | none on any record; eleven Open-i queries are now marked partial, as they are | Claude (agent), for GS |
| 2026-09-24 | 17; README "Reproduce" | `bash run_all.sh --run-date 2026-09-23` runs every stage in one chain | the chain was cut at `check-run` by the end of the operator's session (SIGHUP), after the search had finished; the remaining stages were run one at a time with `make <stage> RUN_DATE=2026-09-23` in the same run dir (a copy of the review directory outside OneDrive, as README advises for a full search) | the search is three hours of network; re-running it to resume a stage would have re-drawn every answer | none; the stages after `dedup` wait for the human screening of 7.3, as the protocol intends | Claude (agent), for GS |

Known points where the plan depends on run-time facts and a deviation is foreseeable (each
will be a row above if it occurs): Papers with Code retirement (probe then static dump);
undocumented or credentialed endpoints at Mendeley Data, OpenDataLab, KoreaMed, Redalyc,
SciELO, grand-challenge.org, PhysioNet (each has a named fallback); Kaggle without
`~/.kaggle/kaggle.json` (`needs-credentials` plus the mention harvest); Wikimedia Commons
category names that no longer resolve; the OSF registration DOI once assigned; the LLM model
named in 7.4 being unavailable on a screening date (columns left empty, no substitute);
Springer Meta API date-constraint names differing from those written; Crossref rejecting a
repeated `type` filter (three passes instead); Zenodo clauses returning zero hits at the
pre-run clause check; known-item identifiers that do not resolve; the D-fail audit stratum
exceeding 2 % inclusions (re-routing, 7.2).

### Pre-registration review notes

Before the freeze, two methodological reviews of this protocol (a methodologist's and a data
engineer's) produced a list of fixes. All were applied except where a fix would have weakened a
predefined criterion or was superseded by a later fix on the same point. Those cases, recorded
here so the reasoning is not lost:

| Point | Fix proposed | Disposition |
|---|---|---|
| Section 7.6 version rule | Define the 50 % rule as (n_large − n_small) / n_large > 0.5 and recheck the VerSe and TotalSegmentator examples | Not applied as written: a second fix asked for the percentage rule to be deleted because any threshold splits one lineage into two datasets and double-counts subjects. The lineage rule (one dataset per lineage; separate only when subjects are stated to be disjoint) replaces it; the two examples are restated under that rule. |
| SAP A3.2 numerator | Make the protocol's stricter numerator (open-download **and** the probed file URL answered 200/206) the primary row | Not applied as written: a later fix showed that `file_url_probed` exists only where enrichment found one (repository APIs), so open datasets on institutional servers would fail the primary numerator by construction. The route-based numerator is primary; the file-URL confirmation is a second row with its own denominator. The text is identical in section 10 and SAP A3.2. |
| Section 7.2 audit sample | Stratify 100 / 50 / 50 by source class, or restrict to records matching at least one positive regex | Superseded by the block × source-class stratification (150 D-fail, 100 M-fail, 50 S-fail) of the later fix, which contains the source-class split and adds the D-fail action rule. |
| Rubric Q7 host redirect | Exempt doi.org, hdl.handle.net and repository hosts from the "different host" penalty | Moot: Q7 was rewritten to score probe outcome only ("access verified by probe") and no longer compares hosts. The host table of section 10 is still used for `host_type`. |
| SAP A5.3(d) | Name `BinomialBayesMixedGLM.fit_vb()` or drop (d) | Dropped, because the later fix made a logit random-intercept model (adaptive Gauss–Hermite, implemented in `sdr/meta.py`) the primary estimator; a variational Bayes fit would then be a second GLMM with a different estimator and no added information. |
| Section 13 typed digits | Either forbid all bare digits or reword to "two or more digits" | Applied in the stricter form (all bare digits in Abstract and Results), because single-digit counts are the ones most easily typed and least likely to be noticed. |
| Variant enums | Two fixes proposed different `ascertainment` and `definition_class` sets | Merged: `ascertainment` = {count-from-c2, count-from-sacrum, local-morphology, report-or-text, unknown} (whole-spine counting is `count-from-c2`); `definition_class` = {castellvi-I-IV, castellvi-II-IV, castellvi-unspecified, sacralisation-lumbarisation-unspecified, count-based, other, not-defined}. |
| LLM step | Decide used or not | Decided *used* with the model, temperature and prompt hash fixed in 7.4, because the charting workflow already relies on drafted charts (section 8) and an unused-but-permitted step would have been the silent deviation. |
| Q7 "first two probes" vs "third probe on disagreement" | Both proposed | Reconciled: Q7 scores the first two probes; when a third was run because they disagreed, it scores the two that agree (`quality_rubric.md` Q7). |

---

## Appendix A. Prescreen regexes (Python `re`, flags `re.I`)

```
SPINE_RE    = r"\b(spine|spinal|vertebr\w*|lumbar|lumbo-?sacral|thoraco-?lumbar|sacrum|cervical spine|thoracic spine|scoliosis|spondylo\w*|intervertebral|pedicle)\b"
MODALITY_RE = r"(\bcomputed tomograph\w*|\bCT\b|\bCBCT\b|cone-?beam|radiograph\w*|\bx-?rays?\b|roentgen\w*|fluoroscop\w*|\bc-?arm\b|image intensifier|\bDXA\b|\bDEXA\b|dual-energy x-?ray|absorptiometry|vertebral fracture assessment|\bEOS\b|biplanar|plain films?)"
DATASET_RE  = r"\b(data\s?sets?|database|benchmark\w*|challenge|publicly available|public(ly)? (data|release)|open(-| )?(access|source|data)|data descriptor|corpus|image collection|repository|zenodo|figshare|physionet|kaggle|hugging ?face|grand-?challenge|github|download)\b"
```

Flags recorded and shown to the reviewer, never used to exclude at prescreen:

```
MRI_RE      = r"\b(MRI?|magnetic resonance|T[12]\*?-?weighted)\b"
ANIMAL_RE   = r"\b(rats?|mice|mouse|murine|porcine|pigs?|swine|ovine|sheep|bovine|canine|dogs?|rabbits?|goats?|macaques?|primates?|zebrafish)\b"
PHANTOM_RE  = r"\b(phantoms?|cadaver\w*|ex[- ]vivo|sawbones?)\b"
SYNTH_RE    = r"\b(synthetic|simulated|DRR|digitally reconstructed|GAN|diffusion model)\b"
```

The same three positive regexes are the local filter for the sources harvested in full
(bioRxiv/medRxiv, PhysioNet, TCIA, grand-challenge.org, Papers with Code dump).

Per-language variants, recorded as flags on records from F5–F8 for per-language reporting
(section 7.2); they never exclude, and F5–F8 records are not prescreened:

```
SPINE_RE_JA    = r"(脊椎|椎体|腰椎|頸椎|頚椎|胸椎|仙骨|側弯|側彎|脊柱)"
SPINE_RE_KO    = r"(척추|요추|경추|흉추|천골|척추측만)"
SPINE_RE_ES_PT = r"(columna|vértebra|vertebra|coluna|lumbar|cervical|torácica|toracica|sacro|escoliosis|escoliose)"
```
