# source-of-copy: CTSpinoPelvic1K repository working tree (public, master; head 7ddfe38 on 2026-10-08), path paper/cns2026/sweep_per_level.py; kept out of every commit by .git/info/exclude (45df97d stopped tracking the folder); copied 2026-10-08. Project folder 03_ctspinopelvic1k_dataset (spine-program); copy rules in MANIFEST_LOCAL.md
# laptop paths on lines 4 (docstring) and 23 (MIRROR): set MIRROR before running (MANIFEST_LOCAL.md section 3.6)
"""paper/cns2026/sweep_per_level.py — exact level by level WITHOUT and WITH the sweep, on the same query frames, from
the sweep_v3 records (<laptop home>/model_night/sweep_v3 mirror of ~/model_night/sweep_v3; tools/sweep_map.py).

Each spine record carries the query frames cut from its render (K = 2, 3, 4 whole bodies, no anchor in them):
`gt` (true level per body), `single_frame` (the level model alone on that frame: morphology, nothing to count from)
and `sweep_hybrid` (the same bodies named through the sweep: the frame registered onto the chain swept from the
anchor, the chain named by count and shape together). Per level, over all query bodies of all spines, the share
named exactly by each. Arms: the TotalSegmentator bench swept from the sacrum (fixed step, overlap 2 bodies) and
from C2 (overlap 1), which together cover C1 to the sacrum; the 120 held-out CTSpinoPelvic1K renders (overlap 2,
end rule) as a third. Writes figs_v2/sweep_per_level.json.

    python paper/cns2026/sweep_per_level.py [--arm name=path ...]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "figs_v2"
MIRROR = Path(r"<laptop home>\model_night\sweep_v3")
ORDER = [f"C{i}" for i in range(1, 8)] + [f"T{i}" for i in range(1, 14)] + [f"L{i}" for i in range(1, 7)] + ["sacrum"]


def tally(path, per, chain, meta):
    d = json.load(open(path))
    recs = d["records"]
    n_sp = 0
    for r in recs:
        if "queries" not in r:
            continue
        n_sp += 1
        for q in r["queries"]:
            for lvl, s1, sw, sc in zip(q["gt"], q["single_frame"], q["sweep_hybrid"], q.get("sweep_count", q["sweep_hybrid"])):
                if lvl is None:
                    continue
                per[lvl]["n"] += 1
                per[lvl]["single"] += int(s1 == lvl)
                per[lvl]["sweep"] += int(sw == lvl)
                per[lvl]["sweep_count"] += int(sc == lvl)
        for lvl, hy, ct, sg in zip(r.get("gt_names", []), r.get("hybrid_names", []), r.get("count_names", []), r.get("single_names", [])):
            if lvl is None:
                continue
            chain[lvl]["n"] += 1
            chain[lvl]["hybrid"] += int(hy == lvl)
            chain[lvl]["count"] += int(ct == lvl)
            chain[lvl]["single"] += int(sg == lvl)
    meta.append({"arm": str(path), "spines": n_sp, "config": d["summary"].get("config", {}),
                 "by_class_all": {k: v for k, v in d["summary"]["by_class"].get("all", d["summary"]["by_class"].get("unknown", {})).items()
                                  if not isinstance(v, (dict, list))}})
    return n_sp


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", action="append", default=None, help="name=path/to/sweep.json")
    a = ap.parse_args()
    arms = a.arm or [f"ts_sacrum={MIRROR / 'ts' / 'ts_ii9_o2_gt_fixed' / 'sweep.json'}",
                     f"ts_c2={MIRROR / 'ts' / 'ts_c2_ii9_o1_gt' / 'sweep.json'}",
                     f"ctsp_end={MIRROR / 'end' / 'jit_skip_open' / 'sweep.json'}"]
    per = defaultdict(lambda: {"n": 0, "single": 0, "sweep": 0, "sweep_count": 0})
    chain = defaultdict(lambda: {"n": 0, "hybrid": 0, "count": 0, "single": 0})
    meta = []
    per_arm = {}
    for spec in arms:
        name, path = spec.split("=", 1)
        if not Path(path).exists():
            print("missing", name, path); continue
        p_arm = defaultdict(lambda: {"n": 0, "single": 0, "sweep": 0, "sweep_count": 0})
        c_arm = defaultdict(lambda: {"n": 0, "hybrid": 0, "count": 0, "single": 0})
        n_sp = tally(path, p_arm, c_arm, meta)
        per_arm[name] = {"spines": n_sp,
                         "frames": {l: {"n": v["n"], "single_pct": round(100 * v["single"] / v["n"], 1), "sweep_pct": round(100 * v["sweep"] / v["n"], 1),
                                        "sweep_count_pct": round(100 * v["sweep_count"] / v["n"], 1)} for l, v in p_arm.items() if v["n"]},
                         "chain": {l: {"n": v["n"], "hybrid_pct": round(100 * v["hybrid"] / v["n"], 1), "count_pct": round(100 * v["count"] / v["n"], 1),
                                       "single_pct": round(100 * v["single"] / v["n"], 1)} for l, v in c_arm.items() if v["n"]}}
        for l, v in p_arm.items():
            for k in v: per[l][k] += v[k]
        for l, v in c_arm.items():
            for k in v: chain[l][k] += v[k]
        print(f"{name}: {n_sp} spines, query bodies {sum(v['n'] for v in p_arm.values())}, chain nodes {sum(v['n'] for v in c_arm.values())}")
    pooled = {l: {"n": per[l]["n"], "single_pct": round(100 * per[l]["single"] / per[l]["n"], 1), "sweep_pct": round(100 * per[l]["sweep"] / per[l]["n"], 1),
                  "sweep_count_pct": round(100 * per[l]["sweep_count"] / per[l]["n"], 1)} for l in ORDER if per[l]["n"]}
    pooled_chain = {l: {"n": chain[l]["n"], "hybrid_pct": round(100 * chain[l]["hybrid"] / chain[l]["n"], 1), "count_pct": round(100 * chain[l]["count"] / chain[l]["n"], 1),
                        "single_pct": round(100 * chain[l]["single"] / chain[l]["n"], 1)} for l in ORDER if chain[l]["n"]}
    out = {"order": ORDER, "arms": per_arm, "pooled_frames": pooled, "pooled_chain": pooled_chain, "meta": meta}
    json.dump(out, open(OUT / "sweep_per_level.json", "w"), indent=1)
    print(f"{'level':7s} {'n':>6s} {'frame':>7s} {'sweep':>7s} | {'chain n':>8s} {'hybrid':>7s} {'count':>7s}")
    for l in ORDER:
        f = pooled.get(l); c = pooled_chain.get(l)
        print(f"{l:7s} {f['n'] if f else 0:6d} {f['single_pct'] if f else float('nan'):7.1f} {f['sweep_pct'] if f else float('nan'):7.1f} | "
              f"{c['n'] if c else 0:8d} {c['hybrid_pct'] if c else float('nan'):7.1f} {c['count_pct'] if c else float('nan'):7.1f}")


if __name__ == "__main__":
    main()
