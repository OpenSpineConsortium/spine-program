"""State and helpers shared by the three repository search modules (R1-R8 in sdr.search_repositories,
R9-R14 in sdr.search_platforms, F1, F4-F8 and the mention harvests in sdr.search_figure_routes).

WHY A SHARED FILE. The engineering rule is 150-450 lines per module and one adapter family per
module, but the twenty adapters share one contract: the record shape of PROTOCOL.md section 15,
the queries.json entry of section 6.3, the merged counts.json, the local prescreen regexes of
Appendix A, and the `--limit`/`--dry-run`/`--replay` switches. Keeping that contract in one class
(`Run`) means a field added here appears in every module's output at once, and the fixture tests
exercise one implementation.

What `Run` records that the adapters cannot see for themselves: `n_requests` per query_id (every
call through `Run.get`, cache hits included, one request-log line each; retries add log lines but
not calls), `n_failed_requests`, `partial` and the last redacted error (`note_status`: a request
that answered with status 0, a 5xx or a 429 that outlived every attempt did not answer at all, and
a source that answered nothing must not be readable as a source that answered zero -- the adapters
cannot report it because their paging loops read a failure as end-of-results, so `query` writes the
count and the flag into the entry, and the count and the error into `notes`, whether or not the
adapter thought to), and the `unit` of each hit count. The sources do not count the same thing: Zenodo
counts records, Open-i figures, Commons files, PhysioNet and TCIA the size of the harvest they
filter locally. `flush` therefore sums `hit_count_api_total` only over unit=records and
role=search and reports the other units separately in `hit_count_by_unit`, so a PRISMA flow
never adds figures to records.

`_get_bytes` is the binary GET the gzip dump needs (sdr.common returns text). It follows
RateLimitedSession.get exactly: sha1 cache key from the session, the same envelope with
`body_b64` in place of `body`, one log line with the redacted url and the cache sha1, and under
`--replay` a cache hit or a ReplayMiss, never the network.

Queries come from queries/repositories.yaml and queries/literature.yaml (`load_repo_queries`):
the appendix sources, byte-checked against information_sources.md by tests/test_queries_yaml.py.
The markdown lines of the list sources carry annotations ("(verify; fallback ...)") that the
YAML strips into `markdown_string`, so reading the YAML is what makes queries.json.query_string
the string actually sent. `_family` and `_first` also accept the markdown primitives (`g01`,
`t01`) so a fixture can pass a two-entry dict.
"""
from __future__ import annotations

import base64
import html as htmlmod
import json
import re
import time
from urllib.parse import parse_qsl, urlsplit

from sdr.common import (RETRY_STATUSES, RateLimitedSession, ReplayMiss, Resp, RunDir, append_jsonl, canonical_string,
                        dump_json, load_queries, load_yaml, normalised_ids, now_iso, record_id, redact_text,
                        review_root, source_table, strip_params, write_jsonl)

# PROTOCOL.md Appendix A. Read from screen/prescreen_rules.yaml when sdr/prescreen.py has written it (keys
# SPINE_RE, MODALITY_RE); the literals below are the frozen v1.0 strings and are used otherwise.
_RULES = {"SPINE_RE": r"\b(spine|spinal|vertebr\w*|lumbar|lumbo-?sacral|thoraco-?lumbar|sacrum|cervical spine|thoracic spine|scoliosis|spondylo\w*|intervertebral|pedicle)\b",
          "MODALITY_RE": r"(\bcomputed tomograph\w*|\bCT\b|\bCBCT\b|cone-?beam|radiograph\w*|\bx-?rays?\b|roentgen\w*|fluoroscop\w*|\bc-?arm\b|image intensifier|\bDXA\b|\bDEXA\b|dual-energy x-?ray|absorptiometry|vertebral fracture assessment|\bEOS\b|biplanar|plain films?)"}
_yaml = review_root() / "screen" / "prescreen_rules.yaml"
if _yaml.exists():
    _RULES.update({k: v for k, v in (load_yaml(_yaml) or {}).items() if k in _RULES and isinstance(v, str)})
