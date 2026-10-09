#!/usr/bin/env python
"""Put a whole-spine CT under DeepFluoro's real C-arm and project its per-vertebra labels.

This is the "apply it to the spine" step, and it deliberately borrows the real device rather than
constructing one. A DeepFluoro pose is a 4x4 that placed a real CIOS Fusion around a real pelvis; the
only thing that changes here is the volume in front of it. The chosen vertebra's centroid is moved to
where that pose saw the pelvis landmark centroid, and then the SAME ext @ inv(T) and the SAME K project
it -- exact geometry, settled to 0.00 px, with nothing new to get wrong. A cranial sweep is the same
pose with the target moved one body at a time.

Labels come from projecting each vertebra mask's voxels through that geometry: the box is where the
bone actually lands on the detector, at whatever magnification the real source-to-object distance
gives. Nothing is annotated.

Anatomy comes from TotalSegmentator (156 of 1939 subjects carry both C2 and sacrum, 1.5 mm), not
VerSe, which turned out to be regional. Volumes are reoriented to LPS to match DeepFluoro's frame and
handed to the same ray-caster the DeepFluoro pairs were rendered with.

    python tools/spine_project.py --subject s0462 --target vertebrae_L3 --pose 17-1882/000 --down 4
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

TS = os.path.expanduser("~/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300")
ORDER = (["vertebrae_C%d" % i for i in range(1, 8)] + ["vertebrae_T%d" % i for i in range(1, 13)]
         + ["vertebrae_L%d" % i for i in range(1, 7)] + ["sacrum"])


def load_lps(path):
    """A NIfTI as an axis-aligned LPS volume: array (z, y, x), origin (x0, y0, z0) mm, spacing (sx, sy, sz)."""
    import nibabel as nib
    img = nib.as_closest_canonical(nib.load(path))              # RAS, positive spacing
    a = np.asarray(img.dataobj)
    sx, sy, sz = [float(v) for v in img.header.get_zooms()[:3]]
    x0, y0, z0 = [float(v) for v in img.affine[:3, 3]]
    nx, ny, nz = a.shape
    # RAS -> LPS: reverse x and y; the origin moves to the other end of each reversed axis
    a = a[::-1, ::-1, :]
    org = np.array([-(x0 + (nx - 1) * sx), -(y0 + (ny - 1) * sy), z0], np.float64)
    return np.ascontiguousarray(np.transpose(a, (2, 1, 0))), org, np.array([sx, sy, sz], np.float64)


def load_geometry(h5, spec, pid):
    import h5py
    with h5py.File(h5, "r") as f:
        pp = f["proj-params"]
        K = np.array(pp["intrinsic"], np.float64); ext = np.array(pp["extrinsic"], np.float64)
        nr, nc = int(np.array(pp["num-rows"])), int(np.array(pp["num-cols"]))
        px = float(np.array(pp["pixel-row-spacing"]))
        g = f[spec]
        vl = np.stack([np.array(g["vol-landmarks"][k], np.float64).ravel() for k in g["vol-landmarks"]])
        T = np.array(g["projections"][pid]["gt-poses"]["cam-to-pelvis-vol"], np.float64)
        rot = int(np.array(g["projections"][pid]["rot-180-for-up"]))
    return dict(K=K, ext=ext, nr=nr, nc=nc, px_mm=px, T=T, rot=rot, c_df=vl.mean(0))


def centroid_mm(mask, org, sp):
    zz, yy, xx = np.nonzero(mask)
    return np.array([xx.mean() * sp[0] + org[0], yy.mean() * sp[1] + org[1], zz.mean() * sp[2] + org[2]])


def project_mask(mask, org, sp, M, K, down, nr, nc, step=2):
    """Bounding box of a mask's projection, in the downsampled detector's (col, row), plus its coverage."""
    zz, yy, xx = np.nonzero(mask[::step, ::step, ::step])
    if xx.size == 0:
        return None
    P = np.c_[xx * step * sp[0] + org[0], yy * step * sp[1] + org[1], zz * step * sp[2] + org[2], np.ones(xx.size)]
    Pc = (M @ P.T).T[:, :3]
    uvw = (K @ Pc.T).T; uv = uvw[:, :2] / uvw[:, 2:3] / down
    inside = (uv[:, 0] >= 0) & (uv[:, 0] < nc / down) & (uv[:, 1] >= 0) & (uv[:, 1] < nr / down)
    if inside.mean() < 0.02:
        return None
    q = uv[inside]
    return dict(box=[float(q[:, 0].min()), float(q[:, 1].min()), float(q[:, 0].max()), float(q[:, 1].max())],
                inside=float(inside.mean()))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", default="s0462")
    ap.add_argument("--target", default="vertebrae_L3", help="the vertebra placed where the real pose saw the pelvis")
    ap.add_argument("--pose", default="17-1882/000", help="spec/pid of the real DeepFluoro pose to borrow")
    ap.add_argument("--h5", default="~/deepfluoro/unpacked_full/ipcai_2020_full_res_data.h5")
    ap.add_argument("--down", type=int, default=4)
    ap.add_argument("--out", default="~/model_night/spine_project")
    ap.add_argument("--calibration", default="~/model_night/deepfluoro/calibration.json",
                    help="fitted device terms; the frame is emitted through them with a quantum draw")
    ap.add_argument("--photons", type=float, default=4000.0,
                    help="quantum budget per pixel for the noise draw; 400 was visibly too grainy")
    ap.add_argument("--no-strip-table", action="store_true",
                    help="keep the scanner table. By default everything outside the largest connected "
                         "body region above -300 HU is set to air, which removes it.")
    a = ap.parse_args()
    out = Path(os.path.expanduser(a.out)); out.mkdir(parents=True, exist_ok=True)
    spec, pid = a.pose.split("/")
    G = load_geometry(os.path.expanduser(a.h5), spec, pid)

    sub = Path(TS) / a.subject
    vol, org, sp = load_lps(str(sub / "ct.nii.gz"))
    if not a.no_strip_table:
        # the table is a dense slab outside the body. Keep the largest connected region above -300 HU
        # after a small opening (which breaks the thin contact between skin and table) and set the rest
        # to air. Checked by eye on s0224: the bright vertical band at the frame edge was the table.
        from scipy.ndimage import binary_opening, label
        body = binary_opening(vol > -300.0, iterations=2)
        lab, n = label(body)
        if n > 1:
            sizes = np.bincount(lab.ravel()); sizes[0] = 0
            body = lab == int(sizes.argmax())
        vol = np.where(body, vol, -1000.0).astype(np.float32)
    masks = {}
    for name in ORDER:
        p = sub / "segmentations" / f"{name}.nii.gz"
        if p.exists():
            m, _, _ = load_lps(str(p))
            if m.any():
                masks[name] = m.astype(bool)
    print(f"{a.subject}: CT {vol.shape} (z,y,x) at {sp} mm, origin {np.round(org, 1)}; "
          f"{len(masks)} vertebral masks: {list(masks)[0]} .. {list(masks)[-1]}")
    if a.target not in masks:
        print(f"target {a.target} not present in this subject"); return 2

    # place the target vertebra where the real pose saw the pelvis: a translation of the volume, nothing else
    c_ts = centroid_mm(masks[a.target], org, sp)
    org_new = org - c_ts + G["c_df"]
    print(f"target {a.target} centroid {np.round(c_ts, 1)} -> pelvis landmark centroid {np.round(G['c_df'], 1)} "
          f"under pose {a.pose} (rot-180 {G['rot']})")

    import deepfluoro_render as DR
    d = dict(K=G["K"], ext=G["ext"], T=G["T"], nr=G["nr"], nc=G["nc"], vol=vol.astype(np.float32), org=org_new, sp=sp)
    trans, water, bone, hit, trunc = DR.raycast(d, down=a.down)
    M = G["ext"] @ np.linalg.inv(G["T"])
    # the calibrated frame: the nine device terms on the same water/bone maps, then a quantum draw
    import deepfluoro_calibrate as CAL
    import render_physics_drr as RP_
    RP = (RP_.ENERGIES.numpy(), RP_.SPECTRUM.numpy(), RP_.MU_WATER.numpy(), RP_.MU_BONE.numpy())
    calp = os.path.expanduser(a.calibration)
    theta = np.array(json.load(open(calp))["theta_median"], np.float64) if os.path.exists(calp) else None
    h, w = trans.shape
    yy, xx = np.mgrid[0:h, 0:w]; uu = (xx - w / 2) / (w / 2); vv = (yy - h / 2) / (h / 2)
    frame = dict(water=water, bone=bone, u=uu, v=vv, r2=uu * uu + vv * vv, rot=G["rot"])
    if theta is not None:
        # the quantum draw sits after scatter and before receptor blur, where the detector counts it
        atten_cal = CAL.forward_noisy(theta, frame, RP, a.photons, np.random.RandomState(0), hit=hit)
    else:
        atten_cal = -np.log(np.clip(trans, 1e-6, 1.0))
    boxes = {}
    for name, m in masks.items():
        b = project_mask(m, org_new, sp, M, G["K"], a.down, G["nr"], G["nc"])
        if b is not None:
            boxes[name] = b
    print(f"DRR {trans.shape}: hit {100 * hit.mean():.0f}%, truncated {100 * trunc.mean():.1f}%; "
          f"{len(boxes)} vertebrae land on the detector: {', '.join(boxes)}")

    stem = f"{a.subject}_{a.target}_{spec}-{pid}"
    # honour the rotation flag on the EMITTED frame and its boxes, so orientation matches the stored real ones
    img_out = atten_cal[::-1, ::-1] if G["rot"] else atten_cal
    if G["rot"]:
        H_, W_ = atten_cal.shape
        boxes = {k: dict(b, box=[W_ - 1 - b["box"][2], H_ - 1 - b["box"][3], W_ - 1 - b["box"][0], H_ - 1 - b["box"][1]])
                 for k, b in boxes.items()}
    np.savez_compressed(out / f"proj_{stem}.npz", drr_trans=trans.astype(np.float32), water_cm=water.astype(np.float32),
                        bone_cm=bone.astype(np.float32), hit=hit, trunc=trunc, rot=G["rot"], down=a.down,
                        px_mm=G["px_mm"] * a.down, calibrated=img_out.astype(np.float32),
                        photons=a.photons, table_stripped=(not a.no_strip_table))
    json.dump(dict(subject=a.subject, target=a.target, pose=a.pose, down=a.down, boxes=boxes,
                   sod_like_mm=float(np.linalg.norm((np.linalg.inv(M) @ np.r_[0, 0, 0, 1.0])[:3] - G["c_df"]))),
              open(out / f"proj_{stem}.json", "w"), indent=1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    logd = img_out
    hit_o = hit[::-1, ::-1] if G["rot"] else hit
    lo, hi = np.percentile(logd[hit_o], (1, 99)) if hit_o.any() else (0, 1)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(np.clip((logd - lo) / max(hi - lo, 1e-6), 0, 1), cmap="gray")
    for name, b in boxes.items():
        x0, y0, x1, y1 = b["box"]
        ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, lw=1.2,
                                   color="#ffd166" if name == a.target else "#06d6a0"))
        ax.text(x0, y0 - 2, name.replace("vertebrae_", ""), fontsize=7, color="#ffd166" if name == a.target else "#06d6a0")
    ax.set_title(f"{a.subject} under real pose {a.pose}, {a.target} at the pelvis point, "
                 f"{'calibrated + noise' if theta is not None else 'raw physics'}, "
                 f"{'table stripped' if not a.no_strip_table else 'table kept'}; truncated {100 * trunc.mean():.1f}%",
                 fontsize=8)
    ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); png = out / f"proj_{stem}.png"; fig.savefig(png, dpi=120)
    print("wrote", png)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
