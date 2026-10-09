#!/usr/bin/env python3
"""Write a copy of docs/RSNAI_DATA_MANIFEST.json whose root paths point at the new CephFS locations, so the hashed
roots can be re-checked on the copy BEFORE the HOME originals are cut over:

    python3 plan/remap_manifest.py                      # writes plan/RSNAI_DATA_MANIFEST.remapped.json
    python3 ../tools/data_manifest.py check --manifest plan/RSNAI_DATA_MANIFEST.remapped.json

After the cut-over the original manifest checks too, through the symlinks at the old paths
(`os.walk` follows a symlinked top directory). Standard library only.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "docs", "RSNAI_DATA_MANIFEST.json")
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "RSNAI_DATA_MANIFEST.remapped.json")
    m = json.load(open(src, encoding="utf-8"))
    moves = [(r["current_path"].rstrip("/"), r["target_path"].rstrip("/"))
             for r in csv.DictReader(open(os.path.join(HERE, "layout_map.csv"), encoding="utf-8"))
             if r["action"] == "move" and r["target_path"]]
    moves.sort(key=lambda t: -len(t[0]))
    changed = 0
    for name, r in m["roots"].items():
        p = r["path"].rstrip("/")
        for old, new in moves:
            if p == old or p.startswith(old + "/"):
                r["path_before_migration"] = r["path"]
                r["path"] = new + p[len(old):]
                changed += 1
                print("%-18s %s\n%-18s -> %s" % (name, p, "", r["path"]))
                break
    m["remapped_from"] = os.path.relpath(src, REPO).replace("\\", "/")
    json.dump(m, open(out, "w", encoding="utf-8"), indent=1)
    print("%d of %d roots remapped; wrote %s" % (changed, len(m["roots"]), out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
