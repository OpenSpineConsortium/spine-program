"""paper/cns2026/prep_v20_benzel_profile.py -- slide 5 of the 6-minute CNS deck, v20 (Greg, 2026-10-31, night).

v19's two Benzel panels, built in four clicks, as Greg asked: the line reweighted to Panjabi's sex and age in purple;
then it divides into men (blue) and women (red), each matched to Panjabi's own men and women by age; then the
population is matched to Tan's ten Chinese Singaporean cadavers (green); then to Alonge's 120 Nigerian adults
(orange). No series in the 39 papers measures these chords in African Americans (Yu 2015's Hamann-Todd skeletons
give only the pedicles, Shin 2024 only the discs), so the fourth step is Alonge's Nigerian CTs, the lumbar canal alone.

The figure is split so PowerPoint can move the lines: each state's picture holds the axes, Benzel's lines and
drawing, T13 and L6 and that state's legend, and geometry.json holds where every gold tier line and every reference
point falls on the picture, as fractions of its width and height from the top left, for make_cns_deck_v20_6min.py
to draw as shapes that Morph carries from one click to the next.

The means are grid/reweight.py's (job 40915304, figs_v20_6min/reweighted.json): Panjabi's whole, his 8 men and his
4 women by sex and age within 5 years; Tan's age, height and weight ranges (56 to 77 years, 159 to 172 cm, 50 to
70 kg; 73 of our adults, 16 of them men); Alonge's sex mix and age (ten pseudo-specimens a sex across a normal of
mean 40.2 and SD 10.07 cut to 18 to 65). T13 and L6 stay every spine's means (figs_v18_6min/profile.json).

    python paper/cns2026/prep_v20_benzel_profile.py
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

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from prep_v19_benzel_profile import DPI, EMU, EXTRA, PANELS as V19_PANELS, drawing, stats  # noqa: E402

FIG = HERE / "figs_v20_6min"
PURPLE, BLUE, RED, GREEN, ORANGE = "#7A3E9D", "#1F5FA8", "#C8102E", "#1B7F4B", "#C26A00"
REFERENCE = "#5A5A5A"
EXTRA_INK = "#333333"
STATES = ("panjabi", "sexes", "tan", "alonge")
COLOURS = {"panjabi": (PURPLE, PURPLE), "sexes": (BLUE, RED), "tan": (GREEN, GREEN), "alonge": (ORANGE, ORANGE)}
TARGETS = {"panjabi": ("panjabi", "panjabi"), "sexes": ("panjabi_men", "panjabi_women"), "tan": ("tan", "tan"),
           "alonge": ("alonge", "alonge")}
LINE_PT, REF_PT = 1.8, 0.9

PANELS = {name: dict(spec) for name, spec in V19_PANELS.items()}
PANELS["body"].update(ylim=(10, 60), yticks=range(10, 61, 5), labels=(("Width", "T7", 36.0), ("Depth", "T4", 12.0)))
PANELS["canal"].update(ylim=(10, 35), yticks=range(10, 36, 5), labels=(("Width", "L2", 28.6), ("Depth", "T7", 13.0)))


def reweighted():
    return json.load(open(FIG / "reweighted.json", encoding="utf-8"))


def references():
    """Every reference series as {(state, panel, chord): {level: mean}}: Panjabi's from his tables, Tan's and Alonge's
    from references.csv, Alonge's pooled over his 54 men and 66 women."""
    out = {}
    panjabi = csv.DictReader(l for l in open(FIG / "panjabi.csv", encoding="utf-8") if not l.startswith("#"))
    measures = {m: (name, chord) for name, spec in PANELS.items() for m, chord in zip(spec["panjabi"], ("width", "depth"))}
    for r in panjabi:
        if r["measure"] in measures:
            name, chord = measures[r["measure"]]
            for state in ("panjabi", "sexes"):
                out.setdefault((state, name, chord), {})[r["level"]] = float(r["mean"])
    for r in csv.DictReader(l for l in open(FIG / "references.csv", encoding="utf-8") if not l.startswith("#")):
        mean = float(r["mean"]) if r["mean"] else (54 * float(r["mean_men"]) + 66 * float(r["mean_women"])) / 120
        out.setdefault((r["source"], r["panel"], r["chord"]), {})[r["level"]] = mean
    return out


def axes(spec):
    plt.rcParams.update({"font.family": "Arial", "font.weight": "bold", "axes.labelweight": "bold"})
    fig, ax = plt.subplots(figsize=(spec["emu"][0] / EMU, spec["emu"][1] / EMU), dpi=DPI)
    fig.subplots_adjust(left=0.135, right=0.975, top=0.975, bottom=0.215)
    ticks, place = spec["axis"]()
    ax.set_xlim(min(place.values()) - 0.1, max(place.values()) + 0.35)
    ax.set_ylim(*spec["ylim"])
    ax.set_yticks(list(spec["yticks"]))
    ax.set_xticks([ticks[lv] for lv in ticks] + [place[lv] for lv in EXTRA])
    ax.set_xticklabels([lv[1:] for lv in ticks] + [lv[1:] for lv in EXTRA], fontsize=8.5, fontweight="bold")
    for label, name in zip(ax.get_xticklabels(), list(ticks) + list(EXTRA)):
        if name in EXTRA:
            label.set_color(EXTRA_INK)
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
    return fig, ax, ticks, place


