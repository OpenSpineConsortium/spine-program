#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_annotate.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Stamp subtype truth into a rare-class render bank and prove the boxes with preview PNGs.

WHY A POST-PASS. render_physics_drr writes `case`, `source_case`, `scheme` into every ann but knows
nothing about patients or transitional subtypes. The level-bank split is drawn on PEOPLE
(tools/patient_keys.py), and the whole point of this bank is per-SUBTYPE evaluation, so every ann
must carry `patient_id` (ctsp_<release id>, the form patient_keys normalises), `subtype` and
`subtype_source` from SchwingNet/results/rare_class/rare_ctsp_subtypes.json -- the radiologist-consensus
table, never re-derived here.

It also writes box-overlaid preview PNGs (levels green, L6 red, sacrum anchor blue) because rendering
the mask is how this project catches what numbers miss, and a per-case summary JSON under
dst/summary/ so frame counts per class and subtype aggregate without re-reading every ann.

    python tools/rare_class_annotate.py --dst /rs/.../rare_class/ctsp_drr \
        --subtypes SchwingNet/results/rare_class/rare_ctsp_subtypes.json --case 0005
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def draw_box(rgb, box, color, w=2):
    x0, y0, x1, y1 = (int(v) for v in box)
    h, ww = rgb.shape[:2]
    x0, x1 = max(0, x0), min(ww - 1, x1)
    y0, y1 = max(0, y0), min(h - 1, y1)
    rgb[y0:y0 + w, x0:x1 + 1] = color
    rgb[max(0, y1 - w + 1):y1 + 1, x0:x1 + 1] = color
    rgb[y0:y1 + 1, x0:x0 + w] = color
    rgb[y0:y1 + 1, max(0, x1 - w + 1):x1 + 1] = color


def preview(img_npy, ann, out_png):
    from PIL import Image, ImageDraw
    g = np.load(img_npy)
    rgb = np.stack([g, g, g], -1)
    for name, lv in ann.get("levels", {}).items():
        color = (255, 60, 60) if name == "L6" else (60, 220, 60)
        draw_box(rgb, lv["box"], color)
    for an in ann.get("anchors", []):
        if an["cls"] == "sacrum":
            draw_box(rgb, an["box"], (80, 140, 255))
    im = Image.fromarray(rgb.astype(np.uint8))
    d = ImageDraw.Draw(im)
    for name, lv in ann.get("levels", {}).items():
        x0, y0 = lv["box"][0], lv["box"][1]
        d.text((min(x0 + 3, im.width - 30), max(0, y0 - 12)), name,
               fill=(255, 60, 60) if name == "L6" else (60, 220, 60))
    d.text((4, 4), f"{ann['case']}  subtype={ann.get('subtype', '?')}", fill=(255, 255, 80))
    im.save(out_png)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dst", required=True)
    ap.add_argument("--subtypes", required=True)
    ap.add_argument("--case", default=None, help="one release id, e.g. 0005; default: every case in the sidecar")
    ap.add_argument("--previews", type=int, default=3, help="preview PNGs per case")
    a = ap.parse_args()
    dst = Path(a.dst).expanduser()
    side = json.load(open(a.subtypes))["cases"]
    cases = [a.case] if a.case else sorted(side)
    (dst / "preview").mkdir(exist_ok=True)
    (dst / "summary").mkdir(exist_ok=True)
    for cid in cases:
        meta = side[cid]
        anns = sorted((dst / "ann").glob(f"ctsp_{cid}_*.json"))
        per_level = {}
        n_prev = 0
        for i, p in enumerate(anns):
            ann = json.load(open(p))
            ann["patient_id"] = f"ctsp_{cid.zfill(4)}"
            ann["subtype"] = meta["subtype"]
            ann["subtype_source"] = meta["subtype_source"]
            ann["subtype_modifiers"] = {k: meta[k] for k in
                                        ("castellvi", "four_lumbar_mask", "lumbar_rib",
                                         "n_lumbar_labelled", "mask_representation", "v8_split")}
            json.dump(ann, open(p, "w"))
            for name in ann.get("levels", {}):
                per_level[name] = per_level.get(name, 0) + 1
            if "sacrum" in {an["cls"] for an in ann.get("anchors", [])}:
                per_level["sacrum_anchor"] = per_level.get("sacrum_anchor", 0) + 1
            if n_prev < a.previews:
                img = dst / "img" / (p.stem + ".npy")
                if img.exists():
                    try:
                        preview(img, ann, dst / "preview" / (p.stem + ".png"))
                        n_prev += 1
                    except Exception as e:  # noqa: BLE001
                        print("  preview failed", p.stem, repr(e)[:80])
        summ = {"case": cid, "subtype": meta["subtype"], "subtype_source": meta["subtype_source"],
                "v8_split": meta["v8_split"], "four_lumbar_mask": meta["four_lumbar_mask"],
                "mask_representation": meta["mask_representation"],
                "frames": len(anns), "frames_with_level": per_level}
        json.dump(summ, open(dst / "summary" / f"{cid}.json", "w"), indent=1)
        print(f"{cid} subtype={meta['subtype']} frames={len(anns)} levels={per_level}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
