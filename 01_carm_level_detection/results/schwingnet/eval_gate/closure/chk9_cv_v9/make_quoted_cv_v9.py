#!/usr/bin/env python
"""quoted_results.json with the C-ArmLSpine rows moved from the allspine_v2_r1 lineage to the cv_v9 (allspine_v9)
lineage, for a CHK-9 re-run (tools/leak_check.py chk9).

WHY. CHK-9 of 2026-09-24 06:01 (job 40429833) found 58 UNRESOLVED rows, 57 of them because every C-ArmLSpine fold model
and the zero-shot arm descended from allspine_v2_r1, whose training bank was deleted (EVAL_LEAKS U1). The closure
re-trained the fold models from allspine_v9 with one change, the initialisation (closure/cv_v9/CV_V9.md), and scored
zero-shot allspine_v9 (encoder + its seed-0 mixed-length head) on the same fold frames. This script substitutes those
checkpoints into every quoted row whose initialisation chain contains allspine_v2_r1, so that CHK-9 can decide the
replacement rows from the lineage store instead of from a declaration. Nothing else in the file changes.

WHAT IS SUBSTITUTED, per pair of a row:
  carm_cv_fold_models   on carm_cv     -> carm_cv_fold_models_v9init   on carm_cv     (same folds, bound by K)
  carm_cvday_fold_models on carm_cvday -> carm_cvday_fold_models_v9init on carm_cvday
  allspine_v2_r1 on carm_all148        -> allspine_v9_encoder on carm_cv AND allspine_v9_head_seed0 on carm_cv
     (the closure's zero-shot family pre:zs_v9head was scored per fold on the pre-repair mirror of the fold
      directories, i.e. the 148 carm_cv cases; the head is the seed-0 mixed-length head of the v9 encoder)
  every other pair (detector_v5z_final, rx_lodo_carmlspine_1024, ...) is left as it is.

The new number each row now quotes is copied from MANUSCRIPT_CORRECTIONS.md section 7.2 item 10 (the NUMBERS.md
table, keyed by the row id in brackets) into `quoted_cv_v9`; `quoted` keeps the old text so the row stays findable.

    python make_quoted_cv_v9.py --quoted ../../quoted_results.json --corrections ../MANUSCRIPT_CORRECTIONS.md \
        --out quoted_results_cv_v9.json
"""
import argparse
import copy
import json
import re
from pathlib import Path

H = "/wsu/home/go/go24/go2432"
CV9 = "SchwingNet/results/eval_gate/closure/cv_v9"

NEW_CHECKPOINTS = {
    "carm_cv_fold_models_v9init": {
        "label": "C-ArmLSpine five-fold models re-trained from allspine_v9 (EVAL_LEAKS U1 closure): "
                 "model_rung_1_ft_cv{K}_v9init_aug2.pt + head_cv{K}_v9init.pt (per fold K)",
        "path": f"{H}/carm_cvmix{{K}}_fov96_ctx/runs/model_rung_1_ft_cv{{K}}_v9init_aug2.pt; "
                f"{H}/model_night/heads_carm/head_cv{{K}}_v9init.pt",
        "parent": "allspine_v9_encoder",
        "train": ["allspine_v7:train_sample", "carm:not_scored_fold"],
        "val": ["allspine_v7:sample", "carm:not_scored_fold"],
        "pose": {},
        "selection": "encoder: best epoch on the fold bank's val (--val-frac 0.2 of the non-test folds' crops); head: final epoch",
        "lists": f"{H}/carm_cvmix{{K}}_fov96_ctx/rung_1.npz (the shipped fold's merged bank, written 2026-09-21 22:16, "
                 "before either fold model; case/split arrays); fold membership /rs/rs_grp_oschome/go2432/data/realxray/carmlspine_cv/fold{K}",
        "evidence": "slurm/carmlspine_cv_v9init.sh (job 40431706; INIT=~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt, epochs 15, "
                    "lr 1e-4, augment 2, the shipped seeds); lineage computed on demand by tools/eval_gate.py inside "
                    "level_prototype.py and cached in or_ready/eval_gate/ondemand/ (unresolved []); "
                    f"{CV9}/cv_v9.json#families/pre:cv5_det/gate (held out, overlap 0, unresolved 0, 150 checks)",
    },
    "carm_cvday_fold_models_v9init": {
        "label": "C-ArmLSpine acquisition-day three-fold models re-trained from allspine_v9 (same recipe, folds by DICOM StudyDate)",
        "path": f"{H}/carm_cvdaymix{{K}}_fov96_ctx/runs/model_rung_1_ft_cvday{{K}}_v9init_aug2.pt; "
                f"{H}/model_night/heads_carm/head_cvday{{K}}_v9init.pt",
        "parent": "allspine_v9_encoder",
        "train": ["allspine_v7:train_sample", "carm:not_scored_fold"],
        "val": ["carm:not_scored_fold"],
        "pose": {},
        "selection": "as the case folds",
        "lists": "results/carmlspine_day_groups.json; the shipped day fold's merged bank ~/carm_cvdaymix{K}_fov96_ctx/rung_1.npz",
        "evidence": "slurm/carmlspine_cv_day_v9init.sh (job 40431707); on-demand lineage as above; "
                    f"{CV9}/cv_v9.json#families/pre:cvday_det/gate (held out, overlap 0, unresolved 0, 90 checks)",
    },
    "allspine_v9_head_seed0": {
        "label": "mixed-length run head on the v9 encoder (seed 0); the head of the zero-shot v9 arm",
        "path": f"{H}/model_night/heads_mixed/head_allspine_v9_mixed_kmax4_seed0.pt",
        "parent": "allspine_v9_encoder",
        "train": ["v9:train"],
        "val": [],
        "pose": {},
        "selection": "final epoch (no selection on val)",
        "lists": f"{H}/allspine_v9_fov96_ctx/rung_1.npz split == train",
        "evidence": "tools/head_mixed_length.py (torch.save after the last epoch); touched.json row; "
                    f"{CV9}/cv_v9.json#families/pre:zs_v9head/gate (held out, overlap 0, unresolved 0, 150 checks)",
    },
}

