# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/level_prototype.py [working tree, uncommitted edit at 097933a]
"""The prototype: one fluoroscopic image in, every visible vertebra named, with a confidence and an abstain flag.

    python tools/level_prototype.py --image frame.png --out ~/proto_out
    python tools/level_prototype.py --image "~/FluoroCap/panels/pmc18m/*.png" --limit 24 --out ~/proto_out

Pipeline, exactly the corpus inference's path minus the caption evidence: orientation net (rotate to upright, and
say whether up/down is known) -> film histogram match -> vertebra detector (keypoint corners -> boxes, top to bottom)
-> fixed-scale context crops (96 px per vertebra on a 320 px canvas, band of 2*rung+1 targets, marker channel)
-> level model (single-crop softmax, plus the recurrent head over the run when a head file is given, plus a
horizontal-flip TTA) -> anchored decode over the whole run with T13 and L6 columns allowed (no caption) ->
per-vertebra name, probability, entropy, and an abstain flag when the decoded name and the single-crop name
disagree or the probability is below --abstain-below. Hardware boxes are drawn when a hardware detector is given.

--flag adds the binary transitional-anatomy flags (LSTV, TLTV) on the whole frame. A flag reports "this spine looks
transitional, count the whole spine or check the CT"; it never renames a vertebra, and it abstains when the frame
does not carry the structure the call depends on (no sacrum in the decoded run, no lumbosacral call). Each model is
<name>.pt with a <name>.flag.json sidecar: {target, arch, size, mean, std, threshold, n_out, needs: [level, ...]}.

Models default to the registry aliases (tools/model_registry.py): detector_v5z_final, allspine_v2_r1,
orientation_net, hardware_detector_v1; pass paths to override. Output per image: <stem>.json and <stem>_overlay.png.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from make_context_crops import LEVEL_ORDER  # noqa: E402
from recurrent_order import RunLabeller  # noqa: E402
from train_level_classifier import build_model  # noqa: E402,F401
from night_loadmodel import load_level_model, embed_dim  # noqa: E402
import fluorocap_infer as v1  # noqa: E402
from fluorocap_anchor import decode as anchor_decode  # noqa: E402
from level_flags import rule_flags  # noqa: E402
import eval_gate as EG  # noqa: E402

REGION = {**{f"C{i}": "cervical" for i in range(1, 8)}, **{f"T{i}": "thoracic" for i in range(1, 14)}, **{f"L{i}": "lumbar" for i in range(1, 7)}, "sacrum": "sacral"}


def resolve_default(alias, fallback):
    try:
        from model_registry import resolve
        return str(resolve(alias))
    except SystemExit:
        return fallback
    except Exception:  # noqa: BLE001
        return fallback


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _default_head_for(home, head_set, head_k, mod_sha, mod_p):
    """The saved head that belongs to THIS encoder, or none at all.

    Picking a default head by directory name alone is how an encoder and a head that never met end up running
    together. So the default is chosen by matching the sidecar's base model against the level model actually
    loaded; if no saved head matches, the prototype runs single-crop and says which heads it rejected and why.
    Running without the head costs accuracy that is measured and quotable; running with the wrong one costs
    correctness that is not detectable from the output.
    """
    roots = [Path(home) / "model_night" / "heads" / head_set,
             Path(home) / "model_night" / "heads"]
    seen, rejected = [], []
    for r in roots:
        if not r.exists():
            continue
        for p in sorted(r.rglob(f"head_k{head_k}.pt")) + sorted(r.rglob("head_k*.pt")):
            if p in seen:
                continue
            seen.append(p)
            side = p.parent / (p.stem + ".arch.json")
            if not side.exists():
                rejected.append((p.name, "no sidecar, cannot confirm which encoder it belongs to"))
                continue
            try:
                m = json.load(open(side))
            except Exception:  # noqa: BLE001
                rejected.append((p.name, "unreadable sidecar"))
                continue
            base = m.get("base_model")
            if not base or not Path(base).exists():
                rejected.append((p.name, "sidecar names a base model that is not on disk"))
                continue
            if sha(base) == mod_sha:
                return str(p)
            rejected.append((p.name, f"trained on {Path(base).name}, not {Path(mod_p).name}"))
    print(f"  note: no saved recurrent head matches this encoder (sha {mod_sha[:12]}); running single-crop "
          f"only, which is the weaker path")
    for n, why in rejected[:6]:
        print(f"        rejected {n}: {why}")
    return None


def load_image(path):
    im = Image.open(path)
    if im.mode in ("I;16", "I"):
        a = np.asarray(im, np.float32); lo, hi = np.percentile(a, 0.5), np.percentile(a, 99.5)
        im = Image.fromarray((np.clip((a - lo) / max(hi - lo, 1e-6), 0, 1) * 255).astype(np.uint8))
    return im.convert("L")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True, help="file, directory or glob")
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--detector", default=None); ap.add_argument("--model", default=None); ap.add_argument("--rung", type=int, default=1)
    ap.add_argument("--head", default=None,
                    help="recurrent head .pt trained for this model/rung. Left unset, the default head set is "
                         "loaded if present; pass '' to force single-crop only.")
    ap.add_argument("--head-set", default="allspine_v2",
                    help="which saved head directory under ~/model_night/heads to take the default head from")
    ap.add_argument("--head-k", type=int, default=3,
                    help="neighbours either side the head was trained for; k=3 is a band of seven vertebrae, "
                         "which scored highest on the bank where this head was first measured")
    ap.add_argument("--orient", default=None); ap.add_argument("--hardware", default=None)
    ap.add_argument("--hist-match", default=os.path.expanduser("~/films_drr"), help="film directory for histogram matching; '' to skip")
    ap.add_argument("--tgt-px", type=float, default=96); ap.add_argument("--size", type=int, default=320)
    ap.add_argument("--imgsz", type=int, default=1024); ap.add_argument("--conf", type=float, default=0.35); ap.add_argument("--hw-conf", type=float, default=0.2)
    ap.add_argument("--no-tta", action="store_true"); ap.add_argument("--abstain-below", type=float, default=0.5)
    ap.add_argument("--rare-penalty", type=float, default=1.0)
    ap.add_argument("--flag", nargs="*", default=None, help="binary transitional-anatomy flag models: paths to <name>.pt, each with a <name>.flag.json "
                                                          "sidecar {target, arch, size, mean, std, threshold, invert?}; the flag is reported, never used to change a level. "
                                                          "Left unset, the LSTV and TLTV flags are loaded from their default location; pass --flag with no paths to run without any.")
    ap.add_argument("--allow-head-mismatch", action="store_true",
                    help="run a recurrent head against an encoder it was not trained on. Only for deliberately "
                         "measuring what the mismatch costs; the output is otherwise confident nonsense.")
    ap.add_argument("--boxes-dir", default=None,
                    help="ORACLE BOXES: a directory of <stem>.json metas (docs/REAL_XRAY_DATASETS_SPEC.md) whose cls-0 boxes replace "
                         "the detector's, so naming is scored apart from detection")
    ap.add_argument("--no-orient", action="store_true", help="skip the orientation net (frames already upright by a device constant)")
    ap.add_argument("--box-detector", default=None,
                    help="a YOLO BOX detector (class 0 vertebra, class 1 sacrum, e.g. fine-tuned on real C-arm frames) used "
                         "instead of the keypoint detector; its vertebra boxes are named, its sacrum box is reported")
    ap.add_argument("--box-conf", type=float, default=0.25)
    ap.add_argument("--no-rule-flags", action="store_true",
                    help="skip the rule flags (no landmark in field, lumbar count, counted-vs-shape disagreement, "
                         "direction, hardware, run confidence). They need no model and are on by default.")
    ap.add_argument("--dump-posterior", action="store_true",
                    help="write the full per-body posterior into each vertebra record: `posterior` (the run posterior the "
                         "decoded `level` is read from: single-crop blended with the recurrent head, flip-TTA averaged) and "
                         "`posterior_single` (single-crop only), both over meta.level_order. Off by default; every existing "
                         "field is unchanged. tools/alphabet_couple.py needs it.")
    ap.add_argument("--dump-corners", action="store_true",
                    help="write the keypoint detector's four corners into each vertebra record: `corners` [[x, y] x 4] in "
                         "the detector's own keypoint order (not re-sorted: a scorer maps them to slots itself) and "
                         "`corner_conf` [4], in the pixel frame of `box` (the input pixels under --no-orient). null "
                         "under --box-detector or --boxes-dir, which carry no corners. Off by default; every existing "
                         "field is unchanged. tools/cine_eval.py reads it.")
    ap.add_argument("--sacrum-detector", default=None,
                    help="a YOLO box detector with a sacrum class (class 1, the realxray convention) run ONLY to fill "
                         "`sacrum_box` when the vertebra boxes come from the keypoint detector or from --boxes-dir, which "
                         "carry no sacrum. The vertebra boxes and every name are untouched. Off by default.")
    ap.add_argument("--sacrum-conf", type=float, default=0.25, help="confidence floor for --sacrum-detector")
    EG.add_args(ap)
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    H = os.path.expanduser("~")
    det_p = a.detector or resolve_default("detector_v5z_final", f"{H}/FluoroCap/detect_v5z_final_best.pt")
    mod_p = a.model or resolve_default("allspine_v2_r1", f"{H}/allspine_v2_fov96_ctx/runs/model_rung_1_aug2.pt")
    ori_p = None if a.no_orient else (a.orient or resolve_default("orientation_net", f"{H}/FluoroCap/orientation_net.pt"))
    hw_p = a.hardware or resolve_default("hardware_detector_v1", f"{H}/FluoroCap/hardware_det_v1.pt")
    from ultralytics import YOLO
    det = YOLO(det_p); hwdet = YOLO(hw_p) if hw_p and Path(hw_p).exists() else None
    boxdet = YOLO(os.path.expanduser(a.box_detector)) if a.box_detector else None
    # THE SACRUM DETECTOR FILLS ONE FIELD. The keypoint detector and the oracle boxes carry no sacrum, so a coupler
    # that counts from the sacrum (tools/alphabet_couple.py) has nothing to count from. This detector is run on the
    # frame as loaded (before the film histogram match, which is what its own training and evaluation saw) and its
    # best class-1 box goes into `sacrum_box`, with `sacrum_source` saying where it came from. It never adds,
    # removes or renames a vertebra.
    sacdet = YOLO(os.path.expanduser(a.sacrum_detector)) if a.sacrum_detector else None
    onet = None
    if ori_p and Path(ori_p).exists():
        from train_orientation import build_net as build_orient, to_tensor as orient_tensor
        onet = build_orient(False).to(dev); onet.load_state_dict(torch.load(ori_p, map_location=dev)); onet.eval()
    # THE ARCHITECTURE COMES FROM THE SIDECAR. This line used to read build_model(..., "resnet18"), which meant
    # the prototype could load only a bare torchvision resnet18 and raised on every model the backbone trainer
    # produces, because those wrap the encoder as LevelNet and carry an "enc." key prefix. The whole 2026-09-15
    # experiment -- the RAD-DINO and DINOv3 arms, the ordinal-loss arms, every arm trained on the merged banks --
    # was unloadable here. A checkpoint with no sidecar still resolves to resnet18, so nothing older changes.
    model, arch_spec = load_level_model(mod_p, len(LEVEL_ORDER), dev)
    fc = model.fc; model.fc = nn.Identity()
    # THE RUN-LEVEL HEAD, AND ITS WIDTH. The head is a bidirectional GRU over the classifier's frozen
    # embeddings, and it is where this project's best numbers came from: on the cervical-and-lumbar bank it took
    # 98.7% to 99.4% as the band grew from three vertebrae to seven. Two things kept it out of inference. Its
    # width was hard-coded to 512, which is right for a resnet18 and silently wrong for every ViT backbone; it
    # now comes from the detached fc. And it was opt-in via --head, so unless a path was typed there was no
    # run-level model at all -- it now loads from the default head directory when one is present.
    #
    # A HEAD IS ONLY VALID WITH THE ENCODER IT WAS TRAINED ON. The head consumes the level model's penultimate
    # features. Pair it with a different encoder and it receives a 512-wide vector that means something else
    # entirely, and it will still run and still return 27 plausible names. So the sidecar's base model is
    # checked against the model actually loaded, and a mismatch is refused rather than warned about. This is not
    # hypothetical: the first version of this default pointed at a head trained on model_r18_ce.pt while the
    # default level model is allspine_v2_r1, two different encoders, and nothing would have complained.
    mod_sha = sha(mod_p)
    head = None
    head_p = a.head or None
    if head_p is None and a.head != "":
        head_p = _default_head_for(H, a.head_set, a.head_k, mod_sha, mod_p)
    if head_p:
        if not Path(head_p).expanduser().exists():
            # an explicitly named head that is absent is a hard error: a caller who typed a path and silently
            # got no head would read the resulting numbers as the head's
            raise SystemExit(f"--head {head_p} does not exist. Pass --head '' to run single-crop only.")
        head_p = str(Path(head_p).expanduser())
        side = Path(head_p).with_suffix("").with_suffix(".arch.json")
        if not side.exists():
            side = Path(str(head_p).replace(".pt", "") + ".arch.json")
        hmeta = json.load(open(side)) if side.exists() else {}
        base = hmeta.get("base_model")
        if base and Path(base).exists():
            bsha = sha(base)
            if bsha != mod_sha and not a.allow_head_mismatch:
                raise SystemExit(
                    f"head/encoder mismatch: {Path(head_p).name} was trained on {Path(base).name} "
                    f"(sha {bsha[:12]}) but the level model loaded is {Path(mod_p).name} (sha {mod_sha[:12]}). "
                    f"The head reads that encoder's features and would return confident nonsense. "
                    f"Pass a matching head, or --allow-head-mismatch if you are deliberately testing this.")
        d_in = embed_dim(fc, arch_spec)
        if hmeta.get("d_in") and int(hmeta["d_in"]) != int(d_in):
            raise SystemExit(f"head expects {hmeta['d_in']}-wide features, encoder gives {d_in}")
        head = RunLabeller(d_in, len(LEVEL_ORDER)).to(dev)
        head.load_state_dict(torch.load(head_p, map_location=dev)); head.eval()
        print(f"  recurrent head {Path(head_p).name} loaded, d_in={d_in}, "
              f"k={hmeta.get('k', '?')} (band {hmeta.get('vertebrae_visible', '?')}), "
              f"bank {Path(str(hmeta.get('bank', '?'))).name}")
    # binary transitional-anatomy flags (LSTV / TLTV). A flag says "this spine looks transitional, count the whole
    # spine or check the CT"; it never renames a vertebra, and it abstains when its field-of-view precondition fails.
    # DEFAULT ON, BUT ONLY WHAT EXISTS. Leaving --flag unset loads the transitional flags from their default
    # location; `--flag` with no paths runs without any. A named path that is missing is a hard error, because a
    # flag the caller asked for and did not get is worse than no flag at all. A DEFAULT path that is missing is
    # skipped with a warning, so the prototype still runs on a machine that has no flag models.
    flag_paths = a.flag
    if flag_paths is None:
        flag_paths = []
        for cand in (f"{H}/lstv_flag/models/lstv_flag_v2.pt", f"{H}/lstv_flag/models/tltv_flag_v2.pt"):
            if Path(cand).exists():
                flag_paths.append(cand)
            else:
                print(f"  note: default flag model {cand} not present; running without it")
    flags = []
    for fp in flag_paths:
        fp = os.path.expanduser(fp)
        side = Path(str(fp).replace(".pt", "") + ".flag.json")
        meta_f = json.load(open(side)) if side.exists() else {}
        arch = meta_f.get("arch", "resnet18"); import torchvision
        net = getattr(torchvision.models, arch)(weights=None); net.fc = nn.Linear(net.fc.in_features, int(meta_f.get("n_out", 2)))
        sd = torch.load(fp, map_location=dev)
        net.load_state_dict(sd.get("state_dict", sd) if isinstance(sd, dict) else sd)
        net.to(dev).eval()
        flags.append({"net": net, "target": meta_f.get("target", Path(fp).stem), "size": int(meta_f.get("size", 384)),
                      "mean": float(meta_f.get("mean", 0.45)), "std": float(meta_f.get("std", 0.25)),
                      "threshold": float(meta_f.get("threshold", 0.5)), "needs": meta_f.get("needs", []), "path": fp})
        flags[-1]["meta"] = {**meta_f, "path": fp, "sha256": sha(fp)}
    ref = v1.film_reference_cdf(a.hist_match) if a.hist_match and Path(os.path.expanduser(a.hist_match)).exists() else None
    meta = {"detector": det_p, "level_model": mod_p, "level_model_sha256": sha(mod_p), "orientation": ori_p if onet else None, "hardware": hw_p if hwdet else None,
            "head": head_p if head else None, "head_active": bool(head),
            "detector_sha256": sha(det_p) if Path(det_p).exists() else None,
            "orientation_sha256": sha(ori_p) if (onet and Path(ori_p).exists()) else None,
            "hardware_sha256": sha(hw_p) if (hwdet and Path(hw_p).exists()) else None, "hist_match": a.hist_match if ref is not None else None, "tta": not a.no_tta, "rare_penalty": a.rare_penalty, "level_order": LEVEL_ORDER,
            "flags": [f["meta"] for f in flags],
            "sacrum_detector": os.path.expanduser(a.sacrum_detector) if sacdet is not None else None,
            "sacrum_detector_sha256": sha(os.path.expanduser(a.sacrum_detector)) if sacdet is not None else None,
            "sacrum_conf": a.sacrum_conf if sacdet is not None else None, "dump_posterior": bool(a.dump_posterior),
            "dump_corners": bool(a.dump_corners)}
    src = os.path.expanduser(a.image)
    paths = sorted(glob.glob(str(Path(src) / "**" / "*"), recursive=True)) if os.path.isdir(src) else sorted(glob.glob(src))
    paths = [p for p in paths if p.lower().endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"))]
    if a.limit:
        paths = paths[: a.limit]
    # THE GATE (tools/eval_gate.py), before any image is named: every model whose output reaches a name or a box --
    # detector, box detector, sacrum detector, level encoder, head, orientation net when it turns the frame, the flag
    # models -- is checked against every image's patient through its initialisation chain. A patient any of them
    # trained or was selected on, an unresolved lineage or an unkeyable image stops the run unless --not-held-out
    # says why (inference on arbitrary images carries no held-out claim, and says so there). The hardware detector
    # only draws boxes and is not gated. The verdict goes into prototype_meta.json, which every scorer carries.
    gated = {"detector": det_p, "box_detector": os.path.expanduser(a.box_detector) if a.box_detector else None,
             "sacrum_detector": os.path.expanduser(a.sacrum_detector) if a.sacrum_detector else None,
             "level_model": mod_p, "head": head_p if head else None, "orientation": ori_p if onet else None}
    for f in flags:
        gated[f"flag:{f['target']}"] = f["path"]
    gate = EG.block(EG.assert_unseen_all([dict(path=p) for p in paths], gated, "tools/level_prototype.py",
                                         eval_set=src, not_held_out=a.not_held_out, touched=a.touched), a.not_held_out)
    # weights_sha256 beside the verdict, hashed now from every gated model: carry_proto binds the two
    meta = EG.stamp(meta, gate, weights={r: pth for r, pth in gated.items() if pth})
    out = Path(os.path.expanduser(a.out)); out.mkdir(parents=True, exist_ok=True)
    json.dump(meta, open(out / "prototype_meta.json", "w"), indent=1)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()
    print(f"prototype: {len(paths)} images; level model {Path(mod_p).name} ({meta['level_model_sha256'][:12]}); head {'on' if head else 'off'}; device {dev}", flush=True)
    summary = []
    for p in paths:
        t0 = time.time(); rec = {"image": p}
        try:
            im = load_image(p); pre = {}; direction_known = True
            if onet is not None:
                with torch.no_grad():
                    po = torch.softmax(onet(orient_tensor(im, 256).unsqueeze(0).to(dev)), 1)[0].cpu().numpy()
                k_rot = int(po.argmax()); pre["rotation_k"] = k_rot; pre["rotation_prob"] = round(float(po.max()), 3)
                if k_rot in (1, 3) and float(po.max()) >= 0.9:
                    im = im.rotate((-90 * k_rot) % 360, expand=True); pre["rotated"] = True
                if k_rot == 2 or float(po[2]) >= 0.25 or float(po.max()) < 0.6:
                    direction_known = False
            im_raw = im          # the frame as loaded (and turned upright), before the film histogram match
            if ref is not None:
                im, pre2 = v1.prepare_panel(im, False, False, hist_ref=ref); pre.update(pre2)
            rgb = np.asarray(im.convert("RGB"))
            boxes, confs = [], []
            # THE CORNERS RIDE WITH THEIR BOX. Kept only from the keypoint detector, appended in the same branch as
            # the box, so the >= 4 px size filter that drops a box drops its corners too and index j is one body in
            # every list. Oracle boxes and the box detector have no corners: those runs write null.
            corners, kpconf = [], []
            rec_sacrum, sac_src = None, None
            if a.boxes_dir:
                # oracle boxes: the truth vertebra boxes of this frame, top to bottom; no detector
                mp = Path(os.path.expanduser(a.boxes_dir)) / (Path(p).stem + ".json")
                mb = json.load(open(mp))["boxes"] if mp.exists() else []
                for bb in sorted([b["box"] for b in mb if b.get("cls", 0) == 0], key=lambda b: (b[1] + b[3]) / 2):
                    boxes.append([int(round(v)) for v in bb]); confs.append(1.0)
                res = None
            else:
                res = det.predict(rgb, imgsz=a.imgsz, conf=a.conf, verbose=False)[0] if boxdet is None else None
            if boxdet is not None and not a.boxes_dir:
                rb = boxdet.predict(rgb, imgsz=a.imgsz, conf=a.box_conf, verbose=False)[0]
                cls = rb.boxes.cls.cpu().numpy().astype(int); xy = rb.boxes.xyxy.cpu().numpy(); cf = rb.boxes.conf.cpu().numpy()
                vi = [i for i in np.argsort((xy[:, 1] + xy[:, 3]) / 2) if cls[i] == 0]
                # overlapping duplicates of one body (IoU > 0.5) keep the most confident
                keep = []
                for i in sorted(vi, key=lambda i: -cf[i]):
                    b = xy[i]
                    def _iou(p, q):
                        ix = max(0, min(p[2], q[2]) - max(p[0], q[0])); iy = max(0, min(p[3], q[3]) - max(p[1], q[1]))
                        u = (p[2] - p[0]) * (p[3] - p[1]) + (q[2] - q[0]) * (q[3] - q[1]) - ix * iy
                        return ix * iy / u if u > 0 else 0
                    if all(_iou(b, xy[j]) <= 0.5 for j in keep):
                        keep.append(i)
                for i in sorted(keep, key=lambda i: (xy[i, 1] + xy[i, 3]) / 2):
                    b = [int(v) for v in xy[i]]
                    if b[2] - b[0] >= 4 and b[3] - b[1] >= 4:
                        boxes.append(b); confs.append(round(float(cf[i]), 3))
                si = [i for i in range(len(cls)) if cls[i] == 1]
                rec_sacrum = [int(v) for v in xy[max(si, key=lambda i: cf[i])]] + [round(float(cf[max(si, key=lambda i: cf[i])]), 3)] if si else None
                sac_src = "box_detector" if rec_sacrum else None
            if sacdet is not None and rec_sacrum is None:
                rs_ = sacdet.predict(np.asarray(im_raw.convert("RGB")), imgsz=a.imgsz, conf=a.sacrum_conf, verbose=False)[0]
                if len(rs_.boxes):
                    scls = rs_.boxes.cls.cpu().numpy().astype(int); sxy = rs_.boxes.xyxy.cpu().numpy(); scf = rs_.boxes.conf.cpu().numpy()
                    si = [i for i in range(len(scls)) if scls[i] == 1]
                    if si:
                        i_ = max(si, key=lambda i: scf[i])
                        rec_sacrum = [int(v) for v in sxy[i_]] + [round(float(scf[i_]), 3)]; sac_src = "sacrum_detector"
            if res is not None and res.keypoints is not None and len(res.boxes):
                kp = res.keypoints.xy.cpu().numpy(); cf = res.boxes.conf.cpu().numpy()
                kc = res.keypoints.conf.cpu().numpy() if res.keypoints.conf is not None else None
                for i in np.argsort(kp[:, :, 1].mean(1)):
                    pts = kp[i]; b = [int(pts[:, 0].min()), int(pts[:, 1].min()), int(pts[:, 0].max()), int(pts[:, 1].max())]
                    if b[2] - b[0] >= 4 and b[3] - b[1] >= 4:
                        boxes.append(b); confs.append(round(float(cf[i]), 3))
                        corners.append([[round(float(x), 2), round(float(y), 2)] for x, y in pts[:, :2]])
                        kpconf.append([round(float(c), 4) for c in kc[i]] if kc is not None else None)
            hw_boxes = []
            if hwdet is not None:
                rh = hwdet.predict(rgb, imgsz=a.imgsz, conf=a.hw_conf, verbose=False)[0]
                if len(rh.boxes):
                    hw_boxes = [[int(v) for v in b] + [round(float(c), 3)] for b, c in zip(rh.boxes.xyxy.cpu().numpy(), rh.boxes.conf.cpu().numpy())]
            rec.update({"preprocess": pre, "direction_known": direction_known, "boxes": boxes, "det_conf": confs, "hw_boxes": hw_boxes, "width": im.size[0], "height": im.size[1],
                        "sacrum_box": rec_sacrum, "sacrum_source": sac_src})
            vert = []
            if boxes:
                arr = np.asarray(im, np.float32); lo, hi = np.percentile(arr, 0.5), np.percentile(arr, 99.5); img0 = np.clip((arr - lo) / max(hi - lo, 1e-6), 0, 1)
                variants = [(img0, boxes)]
                if not a.no_tta:
                    W = img0.shape[1]; fb = [[W - 1 - b[2], b[1], W - 1 - b[0], b[3]] for b in boxes]; variants.append((img0[:, ::-1].copy(), fb))
                # TWO READINGS, KEPT APART ON PURPOSE. `morph` is the single-crop posterior: what one vertebra
                # looks like, with no sequence information in it. `probs` blends that with the run-level head.
                # They must not be collapsed, because the abstain rule and the count_vs_morphology flag both
                # exist to compare a counted name against a shape-only name. Taking the shape-only name from the
                # blended posterior would make the two readings agree by construction, the abstain rate would
                # fall, and the fall would read as the head improving agreement when it is the comparison
                # quietly disappearing.
                morph_ps, all_ps = [], []
                with torch.no_grad():
                    for img, bx in variants:
                        X = torch.from_numpy(v1.crops_for_run(img, bx, a.tgt_px, a.size, a.rung)).float().to(dev)
                        emb = model(X); p1 = torch.softmax(fc(emb), 1)
                        morph_ps.append(p1.cpu().numpy()); all_ps.append(p1.cpu().numpy())
                        if head is not None:
                            all_ps.append(torch.softmax(head(emb.unsqueeze(0))[0], 1).cpu().numpy())
                morph = np.mean(morph_ps, 0)
                probs = np.mean(all_ps, 0)
                single = [LEVEL_ORDER[int(i)] for i in morph.argmax(1)]
                dec = anchor_decode(probs, set(), {}, None, direction_known=direction_known, w_rare=a.rare_penalty)
                decoded = dec.get("anchored_pred") or single
                ent = (-(probs * np.log(probs + 1e-9)).sum(1))
                for j, b in enumerate(boxes):
                    top = np.argsort(probs[j])[::-1][:3]
                    pj = float(probs[j][LEVEL_ORDER.index(decoded[j])]) if decoded[j] in LEVEL_ORDER else 0.0
                    abstain = (decoded[j] != single[j]) or pj < a.abstain_below
                    vert.append({"box": b, "det_conf": confs[j], "level": decoded[j], "level_prob": round(pj, 3), "single_crop": single[j],
                                 "single_crop_prob": round(float(morph[j].max()), 3),
                                 "top3": [[LEVEL_ORDER[int(i)], round(float(probs[j][i]), 3)] for i in top], "entropy": round(float(ent[j]), 3),
                                 "region": REGION.get(decoded[j], "?"), "abstain": bool(abstain)})
                    if a.dump_posterior:
                        # six significant digits, not three decimals: a coupler scores log p, and a probability
                        # rounded to 0.000 would score as the floor rather than as what the model said
                        vert[-1]["posterior"] = [float(f"{float(x):.6g}") for x in probs[j]]
                        vert[-1]["posterior_single"] = [float(f"{float(x):.6g}") for x in morph[j]]
                    if a.dump_corners:
                        vert[-1]["corners"] = corners[j] if len(corners) == len(boxes) else None
                        vert[-1]["corner_conf"] = kpconf[j] if len(kpconf) == len(boxes) else None
                rec["decode_score"] = dec.get("anchor_score"); rec["anchor_source"] = dec.get("anchor_source")
            rec["vertebrae"] = vert
            # the transitional flags, on the whole frame. Each abstains when the frame cannot carry the call: a
            # lumbosacral flag needs the sacrum in view, a thoracolumbar one needs the twelfth-rib region, and the
            # decoded run is what says whether they are there. A flag never changes a level: it asks for a count.
            named = {v["level"] for v in vert}
            for f in flags:
                need = f["needs"] or (["sacrum"] if "lstv" in f["target"].lower() else ["T12"] if "tltv" in f["target"].lower() else [])
                missing = [n for n in need if n not in named]
                entry = {"target": f["target"], "abstain": bool(missing), "needs": need, "missing_in_frame": missing}
                if not missing:
                    with torch.no_grad():
                        arr = np.asarray(im.resize((f["size"], f["size"]), Image.BILINEAR), np.float32) / 255.0
                        x = torch.from_numpy(np.repeat(((arr - f["mean"]) / f["std"])[None], 3, 0)).unsqueeze(0).to(dev)
                        pr = torch.softmax(f["net"](x), 1)[0].cpu().numpy()
                    pos = float(pr[-1])
                    entry.update({"p": round(pos, 3), "flag": bool(pos >= f["threshold"]), "threshold": f["threshold"]})
                rec.setdefault("transitional_flags", []).append(entry)
            # RULE FLAGS. Computed from the decoded run with no model: the conditions under which a level call
            # should not be trusted at all (no landmark in the field, six lumbar bodies, counted and shape-only
            # names disagreeing, unknown direction, hardware, a run the classifier cannot read). They cost
            # nothing, they fire on frames where the learned flags abstain, and unlike the learned flags they can
            # be measured against render ground truth today. See tools/level_flags.py.
            if not a.no_rule_flags:
                rec.setdefault("transitional_flags", []).extend(
                    rule_flags(vert, direction_known=direction_known, hw_boxes=hw_boxes))
            rec["seconds"] = round(time.time() - t0, 2)
            # overlay
            ov = im.convert("RGB"); dr = ImageDraw.Draw(ov)
            for hb in hw_boxes:
                dr.rectangle(hb[:4], outline=(255, 170, 0), width=2)
            for v in vert:
                col = (90, 200, 120) if not v["abstain"] else (230, 90, 70)
                dr.rectangle(v["box"], outline=col, width=2)
                txt = f"{v['level']} {v['level_prob']:.2f}" + ("?" if v["abstain"] else "")
                x, y = v["box"][2] + 4, max(0, v["box"][1])
                dr.rectangle([x - 2, y - 2, x + 8 * len(txt) + 4, y + 18], fill=(0, 0, 0)); dr.text((x, y), txt, fill=col, font=font)
            if not direction_known:
                dr.text((6, 6), "up/down uncertain", fill=(230, 90, 70), font=font)
            yb = 26
            for e in rec.get("transitional_flags", []):
                if e["abstain"]:
                    t2 = f"{e['target']}: abstains ({', '.join(e['missing_in_frame'])} not in frame)"; c2 = (170, 170, 170)
                elif e["flag"]:
                    # A LEARNED FLAG CARRIES A PROBABILITY; A RULE FLAG CARRIES A REASON. Both kinds share
                    # this list, so neither field can be assumed present.
                    sc = f" {e['p']:.2f}" if "p" in e else ""
                    t2 = f"{e['target']}: FIRED{sc} - {e.get('reason', 'count the whole spine')[:72]}"; c2 = (240, 170, 60)
                else:
                    sc = f" {e['p']:.2f}" if "p" in e else ""
                    t2 = f"{e['target']}: quiet{sc}"; c2 = (120, 180, 220)
                dr.rectangle([4, yb - 2, 10 + 8 * len(t2), yb + 18], fill=(0, 0, 0)); dr.text((6, yb), t2, fill=c2, font=font); yb += 22
            stem = Path(p).stem
            ov.save(out / f"{stem}_overlay.png"); json.dump(rec, open(out / f"{stem}.json", "w"), indent=1)
            def _fl(e):
                if e.get("abstain"):
                    return f"[{e['target']}:abstain]"
                sc = format(e["p"], ".2f") if "p" in e else ""
                return f"[{e['target']}:{('FLAG ' + sc).strip() if e.get('flag') else (sc or 'quiet')}]"
            fl = " ".join(_fl(e) for e in rec.get("transitional_flags", []))
            line = f"{stem}: " + (" ".join(f"{v['level']}({v['level_prob']:.2f}{'?' if v['abstain'] else ''})" for v in vert) if vert else "no vertebra detected") + (" " + fl if fl else "") + f"  [{rec['seconds']} s]"
        except Exception as e:  # noqa: BLE001
            rec["error"] = f"{type(e).__name__}: {e}"; line = f"{Path(p).stem}: ERROR {rec['error']}"
        print(line, flush=True); summary.append(rec)
    json.dump(summary, open(out / "prototype_results.json", "w"), indent=1)
    n_v = sum(len(r.get("vertebrae", [])) for r in summary); n_a = sum(1 for r in summary for v in r.get("vertebrae", []) if v["abstain"])
    print(f"done: {len(summary)} images, {n_v} vertebrae named, {n_a} abstained, {sum(1 for r in summary if not r.get('vertebrae'))} with no detection")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
