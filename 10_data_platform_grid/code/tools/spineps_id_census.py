#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_id_census.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""What every SPINEPS vertebra mask on the grid actually means by its ids -- counted, not assumed.

WHY (2026-09-23). The TotalSegmentator bench masks ~/bench_ts/spineps/native/TS_<s>_seg-vert_msk.nii.gz were
read as VerSe-coded (L6 = 25) and "id 25 present" selected twelve "L6" spines. The S-I diagnostic (job 40424652)
found the ids spatially scrambled in all twelve: TS_s0224 has id 24 topmost and id 25 on the sacrum. By the
VERIDAH centroid file beside each mask only 2 of the 12 are L6. The COBRA Elekta harvest (cobra2026/seg/spineps)
had already been found carrying raw instance ids 1..N (A002 read C1..C5). The runner that wrote the older trees
harvested "the last file whose name holds seg-vert" until commit 147428d (2026-09-21 18:20), and SPINEPS also
writes a RAW instance mask (ids 1..N, no VERIDAH names). Nothing raises when a raw id is read as a VerSe name:
every downstream box, body mask and subtype call is finite and plausible. So every tree is censused.

WHAT IS MEASURED, per mask (seg-vert instance masks, their _veridah relabels, and the body masks derived from
them), all in world RAS millimetres from the NIfTI affine, never from an assumed axis order:
  * the id set, split into vertebrae (1-99), discs (100-199), end plates (200-299) and anything else;
  * VERSE-CODED?  every vertebra id in the VerSe alphabet (1-28: C1..L5 = 1..24, L6 = 25, sacrum 26, coccyx 27,
    T13 = 28);  CONTIGUOUS-FROM-1? the id set is exactly {1..N} (what a raw instance enumeration looks like --
    and also what a genuine C1..L5 whole spine looks like, so this alone decides nothing);
  * MONOTONIC?  read as VerSe names (T13 sits between T12 and L1, L6 between L5 and the sacrum), does every
    caudal name lie below every cranial one? A pair counts as inverted only when the caudal centroid is more
    than 5 mm ABOVE the cranial one. Also reported: monotonic in plain integer order (a raw 1..N enumeration
    that happens to run cranio-caudally is monotonic by integer and inverted by VerSe rank at 25-28);
  * THE SPINE AXIS: principal axis of the instance centroids and its cosine with world S; |cos| < 0.5 means the
    world S axis is not the spine (placeholder affine, CBCT) and S-order verdicts are marked suspect;
  * THE CTD beside the mask (VERIDAH's own names, the one ordered naming in these trees): its label set, whether
    ITS names are monotonic in S, and -- the decisive test -- for each named centroid, which instance id the mask
    holds at that world point. Agree = the mask carries VERIDAH's name there; disagree = it carries another id.
  * SIZE vs NAME, a check from outside the naming: median volume (ml) of the instances named cervical (1-7) and
    lumbar (20-25). A cervical vertebra is ~10-20 ml and a lumbar one ~60-90 ml whole; a mask whose "C1..C5" are
    lumbar-sized is a raw enumeration read as names. Reported, and used only to classify masks with no ctd.

VERDICT (one per mask). "Tested" = at least two ctd centroids land inside some instance of the mask.
  verse_ok                  VerSe-coded, monotonic, and every ctd centroid that lands in the mask lands in the
                            instance carrying its own name
  misnamed_1_2_levels       monotonic, VerSe-named, but the ctd puts a different name on 1-2 instances (< 30 % of
                            the tested centroids): an L6 sliver at the lumbosacral junction, an id-26 fragment at the
                            FOV edge -- a defect of VERIDAH's output, not of the id scheme
  veridah_order_error       carries (nearly) the ctd's names, and those names are themselves out of S order
                            (e.g. 'S' named above L5): VERIDAH's naming is inverted, the ids faithfully copy it
  scrambled                 >= 30 % of the tested ctd centroids land in an instance of ANOTHER id and the ids are
                            not S-ordered as VerSe names: the ids are not VERIDAH's names (a raw enumeration)
  ordered_but_not_names     >= 30 % disagreement but S-ordered (a raw enumeration that happens to run
                            cranio-caudally, or names shifted by a level)
  verse_monotonic_no_ctd    VerSe-coded and monotonic, no ctd test possible (size check reported)
  scrambled_no_ctd          not S-ordered as VerSe names, no ctd test possible
  non_verse_ids / empty / unreadable
and a separate flag RAW_INSTANCE: ids exactly 1..N and (>= 30 % ctd disagreement, or -- with no ctd test -- the
size check contradicts the names). A genuine C1.. whole spine is also 1..N; the disagreement is what separates them.

    python tools/spineps_id_census.py census --list files.tsv --shard 0 --n-shards 48 --out rows_0.jsonl
    python tools/spineps_id_census.py aggregate --rows 'rows_*.jsonl' --list files.tsv --out-json census.json
    python tools/spineps_id_census.py report --census census.json --preamble CENSUS_reading.md --out-md CENSUS.md
    python tools/spineps_id_census.py components --label 26 --out cc.json <mask> [<mask> ...]
    python tools/spineps_id_census.py one <mask>                     (one row, for a smoke test)
Grid driver: slurm/spineps_id_census.sh {find|census|aggregate} (ROWS=<dir> for a fresh rows set).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

TOL_MM = 5.0                       # a pair is inverted only if the caudal centroid is > TOL_MM above the cranial
VERSE = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
         **{19 + i: f"L{i}" for i in range(1, 7)}, 26: "S", 27: "Co", 28: "T13"}
MIN_VOX = 50                       # an instance this small is a speck; kept in the id set, left out of the S order


def verse_rank(i: int) -> float:
    return {28: 19.5, 25: 24.5}.get(i, float(i))


def name(i: int) -> str:
    return VERSE.get(i, str(i))


def kind_of(fname: str) -> str:
    n = fname.lower()
    if n.endswith("_body_msk.nii.gz"):
        return "body"
    if "seg-vert" in n:
        if "raw" in n:
            return "seg-vert-raw"
        if "veridah" in n:
            return "seg-vert-veridah"
        return "seg-vert"
    return "other"


