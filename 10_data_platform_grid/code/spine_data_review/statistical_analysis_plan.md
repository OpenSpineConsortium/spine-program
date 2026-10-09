# Statistical analysis plan

Protocol 1.0, frozen 2026-09-19, after the count-only pilot and before the full search. Every
analysis names its input files, its
estimator, its eligibility rule and the key under which its result is written. All analyses
are run by `sdr/analyse.py` (flow, descriptives, availability, quality, grid, reliability,
diagnostics) and `sdr/meta.py` (pooling) from the verified charting records,
`screen/decisions.csv`, `<run-dir>/queries.json` and the probe results, into
`analysis/<name>.json`, where every value is `{value, derived_from, rule}`. Tables
(`tables/*.tex`), the macro file (`tables/numbers.tex`) and figures (`figures/*.pdf`) are
rendered from those JSONs only; the manuscript reads only from them. Analyses not listed here
are exploratory and are labelled so in the manuscript.

## General rules

- **Software**: Python 3.12; numpy, scipy, pandas, statsmodels, matplotlib; versions pinned
  in `requirements.txt` and written to `analysis/build_info.json` with the git commit.
- **Determinism**: every random draw follows protocol section 7.8 (`sdr/sampling.py`:
  population sorted by id, a fresh `random.Random(20260919)` per draw; bootstrap with
  `numpy.random.default_rng(20260919)`); sorted inputs; a test asserts identical output on
  rerun.
- **Unit**: the dataset, unless stated. Records are the unit only in the flow diagram and the
  screening agreement.
- **Denominators** are stated in every table cell footnote or column header. `unknown` (or
  null) is a category in every count, never dropped, and is excluded from every sum, median
  and test with the number excluded stated beside the statistic. No imputation.
- **Derived datasets and parent families** (`flags.derived = true`, `parent_ids`): counted in
  the descriptive tables (they are datasets) but, in every subject or image total and in every
  pooled estimate, **at most one dataset per parent family enters** — the family being the
  parent and everything derived from it, transitively, whether or not the parent is itself
  included — and it is the family member with the largest n_i for that analysis; the excluded
  members are listed beside the result. Two derived datasets of one absent parent (RibSeg v1
  and v2 from RibFrac; several VerSe re-annotations) therefore never both enter. Figure-derived
  collections and datasets with `n_subjects_basis = estimated` are excluded from every sum and
  every pooled estimate (no defined denominator population) and are reported in their own row.
- **Subject overlap**: for a pair of included datasets with a `subject_overlap` entry that is
  not a parent/derived relation, the larger dataset enters totals and pooling and the smaller
  is excluded from them; where `n_shared` is known, totals subtract it instead. Totals are
  labelled "reported subjects summed across datasets (persons may recur)", because a person
  can sit in two datasets that no field links.
- **Versions**: one dataset per lineage (protocol 7.6); the largest version's counts are used.
- **Multi-modal datasets** are counted once overall and once per eligible modality in
  modality-stratified tables, which say so.
- **Statistics**: this is a scoping review; the analyses are descriptive, the tests are
  exploratory and reported with that word, two-sided α = 0.05, 95 % intervals throughout, no
  multiplicity adjustment except Holm within a Dunn post-hoc family. Proportions carry
  Wilson score intervals without continuity correction; per-dataset proportions in A5 and in
  forest plots carry Clopper–Pearson exact intervals. The pooled summaries (A5, A6) are
  secondary and illustrative; the per-dataset tables are primary (protocol section 3).
- **Numerical conventions** (each changes a reported number if changed): medians and
  quartiles by `numpy.percentile(..., method='linear')`; lowess by
  `statsmodels.nonparametric.smoothers_lowess.lowess(frac=2/3, it=3)`; `unknown` and null
  values are dropped from every test and correlation with the n used stated in the table
  footnote; percentages are computed at full precision and rounded half-to-even to one decimal
  by the macro generator after any `\numword` threshold is applied to the unrounded value.
