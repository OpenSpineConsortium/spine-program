# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/fluoro_video/synth.py [untracked at 097933a (laptop copy of 2026-10-08)]
"""Synthetic composite videos with KNOWN panel boxes, on/off times, pulse cadence, playback speed, cuts and replays.

Every scenario is a deterministic function of its seed. Frames are composed in numpy and encoded with libx264
(crf 18, yuv420p) through PyAV, so the pipeline sees real lossy video. The room-camera panels are saturated,
textured colour; the fluoroscopic panel is a greyscale field with bright 'bodies', quantum noise re-drawn on every
pulse, and optional translation; a flat grey UI bar and a white-on-black label are distractors.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

W, H, FPS = 640, 360, 30


def _font(size):
    import matplotlib
    p = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSansMono-Bold.ttf"
    if not p.exists():
        p = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSans.ttf"
    return ImageFont.truetype(str(p), size)


def anatomy_canvas(h, w, seed):
    rng = np.random.default_rng(seed)
    f = ndi.gaussian_filter(rng.normal(size=(h, w)), 7)
    f = (f - f.min()) / (f.max() - f.min())
    img = 70 + 110 * f
    yy, xx = np.mgrid[0:h, 0:w]
    for k in range(int(h / 45)):                       # a column of bright 'vertebral bodies'
        cy = 25 + 45 * k + rng.integers(-4, 5)
        cx = w // 2 + rng.integers(-10, 11)
        m = ((xx - cx) / 38.0) ** 2 + ((yy - cy) / 16.0) ** 2 <= 1
        img[m] += 45
    return np.clip(img, 0, 255)


def room(t, seed=0):
    """Saturated, moving colour scene (the room camera)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = 128 + 100 * np.sin(xx / 37.0 + t * 1.3)
    g = 90 + 60 * np.sin(yy / 23.0 - t * 0.7)
    b = 150 + 90 * np.cos((xx + yy) / 51.0 + t)
    img = np.stack([r, g * 0.5, b], 2)
    rng = np.random.default_rng(seed * 100000 + int(round(t * FPS)))
    img += rng.normal(0, 6, img.shape)
    return np.clip(img, 0, 255)


def fluoro_image(canvas, box, t_img, pulse, v_px_s, seed, noise=5.0):
    x0, y0, x1, y1 = box
    h, w = y1 - y0, x1 - x0
    off = int(round(v_px_s * t_img))
    off = max(0, min(canvas.shape[0] - h, off))
    a = canvas[off:off + h, :w].copy()
    rng = np.random.default_rng(seed * 7919 + pulse)
    a += rng.normal(0, noise, a.shape)
    return np.clip(a, 0, 255)


def distractors(img):
    img[340:360, :, :] = 128                           # flat grey UI bar: greyscale but untextured
    im = Image.fromarray(img.astype(np.uint8))
    dr = ImageDraw.Draw(im)
    dr.rectangle([10, 300, 150, 330], fill=(0, 0, 0))
    dr.text((16, 303), "CAM 2", fill=(255, 255, 255), font=_font(20))
    return np.asarray(im).astype(np.float32)


def encode(path, frames_iter, pts_list=None, time_base=Fraction(1, 90000)):
    import av
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = av.open(str(path), "w")
    st = out.add_stream("libx264", rate=FPS)
    st.width, st.height, st.pix_fmt = W, H, "yuv420p"
    st.options = {"crf": "18", "preset": "medium", "threads": "1"}
    if pts_list is not None:
        st.codec_context.time_base = time_base
    for k, fr in enumerate(frames_iter):
        vf = av.VideoFrame.from_ndarray(fr.astype(np.uint8), format="rgb24")
        if pts_list is not None:
            vf.pts = int(pts_list[k])
            vf.time_base = time_base
        else:
            vf.pts = k
        for pk in st.encode(vf):
            out.mux(pk)
    for pk in st.encode():
        out.mux(pk)
    out.close()


