"""Live three-request probe of sdr.common.RateLimitedSession with the REAL credential store (review of
module 'common'). The shared layer has no --limit search of its own, so this is its `--limit 3` run:
one keyed NCBI esearch (retmax=0), one OpenAlex work by DOI with mailto, one Springer Meta query by
DOI (the one service whose JSON answer echoes the api key back), all into --run-dir. It then verifies
that every request was logged and cached, that a replay session serves all three offline, and that no
credential value appears in requests.log.jsonl, run_meta.json or any raw/ file. It prints credential
NAMES and booleans only; the one raw file that is found to hold a value is deleted and named.

Usage (WSL): ~/sdr_venv/bin/python tests/live_common_probe.py --run-dir runs/review_common --run-date 2026-09-19
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sdr import common, creds  # noqa: E402

DOI = creds.PROBE_DOI


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--run-date", required=True)
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    rd = common.init_run_dir(a.run_dir, a.run_date, ["live_common_probe", "--limit", str(a.limit)])
    specs = [
        ("pubmed", "review_ncbi", "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
         {"db": "pubmed", "term": "spine[tiab] AND dataset[tiab]", "retmax": 0, "retmode": "json", "api_key": creds.cred("NCBI_API_KEY")},
         "NCBI_API_KEY"),
        ("openalex", "review_openalex", f"https://api.openalex.org/works/https://doi.org/{DOI}", {"mailto": creds.contact()}, "FLUOROCAP_CONTACT_EMAIL"),
        ("springer", "review_springer", "https://api.springernature.com/meta/v2/json", {"q": f"doi:{DOI}", "p": 1, "api_key": creds.cred("SPRINGER_API_META_KEY")},
         "SPRINGER_API_META_KEY"),
    ][: a.limit]
    if a.dry_run:
        for s, q, u, p, c in specs:
            print("would request", s, q, u, common.strip_params(p), "credential", c)
        return 0
    sess = common.RateLimitedSession(rd)
    shas = []
    for s, q, u, p, c in specs:
        r = sess.get(s, q, u, p, credential=c, keyed=True)
        shas.append((s, r.sha1, r.status, r.from_cache))
        print(f"  {s:9s} {q:16s} status {r.status} from_cache={r.from_cache} sha1={r.sha1[:12]}")
    rows = [x for x in common.read_jsonl(rd.requests_log) if x["query_id"].startswith("review_")]
    print("logged rows for the three queries:", len(rows), "; cached files present:",
          [(s, (rd.raw / s / f"{sha}.json").exists()) for s, sha, _, _ in shas])
    rp = common.RateLimitedSession(rd, replay=True)
    replay_ok = all(rp.get(s, q, u, p, credential=c, keyed=True).from_cache for s, q, u, p, c in specs)
    print("replay serves all three offline:", replay_ok)
    vals = {k: v for k, v in creds._load().items() if len(v) >= 6}
    leaks = []
    for f in [rd.requests_log, rd.meta, *rd.raw.rglob("*.json")]:
        if f.exists():
            t = f.read_text(encoding="utf-8", errors="replace")
            for k, v in vals.items():
                if v in t:
                    leaks.append((str(f.relative_to(rd.root)), k))
    print("files holding a credential VALUE (path, credential name):", leaks)
    for rel, _ in leaks:
        if rel.startswith("raw/"):
            (rd.root / rel).unlink()
            print("  deleted", rel)
    return 1 if leaks else 0


if __name__ == "__main__":
    sys.exit(main())
