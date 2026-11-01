"""paper/cns2026/render_v21_fingerprint.py -- slide 11's animation, after the last click of slide 10 (v21, Greg, 2026-10-31).

Opens on slide 10 as it stands (both of Benzel's scans, every decade's lines, Panjabi's points, the open circles), drawn
from the same calibration (prep_v21_benzel_profile.py) into a picture covering both panels' boxes, so the cut from the
slide to the video does not show. Then: the canal panel steps back and the body panel's frame becomes the front face of
a box; each decade's depth line turns 90 degrees about the frame's floor into the screen and lies on the floor at its
true depth while the camera tilts, so each width line is seen where it lives, at its decade's depth, a curve in three
dimensions; four ideal spines rise on the right, each the vertebrae of the CT the closing pan is made from (one
ENHANCE.PET whole spine, figs_v21_6min/pan4) widened and deepened level by level to one decade's means, and each
lights gold with its line; then the lines leave as snakes,
turning square corners, and come to rest as the ridges of one fingerprint, palest at the centre where the decades lie
nearest Panjabi's cadavers' age, deepest at the edge. Its last frame is slide 12's left half.

    python paper/cns2026/render_v21_fingerprint.py
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402
from scipy import ndimage  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from prep_v21_benzel_profile import (BOXES, CIRCLE_LINE_PT, CIRCLE_PT, DECADES, DIAMOND_PT, EXTRA_INK,  # noqa: E402
                                     PANJABI_AGE, REF_PT, REFERENCE, Panel, band_colour, data, extras, lines, phantom,
                                     points, references)

FIG = HERE / "figs_v21_6min"
FRAMES = FIG / "fingerprint_frames"
OUT = FIG / "fingerprint.mp4"
FPS = int(os.environ.get("FINGERPRINT_FPS", 30))     # a lower rate is a quick look, not encoded
X0, Y0 = BOXES["body"][0], BOXES["body"][1]
X1 = BOXES["canal"][0] + BOXES["canal"][2]
W = 2400
SCALE = W / (X1 - X0)
H = int(round(BOXES["body"][3] * SCALE / 2)) * 2
PT = 12700 * SCALE                       # pixels a point at this scale
MPL_PX = 72 / 100                        # matplotlib points a pixel at dpi 100
GOLD = "#D9A21B"
FLASHED = ("M20", "F20", "M80", "F80")
LABEL = {"M20": "Men, 20s", "F20": "Women, 20s", "M80": "Men, 80s", "F80": "Women, 80s"}
# seconds: hold, step back, turn into depth, spines rise, four flashes, snakes, rest
T = {"hold": 0.6, "back": 1.5, "turn": 4.6, "rise": 5.4, "flash": 10.2, "snake": 17.6, "end": 18.8}
FLOOR, DEPTH_FAR = 15.0, 45.0


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def ease_in_out(u):
    u = min(max(u, 0.0), 1.0)
    return 0.5 - 0.5 * math.cos(math.pi * u)


def phase(t, start, end):
    return min(max((t - start) / (end - start), 0.0), 1.0)


def to_px(emu):
    return (emu[0] - X0) * SCALE, (emu[1] - Y0) * SCALE


def scan_px(panel, point):
    return to_px(panel.emu(point))


# ------------------------------------------------------------------------------------------------------- the scene
class Scene:
    def __init__(self):
        self.rw, self.bands, self.profile = data()
        self.refs = references()
        self.body, self.canal = Panel("body"), Panel("canal")
        self.scans = {p.name: np.asarray(Image.open(p.image).convert("RGB")) for p in (self.body, self.canal)}
        self.phantoms = {}
        for p in (self.body, self.canal):
            path, crop = phantom(p)
            self.phantoms[p.name] = (np.asarray(Image.open(path)), crop)
        self.groups = [f"{s}{d}" for s in "MF" for d in DECADES]
        self.curves = self.body_curves()

    def body_curves(self):
        """Each decade's body line as levels with width and depth, the levels both measures reach."""
        out = {}
        wkey, dkey = self.body.keys
        for g in self.groups:
            w, d = self.bands["bands"][g][wkey], self.bands["bands"][g][dkey]
            levels = sorted((lv for lv in w if lv in d and lv in self.body.place and lv not in ("T13", "L6")),
                            key=self.body.place.get)
            out[g] = [(self.body.pixel(lv, 15)[0], w[lv]["mean"], d[lv]["mean"]) for lv in levels]
        return out


