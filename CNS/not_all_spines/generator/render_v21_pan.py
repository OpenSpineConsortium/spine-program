"""paper/cns2026/render_v21_pan.py -- the closing video: a prone lateral pan from the sacrum (v21, Greg, 2026-10-31).

The frames are the job's own (grid/pan_render.py: one ENHANCE.PET CT, laterally projected and made real by FLUX.2
klein-9B, cut as a 30-frame-a-second pan from the sacrum to C2), turned a quarter so the patient lies prone as on the
table, the sacrum on the right and the head on the left, posterior up. On them, the level prototype's own boxes, every
frame (grid/pan_detect.sbatch, the reported detector, encoder and head); each box takes its name from the frame the
linker registers it (pan_link.py: counted up from the L5 the model named over the sacrum, and above the shoulders the
model's own reads), so a name appears as the pan reaches its body and never before. Box corners are smoothed over the
last few frames of the same body, causally. Below, the same CT's vertebrae in three dimensions, dark until each is
registered, then lit with its name, and a band where the field is; after the pan, the finished three-dimensional
registration turns once. Nothing is written in the video but the level names.

    python paper/cns2026/render_v21_pan.py RUN_FOLDER
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "grid"))
import pan_render  # noqa: E402
from pan_link import detections  # noqa: E402

FIG = HERE / "figs_v21_6min"
OUT, POSTER, META = FIG / "pan.mp4", FIG / "pan_first.png", FIG / "pan.json"
W, H, FPS = 1920, 1080, 30
FIELD = 680                       # the round field's frame, on screen
STRIP = (40, 676, 1840, 404)      # the 3D strip: left, top, width, height
FINALE, REST = 4.2, 1.0           # seconds of the closing turn, and held after it
BG = (8, 9, 11)
BOX = (64, 224, 128)
BONE, DARK, GLOW = np.array([0.93, 0.90, 0.84]), np.array([0.20, 0.21, 0.23]), np.array([0.25, 0.88, 0.50])
INFERRED = np.array([0.52, 0.60, 0.72])         # placed by the count and the shape on either side, never seen
FONT = "C:/Windows/Fonts/arialbd.ttf"


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * u)


# ----------------------------------------------------------------------------------------------- what the pan saw
class Pan:
    def __init__(self, run):
        self.run = run
        self.meta = json.load(open(run / "pan.json", encoding="utf-8"))
        self.linked = json.load(open(run / "linked.json", encoding="utf-8"))
        self.offsets = np.array(self.linked["offsets"])
        self.n = len(self.meta["centres"])
        dets = detections(run, self.linked["facing"])
        self.by_frame = {}
        for d in dets:
            self.by_frame.setdefault(d["frame"], []).append(d)
        self.bodies = self.linked["bodies"]
        self.registered = self.registration(dets)
        self.inferred = self.bridge()

    def body_of(self, d):
        x0, y0, x1, y1 = d["box"]
        row = (y0 + y1) / 2 - self.offsets[d["frame"]][0]
        near = [b for b in self.bodies if abs(b["row"] - row) < 0.5 * b["height"]]
        if not near:
            return None
        best = min(near, key=lambda b: abs(b["row"] - row))
        if best["how"] == "shape" and d["level"] != best["name"] and not d["abstain"]:
            return None
        return best

    def registration(self, dets):
        """The frame each body's name is first known: a counted body at its first sight, a body named by the model
        once five of its frames have named it."""
        out, votes = {}, {}
        for d in sorted(dets, key=lambda d: d["frame"]):
            b = self.body_of(d)
            if b is None:
                continue
            if b["how"] == "count":
                out.setdefault(b["name"], d["frame"])
            elif not d["abstain"] and d["level"] == b["name"]:
                votes[b["name"]] = votes.get(b["name"], 0) + 1
                if votes[b["name"]] >= 5:
                    out.setdefault(b["name"], d["frame"])
        if "L5" in out:
            out["S1"] = out["L5"]            # the count's base: the sacrum under the L5 the model named
        return out

    def bridge(self):
        """The levels the detector never saw, under the shoulders, placed between the highest body counted from the
        sacrum and the lowest the model named itself, where the gap gives each missing body a pitch between 0.55 and 1.35
        of the two ends' heights (the bodies under the shoulders are smaller than T5); registered when the second of
        the two ends is."""
        from pan_link import UP
        counted = [b for b in self.bodies if b["how"] == "count"]
        shaped = [b for b in self.bodies if b["how"] == "shape"]
        if not counted or not shaped:
            return {}
        top = min(counted, key=lambda b: b["row"])
        low = max(shaped, key=lambda b: b["row"])
        i, j = UP.index(top["name"]), UP.index(low["name"])
        missing = UP[i + 1:j]
        if not missing:
            return {}
        each = (top["row"] - low["row"]) / (len(missing) + 1)          # the pitch the gap gives each body
        if not 0.55 <= each / ((top["height"] + low["height"]) / 2) <= 1.35:
            return {}
        when = max(self.registered.get(top["name"], 0), self.registered.get(low["name"], 0))
        return {name: when for name in missing}

    def frames(self):
        panorama = np.asarray(Image.open(self.run / "flux_s0.png"), np.float32) / 255
        rng = np.random.default_rng(20261102)
        for centre in self.meta["centres"]:
            yield pan_render.fluoro(panorama, centre, rng)


class Smoother:
    """Each body's box, held in the column's own coordinates and eased toward each new sighting, so a box moves with
    the field and not with the detector's frame-to-frame jitter."""

    def __init__(self, alpha=0.45):
        self.alpha, self.state = alpha, {}

    def __call__(self, key, box, offset):
        g = np.array(box, float) - np.array([offset[1], offset[0], offset[1], offset[0]])
        if key in self.state:
            g = self.state[key] + self.alpha * (g - self.state[key])
        self.state[key] = g
        return g + np.array([offset[1], offset[0], offset[1], offset[0]])


