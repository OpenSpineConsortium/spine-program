# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/xray_dataset_usage.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Every X-ray dataset on the grid, how much of it reaches training, and the reason for every image that does not.

WHY THIS EXISTS AS A TOOL AND NOT A DOCUMENT. A written inventory goes stale the moment a bank is rebuilt, and
the question it answers -- "are we using all the real radiographs we have" -- is one this project has already got
wrong once, when the level model trained for a week on a bank with no thoracic vertebrae in it. So the inventory
is computed: raw image counts come from the filesystem, used counts come from the crop banks' own case arrays,
and the difference is reported per dataset with a reason, every time it is run.

THE THREE NUMBERS PER DATASET, and the distinction between them is the whole point:
    on disk        images present in the raw directory
    labelled       images for which a per-vertebra level label exists anywhere (human, converted or pseudo)
    in a bank      images whose crops actually appear in a crop bank that a model was trained on
An image can be on disk, labelled, and still not in a bank, which is the case this tool exists to surface.

REASONS ARE NAMED, NOT INFERRED FROM ABSENCE. A dataset is unused for one of a small number of reasons and they
have different remedies: no annotation exists, the annotation is class-agnostic so it gives boxes without names,
the images are a duplicate of another set, the images are not radiographs, or a converted render directory was
built but never folded into a bank. The last one is a pure oversight and the cheapest to fix; the tool separates
it from the rest so it cannot hide among them.

    python tools/xray_dataset_usage.py --out ~/model_night/XRAY_DATASET_USAGE.md
