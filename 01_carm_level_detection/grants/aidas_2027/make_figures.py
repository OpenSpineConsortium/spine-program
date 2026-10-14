"""Draw the figures of the AIDaS seed packet, at print width, from the files in figures/sources.

Figure 1  one loop in three aims: the trainee, the gate-conditioned repair loop, the CT-to-X-ray problem
Figure 2  Beethoven, the trainee's door to the grid, and what the 2026 cohort reported
Figure 3  panel b only (the projection from a labeled CT to the C-arm image); panel a is the archived
          network drawing, figures/sources/network_architecture.pdf, placed beside it by latex/main.tex
Figure 4  the held-out results: naming the level, and detection on a device never trained on

Every number drawn here is typed once, in NAMING, DETECTION, TARGET, COHORT and GEOMETRY
below, beside the file it comes from; RECORD.md lists the same rows. figures/sources/SOURCES.md says where
each image came from. Every label is set at 6.8 pt or more at print size. Run it on a laptop or as an
sbatch job, never on a login node:

    python3 make_figures.py            # writes latex/figures/*.pdf for the packet and a 300 dpi preview
                                       # of each in figures/*.png
    python3 make_figures.py --check    # also prints each figure's size, to compare with the page

Needs matplotlib and Pillow.
"""

import argparse
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "figures" / "sources"
PREVIEWS = HERE / "figures"
PACKET_FIGURES = HERE / "latex" / "figures"

WIDTH = 7.1  # inches: letter paper less two 0.7 inch margins
LABEL = 7.0  # points: the smallest label size at print
SMALL = 6.8

INK = "#1d1d1b"
MUTED = "#5f5f5a"
RULE = "#c9c5ba"
TEAL = "#0f5f55"  # Beethoven's own green: what works or passes
TEAL_PALE = "#e3efec"
ORANGE = "#eb6834"  # what fails today and must be repaired
ORANGE_PALE = "#fbe3d8"
GREY_PALE = "#f2f1ec"
DOT_BEFORE = "#9a978e"

# Held-out results, docs/handoff/RESULTS_CATALOG.md of 01_carm_level_detection (row id in each entry): the label with
# the count where the row gives one, the value in percent, the 95 % case-clustered interval as the row gives it
# (None where it gives none), and the row. Each point is the stronger of the record's results for its question, as
# the owner asked on 2026-10-14: the tuned points are the fine-tunes of the v9 encoder (A9), the coupled point the
# fold models' (A5), whose training banks hold VinDr and FluoroCap crops (RECORD.md section 4).
NAMING = [
    ("Lateral,\nzero-shot\n595 / 617", 96.4, (92.3, 98.4), "A2.1"),
    ("AP,\nzero-shot\n276 / 631", 43.7, (34.9, 51.9), "A2.2"),
    ("AP, tuned\non 5 of its\ncases", 90.8, None, "A9.2"),
    ("AP, tuned\non all of\nits cases", 98.1, None, "A9.2"),
    ("Count and\nshape coupled\n991 / 1,009", 98.2, (96.5, 99.5), "A5.1"),
]
# Detection on C-ArmLSpine, held out of detector training: each arm at the 0.74 cross-device threshold (with its
# interval and count) and at 0.25 (with its interval where the row gives one).
DETECTION = [
    ("Two devices'\nreal frames", 80.5, (74.1, 86.8), "231 / 287", "A6.1", 90.6, (84.3, 94.5), "A6.2"),
    ("The same and\nstyled renders", 63.1, (54.8, 71.0), "181 / 287", "A6.11, A7.8", 87.8, None, "A6.11"),
    ("Renders\nonly", 0.3, None, "1 / 287", "A6.12", 31.7, None, "A6.12"),
]  # of 287 vertebrae on 56 frames of 28 cases
TARGET = 97.0  # the counting-grade detection target set in advance (RSNAI_PLAN.md C7), met by no held-out cell, A6.13

