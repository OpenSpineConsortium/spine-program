# FluoroCap: a predefined, reproducible collection of published spine fluoroscopy images

FluoroCap is a retrospective, non-interventional image collection assembled from the open
biomedical literature according to the search and inclusion protocol below. It exists to
evaluate a locked vertebral-level identification algorithm on real intra-operative
fluoroscopy, with no patient contact, no prospective imaging and no identifiable private
information. Every image in it is traceable from a statistical result back to a panel, the
figure it was cut from, the article that published it, the licence it was published under,
and the label it carries.

Protocol version 1.0, written 2026-09-13, before the collection was frozen.

## 1. Sources

Four routes lead to figures in the PubMed Central Open Access subset, so every image has a
publisher's licence statement and a stable article URL; a fifth, Wikimedia Commons, is small
but carries an explicit free licence on every file.

| Route | What it is | Query / filter | Image origin |
|---|---|---|---|
| PMC full text | Europe PMC search of open-access articles, figure captions from the PMC BioC API (Europe PMC JATS full text when BioC has no record) | query in `tools/fluorocap.py` `QUERY`; caption rules in section 3 | full-resolution figure from the PMC article page CDN |
| Open-i | NLM Open-i figure search (`it=xg`, x-ray graphics) | 84 queries listed in `tools/fluorocap_openi.py`; every query paged to its `total` | PMC CDN when resolvable; Open-i 512 px copy otherwise |
| MultiCaRe | Zenodo 10079370, CC BY 4.0, sub-figures of PMC case reports with captions | same caption rules over `captions_and_labels.csv` | PMC CDN (original figure) |
| Open-PMC-18M | `vector-institute/open-pmc-18m`, CC BY 4.0, 4,014 shards of decomposed PMC sub-figures with modality labels | same caption rules, sub-caption must carry the level, modality label or caption must say x-ray / fluoroscopy | the sub-figure as shipped (shard and key recorded) |
| Wikimedia Commons | File-namespace search, licence / author / description from `extmetadata` | 28 queries in `tools/fluorocap_commons.py`; description must name a level and say fluoroscopy / radiograph and the spine | the original upload (Commons SHA-1 recorded) |

Search date: 2026-09-13. Europe PMC hit count on that date is recorded in `articles.jsonl`
(`hitCount`), the per-query totals for Open-i in `log_openi.txt`.

## 2. Search query (Europe PMC)

```
(fluoroscop* OR "C-arm" OR "c arm" OR "image intensifier" OR "intraoperative radiograph*" OR
 "intra-operative radiograph*" OR "intraoperative X-ray" OR "intraoperative imaging")
AND (spine OR spinal OR vertebra* OR lumbar OR cervical OR thoracic OR thoracolumbar OR lumbosacral OR
 pedicle OR kyphoplasty OR vertebroplasty OR discectomy OR laminectomy OR laminoplasty OR foraminotomy OR
 "interbody" OR "spondylolisthesis" OR "scoliosis" OR "sacroiliac")
AND (OPEN_ACCESS:y)
```

## 3. Inclusion criteria (applied to the figure caption, in this order)

| Code | Criterion | Rule |
|---|---|---|
| I1 | Article is in the PMC Open Access subset | Europe PMC `OPEN_ACCESS:y`, or aggregator membership (MultiCaRe, Open-PMC-18M are built from that subset) |
| I2 | Caption states fluoroscopy, C-arm, image intensifier, or intra-operative radiography / imaging | `FLUORO_RE` in `tools/fluorocap.py` (article title may supply this for Open-i) |
| I3 | Caption or title refers to the spine | `SPINE_RE` |
| I4 | Caption names at least one vertebral level | `LEVEL_RE`: C1–C7, T1–T13 / Th1–Th13, L1–L6, S1–S2, and ranges (L4-L5, L4/5, L5-S1); MRI weightings (T1-, T2-weighted, T2*) are excluded by a negative look-ahead |

A figure meeting I1–I4 is fetched and split into panels. Each panel then carries its own label:
when the caption enumerates panels ("(a) ... (b) ...") the panel's segment supplies the levels;
otherwise the figure's levels apply to every panel.

## 4. Exclusion criteria (applied per panel; a panel is excluded when any holds)