def _panel_frame(t, on, box, canvas, pulse_hz, v, seed, black=None, extra=None, t_content=None):
    img = room(t, seed)
    if black is not None:
        bx0, by0, bx1, by1 = black
        img[by0:by1, bx0:bx1] = 0
    if on:
        tc = t if t_content is None else t_content
        pulse = int(math.floor(tc * pulse_hz + 1e-9))
        t_img = pulse / pulse_hz
        a = fluoro_image(canvas, box, t_img, pulse, v, seed)
        x0, y0, x1, y1 = box
        img[y0:y1, x0:x1] = a[..., None]
        if extra is not None:
            img = extra(img)
    return distractors(img)


def scenario_rect_motion(out):
    """Rectangle panel ON [2.0, 9.0) s, 7.5 pulses/s at 30 fps (4 frames per image), anatomy moving 20 px/s."""
    box = (300, 40, 600, 320)
    canvas = anatomy_canvas(600, 300, 11)
    n = 12 * FPS
    frames = (_panel_frame(k / FPS, 60 <= k < 270, box, canvas, 7.5, 20.0, 1) for k in range(n))
    p = Path(out) / "rect_motion.mp4"
    encode(p, frames)
    return p, dict(box=list(box), on_frame=60, off_frame=269, on_s=2.0, last_on_s=269 / FPS, fps=FPS,
                   frames_per_image=4, images_per_s=7.5, shape="rect", speed=1.0)


def scenario_circle_static(out):
    """Round image-intensifier field (inside a black square) ON [1.0, 7.0) s, 12 pulses/s at 30 fps (2,3 pattern),
    static anatomy."""
    cx, cy, r = 430, 180, 150
    box = (cx - r, cy - r, cx + r, cy + r)
    canvas = anatomy_canvas(2 * r + 10, 2 * r, 12)
    yy, xx = np.mgrid[0:2 * r, 0:2 * r]
    disk_m = ((xx + 0.5 - r) ** 2 + (yy + 0.5 - r) ** 2) <= r * r

    def mask_circle(img):
        sub = img[box[1]:box[3], box[0]:box[2]]
        sub[~disk_m] = 0
        return img
    n = 10 * FPS
    frames = (_panel_frame(k / FPS, 30 <= k < 210, box, canvas, 12.0, 0.0, 2, black=(270, 20, 590, 340),
                           extra=mask_circle) if 30 <= k < 210 else _panel_frame(k / FPS, False, box, canvas, 12.0,
                                                                                   0.0, 2)
              for k in range(n))
    p = Path(out) / "circle_static.mp4"
    encode(p, frames)
    return p, dict(box=list(box), on_frame=30, off_frame=209, on_s=1.0, last_on_s=209 / FPS, fps=FPS,
                   images_per_s=12.0, pattern={"2,3", "3,2"}, shape="circle", speed=1.0)


def scenario_counter_2x(out):
    """A recording at 7.5 pulses/s with a burned-in clock (mm:ss, 1 s resolution) PLAYED AT 2x: in video time the
    clock advances 2 s per second and images change 15 times per second (2 frames per image at 30 fps)."""
    box = (300, 80, 600, 330)
    canvas = anatomy_canvas(600, 300, 13)
    speed = 2.0
    font = _font(26)

    def frame(k):
        t = k / FPS
        tr = t * speed                                     # real time of this video frame
        img = room(t, 3)
        img[20:345, 280:620] = 0
        pulse = int(math.floor(tr * 7.5 + 1e-9))
        a = fluoro_image(canvas, box, pulse / 7.5, pulse, 10.0, 3)
        img[box[1]:box[3], box[0]:box[2]] = a[..., None]
        clock = 10 + int(math.floor(tr + 1e-9))
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        ImageDraw.Draw(im).text((300, 26), f"{clock // 60:02d}:{clock % 60:02d}", fill=(255, 255, 255), font=font)
        return distractors(np.asarray(im).astype(np.float32))
    n = 12 * FPS
    p = Path(out) / "counter_2x.mp4"
    encode(p, (frame(k) for k in range(n)))
    return p, dict(box=list(box), speed=speed, images_per_video_s=15.0, images_per_real_s=7.5, on_frame=0,
                   off_frame=n - 1)


