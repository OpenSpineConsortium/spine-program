# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/repair_image_links.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Repoint broken image symlinks at wherever the CT volumes actually live now.

WHAT WAS FOUND. Every one of the 802 imagesTr symlinks in Dataset813 is dangling: they name
/data/hf_export/ct/<n>_ct.nii.gz, an absolute path with no such root on this filesystem,
while the volumes sit under ~/data/CTSpinoPelvic1K/ct/. The links were almost certainly made
on a machine where /data was mounted, or with a $HOME that was later stripped.

WHY NOTHING NOTICED. nnU-Net trains from `preprocessed/`, not from `raw/`, and the
preprocessing ran while the links still resolved. So a training run reads no raw image and a
dataset whose every image is missing trains happily to completion. It surfaced only when
something else -- building a merged corpus -- tried to follow them.

That is worth stating plainly: a corpus can be wholly unreadable and every downstream metric
still look healthy, because the metrics are computed from a cache of it. The check that finds
this is following the links, not scoring the model.

    python tools/repair_image_links.py --dir <imagesTr> --search ~/data/CTSpinoPelvic1K/ct --dry
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="imagesTr to repair")
    ap.add_argument("--search", required=True, nargs="+",
                    help="directories that may hold the real volumes")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    d = Path(a.dir)
    pool: dict[str, Path] = {}
    for s in a.search:
        sp = Path(os.path.expanduser(s))
        if not sp.is_dir():
            print(f"  search dir missing: {sp}", file=sys.stderr)
            continue
        for f in sp.rglob("*.nii.gz"):
            pool.setdefault(f.name, f)
    print(f"candidate volumes found: {len(pool)}")

    broken = [p for p in sorted(d.iterdir())
              if p.is_symlink() and not p.exists()]
    print(f"broken links in {d}: {len(broken)}")
    if not broken:
        return 0

    fixed, unresolved = 0, []
    for p in broken:
        want = Path(os.readlink(p)).name           # e.g. 0007_ct.nii.gz
        tgt = pool.get(want)
        if tgt is None:
            unresolved.append((p.name, want))
            continue
        if not a.dry:
            p.unlink()
            os.symlink(tgt.resolve(), p)
        fixed += 1

    print(f"{'would fix' if a.dry else 'fixed'}: {fixed}")
    if unresolved:
        print(f"UNRESOLVED: {len(unresolved)}", file=sys.stderr)
        for n, w in unresolved[:10]:
            print(f"   {n}  wanted {w}", file=sys.stderr)
    if not a.dry:
        still = [p for p in d.iterdir() if p.is_symlink() and not p.exists()]
        print(f"still broken after repair: {len(still)}")
    return 0 if not unresolved else 1


if __name__ == "__main__":
    raise SystemExit(main())