# --------------------------------------------------------------------------------------------------- the 3D camera
class Camera:
    """Orthographic, about the body frame's centre: at elevation and azimuth 0 a point (x in scan pixels, width in mm,
    depth in mm) lands where the 2D plot puts (x, width), whatever its depth."""

    def __init__(self, panel):
        self.p = panel
        self.k = (panel.bottom - panel.top) / (panel.hi - panel.lo)        # scan pixels a millimetre
        self.cx = (panel.left + panel.right) / 2
        self.cy = (panel.lo + panel.hi) / 2
        self.cz = (FLOOR + DEPTH_FAR) / 2

    def project(self, pts, elev, azim, zoom=1.0, shift=(0.0, 0.0)):
        pts = np.asarray(pts, float)
        x = pts[:, 0] - self.cx
        y = (pts[:, 1] - self.cy) * self.k
        z = (pts[:, 2] - self.cz) * self.k
        a, e = math.radians(azim), math.radians(elev)
        x1 = x * math.cos(a) + z * math.sin(a)
        z1 = -x * math.sin(a) + z * math.cos(a)
        y2 = y * math.cos(e) + z1 * math.sin(e)
        sx = self.cx + x1 * zoom + shift[0]
        sy = self.p.bottom - (self.cy - self.p.lo) * self.k - y2 * zoom + shift[1]
        return np.stack([sx, sy], 1)


def view(t):
    """The camera at time t: elevation, azimuth, zoom and shift in scan pixels."""
    u = ease_in_out(phase(t, T["back"], T["turn"]))
    drift = (t - T["turn"]) * 1.6 if t > T["turn"] else 0.0
    drift = min(drift, 14.0)
    return 30 * u, -40 * u - drift, 1 - 0.2 * u, (30 * u, 34 * u)


# ------------------------------------------------------------------------------------------------------ the spines
def spine_meshes():
    """The CT's vertebrae as meshes in millimetres (x left-right, y back-front, z foot-head), from masks.npz."""
    import open3d as o3d
    from skimage import measure
    z = np.load(FIG / "pan4" / "masks.npz")
    names = [n for n in z.files if not n.endswith(("_shape", "_corner"))]
    meshes = {}
    for name in names:
        shape = tuple(int(v) for v in z[name + "_shape"])
        mask = np.unpackbits(z[name])[:int(np.prod(shape))].reshape(shape).astype(np.float32)
        mask = np.pad(mask, 3)
        mask = ndimage.gaussian_filter(mask, 1.0)   # no slice terraces
        verts, faces, _, _ = measure.marching_cubes(mask, 0.5)
        verts = verts - 3 + z[name + "_corner"]
        m = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(verts), o3d.utility.Vector3iVector(faces[:, ::-1]))
        rough = m.simplify_quadric_decimation(4000)
        m = rough.filter_smooth_taubin(8)
        if not np.isfinite(np.asarray(m.vertices)).all():
            m = rough                                  # smoothing can throw a degenerate mesh's points to NaN
        m.compute_vertex_normals()
        meshes[name] = m
    return meshes