- **Implementations that the allowed libraries lack** are written in `sdr/stats.py`,
  each with a unit test against a published example run by `build.sh`:
  Kruskal–Wallis ε² = (H − k + 1) / (n − k); Dunn's pairwise z_ij = (R̄_i − R̄_j) /
  sqrt((N(N+1)/12 − Σ(t³ − t)/(12(N − 1))) · (1/n_i + 1/n_j)) with the tie term over tied
  groups t, two-sided p from the normal, Holm over all pairs; the Cochran–Armitage trend test
  as `statsmodels.stats.contingency_tables.Table(counts).test_ordinal_association(row_scores=[1,2,3,4])`
  over the four year bands, which is the linear-by-linear association test and is stated as
  equivalent to Cochran–Armitage for a 2 × k table; Spearman ρ with a 95 % interval on
  Fisher's z using the Bonett–Wright standard error sqrt((1 + ρ²/2) / (n − 3)); ICC(2,1)
  and κ as in `quality_rubric.md` (`sdr/reliability.py`); I² interval by the Q-profile
  method (Higgins–Thompson), τ² by REML, HKSJ interval, the logit random-intercept model and
  the DL check as in A5 (`sdr/meta.py`).
- **Year bands** wherever a band is used: 2000–2010, 2011–2016, 2017–2020, 2021–2026.
- **Presentation**: numbers under ten are spelled out in prose by the macro generator
  (`\numword…`); percentages to one decimal with numerator and denominator in the table;
  intervals as "(95 % CI a to b)"; figures sans-serif with a grid on both axes, colour-blind
  safe, the degree symbol not "deg", captions at most 60 words with no argument in them; the
  source JSON's SHA-1 in each PDF's metadata.

## A1. Flow counts (PRISMA-ScR item 14) — `analysis/flow.json`

Inputs: `queries.json`, `records/*.jsonl`, `merged.jsonl`, `screen/*.csv`,
`charting/dataset_sources.csv`, `charting/aliases.csv`.

Per source (Table 2) and in total (Figure 1): records returned by the API (`hit_count_api`),
records retrieved (`n_retrieved`, with the cap named when hit), credential mode, coverage;
for sources harvested in full, `n_identified` is the post-filter count and the harvest total
is a separate column; Open-i is counted by distinct articles (PMCID) and Commons by candidate
categories — figure-pool sizes belong to A3.4, not to the flow. Then: after within-source
de-duplication; after cross-source merge (removed per merge rule 1–6); prescreen pass / fail
per block / uncertain / non-english-route; audit sample (per stratum: screened, included,
excluded); screened; excluded at screening per `primary_code` and `use-only`; sought for full
text; not retrieved (charted from abstract); excluded at description review per
`primary_code`; included records; datasets after mapping; derived and figure-derived counts;
`n_use_records` per dataset (median, IQR); source records per dataset (median, IQR). Second
arm: known items (retrieved / not retrieved / excluded-I4), chasing candidates (backward,
forward, manual), search-update records, screened, excluded, included through that arm.

The identity `sdr/analyse.py --check-flow` asserts, and the build fails if it does not hold:

```
search arm:
  identified − duplicates = after_merge
  after_merge = fail_not_audited + fail_audited + pass + uncertain + non_english_route
  fail_audited = audit_included + audit_excluded
  screened = pass + uncertain + non_english_route + audit_included
  screened = screen_excluded (Σ over primary_code) + use_only + unclear_to_full_text + include_to_full_text
  sought_for_full_text = unclear_to_full_text + include_to_full_text
  sought_for_full_text = not_retrieved + retrieved            (not_retrieved are still screened, from the abstract)
  sought_for_full_text = full_text_excluded (Σ over primary_code) + included_records_search
other-methods arm:
  known_items = ki_retrieved_by_search + ki_not_retrieved + ki_excluded_I4
  candidates_other = ki_not_retrieved + chase_backward + chase_forward + chase_manual + update_records
  candidates_other = other_excluded + included_records_other
datasets:
  datasets = |map(included_records_search ∪ included_records_other)|
  datasets = non_derived_non_figure + derived + figure_derived
```

Also (`analysis/search_validation.json`): known-item recall = retrieved / items with
`role = recall` (Wilson interval, overall and per source; I1-test and excluded-I4 items in
their own rows); prescreen false-negative rate per audit stratum (block × source class) =
included / sampled with a Wilson interval, and the implied number missed = rate × stratum
size, reported per stratum and never pooled; for each source, the number of retrieved records
it alone found.

## A2. Descriptive characteristics (items 15, 17) — `analysis/descriptives.json`

Input: `charting/datasets/*.json`.

Table of included datasets (one row each): id, name, year, country, modality, region,
projection, n_subjects, n_images_or_volumes (unit), annotation types, annotation origin,
variant labels (three symbols), licence tier, access route, quality total, fit_level_id;
sorted by modality, year, name. Full charting rendered in Supplement S1.

