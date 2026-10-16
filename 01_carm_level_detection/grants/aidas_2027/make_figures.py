"""Draw the figure of the AIDaS seed packet: one panel of six at the text's full width, from figures/sources.

Figure 1, in two rows of three:
  a  Aim 1: one research iteration held to the frameworks, and how it is scored
  b  Aim 2: Beethoven, the trainee's door to the grid
  c  Aim 2: what the 2026 cohort reported
  d  Aim 3: a sixth lumbar vertebra in a labeled CT, its physics render and another person's radiograph
  e  Aim 3: the spine RAG-LLM that the case example builds, on the grid
  f  the held-out results: naming the level, and finding vertebrae on a C-arm never trained on

The panel is drawn 7.2 in wide, the text width of letter paper less two 0.65 inch margins, and latex/main.tex
places it at its own size, so every label prints at the size it is drawn here, 7 pt or more; a text block narrower
than the panel makes LaTeX report an overfull line rather than shrink the labels. Every number drawn is typed once,
in NAMING, DETECTION, TARGET and COHORT below, beside the file it comes from; RECORD.md lists the same rows.
figures/sources/SOURCES.md says where each image came from. Run it on a laptop or as an sbatch job, never on a
login node:

    python3 make_figures.py            # checks the panel and, once it passes, writes latex/figures/fig1_panel.pdf
                                       # for the packet and a 300 dpi preview of it, figures/fig1_panel.png
    python3 make_figures.py --check    # checks it and writes nothing

The check fails on a label under 7 pt, one outside the panel, one closer than PAD to the edge of its own box, and
one over another label, another box, an image or a data point.

Needs matplotlib and Pillow.
"""

import argparse
import itertools
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import PathCollection  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.transforms import Bbox  # noqa: E402
from matplotlib.text import Text  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
SOURCES = HERE / "figures" / "sources"
PREVIEWS = HERE / "figures"
PACKET_FIGURES = HERE / "latex" / "figures"
NAME = "fig1_panel"

WIDTH = 7.2  # inches: letter paper less two 0.65 inch margins, main.tex's text width
HEIGHT = 3.5
ROW = 1.75  # inches: the height of each of the two rows, its titles included
LABEL = 7.0  # points: every label at print, the smallest size the check allows
TITLE = 8.0
LETTER = 10.0
PAD = 0.03  # inches: the least room the check allows between a box's label and its edge

INK = "#1d1d1b"
MUTED = "#5f5f5a"
RULE = "#c9c5ba"
TEAL = "#0f5f55"  # Beethoven's own green: Beethoven, what passes, the cohort's after and the naming results
TEAL_PALE = "#e3efec"
ORANGE = "#eb6834"  # the loop that repeats, what is built and not yet run, and detection, short of its goal
GREY_PALE = "#f2f1ec"
DOT_BEFORE = "#9a978e"
GRID = "#ebe8e0"

# Held-out results, docs/handoff/RESULTS_CATALOG.md of 01_carm_level_detection (row id in each entry): the label, the
# value in percent, the 95 % case-clustered interval as the row gives it, or, for A9.2, as the file the catalog's A9
# header names gives it (results/schwingnet/indomain/name_fill.json at 5597197, figure5b, AP to AP, N = 5 and
# N = all), and the row, with its count where it gives one. Each point is the stronger of the record's results for
# its question, as the owner asked on 2026-10-14: the tuned points are the fine-tunes of the v9 encoder (A9), the
# coupled point the fold models' (A5), whose training banks hold VinDr and FluoroCap crops (RECORD.md section 4).
NAMING = [
    ("Lateral, zero-shot", 96.4, (92.3, 98.4), "A2.1, 595 / 617"),
    ("AP, zero-shot", 43.7, (34.9, 51.9), "A2.2, 276 / 631"),
    ("AP, tuned on 5 cases", 90.8, (86.7, 94.3), "A9.2"),
    ("AP, tuned on all others", 98.1, (95.7, 99.8), "A9.2"),
    ("Checked by the count", 98.2, (96.5, 99.5), "A5.1, 991 / 1,009"),
]
# Detection on C-ArmLSpine, held out of detector training, of 287 vertebrae on 56 frames of 28 cases: each arm at
# the 0.74 cross-device threshold, with its interval, and at 0.25, with its interval where the row gives one; the
# middle arm trains on the first arm's real frames and the styled renders.
DETECTION = [
    ("Two devices' real frames", 80.5, (74.1, 86.8), 90.6, (84.3, 94.5), "A6.1, 231 / 287; A6.2"),
    ("+ styled renders", 63.1, (54.8, 71.0), 87.8, None, "A6.11 and A7.8, 181 / 287; A6.11"),
    ("Renders only", 0.3, None, 31.7, None, "A6.12, 1 / 287; A6.12"),
]
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

