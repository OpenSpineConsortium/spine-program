"""Reviewer helper: print query_string/params/notes of selected queries.json ids from a run dir."""
import json, sys
from pathlib import Path
q = json.loads((Path(sys.argv[1]) / "queries.json").read_text(encoding="utf-8"))
for k in sys.argv[2:]:
    v = q.get(k)
    if not v:
        print(f"--- {k}: ABSENT"); continue
    print(f"--- {k}: endpoint={v.get('endpoint')} mode={v.get('credential_mode')} hits={v.get('hit_count_api')} n={v.get('n_retrieved')} pages={v.get('n_pages')} n_requests={v.get('n_requests')}")
    print(f"    query_string={v.get('query_string')!r}")
    print(f"    params={v.get('params')} cap_hit={v.get('cap_hit')} date_filter={v.get('date_filter')}")
    print(f"    notes={json.dumps(v.get('notes'), ensure_ascii=False)[:300]}")
