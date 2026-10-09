#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""A SPINEPS instance id is a vertebra's NAME only once that is shown: one guard that raises, one relabel that refuses.

WHY (2026-09-23). Before commit 147428d, benchmark/run_spineps_cases.py harvested "the last file whose name holds
seg-vert", which was SPINEPS's output_raw instance mask: ids 1..N in an arbitrary order, no VERIDAH names. 2,437
masks in ~/bench, ~/bench_ts, tsv3 (links), cobra2026/seg/spineps, deepfluoro and geneva_hip carry those ids
(SchwingNet/results/spineps_ids/CENSUS.md), and 2,714 body masks copied them. A raw id read as a VerSe id gives
a finite, plausible, wrong name, and nothing raised: "id 25 present" picked twelve "L6" TotalSegmentator spines
that were whole-spine fields of view (TS12_VERIFY.md). The ordered names were in the ctd json beside every mask
the whole time. This module is the one place the rule lives, so every reader that turns an id into a level uses
the same test.

THE GUARD -- assert_verse_monotonic(mask, ctd="auto")  (alias: assert_verse_named)
  Raises SpinepsIdError unless the mask's vertebra ids (1-99; id 80 set aside as in the census; discs and end
  plates >= 100 ignored; instances under 50 voxels left out of the order test):
    1. all lie in the VerSe alphabet (C1..L5 = 1..24, L6 = 25, sacrum 26, coccyx 27, T13 = 28);
    2. run cranio-caudally in WORLD S as VerSe names (T13 between T12 and L1, L6 between L5 and the sacrum; a pair
       is inverted when the caudal centroid lies > 5 mm above the cranial one), measured through the affine,
       never from an assumed axis order. If the instance column does not lie along world S (|cos| < 0.5, a
       placeholder affine) the order test is void and the ctd test has to carry the verdict;
    3. agree with the ctd beside the mask (VERIDAH's ordered names; TPTBox POI json): each named point, taken to
       world RAS through the POI header and back into the mask's voxels, lands in the instance with its own label.
       >= 2 disagreements and >= 30 % of the tested points = the ids are not names -> raises (a raw enumeration
       disagrees at chance, e.g. 22 of 23). 1-2 disagreements under 30 % are VERIDAH's own one-level defects (an
       L6 sliver whose point lies in the sacrum, an id-26 fragment at the FOV edge): allowed and reported, and
       raised only with strict=True. Thresholds are the census's (tools/spineps_id_census.py classify);
    4. and the ctd's own names run cranio-caudally (VERIDAH sometimes names 'S' above L5; a mask copying that is
       wrong however faithfully it copies: the SpineSAC phantom set1_A carries a 0.44 ml "sacrum" 200 mm above
       its L6, and closed_A a 0.16 ml one -- both became sacrum truth in or_ready/spinesac/truth);
    5. and, from outside the naming, VERIDAH's "cervical" vertebrae are not lumbar-sized (median > 40 ml; 20 ml
       for a body mask): carmlspine case134's plain mask names C1..C5 on 54-64 ml bones over an L2-S field. Only
       this cervical rule applies when a ctd exists (a lumbar floor would refuse children: TS v3).
  No ctd: require_ctd=True (the default) raises -- a genuine C1.. whole spine is also 1..N, and a raw mask of
  2-3 instances is monotonic by chance, so without the ctd the ids cannot be shown to be names. With
  require_ctd=False, a mask whose ids are exactly 1..N and whose sizes contradict the names (the census rule:
  "cervical" median > 40 ml, "lumbar" median < 15 ml, or cervical larger than lumbar; half that for body masks)
  is refused as a raw enumeration, and anything else passes as verse_ok_no_ctd.
  A body mask (tools/body_masks.py) is tested against the ctd of the instance mask it was cut from
  (<case>_body.json "instance").

