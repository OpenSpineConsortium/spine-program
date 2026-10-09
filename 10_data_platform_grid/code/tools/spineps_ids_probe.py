#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/spineps_ids_probe.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Adversarial probe of the SPINEPS id guard (tools/spineps_ids.py) on real masks: what must raise raises, what must
pass passes, and what the guard cannot see is written down.

Written for the F5 verification (SchwingNet/results/spineps_ids/VERIFY.md, item 2). Grid only (the masks live there):
    sbatch -D $HOME/spinesurg-ct-nnunet -p reqp --qos=requeue -c 2 --mem 16G -t 30 \
        --wrap "$HOME/mambaforge/envs/spineps/bin/python tools/spineps_ids_probe.py --out <dir>/probe.json"

Each case names what it expects: RAISE (the ids are not names), PASS (the ids are names), or LIMIT (the guard passes
it although another labeller disagrees -- the guard certifies VERIDAH's names, not the truth). A case whose file is
missing is reported as missing, never skipped silently. Exit 1 when any RAISE/PASS expectation fails.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spineps_ids as G  # noqa: E402

H = os.path.expanduser("~")
RS = "/rs/rs_grp_oschome/go2432/data"
REL_TS = f"{RS}/spineps/ctd_relabel/bench_ts_native"
REL_CTSP = f"{RS}/spineps/ctd_relabel/bench_native"
VERSE_GT = f"{H}/VerSeFusion/data/raw/verse20/03_test/verse607/verse607_CT-sag_seg.nii.gz"

CASES = [
    # (id, expectation, mask, ctd ('auto' | path | None), kwargs, why)
    ("raw_TS_s1089", "RAISE", f"{H}/bench_ts/spineps/native/TS_s1089_seg-vert_msk.nii.gz", "auto", {},
     "raw 1..25 enumeration; one of the twelve 'id 25 = L6' TS cases"),
    ("raw_COLONOG_1", "RAISE", f"{H}/bench/spineps/native/COLONOG_1_seg-vert_msk.nii.gz", "auto", {},
     "raw CTSP-benchmark mask (C4)"),
    ("raw_VERSE_verse607", "RAISE", f"{H}/bench_ts/spineps/native/VERSE_verse607_seg-vert_msk.nii.gz", "auto", {},
     "raw VerSe mask in bench_ts"),
    ("relabel_VERSE_verse607", "PASS", f"{REL_TS}/VERSE_verse607_seg-vert_msk.nii.gz", "auto", {},
     "the same CT after tools/spineps_ids.py relabel (VERIDAH L6)"),
    ("verse_expert_vs_veridah_ctd", "PASS", VERSE_GT, f"{REL_TS}/VERSE_verse607_ctd.json", {},
     "the VerSe EXPERT mask of verse607 tested against VERIDAH's own ctd points on that CT: not circular"),
    ("verse_expert_auto_ctd", "INFO", VERSE_GT, "auto", {},
     "the VerSe expert mask beside its legacy VerSe ctd (no TPTBox header): require_ctd refuses it"),
    ("verse_expert_no_require_ctd", "PASS", VERSE_GT, "auto", {"require_ctd": False},
     "the VerSe expert mask with require_ctd=False"),
    ("postfix_CTSP_0001", "PASS", f"{RS}/spineps/ctsp/CTSP_0001_seg-vert_msk.nii.gz", "auto", {},
     "post-fix VERIDAH derivative (COLONOG_1's CT)"),
    ("postfix_TS_s0109", "PASS", f"{H}/bench_ts/spineps/native/TS_s0109_seg-vert_msk.nii.gz", "auto", {},
     "post-fix retry mask carrying a real VERIDAH id 25"),
    ("relabel_COLONOG_10_skip", "RAISE", f"{REL_CTSP}/COLONOG_10_seg-vert_msk.nii.gz", "auto", {},
     "relabel reproduces VERIDAH's T12 skip; the reader shows the thoracic names one level low"),
    ("postfix_CTSP_0016_skip", "RAISE", f"{RS}/spineps/ctsp/CTSP_0016_seg-vert_msk.nii.gz", "auto", {},
     "post-fix derivative of the same CT as COLONOG_10: VERIDAH's own skip"),
    ("carm_case42_L6", "LIMIT", f"{RS}/carmlspine/spineps/case42_seg-vert_msk.nii.gz", "auto", {},
     "VERIDAH L2..L6 on the five bones TotalSegmentator reads L1..L5 (levels.json): ids == ctd, so the guard passes"),
    ("postfix_CTSP_0428_shift", "LIMIT", f"{RS}/spineps/ctsp/CTSP_0428_seg-vert_msk.nii.gz", "auto", {},
     "VERIDAH counts 4 lumbar where the reader has 5; every L1-L5 Dice < 0.5 in the post-fix re-score"),
]


def scramble_tests(out):
    """In-memory faults on clean masks, tested against their real ctd. A fault that leaves the mask unchanged is
    recorded as a no-op, not as a pass: a whole-spine C1..L6 mask renumbered 1..N top-down IS its own VerSe ids
    (relabelled VERSE_verse607 carries exactly 1..25), so that fault can only be tested on a field that does not
    start at C1 (CTSP_0001, T9..L5 + S)."""
    for tag, p in (("verse607", f"{REL_TS}/VERSE_verse607_seg-vert_msk.nii.gz"),
                   ("CTSP_0001", f"{RS}/spineps/ctsp/CTSP_0001_seg-vert_msk.nii.gz")):
        if not os.path.exists(p):
            out.append(dict(id=f"synthetic_{tag}", status="missing", path=p))
            continue
        _faults(out, tag, p)


def _faults(out, tag, p):
    arr, A, _ = G.load_mask(p)
    pts = G.read_ctd(G.find_ctd(p))
    ids = sorted(int(i) for i in np.unique(arr) if 0 < i < 100)
    rng = np.random.default_rng(0)
    perm = dict(zip(ids, rng.permutation(ids)))
    lut = np.zeros(max(ids) + 1, np.int32)
    for k, v in perm.items():
        lut[k] = v
    faults = {
        "permuted_ids": lut[np.where(arr < lut.size, arr, 0)],
        "shift_all_ids_down_one_level": np.where((arr > 1) & (arr < 26), arr - 1, arr),
        "raw_style_1_to_N_top_down": None,
    }
    # 1..N numbered top-down (a raw enumeration that happens to be ordered): ids no longer match the ctd names
    st = G.instance_stats(arr, A)
    order = sorted((i for i in st if i < 100), key=lambda i: -st[i][1][2])
    lut2 = np.zeros(max(ids) + 1, np.int32)
    for n, i in enumerate(order, 1):
        lut2[i] = n
    faults["raw_style_1_to_N_top_down"] = lut2[np.where(arr < lut2.size, arr, 0)]
    for name, a2 in faults.items():
        rec = dict(id=f"synthetic_{tag}_{name}", expect="RAISE", source=p)
        if np.array_equal(a2, arr):
            rec.update(status="no-op", got="the fault leaves the mask unchanged (its ids already are this numbering)")
            out.append(rec)
            continue
        try:
            G.assert_verse_monotonic((a2, A), pts, quiet=True)
            rec.update(status="FAIL", got="passed")
        except G.SpinepsIdError as e:
            rec.update(status="ok", got=str(e)[:300])
        out.append(rec)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res = []
    for cid, exp, mask, ctd, kw, why in CASES:
        rec = dict(id=cid, expect=exp, path=mask, ctd=ctd, why=why)
        if not os.path.exists(mask):
            rec["status"] = "missing"
            res.append(rec)
            continue
        t0 = time.time()
        rep = G.check_ids(mask, ctd if ctd != "auto" else "auto")
        rec["check"] = {k: rep.get(k) for k in ("verdict", "ids", "ctd", "ctd_agree", "ctd_disagree", "ctd_labels",
                                                  "order_top_to_bottom", "veridah_skipped_names", "reasons",
                                                  "median_ml_named_cervical", "median_ml_named_lumbar")}
        try:
            G.assert_verse_monotonic(mask, ctd, quiet=True, **kw)
            rec["guard"] = "passed"
        except G.SpinepsIdError as e:
            rec["guard"] = "raised"
            rec["error"] = str(e)[:400]
        want = {"RAISE": "raised", "PASS": "passed", "LIMIT": "passed"}.get(exp)
        rec["status"] = "ok" if want is None or rec["guard"] == want else "FAIL"
        rec["seconds"] = round(time.time() - t0, 1)
        res.append(rec)
        print(f"{rec['status']:<7} {cid:<32} expect {exp:<5} guard {rec['guard']:<6} verdict {rep.get('verdict')}",
              flush=True)
    scramble_tests(res)
    for r in res:
        if r["id"].startswith("synthetic"):
            print(f"{r.get('status'):<7} {r['id']:<32} expect RAISE {r.get('got', '')[:120]}", flush=True)
    bad = [r["id"] for r in res if r.get("status") == "FAIL"]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    import hashlib
    gmd5 = hashlib.md5(open(G.__file__, "rb").read()).hexdigest()
    json.dump(dict(generated=time.strftime("%Y-%m-%d %H:%M:%S"), guard_md5=gmd5, cases=res, failed=bad,
                   missing=[r["id"] for r in res if r.get("status") == "missing"]),
              open(a.out, "w"), indent=1, default=str)
    print("PROBE_DONE failed=", bad, flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
