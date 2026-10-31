"""paper/cns2026/prep_v16_benzel_profile.py -- slide 5 of the 6-minute CNS deck, v16 (Greg, 2026-10-31, evening).

v15's two Benzel panels (prep_v15_benzel_profile.py says how they are drawn), with two changes Greg asked for after
seeing odd gaps between Benzel's lines and the gold tier's in the neck and in the canal:

- Panjabi's cadaveric means with one SD (SEM x sqrt(12)), in red, on both panels: upper end-plate width and depth
  (EPWu, EPDu) on the body panel, canal width and depth (SCW, SCD) on the canal panel, from figs_v16_6min/panjabi.csv
  (bordercall schwingcheck/data/panjabi_long.csv at fbf32d4). Benzel's Fig. 1.9 is Panjabi's canal table to the
  decimal at C2 to C7, and his Fig. 1.1 width follows Panjabi's EPWu.
- Each gold tier line drawn only where bordercall's engine read the measure by its own definition. The engine flags
  the vertebrae where it read a stand-in instead (grid/level_profile.py, STAND_INS), and a level is drawn only where
  at least half its vertebrae were read by the definition, over those vertebrae alone (profile.json's as_defined).
  In the neck no foramen transversarium is found closed in 89 to 99 per cent of vertebrae, so the body is cut at the
  canal's walls and its width is the canal's plus two millimetres, and no pedicle is found on both sides in about 99
  per cent, so the canal's width is the hole's width through its middle: neither is drawn. Canal width is the
  greatest interpedicular distance (Eisenstein 1977, the reading Panjabi's SCW is, interpedicular_max), which matches
  Panjabi within about a millimetre from T2 to L3 where the pedicles are found.

    python paper/cns2026/prep_v16_benzel_profile.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OLD = HERE / "figs_v14_6min"
FIG = HERE / "figs_v16_6min"
FIG.mkdir(exist_ok=True)

OURS = "#1F5FA8"
PANJABI = "#C8102E"
DEFINED_SHARE = 0.5
EXTRA = ("T13", "L6")
LEAST, LEAST_EXTRA = 5, 3
EMU = 914400
DPI = 300


def thoracic_between(first, last, start, end):
    """The thoracic levels strictly between two of Benzel's ticks, placed evenly between them."""
    names = [f"T{i}" for i in range(first + 1, last)]
    step = (end - start) / (len(names) + 1)
    return {name: start + step * (k + 1) for k, name in enumerate(names)}


def body_axis():
    ticks = {"C3": 0, "C5": 1, "C7": 2, "T2": 3, "T7": 4, "T12": 5, "L1": 6, "L2": 7, "L3": 8, "L4": 9, "L5": 10}
    place = dict(ticks, C4=0.5, C6=1.5, T1=2.5, T13=5.5, L6=11)
    place.update(thoracic_between(2, 7, 3, 4))
    place.update(thoracic_between(7, 12, 4, 5))
    return ticks, place


def canal_axis():
    ticks = {"C2": 0, "C3": 1, "C4": 2, "C5": 3, "C6": 4, "C7": 5, "T2": 6, "T7": 7, "T12": 8,
             "L1": 9, "L2": 10, "L3": 11, "L4": 12, "L5": 13}
    place = dict(ticks, T1=5.5, T13=8.5, L6=14)
    place.update(thoracic_between(2, 7, 6, 7))
    place.update(thoracic_between(7, 12, 7, 8))
    return ticks, place


PANELS = {
    "body": {
        "image": "benzel_fig1_1.png", "frame": (11, 368.5, 50, 486), "crop": (126, 33, 232, 143),
        "axis": body_axis, "ylim": (15, 60), "yticks": range(15, 61, 5),
        "ylabel": "Vertebral Body Diameters (mm)", "keys": ("body_w_mid", "body_d_mid"),
        "panjabi": ("endplate", "endplate_depth"),
        "benzel_width": [16.6, 18.5, 22.6, 28.8, 30.0, 40.0, 42.1, 44.0, 45.9, 46.9, 47.9],
        "benzel_depth": [15.5, 16.6, 17.5, 20.0, 27.0, 28.0, 29.0, 29.9, 30.9, 31.9, 31.0],
        "labels": (("Width", "T7", 36.0), ("Depth", "T4", 16.6)),
        "regions": (("Cervical", "C5"), ("Thoracic", "T7"), ("Lumbar", "L3")),
        "legend": ("full", 0.995, 0.005, "lower right"), "emu": (4203658, 3830000), "out": "benzel_body.png",
    },
    "canal": {
        "image": "benzel_fig1_9.png", "frame": (6, 368.5, 46, 491), "crop": (226, 28, 330, 122),
        "axis": canal_axis, "ylim": (10, 30), "yticks": range(10, 31, 5),
        "ylabel": "Spinal Canal Diameter (mm)", "keys": ("interpedicular_max", "canal_ap"),
        "panjabi": ("canal_w", "canal_ap"),
        "benzel_width": [24.4, 23.1, 24.5, 24.5, 25.9, 24.6, 19.1, 17.1, 20.5, 22.0, 22.0, 22.8, 22.9, 22.9],
        "benzel_depth": [20.8, 16.2, 17.8, 17.5, 17.9, 15.0, 15.1, 16.4, 17.0, 17.0, 16.0, 16.2, 16.1, 17.0],
        "labels": (("Width", "L2", 26.6), ("Depth", "L3", 18.6)),
        "regions": (("Cervical", "C4"), ("Thoracic", "T7"), ("Lumbar", "L3")),
        "legend": ("short", 0.005, 0.995, "upper left"), "emu": (4241275, 3829999), "out": "benzel_canal.png",
    },
}