PAIR_MAP = {
    ("carm_cv_fold_models", "carm_cv"): [("carm_cv_fold_models_v9init", "carm_cv")],
    ("carm_cvday_fold_models", "carm_cvday"): [("carm_cvday_fold_models_v9init", "carm_cvday")],
    ("allspine_v2_r1", "carm_all148"): [("allspine_v9_encoder", "carm_cv"), ("allspine_v9_head_seed0", "carm_cv")],
}
PAIR_WHY = {
    "carm_cv_fold_models_v9init": f"substituted (EVAL_LEAKS U1 closure): {CV9}/cv_v9.json#families/pre:cv5_det/gate held out, overlap 0, unresolved 0",
    "carm_cvday_fold_models_v9init": f"substituted (EVAL_LEAKS U1 closure): {CV9}/cv_v9.json#families/pre:cvday_det/gate held out, overlap 0, unresolved 0",
    "allspine_v9_encoder": f"substituted (EVAL_LEAKS U1 closure): zero-shot v9 scored per fold on the pre-repair mirror of the carm_cv fold directories; {CV9}/cv_v9.json#families/pre:zs_v9head/gate held out, overlap 0, unresolved 0",
    "allspine_v9_head_seed0": f"substituted (EVAL_LEAKS U1 closure): the head of the zero-shot v9 arm; {CV9}/cv_v9.json#families/pre:zs_v9head/gate",
}
CHAIN = {
    "carm_cv_fold_models_v9init": ["carm_cv_fold_models_v9init", "allspine_v9_encoder", "imagenet"],
    "carm_cvday_fold_models_v9init": ["carm_cvday_fold_models_v9init", "allspine_v9_encoder", "imagenet"],
    "allspine_v9_encoder": ["allspine_v9_encoder", "imagenet"],
    "allspine_v9_head_seed0": ["allspine_v9_head_seed0", "allspine_v9_encoder", "imagenet"],
}
OUTPUT_BY_FAMILY = {
    "carm_cv_naming": f"{CV9}/rigor_pre/a4.json, a7.json, a9.json (cells as results/a4.json, a7.json, a9.json); {CV9}/cv_v9.json#families/pre:cv5_det",
    "carm_cvday_naming": f"{CV9}/rigor_pre/a9.json#cv/cvday_acquisition_day_folds; {CV9}/cv_v9.json#families/pre:cvday_det",
    "carm_cv_oracle": f"{CV9}/carmlspine_cv5_v9init_pre.json#oracle; {CV9}/cv_v9.json#families/pre:cv5_oracle",
    "carm_zeroshot": f"{CV9}/cv_v9.json#families/pre:zs_v9head/cells, #zero_shot_paired; {CV9}/cv_v9_extras_pre.json#pairs; results/eval_gate/leaks/zeroshot_v9.json (whole frame)",
    "coupling": f"{CV9}/coupling_pre/coupling.json; {CV9}/coupling_pre/COUPLING.md; {CV9}/fig4_inputs_pre/proto_post_v9init_prerepair/cv_fold<K>/det/kfull/couple_c74/couple_all.json",
}

ROW_RX = re.compile(r"^\|\s*(\d+(?:-\d+)?)\s*\[L(\d+)(?:-L(\d+))?\]\s*\|(.*)\|\s*$")


