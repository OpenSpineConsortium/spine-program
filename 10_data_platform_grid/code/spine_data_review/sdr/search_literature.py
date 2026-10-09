"""Literature search L1-L7: PubMed, Europe PMC, OpenAlex, Semantic Scholar, arXiv, bioRxiv/medRxiv, Crossref.

WHAT. One CLI sends the verbatim strings of information_sources.md (read at run time through
`sdr.common.load_queries`, never copied here) to the seven literature indexes, pages each query to
completion or to --limit, and writes records/<source>.jsonl (one line per item, de-duplicated within
the source by record id, sorted), the queries.json entries Appendix A and the PRISMA flow are built
from, and counts.json. Pacing, retry, the request log and the raw cache are `sdr.common`'s; the
coverage and raw-cache cells of each entry are read from the summary table of information_sources.md
(`sdr.common.source_table`), so a change in the protocol file propagates without a code edit.

WHY ONE BOOKKEEPING OBJECT. Appendix A needs, per query_id, the string as sent, the API's hit count,
what was retrieved, pages, cap, credential mode and first/last timestamps, and the flow's per-source
row derives from the same numbers; seven private tallies would drift. So each adapter drives a
`Query`, which counts requests, takes the retrieval timestamp from the answer (a --replay run
reproduces it byte for byte) and applies --limit in one place.

Fallbacks the protocol fixes, each noted in queries.json (the deviations-log cue): PubMed splits a
string over 9,999 hits (NCBI history stops at retstart 9998) into [dp] ranges a-d and caps a sub-range
still over it; OpenAlex re-runs a rejected boolean filter (400) as the 35-string grid, taken from
information_sources.md when the query file lacks section G, and exits non-zero when neither has it;
Crossref pass (a) applies the modality block locally and pass (b) splits into single-type passes on
a 400; bioRxiv/medRxiv have no search, so monthly dumps up to the run date are filtered by the three
prescreen regexes; arXiv's transient empty feed (entries missing, totalResults kept or also zeroed) is
refetched three times under fresh cache keys before a shortfall is recorded as a cap or, at start 0 with
no count in hand, before the hit count is recorded as not established; Europe PMC is asked for
resultType=core because lite carries no abstract and the prescreen reads one, and its JATS markup is
stripped before the record is stored (deviations log). Semantic Scholar elides the abstract of every
paper whose publisher forbids redistributing it, which `abstract_elided` records, and sdr.dedup_prescreen
sends an abstract-less literature record to `uncertain` rather than counting it as a modality or dataset
failure it was never tested for. Semantic Scholar's paging `token` is redacted
in the log, so it is also the cache salt. Session state (NCBI WebEnv, Crossref cursor, S2 token)
travels through the cache: a query resumed in the same run dir whose cached state leads to an uncached
page is restarted live under a resume salt (`Query.stale`), because the state may have expired.
Without NCBI_API_KEY or S2_API_KEY the same endpoint runs at the credential-free rate; without the
contact address OpenAlex and Crossref leave the polite pool.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from calendar import monthrange
from typing import NamedTuple

from sdr.common import (RateLimitedSession, RunDir, add_common_args, canonical_string, contact, cred, dump_json, init_run_dir,
                        load_queries, normalised_ids, now_iso, record_id, source_table, strip_params, write_jsonl)

SOURCES = ("pubmed", "epmc", "openalex", "s2", "arxiv", "biorxiv", "crossref", "springer")
_CODES = dict(zip(SOURCES, ("L1", "L2", "L3", "L4", "L5", "L6", "L7", "S1")))  # summary-table row per source
_META: dict[str, tuple[str, bool, str]] = {}
# PROTOCOL.md Appendix A, the local filter for L6 and Crossref pass (a).
# candidate for common.py: sdr.prescreen needs the same three and they must stay byte-identical.
SPINE_RE = re.compile(r"\b(spine|spinal|vertebr\w*|lumbar|lumbo-?sacral|thoraco-?lumbar|sacrum|cervical spine|thoracic spine|scoliosis"
                      r"|spondylo\w*|intervertebral|pedicle)\b", re.I)
MODALITY_RE = re.compile(r"(\bcomputed tomograph\w*|\bCT\b|\bCBCT\b|cone-?beam|radiograph\w*|\bx-?rays?\b|roentgen\w*|fluoroscop\w*|\bc-?arm\b"
                         r"|image intensifier|\bDXA\b|\bDEXA\b|dual-energy x-?ray|absorptiometry|vertebral fracture assessment|\bEOS\b"
                         r"|biplanar|plain films?)", re.I)
DATASET_RE = re.compile(r"\b(data\s?sets?|database|benchmark\w*|challenge|publicly available|public(ly)? (data|release)|open(-| )?(access|source"
                        r"|data)|data descriptor|corpus|image collection|repository|zenodo|figshare|physionet|kaggle|hugging ?face"
                        r"|grand-?challenge|github|download)\b", re.I)
_EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
_NCBI_MAX, _NCBI_PAGE = 9999, 500  # history paging answers 400 above retstart 9998, verified live; information_sources.md L1
_EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
_OA = "https://api.openalex.org/works"
_OA_SELECT = "id,doi,ids,title,display_name,publication_year,type,primary_location,open_access,abstract_inverted_index,referenced_works,cited_by_count,authorships"
_S2 = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
_S2_FIELDS = "paperId,externalIds,title,abstract,year,venue,publicationTypes,isOpenAccess,openAccessPdf,citationCount,authors"
_AX = "http://export.arxiv.org/api/query"
_NS = {"a": "http://www.w3.org/2005/Atom", "os": "http://a9.com/-/spec/opensearch/1.1/", "ax": "http://arxiv.org/schemas/atom"}
_BX = "https://api.biorxiv.org/details/{server}/{a}/{b}/{cursor}/json"
_BX_START = {"biorxiv": (2013, 11), "medrxiv": (2019, 6)}
_BX_FILTER = "SPINE_RE AND MODALITY_RE AND DATASET_RE over title + abstract"
_CR = "https://api.crossref.org/works"
_CR_SELECT = "DOI,title,abstract,type,container-title,publisher,issued,URL,license,relation,subject,author"
_CR_DATES = "from-pub-date:2000-01-01,until-pub-date:2026-12-31"
_CR_B_TYPES = ("journal-article", "posted-content", "proceedings-article")
_CR_CAP = 5000
_DP = re.compile(r'\("\d{4}/01/01"\[dp\] : "\d{4}/12/31"\[dp\]\)')
_DP_SPLITS = (("2000", "2015", "a"), ("2016", "2020", "b"), ("2021", "2023", "c"), ("2024", "2026", "d"))
_TAG = re.compile(r"<[^>]+>")


# What every adapter needs: the session, the run dir, the run date and --limit.
Ctx = NamedTuple("Ctx", [("sess", RateLimitedSession), ("rd", RunDir), ("run_date", str), ("limit", "int | None")])


def _meta(source: str) -> tuple[str, bool, str]:
    """(coverage, raw_cache_published, raw_cache_note) from the source's summary-table row; "yes (NLM terms)" gives
    (True, "NLM terms"), "no ..." or "partial ..." gives (False, the cell verbatim)."""
    if source not in _META:
        row = source_table()[_CODES[source]]
        rc = row["raw_cache"]
        _META[source] = (row["coverage"], rc.startswith("yes"), rc[3:].strip().strip("()") if rc.startswith("yes") else rc)
    return _META[source]


class Query:
    """Bookkeeping for one query_id ("What is recorded for every query", information_sources.md). `get`
    wraps the session so requests, pages and timestamps are counted once; `take` appends records up
    to --limit and says when it is reached; `stale` detects a resume on expired session state; `entry`
    is the queries.json value."""

    def __init__(self, ctx, source, qid, string, endpoint, grammar, params, mode, intervals=None, date_filter="api",
                 role="search"):
        self.ctx, self.source, self.qid, self.string, self.endpoint = ctx, source, qid, string, endpoint
        self.grammar, self.params, self.mode, self.intervals, self.date_filter = grammar, params, mode, intervals, date_filter
        # The role the adapter is playing, stated by the caller and compared with queries/*.yaml by
        # tests/test_queries_yaml.py. It was hard-coded "search" in `entry`, so Appendix A printed "role search"
        # for S1, the supplementary venue sweep the protocol and the summary table call supplementary.
        self.role = role
        self.hits, self.cap, self.n_req, self.n_pages, self.ts, self.resume = None, None, 0, 0, "", 0
        self.stamps, self.notes, self.records, self.failed = [], [], [], False
        self.n_fetched: int | None = None  # items fetched before a local filter (Crossref pass (a), bioRxiv); else = n_retrieved

    def _salt(self, salt: str) -> str:
        return f"{salt}|resume{self.resume}" if self.resume else salt

    def get(self, url: str, params: dict | None = None, *, cache_salt: str = "", **kw):
        r = self.ctx.sess.get(self.source, self.qid, url, params, cache_salt=self._salt(cache_salt), **kw)
        self.n_req, self.n_pages = self.n_req + 1, self.n_pages + int(r.ok)
        self.ts = r.retrieved_at or now_iso()
        self.stamps.append(self.ts)
        if not r.ok:
            self.notes.append(f"status {r.status} at {url.rsplit('/', 1)[-1]}" + (f": {r.error}" if r.error else ""))
        return r

    def stale(self, r, url: str, pages: list[dict], cache_salt: str = "", keyed: bool = False) -> bool:
        """True when `r` came from the cache but a page its session state leads to (`pages` are the params of the
        next requests: efetch pages under a WebEnv, the next cursor or token page) is not cached. That is a query
        resumed in the same run dir after an interruption, and NCBI history, Crossref cursors and S2 tokens expire
        within hours, so the caller restarts the query from its first request; `get` then salts every cache key
        with resume<n>, and a --replay run follows the same salted chain. Records taken so far are dropped (the
        restart takes them again). Three restarts at most."""
        if not r.from_cache or self.resume >= 3 or all(self.ctx.sess.is_cached(self.source, url, p, cache_salt=self._salt(cache_salt), keyed=keyed)
                                                        for p in pages):
            return False
        self.resume += 1
        self.records.clear()
        self.notes.append(f"resumed in the same run dir: cached session state led to an uncached {url.rsplit('/', 1)[-1]} page; "
                          f"query restarted live (cache_salt resume{self.resume})")
        return True

    def body(self, r, xml: bool = False):
        """Parsed JSON or XML body, or None (noted) when the answer is not ok or does not parse."""
        if not r.ok:
            return None
        try:
            return ET.fromstring(r.text) if xml else r.json()
        except (ValueError, ET.ParseError) as e:
            self.notes.append(f"unparseable body sha1={r.sha1}: {type(e).__name__}")
            return None

    def take(self, items) -> bool:
        """Append records; True once --limit records are held or --limit pages were fetched (a local
        filter such as Crossref pass (a) could otherwise page for thousands of requests in a smoke test)."""
        lim = self.ctx.limit
        for rec in items:
            if lim is not None and len(self.records) >= lim:
                return True
            self.records.append(rec)
        return lim is not None and (len(self.records) >= lim or self.n_pages >= lim)

    def entry(self) -> dict:
        cov, pub, why = _meta(self.source)
        return {"source": self.source, "role": self.role, "endpoint": self.endpoint, "method": "GET", "query_string": self.string,
                "intervals": self.intervals, "n_requests": self.n_req, "params": strip_params(self.params), "grammar": self.grammar,
                "coverage": cov, "run_date": self.ctx.run_date, "first_request_ts": self.stamps[0] if self.stamps else None,
                "last_request_ts": self.stamps[-1] if self.stamps else None, "hit_count_api": self.hits, "n_retrieved": len(self.records),
                "n_fetched": len(self.records) if self.n_fetched is None else self.n_fetched,
                "n_pages": self.n_pages, "cap_hit": self.cap, "date_filter": self.date_filter, "credential_mode": self.mode,
                "raw_cache_published": pub, "raw_cache_note": why, "limit": self.ctx.limit, "notes": "; ".join(self.notes)}


def make_record(source, qid, ids, title, abstract, year, rtype, raw, native_id, ts) -> dict:
    """One records/<source>.jsonl line (PROTOCOL.md section 15) with the record id of sdr.ids."""
    canon = canonical_string(nids := normalised_ids(ids), source, native_id)
    m = re.match(r"\d{4}", str(year or ""))
    return {"record_id": record_id(canon, source, rtype), "canonical": canon, "source": source, "query_id": qid, "retrieved_at": ts,
            "ids": nids, "title": " ".join((title or "").split()), "abstract_or_description": " ".join((abstract or "").split()),
            "year": int(m.group()) if m else None, "type": rtype, "raw": raw}


def _ids_for(qs: dict, pattern: str) -> list[str]:
    return sorted(k for k in qs if re.fullmatch(pattern, k))


def _pick(d: dict, keys: str) -> dict:
    return {k: d.get(k) for k in keys.split()}


def _pubmed_record(art, qid, ts) -> dict:
    med, a = art.find("MedlineCitation"), art.find("MedlineCitation/Article")
    # Only the article's own ids: iter("ArticleId") would also walk the reference list and the last citation's DOI would win.
    pmid, aids = med.findtext("PMID"), {x.get("IdType"): (x.text or "") for x in art.findall("PubmedData/ArticleIdList/ArticleId")}
    title = "".join(a.find("ArticleTitle").itertext()) if a.find("ArticleTitle") is not None else ""
    abstract = " ".join(" ".join(x.itertext()).strip() for x in a.iter("AbstractText"))
    pd = "Journal/JournalIssue/PubDate/"
    year = a.findtext(pd + "Year") or a.findtext(pd + "MedlineDate") or a.findtext("ArticleDate/Year")
    raw = {"pmid": pmid, "journal": a.findtext("Journal/Title"), "language": a.findtext("Language"),
           "mesh": [m.findtext("DescriptorName") for m in med.iter("MeshHeading")], "first_author": a.findtext("AuthorList/Author/LastName"),
           "publication_types": [p.text for p in a.iter("PublicationType")]}
    return make_record("pubmed", qid, {"doi": aids.get("doi"), "pmid": pmid, "pmcid": aids.get("pmc")}, title, abstract, year,
                       "journal-article", raw, pmid, ts)


def run_pubmed(ctx: Ctx, qs: dict) -> list[Query]:
    """esearch with history (retmax=0) for the count, then efetch XML in batches of 500. History paging stops at
    retstart 9998, so a count over 9,999 is re-queued as pubmed_NNa-d by [dp] range, and a sub-range still over
    9,999 is retrieved to 9,999 with the cap recorded. A cached esearch whose efetch pages are not all cached
    is a resume: the WebEnv may have expired, so the esearch is repeated live (Query.stale)."""
    key = cred("NCBI_API_KEY")
    kw, keyp = {"credential": "NCBI_API_KEY" if key else None, "keyed": bool(key)}, {"api_key": key} if key else {}
    per = _NCBI_PAGE if ctx.limit is None else min(_NCBI_PAGE, ctx.limit)
    out, todo = [], [(qid, qs[qid]["string"]) for qid in _ids_for(qs, r"pubmed_\d\d")]
    while todo:
        qid, s = todo.pop(0)
        q = Query(ctx, "pubmed", qid, s, _EU + "esearch.fcgi", "boolean",
                  {"db": "pubmed", "usehistory": "y", "retmax": per, "retmode": "xml", **keyp}, "keyed" if key else "credential-free",
                  # pubmed_NNa-d are the [dp] splits queries/literature.yaml calls conditional-split; recording
                  # them as searches would put the plan and the run at odds over what kind of query they are.
                  role="conditional-split" if re.fullmatch(r"pubmed_\d\d[a-d]", qid) else "search")
        out.append(q)
        while True:  # one pass, restarted by Query.stale when a cached WebEnv leads to uncached pages
            r = q.get(_EU + "esearch.fcgi", {"db": "pubmed", "term": s, "usehistory": "y", "retmax": 0, "retmode": "json", **keyp}, **kw)
            es = q.body(r)
            if not es or "esearchresult" not in es:
                break
            es, q.hits = es["esearchresult"], int(es["esearchresult"].get("count") or 0)
            if q.hits > _NCBI_MAX and qid[-1].isdigit():
                todo.extend((qid + suf, _DP.sub(f'("{lo}/01/01"[dp] : "{hi}/12/31"[dp])', s)) for lo, hi, suf in _DP_SPLITS)
                q.notes.append(f"count > {_NCBI_MAX} (NCBI history limit): re-run as a-d by [dp] range; this row counts only")
                break
            if q.hits > _NCBI_MAX:
                q.cap = _NCBI_MAX
                q.notes.append(f"count {q.hits} > {_NCBI_MAX} in a [dp] sub-range: history paging stops at retstart 9998, retrieval truncated")
            n = min(q.hits, _NCBI_MAX) if ctx.limit is None else min(ctx.limit, q.hits)
            pages = [{"db": "pubmed", "query_key": es.get("querykey"), "WebEnv": es.get("webenv"), "retstart": st, "retmax": min(per, n - st),
                      "retmode": "xml", **keyp} for st in range(0, n, per)]
            if q.stale(r, _EU + "efetch.fcgi", pages, keyed=kw["keyed"]):
                continue
            for p in pages:
                root = q.body(q.get(_EU + "efetch.fcgi", p, **kw), xml=True)
                if root is None or q.take(_pubmed_record(a, qid, q.ts) for a in root.iter("PubmedArticle")):
                    break
            break
    return out


def _epmc_record(it: dict, qid: str, ts: str) -> dict:
    """`abstractText` from resultType=core carries the JATS-derived markup ("<h4>Objectives</h4> ..."), so it is
    stripped the way _cr_record strips Crossref's. Two reasons. The prescreen regexes must not meet a tag
    boundary in the middle of a token (L<sub>5</sub>, <i>in vivo</i>), and sdr.dedup_prescreen merges members by
    keeping the LONGEST abstract, which the markup would make this one for every record Europe PMC shares with
    PubMed - so the marked-up copy, not the clean one, would reach the screening sheet, the charting form's
    verbatim quotes and the manuscript. The raw envelope under raw/epmc/ keeps the original."""
    raw = _pick(it, "id source authorString journalTitle pubType isOpenAccess hasData firstPublicationDate")
    return make_record("epmc", qid, _pick(it, "doi pmid pmcid"), it.get("title"), _TAG.sub(" ", it.get("abstractText") or ""),
                       it.get("pubYear"), "preprint" if it.get("source") == "PPR" else "journal-article", raw,
                       f"{it.get('source')}:{it.get('id')}", ts)


def run_epmc(ctx: Ctx, qs: dict) -> list[Query]:
    """cursorMark paging with resultType=core: lite (information_sources.md L2 as written) carries no abstractText,
    and a record found only here would then be prescreened on its title alone; the departure is noted per query."""
    size, out = 1000 if ctx.limit is None else min(1000, ctx.limit), []
    for qid in _ids_for(qs, r"epmc_\d\d"):
        base = {"query": qs[qid]["string"], "resultType": "core", "format": "json", "pageSize": size}
        q = Query(ctx, "epmc", qid, base["query"], _EPMC, "boolean", base, "credential-free")
        q.notes.append("resultType=core sent where L2 wrote lite: lite has no abstractText and the prescreen reads title + abstract; deviations-log row")
        out.append(q)
        cursor = "*"
        while cursor:
            j = q.body(q.get(_EPMC, {**base, "cursorMark": cursor}))
            if j is None:
                break
            q.hits, items = j.get("hitCount"), j.get("resultList", {}).get("result", [])
            full, nxt = q.take(_epmc_record(it, qid, q.ts) for it in items), j.get("nextCursorMark")
            cursor = nxt if items and nxt and nxt != cursor and not full else None
    return out


def _oa_record(w: dict, qid: str, ts: str) -> dict:
    ids, oa = w.get("ids") or {}, w.get("open_access") or {}
    raw = {"openalex_id": w.get("id"), "type": w.get("type"), "cited_by_count": w.get("cited_by_count"), "is_oa": oa.get("is_oa"),
           "oa_url": oa.get("oa_url"), "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
           "referenced_works": w.get("referenced_works") or [], "authors": [a.get("author", {}).get("display_name") for a in w.get("authorships") or []]}
    abstract = " ".join(x for _, x in sorted((p, t) for t, ps in (w.get("abstract_inverted_index") or {}).items() for p in ps))
    return make_record("openalex", qid, {"doi": w.get("doi"), "pmid": ids.get("pmid"), "pmcid": ids.get("pmcid")},
                       w.get("display_name") or w.get("title"), abstract, w.get("publication_year"), w.get("type"), raw, w.get("id"), ts)


def run_openalex(ctx: Ctx, qs: dict) -> list[Query]:
    """Cursor paging over the boolean `filter`; a 400 on the first page (boolean rejected) re-queues the 35 grid strings as
    openalex_NN_gMM, from information_sources.md section G when the query file has no g01-g35; with neither the query fails."""
    em = contact()
    kw = {"credential": "FLUOROCAP_CONTACT_EMAIL" if em else None, "keyed": bool(em)}
    per, out = 200 if ctx.limit is None else min(200, ctx.limit), []
    todo = [(qid, qs[qid]["string"], "boolean") for qid in _ids_for(qs, r"openalex_0[12]")]
    while todo:
        qid, filt, grammar = todo.pop(0)
        base = {"filter": filt, "per-page": per, "select": _OA_SELECT, **({"mailto": em} if em else {})}
        q = Query(ctx, "openalex", qid, filt, _OA, grammar, base, "keyed" if em else "credential-free")
        out.append(q)
        cursor = "*"
        while cursor:
            r = q.get(_OA, {**base, "cursor": cursor}, **kw)
            if r.status == 400 and q.n_req == 1 and grammar == "boolean":
                gq = qs if _ids_for(qs, r"g\d\d") else load_queries()
                gids = _ids_for(gq, r"g\d\d")
                if not gids:
                    q.failed = True
                    q.notes.append("boolean filter rejected (400) and grid strings unavailable in the query file and information_sources.md: no fallback sent")
                    break
                q.notes.append(f"boolean filter rejected (400): re-run as grid {gids[0]}-{gids[-1]}"
                               f"{' (strings read from information_sources.md)' if gq is not qs else ''}; deviations-log row")
                todo.extend((f"{qid}_{g}", f"{'type:dataset,' if filt.startswith('type:dataset') else ''}title_and_abstract.search:"
                             f"{gq[g]['string']},publication_year:2000-2026", "grid") for g in gids)
                break
            j = q.body(r)
            if j is None:
                break
            q.hits, items = (j.get("meta") or {}).get("count"), j.get("results", [])
            full = q.take(_oa_record(w, qid, q.ts) for w in items)
            cursor = (j.get("meta") or {}).get("next_cursor") if items and not full else None
    return out


def _s2_record(p: dict, qid: str, ts: str) -> dict:
    """`abstract_elided` separates the two ways an S2 record arrives with no abstract. S2 removes the abstract of
    every paper whose publisher forbids redistributing it and says so in openAccessPdf.disclaimer ("the following
    paper fields have been elided by the publisher: {abstract}"); Spine, Eur Spine J and J Neurosurg Spine sit
    with those publishers, so 406 of the 1,000 records on the first s2_01 page carry a title and nothing else,
    353 of them elided and 53 with no abstract anywhere. sdr.dedup_prescreen sends such a record to `uncertain`
    rather than to fail:M/fail:D, and the D-fail audit needs to tell "the publisher withheld it" from "the paper
    has none"."""
    ext, oa = p.get("externalIds") or {}, p.get("openAccessPdf") or {}
    disclaimer = oa.get("disclaimer") or ""
    raw = {**_pick(p, "paperId venue publicationTypes isOpenAccess citationCount"), "openAccessPdf": oa.get("url"),
           "abstract_elided": bool(not p.get("abstract") and "elided" in disclaimer.lower()),
           "disclaimer": disclaimer or None, "authors": [a.get("name") for a in p.get("authors") or []]}
    return make_record("s2", qid, {"doi": ext.get("DOI"), "pmid": ext.get("PubMed"), "pmcid": ext.get("PubMedCentral"), "arxiv": ext.get("ArXiv")},
                       p.get("title"), p.get("abstract"), p.get("year"), "journal-article", raw, p.get("paperId"), ts)


def run_s2(ctx: Ctx, qs: dict) -> list[Query]:
    """Bulk search paged by `token` (redacted in the log, hence also the cache salt); without S2_API_KEY the same endpoint
    at 1 per 5 s. A cached page whose token leads to an uncached page restarts the query live (Query.stale)."""
    key = cred("S2_API_KEY")
    kw = {"headers": {"x-api-key": key} if key else None, "credential": "S2_API_KEY" if key else None, "keyed": bool(key)}
    out = []
    for qid in _ids_for(qs, r"s2_\d\d"):
        base = {"query": qs[qid]["string"], "year": "2000-2026", "fields": _S2_FIELDS}
        q = Query(ctx, "s2", qid, base["query"], _S2, "boolean", base, "keyed" if key else "credential-free")
        out.append(q)
        token, restart = None, True
        while restart:
            restart, token = False, None
            while True:
                r = q.get(_S2, {**base, **({"token": token} if token else {})}, cache_salt=token or "", **kw)
                j = q.body(r)
                if j is None:
                    break
                q.hits, token = j.get("total"), j.get("token")
                if q.take(_s2_record(p, qid, q.ts) for p in j.get("data", [])) or not token or not j.get("data"):
                    break
                if restart := q.stale(r, _S2, [{**base, "token": token}], cache_salt=token, keyed=kw["keyed"]):
                    break
    return out


def _arxiv_record(e, qid: str, ts: str) -> dict:
    t = lambda tag, default=None: e.findtext(tag, default, _NS)  # noqa: E731
    aid = (t("a:id", "") or "").rsplit("/abs/", 1)[-1]
    raw = {"arxiv_id": aid, "published": t("a:published", ""), "updated": t("a:updated", ""), "journal_ref": t("ax:journal_ref"),
           "categories": [c.get("term") for c in e.findall("a:category", _NS)], "authors": [n.text for n in e.findall("a:author/a:name", _NS)]}
    return make_record("arxiv", qid, {"doi": t("ax:doi"), "arxiv": aid}, t("a:title", ""), t("a:summary", ""), (t("a:published", "") or "")[:4],
                       "preprint", raw, aid, ts)


def _ax_total(feed) -> int:
    """<opensearch:totalResults> of an arXiv feed; 0 when the element is absent or does not parse."""
    try:
        return int(feed.findtext("os:totalResults", "0", _NS) or 0)
    except ValueError:
        return 0


def run_arxiv(ctx: Ctx, qs: dict) -> list[Query]:
    """Atom paging by `start`, sorted by submittedDate so pages are stable. An HTTP 200 feed with no entries is
    arXiv's transient-error form, and the session caches it, so the page is refetched up to three times under
    cache_salt retry<n> (the 3 s arXiv interval separates the attempts) and a recovered page's totalResults
    replaces the count the bad feed reported, which is as suspect as its entry list.

    The retry is triggered by the empty feed alone while the query has addressed nothing (start == 0), and NOT
    by start < totalResults: the transient form also comes back all zeros (no entries AND totalResults 0), and
    0 >= 0 made the old guard skip the retry, skip the shortfall branch and end the query with hit_count_api 0,
    n_retrieved 0, cap_hit null and an empty notes string - a silent zero that would wipe the arXiv row of the
    flow without failing the run, and be cached for the rest of that run dir. A page still empty after four
    attempts at start 0 with no count in hand records no count at all (hit_count_api null) and says so in
    `notes`, because a zero that may be a transient error is a number the manuscript would otherwise print;
    further in, or with a count in hand, it is a shortfall with cap_hit = the records addressed so far."""
    per, out = 500 if ctx.limit is None else min(500, ctx.limit), []
    for qid in _ids_for(qs, r"arxiv_\d\d"):
        base = {"search_query": qs[qid]["string"], "max_results": per, "sortBy": "submittedDate", "sortOrder": "ascending"}
        q = Query(ctx, "arxiv", qid, base["search_query"], _AX, "boolean", base, "credential-free")
        out.append(q)
        start = 0
        while True:
            feed = q.body(q.get(_AX, {**base, "start": start}), xml=True)
            if feed is None:
                break
            q.hits, entries = _ax_total(feed), feed.findall("a:entry", _NS)
            for n in range(1, 4):
                if entries or not (start == 0 or start < (q.hits or 0)):
                    break
                feed = q.body(q.get(_AX, {**base, "start": start}, cache_salt=f"retry{n}"), xml=True)
                entries = feed.findall("a:entry", _NS) if feed is not None else []
                if entries:
                    q.hits = _ax_total(feed)
            if not entries and (start == 0 or start < (q.hits or 0)):
                unknown = start == 0 and not q.hits
                q.cap = None if unknown else start
                q.notes.append("empty feed on four attempts at start=0 with totalResults 0 (arXiv transient form); hit count "
                               "not established and nothing retrieved" if unknown else
                               f"shortfall: empty feed at start={start} on four attempts before totalResults={q.hits} "
                               f"(arXiv transient form); truncated at {start}")
                if unknown:
                    q.hits = None
            full, start = q.take(_arxiv_record(e, qid, q.ts) for e in entries), start + per
            if full or not entries or start >= (q.hits or 0):
                break
    return out


def _months(y: int, m: int, until: str):
    """Monthly [from, to] intervals from (y, m) up to the month of `until` (YYYY-MM-DD); nothing after the run date is asked for."""
    last = (int(until[:4]), int(until[5:7]))
    while (y, m) <= last:
        yield [f"{y}-{m:02d}-01", f"{y}-{m:02d}-{monthrange(y, m)[1]:02d}"]
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def _bx_record(it: dict, server: str, qid: str, ts: str) -> dict:
    raw = {"server": server, **_pick(it, "date version category published authors author_corresponding_institution")}
    return make_record("biorxiv", qid, {"doi": it.get("doi")}, it.get("title"), it.get("abstract"), it.get("date"), "preprint", raw, it.get("doi"), ts)


def run_biorxiv(ctx: Ctx, qs: dict) -> list[Query]:
    """No search endpoint: monthly dumps up to the run date are read with cursor step 100 and filtered locally by SPINE_RE,
    MODALITY_RE and DATASET_RE over title + abstract; each DOI kept once at its highest version. The recorded query_string
    is the template (L6: what was sent); the interval bounds and the filter are in `intervals` and `notes`, and
    date_filter `local` says the bounds are the date limit. --limit bounds months and pages per month."""
    out = []
    for server in ("biorxiv", "medrxiv"):
        qid, template = f"{server}_01", _BX.format(server=server, a="<from>", b="<to>", cursor="<cursor>")
        iv = list(_months(*_BX_START[server], ctx.run_date))[:ctx.limit or None]
        q = Query(ctx, "biorxiv", qid, template, template, "dump-filter", {}, "credential-free", intervals=iv, date_filter="local")
        q.notes.append(f"date filter local: monthly interval bounds from {iv[0][0]} to {iv[-1][1]} ({len(iv)} intervals); filter: {_BX_FILTER}")
        out.append(q)
        seen, totals, q.n_fetched = {}, {}, 0
        empty = []            # intervals whose first page answered with no parseable body (2026-09-23: HTTP 200, 0 bytes)
        for a, b in iv:
            cursor = pages = 0
            while True:
                j = q.body(q.get(_BX.format(server=server, a=a, b=b, cursor=cursor)))
                if j is None:
                    if cursor == 0:
                        empty.append(a[:7])
                    break
                totals[a[:7]] = int(((j.get("messages") or [{}])[0]).get("total") or 0)
                for it in j.get("collection", []):
                    q.n_fetched += 1
                    text, d = f"{it.get('title', '')} {it.get('abstract', '')}", (it.get("doi") or "").lower()
                    if d and SPINE_RE.search(text) and MODALITY_RE.search(text) and DATASET_RE.search(text):
                        if d not in seen or int(it.get("version") or 0) >= int(seen[d][0].get("version") or 0):
                            seen[d] = (it, q.ts)
                cursor, pages = cursor + 100, pages + 1
                if not j.get("collection") or cursor >= totals[a[:7]] or (ctx.limit and pages >= ctx.limit):
                    break
        q.hits = sum(totals.values())
        if empty:
            # one summary instead of one "unparseable body" note per month, and never a zero the source did not report:
            # a month that answered with an empty body is a month the source did not answer (check-run `no-answer`)
            q.notes[:] = [n for n in q.notes if not n.startswith("unparseable body")]
            q.notes.append(f"no answer: {len(empty)} of {len(iv)} monthly intervals returned an empty or unparseable "
                           f"body on their first page (first {empty[0]}, last {empty[-1]}); those months are not searched")
            if len(empty) == len(iv):
                q.hits = None
        q.notes.append("per-interval totals: " + json.dumps(totals, sort_keys=True))
        q.take(_bx_record(it, server, qid, ts) for it, ts in seen.values())
    return out


def _cr_record(it: dict, qid: str, ts: str) -> dict:
    issued = ((it.get("issued") or {}).get("date-parts") or [[None]])[0]
    raw = {**_pick(it, "type publisher relation subject URL"), "container": " ".join(it.get("container-title") or []),
           "license": [lic.get("URL") for lic in it.get("license") or []], "first_author": ((it.get("author") or [{}])[0]).get("family")}
    return make_record("crossref", qid, {"doi": it.get("DOI")}, " ".join(it.get("title") or []), _TAG.sub(" ", it.get("abstract") or ""),
                       issued[0] if issued else None, it.get("type"), raw, it.get("DOI"), ts)


def run_crossref(ctx: Ctx, qs: dict) -> list[Query]:
    """query.bibliographic with the deep-paging cursor, capped at 5,000 per string. Pass (a), crossref_01-11, is type:dataset with
    the modality block applied locally (no boolean grammar); pass (b), crossref_12-29, three article types with abstracts, a/b/c on
    a 400. A cached page whose cursor leads to an uncached page restarts the string live (Query.stale)."""
    em = contact()
    kw = {"credential": "FLUOROCAP_CONTACT_EMAIL" if em else None, "keyed": bool(em)}
    rows, out = 1000 if ctx.limit is None else min(1000, ctx.limit), []
    todo = [(qid, qs[qid]["string"], _CR_B_TYPES if int(qid[-2:]) >= 12 else ("dataset",)) for qid in _ids_for(qs, r"crossref_\d\d")]
    while todo:
        qid, s, types = todo.pop(0)
        pass_a = types == ("dataset",)
        filt = ",".join(f"type:{t}" for t in types) + ("," if pass_a else ",has-abstract:true,") + _CR_DATES
        base = {"query.bibliographic": s, "filter": filt, "rows": rows, "select": _CR_SELECT, **({"mailto": em} if em else {})}
        q = Query(ctx, "crossref", qid, s, _CR, "grid", base, "keyed" if em else "credential-free")
        out.append(q)
        restart = True
        while restart:
            cursor, n_seen, restart = "*", 0, False
            while cursor:
                r = q.get(_CR, {**base, "cursor": cursor}, **kw)
                if r.status == 400 and len(types) > 1 and q.n_req == 1:
                    q.notes.append("repeated type filter rejected (400): re-run as a/b/c, one type each; deviations-log row")
                    todo.extend((qid + suf, s, (t,)) for suf, t in zip("abc", _CR_B_TYPES))
                    break
                j = q.body(r)
                if j is None:
                    break
                m = j.get("message") or {}
                q.hits, items = m.get("total-results"), m.get("items", [])
                n_seen += len(items)
                full = q.take(_cr_record(it, qid, q.ts) for it in items
                              if not pass_a or MODALITY_RE.search(_TAG.sub(" ", f"{' '.join(it.get('title') or [])} {it.get('abstract') or ''}")))
                q.cap = _CR_CAP if n_seen >= _CR_CAP and n_seen < (q.hits or 0) else None
                cursor = m.get("next-cursor") if items and not full and q.cap is None and n_seen < (q.hits or 0) else None
                if cursor and (restart := q.stale(r, _CR, [{**base, "cursor": cursor}], keyed=kw["keyed"])):
                    break
        if pass_a:
            q.n_fetched = n_seen
            q.notes.append(f"pass (a): {n_seen} items retrieved, {len(q.records)} kept by local MODALITY_RE (modality filter local)")
    return out


_SP = "https://api.springernature.com/meta/v2/json"
_SP_PAGE = 25  # the basic plan's page ceiling; p=100 is refused as a premium feature (run_springer)


def _sp_record(rec: dict, qid: str, ts: str) -> dict:
    raw = {**_pick(rec, "publicationName contentType publicationDate openaccess"), "urls": [u.get("value") for u in rec.get("url") or []]}
    return make_record("springer", qid, {"doi": rec.get("doi")}, rec.get("title"), rec.get("abstract"), (rec.get("publicationDate") or "")[:4],
                       "journal-article", raw, rec.get("doi") or rec.get("identifier"), ts)


def run_springer(ctx: Ctx, qs: dict) -> list[Query]:
    """S1, the supplementary venue sweep of Scientific Data: `q` carries the journalid and onlinedate constraints
    verbatim, `s` advances by `p` (<= 100) to the reported total. Without SPRINGER_API_META_KEY no request is
    sent and the entry is needs-credentials with zero hits, as information_sources.md S1 says (pubmed_02 covers
    the journal). The API echoes the key in its body; sdr.common redacts it by value before the log and the cache."""
    key, out = cred("SPRINGER_API_META_KEY"), []
    # p=25, not the 100 information_sources.md S1 wrote: on the key's plan p=100 answers 403 "This is a premium
    # feature" whatever the constraints, and p=25 answers 200 with the same total (PROTOCOL.md 19, 2026-09-24).
    per = _SP_PAGE if ctx.limit is None else min(_SP_PAGE, ctx.limit)
    for qid in _ids_for(qs, r"springer_\d\d"):
        base = {"q": qs[qid]["string"], "p": per, **({"api_key": key} if key else {})}
        q = Query(ctx, "springer", qid, base["q"], _SP, "boolean", base, "keyed" if key else "needs-credentials",
                  role="supplementary")  # S1 is the supplementary venue sweep, not one of the seven searches
        out.append(q)
        if not key:
            q.hits = 0
            q.notes.append("SPRINGER_API_META_KEY absent: sweep skipped and recorded needs-credentials (information_sources.md S1)")
            continue
        q.notes.append(f"p={per}: the key's plan refuses p=100 with 403 'premium feature' (deviations log)")
        start = 1
        while True:
            j = q.body(q.get(_SP, {**base, "s": start}, credential="SPRINGER_API_META_KEY", keyed=True))
            if j is None:
                break
            res, recs = (j.get("result") or [{}])[0], j.get("records") or []
            q.hits = int(res.get("total") or 0)
            if q.hits == 0 and start == 1 and not recs:
                q.notes.append("zero hits on the first page: check the constraint names (onlinedatefrom/onlinedateto) before trusting the count")
            full, start = q.take(_sp_record(r, qid, q.ts) for r in recs), start + per
            if full or not recs or start > q.hits:
                break
    return out


RUNNERS = {"pubmed": (run_pubmed, r"pubmed_\d\d", _EU, "NCBI_API_KEY"), "epmc": (run_epmc, r"epmc_\d\d", _EPMC, None),
           "springer": (run_springer, r"springer_\d\d", _SP, "SPRINGER_API_META_KEY"),
           "openalex": (run_openalex, r"openalex_0[12]", _OA, "FLUOROCAP_CONTACT_EMAIL"), "s2": (run_s2, r"s2_\d\d", _S2, "S2_API_KEY"),
           "arxiv": (run_arxiv, r"arxiv_\d\d", _AX, None), "biorxiv": (run_biorxiv, r"(biorxiv|medrxiv)_01", _BX, None),
           "crossref": (run_crossref, r"crossref_\d\d", _CR, "FLUOROCAP_CONTACT_EMAIL")}


def write_source(rd: RunDir, source: str, records: list[dict]) -> int:
    """records/<source>.jsonl, one line per record id; `query_id` is the first (sorted) query that found it, `query_ids` all."""
    by: dict[str, dict] = {}
    for r in sorted(records, key=lambda r: (r["record_id"], r["query_id"])):
        rec = by.setdefault(r["record_id"], {**r, "query_ids": []})
        if r["query_id"] not in rec["query_ids"]:
            rec["query_ids"].append(r["query_id"])
    return write_jsonl(rd.records_file(source), by.values())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m sdr.search_literature", description=__doc__.split("\n")[0])
    add_common_args(ap)
    ap.add_argument("--source", default=",".join(SOURCES), help=f"comma-separated subset of {','.join(SOURCES)}")
    ap.add_argument("--queries", default=None, help="YAML query file instead of information_sources.md (tests)")
    a = ap.parse_args(argv)
    sources = [s.strip() for s in a.source.split(",") if s.strip()]
    if any(s not in RUNNERS for s in sources):
        ap.error(f"unknown source in {sources}; choose from {SOURCES}")
    qs = load_queries(a.queries)
    if a.dry_run:
        for src in sources:
            _, pat, endpoint, name = RUNNERS[src]
            mode = "credential-free" if name is None else ("keyed" if cred(name) else f"credential-free ({name} absent)")
            print(f"[{src}] endpoint {endpoint}  credential mode: {mode}  limit: {a.limit}  coverage: {_meta(src)[0]}")
            for qid in _ids_for(qs, pat):
                print(f"  {qid:14s} {qs[qid]['string'][:110]}{'...' if len(qs[qid]['string']) > 110 else ''}")
        return 0
    rd = init_run_dir(a.run_dir, a.run_date, argv)
    ctx = Ctx(RateLimitedSession(rd, replay=a.replay), rd, a.run_date, a.limit)
    counts = json.loads(counts_path.read_text(encoding="utf-8")) if (counts_path := rd.root / "counts.json").exists() else {}
    failed = []
    for src in sources:
        queries = RUNNERS[src][0](ctx, qs)
        items = [r for q in queries for r in q.records]
        n = write_source(rd, src, items)
        for q in queries:
            rd.update_queries(q.qid, q.entry())
        counts[src] = {"n_records_after_within_source_dedup": n, "n_items": len(items), "queries": {
            q.qid: _pick(q.entry(), "hit_count_api n_retrieved n_requests cap_hit credential_mode notes") for q in queries}}
        dump_json(counts_path, counts)
        print(f"{src}: {len(queries)} queries, {sum(q.n_req for q in queries)} requests, {len(items)} items, "
              f"{n} records after within-source dedup -> {rd.records_file(src).relative_to(rd.root)}")
        for q in queries:
            print(f"  {q.qid:16s} hits {q.hits!s:>8s}  retrieved {len(q.records):6d}  pages {q.n_pages:4d}  {q.mode}"
                  f"{f'  cap {q.cap}' if q.cap else ''}{'  notes: ' + '; '.join(q.notes)[:160] if q.notes else ''}")
        failed += [q.qid for q in queries if q.failed]
    if failed:
        print(f"FAILED (a fallback the protocol names could not be sent): {', '.join(failed)}; see queries.json notes", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
