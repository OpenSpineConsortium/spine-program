"""Availability probe (PROTOCOL.md section 10, RQ5): how each charted dataset can be obtained today.

WHY A PROBE AND NOT A READING. A paper that says "publicly available" was true on the day it was
written. The review's access route is an observation made by code on a recorded date, twice at
least 48 hours apart, so that "described as public" and "actually downloads" (SAP A3.2) can be
compared, and every classification traces to an HTTP status, a repository API field or a
sentence of visible page text, with the rule id (P1-P25) that fired.

WHAT IT DOES. For every charting record (charting/datasets/<id>.json; or, before any record
exists, --from-known-items over screen/known_items.csv) it takes `access_url`, routes it through
the section-10 host table by DOI prefix or host, asks the repository's own API where the table
names one (Zenodo, Figshare, Dryad, OSF, DataCite plus Mendeley's public API, NBIA for TCIA,
Hugging Face, GitHub; PhysioNet's policy string), and otherwise runs the generic method: HEAD,
then GET with `Range: bytes=0-65535`, redirects followed hop by hop (at most five), nothing
beyond the first 64 KiB of any landing page or file, no dataset file ever downloaded. Rules are
applied in the protocol's order (P1-P15, P20, P16-P19, P21-P25; first match wins) and one entry
in the shape of charting_schema.json#/definitions/probe is written per dataset per run.

INTERPRETATIONS the protocol leaves open, each a row of the deviations log (section 19) and
visible in the entry's `evidence`: (a) P22's login-URL test is a whole-token match on the final
URL (host, path, query), and fires only after a redirect or with WWW-Authenticate, so `auth` in
`/authors-dataset/` is not a login page; (b) P16-P19 read 2xx HTML only: a 401/403 page's text
never classifies, P22 does; (c) DUA_RE/REG_RE/REQ_RE/PAY_RE match case-insensitively; (d) a
site root (path `/`, no query) that is not a DOI is `unresolved` (P21) rather than classified
from homepage text; (e) repository API metadata (Zenodo, Hugging Face, GitHub, OSF, DataCite,
Mendeley JSON) is read whole, exempt from the 64 KiB cap that binds pages and files; (f) a probe
that fails (transport error, persistent 429/5xx) is cached like any other so `--replay`
reproduces the failure; a fresh observation needs a fresh run dir; (g) Mendeley's file evidence
comes from its public API listing, the landing page being a script shell with no anchors;
(h) GitHub credential-free runs one request per minute (the 60/h anonymous ceiling) and an
exhausted ceiling is `unresolved` (P21) with the reset time, never a silent fall-through to the
generic method. Persistent 429/5xx and other statuses P22/P23 do not name are `unresolved`; a
repository API state that does not decide falls through to the generic method on the landing
page; one dataset whose probe raises is written as `unresolved` (P21) with the error and the
run continues.

OUTPUTS. charting/probes/<id>.json accumulates {probes[] by date, file_probes[] (the ranged GET
of file_url_probed or of the first file an API listed: the Q7 evidence the probe object has no
field for), host_type, agreement (the two-probe rule of section 10)}; <run-dir>/probes/<run-date>.jsonl
holds this run's row per dataset and <run-dir>/probes/summary.json the counts (`n_requests` =
request-log lines this invocation, cache hits included; `n_live_requests` = network calls). With
--apply the probe list, host_type and, when two probes agree on a route-valued class, access_route
and access_route_rule are written into the charting record (a `verifier:` rule is never overwritten).

Run: python -m sdr.availability --run-dir runs/2026-09-21 --run-date 2026-09-21 [--apply]
     python -m sdr.availability --run-dir R --run-date D --from-known-items --limit 3
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html as html_lib
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote, urljoin, urlsplit

import requests

from sdr.common import (RETRY_STATUSES, TIMEOUT_S, RateLimitedSession, ReplayMiss, Resp, RunDir, add_common_args,
                        append_jsonl, cred, dump_json, init_run_dir, now_iso, redact_text, review_root)

# ----------------------------------------------------------------------------- protocol constants (section 10)
DUA_RE = re.compile(r"data[- ]use (agreement|policy)|data (usage|access|sharing) agreement|\bDUA\b|end[- ]user (licen[cs]e )?agreement|must (sign|complete) .{0,40}(agreement|application)|apply for access|access request form|credential(ed|ing) access", re.I)
REG_RE = re.compile(r"log ?in to download|account (is )?required|register(ed)? (user|account)|create (an|a free) account|registration (is )?required", re.I)
REQ_RE = re.compile(r"contact the (corresponding )?authors?|(up)?on (reasonable )?request|available (from the authors )?on request|e-?mail .{0,60} to (obtain|request)", re.I)
PAY_RE = re.compile(r"\bpurchase\b|\bpricing\b|add to cart|buy now|subscription required|\blicen[cs]e fee\b|commercial licen[cs]e", re.I)
NEAR_RE = re.compile(r"download|data|access|files", re.I)
# Whole-token form of the protocol's `login|signin|sign-in|auth`, matched on host+path+query (interpretation a).
LOGIN_RE = re.compile(r"(^|[/?&#=_.-])(login|signin|sign-in|auth)([/?&#=_.-]|$)", re.I)
EMBARGO_RE = re.compile(r"\bembargo", re.I)
ALLOW_CT = frozenset({"application/zip", "application/gzip", "application/x-gzip", "application/x-tar",
                      "application/x-7z-compressed", "application/dicom", "application/octet-stream"})
DATA_EXT_RE = re.compile(r"\.(dcm|nii|nii\.gz|nrrd|mha|tiff?|png|jpe?g|zip|tar|gz|tgz|7z)$", re.I)
ANCHOR_RE = re.compile(r"\.(zip|tar|gz|tgz|7z|nii|nii\.gz|dcm)(\?.*)?$", re.I)
ROUTES = ("open-download", "registration", "data-use-agreement", "request-to-authors", "unavailable", "commercial")
# Host table: (host regex, route, host_type). Kaggle competitions are re-typed challenge-platform below.
HOSTS = ((r"(^|\.)zenodo\.org$", "zenodo", "repository-api"), (r"(^|\.)figshare\.com$", "figshare", "repository-api"),
         (r"^datadryad\.org$", "dryad", "repository-api"), (r"(^|\.)osf\.io$", "osf", "repository-api"),
         (r"^data\.mendeley\.com$", "mendeley", "repository-api"), (r"(^|\.)physionet\.org$", "physionet", "repository-api"),
         (r"(^|\.)cancerimagingarchive\.net$", "tcia", "repository-api"), (r"^huggingface\.co$", "hf", "repository-api"),
         (r"(^|\.)kaggle\.com$", "kaggle", "repository-api"), (r"(^|\.)grand-challenge\.org$", "gc", "challenge-platform"),
         (r"^github\.com$", "github", "repository-api"), (r"(^|\.)opendatalab\.com$", "odl", "challenge-platform"))
DOI_PREFIX = {"10.5281": "zenodo", "10.6084": "figshare", "10.5061": "dryad", "10.17605": "osf", "10.17632": "mendeley",
              "10.13026": "physionet", "10.7937": "tcia"}
CLOUD_RE = re.compile(r"drive\.google\.com|dropbox\.com|1drv\.ms|onedrive\.live\.com|sharepoint\.com|(^|\.)box\.com$|pan\.baidu\.com|github\.io$|sites\.google\.com")
INST_RE = re.compile(r"\.(edu|gov|ac\.[a-z]{2}|edu\.[a-z]{2})$|\.uni-[a-z0-9-]+\.[a-z]{2}$|university|hospital|clinic")
NBIA = "https://services.cancerimagingarchive.net/nbia-api/services/v1"
MENDELEY = "https://data.mendeley.com/public-api/datasets"
CAP = 65536
GH_FREE_INTERVAL_S = 60.0  # one live GitHub call per minute credential-free: the 60/h anonymous ceiling (interpretation h)


def host_type(url: str) -> str:
    """Section-10 host table value for `url`: repository-api / challenge-platform / institutional /
    personal-or-cloud-drive / unknown. Filled by code; SAP A3.1's stratifier."""
    host = urlsplit(url).netloc.lower()
    if (doi_in(url) or "").split("/")[0] in DOI_PREFIX:
        return "repository-api"
    for pat, route, ht in HOSTS:
        if re.search(pat, host):
            return "challenge-platform" if route == "kaggle" and re.search(r"/(competitions|c)/", url) else ht
    return "personal-or-cloud-drive" if CLOUD_RE.search(host) else "institutional" if INST_RE.search(host) else "unknown"


