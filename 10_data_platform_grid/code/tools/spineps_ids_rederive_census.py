# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids_rederive_census.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Re-derive two IMPACT 'contaminated' counts straight from the F2 census rows (not from impact_counts.json).
C4: ~/bench/spineps/native -- 800 masks, all raw, no id >= 17 anywhere, so the VerSe-id reader scored 0 on every class.
C1: bench_ts TS_* masks carrying id 25 -- 12 (s1089 ... ), ids exactly {1..25}, ctd agreement at chance.
C6: body masks whose source is raw, by tree."""
import gzip
import json
import sys
from collections import Counter

rows = [json.loads(l) for l in gzip.open(sys.argv[1], "rt")]
out = {}

# ---- C4
b = [r for r in rows if "/bench/spineps/native/" in r["path"] and r.get("kind") == "seg-vert"]
ids = [set(int(x) for x in (r.get("ids") or [])) for r in b]
out["C4"] = dict(
    masks=len(b),
    raw_instance=sum(1 for r in b if r.get("raw_instance")),
    contiguous_from_1=sum(1 for r in b if r.get("contiguous_from_1")),
    harvest_chosen_raw=sum(1 for r in b if (r.get("harvest") or {}).get("chosen_is_raw")),
    max_id_over_all=max((max(s) for s in ids if s), default=None),
    masks_with_any_id_ge_17=sum(1 for s in ids if any(i >= 17 for i in s)),
    n_instances_range=[min(len(s) for s in ids), max(len(s) for s in ids)],
    ctd_points_wrong=sum(r.get("ctd_disagree") or 0 for r in b),
    ctd_points_tested=sum((r.get("ctd_agree") or 0) + (r.get("ctd_disagree") or 0) for r in b),
    ctd_names_sacrum=sum(1 for r in b if 26 in (r.get("ctd_labels") or [])),
    id26_present=sum(1 for s in ids if 26 in s),
    verdicts=dict(Counter(r.get("verdict") for r in b)),
)

# ---- C1
t = [r for r in rows if "/bench_ts/spineps/native/TS_" in r["path"] and r.get("kind") == "seg-vert"]
t25 = [r for r in t if 25 in (r.get("ids") or [])]
out["C1"] = dict(
    ts_masks=len(t),
    with_id25=len(t25),
    cases=sorted(r["case"] for r in t25),
    ids_exactly_1_to_25=sum(1 for r in t25 if sorted(r["ids"]) == list(range(1, 26))),
    raw_instance=sum(1 for r in t25 if r.get("raw_instance")),
    ctd_agree_per_case={r["case"]: [r.get("ctd_agree"), r.get("ctd_disagree")] for r in t25},
    ctd_call={r["case"]: ("L6" if 25 in (r.get("ctd_labels") or []) and 28 not in (r.get("ctd_labels") or []) else
                          "T13" if 28 in (r.get("ctd_labels") or []) and 25 not in (r.get("ctd_labels") or []) else
                          "both" if 25 in (r.get("ctd_labels") or []) else "none") for r in t25},
    mtime=sorted(set(r.get("mtime", "")[:10] for r in t25)),
)

# ---- C6: bodies whose source is raw
bod = [r for r in rows if r.get("kind") == "body"]
by = Counter()
for r in bod:
    p = r["path"]
    tree = "bodies_cobra" if "/bodies_cobra/" in p else ("bodies" if "/spineps/bodies/" in p else "other")
    pre = r["case"].split("_")[0] if "_" in r["case"] else r["case"][:1]
    by[(tree, pre, r.get("verdict"))] += 1
out["C6_bodies_by_tree_prefix_verdict"] = {"|".join(map(str, k)): v for k, v in sorted(by.items())}
out["C6_raw_or_scrambled_total"] = sum(v for k, v in by.items() if k[2] in ("raw_or_scrambled", "not_verse_order", "not_verse_ids"))
json.dump(out, sys.stdout, indent=1)