Counts of datasets and, where known, sums and medians (IQR) of `n_subjects` and
`n_images_or_volumes` by unit — sums under the general rules above (one dataset per parent
family, overlaps handled, `estimated` and figure-derived rows separate, label "reported
subjects summed across datasets (persons may recur)"); multi-modal datasets contribute
`n_per_modality` to the per-modality rows, never their overall count — stratified by:
modality; region; projection (radiography only);
annotation type (a dataset counts once per type it carries, so totals exceed the number of
datasets and the table says so); annotation origin (same rule); access route; licence tier;
year (single years for Figure 2, stacked by modality, plus cumulative subjects by modality);
year band; country (top ten and "other"); pediatric inclusion; format; figure_derived and
derived flags.

Cross-tabulations reported without tests: annotation origin × modality; **the review's
central table**, variant labelling × level-name origin — rows: at least one variant with
`how_labelled = explicit-label`, and a second row block for `derivable-from-labels` (never
`status = yes` alone, which includes variants merely mentioned in the text); columns: the
origin list of `annotation_origin_by_type['per-vertebra-level-names']`, falling back to the
segmentation entry when absent as the rubric does, with `counting-inferred` as its own column
so the question "does anyone who counts also label variants?" is answered from the level-name
origin, not the union field; `per_vertebra_level_names` × modality using the same origin
field; region × projection for radiographs with the whole-spine and thoracic rows
highlighted because they are the scarce ones; access route × licence tier (Figure 3, mosaic);
`described_as_public` (charted) × `described_as_public_regex` (flag).

## A3. Availability (RQ5; item 18) — `analysis/availability.json`

Input: `described_as_public`, `described_as_public_regex`, `access_route`,
`access_route_rule`, `access_probe[]`, `host_type`, `file_url_probed`.

- A3.1 Distribution of `access_route` overall, by modality, by year band, and by `host_type`
  (repository-api, institutional, personal-or-cloud-drive, challenge-platform, unknown; the
  field is derived by code from the protocol section-10 host table).
- A3.2 **Share of "described as public" that actually downloads** — one definition, identical
  in `PROTOCOL.md` section 10. Denominator = datasets with the reviewer-charted
  `described_as_public = yes`. Primary row: the proportion with final `access_route =
  open-download` (the route already encodes the file evidence of P1, P13–P15, P20 or a
  repository API's open state, so open datasets on institutional servers are not failed by
  construction). Second row: among datasets with a known `file_url_probed`, the proportion
  whose file URL answered 200/206 on both probes, with that denominator. Third row: route in
  {open-download, registration} (the recipe-eligible set). Wilson intervals on each. Also: the
  proportion whose final route differs from the agreed machine classification (verifier
  overrides), with reasons tabulated; the distribution of `access_route_rule`; the
  cross-tabulation of the charted value against the regex flag.
- A3.3 Probe agreement: the number of datasets whose `classification_machine` or HTTP status
  class (2xx / 4xx / 5xx / no response) changed between the two probe dates, listed by id,
  and the number that needed a third probe.
- A3.4 Figure-derived pool (outside the flow): for Open-i, Commons, MultiCaRe, Open-PMC-18M
  and the four non-English journal APIs, the number of figures (or articles) returned per
  query and per modality with the query date, from `queries.json`; counts only, no pooling.
- A3.5 Route by year band (does older data go dark?): proportion `unavailable` per band with
  Wilson intervals and the trend test named under the general rules, exploratory.
Output: Table of availability outcomes; Figure 3.

## A4. Quality score (SO1; item 16) — `analysis/quality.json`

Input: rubric scores computed by `sdr/quality.py`.

- A4.1 Distribution of the total: median, IQR, range, histogram (Figure 4a), overall and by
  annotated / unannotated stratum; per-item share at 0/1/2.
- A4.2 Total vs modality (CT-only vs projection-only vs multi-modal): Kruskal–Wallis, ε²
  (formula under the general rules), on the annotated stratum as primary and on all datasets
  as secondary.
- A4.3 **Total vs access route**: Kruskal–Wallis H across routes with at least five datasets,
  effect size ε²; if p < 0.05, Dunn's pairwise tests with Holm adjustment (`sdr/stats.py`);
  per-route medians and n. Primary on the annotated stratum (unannotated datasets are capped
  at 16 by rule and would confound the comparison); secondary on all datasets. Reported three
  times: the full total (0–20); with Q7 removed (0–18), because Q7 is a probe outcome that
  co-varies with the route; and with Q6, Q7 and Q8 removed (0–14), because a licence visible
  on a repository and a dataset DOI are structural properties of repository hosting, so the
  relation of quality to route is partly circular even without Q7. ε² and Dunn are computed
  on the annotated stratum only.
- A4.4 **Total vs year**: Spearman ρ with a 95 % interval from Fisher's z with the
  Bonett–Wright standard error and n stated, primary on the annotated stratum and secondary on
  all datasets; scatter with a lowess line (Figure 4b). Also Spearman ρ between the total and
  log10(n_subjects) among datasets with n_subjects reported.
- A4.5 Rubric reliability on the blind re-charted sample of max(25, 20 %) datasets, re-charted
  before verification (protocol section 8): per-item exact agreement and linearly weighted κ
  ("not estimable" with raw and PABAK agreement where an item has zero variance); ICC(2,1) on
  the total with the Shrout–Fleiss F-based 95 % interval; sample size stated.
- A4.6 Fitness: number and list of datasets with `fit_level_id`, `usable_for_training`,
  `fit_variant`, `fit_stitching` true, by modality, with the subjects they carry; the
  distribution of the failing rule (F1–F4) among the rest.
Output: per-dataset item table (`tables/quality.tex`), Figure 4.

## A5. Prevalence of L6, T13 and LSTV per dataset, and an illustrative pooled summary (SO2; item 18) — `analysis/pooled_variants.json`

**Primary output** is the per-dataset table: for every dataset with
`variant_labels.<v>.n_subjects_with` (x_i) and `n_subjects_assessed` (n_i) both non-null and
`unit = subject`, the proportion x_i / n_i with a Clopper–Pearson exact interval, together with
`selection`, `ascertainment`, `definition_class`, modality and n_i. Prevalence differs by
sampling, by ascertainment and by definition, and several candidate datasets were deliberately
enriched for variants (VerSe'20 oversampled transitional vertebrae; CTSpinoPelvic1K is
LSTV-stratified), so a pooled number over them would measure curators' sampling choices. The
pooled summary below is therefore secondary and labelled illustrative (protocol section 3);
heterogeneity is expected to be high, and the **prediction interval, not the pooled point, is
the headline** of that summary.

Eligible for pooling, per variant: the per-dataset conditions above, `n_i ≥ 20`,
`selection = consecutive-or-unselected`, `ascertainment ≠ unknown`, `definition_class ≠
not-defined`, `verified_by` non-null, not figure-derived, one dataset per parent family and
per overlapping pair (the larger n_i; the general rules). Datasets with `selection = enriched`
are summarised as their own stratum with the same estimator and are never in the pooled
estimate; `excluded` and `unknown` selections are tabulated only.

- A5.1 Pooling requires **k ≥ 5** eligible datasets per variant (and per stratum). Fewer → the
  per-dataset table only, and "pooling not done (k < 5)" is stated. No prediction interval is
  reported below k = 5.
- A5.2 Estimator (primary): a logit random-intercept model, logit(p_i) = μ + u_i,
  u_i ~ N(0, τ²), x_i ~ Binomial(n_i, p_i), fitted by maximum likelihood with the
  one-dimensional integral over u_i evaluated by adaptive Gauss–Hermite quadrature (21 nodes,
  centred and scaled at each dataset's conditional mode), implemented directly in `sdr/meta.py`
  with `scipy.optimize` and `numpy.polynomial.hermite`; Wald interval on μ, back-transformed;
  τ² reported; 95 % prediction interval on the logit scale μ ± t_{k−2} · sqrt(τ² + SE(μ)²).
  `tests/test_meta.py` reproduces a published GLMM example (the Schwarzer et al. 2019
  proportion example) to 1e-4 before any review data is pooled. Zero or full cells need no
  correction under this model.
- A5.3 Sensitivity (Supplement S3): (a) DerSimonian–Laird on the logit scale, the estimator
  originally requested: p_i = x_i / n_i, y_i = logit(p_i), v_i = 1/x_i + 1/(n_i − x_i), 0.5
  added to x_i and 1 to n_i for zero or full cells only (stated), w_i = 1/v_i,
  Q = Σ w_i (y_i − ȳ_FE)², C = Σ w_i − Σ w_i² / Σ w_i, τ² = max(0, (Q − (k − 1)) / C),
  w_i* = 1/(v_i + τ²), ȳ_RE = Σ w_i* y_i / Σ w_i*, SE = (Σ w_i*)^(−1/2); the formulae are
  implemented directly and checked against
  `statsmodels.stats.meta_analysis.combine_effects(method_re="dl")`, and the three-study
  hand-computed example in `tests/test_meta.py` must reproduce to 1e-6; (b) REML τ² with the
  Hartung–Knapp–Sidik–Jonkman interval on the logit scale; (c) leave-one-dataset-out under the
  primary model; (d) datasets with n_i ≥ 100 only. Freeman–Tukey double-arcsine is **not**
  used: its back-transform misleads when n_i spans two orders of magnitude (Schwarzer et al.
  2019), which is the expected range here. I² = max(0, (Q − (k − 1)) / Q) with a Q-profile
  interval is reported as a description of the DL analysis, not as a decision criterion.
- A5.4 Pre-specified subgroups, each reported only when every subgroup has ≥ 5 datasets and
  formed from charted enums, never from free text: modality (CT vs radiography);
  `ascertainment` (count-from-c2 / count-from-sacrum vs local-morphology vs report-or-text);
  `definition_class` (for LSTV: castellvi-I-IV vs castellvi-II-IV vs
  sacralisation-lumbarisation-unspecified vs other). Between-subgroup comparison by a
  likelihood-ratio test of the subgroup term in the primary model.
- A5.5 Figure 5: one forest plot per variant, rows sorted by year, squares scaled by n_i,
  per-dataset Clopper–Pearson intervals, the enriched stratum drawn separately, diamond for
  the illustrative pooled estimate when k ≥ 5, dashed prediction interval, τ² in the footer.
- A5.6 Interpretation rule, written now: the pooled number is "prevalence among unselected
  labelled datasets" and is compared in the Discussion with the population literature, never
  treated as a population estimate; when the prediction interval spans the population range,
  that is the reported finding.

## A6. Inter-rater agreement per dataset, and an illustrative pooled summary (SO2) — `analysis/pooled_agreement.json`

Input: `annotation_validation.*`.

- A6.0 `comparable_group` is computed by `sdr/validate.py`, not assigned by a person, from
  this lookup over (`inter_rater_statistic`, the annotation type read by rubric Q2,
  `comparator`); anything not listed → null:

  | statistic | annotation type | comparator | comparable_group |
  |---|---|---|---|
  | kappa, weighted-kappa | per-vertebra-level-names | rater-vs-rater | kappa-level-names |
  | kappa, weighted-kappa | pathology-labels, fracture-grade, image-level-labels | rater-vs-rater | kappa-pathology |
  | dice | segmentation-3d | rater-vs-rater | dice-vertebra-3d |
  | dice | segmentation-2d | rater-vs-rater | dice-2d |
  | icc | measurements | rater-vs-rater | icc-measurement |
  | distance-mm | landmarks, centroids | rater-vs-rater | mm-landmark |

  `model-vs-rater`, `rater-vs-consensus` and `unknown` comparators are never a group: a
  model's Dice against the ground truth is not agreement.
- A6.1 Primary output: the per-dataset table of every reported statistic with its value,
  interval, n, comparator, n_categories and group. Pooling is secondary and illustrative, and
  is attempted only for the two κ groups, only when **k ≥ 5** datasets in a group report a
  95 % interval **and** share the same `n_categories` (a 27-class level-naming κ and a binary
  read are not comparable); otherwise the group is tabulated and "pooling not done" is stated
  with the reason (k, missing intervals, or unequal category counts).
- A6.2 Estimator for a poolable κ group: SE_i = (upper_i − lower_i) / 3.92 from the reported
  interval, never approximated from n; random effects on the κ scale by REML τ² with the HKSJ
  interval, DL as a check. Dice, ICC and mm error are **not pooled**: each group is summarised
  as the median (IQR) across datasets with the per-dataset n, because Dice is bounded and
  skewed and both depend on region, resolution and structure set.
- A6.3 τ² and a prediction interval as in A5.2 for a pooled κ group; forest plot per pooled
  group in Supplement S4; per-dataset table `tables/pooled_agreement.tex`.

## A7. Coverage of the authors' grid (SO4) — `analysis/grid_coverage.json`

Input: `on_grid.*`, `access_route`, fitness booleans.

Per modality and region: included datasets on the grid (yes / partial / no / unknown);
subjects on the grid over subjects in the reachable set (route in {open-download,
registration}); share on the grid among `fit_level_id` datasets. The list of reachable
`fit_level_id` datasets not on the grid, sorted by quality total descending, is the recipe's
first-run order (Table 10).

## A8. Screening reliability — `analysis/screening_reliability.json`

On the stratified dual-screened sample of `pass ∪ uncertain` records (protocol 7.3) and,
separately, on the fully dual-screened description-review stage: Cohen's κ on the binary
decision include vs {exclude, unclear} (primary) with a 95 % bootstrap interval (2,000
resamples, `numpy.random.default_rng(20260919)`); three-class κ (secondary); raw agreement;
PABAK and Gwet's AC1 beside κ because inclusion prevalence is low; disagreements by criterion
code. The LLM step is used (protocol 7.4): raw agreement and binary κ between its suggestion
and the human decision, the number of suggestions reversed, and the number of records it
covered, reported separately and never combined with the human κ.

## A9. Search-coverage diagnostics (exploratory; Limitations) — `analysis/source_overlap.json`

For each included dataset, the set of sources that returned at least one of its source
records; the number of datasets found by exactly one source and which; for the known-item
set, whether the search found each item (a recall check with a known answer, stated as such).
Rendered as an UpSet-style matrix table in the appendix.

## A10. Tables and figures (item 13c)

| Object | Content | Generated from |
|---|---|---|
| Figure 1 | PRISMA 2020 two-arm flow | `analysis/flow.json` |
| Figure 2 | Datasets per year stacked by modality; cumulative subjects | `analysis/descriptives.json` |
| Figure 3 | Access route × licence tier (mosaic); route by year band | `analysis/availability.json` |
| Figure 4 | Quality total: histogram by route (a); scatter vs year (b) | `analysis/quality.json` |
| Figure 5 | Per-dataset prevalence with exact intervals, L6, T13, LSTV; illustrative pooled diamond when k ≥ 5 | `analysis/pooled_variants.json` |
| Table 1 | Eligibility criteria | `PROTOCOL.md` section 4 |
| Table 2 | Information sources, dates, hit counts | `queries.json` |
| Table 3 | Data items | `charting_schema.json` |
| Table 4 | Characteristics of included datasets | `charting/` |
| Table 5 | Quality scores per dataset, per item | `analysis/quality.json` |
| Tables 6–7 | Counts and totals by strata | A2 |
| Table 8 | Availability outcomes | A3 |
| Table 9 | Inter-rater agreement per dataset and pooled | A6 |
| Table 10 | Grid coverage and recipe order | A7 |
| Appendix A | Verbatim search strings, endpoints, dates, counts | `queries.json` |
| Appendix B | Deviations log | `PROTOCOL.md` section 19 |
| Supplement S1 | Full charting records rendered | `charting/` |
| Supplement S2 | Near-miss exclusions with reasons | `screen/decisions.csv` |
| Supplement S3 | Prevalence sensitivity analyses | A5.3 |
| Supplement S4 | Agreement forest plots | A6.3 |

## Search update before submission

The update run (protocol 6.3) is not a flow row only: its records are de-duplicated against
the frozen run and the new ones are screened, charted and probed twice by the same procedure.
If any dataset is included, every analysis in this plan is regenerated from the union, the
manuscript's last-search date becomes the update date, and the deviations log records the
delta (records, datasets, and every macro whose value changed). If none is included, the
update is reported as a flow row with zero datasets and the last-search date is unchanged.

## Checks that fail the build

- Any bare digit in the Abstract or Results source outside a macro, citation, label or the
  allow-list (protocol section 13).
- Any charting record that fails schema validation or has `verified_by = null`.
- Any dataset in `charting/datasets/` absent from `analysis/quality.json`, or vice versa.
- Any pooled estimate with k < 5, or any pooled prevalence including a figure-derived,
  enriched, parent-duplicated or overlap-duplicated dataset.
- Any flow identity of A1 that does not hold (`sdr/analyse.py --check-flow`).
- The three-study DL example not reproduced to 1e-6, the GLMM example not reproduced to 1e-4,
  or any unit test in `tests/` (ids, terms, sampling, reliability, stats, meta) failing.
- Any record in the re-charting sample whose re-chart date does not precede its
  verification date.
- Any dataset with a probe of method other than none and fewer than two probes at least
  48 h apart.
- A `\num…` macro used but undefined, or defined but unused.

## Changes

Any change to this plan after the search runs is a protocol deviation (`PROTOCOL.md`
section 19) and is reported in Methods with its reason and whether it was made before or
after seeing data.
