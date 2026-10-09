#!/usr/bin/env python
# copied into spine-program/06_transitional_ct_census on 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class) tools/transitional_review/pose_to_viewer.py; UNTRACKED in the working tree on 2026-10-08 (commit it after its self-tests: OPEN_QUESTIONS F12, C21). The banned word, where it occurred, is rewritten as origin.
"""pose_to_viewer.py -- a registered C-ArmLSpine spot frame as viewer files, with the test that they agree.

PURPOSE. The transitional-vertebra review tree shows a reviewer the CBCT, its masks and the two spot frames of the
same person in one scene. A pose JSON from tools/carmlspine_pose.py holds K, R, t for one frame; this tool turns it
into files 3D Slicer and ImFusion can place, and proves with a reprojection test that the three descriptions of the
same camera (the projection matrix, the NIfTI placement, the ITK transform) put a point on the same pixel.

INPUTS (explicit paths, or --case on the grid)
  --pose   <case>_<view>[_ref|_ref2].json  from carmlspine_pose.py: K (3x3, pixels of the 2048 frame), R (3x3,
           world LPS -> camera), t (mm), sid, sod, px_mm (the pitch the pose was FIT at), frame_key or frame.
  --cbct   the case's CBCT NIfTI (nifti/<case>_cbct.nii.gz; LPS, 394^3 x 0.5 mm). Read only, never written.
  --mask   SPINEPS/VERIDAH instance mask <case>_seg-vert_msk.nii.gz (VerSe-coded post-fix: L1-L5 20-24, L6 25,
           sacrum 26, T13 28); guarded by tools/spineps_ids.assert_verse_monotonic against the ctd (--ctd).
           --ts-dir <dir with vertebrae_*.nii.gz, sacrum.nii.gz> is the TotalSegmentator alternative.
  --frame  the spot-frame DICOM(s); matched to a pose by frame_key (sha1 of the basename) or the old `frame` field.
  --meta   optional realxray meta JSON(s) (RS/data/realxray/carmlspine/meta/<case>_<view>.json) with the projected
           boxes at 1024 px; the test reports which projected centroids fall inside them.

OUTPUTS, per view, under --out/<case>/
  xr_<view>.nii.gz      the radiograph (bone-bright attenuation, -log of the stored value as the registration saw it;
                        --xr-values raw keeps the stored uint16) as a single-slice volume whose in-plane spacing is
                        the TRUE pitch (--pitch, default 0.150 mm = 307.2 mm / 2048), with origin and direction
                        placing the detector plane in the CBCT's LPS frame (see PITCH below for where).
  xr_<view>.tfm         an ITK affine transform, LPS, "from parent": world LPS mm -> detector-local mm (x along the
                        columns, y along the rows, both zero at the outer corner of pixel (0,0); z along
                        e_col x e_row, zero on the plane). 3D Slicer loads it as a transform node whose
                        "to parent" is the inverse (local -> world, shown in RAS); the SlicerIGT Volume Reslice
                        Driver driven by that node, mode Axial, reslices along the detector plane with x/y along
                        the columns/rows. The convention is proven by the reprojection test (CHECKS).
  xr_<view>_P.txt       the 3x4 projection matrix, world LPS mm -> pixel, three rows (u = column, v = row, w),
                        space-separated, OpenCV pixel convention (pixel centres at integers). The registration's own
                        convention has pixel (c, r) centred at (c+0.5, r+0.5); P_opencv = P_raycaster shifted by
                        -0.5 px in u and v. Both matrices are in the sidecar.
  drr_<view>.nii.gz     a DRR rendered at the pose (own numpy ray-marcher, the camera convention of
                        tools/drr_register.py: ray = R^T K^-1 [u, v, 1], source = -R^T t, pixel (c+0.5, r+0.5)),
                        on the same plane at --drr-down (default 4 -> 512 px, 0.6 mm). --drr-backend torch uses
                        drr_register.Renderer instead when torch is importable.
  xr_<view>.json        the sidecar: every geometric quantity, the conventions in words, the checks, the
                        projected centroids and the box report.
  pose_to_viewer_rows.tsv   one row per view (schema: ROW_COLUMNS below) carrying prereg_sha256, prereg_status,
                        git_sha, tool, tool_version, utc and the sha256 of every input file read.

PITCH (the correction, stated so nothing is silent). Every pose on disk under data/carmlspine/pose/ was fit with
px_mm = 300 / 2048 = 0.146484375 mm (a nominal "30 cm" panel); tools/carmlspine_io.DET_MM now says 307.2 mm
(iRay Jupi1212X, 2048 x 150 um), i.e. 0.150 mm, and the poses are to be refit at 0.150 (refit_carmlspine_poses.sh,
output pose_150/). Until then this tool does NOT rescale K: K [R | t] is what was fit to the frame and is written
as it is. The detector plane is placed where a pixel grid of the true pitch reproduces that projection exactly:
at distance D = |fx| * pitch from the source along the optical axis (the pinhole makes this the only distance at
which the plane's pixel step equals the pitch). For the old poses D = 7782.4 * 0.150 = 1167.36 mm, 27.36 mm beyond
the header SID of 1140 mm; the row carries plane_distance_mm, sid_header_mm, plane_minus_sid_mm and
needs_refit = true. For a refit pose (fx = 1140 / 0.150 = 7600 px) D = 1140 mm and the flag clears.
--k-policy rescale_to_sid instead scales fx, fy to SID / pitch and puts the plane at SID; that changes the
projection by 2.4 % about the principal point (up to 24 px at the frame edge), so the DRR no longer overlays the
frame; the row then says k_rescaled = true. It exists to make the alternative visible, not as a default.

CHECKS (the self-test fails on any of them)
  1. every SPINEPS instance centroid (world LPS, through the mask's own affine) projected by K [R | t] to (u, v);
  2. the same centroid through the .tfm AS READ BACK by SimpleITK (world -> detector-local), the source likewise,
     the ray intersected with the local plane z = 0, divided by the pitch: must agree with 1 within 0.5 px;
  3. the same centroid through the NIfTI's affine AS READ BACK by nibabel (RAS -> LPS): the ray from the source
     intersected with the written plane, expressed in voxel units: within 0.5 px;
  4. the OpenCV matrix reproduces (u - 0.5, v - 0.5);
  5. the registration's own objective, recomputed on its 409-px working grid from this tool's DRR at this pose,
     reproduces the JSON's edge_ncc within 0.02 (an outside check that K, R, t were read the way they were fit);
  6. where torch is importable, drr_register.Renderer at the same pose correlates with the numpy DRR > 0.999;
  7. where a meta JSON exists, the projected centroids are reported against its boxes (1024-px frame, quarter
     turns as tools/carmlspine_labels.rot_pts); complete, fully visible boxes must contain their centroid when the
     meta was built from the same pose tag, otherwise the box report is informational;
  8. the ITK meaning of the .tfm, done the way 3D Slicer uses a transform file: the radiograph rebuilt in the
     detector-LOCAL frame (identity direction) and resampled onto the placed volume's grid with the transform AS
     READ FROM THE FILE (ITK resampling semantics, output point -> transform -> input point) must reproduce the
     placed volume voxel for voxel (max difference 0).
  Also asserted: the pre-registration reads as "draft" while its freeze block is blank.

Self-test result on case42 (2026-09-27): reprojection errors 1e-4 px on every route; edge NCC reproduced within
0.004 of the JSONs (AP 0.372 vs 0.375, LAT _ref2 0.188 vs 0.189, LAT _ref 0.157 vs 0.158); torch renderer
correlation 0.9999; boxes 6/6 inside for AP _ref and LAT _ref2, 3/6 for LAT _ref (a different pose than the boxes:
the two lateral poses on disk put the L2 centroid 36 px apart at full resolution).

COMMANDS
  python tools/transitional_review/pose_to_viewer.py --selftest [--samples DIR]
  python tools/transitional_review/pose_to_viewer.py --pose P.json [--pose ...] --cbct C.nii.gz --mask M.nii.gz \
      --ctd M_ctd.json --frame F.dcm [--frame ...] [--meta meta.json ...] --out OUT [--pitch 0.150] [--suffix-tag]
  python tools/transitional_review/pose_to_viewer.py --case case42 --out OUT [--rs ROOT] [--pose-dir DIR]   # GRID
Two poses of one view in one run (e.g. LAT _ref and _ref2) need --suffix-tag (files xr_LAT_ref.*, xr_LAT_ref2.*);
without it the second is refused rather than overwriting the first.

GRID. --case resolves RS/data/carmlspine/{pose_150 (or --pose-dir), nifti, spineps, unpacked/C-ArmLSpine/<case>}
and RS/data/realxray/carmlspine/meta; the per-view pose tag is the one the meta used (pose.refined), else _ref2
for LAT/OBL when present, else _ref. Frames are found with tools/carmlspine_io.spot_frames (Modality XA, 2048
rows) and matched by frame_key; the frame FILE NAME is never written to an output (a third of the release names
frames by UID). It refuses when the pose directory does not exist: the 0.1465-mm poses are read only when
--pose-dir names them.

HOUSE RULES honoured here: the CBCT and masks are never written; the new single-slice volumes are built in LPS
with SimpleITK and never reoriented; SPINEPS masks are never passed through ostk.labels.labels_for (they have
their own map); failures are rows with status "failed: ..." and a non-zero exit.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys
import traceback
from pathlib import Path

import numpy as np

TOOL = "pose_to_viewer"
TOOL_VERSION = "1"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TOOLS = REPO / "tools"
sys.path.insert(0, str(TOOLS))

RS = "/rs/rs_grp_oschome/go2432"
DEFAULT_PREREG = REPO / "docs" / "ruleclass" / "PREREG_rules.md"
PITCH_TRUE_MM = 307.2 / 2048.0          # 0.150 mm: tools/carmlspine_io.DET_MM over 2048 columns
PITCH_FIT_MM = 300.0 / 2048.0           # 0.146484375 mm: what every pose under data/carmlspine/pose was fit with
REPROJ_TOL_PX = 0.5
SLAB_MM = 1.0                            # thickness given to the single-slice volumes (display only)
WORK_GRID = 384                          # carmlspine_pose.register_frame(work=384) -> f = round(2048/384) = 5

VERSE_NAME = {19: "T12", 20: "L1", 21: "L2", 22: "L3", 23: "L4", 24: "L5", 25: "L6", 26: "sacrum", 27: "coccyx",
              28: "T13", 18: "T11", 17: "T10"}
for _i in range(1, 8):
    VERSE_NAME[_i] = f"C{_i}"
for _i in range(8, 20):
    VERSE_NAME.setdefault(_i, f"T{_i - 7}")

ROW_COLUMNS = [
    "status", "case", "view", "pose_tag", "frame_key", "utc", "tool", "tool_version", "git_sha", "git_dirty",
    "prereg_path", "prereg_sha256", "prereg_status",
    "pitch_fit_mm", "pitch_true_mm", "det_mm", "k_policy", "k_rescaled", "needs_refit",
    "fx_px", "fy_px", "cx_px", "cy_px", "sid_header_mm", "sod_header_mm", "plane_distance_mm", "plane_minus_sid_mm",
    "cbct_centre_depth_mm", "source_lps_mm", "normal_points_toward_source",
    "centroid_source", "n_centroids", "reproj_tfm_max_px", "reproj_nifti_max_px", "reproj_opencv_max_px", "tfm_resample_max_diff", "reproj_pass",
    "edge_ncc_json", "edge_ncc_reproduced", "int_ncc_json", "int_ncc_reproduced", "renderer_corr_torch",
    "drr_down", "drr_steps", "drr_backend", "drr_frame_ncc",
    "boxes_meta", "boxes_pose_tag", "boxes_pose_tag_match", "n_boxed", "n_in_box", "n_in_box_required", "n_in_box_required_hit",
    "in_box_detail", "inputs_sha256", "outputs", "reason",
]


# ------------------------------------------------------------------------------------------------ small utilities
def sha256_file(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def git_state(repo=REPO):
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(repo), capture_output=True, text=True, timeout=30)
        dirty = subprocess.run(["git", "status", "--porcelain"], cwd=str(repo), capture_output=True, text=True, timeout=60)
        if sha.returncode != 0:
            return "unknown", None
        return sha.stdout.strip(), bool(dirty.stdout.strip()) if dirty.returncode == 0 else None
    except Exception:  # noqa: BLE001
        return "unknown", None


def prereg_state(path):
    """(sha256, status) of the pre-registration as read. 'draft' until the freeze block's 'frozen by' line is filled."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"pre-registration not found: {path}")
    sha = sha256_file(path)
    txt = open(path, encoding="utf-8", errors="replace").read()
    # "frozen" only when the freeze block carries a written sha256 (64 hex digits); the blank template line
    # "frozen by: ____ (Greg)" is a placeholder, not a signature (the first version of this test read it as one)
    m = re.search(r"sha256 of this file:\s*([0-9a-fA-F]{64})\b", txt)
    return sha, ("frozen" if m else "draft")