def doi_in(url: str) -> str | None:
    """The DOI carried by a doi.org, dx.doi.org, hdl.handle.net or zenodo.org/doi/ link, else None."""
    p = urlsplit(url)
    if re.search(r"(^|\.)(doi\.org|hdl\.handle\.net)$", p.netloc.lower()) or p.path.startswith("/doi/"):
        m = re.search(r"10\.\d{4,9}/[^\s?#]+", p.path)
        return m.group(0).rstrip(".,;)") if m else None
    return None


def visible_text(body: str) -> str:
    """First 64 KiB of HTML with script/style/nav/header/footer/aside removed, tags stripped,
    entities decoded and whitespace collapsed (section 10, 'Visible text')."""
    s = re.sub(r"(?is)<(script|style|nav|header|footer|aside)\b.*?</\1\s*>", " ", body)
    return re.sub(r"\s+", " ", html_lib.unescape(re.sub(r"(?s)<[^>]+>", " ", s))).strip()


def near(pat: re.Pattern, text: str) -> str | None:
    """A match of `pat` that lies within 200 characters of NEAR_RE, else None (P17, P18)."""
    for m in pat.finditer(text):
        if NEAR_RE.search(text[max(0, m.start() - 200):m.end() + 200]):
            return m.group(0)
    return None


def text_rule(text: str) -> tuple[str, str, str] | None:
    """P16-P19 over visible text in protocol order: (rule, class, evidence) for the first that fires, else
    None. P17 and P18 count only within 200 characters of NEAR_RE; P16 and P19 anywhere."""
    for pat, rule, cls, prox in ((DUA_RE, "P16", "data-use-agreement", False), (PAY_RE, "P17", "commercial", True),
                                 (REG_RE, "P18", "registration", True), (REQ_RE, "P19", "request-to-authors", False)):
        m = near(pat, text) if prox else (pat.search(text).group(0) if pat.search(text) else None)
        if m:
            i = text.lower().find(m.lower())
            return rule, cls, f"{rule} matched '{m}' in: ...{text[max(0, i - 120):i + 160]}..."
    return None


def _len(h: dict) -> int | None:
    """Total size from Content-Range (a 206 answer) else Content-Length; None when neither is given."""
    m = re.search(r"/(\d+)$", h.get("content-range") or "")
    cl = h.get("content-length") or ""
    return int(m.group(1)) if m else int(cl) if cl.isdigit() else None


def _ct(h: dict) -> str | None:
    """Content-Type as recorded: the first value when a server sent the header twice (requests joins them)."""
    v = h.get("content-type")
    return v.split(",")[0].strip() if v else None


def _loc(url: str) -> str:
    """host + path + query of `url`: what LOGIN_RE is matched against."""
    p = urlsplit(url)
    return p.netloc + p.path + (f"?{p.query}" if p.query else "")


def _js(r: Resp):
    try:
        return r.json() if r.ok else None
    except ValueError:
        return None


def _nlines(p: Path) -> int:
    return sum(1 for _ in open(p, encoding="utf-8")) if p.exists() else 0


class Ctx:
    """One run: the session, the run dir, the run date and small caches. `qid` names the dataset in
    every log line so a dataset's requests can be pulled from requests.log.jsonl by query_id.
    `api` reads repository metadata whole (interpretation e): a JSON record or file listing is not a
    dataset file, and cutting it would hide the very fields the rules read. It also sets `attempts`
    on the Resp (the live attempt lines this call wrote, a cache hit counting as one) so an API
    probe entry reports its retries, and paces credential-free GitHub calls at one per minute
    (interpretation h) so the classification of the twentieth GitHub-hosted dataset does not
    depend on how many came before it; a cached answer, a replay or a keyed run never waits."""

    def __init__(self, rd: RunDir | None, run_date: str, replay: bool):
        self.rd, self.date, self.replay = rd, run_date, replay
        self.sess = RateLimitedSession(rd, replay=replay)
        self.sess.s.max_redirects = 5
        self.qid, self._nbia, self._gh_last = "probe", None, -1e9

    def api(self, source: str, url: str, params: dict | None = None, headers: dict | None = None,
            credential: str | None = None) -> Resp:
        if source == "github" and not credential and not self.replay and not self.sess.is_cached(source, url, params):
            gap = GH_FREE_INTERVAL_S - (time.monotonic() - self._gh_last)
            if gap > 0:
                time.sleep(gap)
            self._gh_last = time.monotonic()
        n0 = _nlines(self.rd.requests_log) if self.rd else 0
        r = self.sess.get(source, self.qid, url, params, headers=headers, credential=credential,
                          keyed=bool(credential), retries=3)
        r.attempts = 1 if (self.rd is None or r.from_cache) else max(1, min(3, _nlines(self.rd.requests_log) - n0))
        return r

    def nbia_collections(self) -> set[str]:
        """Normalised names of the collections NBIA lists publicly; fetched once per run (R8)."""
        if self._nbia is None:
            js = _js(self.api("tcia", f"{NBIA}/getCollectionValues")) or []
            self._nbia = {re.sub(r"[^a-z0-9]", "", str(c.get("Collection", "")).lower()) for c in js if isinstance(c, dict)}
        return self._nbia


