# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/sweep_map.py [tracked at 097933a]
"""Serial sweep: a virtual full-spine map from overlapping C-arm frames, and limited-field frames named against it.

WHY. A single limited-field frame names its vertebrae from shape alone, and on transitional spines that is
where the errors live (docs/FEASIBILITY_REPRODUCE.md). The surgeon's own remedy is to count from a landmark,
one fluoroscopic shot at a time, from the sacrum upward. This tool automates that remedy without a CT: the
radiographer takes an ordered series of overlapping frames from the sacrum (or from C2) to the level of
interest, the frames are linked into one chain of vertebrae, the chain is named twice -- by counting from the
anchor and by the morphology model with the whole chain as context -- and every later limited-field frame is
registered onto the swept frames and takes its names from the chain. The count and the shape reading disagree
exactly when the spine is transitional, and that disagreement is surfaced as the flag, not hidden by either.

WHAT IS SIMULATED, AND WHAT IS NOT. Real serial sweeps of one patient do not exist in any public collection,
so a sweep is cut from one long labelled image: a CT render (T10 to sacrum, or the whole spine) or a real film
that reaches the sacrum. Each frame is a window of a stated physical span, cut with a jittered step, and each
frame is degraded independently (gain, offset, gamma, the fitted film-noise model, a small rotation and scale)
so that no two frames share pixels exactly. What this cannot simulate is parallax between exposures and
patient motion between them; both make the LINKING harder and change nothing about the naming, and the
linking is scored separately so a reader can see how much of the result rests on it.

HOW FRAMES ARE LINKED. The column is periodic, so an unconstrained image correlation between two frames can
lock one body off (it did, in the first version of this tool). The protocol fixes the step -- the field is a
known size and the radiographer is told how far to move -- so the translation between consecutive frames is
searched by normalised cross-correlation only within ±0.6 body of the expected step. The shared bodies then
follow from the translation: an upper-frame body whose predicted position lands on a lower-frame body is the
same body. The encoder's embeddings are compared for every pair as a check, and the pairing the embeddings
alone would have chosen is recorded beside the one used.

WHAT THE RENDERED PANORAMAS SHOW, AND ONE THING THEY SHOW THAT THE NUMBERS DO NOT. Every arm writes a contact
sheet of stitched sweeps with the frame boundaries and every vertebra box drawn, and looking at them settled
something the summary could not: on some spines consecutive frames share NO whole vertebra and the chain is
still complete, because the correlation locks the shift from the partial bodies at the seam. That is a real
capability of the linker and a real fragility of the protocol -- it is exactly the case a parallax or a patient
movement would break, and it is why the protocol asks for a body of overlap rather than relying on it.

HOW A QUERY FRAME IS MAPPED. The swept frames are stitched into one panorama with the estimated shifts, and
every chain node's box is placed on it. The later limited-field frame is registered to the panorama by
normalised cross-correlation over a small scale range -- a frame that straddles two swept frames, which most
do, still finds itself -- and its boxes land on node boxes. Embedding matching is kept as the fallback when
nothing correlates, and both offsets are recorded so the two can be compared.

THE FRAME SPAN IS PHYSICAL, NOT A NUMBER OF VERTEBRAE. Nominal receptor size overstates the usable field:
GE's 510(k) K170752 gives 215 mm usable for a 9-inch intensifier and 287 mm for a 12-inch, which is 94% of
nominal, and flat panels are not all 30 cm square -- the GE OEC Elite panel is 21 or 31 cm, Siemens' is
295-298 mm active, Philips' 301 mm. Source-to-image distance is FIXED on every mobile C-arm whose maker
states it, near 100 cm (GE), 98-116 cm across the fleet.

Magnification is the term that sets the span at the spine, and it is measured: 1.2 to 1.6 on intraoperative
fluoroscopy of the PRONE spine with a 9-inch intensifier, projecting four to five vertebral levels (Naik
2022, PMID 35680729). That band is corroborated from the other side by measuring our own CTs: with a lateral
skin-to-body-centroid depth near 15 cm and a 5 cm air gap at 100 cm SID, magnification runs 1.22 to 1.34
across patients, and the upper end of Naik's band needs the 15-25 cm air gap that open spine surgery forces.

So a 9-inch field at the spine is 134 mm at M=1.6 and 179 mm at M=1.2. THE PRESETS BELOW SIT AT THE
SMALL-FIELD END: ii9=140 implies M=1.54, ii12=190 implies 1.51, fpd30=200 implies 1.48. That is the hardest
case, not the typical one -- at M=1.30 they would be 165, 221 and 227 mm -- and it is a deliberate choice,
not an estimate. slurm/geometry_sweep.sh sweeps 95 to 240 mm so no result depends on it.

An earlier version of this comment attributed all of the above to Boduch 2017. That paper is a study of
paediatric femoral fracture shortening on sawbones; it contains no spine, no receptor diameter, no
source-to-image distance and no field at depth, and it supported none of it. It does support one thing worth
keeping: a coin at 0, 20 and 80 mm above the receptor read 31, 33 and 35 mm, an 11% change in image scale
for 80 mm of movement along the beam. That is an external check on the geometry used here, because
dM/M = dz/(SOD-dz) predicts 11.1% for the same displacement.

WHAT A DECLINE COSTS, MEASURED. Reporting an accuracy at a coverage invites the objection that the system is
buying its number by refusing the hard cases. So every query frame is also re-taken: the same vertebrae shot
again from a slightly different height, as a radiographer would if told "I cannot place this one, move and
shoot again". The retake is scored exactly like the original, and the pair answers the clinical question --
does a decline cost one more exposure, or does it cost the level?

WHICH ALPHABET, AND WHEN TO SAY NOTHING. The chain is decoded against four alphabets -- ordinary, with a
thirteenth rib-bearing level, with a sixth lumbar vertebra, and with both -- and the decode returns which one
it chose and by how much it beat the best ordinary one. That margin is the variant call, and it is a call the
whole chain supports and a single frame cannot. Every named vertebra also carries the probability the head
gave the name it received, so accuracy can be reported at a stated coverage: a system that must be right 99%
of the time is allowed to decline, and what it declines is measured rather than hidden.

    python tools/sweep_map.py --drr ~/ctsp_drr --classes ~/model_night/anomaly_manifest/spine_classes.json \\
        --model ~/model_night/runs/model_r18_ce_v3.pt --head ~/model_night/heads_mixed/head_r18_ce_v3_prod.pt \\
        --span ii9 --overlap 1 --boxes gt --perturb film --out ~/model_night/sweep/ctsp_ii9_o1_gt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eval_gate as EG  # noqa: E402
from make_context_crops import LEVEL_ORDER  # noqa: E402

REGION = {**{f"C{i}": "cervical" for i in range(1, 8)}, **{f"T{i}": "thoracic" for i in range(1, 14)},
          **{f"L{i}": "lumbar" for i in range(1, 7)}, "sacrum": "sacral"}
# body-plus-disc pitch along the column, mm. Lumbar body ~25-27 mm (Frontiers Physiol. 2026 CT series) plus
# disc 6-9 mm (Zhou 2018); thoracic body ~20-24 mm plus disc ~5 (Panjabi 1991); cervical body ~14-15 plus disc 5.
PITCH_MM = {"cervical": 19.0, "thoracic": 27.0, "lumbar": 34.0, "sacral": 34.0}
SPAN_PRESETS = {"collimated": 100.0, "ii9": 140.0, "ii12": 190.0, "fpd30": 200.0}
NORMAL = [f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)] + [f"L{i}" for i in range(1, 6)] + ["sacrum"]
ORD = {n: i for i, n in enumerate(LEVEL_ORDER)}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ----------------------------------------------------------------------------------------------------------
# spines
# ----------------------------------------------------------------------------------------------------------
def load_spine(ann_path: Path, img_dir: Path):
    j = json.load(open(ann_path))
    case = j["case"]
    img_p = img_dir / f"{case}.npy"
    if not img_p.exists():
        cands = list(img_dir.glob(f"{case}.*"))
        if not cands:
            return None
        img_p = cands[0]
    if img_p.suffix == ".npy":
        a = np.load(img_p)
    else:
        from PIL import Image
        a = np.asarray(Image.open(img_p).convert("L"))
    if a.ndim == 3:
        a = a[..., 0]
    if a.dtype != np.uint8:
        lo, hi = np.percentile(a, 0.5), np.percentile(a, 99.5)
        a = (np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1) * 255).astype(np.uint8)
    boxes = []
    for k, v in j.get("levels", {}).items():
        name = v.get("name")
        b = v.get("box")
        if name in ORD and b and len(b) == 4:
            boxes.append((name, [int(b[0]), int(b[1]), int(b[2]), int(b[3])]))
    boxes.sort(key=lambda nb: (nb[1][1] + nb[1][3]) / 2.0)
    names = [n for n, _ in boxes]
    if len(names) != len(set(names)) or len(names) < 4:
        return None
    mm = j.get("mm_per_px_row_si_col_ap")
    mm_per_px = float(mm[0]) if (mm and mm[0]) else None
    # the COLUMN spacing was being discarded. Nothing in the counting uses it -- every measurement runs
    # along rows -- but a figure that draws the frame without it stretches the anatomy by up to 29 % on
    # this corpus, so it is carried here rather than re-read from the annotation by each consumer.
    mm_per_px_col = float(mm[1]) if (mm and len(mm) > 1 and mm[1]) else None
    # rib-bearing truth per box (tools/rib_bearing_ann.py): True / False, or None when the ann has no
    # rib labels at all (VerSe, films), in which case the rib term is silent for that spine
    rb = j.get("rib_bearing")
    rib = [None] * len(boxes)
    if isinstance(rb, dict):
        rib = [(bool(rb[n]["left"] or rb[n]["right"]) if n in rb else False) if n != "sacrum" else False
               for n, _ in boxes]
    # the water-equivalent path map, when the corpus has one (make_drr_dataset --path-only). It is the
    # input --perturb physics needs; without it that mode has nothing to render and says so.
    wp = None
    bp = None
    # PREFER THE PAIR. path2/<case>.npz holds water and bone line integrals under the definitions the device
    # cards were fitted with (make_drr_dataset --paths2-only); path/<case>.npy is the older MERGED density path,
    # which carries bone only as extra density and no bone spectrum.
    pp2 = img_dir.parent / "path2" / f"{case}.npz"
    if pp2.exists():
        try:
            z2 = np.load(pp2)
            w2 = z2["water_cm"].astype(np.float32); b2 = z2["bone_cm"].astype(np.float32)
            if w2.shape == a.shape and b2.shape == a.shape:
                wp, bp = w2, b2
        except Exception:
            wp = bp = None
    pp = img_dir.parent / "path" / f"{case}.npy"
    if wp is None and pp.exists():
        try:
            wp = np.load(pp).astype(np.float32)
            if wp.shape != a.shape:
                wp = None
        except Exception:
            wp = None
    return {"case": case, "img": a, "boxes": boxes, "mm_per_px": mm_per_px,
            "mm_per_px_col": mm_per_px_col, "source": j.get("source", ""),
            "pseudo": bool(j.get("pseudo_label", False)), "rib": rib, "path_cm": wp, "bone_cm": bp}


def body_pitch_px(spine):
    """Median centre-to-centre distance between adjacent non-sacral bodies, and the px-per-mm it implies."""
    cs = [((b[1] + b[3]) / 2.0, REGION[n]) for n, b in spine["boxes"] if n != "sacrum"]
    pitches, ratios = [], []
    for (y0, r0), (y1, r1) in zip(cs[:-1], cs[1:]):
        d = y1 - y0
        if d > 0:
            pitches.append(d)
            ratios.append(d / PITCH_MM[r0])
    if not pitches:
        return None, None
    if spine["mm_per_px"]:
        return float(np.median(pitches)), 1.0 / spine["mm_per_px"]
    return float(np.median(pitches)), float(np.median(ratios))


def sacrum_part(spine):
    """The sacrum as a frame sees it: the S1 body region, one lumbar body tall, at the top of the sacral box.

    The render's sacral box covers the whole sacrum (about 15 cm); the detector, and the films' own annotations,
    box the S1 body. A station that ends at the promontory shows the S1 body, not the coccyx, so the anchor box
    used here is the top of the sacral box, as tall as the body above it.
    """
    names = [n for n, _ in spine["boxes"]]
    if "sacrum" not in names:
        return None
    i = names.index("sacrum")
    sb = spine["boxes"][i][1]
    above = spine["boxes"][i - 1][1] if i > 0 else None
    h = int(round(1.1 * (above[3] - above[1]))) if above else int(round((sb[3] - sb[1]) * 0.3))
    return [sb[0], sb[1], sb[2], min(sb[3], sb[1] + h)]


# ----------------------------------------------------------------------------------------------------------
# frames
# ----------------------------------------------------------------------------------------------------------
def _exposed_frac(b, mask, H, W):
    """Fraction of a box's area the receptor actually lit."""
    x0 = int(max(0, min(W, round(b[0])))); x1 = int(max(0, min(W, round(b[2]))))
    y0 = int(max(0, min(H, round(b[1])))); y1 = int(max(0, min(H, round(b[3]))))
    if x1 - x0 < 1 or y1 - y0 < 1:
        return 0.0
    return float(mask[y0:y1, x0:x1].mean())


def field_mask(shape):
    """Which pixels the receptor and collimator actually expose. None when the whole frame is exposed."""
    if FIELD_STOP == "none":
        return None
    h, w = shape[:2]
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    if FIELD_STOP == "circle":
        return np.hypot((yy - cy) / max(cy, 1), (xx - cx) / max(cx, 1)) <= FIELD_OPEN
    return (np.abs(yy - cy) <= FIELD_OPEN * cy) & (np.abs(xx - cx) <= FIELD_OPEN * cx)


def apply_field_stop(a):
    """Blank whatever the receptor and collimator do not expose.

    A round tube gives a disc inside a square readout; a flat panel gives the square itself, stopped
    down by the collimator. The unexposed region is genuinely part of a C-arm frame and a linker has to
    cope with it, so it is not a border to be cropped away.
    """
    keep = field_mask(a.shape)
    if keep is None:
        return a
    return np.where(keep, a, 0).astype(a.dtype)


def perturb_frame(img: np.ndarray, boxes: list, rng, mode: str, film_params,
                  path_cm=None, px_mm=None, bone_cm=None):
    """Independent degradation of one frame: gain, offset, gamma, film noise, small rotation and scale.

    Boxes follow the geometric part (rotation about the frame centre, isotropic scale) as the bounding box of
    their transformed corners. `mode` none|photometric|film.
    """
    from PIL import Image
    if mode == "physics":
        # Render this station from the water-equivalent path, independently of every other station:
        # its own exposure, scatter, heel direction and noise, the way two separate pedal presses
        # differ. A shared degradation would prove nothing about linking.
        if path_cm is None:
            raise ValueError("--perturb physics needs a path map; run make_drr_dataset --path-only "
                             "on this corpus first")
        import fluoro_physics as FPHYS
        recept = PHYSICS_RECEPTOR
        if recept == "mix":
            if FIELD_STOP == "circle":
                # An arm that asks for a disc gets the receptor that HAS one. The field shape under
                # physics comes from the RECEPTOR, not from FIELD_STOP, so a mixed draw hands a
                # circle-labelled arm two thirds square frames -- and lets the two frames of one link
                # carry differently shaped stops, which no mask can repair.
                recept = "ii"
            else:
                # NO SILENT FALLBACK. This read `rng.randint(3) if hasattr(rng, "randint") else 0`, so
                # a Generator (which has no randint) pinned every frame to "ii" while a RandomState
                # mixed, under identical flags. The probe used one and the walk the other.
                recept = ("ii", "cmos", "fpd")[int(rng.randint(3))]
        # The stop comes BACK from the render. Recomputing it here from the module globals is what
        # made masked correlation a no-op under physics: the render draws its collimation, so the
        # recomputed disc was not the disc that was exposed.
        out, nb, rec, stop = FPHYS.render(
            path_cm, rng, boxes=list(boxes), px_mm=(float(px_mm) if px_mm else None),
            receptor=recept, bone_cm=bone_cm,
            grid=PHYSICS_GRID, return_mask=True, exposure_scale=EXPOSURE_SCALE,
            collimation=(FIELD_OPEN if FIELD_STOP != "none" else None))
        rec = dict(rec); rec["_mask"] = stop
        return out, [[int(round(v)) for v in b] for b in nb], rec
    a = img.astype(np.float32) / 255.0
    rec = {}
    if mode != "none":
        g = float(rng.uniform(0.8, 1.2)); o = float(rng.uniform(-0.08, 0.08)); gam = float(np.exp(rng.uniform(-0.25, 0.25)))
        a = np.clip(np.clip(a * g + o, 0, 1) ** gam, 0, 1)
        rec.update({"gain": round(g, 3), "offset": round(o, 3), "gamma": round(gam, 3)})
        ang = float(rng.uniform(-ROT_JITTER, ROT_JITTER))
        sc = float(np.exp(rng.uniform(-MAG_JITTER, MAG_JITTER))) if MAG_JITTER > 0 else 1.0
        H, W = a.shape
        im = Image.fromarray((a * 255).astype(np.uint8))
        im = im.rotate(ang, resample=Image.BILINEAR, center=(W / 2.0, H / 2.0))
        nw, nh = max(1, int(round(W * sc))), max(1, int(round(H * sc)))
        im = im.resize((nw, nh), Image.BILINEAR)
        a = np.asarray(im).astype(np.float32) / 255.0
        th = np.deg2rad(-ang)   # PIL rotates counter-clockwise for positive angles in image coordinates
        c, s = np.cos(th), np.sin(th)
        nb = []
        for b in boxes:
            pts = np.array([[b[0], b[1]], [b[2], b[1]], [b[0], b[3]], [b[2], b[3]]], np.float64)
            pts -= [W / 2.0, H / 2.0]
            rot = np.stack([c * pts[:, 0] - s * pts[:, 1], s * pts[:, 0] + c * pts[:, 1]], 1)
            rot += [W / 2.0, H / 2.0]
            rot *= sc
            nb.append([int(round(rot[:, 0].min())), int(round(rot[:, 1].min())), int(round(rot[:, 0].max())), int(round(rot[:, 1].max()))])
        boxes = nb
        rec.update({"rot_deg": round(ang, 2), "scale": round(sc, 3)})
    if mode == "film":
        from film_match_augment import film_match
        u8 = (a * 255).astype(np.uint8)
        a = film_match(u8, rng, film_params).astype(np.float32) / 255.0
        rec["film_noise"] = True
    return apply_field_stop((a * 255).astype(np.uint8)), boxes, rec


