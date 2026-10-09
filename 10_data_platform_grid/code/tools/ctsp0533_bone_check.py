# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/ctsp0533_bone_check.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Is the rebuilt 0533 the right CT, or does the manifest mean something else by bone_pct?

The rebuild passes every geometric gate and reads 75.7% of labelled voxels at or above 200 HU,
against the manifest's `spine_bone_pct` of 85.1 for this record. Two readings:

  A. the rebuild is the wrong volume (the other acquisition of the same patient), or
  B. 75.7 and 85.1 are not the same measurement -- a different mask (all labels here, and the
     released label is v11 while the manifest was written for v10), or a different subset.

They are told apart by measuring records whose CT is NOT in question. For each control the same
quantities are computed from the RELEASED CT, so whatever offset the manifest's definition
carries shows up there too. If the controls sit 9 points below their own `spine_bone_pct` under
the all-labels measurement and land on it under some other subset, reading B is established and
0533 is judged under that subset.

Nothing here writes to the release tree. It only measures.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import nibabel as nib

BONE_HU = 200.0
VERT = list(range(1, 26)) + [28]                 # C1..L6 and T13
PELVIS = [26, 27, 29, 30, 31, 32, 33]            # sacrum, coccyx, the retired S1 (v10), hips, femora
RIBS = list(range(34, 62))
HARDWARE = list(range(62, 69))
GROUPS = {"vertebrae": VERT, "pelvis": PELVIS, "ribs": RIBS,
          "vert+pelvis": VERT + PELVIS, "vert+ribs": VERT + RIBS,
          "all": VERT + PELVIS + RIBS + HARDWARE}


def frac(img: np.ndarray, lab: np.ndarray, ids) -> tuple[float, int]:
    m = np.isin(lab, ids)
    n = int(m.sum())
    if not n:
        return float("nan"), 0
    return float((img[m] >= BONE_HU).mean() * 100.0), n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", default="~/data/CTSpinoPelvic1K")
    ap.add_argument("--case", default="0533")
    ap.add_argument("--case-ct", required=True, help="the REBUILT CT for --case")
    ap.add_argument("--controls", nargs="+", required=True,
                    help="record ids whose released CT is known good")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    rel = Path(a.release).expanduser()
    recs = json.loads((rel / "manifest.json").read_text(encoding="utf-8"))
    recs = recs if isinstance(recs, list) else recs.get("records", list(recs.values()))
    by_id = {str(r.get("volume_id")): r for r in recs}

    rows = []
    for cid in [a.case] + list(a.controls):
        ct_p = Path(a.case_ct) if cid == a.case else rel / "ct" / f"{cid}_ct.nii.gz"
        if not ct_p.exists():
            print(f"  {cid}: no CT at {ct_p}, skipped", flush=True)
            continue
        try:
            img = np.asarray(nib.load(str(ct_p)).dataobj, dtype=np.float32)
        except Exception as e:                                          # noqa: BLE001
            print(f"  {cid}: CT unreadable ({type(e).__name__}), skipped", flush=True)
            continue
        row = {"case": cid, "rebuilt": cid == a.case,
               "manifest_spine_bone_pct": by_id.get(cid, {}).get("spine_bone_pct"),
               "manifest_pelvic_bone_pct": by_id.get(cid, {}).get("pelvic_bone_pct"),
               "manifest_n_voxels_fg": by_id.get(cid, {}).get("n_voxels_fg"),
               "config": by_id.get(cid, {}).get("config"),
               "match_type": by_id.get(cid, {}).get("match_type")}
        for ver, sub in (("v11", "labels"), ("v10", "labels_v10")):
            lp = rel / sub / f"{cid}_label.nii.gz"
            if not lp.exists():
                continue
            lab = np.asanyarray(nib.load(str(lp)).dataobj)
            if lab.shape != img.shape:
                row[f"{ver}_shape_mismatch"] = [list(lab.shape), list(img.shape)]
                continue
            row[f"{ver}_fg_voxels"] = int(((lab > 0) & (lab != 255)).sum())
            for g, ids in GROUPS.items():
                f, n = frac(img, lab, ids)
                row[f"{ver}_{g}_pct"] = None if f != f else round(f, 2)
                row[f"{ver}_{g}_vox"] = n
            del lab
        del img
        rows.append(row)
        print(f"  {cid}: manifest spine {row['manifest_spine_bone_pct']} pelvic "
              f"{row['manifest_pelvic_bone_pct']} | v11 all {row.get('v11_all_pct')} "
              f"vert {row.get('v11_vertebrae_pct')} vert+pelvis {row.get('v11_vert+pelvis_pct')} "
              f"pelvis {row.get('v11_pelvis_pct')} ribs {row.get('v11_ribs_pct')} | "
              f"v10 all {row.get('v10_all_pct')} vert {row.get('v10_vertebrae_pct')}", flush=True)

    # which computed quantity IS the manifest's spine_bone_pct? decided on the controls alone
    ctrl = [r for r in rows if not r["rebuilt"] and r.get("manifest_spine_bone_pct") is not None]
    summary = {}
    for ver in ("v11", "v10"):
        for g in GROUPS:
            k = f"{ver}_{g}_pct"
            d = [r[k] - r["manifest_spine_bone_pct"] for r in ctrl if r.get(k) is not None]
            if d:
                summary[k] = {"n": len(d), "median_delta": round(float(np.median(d)), 2),
                              "mean_abs_delta": round(float(np.mean(np.abs(d))), 2),
                              "min": round(float(np.min(d)), 2), "max": round(float(np.max(d)), 2)}
    best = min(summary, key=lambda k: summary[k]["mean_abs_delta"]) if summary else None
    out = {"rows": rows, "control_deltas_vs_manifest_spine_bone_pct": summary,
           "closest_to_manifest": best}
    if best:
        case_row = next((r for r in rows if r["rebuilt"]), None)
        d = [r[best] - r["manifest_spine_bone_pct"] for r in ctrl if r.get(best) is not None]
        if case_row and case_row.get(best) is not None:
            cd = case_row[best] - case_row["manifest_spine_bone_pct"]
            inside = float(np.min(d)) - 1e-9 <= cd <= float(np.max(d)) + 1e-9
            out["case_delta"] = round(cd, 2)
            out["case_delta_inside_control_range"] = bool(inside)
            print(f"\n  the manifest's spine_bone_pct is closest to {best} "
                  f"(controls: mean |delta| {summary[best]['mean_abs_delta']}, "
                  f"range {summary[best]['min']} to {summary[best]['max']})")
            print(f"  {a.case} under that same measurement: delta {cd:+.2f} -- "
                  f"{'INSIDE' if inside else 'OUTSIDE'} the control range")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"BONE_CHECK_DONE rows={len(rows)} controls={len(ctrl)} closest={best} "
          f"case_inside={out.get('case_delta_inside_control_range')}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
