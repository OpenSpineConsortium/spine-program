"""Offline fixture test for sdr.search_literature: hand-counted expectations against a replayed cache.

WHAT. Builds tests/fixture_lit_run/ with a raw cache of canned API bodies (envelopes keyed exactly as
sdr.common.RateLimitedSession keys them), a tiny query file, and runs the module with --replay so no
network is touched. Then compares counts.json, queries.json and records/*.jsonl with the numbers
worked out by hand in EXPECTED below.

WHY. The module's statistics are counts: API hit count, items retrieved, requests, pages, and the
within-source de-duplication by record id. The live run cannot check them (the truth is unknown), so
this fixture fixes a truth small enough to count on paper, and exercises the paths a --limit 3 smoke
run never reaches: PubMed's >9,999 [dp] split, Europe PMC's repeated-cursor stop, OpenAlex's 400 ->
grid fallback, Semantic Scholar's token paging (cache salt), Crossref pass (a) local modality filter
and the 400 -> a/b/c split, and the bioRxiv monthly dump filter.

Hand calculation (one line per expectation; the assertions below encode the same numbers):
  pubmed_01  esearch count 10001 -> re-queued as 01a-01d, row counts only        hits 10001, ret 0, req 1
  pubmed_01a count 2, efetch PMIDs 111 (DOI 10.1000/a), 222 (no DOI)                hits 2, ret 2, req 2
  pubmed_01b/c/d count 0 -> no efetch                                            hits 0, ret 0, req 1 each
  pubmed_02  count 2, efetch PMIDs 222, 333                                      hits 2, ret 2, req 2
  pubmed within-source: items 2+2 = 4; ids doi:10.1000/a, pmid:222, pmid:333 -> 3 records;
             pmid:222 carries query_ids [pubmed_01a, pubmed_02]
  epmc_01    page * : hitCount 3, 2 results, next C2; page C2: 1 result, next C2 (== cursor -> stop)
             hits 3, ret 3, req 2 ; epmc_02: hitCount 1, one result (PMID 444 again), next * -> stop
             items 3+1 = 4; ids doi:10.1000/a, native:epmc:PPR:PPR1, pmid:444 -> 3 records
             the first result's abstractText carries JATS markup (<h4>Objectives</h4>, L<sub>5</sub>);
             the stored abstract must hold no '<' and no tag-split token (resultType=core, L2)
  openalex_01 page *: count 2, 1 result (W1, DOI 10.1000/a), next OC2; page OC2: 1 result (W2 dataset, no ids), next null
             hits 2, ret 2, req 2 ; openalex_02: 400 on page 1 -> re-queued as openalex_02_g01, _g02
             g01: count 1 (W3, DOI 10.1000/c); g02: count 0 ; items 2+0+1+0 = 3 -> 3 records
  s2_01      page 1: total 3, 2 papers, token T2; page 2 (token T2): 1 paper, no token
             hits 3, ret 3, req 2 ; ids doi:10.1000/a, arxiv:2101.00001, native:s2:P3 -> 3 records
  arxiv_01   totalResults 2, 2 entries, start 500 >= 2 -> stop                   hits 2, ret 2, req 1
  arxiv_02   transient all-zeros feed (no entries, totalResults 0) at start 0, retry1 carries
             totalResults 1 and one entry: the retry fires on the empty feed alone, and the recovered
             page's count replaces the zero                                      hits 1, ret 1, req 2
  arxiv_03   all-zeros on all four attempts: no bare zero is recorded          hits None, ret 0, req 4
             arxiv items 2+1+0 = 3, all distinct ids -> 3 records
  crossref_01 pass (a): total 3, items D1 "Spine CT dataset", D2 "Spine radiograph collection",
             D3 "Spine morphology tables" -> MODALITY_RE keeps D1, D2                hits 3, ret 2, req 1
  crossref_12 pass (b): total 2, items J1 (DOI 10.1000/a), J2 (DOI 10.1000/d)           hits 2, ret 2, req 1
  crossref_13 pass (b): 400 -> 13a/13b/13c one type each; 13a total 1 (J5, DOI 10.1000/e); 13b, 13c 0
             items 2+2+0+1+0+0 = 5, all distinct DOIs -> 5 records (D1, D2 are repo:, the rest lit:)
  biorxiv_01 (--limit 1: one month) 2013-11: total 2; B1 "A lumbar spine CT dataset ..." passes the
             three regexes, B2 "Mouse neuron ..." fails                            hits 2, ret 1, req 1
  medrxiv_01 2019-06: total 2, the same DOI at versions 1 and 2 -> kept once (v2) hits 2, ret 1, req 1
             biorxiv items 1+1 = 2 -> 2 records
  requests logged, all from_cache: pubmed 8 (1 + 2 + 1 + 1 + 1 + 2), epmc 3, openalex 5, s2 2, arxiv 7 (1 + 2 + 4),
  crossref 6, biorxiv 2 = 33
  retrieved_at on every record == the envelope's retrieved_at (replay reproduces timestamps)

It also checks the one thing about this module that no run can: `queries/literature.yaml` holds a second
copy of the `coverage` and `raw_cache_published` cells that the adapters read from the summary table of
information_sources.md (`sdr.common.source_table`), and sdr.manuscript merges the YAML underneath
queries.json, so the copy is invisible while it disagrees. The eight literature source codes are compared
cell by cell here.

Run:  ~/sdr_venv/bin/python tests/test_search_literature_fixture.py     (from spine_data_review/, WSL)
Exit 0 when every expectation holds; the first failure is printed with the observed value.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sdr.common import RateLimitedSession, RunDir, _canonical_url, contact, cred, load_queries, source_table, strip_params  # noqa: E402
import sdr.search_literature as L  # noqa: E402

RUN = ROOT / "tests" / "fixture_lit_run"
QFILE = ROOT / "tests" / "fixture_lit_queries.yaml"
TS = "2026-09-19T00:00:00Z"
PY = sys.executable

Q = {
    "pubmed_01": 'fixture pubmed one AND ("2000/01/01"[dp] : "2026/12/31"[dp])',
    "pubmed_02": "fixture pubmed two",
    "epmc_01": "TITLE:fixture one", "epmc_02": "TITLE:fixture two",
    "openalex_01": "title_and_abstract.search:fixture,publication_year:2000-2026",
    "openalex_02": "type:dataset,title_and_abstract.search:fixture,publication_year:2000-2026",
    "g01": "fixture g one", "g02": "fixture g two",
    "s2_01": "fixture s2", "arxiv_01": "all:fixture", "arxiv_02": "all:fixture recovered", "arxiv_03": "all:fixture empty",
    "crossref_01": "spine", "crossref_12": "fixture triple", "crossref_13": "fixture split",
    "biorxiv_01": "https://api.biorxiv.org/details/biorxiv/<from>/<to>/<cursor>/json",
    "medrxiv_01": "https://api.biorxiv.org/details/medrxiv/<from>/<to>/<cursor>/json",
}


# `keyed` per source exactly as the adapters decide it: the session puts a `keyed` line in the cache key.
KEYED = {"pubmed": bool(cred("NCBI_API_KEY")), "s2": bool(cred("S2_API_KEY")), "openalex": bool(contact()), "crossref": bool(contact())}


def put(source: str, url: str, params: dict, body, status: int = 200, cache_salt: str = "") -> str:
    """Write one cache envelope exactly where RateLimitedSession.get would look for it: the key comes from
    the session's own `cache_path`, so a change in the key material cannot silently strand the fixture."""
    sparams = strip_params(params)
    sha1, p = RateLimitedSession(RunDir(RUN)).cache_path(source, url, params, cache_salt=cache_salt, keyed=KEYED.get(source, False))
    text = body if isinstance(body, str) else json.dumps(body)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"sha1": sha1, "method": "GET", "url": _canonical_url(url), "params": sparams, "status": status,
                             "headers": {}, "retrieved_at": TS, "body": text}, sort_keys=True), encoding="utf-8")
    return sha1