def _crop_path(spine, y0, y1, x0, x1, which="path_cm"):
    """The water- (or bone-) path crop matching a frame, or None when the corpus has no such map."""
    wp = spine.get(which)
    if wp is None:
        return None
    return wp[int(y0):int(y1), int(x0):int(x1)]


def cut_frame(spine, y0, y1, x0, x1, pitch_px, rng, perturb, film_params, band=0.3):
    """One exposure: rows y0..y1, columns x0..x1 of the long image.

    A body is IN the frame when the middle of its pitch (its centre ± band pitches) lies inside the rows: the
    render's label boxes are taller than the pitch because they carry the posterior elements, so a rule on the
    box's own height would admit a neighbour whose body is outside. Every box is carried in frame coordinates
    as well (all_boxes), so a detector box on a body the rule excluded is scored against the truth, not called
    a false positive.
    """
    img = spine["img"]
    H, W = img.shape
    y0, y1 = max(0, int(y0)), min(H, int(y1)); x0, x1 = max(0, int(x0)), min(W, int(x1))
    crop = img[y0:y1, x0:x1]
    all_boxes, all_idx, keep = [], [], []
    for gi, (name, b) in enumerate(spine["boxes"]):
        bb = b if name != "sacrum" else spine["_sacrum_part"]
        cy = (bb[1] + bb[3]) / 2.0
        all_boxes.append([bb[0] - x0, bb[1] - y0, bb[2] - x0, bb[3] - y0]); all_idx.append(gi)
        keep.append((cy - band * pitch_px) >= y0 and (cy + band * pitch_px) <= y1)
    crop, all_boxes, prec = perturb_frame(crop, all_boxes, rng, perturb, film_params,
                                          path_cm=_crop_path(spine, y0, y1, x0, x1),
                                          bone_cm=_crop_path(spine, y0, y1, x0, x1, "bone_cm"),
                                          px_mm=spine.get("mm_per_px"))
    # What the receptor actually exposed, carried explicitly: a real exposed pixel can window to zero,
    # so inferring the mask from zeros would quietly discard anatomy. The renderer hands back its own
    # stop when it made one; recomputing it here is what made masked correlation a no-op under physics.
    mask = prec.pop("_mask", None) if isinstance(prec, dict) else None
    if mask is None:
        mask = field_mask(crop.shape)
    # A VERTEBRA THE RECEPTOR NEVER EXPOSED IS NOT IN THE FRAME. The row rule above was written for a
    # filled square. With a disc, a box near the top or bottom but off to one side sits in a blanked
    # corner, and counting it puts a node in the chain with no image behind it -- which is a miscount.
    if mask is not None:
        H, W = crop.shape[:2]
        keep = [k and _exposed_frac(b, mask, H, W) >= MIN_EXPOSED for b, k in zip(all_boxes, keep)]
    boxes = [b for b, k in zip(all_boxes, keep) if k]; idxs = [g for g, k in zip(all_idx, keep) if k]
    st = {"img": crop, "boxes": boxes, "gt_idx": idxs, "all_boxes": all_boxes, "all_idx": all_idx,
          "y0": y0, "y1": y1, "x0": x0, "x1": x1, "perturb": prec, "mask": mask}
    # where the spine is in this frame, so the correlation can be confined to it. Taken from the boxes
    # the detector has already produced -- the same boxes the link is about -- and not from the truth.
    bb = boxes or all_boxes
    st["spine_cx"] = float(np.median([(b[0] + b[2]) / 2.0 for b in bb])) if bb else None
    if ERODE_MASK > 0 and mask is not None:
        st["mask_ncc"] = erode_mask(mask, int(round(ERODE_MASK * pitch_px)))
    if PREFILTER == "highpass":
        st["img_hp"] = highpass(crop, pitch_px, mask)
    elif PREFILTER == "grady":
        st["img_hp"] = grad_y(crop)
    elif PREFILTER == "colmean":
        st["img_hp"] = col_demean(crop, mask)
    elif PREFILTER == "colmean+grady":
        st["img_hp"] = grad_y(col_demean(crop, mask))
    elif PREFILTER == "colmean+detrend":
        st["img_hp"] = detrend_y(col_demean(crop, mask), mask)
    elif PREFILTER == "detrend":
        st["img_hp"] = detrend_y(np.asarray(crop, np.float32), mask)
    return st


# THE DEFAULTS ARE THE PROTOCOL. They used to be "clamp" and "protocol", which is a configuration
# nothing publishes: fiducial_walk overrides both on every run and make_count_figures sets them by hand,
# so the only code that ever saw the old defaults was code that had forgotten to set them. link_probe
# forgot, and measured a clamped final frame all day against a protocol that skips it.
END_RULE = "skip"      # "clamp": a final frame that would move less than half a body is SHORTENED
                       # rather than skipped, which makes a large share of all links move less than
                       # commanded and is why the search would then need its asymmetric upper bound
TIGHT_WINDOW = False   # enforce the window the paper describes, |dy - s| <= 0.6 p, on every link
                       # except the last. The default search runs its UPPER bound down to half a
                       # body to admit the shortened final step, and applies that to every link,
                       # which makes the window 2.27 bodies wide instead of 1.20 and lets the
                       # +1-body alias inside. On clean frames the true peak wins anyway; under
                       # physics, where the correlation surface is flat, the alias wins.
LAST_LINK = "open"     # the last link's search window runs down to a zero step. "protocol" holds it
                       # to the commanded step like every other link.


def make_stations(spine, span_px, overlap_bodies, pitch_px, anchor, rng, perturb, film_params, step_jitter=0.3):
    """The radiographer's sweep: frames of span_px rows, each overlapping the last by about overlap_bodies.

    The last frame is a whole frame: when the requested step would run off the image it is shortened, which is
    what the radiographer does at the end of the anatomy, and the linker's search allows a short step.
    """
    H, W = spine["img"].shape
    boxes = [b for _, b in spine["boxes"]]
    xs = [(b[0] + b[2]) / 2.0 for b in boxes]
    cx = float(np.median(xs))
    x0, x1 = cx - span_px / 2.0, cx + span_px / 2.0
    stations = []
    top_of_stack = min(b[1] for b in boxes) - 0.15 * pitch_px
    bottom_of_stack = max(b[3] for b in boxes) + 0.15 * pitch_px
    if anchor == "caudal":
        sp = spine["_sacrum_part"]
        y1 = sp[3] + 0.2 * pitch_px
        while True:
            y0 = y1 - span_px
            if y0 < 0:
                y0, y1 = 0, min(H, span_px)
            # THE END OF THE SWEEP. Clamping the last frame to the top of the scan shortens its step to
            # whatever is left, which on a fixed-step sweep was 0.13 body on one spine: a frame nobody
            # would take, and one the linker cannot represent. Under "skip" such a frame is not taken.
            if stations and END_RULE == "skip" and (stations[-1]["y0"] - y0) < 0.5 * pitch_px:
                break
            st = cut_frame(spine, y0, y1, x0, x1, pitch_px, rng, perturb, film_params)
            st["y0"], st["y1"] = float(y0), float(y1)
            st["step_actual"] = float(stations[-1]["y0"] - y0) if stations else None
            stations.append(st)
            if y0 <= top_of_stack or y0 <= 0:
                break
            step = span_px - (overlap_bodies + rng.uniform(-step_jitter, step_jitter)) * pitch_px
            y1 = y1 - max(step, 0.5 * pitch_px)
    else:
        y0 = top_of_stack
        while True:
            y1 = y0 + span_px
            if y1 > H:
                y1, y0 = H, max(0, H - span_px)
            if stations and END_RULE == "skip" and (y1 - stations[-1]["y1"]) < 0.5 * pitch_px:
                break
            st = cut_frame(spine, y0, y1, x0, x1, pitch_px, rng, perturb, film_params)
            st["y0"], st["y1"] = float(y0), float(y1)
            st["step_actual"] = float(y1 - stations[-1]["y1"]) if stations else None
            stations.append(st)
            if y1 >= bottom_of_stack or y1 >= H:
                break
            step = span_px - (overlap_bodies + rng.uniform(-step_jitter, step_jitter)) * pitch_px
            y0 = y0 + max(step, 0.5 * pitch_px)
        stations = stations[::-1]      # stored bottom-most first, like a caudal sweep, so linking code is one path
    return stations


def cut_query(spine, s, K, pitch_px, rng, perturb, film_params, shift=0.0):
    """One limited-field frame over bodies s..s+K-1, optionally shifted by `shift` vertebral pitches.

    A shift is what a retake is: the same anatomy photographed from a slightly different height, so the frame
    holds the same bodies with different amounts of their neighbours at the edges, a different noise draw and
    a different small rotation. It is not a second look at the same pixels.
    """
    boxes = spine["boxes"]
    cs = [(b[1] + b[3]) / 2.0 if n_ != "sacrum" else (spine["_sacrum_part"][1] + spine["_sacrum_part"][3]) / 2.0
          for n_, b in boxes]
    off = shift * pitch_px
    y0 = (cs[s - 1] + cs[s]) / 2.0 + off
    y1 = (cs[s + K - 1] + cs[s + K]) / 2.0 + off
    xs = [(b[0] + b[2]) / 2.0 for _, b in boxes]
    cx = float(np.median(xs))
    w = max(y1 - y0, 2.5 * pitch_px)
    fr = cut_frame(spine, y0, y1, cx - w / 2.0, cx + w / 2.0, pitch_px, rng, perturb, film_params)
    fr["start"] = int(s); fr["K"] = int(K); fr["shift"] = float(shift)
    return fr


def make_queries(spine, K, n, pitch_px, rng, perturb, film_params, margin=1):
    """Interior limited-field frames of exactly K whole bodies: from the disc above the first to the disc below
    the last, so K bodies and no partial neighbour; no anchor in view."""
    boxes = spine["boxes"]
    nb = len(boxes)
    cs = [(b[1] + b[3]) / 2.0 if n != "sacrum" else (spine["_sacrum_part"][1] + spine["_sacrum_part"][3]) / 2.0 for n, b in boxes]
    starts = [s for s in range(margin, nb - K - margin + 1) if all(boxes[s + j][0] != "sacrum" for j in range(K))]
    if not starts:
        return []
    out = []
    pick = rng.choice(starts, size=min(n, len(starts)), replace=False)
    xs = [(b[0] + b[2]) / 2.0 for _, b in boxes]
    cx = float(np.median(xs))
    for s in pick:
        y0 = (cs[s - 1] + cs[s]) / 2.0
        y1 = (cs[s + K - 1] + cs[s + K]) / 2.0
        w = max(y1 - y0, 2.5 * pitch_px)
        fr = cut_frame(spine, y0, y1, cx - w / 2.0, cx + w / 2.0, pitch_px, rng, perturb, film_params)
        fr["start"] = int(s); fr["K"] = int(K)
        out.append(fr)
    return out


# ----------------------------------------------------------------------------------------------------------
# models
# ----------------------------------------------------------------------------------------------------------
class Namer:
    """Encoder, detached fc, and the run-level head that was trained on THIS encoder."""

    def __init__(self, model_p, head_p, dev, tta=True):
        import torch
        import torch.nn as nn
        from night_loadmodel import load_level_model, embed_dim
        from recurrent_order import RunLabeller
        self.torch = torch
        self.dev = dev
        self.model, self.spec = load_level_model(model_p, len(LEVEL_ORDER), dev)
        self.fc = self.model.fc; self.model.fc = nn.Identity()
        self.head = None
        self.tta = tta
        self.model_sha = sha(model_p)
        self.head_sha = None
        if head_p:
            side = Path(str(head_p).replace(".pt", "") + ".arch.json")
            hmeta = json.load(open(side)) if side.exists() else {}
            base = hmeta.get("base_model")
            if base and Path(base).exists() and sha(base) != self.model_sha:
                raise SystemExit(f"head {Path(head_p).name} was trained on {Path(base).name}, not on {Path(model_p).name}")
            d_in = embed_dim(self.fc, self.spec)
            self.head = RunLabeller(d_in, len(LEVEL_ORDER)).to(dev)
            self.head.load_state_dict(torch.load(head_p, map_location=dev)); self.head.eval()
            self.head_sha = sha(head_p)

    def load_roles(self, role_p):
        """Attach the transition-role head, if it was trained on THIS encoder.

        The role head predicts what a vertebra is -- last thoracic, first lumbar, last presacral -- rather
        than what it is called, and it is the second opinion the alphabet decode uses at the junctions. Like
        the run-level head it reads this encoder's embeddings and nothing else, so the pairing is checked by
        hash and a mismatch is refused rather than warned about.
        """
        import torch.nn as nn
        side = Path(str(role_p).replace(".pt", "") + ".role.json")
        meta = json.load(open(side)) if side.exists() else {}
        base = meta.get("base_model")
        if base and Path(base).exists() and sha(base) != self.model_sha:
            raise SystemExit(f"role head {Path(role_p).name} was trained on {Path(base).name}, not this encoder")
        d_in = int(meta.get("d_in") or 512)
        self.roles = meta.get("roles") or ["other", "last_thoracic", "first_lumbar", "last_presacral"]
        net = nn.Sequential(nn.Linear(d_in, 256), nn.GELU(), nn.Dropout(0.2), nn.Linear(256, len(self.roles)))
        net.load_state_dict(self.torch.load(role_p, map_location=self.dev)); net.to(self.dev).eval()
        self.role_net = net
        self.role_sha = sha(role_p)
        self.role_meta = meta

    def role_probs(self, emb):
        torch = self.torch
        if getattr(self, "role_net", None) is None or len(emb) == 0:
            return None
        with torch.no_grad():
            e = torch.from_numpy(np.asarray(emb, np.float32)).to(self.dev)
            return torch.softmax(self.role_net(e), 1).cpu().numpy()

    def head_on(self, emb):
        """The run-level head over ONE window's embeddings, blended with the single-crop posterior.

        This exists because running the head over a whole film and then slicing its output is not a
        limited-field measurement: the head would have seen the bodies outside the window, including the ones
        that touch a landmark. A window's posterior must be computed from that window's embeddings alone.
        """
        torch = self.torch
        if len(emb) == 0:
            return np.zeros((0, len(LEVEL_ORDER)))
        with torch.no_grad():
            e = torch.from_numpy(np.asarray(emb, np.float32)).to(self.dev)
            p1 = torch.softmax(self.fc(e), 1).cpu().numpy()
            if self.head is None:
                return p1
            ph = torch.softmax(self.head(e.unsqueeze(0))[0], 1).cpu().numpy()
        return (p1 + ph) / 2.0

    def run(self, img_u8, boxes, tgt_px=96.0, size=320, rung=1):
        """-> emb (n,d), p_single (n,C), p_blend (n,C) for the boxes of one frame, in the order given."""
        import fluorocap_infer as v1
        torch = self.torch
        if not boxes:
            return np.zeros((0, 1)), np.zeros((0, len(LEVEL_ORDER))), np.zeros((0, len(LEVEL_ORDER)))
        arr = img_u8.astype(np.float32)
        lo, hi = np.percentile(arr, 0.5), np.percentile(arr, 99.5)
        img0 = np.clip((arr - lo) / max(hi - lo, 1e-6), 0, 1)
        variants = [(img0, boxes)]
        if self.tta:
            W = img0.shape[1]
            variants.append((img0[:, ::-1].copy(), [[W - 1 - b[2], b[1], W - 1 - b[0], b[3]] for b in boxes]))
        embs, singles, blends = [], [], []
        with torch.no_grad():
            for img, bx in variants:
                X = torch.from_numpy(v1.crops_for_run(img, bx, tgt_px, size, rung)).float().to(self.dev)
                emb = self.model(X)
                p1 = torch.softmax(self.fc(emb), 1)
                embs.append(emb.cpu().numpy()); singles.append(p1.cpu().numpy()); blends.append(p1.cpu().numpy())
                if self.head is not None:
                    blends.append(torch.softmax(self.head(emb.unsqueeze(0))[0], 1).cpu().numpy())
        return np.mean(embs, 0), np.mean(singles, 0), np.mean(blends, 0)


