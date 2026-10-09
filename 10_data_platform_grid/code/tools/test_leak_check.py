#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_leak_check.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Does tools/leak_check.py actually catch the defect it was written for? Synthetic ledgers, no grid, no data.

The NHANES double inclusion (docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md) is reproduced in miniature: one bank
holding the same three patients twice, once as source `nhanes` with cases `NHANES_nhanes_cervical_00160` and once
as source `nhanes_drr` with cases `NH_00160_c`, each copy split independently so the two copies of a patient land
on opposite sides. The test asserts BOTH halves of the point:

  * check (1), the per-source view every earlier audit used, reports the bank as CLEAN -- which is why the defect
    survived until 2026-09-22;
  * check (2), on the cross-source key, reports both patients, and check (3) names the two sources structurally
    without any list of corpus names.

The other four checks get a minimal fixture each: a real-frame dataset with a specimen in train and in test, a
model whose evaluation set is inside its training set, two renders of one CT split apart, and a styled corpus
rendered under the pose of a specimen that is in a real test split. A file that matches no keying rule is
included on purpose, to prove the run fails rather than treating the unknown name as a new patient.

    python tools/test_leak_check.py            # prints every assertion and the tool's own output
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

TOOL = Path(__file__).resolve().parent / "leak_check.py"

# --- the synthetic bank, as make_context_crops.py would write it -----------------------------------------------
# (case, split, source). Two crops per case, to prove the per-case collapse works.
BANK_ROWS = [
    # copy A: the film directory, source `nhanes`, patients 00160 / 00161 / 00162
    ("NHANES_nhanes_cervical_00160", "train", "nhanes"),
    ("NHANES_nhanes_lumbar_00160", "train", "nhanes"),
    ("NHANES_nhanes_cervical_00161", "val", "nhanes"),
    ("NHANES_nhanes_cervical_00162", "train", "nhanes"),
    # copy B: the same three patients again under the render directory's own name, split independently
    ("NH_00160_c", "val", "nhanes_drr"),
    ("NH_00160_l", "val", "nhanes_drr"),
    ("NH_00161_c", "train", "nhanes_drr"),
    ("NH_00162_c", "train", "nhanes_drr"),          # this one agrees by luck: same side, still a duplicate
    # a corpus that is present once and split by patient: clean, and must stay clean
    ("BUU_FULL_buu_0001-F-037Y1", "train", "buu_full"),
    ("BUU_FULL_buu_0002-F-030Y1", "val", "buu_full"),
]


