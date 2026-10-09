"""Edge probes for sdr.dedup_prescreen.merge: DOI case in rule 1, year chaining in rule 5, arXiv version suffix.

Usage: ~/sdr_venv/bin/python tests/probe_merge_edges.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sdr.dedup_prescreen import merge  # noqa: E402

T = "A long enough title for rule five to consider merging records"


def r(rid, source, ids, year=2021, title=T, raw=None):
    return {"record_id": rid, "source": source, "query_id": "q", "ids": ids, "title": title, "abstract_or_description": "", "year": year, "raw": raw or {}}


# 1. Same DOI, different case (an adapter that forgot norm_doi): does rule 1 merge?
recs = sorted([r("lit:000000000001", "pubmed", {"doi": "10.1000/ABC.1"}), r("lit:000000000002", "openalex", {"doi": "10.1000/abc.1"})], key=lambda x: x["record_id"])
g, c, _ = merge(recs)
print("rule 1 DOI case-insensitive:", c["rule_1_doi"] == 1, "(unions:", c["rule_1_doi"], ")")

# 2. Rule 5 chaining: years 2019, 2020, 2021 with the same title + first author -> protocol says |diff| <= 1 pairwise
recs = [r(f"lit:00000000000{i}", "pubmed", {"url": f"https://x.org/{i}"}, year=2019 + i, raw={"authors": ["Doe J"]}) for i in range(3)]
g, c, _ = merge(recs)
print("rule 5 chains 2019-2021 into one record:", len(g) == 1, "(groups:", len(g), ", unions:", c["rule_5_title_author_year"], ")")

# 3. arXiv id with a version suffix on one side
recs = sorted([r("lit:000000000001", "s2", {"arxiv": "2105.14711"}), r("lit:000000000002", "arxiv", {"arxiv": "2105.14711v2"})], key=lambda x: x["record_id"])
g, c, _ = merge(recs)
print("rule 3 ignores version suffix:", c["rule_3_arxiv"] == 1)

# 4. Identical record_id in two sources with no DOI/PMID/arXiv (URL canonical): merged?
recs = [r("repo:aaaaaaaaaaaa", "github", {"url": "https://github.com/a/b"}), r("repo:aaaaaaaaaaaa", "pwc", {"url": "https://github.com/a/b"})]
g, c, _ = merge(recs)
print("identical record_id (URL canonical) across sources merged:", len(g) == 1)

# 5. Rule 6 target is another repository record (parent deposit DOI cited in a derived deposit's description)
recs = sorted([r("repo:000000000001", "zenodo", {"doi": "10.5281/zenodo.1"}, title="Parent"),
               {**r("repo:000000000002", "zenodo", {"doi": "10.5281/zenodo.2"}, title="Derived"), "abstract_or_description": "Derived from 10.5281/zenodo.1"}],
              key=lambda x: x["record_id"])
g, c, _ = merge(recs)
print("rule 6 folds a derived deposit into its parent deposit (repo<->repo):", len(g) == 1)