# candidate for common.py: RateLimitedSession.get follows redirects inside requests, logs a header
# subset and reads whole bodies; the probe needs the hop chain, every header and a hard 64 KiB cap.
def probe_fetch(ctx: Ctx, source: str, url: str, method: str = "GET") -> dict:
    """HEAD or ranged GET of `url`, redirects followed hop by hop (at most five), body cut at 64 KiB and
    kept only for textual content types. Three attempts on 429/5xx or a transport error with back-off
    1, 2, 4 s. Logged one line per attempt to requests.log.jsonl in the section-15 format and cached
    under raw/probe/<sha1>.json as {sha1, method, url, params, status, headers, retrieved_at, body,
    chain, final_url, error, attempts}. The terminal envelope is cached whether or not it succeeded
    (interpretation f), so raw_sha1 always names a file and replay reproduces a P23 as observed;
    replay serves the cache and raises ReplayMiss otherwise."""
    hdrs = {"Range": f"bytes=0-{CAP - 1}", "Accept": "*/*"} if method == "GET" else {"Accept": "*/*"}
    meth = "GET-range" if method == "GET" else "HEAD"
    sha1 = hashlib.sha1("\n".join([meth, url, "probe"]).encode("utf-8")).hexdigest()
    cache = ctx.rd.raw / "probe" / f"{sha1}.json" if ctx.rd else None
    base = {"source": source, "query_id": ctx.qid, "method": meth, "url": redact_text(url), "params": {},
            "cache_sha1": sha1, "credential": "none"}
    if cache is not None and cache.exists():
        env = json.loads(cache.read_text(encoding="utf-8"))
        append_jsonl(ctx.rd.requests_log, {"ts": now_iso(), **base, "attempt": 0, "status": env["status"], "elapsed_ms": 0,
                                           "bytes": len(env["body"].encode("utf-8")), "from_cache": True, "error": None})
        return env
    if ctx.replay:
        raise ReplayMiss(f"replay: no cached probe for {url} sha1={sha1}")
    env: dict = {}
    for attempt in (1, 2, 3):
        ctx.sess._wait(source, False)  # the same per-source bucket as every other request of the run
        t0, chain, cur, final, status, headers, body, err = time.monotonic(), [], url, url, 0, {}, "", None
        try:
            for hop in range(6):
                r = ctx.sess.s.request(method, cur, headers=hdrs, allow_redirects=False, stream=True, timeout=TIMEOUT_S)
                chain.append(r.status_code)
                final, status = cur, r.status_code
                headers = {k.lower(): v for k, v in r.headers.items()}
                loc = r.headers.get("location")
                if 300 <= r.status_code < 400 and loc and hop < 5:
                    r.close()
                    cur = urljoin(cur, loc)
                    continue
                ct = (headers.get("content-type") or "").lower()
                if method == "GET" and re.search(r"html|json|text|xml", ct):
                    body = (r.raw.read(CAP, decode_content=True) or b"").decode(r.encoding or "utf-8", errors="replace")
                r.close()
                break
        except requests.RequestException as e:
            err = f"{type(e).__name__}: {redact_text(str(e))}"
        ms = int((time.monotonic() - t0) * 1000)
        ctx.sess.n_requests += 1
        if ctx.rd:
            append_jsonl(ctx.rd.requests_log, {"ts": now_iso(), **base, "attempt": attempt, "status": status, "elapsed_ms": ms,
                                               "bytes": len(body.encode("utf-8")), "from_cache": False, "error": err})
        env = {"sha1": sha1, "method": meth, "url": base["url"], "params": {}, "status": status, "headers": headers,
               "retrieved_at": now_iso(), "body": body, "chain": chain, "final_url": final, "error": err, "attempts": attempt}
        if err is None and status not in RETRY_STATUSES:
            break
        if attempt < 3:
            time.sleep(2 ** (attempt - 1))
    if cache is not None:
        dump_json(cache, env)
    return env


# ----------------------------------------------------------------------------- probe entries
def entry(ctx: Ctx, url: str | None, env: dict, method: str, cls: str, rule: str, evidence: str | None) -> dict:
    """One charting_schema probe object from a fetch envelope (probe_fetch) or an API pseudo-envelope."""
    h = env.get("headers") or {}
    return {"url": url, "final_url": env.get("final_url"), "method": method, "http_status": env.get("status"),
            "status_chain": list(env.get("chain") or []), "content_type": _ct(h), "content_length": _len(h),
            "content_disposition": h.get("content-disposition"), "www_authenticate": h.get("www-authenticate"),
            "date": ctx.date, "attempts": min(3, int(env.get("attempts") or 0)), "classification_machine": cls, "rule": rule,
            "evidence": (evidence or "")[:400] or None, "raw_sha1": env.get("sha1"), "error": env.get("error")}


def api_entry(ctx: Ctx, url: str, r: Resp, cls: str, rule: str, evidence: str) -> dict:
    """A probe object for an API-method answer; `attempts` is what Ctx.api counted (1 for a bare Resp)."""
    env = {"status": r.status, "headers": r.headers, "sha1": r.sha1, "final_url": url, "chain": [r.status], "error": r.error,
           "attempts": getattr(r, "attempts", 1)}
    return entry(ctx, url, env, "API", cls, rule, evidence)


def file_probe(ctx: Ctx, ds: dict, furl: str) -> dict:
    """Ranged GET of one file URL; recorded in file_probes[] (the Q7 evidence). Never more than 64 KiB."""
    env = probe_fetch(ctx, "probe", furl, "GET")
    h = env["headers"] or {}
    fp = {"date": ctx.date, "url": furl, "final_url": env["final_url"], "http_status": env["status"], "status_chain": env["chain"],
          "content_type": _ct(h), "content_length": _len(h), "raw_sha1": env["sha1"], "error": env["error"]}
    ds.setdefault("_file_probes", []).append(fp)
    return fp