def ideal(meshes, bands, group, wkey, dkey):
    """The CT's spine with each vertebra widened and deepened about its own centre by the decade's mean over the mean
    of every decade at that level."""
    import copy
    out = {}
    for name, mesh in meshes.items():
        m = copy.deepcopy(mesh)
        w = bands["bands"][group][wkey].get(name)
        d = bands["bands"][group][dkey].get(name)
        if w and d:
            ws = [bands["bands"][g][wkey][name]["mean"] for g in bands["bands"] if name in bands["bands"][g][wkey]]
            ds = [bands["bands"][g][dkey][name]["mean"] for g in bands["bands"] if name in bands["bands"][g][dkey]]
            sx, sy = w["mean"] / np.mean(ws), d["mean"] / np.mean(ds)
            v = np.asarray(m.vertices)
            c = v.mean(axis=0)
            v = (v - c) * np.array([sx, sy, 1.0]) + c
            m.vertices = __import__("open3d").utility.Vector3dVector(v)
            m.compute_vertex_normals()
        out[name] = m
    return out


class SpineRenderer:
    """The four ideal spines, each in a hidden Open3D window of its own, so each stands in its own column."""

    def __init__(self, scene, size):
        import open3d as o3d
        meshes = spine_meshes()
        wkey, dkey = scene.body.keys
        self.size = size
        self.column = (size[0] // 4) // 2 * 2
        self.spines, self.windows = [], []
        for g in FLASHED:
            whole = o3d.geometry.TriangleMesh()
            for m in ideal(meshes, scene.bands, g, wkey, dkey).values():
                whole += m
            whole.compute_vertex_normals()
            vis = o3d.visualization.Visualizer()
            vis.create_window(width=self.column, height=size[1], visible=False)
            vis.add_geometry(whole)
            opt = vis.get_render_option()
            opt.background_color = np.array([1.0, 1.0, 1.0])
            opt.light_on = True
            opt.mesh_show_back_face = True
            self.spines.append(whole)
            self.windows.append(vis)

    def render(self, colours, turn):
        out = []
        for mesh, vis, colour in zip(self.spines, self.windows, colours):
            mesh.paint_uniform_color(colour)
            vis.update_geometry(mesh)
            ctr = vis.get_view_control()
            a = math.radians(205 + turn)
            ctr.set_front([math.cos(a), math.sin(a), 0.12])
            ctr.set_up([0, 0, 1])
            ctr.set_zoom(0.56)                  # the camera looks at the mesh's centre already; set_lookat blanks it
            vis.poll_events()
            vis.update_renderer()
            out.append(np.asarray(vis.capture_screen_float_buffer(do_render=True)))
        return np.concatenate(out, axis=1)


# --------------------------------------------------------------------------------------------- the fingerprint path
def resample(poly, n):
    poly = np.asarray(poly, float)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(poly, axis=0).T))]
    s = np.linspace(0, seg[-1], n)
    return np.stack([np.interp(s, seg, poly[:, 0]), np.interp(s, seg, poly[:, 1])], 1)


def length(poly):
    return float(np.hypot(*np.diff(np.asarray(poly), axis=0).T).sum())


def ridges(n, centre, rng):
    """N fingerprint ridges, a whorl: each a nearly closed oval a little wider than the last, with the gentle waves and
    the opening a print has, inner first."""
    out = []
    for k in range(n):
        r = 30 + 13.4 * k
        gap = math.radians(14 + 8 * abs(math.sin(k * 0.9)))
        start = math.radians(250 + 70 * math.sin(k * 1.7) + 9 * k)
        theta = np.linspace(start, start + 2 * math.pi - gap, 260)
        wave = 1 + 0.035 * np.sin(2 * theta + 0.4 * k) + 0.018 * np.sin(5 * theta + 1.3 * k)
        spiral = 1 + 0.06 * (theta - theta[0]) / (2 * math.pi)
        rr = r * wave * spiral
        x = centre[0] + 0.80 * rr * np.cos(theta)
        y = centre[1] - rr * np.sin(theta) * (1 + 0.08 * np.clip(np.sin(theta), 0, 1))
        out.append(np.stack([x, y], 1))
    return out


