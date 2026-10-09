"""Audit one run directory against the engineering rules of PROTOCOL.md section 15.

Checks, each printed as PASS/FAIL with the offending items:
  log-cache    every non-retry, error-free request in requests.log.jsonl has raw/<source>/<sha1>.json
               whose envelope sha1 and status match, and every raw file has a log line - a failed
               request is cached too (its envelope carries `error` and `attempts`, so --replay
               reproduces the failure), and its own log line accounts for the file
  log-fields   every log line carries the section-15 fields; url/params never contain a value of a
               SECRET_PARAMS name un-redacted
  strings      queries.json[qid].query_string equals the string in queries/*.yaml (or, for a
               run-time sub-id, its base id) - the verbatim-string rule of PROTOCOL.md 6.3
  no-answer    a query whose requests were mostly transport errors or 5xx says so in its notes
               (n_failed_requests, or a "status N at ..." note). A source that never answered must not
               be readable as a source that answered zero: those are different findings and only one
               of them belongs in Table 2 as a count
  paging       for search queries with a numeric hit count, n_retrieved == min(hit_count_api, limit)
               unless the record explains itself (dump-filter grammar, cap_hit, a note)
  secrets      no credential VALUE from ~/.fluorocap/credentials.env appears in any file under the
               run dir or under the review directory outside runs/*/raw (only names are printed)
  wallclock    no ISO date other than the run date appears in outputs outside the timestamp fields
               (ts, retrieved_at, first/last_request_ts, created_at, probe date), the `intervals` of a
               query (its own planned date windows) and any date a query's own intervals or frozen
               string already contain (a bioRxiv note restating its monthly bounds is not a wall clock)
Exit 1 on secrets, log-cache, log-fields, strings, no-answer or wallclock; paging is printed only.
Usage: ~/sdr_venv/bin/python tests/check_run.py --run-dir runs/<name> --run-date YYYY-MM-DD [--limit N]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sdr.common import RETRY_STATUSES, SECRET_PARAMS, load_queries, read_jsonl  # noqa: E402

TS_KEYS = {"ts", "retrieved_at", "first_request_ts", "last_request_ts", "created_at", "date", "probed_at", "charted_date", "verified_date"}
# Not a timestamp: `intervals` is the query's own plan (the monthly windows bioRxiv is paged by), so the
# dates in it are frozen protocol content, not a wall clock leaking into an output.
SKIP_KEYS = TS_KEYS | {"intervals"}
# Fields of a records/*.jsonl row that are copied from the source (or derived from what it sent, like `canonical`
# from `ids`); the wallclock rule reads only what the pipeline itself writes into a record.
RECORD_SOURCE_KEYS = {"raw", "abstract_or_description", "title", "ids", "canonical", "first_author",
                      "related_identifiers", "concept_doi"}
LOG_FIELDS = {"ts", "source", "query_id", "attempt", "method", "url", "params", "status", "elapsed_ms", "bytes", "cache_sha1", "from_cache", "credential", "error"}


def load_cred_values() -> dict[str, str]:
    p = Path(os.path.expanduser("~/.fluorocap/credentials.env"))
    out = {}
    if p.exists():
        for ln in p.read_text(encoding="utf-8").splitlines():
            if "=" in ln and not ln.lstrip().startswith("#"):
                k, v = ln.split("=", 1)
                v = v.strip().strip("'\"")
                if len(v) >= 6:
                    out[k.strip()] = v
    return out


def base_id(qid: str, known: set[str]) -> str | None:
    """pubmed_01a -> pubmed_01; openalex_01_g01 -> openalex_01; openi_03_xg -> openi_03; crossref_12a -> crossref_12."""
    if qid in known:
        return qid
    for pat in (r"^(.*_\d+)[a-z]$", r"^(.*_\d+)_g\d+$", r"^(.*_\d+)_(c|xg)$", r"^(.*)_\d{4}$"):
        m = re.match(pat, qid)
        if m and m.group(1) in known:
            return m.group(1)
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--run-date", required=True)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    rd = (ROOT / a.run_dir).resolve()
    fails: dict[str, list[str]] = {}

    def fail(check, msg):
        fails.setdefault(check, []).append(msg)

    # ---- log-fields and log-cache
    log = list(read_jsonl(rd / "requests.log.jsonl"))
    seen_raw = set()
    for i, row in enumerate(log):
        miss = LOG_FIELDS - set(row)
        if miss:
            fail("log-fields", f"line {i}: missing {sorted(miss)}")
        for k, v in (row.get("params") or {}).items():
            if k.lower() in SECRET_PARAMS and v != "<redacted>":
                fail("log-fields", f"line {i}: param {k} not redacted")
        if re.search(r"[?&](api_key|apikey|key|token|access_token|mailto|email)=", row.get("url", "")):
            fail("log-fields", f"line {i}: secret-named parameter inside url")
        raw = rd / "raw" / row["source"] / f"{row['cache_sha1']}.json"
        if row.get("error") is None and row.get("status") not in RETRY_STATUSES and row.get("status", 0) != 0:
            if not raw.exists():
                fail("log-cache", f"line {i}: {row['source']}/{row['query_id']} status {row['status']} has no raw file {raw.name}")
            else:
                env = json.loads(raw.read_text(encoding="utf-8"))
                if env.get("sha1") != row["cache_sha1"] or env.get("status") != row["status"]:
                    fail("log-cache", f"line {i}: envelope sha1/status mismatch for {raw.name}")
                seen_raw.add(raw)
        elif raw.exists() and json.loads(raw.read_text(encoding="utf-8")).get("sha1") == row["cache_sha1"]:
            # A request that never answered is cached too, with its `error` and `attempts` (PROTOCOL.md 19,
            # 2026-09-19): Figshare's deliberate 500 and the PwC dump's SSLError are part of what the run
            # observed, and --replay could not reproduce them otherwise. The file is accounted for by the
            # failed line that produced it, so it is not a raw file without a log line.
            seen_raw.add(raw)
    for raw in (rd / "raw").rglob("*.json") if (rd / "raw").exists() else []:
        if raw not in seen_raw:
            fail("log-cache", f"raw file without a successful log line: {raw.relative_to(rd)}")
    print(f"requests logged: {len(log)}; raw files: {len(seen_raw)}")

    # ---- strings
    q = json.loads((rd / "queries.json").read_text(encoding="utf-8")) if (rd / "queries.json").exists() else {}
    yam = {**load_queries(ROOT / "queries" / "literature.yaml"), **load_queries(ROOT / "queries" / "repositories.yaml")}
    md = load_queries()
    known = set(yam) | set(md)
    frozen: dict[str, str] = {}
    for qid, r in sorted(q.items()):
        b = base_id(qid, known)
        if b is None:
            fail("strings", f"{qid}: no base id in queries/*.yaml or information_sources.md")
            continue
        exp = (yam.get(b) or md.get(b) or {}).get("string")
        frozen[qid] = str(exp or "")
        got = r.get("query_string")
        if got != exp:
            fail("strings", f"{qid} (base {b}): json={str(got)[:90]!r} yaml={str(exp)[:90]!r}")

    # ---- no-answer: a query whose requests mostly did not answer must say so in its notes.
    # Counted from the log, not from the notes, so the notes are checked against what happened.
    att: dict[str, int] = {}
    bad: dict[str, int] = {}
    for row in log:
        qid = row.get("query_id")
        if qid not in q:                        # creds-check probes, availability probes: no queries.json entry
            continue
        att[qid] = att.get(qid, 0) + 1
        st = row.get("status") or 0
        if row.get("error") is not None or st == 0 or st >= 500:
            bad[qid] = bad.get(qid, 0) + 1
    for qid, n_bad in sorted(bad.items()):
        if n_bad * 2 <= att.get(qid, 0):        # a retried 5xx that then answered is not a source that went quiet
            continue
        rec = q[qid]
        notes = rec.get("notes")
        txt = notes if isinstance(notes, str) else json.dumps(notes, sort_keys=True)
        if int(rec.get("n_failed_requests") or 0) > 0:
            continue                            # the repository adapters record it as a field of the entry
        if not re.search(r"n_failed_requests|status \d+ at |not_run_reason|no answer", txt or ""):
            fail("no-answer", f"{qid}: {n_bad} of {att[qid]} requests did not answer, notes say nothing: {str(txt)[:80]!r}")

    # ---- paging
    for qid, r in sorted(q.items()):
        if r.get("role", "search") != "search":
            continue
        hits, got = r.get("hit_count_api"), r.get("n_retrieved")
        if not isinstance(hits, int) or got is None or r.get("cap_hit") or r.get("grammar") in ("dump-filter", "list") or r.get("notes"):
            continue
        want = min(hits, a.limit) if a.limit else hits
        if got != want:
            fail("paging", f"{qid}: hit_count_api={hits} limit={a.limit} n_retrieved={got} (expected {want})")

    # ---- secrets
    creds = load_cred_values()
    scan_roots = [rd, ROOT / "tables", ROOT / "manuscript", ROOT / "analysis", ROOT / "charting", ROOT / "recipe", ROOT / "figures"]
    hits_by_name: dict[str, int] = {}
    for root in scan_roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix not in (".pdf", ".png", ".fls", ".fdb_latexmk"):
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                for name, val in creds.items():
                    if val in txt:
                        hits_by_name[name] = hits_by_name.get(name, 0) + 1
                        fail("secrets", f"value of {name} found in {p.relative_to(ROOT)}")
    print(f"credential names checked: {len(creds)}; files with a value: {sum(hits_by_name.values())}")

    # ---- wallclock
    date_re = re.compile(r"\b(20\d\d-\d\d-\d\d)")
    # A query may legitimately carry dates that are not the run date: the monthly windows a source is
    # paged by (`intervals`, skipped outright above) and any restatement of them in `notes` or in the
    # frozen string. Allowed per query id; a date is exempt only where its own query id is on the path.
    allowed: dict[str, set[str]] = {}
    for qid, r in q.items():
        ds = set(date_re.findall(json.dumps(r.get("intervals") or [])))
        ds |= set(date_re.findall(frozen.get(qid, "")))
        ds |= set(date_re.findall(str(r.get("query_string") or "")))
        if ds:
            allowed[qid] = ds

    def exempt(path: str, d: str) -> bool:
        return any(d in ds for qid, ds in allowed.items() if qid in path)

    def walk(obj, path, out):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in SKIP_KEYS:
                    continue
                walk(v, f"{path}.{k}", out)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]", out)
        elif isinstance(obj, str):
            for d in date_re.findall(obj):
                if d != a.run_date and not (d.startswith("2000-") or d.endswith("-01-01") or d.endswith("-12-31")):
                    out.append((path, d))

    for p in sorted(rd.glob("*.json")) + sorted(rd.glob("records/*.jsonl")) + sorted((rd / "analysis").glob("*.json")):
        out: list = []
        if p.suffix == ".jsonl":
            for i, row in enumerate(read_jsonl(p)):
                # What a record copies from its source is the source's text, not a clock of ours: a DOI, a title, a
                # repository name or an identifier can carry a date (10.1002/...2006-01-13, a GitHub repo named for its
                # release day). The first full run (2026-09-23) failed on 39 of them; the rule is about dates the
                # pipeline writes, so the source-copied fields are skipped like `raw` (PROTOCOL.md 19, 2026-09-24).
                row = {k: v for k, v in row.items() if k not in RECORD_SOURCE_KEYS}
                walk(row, f"{p.name}[{i}]", out)
        else:
            walk(json.loads(p.read_text(encoding="utf-8")), p.name, out)
        out = [(path, d) for path, d in out if not exempt(path, d)]
        for path, d in out[:5]:
            fail("wallclock", f"{path}: {d}")
        if len(out) > 5:
            fail("wallclock", f"{p.name}: {len(out) - 5} more")

    for check in ("log-fields", "log-cache", "strings", "no-answer", "paging", "secrets", "wallclock"):
        items = fails.get(check, [])
        print(f"{'FAIL' if items else 'PASS'} {check}" + (f" ({len(items)})" if items else ""))
        for it in items[:25]:
            print("   ", it)
        if len(items) > 25:
            print(f"    ... {len(items) - 25} more")
    # Fatal: every check the adapters now pass. `paging` is printed only, because a source that reports a
    # total it does not serve (a ceiling, a moving index) is the source's behaviour, not the run's fault.
    return 1 if any(fails.get(c) for c in ("secrets", "log-cache", "log-fields", "strings", "no-answer", "wallclock")) else 0


if __name__ == "__main__":
    sys.exit(main())