SPINE_RE, MODALITY_RE = re.compile(_RULES["SPINE_RE"], re.I), re.compile(_RULES["MODALITY_RE"], re.I)
UNITS = ("records", "figures", "files", "harvest")
# adapter name -> source code of the summary table of information_sources.md; `coverage` and the raw-cache
# column of queries.json are read from that table (sdr.common.source_table), never typed here.
SOURCE_CODES = {"zenodo": "R1", "figshare": "R2", "dryad": "R3", "osf": "R4", "mendeley": "R5", "datacite": "R6", "physionet": "R7",
                "tcia": "R8", "kaggle": "R9", "hf": "R10", "gc": "R11", "github": "R12", "pwc": "R13", "odl": "R14",
                "openi": "F1", "multicare": "F2", "openpmc": "F3", "commons": "F4", "jstage": "F5", "koreamed": "F6",
                "scielo": "F7", "redalyc": "F8"}
# F2 and F3 have no search adapter in this version (write_not_run records them); their codes are here so the
# coverage and raw-cache cells of their not-run entries still come from the summary table, not from "unknown".


def _coverage() -> dict[str, tuple[str, bool, str]]:
    """source -> (coverage, raw cache published, reason). `raw_cache` reads "yes", "yes (reason)", "no (reason):
    what is published instead" or "partial: reason"; published means the column starts with yes. The two
    mention harvests have no table row and no HTTP body."""
    table = source_table()
    out = {"kaggle-mention": ("n/a (harvest)", True, ""), "hf-mention": ("n/a (harvest)", True, "")}
    for name, code in SOURCE_CODES.items():
        row = table.get(code)
        if row is None:
            out[name] = ("unknown", True, f"no summary-table row for {code}")
            continue
        rc = row.get("raw_cache", "")
        out[name] = (row.get("coverage", "unknown"), rc.startswith("yes"), "" if rc == "yes" else rc)
    return out


COVERAGE = _coverage()


# ----------------------------------------------------------------------------- queries
def load_repo_queries() -> dict[str, dict]:
    """queries/repositories.yaml and queries/literature.yaml merged (the ids are disjoint; the figure
    routes F1, F4-F8 sit in literature.yaml), keyed by query_id, each with at least `string`."""
    q = review_root() / "queries"
    return {**load_queries(q / "literature.yaml"), **load_queries(q / "repositories.yaml")}


_PLAN: dict[str, dict] = {}


def _plan_for(qid: str) -> dict:
    """The YAML entry of a query id or of its family head (`openi_03_xg` -> `openi_03`, `crossref_12a` -> `crossref_12`,
    `openalex_01_g07` -> `openalex_01`); {} when neither exists (a fixture id)."""
    if not _PLAN:
        try:
            _PLAN.update(load_repo_queries())
        except (OSError, ValueError):
            _PLAN["__missing__"] = {}
    for k in (qid, re.sub(r"_(xg|c)$", "", qid), re.sub(r"[a-d]$", "", qid), re.sub(r"_g\d\d$", "", qid)):
        if k in _PLAN:
            return _PLAN[k]
    return {}


def write_not_run(run: "Run", Q: dict) -> None:
    """One queries.json entry, credential_mode `not-run`, for every YAML id whose source has no adapter in this
    version (its entry carries `not_run_reason`): hits null, nothing retrieved, no request, and no
    `first_request_ts`, which is what Table 2 and \numQueries read to tell a searched source from a planned
    one. Appendix A prints the id with its not_run_reason, so the appendix never presents a template as
    executed. `date_filter="none"` is the observation, not the plan: nothing was sent, so no date limit was
    applied anywhere; Run.query still compares it with the YAML and records a disagreement."""
    for qid, y in sorted(Q.items()):
        if y.get("not_run_reason") and qid not in run.done:
            run.query(qid, y["source"], y.get("endpoint", ""), y["string"], y.get("grammar", "list"), "not-run", None, 0, 0,
                      date_filter="none", role=y.get("role", "search"), notes={"not_run_reason": y["not_run_reason"]})


