#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: SchwingNet/tools/fig6_score.py. Tracked, unmodified at 097933a. KNOWN DEFECT (OPEN_QUESTIONS F3): reads T1/blinded/meta_ref/ where the open gate wrote T1/open/meta_ref/; fix before re-scoring.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""Figure 6 scorer: per person and per body, the level name from the NETWORK (the prototype's classifier name), from
the COUNT (the ordinary alphabet at the ordinal from the sacrum) and from the COUPLING (the best alphabet's name,
tools/alphabet_couple.py), against the reference name; per frame and per person, whether every reference-named body
was named right; the frame draw of SchwingNet/LEVELCHECK_MODEL.md s4 computed from truth alone.

WHAT IS SCORED (LEVELCHECK_MODEL.md s4, the matched endpoint)
  A frame is ELIGIBLE with at least four reference-named vertebral bodies; for a person in an at-risk stratum it must
  also be AT RISK: a reference-named body whose reference name differs from the ordinary alphabet's name at its
  ordinal counted up from the sacrum (convention i) or down from C1 (convention ii), read from the person's frozen
  alphabet (strata.json). A mechanism is CORRECT on a frame when every reference-named body is matched to a box and
  given its reference name; a missed body is wrong; for the count and the coupling a frame without an anchor is
  wrong (the count has no ordinal there, and the coupling's names are then the classifier's unchanged).
  Abstentions are counted beside the result (no tau was chosen for this model, so no low-margin stop exists).
THE DRAW. numpy.random.default_rng(20260923); persons in ascending key order; rng.integers(len(frames)) over the
person's eligible frames sorted by stem. Computed from the truth metas of BOTH gates, so it is fixed before any
prediction exists and the same whichever gate has been run. The primary draw covers the real-frame sets (T2, T3)
without the three C-ArmLSpine L6 patients; T1 (renders) and those three get draws of their own (secondary).
UNBLINDING. This scorer reads only the couple outputs it is given. It never runs a model.
THE REFERENCE STANDARD (LEVELCHECK_MODEL.md s4, s14 R3). With --truth-join (SchwingNet/tools/fig6_truth_join.py output)
  the truth is the frozen reference: the metas under --meta-subdir (meta_ref: reference names) and the couple outputs
  under --couple-subdir (couple_ref: bodies matched to those names). A real-frame person's stratum and alphabet come
  from the reference (human-verified truth first, else the s14 automated reference); a person with no reference is
  out of the primary pool and counted in the flow as `no_reference`. Results are also split by reference class
  (human / automated unanimous / automated rule), as s14 R3 requires. Without --truth-join the truth is the HARVEST
  name on the set metas (SPINEPS+VERIDAH, CBCT labellers), which is not a reference standard: label such a run.

    python SchwingNet/tools/fig6_score.py --sets /rs/.../fig6/sets --frozen /rs/.../fig6/frozen \\
        --runs /rs/.../fig6/eval --out SchwingNet/results/fig6/eval_open.json --gates open \\
        [--truth-join /rs/.../eval/truth_join_open.json --meta-subdir meta_ref --couple-subdir couple_ref --label reference]
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools"))
from sweep_map import alphabet  # noqa: E402

Z = 1.959963984540054
SEED_DRAW = 20260923
AT_RISK_STRATA = {"L6", "T13", "both", "sacralised_L5", "four_lumbar"}
MECH = {"network": "classifier", "count": "count", "coupled": "coupled"}


def wilson(k, n):
    if not n:
        return None
    p = k / n
    d = 1 + Z * Z / n
    c = (p + Z * Z / (2 * n)) / d
    h = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / d
    return [round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)]


