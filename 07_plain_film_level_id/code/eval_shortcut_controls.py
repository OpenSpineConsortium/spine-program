#!/usr/bin/env python
# spine-program/07_plain_film_level_id/code/eval_shortcut_controls.py
# Copied 2026-10-08 from spinesurg-ct-nnunet (private, branch L6_Class, commit 097933a) tools/eval_shortcut_controls.py.
# The repository copy is the one to run; this copy is the record. Runs on the grid in a Slurm job only.
"""NEGATIVE CONTROLS: the experiments that separate this project's numbers from coincidences.

WHY THIS EXISTS. Every headline in this work is a high, plausible number produced by a stack of parts -- a
detector, a fixed-scale crop, a 27-class encoder, a BiGRU over a run, an anchored count over a chain of frames.
A number that high is exactly the shape of this project's recurring failure: finite, reasonable-looking, and
carried by something other than the thing the paper says carries it. Internal consistency has never caught one
of those. What catches them is removing the part that is supposed to be doing the work and showing the number
falls.

The project already runs one such control -- tools/head_mixed_length.py trains the run head on mixed band
lengths and scores on random windows, so the film's own endpoints stop being a cue. This tool adds the rest,
each with an expectation written down BEFORE the result is read, and each with a stated falsifier: the
observation that would mean the project's claim is not supported. The falsifier is evaluated automatically and
written into the JSON, so it cannot be quietly re-read after the fact.

    permute   Retrain the run head on permuted level labels. Two permutations: `shuffle` breaks the
              crop-to-label correspondence entirely, `cyclic` gives each film a random ordinal offset so the
              run's consecutive structure survives but the absolute identity does not. Both are trained with
              permuted labels and scored against the TRUE ones. A global relabelling is NOT used and would be
              no control at all: a consistent bijection is a renaming, and the head would score unchanged.
              Expect: `shuffle` falls to the evaluation set's majority-class rate (computed from the bank, not
              assumed to be 1/27, because the class prior is not uniform).
              FALSIFIES the level model if a head trained on labels that mean nothing still reaches half the
              true-label accuracy, or beats the majority-class rate by more than 10 points: then most of the
              reported accuracy is carried by the structure of the evaluation (one film = one contiguous run,
              a fixed class prior, a fixed field of view) rather than by having learnt what a level looks like.

    anatomy   Mask the vertebral body inside each crop and keep the surround; then the reverse; then keep
              neither (marker channel only). The crop bank already carries the target's own box as channel 1,
              so the ablation is exact and needs no re-cropping. Scored two ways: with the encoder's own
              classifier head (zero-shot, the deployed path) and with a fresh linear read-out fitted per arm on
              the training split -- because masking is out of distribution for an encoder trained on intact
              crops, and without the per-arm read-out a drop could be domain shift rather than lost
              information.
              FALSIFIES the project's central thesis ("teach a net what L4 looks like; do not count from C2")
              if the context-only arm matches the body-only arm, or reaches 90 % of the intact accuracy: the
              level identity would then live in the surrounding field, and a change of field of view -- which
              is the one thing a C-arm does constantly -- would move every call.
              It also falsifies the pixels' role if the marker-only arm reaches half the intact accuracy: the
              box's own geometry would be naming the level.

    scale     Rescale each crop by +-10 and +-20 % about its centre, both channels together. The crops are
              fixed-scale by construction (each body is resampled to tgt_px), so absolute size is not supposed
              to carry identity; a magnification error is what breaks that assumption in the field, and the
              magnification band measured on mobile C-arms in this repo is 1.2 to 1.6, a third of the value.
              FALSIFIES the fixed-scale design if +-20 % costs more than 10 points: the model would be reading
              size, and a device whose magnification is estimated 20 % wrong would be wrong about the level.

    order     Score the trained head with the run's order broken: elements of each window permuted, and the
              window reversed, against the ordered protocol and against the single-crop classifier on the same
              items. The gap between `ordered` and `single` is the work the sequence does.
              FALSIFIES any claim that the chain/run contributes if `shuffled` is within a point of `ordered`:
              the head would not be using order at all and would be averaging neighbours.
              The `reversed` arm answers a second question this project has already been bitten by: 160 of 366
              real DeepFluoro frames are stored upside down, and a head that scores the same reversed is
              direction-blind.

    anchor    Mask the sacrum (or C2) anchor in the PIXELS of a real frame, re-run the detector, re-run the
              count. Three arms on the same frames: intact, anchor masked, and an equal-area control patch
              placed as far from every truth box as it fits -- so a drop can be attributed to the anchor rather
              than to the fact that something was painted out.
              Expect: the sacrum-found rate collapses, naming coverage collapses with it, and the control patch
              changes nothing.
              FALSIFIES the anchor's role if the sacrum is still found on half the frames with its pixels gone:
              the detector would be placing it from the framing convention. That is not hypothetical -- a fixed
              prior box already finds 85.7 % of C-ArmLSpine sacra (or_ready/robust/position_prior.json) -- and
              a sacrum-recall number on such a device is then partly a statement about how the radiographer
              frames, not about the method.

    chain     Hand the linker the sweep's frames in a shuffled order, and in reverse, and count again. Uses
              sweep_map's own station cutting, linking and counting, so the ordered arm reproduces that tool;
              only the order in which the frames are presented changes. Scored with truth boxes, because the
              control is about the chain, not the detector; the embeddings the linker records as a diagnostic
              are stubbed to zero and nothing in the count reads them.
              FALSIFIES the chain if a shuffled sweep counts as accurately as an ordered one: the ordinal would
              be coming from the geometry of a single frame, not from linking the frames.

    dupes     Calls tools/or_audit_dupes.py (not reimplemented) and reads its dupes.json for the one number
              this list needs: whether any test frame is a near-duplicate of a training frame in a DIFFERENT
              case. Same-case pairs are expected and are not leakage; cross-case pairs above the threshold are.

    report    Every control JSON present -> one markdown table, one figure (PNG + PDF), and one verdict list.
    selftest  Builds a synthetic bank and a synthetic sweep, runs every control that does not need a GPU or a
              corpus, and checks the machinery: that each ablation actually changes the pixels it claims to,
              that the arms are scored on the same items, that the falsifier logic fires when it should. It
              tests the plumbing, not the science; it cannot say anything about the real models.

WHAT EVERY CONTROL WRITES. <out>/<control>.json, with a `meta` block (seed, code SHA, tool SHA, every input
path and its hash where it is a file), an `arms` block of measured numbers with case-clustered bootstrap
intervals, and a `verdict` block carrying the expectation, the falsifier, what the control CANNOT say, the
arithmetic used to decide and the boolean. Nothing here invents a number: each arm's accuracy is computed from
the bank, the frames or the renders named in `meta`.

THE KEYS A CLAIM WOULD BE HUNG ON, so docs/RSNAI_CLAIMS.json can point at them and tools/claims_check.py can
re-derive them: `permute.json` arms.true.point / arms.shuffle.point / arms.reference_majority_class.point;
`anatomy.json` arms.<arm>.probe.point and arms.<arm>.zero_shot.point; `scale.json` arms.<zoom>.point;
`order.json` arms.ordered.point / arms.shuffled.point / arms.single_crop.point; `anchor.json`
arms.<arm>.anchor_found.point, arms.<arm>.coverage.point and arms.<arm>.named_and_right.point; `chain.json`
arms.<order>.count_over_bodies.
Every one of them also carries a `ci95` from the case-cluster bootstrap, and every comparison between two arms
is in the `paired` block with the interval of the DIFFERENCE, because two overlapping marginal intervals do not
settle a paired comparison.

TWO QUANTITIES IN HERE ARE NOT WHAT THEY LOOK LIKE, AND BOTH ARE DELIBERATELY NOT THE ONES THE RULES READ.
`anchor.json` arms.<arm>.naming_accuracy is or_crossdev_count's published right/(right+wrong) over the calls a
frame MADE; with the anchor masked a frame that loses its sacrum names nothing, leaves that denominator, and
the arm is then scored on the frames whose anchor survived anyway. `chain.json` arms.<order>.count_exact is
sweep_map's right over the chain NODES that resolved to a truth body, and a scrambled chain resolves fewer of
them. Both are kept, because both are what the published tools compute and the ordered/intact arms have to be
comparable with published rows -- but every arm-to-arm decision and every bar in the figure reads
`named_and_right` and `count_over_bodies`, whose denominators are fixed by the frame and by the sweep and do
not move with the ablation. Any per-source interval is a Wilson interval over crops and is named
`ci95_wilson_item_level`, never `ci95`.

A control that could not apply its own rule writes `verdict.evaluable = false` and says why. It does NOT write
a bare `falsifier_met = false`, which would read as a pass.

    python tools/eval_shortcut_controls.py selftest --out /tmp/controls_selftest
    python tools/eval_shortcut_controls.py anatomy --ctx ~/allspine_v7_fov96_ctx --model <encoder.pt> --out <dir>
    python tools/eval_shortcut_controls.py permute --ctx ~/allspine_v7_fov96_ctx --model <encoder.pt> --out <dir>
    python tools/eval_shortcut_controls.py anchor  --bin <bin dir> --weights <yolo.pt> --out <dir>
    python tools/eval_shortcut_controls.py chain   --drr ~/ctsp_drr --out <dir>
    python tools/eval_shortcut_controls.py report  --out <dir>
"""
from __future__ import annotations

import argparse
import collections
import glob
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eval_gate as EG  # noqa: E402
REPO = Path(__file__).resolve().parents[1]

N_BOOT = 2000            # the project's convention (tools/or_recall_curves.py, carmlspine_pool_scores.py)
BOOT_SEED = 0

# ---------------------------------------------------------------------------------------------------------------
# The pre-stated expectations. These are written here, in the tool, so that they are in git before a result is
# read, and every control JSON copies its entry verbatim into its `verdict` block.
# ---------------------------------------------------------------------------------------------------------------
FALSIFIERS = {
    "permute": {
        "expectation": "A head trained on labels that no longer correspond to the crops falls to the evaluation "
                       "set's majority-class rate. The cyclic arm, which keeps the run's consecutive structure "
                       "but moves the whole column, lands above the majority rate and far below the true arm.",
        "falsifies": "The level model's reported accuracy is not carried by having learnt the level: a head "
                     "trained on meaningless labels reaches a large share of it from the structure of the "
                     "evaluation alone.",
        "criterion": "shuffle_exact >= 0.5 * true_exact  OR  shuffle_exact >= majority_rate + 0.10",
        "limitation": "Only the RUN HEAD is retrained. The encoder underneath was fitted on true labels and its "
                      "embeddings already separate levels, so this control cannot say what an encoder trained on "
                      "permuted labels would do -- it says what the sequence model contributes on top of an "
                      "honest encoder. A full permutation control would retrain the encoder and costs a GPU day.",
    },
    "anatomy": {
        "expectation": "The vertebral body carries the level: body-only keeps most of the intact accuracy and "
                       "context-only falls a long way below it. Marker-only, which has no pixels at all, sits "
                       "near the majority-class rate.",
        "falsifies": "The thesis that local morphology names the vertebra. If the surround alone names it, the "
                     "model is reading the field of view, and the number will not survive a change of framing.",
        "criterion": "context_only >= body_only  OR  context_only >= 0.90 * intact  OR  marker_only >= 0.5 * intact",
        "limitation": "A masked crop is out of distribution for an encoder trained on intact ones, so the "
                      "zero-shot arms understate every ablation by an unknown amount. The linear probe fitted "
                      "per arm is what makes the comparison about information rather than domain shift; read "
                      "the probe row, and read the zero-shot row only as what the deployed path would do.",
    },
    "scale": {
        "expectation": "Crops are fixed-scale by construction, so a +-20 % rescale costs little; the curve over "
                       "zoom is flat within a few points.",
        "falsifies": "The fixed-scale design. A model that loses more than ten points to a 20 % rescale is "
                     "reading absolute size, and C-arm magnification varies by more than that between patients "
                     "and air gaps.",
        "criterion": "max(|exact(0.8) - exact(1.0)|, |exact(1.2) - exact(1.0)|) > 0.10",
        "limitation": "Rescaling an already-cut crop also resamples it, so part of any drop is interpolation "
                      "blur rather than size. The 0.9 and 1.1 arms bound that: a change that is already most of "
                      "the way there at 10 % is resampling, one that grows with the zoom is size.",
    },
    "order": {
        "expectation": "Breaking the run's order costs most of what the run buys: the shuffled and reversed arms "
                       "fall back toward the single-crop classifier on the same items.",
        "falsifies": "Any claim that sequence -- the chain, the run head -- is doing work. If shuffling the order "
                     "costs nothing, the head is averaging neighbours and the ordering is decorative.",
        "criterion": "shuffled_exact >= ordered_exact - 0.01",
        "limitation": "This is the run head's order, not the sweep's. The frames' own order is tested by the "
                      "`chain` control; a head that is order-blind and a linker that is order-blind are two "
                      "different findings and are not interchangeable.",
    },
    "anchor": {
        "expectation": "With the anchor's pixels gone the sacrum is not found, the count has nothing to start "
                       "from and coverage collapses; an equal-area control patch elsewhere changes nothing.",
        "falsifies": "The anchor's role in the count. If the sacrum is still found with its pixels removed, the "
                     "detector is placing it from the device's framing convention, and a sacrum-recall number on "
                     "that device is partly a statement about framing.",
        "criterion": "anchor_found(anchor_masked) >= 0.5  OR  "
                     "named_and_right(anchor_masked) >= named_and_right(intact) - 0.05",
        "criterion_note": "This rule reads `named_and_right`, NOT `naming_accuracy`. `naming_accuracy` is "
                          "right/(right+wrong) over the calls a frame made, which is the published definition "
                          "and is kept in the result -- but with the anchor masked a frame that loses its "
                          "sacrum makes NO calls (name_levels returns all-None), so it leaves the denominator "
                          "entirely. The surviving frames are the ones whose anchor was found anyway, and "
                          "their accuracy is near the intact arm's by construction. Measured on a synthetic "
                          "bin where the anchor was destroyed on every frame and a framing prior recovered it "
                          "on 46 %: naming_accuracy read 100.0 % on both arms (n 120 -> 55, cases 8 -> 5) "
                          "while coverage fell 100 % -> 45.8 %. `named_and_right` is right over EVERY "
                          "scoreable truth vertebra in the frame, so all three arms share one denominator and "
                          "a frame that named nothing counts as nothing named.",
        "limitation": "Painting a rectangle of the median grey over the anchor removes the anatomy and leaves a "
                      "flat block, which is itself a thing a detector can respond to. The control-patch arm is "
                      "what bounds that: it removes the same number of pixels somewhere the anatomy is not. The "
                      "anchor box comes from the truth, which is legitimate for an ablation and means the arm "
                      "cannot be run on frames whose anchor is unlabelled.",
    },
    "chain": {
        "expectation": "A sweep whose frames arrive in a random order cannot be linked into a chain: the chain "
                       "stops being complete, the anchor stops being at the end of it, and the count collapses.",
        "falsifies": "The chain. If a shuffled sweep counts as well as an ordered one, the ordinal is not coming "
                     "from linking overlapping frames and the protocol's central requirement is unnecessary.",
        "criterion": "shuffled_count_over_bodies >= ordered_count_over_bodies - 0.05",
        "criterion_note": "The rule reads `count_over_bodies`, not `count_exact`. `count_exact` is sweep_map's "
                          "own convention -- right over the chain NODES that resolved to a truth body -- and "
                          "is kept in the result so the ordered arm is comparable with the published number. "
                          "But a scrambled chain resolves far fewer nodes, so that denominator SHRINKS with "
                          "the ablation: on the selftest's three synthetic spines the three arms scored 30, 14 "
                          "and 6 vertebrae. `count_over_bodies` divides by the bodies the stations actually "
                          "imaged, which is a property of the sweep and identical in all three arms, so the "
                          "arms are on one scale and a chain that dissolves is not rewarded for it.",
        "limitation": "Run with TRUTH boxes, so it isolates the linker from the detector; with detector boxes "
                      "both arms fall and the gap between them may not be the same one. The sweeps are cut from "
                      "long renders, as sweep_map cuts them, because no real serial sweep of one patient is "
                      "public -- so this is a control on the linker, not on a theatre.",
    },
    "dupes": {
        "expectation": "No test frame is a near-duplicate of a training frame from a different case. Same-case "
                       "pairs are expected (one case contributes several frames to one split) and are not leakage.",
        "falsifies": "The held-out status of the test split: a test frame with a cross-case near-duplicate in "
                     "training has been seen, under another patient's name.",
        "criterion": "any within-dataset train+val vs test cross-case pair at NCC32 >= threshold, OR any frame "
                     "of ours whose nearest neighbour in an external corpus the detector trained on is at "
                     "NCC32 >= threshold",
        "limitation": "NCC32 on a box-downsampled grey image finds the same picture and a mirrored copy is NOT "
                      "found. It is a duplicate test, not a same-patient test: the two split leaks of "
                      "2026-09-22 were the same PERSON under two names with different frames, and no pixel "
                      "measure would have found them. tools/patient_keys.py and tools/leak_check.py are that "
                      "test, and this control does not replace them.",
    },
}

