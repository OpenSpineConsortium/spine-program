#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/rare_class_maximize.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Maximize the rendered transitional bank from the one registry: what is rendered, what is not, and the plan.

Reads SchwingNet/results/transitional_registry/registry.csv (one row per person) and a snapshot of what each
rare-class render root already holds (`--rendered-json`, written from `ls <root>/ann` on the grid, or scanned
with `--scan-roots` when run there), and writes, under SchwingNet/results/transitional_registry/maximize/:

  rare_max_verse.json / rare_max_ctsp.json / rare_max_totalsegmentator.json / rare_max_ctspine1k.json
      case -> {subtype, subtype_source, patient_key, truth_tier, modifiers, ..., require_ids / require_n_lumbar}
      for tools/rare_class_render.py (the id guard fields hold a case whose mask cannot carry its call);
  waiting.csv            single-labeller / morphology-only persons (adjudication first) and real-frame persons (TEST);
  MAXIMIZE.md            per-subtype persons and frames before / after, the oversampling weights the decided recipe
                         implies, the held / unavailable cases, and the PENDING job table when --jobs is given.

RULES (task of 2026-09-24): CT-only persons at tier read or two-labeller are rendered; single-labeller and
morphology-only rows wait for adjudication; COBRA / C-ArmLSpine / DeepFluoro / Ljubljana persons are real-frame
TEST persons and are never rendered for training. One CT per person (the registry's winning case).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
REG_DIR = HERE / "SchwingNet" / "results" / "transitional_registry"
POSITIVE = ("L6", "T13", "both_L6_T13", "sacralised_L5_fused", "castellvi_I_II", "lumbar_rib", "unassigned")
RENDER_TIERS = ("read", "two-labeller")
FRAMES_PER_CASE = 70            # rare_class_render: 10 poses x (1 raw + 6 device cards)
SUBTYPE_ORDER = ["L6", "T13", "sacralised_L5_fused", "castellvi_I_II", "lumbar_rib", "unassigned"]

# the decided recipe (docs/FLAGSHIP_PLAN.md "Ratio and oversampling"; docs/RESUME_2026-09-22_PM.md ratio table)
RECIPE = dict(
    real_transitional_epoch_repeat=4,
    variant_share_of_rendered_cts=(0.25, 0.35),
    synthetic_per_real_rare_frame_max=10,
    real_share_of_finetune_mix=(0.10, 0.20),
    parity_rebalancing="none (no weighted BCE, no parity resampling)",
    renders_per_ct=(200, 500),
)

# every source's render recipe: where the CT + mask come from, how the stage dir / stem / patient_id are spelled
SOURCES = {
    "verse": dict(scheme="verse", layout="verse", pid="{scheme}_{case}", root="verse_drr",
                  mask_scheme="verse_ids (VerSeFusion unified mask)",
                  src="$HOME/VerSeFusion/data/unified"),
    "ctsp": dict(scheme="ctsp", layout="stage", pid="{scheme}_{case}", root="ctsp_drr_arc",
                 mask_scheme="verse_ids (CTSpinoPelvic1K v11 release label, 20..25 lumbar, 26 sacrum)",
                 src="$RC/ctsp_stage"),
    "totalsegmentator": dict(scheme="totalseg", layout="stage", pid="ts_{case}", root="totalsegmentator_drr_arc",
                             mask_scheme="verse_ids_spineps (SPINEPS seg-vert relabelled by the VERIDAH ctd, ~/bench_ts/spineps/native_ctd)",
                             src="$RC/ts_stage_arc"),
    "ctspine1k": dict(scheme="ctspine1k", layout="stage", pid="{scheme}_{case}", root="ctspine1k_drr_arc",
                      mask_scheme="verse_ids (CTSpine1K release annotation; no sacrum id)",
                      src="$RC/ctspine1k_stage"),
}
# TotalSegmentator scans with no SPINEPS mask in native_ctd (v300-only ids): known at plan time from the grid census
TS_NO_MASK = {"s1974": "v300-only scan: no SPINEPS seg-vert mask in ~/bench_ts/spineps/native_ctd, no v201 CT",
              "s2047": "v300-only scan: no SPINEPS seg-vert mask in ~/bench_ts/spineps/native_ctd, no v201 CT"}


def truthy(v):
    return str(v).strip().lower() in ("true", "1", "yes")


def case_of(src, r):
    """The render case id for a registry person (one CT per person: the winning case)."""
    wc = r["winning_case"]
    if src == "ctsp":
        return wc.zfill(4)
    if src == "totalsegmentator":
        return "TS_" + wc.replace("TS_", "")
    if src == "ctspine1k":
        return wc.split("/")[-1]           # MSD-T10/liver_106 -> liver_106 (stage dir); registry_source_case keeps the full form
    return wc


def guard_for(r):
    st = r["subtype"]
    g = {}
    if st == "L6":
        g["require_ids"] = [25]
    elif st == "T13":
        g["require_ids"] = [28]
    elif st == "both_L6_T13":
        g["require_ids"] = [25, 28]
    if truthy(r.get("four_lumbar")) and (r.get("fused_mask_representation") or "") != "own-id":
        g["require_n_lumbar"] = 4
    return g


def load_registry(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rendered_from_roots(rc):
    """Scan the rare-class roots on the grid: {root: sorted source cases}."""
    out = {}
    for name, sp in SOURCES.items():
        d = Path(rc) / sp["root"] / "ann"
        if not d.is_dir():
            out[sp["root"]] = []
            continue
        rx = re.compile(rf"^{sp['scheme']}_(.+?)_(lat|ap|obl)_p\d+")
        out[sp["root"]] = sorted({m.group(1) for p in d.iterdir() if (m := rx.match(p.name))})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default=str(REG_DIR / "registry.csv"))
    ap.add_argument("--out", default=str(REG_DIR / "maximize"))
    ap.add_argument("--rendered-json", default=None, help="{root: [source cases]} snapshot (from ls <root>/ann)")
    ap.add_argument("--scan-roots", default=None, help="rare_class root on the grid; scans ann dirs instead")
    ap.add_argument("--before-frames", default=None, help="{root: {'anns': n, 'per_subtype': {...}}} snapshot")
    ap.add_argument("--jobs", default=None, help="jobs json written after sbatch: [{job, name, submitted, eta, ...}]")
    ap.add_argument("--after-dir", default=None,
                    help="the collect step's output pulled from the grid (<root>_VERIFY.json, held_all.json, "
                         "precheck_stopped.json): frames and held / stopped cases are then read FROM DISK, not projected")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = load_registry(a.registry)

    if a.scan_roots:
        rendered = rendered_from_roots(a.scan_roots)
    elif a.rendered_json:
        rendered = json.load(open(a.rendered_json))
    else:
        rendered = {}
    before = json.load(open(a.before_frames)) if a.before_frames else {}
    already = {}
    for name, sp in SOURCES.items():
        cases = set(rendered.get(sp["root"], []))
        if name == "verse":
            cases |= set(rendered.get("verse_drr", []))
        if name == "ctsp":
            cases |= set(rendered.get("ctsp_drr", []))           # the 34 of rare_ctsp_drr.sh (physics recipe)
        if name == "totalsegmentator":
            cases |= {"TS_" + c for c in rendered.get("totalsegmentator_drr", [])}   # the ts12 (rcts2)
        already[name] = cases

    plan = {name: {} for name in SOURCES}
    unavailable = []
    waiting = []
    persons_by = Counter()          # (source, subtype, tier, status)
    for r in rows:
        if not truthy(r.get("is_person", "True")):
            continue
        st = r["subtype"]
        if st not in POSITIVE:
            continue
        src, tier = r["winning_source"], r["truth_tier"]
        if truthy(r.get("real_frames")):
            waiting.append(dict(patient_key=r["patient_key"], source=src, subtype=st, tier=tier,
                                status="real-frames: TEST only, never rendered"))
            persons_by[(src, st, tier, "test_real")] += 1
            continue
        if tier not in RENDER_TIERS:
            waiting.append(dict(patient_key=r["patient_key"], source=src, subtype=st, tier=tier,
                                status="waits for adjudication (single-labeller / morphology-only)",
                                review_queue=r.get("review_queue", "")))
            persons_by[(src, st, tier, "waiting")] += 1
            continue
        if src not in SOURCES:
            unavailable.append(dict(patient_key=r["patient_key"], source=src, subtype=st, tier=tier,
                                    why=f"no render recipe for source {src}"))
            persons_by[(src, st, tier, "no_recipe")] += 1
            continue
        case = case_of(src, r)
        if src == "totalsegmentator" and case.replace("TS_", "") in TS_NO_MASK:
            unavailable.append(dict(patient_key=r["patient_key"], source=src, subtype=st, tier=tier,
                                    why=TS_NO_MASK[case.replace("TS_", "")]))
            persons_by[(src, st, tier, "unavailable")] += 1
            continue
        if case in already[src]:
            persons_by[(src, st, tier, "rendered")] += 1
            continue
        sp = SOURCES[src]
        entry = dict(
            subtype=st,
            subtype_source=f"transitional registry 2026-09-24 ({src} stream, tier {tier})",
            patient_key=r["patient_key"], truth_tier=tier,
            castellvi=r.get("castellvi", ""), four_lumbar=truthy(r.get("four_lumbar")),
            lumbar_rib=truthy(r.get("lumbar_rib")),
            fused_mask_representation=r.get("fused_mask_representation", ""),
            modifiers=[m for m, on in (("four_lumbar", truthy(r.get("four_lumbar"))),
                                       ("lumbar_rib", truthy(r.get("lumbar_rib")))) if on],
            mask_scheme=sp["mask_scheme"], registry_source_case=r["winning_case"],
            review_queue=r.get("review_queue", ""),
        )
        entry.update(guard_for(r))
        plan[src][case] = entry
        persons_by[(src, st, tier, "to_render")] += 1

    for name, sp in SOURCES.items():
        d = dict(_about=f"tools/rare_class_maximize.py {datetime.now():%Y-%m-%d %H:%M}: {name} persons of the "
                        f"transitional registry at tier read / two-labeller, CT-only, not yet rendered. "
                        f"Renderer: tools/rare_class_render.py --layout {sp['layout']} --scheme {sp['scheme']} "
                        f"--patient-id-format '{sp['pid']}' --dst $RC/{sp['root']}. require_ids / "
                        f"require_n_lumbar hold a case whose mask does not carry its call.",
                 _n=len(plan[name]))
        d.update(plan[name])
        json.dump(d, open(out / f"rare_max_{name}.json", "w"), indent=1)
        with open(out / f"rare_max_{name}_cases.txt", "w", newline="\n") as f:
            for c in sorted(plan[name]):
                f.write(c + "\n")
    with open(out / "waiting.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["patient_key", "source", "subtype", "tier", "status", "review_queue"])
        w.writeheader()
        for row in sorted(waiting, key=lambda x: (x["source"], x["subtype"], x["patient_key"])):
            w.writerow({k: row.get(k, "") for k in w.fieldnames})
    json.dump(unavailable, open(out / "unavailable.json", "w"), indent=1)

    after = load_after(a.after_dir, plan) if a.after_dir else None
    write_md(out, rows, plan, persons_by, waiting, unavailable, before, rendered, already,
             json.load(open(a.jobs)) if a.jobs else None, after)
    if after:
        print("after (from disk): " + ", ".join(
            f"{s} rendered {len(v['rendered'])} held {len(v['held'])} stopped {len(v['stopped'])} "
            f"unaccounted {len(v['unaccounted'])}" for s, v in after["per_source"].items()))
    tot = sum(len(v) for v in plan.values())
    print(f"to render: {tot} cases " + ", ".join(f"{k} {len(v)}" for k, v in plan.items())
          + f"; waiting {len(waiting)}; unavailable {len(unavailable)}")
    return 0


SCHEME_TO_SOURCE = {"verse": "verse", "ctsp": "ctsp", "ts": "totalsegmentator", "ctspine1k": "ctspine1k"}


def person_cases(rows):
    """{(source, patient_key): {render case ids of every scan of that person in that source}} from registry `sources`."""
    out = defaultdict(set)
    for r in rows:
        for s in (r.get("sources") or "").split(";"):
            if ":" not in s:
                continue
            scheme, c = s.split(":", 1)
            src = SCHEME_TO_SOURCE.get(scheme)
            if not src:
                continue
            out[(src, r["patient_key"])].add(case_of(src, {"winning_case": c}))
    return out


def load_after(after_dir, plan):
    """The collect step's files, pulled from the grid: what every planned case became, per source, FROM DISK.

    rendered = the case has frames in <root>_VERIFY.json; held = the renderer's id guard wrote held/<case>.json
    (held_all.json); stopped = the stage precheck refused the case before the renderer ran (precheck_stopped.json,
    transcribed from the task logs); unaccounted = planned but none of the three (a real failure to chase).
    """
    d = Path(after_dir)
    verify = {}
    for name, sp in SOURCES.items():
        p = d / f"{sp['root']}_VERIFY.json"
        if p.exists():
            verify[sp["root"]] = json.load(open(p))
    held = json.load(open(d / "held_all.json")) if (d / "held_all.json").exists() else []
    stopped = {}
    if (d / "precheck_stopped.json").exists():
        stopped = {k: v for k, v in json.load(open(d / "precheck_stopped.json")).items() if not k.startswith("_")}
    per_source = {}
    for name, sp in SOURCES.items():
        root = sp["root"]
        planned = set(plan[name])
        on_disk = set((verify.get(root) or {}).get("frames_per_case", {}))
        h = {x["case"]: x for x in held if x["root"] == root}
        s = {x["case"]: x for x in stopped.get(root, [])}
        per_source[name] = dict(
            root=root, planned=sorted(planned), rendered=sorted(planned & on_disk),
            held=sorted(set(h) & planned), stopped=sorted(set(s) & planned),
            unaccounted=sorted(planned - on_disk - set(h) - set(s)),
            held_records=h, stopped_records=s,
            verify=verify.get(root),
        )
    return dict(dir=str(d), verify=verify, held=held, stopped=stopped, per_source=per_source,
                stamp=datetime.fromtimestamp(max(p.stat().st_mtime for p in d.glob("*.json"))))


def write_md(out, rows, plan, persons_by, waiting, unavailable, before, rendered, already, jobs, after=None):
    L = []
    L.append("# MAXIMIZE: every registry person the recipe allows, rendered")
    L.append("")
    if after:
        L.append(f"Written {datetime.now():%Y-%m-%d %H:%M} by `tools/rare_class_maximize.py` from "
                 f"`registry.csv` ({len(rows)} rows), the render roots' ann listings before the pass, and the collect "
                 f"step's files pulled from the grid (`{Path(after['dir']).as_posix()}`, written "
                 f"{after['stamp']:%Y-%m-%d %H:%M}). Generated; the numbers below are computed, none typed. The AFTER "
                 f"frame counts are READ FROM DISK (`<root>_VERIFY.json` of `SchwingNet/slurm/rare_max_verify.sh`), "
                 f"and the held / stopped cases are the renderer's own records (`held_all.json`, the task logs).")
    else:
        L.append(f"Written {datetime.now():%Y-%m-%d %H:%M} by `tools/rare_class_maximize.py` from "
                 f"`registry.csv` ({len(rows)} rows) and the render roots' ann listings. Generated; the numbers below are "
                 f"computed, none typed. The AFTER frame counts are projections (cases x {FRAMES_PER_CASE} frames: "
                 f"10 poses x [raw + 6 device cards]) until `SchwingNet/slurm/rare_max_verify.sh` (the collect step) "
                 f"rewrites them from disk.")
    L.append("")
    L.append("## The rule applied")
    L.append("")
    L.append("- Rendered for training: CT-only persons whose winning tier is `read` or `two-labeller`, one CT per "
             "person (the registry's winning case), every pose family (lateral x3, AP x3, arc obliques x4 at "
             "+/-35 and +/-50 deg yaw with cranio-caudal tilt) and every device card (bv_pulsera, cios_fusion, "
             "elekta_xvi, pixium_4600, surgio_b51_dr, varian_halcyon; DEVICE_SAMPLE_MODE=typicality) plus the raw "
             "bone DRR: 70 distinct frames per CT, no duplicates.")
    L.append("- Every ann carries patient_key, subtype, subtype_source, truth_tier, the modifiers (castellvi, "
             "four_lumbar, lumbar_rib), fused_mask_representation and mask_scheme, so the split and the stratified "
             "evaluation read the stratum and the tier off any frame.")
    L.append("- ID GUARD: a case is rendered only if its mask carries the ids its call names (L6 -> id 25, T13 -> 28, "
             "a four-lumbar call with the fused body merged or unlabelled -> exactly four lumbar ids). Otherwise the "
             "renderer HOLDS it (`<root>/held/<scheme>_<case>.json`) rather than box bodies under names the registry "
             "disputes. Held cases are listed by the collect step and stay in Greg's review queue.")
    L.append("- Waiting: single-labeller and morphology-only persons (adjudication first). Never rendered: COBRA, "
             "C-ArmLSpine, DeepFluoro, Ljubljana persons (real frames, TEST only).")
    L.append("")

    # ---- persons per subtype x status
    L.append("## Persons per subtype: rendered before, rendered by this pass, waiting, unavailable")
    L.append("")
    # outcome of every planned case, from disk, keyed like persons_by: (source, subtype, tier, outcome)
    outcome_by = Counter()
    if after:
        for src, ps in after["per_source"].items():
            for outcome in ("rendered", "held", "stopped", "unaccounted"):
                for c in ps[outcome]:
                    e = plan[src][c]
                    outcome_by[(src, e["subtype"], e["truth_tier"], outcome)] += 1
    if after:
        L.append("| subtype | source | tier | rendered before | planned by this pass | rendered (disk) | held (ID guard) "
                 "| stopped (precheck) | unaccounted | waiting (adjudication) | real-frames TEST | unavailable |")
        L.append("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    else:
        L.append("| subtype | source | tier | rendered before | to render now | waiting (adjudication) | real-frames TEST | unavailable |")
        L.append("|---|---|---|---:|---:|---:|---:|---:|")
    keys = sorted({(s, st, t) for (s, st, t, _) in persons_by},
                  key=lambda k: (SUBTYPE_ORDER.index(k[1]) if k[1] in SUBTYPE_ORDER else 9, k[0], k[2]))
    for s, st, t in keys:
        g = lambda status: persons_by.get((s, st, t, status), 0)  # noqa: E731
        o = lambda status: outcome_by.get((s, st, t, status), 0)  # noqa: E731
        if after:
            L.append(f"| {st} | {s} | {t} | {g('rendered')} | {g('to_render')} | {o('rendered')} | {o('held')} | "
                     f"{o('stopped')} | {o('unaccounted')} | {g('waiting')} | {g('test_real')} | "
                     f"{g('unavailable') + g('no_recipe')} |")
        else:
            L.append(f"| {st} | {s} | {t} | {g('rendered')} | {g('to_render')} | {g('waiting')} | {g('test_real')} | "
                     f"{g('unavailable') + g('no_recipe')} |")
    L.append("")
    tot_r = sum(v for (s, st, t, x), v in persons_by.items() if x == "rendered")
    tot_n = sum(v for (s, st, t, x), v in persons_by.items() if x == "to_render")
    tot_w = sum(v for (s, st, t, x), v in persons_by.items() if x == "waiting")
    tot_t = sum(v for (s, st, t, x), v in persons_by.items() if x == "test_real")
    tot_u = sum(v for (s, st, t, x), v in persons_by.items() if x in ("unavailable", "no_recipe"))
    tot_ok = sum(v for (s, st, t, x), v in outcome_by.items() if x == "rendered")
    tot_h = sum(v for (s, st, t, x), v in outcome_by.items() if x == "held")
    tot_s = sum(v for (s, st, t, x), v in outcome_by.items() if x == "stopped")
    tot_x = sum(v for (s, st, t, x), v in outcome_by.items() if x == "unaccounted")
    if after:
        L.append(f"Totals: rendered before {tot_r}; planned by this pass {tot_n}, of which rendered {tot_ok}, held by the "
                 f"ID guard {tot_h}, stopped at the precheck {tot_s}, unaccounted {tot_x}; waiting {tot_w}, real-frame "
                 f"TEST {tot_t}, unavailable {tot_u}. Rendered transitional CTs now: {tot_r + tot_ok}.")
    else:
        L.append(f"Totals: rendered before {tot_r}, to render now {tot_n}, waiting {tot_w}, real-frame TEST {tot_t}, "
                 f"unavailable {tot_u}.")
    L.append("")

    # ---- frames per subtype before / after
    per_sub_before = Counter()
    per_root_before = {}
    for root, rec in before.items():
        per_root_before[root] = rec.get("anns", 0)
        for st, n in (rec.get("per_subtype") or {}).items():
            per_sub_before[st] += n
    per_sub_new = Counter()
    per_src_new = Counter()
    if after:
        L.append("## Frames per subtype, before and after, FROM DISK (per source, then summed)")
        L.append("")
        L.append("Before = the ann snapshot taken at plan time (`before_frames.json`). New = what `rare_max_verify` counted "
                 "in each root after the arrays ended. The VerSe pass rendered into the existing `verse_drr` root, so its "
                 "new frames are the root's count minus the snapshot; the other three sources rendered into fresh `_arc` "
                 "roots, so their new frames are the root's whole count. Every frame is one ann with one img npy "
                 "(the verify skips an ann without its image).")
        L.append("")
        L.append("| source | subtype | before | new (disk) | after |")
        L.append("|---|---|---:|---:|---:|")
        # (source, before-root, new-root, shared?)
        pairing = [("verse", "verse_drr", "verse_drr", True), ("ctsp", "ctsp_drr", "ctsp_drr_arc", False),
                   ("totalsegmentator", "totalsegmentator_drr", "totalsegmentator_drr_arc", False),
                   ("ctspine1k", None, "ctspine1k_drr_arc", False),
                   ("carmlspine (real CBCT, TEST)", "carmlspine_cbct_drr", None, False)]
        per_src_frames = {}
        for src, b_root, n_root, shared in pairing:
            b = Counter((before.get(b_root) or {}).get("per_subtype") or {}) if b_root else Counter()
            v = (after["verify"].get(n_root) or {}) if n_root else {}
            disk = Counter(v.get("per_subtype") or {})
            new = Counter({k: disk[k] - b.get(k, 0) for k in disk}) if shared else disk
            aft = disk if shared else Counter(b) + disk
            for st in SUBTYPE_ORDER + sorted((set(b) | set(aft)) - set(SUBTYPE_ORDER)):
                if st not in b and st not in aft:
                    continue
                L.append(f"| {src} | {st} | {b.get(st, 0)} | {new.get(st, 0)} | {aft.get(st, 0)} |")
                per_sub_new[st] += new.get(st, 0)
            tb, tn, ta = sum(b.values()), sum(new.values()), sum(aft.values())
            per_src_frames[src] = (tb, tn, ta)
            per_src_new[src] = tn
            L.append(f"| **{src}** | **all** | **{tb}** | **{tn}** | **{ta}** |")
        L.append("")
        L.append("| subtype | frames before | + new (disk) | frames after |")
        L.append("|---|---:|---:|---:|")
        for st in SUBTYPE_ORDER + sorted((set(per_sub_before) | set(per_sub_new)) - set(SUBTYPE_ORDER)):
            if st not in per_sub_before and st not in per_sub_new:
                continue
            L.append(f"| {st} | {per_sub_before.get(st, 0)} | {per_sub_new.get(st, 0)} | "
                     f"{per_sub_before.get(st, 0) + per_sub_new.get(st, 0)} |")
        tb, tn = sum(per_sub_before.values()), sum(per_sub_new.values())
        L.append(f"| **all** | **{tb}** | **{tn}** | **{tb + tn}** |")
        L.append("")
        L.append("Before, per root (ann count; the TotalSegmentator root's per-subtype split follows the ctd subtypes of "
                 "its 12 cases, seven of which read as ordinary spines by the ctd): "
                 + ", ".join(f"`{k}` {v}" for k, v in sorted(per_root_before.items())) + ".")
        L.append("")
        L.append("New frames per source, from disk: " + ", ".join(
            f"{k} {v} ({len(after['per_source'][k]['rendered'])} CTs x {FRAMES_PER_CASE})"
            for k, v in per_src_new.items() if k in after["per_source"]) + ". Projected at plan time: "
            + ", ".join(f"{k} {len(v) * FRAMES_PER_CASE} ({len(v)} CTs)" for k, v in plan.items()) + ".")
        L.append("")
        # ---- the verify reports: what the collect step checked
        L.append("## What the collect step verified (`rare_class_verify.py` on the grid, one report per root)")
        L.append("")
        L.append("| root | cases with frames | frames (raw + styled) | per view | below floor (60) | bad anns | patient_keys unmatched | missing = held + stopped? |")
        L.append("|---|---:|---|---|---|---|---|---|")
        for src, ps in after["per_source"].items():
            v = ps["verify"]
            if not v:
                L.append(f"| `{ps['root']}` | (no VERIFY.json) | | | | | | |")
                continue
            pv = ", ".join(f"{k} {n}" for k, n in sorted((v.get("per_view") or {}).items()))
            miss = set(v.get("missing_cases") or [])
            expl = set(ps["held"]) | set(ps["stopped"])
            eq = "yes" if miss == expl else f"NO: missing-not-explained {sorted(miss - expl)}, explained-not-missing {sorted(expl - miss)}"
            L.append(f"| `{ps['root']}` | {v['cases']} | {v['frames_total']} ({v['frames_raw']} + {v['frames_styled']}) | {pv} | "
                     f"{v.get('below_floor') or 'none'} | {len(v.get('bad') or [])} | "
                     f"{len((v.get('patient_keys') or {}).get('unmatched') or [])} | {eq} |")
        L.append("")
        L.append("Per-class silhouettes worth knowing before anyone reads them as a defect: the TotalSegmentator "
                 "`unassigned` stratum carries L1-L4 and no L5 in any frame because every one of its cases is a "
                 "four-lumbar call that the `require_n_lumbar = 4` guard passed with exactly four lumbar ids; the "
                 "`sacralised_L5_fused` strata carry no L5 because the fused body is merged into the sacrum id; VerSe "
                 "frames carry no `sacrum` class because the VerSeFusion unified mask has no sacrum id.")
        L.append("")
    else:
        L.append("## Frames per subtype, before and after (after = projection; the collect step rewrites it)")
        L.append("")
        for src, cases in plan.items():
            for c, e in cases.items():
                per_sub_new[e["subtype"]] += FRAMES_PER_CASE
                per_src_new[src] += FRAMES_PER_CASE
        L.append("| subtype | frames before | + projected | frames after (projected) |")
        L.append("|---|---:|---:|---:|")
        for st in SUBTYPE_ORDER + sorted(set(per_sub_before) | set(per_sub_new) - set(SUBTYPE_ORDER)):
            if st not in per_sub_before and st not in per_sub_new:
                continue
            L.append(f"| {st} | {per_sub_before.get(st, 0)} | {per_sub_new.get(st, 0)} | "
                     f"{per_sub_before.get(st, 0) + per_sub_new.get(st, 0)} |")
        L.append("")
        L.append("Before, per root (ann count; the TotalSegmentator root's per-subtype split follows the ctd subtypes of "
                 "its 12 cases, seven of which read as ordinary spines by the ctd): "
                 + ", ".join(f"`{k}` {v}" for k, v in sorted(per_root_before.items())) + ".")
        L.append("")
        L.append("Projected new frames per source: " + ", ".join(f"{k} {v} ({len(plan[k])} CTs)" for k, v in per_src_new.items()) + ".")
        L.append("")

    # ---- oversampling weights from the decided recipe
    L.append("## Oversampling weights, from the decided recipe")
    L.append("")
    L.append("The recipe (docs/FLAGSHIP_PLAN.md, 'Ratio and oversampling'; docs/RESUME_2026-09-22_PM.md ratio table) "
             "fixes four numbers and forbids a fifth:")
    L.append("")
    L.append(f"1. Real transitional frames are repeated **{RECIPE['real_transitional_epoch_repeat']}x per epoch** in the "
             "fine-tune stage (VERIDAH 4x; Dushenev recall peaks at 4x). Real transitional people are TEST here, so "
             "this weight applies to no training frame of this bank; it is recorded so nobody re-derives it.")
    lo, hi = RECIPE["variant_share_of_rendered_cts"]
    L.append(f"2. Variants in **{int(lo*100)}-{int(hi*100)} % of rendered CTs, by choosing which CTs to render**, never "
             "by duplicating renders (x12 duplication once bought L6 Dice 0.000).")
    L.append(f"3. Synthetic per real rare frame capped near **{RECIPE['synthetic_per_real_rare_frame_max']}:1**; real "
             f"frames {int(RECIPE['real_share_of_finetune_mix'][0]*100)}-{int(RECIPE['real_share_of_finetune_mix'][1]*100)} % "
             "of the sampled fine-tune mix.")
    L.append(f"4. {RECIPE['renders_per_ct'][0]}-{RECIPE['renders_per_ct'][1]} renders per CT, transitional CTs first.")
    L.append(f"5. No parity rebalancing: {RECIPE['parity_rebalancing']}; rare recall is reported with PR-AUC.")
    L.append("")
    n_trans_cts = tot_r + (tot_ok if after else tot_n)
    # ordinary CTs in the render corpus (FLAGSHIP_PLAN G4: every CT of CTSP 802, TotalSegmentator ~1,228+, VerSe ~374)
    n_all_cts = 802 + 1228 + 374
    share_now = n_trans_cts / n_all_cts
    w_lo = (lo / (1 - lo)) * ((n_all_cts - n_trans_cts) / max(1, n_trans_cts))
    w_hi = (hi / (1 - hi)) * ((n_all_cts - n_trans_cts) / max(1, n_trans_cts))
    L.append(f"What that implies for this bank. After this pass the rendered transitional CTs number {n_trans_cts} "
             + (f"(rendered before {tot_r} + rendered by this pass from disk {tot_ok}; the {tot_h} held and {tot_s} stopped "
                f"cases do not count) " if after else "")
             + f"(read + two-labeller, CT-only) against ~{n_all_cts} CTs in the whole render corpus (CTSpinoPelvic1K 802 + "
             f"TotalSegmentator 1,228 + VerSe 374, every CT rendered under G4), a variant share of "
             f"{share_now*100:.1f} % by CT. The {int(lo*100)}-{int(hi*100)} % target is reached in the SAMPLER, not by "
             f"duplication: draw transitional CTs' frames with weight **w = {w_lo:.1f} to {w_hi:.1f}** relative to an "
             f"ordinary CT's frames (w = share/(1-share) x N_ordinary/N_transitional), applied per CT so that no frame is "
             f"repeated within an epoch (70 distinct frames per transitional CT here; the ordinary bank's per-CT frame "
             f"count sets how often each is seen). Per subtype the weight is the same w: the recipe balances variant vs "
             f"ordinary, never subtype vs subtype (parity rebalancing is refused).")
    L.append("")
    L.append("| subtype | transitional CTs rendered after this pass | per-CT sampling weight (25 % / 35 % target) |")
    L.append("|---|---:|---|")
    per_sub_cts = Counter()
    for (s, st, t, x), v in persons_by.items():
        if x == "rendered" or (x == "to_render" and not after):
            per_sub_cts[st] += v
    if after:
        for (s, st, t, x), v in outcome_by.items():
            if x == "rendered":
                per_sub_cts[st] += v
    for st in SUBTYPE_ORDER:
        if per_sub_cts.get(st):
            L.append(f"| {st} | {per_sub_cts[st]} | {w_lo:.1f} / {w_hi:.1f} |")
    L.append("")
    L.append("Caveat stated plainly: the TotalSegmentator root's 12 first-pass cases include seven the ctd reads as "
             "ordinary spines; they count as rendered CTs above only where the registry still types them positive.")
    L.append("")

    # ---- unavailable + waiting
    L.append("## Not rendered by this pass, and why")
    L.append("")
    if unavailable:
        L.append("Unavailable (no mask or CT the recipe can use):")
        L.append("")
        for u in unavailable:
            L.append(f"- `{u['patient_key']}` ({u['subtype']}, {u['tier']}): {u['why']}")
        L.append("")
    wc = Counter((w["source"], w["subtype"], w["status"].split(":")[0]) for w in waiting)
    L.append(f"Waiting ({len(waiting)} persons; `waiting.csv`):")
    L.append("")
    for (s, st, why), n in sorted(wc.items()):
        L.append(f"- {s} / {st}: {n} ({why})")
    L.append("")
    if after:
        L.append("### Held by the ID GUARD, from the renderer's own records (`held_all.json`)")
        L.append("")
        L.append("The mask cannot carry the call; a review verdict or a mask relabel unblocks each one. Every held case "
                 "that still needs a verdict is in its source's review queue with the reason `ID guard: mask cannot carry "
                 "the registry call` (verse `review_queue/queue.csv`, ctsp `review_queue/review_queue.csv`, ctspine1k "
                 "`other_ct/review_queue/index.csv`; column `id_guard`), no render duplicated. A held case whose PERSON is "
                 "already in the bank under another scan (the registry's winning case was a scan without the junction in "
                 "its field) is marked below and kept out of the queue: nothing is lost and nothing needs a verdict.")
        L.append("")
        pc = person_cases(rows)
        n_already = 0
        for src, ps in after["per_source"].items():
            if not ps["held"]:
                continue
            rendered_src = set(already.get(src, set())) | set(ps["rendered"])
            L.append(f"**{src}** (`{ps['root']}/held/`): {len(ps['held'])} of {len(ps['planned'])} planned")
            L.append("")
            for c in ps["held"]:
                h = ps["held_records"][c]
                others = sorted(o for o in pc.get((src, h["patient_key"]), set()) if o != c and o in rendered_src)
                note = ""
                if others:
                    n_already += 1
                    note = (f" -- PERSON ALREADY RENDERED under {', '.join(others)} (this scan's field has no "
                            f"lumbosacral junction); no review needed")
                L.append(f"- `{h['patient_key']}` (case {c}; {h['subtype']}, {h['truth_tier']}): {h['held']}{note}")
            L.append("")
        L.append(f"Holds that wait for a verdict: {tot_h - n_already} of {tot_h} ({n_already} are persons already in the "
                 f"bank under another scan).")
        L.append("")
        L.append("### Stopped at the stage precheck (never reached the renderer; `precheck_stopped.json`, from the task logs)")
        L.append("")
        any_stop = False
        for src, ps in after["per_source"].items():
            for c in ps["stopped"]:
                s = ps["stopped_records"][c]
                any_stop = True
                L.append(f"- `{src}:{c}` ({s['subtype']}, {s['truth_tier']}; task {s['job_task']}, {s['exit']}): {s['error']} "
                         f"-- {s['classification']}")
        if not any_stop:
            L.append("- none")
        L.append("")
        unacc = {src: ps["unaccounted"] for src, ps in after["per_source"].items() if ps["unaccounted"]}
        L.append("### Planned but neither rendered, held nor stopped")
        L.append("")
        L.append("- none: every planned case is accounted for" if not unacc else
                 "- " + "; ".join(f"{s}: {', '.join(v)}" for s, v in unacc.items()) + " (chase the task logs)")
        L.append("")
        L.append("What the plan expected the guard to hold, for the record (written before the arrays ran):")
    else:
        L.append("Cases the ID GUARD is expected to hold (the mask cannot carry the call; a review verdict or a mask relabel "
                 "unblocks them, and the renderer's held/ directory is the ground truth once the arrays run):")
    L.append("")
    L.append("- CTSpinoPelvic1K two-labeller L6 candidates 'the release did not call' (0090, 0105, 0359, 0474, 0544, "
             "0552, 0672, 0895, 1151, 1153): the v11 release label names five lumbar bodies and a rib-free T12; L6 is by "
             "the rib convention (the registry's `1-candidate` queue). Rendering them would box the sixth free body as "
             "T12. The mechanical relabel (release 19..24 -> 20..25, thoracic unchanged) is one line once Greg's "
             "verdict lands; it is not applied here.")
    L.append("- CTSpinoPelvic1K two-labeller unassigned 0349 and 1000 (four rib-free bodies by SPINEPS and "
             "TotalSegmentator against five release lumbar ids): held by `require_n_lumbar = 4`.")
    L.append("- VerSe read L6 persons whose VerSeFusion mask carries no id 25 (the split plan's `L6/audit_only` "
             "stratum, 36 persons across sides): held by `require_ids = [25]`; the read is the truth, the mask is not "
             "yet, and a rendered frame needs the mask.")
    L.append("- TotalSegmentator two-labeller L6 cases whose SPINEPS ctd names five lumbar (the 'rib-less T12' kind: "
             "s0158, s0477, s0683 per the stream's SUMMARY): held by `require_ids = [25]` if the ctd relabel did not "
             "write a 25.")
    L.append("")

    # ---- jobs
    if after:
        L.append(f"## Jobs (all ended; collected from disk {after['stamp']:%Y-%m-%d %H:%M}; collect step = "
                 f"`SchwingNet/slurm/rare_max_verify.sh`)")
        L.append("")
        L.append("The table below is the plan-time PENDING list, kept as the record of what was submitted and when. "
                 "Every array task ended (sacct: COMPLETED, except the two TotalSegmentator tasks that FAILED 5:0 at the "
                 "precheck in 11 s, listed under 'Stopped at the stage precheck' above) and the verify wrote its reports.")
        L.append("")
    else:
        L.append("## Jobs (PENDING list; collect step = `SchwingNet/slurm/rare_max_verify.sh`)")
        L.append("")
    if jobs:
        L.append("| job id | name | submitted | ETA | output | collected by |")
        L.append("|---|---|---|---|---|---|")
        for j in jobs:
            L.append(f"| {j['job']} | {j['name']} | {j['submitted']} | {j['eta']} | `{j['output']}` | {j['collect']} |")
        L.append("")
        for j in jobs:
            if j.get("estimate"):
                L.append(f"- {j['name']}: {j['estimate']}")
        L.append("")
    else:
        L.append("(not yet submitted)")
        L.append("")
    L.append("## Recipes per source (what each array does)")
    L.append("")
    for name, sp in SOURCES.items():
        L.append(f"- **{name}** -> `$RC/{sp['root']}`: layout `{sp['layout']}`, scheme `{sp['scheme']}`, patient_id "
                 f"`{sp['pid']}`, mask ids: {sp['mask_scheme']}; source `{sp['src']}`; "
                 f"{len(plan[name])} cases in `rare_max_{name}.json`.")
    L.append("")
    L.append("Staging (rare_max_stage.sh): CTSpinoPelvic1K links `<id>_ct.nii.gz` + `<id>_label.nii.gz` (same grid); "
             "TotalSegmentator links the v201 CT and resamples the native_ctd SPINEPS mask onto it by affine (nearest), "
             "then proves the alignment by the median HU under the mask (> 100) and the id order by "
             "`spineps_ids.assert_verse_monotonic`; CTSpine1K links the HF-mirror volume and its `_seg` annotation. "
             "A precheck failure stops that task with a named reason; the renderer's guard then judges the ids.")
    L.append("")
    L.append("## Identity note")
    L.append("")
    L.append("`tools/patient_keys.py` keys `ctsp_<id>_<view>_p<k>` and `totalseg_<s>_<view>_p<k>` stems today but only "
             "for lat/ap views; the oblique stems (`_obl_p<k>`) and the `ctspine1k_<stem>` scheme are NEW and unkeyed "
             "until its SCHEMES table gains `(?:lat|ap|obl)` and a ctspine1k rule. Every ann carries `patient_key` "
             "explicitly, so the split can key on the ann field; CHK-8 (coverage) will name these roots until the table "
             "is extended, and a bank must refuse them until then.")
    (out / "MAXIMIZE.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    raise SystemExit(main())
