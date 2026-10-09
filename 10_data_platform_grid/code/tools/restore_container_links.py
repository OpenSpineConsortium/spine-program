# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/restore_container_links.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Put the CT image symlinks back to their container paths, and say why they belong there.

THE MISTAKE THIS UNDOES. imagesTr holds symlinks of the form

    COLONOG_1_0000.nii.gz -> /data/hf_export/ct/0007_ct.nii.gz

which look dangling from the host and are not: /data/hf_export is a BIND MOUNT that
singularity supplies, so the link resolves inside the container where the training actually
reads it. slurm/spine_prep.sh says so in its header, and warns that an earlier version ran a
host-side dangling-link cleanup and "wiped the whole dataset on every resume run". A cleanup
was run anyway, repointing all 802 at host-absolute paths under ~/data/CTSpinoPelvic1K/ct.

WHY THAT IS WORTH REVERTING EVEN THOUGH THE FILES MATCHED. The repair preserved every
basename and 802 links matched 802 files, so it is very probably harmless. "Very probably
harmless" is the wrong standard for the input side of a corpus: a host-absolute path resolves
inside the container only if singularity happens to bind that root, and if it does not, the
failure is a training run that reads nothing and still reports metrics -- which is precisely
how the dead links went unnoticed in the first place. The bind is the documented contract;
restore it and set HF_EXPORT_DIR to wherever the export actually lives.

THE ACTUAL PROBLEM, which the repair was mistakenly solving. Every candidate hf_export root
is absent on this filesystem -- ~/CTSpinoPelvic1K/data/hf_export, the project-local shadow,
and the VerSeFusion one. The surviving copy of the 802 volumes is ~/data/CTSpinoPelvic1K/ct.
So the right move is not to rewrite 802 links but to run with

    HF_EXPORT_DIR=~/data/CTSpinoPelvic1K

so that /data/hf_export/ct/<n>_ct.nii.gz binds to the copy that exists.

    python tools/restore_container_links.py --dir <imagesTr> --prefix /data/hf_export/ct --dry
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--prefix", default="/data/hf_export/ct")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    d = Path(a.dir)
    links = [p for p in sorted(d.iterdir()) if p.is_symlink()]
    print(f"symlinks in {d}: {len(links)}")

    changed, already, skipped = 0, 0, []
    for p in links:
        cur = os.readlink(p)
        if cur.startswith(a.prefix):
            already += 1
            continue
        base = Path(cur).name
        if not base.endswith(".nii.gz"):
            skipped.append((p.name, cur))
            continue
        want = f"{a.prefix}/{base}"
        if not a.dry:
            p.unlink()
            os.symlink(want, p)
        changed += 1

    print(f"already container-relative : {already}")
    print(f"{'would restore' if a.dry else 'restored'}  : {changed}")
    if skipped:
        print(f"SKIPPED (unexpected target): {len(skipped)}", file=sys.stderr)
        for n, c in skipped[:5]:
            print(f"   {n} -> {c}", file=sys.stderr)
    print("\nThese now resolve only inside the container. Run preprocessing with")
    print("    HF_EXPORT_DIR=$HOME/data/CTSpinoPelvic1K")
    print("so /data/hf_export binds to the copy that still exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