def item10_table(corrections_md):
    """{'NUMBERS:L64': {'numbers_line': '84', 'old': ..., 'new': ...}, ...} from section 7.2 item 10."""
    out = {}
    text = Path(corrections_md).read_text(encoding="utf-8")
    start = text.find("**10. `SchwingNet/NUMBERS.md`**")
    end = text.find("**11. `CLAIMS_LEDGER.md", start)
    for line in text[start:end].splitlines():
        m = ROW_RX.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(4).split(" | ")]
        old, new = (cells[0], " | ".join(cells[1:])) if len(cells) >= 2 else (cells[0], "")
        lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
        for n in range(lo, hi + 1):
            out[f"NUMBERS:L{n}"] = dict(numbers_line=m.group(1), old=old, new=new)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--quoted", required=True)
    ap.add_argument("--corrections", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    q = json.load(open(a.quoted, encoding="utf-8"))
    new_numbers = item10_table(a.corrections)
    ck = q["checkpoints"]
    for k, v in NEW_CHECKPOINTS.items():
        ck[k] = v
    substituted = []
    for r in q["rows"]:
        chains = [c for c in r.get("checkpoints") or [] if isinstance(c, dict) and "allspine_v2_r1" in (c.get("init_chain") or [])]
        if not chains:
            continue
        old_pairs = [(p["checkpoint"], p["eval_set"]) for p in r.get("per_pair") or []]
        new_pairs, from_keys, to_keys = [], [], []
        for p in r.get("per_pair") or []:
            key = (p["checkpoint"], p["eval_set"])
            if key in PAIR_MAP:
                from_keys.append(p["checkpoint"])
                for nck, nes in PAIR_MAP[key]:
                    to_keys.append(nck)
                    new_pairs.append(dict(checkpoint=nck, eval_set=nes, verdict="to be established by CHK-9",
                                          why=PAIR_WHY[nck]))
            else:
                new_pairs.append(p)
        if not from_keys:
            # a chain names allspine_v2_r1 but no pair does: leave the row alone and say so
            r["substitution"] = dict(note="chain names allspine_v2_r1 but no (checkpoint, eval set) pair does; not substituted")
            continue
        # the checkpoints list: replace the substituted entries, keep the rest
        new_cks = []
        for c in r["checkpoints"]:
            if not isinstance(c, dict) or c.get("key") not in from_keys:
                new_cks.append(c)
                continue
            for nck, _ in PAIR_MAP[(c["key"], next(es for k2, es in old_pairs if k2 == c["key"]))]:
                new_cks.append(dict(key=nck, path=NEW_CHECKPOINTS.get(nck, ck.get(nck, {})).get("path"),
                                    init_chain=CHAIN[nck], selection=ck[nck].get("selection")))
        r["checkpoints"] = new_cks
        r["per_pair"] = new_pairs
        fam = r.get("family")
        old_out = r.get("output_file")
        if fam in OUTPUT_BY_FAMILY:
            r["output_file"] = OUTPUT_BY_FAMILY[fam]
        else:
            r["output_file"] = f"{old_out}; zero-shot member now {CV9}/cv_v9.json#families/pre:zs_v9head, #zero_shot_paired"
        r["why"] = "; ".join(f"{p['checkpoint']} on {p['eval_set']}: {p['verdict']}" for p in new_pairs)
        nn = new_numbers.get(r["id"])
        r["substitution"] = dict(
            reason="EVAL_LEAKS U1 closure (closure/cv_v9/CV_V9.md): the allspine_v2_r1-initialised fold models and the "
                   "zero-shot arm are replaced by the allspine_v9-initialised ones; the pairs below are what CHK-9 checks",
            from_pairs=[f"{k} on {e}" for k, e in old_pairs if (k, e) in PAIR_MAP],
            to_pairs=[f"{p['checkpoint']} on {p['eval_set']}" for p in new_pairs if p["checkpoint"] in to_keys],
            output_file_before=old_out,
            numbers_md_line_as_of_1030=nn["numbers_line"] if nn else None,
            quoted_before=nn["old"] if nn else None,
        )
        if nn:
            r["quoted_cv_v9"] = nn["new"]
        substituted.append(r["id"])
    q["schema"] = "eval_gate/quoted_results/1+cv_v9"
    q["built_by"] = (f"{q.get('built_by')}; then SchwingNet/results/eval_gate/closure/chk9_cv_v9/make_quoted_cv_v9.py "
                     f"(C-ArmLSpine rows moved to the allspine_v9 lineage)")
    q["substituted_rows"] = substituted
    q["n_substituted_rows"] = len(substituted)
    q["n_rows_with_quoted_cv_v9"] = sum(1 for r in q["rows"] if "quoted_cv_v9" in r)
    json.dump(q, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"rows {len(q['rows'])}; substituted {len(substituted)}; with a new quoted number {q['n_rows_with_quoted_cv_v9']}; "
          f"item-10 table rows parsed {len(new_numbers)} -> {a.out}")
    for rid in substituted:
        r = next(x for x in q["rows"] if x["id"] == rid)
        print(f"  {rid}: {r['substitution']['from_pairs']} -> {r['substitution']['to_pairs']}"
              f"{'  [new number]' if 'quoted_cv_v9' in r else ''}")


if __name__ == "__main__":
    main()
