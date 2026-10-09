# Information sources, endpoints, limits and verbatim search strings

Protocol 1.0, frozen 2026-09-19, after the count-only pilot search (section 6.0) and before
the full search is executed. Part of `PROTOCOL.md` (sections 5 and 6). Every source below is
queried by `sdr/search.py --source <name>`; the strings in this file are what the adapter
sends, URL-encoding aside, and **this file is the single source of truth**: the adapter parses
the fenced `query_id:` blocks and grid lines from it at run time, and the two materialised
files `queries/literature.yaml` and `queries/repositories.yaml` (the appendix's source) are
checked against it by `tests/test_queries_yaml.py`, which fails the build if any entry marked
`verbatim_in_markdown` differs from its fenced block or grid line by one byte (`sdr/terms.py`
and `tests/test_terms.py`, named in v1.0, were never written; deviations log 2026-09-19). Hit counts and dates are never
written here: the run records them in `runs/<run-date>/queries.json`, from which Appendix A of
the manuscript is generated; the pilot's counts live in `runs/pilot-2026-09-19/queries.json`.

## Conventions the code relies on

- **query_id.** Every query is `<source>_<nn>` (`pubmed_01`, `zenodo_02`). Grid sources that
  send one request per string from the shared grid table (section G) use `<source>_g<nn>`
  (`dryad_g07`). Enumeration sources with no query (a full listing filtered locally) have one
  id ending in `_list`. The id is the key in `queries.json` and the appendix row.
- **Verbatim blocks.** A fenced block headed by a line `query_id: <id>` holds one string, sent
  as-is after URL-encoding. Line breaks inside a block are joined with one space before
  sending. Grid lines are `<id>  <string>` (two spaces).
- **Placeholders.** `<NCBI_API_KEY>`, `<S2_API_KEY>`, `<CONTACT>` (= `FLUOROCAP_CONTACT_EMAIL`),
  `<HF_TOKEN>`, `<GITHUB_TOKEN>`, `<SPRINGER_API_META_KEY>`, `<UNPAYWALL_EMAIL>` are read by
  name from `~/.fluorocap/credentials.env` (or the optional files named below) and never
  written to any output. A route whose credential is absent runs its credential-free form and
  writes `credential_mode: credential-free` (or `needs-credentials` when no such form exists).
- **Shared request conventions.** User-Agent `spine-data-review/1.0 (scoping review;
  mailto:<CONTACT>)`; 20 s connect and read timeout; retry on 429, 500, 502, 503, 504 with
  back-off 1, 2, 4, 8, 16 s, then give up and log; `Retry-After` honoured; every attempt logged
  to `requests.log.jsonl`; every body cached under `raw/<source>/<sha1>.json`. Rate ceilings
  per source are enforced with a token bucket and are at or under each provider's stated
  policy: NCBI 10/s with key else 3/s; Semantic Scholar 1/s; OpenAlex and Crossref polite pool
  with `mailto` at 2/s; arXiv one request per 3 s (arXiv policy); Zenodo 1/s (guest policy);
  GitHub 10/min unauthenticated, 30/min with token; Wikimedia Commons 1/s with `maxlag=5`;
  every other source 2/s.
- **Dates.** Year limits 2000–2026 are in the string where the source supports a date field,
  else applied locally to the record's year and recorded as `date_filter: local`.
- **Facts marked (verify)** are documented or observed behaviours confirmed on the first run;
  if a source behaves differently the fallback named in its block is used and a row is added to
  the deviations log (`PROTOCOL.md` section 19).

## Section 6.0. Pilot search (JBI step 1)

Run by hand on 2026-09-19, before the freeze, as count-only requests (`retmax=0`,
`pageSize=1`): the Europe PMC string in unfielded form, the same string fielded to
`TITLE:`/`ABSTRACT:`/`KW:`, and `pubmed_01`. The three are recorded in
`runs/pilot-2026-09-19/queries.json` with `role: pilot`, their dates and their hit counts, and
Appendix A reports them in a "pilot" row. No record was retrieved and no title or abstract
was read, so no term harvesting took place in the pilot: the term blocks were assembled from
the titles of the known-item set (`PROTOCOL.md` section 18) and the group's earlier ad-hoc
searches, and Methods says so. The one decision the pilot produced: Europe PMC is queried
fielded, because the unfielded form also matches the full text of open-access articles and
returned many times more hits (the numbers are in the pilot record, not here). The protocol
freeze and the OSF registration follow the pilot and precede the full search.

## Term blocks (PROTOCOL.md section 6.1)

```
BLOCK_S  spine, spinal, vertebra*, lumbar, thoracolumbar, lumbosacral, sacrum,
         "cervical spine", "thoracic spine", scoliosis, spondylolisthesis
BLOCK_M  "computed tomography", "computed tomographic", CT, CBCT, "cone-beam", "cone beam",
         radiograph*, "X-ray", "X-rays", "x ray", xray*, roentgen*, fluoroscop*, "C-arm",
         "image intensifier", DXA, DEXA, absorptiometry, "vertebral fracture assessment",
         EOS, biplanar, "plain film", "plain films"
BLOCK_D  dataset, datasets, "data set", "data sets", database, benchmark*, challenge,
         "publicly available", "public data", "open data", "open access", "open-access",
         "open source", "data descriptor", corpus, "image collection"
```

Where a source has no wildcard, `vertebra*` is written out as `vertebra OR vertebrae OR
vertebral`, `radiograph*` as `radiograph OR radiographs OR radiography OR radiographic`,
`xray*` as `xray OR xrays`, `roentgen*` as `roentgen OR roentgenographic`, `fluoroscop*` as
`fluoroscopy OR fluoroscopic`, `benchmark*` as `benchmark OR benchmarks`. *Cervical*,
*thoracic* and *sacral* alone are not in BLOCK_S (cervix, thoracic surgery, sacral nerve
stimulation); *rib* is absent (rib datasets without a spine claim are out of scope);
*annotated* and *segmentation* are absent from BLOCK_D (they retrieve the whole method
literature, whose released datasets are reached through the repository sources and backward
chasing). MRI is not in BLOCK_M; MRI-only records fail E1 at screening.

## Section G. Shared grid strings for sources without boolean syntax

Reduced sets, chosen so the grid stays at 7 × 5 = 35 strings per source:
`SPINE_R = spine, vertebra, vertebral, lumbar spine, cervical spine, thoracic spine, scoliosis`;
`MODALITY_R = CT, radiograph, x-ray, fluoroscopy, DXA`. The grid id is `g<row><col>` in the
order below. A source block says which ids it sends and what it appends.

```
g01  spine CT
g02  spine radiograph
g03  spine x-ray
g04  spine fluoroscopy
g05  spine DXA
g06  vertebra CT
g07  vertebra radiograph
g08  vertebra x-ray
g09  vertebra fluoroscopy
g10  vertebra DXA
g11  vertebral CT
g12  vertebral radiograph
g13  vertebral x-ray
g14  vertebral fluoroscopy
g15  vertebral DXA
g16  lumbar spine CT
g17  lumbar spine radiograph
g18  lumbar spine x-ray
g19  lumbar spine fluoroscopy
g20  lumbar spine DXA
g21  cervical spine CT
g22  cervical spine radiograph
g23  cervical spine x-ray
g24  cervical spine fluoroscopy
g25  cervical spine DXA
g26  thoracic spine CT
g27  thoracic spine radiograph
g28  thoracic spine x-ray
g29  thoracic spine fluoroscopy
g30  thoracic spine DXA
g31  scoliosis CT
g32  scoliosis radiograph
g33  scoliosis x-ray
g34  scoliosis fluoroscopy
g35  scoliosis DXA
```

Single-term list for repositories whose search is title-only (BLOCK_M applied locally to the
fetched description): `t01 spine`, `t02 spinal`, `t03 vertebra`, `t04 vertebrae`,
`t05 vertebral`, `t06 lumbar`, `t07 scoliosis`, `t08 spondylolisthesis`.

## Summary table

Thirty search sources (L1–L7, R1–R14, F1–F8, S1) and one charting tool (S2, Unpaywall, which
has no `query_id` and is not a search source). `Coverage` is the index's start date from its
own documentation, or "unknown" (PRISMA-ScR item 7); the same value is written to
`queries.json[query_id].coverage`. `Raw cache` says whether the raw response bodies under
`raw/<source>/` are published with the review; where a provider's terms restrict
redistribution, or the body is third-party text (captions, abstracts of paywalled articles,
HTML pages), the cache is withheld and the record ids plus the sha1 of every cached body are
published instead, so a replay can be verified without redistributing the text.

| # | Source | Endpoint | Auth | Ceiling | Grammar | Paging / cap | Coverage | Raw cache |
|---|---|---|---|---|---|---|---|---|
| L1 | PubMed | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`, `efetch.fcgi` | `NCBI_API_KEY` optional | 10/s keyed, 3/s not | boolean, `[tiab] [mh] [ta] [dp]`, `*` | esearch count; `usehistory=y` + efetch `retstart` batches of 500, history addresses 9,999 records (`retstart` ≤ 9,998); > 9,999 hits split by `[dp]` year ranges, a range still > 9,999 capped at 9,999 | MEDLINE 1946–; limited to 2000–2026 by `[dp]` | yes (NLM terms) |
| L2 | Europe PMC | `www.ebi.ac.uk/europepmc/webservices/rest/search` | none | 2/s | fielded Lucene `TITLE: ABSTRACT: KW: PUB_YEAR: SRC: HAS_DATA:` | `cursorMark`, `pageSize` ≤ 1000, no cap | MEDLINE 1946–; PMC 2000–; preprints 2018-07– | yes (core fields) |
| L3 | OpenAlex | `api.openalex.org/works` | `mailto=<CONTACT>` | 2/s | `filter=title_and_abstract.search:(…)` boolean, quoted phrases, no wildcard | `cursor=*`, `per-page` ≤ 200, no cap | all years (MAG lineage); dataset records from DataCite | yes (CC0) |
| L4 | Semantic Scholar | `api.semanticscholar.org/graph/v1/paper/search/bulk` | `S2_API_KEY` header `x-api-key`; absent → 1 per 5 s shared pool | 1/s | bulk: `+` AND, `\|` OR, `-` NOT, `"phrase"`, `*`, `( )` | continuation `token`, 1000 per page, ≤ 10 M | all years (S2 open corpus) | no (API terms): ids + sha1 |
| L5 | arXiv | `export.arxiv.org/api/query` | none | 1 per 3 s | `abs: ti:` AND/OR/ANDNOT, `%22…%22`, no wildcard | `start`, `max_results` 500; addressable ≤ 30,000 (verify) | 1991-08– | yes (Atom metadata) |
| L6 | bioRxiv / medRxiv | `api.biorxiv.org/details/{server}/{from}/{to}/{cursor}/json` | none | 2/s | none: monthly dumps, local regex | cursor step 100 | bioRxiv 2013-11–; medRxiv 2019-06– | yes |
| L7 | Crossref | `api.crossref.org/works` | `mailto=<CONTACT>` | 2/s | `query.bibliographic` free text, relevance; `filter=type:…` | `cursor=*`, `rows` ≤ 1000; 5,000 cap per string recorded | all registered DOIs; abstracts where deposited | partial: metadata yes, publisher abstracts withheld (ids + sha1) |
| R1 | Zenodo | `zenodo.org/api/records` | none | 1/s | InvenioRDM fielded (`metadata.*`), `*` | `page`×`size` ≤ 10,000 → split by year | 2013-05– | yes |
| R2 | Figshare | `POST api.figshare.com/v2/articles/search` | none | 2/s | `:title: :description:` AND/OR/NOT, `\"phrase\"` | `page_size` ≤ 1000, `page`; `offset`/`limit` fallback | 2011– | yes |
| R3 | Dryad | `datadryad.org/api/v2/search` | none | 2/s | free text → grid | `per_page` ≤ 100 | 2008– | yes (CC0 metadata) |
| R4 | OSF | `api.osf.io/v2/nodes/`, `/registrations/`, `/preprints/` | `OSF_TOKEN` optional | 1/s | `filter[title][icontains]` → single terms | `page[size]` ≤ 100 | 2013– | yes |
| R5 | Mendeley Data | `data.mendeley.com/public-api/datasets/search` (observed, verify) → DataCite `prefix=10.17632` | none; OAuth API not held | 2/s | free text → single terms | unknown; fallback always run | 2015– | partial: DataCite route yes; front-end bodies as sha1 |
| R6 | DataCite | `api.datacite.org/dois` | none | 2/s | Lucene fielded `titles.title: descriptions.description: subjects.subject: publicationYear:` | `page[cursor]`, `page[size]` ≤ 1000, no cap | 2009– (registration date) | yes |
| R7 | PhysioNet | `physionet.org/rest/database-list/` (verify) → HTML `physionet.org/content/` | none | 1/s | none: full list, local regex | single response | 1999– | yes |
| R8 | TCIA / NBIA | `services.cancerimagingarchive.net/nbia-api/services/v1/…` | none for public | 2/s | none: enumerate collections, body part and modality filters | unpaged | 2011– | yes |
| R9 | Kaggle | `www.kaggle.com/api/v1/datasets/list`, `/competitions/list` | `~/.kaggle/kaggle.json` REQUIRED | 1/s | `search=` free text → grid | 20 per page until empty | unknown (platform 2010–; datasets 2016–) | no (Kaggle terms): ids + sha1 |
| R10 | Hugging Face | `huggingface.co/api/datasets?search=`; `/api/datasets/{id}?blobs=true` | `HF_TOKEN` optional | 2/s | `search=` substring on repo id → id-like terms | `Link: rel="next"`, `limit` ≤ 1000 | 2020– (datasets hub) | yes (public metadata) |
| R11 | grand-challenge.org | `grand-challenge.org/api/v1/challenges/` (verify anonymous) → HTML all-challenges | none | 1/s | none: list, local regex | `limit`/`offset` | 2007– (first hosted challenge) | yes |
| R12 | GitHub | `api.github.com/search/repositories`; `/search/code` (token only) | `GITHUB_TOKEN` optional | 10/min, 30/min keyed | GitHub qualifiers, implicit AND | 100 per page, 1,000 per query cap | 2008– | partial: metadata yes, README bodies as sha1 |
| R13 | Papers with Code | `paperswithcode.com/api/v1/datasets/?q=` (retired 2025; verify) → static dump | none | 2/s | `q=` free text | `items_per_page` ≤ 500 | 2018–2025 (retired) | yes (CC BY-SA dump) |
| R14 | OpenDataLab | `opendatalab.com/api/v2/datasets/search`, `opendatalab.com/api/datasets`, `opendatalab.com/api/datasets/search` (undocumented; verify) | none | 1/s | `keyword=` | unknown | unknown (platform 2022–) | partial: undocumented-endpoint bodies as sha1 |
| F1 | NLM Open-i | `openi.nlm.nih.gov/api/search` (+ `openi_enrich` via Europe PMC) | none | 1/s | free text, `it=xg` / `it=c`, `coll=pmc` | `m`/`n` window of 30 | PMC open-access subset; index start not documented | no: captions are third-party text; PMCIDs, figure ids + sha1 |
| F2 | MultiCaRe | `zenodo.org/api/records/10079370` + one metadata file via the Zenodo file API | none | 1/s | record metadata + local caption regex (`sdr/figure_counts.py`) | single request + one file | PMC case reports 1990–2023 (v1) | yes (record metadata, CC BY) |
| F3 | Open-PMC-18M | `huggingface.co/api/datasets/vector-institute/open-pmc-18m?blobs=true`; `datasets-server.huggingface.co/search` (verify) | `HF_TOKEN` optional | 2/s | datasets-server full text → grid | `offset`/`length` ≤ 100 | PMC open-access to 2025 (release) | partial: API metadata yes, datasets-server rows as sha1 |
| F4 | Wikimedia Commons | `commons.wikimedia.org/w/api.php` | none | 1/s, `maxlag=5` | CirrusSearch implicit AND, `incategory:`, `filetype:` → grid | `srlimit=50`, `continue.sroffset`; `cmcontinue` | 2004– | yes (API metadata; files never fetched) |
| F5 | J-STAGE | `api.jstage.jst.go.jp/searchapi/do?service=3` | none | 1/s | `text=` space = AND → grid (en + ja) | `start`, `count` ≤ 1000 | journals from 1996 (varies by title) | partial: titles and ids yes, abstracts as sha1 |
| F6 | KoreaMed Synapse | `synapse.koreamed.org/search?q=` → `koreamed.org/search/basic.php?Query=` (HTML) | none | 1 per 2 s | free text → grid (en + ko) | HTML pages until empty | 1997– | partial: HTML pages as sha1 |
| F7 | SciELO | `search.scielo.org/?q=…&output=site&format=summary` (HTML; browser-like client as FluoroCap) | none | 1 per 2 s | boolean in `q` (verify) → else grid (en, es, pt) | `count` 50, `from` | 1997– | partial: HTML pages as sha1 |
| F8 | Redalyc | `www.redalyc.org/busquedaArticuloFiltros.oa?q=` (HTML) | none | 1 per 2 s | free text → grid (es, pt, en) | HTML pages | 2003– | partial: HTML pages as sha1 |
| S1 | Springer Nature Meta (supplementary venue sweep) | `api.springernature.com/meta/v2/json` | `SPRINGER_API_META_KEY`; absent → skipped, logged | 1/s | `q=` with `journalid:`, `onlinedatefrom:`/`onlinedateto:`, AND/OR | `p` ≤ 100, `s` offset | Scientific Data 2014– | no (Meta API terms): DOIs + sha1 |
| S2 | Unpaywall (charting tool, not a search source, not one of the 30) | `api.unpaywall.org/v2/{doi}?email=<UNPAYWALL_EMAIL>` | `UNPAYWALL_EMAIL` | 2/s | by DOI | one call per DOI | n/a | yes (API responses; PDFs never republished) |

Excluded sources, each with its reason as reported in the manuscript: Google Dataset Search and
Google Scholar (no API; terms of service forbid automated querying); YouTube, Instagram,
Reddit, Flickr, Facebook (media platforms that FluoroCap mined for single images; they do not
host subject-level medical-image datasets with a stable record and cannot be screened by
title/abstract; a dataset announced there is indexed by at least one source above);
Openverse (aggregates Commons and Flickr; Commons is searched directly, Flickr is excluded);
Common Crawl (raw web text, not a dataset index; record-level screening is not reproducible);
patents (drawings and claims, not released image collections).

---

## L1. PubMed (E-utilities)

`GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<Q>&usehistory=y&retmax=0&retmode=json&api_key=<NCBI_API_KEY>` then
`GET …/efetch.fcgi?db=pubmed&query_key=<k>&WebEnv=<w>&retstart=<i>&retmax=500&retmode=xml&api_key=<NCBI_API_KEY>`.
Without the key the `api_key` parameter is omitted, the bucket is 3/s, and the log says
`credential-free`. If the count exceeds 9,999 (history paging answers 400 above `retstart`
9,998, so 9,999 records per string are addressable; v1.0 wrote 10,000, deviations log), the
string is re-run with `[dp]` ranges 2000–2015, 2016–2020, 2021–2023, 2024–2026 as
`pubmed_01a`–`pubmed_01d`; a range still above 9,999 is retrieved to 9,999 and `cap_hit`
records it. Records: PMID, DOI,
PMCID, title, abstract, MeSH, publication types, journal, year. The animal filter is the
Cochrane form `NOT (animals[mh] NOT humans[mh])`, which removes only records indexed as animal
and not human.

```
query_id: pubmed_01
(spine[tiab] OR spinal[tiab] OR vertebra*[tiab] OR lumbar[tiab] OR thoracolumbar[tiab] OR lumbosacral[tiab] OR sacrum[tiab] OR "cervical spine"[tiab] OR "thoracic spine"[tiab] OR scoliosis[tiab] OR spondylolisthesis[tiab] OR "Spine"[mh] OR "Spinal Diseases"[mh] OR "Spinal Curvatures"[mh] OR "Spinal Fractures"[mh] OR "Spinal Injuries"[mh])
AND ("computed tomography"[tiab] OR "computed tomographic"[tiab] OR CT[tiab] OR CBCT[tiab] OR "cone-beam"[tiab] OR "cone beam"[tiab] OR radiograph*[tiab] OR "X-ray"[tiab] OR "X-rays"[tiab] OR "x ray"[tiab] OR xray*[tiab] OR roentgen*[tiab] OR fluoroscop*[tiab] OR "C-arm"[tiab] OR "image intensifier"[tiab] OR DXA[tiab] OR DEXA[tiab] OR absorptiometry[tiab] OR "vertebral fracture assessment"[tiab] OR EOS[tiab] OR biplanar[tiab] OR "plain film"[tiab] OR "plain films"[tiab] OR "Tomography, X-Ray Computed"[mh] OR "Radiography"[mh] OR "Fluoroscopy"[mh] OR "Absorptiometry, Photon"[mh])
AND (dataset[tiab] OR datasets[tiab] OR "data set"[tiab] OR "data sets"[tiab] OR database[tiab] OR benchmark*[tiab] OR challenge[tiab] OR "publicly available"[tiab] OR "public data"[tiab] OR "open data"[tiab] OR "open access"[tiab] OR "open-access"[tiab] OR "open source"[tiab] OR "data descriptor"[tiab] OR corpus[tiab] OR "image collection"[tiab] OR "Datasets as Topic"[mh] OR "Databases, Factual"[mh])
AND ("2000/01/01"[dp] : "2026/12/31"[dp])
NOT (animals[mh] NOT humans[mh])
```

```
query_id: pubmed_02
("Sci Data"[ta] OR "Data Brief"[ta] OR "Med Phys"[ta] OR "Radiol Artif Intell"[ta] OR "J Digit Imaging"[ta] OR "J Imaging Inform Med"[ta] OR "Comput Methods Programs Biomed"[ta] OR "Med Image Anal"[ta] OR "IEEE Trans Med Imaging"[ta])
AND (spine[tiab] OR spinal[tiab] OR vertebra*[tiab] OR lumbar[tiab] OR thoracolumbar[tiab] OR lumbosacral[tiab] OR sacrum[tiab] OR "cervical spine"[tiab] OR "thoracic spine"[tiab] OR scoliosis[tiab] OR spondylolisthesis[tiab])
AND ("2000/01/01"[dp] : "2026/12/31"[dp])
NOT (animals[mh] NOT humans[mh])
```

Reasoning: `pubmed_01` adds the MeSH headings whose data descriptors carry only a disease name
or neither "dataset" nor a modality word in the abstract. `pubmed_02` is a venue sweep of the
journals that publish descriptors, without the modality and dataset blocks, because a
descriptor abstract may say only "annotated spine images"; screening does the rest.

## L2. Europe PMC

`GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<Q>&resultType=core&format=json&pageSize=1000&cursorMark=<c>`.
Every block is fielded to `TITLE:`, `ABSTRACT:` and `KW:`. Unfielded terms also match the full
text of open-access articles, which the pilot search showed by count (section 6.0,
`runs/pilot-2026-09-19/queries.json`), so the unfielded form is not used. `SRC:PPR` (preprints, including bioRxiv and medRxiv) is kept.
v1.0 wrote `resultType=lite` here and `core` only at charting; `lite` carries no `abstractText`,
and the prescreen (`PROTOCOL.md` 7.2) reads title + abstract, so a record found only here would
have been screened on its title alone. `core` is sent at search time (deviations log, `PROTOCOL.md`
section 19); the same endpoint, paging and hit counts.

```
query_id: epmc_01
((TITLE:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR ABSTRACT:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR KW:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis))
AND (TITLE:("computed tomography" OR "computed tomographic" OR CT OR CBCT OR "cone-beam" OR "cone beam" OR radiograph* OR "X-ray" OR "X-rays" OR "x ray" OR xray* OR roentgen* OR fluoroscop* OR "C-arm" OR "image intensifier" OR DXA OR DEXA OR absorptiometry OR "vertebral fracture assessment" OR EOS OR biplanar OR "plain film" OR "plain films") OR ABSTRACT:("computed tomography" OR "computed tomographic" OR CT OR CBCT OR "cone-beam" OR "cone beam" OR radiograph* OR "X-ray" OR "X-rays" OR "x ray" OR xray* OR roentgen* OR fluoroscop* OR "C-arm" OR "image intensifier" OR DXA OR DEXA OR absorptiometry OR "vertebral fracture assessment" OR EOS OR biplanar OR "plain film" OR "plain films") OR KW:("computed tomography" OR CT OR CBCT OR radiograph* OR "X-ray" OR xray* OR fluoroscop* OR "C-arm" OR DXA OR DEXA OR EOS OR biplanar))
AND (TITLE:(dataset OR datasets OR "data set" OR "data sets" OR database OR benchmark* OR challenge OR "publicly available" OR "public data" OR "open data" OR "open access" OR "open-access" OR "open source" OR "data descriptor" OR corpus OR "image collection") OR ABSTRACT:(dataset OR datasets OR "data set" OR "data sets" OR database OR benchmark* OR challenge OR "publicly available" OR "public data" OR "open data" OR "open access" OR "open-access" OR "open source" OR "data descriptor" OR corpus OR "image collection") OR KW:(dataset OR datasets OR "data set" OR database OR benchmark* OR challenge OR "open data" OR "data descriptor" OR corpus))
AND (PUB_YEAR:[2000 TO 2026]) AND (SRC:MED OR SRC:PMC OR SRC:PPR))
```

```
query_id: epmc_02
((TITLE:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR ABSTRACT:(vertebra* OR "spine" OR "spinal" OR scoliosis OR "lumbar spine" OR "cervical spine" OR "thoracic spine"))
AND (HAS_DATA:y) AND (PUB_YEAR:[2000 TO 2026]))
```

Reasoning: `epmc_02` uses Europe PMC's data-link flag to reach descriptors whose abstract has
no BLOCK_D term. No animal filter (MeSH is incomplete for preprints); E2 is applied at
screening. The bioRxiv/medRxiv route (L6) is the completeness check for `SRC:PPR`.

## L3. OpenAlex

`GET https://api.openalex.org/works?filter=<F>&per-page=200&cursor=<c>&mailto=<CONTACT>&select=id,doi,ids,title,display_name,publication_year,type,primary_location,open_access,abstract_inverted_index,referenced_works,cited_by_count,authorships`.
Boolean `AND OR NOT` and quoted phrases are accepted inside `.search` filters; no wildcards;
English stemming applies, so inflections are listed. The abstract is rebuilt from the inverted
index by the adapter. If the API rejects the boolean form (status 400, logged), the fallback is
the grid `g01`–`g35` through `title_and_abstract.search`, one string per request, and the
deviation is logged.

```
query_id: openalex_01
title_and_abstract.search:((spine OR spinal OR vertebra OR vertebrae OR vertebral OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) AND ("computed tomography" OR "computed tomographic" OR CT OR CBCT OR "cone-beam" OR "cone beam" OR radiograph OR radiographs OR radiography OR radiographic OR "x-ray" OR "x-rays" OR "x ray" OR xray OR xrays OR roentgen OR roentgenographic OR fluoroscopy OR fluoroscopic OR "c-arm" OR "image intensifier" OR DXA OR DEXA OR absorptiometry OR "vertebral fracture assessment" OR EOS OR biplanar OR "plain film" OR "plain films") AND (dataset OR datasets OR "data set" OR "data sets" OR database OR benchmark OR benchmarks OR challenge OR "publicly available" OR "public data" OR "open data" OR "open access" OR "open-access" OR "open source" OR "data descriptor" OR corpus OR "image collection")),publication_year:2000-2026
```

```
query_id: openalex_02
type:dataset,title_and_abstract.search:((spine OR spinal OR vertebra OR vertebrae OR vertebral OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR scoliosis OR spondylolisthesis) AND ("computed tomography" OR CT OR CBCT OR radiograph OR radiographs OR radiography OR "x-ray" OR "x-rays" OR xray OR fluoroscopy OR DXA OR EOS OR biplanar)),publication_year:2000-2026
```

```
query_id: openalex_03_<openalex_id>
cites:<openalex_id>
```

```
query_id: openalex_03r_<openalex_id>
openalex_id:<referenced_work_id>|<referenced_work_id>|…   (the record's referenced_works, batches of 50)
```

Citation chasing, one hop, for every included source record with an OpenAlex id: one forward
request per id (`filter=cites:<id>&per-page=200`) keyed `openalex_03_<openalex_id>`, and the
record's own `referenced_works` fetched in batches keyed `openalex_03r_<openalex_id>`, both
with `grammar: chase` in `queries.json` so that each chased id has its own hit count. Results
carry `source: chase`. `sdr/appendix.py` collapses every `openalex_03*` key into one Appendix A
row giving the number of ids chased and the total hits. Reasoning: OpenAlex ingests DataCite, so
`openalex_02` reaches repository records the literature indexes miss and gives a second DOI
route for merging.

## L4. Semantic Scholar Graph API (bulk)

`GET https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=<Q>&year=2000-2026&fields=paperId,externalIds,title,abstract,year,venue,publicationTypes,isOpenAccess,openAccessPdf,citationCount,authors&token=<t>` with header `x-api-key: <S2_API_KEY>`; page by `token` until absent. Without the key the same endpoint is called at one request per 5 s and the log says `credential-free`. The non-bulk `/paper/search` (capped at 1,000) is not used. `fieldsOfStudy` is not restricted: challenge datasets appear in computer-science venues.

```
query_id: s2_01
(spine | spinal | vertebra* | lumbar | thoracolumbar | lumbosacral | sacrum | "cervical spine" | "thoracic spine" | scoliosis | spondylolisthesis) + ("computed tomography" | "computed tomographic" | CT | CBCT | "cone-beam" | "cone beam" | radiograph* | "x-ray" | "x-rays" | "x ray" | xray* | roentgen* | fluoroscop* | "c-arm" | "image intensifier" | DXA | DEXA | absorptiometry | "vertebral fracture assessment" | EOS | biplanar | "plain film" | "plain films") + (dataset | datasets | "data set" | "data sets" | database | benchmark* | challenge | "publicly available" | "public data" | "open data" | "open access" | "open-access" | "open source" | "data descriptor" | corpus | "image collection")
```

## L5. arXiv API

`GET http://export.arxiv.org/api/query?search_query=<Q>&start=<i>&max_results=500&sortBy=submittedDate&sortOrder=ascending` (Atom). `sortBy=submittedDate` makes paging stable; 500 keeps each response under the size at which arXiv truncates. No category restriction (cs.CV, eess.IV, physics.med-ph and q-bio all carry spine datasets). Phrases are sent as `%22…%22`.

```
query_id: arxiv_01
(abs:spine OR abs:spinal OR abs:vertebra OR abs:vertebrae OR abs:vertebral OR abs:lumbar OR abs:thoracolumbar OR abs:lumbosacral OR abs:sacrum OR abs:"cervical spine" OR abs:"thoracic spine" OR abs:scoliosis OR abs:spondylolisthesis OR ti:spine OR ti:vertebra OR ti:vertebrae OR ti:vertebral OR ti:scoliosis)
AND (abs:"computed tomography" OR abs:CT OR abs:CBCT OR abs:"cone-beam" OR abs:"cone beam" OR abs:radiograph OR abs:radiographs OR abs:radiography OR abs:radiographic OR abs:"x-ray" OR abs:"x-rays" OR abs:xray OR abs:fluoroscopy OR abs:fluoroscopic OR abs:"c-arm" OR abs:DXA OR abs:DEXA OR abs:EOS OR abs:biplanar OR abs:"plain film")
AND (abs:dataset OR abs:datasets OR abs:"data set" OR abs:database OR abs:benchmark OR abs:challenge OR abs:"publicly available" OR abs:"public data" OR abs:"open data" OR abs:"open access" OR abs:"open source" OR abs:corpus)
AND submittedDate:[200001010000 TO 202612312359]
```

## L6. bioRxiv and medRxiv API

There is no search endpoint. The recorded query is the harvest interval plus the local filter.
`GET https://api.biorxiv.org/details/biorxiv/<from>/<to>/<cursor>/json` for monthly intervals
from 2013-11-01 and `…/details/medrxiv/<from>/<to>/<cursor>/json` from 2019-06-01, both to
the run date (`--run-date`; v1.0 wrote 2026-12-31, deviations log), cursor step 100;
`messages[0].total` per month is recorded so the filter's
selectivity is reportable. A record is retrieved when `SPINE_RE`, `MODALITY_RE` and
`DATASET_RE` (`PROTOCOL.md` Appendix A) all match `title + abstract`. Cross-check: the Europe
PMC `SRC:PPR` result set must contain every DOI retrieved here; the symmetric difference is
reported.

```
query_id: biorxiv_01
template: https://api.biorxiv.org/details/biorxiv/<from>/<to>/<cursor>/json
intervals: monthly from 2013-11-01 to the run date ([2013-11-01, 2013-11-30], [2013-12-01, 2013-12-31], …)
filter: SPINE_RE AND MODALITY_RE AND DATASET_RE over title + abstract
```

```
query_id: medrxiv_01
template: https://api.biorxiv.org/details/medrxiv/<from>/<to>/<cursor>/json
intervals: monthly from 2019-06-01 to the run date
filter: SPINE_RE AND MODALITY_RE AND DATASET_RE over title + abstract
```

Because the request sent is one per month, the `queries.json` record for each of these two ids
carries `query_string` = the template, an explicit `intervals` list, `n_requests`, and the
per-interval `messages[0].total` values in `notes`; the appendix row states "template plus
N monthly intervals" and the summed totals, so the verbatim string reported is what was sent.

## L7. Crossref

`GET https://api.crossref.org/works?query.bibliographic=<terms>&filter=<F>&rows=1000&cursor=*&mailto=<CONTACT>&select=DOI,title,abstract,type,container-title,publisher,issued,URL,license,relation,subject,author`.
No boolean; results are relevance-ranked; each string is capped at the first 5,000 results and
the cap is recorded. Pass (a), `filter=type:dataset,from-pub-date:2000-01-01,until-pub-date:2026-12-31`,
one string per BLOCK_S term (BLOCK_M applied locally by regex):

```
crossref_01  spine
crossref_02  spinal
crossref_03  vertebra
crossref_04  vertebrae
crossref_05  vertebral
crossref_06  lumbar
crossref_07  thoracolumbar
crossref_08  lumbosacral
crossref_09  sacrum
crossref_10  scoliosis
crossref_11  spondylolisthesis
```

Pass (b), `filter=type:journal-article,type:posted-content,type:proceedings-article,has-abstract:true,from-pub-date:2000-01-01,until-pub-date:2026-12-31`
(Crossref filters are comma-separated `name:value` pairs, so the key is repeated for each
type; if the API rejects a repeated `type`, status 400 logged, the string is run as three
passes `crossref_12a`/`12b`/`12c`, one type each, and each is recorded), fixed triples:

```
crossref_12  spine CT dataset
crossref_13  vertebra CT dataset
crossref_14  vertebral segmentation dataset CT
crossref_15  spine radiograph dataset
crossref_16  spine x-ray dataset
crossref_17  lumbar spine radiograph dataset
crossref_18  cervical spine radiograph dataset
crossref_19  thoracic spine radiograph dataset
crossref_20  whole spine radiograph dataset
crossref_21  scoliosis radiograph dataset
crossref_22  vertebral fracture dataset
crossref_23  spine fluoroscopy dataset
crossref_24  spine CT benchmark
crossref_25  spine x-ray benchmark
crossref_26  vertebra segmentation challenge
crossref_27  spine database CT
crossref_28  spine database radiograph
crossref_29  spine DXA vertebral fracture assessment dataset
```

Reasoning: Crossref is the only index that carries publisher-registered dataset DOIs (IEEE
DataPort, Elsevier) with abstracts, and its `relation` field (is-supplement-to) is a merge key.

## R1. Zenodo

`GET https://zenodo.org/api/records?q=<Q>&size=100&page=<n>&sort=bestmatch`. One dialect
only, the InvenioRDM field names of the post-2023 Zenodo (`metadata.title`,
`metadata.description`, `metadata.subjects.subject` — where the legacy keywords are indexed —
`metadata.resource_type.id`, `metadata.publication_date`); the legacy shortcuts `title:`,
`description:` and `keywords:` are not used because `keywords:` matches nothing since the
migration and the shortcuts are undocumented. `*` truncation; quoted phrases. Run twice:
`zenodo_01` with the resource-type clause, `zenodo_02` without it (datasets deposited as
"other", "software" or "image" are typed locally from `metadata.resource_type`); the
difference is reported. **Pre-run clause check**: before the full run each fielded clause of
`zenodo_01` (the spine clause, the modality clause, the resource-type clause, the date clause)
is sent alone with `size=1` and must return `hits.total > 0`; the four counts are written to
`queries.json[zenodo_01].notes`, and a zero is a deviations-log row before anything else runs.
If `hits.total` exceeds 10,000 the publication-date range is split by year. Enrichment per
hit: `files[].checksum`, `files[].size`, `metadata.license.id`, `metadata.access_right`,
`metadata.related_identifiers`, `conceptdoi`.

```
query_id: zenodo_01
((metadata.title:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR metadata.description:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR metadata.subjects.subject:(spine OR spinal OR vertebra* OR scoliosis))
AND (metadata.title:(CT OR "computed tomography" OR CBCT OR "cone-beam" OR radiograph* OR "x-ray" OR "x-rays" OR xray* OR roentgen* OR fluoroscop* OR "c-arm" OR DXA OR DEXA OR EOS OR biplanar) OR metadata.description:(CT OR "computed tomography" OR "computed tomographic" OR CBCT OR "cone-beam" OR "cone beam" OR radiograph* OR "x-ray" OR "x-rays" OR "x ray" OR xray* OR roentgen* OR fluoroscop* OR "c-arm" OR "image intensifier" OR DXA OR DEXA OR absorptiometry OR "vertebral fracture assessment" OR EOS OR biplanar OR "plain film") OR metadata.subjects.subject:(CT OR radiograph* OR "x-ray" OR xray* OR fluoroscop* OR DXA))
AND metadata.resource_type.id:(dataset OR image* OR software OR other)
AND metadata.publication_date:[2000-01-01 TO 2026-12-31])
```

```
query_id: zenodo_02
((metadata.title:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR metadata.description:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR metadata.subjects.subject:(spine OR spinal OR vertebra* OR scoliosis))
AND (metadata.title:(CT OR "computed tomography" OR CBCT OR "cone-beam" OR radiograph* OR "x-ray" OR "x-rays" OR xray* OR roentgen* OR fluoroscop* OR "c-arm" OR DXA OR DEXA OR EOS OR biplanar) OR metadata.description:(CT OR "computed tomography" OR "computed tomographic" OR CBCT OR "cone-beam" OR "cone beam" OR radiograph* OR "x-ray" OR "x-rays" OR "x ray" OR xray* OR roentgen* OR fluoroscop* OR "c-arm" OR "image intensifier" OR DXA OR DEXA OR absorptiometry OR "vertebral fracture assessment" OR EOS OR biplanar OR "plain film") OR metadata.subjects.subject:(CT OR radiograph* OR "x-ray" OR xray* OR fluoroscop* OR DXA))
AND metadata.publication_date:[2000-01-01 TO 2026-12-31])
```

BLOCK_D is omitted: every Zenodo record is a deposit. Concept DOIs collapse versions.

## R2. Figshare

`POST https://api.figshare.com/v2/articles/search` with the JSON body below (`figshare_01`,
`item_type` 3 = dataset) and again with `item_type` omitted (`figshare_02`); the difference
is reported. Phrases use Figshare's documented double-quote syntax, JSON-escaped as `\"…\"`
(single quotes would be tokenised as separate terms). **Pre-run phrase check**: the one-phrase
body `{"search_for": ":description: \"lumbar spine\""}` is sent once with `page_size: 1` and
its count recorded in `queries.json[figshare_01].notes`; a zero is a deviations-log row.
Enrichment: `GET /v2/articles/{id}` (licence, DOI, `is_embargoed`, `is_public`) and
`GET /v2/articles/{id}/files` (`computed_md5`, `size`, `download_url`). Paging is by `page`;
if `page` stops before the reported total (verify), `offset`/`limit` is the fallback, used and
logged.

```
query_id: figshare_01
{"search_for": "(:title: spine OR :title: spinal OR :title: vertebra OR :title: vertebrae OR :title: vertebral OR :title: lumbar OR :title: thoracolumbar OR :title: lumbosacral OR :title: sacrum OR :title: scoliosis OR :title: spondylolisthesis OR :description: vertebra OR :description: vertebrae OR :description: vertebral OR :description: \"lumbar spine\" OR :description: \"thoracic spine\" OR :description: \"cervical spine\" OR :description: scoliosis) AND (:title: CT OR :title: \"computed tomography\" OR :title: CBCT OR :title: radiograph OR :title: radiographs OR :title: radiography OR :title: x-ray OR :title: x-rays OR :title: xray OR :title: fluoroscopy OR :title: fluoroscopic OR :title: DXA OR :title: DEXA OR :title: EOS OR :title: biplanar OR :description: \"computed tomography\" OR :description: CT OR :description: radiograph OR :description: radiographs OR :description: radiography OR :description: x-ray OR :description: x-rays OR :description: fluoroscopy OR :description: \"C-arm\" OR :description: DXA OR :description: DEXA OR :description: EOS OR :description: biplanar)", "item_type": 3, "page_size": 1000, "page": 1, "order": "published_date", "order_direction": "asc", "published_since": "2000-01-01", "published_until": "2026-12-31"}
```

```
query_id: figshare_02
(the same body with the "item_type" key removed)
```

## R3. Dryad

`GET https://datadryad.org/api/v2/search?q=<string>&per_page=100&page=<n>`; grid `dryad_g01`
… `dryad_g35` with the strings of section G unchanged. Enrichment: `GET /api/v2/datasets/{doi}`
and `GET /api/v2/versions/{id}/files` (`digest`, `digestType`, `size`).

## R4. OSF

`GET https://api.osf.io/v2/nodes/?filter[title][icontains]=<term>&filter[public]=true&page[size]=100`
(`osf_01`–`osf_08` over `t01`–`t08`), `GET https://api.osf.io/v2/registrations/?filter[title][icontains]=<term>&page[size]=100`
(`osf_09`–`osf_16`), `GET https://api.osf.io/v2/preprints/?filter[title][icontains]=<term>&page[size]=100`
(`osf_17`–`osf_24`). Description and tags fetched per hit; `MODALITY_RE` applied locally.
`Authorization: Bearer <OSF_TOKEN>` when present; otherwise the anonymous throttle (100/h,
verify) paces the run and the log says `credential-free`.

## R5. Mendeley Data

The documented API (`api.data.mendeley.com/datasets`) needs OAuth client credentials that are
not held. Credential-free behaviour, always run and logged as `mendeley-via-datacite`:
(1) one probe of the observed front-end endpoint
`GET https://data.mendeley.com/public-api/datasets/search?search=<term>&limit=50` per term
`t01`–`t08` (`mendeley_01`–`mendeley_08`; status recorded; hits used if JSON is returned);
(2) DataCite `datacite_04` below (prefix 10.17632), which is the recorded route regardless of
(1).

## R6. DataCite

`GET https://api.datacite.org/dois?query=<Q>&resource-type-id=<T>&page[size]=1000&page[cursor]=1`
then `links.next`. Lucene, fielded. Three runs: `datacite_01` with `resource-type-id=dataset`,
`datacite_02` with `resource-type-id=image`, `datacite_03` with no resource-type parameter and
`types.resourceTypeGeneral:(Dataset OR Image OR Collection)` added to the query. Enrichment:
`relatedIdentifiers`, `rightsList`, `sizes`, `formats`, `version`, `container`.

```
query_id: datacite_01
((titles.title:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR descriptions.description:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR subjects.subject:(spine OR spinal OR vertebra* OR lumbar OR scoliosis))
AND (titles.title:(CT OR "computed tomography" OR CBCT OR "cone-beam" OR radiograph* OR "x-ray" OR "x-rays" OR xray* OR roentgen* OR fluoroscop* OR "c-arm" OR DXA OR DEXA OR EOS OR biplanar) OR descriptions.description:(CT OR "computed tomography" OR "computed tomographic" OR CBCT OR "cone-beam" OR "cone beam" OR radiograph* OR "x-ray" OR "x-rays" OR "x ray" OR xray* OR roentgen* OR fluoroscop* OR "c-arm" OR "image intensifier" OR DXA OR DEXA OR absorptiometry OR "vertebral fracture assessment" OR EOS OR biplanar OR "plain film") OR subjects.subject:(CT OR "computed tomography" OR radiograph* OR "x-ray" OR xray* OR fluoroscop* OR DXA))
AND publicationYear:[2000 TO 2026])
```

```
query_id: datacite_02
(the datacite_01 string; parameter resource-type-id=image)
```

```
query_id: datacite_03
(the datacite_01 string) AND types.resourceTypeGeneral:(Dataset OR Image OR Collection)
```

```
query_id: datacite_04
(titles.title:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR descriptions.description:(spine OR spinal OR vertebra* OR lumbar OR scoliosis OR spondylolisthesis)) AND publicationYear:[2000 TO 2026]
```

`datacite_04` is sent with `&prefix=10.17632` (Mendeley Data) and only the spine clause,
because Mendeley descriptions are short; `MODALITY_RE` is applied locally. Reasoning: DataCite
spans Zenodo (10.5281), Figshare (10.6084), Dryad (10.5061), OSF (10.17605), Mendeley (10.17632),
PhysioNet (10.13026), TCIA (10.7937) and institutional repositories, so it is the merge backbone
for repository records; the per-repository sources are still run because their own APIs return
access and checksum fields DataCite does not carry.

## R7. PhysioNet

```
query_id: physionet_list
https://physionet.org/rest/database-list/   (verify; fallback: https://physionet.org/content/ paged HTML, parsed for slug, title, abstract; logged html-fallback)
```

The full list is filtered locally by `SPINE_RE` and `MODALITY_RE` over title + abstract; for
each hit `GET https://physionet.org/content/<slug>/` once and the access-policy string (`Open
Access | Credentialed Access | Restricted Access | Contributor Review`) is read by regex and
stored for the probe. Zero or near-zero spine datasets is the expected result and is reported
as a finding.

## R8. TCIA / NBIA

```
query_id: tcia_list
https://services.cancerimagingarchive.net/nbia-api/services/v1/getCollectionValues
```

For every collection: `GET …/v1/getBodyPartValues?Collection=<c>` and
`GET …/v1/getModalityValues?Collection=<c>`. A collection is a candidate when any body-part
value matches `(?i)spine|vertebr|sacr|lumbar|thorac|cervic|whole ?body|^[ctl]\s*-?\s*spine$`
and any modality is in `CT|CR|DX|RF|XA|OT`, **or** its description page
`https://www.cancerimagingarchive.net/collection/<slug>/` (fetched once) matches `SPINE_RE`.
For candidates: `GET …/v1/getPatientByCollectionAndModality?Collection=<c>&Modality=<m>` for
each eligible modality (subject counts) and `GET …/v1/getSeries?Collection=<c>&Modality=<m>`
(series counts). Chest, abdomen and pelvis collections without a spine body part or a spine
description are not candidates (they fail I1 unless a literature record describes spine
annotations on them, in which case they enter through that record). Limited-access
collections are flagged for the probe. Collection DOIs and licences from
`https://www.cancerimagingarchive.net/api/v1/collections` if it answers (verify), else
DataCite `prefix=10.7937`.

## R9. Kaggle

`GET https://www.kaggle.com/api/v1/datasets/list?search=<string>&page=<n>` (`kaggle_g01`–`kaggle_g35`)
and `GET https://www.kaggle.com/api/v1/competitions/list?search=<string>&page=<n>`
(`kaggle_c01`–`kaggle_c05` over `spine`, `vertebra`, `scoliosis`, `cervical spine`, `spine
fracture`). HTTP basic auth from `~/.kaggle/kaggle.json`. Without the file the adapter sends
one unauthenticated request, records the status, writes `credential_mode: needs-credentials`
with zero hits to `queries.json`, and runs the credential-free supplement `kaggle_mention`:
the regex `kaggle\.com/(datasets|competitions|c)/[A-Za-z0-9_-]+(/[A-Za-z0-9_-]+)?` over every
other source's title, abstract and description fields, each match recorded as a repository
record with `source: kaggle-mention`.

## R10. Hugging Face Hub

`GET https://huggingface.co/api/datasets?search=<term>&limit=1000&full=true` then the `Link`
header; `GET https://huggingface.co/api/datasets/<id>?blobs=true` per hit (card, `gated`,
`private`, `cardData.license`, `siblings[].lfs.sha256`, `siblings[].size`, `lastModified`,
`sha`). `Authorization: Bearer <HF_TOKEN>` when present. `search` matches the repository id
only, not the card, so terms are id-like; `MODALITY_RE` is applied locally to the card text
(*cervical* and *thoracic* are allowed here because ids are short and the regex removes cervix
and thorax repositories):

```
hf_01  spine
hf_02  spinal
hf_03  vertebra
hf_04  vertebrae
hf_05  verse
hf_06  scoliosis
hf_07  lumbar
hf_08  cervical
hf_09  thoracic
hf_10  sacrum
hf_11  spondylolisthesis
hf_12  spine-xray
hf_13  spine_xray
hf_14  spinexr
hf_15  spine-ct
hf_16  spinect
hf_17  ctspine
hf_18  totalsegmentator
hf_19  lstv
hf_20  dxa
hf_21  fluoroscopy
hf_22  radiograph
```

`hf_23` is `GET https://huggingface.co/api/datasets?filter=medical&limit=1000&full=true`
(tag filter, screened locally). `hf_mention` is the regex
`huggingface\.co/datasets/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+` over all other sources' text
fields, recorded as `source: hf-mention`.

## R11. grand-challenge.org

```
query_id: gc_list
https://grand-challenge.org/api/v1/challenges/?limit=100&offset=<i>   (verify anonymous access; on 401/403/404: https://grand-challenge.org/challenges/all-challenges/ parsed for slug, title, short description; logged html-fallback)
```

The full list is filtered locally by `SPINE_RE` and `MODALITY_RE`; each candidate's challenge
page is fetched once for its description and data-access statement.

## R12. GitHub

`GET https://api.github.com/search/repositories?q=<q>&per_page=100&page=<n>&sort=updated`,
`Accept: application/vnd.github+json`, `Authorization: Bearer <GITHUB_TOKEN>` when present.
Each string is capped by the API at 1,000 results and the cap is recorded. Repository
queries:

```
github_01  spine dataset CT in:name,description,readme fork:false
github_02  vertebra dataset in:name,description,readme fork:false
github_03  vertebrae segmentation dataset in:name,description,readme fork:false
github_04  spine xray dataset in:name,description,readme fork:false
github_05  spine "x-ray" dataset in:name,description,readme fork:false
github_06  spine radiograph dataset in:name,description,readme fork:false
github_07  scoliosis dataset in:name,description,readme fork:false
github_08  lumbar spine dataset in:name,description,readme fork:false
github_09  cervical spine dataset in:name,description,readme fork:false
github_10  thoracic spine dataset in:name,description,readme fork:false
github_11  spine fluoroscopy in:name,description,readme fork:false
github_12  vertebral fracture dataset in:name,description,readme fork:false
github_13  spinal dataset radiograph in:name,description,readme fork:false
github_14  spine DXA dataset in:name,description,readme fork:false
github_15  topic:spine topic:dataset
github_16  topic:vertebrae
github_17  topic:scoliosis
github_18  topic:medical-imaging spine
```

Code search (`GET https://api.github.com/search/code?q=<q>`) requires a token; without it the
two queries are recorded `needs-credentials`:

```
github_c01  "vertebra" dataset download filename:README.md
github_c02  "spine" "x-ray" dataset filename:README.md
```

## R13. Papers with Code

```
pwc_01  https://paperswithcode.com/api/v1/datasets/?q=spine&items_per_page=500&page=1
pwc_02  https://paperswithcode.com/api/v1/datasets/?q=vertebra&items_per_page=500&page=1
pwc_03  https://paperswithcode.com/api/v1/datasets/?q=vertebrae&items_per_page=500&page=1
pwc_04  https://paperswithcode.com/api/v1/datasets/?q=scoliosis&items_per_page=500&page=1
pwc_05  https://paperswithcode.com/api/v1/datasets/?q=lumbar&items_per_page=500&page=1
pwc_06  https://paperswithcode.com/api/v1/datasets/?q=spinal&items_per_page=500&page=1
```

The site was retired in 2025. Each endpoint is probed once and the status logged; on any
non-200 or off-site redirect the static dump
`https://production-media.paperswithcode.com/about/datasets.json.gz` (metadata only) is
fetched once and filtered locally by `SPINE_RE` and `MODALITY_RE` over `name`, `full_name` and
`description` (`pwc_dump`); if that too is gone the source is recorded `retired` with status
and date, and there is no further fallback (no maintained mirror can be named).

## R14. OpenDataLab

```
odl_01  https://opendatalab.com/api/v2/datasets/search?keyword=<term>&pageSize=100&pageNo=1   (candidate 1)
odl_02  https://opendatalab.com/api/datasets?keywords=<term>&pageSize=100&pageNo=1            (candidate 2)
odl_03  https://opendatalab.com/api/datasets/search?keywords=<term>&pageSize=100&pageNo=1   (candidate 3, added 2026-09-19)
```

All undocumented (verify; `odl_03` was added after the first run, which probed and recorded
it: deviations log 2026-09-19); each is probed with `t01`; the first that returns JSON is used for
`t01`–`t08` (`odl_t01`–`odl_t08`) with `MODALITY_RE` applied locally to the fetched
description. If neither answers with JSON, the HTML search page
`https://opendatalab.com/?keywords=<term>` is parsed for dataset slugs and titles
(`html-fallback`); if that also fails, `no-public-api` is recorded. The `openxlab` CLI needs a
key and is not used.

## F1. NLM Open-i

`GET https://openi.nlm.nih.gov/api/search?query=<string>&it=<type>&coll=pmc&m=<i>&n=<i+29>`,
window of 30 as in `tools/fluorocap_openi.py`, paged to `total`. Two image-type runs per
string: `it=xg` (x-ray graphics) and `it=c` (CT). Records: PMCID, article title, figure id,
caption. Open-i returns no abstract, so each distinct PMCID is enriched once through Europe PMC
— `GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:<id>&resultType=lite&format=json`,
logged under `query_id: openi_enrich` with the number of PMCIDs — and the article (title +
abstract from that call, captions appended as description) is merged by PMCID and screened as
a literature record. Purpose: (a)
count figures and distinct articles per modality for the figure-derived pool (SAP A3.4);
(b) reach articles whose caption, not abstract, names a dataset; (c) chart Open-i itself as a
figure-derived source. Strings:

```
openi_01  spine radiograph dataset
openi_02  spine x-ray dataset
openi_03  vertebra radiograph dataset
openi_04  lumbar spine radiograph
openi_05  cervical spine radiograph
openi_06  thoracic spine radiograph
openi_07  whole spine radiograph
openi_08  scoliosis radiograph
openi_09  vertebral fracture radiograph
openi_10  spine fluoroscopy
openi_11  intraoperative fluoroscopy spine
openi_12  spine CT dataset
openi_13  vertebra CT
openi_14  lumbar spine CT
openi_15  cervical spine CT
openi_16  thoracic spine CT
openi_17  sacrum CT
openi_18  spine publicly available
```

## F2. MultiCaRe

```
query_id: multicare_01
https://zenodo.org/api/records/10079370
```

```
query_id: multicare_02
https://zenodo.org/api/records/10079370/files/captions_and_labels.csv/content
```

One request for the record (licence, version, files, sizes, md5), then one download of the
metadata file `captions_and_labels.csv` through the Zenodo file API (`multicare_02`). This is
the one file the review fetches beyond 64 KiB: it is metadata, not images, and the size cap
that distinguishes a metadata file from a dataset download is 200 MB per file (its md5 from
the record is verified and its sha1 recorded in `field_sources.n_images_or_volumes =
"api:zenodo-file@<sha1>"`). `sdr/figure_counts.py` recomputes the spine-radiograph and
spine-CT sub-figure counts over the captions with `SPINE_RE` and `MODALITY_RE`, so a second
team reproduces them from the API tokens alone. MultiCaRe is charted as a figure-derived
collection. Nothing is read from the authors' cluster; if the file exceeds the cap or is
absent, the subset is charted `null` with basis `unknown`.

## F3. Open-PMC-18M

```
query_id: openpmc_01
https://huggingface.co/api/datasets/vector-institute/open-pmc-18m?blobs=true
```

```
openpmc_02  https://datasets-server.huggingface.co/search?dataset=vector-institute/open-pmc-18m&config=default&split=train&query=spine%20radiograph&offset=0&length=100
openpmc_03  … query=spine%20x-ray
openpmc_04  … query=vertebra%20radiograph
openpmc_05  … query=lumbar%20spine%20radiograph
openpmc_06  … query=cervical%20spine%20radiograph
openpmc_07  … query=thoracic%20spine%20radiograph
openpmc_08  … query=scoliosis%20radiograph
openpmc_09  … query=spine%20fluoroscopy
openpmc_10  … query=spine%20CT
openpmc_11  … query=vertebra%20CT
openpmc_12  … query=lumbar%20spine%20CT
```

If datasets-server has no search index for the dataset (404 or an error body; verify), the
spine sub-figure count is charted `null` with basis `unknown` and the log records why; no
value is read from the authors' cluster (the earlier shard scan there is not reproducible by a
second team and is not used).

