"""paper/cns2026/render_v22_anomalies.py -- the anomalies slide's film: eight spines of the gallery turning (v22, Greg, 2026-11-01).

Greg asked for a slide with all his anomalies in 3D, turning, from the consortium's gallery page. These are the
gallery's own surfaces (openspineconsortium.com/assets/gallery/<case>.json and .bin, decimated from the released
CTSpinoPelvic1K segmentations), its eight anomalous cases with the gallery's own titles, which name what is visible
and never a level. Each spine is drawn in bone, the structures the gallery's caption is about in gold (the same gold
the fingerprint film flashes), a cage in steel, with the two bodies it lies between in gold since bone hides it; the femurs are left out so the spine fills its tile. All eight turn
once together, at one constant speed, about their own long axes, over 12 s, so the last frame is the first and the
film holds still when it ends. Nothing but the eight titles is written in the film.

    python paper/cns2026/render_v22_anomalies.py

Writes figs_v22_6min/anomalies.mp4 and anomalies_first.png; the gallery's files are fetched once into
figs_v22_6min/gallery/ (not committed: they are the website's).
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FIG = HERE / "figs_v22_6min"
GALLERY = FIG / "gallery"
SITE = "https://openspineconsortium.com/assets/gallery/"
SIZE = (1920, 1080)
GRID = (4, 2)
LABEL = 64                          # the strip under each tile that holds its title
SUPER = 2                           # each tile drawn at twice the size and brought down, for clean edges
FPS, SECONDS = 30, 12.0
START = -35.0                       # degrees: from the patient's left and in front
FONT = "C:/Windows/Fonts/arialbd.ttf"
BONE = (0.90, 0.87, 0.80)
GOLD = (0.86, 0.64, 0.12)
STEEL = (0.55, 0.60, 0.68)
INK = (51, 51, 51)
CASES = (
    ("1090", "A thirteenth rib-bearing level", lambda s: "lumbar" in s["name"]),
    ("0268", "A process that meets the ala", lambda s: s["name"] in ("L6", "sacrum")),
    ("0349", "The widest transverse span", lambda s: s["name"] in ("L5", "L6", "sacrum")),
    ("0033", "A part-fused transitional vertebra", lambda s: s["name"] in ("L6", "sacrum")),
    ("0068", "A fusion that surgery made", lambda s: s["name"] in ("L5", "L6")),
    ("0631", "A hypoplastic twelfth rib", lambda s: s["name"] in ("rib_left_12", "rib_right_12")),
    ("0378", "Aplastic on one side only", lambda s: s["name"] in ("rib_left_12", "rib_right_12")),
    ("1153", "Eleven rib pairs", lambda s: s["name"] in ("rib_left_11", "rib_right_11")),
)


def fetch(case):
    GALLERY.mkdir(parents=True, exist_ok=True)
    for ext in ("json", "bin"):
        path = GALLERY / f"{case}.{ext}"
        if not path.is_file():
            with urllib.request.urlopen(SITE + f"{case}.{ext}", timeout=60) as r:
                path.write_bytes(r.read())
    return json.load(open(GALLERY / f"{case}.json", encoding="utf-8")), (GALLERY / f"{case}.bin").read_bytes()


def meshes(case, focus):
    """The case's structures as Open3D meshes in millimetres (R, A, S), each painted for its part in the story."""
    import open3d as o3d
    head, buf = fetch(case)
    lo, hi = np.array(head["bbox_lo"]), np.array(head["bbox_hi"])
    out = []
    for st in head["structures"]:
        if st["name"].startswith("femur"):
            continue
        pos = np.frombuffer(buf, np.uint16, st["pos"][1] // 2, st["pos"][0]).reshape(-1, 3)
        kind = np.uint32 if st.get("idx_bytes") == 4 else np.uint16
        idx = np.frombuffer(buf, kind, st["idx"][1] // np.dtype(kind).itemsize, st["idx"][0]).reshape(-1, 3)
        verts = lo + pos / head["quant"] * (hi - lo)
        m = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(verts), o3d.utility.Vector3iVector(idx.astype(np.int32)))
        m.compute_vertex_normals()
        m.paint_uniform_color(STEEL if st["kind"] == "hardware" else GOLD if focus(st) else BONE)
        out.append(m)
    return out


class Tile:
    """One case in a hidden window of its own, the camera turning about the spine's long axis at a fixed scale."""

    def __init__(self, case, focus, size):
        import open3d as o3d
        self.o3d, self.size = o3d, size
        self.parts = meshes(case, focus)
        pts = np.concatenate([np.asarray(m.vertices) for m in self.parts])
        self.centre = (pts.min(axis=0) + pts.max(axis=0)) / 2
        reach = np.hypot(pts[:, 0] - self.centre[0], pts[:, 1] - self.centre[1]).max()
        height = pts[:, 2].max() - pts[:, 2].min()
        self.scale = min(0.92 * size[0] / (2 * reach), 0.94 * size[1] / height)
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window(width=size[0], height=size[1], visible=False)
        for m in self.parts:
            self.vis.add_geometry(m)
        opt = self.vis.get_render_option()
        opt.background_color = np.array([1.0, 1.0, 1.0])
        opt.light_on = True
        opt.mesh_show_back_face = True

    def render(self, degrees):
        a = math.radians(degrees)
        back = np.array([math.sin(a), math.cos(a), 0.0])          # from the spine toward the camera
        forward, down = -back, np.array([0.0, 0.0, -1.0])
        right = np.cross(down, forward)
        rot = np.stack([right, down, forward])
        distance = 6000.0
        ext = np.eye(4)
        ext[:3, :3] = rot
        ext[:3, 3] = np.array([0, 0, distance]) - rot @ self.centre
        w, h = self.size
        params = self.o3d.camera.PinholeCameraParameters()
        f = self.scale * distance
        params.intrinsic = self.o3d.camera.PinholeCameraIntrinsic(w, h, f, f, w / 2 - 0.5, h / 2 - 0.5)
        params.extrinsic = ext
        self.vis.get_view_control().convert_from_pinhole_camera_parameters(params, allow_arbitrary=True)
        self.vis.poll_events()
        self.vis.update_renderer()
        return np.asarray(self.vis.capture_screen_float_buffer(do_render=True))


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    return lines + [line]


def titles(cell):
    """The eight titles, drawn once on a white frame the tiles are pasted into."""
    base = Image.new("RGB", SIZE, "white")
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype(FONT, 25)
    for k, (_, title, _) in enumerate(CASES):
        x0, y0 = (k % GRID[0]) * cell[0], (k // GRID[0]) * cell[1]
        lines = wrap(draw, title, font, cell[0] - 24)
        for i, line in enumerate(lines):
            y = y0 + cell[1] - LABEL + 4 + i * 29 - (len(lines) - 1) * 6
            draw.text((x0 + cell[0] / 2, y), line, font=font, fill=INK, anchor="ma")
    return base


def main():
    import imageio_ffmpeg
    FIG.mkdir(exist_ok=True)
    cell = (SIZE[0] // GRID[0], SIZE[1] // GRID[1])
    size = (cell[0], cell[1] - LABEL)
    tiles = [Tile(case, focus, (size[0] * SUPER, size[1] * SUPER)) for case, _, focus in CASES]
    base = titles(cell)
    frames = int(round(FPS * SECONDS))
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{SIZE[0]}x{SIZE[1]}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "21", "-preset", "slow",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(FIG / "anomalies.mp4")]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(frames + 1):
        degrees = START + 360.0 * f / frames
        frame = base.copy()
        for k, tile in enumerate(tiles):
            image = Image.fromarray((np.clip(tile.render(degrees), 0, 1) * 255).astype(np.uint8))
            image = image.resize(size, Image.LANCZOS)
            frame.paste(image, ((k % GRID[0]) * cell[0], (k // GRID[0]) * cell[1]))
        if f == 0:
            frame.save(FIG / "anomalies_first.png")
        pipe.stdin.write(frame.tobytes())
    pipe.stdin.close()
    pipe.wait()
    json.dump({"seconds": round((frames + 1) / FPS, 2), "cases": [c for c, _, _ in CASES]},
              open(FIG / "anomalies.json", "w", encoding="utf-8"), indent=1)
    print("anomalies.mp4", frames + 1, "frames")


if __name__ == "__main__":
    main()