def fillet(points, radius=22, steps=8):
    """A Manhattan path with each square corner rounded, so the snake turns as a car does, not as a pixel does."""
    pts = [np.asarray(points[0], float)]
    for a, b, c in zip(points, points[1:], points[2:]):
        a, b, c = map(lambda p: np.asarray(p, float), (a, b, c))
        u, v = (b - a), (c - b)
        lu, lv = np.linalg.norm(u), np.linalg.norm(v)
        if lu < 1e-6 or lv < 1e-6:
            continue
        r = min(radius, lu / 2, lv / 2)
        p, q = b - u / lu * r, b + v / lv * r
        for s in np.linspace(0, 1, steps):
            pts.append((1 - s) ** 2 * p + 2 * (1 - s) * s * b + s ** 2 * q)
    pts.append(np.asarray(points[-1], float))
    return np.array(pts)


def wander(head, heading, rng, bounds, turns=5):
    """Square turns about the screen from the head, alternately across and down, kept inside the bounds."""
    x0, y0, x1, y1 = bounds
    pts = [np.array(head, float)]
    horizontal = abs(heading[0]) >= abs(heading[1])
    sign = np.sign(heading[0] if horizontal else heading[1]) or 1
    for i in range(turns):
        step = rng.uniform(90, 260)
        p = pts[-1].copy()
        if horizontal:
            p[0] = np.clip(p[0] + sign * step, x0, x1)
        else:
            p[1] = np.clip(p[1] + sign * step, y0, y1)
        pts.append(p)
        horizontal = not horizontal
        sign = rng.choice([-1, 1])
    return pts


class Snake:
    def __init__(self, start, ridge, colour, rng):
        start = np.asarray(start, float)
        self.colour = colour
        heading = start[-1] - start[-2]
        bounds = (60, 60, W - 60, H - 60)
        corner = wander(start[-1], heading, rng, bounds)
        target = ridge[0]
        corner.append(np.array([target[0], corner[-1][1]]))
        corner.append(np.array(target))
        lead = fillet(corner)
        self.path = np.concatenate([start, lead[1:], ridge[1:]])
        seg = np.r_[0, np.cumsum(np.hypot(*np.diff(self.path, axis=0).T))]
        self.s = seg
        self.l0, self.l1 = length(start), length(ridge)
        self.total = seg[-1]

    def at(self, u):
        """The snake at progress u in [0, 1]: the stretch of its path behind its head."""
        head = self.l0 + (self.total - self.l0) * ease_in_out(u)
        body = self.l0 + (self.l1 - self.l0) * ease(u)
        s = np.linspace(max(head - body, 0), head, 160)
        return np.stack([np.interp(s, self.s, self.path[:, 0]), np.interp(s, self.s, self.path[:, 1])], 1)


# ----------------------------------------------------------------------------------------------------- the drawing
def figure():
    plt.rcParams.update({"font.family": "Arial", "font.weight": "bold"})
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    return fig, ax


def reset(ax):
    ax.clear()
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")


def show_scan(ax, scene, panel, alpha):
    left, top = to_px((panel.box[0], panel.box[1]))
    right, bottom = to_px((panel.box[0] + panel.box[2], panel.box[1] + panel.box[3]))
    ax.imshow(scene.scans[panel.name], extent=(left, right, bottom, top), alpha=alpha, interpolation="lanczos", zorder=1)


def show_phantom(ax, scene, panel, alpha):
    ink, (x0, y0, x1, y1) = scene.phantoms[panel.name]
    a, b = scan_px(panel, (x0, y0)), scan_px(panel, (x1, y1))
    rgba = ink.astype(np.float32) / 255
    rgba[..., 3] *= alpha
    ax.imshow(rgba, extent=(a[0], b[0], b[1], a[1]), interpolation="lanczos", zorder=8)