| Code | Criterion |
|---|---|
| E1 | No vertebral level named for this panel |
| E2 | The panel's caption segment names another modality (MRI, CT, ultrasound, endoscopy, photograph, histology) and not fluoroscopy / radiography |
| E3 | Non-human subject (caption or full text names an animal species and the article is not indexed under MeSH "Humans" with a patient description) |
| E4 | Cadaver, phantom, sawbone or printed model |
| E5 | The panel classifier's probability that the panel is a radiograph / fluoroscopy frame of the spine is below 0.3. The threshold is deliberately permissive: the classifier (ResNet-18 trained on real films, caption-verified C-arm figures and 12,000 labelled non-radiograph sub-figures; `classifier_report.json`) rejects photographs, CT, MRI and histology at 0.3 but still misses some dark or collimated C-arm frames at 0.5, and the reader study is the final gate |
| E6 | Panel short side below 128 px |
| E7 | The caption identifier scan (dates, record numbers, honorifics) hit; the panel is held for review, not used |
| E8 | Human QC fail (`human_qc.csv`: image_id, status, reason, reviewer, date) |

Every panel, included or excluded, stays in the manifest with its `exclude_reason`, so any
stricter subset is a filter on columns and the number excluded under each rule is reported
in `stats.json`.

## 5. Rights: a hard gate, not a note

The article's own licence string (Europe PMC record, or the Commons file's declared licence)
is recorded for every panel as `license`, with `license_url`, `license_source` and
`license_verified_date`, and mapped to a tier:

| Tier | Licence | `commercial_training_eligible` | Derivatives (panel crops) | Redistribution |
|---|---|---|---|---|
| A | public domain, CC0, CC BY | TRUE | yes | yes |
| B | explicit written permission on file (recorded in `license_overrides.csv`) | TRUE | as permitted | as permitted |
| C | CC BY-NC, CC BY-NC-SA | FALSE | yes, non-commercial | non-commercial |
| D | CC BY-ND, CC BY-NC-ND | FALSE | no: panel extraction is a derivative | original figure only |
| E | not stated, share-alike, non-CC or publisher-specific wording, aggregator-only rows whose article was not resolved | REVIEW | unknown | unknown |

"Publicly accessible" is never taken to mean "usable"; a row with no licence string is tier E,
not tier A. Every REVIEW row that would otherwise be included is written to
`license_review_queue.csv` with the reason, and stays out of the clean corpus until a person
resolves it (resolution, resolver and date are recorded there and applied through
`license_overrides.csv`). Aggregator licences (MultiCaRe, Open-PMC-18M: CC BY 4.0) never
override the article's licence; Open-PMC-18M rows are resolved to their article by exact
caption match against the PMC captions, and stay tier E when unresolved.

**Two datasets are frozen from one manifest.** Dataset A (research corpus) is every included
panel, any tier, for exploration and development. Dataset B (clean corpus) is the included
panels with `commercial_training_eligible = TRUE` and no human-QC failure. Headline
validation numbers are reported from Dataset B; Dataset A results are reported as
supplementary. `fluorocap_freeze.py` writes both, each with its own `SHA256SUMS` and
`LOCK.json`.

**Chain of custody.** The original figure is stored unmodified under `raw/` with
`original_figure_hash`; the extracted panel under `panels/` with `panel_hash`, its box in the
figure, `splitter_version` and `splitter_confidence`; the classifier input is a documented
in-memory transform (`classifier_input_transform`); the level pipeline records the SHA-256 of
the detector and level-model weights it ran with (`infer_summary.json`). Every fetch records
the URL, UTC time, HTTP status, user agent and pipeline version, successful or not
(`fetched.jsonl`), so the collection can be repeated and any change at the source detected.

## 6. Reference standard

Two labels exist for each panel.

1. **Caption label** (`levels_panel`): the level(s) the authors wrote in the caption. This is
   the label the collection was searched by; it is author-stated, not independently read.
2. **Reader label** (`reader_1`, `reader_2`, `adjudication`): two readers qualified in spine
   imaging independently record, for each included panel, the levels visible from top to
   bottom, whether the sacrum is visible, the projection, and an image-quality score
   (1–5), blinded to the caption and the source (`reader_sheet_template.csv` carries no
   caption or URL). Disagreements go to a third reader; the adjudicated label is the
   reference standard. `ground_truth_method` records which of these a row's label came from.

