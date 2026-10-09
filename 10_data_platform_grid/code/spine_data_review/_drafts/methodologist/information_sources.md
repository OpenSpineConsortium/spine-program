# Information sources and verbatim search strings

Protocol version 1.0, 2026-09-19. Each source has one block: endpoint, authentication, rate
limit, what the index covers, paging cap, syntax notes, and the query string(s) exactly as the
code sends them (URL-encoding aside). The term blocks are fixed in PROTOCOL.md §6.1 and are
translated here into each source's own syntax; where a source cannot take a boolean query, the
fixed list of term pairs is given. Hit counts are not in this document: they are recorded by the
run in `runs/<run-date>/counts.json` and copied into the manuscript's Appendix A by code.
Endpoints marked *unverified* are taken from public documentation or observed client
behaviour and are confirmed on the first run; a failing endpoint is logged as `unreachable`
with its status and the fallback named here is used.

Credential names (values never printed): `NCBI_API_KEY`, `S2_API_KEY`,
`FLUOROCAP_CONTACT_EMAIL` (the `mailto`), `UNPAYWALL_EMAIL` (full-text resolution only, not a
search source), optional `~/.kaggle/kaggle.json`, `HF_TOKEN`, `GITHUB_TOKEN`.
`SPRINGER_API_*` keys exist in the store and are not used: Springer's API indexes one
publisher's content, which PubMed, Europe PMC, OpenAlex and Crossref already cover.

User agent for every request: `spine-data-review/1.0 (scoping review; mailto:<contact>)`.

## Summary table

