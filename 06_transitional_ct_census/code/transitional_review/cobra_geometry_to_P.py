#!/usr/bin/env python
# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/cobra_geometry_to_P.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""cobra_geometry_to_P.py -- one COBRA projection's RTK geometry as the same P = K [R | t] form pose_to_viewer.py uses.

PURPOSE. COBRA2026 (kV cone-beam sweeps with an RTK geometry.xml) is the other paired corpus of the review tree. RTK
stores, per projection, a 3x4 matrix M mapping RTK-world millimetres (isocentre at the origin, rotation axis y) to
detector millimetres, homogeneous. The masks live on ct_def.mha. This tool composes M with the projection image's
own pixel grid and the CT-to-RTK world map, decomposes the result into a pinhole K [R | t] in the camera convention
of tools/drr_register.py, checks it, and writes it as (a) the OpenCV-convention P for ImFusion and (b) a pose JSON in
the shape of a C-ArmLSpine pose, so pose_to_viewer.export_view can place the projection frame and a DRR the same way.

THE MAPPING (tools/cobra_pairs.py camera_from_matrix, restated):
    P_pix = A_pix . M . W
    A_pix = [[1/sx, 0, -ox/sx + 0.5], [0, 1/sy, -oy/sy + 0.5], [0, 0, 1]]      detector mm -> pixel, raycaster centres
            (ox, oy = the projections.mha Offset; sx, sy = its ElementSpacing; the + 0.5 moves ITK's pixel-centre-
            at-index to the raycaster's pixel (c, r) centred at (c + 0.5, r + 0.5))
    W     = [[Pi, -Pi . iso], [0, 1]]   CT physical LPS mm (ct_def.mha as SimpleITK reads it) -> RTK world;
            Pi for Elekta XVI = [[0, 1, 0], [0, 0, -1], [1, 0, 0]] with iso = 0 (settled by edges in
            drr_register.selftest_cobra); the Varian OBI map is NOT settled here -- pass --pi for it or refuse.
    RQ-decompose P_pix[:, :3] = K R with K's diagonal made positive (a reflection carried in K, R kept proper),
    t = K^-1 P_pix[:, 3], K /= K[2, 2].  Then pixel = K (R p_ct + t) / z, exactly pose_to_viewer's camera.
Detector pitch for the plane files = sx (0.8 mm on A004); its plane distance = |fx| * sx = SDD (1536 mm) by
construction, because here K was built from the true pitch.

INPUTS   geometry.xml (RTK v3), the projection index, and the projection image header (--mha projections.mha, text
         header only, or --offset OX OY --spacing SX SY); optional --pi / --iso.
OUTPUTS  <out>/<case>_p<idx>_P.txt (OpenCV convention, 3 rows u v w), <out>/<case>_p<idx>_pose.json (K, R, t, sid =
         SDD, sod = SID, px_mm = sx, gantry angle, checks, sha256 of the inputs).
         --export --ct ct_def.mha additionally calls pose_to_viewer.export_view with the frame read from
         projections.mha (tools/cobra_pairs.read_mha) -- untested off the grid.

CHECKS (self-test fails on any): K [R | t] reproduces P_pix up to scale (< 1e-9 relative); R is a proper rotation;
the source -R^T t lies SourceToIsocenterDistance (+- 0.5 %) from the RTK isocentre; |fx| is SDD / sx within 1 %;
when tools/cobra_pairs is importable its camera_from_matrix agrees with the decomposition here (< 1e-9).

COMMANDS
  python tools/transitional_review/cobra_geometry_to_P.py --geometry geometry.xml --index 0 --offset -201.2 -201.2 \
      --spacing 0.8 0.8 --case A004 --out OUT
  python tools/transitional_review/cobra_geometry_to_P.py --selftest --samples DIR     # DIR/geometry.xml = A004's
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(HERE))

PI_ELEKTA = np.array([[0, 1, 0], [0, 0, -1], [1, 0, 0]], float)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def read_geometry(path):
    """(list of 3x4 matrices, gantry angles, SourceToIsocenterDistance, SourceToDetectorDistance)."""
    txt = open(path, encoding="latin-1").read()
    mats = [np.array([float(x) for x in m.group(1).split()], float).reshape(3, 4) for m in re.finditer(r"<Matrix>(.*?)</Matrix>", txt, re.S)]
    angles = [float(x) for x in re.findall(r"<GantryAngle>(.*?)</GantryAngle>", txt)]
    sid = float(re.search(r"<SourceToIsocenterDistance>(.*?)</SourceToIsocenterDistance>", txt).group(1))
    sdd = float(re.search(r"<SourceToDetectorDistance>(.*?)</SourceToDetectorDistance>", txt).group(1))
    return mats, angles, sid, sdd


