"""Platform search adapters (information_sources.md R9-R14): Kaggle, Hugging Face Hub,
grand-challenge.org, GitHub, Papers with Code and OpenDataLab.

These six are code and model hosts rather than data archives: their listings are of repositories,
challenges and competitions, a dataset is one kind of item among many, and none of them registers
DOIs or reports a stable total. They share the Run contract of sdr.repo_run with the archive
adapters of sdr.search_repositories (R1-R8) and write the same records/<source>.jsonl, queries.json
and counts.json; `sdr.search_repositories --source all` runs them after the archives.

Live behaviour written into each query's `notes`: Kaggle's list endpoints answer anonymously and
report no total, so hit_count_api is null and the retrieved count stands alone (cap_hit 1000 when
page 50 is still full); Hugging Face reports no total either and pages by the Link header;
grand-challenge answers anonymously; GitHub answers 403 with x-ratelimit-remaining 0 when the
anonymous search quota (10/min) is spent, and the adapter waits to x-ratelimit-reset once and
re-requests under a fresh cache key (never under --replay; the waits are counted); Papers with
Code redirects off-site and its dump host refuses TLS, so it is `retired`; OpenDataLab has no
search API and its three candidate endpoints are probed with t01 before the terms run.

`--limit` is applied after the local modality filter (Hugging Face, OpenDataLab) so a smoke run
reports what passed the filter rather than zero against thousands of hits.

CLI: python -m sdr.search_platforms --run-dir R --run-date D [--source all|kaggle,hf,...]
     [--limit N] [--dry-run] [--replay]
"""
from __future__ import annotations

import argparse
import base64
import gzip
import json
import re
import sys
import time

from sdr.common import RateLimitedSession, Resp, add_common_args, cred, init_run_dir
from sdr.repo_run import MODALITY_RE, SPINE_RE, Run, _first, _family, _get_bytes, _json, _split, _txt, _year, load_repo_queries


# ----------------------------------------------------------------------------- R9 Kaggle, R10 Hugging Face
def src_kaggle(run: Run, Q: dict) -> None:
    u, k = cred("KAGGLE_USERNAME"), cred("KAGGLE_KEY")
    hdr = {"Authorization": "Basic " + base64.b64encode(f"{u}:{k}".encode()).decode()} if u and k else None
    base = "https://www.kaggle.com/api/v1/"
    plan = [(qid, "datasets/list", s) for qid, s in _family(Q, "kaggle_", r"g\d\d")] + [(qid, "competitions/list", s) for qid, s in _family(Q, "kaggle_", r"c\d\d")]
    for qid, path, s in plan:
        n, page, status, cap_hit = 0, 1, None, None
        while True:
            r = run.get("kaggle", qid, base + path, {"search": s, "page": page}, headers=hdr, credential="KAGGLE_KEY" if hdr else None, keyed=bool(hdr))
            j, status = _json(r), r.status
            if not isinstance(j, list):
                break
            for d in run.cap(j):
                ref = d.get("ref") or d.get("url", "").split("kaggle.com/")[-1]
                url = d.get("url") if str(d.get("url", "")).startswith("http") else f"https://www.kaggle.com/{'datasets/' if path.startswith('datasets') else 'competitions/'}{ref}"
                n += run.add("kaggle", qid, ids={"url": url, "repo_id": ref}, title=d.get("title"), desc=_txt(f"{d.get('subtitle') or ''} {d.get('description') or ''}"),
                             year=_year(d.get("lastUpdated") or d.get("enabledDate")), rtype="competition" if path.startswith("comp") else "dataset", native_id=ref,
                             raw={"licenseName": d.get("licenseName"), "totalBytes": d.get("totalBytes"), "usabilityRating": d.get("usabilityRating"), "tags": [t.get("name") if isinstance(t, dict) else t for t in d.get("tags") or []],
                                  "isPrivate": d.get("isPrivate"), "lastUpdated": d.get("lastUpdated"), "downloadCount": d.get("downloadCount"), "voteCount": d.get("voteCount")})
            if page >= 50 and len(j) >= 20:
                cap_hit = 1000  # 50 pages of 20: the list endpoint pages no further
                break
            if len(j) < 20 or run.limit:
                break
            page += 1
        mode = "keyed" if hdr else ("credential-free" if status == 200 else "needs-credentials")
        run.query(qid, "kaggle", base + path, s, "grid", mode, None, n, page, date_filter="local", cap_hit=cap_hit, params={"search": "<string>", "page": 1},
                  notes={"status": status, "total": "API reports no total; n_retrieved is the count of items paged through",
                         "protocol_expectation": "needs-credentials without kaggle.json; the endpoint answered anonymously" if mode == "credential-free" else ""})