def stats(profile, key, level):
    """The level's mean, SD and n over the vertebrae read by the measure's definition, where enough were read (three
    for T13 and L6, five elsewhere) and they are at least DEFINED_SHARE of all read, else None."""
    row = profile["measures"].get(key, {}).get(level)
    defined = profile.get("as_defined", {}).get(key, {}).get(level)
    if defined is not None and row:
        if defined["n"] < DEFINED_SHARE * row["n"]:
            return None
        row = defined
    if not row or row["n"] < (LEAST_EXTRA if level in EXTRA else LEAST) or row.get("sd") is None:
        return None
    return row["mean"], row["sd"], row["n"]


def panjabi_table():
    rows = csv.DictReader(line for line in open(FIG / "panjabi.csv", encoding="utf-8") if not line.startswith("#"))
    return {(r["measure"], r["level"]): (float(r["mean"]), float(r["sem"]) * int(r["n"]) ** 0.5) for r in rows}


def panjabi(ax, table, measure, place, style):
    """Panjabi's means, one SD either side, at every level he measured that the axis holds."""
    levels = sorted((lv for (m, lv) in table if m == measure and lv in place), key=place.get)
    xs = [place[lv] for lv in levels]
    means = [table[(measure, lv)][0] for lv in levels]
    sds = [table[(measure, lv)][1] for lv in levels]
    ax.plot(xs, means, style, color=PANJABI, linewidth=0.9, zorder=4)
    ax.errorbar(xs, means, yerr=sds, fmt="D", color=PANJABI, ms=2.6, elinewidth=0.7, capsize=1.5, zorder=4)


def ours(ax, profile, key, place, style, shift):
    """The gold tier line and its band at every usual level, T13 and L6 as points with their SD."""
    usual = sorted((lv for lv in place if lv not in EXTRA), key=place.get)
    xs, means, sds = [], [], []
    for level in usual:
        found = stats(profile, key, level)
        if found:
            xs.append(place[level]); means.append(found[0]); sds.append(found[1])
        elif xs:
            break
    ax.fill_between(xs, [m - s for m, s in zip(means, sds)], [m + s for m, s in zip(means, sds)],
                    color=OURS, alpha=0.16, linewidth=0, zorder=1)
    ax.plot(xs, means, style, color=OURS, linewidth=1.8, zorder=3)
    for level in EXTRA:
        found = stats(profile, key, level)
        if found:
            ax.errorbar([place[level] + shift], [found[0]], yerr=[found[1]], fmt="o", color=OURS, mfc="white", mew=1.4,
                        ms=4.5, capsize=3, elinewidth=1.3, zorder=4)


