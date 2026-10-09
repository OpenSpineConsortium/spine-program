# Statistical analysis plan

Protocol version 1.0, 2026-09-19. Frozen before the search. Every analysis below names its
input file, its estimator, and the key under which its result is written in
`results/numbers.json`; the manuscript reads only from that file and from
`results/tables/*.tex`. Analyses not listed here are exploratory and labelled so in the
manuscript.

## 1. General rules

- **Software**: Python 3.12; numpy, scipy, pandas, statsmodels, matplotlib; versions pinned in
  `requirements.txt` and printed into `results/environment.json` at run time.
- **Determinism**: seed 20260919 for every random draw (dual-screen sample, prescreen sample,
  bootstrap); sorted inputs; identical outputs on rerun are asserted by a test.
- **Unit**: the dataset, unless stated. Records are the unit only in the flow diagram and the
  screening agreement.
- **Denominators**: stated in every table cell footnote or column header. Datasets with a null
  value for a variable are reported as "not reported" in that variable's table and excluded
  from that variable's percentages, with the excluded number shown.
- **Significance**: two-sided α = 0.05; 95 % intervals throughout; no adjustment for multiple
  testing beyond what is stated in §4.3, because the tests are descriptive characterisations,
  not confirmatory hypotheses, and are reported as such.
- **Proportions**: Wilson score intervals.
- **Derived datasets** (`flags.derived = true`) are counted in the descriptive tables (they are
  datasets) but excluded from subject and image totals and from every pooled prevalence when
  their parent is also included, to avoid counting one person twice; the number so excluded is
  stated.
- **Versions**: one dataset per protocol §7.6; the largest version's counts are used.
- **Numbers under ten** are spelled out in prose by the report generator (numbers in tables and
  with units stay numeric).

## 2. Flow (PRISMA-ScR items 14; numbers.json key `flow`)

Input: `runs/<run-date>/records.jsonl`, `screening/*.csv`, `charting/*.json`.

Reported per source and in total: records retrieved (paging cap reached yes/no), records after
deduplication (with the number removed per merge key), prescreen pass / fail, screened,
excluded at screening by criterion code, sent to description review, excluded at description
review by code, included records, datasets after record-to-dataset mapping. Second arm: known
items (retrieved by search / not retrieved), backward-chasing candidates, included. Search
update before submission: new records, new datasets. Figure 1 is generated from `flow.json`.

Also reported (keys `search_validation`, `screening_agreement`):

- Known-item recall = retrieved / known items, with Wilson interval, overall and per source.
- Prescreen false-negative rate = included / 200 sampled failing records, Wilson interval.
- Screening agreement: Cohen's κ on the 10 % dual-screened sample with 95 % interval
  (bootstrap, 2,000 resamples); raw agreement; count of disagreements by criterion code.
- LLM-suggestion agreement with the human decision: raw agreement and κ, reported separately
  and never combined with the human dual-screen κ.

## 3. Descriptive characteristics (items 15, 17; keys `desc.*`)

Input: `charting/*.json`.

Table 4 (one row per dataset): id, name, year, country, modality, region, projection,
n_subjects, n_images_or_volumes (unit), annotation types, annotation origin, variant labels
(three symbols), licence tier, access route, quality total, fit_level_id. Sorted by modality
then year then name.

Tables 6–7 (counts and totals): number of datasets, total subjects (Σ n_subjects over
non-derived datasets with non-null values; number with null stated), total images/volumes by
unit — each by: modality; region; projection (radiography only); annotation type (a dataset
counts once per type it carries; totals therefore exceed the number of datasets and the table
says so); annotation origin (same rule); access route; licence tier; year (histogram by year;
Figure 2 as a stacked bar by modality); pediatric inclusion; format; figure_derived and
derived flags; country (top ten and "other").

Cross-tabulations: annotation origin × modality; variant coverage (any of L6/T13/LSTV
status = yes) × modality; per_vertebra_level_names × modality; access route × licence tier.

## 4. Availability (RQ5; keys `avail.*`)

Input: `charting/*.json` (`described_as_public`, `access_route`, `access_probe.*`).

4.1 Distribution of `access_route` overall and by modality, year band (2000–2010, 2011–2016,
2017–2020, 2021–2026) and by the host type (repository vs institutional/personal URL).

