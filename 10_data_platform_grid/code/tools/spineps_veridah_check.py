#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_veridah_check.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Two questions the SPINEPS id census leaves open, answered from its rows and from truth held OUTSIDE SPINEPS.

WHY (2026-09-23). The TotalSegmentator "12 SPINEPS+VERIDAH L6" were selected by "id 25 present" in masks whose
ids are raw instance numbers (tools/spineps_id_census.py: ~/bench_ts/spineps/native 1,433 of 1,518 scrambled and
RAW). The repair reads VERIDAH's names from the ctd centroid file instead. That fixes WHICH NAME the tool gave; it
does not say whether the tool's L6 / T13 call is worth anything as truth. Only a reader can say that, and two
collections here carry one beside a VERIDAH ctd: CTSpinoPelvic1K (release labels + two-radiologist Castellvi
consensus, SchwingNet/results/rare_class/transitional_subtypes.csv) and VerSe (raw-mask ids 25 / 28,
SchwingNet/results/anomalous_inventory.json).

  1. per tree: the subtype an id-reading consumer would call (id 25 / 28 present in the mask) against the subtype
     VERIDAH's ctd names -- where these differ, a consumer that reads ids is wrong about VERIDAH's own call;
  2. VERIDAH's ctd call against the reader, on CTSP and on the VerSe volumes of the TS bench;
  3. the TotalSegmentator v2 bench by ctd: which subjects VERIDAH itself calls L6 / T13 (the 12 were never that set).

    python tools/spineps_veridah_check.py --rows /rs/.../or_ready/spineps_ids/census_rows.jsonl \
        --out SchwingNet/results/spineps_ids/veridah_check.json

