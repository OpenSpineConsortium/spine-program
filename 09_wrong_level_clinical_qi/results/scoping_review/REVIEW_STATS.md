# What the charted sources show

**None of this has passed human charting. Every p-value below is provisional and describes what the named patterns extracted from the text, not what the literature says. The two are the same thing only to the degree the validation sample says they are, and that sample (`validation_sample.csv`, 200 rows) is still unread. No number here should be quoted as a finding about wrong-level surgery without reading the sources behind it.**

Produced by `tools/review_stats.py` from `extraction.jsonl` (1933 included sources) and `incidence_reported.csv` (426 rate rows). Every charted field carries an explicit / inferred / absent flag. **The primary analysis is the explicit subset**, where the pattern matched inside a sentence that also named a wrong-level event. The explicit-plus-inferred version is reported beside it as a sensitivity analysis and is never the result.

---

## 1. Is the prevention literature aimed at the failing step?

Per source, whether it names an anatomical or radiological mechanism, against whether it names a radiological countermeasure. Population: sources naming at least one countermeasure, because the outcome is undefined otherwise. The class maps are in `tools/review_patterns.py` and are written into `REVIEW_STATS.json` so the assignment can be disputed.

### Primary (explicit) - n = 45

| | names a radiological countermeasure | does not |
|---|---:|---:|
| names an anatomical or radiological mechanism | 13 | 5 |
| does not | 19 | 8 |

- Test: Fisher exact (two-sided); chi-square also reported
- Odds ratio 1.07 (95% CI 0.30 to 3.84), Fisher p = 1.000
- Naming an imaging mechanism, 72.2% (95% CI 49.1 to 87.5) name an imaging countermeasure; not naming one, 70.4% (95% CI 51.5 to 84.1)
- Risk difference +1.8 points

### Sensitivity (explicit + inferred) - n = 603

| | names a radiological countermeasure | does not |
|---|---:|---:|
| names an anatomical or radiological mechanism | 320 | 9 |
| does not | 267 | 7 |

- Test: Fisher exact (two-sided); chi-square also reported
- Odds ratio 0.95 (95% CI 0.36 to 2.50), Fisher p = 1.000
- Naming an imaging mechanism, 97.3% (95% CI 94.9 to 98.6) name an imaging countermeasure; not naming one, 97.4% (95% CI 94.8 to 98.8)
- Risk difference -0.2 points

Countermeasure classes named, primary stratum: organisational 18, radiological 32. Mechanism classes named: anatomical or radiological 68, organisational 23.

---

## 2. How far has each countermeasure been taken?

Status is the strongest one found in any sentence of that source that mentions that countermeasure, by the patterns in `EVALUATION_STATUS`. Reading it only from the sentence that first named the countermeasure put 90 per cent of mentions in `not stated`, because a paper names a technique in its methods and evaluates it in its results. A sentence reporting an outcome usually also carries a recommending verb, so `proposed only` is tested last, not first. `not stated` means the source mentions the countermeasure without saying how far it has been taken - most often a technique described in use.

### Primary (explicit) - 54 countermeasure mentions

| countermeasure | class | named | outcome | confidence | proposed only | not stated | proportion evaluated against an outcome |
|---|---|---:|---:|---:|---:|---:|---|
| navigation or computer assistance | radiological | 21 | 4 | 4 | 3 | 10 | 19.0% (95% CI 7.7 to 40.0) |
| surgical time-out or protocol | organisational | 18 | 7 | 1 | 6 | 4 | 38.9% (95% CI 20.3 to 61.4) |
| intraoperative radiograph with a marker | radiological | 6 | 0 | 0 | 0 | 6 | 0.0% (95% CI 0.0 to 39.0) |
| implanted or skin marker | radiological | 5 | 0 | 0 | 3 | 2 | 0.0% (95% CI 0.0 to 43.4) |
| count from a fixed landmark | radiological | 3 | 0 | 0 | 2 | 1 | 0.0% (95% CI 0.0 to 56.1) |
| second reader or radiologist | radiological | 1 | 0 | 0 | 1 | 0 | 0.0% (95% CI 0.0 to 79.3) |

- Spearman rho = 0.7775 across 6 countermeasures, p = 0.069. a negative rho is the claim that the most-named are the least-evaluated