def _file_answers(ctx: Ctx, ds: dict, furl: str | None) -> dict:
    """file_probe when a URL is given; a null-status stand-in otherwise, so callers test one field."""
    return file_probe(ctx, ds, furl) if furl else {"http_status": None}


def anchors(body: str, base: str) -> list[str]:
    out = []
    for href in re.findall(r"""href\s*=\s*["']([^"']+)["']""", body, re.I):
        u = urljoin(base, html_lib.unescape(href))
        if ANCHOR_RE.search(urlsplit(u).path + ("?" + urlsplit(u).query if urlsplit(u).query else "")) and u not in out:
            out.append(u)
    return out


def classify_generic(ctx: Ctx, url: str, env: dict, method: str) -> dict:
    """Rules P15, P20, P16-P19, P21-P23 over one fetch envelope, in the protocol's order, with
    interpretations (a), (b) and (d) of the module docstring."""
    st, h, body = env["status"], env.get("headers") or {}, env.get("body") or ""
    ct = (h.get("content-type") or "").split(";")[0].split(",")[0].strip().lower()
    final = env.get("final_url") or url
    if env.get("error") or st == 0:
        return entry(ctx, url, env, method, "unavailable", "P23", f"no response on {env.get('attempts')} attempts: {env.get('error')}")
    if st in (404, 410, 451):
        return entry(ctx, url, env, method, "unavailable", "P23", f"HTTP {st}")
    ok = 200 <= st < 300
    if ok:
        if (len(env.get("chain") or []) > 1 or h.get("www-authenticate")) and LOGIN_RE.search(_loc(final)):
            return entry(ctx, url, env, method, "auth-required", "P22", f"redirect chain {env['chain']} ends at login URL {final}")
        size, fp = _len(h), urlsplit(final)
        if (ct in ALLOW_CT or (ct.startswith("image/") and DATA_EXT_RE.search(fp.path.lower()))
                or "attachment" in (h.get("content-disposition") or "").lower()) and (size is None or size >= 1 << 20):
            return entry(ctx, url, env, method, "open-download", "P15", f"content-type {ct}; length {size}; disposition {h.get('content-disposition')}")
        if fp.path in ("", "/") and not fp.query and not doi_in(url):
            return entry(ctx, url, env, method, "unresolved", "P21", f"site root {final}, not a dataset page; verifier decides")
    if ok and body and ("html" in ct or body.lstrip()[:1] == "<"):
        for a in anchors(body, final)[:3]:
            fe = probe_fetch(ctx, "probe", a, "HEAD")
            if fe["status"] not in (200, 206):
                fe = probe_fetch(ctx, "probe", a, "GET")
            if fe["status"] in (200, 206):
                return entry(ctx, url, env, method, "open-download", "P20", f"anchor {a} answered {fe['status']}")
        hit = text_rule(visible_text(body))
        if hit:
            return entry(ctx, url, env, method, hit[1], hit[0], hit[2])
    if st in (401, 403) or h.get("www-authenticate"):
        return entry(ctx, url, env, method, "auth-required", "P22", f"HTTP {st}; WWW-Authenticate {h.get('www-authenticate')}")
    if ok:
        return entry(ctx, url, env, method, "unresolved", "P21", f"HTTP {st} {ct or 'no content-type'}; no rule matched")
    return entry(ctx, url, env, method, "unresolved", "P21", f"HTTP {st} is outside P22/P23; verifier decides")


def probe_generic(ctx: Ctx, url: str) -> dict:
    """HEAD first (a data file answers P15 from its headers); otherwise the ranged GET carries the rules."""
    head = probe_fetch(ctx, "probe", url, "HEAD")
    if 200 <= head["status"] < 300:
        hc = classify_generic(ctx, url, head, "HEAD")
        if hc["rule"] == "P15":
            return hc
    return classify_generic(ctx, url, probe_fetch(ctx, "probe", url, "GET"), "GET-range")


# ----------------------------------------------------------------------------- repository routes (None = fall through)
def r_zenodo(ctx, ds, url, doi, depth=0):
    m = re.search(r"zenodo\.(\d+)", doi or "") or re.search(r"/(?:records?/|doi/10\.5281/zenodo\.)(\d+)", url)
    if not m:
        return None
    api = f"https://zenodo.org/api/records/{m.group(1)}"
    r = ctx.api("zenodo", api)
    rec = _js(r)
    if r.status == 404:  # a concept record id: the latest version answers the search
        r, api = ctx.api("zenodo", "https://zenodo.org/api/records", {"q": f"conceptrecid:{m.group(1)}", "size": 1, "sort": "mostrecent"}), "https://zenodo.org/api/records"
        hits = (((_js(r) or {}).get("hits") or {}).get("hits") or [])
        rec = hits[0] if hits else None
    if not isinstance(rec, dict) or "metadata" not in rec:
        return None
    md, files = rec["metadata"], rec.get("files") or []
    ar = md.get("access_right")
    if ar == "open" and files:  # the largest file, so the Q7 evidence is a data file and not the LICENSE
        big = max(files, key=lambda f: f.get("size") or 0)
        furl = (big.get("links") or {}).get("self") or (big.get("links") or {}).get("content")
        fp = _file_answers(ctx, ds, furl)
        if fp["http_status"] in (200, 206):
            return api_entry(ctx, api, r, "open-download", "P1", f"access_right open; {len(files)} files; {furl} answered {fp['http_status']}")
        return None
    if ar == "restricted":
        return api_entry(ctx, api, r, "request-to-authors", "P2", "access_right restricted")
    if ar in ("embargoed", "closed"):
        return api_entry(ctx, api, r, "unavailable", "P3", f"access_right {ar}; embargo_date {md.get('embargo_date')}")
    return None


def r_figshare(ctx, ds, url, doi, depth=0):
    m = re.search(r"figshare\.(\d+)", doi or "") or re.search(r"/(\d+)(?:/\d+)?/?$", urlsplit(url).path)
    if not m:
        return None
    api = f"https://api.figshare.com/v2/articles/{m.group(1)}"
    r = ctx.api("figshare", api)
    js = _js(r)
    if not isinstance(js, dict):
        return None
    if js.get("is_embargoed"):
        return api_entry(ctx, api, r, "unavailable", "P13", f"is_embargoed true; embargo_date {js.get('embargo_date')}")
    if js.get("is_confidential"):
        return api_entry(ctx, api, r, "request-to-authors", "P13", "is_confidential true (restricted files)")
    files = js.get("files") or []
    if js.get("is_public") and files and files[0].get("download_url"):
        fp = file_probe(ctx, ds, files[0]["download_url"])
        if fp["http_status"] in (200, 206):
            return api_entry(ctx, api, r, "open-download", "P13", f"is_public true; {len(files)} files; first answered {fp['http_status']}")
    return None


