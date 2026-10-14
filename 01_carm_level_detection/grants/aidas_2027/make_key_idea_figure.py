#!/usr/bin/env python3
"""Draw the key-idea figure of the AIDaS 2027 seed packet as SVG, with the standard library only.

The figure has three panels, one per Specific Aim, read left to right: (a) the autonomous agent loop that writes
and repairs grid jobs until a pre-stated gate passes, (b) the medical trainee who drives that loop from a Claude
Code worker running as a Slurm job in the trainee's own grid account, and (c) the anatomy-aware C-arm pipeline
that the agents extend, from labelled CT through a rendered exposure to a level name or an abstention. One
sentence under the panels says how the aims feed each other.

Usage:  python3 make_key_idea_figure.py [--out figures/fig_key_idea.svg]

The PNG beside it is rendered from this SVG (README.md of this folder says how). Every text is Liberation Sans or
Arial; the colour code follows the SchwingNet figure set: light blue for a learned or generative stage, grey for
everything else, orange for the one loop the figure is about. Text is sized to its box by a width estimate of
0.50 em per character, so no row runs past its box in a renderer with Arial metrics.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

W, H = 2120, 1340
FONT = "Liberation Sans, Arial, Helvetica, sans-serif"
GREY_FILL = "#f2f2f2"
GREY_EDGE = "#333333"
BLUE_FILL = "#d6e6f5"
ORANGE = "#e07b00"
BLACK = "#000000"
NOTE = "#444444"

PANEL_W = 680
GUTTER = 20
LEFT = 20
PANEL_TOP = 120
PANEL_BOTTOM = 1230
CHAR_EM = 0.50  # estimated width of one character in em, Arial metrics, mixed case


def fit(rows: list[str], size: int, width: float) -> int:
    """The largest font size at or below size whose longest row fits the width."""
    longest = max(len(r) for r in rows)
    return int(min(size, width / (CHAR_EM * longest)))


def text(x: float, y: float, s: str, size: int = 40, weight: str = "normal", anchor: str = "middle",
         fill: str = BLACK) -> str:
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}">{s}</text>')


def lines(x: float, y: float, rows: list[str], size: int = 38, weight: str = "normal", anchor: str = "middle",
          fill: str = BLACK, leading: float = 1.22) -> str:
    """Several rows of text centred on (x, y): y is the vertical middle of the block."""
    step = size * leading
    y0 = y - step * (len(rows) - 1) / 2 + size * 0.35
    return "\n".join(text(x, y0 + i * step, r, size, weight, anchor, fill) for i, r in enumerate(rows))


def box(x: float, y: float, w: float, h: float, rows: list[str], fill: str = GREY_FILL, size: int = 38,
        weight: str = "normal") -> str:
    rect = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="18" ry="18" fill="{fill}" '
            f'stroke="{GREY_EDGE}" stroke-width="4"/>')
    return rect + "\n" + lines(x + w / 2, y + h / 2, rows, fit(rows, size, w - 36), weight)


def arrow(x1: float, y1: float, x2: float, y2: float, color: str = BLACK, width: float = 5,
          head: float = 26) -> str:
    """A straight arrow with a polygon head, since not every renderer draws SVG markers."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    bx, by = x2 - ux * head, y2 - uy * head
    px, py = -uy, ux
    half = head * 0.55
    line = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{color}" '
            f'stroke-width="{width}"/>')
    tri = (f'<polygon points="{x2:.1f},{y2:.1f} {bx + px * half:.1f},{by + py * half:.1f} '
           f'{bx - px * half:.1f},{by - py * half:.1f}" fill="{color}"/>')
    return line + "\n" + tri


def elbow(points: list[tuple[float, float]], color: str = ORANGE, width: float = 5, head: float = 26) -> str:
    """A polyline through the points with an arrowhead on the last segment."""
    parts = []
    for (x1, y1), (x2, y2) in zip(points[:-2], points[1:-1]):
        parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
                     f'stroke-width="{width}"/>')
    (x1, y1), (x2, y2) = points[-2], points[-1]
    parts.append(arrow(x1, y1, x2, y2, color, width, head))
    return "\n".join(parts)


