"""paper/cns2026/prep_v21_benzel_profile.py -- where slide 5's lines fall, on Benzel's own figures (v21, Greg, 2026-10-31).

v20 redrew Benzel's two panels with axes of its own, so slide 4's scans and slide 5's redraw had different frames and the
step between them jumped. v21 keeps the scans themselves as every click's base, the exact pictures slide 4 shows in the
exact boxes, and lays the gold tier's lines over them in the scans' own calibration: each level at the place of Benzel's
tick for it (the frame and ticks measured on the scans for v15, checked by overlaying his digitised lines on them), each
value on his y axis. A line that leaves his range is cut at the frame. His vertebra drawing is laid over the lines as a
transparent copy of itself, so no line hides it. T13 and L6, which his axes have no tick for, are open circles between
T12 and L1 and one step past L5.

The clicks, all on one title so the five read as one slide: purple, the gold tier reweighted to Panjabi's sex and age;
divided into men (blue) and women (red); Tan's build (green) and Alonge's sex and age (orange); then every decade of each
sex, 20s to 80s, blue for men and red for women, deeper the farther the decade's mean age lies from his cadavers' 46,
the canal's depth left out of that click: read on the CT it deepens by 5 to 7 mm from the 20s to the 80s at L3, the
opposite of what age does to a canal, so the flood fill leaks in older bone and its decades are not data.

Imported by make_cns_deck_v21_6min.py and render_v21_fingerprint.py; run alone it writes the phantoms and a check image.

    python paper/cns2026/prep_v21_benzel_profile.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from prep_v19_benzel_profile import EXTRA, PANELS as V19, stats  # noqa: E402

OLD = HERE / "figs_v14_6min"
V20 = HERE / "figs_v20_6min"
FIG = HERE / "figs_v21_6min"
PURPLE, BLUE, RED, GREEN, ORANGE = "#7A3E9D", "#1F5FA8", "#C8102E", "#1B7F4B", "#C26A00"
REFERENCE, EXTRA_INK = "#5A5A5A", "#333333"
STATES = ("panjabi", "sexes", "tan", "alonge", "agesex")
TARGETS = {"panjabi": ("panjabi", "panjabi"), "sexes": ("panjabi_men", "panjabi_women"), "tan": ("tan", "tan"),
           "alonge": ("alonge", "alonge")}
COLOURS = {"panjabi": (PURPLE, PURPLE), "sexes": (BLUE, RED), "tan": (GREEN, GREEN), "alonge": (ORANGE, ORANGE)}
REF_SOURCE = {"panjabi": "panjabi", "sexes": "panjabi", "tan": "tan", "alonge": "alonge", "agesex": "panjabi"}
LINE_PT, BAND_PT, REF_PT = 1.8, 1.25, 0.9
DIAMOND_PT, CIRCLE_PT, CIRCLE_LINE_PT = 3.4, 5.0, 1.0      # the reference diamonds' and the open circles' sizes
DECADES = (20, 30, 40, 50, 60, 70, 80)
PANJABI_AGE = 46.3                           # the mean of his twelve specimens' ages (panjabi_specimens.csv)
HUES = {"M": ("#B9CDEB", "#0A2F73"), "F": ("#F4B9C2", "#7E0716")}   # lightest and deepest of each sex
# slide 4's two pictures, the boxes every click reuses (left, top, width, height in EMU)
BOXES = {"body": (2377533, 1420000, 4203658, 3830000), "canal": (7031191, 1420000, 4241275, 3829999)}
# each scan's plot frame in its own pixels (top, bottom, left, right); the canal's bottom remeasured at 10 mm
FRAMES = {"body": (11, 368.5, 50, 486), "canal": (6, 372.5, 46, 491)}


class Panel:
    """One of Benzel's scans and its calibration: a level and a value to the scan's pixel and to the slide's EMU."""

    def __init__(self, name):
        spec = V19[name]
        self.name, self.spec = name, spec
        self.image = OLD / spec["image"]
        self.size = Image.open(self.image).size
        self.ticks, self.place = spec["axis"]()
        self.last = max(self.ticks.values())
        self.top, self.bottom, self.left, self.right = FRAMES[name]
        self.lo, self.hi = spec["ylim"] if name == "canal" else (15, 60)
        self.box = BOXES[name]
        self.keys = spec["keys"]

    def pixel(self, level, value):
        x = self.left + self.place[level] / self.last * (self.right - self.left)
        y = self.bottom - (value - self.lo) / (self.hi - self.lo) * (self.bottom - self.top)
        return x, y

    def emu(self, point):
        left, top, width, height = self.box
        return int(round(left + point[0] / self.size[0] * width)), int(round(top + point[1] / self.size[1] * height))

    def inside(self, point):
        return self.left - 0.01 <= point[0] <= self.right + 0.01 and self.top - 0.01 <= point[1] <= self.bottom + 0.01

    def clip(self, points):
        """The polyline cut at the plot frame: the runs that stay inside, each as its own list of pixels."""
        runs, run = [], []
        for a, b in zip(points, points[1:]):
            piece = clip_segment(a, b, (self.left, self.top, self.right, self.bottom))
            if piece is None:
                if len(run) > 1:
                    runs.append(run)
                run = []
                continue
            p, q = piece
            if run and (abs(run[-1][0] - p[0]) > 1e-6 or abs(run[-1][1] - p[1]) > 1e-6):
                if len(run) > 1:
                    runs.append(run)
                run = []
            if not run:
                run = [p]
            run.append(q)
        if len(run) > 1:
            runs.append(run)
        return runs