4.2 **Share of "described as public" that actually downloads**: among datasets with
`described_as_public = yes`, the proportion with `access_route = open-download`, Wilson
interval; and the proportion with route ∈ {open-download, registration} (the recipe-eligible
set). Also the proportion with `classification_machine ≠ access_route` (how often the verifier
overrode the code), with the reasons tabulated.

4.3 Probe agreement between the two probe dates: proportion of datasets whose
`http_status` class (2xx / 4xx / 5xx / failure) changed, listed by id.

4.4 Figure-derived pool: for Open-i, Commons, MultiCaRe, Open-PMC-18M and the four non-English
journal APIs, the number of figures (or articles) matching Block S × Block M, per modality,
with the query date. Reported as counts only; no pooling.

## 5. Quality (SO1; keys `quality.*`)

Input: `results/quality_scores.csv`.

5.1 Distribution of the total: median, IQR, range, histogram (Figure 4), overall and by
annotated / unannotated stratum. Per-item score distributions (share at 0/1/2).

5.2 Rater agreement: linearly weighted κ per item and for the total (quadratic), with
bootstrap intervals.

5.3 **Quality vs access route**: Kruskal–Wallis H on the total across routes with at least
three datasets; effect size ε²; if p < 0.05, Dunn's pairwise tests with Holm adjustment.
Reported with the per-route medians and n.

5.4 **Quality vs year**: Spearman ρ between total score and year, with a 95 % interval from
Fisher's z; a scatter with a lowess line (Figure 4b). Also Spearman ρ between total score and
log10(n_subjects) among datasets with n_subjects reported.

5.5 Fitness: number and list of datasets with `fit_level_id`, `fit_variant`, `fit_stitching`
true, by modality; the totals of subjects they carry.

Pre-specified caveat: Q7 is derived from the access route, so the association in 5.3 is
partly built in; the manuscript reports 5.3 both with the full total and with Q7 removed
(total 0–18).

## 6. Pooled prevalence of L6, T13 and LSTV (SO2; keys `prev.<variant>.*`)

Input: `charting/*.json` → `variant_labels.<v>.n_subjects_with` (x_i) and
`n_subjects_assessed` (n_i), for datasets with both non-null, `flags.derived = false` or parent
not included, and a stated `definition`.

6.1 Eligibility for pooling: at least three datasets per variant. Fewer → reported as a table
of per-dataset proportions with Wilson intervals and no pooled estimate.

6.2 Estimator: random-effects meta-analysis on the logit scale, DerSimonian–Laird τ².
Per dataset: p_i = x_i / n_i; y_i = logit(p_i); v_i = 1/x_i + 1/(n_i − x_i). Zero cells:
0.5 added to x_i and 1 to n_i for that dataset only (continuity correction, stated in the
table). Fixed-effect weights w_i = 1/v_i; Q = Σ w_i (y_i − ȳ_FE)²; C = Σ w_i − Σ w_i²/Σ w_i;
τ² = max(0, (Q − (k − 1))/C); random-effects weights w_i* = 1/(v_i + τ²); pooled logit
ȳ_RE = Σ w_i* y_i / Σ w_i*, SE = (Σ w_i*)^−1/2; back-transformed pooled prevalence with 95 %
interval; I² = max(0, (Q − (k − 1))/Q); 95 % prediction interval on the logit scale with
t_{k−2} when k ≥ 3. Implementation: `statsmodels.stats.meta_analysis.combine_effects`
(method_re = "dl") on (y_i, v_i), with the corrections applied by our code, and a unit test
against a hand-computed three-study example.

6.3 Sensitivity: (a) Freeman–Tukey double-arcsine transform with the same DL model;
(b) leave-one-dataset-out; (c) datasets with n_i ≥ 100 only. Reported in Supplement S3; the
manuscript states whether conclusions change.

6.4 Pre-specified subgroups (reported only when each subgroup has ≥ 3 datasets): modality (CT
vs radiography); ascertainment (whole-spine count from C2 vs local morphology vs report or
text); variant definition (for LSTV: Castellvi-based vs other). Between-subgroup Q test on the
logit scale.

