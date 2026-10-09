#!/usr/bin/env python
"""Why allspine_v8 holds persons in BOTH its train and its val split, read from the bank itself.

The gate (tools/eval_gate.py) keys every bank case with today's rules (tools/patient_keys.key_any: an implant render
is its SOURCE CT, a VerSe series is its SUBJECT) and finds 192 persons of the v8 validation split in its training
split: 187 CTSpinoPelvic1K and 5 VerSe (EVAL_LEAKS.md L4). The bank build (tools/make_context_crops.py
--patient-json ~/patient_keys.json) printed "people on both sides: 0". Both can be true only if the two keyings
disagree. This script shows which cases, under which build-time key, make each of the 192, and what the overlap
touches:

  1. per overlapping person: its val cases and its train cases, each with the key the BUILD used
     (~/patient_keys.json, 2026-09-22 16:18, tools/patient_keys.py at c27b53f) and the key the GATE uses now;
  2. the cause per person, from the build keys alone (an implant render filed as a person called implant:<case>_v<k>;
     two VerSe series of one subject; the same build key on both sides, which only a per-ann fixed split could do);
  3. which val SOURCES carry the overlapping persons (a film source would move the quoted film numbers);
  4. the "v8 train" exposure as tools/make_split.py counts it (every ~/patient_keys.json case not in the bank's
     val_cases, bank or not) against the bank's own train split, for the G3 transitional val/test persons.

Reads only; writes one JSON. Grid, CPU job (the bank's `case` and `split` arrays are read, not the crops).
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools"))
import eval_gate as EG  # noqa: E402
import patient_keys as PK  # noqa: E402

H = os.path.expanduser("~")


def family(case):
    """The naming family of a bank case (which root / scheme wrote it)."""
    c = str(case)
    for pre in ("implant_", "BUU_FULL_", "CSXA_", "NHANES_", "CTSP_COLONOG_", "CTSP_VERSE_", "CTSP_", "ctsp_",
                "totalseg_", "verse_scan-", "verse_", "verse", "gl"):
        if c.startswith(pre):
            return pre.rstrip("_-")
    return "other"


def load_bank(bank):
    z = np.load(os.path.join(bank, "rung_1.npz"), allow_pickle=True)
    files = list(z.files)
    case = [str(c) for c in z["case"]]
    split = [str(s) for s in z["split"]]
    src = None
    for f in ("source", "src", "srcname", "root"):
        if f in files:
            src = [str(s) for s in z[f]]
            break
    person = [str(p) for p in z["person"]] if "person" in files else None
    return files, case, split, src, person


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", default=f"{H}/allspine_v8_fov96_ctx")
    ap.add_argument("--keys", default=f"{H}/patient_keys.json", help="the key file the bank was built with")
    ap.add_argument("--ckpt", default=f"{H}/allspine_v8_fov96_ctx/runs/model_rung_1_aug2.pt")
    ap.add_argument("--touched", default=EG.GRID_TOUCHED)
    ap.add_argument("--stratify", default=str(REPO / "SchwingNet/results/rare_class/stratify.json"))
    ap.add_argument("--split-final", default=f"{H}/split_final.json")
    ap.add_argument("--also-bank", action="append", default=[], metavar="TAG=BANK=KEYS",
                    help="another bank to run step 4 on (v9), e.g. v9=~/allspine_v9_fov96_ctx=~/patient_keys_v9.json")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.time()
    out = {"written": EG.now_iso(), "bank": a.bank, "keys": a.keys, "ckpt": a.ckpt, "touched": a.touched}

    files, case, split, src, person = load_bank(a.bank)
    out["bank_arrays"] = files
    side_of_case = collections.defaultdict(set)
    src_of_case = {}
    crops = collections.Counter()
    for i, (c, s) in enumerate(zip(case, split)):
        side_of_case[c].add(s)
        crops[(c, s)] += 1
        if src is not None:
            src_of_case.setdefault(c, src[i])
    person_of_case = {}
    if person is not None:
        for c, p in zip(case, person):
            person_of_case.setdefault(c, p)
    two_sided_cases = sorted(c for c, s in side_of_case.items() if len(s) > 1)
    out["cases"] = len(side_of_case)
    out["cases_on_two_sides"] = len(two_sided_cases)
    print(f"bank {a.bank}: {len(case)} crops, {len(side_of_case)} cases, {len(two_sided_cases)} cases on two sides; "
          f"arrays {files}", flush=True)

    pk = json.load(open(a.keys))["keys"]
    memo = {}

    def cur(c):
        """Today's gate key for a bank case: exactly what eval_gate.build_eval_set(kind=bank) computes."""
        if c not in memo:
            ks, _, unk = EG.key_items([dict(case=c)])
            memo[c] = sorted(ks)[0] if len(ks) == 1 else (sorted(ks) if ks else None)
        return memo[c]

    def build(c):
        return pk.get(c)

    # sides by today's key and by the build's key
    by_cur = collections.defaultdict(lambda: {"train": set(), "val": set()})
    by_build = collections.defaultdict(lambda: {"train": set(), "val": set()})
    unkeyed_now = []
    for c, ss in side_of_case.items():
        k = cur(c)
        if k is None or isinstance(k, list):
            unkeyed_now.append(c)
            continue
        for s in ss:
            by_cur[k][s].add(c)
            by_build[build(c) or f"UNKEYED:{c}"][s].add(c)
    both_cur = sorted(k for k, v in by_cur.items() if v["train"] and v["val"])
    both_build = sorted(k for k, v in by_build.items() if v["train"] and v["val"])
    out["persons_val_now"] = sum(1 for v in by_cur.values() if v["val"])
    out["persons_train_now"] = sum(1 for v in by_cur.values() if v["train"])
    out["persons_on_both_sides_now"] = len(both_cur)
    out["persons_on_both_sides_by_build_keys"] = len(both_build)
    out["unkeyed_now"] = unkeyed_now[:40]
    out["n_unkeyed_now"] = len(unkeyed_now)
    print(f"persons on both sides: {len(both_cur)} by today's keys, {len(both_build)} by the build's keys", flush=True)

    # the store's own count, for the same checkpoint
    try:
        st = EG.load_store(a.touched)
        k_, e, how = st.find(a.ckpt)
        tr = {PK.canon_key(x) for x in e.get("train_keys") or []}
        va = {PK.canon_key(x) for x in e.get("val_keys") or []}
        store_both = tr & va
        out["store"] = dict(match=how, train=len(tr), val=len(va), both=len(store_both),
                            both_equals_this=sorted(store_both) == both_cur,
                            only_store=sorted(store_both - set(both_cur))[:20],
                            only_this=sorted(set(both_cur) - store_both)[:20],
                            by_corpus=dict(collections.Counter(x.split(":", 1)[0] for x in store_both)))
        print("store:", out["store"], flush=True)
    except Exception as ex:  # noqa: BLE001
        out["store"] = f"{type(ex).__name__}: {ex}"

    # per person: the cases and the build keys that put it on two sides
    rows, causes = [], collections.Counter()
    val_src_hits = collections.Counter()
    val_crops_hit = collections.Counter()
    for k in both_cur:
        v, t = sorted(by_cur[k]["val"]), sorted(by_cur[k]["train"])
        bv = sorted({build(c) or f"UNKEYED:{c}" for c in v})
        bt = sorted({build(c) or f"UNKEYED:{c}" for c in t})
        if set(bv) & set(bt):
            cause = "same build key on both sides (a per-case split applied after the person draw)"
        elif any(x.startswith("implant:") for x in bv + bt):
            imp_v = any(x.startswith("implant:") for x in bv)
            imp_t = any(x.startswith("implant:") for x in bt)
            where = "val" if imp_v and not imp_t else "train" if imp_t and not imp_v else "both sides"
            cause = f"implant render filed as its own person (implant:<case>_v<k>) on the {where} side"
        elif all(x.startswith("verse:") for x in bv + bt):
            cause = "VerSe: two series of one subject filed as two persons (series keyed as subjects)"
        else:
            cause = f"build keys differ: {sorted({x.split(':', 1)[0] for x in bv})} (val) vs " \
                    f"{sorted({x.split(':', 1)[0] for x in bt})} (train)"
        causes[cause] += 1
        for c in v:
            val_src_hits[src_of_case.get(c) or family(c)] += 1
            val_crops_hit[src_of_case.get(c) or family(c)] += crops[(c, "val")]
        rows.append(dict(person=k, cause=cause,
                         val=[dict(case=c, family=family(c), source=src_of_case.get(c), build_key=build(c),
                                   bank_person=person_of_case.get(c)) for c in v][:12],
                         train=[dict(case=c, family=family(c), source=src_of_case.get(c), build_key=build(c),
                                     bank_person=person_of_case.get(c)) for c in t][:12],
                         n_val_cases=len(v), n_train_cases=len(t)))
    out["causes"] = dict(causes)
    out["by_corpus"] = dict(collections.Counter(k.split(":", 1)[0] for k in both_cur))
    out["cause_by_corpus"] = {}
    for r in rows:
        out["cause_by_corpus"].setdefault(r["person"].split(":", 1)[0], collections.Counter())[r["cause"]] += 1
    out["cause_by_corpus"] = {k: dict(v) for k, v in out["cause_by_corpus"].items()}
    out["val_cases_of_overlap_persons_by_source"] = dict(val_src_hits)
    out["val_crops_of_overlap_persons_by_source"] = dict(val_crops_hit)
    out["val_cases_by_source"] = dict(collections.Counter(src_of_case.get(c) or family(c)
                                                          for c, ss in side_of_case.items() if "val" in ss))
    out["val_crops_by_source"] = dict(collections.Counter(src_of_case.get(c) or family(c)
                                                          for (c, s), n in crops.items() if s == "val"
                                                          for _ in range(n)))
    out["persons"] = rows
    print("causes:", json.dumps(out["causes"], indent=1), flush=True)
    print("by corpus:", out["cause_by_corpus"], flush=True)
    print("val cases of the overlap persons by source:", out["val_cases_of_overlap_persons_by_source"], flush=True)

    # 4. the exposure count tools/make_split.py makes, against the bank's own train split
    fold = lambda k: k  # noqa: E731
    try:
        sf = json.load(open(a.split_final))
        r2g, gof, sop = sf.get("raw_to_group", {}), sf.get("group_of", {}), sf.get("side_of_person", {})

        def fold(k):  # noqa: F811
            g = r2g.get(k, k)
            return gof.get(g, g)
        out["split_final"] = dict(path=a.split_final, generated=sf.get("generated"), verdict=sf.get("verdict"))
    except Exception as ex:  # noqa: BLE001
        sop = {}
        out["split_final"] = f"{type(ex).__name__}: {ex}"
    strat = {}
    try:
        strat = json.load(open(a.stratify)).get("people") or {}
    except Exception as ex:  # noqa: BLE001
        out["stratify"] = f"{type(ex).__name__}: {ex}"

    def exposure(tag, bank, keys_path):
        if bank == a.bank:
            b_side, b_cases = side_of_case, set(side_of_case)
        else:
            _f, c2, s2, _src, _p = load_bank(bank)
            b_side = collections.defaultdict(set)
            for c, s in zip(c2, s2):
                b_side[c].add(s)
            b_cases = set(b_side)
        kk = json.load(open(keys_path))["keys"]
        meta = json.load(open(os.path.join(bank, "meta.json")))
        val_cases = set(meta.get("val_cases") or [])
        # make_split's reading: every key-file case not in val_cases counts as trained
        ms = collections.defaultdict(list)
        for c, k in kk.items():
            if c in val_cases:
                continue
            ms[fold(PK.canon_key(k))].append(c)
        # the bank's reading: the cases whose crops are in split == train, keyed as the gate keys them
        bk = collections.defaultdict(list)
        for c, ss in b_side.items():
            if "train" in ss:
                k = cur(c)
                if isinstance(k, str):
                    bk[fold(k)].append(c)
        not_in_bank = [c for c in kk if c not in b_cases and c not in val_cases]
        res = dict(bank=bank, keys=keys_path, trained_people_make_split=len(ms), trained_people_bank=len(bk),
                   keyfile_cases_not_in_bank=len(not_in_bank),
                   keyfile_cases_not_in_bank_by_family=dict(collections.Counter(family(c) for c in not_in_bank)),
                   only_make_split_by_corpus=dict(collections.Counter(p.split(":", 1)[0] for p in set(ms) - set(bk))),
                   only_bank_by_corpus=dict(collections.Counter(p.split(":", 1)[0] for p in set(bk) - set(ms))))
        g1 = {}
        for pkey, o in strat.items():
            if o.get("real") or pkey.startswith("cobra:") or o.get("side") not in ("val", "test"):
                continue
            fk = fold(PK.canon_key(pkey))
            side = sop.get(fk, o.get("side"))
            if side not in ("val", "test"):
                continue
            sub = o.get("subtype") or "?"
            cell = g1.setdefault(sub, dict(val_test=0, in_make_split=0, in_bank_train=0, make_split_only=[]))
            cell["val_test"] += 1
            a_ = fk in ms
            b_ = fk in bk
            cell["in_make_split"] += int(a_)
            cell["in_bank_train"] += int(b_)
            if a_ and not b_:
                cell["make_split_only"].append(dict(person=fk, cases=ms[fk][:6]))
        res["g1_val_test_exposure"] = g1
        return res, set(ms), set(bk)

    expo = {}
    sets = {}
    try:
        expo["v8"], ms8, bk8 = exposure("v8", a.bank, a.keys)
        sets["v8"] = (ms8, bk8)
    except Exception as ex:  # noqa: BLE001
        expo["v8"] = f"{type(ex).__name__}: {ex}"
    for spec in a.also_bank:
        tag, bank, keys_path = spec.split("=", 2)
        try:
            expo[tag], ms_, bk_ = exposure(tag, os.path.expanduser(bank), os.path.expanduser(keys_path))
            sets[tag] = (ms_, bk_)
        except Exception as ex:  # noqa: BLE001
            expo[tag] = f"{type(ex).__name__}: {ex}"
    # the union the split plan quotes ("val+test people in v8 or v9 train")
    if len(sets) >= 2:
        ms_u = set().union(*(s[0] for s in sets.values()))
        bk_u = set().union(*(s[1] for s in sets.values()))
        u = {}
        for pkey, o in strat.items():
            if o.get("real") or pkey.startswith("cobra:") or o.get("side") not in ("val", "test"):
                continue
            fk = fold(PK.canon_key(pkey))
            if sop.get(fk, o.get("side")) not in ("val", "test"):
                continue
            cell = u.setdefault(o.get("subtype") or "?", dict(val_test=0, in_make_split=0, in_bank_train=0,
                                                               make_split_only=[]))
            cell["val_test"] += 1
            cell["in_make_split"] += int(fk in ms_u)
            cell["in_bank_train"] += int(fk in bk_u)
            if fk in ms_u and fk not in bk_u:
                cell["make_split_only"].append(fk)
        expo["union_" + "_".join(sorted(sets))] = u
    out["exposure"] = expo
    print("exposure:", json.dumps({k: (v if isinstance(v, str) else {kk: vv for kk, vv in v.items()
                                                                        if kk != "g1_val_test_exposure"})
                                   for k, v in expo.items() if not k.startswith("union")}, indent=1)[:4000], flush=True)
    for k, v in expo.items():
        if k.startswith("union"):
            print(k, json.dumps(v)[:3000], flush=True)
        elif isinstance(v, dict):
            print(k, "g1:", json.dumps(v.get("g1_val_test_exposure"))[:3000], flush=True)
    out["seconds"] = round(time.time() - t0, 1)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1, default=list)
    print("wrote", a.out, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
