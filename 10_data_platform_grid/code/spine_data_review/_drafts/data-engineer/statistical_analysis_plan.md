# Statistical analysis plan (predefined; protocol 1.0, 2026-09-19)

All analyses are run by `sdr/analyse.py` (descriptives, tests) and `sdr/meta.py` (pooling)
from the charting JSONs, `screen/decisions.csv`, `<run-dir>/queries.json` and the probe
results, into `analysis/*.json` where every value is `{value, derived_from, rule}`. Tables
(`tables/*.tex`) and figures (`figures/*.pdf`) are rendered from those JSONs only. No number
in the manuscript is typed. Software: Python 3.12, numpy, scipy, pandas, statsmodels,
matplotlib; versions pinned in `requirements.txt` and printed into `analysis/build_info.json`.

This is a scoping review: the analyses are descriptive, the tests are exploratory and
reported with that word, and no multiplicity adjustment is made. Where a pooled estimate is
computed, the plan says which datasets enter it and why.

## A1. Flow counts (PRISMA-ScR item 14)

Per source, from `queries.json` and the records files:
- records returned by the API (`hit_count_api`), records retrieved (`n_retrieved`; differs when
  a paging cap was hit, and the cap is named), records after within-source de-duplication;
- across sources: unique source records after merge (section 7 rules, count per rule);
- prescreen: excluded per rule id; uncertain; include;
- reviewer screening: excluded per reason code; full-text requested; included;
- charting: datasets created; source records per dataset (median, IQR); derived and
  figure-derived counts.
Sources run as `needs-credentials` appear with zero hits and the reason. Output:
`analysis/flow.json`, Figure 1 (flow diagram drawn from the JSON), `tables/flow_by_source.tex`.

## A2. Descriptive characteristics (items 15, 17)

Counts of datasets and, where known, sums and medians (IQR) of `n_subjects` and
`n_images_or_volumes`, stratified by: modality (a multimodal dataset is counted once per
eligible modality and once overall, and the table says so), region, projection, annotation
type, annotation origin, access route, licence tier, year (2000–2026 in five-year bins and by
single year for Figure 2), country, pediatric inclusion, format. `unknown` is a category in
every table, never dropped. Sums exclude `unknown` and state the number of datasets
contributing. Output: `analysis/descriptives.json`, Tables 1–2, Figure 2 (datasets per year by
modality, stacked; and cumulative subjects by modality).