Reads json/csv only (no masks), so it is cheap; on the grid it still goes through sbatch like everything else.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def sub_of(labs) -> str:
    labs = set(labs or [])
    if not labs:
        return "no_ctd"
    l6, t13 = 25 in labs, 28 in labs
    return "both" if (l6 and t13) else "L6" if l6 else "T13" if t13 else "none"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", required=True, help="census_rows.jsonl from tools/spineps_id_census.py")
    ap.add_argument("--subtypes", default=str(REPO / "SchwingNet/results/rare_class/transitional_subtypes.csv"))
    ap.add_argument("--inventory", default=str(REPO / "SchwingNet/results/anomalous_inventory.json"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rows = [json.loads(l) for l in open(a.rows) if l.strip()]
    vert = [r for r in rows if r.get("kind") == "seg-vert"]
    out = dict(rows_file=a.rows, n_rows=len(rows), n_seg_vert=len(vert))

    # 1. id-reading call vs ctd call, per tree
    per_tree = defaultdict(Counter)
    for r in vert:
        ids = set(r.get("ids") or [])
        m = "both" if (25 in ids and 28 in ids) else "L6" if 25 in ids else "T13" if 28 in ids else "none"
        per_tree[os.path.dirname(r["path"])][f"ids:{m} / ctd:{sub_of(r.get('ctd_labels'))}"] += 1
    out["id_call_vs_ctd_call_by_tree"] = {k: dict(v) for k, v in sorted(per_tree.items())}

    # 2a. CTSP: reader subtype vs VERIDAH ctd call
    truth = {}
    for r in csv.DictReader(open(a.subtypes, encoding="utf-8")):
        if r["source"] == "ctsp":
            truth[r["case"]] = r["subtype"]
    tab, ex = Counter(), defaultdict(list)
    for r in vert:
        if "/data/spineps/ctsp/" not in r["path"]:
            continue
        case = str(r.get("case", "")).replace("CTSP_", "")
        k = (truth.get(case, "ordinary"), sub_of(r.get("ctd_labels")))
        tab[k] += 1
        ex[k].append(case)
    l6_calls = sum(n for (t, v), n in tab.items() if v in ("L6", "both"))
    l6_on_reader_l6 = sum(n for (t, v), n in tab.items() if t == "L6" and v in ("L6", "both"))
    reader_l6 = sum(n for (t, v), n in tab.items() if t == "L6")
    cc_calls = sum(n for (t, v), n in tab.items() if v in ("L6", "T13", "both"))
    cc_on_reader_l6 = sum(n for (t, v), n in tab.items() if t == "L6" and v in ("L6", "T13", "both"))
    out["ctsp_reader_vs_veridah"] = dict(
        truth="CTSpinoPelvic1K v11 release labels + two-reader Castellvi consensus (transitional_subtypes.csv); "
              "a case absent from that table is ordinary",
        n=sum(tab.values()),
        table={f"reader:{t} / veridah:{v}": n for (t, v), n in sorted(tab.items())},
        cases={f"reader:{t} / veridah:{v}": sorted(c) for (t, v), c in sorted(ex.items()) if t != "ordinary" or v != "none"},
        L6_calls=l6_calls, L6_calls_on_a_reader_L6=l6_on_reader_l6, reader_L6=reader_l6,
        T13_calls=sum(n for (t, v), n in tab.items() if v in ("T13", "both")),
        count_changing_calls=cc_calls, count_changing_calls_on_a_reader_L6=cc_on_reader_l6,
        note="CTSP carries no reader T13 class; a VERIDAH T13 there is either a naming convention for the same "
             "extra segment (6 reader L6 are called T13) or a call on an ordinary spine")

    # 2b. VerSe volumes of the TS bench: raw-mask truth vs VERIDAH ctd call
    inv = json.load(open(a.inventory))["cases"]
    vt = {k.split(":", 1)[1]: ("L6" if v["l6"] else "T13" if v["t13"] else "none")
          for k, v in inv.items() if v["source"] == "verse"}
    tab, ex = Counter(), defaultdict(list)
    for r in vert:
        if "/bench_ts/spineps/native/VERSE_" not in r["path"]:
            continue
        case = str(r.get("case", "")).replace("VERSE_", "")
        k = (vt.get(case, "none"), sub_of(r.get("ctd_labels")))
        tab[k] += 1
        ex[k].append(case)
    out["verse_mask_vs_veridah"] = dict(
        truth="VerSe raw-mask ids (25 = L6, 28 = T13) from anomalous_inventory.json; VERIDAH was developed on VerSe, "
              "so this is its home ground, not an independent test",
        n=sum(tab.values()),
        table={f"verse:{t} / veridah:{v}": n for (t, v), n in sorted(tab.items())},
        cases={f"verse:{t} / veridah:{v}": sorted(c) for (t, v), c in sorted(ex.items()) if t != "none" or v != "none"})

    # 3. TotalSegmentator v2 bench: id-25 selection vs ctd call, subject lists
    tab, ex = Counter(), defaultdict(list)
    for r in vert:
        if "/bench_ts/spineps/native/TS_" not in r["path"]:
            continue
        ids = set(r.get("ids") or [])
        m = "L6" if 25 in ids else "T13" if 28 in ids else "none"
        k = (m, sub_of(r.get("ctd_labels")), bool(r.get("raw_instance")))
        tab[k] += 1
        ex[k].append(r.get("case"))
    out["ts_v2_bench_id_vs_ctd"] = dict(
        n=sum(tab.values()),
        table={f"ids:{m} / ctd:{c} / raw:{raw}": n for (m, c, raw), n in sorted(tab.items())},
        cases={f"ids:{m} / ctd:{c} / raw:{raw}": sorted(v) for (m, c, raw), v in sorted(ex.items())
               if m != "none" or c != "none"},
        ctd_totals=dict(Counter(sub_of(r.get("ctd_labels")) for r in vert if "/bench_ts/spineps/native/TS_" in r["path"])))

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1))
    c = out["ctsp_reader_vs_veridah"]
    print(f"CTSP: VERIDAH L6 calls {c['L6_calls']}, on a reader L6 {c['L6_calls_on_a_reader_L6']} of "
          f"{c['reader_L6']}; T13 calls {c['T13_calls']}; count-changing calls {c['count_changing_calls']}, "
          f"on a reader L6 {c['count_changing_calls_on_a_reader_L6']}")
    print("TS v2 ctd totals:", out["ts_v2_bench_id_vs_ctd"]["ctd_totals"])
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