# The 2026 cohort, Cureus 2026;18(7):e112661, Table 1 (n = 16; five-point scale, retrospective before and after;
# the means).
COHORT = [
    ("CT spine reading", 1.81, 3.31),
    ("Landmarks, pathology", 2.00, 3.19),
    ("Python coding", 1.31, 2.56),
    ("Abstract writing", 2.94, 3.69),
    ("Conference submission", 2.56, 3.62),
    ("Literature reading", 3.25, 3.88),
]

# C-ArmLSpine's geometry, docs/MODEL_CARD.md section 6.1 of 01_carm_level_detection: source to detector 1,140 mm,
# source to object 745 mm, so each body lands 1,140 / 745 = 1.53 times larger on the detector.
GEOMETRY = {"sid_mm": 1140.0, "sod_mm": 745.0}


def set_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"],
        "font.size": LABEL,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "axes.linewidth": 0.6,
        "pdf.fonttype": 42,
        "savefig.dpi": 300,
    })


def new_canvas(width, height):
    """A figure whose data coordinates are inches from the lower left corner."""
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax


def panel_title(ax, x, y, letter, text):
    ax.text(x, y, letter, fontsize=10, fontweight="bold", va="baseline", ha="left")
    ax.text(x + 0.17, y, text, fontsize=8, fontweight="bold", va="baseline", ha="left")


def place_image(ax, image, x, y, height, border=True):
    """Draws the image with its lower left corner at (x, y) inches and returns its width."""
    width = height * image.width / image.height
    ax.imshow(image, extent=(x, x + width, y, y + height), interpolation="lanczos", zorder=1)
    if border:
        ax.add_patch(Rectangle((x, y), width, height, fill=False, lw=0.5, ec=RULE, zorder=2))
    return width


def open_image(name):
    return Image.open(SOURCES / name).convert("RGB")


def box(ax, x, y, w, h, text, face="white", edge=INK, weight="normal", size=LABEL, color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05",
                                fc=face, ec=edge, lw=0.7, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            fontweight=weight, color=color, zorder=4, linespacing=1.15)


def arrow(ax, start, end, color=INK, style="-|>", lw=0.8, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=7, lw=lw, color=color,
                                 connectionstyle=f"arc3,rad={rad}", linestyle=ls, zorder=5,
                                 shrinkA=0, shrinkB=0))


def note(ax, x, y, text, color=INK, ha="left", va="center", size=SMALL):
    ax.text(x, y, text, fontsize=size, color=color, ha=ha, va=va, linespacing=1.15, zorder=6)


def figure_overview():
    height = 1.97
    fig, ax = new_canvas(WIDTH, height)
    top = height - 0.14
    draw_trainee(ax, top)
    draw_gated_loop(ax, top)
    draw_three_images(ax, top)
    return fig


def draw_trainee(ax, top):
    """Panel a: the trainee's question reaches the grid through Beethoven."""
    panel_title(ax, 0.0, top, "a", "Aim 2: the trainee")
    left, w, h = 0.04, 1.12, 0.42
    rows = [(1.27, "A trainee asks\nin claude.ai", "white", INK),
            (0.71, "Beethoven: one click\nstarts the trainee's\nworker", TEAL_PALE, TEAL),
            (0.15, "Claude Code worker,\na Slurm job on\nthe WSU grid", "white", INK)]
    for y, text, face, edge in rows:
        box(ax, left, y, w, h, text, face=face, edge=edge)
    for (upper, *_), (lower, *_) in zip(rows, rows[1:]):
        arrow(ax, (left + w / 2, upper), (left + w / 2, lower + h))


