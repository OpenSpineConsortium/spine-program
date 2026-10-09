# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/corpus_level_report.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""How many vertebrae of each level the corpus actually holds, split by how the label was obtained.

WHY THE SPLIT IS THE POINT. Once a corpus mixes human annotation, labels converted from a published landmark
file, labels projected from a segmented CT, and labels a model assigned to an unannotated film, a single
per-level count stops meaning anything. Twelve thousand L4 crops is a different asset depending on whether a
person drew them or a network guessed them, and the rare classes are where the difference bites: a transitional
count made mostly of pseudo-labels is a count of what a model already believed.

So every level is reported four ways:

    human        a person annotated the vertebra, or the release shipped per-vertebra landmarks
    converted    a published landmark file was converted by a stated rule, e.g. the AASCE seventeen-body
                 convention or the Mendeley caudal anchor
    from CT      the label was projected from a segmented volume into a rendered radiograph
    pseudo       a model named it on an unannotated film, at one of the supervision tiers

and the pseudo column is broken down again by tier, because an exact name and an unnamed wildcard are not the
same contribution. The supervision tiers come from tools/pseudolabel_real_films.py: exact, candidate, region,
unnamed.

WHAT THIS IS FOR. Two questions that a plain count cannot answer. Does adding twenty-seven thousand
pseudo-labelled films actually add rare-class examples, or only more of the levels that were already common?
And what fraction of any level's training signal now rests on a model's own output, which is the quantity that
decides whether a gain from the expanded corpus is real learning or a self-confirming loop.

    python tools/corpus_level_report.py --banks ~/allspine_v5_fov96_ctx ~/allspine_v3_fov96_ctx
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ORDER = (["C%d" % i for i in range(1, 8)] + ["T%d" % i for i in range(1, 13)] + ["T13"]
         + ["L%d" % i for i in range(1, 7)] + ["sacrum"])

# How each source's labels were obtained. Written out rather than guessed from the name, so a new source is
# reported as "unclassified" and visible rather than silently counted as human.
ORIGIN = {
    "csxa": "human", "CSXA": "human",
    "nhanes": "human", "nh": "human", "NHANES": "human", "nhanes_drr": "human",
    "buu_full": "converted", "BUU_FULL": "converted", "buu": "converted",
    "aasce": "converted", "AASCE": "converted", "aasce_fov96_ctx": "converted",
    "mendeley": "converted", "mendeley_drr": "converted", "mendeley_fov96_ctx": "converted",
    "vindr": "converted", "VINDR": "converted", "vindr_fov96_ctx": "converted",
    "ctsp": "from CT", "CTSP": "from CT", "verse": "from CT", "totalseg": "from CT",
    "implant": "from CT", "gl": "from CT", "ctsp_drr": "from CT", "verse_drr": "from CT",
    "physics_drr": "from CT", "physics_rare": "from CT", "obl_fov96_ctx": "from CT",
    "obl2_fov96_ctx": "from CT",
    "NHANESPS": "pseudo", "VINDRPS": "pseudo", "LAT236PS": "pseudo", "PSEUDO": "pseudo",
    "nhanesps_fov96_ctx": "pseudo", "vindrps_fov96_ctx": "pseudo", "lat236ps_fov96_ctx": "pseudo",
}


def origin_of(src, case):
    for key in (str(src), str(src).split("_")[0], str(case).split("_")[0]):
        if key in ORIGIN:
            return ORIGIN[key]
    for key, val in ORIGIN.items():
        if str(case).upper().startswith(key.upper()):
            return val
    return "unclassified"


