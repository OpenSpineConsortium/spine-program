#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/audit_realxray_lists.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Census of what EVERY trained detector arm actually saw: the lists on disk, not the code that wrote them.

Reads each run's own data.yaml under ~/spine-detector/runs/realxray (and any other --runs root), resolves every
image directory it names, and counts:

  images            files the trainer listed
  distinct_files    distinct os.path.realpath -- a symlink view bank (cobra_elekta_ap45) collapses onto its parent
  distinct_frames   distinct (ROOT BANK, stem): the same projection re-windowed into a new PNG is ONE frame, so
                    this is the number of real X-ray exposures behind the list
  distinct_cases    distinct case ids behind the list, via the root bank
  duplicates        images - distinct_frames: how many times the trainer saw a frame it had already seen

and the two things that would be worse than duplication if they were true, so they are measured rather than
assumed: whether a case id appears in BOTH the train list and the val list of one arm (model-selection leak), and
whether the derived banks' splits.json differ from their parent's (train/test leak). Also runs the same count over
each arm's scores.json, because a test set scored four times weights that device four times in any average.

Root bank = follow tools/realxray_banks.json derived_of, else the from_dataset in the bank's subset.json /
rewindow.json marker. A bank that is neither registered nor marked is reported as its own root and FLAGGED.

    python tools/audit_realxray_lists.py --out /rs/rs_grp_oschome/go2432/tmp/realxray_lists_audit.json

Resumable: exits immediately if --out exists and is a complete report, unless --force.
Final line: REALXRAY_LIST_AUDIT_DONE arms=<n> dirty=<n> leaks=<n>
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_registry():
    p = HERE / "realxray_banks.json"
    if p.exists():
        return json.load(open(p))["banks"]
    return {}


def bank_parent(bank_dir, reg):
    """The bank this one is a second rendering of, or None. Registry first, then the builder's own marker file."""
    name = os.path.basename(bank_dir.rstrip("/"))
    meta = reg.get(name) or {}
    if meta.get("derived_of"):
        return meta["derived_of"], "registry"
    for marker in ("subset.json", "rewindow.json"):
        p = os.path.join(bank_dir, marker)
        if os.path.exists(p):
            try:
                fd = json.load(open(p)).get("from_dataset")
            except Exception:
                fd = None
            if fd:
                return fd, marker
    return None, None


def root_bank(name, root, reg, _seen=None):
    """Follow the derived chain to the independent bank at the bottom of it."""
    _seen = _seen or set()
    if name in _seen:
        return name, ["CYCLE"]
    _seen.add(name)
    parent, how = bank_parent(os.path.join(root, name), reg)
    if not parent:
        return name, []
    r, chain = root_bank(parent, root, reg, _seen)
    return r, [f"{name} <-{how}- {parent}"] + chain


def stems(d):
    return sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(d, "*.png")))


def case_of(stem):
    """<case>_<frame> (docs/REAL_XRAY_DATASETS_SPEC.md); the case precedes the first underscore."""
    return stem.split("_")[0]


SPLIT_KEYS = ("train", "val", "test")


def bank_cases(bank_dir):
    """{split: {case ids}} from splits.json -- ONLY the three split keys, only string entries.

    splits.json is not one schema: deepfluoro's also carries `rule` (a string), `md5_bucket`/`frames` (dicts) and
    `loso` (a list of per-specimen dicts). Iterating .values() raises on `loso` and silently turns `rule` into
    one-character case ids.
    """
    sp = os.path.join(bank_dir, "splits.json")
    if not os.path.exists(sp):
        return None
    d = json.load(open(sp))
    out = {s: {x for x in (d.get(s) or []) if isinstance(x, str)} for s in SPLIT_KEYS}
    return out if any(out.values()) else None


