"""Figure-route and non-English journal adapters (information_sources.md F1, F4-F8) and the two
mention harvests (R9 kaggle_mention, R10 hf_mention).

These routes reach datasets through figures and captions rather than deposit metadata: NLM Open-i
returns figure records (PMCID, figure id, caption) that are enriched to articles through Europe PMC;
Wikimedia Commons returns files whose categories become candidate collections; J-STAGE, KoreaMed
Synapse, SciELO and Redalyc are the non-English literature routes the FluoroCap harvest used. They
share the Run contract of sdr.repo_run with the R1-R14 adapters of sdr.search_repositories and
write the same records/<source>.jsonl, queries.json and counts.json.

What these sources count is not what a repository counts, and the `unit` of every hit count says
so: Open-i hits are figures (each string runs twice, it=xg and it=c, so a figure can be counted
twice), Commons hits are files, and only the journal routes count records. counts.json sums
hit_count_api_total over unit=records alone.

Identity of an article without a DOI is its native id (SciELO PID, Redalyc article id), never its
page URL: those sites address an article only through a query string (`sci_arttext&pid=`,
`articulo.oa?id=`), and sdr.ids.norm_url drops the query, so a URL identity merged every article
of one host into one record. The page URL is kept in `raw.url`.

Live behaviour written into each query's `notes`: SciELO passes only with browser-like headers;
KoreaMed Synapse serves a JavaScript shell with no data endpoint; Redalyc's page calls a JSON
service that the adapter calls directly; Open-i's Europe PMC enrichment needs resultType=core
because lite carries no abstract.

The mention harvests (`mentions`) run last. They scan every record of the run for a Kaggle or
Hugging Face dataset URL: the records still in memory when `--source all` runs everything in one
process, plus every records/<source>.jsonl on disk that is not in memory (a literature run made
earlier). Both lists are recorded in the query's notes, so an under-count is visible.

CLI: python -m sdr.search_figure_routes --run-dir R --run-date D [--source all|openi,commons,...]
     [--limit N] [--dry-run] [--replay]
"""
from __future__ import annotations

import argparse
import html as htmlmod
import json
import re
import sys

from sdr.common import RateLimitedSession, add_common_args, init_run_dir, read_jsonl
from sdr.repo_run import MODALITY_RE, SPINE_RE, Run, _family, _json, _txt, _year, load_repo_queries, write_not_run

BROWSER_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                   "Accept": "text/html,application/xhtml+xml", "Accept-Language": "en-US,en;q=0.9"}