def at_risk_names(al):
    """{reference name -> True if either convention names it differently} for one person's alphabet."""
    if not al:
        return {}
    col_p = alphabet(al["l6"], al["t13"], al["l4"])
    col_o = alphabet(False, False, False)
    out = {}
    for i, nm in enumerate(col_p):
        if nm == "sacrum":
            continue
        n_sac = len(col_p) - 1 - i
        by_sac = col_o[len(col_o) - 1 - n_sac] if n_sac < len(col_o) else None
        by_top = col_o[i] if i < len(col_o) else None
        out[nm] = (by_sac != nm) or (by_top != nm)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sets", required=True, help="fig6_sets.py output root (T1/T2/T3)")
    ap.add_argument("--frozen", required=True)
    ap.add_argument("--runs", required=True, help="eval root: <set>/<gate>/<variant>/couple/*.couple.json")
    ap.add_argument("--gates", default="open", help="gates whose couple outputs are read (open; open,blinded)")
    ap.add_argument("--variants", default="det74,det25,oracle,det74_lodo,det25_lodo",
                    help="variant dirs under <set>/<gate>/; a variant with no couple output is skipped")
    ap.add_argument("--out", required=True)
    ap.add_argument("--bodies-csv", default=None)
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--truth-join", default=None, help="fig6_truth_join.py output: the reference standard per person")
    ap.add_argument("--meta-subdir", default="meta", help="truth metas under <set>/<gate>/ (meta_ref with --truth-join)")
    ap.add_argument("--couple-subdir", default="couple", help="couple outputs under <set>/<gate>/<variant>/ (couple_ref ...)")
    ap.add_argument("--label", default=None, help="what the truth is (written as truth_standard)")
    a = ap.parse_args()

    sets = Path(a.sets)
    S = json.load(open(Path(a.frozen) / "strata.json"))
    strata, default = S["strata"], S["default"]
    gates = [g.strip() for g in a.gates.split(",") if g.strip()]
    # the reference standard per person (fig6_truth_join.py): stratum + alphabet override, primary eligibility
    J = json.load(open(a.truth_join))["persons"] if a.truth_join else {}
    join_sha = __import__("hashlib").sha256(open(a.truth_join, "rb").read()).hexdigest() if a.truth_join else None

    def person_truth(k, st):
        """(strata record, primary_eligible, reference class) for one person of one set."""
        s = strata.get(k, default)
        j = J.get(k)
        if j is None or st == "T1":
            return s, True, ("release" if st == "T1" else ("harvest" if not J else "not_in_join"))
        ref = j.get("reference")
        if ref is None:
            return s, False, "none"
        s2 = dict(s, stratum=ref["stratum"] if j.get("frozen_stratum") != "carmlspine_three_L6" else s["stratum"],
                  alphabet={"l6": ref["l6"], "t13": ref["t13"], "l4": ref.get("l4", False)})
        cls = ref["source"] if ref["source"] != "automated" else ("automated_unanimous" if ref.get("unanimous") else "automated_rule")
        return s2, bool(j.get("primary_eligible")), cls

    # ---------------------------------------------------------------- truth only: frames, eligibility, the draw
    frames = {}                      # (set, stem) -> truth record
    for st in ("T1", "T2", "T3"):
        pj = sets / st / "persons.json"
        if not pj.exists():
            continue
        persons = json.load(open(pj))
        for k, p in persons.items():
            s, prim, refcls = person_truth(k, st)
            risk = at_risk_names(s.get("alphabet"))
            for gate in ("open", "blinded"):
                for stem in p["frames"][gate]:
                    mp = sets / st / gate / a.meta_subdir / f"{stem}.json"
                    if not mp.exists():
                        raise SystemExit(f"no truth meta {mp} (run fig6_truth_join.py for this gate first)")
                    m = json.load(open(mp))
                    named = [b.get("level") for b in m.get("boxes", []) if b.get("cls") == 0 and b.get("level")]
                    three = s["stratum"] == "carmlspine_three_L6" and not named
                    # the three L6 patients' boxes carry no agreed level: their reference comes from the coupler's
                    # truth-variant rule, so their eligibility is read from the couple output (n_truth_named) later
                    # at_risk: the formal rule of LEVELCHECK_MODEL.md s3 (either convention). Its "in practice" gloss
                    # flags an L6 spine only "when the L6 body is on the frame"; the formal rule also flags an L6
                    # spine's L1-L5 (counted up from the sacrum they take the names one level up). The draw uses
                    # the formal rule; the gloss is recorded beside it so the G6 evaluator can see the difference.
                    frames[(st, stem)] = {"set": st, "stem": stem, "person": k, "gate": gate, "stratum": s["stratum"],
                                          "primary_eligible": prim, "reference_class": refcls,
                                          "n_named": len(named) if not three else None,
                                          "at_risk": any(risk.get(n, False) for n in named) if not three else None,
                                          "at_risk_gloss": (("L6" in named) if s["stratum"] == "L6" else
                                                            any(risk.get(n, False) for n in named)) if not three else None,
                                          "real": st != "T1"}

    def eligible(fr):
        if fr["n_named"] is None:
            return None
        if fr["n_named"] < 4:
            return False
        return fr["at_risk"] if fr["stratum"] in AT_RISK_STRATA else True

    def draw(pool):
        by = defaultdict(list)
        for fr in pool:
            if eligible(fr):
                by[fr["person"]].append(fr["stem"])
        rng = np.random.default_rng(SEED_DRAW)
        out = {}
        for k in sorted(by):
            fl = sorted(by[k])
            out[k] = fl[int(rng.integers(len(fl)))]
        return out

    # ---------------------------------------------------------------- the flow: who is in each set, and why not
    flow = {}
    for st in ("T1", "T2", "T3"):
        pj = sets / st / "persons.json"
        if not pj.exists():
            continue
        tab = defaultdict(lambda: {"persons": 0, "persons_with_frames": 0, "withheld_persons_by_reason": Counter()})
        for k, p in json.load(open(pj)).items():
            t = tab[p["stratum"]]
            t["persons"] += 1
            n = len(p["frames"]["open"]) + len(p["frames"]["blinded"])
            t["persons_with_frames"] += int(n > 0)
            if n == 0:
                for r in (p.get("withheld") or {}):
                    t["withheld_persons_by_reason"][r] += 1
        flow[st] = {s_: dict(v, withheld_persons_by_reason=dict(v["withheld_persons_by_reason"])) for s_, v in sorted(tab.items())}
        if J and st != "T1":
            # the reference standard's own flow: who has one, from where, and why the others do not (s14 R3)
            ref = Counter(); why = Counter(); moved = Counter()
            for k, p in json.load(open(pj)).items():
                j = J.get(k)
                if j is None:
                    ref["not_in_join"] += 1; continue
                _, prim, cls = person_truth(k, st)
                ref[cls] += 1
                if not prim:
                    why[(j.get("no_reference_reason") or "excluded in advance").split(":")[0][:80]] += 1
                if j.get("reference") and j["reference"].get("stratum") != j.get("frozen_stratum"):
                    moved[f"{j.get('frozen_stratum')}->{j['reference']['stratum']}"] += 1
            flow[st]["_reference"] = {"persons_by_reference_class": dict(ref), "no_reference_by_reason": dict(why),
                                      "stratum_frozen_to_reference": dict(moved)}
    sets_summary = json.load(open(sets / "SETS.json")) if (sets / "SETS.json").exists() else None

    primary_pool = [f for f in frames.values() if f["real"] and f["stratum"] != "carmlspine_three_L6" and f["primary_eligible"]]
    draws = {"primary_real": draw(primary_pool),
             "T1_renders": draw([f for f in frames.values() if f["set"] == "T1"])}

    # ---------------------------------------------------------------- predictions
    bodies_rows = []
    results = {}
    for st in ("T1", "T2", "T3"):
        for gate in gates:
            for var in [v.strip() for v in a.variants.split(",") if v.strip()]:
                cdir = Path(a.runs) / st / gate / var / a.couple_subdir
                if not (cdir / "couple_all.json").exists():
                    continue
                ca = json.load(open(cdir / "couple_all.json"))
                per_frame = {}
                for r in ca["frames"]:
                    stem = r["stem"]
                    fr = frames.get((st, stem))
                    if fr is None:
                        continue
                    anchored = r["call"] not in ("no anchor", "no alphabet")
                    named = [b for b in r["bodies"] if b.get("truth")]
                    n_named = int(r.get("n_truth_named") or 0)
                    res = {}
                    for mname, field in MECH.items():
                        ok = (len(named) == n_named and n_named > 0 and all(b.get(field) == b["truth"] for b in named))
                        if mname in ("count", "coupled") and not anchored:
                            ok = False
                        res[mname] = bool(ok)
                    per_frame[stem] = {"person": fr["person"], "stratum": fr["stratum"], "n_truth_named": n_named,
                                       "n_matched_named": len(named), "anchored": anchored, "call": r["call"],
                                       "abstentions": sum(1 for b in r["bodies"] if b.get("abstain")),
                                       "eligible": eligible(fr) if fr["n_named"] is not None else (n_named >= 4),
                                       "primary_eligible": fr["primary_eligible"], "reference_class": fr["reference_class"],
                                       "correct": res, "truth_source": r.get("truth_source")}
                    for b in r["bodies"]:
                        bodies_rows.append({"set": st, "gate": gate, "variant": var, "person": fr["person"],
                                            "stratum": fr["stratum"], "frame": stem, "i": b["i"], "ordinal": b.get("ordinal"),
                                            "truth": b.get("truth"), "network": b.get("classifier"),
                                            "count": b.get("count"), "coupled": b.get("coupled"),
                                            "call": r["call"], "abstain": b.get("abstain")})
                # per person: the drawn frame (primary for real sets, T1 draw for renders; the three L6 on all frames)
                dr = draws["T1_renders"] if st == "T1" else draws["primary_real"]
                by_st = defaultdict(lambda: {m: [0, 0] for m in MECH})
                by_ref = defaultdict(lambda: {m: [0, 0] for m in MECH})      # (stratum | reference class), s14 R3
                per_person = {}
                for k in sorted({v["person"] for v in per_frame.values()}):
                    stem = dr.get(k)
                    if stem is None or stem not in per_frame:
                        continue
                    pf = per_frame[stem]
                    per_person[k] = {"frame": stem, "stratum": pf["stratum"], "correct": pf["correct"],
                                     "reference_class": pf["reference_class"]}
                    for m in MECH:
                        by_st[pf["stratum"]][m][0] += int(pf["correct"][m]); by_st[pf["stratum"]][m][1] += 1
                        by_ref[f"{pf['stratum']}|{pf['reference_class']}"][m][0] += int(pf["correct"][m])
                        by_ref[f"{pf['stratum']}|{pf['reference_class']}"][m][1] += 1
                def tab_(d_):
                    return {m: {"k": kk, "n": nn, "acc": round(kk / nn, 4) if nn else None, "wilson95": wilson(kk, nn)}
                            for m, (kk, nn) in d_.items()}
                summ = {s_: tab_(d) for s_, d in sorted(by_st.items())}
                summ_ref = {s_: tab_(d) for s_, d in sorted(by_ref.items())}
                # every eligible frame, person-clustered bootstrap (secondary)
                allf = defaultdict(list)
                for stem, pf in per_frame.items():
                    if pf["eligible"]:
                        allf[pf["person"]].append(pf)
                boot = {}
                if allf:
                    ppl = sorted(allf)
                    rng = np.random.default_rng(0)
                    for m in MECH:
                        kk = sum(f["correct"][m] for k in ppl for f in allf[k]); nn = sum(len(allf[k]) for k in ppl)
                        vals = []
                        for _ in range(a.boot):
                            idx = rng.integers(len(ppl), size=len(ppl))
                            kb = sum(sum(f["correct"][m] for f in allf[ppl[i]]) for i in idx)
                            nb = sum(len(allf[ppl[i]]) for i in idx)
                            vals.append(kb / nb if nb else 0.0)
                        boot[m] = {"k": kk, "n": nn, "persons": len(ppl), "acc": round(kk / nn, 4) if nn else None,
                                   "pct95": [round(float(np.percentile(vals, 2.5)), 4), round(float(np.percentile(vals, 97.5)), 4)]}
                results[f"{st}|{gate}|{var}"] = {
                    "set": st, "gate": gate, "variant": var, "prototype_meta": {k: ca["prototype_meta"].get(k) for k in (
                        "level_model", "level_model_sha256", "head", "detector", "detector_sha256", "sacrum_detector",
                        "sacrum_detector_sha256", "eval_gate")},
                    "couple_args": ca.get("args"), "frames": len(per_frame),
                    "eligible_frames": sum(1 for v in per_frame.values() if v["eligible"]),
                    "anchored_frames": sum(1 for v in per_frame.values() if v["anchored"]),
                    "per_person_drawn_frame": summ, "per_person_drawn_frame_by_reference_class": summ_ref,
                    "per_person": per_person,
                    "all_eligible_frames_person_bootstrap": boot, "per_frame": per_frame}
    out = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "tool": "SchwingNet/tools/fig6_score.py", "gates_read": gates,
           "truth_standard": a.label or ("reference standard (fig6_truth_join.py: human-verified first, else the s14 automated "
                                         "reference; persons without one excluded)" if J else
                                         "HARVEST names on the set metas (SPINEPS+VERIDAH / CBCT labellers): not a reference standard"),
           "truth_join": {"path": a.truth_join, "sha256": join_sha} if a.truth_join else None,
           "meta_subdir": a.meta_subdir, "couple_subdir": a.couple_subdir,
           "frozen_strata_sha256": __import__("hashlib").sha256(open(Path(a.frozen) / "strata.json", "rb").read()).hexdigest(),
           "draw_rule": "numpy.random.default_rng(20260923); persons ascending; rng.integers(len(frames)) over eligible "
                        "frames sorted by stem; truth only; primary pool = T2+T3 without carmlspine_three_L6"
                        + (" and without persons that have no reference standard (truth join)" if J else ""),
           "flow": flow, "sets_summary": sets_summary,
           "draws": draws, "results": results,
           "truth_frames": {f"{k[0]}|{k[1]}": v for k, v in frames.items()}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    if a.bodies_csv:
        with open(a.bodies_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(bodies_rows[0].keys()) if bodies_rows else ["set"])
            w.writeheader()
            w.writerows(bodies_rows)
    for key, r in results.items():
        print(key, "frames", r["frames"], "eligible", r["eligible_frames"], "anchored", r["anchored_frames"])
        for s_, d in r["per_person_drawn_frame"].items():
            print("   ", s_, {m: f"{v['k']}/{v['n']}" for m, v in d.items()})
    print(f"wrote {a.out}; draws: primary {len(draws['primary_real'])} persons, T1 {len(draws['T1_renders'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