# real-film sources, as head_mixed_length defines them; imported there rather than restated, so the two tools
# cannot drift apart about what counts as a real radiograph
try:
    from head_mixed_length import REAL as REAL_SOURCES, wilson  # noqa: E402
except Exception:  # noqa: BLE001 - only when torch is absent; report/dupes still work
    REAL_SOURCES = {"csxa", "buu_full", "nhanes", "nhanes_drr", "vindr", "aasce"}

    def wilson(k, n):
        if not n:
            return (0.0, 0.0)
        p, z = k / n, 1.96
        d = 1 + z * z / n
        c = (p + z * z / (2 * n)) / d
        h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
        return (max(0.0, c - h), min(1.0, c + h))


# ---------------------------------------------------------------------------------------------------------------
# bookkeeping
# ---------------------------------------------------------------------------------------------------------------
def code_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=str(REPO)).decode().strip()
    except Exception:  # noqa: BLE001
        return None


def file_sha(p):
    try:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()[:16]
    except Exception:  # noqa: BLE001
        return None


def meta_block(control, a, inputs):
    """seed, code SHA, tool SHA and every input path with its hash. The plan's rule of accountability is that a
    number in a table comes from a JSON that says what produced it; this is that block."""
    return {
        "control": control,
        "tool": "tools/eval_shortcut_controls.py",
        "tool_sha256": file_sha(__file__),
        "code_sha": code_sha(),
        "seed": int(getattr(a, "seed", 0)),
        "written": time.strftime("%Y-%m-%d %H:%M:%S"),
        "python": sys.version.split()[0],
        "inputs": {k: ({"path": str(v), "sha256": file_sha(v)} if (v and os.path.isfile(str(v))) else
                       {"path": str(v), "exists": bool(v) and os.path.exists(str(v))})
                   for k, v in inputs.items()},
        "argv": sys.argv,
    }


def boot_cases(vals_by_case, n=N_BOOT, seed=BOOT_SEED):
    """Point estimate and a 95 % interval from a case-cluster bootstrap: resample CASES with replacement and
    pool their items. numpy default_rng, 2,000 resamples, percentile method -- the convention already used by
    tools/or_recall_curves.py, so intervals in this tool and in that one mean the same thing."""
    cases = [c for c, v in vals_by_case.items() if len(v)]
    if not cases:
        return {"n": 0, "cases": 0, "point": None, "ci95": [None, None]}
    rng = np.random.default_rng(seed)
    flat = [v for c in cases for v in vals_by_case[c]]
    point = float(np.mean(flat))
    st = np.empty(n, np.float64)
    arrs = [np.asarray(vals_by_case[c], np.float64) for c in cases]
    for b in range(n):
        pick = rng.integers(0, len(arrs), len(arrs))
        st[b] = np.concatenate([arrs[i] for i in pick]).mean()
    return {"n": len(flat), "cases": len(cases), "point": round(point, 4),
            "ci95": [round(float(np.percentile(st, 2.5)), 4), round(float(np.percentile(st, 97.5)), 4)]}


def boot_paired(a_by_case, b_by_case, n=N_BOOT, seed=BOOT_SEED):
    """The interval of the DIFFERENCE b - a on the SAME cases. Two marginal intervals that overlap do not settle
    a paired comparison; this does, and the plan requires it for every 'beats' claim."""
    cases = [c for c in a_by_case if c in b_by_case and len(a_by_case[c]) and len(b_by_case[c])]
    if not cases:
        return {"cases": 0, "delta": None, "ci95": [None, None]}
    rng = np.random.default_rng(seed)
    A = [np.asarray(a_by_case[c], np.float64) for c in cases]
    B = [np.asarray(b_by_case[c], np.float64) for c in cases]
    delta = float(np.concatenate(B).mean() - np.concatenate(A).mean())
    st = np.empty(n, np.float64)
    for b in range(n):
        pick = rng.integers(0, len(cases), len(cases))
        st[b] = (np.concatenate([B[i] for i in pick]).mean() - np.concatenate([A[i] for i in pick]).mean())
    return {"cases": len(cases), "delta": round(delta, 4),
            "ci95": [round(float(np.percentile(st, 2.5)), 4), round(float(np.percentile(st, 97.5)), 4)],
            "excludes_zero": bool(np.percentile(st, 2.5) > 0 or np.percentile(st, 97.5) < 0)}


def write_result(out_dir, control, meta, arms, verdict, extra=None):
    os.makedirs(out_dir, exist_ok=True)
    doc = {"meta": meta, "arms": arms, "verdict": verdict}
    if extra:
        doc.update(extra)
    if _GATE["blk"] is not None:                 # the verdict of the gate this control ran before scoring
        doc = EG.stamp(doc, _GATE["blk"])
    p = os.path.join(out_dir, f"{control}.json")
    json.dump(doc, open(p, "w"), indent=1, default=_json_default)
    print(f"\nwrote {p}")
    print(f"  expectation: {verdict['expectation']}")
    print(f"  limitation : {verdict.get('limitation', '-')}")
    print(f"  falsifier  : {verdict['criterion']}")
    if not verdict.get("evaluable", True):
        print(f"  VERDICT    : NOT EVALUABLE -- {verdict.get('not_evaluable_because', 'an arm the rule needs '
                                                            'is missing')}. 'falsifier_met' is false because "
              f"the rule could not be applied, NOT because the control passed.")
    else:
        print(f"  VERDICT    : {'FALSIFIER MET -- the claim is not supported by this control' if verdict['falsifier_met'] else 'falsifier not met'}")
    return p