def read_mha_header(path):
    """The text header of a MetaImage: Offset, ElementSpacing, DimSize (no pixel data is read)."""
    hdr = {}
    with open(path, "rb") as fh:
        for _ in range(64):
            line = fh.readline().decode("latin-1")
            if "=" not in line:
                break
            k, v = [s.strip() for s in line.split("=", 1)]
            hdr[k] = v
            if k == "ElementDataFile":
                break
    off = [float(x) for x in hdr["Offset"].split()]; sp = [float(x) for x in hdr["ElementSpacing"].split()]
    dims = [int(x) for x in hdr["DimSize"].split()]
    return dict(offset=off, spacing=sp, dims=dims)


def decompose(P):
    """K, R, t from a 3x4 pixel projection matrix: the RQ of tools/cobra_pairs.camera_from_matrix."""
    from scipy.linalg import rq
    K, R = rq(P[:, :3])
    S = np.diag(np.sign(np.diag(K)))
    K = K @ S; R = S @ R
    if np.linalg.det(R) < 0:
        K = -K; R = -R
    t = np.linalg.solve(K, P[:, 3])
    K = K / K[2, 2]
    return K, R, t


def projection_pose(geometry_xml, index, ox, oy, sx, sy, Pi=PI_ELEKTA, iso=(0.0, 0.0, 0.0), case="cobra"):
    mats, angles, sid, sdd = read_geometry(geometry_xml)
    if not (0 <= index < len(mats)):
        raise IndexError(f"projection {index} of {len(mats)}")
    M = mats[index]
    A = np.array([[1.0 / sx, 0.0, -ox / sx + 0.5], [0.0, 1.0 / sy, -oy / sy + 0.5], [0.0, 0.0, 1.0]])
    W = np.eye(4); W[:3, :3] = Pi; W[:3, 3] = -Pi @ np.asarray(iso, float)
    P = A @ M @ W
    K, R, t = decompose(P)
    Pr = K @ np.c_[R, t]
    rel = float(np.abs(Pr / Pr[2, 3] - P / P[2, 3]).max() / max(np.abs(P / P[2, 3]).max(), 1e-12))
    src_ct = -R.T @ t
    src_rtk = Pi @ (src_ct - np.asarray(iso, float))
    checks = dict(P_reproduced_rel_err=rel, R_det=float(np.linalg.det(R)), source_to_iso_mm=float(np.linalg.norm(src_rtk)),
                  source_to_iso_expected_mm=sid, fx_px=float(abs(K[0, 0])), fx_expected_px=sdd / sx, fx_rel_err=float(abs(abs(K[0, 0]) - sdd / sx) / (sdd / sx)),
                  cross_check_cobra_pairs=None)
    try:
        import cobra_pairs as CP
        K2, ext = CP.camera_from_matrix(M @ W, ox, oy, sx, sy)
        checks["cross_check_cobra_pairs"] = float(max(np.abs(np.array(K2) - K).max(), np.abs(ext[:3, :3] - R).max(), np.abs(ext[:3, 3] - t).max()))
    except Exception as e:  # noqa: BLE001
        checks["cross_check_cobra_pairs"] = f"unavailable: {type(e).__name__}"
    ok = rel < 1e-9 and abs(checks["R_det"] - 1) < 1e-9 and abs(checks["source_to_iso_mm"] - sid) / sid < 0.005 and checks["fx_rel_err"] < 0.01 \
        and (not isinstance(checks["cross_check_cobra_pairs"], float) or checks["cross_check_cobra_pairs"] < 1e-9)
    checks["pass"] = bool(ok)
    Tshift = np.array([[1, 0, -0.5], [0, 1, -0.5], [0, 0, 1.0]])
    pose = dict(K=K.tolist(), R=R.tolist(), t=t.tolist(), sid=sdd, sod=sid, px_mm=float(sx), case=case, view=f"p{index}", tag="",
                frame_key=f"rtk:{index}", gantry_deg=angles[index] if index < len(angles) else None, rtk_matrix=M.tolist(), world_map=W.tolist(),
                pixel_map=A.tolist(), P_raycaster=P.tolist(), P_opencv=(Tshift @ Pr).tolist(), checks=checks,
                convention="pixel = K (R p_ct + t) / z with pixel (c, r) centred at (c+0.5, r+0.5); p_ct in ct_def.mha's LPS mm; P_opencv shifts by -0.5",
                inputs_sha256={"geometry.xml": sha256_file(geometry_xml)})
    return pose