# ------------------------------------------------------------------------------------------------ ctd reading
def read_ctd(path: str) -> dict:
    """Return {'format', 'labels': {label: world_ras_xyz or None}, 'si_only': {label: s_value}}.

    TPTBox POI files: [header{zoom, origin, rotation, direction, format}, ..., {label: {subregion: [x,y,z]}}],
    coordinates in VOXELS of the grid the header describes; world = rotation @ (xyz * zoom) + origin (RAS mm; the
    same transform tools/rare_class_ts_fixids.py and tools/spineps_relabel_from_poi.py use and that the S-I
    diagnostic validated on bench_ts). Legacy VerSe centroid files: [{direction}, {label, X, Y, Z}, ...] in voxels
    of the grid reoriented to `direction`, with no origin -- only the S-I ORDER is recoverable, not world points.
    """
    J = json.load(open(path))
    out = {"format": "unknown", "labels": {}, "si": {}}
    if isinstance(J, list) and J and isinstance(J[0], dict) and "zoom" in J[0] and isinstance(J[-1], dict):
        hdr = J[0]
        fmt = str(hdr.get("format", "POI"))
        out["format"] = f"tptbox:{fmt}"
        out["direction"] = hdr.get("direction")
        zoom = np.asarray(hdr["zoom"], float)
        origin = np.asarray(hdr["origin"], float)
        rot = np.asarray(hdr["rotation"], float)
        for k, sub in J[-1].items():
            try:
                lab = int(k)
            except ValueError:
                continue
            if not isinstance(sub, dict) or not sub:
                continue
            c = sub.get("50") or sub.get(50) or next(iter(sub.values()))
            c = np.asarray(c, float)
            if "GLOBAL" in fmt.upper():
                w = c
            else:
                w = rot @ (c * zoom) + origin
            out["labels"][lab] = [float(x) for x in w]
            out["si"][lab] = float(w[2])
        return out
    if isinstance(J, list) and J and isinstance(J[0], dict) and "direction" in J[0]:
        out["format"] = "verse_legacy"
        d = [str(x).upper() for x in J[0]["direction"]]
        out["direction"] = d
        ax = next((k for k, c in enumerate(d) if c in ("S", "I")), None)
        for e in J[1:]:
            if not isinstance(e, dict) or "label" not in e:
                continue
            xyz = [e.get("X"), e.get("Y"), e.get("Z")]
            if ax is None or xyz[ax] is None:
                continue
            s = float(xyz[ax]) * (1.0 if d[ax] == "S" else -1.0)
            out["labels"][int(e["label"])] = None
            out["si"][int(e["label"])] = s
        return out
    return out


def order_check(si: dict, rank=verse_rank) -> dict:
    """Pairs (cranial name, caudal name) whose caudal centroid lies more than TOL_MM above the cranial one."""
    ids = sorted(si, key=rank)
    inv = []
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            i, j = ids[a], ids[b]
            if rank(i) == rank(j):
                continue
            if si[j] > si[i] + TOL_MM:
                inv.append((i, j, round(si[j] - si[i], 1)))
    n_pairs = len(ids) * (len(ids) - 1) // 2
    adj = [(ids[k], ids[k + 1], round(si[ids[k + 1]] - si[ids[k]], 1)) for k in range(len(ids) - 1)
           if si[ids[k + 1]] > si[ids[k]] + TOL_MM]
    return dict(monotonic=not inv, n_inverted_pairs=len(inv), n_pairs=n_pairs,
                inverted_adjacent=[[name(i), name(j), d] for i, j, d in adj][:12],
                order_top_to_bottom=[name(i) for i in sorted(si, key=lambda x: -si[x])])


def find_ctd(mask_path: str) -> tuple[str | None, list[str]]:
    d, n = os.path.split(mask_path)
    m = re.match(r"(.*?)_seg-vert", n)
    prefix = m.group(1) if m else n.split("_body_msk")[0]
    cands = sorted(glob.glob(os.path.join(d, glob.escape(prefix) + "_*ctd*.json")))
    if not cands:
        cands = sorted(glob.glob(os.path.join(d, glob.escape(prefix) + "_*poi*.json")))
    pref = [c for c in cands if c.endswith("_ctd.json")] + [c for c in cands if not c.endswith("_ctd.json")]
    return (pref[0] if pref else None), cands


