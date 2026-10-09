#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_ts_annotate.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Post-pass for the rare-class TotalSegmentator renders: naming, identity and pseudo-truth in every ann.

render_physics_drr.py was pointed at SPINEPS masks through its `verse` scheme (the masks carry VerSe ids:
25 = L6, 28 = T13), so every case came out named `verse_TS_s0224_lat_p0` -- a TotalSegmentator subject
wearing a VerSe prefix. That is exactly the cross-naming that put one person on both sides of a split
twice before (docs/PATIENT_IDENTITY_SPEC.md), so this pass:

  1. renames img/ann pairs to the existing TS render convention `totalseg_s0224_lat_p0`
     (patient_keys.py `ts_render` scheme);
  2. writes identity INTO the ann: patient_id `ts_s0224` (patient_keys keys it `ts:s0224`),
     scheme `totalseg`, source_case `TS_s0224`, and keeps the mask id scheme on record
     (`mask_scheme: verse_ids_spineps`);
  3. writes the pseudo-truth statement: truth `spineps_veridah`, and `subtype` / `subtype_source`
     carried from SchwingNet/results/rare_class/transitional_subtypes.csv -- these labels are a
     SPINEPS+VERIDAH call, not a radiologist read, and every consumer should see that in the ann;
  4. optionally draws box-overlay PNG previews so a human can check the boxes sit on bodies and the
     extra body carries the right label (L6 on these 12).

Idempotent: an ann that already carries patient_id is left alone (previews can still be drawn).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import numpy as np

RX_OLD = re.compile(r"^verse_(TS_s\d+)_(lat|ap)_p(\d+)$")
RX_NEW = re.compile(r"^totalseg_(s\d+)_(lat|ap)_p(\d+)$")


def load_subtype_rows(csv_path):
    rows = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("source") or "").strip() == "totalsegmentator":
                rows[(r.get("case") or "").strip()] = r
    return rows


def annotate(dst: Path, case: str, rows: dict, override: dict | None = None) -> dict:
    """Rename + annotate every frame of one source case. Returns a small census."""
    ann_dir, img_dir = dst / "ann", dst / "img"
    stok = case.replace("TS_", "")                    # s0224
    row = rows.get(case)
    if row is None:
        raise SystemExit(f"{case}: no totalsegmentator row in the subtype table -- refusing to guess")
    n_seen, n_renamed, level_counts = 0, 0, {}
    for ap in sorted(ann_dir.glob(f"verse_{case}_*.json")) + sorted(ann_dir.glob(f"totalseg_{stok}_*.json")):
        stem = ap.stem
        m = RX_OLD.match(stem)
        if m:
            view, p = m.group(2), m.group(3)
            new = f"totalseg_{stok}_{view}_p{p}"
        else:
            mn = RX_NEW.match(stem)
            if not mn:
                continue
            new, view, p = stem, mn.group(2), mn.group(3)
        ann = json.load(open(ap))
        if m:  # rename the pair; a dangling img would make the bank lie, so it is required
            ip = img_dir / f"{stem}.npy"
            if not ip.exists():
                print(f"  {stem}: ann without img -- dropping the ann", flush=True)
                ap.unlink()
                continue
            ip.rename(img_dir / f"{new}.npy")
            ap_new = ann_dir / f"{new}.json"
            ap.unlink()
            ap = ap_new
            n_renamed += 1
        if not ann.get("patient_id"):
            ann.update({
                "case": new,
                "scheme": "totalseg",
                "mask_scheme": "verse_ids_spineps",
                "source_case": case,
                "patient_id": f"ts_{stok}",
                "corpus": "totalsegmentator",
                "truth": "spineps_veridah",
                "subtype": (override or {}).get("subtype") or (row.get("subtype") or "").strip(),
                "subtype_source": (override or {}).get("subtype_source") or (row.get("truth_source") or "").strip(),
                "subtype_confidence": (override or {}).get("subtype_confidence") or (row.get("confidence") or "").strip(),
                "v8_split": (row.get("v8_split") or "").strip(),
            })
            json.dump(ann, open(ap, "w"))
        n_seen += 1
        for lv in ann.get("levels", {}).values():
            level_counts[lv["name"]] = level_counts.get(lv["name"], 0) + 1
    return {"case": case, "frames": n_seen, "renamed": n_renamed,
            "subtype": (row.get("subtype") or "").strip(), "levels": level_counts}


def preview(dst: Path, case: str, n: int):
    """Box-overlay PNGs for the first n frames (one lat, one ap first) under <dst>/preview/."""
    from PIL import Image, ImageDraw
    stok = case.replace("TS_", "")
    ann_dir, img_dir = dst / "ann", dst / "img"
    out = dst / "preview"
    out.mkdir(exist_ok=True)
    picks = []
    for view in ("lat", "ap"):
        for p in range(0, 50):
            ap = ann_dir / f"totalseg_{stok}_{view}_p{p}.json"
            if ap.exists():
                picks.append(ap)
                break
    for ap in sorted(ann_dir.glob(f"totalseg_{stok}_*.json")):
        if len(picks) >= n:
            break
        if ap not in picks:
            picks.append(ap)
    made = []
    for ap in picks[:n]:
        ann = json.load(open(ap))
        img = np.load(img_dir / f"{ap.stem}.npy")
        im = Image.fromarray(img).convert("RGB")
        dr = ImageDraw.Draw(im)
        for lv in ann.get("levels", {}).values():
            x0, y0, x1, y1 = lv["box"]
            col = (255, 60, 60) if lv["name"] in ("L6", "T13") else (80, 200, 255)
            dr.rectangle([x0, y0, x1, y1], outline=col, width=2)
            dr.text((x0 + 3, max(0, y0 + 2)), lv["name"], fill=col)
        for an in ann.get("anchors", []):
            x0, y0, x1, y1 = an["box"]
            dr.rectangle([x0, y0, x1, y1], outline=(120, 255, 120), width=1)
            dr.text((x0 + 3, max(0, y0 + 2)), an["cls"], fill=(120, 255, 120))
        f = out / f"{ap.stem}_boxes.png"
        im.save(f)
        made.append(str(f))
    return made


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dst", required=True)
    ap.add_argument("--case", required=True, help="source case id, e.g. TS_s0224")
    ap.add_argument("--subtypes", required=True, help="transitional_subtypes.csv")
    ap.add_argument("--previews", type=int, default=0)
    ap.add_argument("--subtype-override", default=None,
                    help="subtype_fix.json from rare_class_ts_fixids.py; its subtype fields supersede the CSV row "
                         "(the CSV called all 12 L6 off scrambled mask ids; the ctd naming is the real VERIDAH call)")
    a = ap.parse_args()
    dst = Path(a.dst).expanduser()
    rows = load_subtype_rows(Path(a.subtypes).expanduser())
    override = json.load(open(a.subtype_override)) if a.subtype_override else None
    census = annotate(dst, a.case, rows, override)
    print(json.dumps(census), flush=True)
    if a.previews:
        for f in preview(dst, a.case, a.previews):
            print("preview", f, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