Reported separately: reader 1 vs reference, reader 2 vs reference, reader 1 vs reader 2,
and caption vs reference (how often the published caption is itself wrong).

## 7. Predefined subgroups

The algorithm names a vertebra from local morphology rather than by counting from the
sacrum or C2, so the evaluation is stratified in advance by how countable the image is.
The `challenging_subgroup` column is filled from the reader labels (not from the
algorithm's output):

| Subgroup | Definition |
|---|---|
| primary | sacrum or C2 visible and at least three contiguous vertebrae visible |
| limited field of view | three or fewer vertebrae visible |
| no anchor | neither the sacrum nor C2 visible |
| single vertebra | one vertebra visible |
| transitional | caption or readers report a lumbosacral or thoracolumbar transitional vertebra |
| hardware | screws, rods, cages, needles or cement in the field |
| oblique / rotated | readers report a non-orthogonal projection |
| degenerative / pathological | fracture, tumour, infection, deformity, or advanced degeneration named in caption or reported by readers |

## 8. Endpoints and analysis (prespecified)

- Primary: per-vertebra level accuracy of the locked algorithm against the adjudicated
  reference, with a Wilson 95% confidence interval, on included panels of the primary
  subgroup.
- Secondary: the same in each challenging subgroup; per-region (cervical, thoracic, lumbar,
  lumbosacral) accuracy; agreement with the caption label; reader-vs-reader agreement (Cohen's
  kappa); error distance in levels (±1, ±2, other).
- No image in FluoroCap is used to train, tune or select the algorithm. The algorithm version
  (weights hash) and this protocol version are recorded with the results.

## 9. Preprocessing (recorded per panel)

PIL decode; convert to grey (ITU-R 601 luma); trim uniform borders (row or column standard
deviation below 14 with mean above 200, or mean below 30); split at gutter runs of at least
2 px that are bright (standard deviation below 14, mean above 200, any width) or dark
(standard deviation below 10, mean below 45, width at most 3% of the dimension, so that a
collimator shutter band inside a fluoroscopy frame never splits it), recursively (rows, then
columns, up to four levels); re-trim each panel; save as PNG at native resolution without
resampling. Panels that touch with no uniform gutter between them stay as one panel; the
reader sheet has a comment field for these. The panel's box in the parent figure
(`panel_box_r0_r1_c0_c1`) lets the cut be reproduced from the original file. On the 187
Open-i figures used to tune the rule, 96 split into two or more panels (363 panels in all).
The classifier input (224 px letterboxed grey, 0.5–99.5 percentile window) is a scoring
transform only; the stored panel is unchanged.

## 10. Integrity and versioning

- Every fetched figure and every panel carries a SHA-256 of its exact bytes, and the URL and
  UTC time it was fetched. Byte-identical duplicates across routes are collapsed (first kept).
- Every panel decodes with PIL at load; failures are listed in `figures.csv` with the error.
- `image_id` (FLUO-000001 ...) is assigned once and kept across versions (`ids.json`).
- A version is frozen with `tools/fluorocap_freeze.py`: the included panels are copied under
  their `image_id`, `SHA256SUMS` covers every file, `LOCK.json` records the manifest hash, the
  hash of the checksum file, the pipeline commit, the search query and the regular
  expressions. A frozen directory is never rewritten.

## 11. De-identification

Images are figures published in peer-reviewed open-access journals, which require
identifying information to be removed or consent for publication obtained (ICMJE). The
panels are rasterised pixel data with no DICOM header or EXIF metadata. Captions are scanned
for dates, record numbers and honorifics (E7). Nothing in the manifest links a panel to a
person beyond what the article itself published.

## 12. Files

| File | Content |
|---|---|
| `manifest.csv` | one row per panel, all columns above (`tools/fluorocap_manifest.py` docstring lists them) |
| `figures.csv` | one row per fetched figure with verification status |
| `articles.csv` | one row per article: licence, journal, abstract, MeSH, equipment / exposure / positioning / population / ethics sentences |
| `stats.json` | counts by route, licence class, region, level, projection, exclusion reason; manifest hash |
| `classifier_report.json` | held-out confusion matrices of the modality and view heads |
| `reader_sheet_template.csv` | blinded reading sheet |
| `releases/FluoroCap_v*/` | frozen versions |