def r_dryad(ctx, ds, url, doi, depth=0):
    d = doi or (re.search(r"10\.5061/[^\s?#]+", url) or [None])[0]
    if not d:
        return None
    api = f"https://datadryad.org/api/v2/datasets/{quote(d, safe='')}"
    r = ctx.api("dryad", api)
    js = _js(r)
    if not isinstance(js, dict):
        return None
    vs = str(js.get("versionStatus") or js.get("curationStatus") or "").lower()
    if "embargo" in vs:
        return api_entry(ctx, api, r, "unavailable", "P13", f"versionStatus {vs}")
    if vs == "published":
        fp = file_probe(ctx, ds, api + "/download")
        if fp["http_status"] in (200, 206):
            return api_entry(ctx, api, r, "open-download", "P13", f"versionStatus published; /download answered {fp['http_status']}")
    return None


def _osf_files(items: list) -> tuple[list, list]:
    """(downloadable files, folder listing URLs) from one OSF files page."""
    files = [i for i in items if (i.get("attributes") or {}).get("kind") == "file" and (i.get("links") or {}).get("download")]
    folders = []
    for i in items:
        if (i.get("attributes") or {}).get("kind") == "folder":
            rel = ((((i.get("relationships") or {}).get("files") or {}).get("links") or {}).get("related")) or {}
            href = rel.get("href") if isinstance(rel, dict) else rel
            if href:
                folders.append(href)
    return files, folders


def r_osf(ctx, ds, url, doi, depth=0):
    m = re.search(r"osf\.io/([a-z0-9]{5})\b", (doi or "").lower() + " " + url.lower())
    if not m:
        return None
    tok = cred("OSF_TOKEN")
    hdr, cn, mode = ({"Authorization": f"Bearer {tok}"} if tok else None), ("OSF_TOKEN" if tok else None), ("keyed" if tok else "credential-free")
    api = f"https://api.osf.io/v2/nodes/{m.group(1)}/"
    r = ctx.api("osf", api, headers=hdr, credential=cn)
    js = _js(r)
    if not isinstance(js, dict) or not ((js.get("data") or {}).get("attributes") or {}).get("public"):
        return None
    items = (_js(ctx.api("osf", api + "files/osfstorage/", headers=hdr, credential=cn)) or {}).get("data") or []
    files, folders = _osf_files(items)
    ev = f"public node ({mode}); {len(items)} osfstorage entries"
    if not files and folders:  # one folder level: a dataset that keeps its files in a top-level folder
        files, _ = _osf_files((_js(ctx.api("osf", folders[0], headers=hdr, credential=cn)) or {}).get("data") or [])
        ev += f"; first folder holds {len(files)} files"
    if files:
        fp = file_probe(ctx, ds, files[0]["links"]["download"])
        if fp["http_status"] in (200, 206):
            return api_entry(ctx, api, r, "open-download", "P13", ev + f"; first file answered {fp['http_status']}")
    return None


def r_mendeley(ctx, ds, url, doi, depth=0):
    """P13 for Mendeley Data (interpretation g): DataCite must say findable, the landing page must not say
    embargo, and a file listed by Mendeley's public API (or, failing that, an anchor on the landing page)
    must answer 200/206; `confidential` is request-to-authors, `available: false` is unavailable."""
    m = re.search(r"10\.17632/([a-z0-9]+)(?:\.(\d+))?", doi or "") or re.search(r"/datasets/([a-z0-9]+)(?:/(\d+))?", url)
    if not m:
        return None
    ident, ver = m.group(1), m.group(2)
    for d in ([f"10.17632/{ident}.{ver}"] if ver else [f"10.17632/{ident}", f"10.17632/{ident}.1"]):
        api = f"https://api.datacite.org/dois/{quote(d, safe='')}"
        r = ctx.api("datacite", api)
        js = _js(r)
        if not (isinstance(js, dict) and ((js.get("data") or {}).get("attributes") or {}).get("state") == "findable"):
            continue
        land = probe_fetch(ctx, "probe", url, "GET")
        text = visible_text(land.get("body") or "")
        em = EMBARGO_RE.search(text)
        if em:
            i = em.start()
            return api_entry(ctx, api, r, "unavailable", "P13", f"DataCite {d} findable; landing page says: ...{text[max(0, i - 80):i + 120]}...")
        rec = _js(ctx.api("mendeley", f"{MENDELEY}/{ident}", {"version": ver} if ver else None))
        if isinstance(rec, dict):
            if rec.get("confidential"):
                return api_entry(ctx, api, r, "request-to-authors", "P13", f"DataCite {d} findable; Mendeley record confidential (restricted files)")
            if rec.get("available") is False:
                return api_entry(ctx, api, r, "unavailable", "P13", f"DataCite {d} findable; Mendeley record available=false (embargoed or unpublished)")
            fl = _js(ctx.api("mendeley", f"{MENDELEY}/{ident}/files", {"folder_id": "root", "version": rec.get("version") or ver or 1})) or []
            cands = sorted([f for f in fl if isinstance(f, dict) and (f.get("content_details") or {}).get("download_url")],
                           key=lambda f: -(f.get("size") or 0))
            if cands:
                fp = file_probe(ctx, ds, cands[0]["content_details"]["download_url"])
                if fp["http_status"] in (200, 206):
                    return api_entry(ctx, api, r, "open-download", "P13", f"DataCite {d} findable; Mendeley public API lists {len(cands)} files (credential-free); {cands[0].get('filename')} answered {fp['http_status']}")
        for a in anchors(land.get("body") or "", url)[:3]:
            fp = file_probe(ctx, ds, a)
            if fp["http_status"] in (200, 206):
                return api_entry(ctx, api, r, "open-download", "P13", f"DataCite {d} findable; landing anchor {a} answered {fp['http_status']}")
        return None
    return None


def r_physionet(ctx, ds, url, doi, depth=0):
    m = re.search(r"/content/([^/?#]+)", url)
    land = f"https://physionet.org/content/{m.group(1)}/" if m else url
    env = probe_fetch(ctx, "physionet", land, "GET")
    if 200 <= env["status"] < 300 and env.get("body"):
        pm = re.search(r"Open Access|Credentialed Access|Restricted Access|Contributor Review", visible_text(env["body"]))
        if pm:
            cls, rule = {"Open Access": ("open-download", "P7"), "Contributor Review": ("request-to-authors", "P9")}.get(pm.group(0), ("data-use-agreement", "P8"))
            return entry(ctx, land, env, "GET-range", cls, rule, f"access policy '{pm.group(0)}'")
    return classify_generic(ctx, land, env, "GET-range")


