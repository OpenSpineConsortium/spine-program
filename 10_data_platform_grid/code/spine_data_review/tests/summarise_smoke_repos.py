"""Reviewer helper: per-source summary of what a run's queries.json and counts.json recorded.
Usage: ~/sdr_venv/bin/python tests/summarise_smoke_repos.py runs/<dir>"""
import json, sys
from pathlib import Path
rd = Path(sys.argv[1])
q = json.loads((rd / "queries.json").read_text(encoding="utf-8")) if (rd / "queries.json").exists() else {}
c = json.loads((rd / "counts.json").read_text(encoding="utf-8")) if (rd / "counts.json").exists() else {}
repo = ["zenodo", "figshare", "dryad", "osf", "mendeley", "datacite", "physionet", "tcia", "kaggle", "hf", "gc", "github",
        "pwc", "odl", "openi", "commons", "jstage", "koreamed", "scielo", "redalyc", "kaggle-mention", "hf-mention"]
for s in repo:
    qs = {k: v for k, v in q.items() if v.get("source") == s}
    modes = sorted(set(str(v.get("credential_mode")) for v in qs.values()))
    hits = [(k, v.get("hit_count_api"), v.get("n_retrieved"), v.get("n_pages"), v.get("cap_hit")) for k, v in sorted(qs.items())]
    print(f"{s:16s} nq={len(qs):3d} modes={modes} n_records_unique={c.get(s, {}).get('n_records_unique')} total_hits={c.get(s, {}).get('hit_count_api_total')}")
    for h in hits[:6]:
        print("     ", h)
    if len(hits) > 6:
        print("      ...", len(hits) - 6, "more")
