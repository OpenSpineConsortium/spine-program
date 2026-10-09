# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/cine_latency.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Per-frame latency of the reported naming pipeline on a cine, stage by stage -- after proving it IS that pipeline.

    python tools/cine_latency.py run --pred "/rs/.../or_ready/cine/carm_sweep/case39/primary/pred" \\
        --dataset case39 --fps 10.3 --out /rs/.../or_ready/cine/carm_sweep/case39/primary
    python tools/cine_latency.py self-test          # the non-model parts; runs on Windows, no GPU, no ultralytics

WHY A SEPARATE TIMER (docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md section 0 and 1c). Accuracy comes from
tools/level_prototype.py, the gated and reported pipeline, and its per-frame `seconds` is not a latency: it
includes the hardware detector, the rule flags, an overlay PNG and a JSON write for every frame. So latency is
measured here, in process, on the same three weights, and it is measured only on a pipeline that has first
been shown to BE the prototype's. That is the parity gate:

    on --parity-frames frames (50, evenly spaced over the stream) of the prototype's own output directory, the
    boxes must equal the prototype's exactly, the decoded names, single-crop names and abstain flags must be
    identical, and the largest difference in any posterior entry (blended and single-crop) must be below 1e-5.

If parity fails, NO latency.json is written: the parity record goes to latency_parity_failed.json and the tool
exits 3. Before anything is measured, every file this run could write under its canonical name (latency.json,
latency_frames.csv, latency_parity_failed.json) is moved aside if an earlier run left one (<name>_superseded_<time>),
and latency.json is written LAST and atomically, after latency_frames.csv. So whatever sits under those names after
a run is that run's -- a crash after the gate leaves no latency.json at all -- and latency.json exists only where a
latency was published, which is what an existence predicate in tools/pipeline_state.py can rely on. A --allow-cpu
smoke run writes latency_cpu_smoke*.json/.csv instead and never touches (or moves) the GPU files.
A timer that runs a slightly different pipeline than the one whose accuracy is reported would publish a
speed for a system that was never scored -- a finite, plausible, wrong number, which is this project's usual
failure. Every timed frame is compared as well (outside the clock), and the count is recorded beside the gate.

ONE GPU TYPE FOR BOTH RUNS. Torch's default lets cuDNN convolutions run in TF32 on Ampere and later (L40S, H200)
and in FP32 on a V100, and the three grid GPU partitions carry three architectures, so the 1e-5 posterior gate is
only meaningful when the prototype and this timer ran on the same GPU model. slurm/cine_latency.sh pins one
(gmsap, --constraint=h200) and passes --require-gpu; the cine_infer_* jobs must be pinned to the same. When a
prototype meta records its GPU (`gpu_name`, torch.cuda.get_device_name(0)), a run whose GPU differs from every
recorded one is refused before anything is measured, and the parity record says which GPU each sampled frame's
prototype output came from; when no meta records one (level_prototype does not yet), the record says so
(`parity.gpu.status` = "unrecorded") and the partition pin is the only control.

THE PRIMARY ARM ONLY, unless declared otherwise. Plan section 0 makes the histogram match (~/films_drr) and the
flip-TTA part of the reported pipeline, and the rare penalty and the three weights are the prototype's shipped
ones. A prototype output that ran without either, with another reference directory, another rare penalty or other
weights is refused unless --not-primary REASON is given; the reason and every deviation then go into latency.json
(`arm`) and into the claim sentence, so a faster number from a lighter pipeline cannot be read as the primary's.

WHAT IS TIMED. Every stage calls the function the prototype calls; nothing is a stand-in:

    load_png   level_prototype.load_image                      (disk read and PNG decode: reported, NOT in end to end)
    prepare    fluorocap_infer.prepare_panel(im, False, False, hist_ref=ref) and the RGB copy the detector reads
    detect     YOLO.predict(rgb, imgsz, conf) and the keypoint -> box reduction of level_prototype.py:368-376
    name       sweep_map.Namer(model, head, dev).run(img_u8, boxes) -> (emb, p_single, p_blend); the flip-TTA is
               inside it. Namer.run is the prototype's posterior computation line for line (the parity gate is
               what proves it on the data)
    decode     fluorocap_anchor.decode(p_blend, set(), {}, None, direction_known=True, w_rare) and the prototype's
               abstain rule (level_prototype.py:407-414: the decoded name differs from the single-crop name, or
               its probability is below --abstain-below)
    track      the online tracker of tools/cine_eval.py -- `Tracker(config, fps).step(dets)`, one per sequence, on
               the committed tracker_config.json (see load_tracker) -- fed the same detection dicts cine_eval's
               own run_tracker builds from a prototype record. When that file, its Tracker or the config is
               missing, a CLEARLY MARKED NO-OP: the stage is reported with its status, the end-to-end figure is
               renamed `end_to_end_excluding_tracker`, and no real-time verdict is issued

Each stage boundary is bracketed by torch.cuda.synchronize(), batch 1, FP32 as shipped (the torch defaults,
including whatever TF32 convolution policy they carry, are recorded, not changed). The first --warmup frames
(20) of the timed stream are run and discarded. End to end is ONE clock from the decoded frame to the tracker
update, not a sum of stages; the additive budget of the stage medians is reported beside it with the ratio,
so a decomposition that is missing something says so (tools/eval_runtime_cost.py, trap 2).

WHAT IS NOT TIMED, AND SAID SO IN THE OUTPUT (`excluded`): acquisition, DICOM decode and display; the PNG read;
the hardware detector, the transitional and rule flags, the overlay and the JSON write the prototype does per
frame; model loading (the models are resident). The weights, settings and every sha256 are checked against
each prototype output's prototype_meta.json before anything runs: the histogram-match directory, the flip-TTA
and the rare penalty are TAKEN from that meta, so they cannot drift from the run whose accuracy is reported.

WHAT MAY BE CLAIMED FROM latency.json (plan 1c): "Per-frame compute on <GPU>, models resident, batch 1,
excluding acquisition, DICOM decode and display: p50 X ms, p95 Y ms", and "real-time at <fps>" only when the
end-to-end p95 is under 1000/fps ms WITH the tracker timed. Not claimable from it: glass-to-glass latency,
operating-room hardware (a grid GPU is a data-centre card), throughput under concurrent acquisition, or any
CPU figure. A half-precision or TensorRT arm changes the outputs and needs its own parity and accuracy run.

`per_frame` in latency.json is {stem: end-to-end ms} -- the median over passes of each timed frame, the measure named
in `per_frame_measure` -- which is what `tools/cine_eval.py video --latency` draws in the HUD. The warm-up frames of
the first pass have no entry when the stream runs once.

The latency carries no accuracy claim, so it is not gated by tools/eval_gate.py; the prototype output's own
verdict is copied into `parity_reference` for the reader.
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_context_crops import LEVEL_ORDER  # noqa: E402
from fluorocap_anchor import decode as anchor_decode  # noqa: E402

H = os.path.expanduser("~")
REPO = Path(__file__).resolve().parents[1]
# docs/CINE_DEMO_BUILD_PLAN_2026-09-26.md section 0: the primary stack for every arm. The prototype's own defaults
# load allspine_v2_r1, so these are always passed and always checked against the prototype output's meta.
DEF_DETECTOR = "/wsu/home/go/go24/go2432/model_registry/797de71a9e0e42f7/detect_v5z_final_best.pt"
DEF_MODEL = f"{H}/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt"
DEF_HEAD = f"{H}/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt"
# the tracker's constants, committed and frozen before any Bournemouth frame is seen (tools/pipeline_state.py
# stage cine_tracker_frozen)
DEF_TRACKER_CONFIG = str(REPO / "SchwingNet" / "results" / "cine" / "tracker_config.json")
# the rest of the primary arm (plan section 0): level_prototype's own defaults, --hist-match ~/films_drr, flip-TTA on
# (no --no-tta), --rare-penalty 1.0
DEF_HIST_MATCH = f"{H}/films_drr"
DEF_RARE_PENALTY = 1.0
# where a prototype meta records the GPU it ran on (torch.cuda.get_device_name(0)); the first key present is read
PROTO_GPU_KEYS = ("gpu_name", "cuda_device_name")
POSTERIOR_TOL = 1e-5
# frame stems of the three cine sources (tools/pipeline_state.py, cine layout): <event>_<motion>_f####,
# case<N>_sw###, ctsp_0533_lat_p<frame>. The sequence is everything before the frame number; the tracker is
# reset whenever it changes.
SEQ_RE = r"^(?P<seq>.+?)[_-](?:f|sw|p)?\d+$"
STAGES = ("prepare", "detect", "name", "decode", "track")
NOT_CLAIMABLE = ["glass-to-glass latency (acquisition, DICOM decode and display are outside the clock)",
                 "operating-room hardware (the grid GPU is a data-centre card)",
                 "throughput under concurrent acquisition",
                 "any CPU figure",
                 "a half-precision or TensorRT arm (it changes the outputs and needs its own parity and accuracy run)"]