def measure(dirs, root, reg, cache):
    """One list of image directories -> the counts above."""
    images = realpaths = 0
    frames, cases, per_bank, flags = set(), set(), Counter(), []
    rp = set()
    for d in dirs:
        if not os.path.isdir(d):
            flags.append(f"MISSING DIR {d}")
            continue
        bank = Path(d).parent.parent.name
        if bank not in cache:
            cache[bank] = root_bank(bank, root, reg)
        rb, chain = cache[bank]
        if rb == bank and bank not in reg:
            flags.append(f"UNCLASSIFIED BANK {bank} (not in realxray_banks.json, no subset.json/rewindow.json)")
        ss = stems(d)
        images += len(ss)
        per_bank[bank] += len(ss)
        for s in ss:
            frames.add((rb, s))
            cases.add((rb, case_of(s)))
        for p in glob.glob(os.path.join(d, "*.png")):
            rp.add(os.path.realpath(p))
    realpaths = len(rp)
    return dict(dirs=dirs, images=images, distinct_files=realpaths, distinct_frames=len(frames),
                distinct_cases=len(cases), duplicates=images - len(frames),
                exact_file_duplicates=images - realpaths,
                images_per_bank=dict(sorted(per_bank.items())), flags=flags), frames, cases


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/rs/rs_grp_oschome/go2432/data/realxray")
    ap.add_argument("--runs", default=os.path.expanduser("~/spine-detector/runs/realxray"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    if os.path.exists(a.out) and not a.force:
        try:
            prev = json.load(open(a.out))
            if prev.get("complete"):
                print(f"already complete: {a.out}")
                print(f"REALXRAY_LIST_AUDIT_DONE arms={len(prev['arms'])} "
                      f"dirty={sum(1 for v in prev['arms'].values() if v['train']['duplicates'])} "
                      f"leaks={len(prev['leaks'])}")
                return 0
        except Exception:
            pass

    reg, cache = load_registry(), {}
    import yaml

    # 1. the banks on disk
    banks = {}
    for p in sorted(glob.glob(os.path.join(a.root, "*", "data.yaml"))):
        d = os.path.dirname(p)
        n = os.path.basename(d)
        parent, how = bank_parent(d, reg)
        rb, chain = root_bank(n, a.root, reg)
        sp = bank_cases(d)
        banks[n] = dict(path=d, registered=n in reg, role=(reg.get(n) or {}).get("role"),
                        parent=parent, parent_from=how, root_bank=rb, chain=chain,
                        images={s: len(stems(os.path.join(d, "images", s))) for s in ("train", "val", "test")},
                        cases={s: sorted(v) for s, v in (sp or {}).items()} if sp else None,
                        splits_json=os.path.exists(os.path.join(d, "splits.json")))

    # 2. do the derived banks carry their parent's split? (a different split would be a train/test leak, not a dup)
    split_mismatch = []
    for n, b in banks.items():
        if b["parent"] and b["cases"] and banks.get(b["parent"], {}).get("cases"):
            pc = banks[b["parent"]]["cases"]
            for s in set(pc) | set(b["cases"]):
                if set(b["cases"].get(s, [])) - set(pc.get(s, [])):
                    split_mismatch.append(f"{n}/{s} holds cases its parent {b['parent']} does not put in {s}")

    # 3. every trained arm, from ITS OWN data.yaml
    arms, leaks = {}, []
    for p in sorted(glob.glob(os.path.join(a.runs, "*", "data.yaml"))):
        name = os.path.basename(os.path.dirname(p))
        y = yaml.safe_load(open(p))
        tr, va = y.get("train") or [], y.get("val") or []
        tr = [tr] if isinstance(tr, str) else tr
        va = [va] if isinstance(va, str) else va
        mt, ftr, ctr = measure(tr, a.root, reg, cache)
        mv, fva, cva = measure(va, a.root, reg, cache)
        shared_cases = sorted(c for c in ctr & cva)
        shared_frames = sorted(f"{b}/{s}" for b, s in (ftr & fva))
        if shared_cases:
            leaks.append(f"{name}: {len(shared_cases)} case ids in BOTH its train and its val list: "
                         + ", ".join(f"{b}:{c}" for b, c in shared_cases[:8]))
        w = os.path.join(os.path.dirname(p), "weights", "best.pt")
        sc = os.path.join(os.path.dirname(p), "scores.json")
        scored = {}
        if os.path.exists(sc):
            try:
                res = json.load(open(sc)).get("results", {})
                # Count (root bank, SPLIT), not root bank: a lodo arm scoring its held-out device's train, val and
                # test is the arm's definition, not a defect. Scoring one split of one device through several
                # banks -- init18's cobra_elekta test set through cobra_elekta, _ap45, _v2 and _v2_ap45 -- is the
                # defect, because any average over "datasets" then weights that device four times.
                bysplit, banks_per = Counter(), {}
                for k in res:
                    ds, _, sp = k.partition("/")
                    if ds not in cache:
                        cache[ds] = root_bank(ds, a.root, reg)
                    key = f"{cache[ds][0]}/{sp}"
                    bysplit[key] += 1
                    banks_per.setdefault(key, []).append(ds)
                scored = dict(splits_scored=sorted(res),
                              same_device_split_scored_through_several_banks=
                              {k: sorted(banks_per[k]) for k, v in bysplit.items() if v > 1},
                              device_splits_scored=dict(sorted(bysplit.items())))
            except Exception as e:
                scored = dict(error=str(e))
        arms[name] = dict(data_yaml=p, data_yaml_mtime=os.path.getmtime(p),
                          weights_mtime=os.path.getmtime(w) if os.path.exists(w) else None,
                          train=mt, val=mv,
                          train_val_shared_cases=[f"{b}:{c}" for b, c in shared_cases],
                          train_val_shared_frames=shared_frames[:20],
                          n_train_val_shared_frames=len(shared_frames),
                          scores=scored,
                          clean=(mt["duplicates"] == 0 and mv["duplicates"] == 0 and not shared_cases))

    rep = dict(complete=True, root=a.root, runs=a.runs, banks=banks, split_mismatch=split_mismatch,
               arms=arms, leaks=leaks)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(rep, open(a.out, "w"), indent=1)

    print(f"\n== banks under {a.root}")
    for n, b in banks.items():
        print(f"  {n:24s} role={b['role']}  root_bank={b['root_bank']}  "
              f"train/val/test {b['images']['train']}/{b['images']['val']}/{b['images']['test']}"
              + (f"  chain: {' ; '.join(b['chain'])}" if b["chain"] else ""))
    print(f"\n== arms under {a.runs}")
    for n, v in sorted(arms.items()):
        t, w = v["train"], v["val"]
        print(f"  {n:32s} {'CLEAN' if v['clean'] else 'DUPLICATED'}")
        print(f"      train {t['images']:6d} images -> {t['distinct_frames']:6d} frames, {t['distinct_cases']:4d} cases,"
              f" {t['duplicates']:6d} duplicate ({t['exact_file_duplicates']} byte-identical)")
        print(f"      val   {w['images']:6d} images -> {w['distinct_frames']:6d} frames, {w['distinct_cases']:4d} cases,"
              f" {w['duplicates']:6d} duplicate ({w['exact_file_duplicates']} byte-identical)")
        if t["images_per_bank"]:
            print(f"      train banks: {t['images_per_bank']}")
        for k, bs in (v["scores"].get("same_device_split_scored_through_several_banks") or {}).items():
            print(f"      ONE TEST SET SCORED {len(bs)} TIMES: {k} through {bs}")
        for f in t["flags"] + w["flags"]:
            print(f"      FLAG {f}")
    if split_mismatch:
        print("\n== derived banks whose split differs from their parent's (would be a train/test leak):")
        for s in split_mismatch:
            print("  " + s)
    else:
        print("\n== every derived bank carries its parent's split: no case crosses train/test through them")
    if leaks:
        print("\n== train/val case leaks:")
        for s in leaks:
            print("  " + s)
    dirty = sum(1 for v in arms.values() if not v["clean"])
    print(f"\nwrote {a.out}")
    print(f"REALXRAY_LIST_AUDIT_DONE arms={len(arms)} dirty={dirty} leaks={len(leaks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
