#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_realxray_banks.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Tests for the real-X-ray bank admission rule (tools/realxray_banks.json + realxray_train.ready/assert_disjoint).

The defect these guard (docs/DATA_COMPLETENESS_AUDIT.md, Repairs 2026-09-23): three derived banks --
cobra_elekta_v2 (the same frames re-windowed), cobra_elekta_ap45 and cobra_elekta_v2_ap45 (symlink view subsets) --
entered a pooled training list as if they were separate machines, so 145 COBRA patients were trained on up to four
times. Nothing raised, because the only filter was a test on the directory's NAME.

    python tools/test_realxray_banks.py                 # fixtures only (runs anywhere)
    python tools/test_realxray_banks.py --root /rs/rs_grp_oschome/go2432/data/realxray   # + the real banks

Exit 0 = every test passed. Any failure prints the case and exits 1.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import realxray_train as RT  # noqa: E402

FAILURES = []


def check(name, fn):
    try:
        fn()
    except AssertionError as e:
        FAILURES.append(f"{name}: {e}")
        print(f"FAIL {name}: {e}")
    else:
        print(f"ok   {name}")


def make_bank(root, name, cases, splits=("train", "val", "test"), write_splits=True, n_frames=2):
    """A minimal bank on disk: images, labels, splits.json, data.yaml."""
    d = Path(root) / name
    assign = {s: [] for s in splits}
    for i, c in enumerate(cases):
        s = splits[i % len(splits)]
        assign[s].append(c)
        for k in range(n_frames):
            (d / "images" / s).mkdir(parents=True, exist_ok=True)
            (d / "labels" / s).mkdir(parents=True, exist_ok=True)
            (d / "images" / s / f"{c}_{k:04d}.png").write_bytes(b"")
            (d / "labels" / s / f"{c}_{k:04d}.txt").write_text("0 0.5 0.5 0.2 0.2\n")
    if write_splits:
        json.dump(assign, open(d / "splits.json", "w"))
    (d / "data.yaml").write_text(f"path: {d}\ntrain: images/train\nval: images/val\ntest: images/test\n")
    return d


def with_registry(banks, body):
    """Run body() with tools/realxray_banks.json temporarily replaced by `banks`."""
    real = RT.REGISTRY
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump({"banks": banks}, fh)
        tmp = fh.name
    RT.REGISTRY = Path(tmp)
    try:
        return body()
    finally:
        RT.REGISTRY = real
        os.unlink(tmp)


# ---------------------------------------------------------------- fixture tests

def t_unregistered_bank_is_refused():
    """The bug itself: a directory appears under ROOT and nothing in the code names it."""
    with tempfile.TemporaryDirectory() as root:
        make_bank(root, "alpha", ["A1", "A2", "A3"])
        make_bank(root, "alpha_v2", ["A1", "A2", "A3"])          # a re-display nobody classified
        reg = {"alpha": {"role": "device"}}
        def go():
            try:
                RT.ready(root)
            except SystemExit as e:
                return str(e)
            return None
        msg = with_registry(reg, go)
        assert msg is not None, "ready() admitted or silently skipped a bank absent from the registry"
        assert "alpha_v2" in msg, f"the refusal must name the offending bank; got {msg!r}"


def t_derived_bank_never_enters_pooled():
    with tempfile.TemporaryDirectory() as root:
        make_bank(root, "alpha", ["A1", "A2", "A3"])
        make_bank(root, "alpha_v2", ["A1", "A2", "A3"])
        reg = {"alpha": {"role": "device"}, "alpha_v2": {"role": "derived", "derived_of": "alpha"}}
        avail = with_registry(reg, lambda: RT.ready(root))
        assert set(avail) == {"alpha"}, f"pooled admission must be devices only; got {sorted(avail)}"


def t_smoke_bank_never_enters():
    with tempfile.TemporaryDirectory() as root:
        make_bank(root, "alpha", ["A1", "A2", "A3"])
        make_bank(root, "alpha_smoke", ["A1"])
        reg = {"alpha": {"role": "device"}, "alpha_smoke": {"role": "smoke"}}
        avail = with_registry(reg, lambda: RT.ready(root))
        assert set(avail) == {"alpha"}, f"got {sorted(avail)}"


def t_two_devices_sharing_a_case_are_refused():
    """The independent check: whatever the registry SAYS, the files must not overlap."""
    with tempfile.TemporaryDirectory() as root:
        make_bank(root, "alpha", ["A1", "A2", "A3"])
        make_bank(root, "beta", ["A2", "B1", "B2"])              # A2 is in both, and both claim to be devices
        reg = {"alpha": {"role": "device"}, "beta": {"role": "device"}}
        def go():
            avail = RT.ready(root)
            try:
                RT.arm_sets("pooled", avail)
            except SystemExit as e:
                return str(e)
            return None
        msg = with_registry(reg, go)
        assert msg is not None, "a pooled arm over two banks sharing case A2 was built without raising"
        assert "A2" in msg, f"the refusal must name the shared case; got {msg!r}"


