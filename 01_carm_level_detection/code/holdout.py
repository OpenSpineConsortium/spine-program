#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/holdout.py [tracked at 097933a]
"""Load the set of cases a model has SEEN -- trained on or selected on -- and refuse to be vague about it.

WHY THIS EXISTS. Every tool that reports a held-out number takes `--holdout-bank` and reads the case ids out of the
bank's `rung_*.npz` files, so those cases can be excluded from the evaluation. Each tool grew its own copy of that
loop, and every copy shared one defect: when the bank path did not exist, `glob` returned nothing, the seen set came
back EMPTY, and the evaluation ran over every case including the ones the model was fitted on. Nothing raised. The
only symptom was a number that came out better than it should have.

That is this project's characteristic failure -- a value that is wrong but plausible -- and it is worse here than
usual, because the direction of the error is always flattering. A missing bank cannot make a result look worse.
It stopped being hypothetical on 2026-09-20, when five superseded crop banks were deleted to recover quota and
roughly ninety scripts kept naming them. So: naming a bank that is not there is an error, and this raises. A caller
that genuinely wants every case evaluated says so with `allow_trained_on`, which is a different statement and is
visible in the command line.

VALIDATION IS SEEN (2026-09-23). This function used to return only `split == "train"`. But
tools/train_level_classifier.py keeps the epoch with the best accuracy on the bank's `val` split (`best_state`), so
the val cases CHOSE the model: a number scored on them is a selection-set number, not a held-out one. The same
defect let the recall-vs-angle curve score detectors on the subjects they were selected on
(SchwingNet/results/arc/ARC_CHECK.md item 4). So `val` now counts as seen by default. A caller that truly wants the
train split alone -- because the model it is excluding for was demonstrably not selected on that bank's val -- passes
`train_only_because="<why>"`; the reason is printed, and an empty reason is refused.

This excludes by bank CASE ID, for one bank. It does not follow a checkpoint's initialisation chain and does not key
patients across corpora: tools/eval_gate.py (assert_unseen) does both, and it is what every evaluator on a
manuscript path calls.
"""
from __future__ import annotations

import glob
import os
from pathlib import Path

import numpy as np

SEEN_SPLITS = ("train", "val")


class MissingHoldoutBank(RuntimeError):
    """A bank was named for a held-out evaluation and could not be read."""


def trained_on(banks, allow_trained_on: bool = False, verbose: bool = True, train_only_because: str | None = None) -> set[str]:
    """Case ids a model built from `banks` has SEEN: split `train` AND split `val` (the selection split).

    `banks` is a path or a list of paths. Raises MissingHoldoutBank if any named bank is absent or contributes no seen
    rows, unless `allow_trained_on` is set -- in which case the caller has already declared that it is not excluding
    anything and the set is unused. `train_only_because` returns the train split alone, and must say why."""
    if train_only_because is not None and not str(train_only_because).strip():
        raise ValueError("train_only_because needs a reason: the val split selected the model unless something says "
                         "otherwise, and an empty reason says nothing")
    splits = ("train",) if train_only_because else SEEN_SPLITS
    if banks is None:
        banks = []
    if isinstance(banks, (str, Path)):
        banks = [banks]

    out: set[str] = set()
    missing, empty = [], []
    for b in banks:
        p = Path(os.path.expanduser(str(b)))
        rungs = sorted(glob.glob(str(p / "rung_*.npz")))
        if not p.is_dir() or not rungs:
            missing.append(str(p))
            continue
        before = len(out)
        for npz in rungs:
            z = np.load(npz, allow_pickle=True)
            c = np.array([str(x) for x in z["case"]])
            s = np.array([str(x) for x in z["split"]])
            out |= set(c[np.isin(s, splits)].tolist())
        if len(out) == before:
            empty.append(str(p))

    if (missing or empty) and not allow_trained_on:
        bad = "".join(f"\n    absent, or holds no rung_*.npz: {m}" for m in missing)
        bad += "".join(f"\n    present but contributes no {'/'.join(splits)} rows: {e}" for e in empty)
        raise MissingHoldoutBank(
            f"held-out evaluation asked for {len(banks)} bank(s) and could not read them:{bad}\n"
            f"  Running on would silently evaluate the model on cases it was TRAINED or SELECTED on, and that error "
            f"only ever flatters the result.\n"
            f"  Five banks (allspine_v2/v3/v4/v5/v5c_fov96_ctx) were deleted on 2026-09-20 to recover "
            f"quota. Their train sets are NESTED inside the surviving generations -- v6 is a strict "
            f"subset of v7 -- so repointing at ~/allspine_v7_fov96_ctx refuses a SUPERSET of what the "
            f"old bank refused, which is the conservative direction. Do that, or rebuild the bank, or "
            f"pass --allow-trained-on if this evaluation genuinely is not held out."
        )
    if verbose:
        print(f"holdout: {len(out):,} seen cases ({'+'.join(splits)}) from {len(banks) - len(missing)} bank(s)"
              + (f"; val NOT excluded because: {train_only_because}" if train_only_because else "")
              + (f"; {len(missing)} unreadable, ignored because --allow-trained-on" if missing else ""),
              flush=True)
    return out
