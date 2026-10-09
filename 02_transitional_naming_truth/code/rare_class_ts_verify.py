#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_ts_verify.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Census of the repaired rare-class TotalSegmentator render root.

Counts frames per source case, per subtype, and box instances per level name; checks every ann carries
case/scheme/source_case/patient_id/truth/subtype; and flags any ann whose level names are not
S-I monotonic on the detector (top-of-image order must walk the spine in one direction).
"""
import json, glob, os, sys

ORDER = {f"C{i}": i for i in range(1, 8)}
ORDER.update({f"T{i}": 7 + i for i in range(1, 13)})
ORDER["T13"] = 19.5
ORDER.update({f"L{i}": 19 + i for i in range(1, 7)})

def main():
    root = sys.argv[1]
    anns = sorted(glob.glob(os.path.join(root, "ann", "*.json")))
    per_case, per_subtype, per_level, missing, nonmono = {}, {}, {}, [], []
    for p in anns:
        a = json.load(open(p))
        need = ["case", "scheme", "source_case", "patient_id", "truth", "subtype", "subtype_source"]
        if any(not a.get(k) for k in need):
            missing.append(os.path.basename(p))
        sc = a.get("source_case", "?")
        per_case[sc] = per_case.get(sc, 0) + 1
        st = a.get("subtype", "?")
        per_subtype[st] = per_subtype.get(st, 0) + 1
        lv = [(v["box"][1] + v["box"][3], v["name"]) for v in a.get("levels", {}).values()]
        for _, n in lv:
            per_level[n] = per_level.get(n, 0) + 1
        lv.sort()
        ranks = [ORDER[n] for _, n in lv if n in ORDER]
        if ranks:
            inc = all(ranks[i] <= ranks[i+1] for i in range(len(ranks)-1))
            dec = all(ranks[i] >= ranks[i+1] for i in range(len(ranks)-1))
            if not (inc or dec):
                nonmono.append(os.path.basename(p))
    out = {"n_frames": len(anns), "per_case": per_case, "per_subtype": per_subtype,
           "per_level": dict(sorted(per_level.items(), key=lambda kv: ORDER.get(kv[0], 99))),
           "missing_fields": missing, "non_monotonic_level_names": nonmono[:50],
           "n_non_monotonic": len(nonmono)}
    dst = os.path.join(root, "verify_census.json")
    json.dump(out, open(dst, "w"), indent=1)
    print(json.dumps(out, indent=1)[:4000])
    print("wrote", dst)

if __name__ == "__main__":
    main()
