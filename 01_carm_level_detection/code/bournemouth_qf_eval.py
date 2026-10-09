#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/bournemouth_qf_eval.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Bournemouth cervical quantitative fluoroscopy (BORDaR 385, Cervical_Database.mat; Branney et al., J Funct Morphol
Kinesiol 2024;9:55) as a cine evaluation set for tools/cine_eval.py (docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md section
2; the operating notes are docs/BOURNEMOUTH_QF_HARNESS.md).

WHAT THE FILE HOLDS (checked 2026-09-26 against the .mat, md5 aec3d16d031f62c4a4b7725cd5e0a0be): 126 imaging events
(ImageEvent HV01a ... P##b: 63 people, each with an event a and b) x {flexion, extension} = 252 sequences of 181-339
frames. Templates[i, j] is a 9 x 4 object array, rows C0 ... C7, T1, each cell an (n_frames, 2) array of (x, y) pixels,
y down. The four points are ANATOMICAL, not image-based: 0/1/2/3 = anterior-superior, anterior-inferior,
posterior-inferior, posterior-superior (on all 226 L sequences points 0/1 lie left of 2/3; on 25 of the 26 R sequences
right). A missing level is an EMPTY cell whose shape is (0, 0) uint8 or (1, 0) float64, so the test is c.size == 0; a
frame the authors' tracker failed on is a NaN row (all four points of one level; 472 of 467,369 level-frames). Only
C3-C6 (and C7 when the shoulder does not hide it) are four-corner body templates: C0 is the McGregor line plus two
arbitrary points, C1 marks the marrow cavities, C2's points 2 and 3 are its caudal corners and 1 and 4 arbitrary, T1
and an obscured C7 carry estimated caudal corners. Hence the roles written into every truth meta:

    C3-C6  score        full box and corners (the primary number)
    C7     score        reported separately (--level-group c7=C7): it may be an estimate under the shoulder
    C2     caudal_only  anatomical points 1 and 2 -> geometric slots 2 and 3; its box is never scored
    C0 C1 T1  ignore    a detection there is neither a true nor a false positive

WHAT IS NOT KNOWN (the data request asks; nothing here guesses a value from the data): whether template row 1 is
cine frame 1 (87 of 252 sequences have 1-59 more MachineAngle rows than template rows), the coordinate origin
(--coord-origin matlab1, the default, subtracts 1 from x and y), the pixel spacing (px_mm null; corner errors in px
and relative to the endplate), the polarity and facing of the DICOM, and the images themselves.

WHAT THE TRUTH IS: the output of the authors' semi-automatic template tracker. A score against it is agreement with
a validated tracker, not accuracy against independent hand labels.

    python tools/bournemouth_qf_eval.py export --mat <Cervical_Database.mat> --out /rs/.../realxray/bournemouth_qf
    python tools/bournemouth_qf_eval.py frames --dicom <dir> --root /rs/.../realxray/bournemouth_qf [--polarity auto]
    python tools/bournemouth_qf_eval.py frames --dicom <dir> --root ... --face L        # the 26 R sequences, mirrored
    python tools/bournemouth_qf_eval.py align --pred <prototype out root> --root ...    # diagnostic only
    python tools/bournemouth_qf_eval.py self-test [--mat M] [--out D] [--tier 1,2]
    python tools/bournemouth_qf_eval.py self-test --tier 3 --csxa-png P --csxa-json J --out D   # grid smoke frames
"""
from __future__ import annotations

import argparse
import collections
import csv
import glob
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cine_eval as CE  # noqa: E402

LEVELS = ("C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "T1")
ROLE = {"C0": "ignore", "C1": "ignore", "C2": "caudal_only", "C3": "score", "C4": "score", "C5": "score",
        "C6": "score", "C7": "score", "T1": "ignore"}
MOTIONS = ("flex", "ext")                        # Templates / MachineAngle / orientation column 0 = flexion, 1 = extension
MAT_MD5 = "aec3d16d031f62c4a4b7725cd5e0a0be"
ROOT = "/rs/rs_grp_oschome/go2432/data/realxray/bournemouth_qf"
LOCAL_MAT = r"laptop:data\bournemouth_qf\raw\Cervical_Database.mat"
EVENT_RE = re.compile(r"^((?:HV|P)\d{2})([ab])$")
SIZE = 1024                                      # the template coordinates run 57-955 x 68-957: a 1024 x 1024 frame
BUILDER = "tools/bournemouth_qf_eval.py/1"
# the counts checked against the .mat on 2026-09-26 (plan section 0); the self-test fails if a load disagrees
VERIFIED = dict(sequences=252, events=126, people=63, orientation={"L": 226, "R": 26}, ma_longer=87,
                levels={"C0": 48, "C1": 249, "C2": 252, "C3": 251, "C4": 252, "C5": 251, "C6": 247, "C7": 50, "T1": 7})
OR_PCT = (1.0, 5.0, 50.0, 95.0, 99.0)            # the realxray display ladder (docs/REAL_XRAY_DATASETS_SPEC.md,
OR_T = (27.0, 47.0, 126.0, 216.0, 239.0)         # deepfluoro_anchor.window_or), here over a whole SEQUENCE


@dataclass
class Sequence:
    event: str                   # HV01a
    person: str                  # HV01: the patient key (tools/patient_keys.py bournemouth rule)
    visit: str                   # a | b
    motion: str                  # flex | ext
    orientation: str             # the file's own L / R
    sex: str
    age: int | None
    group: str                   # PatientOrControl: C | P
    machine_angle: np.ndarray    # (n_ma,) degrees
    n_frames: int                # template rows
    levels: dict = field(default_factory=dict)     # name -> (n_frames, 4, 2), anatomical point order, NaN rows kept

    @property
    def seq(self):
        return f"{self.event}_{self.motion}"

    @property
    def facing(self):
        """The side the anterior wall is on, from the anatomical corners of C3-C6 (points 0/1 anterior)."""
        d = []
        for n in ("C3", "C4", "C5", "C6"):
            a = self.levels.get(n)
            if a is not None:
                d.append(np.nanmean(a[:, [0, 1], 0]) - np.nanmean(a[:, [2, 3], 0]))
        d = [x for x in d if np.isfinite(x)]
        return None if not d else ("L" if np.median(d) < 0 else "R")


def _s(x):
    a = np.asarray(x).ravel()
    return str(a[0]) if a.size else ""


def md5_of(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def load(mat, coord_origin="matlab1"):
    """Every sequence of the .mat. scipy.io.loadmat with squeeze_me=False, struct_as_record=False: squeezing would
    turn a one-frame level into a (2,) array and an empty cell into a 0-d one, and the shapes are what say what is
    missing."""
    import scipy.io as sio
    if coord_origin not in ("matlab1", "zero"):
        raise SystemExit(f"--coord-origin {coord_origin!r}: matlab1 or zero")
    m = sio.loadmat(str(mat), squeeze_me=False, struct_as_record=False)
    D = m["Database"][0, 0]
    off = 1.0 if coord_origin == "matlab1" else 0.0
    out = []
    for i in range(D.Templates.shape[0]):
        event = _s(D.ImageEvent[i, 0])
        me = EVENT_RE.match(event)
        if not me:
            raise ValueError(f"ImageEvent {event!r} is not HV##a/b or P##a/b")
        age = np.asarray(D.Age[i, 0]).ravel()
        for j, motion in enumerate(MOTIONS):
            T = D.Templates[i, j]
            if T.shape != (len(LEVELS), 4):
                raise ValueError(f"{event} {motion}: Templates cell is {T.shape}, expected {(len(LEVELS), 4)}")
            levels = {}
            for r, name in enumerate(LEVELS):
                cells = [np.asarray(T[r, c]) for c in range(4)]
                sz = [c.size for c in cells]
                if not any(sz):
                    continue                              # (0, 0) uint8 or (1, 0) float64: the level is absent
                if not all(sz):
                    raise ValueError(f"{event} {motion} {name}: some of the four points are empty and some not")
                arr = np.stack([c.astype(np.float64).reshape(-1, 2) for c in cells], 1) - off    # (n, 4, 2)
                levels[name] = arr
            ns = {a.shape[0] for a in levels.values()}
            if len(ns) > 1:
                raise ValueError(f"{event} {motion}: levels disagree on the frame count {sorted(ns)}")
            out.append(Sequence(event=event, person=me.group(1), visit=me.group(2), motion=motion,
                                orientation=_s(D.orientation[i, j]), sex=_s(D.Sex[i, 0]),
                                age=int(age[0]) if age.size else None, group=_s(D.PatientOrControl[i, 0]),
                                machine_angle=np.asarray(D.MachineAngle[i, j], float).ravel(),
                                n_frames=ns.pop() if ns else 0, levels=levels))
    return out


def _box(q):
    return [round(float(q[:, 0].min()), 3), round(float(q[:, 1].min()), 3),
            round(float(q[:, 0].max()), 3), round(float(q[:, 1].max()), 3)]


def seq_metas(s, offset=0, status="unverified", coord_origin="matlab1"):
    """One cine-schema truth meta per template row of sequence s. Template row k is cine frame k + offset. A NaN row
    (the authors' tracker failed on that level in that frame) is missing truth there: the level becomes an IGNORE
    region placed at its nearest tracked row, so a detection on it is neither rewarded nor charged."""
    fin = {n: np.flatnonzero(np.isfinite(a).all(axis=(1, 2))) for n, a in s.levels.items()}
    facing = s.facing
    out = []
    for k in range(s.n_frames):
        boxes = []
        for name in LEVELS:
            a = s.levels.get(name)
            if a is None:
                continue
            q = a[k]
            if np.isfinite(q).all():
                boxes.append(dict(gt_id=name, cls=0, level=name, box=_box(q),
                                  corners=[[round(float(x), 3), round(float(y), 3)] for x, y in q], role=ROLE[name]))
            elif len(fin[name]):
                kk = int(fin[name][np.argmin(np.abs(fin[name] - k))])
                boxes.append(dict(gt_id=name, cls=0, level=name, box=_box(a[kk]), corners=None, role="ignore",
                                  missing="nan_template_row", box_from_row=kk))
        f = k + offset
        ma = float(s.machine_angle[f]) if 0 <= f < len(s.machine_angle) else None
        out.append(dict(dataset="bournemouth_qf", case=s.event, stem=f"{s.seq}_f{f:04d}", seq=s.seq, frame=f,
                        split="test", template_row=k, view="LAT", px_mm=None, corner_order="anatomical",
                        coord_origin=("matlab1: x - 1, y - 1" if coord_origin == "matlab1" else "as stored"),
                        boxes=boxes,
                        extras=dict(machine_angle_deg=ma, orientation=s.orientation, facing=facing, motion=s.motion,
                                    event=s.event, person=s.person, offset=offset, offset_status=status)))
    return out


def load_offsets(path):
    """{seq: offset} from the authors' answer (JSON). Without one every offset is 0, `unverified`."""
    if not path:
        return {}, "unverified"
    d = json.load(open(os.path.expanduser(path), encoding="utf-8"))
    return {k: int(v) for k, v in d.items()}, "authors"


# ================================================================================================ export
def cmd_export(a):
    out = Path(os.path.expanduser(a.out or ROOT))
    mat = Path(os.path.expanduser(a.mat or out / "raw" / "Cervical_Database.mat"))
    md5 = md5_of(mat)
    if md5 != MAT_MD5:
        print(f"WARNING: {mat} md5 {md5} is not the verified {MAT_MD5}; the counts below are of THIS file", flush=True)
    (out / "raw").mkdir(parents=True, exist_ok=True)
    dst = out / "raw" / "Cervical_Database.mat"
    if not dst.exists() or os.path.realpath(dst) != os.path.realpath(mat):
        if not (dst.exists() and md5_of(dst) == md5):
            shutil.copy2(mat, dst)
    seqs = load(mat, a.coord_origin)
    offsets, status = load_offsets(a.offsets)
    (out / "meta").mkdir(parents=True, exist_ok=True)
    written = set()
    lv_seq, lv_frames, lv_nan = collections.Counter(), collections.Counter(), collections.Counter()
    n_frames = 0
    for s in seqs:
        off = offsets.get(s.seq, 0)
        for m in seq_metas(s, off, status if s.seq in offsets else "unverified", a.coord_origin):
            json.dump(m, open(out / "meta" / f"{m['stem']}.json", "w", encoding="utf-8"), separators=(",", ":"))
            written.add(m["stem"])
            n_frames += 1
        for n, arr in s.levels.items():
            lv_seq[n] += 1
            ok = np.isfinite(arr).all(axis=(1, 2))
            lv_frames[n] += int(ok.sum()); lv_nan[n] += int((~ok).sum())
    stale = [p for p in (out / "meta").glob("*.json") if p.stem not in written]
    for p in stale:
        p.unlink()
    events = sorted({s.event for s in seqs})
    json.dump({"train": [], "val": [], "test": events,
               "rule": "evaluation-only corpus: every event is test (plan section 2); events a and b of one person are "
                       "one patient key (tools/patient_keys.py)"},
              open(out / "splits.json", "w", encoding="utf-8"), indent=1)
    json.dump([dict(seq=s.seq, event=s.event, person=s.person, visit=s.visit, motion=s.motion,
                    orientation=s.orientation, facing=s.facing, sex=s.sex, age=s.age, group=s.group,
                    n_frames=s.n_frames, n_machine_angle=int(len(s.machine_angle)),
                    offset=offsets.get(s.seq, 0), levels=[n for n in LEVELS if n in s.levels]) for s in seqs],
              open(out / "sequences.json", "w", encoding="utf-8"), indent=1)
    longer = [dict(seq=s.seq, extra=int(len(s.machine_angle) - s.n_frames)) for s in seqs
              if len(s.machine_angle) > s.n_frames]
    shorter = [s.seq for s in seqs if len(s.machine_angle) < s.n_frames]
    disagree = [s.seq for s in seqs if s.facing and s.facing != s.orientation]
    summ = dict(dataset="bournemouth_qf", builder=BUILDER, written=time.strftime("%Y-%m-%dT%H:%M:%S"),
                source=dict(file="raw/Cervical_Database.mat", md5=md5, md5_verified=md5 == MAT_MD5,
                            doi="10.18746/bmth.data.00000385", licence="CC BY 4.0"),
                sequences=len(seqs), events=len(events), people=len({s.person for s in seqs}), frames=n_frames,
                roles=ROLE, corner_order="anatomical: anterior-superior, anterior-inferior, posterior-inferior, "
                                         "posterior-superior",
                coord_origin=a.coord_origin, px_mm=None, offset_policy=("authors' offsets from " + a.offsets)
                if a.offsets else "0 for every sequence (unverified); never a data-fitted value",
                levels={n: dict(sequences=lv_seq[n], frames=lv_frames[n], nan_frames=lv_nan[n]) for n in LEVELS},
                nan_level_frames=int(sum(lv_nan.values())),
                orientation=dict(collections.Counter(s.orientation for s in seqs)),
                facing_from_corners=dict(collections.Counter(str(s.facing) for s in seqs)),
                orientation_facing_disagree=disagree,
                machine_angle_longer=dict(n=len(longer), extra_min=min((x["extra"] for x in longer), default=None),
                                          extra_max=max((x["extra"] for x in longer), default=None), sequences=longer),
                machine_angle_shorter=shorter, stale_metas_removed=len(stale),
                truth="the authors' semi-automatic template tracker: agreement with a validated tracker, not accuracy "
                      "against independent hand labels")
    json.dump(summ, open(out / "summary.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k not in ("machine_angle_longer", "roles")}, indent=1))
    print(f"export: {len(seqs)} sequences, {n_frames} truth metas -> {out / 'meta'}", flush=True)
    return 0


# ================================================================================================ frames
MAP_EVENT = re.compile(r"(?<![A-Za-z0-9])((?:HV|P)\d{2}[ab])(?![0-9])", re.I)
MAP_MOTION = re.compile(r"(flex|ext)", re.I)


def _norm_event(e):
    e = e.upper()
    return e[:-1] + e[-1].lower()


def dicom_sequences(dicom_dir, mapping=None):
    """{seq: [file, ...]} from a --map CSV (path relative to --dicom, event, motion) or, without one, from the event
    id and the motion word found in each file's relative path. Returns (groups, n_unmapped)."""
    root = Path(os.path.expanduser(dicom_dir))
    files = []
    for r, dirs, names in os.walk(root):
        dirs.sort()
        files += [Path(r) / n for n in sorted(names)]
    groups, unmapped = collections.defaultdict(list), 0
    mp = {}
    if mapping:
        for row in csv.DictReader(open(os.path.expanduser(mapping), encoding="utf-8")):
            mot = row["motion"].strip().lower()[:4]
            mot = "flex" if mot.startswith("flex") else "ext" if mot.startswith("ext") else None
            mp[str(Path(row["path"].strip()))] = f"{_norm_event(row['event'].strip())}_{mot}"
    for p in files:
        rel = str(p.relative_to(root))
        if mapping:
            s = mp.get(str(Path(rel)))
        else:
            me, mm = MAP_EVENT.search(rel), MAP_MOTION.search(rel)
            s = f"{_norm_event(me.group(1))}_{mm.group(1).lower()}" if me and mm else None
        if s is None:
            unmapped += 1
            continue
        groups[s].append(p)
    return groups, unmapped


HDR_FIELDS = ("Rows", "Columns", "NumberOfFrames", "PhotometricInterpretation", "BitsStored", "Manufacturer",
              "ManufacturerModelName", "InstanceNumber", "FrameTime", "CineRate", "RecommendedDisplayFrameRate",
              "PixelSpacing", "ImagerPixelSpacing", "RescaleSlope", "RescaleIntercept", "Modality")


def _hdr(ds):
    out = {}
    for f in HDR_FIELDS:
        v = getattr(ds, f, None)
        if v is None:
            continue
        if f in ("PixelSpacing", "ImagerPixelSpacing"):
            v = [float(x) for x in v]
        elif f in ("Rows", "Columns", "NumberOfFrames", "BitsStored", "InstanceNumber"):
            v = int(v)
        elif f in ("FrameTime", "CineRate", "RecommendedDisplayFrameRate", "RescaleSlope", "RescaleIntercept"):
            v = float(v)
        else:
            v = str(v)
        out[f] = v
    return out


def read_sequence(files):
    """(frames (n, H, W) float32 in stored units after any rescale, header of the first file)."""
    import pydicom
    dss = [pydicom.dcmread(str(p)) for p in files]
    dss = [d for d in dss if hasattr(d, "PixelData")]
    if not dss:
        raise ValueError("no pixel data")
    multi = [d for d in dss if int(getattr(d, "NumberOfFrames", 1) or 1) > 1]
    if len(multi) > 1 or (multi and len(dss) > 1):
        raise ValueError(f"{len(dss)} files for one sequence, {len(multi)} of them multi-frame: which is the cine is "
                         "ambiguous; give a --map")
    if not multi:
        dss.sort(key=lambda d: int(getattr(d, "InstanceNumber", 0) or 0))
    arr = np.concatenate([np.asarray(d.pixel_array).reshape(-1, int(d.Rows), int(d.Columns)) for d in dss], 0)
    h = _hdr(dss[0])
    arr = arr.astype(np.float32) * float(h.get("RescaleSlope", 1.0)) + float(h.get("RescaleIntercept", 0.0))
    return arr, h


def quad_masks(q, shape):
    """(C4 quad mask, prevertebral band mask) from anatomical corners q (AS, AI, PI, PS). The band runs from 0.25 to
    0.75 endplate lengths anterior of the anterior wall: prevertebral soft tissue and airway, both less attenuating
    than the vertebral body."""
    from PIL import Image, ImageDraw
    AS, AI, PI, PS = q
    u = 0.5 * (AS + AI) - 0.5 * (PS + PI)
    u = u / max(np.linalg.norm(u), 1e-9)
    L = 0.5 * (np.linalg.norm(AS - PS) + np.linalg.norm(AI - PI))
    band = [AS + 0.25 * L * u, AI + 0.25 * L * u, AI + 0.75 * L * u, AS + 0.75 * L * u]
    out = []
    for poly in ([AS, AI, PI, PS], band):
        im = Image.new("L", (shape[1], shape[0]), 0)
        ImageDraw.Draw(im).polygon([(float(x) + 0.5, float(y) + 0.5) for x, y in poly], fill=1)
        out.append(np.asarray(im, bool))
    return out


def ladder(v, q, t=OR_T):
    """deepfluoro_anchor.window_or's mapping with the percentiles q given (one ladder per sequence)."""
    q = np.maximum.accumulate(np.asarray(q, np.float64) + np.arange(len(q)) * 1e-6)
    t = np.asarray(t, np.float64)
    out = np.interp(v, q, t)
    lo_s = (t[1] - t[0]) / max(q[1] - q[0], 1e-9); hi_s = (t[-1] - t[-2]) / max(q[-1] - q[-2], 1e-9)
    out = np.where(v < q[0], t[0] + (v - q[0]) * lo_s, out)
    out = np.where(v > q[-1], t[-1] + (v - q[-1]) * hi_s, out)
    return np.clip(out, 0, 255)


def cmd_frames(a):
    """DICOM cine -> images/<seq>_f####.png (8-bit, bone bright, one window per SEQUENCE so nothing flickers)."""
    import carmlspine_io as CIO
    root = Path(os.path.expanduser(a.root or ROOT))
    mat = Path(os.path.expanduser(a.mat or root / "raw" / "Cervical_Database.mat"))
    seqs = {s.seq: s for s in load(mat, a.coord_origin)}
    offsets, status = load_offsets(a.offsets)
    groups, unmapped = dicom_sequences(a.dicom, a.map)
    unknown = sorted(s for s in groups if s not in seqs)
    todo = sorted(s for s in groups if s in seqs)
    if a.face == "L":
        todo = [s for s in todo if seqs[s].orientation == "R"]
    if a.seq:
        todo = [s for s in todo if s in set(a.seq)]
    print(f"frames: {len(todo)} sequences to write ({len(groups)} found in the DICOM, {len(unknown)} not in the .mat, "
          f"{unmapped} files mapped to no sequence), face {a.face}", flush=True)
    img_dir = root / ("images" if a.face == "asis" else "images_faceL")
    img_dir.mkdir(parents=True, exist_ok=True)
    # 1. read the headers of every sequence; group by device
    info = {}
    for s in todo:
        import pydicom
        h = _hdr(pydicom.dcmread(str(groups[s][0]), stop_before_pixels=True))
        info[s] = dict(files=len(groups[s]), header=h,
                       device=f"{h.get('Manufacturer', '?')} | {h.get('ManufacturerModelName', '?')}")
    # 2. POLARITY, decided once for the dataset: the PhotometricInterpretation gives the displayed brightness, then on
    # up to 5 frames per device the C4 body must be brighter than the prevertebral band. A split vote is refused.
    votes = []
    by_dev = collections.defaultdict(list)
    for s in todo:
        by_dev[info[s]["device"]].append(s)
    for dev, ss in sorted(by_dev.items()):
        pick = [ss[int(i)] for i in np.linspace(0, len(ss) - 1, min(5, len(ss))).round().astype(int)]
        for s in dict.fromkeys(pick):
            S = seqs[s]
            if "C4" not in S.levels:
                continue
            arr, h = read_sequence(groups[s])
            off = offsets.get(s, 0)
            avail = min(S.n_frames, arr.shape[0] - off)
            if avail <= 0:
                continue
            fin = np.flatnonzero(np.isfinite(S.levels["C4"][:avail]).all(axis=(1, 2)))
            if not len(fin):
                continue
            k = int(fin[np.argmin(np.abs(fin - avail // 2))])
            img = arr[k + off]
            b = -img if h.get("PhotometricInterpretation") == "MONOCHROME1" else img
            mq, mb = quad_masks(S.levels["C4"][k], img.shape)
            votes.append(dict(device=dev, seq=s, frame=k + off, photometric=h.get("PhotometricInterpretation"),
                              quad_mean=float(b[mq].mean()), band_mean=float(b[mb].mean()),
                              bone_brighter_as_displayed=bool(b[mq].mean() > b[mb].mean())))
    yes = sum(v["bone_brighter_as_displayed"] for v in votes)
    if a.polarity == "auto":
        if not votes:
            raise SystemExit("frames: polarity auto found no frame with a C4 template to check; pass --polarity")
        if 0 < yes < len(votes):
            raise SystemExit(f"frames: polarity votes split ({yes} of {len(votes)} frames show the C4 body brighter "
                             "than the prevertebral band as displayed); look at the frames and pass --polarity")
        invert = yes == 0
    else:
        invert = a.polarity == "invert"
    decision = dict(mode=a.polarity, invert_displayed=invert, votes=votes,
                    rule="displayed = stored value, negated for MONOCHROME1; inverted once more when the C4 body is "
                         "darker than the prevertebral band on every checked frame; decided once for the dataset")
    print(f"frames: polarity {a.polarity}: {yes}/{len(votes)} checked frames show bone brighter as displayed -> "
          f"{'invert' if invert else 'as displayed'}", flush=True)
    # 3. one window per sequence, then every frame
    written_text = []
    meta_dir = None
    if a.face == "L":
        meta_dir = root / "meta_faceL"; meta_dir.mkdir(parents=True, exist_ok=True)
    for s in todo:
        S = seqs[s]
        arr, h = read_sequence(groups[s])
        n, H, W = arr.shape
        info[s].update(n_dicom=int(n), n_templates=S.n_frames, n_machine_angle=int(len(S.machine_angle)))
        if (H, W) != (SIZE, SIZE) and not a.allow_size_mismatch:
            info[s]["skipped"] = f"frame {W}x{H}, templates are in a {SIZE}x{SIZE} frame; scaling unknown"
            print(f"frames: {s}: SKIPPED ({info[s]['skipped']})", flush=True)
            continue
        disp = -arr if h.get("PhotometricInterpretation") == "MONOCHROME1" else arr
        if invert:
            disp = -disp
        sub = disp[np.unique(np.linspace(0, n - 1, min(16, n)).round().astype(int))]
        fld = sub[:, H // 8: 7 * H // 8, W // 8: 7 * W // 8]
        if a.window == "or":
            q = [float(x) for x in np.percentile(fld, OR_PCT)]
            win = dict(mode="or", field="central 3/4", percentiles=OR_PCT, values=q, targets=OR_T, frames_sampled=len(sub))
        else:
            q = [float(x) for x in np.percentile(fld, (0.5, 99.5))]
            win = dict(mode="pct", field="central 3/4", percentiles=(0.5, 99.5), values=q, frames_sampled=len(sub))
        info[s]["window"] = win
        from PIL import Image
        for f in range(n):
            v = disp[f]
            u8 = ladder(v, q) if a.window == "or" else np.clip((v - q[0]) / max(q[1] - q[0], 1e-9) * 255, 0, 255)
            u8 = u8.astype(np.uint8)
            if a.face == "L":
                u8 = u8[:, ::-1]
            Image.fromarray(u8).save(img_dir / f"{s}_f{f:04d}.png")
        if a.face == "L":
            off = offsets.get(s, 0)
            for m in seq_metas(S, off, status if s in offsets else "unverified", a.coord_origin):
                p = meta_dir / f"{m['stem']}.json"
                json.dump(CE.flip_meta(m, W), open(p, "w", encoding="utf-8"), separators=(",", ":"))
                written_text.append(p)
        print(f"frames: {s}: {n} frames ({S.n_frames} template rows, {len(S.machine_angle)} machine angles), "
              f"window {[round(x, 1) for x in q]}", flush=True)
    summ = dict(builder=BUILDER, written=time.strftime("%Y-%m-%dT%H:%M:%S"), face=a.face, window=a.window,
                images=str(img_dir.name), polarity=decision, n_unmapped_files=unmapped, n_sequences=len(todo),
                sequences_not_in_mat=len(unknown), coord_origin=a.coord_origin,
                sequences={s: {k: v for k, v in info[s].items() if k != "files"} | {"n_files": info[s]["files"]}
                           for s in todo},
                note="header fields are geometry, timing and encoding only; nothing identity-shaped is read into this "
                     "file. PixelSpacing / ImagerPixelSpacing / FrameTime / CineRate answer data-request questions.")
    sp = root / f"frames_summary_{a.face}.json"
    json.dump(summ, open(sp, "w", encoding="utf-8"), indent=1)
    written_text.append(sp)
    # 4. IDENTITY: every identifier string in the DICOM headers against every text byte written (counts only). A
    # header value equal to a public event id is the dataset's own pseudonym and is exempt by equality alone.
    ids = CIO.identifiers(os.path.expanduser(a.dicom))
    alias = {x for x in ids if x.lower() in {t.lower() for s in seqs.values() for t in (s.event, s.person, s.seq)}}
    ids -= alias
    hits = 0
    for p in written_text:
        blob = open(p, "rb").read()
        hits += sum(1 for x in ids if x.encode() in blob)
    summ["identifier_scan"] = dict(strings_checked=len(ids), excluded_public_event_ids=len(alias), hits=hits,
                                   files_scanned=len(written_text))
    json.dump(summ, open(sp, "w", encoding="utf-8"), indent=1)
    if hits:
        print(f"ANON_FAIL: {hits} identifier hit(s) in written text files", flush=True)
        return 3
    print(f"ANON_OK: 0 identifier hits over {len(written_text)} text files ({len(ids)} strings checked)", flush=True)
    return 0


# ================================================================================================ align
def cmd_align(a):
    """For every sequence whose MachineAngle is longer than its templates: the mean truth-to-detection IoU at each
    candidate offset 0 .. n_ma - n_t. DIAGNOSTIC ONLY: the applied offset stays 0 (or the authors' answer)."""
    root = Path(os.path.expanduser(a.root or ROOT))
    mat = Path(os.path.expanduser(a.mat or root / "raw" / "Cervical_Database.mat"))
    seqs = load(mat, a.coord_origin)
    _, preds = CE.load_preds(a.pred)
    res = {}
    for s in seqs:
        n_t, n_ma = s.n_frames, len(s.machine_angle)
        if n_ma <= n_t and not a.all:
            continue
        lv = [n for n in LEVELS if ROLE[n] == "score" and n in s.levels]
        T = np.stack([np.concatenate([s.levels[n].min(1), s.levels[n].max(1)], 1) for n in lv], 1)   # (n_t, L, 4)
        nf = max([int(re.search(r"_f(\d+)$", k).group(1)) for k in preds if k.startswith(s.seq + "_f")] + [-1]) + 1
        if nf == 0:
            continue
        P = max(1, max(len((preds.get(f"{s.seq}_f{f:04d}") or {}).get("vertebrae") or []) for f in range(nf)))
        B = np.full((nf, P, 4), np.nan)
        for f in range(nf):
            for i, v in enumerate((preds.get(f"{s.seq}_f{f:04d}") or {}).get("vertebrae") or []):
                B[f, i] = v["box"]
        row = {}
        for off in range(0, max(0, n_ma - n_t) + 1):
            k = np.arange(n_t); k = k[k + off < nf]
            if not len(k):
                break
            t = T[k][:, :, None, :]; b = B[k + off][:, None, :, :]
            ix = np.clip(np.minimum(t[..., 2], b[..., 2]) - np.maximum(t[..., 0], b[..., 0]), 0, None)
            iy = np.clip(np.minimum(t[..., 3], b[..., 3]) - np.maximum(t[..., 1], b[..., 1]), 0, None)
            inter = ix * iy
            un = (t[..., 2] - t[..., 0]) * (t[..., 3] - t[..., 1]) + (b[..., 2] - b[..., 0]) * (b[..., 3] - b[..., 1]) - inter
            io = np.where(un > 0, inter / np.where(un > 0, un, 1), 0)
            io = np.where(np.isnan(b[..., 0]), 0, io)
            best = io.max(-1)                                   # (k, L): best detection per truth body
            best = best[np.isfinite(T[k]).all(-1)]
            row[off] = dict(mean_iou=round(float(best.mean()), 4) if best.size else None, n=int(best.size))
        if row:
            valid = {o: r for o, r in row.items() if r["mean_iou"] is not None}
            best_off = max(valid, key=lambda o: valid[o]["mean_iou"]) if valid else None
            res[s.seq] = dict(n_templates=n_t, n_machine_angle=n_ma, n_pred_frames=nf, by_offset=row,
                              iou_at_0=row.get(0, {}).get("mean_iou"), argmax_offset=best_off,
                              iou_at_argmax=valid[best_off]["mean_iou"] if best_off is not None else None)
    out = Path(os.path.expanduser(a.out or root / "align.json"))
    json.dump(dict(tool="tools/bournemouth_qf_eval.py align", pred=str(a.pred), applied_offset=0,
                   note="DIAGNOSTIC ONLY. The applied offset is 0, or the authors' answer; an argmax here is never "
                        "applied, because an offset fitted to the detector's own boxes would make the truth agree "
                        "with the prediction by construction.", sequences=res), open(out, "w"), indent=1)
    moved = sum(1 for r in res.values() if r["argmax_offset"] not in (0, None))
    print(f"align: {len(res)} sequences checked; {moved} have their best IoU away from offset 0 -> {out}", flush=True)
    return 0


# ================================================================================================ self-test
def paint_loader(S, offset=0, seed=0):
    """Frames of sequence S painted from its truth arrays directly: noise, and each level's quad filled. Independent
    of the metas, so an overlay drawn from the metas that sits on the quads shows the whole path keeps coordinates."""
    from PIL import Image, ImageDraw

    def load_(stem):
        f = int(stem.rsplit("_f", 1)[1]); k = f - offset
        rng = np.random.default_rng(seed + f)
        bg = rng.integers(20, 90, (SIZE, SIZE), dtype=np.uint8)
        im = Image.fromarray(bg)
        dr = ImageDraw.Draw(im)
        for n, arr in S.levels.items():
            if 0 <= k < arr.shape[0] and np.isfinite(arr[k]).all():
                dr.polygon([(float(x) + 0.5, float(y) + 0.5) for x, y in arr[k]], fill=190 if ROLE[n] != "ignore" else 130)
        return np.asarray(im)
    return load_


def extract_frames(mp4, idx, out_dir):
    exe = CE.find_ffmpeg()
    sel = "+".join(f"eq(n\\,{i})" for i in idx)
    pat = str(Path(out_dir) / "extract_%02d.png")
    subprocess.run([exe, "-y", "-loglevel", "error", "-i", str(mp4), "-vf", f"select={sel}", "-vsync", "0", pat],
                   check=True)
    got = sorted(Path(out_dir).glob("extract_*.png"))
    named = []
    for i, p in zip(idx, got):
        q = Path(out_dir) / f"frame_{i:04d}.png"
        if q.exists():
            q.unlink()
        p.rename(q); named.append(q)
    return named


def synthetic_dicom(S, path, n, *, photometric="MONOCHROME2", bone_dark=True, identifier="Test^Identifier"):
    """A multi-frame DICOM of sequence S's first n template rows: flat field, bodies painted darker (bone dark, as
    raw fluoroscopy usually is), a fake PatientName that must never reach an output."""
    import pydicom
    from pydicom.dataset import Dataset, FileMetaDataset
    from pydicom.uid import ExplicitVRLittleEndian, generate_uid
    from PIL import Image, ImageDraw
    fr = []
    for k in range(n):
        im = Image.new("I", (SIZE, SIZE), 3000)
        dr = ImageDraw.Draw(im)
        for nm, arr in S.levels.items():
            if np.isfinite(arr[k]).all():
                dr.polygon([(float(x) + 0.5, float(y) + 0.5) for x, y in arr[k]], fill=1500 if bone_dark else 3800)
        a = np.asarray(im, np.int64).copy()
        a = (a + np.random.default_rng(k).integers(0, 60, a.shape)).astype(np.uint16)
        fr.append(a)
    arr = np.stack(fr)
    fm = FileMetaDataset()
    fm.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.7.3"
    fm.MediaStorageSOPInstanceUID = generate_uid()
    fm.TransferSyntaxUID = ExplicitVRLittleEndian
    ds = Dataset(); ds.file_meta = fm
    ds.SOPClassUID = fm.MediaStorageSOPClassUID; ds.SOPInstanceUID = fm.MediaStorageSOPInstanceUID
    ds.PatientID = S.event; ds.PatientName = identifier; ds.Modality = "RF"
    ds.Manufacturer = "SelfTest"; ds.ManufacturerModelName = "Synthetic"
    ds.Rows, ds.Columns, ds.NumberOfFrames = SIZE, SIZE, n
    ds.SamplesPerPixel = 1; ds.PhotometricInterpretation = photometric
    ds.BitsAllocated, ds.BitsStored, ds.HighBit, ds.PixelRepresentation = 16, 12, 11, 0
    ds.FrameTime = 66.67
    ds.PixelData = arr.tobytes()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    ds.save_as(str(path), enforce_file_format=True)
    return arr


def csxa_sequence(png, js, out, n=150, fps=15.0, rot_deg=10.0):
    """Tier 3: a real CSXA lateral film animated under a known smooth affine trajectory (rotation +-rot_deg about the
    C3-C7 centroid, plus translation), its annotated corners moved the same way, written as images/ + meta/ in the
    cine schema: C3-C7 score (geometric corners), C2 caudal_only (its two annotated inferior corners)."""
    from PIL import Image
    d = json.load(open(js, encoding="utf-8"))
    rx = re.compile(r"^\s*(C\d)\s+(top|bottom)\s+(left|right)\s*$", re.I)
    pts = collections.defaultdict(dict)
    for s in d.get("shapes", []):
        lab = str(s.get("label", "")).strip()
        xy = np.asarray(s.get("points") or [], float)
        if xy.ndim != 2 or not len(xy):
            continue
        xy = xy.mean(0)
        m = rx.match(lab)
        if m:
            pts[m.group(1).upper()][f"{m.group(2).lower()}_{m.group(3).lower()}"] = xy
        elif re.match(r"^\s*C2\s+centroid\s*$", lab, re.I):
            pts["C2"]["centroid"] = xy
    im = Image.open(png).convert("L")
    Wd, Hd = im.size
    full = {lv: np.array([c[k] for k in ("top_left", "top_right", "bottom_right", "bottom_left")])
            for lv, c in pts.items() if all(k in c for k in ("top_left", "top_right", "bottom_right", "bottom_left"))}
    if not full:
        raise SystemExit(f"{js}: no four-corner level")
    c0 = np.concatenate(list(full.values())).mean(0)
    stem0 = "csxasmoke_" + Path(png).stem
    out = Path(out); (out / "images").mkdir(parents=True, exist_ok=True); (out / "meta").mkdir(parents=True, exist_ok=True)
    for k in range(n):
        t = k / n
        th = math.radians(rot_deg * math.sin(2 * math.pi * t))
        tx, ty = 0.04 * Wd * math.sin(2 * math.pi * t + 1.0), 0.03 * Hd * math.sin(4 * math.pi * t)
        R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        tv = np.array([tx, ty])

        def fwd(p):
            return (np.asarray(p, float) - c0) @ R.T + c0 + tv
        Ri = R.T                                            # PIL wants output -> input, in continuous coordinates
        cc = c0 + 0.5
        cst = cc - Ri @ (cc + tv)
        fr = im.transform((Wd, Hd), Image.AFFINE, (Ri[0, 0], Ri[0, 1], cst[0], Ri[1, 0], Ri[1, 1], cst[1]),
                          resample=Image.BICUBIC, fillcolor=0)
        stem = f"{stem0}_f{k:04d}"
        fr.save(out / "images" / f"{stem}.png")
        boxes = []
        for lv in sorted(full, key=lambda l: int(l[1:])):
            q = CE.canonical_slots(fwd(full[lv]))
            boxes.append(dict(gt_id=lv, cls=0, level=lv, box=_box(q), corners=[[round(float(x), 3), round(float(y), 3)]
                                                                            for x, y in q], role="score"))
        c2 = pts.get("C2", {})
        if "bottom_left" in c2 and "bottom_right" in c2:
            cp = fwd(np.array([c2["bottom_left"], c2["bottom_right"]]))
            allp = np.concatenate([cp, fwd(c2["centroid"][None])]) if "centroid" in c2 else cp
            boxes.append(dict(gt_id="C2", cls=0, level="C2", box=_box(allp), corners=None,
                              caudal=[[round(float(x), 3), round(float(y), 3)] for x, y in cp], role="caudal_only"))
        json.dump(dict(dataset="csxa_smoke", case=stem0, stem=stem, seq=stem0, frame=k, view="LAT", px_mm=None,
                       corner_order="geometric", boxes=boxes,
                       extras=dict(rotation_deg=math.degrees(th), tx=tx, ty=ty, fps=fps,
                                   source="CSXA lateral film (in detector and encoder training: NOT held out)")),
                  open(out / "meta" / f"{stem}.json", "w", encoding="utf-8"))
    return stem0


def cmd_self_test(a):
    tiers = {t.strip() for t in str(a.tier).split(",") if t.strip()}
    out = Path(os.path.expanduser(a.out)) if a.out else Path(os.environ.get("TMP", "/tmp")) / "bqf_selftest"
    ok = True
    if "3" in tiers:
        if not (a.csxa_png and a.csxa_json):
            raise SystemExit("tier 3 needs --csxa-png and --csxa-json (a CSXA lateral film and its LabelMe JSON)")
        stem0 = csxa_sequence(a.csxa_png, a.csxa_json, out, n=a.n_frames, fps=a.fps)
        print(f"tier 3: {a.n_frames} animated frames of {stem0} -> {out}/images, truth -> {out}/meta. Next (GPU): "
              "tools/level_prototype.py --dump-corners --dump-posterior --not-held-out ..., then cine_eval track / "
              "score / video (slurm/cine_eval.sh smoke).", flush=True)
        tiers.discard("3")
        if not tiers:
            return 0
    mat = Path(os.path.expanduser(a.mat)) if a.mat else (Path(LOCAL_MAT) if Path(LOCAL_MAT).exists()
                                                           else Path(ROOT) / "raw" / "Cervical_Database.mat")
    t0 = time.time()
    seqs = load(mat, a.coord_origin)
    md5 = md5_of(mat)
    rows = []

    def row(test, expected, actual, good):
        rows.append(dict(test=test, expected=str(expected), actual=str(actual), ok=bool(good)))
    lv = collections.Counter(n for s in seqs for n in s.levels)
    orient = dict(collections.Counter(s.orientation for s in seqs))
    longer = [len(s.machine_angle) - s.n_frames for s in seqs if len(s.machine_angle) > s.n_frames]
    row("the .mat is the verified release", MAT_MD5, md5, md5 == MAT_MD5)
    row("sequences / events / people", "252 / 126 / 63",
        f"{len(seqs)} / {len({s.event for s in seqs})} / {len({s.person for s in seqs})}",
        (len(seqs), len({s.event for s in seqs}), len({s.person for s in seqs})) == (252, 126, 63))
    row("sequences carrying each level C0..T1", " ".join(f"{n} {VERIFIED['levels'][n]}" for n in LEVELS),
        " ".join(f"{n} {lv[n]}" for n in LEVELS), all(lv[n] == VERIFIED["levels"][n] for n in LEVELS))
    row("orientation L / R", "226 / 26", f"{orient.get('L')} / {orient.get('R')}", orient == VERIFIED["orientation"])
    row("sequences whose MachineAngle is longer than the templates (by 1..59)", "87 (1..59)",
        f"{len(longer)} ({min(longer)}..{max(longer)})", len(longer) == 87 and min(longer) == 1 and max(longer) == 59)
    fac = collections.Counter((s.orientation, s.facing) for s in seqs)
    row("facing from the anatomical corners agrees with the file's orientation", "L:226 of 226, R:25 of 26",
        f"L:{fac[('L', 'L')]} of {orient.get('L')}, R:{fac[('R', 'R')]} of {orient.get('R')}",
        fac[("L", "L")] == 226 and fac[("R", "R")] == 25)
    nan_lf = sum(int((~np.isfinite(a_).all(axis=(1, 2))).sum()) for s in seqs for a_ in s.levels.values())
    all_lf = sum(a_.shape[0] for s in seqs for a_ in s.levels.values())
    nan_f = sum(int((~np.all([np.isfinite(a_).all(axis=(1, 2)) for a_ in s.levels.values()], 0)).sum()) for s in seqs)
    all_f = sum(s.n_frames for s in seqs)
    row("NaN (failed-track) level-frames / sequence-frames with any NaN level", "472 of 467,369 level-frames (0.10%)",
        f"{nan_lf} of {all_lf} level-frames ({100 * nan_lf / all_lf:.2f}%); {nan_f} of {all_f} frames "
        f"({100 * nan_f / all_f:.2f}%)", nan_lf == 472 and all_lf == 467369)
    ok &= CE.print_table(rows, f"loader ({mat}, {time.time() - t0:.1f} s)")
    S = next(s for s in seqs if s.seq == "HV01a_flex")
    metas = seq_metas(S, 0, "unverified", a.coord_origin)
    if "1" in tiers:
        R = next(s for s in seqs if s.orientation == "R" and s.facing == "R")
        rows1 = CE.battery(metas, fps=a.fps, flip_metas=seq_metas(R, 0, "unverified", a.coord_origin), width=SIZE)
        ok &= CE.print_table(rows1, f"tier 1: metric unit tests on {S.seq} ({S.n_frames} frames, facing {S.facing}); "
                                    f"mirror test on {R.seq} ({R.n_frames} frames, orientation R)")
    if "2" in tiers:
        from PIL import Image
        t2 = out / "tier2"
        shutil.rmtree(t2, ignore_errors=True); t2.mkdir(parents=True)
        cfg, csha, _ = CE.load_tracker_config(None) if CE.TRACKER_CONFIG.exists() else (CE.TRACKER_DEFAULTS, None, None)
        preds = CE.perfect_preds(metas)
        tf = CE.run_tracker([(m["frame"], m["stem"], preds[m["stem"]]) for m in metas], cfg, a.fps)
        track = {f["stem"]: f["tracks"] for f in tf}
        fr = [(m["frame"], m["stem"], m, preds[m["stem"]], track[m["stem"]]) for m in metas]
        loader = paint_loader(S)
        mp4 = t2 / f"{S.seq}.mp4"
        rec = CE.render_video(fr, loader, mp4, a.fps)
        n = len(metas)
        idx = [0, n // 2, n - 1]
        got = extract_frames(mp4, idx, t2)
        # the numbers behind the look. The painted frame comes from the .mat arrays; the overlay from the metas, the
        # predictions and the tracker. Every score truth box's centre must be on a painted quad, and in the DECODED
        # video the box's top edge must carry overlay colour (the drawn boxes) while its centre still shows the quad
        rows2 = [dict(test="video written", expected=f"{n} frames, libx264; 3 frames extracted",
                      actual=f"{rec['frames']} frames, {rec['encoder']}; {len(got)} extracted",
                      ok=rec["frames"] == n and mp4.exists() and mp4.stat().st_size > 0 and len(got) == 3)]
        for i, p in zip(idx, got):
            m = metas[i]
            raw = loader(m["stem"]).astype(int)
            dec = np.asarray(Image.open(p).convert("RGB")).astype(int)
            diff = np.abs(dec - raw[:, :, None]).sum(2)
            inside, edge_hit, centre_clean = [], [], []
            for b in m["boxes"]:
                if b["role"] != "score":
                    continue
                cx, cy = int(round((b["box"][0] + b["box"][2]) / 2)), int(round((b["box"][1] + b["box"][3]) / 2))
                inside.append(raw[cy, cx] == 190)
                x0, y0, x1, y1 = [int(round(v)) for v in b["box"]]
                band = diff[max(0, y0 - 2): y0 + 3, x0 + 4: x1 - 3].max(0)
                edge_hit.append(float(band.mean()) > 90)
                centre_clean.append(float(diff[cy - 2: cy + 3, cx - 2: cx + 3].mean()) < 45)
            rows2.append(dict(test=f"frame {i}: truth box centres on painted quads; overlay on each box's top edge; "
                                   "quad visible at each box centre",
                              expected=f"{len(inside)}/{len(inside)}, {len(inside)}/{len(inside)}, "
                                       f"{len(inside)}/{len(inside)}",
                              actual=f"{sum(inside)}/{len(inside)}, {sum(edge_hit)}/{len(edge_hit)}, "
                                     f"{sum(centre_clean)}/{len(centre_clean)}",
                              ok=all(inside) and all(edge_hit) and all(centre_clean)))
        ok &= CE.print_table(rows2, f"tier 2: render smoke test ({S.seq}, painted quads on noise at {SIZE}x{SIZE}); "
                                    f"LOOK at {', '.join(str(p) for p in got)}")
        # the DICOM path: a synthetic bone-dark MONOCHROME2 cine of two sequences through `frames`, polarity auto
        try:
            import pydicom  # noqa: F401
            have_dicom = True
        except ImportError:
            have_dicom = False
        if have_dicom:
            dd = out / "tier2_dicom"
            shutil.rmtree(dd, ignore_errors=True)
            R = next(s for s in seqs if s.orientation == "R" and s.facing == "R")
            nfr = 6
            for s_ in (S, R):
                word = {"flex": "flexion", "ext": "extension"}[s_.motion]
                synthetic_dicom(s_, dd / "dicom" / s_.event / f"{word}.dcm", nfr)
            root = dd / "root"
            base = ["frames", "--dicom", str(dd / "dicom"), "--root", str(root), "--mat", str(mat)]
            rc1 = main(base + ["--polarity", "auto"])
            rc2 = main(base + ["--polarity", "auto", "--face", "L"])
            fs = json.load(open(root / "frames_summary_asis.json"))
            fl = json.load(open(root / "frames_summary_L.json"))
            im0 = np.asarray(Image.open(root / "images" / f"{S.seq}_f0000.png"))
            c4 = next(b for b in metas[0]["boxes"] if b["gt_id"] == "C4")
            cx, cy = int((c4["box"][0] + c4["box"][2]) / 2), int((c4["box"][1] + c4["box"][3]) / 2)
            imL = np.asarray(Image.open(root / "images_faceL" / f"{R.seq}_f0000.png"))
            imR = np.asarray(Image.open(root / "images" / f"{R.seq}_f0000.png"))
            mL = json.load(open(root / "meta_faceL" / f"{R.seq}_f0000.json"))
            rq = seq_metas(R)[0]
            c4r = next(b for b in rq["boxes"] if b["gt_id"] == "C4")
            c4l = next(b for b in mL["boxes"] if b["gt_id"] == "C4")
            rows3 = [dict(test="frames, polarity auto on a bone-dark MONOCHROME2 cine", expected="invert (0 of 2 votes "
                          "bone-brighter)", actual=f"{'invert' if fs['polarity']['invert_displayed'] else 'as displayed'} "
                          f"({sum(v['bone_brighter_as_displayed'] for v in fs['polarity']['votes'])} of "
                          f"{len(fs['polarity']['votes'])})", ok=rc1 == 0 and fs["polarity"]["invert_displayed"]),
                     dict(test="frames: the written PNG is bone bright (C4 centre vs frame median)", expected="C4 > median",
                          actual=f"{int(im0[cy, cx])} vs {int(np.median(im0))}", ok=im0[cy, cx] > np.median(im0) + 40),
                     dict(test="frames: every DICOM frame written; the fake PatientName reached no text file",
                          expected=f"{nfr} + {nfr} PNGs, 0 identifier hits",
                          actual=f"{len(list((root / 'images').glob('*.png')))} PNGs, "
                                 f"{fs['identifier_scan']['hits']} hits ({fs['identifier_scan']['strings_checked']} "
                                 f"strings checked, {fs['identifier_scan']['excluded_public_event_ids']} public event "
                                 "id exempt)",
                          ok=len(list((root / "images").glob("*.png"))) == 2 * nfr and fs["identifier_scan"]["hits"] == 0
                          and fs["identifier_scan"]["strings_checked"] >= 1),
                     dict(test="frames --face L: only the R sequence, image and truth mirrored together",
                          expected=f"{R.seq} only; image == mirrored as-is image; C4 box x0' = 1023 - x1",
                          actual=f"{sorted(fl['sequences'])}; image equal {bool(np.array_equal(imL, imR[:, ::-1]))}; "
                                 f"{c4l['box'][0]} vs {round(SIZE - 1 - c4r['box'][2], 3)}",
                          ok=rc2 == 0 and sorted(fl["sequences"]) == [R.seq] and np.array_equal(imL, imR[:, ::-1])
                          and abs(c4l["box"][0] - (SIZE - 1 - c4r["box"][2])) < 1e-6
                          and mL["extras"]["facing"] == "L")]
            ok &= CE.print_table(rows3, "tier 2b: the DICOM path (`frames`) on a synthetic 6-frame cine of two sequences")
        else:
            print("tier 2b skipped: pydicom not importable here")
    print(f"\nbournemouth_qf_eval self-test: {'ALL PASSED' if ok else 'FAILED'} (outputs in {out})", flush=True)
    return 0 if ok else 1


# ================================================================================================ main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["export", "frames", "align", "self-test"])
    ap.add_argument("--mat", default=None, help="Cervical_Database.mat (default <out|root>/raw/Cervical_Database.mat; "
                                                "self-test: the local copy, else the grid's)")
    ap.add_argument("--out", default=None, help=f"export: the dataset root (default {ROOT}); align: the JSON; "
                                                "self-test: a scratch directory")
    ap.add_argument("--root", default=None, help=f"frames / align: the dataset root (default {ROOT})")
    ap.add_argument("--coord-origin", choices=["matlab1", "zero"], default="matlab1",
                    help="matlab1 (default): the template coordinates are MATLAB 1-based pixel positions and x - 1, "
                         "y - 1 gives 0-based pixel centres. The README does not say; the data request asks")
    ap.add_argument("--offsets", default=None, help="a JSON {seq: offset} from the authors (template row k is cine "
                                                    "frame k + offset); without it every offset is 0, unverified")
    ap.add_argument("--dicom", default=None, help="frames: the directory of DICOM cine files")
    ap.add_argument("--map", default=None, help="frames: CSV path,event,motion (path relative to --dicom); without it "
                                                "the event id and flex/ext are read from each file's relative path")
    ap.add_argument("--polarity", choices=["auto", "asis", "invert"], default="auto",
                    help="frames: auto = PhotometricInterpretation, then the C4-brighter-than-prevertebral-band check "
                         "on up to 5 frames per device, decided ONCE for the dataset; asis / invert force it")
    ap.add_argument("--face", choices=["asis", "L"], default="asis",
                    help="frames: asis (default) writes images/; L writes the R sequences mirrored to images_faceL/ "
                         "with mirrored truth in meta_faceL/ (the secondary arm; the primary is as-is)")
    ap.add_argument("--window", choices=["or", "pct"], default="or",
                    help="frames: or (default) = the realxray OR ladder (p1/5/50/95/99 -> 27/47/126/216/239) over the "
                         "whole sequence; pct = linear p0.5..p99.5 over the whole sequence")
    ap.add_argument("--seq", action="append", default=[], help="frames: only these sequences")
    ap.add_argument("--allow-size-mismatch", action="store_true",
                    help="frames: write a sequence whose frame is not 1024 x 1024 (the truth is NOT rescaled)")
    ap.add_argument("--pred", default=None, help="align: a level_prototype output root (one directory per sequence)")
    ap.add_argument("--all", action="store_true", help="align: every sequence, not only the 87 with extra angles")
    ap.add_argument("--tier", default="1,2", help="self-test: 1 (metrics), 2 (render + DICOM path), 3 (CSXA frames)")
    ap.add_argument("--fps", type=float, default=15.0)
    ap.add_argument("--n-frames", type=int, default=150, help="self-test tier 3")
    ap.add_argument("--csxa-png", default=None); ap.add_argument("--csxa-json", default=None)
    a = ap.parse_args(argv)
    return {"export": cmd_export, "frames": cmd_frames, "align": cmd_align, "self-test": cmd_self_test}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
