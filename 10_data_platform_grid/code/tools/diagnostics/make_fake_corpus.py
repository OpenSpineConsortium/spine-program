#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/diagnostics/make_fake_corpus.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Build a tiny synthetic corpus so `slurm/data_accounting.sh` can be RUN, not just read.

WHY THIS EXISTS.  The data-accounting chain is five tools deep and every stage consumes the previous
stage's files by path.  A wrong flag, a missing subcommand or a stage handed the wrong path does not
announce itself: argparse exits 2, the runner keeps going, and the next stage reads a file that was
never written and reports a clean sheet over nothing.  That is the exact failure shape the whole chain
exists to prevent, so the runner may not be trusted until it has been run end to end against data whose
answer is known in advance.  The real roots are hundreds of GB on the grid and cannot serve that
purpose; this tree can, in under a second, on a laptop.

WHAT IT PLANTS.  The NHANES II defect in miniature, because that is the defect the chain was written
for (docs/NHANES_DOUBLE_INCLUSION_2026-09-22.md).  One person appears under two spellings in two render
directories --

    <home>/films_drr/img/NHANES_nhanes_cervical_00160.png     keys to  nhanes:00160
    <home>/nhanes_drr/img/NH_00160_c.png                      keys to  nhanes:00160

-- the two files are byte-identical, and the crop bank built from them puts the first spelling in
`train` and the second in `val`.  That is a train/val crossing of one patient wearing two names.

The planted leak is designed to be INVISIBLE to the naive check and visible only to the real one:

  * `leak_check` check (1) -- the builder's-eye key, patient qualified by SOURCE name -- stays clean,
    because each source was split cleanly on its own.  That is precisely what was true on disk while
    48 of 54 validation patients had their twin in training.
  * check (2), the cross-source key after alias merging, fires.  So does check (3) (two source names
    whose patient sets coincide) and check (4) (the model's eval keys inside its train keys).

So a run that ends `LEAK_CHECK PASS` on this tree has NOT passed: it has failed to look.

WHAT IT ALSO PLANTS, AND WHY IT IS NOT A LEAK.  Two "CT releases" share one byte-identical volume under
two root names and two file names.  That is an ALIAS -- one acquisition, two packagings, the DeepFluoro
situation -- and it must show up in `canonical.jsonl` as one canonical id spanning two roots while
changing nothing about the leak verdict.  A chain that reports it as leakage is as wrong as one that
misses the NHANES crossing.

--clean builds the same tree with the overlap removed (the second render directory holds five people
nobody else holds, and no pixels are shared with the first).  Running the chain twice, once each way,
is what proves the runner's exit code means something: 0 clean, non-zero leaking.  A runner that exits
0 on both is a runner that is not reading the report.

USAGE

    python tools/diagnostics/make_fake_corpus.py --out <dir>            # with the planted leak
    python tools/diagnostics/make_fake_corpus.py --out <dir> --clean    # without it

It then prints the exact environment and command that drive `slurm/data_accounting.sh` over the tree.
Nothing here touches the grid, the repo, or any real root.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import numpy as np

# One person in two spellings.  The FIRST three are the planted overlap: they exist in both render
# directories, byte for byte, under names no string comparison relates.
OVERLAP = ["00160", "00161", "00162"]
FILMS_ONLY = ["00163", "00164"]
NHANES_ONLY = ["00170", "00171"]
NHANES_ONLY_CLEAN = ["00170", "00171", "00172", "00173", "00174"]

# DeepFluoro specimen ids, used as the real-frame eval corpus: six frames over three specimens, so a
# frame-level split would be a patient-level leak and the chain has something real to key.
SPECIMENS = {"17-1882": "train", "17-1905": "train", "18-0725": "test"}

BUU = ["00011", "00012", "00013", "00014", "00015", "00016"]


def _img(seed: int, w: int = 96, h: int = 128) -> np.ndarray:
    """A picture with structure, not noise: a flat frame is `degenerate` to the ledger and is deliberately
    excluded from every duplicate count, so a corpus of flat frames would prove nothing."""
    r = np.random.default_rng(seed)
    y, x = np.mgrid[0:h, 0:w]
    base = (120 + 60 * np.sin(x / 7.0 + seed) + 40 * np.cos(y / 11.0 - seed)).astype(np.float64)
    return np.clip(base + r.normal(0, 6, (h, w)), 0, 255).astype(np.uint8)


def write_png(path: Path, arr: np.ndarray) -> None:
    from PIL import Image
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr, mode="L").save(path)


