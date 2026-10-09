# Review data: wrong-level and wrong-site spine surgery

_Wrong-level and wrong-site spine surgery: mechanisms, the imaging step that fails, and decision support - a scoping review_

Everything here was produced from the held corpus by `tools/review_screen.py`, `tools/review_extract.py`, `tools/review_prisma.py` and `tools/review_summary.py`. No number below was entered by hand; each one is a count of rows in a named file. Nothing was searched on the open web for this review.

## Files

| file | what is in it | rows |
|---|---|---:|
| `screening.jsonl` | one row per unique record: identifiers, decision, stage, reason code, reason text, and the patterns and matched strings that drove it. Line 1 is the machine-readable criteria block (`record_type: criteria`). | 11981 |
| `criteria.json` | the inclusion criteria as implemented, on their own. | - |
| `dedup_report.json` | every removed duplicate, with the record it duplicated and the key that matched. | 314 |
| `extraction.jsonl` | one row per included record with the charted items, each carrying the exact sentence it came from and a confidence flag. | 1933 |
| `incidence.csv` | the included records carrying both a denominator and a numerator, with the quotes and a flag for whether the two came from one sentence. | 4 |
| `incidence_reported.csv` | the included records stating a rate verbatim, with the quote. A paper far more often states a rate than a fraction. | 426 |
| `PRISMA_FLOW.md` / `.json` / `prisma_flow.svg` | the flow counts and the diagram. | - |
| `incidence_reported.csv` (columns) | each rate carries what it is a rate of, its value per 10,000 where the unit permits it, an explicit reason where it does not, the range where one is written, the design, and how far the rate sits from the wrong-level term. | - |
| `abstracts.jsonl` | one row per record: the fetched abstract, or an empty string with status `none` where the source genuinely has none. | 12294 |
| `screening_titleonly.jsonl` + `titleonly/` | the first screening pass and its outputs, kept whole rather than overwritten. | - |
| `SCREEN_CHANGES.md` / `.json` / `screen_changes.csv` | every record whose decision or reason changed between the two passes, with the abstract evidence that moved it. | 5767 |
| `corpus_snapshot/` | the five corpus files both passes read, with sha256 and line counts, because the source roots are being appended to by a running chain. | - |
| `validation_sample.csv`, `validation_sample_titleonly.csv` | 200 records per pass, fixed seed, stratified 100 included and 100 excluded, with two empty columns for a human reader. | 200 |
| `extraction_stats.json` | how many charted fields came out explicit, inferred or absent. | - |

## Inclusion criteria as implemented

**Population.** Human patients undergoing spine surgery or a spinal intervention, or imaging studies of vertebral enumeration. Implemented as `P_SPINE_PROCEDURE`, `P_ENUMERATION_IMAGING`, `P_SPINE_ANY`.

**Concept.** A wrong-level or wrong-site event, its mechanism, its frequency, the imaging step used to determine level, or a method intended to prevent it, including transitional-anatomy detection and vertebral numbering. Implemented as `C_WRONG_LEVEL_EVENT`, `C_MECHANISM`, `C_FREQUENCY`, `C_IMAGING_LEVEL_STEP`, `C_PREVENTION`, `C_TRANSITIONAL`, `C_NUMBERING`.

**Context.** Any clinical setting, any country, any year, English or any language with an English abstract. No context restriction is applied by the screen.

**Exclusions.**

| reason code | meaning |
|---|---|
| `E_NOT_SPINE` | The record does not concern the spine at all (no spine, vertebral or spinal-region term). |
| `E_NON_SPINE_WRONG_SITE` | Wrong-site surgery outside the spine (wrong-site language with no spine term). |
| `E_ANIMAL_CADAVER` | Animal or cadaver-only work with no clinical claim. |
| `E_EDITORIAL_NO_DATA` | Editorial, comment, letter, erratum or news item with no data. |
| `E_NO_FULLTEXT` | No retrievable abstract or full text in the held corpus. |
| `E_NO_CONCEPT` | Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim. |
| `E_TECHNICAL_NO_LEVEL_CLAIM` | Purely technical imaging paper with no level-determination claim. |
| `E_NO_POPULATION` | No human patient, clinical or imaging-of-enumeration population. |
| `E_PROCEEDINGS_COLLECTION` | A conference proceedings container (a block of abstracts), not a chartable record. |

