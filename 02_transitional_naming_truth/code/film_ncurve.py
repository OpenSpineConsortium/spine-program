#!/usr/bin/env python
# Copied 2026-10-08 into spine-program/02_transitional_naming_truth/code/ from the private repository
# spinesurg-ct-nnunet (https://github.com/Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet, branch L6_Class,
# commit 097933a). Path in the repository: tools/film_ncurve.py. Tracked, unmodified at 097933a.
# This copy is a record for a reader with only this folder; edit and run the repository copy, on the
# grid inside an sbatch job, never on the login node.
"""The FILM N-curve: naming accuracy on plain films against the number of training PERSONS, per film corpus
(NHANES II, BUU-LSPINE, CSXA), with the SAME encoder / head recipe and a superset of the N grid of the C-ArmLSpine
naming curve (tools/indomain_name_fill.py), so the two curves can be pooled and fitted together
(SchwingNet/results/coverage/N_VS_COVERAGE_PLAN.md: accuracy ~ f(N) against accuracy ~ f(N) + g(H*)).

WHY A NEW ENCODER. The C-ArmLSpine curve fine-tunes the v9 encoder, which had never seen a C-arm frame, on N C-arm
cases merged 1:1 with a per-class-600 base sample of its own bank. The v9 encoder HAS seen every film person of its
train split (the bank was built from ~/films_drr), so a film curve on top of it would start from an encoder that already
knows every training film; N would not mean N. The analogue of "an encoder that never saw the target domain" is an
encoder trained on the v9 bank's RENDER rows only (physics_drr, physics_rare, ctsp_drr, verse_drr: TotalSegmentator,
CTSpinoPelvic1K and VerSe renders; no film row), from ImageNet with the v9 recipe (40 epochs, lr 3e-4, --augment 2).
Every film cell then fine-tunes THAT encoder on N film persons merged 1:1 with the render bank's per-class-600 sample,
15 epochs at lr 1e-4, --augment 2, then head_mixed_length --train-mode mixed: the C-ArmLSpine recipe verbatim.
The Figure 6 G3-clean encoder is not usable for the same reason as v9: its bank holds the film roots.

PERSONS AND SPLITS (per corpus S, keyed by tools/rigor_fixes.patient_key: one CSXA film = one person; one four-digit
BUU case = one person; NHANES by film number, which names the person across its cervical and lumbar films).
  TEST       the v9 VAL persons of S: never trained on, never selected on, by any cell or by the render encoder. These
             are the films the manuscript's per-source film numbers are scored on (a5), so the curve's end point is
             comparable with them.
  SELECTION  a fixed seeded draw of min(100, ceil(0.15 x pool)) persons from the v9 TRAIN persons of S: the val split
             of every cell of S (checkpoint selection for the encoder epoch and the head), identical across N and seeds.
  POOL       the remaining v9 TRAIN persons of S; per seed a shuffled order; N takes the first N (nested subsets).
  N          0, 5, 10, 25, 50, 100, 200, all; seeds 0-2 for N <= 25, seed 0 above (the C-arm ladder is 0..50, all).
  N = 0      the render base sample only, selection on S's selection crops: the film-free floor of each curve.
  scoring    tools/rigor_fixes.py a5-rows on ONE test context holding the v9 val films of all three corpora
             (random-length windows of 2..9 vertebrae and the maximal bands, as the manuscript's film numbers), so every
             cell also gives the two other corpora as cross-corpus points. Patient-clustered bootstrap intervals in
             `collect`. tools/eval_gate.py runs inside a5-rows on the encoder + head chain before anything is scored.

Subcommands (grid):
  prep       render bank, test context, per-corpus film pools, persons, cells.json, manifest.txt   (CPU, ~150 GB)
  cellbank   the `real` npz of one cell (read by tools/merge_banks.py --real)
  collect    every cell's a5 rows -> film_ncurve.json + FILM_NCURVE.md
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime
import glob
import json
import math
import os
import random
import re
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))

GRID = "/rs/rs_grp_oschome/go2432/data"
FN = f"{GRID}/or_ready/film_ncurve"
V9 = os.path.expanduser("~/allspine_v9_fov96_ctx")
# tools/train_level_classifier.py --film-sources default: sources that are real films, never rendered CTs
FILM_SOURCES = ("csxa", "buu_full", "nhanes", "nhanes_drr", "vindr", "aasce")
RENDER_SOURCES = ("physics_drr", "physics_rare", "ctsp_drr", "verse_drr")
SOURCES = ("nhanes", "buu_full", "csxa")
N_LADDER = [0, 5, 10, 25, 50, 100, 200, "all"]
SEEDS = {0: [0, 1, 2], 5: [0, 1, 2], 10: [0, 1, 2], 25: [0, 1, 2], 50: [0], 100: [0], 200: [0], "all": [0]}
SEL_FRAC, SEL_CAP = 0.15, 100
PROTOCOLS = ("random", "maximal_band3", "maximal_band5", "maximal_band7", "maximal_band9")


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def str_arr(z, k):
    return np.array([str(v) for v in z[k]])


def patient_key(case):
    """The gate's own person key (tools/patient_keys.key_any: csxa by the full film id, buu by the four-digit case,
    nhanes by the film number that names the person across its cervical and lumbar films); the rigor_fixes key when
    key_any does not recognise the name (it then raises in prep, because an unkeyed film is nobody's)."""
    try:
        import patient_keys as PK
        r, _why = PK.key_any(case)
        if r and r.get("key"):
            return str(r["key"])
    except Exception:  # noqa: BLE001
        pass
    from rigor_fixes import patient_key as pk
    return pk(case)


def cell_name(src, N, seed):
    return f"{src}_N{N}_s{seed}"


# ---------------------------------------------------------------------------------------------------------- prep
def cmd_prep(a):
    os.makedirs(FN, exist_ok=True)
    meta = json.load(open(os.path.join(V9, "meta.json")))
    classes = list(meta["classes"])
    z = np.load(os.path.join(V9, "rung_1.npz"), allow_pickle=True)
    y = np.asarray(z["y"]); case = str_arr(z, "case"); split = str_arr(z, "split"); src = str_arr(z, "source")
    scale = np.asarray(z["scale"])
    seen = sorted(set(src))
    unknown = [s for s in seen if s not in FILM_SOURCES and s not in RENDER_SOURCES]
    if unknown:
        raise SystemExit(f"v9 sources not classified as film or render: {unknown}; extend FILM_SOURCES / RENDER_SOURCES")
    is_film = np.isin(src, FILM_SOURCES)
    check = dict(generated=now(), v9=os.path.join(V9, "rung_1.npz"), n=int(len(y)), sources=dict(collections.Counter(src)),
                 splits=dict(collections.Counter(split)), classes=classes)
    print(f"v9: {len(y)} crops; sources {check['sources']}", flush=True)
    print("loading X ...", flush=True)
    X = z["X"]
    check["x_shape"] = list(X.shape[1:]); check["x_dtype"] = str(X.dtype)

    def write_bank(dirname, idx, split_override=None, extra=None, note=""):
        d = os.path.join(FN, dirname); os.makedirs(d, exist_ok=True)
        idx = np.asarray(sorted(idx))
        sp = split[idx] if split_override is None else np.array([split_override] * len(idx))
        payload = dict(X=X[idx], y=y[idx], case=case[idx], split=sp, source=src[idx], scale=scale[idx])
        if extra:
            payload.update(extra)
        tmp = os.path.join(d, "rung_1.tmp.npz")
        np.savez(tmp, **payload); os.replace(tmp, os.path.join(d, "rung_1.npz"))
        m = dict(meta); m["film_ncurve"] = dict(built=now(), note=note, rows=int(len(idx)),
                                                 splits=dict(collections.Counter(sp.tolist())),
                                                 sources=dict(collections.Counter(src[idx].tolist())))
        json.dump(m, open(os.path.join(d, "meta.json"), "w"), indent=1)
        print(f"  {dirname}: {len(idx)} rows {m['film_ncurve']['splits']}", flush=True)
        return m["film_ncurve"]

    # 1. the render-only bank (the encoder's training data; train/val as v9 split them)
    if not os.path.exists(os.path.join(FN, "render_bank", "rung_1.npz")):
        check["render_bank"] = write_bank("render_bank", np.where(~is_film)[0],
                                          note="v9 rows whose source is a rendered CT (no film row): the film-free encoder's bank")
    else:
        check["render_bank"] = json.load(open(os.path.join(FN, "render_bank", "meta.json")))["film_ncurve"]; print("  render_bank exists", flush=True)
    # 2. the test context: every v9 VAL film row of the three corpora, split "val" (what a5-rows scores)
    test_mask = is_film & (split == "val") & np.isin(src, SOURCES)
    if not os.path.exists(os.path.join(FN, "test_ctx", "rung_1.npz")):
        check["test_ctx"] = write_bank("test_ctx", np.where(test_mask)[0], split_override="val",
                                       note="the v9 val films of nhanes / buu_full / csxa: the fixed TEST persons of every cell")
    else:
        check["test_ctx"] = json.load(open(os.path.join(FN, "test_ctx", "meta.json")))["film_ncurve"]; print("  test_ctx exists", flush=True)
    test_persons = {s: sorted({patient_key(c) for c in case[test_mask & (src == s)]}) for s in SOURCES}
    # 3. per-corpus film pools (v9 TRAIN rows) with their v9 index
    pools = {}
    for s in SOURCES:
        m = is_film & (split == "train") & (src == s)
        idx = np.where(m)[0]
        if not os.path.exists(os.path.join(FN, f"pool_{s}", "rung_1.npz")):
            write_bank(f"pool_{s}", idx, split_override="train", extra=dict(v9_index=np.asarray(sorted(idx))),
                       note=f"the v9 train films of {s}: selection + training persons are drawn from here")
        pools[s] = idx
    del X
    # 4. persons, selection, orders, cells
    cells = collections.OrderedDict(); persons_rep = {}
    for si, s in enumerate(SOURCES):
        idx = pools[s]
        by_p = collections.defaultdict(list)
        for r in idx:
            by_p[patient_key(case[r])].append(int(r))
        unparsed = [p for p in by_p if p.startswith("case:")]
        if unparsed:
            raise SystemExit(f"{s}: {len(unparsed)} train cases with no person key, e.g. {unparsed[:3]}")
        leak = sorted(set(by_p) & set(test_persons[s]))
        if leak:
            raise SystemExit(f"{s}: {len(leak)} persons on both the v9 train and val side, e.g. {leak[:3]}: the v9 split is not by person")
        persons = sorted(by_p)
        order0 = list(persons); random.Random(4242 + si).shuffle(order0)
        n_sel = min(SEL_CAP, int(math.ceil(SEL_FRAC * len(persons))))
        sel = sorted(order0[:n_sel]); pool = sorted(order0[n_sel:])
        sel_rows = sorted(r for p in sel for r in by_p[p])
        persons_rep[s] = dict(train_persons=len(persons), train_crops=int(len(idx)), selection_persons=len(sel), selection_crops=len(sel_rows),
                              pool_persons=len(pool), test_persons=len(test_persons[s]), test_crops=int((test_mask & (src == s)).sum()),
                              films_per_person=round(len(set(case[idx])) / max(1, len(persons)), 3))
        for N in N_LADDER:
            n_take = len(pool) if N == "all" else int(N)
            if N != "all" and n_take > len(pool):
                continue
            for seed in SEEDS[N]:
                order = list(pool); random.Random(100 * seed + si + 7).shuffle(order)
                ppl = sorted(order[:n_take])
                rows = sorted(r for p in ppl for r in by_p[p])
                c = dict(source=s, N=N, seed=seed, n_persons=len(ppl), persons=ppl, pool_rows=rows, n_train_crops=len(rows),
                         selection_persons=sel, selection_rows=sel_rows, n_selection_crops=len(sel_rows),
                         heldout=dict(train_in_test=sorted(set(ppl) & set(test_persons[s])),
                                      selection_in_test=sorted(set(sel) & set(test_persons[s]))))
                c["heldout"]["verdict"] = "HELD OUT" if not (c["heldout"]["train_in_test"] or c["heldout"]["selection_in_test"]) else "NOT HELD OUT"
                if c["heldout"]["verdict"] != "HELD OUT":
                    raise SystemExit(f"{cell_name(s, N, seed)}: {c['heldout']}")
                cells[cell_name(s, N, seed)] = c
    # nested check: for one seed, the N=5 persons are a subset of N=10 etc.
    for s in SOURCES:
        prev = None
        for N in [n for n in N_LADDER if n != 0]:
            k = cell_name(s, N, 0)
            if k not in cells:
                continue
            cur = set(cells[k]["persons"])
            if prev is not None and not prev <= cur:
                raise SystemExit(f"{s}: subsets are not nested at N={N}")
            prev = cur
    # manifest, in priority order: the ends of every curve (N = all, N = 0 seed 0), the seed-0 ladder, the extra seeds
    pri = [k for k, c in cells.items() if c["N"] == "all"] + [k for k, c in cells.items() if c["N"] == 0 and c["seed"] == 0]
    pri += [k for k, c in cells.items() if c["seed"] == 0 and k not in pri]
    pri += [k for k in cells if k not in pri]
    assert sorted(pri) == sorted(cells)
    with open(os.path.join(FN, "manifest.txt"), "w", newline="\n") as f:
        for k in pri:
            c = cells[k]
            f.write(f"{k} {c['source']} {c['N']} {c['seed']}\n")
    check.update(test_persons={s: len(v) for s, v in test_persons.items()}, per_source=persons_rep, n_cells=len(cells),
                 ladder=N_LADDER, seeds={str(k): v for k, v in SEEDS.items()}, selection=dict(frac=SEL_FRAC, cap=SEL_CAP))
    design = dict(
        encoder="tools/train_level_classifier.py on render_bank from ImageNet (--require-pretrained), 40 epochs, lr 3e-4, --augment 2, "
                "--uint8-resident, seed 0, tag renderonly: the film-free encoder every cell fine-tunes",
        cell="tools/merge_banks.py --base render_bank --real <cellbank> --per-class 600 --real-share 0.5 --seed <seed>; "
             "train_level_classifier --init <renderonly> --epochs 15 --lr 1e-4 --augment 2 --seed <seed>; head_mixed_length --train-mode mixed",
        score="tools/rigor_fixes.py a5-rows --ctx test_ctx (the v9 val films of all three corpora) --kmax 4 --seed 0; "
              "tools/eval_gate.py inside a5-rows on the encoder + head chain",
        persons="tools/rigor_fixes.patient_key; TEST = v9 val persons; SELECTION = fixed 15 % (<= 100) of v9 train persons; POOL = the rest, nested by seed",
        analogue="the C-ArmLSpine naming curve (tools/indomain_name_fill.py): v9 init that never saw a C-arm frame + N C-arm cases merged 1:1 "
                 "with the v9 base sample; here: render-only init that never saw a film + N film persons merged 1:1 with the render base sample")
    json.dump(dict(generated=now(), tool="tools/film_ncurve.py prep", design=design, check=check, test_persons=test_persons, cells=cells),
              open(os.path.join(FN, "cells.json"), "w"), indent=1)
    print(json.dumps(dict(n_cells=len(cells), per_source=persons_rep), indent=1), flush=True)
    return 0


# ------------------------------------------------------------------------------------------------------ cellbank
def cmd_cellbank(a):
    D = json.load(open(os.path.join(FN, "cells.json")))
    c = D["cells"][a.cell]; s = c["source"]
    test = set(D["test_persons"][s])
    if set(c["persons"]) & test or set(c["selection_persons"]) & test:
        raise SystemExit(f"{a.cell}: a test person is in the training or selection set")
    z = np.load(os.path.join(FN, f"pool_{s}", "rung_1.npz"), allow_pickle=True)
    v9i = np.asarray(z["v9_index"]); pos = {int(v): i for i, v in enumerate(v9i)}
    tr = np.array([pos[r] for r in c["pool_rows"]], dtype=int); va = np.array([pos[r] for r in c["selection_rows"]], dtype=int)
    case = str_arr(z, "case")
    for name, rows in (("train", tr), ("selection", va)):
        ppl = {patient_key(x) for x in case[rows]}
        if ppl & test:
            raise SystemExit(f"{a.cell}: {name} rows key to a test person")
    idx = np.concatenate([tr, va]).astype(int)
    split = np.array(["train"] * len(tr) + ["val"] * len(va))
    os.makedirs(a.out, exist_ok=True)
    X = z["X"]
    np.savez(os.path.join(a.out, "rung_1.npz"), X=X[idx], y=np.asarray(z["y"])[idx], case=case[idx], split=split,
             source=str_arr(z, "source")[idx], scale=np.asarray(z["scale"])[idx])
    meta = json.load(open(os.path.join(FN, f"pool_{s}", "meta.json")))
    meta["film_ncurve_cell"] = dict(cell=a.cell, source=s, N=c["N"], seed=c["seed"], n_persons=c["n_persons"], train_crops=int(len(tr)),
                                    selection_persons=len(c["selection_persons"]), selection_crops=int(len(va)), built=now())
    json.dump(meta, open(os.path.join(a.out, "meta.json"), "w"), indent=1)
    json.dump(dict(cell=a.cell, source=s, N=c["N"], seed=c["seed"], persons=c["persons"], train_crops=int(len(tr)), val_crops=int(len(va)),
                   test_persons_in_bank=0, heldout=c["heldout"]), open(os.path.join(a.out, "cellbank.json"), "w"), indent=1)
    print(f"{a.cell}: {len(tr)} train crops from {c['n_persons']} persons, {len(va)} selection crops", flush=True)
    return 0


# ------------------------------------------------------------------------------------------------------- collect
def cluster_boot(rows, n_boot=2000, seed=0):
    """Patient-clustered percentile bootstrap of the exact rate; rows = (patient, exact)."""
    by = collections.defaultdict(lambda: [0, 0])
    for p, e in rows:
        by[p][0] += int(e); by[p][1] += 1
    k = np.array([v[0] for v in by.values()], float); n = np.array([v[1] for v in by.values()], float)
    if n.sum() == 0:
        return None
    point = float(k.sum() / n.sum()); rng = np.random.RandomState(seed); m = len(k)
    vals = []
    for _ in range(n_boot):
        i = rng.randint(0, m, m); vals.append(k[i].sum() / max(1.0, n[i].sum()))
    return dict(point=round(point, 4), lo=round(float(np.percentile(vals, 2.5)), 4), hi=round(float(np.percentile(vals, 97.5)), 4),
                k=int(k.sum()), n=int(n.sum()), patients=int(m), films=None)


ARMS = {
    "renderonly": "the reported curve: render-only encoder as init, render base + N film persons (real share 0.5), 15 epochs",
    "imagenet": "ablation: ImageNet init (no render pretraining), the SAME merged bank (render base + N film persons), 15 epochs",
    "filmonly": "ablation: ImageNet init, the merged bank with every render row removed (the N persons' crops at the same "
                "oversampled count, the selection crops as val), 15 epochs; no N = 0 cell (nothing to train on)",
}


def cmd_collect(a):
    D = json.load(open(os.path.join(FN, "cells.json")))
    root = a.root or FN
    arm = a.arm or "renderonly"
    enc = glob.glob(os.path.join(FN, "render_bank", "runs", "result_rung_1_renderonly*.json")) if arm == "renderonly" else []
    encoder = json.load(open(enc[0])) if enc else None
    out = dict(generated=now(), tool="tools/film_ncurve.py collect", arm=arm, arm_design=ARMS.get(arm), root=root,
               design=D["design"], check=D["check"],
               encoder=dict(result=enc[0] if enc else None, val_exact=(encoder or {}).get("exact"), n_train=(encoder or {}).get("n_train"),
                            n_val=(encoder or {}).get("n_val"), init=(encoder or {}).get("init"), pretrained=(encoder or {}).get("pretrained")),
               cells={}, curves={})
    n_done = 0
    for k, c in D["cells"].items():
        W = os.path.join(root, "cells", k)
        st = dict(source=c["source"], N=c["N"], seed=c["seed"], n_persons=c["n_persons"], n_train_crops=c["n_train_crops"],
                  state="missing", heldout=c["heldout"]["verdict"])
        mp = os.path.join(W, "score", "a5_rows_meta.json"); rp = os.path.join(W, "score", "a5_rows.csv")
        if os.path.exists(os.path.join(W, "DONE")) and os.path.exists(mp) and os.path.exists(rp):
            m = json.load(open(mp))
            st["state"] = "scored"; n_done += 1
            st["eval_gate"] = dict(held_out=(m.get("eval_gate") or {}).get("held_out"), reason=(m.get("eval_gate") or {}).get("not_held_out_reason"),
                                   gate_version=(m.get("eval_gate") or {}).get("gate_version"))
            st["per_source_exact"] = m.get("per_source_reproduced")
            rows = list(csv.DictReader(open(rp)))
            st["clustered"] = {}
            for proto in PROTOCOLS:
                st["clustered"][proto] = {}
                for s in SOURCES:
                    R = [(r["patient"], int(r["exact"])) for r in rows if r["protocol"] == proto and r["source"] == s]
                    b = cluster_boot(R, n_boot=a.boot, seed=0)
                    if b:
                        b["films"] = len({r["film"] for r in rows if r["protocol"] == proto and r["source"] == s})
                    st["clustered"][proto][s] = b
            rj = glob.glob(os.path.join(W, "bank", "runs", "result_rung_1_ft_*.json"))
            if rj:
                r = json.load(open(rj[0])); st["encoder_ft"] = dict(val_exact=r.get("exact"), n_train=r.get("n_train"), n_val=r.get("n_val"), init=r.get("init"))
        elif os.path.exists(W):
            st["state"] = "started"
        out["cells"][k] = st
    # curves: per corpus, own-source accuracy vs N (random protocol), every seed; plus the cross-corpus points
    for s in SOURCES:
        cur = collections.OrderedDict()
        for N in N_LADDER:
            pts = []
            for seed in SEEDS[N]:
                k = cell_name(s, N, seed); st = out["cells"].get(k)
                if not st or st["state"] != "scored":
                    continue
                own = st["clustered"]["random"][s]
                pts.append(dict(seed=seed, n_persons=st["n_persons"], n_train_crops=st["n_train_crops"], acc=own["point"], lo=own["lo"], hi=own["hi"],
                                cross={t: st["clustered"]["random"][t]["point"] for t in SOURCES if t != s and st["clustered"]["random"][t]}))
            if pts:
                cur[str(N)] = dict(points=pts, mean_acc=round(float(np.mean([p["acc"] for p in pts])), 4),
                                   n_persons=pts[0]["n_persons"])
        out["curves"][s] = cur
    out["n_cells"] = len(D["cells"]); out["n_cells_scored"] = n_done
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    md = [f"# Film N-curve, arm {arm} (generated {out['generated']}; {n_done} of {len(D['cells'])} cells scored)", "",
          f"Arm: {ARMS.get(arm)}.", "",
          "Naming accuracy on the fixed v9 VAL films of each corpus against N training PERSONS of that corpus (tools/film_ncurve.py "
          "docstring). Random-length windows (2..9 vertebrae), exact level, patient-clustered percentile intervals. Nothing here is "
          "interpreted; the fit is tools/indomain_fit_coverage.py.", ""]
    for s in SOURCES:
        md += [f"## {s}", "", "| N persons | seeds | crops | accuracy (seed mean) | per seed [95 % CI] | cross-corpus (seed 0) |", "|---:|---:|---:|---:|---|---|"]
        for N, v in out["curves"][s].items():
            per = "; ".join(f"s{p['seed']} {100 * p['acc']:.1f} [{100 * p['lo']:.1f}, {100 * p['hi']:.1f}]" for p in v["points"])
            cross = ", ".join(f"{t} {100 * x:.1f}" for t, x in v["points"][0]["cross"].items())
            md += [f"| {N} ({v['n_persons']}) | {len(v['points'])} | {v['points'][0]['n_train_crops']} | {100 * v['mean_acc']:.1f} | {per} | {cross} |"]
        md += [""]
    missing = [k for k, st in out["cells"].items() if st["state"] != "scored"]
    md += [f"Encoder (render only): val exact {out['encoder']['val_exact']}, n_train {out['encoder']['n_train']}, init {out['encoder']['init']}", "",
           f"Cells not scored: {len(missing)}" + (f" -- {missing[:20]}" if missing else ""), ""]
    open(os.path.join(os.path.dirname(os.path.abspath(a.out)), "FILM_NCURVE.md"), "w", newline="\n").write("\n".join(md) + "\n")
    print(f"wrote {a.out}: {n_done}/{len(D['cells'])} scored", flush=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("prep")
    c = sub.add_parser("cellbank"); c.add_argument("--cell", required=True); c.add_argument("--out", required=True)
    o = sub.add_parser("collect"); o.add_argument("--out", default=f"{FN}/film_ncurve.json"); o.add_argument("--boot", type=int, default=2000)
    o.add_argument("--root", default=None, help="cells root of an ablation arm ($FN/ablation/<arm>); default the reported curve's $FN")
    o.add_argument("--arm", default=None, choices=list(ARMS), help="which arm the cells under --root are (recorded; default renderonly)")
    a = ap.parse_args()
    return {"prep": cmd_prep, "cellbank": cmd_cellbank, "collect": cmd_collect}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