def polyline(ax, pts, colour, width_pt, dashed=False, alpha=1.0, z=4):
    """A line as PowerPoint draws it: DASH is four widths on and three off, a dot one on and one off, round."""
    pts = np.asarray(pts)
    style = {False: "solid", True: (0, (4, 3)), "dot": (0, (0.01, 2.0))}[dashed]
    ax.plot(pts[:, 0], pts[:, 1], color=colour, lw=width_pt * PT * MPL_PX, ls=style, alpha=alpha,
            solid_capstyle="round", dash_capstyle="round" if dashed == "dot" else "butt", solid_joinstyle="round",
            zorder=z)


def show_lines(ax, scene, panel, alpha, skip_body=False):
    for name, colour, pts, width, dashed in lines(panel, "agesex", scene.rw, scene.bands):
        if skip_body:
            continue
        for run in panel.clip(pts):
            polyline(ax, [scan_px(panel, p) for p in run], colour, width, dashed, alpha)
    for chord, pts in points(panel, "agesex", scene.refs).items():
        if len(pts) > 1:
            polyline(ax, [scan_px(panel, p) for _, p in pts], REFERENCE, REF_PT, "dot", alpha, 3)
            xy = np.array([scan_px(panel, p) for _, p in pts])
            ax.plot(xy[:, 0], xy[:, 1], ls="none", marker="D", ms=DIAMOND_PT * PT * MPL_PX * 0.75, color=REFERENCE, alpha=alpha,
                    zorder=5)
    for _, p in extras(panel, scene.profile):
        x, y = scan_px(panel, p)
        ax.plot([x], [y], "o", ms=CIRCLE_PT * PT * MPL_PX, mfc="white", mec=EXTRA_INK, mew=CIRCLE_LINE_PT * PT * MPL_PX,
                alpha=alpha, zorder=6)


def box_edges(cam, elev, azim, zoom, shift):
    p = cam.p
    xs, ys, zs = (p.left, p.right), (FLOOR, 60.0), (FLOOR, DEPTH_FAR)
    corners = {(i, j, k): (xs[i], ys[j], zs[k]) for i in (0, 1) for j in (0, 1) for k in (0, 1)}
    edges = []
    for a in corners:
        for axis in range(3):
            if a[axis] == 0:
                b = list(a)
                b[axis] = 1
                b = tuple(b)
                edges.append((a, b))
    return [(cam.project([corners[a], corners[b]], elev, azim, zoom, shift), a, b) for a, b in edges]


def show_box(ax, scene, cam, t, alpha):
    elev, azim, zoom, shift = view(t)
    panel = scene.body
    for seg, a, b in box_edges(cam, elev, azim, zoom, shift):
        front = a[2] == 0 and b[2] == 0
        px = [scan_px(panel, q) for q in seg]
        polyline(ax, px, "black", 1.1 if front else 0.8, False, alpha * (1 if front else 0.55), 2)
    ticks = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
    for v in ticks:
        q = cam.project([(panel.left, v, FLOOR)], elev, azim, zoom, shift)[0]
        x, y = scan_px(panel, q)
        ax.text(x - 10, y, str(v), ha="right", va="center", fontsize=8.5 * PT * MPL_PX * 1.25, alpha=alpha, zorder=7)
    for lv in panel.ticks:
        q = cam.project([(panel.pixel(lv, 15)[0], FLOOR, FLOOR)], elev, azim, zoom, shift)[0]
        x, y = scan_px(panel, q)
        ax.text(x, y + 12, lv[1:], ha="center", va="top", fontsize=8.5 * PT * MPL_PX * 1.25, alpha=alpha, zorder=7)
    for v in (15, 25, 35, 45):
        q = cam.project([(panel.right, FLOOR, v)], elev, azim, zoom, shift)[0]
        x, y = scan_px(panel, q)
        ax.text(x + 10, y + 4, str(v), ha="left", va="center", fontsize=8.5 * PT * MPL_PX * 1.25,
                alpha=alpha * phase(t, T["back"] + 0.8, T["turn"]), zorder=7)
    q = cam.project([(panel.right, FLOOR, DEPTH_FAR + 6)], elev, azim, zoom, shift)[0]
    x, y = scan_px(panel, q)
    ax.text(x + 12, y, "Depth (mm)", ha="left", va="center", fontsize=9.5 * PT * MPL_PX * 1.25,
            alpha=alpha * phase(t, T["back"] + 1.2, T["turn"]), zorder=7)
    q = cam.project([(panel.left, 37.5, FLOOR)], elev, azim, zoom, shift)[0]
    x, y = scan_px(panel, q)
    ax.text(x - 70, y, "Width (mm)", ha="center", va="center", rotation=90, fontsize=9.5 * PT * MPL_PX * 1.25,
            alpha=alpha, zorder=7)


