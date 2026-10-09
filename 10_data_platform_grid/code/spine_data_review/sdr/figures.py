"""Figures drawn from analysis/*.json only: PRISMA flow, forest plots, year histogram, access by modality, quality.

WHY FIGURES READ JSON AND NOTHING ELSE. Every number in the manuscript traces to a file
(PROTOCOL.md section 13), and a figure is a number drawn. So this module never touches a charting
record, a CSV or the network: it reads the analysis JSONs that sdr/stats.py wrote, draws them, and
writes the SHA-1 of the JSON it read into the PDF's metadata (Subject field), so a reviewer can
check that a figure and a table came from the same state of the analysis. A figure whose input is
absent is skipped with a message, never drawn from a default. The PDF carries no CreationDate or
ModDate (matplotlib stamps both from the wall clock unless told not to), so two runs on the same
JSON are byte-identical; `--selftest` renders one figure twice and compares the bytes.

Style, fixed by the SAP's presentation rules: sans-serif, a light grid on both axes, colour-blind
safe hues (Okabe-Ito) assigned in a fixed order per category so that a route or a modality keeps
its colour across figures, thin marks with a surface gap, a legend whenever there are two or more
series, no dual axes, and no caption text inside the figure (captions live in the manuscript, at
most 60 words). Figures 3 and 4 of the SAP (route by year band; quality histogram and scatter) are
drawn when their inputs exist, in addition to the four the task names.

Inputs (all under analysis/, written by sdr/stats.py; there is no fallback to prisma_counts.json,
which has a different shape): flow.json, pooled_variants.json, descriptives.json, availability.json,
quality_analysis.json.
Outputs: figures/fig1_prisma_flow.pdf, fig2_datasets_per_year.pdf, fig3_access_by_modality.pdf,
fig4_quality.pdf, fig5_forest_<variant>.pdf (one per variant with at least one row), plus a PNG twin
of each for quick viewing; the invocation is appended to <run-dir>/run_meta.json. Under --limit the
forest rows are truncated and the panel says so; the diamonds are still pooled over every eligible row.
CLI: python -m sdr.figures --run-dir R --run-date D [--analysis-dir analysis] [--figures-dir figures]
[--only prisma,forest,year,access,quality] [--limit N] [--dry-run] [--selftest]
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Polygon  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

from sdr.common import add_common_args, init_run_dir, review_root  # noqa: E402

# Okabe-Ito, colour-blind safe; hues are assigned to a category by fixed order, never cycled by rank.
OI = {"orange": "#E69F00", "sky": "#56B4E9", "green": "#009E73", "yellow": "#F0E442", "blue": "#0072B2",
      "vermilion": "#D55E00", "purple": "#CC79A7", "black": "#000000", "grey": "#7F7F7F"}
ROUTE_ORDER = ["open-download", "registration", "data-use-agreement", "request-to-authors", "unavailable", "commercial"]
ROUTE_COLOUR = dict(zip(ROUTE_ORDER, [OI["green"], OI["sky"], OI["blue"], OI["orange"], OI["vermilion"], OI["purple"]]))
MODALITY_ORDER = ["CT", "CBCT", "radiograph", "fluoroscopy", "DXA-VFA", "EOS", "MRI", "other"]
MODALITY_COLOUR = dict(zip(MODALITY_ORDER, [OI["blue"], OI["sky"], OI["orange"], OI["vermilion"], OI["purple"], OI["yellow"], OI["grey"], OI["black"]]))
SURFACE = "white"


def _style() -> None:
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"], "font.size": 8,
                         "axes.grid": True, "grid.color": "#D9D9D9", "grid.linewidth": 0.5, "axes.axisbelow": True,
                         "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#4D4D4D", "axes.linewidth": 0.6,
                         "legend.frameon": False, "legend.fontsize": 7, "pdf.fonttype": 42, "figure.dpi": 150})


def _load(adir: Path, name: str) -> tuple[dict | None, str | None]:
    """The analysis JSON's `value` and the SHA-1 of the file it was read from; (None, None) when absent."""
    p = adir / name
    if not p.exists():
        return None, None
    raw = p.read_bytes()
    return json.loads(raw.decode("utf-8")).get("value"), hashlib.sha1(raw).hexdigest()


def _meta(stem: str, sha: str, source: str) -> dict:
    """PDF metadata: the source JSON's sha1 in Subject; CreationDate and ModDate None so matplotlib
    (>= 3.3) omits them and the file carries no wall-clock value (determinism rule)."""
    return {"Subject": f"drawn from analysis/{source} sha1 {sha}", "Creator": "sdr/figures.py", "Title": stem,
            "CreationDate": None, "ModDate": None}