# ----------------------------------------------------------------------------- F1 NLM Open-i
def src_openi(run: Run, Q: dict) -> None:
    base, arts = "https://openi.nlm.nih.gov/api/search", {}
    for i in range(1, 19):
        # One queries.json entry per yaml id: the two image-type runs (it=xg, it=c) share it, n_requests counts both,
        # hit_count_api is the sum of the two totals and notes carry each variant's total (queries/literature.yaml, openi_NN.paging).
        qid, s, n, pages, per_it = f"openi_{i:02d}", Q[f"openi_{i:02d}"]["string"], 0, 0, {}
        for it in ("xg", "c"):
            m, total = 1, None
            while True:
                r = run.get("openi", qid, base, {"query": s, "it": it, "coll": "pmc", "m": m, "n": m + 29})
                j = _json(r)
                if r.ok and j is None:
                    # Open-i answered HTTP 200 with its HTML "There seems to be an error" page on the review run (PROTOCOL.md
                    # 19, 2026-09-24). The loop reads it as end-of-results like any unparseable body, so it is counted as a
                    # failed request here; otherwise a query cut at page 2 of 93 is written as complete.
                    run.note_status(qid, 0, f"HTTP {r.status} with a non-JSON body (the service's HTML error page)")
                total, pages = (j or {}).get("total", total), pages + 1
                for d in run.cap((j or {}).get("list", [])):
                    pmcid = d.get("pmcid") or d.get("uid")
                    a = arts.setdefault(f"PMC{str(pmcid).replace('PMC', '')}", {"pmid": d.get("pmid"), "title": d.get("title"), "journal": d.get("journal_title"),
                                                                                 "year": (d.get("journal_date") or {}).get("year"), "figures": [], "queries": set()})
                    a["figures"].append({"id": (d.get("image") or {}).get("id"), "caption": _txt((d.get("image") or {}).get("caption"))[:1000], "type": it})
                    a["queries"].add(qid)
                    n += 1
                m += 30
                if not j or m > (total or 0) or run.limit:
                    break
            per_it[it] = total
        hits = sum(t for t in per_it.values() if t is not None) if any(t is not None for t in per_it.values()) else None
        run.query(qid, "openi", base, s, "grid", "credential-free", hits, n, pages, date_filter="local", unit="figures",
                  params={"query": "<string>", "it": "xg | c", "coll": "pmc", "m": 1, "n": 30},
                  notes={"unit": "figures; records are distinct articles by PMCID after openi_enrich", "hit_count_by_it": per_it})
    epmc, n_enriched, n_new = "https://www.ebi.ac.uk/europepmc/webservices/rest/search", 0, 0
    for pmcid, a in sorted(arts.items()):
        # resultType=core, not the protocol's lite: lite carries no abstractText (observed on the run; deviations-log row)
        j = _json(run.get("openi", "openi_enrich", epmc, {"query": f"PMCID:{pmcid}", "resultType": "core", "format": "json"}))
        hit = ((j or {}).get("resultList", {}).get("result") or [{}])[0]
        n_enriched += bool(hit)
        caps = " ".join(f"[{f['id']}] {f['caption']}" for f in a["figures"])
        for q in sorted(a["queries"]):
            n_new += run.add("openi", q, ids={"doi": hit.get("doi"), "pmid": hit.get("pmid") or a["pmid"], "pmcid": pmcid}, title=hit.get("title") or a["title"],
                             desc=f"{_txt(hit.get('abstractText'))} Figure captions: {caps}".strip(), year=_year(hit.get("pubYear") or a["year"]), rtype="article",
                             raw={"journal": hit.get("journalTitle") or a["journal"], "figures": a["figures"], "n_figures": len(a["figures"]), "epmc_found": bool(hit), "isOpenAccess": hit.get("isOpenAccess")})
    run.query("openi_enrich", "openi", epmc, "PMCID:<pmcid>", "enrich", "credential-free", len(arts), n_new, len(arts),
              date_filter="local", role="enrich", params={"query": "PMCID:<pmcid>", "resultType": "core", "format": "json"},
              notes={"n_distinct_pmcids": len(arts), "n_found_in_epmc": n_enriched, "n_figures_total": sum(len(a["figures"]) for a in arts.values()),
                     "resultType": "core (lite, as written, returns no abstractText)"})