def build_fixture(root: Path):
    root.mkdir(parents=True, exist_ok=True)

    # 1. the bank
    bank = root / "synth_bank"
    bank.mkdir()
    case, split, source = [], [], []
    for c, s, src in BANK_ROWS:
        case += [c, c]                                  # two crops of the same film
        split += [s, s]
        source += [src, src]
    np.savez_compressed(bank / "rung_1.npz", X=np.zeros((len(case), 1), np.uint8), y=np.zeros(len(case), np.int64),
                        case=np.array(case), split=np.array(split), source=np.array(source))
    json.dump(dict(classes=[], rungs=[1], val_cases=sorted({c for c, s, _ in BANK_ROWS if s == "val"})),
              open(bank / "meta.json", "w"))

    # 2. a real-frame dataset: specimen 17-1882 is the held-out test specimen and also has a frame in train
    rx = root / "synth_rx"
    (rx / "meta").mkdir(parents=True)
    for s in ("train", "val", "test"):
        (rx / "images" / s).mkdir(parents=True)
    frames = [("17-1882_000", "test"), ("17-1882_001", "test"), ("17-1882_099", "train"),
              ("18-1109_000", "train"), ("18-2799_000", "val")]
    rx_paths = []
    for stem, s in frames:
        json.dump(dict(stem=stem, case=stem.split("_")[0], split=s), open(rx / "meta" / f"{stem}.json", "w"))
        (rx / "images" / s / f"{stem}.png").write_bytes(b"")
        rx_paths.append(str(rx / "images" / s / f"{stem}.png"))
    json.dump(dict(train=["18-1109"], val=["18-2799"], test=["17-1882"]), open(rx / "splits.json", "w"))

    # 3. a render directory: two poses of ONE CT, split apart; and the CTSpinoPelvic1K naming gap -- the same CT
    #    under the release id (ctsp_0002) and under its original COLONOG name, which no rule can join
    drr = root / "synth_drr"
    (drr / "ann").mkdir(parents=True)
    for stem, s in (("ctsp_0001_ap_p0", "train"), ("ctsp_0001_lat_p3", "val"),
                    ("ctsp_0002_ap_p0", "train"), ("CTSP_COLONOG_1", "val")):
        json.dump(dict(case=stem, split=s), open(drr / "ann" / f"{stem}.json", "w"))
    canonical = [(str(drr / "ann" / f"{stem}.json"), "ct_0002") for stem in ("ctsp_0002_ap_p0", "CTSP_COLONOG_1")]
    canonical += [(f"{bank / 'rung_1.npz'}#{c}", "blank_frame") for c, _s, _src in BANK_ROWS]
    canonical += [(str(drr / "ann" / f"{s}.json"), "blank_frame") for s in ("ctsp_0001_ap_p0", "ctsp_0002_ap_p0")]

    # 4. a styled corpus rendered under the pose of specimen 17-1882, which is the real test specimen above
    st = root / "styled" / "cios_fusion__elekta_xvi" / "images" / "train"
    st.mkdir(parents=True)
    styled_paths = []
    for stem in ("s0224_00_17-1882-015_elekta_xvi_0", "s0225_01_18-1109-098_elekta_xvi_0"):
        (st / f"{stem}.jpg").write_bytes(b"")
        styled_paths.append(str(st / f"{stem}.jpg"))

    # a DEGENERATE identity token, the way a blank or near-blank frame really behaves: one "canonical id" claiming
    # that a film from every corpus is the same file. Merging on it would fuse thirteen patients into one and
    # manufacture leakage, so the guard must refuse it and say so.
    canonical += [(p, "blank_frame") for p in rx_paths + styled_paths]
    with open(root / "canonical.jsonl", "w") as fh:
        for p, cid in canonical:
            fh.write(json.dumps(dict(path=p.replace("\\", "/"), canonical_id=cid)) + "\n")

    # 5. a file no rule can key: it must FAIL the run, not become its own patient
    odd = root / "odd" / "images" / "train"
    odd.mkdir(parents=True)
    (odd / "scan_from_the_other_hospital_42.png").write_bytes(b"")

    cfg = dict(
        collections={
            "synth_bank": dict(kind="bank", path=str(bank)),
            "synth_rx": dict(kind="realxray", path=str(rx), corpus="deepfluoro", device="cios_fusion"),
            "synth_drr": dict(kind="drr", path=str(drr)),
            "styled": dict(kind="styled", path=str(root / "styled")),
            "odd": dict(kind="yolo", path=str(root / "odd")),
        },
        lineage={
            # fine-tuned on the bank, on the real train split and on the styled corpus; scored on the real test
            # split -- which is where the stray 17-1882_099 training frame becomes a leak
            "synth_model": dict(train=["synth_bank#train", "synth_rx#train,val", "styled/*#train"],
                                eval=["synth_rx#test"], evidence="synthetic fixture in tools/test_leak_check.py"),
        },
    )
    # the device map in the tool points cios_fusion at rx_deepfluoro; the fixture's real corpus is synth_rx, and
    # check (6) finds it through the item device field, so nothing here depends on that map
    json.dump(cfg, open(root / "config.json", "w"), indent=1)
    return root / "config.json"


def run_tool(args, expect=None):
    p = subprocess.run([sys.executable, str(TOOL)] + args, capture_output=True, text=True)
    print(p.stdout, end="")
    if p.stderr.strip():
        print(p.stderr, file=sys.stderr)
    if expect is not None:
        assert p.returncode == expect, f"exit {p.returncode}, expected {expect}"
    return p


def ok(cond, msg):
    print(("  ok   " if cond else "  FAIL ") + msg)
    assert cond, msg