def _save(fig, out: Path, sha: str, source: str) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, metadata=_meta(out.stem, sha, source))
    fig.savefig(out.with_suffix(".png"), dpi=200)
    plt.close(fig)


# ----------------------------------------------------------------------------- Figure 1: PRISMA flow
def _box(ax, x, y, w, h, text, fill="#F2F2F2") -> None:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.15", facecolor=fill, edgecolor="#4D4D4D", linewidth=0.7))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=6.6, linespacing=1.25)


def _arrow(ax, x0, y0, x1, y1) -> None:
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops={"arrowstyle": "-|>", "color": "#4D4D4D", "lw": 0.7, "shrinkA": 0, "shrinkB": 0})


def _n(v) -> str:
    return "n = ?" if v is None else f"n = {v:,}"


def _legend(ax, **kw) -> None:
    """A legend only when something was drawn with a label (matplotlib warns and draws an empty box otherwise)."""
    if ax.get_legend_handles_labels()[0]:
        ax.legend(**kw)


def _codes(d: dict, top: int = 6) -> str:
    items = sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))[:top]
    return "\n".join(f"  {k}: {v:,}" for k, v in items) + ("\n  …" if len(d) > top else "")


def prisma(v: dict, sha: str, out: Path) -> None:
    """PRISMA 2020 two-arm flow: search arm on the left (identification, screening, included) and the
    other-methods arm on the right, every count read from flow.json; a missing count prints '?'."""
    fig, ax = plt.subplots(figsize=(7.2, 8.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.grid(False)
    for y0, y1, lab in ((82, 100, "Identification"), (34, 81, "Screening"), (0, 33, "Included")):
        ax.add_patch(FancyBboxPatch((0, y0), 5, y1 - y0, boxstyle="square,pad=0", facecolor="#E8EEF4", edgecolor="none"))
        ax.text(2.5, (y0 + y1) / 2, lab, rotation=90, ha="center", va="center", fontsize=7)
    sa, oa = v["search_arm"], v["other_arm"]
    p, dsc = sa["prescreen"], v["datasets"]
    v = {**sa, "per_source": v["per_source"]}
    ranked = sorted(v["per_source"].items(), key=lambda kv: (-(kv[1]["n_identified"] or 0), kv[0]))
    src = [f"{s} {r['n_identified'] if r['n_identified'] is not None else '?'}" for s, r in ranked[:5]]
    if len(ranked) > 5:
        src.append(f"{len(ranked) - 5} more sources")
    src_lines = "; ".join(src[:3]) + ("\n" + "; ".join(src[3:]) if src[3:] else "")
    _box(ax, 8, 84, 40, 15, f"Records identified from {len(v['per_source'])} sources\n{_n(v['identified'])}\n"
         f"after merge {_n(v['after_merge'])}\n\nlargest: {src_lines}")
    _box(ax, 52, 84, 22, 15, f"Removed before screening\nduplicates at merge\n{_n(v['duplicates_removed'])}\nprescreen fail {_n(p['fail_total'])}"
         f"\n(audit: {v['audit']['sampled']} sampled,\n{v['audit']['included']} included)")
    _arrow(ax, 48, 91.5, 52, 91.5)
    _box(ax, 77, 84, 22, 15, f"Other methods\nknown items {_n(oa['known_items'])}\nbackward chasing {_n(oa['chase_backward'])}\n"
         f"forward chasing {_n(oa['chase_forward'])}\nmanual {_n(oa['chase_manual'])}", "#FFF4E5")
    _box(ax, 8, 66, 40, 12, f"Records screened (title/abstract)\n{_n(v['screened'])}")
    _arrow(ax, 28, 84, 28, 78)
    _box(ax, 52, 63, 22, 15, f"Excluded {_n(sum(v['screen_excluded_by_code'].values()))}\n{_codes(v['screen_excluded_by_code'])}\n  use-only: {v['use_only']:,}")
    _arrow(ax, 48, 72, 52, 72)
    _box(ax, 8, 48, 40, 10, f"Sought for full text / description\n{_n(v['sought_for_full_text'])}")
    _arrow(ax, 28, 66, 28, 58)
    _box(ax, 52, 48, 22, 10, f"Not retrieved\n(charted from abstract)\n{_n(v['not_retrieved'])}")
    _arrow(ax, 48, 53, 52, 53)
    _box(ax, 8, 36, 40, 8, f"Assessed at description review\n{_n(v['sought_for_full_text'])}")
    _arrow(ax, 28, 48, 28, 44)
    _box(ax, 52, 35, 22, 10, f"Excluded {_n(sum(v['full_text_excluded_by_code'].values()))}\n{_codes(v['full_text_excluded_by_code'])}")
    _arrow(ax, 48, 40, 52, 40)
    _box(ax, 77, 66, 22, 12, f"Screened (other arm)\n{_n(oa['screened'])}\nexcluded {_n(oa.get('excluded'))}", "#FFF4E5")
    _arrow(ax, 88, 84, 88, 78)
    _box(ax, 77, 48, 22, 10, f"Included records\n(other arm)\n{_n(oa['included_records'])}", "#FFF4E5")
    _arrow(ax, 88, 66, 88, 58)
    _box(ax, 8, 20, 40, 9, f"Included records (search arm)\n{_n(v['included_records_search'])}")
    _arrow(ax, 28, 36, 28, 29)
    _arrow(ax, 88, 48, 88, 24.5)
    _arrow(ax, 88, 24.5, 48, 24.5)
    _box(ax, 8, 4, 91, 11, f"Datasets after record-to-dataset mapping  {_n(dsc['total'])}\n"
         f"primary {dsc['non_derived_non_figure']}   derived {dsc['derived']}   figure-derived {dsc['figure_derived']}"
         f"   use-only records per dataset: median {dsc['n_use_records_per_dataset']['median']}", "#E5F3EE")
    _arrow(ax, 28, 20, 28, 15)
    _save(fig, out, sha, "flow.json")


# ----------------------------------------------------------------------------- Figure 5: forest plots
def _diamond(ax, y: float, pr: dict, name: str) -> None:
    lo, hi, p = pr["ci_low"], pr["ci_high"], pr["estimate"]
    ax.add_patch(Polygon([[lo, y], [p, y + 0.3], [hi, y], [p, y - 0.3]], closed=True, facecolor=OI["green"] if name == "unselected" else OI["orange"], edgecolor="none"))
    if pr["pi_low"] is not None:
        ax.plot([pr["pi_low"], pr["pi_high"]], [y, y], ls="--", color="#4D4D4D", lw=0.8)


def forest(v: dict, sha: str, fdir: Path, limit: int | None) -> list[Path]:
    """One panel per variant: rows sorted by year, squares scaled by n, exact intervals; each stratum's
    diamond (illustrative pooled estimate, k >= 5, dashed prediction interval) sits directly under its
    own rows, the enriched stratum below a title; tau2 and I2 in the footer. Under --limit the rows are
    truncated and the footer says so. Variants with no row are skipped."""
    outs = []
    for var in ("L6", "T13", "LSTV"):
        allrows = list(v.get(var, {}).get("per_dataset", []))
        rows = allrows[: limit or None]
        if not rows:
            print(f"  forest {var}: no per-dataset row; skipped")
            continue
        main = sorted([r for r in rows if not r["enriched"]], key=lambda r: (r["year"], r["id"]))
        enr = sorted([r for r in rows if r["enriched"]], key=lambda r: (r["year"], r["id"]))
        pooled = {"unselected": v[var]["pooled"], "enriched": v[var]["enriched"]["pooled"]}
        n_rows = len(main) + len(enr) + sum(1 for pr in pooled.values() if pr) + (1 if enr else 0)
        fig, ax = plt.subplots(figsize=(6.4, 0.28 * n_rows + 1.4))
        nmax = max(r["n"] for r in rows)
        y, labels = 0, []
        for block, name, title in ((main, "unselected", None), (enr, "enriched", "Enriched for the variant (own stratum)")):
            if title and block:
                y += 1
                labels.append((y, title, True))
            for r in block:
                y += 1
                size = 3 + 9 * (r["n"] / nmax) ** 0.5
                ax.plot([r["ci_low"], r["ci_high"]], [y, y], color="#4D4D4D", lw=1)
                ax.plot(r["p"], y, marker="s", ms=size, color=OI["blue"] if not r["enriched"] else OI["orange"], mec=SURFACE, mew=0.6)
                labels.append((y, f"{r['id']} ({r['year']})  {r['x']}/{r['n']}" + ("" if r["poolable"] or r["enriched"] else " †"), False))
            if pooled[name]:                      # the diamond of this stratum, under this stratum's rows
                y += 1
                _diamond(ax, y, pooled[name], name)
                labels.append((y, f"Pooled ({name}, DL, k = {pooled[name]['k']}) — illustrative", True))
        ax.set_yticks([yy for yy, _, _ in labels])
        ax.set_yticklabels([t for _, t, _ in labels], fontsize=6.5)
        for tick, (_, _, bold) in zip(ax.get_yticklabels(), labels):
            tick.set_fontweight("bold" if bold else "normal")
        ax.invert_yaxis()
        ax.set_xlim(0, 1)
        ax.set_xlabel(f"Prevalence of {var} per subject (exact 95 % interval)")
        foot = "; ".join(f"{name}: τ² = {pr['tau2']:.3f}, I² = {100 * pr['I2']:.0f} %" for name, pr in pooled.items() if pr) or "pooling not done (k < 5)"
        foot += "   † not eligible for pooling" if any("†" in t for _, t, _ in labels) else ""
        foot += f"   rows truncated to {len(rows)} of {len(allrows)} (--limit); diamonds pooled over all eligible rows" if len(rows) < len(allrows) else ""
        ax.text(0, 1.01, foot, transform=ax.transAxes, fontsize=6.5, va="bottom")
        fig.tight_layout()
        out = fdir / f"fig5_forest_{var}.pdf"
        _save(fig, out, sha, "pooled_variants.json")
        outs.append(out)
    return outs


# ----------------------------------------------------------------------------- Figure 2: years
def years(v: dict, sha: str, out: Path) -> None:
    """Datasets per year stacked by modality (a dataset counts once per modality) and cumulative reported
    subjects by modality class; two panels, one x axis, no second y axis."""
    ym, cum = v["year_x_modality"], v.get("cumulative_subjects_by_year_modality", {})
    yrs = list(range(2000, 2027))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 4.6), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
    bottom = [0] * len(yrs)
    for m in MODALITY_ORDER:
        vals = [ym.get(str(y), {}).get(m, 0) for y in yrs]
        if sum(vals) == 0:
            continue
        a1.bar(yrs, vals, bottom=bottom, color=MODALITY_COLOUR[m], edgecolor=SURFACE, linewidth=0.6, width=0.8, label=m)
        bottom = [b + x for b, x in zip(bottom, vals)]
    a1.set_ylabel("Datasets (one per modality carried)")
    a1.yaxis.set_major_locator(MaxNLocator(integer=True))
    _legend(a1, ncol=4, loc="upper left")
    for m, col in (("CT", OI["blue"]), ("radiography", OI["orange"])):
        if m in cum:
            a2.step(yrs, [cum[m].get(str(y), 0) for y in yrs], where="post", color=col, lw=2, label=m)
    a2.set_ylabel("Cumulative reported subjects")
    a2.set_xlabel("Year of the record describing the image release")
    _legend(a2, loc="upper left")
    a2.set_xticks(yrs[::2])
    fig.tight_layout()
    _save(fig, out, sha, "descriptives.json")


# ----------------------------------------------------------------------------- Figure 3: access
def access(v: dict, sha: str, out: Path) -> None:
    """Access route by modality (left, stacked) and by year band (right), route colours fixed."""
    rm, rb = v["route_x_modality"], v.get("route_x_year_band", {})
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.0), gridspec_kw={"width_ratios": [1.4, 1]})
    for ax, table, order, xlabel in ((a1, rm, [m for m in MODALITY_ORDER if m in rm], "Modality (a dataset counts once per modality)"),
                                     (a2, rb, sorted(rb), "Year band")):
        bottom = [0] * len(order)
        for r in ROUTE_ORDER:
            vals = [table.get(k, {}).get(r, 0) for k in order]
            if sum(vals) == 0:
                continue
            ax.bar(order, vals, bottom=bottom, color=ROUTE_COLOUR[r], edgecolor=SURFACE, linewidth=0.6, width=0.7, label=r)
            bottom = [b + x for b, x in zip(bottom, vals)]
        ax.set_xlabel(xlabel)
        ax.tick_params(axis="x", labelrotation=30)
    a1.set_ylabel("Datasets")
    a1.yaxis.set_major_locator(MaxNLocator(integer=True))
    a2.yaxis.set_major_locator(MaxNLocator(integer=True))
    _legend(a1, loc="upper right")
    fig.tight_layout()
    _save(fig, out, sha, "availability.json")


