# Information sources: endpoints, limits, and verbatim query strings

Protocol 1.0, 2026-09-19. Every source is queried by `sdr/search.py --source <name>`; the
strings below are what the adapter sends, rendered from the three term sets in `sdr/terms.py`.
Where a source's grammar cannot express the full boolean, the adapter issues a grid of simpler
requests and the appendix reports every one with its hit count. Facts marked (verify) are
documented behaviours that will be confirmed on the first run and recorded in `queries.json`;
if a source behaves differently, the deviations log says so.

Shared conventions for every request: User-Agent `spine-data-review/1.0 (mailto:<contact>)`;
20 s connect/read timeout; retry on 429, 500, 502, 503, 504 with exponential backoff (1, 2, 4,
8, 16 s, then give up and log); `Retry-After` honoured when present; every attempt logged;
every body cached (PROTOCOL section 6). Rate limits below are the ceilings the adapter enforces
with a token bucket per source; they are at or under each provider's published limit.

## Term sets

```
SPINE    = spine, spinal, vertebra, vertebrae, vertebral, lumbar, thoracic, cervical, lumbosacral,
           sacrum, sacral, scoliosis, spondylolisthesis, "vertebral fracture"
MODALITY = CT, "computed tomography", tomography, radiograph, radiographs, radiography, "x-ray",
           "x ray", xray, roentgen, fluoroscopy, fluoroscopic, "C-arm", "image intensifier",
           DXA, DEXA, absorptiometry, "vertebral fracture assessment", EOS, biplanar,
           "plain film", "cone-beam"
DATASET  = dataset, datasets, "data set", database, benchmark, challenge, corpus, collection,
           "publicly available", "open access", "open-access", "open source", "data descriptor",
           annotated
```

Reasoning is in PROTOCOL section 5. For sources without OR, the adapter uses the reduced sets
`SPINE_R = spine, vertebra, vertebral, lumbar, thoracic, cervical, scoliosis`,
`MODALITY_R = CT, radiograph, x-ray, fluoroscopy, DXA`, `DATASET_R = dataset, database,
benchmark, challenge`, so that the grid stays at 7 × 5 × 4 = 140 requests per source; the
reduction is recorded in `queries.json` as `grammar: grid` with the sets used.

## Summary table