"""
from __future__ import annotations

import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

# ".dicom" is VinDr-SpineXR's extension and was missing until 2026-09-23, which is why this table printed
# "VinDr-SpineXR ... on disk 0" while 10,466 DICOMs sat in raw/vindr/1.0.0.
IMG_EXT = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".dcm", ".dicom")

# Every raw radiograph collection, with what is known about it independent of this computation. `key` is the
# substring that identifies its crops inside a bank's case ids.
RAW = [
    {"name": "CSXA cervical", "path": "~/spine-detector/data/raw/csxa", "key": "csxa",
     "annotation": "per-vertebra, released with the dataset", "view": "lateral"},
    {"name": "BUU-LSPINE", "path": "~/spine-detector/data/raw/buu_full", "key": "buu",
     "annotation": "endplate lines, L1-L5 plus S1", "view": "AP + lateral"},
    {"name": "BUU Drive mirror", "path": "~/spine-detector/data/raw/buu_drive", "key": "buu_drive",
     "annotation": "same as BUU-LSPINE", "view": "AP + lateral"},
    {"name": "NHANES II", "path": "~/spine-detector/data/raw/nhanes_full", "key": "nhanes",
     "annotation": "543 films have landmarks; the rest have none", "view": "lateral"},
    {"name": "VinDr-SpineXR", "path": "~/spine-detector/data/raw/vindr/1.0.0", "key": "vindr",
     "annotation": "lesion boxes, NOT per-vertebra levels; 10,466 images in 5,000 studies", "view": "AP + lateral"},
    {"name": "AASCE / BoostNet", "path": "~/spine-detector/data/raw/aasce", "key": "aasce",
     "annotation": "68 landmarks, 17 vertebrae T1-L5", "view": "AP"},
    {"name": "Mendeley 5jdfdgp762", "path": "~/spine-detector/data/raw/mendeley_716", "key": "mendeley",
     "annotation": "4 corners per body, class-agnostic", "view": "lateral"},
    {"name": "IEEE DataPort lateral full-spine", "path": "~/spine-detector/data/raw/lateral_236", "key": "lateral236",
     "annotation": "none in the release", "view": "lateral"},
    {"name": "Spinal-AI2024 (machine generated)", "path": "~/spine-detector/data/raw/spinal_ai2024", "key": "spinalai",
     "annotation": "machine generated, 17 landmarks", "view": "AP"},
    {"name": "AASCE test split", "path": "~/spine-detector/data/raw/buu_2000", "key": "buu2000",
     "annotation": "report spreadsheet only", "view": "AP + lateral"},
]

# The bank the reported model is trained on, in preference order. Every other bank is "some bank".
SHIPPED_BANKS = ["allspine_v9_fov96_ctx", "allspine_v8_fov96_ctx"]

# Converted render directories: an image here has a per-vertebra level label and is one step from a crop bank.
RENDER_DIRS = ["~/nhanes_drr", "~/aasce_drr", "~/mendeley_drr", "~/spinalai_drr", "~/films_drr",
               "~/nhanes_pseudo", "~/vindr_pseudo", "~/lateral236_pseudo"]


def count_images(p: Path, cap=200000):
    if not p.exists():
        return None
    n = 0
    for f in p.rglob("*"):
        if f.suffix.lower() in IMG_EXT:
            n += 1
            if n >= cap:
                break
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="~/model_night/XRAY_DATASET_USAGE.md")
    ap.add_argument("--banks", nargs="*", default=None)
    a = ap.parse_args()
    H = Path(os.path.expanduser("~"))

    banks = [Path(os.path.expanduser(b)) for b in a.banks] if a.banks else \
        sorted({p.parent for p in H.glob("*/rung_1.npz")})
    print(f"{len(banks)} crop banks found")

    # which raw datasets appear in which bank, counted by DISTINCT FILM not by crop
    in_bank = defaultdict(lambda: defaultdict(set))
    bank_films = {}
    for b in banks:
        try:
            z = np.load(b / "rung_1.npz", allow_pickle=True)
            case = np.array([str(c) for c in z["case"]])
        except Exception as e:  # noqa: BLE001
            print(f"  {b.name}: unreadable ({e})")
            continue
        bank_films[b.name] = len(set(case.tolist()))
        low = [c.lower() for c in set(case.tolist())]
        for d in RAW:
            k = d["key"].lower()
            hits = {c for c in low if k in c}
            if hits:
                in_bank[d["name"]][b.name] = hits
        print(f"  {b.name}: {bank_films[b.name]} films", flush=True)

    rows = []
    for d in RAW:
        p = Path(os.path.expanduser(d["path"]))
        n_disk = count_images(p)
        banks_with = in_bank.get(d["name"], {})
        best_bank = max(banks_with, key=lambda k: len(banks_with[k])) if banks_with else None
        n_bank = len(banks_with[best_bank]) if best_bank else 0
        # "some bank" is not "the bank". The reported model is trained on allspine_v9 (v8 before the VerSe
        # re-key), and a dataset can sit in 15,000 crops of a pseudo-label bank while contributing nothing to
        # it -- reading the max-bank column as the shipped one is how VinDr came to be printed three ways.
        shipped = {bn: banks_with[bn] for bn in SHIPPED_BANKS if bn in banks_with}
        rows.append({**d, "on_disk": n_disk, "in_bank_films": n_bank, "best_bank": best_bank,
                     "in_shipped_bank": max((len(v) for v in shipped.values()), default=0),
                     "shipped_bank": next((bn for bn in SHIPPED_BANKS if bn in shipped), None),
                     "banks": sorted(banks_with, key=lambda k: -len(banks_with[k]))[:4]})

    renders = []
    for r in RENDER_DIRS:
        rp = Path(os.path.expanduser(r))
        if not rp.exists():
            continue
        n_ann = len(list((rp / "ann").glob("*.json"))) if (rp / "ann").exists() else 0
        stems = {p.stem.lower() for p in (rp / "ann").glob("*.json")} if (rp / "ann").exists() else set()
        # a render directory is "in a bank" when a bank's case ids include its ann stems
        used = 0
        for b in banks:
            try:
                z = np.load(b / "rung_1.npz", allow_pickle=True)
                cs = {str(c).lower() for c in z["case"]}
            except Exception:  # noqa: BLE001
                continue
            hit = len(stems & cs)
            used = max(used, hit)
        renders.append({"dir": str(rp), "labelled_films": n_ann, "films_in_a_bank": used})

    out = Path(os.path.expanduser(a.out))
    out.parent.mkdir(parents=True, exist_ok=True)
    L = []
    L.append("# X-ray datasets on the grid, and how each one is used\n")
    L.append("Computed by `tools/xray_dataset_usage.py`. Counts of films in a bank are DISTINCT FILMS, not crops,")
    L.append("and are taken from the bank's own case array rather than from any written record.\n")
    L.append("`in the shipped bank` is the level bank the reported model was trained on (allspine_v9, v8 before")
    L.append("the VerSe re-key). `films in any bank` is the largest count over every crop bank on the machine,")
    L.append("most of which are superseded or were never trained on -- the two columns are different questions.\n")
    L.append("| dataset | view | on disk | in the shipped bank | films in any bank | that bank | annotation |")
    L.append("|---|---|---:|---:|---:|---|---|")
    for r in rows:
        od = "missing" if r["on_disk"] is None else f"{r['on_disk']:,}"
        bb = r["best_bank"] or "-"
        L.append(f"| {r['name']} | {r['view']} | {od} | {r['in_shipped_bank']:,} | {r['in_bank_films']:,} | {bb} | {r['annotation']} |")
    L.append("\n## Converted label sets, and whether they reached a bank\n")
    L.append("A render directory holds films with per-vertebra level labels. A row where `films in a bank` is 0")
    L.append("is a label set that exists and is not being trained on, which is the cheapest gap to close.\n")
    L.append("| render directory | labelled films | films in a bank |")
    L.append("|---|---:|---:|")
    for r in renders:
        L.append(f"| `{r['dir']}` | {r['labelled_films']:,} | {r['films_in_a_bank']:,} |")
    L.append("\n## Crop banks\n")
    L.append("| bank | distinct films |")
    L.append("|---|---:|")
    for b, n in sorted(bank_films.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{b}` | {n:,} |")
    txt = "\n".join(L) + "\n"
    out.write_text(txt, encoding="utf-8")
    json.dump({"raw": rows, "renders": renders, "bank_films": bank_films},
              open(str(out).replace(".md", ".json"), "w"), indent=1)
    print("\n" + txt)
    print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