def curve_states(scene, cam, t):
    """Every decade's width curve and depth line in scan pixels at time t: the width curve at its true depth, the
    depth line turned about the frame's floor by up to 90 degrees."""
    elev, azim, zoom, shift = view(t)
    turn = math.radians(90) * ease_in_out(phase(t, T["back"] + 0.2, T["turn"] - 0.3))
    out = {}
    for g, pts in scene.curves.items():
        pts = np.asarray(pts)
        width = cam.project(pts, elev, azim, zoom, shift)
        d = pts[:, 2]
        swung = np.stack([pts[:, 0], FLOOR + (d - FLOOR) * math.cos(turn), FLOOR + (d - FLOOR) * math.sin(turn)], 1)
        depth = cam.project(swung, elev, azim, zoom, shift)
        out[g] = (width, depth)
    return out


def glow(ax, pts, colour, strength):
    for w, a in ((16, 0.10), (10, 0.18), (6, 0.35)):
        polyline(ax, pts, colour, w / PT, False, a * strength, 9)


# ------------------------------------------------------------------------------------------------------ the frames
def flash_level(t, i):
    start = T["rise"] + i * (T["flash"] - T["rise"]) / len(FLASHED)
    dt = t - start
    if dt < 0:
        return 0.0
    if dt < 0.12:
        return dt / 0.12
    return math.exp(-(dt - 0.12) / 0.38) if dt < 1.15 else 0.0


def blend(a, b, u):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return a + (b - a) * u


def hex_rgb(h):
    return np.array([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])


def spine_panel(renderer, scene, t, alpha):
    colours, halos = [], []
    for i, g in enumerate(FLASHED):
        f = flash_level(t, i)
        base = blend(np.array([0.90, 0.87, 0.80]), hex_rgb(band_colour(scene.bands, g)), 0.18)
        colours.append(blend(base, hex_rgb(GOLD) * 1.08, f).clip(0, 1))
        halos.append(f)
    turn = (t - T["turn"]) * 4.0
    image = renderer.render(colours, turn)
    return image, halos


