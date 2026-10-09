# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_masked_link.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Does masked correlation align the mask with the image, and what does the mask actually buy?

An off-by-one between the mask slice and the image slice would correlate misaligned pixels and still
return a plausible number, which is this project's characteristic failure. This builds a pair of frames
whose true displacement is known exactly, on a deliberately PERIODIC column so that an aliased answer is
available and has to be rejected, then checks that the masked search finds the right one.

Measured, and it is the whole explanation for why a circular field broke the count:

    square, no mask, no filter   correlation 1.000   margin over the alias 0.430
    circle, no mask, no filter   correlation 0.570   margin over the alias 0.020
    circle, MASKED, no filter    correlation 1.000   margin over the alias 0.378
    circle, MASKED + highpass    correlation 0.850   margin over the alias 0.309
    circle, no mask, highpass    correlation 0.593   margin over the alias 0.201

The unexposed corners did not destroy the signal. They destroyed the MARGIN. At 0.020 the true
displacement and the one-body alias are indistinguishable, which is precisely the failure this protocol
exists to prevent, and it is why exactness fell from 99.66 per cent to 94.45 on the abdominopelvic
corpus and to 74.65 on the whole-spine one when nothing changed but the shape of the field.

Masking restores a correlation of exactly 1.000. That can only happen if the mask and the image slices
align perfectly, so this is a correctness test and a mechanism at the same time.

Run:  python tools/test_masked_link.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sweep_map as SM  # noqa: E402

H, W = 400, 200
TRUE_DY, TRUE_DX = -70, 3
PITCH = 39.0


def frames():
    """Two crops of one periodic column, displaced by a known amount."""
    rng = np.random.RandomState(0)
    base = rng.randint(40, 200, (H + 200, W + 40)).astype(np.uint8)
    for k in range(0, H + 200, int(PITCH)):
        base[k:k + 18, 60:150] = 235          # the repeating body, so an alias exists
    lower = base[100:100 + 220, 20:20 + W].copy()
    upper = base[100 + TRUE_DY:100 + TRUE_DY + 220, 20 + TRUE_DX:20 + TRUE_DX + W].copy()
    return lower, upper


def run(lower, upper, stop, masked, prefilter):
    SM.FIELD_STOP, SM.FIELD_OPEN = stop, 1.0
    SM.MASKED_NCC, SM.PREFILTER, SM.PREFILTER_BODY = masked, prefilter, 0.75
    lo = {"img": SM.apply_field_stop(lower.copy())}
    up = {"img": SM.apply_field_stop(upper.copy())}
    lo["mask"] = SM.field_mask(lo["img"].shape)
    up["mask"] = SM.field_mask(up["img"].shape)
    if prefilter == "highpass":
        lo["img_hp"] = SM.highpass(lo["img"], PITCH)
        up["img_hp"] = SM.highpass(up["img"], PITCH)
    r = SM.ncc_shift(lo, up, TRUE_DY, PITCH, step=1)
    if r is None:
        return None, "no result"
    ok = r["dy"] == TRUE_DY and abs(r["dx"] - TRUE_DX) <= 1
    return ok, "%-7s dy=%4d (true %d)  dx=%2d (true %d)  ncc=%.3f  margin=%.3f" % (
        "CORRECT" if ok else "WRONG", r["dy"], TRUE_DY, r["dx"], TRUE_DX, r["ncc"], r["margin"])


def main() -> int:
    lower, upper = frames()
    cases = [("square, no mask, no filter", "none", False, "none"),
             ("circle, no mask, no filter", "circle", False, "none"),
             ("circle, MASKED, no filter ", "circle", True, "none"),
             ("circle, MASKED + highpass ", "circle", True, "highpass"),
             ("circle, no mask, highpass ", "circle", False, "highpass")]
    bad = 0
    for label, stop, masked, pre in cases:
        ok, line = run(lower, upper, stop, masked, pre)
        print(f"{label} : {line}")
        if not ok:
            bad += 1
    print()
    if bad:
        print(f"FAIL: {bad} of {len(cases)} cases found the wrong displacement")
        return 1
    print("every case found the true displacement; the mask is aligned with the image it masks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
