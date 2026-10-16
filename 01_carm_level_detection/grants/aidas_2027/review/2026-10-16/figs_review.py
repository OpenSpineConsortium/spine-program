"""Apply the review's findings to make_figures.py: panel e's grid line and OpenEvidence, panel b's GPU label,
panel c's ticks, panel f's goal label and offsets, and a check that writes nothing until the panel passes it."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
s = path.read_text()


def swap(old, new):
    global s
    count = s.count(old)
    if count != 1:
        sys.exit(f"expected once, found {count}: {old[:90]!r}")
    s = s.replace(old, new)


swap('''The panel is drawn 7.2 in wide, the text width of letter paper less two 0.65 inch margins, and latex/main.tex
places it at that width, so every label prints at the size it is drawn here, 7 pt or more. Every number drawn is
typed once, in NAMING, DETECTION, TARGET and COHORT below, beside the file it comes from; RECORD.md lists the same
rows. figures/sources/SOURCES.md says where each image came from. Run it on a laptop or as an sbatch job, never on
a login node:

    python3 make_figures.py            # writes latex/figures/fig1_panel.pdf for the packet and a 300 dpi
                                       # preview of it, figures/fig1_panel.png
    python3 make_figures.py --check    # also prints the panel's size, and fails when a label is under 7 pt,
                                       # leaves the panel or its box, or overlaps another label
''', '''The panel is drawn 7.2 in wide, the text width of letter paper less two 0.65 inch margins, and latex/main.tex
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
''')
swap('''import argparse
import itertools
import sys
''', '''import argparse
import itertools
import math
import sys
''')
swap('''from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402
''', '''from matplotlib.collections import PathCollection  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle  # noqa: E402
from matplotlib.transforms import Bbox  # noqa: E402
''')
swap('''WIDTH = 7.2  # inches: letter paper less two 0.65 inch margins, the width main.tex places the panel at
''', '''WIDTH = 7.2  # inches: letter paper less two 0.65 inch margins, main.tex's text width
''')
swap('''TEAL = "#0f5f55"  # Beethoven's own green: what works or passes
TEAL_PALE = "#e3efec"
ORANGE = "#eb6834"  # what fails today, or is built and not yet run
ORANGE_PALE = "#fbe3d8"
GREY_PALE''', '''TEAL = "#0f5f55"  # Beethoven's own green: Beethoven, what passes, the cohort's after and the naming results
TEAL_PALE = "#e3efec"
ORANGE = "#eb6834"  # the loop that repeats, what is built and not yet run, and detection, short of its goal
GREY_PALE''')

# Each run starts the record of boxes afresh, so that drawing the panel twice in one process checks it once.
swap('''def figure_panel():
    fig, ax = new_canvas()
''', '''def figure_panel():
    BOXED.clear()
    fig, ax = new_canvas()
''')

# Panel b: the GPU label beside its arrow, between the worker and the GPUs.
swap('''    browser_h, middle_h, gpu_h = 0.3, 0.42, 0.27
    box(ax, x + 0.02, top - browser_h, 1.96, browser_h, "claude.ai in the trainee's browser,\\nwith the Beethoven extension")
    middle = top - browser_h - 0.3 - middle_h
''', '''    browser_h, middle_h, gpu_h = 0.3, 0.4, 0.27
    box(ax, x + 0.02, top - browser_h, 1.96, browser_h, "claude.ai in the trainee's browser,\\nwith the Beethoven extension")
    middle = top - browser_h - 0.26 - middle_h
''')
swap('''    note(ax, chat_x - 0.05, middle + middle_h + 0.15, "a chat", color=MUTED, ha="right")
    arrow(ax, (session_x, top - browser_h), (session_x, middle + middle_h))
    note(ax, session_x - 0.05, middle + middle_h + 0.15, "one click:\\na Code session", color=MUTED, ha="right")
    arrow(ax, (x + 0.02 + servers_w, middle + middle_h / 2), (worker_x, middle + middle_h / 2), style="<|-|>")
    # No worker has yet sent a GPU job, only test submissions, so the arrow is drawn as built and not yet run.
    arrow(ax, (session_x, middle), (session_x, bottom + gpu_h), color=ORANGE)
    note(ax, worker_x - 0.06, bottom + gpu_h / 2, "built to send\\nGPU jobs", color=ORANGE, ha="right")
''', '''    gap_middle = middle + middle_h + 0.13
    note(ax, chat_x - 0.05, gap_middle, "a chat", color=MUTED, ha="right")
    arrow(ax, (session_x, top - browser_h), (session_x, middle + middle_h))
    note(ax, session_x - 0.05, gap_middle, "one click:\\na Code session", color=MUTED, ha="right")
    arrow(ax, (x + 0.02 + servers_w, middle + middle_h / 2), (worker_x, middle + middle_h / 2), style="<|-|>")
    # No worker has yet sent a GPU job, only test submissions, so the arrow is drawn as built and not yet run, with
    # its label beside it in the gap between the worker and the GPUs.
    gpu_x = worker_x + 0.18
    arrow(ax, (gpu_x, middle), (gpu_x, bottom + gpu_h), color=ORANGE)
    note(ax, gpu_x - 0.05, (middle + bottom + gpu_h) / 2, "built to send GPU jobs", color=ORANGE, ha="right")
''')

# Panel c: the inset placed from the panel's own x, and no tick marks beside the domain names.
swap('''    plot = inset(fig, 6.24, bottom + 0.27, 0.9, top - 0.2 - (bottom + 0.27))
''', '''    plot = inset(fig, x + 1.24, bottom + 0.27, 0.9, top - 0.2 - (bottom + 0.27))
''')
swap('''    plot.tick_params(axis="both", length=2, width=0.5, labelsize=LABEL, pad=2)
    plot.set_ylim(-0.6, len(COHORT) - 0.4)
''', '''    plot.tick_params(axis="both", length=2, width=0.5, labelsize=LABEL, pad=2)
    plot.tick_params(axis="y", length=0)
    plot.set_ylim(-0.6, len(COHORT) - 0.4)
''')

# Panel e: everything on the grid inside a dashed line, OpenEvidence outside it with what it is sent.
old_e = s[s.index("def draw_rag_llm(ax, x, top, bottom):"):s.index("def draw_results(")]
new_e = '''def draw_rag_llm(ax, x, top, bottom):
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
    box(ax, image_x, input_top - input_h, input_w, input_h, "The image, read by\\nthe detectors and\\nthe level model")
    box(ax, index_x, input_top - input_h, input_w, input_h, "Scopus and\\nScienceDirect spine\\nliterature, indexed")
    model_h, model_top = 0.4, input_top - input_h - 0.16
    box(ax, image_x, model_top - model_h, right - inner - image_x, model_h,
        "Multimodal RAG-LLM, fine-tuned on\\npublic datasets' images, then on images\\nwith charts under the pending protocol")
    arrow_middle = (input_top - input_h + model_top) / 2
    for centre, label in ((image_x + input_w / 2, "reading"), (index_x + input_w / 2, "retrieved passages")):
        arrow(ax, (centre, input_top - input_h), (centre, model_top))
        note(ax, centre - 0.05, arrow_middle, label, color=MUTED, ha="right")

    answer_h, answer_top = 0.3, model_top - model_h - 0.13
    answer_w = split - inner - image_x
    box(ax, image_x, answer_top - answer_h, answer_w, answer_h, "Answer: level, finding,\\nverbatim quotations")
    arrow(ax, (image_x + answer_w / 2, model_top - model_h), (image_x + answer_w / 2, answer_top))
    note(ax, split + 0.06, bottom + 0.02, "OpenEvidence gets\\nonly the question\\nand the reading", color=MUTED,
         va="bottom")


'''
s = s.replace(old_e, new_e)

# Panel f: wider offsets between the two thresholds, smaller naming dots, the goal at the top of its line.
swap('''        plot.scatter([value], [y], s=9, color=TEAL, zorder=3, linewidths=0, clip_on=False)
''', '''        plot.scatter([value], [y], s=7, color=TEAL, zorder=3, linewidths=0, clip_on=False)
''')
swap('''    y -= step + 0.04
    note(ax, x, y, "Vertebrae found, of 287", weight="bold")
    draw_detection_key(plot, y)
    target_top = y - step / 2
''', '''    y -= step + 0.04
    note(ax, x, y, "Vertebrae found, of 287", weight="bold")
    draw_detection_key(plot, y)
    plot.text(TARGET - 2, y, "97 %", fontsize=LABEL, ha="right", va="center", bbox=MASK)
    target_top = y + 0.04
''')
swap('''        for point, bar, offset, filled in ((value, interval, 0.022, True), (value_low, interval_low, -0.022, False)):
''', '''        for point, bar, offset, filled in ((value, interval, 0.03, True), (value_low, interval_low, -0.03, False)):
''')
swap('''    plot.plot([TARGET, TARGET], [axis_y, target_top], color=INK, lw=0.6, ls=(0, (3, 2)), zorder=1)
    plot.text(TARGET - 2, y, "97 % goal", fontsize=LABEL, ha="right", va="center")
''', '''    plot.plot([TARGET, TARGET], [axis_y, target_top], color=INK, lw=0.6, ls=(0, (3, 2)), zorder=1)
''')
swap('''def draw_detection_key(plot, y):
    plot.scatter([2], [y], s=9, color=ORANGE, linewidths=0, clip_on=False)
    plot.text(7, y, "at 0.74", fontsize=LABEL, va="center", ha="left", clip_on=False)
    plot.scatter([52], [y], s=12, facecolors="white", edgecolors=ORANGE, linewidths=0.9, clip_on=False)
    plot.text(57, y, "at 0.25", fontsize=LABEL, va="center", ha="left", clip_on=False)
''', '''def draw_detection_key(plot, y):
    """The two thresholds' points, named on the section's own line; the white behind each name hides the grid."""
    plot.scatter([2], [y], s=9, color=ORANGE, linewidths=0, clip_on=False)
    plot.text(7, y, "0.74", fontsize=LABEL, va="center", ha="left", clip_on=False, bbox=MASK)
    plot.scatter([37], [y], s=12, facecolors="white", edgecolors=ORANGE, linewidths=0.9, clip_on=False)
    plot.text(42, y, "0.25", fontsize=LABEL, va="center", ha="left", clip_on=False, bbox=MASK)
''')
swap('''BOXED = []  # each box with its label, so that the check can hold the label inside the box
''', '''BOXED = []  # each box with its label, so that the check can hold the label inside the box
MASK = {"boxstyle": "square,pad=0.1", "fc": "white", "ec": "none"}  # behind a label set over grid lines
''')

# The check: text against the other boxes, the images and the data points too; and nothing written until it passes.
old_check = s[s.index("def check(fig):"):s.index("def main():")]
new_check = '''def check(fig):
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
    for text in labels:
        for name, owner, extent in obstacles(fig, renderer):
            if owner != own_box.get(id(text)) and extents[id(text)].overlaps(extent):
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


'''
s = s.replace(old_check, new_check)
old_main = s[s.index("def main():"):s.index('if __name__ == "__main__":')]
new_main = '''def main():
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


'''
s = s.replace(old_main, new_main)
path.write_text(s)