def src_hf(run: Run, Q: dict) -> None:
    tok = cred("HF_TOKEN")
    hdr = {"Authorization": f"Bearer {tok}"} if tok else None
    kw = {"headers": hdr, "credential": "HF_TOKEN" if tok else None, "keyed": bool(tok)}
    base, seen = "https://huggingface.co/api/datasets", set()
    qs = [(f"hf_{i:02d}", {"search": Q[f"hf_{i:02d}"]["string"], "limit": 1000, "full": "true"}) for i in range(1, 23)] + \
         [("hf_23", {"filter": Q["hf_23"]["string"], "limit": 1000, "full": "true"})]
    for qid, params0 in qs:
        url, params, n, n_all, pages = base, dict(params0), 0, 0, 0
        while url:
            r = run.get("hf", qid, url, params, **kw)
            pages += 1
            cands = []
            for d in (_json(r) or []):
                n_all += 1
                card = d.get("cardData") or {}
                if MODALITY_RE.search(f"{d['id']} {d.get('description') or ''} {json.dumps(card)} {' '.join(d.get('tags') or [])}"):
                    cands.append(d)
            for d in run.cap(cands):
                card = d.get("cardData") or {}
                det = d if d["id"] in seen else (_json(run.get("hf", qid, f"{base}/{d['id']}", {"blobs": "true"}, **kw)) or d)
                seen.add(d["id"])
                n += run.add("hf", qid, ids={"url": f"https://huggingface.co/datasets/{d['id']}", "repo_id": d["id"]}, title=card.get("pretty_name") or d["id"],
                             desc=_txt(d.get("description")) + (" | tags: " + ", ".join(d.get("tags") or [])), year=_year(d.get("createdAt") or d.get("lastModified")), rtype="dataset",
                             raw={"gated": det.get("gated"), "private": det.get("private"), "license": card.get("license"), "cardData": card, "lastModified": det.get("lastModified"),
                                  "sha": det.get("sha"), "downloads": det.get("downloads"), "siblings": [{"rfilename": s.get("rfilename"), "size": s.get("size"), "sha256": (s.get("lfs") or {}).get("sha256")} for s in det.get("siblings") or []]})
            m = re.search(r"<([^>]+)>;\s*rel=\"next\"", r.headers.get("link", ""))
            url, params = _split(m.group(1)) if m and not run.limit else (None, None)
        run.query(qid, "hf", base, Q[qid]["string"], "grid", "keyed" if tok else "credential-free", None, n, pages, date_filter="local", n_fetched=n_all,
                  params={k: ("<string>" if k in ("search", "filter") else v) for k, v in params0.items()},
                  notes={"total": "API reports no total; paged by the Link header", "local_filter": "MODALITY_RE over id+description+card+tags", "n_before_local_filter": n_all})