def draw_gated_loop(ax, top):
    """Panel b: the gate-conditioned repair loop, with its budget and the two arms it is compared with."""
    panel_title(ax, 1.36, top, "b", "Aim 1: the gate-conditioned repair loop")
    left, w, h = 1.5, 1.5, 0.27
    task, write, submit, gate, done = 1.46, 1.1, 0.74, 0.38, 0.02
    box(ax, left, task, w, h, "Task and its gate, written\nby people, hashed", face=GREY_PALE)
    box(ax, left, write, w, h, "Write the Slurm job")
    box(ax, left, submit, w, h, "Submit; read the scheduler\nand the job's log")
    box(ax, left, gate, w, h, "Does the gate pass?", weight="bold")
    box(ax, left, done, w, h, "Pull request\nfor the trainee", face=TEAL_PALE, edge=TEAL)
    centre = left + w / 2
    for upper, lower in ((task, write), (write, submit), (submit, gate)):
        arrow(ax, (centre, upper), (centre, lower + h))
    arrow(ax, (centre, gate), (centre, done + h), color=TEAL)
    note(ax, centre + 0.06, (gate + done + h) / 2, "passes", color=TEAL)

    arrow(ax, (1.16, task + h / 2), (left, task + h / 2))
    note(ax, 1.19, task + h / 2 - 0.05, "a task\nand its\ngate", color=MUTED, va="top")

    loop_x = left + w + 0.14
    for y in (submit + h / 2, gate + h / 2):
        ax.plot([left + w, loop_x], [y, y], color=ORANGE, lw=1.0, zorder=2)
    ax.plot([loop_x, loop_x], [gate + h / 2, write + h / 2], color=ORANGE, lw=1.0, zorder=2)
    arrow(ax, (loop_x, write + h / 2), (left + w, write + h / 2), color=ORANGE, lw=1.0)
    note(ax, loop_x + 0.08, 1.25, "Repair from the message:\nrefused, out of memory,\na traceback, or the\ngate fails", va="top")
    note(ax, loop_x + 0.08, 0.76, "At most 6 repairs and\n2 GPU-hours, then the\ntask counts as failed", va="top")
    note(ax, loop_x + 0.08, 0.33, "Compared with one shot\nand with a loop that stops\nat a clean exit", va="top",
         color=MUTED)


def draw_three_images(ax, top):
    """Panel c: a sixth lumbar vertebra in a labeled CT, its physics render and another person's radiograph."""
    panel_title(ax, 4.63, top, "c", "Aim 3: labeled 3-D into 2-D")
    note(ax, 7.08, top - 0.2, "white bars, 20 mm", color=MUTED, ha="right")
    tile_h, gap, x = 1.18, 0.03, 4.68
    labels = ("labeled CT", "physics render", "real radiograph")
    for name, label in zip(("l6_labeled_ct.png", "l6_render.png", "l6_film.png"), labels):
        tile_w = place_image(ax, open_image(name), x, 0.36, tile_h)
        note(ax, x + tile_w / 2, 0.29, label, ha="center", va="top", size=LABEL)
        x += tile_w + gap


def figure_beethoven():
    height = 1.7
    fig, ax = new_canvas(WIDTH, height)
    top = height - 0.14
    draw_route(ax, top)
    panel_title(ax, 2.58, top, "b", "One click starts the worker")
    place_image(ax, open_image("beethoven_popup_top.png"), 2.62, 0.02, 1.44)
    panel_title(ax, 5.02, top, "c", "2026 cohort, n = 16")
    note(ax, 5.19, top - 0.2, "grey dots before, green after", size=SMALL)
    plot = fig.add_axes([6.13 / WIDTH, 0.33 / height, 0.9 / WIDTH, 1.0 / height])
    draw_cohort(plot)
    return fig