| Source | Endpoint | Auth | Rate limit enforced | Query grammar | What it indexes | Paging and cap |
|---|---|---|---|---|---|---|
| PubMed | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`, `efetch.fcgi` | `NCBI_API_KEY` optional | 10/s with key, 3/s without (NCBI policy) | Field tags `[tiab] [mh] [ti] [pt] [dp] [ta]`, AND/OR/NOT, parentheses, `*` truncation (≥ 4 chars), phrases in quotes | MEDLINE + PubMed in-process; title/abstract/MeSH, no full text | `retmax` ≤ 10,000 per esearch; beyond that `usehistory=y` + efetch `retstart` in batches of 500; esearch `retstart` cannot exceed 9,999, so > 10,000 hits are split by `[dp]` year ranges (verify count first) |
| Europe PMC | `https://www.ebi.ac.uk/europepmc/webservices/rest/search` | none | 2/s (polite; no published hard limit) | Fielded Lucene-style: `TITLE:`, `ABSTRACT:`, `KW:`, `PUB_YEAR:[a TO b]`, `SRC:`, `HAS_FT:y`, `OPEN_ACCESS:y`, `HAS_DATA:y`, AND/OR/NOT, `*` | PubMed + PMC + preprints (`SRC:PPR` from bioRxiv, medRxiv, arXiv subset, Research Square, others) + Agricola + patents | `cursorMark=*` deep paging, `pageSize` ≤ 1000, no cap |
| OpenAlex | `https://api.openalex.org/works` | none; `mailto=` for polite pool | 10/s, 100,000/day (polite pool) | `filter=title_and_abstract.search:(...)` with AND/OR/NOT and quoted phrases, no wildcards (stemmed); `filter=publication_year:2000-2026`, `type:` | 250M+ works incl. Crossref, PubMed, DataCite (`type:dataset`), repositories; abstracts as inverted index | `cursor=*`, `per-page` ≤ 200, no cap |
| Semantic Scholar | `https://api.semanticscholar.org/graph/v1/paper/search/bulk` | `S2_API_KEY` (header `x-api-key`); unkeyed shares a pool and is refused under load | 1/s with key | Bulk syntax: `+` AND, `\|` OR, `-` NOT, `"phrase"`, `*` prefix, parentheses; matches title + abstract; params `year=2000-2026`, `fieldsOfStudy`, `publicationTypes`, `openAccessPdf` | ~220M papers (S2 corpus: publisher feeds, arXiv, PubMed, web) | continuation `token`, 1000 per page, up to 10M; `/paper/search` (non-bulk) is capped at offset+limit ≤ 1000 and is NOT used |
| arXiv | `http://export.arxiv.org/api/query` | none | 1 request per 3 s (arXiv policy) | `search_query=` with `ti:`, `abs:`, `all:`, `cat:`, `submittedDate:[a TO b]`; AND/OR/ANDNOT; phrases as `%22..%22`; no wildcards | arXiv preprints (cs.CV, eess.IV, physics.med-ph carry the datasets) | `start` + `max_results` ≤ 2000 per call; total addressable ≤ 30,000 (verify); Atom XML |
| bioRxiv / medRxiv | `https://api.biorxiv.org/details/{biorxiv\|medrxiv}/{from}/{to}/{cursor}/json` | none | 2/s | NO search: date-interval dumps of 100 records; filtered locally by the SPINE/MODALITY/DATASET regexes on title + abstract (regex recorded) | all bioRxiv (2013–) and medRxiv (2019–) preprints with category | cursor step 100; a full enumeration is roughly 4,000 requests, done once and cached; monthly intervals |
| Crossref | `https://api.crossref.org/works` | none; `mailto=` for polite pool | 2/s (polite pool asks for < 50/s; we stay far below) | `query.bibliographic=` free text, NO boolean, relevance-ranked; `filter=type:dataset,from-pub-date:,until-pub-date:,has-abstract:true`; `select=` fields | DOIs registered with Crossref: articles, and datasets registered by publishers (not DataCite datasets) | `cursor=*`, `rows` ≤ 1000; for ranked free-text we cap at 5,000 per string and record it |
| Zenodo | `https://zenodo.org/api/records` | none for public | 1/s (guest policy is 60/min, 2000/h) | Elasticsearch: `title:`, `description:`, `keywords:`, `metadata.resource_type.id:`, `metadata.publication_date:[a TO b]`, AND/OR/NOT, `*` | all Zenodo records with files, licence, checksums (`files[].checksum` = `md5:...`), `access_right` | `page`/`size` ≤ 100; page × size ≤ 10,000 → split by year when exceeded |
| Figshare | `POST https://api.figshare.com/v2/articles/search` | none for public | 2/s | JSON body `search_for` with `:title:`, `:description:`, `:keyword:` prefixes, AND/OR/NOT, quotes; `item_type` (3 = dataset, 1 = figure); `published_since`/`published_until` | figshare.com and institutional Figshare portals; files with `computed_md5`, `size` via `/articles/{id}/files` | `page_size` ≤ 1000, `page` (verify the deep-paging cap; use `offset`/`limit` if `page` stops) |
| Dryad | `https://datadryad.org/api/v2/search` | none | 2/s | `q=` free text, no boolean guaranteed → grid | Dryad datasets (CC0), files with digests via `/versions/{id}/files` | `page`, `per_page` ≤ 100 |
| OSF | `https://api.osf.io/v2/nodes/`, `/v2/registrations/` | none; `OSF_TOKEN` optional | anonymous throttle 100/h documented (verify); with token 10,000/h | JSON:API filters `filter[title]=` (contains, case-insensitive), `filter[tags]=`, `filter[public]=true`; no full-text → grid over SPINE_R on title, local screen on description | OSF projects and registrations; DOIs 10.17605 (also in DataCite) | `page[size]` ≤ 100, `page=` |
| Mendeley Data | `https://api.data.mendeley.com/datasets` (documented; requires OAuth client credentials) | not present → `needs-credentials` | — | — | Mendeley Data (DOI prefix 10.17632) | Credential-free behaviour: covered by DataCite with `prefix=10.17632` (below), logged as `mendeley-via-datacite` |
| DataCite | `https://api.datacite.org/dois` | none | 2/s | Lucene: `titles.title:`, `descriptions.description:`, `subjects.subject:`, `publicationYear:[a TO b]`, `types.resourceTypeGeneral:`, AND/OR/NOT, `*`; params `resource-type-id=`, `prefix=`, `client-id=` | every DataCite DOI: Zenodo (10.5281), Figshare (10.6084), Dryad (10.5061), OSF (10.17605), Mendeley (10.17632), PhysioNet (10.13026), TCIA (10.7937), institutional repositories | `page[cursor]=1` then `links.next`, `page[size]` ≤ 1000, no cap |
| PhysioNet | `https://physionet.org/rest/database-list/` (JSON), `https://physionet.org/content/{slug}/` | none | 1/s | NO search: full published-database list, filtered locally by regex on title (+ abstract when the list carries it, else from the content page) | PhysioNet databases with access policy (open / credentialed / restricted) | single response; one content-page request per regex hit |
| TCIA / NBIA | `https://services.cancerimagingarchive.net/nbia-api/services/v1/getCollectionValues`, `getBodyPartValues?Collection=`, `getModalityValues?Collection=`, `getPatientByCollectionAndModality`, `getSeries` | none for public collections; restricted ones need an NBIA token (not used) | 2/s | NO free text: enumerate collections, keep those whose BodyPartExamined matches `SPINE\|LSPINE\|TSPINE\|CSPINE\|LUMBAR\|THORACIC\|CERVICAL\|SACRUM\|PELVIS` and modality in `CT\|CR\|DX\|RF\|XA`; subject counts from `getPatientByCollectionAndModality` | TCIA collections (mostly oncology; spine appears as body part in whole-body CT) | unpaged JSON lists |
| Kaggle | `https://www.kaggle.com/api/v1/datasets/list?search=&page=` | `~/.kaggle/kaggle.json` (HTTP basic) REQUIRED | 1/s | `search=` free text → grid over SPINE_R × MODALITY_R | Kaggle datasets (licence field present) | 20 per page, iterate until empty (practical cap ≈ 500 per string); without credentials: `needs-credentials`, plus `kaggle.com/datasets/<owner>/<slug>` URLs regex-harvested from all other sources' abstracts and READMEs (source `kaggle-mention`) |
| Hugging Face Hub | `https://huggingface.co/api/datasets?search=&limit=100&full=true`; `/api/datasets/{id}?blobs=true` | none; `HF_TOKEN` optional (higher limit) | 2/s | `search=` substring on repo id only (NOT the card text) → grid over SPINE_R and common compounds (`spine`, `vertebra`, `verse`, `scoliosis`, `lumbar`, `xray-spine`, `spine-ct`); `filter=` on tags | HF datasets with `cardData.license`, `gated`, `private`, `siblings` (LFS sha256 + size with `blobs=true`) | `Link: rel="next"` cursor; no cap. Card-text coverage gap is supplemented by `huggingface.co/datasets/…` URL regex over other sources (source `hf-mention`) |
| grand-challenge.org | `https://grand-challenge.org/api/v1/challenges/` (verify: anonymous access) | none tried; token not held | 1/s | none; list filtered locally by regex on title + description | challenges with their data pages | `limit`/`offset`; if the API answers 401/403, fall back to the public HTML list `https://grand-challenge.org/challenges/all-challenges/` parsed by regex, logged as `html-fallback` |
| GitHub | `https://api.github.com/search/repositories`; `/search/code` | none for repos (10/min); `GITHUB_TOKEN` optional (30/min); code search REQUIRES token | 1 per 6 s unauth; 1 per 2 s with token | qualifiers `in:name,description,readme`, `topic:`, `created:>=2000-01-01`, `fork:false`; phrases in quotes; implicit AND | repositories (README text indexed) | 100 per page, 1000 results per query cap → grid of narrower strings; code search `needs-credentials` without token |
| Papers with Code | `https://paperswithcode.com/api/v1/datasets/?q=&items_per_page=500` (site retired 2025; verify) | none | 1/s | `q=` free text | PwC dataset index (historical) | if 404/redirect: fetch the static dump `https://production-media.paperswithcode.com/about/datasets.json.gz` (metadata only, ~tens of MB, not an imaging dataset) and filter locally; if that too is gone, record `retired` with the status and date |
| OpenDataLab | `https://opendatalab.com/api/v2/datasets/search` (undocumented; verify) | none tried | 1/s | `keyword=` | OpenDataLab catalogue (many CN mirrors of public sets) | probe two candidate endpoints recorded in the log; on failure `no-public-api`; the `openxlab` CLI needs a key → `needs-credentials` |
| NLM Open-i | `https://openi.nlm.nih.gov/api/search?query=&it=xg&m=&n=` | none | 1/s | free text; `it=xg` (x-ray graphics), `coll=pmc`; no boolean → grid | PMC OA figures with captions, plus some radiology collections | `m`/`n` window of 30 (as in `tools/fluorocap_openi.py`); total from `total`; this route finds articles whose caption, not abstract, names a dataset |
| MultiCaRe | `https://zenodo.org/api/records/10079370` | none | — | record metadata only (files, sizes, md5, licence) | itself a figure-derived dataset; the spine-radiograph sub-figure count is taken from the FluoroCap run's `stats.json` on disk (path recorded), not by re-downloading captions | single request |
| Open-PMC-18M | `https://huggingface.co/api/datasets/vector-institute/open-pmc-18m?blobs=true`; `https://datasets-server.huggingface.co/search?dataset=vector-institute/open-pmc-18m&config=&split=&query=&offset=&length=100` (verify that the search index exists) | none | 2/s | datasets-server full-text over caption columns; free text → grid | itself a figure-derived dataset; sub-figure counts per query recorded; FluoroCap's shard/key counts cited from disk | `offset`/`length` ≤ 100 |
| Wikimedia Commons | `https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srlimit=50&sroffset=`; `prop=imageinfo&iiprop=url\|size\|mime\|sha1\|extmetadata` | none | 2/s | CirrusSearch: implicit AND, `-` NOT, `intitle:`, `incategory:`, `filetype:bitmap`, `deepcat:`; no reliable OR → grid; plus `list=categorymembers` on `Category:X-rays of the human spine`, `Category:CT images of the spine` (verify names) | files with licence and description in `extmetadata` | `sroffset` ≤ 10,000; `cmcontinue` |
| J-STAGE | `https://api.jstage.jst.go.jp/searchapi/do?service=3` | none | 1/s | params `article=` (title), `abst=`, `text=`, `keyword=`, `pubyearfrom=2000&pubyearto=2026`; space = AND; no documented OR → grid, in English and Japanese (`脊椎`, `椎体`, `腰椎`, `胸椎`, `頸椎`, `CT`, `X線`, `データセット`, `データベース`) | Japanese journals (Atom XML) | `start`, `count` ≤ 1000 |
| KoreaMed / Synapse | `https://koreamed.org/search?searchWord=&pageNumber=` (HTML; no documented JSON API) | none | 1/s | free text → grid; results parsed by regex; logged `html-fallback` | Korean medical journals (largely also in PubMed/PMC, so this is a coverage check) | page number until empty |
| SciELO | `https://search.scielo.org/?q=&lang=en&count=100&from=&output=xml` (verify that `output=xml` is served; else HTML parse, `html-fallback`) | none | 1/s | free text with AND/OR in `q` (verify) → grid in English, Spanish, Portuguese (`columna vertebral`, `vértebra`, `coluna vertebral`, `radiografía`, `radiografia`, `tomografía`, `tomografia`, `base de datos`, `conjunto de datos`, `banco de dados`) | Latin-American and Iberian journals (also in Crossref/OpenAlex; coverage check) | `count` ≤ 100, `from` |
| Redalyc | no documented search API; probe the site's JSON search endpoint used by its front end (URL recorded at run) | none | 1/s | free text → grid, Spanish/Portuguese/English | Latin-American journals | if no JSON endpoint answers, `no-public-api`; coverage relies on OpenAlex/Crossref, and the log says so |
| Springer Nature Meta (supplementary) | `https://api.springernature.com/meta/v2/json?q=&api_key=&s=&p=` | `SPRINGER_API_META_KEY` present | 1/s (free tier 5,000/day) | `q=` with `journalid:`, `title:`, `keyword:`, `year:`, AND/OR, quotes | Springer Nature journals; used for the Scientific Data (journalid 41597) and Data in Brief-equivalent venue sweep | `p` ≤ 100 (verify), `s` offset |
| Unpaywall (supplementary) | `https://api.unpaywall.org/v2/{doi}?email=` | `UNPAYWALL_EMAIL` | 2/s | by DOI only | OA location of a source article, for full-text charting only | one request per DOI needing full text |