def pubmed_xml(*arts) -> str:
    items = []
    for pmid, doi, title in arts:
        ids = f'<ArticleId IdType="doi">{doi}</ArticleId>' if doi else ""
        items.append(f"<PubmedArticle><MedlineCitation><PMID>{pmid}</PMID><Article><Journal><Title>J</Title><JournalIssue>"
                     f"<PubDate><Year>2020</Year></PubDate></JournalIssue></Journal><ArticleTitle>{title}</ArticleTitle>"
                     f"<Abstract><AbstractText>Lumbar spine CT dataset.</AbstractText></Abstract><AuthorList><Author>"
                     f"<LastName>Doe</LastName></Author></AuthorList></Article></MedlineCitation><PubmedData><ArticleIdList>"
                     f'<ArticleId IdType="pubmed">{pmid}</ArticleId>{ids}</ArticleIdList></PubmedData></PubmedArticle>')
    return '<?xml version="1.0"?><PubmedArticleSet>' + "".join(items) + "</PubmedArticleSet>"


def build() -> None:
    shutil.rmtree(RUN, ignore_errors=True)
    QFILE.write_text("".join(f"{k}: {json.dumps(v)}\n" for k, v in Q.items()), encoding="utf-8")
    keyp = {"api_key": "x"} if cred("NCBI_API_KEY") else {}
    em = {"mailto": "x"} if contact() else {}
    # PubMed: esearch (count) then efetch by history; the split strings are what _DP.sub produces.
    def es(qid, term, count, key):
        put("pubmed", L._EU + "esearch.fcgi", {"db": "pubmed", "term": term, "usehistory": "y", "retmax": 0, "retmode": "json", **keyp},
            {"esearchresult": {"count": str(count), "querykey": str(key), "webenv": f"WE{key}"}})
    es("pubmed_01", Q["pubmed_01"], 10001, 1)
    for lo, hi, suf, n in (("2000", "2015", "a", 2), ("2016", "2020", "b", 0), ("2021", "2023", "c", 0), ("2024", "2026", "d", 0)):
        es("pubmed_01" + suf, f'fixture pubmed one AND ("{lo}/01/01"[dp] : "{hi}/12/31"[dp])', n, "1" + suf)
    es("pubmed_02", Q["pubmed_02"], 2, 2)
    put("pubmed", L._EU + "efetch.fcgi", {"db": "pubmed", "query_key": "1a", "WebEnv": "WE1a", "retstart": 0, "retmax": 2, "retmode": "xml", **keyp},
        pubmed_xml(("111", "10.1000/a", "Spine CT one"), ("222", None, "Spine CT two")))
    put("pubmed", L._EU + "efetch.fcgi", {"db": "pubmed", "query_key": "2", "WebEnv": "WE2", "retstart": 0, "retmax": 2, "retmode": "xml", **keyp},
        pubmed_xml(("222", None, "Spine CT two"), ("333", None, "Spine CT three")))
    # Europe PMC: cursorMark paging, stop when nextCursorMark repeats.
    base = {"resultType": "core", "format": "json", "pageSize": 1000}
    put("epmc", L._EPMC, {**base, "query": Q["epmc_01"], "cursorMark": "*"},
        {"hitCount": 3, "nextCursorMark": "C2", "resultList": {"result": [
            {"id": "111", "source": "MED", "pmid": "111", "doi": "10.1000/a", "title": "Spine CT one", "pubYear": "2020",
             "abstractText": "<h4>Objectives</h4>To release a lumbar spine CT dataset.<h4>Methods</h4>L<sub>5</sub> was measured <i>in vivo</i>."},
            {"id": "PPR1", "source": "PPR", "title": "Preprint spine", "pubYear": "2021"}]}})
    put("epmc", L._EPMC, {**base, "query": Q["epmc_01"], "cursorMark": "C2"},
        {"hitCount": 3, "nextCursorMark": "C2", "resultList": {"result": [{"id": "444", "source": "MED", "pmid": "444", "title": "Four", "pubYear": "2019"}]}})
    put("epmc", L._EPMC, {**base, "query": Q["epmc_02"], "cursorMark": "*"},
        {"hitCount": 1, "nextCursorMark": "*", "resultList": {"result": [{"id": "444", "source": "MED", "pmid": "444", "title": "Four", "pubYear": "2019"}]}})
    # OpenAlex: cursor paging; openalex_02 rejected with 400 -> grid g01, g02.
    ob = {"per-page": 200, "select": L._OA_SELECT, **em}
    put("openalex", L._OA, {**ob, "filter": Q["openalex_01"], "cursor": "*"},
        {"meta": {"count": 2, "next_cursor": "OC2"}, "results": [{"id": "https://openalex.org/W1", "doi": "https://doi.org/10.1000/a", "ids": {},
                                                                  "display_name": "Spine CT one", "publication_year": 2020, "type": "article",
                                                                  "abstract_inverted_index": {"lumbar": [0], "spine": [1]}}]})
    put("openalex", L._OA, {**ob, "filter": Q["openalex_01"], "cursor": "OC2"},
        {"meta": {"count": 2, "next_cursor": None}, "results": [{"id": "https://openalex.org/W2", "ids": {}, "display_name": "A dataset", "publication_year": 2022, "type": "dataset"}]})
    put("openalex", L._OA, {**ob, "filter": Q["openalex_02"], "cursor": "*"}, {"error": "bad filter"}, status=400)
    for g, n in (("g01", 1), ("g02", 0)):
        filt = f"type:dataset,title_and_abstract.search:{Q[g]},publication_year:2000-2026"
        res = [{"id": "https://openalex.org/W3", "doi": "https://doi.org/10.1000/c", "ids": {}, "display_name": "Grid hit", "publication_year": 2021, "type": "dataset"}] if n else []
        put("openalex", L._OA, {**ob, "filter": filt, "cursor": "*"}, {"meta": {"count": n, "next_cursor": None}, "results": res})
    # Semantic Scholar: token paging; the token is redacted in the key so it is also the cache salt.
    sb = {"query": Q["s2_01"], "year": "2000-2026", "fields": L._S2_FIELDS}
    put("s2", L._S2, sb, {"total": 3, "token": "T2", "data": [
        {"paperId": "P1", "externalIds": {"DOI": "10.1000/a"}, "title": "Spine CT one", "year": 2020},
        {"paperId": "P2", "externalIds": {"ArXiv": "2101.00001"}, "title": "Arxiv one", "year": 2021}]})
    put("s2", L._S2, {**sb, "token": "T2"}, {"total": 3, "token": None, "data": [{"paperId": "P3", "externalIds": {}, "title": "No ids", "year": 2019}]},
        cache_salt="T2")
    # arXiv: one good Atom page, one all-zeros feed that the retry recovers, one that never does.
    ax = lambda qid, start=0: {"search_query": Q[qid], "max_results": 500, "sortBy": "submittedDate", "sortOrder": "ascending", "start": start}  # noqa: E731
    feed = lambda total, entries="": ('<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom" '  # noqa: E731
                                      'xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:arxiv="http://arxiv.org/schemas/atom">'
                                      f"<opensearch:totalResults>{total}</opensearch:totalResults>{entries}</feed>")
    entry = lambda aid, title, summary, d: (f"<entry><id>http://arxiv.org/abs/{aid}</id><title>{title}</title>"  # noqa: E731
                                            f"<summary>{summary}</summary><published>{d}T00:00:00Z</published></entry>")
    put("arxiv", L._AX, ax("arxiv_01"),
        feed(2, entry("2101.00001v2", "Arxiv one", "Spine CT dataset", "2021-01-01")
             + entry("2102.00002v1", "Arxiv two", "Spine radiograph dataset", "2021-02-01")))
    put("arxiv", L._AX, ax("arxiv_02"), feed(0))                      # transient form: entries AND totalResults zeroed
    put("arxiv", L._AX, ax("arxiv_02"), feed(1, entry("2103.00003v1", "Arxiv three", "Spine radiograph dataset", "2021-03-01")),
        cache_salt="retry1")
    put("arxiv", L._AX, ax("arxiv_03"), feed(0))
    for n in (1, 2, 3):
        put("arxiv", L._AX, ax("arxiv_03"), feed(0), cache_salt=f"retry{n}")
    # Crossref: pass (a) with the local modality filter, pass (b), and the 400 -> a/b/c split.
    cb = {"rows": 1000, "select": L._CR_SELECT, **em, "cursor": "*"}
    item = lambda doi, title, typ: {"DOI": doi, "title": [title], "type": typ, "issued": {"date-parts": [[2020]]}}  # noqa: E731
    put("crossref", L._CR, {**cb, "query.bibliographic": "spine", "filter": "type:dataset," + L._CR_DATES},
        {"message": {"total-results": 3, "next-cursor": "CC2", "items": [item("10.1000/d1", "Spine CT dataset", "dataset"),
                                                                        item("10.1000/d2", "Spine radiograph collection", "dataset"),
                                                                        item("10.1000/d3", "Spine morphology tables", "dataset")]}})
    fb = "type:journal-article,type:posted-content,type:proceedings-article,has-abstract:true," + L._CR_DATES
    put("crossref", L._CR, {**cb, "query.bibliographic": Q["crossref_12"], "filter": fb},
        {"message": {"total-results": 2, "next-cursor": "X", "items": [item("10.1000/a", "Spine CT one", "journal-article"), item("10.1000/d", "J two", "journal-article")]}})
    put("crossref", L._CR, {**cb, "query.bibliographic": Q["crossref_13"], "filter": fb}, {"status": "failed"}, status=400)
    for t, n in zip(L._CR_B_TYPES, (1, 0, 0)):
        put("crossref", L._CR, {**cb, "query.bibliographic": Q["crossref_13"], "filter": f"type:{t},has-abstract:true," + L._CR_DATES},
            {"message": {"total-results": n, "next-cursor": "Y", "items": [item("10.1000/e", "J five", t)] if n else []}})
    # bioRxiv / medRxiv: one month each (--limit 1), cursor 0.
    put("biorxiv", L._BX.format(server="biorxiv", a="2013-11-01", b="2013-11-30", cursor=0), {},
        {"messages": [{"total": 2}], "collection": [
            {"doi": "10.1101/b1", "title": "A lumbar spine CT dataset", "abstract": "publicly available", "version": "1", "date": "2013-11-02"},
            {"doi": "10.1101/b2", "title": "Mouse neuron imaging", "abstract": "none", "version": "1", "date": "2013-11-03"}]})
    put("biorxiv", L._BX.format(server="medrxiv", a="2019-06-01", b="2019-06-30", cursor=0), {},
        {"messages": [{"total": 2}], "collection": [
            {"doi": "10.1101/m1", "title": "Public radiograph database of scoliosis", "abstract": "x", "version": "1", "date": "2019-06-02"},
            {"doi": "10.1101/m1", "title": "Public radiograph database of scoliosis", "abstract": "x", "version": "2", "date": "2019-06-20"}]})