BOXED = []  # each box with its label, so that the check can hold the label inside the box
MASK = {"boxstyle": "square,pad=0.1", "fc": "white", "ec": "none"}  # behind a label set over grid lines


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


def new_canvas():
    """The panel, whose data coordinates are inches from its lower left corner."""
    fig = plt.figure(figsize=(WIDTH, HEIGHT))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.axis("off")
    return fig, ax


def inset(fig, x, y, w, h):
    """Axes whose frame is the rectangle w by h inches with its lower left corner at (x, y)."""
    return fig.add_axes([x / WIDTH, y / HEIGHT, w / WIDTH, h / HEIGHT])


def panel_title(ax, x, y, letter, text):
    ax.text(x, y, letter, fontsize=LETTER, fontweight="bold", va="baseline", ha="left")
    ax.text(x + 0.16, y, text, fontsize=TITLE, fontweight="bold", va="baseline", ha="left")


def place_image(ax, image, x, y, height):
    """Draws the image with its lower left corner at (x, y) inches and returns its width."""
    width = height * image.width / image.height
    ax.imshow(image, extent=(x, x + width, y, y + height), interpolation="lanczos", zorder=1)
    ax.add_patch(Rectangle((x, y), width, height, fill=False, lw=0.5, ec=RULE, zorder=2))
    return width


def open_image(name):
    return Image.open(SOURCES / name).convert("RGB")


def box(ax, x, y, w, h, text, face="white", edge=INK, weight="normal"):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05", fc=face, ec=edge, lw=0.7,
                           zorder=3)
    ax.add_patch(patch)
    label = ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=LABEL, fontweight=weight,
                    zorder=4, linespacing=1.15)
    BOXED.append((patch, label))


def arrow(ax, start, end, color=INK, style="-|>", lw=0.8):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=7, lw=lw, color=color, zorder=5,
                                 shrinkA=0, shrinkB=0))


def note(ax, x, y, text, color=INK, ha="left", va="center", weight="normal"):
    ax.text(x, y, text, fontsize=LABEL, color=color, ha=ha, va=va, fontweight=weight, linespacing=1.15, zorder=6)


def figure_panel():
    BOXED.clear()
    fig, ax = new_canvas()
    top, bottom = HEIGHT - 0.24, ROW + 0.05
    draw_research_loop(ax, 0.0, top, bottom)
    draw_route(ax, 2.86, top, bottom)
    draw_cohort(fig, ax, 5.0, top, bottom)
    top, bottom = ROW - 0.24, 0.0
    draw_three_images(ax, 0.0, top, bottom)
    draw_rag_llm(ax, 2.36, top, bottom)
    draw_results(fig, ax, 4.56, top, bottom)
    return fig


