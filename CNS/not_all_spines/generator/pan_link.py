"""paper/cns2026/pan_link.py -- the pan's frames linked into one column and named by counting (v21, Greg, 2026-10-31).

What the closing video shows on each box. The level prototype names every frame alone, and alone a frame of the mid
thoracic spine under the shoulders cannot be named (it abstains, or calls a run of thoracic bodies lumbar). The pan is
the surgeon's own remedy, counting from the sacrum one frame at a time, done by the machine: each frame is registered to
the one before by phase correlation, every box the detector drew is placed on the one column those shifts build, boxes
of one body in successive frames are merged, a gap longer than the bodies beside it is read as the bodies the detector
missed there, and the column is named upward from the body the model itself named L5 above the sacrum in the first
frames. Nothing here reads the CT's labels; check() sets the names against them afterwards.

The reported stack keeps boxes the detector scores 0.35 or more, and at that floor it boxes the lumbar bodies but none
of the thoracic ones in the upper half of the field until the field is wholly thoracic (v22's run 8, frames 165 to
265). With --det and --floor the linker reads a run made at a lower floor and keeps a weaker box only where it stands
on the column the reported floor's own boxes trace, within 0.4 of its width, so a rib or a bowel loop the low floor
also boxes never enters the count; linked.json records both, and kept() gives the film the same boxes. Even at a floor
of 0.05 one facing boxes nothing at T12 while the lumbar bodies fill the field, where the mirrored frame boxes it at
0.8: --flip names a second run over the mirrored frames, whose boxes are mirrored back and pooled with the first,
one box a body a frame (the more confident where two overlap), the horizontal-flip test the prototype already uses
for its names.

    python paper/cns2026/pan_link.py RUN_FOLDER [--det FOLDER --floor CONF --flip FOLDER]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np
import cv2
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "grid"))
import pan_render  # noqa: E402

UP = [f"L{k}" for k in range(5, 0, -1)] + [f"T{k}" for k in range(12, 0, -1)] + [f"C{k}" for k in range(7, 0, -1)]


def frames(run):
    """The pan's frames as the job cut them: the FLUX panorama, each frame's centre, the same noise."""
    pan = json.load(open(run / "pan.json", encoding="utf-8"))
    panorama = np.asarray(Image.open(run / "flux_s0.png"), np.float32) / 255
    rng = np.random.default_rng(20261102)
    for centre in pan["centres"]:
        yield pan_render.fluoro(panorama, centre, rng)


def shifts(run):
    """Each frame's offset from the first, in pixels (rows, columns), by phase correlation with the frame before."""
    window = cv2.createHanningWindow((512, 512), cv2.CV_32F)
    offsets, last, total = [], None, np.zeros(2)
    for frame in frames(run):
        small = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_AREA).astype(np.float32)
        if last is not None:
            (dx, dy), _ = cv2.phaseCorrelate(last, small, window)
            total = total + np.array([dy, dx]) * 2
        offsets.append(total.copy())
        last = small
    return np.array(offsets)


REPORTED = 0.35                     # the reported stack's detector floor


def detections(run, facing, folder="det", floor=None):
    out = []
    for k, path in enumerate(sorted((run / folder).glob("f*.json"))):
        rec = json.load(open(path, encoding="utf-8"))
        for v in rec["vertebrae"]:
            if floor is not None and v["det_conf"] < floor:
                continue
            x0, y0, x1, y1 = v["box"]
            if facing == "R":
                x0, x1 = rec["width"] - x1, rec["width"] - x0
            out.append({"frame": k, "box": [x0, y0, x1, y1], "level": v["level"], "p": v["level_prob"],
                        "abstain": v["abstain"], "conf": v["det_conf"]})
    return out


def place(dets, offsets):
    """Each box's row, column and height on the one column the frames' shifts build."""
    for d in dets:
        x0, y0, x1, y1 = d["box"]
        d["row"] = (y0 + y1) / 2 - offsets[d["frame"]][0]
        d["col"] = (x0 + x1) / 2 - offsets[d["frame"]][1]
        d["height"] = y1 - y0
    return dets


def on_column(dets):
    """Every box at the reported floor, and a weaker one only where it stands on the column those boxes trace."""
    strong = sorted((d for d in dets if d["conf"] >= REPORTED), key=lambda d: d["row"])
    if len(strong) < 2:
        return dets
    rows = np.array([d["row"] for d in strong])
    cols = np.array([d["col"] for d in strong])
    keep = []
    for d in dets:
        width = d["box"][2] - d["box"][0]
        if d["conf"] >= REPORTED or abs(d["col"] - np.interp(d["row"], rows, cols)) <= 0.4 * width:
            keep.append(d)
    return keep


def iou(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    inter = w * h
    return inter / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter)


def pooled(run, facing, folder, floor, flip):
    """The run's boxes, and with FLIP the mirrored run's too, one box a body a frame, the more confident kept."""
    dets = detections(run, facing, folder, floor)
    if not flip:
        return dets
    dets += detections(run, "R" if facing == "L" else "L", flip, floor)
    out = []
    for d in sorted(dets, key=lambda d: -d["conf"]):
        if all(o["frame"] != d["frame"] or iou(o["box"], d["box"]) <= 0.5 for o in out):
            out.append(d)
    return sorted(out, key=lambda d: (d["frame"], d["box"][1]))


def kept(run, linked):
    """The boxes the linker counted with, as linked.json says it read them, for the film."""
    dets = pooled(run, linked["facing"], linked.get("det", "det"), linked.get("floor"), linked.get("flip"))
    return on_column(place(dets, np.array(linked["offsets"])))