# ------------------------------------------------------------------------------------------------ one mask
def census_one(path: str) -> dict:
    import nibabel as nib

    t0 = time.time()
    rec = dict(path=path, kind=kind_of(os.path.basename(path)), is_link=os.path.islink(path),
               realpath=os.path.realpath(path))
    try:
        st = os.stat(path)
        rec["mtime"] = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
    except OSError as e:
        rec.update(verdict="unreadable", error=repr(e)[:300])
        return rec
    d, n = os.path.split(path)
    m = re.match(r"(.*?)_seg-vert", n)
    case = m.group(1) if m else n.split("_body_msk")[0]
    rec["case"] = case

    # the body masks: where did the ids come from?
    src_vert = None
    if rec["kind"] == "body":
        bj = os.path.join(d, f"{case}_body.json")
        if os.path.exists(bj):
            try:
                B = json.load(open(bj))
                src_vert = B.get("instance")
                rec["body_definition"] = B.get("definition")
                rec["body_source_instance"] = src_vert
                rec["body_source_semantic"] = B.get("semantic")
            except Exception as e:                                   # noqa: BLE001
                rec["body_json_error"] = repr(e)[:200]
        else:
            rec["body_json_error"] = "no _body.json beside the mask"
    # the harvest record (present only for masks harvested after commit 147428d)
    hj = os.path.join(d, f"{case}_harvest.json")
    if os.path.exists(hj):
        try:
            H = json.load(open(hj))
            ch = (H.get("vert") or {}).get("chosen")
            cands = (H.get("vert") or {}).get("candidates") or []
            rec["harvest"] = dict(chosen=ch, chosen_is_raw=bool(ch and "raw" in os.path.basename(ch).lower()),
                                  n_candidates=len(cands),
                                  candidates=[os.path.basename(c) for c in cands][:6])
        except Exception as e:                                       # noqa: BLE001
            rec["harvest"] = dict(error=repr(e)[:200])
    else:
        rec["harvest"] = None

    try:
        img = nib.load(path)
        arr = np.asanyarray(img.dataobj)
        if arr.dtype.kind == "f":
            arr = np.rint(arr).astype(np.int32)
        A = img.affine
    except Exception as e:                                           # noqa: BLE001
        rec.update(verdict="unreadable", error=repr(e)[:300])
        return rec
    rec["shape"] = list(arr.shape)
    rec["axcodes"] = "".join(nib.aff2axcodes(A))
    zooms = np.sqrt((A[:3, :3] ** 2).sum(0))
    rec["zooms"] = [round(float(z), 4) for z in zooms]
    vox_ml = float(abs(np.linalg.det(A[:3, :3]))) / 1000.0

    nz = np.nonzero(arr)
    vals = arr[nz].astype(np.int64)
    if vals.size == 0:
        rec.update(ids=[], verdict="empty", seconds=round(time.time() - t0, 1))
        return rec
    if vals.min() < 0:
        rec["negative_ids"] = True
        keep = vals > 0
        nz = tuple(x[keep] for x in nz)
        vals = vals[keep]
    mx = int(vals.max())
    cnt = np.bincount(vals, minlength=mx + 1)
    sums = [np.bincount(vals, weights=nz[k].astype(np.float64), minlength=mx + 1) for k in range(3)]
    ids_all = [int(i) for i in np.nonzero(cnt)[0] if i > 0]
    vert = [i for i in ids_all if i < 100]
    rec["ids"] = vert
    rec["disc_ids"] = [i for i in ids_all if 100 <= i < 200]
    rec["endplate_ids"] = [i for i in ids_all if 200 <= i < 300]
    rec["other_ids"] = [i for i in ids_all if i >= 300]
    if not vert:
        rec.update(verdict="empty", seconds=round(time.time() - t0, 1))
        return rec
    cen = {}
    vol = {}
    for i in vert:
        ijk = np.array([sums[k][i] / cnt[i] for k in range(3)])
        w = A[:3, :3] @ ijk + A[:3, 3]
        cen[i] = w
        vol[i] = cnt[i] * vox_ml
    rec["n_vox"] = {str(i): int(cnt[i]) for i in vert}
    rec["vol_ml"] = {str(i): round(vol[i], 2) for i in vert}
    rec["centroid_ras"] = {str(i): [round(float(x), 1) for x in cen[i]] for i in vert}

    # AN ID IN TWO PLACES. A centroid hides a small far fragment: on CTSP_0795 id 26 is the sacrum (277 ml) AND a
    # 1.2 ml piece of the FOV-cut T10 at the top edge, 220 mm above it -- the ctd's T10 centroid lands in that piece
    # and a box drawn round "id 26" would span the whole column. So every id's connected components (26-connected)
    # are counted; a component of >= 0.2 ml other than the largest, whose centroid lies > 30 mm from the largest's
    # in S, is a detached fragment.
    try:
        from scipy import ndimage
        order_ = np.argsort(vals, kind="stable")
        sv = vals[order_]
        bounds = np.searchsorted(sv, np.arange(mx + 2))
        frag = {}
        min_frag = max(1, int(round(0.2 / vox_ml))) if vox_ml > 0 else 1
        for i in vert:
            sl = order_[bounds[i]:bounds[i + 1]]
            if len(sl) < 2 * min_frag:
                continue
            idx = np.stack([nz[k][sl] for k in range(3)], 1)
            lo = idx.min(0)
            box = np.zeros(idx.max(0) - lo + 1, bool)
            box[tuple((idx - lo).T)] = True
            lab, n = ndimage.label(box, structure=np.ones((3, 3, 3), bool))
            if n < 2:
                continue
            labs = lab[tuple((idx - lo).T)]
            sizes = np.bincount(labs, minlength=n + 1)
            big_ = int(np.argmax(sizes[1:]) + 1)
            w_all = (A[:3, :3] @ idx.T).T + A[:3, 3]
            s_main = float(w_all[labs == big_, 2].mean())
            det = []
            for k in range(1, n + 1):
                if k == big_ or sizes[k] < min_frag:
                    continue
                s_k = float(w_all[labs == k, 2].mean())
                if abs(s_k - s_main) > 30.0:
                    det.append([round(float(sizes[k] * vox_ml), 2), round(s_k - s_main, 1)])
            if det:
                frag[str(i)] = sorted(det, key=lambda d: -d[0])[:4]
        rec["detached_fragments"] = frag          # id -> [[ml, S offset from the main component (mm)], ...]
    except Exception as e:                           # noqa: BLE001
        rec["detached_fragments_error"] = repr(e)[:200]

    # the ctd
    ctd_path, ctd_cands = find_ctd(src_vert if src_vert else path)
    rec["ctd"] = ctd_path
    rec["ctd_candidates"] = [os.path.basename(c) for c in ctd_cands]
    agree = disagree = empty = outside = in_extra = 0
    near_agree = near_disagree = 0
    dis_examples = []
    if ctd_path:
        try:
            C = read_ctd(ctd_path)
            rec["ctd_format"] = C["format"]
            rec["ctd_labels"] = sorted(C["si"])
            rec["ctd_verse_coded"] = all(1 <= i <= 28 for i in C["si"])
            co = order_check(C["si"])
            rec["ctd_mono"] = co["monotonic"]
            rec["ctd_inverted_adjacent"] = co["inverted_adjacent"]
            rec["ctd_order_top_to_bottom"] = co["order_top_to_bottom"]
            Minv = np.linalg.inv(A)
            for lab, w in C["labels"].items():
                if w is None:
                    continue
                x = Minv @ np.r_[np.asarray(w, float), 1.0]
                ix = np.rint(x[:3]).astype(int)
                if (ix < 0).any() or (ix >= np.array(arr.shape)).any():
                    outside += 1
                    continue
                v = int(arr[tuple(ix)])
                if 0 < v < 100:
                    if v == lab:
                        agree += 1
                    else:
                        disagree += 1
                        dis_examples.append([name(lab), v])
                        if not 1 <= v <= 28:
                            in_extra += 1
                    continue
                lo = np.clip(ix - 2, 0, None)
                hi = np.minimum(ix + 3, arr.shape)
                win = arr[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
                win = win[(win > 0) & (win < 100)]
                if win.size:
                    u, c = np.unique(win, return_counts=True)
                    vv = int(u[np.argmax(c)])
                    if vv == lab:
                        near_agree += 1
                    else:
                        near_disagree += 1
                else:
                    empty += 1
            # rank-match: the name each instance WOULD carry if it took the nearest-in-S ctd name
            rec["ctd_agree"] = agree
            rec["ctd_disagree"] = disagree
            rec["ctd_near_agree"] = near_agree
            rec["ctd_near_disagree"] = near_disagree
            rec["ctd_empty"] = empty
            rec["ctd_outside"] = outside
            rec["ctd_disagree_examples"] = dis_examples[:40]
            rec["ctd_in_extra_id"] = in_extra
            rec["ids_not_in_ctd"] = [i for i in vert if i not in C["si"]]
            rec["ctd_not_in_ids"] = [i for i in sorted(C["si"]) if i not in vert]
        except Exception as e:                                       # noqa: BLE001
            rec["ctd_error"] = repr(e)[:300]
    classify(rec)
    rec["seconds"] = round(time.time() - t0, 1)
    return rec


EXTRA_IDS = (80,)   # an id outside the VerSe alphabet that SPINEPS writes into otherwise VerSe-named masks (590 masks
                    # on 2026-09-23, median 14 voxels); what it stands for is not established here, so it is reported
                    # and kept out of the naming tests rather than guessed at


def classify(rec: dict) -> dict:
    """Derived flags and the verdict, from the measured fields only -- so `aggregate` can re-derive them from the
    stored rows without re-reading a mask (the rule was refined once already: id 80 had been read as a non-VerSe
    vertebra and pushed 530 VerSe-named, ctd-confirmed masks into a 'nonmonotonic' bin)."""
    if rec.get("verdict") in ("unreadable",) or not rec.get("ids"):
        if rec.get("verdict") is None:
            rec["verdict"] = "empty"
        return rec
    ids = rec["ids"]
    nvox = {int(k): v for k, v in rec["n_vox"].items()}
    cen = {int(k): v for k, v in rec["centroid_ras"].items()}
    vol = {int(k): v for k, v in rec["vol_ml"].items()}
    extra = [i for i in ids if i in EXTRA_IDS]
    core = [i for i in ids if i not in EXTRA_IDS]
    rec["extra_ids"] = {str(i): nvox[i] for i in extra}
    rec["extra_vertebra_sized"] = [i for i in extra if vol[i] >= 5.0]
    big = [i for i in core if nvox[i] >= MIN_VOX]
    rec["specks"] = [i for i in core if nvox[i] < MIN_VOX]
    rec["verse_coded"] = bool(core) and all(1 <= i <= 28 for i in big)
    rec["contiguous_from_1"] = core == list(range(1, len(core) + 1))
    named = [i for i in big if 1 <= i <= 28]
    si = {i: float(cen[i][2]) for i in named}
    oc = order_check(si)
    rec["mono_verse"] = oc["monotonic"]
    rec["n_inverted_pairs"] = oc["n_inverted_pairs"]
    rec["n_pairs"] = oc["n_pairs"]
    rec["inverted_adjacent"] = oc["inverted_adjacent"]
    rec["order_top_to_bottom"] = oc["order_top_to_bottom"]
    si_all = {i: float(cen[i][2]) for i in big}
    rec["mono_int"] = order_check(si_all, rank=float)["monotonic"]
    rec["mono_int_reversed"] = order_check(si_all, rank=lambda x: -float(x))["monotonic"]
    if len(big) >= 3:
        P = np.array([cen[i] for i in big], float)
        P = P - P.mean(0)
        _, _, vt = np.linalg.svd(P, full_matrices=False)
        rec["spine_axis_cos_S"] = round(float(abs(vt[0][2])), 3)
    else:
        rec["spine_axis_cos_S"] = None
    rec["orientation_suspect"] = rec["spine_axis_cos_S"] is not None and rec["spine_axis_cos_S"] < 0.5
    # size vs name (outside the naming)
    cerv = [vol[i] for i in big if 1 <= i <= 7]
    lumb = [vol[i] for i in big if 20 <= i <= 25]
    rec["median_ml_named_cervical"] = round(float(np.median(cerv)), 1) if cerv else None
    rec["median_ml_named_lumbar"] = round(float(np.median(lumb)), 1) if lumb else None
    scale = 0.5 if rec.get("kind") == "body" else 1.0        # a body is about half its vertebra
    size_bad = bool((len(cerv) >= 2 and np.median(cerv) > 40.0 * scale)
                    or (len(lumb) >= 2 and np.median(lumb) < 15.0 * scale)
                    or (len(cerv) >= 2 and len(lumb) >= 2 and np.median(cerv) > np.median(lumb)))
    rec["size_contradicts_names"] = size_bad
    # ctd: a centroid that lands in an EXTRA id is not a naming disagreement between two vertebra names
    agree = rec.get("ctd_agree") or 0
    ex = rec.get("ctd_disagree_examples") or []
    dis_total = rec.get("ctd_disagree") or 0
    if "ctd_in_extra_id" in rec:
        in_extra = rec["ctd_in_extra_id"]
    else:                                   # rows written before the split was recorded: exact when <= 10 examples
        in_extra = sum(1 for _, v in ex if v in EXTRA_IDS)
    disagree = dis_total - in_extra
    rec["ctd_disagree_named"] = disagree
    has_ctd_test = bool(rec.get("ctd")) and (agree + disagree) >= 2
    rec["ctd_tested"] = has_ctd_test
    # A raw enumeration disagrees with VERIDAH's names at chance (TS_s0224: 22 of 23); a VerSe-named mask that
    # differs from its own ctd does so at one or two levels (an L6 sliver at the lumbosacral junction, a fragment
    # at the FOV edge). 30 % separates the two with room on both sides (census 2026-09-23).
    frac = disagree / (agree + disagree) if (agree + disagree) else 0.0
    ids_are_not_names = has_ctd_test and disagree >= 2 and frac >= 0.3
    rec["ctd_disagree_frac"] = round(frac, 3)
    if has_ctd_test:
        if ids_are_not_names:
            v = "ordered_but_not_names" if rec["mono_verse"] else "scrambled"
        elif disagree == 0 and rec["mono_verse"] and rec["verse_coded"]:
            v = "verse_ok"
        elif rec["mono_verse"]:
            v = "misnamed_1_2_levels"
        else:
            # the mask carries (nearly) the ctd's names, and those names are out of S order: VERIDAH's own
            # naming is inverted (e.g. 'S' named above L5), not an id-scheme problem
            v = "veridah_order_error"
    else:
        if rec["mono_verse"] and rec["verse_coded"]:
            v = "verse_monotonic_no_ctd"
        elif not rec["mono_verse"]:
            v = "scrambled_no_ctd"
        else:
            v = "non_verse_ids"
    rec["verdict"] = v
    rec["raw_instance"] = bool(rec["contiguous_from_1"] and (
        ids_are_not_names or (not has_ctd_test and size_bad)))
    return rec


def cmd_census(a) -> int:
    lines = [l.rstrip("\n").split("\t") for l in open(a.list) if l.strip()]
    paths = []
    for parts in lines:
        p = parts[-1]
        if p.endswith(".nii.gz") and kind_of(os.path.basename(p)) != "other":
            paths.append(p)
    paths = sorted(set(paths))
    mine = [p for k, p in enumerate(paths) if k % a.n_shards == a.shard]
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out):
            try:
                done.add(json.loads(l)["path"])
            except Exception:                                        # noqa: BLE001
                pass
    print(f"shard {a.shard}/{a.n_shards}: {len(mine)} masks ({len(done)} already done)", flush=True)
    with open(a.out, "a") as fh:
        for k, p in enumerate(mine):
            if p in done:
                continue
            try:
                r = census_one(p)
            except Exception as e:                                   # noqa: BLE001
                r = dict(path=p, verdict="unreadable", error=repr(e)[:300])
            fh.write(json.dumps(r) + "\n")
            fh.flush()
            if k % 50 == 0:
                print(f"  {k}/{len(mine)} {os.path.basename(p)} -> {r.get('verdict')} ({r.get('seconds')} s)", flush=True)
    print(f"SPINEPS_ID_CENSUS_SHARD_DONE {a.shard}", flush=True)
    return 0