def side_note(x: float, y: float, s: str, size: int = 28, room: float = 310) -> str:
    """A note beside an arrow, shrunk to the room left before the panel's edge."""
    return text(x, y, s, fit([s], size, room), "normal", "start", NOTE)


def panel_frame(x: float, letter: str, title: str, subtitle: str) -> str:
    out = [f'<rect x="{x}" y="{PANEL_TOP - 90}" width="{PANEL_W}" height="{PANEL_BOTTOM - PANEL_TOP + 90}" '
           f'rx="24" ry="24" fill="#ffffff" stroke="#999999" stroke-width="3"/>']
    out.append(text(x + 28, PANEL_TOP - 36, letter, 56, "bold", "start"))
    out.append(text(x + 90, PANEL_TOP - 40, title, 44, "bold", "start"))
    out.append(text(x + 90, PANEL_TOP + 4, subtitle, fit([subtitle], 30, PANEL_W - 110), "normal", "start", NOTE))
    return "\n".join(out)


def panel_a(x: float) -> str:
    """The agent loop: five stages in a column, the repair loop drawn in orange on the right."""
    cx = x + 290
    bw, bh = 470, 112
    ys = [200, 372, 544, 716, 888]
    rows = [
        (["Read the repository", "CLAUDE.md, TODO, the board"], GREY_FILL),
        (["Plan and pre-register", "rule, gate, inputs; hashed"], GREY_FILL),
        (["Generate the job script", "sbatch file, partition, QoS"], BLUE_FILL),
        (["Submit as a Slurm job", "the login node runs nothing"], GREY_FILL),
        (["Read logs and exceptions", "a refused job, a traceback"], GREY_FILL),
    ]
    out = []
    for y, (r, fill) in zip(ys, rows):
        out.append(box(cx - bw / 2, y, bw, bh, r, fill, 36))
    for y1, y2 in zip(ys[:-1], ys[1:]):
        out.append(arrow(cx, y1 + bh, cx, y2))
    rx = cx + bw / 2 + 40
    out.append(elbow([(cx + bw / 2, ys[4] + bh / 2), (rx, ys[4] + bh / 2), (rx, ys[2] + bh / 2),
                      (cx + bw / 2, ys[2] + bh / 2)], ORANGE))
    ly = (ys[2] + ys[4]) / 2 + 40
    out.append(text(rx + 12, ly, "repair", 30, "bold", "start", ORANGE))
    out.append(text(rx + 12, ly + 36, "without", 24, "normal", "start", ORANGE))
    out.append(text(rx + 12, ly + 68, "a person", 24, "normal", "start", ORANGE))
    out.append(arrow(cx, ys[4] + bh, cx, 1092))
    out.append(box(cx - bw / 2, 1092, bw, 112, ["Gate passed: pull request", "every number with its file"],
                   GREY_FILL, 34, "bold"))
    return "\n".join(out)


def panel_b(x: float) -> str:
    """The trainee in the loop."""
    cx = x + PANEL_W / 2
    bw, bh = 580, 112
    out = []
    out.append(box(cx - bw / 2, 200, bw, bh, ["Medical trainee", "claude.ai and the Beethoven extension"],
                   GREY_FILL, 36))
    out.append(arrow(cx, 312, cx, 372))
    out.append(side_note(cx + 20, 352, "a pre-registered question"))
    out.append(box(cx - bw / 2, 372, bw, bh, ["Claude Code worker", "a Slurm job in the trainee's own account"],
                   BLUE_FILL, 36))
    out.append(arrow(cx, 484, cx, 544))
    out.append(side_note(cx + 20, 524, "the agent loop of (a)"))
    out.append(box(cx - bw / 2, 544, bw, 150, ["WSU grid: 4 nodes x 4 H200 GPUs", "CPU partition reqp; GPU partitions",
                                               "gmsap, gvohp, galhp; Ceph volume"], GREY_FILL, 34))
    out.append(arrow(cx, 694, cx, 754))
    out.append(side_note(cx + 20, 734, "job ids, logs, a result file"))
    out.append(box(cx - bw / 2, 754, bw, 112, ["Pull request on the board", "mentor review, then the merge"],
                   GREY_FILL, 36))
    out.append(arrow(cx, 866, cx, 926))
    out.append(box(cx - bw / 2, 926, bw, 278,
                   ["Measured per trainee:", "six-domain comfort, before and after",
                    "time to the first successful job", "tasks passed without a mentor",
                    "projects reaching a pull request"], GREY_FILL, 32))
    return "\n".join(out)


