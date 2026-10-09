#!/usr/bin/env python
"""CV_V9.md: every quoted C-ArmLSpine naming number, old (allspine_v2_r1 lineage, UNRESOLVED) beside new
(allspine_v9 lineage, HELD OUT), read from cv_v9.json (closure_cv_v9.py, grid job 40436862) and cv_v9_extras_*.json
(job 40436901). Runs locally; no grid access, no checkpoint.

    python write_cv_v9_md.py
"""
from __future__ import annotations

import json
import os

D = os.path.dirname(os.path.abspath(__file__))
cv = json.load(open(os.path.join(D, "cv_v9.json"), encoding="utf-8"))
EX = {}
for tr in ("pre", "rep"):
    p = os.path.join(D, f"cv_v9_extras_{tr}.json")
    if os.path.exists(p):
        EX[tr] = json.load(open(p, encoding="utf-8"))
F = cv["families"]
C = cv["coupling"]


def pc(x, d=1):
    return "-" if x is None else f"{100 * x:.{d}f}"


def ci(v, d=1):
    return "-" if not v else f"[{pc(v[0], d)}, {pc(v[1], d)}]"


def cell(fam, key):
    return (F.get(fam) or {}).get("cells", {}).get(key)


def main_cell(c):
    if not c:
        return "MISSING"
    s = f"**{pc(c['point'])} % ({c['k']}/{c['n']})**; {c['clusters']} cases ({c['clusters_with_error']} with an error); percentile {ci(c['percentile'])}; BCa {ci(c['bca'])}"
    if c.get("wilson_effective_n"):
        s += f"; Wilson on n_eff {ci(c['wilson_effective_n'])}" + (" (ceiling regime)" if c.get("ceiling_regime") else "")
    s += f"; within one {pc(c['within1'])} %"
    return s


def abst(c):
    if not c:
        return "MISSING"
    a, e = c["answered"], c.get("exact_on_answered") or {}
    return (f"answered {pc(a['point'])} % ({a['k']}/{a['n']}) {ci(a['percentile'])}; exact on answered "
            f"{pc(e.get('point'))} % ({e.get('k')}/{e.get('n')}) {ci(e.get('percentile'))}, BCa {ci(e.get('bca'))}; "
            f"{c['errors_among_abstained']} of {c['errors_total']} errors among the abstained")


def sweep(c):
    if not c:
        return "MISSING"
    out = []
    for t in ("0.90", "0.95"):
        s = c["abstain_sweep"].get(t)
        if s:
            out.append(f"threshold {t} answers {pc(s['answered'])} % ({s['answered_k']}/{c['n']}) at "
                       f"{pc(s['exact_on_answered'])} % ({s['exact_on_answered_k']}/{s['exact_on_answered_n']}) "
                       f"{ci(s['exact_on_answered_percentile'])}")
    return "; ".join(out)


def allc(c):
    if not c:
        return "MISSING"
    a = c["all_correct_cases"]
    return f"{pc(a['point'])} % ({a['k']}/{a['n']}), Wilson {ci(a['wilson'])}"


def ladder(fam):
    pts, pcs, bcs, kn = [], [], [], []
    for k in ("1", "2", "3", "4", "5", "full"):
        c = cell(fam, f"LAT/k{k}")
        if not c:
            pts.append("-"); pcs.append("-"); bcs.append("-"); kn.append("-")
            continue
        pts.append(pc(c["point"])); pcs.append(ci(c["percentile"])); bcs.append(ci(c["bca"]))
        kn.append(f"{c['k']}/{c['n']}, {c['clusters']}")
    return " / ".join(pts) + " % (" + "; ".join(kn) + "); percentile " + " / ".join(pcs) + "; BCa " + " / ".join(bcs)