def tier_counts_from_renders(dirs):
    """Per-level counts by supervision tier, read from the pseudo-label render directories."""
    per = defaultdict(Counter)
    flagged = 0
    films = 0
    for d in dirs:
        p = Path(os.path.expanduser(d))
        if not (p / "ann").exists():
            continue
        for f in (p / "ann").glob("*.json"):
            try:
                a = json.load(open(f))
            except Exception:  # noqa: BLE001
                continue
            films += 1
            flagged += int(bool(a.get("anomaly_flag")))
            for v in (a.get("levels") or {}).values():
                per[v["name"]]["exact"] += 1
            for v in (a.get("candidate_levels") or {}).values():
                per[(v.get("candidates") or ["?"])[0]][v.get("tier", "candidate")] += 1
            for v in (a.get("unnamed") or []):
                per[v.get("best_guess") or "?"]["unnamed"] += 1
    return per, films, flagged


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--banks", nargs="+", required=True)
    ap.add_argument("--pseudo-dirs", nargs="*",
                    default=["~/nhanes_pseudo", "~/vindr_pseudo", "~/lateral236_pseudo"])
    ap.add_argument("--out", default="~/model_night/CORPUS_LEVELS.md")
    a = ap.parse_args()

    L = ["# Levels in the corpus, by how the label was obtained\n",
         "Computed by `tools/corpus_level_report.py`. A per-level count that does not say where its labels came",
         "from cannot answer whether the corpus grew or whether a model's own output did.\n"]

    all_banks = {}
    for b in a.banks:
        bp = Path(os.path.expanduser(b))
        z = np.load(bp / f"rung_1.npz", allow_pickle=True)
        y = z["y"]
        sp = np.array([str(s) for s in z["split"]])
        case = np.array([str(c) for c in z["case"]])
        src = (np.array([str(s) for s in z["source"]]) if "source" in z.files
               else np.array(["?"] * len(y)))
        tr = sp == "train"
        per = defaultdict(Counter)
        for i in np.where(tr)[0]:
            per[ORDER[int(y[i])]][origin_of(src[i], case[i])] += 1
        all_banks[bp.name] = per
        tot = sum(sum(c.values()) for c in per.values())
        origins = Counter()
        for c in per.values():
            origins.update(c)
        L.append(f"\n## `{bp.name}` — {tot:,} training crops, {len(set(case[tr].tolist())):,} films\n")
        L.append("origins: " + ", ".join(f"{k} {v:,}" for k, v in origins.most_common()) + "\n")
        L.append("| level | human | converted | from CT | pseudo | unclassified | total |")
        L.append("|---|---:|---:|---:|---:|---:|---:|")
        for lv in ORDER:
            c = per.get(lv)
            if not c:
                continue
            t = sum(c.values())
            L.append(f"| {lv} | {c['human']:,} | {c['converted']:,} | {c['from CT']:,} | "
                     f"{c['pseudo']:,} | {c['unclassified']:,} | **{t:,}** |")
        rare = {lv: per.get(lv, Counter()) for lv in ("T13", "L6")}
        L.append("\nThe two transitional classes, which are the ones worth watching:\n")
        for lv, c in rare.items():
            t = sum(c.values())
            share = (100.0 * c["pseudo"] / t) if t else 0.0
            L.append(f"- **{lv}**: {t:,} crops, {share:.1f}% of them pseudo-labelled")

    per_tier, n_films, n_flag = tier_counts_from_renders(a.pseudo_dirs)
    if n_films:
        L.append(f"\n## Pseudo-labelled films, by supervision tier\n")
        L.append(f"{n_films:,} films labelled, {n_flag:,} flagged as candidate transitional "
                 f"({100.0 * n_flag / n_films:.1f}%).\n")
        L.append("A vertebra at the `unnamed` tier still enters training, as a wildcard. It is counted here")
        L.append("under the model's best guess purely so the row exists; no name is asserted for it.\n")
        L.append("| level | exact | candidate | region | unnamed |")
        L.append("|---|---:|---:|---:|---:|")
        for lv in ORDER:
            c = per_tier.get(lv)
            if not c:
                continue
            L.append(f"| {lv} | {c['exact']:,} | {c['candidate']:,} | {c['region']:,} | {c['unnamed']:,} |")
        tot_t = Counter()
        for c in per_tier.values():
            tot_t.update(c)
        s = sum(tot_t.values())
        L.append("\ntier shares: " + ", ".join(f"{k} {v:,} ({100.0 * v / s:.1f}%)"
                                               for k, v in tot_t.most_common()))

    out = Path(os.path.expanduser(a.out))
    out.parent.mkdir(parents=True, exist_ok=True)
    txt = "\n".join(L) + "\n"
    out.write_text(txt, encoding="utf-8")
    json.dump({b: {lv: dict(c) for lv, c in per.items()} for b, per in all_banks.items()},
              open(str(out).replace(".md", ".json"), "w"), indent=1)
    print(txt[:4000])
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