def panel_c(x: float) -> str:
    """CT to C-arm exposure to level name."""
    cx = x + PANEL_W / 2
    bw, bh = 580, 112
    out = []
    out.append(box(cx - bw / 2, 200, bw, bh, ["802 labelled CTs (CTSpinoPelvic1K)", "every vertebra, the sacrum, the hips"],
                   GREY_FILL, 34))
    out.append(arrow(cx, 312, cx, 372))
    out.append(side_note(cx + 20, 352, "device-card render"))
    fx, fy, fw, fh = cx - bw / 2, 372, bw, 236
    out.append(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="18" ry="18" fill="#1a1a1a" '
               f'stroke="{GREY_EDGE}" stroke-width="4"/>')
    out.append(text(fx + 20, fy + 42, "2-D C-arm exposure: 3 to 4 bodies in the field", 27, "normal", "start",
                    "#ffffff"))
    for bx in [fx + 80, fx + 235, fx + 390]:
        by = fy + 76
        out.append(f'<rect x="{bx}" y="{by}" width="110" height="110" fill="#d9d9d9" stroke="#ffffff" '
                   f'stroke-width="3"/>')
        for (kx, ky) in [(bx, by), (bx + 110, by), (bx, by + 110), (bx + 110, by + 110)]:
            out.append(f'<circle cx="{kx}" cy="{ky}" r="9" fill="{ORANGE}"/>')
        out.append(f'<rect x="{bx - 10}" y="{by - 10}" width="130" height="130" fill="none" stroke="#6fa8dc" '
                   f'stroke-width="4" stroke-dasharray="10,8"/>')
    out.append(text(fx + fw / 2, fy + fh - 16, "a box and four corner keypoints per body", 26, "normal", "middle",
                    "#ffffff"))
    out.append(arrow(cx, 608, cx, 668))
    out.append(box(cx - bw / 2, 668, bw, 150, ["Detector and level encoder", "name each body from its own shape;",
                                               "count from the detected sacrum"], BLUE_FILL, 34))
    out.append(arrow(cx, 818, cx, 878))
    out.append(box(cx - bw / 2, 878, bw, 112, ["Level name, or abstain", "when the count and the shape disagree"],
                   GREY_FILL, 36, "bold"))
    out.append(arrow(cx, 990, cx, 1050))
    out.append(box(cx - bw / 2, 1050, bw, 154,
                   ["Pre-stated gates on a held-out device:", "97 % detection; under 1 s per exposure;",
                    "paired cadaver CT and X-ray as the sealed test"], GREY_FILL, 31))
    return "\n".join(out)


def build() -> str:
    xa = LEFT
    xb = LEFT + PANEL_W + GUTTER
    xc = LEFT + 2 * (PANEL_W + GUTTER)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}px" height="{H}px" viewBox="0 0 {W} {H}">',
             f'<rect x="0" y="0" width="{W}" height="{H}" fill="#ffffff"/>']
    parts.append(panel_frame(xa, "a", "Foundational AI", "an agent writes and repairs grid jobs"))
    parts.append(panel_frame(xb, "b", "Education and workforce", "a trainee drives the agent on the grid"))
    parts.append(panel_frame(xc, "c", "Health", "anatomy-aware inference on C-arm exposures"))
    parts.append(panel_a(xa))
    parts.append(panel_b(xb))
    parts.append(panel_c(xc))
    parts.append(lines(W / 2, H - 62,
                       ["The loop of (a) runs inside the trainee's worker in (b), and the trainees' tasks extend "
                        "the pipeline of (c);",
                        "every number passes a pre-stated gate before it is quoted."], 30, "normal", "middle"))
    parts.append("</svg>")
    return "\n".join(parts)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "figures" / "fig_key_idea.svg"))
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="ascii", newline="\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
