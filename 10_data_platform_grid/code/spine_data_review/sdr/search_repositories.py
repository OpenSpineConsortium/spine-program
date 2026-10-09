"""Data-archive search adapters (information_sources.md R1-R8): Zenodo, Figshare, Dryad, OSF,
Mendeley Data, DataCite, PhysioNet and TCIA/NBIA; and the entry point of the whole repository search.

One function per source, all writing the record shape of PROTOCOL.md section 15
({record_id, source, query_id, retrieved_at, ids, title, abstract_or_description, year, type, raw},
plus `query_ids`, every query of the source that returned the item) to records/<source>.jsonl,
one queries.json entry per query_id with the fields listed under "What is recorded for every
query", and a per-source summary in <run-dir>/counts.json (merged, so a literature module can
co-write it). The twenty repository adapters are split by what they list, at the 450-line rule:
this module holds the archives (deposits with DOIs and reported totals), sdr.search_platforms the
code and model hosts (R9-R14), sdr.search_figure_routes the figure and non-English routes (F1,
F4-F8) and the mention harvests; sdr.repo_run holds the shared `Run` state and the reasoning
behind `unit`, `n_requests` and the binary cache. `--source all` here runs every adapter in one
process, archives first and the mention harvests last, so the harvest scans every record in memory.

The strings come from queries/repositories.yaml through repo_run.load_repo_queries; nothing here
types a query, and `query_string` is the YAML string character for character (PIPELINE.md stage 1).
Where a source has no query interface (PhysioNet, TCIA) the whole listing is harvested and filtered
by SPINE_RE and MODALITY_RE; `endpoint` and `notes.endpoint_used` record what was actually
requested (the REST list, or the HTML fallback when the REST list answered 404) and `unit` is
`harvest`, so the listing size is never added to record hits.

Live behaviour decides several routes and each fact is written into the query's `notes` so the
deviations log can quote the run: Zenodo's anonymous API rejects size=100; Figshare answers 500
above about eleven terms and reports no total; PhysioNet's REST list is 404 and the HTML index is
parsed; Mendeley's front end reports no total, so only the DataCite prefix route counts. Caps are
recorded where they can bite: Zenodo per year range above 10,000. `--limit` is applied after the
local modality filter (OSF, DataCite prefix route), so a smoke run reports what passed the filter.

CLI: python -m sdr.search_repositories --run-dir R --run-date D [--source all|zenodo,hf,...]
     [--limit N] [--dry-run] [--replay]
"""
from __future__ import annotations

import argparse
import json
import re
import sys

from sdr.common import RateLimitedSession, add_common_args, cred, init_run_dir
from sdr.repo_run import (MODALITY_RE, SPINE_RE, Run, _chunks, _family, _first, _get_bytes, _json,  # noqa: F401 (re-exported for the tests)
                          _split, _top_clauses, _txt, _year, load_repo_queries, write_not_run)
from sdr.search_platforms import SOURCES as PLATFORM_SOURCES, src_kaggle  # noqa: F401 (src_kaggle: the fixture test reaches it here)

TCIA_BODY_RE = re.compile(r"(?i)spine|vertebr|sacr|lumbar|thorac|cervic|whole ?body|^[ctl]\s*-?\s*spine$")
TCIA_MODS = ("CT", "CR", "DX", "RF", "XA", "OT")