def draw_research_loop(ax, x, top, bottom):
    """Panel a: one research iteration held to the frameworks, the loop that repeats it and how the arms are scored."""
    panel_title(ax, x, top + 0.11, "a", "Aim 1: research held to the frameworks")
    left, w = x + 0.02, 1.42
    steps = [("Question and its gate set\nby a person, sealed", GREY_PALE, INK, "normal", 0.27),
             ("Hypothesis sealed; jobs run\nthrough Beethoven; code\nchecked by beethoven-qa", "white", INK, "normal",
              0.38),
             ("REFORMS record kept;\ndoes the gate pass?", "white", INK, "bold", 0.27),
             ("It passes: a pull request\nthat a person merges", TEAL_PALE, TEAL, "normal", 0.27)]
    gap = (top - bottom - sum(step[-1] for step in steps)) / (len(steps) - 1)
    placed = []
    y = top
    for text, face, edge, weight, h in steps:
        y -= h
        box(ax, left, y, w, h, text, face=face, edge=edge, weight=weight)
        placed.append((y, h))
        y -= gap
    centre = left + w / 2
    for (upper, _), (lower, lower_h) in zip(placed, placed[1:]):
        arrow(ax, (centre, upper), (centre, lower + lower_h), color=TEAL if lower == placed[-1][0] else INK)

    (hypothesis, hypothesis_h), (gate, gate_h) = placed[1], placed[2]
    loop_x = left + w + 0.12
    ax.plot([left + w, loop_x], [gate + gate_h / 2] * 2, color=ORANGE, lw=1.0, zorder=2)
    ax.plot([loop_x, loop_x], [gate + gate_h / 2, hypothesis + hypothesis_h / 2], color=ORANGE, lw=1.0, zorder=2)
    arrow(ax, (loop_x, hypothesis + hypothesis_h / 2), (left + w, hypothesis + hypothesis_h / 2), color=ORANGE,
          lw=1.0)
    notes_x = loop_x + 0.08
    note(ax, notes_x, top, "Symphony: one agent\nholds each task; agents\nwork in parallel", va="top")
    loop_middle = (hypothesis + hypothesis_h / 2 + gate + gate_h / 2) / 2
    note(ax, notes_x, loop_middle, "Not yet: the result,\nnull or not, is kept;\nthe agent revises its\nhypothesis",
         color=ORANGE)
    note(ax, notes_x, bottom, "Scored by a hidden\ncheck, with and without\nthe checks", color=MUTED, va="bottom")


def draw_route(ax, x, top, bottom):
    """Panel b, after the extension's own diagram: where a trainee's question goes."""
    panel_title(ax, x, top + 0.11, "b", "Aim 2: the trainee's agent")
    browser_h, middle_h, gpu_h = 0.3, 0.4, 0.27
    box(ax, x + 0.02, top - browser_h, 1.96, browser_h, "claude.ai in the trainee's browser,\nwith the Beethoven extension")
    middle = top - browser_h - 0.26 - middle_h
    servers_w, worker_x, worker_w = 0.68, x + 0.9, 1.08
    box(ax, x + 0.02, middle, servers_w, middle_h, "Claude\nservers:\nthe model")
    box(ax, worker_x, middle, worker_w, middle_h, "WSU grid: the\ntrainee's Claude Code\nworker, a Slurm job",
        face=TEAL_PALE, edge=TEAL)
    box(ax, worker_x, bottom, worker_w, gpu_h, "H200 GPUs,\n4 nodes of 4")

    chat_x, session_x = x + 0.02 + servers_w / 2, worker_x + worker_w / 2
    arrow(ax, (chat_x, top - browser_h), (chat_x, middle + middle_h))
    gap_middle = middle + middle_h + 0.13
    note(ax, chat_x - 0.05, gap_middle, "a chat", color=MUTED, ha="right")
    arrow(ax, (session_x, top - browser_h), (session_x, middle + middle_h))
    note(ax, session_x - 0.05, gap_middle, "one click:\na Code session", color=MUTED, ha="right")
    arrow(ax, (x + 0.02 + servers_w, middle + middle_h / 2), (worker_x, middle + middle_h / 2), style="<|-|>")
    # No worker has yet sent a GPU job, only test submissions, so the arrow is drawn as built and not yet run, with
    # its label beside it in the gap between the worker and the GPUs.
    gpu_x = worker_x + 0.18
    arrow(ax, (gpu_x, middle), (gpu_x, bottom + gpu_h), color=ORANGE)
    note(ax, gpu_x - 0.05, (middle + bottom + gpu_h) / 2, "built to send GPU jobs", color=ORANGE, ha="right")