def run(*extra: str) -> None:
    cmd = [PY, "-m", "sdr.search_literature", "--run-dir", str(RUN.relative_to(ROOT)), "--run-date", "2026-09-19", "--replay",
           "--queries", str(QFILE.relative_to(ROOT)), *extra]
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"module failed: {' '.join(cmd)}\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")


EXPECTED = {  # source: (n_items, n_records, {qid: (hit_count_api, n_retrieved, n_requests)})
    "pubmed": (4, 3, {"pubmed_01": (10001, 0, 1), "pubmed_01a": (2, 2, 2), "pubmed_01b": (0, 0, 1), "pubmed_01c": (0, 0, 1),
                      "pubmed_01d": (0, 0, 1), "pubmed_02": (2, 2, 2)}),
    "epmc": (4, 3, {"epmc_01": (3, 3, 2), "epmc_02": (1, 1, 1)}),
    "openalex": (3, 3, {"openalex_01": (2, 2, 2), "openalex_02": (None, 0, 1), "openalex_02_g01": (1, 1, 1), "openalex_02_g02": (0, 0, 1)}),
    "s2": (3, 3, {"s2_01": (3, 3, 2)}),
    "arxiv": (3, 3, {"arxiv_01": (2, 2, 1), "arxiv_02": (1, 1, 2), "arxiv_03": (None, 0, 4)}),
    "crossref": (5, 5, {"crossref_01": (3, 2, 1), "crossref_12": (2, 2, 1), "crossref_13": (None, 0, 1), "crossref_13a": (1, 1, 1),
                        "crossref_13b": (0, 0, 1), "crossref_13c": (0, 0, 1)}),
    "biorxiv": (2, 2, {"biorxiv_01": (2, 1, 1), "medrxiv_01": (2, 1, 1)}),
}


