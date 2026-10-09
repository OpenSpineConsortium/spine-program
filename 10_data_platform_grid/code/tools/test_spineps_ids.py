#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_spineps_ids.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Synthetic checks for tools/spineps_ids.py: the guard raises on a raw enumeration and passes VerSe names; the
relabel recovers names from a ctd, names C1, takes the semantic sacrum, and refuses a skipped name (the TS_s1178
error), a point in the wrong instance, and an unnamed vertebra inside the column.

    python tools/test_spineps_ids.py          (exit 0 = all pass)
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import spineps_ids as S  # noqa: E402

A = np.diag([1.5, 1.5, 1.5, 1.0])
A[:3, 3] = [-50.0, -50.0, -600.0]


def spine(labels, spacing=20, gap_after=None, shape=(40, 40, 420)):
    """Boxes stacked along +S (axis 2), top of the column first; returns (arr with VerSe ids, ctd points)."""
    arr = np.zeros(shape, np.int32)
    pts = {}
    z = shape[2] - 12
    for lab in labels:
        zc = z
        arr[14:26, 14:26, zc - 5: zc + 5] = lab
        pts[lab] = A[:3, :3] @ np.array([20.0, 20.0, zc - 0.5]) + A[:3, 3]
        z -= int(spacing / 1.5)
        if gap_after is not None and lab == gap_after:
            z -= int(spacing / 1.5)
    return arr, pts


def scramble(arr, seed=0):
    ids = sorted(int(x) for x in np.unique(arr) if x)
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(ids)) + 1
    lut = np.zeros(max(ids) + 1, np.int32)
    for i, p in zip(ids, perm):
        lut[i] = p
    return lut[arr]


def expect_raise(fn, what):
    try:
        fn()
    except S.SpinepsIdError as e:
        print(f"ok   raises: {what}: {str(e)[:150]}")
        return getattr(e, "report", None)
    raise AssertionError(f"did not raise: {what}")