Grouped, evaluated against an outcome:

- level-determination countermeasures: 0 of 15, 0.0% (95% CI 0.0 to 20.4)
- navigation or computer assistance: 4 of 21, 19.0% (95% CI 7.7 to 40.0)
- organisational: 7 of 18, 38.9% (95% CI 20.3 to 61.4)
- countermeasures acting on the level-determination step, against navigation and the organisational countermeasure: odds ratio 0.08 (95% CI 0.00 to 1.45), Fisher p = 0.024

### Sensitivity (explicit + inferred) - 703 countermeasure mentions

| countermeasure | class | named | outcome | confidence | proposed only | not stated | proportion evaluated against an outcome |
|---|---|---:|---:|---:|---:|---:|---|
| navigation or computer assistance | radiological | 441 | 88 | 13 | 41 | 299 | 20.0% (95% CI 16.5 to 23.9) |
| count from a fixed landmark | radiological | 110 | 1 | 0 | 14 | 95 | 0.9% (95% CI 0.2 to 5.0) |
| compare with the preoperative study | radiological | 45 | 22 | 1 | 0 | 22 | 48.9% (95% CI 35.0 to 63.0) |
| implanted or skin marker | radiological | 43 | 0 | 1 | 10 | 32 | 0.0% (95% CI 0.0 to 8.2) |
| surgical time-out or protocol | organisational | 35 | 7 | 2 | 7 | 19 | 20.0% (95% CI 10.0 to 35.9) |
| intraoperative radiograph with a marker | radiological | 17 | 0 | 0 | 1 | 16 | 0.0% (95% CI 0.0 to 18.4) |
| second reader or radiologist | radiological | 12 | 1 | 2 | 3 | 6 | 8.3% (95% CI 1.5 to 35.4) |

- Spearman rho = 0.2523 across 7 countermeasures, p = 0.585. a negative rho is the claim that the most-named are the least-evaluated

Grouped, evaluated against an outcome:

- level-determination countermeasures: 24 of 227, 10.6% (95% CI 7.2 to 15.2)
- navigation or computer assistance: 88 of 441, 20.0% (95% CI 16.5 to 23.9)
- organisational: 7 of 35, 20.0% (95% CI 10.0 to 35.9)
- countermeasures acting on the level-determination step, against navigation and the organisational countermeasure: odds ratio 0.48 (95% CI 0.30 to 0.77), Fisher p = 0.002

---

## 3. Reported frequency and ascertainment

The primary set is the **adjacent** rates: the rate sits within 40 characters of the wrong-level term it is attributed to. Widening to every anchored rate admits sentences where the nearest rate belongs to a different complication, and one where "100% preventable" is read as an incidence, so the wider set is the sensitivity analysis. A rate is either stated in a sentence naming a wrong-level event or it is not, so there is no confidence stratum here.

### Primary (adjacent rates)

43 rates, of which 17 are on a per-10,000 scale and 17 are strictly positive and so have a logarithm (0 zero rates are described but cannot be logged).

Median 500.0 per 10,000, interquartile range 50.0 to 1500.0, span 0.09 to 4000 - 4.65 orders of magnitude.

By what the rate is a rate of:

| group | n | median per 10,000 | min | max |
|---|---:|---:|---:|---:|
| procedures | 13 | 190.00 | 0.09 | 1500.0 |
| patients | 4 | 2300.00 | 100.00 | 4000.0 |

- Test: Kruskal-Wallis on log10(rate per 10,000); groups with fewer than three sources are described but not tested
- Groups tested: procedures, patients. H = 2.3597 on 1 df, p = 0.125, epsilon-squared = 0.0906
- Two groups, so also Mann-Whitney U = 12.5, p = 0.139, rank-biserial 0.5192

By ascertainment (design class):

| group | n | median per 10,000 | min | max |
|---|---:|---:|---:|---:|
| institutional series | 10 | 345.00 | 4.00 | 1500.0 |
| registry or claims | 2 | 2000.04 | 0.09 | 4000.0 |
| review | 2 | 800.00 | 100.00 | 1500.0 |
| technical | 1 | 3.22 | 3.22 | 3.2 |
| survey | 1 | 600.00 | 600.00 | 600.0 |
| (design not stated) | 1 | 4000.00 | 4000.00 | 4000.0 |