def _first(Q: dict, *keys: str) -> str:
    """`string` of the first key present: the YAML id (`mendeley_01`) or its markdown primitive (`t01`)."""
    for k in keys:
        if k in Q:
            return Q[k]["string"]
    raise KeyError(f"none of {keys} in the query set")


def _family(Q: dict, prefix: str, base_re: str) -> list[tuple[str, str]]:
    """Sorted (query_id, string) of a grid/term family: YAML ids `<prefix><base>` win; a bare markdown
    primitive `<base>` (a fixture, or the markdown loader) is prefixed on the fly."""
    out: dict[str, str] = {}
    for k, v in Q.items():
        if re.fullmatch(prefix + base_re, k):
            out[k] = v["string"]
        elif re.fullmatch(base_re, k):
            out.setdefault(prefix + k, v["string"])
    return sorted(out.items())


# ----------------------------------------------------------------------------- small helpers
def _json(r: Resp):
    """Parsed JSON body of an ok response, else None (an HTML page, an error, a dry run)."""
    if not r.ok:
        return None
    try:
        return json.loads(r.text)
    except ValueError:
        return None


def _txt(s) -> str:
    """Visible text of an HTML fragment: script/style removed, tags stripped, entities unescaped, one space."""
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", str(s or ""), flags=re.S | re.I)
    return re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def _year(s):
    """First plausible year (1990-2029) in `s` as int, else None."""
    m = re.search(r"\b(19[9]\d|20[0-2]\d)\b", str(s or ""))
    return int(m.group(1)) if m else None


def _split(url: str) -> tuple[str, dict]:
    """(url without query, params) so server-supplied next-URL pages get distinct cache keys."""
    p = urlsplit(url)
    return p._replace(query="", fragment="").geturl(), dict(parse_qsl(p.query, keep_blank_values=True))


def _chunks(xs: list, k: int) -> list[list]:
    return [xs[i:i + k] for i in range(0, len(xs), k)]


def _top_clauses(s: str) -> list[str]:
    """Split a boolean string on ` AND ` at parenthesis depth 0 (Zenodo pre-run clause check)."""
    s = s.strip()
    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1]
    out, depth, cur, i = [], 0, "", 0
    while i < len(s):
        depth += (s[i] == "(") - (s[i] == ")")
        if depth == 0 and s.startswith(" AND ", i):
            out.append(cur.strip()); cur, i = "", i + 5
            continue
        cur += s[i]; i += 1
    return out + [cur.strip()]


