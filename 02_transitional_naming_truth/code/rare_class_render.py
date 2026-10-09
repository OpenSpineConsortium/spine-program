#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_render.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Multi-view, multi-pose, device-styled renders of the VerSe transitional scans (the rare-class corpus).

WHAT AND WHY. The 56 raw-mask-verified VerSe transitional scans (50 with an L6, id 25; 6 with a T13, id 28)
are the scarcest truth in the program, and the one final dataset needs every one of them expanded by
LEGITIMATE augmentation: distinct poses and distinct device stylings of one CT, never duplicates (x12
duplication once bought L6 Dice 0.000). Per scan this writes

    10 geometry poses    lateral x3, AP x3, oblique x4 (yaw about the SI axis, small cranio-caudal tilt),
                         each a genuine re-projection of the volume, boxes re-projected with it
    x 6 device stylings  one draw per pose per card (bv_pulsera, cios_fusion, elekta_xvi, pixium_4600,
                         surgio_b51_dr, varian_halcyon), DEVICE_SAMPLE_MODE=typicality
    + the 10 raw bone DRRs                                  -> 70 distinct frames per scan.

CONVENTIONS ARE make_drr_dataset's, IMPORTED, NOT COPIED: to_pir reorients by the affine (never assumed),
pir_spacing reads spacing through the same transform (the S-I spacing fix of 2026-09-19), drr() windows on
bone, project_labels records per-level silhouette boxes AND the overlap it would be flattering to hide,
water_bone_paths_cm carries the device cards' own water/bone definitions. On top of that, ONE change: the
volume is resampled to 1.0 mm isotropic before posing, because VerSe in-plane and slice spacings differ by
4x and a rotated projection of an anisotropic grid has no single mm-per-px; every output frame is therefore
exactly 1.0 mm/px in both axes and the ann says so.

YAW CONVENTION (recorded in every ann): the beam always runs along the volume's left-right axis after the
pose rotation; yaw_deg is how far the anatomy was turned about S-I from the lateral start, so 0 = lateral,
90 = AP, +/-35..50 = the two anterior-oblique families. tilt_deg tips the beam cranio-caudally.

EVERY ann carries: case, scheme=verse, source_case, patient_id=verse_<series> (what tools/patient_keys.py
keys on, resolved series->subject through the VerSeFusion manifest), and the SUBTYPE COLUMNS subtype /
subtype_source from SchwingNet/results/rare_class/verse56_subtypes.json, so the stratified evaluation can
read the stratum off any frame without a join.

MAXIMIZE PASS (2026-09-24, tools/rare_class_maximize.py). The same renderer now serves every CT source of the
transitional registry: --layout stage reads <src>/<case>/<case>_ct.nii.gz + <case>_msk.nii.gz (what
SchwingNet/slurm/rare_max_stage.sh materialises for CTSpinoPelvic1K, TotalSegmentator and CTSpine1K), --scheme
sets the stem / ann scheme (ctsp_<id>, totalseg_<s>, ctspine1k_<stem>) and --patient-id-format the patient_id
(ctsp_0090, ts_s0049: the forms tools/patient_keys.py keys). The subtypes json may carry, per case, patient_key,
truth_tier, subtype_source, modifiers, mask_scheme, fused_mask_representation -- copied into every ann -- and
an ID GUARD: `require_ids` (every listed id must be in the mask, e.g. [25] for an L6 call) and/or
`require_n_lumbar` (exact count of ids 20..25). A case whose mask does not carry the ids its call names is
HELD, not rendered: a frame boxed under names the registry itself disputes is a wrong-but-plausible training
label, and the hold is written to <dst>/held/<scheme>_<case>.json for the review queue. A case already at the
frame floor is skipped (idempotent; a re-render would duplicate poses).

    python tools/rare_class_render.py --src ~/VerSeFusion/data/unified \
        --dst /rs/rs_grp_oschome/go2432/data/rare_class/verse_drr \
        --subtypes ~/spinesurg-ct-nnunet/SchwingNet/results/rare_class/verse56_subtypes.json \
        --shard 0 --n-shards 8
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import nibabel as nib
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_drr_dataset as MDD  # noqa: E402
import device_style as DS  # noqa: E402

ISO_MM = 1.0
CARDS = ["bv_pulsera", "cios_fusion", "elekta_xvi", "pixium_4600", "surgio_b51_dr", "varian_halcyon"]
HIT_CM = 0.5           # a ray that crossed less than 5 mm of water-equivalent tissue missed the patient


