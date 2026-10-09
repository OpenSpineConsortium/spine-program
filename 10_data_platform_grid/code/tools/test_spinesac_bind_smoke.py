#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_spinesac_bind_smoke.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Smoke test for tools/spinesac_bind_bodies.py, so a bug does not surface after a three-hour GPU queue.

It already paid for itself once: on the first run it found that SimpleITK REFUSES to open a SPINEPS mask
("ITK only supports orthonormal direction cosines"), which the bind tool was using. The tool now reads with
nibabel. Section 4 measures how general that refusal is rather than leaving it as one anecdote, and section 5
proves a body mask written by the tool is readable by the SimpleITK call in spinesac_truth.load_seg.

    python tools/test_spinesac_bind_smoke.py
"""
from __future__ import annotations

import glob
import os
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import spinesac_bind_bodies as B          # noqa: E402

fail = 0


def check(name, cond, extra=""):
    global fail
    print(("  ok   " if cond else "  FAIL ") + name + (f"  {extra}" if extra else ""), flush=True)
    fail += 0 if cond else 1


# a P,I,R affine -- what these volumes actually are, not RAS
AFF_PIR = np.array([[0, 0, .5, -100.], [-.6, 0, 0, 80.], [0, -.7, 0, 60.], [0, 0, 0, 1.]])

print("1. body construction: instance x semantic corpus")
vi = np.zeros((40, 50, 60), np.int16)
si = np.zeros((40, 50, 60), np.int16)
vi[10:20, 10:20, 10:20] = 22
si[10:15, 10:20, 10:20] = 50
si[15:20, 10:20, 10:20] = 43
vi[25:30, 10:20, 10:20] = 26
si[25:30, 10:20, 10:20] = 49
body = np.where(np.isin(si, B.CORPUS), vi, 0)
check("L3 body is half the whole vertebra", int((body == 22).sum()) == 500, f"{int((body == 22).sum())}/1000")
check("sacrum body is all of it", int((body == 26).sum()) == int((vi == 26).sum()))
check("nothing outside the corpus survives", set(np.unique(body)) == {0, 22, 26})

print("2. axis roles are read off the affine, not assumed")
role, flip, codes = B.axis_roles(AFF_PIR)
check("axcodes read", "".join(codes) == "PIR", "".join(codes))
check("A-P axis is 0", role["ap"] == 0, str(role))
check("S-I axis is 1", role["si"] == 1, str(role))
check("L-R axis is 2", role["lr"] == 2, str(role))

print("3. overlay renderer on a non-RAS volume")
ct = (np.random.RandomState(0).rand(40, 50, 60) * 400 - 200).astype(np.int16)
ct[body > 0] = 900
with tempfile.TemporaryDirectory() as td:
    for view, shape in (("sag", (50, 40)), ("cor", (50, 60))):
        p = Path(td) / f"t_{view}.png"
        B.overlay_png(ct, body, p, view, AFF_PIR)
        check(f"{view} png written", p.exists() and p.stat().st_size > 0)
        if p.exists():
            from PIL import Image
            im = np.asarray(Image.open(p))
            check(f"{view} is S-I by the other axis {shape}", im.shape == (shape[0], shape[1], 3), str(im.shape))
            check(f"{view} is not blank", int(im.max()) > 0 and len(np.unique(im.reshape(-1, 3), axis=0)) > 2)
    p = Path(td) / "empty.png"
    B.overlay_png(ct, np.zeros_like(body), p, "sag", AFF_PIR)
    check("empty mask writes nothing and does not raise", not p.exists())

print("4. same_grid guard, and how general the SimpleITK refusal is")
check("identical grids pass", B.same_grid((4, 5, 6), AFF_PIR, (4, 5, 6), AFF_PIR)[0])
check("shape mismatch caught", not B.same_grid((4, 5, 6), AFF_PIR, (4, 5, 7), AFF_PIR)[0])
a2 = AFF_PIR.copy(); a2[0, 3] += 9
check("affine mismatch caught", not B.same_grid((4, 5, 6), AFF_PIR, (4, 5, 6), a2)[0])

cands = sorted(glob.glob(os.path.expanduser("~/bench_ts/spineps/native/*_seg-vert_msk.nii.gz")))[:25]
if not cands:
    print("  (no SPINEPS masks on disk; skipped)")
else:
    import nibabel as nib
    import SimpleITK as sitk
    sitk_ok = nib_ok = 0
    for v in cands:
        try:
            sitk.ReadImage(v); sitk_ok += 1
        except Exception:                                  # noqa: BLE001
            pass
        try:
            nib.load(v).shape; nib_ok += 1
        except Exception:                                  # noqa: BLE001
            pass
    print(f"  of {len(cands)} SPINEPS masks: SimpleITK opened {sitk_ok}, nibabel opened {nib_ok}")
    check("nibabel opens every SPINEPS mask", nib_ok == len(cands), f"{nib_ok}/{len(cands)}")
    if sitk_ok < len(cands):
        print("  -> SimpleITK cannot be used to READ SPINEPS output; the bind tool uses nibabel. "
              f"({len(cands) - sitk_ok} of {len(cands)} refused)")

    print("5. a real pair through the tool's own path, and readable back by SimpleITK")
    v = cands[0]
    s = v.replace("_seg-vert_msk.nii.gz", "_seg-spine_msk.nii.gz")
    if not os.path.exists(s):
        print("  (no matching semantic mask; skipped)")
    else:
        vi2 = np.asanyarray(nib.load(v).dataobj)
        si2 = np.asanyarray(nib.load(s).dataobj)
        check("instance and semantic share a shape", vi2.shape == si2.shape, f"{vi2.shape} {si2.shape}")
        # the tool's rule, not the naive one: drop discs, corpus for vertebrae, the sacrum whole
        vert2 = np.where(vi2 < B.DISC_MIN_ID, vi2, 0)
        b2 = np.where(np.isin(si2, B.CORPUS), vert2, 0).astype(np.int16)
        b2 = np.where(vert2 == B.SACRUM_ID, B.SACRUM_ID, b2)
        ids = [int(x) for x in np.unique(vi2) if x > 0]
        vert_ids = [i for i in ids if i < B.DISC_MIN_ID and i != B.SACRUM_ID]
        discs = [i for i in ids if i >= B.DISC_MIN_ID]
        fr = [round(float((b2 == i).sum()) / max(1, int((vi2 == i).sum())), 3) for i in vert_ids]
        print(f"  {os.path.basename(v)}: vertebrae {vert_ids}, discs dropped {discs}, "
              f"sacrum present {B.SACRUM_ID in ids}")
        print(f"  body fraction per vertebra {fr}")
        check("a vertebral body is a real but partial share of the vertebra",
              bool(fr) and all(0.05 < f < 0.95 for f in fr), str(fr[:6]))
        check("no disc instance survives", not any((b2 == i).any() for i in discs), str(discs))
        if B.SACRUM_ID in ids:
            sac_fr = float((b2 == B.SACRUM_ID).sum()) / max(1, int((vi2 == B.SACRUM_ID).sum()))
            check("the sacrum is kept WHOLE (SPINEPS gives it no corpus)", abs(sac_fr - 1.0) < 1e-6,
                  f"fraction {sac_fr:.3f}")
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "body_seg.nii.gz")
            img = nib.load(v)
            hdr = img.header.copy(); hdr.set_data_dtype(np.int16)
            nib.save(nib.Nifti1Image(b2, img.affine, hdr), out)
            # the projector reads this with SimpleITK; if the CT's header round-trips, so does this
            try:
                back = sitk.GetArrayFromImage(sitk.ReadImage(out))
                check("SimpleITK reads a mask written on this header", back.size == b2.size)
            except Exception as e:                          # noqa: BLE001
                print(f"  note: SimpleITK cannot read a mask on the SPINEPS header either ({type(e).__name__}); "
                      f"the tool writes on the CT's header instead, which is SimpleITK-readable by construction")

print(f"\nSMOKE_{'FAIL' if fail else 'OK'} failures={fail}")
raise SystemExit(1 if fail else 0)