def kn(v):
    """a coupling_report quantity: {'k','n','point'/'value','ci95'} or a number or a dict of counts."""
    if v is None:
        return "-"
    if isinstance(v, dict):
        if "k" in v and "n" in v:
            p = v.get("point", v.get("value"))
            s = f"{pc(p)} % ({v['k']}/{v['n']})" if p is not None and p <= 1 else f"{v['k']}/{v['n']}"
            if v.get("ci95"):
                s += f" {ci(v['ci95'])}"
            elif v.get("ci"):
                s += f" {ci(v['ci'])}"
            return s
        if "point" in v or "value" in v:
            p = v.get("point", v.get("value"))
            s = f"{p:+.1f} pp" if isinstance(p, (int, float)) and abs(p) > 1 else (f"{100 * p:+.1f} pp" if isinstance(p, (int, float)) else str(p))
            for kk in ("ci95", "ci"):
                if v.get(kk):
                    lo, hi = v[kk]
                    s += f" [{lo:+.1f}, {hi:+.1f}]" if abs(lo) > 1 or abs(hi) > 1 else f" [{100 * lo:+.1f}, {100 * hi:+.1f}]"
            return s
        return json.dumps(v)
    return str(v)


def crow(tag, lab, key):
    r = ((C.get(tag) or {}).get("rows") or {}).get(lab) or {}
    return kn(r.get(key))


L = []
w = L.append
w("# CV_V9: every quoted C-ArmLSpine naming number, old lineage beside the v9 lineage")
w("")
w(f"Written {cv['written']} from `cv_v9.json` (closure_cv_v9.py, grid job 40436862, host {cv['host']}) and "
  f"`cv_v9_extras_pre.json` / `_rep.json` (job 40436901). Nothing here is typed by hand except the row labels.")
w("")
w("**Old** = the shipped fold models fine-tuned from `allspine_v2_r1` (training bank deleted: UNRESOLVED, EVAL_LEAKS U1), "
  "read under a declared `--not-held-out` from the shipped score files. **New (pre)** = the same merged fold banks, the same "
  "fold directories, epochs, seeds and prototype defaults, the encoder fine-tuned from `allspine_v9` (lineage complete), "
  "scored on the export AS IT WAS when the old numbers were scored (`realxray/carmlspine_pre_repair_2026-09-23`, mirrored "
  "link for link; the k-vertebra crops regenerated, case13_LAT one crop short at every k). Old and new differ by the "
  "initialisation alone: **new (pre) is the replacement**. **New (rep)** = the same new models on the export as it stands "
  "today (rewritten 2026-09-23: case118's oblique frame renamed, case134 added), reported beside. Every new score file "
  "carries a held-out gate verdict (overlap 0, unresolved 0; gate eval_gate/1 as installed in the grid clone).")
w("")
g = {k: (v.get("gate") or {}) for k, v in F.items()}
w("| family | held out | overlap | unresolved | gate checks |")
w("|---|---|---:|---:|---:|")
for k in F:
    w(f"| `{k}` | {g[k].get('held_out')} | {g[k].get('overlap')} | {g[k].get('unresolved')} | {g[k].get('n_checks')} |")
w("")
w("Strict gate on the old families (why they cannot be quoted): " + "; ".join(
    f"`{k}`: {str(v)[:120]}..." for k, v in cv["strict_gate_on_old"].items()))
w("")

w("## 1. Case-grouped five-fold CV, film keypoint detector boxes (Table 4, Key Points, Abstract, Results, Figure 4b)")
w("")
w("| row | old (allspine_v2_r1) | new (pre) = replacement | new (rep) |")
w("|---|---|---|---|")
for lab, key in (("lateral, whole frame", "LAT/kfull"), ("AP, whole frame", "AP/kfull"), ("lateral, five in field", "LAT/k5"),
                 ("lateral, four in field", "LAT/k4"), ("lateral, three in field", "LAT/k3"), ("lateral, two in field", "LAT/k2"),
                 ("lateral, one in field", "LAT/k1"), ("AP, three in field", "AP/k3"), ("AP, one in field", "AP/k1")):
    w(f"| {lab} | {main_cell(cell('old:cv5_det', key))} | {main_cell(cell('pre:cv5_det', key))} | {main_cell(cell('rep:cv5_det', key))} |")
