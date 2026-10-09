# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/level_inventory.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""How many distinct PATIENTS carry each vertebral level, by source and by where the label came from.

WHY PATIENTS AND NOT CROPS. A rare class is not learned from crops, it is learned from people. Bank v5 holds
253,763 crops and fewer than a hundred distinct spines with a sixth lumbar vertebra; counting crops makes the
corpus look forty times richer in L6 than it is, because the same few spines are rendered from many poses.
Every count here is of distinct patient stems, with the crop count beside it so the ratio is visible.

WHAT THE LABEL ORIGIN COLUMN DECIDES. A level counted from a landmark is only as good as the landmark; a
level a decoder assigned is only as good as the decoder's alphabet, and the decoder's alphabet is ordinary.
That is why the pseudolabelled sources report zero sixth-lumbar and zero thirteenth-thoracic vertebrae: not
because their films have none, but because nothing in that pipeline can emit one. The gap between the zero
they report and the population prevalence is the number of mislabelled transitional spines sitting in the
corpus, and it is the quantity a reading programme would recover.

    python tools/level_inventory.py --banks ~/allspine_v2_fov96_ctx ~/allspine_v5_fov96_ctx ~/allspine_v6_fov96_ctx
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

# how each source's level names were arrived at
ORIGIN = {
    "NHANESPS": "pseudolabel", "VINDRPS": "pseudolabel", "LAT236PS": "pseudolabel",
    "nhanes": "human", "csxa": "human", "vindr": "human", "mendeley": "human",
    "buu_full": "counted", "aasce": "counted",
    "ctsp_drr": "from CT", "verse_drr": "from CT", "physics_drr": "from CT", "physics_rare": "from CT",
    "nhanes_drr": "from CT", "obl2": "from CT", "ctsp_drr_obl2": "from CT", "verse_drr_obl2": "from CT",
}
VARIANT = ("T13", "L6")


def origin_of(src: str) -> str:
    if src in ORIGIN:
        return ORIGIN[src]
    for k, v in ORIGIN.items():
        if src.startswith(k):
            return v
    return "other"


def patient_of(case: str) -> str:
    """The person behind a crop: render pose, view and hardware variant suffixes removed."""
    c = re.sub(r"_(lat|ap|obl\w*)(_p\d+)?$", "", str(case))
    c = re.sub(r"_v\d+$", "", c)
    c = re.sub(r"_p\d+$", "", c)
    m = re.search(r"(\d{4,6}-[FM]-\d{3}Y)", c)          # BUU / Mendeley study ids
    if m:
        return m.group(1)
    m = re.search(r"(\d{5})", c)                          # NHANES numbers
    if m:
        return m.group(1)
    return c


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--banks", nargs="+", required=True)
    ap.add_argument("--rung", type=int, default=1)
    ap.add_argument("--out", default="~/model_night/LEVEL_INVENTORY.json")
    a = ap.parse_args()
    report = {}
    for bank in a.banks:
        b = Path(os.path.expanduser(bank))
        f = b / f"rung_{a.rung}.npz"
        if not f.exists():
            print(f"{b.name}: not present"); continue
        z = np.load(str(f), allow_pickle=True)
        y = z["y"]; case = np.array([str(c) for c in z["case"]])
        src = np.array([str(s) for s in z["source"]]); split = np.array([str(s) for s in z["split"]])
        classes = json.load(open(b / "meta.json"))["classes"]

        # (level, origin) -> patients, crops -- training rows only, because that is what teaches
        pat = defaultdict(set); crop = defaultdict(int)
        pat_src = defaultdict(set)
        tr = np.where(split == "train")[0]
        for i in tr:
            lv = classes[int(y[i])]; og = origin_of(src[i]); p = patient_of(case[i])
            pat[(lv, og)].add(p); crop[(lv, og)] += 1
            pat_src[(lv, src[i])].add(p)
        origins = sorted({o for _, o in pat})
        print(f"\n===== {b.name}   {len(y):,} crops, {len(tr):,} training")
        print(f"{'level':<8}" + "".join(f"{o:>22}" for o in origins) + f"{'TOTAL patients':>18}")
        rows = {}
        for lv in classes:
            cells, tot = [], set()
            for o in origins:
                s_ = pat.get((lv, o), set())
                tot |= s_
                cells.append(f"{len(s_):>8} pt /{crop.get((lv, o), 0):>7}" if s_ else f"{'-':>18}")
            if tot:
                mark = "  <<<" if lv in VARIANT else ""
                print(f"{lv:<8}" + "".join(f"{c:>22}" for c in cells) + f"{len(tot):>18}{mark}")
                rows[lv] = {o: {"patients": len(pat.get((lv, o), set())), "crops": crop.get((lv, o), 0)}
                            for o in origins if pat.get((lv, o))}
                rows[lv]["total_patients"] = len(tot)
        report[b.name] = {"crops": int(len(y)), "train": int(len(tr)), "levels": rows}

        # the variant classes, by source, because that is where a reading programme would be aimed
        print(f"\n  variant classes by source (training patients):")
        for lv in VARIANT:
            srcs = {s: len(v) for (l_, s), v in pat_src.items() if l_ == lv}
            print(f"    {lv:<5} " + (", ".join(f"{s}={n}" for s, n in sorted(srcs.items(), key=lambda kv: -kv[1]))
                                     if srcs else "no training patient in any source"))
            report[b.name].setdefault("variant_by_source", {})[lv] = srcs
    out = Path(os.path.expanduser(a.out))
    json.dump(report, open(out, "w"), indent=1)
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