## F4. Wikimedia Commons

`GET https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<string>&srnamespace=6&srlimit=50&sroffset=<i>&format=json&maxlag=5`
(`commons_g01`–`commons_g35`, each grid string with ` filetype:bitmap` appended).
`srlimit=50` is the anonymous maximum for `list=search`; the pager advances `sroffset` only to
the `continue.sroffset` value the API returns, never by a fixed increment, and any `warnings`
field in a response is logged. Then category walks
`GET …?action=query&list=categorymembers&cmtitle=<Category>&cmtype=file&cmlimit=500&cmcontinue=<c>&format=json&maxlag=5`:

```
commons_c01  Category:Radiographs of the vertebral column
commons_c02  Category:X-rays of the spine
commons_c03  Category:X-rays of the lumbar spine
commons_c04  Category:CT scans of the spine
commons_c05  Category:Scoliosis
commons_c06  Category:Spondylolisthesis
commons_c07  Category:Congenital vertebral anomalies
```

Category names are those `tools/hunt_commons.py` walked; a name that no longer resolves is
corrected in the deviations log. Per file, `prop=imageinfo&iiprop=url|size|mime|sha1|extmetadata`
in batches of 50 (licence, description). The Action API is the interface Wikimedia's API
etiquette directs contributors to; the host's `robots.txt` disallows `/w/` for crawlers and the
manuscript states the decision to use the documented API at one request per second with
`maxlag`. Commons is charted as one figure-derived source; individual files are not datasets.
A category is recorded as a candidate collection by this decidable rule: at least 10 of its
files have mime `image/*`, an `extmetadata.LicenseShortName`, and a description or category
name matching `SPINE_RE` and `MODALITY_RE`; `n_subjects` is null with basis `unknown`, and
the reviewer decides I1, E2 and E3 from the file descriptions (captions) only.