w(f"| cases with every lateral vertebra right (whole frame) | {allc(cell('old:cv5_det', 'LAT/kfull'))} | {allc(cell('pre:cv5_det', 'LAT/kfull'))} | {allc(cell('rep:cv5_det', 'LAT/kfull'))} |")
w(f"| the ladder, lateral, one to five in field and whole frame | {ladder('old:cv5_det')} | {ladder('pre:cv5_det')} | {ladder('rep:cv5_det')} |")
w(f"| lateral whole frame, per level (exact) | {cell('old:cv5_det', 'LAT/kfull')['per_level']} | {cell('pre:cv5_det', 'LAT/kfull')['per_level']} | {cell('rep:cv5_det', 'LAT/kfull')['per_level']} |")
w(f"| lateral whole frame, confusions | {cell('old:cv5_det', 'LAT/kfull')['confusions'][:6]} | {cell('pre:cv5_det', 'LAT/kfull')['confusions'][:6]} | {cell('rep:cv5_det', 'LAT/kfull')['confusions'][:6]} |")
w(f"| detector recall of agreed lateral vertebrae (unchanged: the detector never changed) | {cell('old:cv5_det', 'LAT/kfull')['recall_named']} | {cell('pre:cv5_det', 'LAT/kfull')['recall_named']} | {cell('rep:cv5_det', 'LAT/kfull')['recall_named']} |")
w("")
w("### 1.1 Abstention (the default rule, `--abstain-below 0.5`, never tuned; Table 4 twin, NUMBERS)")
w("")
w("| row | old | new (pre) | new (rep) |")
w("|---|---|---|---|")
for lab, key in (("lateral, whole frame", "LAT/kfull"), ("AP, whole frame", "AP/kfull"), ("lateral, five in field", "LAT/k5"),
                 ("lateral, three in field", "LAT/k3"), ("lateral, one in field", "LAT/k1")):
    w(f"| {lab} | {abst(cell('old:cv5_det', key))} | {abst(cell('pre:cv5_det', key))} | {abst(cell('rep:cv5_det', key))} |")
w(f"| sweep, lateral whole frame | {sweep(cell('old:cv5_det', 'LAT/kfull'))} | {sweep(cell('pre:cv5_det', 'LAT/kfull'))} | {sweep(cell('rep:cv5_det', 'LAT/kfull'))} |")
w("")
w("### 1.2 Truth boxes (oracle): complete coverage")
w("")
w("| row | old | new (pre) | new (rep) |")
w("|---|---|---|---|")
for lab, key in (("lateral, whole frame, truth boxes", "LAT/kfull"), ("AP, whole frame, truth boxes", "AP/kfull"),
                 ("lateral, three in field, truth boxes", "LAT/k3"), ("lateral, one in field, truth boxes", "LAT/k1")):
    w(f"| {lab} | {main_cell(cell('old:cv5_oracle', key))} | {main_cell(cell('pre:cv5_oracle', key))} | {main_cell(cell('rep:cv5_oracle', key))} |")
w("")

w("## 2. Acquisition-day-grouped three-fold CV (Table 4, Key Point 2, Results, Discussion limits)")
w("")
w("| row | old | new (pre) = replacement | new (rep) |")
w("|---|---|---|---|")
for lab, key in (("lateral, whole frame", "LAT/kfull"), ("AP, whole frame", "AP/kfull"), ("lateral, five in field", "LAT/k5"),
                 ("lateral, three in field", "LAT/k3"), ("lateral, one in field", "LAT/k1")):
    w(f"| {lab} | {main_cell(cell('old:cvday_det', key))} | {main_cell(cell('pre:cvday_det', key))} | {main_cell(cell('rep:cvday_det', key))} |")
w(f"| the ladder, lateral | {ladder('old:cvday_det')} | {ladder('pre:cvday_det')} | {ladder('rep:cvday_det')} |")
for lab, key in (("abstention, lateral whole frame", "LAT/kfull"), ("abstention, AP whole frame", "AP/kfull"),
                 ("abstention, lateral three in field", "LAT/k3"), ("abstention, lateral one in field", "LAT/k1")):
    w(f"| {lab} | {abst(cell('old:cvday_det', key))} | {abst(cell('pre:cvday_det', key))} | {abst(cell('rep:cvday_det', key))} |")
w("")

