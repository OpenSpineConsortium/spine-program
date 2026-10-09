"""Reviewer check on a run dir: every logged non-cached, non-error, non-retry-status attempt for
the repository sources has a raw/<source>/<sha1>.json cache file; every records/<source>.jsonl row has
the required fields; per-source request counts. Prints a table and any gaps. Exit 1 on a gap.
Usage: ~/sdr_venv/bin/python tests/check_log_cache.py runs/<dir>"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
rd = Path(sys.argv[1])
rows = [json.loads(l) for l in (rd / "requests.log.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
REQ = {"ts", "source", "query_id", "attempt", "method", "url", "params", "status", "elapsed_ms", "bytes", "cache_sha1", "from_cache", "credential", "error"}
bad_fields = [r for r in rows if set(r) != REQ]
print("log lines:", len(rows), "| lines with a field set != protocol 15:", len(bad_fields), (sorted(set(bad_fields[0]) ^ REQ) if bad_fields else ""))
per = defaultdict(Counter)
gaps = []
for r in rows:
    per[r["source"]]["attempts"] += 1
    per[r["source"]]["from_cache"] += bool(r["from_cache"])
    per[r["source"]]["errors"] += r["error"] is not None
    per[r["source"]][f"s{r['status']}"] += 1
    if not r["from_cache"] and r["error"] is None and r["status"] not in (429, 500, 502, 503, 504) and r["status"] != 0:
        if r["cache_sha1"] is None or not (rd / "raw" / r["source"] / f"{r['cache_sha1']}.json").exists():
            gaps.append((r["source"], r["query_id"], r["status"], r["cache_sha1"]))
print("credential names in log:", sorted({r["credential"] for r in rows}))
print("non-redacted secret-looking params:", [r for r in rows if any(k.lower() in ("api_key", "token", "key", "mailto", "email") and v != "<redacted>" for k, v in (r["params"] or {}).items())][:3])
for s in sorted(per):
    c = per[s]
    print(f"  {s:16s} attempts={c['attempts']:4d} cached={c['from_cache']:3d} errors={c['errors']:3d} " + " ".join(f"{k}={v}" for k, v in sorted(c.items()) if k.startswith("s")))
print("uncached successful attempts:", len(gaps), gaps[:10])
n_raw = sum(1 for p in (rd / "raw").rglob("*.json"))
print("raw files:", n_raw)
RREQ = {"record_id", "canonical", "source", "query_id", "query_ids", "retrieved_at", "ids", "title", "abstract_or_description", "year", "type", "raw"}
for f in sorted((rd / "records").glob("*.jsonl")):
    recs = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]
    ids = [r["record_id"] for r in recs]
    problems = [r["record_id"] for r in recs if set(r) != RREQ or r["source"] != f.stem]
    print(f"  records/{f.name:22s} n={len(recs):3d} sorted={ids == sorted(ids)} unique={len(ids) == len(set(ids))} field_problems={len(problems)}")
sys.exit(1 if gaps or bad_fields else 0)