def main() -> int:
    labs = list(range(2, 25))                                   # C2..L5, the ctd never names C1
    arr, pts = spine([1] + labs)
    pts.pop(1)
    rep = S.assert_verse_monotonic((arr, A), pts)
    assert rep["verdict"] == "verse_ok", rep
    print("ok   VerSe-named C1..L5 passes:", rep["verdict"], rep["ctd_agree"])

    raw = scramble(arr, 3)
    expect_raise(lambda: S.assert_verse_monotonic((raw, A), pts), "scrambled 1..24 with its ctd")
    expect_raise(lambda: S.assert_verse_monotonic((raw, A), None), "scrambled, no ctd (require_ctd)")
    # a raw enumeration that happens to run top-down: monotonic by integer, so only the ctd catches it
    small, spts = spine([22, 23, 24])
    small_raw = np.where(small > 0, small - 21, 0)
    expect_raise(lambda: S.assert_verse_monotonic((small_raw, A), spts), "ordered raw 1..3 over L3-L5")

    new, r = S.relabel_by_ctd(raw, A, pts)
    assert np.array_equal(new, arr), "relabel did not recover the names"
    assert any("named C1" in n for n in r["notes"]), r["notes"]
    print("ok   relabel recovers C1..L5 from a scramble; C1 named:", r["mapping"].get(str(int(raw[20, 20, 420 - 12]))))

    # sacrum from the semantic mask; an S1 piece below the column becomes 26
    arr2, pts2 = spine(list(range(17, 25)) + [26])
    sem = np.zeros_like(arr2)
    sem[arr2 == 26] = 26
    sem[10:30, 10:30, 5:20] = 26                                # more sacrum below, not in any instance
    raw2 = scramble(arr2, 5)
    new2, r2 = S.relabel_by_ctd(raw2, A, pts2, (sem, A))
    assert (new2[10:30, 10:30, 5:20] == 26).all() and r2["sacrum_semantic_voxels_added"] > 0, r2
    print("ok   semantic sacrum voxels added:", r2["sacrum_semantic_voxels_added"])

    # a raw tree has no semantic sacrum: the instance holding the S point is an S1 piece and is never named 26
    new2b, r2b = S.relabel_by_ctd(raw2, A, pts2)
    assert 26 not in np.unique(new2b) and r2b["sacrum"].startswith("absent"), r2b
    assert set(np.unique(new2b)) - {0} == set(range(17, 25)), np.unique(new2b)
    print("ok   no semantic sacrum -> no 26 written:", r2b["sacrum"][:60])

    # VERIDAH names lumbar-sized bones cervical (carmlspine case134's plain mask): ids agree with the ctd, still raises
    big = np.zeros((60, 60, 300), np.int32)
    bpts = {}
    for k, lab in enumerate([1, 2, 3, 4, 5]):
        zc = 280 - k * 45
        big[10:50, 10:50, zc - 19: zc + 19] = lab                 # 40 x 40 x 38 voxels at 1.5 mm = 205 ml each
        bpts[lab] = A[:3, :3] @ np.array([30.0, 30.0, zc - 0.5]) + A[:3, 3]
    bpts.pop(1)
    expect_raise(lambda: S.assert_verse_monotonic((big, A), bpts), "VERIDAH calls lumbar-sized bones C1..C5")

    # compare_masks reads each instance at its own voxel: a ring (C1) around a core (the dens of C2) is not misread
    ring = np.zeros((30, 30, 30), np.int32)
    ring[5:25, 5:25, 10:16] = 1
    ring[11:19, 11:19, 5:25] = 2
    cm = S.compare_masks((ring, A), (ring.copy(), A))
    assert cm["diff"] == 0 and cm["same"] == 2, cm
    print("ok   compare_masks: a ring's centroid inside another instance is not a name difference:", cm)

    # VERIDAH skips T12 at a normal spacing (TS_s1178): refuse
    arr3, pts3 = spine(list(range(15, 25)))                     # T8..L5 ten instances
    names3 = {15: 15, 16: 16, 17: 17, 18: 18, 19: 20, 20: 21, 21: 22, 22: 23, 23: 24, 24: 25}   # T12 onward shifted
    pts3b = {names3[k]: v for k, v in pts3.items()}
    rep3 = expect_raise(lambda: S.relabel_by_ctd(scramble(arr3, 7), A, pts3b, refuse_skipped_names=True),
                        "ctd skips T12 at normal spacing, --refuse-skipped-names")
    assert rep3["veridah_skipped_names"], rep3
    new3, r3 = S.relabel_by_ctd(scramble(arr3, 7), A, pts3b)
    assert r3["veridah_skipped_names"] and 19 not in np.unique(new3), r3
    print("ok   default: a skipped T12 is reproduced as VERIDAH wrote it and flagged:", r3["veridah_skipped_names"][0]["missing"])
    # ...and the guard refuses to read names from it (names on one side of the skip are one level off), unless the
    # caller gates every name with another labeller
    expect_raise(lambda: S.assert_verse_monotonic((new3, A), pts3b), "the guard on a mask whose ctd skips T12")
    assert S.assert_verse_monotonic((new3, A), pts3b, allow_skipped_names=True)["verdict"] == "verse_ok"
    print("ok   allow_skipped_names=True lets a gated reader through")

    # a real missing vertebra (wide gap) is accepted
    arr4, pts4 = spine([15, 16, 17, 18, 20, 21, 22, 23, 24], gap_after=18)
    arr4[arr4 == 0] = 0
    new4, r4 = S.relabel_by_ctd(scramble(arr4, 9), A, pts4)
    assert r4["ctd_gaps_accepted"] and np.array_equal(new4, arr4), r4
    assert S.assert_verse_monotonic((new4, A), pts4)["verdict"] == "verse_ok"      # a missed vertebra is not a skip
    print("ok   wide gap accepted as a vertebra SPINEPS missed (and the guard passes it):", r4["ctd_gaps_accepted"][0]["missing"])

    # an unnamed vertebra-sized instance inside the column: refuse
    arr5, pts5 = spine(list(range(15, 25)))
    p5 = dict(pts5)
    p5.pop(20)                                                  # L1 unnamed while L2..L5 and T12 are named
    expect_raise(lambda: S.relabel_by_ctd(scramble(arr5, 11), A, p5), "ctd omits a level (T12 -> L2)")

    # two points in one instance: refuse
    arr6, pts6 = spine(list(range(17, 25)))
    p6 = dict(pts6)
    p6[25] = p6[24] + np.array([0, 0, -2.0])                    # an L6 point inside L5
    expect_raise(lambda: S.relabel_by_ctd(scramble(arr6, 13), A, p6), "L5 and L6 points in one instance")

    # a ctd out of order: refuse
    p7 = dict(pts6)
    p7[26] = p7[17] + np.array([0, 0, 30.0])
    expect_raise(lambda: S.relabel_by_ctd(scramble(arr6, 13), A, p7), "sacrum point above the column")
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