# ----------------------------------------------------------------------------------------------------- the spine
class Spine3D:
    """The CT's vertebrae as meshes, rendered from the patient's side with the head to the left and the back up."""

    def __init__(self, run, size):
        import open3d as o3d
        from skimage import measure
        self.o3d = o3d
        z = np.load(run / "masks.npz")
        self.meshes, self.centres = {}, {}
        for name in [n for n in z.files if not n.endswith(("_shape", "_corner"))]:
            shape = tuple(int(v) for v in z[name + "_shape"])
            mask = np.pad(np.unpackbits(z[name])[:int(np.prod(shape))].reshape(shape).astype(np.float32), 3)
            mask = ndimage.gaussian_filter(mask, 1.0)   # no slice terraces
            verts, faces, _, _ = measure.marching_cubes(mask, 0.5)
            verts = verts - 3 + z[name + "_corner"]
            m = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(verts), o3d.utility.Vector3iVector(faces[:, ::-1]))
            rough = m.simplify_quadric_decimation(9000)
            m = rough.filter_smooth_taubin(8)
            if not np.isfinite(np.asarray(m.vertices)).all():
                m = rough                              # smoothing can throw a degenerate mesh's points to NaN
            m.compute_vertex_normals()
            key = "S1" if name == "S" else name
            self.meshes[key] = m
            self.centres[key] = np.nanmean(np.asarray(m.vertices), axis=0)
        self.window(size)

    def window(self, size):
        if hasattr(self, "vis"):
            self.vis.destroy_window()
        self.size = size
        self.vis = self.o3d.visualization.Visualizer()
        self.vis.create_window(width=size[0], height=size[1], visible=False)
        for m in self.meshes.values():
            self.vis.add_geometry(m)
        opt = self.vis.get_render_option()
        opt.background_color = np.array(BG) / 255
        opt.light_on = True
        opt.mesh_show_back_face = True

    def camera(self, azim, fill):
        """A camera far off the patient's left side (head left, back up), turned by azim about the long axis's
        vertical, scaled so the spine fills FILL of the window's width or 80 per cent of its height."""
        pts = np.concatenate([np.asarray(m.vertices) for m in self.meshes.values()])
        centre = (pts.min(axis=0) + pts.max(axis=0)) / 2
        a = math.radians(azim)
        turn = np.array([[math.cos(a), 0, -math.sin(a)], [0, 1, 0], [math.sin(a), 0, math.cos(a)]])
        base = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]], float)      # camera x = -z, y = y, z = x
        rot = base @ turn
        cam = (pts - centre) @ rot.T
        span = cam.max(axis=0) - cam.min(axis=0)
        w, h = self.size
        scale = min(fill * w / span[0], 0.8 * h / span[1])
        distance = 6000.0
        ext = np.eye(4)
        ext[:3, :3] = rot
        ext[:3, 3] = np.array([0, 0, distance]) - rot @ centre
        params = self.o3d.camera.PinholeCameraParameters()
        params.intrinsic = self.o3d.camera.PinholeCameraIntrinsic(w, h, scale * distance, scale * distance, w / 2 - 0.5,
                                                                  h / 2 - 0.5)
        params.extrinsic = ext
        return params

    def render(self, colours, azim=0.0, fill=0.92):
        for name, m in self.meshes.items():
            m.paint_uniform_color(colours.get(name, DARK))
            self.vis.update_geometry(m)
        self.params = self.camera(azim, fill)
        ctr = self.vis.get_view_control()
        ctr.convert_from_pinhole_camera_parameters(self.params, allow_arbitrary=True)
        self.vis.poll_events()
        self.vis.update_renderer()
        image = np.asarray(self.vis.capture_screen_float_buffer(do_render=True))
        return image, self.project

    def project(self, points):
        k, ext = self.params.intrinsic.intrinsic_matrix, self.params.extrinsic
        p = np.c_[np.asarray(points), np.ones(len(points))] @ ext.T
        uv = p[:, :3] @ k.T
        return uv[:, :2] / uv[:, 2:3]