- Test: Kruskal-Wallis on log10(rate per 10,000); groups with fewer than three sources are described but not tested
- fewer than two groups reach three sources; no test was run

Rate against the size of the denominator: Spearman rho = -0.0969 on 15 pairs, p = 0.731. a negative rho is what ascertainment predicts: the larger the denominator, the lower the rate

### Sensitivity (all anchored rates)

75 rates, of which 34 are on a per-10,000 scale and 34 are strictly positive and so have a logarithm (0 zero rates are described but cannot be logged).

Median 200.0 per 10,000, interquartile range 11.1 to 1500.0, span 0.09 to 10000 - 5.05 orders of magnitude.

By what the rate is a rate of:

| group | n | median per 10,000 | min | max |
|---|---:|---:|---:|---:|
| procedures | 25 | 190.00 | 0.09 | 10000.0 |
| patients | 9 | 740.00 | 31.00 | 8570.0 |

- Test: Kruskal-Wallis on log10(rate per 10,000); groups with fewer than three sources are described but not tested
- Groups tested: procedures, patients. H = 3.3121 on 1 df, p = 0.069, epsilon-squared = 0.0723
- Two groups, so also Mann-Whitney U = 66.0, p = 0.072, rank-biserial 0.4133

By ascertainment (design class):

| group | n | median per 10,000 | min | max |
|---|---:|---:|---:|---:|
| institutional series | 15 | 190.00 | 4.00 | 10000.0 |
| registry or claims | 5 | 740.00 | 0.09 | 10000.0 |
| (design not stated) | 5 | 4000.00 | 3.22 | 8570.0 |
| review | 4 | 2745.00 | 100.00 | 4000.0 |
| survey | 3 | 200.00 | 3.22 | 600.0 |
| technical | 2 | 3.22 | 3.22 | 3.2 |

- Test: Kruskal-Wallis on log10(rate per 10,000); groups with fewer than three sources are described but not tested
- Groups tested: institutional series, registry or claims, (design not stated), review, survey. H = 2.2871 on 4 df, p = 0.683, epsilon-squared = 0.0

Rate against the size of the denominator: Spearman rho = -0.1563 on 29 pairs, p = 0.418. a negative rho is what ascertainment predicts: the larger the denominator, the lower the rate

---

## 4. Transitional and numerical anatomy

Among sources discussing a wrong-level event, the share implicating transitional or numerical anatomy. In the primary stratum the population is exact: a field is flagged explicit only when it was matched in a sentence that also named a wrong-level event.

### Primary (explicit)

- 29 of 140 sources implicate transitional or numerical anatomy: 20.7% (95% CI 14.8 to 28.2)
- Lumbosacral-only sources 3.8% (95% CI 0.7 to 18.9) (n = 26) against thoracic-only 0.0% (95% CI 0.0 to 25.9) (n = 11); odds ratio 1.35 (95% CI 0.05 to 35.79), Fisher p = 1.000
- From 2010 21.0% (95% CI 15.0 to 28.6) (n = 138) against before 2010 0.0% (95% CI 0.0 to 65.8) (n = 2); odds ratio 1.35 (95% CI 0.06 to 28.83), Fisher p = 1.000

### Sensitivity (explicit + inferred)

- 452 of 1423 sources implicate transitional or numerical anatomy: 31.8% (95% CI 29.4 to 34.2)
- Lumbosacral-only sources 39.0% (95% CI 35.1 to 43.1) (n = 556) against thoracic-only 8.7% (95% CI 4.7 to 15.8) (n = 103); odds ratio 6.37 (95% CI 3.20 to 12.69), Fisher p = < 0.001
- From 2010 31.9% (95% CI 29.5 to 34.4) (n = 1388) against before 2010 23.5% (95% CI 12.4 to 40.0) (n = 34); odds ratio 1.46 (95% CI 0.67 to 3.19), Fisher p = 0.354

---

## 5. Is attention to the imaging step growing?

The proportion of that year's included sources naming an imaging countermeasure, not the raw count: the corpus itself grows steeply with year, so a count would measure the corpus and not the literature.

