#!/usr/bin/env python3
# spine-program/04_openspinetoolkit: copied 2026-10-08 from the NextPaper working folder on the laptop
# (untracked, in no repository; file dated 2026-05-17). The copy's source path and hash are recorded in
# 04_openspinetoolkit/MANIFEST_LOCAL.md. Superseded by OpenSpineToolkit (main, cb43197); kept as dated lineage.
# Reads the CTSpinoPelvic1K-Sample export of May 2026 under the legacy label map (L1 = 1 ... femur_right = 12);
# never run it on a v11 volume without ostk.labels.labels_for(volume).
"""
vertebral_corners.py
====================
Grab the CTSpinoPelvic1K-Sample dataset from the HuggingFace Hub, load one CT
case + its vertebral label mask, and locate the four sagittal-plane corner
points of every lumbar vertebral body:

    AS  anterosuperior      AI  anteroinferior
    PS  posterosuperior     PI  posteroinferior

Vertebral-body wedging angle (alpha) and intervertebral disc wedging angle
(beta) are then derived directly from those corners, and the whole thing is
rendered to a PNG.

Method -- extremal-corner approach, exactly as requested
--------------------------------------------------------
No osteophyte rejection, no robust line fitting. Corners are the literal
diagonal extrema of the body mask. The one piece of machinery kept is a
*rotated local frame*: lower lumbar bodies are tilted by lordosis, so the
diagonal extrema are taken in a per-vertebra (anterior, superior) frame
rather than in raw image axes. Without that, L5/L6 corners drift badly.

Pipeline
  1. anatomical_axes()  -- read S/I, A/P, L/R axes + signs from the NIfTI
                           affine. Orientation-agnostic; PIR is not assumed.
  2. isolate_body()     -- per vertebra: 3D erosion -> largest connected
                           component -> dilation. Drops spinous process and
                           laminae so posterior extrema land on the body.
                           Swap in your own posterior clip if you prefer;
                           pass --no-isolate to disable.
  3. superior_tangents()-- spine centerline from vertebral centroids; the
                           tangent at each vertebra is its local S-I axis.
  4. find_corners()     -- project body voxels of the vertebra's mid-sagittal
                           slice onto the local (u, v) frame, take 4 extrema.
  5. wedge_angles()     -- angles between endplate lines through the corners.

Usage
  pip install huggingface_hub nibabel scipy matplotlib numpy
  python vertebral_corners.py                  # token 408 (spine_only, L1-L5)
  python vertebral_corners.py --token 761      # a different lumbar case
  python vertebral_corners.py --list           # list cases + dataset stats
  python vertebral_corners.py --selftest       # synthetic check, no network

Only the metadata and the chosen token's two NIfTIs are downloaded -- the
dataset interface (CTSpinoPelvic1K.from_hub) fetches per-case, not the whole
2.37 GB repo. Lumbar-bearing sample tokens: 408, 489 (spine_only); 761, 71,
468 (fused). The other five are pelvic-only and have no lumbar labels.

Output: <out>/<token>_corners.png  and a printed corner/angle table.
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np

# Label ids 1..6 are L1..L6 in CTSpinoPelvic1K (7=sacrum, 8/9=hips).
LUMBAR_LABELS = {1: "L1", 2: "L2", 3: "L3", 4: "L4", 5: "L5", 6: "L6"}
CORNER_KEYS = ["AS", "AI", "PS", "PI"]
REPO_DEFAULT = "anonymous-neurips-ED/CTSpinoPelvic1K-Sample"


# --------------------------------------------------------------------------
# Dataset interface
# --------------------------------------------------------------------------
def load_dataset_interface(repo_id: str, cache_dir: str | None):
    """Download dataset_interface.py from the Hub and import it as a module."""
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(
        repo_id=repo_id,
        repo_type="dataset",
        filename="dataset_interface.py",
        cache_dir=cache_dir,
    )
    spec = importlib.util.spec_from_file_location("ctsp_iface", path)
    mod = importlib.util.module_from_spec(spec)
    # Register before exec_module: dataset_interface.py uses
    # `from __future__ import annotations`, so its @dataclass decorators
    # need the module discoverable in sys.modules to resolve the now-
    # stringized annotations. Without this, dataclass processing crashes
    # with "'NoneType' object has no attribute '__dict__'".
    sys.modules["ctsp_iface"] = mod
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# Orientation
# --------------------------------------------------------------------------
def anatomical_axes(affine: np.ndarray) -> dict:
    """Map array axes -> anatomical directions from a 4x4 affine.

    Returns dict with:
      si_axis, si_sign   array axis for Superior-Inferior; +1 if index
                         increases toward Superior, else -1
      ap_axis, ap_sign   array axis for Anterior-Posterior; +1 toward Anterior
      lr_axis            array axis for Left-Right (the sagittal slicing axis)
    """
    import nibabel as nib

    codes = nib.aff2axcodes(affine)  # e.g. ('P', 'I', 'R')
    info: dict = {}
    for ax, c in enumerate(codes):
        if c in ("S", "I"):
            info["si_axis"] = ax
            info["si_sign"] = 1 if c == "S" else -1
        elif c in ("A", "P"):
            info["ap_axis"] = ax
            info["ap_sign"] = 1 if c == "A" else -1
        elif c in ("L", "R"):
            info["lr_axis"] = ax
    missing = {"si_axis", "ap_axis", "lr_axis"} - info.keys()
    if missing:
        raise ValueError(f"Could not resolve axes {missing} from affine codes {codes}")
    return info


# --------------------------------------------------------------------------
# Body isolation
# --------------------------------------------------------------------------
def isolate_body(mask: np.ndarray, erode_iter: int = 3) -> np.ndarray:
    """Strip posterior elements: erode -> keep largest component -> dilate back.

    The vertebral body is a compact block; the spinous process and laminae
    hang off it through narrow pedicles, so erosion fragments them while the
    body survives as the largest component. This is a convenience default --
    replace it with your own posterior clip if you have one.
    """
    from scipy import ndimage as ndi

    m = mask.astype(bool)
    struct = ndi.generate_binary_structure(3, 3)  # full 3x3x3

    it = erode_iter
    eroded = m
    while it > 0:
        eroded = ndi.binary_erosion(m, structure=struct, iterations=it)
        if eroded.any():
            break
        it -= 1
    if not eroded.any():
        return m  # vertebra too thin to erode; use it as-is

    lbl, n = ndi.label(eroded, structure=struct)
    counts = np.bincount(lbl.ravel())
    counts[0] = 0
    core = lbl == int(counts.argmax())
    body = ndi.binary_dilation(core, structure=struct, iterations=it) & m
    return body


# --------------------------------------------------------------------------
# Spine centerline -> per-vertebra local frame
# --------------------------------------------------------------------------
def order_vertebrae(label: np.ndarray, axes: dict, ids) -> list:
    """Return [(label_id, centroid3d), ...] ordered superior -> inferior."""
    from scipy import ndimage as ndi

    found = []
    for k in ids:
        m = label == k
        if m.any():
            found.append((k, np.array(ndi.center_of_mass(m))))
    si_ax, si_sg = axes["si_axis"], axes["si_sign"]
    found.sort(key=lambda kc: -si_sg * kc[1][si_ax])  # most-superior first
    return found


def superior_tangents(ordered: list, axes: dict) -> dict:
    """Local superior direction (3D) at each vertebra = centerline tangent."""
    pts = [c for _, c in ordered]
    n = len(pts)
    tang = {}
    for i, (k, _) in enumerate(ordered):
        if n == 1:
            t = np.zeros(3)
            t[axes["si_axis"]] = axes["si_sign"]
        else:
            hi = pts[max(i - 1, 0)]      # superior neighbour
            lo = pts[min(i + 1, n - 1)]  # inferior neighbour
            t = hi - lo                  # vector pointing superiorly
        tang[k] = t
    return tang


def frame_2d(tan3d: np.ndarray, axes: dict):
    """Project a 3D superior tangent onto the sagittal plane -> (u, v).

    v = unit superior axis, u = unit anterior axis, both in (anterior,
    superior) coordinates.
    """
    ap_c = axes["ap_sign"] * tan3d[axes["ap_axis"]]
    si_c = axes["si_sign"] * tan3d[axes["si_axis"]]
    v = np.array([ap_c, si_c], float)
    if v[1] < 0:
        v = -v                       # keep v pointing superiorly
    nrm = np.linalg.norm(v)
    v = np.array([0.0, 1.0]) if nrm < 1e-9 else v / nrm
    u = np.array([v[1], -v[0]])      # 90 deg rotation -> points anteriorly
    return u, v


# --------------------------------------------------------------------------
# Corner detection
# --------------------------------------------------------------------------
def slice_si_ap(vol: np.ndarray, lr_index: int, axes: dict) -> np.ndarray:
    """Extract a sagittal slice, returned as a 2D array indexed [si, ap]."""
    sl = [slice(None)] * 3
    sl[axes["lr_axis"]] = int(lr_index)
    s2 = vol[tuple(sl)]
    other = [a for a in range(3) if a != axes["lr_axis"]]
    return np.transpose(s2, (other.index(axes["si_axis"]),
                              other.index(axes["ap_axis"])))


def find_corners(body3d: np.ndarray, lr_index: int, axes: dict,
                 u2d: np.ndarray, v2d: np.ndarray):
    """Four extremal corners of one vertebral body on its mid-sagittal slice.

    Returns (corners, body2d) where corners maps 'AS'/'AI'/'PS'/'PI' to
    (ap_index, si_index) tuples, and body2d is the 2D body mask indexed
    [ap, si]. Returns (None, body2d) if the slice is empty.
    """
    sl = [slice(None)] * 3
    sl[axes["lr_axis"]] = int(lr_index)
    s2 = body3d[tuple(sl)]
    other = [a for a in range(3) if a != axes["lr_axis"]]
    body2d = np.transpose(s2, (other.index(axes["ap_axis"]),
                                other.index(axes["si_axis"]))).astype(bool)

    ii, jj = np.nonzero(body2d)          # ii: ap index, jj: si index
    if ii.size == 0:
        return None, body2d

    ant = axes["ap_sign"] * ii           # anatomical anterior coordinate
    sup = axes["si_sign"] * jj           # anatomical superior coordinate
    pts = np.stack([ant, sup], axis=1).astype(float)
    su = pts @ u2d                       # anterior-ness
    sv = pts @ v2d                       # superior-ness

    pick = lambda score: (int(ii[np.argmax(score)]), int(jj[np.argmax(score)]))
    corners = {
        "AS": pick(su + sv),             # most anterior + most superior
        "AI": pick(su - sv),             # most anterior + most inferior
        "PS": pick(-su + sv),            # most posterior + most superior
        "PI": pick(-su - sv),            # most posterior + most inferior
    }
    return corners, body2d


# --------------------------------------------------------------------------
# Wedge angles
# --------------------------------------------------------------------------
def _anat(corner, axes):
    """(ap_index, si_index) -> (anterior_coord, superior_coord)."""
    return np.array([axes["ap_sign"] * corner[0],
                     axes["si_sign"] * corner[1]], float)


def _endplate_dir(c_post, c_ant, axes):
    """Endplate direction, posterior corner -> anterior corner."""
    return _anat(c_ant, axes) - _anat(c_post, axes)


def _signed_angle(d1, d2):
    """Signed angle (deg) from d1 to d2 in the (anterior, superior) plane."""
    d1 = d1 / (np.linalg.norm(d1) + 1e-12)
    d2 = d2 / (np.linalg.norm(d2) + 1e-12)
    cross = d1[0] * d2[1] - d1[1] * d2[0]
    return float(np.degrees(np.arctan2(cross, d1 @ d2)))


def wedge_angles(corners_by_vert: list, axes: dict):
    """Compute vertebral (alpha) and disc (beta) wedge angles.

    corners_by_vert: [(label_id, corners_dict), ...] ordered superior->inferior.

    Sign convention (both angles): positive => endplate pair diverges
    anteriorly (greater anterior height) -- the usual lordotic sense for
    lower lumbar discs.
    """
    alpha, beta = {}, {}
    for k, c in corners_by_vert:
        sup = _endplate_dir(c["PS"], c["AS"], axes)
        inf = _endplate_dir(c["PI"], c["AI"], axes)
        alpha[k] = _signed_angle(inf, sup)
    for (ku, cu), (kl, cl) in zip(corners_by_vert, corners_by_vert[1:]):
        upper_inf = _endplate_dir(cu["PI"], cu["AI"], axes)  # disc roof
        lower_sup = _endplate_dir(cl["PS"], cl["AS"], axes)  # disc floor
        beta[(ku, kl)] = _signed_angle(lower_sup, upper_inf)
    return alpha, beta


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def render(ct: np.ndarray, label: np.ndarray, axes: dict,
           per_vert: list, alpha: dict, beta: dict,
           out_path: Path, title: str):
    """Sagittal overlay: CT background, body masks, corners, endplate lines."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Common mid-sagittal slice for the CT background.
    lr = axes["lr_axis"]
    lum = np.isin(label, list(LUMBAR_LABELS))
    lr_idx = int(round(np.nonzero(lum)[0 if lr == 0 else (1 if lr == 1 else 2)].mean()))
    ct_slice = slice_si_ap(ct, lr_idx, axes).astype(float)   # [si, ap]

    fig, ax = plt.subplots(figsize=(7, 10))
    ax.imshow(ct_slice, cmap="gray", vmin=-200, vmax=1000, aspect="equal")

    # Orient: superior up, anterior left.
    if axes["si_sign"] > 0:
        ax.invert_yaxis()
    if axes["ap_sign"] > 0:
        ax.invert_xaxis()

    cmap = plt.get_cmap("tab10")
    for idx, (k, corners) in enumerate(per_vert):
        col = cmap(idx % 10)
        # corner (ap, si) -> plot point (x=ap, y=si)
        pt = {key: (corners[key][0], corners[key][1]) for key in CORNER_KEYS}
        # Endplate lines: superior PS-AS, inferior PI-AI.
        for a, b in (("PS", "AS"), ("PI", "AI")):
            ax.plot([pt[a][0], pt[b][0]], [pt[a][1], pt[b][1]],
                    "-", color=col, lw=2.0, alpha=0.9)
        # Anterior + posterior walls (visual closure of the body).
        for a, b in (("AS", "AI"), ("PS", "PI")):
            ax.plot([pt[a][0], pt[b][0]], [pt[a][1], pt[b][1]],
                    "--", color=col, lw=1.0, alpha=0.6)
        for key in CORNER_KEYS:
            ax.plot(pt[key][0], pt[key][1], "o", color=col,
                    ms=7, mec="white", mew=1.2)
        cx = np.mean([pt[key][0] for key in CORNER_KEYS])
        cy = np.mean([pt[key][1] for key in CORNER_KEYS])
        ax.text(cx, cy, f"{LUMBAR_LABELS[k]}\nα={alpha[k]:+.1f}°",
                color="white", fontsize=8, ha="center", va="center",
                bbox=dict(boxstyle="round", fc=col, ec="none", alpha=0.85))

    # Disc-wedge labels at the midpoint between adjacent bodies.
    for (ku, kl), b in beta.items():
        cu = dict(per_vert)[ku]
        cl = dict(per_vert)[kl]
        mx = np.mean([cu["AI"][0], cu["PI"][0], cl["AS"][0], cl["PS"][0]])
        my = np.mean([cu["AI"][1], cu["PI"][1], cl["AS"][1], cl["PS"][1]])
        ax.text(mx, my, f"β={b:+.1f}°", color="yellow", fontsize=7.5,
                ha="center", va="center",
                bbox=dict(boxstyle="round", fc="black", ec="yellow", alpha=0.7))

    ax.set_title(f"{title}\nsagittal slice (L-R idx {lr_idx})  "
                 f"|  α vertebral wedge,  β disc wedge", fontsize=10)
    ax.set_xlabel("anterior  <-->  posterior")
    ax.set_ylabel("superior  <-->  inferior")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)


