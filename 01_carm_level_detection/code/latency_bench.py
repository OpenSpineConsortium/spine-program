# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/latency_bench.py [tracked at 097933a]
"""Inference cost of every piece of the level pipeline, measured on the machine it runs on:
the vertebra detector (YOLO11 pose at 1024 px), the single-vertebra level model (ResNet-18,
two channels, 320 px), and the recurrent head (BiGRU over a run of 9). Batch 1 and batch 16,
on the GPU present and on the CPU at 1, 4 and 8 threads, median of repeated runs after warm-up,
plus parameter counts and multiply-accumulates counted with forward hooks. Jetson numbers are
not measured here; the MAC counts are what a Jetson estimate has to be built from.

    python tools/latency_bench.py --model ~/films_ann_fov96_ctx/runs/model_rung_0.pt \
        --weights ~/spine-detector/runs/pose/runs/pose/runs/detect_v3/weights/best.pt --out ~/bench/latency.json
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_context_crops import LEVEL_ORDER  # noqa: E402
from recurrent_order import RunLabeller  # noqa: E402
from train_level_classifier import build_model  # noqa: E402


def macs_of(model, x):
    total = [0]

    def hook(m, i, o):
        if isinstance(m, nn.Conv2d):
            k = m.kernel_size[0] * m.kernel_size[1] * (m.in_channels // m.groups)
            total[0] += k * o.numel() // o.shape[0] * o.shape[0] if o.dim() == 4 else 0
        elif isinstance(m, nn.Linear):
            total[0] += m.in_features * o.numel()
        elif isinstance(m, nn.GRU):
            L = i[0].shape[1] if i[0].dim() == 3 else 1
            total[0] += 3 * (m.input_size + m.hidden_size) * m.hidden_size * L * m.num_layers * (2 if m.bidirectional else 1)
    hs = [m.register_forward_hook(hook) for m in model.modules() if isinstance(m, (nn.Conv2d, nn.Linear, nn.GRU))]
    with torch.no_grad():
        model(x)
    for h in hs:
        h.remove()
    return int(total[0]) // x.shape[0]


def timeit(fn, n=50, warm=10):
    for _ in range(warm):
        fn()
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    ts = []
    for _ in range(n):
        t0 = time.perf_counter(); fn()
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        ts.append(time.perf_counter() - t0)
    return {"median_ms": 1000 * float(np.median(ts)), "p90_ms": 1000 * float(np.percentile(ts, 90))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--weights", default=None, help="YOLO pose detector .pt (optional)")
    ap.add_argument("--arch", default="resnet18")
    ap.add_argument("--size", type=int, default=320)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res = {"host": platform.node(), "cpu": platform.processor(), "torch": torch.__version__,
           "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None, "level_model": a.model, "detector": a.weights}
    C = len(LEVEL_ORDER)
    level = build_model(C, a.arch); level.load_state_dict(torch.load(a.model, map_location="cpu")); level.eval()
    gru = RunLabeller(512, C).eval()
    res["params"] = {"level_model": sum(p.numel() for p in level.parameters()), "recurrent_head": sum(p.numel() for p in gru.parameters())}
    x1 = torch.rand(1, 2, a.size, a.size)
    res["macs"] = {"level_model_per_crop": macs_of(level, x1), "recurrent_head_per_run_of_9": macs_of(gru, torch.rand(1, 9, 512))}
    devs = [("cuda", None)] if torch.cuda.is_available() else []
    devs += [("cpu", 1), ("cpu", 4), ("cpu", 8)]
    res["latency"] = {}
    for dev, th in devs:
        if th:
            torch.set_num_threads(th)
        key = dev if th is None else f"cpu_{th}thr"
        lm = level.to(dev); g = gru.to(dev)
        r = {}
        for bs in (1, 16):
            xb = torch.rand(bs, 2, a.size, a.size, device=dev)
            with torch.no_grad():
                r[f"level_model_bs{bs}"] = timeit(lambda: lm(xb), n=30 if dev == "cpu" else 100)
        e = torch.rand(1, 9, 512, device=dev)
        with torch.no_grad():
            r["recurrent_head_run9"] = timeit(lambda: g(e))
        if dev == "cuda":
            with torch.no_grad(), torch.autocast("cuda", dtype=torch.float16):
                r["level_model_bs1_fp16"] = timeit(lambda: lm(xb[:1]), n=100)
                r["level_model_bs16_fp16"] = timeit(lambda: lm(xb), n=100)
        res["latency"][key] = r
        print(key, json.dumps(r), flush=True)
    if a.weights:
        try:
            from ultralytics import YOLO
            det = YOLO(a.weights)
            img = (np.random.rand(1024, 1024, 3) * 255).astype(np.uint8)
            for dev in (["cuda"] if torch.cuda.is_available() else []) + ["cpu"]:
                t = timeit(lambda: det.predict(img, imgsz=1024, device=0 if dev == "cuda" else "cpu", verbose=False), n=20, warm=5)
                res["latency"].setdefault(dev if dev == "cuda" else "cpu_8thr", {})["detector_1024"] = t
                print("detector", dev, t, flush=True)
            try:
                res["detector_info"] = str(det.info(verbose=False))
            except Exception:  # noqa: BLE001
                pass
        except Exception as e:  # noqa: BLE001
            res["detector_error"] = repr(e)[:200]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "latency"}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