Excluded sources and reasons (reported in Methods): Google Dataset Search (no API; the terms of
service forbid automated querying); YouTube, Instagram, Reddit, Flickr, Facebook (video and
social media are image sources for FluoroCap but do not host subject-level medical-image
datasets with a stable record, and cannot be screened by title/abstract); Common Crawl (raw
web text, not a dataset index; any dataset it would find is indexed by at least one source
above); patents (drawings, not datasets; no subject-level images).

## Verbatim query strings

Each block is what the adapter sends after URL-encoding. `query_id` values are the keys in
`queries.json`. Dates and hit counts are filled by the run, never by hand.

### PubMed — query_id `pubmed.main`

```
(spine[tiab] OR spinal[tiab] OR vertebra*[tiab] OR lumbar[tiab] OR thoracic[tiab] OR cervical[tiab]
 OR lumbosacral[tiab] OR sacrum[tiab] OR sacral[tiab] OR scoliosis[tiab] OR spondylolisthesis[tiab]
 OR "vertebral fracture"[tiab] OR "vertebral fractures"[tiab]
 OR Spine[mh] OR "Spinal Diseases"[mh] OR "Spinal Injuries"[mh] OR "Spinal Curvatures"[mh])
AND
("computed tomography"[tiab] OR CT[tiab] OR tomograph*[tiab] OR radiograph*[tiab] OR "x-ray"[tiab]
 OR "x ray"[tiab] OR xray*[tiab] OR roentgen*[tiab] OR fluoroscop*[tiab] OR "C-arm"[tiab]
 OR "image intensifier"[tiab] OR DXA[tiab] OR DEXA[tiab] OR absorptiometry[tiab]
 OR "vertebral fracture assessment"[tiab] OR EOS[tiab] OR biplanar[tiab] OR "plain film*"[tiab]
 OR "cone-beam"[tiab] OR "cone beam"[tiab]
 OR "Tomography, X-Ray Computed"[mh] OR Radiography[mh] OR Fluoroscopy[mh] OR "Absorptiometry, Photon"[mh])
AND
(dataset[tiab] OR datasets[tiab] OR "data set"[tiab] OR "data sets"[tiab] OR database[tiab]
 OR databases[tiab] OR benchmark*[tiab] OR challenge[tiab] OR corpus[tiab] OR "publicly available"[tiab]
 OR "open access"[tiab] OR "open-access"[tiab] OR "open source"[tiab] OR "data descriptor"[tiab]
 OR annotated[tiab] OR "Datasets as Topic"[mh] OR "Databases, Factual"[mh])
AND ("2000/01/01"[dp] : "2026/12/31"[dp])
```
Parameters: `db=pubmed&retmode=json&usehistory=y&retmax=0` to get the count and WebEnv, then
`efetch.fcgi?db=pubmed&query_key=&WebEnv=&retstart=&retmax=500&retmode=xml`. Records: PMID,
DOI, PMCID, title, abstract, MeSH, publication types, journal, year. If the count exceeds
10,000 the query is split into `[dp]` ranges 2000–2015, 2016–2020, 2021–2023, 2024–2026 and
each is its own query_id (`pubmed.main.<range>`).