## F5. J-STAGE

`GET https://api.jstage.jst.go.jp/searchapi/do?service=3&text=<string>&pubyearfrom=2000&pubyearto=2026&count=1000&start=<i>` (Atom; space = AND; no documented OR). Parsed for title (en/ja), abstract, DOI, year.

```
jstage_01  spine CT dataset
jstage_02  spine radiograph dataset
jstage_03  vertebra database
jstage_04  spine x-ray database
jstage_05  scoliosis radiograph dataset
jstage_06  脊椎 CT データセット
jstage_07  脊椎 CT データベース
jstage_08  椎体 データベース
jstage_09  脊椎 X線 データセット
jstage_10  脊椎 単純X線 データベース
jstage_11  腰椎 CT 公開
jstage_12  側弯症 X線 データベース
jstage_13  脊椎 画像 データセット
jstage_14  脊椎 透視 データ
```

## F6. KoreaMed Synapse

`GET https://synapse.koreamed.org/search?q=<string>&page=<n>` (HTML; the call
`tools/fluorocap_journal_apis.py` uses), fallback
`GET https://koreamed.org/search/basic.php?Query=<string>`; parsed by regex for article
links, titles and DOIs; for each hit the article page
`https://synapse.koreamed.org/articles/<article_id>` is fetched once and parsed for the
`citation_abstract`, `citation_doi` and `citation_pmid` meta tags (fallback
`https://koreamed.org/article/<id>`), logged under `koreamed_enrich`; logged `html-fallback`.
Every hit is expected to merge with a PubMed record by DOI or PMID; the count that does not is
the coverage finding.