# ----------------------------------------------------------------------------- R11 grand-challenge, R12 GitHub
def src_gc(run: Run, Q: dict) -> None:
    qid, base, fallback = "gc_list", "https://grand-challenge.org/api/v1/challenges/", "https://grand-challenge.org/challenges/all-challenges/"
    url, params, items, pages, status = base, {"limit": 100, "offset": 0}, [], 0, None
    while url:
        r = run.get("gc", qid, url, params)
        j, status, pages = _json(r), r.status, pages + 1
        items += (j or {}).get("results", [])
        nxt = (j or {}).get("next")
        url, params = _split(nxt) if nxt else (None, None)
    mode, used, n = "credential-free", base, 0
    if status in (401, 403, 404):
        mode, used = "html-fallback", fallback
        h = run.get("gc", qid, fallback)
        items = [{"slug": s, "title": _txt(t), "description": "", "url": f"https://{s}.grand-challenge.org/"} for s, t in re.findall(r'href="https?://([a-z0-9-]+)\.grand-challenge\.org/?"[^>]*>(.*?)</a>', h.text, re.S)] if h.ok else []
    cands = [c for c in items if SPINE_RE.search(f"{c.get('title', '')} {c.get('description', '')} {c.get('slug', '')}") and MODALITY_RE.search(f"{c.get('title', '')} {c.get('description', '')} {c.get('slug', '')}")]
    for c in run.cap(cands):
        pg = run.get("gc", qid, c.get("url")) if c.get("url") else Resp(0, "", {}, "", False, 0, "no url")
        n += run.add("gc", qid, ids={"url": c.get("url"), "repo_id": c.get("slug")}, title=c.get("title") or c.get("slug"), desc=_txt(c.get("description")) + " | page: " + _txt(pg.text)[:5000],
                     year=_year(c.get("created")), rtype="challenge", native_id=c.get("slug"),
                     raw={"status": c.get("status"), "public": c.get("public"), "publications": c.get("publications"), "created": c.get("created"), "incentives": c.get("incentives"), "page_status": pg.status})
    run.query(qid, "gc", used, Q[qid]["string"], "list", mode, len(items), n, pages, date_filter="local", unit="harvest", n_fetched=len(items),
              params={"limit": 100, "offset": 0} if mode == "credential-free" else {},
              notes={"endpoint_used": used, "api_status": status, "harvest_total": len(items), "n_candidates": len(cands), "local_filter": "SPINE_RE AND MODALITY_RE over title+description+slug"})


def src_github(run: Run, Q: dict) -> None:
    tok = cred("GITHUB_TOKEN")
    hdr = {"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {tok}"} if tok else {})}
    kw = {"headers": hdr, "credential": "GITHUB_TOKEN" if tok else None, "keyed": bool(tok)}
    waits: dict[str, int] = {}

    def get(qid, url, params):
        """GitHub answers 403 (not 429) with x-ratelimit-remaining: 0 when the search quota (10/min anonymous)
        is spent; common does not retry 403, so wait until x-ratelimit-reset once and re-request under a fresh
        cache key (the 403 body was cached). Under --replay the second request is served from that key, no wait."""
        r = run.get("github", qid, url, params, **kw)
        if r.status == 403 and r.headers.get("x-ratelimit-remaining") == "0" and not run.dry_run:
            waits[qid] = waits.get(qid, 0) + 1
            if not run.replay:
                time.sleep(max(1, min(120, int(r.headers.get("x-ratelimit-reset", "0")) - int(time.time()) + 2)))
            r = run.get("github", qid, url, params, cache_salt="after-ratelimit", **kw)
        return r
    ep = "https://api.github.com/search/repositories"
    for i in range(1, 19):
        qid, s, n, page, total = f"github_{i:02d}", Q[f"github_{i:02d}"]["string"], 0, 1, None
        while True:
            j = _json(get(qid, ep, {"q": s, "per_page": 100, "page": page, "sort": "updated"}))
            total = (j or {}).get("total_count", total)
            items = (j or {}).get("items", [])
            for d in run.cap(items):
                n += run.add("github", qid, ids={"url": d.get("html_url"), "repo_id": d.get("full_name")}, title=d.get("full_name"), desc=_txt(f"{d.get('description') or ''} | topics: {', '.join(d.get('topics') or [])}"),
                             year=_year(d.get("created_at")), rtype="repository", native_id=d.get("full_name"),
                             raw={"license": (d.get("license") or {}).get("spdx_id"), "stargazers_count": d.get("stargazers_count"), "topics": d.get("topics"), "pushed_at": d.get("pushed_at"),
                                  "archived": d.get("archived"), "default_branch": d.get("default_branch"), "size_kb": d.get("size"), "fork": d.get("fork")})
            if len(items) < 100 or page >= 10 or run.limit:
                break
            page += 1
        run.query(qid, "github", ep, s, "boolean", "keyed" if tok else "credential-free", total, n, page, date_filter="local", cap_hit=1000 if (total or 0) > 1000 else None,
                  params={"q": "<string>", "per_page": 100, "page": 1, "sort": "updated"}, notes={"ratelimit_waits": waits.get(qid, 0), "wait_rule": "on 403 with x-ratelimit-remaining 0: sleep to x-ratelimit-reset, re-request under cache_salt after-ratelimit"})
    ep = "https://api.github.com/search/code"
    for i in (1, 2):
        qid, s, n = f"github_c{i:02d}", Q[f"github_c{i:02d}"]["string"], 0
        if tok:
            j = _json(get(qid, ep, {"q": s, "per_page": 100}))
            for d in run.cap((j or {}).get("items", [])):
                rp = d.get("repository", {})
                n += run.add("github", qid, ids={"url": rp.get("html_url"), "repo_id": rp.get("full_name")}, title=rp.get("full_name"), desc=_txt(rp.get("description")), year=None,
                             rtype="repository", native_id=rp.get("full_name"), raw={"matched_file": d.get("path"), "code_search": True})
            run.query(qid, "github", ep, s, "boolean", "keyed", (j or {}).get("total_count"), n, 1, date_filter="local",
                      params={"q": "<string>", "per_page": 100}, notes={"ratelimit_waits": waits.get(qid, 0)})
        else:
            run.query(qid, "github", ep, s, "boolean", "needs-credentials", None, 0, 0, date_filter="local",
                      params={"q": "<string>", "per_page": 100}, notes={"reason": "code search requires GITHUB_TOKEN; not sent"})