Reasoning: MeSH terms recover records with sparse abstracts; `[tiab]` keeps the string
portable to Europe PMC; `annotated` is included because segmentation datasets often say
"annotated CT scans" without the word dataset in the abstract; `EOS` and `CT` are ambiguous
alone but only fire inside the SPINE conjunction.

### PubMed — query_id `pubmed.venues`

```
("Sci Data"[ta] OR "Data Brief"[ta] OR "Med Phys"[ta] OR "Radiol Artif Intell"[ta] OR "J Digit Imaging"[ta]
 OR "J Imaging Inform Med"[ta] OR "Comput Methods Programs Biomed"[ta] OR "Med Image Anal"[ta])
AND (spine[tiab] OR spinal[tiab] OR vertebra*[tiab] OR lumbar[tiab] OR thoracic[tiab] OR scoliosis[tiab])
AND ("2000/01/01"[dp] : "2026/12/31"[dp])
```
Reasoning: dataset descriptors in these venues sometimes omit the modality word from the
abstract ("annotated spine images"); the venue sweep drops the MODALITY and DATASET
conjunctions and lets screening do the work.

### Europe PMC — query_id `epmc.main`

```
((TITLE:spine OR TITLE:spinal OR TITLE:vertebra* OR TITLE:lumbar OR TITLE:thoracic OR TITLE:cervical
  OR TITLE:lumbosacral OR TITLE:sacrum OR TITLE:sacral OR TITLE:scoliosis OR TITLE:spondylolisthesis
  OR TITLE:"vertebral fracture" OR ABSTRACT:spine OR ABSTRACT:spinal OR ABSTRACT:vertebra*
  OR ABSTRACT:lumbar OR ABSTRACT:thoracic OR ABSTRACT:lumbosacral OR ABSTRACT:sacrum
  OR ABSTRACT:scoliosis OR ABSTRACT:spondylolisthesis OR ABSTRACT:"vertebral fracture")
 AND
 (TITLE:"computed tomography" OR TITLE:CT OR TITLE:tomograph* OR TITLE:radiograph* OR TITLE:"x-ray"
  OR TITLE:xray* OR TITLE:fluoroscop* OR TITLE:"C-arm" OR TITLE:DXA OR TITLE:DEXA OR TITLE:EOS
  OR TITLE:biplanar OR ABSTRACT:"computed tomography" OR ABSTRACT:CT OR ABSTRACT:tomograph*
  OR ABSTRACT:radiograph* OR ABSTRACT:"x-ray" OR ABSTRACT:"x ray" OR ABSTRACT:xray*
  OR ABSTRACT:roentgen* OR ABSTRACT:fluoroscop* OR ABSTRACT:"C-arm" OR ABSTRACT:"image intensifier"
  OR ABSTRACT:DXA OR ABSTRACT:DEXA OR ABSTRACT:absorptiometry OR ABSTRACT:"vertebral fracture assessment"
  OR ABSTRACT:EOS OR ABSTRACT:biplanar OR ABSTRACT:"plain film*" OR ABSTRACT:"cone-beam")
 AND
 (TITLE:dataset* OR TITLE:"data set" OR TITLE:database* OR TITLE:benchmark* OR TITLE:challenge
  OR TITLE:corpus OR ABSTRACT:dataset* OR ABSTRACT:"data set*" OR ABSTRACT:database*
  OR ABSTRACT:benchmark* OR ABSTRACT:challenge OR ABSTRACT:corpus OR ABSTRACT:"publicly available"
  OR ABSTRACT:"open access" OR ABSTRACT:"open-access" OR ABSTRACT:"open source"
  OR ABSTRACT:"data descriptor" OR ABSTRACT:annotated))
AND (PUB_YEAR:[2000 TO 2026]) AND (SRC:MED OR SRC:PMC OR SRC:PPR)
```
Parameters: `format=json&resultType=lite&pageSize=1000&cursorMark=*`, then `nextCursorMark`.
`resultType=core` is requested only for records that reach charting (abstract, grants,
`fullTextUrlList`). Reasoning: `SRC:PPR` is the only place bioRxiv/medRxiv are searchable by
field, which is why the bioRxiv API route is a dump-and-filter rather than the primary
preprint search. The Open-i, MultiCaRe and Open-PMC-18M routes reach the same PMC OA subset
through captions rather than abstracts.