# ----------------------------------------------------------------------------- R1 Zenodo
def src_zenodo(run: Run, Q: dict) -> None:
    base, notes = "https://zenodo.org/api/records", {}
    for i, clause in enumerate(_top_clauses(Q["zenodo_01"]["string"]), 1):
        j = _json(run.get("zenodo", "zenodo_01", base, {"q": clause, "size": 1}))
        notes[f"clause_{i}_hits"] = (j or {}).get("hits", {}).get("total") if j else None
    for qid in ("zenodo_01", "zenodo_02"):
        s, ranges = Q[qid]["string"], [None]
        j = _json(run.get("zenodo", qid, base, {"q": s, "size": 1}))
        total = (j or {}).get("hits", {}).get("total", 0) if j else 0
        if total > 10000:
            ranges = [f"[{y}-01-01 TO {y}-12-31]" for y in range(2000, 2027)]
        n, pages, range_totals = 0, 0, {}
        for rng in ranges:
            qs = s.replace("[2000-01-01 TO 2026-12-31]", rng) if rng else s
            page, got = 1, 0
            while True:
                j = _json(run.get("zenodo", qid, base, {"q": qs, "size": 25, "page": page, "sort": "bestmatch"}))  # anonymous cap is 25 (400 above it)
                hits = (j or {}).get("hits", {}).get("hits", []) if j else []
                pages += 1
                range_totals[rng or "all"] = (j or {}).get("hits", {}).get("total", 0) if j else 0
                for h in run.cap(hits):
                    m = h.get("metadata", {})
                    n += run.add("zenodo", qid, ids={"doi": h.get("doi"), "url": h.get("links", {}).get("self_html"), "repo_id": str(h.get("id"))},
                                 title=m.get("title"), desc=_txt(m.get("description")), year=_year(m.get("publication_date")),
                                 rtype=(m.get("resource_type") or {}).get("type"), native_id=h.get("id"),
                                 raw={"conceptdoi": h.get("conceptdoi"), "access_right": m.get("access_right"), "license": (m.get("license") or {}).get("id"),
                                      "resource_type": m.get("resource_type"), "publication_date": m.get("publication_date"),
                                      "files": [{"key": f.get("key"), "size": f.get("size"), "checksum": f.get("checksum")} for f in h.get("files", [])],
                                      "related_identifiers": m.get("related_identifiers"), "creators": [c.get("name") for c in m.get("creators", [])]})
                    got += 1
                if not hits or got >= min(10000, range_totals[rng or "all"]) or run.limit:
                    break
                page += 1
        capped = sorted(k for k, v in range_totals.items() if v > 10000)  # a range above the window cap loses its tail
        run.query(qid, "zenodo", base, s, "boolean", "credential-free", total, n, pages, date_filter="api", cap_hit=10000 if capped else None,
                  notes={**(notes if qid == "zenodo_01" else {}), "year_split": len(ranges) > 1, "ranges_over_cap": capped,
                         "page_size": "25: the anonymous API rejects size=100 (deviation from the written 100)"},
                  params={"q": "<string>", "size": 25, "page": 1, "sort": "bestmatch"})


# ----------------------------------------------------------------------------- R2 Figshare
def src_figshare(run: Run, Q: dict) -> None:
    url, hdr = "https://api.figshare.com/v2/articles/search", {"Content-Type": "application/json"}
    body0 = json.loads(Q["figshare_01"]["string"])
    chk = run.get("figshare", "figshare_01", url, method="POST", headers=hdr, data=json.dumps({"search_for": ':description: "lumbar spine"', "page_size": 1}))
    notes = {"phrase_check_hits": len(_json(chk) or []) if chk.ok else None, "phrase_check_status": chk.status}
    # Observed on the run: the API answers 500 "UnknownFigcoreException" to any search_for with more than about
    # eleven terms (eleven pass, fourteen fail), so the verbatim body is sent once and, on a 500, the same boolean is
    # executed as the union of (spine chunk) AND (modality chunk) sub-queries, which OR-distribution makes equivalent.
    spine, mod = body0["search_for"][1:-1].split(") AND (")
    term = re.compile(r':(?:title|description): (?:"[^"]+"|\S+)')
    chunks = [(a, b) for a in _chunks(term.findall(spine), 5) for b in _chunks(term.findall(mod), 6)]
    for qid in ("figshare_01", "figshare_02"):
        body = {k: v for k, v in body0.items() if not (qid == "figshare_02" and k == "item_type")}
        first = run.get("figshare", qid, url, method="POST", headers=hdr, data=json.dumps({**body, "page": 1}, sort_keys=True))
        if first.status == 500:  # the answer this request was sent to get: it selects the split, it does not truncate the search
            run.expect_failure(qid, "the verbatim body is sent once to test the ~11-term ceiling; a 500 selects the equivalent union of sub-queries")
        forms = [body["search_for"]] if first.status != 500 else [f"({' OR '.join(a)}) AND ({' OR '.join(b)})" for a, b in chunks]
        n, n_seen, pages = 0, 0, 0
        for form in forms:
            page = 1
            while True:
                items = _json(run.get("figshare", qid, url, method="POST", headers=hdr, data=json.dumps({**body, "search_for": form, "page": page}, sort_keys=True))) or []
                pages += 1
                for it in run.cap(items):
                    d = _json(run.get("figshare", qid, f"https://api.figshare.com/v2/articles/{it['id']}")) or {}
                    n_seen += 1
                    n += run.add("figshare", qid, ids={"doi": d.get("doi") or it.get("doi"), "url": d.get("url_public_html") or it.get("url_public_html"), "repo_id": str(it["id"])},
                                 title=it.get("title"), desc=_txt(d.get("description")), year=_year(it.get("published_date")), rtype=it.get("defined_type_name"),
                                 native_id=it["id"], raw={"license": d.get("license"), "is_public": d.get("is_public"), "is_embargoed": d.get("is_embargoed"),
                                                          "published_date": it.get("published_date"), "handle": it.get("handle"),
                                                          "files": [{"name": f.get("name"), "size": f.get("size"), "computed_md5": f.get("computed_md5"), "download_url": f.get("download_url")} for f in d.get("files", [])]})
                if len(items) < body["page_size"] or run.limit:
                    break
                page += 1
            if run.limit and n_seen >= run.limit:
                break
        # grammar stays the planned "boolean" (the language of the body); the split into sub-queries is the form the
        # run had to use and is stated in notes.executed_as, so Appendix A never prints a grammar the protocol has no word for.
        run.query(qid, "figshare", url, Q[qid]["string"] if qid in Q else json.dumps(body), "boolean", "credential-free", None, n, pages, method="POST",
                  date_filter="api",
                  params={"page_size": body.get("page_size"), "order": body.get("order")},
                  notes={**notes, "total": "API reports no total; paged until a short page", "n_seen_across_sub_queries": n_seen, "verbatim_body_status": first.status,
                         "executed_as": "verbatim body" if len(forms) == 1 else f"union of {len(forms)} sub-queries (spine chunks of 5 x modality chunks of 6), equivalent by OR-distribution; the verbatim body answers 500 above ~11 terms"})