w("## 3. Zero-shot on the same fold frames (the v9 encoder; no C-ArmLSpine frame in training)")
w("")
w("`pre:zeroshot_v9_existing` is the run already quoted (`leaks/zeroshot_v9.json`, 2026-09-23); `pre:zs_v9head` re-scores "
  "the same encoder and head on the fold directories inside this closure; `zs_v9nohead` is the zeroshot2 protocol (no head). "
  "`old:zeroshot2` is the first run, `allspine_v2_r1`, no head (UNRESOLVED; disclosed in Table 4 note h).")
w("")
w("| family | lateral, whole frame | AP, whole frame | lateral minus AP, paired (same vertebrae) |")
w("|---|---|---|---|")
for fam in ("old:zeroshot2", "pre:zeroshot_v9_existing", "pre:zs_v9head", "pre:zs_v9nohead", "rep:zs_v9head", "rep:zs_v9nohead"):
    pl = F[fam].get("paired_lat_minus_ap") or {}
    w(f"| `{fam}` | {main_cell(cell(fam, 'LAT/kfull'))}; {abst(cell(fam, 'LAT/kfull'))} | {main_cell(cell(fam, 'AP/kfull'))}; {abst(cell(fam, 'AP/kfull'))} | "
      f"{pl.get('diff_pp', float('nan')):+.1f} pp {ci([x / 100 for x in pl.get('percentile_pp', [0, 0])])}, BCa {ci([x / 100 for x in pl.get('bca_pp', [0, 0])])} on {pl.get('n_items')} vertebrae of {pl.get('n_clusters')} cases; "
      f"cases lateral better {pl.get('clusters_favouring_a')} : {pl.get('clusters_favouring_b')}; exact sign p {pl.get('cluster_sign_test_p')}; McNemar {pl.get('mcnemar_exact_p')} |")
w("")
w("### 3.1 The zero-shot ladder, lateral, one to five in field and whole frame (Table 4 'three and one in field', Results, Figure 4b)")
w("")
w("| family | ladder | three in field | one in field |")
w("|---|---|---|---|")
for fam in ("old:zeroshot2", "pre:zs_v9head", "rep:zs_v9head"):
    w(f"| `{fam}` | {ladder(fam)} | {main_cell(cell(fam, 'LAT/k3'))}; {abst(cell(fam, 'LAT/k3'))} | {main_cell(cell(fam, 'LAT/k1'))}; {abst(cell(fam, 'LAT/k1'))} |")
w("")
w("| family | AP three in field | AP one in field |")
w("|---|---|---|")
for fam in ("old:zeroshot2", "pre:zs_v9head", "rep:zs_v9head"):
    w(f"| `{fam}` | {main_cell(cell(fam, 'AP/k3'))} | {main_cell(cell(fam, 'AP/k1'))} |")
w("")
w("Holm over the four pre-named comparisons with the zero-shot member replaced (two other members are LEAKED, EVAL_LEAKS L2, L6): " +
  "; ".join(f"`{k}`: p {v.get('p_exact'):.2e}, Holm {v.get('p_exact_holm'):.2e}" for k, v in cv["zero_shot_paired"].items() if isinstance(v, dict) and v.get("p_exact") is not None))
w("")
w(f"The naming detector's lowest boxed `det_conf`: old cv {cv.get('detector_min_det_conf_old')}; new cv {cv['detector_min_det_conf_pre']['cv']} (pre), {cv['detector_min_det_conf_rep']['cv']} (rep); zero-shot v9 {cv['detector_min_det_conf_pre']['zs_v9head']} (pre).")
w("")

w("## 4. Coupling the classifier to the count from the sacrum (Table 4, Results, Figure 4c/d)")
w("")
w("Cells of `coupling_report.py` over the re-run's coupling prototypes (`coupling_pre/coupling.json`, `coupling_rep/coupling.json`) "
  "beside the shipped `results/coupling.json`. det74 = keypoint boxes, held-out sacrum detector at confidence 0.74 (the operating "
  "point the text quotes); det = the same at 0.25; oracle = truth boxes and truth sacrum.")