def t_lodo_refuses_a_shared_case():
    with tempfile.TemporaryDirectory() as root:
        make_bank(root, "alpha", ["A1", "A2", "A3"])
        make_bank(root, "beta", ["A2", "B1", "B2"])
        reg = {"alpha": {"role": "device"}, "beta": {"role": "device"}}
        def go():
            avail = RT.ready(root)
            try:
                RT.arm_sets("lodo:beta", avail)
            except SystemExit as e:
                return str(e)
            return None
        msg = with_registry(reg, go)
        assert msg is not None, "lodo:beta trained on alpha although alpha contains beta's case A2"


def t_disjoint_devices_pass():
    with tempfile.TemporaryDirectory() as root:
        make_bank(root, "alpha", ["A1", "A2", "A3"])
        make_bank(root, "beta", ["B1", "B2", "B3"])
        reg = {"alpha": {"role": "device"}, "beta": {"role": "device"}}
        def go():
            avail = RT.ready(root)
            tr, va, score = RT.arm_sets("pooled", avail)
            return tr, score
        tr, score = with_registry(reg, go)
        assert len(tr) == 2, f"two devices should give two train dirs; got {tr}"
        assert sorted(n for n, _ in score) == ["alpha", "beta"], score


def t_case_ids_fall_back_to_stems_without_splits_json():
    with tempfile.TemporaryDirectory() as root:
        d = make_bank(root, "alpha", ["A1", "A2"], write_splits=False)
        assert RT.case_ids(d) == {"A1", "A2"}, RT.case_ids(d)


def t_case_ids_reads_only_the_split_keys():
    """splits.json is not one schema. deepfluoro's carries `rule` (str), `md5_bucket`/`frames` (dict) and `loso`
    (list of dicts) beside train/val/test. Iterating .values() raises on loso -- and would silently have turned
    the 300-character `rule` string into 300 one-letter case ids if loso were absent."""
    with tempfile.TemporaryDirectory() as root:
        d = make_bank(root, "alpha", ["A1", "A2", "A3"])
        j = json.load(open(d / "splits.json"))
        j["rule"] = "test fixed to A3 (coordinator's choice); val by md5 bucket. Split BY SPECIMEN."
        j["md5_bucket"] = {"A1": 7, "A2": 4, "A3": 7}
        j["frames"] = {"A1": 111, "A2": 24, "A3": 24}
        j["loso"] = [{"test": ["A1"], "train": ["A2", "A3"]}, {"test": ["A2"], "train": ["A1", "A3"]}]
        json.dump(j, open(d / "splits.json", "w"))
        got = RT.case_ids(d)
        assert got == {"A1", "A2", "A3"}, f"case_ids must read train/val/test only; got {sorted(got)}"


def t_case_ids_refuses_a_non_string_case_list():
    with tempfile.TemporaryDirectory() as root:
        d = make_bank(root, "alpha", ["A1", "A2", "A3"])
        j = json.load(open(d / "splits.json"))
        j["train"] = [{"case": "A1"}]
        json.dump(j, open(d / "splits.json", "w"))
        try:
            RT.case_ids(d)
        except SystemExit as e:
            assert "non-string" in str(e), str(e)
        else:
            raise AssertionError("a split list of dicts was accepted as case ids")


def t_only_arm_can_name_a_derived_bank():
    with tempfile.TemporaryDirectory() as root:
        make_bank(root, "alpha", ["A1", "A2", "A3"])
        make_bank(root, "alpha_multi", ["A1", "A2", "A3"])
        reg = {"alpha": {"role": "device"}, "alpha_multi": {"role": "derived", "derived_of": "alpha"}}
        avail = with_registry(reg, lambda: RT.ready(root, only="alpha_multi"))
        assert "alpha_multi" in avail, "only:<derived bank> must still be reachable by name"


# ---------------------------------------------------------------- the real banks

def t_real_root(root):
    reg = RT.registry()
    import glob
    on_disk = sorted(Path(p).parent.name for p in glob.glob(os.path.join(root, "*", "data.yaml")))
    missing = [n for n in on_disk if n not in reg]
    assert not missing, f"banks on disk with no entry in tools/realxray_banks.json: {missing}"
    avail = RT.ready(root)
    devices = sorted(n for n in avail if avail[n]["role"] == "device")
    RT.assert_disjoint(devices, avail)
    derived = sorted(n for n, m in reg.items() if m.get("role") == "derived")
    for n in derived:
        assert n not in avail, f"{n} is registered derived but ready() admitted it"
    print(f"     admitted devices: {devices}")
    print(f"     registered derived (correctly excluded): {derived}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="also test the real bank root (grid only)")
    a = ap.parse_args()
    for fn in (t_unregistered_bank_is_refused, t_derived_bank_never_enters_pooled, t_smoke_bank_never_enters,
               t_two_devices_sharing_a_case_are_refused, t_lodo_refuses_a_shared_case, t_disjoint_devices_pass,
               t_case_ids_fall_back_to_stems_without_splits_json, t_case_ids_reads_only_the_split_keys,
               t_case_ids_refuses_a_non_string_case_list, t_only_arm_can_name_a_derived_bank):
        check(fn.__name__, fn)
    if a.root and os.path.isdir(a.root):
        check("t_real_root", lambda: t_real_root(a.root))
    elif a.root:
        print(f"skip t_real_root: {a.root} does not exist here")
    print(f"\nREALXRAY_BANKS_TEST {'PASS' if not FAILURES else 'FAIL'} failures={len(FAILURES)}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