Cross-tabulations reported without tests: annotation origin × modality; variant labelling ×
annotation origin (the review's central table: does anyone who counts also label variants?);
region × projection for radiographs, with the whole-spine and thoracic rows highlighted because
they are the scarce ones.

## A3. Availability (item 18)

- Distribution of `access_route` over all datasets and by modality.
- Share of "described as public" that actually downloads: numerator and denominator as in
  PROTOCOL section 10, Wilson 95% CI.
- Agreement of the two probe days: number of datasets whose classification changed between
  probes, with the pairs listed.
- Access route by year of first description (does older data go dark?): proportion
  `unavailable` per five-year bin with Wilson CIs; Cochran-Armitage trend test, exploratory.
Output: `analysis/availability.json`, Table 4, Figure 3.

## A4. Quality score (item 16)

- Per-item and total score distributions (median, IQR, min, max; histogram in Figure 4).
- Total score vs access route: Kruskal-Wallis across the routes with at least five datasets;
  pairwise Dunn tests reported only as exploratory, unadjusted, with the route sample sizes.
- Total score vs year: Spearman rho with 95% CI by Fisher z, n stated.
- Total score vs modality (CT vs projection-only vs multimodal): Kruskal-Wallis.
- Fit-for-level-identification and usable-for-training: counts, and the failing rule
  distribution (which of F1–F5 fails most often).
- Inter-rater reliability of the rubric on the 20% re-charted sample: ICC(2,1) with 95% CI;
  per-item exact agreement.
Output: `analysis/quality.json`, Table 3, Figure 4.

## A5. Pooled prevalence of L6, T13 and LSTV (item 18)

Eligible for pooling: datasets with an integer `n_positive` and `n_assessed` for the variant
with `unit` = subject, `verified_by` non-empty, and `n_assessed` ≥ 20. A dataset flagged
`derived` is excluded from the pool when its parent is in the pool (the subjects are the
same). Figure-derived collections are excluded (no defined denominator population).

Method: random-effects meta-analysis of proportions on the logit scale, DerSimonian-Laird
between-study variance, per-study variance 1/(np(1−p)) with a 0.5 continuity correction when
`n_positive` is 0 or equals `n_assessed`; back-transformed pooled estimate with 95% CI;
Cochran's Q, I² with 95% CI (Higgins), tau². Per-study CIs are Clopper-Pearson exact.
Sensitivity: Freeman-Tukey double-arcsine transform with the same DL weights; and a
generalised linear mixed model (logistic random intercept, statsmodels) when ≥ 5 datasets.
Reported for each variant only when ≥ 3 datasets qualify; otherwise the per-dataset values are
tabulated and pooling is stated as not done. Subgroup: CT vs radiograph (the same anatomy is
read differently on the two), reported as two pooled rows, no test between them unless both
have ≥ 3 datasets.

Implementation note: `sdr/meta.py` implements DL from the formulae and is unit-tested against
a published worked example (the `metafor` `dat.bcg` logit-proportion example values are the
fixture) before any review data is pooled; the test is part of `build.sh`.

Output: `analysis/pooled_variants.json`, `tables/pooled_variants.tex`, Figure 5 (forest plot
per variant; study rows sorted by year; squares scaled by DL weight; diamond for the pooled
estimate; caption under 60 words).

## A6. Pooled inter-rater agreement

Run only when ≥ 3 datasets report the same statistic on a comparable task
(`annotation_validation.type` and `statistic_name` identical, e.g. Cohen's kappa for
per-vertebra level names, Dice for vertebral segmentation). Kappa: DL random effects on the
Fisher-z scale when a CI or standard error is reported, else per-study variance from the
Fleiss approximation with `n_items`; datasets that report neither n nor CI are listed but not
pooled. Dice: DL on the raw scale with the reported SD/n; datasets reporting only a mean are
listed but not pooled. Output: `analysis/pooled_agreement.json`, `tables/pooled_agreement.tex`.

## A7. Coverage of the authors' grid

Share of datasets `on_grid.present` in {yes, partial}, overall and by access route, by
modality, and among `fit_for_level_id` datasets. The list of `fit_for_level_id` datasets that
are `open-download` or `registration` and NOT on the grid is the recipe's priority list and is
Table 5. Output: `analysis/grid_coverage.json`.

## A8. Screening reliability

Cohen's kappa (with 95% CI) between reviewers on the 10% double-screened sample; number of
LLM-suggested prescreen labels reversed by the reviewer, if the LLM step is used. Output:
`analysis/screening_reliability.json`.

## A9. Search-coverage diagnostics (exploratory, reported in Limitations)

For each included dataset, the set of sources that returned at least one of its source
records; the number of datasets found by exactly one source, and which source; and, for the
eight datasets already in use by the project, whether the search found them (a recall check
with a known answer, stated as such). Output: `analysis/source_overlap.json`, an UpSet-style
matrix table in the appendix.

## Handling of missing data and unknowns

`unknown` is reported as a category in every count and excluded from every sum, median and
test, with the number excluded stated beside the statistic. No imputation.

## Presentation rules

Numbers under ten are spelled out in prose (the macro generator emits words for 0–9 in a
`\numword...` variant); percentages to one decimal with the numerator and denominator in the
table; CIs as "(95% CI a to b)"; figures sans-serif, grid on both axes, captions at most 60
words, no argument in captions. Figures are generated with a fixed seed where any randomness
exists (none is planned) and with the source JSON's sha1 in the PDF metadata.