| # | Source | Endpoint | Auth | Rate limit used | Indexes | Paging cap | Query mode |
|---|---|---|---|---|---|---|---|
| L1 | PubMed | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`, `efetch.fcgi` | `NCBI_API_KEY` optional | 10/s with key, 3/s without | MEDLINE + PubMed in-process, title/abstract/MeSH | esearch retmax 10,000; history + efetch retstart beyond that | boolean, fielded |
| L2 | Europe PMC | `www.ebi.ac.uk/europepmc/webservices/rest/search` | none | 2/s | PubMed + PMC + preprints (bioRxiv, medRxiv, arXiv via SRC:PPR) + Agricola etc. | none (cursorMark) | boolean, fielded |
| L3 | OpenAlex | `api.openalex.org/works` | `mailto` (polite pool) | 10/s, 100k/day | 250 M works incl. DataCite datasets (type = dataset) | none (cursor) | boolean in `title_and_abstract.search` |
| L4 | Semantic Scholar | `api.semanticscholar.org/graph/v1/paper/search/bulk` | `S2_API_KEY` optional | 1/s with key; 1 per 3 s shared pool without | ~220 M papers, title + abstract | none (token), ≤ 10 M | boolean (`+ | - " " * ( )`) |
| L5 | arXiv | `export.arxiv.org/api/query` | none | 1 per 3 s | arXiv all categories, title/abstract | `start` ≤ 30,000; `max_results` 2,000 per call | boolean, fielded |
| L6 | bioRxiv / medRxiv | `api.biorxiv.org/details/{server}/{from}/{to}/{cursor}` | none | 2/s | all preprints on each server | none (cursor by 100) | full harvest + local regex |
| L7 | Crossref | `api.crossref.org/works` | `mailto` (polite pool) | polite pool (~50/s allowed; 2/s used) | DOIs of articles, datasets, preprints | `rows` ≤ 1,000; `cursor` for deep paging | term relevance, no boolean |
| R1 | Zenodo | `zenodo.org/api/records` | none | 1/s (guest limit 60/min) | Zenodo records, all types | 10,000 per query (Elasticsearch window) | Lucene boolean |
| R2 | Figshare | `api.figshare.com/v2/articles/search` (POST) | none | 2/s | Figshare public items | `page_size` ≤ 1,000; offset ≤ 9,000 (*unverified*) | boolean AND/OR/NOT, `:title:` fields |
| R3 | Dryad | `datadryad.org/api/v2/search` | none | 2/s | Dryad datasets | `per_page` ≤ 100 | plain terms |
| R4 | OSF | `api.osf.io/v2/nodes/`, `/v2/registrations/`, `/v2/preprints/` | none | 1/s (anonymous throttle) | OSF projects, registrations, preprints | `page[size]` ≤ 100 | `filter[title][icontains]` per term |
| R5 | Mendeley Data | `data.mendeley.com/api/research-data/search` (*unverified*) → fallback DataCite `prefix:10.17632` | none | 2/s | Mendeley Data datasets | unknown | plain terms |
| R6 | DataCite | `api.datacite.org/dois` | none | 2/s | all DataCite DOIs (covers Zenodo, Figshare, Dryad, Mendeley, PhysioNet, TCIA, institutional) | none (`page[cursor]`) | Lucene boolean, fielded |
| R7 | PhysioNet | `physionet.org/rest/database-list/` (*unverified*; fallback HTML `physionet.org/content/`) | none | 1/s | all published PhysioNet projects | none (single list) | full list + local regex |
| R8 | TCIA / NBIA | `services.cancerimagingarchive.net/nbia-api/services/v1/{getCollectionValues,getBodyPartValues,getModalityValues,getSeries}` | none for public | 2/s | TCIA collections, series metadata | none | enumerate + filter |
| R9 | Kaggle | `www.kaggle.com/api/v1/datasets/list?search=` and `/competitions/list?search=` | basic auth from `~/.kaggle/kaggle.json`; **401 without** → logged `needs credentials` | 1/s | Kaggle datasets and competitions | 20 per page, `page` param | plain terms |
| R10 | Hugging Face | `huggingface.co/api/datasets?search=` | `HF_TOKEN` optional (raises limits) | 2/s | HF dataset repos (id, tags, card) | `limit` ≤ 1,000 per call; `Link` header paging | substring per term |
| R11 | grand-challenge.org | `grand-challenge.org/api/v1/challenges/` (*unverified*; fallback HTML `grand-challenge.org/challenges/all-challenges/`) | none / token | 1/s | challenges, their descriptions | `limit`/`offset` | list + local regex |
| R12 | GitHub | `api.github.com/search/repositories`; `/search/code` | `GITHUB_TOKEN` optional; code search **requires** it | 10/min without, 30/min with | public repositories | 1,000 per query | GitHub search syntax |
| R13 | Papers with Code | `paperswithcode.com/api/v1/datasets/?q=` | none | 2/s | PwC dataset index (site retired 2025; probe and log) | `items_per_page` ≤ 500 | plain terms |
| R14 | OpenDataLab | `opendatalab.com/api/datasets` (*unverified*; fallback HTML search) | none | 1/s | OpenDataLab catalogue | unknown | plain terms |
| F1 | NLM Open-i | `openi.nlm.nih.gov/api/search` | none | 1/s | PMC figures with captions, image-type classes | `n` ≤ 10,000 per query (*unverified*), 100 per page | plain terms + `it=` filter |
| F2 | MultiCaRe | `zenodo.org/api/records/10079370` + local `captions_and_labels.csv` (already on the grid from FluoroCap) | none | 1/s | PMC case-report sub-figures with captions and labels | NA | record metadata + local regex over captions |
| F3 | Open-PMC-18M | `huggingface.co/api/datasets/vector-institute/open-pmc-18m` + local shards where present | `HF_TOKEN` optional | 2/s | 18 M decomposed PMC sub-figures with modality labels | NA | record metadata + local regex where shards exist; else `unknown` |
| F4 | Wikimedia Commons | `commons.wikimedia.org/w/api.php` (`action=query&list=search`) with `maxlag=5` | none | 1/s | Commons files (namespace 6) | 10,000 per query (`sroffset`) | CirrusSearch: terms, `incategory:` |
| F5 | J-STAGE | `api.jstage.jst.go.jp/searchapi/do` | none | 1/s | Japanese journal articles | `count` ≤ 1,000 per call, `start` paging | plain terms (`text`, `article`, `abst`) |
| F6 | KoreaMed Synapse | `synapse.koreamed.org/search?q=` (HTML; fallback `koreamed.org/search/basic.php?Query=`) | none | 1 per 2 s | Korean medical journals | HTML paging | plain terms |
| F7 | SciELO | `search.scielo.org/?q=&output=site&format=summary&count=50&from=` (HTML) | none | 1 per 2 s | Latin-American / Iberian journals | `from` paging | plain terms, `lang` param |
| F8 | Redalyc | `www.redalyc.org/busquedaArticuloFiltros.oa?q=` (HTML) | none | 1 per 2 s | Latin-American journals | HTML paging | plain terms |

Excluded sources, with the reason recorded in the manuscript: Google Dataset Search and Google
Scholar (no API; terms of service forbid automated querying), YouTube, Instagram, Reddit,
Flickr, Facebook (media platforms; content there is not a dataset under I4), Common Crawl (a
web crawl, not a dataset index; record-level screening is not reproducible), patents (describe
methods and claims, not released image collections).

---

## L1. PubMed (E-utilities)

Endpoint: `GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<Q>&usehistory=y&retmax=0&api_key=<NCBI_API_KEY>` then
`GET .../efetch.fcgi?db=pubmed&query_key=<k>&WebEnv=<w>&retstart=<i>&retmax=500&retmode=xml`.
Without a key the code sleeps to 3/s and logs `credential: none`.

Syntax: `[tiab]` title/abstract, `[mh]` MeSH heading with explosion, `*` right truncation
(not inside quoted phrases), `[dp]` publication date. MeSH terms are added for recall on
indexed records; `[tiab]` carries in-process records. The animal filter is the Cochrane form
`NOT (animals[mh] NOT humans[mh])`, which removes only records indexed as animal and not human.

```
(spine[tiab] OR spinal[tiab] OR vertebra*[tiab] OR lumbar[tiab] OR thoracolumbar[tiab] OR lumbosacral[tiab] OR "cervical spine"[tiab] OR "thoracic spine"[tiab] OR scoliosis[tiab] OR spondylolisthesis[tiab] OR "Spine"[mh] OR "Spinal Diseases"[mh] OR "Spinal Curvatures"[mh] OR "Spinal Fractures"[mh] OR "Spinal Injuries"[mh])
AND
("computed tomography"[tiab] OR "computed tomographic"[tiab] OR CT[tiab] OR CBCT[tiab] OR "cone-beam"[tiab] OR radiograph*[tiab] OR "X-ray"[tiab] OR "X-rays"[tiab] OR "x ray"[tiab] OR roentgen*[tiab] OR fluoroscop*[tiab] OR "C-arm"[tiab] OR DXA[tiab] OR DEXA[tiab] OR "vertebral fracture assessment"[tiab] OR "EOS imaging"[tiab] OR biplanar[tiab] OR "Tomography, X-Ray Computed"[mh] OR "Radiography"[mh] OR "Fluoroscopy"[mh] OR "Absorptiometry, Photon"[mh])
AND
(dataset[tiab] OR datasets[tiab] OR "data set"[tiab] OR "data sets"[tiab] OR database[tiab] OR benchmark*[tiab] OR challenge[tiab] OR "publicly available"[tiab] OR "public data"[tiab] OR "open data"[tiab] OR "open-access data"[tiab] OR "open source"[tiab] OR "data descriptor"[tiab] OR corpus[tiab] OR "image collection"[tiab] OR "Datasets as Topic"[mh] OR "Databases, Factual"[mh])
AND ("2000/01/01"[dp] : "2026/12/31"[dp])
NOT (animals[mh] NOT humans[mh])
```

Reasoning: Block S adds MeSH "Spine" (explodes to every vertebral region) and the disease
headings whose datasets often carry only the disease name; Block M adds the modality MeSH
headings and the DXA heading; Block D adds "Datasets as Topic" and "Databases, Factual",
which index data descriptors that use neither word in the abstract.

## L2. Europe PMC

Endpoint: `GET https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<Q>&resultType=lite&format=json&pageSize=1000&cursorMark=<c>`.
Syntax: every block is fielded to `TITLE:`, `ABSTRACT:` and `KW:` (keywords). **Unfielded
terms in Europe PMC also match the full text of open-access articles**: a count-only syntax
check on 2026-09-19 returned 214,305 hits for the unfielded form of this string against 5,810
for the PubMed string and 5,846 for the fielded form below, so the unfielded form is not used.
`*` truncation and quoted phrases work inside fielded groups; `PUB_YEAR:[a TO b]`; preprints
are included by default (`SRC:PPR`) and are kept.

```
(TITLE:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR ABSTRACT:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) OR KW:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis))
AND (TITLE:("computed tomography" OR "computed tomographic" OR CT OR CBCT OR "cone-beam" OR radiograph* OR "X-ray" OR "X-rays" OR roentgen* OR fluoroscop* OR "C-arm" OR DXA OR DEXA OR "vertebral fracture assessment" OR "EOS imaging" OR biplanar) OR ABSTRACT:("computed tomography" OR "computed tomographic" OR CT OR CBCT OR "cone-beam" OR radiograph* OR "X-ray" OR "X-rays" OR roentgen* OR fluoroscop* OR "C-arm" OR DXA OR DEXA OR "vertebral fracture assessment" OR "EOS imaging" OR biplanar) OR KW:("computed tomography" OR "computed tomographic" OR CT OR CBCT OR "cone-beam" OR radiograph* OR "X-ray" OR "X-rays" OR roentgen* OR fluoroscop* OR "C-arm" OR DXA OR DEXA OR "vertebral fracture assessment" OR "EOS imaging" OR biplanar))
AND (TITLE:(dataset OR datasets OR "data set" OR "data sets" OR database OR benchmark* OR challenge OR "publicly available" OR "public data" OR "open data" OR "open source" OR "data descriptor" OR corpus OR "image collection") OR ABSTRACT:(dataset OR datasets OR "data set" OR "data sets" OR database OR benchmark* OR challenge OR "publicly available" OR "public data" OR "open data" OR "open source" OR "data descriptor" OR corpus OR "image collection") OR KW:(dataset OR datasets OR "data set" OR "data sets" OR database OR benchmark* OR challenge OR "publicly available" OR "public data" OR "open data" OR "open source" OR "data descriptor" OR corpus OR "image collection"))
AND (PUB_YEAR:[2000 TO 2026])
```

Reasoning: same three blocks; no animal filter because Europe PMC's MeSH coverage is
incomplete for preprints and screening handles E2. Europe PMC is also the cross-check for L6
(bioRxiv/medRxiv) and for arXiv medical preprints. The two syntax-check counts above are not
the review's search; the search's counts are recorded at run time.

## L3. OpenAlex

Endpoint (a): `GET https://api.openalex.org/works?filter=title_and_abstract.search:<Q>,publication_year:2000-2026&per-page=200&cursor=<c>&mailto=<FLUOROCAP_CONTACT_EMAIL>&select=id,doi,ids,title,publication_year,type,primary_location,abstract_inverted_index,authorships`.
Endpoint (b), typed datasets: `GET https://api.openalex.org/works?filter=type:dataset,default.search:<Q_b>,publication_year:2000-2026&per-page=200&cursor=<c>&mailto=<…>`.