def _seed(*parts):
    """Deterministic across processes -- Python's hash() is salted per interpreter and would make every
    rerun a different corpus, which is exactly the reproducibility failure the seeded-checks rule bans."""
    return int(hashlib.md5("|".join(parts).encode()).hexdigest()[:8], 16)


def poses_for(case: str, rng: np.random.Generator):
    """Ten poses: p0 of each family is canonical (no jitter), the rest are drawn per case.

    (view, index, yaw_deg, tilt_deg). Obliques cover BOTH sides at two depths, so the four are distinct
    projections rather than four copies of one.
    """
    j = lambda a: float(rng.uniform(-a, a))  # noqa: E731
    return [
        ("lat", 0, 0.0, 0.0),
        ("lat", 1, j(6.0), j(6.0)),
        ("lat", 2, j(6.0), j(6.0)),
        ("ap", 0, 90.0, 0.0),
        ("ap", 1, 90.0 + j(8.0), j(6.0)),
        ("ap", 2, 90.0 + j(8.0), j(6.0)),
        ("obl", 0, 35.0 + j(5.0), j(8.0)),
        ("obl", 1, 50.0 + j(5.0), j(8.0)),
        ("obl", 2, -35.0 + j(5.0), j(8.0)),
        ("obl", 3, -50.0 + j(5.0), j(8.0)),
    ]


def iso_resample(arr, sp_pir, order, cval):
    from scipy.ndimage import zoom
    f = [s / ISO_MM for s in sp_pir]
    return zoom(arr, f, order=order, cval=cval, prefilter=(order > 0))


def rotate_pair(ct, gt, yaw, tilt):
    """Rotate CT (linear, air fill) and mask (nearest, background fill) identically; beam stays axis 2.

    yaw about S-I mixes A-P into the beam axis: plane (0, 2). tilt about A-P mixes S-I in: plane (1, 2).
    reshape=True on both with the same angles keeps the two grids congruent.
    """
    from scipy.ndimage import rotate
    if abs(yaw) > 0.25:
        ct = rotate(ct, yaw, axes=(0, 2), reshape=True, order=1, cval=-1000.0, prefilter=False)
        gt = rotate(gt, yaw, axes=(0, 2), reshape=True, order=0, cval=0, prefilter=False)
    if abs(tilt) > 0.25:
        ct = rotate(ct, tilt, axes=(1, 2), reshape=True, order=1, cval=-1000.0, prefilter=False)
        gt = rotate(gt, tilt, axes=(1, 2), reshape=True, order=0, cval=0, prefilter=False)
    return ct, gt


def save_frame(dst, stem, img8, ann, png=True):
    np.save(dst / "img" / f"{stem}.npy", img8)
    json.dump(ann, open(dst / "ann" / f"{stem}.json", "w"), indent=1)
    if png:
        from PIL import Image
        Image.fromarray(img8).save(dst / "img" / f"{stem}.png")


def overlay(dst, stem, img8, levels):
    """A QC frame with the projected boxes drawn and named, for eyes, not for training."""
    from PIL import Image, ImageDraw
    im = Image.fromarray(img8).convert("RGB")
    d = ImageDraw.Draw(im)
    for cid, rec in levels.items():
        x0, y0, x1, y1 = rec["box"]
        red = rec["name"] in ("L6", "T13")
        d.rectangle([x0, y0, x1, y1], outline=(255, 60, 60) if red else (80, 200, 255), width=2 if red else 1)
        d.text((x0 + 2, max(0, y0 - 10)), rec["name"], fill=(255, 60, 60) if red else (80, 200, 255))
    im.save(dst / "qc" / f"{stem}_overlay.png")


def case_paths(src, case, layout):
    if layout == "verse":
        return src / f"scan-{case}" / f"scan-{case}_ct.nii.gz", src / f"scan-{case}" / f"scan-{case}_msk.nii.gz"
    return src / case / f"{case}_ct.nii.gz", src / case / f"{case}_msk.nii.gz"


EXTRA_FIELDS = ("patient_key", "truth_tier", "modifiers", "mask_scheme", "fused_mask_representation",
                "castellvi", "four_lumbar", "lumbar_rib", "registry_source_case")


