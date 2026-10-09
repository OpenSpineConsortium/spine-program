"""Project VerSe CTs to lateral radiographs, carrying every vertebra's identity into 2-D.

THE QUESTION THIS SERVES. Naming a vertebra by counting from C2 uses one thing: position in
a visible sequence. Crop the field of view until only one vertebra remains and that
information is gone, so whatever accuracy survives is carried by morphology alone. Measuring
where the curve falls says how much identity is encoded locally -- and it can be measured in
2-D, cheaply, on radiographs, which is the modality a case is actually planned on.

VerSe is the substrate because it is whole-spine: C2 to sacrum in one volume. CTSpinoPelvic1K
cannot host this experiment at all -- no record contains C2 and thoracic labels stop near T8,
so the top of the ladder does not exist there.

WHY LATERAL. Vertebrae stack along the supero-inferior axis, so a lateral beam projects each
body to its own horizontal band and they barely overlap -- an AP view superimposes the
posterior elements on the bodies and the level boundaries blur. Lateral is also the view the
existing corner detector was trained on, so the two stay comparable.

WHAT A 2-D LABEL MEANS HERE. A DRR integrates along the beam, so a 3-D label has no exact
2-D counterpart. Each vertebra's mask is projected by MAXIMUM (did this ray pass through the
bone at all), which gives its silhouette, and the per-vertebra box is the extent of that
silhouette. Where two labels claim a pixel the more anterior one is not preferred -- the
overlap is recorded, because a pixel claimed by two vertebrae is exactly the ambiguity a 2-D
classifier has to live with and hiding it would flatter the result.

ORIENTATION IS READ, NEVER ASSUMED. This corpus was reoriented to PIR by the converter, but
a fixed axis order is how this project has gone wrong before: resolving a structure against
the wrong map returns a finite, plausible, wrong answer. The supero-inferior and left-right
axes are taken from the affine's axcodes every time, and the output is flipped so that down
is inferior and left is anterior regardless of what came in.

    python tools/make_drr_dataset.py --src ~/vf_813 --dst ~/verse_drr --limit 4
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import nibabel as nib
import numpy as np

# VERSE-NATIVE IDS, NOT DATASET813 IDS, and the distinction decides whether this experiment
# is possible at all. convert_versefusion.py maps VerSe's C1-T9 to `ignore`, correctly --
# Dataset813's scheme begins at T10 and calling unnamed bone background would teach a
# falsehood. But the ladder's top rung IS C2, so reading vf_813 here yields cervical cases
# with no labelled vertebra whatsoever: gl003 carries C1-T5 in the raw mask and nothing in
# the converted one. The raw masks under VerSeFusion/data/unified/scan-*/*_msk.nii.gz are
# the source, in VerSe's own numbering.
LEVEL_NAMES = {**{i: f"C{i}" for i in range(1, 8)},
               **{7 + i: f"T{i}" for i in range(1, 13)},
               **{19 + i: f"L{i}" for i in range(1, 7)},
               26: "sacrum", 28: "T13"}
# Ordered cranial -> caudal, which is what "n vertebrae of context" has to mean.
LEVEL_ORDER = ([f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)]
               + ["T13"] + [f"L{i}" for i in range(1, 7)] + ["sacrum"])
IGNORE_ID = 44

# CTSpinoPelvic1K arrives in Dataset813 ids. It is the second, larger source for this
# experiment: 802 expert-labelled abdominopelvic CTs with T10-L6 and the sacrum, including
# the L6 cases. Both schemes are mapped onto the ONE class list above so a T12 from VerSe and
# a T12 from CTSpinoPelvic1K are the same class, which is what makes the two corpora a
# domain-generalisation test rather than two separate experiments.
DS813_NAMES = {1: "T10", 2: "T11", 3: "T12", 4: "T13", 5: "L1", 6: "L2", 7: "L3",
               8: "L4", 9: "L5", 10: "L6", 11: "sacrum"}
SCHEMES = {"verse": LEVEL_NAMES, "ds813": DS813_NAMES}
MIN_PIX = 60          # a silhouette smaller than this is a clipped sliver, not a vertebra

# A BONE PROJECTION, NOT A CHEST FILM. The first render integrated everything above -200 HU
# and came out as soft-tissue blur with the vertebrae flattened into the white -- the label
# boxes proved the geometry was right and the window was wrong. Soft tissue contributes a
# large, thickness-dependent offset that carries no level information, and the experimental
# variable here is how much SPINE is visible, so anything that makes brightness a function
# of how much neck is in frame is noise by construction.
#
# 150 HU is the conventional floor for cortical and trabecular bone in CT. Below it the ray
# contributes nothing, so what is integrated is bone path length and the vertebral outlines
# come through. This is not what a real radiograph looks like, and that is deliberate: the
# question is whether vertebral MORPHOLOGY identifies a level, not whether a network can
# also see through overlying muscle.
HU_FLOOR, HU_CEIL = 150.0, 1800.0
MU_WATER = 0.02
# For the PHYSICAL render (--path): everything above this is material a photon must cross. -900 HU keeps
# lung (about -800) and excludes air, so the path does not accumulate over the gap between couch and
# skin. The ceiling is shared with the bone render.
HU_AIR = -900.0


def to_pir(arr: np.ndarray, affine: np.ndarray) -> np.ndarray:
    """Reorient an array to PIR in memory, so every downstream axis is known.

    CANONICALISE TO ANALYSE, NEVER TO WRITE -- this project's standing rule, and this is the
    analyse side: nothing reoriented here is ever saved, and the CT and its mask are put
    through the identical transform derived from the same affine.

    The previous version computed the projection axis arithmetically from axcodes and got it
    wrong: the rendered DRR came out on its side and washed out. Index arithmetic over five
    possible source orientations is precisely the kind of finite, plausible, wrong answer
    that has cost this project weeks. Reorienting first makes the axes a fact rather than a
    derivation.

    After this: axis0 runs anterior->posterior, axis1 superior->inferior, axis2 left->right.
    """
    src = nib.orientations.io_orientation(affine)
    dst = nib.orientations.axcodes2ornt(("P", "I", "R"))
    return nib.orientations.apply_orientation(arr, nib.orientations.ornt_transform(src, dst))


def pir_spacing(header, affine):
    """Voxel spacing along each PIR axis, read through the SAME reorientation the voxels go through.

    The first version wrote `as_closest_canonical(...).get_zooms()[1]` as the row spacing. Canonical is
    RAS, so index 1 is the anterior-posterior spacing, and the DRR's rows run superior-inferior. On
    VerSe (0.29 mm in-plane, 1.25 mm slices) every ann said 0.29 mm/px, the sweep tool turned a 140 mm
    field into 481 rows on a 214-row image, and a "9-inch" sweep from C2 was two frames the height of
    the whole spine. On near-isotropic CTSP the same error was 2.4 %. A finite, plausible, wrong number.
    -> (mm along A->P, mm along S->I, mm along L->R)
    """
    src = nib.orientations.io_orientation(affine)
    dst = nib.orientations.axcodes2ornt(("P", "I", "R"))
    tr = nib.orientations.ornt_transform(src, dst)
    z = np.asarray(header.get_zooms()[:3], float)
    # row j of the transform is INPUT axis j and its first entry is where that axis lands, so the
    # source axis of output axis i is the inverse permutation. Indexing z[tr[i][0]] is the identity
    # on PIR input (CTSP) and wrong on anything else (VerSe is LPS), which is how the first respace
    # wrote 0.29 mm rows for gl003 a second time.
    inv = np.argsort(tr[:, 0].astype(int))
    return [float(z[int(inv[i])]) for i in range(3)]


def drr(ct_pir: np.ndarray) -> np.ndarray:
    """Lateral DRR from a PIR volume: integrate along left-right, then put SI down the page.

    First-order model only -- no spectrum, no scatter, no beam hardening. What it must get
    right here is that bone stands out from soft tissue, so vertebral outlines are findable.

    THE CONTRAST IS SET ON BONE, NOT ON THE WHOLE RAY. Normalising the integrated path by its
    global maximum let the shoulders and skull -- far thicker than the neck -- take the top of
    the range and flatten every vertebra into near-white, which is what the first render
    showed. Windowing on the bone percentile puts the dynamic range where the anatomy is.
    """
    a = np.clip(ct_pir.astype(np.float32), HU_FLOOR, HU_CEIL)
    mu = MU_WATER * (1.0 + a / 1000.0)
    mu[a <= HU_FLOOR] = 0.0
    path = mu.sum(axis=2)                       # left-right -> lateral view
    img = path.T                                # rows = SI (down = inferior), cols = AP
    # window on the rays that actually struck bone; an image that is mostly empty has a
    # 2nd percentile of zero and would otherwise spend its whole range on background
    nz = img[img > 0]
    lo = 0.0 if nz.size == 0 else float(np.percentile(nz, 1.0))
    hi = 1.0 if nz.size == 0 else float(np.percentile(nz, 99.5))
    img = np.clip((img - lo) / max(hi - lo, 1e-6), 0.0, 1.0)
    return img


def water_path_cm(ct_pir: np.ndarray, spacing_lr_mm: float) -> np.ndarray:
    """Water-equivalent path length in cm along each lateral ray, unwindowed.

    This is the quantity a physics model needs: transmitted intensity is I0*exp(-mu_w * L) with L in cm
    of water, before scatter and before the detector. It is NOT a displayable image and is never
    windowed, because windowing is what destroys the information the noise model depends on.

    mu is linear in HU against water. That is the same first-order model the bone render uses. It is
    good to a few per cent through soft tissue and it UNDERSTATES cortical bone at diagnostic energies,
    where the photoelectric term makes bone attenuate more than its HU suggests. Behind the vertebral body
    the simulated frame is therefore less photon-starved than a real one, but the larger consequence is the
    CONTRAST: a lumbar body adds only a few per cent to a lateral path of ~30 cm of water, and frames rendered
    from this map by sweep_map --perturb physics were LOOKED AT on 2026-09-22 (VerSe 602, CTSpinoPelvic1K 175)
    and showed no visible spine under the drawn noise and scatter. A linking or detection number measured on
    such frames is measured on soft-tissue texture, not bone (docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md).
    """
    a = np.clip(ct_pir.astype(np.float32), HU_AIR, HU_CEIL)
    rel = 1.0 + a / 1000.0          # water-equivalent density, 0 at -1000 HU, 1 at 0 HU
    rel[a <= HU_AIR] = 0.0
    cm = float(spacing_lr_mm) / 10.0
    return (rel.sum(axis=2) * cm).T.astype(np.float32)


def water_bone_paths_cm(ct_pir: np.ndarray, spacing_lr_mm: float):
    """Water and bone line integrals in cm along each lateral ray, with the DEFINITIONS THE DEVICE CARDS WERE
    FITTED WITH (deepfluoro_render.raycast, the corpus builder): water is density capped at water,
    clip((HU + 1000)/1000, 0, 1); bone is the positive-HU excess times the water/cortical attenuation ratio at
    70 keV, clip(HU, 0)/1000 * MU_RATIO_E0. device_style.style takes exactly this pair. water_path_cm above
    merges the two into one density-weighted path, which is what left the sweep's physics frames without a
    visible spine (docs/PHYSICS_SWEEP_NO_BONE_2026-09-22.md)."""
    import render_physics_drr as RPD
    hu = ct_pir.astype(np.float32)
    w = np.clip((hu + 1000.0) / 1000.0, 0.0, 1.0)
    b = np.clip(hu, 0.0, None) / 1000.0 * float(RPD.MU_RATIO_E0)
    cm = float(spacing_lr_mm) / 10.0
    return (w.sum(axis=2) * cm).T.astype(np.float32), (b.sum(axis=2) * cm).T.astype(np.float32)


def project_labels(gt_pir: np.ndarray, names: dict):
    """Per-level silhouette, box and overlap count in the projected plane (PIR input)."""
    levels, stack = {}, {}
    for cid in sorted(names):
        m = gt_pir == cid
        if not m.any():
            continue
        sil = m.any(axis=2).T
        n = int(sil.sum())
        if n < MIN_PIX:
            continue
        ys, xs = np.nonzero(sil)
        levels[cid] = {
            "name": names[cid],
            "box": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
            "pixels": n,
            "centroid": [float(xs.mean()), float(ys.mean())],
        }
        stack[cid] = sil
    # a pixel claimed by two vertebrae is real ambiguity; count it rather than resolve it
    if stack:
        tot = np.sum(np.stack(list(stack.values())), axis=0)
        overlap = int((tot > 1).sum())
        union = int((tot > 0).sum())
    else:
        overlap = union = 0
    return levels, overlap, union



def body_mask_for(stem: str, body_dir, ct_shape, prefixes=("", "CTSP_", "TS_", "VERSE_"), ct_affine=None):
    """The SPINEPS body mask for a render case, or None, with the reason printed rather than swallowed.

    THE BOX CONVENTION (Greg, 2026-09-23): the human annotation on the real frames boxes the vertebral BODY, so a
    rendered box must box the body too. The release labels are whole vertebrae, and the body is SPINEPS's instance
    mask restricted to semantic sub-regions 49/50 -- tools/body_masks.py writes exactly that, per case, on the CT's
    own grid. Matching is by case name with the collection prefixes tried in turn; a shape mismatch means the mask
    was built from a different volume and is refused, never resampled silently. So is an affine mismatch (the
    same shape on another grid would put every box in the wrong place, and only the shape used to be compared).

    THE IDS ARE NAMES ONLY IF SHOWN (2026-09-23, SchwingNet/results/spineps_ids/IMPACT.md): body_boxes() reads a
    body id as a VerSe name, and 2,714 bodies carried raw SPINEPS instance ids 1..N. Every mask is passed through
    tools/spineps_ids.body_source_ok (the guard, against the ctd of the instance mask it was cut from) and a mask
    that fails RAISES SpinepsIdError: relabel its source with `tools/spineps_ids.py relabel` and rebuild the body.
    """
    import os
    import nibabel as nib
    import numpy as np
    if not body_dir:
        return None
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from spineps_ids import body_source_ok
    base = str(stem)
    for pre in prefixes:
        for cand in (pre + base, pre + base.split("_")[-1]):
            f = os.path.join(os.path.expanduser(str(body_dir)), f"{cand}_body_msk.nii.gz")
            if os.path.exists(f):
                bm = nib.load(f)
                arr = np.asanyarray(bm.dataobj).astype(np.int16)
                if arr.shape != tuple(ct_shape):
                    print(f"  body mask shape {arr.shape} != label {tuple(ct_shape)} for {cand}: refused",
                          file=sys.stderr)
                    return None
                if ct_affine is not None and not np.allclose(bm.affine, ct_affine, atol=1e-3):
                    print(f"  body mask affine differs from the label's for {cand}: refused", file=sys.stderr)
                    return None
                body_source_ok(f, what=f"{cand} body mask")      # a path: the ctd is found through <case>_body.json
                return arr, bm.affine
    return None


def body_boxes(body_pir, names, verse_names):
    """Per-level body box, keyed by the RENDER scheme's ids, from the body mask (which carries VerSe ids).

    The two schemes are bridged by NAME, never by a fixed offset: a render id whose name has no VerSe id (or whose
    body is absent from the mask) simply has no body box, and the caller keeps the whole-vertebra box and says so.
    """
    import numpy as np
    inv = {v: k for k, v in verse_names.items()}
    out = {}
    for cid, nm in names.items():
        vid = inv.get(nm)
        if vid is None:
            continue
        m = body_pir == vid
        if not m.any():
            continue
        sil = m.any(axis=2).T
        n = int(sil.sum())
        if n < MIN_PIX:
            continue
        ys, xs = np.nonzero(sil)
        out[cid] = {"box": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                    "pixels": n, "centroid": [float(xs.mean()), float(ys.mean())]}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="vf_813 (imagesTr/labelsTr)")
    ap.add_argument("--dst", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--png", action="store_true", help="also write a viewable PNG")
    ap.add_argument("--scheme", choices=sorted(SCHEMES), default="verse")
    ap.add_argument("--ct-root", default=None,
                    help="ds813 only: where the CT volumes really live; the imagesTr links "
                         "are container paths and do not resolve on the host")
    ap.add_argument("--prefix", default="", help="prepended to every case id")
    ap.add_argument("--resume", action="store_true", help="skip cases whose ann already exists")
    ap.add_argument("--body-mask-dir", default=None,
                    help="SPINEPS body masks (tools/body_masks.py). With this, the per-level `box` is the "
                         "VERTEBRAL BODY box -- the convention of the human annotation on the real frames -- and "
                         "the whole-vertebra box is kept as `outline_box`. Without it, `box` stays the whole "
                         "vertebra and the ann records which convention it is in.")
    ap.add_argument("--respace", action="store_true",
                    help="only rewrite mm_per_px_row_si_col_ap in existing anns from the source headers; "
                         "the rendered pixels do not change, so nothing is re-rendered")
    ap.add_argument("--path-only", action="store_true",
                    help="write ONLY path/<case>.npy and leave img/ and ann/ untouched. Use this to add "
                         "the physical render to a corpus that already exists: re-running the full "
                         "renderer would rewrite every annotation, and the scheme that produced them is "
                         "not recorded.")
    ap.add_argument("--path", action="store_true",
                    help="also write path/<case>.npy: the water-equivalent path length in cm along each "
                         "ray, float16, unwindowed. This is the input a physics noise model needs; the "
                         "bone render cannot serve because it has no soft tissue and so no realistic "
                         "photon budget and nothing to scatter.")
    ap.add_argument("--paths2-only", action="store_true",
                    help="write ONLY path2/<case>.npz holding water_cm and bone_cm with the device cards' definitions "
                         "(water_bone_paths_cm); img/, ann/ and path/ are untouched")
    ap.add_argument("--cases", default=None,
                    help="restrict to these case ids (after --prefix): a comma list or a file with one per line")
    ap.add_argument("--hu-floor", type=float, default=None,
                    help="override the 150 HU bone floor; -200 integrates soft tissue too, "
                         "which looks like a radiograph rather than a bone projection")
    a = ap.parse_args()
    names = SCHEMES[a.scheme]
    if a.hu_floor is not None:
        global HU_FLOOR
        HU_FLOOR = float(a.hu_floor)
        print(f"  HU floor overridden to {HU_FLOOR}")

    src, dst = Path(a.src), Path(a.dst)
    want = None
    if a.cases:
        pc = Path(a.cases)
        want = set(x.strip() for x in (pc.read_text().splitlines() if pc.exists() else a.cases.split(",")) if x.strip())
        print(f"  restricted to {len(want)} cases")
    (dst / "img").mkdir(parents=True, exist_ok=True)
    (dst / "ann").mkdir(parents=True, exist_ok=True)

    labels = sorted(src.glob("scan-*/*_msk.nii.gz"))
    if not labels:                       # fall back to an nnU-Net-style tree
        labels = sorted((src / "labelsTr").glob("*.nii.gz"))
    if a.limit:
        labels = labels[: a.limit]
    print(f"{len(labels)} cases")

    n_ok, n_skip, lvl_hist, overlaps = 0, 0, {}, []
    for i, lp in enumerate(labels, 1):
        if lp.name.endswith("_msk.nii.gz"):
            stem = lp.name[: -len("_msk.nii.gz")].replace("scan-", "")
            ip = lp.parent / lp.name.replace("_msk.nii.gz", "_ct.nii.gz")
        else:
            stem = lp.name[: -len(".nii.gz")]
            ip = src / "imagesTr" / f"{stem}_0000.nii.gz"
            # DATASET813'S IMAGE LINKS ARE CONTAINER PATHS (/data/hf_export/ct/<n>_ct.nii.gz)
            # and dangle on the host. The basename is the only part that survives, and it
            # names the file under the real CT root -- so follow the link one step, keep the
            # name, and look it up there. Never "repair" the links themselves; that has
            # already been done once by mistake and reverted.
            if a.ct_root and ip.is_symlink() and not ip.exists():
                import os as _os
                ip = Path(a.ct_root) / Path(_os.readlink(ip)).name
        stem = a.prefix + stem
        if want is not None and stem not in want:
            continue
        if not ip.exists():
            print(f"  no image for {stem}", file=sys.stderr)
            n_skip += 1
            continue
        if a.respace:
            ap_ = dst / "ann" / f"{stem}.json"
            if not ap_.exists():
                n_skip += 1
                continue
            lim = nib.load(str(lp))
            zp = pir_spacing(lim.header, lim.affine)
            ann = json.load(open(ap_))
            old = ann.get("mm_per_px_row_si_col_ap")
            ann["mm_per_px_row_si_col_ap"] = [zp[1], zp[0]]
            ann["mm_per_px_before_respace"] = ann.get("mm_per_px_before_respace") or old
            json.dump(ann, open(ap_, "w"), indent=1)
            n_ok += 1
            if i % 100 == 0 or i == len(labels):
                print(f"  {i}/{len(labels)}  {stem}: {old} -> {[round(zp[1], 4), round(zp[0], 4)]}")
            continue
        # with --path, an existing ann is not enough to skip: the path file is a second output and an
        # earlier run of this tool did not write one
        _done = ((dst / "path2" / f"{stem}.npz").exists() if a.paths2_only else
                 (dst / "path" / f"{stem}.npy").exists() if a.path_only
                 else ((dst / "ann" / f"{stem}.json").exists()
                       and (not a.path or (dst / "path" / f"{stem}.npy").exists())))
        if a.resume and _done:
            n_ok += 1
            continue
        # A TRUNCATED GZIP COSTS ONE CASE, NOT THE JOB. The first pass over CTSpinoPelvic1K
        # died at case 303 of 802 on "Compressed file ended before the end-of-stream marker"
        # -- one damaged .nii.gz in the canonical CT copy -- and took the other 499 with it.
        # The damaged file is named to stderr so it can be fixed at the source, and the run
        # goes on.
        try:
            lim = nib.load(str(lp))
            gt = np.asanyarray(lim.dataobj).astype(np.int16)
            ct = np.asanyarray(nib.load(str(ip)).dataobj).astype(np.float32)
        except (EOFError, OSError, ValueError) as e:
            print(f"  UNREADABLE {stem}: {ip.name}: {type(e).__name__}: {e}", file=sys.stderr)
            n_skip += 1
            continue
        if ct.shape != gt.shape:
            print(f"  shape mismatch {stem}: {ct.shape} vs {gt.shape}", file=sys.stderr)
            n_skip += 1
            continue
        ct_p = to_pir(ct, lim.affine)
        if a.paths2_only:
            (dst / "path2").mkdir(parents=True, exist_ok=True)
            zp = pir_spacing(lim.header, lim.affine)
            wcm, bcm = water_bone_paths_cm(ct_p, zp[2])
            np.savez_compressed(dst / "path2" / f"{stem}.npz", water_cm=wcm.astype(np.float16), bone_cm=bcm.astype(np.float16))
            print(f"  {stem}: water p50 {np.percentile(wcm, 50):.1f} cm, bone p99 {np.percentile(bcm, 99):.2f} cm", flush=True)
            n_ok += 1
            continue
        if a.path_only:
            (dst / "path").mkdir(parents=True, exist_ok=True)
            zp = pir_spacing(lim.header, lim.affine)
            np.save(dst / "path" / f"{stem}.npy",
                    water_path_cm(ct_p, zp[2]).astype(np.float16))
            n_ok += 1
            continue
        gt_p = to_pir(gt, lim.affine)
        img = drr(ct_p)
        levels, ov, un = project_labels(gt_p, names)
        if not levels:
            n_skip += 1
            continue
        # the box convention: body if a SPINEPS body mask exists for this case, whole vertebra otherwise
        convention, n_body = "outline", 0
        bm = body_mask_for(stem, a.body_mask_dir, gt.shape, ct_affine=lim.affine)
        if bm is not None:
            body_p = to_pir(bm[0], lim.affine)                  # same grid as the label (shape AND affine checked)
            bb = body_boxes(body_p, names, SCHEMES["verse"])
            for cid, rec in levels.items():
                if cid in bb:
                    rec["outline_box"] = rec["box"]
                    rec["outline_pixels"] = rec["pixels"]
                    rec["box"] = bb[cid]["box"]
                    rec["pixels"] = bb[cid]["pixels"]
                    rec["centroid"] = bb[cid]["centroid"]
                    rec["box_convention"] = "body"
                    n_body += 1
                else:
                    rec["box_convention"] = "outline"       # no body for this level: said, not guessed
            convention = "body" if n_body else "outline"

        np.save(dst / "img" / f"{stem}.npy", (img * 255).astype(np.uint8))
        zp = pir_spacing(lim.header, lim.affine)
        if a.path:
            (dst / "path").mkdir(parents=True, exist_ok=True)
            # zp is [col_ap, row_si, lr] after pir_spacing; the projection runs along left-right
            wp = water_path_cm(ct_p, zp[2])
            np.save(dst / "path" / f"{stem}.npy", wp.astype(np.float16))
        ann = {
            "case": stem,
            "shape": list(img.shape),
            "axcodes": "".join(nib.aff2axcodes(lim.affine)),
            # mm per pixel in the projected plane (rows S-I, cols A-P), so a crop can be expressed in mm
            "mm_per_px_row_si_col_ap": [zp[1], zp[0]],
            "levels": {str(k): v for k, v in levels.items()},
            "overlap_px": ov, "union_px": un,
            "box_convention": convention,
            "n_levels_with_body_box": n_body,
        }
        if a.path:
            ann["water_path_cm_p50_p99"] = [round(float(np.percentile(wp, 50)), 2),
                                            round(float(np.percentile(wp, 99)), 2)]
        json.dump(ann, open(dst / "ann" / f"{stem}.json", "w"), indent=1)
        if a.png:
            try:
                from PIL import Image
                Image.fromarray((img * 255).astype(np.uint8)).save(dst / "img" / f"{stem}.png")
            except ImportError:
                pass
        for k in levels:
            lvl_hist[names[k]] = lvl_hist.get(names[k], 0) + 1
        overlaps.append(ov / max(un, 1))
        n_ok += 1
        if i % 25 == 0 or i == len(labels):
            print(f"  {i}/{len(labels)}")

    print(f"\nwrote {n_ok} DRRs, skipped {n_skip}")
    print("levels present, by case count:")
    for k in sorted(lvl_hist, key=lambda n: LEVEL_ORDER.index(n) if n in LEVEL_ORDER else 99):
        print(f"   {k:<8} {lvl_hist[k]:>4}")
    if overlaps:
        o = np.array(overlaps)
        print(f"\nsilhouette overlap between vertebrae: median {np.median(o):.3%}  "
              f"p95 {np.percentile(o,95):.3%}  max {o.max():.3%}")
        print("  (a pixel claimed by two levels is ambiguity a 2-D classifier inherits)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