# ----------------------------------------------------------------------------- R13 Papers with Code, R14 OpenDataLab
def src_pwc(run: Run, Q: dict) -> None:
    statuses, any_json = {}, False
    for i in range(1, 7):
        qid, u = f"pwc_{i:02d}", Q[f"pwc_{i:02d}"]["string"]
        base, params = _split(u)
        r = run.get("pwc", qid, base, params)
        j, n = _json(r), 0
        ok = isinstance(j, dict) and "results" in j
        any_json |= ok
        for d in run.cap((j or {}).get("results", []) if ok else []):
            n += run.add("pwc", qid, ids={"url": d.get("url") or d.get("homepage"), "repo_id": d.get("id")}, title=d.get("name"), desc=_txt(d.get("description")), year=_year(d.get("introduced_date")),
                         rtype="dataset", native_id=d.get("id"), raw=d)
        statuses[qid] = r.status
        run.query(qid, "pwc", base, u, "grid", "credential-free" if ok else "retired", (j or {}).get("count") if ok else None, n, 1, date_filter="local", params=params,
                  notes={"status": r.status, "body_is_api_json": ok, "observed": "" if ok else "non-JSON body: the site redirects off-site (retired 2025)"})
    if any_json:
        return
    dump = Q["pwc_dump"]["string"]
    status, body = _get_bytes(run, "pwc", "pwc_dump", dump)
    n, total = 0, None
    if status == 200 and body:
        try:
            items = json.loads(gzip.decompress(body).decode("utf-8"))
        except (OSError, ValueError):
            items = []
        total = len(items)
        for d in run.cap([d for d in items if SPINE_RE.search(f"{d.get('name', '')} {d.get('full_name', '')} {d.get('description', '')}") and MODALITY_RE.search(f"{d.get('name', '')} {d.get('full_name', '')} {d.get('description', '')}")]):
            n += run.add("pwc", "pwc_dump", ids={"url": d.get("url") or d.get("homepage"), "repo_id": d.get("name")}, title=d.get("full_name") or d.get("name"), desc=_txt(d.get("description")),
                         year=_year(d.get("introduced_date")), rtype="dataset", native_id=d.get("name"), raw={k: d.get(k) for k in ("homepage", "paper", "modalities", "tasks", "languages", "introduced_date")})
    run.query("pwc_dump", "pwc", dump, dump, "dump-filter", "credential-free" if status == 200 else "retired", total, n, 1, date_filter="local", unit="harvest", role="fallback", n_fetched=total or 0,
              notes={"dump_status": status, "api_statuses": statuses, "local_filter": "SPINE_RE AND MODALITY_RE over name+full_name+description", "fallback": "none (no maintained mirror)"})