# --------------------------------------------------------------------------
# Core driver: label volume -> corners, angles, figure
# --------------------------------------------------------------------------
def process(ct: np.ndarray, label: np.ndarray, affine: np.ndarray,
            out_path: Path, title: str, do_isolate: bool = True):
    axes = anatomical_axes(affine)
    present = [k for k in LUMBAR_LABELS if (label == k).any()]
    if not present:
        print("  no lumbar labels (1..6) present in this case -- nothing to do.")
        return
    print(f"  lumbar labels present: {[LUMBAR_LABELS[k] for k in present]}")

    ordered = order_vertebrae(label, axes, present)
    tang = superior_tangents(ordered, axes)

    per_vert = []
    for k, centroid in ordered:
        vmask = label == k
        body3d = isolate_body(vmask) if do_isolate else vmask
        lr_index = int(round(centroid[axes["lr_axis"]]))
        u2d, v2d = frame_2d(tang[k], axes)
        corners, _ = find_corners(body3d, lr_index, axes, u2d, v2d)
        if corners is None:
            print(f"  {LUMBAR_LABELS[k]}: empty mid-sagittal slice, skipped.")
            continue
        per_vert.append((k, corners))

    if not per_vert:
        print("  no usable vertebrae.")
        return

    alpha, beta = wedge_angles(per_vert, axes)

    print(f"\n  {'vert':5s} {'AS(ap,si)':>13s} {'AI(ap,si)':>13s} "
          f"{'PS(ap,si)':>13s} {'PI(ap,si)':>13s} {'alpha':>9s}")
    for k, c in per_vert:
        row = " ".join(f"({c[key][0]:3d},{c[key][1]:3d})" for key in CORNER_KEYS)
        print(f"  {LUMBAR_LABELS[k]:5s} {row}  {alpha[k]:+7.2f}°")
    if beta:
        print("\n  disc wedge angles (beta):")
        for (ku, kl), b in beta.items():
            print(f"    {LUMBAR_LABELS[ku]}-{LUMBAR_LABELS[kl]}: {b:+7.2f}°")

    render(ct, label, axes, per_vert, alpha, beta, out_path, title)
    print(f"\n  figure -> {out_path}")