The screen runs in three stages, so that a record that was never judged is not counted as a record that was judged and rejected: a title-and-type screen over every record, then whether text was retrieved for it, then an assessment against the criteria over the retrieved text.

## Counts

Two screening passes are reported, because the screen was revised after the abstracts were fetched. **Pass 1** had a title and a publication type; **pass 2** added the abstract wherever one could be fetched. Neither replaces the other: pass 1 is `screening_titleonly.jsonl` with its own outputs under `titleonly/`, pass 2 is `screening.jsonl`. `SCREEN_CHANGES.md` reports the movement between them.

| step | pass 2 (title + abstract) | pass 1 (title only) |
|---|---:|---:|
| records identified | 12294 | 12294 |
| duplicates removed | 314 | 314 |
| records screened | 11980 | 11980 |
| excluded at the automated screen | 3243 | 4711 |
| reports sought for retrieval | 8737 | 7269 |
| no abstract and no full text retrieved | 990 | 4947 |
| records assessed | 7747 | 2322 |
| excluded at assessment | 5814 | 1657 |
| **records included** | **1933** | 665 |

`PRISMA_FLOW.md` gives the reason tables. Included records by source: semanticscholar 1115, europepmc 818. Every included record has an abstract or full text by construction (full text no 1076, yes 857; abstract yes 1911, no 22).

## Top journals among the included records

| journal | included records |
|---|---:|
| Cureus | 113 |
| (no journal) | 99 |
| Journal of Orthopaedic Surgery and Research | 46 |
| Global spine journal | 43 |
| Asian spine journal | 38 |
| BMC Musculoskeletal Disorders | 38 |
| Asian Spine Journal | 37 |
| Frontiers in Surgery | 37 |
| BMC musculoskeletal disorders | 35 |
| Neurospine | 34 |
| Surgical neurology international | 33 |
| Journal of Korean Neurosurgical Society | 33 |
| The International Journal of Spine Surgery | 29 |
| Medicine | 28 |
| European spine journal | 23 |
| Journal of Pain Research | 23 |
| Spine | 22 |
| American Journal of Neuroradiology | 21 |
| Spine Surgery and Related Research | 21 |
| Scientific reports | 20 |

## Years

| year | included records |
|---|---:|
| 2026 | 174 |
| 2025 | 236 |
| 2024 | 144 |
| 2023 | 191 |
| 2022 | 187 |
| 2021 | 170 |
| 2020 | 165 |
| 2019 | 108 |
| 2018 | 87 |
| 2017 | 92 |
| 2016 | 78 |
| 2015 | 66 |
| 2014 | 47 |
| 2013 | 33 |
| 2012 | 42 |
| 2011 | 31 |
| 2010 | 23 |
| 2009 | 16 |
| 2008 | 18 |
| 2007 | 8 |
| 2005 | 5 |
| 2004 | 2 |
| 2003 | 1 |
| 2002 | 2 |
| 2001 | 1 |

Year span of the included records: 1999 to 2026.

## Design mix

One design per record, taken from the first design pattern that matched a sentence carrying a study-describing term; `(not stated)` means no design pattern matched anything held for that record.

| design | records (pass 2) | share | records (pass 1) |
|---|---:|---:|---:|
| (not stated) | 584 | 30.2% | 234 |
| cohort | 536 | 27.7% | 139 |
| review | 257 | 13.3% | 98 |
| case report | 197 | 10.2% | 87 |
| technical | 100 | 5.2% | 18 |
| survey | 99 | 5.1% | 38 |
| registry | 97 | 5.0% | 32 |
| case series | 63 | 3.3% | 19 |

Confidence of the design field: explicit 1123, absent 584, inferred 226.

## What was chartable

A field is `explicit` when the pattern matched inside a sentence that also carries the anchor for that item, `inferred` when it matched elsewhere in the record, and `absent` when nothing matched. An empty field is left empty.