def r_tcia(ctx, ds, url, doi, depth=0):
    m = re.search(r"/collection/([^/?#]+)", url)
    if m and re.sub(r"[^a-z0-9]", "", m.group(1).lower()) in ctx.nbia_collections():
        r = ctx.api("tcia", f"{NBIA}/getCollectionValues")
        return api_entry(ctx, f"{NBIA}/getCollectionValues", r, "open-download", "P10", f"collection '{m.group(1)}' listed publicly by NBIA (download via NBIA REST or Data Retriever)")
    env = probe_fetch(ctx, "probe", url, "GET")
    if 200 <= env["status"] < 300 and env.get("body"):
        text = visible_text(env["body"])
        lm = re.search(r"limited[- ]access", text, re.I) or DUA_RE.search(text)
        if lm:
            return entry(ctx, url, env, "GET-range", "data-use-agreement", "P11", f"'{lm.group(0)}' on the collection page; not in the public NBIA list")
    return classify_generic(ctx, url, env, "GET-range")


def r_hf(ctx, ds, url, doi, depth=0):
    m = re.search(r"huggingface\.co/datasets/([^/\s?#]+/[^/\s?#]+)", url)
    if not m:
        return None
    hdr = {"Authorization": f"Bearer {cred('HF_TOKEN')}"} if cred("HF_TOKEN") else None
    api = f"https://huggingface.co/api/datasets/{m.group(1)}"
    r = ctx.api("hf", api, headers=hdr, credential="HF_TOKEN" if hdr else None)
    js = _js(r)
    if not isinstance(js, dict):
        return None
    gated, mode = js.get("gated"), "keyed" if hdr else "credential-free"
    if gated is False and not js.get("private"):
        sib = [s.get("rfilename") for s in js.get("siblings") or [] if not re.match(r"(README|\.gitattributes)", s.get("rfilename", ""))]
        ev = f"gated false, private false ({mode}); {len(sib)} files"
        if sib:
            fp = file_probe(ctx, ds, f"https://huggingface.co/datasets/{m.group(1)}/resolve/main/{quote(sib[0])}")
            ev += f"; {sib[0]} answered {fp['http_status']}"
        return api_entry(ctx, api, r, "open-download", "P4", ev)
    if gated == "auto":
        return api_entry(ctx, api, r, "registration", "P5", f"gated auto ({mode})")
    if gated == "manual":
        return api_entry(ctx, api, r, "data-use-agreement", "P6", f"gated manual ({mode})")
    return None


def _gh_limited(r: Resp) -> bool:
    """True when GitHub answered from an exhausted rate-limit window (403/429 with no remaining calls)."""
    return r.status in (403, 429) and str((r.headers or {}).get("x-ratelimit-remaining")) == "0"


def _gh(ctx: Ctx, url: str, params: dict | None, hdr: dict, cn: str | None) -> Resp:
    """One GitHub API call. On an exhausted window whose reset is under 120 s away, wait for it and call
    again (the cached 403 is dropped first so the retry reaches the network); otherwise return the
    limited answer for the caller to record (interpretation h)."""
    r = ctx.api("github", url, params, headers=hdr, credential=cn)
    if _gh_limited(r) and ctx.rd is not None and not ctx.replay:
        wait = int(r.headers.get("x-ratelimit-reset") or 0) - time.time()
        if 0 < wait <= 120:
            (ctx.rd.raw / "github" / f"{r.sha1}.json").unlink(missing_ok=True)  # a 403 is cached; drop it so the retry reaches the network
            time.sleep(wait + 1)
            ctx._gh_last = -1e9  # the window has reset; the retry need not also wait out the pacing interval
            r = ctx.api("github", url, params, headers=hdr, credential=cn)
    return r


def r_github(ctx, ds, url, doi, depth=0):
    m = re.search(r"github\.com/([^/\s?#]+)/([^/\s?#]+)", url)
    if not m:
        return None
    repo = f"{m.group(1)}/{m.group(2).removesuffix('.git')}"
    tok = cred("GITHUB_TOKEN")
    hdr = {"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {tok}"} if tok else {})}
    cn, mode = ("GITHUB_TOKEN" if tok else None), ("keyed" if tok else "credential-free")
    api = f"https://api.github.com/repos/{repo}"
    r = _gh(ctx, api, None, hdr, cn)
    if _gh_limited(r):
        return api_entry(ctx, api, r, "unresolved", "P21", f"GitHub API rate-limited ({mode}); reset {r.headers.get('x-ratelimit-reset')}")
    if r.status == 404:
        return api_entry(ctx, api, r, "unavailable", "P23", f"repository not found (404) ({mode})")
    if not r.ok:
        return None
    rel = _gh(ctx, api + "/releases", {"per_page": 5}, hdr, cn)
    if _gh_limited(rel):
        return api_entry(ctx, api, rel, "unresolved", "P21", f"GitHub API rate-limited on /releases ({mode}); reset {rel.headers.get('x-ratelimit-reset')}")
    assets = [a for x in (_js(rel) or []) for a in (x.get("assets") or []) if a.get("size", 0) >= 1 << 20]
    if assets:
        fp = file_probe(ctx, ds, assets[0]["browser_download_url"])
        return api_entry(ctx, api, r, "open-download", "P14", f"{len(assets)} release assets >= 1 MiB ({mode}); first answered {fp['http_status']}")
    rmr = _gh(ctx, api + "/readme", None, hdr, cn)
    if _gh_limited(rmr):
        return api_entry(ctx, api, rmr, "unresolved", "P21", f"GitHub API rate-limited on /readme ({mode}); reset {rmr.headers.get('x-ratelimit-reset')}")
    try:
        readme = base64.b64decode((_js(rmr) or {}).get("content") or "").decode("utf-8", errors="replace")
    except ValueError:
        readme = ""
    links = [u.rstrip(".,;)") for u in re.findall(r"https?://[^\s)\]>\"'`]+", readme)
             if f"github.com/{repo}".lower() not in u.lower() and (ANCHOR_RE.search(urlsplit(u).path) or doi_in(u)
             or any(re.search(p, urlsplit(u).netloc.lower()) for p, _, _ in HOSTS) or CLOUD_RE.search(urlsplit(u).netloc.lower()))]
    if links and depth == 0:
        sub = classify_url(ctx, ds, links[0], None, depth=1)
        sub["rule"], sub["evidence"] = "P14", f"README link {links[0]} followed once ({mode}): {sub['classification_machine']} by {sub['rule']}; {sub['evidence']}"
        return sub
    hit = text_rule(visible_text(readme))
    if hit:
        return api_entry(ctx, api, r, hit[1], hit[0], f"README ({mode}): " + hit[2])
    return api_entry(ctx, api, r, "unresolved", "P21", f"repository reachable ({mode}); no data files, release assets or data link in README")