# ----------------------------------------------------------------------------- F4 Wikimedia Commons
def src_commons(run: Run, Q: dict) -> None:
    api, cats = "https://commons.wikimedia.org/w/api.php", {}  # category -> {file title -> info}

    def file_info(qid, titles):
        out = {}
        for k in range(0, len(titles), 50):
            j = _json(run.get("commons", qid, api, {"action": "query", "prop": "imageinfo|categories", "iiprop": "url|size|mime|sha1|extmetadata",
                                                     "iiextmetadatafilter": "LicenseShortName|ImageDescription", "cllimit": "max", "titles": "|".join(titles[k:k + 50]), "format": "json", "maxlag": 5}))
            for p in ((j or {}).get("query", {}).get("pages") or {}).values():
                ii = (p.get("imageinfo") or [{}])[0]
                em = ii.get("extmetadata") or {}
                out[p.get("title")] = {"mime": ii.get("mime"), "sha1": ii.get("sha1"), "size": ii.get("size"), "licence": (em.get("LicenseShortName") or {}).get("value"),
                                       "description": _txt((em.get("ImageDescription") or {}).get("value"))[:500], "categories": [c.get("title") for c in p.get("categories") or []]}
        return out
    for qid, s in _family(Q, "commons_", r"g\d\d"):
        s = s if s.endswith(" filetype:bitmap") else s + " filetype:bitmap"  # the YAML carries the suffix; a markdown primitive does not
        off, titles, total, pages = 0, [], None, 0
        while True:
            j = _json(run.get("commons", qid, api, {"action": "query", "list": "search", "srsearch": s, "srnamespace": 6, "srlimit": 50, "sroffset": off, "format": "json", "maxlag": 5}))
            total, pages = (j or {}).get("query", {}).get("searchinfo", {}).get("totalhits", total), pages + 1
            titles += [x["title"] for x in (j or {}).get("query", {}).get("search", [])]
            nxt = (j or {}).get("continue", {}).get("sroffset")
            if nxt is None or run.limit:
                break
            off = nxt
        n_seen, titles = len(titles), run.cap(titles)
        for t, info in file_info(qid, titles).items():
            for c in info["categories"]:
                cats.setdefault(c, {"files": {}, "queries": set()})["files"][t] = info
                cats[c]["queries"].add(qid)
        run.query(qid, "commons", api, s, "grid", "credential-free", total, len(titles), pages, date_filter="local", unit="files", n_fetched=n_seen,
                  params={"action": "query", "list": "search", "srsearch": "<string>", "srnamespace": 6, "srlimit": 50, "sroffset": 0, "format": "json", "maxlag": 5},
                  notes={"unit": "files; records are candidate categories", "warnings": (j or {}).get("warnings")})
    for i in range(1, 8):
        qid, cat, cont, titles, pages = f"commons_c{i:02d}", Q[f"commons_c{i:02d}"]["string"], None, [], 0
        info = _json(run.get("commons", qid, api, {"action": "query", "titles": cat, "format": "json", "maxlag": 5})) or {}
        exists = not any("missing" in p for p in (info.get("query", {}).get("pages") or {}).values())
        while True:
            p = {"action": "query", "list": "categorymembers", "cmtitle": cat, "cmtype": "file", "cmlimit": 500, "format": "json", "maxlag": 5, **({"cmcontinue": cont} if cont else {})}
            j = _json(run.get("commons", qid, api, p))
            pages += 1
            titles += [x["title"] for x in (j or {}).get("query", {}).get("categorymembers", [])]
            cont = (j or {}).get("continue", {}).get("cmcontinue")
            if not cont or run.limit:
                break
        titles = run.cap(titles)
        for t, info in file_info(qid, titles).items():
            cats.setdefault(cat, {"files": {}, "queries": set()})["files"][t] = info
            cats[cat]["queries"].add(qid)
        run.query(qid, "commons", api, cat, "list", "credential-free", len(titles), len(titles), pages, date_filter="local", unit="files",
                  params={"action": "query", "list": "categorymembers", "cmtitle": "<string>", "cmtype": "file", "cmlimit": 500, "format": "json", "maxlag": 5},
                  notes={"category_exists": exists, "unit": "files in the category", "observed": "" if exists else "category name does not resolve (deviations-log row: correct the name)"})
    n = 0
    for cat, d in sorted(cats.items()):
        ok = [t for t, f in d["files"].items() if str(f.get("mime", "")).startswith("image/") and f.get("licence") and SPINE_RE.search(f"{cat} {f['description']}") and MODALITY_RE.search(f"{cat} {f['description']}")]
        if len(ok) < 10 and not (run.limit and ok):
            continue
        lic = {}
        for t in ok:
            lic[d["files"][t]["licence"]] = lic.get(d["files"][t]["licence"], 0) + 1
        for q in sorted(d["queries"]):
            run.add("commons", q, ids={"url": "https://commons.wikimedia.org/wiki/" + cat.replace(" ", "_")}, title=cat, desc=f"{cat}. Sample descriptions: " + " | ".join(d["files"][t]["description"] for t in ok[:5]),
                    year=None, rtype="category", raw={"n_files_seen": len(d["files"]), "n_qualifying": len(ok), "licences": lic, "sample_files": ok[:20], "rule": ">=10 image/* files with a licence and SPINE_RE+MODALITY_RE"})
        n += 1
    print(f"  commons: {len(cats)} categories seen, {n} candidate categories")


