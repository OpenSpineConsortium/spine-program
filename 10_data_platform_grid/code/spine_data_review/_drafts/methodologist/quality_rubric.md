# Data-quality rubric for spine imaging datasets

Protocol version 1.0, 2026-09-19. Ten items, each scored 0, 1 or 2 by the rule stated; total
0–20. Every score is computed from charted fields and quotes only — a rater who cannot point to
the charted field or quote that satisfies a rule gives the lower score. The rubric measures how
usable and how trustworthy a dataset is as a source of vertebral imaging with known labels; it
does not measure the scientific value of the study that produced it, and it does not affect
inclusion.

## Scoring procedure

1. Both reviewers score every dataset independently from the verified charting record, without
   seeing each other's scores. Scores are entered in `results/quality_scores_raw.csv`
   (dataset_id, rater, item, score, basis) where `basis` names the charted field or quote index.
2. Item-level agreement is reported as linearly weighted kappa across datasets, per item.
3. Disagreements are resolved by discussion with reference to the rule; if the rule is found
   ambiguous, the rule is clarified in the deviations log and every dataset is rescored on that
   item by both raters.
4. The consensus score per item and the total are written to `results/quality_scores.csv`.
5. Datasets with `annotation_types = ["none"]` score 0 on Q2 and Q3 by rule and are reported in
   a separate stratum in every analysis of the total score (SAP §4.3), so that "unannotated" is
   not read as "poorly annotated".

## Items

### Q1. Documentation

| Score | Rule |
|---|---|
| 0 | The only description is a title, or a repository/challenge record of fewer than 100 words, with no article or preprint. |
| 1 | A description of at least 100 words that states the population and the acquisition (modality, scanner or site, or inclusion criteria) **or** the annotation protocol, but not both; or an article or preprint exists without a README/data record that documents the file layout. |
| 2 | An article, preprint or data descriptor **and** a repository record or README that together state population, acquisition, annotation protocol (when annotated) and file layout with the label scheme (class ids or filename conventions). |

Basis fields: `source_record`, `quotes` with `field` in {population, acquisition, annotation_protocol, file_layout}.

### Q2. Annotation origin

| Score | Rule |
|---|---|
| 0 | `annotation_types = ["none"]`, or `annotation_origin` contains only `unknown`. |
| 1 | `annotation_origin` contains any of `model-generated`, `counting-inferred`, `report-derived`, `crowd-or-trainee`, `caption-derived` **and no** expert category; or an expert category is present but the annotator's role or qualification is not stated. |
| 2 | `annotation_origin` contains `expert-manual` or `expert-corrected-model` **and** the description names the annotators' qualification (e.g. radiologist, spine surgeon, "trained annotator supervised by a radiologist") for the annotation type that carries level names or segmentations. |

A dataset with mixed origins is scored on the annotation type most relevant to level
identification (level names first, then segmentation, then landmarks/boxes); notes says which.

### Q3. Annotation validation

| Score | Rule |
|---|---|
| 0 | `annotation_validation.described = false`, or `annotation_types = ["none"]`. |
| 1 | `qa_process` ≠ none is described (double read, adjudication, automated consistency checks) **without** a statistic; or a statistic is reported without `inter_rater_n` and without a confidence interval; or the statistic was computed on fewer than 10 % of items and fewer than 30 items. |
| 2 | An inter-rater or against-reference statistic (`inter_rater_statistic` ≠ none) is reported with `inter_rater_n` stated and either a confidence interval or a per-structure/per-level breakdown. |

### Q4. Variant-anatomy coverage (L6, T13, LSTV)

| Score | Rule |
|---|---|
| 0 | All three of `variant_labels.*.status` are `unknown`, or the label scheme cannot represent any variant (fixed names L1–L5, T1–T12 and no transitional flag) and the text is silent. |
| 1 | At least one variant has `how_labelled` in {`derivable-from-labels`, `reported-in-text`, `excluded-by-design`} — the dataset acknowledges the variant, by count in text, by a label scheme that could carry it, or by a documented exclusion with a count. |
| 2 | At least one variant has `how_labelled = explicit-label` **and** `n_subjects_with` and `n_subjects_assessed` are both non-null (the variant is labelled per subject and its prevalence in the dataset is computable). |

### Q5. Metadata completeness

Six elements: (a) age and sex distributions; (b) scanner vendor/model or acquisition parameters
(kVp, exposure, slice thickness, protocol); (c) pixel spacing / voxel size, or the DICOM headers
released; (d) site and country; (e) subject inclusion/exclusion criteria; (f) pathology or
clinical status per subject (or an explicit statement of a healthy cohort).

| Score | Rule |
|---|---|
| 0 | 0 or 1 of the six elements stated. |
| 1 | 2, 3 or 4 elements stated. |
| 2 | 5 or 6 elements stated. |