```
koreamed_01  spine CT dataset
koreamed_02  spine radiograph dataset
koreamed_03  vertebra database
koreamed_04  척추 CT 데이터셋
koreamed_05  척추 X선 데이터베이스
koreamed_06  요추 방사선 데이터
koreamed_07  척추측만증 방사선 데이터셋
koreamed_08  척추 영상 데이터베이스
koreamed_09  척추 투시 데이터
```

## F7. SciELO

`GET https://search.scielo.org/?q=<string>&lang=<l>&output=site&format=summary&count=50&from=<i>`
with the browser-like client FluoroCap uses (the portal refuses plain clients); parsed HTML,
logged `html-fallback`. Boolean in `q` is tried first (`scielo_01`–`scielo_03`, verify); if
the hit counts equal those of the bare first term, the grid form is used and recorded.

```
scielo_01  vertebra AND (radiograph OR tomography OR "x-ray") AND (dataset OR database)          lang=en
scielo_02  vértebra AND (radiografía OR tomografía) AND ("base de datos" OR "conjunto de datos")   lang=es
scielo_03  vértebra AND (radiografia OR tomografia) AND ("banco de dados" OR "conjunto de dados")  lang=pt
scielo_04  coluna vertebral tomografia banco de dados                                              lang=pt
scielo_05  radiografia coluna base de dados                                                        lang=pt
scielo_06  escoliose radiografia dataset                                                           lang=pt
scielo_07  columna vertebral tomografía base de datos                                              lang=es
scielo_08  radiografía columna base de datos                                                       lang=es
scielo_09  escoliosis radiografía conjunto de datos                                                lang=es
scielo_10  spine CT dataset                                                                        lang=en
scielo_11  spine radiograph dataset                                                                lang=en
```