# --------------------------------------------------------------------------
# Self-test (no network): synthetic lordotic spine
# --------------------------------------------------------------------------
def selftest(out_dir: Path):
    """Build a 3-vertebra synthetic volume in PIR orientation and run the
    pipeline. Each vertebra is a box (with a posterior 'spinous process'
    tail) shifted anteriorly down the stack to create lordotic curvature."""
    print("Self-test: synthetic PIR volume, 3 vertebrae with curvature.\n")
    P, I, R = 90, 150, 60                     # axes: Posterior, Inferior, Right
    ct = np.full((P, I, R), -1000, np.int16)
    label = np.zeros((P, I, R), np.uint8)
    # PIR affine: axis0->P (0,-1,0), axis1->I (0,0,-1), axis2->R (1,0,0)
    affine = np.array([[0, 0, 1, 0],
                       [-1, 0, 0, 0],
                       [0, -1, 0, 0],
                       [0, 0, 0, 1]], float)

    for n, lab in enumerate((1, 2, 3)):
        i0 = 20 + n * 38                      # inferior position of this body
        ap_shift = n * 7                      # progressive anterior shift
        a0 = 22 + ap_shift                    # anterior face (small P index)
        body = (slice(a0, a0 + 34), slice(i0, i0 + 30), slice(22, 38))
        proc = (slice(a0 + 34, a0 + 52), slice(i0 + 8, i0 + 22),
                slice(27, 33))                # posterior spinous-process tail
        for region in (body, proc):
            ct[region] = 450
            label[region] = lab

    out = out_dir / "selftest_corners.png"
    process(ct, label, affine, out, "SELF-TEST synthetic spine", do_isolate=True)
    print("\nExpected: posterior corners on the body block, NOT on the "
          "process tail; α near 0° (rectangular boxes); per-vertebra frames "
          "rotated by the synthetic curvature.")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=REPO_DEFAULT, help="HF dataset repo id")
    ap.add_argument("--token", default="408",
                    help="case token to process (default: 408 -- a "
                         "spine_only case with L1-L5; other lumbar-bearing "
                         "sample tokens: 761, 71, 468, 489)")
    ap.add_argument("--cache-dir", default=None, help="huggingface_hub cache dir")
    ap.add_argument("--out", default="./corner_output", help="output directory")
    ap.add_argument("--list", action="store_true",
                    help="print dataset stats + case tokens, then exit")
    ap.add_argument("--no-isolate", action="store_true",
                    help="skip morphological body isolation (use raw masks)")
    ap.add_argument("--selftest", action="store_true",
                    help="run synthetic sanity check, no network needed")
    args = ap.parse_args()

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.selftest:
        selftest(out_dir)
        return

    print(f"Loading dataset interface from {args.repo} ...")
    iface = load_dataset_interface(args.repo, args.cache_dir)
    ds = iface.CTSpinoPelvic1K.from_hub(repo_id=args.repo, cache_dir=args.cache_dir)
    print(ds.stats())

    if args.list:
        print("\nCases:")
        for c in ds.cases:
            print(f"  token={c.token:>6s}  config={c.config:14s} "
                  f"lstv={c.lstv_label or '-':14s} split={c.split}")
        return

    case = next((c for c in ds.cases if c.token == args.token), None)
    if case is None:
        tokens = ", ".join(c.token for c in ds.cases)
        sys.exit(f"token {args.token!r} not found. Available: {tokens}")
    if getattr(case, "n_lumbar_labels", 0) == 0:
        print(f"WARNING: token {case.token} ({case.config}) has no lumbar "
              f"labels -- the corner detector will find nothing. "
              f"Try --token 408 / 761 / 71 / 468 / 489.")

    print(f"\nProcessing token={case.token}  config={case.config}  "
          f"lstv={case.lstv_label or '-'}")
    print("  fetching CT + label NIfTIs (only this token is downloaded) ...")
    ct, _ = case.load_ct()
    label, affine = case.load_label()
    print(f"  ct {ct.shape} {ct.dtype}   label {label.shape} {label.dtype}")

    out_path = out_dir / f"{case.token}_corners.png"
    process(ct, label, affine, out_path,
            f"token {case.token}  ({case.config}, lstv={case.lstv_label or '-'})",
            do_isolate=not args.no_isolate)


if __name__ == "__main__":
    main()