def test_nhanes_double_inclusion_is_caught():
    tmp = Path(tempfile.mkdtemp(prefix="leakcheck_"))
    cfg = build_fixture(tmp)
    out = tmp / "out"
    p = run_tool(["check", "--config", str(cfg), "--only-config", "--out", str(out)])
    rep = json.load(open(out / "leak_report.json"))
    C = rep["checks"]

    print("\nassertions")
    # the defect is invisible per source -- this is the whole reason the tool exists
    ok("synth_bank" not in C["1_within_collection_builder_key"]["by_collection"],
       "check (1), the per-source view, reports the bank as clean (the defect hides exactly here)")

    # and visible on the cross-source key
    b2 = C["2_within_collection_merged_key"]["by_collection"].get("synth_bank")
    keys2 = {r["key"] for r in (b2 or {}).get("shown", [])}
    ok(b2 is not None and keys2 == {"nhanes:00160", "nhanes:00161"},
       f"check (2) names both split-crossing patients: {sorted(keys2)}")
    ok(all(set(r["sources"]) == {"nhanes", "nhanes_drr"} for r in b2["shown"]),
       "check (2) shows both source names on the crossing keys")
    ok(not any(r["key"].startswith("buu:") for r in b2["shown"]),
       "the cleanly split BUU corpus is not flagged")
    ok(C["1_within_collection_builder_key"]["n"] == 2 and C["2_within_collection_merged_key"]["n"] == 4,
       f"the two views differ by exactly the doubled corpus: {C['1_within_collection_builder_key']['n']} keys on the "
       f"builder's key, {C['2_within_collection_merged_key']['n']} on the cross-source key")

    # the structural duplicate-source test, with no corpus name hard-coded
    d = C["3_source_entered_twice"]["shown"]
    ok(len(d) == 1 and {d[0]["source_a"], d[0]["source_b"]} == {"nhanes", "nhanes_drr"},
       f"check (3) finds the doubled source structurally: {d[0]['source_a']} == {d[0]['source_b']}")
    ok(d[0]["n_shared"] == 3 and d[0]["containment"] == 1.0,
       f"all {d[0]['n_shared']} patients of the smaller copy are in the other ({d[0]['containment']:.0%})")
    ok(d[0]["n_split_disagreement"] == 2,
       f"and {d[0]['n_split_disagreement']} of them were given different splits by the two copies")

    # (4) the model's evaluation specimen is in its training set
    m = next(r for r in C["4_eval_vs_training"]["models"] if r["model"] == "synth_model")
    ok(m["n_eval_keys_in_train"] == 1 and m["examples"] == ["deepfluoro:17-1882"],
       f"check (4): {m['n_eval_keys_in_train']} evaluation patient(s) inside training -- {m['examples']}")

    # (5) two poses of one CT on opposite sides
    r5 = C["5_render_pose_duplicates"]["shown"]
    ok(len(r5) == 1 and r5[0]["key"] == "ctsp:0001",
       "check (5) catches ctsp_0001_ap_p0 (train) vs ctsp_0001_lat_p3 (val), and only that")
    ok(not any(r["key"].startswith("nhanes:") for r in r5),
       "and does not re-report the two NHANES films as a pose duplicate: they are check (2)'s")

    # (6) a styled frame rendered under the pose of the real test specimen
    r6 = C["6_styled_vs_real_device"]["shown"]
    ok(r6 and r6[0]["n_donor_in_real_heldout"] == 1 and
       any(h["real_collection"] == "synth_rx" and h["split"] == "test" for h in r6[0]["donor_in_real"]),
       "check (6) catches the styled frame whose pose donor is the real test specimen")

    # the loud failure on an unkeyable name
    ok(rep["keying"]["n_unkeyed"] == 1 and "scan_from_the_other_hospital_42" in rep["keying"]["unkeyed"][0]["item"],
       "an unkeyable file is reported, not silently treated as its own patient")
    ok(rep["verdict"]["pass"] is False and p.returncode == 1,
       f"the run fails with exit {p.returncode} (1 = leakage found)")

    # the same fixture minus every leak, with only the unkeyable collection: exit 2, config incomplete
    p2 = run_tool(["check", "--config", str(cfg), "--only-config", "--only", "odd", "--out", str(tmp / "out2")], expect=2)
    ok(p2.returncode == 2, "a run whose only defect is an unkeyable item exits 2 (incomplete table), not 0")
    p3 = run_tool(["check", "--config", str(cfg), "--only-config", "--only", "odd", "--allow-unkeyed",
                   "--out", str(tmp / "out3")], expect=0)
    ok(p3.returncode == 0, "--allow-unkeyed is the only way that item passes, and it has to be asked for")

    # a clean collection passes
    p4 = run_tool(["check", "--config", str(cfg), "--only-config", "--only", "synth_drr", "--out", str(tmp / "out4")])
    ok(p4.returncode == 1, "the render directory alone still fails on its own pose duplicate (nothing is masked)")

    ok((out / "DATA_LEAKAGE_REPORT.md").exists() and (out / "leak_report.json").exists(),
       "both outputs are written")

    # the declared-but-unresolvable naming gap is reported, and NOT quietly assumed to be fine
    gaps = [g for g in C["alias_gaps"]["shown"] if g["collection"] == "synth_drr"]
    ok(gaps and gaps[0]["both_spellings_straddle_a_split"],
       "the CTSpinoPelvic1K naming gap (ctsp_0002 vs CTSP_COLONOG_1) is reported with both spellings straddling a split")
    ok(not any(r["key"] in ("ctsp:0002", "ctsp:COLONOG_1")
               for r in C["2_within_collection_merged_key"]["by_collection"]["synth_drr"]["shown"]),
       "and the two names are NOT merged on a guess -- no rule relates them")

    # ... until the content layer says they are one file
    print("\nwith the content layer's canonical.jsonl")
    p6 = run_tool(["check", "--config", str(cfg), "--only-config", "--canonical", str(tmp / "canonical.jsonl"),
                   "--out", str(tmp / "out6")])
    rep6 = json.load(open(tmp / "out6" / "leak_report.json"))
    C6 = rep6["checks"]
    ok(any(r["key"] == "ctsp:0002" for r in C6["2_within_collection_merged_key"]["by_collection"]["synth_drr"]["shown"]),
       "the canonical id joins ctsp_0002_ap_p0 (train) to CTSP_COLONOG_1 (val) and check (2) flags it")
    ok(rep6["keying"]["n_degenerate_groups"] == 1,
       "a canonical id claiming a film from every corpus is one file is refused and reported, not merged")
    ok(not any(r["key"] == "buu:0001" for r in C6["2_within_collection_merged_key"]["by_collection"]["synth_bank"]["shown"]),
       "so the clean BUU patients are still clean -- a degenerate token cannot manufacture leakage")

    print(f"\nfixture kept at {tmp}")
    return tmp