def draw_route(ax, top):
    """Panel a, after the extension's own diagram: where a trainee's question goes."""
    panel_title(ax, 0.0, top, "a", "Ask in claude.ai; the grid does the work")
    box(ax, 0.02, 0.45, 0.86, 0.6, "claude.ai in the\ntrainee's browser,\nwith Beethoven")
    box(ax, 1.4, 1.06, 1.0, 0.36, "Claude servers:\nthe model")
    box(ax, 1.4, 0.5, 1.0, 0.44, "WSU grid: the\ntrainee's Claude\nCode worker", face=TEAL_PALE, edge=TEAL)
    box(ax, 1.4, 0.02, 1.0, 0.34, "H200 GPUs, 4 nodes\nof 4 (partition gmsap)")
    arrow(ax, (0.88, 0.95), (1.4, 1.24), rad=-0.2)
    note(ax, 1.0, 1.2, "a chat", color=MUTED, ha="center", va="bottom")
    arrow(ax, (0.88, 0.72), (1.4, 0.72))
    note(ax, 1.14, 0.75, "a Code\nsession", color=MUTED, ha="center", va="bottom")
    arrow(ax, (1.9, 0.94), (1.9, 1.06))
    note(ax, 1.95, 1.0, "the model", color=MUTED)
    arrow(ax, (1.9, 0.5), (1.9, 0.36), color=ORANGE)
    note(ax, 1.85, 0.43, "the heavy lifting", color=ORANGE, ha="right")