# ------------------------------------------------------------------------------------------------------ drawing
def font(size):
    return ImageFont.truetype(FONT, size)


def to_screen(box, size):
    """An upright frame's box (x0, y0, x1, y1), the frame turned a quarter counter-clockwise (head left, back up),
    scaled to the field on screen."""
    x0, y0, x1, y1 = box
    n = 1024
    s = FIELD / n
    return np.array([y0 * s, (n - 1 - x1) * s, y1 * s, (n - 1 - x0) * s])


def colours_at(spine, pan, k):
    out = {}
    for name in spine.meshes:
        f, g = pan.registered.get(name), pan.inferred.get(name)
        if f is not None and k >= f:
            out[name] = np.clip(BONE + (GLOW - BONE) * math.exp(-(k - f) / 9.0), 0, 1)
        elif g is not None and k >= g:
            out[name] = INFERRED
        else:
            out[name] = DARK
    return out


def field_band(spine, pan, k):
    """The field's span along the spine on the strip, from the frame's centre in the panorama back to the CT's z."""
    zmax, ymax, r0, _ = pan.meta["to_panorama"]
    px = pan.meta["mm_per_px"]
    row = pan.meta["centres"][k][0]
    z = zmax - (row + r0) * px
    half = 0.47 * pan.meta["frame"] * px
    mid = np.mean(list(spine.centres.values()), axis=0)
    a, b = mid.copy(), mid.copy()
    a[2], b[2] = z - half, z + half
    return a, b


