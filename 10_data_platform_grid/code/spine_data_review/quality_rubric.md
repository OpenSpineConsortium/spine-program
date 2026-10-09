# Data-quality rubric for spine imaging datasets

Protocol 1.0, frozen 2026-09-19. Ten items, each scored 0, 1 or 2 by the rule stated; total
0–20. Every score is computed by `sdr/quality.py` from fields of the charting record
(`charting_schema.json`) and nothing else, so a score can change only when a charted field
changes, and every charted field carries a quote or an API value. The rubric measures how
usable and how trustworthy a dataset is as a source of vertebral imaging with known labels; it
does not measure the scientific value of the study that produced it, it never sees the images
(the review downloads none), and it does not affect inclusion.

## Procedure

1. `sdr/quality.py` scores every verified charting record and writes
   `analysis/quality.json` (per dataset: ten item scores with the rule that fired, the total,
   the three booleans below with the failing rule, and `derived_from`) and `tables/quality.tex`.
2. Inter-rater reliability: the second reviewer's blind re-charting of max(25, ceil(0.20 · N))
   datasets, drawn by `sdr/sampling.py` and done before that reviewer verifies anything
   (protocol section 8), is scored by the same code. Reported with the sample size (SAP A4.5):
   per-item exact agreement; per-item linearly weighted κ via
   `statsmodels.stats.inter_rater.cohens_kappa(table, wt='linear')`, reported as "not
   estimable" with raw and prevalence-adjusted agreement (PABAK) when an item has zero
   variance in the sample; ICC(2,1) on the total by Shrout–Fleiss (two-way random effects,
   single rater, absolute agreement) from the two-way ANOVA mean squares,
   ICC = (MS_R − MS_E) / (MS_R + (k − 1) MS_E + k (MS_C − MS_E) / n), with the F-based 95 %
   interval of Shrout & Fleiss (1979). Both live in `sdr/reliability.py` and
   `tests/test_reliability.py` reproduces a published example of each (the Shrout–Fleiss
   Table 2 data for the ICC; a textbook 2 × 2 table for κ) before any review data is scored.
   Disagreements are resolved by re-charting, never by editing a score.
3. Datasets with `annotation_types = ["none"]` score 0 on Q2 and Q3 by rule and are reported
   in a separate stratum in every analysis of the total (SAP A4), so that "unannotated" is not
   read as "poorly annotated".
4. A rule found ambiguous during charting is clarified in the deviations log and every
   dataset is rescored on that item by the code; the manuscript reports scores under both
   wordings if the change comes after charting began.

## Items

### Q1. Documentation

Fields: `documentation.*`, `source_record.record_type`.

| Score | Rule |
|---|---|
| 0 | `article_or_preprint = false` **and** (`repository_record_or_readme = false` **or** `description_at_least_100_words = false`): the only description is a title or a repository/challenge record under 100 words. |
| 1 | Not 0 and not 2: a description of at least 100 words that states `states_population` and `states_acquisition`, **or** `states_annotation_protocol` (or the dataset is unannotated), but not all; or an article or preprint exists without a repository record or README that documents the file layout. |
| 2 | (`article_or_preprint = true`) **and** (`repository_record_or_readme = true`) **and** `states_population` **and** `states_acquisition` **and** (`states_annotation_protocol` or `annotation_types = ["none"]`) **and** `states_file_layout_and_label_scheme`. |

### Q2. Annotation origin

Fields: `annotation_types`, `annotation_origin_by_type`, `annotator_qualification_stated`.
The origin read is that of the annotation type most relevant to level identification, in the
order of the `annotation_type` enum in `charting_schema.json`: `per-vertebra-level-names`,
`segmentation-3d`, `segmentation-2d`, `landmarks`, `bounding-boxes`, `centroids`,
`pathology-labels`, `fracture-grade`, `measurements`, `radiology-reports`,
`image-level-labels`; the first type present is read and is recorded in
`analysis/quality.json` as `q2_type_read`, so two charts with the same types score the same.

| Score | Rule |
|---|---|
| 0 | `annotation_types = ["none"]`, or the origin read is `["unknown"]`. |
| 1 | The origin read contains none of `expert-manual`, `expert-corrected-model` (it is model-generated, counting-inferred, report-derived, crowd-or-trainee or caption-derived); or it contains an expert category but `annotator_qualification_stated = false`. |
| 2 | The origin read contains `expert-manual` or `expert-corrected-model` **and** `annotator_qualification_stated = true`. |

### Q3. Annotation validation

Fields: `annotation_validation.*`, `annotation_types`.