def draw_cohort(ax):
    rows = list(range(len(COHORT)))[::-1]
    for y, (name, before, after) in zip(rows, COHORT):
        ax.plot([before, after], [y, y], color=RULE, lw=1.4, zorder=1, solid_capstyle="round")
        ax.scatter([before], [y], s=13, color=DOT_BEFORE, zorder=2, linewidths=0)
        ax.scatter([after], [y], s=15, color=TEAL, zorder=3, linewidths=0)
    ax.set_yticks(rows)
    ax.set_yticklabels([name for name, _, _ in COHORT], fontsize=LABEL, color=INK)
    ax.set_xlim(1, 5)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.tick_params(axis="both", length=2, width=0.5, labelsize=LABEL, pad=2)
    ax.set_ylim(-0.6, len(COHORT) - 0.4)
    ax.grid(axis="x", color="#ebe8e0", lw=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.set_xlabel("mean comfort, 1 to 5", fontsize=LABEL, labelpad=1.5, color=INK)


def figure_projection():
    """Panel 3b: the CT's labeled bodies projected at the device's geometry, edge-on on the detector and face-on in
    the image, where the transitional body's four corners become its keypoint labels."""
    width, height = 2.62, 1.62
    fig, ax = new_canvas(width, height)
    source = (0.08, 0.8)
    detector_x = 1.72
    magnification = GEOMETRY["sid_mm"] / GEOMETRY["sod_mm"]
    object_x = source[0] + (detector_x - source[0]) / magnification
    bodies = [(1.06, 1.14), (0.92, 1.0), (0.78, 0.86), (0.64, 0.72), (0.5, 0.58)]
    transitional = len(bodies) - 2

    ax.add_patch(FancyBboxPatch((object_x - 0.19, 0.4), 0.38, 0.83, boxstyle="round,pad=0,rounding_size=0.05",
                                fc=GREY_PALE, ec=RULE, lw=0.6, zorder=1))
    note(ax, object_x, 1.27, "labeled CT", ha="center", va="bottom", size=LABEL)
    image_left, image_w = 1.98, 0.6
    ax.add_patch(Rectangle((image_left, 0.22), image_w, 1.22, fc=GREY_PALE, ec=RULE, lw=0.6, zorder=1))
    note(ax, image_left + image_w / 2, 1.48, "the image", ha="center", va="bottom", size=LABEL)
    for i, (low, high) in enumerate(bodies):
        face, edge = (ORANGE_PALE, ORANGE) if i == transitional else (TEAL_PALE, TEAL)
        ax.add_patch(Rectangle((object_x - 0.08, low), 0.16, high - low, fc=face, ec=edge, lw=0.6, zorder=3))
        projected = [project(source, detector_x, x, y)
                     for x in (object_x - 0.08, object_x + 0.08) for y in (low, high)]
        bottom, top = min(projected), max(projected)
        ax.add_patch(Rectangle((detector_x - 0.06, bottom), 0.06, top - bottom, fc=face, ec=edge, lw=0.6,
                               zorder=3))
        corners = draw_face_on(ax, image_left + image_w / 2, bottom, top, face, edge)
        if i == transitional:
            for x, y in corners:
                ax.plot([x], [y], marker="o", ms=2.6, color=ORANGE, zorder=6)
            ax.plot([detector_x, image_left + 0.1], [top, top], color=ORANGE, lw=0.4, ls=(0, (2, 2)), zorder=2)
            ax.plot([detector_x, image_left + 0.1], [bottom, bottom], color=ORANGE, lw=0.4, ls=(0, (2, 2)),
                    zorder=2)
    for x, y in ((object_x - 0.08, bodies[0][1]), (object_x - 0.08, bodies[-1][0])):
        ax.plot([source[0], detector_x - 0.06], [source[1], project(source, detector_x, x, y)],
                color=MUTED, lw=0.45, zorder=2)
    ax.plot(*source, marker="o", ms=4, color=INK, zorder=4)
    note(ax, 0.0, source[1] + 0.09, "source", va="bottom", size=LABEL)
    ax.plot([detector_x, detector_x], [0.2, 1.44], color=INK, lw=1.6, zorder=4)
    note(ax, detector_x, 1.48, "detector", ha="center", va="bottom", size=LABEL)

    measure(ax, source[0], object_x, 0.26, f"{GEOMETRY['sod_mm']:,.0f} mm")
    measure(ax, source[0], detector_x, 0.06, f"{GEOMETRY['sid_mm']:,.0f} mm: {magnification:.2f} times larger")
    return fig


def project(source, detector_x, x, y):
    """Where the ray from the source through (x, y) meets the detector, for a point at depth x."""
    return source[1] + (y - source[1]) * (detector_x - source[0]) / (x - source[0])


def draw_face_on(ax, centre, bottom, top, face, edge):
    """A body as the image shows it, face on: a slightly tapered quadrilateral between its projected bottom and
    top; returns its four corners."""
    half_low, half_high = 0.17, 0.15
    corners = [(centre - half_low, bottom), (centre + half_low, bottom), (centre + half_high, top),
               (centre - half_high, top)]
    ax.add_patch(plt.Polygon(corners, closed=True, fc=face, ec=edge, lw=0.6, zorder=3))
    return corners


def measure(ax, x0, x1, y, label):
    arrow(ax, (x0, y), (x1, y), color=MUTED, style="<|-|>", lw=0.5)
    note(ax, (x0 + x1) / 2, y + 0.025, label, ha="center", va="bottom", size=SMALL)


def figure_results():
    height = 1.48
    fig = plt.figure(figsize=(WIDTH, height))
    naming = fig.add_axes([0.42 / WIDTH, 0.46 / height, 2.95 / WIDTH, 0.78 / height])
    detection = fig.add_axes([4.08 / WIDTH, 0.46 / height, 2.95 / WIDTH, 0.78 / height])
    title_y = (height - 0.14) / height
    fig.text(0.0, title_y, "a", fontsize=10, fontweight="bold")
    fig.text(0.17 / WIDTH, title_y, "Naming the level on C-ArmLSpine", fontsize=8, fontweight="bold")
    fig.text(3.62 / WIDTH, title_y, "b", fontsize=10, fontweight="bold")
    fig.text(3.79 / WIDTH, title_y, "Finding vertebrae on a device never trained on", fontsize=8,
             fontweight="bold")
    draw_naming(naming)
    draw_detection(detection)
    return fig


def draw_naming(ax):
    for x, (_, value, interval, _) in enumerate(NAMING):
        if interval:
            ax.plot([x, x], interval, color=TEAL, lw=1.3, solid_capstyle="butt", zorder=2)
        ax.scatter([x], [value], s=14, color=TEAL, zorder=3, linewidths=0)
        ax.text(x + 0.12, value, f"{value:.1f} %", fontsize=SMALL, va="center", ha="left")
    style_axes(ax, [label for label, *_ in NAMING], "exact level, %")


def draw_detection(ax):
    """Each arm at 0.74 (filled, with its interval) and at 0.25 (open), side by side, each value beside its point."""
    for x, (_, value, interval, _, _, value_low, interval_low, _) in enumerate(DETECTION):
        for centre, bar in ((x - 0.13, interval), (x + 0.13, interval_low)):
            if bar:
                ax.plot([centre, centre], bar, color=ORANGE, lw=1.3, solid_capstyle="butt", zorder=2)
        ax.scatter([x - 0.13], [value], s=14, color=ORANGE, zorder=3, linewidths=0)
        ax.scatter([x + 0.13], [value_low], s=16, facecolors="white", edgecolors=ORANGE, linewidths=0.9, zorder=3)
        ax.text(x - 0.21, value, f"{value:.1f} %", fontsize=SMALL, va="center", ha="right")
        # A label is kept clear of the target's dashed line above it.
        ax.text(x + 0.21, min(value_low, TARGET - 9), f"{value_low:.1f} %", fontsize=SMALL, va="center", ha="left")
    ax.scatter([1.72], [76], s=14, color=ORANGE, linewidths=0)
    ax.text(1.8, 76, "threshold 0.74", fontsize=SMALL, va="center", ha="left")
    ax.scatter([1.72], [62], s=16, facecolors="white", edgecolors=ORANGE, linewidths=0.9)
    ax.text(1.8, 62, "threshold 0.25", fontsize=SMALL, va="center", ha="left")
    ax.axhline(TARGET, color=INK, lw=0.6, ls=(0, (3, 2)), zorder=1)
    ax.text(len(DETECTION) - 0.45, TARGET + 2.5, "97 % set in advance", fontsize=SMALL, ha="right",
            va="bottom")
    style_axes(ax, [label for label, *_ in DETECTION], "vertebrae found, %", left=-0.75)


def style_axes(ax, labels, ylabel, left=-0.35):
    ax.set_xlim(left, len(labels) - 0.05)
    ax.set_ylim(0, 108)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xticks(list(range(len(labels))))
    ax.set_xticklabels(labels, fontsize=SMALL, linespacing=1.1)
    ax.tick_params(axis="both", length=2, width=0.5, labelsize=SMALL, pad=2)
    ax.tick_params(axis="x", length=0, pad=3)
    ax.set_ylabel(ylabel, fontsize=SMALL, labelpad=2)
    ax.grid(axis="y", color="#ebe8e0", lw=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)


def save(fig, name, check):
    # No creation date in the PDF, so a figure redrawn from unchanged sources, with the same matplotlib and the same
    # fonts, is byte for byte the same file.
    fig.savefig(PACKET_FIGURES / f"{name}.pdf", facecolor="white", metadata={"CreationDate": None})
    fig.savefig(PREVIEWS / f"{name}.png", facecolor="white")
    if check:
        width, height = fig.get_size_inches()
        print(f"{name}: {width:.2f} x {height:.2f} in")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="print each figure's size")
    args = parser.parse_args()
    set_style()
    PACKET_FIGURES.mkdir(parents=True, exist_ok=True)
    # Figure 3a is the archived drawing itself, copied so that latex/ holds everything the packet needs.
    shutil.copyfile(SOURCES / "network_architecture.pdf", PACKET_FIGURES / "network_architecture.pdf")
    save(figure_overview(), "fig1_overview", args.check)
    save(figure_beethoven(), "fig2_beethoven", args.check)
    save(figure_projection(), "fig3b_projection", args.check)
    save(figure_results(), "fig4_results", args.check)


if __name__ == "__main__":
    main()