def frame_key_of(path):
    return hashlib.sha1(os.path.basename(path).encode()).hexdigest()[:12]


def utc_now():
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------------------------------------ camera geometry
def camera_from_pose(pose):
    K = np.array(pose["K"], float); R = np.array(pose["R"], float); t = np.array(pose["t"], float).reshape(3)
    if K.shape != (3, 3) or R.shape != (3, 3):
        raise ValueError("pose K and R must be 3x3")
    if abs(K[0, 1]) > 1e-9 or abs(K[2, 0]) > 1e-12 or abs(K[2, 1]) > 1e-12 or abs(K[2, 2] - 1) > 1e-12:
        raise ValueError(f"K is not a zero-skew pinhole with K[2,2] = 1: {K.tolist()}")
    if abs(abs(np.linalg.det(R)) - 1) > 1e-6 or np.abs(R @ R.T - np.eye(3)).max() > 1e-5:
        raise ValueError("R is not orthonormal")
    if np.linalg.det(R) < 0:
        raise ValueError("R is a reflection; the registration keeps R proper and carries a mirror in K")
    return K, R, t


def project(K, R, t, pts):
    """Pixels (u, v) in the raycaster convention (pixel (c, r) centred at (c + 0.5, r + 0.5)) of world LPS points."""
    pts = np.atleast_2d(np.asarray(pts, float))
    c = pts @ R.T + t
    uv = c @ K.T
    return uv[:, :2] / uv[:, 2:3], c[:, 2]


def plane_frame(K, R, t, pitch):
    """The detector plane implied by K [R | t] and the true pitch.

    Distance D = |fx| * pitch from the source along the optical axis R^T e_z: the one distance at which the plane's
    pixel step equals the pitch. Returns the world corner of pixel (0,0) (edge, not centre), unit column and row
    directions, the plane normal e_col x e_row (always right-handed), the steps, the source, and D."""
    fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
    D = abs(fx) * pitch
    Kinv = np.linalg.inv(K)
    src = -R.T @ t
    axis = R.T @ np.array([0, 0, 1.0])
    e_col = np.sign(fx) * (R.T @ np.array([1.0, 0, 0]))
    e_row = np.sign(fy) * (R.T @ np.array([0, 1.0, 0]))
    corner = src + D * (R.T @ (Kinv @ np.array([0.0, 0.0, 1.0])))
    n = np.cross(e_col, e_row); n /= np.linalg.norm(n)
    return dict(corner=corner, e_col=e_col, e_row=e_row, normal=n, distance=float(D), source=src, beam_axis=axis,
                step_col=float(D / abs(fx)), step_row=float(D / abs(fy)),
                normal_points_toward_source=bool(np.dot(n, axis) < 0))


