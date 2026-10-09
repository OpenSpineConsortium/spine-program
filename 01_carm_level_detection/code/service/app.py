# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): service/app.py [tracked at 097933a]
"""Level-identification service: the weights stay on the server; the website sends an image and gets back
boxes, corner landmarks and level names.

Weights are pulled at start-up from a PRIVATE Hugging Face model repo with a read token in the environment
(HF_TOKEN, WEIGHTS_REPO); nothing under /static or in any response contains model parameters. Runs on CPU by
default (torch threads = CPU count); a GPU is used when present. Same container runs on a Hugging Face Docker
Space, Modal, Fly.io, an EC2 box or a workstation behind a tunnel.

    POST /infer   multipart 'image' (PNG/JPEG, any size), optional form fields conf (0.35), imgsz (640)
    GET  /health  {status, model registry, device}
"""
from __future__ import annotations

import io
import json
import os
import time
from pathlib import Path

import numpy as np
import torch
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from model_defs import LevelPipeline

WEIGHTS_REPO = os.environ.get("WEIGHTS_REPO", "gregoryschwingmdphd/level-id-weights")
ALLOWED = [o.strip() for o in os.environ.get("ALLOWED_ORIGINS", "https://openspineconsortium.org,https://www.openspineconsortium.org,https://openspineconsortium.github.io,http://localhost:8000,http://127.0.0.1:8000").split(",")]
MAX_PIXELS = 4096 * 4096

app = FastAPI(title="OpenSpine level identification", docs_url=None, redoc_url=None)
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED, allow_methods=["POST", "GET"], allow_headers=["*"])
STATE = {"pipe": None, "registry": None, "device": None, "loaded_at": None}


def load():
    from huggingface_hub import snapshot_download
    tok = os.environ.get("HF_TOKEN")
    d = Path(snapshot_download(WEIGHTS_REPO, token=tok, allow_patterns=["*.pt", "registry.json"], local_dir=os.environ.get("WEIGHTS_DIR", "/tmp/weights")))
    reg = json.load(open(d / "registry.json"))
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = LevelPipeline(d / reg["detector"]["file"], d / reg["level_model"]["file"], d / reg["recurrent_head"]["file"], reg, device=dev, threads=os.cpu_count())
    # warm-up: first call compiles kernels and allocates; keep it off the first user's clock
    pipe.run(np.full((640, 480), 114, np.uint8))
    STATE.update(pipe=pipe, registry={k: {kk: vv for kk, vv in v.items() if kk != "file"} if isinstance(v, dict) else v for k, v in reg.items()}, device=dev, loaded_at=time.time())


@app.on_event("startup")
def _startup():
    load()


@app.get("/health")
def health():
    return {"status": "ok" if STATE["pipe"] else "loading", "device": STATE["device"], "registry": STATE["registry"], "torch": torch.__version__, "threads": torch.get_num_threads()}


@app.post("/infer")
async def infer(image: UploadFile = File(...), conf: float = Form(0.35), imgsz: int = Form(640)):
    t0 = time.time()
    raw = await image.read()
    im = Image.open(io.BytesIO(raw)); im.draft("L", (2048, 2048)); im = im.convert("L")
    if im.size[0] * im.size[1] > MAX_PIXELS:
        s = (MAX_PIXELS / (im.size[0] * im.size[1])) ** 0.5; im = im.resize((int(im.size[0] * s), int(im.size[1] * s)))
    arr = np.asarray(im, np.uint8)
    out = STATE["pipe"].run(arr, conf=float(conf), imgsz=int(max(320, min(1280, imgsz))))
    out.update({"ms": round((time.time() - t0) * 1000, 1), "width": int(arr.shape[1]), "height": int(arr.shape[0]), "device": STATE["device"],
                "model": {"level_model": STATE["registry"]["level_model"].get("registry_id"), "release": STATE["registry"].get("release")}})
    return out