# ------------------------------------------------------------------------------------------------ aggregate
def tree_of(path: str, per_dir: Counter) -> str:
    """A per-case layout (<tree>/<case>/<file>: every sibling directory holds <= 3 masks, and there are >= 2 of
    them) collapses onto <tree>; a small tree beside big ones (spinesac, spineps_retry134) keeps its own name."""
    d = os.path.dirname(path)
    parent = os.path.dirname(d)
    sibs = [k for k in per_dir if os.path.dirname(k) == parent]
    if per_dir[d] <= 3 and len(sibs) >= 2 and all(per_dir[k] <= 3 for k in sibs):
        return parent
    return d


def cmd_aggregate(a) -> int:
    rows = []
    for f in sorted(glob.glob(a.rows)):
        for l in open(f):
            if l.strip():
                rows.append(json.loads(l))
    # de-duplicate by path (a requeued shard may have appended twice)
    by_path = {}
    for r in rows:
        by_path[r["path"]] = r
    rows = [classify(r) for r in by_path.values()]      # re-derive: the rule may be newer than the rows
    listed = [l.rstrip("\n").split("\t")[-1] for l in open(a.list) if l.strip()]
    per_dir = Counter(os.path.dirname(r["path"]) for r in rows)
    all_ctd = [p for p in listed if p.endswith(".json") and "ctd" in os.path.basename(p)]
    ctd_dirs = Counter(os.path.dirname(p) for p in all_ctd)

    verdict_of_real = {}
    for r in rows:
        verdict_of_real[r.get("realpath", r["path"])] = r
        verdict_of_real[r["path"]] = r

    trees = defaultdict(list)
    for r in rows:
        trees[tree_of(r["path"], per_dir)].append(r)

    def offender_score(r):
        tier = {"scrambled": 3, "ordered_but_not_names": 3, "scrambled_no_ctd": 3, "veridah_order_error": 2,
                "misnamed_1_2_levels": 1}.get(r.get("verdict"), 0)
        if r.get("raw_instance"):
            tier = max(tier, 3)
        return (tier, r.get("ctd_disagree_named") or 0, r.get("n_inverted_pairs") or 0)

    summary = {}
    for t, rs in sorted(trees.items()):
        vc = Counter(r.get("verdict") for r in rs)
        kinds = Counter(r.get("kind") for r in rs)
        s = dict(
            n_masks=len(rs), kinds=dict(kinds), verdicts=dict(vc),
            n_verse_coded_monotonic=sum(1 for r in rs if r.get("verse_coded") and r.get("mono_verse")
                                        and not r.get("ctd_disagree_named")),
            n_verse_ok_ctd_confirmed=vc.get("verse_ok", 0),
            n_scrambled=sum(1 for r in rs if r.get("mono_verse") is False),
            n_scrambled_ids_not_names=vc.get("scrambled", 0) + vc.get("scrambled_no_ctd", 0),
            n_veridah_order_error=vc.get("veridah_order_error", 0),
            n_ordered_but_not_names=vc.get("ordered_but_not_names", 0),
            n_misnamed_1_2_levels=vc.get("misnamed_1_2_levels", 0),
            n_raw_instance=sum(1 for r in rs if r.get("raw_instance")),
            n_contiguous_from_1=sum(1 for r in rs if r.get("contiguous_from_1")),
            n_with_ctd=sum(1 for r in rs if r.get("ctd")),
            n_ctd_tested=sum(1 for r in rs if r.get("ctd_tested")),
            n_ctd_monotonic=sum(1 for r in rs if r.get("ctd_mono") is True),
            n_ctd_nonmonotonic=sum(1 for r in rs if r.get("ctd_mono") is False),
            n_ctd_any_disagree=sum(1 for r in rs if (r.get("ctd_disagree_named") or 0) > 0),
            n_extra_id=sum(1 for r in rs if r.get("extra_ids")),
            n_extra_id_vertebra_sized=sum(1 for r in rs if r.get("extra_vertebra_sized")),
            n_fragments_censused=sum(1 for r in rs if "detached_fragments" in r),
            n_detached_fragment_any=sum(1 for r in rs if r.get("detached_fragments")),
            n_detached_fragment_id26=sum(1 for r in rs if "26" in (r.get("detached_fragments") or {})),
            n_with_ids_25_counted=sum(1 for r in rs if "25" in (r.get("vol_ml") or {})),
            n_id25_sliver_lt5ml=sum(1 for r in rs if "25" in (r.get("vol_ml") or {}) and r["vol_ml"]["25"] < 5.0),
            n_id25_ge20ml=sum(1 for r in rs if ((r.get("vol_ml") or {}).get("25") or 0) >= 20.0),
            n_id28_ge20ml=sum(1 for r in rs if ((r.get("vol_ml") or {}).get("28") or 0) >= 20.0),
            n_before_harvest_fix_without_record=sum(1 for r in rs if not r.get("harvest")
                                                    and (r.get("mtime") or "9") < "2026-09-21 18:20"
                                                    and r.get("kind") == "seg-vert"),
            n_size_contradicts_names=sum(1 for r in rs if r.get("size_contradicts_names")),
            n_orientation_suspect=sum(1 for r in rs if r.get("orientation_suspect")),
            n_symlinks=sum(1 for r in rs if r.get("is_link")),
            n_harvest_record=sum(1 for r in rs if r.get("harvest")),
            n_harvest_chose_raw=sum(1 for r in rs if (r.get("harvest") or {}).get("chosen_is_raw")),
            n_with_ids_25=sum(1 for r in rs if 25 in (r.get("ids") or [])),
            n_with_ids_28=sum(1 for r in rs if 28 in (r.get("ids") or [])),
            n_with_ids_26=sum(1 for r in rs if 26 in (r.get("ids") or [])),
            n_with_disc_ids=sum(1 for r in rs if r.get("disc_ids")),
            mtime_range=[min((r.get("mtime") or "~") for r in rs), max((r.get("mtime") or "") for r in rs)],
            ctd_files_in_tree=sum(v for k, v in ctd_dirs.items() if k == t or os.path.dirname(k) == t),
        )
        # link targets
        tgt = Counter(os.path.dirname(r["realpath"]) for r in rs if r.get("is_link"))
        if tgt:
            s["symlink_targets"] = dict(tgt.most_common(5))
        # body masks: trace each to its source instance mask's verdict
        if kinds.get("body"):
            src = Counter()
            srcv = Counter()
            unresolved = 0
            ids_subset_bad = 0
            for r in rs:
                sp = r.get("body_source_instance")
                if not sp:
                    unresolved += 1
                    continue
                src[os.path.dirname(sp)] += 1
                sr = verdict_of_real.get(sp) or verdict_of_real.get(os.path.realpath(sp))
                if sr is None:
                    srcv["source_not_censused"] += 1
                else:
                    srcv[sr.get("verdict")] += 1
                    if not set(r.get("ids") or []) <= set(sr.get("ids") or []):
                        ids_subset_bad += 1
            s["body_sources"] = dict(src.most_common())
            s["body_source_verdicts"] = dict(srcv)
            s["body_without_source_record"] = unresolved
            s["body_ids_not_subset_of_source"] = ids_subset_bad
            s["body_naming"] = ("inherits the SOURCE instance id verbatim (tools/body_masks.py: instance id where the "
                                "semantic mask is 49/50); no ctd, no position match")
        offenders = sorted([r for r in rs if offender_score(r)[0] > 0], key=offender_score, reverse=True)
        # one example per verdict first, so a tree with several failure kinds shows each of them
        seen_v, first, rest = set(), [], []
        for r in offenders:
            (first if r.get("verdict") not in seen_v else rest).append(r)
            seen_v.add(r.get("verdict"))
        offenders = first + rest
        # spread examples over cases (not three from the same failure pattern if avoidable)
        ex = []
        for r in offenders[:3]:
            ex.append(dict(case=r.get("case"), path=r["path"], verdict=r.get("verdict"),
                           raw_instance=r.get("raw_instance"), ids=r.get("ids"),
                           order_top_to_bottom_as_verse=r.get("order_top_to_bottom"),
                           inverted_adjacent=r.get("inverted_adjacent", [])[:4],
                           ctd_order_top_to_bottom=r.get("ctd_order_top_to_bottom"),
                           ctd_agree=r.get("ctd_agree"), ctd_disagree=r.get("ctd_disagree_named"),
                           ctd_disagree_examples=r.get("ctd_disagree_examples", [])[:5],
                           median_ml_named_cervical=r.get("median_ml_named_cervical"),
                           median_ml_named_lumbar=r.get("median_ml_named_lumbar"),
                           body_source_instance=r.get("body_source_instance")))
        s["examples_offenders"] = ex
        summary[t] = s

    out = dict(
        generated=time.strftime("%Y-%m-%d %H:%M"),
        tool="tools/spineps_id_census.py",
        tolerance_mm=TOL_MM,
        n_masks=len(rows),
        n_ctd_files_found=len(all_ctd),
        verdict_totals=dict(Counter(r.get("verdict") for r in rows)),
        trees=summary,
        masks={r["path"]: dict(verdict=r.get("verdict"), raw_instance=r.get("raw_instance"),
                               ids=r.get("ids"), ctd_agree=r.get("ctd_agree"), ctd_disagree=r.get("ctd_disagree_named"),
                               mono_verse=r.get("mono_verse"), ctd_mono=r.get("ctd_mono"),
                               size_contradicts_names=r.get("size_contradicts_names"),
                               detached_fragments=r.get("detached_fragments") or None,
                               vol_ml_25=(r.get("vol_ml") or {}).get("25"), vol_ml_28=(r.get("vol_ml") or {}).get("28"),
                               harvest_record=bool(r.get("harvest")), is_link=bool(r.get("is_link")),
                               body_source_instance=r.get("body_source_instance")) for r in rows},
    )
    Path(a.out_json).write_text(json.dumps(out, indent=1))
    print(f"wrote {a.out_json}: {len(rows)} masks in {len(summary)} trees", flush=True)
    return 0