### Europe PMC — query_id `epmc.data_links`

```
(TITLE:spine OR TITLE:vertebra* OR TITLE:lumbar OR TITLE:thoracic OR TITLE:scoliosis
 OR ABSTRACT:vertebra* OR ABSTRACT:"spine")
AND (HAS_DATA:y) AND (PUB_YEAR:[2000 TO 2026])
```
Reasoning: `HAS_DATA:y` marks articles with linked data records (via Europe PMC's data
links); this catches descriptors whose abstract has no DATASET term.

### OpenAlex — query_id `openalex.works`

```
GET https://api.openalex.org/works
  ?filter=title_and_abstract.search:((spine OR spinal OR vertebra OR vertebrae OR vertebral OR lumbar OR thoracic OR cervical OR lumbosacral OR sacrum OR scoliosis OR spondylolisthesis OR "vertebral fracture") AND (CT OR "computed tomography" OR tomography OR radiograph OR radiographs OR radiography OR "x-ray" OR "x ray" OR xray OR roentgen OR fluoroscopy OR fluoroscopic OR "C-arm" OR "image intensifier" OR DXA OR DEXA OR absorptiometry OR EOS OR biplanar OR "plain film" OR "cone-beam") AND (dataset OR datasets OR "data set" OR database OR benchmark OR challenge OR corpus OR "publicly available" OR "open access" OR "open-access" OR "open source" OR "data descriptor" OR annotated)),publication_year:2000-2026
  &per-page=200&cursor=*&mailto=<redacted>
  &select=id,doi,ids,title,display_name,publication_year,type,primary_location,open_access,abstract_inverted_index,referenced_works,cited_by_count,authorships
```
Reasoning: OpenAlex stems, so singular/plural variants are redundant but harmless; no
wildcard exists, so `fluoroscop*` becomes two words. The abstract is reconstructed from the
inverted index by the adapter and stored in the record. Also `openalex.datasets`:

```
  ?filter=type:dataset,title_and_abstract.search:(spine OR spinal OR vertebra OR vertebrae OR vertebral OR lumbar OR thoracic OR lumbosacral OR sacrum OR scoliosis),publication_year:2000-2026
```
Reasoning: dataset-typed works come from DataCite and repositories where the MODALITY term is
often only in the file names; the reduced string is screened locally.

Citation chasing (`openalex.chase`): for every included source record with an OpenAlex id,
`GET /works?filter=cites:<id>&per-page=200` and the `referenced_works` list of the record;
one hop; results flagged `source=chase`.

### Semantic Scholar bulk — query_id `s2.bulk`

```
GET https://api.semanticscholar.org/graph/v1/paper/search/bulk
  ?query=(spine | spinal | vertebra* | lumbar | thoracic | cervical | lumbosacral | sacrum | sacral | scoliosis | spondylolisthesis | "vertebral fracture") + ("computed tomography" | CT | tomograph* | radiograph* | "x-ray" | "x ray" | xray* | roentgen* | fluoroscop* | "C-arm" | "image intensifier" | DXA | DEXA | absorptiometry | EOS | biplanar | "plain film" | "cone-beam") + (dataset* | "data set" | database* | benchmark* | challenge | corpus | "publicly available" | "open access" | "open-access" | "open source" | "data descriptor" | annotated)
  &year=2000-2026
  &fields=paperId,externalIds,title,abstract,year,venue,publicationTypes,isOpenAccess,openAccessPdf,citationCount,authors
```
Header `x-api-key: <redacted>`; page by `token` until absent. Reasoning: the same string as
`tools/fluorocap_s2.py` uses in form; `fieldsOfStudy` is NOT restricted to Medicine here
because computer-science venues are where challenge datasets appear. Without the key the
adapter tries the unkeyed endpoint at 1 per 5 s and records `credential-free` with whatever it
returns.

### arXiv — query_id `arxiv.main`

```
GET http://export.arxiv.org/api/query
  ?search_query=(abs:spine OR abs:spinal OR abs:vertebra OR abs:vertebrae OR abs:vertebral OR abs:lumbar OR abs:thoracic OR abs:cervical OR abs:lumbosacral OR abs:sacrum OR abs:scoliosis OR abs:spondylolisthesis OR ti:spine OR ti:vertebra OR ti:vertebrae OR ti:vertebral OR ti:scoliosis)
    AND (abs:CT OR abs:%22computed%20tomography%22 OR abs:tomography OR abs:radiograph OR abs:radiographs OR abs:radiography OR abs:%22x-ray%22 OR abs:xray OR abs:fluoroscopy OR abs:fluoroscopic OR abs:%22C-arm%22 OR abs:DXA OR abs:DEXA OR abs:EOS OR abs:biplanar OR abs:%22cone-beam%22)
    AND (abs:dataset OR abs:datasets OR abs:%22data%20set%22 OR abs:database OR abs:benchmark OR abs:challenge OR abs:corpus OR abs:%22publicly%20available%22 OR abs:%22open%20access%22 OR abs:annotated)
    AND submittedDate:[200001010000 TO 202612312359]
  &start=0&max_results=500&sortBy=submittedDate&sortOrder=ascending
```
Reasoning: `sortBy=submittedDate` makes paging stable; `max_results=500` keeps each Atom
response under the size at which arXiv truncates. No wildcards, so forms are enumerated.

### bioRxiv and medRxiv — query_ids `biorxiv.dump`, `medrxiv.dump`

```
GET https://api.biorxiv.org/details/medrxiv/2019-06-01/2019-06-30/0/json     (then cursor 100, 200, ...)
GET https://api.biorxiv.org/details/biorxiv/2013-11-01/2013-11-30/0/json
```
Monthly intervals to 2026-12-31. Local filter (recorded in `sdr/terms.py` as `SPINE_RE`,
`MODALITY_RE`, `DATASET_RE`, case-insensitive, word-bounded, applied to title + abstract; all
three must match). The unfiltered per-month totals are recorded so the filter's selectivity is
reportable. Reasoning: there is no query endpoint; Europe PMC `SRC:PPR` is the fielded route
and this dump is the completeness check for it.

