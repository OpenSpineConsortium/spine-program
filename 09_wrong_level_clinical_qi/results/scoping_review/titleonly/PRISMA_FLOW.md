# PRISMA-ScR flow

_Wrong-level and wrong-site spine surgery: mechanisms, the imaging step that fails, and decision support - a scoping review_

Counts produced by `tools/review_prisma.py` from `review/screening.jsonl`. Every count below is a count of rows in that file carrying the named stage and reason code; no count is entered by hand.

## Identification

| source | records identified |
|---|---:|
| europepmc | 6007 |
| semanticscholar | 6287 |
| **total** | **12294** |

### Duplicates removed

| matched on | removed |
|---|---:|
| doi | 14 |
| normalised_title | 153 |
| pmcid | 147 |
| **total** | **314** |

Split by whether the duplicate came from the other source or the same one:

| matched on / scope | removed |
|---|---:|
| doi/within_source | 14 |
| normalised_title/cross_source | 33 |
| normalised_title/within_source | 120 |
| pmcid/cross_source | 147 |

## Screening

Records screened: **11980**

### Excluded at the automated screen (title and publication type)

| reason | n | what the reason means |
|---|---:|---|
| `E_NOT_SPINE` | 3926 | The record does not concern the spine at all (no spine, vertebral or spinal-region term). |
| `E_ANIMAL_CADAVER` | 635 | Animal or cadaver-only work with no clinical claim. |
| `E_EDITORIAL_NO_DATA` | 86 | Editorial, comment, letter, erratum or news item with no data. |
| `E_PROCEEDINGS_COLLECTION` | 49 | A conference proceedings container (a block of abstracts), not a chartable record. |
| `E_NON_SPINE_WRONG_SITE` | 15 | Wrong-site surgery outside the spine (wrong-site language with no spine term). |
| **total** | **4711** | |

## Full text

Full texts sought from the held corpus: **7269**

### Full texts not retrieved

| reason | n |
|---|---:|
| no open full text | 1378 |
| no full text parsed or no review term matched in it; the parse log records 3862 parsed and 2145 failed over 6007 records but does not attribute failure to a record | 1323 |
| PDF retrieved but no passage matched a review term | 1271 |
| fetch failure: HTTP 403 | 331 |
| fetch failure: the link did not return a PDF (not_pdf(200)) | 293 |
| fetch failure: the link did not return a PDF (not_pdf(202)) | 122 |
| fetch failure: URLError | 59 |
| fetch failure: HTTP 404 | 44 |
| fetch failure: HTTP 302 | 33 |
| fetch failure: HTTP 500 | 29 |
| fetch failure: HTTP 429 | 22 |
| fetch failure: HTTP 401 | 11 |
| fetch failure: HTTP 502 | 9 |
| fetch failure: InvalidURL | 5 |
| fetch failure: 522 | 4 |
| fetch failure: RemoteDisconnected | 4 |
| fetch failure: TimeoutError | 4 |
| fetch failure: 410 | 2 |
| fetch failure: 406 | 1 |
| fetch failure: 503 | 1 |
| fetch failure: 408 | 1 |
| **total** | **4947** |

## Assessment

Records assessed against the criteria: **2322**

### Excluded at assessment

| reason | n | what the reason means |
|---|---:|---|
| `E_NO_POPULATION` | 1437 | No human patient, clinical or imaging-of-enumeration population. |
| `E_NO_CONCEPT` | 127 | Spine record with no wrong-level, level-determination, enumeration or transitional-anatomy claim. |
| `E_ANIMAL_CADAVER` | 86 | Animal or cadaver-only work with no clinical claim. |
| `E_TECHNICAL_NO_LEVEL_CLAIM` | 7 | Purely technical imaging paper with no level-determination claim. |
| **total** | **1657** | |

## Included

Records included: **665**

Of those, records carrying both a denominator and a numerator, and so usable for a proportion synthesis: **3** (`review/incidence.csv`).

![PRISMA flow](prisma_flow.svg)

## A note on where the boxes sit

Records with no retrieved text are counted in the full-text box rather than at the automated screen, so that the flow separates 'not judged' from 'judged and excluded'.

The screen is machine-assisted. Its precision and recall are not known and cannot be stated until the `human_decision` column of `review/validation_sample.csv` is filled in.
