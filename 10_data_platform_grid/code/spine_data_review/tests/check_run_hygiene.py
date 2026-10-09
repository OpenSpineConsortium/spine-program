"""Run-directory hygiene for the search stage: secrets, log/cache completeness, determinism.

WHY. The protocol's evidence is the run directory. Three things must hold for it and are cheap to
break: no credential value anywhere in it (section 15); every HTTP attempt logged and every
answered request cached so --replay works; and two runs of the same strings producing the same
records apart from the retrieval timestamps. This script checks them without printing a value.

Usage: ~/sdr_venv/bin/python tests/check_run_hygiene.py --run-dir runs/A [--other runs/B] [--stdout-log tests/x.log]
Credential values are read from ~/.fluorocap/credentials.env (and env) into memory only; output is
the credential NAME and the number of files containing its value.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RETRY = {429, 500, 502, 503, 504}
TS_KEYS = {"retrieved_at", "first_request_ts", "last_request_ts", "ts", "created_at"}


def secret_values() -> dict[str, str]:
    vals: dict[str, str] = {}
    p = Path.home() / ".fluorocap" / "credentials.env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\s*([A-Z][A-Z0-9_]+)\s*=\s*(.+?)\s*$", line)
            if m and len(m.group(2).strip("'\"")) >= 6:
                vals[m.group(1)] = m.group(2).strip("'\"")
    for n in ("HF_TOKEN", "GITHUB_TOKEN", "OSF_TOKEN", "NCBI_API_KEY", "S2_API_KEY"):
        if os.environ.get(n) and len(os.environ[n]) >= 6:
            vals[n] = os.environ[n]
    kj = Path.home() / ".kaggle" / "kaggle.json"
    if kj.exists():
        try:
            vals["KAGGLE_KEY"] = json.loads(kj.read_text())["key"]
        except Exception:
            pass
    return vals


def scan_secrets(run_dir: Path, extra: list[Path]) -> int:
    vals = secret_values()
    files = [p for p in run_dir.rglob("*") if p.is_file()] + [p for p in extra if p.exists()]
    hits = Counter()
    for p in files:
        try:
            t = p.read_bytes()
        except OSError:
            continue
        for name, v in vals.items():
            if v.encode("utf-8") in t:
                hits[name] += 1
    print(f"secrets: {len(vals)} credential values known by name ({sorted(vals)}); {len(files)} files scanned")
    for name, n in sorted(hits.items()):
        print(f"  LEAK {name}: value found in {n} file(s)")
    if not hits:
        print("  no credential value found in any file")
    return len(hits)


def usable(run_dir: Path, what: str) -> bool:
    """Is there a run to read? A missing directory or a missing requests.log.jsonl is the ordinary state of
    `--other` when no twin run has been built, and the prescribed review command ends on it; it is reported
    as a skipped comparison, not as a traceback out of read_text()."""
    if not run_dir.exists():
        print(f"{what}: {run_dir} does not exist; nothing scanned")
        return False
    if not (run_dir / "requests.log.jsonl").exists():
        print(f"{what}: {run_dir} holds no requests.log.jsonl (an empty or unstarted run); nothing scanned")
        return False
    return True


def scan_log(run_dir: Path) -> int:
    log = run_dir / "requests.log.jsonl"
    rows = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]
    bad = 0
    need = {"ts", "source", "query_id", "attempt", "method", "url", "params", "status", "elapsed_ms", "bytes", "cache_sha1", "from_cache", "credential", "error"}
    missing = [r for r in rows if not need <= set(r)]
    print(f"log: {len(rows)} attempts, {len({r['cache_sha1'] for r in rows})} distinct cache keys, sources {len({r['source'] for r in rows})}")
    print(f"  attempts missing a section-15 field: {len(missing)}")
    bad += bool(missing)
    unred = [r for r in rows if any(k.lower() in ("api_key", "apikey", "key", "token", "access_token", "email", "mailto") and v != "<redacted>"
                                    for k, v in (r.get("params") or {}).items())]
    print(f"  attempts with an unredacted secret parameter: {len(unred)}")
    bad += bool(unred)
    urlq = [r for r in rows if "?" in r["url"] or "@" in r["url"]]
    print(f"  attempts whose logged url carries a query string or '@': {len(urlq)}")
    creds = Counter(r["credential"] for r in rows)
    print(f"  credential field values (names only): {dict(creds)}")
    # every final, non-retry, error-free attempt must have a cache file
    final = {}
    for r in rows:
        final[r["cache_sha1"]] = r
    nocache = [r for r in final.values() if r["error"] is None and r["status"] not in RETRY and r["status"] != 0
               and not (run_dir / "raw" / r["source"] / f"{r['cache_sha1']}.json").exists()]
    print(f"  answered requests without a raw cache file: {len(nocache)}" + (f" e.g. {[(r['source'], r['query_id'], r['status']) for r in nocache[:5]]}" if nocache else ""))
    bad += bool(nocache)
    errs = Counter((r["source"], r["status"]) for r in rows if r["error"] or r["status"] >= 400 or r["status"] == 0)
    print(f"  attempts with error / status>=400 / no answer by (source, status): {dict(errs)}")
    q = json.loads((run_dir / "queries.json").read_text(encoding="utf-8")) if (run_dir / "queries.json").exists() else {}
    n_req = sum(int(v.get("n_requests") or 0) for v in q.values())
    print(f"  queries.json: {len(q)} ids, sum n_requests = {n_req} (None for {sum(1 for v in q.values() if v.get('n_requests') is None)} ids) vs log attempts {len(rows)}")
    orphan_q = sorted({r["query_id"] for r in rows} - set(q) - {"check"})
    print(f"  query_ids in the log with no queries.json entry: {len(orphan_q)} {orphan_q[:20]}")
    return bad


def strip_ts(o):
    if isinstance(o, dict):
        return {k: strip_ts(v) for k, v in o.items() if k not in TS_KEYS}
    if isinstance(o, list):
        return [strip_ts(x) for x in o]
    return o


def compare(a: Path, b: Path) -> int:
    bad = 0
    ra = sorted(p.name for p in (a / "records").glob("*.jsonl"))
    rb = sorted(p.name for p in (b / "records").glob("*.jsonl"))
    print(f"determinism: records files A={len(ra)} B={len(rb)}; only in one side: {sorted(set(ra) ^ set(rb))}")
    for name in sorted(set(ra) & set(rb)):
        la = [strip_ts(json.loads(l)) for l in (a / "records" / name).read_text(encoding="utf-8").splitlines() if l.strip()]
        lb = [strip_ts(json.loads(l)) for l in (b / "records" / name).read_text(encoding="utf-8").splitlines() if l.strip()]
        ida, idb = [r["record_id"] for r in la], [r["record_id"] for r in lb]
        same_ids, same_rows = ida == idb, la == lb
        if not same_rows:
            bad += 1
            diff_fields = Counter()
            for x, y in zip(la, lb):
                if x["record_id"] == y["record_id"]:
                    for k in set(x) | set(y):
                        if x.get(k) != y.get(k):
                            diff_fields[k] += 1
            print(f"  {name:16s} A={len(la):3d} B={len(lb):3d} ids {'same' if same_ids else 'DIFFER'}; "
                  f"{'rows identical' if same_rows else 'rows differ in ' + str(dict(diff_fields))}"
                  + (f"; ids only in A {len(set(ida) - set(idb))}, only in B {len(set(idb) - set(ida))}" if not same_ids else ""))
    qa = strip_ts(json.loads((a / "queries.json").read_text(encoding="utf-8")))
    qb = strip_ts(json.loads((b / "queries.json").read_text(encoding="utf-8")))
    keys = sorted(set(qa) | set(qb))
    dq = Counter()
    for k in keys:
        x, y = qa.get(k, {}), qb.get(k, {})
        for f in set(x) | set(y):
            if x.get(f) != y.get(f):
                dq[f] += 1
    print(f"  queries.json: {len(keys)} ids; ids on one side only {sorted(set(qa) ^ set(qb))}; fields differing (field: n ids) {dict(dq)}")
    stable = {k for k in keys if all(qa.get(k, {}).get(f) == qb.get(k, {}).get(f) for f in ("query_string", "endpoint", "params", "grammar", "credential_mode", "source", "role"))}
    print(f"  ids with identical query_string/endpoint/params/grammar/credential_mode/source/role: {len(stable)}/{len(keys)}")
    bad += len(keys) - len(stable)
    return bad


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--other", default=None, help="a second run directory to compare for determinism")
    ap.add_argument("--stdout-log", action="append", default=[], help="captured stdout/stderr files to include in the secret scan")
    a = ap.parse_args(argv)
    rd = Path(a.run_dir) if Path(a.run_dir).is_absolute() else ROOT / a.run_dir
    if not usable(rd, "run-dir"):
        return 2
    bad = scan_secrets(rd, [Path(p) if Path(p).is_absolute() else ROOT / p for p in a.stdout_log])
    bad += scan_log(rd)
    if a.other:
        od = Path(a.other) if Path(a.other).is_absolute() else ROOT / a.other
        if usable(od, "other"):
            bad += scan_secrets(od, [])
            bad += scan_log(od)
            bad += compare(rd, od)
        else:
            print("determinism: skipped (build the twin with the same --run-date and --limit to compare)")
    print(f"\nhygiene: {'OK' if not bad else str(bad) + ' problem group(s)'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