def plane_pixel_from_local(p_local, s_local, pitch_col, pitch_row):
    """(u, v) where the ray from s_local through p_local crosses the local plane z = 0, in pixels (edge coords)."""
    d = p_local - s_local
    if abs(d[2]) < 1e-12:
        return np.array([np.nan, np.nan])
    lam = -s_local[2] / d[2]
    X = s_local + lam * d
    return np.array([X[0] / pitch_col, X[1] / pitch_row])


# ------------------------------------------------------------------------------------------------ volumes and frames
def load_mu(path):
    """(mu (z,y,x) float32 1/mm, affine index->world LPS 4x4, sitk image) exactly as tools/drr_register.load_volume."""
    import SimpleITK as sitk
    im = sitk.ReadImage(path)
    hu = sitk.GetArrayFromImage(im).astype(np.float32)
    mu = np.clip((hu + 1000.0) / 1000.0, 0.0, None) * 0.02
    D = np.array(im.GetDirection()).reshape(3, 3); sp = np.array(im.GetSpacing()); org = np.array(im.GetOrigin())
    A = np.eye(4); A[:3, :3] = D @ np.diag(sp); A[:3, 3] = org
    return mu, A, im


def stored_to_atten(img):
    """tools/carmlspine_pose.stored_to_atten: bone bright, -log of the transmission-like stored value."""
    x = img.astype(np.float64)
    lo = np.percentile(x, 0.1)
    return -np.log(np.clip(x - lo + 1.0, 1.0, None) / (np.percentile(x, 99.9) - lo + 1.0))


def read_frame(path):
    import pydicom
    ds = pydicom.dcmread(path)
    img = ds.pixel_array
    if img.ndim != 2:
        raise ValueError("a spot frame must be a single 2-D image")
    if str(getattr(ds, "PhotometricInterpretation", "")) == "MONOCHROME1":
        img = img.max() - img
    return img, dict(rows=int(ds.Rows), cols=int(ds.Columns), angle=float(getattr(ds, "PositionerPrimaryAngle", 0) or 0),
                     sid=float(getattr(ds, "DistanceSourceToDetector", 0) or 0), sod=float(getattr(ds, "DistanceSourceToPatient", 0) or 0),
                     kvp=float(getattr(ds, "KVP", 0) or 0))


def block_mean(x, f):
    H, W = x.shape[0] // f, x.shape[1] // f
    return x[: H * f, : W * f].reshape(H, f, W, f).mean((1, 3))


# ------------------------------------------------------------------------------------------------ centroids
def spineps_centroids(mask_path, ctd_path=None):
    """{id: (name, world LPS centroid, voxels)} of the instance ids < 100 of a SPINEPS/VERIDAH mask, through the
    mask's own affine; guarded by tools/spineps_ids.assert_verse_monotonic (raises when the ids are not names)."""
    import SimpleITK as sitk
    guard = "spineps_ids.assert_verse_monotonic"
    try:
        import spineps_ids as SI
        SI.assert_verse_monotonic(mask_path, ctd_path if ctd_path else "auto", require_ctd=bool(ctd_path), quiet=True,
                                  allow_skipped_names=True, what=os.path.basename(mask_path))
    except ImportError:
        guard = "own_minimal(ids in 1..28 or >= 100)"
    im = sitk.ReadImage(mask_path)
    arr = sitk.GetArrayFromImage(im)                       # (z, y, x)
    D = np.array(im.GetDirection()).reshape(3, 3); sp = np.array(im.GetSpacing()); org = np.array(im.GetOrigin())
    A = np.eye(4); A[:3, :3] = D @ np.diag(sp); A[:3, 3] = org
    ids = [int(i) for i in np.unique(arr) if 0 < i < 100]
    if guard.startswith("own") and any(not (1 <= i <= 28) for i in ids):
        raise RuntimeError(f"mask ids {ids} are outside the VerSe alphabet and spineps_ids is not importable")
    out = {}
    for i in ids:
        zyx = np.argwhere(arr == i)
        if len(zyx) < 50:
            continue
        ijk = zyx.mean(0)[::-1]
        w = A @ np.r_[ijk, 1.0]
        out[i] = (VERSE_NAME.get(i, str(i)), w[:3], int(len(zyx)))
    return out, guard, A


def ts_centroids(ts_dir):
    """{name: (name, world LPS centroid, voxels)} from per-structure TotalSegmentator files."""
    import SimpleITK as sitk
    out = {}
    for p in sorted(Path(ts_dir).glob("*.nii.gz")):
        nm = p.name[: -len(".nii.gz")]
        if not (nm.startswith("vertebrae_") or nm == "sacrum"):
            continue
        im = sitk.ReadImage(str(p)); arr = sitk.GetArrayFromImage(im)
        zyx = np.argwhere(arr > 0)
        if len(zyx) < 50:
            continue
        D = np.array(im.GetDirection()).reshape(3, 3); sp = np.array(im.GetSpacing()); org = np.array(im.GetOrigin())
        A = np.eye(4); A[:3, :3] = D @ np.diag(sp); A[:3, 3] = org
        w = A @ np.r_[zyx.mean(0)[::-1], 1.0]
        out[nm.replace("vertebrae_", "")] = (nm.replace("vertebrae_", ""), w[:3], int(len(zyx)))
    return out


# ------------------------------------------------------------------------------------------------ DRR
def render_numpy(mu, A, K, R, t, H, W, n_steps=192, chunk_rows=16):
    """Line integral of mu along R^T K^-1 [u, v, 1] rays from -R^T t, sampled like drr_register.Renderer: n_steps
    samples across the volume's bounding sphere about the ray's closest approach to the volume centre, trilinear,
    zero outside. (H x W) float32, 1/mm * mm."""
    from scipy.ndimage import map_coordinates
    Ainv = np.linalg.inv(A)
    Z, Y, X = mu.shape
    corners = np.array([[i, j, k, 1.0] for i in (0, X - 1) for j in (0, Y - 1) for k in (0, Z - 1)])
    wc = (A @ corners.T).T[:, :3]
    centre = wc.mean(0); radius = float(np.linalg.norm(wc - centre, axis=1).max())
    src = -R.T @ t
    Kinv = np.linalg.inv(K)
    s = np.linspace(-radius, radius, n_steps); step = float(2 * radius / (n_steps - 1))
    out = np.zeros((H, W), np.float32)
    u = np.arange(W, dtype=np.float64) + 0.5
    for r0 in range(0, H, chunk_rows):
        rows = np.arange(r0, min(H, r0 + chunk_rows), dtype=np.float64) + 0.5
        vv, uu = np.meshgrid(rows, u, indexing="ij")
        pix = np.stack([uu.ravel(), vv.ravel(), np.ones(uu.size)], 1)
        dw = (pix @ Kinv.T) @ R                                # R^T d for row vectors
        dw /= np.linalg.norm(dw, axis=1, keepdims=True)
        tc = ((centre - src)[None] * dw).sum(1, keepdims=True)
        P = src[None, None] + dw[:, None] * (tc + s[None])[..., None]          # (N, S, 3)
        idx = P.reshape(-1, 3) @ Ainv[:3, :3].T + Ainv[:3, 3]                 # (i, j, k) = (x, y, z)
        val = map_coordinates(mu, [idx[:, 2], idx[:, 1], idx[:, 0]], order=1, mode="constant", cval=0.0, prefilter=False)
        out[r0: r0 + len(rows)] = (val.reshape(len(pix), n_steps).sum(1) * step).reshape(len(rows), W)
    return out


def render_torch(mu, A, K, R, t, H, W, n_steps=192):
    """drr_register.Renderer on the CPU at the same pose (None if torch or the module is missing)."""
    try:
        import torch
        import drr_register as DRG
    except Exception:  # noqa: BLE001
        return None
    rend = DRG.Renderer(mu, A, "cpu", n_steps=n_steps)
    with torch.no_grad():
        d = rend.render(torch.tensor(K, dtype=torch.float32), torch.tensor(R, dtype=torch.float32),
                        torch.tensor(t, dtype=torch.float32), H, W)
    return d.numpy()