def r_platform(ctx, ds, url, doi, depth=0):
    """P12: Kaggle, grand-challenge.org, OpenDataLab. A dead page is still P23."""
    env = probe_fetch(ctx, "probe", url, "GET")
    if env["error"] or env["status"] in (0, 404, 410, 451):
        return classify_generic(ctx, url, env, "GET-range")
    text = visible_text(env.get("body") or "")
    if "grand-challenge.org" in urlsplit(url).netloc and DUA_RE.search(text):
        return entry(ctx, url, env, "GET-range", "data-use-agreement", "P12", f"grand-challenge page matched DUA_RE '{DUA_RE.search(text).group(0)}'")
    return entry(ctx, url, env, "GET-range", "registration", "P12", f"platform account required ({urlsplit(url).netloc}); HTTP {env['status']}")


ROUTE_FN = {"zenodo": r_zenodo, "figshare": r_figshare, "dryad": r_dryad, "osf": r_osf, "mendeley": r_mendeley,
            "physionet": r_physionet, "tcia": r_tcia, "hf": r_hf, "github": r_github, "kaggle": r_platform,
            "gc": r_platform, "odl": r_platform}


def route_for(url: str, doi: str | None) -> str:
    """The section-10 route name for `url` (with a DOI's prefix taking precedence), else 'generic'."""
    pfx = (doi or "").split("/")[0]
    if pfx in DOI_PREFIX:
        return DOI_PREFIX[pfx]
    host = urlsplit(url).netloc.lower()
    return next((route for pat, route, _ in HOSTS if re.search(pat, host)), "generic")


def classify_url(ctx: Ctx, ds: dict, url: str, doi: str | None, depth: int = 0) -> dict:
    """Resolve a DOI or handle link once, pick the route, run it, fall back to the generic method.
    `depth` travels into every route so a README link is followed once and never re-enters (a pair
    of repositories citing each other used to recurse until the run died)."""
    doi = doi or doi_in(url)
    route = route_for(url, doi)
    if doi_in(url) and route in ("generic", "physionet", "tcia"):
        env, method = probe_fetch(ctx, "probe", url, "HEAD"), "HEAD"
        if env["status"] == 404:  # doi.org's 404 is confirmed with a GET before an identifier is called dead
            env, method = probe_fetch(ctx, "probe", url, "GET"), "GET-range"
        if env["error"] or env["status"] in (0, 404):
            return entry(ctx, url, env, method, "unavailable", "P23", f"identifier did not resolve: {env['error'] or env['status']}")
        url = env["final_url"]
        if depth == 0:  # host_type describes access_url's own target, not a link followed from a README
            ds["_resolved_url"] = url
        route = route_for(url, None) if route == "generic" else route
    fn = ROUTE_FN.get(route)
    e = fn(ctx, ds, url, doi, depth) if fn else None
    return e if e is not None else probe_generic(ctx, url)