# ----------------------------------------------------------------------------- R3 Dryad, R4 OSF
def src_dryad(run: Run, Q: dict) -> None:
    for qid, s in _family(Q, "dryad_", r"g\d\d"):
        n, page, total = 0, 1, None
        while True:
            j = _json(run.get("dryad", qid, "https://datadryad.org/api/v2/search", {"q": s, "per_page": 100, "page": page}))
            items = (j or {}).get("_embedded", {}).get("stash:datasets", [])
            total = (j or {}).get("total", total)
            for d in run.cap(items):
                n += run.add("dryad", qid, ids={"doi": d.get("identifier"), "url": d.get("sharingLink"), "repo_id": str(d.get("id"))}, title=d.get("title"),
                             desc=_txt(d.get("abstract")), year=_year(d.get("publicationDate")), rtype="dataset", native_id=d.get("id"),
                             raw={"license": d.get("license"), "storageSize": d.get("storageSize"), "keywords": d.get("keywords"),
                                  "relatedPublicationISSN": d.get("relatedPublicationISSN"), "versionNumber": d.get("versionNumber"), "curationStatus": d.get("curationStatus")})
            if not j or not (j.get("_links", {}).get("next")) or run.limit:
                break
            page += 1
        run.query(qid, "dryad", "https://datadryad.org/api/v2/search", s, "grid", "credential-free", total, n, page, date_filter="local",
                  params={"q": "<string>", "per_page": 100, "page": 1})


def src_osf(run: Run, Q: dict) -> None:
    tok = cred("OSF_TOKEN")
    hdr = {"Authorization": f"Bearer {tok}"} if tok else None
    for kind, off, extra in (("nodes", 0, {"filter[public]": "true"}), ("registrations", 8, {}), ("preprints", 16, {})):
        for i in range(1, 9):
            qid, base = f"osf_{off + i:02d}", f"https://api.osf.io/v2/{kind}/"
            t = _first(Q, qid, f"t{i:02d}")
            url, params, n, n_all, pages, total = base, {"filter[title][icontains]": t, "page[size]": 100, **extra}, 0, 0, 0, None
            while url:
                j = _json(run.get("osf", qid, url, params, headers=hdr, credential="OSF_TOKEN" if tok else None, keyed=bool(tok)))
                pages += 1
                total = (j or {}).get("links", {}).get("meta", {}).get("total", total)
                cands = []
                for d in (j or {}).get("data", []):
                    a = d.get("attributes", {})
                    n_all += 1
                    if MODALITY_RE.search(f"{a.get('title', '')} {a.get('description', '')} {' '.join(a.get('tags') or [])}"):
                        cands.append(d)
                for d in run.cap(cands):
                    a, l = d.get("attributes", {}), d.get("links", {})
                    n += run.add("osf", qid, ids={"doi": a.get("doi") or l.get("preprint_doi"), "url": l.get("html"), "repo_id": d.get("id")}, title=a.get("title"),
                                 desc=_txt(a.get("description")), year=_year(a.get("date_created") or a.get("date_published")), rtype=kind, native_id=d.get("id"),
                                 raw={"tags": a.get("tags"), "category": a.get("category"), "date_created": a.get("date_created"), "public": a.get("public"),
                                      "node_license": a.get("node_license"), "license_id": ((d.get("relationships") or {}).get("license") or {}).get("data")})
                nxt = (j or {}).get("links", {}).get("next")
                url, params = _split(nxt) if nxt and not run.limit else (None, None)
            run.query(qid, "osf", base, t, "grid", "keyed" if tok else "credential-free", total, n, pages, date_filter="local", n_fetched=n_all,
                      params={"filter[title][icontains]": "<string>", "page[size]": 100, **extra},
                      notes={"local_filter": "MODALITY_RE over title+description+tags", "n_before_local_filter": n_all})