def copy_bytes(src: Path, dst: Path) -> None:
    """A BYTE copy, not a re-save.  A re-save through PIL would give a different file with the same
    picture, which is a weaker claim than the one being tested here."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def write_nii(path: Path, seed: int) -> None:
    import nibabel as nib
    r = np.random.default_rng(seed)
    vol = (r.normal(40, 15, (16, 16, 12)) + np.arange(12)[None, None, :] * 5).astype(np.float32)
    path.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nib.Nifti1Image(vol, np.eye(4)), str(path))


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1), encoding="utf-8")


def build(out: Path, clean: bool) -> dict:
    home = out / "home"
    data = out / "data"
    films = home / "films_drr"
    nh = home / "nhanes_drr"
    bank = home / "fake_fov96_ctx"
    yolo = home / "spine-detector" / "data" / "yolo_fake"
    rx = data / "realxray" / "deepfluoro"

    films_cases, nh_cases, bank_rows = [], [], []

    # ---- render directory 1: films_drr.  Stems carry the corpus and the view: NHANES_nhanes_cervical_00160
    for i, pid in enumerate(OVERLAP + FILMS_ONLY):
        case = f"NHANES_nhanes_cervical_{pid}"
        write_png(films / "img" / f"{case}.png", _img(100 + i))
        write_json(films / "ann" / f"{case}.json",
                   dict(case=case, source="nhanes", patient_id=f"nhanes_{pid}", split="train",
                        source_file=f"raw/nhanes_full/C{pid}.tiff"))
        films_cases.append(case)
        bank_rows.append((case, "train", "nhanes"))

    # ---- render directory 2: nhanes_drr.  Stems carry NOTHING that relates them to the first directory.
    # In the leaking build the first three ARE the first three people of films_drr, byte for byte.
    second = OVERLAP + NHANES_ONLY if not clean else NHANES_ONLY_CLEAN
    for i, pid in enumerate(second):
        case = f"NH_{pid}_c"
        dst = nh / "img" / f"{case}.png"
        if (not clean) and pid in OVERLAP:
            copy_bytes(films / "img" / f"NHANES_nhanes_cervical_{pid}.png", dst)
        else:
            write_png(dst, _img(500 + i))
        write_json(nh / "ann" / f"{case}.json",
                   dict(case=case, split="val", source_file=f"raw/nhanes_full/C{pid}.tiff"))
        nh_cases.append(case)
        bank_rows.append((case, "val", "nhanes_drr"))

    # ---- the crop bank: this is where the crossing is actually consumed.  Two rungs, because a case
    # only appears in a rung it can fill and reading one rung is how a bank gets half-inventoried.
    bank.mkdir(parents=True, exist_ok=True)
    cases = np.array([c for c, _, _ in bank_rows])
    splits = np.array([s for _, s, _ in bank_rows])
    sources = np.array([s for _, _, s in bank_rows])
    np.savez(bank / "rung_0.npz", case=cases, split=splits, source=sources,
             X=np.zeros((len(cases), 4, 4), np.uint8))
    half = len(cases) // 2
    np.savez(bank / "rung_1.npz", case=cases[:half], split=splits[:half], source=sources[:half],
             X=np.zeros((half, 4, 4), np.uint8))
    write_json(bank / "meta.json",
               dict(classes=["L1", "L2", "L3"], rungs=2, size=96, tgt_px=96, mode="ctx",
                    val_cases=[c for c, s, _ in bank_rows if s == "val"],
                    merged_from=[str(films), str(nh)]))

    # ---- a detector corpus, keyed on a different release (BUU): it must come back CLEAN, so that a
    # report in which everything fails proves as little as one in which nothing does.
    for i, pid in enumerate(BUU):
        split = "train" if i < 4 else "val"
        write_png(yolo / "images" / split / f"buu_{pid}_AP.png", _img(900 + i))
    write_json(yolo / "data.yaml", {})          # placeholder; data_lineage parses the real YAML, not this
    (yolo / "data.yaml").write_text(
        "path: .\ntrain: images/train\nval: images/val\nnames: [vertebra]\n", encoding="utf-8")

    # ---- real frames: six frames over three specimens, split by SPECIMEN
    for si, (spec, split) in enumerate(SPECIMENS.items()):
        for k in range(2):
            stem = f"{spec}_{k:03d}"
            # NOT hash(stem): Python salts str hashing per process, so the tree was a different tree
            # on every build and two runs of the proof could not be compared byte for byte.
            write_png(rx / "images" / split / f"{stem}.png", _img(700 + 10 * si + k))
            write_json(rx / "meta" / f"{stem}.json", dict(stem=stem, case=spec, split=split,
                                                          device="cios_fusion"))
    write_json(rx / "splits.json", {s: [c for c, v in SPECIMENS.items() if v == s]
                                    for s in ("train", "val", "test")})

    # ---- two CT "releases" sharing one volume, byte for byte, under two names.  An ALIAS, not a leak.
    # The names match NO patient rule in any of the five tools, on purpose: this is also the third
    # thing the tree demonstrates -- a root that is wholly anonymous to the keying layer, which joins
    # to nobody and takes part in no split check, and which the ledger's per-root null column exists
    # to put on the face of the accounting rather than leave for somebody to find in the JSONL.
    # (An earlier draft called the copy `case0001.nii.gz`; leak_check's C-ArmLSpine rule `case(\d+)`
    # fired on it and filed a CT under the fluoroscopy corpus.  Real, and a different demonstration.)
    write_nii(data / "ct_release" / "0001_ct.nii.gz", 11)
    write_nii(data / "ct_release" / "0002_ct.nii.gz", 12)
    copy_bytes(data / "ct_release" / "0001_ct.nii.gz", data / "ct_vendor" / "vendorcopy_0001.nii.gz")

    # ---- the model registry data_lineage reads.  `bank` is the bank's DIRECTORY NAME on purpose:
    # leak_check's --lineage-graph join turns models[].bank straight into "<bank>#train", and a full
    # path there resolves to no collection and is reported as an unresolved ref.
    reg = home / "model_registry" / "registry.jsonl"
    reg.parent.mkdir(parents=True, exist_ok=True)
    reg.write_text(json.dumps(dict(name="fake_level_encoder", sha="0" * 40, stage="encoder",
                                   bank="fake_fov96_ctx", store_path=str(home / "models" / "enc.pt"),
                                   ts="2026-09-22T00:00:00", git="synthetic")) + "\n", encoding="utf-8")

    # ---- the collection + lineage table leak_check reads under --only-config.  Written here because
    # this file is the only thing that knows where the tree landed.
    cfg = dict(
        collections={
            "fake_films_drr": dict(kind="drr", path=str(films)),
            "fake_nhanes_drr": dict(kind="drr", path=str(nh)),
            "fake_fov96_ctx": dict(kind="bank", path=str(bank)),
            "yolo_fake": dict(kind="yolo", path=str(yolo)),
            "rx_fake_deepfluoro": dict(kind="realxray", path=str(rx), corpus="deepfluoro",
                                       device="cios_fusion"),
        },
        lineage={
            "fake_level_encoder": dict(train=["fake_fov96_ctx#train"], eval=["fake_fov96_ctx#val"],
                                       evidence="tools/diagnostics/make_fake_corpus.py (synthetic)"),
            "fake_detector": dict(train=["yolo_fake#train"], eval=["rx_fake_deepfluoro#test"],
                                  evidence="tools/diagnostics/make_fake_corpus.py (synthetic)"),
        })
    write_json(out / "leak_config.json", cfg)

    return dict(home=home, data=data, films=films, nh=nh, bank=bank, yolo=yolo, rx=rx,
                films_cases=films_cases, nh_cases=nh_cases,
                overlap=[] if clean else OVERLAP, clean=clean)


def recipe(out: Path, info: dict, repo: Path, acct: Path) -> str:
    """The command that drives the real runner over this tree.  Printed rather than executed: the point
    of the exercise is that the RUNNER runs it, not that this file reproduces the runner's command lines
    (two copies of a command line is how the runner got out of step with the tools in the first place)."""
    # POSIX spellings throughout: the runner is a bash script, and a Windows backslash inside a
    # double-quoted *_ARGS string is an escape, not a separator.  Python opens either spelling.
    home, data = info["home"].as_posix(), info["data"].as_posix()
    extra = " ".join(
        f"--extra-root '{n}|{stage}|{Path(p).as_posix()}'" for n, stage, p in (
            ("fake_films_drr", "render", f"{home}/films_drr"),
            ("fake_nhanes_drr", "render", f"{home}/nhanes_drr"),
            ("fake_ctx", "crop", f"{home}/fake_fov96_ctx"),
            ("fake_yolo", "detector-set", f"{home}/spine-detector/data/yolo_fake"),
            ("fake_realxray", "eval", f"{data}/realxray/deepfluoro"),
            ("fake_ct_release", "source", f"{data}/ct_release"),
            ("fake_ct_vendor", "source", f"{data}/ct_vendor"),
        ))
    names = "fake_films_drr,fake_nhanes_drr,fake_ctx,fake_yolo,fake_realxray,fake_ct_release,fake_ct_vendor"
    return "\n".join([
        "ALLOW_LOCAL=1 STAGE=all NSHARD=2 MIN_LEDGER_ROWS=20 \\",
        f"  REPO='{repo.as_posix()}' OUT='{acct.as_posix()}' PY=python \\",
        f'  LEDGER_ARGS="--roots {names} {extra}" \\',
        f'  LINEAGE_ARGS="--home {home} --data {data} --sections drr,crops,realxray,models" \\',
        f'  LEAK_ARGS="--only-config --config {(out / "leak_config.json").as_posix()}" \\',
        "  bash slurm/data_accounting.sh",
    ])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", required=True, help="directory to build the tree in (created; --force to reuse)")
    ap.add_argument("--clean", action="store_true", help="build the same tree with NO planted leak")
    ap.add_argument("--force", action="store_true", help="delete --out first")
    ap.add_argument("--acct", default=None, help="where the chain should write (default <out>/accounting)")
    a = ap.parse_args()
    out = Path(a.out).resolve()
    if out.exists():
        if not a.force:
            print(f"{out} exists; --force to rebuild it", file=sys.stderr)
            return 2
        shutil.rmtree(out)
    out.mkdir(parents=True)
    info = build(out, a.clean)
    repo = Path(__file__).resolve().parents[2]
    acct = Path(a.acct).resolve() if a.acct else out / "accounting"

    n_files = sum(1 for _ in out.rglob("*") if _.is_file())
    print(f"built {'CLEAN' if a.clean else 'LEAKING'} synthetic corpus at {out}  ({n_files} files)")
    print(f"  {info['films']}  {len(info['films_cases'])} renders, split train")
    print(f"  {info['nh']}  {len(info['nh_cases'])} renders, split val")
    if info["overlap"]:
        print(f"  PLANTED LEAK: people {', '.join(info['overlap'])} are in BOTH, byte-identical, one in")
        print(f"                train as NHANES_nhanes_cervical_<id> and one in val as NH_<id>_c.")
        print(f"                Expect leak_check check (2)/(3)/(4) to fire and the chain to exit non-zero.")
    else:
        print("  no overlap: the two render directories hold disjoint people and share no pixels.")
        print("                Expect LEAK_CHECK PASS and the chain to exit 0.")
    print(f"  alias (not a leak, in both builds): {info['data'] / 'ct_release' / '0001_ct.nii.gz'}")
    print(f"                                  and {info['data'] / 'ct_vendor' / 'vendorcopy_0001.nii.gz'} are")
    print("                                  one volume, and neither carries a patient key: expect both CT")
    print("                                  roots in the ledger's roots-wholly-without-a-patient-key line.")
    print()
    print("run the chain over it with:")
    print()
    print(recipe(out, info, repo, acct))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
