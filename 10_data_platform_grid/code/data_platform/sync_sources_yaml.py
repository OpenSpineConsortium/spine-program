#!/usr/bin/env python3
"""Rewrite sources.yaml from sources.json (the two must hold the same data; reacquire/test_reacquire.py and
verify_planning.py check it). Edit sources.json, then run this. Standard library only.

    python3 data_platform/sync_sources_yaml.py           # rewrite
    python3 data_platform/sync_sources_yaml.py --check   # exit 1 if they differ
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))
import mini_yaml  # noqa: E402

HEADER = ("sources.yaml: one entry per imaging source (upstream release, project release, derived bank or request).\n"
          "Generated from sources.json (the same data); edit sources.json and run sync_sources_yaml.py.\n"
          "Human-readable cards with every citation: DATA_MANIFEST.md. Read with PyYAML or with lib/mini_yaml.py.")


def main():
    doc = json.load(open(os.path.join(HERE, "sources.json"), encoding="utf-8"))
    yp = os.path.join(HERE, "sources.yaml")
    if "--check" in sys.argv:
        same = mini_yaml.load(open(yp, encoding="utf-8")) == doc
        print("sources.yaml %s sources.json" % ("matches" if same else "DIFFERS FROM"))
        return 0 if same else 1
    with open(yp, "w", encoding="utf-8", newline="\n") as fh:
        mini_yaml.dump(doc, fh, header=HEADER)
    print("wrote", yp, "(%d sources)" % len(doc["sources"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