def clip_segment(a, b, rect):
    """Liang-Barsky: the part of segment a-b inside rect (x0, y0, x1, y1), or None."""
    x0, y0, x1, y1 = rect
    dx, dy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return None
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy)


def mix(light, deep, t):
    a = [int(light[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(deep[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def data():
    rw = json.load(open(V20 / "reweighted.json", encoding="utf-8"))
    bands = json.load(open(V20 / "bands.json", encoding="utf-8"))
    profile = json.load(open(HERE / "figs_v18_6min" / "profile.json", encoding="utf-8"))
    return rw, bands, profile


def references():
    """Every reference series as {(source, panel, chord): {level: mean}}, as v20 read them."""
    out = {}
    measures = {m: (name, chord) for name, spec in V19.items() for m, chord in zip(spec["panjabi"], ("width", "depth"))}
    for r in csv.DictReader(l for l in open(V20 / "panjabi.csv", encoding="utf-8") if not l.startswith("#")):
        if r["measure"] in measures:
            name, chord = measures[r["measure"]]
            out.setdefault(("panjabi", name, chord), {})[r["level"]] = float(r["mean"])
    for r in csv.DictReader(l for l in open(V20 / "references.csv", encoding="utf-8") if not l.startswith("#")):
        mean = float(r["mean"]) if r["mean"] else (54 * float(r["mean_men"]) + 66 * float(r["mean_women"])) / 120
        out.setdefault((r["source"], r["panel"], r["chord"]), {})[r["level"]] = mean
    return out


def band_colour(bands, group):
    far = max(abs(age - PANJABI_AGE) for age in bands["ages"].values())
    t = abs(bands["ages"][group] - PANJABI_AGE) / far
    light, deep = HUES[group[0]]
    return mix(light, deep, 0.12 + 0.88 * t)


def series_line(panel, measure):
    levels = sorted((lv for lv in measure if lv in panel.place and lv not in EXTRA), key=panel.place.get)
    return [panel.pixel(lv, measure[lv]["mean"]) for lv in levels]


def lines(panel, state, rw, bands):
    """This click's lines: (name, colour, points in scan pixels, width in points, dashed), the name shared across
    clicks where the line is the same line moving."""
    out = []
    for chord, key in zip(("w", "d"), panel.keys):
        if state == "agesex":
            if panel.name == "canal" and chord == "d":
                continue          # the CT canal's depth deepens with age, the flood fill leaking in older bone
            for sex in ("M", "F"):
                for decade in DECADES:
                    group = f"{sex}{decade}"
                    tag = sex.lower() if decade == 40 else group
                    out.append((f"{panel.name}_{chord}_{tag}", band_colour(bands, group),
                                series_line(panel, bands["bands"][group][key]), BAND_PT, chord == "d"))
            continue
        for sex, target, colour in zip(("m", "f"), TARGETS[state], COLOURS[state]):
            out.append((f"{panel.name}_{chord}_{sex}", colour, series_line(panel, rw["targets"][target]["measures"][key]),
                        LINE_PT, chord == "d"))
    return out


def points(panel, state, refs):
    """The reference series' points (chord, level, pixel) and the line through them, gray."""
    out = {}
    for chord, word in (("w", "width"), ("d", "depth")):
        series = refs.get((REF_SOURCE[state], panel.name, word), {})
        levels = sorted((lv for lv in series if lv in panel.place and lv not in EXTRA), key=panel.place.get)
        out[chord] = [(lv, panel.pixel(lv, series[lv])) for lv in levels]
    return out


def extras(panel, profile):
    """T13 and L6, every spine's means, as open circles: (name, pixel), width left of the level and depth right."""
    out = []
    for chord, key, shift in (("w", panel.keys[0], -0.13), ("d", panel.keys[1], 0.13)):
        for level in EXTRA:
            found = stats(profile, key, level)
            if found:
                x, y = panel.pixel(level, found[0])
                x += shift / panel.last * (panel.right - panel.left)
                out.append((f"{panel.name}_x_{chord}_{level}", (x, y)))
    return out


def phantom(panel):
    """Benzel's vertebra drawing cut from the scan with its paper made transparent, and where it sits in pixels."""
    x0, y0, x1, y1 = panel.spec["crop"]
    grey = Image.open(panel.image).convert("L").crop((x0, y0, x1, y1))
    scale = 4
    grey = grey.resize((grey.width * scale, grey.height * scale), Image.LANCZOS)
    alpha = grey.point(lambda v: 0 if v > 215 else min(255, int((235 - v) * 1.6)))
    ink = Image.new("RGBA", grey.size, (0, 0, 0, 0))
    ink.putalpha(alpha)
    path = FIG / f"phantom_{panel.name}.png"
    ink.save(path)
    return path, (x0, y0, x1, y1)


def check_image():
    """Every click's lines drawn on the scans, to look at before the deck is built."""
    from PIL import ImageDraw
    rw, bands, profile = data()
    refs = references()
    rows = []
    for state in STATES:
        row = []
        for name in BOXES:
            panel = Panel(name)
            k = 3
            im = Image.open(panel.image).convert("RGB").resize((panel.size[0] * k, panel.size[1] * k), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            for _, colour, pts, _, dashed in lines(panel, state, rw, bands):
                for run in panel.clip(pts):
                    d.line([(x * k, y * k) for x, y in run], fill=colour, width=4 if not dashed else 3)
            for chord, pts in points(panel, state, refs).items():
                for _, (x, y) in pts:
                    d.rectangle([x * k - 4, y * k - 4, x * k + 4, y * k + 4], fill=REFERENCE)
            for _, (x, y) in extras(panel, profile):
                d.ellipse([x * k - 7, y * k - 7, x * k + 7, y * k + 7], outline=EXTRA_INK, width=3)
            path, (x0, y0, x1, y1) = phantom(panel)
            ink = Image.open(path).resize(((x1 - x0) * k, (y1 - y0) * k))
            im.paste(ink, (x0 * k, y0 * k), ink)
            row.append(im)
        width = sum(i.width for i in row)
        strip = Image.new("RGB", (width, max(i.height for i in row)), "white")
        strip.paste(row[0], (0, 0))
        strip.paste(row[1], (row[0].width, 0))
        rows.append(strip)
    sheet = Image.new("RGB", (rows[0].width, sum(r.height for r in rows)), "white")
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.height
    sheet.save(FIG / "check_states.png")


if __name__ == "__main__":
    FIG.mkdir(exist_ok=True)
    check_image()
    print("wrote", FIG / "check_states.png")