### Primary (explicit) - 1754 sources, 2000 to 2025

- Imaging countermeasure, Cochran-Armitage z = 0.3969, p = 0.691
- Organisational countermeasure, z = -0.7269, p = 0.467
- Spearman year against the yearly proportion, rho = 0.3532, p = 0.127, over 20 years with at least five sources

| year | included | imaging countermeasure | organisational | proportion imaging |
|---:|---:|---:|---:|---|
| 2005 | 5 | 0 | 0 | 0.0% (95% CI 0.0 to 43.4) |
| 2007 | 8 | 0 | 0 | 0.0% (95% CI 0.0 to 32.4) |
| 2008 | 18 | 0 | 0 | 0.0% (95% CI 0.0 to 17.6) |
| 2009 | 16 | 0 | 1 | 0.0% (95% CI 0.0 to 19.4) |
| 2010 | 23 | 0 | 0 | 0.0% (95% CI 0.0 to 14.3) |
| 2011 | 31 | 1 | 2 | 3.2% (95% CI 0.6 to 16.2) |
| 2012 | 42 | 1 | 1 | 2.4% (95% CI 0.4 to 12.3) |
| 2013 | 33 | 1 | 1 | 3.0% (95% CI 0.5 to 15.3) |
| 2014 | 47 | 1 | 0 | 2.1% (95% CI 0.4 to 11.1) |
| 2015 | 66 | 2 | 0 | 3.0% (95% CI 0.8 to 10.4) |
| 2016 | 78 | 2 | 0 | 2.6% (95% CI 0.7 to 8.9) |
| 2017 | 92 | 1 | 1 | 1.1% (95% CI 0.2 to 5.9) |
| 2018 | 87 | 2 | 0 | 2.3% (95% CI 0.6 to 8.0) |
| 2019 | 108 | 1 | 0 | 0.9% (95% CI 0.2 to 5.1) |
| 2020 | 165 | 2 | 2 | 1.2% (95% CI 0.3 to 4.3) |
| 2021 | 170 | 4 | 1 | 2.4% (95% CI 0.9 to 5.9) |
| 2022 | 187 | 3 | 2 | 1.6% (95% CI 0.5 to 4.6) |
| 2023 | 191 | 2 | 2 | 1.0% (95% CI 0.3 to 3.7) |
| 2024 | 144 | 2 | 1 | 1.4% (95% CI 0.4 to 4.9) |
| 2025 | 236 | 7 | 3 | 3.0% (95% CI 1.4 to 6.0) |

Years with fewer than five included sources are counted in the trend test but left out of the table, where a proportion over two or three sources would read as a finding.

### Sensitivity (explicit + inferred) - 1754 sources, 2000 to 2025

- Imaging countermeasure, Cochran-Armitage z = 5.7641, p = < 0.001
- Organisational countermeasure, z = -0.2398, p = 0.811
- Spearman year against the yearly proportion, rho = 0.8346, p = < 0.001, over 20 years with at least five sources

| year | included | imaging countermeasure | organisational | proportion imaging |
|---:|---:|---:|---:|---|
| 2005 | 5 | 0 | 0 | 0.0% (95% CI 0.0 to 43.4) |
| 2007 | 8 | 2 | 0 | 25.0% (95% CI 7.1 to 59.1) |
| 2008 | 18 | 3 | 0 | 16.7% (95% CI 5.8 to 39.2) |
| 2009 | 16 | 2 | 1 | 12.5% (95% CI 3.5 to 36.0) |
| 2010 | 23 | 5 | 0 | 21.7% (95% CI 9.7 to 41.9) |
| 2011 | 31 | 5 | 2 | 16.1% (95% CI 7.1 to 32.6) |
| 2012 | 42 | 10 | 1 | 23.8% (95% CI 13.5 to 38.5) |
| 2013 | 33 | 3 | 2 | 9.1% (95% CI 3.1 to 23.6) |
| 2014 | 47 | 9 | 1 | 19.1% (95% CI 10.4 to 32.5) |
| 2015 | 66 | 14 | 0 | 21.2% (95% CI 13.1 to 32.5) |
| 2016 | 78 | 15 | 1 | 19.2% (95% CI 12.0 to 29.3) |
| 2017 | 92 | 27 | 1 | 29.3% (95% CI 21.0 to 39.3) |
| 2018 | 87 | 22 | 1 | 25.3% (95% CI 17.3 to 35.3) |
| 2019 | 108 | 34 | 0 | 31.5% (95% CI 23.5 to 40.7) |
| 2020 | 165 | 47 | 4 | 28.5% (95% CI 22.1 to 35.8) |
| 2021 | 170 | 59 | 1 | 34.7% (95% CI 28.0 to 42.1) |
| 2022 | 187 | 72 | 3 | 38.5% (95% CI 31.8 to 45.6) |
| 2023 | 191 | 57 | 3 | 29.8% (95% CI 23.8 to 36.7) |
| 2024 | 144 | 60 | 2 | 41.7% (95% CI 33.9 to 49.8) |
| 2025 | 236 | 81 | 6 | 34.3% (95% CI 28.6 to 40.6) |