| field : confidence | records |
|---|---:|
| countermeasures:absent | 1330 |
| countermeasures:present | 603 |
| country:absent | 1559 |
| country:present | 374 |
| denominator:absent | 915 |
| denominator:explicit | 1015 |
| denominator:inferred | 3 |
| design:absent | 584 |
| design:explicit | 1123 |
| design:inferred | 226 |
| imaging_modality_for_level:absent | 288 |
| imaging_modality_for_level:present | 1645 |
| incidence_verbatim:absent | 1507 |
| incidence_verbatim:explicit | 75 |
| incidence_verbatim:inferred | 351 |
| mechanisms:absent | 832 |
| mechanisms:present | 1101 |
| numerator:absent | 1929 |
| numerator:explicit | 1 |
| numerator:inferred | 3 |
| pairing:denominator_only | 1014 |
| pairing:different_sentences | 3 |
| pairing:none | 915 |
| pairing:same_sentence | 1 |
| setting:absent | 1688 |
| setting:explicit | 221 |
| setting:inferred | 24 |
| spinal_region:absent | 226 |
| spinal_region:present | 1707 |
| transitional_implicated:absent | 1481 |
| transitional_implicated:explicit | 29 |
| transitional_implicated:inferred | 423 |
| years_covered:absent | 1760 |
| years_covered:explicit | 173 |

### A proportion synthesis is not available from this corpus

This is a result, not a shortfall in the charting. Records carrying both a denominator and a numerator: **4 (was 3)**. Of those, pairs stated in one sentence, and so usable as a proportion: **1**. One record is not a synthesis.

What the corpus does carry is rates stated in words. Records stating a rate verbatim: **426 (was 244)** (`incidence_reported.csv`), of which **75 (was 70)** state it in a sentence that also names a wrong-level or wrong-site event.

**These are not pooled and must not be.** Their denominators are not the same denominator:

| what the rate is a rate of | records |
|---|---:|
| procedures | 25 |
| surgeons surveyed | 16 |
| (the sentence does not say) | 15 |
| patients | 9 |
| wrong-level cases | 5 |
| reported events | 3 |
| malpractice claims | 2 |

Only the rows whose denominator is procedures or patients are put on a per-10,000 scale, and each keeps its unit: **34** of the 75 anchored rows. A rate is converted by `rate_to_per_10000` in `tools/review_patterns.py` (a percentage times 100, `1 in N` as 10,000/N, `N per M` as N times 10,000/M), and the conversion used is written into the `normalisation` column.

Each row also carries `chars_from_event_term` and `event_association`: how far the rate sits from the wrong-level term it is attributed to. A complications sentence lists several rates - "dural tears (1.9%), wrong-level operations (0.3%)" - and distance is the only thing in the text that says which one belongs to this review. `adjacent` is 40 characters or fewer, `same sentence` is 41 to 100, `distant` is more; the thresholds are arbitrary and are stated so they can be moved.

Among the 17 rows that are both normalisable and `adjacent`, the stated rates span **0.09 to 4000 per 10,000** - roughly four orders of magnitude. The spread is the finding: the low end is registry and claims-based ascertainment (`1 in 112,000`, `1 in 3110`) and the high end is small prospective discectomy series that inspected every level (`the wrong level was approached in 15% of cases`). They are not estimates of one quantity.

| rate per 10,000 | unit | as reported | design | association |
|---:|---|---|---|---|
| 0.0893 | per 10,000 procedures | 1 in 112,000 | registry | adjacent |
| 3.2154 | per 10,000 procedures | 1 per 3110 | technical | adjacent |
| 4.0 | per 10,000 procedures | 0.04% | cohort | adjacent |
| 50.0 | per 10,000 procedures | 0.5% | cohort | adjacent |
| 50.0 | per 10,000 procedures | 0.5% | case report | adjacent |
| 100.0 | per 10,000 patients | 1% | review | adjacent |
| 190.0 | per 10,000 procedures | 1.9% | cohort | adjacent |
| 190.0 | per 10,000 procedures | 1.90% | cohort | adjacent |
| 500.0 | per 10,000 procedures | 5% | cohort | adjacent |
| 600.0 | per 10,000 procedures | 6% | survey | adjacent |
| 600.0 | per 10,000 patients | 6% | cohort | adjacent |
| 1300.0 | per 10,000 procedures | 13% | cohort | adjacent |
| 1500.0 | per 10,000 procedures | 15% | review | adjacent |
| 1500.0 | per 10,000 procedures | 15% | cohort | adjacent |
| 1500.0 | per 10,000 procedures | 15% | cohort | adjacent |
| 4000.0 | per 10,000 patients | 40% | registry | adjacent |
| 4000.0 | per 10,000 patients | 40% | - | adjacent |

Rates written as a range are kept as a range rather than reduced to a midpoint:

