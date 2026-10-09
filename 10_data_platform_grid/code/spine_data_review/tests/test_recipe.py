#!/usr/bin/env python3
"""Adversarial checks of sdr.recipe and recipe/prepare_splits.py on tests/fixtures/recipe/.

Run from spine_data_review/ inside WSL:
    ~/sdr_venv/bin/python tests/make_recipe_fixture.py
    ~/sdr_venv/bin/python tests/test_recipe.py

What is checked, each against a value computed by hand in this file, not by the module:
  T1  the recipe reads analysis/quality.json in the shape sdr.quality writes (scalar total, bool fit)
  T2  the SAP A7 order on the fixture (tier, quality desc, id)
  T3  byte-identical output across two runs into two directories
  T4  route -> action/method table of recipe/README.md, per fixture record
  T5  file list: checksums[] + enrichment merged, unique by URL, sorted; verification = strongest check
  T6  every generated script parses (bash -n); the offline ones behave under DRY_RUN=1 (exit codes,
      no writes, no network); download_all.sh --dry-run --skip-manual counts
  T7  prepare_splits: hand-computed partition sizes for ten singleton subjects and grouped pairs
No network is used here; the live listing checks are run separately (see the review report).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FX = ROOT / "tests" / "fixtures" / "recipe"
PY = sys.executable
RUN = ROOT / "runs" / "review_recipe"
FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        FAILS.append(msg)


def gen(out: Path, quality: str, extra: list[str] | None = None) -> subprocess.CompletedProcess:
    if out.exists():
        shutil.rmtree(out)
    cmd = [PY, "-m", "sdr.recipe", "--run-dir", str(RUN), "--run-date", "2026-09-19", "--datasets", str(FX / "datasets"),
           "--quality", str(FX / quality), "--enrichment", str(FX / "enrichment"), "--out", str(out)] + (extra or [])
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def manifest(out: Path) -> list[dict]:
    import csv
    with open(out / "manifest.csv", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    os.environ.setdefault("PYTHONPATH", str(ROOT))
    # ---- T1: the real quality shape ------------------------------------------------------------
    r = gen(RUN / "fx_real", "quality_real_shape.json")
    check(r.returncode == 0, f"T1 recipe runs on quality.json in sdr.quality's shape (rc={r.returncode}); "
                             f"stderr tail: {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''}")
    # ---- T2/T3: order and determinism on the {value:} shape (the shape the recipe was written for) --
    r1 = gen(RUN / "fx_a", "quality_value_shape.json")
    r2 = gen(RUN / "fx_b", "quality_value_shape.json")
    check(r1.returncode == 0 and r2.returncode == 0, f"T2 recipe runs on the {{value:}} quality shape (rc={r1.returncode})")
    if r1.returncode != 0:
        print(r1.stderr)
        return finish()
    rows = manifest(RUN / "fx_a")
    got = [x["dataset_id"] for x in rows]
    # Hand-computed SAP A7 order.
    # tier 0 = reachable (open-download/registration) AND fit AND on_grid in (no, unknown), by total desc then id:
    #   fx-zenodo 17, fx-files 14, fx-kaggle 14 (tie -> id: files < kaggle), fx-physionet-open 12
    # tier 1 = other reachable, by total desc then id:
    #   fx-on-grid 18, fx-mendeley-nover 15, fx-gc 13, fx-tcia 11, fx-mendeley 10, fx-dryad 9,
    #   fx-figshare 9, fx-osf 8, fx-generic-fileurl 7, fx-hf-open 6, fx-github 5, fx-generic-browser 4,
    #   fx-hf-gated 3
    # tier 2 = the rest: fx-dua 16, fx-request 2, fx-commercial 1, fx-unavailable 0
    expect = ["fx-zenodo", "fx-files", "fx-kaggle", "fx-physionet-open",
              "fx-on-grid", "fx-mendeley-nover", "fx-gc", "fx-tcia", "fx-mendeley", "fx-dryad", "fx-figshare", "fx-osf",
              "fx-generic-fileurl", "fx-hf-open", "fx-github", "fx-generic-browser", "fx-hf-gated",
              "fx-dua", "fx-request", "fx-commercial", "fx-unavailable"]
    check(got == expect, f"T2 A7 order matches the hand computation\n      got    {got}\n      expect {expect}")
    check([int(x["recipe_order"]) for x in rows] == list(range(1, len(rows) + 1)), "T2 recipe_order is 1..n")
    diff = subprocess.run(["diff", "-r", str(RUN / "fx_a"), str(RUN / "fx_b")], capture_output=True, text=True)
    check(diff.returncode == 0 and not diff.stdout, "T3 two runs are byte-identical (diff -r)")
    # ---- T4: the README table ---------------------------------------------------------------------
    table = {"fx-files": ("download", "files"), "fx-zenodo": ("download", "zenodo-api"), "fx-figshare": ("download", "figshare-api"),
             "fx-dryad": ("download", "dryad-zip"), "fx-osf": ("download", "osf-zip"), "fx-physionet-open": ("download", "physionet-wget"),
             "fx-tcia": ("download", "nbia-rest"), "fx-hf-open": ("download", "hf-cli"), "fx-github": ("download", "git-clone"),
             "fx-generic-fileurl": ("download", "files"), "fx-generic-browser": ("download", "browser"),
             "fx-kaggle": ("registration", "kaggle-cli"), "fx-hf-gated": ("registration", "hf-cli"), "fx-gc": ("registration", "browser"),
             "fx-dua": ("manual-dua", "none"), "fx-request": ("manual-request", "none"), "fx-commercial": ("commercial", "none"),
             "fx-unavailable": ("unavailable", "none"), "fx-on-grid": ("download", "zenodo-api"),
             "fx-mendeley": ("download", "mendeley-api"), "fx-mendeley-nover": ("download", "mendeley-api")}
    by = {x["dataset_id"]: x for x in rows}
    for k, (act, meth) in table.items():
        check((by[k]["recipe_action"], by[k]["download_method"]) == (act, meth),
              f"T4 {k}: ({by[k]['recipe_action']}, {by[k]['download_method']}) == ({act}, {meth})")
    check(by["fx-mendeley"]["verification"] == "sha256 (API, run time)",
          f"T4 fx-mendeley verification is the API sha256 (got {by['fx-mendeley']['verification']})")
    # hand: the Mendeley files API refuses a version-less listing (200 {"error": 400}), so a record whose URL
    # and DOI carry no version must ask /versions first; one that carries v1 must not.
    s_v = (RUN / "fx_a" / "datasets" / "fx-mendeley.sh").read_text(encoding="utf-8")
    s_nv = (RUN / "fx_a" / "datasets" / "fx-mendeley-nover.sh").read_text(encoding="utf-8")
    check("V=1" in s_v and "/versions" not in s_v, "T4 fx-mendeley takes version 1 from its DOI, no /versions call")
    check("/versions" in s_nv and "V=$(curl" in s_nv, "T4 fx-mendeley-nover resolves the latest version at /versions")
    for k, sc in (("fx-mendeley", s_v), ("fx-mendeley-nover", s_nv)):
        check("folder_id=root&version=$V" in sc and "folder_id=root\"" not in sc,
              f"T4 {k} lists files with an explicit &version (a version-less listing answers {{\"error\":400}})")
    # hand: the three methods that verify nothing the review recorded (README.md)
    for k, v in (("fx-kaggle", "none"), ("fx-generic-browser", "none"), ("fx-hf-open", "client (not a published checksum)")):
        check(by[k]["verification"] == v, f"T4 {k} verification={by[k]['verification']} (expected {v})")
    # ---- T5: file list merge and verification -----------------------------------------------------
    s = (RUN / "fx_a" / "datasets" / "fx-files.sh").read_text(encoding="utf-8")
    fetches = [l for l in s.splitlines() if l.startswith("fetch ")]
    check(len(fetches) == 3, f"T5 three unique file URLs after merging checksums[] and enrichment (got {len(fetches)})")
    check([l.split()[1] for l in fetches] == sorted(l.split()[1] for l in fetches), "T5 fetch lines sorted by file name")
    check(by["fx-files"]["verification"] == "sha256" and by["fx-files"]["n_files_known"] == "3",
          f"T5 verification=sha256 (strongest present), n_files_known=3 (got {by['fx-files']['verification']}, {by['fx-files']['n_files_known']})")
    check("'" + "a" * 64 + "'" in fetches[0] or "a" * 64 in fetches[0], "T5 sha256 of vol_001 rendered into its fetch line")
    check(by["fx-generic-fileurl"]["n_files_known"] == "1" and "all.zip" in (RUN / "fx_a" / "datasets" / "fx-generic-fileurl.sh").read_text(),
          "T5 file_url_probed becomes the single fetch")
    # ---- T6: the scripts under bash -----------------------------------------------------------------
    dsdir = RUN / "fx_a" / "datasets"
    for f in sorted(dsdir.glob("*.sh")):
        p = subprocess.run(["bash", "-n", str(f)], capture_output=True, text=True)
        check(p.returncode == 0, f"T6 bash -n {f.name}" + (": " + p.stderr.strip() if p.stderr.strip() else ""))
    p = subprocess.run(["bash", "-n", str(RUN / "fx_a" / "download_all.sh")], capture_output=True, text=True)
    check(p.returncode == 0, "T6 bash -n download_all.sh")
    data_root = RUN / "fx_data_root"
    if data_root.exists():
        shutil.rmtree(data_root)
    env = {**os.environ, "DATA_ROOT": str(data_root), "DRY_RUN": "1", "PATH": os.environ["PATH"]}
    # offline-safe under DRY_RUN=1: files (fetch prints), browser/manual routes (exit 10), hf/kaggle/git (exit 0 or 10)
    expect_rc = {"fx-files": 0, "fx-generic-fileurl": 0, "fx-generic-browser": 10, "fx-gc": 10, "fx-dua": 10, "fx-request": 10,
                 "fx-commercial": 10, "fx-unavailable": 10, "fx-mendeley": 0, "fx-mendeley-nover": 0, "fx-github": 0,
                 "fx-osf": 0, "fx-dryad": 0, "fx-zenodo": 0, "fx-figshare": 0, "fx-physionet-open": 0, "fx-tcia": 0}
    for k, rc in expect_rc.items():
        p = subprocess.run(["bash", str(dsdir / f"{k}.sh")], capture_output=True, text=True, env=env)
        check(p.returncode == rc, f"T6 DRY_RUN=1 {k}.sh exit {p.returncode} (expected {rc})"
              + (f"; stderr: {p.stderr.strip()[:200]}" if p.stderr.strip() else ""))
        if k == "fx-files":
            check(p.stdout.count("would fetch") == 3, "T6 fx-files DRY_RUN lists three fetches")
    check(not data_root.exists(), "T6 DRY_RUN=1 wrote nothing under DATA_ROOT")
    # the header promises "no network call is made" under DRY_RUN=1: every listing call must sit after the gate
    for k, marker in (("fx-zenodo", "curl -fsSL"), ("fx-figshare", "curl -fsSL"), ("fx-mendeley", "curl -fsSL"),
                      ("fx-mendeley-nover", "curl -fsSL"), ("fx-physionet-open", "EFF=$(curl"),
                      ("fx-tcia", "getCollectionValues")):
        s = (dsdir / f"{k}.sh").read_text(encoding="utf-8")
        body = s.split("listed(){")[1]
        check(marker in body, f"T6 {k}.sh lists through `{marker}`")
        gate = 'if [ "$DRY_RUN" = 1 ]' in body.split(marker)[0] or '[ "$DRY_RUN" = 1 ] &&' in body.split(marker)[0]
        check(gate, f"T6 {k}.sh gates network under DRY_RUN (`{marker}` must come after the gate)")
    # a missing record must exit 5 (not a python traceback): the listing is captured before it is parsed
    for k in ("fx-zenodo", "fx-figshare", "fx-mendeley", "fx-mendeley-nover"):
        s = (dsdir / f"{k}.sh").read_text(encoding="utf-8")
        check("J=$(curl -fsSL" in s and "exit 5" in s, f"T6 {k}.sh captures the listing and exits 5 when the record is gone")
    # the direct-fetch and mirror methods must classify the host's HTTP error too (exit 5, .recipe_status=failed),
    # not let curl's 22 out through set -e with nothing written
    for k in ("fx-dryad", "fx-osf", "fx-files", "fx-generic-fileurl"):
        s = (dsdir / f"{k}.sh").read_text(encoding="utf-8")
        check('[ "$rc" = 22 ] && exit 5' in s and "status failed" in s,
              f"T6 {k}.sh turns a host HTTP error into exit 5 with .recipe_status=failed")
    s = (dsdir / "fx-physionet-open.sh").read_text(encoding="utf-8")
    check("EFF=$(curl" in s and "status failed; exit 5" in s, "T6 fx-physionet-open.sh guards the version resolution (exit 5)")
    s = (dsdir / "fx-tcia.sh").read_text(encoding="utf-8")
    check("status failed; exit 5" in s, "T6 fx-tcia.sh writes .recipe_status=failed when NBIA has no such collection")
    # driver: --dry-run --skip-manual over the fixture; manual routes skipped, browser steps counted manual
    p = subprocess.run(["bash", str(RUN / "fx_a" / "download_all.sh"), "--dry-run", "--skip-manual",
                        "--only", "fx-files,fx-generic-browser,fx-dua,fx-request,fx-unavailable,fx-gc"],
                       capture_output=True, text=True, env={**os.environ, "DATA_ROOT": str(data_root)})
    summary = [l for l in p.stdout.splitlines() if l.startswith("== summary")]
    # hand: 21 records; --only keeps 6 ids; --skip-manual drops dua, request, unavailable (3 skipped + 15 not in
    # --only = 18 skipped); fx-files -> ok; fx-generic-browser (download/browser) and fx-gc (registration/browser)
    # -> exit 10 -> manual=2
    check(bool(summary) and "ok=1 manual=2 failed=0 skipped=18" in summary[0], f"T6 driver summary hand check: {summary}")
    check(p.returncode == 0, f"T6 driver exit 0 when nothing failed (rc={p.returncode})")
    check(not data_root.exists(), "T6 driver --dry-run wrote nothing under DATA_ROOT")
    # ---- T7: prepare_splits hand check ------------------------------------------------------------
    sys.path.insert(0, str(ROOT / "recipe"))
    import prepare_splits as ps  # noqa: E402
    subs = [ps.Subject("d", f"s{i}", f"s{i}", [f"s{i}.png"]) for i in range(10)]
    sp = ps.patient_grouped_split(subs)
    # hand: n=10, cuts (7.0, 8.0); groups filled in shuffled order: placed 0..6 -> train (7), placed 7 -> val (1), 8,9 -> test (2)
    sizes = {k: len(v) for k, v in sp.items()}
    check(sizes == {"train": 7, "val": 1, "test": 2}, f"T7 ten singletons split 7/1/2 by the cumulative rule (got {sizes})")
    pairs = [ps.Subject("e", f"p{i}-{v}", f"p{i}", [f"p{i}_{v}.png"]) for i in range(5) for v in ("ap", "lat")]
    sp2 = ps.patient_grouped_split(pairs)
    # hand: n=10 subjects in 5 groups of 2; cuts (7, 8); groups of two fill: placed 0,2,4,6 -> train (8 subjects),
    # placed 8 -> test (2). val is empty: a group is never divided, so val gets nothing here.
    sizes2 = {k: len(v) for k, v in sp2.items()}
    check(sizes2 == {"train": 8, "val": 0, "test": 2}, f"T7 five pairs: 8/0/2, val starves because groups are atomic (got {sizes2})")
    same = ps.patient_grouped_split(subs, seed=ps.SEED)
    check([s.subject_id for s in same["test"]] == [s.subject_id for s in sp["test"]], "T7 same seed, same test set")
    p = subprocess.run([PY, str(ROOT / "recipe" / "prepare_splits.py"), "--manifest", str(RUN / "fx_a" / "manifest.csv"),
                        "--data-root", str(data_root), "--dry-run"], capture_output=True, text=True)
    check(p.returncode == 0 and "nothing to split" in p.stdout, f"T7 prepare_splits --dry-run on an empty DATA_ROOT exits 0 (rc={p.returncode})")
    p = subprocess.run([PY, str(ROOT / "recipe" / "prepare_splits.py"), "--manifest", str(RUN / "no_such_manifest.csv"),
                        "--data-root", str(data_root), "--dry-run"], capture_output=True, text=True)
    check(p.returncode == 2 and "Traceback" not in p.stderr and "python -m sdr.recipe" in p.stderr,
          f"T7 prepare_splits with a missing manifest exits 2 and names the regenerate command (rc={p.returncode}; "
          f"stderr: {p.stderr.strip().splitlines()[-1][:120] if p.stderr.strip() else ''})")
    return finish()


def finish() -> int:
    print(f"\n{len(FAILS)} failure(s)")
    for f in FAILS:
        print("  -", f.splitlines()[0])
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
