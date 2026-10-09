#!/usr/bin/env python3
"""Patient-grouped train/validation/test split over the datasets the recipe downloaded (SO3, interface stub).

WHY A STUB WITH A FIXED INTERFACE. The split rule is the part that must not vary between datasets:
every image of one person lands in one partition, the draw is deterministic (seed 20260919, the
review's seed, protocol section 7.8), and the partition is stratified per dataset so a small set is
not swallowed by a large one. That rule is implemented and self-tested here. What varies per
dataset is how to find its subjects under $DATA_ROOT/<id>/ and which released field groups images
by person (charting field `grouping_variable_released`; the schema's `patient_level_dedup`), and
that cannot be written before the data is on disk and its layout read. So discovery is a registry:
`DISCOVERY_RULES` maps a dataset id to a glob and a regex that extracts the subject id from a path,
and `DISCOVERERS` holds any function that needs more than a regex. Both are empty on purpose. A
dataset with no rule is reported, never split by guess: a split that groups by file name when the
release groups by patient id is the leakage this stub exists to prevent.

A KNOWN LIMIT OF THE FILL RULE. Partitions are filled by cumulative subject count, and a group is
never divided, so a partition whose slice is smaller than one group can end up empty: five patients
with two images each split 8/0/2 under 0.7/0.1/0.2, because the group that would straddle the
train/val cut goes whole into train and the next one lands past the val cut. The rule is kept
because it is the one the self-test and tests/test_recipe.py compute by hand; `main` prints a
warning for every dataset whose non-zero fraction got no subject, and a dataset that small should
be held out entirely rather than split.

Interface:
  Subject(dataset_id, subject_id, group_key, images)         one person in one dataset
  discover(dataset_id, dest) -> list[Subject]                 registry lookup; NotImplementedError when unknown
  patient_grouped_split(subjects, fractions, seed) -> {train, val, test: [Subject]}
  main: --data-root, --manifest, --out, --fractions, --seed, --datasets, --limit, --dry-run, --self-test,
        --run-dir/--run-date (optional: record the invocation in <run-dir>/run_meta.json through sdr.common)
Output: <out>/splits.json = {dataset_id: {train: [subject_id], val: [...], test: [...]}, meta: {...}}.
Reads recipe/manifest.csv (written by `python -m sdr.recipe`) and $DATA_ROOT/<id>/.recipe_status.
This script runs on a reader's machine after the download, so `--run-dir` is optional here and
sdr is imported only when it is given.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

SEED = 20260919
FRACTIONS = (0.7, 0.1, 0.2)   # train, val, test; the same split rule for every dataset

# dataset_id -> (glob under $DATA_ROOT/<id>/, regex with a `subject` group applied to the path relative to it).
# Example (not a rule; VerSe's layout must be read from disk first):
#   "verse": ("**/rawdata/*/*_ct.nii.gz", r"sub-(?P<subject>verse\d+)")
DISCOVERY_RULES: dict[str, tuple[str, str]] = {}
DISCOVERERS: dict[str, Callable[[Path], list["Subject"]]] = {}


@dataclass
class Subject:
    dataset_id: str
    subject_id: str
    group_key: str                    # what must stay in one partition: the patient id; equals subject_id unless a dataset says otherwise
    images: list[str] = field(default_factory=list)


def register(dataset_id: str):
    """Decorator: register a discoverer `f(dest: Path) -> list[Subject]` for one dataset id."""
    def deco(f):
        DISCOVERERS[dataset_id] = f
        return f
    return deco


def discover_by_rule(dataset_id: str, dest: Path, glob: str, regex: str) -> list[Subject]:
    """Group files matching `glob` by the `subject` group of `regex` over the relative path."""
    rx, groups = re.compile(regex), defaultdict(list)
    for f in sorted(dest.glob(glob)):
        m = rx.search(str(f.relative_to(dest)).replace("\\", "/"))
        if m:
            groups[m.group("subject")].append(str(f.relative_to(dest)))
    return [Subject(dataset_id, s, s, imgs) for s, imgs in sorted(groups.items())]


def discover(dataset_id: str, dest: Path) -> list[Subject]:
    """Subjects of one downloaded dataset, through the registry. Raises NotImplementedError with
    what to add when neither a rule nor a discoverer exists."""
    if dataset_id in DISCOVERERS:
        return DISCOVERERS[dataset_id](dest)
    if dataset_id in DISCOVERY_RULES:
        return discover_by_rule(dataset_id, dest, *DISCOVERY_RULES[dataset_id])
    raise NotImplementedError(f"{dataset_id}: add a (glob, regex) to DISCOVERY_RULES or a @register('{dataset_id}') "
                              f"discoverer after reading the layout under {dest}; see charting/datasets/{dataset_id}.json "
                              f"(grouping_variable_released, patient_level_dedup)")


def patient_grouped_split(subjects: list[Subject], fractions: tuple[float, float, float] = FRACTIONS,
                          seed: int = SEED) -> dict[str, list[Subject]]:
    """Deterministic, per-dataset stratified, group-respecting split. Per dataset: groups (group_key)
    sorted, shuffled by a fresh random.Random(seed), then filled into train, val, test in that order
    by cumulative subject count against the fraction targets; a group is never divided."""
    assert abs(sum(fractions) - 1) < 1e-9 and all(x >= 0 for x in fractions), fractions
    out: dict[str, list[Subject]] = {"train": [], "val": [], "test": []}
    by_ds: dict[str, dict[str, list[Subject]]] = defaultdict(lambda: defaultdict(list))
    for s in subjects:
        by_ds[s.dataset_id][s.group_key].append(s)
    for ds in sorted(by_ds):
        keys = sorted(by_ds[ds])
        random.Random(seed).shuffle(keys)
        n, placed = sum(len(by_ds[ds][k]) for k in keys), 0
        cuts = (fractions[0] * n, (fractions[0] + fractions[1]) * n)
        for k in keys:
            part = "train" if placed < cuts[0] else "val" if placed < cuts[1] else "test"
            out[part].extend(by_ds[ds][k])
            placed += len(by_ds[ds][k])
    seen: dict[tuple[str, str], str] = {}
    for part, subs in out.items():
        for s in subs:
            assert seen.setdefault((s.dataset_id, s.group_key), part) == part, "a group crossed partitions"
    return out


def read_manifest(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def status_of(data_root: Path, dataset_id: str) -> str:
    p = data_root / dataset_id / ".recipe_status"
    return p.read_text(encoding="utf-8").strip() if p.exists() else ("present" if (data_root / dataset_id).exists() else "absent")


def self_test() -> int:
    """Synthetic subjects: two datasets, one with two images per person; asserts grouping,
    determinism and per-dataset stratification."""
    subs = [Subject("a", f"a{i:03d}", f"a{i:03d}", [f"a{i:03d}.png"]) for i in range(100)]
    subs += [Subject("b", f"p{i:02d}-{v}", f"p{i:02d}", [f"p{i:02d}_{v}.nii.gz"]) for i in range(20) for v in ("ap", "lat")]
    s1, s2 = patient_grouped_split(subs), patient_grouped_split(subs)
    assert [x.subject_id for x in s1["test"]] == [x.subject_id for x in s2["test"]], "not deterministic"
    counts = {p: sum(1 for x in s1[p] if x.dataset_id == "a") for p in s1}
    assert counts == {"train": 70, "val": 10, "test": 20}, counts
    for p in s1:
        pairs = defaultdict(set)
        for x in s1[p]:
            pairs[x.group_key].add(x.subject_id)
        assert all(len(v) == 2 for k, v in pairs.items() if k.startswith("p")), "a patient's two views were separated"
    print("self-test ok: grouped, deterministic, stratified per dataset")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-root", default=str(Path("~/data").expanduser()), help="$DATA_ROOT of the recipe (default ~/data)")
    ap.add_argument("--manifest", default=str(Path(__file__).resolve().parent / "manifest.csv"))
    ap.add_argument("--out", default=None, help="directory for splits.json (default: $DATA_ROOT)")
    ap.add_argument("--fractions", default="0.7,0.1,0.2", help="train,val,test")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--datasets", default=None, help="comma-separated dataset ids (default: every downloaded one)")
    ap.add_argument("--limit", type=int, default=None, help="cap the subjects discovered per dataset (the first N by subject id)")
    ap.add_argument("--dry-run", action="store_true", help="report what would be split; write nothing")
    ap.add_argument("--self-test", action="store_true", help="run the synthetic split test and exit")
    ap.add_argument("--run-dir", default=None, help="optional runs/<run-date> (relative to spine_data_review/) to record this invocation")
    ap.add_argument("--run-date", default=None, help="YYYY-MM-DD; required with --run-dir")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.run_dir:
        if not a.run_date:
            print("--run-dir needs --run-date", file=sys.stderr)
            return 2
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from sdr.common import init_run_dir  # noqa: E402  (only when asked: readers run this without sdr)
        init_run_dir(a.run_dir, a.run_date, argv)
    root, fr = Path(a.data_root).expanduser(), tuple(float(x) for x in a.fractions.split(","))
    if not Path(a.manifest).exists():
        print(f"{a.manifest} missing: run python -m sdr.recipe first (it writes recipe/manifest.csv)", file=sys.stderr)
        return 2
    rows = read_manifest(Path(a.manifest))
    want = set(a.datasets.split(",")) if a.datasets else None
    subjects, report = [], []
    for r in rows:
        ds, st = r["dataset_id"], status_of(root, r["dataset_id"])
        if want and ds not in want:
            continue
        if st != "downloaded":
            report.append((ds, st, "skipped: not marked downloaded by recipe/datasets/%s.sh" % ds))
            continue
        try:
            found = sorted(discover(ds, root / ds), key=lambda s: s.subject_id)[: a.limit]
            subjects += found
            report.append((ds, st, f"{len(found)} subjects, {sum(len(s.images) for s in found)} images"))
        except NotImplementedError as e:
            report.append((ds, st, f"no discoverer: {e}"))
    for ds, st, msg in report:
        print(f"{ds:32s} {st:11s} {msg}")
    if not subjects:
        print("nothing to split: no downloaded dataset has a discoverer yet (DISCOVERY_RULES / @register)")
        return 0 if a.dry_run else 2
    split = patient_grouped_split(subjects, fr, a.seed)
    print({p: len(v) for p, v in split.items()})
    for ds in sorted({s.dataset_id for s in subjects}):   # the fill rule's known limit (module docstring)
        for part, f in zip(("train", "val", "test"), fr):
            if f > 0 and not any(s.dataset_id == ds for s in split[part]):
                print(f"warning: {ds}: {part} is empty although its fraction is {f}; too few or too large groups "
                      f"for the cumulative fill, hold this dataset out instead of splitting it", file=sys.stderr)
    if a.dry_run:
        return 0
    out = Path(a.out).expanduser() if a.out else root
    out.mkdir(parents=True, exist_ok=True)
    doc = {ds: {p: sorted(s.subject_id for s in split[p] if s.dataset_id == ds) for p in split} for ds in sorted({s.dataset_id for s in subjects})}
    doc["meta"] = {"seed": a.seed, "fractions": fr, "group_key": "group_key (patient id where released, else subject id)",
                   "subjects": [asdict(s) for s in sorted(subjects, key=lambda s: (s.dataset_id, s.subject_id))]}
    (out / "splits.json").write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out / 'splits.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