# ----------------------------------------------------------------------------- Figure 4: quality
def quality(v: dict, sha: str, out: Path) -> None:
    """(a) histogram of the rubric total by access route; (b) total against year with a lowess line."""
    from statsmodels.nonparametric.smoothers_lowess import lowess
    sc = v.get("scatter", [])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.8, 3.0))
    bins = list(range(0, 22))
    data = [[r["total"] for r in sc if r["route"] == rt] for rt in ROUTE_ORDER]
    present = [i for i, d in enumerate(data) if d]
    if present:
        a1.hist([data[i] for i in present], bins=bins, stacked=True, color=[ROUTE_COLOUR[ROUTE_ORDER[i]] for i in present],
                label=[ROUTE_ORDER[i] for i in present], edgecolor=SURFACE, linewidth=0.6)
    a1.set_xlabel("Rubric total (0-20)")
    a1.set_ylabel("Datasets")
    a1.yaxis.set_major_locator(MaxNLocator(integer=True))
    _legend(a1, loc="upper left")
    for ann, col, lab in ((True, OI["blue"], "annotated"), (False, OI["grey"], "unannotated")):
        pts = [r for r in sc if r["annotated"] == ann]
        if pts:
            a2.scatter([r["year"] for r in pts], [r["total"] for r in pts], s=18, color=col, edgecolor=SURFACE, linewidth=0.5, label=lab)
    if len(sc) >= 4:
        sm = lowess([r["total"] for r in sc], [r["year"] for r in sc], frac=2 / 3, it=3)
        a2.plot(sm[:, 0], sm[:, 1], color=OI["vermilion"], lw=1.5, label="lowess")
    a2.set_xlabel("Year")
    a2.set_ylabel("Rubric total")
    a2.set_ylim(-0.5, 20.5)
    a2.xaxis.set_major_locator(MaxNLocator(integer=True))      # years, never 2012.5
    _legend(a2, loc="lower right")
    fig.tight_layout()
    _save(fig, out, sha, "quality_analysis.json")