def guard(ids_present, sub):
    """The call's ids must be in the mask, or the case is held. Returns a reason string or None."""
    need = [int(i) for i in (sub.get("require_ids") or [])]
    miss = [i for i in need if i not in ids_present]
    if miss:
        return (f"mask carries ids {ids_present} but the {sub.get('subtype')} call ({sub.get('truth_tier')}) "
                f"needs {need}; missing {miss}: rendered names would contradict the call")
    nl = sub.get("require_n_lumbar")
    if nl is not None:
        have = [i for i in ids_present if 20 <= i <= 25]
        if len(have) != int(nl):
            return (f"mask carries {len(have)} lumbar ids {have} but the call ({sub.get('subtype')}, "
                    f"{sub.get('truth_tier')}) needs exactly {nl}")
    return None


def render_case(case, src, dst, sub, RP, layout="verse", scheme="verse", pid_fmt="{scheme}_{case}"):
    t0 = time.time()
    ip, lp = case_paths(src, case, layout)
    lim = nib.load(str(lp))
    gt = np.asanyarray(lim.dataobj).astype(np.int16)
    ids_present = sorted(int(v) for v in np.unique(gt) if int(v) in MDD.LEVEL_NAMES)
    why = guard(ids_present, sub)
    if why:
        (dst / "held").mkdir(exist_ok=True)
        rec = dict(case=case, scheme=scheme, subtype=sub.get("subtype"), truth_tier=sub.get("truth_tier"),
                   patient_key=sub.get("patient_key"), ids_in_mask=ids_present, held=why, mask=str(lp))
        json.dump(rec, open(dst / "held" / f"{scheme}_{case}.json", "w"), indent=1)
        return dict(case=case, subtype=sub.get("subtype"), held=why, ids_in_mask=ids_present, frames=0)
    ct = np.asanyarray(nib.load(str(ip)).dataobj).astype(np.float32)
    if ct.shape != gt.shape:
        return dict(case=case, error=f"shape mismatch {ct.shape} vs {gt.shape}")
    ct_p = MDD.to_pir(ct, lim.affine)
    gt_p = MDD.to_pir(gt, lim.affine)
    sp = MDD.pir_spacing(lim.header, lim.affine)
    ct_i = iso_resample(ct_p, sp, 1, -1000.0)
    gt_i = iso_resample(gt_p, sp, 0, 0)
    del ct, gt, ct_p, gt_p

    rng = np.random.default_rng(_seed("rare_class", case))
    devs = {c: DS.load_device(c) for c in CARDS}
    made, by_view, skipped = 0, {}, []
    extra = {k: sub[k] for k in EXTRA_FIELDS if k in sub}
    pid = pid_fmt.format(scheme=scheme, case=case)
    for view, k, yaw, tilt in poses_for(case, rng):
        ctr, gtr = rotate_pair(ct_i, gt_i, yaw, tilt)
        img = MDD.drr(ctr)
        levels, ov, un = MDD.project_labels(gtr, MDD.LEVEL_NAMES)
        if not levels:
            skipped.append(f"{view}_p{k}: no level survived projection")
            continue
        water, bone = MDD.water_bone_paths_cm(ctr, ISO_MM)
        hit = water > HIT_CM
        stem = f"{scheme}_{case}_{view}_p{k}"
        base = dict(
            case=stem, scheme=scheme, source_case=case, patient_id=pid,
            subtype=sub["subtype"], subtype_source=sub["subtype_source"], **extra,
            shape=list(img.shape), axcodes="PIR+iso", mm_per_px_row_si_col_ap=[ISO_MM, ISO_MM],
            view=view, pose=k, yaw_deg=round(yaw, 2), tilt_deg=round(tilt, 2),
            levels={str(cid): rec for cid, rec in levels.items()},
            overlap_px=ov, union_px=un, box_convention="outline", styled=None,
        )
        save_frame(dst, stem, (img * 255).astype(np.uint8), base)
        if k == 0:
            overlay(dst, stem, (img * 255).astype(np.uint8), levels)
        made += 1
        by_view[view] = by_view.get(view, 0) + 1

        # thickness for the AEC condition: median water path in a centre disc of rays that hit
        H, W = water.shape
        yy, xx = np.mgrid[0:H, 0:W]
        disc = ((yy - H / 2) ** 2 + (xx - W / 2) ** 2 <= (0.06 * min(H, W)) ** 2) & hit
        thick = float(np.median(water[disc])) if disc.any() else float("nan")
        for card in CARDS:
            crng = np.random.default_rng(_seed("rare_style", case, view, str(k), card))
            t = DS.sample_terms(devs[card], 1, crng,
                                cond={"thickness_cm": thick} if np.isfinite(thick) else None,
                                mode="typicality")[0]
            simg, _ = DS.style(water.astype(np.float64), bone.astype(np.float64), hit, devs[card], t, crng,
                               ISO_MM, RP=RP)
            slv = {}
            for cid, rec in levels.items():
                r = dict(rec)
                if t["rot180"]:
                    x0, y0, x1, y1 = rec["box"]
                    r["box"] = [W - 1 - x1, H - 1 - y1, W - 1 - x0, H - 1 - y0]
                    cx, cy = rec["centroid"]
                    r["centroid"] = [W - 1 - cx, H - 1 - cy]
                slv[str(cid)] = r
            sann = dict(base, case=f"{stem}_{card}_0", levels=slv,
                        styled=dict(device=card, draw=0, sample_mode="typicality",
                                    rot180=bool(t["rot180"]), aec_extrapolated=bool(t.get("aec_extrapolated"))))
            save_frame(dst, f"{stem}_{card}_0", simg, sann, png=True)
            made += 1
            by_view[f"{view}_{card}"] = by_view.get(f"{view}_{card}", 0) + 1
    return dict(case=case, subtype=sub["subtype"], frames=made, by_view=by_view,
                ids_in_mask=ids_present, skipped=skipped, seconds=round(time.time() - t0, 1))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--subtypes", required=True, help="verse56_subtypes.json: case -> subtype/subtype_source")
    ap.add_argument("--cases", default=None, help="restrict to these cases (comma list)")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--n-shards", type=int, default=1)
    ap.add_argument("--layout", choices=["verse", "stage"], default="verse",
                    help="verse: <src>/scan-<case>/scan-<case>_{ct,msk}; stage: <src>/<case>/<case>_{ct,msk}")
    ap.add_argument("--scheme", default="verse", help="stem prefix and ann scheme (verse, ctsp, totalseg, ctspine1k)")
    ap.add_argument("--patient-id-format", default="{scheme}_{case}",
                    help="ann patient_id, e.g. ts_{case} for TotalSegmentator (tools/patient_keys.py forms)")
    ap.add_argument("--floor", type=int, default=60, help="a case with >= this many anns already is skipped")
    ap.add_argument("--report-tag", default=None, help="RENDER_INFO_<tag>.json instead of shard<k>")
    a = ap.parse_args()
    src, dst = Path(os.path.expanduser(a.src)), Path(os.path.expanduser(a.dst))
    for d in ("img", "ann", "qc"):
        (dst / d).mkdir(parents=True, exist_ok=True)
    subs = json.load(open(os.path.expanduser(a.subtypes)))
    subs = {k: v for k, v in subs.items() if not k.startswith("_")}
    cases = sorted(subs) if not a.cases else [c for c in a.cases.split(",") if c]
    cases = [c for i, c in enumerate(cases) if i % a.n_shards == a.shard]
    print(f"shard {a.shard}/{a.n_shards}: {len(cases)} cases -> {dst} (layout {a.layout}, scheme {a.scheme})",
          flush=True)
    RP = DS.rp_tables()
    reports = []
    for c in cases:
        have = len(list((dst / "ann").glob(f"{a.scheme}_{c}_*.json")))
        if have >= a.floor:
            r = dict(case=c, subtype=subs[c].get("subtype"), frames=have, skipped_already_rendered=True)
            reports.append(r)
            print(json.dumps(r), flush=True)
            continue
        try:
            r = render_case(c, src, dst, subs[c], RP, layout=a.layout, scheme=a.scheme,
                            pid_fmt=a.patient_id_format)
        except Exception as e:  # noqa: BLE001  -- one bad case must cost one case, not the shard
            import traceback
            traceback.print_exc()
            r = dict(case=c, error=f"{type(e).__name__}: {e}")
        reports.append(r)
        print(json.dumps({k: v for k, v in r.items() if k != "by_view"}), flush=True)
    tag = a.report_tag or f"shard{a.shard}"
    json.dump(reports, open(dst / f"RENDER_INFO_{tag}.json", "w"), indent=1)
    ok = [r for r in reports if "error" not in r and "held" not in r]
    held = [r for r in reports if "held" in r]
    print(f"shard {a.shard}: {len(ok)}/{len(cases)} cases, {sum(r['frames'] for r in ok)} frames, "
          f"{len(held)} held (mask names contradict the call)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