# ----------------------------------------------------------------------------- F5-F8 non-English journal routes
def src_jstage(run: Run, Q: dict) -> None:
    base = "https://api.jstage.jst.go.jp/searchapi/do"
    for i in range(1, 15):
        qid, s, start, n, total, pages = f"jstage_{i:02d}", Q[f"jstage_{i:02d}"]["string"], 1, 0, None, 0
        while True:
            r = run.get("jstage", qid, base, {"service": 3, "text": s, "pubyearfrom": 2000, "pubyearto": 2026, "count": 1000, "start": start})
            pages += 1
            m = re.search(r"<opensearch:totalResults>(\d+)</opensearch:totalResults>", r.text)
            total = int(m.group(1)) if m else total
            entries = re.findall(r"<entry>(.*?)</entry>", r.text, re.S) if r.ok else []
            for e in run.cap(entries):
                e = e.replace("<![CDATA[", "").replace("]]>", "")  # _txt would otherwise eat a CDATA block as one tag

                def f(tag, block=e):
                    mm = re.search(rf"<{tag}>\s*(.*?)\s*</{tag}>", block, re.S)
                    return htmlmod.unescape(mm.group(1).strip()) if mm else ""
                at, mt = f("article_title"), f("material_title")
                ten, tja, link = f("en", at), f("ja", at), f("en", f("article_link"))
                n += run.add("jstage", qid, ids={"doi": f("prism:doi"), "url": link or f("id")}, title=ten or tja or f("title"), desc=tja if ten else "",
                             year=_year(f("pubyear")), rtype="article", raw={"journal": f("cdjournal"), "issn": f("prism:issn"), "material_title": f("en", mt) or f("ja", mt), "title_ja": tja})
            if not entries or start + 1000 > (total or 0) or run.limit:
                break
            start += 1000
        run.query(qid, "jstage", base, s, "grid", "credential-free", total, n, pages, date_filter="api",
                  params={"service": 3, "text": "<string>", "pubyearfrom": 2000, "pubyearto": 2026, "count": 1000, "start": 1})


def src_koreamed(run: Run, Q: dict) -> None:
    search, n_enrich, n_pages_ok = "https://synapse.koreamed.org/search", 0, 0
    for i in range(1, 10):
        qid, s, n = f"koreamed_{i:02d}", Q[f"koreamed_{i:02d}"]["string"], 0
        r = run.get("koreamed", qid, search, {"q": s, "page": 1})
        arts = sorted(set(re.findall(r'href="(https?://synapse\.koreamed\.org/articles/\d+)"', r.text)))
        st = {"synapse_status": r.status}
        if not arts:
            r2 = run.get("koreamed", qid, "https://koreamed.org/search/basic.php", {"Query": s})
            st["basic_php_status"] = r2.status
            if not r2.ok:
                r2 = run.get("koreamed", qid, "https://www.koreamed.org/SearchBasic.php", {"Query": s})
                st["searchbasic_status"] = r2.status
            arts = sorted(set(re.findall(r'href="(https?://synapse\.koreamed\.org/articles/\d+)"', r2.text))) if r2.ok else []
        for u in run.cap(arts):
            pg = run.get("koreamed", "koreamed_enrich", u)
            n_enrich, n_pages_ok = n_enrich + 1, n_pages_ok + pg.ok
            meta = dict(re.findall(r'<meta name="citation_(title|abstract|doi|pmid|publication_date)" content="([^"]*)"', pg.text)) if pg.ok else {}
            n += run.add("koreamed", qid, ids={"doi": meta.get("doi"), "pmid": meta.get("pmid"), "url": u}, title=htmlmod.unescape(meta.get("title", "")), desc=htmlmod.unescape(meta.get("abstract", "")),
                         year=_year(meta.get("publication_date")), rtype="article", raw={"page_status": pg.status})
        run.query(qid, "koreamed", search, s, "grid", "html-fallback" if arts else "no-public-api", None, n, 1, date_filter="local",
                  params={"q": "<string>", "page": 1}, n_fetched=len(arts),
                  notes={**st, "n_article_links": len(arts),
                         "total": "no API total; n_fetched is the count of article links on the first page", "observed": "" if arts else "search page is a JavaScript shell with no article links and no data endpoint; basic.php is 404"})
    run.query("koreamed_enrich", "koreamed", "https://synapse.koreamed.org/articles/<article_id>", "https://synapse.koreamed.org/articles/<article_id>", "enrich",
              "html-fallback" if n_pages_ok else "no-public-api", n_enrich, n_pages_ok, n_enrich, role="enrich", date_filter="local",
              notes={"n_article_pages_fetched": n_enrich, "n_pages_ok": n_pages_ok, "parsed": "citation_title/abstract/doi/pmid/publication_date meta tags"})


