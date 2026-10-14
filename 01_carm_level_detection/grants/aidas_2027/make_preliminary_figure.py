"""Compose the preliminary-data figure of the AIDaS packet from three figures already in the record.

Panel (a) is the spine cartoon (figures/schwingnet fig1_row2_anatomy at main 5597197), panel (b) the top of the
corpus manifold figure (figS1, same commit), panel (c) the off-by-one problem cartoon (fig1a_problem). The
composition is plain Pillow so the figure can be rebuilt from the three PNGs beside it without matplotlib.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent / "figures"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
WIDTH = 3960
GAP = 60
MARGIN = 40


def letter(canvas: Image.Image, x: int, y: int, s: str) -> None:
    draw = ImageDraw.Draw(canvas)
    draw.text((x, y), s, fill=(0, 0, 0), font=ImageFont.truetype(FONT, 96))


def fit_width(im: Image.Image, width: int) -> Image.Image:
    h = round(im.height * width / im.width)
    return im.convert("RGB").resize((width, h), Image.LANCZOS)


def main() -> None:
    cartoon = fit_width(Image.open(HERE / "fig_spine_cartoon_typical_vs_t13.png"), WIDTH - 2 * MARGIN)
    manifold = Image.open(HERE / "fig_corpus_tsne_manifold.png").crop((0, 0, 2100, 910))
    problem = Image.open(HERE / "fig_problem_count_off_by_one.png")
    half = (WIDTH - 2 * MARGIN - GAP) // 2
    manifold = fit_width(manifold, half)
    problem = fit_width(problem, half)
    row2 = max(manifold.height, problem.height)
    height = MARGIN + 110 + cartoon.height + GAP + 110 + row2 + MARGIN
    canvas = Image.new("RGB", (WIDTH, height), (255, 255, 255))
    y = MARGIN
    letter(canvas, MARGIN, y, "a")
    canvas.paste(cartoon, (MARGIN, y + 110))
    y += 110 + cartoon.height + GAP
    letter(canvas, MARGIN, y, "b")
    letter(canvas, MARGIN + half + GAP, y, "c")
    canvas.paste(manifold, (MARGIN, y + 110))
    canvas.paste(problem, (MARGIN + half + GAP, y + 110 + (row2 - problem.height) // 2))
    out = HERE / "fig_preliminary_data.png"
    canvas.save(out, optimize=True)
    print("wrote", out, canvas.size)


if __name__ == "__main__":
    main()
