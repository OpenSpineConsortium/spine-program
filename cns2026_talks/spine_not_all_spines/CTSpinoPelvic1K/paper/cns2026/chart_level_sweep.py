"""paper/cns2026/chart_level_sweep.py — the per-level chart of deck v8 (chart_level_accuracy.png: exact level by level
from one exposure, the level model's checkpoint-selection split, three seeds) with the sweep added: the same levels
named through a sweep of overlapping exposures, from sweep_v3 records (tools/sweep_map.py; every spine swept from its
anchor, every vertebra in the sweep named by count and shape together = `hybrid_names` against `gt_names` per chain
node). The navy curve is drawn exactly as before. Two gold series:
  --arm   solid squares: the whole-spine sweep on the TotalSegmentator bench (522 from the sacrum + 203 from C2,
          683 spines the encoder never saw), which ran on the earlier checkpoint of the encoder (model_r18_ce_v3);
  --arm2  dashed, open squares: the same protocol on the encoder and heads the navy curve uses (v9, three seeds),
          on the render spines that encoder never saw (41: what the eval gate left of ts_drr + ctsp_drr), T10 to
          the sacrum where n per seed reaches --min-n.
Arms of one series are grouped by the token after the last '_' of their name (a head seed); the band is min-max over
seeds. Writes chart_level_sweep.png and sweep_curve.json (the caption and notes lines the deck reads).

    python paper/cns2026/chart_level_sweep.py --arm v3sac_s0=... --arm v3c2_s0=... --arm2 v9_s0=... --arm2 v9_s1=... --arm2 v9_s2=...
"""
import argparse
import glob
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
SN = HERE.parent.parent.parent / "spinesurg-ct-nnunet" / "SchwingNet"
NAVY, PALE, GOLD, GOLD_PALE, GOLD_INK, GREY, INK = "#191D63", "#C9D4EC", "#E0A800", "#FFE9A8", "#9A7300", "#8A8A8A", "#191D63"
plt.rcParams["font.family"] = "Arial"
ORDER = [f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 13)] + [f"L{i}" for i in range(1, 7)] + ["sacrum"]


def chain_per_level(path):
    d = json.load(open(path))
    per = defaultdict(lambda: [0, 0]); cases = set()
    for r in d["records"]:
        if "gt_names" not in r:
            continue
        cases.add(r["case"])
        for lvl, hy in zip(r["gt_names"], r.get("hybrid_names", [])):
            if lvl is None:
                continue
            per[lvl][0] += 1; per[lvl][1] += int(hy == lvl)
    return per, cases, d["summary"].get("config", {})