# ----------------------------------------------------------------------------- inputs, agreement, outputs
def load_datasets(a) -> list[dict]:
    """Charting records (id, access_url, doi, file_url_probed, description text) or the known-item rows."""
    root, out = review_root(), []
    if a.from_known_items:
        with open(root / "screen" / "known_items.csv", encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                out.append({"id": row["item"], "access_url": row.get("url") or None, "doi": row.get("doi") or None,
                            "file_url_probed": None, "text": row.get("note") or "", "_record": None, "_path": None})
    else:
        for p in sorted((root / a.datasets_dir).glob("*.json")):
            rec = json.loads(p.read_text(encoding="utf-8"))
            en_p = root / "charting" / "enrichment" / f"{rec['id']}.json"
            en = json.loads(en_p.read_text(encoding="utf-8")) if en_p.exists() else {}
            furl = rec.get("file_url_probed") or en.get("file_url_probed") or next(
                (x.get("url") for x in (en.get("files") or rec.get("checksums") or []) if isinstance(x, dict) and x.get("url")), None)
            text = " ".join([rec.get("notes") or ""] + [q.get("text", "") for q in rec.get("quotes") or []])
            out.append({"id": rec["id"], "access_url": rec.get("access_url"), "file_url_probed": furl, "text": text, "_record": rec, "_path": p,
                        "doi": (rec.get("versioning") or {}).get("dataset_doi") or (rec.get("source_record") or {}).get("doi")})
    if a.ids:
        want = set(a.ids.split(","))
        out = [d for d in out if d["id"] in want]
    out.sort(key=lambda d: d["id"])
    return out[:a.limit] if a.limit else out


def agreement(probes: list[dict]) -> dict:
    """Section 10: the class two probes agree on (the first two, or the agreeing pair when a third was run),
    a route only when that class is route-valued; otherwise what is still needed."""
    if not probes:
        return {"status": "not-probed", "route": None, "rule": None}
    if len(probes) == 1:
        return {"status": "one-probe", "route": None, "rule": None}
    pairs = [(probes[0], probes[1])] + ([(probes[0], probes[2]), (probes[1], probes[2])] if len(probes) > 2 else [])
    pair = next(((x, y) for x, y in pairs if x["classification_machine"] == y["classification_machine"]), None)
    if pair is None:
        return {"status": "needs-third-probe" if len(probes) == 2 else "verifier", "route": None, "rule": None,
                "reason": "probes disagree: " + ", ".join(f"{p['date']} {p['classification_machine']}" for p in probes)}
    cls = pair[0]["classification_machine"]
    rule = pair[0]["rule"] if pair[0]["rule"] == pair[1]["rule"] else f"{pair[0]['rule']}/{pair[1]['rule']}"
    if cls in ROUTES:
        return {"status": "agreed", "route": cls, "rule": rule, "dates": [pair[0]["date"], pair[1]["date"]]}
    return {"status": "verifier", "route": None, "rule": rule, "reason": f"agreed machine class '{cls}' needs the verifier"}


def run_one(ctx: Ctx, ds: dict) -> dict:
    """Probe one dataset and return this run's row {id, access_url, host_type, probe, file_probes}."""
    url = ds["access_url"]
    ds["_file_probes"] = []
    if not url:
        m = REQ_RE.search(ds["text"] or "")
        env = {"status": None, "headers": {}, "sha1": None, "final_url": None, "chain": [], "error": None, "attempts": 0}
        pe = entry(ctx, None, env, "none", "request-to-authors" if m else "unavailable", "P24" if m else "P25",
                   f"no URL; description matched REQ_RE '{m.group(0)}'" if m else "no URL and no request statement")
        ht = "unknown"
    else:
        pe = classify_url(ctx, ds, url, ds.get("doi"))
        ht = host_type(ds.get("_resolved_url") or url)
        if ds.get("file_url_probed") and not any(f["url"] == ds["file_url_probed"] for f in ds["_file_probes"]):
            file_probe(ctx, ds, ds["file_url_probed"])
    return {"id": ds["id"], "access_url": url, "host_type": ht, "probe": pe, "file_probes": ds["_file_probes"]}


def aborted_row(ctx: Ctx, ds: dict, exc: BaseException) -> dict:
    """The row for a dataset whose probe raised: `unresolved` (P21) carrying the redacted error, so the
    verifier sees it and the other datasets are still probed."""
    err = f"{type(exc).__name__}: {redact_text(str(exc))}"
    env = {"status": None, "headers": {}, "sha1": None, "final_url": None, "chain": [], "error": err, "attempts": 0}
    url = ds.get("access_url")
    return {"id": ds["id"], "access_url": url, "host_type": host_type(url) if url else "unknown",
            "probe": entry(ctx, url, env, "none", "unresolved", "P21", f"probe aborted: {err}"), "file_probes": ds.get("_file_probes") or []}


def persist(row: dict, ds: dict, probes_dir: Path, apply: bool) -> dict:
    """Merge this run into charting/probes/<id>.json (same-date entries replaced) and, with --apply, into the record."""
    pf_path = probes_dir / f"{row['id']}.json"
    pf = json.loads(pf_path.read_text(encoding="utf-8")) if pf_path.exists() else {"id": row["id"], "probes": [], "file_probes": []}
    pf["probes"] = sorted([p for p in pf["probes"] if p["date"] != row["probe"]["date"]] + [row["probe"]], key=lambda p: p["date"])
    pf["file_probes"] = sorted([f for f in pf["file_probes"] if f["date"] != row["probe"]["date"]] + row["file_probes"], key=lambda f: (f["date"], f["url"]))
    pf.update({"access_url": row["access_url"], "host_type": row["host_type"], "file_url_probed": ds.get("file_url_probed"), "agreement": agreement(pf["probes"])})
    dump_json(pf_path, pf)
    if apply and ds.get("_record") is not None:
        rec = ds["_record"]
        rec["access_probe"], rec["host_type"] = pf["probes"], row["host_type"]
        rec["file_url_probed"] = rec.get("file_url_probed") or ds.get("file_url_probed")
        ag = pf["agreement"]
        if ag["status"] == "agreed" and not str(rec.get("access_route_rule") or "").startswith("verifier:"):
            rec["access_route"], rec["access_route_rule"] = ag["route"], ag["rule"]
        dump_json(ds["_path"], rec)
    return pf["agreement"]


def main(argv: list[str] | None = None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.availability", description=__doc__.split("\n")[0]))
    ap.add_argument("--datasets-dir", default="charting/datasets", help="charting records, relative to spine_data_review/")
    ap.add_argument("--probes-dir", default="charting/probes", help="where <id>.json probe histories accumulate")
    ap.add_argument("--ids", default=None, help="comma-separated dataset ids to probe (default: all)")
    ap.add_argument("--from-known-items", action="store_true", help="probe screen/known_items.csv URLs (smoke test before charting)")
    ap.add_argument("--apply", action="store_true", help="write access_probe/host_type/access_route into the charting records")
    a = ap.parse_args(argv)
    dsets = load_datasets(a)
    if a.dry_run:
        for d in dsets:
            u, doi = d["access_url"], d.get("doi")
            plan = ("P24/P25 from text, no request" if not u else
                    f"route {route_for(u, doi or doi_in(u))}, host_type {host_type(u)}, " + ("resolve identifier then " if doi_in(u) else "") + "API or HEAD+GET-range")
            print(f"{d['id']:34s} {u or '(no url)'}\n{'':34s} {plan}" + (f"; file {d['file_url_probed']}" if d.get("file_url_probed") else ""))
        print(f"dry-run: {len(dsets)} datasets, no request made")
        return 0
    rd = init_run_dir(a.run_dir, a.run_date, argv)
    ctx = Ctx(rd, a.run_date, a.replay)
    probes_dir = review_root() / a.probes_dir
    log0 = _nlines(rd.requests_log)
    rows, summary = [], {"run_date": a.run_date, "n_datasets": len(dsets), "by_class": {}, "by_rule": {}, "by_status": {}, "needs_action": []}
    for d in dsets:
        ctx.qid = f"probe_{d['id']}"
        try:
            row = run_one(ctx, d)
        except ReplayMiss as e:
            print(f"{d['id']}: {e}", file=sys.stderr)
            return 2
        except Exception as e:  # one dataset never aborts the run: its row is P21 with the error
            row = aborted_row(ctx, d, e)
            print(f"{d['id']}: probe aborted, recorded as unresolved: {row['probe']['error']}", file=sys.stderr)
        ag = persist(row, d, probes_dir, a.apply)
        rows.append(row)
        pe = row["probe"]
        summary["by_class"][pe["classification_machine"]] = summary["by_class"].get(pe["classification_machine"], 0) + 1
        summary["by_rule"][pe["rule"]] = summary["by_rule"].get(pe["rule"], 0) + 1
        summary["by_status"][ag["status"]] = summary["by_status"].get(ag["status"], 0) + 1
        if ag["status"] in ("needs-third-probe", "verifier"):
            summary["needs_action"].append({"id": d["id"], **ag})
        print(f"{d['id']:34s} {pe['classification_machine']:20s} {pe['rule']:4s} {pe['method']:9s} {pe['http_status']}  {(pe['evidence'] or '')[:90]}")
    out = rd.root / "probes"
    out.mkdir(parents=True, exist_ok=True)
    with open(out / f"{a.run_date}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in sorted(rows, key=lambda r: r["id"]):
            f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
    summary["n_requests"] = _nlines(rd.requests_log) - log0  # log lines this invocation, cache hits included
    summary["n_live_requests"] = ctx.sess.n_requests
    dump_json(out / "summary.json", summary)
    print(f"{len(rows)} datasets probed; {summary['n_requests']} requests ({ctx.sess.n_requests} live); summary {out / 'summary.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