def src_odl(run: Run, Q: dict) -> None:
    terms = [(f"odl_t{i:02d}", _first(Q, f"odl_t{i:02d}", f"t{i:02d}")) for i in range(1, 9)]
    cands = [(qid, *_split(Q[qid]["string"].replace("<term>", ""))) for qid in ("odl_01", "odl_02", "odl_03") if qid in Q]

    def hits_of(j):
        d = (j or {}).get("data") if isinstance(j, dict) else j
        for key in ("list", "datasets", "items", "records"):
            if isinstance(d, dict) and isinstance(d.get(key), list):
                return d[key]
        return d if isinstance(d, list) else []
    chosen = None
    for qid, base, p in cands:
        key = "keyword" if "keyword" in p else "keywords"
        r = run.get("odl", qid, base, {key: terms[0][1], "pageSize": 100, "pageNo": 1})
        j = _json(r)
        run.query(qid, "odl", base, Q[qid]["string"], "probe", "credential-free" if hits_of(j) else "no-public-api", len(hits_of(j)) if j is not None else None, 0, 1,
                  date_filter="local", role="probe", params={key: "<string>", "pageSize": 100, "pageNo": 1}, notes={"status": r.status, "json": j is not None, "n_hits": len(hits_of(j)), "probe_term": terms[0][1]})
        if hits_of(j) and not chosen:
            chosen = (base, key)
    for qid, t in terms:
        n = 0
        if chosen:
            j = _json(run.get("odl", qid, chosen[0], {chosen[1]: t, "pageSize": 100, "pageNo": 1}))
            items, mode, params = hits_of(j), "credential-free", {chosen[1]: "<string>", "pageSize": 100, "pageNo": 1}
        else:
            h = run.get("odl", qid, "https://opendatalab.com/", {"keywords": t})
            items = [{"name": s, "url": f"https://opendatalab.com/{o}/{s}"} for o, s in dict.fromkeys(re.findall(r'href="/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+)"', h.text)) if o not in ("datasets", "static", "assets")] if h.ok else []
            mode, params = ("html-fallback" if items else "no-public-api"), {"keywords": "<string>"}
        n_all, keep = len(items), []
        for d in items:
            name = d.get("name") or d.get("displayName")
            intro = d.get("introduction") if isinstance(d.get("introduction"), str) else json.dumps(d.get("introduction") or "")
            if MODALITY_RE.search(f"{name} {intro}") or not chosen:
                keep.append((d, name, intro))
        for d, name, intro in run.cap(keep):
            n += run.add("odl", qid, ids={"url": d.get("url") or f"https://opendatalab.com/{name}", "repo_id": name}, title=name, desc=_txt(intro), year=None, rtype="dataset", native_id=name, raw=d)
        run.query(qid, "odl", chosen[0] if chosen else "https://opendatalab.com/?keywords=<string>", t, "grid", mode, None, n, 1, date_filter="local", params=params, n_fetched=n_all,
                  notes={"total": "API reports no total; n_fetched is the count of items on the first page", "local_filter": "MODALITY_RE over name+introduction" if chosen else "none (HTML fallback carries no description)", "n_before_local_filter": n_all,
                         "observed": "no search endpoint answers with a dataset list; the HTML page is client-rendered (no slugs)" if not chosen and not items else ""})


SOURCES = {"kaggle": src_kaggle, "hf": src_hf, "gc": src_gc, "github": src_github, "pwc": src_pwc, "odl": src_odl}


def main(argv=None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.search_platforms", description=__doc__.split("\n")[0]))
    ap.add_argument("--source", default="all", help="comma-separated source names, or all")
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
    run.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