# ----------------------------------------------------------------------------- the run
class Run:
    """State of one invocation: the session, the run dir, the records per source (de-duplicated by
    record_id within a source, `query_ids` accumulating), per-source counts, the per-query request
    counter, and the dry-run switch."""

    def __init__(self, rd: RunDir | None, sess: RateLimitedSession | None, run_date: str, limit, dry_run: bool):
        self.rd, self.sess, self.run_date, self.limit, self.dry_run = rd, sess, run_date, limit, dry_run
        self.records: dict[str, dict[str, dict]] = {}
        self.counts: dict[str, dict] = {}
        self.done: set[str] = set()
        self._t0: dict[str, str] = {}
        self._nreq: dict[str, int] = {}
        self._nfail: dict[str, int] = {}
        self._nexp: dict[str, int] = {}
        self._expwhy: dict[str, str] = {}
        self._lasterr: dict[str, str] = {}
        self.n_unusable: dict[str, int] = {}
        self.n_would = 0

    @property
    def replay(self) -> bool:
        return bool(self.sess is not None and getattr(self.sess, "replay", False))

    def count(self, qid: str) -> None:
        """One more request on behalf of `qid` (Run.get and _get_bytes call this)."""
        self._t0.setdefault(qid, now_iso())
        self._nreq[qid] = self._nreq.get(qid, 0) + 1

    def note_status(self, qid: str, status: int, error: str | None = None) -> None:
        """A request on behalf of `qid` that did not answer: status 0 (a transport error, which is what a
        refused connection or a read timeout looks like here), a 5xx, or one of the retryable statuses that
        survived every attempt (a 429 the service never lifted). Counted so that `query` can say so without
        the adapter remembering to; any other 4xx is an answer and is not counted. It has to be counted
        here because every paging loop in the adapters reads a failure as end-of-results - `_json` returns
        None, the loop breaks - so a truncated search would otherwise be written as a complete one."""
        if status == 0 or status in RETRY_STATUSES or error is not None or (isinstance(status, int) and status >= 500):
            self._nfail[qid] = self._nfail.get(qid, 0) + 1
            self._lasterr[qid] = redact_text(error or f"status {status}")[:200]

    def expect_failure(self, qid: str, why: str) -> None:
        """One of `qid`'s failed requests was a probe, not a truncation: the adapter sent it to find out
        what the service does and took another route on the answer. It stays in `n_failed_requests` - the
        request did fail - but it does not raise `partial`, which says the query's counts are lower bounds.
        Only Figshare uses it: one body is sent to see whether the service still answers 500 above about
        eleven terms, and the same boolean is then executed as an equivalent union of sub-queries."""
        self._nexp[qid] = self._nexp.get(qid, 0) + 1
        self._expwhy[qid] = why

    def get(self, source, qid, url, params=None, **kw) -> Resp:
        if self.dry_run:
            self.n_would += 1
            print(f"would {kw.get('method', 'GET')} [{source}/{qid}] {url} {json.dumps(params or {}, ensure_ascii=False)[:160]}")
            return Resp(0, "", {}, "", False, 0, "dry-run")
        self.count(qid)
        r = self.sess.get(source, qid, url, params, **kw)
        self.note_status(qid, r.status, r.error)
        return r

    def cap(self, items):
        """`--limit`: at most this many items per query. Adapters apply it AFTER any local filter, so a
        smoke run exercises the filtered branches."""
        return list(items)[: self.limit] if self.limit else list(items)

    def add(self, source, qid, *, ids: dict, title, desc, year, rtype, raw: dict, native_id=None) -> bool:
        """Build and keep one record. True when the item is new to this query: a new record, or an existing
        record of the source that `qid` now also found (its `query_ids` grows). False when this query already
        returned the item (a union sub-query, a second page) or it had no usable identifier (counted per
        source). Summing the True results gives n_retrieved: distinct items per query, so a record found
        by two queries counts once in each and the source's n_records_unique counts it once."""
        try:
            can = canonical_string(ids, source, native_id)
        except ValueError:
            self.n_unusable[source] = self.n_unusable.get(source, 0) + 1
            return False
        rid = record_id(can, source, rtype)
        bucket = self.records.setdefault(source, {})
        if rid in bucket:
            if qid in bucket[rid]["query_ids"]:
                return False
            bucket[rid]["query_ids"] = sorted(bucket[rid]["query_ids"] + [qid])
            return True
        bucket[rid] = {"record_id": rid, "source": source, "query_id": qid, "query_ids": [qid], "retrieved_at": now_iso(),
                       "canonical": can, "ids": normalised_ids(ids), "title": (title or "").strip(),
                       "abstract_or_description": (desc or "").strip(), "year": year, "type": rtype, "raw": raw}
        return True

    def query(self, qid, source, endpoint, string, grammar, mode, hits, n_retrieved, n_pages, *, date_filter,
              cap_hit=None, notes=None, params=None, method="GET", role="search", intervals=None, unit="records",
              n_fetched=None) -> None:
        """One queries.json entry (PROTOCOL.md 6.3) and the per-source line of counts.json. `hits` is the
        API's own total, None when the API reports none (never the retrieved count); `unit` names what it
        counts (records | figures | files | harvest); `n_fetched` is what the source handed over before any
        local filter (default n_retrieved), so a smoke run shows the pages were read even when the filter
        kept fewer than `--limit` items; `n_failed_requests` comes from note_status, not from the adapter,
        and `partial` is true when the query has more failed requests than the adapter declared through
        `expect_failure` - that is, when a request failed that nobody was probing for, and the paging loop
        therefore stopped at a hole rather than at the end of the results.

        `date_filter` has no default: every adapter states what its request did, `api` when the request
        carried the 2000-2026 limit, `local` when the limit is left to the screen, `none` when nothing was
        sent. What is recorded is that observation, and `raw_cache_published` is the summary table's cell
        (sdr.common.source_table). Neither is taken from queries/*.yaml, so tests/test_queries_yaml.py
        compares two independently produced values and can fail; a disagreement is also recorded here, as
        `date_filter_planned` / `raw_cache_published_planned`, and printed. Until this version the plan
        overwrote both before the record existed, which made that test compare the plan with a copy of
        itself -- and it hid a live bug: `_datacite` computed `local` from a flag that selects a modality
        filter, not a date filter, while its string carries publicationYear:[2000 TO 2026]."""
        assert unit in UNITS, unit
        assert date_filter in ("api", "local", "none"), date_filter
        # A source that never answered is not a source that answered zero (tests/check_run.py `no-answer`,
        # Table 2). Written here, not by the adapter, so no adapter can leave it out. The same count is a field
        # of the entry (below) for the tables to read and a `notes` line for a person reading the record.
        nfail, nexp = self._nfail.get(qid, 0), self._nexp.get(qid, 0)
        part = nfail > nexp
        if nfail:
            notes = {**(notes or {}), "n_failed_requests": nfail, "last_request_error": self._lasterr.get(qid, "")}
        if nexp:
            notes = {**(notes or {}), "n_expected_failures": nexp, "expected_failure_reason": self._expwhy.get(qid, "")}
        cov, pub, why = COVERAGE.get(source, ("unknown", True, ""))
        plan = _plan_for(qid)
        planned, pub_planned = plan.get("date_filter"), plan.get("raw_cache_published")
        rec = {"source": source, "role": role, "endpoint": endpoint, "method": method, "query_string": string,
               "intervals": intervals, "n_requests": self._nreq.get(qid, 0), "n_failed_requests": nfail,
               "partial": part, "params": strip_params(params), "grammar": grammar,
               "coverage": cov, "run_date": self.run_date, "first_request_ts": self._t0.get(qid), "last_request_ts": now_iso(),
               "hit_count_api": hits, "unit": unit, "n_fetched": n_retrieved if n_fetched is None else n_fetched,
               "n_retrieved": n_retrieved, "n_pages": n_pages, "cap_hit": cap_hit,
               "limit": self.limit, "date_filter": date_filter,
               "credential_mode": mode, "raw_cache_published": pub, "raw_cache_note": why, "notes": notes or {}}
        for field, seen, want in (("date_filter", date_filter, planned), ("raw_cache_published", pub, pub_planned)):
            if want is not None and want != seen:
                rec[f"{field}_planned"] = want
                print(f"  ! {qid}: {field} observed {seen!r}, queries/*.yaml plans {want!r}")
        c = self.counts.setdefault(source, {"queries": {}, "credential_mode": mode})
        c["queries"][qid] = {"hit_count_api": hits, "unit": unit, "role": role, "n_retrieved": n_retrieved,
                             "n_requests": rec["n_requests"], "n_failed_requests": nfail, "partial": part,
                             "cap_hit": cap_hit, "credential_mode": mode}
        self.done.add(qid)
        if not self.dry_run:
            self.rd.update_queries(qid, rec)
        print(f"  {qid:22s} {mode:18s} hits={hits} ({unit}) retrieved={n_retrieved} pages={n_pages} requests={rec['n_requests']}"
              + (f" FAILED={nfail}{'' if part else ' (probed for, not a truncation)'}" if nfail else ""))

    def flush(self) -> None:
        """records/<source>.jsonl per source touched and the merged counts.json; nothing in a dry run.
        hit_count_api_total sums unit=records, role=search only; the rest goes to hit_count_by_unit."""
        if self.dry_run:
            print(f"dry run: {self.n_would} requests would be sent; nothing written")
            return
        for source, bucket in sorted(self.records.items()):
            n = write_jsonl(self.rd.records_file(source), bucket.values())
            self.counts.setdefault(source, {"queries": {}})["n_records_unique"] = n
        for source, c in self.counts.items():
            c.setdefault("n_records_unique", 0)
            c["n_unusable_ids"] = self.n_unusable.get(source, 0)
            qs = c["queries"].values()
            c["hit_count_api_total"] = sum((q["hit_count_api"] or 0) for q in qs if q["unit"] == "records" and q["role"] == "search")
            c["hit_count_by_unit"] = {u: sum((q["hit_count_api"] or 0) for q in qs if q["unit"] == u) for u in UNITS
                                      if any(q["unit"] == u for q in qs)}
            c["n_requests"] = sum(q["n_requests"] for q in qs)
            c["n_failed_requests"] = sum(q.get("n_failed_requests") or 0 for q in qs)
        path = self.rd.root / "counts.json"
        old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        old.update(self.counts)
        dump_json(path, old)