BODY_CLASSES = ("vertebra", "sacrum", "c2")   # c2 is a body AND the cranial anchor, as sacrum is caudally


def detect_boxes(det, img_u8, imgsz=1024, conf=0.35):
    """Vertebral boxes from either kind of detector, top to bottom.

    A pose model gives keypoints and the box is their extent. A plain detection model has
    res.keypoints None -- and until this branch existed that path returned NO boxes, so every
    detector arm on renders scored "chain complete 0%" for a reason that had nothing to do
    with the detector. For a detection model the boxes are read directly and filtered to
    the body classes BY NAME from the model's own names dict: an anchor detector also boxes
    femoral heads, ribs, implants and skull, none of which is a chain node.
    """
    rgb = np.stack([img_u8] * 3, -1)
    res = det.predict(rgb, imgsz=imgsz, conf=conf, verbose=False)[0]
    boxes = []
    if res.keypoints is not None and len(res.boxes):
        kp = res.keypoints.xy.cpu().numpy()
        for i in np.argsort(kp[:, :, 1].mean(1)):
            pts = kp[i]; b = [int(pts[:, 0].min()), int(pts[:, 1].min()), int(pts[:, 0].max()), int(pts[:, 1].max())]
            if b[2] - b[0] >= 4 and b[3] - b[1] >= 4:
                boxes.append(b)
    elif len(res.boxes):
        names = getattr(det, "names", None) or getattr(res, "names", {}) or {}
        keep = {int(i) for i, n in dict(names).items() if str(n) in BODY_CLASSES}
        xyxy = res.boxes.xyxy.cpu().numpy(); cls = res.boxes.cls.cpu().numpy().astype(int)
        for i in np.argsort((xyxy[:, 1] + xyxy[:, 3]) / 2.0):
            if keep and int(cls[i]) not in keep:
                continue
            b = [int(round(v)) for v in xyxy[i]]
            if b[2] - b[0] >= 4 and b[3] - b[1] >= 4:
                boxes.append(b)
    return boxes


def detect_boxes_with_class(det, img_u8, imgsz=1024, conf=0.35):
    """detect_boxes, but the class name travels with each box.

    A caller that has to find an ANCHOR cannot use position: the lowest box in the field is the lowest
    box, not necessarily the sacrum. A detector that carries a sacrum class already knows which one it is,
    and throwing that away and then assuming the terminal box is the anchor was worth 70 points of
    counting accuracy on the anchor detector's own held-out cases.
    -> (boxes top->bottom, class names in the same order)
    """
    rgb = np.stack([img_u8] * 3, -1)
    res = det.predict(rgb, imgsz=imgsz, conf=conf, verbose=False)[0]
    boxes, kinds = [], []
    names = dict(getattr(det, "names", None) or getattr(res, "names", {}) or {})
    if res.keypoints is not None and len(res.boxes):
        kp = res.keypoints.xy.cpu().numpy()
        cls = res.boxes.cls.cpu().numpy().astype(int) if len(res.boxes) == len(kp) else None
        for i in np.argsort(kp[:, :, 1].mean(1)):
            pts = kp[i]; b = [int(pts[:, 0].min()), int(pts[:, 1].min()), int(pts[:, 0].max()), int(pts[:, 1].max())]
            if b[2] - b[0] >= 4 and b[3] - b[1] >= 4:
                boxes.append(b); kinds.append(str(names.get(int(cls[i]), "vertebra")) if cls is not None else "vertebra")
    elif len(res.boxes):
        keep = {int(i) for i, n in names.items() if str(n) in BODY_CLASSES}
        xyxy = res.boxes.xyxy.cpu().numpy(); cls = res.boxes.cls.cpu().numpy().astype(int)
        for i in np.argsort((xyxy[:, 1] + xyxy[:, 3]) / 2.0):
            if keep and int(cls[i]) not in keep:
                continue
            b = [int(round(v)) for v in xyxy[i]]
            if b[2] - b[0] >= 4 and b[3] - b[1] >= 4:
                boxes.append(b); kinds.append(str(names.get(int(cls[i]), "vertebra")))
    return boxes, kinds


def repair_boxes(boxes, dup_ratio=0.45, gap_ratio=1.55, max_insert=2):
    """Use the chain's LOCAL regularity to merge double-detections and fill single misses.

    Vertebrae in one frame sit in a line at nearly constant spacing, which is a strong prior the detector
    does not get to use: it scores each box alone. Two consequences are repairable without touching the
    model. A pair of boxes far closer together than the local pitch is one vertebra found twice. A pair far
    further apart is a vertebra that was missed, and where it should be is determined by its neighbours.

    WHAT THIS DELIBERATELY DOES NOT DO. It never assumes how many vertebrae there are. That is the trap the
    published BUU baseline fell into -- five fixed per-level classes with exactly one box decoded each
    because "the human spine typically consists of five lumbar vertebrae" -- which makes lumbarization drop
    a vertebra and sacralization put the fifth box on the sacrum, by construction, in precisely the
    population this project exists for. The pitch here is measured from the boxes actually present in this
    frame, so a six-lumbar spine is repaired the same way a five-lumbar one is.

    At most `max_insert` bodies are filled into any one gap: beyond two the spacing estimate is being
    extrapolated further than it can carry, and a run of invented boxes is worse than an honest hole.
    Nothing is extrapolated past the ends of the run -- a missing sacrum at the bottom has no neighbour
    below it to place it from, and guessing there would invent the landmark the whole method anchors on.

    -> (boxes sorted top to bottom, list of bools marking the invented ones)
    """
    if len(boxes) < 3:
        return list(boxes), [False] * len(boxes)
    bs = sorted((list(map(int, b)) for b in boxes), key=lambda b: (b[1] + b[3]) / 2.0)
    cy = [(b[1] + b[3]) / 2.0 for b in bs]
    steps = [cy[i + 1] - cy[i] for i in range(len(cy) - 1)]
    pitch = float(np.median([x for x in steps if x > 0] or [1.0]))
    if pitch <= 0:
        return bs, [False] * len(bs)
    med_h = float(np.median([b[3] - b[1] for b in bs]))
    med_w = float(np.median([b[2] - b[0] for b in bs]))

    # 1. merge a double detection into the union of the pair
    merged, i = [], 0
    while i < len(bs):
        if i + 1 < len(bs) and (cy[i + 1] - cy[i]) < dup_ratio * pitch:
            a, b = bs[i], bs[i + 1]
            merged.append([min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])])
            i += 2
        else:
            merged.append(bs[i]); i += 1
    bs = merged
    cy = [(b[1] + b[3]) / 2.0 for b in bs]

    # 2. fill an interior gap from its two neighbours
    out, made = [bs[0]], [False]
    for k in range(len(bs) - 1):
        gap = cy[k + 1] - cy[k]
        n = int(round(gap / pitch)) - 1
        if gap > gap_ratio * pitch and 1 <= n <= max_insert:
            for j in range(1, n + 1):
                c = cy[k] + gap * j / (n + 1)
                x = ((bs[k][0] + bs[k][2]) / 2.0 + (bs[k + 1][0] + bs[k + 1][2]) / 2.0) / 2.0
                out.append([int(x - med_w / 2), int(c - med_h / 2), int(x + med_w / 2), int(c + med_h / 2)])
                made.append(True)
        out.append(bs[k + 1]); made.append(False)
    return out, made


def assign_gt(det_boxes, gt_boxes, gt_idx):
    """Detector box -> GT index by centre containment, else None (a false positive)."""
    out = []
    for b in det_boxes:
        cy, cx = (b[1] + b[3]) / 2.0, (b[0] + b[2]) / 2.0
        hit = None
        for g, gi in zip(gt_boxes, gt_idx):
            if g[1] <= cy <= g[3] and g[0] <= cx <= g[2]:
                hit = gi; break
        out.append(hit)
    return out


# ----------------------------------------------------------------------------------------------------------
# linking
# ----------------------------------------------------------------------------------------------------------
def erode_mask(m, r):
    """Shrink the exposed region by r pixels, so no correlated pixel is within r of the field stop."""
    if r <= 0:
        return m
    from scipy.ndimage import minimum_filter
    return minimum_filter(np.asarray(m, bool), size=2 * int(r) + 1, mode="constant", cval=False)


def col_demean(a, m=None):
    """Remove the part of the frame that does not vary along the spine axis.

    THIS IS THE ONE THAT FOLLOWS FROM THE DIAGNOSIS. A lateral projection of an abdomen is dominated by
    its anterior-posterior silhouette: air, then the abdominal wall, then the vertebral column, then the
    dorsal muscles, then air again. That profile carries most of the variance in the frame and it is very
    nearly the same at every height, which is exactly why the correlation surface went flat under physics
    -- ncc 0.970 at the peak and a margin of 0.007. A shift-invariant structure correlates with itself at
    every shift. It contributes enormously to the numerator and nothing at all to the discrimination.

    Subtracting each column's own mean deletes it and keeps everything else. Unlike an isotropic
    high-pass, which was refuted at every width because the scatter kernel (about 1.3 bodies) and the
    vertebral periodicity (1 body) are not separable in scale, this separates them by DIRECTION, where
    they genuinely are separable: the nuisance is constant in y and the signal is not. And unlike a
    derivative it removes the nuisance without amplifying the noise, which under a fluoroscopic photon
    budget is the difference that matters.

    The mean must be taken over the EXPOSED pixels only. Averaging the blanked corners of a circular
    field into a column mean puts a ring-shaped artefact into the residual, which is a structure that
    moves with the receptor rather than with the patient -- the one thing correlation must never lock on.
    """
    a = np.asarray(a, np.float32)
    if m is None:
        return a - a.mean(axis=0, keepdims=True)
    m = np.asarray(m, bool)
    n = m.sum(axis=0, keepdims=True).astype(np.float32)
    mu = np.where(n > 0, (a * m).sum(axis=0, keepdims=True) / np.maximum(n, 1), 0.0)
    return (a - mu) * m


def detrend_y(a, m=None, order=2):
    """Remove a slow ramp ALONG the spine axis, which is a separate nuisance from the silhouette.

    col_demean removes any function of x, and the anterior-posterior silhouette is one. It does not
    remove a function of y, and the physics render makes two: the anode heel, whose direction is drawn
    per frame, and the vignette. Both are smooth ramps down the column, both differ between two
    exposures, and a broad mismatched ramp can shift a correlation peak without ever being mistaken for
    anatomy. A low-order polynomial in y is the smallest thing that removes them and cannot represent a
    vertebra: at order two it has no way to express a period of one body over a frame four bodies tall.
    """
    a = np.asarray(a, np.float32)
    h = a.shape[0]
    if h < order + 2:
        return a
    y = (np.arange(h, dtype=np.float32) / max(h - 1, 1)) * 2.0 - 1.0
    if m is None:
        prof = a.mean(axis=1)
        w = np.ones(h, np.float32)
    else:
        m = np.asarray(m, bool)
        cnt = m.sum(axis=1).astype(np.float32)
        prof = np.where(cnt > 0, (a * m).sum(axis=1) / np.maximum(cnt, 1), 0.0)
        w = cnt
    good = w > 0
    if good.sum() < order + 2:
        return a
    V = np.stack([y ** k for k in range(order + 1)], 1)
    sw = np.sqrt(w[good])[:, None]
    coef, *_ = np.linalg.lstsq(V[good] * sw, prof[good] * sw[:, 0], rcond=None)
    return a - (V @ coef)[:, None]


def grad_y(a):
    """Vertical gradient: isolates the ENDPLATES, which is what a reader counts on a lateral film.

    An isotropic high-pass was tried first and refuted at every width from 0.08 to 0.75 of a vertebral
    body: it made the links worse than no filter at all, because the scatter kernel is about 1.3 bodies
    and the vertebral periodicity is at 1, so no isotropic filter separates them.

    A directional derivative is a different instrument. Endplates and cortical margins are near-horizontal
    edges; the soft-tissue background, the scatter haze, the anode heel and the vignette all vary slowly
    along the spine axis. Differentiating down the column keeps the first and removes the others, and it
    does so without needing the two to be separated in scale.
    """
    a = np.asarray(a, np.float32)
    g = np.zeros_like(a)
    g[1:-1, :] = a[2:, :] - a[:-2, :]
    return g


def _blur(a, sig):
    try:
        from scipy.ndimage import gaussian_filter
        return gaussian_filter(np.asarray(a, np.float32), sig, mode="nearest")
    except ImportError:
        import cv2
        k = int(max(3, 2 * round(3 * sig) + 1))
        return cv2.GaussianBlur(np.asarray(a, np.float32), (k, k), sig,
                                borderType=cv2.BORDER_REPLICATE)


def highpass(a, pitch_px, m=None):
    """Subtract a blurred copy: deletes the frequency band the path census measured to be empty.

    Scatter, the heel effect and the vignette are all low frequency, and the mean level carries no
    vertebral periodicity -- a disc space and a vertebral body differ by about one per cent of total
    path. So everything below about a vertebral body in scale is nuisance, and removing it costs no
    signal. It also removes the vignette, which matters more than it looks: the vignette is fixed to the
    RECEPTOR, so it is in the same place in both frames and correlates best where the two field stops
    coincide, which is a pull toward a short step that has nothing to do with the patient.

    THE BLUR IS TAKEN OVER EXPOSED PIXELS ONLY. Blurring across the field stop averages the blanked
    exterior into the interior, so the low-pass copy is pulled dark near the stop and the difference
    carries a bright ring just inside it. That ring is fixed to the receptor too, and it is the strongest
    such structure in the frame: with a plain blur the high-pass arm chose a step 1.64 bodies short, for
    no reason to do with anatomy. Normalising by the blurred mask removes the cause rather than masking
    the symptom, and leaves no radius to tune -- which matters, because the tuned version's bias was set
    by the tuning constant (-0.51, -0.03 and +0.72 of a body at radii of 0.50, 0.75 and 1.00) and
    picking the radius that centres it would be fitting the constant to the answer.
    """
    sig = max(1.0, PREFILTER_BODY * float(pitch_px))
    a = np.asarray(a, np.float32)
    if m is None:
        return a - _blur(a, sig)
    m = np.asarray(m, np.float32)
    num = _blur(a * m, sig)
    den = _blur(m, sig)
    lo = np.where(den > 1e-3, num / np.maximum(den, 1e-6), a)
    return (a - lo) * (m > 0)


def _ncc(a, b, m=None):
    """Normalised cross-correlation, optionally over a mask of jointly exposed pixels."""
    a = a.astype(np.float32).ravel(); b = b.astype(np.float32).ravel()
    if m is not None:
        m = np.asarray(m).ravel()
        # NOT -1.0. A sentinel that is a valid correlation gets ranked against real ones, and the
        # caller cannot tell a shift that correlated badly from one that was never scored.
        if m.sum() < 32:
            return None
        a = a[m]; b = b[m]
    a = a - a.mean(); b = b - b.mean()
    d = float(np.sqrt((a * a).sum() * (b * b).sum()))
    return float((a * b).sum() / d) if d > 0 else -1.0


SHIFT_MODE = "ncc"        # set from --shift; "phase" seeds the search by phase correlation
PLACE_MODE = "template"   # set from --place; "ecc" refines the template peak by ECC alignment