| Score | Rule |
|---|---|
| 0 | `annotation_types = ["none"]`, or `described = false`. |
| 1 | `described = true` and not 2: a `qa_process` other than none/unknown without a statistic; or a statistic with `inter_rater_n = null` and `inter_rater_ci = null`; or a statistic computed on `fraction_of_items < 0.10` **and** `inter_rater_n < 30`. |
| 2 | `inter_rater_statistic ≠ none`, `inter_rater_value ≠ null`, `inter_rater_n ≠ null`, **and** (`inter_rater_ci ≠ null` **or** `per_structure_breakdown = true`), **and not** (`fraction_of_items < 0.10` and `inter_rater_n < 30`). |

`fraction_of_items = null` (the dataset's total in that unit is not charted) is treated as
"not < 0.10" in both rows, so a null never lowers the score. Q3 scores any comparator; the
pooling restriction to rater-vs-rater is SAP A6's, not the rubric's.

### Q4. Variant-anatomy coverage (L6, T13, LSTV)

Fields: `variant_labels.{L6,T13,LSTV}.*`.

| Score | Rule |
|---|---|
| 0 | All three `status = unknown`; or every `how_labelled` is `not-labelled` or `unknown` (a fixed L1–L5 / T1–T12 scheme and silent text). |
| 1 | At least one variant has `how_labelled` in {`derivable-from-labels`, `reported-in-text`, `excluded-by-design`} and none qualifies for 2: the dataset acknowledges the variant by a count in text, a label scheme that could carry it, or a documented exclusion. |
| 2 | At least one variant has `how_labelled = explicit-label` **and** `n_subjects_with ≠ null` **and** `n_subjects_assessed ≠ null` (labelled per subject with a computable prevalence). |

### Q5. Metadata completeness

Field: `metadata_elements` (six possible elements: age-sex; scanner-or-acquisition-parameters;
spacing-or-dicom-headers; site-and-country; inclusion-exclusion-criteria;
clinical-status-per-subject, the last also satisfied by an explicit statement of a healthy
cohort).

| Score | Rule |
|---|---|
| 0 | 0 or 1 elements. |
| 1 | 2, 3 or 4 elements. |
| 2 | 5 or 6 elements. |

### Q6. Licence clarity

Fields: `licence.*`.

| Score | Rule |
|---|---|
| 0 | `tier = unknown`. |
| 1 | Not 0 and not 2: `standard = false` (research-use-only, competition rules, DUA-only or custom terms, `tier = custom`); or `consistent = no`; or `stated_in = article` (the downloader does not see it). |
| 2 | `standard = true` **and** `stated_in` in {`repository`, `both`} **and** `consistent` in {`yes`, `single-source`}. |

`tier`, `spdx` and `standard` are looked up by `sdr/validate.py` from `licence.text` through
`licence_tiers.csv` (pattern → tier, spdx, standard), which covers CC0, CC BY, CC BY-SA,
CC BY-NC, CC BY-NC-SA, CC BY-NC-ND, CC BY-ND, ODC-By, ODbL, PDDL, MIT, Apache, GPL, PhysioNet
Open / Credentialed / Restricted, TCIA CC BY and limited-access, US public domain,
research-use-only, competition rules, DUA and "not stated"; anything else is `custom`. The
table is the list that "standard licence with a stable identifier" refers to.

### Q7. Access verified by probe

Fields: `access_probe[]`, `file_url_probed`. The route is **not** read: Q7 scores what the
probes observed, and `access_route` is a stratifier in SAP A4.3, so that openness is not
encoded in the total a second time. The scoring probes are the first two; when a third probe
was run because the first two disagreed (protocol section 10), the scoring probes are the two
that agree. Two probes two days apart do not measure stability over time, and the item is
named for what it measures.

| Score | Rule |
|---|---|
| 0 | Both scoring probes failed: each ended in a non-2xx final status or no response (P22, P23), or `method = none` on every probe (P24, P25). |
| 1 | Not 0 and not 2: exactly one scoring probe answered 2xx (or an open/restricted repository API state); or both answered 2xx with the same `classification_machine` but no file URL was confirmed 200/206 on both; or the scoring probes' `classification_machine` differ. |
| 2 | Both scoring probes answered 2xx (or a repository API state) with the same `classification_machine`, **and** `file_url_probed` answered 200/206 on both (or the repository API listed files and a listed file URL answered 200/206 on both). |

A redirect to another host is not penalised: doi.org, hdl.handle.net and every repository
host in the protocol's host table redirect by design, so the item compares probe outcomes
between the two days, never the final host against `access_url`.

### Q8. Versioning and identifier

Fields: `versioning.*`, `versions`.

| Score | Rule |
|---|---|
| 0 | `dataset_doi = null` **and** `version_identifier = null` **and** `versions = []`: the only citable object is an article or a mutable URL. |
| 1 | Not 0 and not 2. Examples: exactly one of {`dataset_doi ≠ null` with `doi_resolves_to = dataset-record`, a version identifier or non-empty `versions`} holds; `dataset_doi ≠ null` but `doi_resolves_to = article`; a dataset DOI and a version identifier without `changelog_or_versioned_records`. |
| 2 | `dataset_doi ≠ null` with `doi_resolves_to = dataset-record` **and** (`version_identifier ≠ null` or `versions` non-empty) **and** `changelog_or_versioned_records = true`. |

### Q9. Split definition and patient-level de-duplication

Fields: `split_defined`, `patient_level_dedup`, `grouping_variable_released`.

| Score | Rule |
|---|---|
| 0 | `split_defined` in {no, unknown} **and** `patient_level_dedup` in {no, unknown}. |
| 1 | `split_defined = yes` with `patient_level_dedup` in {no, unknown}; or `patient_level_dedup` in {yes, NA} with no released split; or `split_defined = yes` and `patient_level_dedup = yes` but `grouping_variable_released = false`. |
| 2 | `split_defined = yes` **and** (`patient_level_dedup = yes` **and** `grouping_variable_released = true`, **or** `patient_level_dedup = NA`). |

`patient_level_dedup = NA` (one image per subject by construction) satisfies the grouping
requirement on its own: there is nothing to group, so the absence of a grouping variable is
not a defect.

### Q10. Image-quality reporting

Field: `image_quality_reported`.

| Score | Rule |
|---|---|
| 0 | `no` or `unknown`. |
| 1 | `yes-qualitative`: quality-based exclusions with counts, or a qualitative description ("films with motion artefact were removed, n = 12"). |
| 2 | `yes-quantitative`: per-image or per-series quality metrics, reader quality grades or artefact flags released with the data. |

## Total and bands

Total = Q1 + … + Q10, range 0–20, reported as a number. Q6 (licence visible on the
repository), Q7 (probe outcome) and Q8 (dataset DOI) are all tied to hosting on a repository,
so every analysis of the total against the access route is reported three times: the full
total, with Q7 removed (0–18), and with Q6–Q8 removed (0–14) (SAP A4.3). Bands are for figures only and are never used in
a test: 0–6 low, 7–13 medium, 14–20 high. No weighting: a licence score and an annotation
score do not add in any physical sense and the sum is a ranking device, so the per-item
distributions are reported alongside it.

## "Fit for level identification" (boolean, computed, not scored)

Rules are tested in order and the first failing rule is recorded as `fit_level_id_fail_rule`:

```
F1  per_vertebra_level_names in {yes, partial}
F2  the origin of "per-vertebra-level-names" (annotation_origin_by_type) contains
    expert-manual or expert-corrected-model AND does not contain counting-inferred
    (a counting-inferred level name cannot test a counting-free method: it is the
    hypothesis under test). The list read is the one for the level names specifically:
    expert-drawn masks whose names were assigned by counting from C2 chart
    ['counting-inferred'] under per-vertebra-level-names and fail F2, whatever the
    masks' origin (schema, annotation_origin_by_type)
F3  access_route in {open-download, registration, data-use-agreement}
F4  n_subjects is not null and n_subjects >= 20
fit_level_id = F1 and F2 and F3 and F4
```

Three derived booleans, reported alongside with their own failing rule:

```
usable_for_training = F1 and F3 and F4
    (a dataset can train a level model without being able to test the failure mode)
fit_variant   = fit_level_id and any(variant_labels[v].status == "yes" for v in {L6, T13, LSTV})
fit_stitching = fit_level_id and (region ∩ {thoracic, whole-spine} ≠ ∅)
    ("whole-spine" in region iff every image covers at least C7 through S1, the one
    definition shared with projection; the projection field is not read separately)
```

`fit_stitching` names the class the project is shortest of: whole-spine films and thoracic
coverage with level names from an expert. The threshold of 20 subjects is the smallest set on
which a per-level confusion matrix is worth reading; it is arbitrary and is stated as such in
the manuscript.

## Worked example (illustrative, not a charted record)

A challenge dataset with a peer-reviewed descriptor and a README with class ids (Q1 = 2),
masks by trained annotators corrected by a radiologist with qualifications stated (Q2 = 2),
Dice between two raters on 20 volumes with a per-vertebra breakdown (Q3 = 2), a label scheme
with a class for a sixth lumbar vertebra but no published count (Q4 = 1), age/sex, vendor,
voxel size and country stated, no inclusion criteria, no clinical status (Q5 = 1), CC BY-SA
4.0 stated on the repository and in the paper (Q6 = 2), open download at the published URL on
both probes agreeing with the file URL answering 206 on both (Q7 = 2), a versioned DOI but no change log
(Q8 = 1), a released split by patient with patient ids (Q9 = 2), no quality reporting
(Q10 = 0): total 15, high band; `fit_level_id` true; `fit_variant` false (status derivable,
not yes); `fit_stitching` true if the region includes thoracic.