def draw_cohort(fig, ax, x, top, bottom):
    """Panel c: the 2026 cohort's mean comfort in six domains, recalled before and rated after."""
    panel_title(ax, x, top + 0.11, "c", "2026 cohort, n = 16")
    note(ax, x + 0.16, top, "gray: before (recalled); green: after", va="top")
    plot = inset(fig, x + 1.24, bottom + 0.27, 0.9, top - 0.2 - (bottom + 0.27))
    rows = list(range(len(COHORT)))[::-1]
    for y, (_, before, after) in zip(rows, COHORT):
        plot.plot([before, after], [y, y], color=RULE, lw=1.4, zorder=1, solid_capstyle="round")
        plot.scatter([before], [y], s=13, color=DOT_BEFORE, zorder=2, linewidths=0)
        plot.scatter([after], [y], s=15, color=TEAL, zorder=3, linewidths=0)
    plot.set_yticks(rows)
    plot.set_yticklabels([name for name, _, _ in COHORT], fontsize=LABEL, color=INK)
    plot.set_xlim(1, 5)
    plot.set_xticks([1, 2, 3, 4, 5])
    plot.tick_params(axis="both", length=2, width=0.5, labelsize=LABEL, pad=2)
    plot.tick_params(axis="y", length=0)
    plot.set_ylim(-0.6, len(COHORT) - 0.4)
    plot.grid(axis="x", color=GRID, lw=0.5)
    plot.set_axisbelow(True)
    for side in ("top", "right", "left"):
        plot.spines[side].set_visible(False)
    plot.set_xlabel("mean comfort, 1 to 5", fontsize=LABEL, labelpad=1.5, color=INK)


def draw_three_images(ax, x, top, bottom):
    """Panel d: a sixth lumbar vertebra in a labeled CT, its physics render and another person's radiograph."""
    panel_title(ax, x, top + 0.11, "d", "Aim 3: from labeled CT to X-ray")
    tile_h, gap, tile_bottom = 1.08, 0.03, bottom + 0.25
    labels = ("labeled CT", "physics render", "another person's\nradiograph")
    for name, label in zip(("l6_labeled_ct.png", "l6_render.png", "l6_film.png"), labels):
        tile_w = place_image(ax, open_image(name), x, tile_bottom, tile_h)
        note(ax, x + tile_w / 2, tile_bottom - 0.04, label, ha="center", va="top")
        x += tile_w + gap
    note(ax, x - gap, top, "scale bars, 20 mm", color=MUTED, ha="right", va="top")


def draw_rag_llm(ax, x, top, bottom):
    """Panel e: the RAG-LLM, its two inputs and its answer inside the dashed line of the WSU grid, and OpenEvidence
    outside it, sent only the question and the detectors' reading. Nothing here is built yet, so no box is green."""
    panel_title(ax, x, top + 0.11, "e", "Aim 3: the spine RAG-LLM")
    right, inner = x + 2.06, 0.05
    # The grid's line leaves out the lower right corner, where OpenEvidence sits.
    split, notch = x + 1.21, bottom + 0.4
    corners = [(x + 0.004, bottom + 0.004), (x + 0.004, top), (right - 0.004, top), (right - 0.004, notch),
               (split, notch), (split, bottom + 0.004)]
    ax.add_patch(Polygon(corners, closed=True, fill=False, ec=MUTED, lw=0.7, ls=(0, (3, 2)), zorder=2))
    ax.text(x + 0.08, top, "WSU grid", fontsize=LABEL, color=MUTED, ha="left", va="center", zorder=6,
            bbox={"boxstyle": "square,pad=0.15", "fc": "white", "ec": "none"})

    input_w, input_h, input_top = 0.94, 0.4, top - 0.09
    image_x, index_x = x + inner, right - inner - input_w
    box(ax, image_x, input_top - input_h, input_w, input_h, "The image, read by\nthe detectors and\nthe level model")
    box(ax, index_x, input_top - input_h, input_w, input_h, "Scopus and\nScienceDirect spine\nliterature, indexed")
    model_h, model_top = 0.4, input_top - input_h - 0.16
    box(ax, image_x, model_top - model_h, right - inner - image_x, model_h,
        "Multimodal RAG-LLM, fine-tuned on\npublic datasets' images, then on images\nwith charts under the pending protocol")
    arrow_middle = (input_top - input_h + model_top) / 2
    for centre, label in ((image_x + input_w / 2, "reading"), (index_x + input_w / 2, "retrieved passages")):
        arrow(ax, (centre, input_top - input_h), (centre, model_top))
        note(ax, centre - 0.05, arrow_middle, label, color=MUTED, ha="right")

    answer_h, answer_top = 0.3, model_top - model_h - 0.13
    answer_w = split - inner - image_x
    box(ax, image_x, answer_top - answer_h, answer_w, answer_h, "Answer: level, finding,\nverbatim quotations")
    arrow(ax, (image_x + answer_w / 2, model_top - model_h), (image_x + answer_w / 2, answer_top))
    note(ax, split + 0.06, bottom + 0.02, "OpenEvidence gets\nonly the question\nand the reading", color=MUTED,
         va="bottom")