## F8. Redalyc

`GET https://www.redalyc.org/busquedaArticuloFiltros.oa?q=<string>` (HTML, the call FluoroCap
uses), parsed for article ids and titles; logged `html-fallback`. If the page is rendered
client-side and no article ids appear in the HTML, the front-end JSON endpoint is discovered
by inspecting the page's network calls, recorded in `queries.json` before any hit is counted;
if nothing answers, `no-public-api`.

```
redalyc_01  columna vertebral tomografía base de datos
redalyc_02  radiografía columna base de datos
redalyc_03  escoliosis radiografía conjunto de datos
redalyc_04  vértebra radiografía base de datos
redalyc_05  coluna vertebral tomografia banco de dados
redalyc_06  radiografia coluna base de dados
redalyc_07  escoliose radiografia dataset
redalyc_08  spine CT dataset
redalyc_09  spine radiograph dataset
```

## S1. Springer Nature Meta API (supplementary venue sweep)

`GET https://api.springernature.com/meta/v2/json?q=<Q>&s=<i>&p=100&api_key=<SPRINGER_API_META_KEY>`.
Scientific Data is journal id 41597. Absent key → skipped, logged `needs-credentials`;
`pubmed_02` covers the same journal, so the sweep is a recall check, not a unique route.

```
query_id: springer_01
journalid:41597 AND (spine OR spinal OR vertebra OR vertebrae OR vertebral OR lumbar OR thoracolumbar OR lumbosacral OR sacrum OR scoliosis OR spondylolisthesis) onlinedatefrom:2014-01-01 onlinedateto:2026-12-31
```