def cmd_components(a) -> int:
    """Where the voxels of one id actually are: its connected components (26-connectivity), each with volume,
    world S range and centroid, and which ctd centroids fall inside each. Used to settle a ctd centroid of a
    thoracic name landing in id 26 (sacrum): a second id-26 component up the column, or a misplaced centroid."""
    import nibabel as nib
    from scipy import ndimage
    out = []
    for p in a.paths:
        img = nib.load(p)
        arr = np.asanyarray(img.dataobj).astype(np.int32)
        A = img.affine
        vox_ml = float(abs(np.linalg.det(A[:3, :3]))) / 1000.0
        lab, n = ndimage.label(arr == a.label, structure=np.ones((3, 3, 3), bool))
        comps = []
        for k in range(1, n + 1):
            idx = np.argwhere(lab == k)
            w = (A[:3, :3] @ idx.T).T + A[:3, 3]
            comps.append(dict(component=k, voxels=int(len(idx)), ml=round(len(idx) * vox_ml, 2),
                              s_min=round(float(w[:, 2].min()), 1), s_max=round(float(w[:, 2].max()), 1),
                              centroid=[round(float(x), 1) for x in w.mean(0)], ctd_inside=[]))
        comps.sort(key=lambda c: -c["voxels"])
        ctd_path, _ = find_ctd(p)
        pois = {}
        if ctd_path:
            C = read_ctd(ctd_path)
            Minv = np.linalg.inv(A)
            for l, w in C["labels"].items():
                if w is None:
                    continue
                ix = np.rint((Minv @ np.r_[np.asarray(w, float), 1.0])[:3]).astype(int)
                inside = bool((ix >= 0).all() and (ix < np.array(arr.shape)).all())
                pois[name(l)] = dict(world=[round(float(x), 1) for x in w],
                                     mask_id_there=int(arr[tuple(ix)]) if inside else None)
                if inside and lab[tuple(ix)]:
                    k = int(lab[tuple(ix)])
                    for c in comps:
                        if c["component"] == k:
                            c["ctd_inside"].append(name(l))
        # S of every instance for context
        inst = {}
        for i in (int(x) for x in np.unique(arr) if 0 < x < 100):
            idx = np.argwhere(arr == i)
            w = (A[:3, :3] @ idx.T).T + A[:3, 3]
            inst[name(i)] = dict(ml=round(len(idx) * vox_ml, 2), s_min=round(float(w[:, 2].min()), 1),
                                 s_max=round(float(w[:, 2].max()), 1))
        rec = dict(path=p, label=a.label, n_components=n, components=comps[:8], ctd=ctd_path, pois=pois,
                   instances=inst)
        out.append(rec)
        print(json.dumps(rec), flush=True)
    if a.out:
        Path(a.out).write_text(json.dumps(out, indent=1))
    return 0