def test_cross_source_keys():
    """The three spellings of one NHANES patient, and the aliased DeepFluoro releases, resolve to one key."""
    print("\nkey resolution")
    p = run_tool(["keys",
                  "--id", "nhanes_00160", "--id", "NHANES_nhanes_cervical_00160", "--id", "NHANES_nhanes_lumbar_00160",
                  "--id", "NH_00160_c", "--id", "C00160_cervical_masks_4.pkl",
                  "--id", "17-1882_000", "--id", "03_cadaver_17-1882", "--id", "18-1109",
                  "--id", "BUU_FULL_buu_0001-F-037Y1", "--id", "buu_0001",
                  "--id", "ctsp_0001_ap_p0", "--id", "ctsp_0001_lat_p3",
                  "--id", "s0224_00_17-1882-015_elekta_xvi_0", "--id", "case100_AP_0003", "--id", "case100"], expect=0)
    lines = [l for l in p.stdout.splitlines() if "->" in l]
    got = {l.split("->")[0].strip(): l.split("->")[1].split()[0] for l in lines}
    ok(len({got["nhanes_00160"], got["NHANES_nhanes_cervical_00160"], got["NHANES_nhanes_lumbar_00160"],
            got["NH_00160_c"], got["C00160_cervical_masks_4.pkl"]}) == 1,
       f"five spellings of one NHANES patient -> {got['NH_00160_c']}")
    ok(got["17-1882_000"] == got["03_cadaver_17-1882"] == "deepfluoro:17-1882",
       "the DeepFluoro h5 frame and the JHU vendor DICOM directory -> one specimen key")
    ok(got["BUU_FULL_buu_0001-F-037Y1"] == got["buu_0001"] == "buu:0001", "BUU case and patient id -> one key")
    ok(got["ctsp_0001_ap_p0"] == got["ctsp_0001_lat_p3"] == "ctsp:0001", "two poses of one CT -> one key")
    ok(got["case100_AP_0003"] == got["case100"] == "carmlspine:case100", "a C-ArmLSpine frame -> its case")
    ok("17-1882" in p.stdout and "totalseg:s0224" in p.stdout,
       "a styled render keys to its CT and records its pose donor")
    p5 = run_tool(["keys", "--id", "scan_from_the_other_hospital_42"], expect=2)
    ok(p5.returncode == 2, "an unknown name is UNKEYED and exits 2, never a silent new patient")