def _ncc_table(L, U, dys, dxs, step_dx, ML=None, MU=None):
    """NCC of the overlap band at every (dy, dx) in the given ranges -> {(dy, dx): ncc}."""
    hL, wL = L.shape; hU, wU = U.shape
    table = {}
    for dy in dys:
        r0 = max(0, -dy); r1 = min(hU, hL - dy)
        if r1 - r0 < 1:
            continue
        for dx in dxs:
            c0 = max(0, -dx); c1 = min(wU, wL - dx)
            if c1 - c0 < 8:
                continue
            v = _ncc(U[r0:r1, c0:c1], L[r0 + dy:r1 + dy, c0 + dx:c1 + dx])
            if v is not None:
                table[(dy, dx)] = v
    return table


def _phase_seed(L, U, prior_dy):
    """Sub-pixel translation of the expected overlap band by phase correlation, or None.

    Fourier phase correlation is what long-length radiograph stitching converged on: O(N log N),
    sub-pixel, and invariant to the per-frame illumination difference that a normalised
    correlation only partly removes. OpenCV's sign convention is not worth trusting under a
    deadline, so BOTH candidate shifts are returned and the NCC refinement keeps the better.
    """
    import cv2
    p = int(round(prior_dy))
    hL, wL = L.shape; hU, wU = U.shape
    r0 = max(0, -p); r1 = min(hU, hL - p)
    if r1 - r0 < 8:
        return None
    w = min(wL, wU)
    A = U[r0:r1, :w].astype(np.float32); B = L[r0 + p:r1 + p, :w].astype(np.float32)
    if A.shape != B.shape or A.size == 0 or A.std() < 1e-3 or B.std() < 1e-3:
        return None
    try:
        win = cv2.createHanningWindow((A.shape[1], A.shape[0]), cv2.CV_32F)
        (sx, sy), resp = cv2.phaseCorrelate(A, B, win)
    except cv2.error:
        return None
    if not np.isfinite(sx) or not np.isfinite(sy):
        return None
    return [(p + int(round(sy)), int(round(sx))), (p - int(round(sy)), -int(round(sx)))], float(resp)


def ncc_shift(lower, upper, prior_dy, pitch_px, step=2, lo=None, hi=None):
    """Translation (dy, dx) of the upper frame relative to the lower one: upper row r sits on lower row r + dy.

    lo/hi override the dy search window (used for the skip links of the global solve, which are
    centred on the sum of two measured steps rather than on the protocol's prior).

    Searched by normalised cross-correlation of the overlap band from 0.6 body beyond the protocol's expected
    step (prior_dy < 0) to a step of half a body, and ±0.3 body sideways. The lower bound is what stops the
    periodic column aliasing by a body on a one-body overlap; the upper bound admits the shortened last step.
    Returns the best shift, its correlation, and the margin over the best shift more than half a body away.
    """
    _pre = PREFILTER != "none"
    L = lower.get("img_hp") if _pre else lower["img"]
    U = upper.get("img_hp") if _pre else upper["img"]
    if L is None or U is None:
        L, U = lower["img"], upper["img"]
    ML = lower.get("mask_ncc", lower.get("mask")) if MASKED_NCC else None
    MU = upper.get("mask_ncc", upper.get("mask")) if MASKED_NCC else None
    if NCC_BAND > 0:
        # cut each frame to a band about its OWN spine, so a lateral offset between the two exposures
        # does not have to be undone before the band can be taken; dx then searches inside the band.
        half = 0.5 * NCC_BAND * pitch_px
        def _cut(A, M, cx):
            if cx is None:
                return A, M
            a0 = int(max(0, round(cx - half))); a1 = int(min(A.shape[1], round(cx + half)))
            if a1 - a0 < 8:
                return A, M
            return A[:, a0:a1], (None if M is None else M[:, a0:a1])
        L, ML = _cut(L, ML, lower.get("spine_cx"))
        U, MU = _cut(U, MU, upper.get("spine_cx"))
    hL, wL = L.shape; hU, wU = U.shape
    best = (None, None, -2.0)
    table = {}
    # LINK_WINDOW widens the search either side of the commanded step. 1.0 is the protocol; larger values
    # exist so the window's contribution can be measured rather than asserted, by letting the periodic
    # column compete the way it would in an implementation that did not restrict the search at all.
    span_dy = int(round(0.6 * LINK_WINDOW * pitch_px)); span_dx = int(round(0.3 * pitch_px))
    dy_lo = int(prior_dy) - span_dy if lo is None else int(lo)
    if hi is not None:
        dy_hi = int(hi)
    elif TIGHT_WINDOW or LINK_WINDOW > 1.0:
        # the window the protocol commands: symmetric about the commanded step. The asymmetric bound
        # below exists for the shortened final frame of a sweep, and build_chain passes `hi` for that
        # link explicitly, so there is no reason for every other link to carry it.
        dy_hi = int(prior_dy) + span_dy
    else:
        dy_hi = -int(round(0.5 * pitch_px))
    dy_hi = min(dy_hi, -int(round(0.2 * pitch_px)))
    if SHIFT_MODE == "phase":
        # coarse table at step 4 (a quarter of the evaluations) for the margin and a coarse best;
        # a phase-correlation seed; then a step-1 refinement round each candidate
        coarse = _ncc_table(L, U, range(dy_lo, dy_hi + 1, 4), range(-span_dx, span_dx + 1, 4), 4)
        coarse = {k: v for k, v in coarse.items()
                  if min(upper["img"].shape[0], lower["img"].shape[0] - k[0]) - max(0, -k[0]) >= 0.4 * pitch_px}
        if not coarse:
            return None
        cands = [max(coarse, key=coarse.get)]
        seed = _phase_seed(L, U, prior_dy)
        if seed:
            cands += [c for c in seed[0] if dy_lo <= c[0] <= dy_hi]
        rf = int(round(0.2 * pitch_px)); rx = int(round(0.15 * pitch_px))
        table = dict(coarse)
        for cdy, cdx in cands:
            fine = _ncc_table(L, U, range(max(dy_lo, cdy - rf), min(dy_hi, cdy + rf) + 1, 1),
                              range(max(-span_dx, cdx - rx), min(span_dx, cdx + rx) + 1, 1), 1)
            table.update({k: v for k, v in fine.items()
                          if min(hU, hL - k[0]) - max(0, -k[0]) >= 0.4 * pitch_px})
        table = {k: v for k, v in table.items() if v is not None}
        if not table:
            return None
        bk = max(table, key=table.get); best = (bk[0], bk[1], table[bk])
        far = [v for (dy, dx), v in table.items() if abs(dy - best[0]) > 0.5 * pitch_px]
        margin = best[2] - (max(far) if far else -1.0)
        return {"dy": int(best[0]), "dx": int(best[1]), "ncc": round(best[2], 3), "margin": round(margin, 3),
                "seed": "phase" if seed else "coarse"}
    # from 0.6 body beyond the full step (the radiographer overshot) to a step of half a body (the last frame
    # of the sweep, shortened at the end of the anatomy)
    for dy in range(dy_lo, dy_hi + 1, step):
        # upper rows r in [r0, hU) overlap lower rows r + dy in [0, hL)
        r0 = max(0, -dy); r1 = min(hU, hL - dy)
        if r1 - r0 < 0.4 * pitch_px:
            continue
        for dx in range(-span_dx, span_dx + 1, step):
            c0 = max(0, -dx); c1 = min(wU, wL - dx)
            if c1 - c0 < 8:
                continue
            m = None
            if ML is not None and MU is not None:
                m = MU[r0:r1, c0:c1] & ML[r0 + dy:r1 + dy, c0 + dx:c1 + dx]
            v = _ncc(U[r0:r1, c0:c1], L[r0 + dy:r1 + dy, c0 + dx:c1 + dx], m)
            if v is None:
                continue
            table[(dy, dx)] = v
            if v > best[2]:
                best = (dy, dx, v)
    if best[0] is None:
        return None
    # HOW MUCH OF THE WINDOW WAS ACTUALLY SEARCHED. A peak is only a peak relative to the alternatives
    # that were scored beside it; if most of the window could not be scored, the argmax is the edge of
    # whatever region could, and it will sit near the prior for no better reason than that the window is
    # centred there. This is not hypothetical -- it is what an eroded mask did, and every other summary
    # statistic reported it as an improvement.
    want = len(range(dy_lo, dy_hi + 1, step))
    cover = len({dy for dy, _ in table}) / max(want, 1)
    if cover < MIN_COVER:
        return None
    far = [v for (dy, dx), v in table.items() if abs(dy - best[0]) > 0.5 * pitch_px]
    margin = best[2] - (max(far) if far else -1.0)
    return {"dy": int(best[0]), "dx": int(best[1]), "ncc": round(best[2], 3), "margin": round(margin, 3),
            "cover": round(cover, 3)}


def link_pair(lower, upper, pitch_px, prior_dy, min_cos=0.35, mode="strict", hi=None):
    """Which bodies the upper frame shares with the lower one.

    The image shift decides: an upper body whose centre, moved by the shift, lands within 0.4 body of a lower
    body's centre is that body. The pairs must form the only shape a sweep allows (the upper frame's bottom m
    bodies on the lower frame's top m), and the embedding cosine of each pair is recorded as a check, together
    with the m the embeddings alone would have picked.
    """
    nl, nu = len(lower["boxes"]), len(upper["boxes"])
    sh = ncc_shift(lower, upper, prior_dy, pitch_px, hi=hi)
    pairs = []
    if sh is not None:
        cl = [((b[1] + b[3]) / 2.0, (b[0] + b[2]) / 2.0) for b in lower["boxes"]]
        for j, b in enumerate(upper["boxes"]):
            cy, cx = (b[1] + b[3]) / 2.0 + sh["dy"], (b[0] + b[2]) / 2.0 + sh["dx"]
            d = [abs(cy - y) + 0.5 * abs(cx - x) for y, x in cl]
            if d and min(d) < 0.4 * pitch_px:
                pairs.append((int(np.argmin(d)), j))
        # The only shape a sweep allows: the upper frame's bottom m bodies on the lower frame's top m.
        #
        # STRICT takes the largest m whose every pair the shift supports. That is right when the boxes are
        # the annotation's and wrong when they are a detector's: one missed or spurious box inside the
        # shared block fails the `all(...)` test, m falls away, and every genuinely shared vertebra is
        # entered as a NEW node. On real films the detector misses only 2.2 % of bodies but 17.9 % come out
        # duplicated, which is this rule firing, not a failure to see the bone.
        #
        # ROBUST chooses m by best support instead of perfect support: score each candidate block by how
        # many of its pairs the shift agrees with, less half a point for each it does not, and keep the
        # whole block at the winning m. A single bad box then costs one mispaired body rather than the
        # entire link.
        ps = set(pairs)
        if mode == "robust":
            best_m, best_sc = 0, 0.0
            for m in range(1, min(nl, nu) + 1):
                hit = sum(1 for k in range(m) if (k, nu - m + k) in ps)
                sc = hit - 0.5 * (m - hit)
                # require the block to be mostly supported, so a long unsupported block cannot win on size
                if hit >= max(1, 0.6 * m) and sc > best_sc:
                    best_m, best_sc = m, sc
            m = best_m
        else:
            m = min(nl, nu)
            while m > 0 and not all((k, nu - m + k) in ps for k in range(m)):
                m -= 1
        pairs = [(k, nu - m + k) for k in range(m)]
    def cos(i, j):
        a, b = lower["emb"][i], upper["emb"][j]
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6))
    pair_cos = [round(cos(i, j), 3) for i, j in pairs]
    # what the embeddings alone would have chosen
    m_emb, best = 0, -1.0
    for m in range(1, min(nl, nu) + 1):
        c = float(np.mean([cos(k, nu - m + k) for k in range(m)]))
        if c >= min_cos and c > best:
            m_emb, best = m, c
    return {"m": len(pairs), "pairs": pairs, "shift": sh, "pair_cos": pair_cos, "m_emb": m_emb, "m_emb_cos": round(best, 3)}


def _prior_for(prior_dy, i):
    """One expected step, or the i-th of a list of them.

    A fixed-protocol sweep steps by the same amount every time and passes a scalar. A guided sweep does not:
    when a link comes back ambiguous the next step is SHORTENED to thicken it, so each pair has its own
    expectation and the linker's search window has to be centred on the one that was actually commanded for
    that pair. Passing a scalar keeps the old behaviour exactly.
    """
    if isinstance(prior_dy, (list, tuple, np.ndarray)):
        return float(prior_dy[i]) if i < len(prior_dy) else float(prior_dy[-1])
    return float(prior_dy)


def _finish_chain(chain, stations):
    for n in chain:
        n["emb"] = np.mean([stations[s]["emb"][j] for s, j in n["obs"]], 0)
        n["p_single"] = np.mean([stations[s]["p_single"][j] for s, j in n["obs"]], 0)
        n["p_blend"] = np.mean([stations[s]["p_blend"][j] for s, j in n["obs"]], 0)
        gts = [stations[s]["gt"][j] for s, j in n["obs"]]
        # a detector box with no truth (None) merged with one that has truth is that body, not a conflict
        vals = {g for g in gts if g is not None}
        n["gt"] = (next(iter(vals)) if len(vals) == 1 else None if not vals else ("conflict", gts))
    return chain


def _solve_positions(n, meas, huber):
    """Station offsets (Y_i, X_i), Y_0 = X_0 = 0, from pairwise measurements (i, j, dy, dx, w).

    Robust least squares: five rounds of IRLS with a Huber weight of one-fifth of a pitch, so a
    link that disagrees with the rest of the graph by more than that is down-weighted rather than
    obeyed. With consecutive links only the system is a chain and the solution is the cumulative
    sum -- identical to the pairwise build. Skip links are what make it over-determined.
    """
    if n <= 1:
        return [0.0] * n, [0.0] * n
    def solve(col, huber):
        w = np.array([m[4] for m in meas], float)
        x = np.zeros(n)
        for _ in range(5):
            A = np.zeros((len(meas), n - 1)); b = np.zeros(len(meas))
            for r, (i, j, dy, dx, _w) in enumerate(meas):
                v = dy if col == 0 else dx
                if j > 0: A[r, j - 1] += 1.0
                if i > 0: A[r, i - 1] -= 1.0
                b[r] = v
            sw = np.sqrt(w)[:, None]
            sol, *_ = np.linalg.lstsq(A * sw, b * sw[:, 0], rcond=None)
            x = np.concatenate([[0.0], sol])
            res = np.abs(A @ sol - b)
            w = np.array([m[4] for m in meas], float) * np.where(res <= huber, 1.0, huber / np.maximum(res, 1e-6))
        return x.tolist()
    return solve(0, huber), solve(1, huber)


def build_chain_global(stations, pitch_px, prior_dy, mode="strict"):
    """The same chain, from ALL the evidence at once instead of one link at a time.

    Every consecutive pair is measured as before. Every skip pair (i, i+2) is measured too, in a
    window centred on the sum of the two consecutive steps; where two frames share nothing the
    search returns None and the skip link simply does not exist -- so at two bodies of overlap on
    a four-body field this reduces to the pairwise chain, and the difference appears only where
    frames overlap enough to see past their neighbour. Station positions come from a robust least
    squares over every measurement; nodes come from clustering box centres in that common frame.
    Clustering, not pairing, is what makes a duplicated detector box across two frames ONE node.
    """
    n = len(stations)
    huber = 0.2 * pitch_px
    meas, cons = [], []
    for si in range(1, n):
        sh = ncc_shift(stations[si - 1], stations[si], _prior_for(prior_dy, si - 1), pitch_px)
        if sh:
            meas.append((si - 1, si, sh["dy"], sh["dx"], max(sh["ncc"], 0.05))); cons.append(sh)
        else:
            meas.append((si - 1, si, int(round(_prior_for(prior_dy, si - 1))), 0, 0.05)); cons.append(None)
    n_skip = 0
    for si in range(2, n):
        c = meas[si - 2][2] + meas[si - 1][2]
        sh = ncc_shift(stations[si - 2], stations[si], c, pitch_px,
                       lo=int(c - 0.8 * pitch_px), hi=int(c + 0.8 * pitch_px))
        if sh:
            meas.append((si - 2, si, sh["dy"], sh["dx"], max(sh["ncc"], 0.05))); n_skip += 1
    # Huber weighting lives inside _solve_positions; pass the threshold through the closure
    Y, X = _solve_positions(n, meas, huber)
    # cluster boxes in the common frame, top to bottom
    items = []
    for si, st in enumerate(stations):
        for j, b in enumerate(st["boxes"]):
            items.append(((b[1] + b[3]) / 2.0 + Y[si], (b[0] + b[2]) / 2.0 + X[si], si, j))
    items.sort()
    nodes = []
    for cy, cx, si, j in items:
        home = None
        for nd in nodes:
            if any(s == si for s, _ in nd["obs"]):
                continue
            if abs(cy - nd["cy"]) + 0.5 * abs(cx - nd["cx"]) < 0.4 * pitch_px:
                home = nd; break
        if home is None:
            nodes.append({"obs": [(si, j)], "cy": cy, "cx": cx})
        else:
            k = len(home["obs"]); home["obs"].append((si, j))
            home["cy"] = (home["cy"] * k + cy) / (k + 1); home["cx"] = (home["cx"] * k + cx) / (k + 1)
    nodes.sort(key=lambda nd: nd["cy"])
    chain = [{"obs": nd["obs"]} for nd in nodes]
    # link records the rest of the tool reads: the solved consecutive shifts, and the pairs the
    # clustering implies, so a link can still be checked against the truth afterwards
    node_of = {ob: k for k, nd in enumerate(chain) for ob in nd["obs"]}
    links = []
    for si in range(1, n):
        pairs = sorted((i, j) for (s0, i), k0 in node_of.items() if s0 == si - 1
                       for (s1, j), k1 in node_of.items() if s1 == si and k0 == k1)
        sh = cons[si - 1]
        shift = {"dy": int(round(Y[si] - Y[si - 1])), "dx": int(round(X[si] - X[si - 1])),
                 "ncc": sh["ncc"] if sh else None, "margin": sh["margin"] if sh else None,
                 "solved": True}
        lo, up = stations[si - 1], stations[si]
        def cos(i, j):
            a, b = lo["emb"][i], up["emb"][j]
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6))
        links.append({"lower": si - 1, "upper": si, "m": len(pairs), "pairs": pairs, "shift": shift,
                      "pair_cos": [round(cos(i, j), 3) for i, j in pairs], "m_emb": None, "m_emb_cos": None})
    if links:
        links[0]["n_skip_links"] = n_skip
    return _finish_chain(chain, stations), links