def whole(box, size=1024, field=0.47):
    """A box the round field does not cut: all four corners well inside it, so its centre is the body's."""
    c, r = (size - 1) / 2, field * size * 0.96
    return all(np.hypot(x - c, y - c) < r for x in box[0::2] for y in box[1::2])


def link(dets, offsets):
    """Bodies along the column: each box placed by its frame's offset (the column's rows grow caudally), boxes within
    half a body of one another merged, then gaps longer than 1.6 bodies filled with the bodies they must hold."""
    place(dets, offsets)
    bodies = []
    for d in sorted(dets, key=lambda d: d["row"]):
        if bodies and d["row"] - bodies[-1]["rows"][-1] < 0.45 * d["height"]:
            bodies[-1]["rows"].append(d["row"])
            bodies[-1]["members"].append(d)
        else:
            bodies.append({"rows": [d["row"]], "members": [d]})
    for b in bodies:
        seen = [m for m in b["members"] if whole(m["box"])]
        seen = seen if len(seen) >= 3 else b["members"]
        b["row"] = float(np.median([m["row"] for m in seen]))
        b["height"] = float(np.median([m["height"] for m in seen]))
        b["col"] = float(np.median([m["col"] for m in seen]))
    bodies = [b for b in bodies if len(b["members"]) >= 3]
    return sorted(bodies, key=lambda b: -b["row"])                     # caudal first


def name(bodies):
    """Upward from the model's own L5, the lowest body the first second of frames names L5, one level a body while the
    bodies follow one another. Past the first gap the count cannot bridge with certainty (under the shoulders, where
    the detector sees nothing), and the neck's small bodies lie too close for boxes to be merged by place alone, so
    there each box keeps the name the model gave it in its own frame, and the boxes of one name, five or more, are one
    body."""
    first = [b for b in bodies if any(m["frame"] < 30 and m["level"] == "L5" and not m["abstain"] for m in b["members"])]
    anchor = bodies.index(first[0])
    named = []
    for k, b in enumerate(bodies[anchor:]):
        if k:
            prev = bodies[anchor + k - 1]
            if (prev["row"] - b["row"]) / (1.25 * (prev["height"] + b["height"]) / 2) > 1.6:
                return named + by_shape([m for c in bodies[anchor + k:] for m in c["members"]])
        b["name"], b["how"] = UP[k], "count"
        named.append(b)
    return named


def by_shape(members):
    groups = {}
    for m in members:
        if not m["abstain"]:
            groups.setdefault(m["level"], []).append(m)
    out = []
    for level, ms in groups.items():
        if len(ms) >= 5:
            seen = [m for m in ms if whole(m["box"])] or ms
            out.append({"name": level, "how": "shape", "members": ms,
                        "row": float(np.median([m["row"] for m in seen])),
                        "col": float(np.median([m["col"] for m in seen])),
                        "height": float(np.median([m["height"] for m in seen]))})
    return sorted(out, key=lambda b: -b["row"])


def check(run, bodies, offsets):
    """Each named body set against the CT's own label at its place in the first frame's coordinates."""
    pan = json.load(open(run / "pan.json", encoding="utf-8"))
    labels = np.asarray(Image.open(run / "labels.png"))
    ids = {i: n for i, n in pan_render.LEVELS.items()}
    ids[pan_render.SACRUM] = "S"
    c0 = np.array(pan["centres"][0]) - pan["frame"] / 2
    right = 0
    for b in bodies:
        r, c = int(round(b["row"] + c0[0])), int(round(b["col"] + c0[1]))
        window = labels[max(r - 6, 0):r + 7, max(c - 6, 0):c + 7]
        found = np.bincount(window.ravel(), minlength=29)
        found[0] = 0
        truth = ids.get(int(found.argmax()), "?") if found.max() else "?"
        b["truth"] = truth
        right += truth == b["name"]
    return right, len(bodies)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--det", default="det")
    ap.add_argument("--floor", type=float, default=None)
    ap.add_argument("--flip", default=None)
    a = ap.parse_args()
    run = Path(a.run)
    facing = (run / "facing.txt").read_text().strip() if (run / "facing.txt").is_file() else "L"
    cache = run / "offsets.npy"
    offsets = np.load(cache) if cache.is_file() else shifts(run)
    np.save(cache, offsets)
    centres = np.array(json.load(open(run / "pan.json", encoding="utf-8"))["centres"])
    drift = np.abs((offsets - (centres - centres[0]) * [-1, -1])).max()
    dets = on_column(place(pooled(run, facing, a.det, a.floor, a.flip), offsets))
    bodies = name(link(dets, offsets))
    right, n = check(run, bodies, offsets)
    print(f"registration's worst drift against the pan's own path: {drift:.1f} px; named {n} bodies, {right} as the CT labels them")
    print(" ".join(f"{b['name']}/{b['truth']}({b['how'][0]})" for b in bodies))
    json.dump({"offsets": offsets.round(2).tolist(), "facing": facing, "det": a.det, "floor": a.floor, "flip": a.flip,
               "bodies": [{"name": b["name"], "truth": b["truth"], "how": b["how"], "row": b["row"], "col": b["col"], "height": b["height"],
                           "first": min(m["frame"] for m in b["members"]),
                           "frames": sorted({m["frame"] for m in b["members"]})} for b in bodies]},
              open(run / "linked.json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