Syntax: boolean `AND OR NOT` and quoted phrases are supported in `.search` filters; no
wildcards, English stemming applies, so inflections are listed explicitly. If the API rejects
the boolean form (logged status 400), the fallback is the enumerated S × M pairs of L7 run
through `title_and_abstract.search` one at a time, and the deviation is logged.

Query (a):
```
(spine OR spinal OR vertebra OR vertebrae OR vertebral OR lumbar OR thoracolumbar OR lumbosacral OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) AND ("computed tomography" OR CT OR CBCT OR "cone beam" OR radiograph OR radiographs OR radiography OR radiographic OR "x-ray" OR "x-rays" OR roentgen OR fluoroscopy OR fluoroscopic OR "c-arm" OR DXA OR DEXA OR "vertebral fracture assessment" OR "EOS imaging" OR biplanar) AND (dataset OR datasets OR "data set" OR database OR benchmark OR challenge OR "publicly available" OR "public data" OR "open data" OR "open source" OR "data descriptor" OR corpus OR "image collection")
```
Query (b), type = dataset (Block D is implied by the type):
```
(spine OR spinal OR vertebra OR vertebrae OR vertebral OR lumbar OR thoracolumbar OR lumbosacral OR scoliosis OR spondylolisthesis) AND ("computed tomography" OR CT OR radiograph OR radiographs OR radiography OR "x-ray" OR "x-rays" OR fluoroscopy OR DXA OR EOS OR biplanar)
```

