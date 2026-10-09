"""Diff two complete run directories (search through recipe) ignoring the timestamp fields.

Companion to tests/diff_runs.py (which covers records, queries and counts): this one also covers
merged.jsonl, screening_sheet.csv, prisma_counts.json, analysis/*.json, tables/*.tex|csv,
manuscript/main.tex, recipe/**, charting_probes/*.json and probes/summary.json, and compares the
request log as the ordered sequence of (source, query_id, url, params, status). Volatile keys
(ts, retrieved_at, first/last_request_ts, created_at, elapsed_ms, invocations, probe dates, bytes)
are dropped, ISO timestamps inside strings are masked, and the NCBI history tokens (WebEnv,
query_key) keep their key with a masked value: they are minted per session, so comparing them
would report every pair of runs as different on the first efetch and hide everything after it.

A live-vs-live diff moves with the sources as well as with this code (a repository indexes a new
record, a server returns a 502 that a retry then answers). The supported determinism test is a
live run against its own --replay over the same cache, which is byte-identical.
Exit 1 on any difference.
Usage: ~/sdr_venv/bin/python tests/diff_run_dirs.py runs/A runs/B
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOLATILE = {"ts", "retrieved_at", "first_request_ts", "last_request_ts", "created_at", "elapsed_ms", "invocations",
            "probed_at", "date", "dates", "bytes"}
# Masked, not dropped: a run that stopped sending a history token is a real difference; its value is not.
MASKED = {"WebEnv", "query_key"}
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


def scrub(obj):
    if isinstance(obj, dict):
        return {k: ("<masked>" if k in MASKED else scrub(v)) for k, v in obj.items() if k not in VOLATILE}
    if isinstance(obj, list):
        return [scrub(v) for v in obj]
    if isinstance(obj, str):
        return DATE_RE.sub("<ts>", obj)
    return obj


def load(p: Path):
    if p.suffix == ".jsonl":
        return [scrub(json.loads(l)) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    if p.suffix == ".json":
        return scrub(json.loads(p.read_text(encoding="utf-8")))
    return DATE_RE.sub("<ts>", p.read_text(encoding="utf-8", errors="ignore"))


def main(a: str, b: str) -> int:
    A, B = (ROOT / a).resolve(), (ROOT / b).resolve()
    pats = ["records/*.jsonl", "merged.jsonl", "screening_sheet.csv", "prisma_counts.json", "queries.json", "counts.json",
            "analysis/*.json", "tables/*.tex", "tables/*.csv", "manuscript/main.tex", "recipe/**/*", "charting_probes/*.json",
            "probes/summary.json"]
    files = sorted({p.relative_to(A) for pat in pats for p in A.glob(pat) if p.is_file()} |
                   {p.relative_to(B) for pat in pats for p in B.glob(pat) if p.is_file()})
    n_bad = 0
    for rel in files:
        pa, pb = A / rel, B / rel
        if not pa.exists() or not pb.exists():
            print(f"DIFF only in {'A' if pa.exists() else 'B'}: {rel}")
            n_bad += 1
            continue
        va, vb = load(pa), load(pb)
        if va != vb:
            n_bad += 1
            detail = ""
            if isinstance(va, dict) and isinstance(vb, dict):
                detail = " keys: " + ", ".join(k for k in sorted(set(va) | set(vb)) if va.get(k) != vb.get(k))[:200]
            elif isinstance(va, list) and isinstance(vb, list):
                detail = f" rows {len(va)} vs {len(vb)}"
            print(f"DIFF {rel}{detail}")
    la = [(r["source"], r["query_id"], r["url"], json.dumps(r["params"], sort_keys=True), r["status"]) for r in load(A / "requests.log.jsonl")]
    lb = [(r["source"], r["query_id"], r["url"], json.dumps(r["params"], sort_keys=True), r["status"]) for r in load(B / "requests.log.jsonl")]
    if la != lb:
        i = next((i for i, (x, y) in enumerate(zip(la, lb)) if x != y), min(len(la), len(lb)))
        print(f"DIFF requests.log.jsonl sequence: {len(la)} vs {len(lb)} attempts; first divergence at line {i}: "
              f"{la[i] if i < len(la) else None} vs {lb[i] if i < len(lb) else None}")
        n_bad += 1
    print(f"compared {len(files)} files + request sequence: {'identical' if n_bad == 0 else f'{n_bad} differ'}")
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