EXCLUDED = ["acquisition", "DICOM decode", "display",
            "the PNG read (timed as load_png, reported, not in end to end)",
            "the hardware detector, transitional flags and rule flags level_prototype runs per frame "
            "(they draw or flag; they change no box and no name)",
            "the overlay PNG and JSON writes level_prototype does per frame",
            "model loading (models resident; load time reported separately)"]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def code_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=str(REPO),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:  # noqa: BLE001
        return None


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


# ------------------------------------------------------------------------------------------------ pure helpers

def summ(ms):
    """p50, p95 and max -- the three the plan asks for -- plus mean, min and p99, in ms (numpy's linear
    interpolation between order statistics). A latency quoted as one number is a latency measured once."""
    a = np.asarray(ms, float)
    if a.size == 0:
        return {"n": 0}
    return {"n": int(a.size), "p50_ms": round(float(np.percentile(a, 50)), 3),
            "p95_ms": round(float(np.percentile(a, 95)), 3), "max_ms": round(float(a.max()), 3),
            "p99_ms": round(float(np.percentile(a, 99)), 3), "mean_ms": round(float(a.mean()), 3),
            "min_ms": round(float(a.min()), 3)}


def seq_of(stem, seq_re=SEQ_RE):
    m = re.match(seq_re, stem)
    return m.group("seq") if m else stem


def boxes_from_keypoints(res):
    """level_prototype.py:368-376, verbatim in effect: corners -> tight min/max box, sorted by mean corner y, a
    box under 4 px either way dropped with its corners. Returns (boxes, confs, corners, corner_conf)."""
    boxes, confs, corners, kpconf = [], [], [], []
    if res is not None and res.keypoints is not None and len(res.boxes):
        kp = res.keypoints.xy.cpu().numpy(); cf = res.boxes.conf.cpu().numpy()
        kc = res.keypoints.conf.cpu().numpy() if res.keypoints.conf is not None else None
        for i in np.argsort(kp[:, :, 1].mean(1)):
            pts = kp[i]; b = [int(pts[:, 0].min()), int(pts[:, 1].min()), int(pts[:, 0].max()), int(pts[:, 1].max())]
            if b[2] - b[0] >= 4 and b[3] - b[1] >= 4:
                boxes.append(b); confs.append(round(float(cf[i]), 3))
                corners.append([[round(float(x), 2), round(float(y), 2)] for x, y in pts[:, :2]])
                kpconf.append([round(float(c), 4) for c in kc[i]] if kc is not None else None)
    return boxes, confs, corners, kpconf


def decode_frame(p_blend, p_single, direction_known=True, rare_penalty=1.0, abstain_below=0.5):
    """Stage 4: the anchored decode and the prototype's abstain rule (level_prototype.py:405-414).

    `single` is read from the SINGLE-CROP posterior, never from the blended one: the abstain rule exists to
    compare a counted name with a shape-only name, and reading both from the blend would make them agree by
    construction (the comment at level_prototype.py:390-396)."""
    if len(p_blend) == 0:
        return [], [], [], []
    single = [LEVEL_ORDER[int(i)] for i in np.asarray(p_single).argmax(1)]
    dec = anchor_decode(p_blend, set(), {}, None, direction_known=direction_known, w_rare=rare_penalty)
    decoded = dec.get("anchored_pred") or single
    pj, abstain = [], []
    for j in range(len(decoded)):
        pr = float(p_blend[j][LEVEL_ORDER.index(decoded[j])]) if decoded[j] in LEVEL_ORDER else 0.0
        pj.append(pr); abstain.append(bool((decoded[j] != single[j]) or pr < abstain_below))
    return list(decoded), single, abstain, pj


def compare_frame(rec, out, tol=POSTERIOR_TOL):
    """One frame of this pipeline against the prototype's record of the same frame -> (ok, detail).

    Boxes equal exactly (integers, in order), decoded names, single-crop names and abstain flags identical, and
    every posterior entry within `tol`. The prototype writes posteriors to six significant digits (at most 5e-7
    off for a probability), which is inside the tolerance by a factor of twenty."""
    vert = rec.get("vertebrae") or []
    d = {"stem": rec.get("_stem"), "n_proto": len(vert), "n_here": len(out["boxes"])}
    pb = [[int(v) for v in x["box"]] for x in vert]
    d["boxes_equal"] = pb == [[int(v) for v in b] for b in out["boxes"]]
    d["names_equal"] = [x.get("level") for x in vert] == list(out["names"])
    d["single_equal"] = [x.get("single_crop") for x in vert] == list(out["single"])
    d["abstain_equal"] = [bool(x.get("abstain")) for x in vert] == [bool(v) for v in out["abstain"]]
    dp = ds = None
    if d["boxes_equal"] and vert:
        if any("posterior" not in x or "posterior_single" not in x for x in vert):
            d["posterior_missing"] = True
        else:
            dp = float(np.abs(np.asarray([x["posterior"] for x in vert], float) - np.asarray(out["p_blend"], float)).max())
            ds = float(np.abs(np.asarray([x["posterior_single"] for x in vert], float)
                              - np.asarray(out["p_single"], float)).max())
    d["max_posterior_diff"] = dp; d["max_posterior_single_diff"] = ds
    ok = (d["boxes_equal"] and d["names_equal"] and d["single_equal"] and d["abstain_equal"]
          and not d.get("posterior_missing") and (dp is None or dp < tol) and (ds is None or ds < tol))
    d["ok"] = bool(ok)
    return bool(ok), d


def parity_summary(details, tol=POSTERIOR_TOL):
    n_b = sum(x["n_proto"] for x in details)
    dps = [x["max_posterior_diff"] for x in details if x["max_posterior_diff"] is not None]
    dss = [x["max_posterior_single_diff"] for x in details if x["max_posterior_single_diff"] is not None]
    bad = [x for x in details if not x["ok"]]
    out = {"n_frames": len(details), "n_bodies": n_b, "n_frames_with_bodies": sum(1 for x in details if x["n_proto"]),
           "tolerance": tol,
           "max_posterior_diff": max(dps) if dps else None, "max_posterior_single_diff": max(dss) if dss else None,
           "box_mismatch_frames": sum(1 for x in details if not x["boxes_equal"]),
           "name_mismatch_frames": sum(1 for x in details if not x["names_equal"]),
           "single_mismatch_frames": sum(1 for x in details if not x["single_equal"]),
           "abstain_mismatch_frames": sum(1 for x in details if not x["abstain_equal"]),
           "posterior_missing_frames": sum(1 for x in details if x.get("posterior_missing")),
           "n_failed": len(bad), "failures": bad[:20]}
    # a parity check over frames with no body in them checks nothing about the namer, so it cannot pass
    out["vacuous"] = n_b == 0
    out["passed"] = bool(details) and not bad and not out["vacuous"]
    return out


# ------------------------------------------------------------------------------------------------ the prototype's output

def _norm(p):
    return os.path.normpath(os.path.expanduser(str(p))) if p else None


def read_pred_dir(d):
    """(meta, [records in the prototype's own order]) for one level_prototype output directory."""
    d = Path(os.path.expanduser(str(d)))
    mp = d / "prototype_meta.json"
    if not mp.exists():
        raise SystemExit(f"{d}: no prototype_meta.json -- not a tools/level_prototype.py output directory")
    meta = json.load(open(mp, encoding="utf-8"))
    rp = d / "prototype_results.json"
    if rp.exists():
        recs = json.load(open(rp, encoding="utf-8"))
    else:  # a run still in progress, or one that died before its summary: the per-image records
        recs = [json.load(open(f, encoding="utf-8")) for f in sorted(d.glob("*.json"))
                if f.name not in ("prototype_meta.json", "prototype_results.json")]
    out = []
    for r in recs:
        if isinstance(r, dict) and r.get("image") and not r.get("error"):
            r["_stem"] = Path(r["image"]).stem; r["_pred_dir"] = str(d)
            out.append(r)
    out.sort(key=lambda r: r["_stem"])
    return meta, out


