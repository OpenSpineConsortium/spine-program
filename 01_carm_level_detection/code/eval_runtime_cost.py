# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/eval_runtime_cost.py [tracked at 097933a]
"""What the C-arm level pipeline COSTS to run once, on named hardware, stage by stage.

WHY THIS EXISTS. The manuscript's economic argument is about cost -- a new C-arm is meant to cost a parameter
fit rather than a labelled dataset -- and no cost is stated anywhere in it: a grep for speed, latency, runtime
or real-time over `paper/rsnai/main_v2.tex` and `paper/rsnai/main.tex` returns nothing. The earlier focused
paper at least disclaims it, at `paper/focused/main.tex` line 632 ("No speed claim is made here: end-to-end
latency on the hardware this would run on was not measured") and line 382. The only latency measurement on
disk (`tools/latency_bench.py`) is of a DIFFERENT detector (detect_v3) on a V100, times three network pieces
in isolation, and never composes them into the thing a surgeon waits for: a sweep of exposures turned into a
named chain. An operating room may also have no GPU at all, so a GPU-only figure answers the wrong question.

WHAT THE ANSWER IS COMPARED WITH. The same paragraph of `paper/focused/main.tex` carries the only numbers
that make a millisecond mean anything here: LevelCheck registration at 4.7 s per image on a 2012 graphics
card and 17-72 s per registration in an operating room, against three surgeons willing to wait 20 s to one
minute in all cases and over a minute in 60.6 % (305/503) of the ratings where they judged it helpful. The
protocol is three or four exposures for a lumbar target and six or seven for a mid-thoracic one, which is
where --sweep 3 7 comes from.

WHAT IT MEASURES. Every stage of the deployed path, each one by calling the SAME function the pipeline calls,
not a stand-in:

    detect      ultralytics YOLO forward at --imgsz on one frame            (tools/devcorpus_train.py's model)
    crop        fluorocap_infer.crops_for_run for this frame's boxes        (fixed-scale context crops)
    encode      the level encoder's forward over those crops                (ResNet-18, 2 channels, 320 px)
    head        the detached fc + recurrent_order.RunLabeller over the run  (BiGRU, 2-9 vertebrae)
    link        sweep_map.ncc_shift on one consecutive frame pair           (the windowed correlation)
    chain       sweep_map.build_chain bookkeeping, its links subtracted     (node merge and pooling)
    confirm     build_panorama + node_boxes_on_panorama + map_query_panorama (the instrument's exposure)

and then the end-to-end wall clock for a sweep of 3 and of 7 exposures, on the GPU when one is present and on
the CPU at several thread counts, with memory and with the spread over repeats rather than a single number.

THE GEOMETRY IS READ, NOT ASSUMED. A stage's cost depends on the frame, so the frame is the real one: all 296
C-ArmLSpine meta files record `size` 1024 and `px_mm` 0.1915, and the median spacing of their truth box
centres is 177.9 px. The default pitch here is derived independently, from `sweep_map.PITCH_MM["lumbar"]`
(34.0 mm) over that pixel size, which gives 177.5 px -- 0.2 % from the measured spacing. That agreement is
printed as a cross-check, because a linker timed at the wrong pitch is timed on the wrong search window and
the number would still look reasonable.

FIVE TRAPS THIS AVOIDS.

1. *A MAC count is not a latency.* `latency_bench.py` reports multiply-accumulates, which is the right thing
   to carry to unmeasured hardware and the wrong thing to quote as a speed. Everything here is a clock.

2. *An additive budget is not an end-to-end measurement.* Summing stage medians ignores data movement,
   allocator behaviour and the per-call overhead of six libraries. So both are computed and BOTH are
   reported, with their ratio: if the composed wall clock and the additive budget disagree, the stage
   decomposition is missing something and the JSON says so rather than hiding it.

3. *A pipeline is not its slowest network.* The linker's correlation is pure numpy over a window that grows
   with the frame, and the confirmation's template match is over the whole panorama. On real C-ArmLSpine
   geometry the linker is not a rounding error beside the networks; it is the pipeline. `map_query_panorama`
   already reduces its images to `sweep_map.WORK_PITCH` (40 px per body) before matching, and its docstring
   says why -- "the difference between seconds and a day per collection". `ncc_shift` does not. So the link
   is timed BOTH as implemented and under that same reduction, and the two are reported side by side: the
   cost and its measured remedy, rather than the cost alone.

4. *An end-to-end number that quietly omits the detector.* If ultralytics or the detector weights are absent
   the detector stage is recorded as `not_measured` with the reason, every end-to-end figure is renamed
   `end_to_end_excluding_detector`, and `detector_included: false` travels with each one. No stage is ever
   estimated, scaled from another machine, or filled in from a published throughput.

5. *A latency measured on a busy machine.* System CPU use and every other process above 20 % are sampled at
   the start and at the end and stored as `machine_load_at_start` / `machine_load_at_end`; when anything
   else was busy the tool says so in `caveats` and calls its own figures an upper bound. A reference
   measurement belongs in a SLURM job, not on a workstation that is running three other analyses.

`--redraw <result.json>` redraws the figure from a result this tool wrote, and measures nothing.

`--selftest` checks the fallback encoder against the published ResNet-18 arithmetic (1.814 GMAC at 224 px,
11,689,512 parameters) before any timing from it is believed, because the published arithmetic of an
architecture is the one check on an implementation that comes from outside the implementation.

    # everything this machine can do, with a figure
    python tools/eval_runtime_cost.py --out ~/bench/runtime_cost.json --fig ~/bench/fig_runtime

    # the full measurement, on the grid, with the paper's detector and level model
    python tools/eval_runtime_cost.py --out $OUT/runtime_cost.json --fig $OUT/fig_runtime \\
        --detector ~/spine-detector/runs/devcorpus/dc_A_held_surgio_b51_dr/weights/best.pt --imgsz 1024 \\
        --model ~/carm_cvmix0_fov96_ctx/runs/model_rung_1_ft_cv0_aug2.pt \\
        --head ~/model_night/heads_carm/head_cv0.pt --bodies 6 --repeats 30
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eval_gate as EG  # noqa: E402

# Published reference cost of the encoder architecture, used by --selftest as the one external check
# available on an implementation: torchvision's resnet18 at 224x224x3 is 1.814 GMAC and 11,689,512
# parameters (He et al. 2016; torchvision model summary). A local rewrite that misses this is not ResNet-18.
RESNET18_REF_GMAC_224 = 1.814
RESNET18_REF_PARAMS = 11_689_512

# Measured over all 296 /rs/rs_grp_oschome/go2432/data/realxray/carmlspine/meta/*.json on the grid,
# 2026-09-22: size 1024 in 296 of 296; px_mm 0.1915 (median); median spacing of truth box centres 177.9 px;
# 6.10 truth boxes per frame; 4.17 vertebrae per LATERAL WHOLE FRAME carry an agreed level
# (docs/carmlspine_cv5_mixed_2026-09-21.json det/LAT/kfull: 617 vertebrae over 148 frames).
CARM_FRAME_PX = 1024
CARM_PX_MM = 0.1915
CARM_MEASURED_PITCH_PX = 177.9
CARM_MEASURED_PITCH_SOURCE = ("median spacing of truth box centres over all 296 "
                              "realxray/carmlspine/meta/*.json, read on the grid 2026-09-22")

DEFAULT_BODIES_FILE = "docs/carmlspine_cv5_mixed_2026-09-21.json"


# ------------------------------------------------------------------------------------------- housekeeping

def code_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                       cwd=str(Path(__file__).resolve().parents[1]),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:  # noqa: BLE001
        return None


def cpu_model_name():
    """The CPU's marketing name, which platform.processor() does not give on Linux."""
    try:
        if sys.platform.startswith("linux"):
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
        elif sys.platform == "win32":
            v = os.environ.get("PROCESSOR_IDENTIFIER")
            if v:
                return v.strip()
    except Exception:  # noqa: BLE001
        pass
    return platform.processor() or platform.machine()