Reasoning: OpenAlex ingests DataCite, so (b) reaches repository datasets the literature
indexes miss and gives a second route to Zenodo/Figshare records for deduplication by DOI.

## L4. Semantic Scholar Graph API (bulk search)

Endpoint: `GET https://api.semanticscholar.org/graph/v1/paper/search/bulk?query=<Q>&year=2000-2026&fields=externalIds,title,abstract,year,venue,publicationTypes,openAccessPdf,citationCount&token=<t>` with header `x-api-key: <S2_API_KEY>` when present; without it the code runs at one request per 3 s and logs `credential: none`.

Syntax (bulk endpoint only): `+` AND, `|` OR, `-` NOT, `"phrase"`, `*` prefix, `( )` grouping.
Matches title and abstract.

```
(spine | spinal | vertebra* | lumbar | thoracolumbar | lumbosacral | "cervical spine" | "thoracic spine" | scoliosis | spondylolisthesis) + ("computed tomography" | CT | CBCT | "cone-beam" | radiograph* | "x-ray" | "x-rays" | roentgen* | fluoroscop* | "c-arm" | DXA | DEXA | "vertebral fracture assessment" | "EOS imaging" | biplanar) + (dataset | datasets | "data set" | database | benchmark* | challenge | "publicly available" | "public data" | "open data" | "open source" | "data descriptor" | corpus | "image collection")
```

Reasoning: S2 covers conference proceedings (MICCAI, ISBI, CVPR workshops) where challenge
datasets are described and which PubMed does not index.

## L5. arXiv API