def settings_from_meta(metas, shas):
    """Check every prototype output against the weights loaded here and take the settings its meta records.

    Refused: a different detector, level model or head by sha256; the orientation net (its turn is not timed
    here and its boxes are in the turned frame); a box detector (no corners, a different stage 2); a run without
    --dump-posterior (the posterior half of the gate cannot be checked); outputs that disagree among themselves on
    the histogram match, the flip-TTA, the rare penalty or the level order."""
    seen = {}
    for d, m in metas.items():
        ws = m.get("weights_sha256") if isinstance(m.get("weights_sha256"), dict) else {}
        rec = {"detector": ws.get("detector") or m.get("detector_sha256"),
               "level_model": ws.get("level_model") or m.get("level_model_sha256"),
               "head": ws.get("head")}
        for role, s in rec.items():
            if s and shas.get(role) and s != shas[role]:
                raise SystemExit(f"{d}: the prototype ran {role} sha256 {s[:16]}, this run loaded {shas[role][:16]} "
                                 f"-- parity against a different model is meaningless; pass the same weights")
        if not m.get("head_active"):
            raise SystemExit(f"{d}: the prototype ran without a recurrent head; this timer times the reported "
                             "pipeline, which has one (plan section 0)")
        if m.get("orientation"):
            raise SystemExit(f"{d}: the prototype ran the orientation net ({m['orientation']}); rerun it with "
                             "--no-orient (plan section 0) -- that stage is not timed here")
        if ws.get("box_detector"):
            raise SystemExit(f"{d}: the prototype ran a box detector; this timer times the keypoint detector")
        if not m.get("dump_posterior"):
            raise SystemExit(f"{d}: the prototype ran without --dump-posterior, so the posterior half of the parity "
                             "gate cannot be checked; rerun it with --dump-posterior")
        if m.get("level_order") and list(m["level_order"]) != list(LEVEL_ORDER):
            raise SystemExit(f"{d}: the prototype's level_order differs from make_context_crops.LEVEL_ORDER")
        # read as recorded, never defaulted: a meta that does not say whether the flip-TTA ran cannot be reproduced
        if "tta" not in m or "rare_penalty" not in m:
            raise SystemExit(f"{d}: the prototype meta does not record {'tta' if 'tta' not in m else 'rare_penalty'}; "
                             "what it ran cannot be reproduced here")
        cur = {"hist_match": _norm(m.get("hist_match")), "tta": bool(m["tta"]),
               "rare_penalty": float(m["rare_penalty"])}
        for k, v in cur.items():
            if k in seen and seen[k][0] != v:
                raise SystemExit(f"prototype outputs disagree on {k}: {seen[k][1]} has {seen[k][0]!r}, {d} has {v!r}")
            seen.setdefault(k, (v, d))
        unrecorded = [r for r, s in rec.items() if not s]
        if unrecorded:
            print(f"  note: {d} records no sha256 for {unrecorded}; the parity gate alone binds those weights", flush=True)
    return {k: v[0] for k, v in seen.items()}


def _same_path(p, q):
    return bool(p) and bool(q) and os.path.realpath(_norm(p)) == os.path.realpath(_norm(q))


def primary_deviations(st, weights=()):
    """What makes this run something other than plan section 0's primary arm -> [reason, ...] (empty: primary).

    st: settings_from_meta's result. weights: [(role, path loaded here, primary path)]. Parity cannot catch any of
    these -- the timer takes them from the prototype's meta and reproduces them faithfully -- so a prototype run
    without the histogram match or the flip-TTA would pass the gate and publish a faster latency as the pipeline's."""
    out = []
    if st.get("tta") is not True:
        out.append("flip-TTA off (the prototype ran --no-tta)")
    if not st.get("hist_match"):
        out.append("no histogram match (the prototype's --hist-match was '' or its directory was not on the node)")
    elif not _same_path(st["hist_match"], DEF_HIST_MATCH):
        out.append(f"histogram match to {st['hist_match']}, not {DEF_HIST_MATCH}")
    if st.get("rare_penalty") != DEF_RARE_PENALTY:
        out.append(f"rare penalty {st.get('rare_penalty')}, not {DEF_RARE_PENALTY}")
    for role, p, want in weights:
        if not _same_path(p, want):
            out.append(f"{role} {p}, not the primary stack's {want}")
    return out


def proto_gpu(meta):
    """The GPU a prototype output ran on, when its meta records one, else None."""
    for k in PROTO_GPU_KEYS:
        if meta.get(k):
            return str(meta[k])
    return None


def gpu_check(this_gpu, metas):
    """This run's GPU against every prototype output's -> record. status: "same" (every recorded GPU is this one),
    "differs" (none is), "mixed" (some are; the frames of the others are expected to fail the posterior gate),
    "unrecorded" (no meta records one), "cpu" (this run has no GPU)."""
    per = {d: proto_gpu(m) for d, m in metas.items()}
    rec = {"this_run": this_gpu, "prototype": per}
    known = {g for g in per.values() if g}
    if this_gpu is None:
        rec["status"] = "cpu"
    elif not known:
        rec["status"] = "unrecorded"
        rec["note"] = ("no prototype meta records its GPU; the partition pin of slurm/cine_latency.sh and of the "
                       "cine_infer_* jobs is the only control, and a posterior-only parity failure should be checked "
                       "against the prototype job's log first")
    elif known == {this_gpu}:
        rec["status"] = "same"
    elif this_gpu not in known:
        rec["status"] = "differs"
    else:
        rec["status"] = "mixed"
    rec["unrecorded_dirs"] = sum(1 for g in per.values() if not g)
    return rec


def out_names(dev):
    """The files a run writes under their canonical names. A CPU smoke run has its own, so it can neither publish a
    latency.json nor move a published one aside."""
    base = "latency" if dev == "cuda" else "latency_cpu_smoke"
    return {"json": f"{base}.json", "frames": f"{base}_frames.csv", "failed": f"{base}_parity_failed.json"}


def write_atomic(path, write):
    """write(fh) into <path>.tmp, then rename over <path>: a crash mid-write leaves no half file under the name."""
    path = Path(path); tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as fh:
        write(fh)
    os.replace(tmp, path)


def per_frame_ms(rows, key="end_to_end_ms"):
    """{stem: median over passes of that frame's `key`}: what tools/cine_eval.py video --latency draws in the HUD."""
    by = {}
    for x in rows:
        by.setdefault(x["stem"], []).append(x[key])
    return {s: round(float(np.median(v)), 3) for s, v in sorted(by.items())}


def build_stream(pred_dirs, max_frames=0, seq_re=SEQ_RE):
    """Frames in cine order: pred directories sorted, frames by stem within each, each tagged with its sequence."""
    metas, stream = {}, []
    for d in pred_dirs:
        if max_frames and len(stream) >= max_frames:
            break                                 # 252 Bournemouth shards are not parsed to time the first ten
        meta, recs = read_pred_dir(d)
        metas[str(Path(os.path.expanduser(d)))] = meta
        for r in recs:
            r["_seq"] = f"{Path(r['_pred_dir']).name}/{seq_of(r['_stem'], seq_re)}"
            stream.append(r)
    if max_frames and len(stream) > max_frames:
        stream = stream[:max_frames]
    return metas, stream


def set_aside(p):
    """Move an earlier run's file out of the way (never delete it), so what is left under the canonical name is this
    run's. The name keeps its stem (latency_parity_failed_superseded_<t>.json is never mistaken for a superseded
    published latency.json)."""
    p = Path(p)
    if p.exists():
        q = p.with_name(f"{p.stem}_superseded_{time.strftime('%Y%m%d_%H%M%S')}{p.suffix}")
        p.rename(q)
        print(f"  note: an earlier {p.name} was moved aside to {q.name}", flush=True)


def spread(n, k):
    """k indices evenly spaced over range(n) (all of them when n <= k)."""
    if n <= k:
        return list(range(n))
    return sorted({int(round(x)) for x in np.linspace(0, n - 1, k)})


# ------------------------------------------------------------------------------------------------ the tracker

class NoTracker:
    """NO-OP STAND-IN, NOT A TRACKER. Used only when tools/cine_eval.py, its Tracker or the committed
    tracker_config.json is missing or does not meet the contract (load_tracker says which), so stage 5 costs
    nothing and is reported with that status. The end-to-end figure is then `end_to_end_excluding_tracker` and no
    real-time verdict is issued; do not quote an end-to-end number from a run that used this."""
    implemented = False

    def step(self, dets):
        return None

    update = step


def track_dets(boxes, confs, corners, kpconf, p_blend, names, abstain, pj):
    """One frame's detections in the shape tools/cine_eval.run_tracker builds from a prototype record (box as floats,
    corners, posterior, level, abstain, level_prob), plus the detector's confidences. Built inside the clock: it is
    part of what the tracker stage costs."""
    return [{"box": [float(v) for v in boxes[j]], "det_conf": confs[j], "corners": corners[j], "corner_conf": kpconf[j],
             "posterior": p_blend[j], "level": names[j], "abstain": abstain[j], "level_prob": pj[j]}
            for j in range(len(boxes))]