def hardware(torch_mod):
    """Everything a reader needs to know before believing a millisecond."""
    hw = {"host": platform.node(), "platform": platform.platform(), "python": platform.python_version(),
          "cpu_model": cpu_model_name(), "cpu_logical": os.cpu_count(), "numpy": np.__version__}
    try:
        import psutil
        hw["cpu_physical"] = psutil.cpu_count(logical=False)
        hw["ram_total_gb"] = round(psutil.virtual_memory().total / 1e9, 1)
    except Exception:  # noqa: BLE001
        hw["cpu_physical"] = hw["ram_total_gb"] = None
    if torch_mod is not None:
        hw["torch"] = torch_mod.__version__
        hw["torch_default_threads"] = torch_mod.get_num_threads()
        if torch_mod.cuda.is_available():
            hw["gpu"] = torch_mod.cuda.get_device_name(0)
            hw["gpu_memory_gb"] = round(torch_mod.cuda.get_device_properties(0).total_memory / 1e9, 1)
            hw["cuda"] = torch_mod.version.cuda
        else:
            hw["gpu"] = None
    try:
        import cv2
        hw["opencv"] = cv2.__version__
        hw["opencv_threads"] = cv2.getNumThreads()
    except Exception:  # noqa: BLE001
        hw["opencv"] = None
    try:
        import ultralytics
        hw["ultralytics"] = ultralytics.__version__
    except Exception:  # noqa: BLE001
        hw["ultralytics"] = None
    for k in ("SLURM_JOB_ID", "SLURM_JOB_PARTITION", "SLURM_CPUS_ON_NODE", "SLURM_JOB_GPUS", "CUDA_VISIBLE_DEVICES"):
        if os.environ.get(k):
            hw[k.lower()] = os.environ[k]
    return hw


def machine_load(seconds=1.0):
    """How busy the machine is APART from this process, and which other processes are busy.

    A latency measured while three other jobs are saturating the cores is not the latency of this
    pipeline, and nothing else in the output would say so. This is sampled at the start and at the end of
    the run and stored, so a contaminated measurement identifies itself instead of being quoted.
    """
    try:
        import psutil
        me = os.getpid()
        procs = list(psutil.process_iter(["pid", "name"]))
        for pr in procs:                      # psutil needs a first call to start each counter;
            try:                              # without it every per-process figure comes back 0.0
                pr.cpu_percent(None)
            except Exception:  # noqa: BLE001
                continue
        total = psutil.cpu_percent(interval=seconds)
        busy = []
        for pr in procs:
            try:
                v = pr.cpu_percent(None)
                if pr.pid not in (me, 0) and v >= 20.0 and "idle" not in pr.name().lower():
                    busy.append({"pid": pr.pid, "name": pr.name(), "cpu_percent": round(v, 1)})
            except Exception:  # noqa: BLE001
                continue
        busy.sort(key=lambda d: -d["cpu_percent"])
        return {"system_cpu_percent": total, "other_busy_processes": busy[:8],
                "loadavg": [round(v, 2) for v in os.getloadavg()] if hasattr(os, "getloadavg") else None}
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}"}


def peak_rss_mb():
    """Peak resident set of THIS process, MB. A high-water mark, cumulative and monotone -- not a per-stage
    working set, and reported as such."""
    try:
        import psutil
        mi = psutil.Process().memory_info()
        for attr in ("peak_wset", "peak_pagefile"):        # Windows
            if hasattr(mi, attr):
                return round(getattr(mi, attr) / 1e6, 1)
        import resource                                     # POSIX
        return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e3, 1)
    except Exception:  # noqa: BLE001
        try:
            import psutil
            return round(psutil.Process().memory_info().rss / 1e6, 1)
        except Exception:  # noqa: BLE001
            return None


def stats(ts, extra=None):
    """Median and the SPREAD. A latency quoted as one number is a latency measured once."""
    a = np.asarray(ts, float) * 1000.0
    out = {"n": int(a.size),
           "median_ms": round(float(np.median(a)), 3),
           "mean_ms": round(float(a.mean()), 3),
           "sd_ms": round(float(a.std(ddof=1)) if a.size > 1 else 0.0, 3),
           "min_ms": round(float(a.min()), 3),
           "max_ms": round(float(a.max()), 3),
           "p05_ms": round(float(np.percentile(a, 5)), 3),
           "p95_ms": round(float(np.percentile(a, 95)), 3),
           "iqr_ms": round(float(np.percentile(a, 75) - np.percentile(a, 25)), 3)}
    out["rel_sd"] = round(out["sd_ms"] / out["median_ms"], 4) if out["median_ms"] > 0 else None
    if extra:
        out.update(extra)
    return out


def timeit(fn, repeats, warmup, sync=None):
    for _ in range(warmup):
        fn()
    if sync:
        sync()
    ts = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        if sync:
            sync()
        ts.append(time.perf_counter() - t0)
    return ts


# ------------------------------------------------------------------------------------------- the encoder

