"""The layer every other sdr module imports: HTTP with limits, log and cache; run-dir layout; JSONL; queries.

WHY ONE MODULE. The review's reproducibility claim rests on four habits that are easy to get
wrong once per adapter and hard to audit afterwards: a credential is read by name and never
written anywhere; every HTTP attempt is logged and every body is cached so a run can be
replayed offline; every file lands inside `spine_data_review/`; and a record's identity is one
canonical string hashed the same way by every source. Those habits live in this module and its
two companions (`sdr.creds`, `sdr.ids`), whose public names are re-exported here so an adapter
imports one thing. The contracts are fixed by PROTOCOL.md sections 7.1, 14 and 15, by the
"Conventions the code relies on" in information_sources.md and by "Shared layer contract" in
PIPELINE.md; a change to any of them is a deviations-log row.

Three traps the design answers. (1) The protocol redacts any parameter named `token` in the
request log and hashes secret-stripped parameters into the cache key, but Semantic Scholar
pages with a query parameter named `token`; without `cache_salt` every S2 page would land on
one cache file. (2) `requests` puts the full URL, query string included, into its exception
messages, and an API may echo its request back, so nothing is written raw: `redact_text`
scrubs every loaded credential value (plain and URL-encoded) from the url, every string
parameter, the error text and the response body before they are logged or cached. (3) A query
string embedded in `url` used to be dropped from the cache key and the log, so two pages that
differed only there shared one cache file: `get` now moves it into `params` first.

Public API (each docstring states arguments, return, side effects and what is logged):
  cred, creds_present, contact, unpaywall_email, redact_text      (sdr.creds) names, never values
  norm_doi, norm_pmid, norm_pmcid, norm_arxiv, norm_url, norm_title, canonical_string, record_id,
  normalised_ids, known_item_matches                                (sdr.ids)
  RateLimitedSession, Resp, ReplayMiss, rate_for, SECRET_PARAMS     HTTP: limit, retry, log, cache
  review_root, resolve_run_dir, RunDir, init_run_dir, add_common_args
  now_iso, dump_json, read_jsonl, write_jsonl, append_jsonl         deterministic serialisation
  load_yaml, load_queries, source_table                             rule files, verbatim strings, summary table
CLI: `python -m sdr.common check [--limit N] [--dry-run] [--run-dir R --run-date D]` and
     `python -m sdr.common init --run-dir R --run-date D [--dry-run]`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator
from urllib.parse import parse_qsl, urljoin, urlsplit, urlunsplit

import requests
import yaml

from sdr import PROTOCOL_VERSION

# The screening sheet carries every record's full description, and on the review run of 2026-09-23 one field was over
# the csv module's 128 kB default, so `stats` died reading it (PROTOCOL.md 19, 2026-09-24). Every module imports this
# one, so the limit is raised once here for every csv reader (2**31 - 1: a C long on every platform).
import csv as _csv
_csv.field_size_limit(2**31 - 1)
from sdr.creds import (CREDENTIAL_FREE_FORM, CRED_NAMES, CRED_STORE, contact, cred, creds_present,  # noqa: F401
                       probe_specs, redact_text, unpaywall_email)
from sdr.ids import (REPO_SOURCES, canonical_string, known_item_matches, norm_arxiv, norm_doi,  # noqa: F401
                     norm_family_name, norm_pmcid, norm_pmid, norm_title, norm_url, normalised_ids, record_id)

# ----------------------------------------------------------------------------- HTTP
# Parameter names replaced by <redacted> in the log and in the cache key (PROTOCOL.md section 15).
SECRET_PARAMS = frozenset({"api_key", "apikey", "key", "token", "access_token", "email", "mailto"})
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
BACKOFF_S = (1, 2, 4, 8, 16)
MAX_RETRY_AFTER_S = 120
TIMEOUT_S = 20


def max_attempts() -> int:
    """Attempts per request: the protocol's five, or SDR_MAX_ATTEMPTS from the environment. The
    Makefile exports 2 on a LIMIT run so a source that times out (api.osf.io answered 20 s read
    timeouts on every attempt during one smoke chain) costs seconds, not minutes; the value in force
    is recorded with each invocation in run_meta.json. Never below one."""
    try:
        return max(1, int(os.environ.get("SDR_MAX_ATTEMPTS", "5")))
    except ValueError:
        return 5


# Statuses a cached envelope may carry that say the source did not answer the question, as opposed to answering it:
# transport errors (status 0), the retryable statuses, and the edge refusals seen on the review run (401/403 at an
# access tier, 406 to a client the CDN refused). 404/410 are answers and are never re-observed.
REOBSERVE_STATUSES = RETRY_STATUSES | frozenset({0, 401, 403, 406})


def reobserve() -> tuple[str, frozenset[str]]:
    """(label, sources) of a re-observation pass, or ("", {}) when none is in force. PROTOCOL.md 19 (2026-09-24):
    a request whose cached envelope records a non-answer (`REOBSERVE_STATUSES` or an `error`) is sent again when
    SDR_REOBSERVE names a label and SDR_REOBSERVE_SOURCES lists its source; the failed envelope stays in raw/ with
    its own log line, and the new answer is cached under the same key salted with `|reobs:<label>`. The label and
    the source list travel with the invocation in run_meta.json, and a --replay with the same two variables serves
    the salted envelope, so a re-observed run stays replayable and a replay without them reproduces the failure. A
    request that first failed during the labelled pass itself has no salted answer; a replay serves its failure."""
    label = os.environ.get("SDR_REOBSERVE", "").strip()
    srcs = frozenset(s.strip() for s in os.environ.get("SDR_REOBSERVE_SOURCES", "").split(",") if s.strip())
    return (label, srcs) if label and srcs else ("", frozenset())


def _non_answer(env: dict) -> bool:
    return bool(env.get("error")) or int(env.get("status") or 0) in REOBSERVE_STATUSES


_LOGGED_HEADERS = ("content-type", "retry-after", "link", "x-ratelimit-remaining", "x-ratelimit-reset",
                   "x-total-count", "content-length")
# Minimum seconds between requests per source, (keyed, credential-free); unlisted sources run at 2/s.
_RATES = {"pubmed": (0.1, 1 / 3), "ncbi": (0.1, 1 / 3), "s2": (1.0, 5.0), "openalex": (0.5, 0.5),
          "crossref": (0.5, 0.5), "arxiv": (3.0, 3.0), "zenodo": (1.0, 1.0), "multicare": (1.0, 1.0),
          "github": (2.0, 6.0), "commons": (1.0, 1.0), "osf": (1.0, 1.0), "physionet": (1.0, 1.0),
          "kaggle": (1.0, 1.0), "gc": (1.0, 1.0), "odl": (1.0, 1.0), "openi": (1.0, 1.0),
          "jstage": (1.0, 1.0), "koreamed": (2.0, 2.0), "scielo": (2.0, 2.0), "redalyc": (2.0, 2.0),
          "springer": (1.0, 1.0)}


def rate_for(source: str, keyed: bool = False) -> float:
    """Minimum interval in seconds between two requests to `source`, keyed or credential-free
    (information_sources.md, shared request conventions)."""
    k, free = _RATES.get(source, (0.5, 0.5))
    return k if keyed else free


class ReplayMiss(RuntimeError):
    """Raised in replay mode when a request is not in the raw cache. Never swallowed."""


@dataclass
class Resp:
    """What `RateLimitedSession.get` returns: HTTP status (0 when no answer), body text (redacted by
    value), the logged header subset, cache sha1, whether it came from the cache, elapsed ms,
    redacted error or None, `retrieved_at` (the envelope's timestamp on a cache hit, so a --replay
    run reproduces it, else the time of the answering attempt), the status of every hop (`chain`)
    and the URL that answered (`final_url`). Adapters take `retrieved_at` from here."""
    status: int
    text: str
    headers: dict[str, str]
    sha1: str
    from_cache: bool
    elapsed_ms: int
    error: str | None = None
    retrieved_at: str | None = None
    chain: list[int] = field(default_factory=list)
    final_url: str | None = None

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

    def json(self) -> Any:
        return json.loads(self.text)


def strip_params(params: dict | None) -> dict:
    """Sorted copy of `params` with every SECRET_PARAMS value replaced by <redacted> (by name) and every
    other string value passed through `redact_text` (by value), so a credential under an unlisted
    name (`user`) is still not written. Non-string values are kept as they are: coercing them would
    change the serialised key material and so every cache sha1."""
    return {k: ("<redacted>" if k.lower() in SECRET_PARAMS else redact_text(v) if isinstance(v, str) else v)
            for k, v in sorted((params or {}).items())}


def _canonical_url(url: str) -> str:
    """Scheme + lower-cased host + path, no query or fragment; the query lives in `params`."""
    p = urlsplit(url)
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path, "", ""))


def _merge_query(url: str, params: dict | None) -> tuple[str, dict]:
    """(url without its query string, params with that query string merged in; explicit `params`
    win on a clash, repeated keys keep the last). A server-supplied next-page URL can then be passed
    straight through and still get its own cache key and log line."""
    p = urlsplit(url)
    if not p.query:
        return url, dict(params or {})
    merged = dict(parse_qsl(p.query, keep_blank_values=True))
    merged.update(params or {})
    return urlunsplit((p.scheme, p.netloc, p.path, "", "")), merged


class RateLimitedSession:
    """One HTTP session for a run. Every `get` (1) waits until the per-source interval from `rate_for`
    has passed, (2) returns the cached body when the cache key exists, else fetches with up to
    `max_attempts()` attempts (five; SDR_MAX_ATTEMPTS) on 429/500/502/503/504, back-off 1, 2, 4, 8,
    16 s raised to Retry-After (delta-seconds or HTTP-date, capped at 120 s), (3) appends one line
    per ATTEMPT to <run_dir>/requests.log.jsonl with the fields of PROTOCOL.md section 15 (url and
    params secret-stripped, credential by name, error redacted), and (4) writes the body to
    <run_dir>/raw/<source>/<sha1>.json as an envelope {sha1, method, url, params, status, headers,
    retrieved_at, body, chain, final_url} so XML, Atom and HTML replay like JSON. The cache key is
    sha1 over method + canonical secret-stripped URL + sorted secret-stripped params + body +
    cache_salt, plus the line `keyed` for a keyed request, so a keyed and an anonymous answer to one
    URL (Hugging Face gated datasets) are stored apart while anonymous keys are unchanged.
    `run_dir=None` disables logging and caching; `replay=True` never touches the network and raises
    ReplayMiss on a miss. Pacing is a fixed minimum interval per source, at or under every ceiling
    the providers state."""

    def __init__(self, run_dir: "RunDir | None", replay: bool = False):
        self.run_dir, self.replay = run_dir, replay
        self._last: dict[str, float] = {}
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "spine-data-review/1.0 (scoping review" + (
            f"; mailto:{contact()})" if contact() else ")")
        self.n_requests = 0

    def _wait(self, source: str, keyed: bool) -> None:
        gap = rate_for(source, keyed) - (time.monotonic() - self._last.get(source, -1e9))
        if gap > 0:
            time.sleep(gap)
        self._last[source] = time.monotonic()

    def _log(self, row: dict) -> None:
        if self.run_dir is not None:
            append_jsonl(self.run_dir.requests_log, row)

    def cache_path(self, source: str, url: str, params: dict | None = None, *, cache_salt: str = "",
                   method: str = "GET", data: str | None = None, keyed: bool = False) -> tuple[str, "Path | None"]:
        """(sha1, path) of the raw cache file `get` would read or write for this request; the path is
        None without a run dir. A query string in `url` is merged into `params` first, as `get` does.
        Exposed so an adapter can ask `is_cached` before sending a page whose session state (PubMed
        WebEnv, Crossref cursor, Semantic Scholar token) came out of the cache."""
        url, params = _merge_query(url, params)
        surl, sparams = _canonical_url(url), strip_params(params)
        lines = [method, surl, json.dumps(sparams, sort_keys=True), data or "", cache_salt] + (["keyed"] if keyed else [])
        sha1 = hashlib.sha1("\n".join(lines).encode("utf-8")).hexdigest()
        return sha1, (self.run_dir.raw / source / f"{sha1}.json" if self.run_dir is not None else None)

    def is_cached(self, source: str, url: str, params: dict | None = None, **kw) -> bool:
        """True when `get` with these arguments would be served from the raw cache."""
        p = self.cache_path(source, url, params, **kw)[1]
        return p is not None and p.exists()

    def _request(self, method: str, url: str, params: dict, headers: dict | None, data: str | None,
                 allow_redirects: bool, stream_cap: int | None, full_headers: bool) -> tuple[int, str, dict, list[int], str]:
        """One network attempt: (status, body text, headers, status chain, final url). With
        `allow_redirects` False the hops are followed here one at a time (at most `self.s.max_redirects`)
        so the chain records every status, which is what the availability probe classifies on; with
        `stream_cap` the body is read at most that many bytes instead of whole (a file URL). `params`
        go with the first hop only: a Location header carries its own query."""
        chain, cur, hops = [], url, 0
        while True:
            r = self.s.request(method, cur, params=params if hops == 0 else None, headers=headers, data=data,
                               allow_redirects=allow_redirects, stream=stream_cap is not None, timeout=TIMEOUT_S)
            chain += [h.status_code for h in r.history] + [r.status_code]
            loc = r.headers.get("location")
            if not allow_redirects and 300 <= r.status_code < 400 and loc and hops < self.s.max_redirects:
                r.close()
                cur, hops = urljoin(cur, loc), hops + 1
                continue
            break
        if method == "HEAD":
            text = ""
        elif stream_cap is not None:
            text = (r.raw.read(stream_cap, decode_content=True) or b"").decode(r.encoding or "utf-8", errors="replace")
        else:
            text = r.text
        r.close()
        hdrs = {k.lower(): v for k, v in r.headers.items() if full_headers or k.lower() in _LOGGED_HEADERS}
        return r.status_code, text, hdrs, chain, (r.url if allow_redirects else cur)

    @staticmethod
    def _backoff(attempt: int, hdrs: dict) -> float:
        """Seconds to sleep after a retryable answer: the ladder, raised to Retry-After when the server
        sent one as delta-seconds or as an HTTP-date, never above MAX_RETRY_AFTER_S."""
        wait, ra = BACKOFF_S[min(attempt - 1, len(BACKOFF_S) - 1)], (hdrs.get("retry-after") or "").strip()
        if ra.isdigit():
            return max(wait, min(int(ra), MAX_RETRY_AFTER_S))
        try:
            until = parsedate_to_datetime(ra) if ra else None
        except (TypeError, ValueError, IndexError):
            until = None
        if until is None:
            return wait
        until = until if until.tzinfo else until.replace(tzinfo=timezone.utc)
        return max(wait, min(max(0.0, (until - datetime.now(timezone.utc)).total_seconds()), MAX_RETRY_AFTER_S))

    def get(self, source: str, query_id: str, url: str, params: dict | None = None, *,
            headers: dict | None = None, credential: str | None = None, keyed: bool = False,
            cache_salt: str = "", method: str = "GET", data: str | None = None, retries: int | None = None,
            allow_redirects: bool = True, stream_cap: int | None = None, full_headers: bool = False) -> Resp:
        """Fetch `url` with `params` on behalf of `source`/`query_id` and return a Resp. A query string
        inside `url` is moved into `params` (explicit params win) before anything is hashed or logged.
        `credential` is the NAME logged (never the value); `keyed` picks the rate tier and separates
        the cache key; `cache_salt` disambiguates pages whose state travels in a redacted parameter
        (Semantic Scholar's `token`); `method` may be GET, POST (`data`, the Figshare search) or HEAD;
        `allow_redirects=False` follows hops here and records them in `chain`/`final_url`;
        `stream_cap` reads at most that many bytes; `full_headers` keeps every response header
        instead of the logged subset. Side effects: one requests.log.jsonl line per attempt, one raw
        cache file holding the terminal answer whatever it was, sleeps for pacing and back-off. Body, error and every
        string parameter are passed through `redact_text` before they are logged, cached or returned.
        Never raises on HTTP failure: the final Resp carries the status and the redacted error, and so does
        the cache file, so `--replay` reproduces a failure instead of raising ReplayMiss on it."""
        url, params = _merge_query(url, params)
        retries = retries or max_attempts()
        surl, sparams = _canonical_url(url), strip_params(params)
        sha1, cache = self.cache_path(source, url, params, cache_salt=cache_salt, method=method, data=data, keyed=keyed)
        base = {"source": source, "query_id": query_id, "method": method, "url": redact_text(surl),
                "params": sparams, "cache_sha1": sha1, "credential": credential or "none"}
        if cache is not None and cache.exists():
            env = json.loads(cache.read_text(encoding="utf-8"))
            label, srcs = reobserve()
            salted = f"{cache_salt}|reobs:{label}"
            if (label and source in srcs and "|reobs:" not in cache_salt and _non_answer(env)
                    and not (self.replay and not self.is_cached(source, url, params, cache_salt=salted, method=method,
                                                                data=data, keyed=keyed))):
                # The cached non-answer is left where it is (its own log line accounts for it); the question is asked
                # again under the salted key, which a rerun or a --replay with the same label then serves from cache.
                # A --replay whose salted answer does not exist serves the non-answer instead: that request was first
                # sent, and failed, during the labelled pass itself, so the run never re-observed it (found by the
                # replay of the review run, 2026-09-24: openi_05 page 871).
                return self.get(source, query_id, url, params, headers=headers, credential=credential, keyed=keyed,
                                cache_salt=salted, method=method, data=data, retries=retries,
                                allow_redirects=allow_redirects, stream_cap=stream_cap, full_headers=full_headers)
            self._log({"ts": now_iso(), **base, "attempt": 0, "status": env["status"], "elapsed_ms": 0,
                       "bytes": len(env["body"].encode("utf-8")), "from_cache": True, "error": env.get("error")})
            return Resp(env["status"], env["body"], env.get("headers", {}), sha1, True, 0, env.get("error"), env.get("retrieved_at"),
                        list(env.get("chain") or []), env.get("final_url"))
        if self.replay:
            raise ReplayMiss(f"replay: no cached body for {source}/{query_id} sha1={sha1}")
        resp = Resp(0, "", {}, sha1, False, 0, "no attempt", now_iso())
        for attempt in range(1, retries + 1):
            self._wait(source, keyed)
            t0, err, status, text, hdrs, chain, final = time.monotonic(), None, 0, "", {}, [], None
            try:
                status, text, hdrs, chain, final = self._request(method, url, params, headers, data,
                                                                 allow_redirects, stream_cap, full_headers)
            except requests.RequestException as e:
                err = f"{type(e).__name__}: {redact_text(str(e))}"
            text, ms, ts = redact_text(text), int((time.monotonic() - t0) * 1000), now_iso()
            self.n_requests += 1
            self._log({"ts": ts, **base, "attempt": attempt, "status": status, "elapsed_ms": ms,
                       "bytes": len(text.encode("utf-8")), "from_cache": False, "error": err})
            resp = Resp(status, text, hdrs, sha1, False, ms, err, ts, chain, redact_text(final) if final else None)
            if err is None and status not in RETRY_STATUSES:
                break
            if attempt < retries:
                time.sleep(self._backoff(attempt, hdrs))
        # The terminal envelope is cached whatever the outcome, as availability.probe_fetch does. A failure is
        # part of what the run observed and several adapters branch on it: Figshare sends a body it expects to be
        # answered 500 and splits the boolean on that status, and OSF and the PwC dump recorded transport errors.
        # Caching only the successes meant a --replay of a completed run raised ReplayMiss on the first such answer,
        # so nothing could be replayed. `error` and `attempts` travel with the envelope, so the replayed Resp
        # carries the same status and the same error the live attempt returned. A retryable answer is therefore
        # frozen for the life of a run directory: a fresh observation needs a fresh run dir (PROTOCOL.md 19).
        if cache is not None:
            dump_json(cache, {"sha1": sha1, "method": method, "url": base["url"], "params": sparams,
                              "status": resp.status, "headers": resp.headers, "retrieved_at": resp.retrieved_at,
                              "body": resp.text, "chain": resp.chain, "final_url": resp.final_url,
                              "error": resp.error, "attempts": attempt})
        return resp


# ----------------------------------------------------------------------------- run-dir layout
def review_root() -> Path:
    """The spine_data_review directory (parent of the sdr package). Every write stays under it."""
    return Path(__file__).resolve().parent.parent


def resolve_run_dir(run_dir: str | os.PathLike) -> Path:
    """Absolute path for `run_dir`: a relative path resolves against `review_root()`, so
    `--run-dir runs/2026-09-19` means the same from any cwd. A run dir must be a strict descendant of
    `runs/` (PROTOCOL.md section 14) or of `tests/` (fixture runs); the review root itself, `runs/`
    itself and anything outside raise ValueError, because raw/, records/ and run_meta.json at the
    top level would shadow the layout of section 14."""
    root, p = review_root(), Path(run_dir)
    p = (p if p.is_absolute() else root / p).resolve()
    if not any(d in p.parents for d in (root / "runs", root / "tests")):
        raise ValueError(f"run dir {p} must lie under {root / 'runs'} (or tests/ for a fixture); nothing is written there")
    return p


def _guard(path: str | os.PathLike) -> Path:
    """Resolve `path` and refuse it unless it lies under review_root()."""
    p = Path(path).resolve()
    if review_root() not in p.parents:
        raise ValueError(f"refusing to write outside spine_data_review/: {p}")
    return p


@dataclass
class RunDir:
    """The fixed layout of runs/<run-date>/ (PROTOCOL.md section 14): raw/<source>/<sha1>.json,
    records/<source>.jsonl, requests.log.jsonl, queries.json, merged.jsonl, run_meta.json."""
    root: Path

    def __post_init__(self) -> None:
        self.root = resolve_run_dir(self.root)
        self.raw, self.records = self.root / "raw", self.root / "records"
        self.requests_log, self.queries_json = self.root / "requests.log.jsonl", self.root / "queries.json"
        self.merged, self.meta = self.root / "merged.jsonl", self.root / "run_meta.json"

    def records_file(self, source: str) -> Path:
        return self.records / f"{source}.jsonl"

    def queries(self) -> dict:
        """The queries.json mapping (query_id -> record), {} when the file does not exist yet."""
        return json.loads(self.queries_json.read_text(encoding="utf-8")) if self.queries_json.exists() else {}

    def update_queries(self, query_id: str, record: dict) -> None:
        """Merge `record` into queries.json[query_id] (existing keys overwritten) and rewrite sorted."""
        q = self.queries()
        q[query_id] = {**q.get(query_id, {}), **record}
        dump_json(self.queries_json, q)


def init_run_dir(run_dir: str | os.PathLike, run_date: str, argv: list[str] | None = None) -> RunDir:
    """Create raw/ and records/ under `run_dir` and write run_meta.json {run_date, protocol_version,
    created_at, python, platform, packages, credentials_present (names), invocations}. Idempotent:
    an existing run_meta.json is kept and this call is appended to `invocations` with a redacted
    argv; a different `run_date` for an existing run dir raises ValueError. Returns the RunDir."""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", run_date):
        raise ValueError(f"--run-date must be YYYY-MM-DD, got {run_date!r}")
    rd = RunDir(Path(run_dir))
    rd.raw.mkdir(parents=True, exist_ok=True)
    rd.records.mkdir(parents=True, exist_ok=True)
    meta = json.loads(rd.meta.read_text(encoding="utf-8")) if rd.meta.exists() else {
        "run_date": run_date, "protocol_version": PROTOCOL_VERSION, "created_at": now_iso(),
        "python": sys.version.split()[0], "platform": sys.platform,
        "packages": {p: _version(p) for p in ("requests", "numpy", "scipy", "pandas", "matplotlib", "statsmodels", "PyYAML")},
        "credentials_present": creds_present(), "invocations": []}
    if meta["run_date"] != run_date:
        raise ValueError(f"run dir {rd.root} was created for run date {meta['run_date']}, not {run_date}")
    label, srcs = reobserve()
    meta["invocations"].append({"ts": now_iso(), "argv": [redact_text(a) for a in (argv or sys.argv)],
                                "max_attempts": max_attempts(),
                                **({"reobserve": {"label": label, "sources": sorted(srcs)}} if label else {})})
    dump_json(rd.meta, meta)
    return rd


def _version(pkg: str) -> str:
    try:
        return version(pkg)
    except PackageNotFoundError:
        return "absent"


def add_common_args(parser: argparse.ArgumentParser, required: bool = True) -> argparse.ArgumentParser:
    """Add the flags every module carries: --run-dir, --run-date, --limit, --dry-run, --replay
    (PROTOCOL.md section 15). Returns the parser; modules add their own flags after this call."""
    parser.add_argument("--run-dir", required=required, help="runs/<run-date>, relative to spine_data_review/")
    parser.add_argument("--run-date", required=required, help="YYYY-MM-DD; the only date written to outputs")
    parser.add_argument("--limit", type=int, default=None, help="stop after this many items (smoke tests)")
    parser.add_argument("--dry-run", action="store_true", help="print what would be requested or written; no network, no writes")
    parser.add_argument("--replay", action="store_true", help="serve every request from raw/; fail on a miss")
    return parser


# ----------------------------------------------------------------------------- serialisation
def now_iso() -> str:
    """Wall-clock UTC timestamp, ISO-8601 with Z: the only wall-clock value allowed in any output."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def dump_json(path: str | os.PathLike, obj: Any) -> None:
    """Write `obj` as JSON with sorted keys, two-space indent, UTF-8, LF, trailing newline, atomically
    (temp file then replace). Refuses a path outside review_root()."""
    p = _guard(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, sort_keys=True, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, p)


def read_jsonl(path: str | os.PathLike) -> Iterator[dict]:
    """Yield one dict per non-blank line of a JSONL file; an absent file yields nothing."""
    p = Path(path)
    if p.exists():
        with open(p, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)


def write_jsonl(path: str | os.PathLike, rows: Iterable[dict], key: Callable[[dict], Any] | None = None) -> int:
    """Overwrite `path` with `rows` as JSONL, sorted keys, rows ordered by `key` (default: record_id,
    query_id, then the serialised row, so output is byte-stable). Returns the row count."""
    p = _guard(path)
    key = key or (lambda r: (r.get("record_id", ""), r.get("query_id", ""), json.dumps(r, sort_keys=True)))
    rows = sorted(rows, key=key)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
    return len(rows)


def append_jsonl(path: str | os.PathLike, row: dict) -> None:
    """Append one row (sorted keys) to a JSONL file; used for the request log."""
    p = _guard(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


# ----------------------------------------------------------------------------- queries and rules
_GRID_LINE = re.compile(r"^([a-z][a-z0-9]*(?:_[a-z]*\d+[a-z]?)?|[gt]\d{2})\s{2,}(\S.*)$")
_PROSE_TERM = re.compile(r"`(t\d{2}) ([^`]+)`")


def load_yaml(path: str | os.PathLike) -> Any:
    """Parse a YAML file (screen/prescreen_rules.yaml, or a query file) with the safe loader."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_queries(path: str | os.PathLike | None = None) -> dict[str, dict]:
    """The verbatim query strings keyed by query_id, from information_sources.md (default) or from a
    YAML file mapping id -> {string, ...}. From the markdown: fenced blocks headed `query_id: <id>`
    (lines joined with one space; form `fenced`), two-space grid lines `<id>  <string>` inside
    fences (form `grid`), and the backticked single-term list `t01`-`t08` (form `term`), each with
    the `## ` section it sits under. Strings are returned as written, placeholders included:
    substituting a credential is the adapter's job, so this function never sees a value."""
    path = Path(path) if path else review_root() / "information_sources.md"
    if path.suffix in (".yaml", ".yml"):
        return {k: dict(v) if isinstance(v, dict) else {"string": v} for k, v in load_yaml(path).items()}
    out: dict[str, dict] = {}
    section, fence, qid, buf = "", False, None, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            if fence and qid:
                out[qid] = {"string": " ".join(buf).strip(), "section": section, "form": "fenced"}
            fence, qid, buf = not fence, None, []
            continue
        if line.startswith("## "):
            section = line[3:].strip()
        elif fence:
            m = re.match(r"^query_id:\s*(\S+)\s*$", line)
            g = _GRID_LINE.match(line)
            if m and not buf:
                qid = m.group(1)
            elif qid:
                buf.append(line.strip())
            elif g:
                out[g.group(1)] = {"string": g.group(2).strip(), "section": section, "form": "grid"}
        else:
            for t, s in _PROSE_TERM.findall(line):
                out[t] = {"string": s.strip(), "section": section, "form": "term"}
    return dict(sorted(out.items()))


def source_table(path: str | os.PathLike | None = None) -> dict[str, dict[str, str]]:
    """The summary table of information_sources.md keyed by source code (L1, R3, F2, S1): {source, endpoint,
    auth, ceiling, grammar, paging, coverage, raw_cache}, backticks removed, escaped pipes restored. The
    protocol says `coverage` and the raw-cache reason in queries.json come "from the summary table", so
    adapters read them here rather than carrying a typed copy that drifts from the file."""
    path = Path(path) if path else review_root() / "information_sources.md"
    out, active, cols = {}, False, ("source", "endpoint", "auth", "ceiling", "grammar", "paging", "coverage", "raw_cache")
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            active = line.strip() == "## Summary table"
        elif active and line.startswith("|"):
            cells = [c.strip().replace("`", "").replace("\x00", "|") for c in line.replace("\\|", "\x00").strip().strip("|").split("|")]
            if len(cells) == len(cols) + 1 and re.fullmatch(r"[A-Z]\d+", cells[0]):
                out[cells[0]] = dict(zip(cols, cells[1:]))
    return out


# ----------------------------------------------------------------------------- CLI
def _check(a: argparse.Namespace) -> int:
    """Print which credential names are present and probe each credentialed service once with a
    harmless request (sdr.creds.probe_specs), the first --limit of them. --dry-run prints the
    secret-stripped probes and makes no request. With --run-dir/--run-date the probes are logged and
    cached there like any run (a second check on the same run dir is then served from the cache).
    Prints names, status codes and redacted errors only."""
    present = creds_present()
    print("credential store:", CRED_STORE, "(exists)" if CRED_STORE.exists() else "(absent)")
    for n in CRED_NAMES:
        print(f"  {n:30s} {'present' if n in present else 'absent'}")
    specs = probe_specs()[: a.limit]
    if a.dry_run:
        for name, source, url, params, headers in specs:
            print(f"  would probe {source:10s} {name:28s} {url} {strip_params(params)} headers={sorted(headers)}")
        return 0
    rd = init_run_dir(a.run_dir, a.run_date, sys.argv) if a.run_dir else None
    sess, failures = RateLimitedSession(rd, replay=a.replay), 0
    for name, source, url, params, headers in specs:
        if name not in present:
            print(f"  probe {source:10s} skipped: {name} absent -> {CREDENTIAL_FREE_FORM.get(name, '')}")
            continue
        r = sess.get(source, "check", url, params, headers=headers, credential=name, keyed=True, retries=2)
        # 429 is the service answering with the key accepted and the pace exceeded (the probes fire back to
        # back), not a credential that does not work. Calling it a failure would contradict the credential_mode
        # the run then records for every query of that source, which is the field this review asks to be trusted.
        limited = r.status == 429
        failures += not (r.ok or limited)
        print(f"  probe {source:10s} {name:28s} status {r.status:3d} "
              + ("ok" if r.ok else "rate-limited (key in use)" if limited else "FAIL")
              + (f"  {redact_text(r.error)}" if r.error else ""))
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m sdr.common", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    add_common_args(sub.add_parser("check", help="credential names present and one harmless probe per service"), required=False)
    add_common_args(sub.add_parser("init", help="create runs/<run-date>/ layout and run_meta.json"))
    a = ap.parse_args(argv)
    if a.cmd == "check":
        if bool(a.run_dir) != bool(a.run_date):
            ap.error("--run-dir and --run-date go together")
        return _check(a)
    if a.dry_run:
        print(f"dry run: would create {resolve_run_dir(a.run_dir)}/{{raw/, records/}} and write run_meta.json for run"
              f" date {a.run_date}; credentials present: {creds_present()}")
        return 0
    rd = init_run_dir(a.run_dir, a.run_date, argv)
    print(f"run dir ready: {rd.root}\n  run_meta.json written; credentials present: {creds_present()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