def registration_score(drr, att_full, f):
    """drr_register.register's objective at level 1 for a DRR on the (2048 // f)^2 working grid: signed Sobel
    gradient correlation (x and y) on lightly smoothed images inside the body mask with the border excluded, and
    the intensity NCC. Same constants as the registration (smooth sigma 1, r 3; Sobel / 8; border 8; body >
    5th percentile)."""
    from scipy.ndimage import convolve, correlate1d
    img = block_mean(att_full, f)
    H, W = img.shape
    drr = drr[:H, :W]

    def smooth(x):
        g = np.exp(-(np.arange(-3, 4) ** 2) / 2.0); g /= g.sum()
        return correlate1d(correlate1d(x, g, axis=1, mode="nearest"), g, axis=0, mode="nearest")

    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float) / 8

    def grad(x):
        # torch conv2d is a correlation; scipy.ndimage.correlate matches it, with replicate ('nearest') padding
        from scipy.ndimage import correlate
        return correlate(x, kx, mode="nearest"), correlate(x, kx.T, mode="nearest")

    body = img > np.quantile(img, 0.05)
    m = body.copy(); b = 8
    m[:b] = False; m[-b:] = False; m[:, :b] = False; m[:, -b:] = False

    def ncc(a, c):
        a = a[m] - a[m].mean(); c = c[m] - c[m].mean()
        return float((a * c).sum() / np.sqrt((a * a).sum() * (c * c).sum() + 1e-12))

    gxd, gyd = grad(smooth(drr.astype(np.float64))); gxr, gyr = grad(smooth(img))
    return 0.5 * (ncc(gxd, gxr) + ncc(gyd, gyr)), ncc(drr.astype(np.float64), img)


# ------------------------------------------------------------------------------------------------ writers
def write_plane_nifti(path, img2d, fr, down=1):
    """A single-slice volume on the detector plane: voxel (c, r, 0) centred at corner + (c+0.5) down step_col e_col
    + (r+0.5) down step_row e_row. Built in LPS with SimpleITK, which writes the NIfTI sform/qform itself."""
    import SimpleITK as sitk
    im = sitk.GetImageFromArray(np.ascontiguousarray(img2d)[None])       # numpy (z=1, rows, cols) -> index (c, r, 0)
    sc, sr = fr["step_col"] * down, fr["step_row"] * down
    im.SetSpacing((float(sc), float(sr), float(SLAB_MM)))
    im.SetOrigin(tuple(float(v) for v in fr["corner"] + 0.5 * sc * fr["e_col"] + 0.5 * sr * fr["e_row"]))
    im.SetDirection(tuple(float(v) for v in np.c_[fr["e_col"], fr["e_row"], fr["normal"]].ravel()))
    sitk.WriteImage(im, path, True)


def write_tfm(path, fr):
    """ITK affine, LPS, from parent: p_local = C^T p_world - C^T corner, C = [e_col e_row normal]."""
    import SimpleITK as sitk
    C = np.c_[fr["e_col"], fr["e_row"], fr["normal"]]
    Afp = C.T; bfp = -C.T @ fr["corner"]
    tf = sitk.AffineTransform(3)
    tf.SetMatrix([float(v) for v in Afp.ravel()]); tf.SetTranslation([float(v) for v in bfp]); tf.SetCenter((0.0, 0.0, 0.0))
    sitk.WriteTransform(tf, path)
    return Afp, bfp


def write_P(path, P):
    with open(path, "w", newline="\n") as fh:
        for row in P:
            fh.write(" ".join(f"{v:.10f}" for v in row) + "\n")


def read_tfm_as_affine(path):
    import SimpleITK as sitk
    tf = sitk.ReadTransform(path)
    try:
        tf = sitk.AffineTransform(tf)
    except Exception:  # noqa: BLE001
        pass
    M = np.array(tf.GetMatrix(), float).reshape(3, 3); c = np.array(tf.GetCenter(), float); b = np.array(tf.GetTranslation(), float)
    return M, M @ (-c) + c + b            # p' = M (p - c) + c + b


# ------------------------------------------------------------------------------------------------ boxes
def rot_pts(uv, k, S):
    """tools/carmlspine_labels.rot_pts: points under np.rot90(img, k): (x, y) -> (y, S-1-x) per quarter turn."""
    uv = np.array(uv, float, copy=True)
    for _ in range(k % 4):
        uv = np.c_[uv[:, 1], S - 1 - uv[:, 0]]
    return uv


def box_report(meta, uv_full, names, cols_full, pose_tag):
    """Which projected centroids fall inside the meta's boxes (matched by level_spineps, else level_ts)."""
    S = int(meta.get("size", 1024)); k = int(meta.get("quarter_turns", 0)); sc = S / float(cols_full)
    uv = rot_pts(uv_full * sc, k, S)
    boxes = meta.get("boxes", [])
    tag = (meta.get("pose") or {}).get("refined")
    same = (tag == pose_tag)
    rows = []
    for (nm, p) in zip(names, uv):
        cands = [b for b in boxes if (b.get("level_spineps") == nm) or (b.get("level_ts") == nm and b.get("level_spineps") is None)]
        if not cands:
            cands = [b for b in boxes if b.get("level_ts") == nm and nm not in {b2.get("level_spineps") for b2 in boxes}]
        if not cands:
            rows.append(dict(name=nm, u=float(p[0]), v=float(p[1]), box=None, inside=None, required=False)); continue
        b = cands[0]; x0, y0, x1, y1 = b["box"]
        inside = bool(x0 <= p[0] <= x1 and y0 <= p[1] <= y1)
        dx = max(x0 - p[0], 0, p[0] - x1); dy = max(y0 - p[1], 0, p[1] - y1)
        required = bool(same and b.get("complete") and float(b.get("visible_frac", 0)) >= 0.99)
        rows.append(dict(name=nm, u=round(float(p[0]), 1), v=round(float(p[1]), 1), box=[x0, y0, x1, y1], level_ts=b.get("level_ts"),
                         level_spineps=b.get("level_spineps"), inside=inside, outside_px=round(float(np.hypot(dx, dy)), 1),
                         required=required))
    return dict(size=S, quarter_turns=k, boxes_pose_tag=tag, same_pose_tag=same, rows=rows,
                n_boxed=sum(r["box"] is not None for r in rows), n_in_box=sum(bool(r["inside"]) for r in rows),
                n_required=sum(r["required"] for r in rows), n_required_hit=sum(r["required"] and r["inside"] for r in rows))