### Crossref — query_ids `crossref.datasets.<i>`, `crossref.articles.<i>`

```
GET https://api.crossref.org/works
  ?query.bibliographic=spine vertebra vertebral radiograph x-ray CT dataset
  &filter=type:dataset,from-pub-date:2000-01-01,until-pub-date:2026-12-31
  &rows=1000&cursor=*&mailto=<redacted>
  &select=DOI,title,abstract,type,container-title,publisher,issued,URL,license,relation,subject
```
Strings (no boolean, relevance-ranked): `i` ranges over the seven SPINE_R terms, each
concatenated with `radiograph x-ray CT dataset`, and each with `fluoroscopy DXA database
benchmark`, giving 14 dataset-typed queries; `crossref.articles.<i>` repeats them with
`type:journal-article,has-abstract:true` capped at 5,000 rows each (cap recorded).
Reasoning: Crossref's free-text search cannot express the conjunction, so the strings are
short and the cap is explicit; Crossref's main use is DOI metadata and `relation` links
(is-supplement-to) for merging.

### Zenodo — query_id `zenodo.main`

```
GET https://zenodo.org/api/records
  ?q=((title:(spine OR spinal OR vertebra* OR lumbar OR thoracic OR cervical OR lumbosacral OR sacrum OR scoliosis OR spondylolisthesis) OR description:(spine OR spinal OR vertebra* OR lumbar OR thoracic OR lumbosacral OR sacrum OR scoliosis OR spondylolisthesis) OR keywords:(spine OR vertebra* OR scoliosis))
       AND (title:(CT OR tomograph* OR radiograph* OR "x-ray" OR xray OR fluoroscop* OR "C-arm" OR DXA OR DEXA OR EOS OR biplanar OR "cone-beam") OR description:(CT OR "computed tomography" OR tomograph* OR radiograph* OR "x-ray" OR "x ray" OR xray OR roentgen* OR fluoroscop* OR "C-arm" OR "image intensifier" OR DXA OR DEXA OR absorptiometry OR EOS OR biplanar OR "plain film" OR "cone-beam") OR keywords:(CT OR radiograph* OR "x-ray" OR fluoroscop* OR DXA))
       AND (metadata.resource_type.id:dataset OR metadata.resource_type.id:image* OR metadata.resource_type.id:software OR metadata.resource_type.id:other)
       AND metadata.publication_date:[2000-01-01 TO 2026-12-31])
  &size=100&page=1&sort=bestmatch
```
Reasoning: no DATASET term because the resource-type clause does that job; `software` is
included because dataset-plus-code releases are typed software. If `hits.total` exceeds
10,000 the year range is split. Legacy `type=dataset` parameter is tried if the resource-type
clause returns zero (recorded). Enrichment per hit: `files[].checksum`, `files[].size`,
`metadata.license.id`, `metadata.access_right`, `metadata.related_identifiers`, `conceptdoi`.

### Figshare — query_id `figshare.main`

```
POST https://api.figshare.com/v2/articles/search
{"search_for": "(:title: spine OR :title: spinal OR :title: vertebra OR :title: vertebrae OR :title: vertebral OR :title: lumbar OR :title: thoracic OR :title: scoliosis OR :description: vertebra OR :description: vertebrae OR :description: vertebral OR :description: lumbar spine OR :description: thoracic spine OR :description: cervical spine) AND (:title: CT OR :title: tomography OR :title: radiograph OR :title: radiographs OR :title: x-ray OR :title: xray OR :title: fluoroscopy OR :title: DXA OR :description: computed tomography OR :description: radiograph OR :description: radiographs OR :description: x-ray OR :description: fluoroscopy OR :description: DXA OR :description: EOS OR :description: biplanar)",
 "item_type": 3, "page_size": 1000, "page": 1, "order": "published_date", "order_direction": "asc",
 "published_since": "2000-01-01", "published_until": "2026-12-31"}
```
Repeated with `item_type` omitted (all types) as `figshare.alltypes`; the difference is
reported. Enrichment: `/v2/articles/{id}` (licence, DOI, `is_embargoed`, `is_public`) and
`/v2/articles/{id}/files` (`computed_md5`, `size`, `download_url`).

### Dryad — query_ids `dryad.<spine>.<modality>`

```
GET https://datadryad.org/api/v2/search?q=vertebra%20radiograph&per_page=100&page=1
```
Grid SPINE_R × MODALITY_R (35 strings). Enrichment: `/api/v2/datasets/{doi}` and
`/versions/{id}/files` (`digest`, `digestType`, `size`).

### OSF — query_ids `osf.nodes.<spine>`, `osf.registrations.<spine>`

```
GET https://api.osf.io/v2/nodes/?filter[title]=vertebra&filter[public]=true&page[size]=100
GET https://api.osf.io/v2/registrations/?filter[title]=vertebra&page[size]=100
```
Grid over SPINE_R (seven strings each). Local screen on `description` + `tags` for a
MODALITY term. Token from `OSF_TOKEN` if set (`Authorization: Bearer`), else the anonymous
throttle applies and the run is paced to it.

### DataCite — query_ids `datacite.main`, `datacite.mendeley`, `datacite.<prefix>`