def build_chain(stations, pitch_px, prior_dy, mode="strict", solve="pairwise"):
    """Bottom-most station first. Returns nodes top->bottom with their observations and pooled evidence."""
    if solve == "global":
        return build_chain_global(stations, pitch_px, prior_dy, mode=mode)
    chain = [{"obs": [(0, k)]} for k in range(len(stations[0]["boxes"]))]
    links = []
    for si in range(1, len(stations)):
        lo, up = stations[si - 1], stations[si]
        # the last link is the only one the protocol allows to be short (the sweep ends where the anatomy
        # or the target does), so under "open" its search runs down to a zero step
        is_last = si == len(stations) - 1
        if LAST_LINK == "open" and is_last:
            last_hi = 0
        elif TIGHT_WINDOW and not is_last:
            # the paper's window: the commanded step plus 0.6 of a body, no further. Only the FINAL
            # link is allowed a short step, because only the final frame runs out of anatomy.
            last_hi = int(round(_prior_for(prior_dy, si - 1) + 0.6 * LINK_WINDOW * pitch_px))
        else:
            last_hi = None
        lk = link_pair(lo, up, pitch_px, _prior_for(prior_dy, si - 1), mode=mode, hi=last_hi)
        # `pairs` is kept: it is a few index pairs, and it is the only record of WHICH bodies a link
        # decided were shared, which is what lets a link be checked against the truth afterwards.
        links.append({"lower": si - 1, "upper": si, **lk})
        lower_nodes = [n for n in chain if any(s == si - 1 for s, _ in n["obs"])]
        nu = len(up["boxes"])
        shared = {j: lower_nodes[i] for i, j in lk["pairs"] if i < len(lower_nodes)}
        new_nodes = []
        for j in range(nu):
            if j in shared:
                shared[j]["obs"].append((si, j))
            else:
                new_nodes.append({"obs": [(si, j)]})
        chain = new_nodes + chain
    if NODE_ORDER == "position" or NODE_MERGE > 0:
        chain = merge_nodes_by_position(chain, stations, links, pitch_px, prior_dy)
    return _finish_chain(chain, stations), links


P_FLOOR = 1e-9         # posterior floor inside a log; the decoder's own
MIN_EXPOSED = 0.5          # a box needs this fraction of its area inside the exposed field to count
                           # as visible. Without it a vertebra in a blanked corner of a circular
                           # field is counted as present although the frame shows nothing there.
MASKED_NCC = False         # correlate only where BOTH frames are exposed
NCC_BAND = 0.0             # correlate only a band this many vertebral bodies wide, centred on the
                           # spine. 0 uses the whole frame, which is what every arm has done so far and
                           # which spends most of its variance on the anterior-posterior silhouette --
                           # a structure that is the same at every height and therefore correlates with
                           # itself at every shift.
MIN_COVER = 0.60           # a link is refused when less than this fraction of its search window could
                           # be scored. Below it the argmax is the edge of the scorable region rather
                           # than a peak, and it lands near the prior because the window is centred
                           # there -- which reads as accuracy in every summary statistic.
ERODE_MASK = 0.0           # shrink the correlated region by this many vertebral bodies, to keep the
                           # FIELD-STOP EDGE out of it. Any filter run over a frame that has a stop
                           # leaves a ring at the stop, and a ring is fixed to the RECEPTOR, not to the
                           # patient: it is in the same place in both frames, so it correlates best
                           # where the two discs coincide and drags the estimate toward a short step.
                           # This is what the high-pass arms were measuring -- a median error of +1.64
                           # bodies, all of it toward the shortest step the window allows -- and it is
                           # a property of filtering a stopped frame, not of the filter.
PREFILTER = "none"         # 'highpass' subtracts a blurred copy before correlating
PREFILTER_BODY = 0.75      # blur width for that subtraction, in vertebral bodies
FIELD_STOP = "none"        # 'none' (square, as every published arm), 'circle' (image intensifier),
                           # 'square' (flat panel with collimation). Applies to EVERY perturb mode, so
                           # the shape of the field can be ablated without also changing the physics.
FIELD_OPEN = 1.0           # fraction of the receptor left open by the collimator
PHYSICS_RECEPTOR = "mix"   # --perturb physics: 'ii', 'cmos', 'fpd', or 'mix' to draw per frame
EXPOSURE_SCALE = 1.0       # 1 is a live low-dose fluoroscopy frame; 10 is a deliberate stored spot
                           # exposure. Both sit inside the range measured on one mobile C-arm, and which
                           # one a theatre takes for a counting shot is a protocol decision.
PHYSICS_GRID = "high"      # anti-scatter grid regime: 'high' (13:1-17:1), 'low' (8:1) or 'none'
LINK_WINDOW = 1.0      # >1 widens the link search; 1.0 is the protocol's commanded step +/- 0.6 body
# Per-frame geometric jitter. MAG_JITTER is the half-width of the log-uniform scale draw, so the
# mismatch BETWEEN two frames of a link is up to twice it. 0.05 is what every arm published so far used;
# it was hard-coded and unnamed, which is why nobody could say what it cost.
MAG_JITTER = 0.05
ROT_JITTER = 3.0       # degrees, half-width; a hand-panned C-arm rolls as well as translating
NODE_MERGE = 0.0       # >0: merge nodes from different stations closer than this many bodies (opt-in)
NODE_ORDER = "prepend"  # "position": order the chain by panorama position instead of prepending (opt-in)


def merge_nodes_by_position(chain, stations, links, pitch_px, prior_dy, ratio=None):
    """Place every node by its panorama position, order the chain by it, and merge nodes that coincide.

    The pairwise builder prepends every unshared upper-frame box above the existing chain, whatever its
    position: a box a detector found twice in one frame, or one box in the shared block that failed to pair,
    became a node above everything and shifted every count by one.

    BOTH PARTS ARE OPT-IN, because the first version was not inert on true boxes: with the merge at 0.45
    body the fixed-step control fell from 98.3% to 95.8% chain complete, missed bodies rose and one anchor
    was lost. Where a link's shift is off by about half a body, two DIFFERENT bodies from adjacent frames
    land within the threshold and were merged into one. So the merge now refuses nodes that share a
    station (two boxes in one frame are two boxes) and defaults to off; the ordering is a separate switch.
    """
    ratio = NODE_MERGE if ratio is None else ratio
    if len(chain) < 2:
        return chain
    pos = [(0.0, 0.0)]
    for i, lk in enumerate(links):
        sh = lk.get("shift")
        dy, dx = (sh["dy"], sh["dx"]) if sh else (float(_prior_for(prior_dy, i)), 0.0)
        pos.append((pos[-1][0] + dy, pos[-1][1] + dx))
    def centre(n):
        ys, xs = [], []
        for s_, j in n["obs"]:
            b = stations[s_]["boxes"][j]
            ys.append(pos[s_][0] + (b[1] + b[3]) / 2.0); xs.append(pos[s_][1] + (b[0] + b[2]) / 2.0)
        return float(np.mean(ys)), float(np.mean(xs))
    nodes = sorted(chain, key=lambda n: centre(n)[0])
    if ratio <= 0:
        return nodes
    out = []
    for n in nodes:
        if out:
            y0, x0 = centre(out[-1]); y1, x1 = centre(n)
            same_station = {s_ for s_, _ in out[-1]["obs"]} & {s_ for s_, _ in n["obs"]}
            if not same_station and abs(y1 - y0) + 0.5 * abs(x1 - x0) < ratio * pitch_px:
                out[-1] = {"obs": out[-1]["obs"] + n["obs"]}
                continue
        out.append(n)
    return out


def count_names(n_nodes, anchor, anchor_present):
    """Names by counting from the anchor with the ordinary alphabet; None when the anchor is not in the chain."""
    if not anchor_present or anchor == "none":
        return [None] * n_nodes
    if anchor == "caudal":
        col = NORMAL[::-1]          # sacrum, L5, L4, ...
        names = [col[i] if i < len(col) else None for i in range(n_nodes)]
        return names[::-1]
    col = NORMAL[1:]                # C2, C3, ... (the sweep starts at C2; C1 is not a body the detector boxes reliably)
    return [col[i] if i < len(col) else None for i in range(n_nodes)]


ALPHABETS = "std"      # "ext": add the four-lumbar (sacralised L5) alphabet and its T13 variant


def alphabet(l6: bool, t13: bool, l4: bool = False):
    col = [f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)]
    if t13:
        col += ["T13"]
    col += [f"L{i}" for i in range(1, 5 if l4 else 7 if l6 else 6)]
    return col + ["sacrum"]


def role_score(labels, R, roles, w=1.0):
    """How well a candidate naming agrees with the role head, in mean log probability per vertebra.

    The candidate says which body is the last thoracic, which the first lumbar and which the last presacral;
    the role head says the same thing from the pixels, without ever having been told the names. Only the
    bodies a candidate assigns a role are scored, so a run that contains no junction is unaffected -- which is
    correct: the role head has nothing to say about a mid-lumbar body, and should not be allowed to pretend it
    does.
    """
    if R is None:
        return 0.0
    idx = {r: i for i, r in enumerate(roles)}
    THOR_ = {f"T{i}" for i in range(1, 14)}; LUMB_ = {f"L{i}" for i in range(1, 7)}
    want = {}
    thor = [i for i, n in enumerate(labels) if n in THOR_]
    lumb = [i for i, n in enumerate(labels) if n in LUMB_]
    if thor and lumb:
        want[thor[-1]] = "last_thoracic"; want[lumb[0]] = "first_lumbar"
    if "sacrum" in labels:
        j = labels.index("sacrum")
        if j > 0 and labels[j - 1] in LUMB_:
            want[j - 1] = "last_presacral"
    if not want:
        return 0.0
    return w * float(np.mean([np.log(max(1e-9, R[i][idx[r]])) for i, r in want.items() if r in idx]))


def rib_violation(labels, rib):
    """Share of nodes whose name disagrees with their rib-bearing truth: a rib-bearing body named
    lumbar, cervical or sacral, or a rib-free body named thoracic. None flags are skipped."""
    if not rib:
        return 0.0
    v = t = 0
    for name, r in zip(labels, rib):
        if r is None:
            continue
        t += 1
        v += int((REGION.get(name) == "thoracic") != bool(r))
    return v / t if t else 0.0


def decode_alphabets(P, anchor, anchor_present, R=None, roles=None, w_role=1.0, rib=None, w_rib=0.0):
    """Score the four alphabets against the chain and return the best naming, the variant call, and its margin.

    The chain runs top to bottom and its names are consecutive in one alphabet; with the landmark declared the
    run's end is pinned, so each alphabet admits one naming per starting offset and the score is the mean log
    probability the head gives that naming. The variant call is the alphabet that wins; the margin is how much
    it beat the best ordinary naming by, in mean log probability per vertebra. A single frame cannot make this
    call because it cannot see the alphabet's ends; a chain that reaches a landmark can.
    """
    n = len(P)
    best = None
    per_variant = {}
    combos = [(l6, t13, False) for l6 in (False, True) for t13 in (False, True)]
    if ALPHABETS == "ext":
        combos += [(False, False, True), (False, True, True)]
    for l6, t13, l4 in combos:
            col = alphabet(l6, t13, l4)
            tag = ("L4T13" if (l4 and t13) else "L4" if l4 else "both" if (l6 and t13) else "L6" if l6 else "T13" if t13 else "ordinary")
            starts = range(0, len(col) - n + 1)
            cand = []
            for st in starts:
                labels = col[st:st + n]
                if anchor_present and anchor == "caudal" and labels[-1] != "sacrum":
                    continue
                if anchor_present and anchor == "cranial" and labels[0] != "C2":
                    continue
                sc = float(np.mean([np.log(max(1e-9, P[i][ORD[labels[i]]])) for i in range(n)]))
                sc += role_score(labels, R, roles or [], w_role)
                if rib is not None and w_rib > 0:
                    sc -= w_rib * rib_violation(labels, rib)
                cand.append((sc, labels))
            if not cand:
                continue
            sc, labels = max(cand, key=lambda c: c[0])
            per_variant[tag] = round(sc, 4)
            if best is None or sc > best[0]:
                best = (sc, labels, tag)
    if best is None:
        names = [LEVEL_ORDER[int(i)] for i in P.argmax(1)]
        return names, None, "none", None, {}
    sc, labels, tag = best
    margin = None
    if "ordinary" in per_variant:
        margin = round(sc - per_variant["ordinary"], 4)
    probs = [float(P[i][ORD[labels[i]]]) for i in range(n)]
    return labels, round(sc, 4), tag, margin, {"per_variant": per_variant, "probs": [round(v, 4) for v in probs]}


def morph_names(P, anchor, anchor_present, direction_known=True, w_rare=1.0):
    """The morphology reading of a run, with the protocol's anchor declared as the caption would be.

    The radiographer starts the sweep on the sacrum (or on C2) and says so; the decoder is told the run
    contains that level, which pins the run's end, and the variant columns (T13, L6) stay open so a
    transitional spine is read as one.
    """
    from fluorocap_anchor import decode as anchor_decode
    cap = set()
    if anchor_present and anchor == "caudal":
        cap = {"sacrum"}
    elif anchor_present and anchor == "cranial":
        cap = {"C2"}
    dec = anchor_decode(P, cap, {}, None, direction_known=direction_known, w_rare=w_rare)
    names = dec.get("anchored_pred") or [LEVEL_ORDER[int(i)] for i in P.argmax(1)]
    return names, dec.get("anchor_score")


def build_panorama(stations, links, prior_dy):
    """Stitch the swept frames with the estimated shifts into one image, and place every box on it.

    Station 0 (the bottom of the sweep) is the origin; station i sits at the cumulative shift of its links.
    A link with no usable correlation falls back to the protocol's expected step. Overlaps are averaged.
    Returns the panorama (uint8), the station origins, and each station's boxes in panorama coordinates.
    """
    pos = [(0, 0)]
    for i, lk in enumerate(links):
        sh = lk.get("shift")
        dy, dx = (sh["dy"], sh["dx"]) if sh else (int(round(_prior_for(prior_dy, i))), 0)
        pos.append((pos[-1][0] + dy, pos[-1][1] + dx))
    y_min = min(p[0] for p in pos); x_min = min(p[1] for p in pos)
    pos = [(p[0] - y_min, p[1] - x_min) for p in pos]
    Hc = max(p[0] + st["img"].shape[0] for p, st in zip(pos, stations)); Wc = max(p[1] + st["img"].shape[1] for p, st in zip(pos, stations))
    acc = np.zeros((Hc, Wc), np.float32); wgt = np.zeros((Hc, Wc), np.float32)
    for p, st in zip(pos, stations):
        h, w = st["img"].shape
        acc[p[0]:p[0] + h, p[1]:p[1] + w] += st["img"].astype(np.float32); wgt[p[0]:p[0] + h, p[1]:p[1] + w] += 1.0
    pano = np.where(wgt > 0, acc / np.maximum(wgt, 1e-6), 0).astype(np.uint8)
    boxes = [[[b[0] + p[1], b[1] + p[0], b[2] + p[1], b[3] + p[0]] for b in st["boxes"]] for p, st in zip(pos, stations)]
    return pano, pos, boxes


