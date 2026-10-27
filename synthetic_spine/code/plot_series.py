"""Draw every published series, one panel per measure, levels top to bottom as in the spine.

    python3 code/plot_series.py          # from synthetic_spine/; needs matplotlib

Writes figures/series_by_level.png and .pdf. One line per series through its own per-level means, a series drawn
only where it reports two or more levels; a series that reports one level is a marker. Panjabi's twelve cadaveric
spines are black and drawn last; every other series in a panel takes a colour and a dash from a fixed table, assigned
in sorted order within the panel, so no two curves of one panel look alike, and each legend sits beside its panel.
The style follows the dataset article's Figure 6 code, which drew these same series before it was cut back to
Panjabi alone.

Dispersion is not drawn. The series report SD, SEM, a pooled meta-analytic SE, a median, or nothing, and these cannot
be drawn alike (an SEM bar over twelve specimens is about 3.5 times narrower than the SD of the same data). The tables
carry each row's dispersion and its type; README.md says how to convert.
"""
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
OUT = HERE / "figures"

VERTEBRAE = ["T11", "T12", "L1", "L2", "L3", "L4", "L5"]
MEASURES = [  # (measure in the tables, title, levels)
    ("h_ant", "Anterior body height (VBHa)", VERTEBRAE),
    ("h_post", "Posterior body height (VBHp)", VERTEBRAE),
    ("endplate", "Upper end-plate width (EPWu)", VERTEBRAE),
    ("canal_w", "Canal width, interpedicular (SCW)", VERTEBRAE),
    ("canal_ap", "Canal depth, midsagittal (SCD)", VERTEBRAE),
    ("pedicle", "Transverse pedicle width (PDW)", VERTEBRAE),
    ("disc", "Disc height", ["T12L1", "L1L2", "L2L3", "L3L4", "L4L5", "L5S1"]),
]
DASHES = [(0, ()), (0, (4.0, 1.4)), (0, (2.4, 1.2)), (0, (1.2, 1.2)), (0, (5.0, 1.2, 1.0, 1.2)), (0, (1.0, 1.8))]
PALETTE = ["#0072B2", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#E69F00", "#7A5195", "#4D7C3A"]
NOTE = ("Published per-level means, every series in data/.",
        "Dispersion is not drawn: the series report SD, SEM,",
        "pooled SE, medians or nothing (see README.md).",
        "A sex-stratified series is one curve per sex.",
        "Labels: first author and year of the paper as",
        "resolved in sources.json.")


def rows_of(name):
    lines = [l for l in (DATA / name).read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    return list(csv.DictReader(lines))


def labels():
    """Series label = the paper's first author and year as resolved, so a misattributed table name is not repeated."""
    papers = json.loads((HERE / "sources.json").read_text(encoding="ascii"))["papers"]
    mapping = list(csv.DictReader((DATA / "series_papers.csv").read_text(encoding="ascii").splitlines()))
    out = {}
    for m in mapping:
        p = papers[m["paper"]]
        first = ((p.get("pubmed") or {}).get("first_author") or (p.get("crossref") or {}).get("first_author") or m["series"]).split(" ")
        surname = " ".join(w for w in first if not (w.isupper() and len(w) <= 3)) or m["series"]
        year = (p.get("crossref") or {}).get("year") or str((p.get("pubmed") or {}).get("pubdate", ""))[:4]
        label = f"{surname} {year}".strip()
        if m["paper"].startswith("panjabi"):
            label = "Panjabi 1991/1992 (n = 12, cadaveric)"
        out[(m["file"], m["series"], m["citation_contains"])] = label
    return out


def collect():
    """{measure: {curve name: {level: mean}}} from both tables; a sex-stratified series is one curve per sex."""
    lab = labels()
    series = {}
    for name in ("level_references.csv", "pedicle_width_references.csv"):
        for r in rows_of(name):
            key = next(k for k in lab if k[0] == name and k[1] == r["series"] and (not k[2] or k[2] in r["citation"]))
            measure = "pedicle" if r["measure"] in ("PDW", "pedicle") else r["measure"]
            sex = r.get("sex") or "all"
            curve = lab[key] if sex in ("all", "") else f"{lab[key]} ({sex})"
            series.setdefault(measure, {}).setdefault(curve, {})[r["level"]] = float(r["mean"])
    return series


def styles(names):
    out, i = {}, 0
    for n in sorted(names):
        if n.startswith("Panjabi"):
            out[n] = ("#000000", DASHES[0], 1.6)
            continue
        out[n] = (PALETTE[i % len(PALETTE)], DASHES[(i // len(PALETTE)) % len(DASHES)], 0.9)
        i += 1
    assert len({(c, d) for c, d, _ in out.values()}) == len(out), "two curves of one panel would look alike"
    return out


def main():
    data = collect()
    fig, axes = plt.subplots(4, 2, figsize=(15, 22), constrained_layout=True)
    for ax, (measure, title, levels) in zip(axes.flat, MEASURES):
        y = {l: -i for i, l in enumerate(levels)}
        curves = data.get(measure, {})
        style = styles(set(curves))
        for name in sorted(curves, key=lambda n: n.startswith("Panjabi")):
            per = curves[name]
            lv = [l for l in levels if l in per]
            colour, dash, lw = style[name]
            if len(lv) >= 2:
                ax.plot([per[l] for l in lv], [y[l] for l in lv], color=colour, ls=dash, lw=lw, label=name,
                        solid_capstyle="round", zorder=3 if name.startswith("Panjabi") else 2)
            elif lv:
                ax.plot([per[lv[0]]], [y[lv[0]]], marker="o", ms=4, color=colour, ls="none", label=name)
        ax.set_yticks([y[l] for l in levels], levels)
        ax.set_title(f"{title}: {len(curves)} curves", fontsize=11, loc="left")
        ax.set_xlabel("mm")
        ax.grid(axis="x", color="#dddddd", lw=0.5)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.legend(fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    axes.flat[-1].axis("off")
    axes.flat[-1].text(0, 0.95, "\n".join(NOTE), va="top", fontsize=10)
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "series_by_level.png", dpi=110)
    fig.savefig(OUT / "series_by_level.pdf", metadata={"CreationDate": None})
    print(f"figures/series_by_level.png and .pdf: {sum(len(d) for d in data.values())} curves over {len(data)} measures")


if __name__ == "__main__":
    main()