def write_outputs(pose, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    stem = f"{pose['case']}_{pose['view']}"
    with open(os.path.join(out_dir, stem + "_P.txt"), "w", newline="\n") as fh:
        for row in pose["P_opencv"]:
            fh.write(" ".join(f"{v:.10f}" for v in row) + "\n")
    json.dump(pose, open(os.path.join(out_dir, stem + "_pose.json"), "w"), indent=1)
    return os.path.join(out_dir, stem + "_pose.json")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--geometry"); ap.add_argument("--index", type=int, default=0); ap.add_argument("--case", default="cobra")
    ap.add_argument("--mha", default=None, help="projections.mha: its text header gives the offset and spacing")
    ap.add_argument("--offset", type=float, nargs=2, default=None); ap.add_argument("--spacing", type=float, nargs=2, default=None)
    ap.add_argument("--pi", default="elekta", help="'elekta' or 9 numbers row-major")
    ap.add_argument("--iso", type=float, nargs=3, default=(0.0, 0.0, 0.0))
    ap.add_argument("--out", default=None)
    ap.add_argument("--export", action="store_true", help="also write the plane files through pose_to_viewer (needs --ct, --mha, --mask)")
    ap.add_argument("--ct", default=None); ap.add_argument("--mask", default=None); ap.add_argument("--ctd", default=None)
    ap.add_argument("--selftest", action="store_true"); ap.add_argument("--samples", default=os.environ.get("TR_SAMPLES", ""))
    a = ap.parse_args()
    if a.pi == "elekta":
        Pi = PI_ELEKTA
    else:
        Pi = np.array([float(x) for x in a.pi.split()], float).reshape(3, 3)
    if a.selftest:
        g = os.path.join(a.samples, "geometry.xml")
        if not os.path.exists(g):
            print("selftest: no geometry.xml in", a.samples); return 2
        fails = []
        # A004's projections.mha header (read on the grid 2026-09-27): Offset -201.2 -201.2 0, ElementSpacing 0.8 0.8 1, DimSize 504 504 378
        for idx in (0, 189, 377):
            try:
                pose = projection_pose(g, idx, -201.2, -201.2, 0.8, 0.8, Pi, (0, 0, 0), case="A004")
                c = pose["checks"]
                print(f"A004 p{idx} gantry {pose['gantry_deg']:.2f}: P rel err {c['P_reproduced_rel_err']:.1e}, det R {c['R_det']:.6f}, "
                      f"source-iso {c['source_to_iso_mm']:.2f} mm (SID {c['source_to_iso_expected_mm']:.0f}), fx {c['fx_px']:.2f} px "
                      f"(SDD/sx {c['fx_expected_px']:.2f}), cobra_pairs cross-check {c['cross_check_cobra_pairs']} -> {'PASS' if c['pass'] else 'FAIL'}")
                if not c["pass"]:
                    fails.append(f"p{idx}: {c}")
                if a.out:
                    write_outputs(pose, a.out)
            except Exception as e:  # noqa: BLE001
                fails.append(f"p{idx}: {type(e).__name__}: {e}")
        print("SELFTEST", "PASS" if not fails else "FAIL")
        for f in fails:
            print("  -", f)
        return 0 if not fails else 1
    if not a.geometry or not a.out:
        ap.error("--geometry and --out are required")
    if a.mha:
        h = read_mha_header(a.mha); ox, oy = h["offset"][:2]; sx, sy = h["spacing"][:2]
    elif a.offset and a.spacing:
        (ox, oy), (sx, sy) = a.offset, a.spacing
    else:
        ap.error("give --mha or both --offset and --spacing")
    pose = projection_pose(a.geometry, a.index, ox, oy, sx, sy, Pi, tuple(a.iso), case=a.case)
    pj = write_outputs(pose, a.out)
    c = pose["checks"]
    print(f"{a.case} p{a.index}: {'PASS' if c['pass'] else 'FAIL'} P rel err {c['P_reproduced_rel_err']:.1e} source-iso {c['source_to_iso_mm']:.2f} mm fx {c['fx_px']:.2f} px -> {pj}")
    if a.export:
        if not (a.ct and a.mha and (a.mask or True)):
            ap.error("--export needs --ct and --mha")
        import cobra_pairs as CP
        import pose_to_viewer as PV
        frames, _ = CP.read_mha(a.mha, frames=[a.index])
        img = np.asarray(frames[0], np.float64)
        cents, guard, _ = PV.spineps_centroids(a.mask, a.ctd) if a.mask else ({}, "none", None)
        # COBRA projections are LINEAR detector signal: the same -log map gives an attenuation image
        row, side = PV.export_view(pose, pj, img, dict(rows=img.shape[0], cols=img.shape[1], angle=pose["gantry_deg"], sid=pose["sid"], sod=pose["sod"], kvp=None),
                                   a.mha, a.ct, cents, f"spineps:{guard}", os.path.join(a.out, a.case), pitch=sx, reproduce_score=False)
        print("export:", row["status"], "reproj", row["reproj_tfm_max_px"], row["reproj_nifti_max_px"])
    return 0 if c["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
