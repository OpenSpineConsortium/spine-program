"""SAP A1: the PRISMA two-arm flow counts and the identities the build asserts, into analysis/flow.json.

WHY THE FLOW READS ITS OWN PRODUCER'S BOOK-KEEPING BACK. sdr/dedup_prescreen.py writes
prisma_counts.json with `identified`, `duplicates_removed` (the sum over its merge rules) and
`after_merge`, and merged.jsonl with one row per merged record. An earlier version of this
analysis derived `duplicates_removed` as identified - len(merged) and then asserted that
identified - duplicates = after_merge, which cannot fail. Now the three numbers are read from
prisma_counts.json and compared with what is on disk: after_merge against the rows of
merged.jsonl, duplicates_removed against the sum of the rule counts (keys `rule_0_` .. `rule_6_`;
`rule_6_skipped_*` are diagnostics and are not merge rules). Only when prisma_counts.json is
absent are the derived values used, and then that is a listed missing input.

The other identities: the search-arm chain from screening to full text (reviewer CSVs under
data/screening/ first, then screen/: decisions.csv with protocol 7.3 columns plus optional
`full_text_retrieved` yes/no and `arm` search/other, prescreen_audit.csv, chase_manual.csv,
known_items.csv), and the record-to-dataset map: the number of charted datasets must equal the
number of distinct datasets reached from the included records (search and other arm) through
charting/dataset_sources.csv (`dataset_id, record_id, role`; role `use` is a use, not a source)
and each record's `source_record.record_ids`, with no included record unmapped. When
dataset_sources.csv is present the identity is True or False, never skipped; the datasets not
reached and the records not mapped are listed beside it.

`prescreen.uncertain_no_abstract` is the share of `uncertain` that carries 7.2's no-abstract rule:
records no source gave an abstract for (Semantic Scholar elides closed-access abstracts), which
reach the reviewer instead of being counted as a modality or dataset failure. It is read from the
`rule_fired` column of the prescreen sheet, so it is null-free and never exceeds `uncertain`.

Chase counts (backward, forward) come from records/chase.jsonl (queries/literature.yaml: source
`chase`, query ids `openalex_03_*` forward and `openalex_03r_*` backward) or, until that adapter
exists, from `openalex_03*` rows in any records file; those rows are other-arm candidates and are
not counted in a search source's `n_identified`. With no chase rows at all the two counts are
null and `chase records` is a missing input, so a zero is never reported for a step not run.
Sources whose queries.json roles hold no `search` entry are not search-arm sources and do not
appear in per_source.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from sdr.common import RunDir, read_jsonl
from sdr.dedup_prescreen import NO_ABSTRACT_RULE
from sdr.descriptives import _sec, _sum_median, _xt

MERGE_RULE_KEY = re.compile(r"^rule_[0-6]_(?!skipped)")     # dedup_prescreen.MERGE_RULES; rule_6_skipped_* are diagnostics


def _csv(path: Path, missing: list) -> list[dict]:
    if not path.exists():
        missing.append(str(path.name))
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _csv_in(name: str, dirs: list[Path], missing: list) -> list[dict]:
    """The first `dirs` entry holding `name` (data/screening/ before screen/); missing when none does."""
    for d in dirs:
        if (d / name).exists():
            return _csv(d / name, missing)
    missing.append(name)
    return []


def _sources(rd: RunDir, missing: list) -> tuple[dict, Counter]:
    """per_source (search-arm sources only) from queries.json and records/*.jsonl, and the chase counter.

    `hit_count_api` sums the queries whose `unit` is `records` only, as counts.json does: Open-i reports
    figures, Commons files, PhysioNet, TCIA and grand-challenge the size of a listing, and adding those to
    a record count would put figures into a PRISMA number. The other units are kept, per unit, in
    `hit_count_by_unit`. `partial` lists the query ids whose requests did not all answer, so a count that
    is a lower bound is not read as a complete one."""
    per_source = defaultdict(lambda: {"hit_count_api": 0, "hit_count_by_unit": {}, "n_retrieved": 0, "n_identified": None,
                                      "credential_mode": set(), "cap_hit": [], "partial": []})
    roles = defaultdict(set)
    for qid, r in rd.queries().items():
        if not isinstance(r, dict):
            continue
        roles[r["source"]].add(r.get("role", "search"))
        if r.get("role", "search") == "search":
            s, u, h = per_source[r["source"]], str(r.get("unit") or "records"), r.get("hit_count_api") or 0
            s["hit_count_by_unit"][u] = s["hit_count_by_unit"].get(u, 0) + h
            s["hit_count_api"] += h if u == "records" else 0
            s["n_retrieved"] += r.get("n_retrieved") or 0
            s["credential_mode"].add(r.get("credential_mode", "unknown"))
            s["cap_hit"] += [qid] if r.get("cap_hit") else []
            s["partial"] += [qid] if (r["partial"] if "partial" in r else (r.get("n_failed_requests") or 0)) else []
    chase = Counter()
    for f in sorted(rd.records.glob("*.jsonl")) if rd.records.exists() else []:
        rows = list(read_jsonl(f))
        ch = [r for r in rows if f.stem == "chase" or str(r.get("query_id", "")).startswith("openalex_03")]
        chase.update("backward" if str(r.get("query_id", "")).startswith("openalex_03r_") else "forward" for r in ch)
        if f.stem != "chase" and "search" in roles.get(f.stem, {"search"}):
            per_source[f.stem]["n_identified"] = len(rows) - len(ch)
    if not chase:
        missing.append("chase records (records/chase.jsonl or openalex_03* rows)")
    for s in per_source.values():
        s["credential_mode"] = sorted(s["credential_mode"])
        s["hit_count_by_unit"] = dict(sorted(s["hit_count_by_unit"].items()))
    return dict(sorted(per_source.items())), chase


def flow(rd: RunDir, screen: Path, charting: Path, ds: list[dict], decisions_dir: Path | None = None) -> dict:
    """PRISMA two-arm counts (SAP A1) and the identity checks; null wherever an input is missing.
    Reviewer CSVs are looked up under `decisions_dir` (data/screening/) first, then `screen`."""
    dirs, missing = [d for d in (decisions_dir, screen) if d is not None], []
    per_source, chase = _sources(rd, missing)
    merged = list(read_jsonl(rd.merged)) if rd.merged.exists() else None
    if merged is None:
        missing.append("merged.jsonl")
    pc_path = rd.root / "prisma_counts.json"
    prisma = json.loads(pc_path.read_text(encoding="utf-8")) if pc_path.exists() else None
    if prisma is not None:
        identified, after_merge, dups = prisma["identified"], prisma.get("after_merge"), prisma.get("duplicates_removed")
        rules = {k: v for k, v in prisma.get("merge", {}).items() if MERGE_RULE_KEY.match(k)}
    else:
        missing.append("prisma_counts.json (identified, after_merge and duplicates_removed derived from records/ and merged.jsonl)")
        identified = sum(s["n_identified"] or 0 for s in per_source.values()) + sum(chase.values())
        after_merge = None if merged is None else len(merged)
        dups = None if merged is None else identified - after_merge
        rules = {}
    pre = _csv_in("prescreen.csv", dirs, []) or [{"record_id": r["record_id"], "outcome": r["prescreen_outcome"], "source_class": r.get("source_class"),
                                                  "rule_fired": r.get("rule_fired", "")} for r in _csv(rd.root / "screening_sheet.csv", missing)]
    audit = _csv_in("prescreen_audit.csv", dirs, missing)
    dec, srcs_path = _csv_in("decisions.csv", dirs, missing), charting / "dataset_sources.csv"
    srcs = _csv(srcs_path, missing)
    pc, aud = Counter(r["outcome"] for r in pre), Counter(r["decision"] for r in audit)
    fails = {k: v for k, v in pc.items() if k.startswith("fail")}
    ta_all = {r["record_id"]: r for r in dec if r["stage"] == "title-abstract"}
    other = {rid for rid, r in ta_all.items() if r.get("arm") == "other"}
    ta = {rid: r for rid, r in ta_all.items() if rid not in other}          # search arm only; the other arm has its own box
    final = {}
    for r in dec:
        if r["stage"] == "resolution" or (r["stage"] == "full-text" and r["record_id"] not in final):
            final[r["record_id"]] = r
    ta_dec = Counter(r["decision"] for r in ta.values())
    excl = [r for r in ta.values() if r["decision"] == "exclude"]
    use_only = sum("use-only" in (r.get("codes") or "") for r in excl)
    ft_ids = [rid for rid, r in ta.items() if r["decision"] in ("include", "unclear")]
    ft = {rid: final[rid] for rid in ft_ids if rid in final}
    included = sorted(rid for rid, r in ft.items() if r["decision"] == "include")
    inc_other = sorted(rid for rid in other if final.get(rid, ta_all[rid])["decision"] == "include")
    kic = Counter(f"{r.get('role')}/{r.get('retrieved') or 'unknown'}" for r in _csv_in("known_items.csv", dirs, missing))
    use_per, rec_per = Counter(r["dataset_id"] for r in srcs if r.get("role") == "use"), Counter(r["dataset_id"] for r in srcs if r.get("role") != "use")
    rmap, inc_all = defaultdict(set), set(included) | set(inc_other)          # record -> datasets (module docstring)
    for r in srcs:
        if r.get("role") != "use":
            rmap[r["record_id"]].add(r["dataset_id"])
    for d in ds:
        for rid in d["source_record"]["record_ids"]:
            rmap[rid].add(d["id"])
    listed = {r["record_id"] for r in srcs} | set(rmap)
    mapped = sorted(set().union(*(rmap.get(r, set()) for r in inc_all)) if inc_all else set())
    v = {"per_source": per_source, "missing_inputs": missing, "identified": identified, "after_merge": after_merge,
         "merged_rows": None if merged is None else len(merged), "duplicates_removed": dups, "merge_rules": rules, "prisma_counts_present": prisma is not None,
         "prescreen": {"pass": pc.get("pass", 0), "uncertain": pc.get("uncertain", 0), "non_english_route": pc.get("pass:non-english-route", 0),
                       "uncertain_no_abstract": sum((r.get("rule_fired") or "") == NO_ABSTRACT_RULE for r in pre),
                       "fail": dict(sorted(fails.items())), "fail_total": sum(fails.values()),
                       "by_source_class": _xt(pre, lambda r: [r.get("source_class", "unknown")], lambda r: [r["outcome"]])},
         "audit": {"sampled": len(audit), "included": aud.get("include", 0), "excluded": len(audit) - aud.get("include", 0),
                   "by_stratum": _xt(audit, lambda r: [r.get("stratum", "unknown")], lambda r: [r["decision"]])},
         "screened": len(ta), "screen_excluded_by_code": dict(sorted(Counter(r.get("primary_code") or "unknown" for r in excl if "use-only" not in (r.get("codes") or "")).items())),
         "use_only": use_only, "unclear_to_full_text": ta_dec.get("unclear", 0), "include_to_full_text": ta_dec.get("include", 0),
         "sought_for_full_text": len(ft_ids), "not_retrieved": sum((r.get("full_text_retrieved") or "yes").lower() == "no" for r in ft.values()),
         "full_text_excluded_by_code": dict(sorted(Counter(r.get("primary_code") or "unknown" for r in ft.values() if r["decision"] == "exclude").items())),
         "included_records": len(included), "included_records_search": len(included), "included_records_other": len(inc_other),
         "other_arm": {"known_items": dict(sorted(kic.items())), "chase_backward": chase["backward"] if chase else None,
                       "chase_forward": chase["forward"] if chase else None, "chase_manual": len(_csv_in("chase_manual.csv", dirs, missing)),
                       "screened": len(other), "excluded": len(other) - len(inc_other), "included": len(inc_other)},
         "datasets": len(ds), "derived": sum(d["flags"]["derived"] for d in ds), "figure_derived": sum(d["flags"]["figure_derived"] for d in ds),
         "non_derived_non_figure": sum(not d["flags"]["derived"] and not d["flags"]["figure_derived"] for d in ds),
         "mapped_from_included_records": mapped, "included_records_unmapped": sorted(inc_all - listed),
         "not_mapped_from_included": sorted(d["id"] for d in ds if d["id"] not in mapped), "dataset_sources_present": srcs_path.exists(),
         "n_use_records_per_dataset": _sum_median([use_per.get(d["id"], 0) for d in ds]),
         "source_records_per_dataset": _sum_median([rec_per.get(d["id"], len(d["source_record"]["record_ids"])) for d in ds])}
    v["identities"] = flow_identities(v)
    return _sec(nest_flow(v), ["<run-dir>/queries.json", "<run-dir>/merged.jsonl", "<run-dir>/records/*.jsonl", "<run-dir>/prisma_counts.json",
                               "<run-dir>/screening_sheet.csv", "data/screening/*.csv", "screen/*.csv", "charting/dataset_sources.csv",
                               "charting/datasets/*.json"], "SAP A1")


def nest_flow(v: dict) -> dict:
    """The manuscript's shape: search_arm.*, other_arm.*, datasets.* (sdr/manuscript.py docstring); the
    identities are computed on the flat dict first, then the keys are grouped."""
    ds_keys = ("datasets", "derived", "figure_derived", "non_derived_non_figure", "n_use_records_per_dataset", "source_records_per_dataset",
               "mapped_from_included_records", "included_records_unmapped", "not_mapped_from_included", "dataset_sources_present")
    top = ("per_source", "missing_inputs", "identities", "other_arm")
    oa = dict(v["other_arm"])
    oa["known_items_by_role_retrieved"], oa["known_items"] = oa["known_items"], sum(oa["known_items"].values())
    oa["included_records"] = oa.pop("included")
    return {**{k: v[k] for k in top if k != "other_arm"}, "other_arm": oa,
            "search_arm": {k: v[k] for k in v if k not in top and k not in ds_keys and k != "included_records_other"},
            "datasets": {("total" if k == "datasets" else k): v[k] for k in ds_keys}}


def flow_identities(v: dict) -> dict:
    """The SAP A1 identities the build asserts; True / False / None (an input was missing). The first
    three compare prisma_counts.json with itself, with merged.jsonl and with the rule counts."""
    p, pc, known = v["prescreen"], v["prisma_counts_present"], lambda *xs: all(x is not None for x in xs)
    return {"identified - duplicates = after_merge": (v["identified"] - v["duplicates_removed"] == v["after_merge"]) if known(v["duplicates_removed"], v["after_merge"]) else None,
            "after_merge (prisma_counts) = rows of merged.jsonl": (v["after_merge"] == v["merged_rows"]) if pc and known(v["merged_rows"]) else None,
            "duplicates_removed = sum of merge rule counts": (v["duplicates_removed"] == sum(v["merge_rules"].values())) if pc and known(v["duplicates_removed"]) else None,
            "after_merge = fail + pass + uncertain + non_english": (v["after_merge"] == p["fail_total"] + p["pass"] + p["uncertain"] + p["non_english_route"]) if known(v["after_merge"]) else None,
            "screened = pass + uncertain + non_english + audit_included": v["screened"] == p["pass"] + p["uncertain"] + p["non_english_route"] + v["audit"]["included"],
            "screened = excluded + use_only + to_full_text": v["screened"] == sum(v["screen_excluded_by_code"].values()) + v["use_only"] + v["unclear_to_full_text"] + v["include_to_full_text"],
            "sought = full_text_excluded + included_records": v["sought_for_full_text"] == sum(v["full_text_excluded_by_code"].values()) + v["included_records"],
            "datasets = non_derived_non_figure + derived + figure_derived": v["datasets"] == v["non_derived_non_figure"] + v["derived"] + v["figure_derived"],
            "datasets = |map(included_records_search U included_records_other)|":
                (v["datasets"] == len(v["mapped_from_included_records"]) and not v["included_records_unmapped"]) if v["dataset_sources_present"] else None}