def compose(pan, spine, smoother, frame, k, strip_img, project):
    canvas = Image.new("RGB", (W, H), BG)
    grey = (np.rot90(frame, 1) * 255).astype(np.uint8)
    field = Image.fromarray(grey).resize((FIELD, FIELD), Image.LANCZOS).convert("RGB")
    fx, fy = (W - FIELD) // 2, 6
    canvas.paste(field, (fx, fy))
    strip = Image.fromarray((strip_img * 255).astype(np.uint8))
    canvas.paste(strip, (STRIP[0], STRIP[1]))
    over = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    label = font(46)
    for det in pan.by_frame.get(k, []):
        body = pan.body_of(det)
        key = body["name"] if body else f"x{k}_{det['box'][1]}"
        box = smoother(key, det["box"], pan.offsets[k])
        x0, y0, x1, y1 = (to_screen(box, FIELD) + [fx, fy, fx, fy]) * 2
        named = body is not None and k >= pan.registered.get(body["name"], 10 ** 9)
        colour = BOX + (235,) if named else (150, 150, 150, 150)
        d.rounded_rectangle([x0, y0, x1, y1], radius=10, outline=colour, width=5 if named else 3)
        if named:
            text = body["name"]
            tw = d.textlength(text, font=label)
            tx, ty = (x0 + x1) / 2 - tw / 2, y0 - 60
            d.text((tx + 2, ty + 2), text, font=label, fill=(0, 0, 0, 160))
            d.text((tx, ty), text, font=label, fill=(255, 255, 255, 245))
    a, b = field_band(spine, pan, k)
    (ua, _), (ub, _) = project([a, b])
    left, right = sorted((ua, ub))
    sx, sy, sw, sh = STRIP
    left, right = max(left, 0) + sx, min(right, sw) + sx
    d.rounded_rectangle([left * 2, (sy + 8) * 2, right * 2, (sy + sh - 8) * 2], radius=24,
                        fill=(255, 255, 255, 18), outline=(255, 255, 255, 90), width=3)
    small = font(30)
    shown = [(n, (230, 230, 230, 230)) for n, f in pan.registered.items() if k >= f and n in spine.centres]
    shown += [(n, (140, 160, 190, 220)) for n, f in pan.inferred.items() if k >= f and n in spine.centres]
    if shown:
        uv = project([spine.centres[n] for n, _ in shown])
        for (n, ink), (u, v) in zip(shown, uv):
            tw = d.textlength(n, font=small)
            d.text(((sx + u) * 2 - tw / 2, (sy + sh - 30) * 2), n, font=small, fill=ink)
    over = over.resize((W, H), Image.LANCZOS)
    canvas.paste(over, (0, 0), over)
    return canvas


def finale(pan, spine, t, size):
    """The finished registration turning once: every registered vertebra lit and named."""
    u = ease(t / FINALE)
    colours = {n: (BONE if n in pan.registered else INFERRED if n in pan.inferred else DARK) for n in spine.meshes}
    image, project = spine.render(colours, azim=-38 * math.sin(math.pi * u) - 12 * u, fill=0.86 + 0.04 * u)
    canvas = Image.fromarray((image * 255).astype(np.uint8)).convert("RGB")
    over = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    names = [(n, (235, 235, 235, 235)) for n in pan.registered if n in spine.centres]
    names += [(n, (140, 160, 190, 225)) for n in pan.inferred if n in spine.centres]
    uv = project([spine.centres[n] for n, _ in names])
    label = font(42)
    for (n, ink), (x, y) in zip(names, uv):
        tw = d.textlength(n, font=label)
        d.text((x * 2 - tw / 2, (y + 95) * 2), n, font=label, fill=ink)
    over = over.resize((W, H), Image.LANCZOS)
    canvas.paste(over, (0, 0), over)
    return canvas


def build(run):
    import imageio_ffmpeg
    pan = Pan(run)
    spine = Spine3D(run, (STRIP[2], STRIP[3]))
    smoother = Smoother()
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                             "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "15",
                             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT)], stdin=subprocess.PIPE)
    last = None
    every = int(__import__("os").environ.get("PAN_EVERY", 1))     # above 1, a quick look: every nth frame
    for k, frame in enumerate(pan.frames()):
        if k % every:
            continue
        strip, project = spine.render(colours_at(spine, pan, k), azim=0.0, fill=0.95)
        image = compose(pan, spine, smoother, frame, k, strip, project)
        if k == 0:
            image.save(POSTER)
        proc.stdin.write(np.asarray(image).tobytes())
        if every > 1:
            image.save(FIG / f"pan_look_{k:04d}.png")
        last = image
    spine.window((W, H))
    cross = int(0.8 * FPS)
    for j in range(0, int((FINALE + REST) * FPS), every):
        t = min(j / FPS, FINALE)
        image = finale(pan, spine, t, (W, H))
        if j < cross:
            image = Image.blend(last, image, ease(j / cross))
        proc.stdin.write(np.asarray(image).tobytes())
        if every > 1:
            image.save(FIG / f"pan_look_end_{j:04d}.png")
    proc.stdin.close()
    proc.wait()
    seconds = pan.n / FPS + FINALE + REST
    json.dump({"seconds": round(seconds, 2), "frames": pan.n, "registered": pan.registered, "inferred": pan.inferred,
               "named": {b["name"]: b["truth"] for b in pan.bodies}}, open(META, "w", encoding="utf-8"), indent=1)
    print("wrote", OUT, round(seconds, 1), "s;", "registered", len(pan.registered))


if __name__ == "__main__":
    build(Path(sys.argv[1]))