Endpoint: `GET http://export.arxiv.org/api/query?search_query=<Q>&start=<i>&max_results=2000&sortBy=submittedDate&sortOrder=ascending`.
Syntax: `abs:` `ti:` fields, `AND OR ANDNOT`, quoted phrases as `%22…%22`, no wildcards;
`submittedDate:[…]` range. Inflections listed explicitly. No category restriction (recall over
precision; cs.CV, eess.IV, physics.med-ph and q-bio all carry spine datasets).

```
(abs:spine OR abs:spinal OR abs:vertebra OR abs:vertebrae OR abs:vertebral OR abs:lumbar OR abs:thoracolumbar OR abs:lumbosacral OR abs:"cervical spine" OR abs:"thoracic spine" OR abs:scoliosis OR abs:spondylolisthesis) AND (abs:"computed tomography" OR abs:CT OR abs:CBCT OR abs:"cone-beam" OR abs:radiograph OR abs:radiographs OR abs:radiography OR abs:radiographic OR abs:"x-ray" OR abs:"x-rays" OR abs:fluoroscopy OR abs:fluoroscopic OR abs:"c-arm" OR abs:DXA OR abs:DEXA OR abs:biplanar) AND (abs:dataset OR abs:datasets OR abs:"data set" OR abs:database OR abs:benchmark OR abs:challenge OR abs:"publicly available" OR abs:"public data" OR abs:"open data" OR abs:"open source" OR abs:corpus) AND submittedDate:[200001010000 TO 202612312359]
```

## L6. bioRxiv and medRxiv API

Endpoint: `GET https://api.biorxiv.org/details/biorxiv/2013-11-01/2026-12-31/<cursor>` and
`GET https://api.biorxiv.org/details/medrxiv/2019-06-01/2026-12-31/<cursor>`; cursor advances
by 100; `messages[0].total` recorded as the interval size. There is no search endpoint, so the
"query" is: harvest every record in the interval; apply `SPINE_RE`, `MODALITY_RE` and
`DATASET_RE` (PROTOCOL.md Appendix A) to `title + abstract`; a record is retrieved when all
three match. The regexes, the harvest interval and the total harvested are the recorded query.
Cross-check: the Europe PMC result set restricted to `SRC:PPR` must contain every bioRxiv/medRxiv
DOI retrieved here; the symmetric difference is reported.

## L7. Crossref

Endpoint: `GET https://api.crossref.org/works?query.bibliographic=<terms>&filter=type:<T>,from-pub-date:2000-01-01,until-pub-date:2026-12-31&rows=1000&cursor=*&mailto=<FLUOROCAP_CONTACT_EMAIL>&select=DOI,title,abstract,type,issued,container-title,author,URL`.

Syntax: no boolean; terms are relevance-ranked; deep paging by `cursor` returns every match, so
each query is capped at the first 5,000 results by relevance (cap recorded). Two passes:

Pass (a), `type:dataset`, one query per Block S term (Block M applied locally by regex):
```
spine | spinal | vertebra | vertebrae | vertebral | lumbar | thoracolumbar | lumbosacral | scoliosis | spondylolisthesis
```
Pass (b), `type:journal-article,posted-content,proceedings-article`, the fixed S × M × D triples:
```
"spine CT dataset" | "vertebra CT dataset" | "vertebral segmentation dataset CT" | "spine radiograph dataset" | "spine x-ray dataset" | "lumbar spine radiograph dataset" | "cervical spine radiograph dataset" | "scoliosis radiograph dataset" | "vertebral fracture dataset" | "spine fluoroscopy dataset" | "spine CT benchmark" | "spine x-ray benchmark" | "vertebra segmentation challenge" | "spine database CT" | "spine database radiograph"
```

Reasoning: Crossref is the only index that carries publisher-registered dataset DOIs
(e.g. IEEE DataPort, Elsevier/Mendeley) with abstracts; its journal-article pass is a
low-cost recall check against L1–L4.

## R1. Zenodo

Endpoint: `GET https://zenodo.org/api/records?q=<Q>&size=100&page=<n>&sort=mostrecent` run
twice: once with `&type=dataset`, once without a type filter (datasets deposited as "other",
"software" or "image" are typed locally from `metadata.resource_type`). Syntax: Elasticsearch
query string; unfielded terms search title, description, keywords, subjects; `*` truncation;
quoted phrases.

```
(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR "cervical spine" OR "thoracic spine" OR scoliosis OR spondylolisthesis) AND (CT OR "computed tomography" OR CBCT OR radiograph* OR "x-ray" OR "x-rays" OR xray OR roentgen* OR fluoroscop* OR "c-arm" OR DXA OR DEXA OR EOS OR biplanar)
```

