#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids_impact.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""How many names each raw-id SPINEPS tree would hand a reader that takes an id for a level -- from the census rows.

Reads the F2 census rows (tools/spineps_id_census.py; one row per mask: ids, voxels, world centroids, and for each
VERIDAH ctd point the id the mask holds there) and counts, per tree, what an id-as-name reader gets wrong:
  * masks / distinct files, and how many are raw (ids exactly 1..N contradicted by the ctd) or scrambled;
  * instances that would be read as a level (ids 1..28, >= 50 voxels), and of the ctd points that land inside an
    instance, how many land in an instance carrying ANOTHER id (a wrong name at a vertebra VERIDAH named);
  * "id 25 present" / "id 28 present" masks against the ctd's own L6 / T13 calls (false and missed calls);
  * the sacrum class: masks with an id 26 at all, and whether the ctd sacrum point lies in it (a raw mask has
    no sacrum instance; 26 is simply the 26th instance when there are 26 or more).

    python tools/spineps_ids_impact.py --rows SchwingNet/results/spineps_ids/census_rows.jsonl.gz \
        --out SchwingNet/results/spineps_ids/impact_counts.json
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
from collections import Counter, defaultdict

TREES = [
    ("bench (CTSP benchmark, COLONOG)", "/bench/spineps/native/"),
    ("bench_ts TS v2", "/bench_ts/spineps/native/TS_"),
    ("bench_ts VerSe", "/bench_ts/spineps/native/VERSE_"),
    ("tsv3", "/data/spineps/tsv3/"),
    ("cobra v1 (Elekta)", "/data/cobra2026/seg/spineps/"),
    ("spineps_v1_relabel plain", "/crossdev/levels/spineps_v1_relabel/"),
    ("deepfluoro", "/realxray_work/deepfluoro/spineps/"),
    ("geneva_hip", "/realxray_work/geneva_hip/spineps/"),
    ("bodies TS v2", "/data/spineps/bodies/TS_"),
    ("bodies TSV3", "/data/spineps/bodies/TSV3_"),
    ("bodies VerSe", "/data/spineps/bodies/VERSE_"),
    ("bodies CTSP", "/data/spineps/bodies/CTSP_"),
    ("bodies_cobra Elekta", "/data/spineps/bodies_cobra/"),
    ("ctsp (post-fix)", "/data/spineps/ctsp/"),
    ("cobra lstv/seg (post-fix)", "/data/cobra2026/lstv/seg/"),
    ("cobra_varian (post-fix)", "/data/spineps/cobra_varian/"),
    ("carmlspine (post-fix)", "/data/carmlspine/spineps/"),
    ("spineps_v2 (post-fix)", "/data/cobra2026/seg/spineps_v2/"),
]
BAD = ("scrambled", "ordered_but_not_names", "scrambled_no_ctd")


def tree_of(p: str) -> str | None:
    for name, key in TREES:
        if key in p:
            if name == "bodies_cobra Elekta" and os.path.basename(p)[:1] in ("F", "G"):
                return "bodies_cobra Varian"
            if name == "spineps_v1_relabel plain" and "veridah" in os.path.basename(p):
                return "spineps_v1_relabel _veridah"
            if name in ("carmlspine (post-fix)",) and "veridah" in os.path.basename(p):
                return "carmlspine _veridah"
            return name
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    op = gzip.open if a.rows.endswith(".gz") else open
    rows = [json.loads(l) for l in op(a.rows, "rt") if l.strip()]
    per = defaultdict(list)
    for r in rows:
        if r.get("kind") not in ("seg-vert", "seg-vert-veridah", "body"):
            continue
        t = tree_of(r["path"])
        if t:
            per[t].append(r)
    out = {}
    for t, rs in per.items():
        c = Counter()
        l6 = Counter()
        wrong_examples = []
        for r in rs:
            c["masks"] += 1
            c["links"] += int(bool(r.get("is_link")))
            v = r.get("verdict")
            raw = bool(r.get("raw_instance"))
            bad = v in BAD or raw
            c["raw_instance"] += int(raw)
            c["ids_not_names"] += int(bad)
            ids = [int(i) for i in r.get("ids") or []]
            nv = {int(k): n for k, n in (r.get("n_vox") or {}).items()}
            named = [i for i in ids if 1 <= i <= 28 and nv.get(i, 0) >= 50]
            ctd = set(int(x) for x in (r.get("ctd_labels") or []))
            agree = r.get("ctd_agree") or 0
            dis = r.get("ctd_disagree_named", r.get("ctd_disagree")) or 0
            if bad:
                c["named_instances_in_bad_masks"] += len(named)
                c["ctd_points_tested_bad"] += agree + dis
                c["ctd_points_wrong_bad"] += dis
                c["bad_masks_with_every_tested_point_wrong"] += int(agree == 0 and dis > 0)
                c["bad_masks_id26_present"] += int(26 in ids)
                c["bad_masks_no_id26"] += int(26 not in ids)
                c["bad_masks_ctd_names_sacrum"] += int(26 in ctd)
                if len(wrong_examples) < 3 and dis:
                    wrong_examples.append(dict(case=r.get("case"), ids_top_to_bottom=r.get("order_top_to_bottom", [])[:8],
                                               ctd_top_to_bottom=(r.get("ctd_order_top_to_bottom") or [])[:8],
                                               agree=agree, disagree=dis))
            else:
                c["named_instances_ok_masks"] += len(named)
                c["ctd_points_tested_ok"] += agree + dis
                c["ctd_points_wrong_ok"] += dis
            # L6 / T13 by id presence against the ctd's own call
            id_l6, id_t13 = 25 in ids, 28 in ids
            ctd_l6, ctd_t13 = 25 in ctd, 28 in ctd
            l6["id25_present"] += int(id_l6)
            l6["id25_and_ctd_L6"] += int(id_l6 and ctd_l6)
            l6["id25_but_ctd_no_L6"] += int(id_l6 and not ctd_l6)
            l6["ctd_L6_but_no_id25"] += int(ctd_l6 and not id_l6)
            l6["ctd_L6"] += int(ctd_l6)
            l6["id28_present"] += int(id_t13)
            l6["id28_and_ctd_T13"] += int(id_t13 and ctd_t13)
            l6["id28_but_ctd_no_T13"] += int(id_t13 and not ctd_t13)
            l6["ctd_T13_but_no_id28"] += int(ctd_t13 and not id_t13)
            l6["ctd_T13"] += int(ctd_t13)
        d = dict(c)
        if c["ctd_points_tested_bad"]:
            d["wrong_name_rate_bad"] = round(c["ctd_points_wrong_bad"] / c["ctd_points_tested_bad"], 3)
        if c["ctd_points_tested_ok"]:
            d["wrong_name_rate_ok"] = round(c["ctd_points_wrong_ok"] / c["ctd_points_tested_ok"], 4)
        d["l6_t13_by_id_vs_ctd"] = dict(l6)
        d["examples"] = wrong_examples
        out[t] = d
    json.dump(out, open(a.out, "w"), indent=1)
    keys = ("masks", "ids_not_names", "raw_instance", "named_instances_in_bad_masks", "ctd_points_tested_bad",
            "ctd_points_wrong_bad", "wrong_name_rate_bad", "bad_masks_id26_present", "wrong_name_rate_ok")
    print("tree".ljust(34) + " ".join(k[:14].rjust(14) for k in keys))
    for t in sorted(out, key=lambda x: -out[x]["masks"]):
        print(t.ljust(34) + " ".join(str(out[t].get(k, "")).rjust(14) for k in keys))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