def cmd_report(a) -> int:
    """CENSUS.md from census.json: the hand-written reading (--preamble) on top, then the counted tables."""
    C = json.load(open(a.census))
    T = C["trees"]
    L = []
    if a.preamble and os.path.exists(a.preamble):
        L.append(Path(a.preamble).read_text().rstrip() + "\n")
    L.append(f"## Per-tree counts (generated {C['generated']} by `{C['tool']}`; {C['n_masks']} masks, "
             f"{C['n_ctd_files_found']} ctd files found)\n")
    L.append("Columns: **n** masks; **VerSe-mono** = ids all in the VerSe alphabet, cranio-caudal as VerSe names, "
             "no ctd centroid in another id; **ctd-ok** = of those, confirmed by >= 2 ctd centroids (verdict "
             "verse_ok); **scrambled** = ids are not VERIDAH's names (>= 30 % of ctd centroids in another id, not "
             "S-ordered; + scrambled_no_ctd); **ordered-not-names** = >= 30 % disagreement but S-ordered; **VERIDAH "
             "order** = the mask copies the ctd and the ctd's own names are out of S order; **1-2 lvl** = VerSe-named, "
             "S-ordered, ctd differs at 1-2 levels; **raw** = ids exactly 1..N and contradicted by the ctd (or size); "
             "**ctd** = masks with a ctd file (ctd names S-ordered / tested against the mask); **pre-fix** = seg-vert "
             "masks with no harvest record written before commit 147428d (2026-09-21 18:20); **harvest** = masks "
             "with a harvest record (of which the record says a raw file was chosen).\n")
    L.append("| tree | kind | n | VerSe-mono | ctd-ok | scrambled | ordered-not-names | VERIDAH order | 1-2 lvl | "
             "raw | ctd (mono/tested) | pre-fix | harvest (raw) | links | mtime |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    order = sorted(T, key=lambda t: (-T[t]["n_masks"]))
    for t in order:
        s = T[t]
        kinds = ",".join(f"{k}:{v}" for k, v in sorted(s["kinds"].items()))
        short = t.replace("/rs/rs_grp_oschome/go2432/", "/rs/.../").replace("/wsu/home/go/go24/go2432/", "~/")
        L.append(f"| `{short}` | {kinds} | {s['n_masks']} | {s['n_verse_coded_monotonic']} | "
                 f"{s['n_verse_ok_ctd_confirmed']} | {s['n_scrambled_ids_not_names']} | {s['n_ordered_but_not_names']} | "
                 f"{s['n_veridah_order_error']} | {s['n_misnamed_1_2_levels']} | "
                 f"{s['n_raw_instance']} | {s['n_with_ctd']} ({s['n_ctd_monotonic']}/{s['n_ctd_tested']}) | "
                 f"{s['n_before_harvest_fix_without_record']} | "
                 f"{s['n_harvest_record']} ({s['n_harvest_chose_raw']}) | {s['n_symlinks']} | "
                 f"{s['mtime_range'][0][:10]}..{s['mtime_range'][1][:10]} |")
    L.append("")
    L.append("## Defects that survive a correct harvest (counted in every tree)\n")
    L.append("**id25 <5 ml** = an L6 id holding under 5 ml (a sliver, not a vertebra); **id25/id28 >=20 ml** = an "
             "L6 / T13 id holding a vertebra-sized instance; **frag** = masks in which some id also occupies a "
             "detached component >= 0.2 ml more than 30 mm (in S) from its main one (of which id 26); **id 80** = "
             "masks carrying the non-VerSe id 80 (of which >= 5 ml). These read on raw trees too, where the id is "
             "an instance number and the column says nothing about L6.\n")
    L.append("| tree | n | id25 <5 ml | id25 >=20 ml | id28 >=20 ml | frag (id 26) | id 80 (>=5 ml) |")
    L.append("|---|---|---|---|---|---|---|")
    for t in order:
        s = T[t]
        short = t.replace("/rs/rs_grp_oschome/go2432/", "/rs/.../").replace("/wsu/home/go/go24/go2432/", "~/")
        fr = (f"{s.get('n_detached_fragment_any', 0)} ({s.get('n_detached_fragment_id26', 0)})"
              if s.get("n_fragments_censused") else "not censused")
        L.append(f"| `{short}` | {s['n_masks']} | {s.get('n_id25_sliver_lt5ml', 0)} | {s.get('n_id25_ge20ml', 0)} | "
                 f"{s.get('n_id28_ge20ml', 0)} | {fr} | {s.get('n_extra_id', 0)} ({s.get('n_extra_id_vertebra_sized', 0)}) |")
    L.append("")
    L.append("## Body-mask trees: where each body's ids came from\n")
    for t in order:
        s = T[t]
        if "body_sources" not in s:
            continue
        short = t.replace("/rs/rs_grp_oschome/go2432/", "/rs/.../").replace("/wsu/home/go/go24/go2432/", "~/")
        L.append(f"**`{short}`** ({s['n_masks']} bodies). Naming: {s['body_naming']}.\n")
        L.append("| source instance tree | bodies |")
        L.append("|---|---|")
        for src, n in s["body_sources"].items():
            L.append(f"| `{src.replace('/rs/rs_grp_oschome/go2432/', '/rs/.../').replace('/wsu/home/go/go24/go2432/', '~/')}` | {n} |")
        L.append("")
        L.append("Verdict of the source instance mask behind each body: "
                 + ", ".join(f"{k} {v}" for k, v in sorted(s["body_source_verdicts"].items(), key=lambda kv: -kv[1]))
                 + f". Bodies with no source record: {s['body_without_source_record']}; bodies whose ids are not a "
                 f"subset of their source's: {s['body_ids_not_subset_of_source']}.\n")
    L.append("## Three example offenders per tree\n")
    for t in order:
        ex = T[t]["examples_offenders"]
        short = t.replace("/rs/rs_grp_oschome/go2432/", "/rs/.../").replace("/wsu/home/go/go24/go2432/", "~/")
        if not ex:
            L.append(f"- `{short}`: none.")
            continue
        L.append(f"- `{short}`:")
        for e in ex:
            inv = "; ".join(f"{x[1]} sits {x[2]} mm above {x[0]}" for x in (e.get("inverted_adjacent") or [])[:3])
            dis = ", ".join(f"ctd {x[0]} lands in id {x[1]}" for x in (e.get("ctd_disagree_examples") or [])[:4])
            L.append(f"  - **{e['case']}** {e['verdict']}{' RAW' if e.get('raw_instance') else ''}: ids "
                     f"{e['ids']}; top-to-bottom as VerSe names {e.get('order_top_to_bottom_as_verse')}; ctd "
                     f"top-to-bottom {e.get('ctd_order_top_to_bottom')}; ctd agree/disagree "
                     f"{e.get('ctd_agree')}/{e.get('ctd_disagree')}"
                     + (f" ({dis})" if dis else "") + (f"; inverted adjacent: {inv}" if inv else "")
                     + (f"; median ml named cervical {e['median_ml_named_cervical']}, lumbar "
                        f"{e['median_ml_named_lumbar']}" if e.get('median_ml_named_cervical') or e.get('median_ml_named_lumbar') else "")
                     + (f"; body source `{e['body_source_instance']}`" if e.get("body_source_instance") else ""))
    L.append("")
    Path(a.out_md).write_text("\n".join(L) + "\n")
    print(f"wrote {a.out_md}", flush=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    k = sub.add_parser("components")
    k.add_argument("--label", type=int, default=26)
    k.add_argument("--out", default=None)
    k.add_argument("paths", nargs="+")
    r = sub.add_parser("report")
    r.add_argument("--census", required=True)
    r.add_argument("--out-md", required=True)
    r.add_argument("--preamble", default=None)
    c = sub.add_parser("census")
    c.add_argument("--list", required=True)
    c.add_argument("--shard", type=int, default=0)
    c.add_argument("--n-shards", type=int, default=1)
    c.add_argument("--out", required=True)
    g = sub.add_parser("aggregate")
    g.add_argument("--rows", required=True, help="glob of rows_*.jsonl")
    g.add_argument("--list", required=True)
    g.add_argument("--out-json", required=True)
    o = sub.add_parser("one")
    o.add_argument("path")
    a = ap.parse_args()
    if a.cmd == "census":
        return cmd_census(a)
    if a.cmd == "aggregate":
        return cmd_aggregate(a)
    if a.cmd == "report":
        return cmd_report(a)
    if a.cmd == "components":
        return cmd_components(a)
    print(json.dumps(census_one(a.path), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