The Meta API takes a single `year:` value, so the range is expressed with
`onlinedatefrom:`/`onlinedateto:` (verify on first run; if the constraint names differ —
`datefrom`/`dateto` — the string is corrected and the change is a deviations-log row).

## S2. Unpaywall (charting only)

`GET https://api.unpaywall.org/v2/<doi>?email=<UNPAYWALL_EMAIL>`, one call per DOI whose full
text is needed at charting; `best_oa_location.url_for_pdf` recorded; the PDF fetch is logged
like any other request and cached under `raw/fulltext/`. Not a search source; no query_id in
the appendix table.

---

## What is recorded for every query

`queries.json[query_id] = {source, role ("search" | "supplement" | "fallback" | "probe" |
"pilot" | "chase" | "enrich"), endpoint, method, query_string (verbatim, unencoded; the
template for interval sources), intervals (list of [from, to] for template sources, else
null), n_requests, n_failed_requests (requests that did not answer: status 0, a 5xx, or a
429 that outlived every attempt), partial (true when n_failed_requests is above zero: a
paging loop reads a failure as end-of-results, so the counts of that query are lower
bounds), params (secret-stripped), grammar ("boolean" | "grid" | "dump-filter" | "list" |
"chase"), coverage (from the summary table, or "unknown"), run_date, first_request_ts,
last_request_ts, hit_count_api (the source's own reported total, null when it reports none;
never the retrieved count), unit ("records" | "figures" | "files" | "harvest": what that
total counts), n_fetched (items the source handed over before any local filter),
n_retrieved, n_pages, cap_hit (null or the cap), date_filter ("api" | "local" | "none"),
credential_mode ("keyed" | "credential-free" | "needs-credentials" | "html-fallback" |
"no-public-api" | "retired" | "not-run"), raw_cache_published (true | false, with the reason
from the summary table), notes}`. A consumer that adds hit counts across sources adds
`unit == "records"` and `role == "search"` only; `counts.json` does this in
`hit_count_api_total` and keeps the rest in `hit_count_by_unit`.
`sdr/appendix.py` renders it to `tables/search_strings.tex`, one row per query_id (the
`openalex_03*` chase keys collapsed to one summary row; the pilot record's three rows marked
"pilot"), which is Appendix A of the manuscript.