def _json_default(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    return str(o)


def verdict_for(control, met, numbers, evaluable=True, because=None):
    """`evaluable` is the difference between 'the rule was applied and did not fire' and 'the rule could not be
    applied'. Both used to write falsifier_met = false, which reads as a pass; a control that could not decide
    must not be readable as a control that decided in the project's favour."""
    v = dict(FALSIFIERS[control])
    v["falsifier_met"] = bool(met) and bool(evaluable)
    v["evaluable"] = bool(evaluable)
    if not evaluable:
        v["not_evaluable_because"] = because or "an arm the decision rule needs is missing or empty"
    v["numbers_used"] = numbers
    return v


# ---------------------------------------------------------------------------------------------------------------
# the crop bank
# ---------------------------------------------------------------------------------------------------------------
# THE GATE (tools/eval_gate.py; docs/DATA_ACCOUNTING.md 5.3, not opt-in). Each control that loads weights gates them
# on the patients it scores BEFORE it scores; write_result then writes the verdict first in the control's JSON. A
# read-out or head this tool fits on the bank's train split is checked as a model fitted in the run (also_seen). The
# selftest's stub encoder and stub detector have no weights and no patients: their verdict says so, not held out.
_GATE = {"blk": None}


def _gate_bank(a, B, where, fitted_here=None, extra=None):
    if getattr(a, "_stub", None):
        blk = EG.block([], "selftest: a stub encoder -- no weights, no patients; not a held-out number")
    else:
        val = sorted(set(B["case"][B["split"] == "val"].tolist()))
        also = None
        if fitted_here:
            tr = sorted(set(B["case"][B["split"] == "train"].tolist()))
            also = {fitted_here: sorted(EG.key_items([dict(case=c) for c in tr])[0])}
        blk = EG.gate_evaluation([dict(case=c) for c in val], {"encoder": a.model, **(extra or {})}, where, a,
                                 eval_set=f"{B['ctx']}/rung_{B['rung']}.npz#val", also_seen=also)
    _GATE["blk"] = blk
    return blk


def load_bank(ctx, rung):
    """X (N,2,S,S) uint8 -- channel 0 the masked image, channel 1 the TARGET BODY's own box as a mask -- plus
    y, case, split, source. The second channel is what makes the anatomy ablation exact: the body to be named is
    already delineated inside the crop, so it can be kept or removed without re-cropping anything."""
    ctx = Path(os.path.expanduser(ctx))
    classes = json.load(open(ctx / "meta.json"))["classes"]
    z = np.load(ctx / f"rung_{rung}.npz", allow_pickle=True)
    X, y = z["X"], z["y"].astype(np.int64)
    case = np.array([str(c) for c in z["case"]])
    split = np.array([str(s) for s in z["split"]])
    src = np.array([str(s) for s in z["source"]]) if "source" in z.files else np.array(["?"] * len(y))
    if X.ndim != 4 or X.shape[1] != 2:
        raise SystemExit(f"{ctx}/rung_{rung}.npz has X of shape {X.shape}; expected (N,2,S,S)")
    return dict(X=X, y=y, case=case, split=split, source=src, classes=classes, ctx=str(ctx), rung=str(rung))


def majority_rate(y_eval):
    """The evaluation set's own majority-class rate: what a model that has learnt nothing but the class prior
    scores. Quoting 1/27 as 'chance' here would understate chance, because the prior is not uniform."""
    if not len(y_eval):
        return None, None
    c = collections.Counter(int(v) for v in y_eval)
    k, n = c.most_common(1)[0][1], len(y_eval)
    return k / n, {"n": n, "classes_present": len(c), "uniform_rate": round(1.0 / len(c), 4)}


def load_encoder(model_path, n_classes, dev):
    import torch.nn as nn
    from night_loadmodel import load_level_model
    model, spec = load_level_model(model_path, n_classes, dev)
    fc = model.fc
    model.fc = nn.Identity()
    model.eval()
    return model, fc, spec


# ---- crop transforms (every one of them operates on a float batch in [0,1] on the device) -----------------------
def tf_none(xb):
    return xb


def tf_body_only(xb):
    """Keep the pixels inside the target body's own box; zero everything else in the image channel. The marker
    channel is left alone, so the network still knows which body it is being asked about -- otherwise the arm
    would be testing two things at once."""
    m = (xb[:, 1:2] > 0.5).float()
    return xb.clone().index_copy_(1, _ix(xb, 0), xb[:, 0:1] * m)


def tf_context_only(xb):
    """The reverse: zero the target body, keep the surround."""
    m = (xb[:, 1:2] > 0.5).float()
    return xb.clone().index_copy_(1, _ix(xb, 0), xb[:, 0:1] * (1.0 - m))


def tf_marker_only(xb):
    """No pixels at all: only the target's box. The floor for how much the crop's geometry alone can name."""
    return xb.clone().index_copy_(1, _ix(xb, 0), xb[:, 0:1] * 0.0)


def _ix(xb, i):
    import torch
    return torch.tensor([i], device=xb.device)


def make_zoom(s):
    """Rescale BOTH channels about the crop centre by s, keeping the canvas size: a magnification error, which
    is what a mis-estimated air gap or source-to-image distance does to a real frame."""
    import torch
    import torch.nn.functional as F

    def tf(xb):
        if abs(s - 1.0) < 1e-9:
            return xb
        N, C, H, W = xb.shape
        nh, nw = max(1, int(round(H * s))), max(1, int(round(W * s)))
        r = F.interpolate(xb, size=(nh, nw), mode="bilinear", align_corners=False)
        if s >= 1.0:
            y0, x0 = (nh - H) // 2, (nw - W) // 2
            return r[:, :, y0:y0 + H, x0:x0 + W]
        out = torch.zeros_like(xb)
        y0, x0 = (H - nh) // 2, (W - nw) // 2
        out[:, :, y0:y0 + nh, x0:x0 + nw] = r
        return out
    return tf


def embed_and_score(model, fc, X, dev, tf=None, bs=256, idx=None):
    """-> (embeddings (N,d) cpu tensor, predicted class (N,) int). One pass, so every arm sees the same items.

    `idx` selects a subset WITHOUT copying the bank: X[mask] on a 50,000-crop bank is an 8 GB allocation, and
    four ablation arms would make it four times over. Slicing per batch keeps the peak at one batch."""
    import torch
    sel = np.arange(len(X)) if idx is None else np.asarray(idx)
    embs, preds = [], []
    with torch.no_grad():
        for i in range(0, len(sel), bs):
            xb = torch.from_numpy(np.ascontiguousarray(X[sel[i:i + bs]])).float().div_(255.0).to(dev)
            if tf is not None:
                xb = tf(xb)
            e = model(xb)
            embs.append(e.cpu())
            preds.append(fc(e).argmax(1).cpu())
    return torch.cat(embs), torch.cat(preds).numpy()


def linear_probe(Etr, ytr, Eva, n_classes, dev, epochs=300, lr=1e-2, seed=0):
    """A fresh linear read-out fitted on THIS arm's own training embeddings. Without it, an ablation arm is
    scored by a classifier that never saw an ablated crop, and a drop could be domain shift rather than lost
    information. With it, each arm is given its best chance and the comparison is about what is still in the
    features."""
    import torch
    import torch.nn as nn
    torch.manual_seed(seed)
    lin = nn.Linear(Etr.shape[1], n_classes).to(dev)
    opt = torch.optim.AdamW(lin.parameters(), lr=lr, weight_decay=1e-4)
    Xt = Etr.to(dev)
    yt = torch.from_numpy(np.asarray(ytr)).long().to(dev)
    mu, sd = Xt.mean(0, keepdim=True), Xt.std(0, keepdim=True).clamp_min(1e-6)
    Xt = (Xt - mu) / sd
    for _ in range(epochs):
        opt.zero_grad()
        loss = nn.functional.cross_entropy(lin(Xt), yt)
        loss.backward()
        opt.step()
    with torch.no_grad():
        Xv = (Eva.to(dev) - mu) / sd
        return lin(Xv).argmax(1).cpu().numpy()


def per_case_hits(pred, y, case, mask):
    d = collections.defaultdict(list)
    for i in np.nonzero(mask)[0]:
        d[str(case[i])].append(float(pred[i] == y[i]))
    return d


def per_source(pred, y, src, mask, case=None):
    """Per-source accuracy. The interval here is NOT the case-clustered one the arms carry.

    A Wilson interval treats every crop as independent, and crops from one film are not: a film contributes a
    whole column of neighbouring vertebrae. So the key is named `ci95_wilson_item_level`, never `ci95`, because
    a reader keying on `ci95` elsewhere in this file gets a case-clustered interval and would otherwise be
    handed a too-narrow one under the same name. Where the case labels are passed, the clustered interval is
    computed beside it and IS called ci95."""
    out = {}
    for s in sorted(set(str(v) for v in src[mask])):
        sel = np.nonzero(mask & (src == s))[0]
        if len(sel):
            k = int(sum(pred[i] == y[i] for i in sel))
            row = {"n": len(sel), "exact": round(k / len(sel), 4),
                   "ci95_wilson_item_level": [round(v, 4) for v in wilson(k, len(sel))],
                   "ci95_note": "the Wilson interval treats each crop as independent and is too narrow; "
                                "`ci95` on this row, where present, is the case-clustered bootstrap"}
            if case is not None:
                d = collections.defaultdict(list)
                for i in sel:
                    d[str(case[i])].append(float(pred[i] == y[i]))
                b = boot_cases(d)
                row["ci95"] = b["ci95"]
                row["cases"] = b["cases"]
            out[s] = row
    return out


# ---------------------------------------------------------------------------------------------------------------
# control: anatomy
# ---------------------------------------------------------------------------------------------------------------
def cmd_anatomy(a):
    import torch
    dev = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    B = load_bank(a.ctx, a.rung)
    X, y, case, split, src, classes = B["X"], B["y"], B["case"], B["split"], B["source"], B["classes"]
    va = split == "val"
    tr = split == "train"
    iva, itr = np.nonzero(va)[0], np.nonzero(tr)[0]
    if not len(iva):
        raise SystemExit(f"{B['ctx']} rung {B['rung']} has no val items; nothing to score")
    _gate_bank(a, B, "tools/eval_shortcut_controls.py anatomy",
               fitted_here="the linear read-out per arm, fitted here on the train split" if a.probe else None)
    model, fc, spec = (a._stub if getattr(a, "_stub", None) else load_encoder(a.model, len(classes), dev))
    maj, maj_meta = majority_rate(y[va])
    arms = {}
    ARMS = [("intact", tf_none), ("body_only", tf_body_only), ("context_only", tf_context_only),
            ("marker_only", tf_marker_only)]
    hits_by_case = {}
    for name, tf in ARMS:
        Eva, pva = embed_and_score(model, fc, X, dev, tf, a.bs, idx=iva)
        hits = per_case_hits(pva, y[va], case[va], np.ones(va.sum(), bool))
        row = {"zero_shot": boot_cases(hits, seed=a.seed),
               "zero_shot_per_source": per_source(pva, y[va], src[va], np.ones(va.sum(), bool), case[va])}
        hits_by_case[name] = hits
        if a.probe:
            Etr, _ = embed_and_score(model, fc, X, dev, tf, a.bs, idx=itr)
            pp = linear_probe(Etr, y[itr], Eva, len(classes), dev, epochs=a.probe_epochs, seed=a.seed)
            row["probe"] = boot_cases(per_case_hits(pp, y[va], case[va], np.ones(va.sum(), bool)), seed=a.seed)
            hits_by_case[name + "/probe"] = per_case_hits(pp, y[va], case[va], np.ones(va.sum(), bool))
            del Etr
        arms[name] = row
        print(f"  {name:<13} zero-shot {100 * row['zero_shot']['point']:6.2f}% "
              f"[{100 * row['zero_shot']['ci95'][0]:.2f}, {100 * row['zero_shot']['ci95'][1]:.2f}]"
              + (f"   probe {100 * row['probe']['point']:6.2f}%" if a.probe else ""), flush=True)
        del Eva
    key = "probe" if a.probe else "zero_shot"
    g = lambda n: arms[n][key]["point"]  # noqa: E731
    met = (g("context_only") >= g("body_only") or g("context_only") >= 0.90 * g("intact")
           or g("marker_only") >= 0.5 * g("intact"))
    paired = {"body_only_minus_context_only":
              boot_paired(hits_by_case["context_only" + ("/probe" if a.probe else "")],
                          hits_by_case["body_only" + ("/probe" if a.probe else "")], seed=a.seed),
              "intact_minus_body_only":
              boot_paired(hits_by_case["body_only" + ("/probe" if a.probe else "")],
                          hits_by_case["intact" + ("/probe" if a.probe else "")], seed=a.seed)}
    v = verdict_for("anatomy", met, {"scored_with": key, "intact": g("intact"), "body_only": g("body_only"),
                                     "context_only": g("context_only"), "marker_only": g("marker_only"),
                                     "majority_rate": round(maj, 4) if maj else None})
    meta = meta_block("anatomy", a, {"ctx": B["ctx"], "encoder": a.model})
    meta["bank"] = {"rung": B["rung"], "n_val": int(va.sum()), "n_train": int(tr.sum()),
                    "classes": len(classes), "majority_rate": round(maj, 4) if maj else None, **(maj_meta or {})}
    meta["encoder_spec"] = spec if isinstance(spec, dict) else str(spec)
    return write_result(a.out, "anatomy", meta, arms, v, {"paired": paired})


# ---------------------------------------------------------------------------------------------------------------
# control: scale
# ---------------------------------------------------------------------------------------------------------------
def cmd_scale(a):
    import torch
    dev = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    B = load_bank(a.ctx, a.rung)
    X, y, case, split, src, classes = B["X"], B["y"], B["case"], B["split"], B["source"], B["classes"]
    va = split == "val"
    iva = np.nonzero(va)[0]
    _gate_bank(a, B, "tools/eval_shortcut_controls.py scale")
    model, fc, spec = (a._stub if getattr(a, "_stub", None) else load_encoder(a.model, len(classes), dev))
    arms, hits_by_case = {}, {}
    for s in a.zooms:
        _, p = embed_and_score(model, fc, X, dev, make_zoom(s), a.bs, idx=iva)
        hits = per_case_hits(p, y[va], case[va], np.ones(va.sum(), bool))
        hits_by_case[s] = hits
        arms[f"{s:g}"] = {**boot_cases(hits, seed=a.seed), "zoom": s,
                          "per_source": per_source(p, y[va], src[va], np.ones(va.sum(), bool), case[va])}
        print(f"  zoom {s:>4g}x  {100 * arms[f'{s:g}']['point']:6.2f}% "
              f"[{100 * arms[f'{s:g}']['ci95'][0]:.2f}, {100 * arms[f'{s:g}']['ci95'][1]:.2f}]  n={arms[f'{s:g}']['n']}", flush=True)
    base = arms.get("1", arms[f"{min(a.zooms, key=lambda z: abs(z - 1)):g}"])["point"]
    lo = arms.get("0.8", {}).get("point")
    hi = arms.get("1.2", {}).get("point")
    drops = [abs(v - base) for v in (lo, hi) if v is not None]
    # the rule names exact(0.8) and exact(1.2); without those arms it has nothing to decide on, and a verdict
    # of "not met" would read as a pass
    evaluable = bool(drops) and 1.0 in [float(z) for z in a.zooms]
    met = evaluable and max(drops) > 0.10
    paired = ({f"{s:g}_minus_1": boot_paired(hits_by_case[1.0], hits_by_case[s], seed=a.seed)
               for s in a.zooms if s != 1.0} if 1.0 in hits_by_case else
              {"note": "no 1.0 zoom requested, so there is no unrescaled arm to pair against"})
    v = verdict_for("scale", met, {"exact_at_1.0": base, "exact_at_0.8": lo, "exact_at_1.2": hi,
                                   "max_abs_change": round(max(drops), 4) if drops else None},
                    evaluable, "the rule needs the 0.8, 1.0 and 1.2 arms and at least one of them was not run")
    meta = meta_block("scale", a, {"ctx": B["ctx"], "encoder": a.model})
    meta["bank"] = {"rung": B["rung"], "n_val": int(va.sum()), "classes": len(classes),
                    "tgt_px": json.load(open(Path(B["ctx"]) / "meta.json")).get("tgt_px")
                    if (Path(B["ctx"]) / "meta.json").exists() else None}
    meta["encoder_spec"] = spec if isinstance(spec, dict) else str(spec)
    return write_result(a.out, "scale", meta, arms, v, {"paired": paired})


# ---------------------------------------------------------------------------------------------------------------
# the run head: shared training and scoring for `permute` and `order`
# ---------------------------------------------------------------------------------------------------------------
def _films(y, case, split, which):
    """Group the bank into films and return the ones on `which` side of the split.

    A film's side is taken from its FIRST crop, which is only correct if every crop of a case is on one side.
    That is the bank's contract and it is checked rather than assumed: a case straddling the split would put
    its held-out crops into the training windows of the run head, which is a leak of exactly the kind this
    project found twice on 2026-09-22 -- and it would be invisible, because the tool would still print a
    plausible number."""
    by = collections.defaultdict(list)
    for i in range(len(y)):
        by[str(case[i])].append(i)
    mixed = [f for f, idx in by.items() if len({str(split[i]) for i in idx}) > 1]
    if mixed:
        raise SystemExit(
            f"{len(mixed)} cases have crops on both sides of the split (e.g. {mixed[:5]}). This tool assigns a "
            f"whole film to the side of its first crop, so a straddling case would train the run head on its "
            f"own held-out crops. Fix the bank's split before running any control on it.")
    for f in by:
        by[f].sort(key=lambda i: int(y[i]))     # anatomical order: the run, top to bottom
    return by, [f for f, idx in by.items() if str(split[idx[0]]) == which]


def train_head(Fm, y_train_labels, by_film, films, C, dev, kmax, epochs, bs, lr, seed, tag=""):
    """head_mixed_length's mixed-length loop, reduced to what a control needs: a fresh window length and offset
    every epoch so the film's endpoints are never a fixed cue. `y_train_labels` is what the head is TOLD; the
    scorer always compares against the true labels, which is what makes the permutation arms controls rather
    than relabellings."""
    import torch
    import torch.nn.functional as F
    from recurrent_order import RunLabeller
    torch.manual_seed(seed)
    rng = np.random.RandomState(seed)
    d_in = Fm.shape[1]
    net = RunLabeller(d_in, C).to(dev)
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)
    Lmax = 2 * kmax + 1
    for ep in range(epochs):
        net.train()
        wins = []
        for f in films:
            idx = by_film[f]
            n = len(idx)
            if n < 2:
                continue
            for _ in range(max(1, n // 3)):
                L = min(int(rng.randint(2, Lmax + 1)), n)
                s = int(rng.randint(0, n - L + 1))
                wins.append(idx[s:s + L])
        order = np.arange(len(wins))
        rng.shuffle(order)
        tot = 0.0
        for b in range(0, len(order), bs):
            ids = order[b:b + bs]
            LM = max(len(wins[i]) for i in ids)
            xb = torch.zeros(len(ids), LM, d_in)
            yb = torch.full((len(ids), LM), -100, dtype=torch.long)
            for r, i in enumerate(ids):
                w = wins[i]
                xb[r, :len(w)] = Fm[w]
                yb[r, :len(w)] = torch.tensor([int(y_train_labels[j]) for j in w])
            xb = xb.to(dev)
            xb = xb * (torch.rand(xb.shape[:2], device=dev) > 0.1).unsqueeze(-1).float()
            loss = F.cross_entropy(net(xb).reshape(-1, C), yb.reshape(-1).to(dev), ignore_index=-100)
            opt.zero_grad(); loss.backward(); opt.step()
            tot += float(loss.detach()) * len(ids)
        sched.step()
        if ep % 10 == 0 or ep == epochs - 1:
            print(f"    {tag}ep {ep:>3} windows {len(wins):>6} loss {tot / max(1, len(order)):.4f}", flush=True)
    net.eval()
    return net


def score_head(net, Fm, y_true, by_film, films, classes, dev, k, mode="ordered", seed=0):
    """Each target scored inside its maximal band of 2k+1, as the published protocol does.

      ordered    the run in anatomical order
      shuffled   the SAME window with its elements permuted; the target is read back at the position it was
                 moved to, so the network sees a scrambled spine and is still asked about the same vertebra
      reversed   the same window end to end
    """
    import torch
    rng = np.random.RandomState(seed)
    hits = collections.defaultdict(list)
    per_lvl = collections.defaultdict(list)
    with torch.no_grad():
        for f in films:
            idx = by_film[f]
            n = len(idx)
            for pos, i in enumerate(idx):
                lo, hi = max(0, pos - k), min(n, pos + k + 1)
                w = list(idx[lo:hi])
                tpos = pos - lo
                if mode == "shuffled":
                    perm = rng.permutation(len(w))
                    w = [w[j] for j in perm]
                    tpos = int(np.nonzero(perm == (pos - lo))[0][0])
                elif mode == "reversed":
                    w = w[::-1]
                    tpos = len(w) - 1 - (pos - lo)
                if not w or tpos >= len(w):
                    continue
                out = net(Fm[w].unsqueeze(0).to(dev))[0]
                p = int(out[tpos].argmax())
                ok = float(p == int(y_true[i]))
                hits[f].append(ok)
                per_lvl[classes[int(y_true[i])]].append(ok)
    return hits, {k2: {"n": len(v), "exact": round(float(np.mean(v)), 4)} for k2, v in per_lvl.items()}


def _bank_and_embeddings(a):
    import torch
    dev = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    B = load_bank(a.ctx, a.rung)
    classes = B["classes"]
    head_given = getattr(a, "head", None)
    _gate_bank(a, B, f"tools/eval_shortcut_controls.py {getattr(a, 'cmd', 'permute/order')}",
               fitted_here=None if head_given else "the run head trained here on the train split",
               extra={"head": os.path.expanduser(head_given)} if head_given else None)
    model, fc, spec = (a._stub if getattr(a, "_stub", None) else load_encoder(a.model, len(classes), dev))
    E, single_pred = embed_and_score(model, fc, B["X"], dev, None, a.bs)
    print(f"  embedded {len(E)} crops into {E.shape[1]} dims", flush=True)
    return B, classes, E, single_pred, dev, spec


def cmd_permute(a):
    B, classes, Fm, single_pred, dev, spec = _bank_and_embeddings(a)
    y, case, split, src = B["y"], B["case"], B["split"], B["source"]
    by_film, tr_films = _films(y, case, split, "train")
    _, va_films = _films(y, case, split, "val")
    print(f"  {len(tr_films)} training films, {len(va_films)} held-out films", flush=True)
    va_mask = split == "val"
    maj, maj_meta = majority_rate(y[va_mask])
    rng = np.random.RandomState(a.seed)

    # the three label sets the head is TRAINED on. Evaluation is always against y.
    labels = {"true": y.copy()}
    sh = y.copy()
    tr_idx = np.nonzero(split == "train")[0]
    sh[tr_idx] = y[tr_idx][rng.permutation(len(tr_idx))]      # crop <-> label correspondence destroyed
    labels["shuffle"] = sh
    cy = y.copy()
    n_ident = 0
    for f in tr_films:                                        # each film's whole column moved by a random offset
        idx = by_film[f]
        # 1..C-1, never 0: an offset of zero leaves that film's labels TRUE, and with 27 classes about one
        # film in 27 would have been trained on honest labels inside the arm that is meant to have none
        off = int(rng.randint(1, len(classes)))
        n_ident += int(off == 0)
        for i in idx:
            cy[i] = (int(y[i]) + off) % len(classes)
    labels["cyclic"] = cy

    arms, hits_by_case = {}, {}
    for name in ("true", "shuffle", "cyclic"):
        print(f"  training head on {name} labels", flush=True)
        net = train_head(Fm, labels[name], by_film, tr_films, len(classes), dev, getattr(a, "train_kmax", 4),
                         a.epochs, a.bs_head, a.lr, a.seed, tag=f"{name}: ")
        hits, per_lvl = score_head(net, Fm, y, by_film, va_films, classes, dev, a.k, "ordered", a.seed + 1)
        hits_by_case[name] = hits
        arms[name] = {**boot_cases(hits, seed=a.seed), "per_level": per_lvl,
                      "trained_on": ("true levels" if name == "true" else
                                     "levels shuffled across all training crops" if name == "shuffle" else
                                     "each training film's column shifted by a random ordinal offset")}
        print(f"  {name:<8} exact {100 * arms[name]['point']:6.2f}% "
              f"[{100 * arms[name]['ci95'][0]:.2f}, {100 * arms[name]['ci95'][1]:.2f}]  "
              f"n={arms[name]['n']} over {arms[name]['cases']} films", flush=True)
        if a.save_head:
            import torch
            os.makedirs(a.out, exist_ok=True)
            torch.save(net.state_dict(), os.path.join(a.out, f"head_permute_{name}_seed{a.seed}.pt"))
        del net

    arms["reference_majority_class"] = {"point": round(maj, 4) if maj else None, "ci95": [None, None],
                                        "note": "the val set's own majority-class rate: what a model that "
                                                "learnt only the class prior scores", **(maj_meta or {})}
    met = (arms["shuffle"]["point"] >= 0.5 * arms["true"]["point"]
           or (maj is not None and arms["shuffle"]["point"] >= maj + 0.10))
    paired = {"true_minus_shuffle": boot_paired(hits_by_case["shuffle"], hits_by_case["true"], seed=a.seed),
              "true_minus_cyclic": boot_paired(hits_by_case["cyclic"], hits_by_case["true"], seed=a.seed)}
    v = verdict_for("permute", met, {"true": arms["true"]["point"], "shuffle": arms["shuffle"]["point"],
                                     "cyclic": arms["cyclic"]["point"],
                                     "majority_rate": round(maj, 4) if maj else None})
    meta = meta_block("permute", a, {"ctx": B["ctx"], "encoder": a.model})
    meta["bank"] = {"rung": B["rung"], "train_films": len(tr_films), "val_films": len(va_films),
                    "classes": len(classes), "band": 2 * a.k + 1, "epochs": a.epochs,
                    "train_window_lengths": f"2..{2 * getattr(a, 'train_kmax', 4) + 1}",
                    "train_kmax": getattr(a, "train_kmax", 4),
                    "note": "the band is the SCORING band (2k+1); train_window_lengths is what the head was "
                            "trained on and must match head_mixed_length's --kmax for the true arm to be "
                            "comparable with a published row"}
    meta["encoder_spec"] = spec if isinstance(spec, dict) else str(spec)
    extra = {}
    if a.reference_json and os.path.exists(os.path.expanduser(a.reference_json)):
        # AN EXTERNAL CHECK ON THE TRUE ARM. The control's true-label head should reproduce the published
        # mixed-length head on the same bank at the same band; if it does not, the control's own training is
        # what moved, and the permutation arms cannot be read against the published number.
        ref = json.load(open(os.path.expanduser(a.reference_json)))
        band = 2 * a.k + 1
        hit = [r for r in ref.get("results", []) if r.get("band") == band]
        # THE REFERENCE MUST BE THE SAME BANK. head_mixed_length records the bank it was fitted on; the runner
        # picks the file by a glob over filenames, and a --tag that does not carry the bank's directory name
        # (which is what slurm/allspine_v8_train.sh passes) makes that glob fall through to whatever mixed_*.json
        # is newest. Comparing this arm with a head fitted on another bank would report a bank difference as a
        # drift in this control's training, which is the opposite of what the block is for.
        ref_bank = str(ref.get("bank") or "")
        same_bank = bool(ref_bank) and os.path.basename(ref_bank.rstrip("/\\")) == os.path.basename(str(B["ctx"]).rstrip("/\\"))
        if hit and same_bank:
            extra["reference"] = {"file": a.reference_json, "band": band, "published_exact": hit[0]["exact"],
                                  "reference_bank": ref_bank, "this_bank": B["ctx"],
                                  "this_train_kmax": getattr(a, "train_kmax", None),
                                  "train_kmax_note": "head_mixed_length's --kmax must equal this, or the two "
                                                     "heads saw different window-length distributions and the "
                                                     "difference below is not drift in this control",
                                  "this_true_arm": arms["true"]["point"],
                                  "difference": round(arms["true"]["point"] - hit[0]["exact"], 4)}
            print(f"  reference: published band-{band} exact {100 * hit[0]['exact']:.2f}% vs this true arm "
                  f"{100 * arms['true']['point']:.2f}%", flush=True)
        else:
            extra["reference"] = {"file": a.reference_json, "band": band, "reference_bank": ref_bank or None,
                                  "this_bank": B["ctx"], "compared": False,
                                  "why": ("the reference was fitted on a DIFFERENT bank, so it is recorded and "
                                          "not compared" if hit and not same_bank else
                                          f"the reference file carries no band-{band} row")}
            print(f"  reference NOT comparable: {extra['reference']['why']} "
                  f"(reference bank {ref_bank or '?'}, this bank {B['ctx']})", flush=True)
    return write_result(a.out, "permute", meta, arms, v, extra)


def cmd_order(a):
    B, classes, Fm, single_pred, dev, spec = _bank_and_embeddings(a)
    y, case, split = B["y"], B["case"], B["split"]
    by_film, tr_films = _films(y, case, split, "train")
    _, va_films = _films(y, case, split, "val")
    if a.head:
        import torch
        from recurrent_order import RunLabeller
        net = RunLabeller(Fm.shape[1], len(classes)).to(dev)
        net.load_state_dict(torch.load(os.path.expanduser(a.head), map_location=dev))
        net.eval()
        head_src = os.path.expanduser(a.head)
    else:
        print("  no --head given; training one on the true labels with the same loop the permute control uses",
              flush=True)
        net = train_head(Fm, y, by_film, tr_films, len(classes), dev, getattr(a, "train_kmax", 4), a.epochs,
                         a.bs_head, a.lr, a.seed)
        head_src = "trained here (true labels)"
    arms, hits_by_case = {}, {}
    for mode in ("ordered", "shuffled", "reversed"):
        hits, per_lvl = score_head(net, Fm, y, by_film, va_films, classes, dev, a.k, mode, a.seed + 1)
        hits_by_case[mode] = hits
        arms[mode] = {**boot_cases(hits, seed=a.seed), "per_level": per_lvl}
        print(f"  {mode:<9} exact {100 * arms[mode]['point']:6.2f}% "
              f"[{100 * arms[mode]['ci95'][0]:.2f}, {100 * arms[mode]['ci95'][1]:.2f}]", flush=True)
    # the same items named by the single-crop classifier alone: no sequence at any point
    sing = collections.defaultdict(list)
    va_set = set(va_films)
    for i in range(len(y)):
        if str(case[i]) in va_set:
            sing[str(case[i])].append(float(single_pred[i] == y[i]))
    hits_by_case["single_crop"] = sing
    arms["single_crop"] = {**boot_cases(sing, seed=a.seed),
                           "note": "the encoder's own per-crop classifier on the same held-out items; no run, "
                                   "no order, no neighbours"}
    print(f"  {'single':<9} exact {100 * arms['single_crop']['point']:6.2f}%", flush=True)
    met = arms["shuffled"]["point"] >= arms["ordered"]["point"] - 0.01
    paired = {"ordered_minus_shuffled": boot_paired(hits_by_case["shuffled"], hits_by_case["ordered"], seed=a.seed),
              "ordered_minus_reversed": boot_paired(hits_by_case["reversed"], hits_by_case["ordered"], seed=a.seed),
              "ordered_minus_single": boot_paired(hits_by_case["single_crop"], hits_by_case["ordered"], seed=a.seed)}
    v = verdict_for("order", met, {"ordered": arms["ordered"]["point"], "shuffled": arms["shuffled"]["point"],
                                   "reversed": arms["reversed"]["point"],
                                   "single_crop": arms["single_crop"]["point"]})
    meta = meta_block("order", a, {"ctx": B["ctx"], "encoder": a.model, "head": a.head})
    meta["head_source"] = head_src
    meta["bank"] = {"rung": B["rung"], "val_films": len(va_films), "classes": len(classes),
                    "band": 2 * a.k + 1, "train_kmax": getattr(a, "train_kmax", 4)}
    meta["encoder_spec"] = spec if isinstance(spec, dict) else str(spec)
    return write_result(a.out, "order", meta, arms, v, {"paired": paired})


# ---------------------------------------------------------------------------------------------------------------
# control: anchor ablation on real frames
# ---------------------------------------------------------------------------------------------------------------
def _mask_patch(arr, box, fill):
    x0, y0, x1, y1 = [int(round(v)) for v in box]
    H, W = arr.shape[:2]
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(W, x1), min(H, y1)
    if x1 > x0 and y1 > y0:
        arr[y0:y1, x0:x1] = fill
    return arr


def _control_box(box, truth_boxes, W, H):
    """An equal-area patch placed where it overlaps the anatomy least, so the control arm removes the same
    number of pixels as the anchor arm and nothing else. Its overlap with every truth box is reported; if the
    best available position still touches a truth box, the arm says so rather than pretending it did not."""
    bw, bh = box[2] - box[0], box[3] - box[1]
    cands = []
    for fx in np.linspace(0.02, 0.98, 25):
        for fy in np.linspace(0.02, 0.98, 25):
            x0 = float(np.clip(fx * W - bw / 2, 0, max(0, W - bw)))
            y0 = float(np.clip(fy * H - bh / 2, 0, max(0, H - bh)))
            cb = [x0, y0, x0 + bw, y0 + bh]
            ov = sum(_overlap_area(cb, t) for t in truth_boxes)
            d = min([abs((cb[1] + cb[3]) / 2 - (t[1] + t[3]) / 2) + abs((cb[0] + cb[2]) / 2 - (t[0] + t[2]) / 2)
                     for t in truth_boxes], default=0.0)
            cands.append((ov, -d, cb))
    cands.sort(key=lambda c: (c[0], c[1]))
    ov, _, cb = cands[0]
    return cb, float(ov / max(1.0, bw * bh))


def _overlap_area(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return ix * iy


def _iou(a, b):
    i = _overlap_area(a, b)
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i
    return i / u if u > 0 else 0.0


def _anchor_found(pred, truth, cls, conf):
    """Whether the detector put a box of the anchor class on the anchor, at IoU >= 0.5.

    Computed here rather than read off or_crossdev_count.frame_eval's `det` block, because that block scores
    classes 0 and 1 only: a bin whose anchor is C2 (class 2) would silently have no entry, and this control
    would then report an anchor that was never scored as an anchor that was never found."""
    T = [t[1] for t in truth if t[0] == cls]
    P = sorted([q for q in pred if q[0] == cls and q[2] >= conf], key=lambda q: -q[2])
    used, tp = set(), 0
    for q in P:
        for j, t in enumerate(T):
            if j not in used and _iou(q[1], t) >= 0.5:
                used.add(j); tp += 1; break
    return {"truth": len(T), "pred": len(P), "tp": tp}


def cmd_anchor(a):
    from PIL import Image
    from ultralytics import YOLO
    from or_crossdev_count import frame_eval
    from or_crossdev_bins import lat_of
    metas = sorted(glob.glob(os.path.join(a.bin, "meta", "*.json")))
    splits = set(a.splits.split(",")) if a.splits else None
    if a.weights == "(selftest stub)":
        _GATE["blk"] = EG.block([], "selftest: a stub detector -- no weights, no patients; not a held-out number")
    else:
        items_ = []
        for mp_ in metas:
            m_ = json.load(open(mp_))
            if splits and m_.get("split") not in splits:
                continue
            items_.append(dict(case=m_.get("case"), stem=Path(mp_).stem,
                               path=os.path.join(a.bin, "images", Path(mp_).stem + ".png")))
        _GATE["blk"] = EG.gate_evaluation(items_, a.weights, "tools/eval_shortcut_controls.py anchor", a,
                                         eval_set=f"{a.bin} splits {a.splits or 'all'}")
    model = YOLO(os.path.expanduser(a.weights))
    per_frame = []
    n_no_anchor = 0
    scratch = Path(os.path.expanduser(a.out)) / "ablated"
    if a.save_images:
        scratch.mkdir(parents=True, exist_ok=True)
    for mi, mp in enumerate(metas):
        m = json.load(open(mp))
        stem = Path(mp).stem
        if splits and m.get("split") not in splits:
            continue
        ip = os.path.join(a.bin, "images", stem + ".png")
        if not os.path.exists(ip):
            continue
        truth = [(b["cls"], b["box"], b.get("level")) for b in m["boxes"] if b.get("kept", True)]
        anchors = [t[1] for t in truth if t[0] == a.anchor_cls]
        if not anchors:
            n_no_anchor += 1
            continue
        im = np.asarray(Image.open(ip).convert("L"))
        H, W = im.shape
        fill = int(np.median(im))
        abox = max(anchors, key=lambda b: (b[2] - b[0]) * (b[3] - b[1]))
        dw, dh = a.dilate * (abox[2] - abox[0]), a.dilate * (abox[3] - abox[1])
        abox_d = [abox[0] - dw, abox[1] - dh, abox[2] + dw, abox[3] + dh]
        cbox, cov = _control_box(abox_d, [t[1] for t in truth], W, H)
        variants = {"intact": im,
                    "anchor_masked": _mask_patch(im.copy(), abox_d, fill),
                    "control_masked": _mask_patch(im.copy(), cbox, fill)}
        rec = {"stem": stem, "case": m.get("case", stem), "split": m.get("split"), "lat": lat_of(m),
               "anchor_box": [round(float(v), 1) for v in abox_d], "control_box": [round(float(v), 1) for v in cbox],
               "control_overlap_frac": round(cov, 4), "n_truth": len(truth),
               "n_truth_named": sum(1 for t in truth if t[0] == 0 and t[2] is not None), "arms": {}}
        for name, arr in variants.items():
            rgb = np.stack([arr] * 3, -1)
            res = model.predict(rgb, imgsz=a.imgsz, conf=0.01, verbose=False)[0]
            pred = [(int(c), [round(float(x), 2) for x in b], round(float(s), 4))
                    for c, b, s in zip(res.boxes.cls.tolist(), res.boxes.xyxy.tolist(), res.boxes.conf.tolist())]
            e = frame_eval(pred, truth, a.op, a.gap)
            e["anchor"] = _anchor_found(pred, truth, a.anchor_cls, a.op)
            if not a.keep_calls:
                e.pop("calls", None)
            rec["arms"][name] = e
            # RENDER THE MASK. Three analytically reasonable fixes have been wrong in this project in ways the
            # numbers did not reveal; one look at the ablated frame says at once whether the patch landed on
            # the sacrum and whether the control patch landed on nothing.
            if a.save_images and name != "intact" and len(per_frame) < a.save_images:
                Image.fromarray(arr).save(scratch / f"{stem}_{name}.png")
        per_frame.append(rec)
        if mi % 25 == 0:
            print(f"  {mi}/{len(metas)} {stem}", flush=True)
    if not per_frame:
        raise SystemExit(f"no frame in {a.bin} carries a class-{a.anchor_cls} truth box "
                         f"({n_no_anchor} frames had none); this control needs the anchor labelled to mask it")

    def collect(name, key):
        d = collections.defaultdict(list)
        for r in per_frame:
            e = r["arms"][name]
            if key == "anchor_found":
                if e["anchor"]["truth"]:
                    d[r["case"]].append(float(bool(e["anchor"]["tp"])))
            elif key == "vertebra_recall":
                if e["det"][0]["truth"]:
                    d[r["case"]] += [1.0] * e["det"][0]["tp"] + [0.0] * (e["det"][0]["truth"] - e["det"][0]["tp"])
            elif key == "coverage":
                if r["n_truth_named"] > 0:
                    d[r["case"]].append(float(bool(e["named"])))
            elif key == "naming_accuracy":
                # or_crossdev_count's published definition: right / (right + wrong) over the calls the frame
                # MADE. Conditional on the frame having named something, and therefore NOT comparable between
                # an intact arm and an arm whose ablation stops most frames naming anything at all.
                if e["right"] + e["wrong"]:
                    d[r["case"]] += [1.0] * e["right"] + [0.0] * e["wrong"]
            elif key == "named_and_right":
                # the same numerator over a denominator that does not move with the ablation: every truth
                # vertebra in the frame that carries an agreed level. A frame that named nothing scores zero
                # here instead of leaving the table.
                if r["n_truth_named"] > 0:
                    k = min(int(e["right"]), int(r["n_truth_named"]))
                    d[r["case"]] += [1.0] * k + [0.0] * (int(r["n_truth_named"]) - k)
        return d

    KEYS = ("anchor_found", "vertebra_recall", "coverage", "naming_accuracy", "named_and_right")
    arms, by = {}, {}
    for name in ("intact", "anchor_masked", "control_masked"):
        by[name] = {k: collect(name, k) for k in KEYS}
        arms[name] = {k: boot_cases(by[name][k], seed=a.seed) for k in KEYS}
        print(f"  {name:<15} " + "  ".join(
            f"{k} {100 * arms[name][k]['point']:.1f}%" if arms[name][k]["point"] is not None else f"{k} -"
            for k in KEYS), flush=True)
    paired = {f"{k}/anchor_masked_minus_intact": boot_paired(by["intact"][k], by["anchor_masked"][k], seed=a.seed)
              for k in KEYS}
    paired.update({f"{k}/control_masked_minus_intact": boot_paired(by["intact"][k], by["control_masked"][k], seed=a.seed)
                   for k in KEYS})
    sf = arms["anchor_masked"]["anchor_found"]["point"]
    na, ni = arms["anchor_masked"]["named_and_right"]["point"], arms["intact"]["named_and_right"]["point"]
    evaluable = sf is not None and na is not None and ni is not None
    met = bool(evaluable and ((sf >= 0.5) or (na >= ni - 0.05)))
    numbers = {"anchor_found_intact": arms["intact"]["anchor_found"]["point"], "anchor_found_anchor_masked": sf,
               "named_and_right_intact": ni, "named_and_right_anchor_masked": na,
               "coverage_intact": arms["intact"]["coverage"]["point"],
               "coverage_anchor_masked": arms["anchor_masked"]["coverage"]["point"],
               "naming_accuracy_intact_CONDITIONAL": arms["intact"]["naming_accuracy"]["point"],
               "naming_accuracy_anchor_masked_CONDITIONAL": arms["anchor_masked"]["naming_accuracy"]["point"],
               "naming_accuracy_items_intact": arms["intact"]["naming_accuracy"]["n"],
               "naming_accuracy_items_anchor_masked": arms["anchor_masked"]["naming_accuracy"]["n"],
               "anchor_found_control_masked": arms["control_masked"]["anchor_found"]["point"]}
    # the framing prior this control exists to separate from the anatomy, quoted from its own file when present
    pp = os.path.expanduser(a.position_prior) if a.position_prior else ""
    prior = None
    if pp and os.path.exists(pp):
        try:
            prior = json.load(open(pp))
        except Exception:  # noqa: BLE001
            prior = None
    v = verdict_for("anchor", met, numbers, evaluable,
                    "no frame in an arm produced a scoreable named vertebra, so there is nothing to compare")
    meta = meta_block("anchor", a, {"bin": a.bin, "weights": a.weights, "position_prior": pp})
    meta["frames"] = {"scored": len(per_frame), "cases": len({r["case"] for r in per_frame}),
                      "skipped_no_anchor_box": n_no_anchor, "operating_point": a.op, "anchor_cls": a.anchor_cls,
                      "dilate": a.dilate, "imgsz": a.imgsz,
                      "control_patch_median_overlap": round(float(np.median([r["control_overlap_frac"] for r in per_frame])), 4)}
    extra = {"paired": paired, "frames": per_frame if a.keep_frames else None}
    # AN EXTERNAL CHECK ON THE INTACT ARM. The intact arm is an ordinary run of this detector at this
    # threshold, so it must reproduce the row tools/or_crossdev_count.py already wrote for the same bin. If it
    # does not, the control's own frame handling moved and the ablation arms cannot be read against the
    # published number -- which is exactly the failure this project keeps meeting.
    if a.reference_json and os.path.exists(os.path.expanduser(a.reference_json)):
        try:
            ref = json.load(open(os.path.expanduser(a.reference_json)))
            row = next((r for r in ref.get("curve", []) if abs(float(r["conf"]) - a.op) < 1e-9), None)
            if row:
                extra["reference"] = {
                    "file": a.reference_json, "conf": a.op,
                    "published": {k: row.get(k) for k in ("sacrum_found_rate", "vertebra_recall", "coverage", "accuracy")},
                    "this_intact_arm": {"anchor_found": arms["intact"]["anchor_found"]["point"],
                                        "vertebra_recall": arms["intact"]["vertebra_recall"]["point"],
                                        "coverage": arms["intact"]["coverage"]["point"],
                                        "naming_accuracy": arms["intact"]["naming_accuracy"]["point"]},
                    "note": "the two are computed over the frames each tool kept; a difference means the frame "
                            "sets differ (splits, kept boxes) or the handling moved, and must be explained "
                            "before the ablation arms are quoted"}
                print(f"  reference {a.reference_json}: published vertebra recall {row.get('vertebra_recall')}, "
                      f"this intact arm {arms['intact']['vertebra_recall']['point']}", flush=True)
        except Exception as e:  # noqa: BLE001
            extra["reference"] = {"file": a.reference_json, "error": f"{type(e).__name__}: {e}"}
    if prior is not None:
        extra["position_prior_reference"] = {"file": pp, "note": "a fixed prior box, no image content: what the "
                                                                 "framing convention alone achieves on this device",
                                             "content": prior if a.keep_frames else "see file"}
    return write_result(a.out, "anchor", meta, arms, v, extra)


# ---------------------------------------------------------------------------------------------------------------
# control: chain -- the sweep's frames in a shuffled order
# ---------------------------------------------------------------------------------------------------------------
def cmd_chain(a):
    import sweep_map as sm
    # Reproduce the published arm's link configuration exactly. sweep_map's module defaults are NOT the defaults
    # its command line uses (END_RULE is "skip" in the module and "clamp" on the command line), and a control
    # that silently ran a different linker would compare two things.
    sm.END_RULE = a.end_rule
    sm.LAST_LINK = a.last_link
    sm.LINK_WINDOW = a.link_window
    sm.NODE_MERGE = a.node_merge
    sm.NODE_ORDER = a.node_order
    sm.SHIFT_MODE, sm.PLACE_MODE = a.shift, a.place
    span_mm = sm.SPAN_PRESETS.get(a.span, None)
    if span_mm is None:
        span_mm = float(a.span)
    film_params = None
    if a.perturb == "film":
        # film_match_augment.load_params, NOT json.load. The fitted file is {"params": {...}, ...} and
        # film_match does `dict(DEFAULT_PARAMS); update(params)`, so handing it the whole file adds a junk
        # `params` key and leaves every real term at its UNFITTED default -- photons 20k-200k instead of the
        # fitted band, scatter 0.15-0.40 instead of the fitted one. Measured on one crop at one seed that is
        # 24.5/255 mean absolute pixel difference. The control would then have run the ordered arm under a
        # different degradation from the published sweep and reported the difference as the linker's.
        from film_match_augment import load_params
        fp = os.path.expanduser(a.film_params)
        film_params = load_params(fp)
        if film_params is None:
            print(f"  note: no fitted film parameters at {fp}; falling back to --perturb photometric. The "
                  f"ordered arm is then NOT the published film arm and meta.sweep.perturb records that.",
                  flush=True)
            a.perturb = "photometric"
    anns = []
    for d in a.drr:
        d = Path(os.path.expanduser(d))
        anns += [(p, d / "img") for p in sorted((d / "ann").glob("*.json"))]
    if a.limit:
        anns = anns[: a.limit]
    print(f"chain control: {len(anns)} candidate spines; span {a.span} = {span_mm:.0f} mm; overlap {a.overlap} "
          f"bodies; truth boxes; link {a.link}", flush=True)

    MODES = ("ordered", "shuffled", "reversed")
    per_spine = {m: [] for m in MODES}
    rows = []
    rng = np.random.RandomState(a.seed)
    for ai, (ann_p, img_dir) in enumerate(anns):
        sp = sm.load_spine(ann_p, img_dir)
        if sp is None:
            continue
        names = [n for n, _ in sp["boxes"]]
        has_sac, has_cr = "sacrum" in names, ("C2" in names or "C1" in names)
        anchor = a.anchor
        if anchor == "auto":
            anchor = "caudal" if has_sac else ("cranial" if has_cr else None)
        if anchor is None or (anchor == "caudal" and not has_sac) or (anchor == "cranial" and not has_cr):
            continue
        pitch_px, px_per_mm = sm.body_pitch_px(sp)
        if not pitch_px or not px_per_mm:
            continue
        sp["_sacrum_part"] = sm.sacrum_part(sp) if has_sac else None
        if anchor == "cranial" and names[0] == "C1":
            sp["boxes"] = sp["boxes"][1:]; names = names[1:]
        span_px = span_mm * px_per_mm
        prior_dy = -(span_px - a.overlap * pitch_px)
        stations = sm.make_stations(sp, span_px, a.overlap, pitch_px, anchor,
                                    np.random.RandomState(a.seed + ai), a.perturb, film_params,
                                    step_jitter=a.step_jitter)
        if len(stations) < 2:
            continue
        for st in stations:
            st["gt"] = list(st["gt_idx"])
            n = len(st["boxes"])
            # THE COUNT NEVER READS THESE. The linker records an embedding cosine as a diagnostic and
            # _finish_chain averages per-node posteriors; neither enters count_names, so they are stubbed and
            # this control needs no encoder. Any arm of this tool that did read them would be meaningless here
            # and is not computed.
            st["emb"] = np.zeros((n, 8), np.float32)
            st["p_single"] = np.zeros((n, len(sm.LEVEL_ORDER)), np.float32)
            st["p_blend"] = np.zeros((n, len(sm.LEVEL_ORDER)), np.float32)
        if any(len(st["boxes"]) == 0 for st in stations):
            continue
        sac_i = names.index("sacrum") if has_sac else None
        row = {"case": sp["case"], "stations": len(stations), "n_bodies": len(names), "anchor": anchor}
        for mode in MODES:
            if mode == "ordered":
                perm = list(range(len(stations)))
            elif mode == "reversed":
                perm = list(range(len(stations)))[::-1]
            else:
                perm = list(rng.permutation(len(stations)))
                # a permutation that happens to be the identity is not a shuffle; redraw once
                if perm == list(range(len(stations))) and len(stations) > 2:
                    perm = list(rng.permutation(len(stations)))
            S = [stations[i] for i in perm]
            chain, links = sm.build_chain(S, pitch_px, prior_dy, mode=a.link, solve=a.link_solve)
            n_nodes = len(chain)
            gts = [n["gt"] for n in chain]
            dup = len(gts) - len(set(str(g) for g in gts))
            covered = {g for g in gts if isinstance(g, int)}
            expected = set()
            for st in S:
                expected.update(st["gt_idx"])
            missed = len([g for g in expected if g not in covered])
            conflict = sum(1 for n in chain if isinstance(n["gt"], tuple))
            # sweep_map's OWN false-positive rule, not a stricter one. A run of unresolved nodes at the end of
            # the chain away from the anchor is the chain reaching past the labelled stack, which that tool
            # calls `unlabelled` and does not count as a false positive. Counting them here would make this
            # control's `chain_complete` a different quantity from the published one under the same name.
            none_idx = [i for i, n in enumerate(chain) if n["gt"] is None]
            unl = []
            if anchor == "caudal":
                for i in range(n_nodes):
                    if chain[i]["gt"] is None:
                        unl.append(i)
                    else:
                        break
            elif anchor == "cranial":
                for i in range(n_nodes - 1, -1, -1):
                    if chain[i]["gt"] is None:
                        unl.append(i)
                    else:
                        break
            fp = len(none_idx) - len(unl)
            if anchor == "caudal":
                anchor_present = chain[-1]["gt"] == sac_i
            elif anchor == "cranial":
                anchor_present = chain[0]["gt"] == 0 and names[0] == "C2"
            else:
                anchor_present = False
            gt_names = [names[n["gt"]] if isinstance(n["gt"], int) else None for n in chain]
            c_names = sm.count_names(n_nodes, anchor, anchor_present)
            c, t = sm._acc(c_names, gt_names)
            complete = (dup == 0 and missed == 0 and fp == 0 and conflict == 0)
            # THE DENOMINATOR THAT DOES NOT MOVE WITH THE ABLATION. sweep_map's _acc scores the chain NODES
            # that resolved to a truth body, and a scrambled chain resolves far fewer of them -- so `t` is
            # itself an outcome of the ablation and the three arms are not on one scale. `n_bodies_imaged` is
            # the number of distinct truth bodies the STATIONS covered, which depends only on how the sweep was
            # cut and is identical in all three arms of this spine.
            n_imaged = len(expected)
            per_spine[mode].append((c, t, complete, bool(anchor_present), n_imaged))
            row[mode] = {"nodes": n_nodes, "duplicates": dup, "missed": missed, "false_positive": fp,
                         "conflict": conflict, "complete": bool(complete), "anchor_present": bool(anchor_present),
                         "count_right": c, "count_total": t, "bodies_imaged": n_imaged, "order": perm}
        rows.append(row)
        if ai % 20 == 0:
            print(f"  {ai}/{len(anns)} {sp['case']}: " +
                  " ".join(f"{m} {row[m]['count_right']}/{row[m]['count_total']}" for m in MODES), flush=True)
        if a.limit_spines and len(rows) >= a.limit_spines:
            break
    if not rows:
        raise SystemExit("no spine in the given --drr directories produced a two-station sweep with an anchor; "
                         "this control needs a render bank with level annotations")

    arms = {}
    for mode in MODES:
        ps = per_spine[mode]
        acc, ci = sm.cluster_boot([(c, t) for c, t, _, _, _ in ps], n_boot=N_BOOT, seed=a.seed)
        acc_b, ci_b = sm.cluster_boot([(c, nb) for c, _, _, _, nb in ps], n_boot=N_BOOT, seed=a.seed)
        arms[mode] = {"spines": len(ps),
                      "count_over_bodies": round(acc_b, 4) if acc_b is not None else None,
                      "ci95": [round(v, 4) for v in ci_b] if ci_b and ci_b[0] is not None else [None, None],
                      "bodies_imaged": int(sum(nb for _, _, _, _, nb in ps)),
                      "count_exact": round(acc, 4) if acc is not None else None,
                      "count_exact_ci95": [round(v, 4) for v in ci] if ci and ci[0] is not None else [None, None],
                      "count_exact_note": "sweep_map's convention: right over the chain nodes that resolved to "
                                          "a truth body. Its DENOMINATOR moves with the ablation, so compare "
                                          "arms on count_over_bodies and read this one only against the "
                                          "published ordered arm.",
                      "chain_complete": round(float(np.mean([p[2] for p in ps])), 4),
                      "anchor_at_end_of_chain": round(float(np.mean([p[3] for p in ps])), 4),
                      "vertebrae_scored": int(sum(t for _, t, _, _, _ in ps))}
        print(f"  {mode:<9} over bodies {100 * (arms[mode]['count_over_bodies'] or 0):6.2f}%  "
              f"(sweep_map count {100 * (arms[mode]['count_exact'] or 0):6.2f}% over "
              f"{arms[mode]['vertebrae_scored']} of {arms[mode]['bodies_imaged']} imaged)  complete "
              f"{100 * arms[mode]['chain_complete']:5.1f}%  anchor at end "
              f"{100 * arms[mode]['anchor_at_end_of_chain']:5.1f}%", flush=True)
    o, s = arms["ordered"]["count_over_bodies"], arms["shuffled"]["count_over_bodies"]
    evaluable = o is not None and s is not None
    met = bool(evaluable and s >= o - 0.05)
    v = verdict_for("chain", met,
                    {"ordered_over_bodies": o, "shuffled_over_bodies": s,
                     "reversed_over_bodies": arms["reversed"]["count_over_bodies"],
                     "ordered_count_exact_SHIFTING_DENOMINATOR": arms["ordered"]["count_exact"],
                     "shuffled_count_exact_SHIFTING_DENOMINATOR": arms["shuffled"]["count_exact"],
                     "ordered_vertebrae_scored": arms["ordered"]["vertebrae_scored"],
                     "shuffled_vertebrae_scored": arms["shuffled"]["vertebrae_scored"],
                     "bodies_imaged": arms["ordered"]["bodies_imaged"],
                     "ordered_chain_complete": arms["ordered"]["chain_complete"],
                     "shuffled_chain_complete": arms["shuffled"]["chain_complete"]},
                    evaluable, "no spine produced a scoreable chain in one of the arms")
    meta = meta_block("chain", a, {"drr": ",".join(a.drr), "film_params": a.film_params,
                                   "sweep_map": str(REPO / "tools" / "sweep_map.py")})
    meta["sweep"] = {"span": a.span, "span_mm": span_mm, "overlap": a.overlap, "step_jitter": a.step_jitter,
                     "anchor": a.anchor, "boxes": "gt", "perturb": a.perturb,
                     "film_params_in_force": {k: list(v) if isinstance(v, (list, tuple)) else v
                                              for k, v in (film_params or {}).items()},
                     "link": a.link,
                     "link_solve": a.link_solve, "end_rule": a.end_rule, "last_link": a.last_link,
                     "spines": len(rows)}
    return write_result(a.out, "chain", meta, arms, v, {"spines": rows if a.keep_frames else None})


# ---------------------------------------------------------------------------------------------------------------
# control: duplicate detection (delegated)
# ---------------------------------------------------------------------------------------------------------------
def cmd_dupes(a):
    """Runs tools/or_audit_dupes.py -- it is already written, already tuned (NCC32 with an NCC64 re-score) and
    already draws the contact sheets, so it is called rather than reimplemented -- then reads its dupes.json for
    the single question this list asks: is any test frame a near-duplicate of a TRAINING frame from a different
    case?"""
    out = os.path.expanduser(a.out)
    os.makedirs(out, exist_ok=True)
    dj = os.path.join(a.audit_dir or out, "dupes.json")
    if a.run:
        cmd = [sys.executable, str(REPO / "tools" / "or_audit_dupes.py"), "--out", a.audit_dir or out,
               "--workers", str(a.workers), "--thr", str(a.thr)]
        print("  " + " ".join(cmd), flush=True)
        rc = subprocess.call(cmd)
        if rc != 0:
            raise SystemExit(f"or_audit_dupes.py exited {rc}")
    if not os.path.exists(dj):
        raise SystemExit(f"{dj} not present. Run this control with --run (it needs the realxray frames and the "
                         f"film corpora on the grid), or point --audit-dir at an existing audit directory.")
    D = json.load(open(dj))
    arms, worst = {}, []
    for ds, blk in (D.get("within") or {}).items():
        comp = (blk.get("comparisons") or {}).get("train+val|test") or {}
        cross = comp.get("n_cross_case", 0)
        n_raw = blk.get("n")
        arms[ds] = {"n": (sum(v for v in n_raw.values() if isinstance(v, int)) if isinstance(n_raw, dict)
                          else n_raw),
                    "n_per_split": n_raw if isinstance(n_raw, dict) else None,
                    "threshold": blk.get("threshold"),
                    "cross_case_pairs_train_val_vs_test": cross,
                    "same_case_pairs": comp.get("n_same_case"),
                    "cross_case_ncc64_ge_thr": comp.get("n_ncc64_ge_thr"),
                    "max_ncc32_nearest_test_frame": comp.get("max_ncc32"),
                    "top_cross_case": (comp.get("top_cross_case") or [])[:5]}
        if cross:
            worst.append((ds, cross))
        print(f"  {ds:<14} cross-case train/val vs test pairs >= {blk.get('threshold')}: {cross}", flush=True)
    # THE OTHER DIRECTION, WHICH IS EASY TO FORGET. The within-dataset block asks whether a test frame of one
    # device repeats a training frame of the same device. The across block asks whether it repeats a frame of
    # the film or FluoroCap corpora, which are training data for the detectors those frames are scored with --
    # a duplicate there is the same leak wearing a different name.
    across = {}
    for corp, blk in (D.get("across") or {}).get("corpora", {}).items():
        near = blk.get("nearest_by_dataset") or {}
        across[corp] = {"n": blk.get("n"), "n_pairs": blk.get("n_pairs"),
                        "n_ncc64_ge_thr": blk.get("n_ncc64_ge_thr"),
                        "max_nearest_per_dataset": {k: v.get("max") for k, v in near.items()},
                        "n_ge_thr_per_dataset": {k: v.get("n_ge_thr") for k, v in near.items()}}
        n_over = sum(v.get("n_ge_thr") or 0 for v in near.values())
        if n_over:
            worst.append((f"external/{corp}", n_over))
        print(f"  external {corp:<22} frames {blk.get('n')}  pairs >= thr {blk.get('n_pairs')}  "
              f"frames of ours at/over thr {n_over}", flush=True)
    if across:
        arms["_external_corpora"] = across
    met = any(c for _, c in worst)
    v = verdict_for("dupes", met, {"datasets_with_cross_case_pairs": dict(worst),
                                   "threshold": D.get("threshold")})
    meta = meta_block("dupes", a, {"dupes_json": dj, "or_audit_dupes": str(REPO / "tools" / "or_audit_dupes.py")})
    return write_result(a.out, "dupes", meta, arms, v)


# ---------------------------------------------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------------------------------------------
def _pct(v):
    return "-" if v is None else f"{100 * v:.1f}%"


def _ci(d):
    if not d or d.get("ci95") in (None, [None, None]):
        return ""
    return f" [{100 * d['ci95'][0]:.1f}, {100 * d['ci95'][1]:.1f}]"


def cmd_report(a):
    out = os.path.expanduser(a.out)
    found = {}
    for c in ("permute", "anatomy", "scale", "order", "anchor", "chain", "dupes"):
        p = os.path.join(out, f"{c}.json")
        if os.path.exists(p):
            found[c] = json.load(open(p))
    if not found:
        raise SystemExit(f"no control JSON in {out}; run the controls first")
    lines = ["# Negative controls and shortcut tests", "",
             f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `tools/eval_shortcut_controls.py report` from the "
             f"JSONs in `{out}`. Every expectation and falsifier below was written into the tool before the "
             f"result was read; the verdict is computed from the numbers in the same file.", "",
             "| control | verdict | numbers | falsifier |", "|---|---|---|---|"]
    for c, d in found.items():
        v = d["verdict"]
        nums = ", ".join(f"{k} {(_pct(x) if isinstance(x, float) and 0 <= x <= 1 else x)}"
                         for k, x in (v.get("numbers_used") or {}).items())
        vd = ("**FALSIFIER MET**" if v["falsifier_met"] else
              ("**NOT EVALUABLE**" if not v.get("evaluable", True) else "not falsified"))
        lines.append(f"| {c} | {vd} | {nums} | {v['criterion']} |")
    lines += ["", "## What each control removed, and what it found", ""]
    for c, d in found.items():
        v = d["verdict"]
        lines += [f"### {c}", "", f"*Expectation, stated before the run:* {v['expectation']}", "",
                  f"*What would falsify the project's claim:* {v['falsifies']}", "",
                  f"*What this control cannot say:* {v.get('limitation', '-')}", "",
                  f"*Decision rule:* `{v['criterion']}` -> "
                  f"**{'MET' if v['falsifier_met'] else ('NOT EVALUABLE -- ' + v.get('not_evaluable_because', '') if not v.get('evaluable', True) else 'not met')}**", ""]
        if v.get("criterion_note"):
            lines += [f"*Why the rule reads that quantity and not the obvious one:* {v['criterion_note']}", ""]
        if c == "anatomy":
            has_probe = any("probe" in row for row in d["arms"].values() if isinstance(row, dict))
            lines.append("| arm | exact (encoder's own head) | 95 % CI | " +
                         ("exact (linear probe fitted per arm) | 95 % CI | " if has_probe else "") + "items | cases |")
            lines.append("|---|---|---|" + ("---|---|" if has_probe else "") + "---|---|")
            for arm, row in d["arms"].items():
                z = row.get("zero_shot")
                if not z:
                    continue
                cells = [arm, _pct(z["point"]), _ci(z).strip() or "-"]
                if has_probe:
                    p = row.get("probe") or {}
                    cells += [_pct(p.get("point")), _ci(p).strip() or "-"]
                cells += [str(z.get("n", "-")), str(z.get("cases", "-"))]
                lines.append("| " + " | ".join(cells) + " |")
        elif c in ("permute", "order", "scale"):
            lines.append("| arm | exact | 95 % CI | items | cases |")
            lines.append("|---|---|---|---|---|")
            for arm, row in d["arms"].items():
                r = row if isinstance(row, dict) else {}
                if "point" not in r:
                    continue
                lines.append(f"| {arm} | {_pct(r.get('point'))} | "
                             f"{_ci(r).strip() or '-'} | {r.get('n', '-')} | {r.get('cases', '-')} |")
        elif c == "anchor":
            keys = [k for k in ("anchor_found", "vertebra_recall", "coverage", "named_and_right",
                                "naming_accuracy") if k in next(iter(d["arms"].values()))]
            lines.append("| arm | " + " | ".join(k.replace("_", " ") for k in keys) + " | items behind the "
                         "naming column |")
            lines.append("|---|" + "---|" * (len(keys) + 1))
            for arm, row in d["arms"].items():
                lines.append(f"| {arm} | " + " | ".join(_pct(row[k]["point"]) + _ci(row[k]) for k in keys)
                             + f" | {row['naming_accuracy']['n']} over {row['naming_accuracy']['cases']} cases |")
            lines += ["", "`named_and_right` is right over EVERY scoreable truth vertebra in the frame and so "
                      "has the same denominator in all three arms. `naming_accuracy` is the published "
                      "right/(right+wrong) over the calls a frame MADE: a frame that lost its anchor names "
                      "nothing and leaves that column entirely, which is why its item count moves with the "
                      "ablation and why the decision rule does not read it.", ""]
        elif c == "chain":
            lines.append("| frame order | bodies named right | 95 % CI | sweep_map count exact | its items | "
                         "chain complete | anchor at end | spines |")
            lines.append("|---|---|---|---|---|---|---|---|")
            for arm, row in d["arms"].items():
                lines.append(f"| {arm} | {_pct(row.get('count_over_bodies'))} | {_ci(row).strip() or '-'} | "
                             f"{_pct(row['count_exact'])} | {row.get('vertebrae_scored')} of "
                             f"{row.get('bodies_imaged')} | "
                             f"{_pct(row['chain_complete'])} | {_pct(row['anchor_at_end_of_chain'])} | "
                             f"{row['spines']} |")
            lines += ["", "The `sweep_map count exact` column is that tool's own convention -- right over the "
                      "chain nodes that resolved to a truth body -- and its denominator SHRINKS as the chain "
                      "dissolves, which is why the two shuffled columns disagree. Compare the arms on the "
                      "first column, whose denominator is the bodies the stations imaged and is the same in "
                      "all three.", ""]
        elif c == "dupes":
            lines.append("| dataset | frames | cross-case train/val vs test pairs | max NCC32 of a test frame |")
            lines.append("|---|---|---|---|")
            for ds, row in d["arms"].items():
                if ds.startswith("_"):
                    continue
                nn = row.get("n")
                nn = sum(v for v in nn.values() if isinstance(v, int)) if isinstance(nn, dict) else nn
                lines.append(f"| {ds} | {nn} | {row.get('cross_case_pairs_train_val_vs_test')} | "
                             f"{row.get('max_ncc32_nearest_test_frame')} |")
            ext = d["arms"].get("_external_corpora") or {}
            if ext:
                lines += ["", "Against corpora these frames are scored with a detector trained on:", "",
                          "| external corpus | its frames | pairs over threshold | our frames at/over threshold |",
                          "|---|---|---|---|"]
                for corp, row in ext.items():
                    n_over = sum(v or 0 for v in (row.get("n_ge_thr_per_dataset") or {}).values())
                    lines.append(f"| {corp} | {row.get('n')} | {row.get('n_pairs')} | {n_over} |")
        lines.append("")
        lines.append(f"Source: `{out}/{c}.json` (code {d['meta'].get('code_sha')}, seed {d['meta'].get('seed')}).")
        lines.append("")
    mdp = os.path.join(out, "CONTROLS.md")
    open(mdp, "w").write("\n".join(lines) + "\n")
    print("wrote", mdp)
    if not a.no_figure:
        _figure(found, out)
    return 0


def _figure(found, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from _figfit import fit
    INK, INK2, GRID = "#18222c", "#4a5866", "#d7dee7"
    OK, BAD, REF = "#2f6fb0", "#b04a3a", "#8d93a0"
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                         "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID,
                         "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
                         "legend.frameon": False})
    # panels: the controls that produce a bar of arms, in the order the argument runs
    panels = []
    for c in ("permute", "anatomy", "order", "scale", "anchor", "chain"):
        if c not in found:
            continue
        d = found[c]
        if c == "anchor":
            # `named_and_right`, not `naming_accuracy`: the latter's denominator is the calls a frame made, so
            # an arm that stops most frames naming anything at all is scored on the frames it did not break.
            # Drawing that would show three equal bars under an ablation that wiped out every call.
            kk = "named_and_right" if "named_and_right" in next(iter(d["arms"].values())) else "naming_accuracy"
            arms = [(k, d["arms"][k][kk]["point"], d["arms"][k][kk]["ci95"], d["arms"][k][kk].get("n"))
                    for k in d["arms"]]
            ttl = "anchor masked in the pixels"
            xl = "truth vertebrae named right" if kk == "named_and_right" else "naming accuracy"
        elif c == "chain":
            kk = "count_over_bodies" if "count_over_bodies" in next(iter(d["arms"].values())) else "count_exact"
            arms = [(k, d["arms"][k][kk], d["arms"][k]["ci95"], d["arms"][k].get("bodies_imaged")) for k in d["arms"]]
            ttl = "sweep frames re-ordered"
            xl = "bodies named right" if kk == "count_over_bodies" else "count exact"
        else:
            # the anatomy control is read with the same arm its verdict used (the per-arm linear probe when one
            # was fitted), so the picture and the decision cannot disagree
            want = (d["verdict"].get("numbers_used") or {}).get("scored_with", "zero_shot")
            arms = []
            for k, row in d["arms"].items():
                r = row.get(want, row.get("zero_shot", row)) if isinstance(row, dict) else row
                if isinstance(r, dict) and "point" in r:
                    arms.append((k if c != "scale" else f"{k}x", r["point"], r.get("ci95", [None, None]),
                                 r.get("n")))
            ttl = {"permute": "labels permuted (head retrained)",
                   "anatomy": f"crop content removed ({want.replace('_', ' ')})",
                   "order": "run order broken", "scale": "crops rescaled"}[c]
            xl = "exact level"
        panels.append((c, ttl, xl, arms, found[c]["verdict"]["falsifier_met"]))
    if not panels:
        print("no plottable control; figure skipped")
        return
    # ONE ROW OF SIX DOES NOT FIT. At 13 in a six-panel row leaves each panel about 2.1 in, and the y labels
    # ("reference majority class") plus the value annotation take all of it: tight_layout then collapses the
    # data area to a sliver and every axis reads "0 50 100" on top of itself. Three to a row, wrapped.
    NC = 3 if len(panels) > 4 else len(panels)
    NR = int(np.ceil(len(panels) / NC))
    W = 13.0
    H = NR * (1.35 + 0.34 * max(len(p[3]) for p in panels)) + 0.6
    fig, axes = plt.subplots(NR, NC, figsize=(W, H), squeeze=False)
    flat = [ax for row in axes for ax in row]
    for ax in flat[len(panels):]:
        ax.axis("off")
    for ax, (c, ttl, xl, arms, met) in zip(flat, panels):
        # AN ARM WITH NO NUMBER IS DRAWN, NOT DROPPED. An ablation that removes every scoreable item produces
        # a null, and silently omitting its bar turns the most informative outcome the control has into a
        # picture of two untouched arms.
        ys = np.arange(len(arms))[::-1]
        for yy, (k, v, ci, n) in zip(ys, arms):
            if v is None:
                ax.text(0.02, yy, "no scoreable item left by this arm", va="center", fontsize=11.5, color=BAD,
                        style="italic")
                continue
            col = REF if k.startswith("reference") else (OK if k in ("true", "intact", "ordered", "1x", "single_crop") else BAD)
            ax.barh(yy, v, height=0.62, color=col, alpha=0.85)
            right = v
            if ci and ci[0] is not None:
                ax.plot([ci[0], ci[1]], [yy, yy], color=INK, lw=1.2)
                right = max(right, ci[1])
            ax.text(min(right + 0.03, 1.12), yy, f"{100 * v:.1f}%", va="center", fontsize=12.5, color=INK)
            if n:
                ax.text(min(right + 0.03, 1.12), yy - 0.34, f"n={n}", va="center", fontsize=9.5, color=INK2)
        ax.set_yticks(ys)
        ax.set_yticklabels([k.replace("_", " ") for k, _, _, _ in arms], fontsize=12.5)
        ax.set_xlim(0, 1.45)      # room for the value AND its item count, so unequal denominators are visible
        ax.set_xticks([0, 0.5, 1.0])
        ax.set_xticklabels(["0", "50", "100"])
        ax.set_xlabel(xl + " (%)", fontsize=12.5)
        fit(fig, ax.set_title(ttl + ("\nFALSIFIER MET" if met else ""), fontsize=13.5,
                              color=(BAD if met else INK), pad=8), W / NC - 0.7)
        ax.tick_params(labelsize=12)
    fit(fig, fig.suptitle("Negative controls: each arm removes the part the method says is doing the work "
                          "(bars are point estimates, lines are case-clustered 95 % intervals)",
                          fontsize=14.5, color=INK), W - 0.5)
    fig.tight_layout(rect=(0.005, 0, 0.995, 1.0 - 0.55 / H))
    for ext in ("png", "pdf"):
        p = os.path.join(out, f"fig_shortcut_controls.{ext}")
        fig.savefig(p, dpi=170)
        print("wrote", p)


# ---------------------------------------------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------------------------------------------
def _stub_encoder(n_classes, dev, d=32):
    """A tiny untrained encoder used ONLY by the selftest, so the machinery can be exercised on a machine with
    no corpus, no GPU and no torchvision. It says nothing about the real models; anything it scores is noise."""
    import torch
    import torch.nn as nn

    class Enc(nn.Module):
        def __init__(self):
            super().__init__()
            self.body = nn.Sequential(nn.Conv2d(2, 8, 5, 4, 2), nn.ReLU(), nn.Conv2d(8, 16, 5, 4, 2), nn.ReLU(),
                                      nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Linear(16, d))
            self.fc = nn.Linear(d, n_classes)

        def forward(self, x):
            return self.fc(self.body(x))
    torch.manual_seed(0)
    m = Enc().to(dev)
    fc = m.fc
    m.fc = nn.Identity()
    m.eval()
    return m, fc, {"arch": "selftest stub (untrained)", "loss": "none"}


def _synth_bank(dirpath, n_films=14, size=64, seed=0):
    """A synthetic crop bank with the real bank's contract: X (N,2,S,S) uint8, channel 1 the target's box.

    The 'anatomy' is deliberately planted INSIDE the target box (a bar whose length encodes the class) and a
    different, uninformative texture outside it, so the selftest can check that the body-only and context-only
    ablations really do remove what they say they remove. It is not a model of a vertebra."""
    from make_context_crops import LEVEL_ORDER
    rng = np.random.RandomState(seed)
    dirpath = Path(dirpath)
    dirpath.mkdir(parents=True, exist_ok=True)
    X, y, case, split, source = [], [], [], [], []
    for f in range(n_films):
        n = int(rng.randint(5, 9))
        start = int(rng.randint(0, len(LEVEL_ORDER) - n))
        for j in range(n):
            cls = start + j
            img = (rng.rand(size, size) * 60).astype(np.float32)          # context: noise, no class information
            mk = np.zeros((size, size), np.float32)
            y0, y1 = size // 2 - 8, size // 2 + 8
            x0, x1 = size // 2 - 8, size // 2 + 8
            mk[y0:y1, x0:x1] = 1.0
            bar = 1 + (cls % 14)                                          # the class, drawn inside the body box
            img[y0 + 2:y0 + 2 + max(1, bar), x0 + 2:x1 - 2] = 230
            X.append(np.stack([img, mk * 255]).astype(np.uint8))
            y.append(cls)
            case.append(f"synth_{f:03d}")
            split.append("val" if f % 4 == 0 else "train")
            source.append("synthetic")
    X = np.stack(X)
    np.savez_compressed(dirpath / "rung_1.npz", X=X, y=np.array(y, np.int64), case=np.array(case),
                        split=np.array(split), source=np.array(source))
    json.dump({"classes": LEVEL_ORDER, "size": size, "tgt_px": 16, "mode": "fov"}, open(dirpath / "meta.json", "w"))
    return str(dirpath)


def _synth_drr(dirpath, n_spines=3, seed=0):
    """A synthetic render bank with the contract tools/sweep_map.py reads: ann/<case>.json carrying `levels`
    (name + box) and the row/column spacing, img/<case>.npy carrying the long image.

    Each body is a bright block with its OWN speckle, so consecutive frames can be locked to each other by
    correlation the way the real linker does. It is a test of the plumbing, not a spine."""
    dirpath = Path(dirpath)
    (dirpath / "ann").mkdir(parents=True, exist_ok=True)
    (dirpath / "img").mkdir(parents=True, exist_ok=True)
    NAMES = ["T9", "T10", "T11", "T12", "L1", "L2", "L3", "L4", "L5", "sacrum"]
    cases = []
    for s in range(n_spines):
        rng = np.random.RandomState(seed + s)
        pitch, W = 100, 360
        H = pitch * (len(NAMES) + 2)
        img = (rng.rand(H, W) * 40 + 20).astype(np.float32)
        levels = {}
        for i, nm in enumerate(NAMES):
            cy = int(pitch * (1.5 + i))
            h = 70 if nm != "sacrum" else 150
            y0, y1 = cy - h // 2, cy + h // 2
            x0, x1 = W // 2 - 55, W // 2 + 55
            img[y0:y1, x0:x1] = 120 + rng.rand(y1 - y0, x1 - x0) * 120   # its own speckle: a lockable target
            levels[nm] = {"name": nm, "box": [x0, y0, x1, y1]}
        np.save(dirpath / "img" / f"synth{s:02d}.npy", np.clip(img, 0, 255).astype(np.uint8))
        json.dump({"case": f"synth{s:02d}", "levels": levels,
                   "mm_per_px_row_si_col_ap": [0.34, 0.34], "source": "selftest"},
                  open(dirpath / "ann" / f"synth{s:02d}.json", "w"))
        cases.append(f"synth{s:02d}")
    return str(dirpath), cases


def _synth_anchor_bin(dirpath, n_frames=24, W=400, H=700, seed=0):
    """A synthetic image+meta bin with the contract tools/or_crossdev_bins.py writes: images/<stem>.png and
    meta/<stem>.json carrying case, split and kept boxes (cls 0 vertebra with a level, cls 1 sacrum).

    Each body and the sacrum are drawn as their own bright speckle, so a detector stub can tell an intact
    structure from a flat painted block by its variance alone. It is not a radiograph."""
    d = Path(dirpath)
    (d / "images").mkdir(parents=True, exist_ok=True)
    (d / "meta").mkdir(parents=True, exist_ok=True)
    rng = np.random.RandomState(seed)
    LEVELS = ["L5", "L4", "L3", "L2", "L1"]
    for f in range(n_frames):
        im = (rng.rand(H, W) * 30 + 40).astype(np.uint8)
        boxes = []
        sac = [150, 560, 250, 660]
        im[sac[1]:sac[3], sac[0]:sac[2]] = (rng.rand(sac[3] - sac[1], sac[2] - sac[0]) * 120 + 110).astype(np.uint8)
        boxes.append({"cls": 1, "box": sac, "level": None, "kept": True})
        for i, lv in enumerate(LEVELS):
            y0 = 500 - 90 * i
            b = [160, y0, 240, y0 + 70]
            im[b[1]:b[3], b[0]:b[2]] = (rng.rand(b[3] - b[1], b[2] - b[0]) * 120 + 110).astype(np.uint8)
            boxes.append({"cls": 0, "box": b, "level": lv, "kept": True})
        from PIL import Image
        Image.fromarray(im).save(d / "images" / f"fr{f:03d}.png")
        json.dump({"case": f"case{f // 3:02d}", "split": "test", "boxes": boxes, "lat": True},
                  open(d / "meta" / f"fr{f:03d}.json", "w"))
    return str(d)


class _StubYOLO:
    """A detector whose behaviour is known exactly, so the anchor control's ARITHMETIC can be checked without
    a GPU, weights or a real bin. Every vertebra is always found; the sacrum is found when its pixels still
    carry variance, and on a fixed share of frames regardless -- which is the framing-convention shortcut
    or_ready/robust/position_prior.json measured at 85.7 % on a real device."""
    _truth, _n, _share = {}, 0, 0.0

    @classmethod
    def reset(cls, bin_dir, prior_share=0.0):
        cls._truth = {i: json.load(open(p))["boxes"]
                      for i, p in enumerate(sorted(glob.glob(os.path.join(bin_dir, "meta", "*.json"))))}
        cls._n, cls._share = 0, float(prior_share)

    def __init__(self, path):
        self.path = path

    def predict(self, arr, imgsz=1024, conf=0.01, verbose=False):
        g = arr[:, :, 0] if getattr(arr, "ndim", 2) == 3 else arr
        idx = _StubYOLO._n // 3          # three variants per frame, in the order cmd_anchor calls them
        _StubYOLO._n += 1
        tb = _StubYOLO._truth[idx]
        rows = [(0, b["box"], 0.9) for b in tb if b["cls"] == 0]
        sac = [b["box"] for b in tb if b["cls"] == 1][0]
        patch = g[sac[1]:sac[3], sac[0]:sac[2]]
        if float(np.std(patch)) > 5.0 or (idx % 20) < round(_StubYOLO._share * 20):
            rows.append((1, sac, 0.9))

        class _B:
            def __init__(s, r):
                s.cls = type("T", (), {"tolist": staticmethod(lambda r=r: [q[0] for q in r])})()
                s.xyxy = type("T", (), {"tolist": staticmethod(lambda r=r: [[float(v) for v in q[1]] for q in r])})()
                s.conf = type("T", (), {"tolist": staticmethod(lambda r=r: [q[2] for q in r])})()
        return [type("R", (), {"boxes": _B(rows)})()]


def cmd_selftest(a):
    import torch
    out = os.path.expanduser(a.out)
    os.makedirs(out, exist_ok=True)
    ctx = _synth_bank(os.path.join(out, "synth_bank"), seed=a.seed)
    dev = "cpu"
    B = load_bank(ctx, "1")
    n_classes = len(B["classes"])
    stub = _stub_encoder(n_classes, dev)
    checks = []

    # 1. the ablations change the pixels they claim to, and nothing else
    xb = torch.from_numpy(B["X"][:8]).float().div_(255.0)
    m = (xb[:, 1:2] > 0.5).float()
    b, c, k = tf_body_only(xb), tf_context_only(xb), tf_marker_only(xb)
    checks.append(("body_only zeroes the surround", bool(((b[:, 0:1] * (1 - m)).abs().max() == 0))))
    checks.append(("body_only keeps the body", bool(torch.allclose(b[:, 0:1] * m, xb[:, 0:1] * m))))
    checks.append(("context_only zeroes the body", bool(((c[:, 0:1] * m).abs().max() == 0))))
    checks.append(("context_only keeps the surround", bool(torch.allclose(c[:, 0:1] * (1 - m), xb[:, 0:1] * (1 - m)))))
    checks.append(("marker_only zeroes the image channel", bool(k[:, 0].abs().max() == 0)))
    checks.append(("every ablation leaves the marker channel intact",
                   all(bool(torch.allclose(t[:, 1], xb[:, 1])) for t in (b, c, k))))
    z = make_zoom(1.2)(xb)
    checks.append(("zoom changes the pixels and keeps the canvas", z.shape == xb.shape and not torch.allclose(z, xb)))
    checks.append(("zoom 1.0 is the identity", bool(torch.allclose(make_zoom(1.0)(xb), xb))))

    # 2. the bank-based controls run end to end and write a complete result
    class NS:  # a namespace shaped like argparse's, with the stub encoder attached
        pass
    for name, fn, kw in (("anatomy", cmd_anatomy, dict(probe=True, probe_epochs=60)),
                         ("scale", cmd_scale, dict(zooms=[0.8, 0.9, 1.0, 1.1, 1.2])),
                         ("permute", cmd_permute, dict(epochs=3, k=2, bs_head=64, lr=1e-3, save_head=False,
                                                       reference_json=None)),
                         ("order", cmd_order, dict(epochs=3, k=2, bs_head=64, lr=1e-3, head=None))):
        ns = NS()
        ns.__dict__.update(dict(ctx=ctx, rung="1", model="(selftest stub)", out=out, seed=a.seed, bs=64,
                                device=dev, probe=False, probe_epochs=60, zooms=[1.0], epochs=3, k=2,
                                bs_head=64, lr=1e-3, save_head=False, reference_json=None, head=None))
        ns.__dict__.update(kw)
        ns._stub = stub
        print(f"\n[selftest] {name}")
        fn(ns)
        d = json.load(open(os.path.join(out, f"{name}.json")))
        checks.append((f"{name}: result carries meta/arms/verdict",
                       all(kk in d for kk in ("meta", "arms", "verdict"))))
        checks.append((f"{name}: verdict states expectation, falsifier and criterion",
                       all(kk in d["verdict"] for kk in ("expectation", "falsifies", "criterion", "falsifier_met"))))
        checks.append((f"{name}: meta records seed and code sha",
                       "seed" in d["meta"] and "code_sha" in d["meta"]))

    # 2b. the ablation SEMANTICS, not just its arithmetic. The synthetic bank plants the class signal inside
    #     the target's own box and puts pure noise outside it, so a correct body/context ablation must rank
    #     body_only above context_only once each arm gets its own read-out. If this check fails the two
    #     channels have been crossed somewhere and every anatomy number would be the wrong way round.
    da = json.load(open(os.path.join(out, "anatomy.json")))
    checks.append(("anatomy: on a bank whose signal is inside the body box, the probe ranks body_only above "
                   "context_only", da["arms"]["body_only"]["probe"]["point"] > da["arms"]["context_only"]["probe"]["point"]))
    ds = json.load(open(os.path.join(out, "scale.json")))
    checks.append(("scale: every requested zoom is scored on the same items",
                   len(ds["arms"]) == 5 and len({r["n"] for r in ds["arms"].values()}) == 1))

    # 3. the falsifier logic fires when it should. The stub encoder is untrained, so its permutation arms are
    #    all noise and the permute control SHOULD report the falsifier met -- that is the check: the rule is
    #    live, not decorative.
    dp = json.load(open(os.path.join(out, "permute.json")))
    checks.append(("permute falsifier fires on an untrained encoder (all arms at chance)",
                   dp["verdict"]["falsifier_met"] is True))
    checks.append(("scale: the rule is marked NOT EVALUABLE when the arms it names were not run",
                   json.load(open(os.path.join(out, "scale.json")))["verdict"]["evaluable"] is True))
    checks.append(("per-source intervals are not called ci95 unless they are the clustered ones",
                   all("ci95_wilson_item_level" in r for r in
                       da["arms"]["intact"]["zero_shot_per_source"].values())))

    # 3a-bis. A CASE ON BOTH SIDES OF THE SPLIT MUST RAISE, not train the head on its own held-out crops.
    bad_ctx = _synth_bank(os.path.join(out, "synth_bank_mixed_split"), seed=a.seed + 7)
    zz = dict(np.load(Path(bad_ctx) / "rung_1.npz", allow_pickle=True))
    sp_ = np.array([str(v) for v in zz["split"]])
    first = str(zz["case"][0])
    where = np.nonzero(np.array([str(c) for c in zz["case"]]) == first)[0]
    sp_[where[0]] = "train" if sp_[where[0]] == "val" else "val"      # one crop moved across
    zz["split"] = sp_
    np.savez_compressed(Path(bad_ctx) / "rung_1.npz", **zz)
    Bb = load_bank(bad_ctx, "1")
    try:
        _films(Bb["y"], Bb["case"], Bb["split"], "train")
        straddle_raises = False
    except SystemExit:
        straddle_raises = True
    checks.append(("a case straddling the split raises instead of leaking into the run head's windows",
                   straddle_raises))

    # 3b. the anchor control's two geometry helpers, which decide what the ablation actually removes
    truth = [[100, 100, 160, 180], [100, 200, 160, 280], [100, 300, 160, 400]]
    cb, cov = _control_box([100, 300, 160, 400], truth, 640, 640)
    checks.append(("anchor: the control patch is the same size as the anchor box",
                   abs((cb[2] - cb[0]) - 60) < 1e-6 and abs((cb[3] - cb[1]) - 100) < 1e-6))
    checks.append(("anchor: the control patch avoids the anatomy", cov == 0.0))
    arr = np.full((40, 40), 200, np.uint8)
    _mask_patch(arr, [10, 10, 20, 30], 7)
    checks.append(("anchor: the mask fills exactly the box it is given",
                   arr[10:30, 10:20].max() == 7 and arr[0:10, :].min() == 200 and int((arr == 7).sum()) == 200))

    # 3c. the chain control end to end on a synthetic sweep: it must run, score all three orders on the same
    #     spines, and actually present the linker a different order in the shuffled arm.
    drr, _ = _synth_drr(os.path.join(out, "synth_drr"), seed=a.seed)
    ns = NS()
    ns.__dict__.update(dict(out=out, seed=a.seed, drr=[drr], span="ii9", overlap=2.0, step_jitter=0.0,
                            anchor="caudal", perturb="photometric", film_params="", link="robust",
                            link_solve="pairwise", shift="ncc", place="template", end_rule="clamp",
                            last_link="protocol", link_window=1.0, node_merge=0.0, node_order="prepend",
                            limit=0, limit_spines=0, keep_frames=True))
    print("\n[selftest] chain")
    cmd_chain(ns)
    dc = json.load(open(os.path.join(out, "chain.json")))
    checks.append(("chain: three frame orders scored on the same spines",
                   len({dc["arms"][m]["spines"] for m in ("ordered", "shuffled", "reversed")}) == 1
                   and dc["arms"]["ordered"]["spines"] > 0))
    checks.append(("chain: the shuffled arm really re-orders the frames",
                   any(sp["shuffled"]["order"] != sp["ordered"]["order"] for sp in (dc.get("spines") or []))))
    checks.append(("chain: the reversed arm is the ordered arm end to end",
                   all(sp["reversed"]["order"] == sp["ordered"]["order"][::-1] for sp in (dc.get("spines") or []))))
    checks.append(("chain: the three arms share one denominator (the bodies the stations imaged)",
                   len({dc["arms"][m]["bodies_imaged"] for m in ("ordered", "shuffled", "reversed")}) == 1))
    checks.append(("chain: the shifting-denominator metric is kept and is NOT the one the rule reads",
                   "count_exact" in dc["arms"]["ordered"]
                   and "shuffled_over_bodies" in dc["verdict"]["numbers_used"]))
    # the film model must be read the way sweep_map reads it, or the sweep runs under unfitted defaults
    from film_match_augment import DEFAULT_PARAMS, load_params
    fpj = Path(out) / "film_params_probe.json"
    json.dump({"fitted_on": "selftest", "params": {"photons": [150000, 250000], "scatter": [0.02, 0.05]}},
              open(fpj, "w"))
    _lp = load_params(str(fpj)) or {}
    _raw = json.load(open(fpj))
    checks.append(("chain: film parameters are read through load_params, so the FITTED terms are in force",
                   set(_lp) == {"photons", "scatter"} and "params" not in _lp
                   and dict(DEFAULT_PARAMS, **_lp)["photons"] != dict(DEFAULT_PARAMS, **_raw)["photons"]))

    # 3d. THE ANCHOR CONTROL'S SELECTION EFFECT, on a bin and a detector whose behaviour is known exactly.
    #     The anchor is destroyed on every frame and a framing prior recovers it on a fixed share; the
    #     published conditional accuracy must stay put on the survivors while the arm-invariant one falls.
    ab = _synth_anchor_bin(os.path.join(out, "synth_bin"))
    ns = NS()
    ns.__dict__.update(dict(out=out, seed=a.seed, bin=ab, weights="(selftest stub)", splits="test",
                            anchor_cls=1, dilate=0.15, op=0.25, gap=1.8, imgsz=1024, position_prior="",
                            reference_json=None, keep_frames=False, keep_calls=False, save_images=0))
    print("\n[selftest] anchor (synthetic bin, stub detector)")
    import types as _types
    _saved = sys.modules.get("ultralytics")
    sys.modules["ultralytics"] = _types.SimpleNamespace(YOLO=_StubYOLO)
    try:
        _StubYOLO.reset(ab, prior_share=0.5)
        cmd_anchor(ns)
    finally:
        if _saved is None:
            sys.modules.pop("ultralytics", None)
        else:
            sys.modules["ultralytics"] = _saved
    dan = json.load(open(os.path.join(out, "anchor.json")))
    A = dan["arms"]
    checks.append(("anchor: the stub's masked arm really loses the anchor on the frames it should",
                   A["anchor_masked"]["anchor_found"]["point"] < A["intact"]["anchor_found"]["point"]))
    checks.append(("anchor: the CONDITIONAL naming accuracy is scored on fewer items once the anchor is gone",
                   A["anchor_masked"]["naming_accuracy"]["n"] < A["intact"]["naming_accuracy"]["n"]))
    checks.append(("anchor: named_and_right keeps one denominator across the arms",
                   A["anchor_masked"]["named_and_right"]["n"] == A["intact"]["named_and_right"]["n"]))
    checks.append(("anchor: the arm-invariant metric falls where the conditional one does not",
                   A["anchor_masked"]["named_and_right"]["point"] < A["intact"]["named_and_right"]["point"]
                   and A["anchor_masked"]["naming_accuracy"]["point"] >= A["intact"]["naming_accuracy"]["point"] - 1e-9))
    checks.append(("anchor: the control patch changes nothing",
                   A["control_masked"]["named_and_right"]["point"] == A["intact"]["named_and_right"]["point"]))

    # 4. the report renders
    ns = NS(); ns.out = out; ns.no_figure = False
    cmd_report(ns)
    checks.append(("report writes CONTROLS.md", os.path.exists(os.path.join(out, "CONTROLS.md"))))
    checks.append(("report writes the figure", os.path.exists(os.path.join(out, "fig_shortcut_controls.png"))
                   and os.path.exists(os.path.join(out, "fig_shortcut_controls.pdf"))))

    print("\n" + "=" * 92)
    bad = 0
    for name, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
        bad += int(not ok)
    json.dump({"checks": [{"check": n, "pass": bool(o)} for n, o in checks], "failed": bad,
               "note": "the selftest exercises the machinery on a synthetic bank and an untrained stub encoder. "
                       "It says nothing about the real models; it checks that each ablation removes what it "
                       "claims to, that every control writes a complete result, and that the falsifier rules "
                       "are live.", "meta": meta_block("selftest", a, {"synthetic_bank": ctx})},
              open(os.path.join(out, "selftest.json"), "w"), indent=1, default=_json_default)
    print(f"\n{len(checks) - bad}/{len(checks)} checks passed; wrote {os.path.join(out, 'selftest.json')}")
    return 1 if bad else 0


# ---------------------------------------------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, bank=True):
        p.add_argument("--out", required=True, help="directory for <control>.json")
        EG.add_args(p)
        p.add_argument("--seed", type=int, default=0)
        if bank:
            p.add_argument("--ctx", required=True, help="crop bank directory (meta.json + rung_<k>.npz)")
            p.add_argument("--rung", default="1")
            p.add_argument("--model", required=True, help="level-model encoder .pt (its sidecar names the arch)")
            p.add_argument("--bs", type=int, default=256)
            p.add_argument("--device", default=None)

    p = sub.add_parser("anatomy", help="body-only / context-only / marker-only crop ablation")
    common(p)
    p.add_argument("--probe", action="store_true", default=True,
                   help="also fit a fresh linear read-out per arm on the training split (default on): without "
                        "it a drop could be the encoder meeting an out-of-distribution crop rather than lost "
                        "information")
    p.add_argument("--no-probe", dest="probe", action="store_false")
    p.add_argument("--probe-epochs", type=int, default=300)

    p = sub.add_parser("scale", help="crops rescaled about their centre")
    common(p)
    p.add_argument("--zooms", type=float, nargs="+", default=[0.8, 0.9, 1.0, 1.1, 1.2])

    p = sub.add_parser("permute", help="retrain the run head on permuted level labels")
    common(p)
    p.add_argument("--k", type=int, default=3, help="neighbours either side at scoring time (band 2k+1)")
    p.add_argument("--train-kmax", type=int, default=4,
                   help="the head is trained on window lengths 2..2*train_kmax+1. head_mixed_length's --kmax "
                        "default is 4, and the published rows come from that; tying this to --k instead would "
                        "train on a narrower distribution than the reference and the difference would be read "
                        "as drift in this control")
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--bs-head", type=int, default=256)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--save-head", action="store_true")
    p.add_argument("--reference-json", default=None,
                   help="a published mixed_*.json from tools/head_mixed_length.py on the SAME bank: the true-label "
                        "arm is reported beside it, so a control whose own training drifted is visible")

    p = sub.add_parser("order", help="run-order shuffle for the run head")
    common(p)
    p.add_argument("--head", default=None, help="a trained RunLabeller .pt; otherwise one is trained here")
    p.add_argument("--k", type=int, default=3)
    p.add_argument("--train-kmax", type=int, default=4, help="window lengths 2..2*train_kmax+1 when a head is "
                                                             "trained here; ignored when --head is given")
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--bs-head", type=int, default=256)
    p.add_argument("--lr", type=float, default=1e-3)

    p = sub.add_parser("anchor", help="mask the anchor in the pixels and re-run the detector and the count")
    common(p, bank=False)
    p.add_argument("--bin", required=True, help="an image+meta directory (tools/or_crossdev_bins.py) or a realxray dataset")
    p.add_argument("--weights", required=True, help="YOLO box detector (cls 0 vertebra, cls 1 sacrum)")
    p.add_argument("--splits", default="test", help="comma list, or empty for every split")
    p.add_argument("--anchor-cls", type=int, default=1, help="1 = sacrum; 2 = C2 where the bin labels one")
    p.add_argument("--dilate", type=float, default=0.15, help="grow the anchor box by this fraction before masking")
    p.add_argument("--op", type=float, default=0.25, help="confidence at which the count is scored")
    p.add_argument("--gap", type=float, default=1.8, help="name_levels gap rule, as or_crossdev_count uses it")
    p.add_argument("--imgsz", type=int, default=1024)
    p.add_argument("--position-prior", default="/rs/rs_grp_oschome/go2432/data/or_ready/robust/position_prior.json",
                   help="quoted beside the result: what a fixed prior box alone achieves on this device")
    p.add_argument("--reference-json", default=None,
                   help="a score.json from tools/or_crossdev_count.py on the SAME bin and detector: the intact "
                        "arm is reported beside its published row, so a control whose frame handling drifted "
                        "is visible before the ablation arms are read")
    p.add_argument("--keep-frames", action="store_true", help="write the per-frame rows into the JSON")
    p.add_argument("--keep-calls", action="store_true")
    p.add_argument("--save-images", type=int, default=0, help="write this many ablated frames for the eye")

    p = sub.add_parser("chain", help="hand the linker the sweep's frames out of order")
    common(p, bank=False)
    p.add_argument("--drr", action="append", required=True, help="render bank (ann/ + img/); repeatable")
    p.add_argument("--span", default="ii9")
    p.add_argument("--overlap", type=float, default=2.0)
    p.add_argument("--step-jitter", type=float, default=0.0)
    p.add_argument("--anchor", choices=["auto", "caudal", "cranial"], default="caudal")
    p.add_argument("--perturb", choices=["none", "photometric", "film"], default="film")
    p.add_argument("--film-params", default="~/model_night/film_match/film_match_params.json")
    p.add_argument("--link", choices=["strict", "robust"], default="robust")
    p.add_argument("--link-solve", choices=["pairwise", "global"], default="pairwise")
    p.add_argument("--shift", choices=["ncc", "phase"], default="ncc")
    p.add_argument("--place", choices=["template", "ecc"], default="template")
    p.add_argument("--end-rule", choices=["clamp", "skip"], default="clamp")
    p.add_argument("--last-link", choices=["protocol", "open"], default="protocol")
    p.add_argument("--link-window", type=float, default=1.0)
    p.add_argument("--node-merge", type=float, default=0.0)
    p.add_argument("--node-order", choices=["prepend", "position"], default="prepend")
    p.add_argument("--limit", type=int, default=0, help="candidate annotations to read")
    p.add_argument("--limit-spines", type=int, default=0, help="stop after this many usable spines")
    p.add_argument("--keep-frames", action="store_true")

    p = sub.add_parser("dupes", help="near-duplicate audit (delegates to tools/or_audit_dupes.py)")
    common(p, bank=False)
    p.add_argument("--run", action="store_true", help="run or_audit_dupes.py rather than reading an existing dupes.json")
    p.add_argument("--audit-dir", default=None)
    p.add_argument("--workers", type=int, default=16)
    p.add_argument("--thr", type=float, default=0.97)

    p = sub.add_parser("report", help="aggregate every control JSON into a table and a figure")
    p.add_argument("--out", required=True)
    p.add_argument("--no-figure", action="store_true")
    p.add_argument("--seed", type=int, default=0, help="accepted and unused, so one runner can pass it to every "
                                                       "subcommand")

    p = sub.add_parser("selftest", help="synthetic end-to-end exercise of the machinery")
    p.add_argument("--out", required=True)
    p.add_argument("--seed", type=int, default=0)

    a = ap.parse_args()
    fn = {"anatomy": cmd_anatomy, "scale": cmd_scale, "permute": cmd_permute, "order": cmd_order,
          "anchor": cmd_anchor, "chain": cmd_chain, "dupes": cmd_dupes, "report": cmd_report,
          "selftest": cmd_selftest}[a.cmd]
    r = fn(a)
    return r if isinstance(r, int) else 0


if __name__ == "__main__":
    raise SystemExit(main())