6.5 Figure 5: one forest plot per variant, datasets sorted by year, squares sized by w_i*,
diamond for the pooled estimate, dashed prediction interval, I² and τ² in the footer.
Captions ≤ 60 words.

6.6 Interpretation rule (written now): prevalence differs by ascertainment method, so the pooled
number is reported as "prevalence among labelled datasets" and compared in the Discussion
with the population literature, not treated as a population estimate.

## 7. Pooled inter-rater agreement (SO2; keys `agree.<group>.*`)

Input: `annotation_validation.*` with `comparable_group` non-null.

7.1 Eligibility: a group is pooled when ≥ 3 datasets share a `comparable_group` value (same
statistic and same annotation class) and each has `inter_rater_value` non-null. Otherwise the
group is tabulated only.

7.2 Estimators by statistic:
- κ (level names, pathology): random-effects DL on the κ scale; SE from the reported interval
  ((upper − lower)/3.92) when given, else the large-sample approximation
  SE ≈ sqrt((1 − κ²)/n) with n = `inter_rater_n`; datasets with neither interval nor n are
  tabulated, not pooled.
- ICC: Fisher z transform, DL, back-transform.
- Dice and mm error: no standard error is usually reported; these are summarised as median
  (IQR) across datasets with the per-dataset n, and pooled only if ≥ 3 datasets report an SD
  or interval (then DL on the raw scale).

7.3 I² and prediction interval as in §6.2; forest plot per pooled group in Supplement S4.

## 8. Grid coverage (SO4; keys `grid.*`)

Input: `on_grid.*`.

Per modality and region: number of included datasets on the grid (yes / partial / no /
unknown); subjects on the grid / subjects in datasets with route ∈ {open-download,
registration} (the reachable set); the list of reachable datasets not on the grid, sorted by
quality total descending, which is the recipe's first-run order (Table 10).

## 9. Tables and figures (item 13c)

| Object | Content | Generated by |
|---|---|---|
| Figure 1 | PRISMA 2020 two-arm flow | `sdr.report --flow` from `flow.json` |
| Figure 2 | Datasets per year, stacked by modality | `sdr.report --figures` |
| Figure 3 | Access route × licence tier, mosaic | idem |
| Figure 4 | Quality total: histogram by route; scatter vs year | idem |
| Figure 5 | Forest plots: L6, T13, LSTV | idem |
| Table 1 | Eligibility criteria | protocol §4 |
| Table 2 | Information sources, dates, hit counts | `runs/<run-date>/counts.json` |
| Table 3 | Data items | `charting_schema.json` |
| Table 4 | Characteristics of included datasets | `charting/` |
| Table 5 | Quality scores per dataset, per item | `quality_scores.csv` |
| Tables 6–7 | Counts and totals by strata | §3 |
| Table 8 | Availability outcomes | §4 |
| Table 9 | Inter-rater agreement per dataset and pooled | §7 |
| Table 10 | Grid coverage and recipe order | §8 |
| Supplement S1 | Full charting records rendered | `charting/` |
| Supplement S2 | Deviations log | protocol §17 |
| Supplement S3 | Prevalence sensitivity analyses | §6.3 |
| Supplement S4 | Agreement forest plots | §7.3 |

All figures: sans-serif, grid on both axes, degree symbol not "deg", captions ≤ 60 words,
colour-blind-safe palette, both light and dark backgrounds not required (print).

## 10. Missing data

Never imputed. Each variable's table states the number not reported. For pooling, missing
denominators exclude the dataset from that pool (§6.1). For the quality rubric, a missing
field yields the lower score by rule, which is the rubric's intent (undocumented = lower
quality), and this is stated.

## 11. Checks that fail the build

- Any numeric literal in the Results section of the manuscript source that is not an
  `\input` from `results/tables/` or a macro defined from `numbers.json`.
- Any charting record that fails schema validation.
- Any dataset in `charting/` absent from `results/quality_scores.csv`, or vice versa.
- Any pooled estimate with k < 3.
- Any flow count that does not reconcile (retrieved − duplicates − prescreen fails − screening
  exclusions − description exclusions ≠ included records).
- The three-study hand-computed DL example reproduced to 1e-6.

## 12. Changes

Any change to this plan after the search runs is a protocol deviation (protocol §17) and is
reported in Methods with its reason and whether it was made before or after seeing data.