# ----------------------------------------------------------------------------- R5 Mendeley, R6 DataCite
def _datacite(run: Run, qid, s, params, local=False) -> None:
    base = "https://api.datacite.org/dois"
    url, p, n, n_all, pages, total = base, {"query": s, "page[size]": 1000, "page[cursor]": 1, **params}, 0, 0, 0, None
    while url:
        j = _json(run.get("datacite", qid, url, p))
        pages += 1
        total = (j or {}).get("meta", {}).get("total", total)
        cands = []
        for d in (j or {}).get("data", []):
            a = d.get("attributes", {})
            title = " ".join(t.get("title", "") for t in a.get("titles", []))
            desc = _txt(" ".join(x.get("description", "") for x in a.get("descriptions", [])))
            n_all += 1
            if not local or MODALITY_RE.search(f"{title} {desc} {' '.join(x.get('subject', '') for x in a.get('subjects', []))}"):
                cands.append((a, title, desc))
        for a, title, desc in run.cap(cands):
            n += run.add("datacite", qid, ids={"doi": a.get("doi"), "url": a.get("url"), "repo_id": a.get("doi")}, title=title, desc=desc,
                         year=a.get("publicationYear"), rtype=(a.get("types") or {}).get("resourceTypeGeneral"),
                         raw={"publisher": a.get("publisher"), "rightsList": a.get("rightsList"), "relatedIdentifiers": a.get("relatedIdentifiers"),
                              "sizes": a.get("sizes"), "formats": a.get("formats"), "version": a.get("version"), "container": a.get("container"),
                              "subjects": [x.get("subject") for x in a.get("subjects", [])], "types": a.get("types")})
        nxt = (j or {}).get("links", {}).get("next")
        url, p = _split(nxt) if nxt and not run.limit else (None, None)
    # date_filter="api": the string carries publicationYear:[2000 TO 2026] on all four ids. The `local` flag
    # selects the MODALITY_RE filter, which is not a date filter; it travels in the notes, never as date_filter.
    run.query(qid, "datacite", base, s, "boolean", "credential-free", total, n, pages, date_filter="api", n_fetched=n_all,
              params={"query": "<string>", "page[size]": 1000, "page[cursor]": 1, **params},
              notes={"local_filter": "MODALITY_RE", "n_before_local_filter": n_all} if local else None)


def src_datacite(run: Run, Q: dict) -> None:
    s = Q["datacite_01"]["string"]
    _datacite(run, "datacite_01", s, {"resource-type-id": "dataset"})
    _datacite(run, "datacite_02", s, {"resource-type-id": "image"})
    _datacite(run, "datacite_03", Q["datacite_03"]["string"] if "datacite_03" in Q else f"{s} AND types.resourceTypeGeneral:(Dataset OR Image OR Collection)", {})