def draw_results(fig, ax, x, top, bottom):
    """Panel f: the level named exactly, and vertebrae found on a C-arm the detector never trained on, as a dot plot
    with one row a result, each value in the column on the right."""
    panel_title(ax, x, top + 0.11, "f", "Held-out results on a public C-arm")
    step, axis_y = 0.12, bottom + 0.2
    plot_x, plot_w, right = x + 1.2, 0.92, WIDTH
    plot = inset(fig, plot_x, axis_y, plot_w, top - axis_y)
    plot.set_xlim(-3, 103)
    plot.set_ylim(axis_y, top)  # inches, as the canvas, so a row's label and its points share one y

    y = top - 0.05
    note(ax, x, y, "Level named exactly", weight="bold")
    for label, value, interval, _ in NAMING:
        y -= step
        note(ax, plot_x - 0.06, y, label, ha="right")
        interval_bar(plot, interval, y, TEAL)
        plot.scatter([value], [y], s=7, color=TEAL, zorder=3, linewidths=0, clip_on=False)
        note(ax, right, y, f"{value:.1f}", ha="right")

    y -= step + 0.04
    note(ax, x, y, "Vertebrae found, of 287", weight="bold")
    draw_detection_key(plot, y)
    plot.text(TARGET - 2, y, "97 %", fontsize=LABEL, ha="right", va="center", bbox=MASK)
    target_top = y + 0.04
    for label, value, interval, value_low, interval_low, _ in DETECTION:
        y -= step
        note(ax, plot_x - 0.06, y, label, ha="right")
        # The two thresholds sit just above and below the row's line, so their intervals never cover each other.
        for point, bar, offset, filled in ((value, interval, 0.03, True), (value_low, interval_low, -0.03, False)):
            if bar:
                interval_bar(plot, bar, y + offset, ORANGE)
            plot.scatter([point], [y + offset], s=9 if filled else 12, facecolors=ORANGE if filled else "white",
                         edgecolors=ORANGE, linewidths=0 if filled else 0.9, zorder=3, clip_on=False)
        note(ax, right, y, f"{value:.1f}, {value_low:.1f}", ha="right")
    plot.plot([TARGET, TARGET], [axis_y, target_top], color=INK, lw=0.6, ls=(0, (3, 2)), zorder=1)

    plot.set_xticks([0, 25, 50, 75, 100])
    plot.set_xticklabels(["0", "", "50", "", "100 %"])
    plot.tick_params(axis="x", length=2, width=0.5, labelsize=LABEL, pad=1.5)
    plot.set_yticks([])
    plot.grid(axis="x", color=GRID, lw=0.5)
    plot.set_axisbelow(True)
    for side in ("top", "right", "left"):
        plot.spines[side].set_visible(False)


def interval_bar(plot, interval, y, color):
    """A 95 % interval as a line with short caps, so that one narrower than its point still shows its ends."""
    low, high = interval
    plot.plot([low, high], [y, y], color=color, lw=1.0, solid_capstyle="butt", zorder=2)
    for end in (low, high):
        plot.plot([end, end], [y - 0.025, y + 0.025], color=color, lw=0.8, solid_capstyle="butt", zorder=2)