def build():
    FIG.mkdir(exist_ok=True)
    FRAMES.mkdir(exist_ok=True)
    scene = Scene()
    cam = Camera(scene.body)
    right = to_px((BOXES["canal"][0], BOXES["canal"][1]))[0]
    panel_size = (int(W - right), H)
    renderer = SpineRenderer(scene, (panel_size[0] - panel_size[0] % 2, panel_size[1]))
    rng = np.random.default_rng(1102)
    fig, ax = figure()
    n = int(round(T["end"] * FPS))
    snakes = None
    order = sorted(scene.groups, key=lambda g: abs(scene.bands["ages"][g] - PANJABI_AGE))
    for k in range(n):
        t = k / FPS
        reset(ax)
        u_back = ease(phase(t, T["hold"], T["back"]))
        u_fade = ease(phase(t, T["flash"], T["flash"] + 0.6))
        if t < T["back"] + 0.4:
            show_scan(ax, scene, scene.body, 1 - u_back)
            show_phantom(ax, scene, scene.body, 1 - u_back)
        if t < T["back"]:
            show_scan(ax, scene, scene.canal, 1 - u_back)
            show_phantom(ax, scene, scene.canal, 1 - u_back)
            show_lines(ax, scene, scene.canal, 1 - u_back)
            show_lines(ax, scene, scene.body, 1 - u_back, skip_body=True)
        if t >= T["hold"] and t < T["flash"] + 0.7:
            show_box(ax, scene, cam, t, u_back * (1 - u_fade))
        if t < T["flash"]:
            states = curve_states(scene, cam, t)
            lit = None
            for i, g in enumerate(FLASHED):
                if flash_level(t, i) > 0:
                    lit = (g, flash_level(t, i))
            for g, (width, depth) in states.items():
                colour = band_colour(scene.bands, g)
                dim = 1.0 if lit is None else (1.0 if g == lit[0] else 1 - 0.65 * lit[1])
                for pts, dashed in ((width, False), (depth, True)):
                    for run in scene.body.clip(pts.tolist()) if t < T["hold"] else [pts.tolist()]:
                        polyline(ax, [scan_px(scene.body, p) for p in run], colour, 1.25, dashed,
                                 dim * (0.75 if dashed and t > T["back"] else 1.0))
                if lit and g == lit[0]:
                    px = [scan_px(scene.body, p) for p in width]
                    glow(ax, px, GOLD, lit[1])
                    polyline(ax, px, GOLD, 1.25 + 1.6 * lit[1], False, lit[1], 10)
        if T["back"] + 0.8 < t < T["flash"] + 0.7:
            alpha = ease(phase(t, T["turn"], T["rise"])) * (1 - u_fade)
            if alpha > 0:
                image, halos = spine_panel(renderer, scene, t, alpha)
                ax.imshow(image, extent=(right, right + image.shape[1], H, 0), alpha=alpha, zorder=2)
                for i, (g, f) in enumerate(zip(FLASHED, halos)):
                    cx = right + renderer.column * (i + 0.5)
                    ax.text(cx, H - 36, LABEL[g], ha="center", va="center", color=band_colour(scene.bands, g),
                            fontsize=11 * PT * MPL_PX * 1.25, alpha=alpha, zorder=11)
                    if f > 0.02:
                        half = renderer.column / 2 - 6
                        ax.add_patch(Polygon([[cx - half, 30], [cx + half, 30], [cx + half, H - 70], [cx - half, H - 70]],
                                             closed=True, color=GOLD, alpha=0.12 * f * alpha, lw=0, zorder=3))
        if t >= T["flash"]:
            if snakes is None:
                states = curve_states(scene, cam, T["flash"])
                starts, colours = [], []
                for g in order:
                    width, depth = states[g]
                    starts += [np.array([scan_px(scene.body, p) for p in width]),
                               np.array([scan_px(scene.body, p) for p in depth])[::-1]]
                    colours += [band_colour(scene.bands, g)] * 2
                centre = (to_px((BOXES["body"][0] + BOXES["body"][2] / 2, 0))[0], H / 2 + 6)
                rings = ridges(len(starts), centre, rng)
                snakes = [Snake(s, r, c, rng) for s, r, c in zip(starts, rings, colours)]
            u = phase(t, T["flash"], T["snake"])
            for s in snakes:
                polyline(ax, s.at(u), s.colour, 1.7, False, 1.0, 5)
        fig.savefig(FRAMES / f"f{k:04d}.png", dpi=100)
        if k in (0, n - 1):
            fig.savefig(FIG / ("fingerprint_first.png" if k == 0 else "fingerprint_last.png"), dpi=100)
    plt.close(fig)
    if FPS == 30:
        encode()


def encode():
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(FRAMES / "f%04d.png"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    str(OUT)], check=True)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
