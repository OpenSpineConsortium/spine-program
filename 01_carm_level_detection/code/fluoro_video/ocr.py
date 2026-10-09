# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/ocr.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""On-screen text read programmatically (tesseract, pinned in the environment).

DISCOVERY (per video): tesseract (--psm 11, sparse text) on up to ocr_probe_frames full frames spread evenly over
the sampled frames that lie inside kept segments (the rest of the budget spread over the whole video). A word
matching the CLOCK pattern (h:mm:ss, hh:mm:ss or mm:ss), or a line matching an ANGLE pattern (LAO/RAO/CRA/CAU n,
or n followed by a degree sign), is a hit. Hits are grouped by location (centres within region_tol of the frame
size); a group is a text REGION when it has >= ocr_min_hits hits, and, for a clock, >= 2 distinct values (a
constant string is not a clock). The region box is the union of its hits padded by ocr_pad x its height.

READING (per clip): the region is cropped from the full native frame every ocr_interval_s of pts (at most
ocr_max_per_clip readings, evenly spread), scaled to ocr_target_h px high (Lanczos), binarised by Otsu, turned dark
text on light, padded, and read with --psm 7 and a character whitelist. The value is parsed with the same pattern.
"""
from __future__ import annotations

import os
import re

import numpy as np
from PIL import Image

from .common import tool_path

CLOCK_RE = re.compile(r"(?<![\d:])(\d{1,2}):([0-5]\d)(?::([0-5]\d))?(?![\d:])")
ANGLE_RES = [re.compile(r"\b(LAO|RAO|CRAN|CAUD|CRA|CAU)\s*[:=]?\s*([-+]?\d{1,3}(?:[.,]\d)?)", re.I),
             re.compile(r"([-+]?\d{1,3}(?:[.,]\d)?)\s*(?:°|º|deg\b)", re.I)]
ANGLE_SIGN = {"LAO": 1, "RAO": -1, "CRA": 1, "CRAN": 1, "CAU": -1, "CAUD": -1}


def _tess():
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = tool_path("tesseract")
    os.environ.setdefault("OMP_THREAD_LIMIT", "1")
    return pytesseract


def parse_clock(s):
    if not s:
        return None, None
    m = CLOCK_RE.search(s.replace(" ", ""))
    if not m:
        return None, None
    a, b, c = m.group(1), m.group(2), m.group(3)
    if c is not None:
        v = int(a) * 3600 + int(b) * 60 + int(c)
    else:
        v = int(a) * 60 + int(b)
    return m.group(0), float(v)


def parse_angle(s):
    if not s:
        return None, None, None
    for rx in ANGLE_RES:
        m = rx.search(s)
        if m:
            if m.lastindex == 2:
                lab = m.group(1).upper()
                v = float(m.group(2).replace(",", ".")) * ANGLE_SIGN.get(lab, 1)
                return m.group(0), v, lab
            return m.group(0), float(m.group(1).replace(",", ".")), None
    return None, None, None


def _otsu_u8(a):
    hist = np.bincount(a.ravel(), minlength=256).astype(np.float64)
    w0 = np.cumsum(hist)
    w1 = w0[-1] - w0
    m = np.cumsum(hist * np.arange(256))
    with np.errstate(divide="ignore", invalid="ignore"):
        mu0 = m / w0
        mu1 = (m[-1] - m) / w1
        b = w0 * w1 * (mu0 - mu1) ** 2
    b[~np.isfinite(b)] = -1
    return int(np.argmax(b))


def prep_line(grey, target_h):
    h, w = grey.shape
    s = max(1.0, float(target_h) / max(1, h))
    im = Image.fromarray(grey).resize((max(1, int(round(w * s))), max(1, int(round(h * s)))), Image.LANCZOS)
    a = np.asarray(im)
    t = _otsu_u8(a)
    b = a > t
    if b.mean() < 0.5:           # mostly dark background: light text -> make the text dark on light
        b = ~b
    out = np.where(b, 255, 0).astype(np.uint8)
    return np.pad(out, 12, constant_values=255)


def discover(probes, P, frame_w, frame_h):
    """probes: [(pts_s, grey full-res uint8)]. Returns (regions, raw hits)."""
    pt = _tess()
    hits = []
    for t, g in probes:
        up = 2 if g.shape[0] < int(P["ocr_upscale_below_h"]) else 1
        im = Image.fromarray(g)
        if up > 1:
            im = im.resize((g.shape[1] * up, g.shape[0] * up), Image.LANCZOS)
        d = pt.image_to_data(im, config="--psm 11 --oem 1", output_type=pt.Output.DICT)
        lines = {}
        for k in range(len(d["text"])):
            txt = (d["text"][k] or "").strip()
            try:
                conf = float(d["conf"][k])
            except Exception:
                conf = -1
            if not txt or conf < float(P["ocr_min_conf"]):
                continue
            box = [d["left"][k] / up, d["top"][k] / up, (d["left"][k] + d["width"][k]) / up,
                   (d["top"][k] + d["height"][k]) / up]
            key = (d["block_num"][k], d["par_num"][k], d["line_num"][k])
            lines.setdefault(key, []).append((txt, box))
            s, v = parse_clock(txt)
            if s is not None:
                hits.append(dict(kind="clock", t=t, text=txt, value=v, box=box))
        for key in sorted(lines):
            ws = lines[key]
            txt = " ".join(w[0] for w in ws)
            s, v, lab = parse_angle(txt)
            if s is not None:
                B = np.array([w[1] for w in ws])
                hits.append(dict(kind="angle", t=t, text=txt, value=v, label=lab,
                                 box=[float(B[:, 0].min()), float(B[:, 1].min()), float(B[:, 2].max()),
                                      float(B[:, 3].max())]))
    regions = []
    tolx, toly = float(P["ocr_region_tol"]) * frame_w, float(P["ocr_region_tol"]) * frame_h
    for kind in ("clock", "angle"):
        groups = []
        for h in [h for h in hits if h["kind"] == kind]:
            cx, cy = 0.5 * (h["box"][0] + h["box"][2]), 0.5 * (h["box"][1] + h["box"][3])
            g = next((g for g in groups if abs(g["cx"] - cx) <= tolx and abs(g["cy"] - cy) <= toly), None)
            if g is None:
                groups.append(dict(cx=cx, cy=cy, hits=[h]))
            else:
                g["hits"].append(h)
        for g in groups:
            vals = {h["value"] for h in g["hits"]}
            ok = len(g["hits"]) >= int(P["ocr_min_hits"]) and (kind != "clock" or len(vals) >= 2)
            B = np.array([h["box"] for h in g["hits"]])
            x0, y0, x1, y1 = B[:, 0].min(), B[:, 1].min(), B[:, 2].max(), B[:, 3].max()
            pad = float(P["ocr_pad"]) * (y1 - y0)
            box = [int(max(0, np.floor(x0 - pad))), int(max(0, np.floor(y0 - pad))),
                   int(min(frame_w, np.ceil(x1 + pad))), int(min(frame_h, np.ceil(y1 + pad)))]
            regions.append(dict(kind=kind, box=box, n_hits=len(g["hits"]), n_distinct=len(vals), accepted=ok,
                                examples=sorted({h["text"] for h in g["hits"]})[:6]))
    regions.sort(key=lambda r: (not r["accepted"], r["kind"], r["box"]))
    for n, r in enumerate(regions):
        r["id"] = f"T{n:02d}"
    return regions, hits


def read_region(grey_crop, kind, P):
    pt = _tess()
    img = prep_line(grey_crop, int(P["ocr_target_h"]))
    if kind == "clock":
        cfg = "--psm 7 --oem 1 -c tessedit_char_whitelist=0123456789:"
    else:
        cfg = "--psm 7 --oem 1"
    txt = pt.image_to_string(Image.fromarray(img), config=cfg).strip()
    if kind == "clock":
        s, v = parse_clock(txt)
        return txt, v, None
    s, v, lab = parse_angle(txt)
    return txt, v, lab
