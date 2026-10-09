# Data-quality rubric (predefined; protocol 1.0, 2026-09-19)

Ten items, each scored 0, 1 or 2 by the rules below, total 0–20. Scores are computed by
`sdr/quality.py` from the charting JSON; a reviewer changes a score only by changing a charted
field, so every score traces to a quote or an API field. The rubric measures how usable and
how well-described a dataset is for reuse; it does not judge the images themselves, which the
review never downloads.

Each rule names the charting fields it reads. "Stated" means a `quotes` entry supports the
field; an API-filled field counts as stated.

| # | Item | 0 | 1 | 2 | Fields read |
|---|---|---|---|---|---|
| 1 | Documentation | No article, preprint or README describing acquisition and content; only a file listing | A README or challenge page, or an article that describes the data in under one paragraph | A peer-reviewed article, preprint or data descriptor with acquisition, population and annotation sections | `source_record.record_type`, `quotes` (≥3 quotes from a document describing acquisition, population, annotation) |
| 2 | Annotation origin | `annotation_origin` is `unknown`, or annotations exist and their origin is not stated | Origin stated but includes `model-generated` without correction, `counting-inferred`, or `crowd`, or `none` (no annotations, so nothing to judge; scored 1 so that unannotated raw sets are not penalised twice) | Origin stated as `expert-manual` or `model-generated-expert-corrected` for every annotation type, with rater qualification given | `annotation_origin`, `annotation_types`, `quotes` |
| 3 | Annotation validation | `annotation_validation.type` is `none` or `unknown` while annotations exist | `qa-process-described` or `consensus-read` without a statistic | An inter-rater statistic with its value and n reported (`inter-rater-kappa`, `-dice`, `-other` with `value` present) | `annotation_validation` |
| 4 | Variant-anatomy coverage | All three of L6, T13, LSTV `unknown` | At least one of the three explicitly `yes` or `no` | At least one `yes` with `n_positive` and `n_assessed` reported, or all three explicitly `no` with the exclusion stated | `variant_labels` |
| 5 | Metadata completeness | Fewer than three of {n_subjects, n_images_or_volumes, age/pediatric, region, projection, format} are known | Three to five known | All six known (`pediatric_included` ≠ unknown counts as age known) | those fields |
| 6 | Licence clarity | `licence.tier` = `unknown` | `restricted` or a named licence stated only in the article, not on the repository record | `open` or `non-commercial` with the licence on the repository record (`licence.from` = `api` or `repository-page`) | `licence` |
| 7 | Access stability (from the probe) | Probe classification `unavailable`, `unresolved`, or the two probe days disagree | `registration`, `data-use-agreement`, `request-to-authors`, `commercial`, agreeing on both days | `open-download` on both probe days with a file URL answering 200/206 | `access_probe`, `access_route` |
| 8 | Versioning and DOI | No DOI on the dataset or its descriptor | A DOI on the descriptor article only, or a repository record without version labels | A dataset DOI (DataCite or Crossref type dataset) and versions labelled, or a single version with a concept/version DOI pair (Zenodo) | `source_record.doi`, `versions`, `checksums.from` |
| 9 | Split and patient-level de-duplication | `split_defined` = no/unknown and `patient_level_dedup` = no/unknown | One of the two is `yes` | Both `yes`, or `split_defined` = yes with the split stated to be grouped by subject | `split_defined`, `patient_level_dedup` |
| 10 | Image-quality reporting | `image_quality_reported` = no/unknown | Resolution or spacing given without acquisition parameters, or acquisition parameters without resolution | Both resolution/spacing and acquisition parameters (kV/mAs or detector, reconstruction kernel or slice thickness for CT) reported, or an explicit per-image quality assessment | `image_quality_reported`, `resolution_summary`, `quotes` |

Total = sum of the ten items. Reported per dataset in Table 3 and as a distribution in Figure 4.
No weighting; the items are presented separately as well, because a licence score and an
annotation score do not add in any physical sense and the sum is only a ranking device.

## Boolean: fit for level identification

`fit_for_level_id = true` when all of the following hold, else `false`; the rule that failed
is recorded (`fit_for_level_id_fail_rule`):

- F1. `per_vertebra_level_names` = `yes`.
- F2. `annotation_origin` contains `expert-manual` or `model-generated-expert-corrected`, and does
  NOT contain `counting-inferred` as the only origin for level names. (A counting-inferred
  level name cannot test a counting-free method; it is the hypothesis being tested.)
- F3. `access_route` in {open-download, registration, data-use-agreement}.
- F4. Item 4 (variant-anatomy coverage) ≥ 1, i.e. the dataset says something about L6, T13 or
  LSTV; a dataset silent on variants can train a model but cannot evaluate the failure mode
  the project cares about.
- F5. `n_subjects` ≥ 50 in an eligible modality.

A second, weaker boolean `usable_for_training` = F1 and F3 and F5 is also reported, because a
dataset can train a level model without being able to test it on variants.

## Reporting

- Per-item scores, total, and both booleans go in `analysis/quality.json` (with `derived_from`
  per dataset) and `tables/quality.tex`.
- Inter-rater check: the second reviewer re-charts a 20% sample; rubric totals are recomputed
  from both chartings and the intraclass correlation (two-way, absolute agreement) is reported
  with the sample size. Disagreement per item is tabulated.
- Rubric text is frozen at protocol 1.0. A change to any rule is a deviations-log row and the
  manuscript reports scores under both versions if the change occurs after charting began.