def series(specs, min_n):
    """(x indices, mean, lo, hi, {level: n per seed}, cases, cfgs, seeds) for one group of arms."""
    by_seed = defaultdict(lambda: defaultdict(lambda: [0, 0])); cases_all = set(); cfgs = {}
    for spec in specs:
        name, path = spec.split("=", 1)
        per, cases, cfg = chain_per_level(path)
        seed = name.rsplit("_", 1)[-1]
        for l, (n, k) in per.items():
            by_seed[seed][l][0] += n; by_seed[seed][l][1] += k
        cases_all |= cases
        cfgs[name] = {"spines": len(cases), "overlap": cfg.get("overlap"), "anchor": cfg.get("anchor"),
                      "model": str(cfg.get("model", "")).split("/")[-1], "end_rule": cfg.get("end_rule"), "last_link": cfg.get("last_link")}
        print(f"{name}: {len(cases)} spines, {sum(v[0] for v in per.values())} swept vertebrae")
    seeds = sorted(by_seed)
    sx, sm, slo, shi, sn = [], [], [], [], {}
    for i, l in enumerate(ORDER):
        ns = [by_seed[s][l][0] for s in seeds]
        if not ns or min(ns) < min_n:
            continue
        vals = [100 * by_seed[s][l][1] / by_seed[s][l][0] for s in seeds]
        sx.append(i); sm.append(float(np.mean(vals))); slo.append(min(vals)); shi.append(max(vals)); sn[l] = int(round(np.mean(ns)))
    return sx, sm, slo, shi, sn, cases_all, cfgs, seeds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", action="append", required=True, help="name=path/to/sweep.json, series 1 (solid)")
    ap.add_argument("--arm2", action="append", default=None, help="name=path/to/sweep.json, series 2 (dashed)")
    ap.add_argument("--min-n", type=int, default=15, help="a level is drawn when every seed swept at least this many vertebrae of it")
    ap.add_argument("--label", default="with a sweep: earlier checkpoint, 683 spines never seen")
    ap.add_argument("--label2", default="with a sweep: this model, 41 spines never seen")
    a = ap.parse_args()
    # ---- navy: exactly the v8 curve
    files = sorted(glob.glob(str(SN / "results" / "alpha_0.3_seed*" / "mixed_allspine_v9_mixed_kmax4_alpha0.3_seed*.json")))
    acc = {l: [] for l in ORDER}; nn = {}
    for f in files:
        pl = json.load(open(f))["results"][-1]["per_level"]
        for l in ORDER:
            if l in pl:
                acc[l].append(pl[l]["exact"] * 100); nn[l] = pl[l]["n"]
    xs = list(range(len(ORDER)))
    mean = [np.mean(acc[l]) for l in ORDER]; lo = [min(acc[l]) for l in ORDER]; hi = [max(acc[l]) for l in ORDER]
    # ---- gold
    S1 = series(a.arm, a.min_n)
    S2 = series(a.arm2, a.min_n) if a.arm2 else None
    g1 = {ORDER[i]: m for i, m in zip(S1[0], S1[1])}
    g2 = {ORDER[i]: m for i, m in zip(S2[0], S2[1])} if S2 else {}
    # ---- draw
    fig, ax = plt.subplots(figsize=(14.0, 5.8))
    ax.axvspan(6.5, 18.5, color="#FFF4D6", zorder=0)
    ax.text(12.5, 37, "thoracic", ha="center", fontsize=18, color=GOLD)
    ax.fill_between(xs, lo, hi, color=PALE, alpha=0.8, zorder=1)
    ax.plot(xs, mean, color=NAVY, lw=3, marker="o", ms=9, zorder=3, label="one exposure (validation split)")
    for x, m_, l in zip(xs, mean, ORDER):
        golds = [v for v in (g1.get(l), g2.get(l)) if v is not None]
        above = bool(golds) and min(golds) < m_            # a gold point under the navy one: the navy label goes above
        dx, dy = 0, (9 if above else -9)
        if l == "L6":
            dx, dy, above = -14, -4, False
        ax.annotate(f"{m_:.0f}", (x, m_), xytext=(dx, dy), textcoords="offset points", ha="center" if l != "L6" else "right",
                    va="bottom" if above else "top", fontsize=13, color=INK)
    sx, sm, slo, shi, sn, cases1, cfg1, seeds1 = S1
    ax.fill_between(sx, slo, shi, color=GOLD_PALE, alpha=0.9, zorder=2)
    ax.plot(sx, sm, color=GOLD, lw=3, marker="s", ms=8, zorder=4, label=a.label)
    for i, m_ in zip(sx, sm):
        l = ORDER[i]
        above = m_ >= mean[i]
        dy = 9 if above else -9
        if above and l in g2 and abs(g2[l] - m_) >= 1 and g2[l] >= m_:
            dy = -9; above = False                         # series 2's label takes the space above
        ax.annotate(f"{m_:.0f}", (i, m_), xytext=(0, dy), textcoords="offset points", ha="center", va="bottom" if above else "top",
                    fontsize=13, color=GOLD_INK)
    if S2:
        sx2, sm2, slo2, shi2, sn2, cases2, cfg2, seeds2 = S2
        ax.fill_between(sx2, slo2, shi2, color=GOLD_PALE, alpha=0.6, zorder=2)
        ax.plot(sx2, sm2, color=GOLD, lw=2.4, ls="--", marker="s", ms=9, mfc="white", mew=2.4, zorder=5, label=a.label2)
        for j, (i, m_) in enumerate(zip(sx2, sm2)):
            l = ORDER[i]
            if l in g1 and abs(g1[l] - m_) < 1:
                continue                                   # same number as series 1: one label is enough
            if 0 < j < len(sx2) - 1 and abs(m_ - sm2[j - 1]) < 0.5 and abs(m_ - sm2[j + 1]) < 0.5:
                continue                                   # a flat run is labelled at its ends only
            ax.annotate(f"{m_:.0f}", (i, m_), xytext=(0, 9), textcoords="offset points", ha="center", va="bottom", fontsize=13, color=GOLD_INK)
    ax.set_xticks(xs); ax.set_xticklabels([l if l != "sacrum" else "\nsacrum" for l in ORDER], fontsize=15)
    ax.set_ylim(20, 108); ax.set_ylabel("exact level, %", fontsize=19); ax.tick_params(axis="y", labelsize=15)
    ax.grid(axis="y", color="#DDDDDD"); ax.set_axisbelow(True)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=15, frameon=False, ncol=3, handlelength=2.4, columnspacing=1.8)
    ax.text(0.2, 23, f"one exposure: n per level {min(nn.values()):,}–{max(nn.values()):,} crops, three seeds (band)", fontsize=12, color=GREY)
    ax.text(0.2, 28, f"sweep, solid: {len(cases1):,} spines, n per level {min(sn.values()):,}–{max(sn.values()):,} vertebrae", fontsize=12, color=GOLD_INK)
    if S2:
        ax.text(0.2, 33, f"sweep, dashed: {len(cases2):,} spines, n per level {min(sn2.values()):,}–{max(sn2.values()):,} vertebrae per seed, "
                         f"{len(seeds2)} seeds (band)", fontsize=12, color=GOLD_INK)
    fig.tight_layout()
    fig.savefig(OUT / "chart_level_sweep.png", dpi=220, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    with Image.open(OUT / "chart_level_sweep.png") as im:
        print("chart_level_sweep.png", im.size)
    # ---- what the deck reads
    lv1 = "; ".join(f"{ORDER[i]} {m_:.0f} % ({sn[ORDER[i]]:,})" for i, m_ in zip(sx, sm))
    models1 = sorted({c["model"] for c in cfg1.values()})
    out = {"series1": {"n_spines": len(cases1), "arms": cfg1, "seeds": seeds1, "models": models1,
                       "per_level": {ORDER[i]: {"mean_pct": round(m_, 1), "lo": round(l_, 1), "hi": round(h_, 1), "n": sn[ORDER[i]]}
                                     for i, m_, l_, h_ in zip(sx, sm, slo, shi)}},
           "caption": (f"Gold, solid: the same levels read through a sweep of overlapping exposures, simulated from {len(cases1):,} CT renders the "
                       f"encoder never saw (TotalSegmentator bench, an earlier checkpoint): a proprietary algorithm reconstructs the spine "
                       f"from the overlap."),
           "notes": (f"Gold, solid: the sweep on the earlier checkpoint of the encoder ({', '.join(models1)}), {len(cases1):,} TotalSegmentator "
                     f"renders it never saw: 522 swept from the sacrum at overlap 2 and 203 from C2 at overlap 1 (fixed step; 41 spines are in "
                     f"both), every vertebra in the sweep scored exact. Per level (n vertebrae): {lv1}. Levels with fewer than {a.min_n} swept "
                     f"vertebrae are not drawn. Source: ~/model_night/sweep_v3/ts/ts_ii9_o2_gt_fixed and ts_c2_ii9_o1_gt.")}
    if S2:
        lv2 = "; ".join(f"{ORDER[i]} {m_:.0f} % ({sn2[ORDER[i]]:,})" for i, m_ in zip(sx2, sm2))
        models2 = sorted({c["model"] for c in cfg2.values()})
        out["series2"] = {"n_spines": len(cases2), "arms": cfg2, "seeds": seeds2, "models": models2,
                          "per_level": {ORDER[i]: {"mean_pct": round(m_, 1), "lo": round(l_, 1), "hi": round(h_, 1), "n": sn2[ORDER[i]]}
                                        for i, m_, l_, h_ in zip(sx2, sm2, slo2, shi2)}}
        out["caption"] += (f" Dashed: the model behind the navy curve on the {len(cases2):,} render spines it never saw, T10 to the sacrum. "
                           f"Real C-arm testing is lumbar; thoracic naming on a real C-arm is not yet tested.")
        out["notes"] += (f" Gold, dashed: the same protocol on the encoder and the three heads the navy curve uses (v9, {', '.join(models2)}), "
                         f"on every render spine that encoder never saw ({len(cases2):,}: 40 TotalSegmentator and 1 CTSpinoPelvic1K; the "
                         f"eval gate found the other 1,100 TS, 801 CTSP and 387 VerSe renders in its training or selection keys), swept from "
                         f"the sacrum at overlap 2 with the end rule (skip, open); every chain complete, every swept vertebra exact on all three "
                         f"seeds; the frame alone on the same spines 69 %. Per level (n vertebrae per seed): {lv2}; above T10 fewer than "
                         f"{a.min_n} per seed, not drawn. Source: ~/model_night/sweep_v3/cns/sac_o2_s0..2 (job 40454032, 2026-09-25).")
    else:
        out["caption"] += " Real C-arm testing is lumbar; thoracic naming on a real C-arm is not yet tested."
    json.dump(out, open(OUT / "sweep_curve.json", "w"), indent=1)
    print("series 1:", len(cases1), "spines;", lv1)
    if S2:
        print("series 2:", len(cases2), "spines;", lv2)


if __name__ == "__main__":
    main()