```
GET https://api.datacite.org/dois
  ?query=((titles.title:(spine OR spinal OR vertebra* OR lumbar OR thoracic OR cervical OR lumbosacral OR sacrum OR scoliosis OR spondylolisthesis) OR descriptions.description:(spine OR spinal OR vertebra* OR lumbar OR thoracic OR lumbosacral OR sacrum OR scoliosis) OR subjects.subject:(spine OR vertebra* OR scoliosis))
          AND (titles.title:(CT OR tomograph* OR radiograph* OR "x-ray" OR xray OR fluoroscop* OR "C-arm" OR DXA OR DEXA OR EOS OR biplanar OR "cone-beam") OR descriptions.description:(CT OR "computed tomography" OR tomograph* OR radiograph* OR "x-ray" OR xray OR roentgen* OR fluoroscop* OR "C-arm" OR DXA OR DEXA OR absorptiometry OR EOS OR biplanar OR "cone-beam") OR subjects.subject:(CT OR radiograph* OR "x-ray" OR tomography))
          AND publicationYear:[2000 TO 2026])
  &resource-type-id=dataset&page[size]=1000&page[cursor]=1
```
Repeated with `resource-type-id=image` and with no resource-type filter but
`types.resourceTypeGeneral:(Dataset OR Image OR Collection)` in the query (recorded
separately). `datacite.mendeley` adds `&prefix=10.17632` with the SPINE clause only (Mendeley
descriptions are short) and is the credential-free Mendeley Data route. Enrichment:
`relatedIdentifiers`, `rightsList`, `sizes`, `formats`, `version`, `container`.

### PhysioNet — query_id `physionet.list`

```
GET https://physionet.org/rest/database-list/
```
Filter locally: title matches `SPINE_RE`. For each hit, `GET https://physionet.org/content/{slug}/`
and read the access-policy string (`Open Access|Credentialed Access|Restricted Access`) by
regex, cached. The expected result is zero or near-zero spine datasets; that is reported as a
finding, not omitted.

### TCIA / NBIA — query_ids `tcia.collections`, `tcia.<collection>`

```
GET https://services.cancerimagingarchive.net/nbia-api/services/v1/getCollectionValues
GET .../v1/getBodyPartValues?Collection=<name>
GET .../v1/getModalityValues?Collection=<name>
GET .../v1/getPatientByCollectionAndModality?Collection=<name>&Modality=CT
```
Keep collections with a body part matching `SPINE|LSPINE|TSPINE|CSPINE|LUMBAR|THORACIC|CERVICAL|SACRUM|PELVIS|WHOLE ?BODY` and a modality in `CT|CR|DX|RF|XA`. Collection DOIs and licences via `https://www.cancerimagingarchive.net/api/v1/collections` if it answers (verify), else DataCite `prefix=10.7937`.

### Kaggle — query_ids `kaggle.<spine>.<modality>`

```
GET https://www.kaggle.com/api/v1/datasets/list?search=spine%20x-ray&page=1&sortBy=hottest
```
HTTP basic auth from `~/.kaggle/kaggle.json`; grid SPINE_R × MODALITY_R. Without the file:
`needs-credentials`, and `kaggle-mention` regex `kaggle\.com/datasets/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+`
over every other source's text fields.

### Hugging Face Hub — query_ids `hf.search.<term>`, `hf.mention`

```
GET https://huggingface.co/api/datasets?search=vertebra&limit=100&full=true
GET https://huggingface.co/api/datasets?search=spine&limit=100&full=true
GET https://huggingface.co/api/datasets?filter=medical&limit=100&full=true        (tag filter; screened locally)
GET https://huggingface.co/api/datasets/<id>?blobs=true                          (enrichment)
```
Terms: spine, spinal, vertebra, vertebrae, verse, scoliosis, lumbar, thoracic, cervical,
spondylolisthesis, xray-spine, spine-ct, spine-xray, lstv. `hf.mention` is the regex
`huggingface\.co/datasets/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+` over all other sources.
Enrichment fields: `cardData.license`, `gated`, `private`, `siblings[].lfs.sha256`,
`siblings[].size`, `lastModified`, `sha`.

### grand-challenge.org — query_id `gc.challenges`

```
GET https://grand-challenge.org/api/v1/challenges/?limit=100&offset=0
```
On 401/403: `GET https://grand-challenge.org/challenges/all-challenges/` and regex over the
HTML for challenge slugs and titles, logged `html-fallback`. Local filter: `SPINE_RE` on title +
description; challenge pages of hits fetched once for the data-access statement.

### GitHub — query_ids `github.repos.<i>`, `github.code.<i>`

```
GET https://api.github.com/search/repositories?q=vertebra+dataset+CT+in:name,description,readme+fork:false&per_page=100&page=1
GET https://api.github.com/search/repositories?q=spine+"x-ray"+dataset+in:name,description,readme+fork:false&per_page=100&page=1
GET https://api.github.com/search/repositories?q=topic:spine+topic:dataset&per_page=100
GET https://api.github.com/search/code?q=vertebra+dataset+filename:README.md      (token only)
```
Grid: SPINE_R × MODALITY_R with `dataset`, plus the topic queries `topic:spine`,
`topic:vertebrae`, `topic:scoliosis`, `topic:medical-imaging+spine`. Each string's 1000-result
cap is recorded when hit. `Accept: application/vnd.github+json`.

### Papers with Code — query_id `pwc.datasets`

```
GET https://paperswithcode.com/api/v1/datasets/?q=spine&items_per_page=500&page=1
```
Grid over SPINE_R. If the endpoint answers 404 or redirects off-site, the static dump is
fetched once, filtered locally (`name`, `full_name`, `description` against the regexes), and
the retirement is a deviations-log row.

### OpenDataLab — query_id `odl.search`

```
GET https://opendatalab.com/api/v2/datasets/search?keyword=spine&pageSize=100&pageNo=1     (candidate 1)
GET https://opendatalab.com/api/datasets?keywords=spine&pageSize=100                        (candidate 2)
```
Grid over SPINE_R; the first candidate that returns JSON is used; otherwise `no-public-api`.

### NLM Open-i — query_ids `openi.<i>`

```
GET https://openi.nlm.nih.gov/api/search?query=lumbar%20spine%20radiograph%20dataset&it=xg&m=1&n=30
```
Strings: for each SPINE_R term, `<term> radiograph dataset`, `<term> CT dataset`, `<term>
fluoroscopy`, `<term> "publicly available"`. Records: PMCID, article title, caption; the
article is merged by PMCID and screened as a literature record. Reasoning: Open-i finds
articles whose captions say "from the X dataset" while the abstract does not.

### MultiCaRe — query_id `multicare.record`