def src_scielo(run: Run, Q: dict) -> None:
    base = "https://search.scielo.org/"
    for i in range(1, 12):
        qid, raw = f"scielo_{i:02d}", Q[f"scielo_{i:02d}"]["string"]
        s = re.split(r"\s{2,}lang=", raw)[0].strip()  # the markdown grid line carries `lang=`; the YAML splits it into `language`
        lang = Q[qid].get("language") or (re.search(r"lang=(\w+)", raw) or [None, "en"])[1]
        frm, n, total, pages, notes = 1, 0, None, 0, {}
        while True:
            r = run.get("scielo", qid, base, {"q": s, "lang": lang, "output": "site", "format": "summary", "count": 50, "from": frm}, headers=BROWSER_HEADERS)
            pages += 1
            m = re.search(r'id="TotalHits">(\d+)', r.text)
            total = int(m.group(1)) if m else total
            items = re.findall(r'<div id="([A-Za-z0-9-]+)" class="item">(.*?)(?=<div id="[A-Za-z0-9-]+" class="item">|<div class="pagination|$)', r.text, re.S) if r.ok else []
            for pid, blk in run.cap(items):
                t = re.search(r'<strong class="title"[^>]*>(.*?)</strong>', blk, re.S)
                u = re.search(r'href="(https?://[^"]*sci_arttext[^"]*)"', blk)
                d = re.search(r"doi\.org/(10\.[^\s\"<]+)", blk)
                # identity is the DOI, else the PID: the article URL carries the PID only in its query string, which
                # sdr.ids.norm_url drops, so passing it as `url` would merge every SciELO article of one host into one record
                n += run.add("scielo", qid, ids={"doi": d.group(1) if d else None, "repo_id": pid}, title=_txt(t.group(1)) if t else pid,
                             desc=_txt(re.search(r'class="abstract[^"]*"[^>]*>(.*?)</div>', blk, re.S).group(1)) if re.search(r'class="abstract[^"]*"', blk) else "", year=_year(pid[10:14]),
                             rtype="article", native_id=pid, raw={"pid": pid, "lang": lang, "url": htmlmod.unescape(u.group(1)) if u else None})
            if not items or frm + 50 > (total or 0) or run.limit:
                break
            frm += 50
        if i <= 3 and not run.dry_run:  # boolean check: the bare first term alone
            rb = run.get("scielo", qid, base, {"q": s.split()[0], "lang": lang, "output": "site", "format": "summary", "count": 1, "from": 1}, headers=BROWSER_HEADERS)
            mb = re.search(r'id="TotalHits">(\d+)', rb.text)
            notes = {"bare_first_term_hits": int(mb.group(1)) if mb else None, "boolean_honoured": (int(mb.group(1)) != total) if mb and total is not None else None}
        run.query(qid, "scielo", base, s, "boolean" if i <= 3 else "grid", "html-fallback" if r.ok else "no-public-api", total, n, pages, date_filter="local",
                  params={"q": "<string>", "lang": lang, "output": "site", "format": "summary", "count": 50, "from": 1},
                  notes={**notes, "status": r.status, "client": "browser-like headers (the portal's bot shield refuses the review User-Agent)"})


def src_redalyc(run: Run, Q: dict) -> None:
    page_url = "https://www.redalyc.org/busquedaArticuloFiltros.oa"
    for i in range(1, 10):
        qid, s, n = f"redalyc_{i:02d}", Q[f"redalyc_{i:02d}"]["string"], 0
        h = run.get("redalyc", qid, page_url, {"q": s})
        ids = sorted(set(re.findall(r"articulo\.oa\?id=(\d+)", h.text))) if h.ok else []
        # total stays None on the HTML route: `ids` are anchors counted here, and Run.query's `hits` is the
        # API's own total or nothing. The count travels as n_fetched and in the notes.
        items, total, mode, ep, params = [{"id": a} for a in ids], None, "html-fallback", page_url, {"q": "<string>"}
        if not ids:  # the page is an AngularJS app; its data call (js/busquedaArticulo.js, servicioRedalyc) is called directly
            ep, params = f"https://www.redalyc.org/service/r2020/getArticles/{s}/1/50/1/0/", {}
            j = _json(run.get("redalyc", qid, ep))
            res = (j or {}).get("resultados")
            items = res if isinstance(res, list) else (list(res.values()) if isinstance(res, dict) else [])
            total, mode = (j or {}).get("totalResultados"), "html-fallback" if j is not None and items else "no-public-api"
        for d in run.cap(items):
            aid = str(d.get("id") or d.get("idArticulo") or "")
            # identity is the DOI, else the article id: articulo.oa?id=<aid> carries the id in its query string, which norm_url drops
            n += run.add("redalyc", qid, ids={"doi": d.get("doi"), "repo_id": aid}, title=_txt(d.get("titulo") or d.get("title") or aid),
                         desc=_txt(d.get("resumen") or d.get("abstract")), year=_year(d.get("anio") or d.get("fecha") or d.get("year")), rtype="article", native_id=aid,
                         raw={**d, "url": f"https://www.redalyc.org/articulo.oa?id={aid}"})
        run.query(qid, "redalyc", ep, s, "grid", mode, total, n, 1, date_filter="local", params=params, n_fetched=len(items),
                  notes={"page_status": h.status, "html_ids": len(ids),
                         "total": "HTML route: the article anchors are counted here; the API reports no total, so hits is null and the count travels as n_fetched" if ids else "", "data_endpoint": "service/r2020/getArticles/<q>/<page>/<size>/1/<order> discovered in js/busquedaArticulo.js" if not ids else "",
                         "observed": "" if items or ids else "the page is client-rendered (no article ids); the service answers JSON with totalResultados 0 for every string, single common words included"})