def node_boxes_on_panorama(chain, pano_boxes):
    """One box per chain node in panorama coordinates: the mean of its observations' boxes."""
    out = []
    for n in chain:
        bs = np.array([pano_boxes[s][j] for s, j in n["obs"]], float)
        out.append(bs.mean(0).tolist())
    return out


WORK_PITCH = 40.0      # vertebral pitch, in pixels, that the correlation search works at


def map_query_panorama(q, pano, node_boxes, pitch_px, scales=(0.9, 0.95, 1.0, 1.05, 1.1), min_ncc=0.2):
    """Register the query frame onto the panorama; its boxes then land on node boxes.

    OpenCV normalised cross-correlation over a small scale range; the query is centre-cropped when larger than
    the panorama in either dimension. Returns the chain offset of the query's first box, the correlation, and
    None when nothing correlates above min_ncc.

    THE SEARCH RUNS AT A FIXED WORKING RESOLUTION, AND IT HAS TO. Template matching costs the product of the
    search area and the template area, so a real 2048-pixel film costs about a thousand times what a 600-pixel
    render costs -- the difference between seconds and a day per collection, which is how this was found. Both
    images are therefore reduced so that a vertebra is WORK_PITCH pixels tall before the search, and the peak
    is mapped back. Locating a body needs a fraction of the resolution that naming one does, so nothing is lost
    that the returned offset depends on.
    """
    import cv2
    Q = q["img"]
    red = min(1.0, WORK_PITCH / max(4.0, pitch_px))     # <= 1; 1.0 leaves small images untouched
    if red < 1.0:
        pano_w = cv2.resize(pano, (max(8, int(pano.shape[1] * red)), max(8, int(pano.shape[0] * red))), interpolation=cv2.INTER_AREA)
        Q = cv2.resize(Q, (max(8, int(Q.shape[1] * red)), max(8, int(Q.shape[0] * red))), interpolation=cv2.INTER_AREA)
    else:
        pano_w = pano
    best = None
    for sc in scales:
        Qs = cv2.resize(Q, (max(8, int(round(Q.shape[1] * sc))), max(8, int(round(Q.shape[0] * sc)))), interpolation=cv2.INTER_AREA) if sc != 1.0 else Q
        ch, cw = min(Qs.shape[0], pano_w.shape[0] - 2), min(Qs.shape[1], pano_w.shape[1] - 2)
        if ch < 4 or cw < 4:
            continue
        oy, ox = (Qs.shape[0] - ch) // 2, (Qs.shape[1] - cw) // 2
        T = Qs[oy:oy + ch, ox:ox + cw]
        r = cv2.matchTemplate(pano_w, T, cv2.TM_CCOEFF_NORMED)
        _, v, _, loc = cv2.minMaxLoc(r)
        # THE SAME ALIASING GUARD THE LINKER HAS. A column of vertebrae is periodic at the body pitch, so a
        # query frame correlates nearly as well one body off as it does in the right place -- and when it
        # wins there, every name taken from the registration is off by one, silently. The margin over the
        # best peak more than half a pitch away is what separates the two; the peak alone does not.
        pw = max(1.0, pitch_px * red)
        rows = np.arange(r.shape[0])
        far = r[np.abs(rows - loc[1]) > 0.5 * pw]
        margin = float(v) - (float(far.max()) if far.size else -1.0)
        if best is None or v > best["ncc"]:
            # back to panorama coordinates: the reduction applies to the peak and to the centre-crop offsets
            best = {"ncc": float(v), "scale": sc, "top": int(loc[1] / red), "left": int(loc[0] / red),
                    "oy": oy / red, "ox": ox / red, "margin": round(margin, 3)}
    if best is None or best["ncc"] < min_ncc:
        return None
    sc = best["scale"]
    warp = None
    if PLACE_MODE == "ecc":
        # Refine the template peak by ECC alignment (Evangelidis & Psarakis): a continuous optimum
        # over translation and rotation, seeded from the discrete peak, instead of the five-scale
        # grid alone. Failure of any kind keeps the template result -- ECC is a refinement, not a
        # second opinion, and a query that does not refine is not a query that was placed wrongly.
        try:
            Qs = cv2.resize(Q, (max(8, int(round(Q.shape[1] * sc))), max(8, int(round(Q.shape[0] * sc)))), interpolation=cv2.INTER_AREA) if sc != 1.0 else Q
            oy_w, ox_w = int(round(best["oy"] * red)), int(round(best["ox"] * red))
            T = Qs[oy_w:oy_w + min(Qs.shape[0], pano_w.shape[0] - 2), ox_w:ox_w + min(Qs.shape[1], pano_w.shape[1] - 2)]
            ty, tx = int(round(best["top"] * red)), int(round(best["left"] * red))
            pad = int(round(0.5 * max(1.0, pitch_px * red)))
            y0, x0 = max(0, ty - pad), max(0, tx - pad)
            y1, x1 = min(pano_w.shape[0], ty + T.shape[0] + pad), min(pano_w.shape[1], tx + T.shape[1] + pad)
            crop = pano_w[y0:y1, x0:x1]
            if crop.shape[0] > T.shape[0] and crop.shape[1] > T.shape[1]:
                W = np.array([[1, 0, tx - x0], [0, 1, ty - y0]], np.float32)
                crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 60, 1e-4)
                cc, W = cv2.findTransformECC(T.astype(np.float32) / 255.0, crop.astype(np.float32) / 255.0,
                                             W, cv2.MOTION_EUCLIDEAN, crit, None, 5)
                if np.isfinite(cc) and cc >= best["ncc"] - 0.15:
                    warp = (W, x0, y0); best["ecc"] = round(float(cc), 3)
        except Exception:  # noqa: BLE001  -- cv2.error on non-convergence, shape mismatches
            warp = None
    cs = [((b[1] + b[3]) / 2.0, (b[0] + b[2]) / 2.0) for b in node_boxes]
    hits = []
    for b in q["boxes"]:
        if warp is not None:
            # query centre -> working-resolution template coordinates -> ECC warp -> panorama
            W, x0, y0 = warp
            px = ((b[0] + b[2]) / 2.0 * sc - best["ox"]) * red; py = ((b[1] + b[3]) / 2.0 * sc - best["oy"]) * red
            wx = W[0, 0] * px + W[0, 1] * py + W[0, 2] + x0; wy = W[1, 0] * px + W[1, 1] * py + W[1, 2] + y0
            cy, cx = wy / red, wx / red
            d = [abs(cy - y) + 0.5 * abs(cx - x) for y, x in cs]
            hits.append(int(np.argmin(d)) if (d and min(d) < 0.45 * pitch_px) else None)
            continue
        cy = ((b[1] + b[3]) / 2.0) * sc - best["oy"] + best["top"]
        cx = ((b[0] + b[2]) / 2.0) * sc - best["ox"] + best["left"]
        d = [abs(cy - y) + 0.5 * abs(cx - x) for y, x in cs]
        hits.append(int(np.argmin(d)) if (d and min(d) < 0.45 * pitch_px) else None)
    if hits and hits[0] is not None and all(h is None or h == hits[0] + k for k, h in enumerate(hits)):
        return {"offset": hits[0], "ncc": round(best["ncc"], 3), "scale": sc, "matched_boxes": sum(h is not None for h in hits),
                "top": best["top"], "left": best["left"], "oy": best["oy"], "ox": best["ox"], "margin": best["margin"]}
    known = [(k, h) for k, h in enumerate(hits) if h is not None]
    if known:
        k, h = known[0]
        return {"offset": h - k, "ncc": round(best["ncc"], 3), "scale": sc, "matched_boxes": len(known), "inconsistent": True,
                "top": best["top"], "left": best["left"], "oy": best["oy"], "ox": best["ox"], "margin": best["margin"]}
    return None


def map_query_emb(q, chain, min_margin=0.05):
    """Fallback: the chain offset maximising the mean cosine of the query's embeddings, with its margin."""
    K = len(q["boxes"]); n = len(chain)
    if K == 0 or n < K:
        return None
    E = np.stack([c["emb"] for c in chain]); E = E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-6)
    Q = q["emb"] / (np.linalg.norm(q["emb"], axis=1, keepdims=True) + 1e-6)
    scores = np.array([float(np.mean([np.dot(Q[j], E[o + j]) for j in range(K)])) for o in range(n - K + 1)])
    order = np.argsort(scores)[::-1]
    best = int(order[0]); second = float(scores[order[1]]) if len(order) > 1 else -1.0
    return {"offset": best, "score": round(float(scores[best]), 3), "margin": round(float(scores[best]) - second, 3),
            "abstain": bool(float(scores[best]) - second < min_margin)}