def src_mendeley(run: Run, Q: dict) -> None:
    url = "https://data.mendeley.com/public-api/datasets/search"
    for i in range(1, 9):
        qid = f"mendeley_{i:02d}"
        t = _first(Q, qid, f"t{i:02d}")
        r = run.get("mendeley", qid, url, {"search": t, "limit": 50})
        j = _json(r)
        items = j if isinstance(j, list) else (j or {}).get("results") or (j or {}).get("datasets") or []
        items = items if isinstance(items, list) else []
        n = 0
        for d in run.cap(items):
            n += run.add("mendeley", qid, ids={"doi": d.get("doi"), "url": d.get("url") or d.get("links", {}).get("html"), "repo_id": d.get("id")},
                         title=d.get("name") or d.get("title"), desc=_txt(d.get("description")), year=_year(d.get("publishedDate") or d.get("publishDate")),
                         rtype="dataset", native_id=d.get("id"), raw=d)
        run.query(qid, "mendeley", url, t, "grid", "mendeley-via-datacite", None, n, 1, date_filter="local", params={"search": "<string>", "limit": 50},
                  notes={"front_end_status": r.status, "front_end_json": j is not None, "n_items_returned": len(items),
                         "total": "API reports no total (undocumented front end)", "recorded_route": "datacite_04 (prefix 10.17632)"})
    if "datacite_04" not in run.done:
        _datacite(run, "datacite_04", Q["datacite_04"]["string"], {"prefix": "10.17632"}, local=True)


# ----------------------------------------------------------------------------- R7 PhysioNet, R8 TCIA
def src_physionet(run: Run, Q: dict) -> None:
    qid, api, fallback = "physionet_list", "https://physionet.org/rest/database-list/", "https://physionet.org/content/"
    r = run.get("physionet", qid, api)
    projects, mode, pages, notes, used = [], "credential-free", 1, {"rest_status": r.status}, api
    j = _json(r)
    if isinstance(j, list):
        projects = [(p.get("slug"), p.get("version"), p.get("title", ""), p.get("abstract", "")) for p in j]
    else:
        mode, used, page, last, seen = "html-fallback", fallback, 1, None, set()
        while True:  # the index serves its last page for any page number beyond it, so stop at the pager's maximum
            h = run.get("physionet", qid, fallback, {"page": page})
            blocks = re.findall(r'<h2><a href="/content/([^/]+)/([^/]+)/">(.*?)</a></h2>(.*?)(?=<h2>|<nav|</main)', h.text, re.S) if h.ok else []
            new = [(s, v, _txt(t), _txt(re.sub(r'<p class="text-muted[^"]*">.*?</p>', " ", b, flags=re.S))) for s, v, t, b in blocks if s not in seen]
            seen.update(s for s, *_ in new)
            projects += new
            last = last or max([int(x) for x in re.findall(r"[?&]page=(\d+)", h.text)] or [1])
            pages = page
            if not new or page >= last:
                break
            page += 1
    cands = [p for p in projects if SPINE_RE.search(f"{p[2]} {p[3]}") and MODALITY_RE.search(f"{p[2]} {p[3]}")]
    n = 0
    for slug, ver, title, desc in run.cap(cands):
        url = f"https://physionet.org/content/{slug}/{ver}/"
        pg = run.get("physionet", qid, url)
        m = re.search(r"(Open Access|Credentialed Access|Restricted Access|Contributor Review)", pg.text) if pg.ok else None
        pub = re.search(r"Published:?\s*([A-Za-z.]+ \d+, \d{4})", pg.text) if pg.ok else None
        n += run.add("physionet", qid, ids={"url": url, "repo_id": slug}, title=title, desc=desc, year=_year(pub.group(1) if pub else None),
                     rtype="database", raw={"version": ver, "access_policy": m.group(1) if m else "unknown", "page_status": pg.status})
    run.query(qid, "physionet", used, Q[qid]["string"], "list", mode, len(projects), n, pages, date_filter="local", unit="harvest", n_fetched=len(projects),
              params={"page": 1} if mode == "html-fallback" else {},
              notes={**notes, "endpoint_used": used, "local_filter": "SPINE_RE AND MODALITY_RE over title+abstract", "harvest_total": len(projects), "n_candidates": len(cands)})


