"""CLOSURE of VERIFY.md items 1b and 1c, reproduced on the grid against the real lineage store and the real files.

Run from the STAGED code directory (the eval_gate/2 tools copied beside, never over, the grid clone the Figure 6 chain
runs from). Each subcommand prints one JSON line per check and writes its results to --out.

  bound-matches SRC OUT     a copy of a pre-eval_gate/2 matches.json made the way eval_gate/2 writes it (weights_sha256
                            hashed from the weight files, verdict re-computed on the record subjects): the CONTROL for
                            the --matches check, so that a refusal can be told from a file that merely lacks a field
  carry OUT                 1b-ii on real files: a hand-written block, a genuine block from another checkpoint, a
                            genuine block from another evaluation set, and the real pre-gate dump
  transplant OUT DUMP       1b-ii on a dump eval_gate/2 wrote today (tools/realxray_eval.py, rx_lodo on carm_test):
                            carried as held out; its block pasted onto dc_P_pooled's weights, or onto the 17 arc
                            subjects, is refused
  keys OUT                  1b-iii on the real v9 bank, the real ~/patient_keys_v9.json and the real store
  curve-cells NEW PUB OUT   the R1d control curve against the published unseen curve, cell by cell
  eval-sets-diff OLD NEW OUT  what regenerating eval_sets.json under eval_gate/2 changed, set by set
"""
import json
import os
import sys
import traceback
from pathlib import Path

CODE = Path(os.environ.get("CLOSURE_CODE", Path.cwd()))
sys.path.insert(0, str(CODE / "tools"))
import eval_gate as EG  # noqa: E402

H = os.path.expanduser("~")
RUNS = f"{H}/spine-detector/runs"
P = f"{RUNS}/devcorpus/dc_P_pooled/weights/best.pt"
A = f"{RUNS}/devcorpus/dc_A_held_surgio_b51_dr/weights/best.pt"
B = f"{RUNS}/devcorpus/dc_B_held_surgio_b51_dr_s1/weights/best.pt"
LODO = f"{RUNS}/realxray/rx_lodo_carmlspine_1024/weights/best.pt"
V5Z = f"{H}/FluoroCap/detect_v5z_final_best.pt"
V9 = f"{H}/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt"
RENDER = f"{H}/model_night/runs/model_scal_pt_render.pt"
DATA = "/rs/rs_grp_oschome/go2432/data"
ARC17 = ["s0585", "s0970", "s1045", "s1062", "s1159", "s1384", "s1535", "s1579", "s1700", "s1836", "s1842", "s1872",
         "s1880", "s1883", "s1902", "s2033", "s2053"]
UNSEEN = json.load(open(f"{DATA}/devcorpus_arc/anglesweep_unseen/SET_INFO.json"))["subjects"]
LEAKDUMP = f"{DATA}/or_ready/lodo/sweeps/lodo_carm__cobra_test.json"
RES = {}


def check(name, fn, expect):
    """expect: an exception class name, or 'pass'."""
    try:
        out = fn()
        got, msg = "pass", out
    except EG.EvalGateError as e:
        got, msg = type(e).__name__, str(e).splitlines()[0][:400]
    except Exception as e:  # noqa: BLE001
        got, msg = f"NOT A GATE ERROR {type(e).__name__}", f"{e} | {traceback.format_exc()[-600:]}"
    ok = (got == expect)
    RES[name] = dict(expect=expect, got=got, ok=ok, detail=msg)
    print(json.dumps({"check": name, "expect": expect, "got": got, "ok": ok, "detail": msg}, default=str)[:1200],
          flush=True)
    return ok