# ----------------------------------------------------------------------------------------------------------
# scoring
# ----------------------------------------------------------------------------------------------------------
def cluster_boot(per_spine, n_boot=2000, seed=0):
    """Accuracy with a spine-level bootstrap interval; per_spine = list of (correct, total)."""
    per_spine = [(c, t) for c, t in per_spine if t > 0]
    if not per_spine:
        return None, [None, None]
    rng = np.random.RandomState(seed)
    c = np.array([p[0] for p in per_spine], float); t = np.array([p[1] for p in per_spine], float)
    acc = float(c.sum() / t.sum())
    vals = []
    for _ in range(n_boot):
        idx = rng.randint(0, len(c), len(c))
        vals.append(c[idx].sum() / max(1.0, t[idx].sum()))
    return acc, [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def spine_class(rec):
    if not rec:
        return "unknown"
    c = rec.get("cls") if isinstance(rec, dict) else None
    return {"ordinary": "ordinary", "lumbosacral_only": "lumbosacral", "thoracolumbar_only": "thoracolumbar", "both": "both"}.get(c, c or "unknown")


def _acc(pred, gt):
    c = t = 0
    for p, g in zip(pred, gt):
        if g is None:
            continue
        t += 1; c += int(p == g)
    return (c, t)


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drr", action="append", required=True, help="ann/img directory (repeatable)")
    ap.add_argument("--classes", required=True, help="spine_classes.json from anomaly_manifest.py")
    ap.add_argument("--model", required=True); ap.add_argument("--head", default=None)
    ap.add_argument("--detector", default=None, help="YOLO pose weights; needed for --boxes det")
    ap.add_argument("--box-repair", type=int, default=1,
                    help="1: merge double detections and fill single misses using the LOCAL inter-vertebral "
                         "spacing of each frame. Never assumes a vertebra count, so a six-lumbar spine is "
                         "repaired like any other -- unlike the published baselines, whose fixed cardinality "
                         "makes them fail on exactly the transitional spines this project is about. On by "
                         "default: at the operating threshold it takes duplicated bodies from 3.03%% to "
                         "0.61%% and naming from 83.0/85.6/90.2 to 87.2/90.4/91.4 at two, three and four "
                         "vertebrae, closing more than half the distance to the annotation-box ceiling. "
                         "Pass 0 to reproduce the older arms.")
    ap.add_argument("--det-conf", type=float, default=0.25,
                    help="detector confidence. A sweep of held-out real film puts recall at 98.77%% at 0.25 "
                         "and 99.18%% at 0.10, halving the sacrum misses, and flat below that -- at the "
                         "cost of 23 boxes on no vertebra rather than 17. Whether that trade helps depends "
                         "on the linker, which is why it is a flag and not a constant.")
    ap.add_argument("--boxes", choices=["gt", "det"], default="gt")
    ap.add_argument("--span", default="ii9", help="preset " + "|".join(SPAN_PRESETS) + " or a number of mm at the spine")
    ap.add_argument("--overlap", type=float, default=1.0, help="bodies shared by consecutive frames (nominal; jittered ±0.3)")
    ap.add_argument("--step-jitter", type=float, default=0.3,
                    help="the step between exposures is span - (overlap + U(-j, j)) bodies. 0 is the "
                         "protocol as written, a fixed move; 0.3 is what every earlier arm used. The "
                         "jitter draw still consumes the generator at 0, so the two are paired: same "
                         "photometric draws, different geometry only.")
    ap.add_argument("--anchor", choices=["auto", "caudal", "cranial", "none"], default="auto",
                    help="none: sweep the labelled stack top to bottom with no declared landmark (morphology only)")
    ap.add_argument("--perturb", choices=["none", "photometric", "film"], default="film")
    ap.add_argument("--film-params", default="~/model_night/film_match/film_match_params.json")
    ap.add_argument("--ks", type=int, nargs="+", default=[2, 3, 4], help="query frame lengths in whole bodies")
    ap.add_argument("--queries-per-k", type=int, default=2)
    ap.add_argument("--require-sacrum", type=int, default=0, help="1: skip spines without a labelled sacrum")
    ap.add_argument("--link-solve", choices=["pairwise", "global"], default="pairwise",
                    help="pairwise: one link at a time, as published. global: consecutive AND skip links "
                         "solved together by robust least squares, nodes by clustering in the common frame")
    ap.add_argument("--shift", choices=["ncc", "phase"], default="ncc",
                    help="ncc: exhaustive NCC search. phase: coarse NCC + phase-correlation seed + fine refine")
    ap.add_argument("--place", choices=["template", "ecc"], default="template",
                    help="template: matchTemplate peak. ecc: the peak refined by ECC (Euclidean) alignment")
    ap.add_argument("--link", choices=["strict", "robust"], default="robust",
                    help="how a station pairs with the one below. strict needs EVERY pair in the shared "
                         "block supported by the image shift; robust needs 60%% and keeps the block, so one "
                         "bad box costs one mispaired body rather than the whole overlap. Robust is the "
                         "default because the A/B says it is free: with annotation boxes the two are "
                         "identical to the second decimal (duplicates 0.00%% either way, naming 93.62 / "
                         "93.88 / 100.00 at two, three and four vertebrae), while with detector boxes it "
                         "takes duplicates from 21.82%% to 3.03%% and naming at four vertebrae from 56.25%% "
                         "to 93.75%%. Pass strict to reproduce the older arms.")
    ap.add_argument("--holdout-bank", action="append", default=None, metavar="BANK",
                    help="a training bank (dir with rung_*.npz). Any film with a crop in that bank's TRAIN "
                         "split is REFUSED. Repeatable: an arm comparing models fitted on different banks "
                         "must exclude the UNION, or it is a held-out test for one and a memory test for "
                         "another. Without this the arm may score films the encoder was fitted on.")
    ap.add_argument("--fold", default=None,
                    help="a fold{k}.json from make_fold_banks.py. Scores ONLY that fold's held-out cases, "
                         "and counts as a holdout in its own right: the encoder passed with it was fitted "
                         "with exactly those cases excluded, which is what --holdout-bank proves the long "
                         "way round. Cannot be combined with --holdout-bank.")
    ap.add_argument("--cases", default=None, metavar="FILE",
                    help="score only the case ids listed one per line, on top of any --holdout-bank filter; "
                         "for a second holdout such as a detector's own validation split")
    ap.add_argument("--allow-trained-on", action="store_true",
                    help="run without --holdout-bank and accept that the number is not a held-out number")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-tta", action="store_true")
    ap.add_argument("--role-head", default=None,
                    help="transition-role head from tools/train_role_head.py, trained on THIS encoder. Its "
                         "posterior is a second opinion about where the junctions are, added to the alphabet "
                         "score at the bodies a candidate naming assigns a role to.")
    ap.add_argument("--w-role", type=float, default=1.0)
    ap.add_argument("--retake", type=float, default=0.0,
                    help="also shoot each query frame again, shifted by this many vertebral pitches up or down, "
                         "and score it identically. 0.25 is what a radiographer told to move a little would do. "
                         "0 disables it.")
    ap.add_argument("--end-rule", choices=["clamp", "skip"], default="clamp",
                    help="clamp: the last frame is slid to fit the scan, however short that makes its step. "
                         "skip: a final frame that would move less than half a body is not taken.")
    ap.add_argument("--last-link", choices=["protocol", "open"], default="protocol",
                    help="open: the last link's shift search runs down to a zero step (the only link the "
                         "protocol allows to be short) instead of stopping at half a body.")
    ap.add_argument("--rib", choices=["none", "oracle"], default="none",
                    help="oracle: the ann's rib-bearing truth (tools/rib_bearing_ann.py) enters the alphabet "
                         "decoder as a soft penalty of --rib-weight per disagreeing body. The ceiling of a "
                         "perfect rib reader; anns without rib labels are unaffected.")
    ap.add_argument("--rib-weight", type=float, default=2.0)
    ap.add_argument("--hybrid", choices=["margin", "local"], default="margin",
                    help="margin: take the count unless the variant alphabet beats the ordinary one by more than "
                         "--variant-tau over the whole chain. local: compare the two readings only on the bodies "
                         "they name differently, which is where the evidence is.")
    ap.add_argument("--link-window", type=float, default=1.0,
                    help="multiplier on the correlation search span either side of the commanded step. "
                         "1.0 is the protocol. Larger values measure what the restriction is worth by "
                         "letting the periodic column compete.")
    ap.add_argument("--node-merge", type=float, default=0.0,
                    help="OPT-IN: merge chain nodes from different stations closer than this many bodies on the "
                         "panorama. Aimed at detector boxes; on true boxes 0.45 merged distinct bodies where a "
                         "link shift was half a body off, so it is off by default.")
    ap.add_argument("--node-order", choices=["prepend", "position"], default="prepend",
                    help="OPT-IN: order chain nodes by panorama position rather than prepending every unshared "
                         "upper-frame box above the chain.")
    ap.add_argument("--alphabets", choices=["std", "ext"], default="std",
                    help="ext: add the four-lumbar (sacralised L5) alphabet and its T13 variant to the decoder")
    ap.add_argument("--variant-tau", type=float, default=0.0,
                    help="how much the variant alphabet must beat the ordinary one by, in mean log probability "
                         "per vertebra, before the hybrid abandons the count. 0 = take the count on any tie.")
    ap.add_argument("--contact-sheet", type=int, default=6, help="draw this many sweeps (anomalous first)")
    ap.add_argument("--out", required=True)
    EG.add_args(ap)
    a = ap.parse_args()
    if a.allow_trained_on and not a.not_held_out:     # the tool's own declaration is the gate's declaration
        a.not_held_out = "--allow-trained-on: the caller admitted films the model trained or was selected on"
    global NODE_MERGE, NODE_ORDER, END_RULE, LAST_LINK, ALPHABETS, LINK_WINDOW
    NODE_MERGE = a.node_merge; NODE_ORDER = a.node_order; END_RULE = a.end_rule; LAST_LINK = a.last_link
    LINK_WINDOW = a.link_window
    ALPHABETS = a.alphabets

    import torch
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    rng = np.random.RandomState(a.seed)
    out = Path(os.path.expanduser(a.out)); out.mkdir(parents=True, exist_ok=True)
    span_mm = SPAN_PRESETS.get(a.span, None)
    if span_mm is None:
        span_mm = float(a.span)
    film_params = None
    if a.perturb == "film":
        from film_match_augment import load_params
        film_params = load_params(os.path.expanduser(a.film_params))
        if film_params is None:
            raise SystemExit(f"--perturb film needs fitted parameters at {a.film_params}")
    from eval_feasibility_claims import resolve_case
    from fluorocap_anchor import decode as anchor_decode
    spine_cls = json.load(open(os.path.expanduser(a.classes)))
    spine_cls = spine_cls.get("per_case", spine_cls)
    namer = Namer(os.path.expanduser(a.model), os.path.expanduser(a.head) if a.head else None, dev, tta=not a.no_tta)
    if a.role_head:
        namer.load_roles(os.path.expanduser(a.role_head))
        print(f"  role head {Path(a.role_head).name} loaded: {namer.roles} "
              f"(balanced {100 * float(namer.role_meta.get('balanced_accuracy') or 0):.1f}%)", flush=True)
    det = None
    if a.boxes == "det":
        from ultralytics import YOLO
        det = YOLO(os.path.expanduser(a.detector))

    anns = []
    # WHICH FILMS IS THIS ARM ALLOWED TO SCORE?
    # A film the encoder was fitted on is not a test of the encoder. The banks carry a patient-grouped
    # train/val split, so the question is answerable mechanically: refuse any case with a crop in TRAIN.
    # This exists because the first real-film arm scored 170 films of which 145 were training films, and
    # nothing in the pipeline objected -- the arm read a render directory, and render directories do not
    # know what a bank did with them.
    trained_on = set()
    only_cases = None
    listed_cases = set()
    if a.cases:
        listed_cases = {l.strip() for l in open(os.path.expanduser(a.cases)) if l.strip()}
        print(f"cases: restricting to the {len(listed_cases):,} ids in {a.cases}", flush=True)
    if a.fold:
        if a.holdout_bank:
            raise SystemExit("--fold and --holdout-bank say different things about the same run; pass one")
        F = json.load(open(os.path.expanduser(a.fold)))
        only_cases = set(F["held_out_cases"])
        print(f"fold {F['fold']}/{F['folds']}: scoring only its {len(only_cases):,} held-out cases "
              f"({len(F['held_out_variant_patients'])} variant patients); the encoder was fitted without them",
              flush=True)
    elif a.holdout_bank:
        import glob as _glob
        for b in a.holdout_bank:
            bd = Path(os.path.expanduser(b))
            n0 = len(trained_on)
            found = sorted(_glob.glob(str(bd / "rung_*.npz")))
            if not found:
                raise SystemExit(f"{bd} holds no rung_*.npz; cannot prove a holdout against it")
            for npz in found:
                z = np.load(npz, allow_pickle=True)
                if "split" not in z:
                    raise SystemExit(f"{npz} has no split array; cannot prove a holdout")
            # one rule for what a bank's model has seen: tools/holdout.trained_on, which counts the val split too
            # (the encoder kept its best epoch on it). This loop used to read split == "train" only.
            import holdout as _HO
            trained_on |= _HO.trained_on(bd, verbose=False)
            print(f"holdout: {bd.name} contributes {len(trained_on) - n0:,} new seen case ids (train + val)", flush=True)
        print(f"holdout: {len(trained_on):,} case ids will be refused as trained or selected on", flush=True)
    elif not a.allow_trained_on:
        raise SystemExit("refusing to run without --holdout-bank: pass a bank to exclude its training films, "
                         "or --allow-trained-on to state in the record that this is not a held-out number")

    for d in a.drr:
        d = Path(os.path.expanduser(d))
        anns += [(p, d / "img") for p in sorted((d / "ann").glob("*.json"))]
    if a.limit:
        anns = anns[: a.limit]
    global SHIFT_MODE, PLACE_MODE
    SHIFT_MODE, PLACE_MODE = a.shift, a.place
    print(f"sweep: {len(anns)} candidate spines; span {a.span} = {span_mm:.0f} mm at the spine; overlap {a.overlap} bodies; "
          f"boxes {a.boxes}; perturb {a.perturb}; anchor {a.anchor}; device {dev}", flush=True)

    # CHEAP REJECTION BEFORE THE EXPENSIVE READ. load_spine() opens the image, and on a film collection that
    # is several megabytes per case; the arms that require a landmark use a few percent of what they scan.
    # Reading the annotation's level names first turns a 9,109-image pass into a 170-image one and changes no
    # result, because the same films are rejected either way.
    def _can_use(ann_path):
        if ann_path.stem in trained_on:
            return False
        if a.cases and ann_path.stem not in listed_cases:
            return False
        if only_cases is not None and ann_path.stem not in only_cases:
            return False
        try:
            j = json.load(open(ann_path))
        except Exception:  # noqa: BLE001
            return False
        names = {v.get("name") for v in (j.get("levels") or {}).values()}
        if len(names) < 4:
            return False
        if a.require_sacrum and "sacrum" not in names:
            return False
        if a.anchor == "caudal" and "sacrum" not in names:
            return False
        if a.anchor == "cranial" and not ({"C1", "C2"} & names):
            return False
        if a.anchor == "auto" and "sacrum" not in names and not ({"C1", "C2"} & names):
            return False
        return True

    before = len(anns)
    n_refused_trained = sum(1 for p_, _ in anns if p_.stem in trained_on)
    anns = [(p_, d_) for p_, d_ in anns if _can_use(p_)]
    if n_refused_trained:
        print(f"  {n_refused_trained} spines refused because the encoder was trained on them", flush=True)
    if len(anns) != before:
        print(f"  {len(anns)} of {before} spines carry what this arm needs; the rest are skipped without "
              f"reading their images", flush=True)
    # THE GATE (tools/eval_gate.py; docs/DATA_ACCOUNTING.md 5.3, not opt-in), before anything is scored: every
    # model loaded here against every evaluation patient, through its initialisation chain. A patient it trained
    # or was selected on, an unresolved lineage or an unkeyable item stops the run unless --not-held-out says why.
    # (--holdout-bank refuses a level bank's train+val cases; the gate asks every loaded model's own lineage.)
    gate = EG.gate_evaluation([dict(case=p_.stem, hint=EG.PK.corpus_hint_for_path(str(d_) + "/")) for p_, d_ in anns],
                              {"encoder": a.model, "head": a.head, "role_head": a.role_head,
                               "detector": a.detector if a.boxes == "det" else None},
                              "tools/sweep_map.py", a, eval_set=";".join(a.drr))

    records = []
    t0 = time.time()
    for ai, (ann_p, img_dir) in enumerate(anns):
        sp = load_spine(ann_p, img_dir)
        if sp is None:
            continue
        names = [n for n, _ in sp["boxes"]]
        has_sac = "sacrum" in names; has_cr = ("C2" in names) or ("C1" in names)
        anchor = a.anchor
        if anchor == "auto":
            anchor = "caudal" if has_sac else ("cranial" if has_cr else None)
        if anchor is None or (anchor == "caudal" and not has_sac) or (anchor == "cranial" and not has_cr):
            continue
        if a.require_sacrum and not has_sac:
            continue
        pitch_px, px_per_mm = body_pitch_px(sp)
        if not pitch_px or not px_per_mm:
            continue
        sp["_sacrum_part"] = sacrum_part(sp) if has_sac else None
        if anchor == "cranial" and names[0] == "C1":
            sp["boxes"] = sp["boxes"][1:]; names = names[1:]
        span_px = span_mm * px_per_mm
        prior_dy = -(span_px - a.overlap * pitch_px)      # what the protocol asks the radiographer to do
        cls_rec, how = resolve_case(sp["case"], spine_cls, {})
        if not cls_rec:
            tail = sp["case"].split("_")[-1]
            if tail.isdigit() and tail.zfill(4) in spine_cls:      # release ids are zero-padded; the renders' are not
                cls_rec, how = spine_cls[tail.zfill(4)], "ct_flag_table_zfill"
        klass = spine_class(cls_rec)

        sweep_anchor = anchor if anchor != "none" else "cranial"
        stations = make_stations(sp, span_px, a.overlap, pitch_px, sweep_anchor, rng, a.perturb, film_params,
                                 step_jitter=a.step_jitter)
        for st in stations:
            if a.boxes == "det":
                db = detect_boxes(det, st["img"], conf=a.det_conf)
                if a.box_repair:
                    db, _ = repair_boxes(db)
                st["gt"] = assign_gt(db, st["all_boxes"], st["all_idx"]); st["boxes"] = db
            else:
                st["gt"] = list(st["gt_idx"])
            st["emb"], st["p_single"], st["p_blend"] = namer.run(st["img"], st["boxes"])
        if any(len(st["boxes"]) == 0 for st in stations):
            records.append({"case": sp["case"], "class": klass, "anchor": anchor, "skipped": "empty station"}); continue
        chain, links = build_chain(stations, pitch_px, prior_dy, mode=a.link, solve=a.link_solve)
        n_nodes = len(chain)
        # what the system knows about its own chain WITHOUT the truth: the weakest link's correlation margin
        # over the best shift half a body away. A link that cannot tell its own offset from a one-body offset
        # is the failure that puts every name above it wrong, and it is visible at run time.
        margins = [(l.get("shift") or {}).get("margin") for l in links]
        chain_margin = float(min([m for m in margins if m is not None], default=1.0)) if links else 1.0
        pano, pano_pos, pano_boxes = build_panorama(stations, links, prior_dy)
        nboxes = node_boxes_on_panorama(chain, pano_boxes)
        gt_names = [names[n["gt"]] if isinstance(n["gt"], int) else None for n in chain]
        sac_i = names.index("sacrum") if has_sac else None
        if anchor == "caudal":
            anchor_present = chain[-1]["gt"] == sac_i
        elif anchor == "cranial":
            anchor_present = chain[0]["gt"] == 0 and names[0] == "C2"
        else:
            anchor_present = False
        c_names = count_names(n_nodes, anchor, anchor_present)
        P = np.stack([n["p_blend"] for n in chain])
        m_names, m_score = morph_names(P, anchor, anchor_present)
        R = namer.role_probs(np.stack([n["emb"] for n in chain])) if a.role_head else None
        rib_flags = None
        if a.rib == "oracle" and sp.get("rib") and any(r is not None for r in sp["rib"]):
            rib_flags = [sp["rib"][n["gt"]] if isinstance(n["gt"], int) else None for n in chain]
        v_names, v_score, v_tag, v_margin, v_extra = decode_alphabets(
            P, anchor, anchor_present, R, getattr(namer, "roles", None), a.w_role, rib=rib_flags, w_rib=a.rib_weight)
        node_conf = v_extra.get("probs") or [float(P[i].max()) for i in range(n_nodes)]
        # THE HYBRID, AND WHY IT IS NOT OBVIOUS WHICH READING TO TRUST. When the chain reaches the landmark the
        # count is a hard constraint and the shape reading is an estimate; on ordinary spines the shape reading
        # wins, and on lumbosacral-variant spines the count won by two points in the first run. The hybrid takes
        # the count whenever the chain is anchored and the variant alphabet did not beat the ordinary one by
        # more than `--variant-tau` in mean log probability per vertebra. tau is a knob, not a fitted value, and
        # the margin is recorded per spine so the whole curve can be drawn without re-running anything.
        # --hybrid local: the two readings differ on a few bodies (where the extra one sits); only those
        # bodies carry evidence about which reading is right. On a real film whose top body was a T11 the
        # whole-chain mean chose L6, because every undisputed body was read one level caudal with high
        # confidence and outvoted the single body the L6 reading had to name L6 at probability zero.
        count_ok = anchor_present and all(c is not None for c in c_names)
        local_adv = None
        if count_ok and v_names != c_names:
            disp = [i for i in range(n_nodes) if v_names[i] != c_names[i]]
            local_adv = round(float(np.mean([np.log(max(P_FLOOR, P[i][ORD[v_names[i]]])) -
                                             np.log(max(P_FLOOR, P[i][ORD[c_names[i]]])) for i in disp])), 4)
        if a.hybrid == "local":
            h_names = v_names if (not count_ok or (local_adv is not None and local_adv > a.variant_tau)) else c_names
        elif count_ok and (v_margin is None or v_margin <= a.variant_tau):
            h_names = c_names
        else:
            h_names = v_names
        s_names = [LEVEL_ORDER[int(np.argmax(n["p_single"]))] for n in chain]
        # chain integrity against the truth: every body that lay wholly inside some frame should be one node
        gts = [n["gt"] for n in chain if isinstance(n["gt"], int)]
        dup = len(gts) - len(set(gts))
        covered = set(gts)
        expected = set()
        for st in stations:
            expected.update(st["gt_idx"])
        missed = len([g for g in expected if g not in covered])
        # A box with no truth at the far end of the chain from the anchor is a vertebra the annotation does
        # not cover -- NHANES labels L1 to the sacrum and the film shows a T12 above L1 -- not a false
        # positive, and the scorer cannot say the detector was wrong there. It is counted as unlabelled and
        # not held against the chain; its name is recorded so the reader can see what it was called.
        none_idx = [i for i, n in enumerate(chain) if n["gt"] is None]
        unl = []
        if anchor == "caudal":
            for i in range(n_nodes):
                if chain[i]["gt"] is None: unl.append(i)
                else: break
        elif anchor == "cranial":
            for i in range(n_nodes - 1, -1, -1):
                if chain[i]["gt"] is None: unl.append(i)
                else: break
        fp = len(none_idx) - len(unl)
        conflict = sum(1 for n in chain if isinstance(n["gt"], tuple))
        disagree = [i for i in range(n_nodes) if c_names[i] is not None and m_names[i] is not None and c_names[i] != m_names[i]]
        rec = {"case": sp["case"], "class": klass, "class_how": how, "anchor": anchor, "n_bodies": len(names), "pseudo_truth": sp["pseudo"],
               "panorama_shape": list(pano.shape),
               "stations": len(stations), "chain_nodes": n_nodes, "duplicates": dup, "missed": missed, "false_positive": fp,
               "unlabelled": len(unl), "unlabelled_named": [h_names[i] for i in unl],
               "station_steps": [st.get("step_actual") for st in stations],
               "rib_flags": rib_flags,
               "hybrid_rule": a.hybrid, "local_advantage": local_adv,
               "node_P": [[round(float(v), 3) for v in P[i]] for i in range(n_nodes)],
               "conflict": conflict, "anchor_present": bool(anchor_present), "prior_dy": round(prior_dy, 1), "pitch_px": round(pitch_px, 1),
               "chain_margin": round(chain_margin, 4),
               "links": links, "gt_names": gt_names, "count_names": c_names, "morph_names": m_names, "single_names": s_names,
               "variant_names": v_names, "variant_call": v_tag, "variant_margin": v_margin, "variant_scores": v_extra.get("per_variant"),
               "hybrid_names": h_names,
               "node_conf": node_conf,
               "count_vs_morph_disagree": len(disagree), "morph_score": m_score,
               "chain_acc": {"count": _acc(c_names, gt_names), "morph": _acc(m_names, gt_names),
                             "single": _acc(s_names, gt_names), "variant": _acc(v_names, gt_names),
                             "hybrid": _acc(h_names, gt_names)},
               "queries": []}
        for K in a.ks:
            for q in make_queries(sp, K, a.queries_per_k, pitch_px, rng, a.perturb, film_params):
                if a.boxes == "det":
                    db = detect_boxes(det, q["img"], conf=a.det_conf)
                    if a.box_repair:
                        db, _ = repair_boxes(db)
                    q["gt"] = assign_gt(db, q["all_boxes"], q["all_idx"]); q["boxes"] = db
                else:
                    q["gt"] = list(q["gt_idx"])
                if not q["boxes"]:
                    continue
                q["emb"], q["p_single"], q["p_blend"] = namer.run(q["img"], q["boxes"])
                q_gt = [names[g] if isinstance(g, int) else None for g in q["gt"]]
                d1 = anchor_decode(q["p_blend"], set(), {}, None, direction_known=True, w_rare=1.0)
                single_frame = d1.get("anchored_pred") or [LEVEL_ORDER[int(i)] for i in q["p_blend"].argmax(1)]
                mi = map_query_panorama(q, pano, nboxes, pitch_px)
                me = map_query_emb(q, chain)
                if mi is None and me is None:
                    continue
                o = mi["offset"] if mi is not None else me["offset"]
                true_offset = None
                if all(isinstance(g, int) for g in q["gt"]):
                    for oo in range(n_nodes - len(q["boxes"]) + 1):
                        if [chain[oo + j]["gt"] for j in range(len(q["boxes"]))] == q["gt"]:
                            true_offset = oo; break
                def at(seq, o_):
                    return [seq[o_ + j] if 0 <= o_ + j < n_nodes else None for j in range(len(q["boxes"]))]
                cn, mn, vn, hn = at(c_names, o), at(m_names, o), at(v_names, o), at(h_names, o)
                conf = [c for c in at(node_conf, o) if c is not None]
                # THE RETAKE. The same bodies, shot from a quarter of a vertebra higher or lower, which is what a
                # radiographer does when told the frame cannot be placed. Scored identically, so the pair says
                # whether a decline costs an exposure or costs the level.
                retake = None
                if a.retake and 0 <= q["start"] and q["start"] + K < len(names):
                    try:
                        rq = cut_query(sp, q["start"], K, pitch_px, rng, a.perturb, film_params,
                                       shift=float(rng.choice([-a.retake, a.retake])))
                        if a.boxes == "det":
                            rdb = detect_boxes(det, rq["img"], conf=a.det_conf)
                            if a.box_repair:
                                rdb, _ = repair_boxes(rdb)
                            rq["gt"] = assign_gt(rdb, rq["all_boxes"], rq["all_idx"]); rq["boxes"] = rdb
                        else:
                            rq["gt"] = list(rq["gt_idx"])
                        if rq["boxes"]:
                            rq["emb"], rq["p_single"], rq["p_blend"] = namer.run(rq["img"], rq["boxes"])
                            rmi = map_query_panorama(rq, pano, nboxes, pitch_px)
                            rme = map_query_emb(rq, chain)
                            if rmi is not None or rme is not None:
                                ro = rmi["offset"] if rmi is not None else rme["offset"]
                                rgt = [names[g] if isinstance(g, int) else None for g in rq["gt"]]
                                rn = [m_names[ro + j] if 0 <= ro + j < n_nodes else None for j in range(len(rq["boxes"]))]
                                rconf = [node_conf[ro + j] for j in range(len(rq["boxes"])) if 0 <= ro + j < n_nodes]
                                rc, rt = _acc(rn, rgt)
                                retake = {"shift": rq["shift"], "correct": rc, "total": rt,
                                          "conf": round(float(min(rconf)), 4) if rconf else None,
                                          "joint_conf": round(float(min(rconf)) * float(np.clip(chain_margin / 0.2, 0, 1)), 4) if rconf else None}
                    except Exception:  # noqa: BLE001
                        retake = None
                qrec = {"K": len(q["boxes"]), "K_asked": K, "start": q["start"], "gt": q_gt, "single_frame": single_frame,
                        "retake": retake,
                        "sweep_count": cn, "sweep_morph": mn, "sweep_variant": vn, "sweep_hybrid": hn,
                        "conf": round(float(min(conf)), 4) if conf else None,
                        "chain_margin": round(chain_margin, 4),
                        "joint_conf": round(float(min(conf)) * float(np.clip(chain_margin / 0.2, 0, 1)), 4) if conf else None,
                        "offset": o, "true_offset": true_offset, "mapped_right": bool(true_offset == o),
                        "map_by": "image" if mi is not None else "embedding",
                        "map_ncc": mi["ncc"] if mi else None, "map_inconsistent": bool(mi.get("inconsistent")) if mi else None,
                        "emb_offset": me["offset"] if me else None, "emb_right": bool(me and true_offset == me["offset"]),
                        "emb_margin": me["margin"] if me else None}
                rec["queries"].append(qrec)
        records.append(rec)
        if (ai + 1) % 50 == 0:
            print(f"  {ai + 1}/{len(anns)} spines, {time.time() - t0:.0f}s", flush=True)

    # ------------------------------------------------------------------ summary
    done = [r for r in records if "skipped" not in r]
    summ = {"config": {"span": a.span, "span_mm": span_mm, "overlap": a.overlap, "boxes": a.boxes, "perturb": a.perturb, "ks": a.ks,
                       "anchor": a.anchor, "link": a.link, "det_conf": a.det_conf, "box_repair": a.box_repair,
                       "hybrid": a.hybrid, "node_merge": a.node_merge, "node_order": a.node_order, "variant_tau": a.variant_tau, "link_window": a.link_window,
                       "end_rule": a.end_rule, "last_link": a.last_link, "rib": a.rib, "rib_weight": a.rib_weight, "alphabets": a.alphabets,
                       "model": a.model, "model_sha256": namer.model_sha, "head": a.head, "head_sha256": namer.head_sha,
                       "detector": a.detector, "seed": a.seed, "sources": a.drr, "tta": not a.no_tta,
                       "step_jitter": a.step_jitter, "cases": a.cases,
                       "link_solve": a.link_solve, "shift": a.shift, "place": a.place,
                       "role_head": a.role_head, "role_head_sha256": getattr(namer, "role_sha", None), "w_role": a.w_role,
                       "pseudo_truth": bool(done and all(r["pseudo_truth"] for r in done)),
                       "held_out": bool(a.holdout_bank) or bool(a.fold), "holdout_bank": a.holdout_bank,
                       "fold": a.fold,
                       "films_refused_as_trained_on": int(n_refused_trained)},
            "spines": len(done), "skipped": len(records) - len(done), "by_class": {}}
    classes = sorted({r["class"] for r in done})
    for cl in classes + ["all"]:
        rs = [r for r in done if cl == "all" or r["class"] == cl]
        if not rs:
            continue
        ent = {"spines": len(rs), "stations_mean": round(float(np.mean([r["stations"] for r in rs])), 2),
               "chain_complete": round(float(np.mean([(r["duplicates"] == 0 and r["missed"] == 0 and r["false_positive"] == 0 and r["conflict"] == 0) for r in rs])), 4),
               "duplicates_per_spine": round(float(np.mean([r["duplicates"] for r in rs])), 3),
               "missed_per_spine": round(float(np.mean([r["missed"] for r in rs])), 3),
               "false_positive_per_spine": round(float(np.mean([r["false_positive"] for r in rs])), 3),
               "unlabelled_per_spine": round(float(np.mean([r.get("unlabelled", 0) for r in rs])), 3),
               "conflict_per_spine": round(float(np.mean([r["conflict"] for r in rs])), 3),
               "anchor_present": round(float(np.mean([r["anchor_present"] for r in rs])), 4),
               "links": int(sum(len(r["links"]) for r in rs)),
               "link_emb_agrees": round(float(np.mean([l["m"] == l["m_emb"] for r in rs for l in r["links"]])), 4) if any(r["links"] for r in rs) else None,
               "count_vs_morph_disagree_spines": round(float(np.mean([r["count_vs_morph_disagree"] > 0 for r in rs])), 4),
               "chain_margin_median": round(float(np.median([r.get("chain_margin", 1.0) for r in rs])), 4)}
        ok = [r for r in rs if r["duplicates"] == 0 and r["missed"] == 0 and r["false_positive"] == 0 and r["conflict"] == 0]
        if ok:
            acc, ci = cluster_boot([(r["chain_acc"]["variant"][0], r["chain_acc"]["variant"][1]) for r in ok])
            ent["chain_variant_given_complete"] = {"acc": acc, "ci95": ci, "spines": len(ok)}
        for m in ("count", "morph", "single", "variant", "hybrid"):
            acc, ci = cluster_boot([(r["chain_acc"][m][0], r["chain_acc"][m][1]) for r in rs])
            ent[f"chain_{m}"] = {"acc": acc, "ci95": ci}
        calls = Counter(r.get("variant_call") for r in rs)
        ent["variant_call"] = {k: round(v / len(rs), 4) for k, v in calls.items()}
        for K in a.ks:
            for meth in ("single_frame", "sweep_count", "sweep_morph", "sweep_variant", "sweep_hybrid"):
                per = []
                for r in rs:
                    qs = [q for q in r["queries"] if q["K"] == K]
                    c = sum(_acc(q[meth], q["gt"])[0] for q in qs); t = sum(_acc(q[meth], q["gt"])[1] for q in qs)
                    per.append((c, t))
                acc, ci = cluster_boot(per)
                ent[f"K{K}_{meth}"] = {"acc": acc, "ci95": ci, "n": int(sum(t for _, t in per))}
            for key, fld in (("mapped_right", "mapped_right"), ("emb_right", "emb_right")):
                per = [(sum(q[fld] for q in r["queries"] if q["K"] == K), sum(1 for q in r["queries"] if q["K"] == K)) for r in rs]
                acc, ci = cluster_boot(per)
                ent[f"K{K}_{key}"] = {"acc": acc, "ci95": ci}
            by_img = [q["map_by"] == "image" for r in rs for q in r["queries"] if q["K"] == K]
            ent[f"K{K}_mapped_by_image"] = round(float(np.mean(by_img)), 4) if by_img else None
            # accuracy at a stated coverage: sort the frames by the decode's own confidence and keep the top
            # share. A system that must be right 99% of the time is allowed to decline; what it declines is
            # reported rather than hidden.
            for key, fld in (("at_coverage", "conf"), ("at_coverage_joint", "joint_conf")):
                pool = [(q[fld], _acc(q["sweep_hybrid"], q["gt"])) for r in rs for q in r["queries"]
                        if q["K"] == K and q.get(fld) is not None]
                pool.sort(key=lambda t: -t[0])
                cov = {}
                for frac in (1.0, 0.95, 0.9, 0.8, 0.7, 0.5):
                    keep = pool[: max(1, int(round(frac * len(pool))))] if pool else []
                    c = sum(a[0] for _, a in keep); t = sum(a[1] for _, a in keep)
                    cov[str(frac)] = {"acc": round(c / t, 4) if t else None, "n": t}
                ent[f"K{K}_{key}"] = cov
        summ["by_class"][cl] = ent
    json.dump(EG.stamp({"summary": summ, "records": records}, gate), open(out / "sweep.json", "w"), indent=1,
              default=_json_default)

    print(f"\nspines {len(done)} (skipped {len(records) - len(done)}); stations/spine {summ['by_class'].get('all', {}).get('stations_mean')}")
    print(f"{'class':<14}{'n':>5}  {'chain ok':>8}  {'count':>7}  {'morph':>7}  {'hybrid':>7}  {'single':>7}  " + "  ".join(f"K{K}:frame/shape/hybrid(map)" for K in a.ks))
    for cl, e in summ["by_class"].items():
        def f(x):
            return "  -  " if x is None or x.get("acc") is None else f"{100 * x['acc']:5.1f}"
        row = f"{cl:<14}{e['spines']:>5}  {100 * e['chain_complete']:7.1f}%  {f(e['chain_count'])}  {f(e['chain_morph'])}  {f(e['chain_hybrid'])}  {f(e['chain_single'])}  "
        row += "  ".join(f"{f(e[f'K{K}_single_frame'])}/{f(e[f'K{K}_sweep_morph'])}/{f(e[f'K{K}_sweep_hybrid'])}({f(e[f'K{K}_mapped_right'])})" for K in a.ks)
        print(row)
    print(f"wrote {out / 'sweep.json'}")

    if a.contact_sheet:
        try:
            draw_contact_sheet(records, anns, a, out, span_mm, film_params)
        except Exception as e:  # noqa: BLE001
            print(f"contact sheet failed: {e}")
    return 0


def draw_contact_sheet(records, anns, a, out, span_mm, film_params):
    """A few sweeps, anomalous first: the stitched panorama with every node box, count and morphology names."""
    from PIL import Image, ImageDraw
    rng = np.random.RandomState(a.seed)
    by_case = {p.stem: (p, d) for p, d in anns}
    order = sorted([r for r in records if "skipped" not in r], key=lambda r: (r["class"] == "ordinary", r["case"]))
    picked = order[: a.contact_sheet]
    panels = []
    for r in picked:
        sp = load_spine(*by_case[r["case"]])
        if sp is None:
            continue
        pitch_px, px_per_mm = body_pitch_px(sp)
        sp["_sacrum_part"] = sacrum_part(sp)
        anchor = r["anchor"] if r["anchor"] != "none" else "cranial"
        st = make_stations(sp, span_mm * px_per_mm, a.overlap, pitch_px, anchor, rng, a.perturb, film_params,
                           step_jitter=a.step_jitter)
        for s_ in st:
            s_["gt"] = list(s_["gt_idx"]); s_["emb"] = np.zeros((len(s_["boxes"]), 4)); s_["p_single"] = np.zeros((len(s_["boxes"]), len(LEVEL_ORDER))); s_["p_blend"] = s_["p_single"]
        prior_dy = -(span_mm * px_per_mm - a.overlap * pitch_px)
        links = [link_pair(st[i - 1], st[i], pitch_px, prior_dy) for i in range(1, len(st))]
        pano, pos, pboxes = build_panorama(st, [{"shift": lk["shift"]} for lk in links], prior_dy)
        im = Image.fromarray(pano).convert("RGB")
        dr = ImageDraw.Draw(im)
        for p, s_ in zip(pos, st):
            h, w = s_["img"].shape
            dr.rectangle([p[1], p[0], p[1] + w - 1, p[0] + h - 1], outline=(90, 90, 200), width=1)
        for bs in pboxes:
            for b in bs:
                dr.rectangle(b, outline=(255, 200, 0), width=2)
        W0 = im.size[0]
        strip = Image.new("RGB", (W0 + 420, max(im.size[1], 120)), (20, 20, 20))
        strip.paste(im, (0, 0))
        dr = ImageDraw.Draw(strip)
        y = 6
        dr.text((W0 + 8, y), f"{r['case']}  {r['class']}  stations {r['stations']}  nodes {r['chain_nodes']}  dup {r['duplicates']} miss {r['missed']} fp {r['false_positive']} unlabelled {r.get('unlabelled', 0)} conflict {r['conflict']}", fill=(255, 255, 255)); y += 16
        dr.text((W0 + 8, y), "truth: " + " ".join(str(n) for n in r["gt_names"]), fill=(180, 255, 180)); y += 16
        dr.text((W0 + 8, y), "count: " + " ".join(str(n) for n in r["count_names"]), fill=(255, 255, 255)); y += 16
        dr.text((W0 + 8, y), "morph: " + " ".join(str(n) for n in r["morph_names"]), fill=(255, 220, 120)); y += 16
        for lk in r["links"]:
            dr.text((W0 + 8, y), f"link {lk['lower']}->{lk['upper']}: shared {lk['m']} (embeddings alone {lk['m_emb']}) shift {lk['shift']}", fill=(200, 200, 200)); y += 14
        panels.append(strip)
    if not panels:
        return
    W = max(p.size[0] for p in panels); H = sum(p.size[1] for p in panels) + 6 * len(panels)
    sheet = Image.new("RGB", (W, H), (0, 0, 0))
    y = 0
    for p in panels:
        sheet.paste(p, (0, y)); y += p.size[1] + 6
    sheet.save(out / "contact_sheet.png")
    print(f"wrote {out / 'contact_sheet.png'}")


if __name__ == "__main__":
    raise SystemExit(main())