def macs_of(model, x, torch_mod):
    """Multiply-accumulates of one forward, per sample, by forward hook. Carried so hardware this was never
    run on can be reasoned about; it is NOT quoted as a speed."""
    import torch.nn as nn
    total = [0]

    def hook(m, i, o):
        if isinstance(m, nn.Conv2d):
            k = m.kernel_size[0] * m.kernel_size[1] * (m.in_channels // m.groups)
            total[0] += k * int(o.numel())
        elif isinstance(m, nn.Linear):
            total[0] += m.in_features * int(o.numel())
        elif isinstance(m, nn.GRU):
            L = i[0].shape[1] if i[0].dim() == 3 else 1
            total[0] += (3 * (m.input_size + m.hidden_size) * m.hidden_size * L
                         * m.num_layers * (2 if m.bidirectional else 1))

    hs = [m.register_forward_hook(hook) for m in model.modules()
          if isinstance(m, (nn.Conv2d, nn.Linear, nn.GRU))]
    with torch_mod.no_grad():
        model(x)
    for h in hs:
        h.remove()
    return int(total[0]) // int(x.shape[0])


def _local_resnet18(in_ch, n_classes):
    """torchvision's resnet18, written out, for a machine with torch and no torchvision.

    Used ONLY when torchvision is missing, labelled as such in the output, and checked by --selftest against
    the published 1.814 GMAC / 11,689,512 parameters at 224 px before any number from it is believed. A
    latency depends on the SHAPES, not on the values of the weights, so a randomly initialised network of the
    right architecture times correctly -- but only if it is the right architecture, which is what the
    self-test is for.
    """
    import torch.nn as nn

    def conv3(i, o, s=1):
        return nn.Conv2d(i, o, 3, s, 1, bias=False)

    class Basic(nn.Module):
        def __init__(self, i, o, s=1, down=None):
            super().__init__()
            self.conv1, self.bn1 = conv3(i, o, s), nn.BatchNorm2d(o)
            self.conv2, self.bn2 = conv3(o, o), nn.BatchNorm2d(o)
            self.relu, self.down = nn.ReLU(inplace=True), down

        def forward(self, x):
            idt = x if self.down is None else self.down(x)
            y = self.relu(self.bn1(self.conv1(x)))
            return self.relu(self.bn2(self.conv2(y)) + idt)

    class ResNet18(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(in_ch, 64, 7, 2, 3, bias=False)
            self.bn1, self.relu = nn.BatchNorm2d(64), nn.ReLU(inplace=True)
            self.maxpool = nn.MaxPool2d(3, 2, 1)
            self.inp = 64
            self.layer1, self.layer2 = self._make(64, 1), self._make(128, 2)
            self.layer3, self.layer4 = self._make(256, 2), self._make(512, 2)
            self.avgpool, self.fc = nn.AdaptiveAvgPool2d(1), nn.Linear(512, n_classes)

        def _make(self, o, s):
            down = None
            if s != 1 or self.inp != o:
                down = nn.Sequential(nn.Conv2d(self.inp, o, 1, s, bias=False), nn.BatchNorm2d(o))
            blocks = [Basic(self.inp, o, s, down), Basic(o, o)]
            self.inp = o
            return nn.Sequential(*blocks)

        def forward(self, x):
            x = self.maxpool(self.relu(self.bn1(self.conv1(x))))
            x = self.layer4(self.layer3(self.layer2(self.layer1(x))))
            return self.fc(self.avgpool(x).flatten(1))

    return ResNet18()


def build_encoder(n_classes, arch, in_ch, weights, torch_mod):
    """The level encoder, preferring the project's own constructor. -> (module, source, note, weights_loaded)."""
    try:
        from train_level_classifier import build_model
        m = build_model(n_classes, arch)
        src, note = "tools/train_level_classifier.build_model (torchvision)", None
    except Exception as e:  # noqa: BLE001  -- torchvision absent on this machine
        if arch != "resnet18":
            raise SystemExit(f"--arch {arch} needs torchvision, not importable here: {e!r}")
        m = _local_resnet18(in_ch, n_classes)
        src = "tools/eval_runtime_cost._local_resnet18 (torchvision not importable)"
        note = (f"torchvision not importable ({type(e).__name__}); the architecture is written out locally "
                f"and checked against the published ResNet-18 cost by --selftest")
    loaded = False
    if weights:
        try:
            sd = torch_mod.load(weights, map_location="cpu")
            if isinstance(sd, dict) and "state_dict" in sd:
                sd = sd["state_dict"]
            m.load_state_dict(sd)
            loaded = True
        except Exception as e:  # noqa: BLE001
            note = ((note + "; " if note else "")
                    + f"weights not loaded ({type(e).__name__}); shapes unchanged so the timing is unaffected")
    m.eval()
    return m, src, note, loaded


def selftest(torch_mod, verbose=True):
    """Check the fallback encoder against the published ResNet-18 arithmetic."""
    m = _local_resnet18(3, 1000).eval()
    params = sum(p.numel() for p in m.parameters())
    gmac = macs_of(m, torch_mod.rand(1, 3, 224, 224), torch_mod) / 1e9
    ok_p = params == RESNET18_REF_PARAMS
    ok_m = abs(gmac - RESNET18_REF_GMAC_224) / RESNET18_REF_GMAC_224 < 0.01
    if verbose:
        print(f"selftest local resnet18: params {params:,} (published {RESNET18_REF_PARAMS:,}) "
              f"{'OK' if ok_p else 'MISMATCH'}")
        print(f"selftest local resnet18: {gmac:.3f} GMAC at 224x224x3 (published {RESNET18_REF_GMAC_224}) "
              f"{'OK' if ok_m else 'MISMATCH'}")
    return bool(ok_p and ok_m), {"params": int(params), "gmac_224": round(float(gmac), 4),
                                 "params_published": RESNET18_REF_PARAMS,
                                 "gmac_224_published": RESNET18_REF_GMAC_224,
                                 "pass": bool(ok_p and ok_m)}


# ------------------------------------------------------------------------------------------- the frames

def bodies_per_frame(repo_root, path):
    """Vertebrae per whole lateral exposure, READ FROM THE SCORED RESULT rather than assumed.

    docs/carmlspine_cv5_mixed_2026-09-21.json det/LAT/kfull carries `vertebrae` and `frames` for the
    five-fold cross-validation the manuscript quotes. Their ratio is how many bodies the crop, encode and
    head stages run on per exposure. Returned with the file it came from. NOTE that this counts the
    vertebrae with an AGREED level; the truth carries 6.10 boxes per frame, so a run that wants the
    detector's own load should pass --bodies 6.

    THE KEY IS FLAT. That file is keyed "det/LAT/kfull" as ONE string, not nested det -> LAT -> kfull.
    Walking it as a nested dict returns nothing, the caller falls back to its hard-coded 4, and because
    617/148 = 4.17 rounds to exactly that 4 the substitution is invisible in every output -- the project's
    own recurring failure mode. Both spellings are tried, and the JSON records which one answered.
    """
    p = Path(path) if Path(path).is_absolute() else repo_root / path
    if not p.exists():
        return None, {"source": "file not found", "file": str(p)}
    d = json.load(open(p))
    node, key = d.get("det/LAT/kfull"), "det/LAT/kfull (flat key)"
    if not isinstance(node, dict):                       # older nested spelling
        node, key = d.get("det", {}).get("LAT", {}).get("kfull", {}), "det -> LAT -> kfull (nested)"
    v, f = (node or {}).get("vertebrae"), (node or {}).get("frames")
    if not v or not f:
        return None, {"source": "vertebrae/frames absent under 'det/LAT/kfull' in either the flat or the "
                                "nested spelling", "file": str(p), "keys_seen": sorted(d)[:8]}
    return v / f, {"source": f"{key} vertebrae/frames (levels both segmentation tools agree on)",
                   "file": str(p), "vertebrae": int(v), "frames": int(f), "mean": round(v / f, 3)}


def _station(img, boxes, d_in, n_classes, rng):
    """Everything sweep_map's linker, chain builder and panorama need of one exposure."""
    n = len(boxes)
    return {"img": img, "boxes": boxes, "gt_idx": list(range(n)), "all_boxes": list(boxes),
            "all_idx": list(range(n)), "y0": 0, "y1": img.shape[0], "x0": 0, "x1": img.shape[1],
            "perturb": {}, "mask": None,
            "spine_cx": float(np.median([(b[0] + b[2]) / 2.0 for b in boxes])) if boxes else None,
            "emb": rng.normal(0, 1, (n, d_in)).astype(np.float32),
            "p_single": np.full((n, n_classes), 1.0 / n_classes, np.float32),
            "p_blend": np.full((n, n_classes), 1.0 / n_classes, np.float32),
            "gt": [None] * n}


def synth_stations(n_frames, h, w, bodies, pitch, d_in, n_classes, rng):
    """Exposures of the real size holding the real number of bodies at the real pitch.

    The content is noise plus a periodic column of bright blocks, because what a stage costs is set by the
    SHAPE of its work -- the correlation grid is (dy x dx) fixed by pitch and frame size, the crops are fixed
    by the box count and the canvas, the template match is over the panorama -- and not by what the bone
    looks like. `--frames` times the same stages on real device frames, and the JSON records which was used.
    """
    out = []
    for _ in range(n_frames):
        img = rng.normal(110, 22, (h, w)).astype(np.float32)
        boxes = []
        for k in range(bodies):
            cy = int((k + 0.5) * pitch)
            y0, y1 = max(0, cy - int(0.35 * pitch)), min(h - 1, cy + int(0.35 * pitch))
            x0, x1 = max(0, w // 2 - int(0.28 * pitch)), min(w - 1, w // 2 + int(0.28 * pitch))
            if y1 - y0 < 4:
                continue
            img[y0:y1, x0:x1] += 60.0
            boxes.append([x0, y0, x1, y1])
        out.append(_station(np.clip(img, 0, 255).astype(np.uint8), boxes, d_in, n_classes, rng))
    return out


def real_stations(frames_dir, n, bodies, pitch, d_in, n_classes, rng):
    """Exposures cut from real device frames on disk (realxray layout: images/<split>/<stem>.png with
    labels/<split>/<stem>.txt). Boxes come from the label file when there is one.

    WHAT THIS IS AND IS NOT. The first n PNGs in path order are taken. That gives real frames of the real
    size holding real boxes, which is all a TIMING needs -- the correlation grid, the crop canvas and the
    template are set by shape, not by content. It does NOT give a sweep: consecutive frames here are
    different cases (C-ArmLSpine ships one AP and one lateral per case, and only two raw sweeps in the
    whole release), so there is no true translation between station k and station k+1. Any shift the linker
    returns on such a pair is arbitrary, and `geometry.reduced.same_answer_check` is therefore NOT
    meaningful under --frames either: it needs two overlapping exposures of one spine. Until it is pointed
    at a real sweep, that check can refute the reduction (a disagreement is real) but cannot support it.
    """
    from PIL import Image
    d = Path(frames_dir)
    imgs = sorted(p for p in d.rglob("*.png"))[:n]
    if len(imgs) < n:
        raise SystemExit(f"--frames {frames_dir}: found {len(imgs)} PNGs, need {n}")
    out, used_labels = [], 0
    for p in imgs:
        a = np.asarray(Image.open(p).convert("L"), np.uint8)
        h, w = a.shape
        lp = Path(str(p).replace(os.sep + "images" + os.sep, os.sep + "labels" + os.sep)
                  .replace("/images/", "/labels/")).with_suffix(".txt")
        boxes = []
        if lp.exists():
            for line in lp.read_text().split("\n"):
                f = line.split()
                if len(f) >= 5:
                    cx, cy, bw, bh = (float(x) for x in f[1:5])
                    boxes.append([int((cx - bw / 2) * w), int((cy - bh / 2) * h),
                                  int((cx + bw / 2) * w), int((cy + bh / 2) * h)])
            boxes.sort(key=lambda b: (b[1] + b[3]) / 2.0)
            if boxes:
                used_labels += 1
        if not boxes:
            for k in range(bodies):
                cy = int((k + 0.5) * pitch)
                boxes.append([w // 2 - int(0.28 * pitch), max(0, cy - int(0.35 * pitch)),
                              w // 2 + int(0.28 * pitch), min(h - 1, cy + int(0.35 * pitch))])
        out.append(_station(a, boxes, d_in, n_classes, rng))
    return out, {"kind": "real frames on disk", "dir": str(d),
                 "files": [str(p) for p in imgs], "frames_with_a_label_file": used_labels}


def reduce_stations(stations, pitch, work_pitch, d_in, n_classes, rng):
    """The same exposures at the working resolution `map_query_panorama` already uses (WORK_PITCH px per
    vertebral body), so the linker's cost can be reported beside its remedy."""
    import cv2
    red = min(1.0, work_pitch / max(4.0, pitch))
    if red >= 1.0:
        return stations, 1.0
    out = []
    for st in stations:
        h, w = st["img"].shape
        a = cv2.resize(st["img"], (max(8, int(w * red)), max(8, int(h * red))), interpolation=cv2.INTER_AREA)
        bx = [[int(v * red) for v in b] for b in st["boxes"]]
        out.append(_station(a, bx, d_in, n_classes, rng))
    return out, red


# ------------------------------------------------------------------------------------------- the stages

def measure_networks(dev, enc, head_mod, fc, size, in_ch, n_classes, tta, repeats, warmup, torch_mod,
                     img_u8, boxes):
    """crop, encode, head -- on one device, for one exposure's worth of bodies."""
    import fluorocap_infer as v1
    sync = (lambda: torch_mod.cuda.synchronize()) if dev == "cuda" else None
    nv = 2 if tta else 1
    res = {}

    def normalise():
        arr = img_u8.astype(np.float32)
        lo, hi = np.percentile(arr, 0.5), np.percentile(arr, 99.5)
        return np.clip((arr - lo) / max(hi - lo, 1e-6), 0, 1)

    def do_crop():
        # the percentile windowing is inside the timing because it is inside the pipeline: it runs once per
        # exposure over the whole frame, and leaving it out was worth about 20 % of a short sweep when the
        # additive budget was checked against the composed wall clock
        im = normalise()
        for _ in range(nv):
            v1.crops_for_run(im, boxes, 96.0, size, 1)

    res["crop"] = stats(timeit(do_crop, repeats, warmup),
                        {"what": f"percentile windowing of the whole frame + fluorocap_infer.crops_for_run, "
                                 f"{len(boxes)} boxes x {nv} TTA variant(s), one exposure"})
    img0 = normalise()

    X = torch_mod.from_numpy(v1.crops_for_run(img0, boxes, 96.0, size, 1)).float().to(dev)

    def do_encode():
        with torch_mod.no_grad():
            for _ in range(nv):
                enc(X)

    res["encode"] = stats(timeit(do_encode, repeats, warmup, sync),
                          {"what": f"encoder forward over {len(boxes)} crops of {in_ch}x{size}x{size} "
                                   f"x {nv} TTA variant(s), one exposure"})

    with torch_mod.no_grad():
        emb = enc(X)

    def do_head():
        with torch_mod.no_grad():
            for _ in range(nv):
                p1 = torch_mod.softmax(fc(emb), 1)
                ph = torch_mod.softmax(head_mod(emb.unsqueeze(0))[0], 1)
                _ = (p1 + ph) / 2.0

    res["head"] = stats(timeit(do_head, repeats, warmup, sync),
                        {"what": f"detached fc ({emb.shape[1]}->{n_classes}) + RunLabeller BiGRU over a run "
                                 f"of {len(boxes)} x {nv} TTA variant(s), one exposure"})
    return res


def chain_with_known_links(SM, stations, pitch_px, prior_dy, links):
    """build_chain's node bookkeeping, replayed against links that are already known.

    WHY THIS EXISTS. `build_chain` calls `link_pair` once per consecutive pair, and at full resolution one
    link costs minutes, so building a chain purely to set up the confirmation measurement would cost
    (n-1) x link and measure nothing new. The links from the reduced-resolution pass are the SAME links
    (the shift is the same translation expressed in different pixels), so they are scaled and replayed:
    `link_pair` is swapped for a function that hands back the known result, `build_chain` runs its own
    bookkeeping unchanged, and the original function is put back. Nothing about the chain's structure is
    reimplemented here, which is the point.
    """
    it = iter(links)
    orig = SM.link_pair
    try:
        SM.link_pair = lambda *args, **kw: next(it)
        return SM.build_chain(stations, pitch_px, prior_dy)
    finally:
        SM.link_pair = orig


def scale_links(links, factor):
    """The same links with their shifts expressed in another pixel size."""
    out = []
    for lk in links:
        d = dict(lk)
        sh = d.get("shift")
        if sh:
            d["shift"] = {**sh, "dy": int(round(sh["dy"] * factor)), "dx": int(round(sh["dx"] * factor))}
        out.append(d)
    return out


def measure_geometry(stations, pitch_px, prior_dy, repeats, tag, do_chain=True, known_links=None):
    """link, chain, confirm. Pure numpy / OpenCV: these do not move to a GPU, so they are measured once.

    `do_chain=False` skips timing `build_chain`, which contains one link per pair and would therefore cost
    (n-1) x link. The chain's own work -- pairing indices, prepending nodes, averaging embeddings and
    posteriors -- is index bookkeeping over a handful of nodes and does not depend on the image size, so at
    full resolution it is taken from the reduced measurement and labelled as such.
    """
    import sweep_map as SM
    res = {}
    lo, up = stations[0], stations[1]

    keep = {}

    def one_link():
        # the ANSWER is kept beside the cost, so "the reduction is free" can be checked rather than
        # asserted: the two resolutions must return the same translation once dy is divided by the scale.
        # It is captured from a TIMED call, so no extra full-resolution correlation is paid for.
        keep["shift"] = SM.ncc_shift(lo, up, prior_dy, pitch_px)

    res["link"] = stats(timeit(one_link, repeats, 0),
                        {"what": f"sweep_map.ncc_shift on one consecutive pair, {tag} "
                                 f"(windowed normalised cross-correlation; no warm-up, numpy has none)",
                         "frame_px": [int(lo["img"].shape[0]), int(lo["img"].shape[1])],
                         "pitch_px": round(float(pitch_px), 2),
                         "shift": keep.get("shift")})

    n_links = len(stations) - 1
    if do_chain:
        chain_total = stats(timeit(lambda: SM.build_chain(stations, pitch_px, prior_dy), max(2, repeats // 2), 0),
                            {"what": f"sweep_map.build_chain over {len(stations)} stations, {tag} "
                                     f"(includes its {n_links} links)"})
        res["chain_total"] = chain_total
        raw = chain_total["median_ms"] - n_links * res["link"]["median_ms"]
        res["chain"] = {"median_ms": round(max(raw, 0.0), 3), "raw_difference_ms": round(raw, 3),
                        "n": chain_total["n"],
                        "what": f"build_chain minus its {n_links} links: node bookkeeping and pooling only",
                        "derivation": "chain_total.median_ms - n_links * link.median_ms"}
        if raw < 0:
            res["chain"]["note"] = ("the difference came out negative, which means the chain's own work is "
                                    "below the run-to-run spread of its links at this repeat count: it is "
                                    "reported as 0 and it is not a measurable share of the sweep")

    if known_links is not None:
        chain, links = chain_with_known_links(SM, stations, pitch_px, prior_dy, known_links)
    else:
        chain, links = SM.build_chain(stations, pitch_px, prior_dy)
    pano, _, pano_boxes = SM.build_panorama(stations, links, prior_dy)
    mid = stations[len(stations) // 2]
    q = {"img": mid["img"], "boxes": mid["boxes"]}

    def do_confirm():
        p, _, pb = SM.build_panorama(stations, links, prior_dy)
        nb = SM.node_boxes_on_panorama(chain, pb)
        SM.map_query_panorama(q, p, nb, pitch_px)

    res["confirm"] = stats(timeit(do_confirm, max(2, repeats), 0),
                           {"what": "build_panorama + node_boxes_on_panorama + map_query_panorama: the "
                                    "instrument's exposure matched onto the chain, " + tag,
                            "panorama_px": [int(pano.shape[0]), int(pano.shape[1])],
                            "chain_nodes": len(chain),
                            "note": f"map_query_panorama reduces internally to WORK_PITCH="
                                    f"{SM.WORK_PITCH} px per body before matching, so this stage is nearly "
                                    f"independent of the frame's resolution"})
    res["_links"] = links
    return res


def end_to_end(stations, pitch_px, prior_dy, dev, enc, head_mod, fc, size, tta, torch_mod,
               detector, imgsz, repeats):
    """The composed loop, timed as a whole, on the stations it is handed."""
    import fluorocap_infer as v1
    import sweep_map as SM
    sync = (lambda: torch_mod.cuda.synchronize()) if dev == "cuda" else None
    nv = 2 if tta else 1

    def once():
        for st in stations:
            if detector is not None:
                SM.detect_boxes(detector, st["img"], imgsz=imgsz, conf=0.25)
            arr = st["img"].astype(np.float32)
            lo, hi = np.percentile(arr, 0.5), np.percentile(arr, 99.5)
            img0 = np.clip((arr - lo) / max(hi - lo, 1e-6), 0, 1)
            embs, blends = [], []
            with torch_mod.no_grad():
                for vi in range(nv):
                    im, bx = img0, st["boxes"]
                    if vi == 1:
                        W = img0.shape[1]
                        im = img0[:, ::-1].copy()
                        bx = [[W - 1 - b[2], b[1], W - 1 - b[0], b[3]] for b in st["boxes"]]
                    X = torch_mod.from_numpy(v1.crops_for_run(im, bx, 96.0, size, 1)).float().to(dev)
                    e = enc(X)
                    p1 = torch_mod.softmax(fc(e), 1)
                    ph = torch_mod.softmax(head_mod(e.unsqueeze(0))[0], 1)
                    embs.append(e.cpu().numpy())
                    blends.append(((p1 + ph) / 2.0).cpu().numpy())
            st["emb"] = np.mean(embs, 0)
            st["p_single"] = st["p_blend"] = np.mean(blends, 0)
        chain, links = SM.build_chain(stations, pitch_px, prior_dy)
        pano, _, pano_boxes = SM.build_panorama(stations, links, prior_dy)
        nb = SM.node_boxes_on_panorama(chain, pano_boxes)
        mid = stations[len(stations) // 2]
        SM.map_query_panorama({"img": mid["img"], "boxes": mid["boxes"]}, pano, nb, pitch_px)

    return timeit(once, repeats, 1, sync)


def additive_budget(stages, n, link_key):
    """Stage medians times the number of times each runs in a sweep of n exposures.

    Returns the total, the parts, and the stages that were NOT available to it. A budget that quietly
    drops the linker, the chain and the confirmation still prints a plausible total and a plausible
    budget/measured ratio -- which is the one thing this whole comparison exists to catch, so the
    omissions travel with the number instead of being inferred from a shorter parts dict.
    """
    counts = {"detect": n, "crop": n, "encode": n, "head": n, link_key: n - 1, "chain": 1, "confirm": 1}
    total, parts, missing = 0.0, {}, []
    for s, c in counts.items():
        v = stages.get(s)
        if isinstance(v, dict) and "median_ms" in v:
            parts[s] = round(c * v["median_ms"], 3)
            total += c * v["median_ms"]
        else:
            missing.append(s)
    return round(total, 2), parts, missing


# ------------------------------------------------------------------------------------------- the figure

def make_figure(res, out_stem):
    """Three panels: stage cost per exposure by device, the sweep cost against the number of exposures, and
    where the time goes. Drawn at 13 in for printing at 6.9 in (tools/_figfit)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from _figfit import fit

    plt.rcParams.update({"font.size": 13, "axes.titlesize": 14, "axes.labelsize": 13})
    devs = list(res["by_device"])
    geo = res["geometry"]
    order = ["detect", "crop", "encode", "head", "link", "link_reduced", "chain", "confirm"]

    def stage_of(di, dv, s):
        # link / chain / confirm are numpy and OpenCV: they were measured ONCE, not per torch device,
        # so they are drawn once rather than repeated as though each device had its own measurement
        if s in ("link", "link_reduced", "chain", "confirm"):
            if di > 0:
                return None
            if s == "link_reduced":
                return (geo.get("reduced") or {}).get("link")
            if s == "link":
                return (geo.get("as_implemented") or {}).get("link")   # never fall back: a reduced link
                #                                                       drawn in the "link" row would read
                #                                                       as the cost of the shipped code
            return (geo.get("as_implemented") or {}).get(s) or (geo.get("reduced") or {}).get(s)
        return res["by_device"][dv]["stages"].get(s)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))

    ax = axes[0]
    wid = 0.8 / max(1, len(devs))
    GEO_ROWS = ("link", "link_reduced", "chain", "confirm")
    drawn_geo = False
    for di, dv in enumerate(devs):
        for si, s in enumerate(order):
            v = stage_of(di, dv, s)
            if not isinstance(v, dict) or "median_ms" not in v:
                continue
            geo_row = s in GEO_ROWS
            # link / chain / confirm are numpy and OpenCV and were measured ONCE, not per torch device.
            # Drawing them in the first device's colour and under its legend entry reads as though that
            # device had its own measurement, so they get a neutral colour and a legend entry of their own.
            y = (si if geo_row else si + di * wid - 0.4 + wid / 2)
            h = (0.55 if geo_row else wid * 0.9)
            kw = {"color": "0.55", "label": ("CPU only, measured once" if not drawn_geo else None)} \
                if geo_row else {"color": f"C{di}", "label": (dv if si == 0 or True else None)}
            if geo_row:
                drawn_geo = True
            ax.barh([y], [max(v["median_ms"], 1e-3)], height=h, **kw)
            ax.hlines([y], [max(v.get("p05_ms", v["median_ms"]), 1e-3)],
                      [max(v.get("p95_ms", v["median_ms"]), 1e-3)], color="k", linewidth=1.0)
            # A "p5-p95" drawn from two repeats is the range of two numbers. The n is on the bar so the
            # whisker is not read as a distribution it was never measured from.
            if v.get("n"):
                ax.text(max(v["median_ms"], 1e-3) * 1.08, y, f"n={v['n']}", va="center",
                        fontsize=8, color="0.25")
    h_, l_ = ax.get_legend_handles_labels()
    seen, hh, ll = set(), [], []
    for hx, lx in zip(h_, l_):
        if lx and lx not in seen:
            seen.add(lx); hh.append(hx); ll.append(lx)
    # detect/crop/encode/head run once PER EXPOSURE; link runs once per consecutive PAIR; chain and
    # confirm run once per SWEEP. One "ms per exposure" label over all seven rows would be wrong for four
    # of them, so the y labels carry the unit and the x label carries only the clock.
    per = {"detect": "/exposure", "crop": "/exposure", "encode": "/exposure", "head": "/exposure",
           "link": "/pair", "link_reduced": "/pair", "chain": "/sweep", "confirm": "/sweep"}
    ax.set_yticks(np.arange(len(order)))
    ax.set_yticklabels([s + per.get(s, "") for s in order])
    ax.set_xscale("log")
    ax.set_xlabel("ms, median; bar range is p5-p95 of n repeats (n on each bar)")
    ax.set_title("Stage cost")
    ax.grid(True, axis="x", alpha=0.3)
    ax.legend(hh, ll, fontsize=9, loc="best", framealpha=0.9)
    ax.invert_yaxis()

    ax = axes[1]
    for dv in devs:
        e2e = res["by_device"][dv]["end_to_end"]
        ks = sorted(int(k) for k in e2e)
        ax.plot(ks, [e2e[str(k)]["measured"]["median_ms"] / 1000.0 for k in ks], "o-",
                label=f"{dv}, reduced linker (measured)")
        bud = [e2e[str(k)]["budget_as_implemented_ms"] for k in ks]
        if all(b is not None for b in bud):
            ax.plot(ks, [b / 1000.0 for b in bud], "s--", alpha=0.7,
                    label=f"{dv}, as implemented (budget)")
    ax.set_xlabel("exposures in the sweep")
    ax.set_ylabel("seconds, whole sweep")
    ax.set_yscale("log")
    ax.set_title("End to end")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)

    ax = axes[2]
    dv = devs[0]
    n = res["config"]["sweep_lengths"][-1]
    ee = res["by_device"][dv]["end_to_end"][str(n)]
    parts = ee["budget_as_implemented_parts"] or ee["additive_budget_reduced_parts"]
    tot = sum(v for v in parts.values() if v > 0) or 1.0
    labs, vals, small = [], [], 0.0
    for k, v in sorted(parts.items(), key=lambda kv: -kv[1]):
        if v <= 0:
            continue
        if v / tot < 0.02:            # slices under 2 % collide with each other's labels
            small += v
        else:
            labs.append(k); vals.append(v)
    if small > 0:
        labs.append("other"); vals.append(small)
    if vals:
        ax.pie(vals, labels=labs, autopct="%1.0f%%", textprops={"fontsize": 10})
    kind = "as implemented" if ee["budget_as_implemented_parts"] else "reduced linker"
    # A pie reads as a whole. If the detector is not in it, the share every other stage shows is over a
    # denominator that is missing the largest stage on any machine, so the title says so.
    gone = [s for s in (ee.get("budget_as_implemented_missing_stages")
                        if ee["budget_as_implemented_parts"]
                        else ee.get("additive_budget_reduced_missing_stages")) or []]
    ax.set_title(f"{n} exposures, {kind}" + chr(10) + f"{dv}"
                 + (chr(10) + "EXCLUDES " + ", ".join(gone) if gone else ""))

    miss = ", ".join(res["not_measured"]) or "none"
    fig.suptitle(f"Runtime cost of the C-arm level pipeline | {res['hardware'].get('cpu_model', '?')} | "
                 f"GPU {res['hardware'].get('gpu') or 'none'} | not measured: {miss}", fontsize=13)
    fig.tight_layout(rect=(0, 0.02, 1, 0.91))
    fit(fig, fig.texts[0], 12.6)
    Path(out_stem).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out_stem) + ".png", dpi=200)
    fig.savefig(str(out_stem) + ".pdf")
    plt.close(fig)
    return [str(out_stem) + ".png", str(out_stem) + ".pdf"]


# ------------------------------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", help="result JSON")
    ap.add_argument("--fig", default=None, help="figure stem (writes .png and .pdf)")
    ap.add_argument("--detector", default=None, help="YOLO .pt; the detector stage is not_measured without it")
    ap.add_argument("--imgsz", type=int, default=1024, help="detector input size (the devcorpus arms use 1024)")
    ap.add_argument("--model", default=None, help="level encoder .pt (optional: shapes, not values, set the time)")
    ap.add_argument("--head", default=None, help="recurrent head .pt (optional, same reason)")
    ap.add_argument("--arch", default="resnet18")
    ap.add_argument("--size", type=int, default=320, help="context-crop canvas (make_context_crops --size)")
    ap.add_argument("--frames", default=None, help="directory of real device frames to time on instead of synthetic")
    ap.add_argument("--frame-size", type=int, nargs=2, default=[CARM_FRAME_PX, CARM_FRAME_PX], metavar=("H", "W"))
    ap.add_argument("--px-mm", type=float, default=CARM_PX_MM, help="pixel size of an exposure, mm")
    ap.add_argument("--pitch-mm", type=float, default=None, help="vertebral pitch, mm; default sweep_map.PITCH_MM lumbar")
    ap.add_argument("--pitch-px", type=float, default=None, help="override the derived pitch in pixels")
    ap.add_argument("--bodies", type=int, default=None, help="vertebrae per exposure; default read from --bodies-from")
    ap.add_argument("--bodies-from", default=DEFAULT_BODIES_FILE)
    ap.add_argument("--overlap-bodies", type=float, default=1.0, help="bodies of overlap the protocol commands")
    ap.add_argument("--sweep", type=int, nargs="+", default=[3, 7], help="sweep lengths to time end to end")
    ap.add_argument("--repeats", type=int, default=20, help="repeats for the network stages")
    ap.add_argument("--geo-repeats", type=int, default=5, help="repeats for link / chain / confirm")
    ap.add_argument("--full-linker-repeats", type=int, default=2,
                    help="repeats for the FULL-resolution link; each one is minutes on a real frame")
    ap.add_argument("--warmup", type=int, default=3)
    ap.add_argument("--e2e-repeats", type=int, default=3)
    ap.add_argument("--threads", type=int, nargs="+", default=None, help="CPU thread counts; default [1, all]")
    ap.add_argument("--no-gpu", action="store_true", help="skip the GPU even if one is present")
    ap.add_argument("--no-tta", action="store_true", help="no horizontal-flip TTA (the prototype uses it)")
    ap.add_argument("--skip-full-linker", action="store_true",
                    help="do not time the linker at full resolution (it is minutes per link)")
    ap.add_argument("--full-linker-e2e", action="store_true",
                    help="also MEASURE the end-to-end sweep with the full-resolution linker (slow)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--selftest", action="store_true",
                    help="check the fallback encoder against the published ResNet-18 cost and exit")
    ap.add_argument("--redraw", default=None,
                    help="redraw the figure from a result JSON this tool wrote and exit; measures nothing")
    EG.add_args(ap)
    a = ap.parse_args()

    if a.redraw:
        if not a.fig:
            ap.error("--redraw needs --fig")
        print("figure:", make_figure(json.load(open(a.redraw)), a.fig))
        return 0

    import torch
    torch.manual_seed(a.seed)
    if a.selftest:
        return 0 if selftest(torch)[0] else 1
    if not a.out:
        ap.error("--out is required (unless --selftest)")

    repo = Path(__file__).resolve().parents[1]
    load0 = machine_load()
    if load0.get("other_busy_processes"):
        print("WARNING: other processes are busy on this machine; every millisecond below is contended: "
              + ", ".join(f"{d['name']}({d['pid']}) {d['cpu_percent']}%" for d in load0["other_busy_processes"]),
              flush=True)
    import sweep_map as SM
    from make_context_crops import LEVEL_ORDER
    n_classes = len(LEVEL_ORDER)
    tta = not a.no_tta
    rng = np.random.default_rng(a.seed)
    caveats, not_measured = [], {}

    # --- how many bodies an exposure holds, from the scored result rather than from a habit
    bpf, bpf_src = bodies_per_frame(repo, a.bodies_from)
    bodies = a.bodies if a.bodies else (int(round(bpf)) if bpf else 4)
    if a.bodies:
        bpf_src = {"source": "--bodies on the command line", "value": a.bodies, "also_on_disk": bpf_src}
    elif not bpf:
        # Say it, rather than let a hard-coded 4 pass as a number read from a scored result.
        bpf_src = {"source": "HARD-CODED DEFAULT 4: the file could not be read", "value": 4,
                   "tried": bpf_src}
        caveats.append(f"Bodies per exposure is the hard-coded default 4, NOT a number read from "
                       f"{a.bodies_from}: {bpf_src['tried'].get('source')}.")

    # --- the geometry, derived and then cross-checked against the measured spacing
    H, W = a.frame_size
    pitch_mm = a.pitch_mm if a.pitch_mm else SM.PITCH_MM["lumbar"]
    pitch = a.pitch_px if a.pitch_px else pitch_mm / a.px_mm
    prior_dy = -(bodies - a.overlap_bodies) * pitch
    print(f"geometry: pitch {pitch:.1f} px derived from {pitch_mm} mm at {a.px_mm} mm/px; "
          f"{bodies} bodies per exposure", flush=True)

    # --- the exposures
    n_max = max(a.sweep)
    d_in_guess = 512
    if a.frames:
        stations_all, frames_src = real_stations(a.frames, n_max, bodies, pitch, d_in_guess, n_classes, rng)
        H, W = stations_all[0]["img"].shape
    else:
        stations_all = synth_stations(n_max, H, W, bodies, pitch, d_in_guess, n_classes, rng)
        frames_src = {"kind": "synthetic exposures at the geometry above",
                      "why": "the correlation grid, the crops and the template are set by frame size, pitch "
                             "and box count, not by the bone; --frames times the same stages on real frames"}
        caveats.append("Exposures were SYNTHETIC (noise plus a periodic column of blocks at a fixed pitch). "
                       "Image CONTENT does not change the size of the correlation grid, the crops or the "
                       "template, so the TIMINGS stand; but consecutive synthetic exposures hold their "
                       "blocks at identical positions, so any correlation peak lands on a multiple of the "
                       "pitch by construction and geometry.reduced.same_answer_check is DEGENERATE on this "
                       "input -- it says nothing about whether the reduction preserves a real translation. "
                       "Only --frames answers that.")

    # --- the geometry cross-check, made only NOW, because --frames may have changed the frame size and a
    #     check decided on the default 1024 would certify a pitch that is not the pitch of these exposures.
    #     A linker timed at the wrong pitch searches the wrong window and still prints a plausible number.
    at_carm = (int(H) == CARM_FRAME_PX and abs(a.px_mm - CARM_PX_MM) < 1e-6 and a.pitch_px is None)
    xcheck = {"applies": bool(at_carm),
              "derived_pitch_px": round(float(pitch), 2),
              "frame_px_actually_used": [int(H), int(W)],
              "measured_pitch_px": CARM_MEASURED_PITCH_PX if at_carm else None,
              "measured_from": CARM_MEASURED_PITCH_SOURCE if at_carm else
                               "not applicable: the frame size (%dx%d), the pixel size or the pitch is not "
                               "the C-ArmLSpine geometry the reference pitch was measured at" % (H, W),
              "relative_difference": (round(abs(pitch - CARM_MEASURED_PITCH_PX) / CARM_MEASURED_PITCH_PX, 4)
                                      if at_carm else None)}
    if not at_carm:
        caveats.append(f"The pitch cross-check does NOT apply: these exposures are {H}x{W} px at "
                       f"{a.px_mm} mm/px with pitch {pitch:.1f} px, which is not the C-ArmLSpine geometry "
                       f"the 177.9 px reference was measured at. The pitch is unverified against anything "
                       f"outside this run.")
    print(f"geometry: frame {H}x{W} px, pitch {pitch:.1f} px"
          + (f" (C-ArmLSpine measured median {CARM_MEASURED_PITCH_PX} px, "
             f"{100 * xcheck['relative_difference']:.1f} % apart)" if at_carm
             else " (cross-check NOT applicable at this geometry)"), flush=True)

    # --- the encoder, and the one external check available on it
    # THE GATE (tools/eval_gate.py; docs/DATA_ACCOUNTING.md 5.3). This tool reports latency, not accuracy, but it
    # runs the named weights over --frames; those frames' patients are gated like any evaluation set, so no
    # output of these weights on a patient they saw leaves this tool without saying so. Synthetic exposures hold
    # no patient: the verdict then says not held out, and why.
    loaded = {"detector": a.detector, "encoder": a.model, "head": a.head}
    if a.frames and any(loaded.values()):
        frame_items = [dict(path=str(p)) for p in sorted(Path(a.frames).rglob("*.png"))[:n_max]]
        gate = EG.gate_evaluation(frame_items, loaded, "tools/eval_runtime_cost.py", a, eval_set=str(a.frames))
    else:
        gate = EG.block([], "no patient is scored: synthetic exposures or no weights; a timing, not a held-out "
                            "number")
    enc, enc_src, enc_note, enc_loaded = build_encoder(n_classes, a.arch, 2, a.model, torch)
    st_detail = None
    if "_local_resnet18" in enc_src:
        ok, st_detail = selftest(torch)
        if not ok:
            raise SystemExit("the local ResNet-18 fallback does not match the published ResNet-18 cost; "
                             "refusing to time it")
    if enc_note:
        caveats.append("Encoder: " + enc_note)
    if not enc_loaded:
        caveats.append("Encoder weights were not loaded. A forward's latency is a function of the architecture "
                       "and the input shapes, not of the weight values, so the timing stands; the JSON records it.")

    import torch.nn as nn
    from recurrent_order import RunLabeller
    fc = enc.fc if isinstance(getattr(enc, "fc", None), nn.Linear) else nn.Linear(512, n_classes)
    d_in = fc.in_features
    enc.fc = nn.Identity()
    head_mod = RunLabeller(d_in, n_classes).eval()
    head_loaded = False
    if a.head:
        try:
            head_mod.load_state_dict(torch.load(a.head, map_location="cpu"))
            head_loaded = True
        except Exception as e:  # noqa: BLE001
            caveats.append(f"Head weights not loaded ({type(e).__name__}); shapes unchanged so the timing "
                           f"is unaffected.")

    macs = {"encoder_per_crop": macs_of(enc, torch.rand(1, 2, a.size, a.size), torch),
            "head_per_run_of_%d" % bodies: macs_of(head_mod, torch.rand(1, bodies, d_in), torch)}

    # --- the detector, or an honest hole where it would be
    detector = None
    if a.detector:
        try:
            from ultralytics import YOLO
            detector = YOLO(a.detector)
        except Exception as e:  # noqa: BLE001
            not_measured["detect"] = {"reason": f"{type(e).__name__}: {str(e)[:160]}", "weights": a.detector}
    else:
        not_measured["detect"] = {"reason": "no --detector given"}
    if "detect" in not_measured:
        caveats.append("The detector stage was NOT measured, so every end-to-end figure here excludes it, is "
                       "named end_to_end_excluding_detector, and is a LOWER BOUND on the sweep.")

    res = {
        "about": "per-stage and end-to-end runtime of the C-arm level pipeline, measured by "
                 "tools/eval_runtime_cost.py; every number is a clock on this machine",
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "code_sha": code_sha(),
        "seed": a.seed,
        "hardware": hardware(torch),
        "machine_load_at_start": load0,
        "config": {
            "frame_px": [int(H), int(W)], "px_mm": a.px_mm, "pitch_mm": pitch_mm,
            "pitch_px": round(float(pitch), 2),
            "pitch_px_derivation": "--pitch-px" if a.pitch_px else "pitch_mm / px_mm",
            "pitch_px_cross_check": xcheck,
            "bodies_per_exposure": bodies, "bodies_per_exposure_source": bpf_src,
            "commanded_step_px": round(float(prior_dy), 2), "overlap_bodies": a.overlap_bodies,
            "crop_canvas_px": a.size, "crop_target_px": 96.0, "detector_imgsz": a.imgsz,
            "tta_horizontal_flip": tta, "sweep_lengths": a.sweep,
            "repeats": a.repeats, "geo_repeats": a.geo_repeats,
            "full_linker_repeats": a.full_linker_repeats, "e2e_repeats": a.e2e_repeats,
            "frames": frames_src, "work_pitch_px": SM.WORK_PITCH,
        },
        "models": {
            "encoder_source": enc_src, "encoder_weights": a.model, "encoder_weights_loaded": enc_loaded,
            "head_weights": a.head, "head_weights_loaded": head_loaded,
            "detector_weights": a.detector, "detector_loaded": detector is not None,
            "n_classes": n_classes, "embedding_dim": int(d_in),
            "encoder_params": int(sum(p.numel() for p in enc.parameters())),
            "head_params": int(sum(p.numel() for p in head_mod.parameters())),
            "macs": macs, "resnet18_selftest": st_detail,
        },
        "geometry": {}, "by_device": {}, "not_measured": not_measured, "caveats": caveats,
    }

    # --- link / chain / confirm: CPU-only, so measured once. The REDUCED pass runs first, because its
    #     links are what lets the full-resolution confirmation be set up without paying for (n-1) links.
    red_stations, red = reduce_stations(stations_all, pitch, SM.WORK_PITCH, d_in_guess, n_classes, rng)
    geo_red, links_red = None, None
    if red < 1.0:
        geo_red = measure_geometry(red_stations, pitch * red, prior_dy * red, max(a.geo_repeats, 5),
                                   f"reduced to WORK_PITCH={SM.WORK_PITCH} px per body (scale {red:.3f})")
        links_red = geo_red.pop("_links")
        geo_red["scale"] = round(float(red), 4)
        res["geometry"]["reduced"] = geo_red
        print("  reduced: link %.1f ms  chain %.1f ms  confirm %.1f ms"
              % (geo_red["link"]["median_ms"], geo_red["chain"]["median_ms"],
                 geo_red["confirm"]["median_ms"]), flush=True)
    else:
        res["geometry"]["reduced"] = None
        red_stations = stations_all

    geo_full = {}
    if not a.skip_full_linker:
        print(f"timing the linker at full resolution ({a.full_linker_repeats} repeat(s); minutes per link "
              f"on a real frame)...", flush=True)
        geo_full = measure_geometry(stations_all, pitch, prior_dy, a.full_linker_repeats,
                                    "as implemented (full resolution)", do_chain=False,
                                    known_links=scale_links(links_red, 1.0 / red) if links_red else None)
        geo_full.pop("_links", None)
        if geo_red:
            geo_full["chain"] = {**geo_red["chain"],
                                 "note": "measured in the reduced pass: the chain's own work is index "
                                         "bookkeeping over the nodes and does not depend on the frame's "
                                         "resolution"}
            geo_red["speedup_vs_as_implemented"] = round(
                geo_full["link"]["median_ms"] / max(geo_red["link"]["median_ms"], 1e-6), 1)
            sf, sr = geo_full["link"].get("shift"), geo_red["link"].get("shift")
            if sf and sr:
                agrees = bool(abs(sr["dy"] / red - sf["dy"]) <= 1.0 / red)
                geo_red["same_answer_check"] = {
                    "full_dy": sf["dy"], "reduced_dy": sr["dy"], "scale": round(float(red), 4),
                    "reduced_dy_rescaled": round(sr["dy"] / red, 1),
                    "disagreement_px_full_scale": round(abs(sr["dy"] / red - sf["dy"]), 1),
                    "tolerance_px_full_scale": round(1.0 / red, 1),
                    "agrees_within_one_reduced_pixel": agrees,
                    "synthetic_exposures": not bool(a.frames),
                    "what": "the reduction is only free if it returns the same translation",
                    "caveat": None if a.frames else
                              "DEGENERATE: synthetic exposures repeat the same periodic block column, so "
                              "both resolutions lock onto the same multiple of the pitch whatever the "
                              "reduction does. Re-run with --frames before reading this as evidence."}
                # A disagreement is the whole reason the check exists, so it is not left as a buried
                # boolean beside a headline speed-up.
                print(("  same answer: " if agrees else "  DIFFERENT ANSWER: ")
                      + "full dy %d, reduced dy %d -> %.1f at full scale (tolerance %.1f px)"
                      % (sf["dy"], sr["dy"], sr["dy"] / red, 1.0 / red), flush=True)
                if not agrees:
                    caveats.append(
                        f"THE REDUCTION CHANGED THE ANSWER: ncc_shift returned dy {sf['dy']} at full "
                        f"resolution and {sr['dy']} reduced ({sr['dy'] / red:.1f} rescaled), "
                        f"{abs(sr['dy'] / red - sf['dy']):.1f} px apart against a tolerance of "
                        f"{1.0 / red:.1f} px. The "
                        f"{geo_red.get('speedup_vs_as_implemented')}x speed-up is NOT free on this input "
                        f"and must not be quoted as a remedy.")
                elif not a.frames:
                    caveats.append(
                        "same_answer_check passed on SYNTHETIC exposures, whose blocks sit at identical "
                        "positions in every frame; agreement there is forced by the periodicity and is "
                        "not evidence that the reduction preserves a real translation.")
        res["geometry"]["as_implemented"] = geo_full
        print("  as implemented: link %.0f ms  confirm %.0f ms"
              % (geo_full["link"]["median_ms"], geo_full["confirm"]["median_ms"]), flush=True)
        if a.full_linker_repeats < 3:
            caveats.append(f"The full-resolution link was timed {a.full_linker_repeats} time(s), so its "
                           f"spread is not estimated; raise --full-linker-repeats to get one.")
    else:
        not_measured["link_full_resolution"] = {"reason": "--skip-full-linker"}
        res["geometry"]["as_implemented"] = {}

    # --- which torch devices to run the networks on
    devices = []
    if torch.cuda.is_available() and not a.no_gpu:
        devices.append(("cuda", "cuda", None))
    for t in (a.threads if a.threads else sorted({1, os.cpu_count() or 1})):
        devices.append(("cpu", f"cpu_{t}thr", t))

    img0, boxes0 = stations_all[0]["img"], stations_all[0]["boxes"]
    e2e_name = "end_to_end" if detector is not None else "end_to_end_excluding_detector"

    for dev, label, threads in devices:
        if threads:
            torch.set_num_threads(int(threads))
        enc_d, fc_d, head_d = enc.to(dev), fc.to(dev), head_mod.to(dev)
        # The detector has to be moved TOO. The stage below times it with an explicit device= argument,
        # but the end-to-end loop reaches it through sweep_map.detect_boxes, which passes no device and so
        # uses whatever the model is on. Without this, a "cpu_16thr" end-to-end on a GPU node would run
        # the detector on the GPU while its budget line held a CPU-timed detector -- the two halves of the
        # cross-check measuring different hardware, which is the kind of disagreement it exists to detect.
        if detector is not None:
            try:
                detector.to(0 if dev == "cuda" else "cpu")
            except Exception as e:  # noqa: BLE001
                caveats.append(f"[{label}] the detector could not be moved to {dev} ({type(e).__name__}); "
                               f"the end-to-end detector call may be on another device than its stage "
                               f"timing, so budget and wall clock are not comparable for this arm.")
        if dev == "cuda":
            torch.cuda.reset_peak_memory_stats()

        stages = measure_networks(dev, enc_d, head_d, fc_d, a.size, 2, n_classes, tta,
                                  a.repeats, a.warmup, torch, img0, boxes0)
        if detector is not None:
            dev_arg = 0 if dev == "cuda" else "cpu"
            rgb = np.stack([img0] * 3, -1)
            stages["detect"] = stats(
                timeit(lambda: detector.predict(rgb, imgsz=a.imgsz, conf=0.25, device=dev_arg, verbose=False),
                       max(5, a.repeats // 2), 2,
                       (lambda: torch.cuda.synchronize()) if dev == "cuda" else None),
                {"what": f"ultralytics YOLO forward at imgsz {a.imgsz}, one exposure, conf 0.25",
                 "weights": a.detector})

        e2e = {}
        for n in a.sweep:
            red_n = [dict(s) for s in red_stations[:n]]
            ts = end_to_end(red_n, pitch * red, prior_dy * red, dev, enc_d, head_d, fc_d, a.size, tta,
                            torch, detector, a.imgsz, a.e2e_repeats)
            m = stats(ts, {"what": f"composed pipeline over {n} exposures, wall clock, with the linker at "
                                   f"WORK_PITCH (the reduction map_query_panorama already applies)"})
            geo_impl = res["geometry"].get("as_implemented") or {}
            # When nothing was reduced (pitch already <= WORK_PITCH) the wall clock above ran the
            # FULL-resolution linker, so the budget it is compared against must be the full one too.
            # Taking the empty "reduced" geometry would drop link, chain and confirm and still print a
            # ratio -- a budget missing three stages compared against a clock that ran them.
            geo_for_budget = res["geometry"].get("reduced") or geo_impl
            b_red, p_red, miss_red = additive_budget({**stages, **geo_for_budget}, n, "link")
            if geo_impl.get("link"):
                b_full, p_full, miss_full = additive_budget({**stages, **geo_impl}, n, "link")
                kind = ("additive budget from measured stages, not a wall clock; its validity is the "
                        "measured/budget ratio at reduced resolution, reported beside it")
            else:
                b_full, p_full, miss_full = None, None, None
                kind = "not computed: the full-resolution linker was not measured (--skip-full-linker)"
            entry = {
                "measured": m,
                "additive_budget_reduced_ms": b_red,
                "additive_budget_reduced_parts": p_red,
                "additive_budget_reduced_missing_stages": miss_red,
                "budget_over_measured_reduced": round(b_red / m["median_ms"], 3) if m["median_ms"] else None,
                "budget_over_measured_is_a_check_only_if": (
                    "the missing-stage lists are empty and the measured spread is small beside the "
                    f"disagreement: here rel SD of the wall clock is {m.get('rel_sd')} over n="
                    f"{m['n']} repeat(s), and any stage smaller than that spread is invisible to this "
                    "comparison. Raise --e2e-repeats before reading the ratio as evidence."),
                "budget_stage_resolution_note": (
                    "crop/encode/head in this budget were timed on FULL-resolution exposures while the "
                    f"wall clock composed them at scale {red:.4f}; the crop stage in particular is "
                    "resolution-dependent (a percentile over the whole frame), so the budget over-counts "
                    "it. The two are not the same quantity to within better than a few per cent."
                    if red < 1.0 else "no reduction applied; budget and wall clock are at one resolution"),
                "budget_as_implemented_ms": b_full,
                "budget_as_implemented_parts": p_full,
                "budget_as_implemented_missing_stages": miss_full,
                "budget_as_implemented_kind": kind,
                "detector_included": detector is not None,
                "name": e2e_name,
            }
            hard_miss = [s for s in miss_red if s != "detect"]   # detect is already caveated and renamed
            if hard_miss:
                caveats.append(f"[{label}] sweep of {n}: the additive budget is missing "
                               f"{', '.join(hard_miss)}; budget_over_measured_reduced "
                               f"({entry['budget_over_measured_reduced']}) is NOT a consistency check.")
            if a.full_linker_e2e:
                # build_chain pays one FULL-resolution link per pair, and a full link is minutes on a real
                # frame. Say what this will cost before spending it, so a job is not silently sized in hours.
                lk = (geo_impl.get("link") or {}).get("median_ms")
                if lk:
                    reps = max(1, a.e2e_repeats // 2) + 1
                    print(f"  --full-linker-e2e: {reps} run(s) x {n - 1} link(s) x {lk / 1000:.0f} s "
                          f"= about {reps * (n - 1) * lk / 60000:.0f} min for this sweep alone", flush=True)
                sts = [dict(s) for s in stations_all[:n]]
                entry["measured_as_implemented"] = stats(
                    end_to_end(sts, pitch, prior_dy, dev, enc_d, head_d, fc_d, a.size, tta, torch,
                               detector, a.imgsz, max(1, a.e2e_repeats // 2)),
                    {"what": f"composed pipeline over {n} exposures, wall clock, linker at full resolution"})
            e2e[str(n)] = entry

        entry = {"stages": stages,
                 "end_to_end": e2e, "torch_threads": int(threads) if threads else None,
                 "peak_process_rss_mb": peak_rss_mb(),
                 "peak_rss_note": "high-water mark of the whole process, cumulative and monotone; not a "
                                  "per-stage working set"}
        if dev == "cuda":
            entry["gpu_peak_allocated_mb"] = round(torch.cuda.max_memory_allocated() / 1e6, 1)
            entry["gpu_peak_reserved_mb"] = round(torch.cuda.max_memory_reserved() / 1e6, 1)
        res["by_device"][label] = entry

        print(f"[{label}] " + "  ".join(f"{k}={v['median_ms']:.1f}ms" for k, v in entry["stages"].items()
                                        if isinstance(v, dict) and "median_ms" in v), flush=True)
        for n in a.sweep:
            ee = e2e[str(n)]
            print(f"[{label}] sweep of {n}: measured {ee['measured']['median_ms'] / 1000:.2f} s with the "
                  f"reduced linker (budget {ee['additive_budget_reduced_ms'] / 1000:.2f} s, ratio "
                  f"{ee['budget_over_measured_reduced']}); as implemented, budget "
                  + (f"{ee['budget_as_implemented_ms'] / 1000:.1f} s" if ee['budget_as_implemented_ms'] else "not measured")
                  + f"; detector_included={ee['detector_included']}",
                  flush=True)

    res["machine_load_at_end"] = machine_load()
    for tag in ("machine_load_at_start", "machine_load_at_end"):
        busy = (res.get(tag) or {}).get("other_busy_processes")
        if busy:
            caveats.append(f"{tag}: the machine was shared - "
                           + ", ".join(f"{d['name']} at {d['cpu_percent']} %" for d in busy)
                           + ". Every latency here is a CONTENDED latency and is an upper bound.")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    if a.fig:
        try:
            res["figure"] = make_figure(res, a.fig)
            print("figure:", res["figure"])
        except Exception as e:  # noqa: BLE001
            res["figure_error"] = f"{type(e).__name__}: {str(e)[:200]}"
            print("figure failed:", res["figure_error"], flush=True)
    json.dump(EG.stamp(res, gate), open(a.out, "w"), indent=1)
    print("wrote", a.out)
    if not_measured:
        print("NOT MEASURED:", json.dumps(not_measured))
    for c in caveats:
        print("caveat:", c)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