def _selftest() -> int:
    """Render one small figure twice into memory with _meta and compare the PDF bytes: the determinism
    rule holds only if matplotlib writes no CreationDate/ModDate."""
    _style()
    bufs = []
    for _ in range(2):
        fig, ax = plt.subplots(figsize=(2, 1.5))
        ax.bar(["a", "b"], [1, 2], label="x")
        _legend(ax)
        buf = io.BytesIO()
        fig.savefig(buf, format="pdf", metadata=_meta("selftest", "0" * 40, "none"))
        plt.close(fig)
        bufs.append(buf.getvalue())
    same, dated = bufs[0] == bufs[1], b"/CreationDate" in bufs[0] or b"/ModDate" in bufs[0]
    print("figures selftest (two renders byte-identical, no CreationDate/ModDate):", "ok" if same and not dated else f"FAIL identical={same} dated={dated}")
    return 0 if same and not dated else 1


# ----------------------------------------------------------------------------- CLI
def main(argv: list[str] | None = None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.figures", description=__doc__.split("\n")[0]))
    ap.add_argument("--analysis-dir", default="analysis")
    ap.add_argument("--figures-dir", default="figures")
    ap.add_argument("--only", default="prisma,year,access,quality,forest", help="comma list of figures to draw")
    ap.add_argument("--selftest", action="store_true", help="render twice in memory and compare bytes; nothing written")
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    _style()
    root = review_root()
    adir, fdir = root / a.analysis_dir, root / a.figures_dir
    jobs = {"prisma": ("flow.json", lambda v, s: prisma(v, s, fdir / "fig1_prisma_flow.pdf")),
            "year": ("descriptives.json", lambda v, s: years(v, s, fdir / "fig2_datasets_per_year.pdf")),
            "access": ("availability.json", lambda v, s: access(v, s, fdir / "fig3_access_by_modality.pdf")),
            "quality": ("quality_analysis.json", lambda v, s: quality(v, s, fdir / "fig4_quality.pdf")),
            "forest": ("pooled_variants.json", lambda v, s: forest(v, s, fdir, a.limit))}
    names = [n.strip() for n in a.only.split(",") if n.strip()]
    bad = [n for n in names if n not in jobs]
    if bad:
        print(f"--only: unknown figure(s) {', '.join(bad)}; valid names: {', '.join(jobs)}")
        return 2
    if not a.dry_run:
        init_run_dir(a.run_dir, a.run_date, argv)
    rc = 0
    for name in names:
        src, fn = jobs[name]
        v, sha = _load(adir, src)
        if a.dry_run:
            print(f"{name:8s} <- analysis/{src} {'present' if v is not None else 'ABSENT'} -> {fdir}")
            continue
        if v is None:
            print(f"{name:8s} skipped: analysis/{src} absent (written by sdr.stats)")
            rc = 1
            continue
        fn(v, sha)
        print(f"{name:8s} drawn from analysis/{src} (sha1 {sha[:12]}) -> {fdir}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