# ----------------------------------------------------------------------------- mention harvests (run last)
def src_mentions(run: Run, Q: dict) -> None:
    pats = {"kaggle-mention": (re.compile(Q["kaggle_mention"]["string"]), "https://www."), "hf-mention": (re.compile(Q["hf_mention"]["string"]), "https://")}
    found = {k: {} for k in pats}
    in_memory = sorted(s for s in run.records if s not in pats)
    files = sorted(p for p in run.rd.records.glob("*.jsonl") if p.stem not in pats and p.stem not in in_memory) if run.rd else []

    def scan(rec):
        text = f"{rec.get('title', '')} {rec.get('abstract_or_description', '')} {json.dumps(rec.get('raw', {}), ensure_ascii=False)}"
        for src, (pat, pre) in pats.items():
            for m in pat.finditer(text):
                found[src].setdefault(pre + m.group(0).rstrip("/."), set()).add(rec["record_id"])  # the pattern admits a sentence-ending dot
    for s in in_memory:
        for rec in run.records[s].values():
            scan(rec)
    for p in files:
        for rec in read_jsonl(p):
            scan(rec)
    for src, hits in found.items():
        qid, n = src.replace("-", "_"), 0
        for url, rids in sorted(hits.items()):
            n += run.add(src, qid, ids={"url": url, "repo_id": url.split("/", 3)[-1]}, title=url.split("/", 3)[-1], desc="", year=None, rtype="dataset", raw={"found_in": sorted(rids)})
        run.query(qid, src, "local", pats[src][0].pattern, "regex", "credential-free", len(hits), n, 0, role="supplement", unit="harvest", date_filter="local",
                  notes={"scanned_in_memory_sources": in_memory, "scanned_files": [p.name for p in files],
                         "n_records_scanned": sum(len(run.records[s]) for s in in_memory) + sum(1 for p in files for _ in read_jsonl(p))})


SOURCES = {"openi": src_openi, "commons": src_commons, "jstage": src_jstage, "koreamed": src_koreamed, "scielo": src_scielo, "redalyc": src_redalyc, "mentions": src_mentions}


def main(argv=None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.search_figure_routes", description=__doc__.split("\n")[0]))
    ap.add_argument("--source", default="all", help="comma-separated source names, or all (mentions runs last)")
    a = ap.parse_args(argv)
    names = list(SOURCES) if a.source == "all" else [s.strip() for s in a.source.split(",")]
    bad = [s for s in names if s not in SOURCES]
    if bad:
        sys.exit(f"unknown source(s): {bad}; known: {sorted(SOURCES)}")
    Q = load_repo_queries()
    if a.dry_run:
        run = Run(None, None, a.run_date, a.limit, True)
    else:
        rd = init_run_dir(a.run_dir, a.run_date, argv)
        run = Run(rd, RateLimitedSession(rd, replay=a.replay), a.run_date, a.limit, False)
    for name in names:
        print(f"== {name}")
        SOURCES[name](run, Q)
    if a.source == "all":  # the YAML ids with no adapter (MultiCaRe, Open-PMC-18M: charting-time routes) are written as not-run
        print("== not-run (yaml ids without an adapter)")
        write_not_run(run, Q)
    run.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
