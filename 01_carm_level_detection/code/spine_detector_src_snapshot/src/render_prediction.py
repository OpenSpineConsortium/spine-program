# Copied 2026-10-08 from a local snapshot of the private repository OpenSpineConsortium/spine-detector: src/render_prediction.py [commit unknown: the snapshot has no .git; files dated 2026-09-01 to 2026-09-12; the live tree is grid HOME/spine-detector]
"""Run the deployed detector on one film and draw what it found.

This exists because a number is not an answer about a detector. AP50 and PCK are computed
over a test split; they say nothing about whether THIS film worked, and a film a user
brought is usually the one that is off-distribution in some way the split never sampled.
Rendering the corners onto the film is the only check that shows what a reader would see.

Preprocessing and decode are copied deliberately from check_fp16_films.py, which is the
path the website runs: letterbox to 1024 on the long side with (114,114,114) padding,
conf 0.25, greedy NMS at IoU 0.7. If those drift apart the local render stops predicting
the site, which is the whole point of it.

    python src/render_prediction.py FILM.png --model dist/v11m_1024_v4_fp16.onnx --out out.png
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image, ImageDraw

# Read from the model rather than assumed: a 640 export and a 1024 export are the same
# network at different input sizes, and feeding one the other's tensor is an immediate
# InvalidArgument rather than a silent wrong answer -- but only because the export is
# static. Taking it from the session keeps this tool correct for both.
IMG = 1024
CONF = 0.25
IOU = 0.7


def letterbox(im: Image.Image):
    """Resize long side to 1024 and pad to square. Returns the tensor and the inverse map."""
    s = min(IMG / im.width, IMG / im.height)
    w, h = max(1, int(im.width * s)), max(1, int(im.height * s))
    r = im.convert("RGB").resize((w, h), Image.BILINEAR)
    canvas = Image.new("RGB", (IMG, IMG), (114, 114, 114))
    ox, oy = (IMG - w) // 2, (IMG - h) // 2
    canvas.paste(r, (ox, oy))
    a = np.asarray(canvas, np.float32).transpose(2, 0, 1) / 255.0
    return a[None], (s, ox, oy)


def nms(cand: np.ndarray, iou_thr: float = IOU) -> np.ndarray:
    if len(cand) == 0:
        return cand
    xy, wh, conf = cand[:, :2], cand[:, 2:4], cand[:, 4]
    x1, y1 = xy[:, 0] - wh[:, 0] / 2, xy[:, 1] - wh[:, 1] / 2
    x2, y2 = xy[:, 0] + wh[:, 0] / 2, xy[:, 1] + wh[:, 1] / 2
    area = (x2 - x1) * (y2 - y1)
    order = np.argsort(-conf)
    keep = []
    while len(order):
        i = order[0]
        keep.append(i)
        if len(order) == 1:
            break
        rest = order[1:]
        xx1 = np.maximum(x1[i], x1[rest]); yy1 = np.maximum(y1[i], y1[rest])
        xx2 = np.minimum(x2[i], x2[rest]); yy2 = np.minimum(y2[i], y2[rest])
        inter = np.clip(xx2 - xx1, 0, None) * np.clip(yy2 - yy1, 0, None)
        iou = inter / (area[i] + area[rest] - inter + 1e-9)
        order = rest[iou < iou_thr]
    return cand[np.array(keep)]


def decode(out: np.ndarray):
    a = out[0]
    keep = a[4] > CONF
    return nms(a[:, keep].T)


def unmap(pts: np.ndarray, m) -> np.ndarray:
    """Letterbox space -> original pixel coordinates."""
    s, ox, oy = m
    q = pts.copy().astype(np.float64)
    q[..., 0] = (q[..., 0] - ox) / s
    q[..., 1] = (q[..., 1] - oy) / s
    return q


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--repeats", type=int, default=5)
    a = ap.parse_args()

    im = Image.open(a.film)
    print(f"film   {Path(a.film).name}  {im.width}x{im.height}  aspect {im.height/im.width:.3f}")

    sess = ort.InferenceSession(a.model, providers=["CPUExecutionProvider"])
    inp = sess.get_inputs()[0]
    name = inp.name
    global IMG
    if isinstance(inp.shape[2], int) and inp.shape[2] > 0:
        IMG = int(inp.shape[2])
    x, m = letterbox(im)

    sess.run(None, {name: x})                      # warm up; first run builds the plan
    t = time.perf_counter()
    for _ in range(a.repeats):
        raw = sess.run(None, {name: x})[0]
    ms = (time.perf_counter() - t) / a.repeats * 1000
    print(f"model  {Path(a.model).name}  output {raw.shape}  {ms:.0f} ms/inference (CPU)")

    det = decode(raw)
    nk = (raw.shape[1] - 5) // 3
    print(f"detections after NMS: {len(det)}   keypoints per detection: {nk}")
    if len(det) == 0:
        print("NOTHING DETECTED at conf 0.25")
        return 1

    kp = det[:, 5:].reshape(len(det), nk, 3)
    corners = unmap(kp[:, :, :2], m)
    conf = det[:, 4]
    ctr = unmap(det[:, :2], m)

    order = np.argsort(ctr[:, 1])                  # cranial to caudal
    canvas = im.convert("RGB").copy()
    d = ImageDraw.Draw(canvas)
    for rank, i in enumerate(order, 1):
        pts = [tuple(p) for p in corners[i]]
        d.polygon(pts, outline=(0, 220, 120))
        for p in pts:
            d.ellipse([p[0] - 2.5, p[1] - 2.5, p[0] + 2.5, p[1] + 2.5], fill=(255, 90, 60))
        d.text((ctr[i][0] + 6, ctr[i][1] - 6), f"{rank} {conf[i]:.2f}", fill=(255, 220, 0))
    canvas.save(a.out)
    print(f"wrote {a.out}")

    print("\n  #   conf   centre (x,y)      body height px")
    for rank, i in enumerate(order, 1):
        c = corners[i]
        hgt = np.linalg.norm(c.mean(axis=0) - c[0]) * 2
        print(f"  {rank:<3} {conf[i]:.3f}  ({ctr[i][0]:6.1f},{ctr[i][1]:6.1f})   {hgt:5.1f}")
    print(f"\n  confidence: min {conf.min():.3f}  median {np.median(conf):.3f}  max {conf.max():.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
