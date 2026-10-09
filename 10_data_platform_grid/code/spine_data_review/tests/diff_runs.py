"""Reviewer check: are two run directories identical apart from timestamps?
Compares records/*.jsonl (dropping retrieved_at), queries.json (dropping first/last_request_ts)
and counts.json. Prints per-file verdicts and the first differing keys. Exit 1 on any difference.
Usage: ~/sdr_venv/bin/python tests/diff_runs.py runs/A runs/B"""
import json, sys
from pathlib import Path
A, B = Path(sys.argv[1]), Path(sys.argv[2])
TS = {"retrieved_at", "first_request_ts", "last_request_ts"}


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in TS}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


diff = 0
for name in ("queries.json", "counts.json"):
    a, b = strip(json.loads((A / name).read_text(encoding="utf-8"))), strip(json.loads((B / name).read_text(encoding="utf-8")))
    if a == b:
        print(f"SAME  {name}")
    else:
        diff += 1
        keys = [k for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
        print(f"DIFF  {name}: {len(keys)} keys differ, e.g. {keys[:8]}")
        for k in keys[:3]:
            av, bv = a.get(k, {}), b.get(k, {})
            sub = [s for s in sorted(set(av) | set(bv)) if av.get(s) != bv.get(s)] if isinstance(av, dict) and isinstance(bv, dict) else ["<whole>"]
            print(f"        {k}: {sub[:6]}")
files = sorted({p.name for p in (A / "records").glob("*.jsonl")} | {p.name for p in (B / "records").glob("*.jsonl")})
for f in files:
    ra = [strip(json.loads(l)) for l in (A / "records" / f).read_text(encoding="utf-8").splitlines() if l.strip()] if (A / "records" / f).exists() else None
    rb = [strip(json.loads(l)) for l in (B / "records" / f).read_text(encoding="utf-8").splitlines() if l.strip()] if (B / "records" / f).exists() else None
    if ra == rb:
        print(f"SAME  records/{f} ({len(ra)})")
    else:
        diff += 1
        ia, ib = {r["record_id"] for r in ra or []}, {r["record_id"] for r in rb or []}
        changed = [r["record_id"] for r in ra or [] if r["record_id"] in ib and r != next(x for x in rb if x["record_id"] == r["record_id"])]
        print(f"DIFF  records/{f}: A={len(ra or [])} B={len(rb or [])} onlyA={len(ia - ib)} onlyB={len(ib - ia)} changed={len(changed)} {changed[:3]}")
print("result:", "identical (modulo timestamps)" if not diff else f"{diff} file(s) differ")
sys.exit(1 if diff else 0)
