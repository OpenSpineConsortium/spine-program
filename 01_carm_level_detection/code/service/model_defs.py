# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): service/model_defs.py [tracked at 097933a]
"""Level-identification inference, self-contained: detector -> per-vertebra crops -> level model -> run labeller.

This is the minimum the service needs, copied from the training code so the service repo carries no
training machinery. The crop transform must match training exactly (target box scaled to TGT_PX on a
SIZE canvas, a band of (2*rung+1) target heights kept, marker channel for the target box); the numbers
come from registry.json alongside the weights.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

LEVEL_ORDER = ([f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)] + ["T13"] + [f"L{i}" for i in range(1, 7)] + ["sacrum"])
CLASS_OF = {n: i for i, n in enumerate(LEVEL_ORDER)}
STD = [n for n in LEVEL_ORDER if n not in ("T13", "L6")]


def build_model(n_classes: int, arch: str = "resnet18") -> nn.Module:
    import torchvision.models as tvm
    m = {"resnet18": tvm.resnet18, "resnet50": tvm.resnet50}[arch](weights=None)
    conv = m.conv1
    m.conv1 = nn.Conv2d(2, conv.out_channels, conv.kernel_size, stride=conv.stride, padding=conv.padding, bias=conv.bias is not None)
    m.fc = nn.Linear(m.fc.in_features, n_classes)
    return m


class RunLabeller(nn.Module):
    def __init__(self, d_in, n_classes, hidden=256):
        super().__init__()
        self.proj = nn.Linear(d_in, hidden)
        self.gru = nn.GRU(hidden, hidden, num_layers=2, batch_first=True, bidirectional=True, dropout=0.2)
        self.head = nn.Linear(2 * hidden, n_classes)

    def forward(self, x):
        h, _ = self.gru(F.gelu(self.proj(x)))
        return self.head(h)


def resize_nn(a: np.ndarray, s: float) -> np.ndarray:
    h, w = a.shape
    nh, nw = max(1, int(round(h * s))), max(1, int(round(w * s)))
    ys = np.minimum((np.arange(nh) / s).astype(int), h - 1)
    xs = np.minimum((np.arange(nw) / s).astype(int), w - 1)
    return a[ys][:, xs]


def window(a: np.ndarray, cy: int, cx: int, size: int) -> np.ndarray:
    out = np.zeros((size, size), np.float32)
    h, w = a.shape
    y0, x0 = cy - size // 2, cx - size // 2
    sy0, sx0 = max(0, y0), max(0, x0)
    sy1, sx1 = min(h, y0 + size), min(w, x0 + size)
    if sy1 <= sy0 or sx1 <= sx0:
        return out
    out[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = a[sy0:sy1, sx0:sx1]
    return out


def gray01(arr: np.ndarray) -> np.ndarray:
    a = arr.astype(np.float32)
    lo, hi = np.percentile(a, 0.5), np.percentile(a, 99.5)
    return np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1)


def crops_for_run(img0, boxes, tgt_px, size, rung):
    out = []
    for ti, tbox in enumerate(boxes):
        th = tbox[3] - tbox[1] + 1
        s = tgt_px / float(th)
        img = resize_nn(img0, s)
        cy = int(round((tbox[1] + tbox[3]) / 2 * s)); cx = int(round((tbox[0] + tbox[2]) / 2 * s))
        sb = [[int(round(v * s)) for v in b] for b in boxes]
        mk = np.zeros_like(img); b = sb[ti]
        mk[max(0, b[1]):b[3] + 1, max(0, b[0]):b[2] + 1] = 1.0
        keep = np.zeros_like(img)
        half = int(round((2 * rung + 1) * tgt_px / 2.0))
        keep[max(0, cy - half):cy + half + 1, :] = 1.0
        out.append(np.stack([window(img * keep, cy, cx, size), window(mk, cy, cx, size)]))
    return np.stack(out)


def contiguous_run(probs: np.ndarray, floor=0.02):
    """Best contiguous run of the ordinary column for boxes ordered cranial->caudal (floored log-prob sum)."""
    n = len(probs)
    best, best_s = -1e18, None
    for s in range(0, len(STD) - n + 1):
        labels = STD[s:s + n]
        sc = float(sum(np.log(max(probs[i][CLASS_OF[l]], floor)) for i, l in enumerate(labels)))
        if sc > best:
            best, best_s = sc, labels
    return best_s or [LEVEL_ORDER[int(p.argmax())] for p in probs]


class LevelPipeline:
    def __init__(self, detector_path, level_path, head_path, registry, device="cpu", threads=None):
        from ultralytics import YOLO
        if threads:
            torch.set_num_threads(threads)
        self.dev = device
        self.det = YOLO(str(detector_path))
        self.model = build_model(len(LEVEL_ORDER), registry["level_model"].get("arch", "resnet18")).to(device)
        self.model.load_state_dict(torch.load(level_path, map_location=device)); self.model.eval()
        self.fc = self.model.fc; self.model.fc = nn.Identity()
        self.head = RunLabeller(512, len(LEVEL_ORDER)).to(device)
        self.head.load_state_dict(torch.load(head_path, map_location=device)); self.head.eval()
        self.tgt_px = float(registry.get("tgt_px", 96)); self.size = int(registry.get("size", 320)); self.rung = int(registry["level_model"].get("rung", 1))

    @torch.inference_mode()
    def run(self, gray_u8: np.ndarray, conf=0.35, imgsz=640):
        rgb = np.repeat(gray_u8[..., None], 3, -1)
        res = self.det.predict(rgb, imgsz=imgsz, conf=conf, verbose=False)[0]
        dets = []
        if res.keypoints is not None and len(res.boxes):
            kp = res.keypoints.xy.cpu().numpy(); kc = res.keypoints.conf.cpu().numpy() if res.keypoints.conf is not None else np.ones(kp.shape[:2])
            cf = res.boxes.conf.cpu().numpy()
            for i in np.argsort(kp[:, :, 1].mean(1)):
                pts = kp[i]
                b = [float(pts[:, 0].min()), float(pts[:, 1].min()), float(pts[:, 0].max()), float(pts[:, 1].max())]
                if b[2] - b[0] < 4 or b[3] - b[1] < 4:
                    continue
                dets.append({"conf": float(cf[i]), "x0": b[0], "y0": b[1], "x1": b[2], "y1": b[3],
                             "kpts": [{"name": n, "x": float(pts[k, 0]), "y": float(pts[k, 1]), "v": float(kc[i][k])} for k, n in enumerate(("sup_ant", "sup_post", "inf_ant", "inf_post"))]})
        if not dets:
            return {"dets": [], "levels": [], "run": []}
        boxes = [[int(d["x0"]), int(d["y0"]), int(d["x1"]), int(d["y1"])] for d in dets]
        X = torch.from_numpy(crops_for_run(gray01(gray_u8), boxes, self.tgt_px, self.size, self.rung)).float().to(self.dev)
        emb = self.model(X); p1 = torch.softmax(self.fc(emb), 1).cpu().numpy(); pr = torch.softmax(self.head(emb.unsqueeze(0))[0], 1).cpu().numpy()
        run = contiguous_run(pr)
        for i, d in enumerate(dets):
            d["level"] = LEVEL_ORDER[int(pr[i].argmax())]; d["level_conf"] = float(pr[i].max())
            d["level_single"] = LEVEL_ORDER[int(p1[i].argmax())]; d["level_single_conf"] = float(p1[i].max())
            d["level_run"] = run[i]
            d["top3"] = [(LEVEL_ORDER[int(j)], float(pr[i][j])) for j in np.argsort(-pr[i])[:3]]
        return {"dets": dets, "levels": [d["level"] for d in dets], "run": run}