def scenario_cut_replay(out):
    """Panel always ON. 0-5 s scene A (moving); HARD CUT at 5.0 s to scene B; at 10.0 s a REPLAY of scene A's
    1.0-4.0 s; at 13.0 s back to scene B (a cut)."""
    box = (300, 40, 600, 320)
    cA = anatomy_canvas(600, 300, 21)
    cB = np.flipud(anatomy_canvas(600, 300, 22)) * 0.7 + 40

    def content(t):
        if t < 5.0:
            return "A", t
        if t < 10.0:
            return "B", t
        if t < 13.0:
            return "A", 1.0 + (t - 10.0)
        return "B", t
    frames = []
    for k in range(16 * FPS):
        t = k / FPS
        which, tc = content(t)
        img = room(t, 4)
        pulse = int(math.floor(tc * 7.5 + 1e-9))
        cv, sd = (cA, 4) if which == "A" else (cB, 5)
        a = fluoro_image(cv, box, pulse / 7.5, pulse, 30.0, sd)
        img[box[1]:box[3], box[0]:box[2]] = a[..., None]
        frames.append(distractors(img))
    p = Path(out) / "cut_replay.mp4"
    encode(p, iter(frames))
    return p, dict(box=list(box), cuts_frames=[150, 300, 390], replay_s=(10.0, 13.0), original_s=(1.0, 4.0))


def scenario_vfr(out):
    """Variable frame rate: intervals alternate 1/30 and 1/15 s (pts on a 1/90000 time base); every frame a new
    image; panel always ON."""
    box = (300, 40, 600, 320)
    canvas = anatomy_canvas(600, 300, 31)
    t, pts = 0.0, []
    for k in range(240):
        pts.append(int(round(t * 90000)))
        t += (1 / 30) if k % 2 == 0 else (1 / 15)
    frames = []
    for k, p90 in enumerate(pts):
        tt = p90 / 90000.0
        img = room(tt, 6)
        a = fluoro_image(canvas, box, tt, k, 15.0, 6)
        img[box[1]:box[3], box[0]:box[2]] = a[..., None]
        frames.append(distractors(img))
    p = Path(out) / "vfr.mp4"
    encode(p, iter(frames), pts_list=pts)
    return p, dict(box=list(box), pts_s=[x / 90000.0 for x in pts], vfr=True)


SCENARIOS = dict(rect_motion=scenario_rect_motion, circle_static=scenario_circle_static,
                 counter_2x=scenario_counter_2x, cut_replay=scenario_cut_replay, vfr=scenario_vfr)


def _jsonable(o):
    if isinstance(o, set):
        return sorted(o)
    if isinstance(o, tuple):
        return list(o)
    return o


def make_all(out, names=None):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    truth = {}
    for name, fn in SCENARIOS.items():
        if names and name not in names:
            continue
        p, t = fn(out / "synthetic")
        truth[name] = dict(path=str(p), **{k: _jsonable(v) for k, v in t.items()})
    (out / "synthetic_truth.json").write_text(json.dumps(truth, indent=1), encoding="utf-8")
    return truth


def synthetic_frame(seed=0, circle=False):
    """One composite RGB frame (no video) with a known panel box, for fast unit tests."""
    if circle:
        cx, cy, r = 430, 180, 150
        box = (cx - r, cy - r, cx + r, cy + r)
    else:
        box = (300, 40, 600, 320)
    canvas = anatomy_canvas(600, box[2] - box[0], 40 + seed)
    img = room(0.3, seed)
    if circle:
        img[20:340, 270:590] = 0
    a = fluoro_image(canvas, box, 0.0, 0, 0.0, seed)
    x0, y0, x1, y1 = box
    if circle:
        yy, xx = np.mgrid[0:y1 - y0, 0:x1 - x0]
        m = ((xx + 0.5 - r) ** 2 + (yy + 0.5 - r) ** 2) <= r * r
        sub = img[y0:y1, x0:x1]
        sub[m] = a[m][..., None]
    else:
        img[y0:y1, x0:x1] = a[..., None]
    return distractors(img).astype(np.uint8), list(box)