| as written | low per 10,000 | high per 10,000 |
|---|---:|---:|
| between 0.09 and 4.5 per 10,000 | 0.09 | 4.5 |
| from 0.09 to 4.5 per 10,000 | 0.09 | 4.5 |
| from 14.3–7.4% | 1430.0 | 740.0 |
| from 0.14 to 5.3 percent | - | - |
| between 25% and 45% | 2500.0 | 4500.0 |
| from 4% to 37% | - | - |
| between 4% and 35% | - | - |
| between 4% and 8% | - | - |
| between 4-8% | - | - |
| from 5 to 36% | - | - |
| from 1.7 to 14% | - | - |
| between 4 and 36% | - | - |
| from 69.5 to 98.0 % | - | - |
| from 80% to 25% | - | - |
| from 9.9% to 25% | - | - |
| Between 7-17% | - | - |

### Region, mechanism, countermeasure, modality

| spinal region | records |
|---|---:|
| lumbar or lumbosacral | 1367 |
| thoracic | 667 |
| sacral or pelvic | 639 |
| cervical | 520 |

| mechanism named | records |
|---|---:|
| deformity or scoliosis | 468 |
| transitional or numerical variant | 465 |
| osteopenia or degenerative change | 255 |
| prior surgery or instrumentation | 190 |
| anatomy obscured by habitus | 168 |
| process or communication failure | 161 |
| marker or localisation failure | 58 |
| miscounted from a landmark | 53 |
| image misread or misinterpreted | 41 |
| poor intraoperative visualisation | 22 |
| level lost between images | 11 |

| countermeasure named | records |
|---|---:|
| navigation or computer assistance | 441 |
| count from a fixed landmark | 110 |
| compare with the preoperative study | 45 |
| implanted or skin marker | 43 |
| surgical time-out or protocol | 35 |
| intraoperative radiograph with a marker | 17 |
| second reader or radiologist | 12 |

| imaging modality for level | records |
|---|---:|
| intraoperative fluoroscopy | 1167 |
| computed tomography | 746 |
| magnetic resonance | 471 |
| navigation or robotics | 402 |
| plain radiograph | 141 |
| ultrasound | 107 |
| intraoperative radiograph | 75 |
| scout or scanogram | 5 |

Transitional anatomy implicated: absent 1481, inferred 423, explicit 29 (`explicit` means the transitional term sat in a sentence that also named a wrong-level event).

Country, counted only where the country name sat in a sentence that also places a study:

| country | records |
|---|---:|
| United States | 40 |
| Japan | 28 |
| China | 27 |
| Korea | 8 |
| Norway | 8 |
| Australia | 7 |
| India | 7 |
| United Kingdom | 6 |
| Netherlands | 6 |
| Bangladesh | 5 |
| France | 5 |
| Finland | 3 |
| Egypt | 3 |
| Germany | 3 |
| Nigeria | 3 |

## Overlap with the two corpora that are not part of this search

The fluoroscopy and pathology arms were built for a different question and are **not** part of this review's search. They are reported here only so the overlap is on the record. Nothing is merged.

| corpus | records (unique PMCID) | shared with this review's screened set | shared with the included set |
|---|---:|---:|---:|
| fluoroscopy arm (`FluoroCap_wsl/articles.jsonl`) | 56173 | 2539 | 1025 |
| pathology arm (`FluoroCap_path/articles.jsonl`) | 158955 | 6136 | 1425 |

## Limitations of the corpus itself