Block D is omitted because every Zenodo record is a deposit. Concept DOIs collapse versions.
`access_right` and `files` are stored for the probe (PROTOCOL.md Appendix B, rule 1).

## R2. Figshare

Endpoint: `POST https://api.figshare.com/v2/articles/search` with body
`{"search_for": "<Q>", "item_type": 3, "page_size": 1000, "page": <n>, "published_since": "2000-01-01", "order": "published_date", "order_direction": "asc"}`; a second run without `item_type`. Syntax: `AND OR NOT`, quotes, `:title:` `:description:` field prefixes; wildcards not relied on.

```
(spine OR spinal OR vertebra OR vertebrae OR vertebral OR lumbar OR thoracolumbar OR lumbosacral OR scoliosis OR spondylolisthesis) AND (CT OR "computed tomography" OR CBCT OR radiograph OR radiographs OR radiography OR "x-ray" OR "x-rays" OR xray OR fluoroscopy OR fluoroscopic OR "c-arm" OR DXA OR DEXA OR EOS OR biplanar)
```

## R3. Dryad

Endpoint: `GET https://datadryad.org/api/v2/search?q=<term>&per_page=100&page=<n>`, one call
series per term; Block M applied locally.
```
spine | spinal | vertebra | vertebrae | vertebral | lumbar | scoliosis | spondylolisthesis
```

## R4. OSF

Endpoints: `GET https://api.osf.io/v2/nodes/?filter[title][icontains]=<term>&filter[public]=true&page[size]=100`,
`GET https://api.osf.io/v2/registrations/?filter[title][icontains]=<term>&page[size]=100`,
`GET https://api.osf.io/v2/preprints/?filter[title][icontains]=<term>&page[size]=100`.
Terms as R3; description fetched per hit and Block M applied locally. OSF's own search
endpoint is not used because it is not documented as stable.

## R5. Mendeley Data