Years with fewer than five included sources are counted in the trend test but left out of the table, where a proportion over two or three sources would read as a finding.

---

## 6. What the corpus cannot support

Tests that were not run, and what each would need.

1. **Any multivariable model.** With 45 sources in the primary 2x2 for question 1 and the smallest cell at 5, a logistic regression adjusting for design, region and year would be fitting more parameters than there are events. It would need the explicit stratum to be an order of magnitude larger, which means human charting of the full text, not more patterns.
2. **A pooled incidence.** One source states a numerator and a denominator in one sentence. A random-effects proportion meta-analysis needs a numerator and a denominator per study, on one denominator; this corpus has 43 adjacent rates spread over 2 different kinds of denominator. It would need those sources read and their tables charted by hand.
3. **Mechanism-specific countermeasure alignment.** Cross-tabulating each of the eleven mechanisms against each of the seven countermeasures is a 77-cell table over 26 sources with both flagged explicitly. Almost every cell would be zero or one. It would need either a much larger explicit subset or a deliberate collapse of the classes agreed before the counting, not after.
4. **Publication-bias or small-study tests.** Funnel plots and Egger's test need a standard error per estimate. These rates are sentences, mostly without a denominator; 15 of the 43 anchored rates carry a stated denominator at all.
5. **Country and setting comparisons.** Country is charted from whatever sentence named a country, and a review describing another country's registry charts that country. Comparing rates or practices by country would be comparing charting artefacts. It would need the affiliation field, which neither source file stores.
6. **Anything about the sources with no abstract and no full text.** 990 records were never judged. If they differ systematically from the judged ones - and closed-access surgical journals are exactly where registry and litigation series appear - every proportion here is conditioned on open access. Nothing in the corpus can measure that. It would need the abstracts of the 990, which is a request to the publishers, not a query.
7. **Evaluation status as a property of a study.** It is charted per countermeasure, so a source that evaluates one countermeasure and merely proposes another contributes to both columns. Per-source evaluation status would need the methods and results read, and 1076 of the 1933 included sources have no full text at all - for those the whole evidence is an abstract.
8. **A time trend before 2000 or after 2025.** Years outside the window carry too few sources to estimate a proportion, and 2026 is a partial year in a corpus fetched in September 2026.


One more, stated because it is the largest: **the explicit stratum is small.** The primary analyses rest on 81 sources naming a mechanism explicitly and 45 naming a countermeasure explicitly, out of 1933 included. The explicit flag requires the pattern and a wrong-level term in one sentence, and window-mined passages break sentences.

**The two strata do not agree everywhere, and where they disagree the primary one governs.** Comparing the two on each test:

| test | primary p | sensitivity p | |
|---|---|---|---|
| 1, alignment of mechanism and countermeasure | 1.000 | 1.000 | agree |
| 2, level-step countermeasures against the rest | 0.024 | 0.002 | agree |
| 4, transitional by region | 1.000 | < 0.001 | **disagree** |
| 4, transitional by era | 1.000 | 0.354 | agree |
| 5, trend in imaging countermeasures | 0.691 | < 0.001 | **disagree** |

Where they disagree, the sensitivity stratum is the one counting matches that were never tied to a wrong-level event in the same sentence. It is the larger number and the weaker evidence, and it is reported so the disagreement is visible rather than so it can be quoted.
