"""paper/cns2026/prep_v15_figs.py — for deck v10 (Greg 2026-09-26: Result 1 and Result 2 look like identical slides):
  * chart_fov_lines.png: Result 1 as a line chart, exact level against how many bodies are in the field (one, three,
    five, the whole frame), lateral and anteroposterior, tuned on other cases and never trained on this C-arm. The
    numbers are Table 3 / Table 4 of the manuscript as already used in table_fov.png (prep_v13_figs.py); the JSON
    beside the chart records them with their denominators.
  * chart_l6.png: the sixth lumbar vertebra, every L6 number the manuscript reports, as columns: the selection split
    (75 of 98 L6 crops named L6; 111 of 1,012 L5 crops mis-named L6), held-out L6 spines on renders (body-level
    recall 56.1-72.4 % over three seeds), the three never-seen real L6 patients on CBCT renders (84 of 180 crops),
    and the real C-arm frames (L6 called on 3 of 233 anchored frames, all flagged; coupled exact 12 of 12 bodies
    against 0 of 12 by counting). Sources: SchwingNet/NUMBERS.md rows 57-58, 431, 466 and LEVELCHECK_MODEL.md §3,
    read from results/figure2/figure2_metrics.json where the file holds them.

    python paper/cns2026/prep_v15_figs.py
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
NAVY, BLUE, PALE, RED, GOLD, GOLD_INK, GREY, INK = "#191D63", "#4C70B7", "#C9D4EC", "#EF4627", "#E0A800", "#9A7300", "#8A8A8A", "#191D63"
plt.rcParams["font.family"] = "Arial"


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    with Image.open(OUT / name) as im:
        print(name, im.size, round(im.size[0] / im.size[1], 2))


# ------------------------------------------------------------------ 1. Result 1 as lines
FIELDS = ["one body", "three bodies", "five bodies", "whole frame"]
ROWS = {  # (exact %, k, n) per field; None where the manuscript reports no cell
    "lateral, tuned on other cases": [(74.8, 451, 603), (93.1, 1079, 1159), (97.0, 647, 667), (97.4, 601, 617)],
    "lateral, never saw this C-arm": [(63.8, 385, 603), (83.7, 970, 1159), None, (96.4, 595, 617)],
    "anteroposterior, tuned": [None, (86.3, 1015, 1176), None, (96.4, 608, 631)],
    "anteroposterior, never saw this C-arm": [None, None, None, (43.7, 276, 631)],
}
STYLE = {"lateral, tuned on other cases": (NAVY, "-", "o"), "lateral, never saw this C-arm": (NAVY, "--", "o"),
         "anteroposterior, tuned": (GOLD, "-", "s"), "anteroposterior, never saw this C-arm": (GOLD, "--", "s")}
fig, ax = plt.subplots(figsize=(9.2, 5.4))
xs = list(range(len(FIELDS)))
ABOVE = {("lateral, tuned on other cases", 0), ("lateral, tuned on other cases", 1), ("lateral, tuned on other cases", 2), ("lateral, tuned on other cases", 3),
         ("anteroposterior, tuned", 1)}
labelled = set()
for name, cells in ROWS.items():
    col, ls, mk = STYLE[name]
    pts = [(x, c[0]) for x, c in zip(xs, cells) if c]
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=col, ls=ls, lw=3, marker=mk, ms=11, mfc="white" if "never" in name else col,
            mew=2.5, label=name, zorder=3)
    for x, c in zip(xs, cells):
        if not c or (x, round(c[0], 1)) in labelled:      # two series share 96.4 at the whole frame: one label
            continue
        labelled.add((x, round(c[0], 1)))
        dy = 11 if (name, x) in ABOVE else -15
        ax.annotate(f"{c[0]:.1f}", (x, c[0]), xytext=(0, dy), textcoords="offset points", ha="center",
                    va="bottom" if dy > 0 else "top", fontsize=13, color=col if col != GOLD else GOLD_INK)
ax.set_xticks(xs); ax.set_xticklabels(FIELDS, fontsize=16); ax.set_xlim(-0.25, 3.25)
ax.set_ylim(38, 104.5); ax.set_ylabel("exact level, %", fontsize=18); ax.tick_params(axis="y", labelsize=14)
ax.axhline(97.6, color=GREY, lw=1.2, ls=(0, (3, 3)), zorder=1)
ax.text(0.05, 98.6, "surgeons with a registration overlay, 97.6 %", fontsize=12.5, color=GREY, ha="left", va="bottom")
ax.grid(axis="y", color="#DDDDDD"); ax.set_axisbelow(True)
for s_ in ("top", "right"):
    ax.spines[s_].set_visible(False)
ax.legend(loc="lower left", bbox_to_anchor=(0.01, 0.03), fontsize=13.5, frameon=False, handlelength=2.6)
fig.tight_layout()
save(fig, "chart_fov_lines.png")
json.dump({f: {n: (c if c else None) for n, cells in ROWS.items() for c in [cells[i]]} for i, f in enumerate(FIELDS)}, open(OUT / "fov_lines.json", "w"), indent=1)

# ------------------------------------------------------------------ 2. the sixth lumbar vertebra
M = json.load(open(SN / "results" / "figure2" / "figure2_metrics.json"))
v = M["validation_neighbours_and_calls"]
l6_own = v["L6"]["called"]["L6"]; n_l6 = v["L6"]["n"]; p_l6 = v["L6"]["persons"]
l5_as_l6 = v["L5"]["called"]["L6"]; n_l5 = v["L5"]["n"]
hl = M["heldout_l6"]
cells = hl.get("cells", {})
# the never-seen crops named L6: 84 of 180 (NUMBERS.md row 58), read from the metrics file when the key is present
try:
    never = cells["whole|primary"]["L6"]["called"]["L6"]
    never_n = cells["whole|primary"]["L6"]["n"]
except Exception:  # noqa: BLE001
    never, never_n = 84 / 180, 180
cols_ = [("selection split:\nL6 crops\nnamed L6", 100 * l6_own, f"{round(l6_own * n_l6)} of {n_l6} crops\n{p_l6} people", NAVY),
         ("selection split:\nL5 crops\nmis-named L6", 100 * l5_as_l6, f"{round(l5_as_l6 * n_l5)} of {n_l5:,} crops", GREY),
         ("10 L6 spines,\nrenders:\nbody recall", (56.1 + 72.4) / 2, "three seeds\n56 to 72 %", NAVY),
         ("never-seen real\nL6 patients:\ncrops named L6", 100 * never, f"{round(never * never_n)} of {never_n} crops\n3 patients", NAVY),
         ("real C-arm frames:\nL6 called, then\ncoupled, bodies exact", 100.0, "3 frames of 2 patients,\nall flagged; 12 of 12", BLUE)]
fig, ax = plt.subplots(figsize=(11.5, 5.4))
xs = [i * 1.3 for i in range(len(cols_))]
ax.bar(xs, [c[1] for c in cols_], width=0.8, color=[c[3] for c in cols_], zorder=3)
ax.errorbar([xs[2]], [(56.1 + 72.4) / 2], yerr=[[(56.1 + 72.4) / 2 - 56.1], [72.4 - (56.1 + 72.4) / 2]], fmt="none", ecolor=INK, elinewidth=2, capsize=9, zorder=4)
for i, (x, (lab, val, sub, col)) in enumerate(zip(xs, cols_)):
    top_ = 72.4 if i == 2 else val
    txt = f"{val:.1f} %" if i not in (2, 4) else ("56–72 %" if i == 2 else "12 of 12")
    ax.text(x, top_ + 1.5, txt, ha="center", va="bottom", fontsize=16, fontweight="bold", color=INK)
    ax.text(x, -4, sub, ha="center", va="top", fontsize=12.5, color=GREY, linespacing=1.15)
ax.set_xticks(xs); ax.set_xticklabels([c[0] for c in cols_], fontsize=13, linespacing=1.1)
ax.xaxis.set_ticks_position("top"); ax.tick_params(axis="x", length=0, pad=6)
ax.set_ylim(0, 112); ax.set_yticks([0, 25, 50, 75, 100]); ax.set_ylabel("%", fontsize=18); ax.tick_params(axis="y", labelsize=14)
for s_ in ("top", "right", "bottom"):
    ax.spines[s_].set_visible(False)
ax.grid(axis="y", color="#DDDDDD"); ax.set_axisbelow(True)
fig.subplots_adjust(bottom=0.16)
save(fig, "chart_l6.png")
json.dump({"selection_L6_named_L6": [round(l6_own * n_l6), n_l6, p_l6], "selection_L5_named_L6": [round(l5_as_l6 * n_l5), n_l5],
           "heldout_render_recall_pct": [56.1, 72.4], "never_seen_crops_named_L6": [round(never * never_n), never_n],
           "carm_L6_calls": "3 of 233 anchored frames, all flagged; coupled exact 12/12, count 0/12 (NUMBERS.md row 466)"},
          open(OUT / "l6_result.json", "w"), indent=1)
print("done")