def draw_detection_key(plot, y):
    """The two thresholds' points, named on the section's own line; the white behind each name hides the grid."""
    plot.scatter([2], [y], s=9, color=ORANGE, linewidths=0, clip_on=False)
    plot.text(7, y, "0.74", fontsize=LABEL, va="center", ha="left", clip_on=False, bbox=MASK)
    plot.scatter([37], [y], s=12, facecolors="white", edgecolors=ORANGE, linewidths=0.9, clip_on=False)
    plot.text(42, y, "0.25", fontsize=LABEL, va="center", ha="left", clip_on=False, bbox=MASK)


def check(fig):
    """The panel's own proof that it can be read at print: every label at LABEL points or more, inside the panel,
    inside its box with PAD to spare, and clear of every other label, every other box, the images and the data
    points. Lines, arrows and grid lines are not obstacles: a label set over grid lines carries MASK. Returns the
    problems found."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pad = PAD * fig.dpi
    panel = fig.bbox
    labels = [text for text in fig.findobj(Text) if text.get_visible() and text.get_text().strip()]
    extents = {id(text): text.get_window_extent(renderer) for text in labels}
    own_box = {id(label): id(patch) for patch, label in BOXED}
    problems = []
    for text in labels:
        extent = extents[id(text)]
        if text.get_fontsize() < LABEL:
            problems.append(f"under {LABEL} pt: {text.get_text()!r}")
        if extent.x0 < panel.x0 or extent.y0 < panel.y0 or extent.x1 > panel.x1 or extent.y1 > panel.y1:
            problems.append(f"outside the panel: {text.get_text()!r}")
    for patch, label in BOXED:
        inner = patch.get_window_extent(renderer).padded(-pad)
        extent = extents[id(label)]
        if extent.x0 < inner.x0 or extent.y0 < inner.y0 or extent.x1 > inner.x1 or extent.y1 > inner.y1:
            problems.append(f"too tight in its box: {label.get_text()!r}")
    for first, second in itertools.combinations(labels, 2):
        if extents[id(first)].overlaps(extents[id(second)]):
            problems.append(f"overlap: {first.get_text()!r} and {second.get_text()!r}")
    found = obstacles(fig, renderer)
    for text in labels:
        for name, owner, extent in found:
            if owner is not None and owner == own_box.get(id(text)):
                continue  # a box's own label sits inside it, which the rule above already holds
            if extents[id(text)].overlaps(extent):
                problems.append(f"over {name}: {text.get_text()!r}")
    return problems


def obstacles(fig, renderer):
    """What a label must not cover, as (name, owner, extent): each box, each image and each data point, a point as
    the square its marker fills."""
    found = [("a box", id(patch), patch.get_window_extent(renderer)) for patch, _ in BOXED]
    for axes in fig.axes:
        found += [("an image", None, image.get_window_extent(renderer)) for image in axes.images]
        for points in axes.collections:
            if not isinstance(points, PathCollection):
                continue
            centres = points.get_offset_transform().transform(points.get_offsets())
            half = math.sqrt(max(points.get_sizes())) * fig.dpi / 72 / 2
            found += [("a data point", None, Bbox([[cx - half, cy - half], [cx + half, cy + half]]))
                      for cx, cy in centres]
    return found


def save(fig):
    # No creation date in the PDF, so a panel redrawn from unchanged sources, with the same matplotlib and the same
    # fonts, is byte for byte the same file.
    fig.savefig(PACKET_FIGURES / f"{NAME}.pdf", facecolor="white", metadata={"CreationDate": None})
    fig.savefig(PREVIEWS / f"{NAME}.png", facecolor="white")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="check the panel and write nothing")
    args = parser.parse_args()
    set_style()
    fig = figure_panel()
    width, height = fig.get_size_inches()
    print(f"{NAME}: {width:.2f} x {height:.2f} in")
    problems = check(fig)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        sys.exit(f"{len(problems)} problems; nothing written")
    if not args.check:
        PACKET_FIGURES.mkdir(parents=True, exist_ok=True)
        save(fig)
    plt.close(fig)


if __name__ == "__main__":
    main()
