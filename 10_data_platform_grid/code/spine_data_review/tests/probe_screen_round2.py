"""Round-2 adversarial probes for sdr.dedup_prescreen.merge / build_merged and sdr.chart.licence_lookup.

Not part of the smoke script: these are the edges the fixes could have opened. Usage:
    ~/sdr_venv/bin/python tests/probe_screen_round2.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sdr.dedup_prescreen import merge, build_merged, known_item_rule  # noqa: E402
from sdr.chart import licence_lookup, load_licence_tiers  # noqa: E402
from sdr.common import review_root  # noqa: E402

T = "A long enough title for rule five to consider merging these two records"
out = []


def rec(rid, source, ids, year=2021, title=T, abstract="", raw=None):
    return {"record_id": rid, "source": source, "query_id": "q", "ids": ids, "title": title,
            "abstract_or_description": abstract, "year": year, "raw": raw or {}}


def run(recs):
    recs = sorted(recs, key=lambda x: (x["record_id"], x["source"]))
    g, c, log = merge(recs)
    rows = [build_merged(recs, grp, [l["rule"] for l in log]) for grp in g]
    return g, c, rows


def info(name, value, why=""):
    print(f"INFO {name} = {value}" + ((" :: " + why) if why else ""))


def say(name, ok, detail=""):
    out.append((name, ok, detail))
    print(("PASS " if ok else "FAIL ") + name + ((" :: " + detail) if detail else ""))


# --- A. rule 0 must not double-count when the pair is ALSO an identifier duplicate
recs = [rec("lit:000000000001", "pubmed", {"doi": "10.1000/a"}), rec("lit:000000000001", "openalex", {"doi": "10.1000/a"})]
g, c, rows = run(recs)
say("A same record_id AND same DOI counts one union, one row",
    len(g) == 1 and c["rule_0_identical_canonical"] + c["rule_1_doi"] == 1, json.dumps(c))

# --- B. three copies of one canonical (github, pwc, hf-mention) collapse to one row, n_members=1
recs = [rec(f"repo:aaaaaaaaaaaa", s, {"url": "https://github.com/a/b"}) for s in ("github", "pwc", "hf")]
g, c, rows = run(recs)
say("B three files, one canonical -> 1 row, 2 unions, n_members 1",
    len(g) == 1 and c["rule_0_identical_canonical"] == 2 and rows[0]["n_members"] == 1 and rows[0]["sources"] == ["github", "hf", "pwc"],
    f"n_members={rows[0]['n_members']} sources={rows[0]['sources']}")

# --- C. rule 6: a repo record duplicated across two files AND linking an article -> one row
art = rec("lit:000000000001", "pubmed", {"doi": "10.1000/spine.1"})
dep = lambda s: rec("repo:000000000002", s, {"doi": "10.5281/zenodo.1", "repo_id": "1"}, abstract="Supplement to 10.1000/spine.1",
                    raw={"metadata": {"related_identifiers": [{"identifier": "10.1000/spine.1", "relation": "isSupplementTo"}]}})
g, c, rows = run([art, dep("zenodo"), dep("datacite")])
say("C duplicate deposit + article -> one row", len(g) == 1 and len(rows) == 1, json.dumps(c))

# --- D. rule 6 must not fire repo->repo even when the parent deposit also has a lit twin with the SAME DOI
parent_repo = rec("repo:000000000001", "zenodo", {"doi": "10.5281/zenodo.1"}, title="Parent deposit")
child = rec("repo:000000000002", "zenodo", {"doi": "10.5281/zenodo.2"}, title="Child deposit",
            abstract="Supplement to 10.5281/zenodo.1")
g, c, rows = run([parent_repo, child])
say("D repo->repo never merges", len(g) == 2, f"groups={len(g)}")

# --- E. derived-context skip is case-insensitive and catches 'Derived from'
child = rec("repo:000000000002", "zenodo", {"doi": "10.5281/zenodo.2"},
            abstract="Derived From the parent article 10.1000/spine.1 with L6 cases.")
g, c, rows = run([art, child])
say("E 'Derived From' (mixed case) skips the link", len(g) == 2 and c["rule_6_skipped_derived_context"] == 1, json.dumps(c))

# --- F. related_dois keeps the skipped parent DOI for the 7.6 mapping
d = next(r for r in rows if r["record_id"] == "repo:000000000002")
say("F derived row keeps related_dois", d["related_dois"] == ["10.1000/spine.1"], json.dumps(d["related_dois"]))

# --- G. docstring claim: 'related' is every DOI seen, linkable or not -- reference-list branch
many = rec("repo:000000000003", "zenodo", {"doi": "10.5281/zenodo.3"},
           abstract="See 10.1000/a, 10.1000/b and 10.1000/c for context.")
g, c, rows = run([many])
say("G >2 in-text DOIs: skipped_many counted", c["rule_6_skipped_many_dois"] == 1, json.dumps(c))
info("G2 related_dois after the reference-list skip", rows[0]["related_dois"],
     "docstring says `related` is every DOI seen; the >2 branch returns before the in-text DOIs are added")

# --- H. concept key from conceptrecid vs conceptdoi on the two versions of one deposit
v1 = rec("repo:000000000001", "zenodo", {"doi": "10.5281/zenodo.11"}, raw={"conceptdoi": "10.5281/zenodo.10"})
v2 = rec("repo:000000000002", "zenodo", {"doi": "10.5281/zenodo.12"}, raw={"conceptrecid": "10"})
vr = rec("repo:000000000003", "zenodo", {"doi": "10.5281/zenodo.13"}, raw={"conceptrecid": "10"})
g3, _, _ = run([v1, vr])
info("H conceptdoi vs conceptrecid", len(g3),
     "_concept_key builds concept:10.5281/zenodo.10 from conceptdoi and concept:10 from conceptrecid, "
     "so the two keys never meet; inert today because src_zenodo only ever writes conceptdoi")

# --- I. known item on the concept DOI when the representative carries only a version DOI
v2b = rec("repo:000000000002", "zenodo", {"doi": "10.5281/zenodo.12"}, raw={"conceptdoi": "10.5281/zenodo.10"})
g, c, rows = run([v1, v2b])
m = rows[0]
item = {"item": "x", "match_rule": "doi", "doi": "10.5281/zenodo.10"}
say("I known item matched through concept_doi", known_item_rule(m, item) == "doi",
    f"concept_doi={m.get('concept_doi')} member_dois={m.get('member_dois')}")

# --- J. known item on a MEMBER version DOI that is not the representative's
item2 = {"item": "y", "match_rule": "doi", "doi": "10.5281/zenodo.12"}
say("J known item matched through a member DOI", known_item_rule(m, item2) == "doi",
    f"rep_doi={m['ids']['doi']}")

# --- K. rule 5 pairwise window: 2020 and 2021 still merge, 2019+2021 do not
recs = [rec(f"lit:00000000000{i}", "pubmed", {"url": f"https://x/{i}"}, year=y, raw={"authors": ["Doe J"]})
        for i, y in enumerate((2020, 2021))]
g, c, _ = run(recs)
say("K rule 5 still merges a 1-year gap", len(g) == 1, f"groups={len(g)}")

# --- L2. empty record_id: rule 0 keys on it directly
g0, c0, _ = run([rec("", "github", {"url": "https://github.com/a/b"}, title="Alpha spine dataset"),
                 rec("", "figshare", {"url": "https://figshare.com/x"}, title="Beta spine dataset")])
info("L2 two records with an empty record_id", len(g0),
     "rule 0 keys on r['record_id'] with no truthiness guard, so unrelated records fold into one row and the "
     "duplicate-id assertion cannot see it; ids.canonical_string raises rather than returning '', so inert today")

# --- L. licence: CC BY 3.0 text against a CC-BY-4.0 row, and the CC-BY-SA family
tiers = load_licence_tiers(review_root() / "licence_tiers.csv")
for text, want in [("CC BY 3.0", "CC-BY-3.0"), ("CC BY 4.0", "CC-BY-4.0"), ("CC BY-SA 3.0", "CC-BY-SA-3.0"),
                   ("CC BY-NC 4.0", "CC-BY-NC-4.0"), ("CC BY 2.0", "CC-BY-2.0"), ("CC0 1.0", "CC0-1.0"),
                   ("TCIA Data Usage Policy; CC BY 3.0", "CC-BY-3.0"),
                   ("Creative Commons Attribution 4.0 International (CC BY 4.0)", "CC-BY-4.0"),
                   ("Creative Commons Attribution 3.0 Unported", "CC-BY-3.0")]:
    got = (licence_lookup(text, tiers) or {}).get("spdx")
    say(f"L licence {text!r} -> {want}", got == want, f"got {got}")

print("\n" + json.dumps({"n": len(out), "failed": [n for n, ok, _ in out if not ok]}, indent=2))
sys.exit(0 if all(ok for _, ok, _ in out) else 1)