Endpoint (*unverified*, observed from the site's client): `GET https://data.mendeley.com/api/research-data/search?search=<term>&type=DATASET&page=<n>`.
Fallback on any non-200: DataCite (R6) with `prefix:10.17632` added to the query, which is
Mendeley Data's DOI prefix; the fallback is logged. Terms as R3.

## R6. DataCite

Endpoint: `GET https://api.datacite.org/dois?query=<Q>&resource-type-id=<dataset|image|collection>&page[size]=1000&page[cursor]=1`, three runs (one per resource type). Syntax: Lucene, fielded.

```
(titles.title:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR scoliosis OR spondylolisthesis) OR descriptions.description:(spine OR spinal OR vertebra* OR lumbar OR thoracolumbar OR lumbosacral OR scoliosis OR spondylolisthesis) OR subjects.subject:(spine OR spinal OR vertebra* OR lumbar OR scoliosis)) AND (titles.title:(CT OR "computed tomography" OR CBCT OR radiograph* OR "x-ray" OR "x-rays" OR xray OR fluoroscop* OR "c-arm" OR DXA OR DEXA OR EOS OR biplanar) OR descriptions.description:(CT OR "computed tomography" OR CBCT OR radiograph* OR "x-ray" OR "x-rays" OR xray OR fluoroscop* OR "c-arm" OR DXA OR DEXA OR EOS OR biplanar) OR subjects.subject:(CT OR "computed tomography" OR radiograph* OR "x-ray" OR fluoroscop*)) AND publicationYear:[2000 TO 2026]
```

Reasoning: DataCite spans Zenodo, Figshare, Dryad, Mendeley, PhysioNet, TCIA and institutional
repositories, so it is the deduplication backbone for repository records; the per-repository
sources are still run because their APIs return access fields DataCite does not carry.

## R7. PhysioNet

Endpoint (*unverified*): `GET https://physionet.org/rest/database-list/`; fallback: the HTML
listing `https://physionet.org/content/` paged, parsed for project slug, title and abstract.
No query: the full list is filtered locally by `SPINE_RE` and `MODALITY_RE` over title +
abstract; the access policy field (open / restricted / credentialed / contributor-review) is
stored for the probe.

## R8. TCIA / NBIA

Endpoints: `GET .../v1/getCollectionValues`; for each collection `GET .../v1/getBodyPartValues?Collection=<c>` and `GET .../v1/getModalityValues?Collection=<c>`; for candidate collections `GET .../v1/getSeries?Collection=<c>&Modality=<m>` for `m ∈ {CT, CR, DX, RF, XA, OT}` to count series and subjects.

Rule: a collection is a candidate when any body part value matches
`(?i)^(c|t|l)?\s*-?\s*spine$|spine|vertebr|sacr|lumbar|thorac(ic)? spine|cervical spine|whole ?body` **or** the collection's TCIA description page (fetched once, `https://www.cancerimagingarchive.net/collection/<slug>/`) matches `SPINE_RE`. Chest/abdomen/pelvis collections without a spine body part or description match are not candidates (they fail I1 unless a literature record describes spine annotations on them, in which case they enter through that record). "Limited access" collections are recorded with the flag for the probe.

## R9. Kaggle

Endpoints: `GET https://www.kaggle.com/api/v1/datasets/list?search=<term>&page=<n>` and
`GET https://www.kaggle.com/api/v1/competitions/list?search=<term>&page=<n>`, HTTP basic
auth from `~/.kaggle/kaggle.json`. Without the file the code sends one unauthenticated request,
records the 401 and writes `kaggle: needs credentials` to the log and to `counts.json`.
Terms:
```
spine | vertebra | vertebrae | spinal | lumbar | scoliosis | "cervical spine" | "spine x-ray" | "spine xray" | "spine ct" | "vertebral fracture" | spondylolisthesis
```

## R10. Hugging Face

Endpoint: `GET https://huggingface.co/api/datasets?search=<term>&limit=1000&full=true`, then
`GET https://huggingface.co/api/datasets/<id>` for each hit (card, `gated`, `private`,
`cardData.license`, siblings). Header `Authorization: Bearer <HF_TOKEN>` when present. The
`search` parameter matches the repository id and name, so terms are id-like:
```
spine | vertebra | vertebrae | spinal | lumbar | scoliosis | verse | totalsegmentator | spinexr | spine-xray | spine_xray | spinect | spine-ct | ctspine | cervical | thoracic | sacrum | dxa | fluoroscopy | radiograph
```
Block M is applied locally to the card text; "cervical" and "thoracic" alone are allowed here
because HF ids are short and the local regex removes cervix and thorax datasets.

## R11. grand-challenge.org

Endpoint (*unverified*): `GET https://grand-challenge.org/api/v1/challenges/?limit=100&offset=<i>`;
on 401/403/404 the fallback is the HTML page `https://grand-challenge.org/challenges/all-challenges/`, parsed for challenge slug, title and short description, logged as `html`. The full list is filtered locally by `SPINE_RE` and `MODALITY_RE`; each candidate's challenge page is fetched once for its description and data-access statement.

## R12. GitHub

Endpoint: `GET https://api.github.com/search/repositories?q=<q>&per_page=100&page=<n>&sort=updated`, header `Authorization: Bearer <GITHUB_TOKEN>` when present (rate 30/min; 10/min without, logged). Queries (each ≤ 1,000 results by the API's cap, recorded):
```
spine dataset CT in:name,description,readme,topics
vertebra dataset in:name,description,readme,topics
vertebrae segmentation dataset in:name,description,readme,topics
spine xray dataset in:name,description,readme,topics
spine x-ray dataset in:name,description,readme,topics
spine radiograph dataset in:name,description,readme,topics
scoliosis dataset in:name,description,readme,topics
lumbar spine dataset in:name,description,readme,topics
cervical spine dataset in:name,description,readme,topics
spine fluoroscopy in:name,description,readme,topics
vertebral fracture dataset in:name,description,readme,topics
spinal dataset radiograph in:name,description,readme,topics
```
Code search (`GET https://api.github.com/search/code?q=<q>`) requires a token; queries
`"vertebra" dataset download extension:md` and `"spine" "x-ray" dataset extension:md` run
only when `GITHUB_TOKEN` is present, else logged `needs credentials`.

## R13. Papers with Code

Endpoint: `GET https://paperswithcode.com/api/v1/datasets/?q=<term>&items_per_page=500&page=<n>`. The site was retired in 2025; the endpoint is probed once per term, the status logged, and on any non-200 the source is recorded as `unavailable` in `counts.json` with no fallback (there is no maintained mirror of the dataset index that the protocol can name). Terms as R3.

## R14. OpenDataLab

Endpoint (*unverified*): `GET https://opendatalab.com/api/datasets?keywords=<term>&pageSize=100&pageNo=<n>`; fallback: the HTML search page `https://opendatalab.com/?keywords=<term>`, parsed for dataset slugs and titles, logged as `html`. Terms as R3; Block M applied locally to the fetched description.

## F1. NLM Open-i

Endpoint: `GET https://openi.nlm.nih.gov/api/search?query=<q>&it=xg&coll=pmc&m=<i>&n=<i+99>` (image type `xg` = x-ray graphics; a second run with `it=c` for CT). Purpose: count figures (and distinct articles) per modality for the figure-derived pool (SAP §4.4) and chart Open-i as a figure-derived source. Queries (S × M pairs in Open-i's plain syntax):
```
spine radiograph | spine x-ray | lumbar spine radiograph | cervical spine radiograph | thoracic spine radiograph | whole spine radiograph | scoliosis radiograph | vertebral fracture radiograph | spine fluoroscopy | spine CT | vertebra CT | lumbar spine CT | cervical spine CT | thoracic spine CT | sacrum CT
```

## F2. MultiCaRe

Endpoint: `GET https://zenodo.org/api/records/10079370` for the record (licence, version,
files, sizes). The spine subset is counted from the local copy of `captions_and_labels.csv`
that FluoroCap already holds on the grid (no new download): captions matching `SPINE_RE` and
`MODALITY_RE`, split into radiograph vs CT by the modality label and caption. If the local copy
is absent, the subset is recorded `unknown` and only the record metadata is charted.

## F3. Open-PMC-18M

Endpoint: `GET https://huggingface.co/api/datasets/vector-institute/open-pmc-18m` for the
record; subset counted over the shards present locally from FluoroCap (sub-caption matching
`SPINE_RE`, modality label or caption matching `MODALITY_RE`); absent shards → `unknown`.

## F4. Wikimedia Commons

Endpoint: `GET https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<q>&srnamespace=6&srlimit=500&sroffset=<i>&format=json&maxlag=5`; each hit's `extmetadata` (licence, description) via `prop=imageinfo&iiprop=extmetadata`. The Action API is the interface Wikimedia's API etiquette directs contributors to; the host's `robots.txt` disallows `/w/` for crawlers, and the manuscript states the decision to use the documented API at one request per second with `maxlag`. Queries:
```
spine radiograph | spine x-ray | vertebra radiograph | lumbar spine x-ray | cervical spine x-ray | thoracic spine x-ray | scoliosis x-ray | spine fluoroscopy | vertebral fracture x-ray | spine CT | vertebra CT | lumbar spine CT | incategory:"X-rays of the human spine" | incategory:"CT scans of the human spine" | incategory:"Radiographs of scoliosis"
```
(`incategory:` names are verified on the first run against the category tree and corrected in
the deviations log if a category is misnamed.)

## F5. J-STAGE

Endpoint: `GET https://api.jstage.jst.go.jp/searchapi/do?service=3&text=<q>&pubyearfrom=2000&pubyearto=2026&count=1000&start=<i>` (XML). Queries in Japanese and English:
```
脊椎 CT データセット | 椎体 データベース | 脊椎 X線 データセット | 側弯症 X線 データベース | 腰椎 CT 公開 | 脊椎 画像 データセット | spine CT dataset | spine radiograph dataset | vertebra database
```

## F6. KoreaMed Synapse

Endpoint (HTML): `GET https://synapse.koreamed.org/search?q=<q>&page=<n>`; fallback
`GET https://koreamed.org/search/basic.php?Query=<q>`. Parsed for article links and titles;
abstracts fetched once per hit. Queries:
```
척추 CT 데이터셋 | 척추 X선 데이터베이스 | 요추 방사선 데이터 | 척추측만증 방사선 데이터셋 | 척추 영상 데이터베이스 | spine CT dataset | spine radiograph dataset
```

## F7. SciELO

Endpoint (HTML): `GET https://search.scielo.org/?q=<q>&lang=en&output=site&format=summary&count=50&from=<i>` (the same call FluoroCap uses, which needs a browser-like client; logged as `html`). Queries in Portuguese, Spanish and English:
```
coluna vertebral tomografia banco de dados | radiografia coluna base de dados | escoliose radiografia dataset | columna vertebral tomografía base de datos | radiografía columna base de datos | escoliosis radiografía conjunto de datos | spine CT dataset | spine radiograph dataset
```

## F8. Redalyc

Endpoint (HTML): `GET https://www.redalyc.org/busquedaArticuloFiltros.oa?q=<q>`. Same queries
as F7 (Spanish and Portuguese sets).

---

## Recording format (every source)

One line per request in `runs/<run-date>/requests.log.jsonl`:
`{"ts","source","query_id","url","params","status","elapsed_ms","sha1","credential":"<name|none>","note"}`.
One line per retrieved record in `records.jsonl`: `{"record_id","source","query_id","retrieved_at","ids":{doi,pmid,pmcid,arxiv,url},"title","abstract_or_description","year","type","raw_sha1"}`.
Per source in `counts.json`: `{"source","query_id","query","endpoint","date","reported_total","retrieved","cap_reached","credential","status"}`.
