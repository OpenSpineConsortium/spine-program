"""Compare a dedup_prescreen run on tests/fixtures/screen_run with the hand-typed expectations.

Prints one line per check, PASS or FAIL, and exits 1 when any check that the protocol requires
fails. Checks that document a known limitation rather than a protocol requirement are marked
INFO so the reviewer can quote them without the script failing on them twice.

Usage: ~/sdr_venv/bin/python tests/check_screen_counts.py --run-dir runs/review_screen
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", default="runs/review_screen")
    a = ap.parse_args()
    rd = ROOT / a.run_dir
    exp = json.loads((HERE / "expected_screen_counts.json").read_text(encoding="utf-8"))
    pc = json.loads((rd / "prisma_counts.json").read_text(encoding="utf-8"))
    merged = [json.loads(l) for l in (rd / "merged.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    sheet = list(csv.DictReader((rd / "screening_sheet.csv").open(encoding="utf-8")))
    fails = 0

    def check(name, got, want, required=True):
        nonlocal fails
        ok = got == want
        tag = "PASS" if ok else ("FAIL" if required else "INFO")
        fails += (not ok) and required
        print(f"{tag} {name}: got {json.dumps(got, sort_keys=True)} want {json.dumps(want, sort_keys=True)}")

    rows = sum(s["n_rows"] for s in pc["per_source"].values())
    check("rows read", rows, exp["identified_rows"])
    check("identified after within-source dedup", pc["identified"], exp["identified"])
    check("within-source duplicates (pubmed)", pc["per_source"]["pubmed"]["within_source_duplicates"], 1)
    check("merge counts per rule", pc["merge"], exp["merge"])
    check("flow identity holds", pc["identity_check"]["identified_minus_duplicates_equals_after_merge"], True)
    check("after_merge = protocol (identical canonical ids removed)", pc["after_merge"], exp["after_merge_protocol"])
    check("after_merge = protocol violated: identical ids kept", pc["after_merge"], exp["after_merge_if_identical_ids_not_merged"], required=False)
    dup_ids = [k for k, n in Counter(m["record_id"] for m in merged).items() if n > 1]
    check("merged.jsonl has no duplicate record_id", dup_ids, [])
    check("screening_sheet.csv has no duplicate record_id", [k for k, n in Counter(r["record_id"] for r in sheet).items() if n > 1], [])
    check("prescreen outcomes (protocol)", pc["prescreen"], exp["prescreen_protocol"])
    check("to_screen (protocol)", pc["to_screen"], exp["to_screen_protocol"])
    check("flags", pc["flags"], exp["flags"])
    check("known items matched (protocol)", sorted(pc["known_items"]["matched"]), sorted(exp["known_items_expected_by_protocol"]))
    # Rule 6 folded the derived deposit into the parent article: is the derived record still its own row?
    derived = [m for m in merged if any("zenodo.99" in (x or "") for x in [m["ids"].get("doi")] + m["member_record_ids"])]
    own_row = [m for m in merged if m["ids"].get("doi") == "10.5281/zenodo.99"]
    parent = [m for m in merged if m["ids"].get("doi") == "10.1016/j.media.2021.102166"]
    folded = bool(parent) and any("zenodo" in s for s in parent[0]["sources"]) and not own_row
    check("derived Zenodo deposit keeps its own screening row (PROTOCOL 7.6: not a duplicate of its parent)", not folded, True)
    if folded:
        print(f"      parent row {parent[0]['record_id']} now carries sources {parent[0]['sources']} and members {parent[0]['member_record_ids']}")
    # Sheet columns and ordering
    want_cols = ["record_id", "to_screen", "prescreen_outcome", "rule_fired", "source_class", "sources", "query_ids", "n_members", "merge_rules",
                 "flags", "lang_flags", "known_item", "title", "year", "type", "doi", "pmid", "pmcid", "arxiv", "url", "first_author",
                 "abstract_or_description", "member_record_ids"]
    check("sheet columns match PIPELINE.md", list(sheet[0].keys()), want_cols)
    check("sheet sorted by record_id", [r["record_id"] for r in sheet], sorted(r["record_id"] for r in sheet))
    check("merged sorted by record_id", [m["record_id"] for m in merged], sorted(m["record_id"] for m in merged))
    check("sheet rows == after_merge", len(sheet), pc["after_merge"])
    # Rule 5 partner: the crossref record must be a member of the openalex record
    xr = [m for m in merged if m["ids"].get("doi") == "10.1000/spinexr.2"]
    check("rule 5 merged crossref into openalex (n_members)", xr[0]["n_members"] if xr else None, 2)
    check("rule 5 record merge_rules", xr[0]["merge_rules"] if xr else None, ["rule_5_title_author_year"])
    ja = [m for m in merged if "jstage" in m["sources"]]
    check("jstage lang flag", ja[0]["lang_flags"] if ja else None, ["ja"])
    check("jstage outcome", ja[0]["prescreen_outcome"] if ja else None, "pass:non-english-route")
    print(f"\n{'ALL REQUIRED CHECKS PASS' if not fails else f'{fails} REQUIRED CHECK(S) FAILED'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
