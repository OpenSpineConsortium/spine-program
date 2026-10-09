#!/usr/bin/env python
"""Fill the GENERATED blocks of SchwingNet/results/eval_gate/EVAL_LEAKS.md from CHK-9 and the re-scores beside it.

Reads (all in the repo; the grid copies are pulled beside them):
  ../quoted_results.json       every quoted number and the (checkpoint, evaluation set) pairs behind it (build_inventory.py)
  ../chk9/chk9_report.json     tools/leak_check.py chk9 over those rows (grid job; the log is chk9/job_<id>.log)
  ./*.json                     the re-reads and reruns of the LEAKED rows (this directory; each script says what it is)
Only the blocks between <!-- BEGIN:GENERATED <name> --> and <!-- END:GENERATED <name> --> are rewritten.

    python SchwingNet/results/eval_gate/leaks/build_eval_leaks.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
EG_DIR = HERE.parent
MD = EG_DIR / "EVAL_LEAKS.md"
VERDICT = {"HELD OUT": "CLEAN", "SEEN": "LEAKED", "UNRESOLVED": "UNRESOLVED", "NO EVAL KEYS": "UNRESOLVED",
           "DECLARED": "DECLARED", "N/A": "N/A"}
# where each family's LEAKED / UNRESOLVED rows are dealt with in the hand-written sections
FAMILY_SECTION = {"arc": "L1", "render_vs_film": "L2", "lcurve": "L3", "film_naming_v8": "L4", "embedding_v9": "L5",
                  "device_cards": "L6", "fig4a_pairs": "L7", "count_only": "L2", "carm_zeroshot": "U1", "carm_cv_naming": "U1",
                  "carm_cvday_naming": "U1", "carm_cv_oracle": "U1", "coupling": "U1", "card_refit": "U2"}


def load(p):
    p = Path(p)
    return json.load(open(p, encoding="utf-8")) if p.exists() else None


def short_ck(p):
    p = str(p or "")
    for cut in ("/runs/", "go2432/"):
        if cut in p:
            p = p.split(cut, 1)[1]
    return p.replace("/weights/best.pt", "").replace("/model_rung_1_aug2.pt", "")


def pct(x, d=1):
    return "-" if x is None else f"{100 * x:.{d}f}"


def ci(v, d=1):
    return "-" if not v else f"[{100 * v[0]:.{d}f}, {100 * v[1]:.{d}f}]"


def row_why(r):
    """One line: what decided the row."""
    out = []
    for p in r.get("pairs") or []:
        if p["verdict"] == "HELD OUT":
            continue
        if p.get("why") and not p.get("instances"):
            out.append(f"{p.get('checkpoint')}: {p['why'][:220]}")
            continue
        ck = str(p.get("checkpoint") or "")
        if ck.startswith("card_median:"):
            n = len(p.get("instances") or [])
            out.append(f"{ck}: scored under the median of {n} leave-one-group-out fits; every group, the pair's own "
                       f"included, was fitted by {n - 1} of them")
            continue
        if ck.startswith("card:"):
            bad = [i for i in p.get("instances") or [] if i["verdict"] != "HELD OUT"]
            out.append(f"{ck}: {len(bad)} of {len(p.get('instances') or [])} folds fitted the subject they scored "
                       f"({p.get('eval_set')})")
            continue
        at = Counter()
        unres = Counter()
        nk = set()
        for i in p.get("instances") or []:
            if i["verdict"] == "HELD OUT":
                continue
            for k, n in (i.get("overlap_at") or {}).items():
                ck, _, split = k.rpartition("#")
                anc = ck.startswith("ancestor ")
                at[f"{'ancestor ' if anc else ''}{short_ck(ck.replace('ancestor ', ''))}#{split}"] += n
            for u in i.get("unresolved_what") or []:
                unres[short_ck(u.split(": ")[0]) + ": " + u.split(": ", 1)[-1]] += 1
            if i.get("n_eval_keys"):
                nk.add((i.get("fold"), i.get("n_eval_keys"), i.get("overlap")))
        if at:
            n_ov = sum(o for _, _, o in nk if o) if nk else None
            n_all = sum(k for _, k, _ in nk) if nk else None
            out.append(f"{p['checkpoint']} on {p['eval_set']}: {n_ov if n_ov is not None else '?'} of {n_all if n_all is not None else '?'} "
                       f"patients seen at " + "; ".join(f"{k} ({v})" for k, v in at.most_common(4)))
        elif unres:
            out.append(f"{p['checkpoint']} on {p['eval_set']}: unresolved link " + "; ".join(k for k, _ in unres.most_common(2)))
        elif p.get("why"):
            out.append(f"{p['checkpoint']}: {p['why'][:220]}")
    if not out and r["verdict"] == "HELD OUT":
        pairs = [f"{p['checkpoint']} on {p['eval_set']}" for p in r.get("pairs") or []]
        return "held out for " + "; ".join(pairs[:4]) + (" ..." if len(pairs) > 4 else "")
    if not out and r["verdict"] == "N/A":
        return "no checkpoint: a count, a parameter, arithmetic or a published number"
    return " | ".join(out)


def md_escape(s):
    return str(s).replace("|", "/").replace("\n", " ")


def block_counts(chk, q):
    by = defaultdict(Counter)
    for r in chk["rows"]:
        by[r["id"].split(":")[0]][VERDICT[r["verdict"]]] += 1
    L = ["| source | rows | CLEAN | LEAKED | UNRESOLVED | N/A |", "|---|---:|---:|---:|---:|---:|"]
    tot = Counter()
    for s, c in by.items():
        tot.update(c)
        L.append(f"| {s} | {sum(c.values())} | {c['CLEAN']} | {c['LEAKED']} | {c['UNRESOLVED']} | {c['N/A']} |")
    L.append(f"| **all** | **{sum(tot.values())}** | **{tot['CLEAN']}** | **{tot['LEAKED']}** | **{tot['UNRESOLVED']}** | {tot['N/A']} |")
    L.append("")
    L.append(f"CHK-9 as run: {chk['n_rows']} rows, SEEN {chk['n_seen']}, UNRESOLVED {chk['n_unresolved']}, NO EVAL KEYS "
             f"{chk['n_no_eval_keys']}, HELD OUT {chk['n_held_out']}, DECLARED {chk['n_declared']}, N/A {chk['n_not_applicable']} "
             f"(inputs: `{chk['inputs']['quoted_results']}`, `{chk['inputs']['touched']}`, `{chk['inputs']['eval_sets']}`; "
             f"evaluation sets that failed to build: {chk['inputs'].get('eval_sets_failed') or 'none'}).")
    return "\n".join(L)


def block_families(chk, q):
    fam = {r["id"]: r["family"] for r in q["rows"]}
    by = defaultdict(Counter)
    for r in chk["rows"]:
        by[fam.get(r["id"], "?")][VERDICT[r["verdict"]]] += 1
    L = ["| family | rows | CLEAN | LEAKED | UNRESOLVED | N/A | section |", "|---|---:|---:|---:|---:|---:|---|"]
    for f in sorted(by, key=lambda f: (-(by[f]["LEAKED"] + by[f]["UNRESOLVED"]), f)):
        c = by[f]
        sec = FAMILY_SECTION.get(f, "") if (c["LEAKED"] or c["UNRESOLVED"]) else ""
        L.append(f"| `{f}` | {sum(c.values())} | {c['CLEAN']} | {c['LEAKED']} | {c['UNRESOLVED']} | {c['N/A']} | {sec} |")
    return "\n".join(L)


def block_rescored():
    L = []
    # ---- L1 arc
    a = load(HERE / "arc_old_vs_new.json")
    L.append("**L1. Recall against C-arm angle** (`arc_old_vs_new.json`; vertebral body, tilt 0, lateral angle 0; recall "
             "pooled over every lateral angle beside it)\n")
    if a:
        fpc = lambda d: ", ".join(f"{k} {v}" for k, v in d.items())  # noqa: E731
        L.append(f"Old: {a['old']['subjects']} selection subjects; frames per card: {fpc(a['old']['frames_per_card'])}. "
                 f"New: {a['new']['subjects']} subjects the gate passes for all four detectors; frames per card: "
                 f"{fpc(a['new']['frames_per_card'])}; gate held_out {a['new']['gate']['held_out']}, overlap "
                 f"{a['new']['gate']['overlap']}.\n")
        L.append("| detector | card | conf | lat 0, old (boxes) | lat 0, new [95 % subject bootstrap] (boxes) | all angles old -> new |")
        L.append("|---|---|---|---|---|---|")
        for c in a["cells"]:
            o, w = c["lat0_old"], c["lat0_new"]
            L.append(f"| {c['detector']} | {c['card']} | {c['conf']} | {pct(o['recall'])} ({o['n']}) | {pct(w['recall'])} "
                     f"[{pct(w['lo'])}, {pct(w['hi'])}] ({w['n']}) | {pct(c['all_angles_old']['recall'])} -> "
                     f"{pct(c['all_angles_new']['recall'])} ({c['all_angles_old']['n']} -> {c['all_angles_new']['n']}) |")
    else:
        L.append("pending: `arc_old_vs_new.py` has not run")
    # ---- L2 render vs film
    L.append("\n**L2. Render-trained vs film-trained detector, NHANES II lumbar films** (`render_vs_film_unseen.json`, "
             "`render_vs_film_unseen_rerun.json`; percentile interval over spines)\n")
    rv = load(HERE / "render_vs_film_unseen.json")
    rr = load(HERE / "render_vs_film_unseen_rerun.json")
    a3 = load(EG_DIR.parent / "a3.json")
    L.append("| set | conf | spines | bodies | film-trained | render-trained | film minus render [95 %] | spines film > render : render > film |")
    L.append("|---|---|---:|---:|---|---|---|---|")

    def cmp_row(label, c, conf, extra=""):
        k_a, k_b = round(c["p_a"] * c["n_items"]), round(c["p_b"] * c["n_items"])
        return (f"| {label} | {conf} | {c['n_clusters']} | {c['n_items']} | {pct(c['p_a'], 2)} ({k_a}) | {pct(c['p_b'], 2)} ({k_b}) | "
                f"{c['diff_pp']:+.1f} [{c['percentile_pp'][0]:.1f}, {c['percentile_pp'][1]:.1f}] | "
                f"{c['clusters_favouring_a']} : {c['clusters_favouring_b']}{extra} |")
    for conf in ("0.05", "0.25"):
        if a3:
            L.append(cmp_row("as quoted: first 25 annotated spines, 24 of them in the film detector's own train or val",
                             a3["comparisons"]["render_vs_film_detector"][f"conf_{conf}"], conf))
        if rv and conf == "0.05":
            b = rv["unseen_by_both"]
            L.append(f"| re-read: of those 25, the spines neither detector saw ({', '.join(b.get('spine_ids') or [])}) | {conf} | "
                     f"{b.get('spines', 0)} | {b.get('bodies', 0)} | {b.get('film_found', 0)}/{b.get('bodies', 0)} | "
                     f"{b.get('render_found', 0)}/{b.get('bodies', 0)} | one cluster: no interval | "
                     f"{b.get('spines_favouring_film', 0)} : {b.get('spines_favouring_render', 0)} |")
        if rr and rr.get(f"conf_{conf}"):
            g = (rr.get("eval_gate") or {})
            c = rr[f"conf_{conf}"]
            L.append(cmp_row(f"rerun: every annotated NHANES II lumbar spine the gate passes for both detectors (gate "
                             f"held_out {g.get('held_out')}, overlap {g.get('overlap')})", c, conf,
                             f" (sign test p {c['cluster_sign_test_p']:.2g})"))
        elif conf == "0.05":
            L.append("| rerun: every annotated NHANES II lumbar spine the gate passes for both detectors | | pending: grid job "
                     "`slurm/eval_leaks_gpu.sh` (40429839, CPU) | | | | | |")
    # ---- zero-shot
    L.append("\n**U1 replacement. Zero-shot C-ArmLSpine naming, whole frame, detected vertebrae** (`zeroshot_v9.json`; "
             "percentile interval, case bootstrap)\n")
    z = load(HERE / "zeroshot_v9.json")
    if z:
        L.append("| run | encoder (lineage) | view | exact | answered | exact on answered | cases |")
        L.append("|---|---|---|---|---|---|---:|")
        for key, lab, enc in (("zeroshot2_declared", "zeroshot2 (as quoted)", "allspine_v2_r1, no head (UNRESOLVED)"),
                              ("zeroshot_v9", "zeroshot_v9 (replacement)", "allspine_v9 + head_allspine_v9_mixed_kmax4_seed0 (HELD OUT)")):
            c = z.get(key) or {}
            pre = key.replace("_declared", "")
            for view in ("LAT", "AP"):
                v = c.get(f"{pre}/det/{view}/kfull")
                if not v:
                    continue
                e, an, ea = v["exact_full_coverage"], v["answered"], v.get("exact_on_answered") or {}
                L.append(f"| {lab} | {enc} | {view} | {pct(e['point'])} = {e['k']}/{e['n']} {ci(e['percentile'])} | "
                         f"{pct(an['point'])} | {pct(ea.get('point'))} {ci(ea.get('percentile'))} | {e['clusters']} |")
            pc = c.get("lateral_minus_ap_paired")
            if pc:
                L.append(f"| {lab} | | lateral minus AP, paired | {pc['diff_pp']:+.1f} pp [{pc['percentile_pp'][0]:.1f}, "
                         f"{pc['percentile_pp'][1]:.1f}] on {pc.get('matched_vertebrae')} vertebrae | | cases lateral better "
                         f"{pc['clusters_favouring_a']} : {pc['clusters_favouring_b']} | {pc['n_clusters']} |")
        g = (z.get("zeroshot_v9") or {}).get("eval_gate") or {}
        L.append(f"\nzeroshot_v9 gate: held_out {g.get('held_out')}, overlap {g.get('overlap')}, unresolved {g.get('unresolved')}, "
                 f"{g.get('n_checks')} checks (detector_v5z_final, allspine_v9 encoder, v9 head, per split). zeroshot2 under the "
                 f"strict gate: {((z.get('zeroshot2') or {}).get('error') or '')[:160]} ...")
    # ---- L6 card gain
    L.append("\n**L6. Device-card gain in held-out R^2 over uncalibrated physics** (`card_gain_unseen.json`; 10,000 fold "
             "resamples, percentile)\n")
    cg = load(HERE / "card_gain_unseen.json")
    if cg:
        L.append("| folds | frames | mean gain [95 %] | frame-weighted [95 %] | median | negative folds | exact sign-flip p |")
        L.append("|---|---:|---|---|---:|---:|---:|")
        for key, lab in (("all_24", "all 24 (as quoted: four devices)"),
                         ("patient_held_out_12", f"12 patient-held-out ({', '.join(cg['devices_patient_held_out'])})"),
                         ("within_subject_12", f"12 within-subject ({', '.join(cg['devices_within_subject'])})")):
            s = cg[key]
            L.append(f"| {lab} | {s['frames']} | {s['mean_unweighted']:+.4f} [{s['mean_unweighted_ci_percentile'][0]:.4f}, "
                     f"{s['mean_unweighted_ci_percentile'][1]:.4f}] | {s['mean_frame_weighted']:+.4f} "
                     f"[{s['mean_frame_weighted_ci_percentile'][0]:.4f}, {s['mean_frame_weighted_ci_percentile'][1]:.4f}] | "
                     f"{s['median']:+.4f} | {s['negative_folds']} of {s['n_folds']} | {s['signflip_exact']:.2g} |")
    # ---- L7 fig S2a
    L.append("\n**L7. Figure S2a body-region R^2 under the fold fit that held the pair's group out** "
             "(`fig4_pairs_heldout.json`)\n")
    f4 = load(HERE / "fig4_pairs_heldout.json")
    if f4:
        L.append("| device | pairs | subject held out? | device median, as drawn (median of fold fits) | device median, held-out fold | shown pair | shown pair as drawn | shown pair, held-out fold |")
        L.append("|---|---:|---|---:|---:|---|---:|---:|")
        for name, d in f4["devices"].items():
            sp = d.get("shown_pair") or {}
            f = lambda x: "-" if x is None else f"{x:.3f}"  # noqa: E731
            L.append(f"| {name} | {d['n_pairs']} | {'yes' if d['patient_held_out'] else 'no: one subject, fold = view/frame'} | "
                     f"{f(d['device_median_r2_median_theta'])} | {f(d['device_median_r2_heldout_fold'])} | {sp.get('pair')} | "
                     f"{f(sp.get('as_drawn'))} | {f(sp.get('r2_heldout_fold'))} |")
    else:
        L.append("pending: grid job `rescore_fig4_pairs_heldout.py` (40429711)")
    return "\n".join(L)


def block_rows(chk, q):
    fam = {r["id"]: r for r in q["rows"]}
    L = ["| row | verdict | family | number (truncated) | what decided it | section |", "|---|---|---|---|---|---|"]
    order = {"LEAKED": 0, "UNRESOLVED": 1, "CLEAN": 2, "N/A": 3, "DECLARED": 1}
    rows = sorted(chk["rows"], key=lambda r: (order[VERDICT[r["verdict"]]], r["id"]))
    for r in rows:
        v = VERDICT[r["verdict"]]
        f = fam.get(r["id"], {}).get("family", "?")
        sec = FAMILY_SECTION.get(f, "") if v in ("LEAKED", "UNRESOLVED") else ""
        num = md_escape(fam.get(r["id"], {}).get("quoted") or r.get("quoted") or "")[:150]
        L.append(f"| `{r['id']}` | {v} | {f} | {num} | {md_escape(row_why(r))[:420]} | {sec} |")
    return "\n".join(L)


def fill(md, blocks):
    txt = md.read_text(encoding="utf-8")
    for name, body in blocks.items():
        pat = re.compile(rf"(<!-- BEGIN:GENERATED {name} -->\r?\n)(?:.*?\r?\n)?(<!-- END:GENERATED {name} -->)", re.S)
        if not pat.search(txt):
            raise SystemExit(f"{md} has no block {name}")
        txt = pat.sub(lambda m: m.group(1) + body + "\n" + m.group(2), txt)
    md.write_text(txt, encoding="utf-8")


def main() -> int:
    chk = load(EG_DIR / "chk9" / "chk9_report.json")
    q = load(EG_DIR / "quoted_results.json")
    fill(MD, {"counts": block_counts(chk, q), "families": block_families(chk, q), "rescored": block_rescored(),
              "rows": block_rows(chk, q)})
    c = Counter(VERDICT[r["verdict"]] for r in chk["rows"])
    print(f"wrote {MD}: {dict(c)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