def src_tcia(run: Run, Q: dict) -> None:
    qid, nbia = "tcia_list", "https://services.cancerimagingarchive.net/nbia-api/services/v1/"
    cols = [c.get("Collection") for c in (_json(run.get("tcia", qid, nbia + "getCollectionValues")) or [])]
    page, meta = 1, {}
    while True:  # collection descriptions, DOIs and licences from the site API (verified live)
        j = _json(run.get("tcia", qid, "https://www.cancerimagingarchive.net/api/v1/collections", {"per_page": 100, "page": page}))
        for c in (j if isinstance(j, list) else []):
            key = re.sub(r"[^a-z0-9]", "", _txt((c.get("title") or {}).get("rendered", "")).lower())
            meta[key] = {"slug": c.get("slug"), "link": c.get("link"), "doi": c.get("collection_doi"), "date": c.get("date"),
                         "abstract": _txt(c.get("collection_abstract") or c.get("collection_summary") or c.get("detailed_description")),
                         "accessibility": c.get("collection_page_accessibility"), "status": c.get("collection_status")}
        page += 1
        if not isinstance(j, list) or len(j) < 100 or run.limit:
            break
    n, cand = 0, 0
    for col in cols:  # --limit counts candidates (the filter needs two requests per collection, so it cannot run first)
        if run.limit and cand >= run.limit:
            break
        parts = [b.get("BodyPartExamined") for b in (_json(run.get("tcia", qid, nbia + "getBodyPartValues", {"Collection": col})) or []) if b.get("BodyPartExamined")]
        mods = [m.get("Modality") for m in (_json(run.get("tcia", qid, nbia + "getModalityValues", {"Collection": col})) or []) if m.get("Modality")]
        m = meta.get(re.sub(r"[^a-z0-9]", "", col.lower()), {})
        by_body = any(TCIA_BODY_RE.search(p) for p in parts) and any(x in TCIA_MODS for x in mods)
        by_desc = bool(SPINE_RE.search(f"{col} {m.get('abstract', '')}"))
        if not (by_body or by_desc):
            continue
        cand += 1
        pats, series = {}, {}
        for mod in [x for x in mods if x in TCIA_MODS]:
            pats[mod] = len(_json(run.get("tcia", qid, nbia + "getPatientByCollectionAndModality", {"Collection": col, "Modality": mod})) or [])
            series[mod] = len(_json(run.get("tcia", qid, nbia + "getSeries", {"Collection": col, "Modality": mod})) or [])
        url = m.get("link") or f"https://www.cancerimagingarchive.net/collection/{col.lower()}/"
        n += run.add("tcia", qid, ids={"doi": m.get("doi"), "url": url, "repo_id": col}, title=col, desc=m.get("abstract", ""), year=_year(m.get("date")),
                     rtype="collection", native_id=col, raw={"body_parts": parts, "modalities": mods, "n_patients_by_modality": pats, "n_series_by_modality": series,
                                                             "candidate_rule": "body-part" if by_body else "description", "accessibility": m.get("accessibility"), "status": m.get("status")})
    run.query(qid, "tcia", nbia + "getCollectionValues", Q[qid]["string"], "list", "credential-free", len(cols), n, 1, date_filter="local", unit="harvest", n_fetched=len(cols),
              notes={"endpoint_used": nbia + "getCollectionValues", "harvest_total": len(cols), "n_candidates": cand, "site_api_collections": len(meta),
                     "rule": "body part + modality, or SPINE_RE on the site-API abstract"})


SOURCES = {"zenodo": src_zenodo, "figshare": src_figshare, "dryad": src_dryad, "osf": src_osf, "mendeley": src_mendeley, "datacite": src_datacite,
           "physionet": src_physionet, "tcia": src_tcia}


def main(argv=None) -> int:
    from sdr.search_figure_routes import SOURCES as FIGURE_SOURCES  # F1, F4-F8, then the mention harvests last
    all_sources = {**SOURCES, **PLATFORM_SOURCES, **FIGURE_SOURCES}
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.search_repositories", description=__doc__.split("\n")[0]))
    ap.add_argument("--source", default="all", help="comma-separated source names, or all (R1-R8, R9-R14, the figure routes, mentions last)")
    a = ap.parse_args(argv)
    names = list(all_sources) if a.source == "all" else [s.strip() for s in a.source.split(",")]
    bad = [s for s in names if s not in all_sources]
    if bad:
        sys.exit(f"unknown source(s): {bad}; known: {sorted(all_sources)}")
    Q = load_repo_queries()
    if a.dry_run:
        run = Run(None, None, a.run_date, a.limit, True)
    else:
        rd = init_run_dir(a.run_dir, a.run_date, argv)
        run = Run(rd, RateLimitedSession(rd, replay=a.replay), a.run_date, a.limit, False)
    for name in names:
        print(f"== {name}")
        all_sources[name](run, Q)
    if a.source == "all":  # YAML ids whose source has no adapter (MultiCaRe, Open-PMC-18M) are recorded as not-run
        print("== not-run (yaml ids without an adapter)")
        write_not_run(run, Q)
    run.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