# ------------------------------------------------------------------------------------------------ one view
def export_view(pose, pose_path, frame_img, frame_hdr, frame_path, cbct_path, cents, cent_source, out_dir, *,
                pitch=PITCH_TRUE_MM, k_policy="as_fit", drr_down=4, drr_steps=192, drr_backend="numpy",
                xr_values="atten", meta=None, meta_path=None, reproduce_score=True, torch_check=True,
                extra_inputs=None, mu_cache=None, stem=None):
    """Write the five files of one view (named xr_<stem>.*, stem = the view unless given) and return (row, sidecar)."""
    import nibabel as nib
    import SimpleITK as sitk
    os.makedirs(out_dir, exist_ok=True)
    case = pose.get("case", "case"); view = pose.get("view", "view"); tag = pose.get("tag", "")
    stem = stem or view
    K0, R, t = camera_from_pose(pose)
    sid = float(pose.get("sid", frame_hdr.get("sid", 0) or 0)); sod = float(pose.get("sod", frame_hdr.get("sod", 0) or 0))
    px_fit = float(pose.get("px_mm", PITCH_FIT_MM))
    rows_f, cols_f = frame_img.shape
    if (rows_f, cols_f) != (2048, 2048) and abs(K0[0, 2] * 2 - cols_f) > 8:
        raise ValueError(f"frame {rows_f}x{cols_f} does not look like the frame K was fit on (cx {K0[0, 2]})")
    # ---- K policy
    K = K0.copy(); k_rescaled = False
    if k_policy == "rescale_to_sid":
        f_new = sid / pitch
        K[0, 0] = np.sign(K0[0, 0]) * f_new; K[1, 1] = np.sign(K0[1, 1]) * f_new; k_rescaled = True
    elif k_policy != "as_fit":
        raise ValueError(f"unknown --k-policy {k_policy}")
    fr = plane_frame(K, R, t, pitch)
    P = K @ np.c_[R, t]
    Tshift = np.array([[1, 0, -0.5], [0, 1, -0.5], [0, 0, 1.0]])
    P_cv = Tshift @ P
    # ---- radiograph on the plane
    att = stored_to_atten(frame_img)
    xr_arr = att.astype(np.float32) if xr_values == "atten" else frame_img.astype(np.uint16)
    xr_path = os.path.join(out_dir, f"xr_{stem}.nii.gz")
    write_plane_nifti(xr_path, xr_arr, fr, 1)
    tfm_path = os.path.join(out_dir, f"xr_{stem}.tfm"); Afp, bfp = write_tfm(tfm_path, fr)
    P_path = os.path.join(out_dir, f"xr_{stem}_P.txt"); write_P(P_path, P_cv)
    # ---- DRR on the same plane
    if mu_cache is None or mu_cache.get("path") != cbct_path:
        mu, A, _ = load_mu(cbct_path)
        if mu_cache is not None:
            mu_cache.update(path=cbct_path, mu=mu, A=A)
    else:
        mu, A = mu_cache["mu"], mu_cache["A"]
    if cols_f % drr_down or rows_f % drr_down:
        raise ValueError(f"--drr-down {drr_down} does not divide the frame {cols_f}x{rows_f}")
    Hd, Wd = rows_f // drr_down, cols_f // drr_down
    Kd = K.copy(); Kd[:2] /= drr_down
    backend = drr_backend
    drr = None
    if drr_backend == "torch":
        drr = render_torch(mu, A, Kd, R, t, Hd, Wd, drr_steps)
        if drr is None:
            backend = "numpy(torch unavailable)"
    if drr is None:
        drr = render_numpy(mu, A, Kd, R, t, Hd, Wd, drr_steps)
    drr_path = os.path.join(out_dir, f"drr_{stem}.nii.gz")
    write_plane_nifti(drr_path, drr.astype(np.float32), fr, drr_down)
    att_d = block_mean(att, drr_down)
    drr_frame_ncc = float(np.corrcoef(drr.ravel(), att_d.ravel())[0, 1])
    # ---- checks 1-4: the three descriptions of the camera agree on every centroid
    names = [cents[k][0] for k in cents]; pts = np.array([cents[k][1] for k in cents]); vox = [cents[k][2] for k in cents]
    uv, depth = project(K, R, t, pts)
    uv_cv = (P_cv @ np.c_[pts, np.ones(len(pts))].T).T; uv_cv = uv_cv[:, :2] / uv_cv[:, 2:3]
    e_cv = np.abs(uv_cv - (uv - 0.5)).max() if len(pts) else 0.0
    M, b = read_tfm_as_affine(tfm_path)
    s_loc = M @ fr["source"] + b
    uv_tfm = np.array([plane_pixel_from_local(M @ p + b, s_loc, fr["step_col"], fr["step_row"]) for p in pts])
    e_tfm = float(np.abs(uv_tfm - uv).max()) if len(pts) else 0.0
    ni = nib.load(xr_path)
    A_lps = np.diag([-1, -1, 1, 1.0]) @ ni.affine
    o = A_lps[:3, 3]; a1 = A_lps[:3, 0]; a2 = A_lps[:3, 1]; nrm = np.cross(a1, a2); nrm /= np.linalg.norm(nrm)
    uv_nii = []
    for p in pts:
        d = p - fr["source"]; lam = np.dot(nrm, o - fr["source"]) / np.dot(nrm, d)
        X = fr["source"] + lam * d
        cr, *_ = np.linalg.lstsq(np.c_[a1, a2], X - o, rcond=None)
        uv_nii.append(cr + 0.5)
    uv_nii = np.array(uv_nii) if len(pts) else np.zeros((0, 2))
    e_nii = float(np.abs(uv_nii - uv).max()) if len(pts) else 0.0
    im_rb = sitk.ReadImage(xr_path)
    sp_rb = np.array(im_rb.GetSpacing()); sp_err = float(np.abs(sp_rb[:2] - [fr["step_col"], fr["step_row"]]).max())
    # ---- check 8: the ITK meaning of the .tfm, done the way 3D Slicer uses a transform file. A copy of the
    # radiograph in the detector-LOCAL frame (identity direction; voxel (c, r) centred at ((c+0.5) step_col,
    # (r+0.5) step_row, 0)) resampled onto the PLACED volume's grid with the file's transform (ITK resampling
    # semantics: output point -> transform -> input point) must reproduce the placed volume voxel for voxel.
    local = sitk.GetImageFromArray(np.ascontiguousarray(xr_arr)[None])
    local.SetSpacing((fr["step_col"], fr["step_row"], SLAB_MM)); local.SetOrigin((0.5 * fr["step_col"], 0.5 * fr["step_row"], 0.0))
    res = sitk.Resample(local, im_rb, sitk.ReadTransform(tfm_path), sitk.sitkNearestNeighbor, 0.0, local.GetPixelID())
    resample_diff = float(np.abs(sitk.GetArrayFromImage(res).astype(np.float64) - sitk.GetArrayFromImage(im_rb).astype(np.float64)).max())
    reproj_pass = bool(e_tfm <= REPROJ_TOL_PX and e_nii <= REPROJ_TOL_PX and e_cv <= 1e-6 and sp_err < 1e-6 and resample_diff == 0.0)
    # ---- check 5: the registration's objective at this pose on its own working grid
    edge_rep = int_rep = None; f_work = max(1, int(round(max(rows_f, cols_f) / WORK_GRID)))
    if reproduce_score and not k_rescaled:
        Kw = K0.copy(); Kw[:2] /= f_work
        drr_w = render_numpy(mu, A, Kw, R, t, rows_f // f_work, cols_f // f_work, drr_steps)
        edge_rep, int_rep = registration_score(drr_w, att, f_work)
    # ---- check 6: the torch renderer at the same pose
    corr_torch = None
    if torch_check:
        d2 = render_torch(mu, A, Kd, R, t, Hd, Wd, drr_steps)
        if d2 is not None:
            corr_torch = float(np.corrcoef(drr.ravel(), d2.ravel())[0, 1])
    # ---- check 7: boxes
    boxes = box_report(meta, uv, names, cols_f, tag) if meta else None
    # ---- sidecar and row
    inputs = {"pose": (pose_path, sha256_file(pose_path)), "cbct": (cbct_path, sha256_file(cbct_path)),
              "frame": (f"frame_key:{frame_key_of(frame_path)}", sha256_file(frame_path))}
    if meta_path:
        inputs["meta"] = (meta_path, sha256_file(meta_path))
    for k_, v_ in (extra_inputs or {}).items():
        inputs[k_] = v_
    git_sha, dirty = git_state()
    centre_depth = float((R @ (A @ np.r_[(np.array(mu.shape[::-1]) - 1) / 2.0, 1.0])[:3] + t)[2])
    side = dict(
        tool=TOOL, tool_version=TOOL_VERSION, utc=utc_now(), git_sha=git_sha, git_dirty=dirty, case=case, view=view, pose_tag=tag,
        frame_key=frame_key_of(frame_path), frame_header=frame_hdr, pose_fields=dict(edge_ncc=pose.get("edge_ncc"), int_ncc=pose.get("int_ncc"),
        margin=pose.get("margin"), hyp=pose.get("hyp"), sid=sid, sod=sod, px_mm_fit=px_fit, kvp=pose.get("kvp")),
        conventions=dict(
            world="the CBCT's physical frame as SimpleITK reports it: LPS mm, direction honoured",
            camera="p_cam = R p_world + t; pixel = K p_cam / z; pixel (c, r) is centred at (c + 0.5, r + 0.5) (raycaster convention)",
            P_txt="xr_<view>_P.txt is OpenCV-convention (pixel centres at integers): P_opencv = [[1,0,-0.5],[0,1,-0.5],[0,0,1]] K [R | t]; rows u (column), v (row), w",
            nifti=("single-slice volume in LPS: voxel (c, r, 0) centre = corner + (c+0.5) step_col e_col + (r+0.5) step_row e_row; "
                   "direction columns e_col, e_row, normal = e_col x e_row (right-handed); the file's NIfTI affine is RAS as usual"),
            tfm=("ITK AffineTransform, LPS, FROM PARENT: p_local = C^T (p_world - corner), C = [e_col e_row normal]; local x/y in mm along "
                 "columns/rows from the outer corner of pixel (0,0), z along the normal (0 on the plane). 3D Slicer shows the inverse "
                 "(local -> world) as the node's transform-to-parent in RAS; the Volume Reslice Driver in Axial mode driven by this node "
                 "reslices along the detector plane"),
            plane=("distance D = |fx| * pitch from the source along R^T e_z, the one distance at which the plane's pixel step equals the "
                   "pitch; equals the header SID only when K was fit at this pitch"),
            drr="own numpy ray-marcher (drr_register.Renderer's sampling) at K / drr_down on the same plane; values are line integrals of mu (1/mm * mm)",
            xr_values=("-log((stored - p0.1 + 1) / (p99.9 - p0.1 + 1)), bone bright (carmlspine_pose.stored_to_atten)" if xr_values == "atten" else "stored uint16"),
        ),
        pitch=dict(fit_mm=px_fit, true_mm=pitch, det_mm=pitch * cols_f, k_policy=k_policy, k_rescaled=k_rescaled,
                   needs_refit=bool(abs(px_fit - pitch) > 1e-9),
                   note=("K is written as fit; the plane sits at |fx| * pitch, not at the header SID, until the pose is refit at the true pitch"
                         if not k_rescaled else "fx, fy were rescaled to SID / pitch: the projection differs from the fit by the ratio of the pitches")),
        K_written=K.tolist(), K_fit=K0.tolist(), R=R.tolist(), t=t.tolist(), P_raycaster=P.tolist(), P_opencv=P_cv.tolist(),
        plane=dict(distance_mm=fr["distance"], sid_header_mm=sid, plane_minus_sid_mm=fr["distance"] - sid, source_lps=fr["source"].tolist(),
                   corner_lps=fr["corner"].tolist(), e_col=fr["e_col"].tolist(), e_row=fr["e_row"].tolist(), normal=fr["normal"].tolist(),
                   beam_axis=fr["beam_axis"].tolist(), normal_points_toward_source=fr["normal_points_toward_source"],
                   step_col_mm=fr["step_col"], step_row_mm=fr["step_row"], slab_mm=SLAB_MM, cbct_centre_depth_mm=centre_depth,
                   sod_header_mm=sod),
        tfm_from_parent=dict(matrix=Afp.tolist(), translation=bfp.tolist(), read_back_matrix=M.tolist(), read_back_translation=b.tolist()),
        checks=dict(reproj_tfm_max_px=e_tfm, reproj_nifti_max_px=e_nii, reproj_opencv_max_px=float(e_cv), nifti_spacing_err_mm=sp_err,
                    tfm_resample_max_diff=resample_diff,
                    nifti_axcodes=list(nib.aff2axcodes(ni.affine)), tolerance_px=REPROJ_TOL_PX, reproj_pass=reproj_pass,
                    edge_ncc_json=pose.get("edge_ncc"), edge_ncc_reproduced=edge_rep, int_ncc_json=pose.get("int_ncc"), int_ncc_reproduced=int_rep,
                    work_factor=f_work, renderer_corr_torch=corr_torch, drr_frame_ncc=drr_frame_ncc),
        centroids=[dict(name=n, voxels=v, lps=p.tolist(), depth_mm=float(z), u=float(a[0]), v=float(a[1]), u_tfm=float(b_[0]), v_tfm=float(b_[1]),
                        u_nii=float(c_[0]), v_nii=float(c_[1]), in_frame=bool(0 <= a[0] < cols_f and 0 <= a[1] < rows_f))
                   for n, v, p, z, a, b_, c_ in zip(names, vox, pts, depth, uv, uv_tfm, uv_nii)],
        centroid_source=cent_source, boxes=boxes,
        drr=dict(down=drr_down, steps=drr_steps, backend=backend, shape=[Hd, Wd], spacing_mm=[fr["step_col"] * drr_down, fr["step_row"] * drr_down]),
        inputs_sha256={k: dict(path=v[0], sha256=v[1]) for k, v in inputs.items()},
        outputs=dict(xr=xr_path, tfm=tfm_path, P=P_path, drr=drr_path),
    )
    row = dict(status="ok", case=case, view=view, pose_tag=tag, frame_key=side["frame_key"], utc=side["utc"], tool=TOOL, tool_version=TOOL_VERSION,
               git_sha=git_sha, git_dirty=dirty, pitch_fit_mm=px_fit, pitch_true_mm=pitch, det_mm=pitch * cols_f, k_policy=k_policy,
               k_rescaled=k_rescaled, needs_refit=side["pitch"]["needs_refit"], fx_px=K[0, 0], fy_px=K[1, 1], cx_px=K[0, 2], cy_px=K[1, 2],
               sid_header_mm=sid, sod_header_mm=sod, plane_distance_mm=fr["distance"], plane_minus_sid_mm=fr["distance"] - sid,
               cbct_centre_depth_mm=centre_depth, source_lps_mm=json.dumps([round(float(x), 3) for x in fr["source"]]),
               normal_points_toward_source=fr["normal_points_toward_source"], centroid_source=cent_source, n_centroids=len(pts),
               reproj_tfm_max_px=e_tfm, reproj_nifti_max_px=e_nii, reproj_opencv_max_px=float(e_cv), tfm_resample_max_diff=resample_diff,
               reproj_pass=reproj_pass,
               edge_ncc_json=pose.get("edge_ncc"), edge_ncc_reproduced=edge_rep, int_ncc_json=pose.get("int_ncc"), int_ncc_reproduced=int_rep,
               renderer_corr_torch=corr_torch, drr_down=drr_down, drr_steps=drr_steps, drr_backend=backend, drr_frame_ncc=drr_frame_ncc,
               boxes_meta=meta_path or "", boxes_pose_tag=(boxes or {}).get("boxes_pose_tag", ""), boxes_pose_tag_match=(boxes or {}).get("same_pose_tag", ""),
               n_boxed=(boxes or {}).get("n_boxed", ""), n_in_box=(boxes or {}).get("n_in_box", ""), n_in_box_required=(boxes or {}).get("n_required", ""),
               n_in_box_required_hit=(boxes or {}).get("n_required_hit", ""),
               in_box_detail=json.dumps([dict(name=r["name"], inside=r["inside"], outside_px=r.get("outside_px")) for r in (boxes or {}).get("rows", [])]),
               inputs_sha256=json.dumps({k: v[1] for k, v in inputs.items()}), outputs=json.dumps(side["outputs"]), reason="")
    json.dump(side, open(os.path.join(out_dir, f"xr_{stem}.json"), "w"), indent=1)
    return row, side


# ------------------------------------------------------------------------------------------------ rows
def write_rows(path, rows, prereg_path, prereg_sha, prereg_status):
    old = {}
    if os.path.exists(path):
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                old[(r["case"], r["view"], r["pose_tag"])] = r
    for r in rows:
        r = dict(r); r.update(prereg_path=str(prereg_path), prereg_sha256=prereg_sha, prereg_status=prereg_status)
        old[(r["case"], r["view"], r["pose_tag"])] = {c: ("" if r.get(c) is None else r.get(c, "")) for c in ROW_COLUMNS}
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ROW_COLUMNS, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for k in sorted(old):
            w.writerow({c: old[k].get(c, "") for c in ROW_COLUMNS})


def failed_row(case, view, tag, reason):
    git_sha, dirty = git_state()
    return {c: "" for c in ROW_COLUMNS} | dict(status=f"failed: {reason}", case=case, view=view, pose_tag=tag, utc=utc_now(), tool=TOOL,
                                                 tool_version=TOOL_VERSION, git_sha=git_sha, git_dirty=dirty, reason=reason)


# ------------------------------------------------------------------------------------------------ matching / grid
def match_frame(pose, frame_paths):
    fk = pose.get("frame_key")
    for p in frame_paths:
        if fk and frame_key_of(p) == fk:
            return p
    old = pose.get("frame")
    for p in frame_paths:
        if old and os.path.basename(p) == old:
            return p
    return None


def resolve_case(case, pose_dir, roots):
    """The grid layout: (pose paths by view, cbct, mask, ctd, frame paths, meta paths). Refuses a missing pose dir."""
    import glob
    if not os.path.isdir(pose_dir):
        raise FileNotFoundError(f"pose directory {pose_dir} does not exist (the 0.1465-mm poses are read only with an explicit --pose-dir)")
    meta_dir = roots["meta"]
    metas = {os.path.basename(p)[len(case) + 1: -5]: p for p in glob.glob(os.path.join(meta_dir, f"{case}_*.json"))}
    poses = {}
    for p in sorted(glob.glob(os.path.join(pose_dir, f"{case}_*_ref*.json"))):
        stem = os.path.basename(p)[len(case) + 1: -5]
        view, tag = stem.split("_ref"); tag = "_ref" + tag
        poses.setdefault(view, {})[tag] = p
    chosen = {}
    for view, tags in poses.items():
        want = None
        if view in metas:
            want = (json.load(open(metas[view])).get("pose") or {}).get("refined")
        if want not in tags:
            want = "_ref2" if ("_ref2" in tags and view.startswith(("LAT", "OBL"))) else "_ref"
        chosen[view] = tags[want]
    import carmlspine_io as CIO
    frames = [f["path"] for f in CIO.spot_frames(os.path.join(roots["unpacked"], case))]
    return dict(poses=chosen, cbct=os.path.join(roots["nifti"], f"{case}_cbct.nii.gz"),
                mask=os.path.join(roots["spineps"], f"{case}_seg-vert_msk.nii.gz"), ctd=os.path.join(roots["spineps"], f"{case}_ctd.json"),
                frames=frames, metas=metas)


# ------------------------------------------------------------------------------------------------ main / selftest
def run(a):
    prereg_sha, prereg_status = prereg_state(a.prereg)
    if a.case:
        rs = a.rs.rstrip("/")
        roots = dict(nifti=f"{rs}/data/carmlspine/nifti", spineps=f"{rs}/data/carmlspine/spineps",
                     unpacked=f"{rs}/data/carmlspine/unpacked/C-ArmLSpine", meta=f"{rs}/data/realxray/carmlspine/meta")
        res = resolve_case(a.case, a.pose_dir, roots)
        pose_paths = list(res["poses"].values()); cbct = res["cbct"]; mask = res["mask"]; ctd = res["ctd"]
        frames = res["frames"]; metas = list(res["metas"].values())
    else:
        pose_paths, cbct, mask, ctd, frames, metas = a.pose, a.cbct, a.mask, a.ctd, a.frame, a.meta or []
    if not pose_paths:
        raise SystemExit("no pose JSON given")
    poses = [(p, json.load(open(p))) for p in pose_paths]
    case = poses[0][1].get("case", a.case or "case")
    out_dir = os.path.join(a.out, case)
    os.makedirs(out_dir, exist_ok=True)
    extra = {}
    cents, cent_source = None, None
    cent_err = None
    try:
        if a.ts_dir:
            cents = ts_centroids(a.ts_dir); cent_source = f"ts:{a.ts_dir}"
            for p in sorted(Path(a.ts_dir).glob("*.nii.gz")):
                extra[f"ts:{p.name}"] = (str(p), sha256_file(p))
        else:
            cents, guard, _ = spineps_centroids(mask, ctd); cent_source = f"spineps:{guard}"
            extra["mask"] = (mask, sha256_file(mask))
            if ctd:
                extra["ctd"] = (ctd, sha256_file(ctd))
    except Exception as e:  # noqa: BLE001
        cent_err = f"{type(e).__name__}: {e}"
    meta_by_view = {}
    for m in metas:
        try:
            mj = json.load(open(m)); meta_by_view[mj.get("view")] = (m, mj)
        except Exception:  # noqa: BLE001
            pass
    rows = []; sides = []; cache = {}
    n_per_view = {}
    for _, pose in poses:
        n_per_view[pose.get("view", "?")] = n_per_view.get(pose.get("view", "?"), 0) + 1
    for pose_path, pose in poses:
        view = pose.get("view", "?"); tag = pose.get("tag", "")
        try:
            if cent_err:
                raise RuntimeError(f"centroids unavailable: {cent_err}")
            if n_per_view[view] > 1 and not a.suffix_tag:
                # xr_<view>.* would be overwritten by the other tag's files: refuse rather than leave whichever ran last
                raise RuntimeError(f"{n_per_view[view]} poses for view {view} in one run; pass --suffix-tag (files xr_{view}{tag}.*) or choose one")
            stem = f"{view}{tag}" if a.suffix_tag else view
            fp = match_frame(pose, frames)
            if fp is None:
                raise FileNotFoundError(f"no frame matches pose {os.path.basename(pose_path)} (frame_key {pose.get('frame_key')}, frame {pose.get('frame')})")
            img, hdr = read_frame(fp)
            mp, mj = meta_by_view.get(view, (None, None))
            row, side = export_view(pose, pose_path, img, hdr, fp, cbct, cents, cent_source, out_dir, pitch=a.pitch, k_policy=a.k_policy,
                                    drr_down=a.drr_down, drr_steps=a.drr_steps, drr_backend=a.drr_backend, xr_values=a.xr_values,
                                    meta=mj, meta_path=mp, reproduce_score=not a.no_score, torch_check=not a.no_torch_check,
                                    extra_inputs=extra, mu_cache=cache, stem=stem)
            rows.append(row); sides.append(side)
            print(f"{case} {view}{tag}: reproj tfm {row['reproj_tfm_max_px']:.4f} px, nifti {row['reproj_nifti_max_px']:.4f} px, "
                  f"opencv {row['reproj_opencv_max_px']:.1e} px, itk-resample diff {row['tfm_resample_max_diff']:.1e} -> "
                  f"{'PASS' if row['reproj_pass'] else 'FAIL'}; plane {row['plane_distance_mm']:.2f} mm "
                  f"(SID {row['sid_header_mm']:.0f}, {row['plane_minus_sid_mm']:+.2f}); edge NCC json {row['edge_ncc_json']} reproduced "
                  f"{row['edge_ncc_reproduced']}; torch corr {row['renderer_corr_torch']}; boxes {row['n_in_box']}/{row['n_boxed']} inside "
                  f"(required {row['n_in_box_required_hit']}/{row['n_in_box_required']}, same pose tag {row['boxes_pose_tag_match']})", flush=True)
        except Exception as e:  # noqa: BLE001
            traceback.print_exc()
            rows.append(failed_row(case, view, tag, f"{type(e).__name__}: {e}"))
            print(f"{case} {view}{tag}: FAILED {type(e).__name__}: {e}", flush=True)
    write_rows(os.path.join(out_dir, "pose_to_viewer_rows.tsv"), rows, a.prereg, prereg_sha, prereg_status)
    return rows, sides


def selftest(a):
    """case42 (VERIDAH L6): AP _ref and LAT _ref2 (the poses the realxray meta boxes were built from) plus LAT _ref
    (a different pose than the boxes: the box report is informational there). Exits non-zero on any mismatch."""
    S = Path(a.samples)
    need = ["case42_AP_ref.json", "case42_LAT_ref2.json", "case42_LAT_ref.json", "case42_cbct.nii.gz", "case42_seg-vert_msk.nii.gz",
            "case42_ctd.json", "0001.dcm", "0002.dcm", "case42_AP.json", "case42_LAT.json"]
    missing = [n for n in need if not (S / n).exists()]
    if missing:
        print("selftest: missing sample files:", missing); return 2
    ns = argparse.Namespace(**vars(a))
    ns.case = None; ns.pose = [str(S / "case42_AP_ref.json"), str(S / "case42_LAT_ref2.json"), str(S / "case42_LAT_ref.json")]
    ns.cbct = str(S / "case42_cbct.nii.gz"); ns.mask = str(S / "case42_seg-vert_msk.nii.gz"); ns.ctd = str(S / "case42_ctd.json")
    ns.frame = [str(S / "0001.dcm"), str(S / "0002.dcm")]; ns.meta = [str(S / "case42_AP.json"), str(S / "case42_LAT.json")]
    ns.ts_dir = None; ns.suffix_tag = True          # LAT _ref2 and LAT _ref in one run: files are xr_LAT_ref2.* and xr_LAT_ref.*
    ns.out = a.out or str(S / "out")
    rows, sides = run(ns)
    fails = []
    for r in rows:
        tagv = f"{r['view']}{r['pose_tag']}"
        if r["status"] != "ok":
            fails.append(f"{tagv}: {r['status']}"); continue
        if not r["reproj_pass"]:
            fails.append(f"{tagv}: reprojection tfm {r['reproj_tfm_max_px']:.3f} / nifti {r['reproj_nifti_max_px']:.3f} px > {REPROJ_TOL_PX}, "
                         f"itk resample diff {r['tfm_resample_max_diff']}")
        if r["tfm_resample_max_diff"] != 0.0:
            fails.append(f"{tagv}: the local radiograph resampled through the .tfm differs from the placed one by {r['tfm_resample_max_diff']}")
        if abs(r["plane_distance_mm"] - abs(r["fx_px"]) * r["pitch_true_mm"]) > 1e-6:
            fails.append(f"{tagv}: plane distance is not |fx| * pitch")
        if r["needs_refit"] is not True:
            fails.append(f"{tagv}: needs_refit should be True for a 0.1465-mm pose")
        if r["edge_ncc_reproduced"] is None or abs(r["edge_ncc_reproduced"] - r["edge_ncc_json"]) > 0.02:
            fails.append(f"{tagv}: edge NCC reproduced {r['edge_ncc_reproduced']} vs json {r['edge_ncc_json']}")
        if r["renderer_corr_torch"] is not None and r["renderer_corr_torch"] < 0.999:
            fails.append(f"{tagv}: torch renderer corr {r['renderer_corr_torch']:.4f}")
        if r["boxes_pose_tag_match"] is True and r["n_in_box_required"] and r["n_in_box_required_hit"] != r["n_in_box_required"]:
            fails.append(f"{tagv}: {r['n_in_box_required_hit']}/{r['n_in_box_required']} required box hits")
        if r["n_centroids"] < 3:
            fails.append(f"{tagv}: only {r['n_centroids']} centroids")
    # the pre-registration on disk is DRAFT v1 with a blank freeze block: the rows must say "draft" (the first version
    # of prereg_state read the placeholder "frozen by: ____ (Greg)" as a signature)
    p_sha, p_status = prereg_state(a.prereg)
    if p_status != "draft":
        fails.append(f"prereg_status is {p_status!r} for {a.prereg} (freeze block blank -> expected 'draft')")
    print(f"prereg {os.path.basename(a.prereg)} sha256 {p_sha[:16]}... status {p_status}")
    # the TS fallback, if the files are beside the samples
    if (S / "ts_case42").is_dir():
        try:
            c = ts_centroids(str(S / "ts_case42"))
            print(f"ts fallback: {len(c)} structures {sorted(c)}")
            if len(c) < 3:
                fails.append("ts fallback found < 3 structures")
        except Exception as e:  # noqa: BLE001
            fails.append(f"ts fallback: {e}")
    # a rescale_to_sid run on one view, to show what the alternative policy does to the projection
    try:
        ns2 = argparse.Namespace(**vars(ns)); ns2.k_policy = "rescale_to_sid"; ns2.pose = [str(S / "case42_AP_ref.json")]
        ns2.out = os.path.join(ns.out, "rescale_to_sid"); ns2.no_score = True; ns2.no_torch_check = True; ns2.meta = [str(S / "case42_AP.json")]
        r2, s2 = run(ns2)
        r2 = r2[0]
        if r2["status"] != "ok" or not r2["k_rescaled"] or abs(r2["plane_distance_mm"] - r2["sid_header_mm"]) > 1e-6:
            fails.append(f"rescale_to_sid: {r2['status']} k_rescaled {r2['k_rescaled']} plane {r2['plane_distance_mm']}")
        else:
            du = np.array([[c["u"], c["v"]] for c in s2[0]["centroids"]]) - np.array([[c["u"], c["v"]] for c in sides[0]["centroids"]])
            print(f"rescale_to_sid moves the AP centroids by up to {np.abs(du).max():.1f} px (the 2.4 % about the principal point); boxes "
                  f"{r2['n_in_box']}/{r2['n_boxed']} inside")
    except Exception as e:  # noqa: BLE001
        fails.append(f"rescale_to_sid run: {type(e).__name__}: {e}")
    print("\nSELFTEST", "PASS" if not fails else "FAIL")
    for f in fails:
        print("  -", f)
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pose", action="append", default=[], help="pose JSON (repeatable)")
    ap.add_argument("--cbct"); ap.add_argument("--mask"); ap.add_argument("--ctd", default=None); ap.add_argument("--ts-dir", default=None)
    ap.add_argument("--frame", action="append", default=[], help="spot-frame DICOM (repeatable); matched by frame_key")
    ap.add_argument("--meta", action="append", default=[], help="realxray meta JSON (repeatable)")
    ap.add_argument("--case", default=None, help="grid mode: resolve every input from the standard roots")
    ap.add_argument("--pose-dir", default=f"{RS}/data/carmlspine/pose_150")
    ap.add_argument("--rs", default=RS, help="grid mode: the root the standard layout hangs from (a local mirror for testing)")
    ap.add_argument("--suffix-tag", action="store_true", help="name files xr_<view><tag>.* so two poses of one view can be exported in one run")
    ap.add_argument("--out", default=None)
    ap.add_argument("--pitch", type=float, default=PITCH_TRUE_MM, help="true detector pitch mm (307.2 / 2048)")
    ap.add_argument("--k-policy", default="as_fit", choices=["as_fit", "rescale_to_sid"])
    ap.add_argument("--drr-down", type=int, default=4); ap.add_argument("--drr-steps", type=int, default=192)
    ap.add_argument("--drr-backend", default="numpy", choices=["numpy", "torch"])
    ap.add_argument("--xr-values", default="atten", choices=["atten", "raw"])
    ap.add_argument("--no-score", action="store_true", help="skip the registration-objective reproduction (check 5)")
    ap.add_argument("--no-torch-check", action="store_true", help="skip the torch renderer comparison (check 6)")
    ap.add_argument("--prereg", default=str(DEFAULT_PREREG))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--samples", default=os.environ.get("TR_SAMPLES", ""), help="selftest: folder with the case42 sample files")
    a = ap.parse_args()
    if a.selftest:
        if not a.samples:
            ap.error("--selftest needs --samples DIR (or TR_SAMPLES)")
        return selftest(a)
    if not a.out:
        ap.error("--out is required")
    rows, _ = run(a)
    return 0 if all(r["status"] == "ok" for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