def panel(profile, spec):
    plt.rcParams.update({"font.family": "Arial", "font.weight": "bold", "axes.labelweight": "bold"})
    width_in, height_in = spec["emu"][0] / EMU, spec["emu"][1] / EMU
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=DPI)
    fig.subplots_adjust(left=0.135, right=0.975, top=0.975, bottom=0.215)
    ticks, place = spec["axis"]()
    width_key, depth_key = spec["keys"]
    ours(ax, profile, width_key, place, "-", -0.13)
    ours(ax, profile, depth_key, place, "--", 0.13)
    table = panjabi_table()
    panjabi(ax, table, spec["panjabi"][0], place, ":")
    panjabi(ax, table, spec["panjabi"][1], place, ":")
    bx = [ticks[lv] for lv in ticks]
    ax.plot(bx, spec["benzel_width"], "-", color="black", linewidth=1.5, zorder=5)
    ax.plot(bx, spec["benzel_depth"], "--", color="black", linewidth=1.5, zorder=5)
    for word, level, y in spec["labels"]:
        ax.text(place[level], y, word, fontsize=10, ha="center", zorder=6)
    ax.set_xlim(min(place.values()) - 0.1, max(place.values()) + 0.35)
    ax.set_ylim(*spec["ylim"])
    ax.set_yticks(list(spec["yticks"]))
    positions = [ticks[lv] for lv in ticks] + [place[lv] for lv in EXTRA]
    names = [lv[1:] for lv in ticks] + [lv[1:] for lv in EXTRA]
    ax.set_xticks(positions)
    ax.set_xticklabels(names, fontsize=8.5, fontweight="bold")
    for label, name in zip(ax.get_xticklabels(), list(ticks) + list(EXTRA)):
        if name in EXTRA:
            label.set_color(OURS)
    ax.tick_params(axis="both", direction="in", length=4, width=1.0, labelsize=8.5, pad=3)
    for label in ax.get_yticklabels():
        label.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_linewidth(1.1)
    ax.set_ylabel(spec["ylabel"], fontsize=9.5)
    for name, level in spec["regions"]:
        ax.text(place[level], -0.085, name, transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=9.5)
    ax.text(sum(ax.get_xlim()) / 2, -0.175, "Spinal Level", transform=ax.get_xaxis_transform(), ha="center",
            va="top", fontsize=9.5)
    drawing(fig, ax, spec)
    legend(ax, profile, spec)
    fig.savefig(FIG / spec["out"], dpi=DPI)
    plt.close(fig)


def drawing(fig, ax, spec):
    """Benzel's vertebra, cropped from his image and set where it sits in his frame."""
    top, bottom, left, right = spec["frame"]
    x0, y0, x1, y1 = spec["crop"]
    image = Image.open(OLD / spec["image"]).convert("L").crop(spec["crop"]).point(lambda v: 255 if v > 200 else v)
    box = ax.get_position()
    fx0 = box.x0 + (x0 - left) / (right - left) * box.width
    fx1 = box.x0 + (x1 - left) / (right - left) * box.width
    fy1 = box.y1 - (y0 - top) / (bottom - top) * box.height
    fy0 = box.y1 - (y1 - top) / (bottom - top) * box.height
    holder = fig.add_axes([fx0, fy0, fx1 - fx0, fy1 - fy0])
    holder.imshow(image, cmap="gray", vmin=0, vmax=255, aspect="auto")
    holder.axis("off")


def extra_n(profile, spec, level):
    """The number of spines a T13 or L6 point is drawn from, the most of the panel's two measures."""
    return max((s[2] for key in spec["keys"] if (s := stats(profile, key, level))), default=0)


def legend(ax, profile, spec):
    n = profile["spines"]["all"]
    handles = [Line2D([], [], color="black", lw=1.5, label="Benzel 2015 (digitised)"),
               Line2D([], [], color=PANJABI, lw=0.9, ls=":", marker="D", ms=2.6,
                      label="Panjabi 1991-92, 12 cadavers, ± 1 SD"),
               Line2D([], [], color=OURS, lw=1.8, label=f"Gold tier 3 & 4, mean ± 1 SD,\nN = {n:,} full spines"),
               Patch(facecolor=OURS, alpha=0.16, label="± 1 SD"),
               Line2D([], [], color=OURS, marker="o", mfc="white", mew=1.4, ms=4.5, ls="none",
                      label="T13, L6 (n = %d, %d)" % (extra_n(profile, spec, "T13"), extra_n(profile, spec, "L6")))]
    kind, x, y, where = spec["legend"]
    if kind == "short":
        handles = [handles[0], Line2D([], [], color=PANJABI, lw=0.9, ls=":", marker="D", ms=2.6, label="Panjabi, 12 cadavers"), Line2D([], [], color=OURS, lw=1.8, label=f"Gold tier 3 & 4 ± 1 SD,\nN = {n:,} full spines")]
    ax.legend(handles=handles, loc=where, bbox_to_anchor=(x, y), fontsize=7, frameon=True, framealpha=0.92,
              edgecolor="white", borderpad=0.3, handlelength=1.8, labelspacing=0.3)


def main():
    profile = json.load(open(FIG / "profile.json", encoding="utf-8"))
    for name, spec in PANELS.items():
        panel(profile, spec)
        ticks, place = spec["axis"]()
        for key in spec["keys"]:
            print(name, key, {lv: (round(s[0], 1), round(s[1], 1), s[2])
                              for lv in sorted(place, key=place.get) if (s := stats(profile, key, lv))})
    print("spines", profile["spines"], "extra", profile["extra_levels"])


if __name__ == "__main__":
    main()
