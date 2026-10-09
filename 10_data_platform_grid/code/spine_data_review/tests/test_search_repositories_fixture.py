"""Hand-checkable fixture for sdr.search_repositories: a fake session serves canned pages and the
per-query and per-source numbers the module writes (n_retrieved, n_pages, hit_count_api, query_ids
merging, n_records_unique, hit_count_api_total, the --limit cap) are compared with values worked
out by hand in the comments. Prints PASS/FAIL per check; exits 1 on any FAIL.

Run: ~/sdr_venv/bin/python tests/test_search_repositories_fixture.py
Writes only under tests/_fixture_run/ (a RunDir must sit inside spine_data_review/).
"""
import json, shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sdr.common import Resp, init_run_dir
import sdr.search_repositories as sr

FAILS = []


def check(name, got, want):
    ok = got == want
    print(f"{'PASS' if ok else 'FAIL'} {name}: got={got!r} want={want!r}")
    if not ok:
        FAILS.append(name)


class FakeSession:
    """Serves canned bodies keyed by (url, sorted params); unknown keys answer 404 with an empty body."""

    def __init__(self, table):
        self.table, self.calls = table, []

    def get(self, source, qid, url, params=None, **kw):
        key = (url, json.dumps(params or {}, sort_keys=True))
        self.calls.append((source, qid, key))
        body = self.table.get(key)
        if body is None:
            return Resp(404, "", {}, "x", False, 0)
        return Resp(200, json.dumps(body), {}, "x", False, 0)


def dryad_page(items, total, has_next):
    return {"total": total, "_embedded": {"stash:datasets": items},
            "_links": ({"next": {"href": "/api/v2/search?page=2"}} if has_next else {})}


def ds(i, doi):
    return {"identifier": f"doi:{doi}", "title": f"Set {i}", "abstract": f"spine CT set {i}", "publicationDate": "2020-05-01",
            "id": i, "sharingLink": f"https://datadryad.org/stash/share/{i}", "license": "CC0", "keywords": ["spine"]}


D = "https://datadryad.org/api/v2/search"
# g01 'spine CT': page 1 -> A, B (next present), page 2 -> C (no next); total 3.
# g02 'spine radiograph': page 1 -> B again (same DOI) ; total 1.
# Hand calculation: dryad_g01 n_retrieved 3, n_pages 2, hits 3; dryad_g02 n_retrieved 1, n_pages 1, hits 1;
# unique records 3 (B merges), hit_count_api_total 4, record B has query_ids [dryad_g01, dryad_g02].
TABLE = {
    (D, json.dumps({"page": 1, "per_page": 100, "q": "spine CT"}, sort_keys=True)): dryad_page([ds(1, "10.5061/dryad.a1"), ds(2, "10.5061/dryad.b2")], 3, True),
    (D, json.dumps({"page": 2, "per_page": 100, "q": "spine CT"}, sort_keys=True)): dryad_page([ds(3, "10.5061/dryad.c3")], 3, False),
    (D, json.dumps({"page": 1, "per_page": 100, "q": "spine radiograph"}, sort_keys=True)): dryad_page([ds(2, "10.5061/dryad.b2")], 1, False),
}
K = "https://www.kaggle.com/api/v1/datasets/list"
# Kaggle: one page of 3 datasets answered anonymously (status 200), fewer than 20 so no second page.
# The API reports NO total. Hand calculation: n_retrieved 3, hit_count_api must be None (unknown), not 3.
TABLE[(K, json.dumps({"page": 1, "search": "spine CT"}, sort_keys=True))] = [
    {"ref": f"u/s{i}", "title": f"S{i}", "subtitle": "spine CT", "url": f"https://www.kaggle.com/datasets/u/s{i}", "lastUpdated": "2021-01-01"} for i in range(3)]

Q = {"g01": {"string": "spine CT"}, "g02": {"string": "spine radiograph"}}


def run_dir():
    p = ROOT / "tests" / "_fixture_run"
    shutil.rmtree(p, ignore_errors=True)
    return init_run_dir(p, "2026-09-19", ["fixture"])


# --- 1. dryad, no limit
rd = run_dir()
run = sr.Run(rd, FakeSession(TABLE), "2026-09-19", None, False)
sr.src_dryad(run, Q)
run.flush()
q = json.loads(rd.queries_json.read_text())
c = json.loads((rd.root / "counts.json").read_text())
check("dryad_g01 n_retrieved", q["dryad_g01"]["n_retrieved"], 3)
check("dryad_g01 n_pages", q["dryad_g01"]["n_pages"], 2)
check("dryad_g01 hit_count_api", q["dryad_g01"]["hit_count_api"], 3)
check("dryad_g02 n_retrieved", q["dryad_g02"]["n_retrieved"], 1)
check("dryad n_records_unique", c["dryad"]["n_records_unique"], 3)
check("dryad hit_count_api_total", c["dryad"]["hit_count_api_total"], 4)
recs = [json.loads(l) for l in (rd.records / "dryad.jsonl").read_text().splitlines()]
b = [r for r in recs if r["ids"]["doi"] == "10.5061/dryad.b2"][0]
check("record B query_ids merged", b["query_ids"], ["dryad_g01", "dryad_g02"])
check("record B first query_id", b["query_id"], "dryad_g01")
check("record ids sorted in file", [r["record_id"] for r in recs], sorted(r["record_id"] for r in recs))
check("record_id prefix repo:", all(r["record_id"].startswith("repo:") for r in recs), True)
check("dryad_g01 n_requests recorded (protocol 6.3)", q["dryad_g01"]["n_requests"], 2)

# --- 2. dryad, --limit 1: one item per query, one page
rd = run_dir()
run = sr.Run(rd, FakeSession(TABLE), "2026-09-19", 1, False)
sr.src_dryad(run, Q)
run.flush()
q = json.loads(rd.queries_json.read_text())
check("limit=1 dryad_g01 n_retrieved", q["dryad_g01"]["n_retrieved"], 1)
check("limit=1 dryad_g01 n_pages", q["dryad_g01"]["n_pages"], 1)
check("limit=1 hit_count_api still the API total", q["dryad_g01"]["hit_count_api"], 3)

# --- 3. kaggle anonymous: hit count unknown must not be reported as the retrieved count
rd = run_dir()
run = sr.Run(rd, FakeSession(TABLE), "2026-09-19", None, False)
sr.src_kaggle(run, {"g01": {"string": "spine CT"}})
run.flush()
q = json.loads(rd.queries_json.read_text())
c = json.loads((rd.root / "counts.json").read_text())
check("kaggle_g01 n_retrieved", q["kaggle_g01"]["n_retrieved"], 3)
check("kaggle_g01 hit_count_api is None (API reports no total)", q["kaggle_g01"]["hit_count_api"], None)
check("kaggle hit_count_api_total excludes unknown totals", c["kaggle"]["hit_count_api_total"], 0)

# --- 4. helpers
clauses = sr._top_clauses("((a OR b) AND (c OR d) AND e:(f OR g) AND h:[1 TO 2])")
check("_top_clauses splits four depth-0 clauses", clauses, ["(a OR b)", "(c OR d)", "e:(f OR g)", "h:[1 TO 2]"])
check("_split moves the query string into params", sr._split("https://x.org/a?b=1&c=d%20e"), ("https://x.org/a", {"b": "1", "c": "d e"}))
check("_year", sr._year("published 2019-03-02"), 2019)

shutil.rmtree(ROOT / "tests" / "_fixture_run", ignore_errors=True)
print("\nFAILED:", FAILS if FAILS else "none")
sys.exit(1 if FAILS else 0)