Basis: one quote per element claimed, `field = metadata.<letter>`.

### Q6. Licence clarity

| Score | Rule |
|---|---|
| 0 | `licence.tier = unknown` (no licence stated anywhere). |
| 1 | A licence or terms are stated but are custom (no `spdx`, not a named standard licence such as CC, ODC, PhysioNet, TCIA data usage policy), or `licence.consistent = no` (article and repository disagree), or the terms are stated only in a place the downloader does not see (article text but not repository). |
| 2 | A named standard licence with `spdx` or an equivalent stable licence identifier, stated in the repository record (or the download flow) and, when an article exists, `licence.consistent` ∈ {yes, single-source}. |

### Q7. Access stability (from the probe)

| Score | Rule |
|---|---|
| 0 | `access_route` ∈ {unavailable, unknown, commercial}; or the URL given in the primary describing record returns 404/410 on both probes even when a mirror is found (the published pointer is broken). |
| 1 | `access_route` ∈ {registration, dua, request-authors}; or `open-download` reached only through a redirect to a different host than the one published, or only one of the two probes returned 200. |
| 2 | `access_route = open-download`, both probes returned 200 at the published URL (or its documented repository API), and the response was the data or a repository record listing the data files. |

### Q8. Versioning and identifier

| Score | Rule |
|---|---|
| 0 | No dataset DOI and no version identifier; the only citable object is an article or a mutable URL. |
| 1 | A dataset DOI **or** a version identifier, but not both; or the DOI resolves only to the article. |
| 2 | A dataset DOI (concept or versioned) **and** a version identifier, with either versioned repository records or a change log stating what changed between versions. |

### Q9. Split definition and patient-level de-duplication

| Score | Rule |
|---|---|
| 0 | `split_defined = no` or `unknown`, **and** `patient_level_dedup` ∈ {no, unknown}. |
| 1 | `split_defined = yes` but `patient_level_dedup` ∈ {no, unknown}; or `patient_level_dedup = yes` (or NA by construction) with no released split. |
| 2 | `split_defined = yes` **and** `patient_level_dedup` ∈ {yes, NA} **and** the grouping variable (patient id or an equivalent) is released so the rule can be checked. |

### Q10. Image-quality reporting

| Score | Rule |
|---|---|
| 0 | `image_quality_reported ∈ {no, unknown}`. |
| 1 | `yes-qualitative`: a statement of quality-based exclusions with counts, or a qualitative description of image quality (e.g. "films with motion artefact were removed, n = 12"). |
| 2 | `yes-quantitative`: per-image or per-series quality metrics, reader quality grades or artefact flags released with the data. |

## Total and bands

Total = Σ Q1…Q10, range 0–20. Reported as a number; bands are for the figure only:
0–6 low, 7–13 medium, 14–20 high. Bands are not used in any statistical test.

## "Fit for level identification" (boolean, computed, not scored)

```
fit_level_id =
      (modality ∩ {CT, CBCT, radiograph, fluoroscopy, DXA-VFA, EOS}) ≠ ∅
  and per_vertebra_level_names ∈ {yes, partial}
  and annotation_origin ∩ {expert-manual, expert-corrected-model} ≠ ∅
  and n_subjects is not null and n_subjects ≥ 20
  and access_route ∈ {open-download, registration, dua}
```

Two derived booleans, reported alongside:

```
fit_variant   = fit_level_id and any(variant_labels[v].status == "yes" for v in {L6, T13, LSTV})
fit_stitching = fit_level_id and ("whole-spine" ∈ projection or region ∩ {thoracic, whole-spine} ≠ ∅)
```

`fit_stitching` names the class the project is shortest of: whole-spine films and thoracic
coverage with level names from an expert. The threshold of 20 subjects is the smallest set on
which a per-level confusion matrix is worth reading; it is arbitrary and is stated as such.

## Worked example (illustrative, not a charted record)

A challenge dataset with a peer-reviewed descriptor and a README with class ids (Q1 = 2),
masks by trained annotators corrected by a radiologist with qualifications stated (Q2 = 2),
Dice between two raters on 20 volumes with per-vertebra breakdown (Q3 = 2), a label scheme with
a class for a sixth lumbar vertebra but no published count (Q4 = 1), age/sex, vendor, voxel
size and country stated, no inclusion criteria, no clinical status (Q5 = 1), CC BY-SA 4.0 stated
on the repository and in the paper (Q6 = 2), open download at the published URL on both probes
(Q7 = 2), a versioned DOI but no change log (Q8 = 1), a released split by patient with patient
ids (Q9 = 2), no quality reporting (Q10 = 0): total 15, high band; fit_level_id true;
fit_variant false (status derivable, not yes); fit_stitching true if the region includes thoracic.