1. **The primary search is a Europe PMC full-text query restricted to records with full text.** It cannot see closed-access work at all. The wrong-level literature includes closed-access surgical journals and closed registry reports, so the sampling frame is skewed toward open-access journals; the journal table above shows that skew directly.
2. **The abstracts were fetched, and that changed the review.** Neither source file stores an abstract, so the first pass screened on a title and a publication type alone. `tools/review_abstracts.py` fetched 9487 abstracts from Europe PMC (resultType=core) and the Semantic Scholar batch endpoint; 2807 records genuinely have none at either source and 0 identifiers failed to resolve. Adding them moved the included count from 665 to 1933 and changed 48% of screened records. What remains is that 990 records still carry no abstract and no full text, and those cannot be judged at all.
3. **The text held is not full text; it is windows around a matched term.** `passages.jsonl` keeps an excerpt around each hit, so a denominator and a numerator usually land in different windows or in no window at all. That, not the literature, is why a one-sentence denominator-and-numerator pair comes out of only 1 of the 1933 included records, while 426 of them state a rate verbatim.
4. **Full-text failures are known in aggregate but not per record.** The Europe PMC parse log (`FluoroCap_lstv/log_passages.txt`) records 3862 parsed and 2145 failed over 6007 records, and writes every attempted PMCID to `passages_done.txt` whether it succeeded or failed. A record with no passages therefore cannot be separated into 'parsed, no term matched' and 'never parsed'. The flow reports that bucket under one reason and says so.
5. **Semantic Scholar adds records with no full text.** Of its 6287 records, 2556 yielded a parsed PDF and only 325 yielded a passage; the rest are title-only rows. It widens identification and barely widens what can be charted.
6. **Semantic Scholar's queries are not all this review's question.** Its `origin` field spans `lstv`, `wrong_level` and `tltv` but also `fluoro_general`, `hardware`, `injections` and `pathology`. Those off-topic rows are carried into identification and removed by the screen, which inflates both the identified count and the excluded count. The alternative, filtering by query name before screening, would hide records the screen would have kept.
7. **The screen is machine-assisted and its accuracy is not known.** Precision and recall cannot be stated until the `human_decision` column of `validation_sample.csv` is filled in. Until then, every count downstream of the screen is a count of what the patterns did, not of what is true.
8. **Patterns miss what they do not name.** Two misses were found by reading the excluded rows: a spine record whose title says only `os odontoideum` (fixed by adding the term), and a record whose level-determination claim is phrased as `conus localization` (not fixed, because widening that pattern to `localization` alone would admit most of the corpus). There will be others.
9. **Reference lists and tables are text too.** A reference list is other papers' titles and a flattened table is a grid with the grid removed; both were charted at first and both produced confident, wrong numbers, including a calendar year read as a count of wrong-site events and `2,826,367 operations` read as `826,367`. Sections labelled `REF` are now dropped before charting, counts are refused from `TABLE` and `FIG`, and any sentence carrying eight or more bare numbers is treated as a table. PDF text carries no section label, so this guard is weaker on the Semantic Scholar rows.
10. **A duplicate that shares neither a PMCID nor a DOI nor a near-identical title is not detected.** Preprint-and-journal pairs and conference-abstract-and-paper pairs will survive deduplication as two records.
11. **Design, country and setting are charted from whatever sentence matched.** A review that describes another study's cohort will chart that cohort. The exact sentence is carried in every field so this is visible per record, but it is not corrected.
12. **The `(not stated)` design bucket is large** (584 records, was 234 in pass 1). That is a property of window-mined text, not evidence that those papers have no design.
13. **The corpus roots are live.** `FluoroCap_lstv/captions_matched.jsonl` grew from 1,297 to 1,327 lines between two runs of the screen an hour apart, and three records changed exclusion bucket because of it. Both passes therefore read a pinned copy in `corpus_snapshot/`, with sha256 sums, and the counts here are counts against that snapshot rather than against whatever the roots hold now.
14. **The abstract must not be allowed to answer questions the title answers better.** On the first abstract pass a feline case report was included, because a veterinary abstract says "patient" and that overruled the animal term in the title. The rules about what kind of work a record is (animal, proceedings container) now read the title only; the rules about what the work is on read the title and the abstract. Three records moved the other way, from included to excluded, when their abstracts showed the wrong-site language was not about the spine.
15. **A rate is attributed by proximity, not by reading.** `event_association` measures the gap in characters between the rate and the wrong-level term. It caught real errors - a sentence listing complications had `dural tears (4.6%)` charted as a wrong-level rate - but proximity is not comprehension, and 6 of the anchored rates sit more than 100 characters from the term they are attributed to. Those are marked `distant` and should be read before being quoted.
16. **Normalising to per 10,000 makes rates comparable in units, not in meaning.** A registry rate over every spinal procedure in a country and a 15% figure from a hundred discectomies inspected level by level differ by ascertainment, not only by units. They are listed, never pooled, and the `rate_denominator_nature` column says what each one counts.

## What is not known

The screen's precision and recall. The true number of eligible closed-access records. Which of the 258 Europe PMC records that produced no text were parsed and matched nothing, and which were never parsed: the log gives 3862 parsed and 2145 failed but names neither set. Whether the 1101 records charted with a mechanism name that mechanism as a cause of a wrong-level event in their own data or merely mention it in a background sentence - the anchor test asks only that a wrong-level term sit in the same sentence, which is a proximity test, not a reading.