# Real names, copied from grid listings on 2026-09-22 (`ls` only: ~/films_drr/ann, ~/nhanes_drr/ann, ~/verse_drr/ann,
# ~/ctsp_drr/ann, ~/physics_drr/ann, ~/spine-detector/data/yolo_v{3,4z,6f}/images, realxray/*/images, devcorpus/styled,
# ~/model_night/anchor_none_v2_17-1882/images). The rules were checked against 4,295 render names and 35,668 detector
# stems with zero unkeyed; these lock the forms that were actually seen.
REAL_NAMES = [
    ("BUU_FULL_buu_0001-F-037Y1", "buu:0001"), ("buu_0003-F-013Y0", "buu:0003"),
    ("buu_0003-F-013Y0__zoom0", "buu:0003"),                      # a derived view is the same film
    ("CSXA_csxa_0001035", "csxa:0001035"), ("csxa_0001035__zoom1", "csxa:0001035"),
    ("NHANES_nhanes_cervical_00160", "nhanes:00160"), ("nhanes_cervical_00161__zoom1", "nhanes:00161"),
    ("NH_00160_c", "nhanes:00160"), ("NH_00160_l", "nhanes:00160"),
    ("MEND_2662-F-044Y1", "mendeley:2662"), ("mendeley_Screenshot-2022-07-31-045959", "mendeley:Screenshot-2022-07-31-045959"),
    ("AASCE_sunhl-1th-02-Jan-2017-162_A_AP", "aasce:sunhl-1th-02-Jan-2017-162_A"),
    ("AASCE_sunhl-1th-20-Jul-2016-coronal1", "aasce:sunhl-1th-20-Jul-2016-coronal1"),
    ("aasce_sunhl-1th-10-Jan-2017-239_C_AP", "aasce:sunhl-1th-10-Jan-2017-239_C"),
    ("CTSP_COLONOG_1", "ctsp:COLONOG_1"), ("ctsp_0001_ap_p1", "ctsp:0001"),
    ("TS_s0001", "totalseg:s0001"), ("gl003", "verse:gl003"), ("glgl003", "verse:glgl003"),
    ("verse004", "verse:verse004"), ("sub-verse004", "verse:verse004"),
    ("18-1109_000", "deepfluoro:18-1109"), ("03_cadaver_17-1882", "deepfluoro:17-1882"),
    ("case100_AP", "carmlspine:case100"), ("A053_0020", "cobra:A053"), ("phantom_p01_065kv", "geneva:phantom_p01"),
    ("s0224_00_17-1882-015_cios_fusion_0", "totalseg:s0224"), ("s0467_00_18-1109-021", "totalseg:s0467"),
    ("fluoro_FLUO-000001", "fluorocap:FLUO-000001"),
    ("fluoro_video_-wRtGXiWymY_00032__r3", "fluorocap_video:-wRtGXiWymY"),
]
HINTS = {"A053_0020": "cobra", "phantom_p01_065kv": "geneva"}


def test_real_name_forms():
    """Every naming form seen on the grid resolves, and resolves to the right patient."""
    print("\nreal names from the grid")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import leak_check as L                                       # noqa: PLC0415
    bad = 0
    for name, want in REAL_NAMES:
        k, why = L.key_for(name, HINTS.get(name))
        got = f"{k['corpus']}:{k['patient']}" if k else f"UNKEYED ({why})"
        bad += got != want
        print(f"  {'ok  ' if got == want else 'FAIL'} {name:<44} -> {got}" + ("" if got == want else f"  want {want}"))
    ok(bad == 0, f"{len(REAL_NAMES)} real names, {bad} wrong")
    # the doubled VerSe prefix is NOT silently merged, and it IS declared as a gap
    ok(any("glgl" in g["b"] for g in L.ALIAS_GAPS),
       "the gl003 / glgl003 pair in ~/verse_drr is declared as an unresolved alias, not merged on a guess")


if __name__ == "__main__":
    test_cross_source_keys()
    test_real_name_forms()
    test_nhanes_double_inclusion_is_caught()
    print("\nALL ASSERTIONS PASSED")