def benzel(ax, spec, ticks, place, profile):
    bx = [ticks[lv] for lv in ticks]
    ax.plot(bx, spec["benzel_width"], "-", color="black", linewidth=1.5, zorder=5)
    ax.plot(bx, spec["benzel_depth"], "--", color="black", linewidth=1.5, zorder=5)
    for word, level, y in spec["labels"]:
        ax.text(place[level], y, word, fontsize=10, ha="center", zorder=6)
    for key, shift in zip(spec["keys"], (-0.13, 0.13)):
        for level in EXTRA:
            found = stats(profile, key, level)
            if found:
                ax.plot([place[level] + shift], [found[0]], "o", color=EXTRA_INK, mfc="white", mew=1.4, ms=4.5, zorder=4)


def legend(ax, spec, state, rw, profile):
    n = rw["people"]
    tan = rw["targets"]["tan"]["who"]
    extra = "T13, L6, all spines (n = %d, %d)" % tuple(
        max((s[2] for key in spec["keys"] if (s := stats(profile, key, lv))), default=0) for lv in EXTRA)
    ours = {
        "panjabi": [(PURPLE, f"Gold tier 3 & 4, reweighted to\nPanjabi's sex and age, N = {n:,} adults")],
        "sexes": [(BLUE, "Men, matched to his 8 men"), (RED, "Women, matched to his 4 women")],
        "tan": [(GREEN, f"Gold tier adults of their age,\nheight and weight, n = {tan['people']}")],
        "alonge": [(ORANGE, "Gold tier, reweighted to\ntheir sex and age")],
    }[state]
    reference = {"panjabi": "Panjabi 1991-92, 12 cadavers", "sexes": "Panjabi 1991-92, 12 cadavers",
                 "tan": "Tan 2004, 10 Chinese\nSingaporean cadavers", "alonge": "Alonge 2021, 120 Nigerian\nadults, CT, L1 to L5"}[state]
    if spec["legend"][0] == "short":      # the canal's legend stands left of Benzel's drawing, so it is kept narrow
        ours = {"panjabi": [(PURPLE, f"Reweighted, N = {n:,}")], "sexes": [(BLUE, "Men, his 8 men"), (RED, "Women, his 4 women")],
                "tan": [(GREEN, "Ours of their build")], "alonge": [(ORANGE, "Ours, reweighted")]}[state]
        reference = {"panjabi": "Panjabi, 12 cadavers", "sexes": "Panjabi, 12 cadavers", "tan": "Tan, 10 cadavers",
                     "alonge": "Alonge, 120 CTs"}[state]
    handles = [Line2D([], [], color="black", lw=1.5, label="Benzel 2015 (digitised)")]
    if not (state == "alonge" and spec["out"] == "benzel_body.png"):
        handles.append(Line2D([], [], color=REFERENCE, lw=REF_PT, ls=":", marker="D", ms=2.6, label=reference))
    handles += [Line2D([], [], color=c, lw=LINE_PT, label=label) for c, label in ours]
    if spec["legend"][0] == "full":
        handles.append(Line2D([], [], color=EXTRA_INK, marker="o", mfc="white", mew=1.4, ms=4.5, ls="none", label=extra))
    kind, x, y, where = spec["legend"]
    ax.legend(handles=handles, loc=where, bbox_to_anchor=(x, y), fontsize=7, frameon=True, framealpha=0.92,
              edgecolor="white", borderpad=0.3, handlelength=1.8, labelspacing=0.3)


def fractions(fig, ax, xs, ys):
    """Data points as fractions of the saved picture's width and height, from its top left."""
    width, height = fig.bbox.width, fig.bbox.height
    out = []
    for x, y in zip(xs, ys):
        px, py = ax.transData.transform((x, y))
        out.append([px / width, 1.0 - py / height])
    return out


def geometry(fig, ax, spec, place, rw, refs):
    usual = sorted((lv for lv in place if lv not in EXTRA), key=place.get)
    states = {}
    for state in STATES:
        lines = {}
        for chord, key in zip(("w", "d"), spec["keys"]):
            for sex, target in zip(("m", "f"), TARGETS[state]):
                measure = rw["targets"][target]["measures"][key]
                levels = [lv for lv in usual if lv in measure]
                lines[f"{chord}_{sex}"] = fractions(fig, ax, [place[lv] for lv in levels],
                                                    [measure[lv]["mean"] for lv in levels])
        points = {}
        for chord, word in (("w", "width"), ("d", "depth")):
            series = refs.get((state if state != "sexes" else "panjabi", spec_name(spec), word), {})
            levels = [lv for lv in usual if lv in series]
            points[chord] = [[lv] + xy for lv, xy in zip(levels, fractions(fig, ax, [place[lv] for lv in levels],
                                                                            [series[lv] for lv in levels]))]
        states[state] = {"lines": lines, "points": points, "colours": COLOURS[state]}
    return states


def spec_name(spec):
    return next(name for name, s in PANELS.items() if s is spec)


def main():
    rw, refs = reweighted(), references()
    profile = json.load(open(HERE / "figs_v18_6min" / "profile.json", encoding="utf-8"))
    out = {"line_pt": LINE_PT, "ref_pt": REF_PT, "reference": REFERENCE, "panels": {}}
    for name, spec in PANELS.items():
        for state in STATES:
            fig, ax, ticks, place = axes(spec)
            benzel(ax, spec, ticks, place, profile)
            drawing(fig, ax, spec)
            legend(ax, spec, state, rw, profile)
            if state == STATES[0]:
                out["panels"][name] = {"emu": spec["emu"], "states": geometry(fig, ax, spec, place, rw, refs)}
            fig.savefig(FIG / f"{name}_{state}.png", dpi=DPI)
            plt.close(fig)
    json.dump(out, open(FIG / "geometry.json", "w", encoding="utf-8"), indent=1)
    for name in PANELS:
        print(name, {s: len(v["points"]["w"]) for s, v in out["panels"][name]["states"].items()})


if __name__ == "__main__":
    main()
