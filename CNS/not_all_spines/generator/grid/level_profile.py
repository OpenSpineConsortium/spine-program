"""The gold tier 3 and 4 vertebral body profile by level, for the Benzel slide of the CNS deck (Greg, 2026-10-31).

Greg's ask: the slide after Benzel shows Benzel's own plot of vertebral body width and depth by level, with a
second line from his gold tier 3 and 4 CTs, T13 and L6 included, with the standard deviation, the legend
saying how many full spines it comes from. This runs on the grid inside grid/cns_level_profile.sh and writes
aggregates only; no study id or person key leaves the grid.

links    one link per gold tier 4 person to its TotalSegmentator map, from records.jsonl: segmented, not held
         out, and concordant with the census's SPINEPS mask (the name of every bone agreed, so no level slid);
         a person's first CT by id. TotalSegmentator names no T13 or L6, so those come from gold tier 3 alone.
profile  per measure and level the n, mean, SD and percentiles over gold tier 3 (one study a person, the
         persons of the covariates join, SchwingNet job 40902924) and gold tier 4 (the rows of the links),
         and how many spines show a T13 or an L6.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
import sys

KEYS = ("endplate", "endplate_depth", "endplate_lower", "endplate_lower_depth", "body_w_mid", "body_d_mid",
        "canal_w", "canal_ap", "canal_ap_min", "interpedicular", "interpedicular_max")
RESOLUTION = ((1.25, "slices to 1.25 mm"), (2.5, "slices to 2.5 mm"), (float("inf"), "slices over 2.5 mm"))
GOLD3_ROWS = {"autopet": "enhance/rows.csv", "enhance_pet": "enhance/rows.csv",
              "verse": "verse/rows.csv", "totalseg": "verse/totalseg/rows.csv"}
EXTRA = ("T13", "L6")


def links(records: str, labels_root: str, masks: str) -> None:
    """Link each chosen gold tier 4 map into MASKS; print the counts."""
    os.makedirs(masks, exist_ok=True)
    seen, counts = set(), {"records": 0, "chosen": 0}
    rows = [json.loads(line) for line in open(records, encoding="utf-8") if line.strip()]
    rows.sort(key=lambda r: r.get("id", ""))
    for row in rows:
        counts["records"] += 1
        reason = None
        if row.get("status") != "segmented":
            reason = "not segmented"
        elif row.get("held_out"):
            reason = "held out"
        elif row.get("kind") != "concordant":
            reason = "kind " + str(row.get("kind"))
        elif row.get("person_key") in seen:
            reason = "a second CT of a person"
        if reason:
            counts[reason] = counts.get(reason, 0) + 1
            continue
        seen.add(row.get("person_key"))
        target = os.path.join(labels_root, row["labels"])
        link = os.path.join(masks, row["id"] + ".nii.gz")
        if not os.path.lexists(link):
            os.symlink(target, link)
        counts["chosen"] += 1
    print(json.dumps(counts, sort_keys=True))


def number(text):
    try:
        value = float(text)
    except (TypeError, ValueError):
        return None
    return value if math.isfinite(value) else None


def read_rows(path: str, studies, source: str, values: dict, spines: dict, member: str = "", strata: dict = None,
              coarsest: dict = None, flags: dict = None) -> None:
    """Every chosen study's readings of KEYS by level into VALUES, and the levels it shows into SPINES; with STRATA,
    each reading again under its member and its study, and each study's coarsest spacing into COARSEST."""
    with open(path, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            study = row["study"]
            if studies is not None and study not in studies:
                continue
            level = row["level"]
            if level == "study":
                if coarsest is not None and row["key"] == "coarsest_mm" and number(row["value"]) is not None:
                    coarsest[(path, study)] = number(row["value"])
                continue
            spine = spines.setdefault((source, path, study), set())
            spine.add(level)
            if flags is not None and row["key"].startswith("flag:"):
                flags.setdefault((path, study, level), set()).add(row["key"][5:])
            if row["key"] in KEYS:
                value = number(row["value"])
                if value is not None:
                    values.setdefault((row["key"], level), []).append((source, value))
                    if strata is not None:
                        strata.setdefault((row["key"], level), []).append((member, path, study, value))


def quantile(ordered, share):
    position = share * (len(ordered) - 1)
    low = math.floor(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def summary(pairs):
    ordered = sorted(v for _, v in pairs)
    n = len(ordered)
    out = {"n": n, "n_gold3": sum(1 for s, _ in pairs if s == "gold3"),
           "n_gold4": sum(1 for s, _ in pairs if s == "gold4")}
    if n:
        median = statistics.median(ordered)
        mad = statistics.median(abs(v - median) for v in ordered)
        kept = [v for v in ordered if mad == 0 or abs(v - median) <= 5 * 1.4826 * mad]
        out.update(mean=statistics.fmean(ordered), sd=statistics.stdev(ordered) if n > 1 else None,
                   median=median, q05=quantile(ordered, 0.05), q25=quantile(ordered, 0.25),
                   q75=quantile(ordered, 0.75), q95=quantile(ordered, 0.95),
                   robust_n=len(kept), robust_mean=statistics.fmean(kept),
                   robust_sd=statistics.stdev(kept) if len(kept) > 1 else None)
    return out


def resolution(spacing):
    if spacing is None:
        return "spacing not read"
    return next(name for top, name in RESOLUTION if spacing <= top)


def brief(readings):
    n = len(readings)
    return {"n": n, "mean": statistics.fmean(readings) if n else None,
            "sd": statistics.stdev(readings) if n > 1 else None,
            "median": statistics.median(readings) if n else None}


def by_stratum(strata, coarsest):
    """Each key and level's mean and SD again by member (label source) and by the CT's coarsest spacing."""
    members, resolutions = {}, {}
    for (key, level), rows in sorted(strata.items()):
        groups_m, groups_r = {}, {}
        for member, path, study, value in rows:
            groups_m.setdefault(member, []).append(value)
            groups_r.setdefault(resolution(coarsest.get((path, study))), []).append(value)
        members.setdefault(key, {})[level] = {name: brief(v) for name, v in sorted(groups_m.items())}
        resolutions.setdefault(key, {})[level] = {name: brief(v) for name, v in sorted(groups_r.items())}
    return members, resolutions


FLAGGED_KEYS = ("body_w_mid", "body_d_mid", "endplate", "canal_w", "interpedicular_max")
# The engine's stand-ins: where it cannot read a measure by its definition it reads something else and flags it.
# canal.py: no pedicle found on both sides, the hole's width through the middle stands in for the interpedicular
# distances (interpedicular_band); anatomy.clip_to_foramina: no foramen transversarium found closed, the cervical body
# is cut at the canal's side walls and a millimetre beyond, so its width is the canal's plus two (body_foramina).
STAND_INS = {"interpedicular_max": ("interpedicular_band",), "interpedicular": ("interpedicular_band",),
             "body_w_mid": ("body_foramina",), "endplate": ("body_foramina",)}


def as_defined(strata, flags):
    """Each stand-in measure's summary over the vertebrae the engine read by the measure's own definition."""
    out = {}
    for (key, level), rows in strata.items():
        if key not in STAND_INS:
            continue
        kept = [(member, value) for member, path, study, value in rows
                if not set(STAND_INS[key]) & flags.get((path, study, level), set())]
        out.setdefault(key, {})[level] = summary([("gold4" if m == "gold4" else "gold3", v) for m, v in kept])
    return out


def by_flag(strata, flags):
    """For the body and canal widths, each level's mean again by whether the vertebra carries each flag, and how many
    vertebrae carry each flag at each level."""
    out = {"counts": {}, "means": {}}
    for (path, study, level), names in flags.items():
        for name in names:
            out["counts"].setdefault(level, {}).setdefault(name, 0)
            out["counts"][level][name] += 1
    for (key, level), rows in strata.items():
        if key not in FLAGGED_KEYS:
            continue
        groups = {}
        for member, path, study, value in rows:
            for name in flags.get((path, study, level), {"none"}):
                groups.setdefault(name, []).append(value)
        out["means"].setdefault(key, {})[level] = {name: brief(v) for name, v in sorted(groups.items()) if len(v) >= 5}
    return out


def profile(morphometry: str, persons: str, gold4: str, out: str) -> None:
    chosen = {}
    with open(persons, newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            chosen.setdefault(GOLD3_ROWS[row["member"]], set()).add(row["study"])
    values, spines, strata, coarsest, flags = {}, {}, {}, {}, {}
    for rows, studies in sorted(chosen.items()):
        member = {"enhance/rows.csv": "enhance_pet", "verse/rows.csv": "verse", "verse/totalseg/rows.csv": "totalseg"}[rows]
        read_rows(os.path.join(morphometry, rows), studies, "gold3", values, spines, member, strata, coarsest, flags)
    if gold4 and os.path.isfile(gold4):
        read_rows(gold4, None, "gold4", values, spines, "gold4", strata, coarsest, flags)
    measured = {k for k, levels in spines.items() if levels}
    result = {
        "spines": {source: sum(1 for k in measured if k[0] == source) for source in ("gold3", "gold4")},
        "persons_listed_gold3": sum(len(s) for s in chosen.values()),
        "extra_levels": {level: {source: sum(1 for k in measured if k[0] == source and level in spines[k])
                                 for source in ("gold3", "gold4")} for level in EXTRA},
        "measures": {},
    }
    result["spines"]["all"] = result["spines"]["gold3"] + result["spines"]["gold4"]
    for (key, level), pairs in sorted(values.items()):
        result["measures"].setdefault(key, {})[level] = summary(pairs)
    result["by_member"], result["by_resolution"] = by_stratum(strata, coarsest)
    result["by_flag"] = by_flag(strata, flags)
    result["as_defined"] = as_defined(strata, flags)
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=1, sort_keys=True)
    print(json.dumps({"spines": result["spines"], "extra_levels": result["extra_levels"]}, sort_keys=True))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("links")
    a.add_argument("--records", required=True)
    a.add_argument("--labels-root", required=True)
    a.add_argument("--masks", required=True)
    b = sub.add_parser("profile")
    b.add_argument("--morphometry", required=True)
    b.add_argument("--persons", required=True)
    b.add_argument("--gold4", default="")
    b.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    if args.cmd == "links":
        links(args.records, args.labels_root, args.masks)
    else:
        profile(args.morphometry, args.persons, args.gold4, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
