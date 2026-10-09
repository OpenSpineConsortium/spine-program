"""VERIFY item 1, the routes around the gate that do not go through an evaluator's own gate call (local, repo touched.json).

  T1  carry() of a dump whose eval_gate block was written by hand: held_out true, no checks.
  T2  carry() of a dump whose block is genuine but belongs to a DIFFERENT checkpoint than the dump's `weights`.
  T3  carry() of the real pre-gate leaked dump shape (weights + frames, no block): must raise.
  T4  key_items() of an item that carries both `key` and `case`: which patient is checked.
  T5  device_fit.fold_gate on a one-phantom card and on a specimen filed under two group names (in-process).
"""
import json
import sys
from pathlib import Path

REPO = Path(r"spinesurg-ct-nnunet:")
sys.path.insert(0, str(REPO / "tools"))
import eval_gate as EG  # noqa: E402

GH = "/wsu/home/go/go24/go2432"
P_POOLED = f"{GH}/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt"
RX_LODO = f"{GH}/spine-detector/runs/realxray/rx_lodo_carmlspine_1024/weights/best.pt"
CLEAN = f"{GH}/FluoroCap/detect_v5z_final_best.pt"
ARC17 = ["s0585", "s0970", "s1045", "s1062", "s1159", "s1384", "s1535", "s1579", "s1700", "s1836", "s1842", "s1872",
         "s1880", "s1883", "s1902", "s2033", "s2053"]
store = EG.load_store(str(REPO / "SchwingNet/results/eval_gate/touched.json"))
res = {}


def attempt(name, fn):
    try:
        out = fn()
        res[name] = dict(raised=None, result=out)
    except EG.EvalGateError as e:
        res[name] = dict(raised=type(e).__name__, message=str(e).splitlines()[0][:300])
    except Exception as e:  # noqa: BLE001
        res[name] = dict(raised=f"(not a gate error) {type(e).__name__}", message=str(e)[:300])
    print(name, "->", json.dumps(res[name])[:400])


leaky = dict(weights=P_POOLED, data="/rs/rs_grp_oschome/go2432/data/devcorpus_arc/anglesweep", split="",
             frames=[dict(case=f"TS_{s}", stem=f"{s}_lat+000_tilt+00") for s in ARC17])

# T1: a hand-written block
forged = dict(leaky, eval_gate=dict(gate_version="eval_gate/1", held_out=True, checks=[]))
attempt("T1 forged block (held_out true, zero checks) on the leaked arc dump",
        lambda: {k: v for k, v in EG.carry(forged, "verify T1", touched=store).items() if k in ("held_out", "n_checks", "overlap")})

# T2: a genuine block from another checkpoint pasted onto the leaked dump
genuine = EG.block([EG.assert_unseen([f"TS_{s}" for s in ARC17], CLEAN, "verify T2 (clean checkpoint)", touched=store,
                                     compute=False)])
swapped = dict(leaky, eval_gate=genuine)
attempt("T2 genuine block of another checkpoint on a dump whose weights are dc_P_pooled",
        lambda: dict(held_out=EG.carry(swapped, "verify T2", touched=store)["held_out"],
                     block_checkpoint=genuine["checks"][0]["checkpoint"], dump_weights=swapped["weights"]))

# T3: the same dump with no block must be gated now and refused
attempt("T3 pre-gate dump (weights dc_P_pooled, 17 arc subjects, no block)", lambda: EG.carry(dict(leaky), "verify T3", touched=store)["held_out"])
attempt("T3b pre-gate dump (weights rx_lodo_carmlspine_1024, s0970 = its parent's train subject, no block)",
        lambda: EG.carry(dict(weights=RX_LODO, data="/x", split="", frames=[dict(case="TS_s0970")]), "verify T3b",
                         touched=store)["held_out"])

# T4: which key wins when an item carries both
k1 = EG.key_items([dict(key="ts:s9999", case="TS_s0585")])[0]
k2 = EG.key_items([dict(case="TS_s0585", stem="TS_s9999")])[0]
res["T4 key vs case"] = dict(key_and_case=sorted(k1), case_and_stem=sorted(k2))
print("T4", res["T4 key vs case"])
attempt("T4b a keys map that re-keys a leaked subject (the learning_embed --keys route)",
        lambda: EG.assert_unseen(["ts:s9999"], P_POOLED, "verify T4b", touched=store, compute=False)["held_out"])

# T5: device cards, in-process
import device_fit as DF  # noqa: E402
geneva = [dict(spec=f"p{k:02d}", subject_spec=f"p{k:02d}") for k in range(1, 7)]
attempt("T5a bv_pulsera fold gate (one phantom, six position groups)",
        lambda: DF.fold_gate("bv_pulsera", geneva, sorted({d["spec"] for d in geneva}))["held_out"])
df = [dict(spec=s, subject_spec=s) for s in ("17-1882", "17-1905", "18-0725", "18-1109", "18-2799", "18-2800")]
attempt("T5b cios_fusion fold gate (six specimens, one per group)",
        lambda: DF.fold_gate("cios_fusion", df, sorted({d["spec"] for d in df}))["held_out"])
df2 = df + [dict(spec="zz_alias", subject_spec="18-1109")]
attempt("T5c cios_fusion with 18-1109 also filed under a second group",
        lambda: DF.fold_gate("cios_fusion", df2, sorted({d["spec"] for d in df2}))["held_out"])
json.dump(res, open(Path(__file__).resolve().parent / "verify_trust.json", "w"), indent=1, default=str)