def load_tracker(config_path, fps):
    """-> (factory or None, record). factory() returns the per-frame call of a NEW tools/cine_eval.py Tracker, one per
    sequence.

    CONTRACT (tools/cine_eval.py track): `Tracker(config: dict, fps: float)` with `.step(dets) -> per-frame
    entries`, `dets` this frame's detections top to bottom as track_dets builds them. `.update` is accepted when
    there is no `.step`. The config is read with cine_eval's own load_tracker_config when it has one (it checks the
    constants are all there), so `config_sha256` is recorded in its "sha256:<hex>" form and compares directly with
    the `config_sha256` of a track.json. The contract is probed once, on a two-body frame of the timed loop's shape
    (float32 posterior rows, corners None) stepped three times, before anything is timed; a module that does not
    meet it is reported `interface_mismatch` with the error, and stage 5 falls back to the no-op -- it is never
    guessed around inside the timed loop."""
    rec = {"config": config_path, "config_sha256": None}
    if config_path and Path(config_path).is_file():
        rec["config_sha256"] = "sha256:" + sha(config_path)
    try:
        import cine_eval as CE  # noqa: F401
    except ImportError as e:
        rec.update(status="not_implemented", why=f"tools/cine_eval.py is not importable ({e}); stage 5 is a no-op")
        return None, rec
    T = getattr(CE, "Tracker", None)
    if T is None:
        rec.update(status="not_implemented", why="tools/cine_eval.py exposes no Tracker; stage 5 is a no-op")
        return None, rec
    if not rec["config_sha256"]:
        rec.update(status="not_implemented", why=f"tracker config {config_path} is not a file; the tracker's "
                                                 "constants are frozen in it (plan 1b) and it is not run without them")
        return None, rec
    try:
        if hasattr(CE, "load_tracker_config"):
            cfg, csha, _ = CE.load_tracker_config(config_path)
            rec["config_sha256"] = csha
        else:
            cfg = json.load(open(config_path, encoding="utf-8"))
    except (Exception, SystemExit) as e:  # noqa: BLE001  (cine_eval refuses an incomplete config with SystemExit)
        rec.update(status="config_invalid", why=f"{config_path}: {type(e).__name__}: {e}; stage 5 is a no-op")
        return None, rec
    C = len(LEVEL_ORDER)
    p = np.full(C, 1e-3, np.float32); p[LEVEL_ORDER.index("C4")] = 1 - 1e-3 * (C - 1)
    q = np.full(C, 1e-3, np.float32); q[LEVEL_ORDER.index("C5")] = 1 - 1e-3 * (C - 1)
    P = np.stack([p, q])
    dummy = track_dets([[100, 100, 160, 150], [100, 170, 160, 220]], [0.9, 0.9], [None, None], [None, None], P,
                       ["C4", "C5"], [False, False], [float(p.max()), float(q.max())])
    method = None
    try:
        t = T(cfg, fps=fps)
        method = next((m for m in ("step", "update") if callable(getattr(t, m, None))), None)
        if method is None:
            raise AttributeError("the Tracker has neither .step nor .update")
        for _ in range(3):
            got = getattr(t, method)(dummy)
    except (Exception, SystemExit) as e:  # noqa: BLE001  (cine_eval raises SystemExit on a detection it cannot use)
        rec.update(status="interface_mismatch", method=method,
                   why=f"cine_eval.Tracker(config, fps).{method or 'step'}(dets) failed on a probe frame: "
                       f"{type(e).__name__}: {e}; stage 5 is a no-op")
        return None, rec
    probe = None
    if isinstance(got, list):
        probe = [e.get("name_tracked") for e in got if isinstance(e, dict) and e.get("det_index") is not None]
    rec.update(status="cine_eval.Tracker", method=method, module=str(Path(CE.__file__).resolve()),
               module_sha256=sha(CE.__file__), probe_names_tracked=probe)
    return (lambda: getattr(T(cfg, fps=fps), method)), rec


# ------------------------------------------------------------------------------------------------ hardware

def nvidia_smi(query, apps=False):
    try:
        cmd = ["nvidia-smi", f"--query-{'compute-apps' if apps else 'gpu'}={query}", "--format=csv,noheader"]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()] if r.returncode == 0 else None
    except Exception:  # noqa: BLE001
        return None


def gpu_uuid(torch):
    """This process's GPU as nvidia-smi names it (GPU-<uuid>), or None. A node shows every job's processes; only
    the ones on OUR device contend with the clock."""
    try:
        u = str(torch.cuda.get_device_properties(0).uuid)
        return u if u.startswith("GPU-") else f"GPU-{u}"
    except Exception:  # noqa: BLE001
        return None


def gpu_state(uuid=None):
    """Who else is on the GPU. A latency measured beside another job's kernels is an upper bound, and nothing
    else in the output would say so. `n_apps_on_this_gpu` counts compute processes on this process's device
    (this process is one of them); None when the device cannot be identified."""
    gpus = nvidia_smi("index,uuid,utilization.gpu,memory.used,memory.total")
    apps = nvidia_smi("gpu_uuid,pid,process_name,used_memory", apps=True)
    mine = [g for g in gpus or [] if uuid and uuid in g]
    n_here = sum(1 for x in apps or [] if uuid and x.startswith(uuid)) if (uuid and apps is not None) else None
    return {"gpu_uuid": uuid, "this_gpu": mine or None, "all_gpus": gpus, "compute_apps": apps,
            "n_apps_on_this_gpu": n_here}


def hardware_record(torch):
    try:
        from eval_runtime_cost import hardware  # the repository's record of a machine, reused as is
        hw = hardware(torch)
    except Exception as e:  # noqa: BLE001
        hw = {"host": platform.node(), "platform": platform.platform(), "python": platform.python_version(),
              "torch": torch.__version__, "hardware_record_error": f"{type(e).__name__}: {e}"}
    hw["nvidia_smi_name_driver"] = nvidia_smi("name,driver_version")
    try:
        import ultralytics
        hw["ultralytics"] = ultralytics.__version__
    except Exception:  # noqa: BLE001
        hw["ultralytics"] = None
    hw["numpy"] = np.__version__
    try:
        import PIL
        hw["pillow"] = PIL.__version__
    except Exception:  # noqa: BLE001
        pass
    if torch.cuda.is_available():
        hw["gpu_torch_name"] = torch.cuda.get_device_name(0)
        hw["cudnn"] = torch.backends.cudnn.version()
    # "FP32 as shipped": the flags as they were, recorded rather than set -- on Ampere and later a convolution may
    # run in TF32 under torch's default, and the prototype ran under the same default
    hw["torch_numerics"] = {"cudnn_allow_tf32": bool(torch.backends.cudnn.allow_tf32),
                            "matmul_allow_tf32": bool(torch.backends.cuda.matmul.allow_tf32),
                            "cudnn_benchmark": bool(torch.backends.cudnn.benchmark),
                            "cudnn_deterministic": bool(torch.backends.cudnn.deterministic),
                            "float32_matmul_precision": torch.get_float32_matmul_precision()}
    return hw


def machine_load_record():
    try:
        from eval_runtime_cost import machine_load
        return machine_load(1.0)
    except Exception as e:  # noqa: BLE001
        return {"error": f"{type(e).__name__}: {e}"}


# ------------------------------------------------------------------------------------------------ run

