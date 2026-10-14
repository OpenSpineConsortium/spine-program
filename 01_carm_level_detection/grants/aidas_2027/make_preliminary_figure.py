"""Compose Figure 2 of the AIDaS packet, the preliminary data, at full page width.

Three panels: (a) the off-by-one count cartoon (figures/schwingnet/fig1a_problem.pdf at main 5597197, the figure
the owner keeps), (b) the by-source map of the corpus manifold (panel a of figures/schwingnet/figS1.pdf at the
same commit, rendered at 600 dpi and cropped so that no footer or inner letter rides along), and (c) a bar chart
of the held-out results the narrative quotes, drawn here from the rows of docs/handoff/RESULTS_CATALOG.md with
the intervals those rows give (Wilson on the effective sample size, since frames cluster within cases). Plain
Pillow, no matplotlib, so the figure rebuilds from the two PNGs beside it on any machine with Pillow.

Run on a laptop or as an sbatch job; never on the login node (root CLAUDE.md rule 7).
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent / "figures"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
WIDTH = 3960            # 6.9 inches at about 574 dots per inch
MARGIN = 40
GAP = 60
LETTER_H = 110
ROW1_H = 795
CHART_H = 900
GREY = (90, 90, 90)
ORANGE = (224, 123, 32)
BLACK = (0, 0, 0)
LIGHT = (205, 205, 205)

# RESULTS_CATALOG.md rows: (first label line, second label line, rate, low, high, colour).
# A2.1 zero-shot lateral, A3.1 fine-tuned lateral, A3.2 AP, A5.1 coupled, A6.1 and A6.2 the held-out device.
RESULTS = [
    ("Exact level, lateral", "zero-shot, 595 of 617", 96.4, 92.3, 98.4, GREY),
    ("Exact level, lateral", "fine-tuned, 601 of 617", 97.4, 93.2, 99.0, GREY),
    ("Exact level, AP", "fine-tuned, 608 of 631", 96.4, 92.5, 98.3, GREY),
    ("Count and shape coupled", "991 of 1,009 bodies", 98.2, 96.5, 99.5, GREY),
    ("Held-out device at 0.74", "231 of 287 vertebrae", 80.5, 74.1, 86.8, ORANGE),
    ("Held-out device at 0.25", "260 of 287 vertebrae", 90.6, 84.3, 94.5, ORANGE),
]
GATE = 97.0
Y_MIN, Y_MAX = 70.0, 100.0


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """DejaVu Sans where it is installed, else Pillow's own scalable default."""
    path = FONT_DIR / ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    try:
        return ImageFont.truetype(str(path), size)
    except OSError:
        return ImageFont.load_default(size=size)


def fit_height(im: Image.Image, height: int) -> Image.Image:
    width = round(im.width * height / im.height)
    return im.convert("RGB").resize((width, height), Image.LANCZOS)


def fit_width(im: Image.Image, width: int) -> Image.Image:
    height = round(im.height * width / im.width)
    return im.convert("RGB").resize((width, height), Image.LANCZOS)


def results_chart(width: int, height: int) -> Image.Image:
    """Panel (c): one bar per catalog row, its interval as a line with caps, the 97 % gate dashed."""
    im = Image.new("RGB", (width, height), (255, 255, 255))
    d = ImageDraw.Draw(im)
    f_title, f_tick, f_label, f_value = font(50), font(46), font(44), font(50, bold=True)
    x0, x1, y0, y1 = 190, width - 40, 170, height - 170

    def y_of(v: float) -> float:
        return y1 - (v - Y_MIN) / (Y_MAX - Y_MIN) * (y1 - y0)

    d.text((x0, 14), "Held-out results with 95 % Wilson intervals; grey: exact level naming; "
           "orange: detection on a device never trained on", font=f_title, fill=BLACK)
    for v in (70, 80, 90, 100):
        y = y_of(v)
        d.line([(x0, y), (x1, y)], fill=LIGHT, width=3)
        d.text((x0 - 24, y), f"{v} %", font=f_tick, fill=BLACK, anchor="rm")
    d.line([(x0, y0), (x0, y1)], fill=BLACK, width=4)
    d.line([(x0, y1), (x1, y1)], fill=BLACK, width=4)
    yg = y_of(GATE)
    for xs in range(x0, x1, 48):
        d.line([(xs, yg), (min(xs + 28, x1), yg)], fill=BLACK, width=5)
    d.text((x1 - 10, yg - 12), f"{GATE:.0f} % gate", font=f_tick, fill=BLACK, anchor="rb")
    slot = (x1 - x0) / len(RESULTS)
    bar_w = slot * 0.52
    for i, (line1, line2, rate, lo, hi, colour) in enumerate(RESULTS):
        cx = x0 + slot * (i + 0.5)
        left, right = cx - bar_w / 2, cx + bar_w / 2
        d.rectangle([left, y_of(rate), right, y1], fill=colour)
        d.line([(cx, y_of(lo)), (cx, y_of(hi))], fill=BLACK, width=6)
        for v in (lo, hi):
            d.line([(cx - 28, y_of(v)), (cx + 28, y_of(v))], fill=BLACK, width=6)
        label = f"{rate:.1f} %"
        box = d.textbbox((cx, y_of(hi) - 16), label, font=f_value, anchor="mb")
        d.rectangle([box[0] - 10, box[1] - 4, box[2] + 10, box[3] + 4], fill=(255, 255, 255))
        d.text((cx, y_of(hi) - 16), label, font=f_value, fill=BLACK, anchor="mb")
        d.text((cx, y1 + 22), line1, font=f_label, fill=BLACK, anchor="ma")
        d.text((cx, y1 + 82), line2, font=f_label, fill=BLACK, anchor="ma")
    return im


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=HERE / "fig_preliminary_data.png")
    args = ap.parse_args()
    cartoon = Image.open(HERE / "fig_problem_count_off_by_one.png")
    by_source = Image.open(HERE / "fig_corpus_tsne_by_source.png")
    inner = WIDTH - 2 * MARGIN - GAP
    aspect = cartoon.width / cartoon.height + by_source.width / by_source.height
    row1_h = min(ROW1_H, int(inner / aspect))
    cartoon = fit_height(cartoon, row1_h)
    by_source = fit_height(by_source, row1_h)
    chart = results_chart(WIDTH - 2 * MARGIN, CHART_H)
    height = MARGIN + LETTER_H + row1_h + GAP + LETTER_H + chart.height + MARGIN
    canvas = Image.new("RGB", (WIDTH, height), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    f_letter = font(100, bold=True)
    y = MARGIN
    draw.text((MARGIN, y), "a", font=f_letter, fill=BLACK)
    canvas.paste(cartoon, (MARGIN, y + LETTER_H))
    xb = WIDTH - MARGIN - by_source.width
    draw.text((xb, y), "b", font=f_letter, fill=BLACK)
    canvas.paste(by_source, (xb, y + LETTER_H))
    y += LETTER_H + row1_h + GAP
    draw.text((MARGIN, y), "c", font=f_letter, fill=BLACK)
    canvas.paste(chart, (MARGIN, y + LETTER_H))
    canvas.save(args.out, optimize=True)
    print("wrote", args.out, canvas.size)


if __name__ == "__main__":
    main()