def dump(obj, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    json.dump(obj, open(path, "w"), indent=1, default=str)


def arc_dump(weights, subjects, sha=None, block=None):
    """A dump shaped like the leaked arc evaluation: weights, the frames of the subjects, optionally a verdict."""
    d = dict(weights=weights, weights_sha256=sha if sha is not None else EG.sha256_of(weights),
             data=f"{DATA}/devcorpus_arc/anglesweep", split="",
             frames=[dict(case=f"TS_{s}", stem=f"{s}_lat+000_tilt+00") for s in subjects])
    if block is not None:
        d["eval_gate"] = block
    return d


def cmd_bound_matches(src, out):
    m = json.load(open(src))
    w = m["weights"]
    subj = sorted({r["subject"] for r in m["records"]})
    gate = EG.block(EG.assert_unseen_all([f"TS_{s}" for s in subj], w, "closure R1d control (bound copy)"))
    m.pop("eval_gate", None)
    m.pop("weights_sha256", None)
    b = EG.stamp(m, gate)
    json.dump(b, open(out, "w"))
    print(json.dumps({"bound_matches": out, "weights_sha256": b["weights_sha256"], "held_out": gate["held_out"],
                      "n_subjects": len(subj)}), flush=True)


def cmd_carry(out):
    # T1: a hand-written verdict on the leaked arc shape (dc_P_pooled selected on the 17 subjects)
    check("T1 hand-written block, no checks, on dc_P_pooled x the 17 arc subjects",
          lambda: EG.carry(arc_dump(P, ARC17, block=dict(gate_version="eval_gate/1", held_out=True, checks=[])),
                           "closure T1")["held_out"], "UnverifiedDump")
    # T2: a GENUINE eval_gate/2 verdict of another checkpoint (detect_v5z passes the 17) pasted onto dc_P_pooled's dump
    genuine = EG.block([EG.assert_unseen([f"TS_{s}" for s in ARC17], V5Z, "closure T2 (a checkpoint the 17 are unseen by)")])
    RES["T2 genuine block (detect_v5z on the 17)"] = dict(held_out=genuine["held_out"],
                                                          checkpoint_sha256=genuine["checks"][0]["checkpoint_sha256"])
    check("T2 genuine block of detect_v5z pasted onto dc_P_pooled's dump of the 17",
          lambda: EG.carry(arc_dump(P, ARC17, block=genuine), "closure T2")["held_out"], "UnverifiedDump")
    check("T2-control the same block on detect_v5z's own dump of the 17 is carried",
          lambda: EG.carry(EG.stamp(arc_dump(V5Z, ARC17), genuine), "closure T2 control")["held_out"], "pass")
    # T2b: a genuine verdict of dc_P_pooled itself, but on another set (the 40 unseen), pasted onto its dump of the 17
    other = EG.block(EG.assert_unseen_all([f"TS_{s}" for s in UNSEEN], {"pooled": P}, "closure T2b"))
    check("T2b dc_P_pooled's genuine block on the 40 unseen pasted onto its dump of the 17",
          lambda: EG.carry(arc_dump(P, ARC17, block=other), "closure T2b")["held_out"], "UnverifiedDump")
    # T3: the real pre-gate dump (records no sha256): refused; declared, it is carried as not held out
    check("T3 real pre-gate dump lodo_carm__cobra_test.json", lambda: EG.carry(LEAKDUMP, "closure T3")["held_out"],
          "UnverifiedDump")
    check("T3-declared the same, --not-held-out", lambda: EG.carry(LEAKDUMP, "closure T3d",
                                                                   not_held_out="closure: a pre-eval_gate/2 dump")["held_out"],
          "pass")
    # T3b: that dump, with the sha256 of the file at its weights path today written in: gated by that sha -> seen
    d = json.load(open(LEAKDUMP))
    d["weights_sha256"] = EG.sha256_of(d["weights"])
    check("T3b the same dump carrying rx_lodo's sha256: gated at scoring, 27 of 27 in its VAL set",
          lambda: EG.carry(d, "closure T3b")["held_out"], "SeenInEvaluation")
    dump(RES, out)


def cmd_transplant(out, rx_dump):
    d = json.load(open(rx_dump))
    RES["C the eval_gate/2 dump"] = dict(file=rx_dump, weights=d["weights"], weights_sha256=d.get("weights_sha256"),
                                         held_out=d["eval_gate"]["held_out"], n_keys=d["eval_gate"]["checks"][0]["n_keys"],
                                         eval_digest=d["eval_gate"]["checks"][0]["eval_digest"])
    check("C1 rx_lodo x carm_test, written by eval_gate/2 realxray_eval: carried held out",
          lambda: EG.carry(rx_dump, "closure C1")["held_out"], "pass")
    t = dict(d, weights=P, weights_sha256=EG.sha256_of(P))
    check("C2 its block pasted onto a dump whose weights are dc_P_pooled", lambda: EG.carry(t, "closure C2")["held_out"],
          "UnverifiedDump")
    t = dict(d, frames=[dict(case=f"TS_{s}", stem=f"{s}_lat+000_tilt+00") for s in ARC17])
    check("C3 its block pasted onto a dump of the 17 arc subjects (same weights)",
          lambda: EG.carry(t, "closure C3")["held_out"], "UnverifiedDump")
    t = json.loads(json.dumps(d))
    t["eval_gate"]["checks"][0]["eval_keys"] = t["eval_gate"]["checks"][0]["eval_keys"][1:]
    check("C4 a check with one key removed (its digest no longer reproduces)",
          lambda: EG.carry(t, "closure C4")["held_out"], "UnverifiedDump")
    t = dict(d)
    t.pop("weights_sha256")
    check("C5 the same dump with its weights_sha256 deleted", lambda: EG.carry(t, "closure C5")["held_out"],
          "UnverifiedDump")
    dump(RES, out)


def cmd_keys(out):
    import numpy as np
    sys.path.insert(0, str(CODE / "tools"))
    import learning_embed as LE
    keys = json.load(open(f"{H}/patient_keys_v9.json"))["keys"]
    z = np.load(f"{H}/allspine_v9_fov96_ctx/rung_1.npz", allow_pickle=True)
    case, split = z["case"].astype(str), z["split"].astype(str)
    val = sorted(set(case[split == "val"].tolist()))
    e = EG.load_store().entries[EG.norm_path(V9)]
    train = EG._canon_set(e["train_keys"])
    k_route, n, unk = EG.key_items(LE.bank_gate_items(val, keys))
    k_name = EG.key_items([dict(case=c) for c in val])[0]
    k_map_old = {EG.PK.canon_key(keys[c]) for c in val if keys.get(c)}          # the old route's keys (as given)
    implant_map = sum(1 for c in val if str(keys.get(c, "")).startswith("implant:"))
    bad_map = sorted({keys[c] for c in val if keys.get(c) and not EG.resolve_given_key(keys[c])[0]})
    RES["K1 learning_embed route over the v9 val split"] = dict(
        val_cases=len(val), val_cases_the_map_sends_to_implant_keys=implant_map,
        persons_keyed_now=len(k_route), unkeyed_now=len(unk), unkeyed_examples=unk[:5],
        train_persons_seen_now=len(k_route & train), train_persons_keying_names_only=len(k_name & train),
        train_persons_the_old_route_saw=len((k_map_old | {k for c in val if not keys.get(c)
                                                            for k in EG.key_items([dict(case=c)])[0]}) & train),
        map_values_that_name_no_person=len(bad_map), map_value_examples=bad_map[:5])
    print(json.dumps(RES["K1 learning_embed route over the v9 val split"]), flush=True)
    check("K2 implant:0001_v0 against model_scal_pt_render (trained on ctsp:0001)",
          lambda: EG.assert_unseen(["implant:0001_v0"], RENDER, "closure K2")["held_out"], "SeenInEvaluation")
    check("K3 {key: ts:s9999, case: TS_s0585} against dc_P_pooled (s0585 is a selection subject)",
          lambda: EG.assert_unseen([dict(key="ts:s9999", case="TS_s0585")], P, "closure K3")["held_out"],
          "SeenInEvaluation")
    check("K4 implant:zzz9_v0 (no record, no declared build fits): not a person",
          lambda: EG.assert_unseen(["implant:zzz9_v0"], P, "closure K4")["held_out"], "UnkeyedEvalItem")
    check("K5 ts:bogus: a known corpus, not a person id", lambda: EG.assert_unseen(["ts:bogus"], P, "closure K5")["held_out"],
          "UnkeyedEvalItem")
    check("K6 control: carmlspine:case100 against rx_lodo_carmlspine_1024 is held out",
          lambda: EG.assert_unseen(["carmlspine:case100"], LODO, "closure K6")["held_out"], "pass")
    dump(RES, out)


def cmd_curve_cells(new, pub, out):
    a, b = json.load(open(new)), json.load(open(pub))
    n = same = 0
    diff = []
    for det, cards in b["curves"].items():
        for card, confs in cards.items():
            for conf, clss in confs.items():
                for cls, tilts in clss.items():
                    for tilt, cells in tilts.items():
                        for x, y in zip(a["curves"][det][card][conf][cls][tilt], cells):
                            n += 1
                            if x["n"] == y["n"] and x["recall"] == y["recall"] and x["lo"] == y["lo"] and x["hi"] == y["hi"]:
                                same += 1
                            elif len(diff) < 5:
                                diff.append(dict(det=det, card=card, conf=conf, cls=cls, tilt=tilt, new=x, pub=y))
    r = dict(cells=n, identical=same, differing_examples=diff, new_eval_gate_held_out=a["eval_gate"]["held_out"],
             new_weights_sha256=a.get("weights_sha256"))
    dump(r, out)
    print(json.dumps(r)[:1500], flush=True)


def cmd_eval_sets_diff(old, new, out):
    o, w = json.load(open(old)), json.load(open(new))
    rows = {}
    for name in sorted(set(o["sets"]) | set(w["sets"])):
        a, b = o["sets"].get(name), w["sets"].get(name)
        if a is None or b is None:
            rows[name] = dict(old=a is not None, new=b is not None)
            continue
        ka, kb = set(a["keys"]), set(b["keys"])
        rows[name] = dict(old_keys=len(ka), new_keys=len(kb), old_unkeyed=a["n_unkeyed"], new_unkeyed=b["n_unkeyed"],
                          only_old=sorted(ka - kb)[:10], only_new=sorted(kb - ka)[:10], n_only_old=len(ka - kb),
                          n_only_new=len(kb - ka), source_old=a["source"][:160], source_new=b["source"][:160])
    r = dict(old=dict(built=o["built"], gate_version=o["gate_version"], failed=o["failed"]),
             new=dict(built=w["built"], gate_version=w["gate_version"], failed=w["failed"]), sets=rows)
    dump(r, out)
    print(json.dumps(r, indent=1)[:6000], flush=True)


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "bound-matches":
        cmd_bound_matches(sys.argv[2], sys.argv[3])
    elif c == "carry":
        cmd_carry(sys.argv[2])
    elif c == "transplant":
        cmd_transplant(sys.argv[2], sys.argv[3])
    elif c == "keys":
        cmd_keys(sys.argv[2])
    elif c == "curve-cells":
        cmd_curve_cells(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == "eval-sets-diff":
        cmd_eval_sets_diff(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        raise SystemExit(f"unknown subcommand {c}")
    bad = [k for k, v in RES.items() if isinstance(v, dict) and v.get("ok") is False]
    print(f"CLOSURE_{c.upper()}_DONE failed_expectations={bad}", flush=True)
    raise SystemExit(1 if bad else 0)
