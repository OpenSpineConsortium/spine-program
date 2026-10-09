#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/data_manifest.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""The data manifest the RSNA AI paper's Table 1 is checked against (docs/RSNAI_PLAN.md, box E1).

One entry per dataset root: source (DOI / URL), licence, device, what the root holds (file count, total bytes, extension
histogram), and a SHA-256 over the sorted list of (relative path, size) -- a content-list hash that changes when a
file is added, removed or resized, cheap enough to recompute on every check (hashing 950 GB of projections is not).
Optionally (`--content N`) the SHA-256 of the first N bytes of every file is folded in. Splits used by the experiments
are recorded by path so a reviewer can see which case went where.

    python tools/data_manifest.py build --out docs/RSNAI_DATA_MANIFEST.json
    python tools/data_manifest.py check --manifest docs/RSNAI_DATA_MANIFEST.json     # exit 1 if any root drifted
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import sys
import time
from pathlib import Path

D = "/rs/rs_grp_oschome/go2432/data"
H = os.path.expanduser("~")
ROOTS = {
    "deepfluoro_h5": dict(path=f"{H}/deepfluoro/unpacked_full", source="Grupp et al. 2020, DeepFluoro, JHU (ipcai_2020_full_res_data.h5)", licence="CC BY-NC-SA 4.0 (dataset)",
                          device="Siemens Cios Fusion (CsI flat panel, 0.194 mm, 1536^2)", paired="CT + pose (6 cadaveric pelves, 366 frames)"),
    "deepfluoro_vendor": dict(path=f"{D}/deepfluoro_vendor/unpacked", source="JHU Dataverse vendor DICOMs (doi:10.7281/T1/IFSXNV)", licence="see LICENSE in archive",
                              device="Siemens Cios Fusion", paired="vendor DICOM headers of the same frames"),
    "carmlspine": dict(path=f"{D}/carmlspine/unpacked/C-ArmLSpine", source="C-ArmLSpine, Zenodo 10.5281/zenodo.22768651", licence="CC BY 4.0",
                       device="FIRST/Yiying Surgio-B51 (flat panel, 0.15 mm, 2048^2; raw sweeps 1024^2)", paired="CBCT per case; poses by registration (data/carmlspine/pose)"),
    "carmlspine_pose": dict(path=f"{D}/carmlspine/pose", source="this project: tools/carmlspine_pose.py", licence="-", device="-", paired="registered poses per frame"),
    "cobra2026": dict(path=f"{D}/cobra2026/cases", source="COBRA2026, Zenodo 10.5281/zenodo.21322350; CREATIS Girder", licence="CC BY-NC 4.0",
                      device="Elekta XVI (centres A-D, 504^2 at 0.8 mm) and Varian OBI (F-G)", paired="planning CT deformably registered + RTK geometry per projection"),
    "geneva_hip": dict(path=f"{D}/realxray_work/geneva_hip", source="D'Isidoro et al. 2021, Yareta 10.26037/yareta:2kw5s2jadbbv3ngtkzsovihtnu", licence="CC BY-SA 4.0 (repository)",
                       device="Philips BV Pulsera (image intensifier, 0.29 mm, 1000^2)", paired="CT + gold-standard poses (19)"),
    "ljubljana": dict(path=f"{D}/ljubljana", source="Tomazevic et al. 2002, lit.fe.uni-lj.si 2D-3D-GS", licence="CC BY-NC-ND",
                      device="Trixell PIXIUM 4600 flat panel (turntable radiograph, 0.286 mm supplied)", paired="CT + 18 gold-standard poses"),
    "spinesac": dict(path=f"{D}/spinesac/drive", source="SpineSAC (Google Drive)", licence="see repository",
                     device="Philips Allura Xper, GE Fluorostar, Ziehm NetPort, Siemens Healthineers (model unnamed), Skanray, Siemens Fluorospot Compact S1", paired="phantom CTs + scenario poses; no bone truth yet"),
    "realxray": dict(path=f"{D}/realxray", source="this project: tools/realxray_*_export.py", licence="-", device="-", paired="the common real-frame layout (images/labels/meta/splits.json) per device"),
    "or_ready": dict(path=f"{D}/or_ready", source="this project", licence="-", device="-", paired="every result JSON of the readiness program"),
    "devcorpus": dict(path=f"{D}/devcorpus", source="this project: tools/devcorpus_build.py", licence="-", device="-", paired="pose pools, renders, styled corpora, LODO lists"),
    "ts_subjects": dict(path=f"{H}/data/TotalSegmentator_v3/Totalsegmentator_dataset_v300", source="TotalSegmentator v2 dataset (Wasserthal et al.)", licence="CC BY 4.0",
                        device="-", paired="whole-spine CTs used for renders (subject list ~/model_night/ts_clean_subjects.txt)"),
    "polypose_bank": dict(path=f"{D}/polypose", source="this project: tools/polypose_sample.py, warped with PolyPose (Gopalakrishnan, Dey, Golland, NeurIPS 2025; MIT)", licence="-",
                          device="-", paired="SYNTHETIC curvature variants of held CTs; every volume keyed to its SOURCE patient (manifest/rows.jsonl + ann sidecars; origin column 'polypose' in the ledger)"),
}
SPLITS = [f"{D}/realxray/carmlspine/splits.json", f"{D}/realxray/cobra_elekta/splits.json", f"{D}/realxray/deepfluoro/splits.json",
          f"{D}/realxray/geneva_hip/splits.json", f"{H}/model_night/ts_clean_subjects.txt"]