def check_yaml_against_summary_table(ok) -> int:
    """queries/literature.yaml duplicates two summary-table cells per entry; `_meta` reads them from the table,
    so the YAML copy is free to drift unchecked (it did, for six of the eight literature sources). Compared here
    for L1-L7 and S1: `coverage` byte for byte, `raw_cache_published` against the table's yes/no. The long
    `raw_cache_reason` prose is deliberately not compared - the table cell is the authority and the YAML says
    the same thing at length."""
    st, qs, n = source_table(), load_queries(ROOT / "queries" / "literature.yaml"), 0
    for qid, y in sorted(qs.items()):
        code = y.get("source_code")
        if code not in ("L1", "L2", "L3", "L4", "L5", "L6", "L7", "S1"):
            continue
        n += 1
        row = st[code]
        ok(y.get("coverage") == row["coverage"], f"{qid}: yaml coverage {y.get('coverage')!r} != summary table {code} {row['coverage']!r}")
        ok(y.get("raw_cache_published") == row["raw_cache"].startswith("yes"),
           f"{qid}: yaml raw_cache_published {y.get('raw_cache_published')!r} != summary table {code} {row['raw_cache']!r}")
    return n


def check() -> int:
    fails = []
    ok = lambda cond, msg: None if cond else fails.append(msg)  # noqa: E731
    n_yaml = check_yaml_against_summary_table(ok)
    counts = json.loads((RUN / "counts.json").read_text(encoding="utf-8"))
    queries = json.loads((RUN / "queries.json").read_text(encoding="utf-8"))
    for src, (n_items, n_recs, qexp) in EXPECTED.items():
        c = counts.get(src, {})
        ok(c.get("n_items") == n_items, f"{src}: n_items {c.get('n_items')} != {n_items}")
        ok(c.get("n_records_after_within_source_dedup") == n_recs, f"{src}: n_records {c.get('n_records_after_within_source_dedup')} != {n_recs}")
        ok(set(c.get("queries", {})) == set(qexp), f"{src}: query ids {sorted(c.get('queries', {}))} != {sorted(qexp)}")
        for qid, (hits, ret, req) in qexp.items():
            q = queries.get(qid, {})
            ok(q.get("hit_count_api") == hits, f"{qid}: hit_count_api {q.get('hit_count_api')} != {hits}")
            ok(q.get("n_retrieved") == ret, f"{qid}: n_retrieved {q.get('n_retrieved')} != {ret}")
            ok(q.get("n_requests") == req, f"{qid}: n_requests {q.get('n_requests')} != {req}")
            ok(q.get("first_request_ts") == TS, f"{qid}: first_request_ts {q.get('first_request_ts')} != envelope {TS}")
        recs = [json.loads(l) for l in (RUN / "records" / f"{src}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        ok(len(recs) == n_recs, f"{src}: {len(recs)} lines in records file != {n_recs}")
        ok(all(r["retrieved_at"] == TS for r in recs), f"{src}: retrieved_at not taken from the envelope")
        ok([r["record_id"] for r in recs] == sorted(r["record_id"] for r in recs), f"{src}: records not sorted by record_id")
    pm = {r["canonical"]: r for r in (json.loads(l) for l in (RUN / "records" / "pubmed.jsonl").read_text(encoding="utf-8").splitlines())}
    ok(set(pm) == {"doi:10.1000/a", "pmid:222", "pmid:333"}, f"pubmed canonicals {sorted(pm)}")
    ok(pm.get("pmid:222", {}).get("query_ids") == ["pubmed_01a", "pubmed_02"], f"pmid:222 query_ids {pm.get('pmid:222', {}).get('query_ids')}")
    ok(pm.get("pmid:222", {}).get("query_id") == "pubmed_01a", "pmid:222 query_id is not the first sorted query")
    cr = {r["canonical"]: r["record_id"][:4] for r in (json.loads(l) for l in (RUN / "records" / "crossref.jsonl").read_text(encoding="utf-8").splitlines())}
    ok(cr == {"doi:10.1000/d1": "repo", "doi:10.1000/d2": "repo", "doi:10.1000/a": "lit:", "doi:10.1000/d": "lit:", "doi:10.1000/e": "lit:"}, f"crossref ids/prefixes {cr}")
    ok("3 items retrieved, 2 kept" in queries["crossref_01"]["notes"], f"crossref_01 notes: {queries['crossref_01']['notes']}")
    ok("re-run as a/b/c" in queries["crossref_13"]["notes"], f"crossref_13 notes: {queries['crossref_13']['notes']}")
    ok("re-run as grid" in queries["openalex_02"]["notes"], f"openalex_02 notes: {queries['openalex_02']['notes']}")
    ok("count > 9999" in queries["pubmed_01"]["notes"], f"pubmed_01 notes: {queries['pubmed_01']['notes']}")
    ep = {r["canonical"]: r["abstract_or_description"] for r in (json.loads(l) for l in (RUN / "records" / "epmc.jsonl").read_text(encoding="utf-8").splitlines())}
    a111 = ep.get("doi:10.1000/a", "")
    ok("<" not in a111, f"epmc abstract kept JATS markup: {a111!r}")
    ok("L 5 " in a111 and "Objectives To release" in a111, f"epmc abstract not stripped as expected: {a111!r}")
    ok("hit count not established" in queries["arxiv_03"]["notes"], f"arxiv_03 notes: {queries['arxiv_03']['notes']}")
    ok(queries["arxiv_03"]["cap_hit"] is None, f"arxiv_03 cap_hit {queries['arxiv_03']['cap_hit']} is not null")
    ok(queries["arxiv_02"]["notes"] == "", f"arxiv_02 recovered but noted {queries['arxiv_02']['notes']!r}")
    bx = {r["ids"]["doi"]: r["raw"]["version"] for r in (json.loads(l) for l in (RUN / "records" / "biorxiv.jsonl").read_text(encoding="utf-8").splitlines())}
    ok(bx == {"10.1101/b1": "1", "10.1101/m1": "2"}, f"biorxiv records/versions {bx}")
    log = [json.loads(l) for l in (RUN / "requests.log.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    per = {}
    for row in log:
        per[row["source"]] = per.get(row["source"], 0) + 1
    ok(per == {"pubmed": 8, "epmc": 3, "openalex": 5, "s2": 2, "arxiv": 7, "crossref": 6, "biorxiv": 2}, f"log lines per source {per}")
    ok(all(row["from_cache"] for row in log), "a replay request was not served from the cache")
    ok(all((RUN / "raw" / row["source"] / f"{row['cache_sha1']}.json").exists() for row in log), "a logged cache_sha1 has no envelope")
    ok(not any(v == "x" for row in log for v in row["params"].values()), "a credential placeholder reached the log unredacted")
    for f in fails:
        print("FAIL", f)
    print(f"{len(fails)} failures; {sum(len(v[2]) for v in EXPECTED.values())} query rows, {len(log)} log lines and "
          f"{n_yaml} yaml entries against the summary table checked")
    return 1 if fails else 0


if __name__ == "__main__":
    build()
    run("--source", "pubmed,epmc,openalex,s2,arxiv,crossref")
    run("--source", "biorxiv", "--limit", "1")
    sys.exit(check())