def cmd_run(a) -> int:
    import torch
    import fluorocap_infer as v1
    from sweep_map import Namer
    from level_prototype import load_image

    if torch.cuda.is_available():
        dev = "cuda"
    elif a.allow_cpu:
        dev = "cpu"
        print("  note: no CUDA device; --allow-cpu: this run is a smoke test, publishes no claim and writes "
              "latency_cpu_smoke*, never latency.json", flush=True)
    else:
        raise SystemExit("no CUDA device. The plan's latency is a GPU measurement; pass --allow-cpu only for a smoke "
                         "test (no claim is written from it)")
    this_gpu = torch.cuda.get_device_name(0) if dev == "cuda" else None
    if a.require_gpu and dev == "cuda" and a.require_gpu.lower() not in this_gpu.lower():
        raise SystemExit(f"this job got a {this_gpu}, and --require-gpu is {a.require_gpu!r}: the parity gate is only "
                         "meaningful on the GPU model the prototype ran on (TF32 convolutions differ by architecture); "
                         "submit to that GPU's partition/constraint (slurm/cine_latency.sh)")
    outn = out_names(dev)

    def sync():
        if dev == "cuda":
            torch.cuda.synchronize()

    pred_dirs = []
    for pat in a.pred:
        hits = sorted(glob.glob(os.path.expanduser(pat)))
        pred_dirs += [h for h in hits if os.path.isdir(h)]
    if not pred_dirs:
        raise SystemExit(f"--pred matched no directory: {a.pred}")
    det_p, mod_p, head_p = (os.path.expanduser(x) for x in (a.detector, a.model, a.head))
    for role, p in (("detector", det_p), ("model", mod_p), ("head", head_p)):
        if not Path(p).is_file():
            raise SystemExit(f"--{role} {p} is not a file")
    shas = {"detector": sha(det_p), "level_model": sha(mod_p), "head": sha(head_p)}
    metas, stream = build_stream(pred_dirs, a.max_frames, a.seq_re)
    if len(stream) <= a.warmup:
        raise SystemExit(f"{len(stream)} frames in the stream, not more than the {a.warmup} warm-up frames")
    st = settings_from_meta(metas, shas)
    deviations = primary_deviations(st, [("detector", det_p, DEF_DETECTOR), ("level model", mod_p, DEF_MODEL),
                                         ("head", head_p, DEF_HEAD)])
    if deviations and not a.not_primary:
        raise SystemExit("this is not plan section 0's primary arm: " + "; ".join(deviations) + ". The primary "
                         "pipeline's latency is published only from a prototype run of the primary pipeline; to time "
                         "another arm, pass --not-primary REASON (it is written into latency.json and the claim)")
    arm = {"primary": not deviations and not a.not_primary, "not_primary": a.not_primary or None,
           "deviations": deviations}
    gpu_rec = gpu_check(this_gpu, metas)
    if gpu_rec["status"] == "differs":
        raise SystemExit(f"this job's GPU is {this_gpu}; the prototype outputs record {sorted(set(filter(None, gpu_rec['prototype'].values())))}. "
                         "The 1e-5 posterior gate compares across GPU architectures only by luck; submit this job to "
                         "the prototype's GPU (slurm/cine_latency.sh: partition, --constraint and CINE_GPU)")
    if gpu_rec["status"] == "mixed":
        print(f"  note: the prototype outputs ran on {sorted(set(filter(None, gpu_rec['prototype'].values())))}, this "
              f"job on {this_gpu}; frames from the other GPU are expected to fail the posterior gate "
              "(parity.gpu says which)", flush=True)
    missing = [r["image"] for r in stream if not Path(r["image"]).is_file()]
    if missing:
        raise SystemExit(f"{len(missing)} frames the prototype read are not on disk here, e.g. {missing[0]}")
    out_dir = Path(os.path.expanduser(a.out)); out_dir.mkdir(parents=True, exist_ok=True)
    # from here on this run writes to out_dir: whatever an earlier run left under this run's canonical names goes
    # aside FIRST, so a crash anywhere below cannot leave an earlier latency.json to be read as this run's
    for k in ("json", "frames", "failed"):
        set_aside(out_dir / outn[k])
    print(f"cine_latency: {a.dataset}: {len(pred_dirs)} prototype output(s), {len(stream)} frames, "
          f"{len({r['_seq'] for r in stream})} sequence(s); device {dev} ({this_gpu}); prototype GPU "
          f"{gpu_rec['status']}; arm {'primary' if arm['primary'] else 'NOT PRIMARY: ' + (a.not_primary or '')}",
          flush=True)

    # ---- the models, loaded once and kept resident
    t_load = time.perf_counter()
    from ultralytics import YOLO
    det = YOLO(det_p)
    namer = Namer(mod_p, head_p, dev, tta=st["tta"])
    if namer.head is None:
        raise SystemExit("the head did not load; the reported pipeline has one")
    ref = v1.film_reference_cdf(st["hist_match"]) if st["hist_match"] and Path(st["hist_match"]).exists() else None
    if st["hist_match"] and ref is None:
        raise SystemExit(f"the prototype histogram-matched to {st['hist_match']}, which is not on disk here")
    sync(); load_s = time.perf_counter() - t_load
    make_tracker, trk_rec = load_tracker(a.tracker_config, a.fps)
    tracked = make_tracker is not None
    print(f"  models resident in {load_s:.1f} s; hist ref {'on' if ref is not None else 'off'}; flip-TTA "
          f"{'on' if st['tta'] else 'off'}; tracker: {trk_rec['status']}", flush=True)

    def run_frame(im, step):
        """One frame through stages 1-5 on an already decoded image -> (outputs, stage seconds, end to end).
        step: the sequence's tracker call (load_tracker's factory()), or None (parity frames; the no-op)."""
        t = {}
        sync(); t0 = time.perf_counter()
        if ref is not None:
            im, _ = v1.prepare_panel(im, False, False, hist_ref=ref)
        rgb = np.asarray(im.convert("RGB"))
        sync(); t1 = time.perf_counter(); t["prepare"] = t1 - t0
        res = det.predict(rgb, imgsz=a.imgsz, conf=a.conf, verbose=False)[0]
        boxes, confs, corners, kpconf = boxes_from_keypoints(res)
        sync(); t2 = time.perf_counter(); t["detect"] = t2 - t1
        emb, p_single, p_blend = namer.run(np.asarray(im), boxes, a.tgt_px, a.size, a.rung)
        sync(); t3 = time.perf_counter(); t["name"] = t3 - t2
        names, single, abstain, pj = decode_frame(p_blend, p_single, True, st["rare_penalty"], a.abstain_below)
        t4 = time.perf_counter(); t["decode"] = t4 - t3
        if step is not None:
            step(track_dets(boxes, confs, corners, kpconf, p_blend, names, abstain, pj))
        sync(); t5 = time.perf_counter(); t["track"] = t5 - t4
        o = {"boxes": boxes, "names": names, "single": single, "abstain": abstain, "p_blend": p_blend,
             "p_single": p_single, "size": list(im.size)}
        return o, t, t5 - t0

    # ---- 1. the parity gate, before any latency is measured
    pidx = spread(len(stream), a.parity_frames)
    details, cold_ms = [], None
    for i in pidx:
        r = stream[i]
        o, _, tot = run_frame(load_image(r["image"]), None)
        if cold_ms is None:                       # the first frame after loading: CUDA, cuDNN and predictor set-up
            cold_ms = round(tot * 1000, 3)
        d = compare_frame(r, o)[1]
        d["proto_gpu"] = gpu_rec["prototype"].get(r["_pred_dir"])
        details.append(d)
    par = parity_summary(details)
    fails_by_gpu = {}
    for d in details:
        if not d["ok"]:
            k = d["proto_gpu"] or "unrecorded"; fails_by_gpu[k] = fails_by_gpu.get(k, 0) + 1
    par["gpu"] = {**gpu_rec, "failed_frames_by_prototype_gpu": fails_by_gpu}
    ref_info = {d: {"eval_gate_held_out": (m.get("eval_gate") or {}).get("held_out"),
                    "not_held_out_reason": (m.get("eval_gate") or {}).get("not_held_out_reason"),
                    "weights_sha256": m.get("weights_sha256")} for d, m in metas.items()}
    result = {"tool": "tools/cine_latency.py", "code_sha": code_sha(), "written": now_iso(), "dataset": a.dataset,
              "pred_dirs": pred_dirs, "device": dev, "gpu": this_gpu, "arm": arm,
              "weights": {"detector": det_p, "level_model": mod_p, "head": head_p}, "weights_sha256": shas,
              "settings": {"imgsz": a.imgsz, "conf": a.conf, "tgt_px": a.tgt_px, "size": a.size, "rung": a.rung,
                           "abstain_below": a.abstain_below, "batch": 1, "precision": "fp32 (torch defaults, recorded)",
                           "direction_known": True, "hist_ref_sha256": (hashlib.sha256(np.asarray(ref).tobytes()).hexdigest()
                                                                        if ref is not None else None),
                           **st, "taken_from_prototype_meta": sorted(st),
                           "warmup_frames": a.warmup, "passes": a.passes, "fps": a.fps, "seq_re": a.seq_re},
              "parity_reference": ref_info, "parity": {**par, "frames": [stream[i]["_stem"] for i in pidx]},
              "tracker": trk_rec, "excluded": EXCLUDED, "not_claimable": NOT_CLAIMABLE, "model_load_s": round(load_s, 2),
              "cold_first_frame_ms": cold_ms}
    print(f"  parity: {par['n_frames']} frames, {par['n_bodies']} bodies; boxes off on {par['box_mismatch_frames']}, "
          f"names off on {par['name_mismatch_frames']}, abstain off on {par['abstain_mismatch_frames']}; max |dp| "
          f"{par['max_posterior_diff']} (single {par['max_posterior_single_diff']}) -> "
          f"{'PASSED' if par['passed'] else 'FAILED'}", flush=True)
    if not par["passed"]:
        # the GPU this ran on goes into the record even without a timing: one cause to TEST (not a conclusion) when
        # boxes and names agree and only posteriors drift is a different GPU model from the prototype run's --
        # torch's default TF32 convolutions accumulate differently across architectures. parity.gpu says which GPU
        # each prototype output recorded, or that none did (then the prototype job's log says).
        result.update(timing=None, claim=None, hardware=hardware_record(torch),
                      why_no_timing="the parity gate failed: this timer is not provably the prototype's pipeline, so "
                                    "no latency is published (plan 1c)")
        write_atomic(out_dir / outn["failed"], lambda fh: json.dump(result, fh, indent=1))
        for f in par["failures"][:5]:
            print(f"    {f}", flush=True)
        print(f"  prototype GPU {gpu_rec['status']}; failed frames by prototype GPU {fails_by_gpu}", flush=True)
        print(f"PARITY_FAILED -> {out_dir / outn['failed']} (no latency written)", flush=True)
        return 3

    # ---- 2. the timed stream
    hw = hardware_record(torch)
    uuid = gpu_uuid(torch) if dev == "cuda" else None
    load0, gpu0 = machine_load_record(), gpu_state(uuid)
    if dev == "cuda":
        torch.cuda.reset_peak_memory_stats()
    rows, times, e2e, t_png = [], {s: [] for s in STAGES}, [], []
    n_run, tparity_bad, tparity_n = 0, [], 0
    for ps in range(a.passes):
        step, cur = None, None
        for r in stream:
            if r["_seq"] != cur:                  # a new sequence starts a new tracker (outside the clock)
                cur = r["_seq"]; step = make_tracker() if tracked else None
            tl = time.perf_counter(); im = load_image(r["image"]); tl = time.perf_counter() - tl
            o, t, tot = run_frame(im, step)
            n_run += 1
            if n_run <= a.warmup:
                continue
            ok, d = compare_frame(r, o)           # after the clock: is every timed frame still the prototype's?
            tparity_n += 1
            if not ok:
                tparity_bad.append(d)
            for s in STAGES:
                times[s].append(t[s] * 1000)
            e2e.append(tot * 1000); t_png.append(tl * 1000)
            rows.append({"pass": ps, "seq": r["_seq"], "stem": r["_stem"], "width": o["size"][0], "height": o["size"][1],
                         "bodies": len(o["boxes"]), "load_png_ms": round(tl * 1000, 3),
                         **{f"{s}_ms": round(t[s] * 1000, 3) for s in STAGES}, "end_to_end_ms": round(tot * 1000, 3),
                         "parity_ok": ok})
    load1, gpu1 = machine_load_record(), gpu_state(uuid)
    peak_mb = round(torch.cuda.max_memory_allocated() / 1e6, 1) if dev == "cuda" else None

    stages = {"load_png": {**summ(t_png), "in_end_to_end": False}}
    for s in STAGES:
        stages[s] = summ(times[s])
    if not tracked:
        stages["track"] = {"status": trk_rec["status"], "why": trk_rec["why"],
                           "note": "no-op stand-in (NoTracker); its clock reads ~0 and is not reported as a tracker cost"}
    e2e_key = "end_to_end" if tracked else "end_to_end_excluding_tracker"
    e2e_s = summ(e2e)
    budget = round(sum(stages[s]["p50_ms"] for s in STAGES if "p50_ms" in stages[s]), 3)
    bodies = np.asarray([x["bodies"] for x in rows])
    by_bodies = {int(k): {"n_frames": int((bodies == k).sum()),
                          **{kk: v for kk, v in summ([x["end_to_end_ms"] for x in rows if x["bodies"] == k]).items()
                             if kk in ("p50_ms", "p95_ms", "max_ms")}} for k in sorted(set(bodies.tolist()))}
    sizes = {}
    for x in rows:
        k = f"{x['width']}x{x['height']}"; sizes[k] = sizes.get(k, 0) + 1
    caveats = []
    busy = (load0.get("other_busy_processes") or []) + (load1.get("other_busy_processes") or [])
    if busy:
        caveats.append("other processes were busy on this host during the run (machine_load_*); treat the figures "
                       "as an upper bound")
    if any((g.get("n_apps_on_this_gpu") or 0) > 1 for g in (gpu0, gpu1)):
        caveats.append("another compute process shared this GPU (gpu_state_*); treat the figures as an upper bound")
    elif dev == "cuda" and any(g.get("n_apps_on_this_gpu") is None for g in (gpu0, gpu1)):
        caveats.append("whether another process shared this GPU could not be read (gpu_state_*)")
    if tparity_bad:
        caveats.append(f"{len(tparity_bad)} of {tparity_n} timed frames did not reproduce the prototype's output "
                       "exactly (timed_parity); the 50-frame gate passed")
    budget_ms = round(1000.0 / a.fps, 2) if a.fps else None
    gpu_name = hw.get("gpu_torch_name") or (hw.get("nvidia_smi_name_driver") or ["?"])[0]
    claim = None
    if dev == "cuda":
        label = "" if arm["primary"] else f"Non-primary arm ({a.not_primary}; {'; '.join(deviations) or 'as declared'}): "
        claim = {"sentence": (f"{label}Per-frame compute on {gpu_name}, models resident, batch 1, excluding acquisition, "
                              f"DICOM decode and display"
                              f"{'' if tracked else ', and excluding the tracker (not timed: ' + trk_rec['status'] + ')'}: "
                              f"p50 {e2e_s['p50_ms']:.1f} ms, p95 {e2e_s['p95_ms']:.1f} ms."),
                 "primary_arm": arm["primary"],
                 "fps": a.fps, "frame_budget_ms": budget_ms,
                 "realtime_at_fps": (bool(e2e_s["p95_ms"] < budget_ms) if (tracked and budget_ms) else None),
                 "why_no_realtime_verdict": (None if tracked else "the tracker stage is a no-op here; a real-time claim "
                                             "needs the whole causal pipeline timed"),
                 "p95_within_budget_excluding_tracker": (bool(e2e_s["p95_ms"] < budget_ms)
                                                         if (not tracked and budget_ms) else None)}
    else:
        caveats.append("CPU run (--allow-cpu): a smoke test; no claim is made from it (plan 1c)")
    result.update({
        "hardware": hw, "machine_load_at_start": load0, "machine_load_at_end": load1,
        "gpu_state_at_start": gpu0, "gpu_state_at_end": gpu1, "gpu_peak_allocated_mb": peak_mb,
        "timing": {"n_frames_run": n_run, "n_frames_timed": len(rows),
                   "stages": stages, e2e_key: e2e_s,
                   "additive_budget_p50_ms": budget,
                   "ratio_p50_clock_to_budget": (round(e2e_s["p50_ms"] / budget, 4) if budget else None),
                   "by_bodies_per_frame": by_bodies},
        "frames": {"size": sizes, "bodies_per_frame": {"mean": round(float(bodies.mean()), 3),
                                                       "p50": float(np.median(bodies)), "min": int(bodies.min()),
                                                       "max": int(bodies.max())},
                   "n_sequences": len({x["seq"] for x in rows})},
        "timed_parity": {"n_frames": tparity_n, "n_mismatch": len(tparity_bad), "mismatches": tparity_bad[:20]},
        "claim": claim, "caveats": caveats,
        # what tools/cine_eval.py video --latency draws in the HUD ({stem: ms}); every row is in the frames CSV
        "per_frame_measure": e2e_key,
        "per_frame_definition": (f"{e2e_key} ms of each timed frame, median over the {a.passes} pass(es); the first "
                                 f"{a.warmup} frames of pass 0 are warm-up and untimed"),
        # a stem timed under two sequences (two pred directories holding one frame) would pool into one HUD value
        "per_frame_stem_collision": len({x["stem"] for x in rows}) != len({(x["seq"], x["stem"]) for x in rows}),
        "per_frame": per_frame_ms(rows)})

    def write_rows(fh):
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    # the frames CSV first, latency.json LAST, both atomically: latency.json exists only once everything is written
    write_atomic(out_dir / outn["frames"], write_rows)
    write_atomic(out_dir / outn["json"], lambda fh: json.dump(result, fh, indent=1))
    print(f"  {len(rows)} frames timed after {a.warmup} warm-up; {e2e_key}: p50 {e2e_s['p50_ms']} ms, "
          f"p95 {e2e_s['p95_ms']} ms, max {e2e_s['max_ms']} ms (stage-median budget {budget} ms)", flush=True)
    for s in STAGES:
        v = stages[s]
        print(f"    {s:8s} " + (f"p50 {v['p50_ms']:8.2f}  p95 {v['p95_ms']:8.2f}  max {v['max_ms']:8.2f} ms"
                                if "p50_ms" in v else f"{v.get('status')}"), flush=True)
    if claim:
        print(f"  {claim['sentence']}", flush=True)
    for c in caveats:
        print(f"  caveat: {c}", flush=True)
    print(f"CINE_LATENCY_DONE -> {out_dir / outn['json']}", flush=True)
    return 0