def walk(root, content=0, max_files=0):
    rows = []; exts = collections.Counter(); total = 0
    for dp, dn, fn in os.walk(root):
        dn.sort()
        for f in sorted(fn):
            p = os.path.join(dp, f)
            try:
                sz = os.path.getsize(p)
            except OSError:
                continue
            rel = os.path.relpath(p, root).replace("\\", "/")
            rows.append((rel, sz)); exts[os.path.splitext(f)[1].lower() or "(none)"] += 1; total += sz
            if max_files and len(rows) >= max_files:
                break
    h = hashlib.sha256()
    for rel, sz in rows:
        h.update(f"{rel}\t{sz}\n".encode())
    ch = None
    if content:
        hc = hashlib.sha256()
        for rel, sz in rows:
            try:
                with open(os.path.join(root, rel), "rb") as fh:
                    hc.update(fh.read(content))
            except OSError:
                hc.update(b"<unreadable>")
        ch = hc.hexdigest()
    return dict(files=len(rows), bytes=total, extensions=dict(exts.most_common(12)), list_sha256=h.hexdigest(), content_head_sha256=ch, content_head_bytes=content or None)


def cmd_build(a):
    out = dict(built=time.strftime("%Y-%m-%d %H:%M"), host=os.uname().nodename, roots={}, splits={})
    for name, meta in ROOTS.items():
        p = meta["path"]
        if not os.path.isdir(p):
            out["roots"][name] = dict(meta, present=False); print(f"{name}: MISSING {p}", flush=True); continue
        t0 = time.time(); w = walk(p, a.content)
        out["roots"][name] = dict(meta, present=True, **w, seconds=int(time.time() - t0))
        print(f"{name}: {w['files']} files, {w['bytes'] / 1e9:.2f} GB, {w['list_sha256'][:12]} ({int(time.time() - t0)} s)", flush=True)
    for sp in SPLITS:
        if os.path.exists(sp):
            b = open(sp, "rb").read(); out["splits"][sp] = dict(sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
        else:
            out["splits"][sp] = None
    json.dump(out, open(a.out, "w"), indent=1)
    print("wrote", a.out)
    return 0


def cmd_check(a):
    m = json.load(open(a.manifest)); bad = 0
    for name, r in m["roots"].items():
        if not r.get("present"):
            continue
        w = walk(r["path"], r.get("content_head_bytes") or 0)
        ok = w["list_sha256"] == r["list_sha256"] and (r.get("content_head_sha256") is None or w["content_head_sha256"] == r["content_head_sha256"])
        print(f"{name}: {'ok' if ok else 'DRIFT'} ({w['files']} files vs {r['files']}; {w['bytes']} vs {r['bytes']} bytes)", flush=True)
        bad += not ok
    for sp, rec in m["splits"].items():
        if rec and os.path.exists(sp):
            h = hashlib.sha256(open(sp, "rb").read()).hexdigest()
            if h != rec["sha256"]:
                print(f"split DRIFT: {sp}"); bad += 1
    print("MANIFEST_OK" if not bad else f"MANIFEST_DRIFT {bad}")
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "check"])
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "docs" / "RSNAI_DATA_MANIFEST.json"))
    ap.add_argument("--manifest", default=str(Path(__file__).resolve().parents[1] / "docs" / "RSNAI_DATA_MANIFEST.json"))
    ap.add_argument("--content", type=int, default=0, help="also hash the first N bytes of every file (slow on CephFS)")
    a = ap.parse_args()
    return dict(build=cmd_build, check=cmd_check)[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