```
GET https://zenodo.org/api/records/10079370
```
The dataset is charted as a figure-derived collection (flag `figure-derived`); its
spine-radiograph sub-figure count is the FluoroCap run's `stats.json` value, with the path and
the file's sha1 recorded in the charting JSON (`field_sources.n_images_or_volumes =
"disk:<path>@<sha1>"`).

### Open-PMC-18M — query_ids `openpmc.record`, `openpmc.search.<i>`

```
GET https://huggingface.co/api/datasets/vector-institute/open-pmc-18m?blobs=true
GET https://datasets-server.huggingface.co/search?dataset=vector-institute/open-pmc-18m&config=default&split=train&query=lumbar%20spine%20radiograph&offset=0&length=100
```
Grid over SPINE_R × {radiograph, CT, fluoroscopy}. If datasets-server has no search index for
the dataset (HTTP 404 or an error body), the counts come from the FluoroCap run on disk as
above and the log records the fallback.

### Wikimedia Commons — query_ids `commons.search.<i>`, `commons.cat.<i>`

```
GET https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=vertebra%20radiograph%20filetype:bitmap&srnamespace=6&srlimit=50&sroffset=0&format=json
GET https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:X-rays%20of%20the%20human%20spine&cmtype=file&cmlimit=500&format=json
GET https://commons.wikimedia.org/w/api.php?action=query&titles=<batch of 50>&prop=imageinfo&iiprop=url|size|mime|sha1|extmetadata&format=json
```
Grid SPINE_R × MODALITY_R with `filetype:bitmap`. Commons is charted as one figure-derived
source; individual files are not datasets, but categories with ≥ 10 subject images and a
licence are recorded as a candidate collection with `n_subjects = unknown`.

### J-STAGE — query_ids `jstage.<lang>.<i>`

```
GET https://api.jstage.jst.go.jp/searchapi/do?service=3&text=vertebra%20CT%20dataset&pubyearfrom=2000&pubyearto=2026&start=1&count=1000
GET https://api.jstage.jst.go.jp/searchapi/do?service=3&text=%E8%84%8A%E6%A4%8E%20CT%20%E3%83%87%E3%83%BC%E3%82%BF%E3%83%99%E3%83%BC%E3%82%B9&pubyearfrom=2000&pubyearto=2026&start=1&count=1000
```
(`脊椎 CT データベース`.) Grid SPINE_R × MODALITY_R × {dataset, database} in English and the
Japanese equivalents `脊椎, 椎体, 腰椎, 胸椎, 頸椎` × `CT, X線, 単純X線, 透視` × `データセット,
データベース`. Atom parsed for title (en/ja), abstract, DOI, year.

### KoreaMed / Synapse — query_ids `koreamed.<i>`

```
GET https://koreamed.org/search?searchWord=vertebra%20CT%20dataset&pageNumber=1
```
HTML, regex for article ids/titles/DOIs, `html-fallback`. Grid SPINE_R × {CT, radiograph} ×
{dataset, database}. Every hit is expected to merge with a PubMed record; the count that does
not is the coverage finding.

### SciELO — query_ids `scielo.<lang>.<i>`

```
GET https://search.scielo.org/?q=vertebra%20AND%20(radiograph%20OR%20tomograph*)%20AND%20(dataset%20OR%20database)&lang=en&count=100&from=1&output=xml
GET https://search.scielo.org/?q=v%C3%A9rtebra%20AND%20(radiograf%C3%ADa%20OR%20tomograf%C3%ADa)%20AND%20(%22base%20de%20datos%22%20OR%20%22conjunto%20de%20datos%22)&lang=es&count=100&from=1&output=xml
GET https://search.scielo.org/?q=v%C3%A9rtebra%20AND%20(radiografia%20OR%20tomografia)%20AND%20(%22banco%20de%20dados%22%20OR%20%22conjunto%20de%20dados%22)&lang=pt&count=100&from=1&output=xml
```
Reasoning: SciELO's portal accepts boolean in `q` (verify on first run; if not, the grid form
is used and recorded). If `output=xml` is not served, the HTML is parsed (`html-fallback`).

### Redalyc — query_id `redalyc.<i>`

The site's front-end JSON search endpoint is discovered on the first run by inspecting the
network calls of `https://www.redalyc.org/busquedaArticuloFiltros.oa`; the URL is recorded in
`queries.json` and the log before any hit is counted. Grid as SciELO (es/pt/en). If nothing
answers with JSON: `no-public-api`.

### Springer Nature Meta (supplementary) — query_id `springer.scidata`

```
GET https://api.springernature.com/meta/v2/json?q=journalid:41597%20AND%20(spine%20OR%20spinal%20OR%20vertebra%20OR%20vertebrae%20OR%20vertebral%20OR%20lumbar%20OR%20thoracic%20OR%20scoliosis)%20AND%20year:2014-2026&s=1&p=100&api_key=<redacted>
```
Reasoning: Scientific Data (journalid 41597) is the dominant descriptor venue; this keyed
route returns abstracts and `url` fields in bulk. `SPRINGER_API_META_KEY` absent → skipped
and logged; PubMed `pubmed.venues` covers the same journal.

### Unpaywall (supplementary, charting only) — query_id `unpaywall.<doi>`

```
GET https://api.unpaywall.org/v2/10.1038/s41597-020-0517-9?email=<redacted>
```
One call per DOI whose full text is needed at charting; `best_oa_location.url_for_pdf`
recorded; the PDF fetch is logged like any other request and cached under `raw/fulltext/`.

## What is recorded for every query (the appendix row)

`queries.json[query_id] = {source, endpoint, method, query_string (verbatim, unencoded),
params (secret-stripped), grammar ("boolean" | "grid" | "dump-filter" | "list"), run_date,
first_request_ts, last_request_ts, hit_count_api, n_retrieved, n_pages, cap_hit (null or the
cap), credential_mode ("keyed" | "credential-free" | "needs-credentials" | "html-fallback" |
"no-public-api" | "retired"), notes}`. `sdr/appendix.py` renders it to `tables/search_strings.tex`.