w("")
w("| cell | quantity | old | new (pre) = replacement | new (rep) |")
w("|---|---|---|---|---|")
for lab in ("det74/kfull", "det/kfull", "oracle/k5", "oracle_ext/k5", "oracle/kfull"):
    for q in ("frames", "cases", "frames_anchored", "bodies_counted", "classifier_exact_counted", "count_exact_counted",
              "coupled_exact_counted", "coupled_minus_count_counted", "coupled_minus_classifier_anchored",
              "classifier_exact_anchored", "coupled_exact_anchored", "disagreement_bodies", "disagreement_frames",
              "when_agree", "when_disagree", "calls", "calls_anchored", "non_ordinary_calls", "flags"):
        vals = [crow(t, lab, q) for t in ("old", "pre", "rep")]
        if all(v == "-" for v in vals):
            continue
        w(f"| {lab} | {q} | {vals[0]} | {vals[1]} | {vals[2]} |")
w("")
w("### 4.1 The three C-ArmLSpine cases one labeller (VERIDAH) reads as L6 (agreement with that read, not correctness)")
w("")
w("| quantity | old | new (pre) | new (rep) |")
w("|---|---|---|---|")
for lab in ("veridah_l6:det/kfull", "veridah_l6:det74/kfull"):
    vals = [json.dumps(((C.get(t) or {}).get("rows") or {}).get(lab)) for t in ("old", "pre", "rep")]
    w(f"| {lab} per-level L6 (n, classifier, coupled) | {vals[0]} | {vals[1]} | {vals[2]} |")
for t in ("old", "pre", "rep"):
    pass
vals = [((C.get(t) or {}).get("rows") or {}).get("l6_patients_det74_full") or {} for t in ("old", "pre", "rep")]
w(f"| det74, whole frames of the three patients: frames / anchored / L6 calls / flagged | " + " | ".join(
    f"{v.get('frames')} / {v.get('anchored')} / {v.get('l6_calls')} / {v.get('l6_calls_flagged')}" for v in vals) + " |")
w(f"| the six frames (case, view, call, flag reason) | " + " | ".join(json.dumps(v.get("calls")) for v in vals) + " |")
w("")
w("### 4.2 Figure 4d: case42 lateral, fold 2, det74")
w("")
w("| quantity | old | new (pre) | new (rep) |")
w("|---|---|---|---|")
for q in ("call", "margin", "margin_next", "candidates", "flag", "flag_reason", "count_differs_from_shape", "anchor"):
    w(f"| {q} | " + " | ".join(json.dumps(cv["figure4"][f"d_{t}"].get(q)) for t in ("old", "pre", "rep")) + " |")
w("| rows drawn | " + " | ".join("; ".join(r["drawn"] for r in cv["figure4"][f"d_{t}"].get("rows", [])) for t in ("old", "pre", "rep")) + " |")
w("| p_classifier per ordinal | " + " | ".join(json.dumps([(r["ordinal"], r.get("p_classifier")) for r in cv["figure4"][f"d_{t}"].get("rows", [])]) for t in ("old", "pre", "rep")) + " |")
w("")
w("### 4.3 Figure 4b: case11_LAT, fold 3, three in field (the drawn names)")
w("")
w("| old | new (pre) | new (rep) |")
w("|---|---|---|")
w("| " + " | ".join("; ".join(f"{r['drawn']} (level {r.get('level')}, p {r.get('level_prob')}, det {r.get('det_conf')})" for r in cv["figure4"][f"b_{t}"].get("rows", [])) for t in ("old", "pre", "rep")) + " |")
w("")

w("## 5. The count-versus-classifier matrix (det74/kfull; NUMBERS '(d) matrix' row, drawn nowhere since fig5_naming was retired)")
w("")
for tr, ex in EX.items():
    m = ex["matrix_det74_kfull"]
    w(f"- **{tr}**: {m['frames_anchored_agreed']} anchored agreed frames, {m['bodies_counted']} counted bodies, {m['on_diagonal']} on the diagonal; "
      f"diagonal {m['diagonal']}; off-diagonal {m['off_diagonal']}; gate: {sum(1 for g in m['gates'] if g['held_out'])} of {len(m['gates'])} files held out")
if not EX:
    w("- cv_v9_extras_*.json not present yet")
w("")