def _get_bytes(run: Run, source, qid, url) -> tuple[int, bytes]:
    """Binary GET (the gzip dump) with the session's contract: sha1 cache key, envelope under
    raw/<source>/<sha1>.json with `body_b64`, one log line (redacted url, cache sha1), a cache hit before
    any network, the envelope written whatever the outcome, and under --replay a ReplayMiss on a miss.
    Returns (status, body); status 0 on error, which is counted against the query like any other failure."""
    if run.dry_run:
        run.get(source, qid, url)
        return 0, b""
    s = run.sess
    sha1, cache = s.cache_path(source, url, {})
    base = {"source": source, "query_id": qid, "method": "GET", "url": redact_text(url), "params": {}, "cache_sha1": sha1, "credential": "none"}
    run.count(qid)
    if cache is not None and cache.exists():
        env = json.loads(cache.read_text(encoding="utf-8"))
        body = base64.b64decode(env.get("body_b64", ""))
        append_jsonl(run.rd.requests_log, {"ts": now_iso(), **base, "attempt": 0, "status": env["status"], "elapsed_ms": 0, "bytes": len(body),
                                           "from_cache": True, "error": env.get("error")})
        # A cached failure is still a failure: counted here as it was counted live, so a replay of a run
        # writes the same n_failed_requests as the run it replays (RateLimitedSession.get does this by
        # returning the envelope's error, which Run.get passes to note_status).
        run.note_status(qid, env["status"], env.get("error"))
        return env["status"], body
    if s.replay:
        append_jsonl(run.rd.requests_log, {"ts": now_iso(), **base, "attempt": 0, "status": 0, "elapsed_ms": 0, "bytes": 0, "from_cache": False,
                                           "error": f"ReplayMiss: no cached body for {source}/{qid} sha1={sha1}"})
        raise ReplayMiss(f"replay: no cached body for {source}/{qid} sha1={sha1}")
    s._wait(source, False)
    t0, status, body, err = time.monotonic(), 0, b"", None
    try:
        r = s.s.get(url, timeout=20)
        status, body = r.status_code, r.content
    except Exception as e:  # noqa: BLE001 - every failure is logged, none is raised
        err = f"{type(e).__name__}: {redact_text(str(e))}"
    ts = now_iso()
    append_jsonl(run.rd.requests_log, {"ts": ts, **base, "attempt": 1, "status": status, "elapsed_ms": int((time.monotonic() - t0) * 1000),
                                       "bytes": len(body), "from_cache": False, "error": err})
    run.note_status(qid, status, err)
    # Cached whatever the outcome, exactly as RateLimitedSession.get does: the PwC dump answered an SSLError on the
    # review run, and a cache holding only the successes cannot replay that.
    if cache is not None:
        dump_json(cache, {"sha1": sha1, "method": "GET", "url": base["url"], "params": {}, "status": status, "headers": {},
                          "retrieved_at": ts, "body_b64": base64.b64encode(body).decode(), "error": err, "attempts": 1})
    return status, body