THE RELABEL -- relabel_by_ctd(arr, affine, ctd_points, semantic=None)
  Generalises tools/rare_class_ts_fixids.py (z-rank alignment) with the position lookup of
  tools/spineps_relabel_from_poi.py, and refuses unless the two agree:
    a. the ctd itself must be usable: >= 2 points, VerSe labels, its presacral names strictly cranio-caudal in
       world S and the sacrum point below them. A mandatory name missing between two named points whose S gap is
       under (1 + 0.5 x missing) local spacings is a name SKIPPED at a normal spacing. The only one VERIDAH ever
       skips is T12 (census rows: 54 of 801 CTSP ctds, 47 of 1,144 TS v2, 36 of 374 VerSe) -- its encoding of an
       11-thoracic spine, i.e. a count call like its L6/T13 calls. It is reproduced as written and flagged
       (`veridah_skipped_names`), because a post-fix derivative carries it the same way; --refuse-skipped-names
       refuses it instead. On TS_s1178 it is shown wrong (the 12th ribs meet VERIDAH's "L1"), and that case is
       refused by name (KNOWN_VERIDAH_ERRORS). A wider gap is a vertebra SPINEPS did not find: accepted, reported;
    b. POSITION: each ctd point binds to the instance holding it (else the majority vertebra instance within 3
       voxels). One label per instance; a bound instance's centroid within 25 mm in S (45 for the sacrum) and 40 mm
       in 3-D (60) of its point. A named level with no instance is allowed only at an end of the column;
    c. RANK (fixids' test, now a cross-check): the vertebra-sized instances inside the named column, sorted by
       world S, must pair one-to-one with the bound presacral labels sorted anatomically, and that pairing must be
       the position binding. An unnamed vertebra-sized instance inside the column refuses the case (VERIDAH named
       fewer levels than SPINEPS found there); a fragment (< 15 % of the median named instance) is dropped;
    d. unnamed instances ABOVE the column: C1 when the top named level is C2 and exactly one vertebra-sized
       instance sits > 8 mm above the C2 point (VERIDAH's ctd never names C1); otherwise dropped and reported.
       THE SACRUM (26) is named ONLY from the SPINEPS semantic mask on the same grid: an instance that holds the
       ctd S point, or lies below the column, becomes 26 when >= 50 % of it is semantic sacrum, and the semantic
       sacrum voxels not already in a named vertebra also become 26 -- the whole sacrum, as the VERIDAH derivative
       carries it (CTSP_0795's 26 is 277 ml). A RAW semantic mask has no class 26 (smoke job 40425314: COLONOG_1,
       TS_s0224), and the raw instance that holds the S point is an 8-40 ml S1-level piece (10 of 853 raw
       bench_ts masks; fixids gave 26 to 380-684-voxel fragments, TS12_VERIFY). So a mask relabelled from a raw
       tree carries NO sacrum (report "sacrum": "absent: ..."): take the sacrum from another labeller;
    e. the result must pass the guard with ZERO ctd disagreements, or nothing is written.
  Whatever is refused raises RelabelRefused (a SpinepsIdError) with every reason; nothing is guessed.

CLI (spineps env: nibabel, numpy, scipy not needed)
    python tools/spineps_ids.py check <mask> [<mask> ...] [--no-require-ctd] [--strict]     exit 1 on any failure
    python tools/spineps_ids.py relabel --src-dir D --out-dir O [--shard i --n-shards n] [--cases a,b] [--force]
        -> O/<case>_seg-vert_msk.nii.gz (a NEW file; the source is never touched), with the semantic mask and ctd
           linked beside it (so body_masks.py and find_ctd work on O), O/<case>_relabel.json, O/relabel_shard<i>.jsonl.
           A source that already passes the guard is linked through unchanged (action "passthrough").
    python tools/spineps_ids.py summary --out-dir O           -> O/relabel_summary.json
    python tools/spineps_ids.py compare --a <mask> --b <mask>  per-instance world-centroid agreement of two masks
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

VERSE = {**{i: f"C{i}" for i in range(1, 8)}, **{7 + i: f"T{i}" for i in range(1, 13)},
         **{19 + i: f"L{i}" for i in range(1, 7)}, 26: "S", 27: "Co", 28: "T13"}
EXTRA_IDS = (80,)          # outside the VerSe alphabet, written by SPINEPS into otherwise VerSe-named masks (census:
                           # 590 masks, median 14 voxels); meaning not established, so it is set aside, never named
MIN_VOX = 50               # smaller instances are specks: kept out of the order test (the census's floor)
TOL_MM = 5.0               # a pair is inverted when the caudal centroid lies more than this above the cranial one
RAW_FRAC = 0.30            # >= 2 disagreements and >= 30 % of tested ctd points: the ids are not VERIDAH's names
PRESACRAL_ORDER = list(range(1, 20)) + [28] + list(range(20, 26))       # C1..T12, T13, L1..L6
OPTIONAL = {1, 25, 28}     # C1 is never in the ctd; T13 and L6 are variants, so skipping them is not a gap
ANAT = {lab: k for k, lab in enumerate(PRESACRAL_ORDER + [26, 27])}
# VERIDAH names shown wrong from outside VERIDAH; relabel refuses these by source case name (realpath, so the TS v3
# links to the same file are refused too). Add a case only with the evidence that refutes the name.
KNOWN_VERIDAH_ERRORS = {
    "TS_s1178": "SchwingNet/results/spineps_ids/TS12_VERIFY.md: the 12th ribs meet the vertebra VERIDAH calls L1 "
                "(TS_s1178_axial.png); its ctd skips T12, so its L1..L6 are T12, L1..L5 of a normal 24-presacral spine",
}


class SpinepsIdError(RuntimeError):
    """The mask's ids cannot be read as VerSe names. Never catch this to carry on naming by id."""


class RelabelRefused(SpinepsIdError):
    """relabel_by_ctd could not show a safe alignment; the reasons are in .report['refused']."""

    def __init__(self, msg: str, report: dict):
        super().__init__(msg)
        self.report = report


def name(i: int) -> str:
    return VERSE.get(int(i), str(i))


def verse_rank(i: int) -> float:
    return {28: 19.5, 25: 24.5}.get(int(i), float(i))


# ------------------------------------------------------------------------------------------------ inputs
def load_mask(mask):
    """(int32 array, affine, path-or-None) from a path, a nibabel image, or an (array, affine) pair."""
    import nibabel as nib
    if isinstance(mask, (str, os.PathLike)):
        img = nib.load(str(mask))
        arr, A, p = np.asanyarray(img.dataobj), img.affine, str(mask)
    elif isinstance(mask, tuple) and len(mask) == 2:
        arr, A, p = np.asarray(mask[0]), np.asarray(mask[1], float), None
    elif hasattr(mask, "affine") and hasattr(mask, "dataobj"):
        arr, A, p = np.asanyarray(mask.dataobj), mask.affine, getattr(mask, "get_filename", lambda: None)()
    else:
        raise TypeError(f"mask must be a path, a nibabel image or (array, affine), not {type(mask)}")
    if arr.dtype.kind == "f":
        arr = np.rint(arr)
    return arr.astype(np.int32, copy=False), np.asarray(A, float), p


def read_ctd(path) -> dict | None:
    """{label: world RAS mm (np.ndarray)} from a TPTBox POI json (header zoom/origin/rotation, points in voxels of
    that grid: world = rotation @ (xyz * zoom) + origin, the transform the census, fixids and relabel_from_poi use).
    None for a file with no world points (legacy VerSe centroid files carry no origin)."""
    J = json.load(open(path))
    if not (isinstance(J, list) and J and isinstance(J[0], dict) and "zoom" in J[0] and isinstance(J[-1], dict)):
        return None
    hdr = J[0]
    if hdr.get("direction") not in (None, ["R", "A", "S"]):
        # the rotation carries the orientation; a non-RAS direction is legal, but record it rather than assume
        pass
    fmt = str(hdr.get("format", "POI")).upper()
    zoom = np.asarray(hdr["zoom"], float)
    origin = np.asarray(hdr["origin"], float)
    rot = np.asarray(hdr["rotation"], float)
    out = {}
    for k, sub in J[-1].items():
        try:
            lab = int(k)
        except ValueError:
            continue
        if not isinstance(sub, dict) or not sub:
            continue
        c = np.asarray(sub.get("50") or sub.get(50) or next(iter(sub.values())), float)
        out[lab] = c if "GLOBAL" in fmt else rot @ (c * zoom) + origin
    return out


def find_ctd(mask_path) -> str | None:
    """The ctd beside a mask (<case>_ctd.json preferred, then any <case>_*ctd*.json, then *_poi*.json). For a body
    mask, the ctd of the instance mask it was cut from (<case>_body.json "instance")."""
    mask_path = str(mask_path)
    d, n = os.path.split(mask_path)
    if n.endswith("_body_msk.nii.gz"):
        case = n[: -len("_body_msk.nii.gz")]
        bj = os.path.join(d, f"{case}_body.json")
        if os.path.exists(bj):
            src = (json.load(open(bj)) or {}).get("instance")
            if src:
                return find_ctd(src)
        return None
    m = re.match(r"(.*?)_seg-vert", n)
    prefix = m.group(1) if m else n.split(".nii")[0]
    cands = sorted(glob.glob(os.path.join(d, glob.escape(prefix) + "_*ctd*.json")))
    if not cands:
        cands = sorted(glob.glob(os.path.join(d, glob.escape(prefix) + "_*poi*.json")))
    pref = [c for c in cands if c.endswith("_ctd.json")] + [c for c in cands if not c.endswith("_ctd.json")]
    if pref:
        return pref[0]
    # a link under another case name (a COLONOG_<n> link to CTSP_<id>, a TSV3 link into bench_ts): the ctd lies
    # beside the file the link resolves to
    real = os.path.realpath(mask_path)
    if real != os.path.abspath(mask_path):
        return find_ctd(real)
    return None


def instance_stats(arr: np.ndarray, A: np.ndarray) -> dict:
    """{id: (voxels, world RAS centroid)} for ids 1..99."""
    nz = np.nonzero((arr > 0) & (arr < 100))
    vals = arr[nz].astype(np.int64)
    if vals.size == 0:
        return {}
    mx = int(vals.max())
    cnt = np.bincount(vals, minlength=mx + 1)
    sums = [np.bincount(vals, weights=nz[k].astype(np.float64), minlength=mx + 1) for k in range(3)]
    out = {}
    for i in np.nonzero(cnt)[0]:
        i = int(i)
        if i == 0:
            continue
        ijk = np.array([sums[k][i] / cnt[i] for k in range(3)])
        out[i] = (int(cnt[i]), A[:3, :3] @ ijk + A[:3, 3])
    return out


def point_instance(arr: np.ndarray, Minv: np.ndarray, w, radius: int = 3):
    """(instance id or 0, how) at world point w: 'in' (the voxel holds a vertebra id), 'near' (majority vertebra id
    within `radius` voxels), 'empty', or 'outside' the grid."""
    ix = np.rint((Minv @ np.r_[np.asarray(w, float), 1.0])[:3]).astype(int)
    if (ix < 0).any() or (ix >= np.array(arr.shape)).any():
        return 0, "outside"
    v = int(arr[tuple(ix)])
    if 0 < v < 100:
        return v, "in"
    lo = np.clip(ix - radius, 0, None)
    hi = np.minimum(ix + radius + 1, arr.shape)
    win = arr[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    win = win[(win > 0) & (win < 100)]
    if win.size:
        u, c = np.unique(win, return_counts=True)
        return int(u[np.argmax(c)]), "near"
    return 0, "empty"


def _order_inversions(si: dict, rank) -> list:
    ids = sorted(si, key=rank)
    inv = []
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            i, j = ids[a], ids[b]
            if rank(i) != rank(j) and si[j] > si[i] + TOL_MM:
                inv.append((name(i), name(j), round(si[j] - si[i], 1)))
    return inv


# ------------------------------------------------------------------------------------------------ the guard
def check_ids(mask, ctd="auto", *, kind: str | None = None) -> dict:
    """Measure whether a mask's ids are VerSe names. Never raises on the verdict (see assert_verse_monotonic)."""
    arr, A, path = load_mask(mask)
    if kind is None:
        kind = "body" if (path and str(path).endswith("_body_msk.nii.gz")) else "seg-vert"
    rep = dict(path=path, kind=kind, reasons=[])
    st = instance_stats(arr, A)
    rep["ids"] = sorted(st)
    core = {i: v for i, v in st.items() if i not in EXTRA_IDS}
    rep["extra_ids"] = {str(i): st[i][0] for i in st if i in EXTRA_IDS}
    big = {i: v for i, v in core.items() if v[0] >= MIN_VOX}
    if not core:
        rep["verdict"] = "empty"
        return rep
    vox_ml = abs(float(np.linalg.det(A[:3, :3]))) / 1000.0
    rep["verse_coded"] = all(1 <= i <= 28 for i in big)
    rep["contiguous_from_1"] = sorted(core) == list(range(1, len(core) + 1))
    named = {i: v for i, v in big.items() if 1 <= i <= 28}
    si = {i: float(v[1][2]) for i, v in named.items()}
    inv = _order_inversions(si, verse_rank)
    rep["mono_verse"] = not inv
    rep["inverted_pairs"] = inv[:8]
    rep["n_inverted_pairs"] = len(inv)
    rep["order_top_to_bottom"] = [name(i) for i in sorted(si, key=lambda x: -si[x])]
    if len(big) >= 3:
        P = np.array([v[1] for v in big.values()], float)
        P = P - P.mean(0)
        _, _, vt = np.linalg.svd(P, full_matrices=False)
        rep["spine_axis_cos_S"] = round(float(abs(vt[0][2])), 3)
    else:
        rep["spine_axis_cos_S"] = None
    axis_ok = rep["spine_axis_cos_S"] is None or rep["spine_axis_cos_S"] >= 0.5
    # size against name, from outside the naming
    cerv = [v[0] * vox_ml for i, v in big.items() if 1 <= i <= 7]
    lumb = [v[0] * vox_ml for i, v in big.items() if 20 <= i <= 25]
    scale = 0.5 if kind == "body" else 1.0
    rep["median_ml_named_cervical"] = round(float(np.median(cerv)), 1) if cerv else None
    rep["median_ml_named_lumbar"] = round(float(np.median(lumb)), 1) if lumb else None
    size_bad = bool((len(cerv) >= 2 and np.median(cerv) > 40.0 * scale)
                    or (len(lumb) >= 2 and np.median(lumb) < 15.0 * scale)
                    or (len(cerv) >= 2 and len(lumb) >= 2 and np.median(cerv) > np.median(lumb)))
    rep["size_contradicts_names"] = size_bad

    # the ctd
    cpath = None
    pts = None
    if isinstance(ctd, dict):
        pts, cpath = ctd, "<given>"
    elif ctd == "auto":
        cpath = find_ctd(path) if path else None
    elif ctd:
        cpath = str(ctd)
    if pts is None and cpath and os.path.exists(cpath):
        pts = read_ctd(cpath)
    rep["ctd"] = cpath
    agree = disagree = near_agree = near_disagree = 0
    dis = []
    if pts:
        rep["ctd_labels"] = [name(l) for l in sorted(pts, key=lambda l: ANAT.get(l, 99))]
        csi = {l: float(w[2]) for l, w in pts.items() if 1 <= l <= 28}
        cinv = _order_inversions(csi, verse_rank)
        rep["ctd_mono"] = not cinv
        rep["ctd_inverted_pairs"] = cinv[:6]
        # a mandatory name skipped at a normal spacing (VERIDAH's T12 skip): reported here, raised by the assert
        try:
            skipped, _ = _ctd_gaps({l: np.asarray(w, float) for l, w in pts.items() if l in ANAT})
        except Exception:                              # noqa: BLE001  (a malformed ctd is judged by the order test)
            skipped = []
        rep["veridah_skipped_names"] = [g for g in skipped if "normal vertebral spacing" in g.get("why", "")]
        Minv = np.linalg.inv(A)
        for lab, w in pts.items():
            v, how = point_instance(arr, Minv, w, radius=2)
            if how == "in":
                if v in EXTRA_IDS:
                    continue
                if v == lab:
                    agree += 1
                else:
                    disagree += 1
                    dis.append(f"ctd {name(lab)} lands in id {v}")
            elif how == "near":
                if v == lab:
                    near_agree += 1
                else:
                    near_disagree += 1
    tested = agree + disagree
    frac = disagree / tested if tested else 0.0
    rep.update(ctd_agree=agree, ctd_disagree=disagree, ctd_near_agree=near_agree, ctd_near_disagree=near_disagree,
               ctd_tested=tested, ctd_disagree_frac=round(frac, 3), ctd_disagree_examples=dis[:10])
    has_test = tested >= 2

    if not rep["verse_coded"]:
        rep["verdict"] = "not_verse_ids"
        rep["reasons"].append(f"vertebra ids outside the VerSe alphabet: {[i for i in big if not 1 <= i <= 28]}")
    elif has_test and disagree >= 2 and frac >= RAW_FRAC:
        rep["verdict"] = "raw_or_scrambled"
        rep["reasons"].append(f"{disagree} of {tested} ctd points land in an instance of another id ({frac:.0%})"
                              + ("; ids are exactly 1..N (a raw instance enumeration)" if rep["contiguous_from_1"] else ""))
    elif axis_ok and not rep["mono_verse"]:
        if has_test and pts and not rep.get("ctd_mono", True):
            rep["verdict"] = "veridah_order_error"
            rep["reasons"].append(f"the ctd's own names are out of S order {rep['ctd_inverted_pairs'][:3]}, "
                                  "and the mask copies them")
        else:
            rep["verdict"] = "not_verse_order"
            rep["reasons"].append(f"read as VerSe names the ids are not cranio-caudal: {inv[:3]}")
    elif has_test and pts and not rep.get("ctd_mono", True):
        rep["verdict"] = "veridah_order_error"
        rep["reasons"].append(f"the ctd's own names are out of S order {rep['ctd_inverted_pairs'][:3]}")
    elif has_test and len(cerv) >= 2 and np.median(cerv) > 40.0 * scale:
        # the ids ARE VERIDAH's names, and VERIDAH named lumbar-sized bones cervical (carmlspine case134: C1..C5 at
        # 54-64 ml over an L2-S field). Only the cervical rule is used when a ctd exists: the lumbar floor would
        # refuse children (TS v3 paediatric lumbar vertebrae of 5-14 ml pass VerSe-named and ctd-concordant).
        rep["verdict"] = "veridah_size_contradiction"
        rep["reasons"].append(f"VERIDAH names vertebrae cervical whose median volume is {np.median(cerv):.1f} ml "
                              f"(> {40.0 * scale:.0f}); the names are VERIDAH's, and wrong")
    elif has_test and disagree == 0:
        rep["verdict"] = "verse_ok"
    elif has_test:
        rep["verdict"] = "misnamed_1_2_levels"
        rep["reasons"].append(f"{disagree} of {tested} ctd points in another id: {dis[:3]} (VERIDAH's own one-level "
                              "defect, not the id scheme)")
    else:
        if rep["contiguous_from_1"] and size_bad:
            rep["verdict"] = "raw_or_scrambled"
            rep["reasons"].append("no ctd test; ids are exactly 1..N and the sizes contradict the names "
                                  f"(cervical median {rep['median_ml_named_cervical']} ml, lumbar "
                                  f"{rep['median_ml_named_lumbar']} ml)")
        elif not axis_ok:
            rep["verdict"] = "untestable"
            rep["reasons"].append(f"no ctd test and the instance column is not along world S "
                                  f"(|cos| {rep['spine_axis_cos_S']})")
        else:
            rep["verdict"] = "verse_ok_no_ctd"
            rep["reasons"].append("no ctd test possible" + (f" (ctd {cpath})" if cpath else " (no ctd beside the mask)"))
    return rep


def assert_verse_monotonic(mask, ctd="auto", *, require_ctd: bool = True, strict: bool = False,
                           what: str = "", kind: str | None = None, quiet: bool = False,
                           allow_skipped_names: bool = False) -> dict:
    """Raise SpinepsIdError unless the mask's ids are VerSe names (see the module docstring); return the report.

    Allowed verdicts: verse_ok; misnamed_1_2_levels unless strict (a warning is printed); verse_ok_no_ctd only when
    require_ctd is False; empty (no names to be wrong).

    A ctd that SKIPS a mandatory name at a normal vertebral spacing (VERIDAH's T12 skip) also raises, unless
    allow_skipped_names: every time a reader could check one, the names on one side of the skip were one level off
    (all 53 CTSP benchmark cases against the release labels: T12 Dice 0 in 53, T11 < 0.2 in 50, lumbar names right;
    TS_s1178: the lumbar names were off; SchwingNet/results/spineps_ids/REPAIRS.md section 4). Pass
    allow_skipped_names=True only where another labeller gates every name (tools/dual_seg_compare.py)."""
    rep = check_ids(mask, ctd, kind=kind)
    v = rep["verdict"]
    label = what or rep.get("path") or "mask"
    if rep.get("veridah_skipped_names") and not allow_skipped_names and v in ("verse_ok", "misnamed_1_2_levels"):
        g = rep["veridah_skipped_names"][0]
        raise SpinepsIdError(
            f"{label}: SPINEPS ids cannot be read as VerSe names [veridah_skipped_name]: VERIDAH's ctd skips "
            f"{'/'.join(g['missing'])} between {g['above']} and {g['below']} at a normal spacing ({g['dz_mm']} mm, "
            f"local {g['local_spacing_mm']} mm), so the names on one side of the skip are one level off. Name this "
            "case from another labeller, or pass allow_skipped_names=True where another labeller gates every name.")
    ok = v in ("verse_ok", "empty") or (v == "misnamed_1_2_levels" and not strict) \
        or (v == "verse_ok_no_ctd" and not require_ctd)
    if not ok:
        if v == "verse_ok_no_ctd":
            why = "no ctd to show the ids are VERIDAH's names (a raw 1..N enumeration looks the same)"
        else:
            why = "; ".join(rep["reasons"]) or v
        fix = ("Name this case from another labeller: VERIDAH's own names are wrong here."
               if v.startswith("veridah_") else
               "Read the names from the ctd (tools/spineps_ids.py relabel), never from the id.")
        raise SpinepsIdError(f"{label}: SPINEPS ids cannot be read as VerSe names [{v}]: {why}. {fix}")
    if v == "misnamed_1_2_levels" and not quiet:
        print(f"WARNING {label}: {'; '.join(rep['reasons'])}", file=sys.stderr, flush=True)
    return rep


assert_verse_named = assert_verse_monotonic


def body_source_ok(body_path, **kw) -> dict:
    """The guard for a body mask: its ids are its source instance mask's ids, so test the body against the ctd of
    that source (find_ctd follows <case>_body.json)."""
    return assert_verse_monotonic(body_path, "auto", kind="body", **kw)


# ------------------------------------------------------------------------------------------------ the relabel
def _ctd_gaps(pts: dict) -> tuple[list, list]:
    """(refusals, accepted gaps) for mandatory names missing between two named presacral points."""
    pres = sorted((l for l in pts if l in PRESACRAL_ORDER), key=ANAT.get)
    z = {l: float(pts[l][2]) for l in pres}
    pairs = list(zip(pres, pres[1:]))
    dzs = [z[a] - z[b] for a, b in pairs]
    refuse, accept = [], []
    for k, (a, b) in enumerate(pairs):
        between = PRESACRAL_ORDER[ANAT[a] + 1: ANAT[b]]
        missing = [x for x in between if x not in OPTIONAL]
        if not missing:
            continue
        # local spacing from the neighbouring gap-free pairs (up to 3 each side)
        loc = []
        for j in list(range(max(0, k - 3), k)) + list(range(k + 1, min(len(pairs), k + 4))):
            aa, bb = pairs[j]
            if not [x for x in PRESACRAL_ORDER[ANAT[aa] + 1: ANAT[bb]] if x not in OPTIONAL] and dzs[j] > 0:
                loc.append(dzs[j])
        rec = dict(above=name(a), below=name(b), missing=[name(x) for x in missing], dz_mm=round(dzs[k], 1),
                   local_spacing_mm=round(float(np.median(loc)), 1) if loc else None)
        if not loc:
            rec["why"] = "no gap-free neighbour to measure the spacing"
            refuse.append(rec)
        elif dzs[k] < (1.0 + 0.5 * len(missing)) * float(np.median(loc)):
            rec["why"] = "a name skipped at a normal vertebral spacing (VERIDAH's naming, not a missing vertebra)"
            refuse.append(rec)
        else:
            rec["why"] = "gap wide enough for the missing vertebra(e): SPINEPS did not find them"
            accept.append(rec)
    return refuse, accept


def relabel_by_ctd(arr, A, pts: dict, semantic=None, *, tol_z: float = 25.0, tol_z_sac: float = 45.0,
                   tol_3d: float = 40.0, tol_3d_sac: float = 60.0, frag_frac: float = 0.15,
                   refuse_skipped_names: bool = False):
    """(relabelled int16 array, report) -- see the module docstring. Raises RelabelRefused."""
    arr = np.asarray(arr).astype(np.int32, copy=False)
    A = np.asarray(A, float)
    rep = dict(refused=[], notes=[])

    def refuse(msg):
        rep["refused"].append(msg)

    pts = dict(pts or {})
    ignored = sorted(l for l in pts if l not in ANAT)
    bad = [l for l in ignored if l < 100]              # 100+ are disc / end-plate points: not vertebra names
    pts = {l: np.asarray(w, float) for l, w in pts.items() if l in ANAT}
    if ignored:
        rep["ctd_labels_ignored"] = ignored
    if bad:
        refuse(f"ctd labels outside the VerSe alphabet: {bad}")
    if len(pts) < 2:
        refuse(f"ctd has {len(pts)} usable points")
        raise RelabelRefused("; ".join(rep["refused"]), rep)
    pres = sorted((l for l in pts if l in PRESACRAL_ORDER), key=ANAT.get)
    z = {l: float(w[2]) for l, w in pts.items()}
    for a_, b_ in zip(pres, pres[1:]):
        if z[b_] - z[a_] > TOL_MM:
            refuse(f"ctd names out of S order: {name(b_)} lies {z[b_] - z[a_]:.1f} mm above {name(a_)}")
    if 26 in pts and pres and z[26] > min(z[l] for l in pres) + TOL_MM:
        refuse(f"ctd sacrum point lies {z[26] - min(z[l] for l in pres):.1f} mm above the lowest named vertebra")
    gref, gacc = _ctd_gaps(pts)
    rep["ctd_gaps_accepted"] = gacc
    rep["veridah_skipped_names"] = gref
    for g in gref:
        msg = (f"ctd skips {'/'.join(g['missing'])} between {g['above']} and {g['below']} ({g['dz_mm']} mm apart, "
               f"local spacing {g['local_spacing_mm']} mm): {g['why']}")
        if refuse_skipped_names:
            refuse(msg)
        else:
            rep["notes"].append(msg + " -- reproduced as VERIDAH wrote it (its encoding of an 11-thoracic spine); "
                                "the count it implies is VERIDAH's call, wrong on TS_s1178")
    if rep["refused"]:
        raise RelabelRefused("; ".join(rep["refused"]), rep)

    st = instance_stats(arr, A)
    objs = {i: v for i, v in st.items() if v[0] >= MIN_VOX}
    specks = sorted(i for i, v in st.items() if v[0] < MIN_VOX)
    Minv = np.linalg.inv(A)
    vox_ml = abs(float(np.linalg.det(A[:3, :3]))) / 1000.0

    # the semantic mask decides the sacrum. A RAW SPINEPS semantic mask has no class 26 and the raw instance mask
    # holds no sacrum: in the raw bench_ts masks the ctd S point lies inside an instance in 10 of 853, and that
    # instance is an 8-40 ml S1-level piece (census rows); TS12_VERIFY found fixids' 26 on 380-684-voxel fragments
    # (s0790, s1124, s1350) and on S1-sized pieces 24-29 mm above the point (s0224, s1304, s1380). A 26 written
    # from such an object would be a sacrum box on the wrong bone, so without semantic sacrum no 26 is written.
    sem = None
    if semantic is not None:
        sarr, sA = semantic
        if tuple(sarr.shape) == tuple(arr.shape) and np.allclose(sA, A, atol=1e-3):
            sem = np.asarray(sarr)
            rep["semantic_labels"] = sorted(int(x) for x in np.unique(sem) if x)
        else:
            rep["notes"].append(f"semantic mask not on the instance grid ({tuple(sarr.shape)} vs {tuple(arr.shape)}): "
                                "no sacrum can be named")
    sem_sac = (sem == 26) if (sem is not None and 26 in rep.get("semantic_labels", [])) else None

    # b. POSITION
    bind, how_of = {}, {}
    for lab, w in pts.items():
        v, how = point_instance(arr, Minv, w, radius=3)
        how_of[lab] = how
        if v and v in objs:
            bind[lab] = v
    sacrum_pieces = {}
    for lab in (26, 27):
        if lab in bind:
            i = bind[lab]
            frac_sac = float(sem_sac[arr == i].mean()) if sem_sac is not None else 0.0
            if frac_sac < 0.5:
                del bind[lab]
                sacrum_pieces[i] = (f"holds the ctd {name(lab)} point but is {frac_sac:.0%} semantic sacrum "
                                    f"({objs[i][0] * vox_ml:.1f} ml): an S1-level piece, not the {name(lab)}")
    by_inst = {}
    for lab, v in bind.items():
        by_inst.setdefault(v, []).append(lab)
    for v, labs in by_inst.items():
        if len(labs) > 1:
            pres_l = [l for l in labs if l in PRESACRAL_ORDER]
            if len(pres_l) == 1:                      # a vertebra and the sacrum/coccyx point: the vertebra keeps it
                for l in labs:
                    if l not in PRESACRAL_ORDER:
                        del bind[l]
                        rep["notes"].append(f"{name(l)} point lies in the instance of {name(pres_l[0])}: unbound")
            else:
                refuse(f"instance {v} holds the points of {'+'.join(name(l) for l in sorted(labs, key=ANAT.get))}")
    for lab, v in list(bind.items()):
        c = objs[v][1]
        dz = abs(float(c[2]) - z[lab])
        d3 = float(np.linalg.norm(c - pts[lab]))
        sac = lab in (26, 27)
        if dz > (tol_z_sac if sac else tol_z) or d3 > (tol_3d_sac if sac else tol_3d):
            msg = f"{name(lab)} point lies in instance {v} whose centroid is {dz:.1f} mm away in S, {d3:.1f} mm in 3-D"
            if sac:                                   # the sacrum point is not a centroid: unbind, never refuse on it
                del bind[lab]
                rep["notes"].append(msg + ": sacrum left to the below-the-column rule")
            else:
                refuse(msg)
    bound_pres = [l for l in pres if l in bind]
    unbound_pres = [l for l in pres if l not in bind]
    if not bound_pres:
        refuse("no presacral ctd point lands in an instance")
        raise RelabelRefused("; ".join(rep["refused"]), rep)
    k_top, k_bot = pres.index(bound_pres[0]), pres.index(bound_pres[-1])
    inner_unbound = [l for l in unbound_pres if k_top < pres.index(l) < k_bot]
    if inner_unbound:
        refuse(f"named levels with no instance inside the column: {[name(l) for l in inner_unbound]}")
    rep["unbound_end_labels"] = [name(l) for l in unbound_pres if l not in inner_unbound]
    if rep["refused"]:
        raise RelabelRefused("; ".join(rep["refused"]), rep)

    # c. RANK cross-check (fixids)
    s_top = max(float(objs[bind[l]][1][2]) for l in bound_pres)
    s_bot = min(float(objs[bind[l]][1][2]) for l in bound_pres)
    med_n = float(np.median([objs[bind[l]][0] for l in bound_pres]))
    bound_insts = set(bind.values())
    col, frags_inside, above, below = [], [], [], []
    for i, (n, c) in objs.items():
        s = float(c[2])
        if i in bound_insts and i in [bind[l] for l in bound_pres]:
            col.append(i)
            continue
        if i in bound_insts:              # bound to the sacrum / coccyx point
            continue
        if i in sacrum_pieces:            # held the S point, but no semantic sacrum: left unnamed (dropped below)
            continue
        if s > s_top + 1.0:
            above.append(i)
        elif s < s_bot - 1.0:
            below.append(i)
        elif n < frag_frac * med_n:
            frags_inside.append(i)
        else:
            refuse(f"unnamed vertebra-sized instance {i} ({n} voxels, median named {med_n:.0f}) inside the named "
                   f"column at S {s:.1f}")
    if rep["refused"]:
        raise RelabelRefused("; ".join(rep["refused"]), rep)
    col_sorted = sorted(col, key=lambda i: -float(objs[i][1][2]))
    rank_pairs = list(zip(col_sorted, bound_pres))
    mism = [(i, name(l), name(next(k for k, v in bind.items() if v == i))) for i, l in rank_pairs if bind[l] != i]
    if len(col_sorted) != len(bound_pres) or mism:
        refuse(f"z-rank and position disagree: {mism[:4]} (instances {len(col_sorted)}, named {len(bound_pres)})")
        raise RelabelRefused("; ".join(rep["refused"]), rep)
    dzs = [abs(float(objs[bind[l]][1][2]) - z[l]) for l in bound_pres]

    # d. above / below the column
    mapping = {bind[l]: l for l in bind}
    dropped = {i: "speck (< 50 voxels)" for i in specks}
    dropped.update(sacrum_pieces)
    for i in frags_inside:
        dropped[i] = f"fragment inside the column ({objs[i][0]} voxels)"
    if above:
        big_above = [i for i in above if objs[i][0] >= frag_frac * med_n]
        if bound_pres[0] == 2 and len(big_above) == 1 and 2 in pts and float(objs[big_above[0]][1][2]) > z[2] + 8.0:
            mapping[big_above[0]] = 1
            rep["notes"].append(f"instance {big_above[0]} above the C2 point named C1 (the ctd never names C1)")
            above = [i for i in above if i != big_above[0]]
        for i in above:
            dropped[i] = f"unnamed, above the named column ({objs[i][0]} voxels)"
    for i in below:
        if sem_sac is not None:
            frac_sac = float(sem_sac[arr == i].mean())
            if frac_sac >= 0.5:
                mapping[i] = 26
                rep["notes"].append(f"instance {i} below the column is {frac_sac:.0%} semantic sacrum: 26")
                continue
            dropped[i] = f"unnamed, below the column, {frac_sac:.0%} semantic sacrum ({objs[i][0]} voxels)"
        else:
            near = (f", {abs(float(objs[i][1][2]) - z[26]):.0f} mm from the ctd S point in S" if 26 in pts else "")
            dropped[i] = (f"unnamed, below the column ({objs[i][0] * vox_ml:.1f} ml{near}); no semantic sacrum, "
                          "so not named sacrum")
    for i in st:
        if i not in mapping and i not in dropped:
            dropped[i] = "unnamed"

    lut = np.zeros(max(int(arr.max()), 1) + 1, np.int16)
    for old, new in mapping.items():
        lut[old] = new
    arr_c = np.where((arr > 0) & (arr < lut.size), arr, 0)
    out = lut[arr_c]
    if sem_sac is not None:
        add = sem_sac & (out == 0) & ((arr == 0) | np.isin(arr, list(dropped) or [-1]))
        out[add] = 26
        rep["sacrum_semantic_voxels_added"] = int(add.sum())
    rep["mapping"] = {str(k): name(v) for k, v in sorted(mapping.items(), key=lambda kv: ANAT.get(kv[1], 99))}
    rep["dropped"] = {str(k): v for k, v in dropped.items()}
    rep["point_binding"] = {name(l): how_of[l] for l in sorted(pts, key=lambda l: ANAT.get(l, 99))}
    rep["max_dz_mm"] = round(max(dzs), 1)
    rep["median_dz_mm"] = round(float(np.median(dzs)), 1)
    labels = sorted(set(mapping.values()) | ({26} if rep.get("sacrum_semantic_voxels_added") else set()), key=ANAT.get)
    rep["labels"] = [name(l) for l in labels]
    if 26 in labels:
        rep["sacrum"] = "named 26 from the semantic sacrum"
    elif 26 in pts:
        rep["sacrum"] = ("absent: the ctd names a sacrum but the source has no semantic sacrum (a raw SPINEPS mask "
                         "carries none); take the sacrum from another labeller, never from this mask")
    else:
        rep["sacrum"] = "not in the ctd"
    rep["ctd_call"] = "L6" if 25 in pts and 28 not in pts else ("T13" if 28 in pts and 25 not in pts else
                                                                ("both" if 25 in pts else "none"))
    rep["ctd_call_is"] = "VERIDAH pseudo-truth, not a reader's (CONSUMERS.md section 4: CTSP PPV of an L6 call 10/24)"

    # e. the result must pass the guard with zero disagreements
    chk = check_ids((out, A), {l: pts[l] for l in bind})   # an unbound sacrum point is not a name the mask carries
    rep["post_check"] = {k: chk.get(k) for k in ("verdict", "ctd_agree", "ctd_disagree", "mono_verse", "reasons")}
    if chk.get("ctd_tested", 0) < 2:
        refuse(f"only {chk.get('ctd_tested', 0)} ctd point(s) bind to an instance: nothing to cross-check the "
               "name against (no rank, no order)")
        raise RelabelRefused("; ".join(rep["refused"]), rep)
    if chk["verdict"] != "verse_ok" or chk["ctd_disagree"]:
        refuse(f"relabelled mask fails the guard: {chk['verdict']} {chk['reasons']}")
        raise RelabelRefused("; ".join(rep["refused"]), rep)
    return out.astype(np.int16), rep


# ------------------------------------------------------------------------------------------------ CLI
def _cases(src: Path, only: str):
    got = sorted(p.name[: -len("_seg-vert_msk.nii.gz")] for p in src.glob("*_seg-vert_msk.nii.gz"))
    if only:
        keep = set(only.split(","))
        got = [c for c in got if c in keep]
    return got


def _link(src: str, dst: Path):
    if dst.is_symlink() or dst.exists():
        dst.unlink()
    os.symlink(os.path.realpath(src), dst)


def cmd_relabel(a) -> int:
    import nibabel as nib
    src, out = Path(os.path.expanduser(a.src_dir)), Path(os.path.expanduser(a.out_dir))
    if src.resolve() == out.resolve():
        raise SystemExit("--out-dir must differ from --src-dir: the source tree is never overwritten")
    out.mkdir(parents=True, exist_ok=True)
    cases = _cases(src, a.cases)
    mine = [c for k, c in enumerate(cases) if k % a.n_shards == a.shard]
    print(f"relabel shard {a.shard}/{a.n_shards}: {len(mine)} of {len(cases)} cases {src} -> {out}", flush=True)
    log = open(out / f"relabel_shard{a.shard}.jsonl", "a")
    tally = {}
    for c in mine:
        vp = src / f"{c}_seg-vert_msk.nii.gz"
        dst = out / f"{c}_seg-vert_msk.nii.gz"
        rj = out / f"{c}_relabel.json"
        if rj.exists() and not a.force:
            tally["skipped_done"] = tally.get("skipped_done", 0) + 1
            continue
        rec = dict(case=c, source=str(vp), source_realpath=os.path.realpath(vp), source_is_link=vp.is_symlink())
        try:
            cp = find_ctd(str(vp))
            rec["ctd"] = cp
            sp = src / f"{c}_seg-spine_msk.nii.gz"
            img = nib.load(str(vp))
            arr = np.asanyarray(img.dataobj).astype(np.int32)
            pts = read_ctd(cp) if cp else None
            pre = check_ids((arr, img.affine), pts if pts else None)
            rec["source_verdict"] = pre["verdict"]
            rec["source_reasons"] = pre["reasons"]
            rec["source_ids"] = pre["ids"]
            rec["source_ctd_agree_disagree"] = [pre.get("ctd_agree"), pre.get("ctd_disagree")]   # absent when empty
            known = KNOWN_VERIDAH_ERRORS.get(os.path.basename(os.path.realpath(vp))[: -len("_seg-vert_msk.nii.gz")])
            if known:
                rec["action"] = "refused"
                rec["refused"] = [f"known VERIDAH naming error: {known}"]
            elif pre["verdict"] in ("verse_ok", "misnamed_1_2_levels"):
                _link(str(vp), dst)
                rec["action"] = "passthrough"
                if pre["verdict"] == "misnamed_1_2_levels":
                    rec["note"] = "VerSe-named source with a one-level VERIDAH defect; linked unchanged"
            elif pre["verdict"] == "empty":
                rec["action"] = "refused"
                rec["refused"] = ["empty mask"]
            elif not pts:
                rec["action"] = "refused"
                rec["refused"] = [f"no usable ctd ({cp}); ids cannot be named"]
            else:
                semantic = None
                if sp.exists():
                    simg = nib.load(str(sp))
                    semantic = (np.asanyarray(simg.dataobj).astype(np.int32), simg.affine)
                try:
                    new, r = relabel_by_ctd(arr, img.affine, pts, semantic,
                                            refuse_skipped_names=a.refuse_skipped_names)
                    hdr = img.header.copy()
                    hdr.set_data_dtype(np.int16)
                    tmp = out / f".{c}_seg-vert_msk.tmp.nii.gz"
                    nib.save(nib.Nifti1Image(new, img.affine, hdr), str(tmp))          # same grid, never reoriented
                    os.replace(tmp, dst)
                    rec.update(r)
                    rec["action"] = "relabelled"
                except RelabelRefused as e:
                    rec.update(e.report)
                    rec["action"] = "refused"
            if rec["action"] in ("passthrough", "relabelled"):
                if sp.exists():
                    _link(str(sp), out / f"{c}_seg-spine_msk.nii.gz")
                if cp:
                    _link(cp, out / os.path.basename(cp))
            elif dst.exists() or dst.is_symlink():
                dst.unlink()                        # a refused case leaves no mask behind to be read by id
        except Exception as e:                      # noqa: BLE001
            rec["action"] = "error"
            rec["error"] = repr(e)[:400]
        tally[rec["action"]] = tally.get(rec["action"], 0) + 1
        json.dump(rec, open(rj, "w"), indent=1, default=str)
        log.write(json.dumps(rec, default=str) + "\n")
        log.flush()
        print(f"{c}: {rec['action']} (source {rec.get('source_verdict')})"
              + (f" refused: {rec.get('refused')}" if rec["action"] == "refused" else "")
              + (f" labels {rec.get('labels')}" if rec["action"] == "relabelled" else ""), flush=True)
    print(f"SPINEPS_IDS_RELABEL_SHARD_DONE {a.shard} {json.dumps(tally)}", flush=True)
    return 0


def cmd_summary(a) -> int:
    out = Path(os.path.expanduser(a.out_dir))
    recs = {}
    for f in sorted(out.glob("*_relabel.json")):       # one per case, rewritten by a --force re-run: authoritative
        try:
            r = json.load(open(f))
        except Exception:                              # noqa: BLE001
            continue
        recs[r["case"]] = r
    act = Counter(r["action"] for r in recs.values())
    src = Counter((r.get("source_verdict"), r["action"]) for r in recs.values())
    reasons = Counter()
    for r in recs.values():
        if r["action"] == "refused":
            for m in r.get("refused") or []:
                reasons[re.sub(r"[-\d.]+", "#", m)[:120]] += 1
    calls = Counter(r.get("ctd_call") for r in recs.values() if r["action"] == "relabelled")
    dz = [r["max_dz_mm"] for r in recs.values() if r["action"] == "relabelled" and "max_dz_mm" in r]
    S = dict(out_dir=str(out), cases=len(recs), actions=dict(act),
             source_verdict_x_action={f"{k[0]} -> {k[1]}": v for k, v in sorted(src.items(), key=str)},
             refusal_reasons=dict(reasons.most_common()),
             relabelled_ctd_call=dict(calls),
             relabelled_max_dz_mm=dict(median=float(np.median(dz)), p95=float(np.percentile(dz, 95)),
                                       max=float(max(dz))) if dz else None,
             sacrum_semantic_used=sum(1 for r in recs.values() if r.get("sacrum_semantic_voxels_added")),
             sacrum_state=dict(Counter(str(r.get("sacrum", "")).split(":")[0] for r in recs.values()
                                       if r["action"] == "relabelled")),
             c1_added=sum(1 for r in recs.values() if any("named C1" in n for n in r.get("notes") or [])),
             ctd_gaps_accepted=sum(1 for r in recs.values() if r.get("ctd_gaps_accepted")),
             veridah_skipped_names_relabelled=sorted(c for c, r in recs.items()
                                                     if r["action"] == "relabelled" and r.get("veridah_skipped_names")),
             refused_cases={c: r.get("refused") for c, r in sorted(recs.items()) if r["action"] == "refused"},
             error_cases={c: r.get("error") for c, r in sorted(recs.items()) if r["action"] == "error"})
    json.dump(S, open(out / "relabel_summary.json", "w"), indent=1, default=str)
    print(json.dumps({k: S[k] for k in ("cases", "actions", "refusal_reasons", "relabelled_ctd_call",
                                         "relabelled_max_dz_mm", "sacrum_semantic_used", "sacrum_state",
                                         "c1_added")}, indent=1,
                     default=str))
    return 0


def instance_inner_points(arr: np.ndarray, A: np.ndarray) -> dict:
    """{id: (voxels, world RAS of the instance's own voxel nearest its centroid)}. The centroid itself can lie
    outside the instance: C1 is a ring, and its centroid sits in the dens of C2."""
    nz = np.nonzero((arr > 0) & (arr < 100))
    if nz[0].size == 0:
        return {}
    vals = arr[nz].astype(np.int64)
    order = np.argsort(vals, kind="stable")
    idx = np.stack(nz, 1)[order]
    vals = vals[order]
    ids, starts, counts = np.unique(vals, return_index=True, return_counts=True)
    out = {}
    for i, s0, n in zip(ids, starts, counts):
        P = idx[s0: s0 + n].astype(np.float64)
        c = P.mean(0)
        p = P[int(np.argmin(((P - c) ** 2).sum(1)))]
        out[int(i)] = (int(n), A[:3, :3] @ p + A[:3, 3])
    return out


def compare_masks(pa, pb) -> dict:
    """For every instance of mask A (>= 50 voxels), the id mask B holds at A's inner point (A's own voxel nearest
    its centroid, in world space): same id or not. The masks may sit on different grids (SPINEPS's crop grid vs the
    CT grid)."""
    a_arr, a_A, _ = load_mask(pa)
    b_arr, b_A, _ = load_mask(pb)
    sa = instance_inner_points(a_arr, a_A)
    Minv = np.linalg.inv(b_A)
    same = diff = miss = 0
    ex = []
    for i, (n, c) in sa.items():
        if n < MIN_VOX:
            continue
        v, how = point_instance(b_arr, Minv, c, radius=3)
        if not v:
            miss += 1
        elif v == i:
            same += 1
        else:
            diff += 1
            ex.append(f"A {name(i)} -> B {name(v)}")
    return dict(same=same, diff=diff, miss=miss, examples=ex[:8])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("masks", nargs="+")
    c.add_argument("--no-require-ctd", action="store_true")
    c.add_argument("--strict", action="store_true")
    r = sub.add_parser("relabel")
    r.add_argument("--src-dir", required=True)
    r.add_argument("--out-dir", required=True)
    r.add_argument("--shard", type=int, default=int(os.environ.get("SLURM_ARRAY_TASK_ID", 0)))
    r.add_argument("--n-shards", type=int, default=1)
    r.add_argument("--cases", default="")
    r.add_argument("--force", action="store_true")
    r.add_argument("--refuse-skipped-names", action="store_true",
                   help="refuse a ctd that skips a mandatory name at a normal spacing (default: reproduce and flag)")
    s = sub.add_parser("summary")
    s.add_argument("--out-dir", required=True)
    m = sub.add_parser("compare")
    m.add_argument("--a", required=True)
    m.add_argument("--b", required=True)
    a = ap.parse_args()
    if a.cmd == "check":
        bad = 0
        for p in a.masks:
            try:
                rep = assert_verse_monotonic(p, require_ctd=not a.no_require_ctd, strict=a.strict)
                print(f"OK   {p}: {rep['verdict']}")
            except SpinepsIdError as e:
                bad += 1
                print(f"FAIL {e}")
        return 1 if bad else 0
    if a.cmd == "relabel":
        return cmd_relabel(a)
    if a.cmd == "summary":
        return cmd_summary(a)
    if a.cmd == "compare":
        print(json.dumps(compare_masks(a.a, a.b), indent=1))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
