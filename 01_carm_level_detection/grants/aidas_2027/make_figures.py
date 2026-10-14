"""Draw the four figures of the AIDaS seed packet, at print width, from the files in figures/sources.

Figure 1  the idea: a trainee asks, the agent writes, runs and repairs grid jobs, on the CT-to-X-ray problem
Figure 2  Beethoven, the trainee's door to the grid, and what the 2026 cohort reported
Figure 3  panel b only (the projection from a labeled CT to the C-arm image); panel a is the archived
          network drawing, figures/sources/network_architecture.pdf, placed beside it by latex/main.tex
Figure 4  the held-out results: naming the level, and detection on a device never trained on

Every number drawn here is typed once, in NAMING, DETECTION and COHORT below, beside the file it comes
from; RECORD.md lists the same rows. figures/sources/SOURCES.md says where each image came from. Run it
on a laptop or as an sbatch job, never on a login node:

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

INK = "#1d1d1b"
MUTED = "#5f5f5a"
RULE = "#c9c5ba"
TEAL = "#0f5f55"  # Beethoven's own green
TEAL_PALE = "#e3efec"
BLUE_PALE = "#dbe8f5"  # the network drawing's block fill
ORANGE = "#eb6834"
ORANGE_PALE = "#fbe3d8"
DOT_BEFORE = "#9a978e"

# Held-out results, docs/handoff/RESULTS_CATALOG.md of 01_carm_level_detection (row id in each entry).
# value and Wilson interval in percent; an empty interval means the row records none.
NAMING = [
    ("Lateral,\nno C-arm frame\nin training", 96.4, (92.3, 98.4), "595 / 617", "A2.1"),
    ("AP,\nno C-arm frame\nin training", 43.7, (34.9, 51.9), "276 / 631", "A2.2"),
    ("AP, with the\ndevice's own\nframes", 96.4, (92.5, 98.3), "608 / 631", "A3.2"),
    ("Count and shape\ncoupled, frames\nwith the sacrum", 98.2, (96.5, 99.5), "991 / 1,009", "A5.1"),
]
DETECTION = [
    ("Physics\nrenders only", 0.3, None, "1 / 287", "A6.12"),
    ("Styled renders\nand two devices'\nreal frames", 63.1, None, "181 / 287", "A6.11"),
    ("Two devices'\nreal frames", 80.5, (74.1, 86.8), "231 / 287", "A6.1"),
]
SEPARABILITY = "styled renders stay\n99 to 100 % separable\nfrom real frames"  # row A13.3
TARGET = 97.0  # the pre-stated counting-grade detection target (RSNAI_PLAN.md C7), met by no held-out cell, row A6.13

# The 2026 cohort, Cureus 2026;18(7):e112661, Table 1 (n = 16; five-point scale, retrospective before and after).
COHORT = [
    ("CT spine reading", 1.81, 3.31),
    ("Landmarks, pathology", 2.00, 3.19),
    ("Python coding", 1.31, 2.56),
    ("Abstract writing", 2.94, 3.69),
    ("Conference submission", 2.56, 3.62),
    ("Literature reading", 3.25, 3.88),
]


def set_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Liberation Sans", "Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7.5,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "text.color": INK,
        "axes.linewidth": 0.6,
        "pdf.fonttype": 42,
        "savefig.dpi": 300,
    })


def new_canvas(height):
    """A figure whose data coordinates are inches from the lower left corner."""
    fig = plt.figure(figsize=(WIDTH, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax


def panel_title(ax, x, y, letter, text):
    ax.text(x, y, letter, fontsize=10, fontweight="bold", va="baseline", ha="left")
    ax.text(x + 0.17, y, text, fontsize=8, fontweight="bold", va="baseline", ha="left")


def place_image(ax, path, x, y, height, border=True):
    """Draws the image with its lower left corner at (x, y) inches and returns its width."""
    image = Image.open(path).convert("RGB")
    width = height * image.width / image.height
    ax.imshow(image, extent=(x, x + width, y, y + height), interpolation="lanczos", zorder=1)
    if border:
        ax.add_patch(Rectangle((x, y), width, height, fill=False, lw=0.5, ec=RULE, zorder=2))
    return width


def box(ax, x, y, w, h, text, face="white", edge=INK, weight="normal", size=7.5, color=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=face, ec=edge, lw=0.7, zorder=3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
            fontweight=weight, color=color, zorder=4, linespacing=1.15)


def arrow(ax, start, end, color=INK, style="-|>", lw=0.8, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=7, lw=lw, color=color,
                                 connectionstyle=f"arc3,rad={rad}", linestyle=ls, zorder=5,
                                 shrinkA=0, shrinkB=0))


def figure_overview():
    height = 2.2
    fig, ax = new_canvas(height)
    top = height - 0.14

    panel_title(ax, 0.0, top, "a", "Aim 2: a trainee asks")
    popup_w = place_image(ax, SOURCES / "beethoven_popup.png", 0.1, 0.5, 1.45)
    ax.text(0.1 + popup_w / 2, 0.3, "Beethoven starts the\ntrainee's agent on the\ngrid in one click",
            ha="center", va="center", fontsize=6.6, color=MUTED, linespacing=1.12)

    left, w, h = 1.8, 1.72, 0.3
    rows = [1.66, 1.18, 0.70, 0.18]
    arrow(ax, (1.39, rows[0] + h / 2), (left, rows[0] + h / 2))
    ax.text((1.39 + left) / 2, rows[0] + h / 2 - 0.06, "an issue\nand its\ngate", ha="center", va="top",
            fontsize=6.4, color=MUTED, linespacing=1.1)

    panel_title(ax, 1.72, top, "b", "Aim 1: the agent writes, runs and repairs")
    box(ax, left, rows[0], w, h, "Register the gate: rule, threshold,\ninputs and seed, hashed", size=6.9)
    box(ax, left, rows[1], w, h, "Write the Slurm job", size=7.3)
    box(ax, left, rows[2], w, h, "Submit; read the scheduler\nand the job's log", size=6.9)
    box(ax, left, rows[3], w, h, "Open the pull request\nfor the trainee", face=TEAL_PALE, edge=TEAL,
        size=6.9)
    for upper, lower in ((rows[0], rows[1]), (rows[1], rows[2])):
        arrow(ax, (left + w / 2, upper), (left + w / 2, lower + h))
    arrow(ax, (left + w / 2, rows[2]), (left + w / 2, rows[3] + h), color=TEAL)
    ax.text(left + w / 2 + 0.06, (rows[2] + rows[3] + h) / 2, "gate passes", fontsize=6.5, color=TEAL,
            va="center", ha="left")
    loop_x = left + w + 0.13
    ax.plot([left + w, loop_x, loop_x], [rows[2] + h / 2, rows[2] + h / 2, rows[1] + h / 2],
            color=ORANGE, lw=0.9, zorder=2)
    arrow(ax, (loop_x, rows[1] + h / 2), (left + w, rows[1] + h / 2), color=ORANGE, lw=0.9)
    ax.text(loop_x + 0.07, (rows[1] + rows[2] + h) / 2, "repair from\nthe message:\nwrong QoS,\n"
            "out of memory,\ntraceback,\ntime limit", fontsize=6.4, color=INK, va="center", ha="left",
            linespacing=1.12)

    arrow(ax, (4.43, 1.1), (4.66, 1.1))
    ax.text(4.545, 1.2, "jobs on\nH200s", ha="center", va="bottom", fontsize=6.4, color=MUTED,
            linespacing=1.1)

    panel_title(ax, 4.62, top, "c", "Aim 3: labeled 3-D to 2-D")
    tile_h, gap, x = 1.13, 0.035, 4.72
    labels = ("labeled CT", "physics render", "real film")
    for name, label in zip(("l6_labeled_ct.png", "l6_render.png", "l6_film.png"), labels):
        tile_w = place_image(ax, SOURCES / name, x, 0.62, tile_h)
        ax.text(x + tile_w / 2, 0.55, label, ha="center", va="top", fontsize=6.7)
        x += tile_w + gap
    ax.text(4.72, 0.2, "arrow: a sixth lumbar vertebra. The CT and its\nrender are one person; the film is another's",
            fontsize=6.3, color=MUTED, ha="left", va="bottom", linespacing=1.12)
    return fig


def figure_beethoven():
    height = 1.72
    fig, ax = new_canvas(height)
    top = height - 0.14

    panel_title(ax, 0.0, top, "a", "Ask in claude.ai; the grid does the work")
    place_image(ax, SOURCES / "beethoven_route.png", 0.06, 0.04, 1.42)

    panel_title(ax, 3.2, top, "b", "Your worker, your rules")
    place_image(ax, SOURCES / "beethoven_worker_settings.png", 3.28, 0.04, 1.4)

    panel_title(ax, 4.9, top, "c", "2026 cohort, n = 16")
    plot = fig.add_axes([5.98 / WIDTH, 0.3 / height, 1.04 / WIDTH, 1.06 / height])
    draw_cohort(plot)
    return fig


def draw_cohort(ax):
    rows = list(range(len(COHORT)))[::-1]
    for y, (name, before, after) in zip(rows, COHORT):
        ax.plot([before, after], [y, y], color=RULE, lw=1.4, zorder=1, solid_capstyle="round")
        ax.scatter([before], [y], s=13, color=DOT_BEFORE, zorder=2, linewidths=0)
        ax.scatter([after], [y], s=15, color=TEAL, zorder=3, linewidths=0)
    ax.set_yticks(rows)
    ax.set_yticklabels([name for name, _, _ in COHORT], fontsize=6.5, color=INK)
    ax.set_xlim(1, 5)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.tick_params(axis="both", length=2, width=0.5, labelsize=6.5, pad=2)
    ax.set_ylim(-0.6, len(COHORT) - 0.4)
    ax.grid(axis="x", color="#ebe8e0", lw=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.set_xlabel("comfort, 1 to 5", fontsize=6.4, labelpad=1.5, color=MUTED)
    ax.text(1.0, len(COHORT) - 0.25, "grey before, green after", fontsize=6.2, color=MUTED, ha="left",
            va="bottom")


def figure_projection():
    width, height = 2.35, 1.86
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.axis("off")
    panel_title(ax, 0.0, height - 0.14, "b", "From the labeled CT to the image")

    source = (0.12, 0.95)
    detector_x = 2.18
    object_x = source[0] + (detector_x - source[0]) * 745.0 / 1140.0
    magnification = 1140.0 / 745.0
    bodies = [(1.19, 1.27), (1.05, 1.13), (0.91, 0.99), (0.77, 0.85), (0.63, 0.71)]

    ax.add_patch(FancyBboxPatch((object_x - 0.2, 0.53), 0.4, 0.84, boxstyle="round,pad=0,rounding_size=0.05",
                                fc="#f2f1ec", ec=RULE, lw=0.6, zorder=1))
    ax.text(object_x, 1.41, "labeled CT", ha="center", va="bottom", fontsize=6.8)
    for i, (low, high) in enumerate(bodies):
        transitional = i == len(bodies) - 2
        face, edge = (ORANGE_PALE, ORANGE) if transitional else (BLUE_PALE, INK)
        ax.add_patch(Rectangle((object_x - 0.09, low), 0.18, high - low, fc=face, ec=edge, lw=0.6, zorder=3))
        projected_low = source[1] + (low - source[1]) * magnification
        projected_high = source[1] + (high - source[1]) * magnification
        ax.add_patch(Rectangle((detector_x - 0.07, projected_low), 0.07, projected_high - projected_low,
                               fc=face, ec=edge, lw=0.6, zorder=3))
    for y_object in (bodies[0][1], bodies[-1][0]):
        y_detector = source[1] + (y_object - source[1]) * magnification
        ax.plot([source[0], detector_x - 0.07], [source[1], y_detector], color=MUTED, lw=0.45, zorder=2)
    ax.plot(*source, marker="o", ms=4, color=INK, zorder=4)
    ax.text(0.04, source[1] + 0.09, "source", ha="left", va="bottom", fontsize=6.8)
    ax.plot([detector_x, detector_x], [0.22, 1.5], color=INK, lw=1.6, zorder=4)
    ax.text(detector_x + 0.06, 1.53, "detector", ha="right", va="bottom", fontsize=6.8)

    measure(ax, source[0], object_x, 0.33, "745 mm")
    measure(ax, source[0], detector_x, 0.12, "1,140 mm: each body lands 1.53 times larger")
    return fig


def measure(ax, x0, x1, y, label):
    arrow(ax, (x0, y), (x1, y), color=MUTED, style="<|-|>", lw=0.5)
    ax.text((x0 + x1) / 2, y + 0.025, label, ha="center", va="bottom", fontsize=6.3, color=MUTED)


def figure_results():
    height = 1.68
    fig = plt.figure(figsize=(WIDTH, height))
    naming = fig.add_axes([0.42 / WIDTH, 0.5 / height, 3.1 / WIDTH, 0.95 / height])
    detection = fig.add_axes([4.27 / WIDTH, 0.5 / height, 2.75 / WIDTH, 0.95 / height])
    title_y = (height - 0.14) / height
    fig.text(0.0, title_y, "a", fontsize=10, fontweight="bold")
    fig.text(0.17 / WIDTH, title_y, "Naming the level on C-ArmLSpine, held out", fontsize=8,
             fontweight="bold")
    fig.text(3.8 / WIDTH, title_y, "b", fontsize=10, fontweight="bold")
    fig.text(3.97 / WIDTH, title_y, "Finding vertebrae on a device never trained on", fontsize=8,
             fontweight="bold")
    draw_points(naming, NAMING, TEAL, "exact level, %", target=False)
    draw_points(detection, DETECTION, ORANGE, "vertebrae found, %", target=True)
    detection.text(-0.38, 50, SEPARABILITY, fontsize=6.3, color=MUTED, va="center", ha="left",
                   linespacing=1.15)
    return fig


def label_place(value):
    """Where a point's two-line label sits, as (y, vertical alignment): above the point, beside it, or
    below it, whichever keeps the label off the top of the axes and the target line."""
    if value + 18 < TARGET - 2:
        return value + 4, "bottom"
    if value + 7 < TARGET - 2:
        return value, "center"
    return value - 15, "center"


def draw_points(ax, rows, color, ylabel, target):
    xs = range(len(rows))
    for x, (_, value, interval, count, _) in zip(xs, rows):
        if interval:
            ax.plot([x, x], interval, color=color, lw=1.3, solid_capstyle="butt", zorder=2)
        ax.scatter([x], [value], s=13, color=color, zorder=3, linewidths=0)
        y, alignment = label_place(value)
        ax.text(x + 0.09, y, f"{value:.1f} %\n{count}", fontsize=6.4, va=alignment, ha="left",
                linespacing=1.1)
    if target:
        ax.axhline(TARGET, color=INK, lw=0.6, ls=(0, (3, 2)), zorder=1)
        ax.text(len(rows) - 0.3, TARGET + 2.5, "pre-stated 97 %", fontsize=6.4, ha="right", va="bottom")
    ax.set_xlim(-0.45, len(rows) - 0.25)
    ax.set_ylim(0, 108)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_xticks(list(xs))
    ax.set_xticklabels([label for label, *_ in rows], fontsize=6.5, linespacing=1.1)
    ax.tick_params(axis="both", length=2, width=0.5, labelsize=6.6, pad=2)
    ax.tick_params(axis="x", length=0, pad=3)
    ax.set_ylabel(ylabel, fontsize=6.6, labelpad=2)
    ax.grid(axis="y", color="#ebe8e0", lw=0.5)
    ax.set_axisbelow(True)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)


def save(fig, name, check):
    # No creation date in the PDF, so a figure redrawn from unchanged sources is byte for byte the same file.
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