# ------------------------------------------------------------------------------------------------ self-test

def cmd_self_test(a) -> int:
    """The parts that decide whether a number is published, checked on inputs whose answer is known."""
    fails = []

    def check(name, cond, got=None):
        print(f"  {'ok  ' if cond else 'FAIL'} {name}" + ("" if cond else f"  (got {got})"))
        if not cond:
            fails.append(name)

    s = summ(list(range(1, 101)))
    check("summ p50 of 1..100 is 50.5", s["p50_ms"] == 50.5, s)
    check("summ p95 of 1..100 is 95.05", s["p95_ms"] == 95.05, s)
    check("summ max of 1..100 is 100", s["max_ms"] == 100.0, s)
    check("summ of nothing reports n 0", summ([]) == {"n": 0})
    for stem, want in (("HV01a_flex_f0012", "HV01a_flex"), ("P07b_ext_f0300", "P07b_ext"), ("case134_sw012", "case134"),
                       ("case39_sw300", "case39"), ("ctsp_0533_lat_p030", "ctsp_0533_lat"), ("oddname", "oddname")):
        check(f"sequence of {stem} is {want}", seq_of(stem) == want, seq_of(stem))
    check("spread 50 over 301 frames: 50 distinct, ends included",
          (lambda x: len(x) == 50 and x[0] == 0 and x[-1] == 300)(spread(301, 50)), spread(301, 50)[:5])
    check("spread over fewer frames than asked takes them all", spread(7, 50) == list(range(7)))

    # stage 4 on a run whose answer is known: four bodies peaked on C3..C6
    C = len(LEVEL_ORDER)

    def peaked(names, w=0.9):
        p = np.full((len(names), C), (1 - w) / (C - 1))
        for j, n in enumerate(names):
            p[j, LEVEL_ORDER.index(n)] = w
        return p
    pb = peaked(["C3", "C4", "C5", "C6"]); pss = pb.copy()
    names, single, abst, pj = decode_frame(pb, pss)
    check("decode C3..C6 run", names == ["C3", "C4", "C5", "C6"], names)
    check("no abstain when decode, single crop and probability agree", abst == [False] * 4, abst)
    pss2 = peaked(["C3", "C4", "C7", "C6"])
    _, single2, abst2, _ = decode_frame(pb, pss2)
    check("abstain where the single-crop name differs from the decoded one", abst2 == [False, False, True, False], abst2)
    _, _, abst3, _ = decode_frame(peaked(["C3", "C4", "C5", "C6"], w=0.45), peaked(["C3", "C4", "C5", "C6"], w=0.45))
    check("abstain below 0.5 even when the names agree", abst3 == [True] * 4, abst3)
    check("empty frame decodes to nothing", decode_frame(np.zeros((0, C)), np.zeros((0, C))) == ([], [], [], []))

    # the parity comparison: a record written the way level_prototype writes it, then perturbed
    boxes = [[100, 100, 160, 150], [102, 170, 163, 222], [104, 240, 166, 293], [105, 310, 168, 365]]
    rnd = lambda v: [float(f"{float(x):.6g}") for x in v]  # noqa: E731  (the prototype's six significant digits)
    rec = {"_stem": "HV01a_flex_f0001",
           "vertebrae": [{"box": b, "level": names[j], "single_crop": single[j], "abstain": abst[j],
                          "posterior": rnd(pb[j]), "posterior_single": rnd(pss[j])} for j, b in enumerate(boxes)]}
    out = {"boxes": [list(b) for b in boxes], "names": names, "single": single, "abstain": abst, "p_blend": pb,
           "p_single": pss}
    ok, d = compare_frame(rec, out)
    check("identical frame passes (six-digit rounding inside 1e-5)", ok and d["max_posterior_diff"] < 1e-6, d)
    o2 = dict(out, boxes=[list(b) for b in boxes]); o2["boxes"][2] = [104, 240, 166, 294]
    ok, d = compare_frame(rec, o2)
    check("a box one pixel off fails", (not ok) and not d["boxes_equal"], d)
    o3 = dict(out, names=["C3", "C5", "C4", "C6"])
    ok, d = compare_frame(rec, o3)
    check("two names swapped fail", (not ok) and not d["names_equal"], d)
    o4 = dict(out, p_blend=pb + np.eye(1, C * 4, 7).reshape(4, C) * 2e-5)
    ok, d = compare_frame(rec, o4)
    check("a posterior entry 2e-5 off fails", (not ok) and d["max_posterior_diff"] > 1e-5, d)
    o5 = dict(out, p_single=pss + np.eye(1, C * 4, 30).reshape(4, C) * 2e-6)
    ok, d = compare_frame(rec, o5)
    check("a single-crop entry 2e-6 off passes", ok, d)
    o6 = dict(out, abstain=[False, True, False, False])
    ok, d = compare_frame(rec, o6)
    check("an abstain flag flipped fails", (not ok) and not d["abstain_equal"], d)
    rec_np = {"_stem": "x", "vertebrae": [{k: v for k, v in x.items() if k != "posterior"} for x in rec["vertebrae"]]}
    ok, d = compare_frame(rec_np, out)
    check("a record without posteriors fails (cannot be checked)", (not ok) and d.get("posterior_missing"), d)
    ok, d = compare_frame({"_stem": "empty", "vertebrae": []}, {"boxes": [], "names": [], "single": [], "abstain": [],
                                                                "p_blend": [], "p_single": []})
    check("an empty frame matches an empty record", ok, d)
    ps = parity_summary([d])
    check("parity over frames with no body is vacuous and does not pass", ps["vacuous"] and not ps["passed"], ps)
    ps = parity_summary([compare_frame(rec, out)[1], compare_frame(rec, o3)[1]])
    check("one bad frame fails the gate", (not ps["passed"]) and ps["name_mismatch_frames"] == 1, ps)
    ps = parity_summary([compare_frame(rec, out)[1]] * 3)
    check("clean frames pass the gate", ps["passed"] and ps["n_bodies"] == 12, ps)

    # the meta check refuses what would make parity meaningless or the timing a different pipeline
    shas = {"detector": "a" * 64, "level_model": "b" * 64, "head": "c" * 64}
    good = {"weights_sha256": dict(shas), "head_active": True, "orientation": None, "dump_posterior": True,
            "level_order": LEVEL_ORDER, "hist_match": "~/films_drr", "tta": True, "rare_penalty": 1.0}
    got = settings_from_meta({"d1": good, "d2": good}, shas)
    check("matching metas give their settings", got["tta"] is True and got["rare_penalty"] == 1.0
          and got["hist_match"] == os.path.normpath(os.path.expanduser("~/films_drr")), got)
    for why, bad in (("a different head", {**good, "weights_sha256": {**shas, "head": "d" * 64}}),
                     ("the orientation net", {**good, "orientation": "/x/orientation_net.pt"}),
                     ("no --dump-posterior", {**good, "dump_posterior": False}),
                     ("no head", {**good, "head_active": False}),
                     ("a box detector", {**good, "weights_sha256": {**shas, "box_detector": "e" * 64}})):
        try:
            settings_from_meta({"d": bad}, shas); refused = False
        except SystemExit:
            refused = True
        check(f"meta check refuses {why}", refused)
    try:
        settings_from_meta({"d1": good, "d2": {**good, "tta": False}}, shas); refused = False
    except SystemExit:
        refused = True
    check("meta check refuses outputs that disagree on the flip-TTA", refused)
    try:
        settings_from_meta({"d": {k: v for k, v in good.items() if k != "tta"}}, shas); refused = False
    except SystemExit:
        refused = True
    check("meta check refuses a meta that does not record the flip-TTA (never defaulted)", refused)

    # the primary arm (plan section 0): a lighter pipeline passes parity, so it is refused here unless declared
    W = [("detector", DEF_DETECTOR, DEF_DETECTOR), ("level model", DEF_MODEL, DEF_MODEL), ("head", DEF_HEAD, DEF_HEAD)]
    prim = {"hist_match": _norm(DEF_HIST_MATCH), "tta": True, "rare_penalty": 1.0}
    check("the primary settings deviate in nothing", primary_deviations(prim, W) == [], primary_deviations(prim, W))
    for why, st_bad, w_bad, key in (("flip-TTA off", {**prim, "tta": False}, W, "flip-TTA"),
                                    ("no histogram match", {**prim, "hist_match": None}, W, "no histogram match"),
                                    ("another reference", {**prim, "hist_match": "/x/other_films"}, W, "/x/other_films"),
                                    ("rare penalty 2", {**prim, "rare_penalty": 2.0}, W, "rare penalty"),
                                    ("another head", prim, W[:2] + [("head", "/x/head_other.pt", DEF_HEAD)], "head_other")):
        dv = primary_deviations(st_bad, w_bad)
        check(f"not the primary arm: {why}", len(dv) == 1 and key in dv[0], dv)

    # the GPU the prototype ran on against this run's
    g = lambda *n: {f"d{i}": ({"gpu_name": x} if x else {}) for i, x in enumerate(n)}  # noqa: E731
    for want, this, metas_ in (("unrecorded", "NVIDIA H200", g(None, None)), ("same", "NVIDIA H200", g("NVIDIA H200", None)),
                               ("differs", "NVIDIA H200", g("NVIDIA L40S", "NVIDIA L40S")),
                               ("mixed", "NVIDIA H200", g("NVIDIA H200", "Tesla V100-SXM2-32GB")),
                               ("cpu", None, g("NVIDIA H200"))):
        got_g = gpu_check(this, metas_)
        check(f"GPU check: {want}", got_g["status"] == want, got_g)

    # output names, setting aside and writing: nothing an earlier run left can be read as this run's
    import tempfile
    check("a CPU smoke run never writes latency.json", out_names("cpu")["json"] != "latency.json"
          and not set(out_names("cpu").values()) & set(out_names("cuda").values()), out_names("cpu"))
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        for n in out_names("cuda").values():
            (tdp / n).write_text("earlier run")
        for n in out_names("cuda").values():
            set_aside(tdp / n)
        left = sorted(x.name for x in tdp.iterdir())
        check("every canonical file of an earlier run is moved aside", not set(out_names("cuda").values()) & set(left), left)
        check("a set-aside parity failure keeps its tag", any(x.startswith("latency_parity_failed_superseded_") for x in left)
              and any(x.startswith("latency_frames_superseded_") for x in left), left)
        write_atomic(tdp / "latency.json", lambda fh: json.dump({"ok": 1}, fh))
        check("an atomic write leaves the file and no .tmp", json.load(open(tdp / "latency.json")) == {"ok": 1}
              and not list(tdp.glob("*.tmp")), sorted(x.name for x in tdp.iterdir()))
    pf = per_frame_ms([{"stem": "a", "end_to_end_ms": 10.0}, {"stem": "a", "end_to_end_ms": 30.0},
                       {"stem": "a", "end_to_end_ms": 12.0}, {"stem": "b", "end_to_end_ms": 5.0}])
    check("per_frame is {stem: median over passes}", pf == {"a": 12.0, "b": 5.0}, pf)

    # the tracker adapter says what it did, whatever state tools/cine_eval.py is in
    fac, rec_t = load_tracker(DEF_TRACKER_CONFIG, 15.0)
    check("tracker record carries a status", rec_t.get("status") in ("not_implemented", "interface_mismatch",
                                                                     "config_invalid", "cine_eval.Tracker"), rec_t)
    print(f"  tracker status here: {rec_t.get('status')} -- {rec_t.get('why', rec_t.get('module'))}")
    check("NoTracker is a marked no-op", NoTracker.implemented is False and NoTracker().update([]) is None
          and NoTracker().step([]) is None)
    CE = None
    if (Path(__file__).resolve().parent / "cine_eval.py").is_file():
        # cine_eval.py is here, so its tracker must be what stage 5 times: a probe that fails now would make every run
        # report interface_mismatch and never issue the real-time verdict
        try:
            import cine_eval as CE
        except Exception as e:  # noqa: BLE001
            check("tools/cine_eval.py imports in this environment", False, f"{type(e).__name__}: {e}")
    else:
        print("  (tools/cine_eval.py absent: the tracker contract is not checked here)")
    if CE is not None:
        with tempfile.TemporaryDirectory() as td:
            cp = Path(td) / "tracker_config.json"
            json.dump(CE.TRACKER_DEFAULTS, open(cp, "w"), indent=1)
            fac2, rec2 = load_tracker(str(cp), 15.0)
            check("with cine_eval.py and a config, stage 5 is cine_eval's Tracker", rec2.get("status") == "cine_eval.Tracker"
                  and rec2.get("method") == "step", rec2)
            check("the tracker config sha is recorded in cine_eval's sha256:<hex> form, equal to its own",
                  rec2.get("config_sha256") == CE.load_tracker_config(str(cp))[1], rec2.get("config_sha256"))
            if fac2 is not None:
                stp = fac2(); P = np.full((2, C), 1e-3, np.float32)
                P[0, LEVEL_ORDER.index("C4")] = P[1, LEVEL_ORDER.index("C5")] = 1 - 1e-3 * (C - 1)
                for _ in range(3):
                    ent = stp(track_dets([[100, 100, 160, 150], [101, 171, 161, 221]], [0.9, 0.9], [None, None],
                                         [None, None], P, ["C4", "C5"], [False, False], [0.97, 0.97]))
                nm = [e.get("name_tracked") for e in ent if e.get("det_index") is not None]
                check("the timed loop's detections go through cine_eval's Tracker: confirmed C4, C5", nm == ["C4", "C5"], ent)
            json.dump({k: v for k, v in CE.TRACKER_DEFAULTS.items() if k != "max_age_s"}, open(cp, "w"))
            fac3, rec3 = load_tracker(str(cp), 15.0)
            check("an incomplete tracker config is refused, not run on defaults", fac3 is None
                  and rec3.get("status") == "config_invalid", rec3)
        if Path(DEF_TRACKER_CONFIG).is_file():
            check("the committed tracker_config.json gives cine_eval's Tracker", rec_t.get("status") == "cine_eval.Tracker",
                  rec_t)
    print(f"self-test: {'PASSED' if not fails else 'FAILED ' + str(fails)}")
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="parity gate, then the timed stream -> <out>/latency.json")
    r.add_argument("--pred", nargs="+", required=True,
                   help="level_prototype output directories (globs allowed; a sequence-sharded run is pred/*)")
    r.add_argument("--dataset", required=True, help="name written into latency.json (bournemouth_qf, case39, ...)")
    r.add_argument("--out", required=True, help="directory for latency.json and latency_frames.csv")
    r.add_argument("--detector", default=DEF_DETECTOR); r.add_argument("--model", default=DEF_MODEL)
    r.add_argument("--head", default=DEF_HEAD)
    r.add_argument("--imgsz", type=int, default=1024); r.add_argument("--conf", type=float, default=0.35)
    r.add_argument("--tgt-px", type=float, default=96); r.add_argument("--size", type=int, default=320)
    r.add_argument("--rung", type=int, default=1); r.add_argument("--abstain-below", type=float, default=0.5)
    r.add_argument("--fps", type=float, default=15.0,
                   help="the sequence's frame rate, for the frame budget: 15 (Bournemouth, synthetic), 10.3 (C-arm sweep)")
    r.add_argument("--warmup", type=int, default=20, help="frames run and discarded before timing (plan 1c: 20)")
    r.add_argument("--parity-frames", type=int, default=50, help="frames in the parity gate (plan 1c: 50)")
    r.add_argument("--max-frames", type=int, default=0, help="cap the stream (0 = every frame in --pred)")
    r.add_argument("--passes", type=int, default=1,
                   help="times the stream is run; a short cine (60 frames) needs several for a p95 to mean anything. "
                        "The tracker restarts with each pass.")
    r.add_argument("--tracker-config", default=DEF_TRACKER_CONFIG)
    r.add_argument("--seq-re", default=SEQ_RE, help="regex with a (?P<seq>...) group: a frame stem's sequence")
    r.add_argument("--allow-cpu", action="store_true",
                   help="smoke test without a GPU; no claim is written, and the outputs are latency_cpu_smoke*")
    r.add_argument("--require-gpu", default=None,
                   help="refuse unless torch.cuda.get_device_name(0) contains this (case-insensitive), e.g. H200: the "
                        "GPU model the prototype ran on (slurm/cine_latency.sh passes it)")
    r.add_argument("--not-primary", default=None, metavar="REASON",
                   help="time a prototype output that is not plan section 0's primary arm (no histogram match, no "
                        "flip-TTA, another reference, rare penalty or weights); REASON goes into latency.json and the claim")
    sub.add_parser("self-test", help="the parity comparison, the abstain rule, the statistics and the meta check")
    a = ap.parse_args()
    return cmd_run(a) if a.cmd == "run" else cmd_self_test(a)


if __name__ == "__main__":
    raise SystemExit(main())