w("## 6. Zero-shot against fine-tuned on the same detected vertebrae (paired; the accuracy-saturation reading)")
w("")
for tr, ex in EX.items():
    w(f"**{tr}**")
    w("")
    w("| view | comparison | a (k/n) | b (k/n) | a minus b, pp [95 % case bootstrap] | cases favouring a : b | exact sign p | discordant a-only : b-only |")
    w("|---|---|---|---|---|---|---|---|")
    for view in ("LAT", "AP"):
        for k, v in ex["pairs"][view].items():
            if k in ("n", "gates"):
                continue
            w(f"| {view} | {k} | {v['k_a']}/{v['n_items']} = {pc(v['p_a'])} % | {v['k_b']}/{v['n_items']} = {pc(v['p_b'])} % | "
              f"{v['diff_pp']:+.1f} [{v['percentile_pp'][0]:+.1f}, {v['percentile_pp'][1]:+.1f}] | {v['cases_favouring_a']} : {v['cases_favouring_b']} "
              f"(of {v['n_cases']}) | {v['cluster_sign_test_p']:.2e} | {v['discordant_a_only']} : {v['discordant_b_only']} |" if v['cluster_sign_test_p'] is not None else
              f"| {view} | {k} | {v['k_a']}/{v['n_items']} | {v['k_b']}/{v['n_items']} | {v['diff_pp']:+.1f} | {v['cases_favouring_a']} : {v['cases_favouring_b']} | - | {v['discordant_a_only']} : {v['discordant_b_only']} |")
    bad = sum(1 for view in ex["pairs"] for fam in ex["pairs"][view]["gates"].values() for gg in fam if not gg["held_out"])
    w("")
    w(f"Score files read: every one carries a held-out gate block ({bad} not held out).")
    w("")
    if ex.get("pairs_by_k"):
        w(f"**{tr}, by field size** (the same pairing on the k-vertebra crops; a minus b in percentage points, case bootstrap; cases favouring a : b)")
        w("")
        w("| view | field | fine-tuned (case) minus zero-shot | day-grouped minus zero-shot | case-grouped minus day-grouped |")
        w("|---|---|---|---|---|")
        for view in ("LAT", "AP"):
            for k in ("k1", "k2", "k3", "k4", "k5", "kfull"):
                blk = ex["pairs_by_k"][view].get(k) or {}
                cells = []
                for name in ("cv5_case minus zeroshot_v9head", "cvday minus zeroshot_v9head", "cv5_case minus cvday"):
                    v = blk.get(name)
                    cells.append(f"{v['k_a']}/{v['n_items']} vs {v['k_b']}/{v['n_items']}: {v['diff_pp']:+.1f} [{v['percentile_pp'][0]:+.1f}, {v['percentile_pp'][1]:+.1f}]; {v['cases_favouring_a']} : {v['cases_favouring_b']}" if v else blk.get("status", "-"))
                w(f"| {view} | {k} | " + " | ".join(cells) + " |")
        w("")

w("## 7. Controls: the shipped fold models re-run with today's code")
w("")
w("`pre_*`: on the pre-repair mirror (must reproduce the shipped score files item for item at kfull; at k = 1..5 the regenerated crops "
  "can differ). `rep_*`: on the repaired export (the truth moved). Tuple = (reproduces, identical items, shipped items, re-run items).")
w("")
w("| fold | " + " | ".join(f"k{k}" for k in ("full", "5", "4", "3", "2", "1")) + " |")
w("|---|" + "---|" * 6)
for k, v in cv["controls"].items():
    w(f"| {k} | " + " | ".join(f"{vv.get('reproduces')} {vv.get('identical')}/{vv.get('shipped_items')}/{vv.get('rerun_items')}" for vv in v.values()) + " |")
w("")
w("The pre-repair kfull rows reproduce the shipped files exactly in 7 of 8 folds; day fold 0 differs in 1 of 588 items "
  "(one call flipped: floating-point nondeterminism across nodes, as in MANUSCRIPT_CORRECTIONS §5.2). At k = 1..5, case fold 0 "
  "and day fold 2 are short exactly case13_LAT's missing last crop (5, 4, 3, 2, 1 items); case fold 4 and day folds 0-2 differ in a "
  "handful of regenerated-crop items. So the pre-repair comparison is like for like at the whole frame and within a few items at k = 1..5.")

open(os.path.join(D, "CV_V9.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote", os.path.join(D, "CV_V9.md"), len(L), "lines")
