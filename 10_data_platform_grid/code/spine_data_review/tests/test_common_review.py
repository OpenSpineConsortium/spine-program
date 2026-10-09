"""Adversarial fixture for sdr.common / sdr.creds / sdr.ids (review of module 'common', 2026-09-19).

Runs offline against a local stdlib HTTP server so every claim in the module docstrings can be
checked against a hand calculation: one log line per attempt, back-off on 429/500 with Retry-After
honoured, a cache file only for a non-retryable answer, ReplayMiss on a cold cache, secret-stripping
by NAME in the log and cache key, redaction by VALUE in error messages, parameters and bodies, the
merge of a URL's own query string into params, the keyed/anonymous cache split, HEAD, redirect
chains and a streamed byte cap, Retry-After as an HTTP-date, the pacing interval per source,
byte-identical outputs
across two runs, the worked examples of PROTOCOL.md 7.1 for ids.py (sha1 checked against
`sha1sum`), and byte-identity of the strings load_queries() reads from information_sources.md
against queries/*.yaml. The real credential store is DISABLED (FLUOROCAP_CREDS points at an empty
directory) and fake values are injected through the environment, so nothing here can leak a real
value; the fake values are asserted absent from every file the session writes.

Usage (WSL):  ~/sdr_venv/bin/python tests/test_common_review.py [--keep]
Writes only under tests/_tmp_common/ (deleted at the end unless --keep). Exit 1 when any check fails.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / "tests" / "_tmp_common"
FAKE = {"NCBI_API_KEY": "FAKEKEY0123456789ABCDEF", "FLUOROCAP_CONTACT_EMAIL": "fake.reviewer@example.org",
        "S2_API_KEY": "FAKES2KEY9876543210", "HF_TOKEN": "hf_FAKETOKEN_abcdefghijklmnop"}
# The real store must not be read by this fixture.
os.environ["FLUOROCAP_CREDS"] = str(TMP / "no_such_store")
os.environ.update(FAKE)
sys.path.insert(0, str(ROOT))

from sdr import common, creds, ids  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


# ----------------------------------------------------------------------------- local server
class Handler(BaseHTTPRequestHandler):
    calls: dict[str, int] = {}

    def log_message(self, *a):  # silence
        pass

    def _send(self, status: int, body: str, extra: dict | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        p = urlsplit(self.path)
        n = Handler.calls[p.path] = Handler.calls.get(p.path, 0) + 1
        if p.path == "/flaky":  # two 429s with Retry-After then 200
            if n <= 2:
                return self._send(429, '{"err":"slow down"}', {"Retry-After": "1"})
            return self._send(200, '{"ok":true,"n":%d}' % n)
        if p.path == "/fail":
            return self._send(500, '{"err":"boom"}')
        if p.path == "/echo":  # an API that echoes the request (Springer echoes apiKey; error pages echo URLs)
            return self._send(200, json.dumps({"query_string": p.query, "path": self.path}))
        if p.path == "/notfound":
            return self._send(404, '{"err":"no"}')
        if p.path == "/redir":  # one hop to /ok, for the allow_redirects=False chain
            return self._send(302, "", {"Location": "/ok?via=redir"})
        if p.path == "/flaky-date":  # one 429 whose Retry-After is an HTTP-date 2 s ahead, then 200
            if n == 1:
                later = format_datetime(datetime.now(timezone.utc) + timedelta(seconds=2), usegmt=True)
                return self._send(429, '{"err":"later"}', {"Retry-After": later})
            return self._send(200, '{"ok":true}')
        if p.path == "/big":
            return self._send(200, "x" * 100000)
        return self._send(200, json.dumps({"path": self.path, "query": p.query}))

    def do_HEAD(self):
        Handler.calls["HEAD"] = Handler.calls.get("HEAD", 0) + 1
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", "2")
        self.end_headers()

    def do_POST(self):
        ln = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(ln).decode("utf-8")
        self._send(200, json.dumps({"posted": body}))


def start_server() -> tuple[HTTPServer, str]:
    srv = HTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def log_rows(rd: common.RunDir) -> list[dict]:
    return list(common.read_jsonl(rd.requests_log))


def files_text(root: Path) -> str:
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in root.rglob("*") if p.is_file())


# ----------------------------------------------------------------------------- tests
def test_creds() -> None:
    check("creds: real store disabled, fake env values loaded",
          creds.cred("NCBI_API_KEY") == FAKE["NCBI_API_KEY"] and not creds.CRED_STORE.exists())
    check("creds: creds_present returns names only", creds.creds_present() == sorted(FAKE))
    check("creds: redact_text scrubs a plain value", "<redacted>" in creds.redact_text("k=" + FAKE["NCBI_API_KEY"]))
    enc = FAKE["FLUOROCAP_CONTACT_EMAIL"].replace("@", "%40")
    check("creds: redact_text scrubs the URL-ENCODED email (requests puts ?mailto=a%40b in exception text)",
          FAKE["FLUOROCAP_CONTACT_EMAIL"].split("@")[0] not in creds.redact_text("url: /x?mailto=" + enc),
          "value survives in encoded form" if enc in creds.redact_text("url: /x?mailto=" + enc) else "")
    check("creds: unpaywall_email falls back to contact name", creds.unpaywall_email() == (FAKE["FLUOROCAP_CONTACT_EMAIL"], "FLUOROCAP_CONTACT_EMAIL"))


def test_ids() -> None:
    doi = "10.1038/s41597-020-00715-8"
    canon = ids.canonical_string({"doi": f"https://doi.org/{doi.upper()}."}, "pubmed", 1)
    check("ids: DOI canonical (prefix stripped, lower-cased, trailing punct)", canon == f"doi:{doi}", canon)
    # hand calculation with sha1sum on the same UTF-8 bytes
    ext = subprocess.run(["sha1sum"], input=canon.encode("utf-8"), capture_output=True).stdout.decode().split()[0]
    check("ids: record_id == lit: + first 12 hex of sha1sum(canonical)", ids.record_id(canon, "pubmed") == f"lit:{ext[:12]}",
          f"{ids.record_id(canon, 'pubmed')} vs sha1sum {ext[:12]}")
    check("ids: repo: prefix for R-sources and dataset-typed crossref", ids.record_id(canon, "zenodo").startswith("repo:")
          and ids.record_id(canon, "crossref", "Dataset").startswith("repo:") and ids.record_id(canon, "crossref", "journal-article").startswith("lit:"))
    check("ids: order doi > pmid > pmcid > arxiv > url > native",
          ids.canonical_string({"pmid": "PMID: 123"}, "x", 9) == "pmid:123"
          and ids.canonical_string({"pmcid": "pmc55"}, "x", 9) == "pmcid:PMC55"
          and ids.canonical_string({"arxiv": "arXiv:2105.14711v2"}, "x", 9) == "arxiv:2105.14711"
          and ids.canonical_string({"url": "HTTP://Zenodo.org/records/10079370/?x=1#f"}, "x", 9) == "url:https://zenodo.org/records/10079370"
          and ids.canonical_string({}, "zenodo", 10079370) == "native:zenodo:10079370")
    try:
        ids.canonical_string({"doi": None, "url": "ftp://x"}, "zenodo", None)
        check("ids: unidentifiable record raises", False)
    except ValueError:
        check("ids: unidentifiable record raises", True)
    check("ids: norm_title NFKC lower alnum", ids.norm_title("VerSe: A Vertebrae Labelling — ﬁne") == "verseavertebraelabellingfine")
    jp = ids.norm_title("腰椎X線画像データセット 2020")
    check("ids: norm_title keeps non-Latin alphanumerics (a J-STAGE title compares as itself, not its ASCII residue)",
          jp == "腰椎x線画像データセット2020", f"-> {jp!r}")
    check("ids: norm_pmcid is anchored: a DOI-like value is None, a PMC URL resolves",
          ids.norm_pmcid("10.1038/x") is None and ids.norm_pmcid("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123/") == "PMC123",
          f"-> {ids.norm_pmcid('10.1038/x')}")
    check("ids: norm_pmid(0) is None and a title ending in a year is None",
          ids.norm_pmid(0) is None and ids.norm_pmid("Lumbar CT 2020") is None, f"-> {ids.norm_pmid(0)!r}")
    rec = {"ids": {"doi": doi}, "title": "CT-ORG, a new dataset for multiple organ segmentation in computed tomography", "year": "2020"}
    check("ids: known_item_matches doi / title-year / url",
          ids.known_item_matches(rec, {"match_rule": "doi", "doi": f"doi:{doi}"}) == "doi"
          and ids.known_item_matches(rec, {"match_rule": "title-year", "title_norm": "ct org a new dataset for multiple organ segmentation in computed tomography", "year": 2021}) == "title-year"
          and ids.known_item_matches({"ids": {"url": "http://zenodo.org/records/1/"}}, {"match_rule": "url", "url": "https://zenodo.org/records/1"}) == "url"
          and ids.known_item_matches(rec, {"match_rule": "title-year", "title_norm": "ct org a new dataset for multiple organ segmentation in computed tomography", "year": 2022}) is None)


def test_queries() -> None:
    md = common.load_queries()
    pipeline = (ROOT / "PIPELINE.md").read_text(encoding="utf-8")
    m_md = re.search(r"(\d+) ids\s+from the markdown", pipeline)
    m_y = re.search(r"the (\d+)\s+materialised entries", pipeline)
    n_md, n_yaml = int(m_md.group(1)) if m_md else 228, int(m_y.group(1)) if m_y else 345
    check(f"queries: load_queries() from markdown returns the {n_md} ids PIPELINE.md states", len(md) == n_md, f"n={len(md)}")
    mism, n_checked, ys = [], 0, {}
    for yf in ("queries/literature.yaml", "queries/repositories.yaml"):
        try:
            ys[yf] = common.load_queries(ROOT / yf)
        except Exception as e:  # noqa: BLE001 - a malformed query file is a failed check, not a crash
            ys[yf] = {}
            check(f"queries: {yf} parses", False, f"{type(e).__name__}: {str(e).splitlines()[-1][:120]}")
    for yf, y in ys.items():
        for qid, e in y.items():
            if e.get("verbatim_in_markdown") is True:
                mid = e.get("markdown_id") or e.get("grid_id") or qid
                n_checked += 1
                if mid not in md:
                    mism.append(f"{yf}:{qid}: markdown id {mid} not loaded")
                elif md[mid]["string"] != e["string"]:
                    mism.append(f"{yf}:{qid}: differs from markdown {mid}")
    check(f"queries: every verbatim_in_markdown entry ({n_checked}) is byte-identical to load_queries() from the markdown",
          not mism, "; ".join(mism[:5]))
    # the YAML has entries the markdown does not (operational forms); count them so the appendix knows
    y_all = {k: v for y in ys.values() for k, v in y.items()}
    check(f"queries: YAML entry count is the {n_yaml} PIPELINE.md states", len(y_all) == n_yaml, f"n={len(y_all)}")


def test_session(base: str) -> None:
    rd = common.init_run_dir(TMP / "runA", "2026-09-19", ["fixture", FAKE["NCBI_API_KEY"]])
    meta = json.loads(rd.meta.read_text())
    check("run_meta: argv redacted by value", FAKE["NCBI_API_KEY"] not in rd.meta.read_text() and meta["invocations"][0]["argv"][1] == "<redacted>")
    sess = common.RateLimitedSession(rd)
    src = "fixture"  # unlisted source -> 0.5 s interval
    # 1. two 429 (Retry-After: 1) then 200: three attempts, three log lines, back-off >= 1 s each, one cache file
    t0 = time.monotonic()
    r = sess.get(src, "q1", base + "/flaky", {"api_key": FAKE["NCBI_API_KEY"], "term": "spine"}, credential="NCBI_API_KEY")
    dt = time.monotonic() - t0
    rows = log_rows(rd)
    check("session: 429,429,200 -> status 200 after three attempts", r.ok and [x["attempt"] for x in rows] == [1, 2, 3], str([x["status"] for x in rows]))
    check("session: back-off honoured (Retry-After 1 s twice -> >= 2 s, < 8 s)", 2.0 <= dt < 8.0, f"{dt:.2f}s")
    cache = rd.raw / src / f"{r.sha1}.json"
    check("session: cache file written for the 200", cache.exists())
    env = json.loads(cache.read_text())
    check("session: cache envelope has sha1/method/url/params/status/headers/retrieved_at/body",
          set(env) >= {"sha1", "method", "url", "params", "status", "headers", "retrieved_at", "body"})
    check("session: api_key redacted by NAME in log params and cache envelope", all(x["params"]["api_key"] == "<redacted>" for x in rows) and env["params"]["api_key"] == "<redacted>")
    check("session: credential logged by name", all(x["credential"] == "NCBI_API_KEY" for x in rows))
    # 2. second call is served from cache: attempt 0, from_cache true, no network call
    n_before = Handler.calls.get("/flaky", 0)
    r2 = sess.get(src, "q1", base + "/flaky", {"api_key": FAKE["NCBI_API_KEY"], "term": "spine"}, credential="NCBI_API_KEY")
    rows = log_rows(rd)
    check("session: cache hit -> from_cache, attempt 0, no network", r2.from_cache and rows[-1]["attempt"] == 0 and rows[-1]["from_cache"] is True
          and Handler.calls.get("/flaky", 0) == n_before and r2.text == r.text)
    # 3. 500 x5: five attempts, no cache file, final status 500, error None
    n0 = len(rows)
    r3 = sess.get(src, "q2", base + "/fail")
    rows = log_rows(rd)
    check("session: 500 x5 -> five attempts logged, status 500 returned, not cached",
          r3.status == 500 and len(rows) - n0 == 5 and not (rd.raw / src / f"{r3.sha1}.json").exists())
    # 4. 404 is cached (non-retryable) and replays
    r4 = sess.get(src, "q3", base + "/notfound")
    check("session: 404 cached (non-retryable answer)", (rd.raw / src / f"{r4.sha1}.json").exists())
    # 5. replay: hit served, miss raises ReplayMiss
    rp = common.RateLimitedSession(rd, replay=True)
    ok = rp.get(src, "q3", base + "/notfound").from_cache
    try:
        rp.get(src, "q9", base + "/never")
        miss = False
    except common.ReplayMiss:
        miss = True
    check("session: --replay serves the cache and raises ReplayMiss on a miss", ok and miss)
    # 6. cache_salt disambiguates identical URL+params (S2 token pages)
    a = sess.get(src, "q4", base + "/ok", {"token": "p1"}, cache_salt="p1")
    b = sess.get(src, "q4", base + "/ok", {"token": "p2"}, cache_salt="p2")
    c = sess.get(src, "q4", base + "/ok", {"token": "p3"})  # no salt: collides with nothing yet, but
    d = sess.get(src, "q4", base + "/ok", {"token": "p4"})  # ... p4 lands on p3's cache file
    check("session: cache_salt separates redacted-param pages", a.sha1 != b.sha1)
    check("session: redacted param WITHOUT cache_salt collides (documented trap; adapters must pass the salt)",
          c.sha1 == d.sha1 and d.from_cache and json.loads(d.text)["query"] == "token=p3", "p4 served p3's body")
    # 7. a URL that carries its own query string: the query is merged into params, so key and log see it
    e = sess.get(src, "q5", base + "/ok?a=1")
    f = sess.get(src, "q5", base + "/ok?a=2")
    check("session: URL with embedded query -> distinct cache keys, second request fetched, body of ?a=2",
          e.sha1 != f.sha1 and not f.from_cache and json.loads(f.text)["query"] == "a=2", f"from_cache={f.from_cache}")
    q5 = [x for x in log_rows(rd) if x["query_id"] == "q5"]
    check("session: URL query string moved into logged params, url logged without it",
          [x["params"].get("a") for x in q5] == ["1", "2"] and all("?" not in x["url"] for x in q5))
    check("session: explicit params win over the URL query and is_cached agrees with get",
          sess.get(src, "q5", base + "/ok?a=9", {"a": "2"}).from_cache and sess.is_cached(src, base + "/ok?a=2"))
    # 8. POST body is in the key
    p1 = sess.get(src, "q6", base + "/post", method="POST", data='{"q":1}')
    p2 = sess.get(src, "q6", base + "/post", method="POST", data='{"q":2}')
    check("session: POST data is part of the cache key", p1.sha1 != p2.sha1 and not p2.from_cache)
    # 9. value in a NON-listed parameter name and an echoing body
    sess.get(src, "q7", base + "/echo", {"user": FAKE["NCBI_API_KEY"], "mailto": FAKE["FLUOROCAP_CONTACT_EMAIL"]})
    txt = files_text(rd.root)
    check("session: a credential value in a parameter NOT in SECRET_PARAMS (`user`) is redacted by value in log and cache",
          FAKE["NCBI_API_KEY"] not in txt, "value found in run files")
    body = json.loads((rd.raw / src / f"{sess.get(src, 'q7', base + '/echo', {'user': FAKE['NCBI_API_KEY'], 'mailto': FAKE['FLUOROCAP_CONTACT_EMAIL']}).sha1}.json").read_text())["body"]
    check("session: a response body that echoes the request (Springer echoes apiKey; error pages echo URLs) is cached redacted",
          FAKE["NCBI_API_KEY"] not in body and "fake.reviewer" not in body and "<redacted>" in body, "raw body holds the api key or the email")
    # 10. exception text: URL-encoded email in a requests error message
    sess.get("dead", "q8", "https://nonexistent-host.invalid/x", {"mailto": FAKE["FLUOROCAP_CONTACT_EMAIL"], "api_key": FAKE["NCBI_API_KEY"]}, retries=1)
    err = [x for x in log_rows(rd) if x["query_id"] == "q8"][-1]["error"] or ""
    check("session: connection error logged, redacted by value (plain form)", err and FAKE["NCBI_API_KEY"] not in err and FAKE["FLUOROCAP_CONTACT_EMAIL"] not in err, err[:120])
    check("session: URL-encoded email (a%40b) is redacted in the logged error",
          "fake.reviewer%40example.org" not in err and "fake.reviewer" not in err,
          "encoded email present in requests.log error field" if "%40" in err else "")
    # 11. pacing: 'zenodo' interval 1 s -> three calls take >= 2 s; unlisted 0.5 s -> three calls >= 1 s
    t0 = time.monotonic()
    for i in range(3):
        sess.get("zenodo", "q10", base + "/ok", {"i": i})
    dz = time.monotonic() - t0
    t0 = time.monotonic()
    for i in range(3):
        sess.get("unlisted", "q11", base + "/ok", {"i": i})
    du = time.monotonic() - t0
    check("session: pacing zenodo 1/s (3 calls >= 2.0 s) and default 2/s (3 calls >= 1.0 s)", dz >= 2.0 and du >= 1.0, f"zenodo {dz:.2f}s unlisted {du:.2f}s")
    check("session: rate_for table matches information_sources.md (ncbi 0.1/0.333, s2 1/5, openalex 0.5, arxiv 3, github 2/6, commons 1)",
          (common.rate_for("pubmed", True), round(common.rate_for("pubmed"), 3), common.rate_for("s2", True), common.rate_for("s2"),
           common.rate_for("openalex", True), common.rate_for("arxiv"), common.rate_for("github", True), common.rate_for("github"), common.rate_for("commons"))
          == (0.1, 0.333, 1.0, 5.0, 0.5, 3.0, 2.0, 6.0, 1.0))
    # 12. every logged row has the protocol section-15 fields
    need = {"ts", "source", "query_id", "attempt", "method", "url", "params", "status", "elapsed_ms", "bytes", "cache_sha1", "from_cache", "credential", "error"}
    check("log: every row carries the section-15 fields", all(set(x) == need for x in log_rows(rd)), str(set(log_rows(rd)[0]) ^ need))
    # 13. no fake value anywhere in the run dir except the two documented leak paths (q7 echo/user)
    leak_files = [p for p in rd.root.rglob("*") if p.is_file() and any(v in p.read_text(errors="replace") for v in FAKE.values())]
    check("no file in the run dir holds a credential value", not leak_files, str([p.name for p in leak_files]))
    # 14. keyed and anonymous answers to one URL are stored apart; anonymous key material is unchanged
    ka = sess.get(src, "q12", base + "/ok", {"k": "1"})
    kb = sess.get(src, "q12", base + "/ok", {"k": "1"}, keyed=True)
    hand = hashlib.sha1("\n".join(["GET", base + "/ok", json.dumps({"k": "1"}), "", ""]).encode()).hexdigest()
    check("session: keyed request has its own cache key; anonymous key equals the five-line hand calculation",
          ka.sha1 != kb.sha1 and not kb.from_cache and ka.sha1 == hand, f"{ka.sha1[:8]} vs hand {hand[:8]}")
    # 15. HEAD, a redirect chain with allow_redirects=False, and a streamed byte cap
    h = sess.get(src, "q13", base + "/ok", method="HEAD")
    rc = sess.get(src, "q13", base + "/redir", allow_redirects=False, full_headers=True)
    big = sess.get(src, "q13", base + "/big", stream_cap=1000)
    check("session: HEAD returns the status with an empty body and is cached",
          h.ok and h.text == "" and sess.get(src, "q13", base + "/ok", method="HEAD").from_cache)
    check("session: allow_redirects=False records the hop chain and the final url",
          rc.ok and rc.chain == [302, 200] and (rc.final_url or "").endswith("/ok?via=redir"), f"chain={rc.chain} final={rc.final_url}")
    env_rc = json.loads((rd.raw / src / f"{rc.sha1}.json").read_text())
    check("session: envelope carries chain/final_url and a replay returns them",
          env_rc.get("chain") == [302, 200] and sess.get(src, "q13", base + "/redir", allow_redirects=False).chain == [302, 200])
    check("session: stream_cap reads at most that many bytes", big.ok and len(big.text) == 1000, f"len={len(big.text)}")
    # 16. Retry-After as an HTTP-date is honoured (2 s ahead raises the 1 s ladder step to about 2 s)
    t0 = time.monotonic()
    fd = sess.get(src, "q14", base + "/flaky-date")
    dfd = time.monotonic() - t0
    check("session: Retry-After HTTP-date honoured (waited >= 1.5 s, < 8 s)", fd.ok and 1.5 <= dfd < 8.0, f"{dfd:.2f}s status {fd.status}")


def test_determinism(base: str) -> None:
    Handler.calls.clear()
    outs = []
    for name in ("runB", "runC"):
        rd = common.init_run_dir(TMP / name, "2026-09-19", ["fixture"])
        s = common.RateLimitedSession(rd)
        for i in (2, 0, 1):
            s.get("det", "q1", base + "/ok", {"i": i, "term": "spine CT"})
        common.write_jsonl(rd.records_file("det"), [{"record_id": "b", "x": 1}, {"record_id": "a", "x": 2}])
        rd.update_queries("q1", {"source": "det", "hit_count_api": 3})
        strip = lambda t: "\n".join(l for l in t.splitlines() if '"ts"' not in l and "retrieved_at" not in l and "created_at" not in l and "elapsed_ms" not in l)  # noqa: E731
        outs.append({str(p.relative_to(rd.root)): strip(p.read_text()) for p in sorted(rd.root.rglob("*")) if p.is_file()})
    same = outs[0].keys() == outs[1].keys() and all(outs[0][k] == outs[1][k] for k in outs[0] if k != "requests.log.jsonl")
    log_same = [json.loads(l) for l in outs[0]["requests.log.jsonl"].splitlines()] == [json.loads(l) for l in outs[1]["requests.log.jsonl"].splitlines()]
    check("determinism: two runs give identical file set, cache sha1 names, records, queries.json (ignoring ts/retrieved_at/created_at/elapsed_ms)", same, str(sorted(outs[0])))
    check("determinism: request logs identical apart from timestamps/elapsed", log_same)
    check("determinism: write_jsonl sorts by record_id", [r["record_id"] for r in common.read_jsonl(TMP / "runB" / "records" / "det.jsonl")] == ["a", "b"])


def test_guards() -> None:
    for fn, arg in ((common.dump_json, (Path("/tmp/sdr_guard.json"), {})), (common.append_jsonl, (Path("/tmp/sdr_guard.jsonl"), {})),
                    (common.write_jsonl, (Path("/tmp/sdr_guard2.jsonl"), []))):
        try:
            fn(*arg)
            check(f"guard: {fn.__name__} refuses a path outside the root", False)
        except ValueError:
            check(f"guard: {fn.__name__} refuses a path outside the root", not Path(arg[0]).exists())
    try:
        common.resolve_run_dir("../outside")
        check("guard: resolve_run_dir refuses ../outside", False)
    except ValueError:
        check("guard: resolve_run_dir refuses ../outside", True)
    for bad in (".", "runs", "tests", "charting/x"):
        try:
            common.resolve_run_dir(bad)
            check(f"guard: resolve_run_dir refuses {bad!r}", False)
        except ValueError:
            check(f"guard: resolve_run_dir refuses {bad!r}", True)
    check("guard: resolve_run_dir accepts runs/<date> and tests/<fixture>",
          common.resolve_run_dir("runs/2026-09-19") == ROOT / "runs" / "2026-09-19" and common.resolve_run_dir(TMP / "x") == TMP / "x")
    try:
        common.init_run_dir(TMP / "bad", "20260919")
        check("guard: init_run_dir rejects a non ISO run date", False)
    except ValueError:
        check("guard: init_run_dir rejects a non ISO run date", True)


def main() -> int:
    keep = "--keep" in sys.argv
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True)
    srv, base = start_server()
    try:
        test_creds()
        test_ids()
        test_queries()
        test_session(base)
        test_determinism(base)
        test_guards()
    finally:
        srv.shutdown()
        if not keep:
            shutil.rmtree(TMP, ignore_errors=True)
    n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks passed; {n_fail} failed")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
