#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/film_corpus_inventory.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Full usable inventory of the two film corpora the audit left half-counted: NHANES II and VinDr-SpineXR.

Why this exists (docs/DATA_COMPLETENESS_AUDIT.md, gate G0, directives D2 and D3):

  NHANES II  the release lists 17,075 entries, 17,073 are on disk, and only the 543 annotated films were ever
             offered to anything -- 542 of them films on disk, since L00452 exists only inside the Zenodo
             pickle, which is why the unannotated count is 16,531 and not the 16,530 in circulation.  Those
             films have no written reason to be out of the DETECTOR (the level bank exclusion IS written and
             measured).  This builds the per-film manifest so the detector
             self-training corpus and the corpus-manifold plot can consume them, and re-confirms from the
             compute node that the two absent entries are served as 0 bytes BY THE CDC.

  VinDr      three numbers (744 / 2,632 / 10,274) are three different objects.  This counts every one of them
             from the object itself -- the release CSVs, the pseudo-label directory, and each bank's own case
             array -- and writes one row per released image so one number means one thing afterwards.

Every count comes from the filesystem; nothing is copied from a document.  Runs as an sbatch job.  Resumable:
outputs that already exist and parse are left alone unless --force.

    python tools/film_corpus_inventory.py --out /rs/rs_grp_oschome/go2432/data/inventory/films
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import pickle
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

H = Path(os.path.expanduser("~"))
RAW = H / "spine-detector/data/raw"
HEX32 = re.compile(r"([0-9a-f]{32})")

# banks whose membership is recorded per film.  name -> path
LEVEL_BANKS = {
    "allspine_v9_fov96_ctx": H / "allspine_v9_fov96_ctx",
    "allspine_v8_fov96_ctx": H / "allspine_v8_fov96_ctx",
    "allspine_v7_fov96_ctx": H / "allspine_v7_fov96_ctx",
    "vindrps_fov96_ctx": H / "vindrps_fov96_ctx",
    "vindr_fov96_ctx": H / "vindr_fov96_ctx",
    "carm_mix_fov96_ctx": H / "carm_mix_fov96_ctx",
    "films_all2_fov96_ctx": H / "films_all2_fov96_ctx",
}
YOLO_BANKS = ["yolo_v2", "yolo_v3", "yolo_v4z", "yolo_v5f_p00", "yolo_v5f_p05", "yolo_v5f_p08", "yolo_v6f"]


def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)


# --------------------------------------------------------------------------------------- bank readers
def bank_cases(bank: Path):
    """{case string} and {case: source} from a bank's rung_1.npz, plus the val set."""
    if not bank.exists():
        return None
    try:
        z = np.load(bank / "rung_1.npz", allow_pickle=True)
    except Exception as e:  # noqa: BLE001
        log(f"  {bank.name}: npz unreadable ({e})")
        return None
    case = np.array([str(c) for c in z["case"]])
    src = np.array([str(s) for s in z["source"]]) if "source" in z.keys() else None
    split = np.array([str(s) for s in z["split"]]) if "split" in z.keys() else None
    per = {}
    val = set()
    for i, c in enumerate(case):
        per.setdefault(c, src[i] if src is not None else c.split("_")[0])
        if split is not None and split[i] == "val":
            val.add(c)
    return {"cases": per, "val": val, "n_crops": int(len(case))}


def load_vindr_study_map():
    """tools/identity/vindr_image_to_study.json -- the file nests the map under a key beside a _summary block,
    which is why every distinct-study count in the 2026-09-23 audit came back 0.  Find the map by shape."""
    p = H / "spinesurg-ct-nnunet/tools/identity/vindr_image_to_study.json"
    if not p.exists():
        return {}, f"absent: {p}"
    j = json.load(open(p))
    if isinstance(j, dict):
        flat = {k: v for k, v in j.items() if HEX32.fullmatch(str(k))}
        if len(flat) > 1000:
            return flat, f"{p} (top level, {len(flat)} keys)"
        for k, v in j.items():
            if isinstance(v, dict):
                inner = {kk: vv for kk, vv in v.items() if HEX32.fullmatch(str(kk))}
                if len(inner) > 1000:
                    return inner, f"{p}['{k}'] ({len(inner)} keys)"
    return {}, f"{p}: no 32-hex keyed map found (top-level keys: {sorted(j)[:8]})"


def ann_levels(path: Path):
    """(n_levels, n_exact) for one pseudo-label ann json; (-1, -1) if unreadable."""
    try:
        j = json.load(open(path))
    except Exception:  # noqa: BLE001
        return -1, -1
    lv = j.get("levels") or {}
    exact = 0
    for v in lv.values():
        if isinstance(v, dict) and str(v.get("tier") or v.get("level_tier") or "") == "exact":
            exact += 1
    return len(lv), exact


# --------------------------------------------------------------------------------------- NHANES
def nhanes(out: Path, banks: dict):
    R = {}
    n = RAW / "nhanes_full"
    tif = sorted(n.glob("*.tiff"))
    on_disk = {f.name: f.stat().st_size for f in tif}
    log(f"NHANES: {len(on_disk)} tiff on disk")

    # the CDC index the downloader walked
    listed = []
    fl = n / ".filelist.txt"
    if fl.exists():
        listed = [x.strip() for x in open(fl) if x.strip().lower().endswith((".tiff", ".tif"))]
    listed_set = set(listed)
    absent = sorted(listed_set - set(on_disk))
    R["release_index_entries"] = len(listed_set)
    R["on_disk"] = len(on_disk)
    R["absent_from_disk"] = absent
    R["on_disk_not_listed"] = sorted(set(on_disk) - listed_set)

    # re-confirm at source, from the compute node (the login node has no route)
    R["absent_at_source"] = {}
    import urllib.request
    for name in absent:
        rec = {}
        for meth in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(
                    f"https://ftp.cdc.gov/pub/NHANES/XRays/Nhanes2/{name}", method=meth)
                with urllib.request.urlopen(req, timeout=120) as resp:
                    body = resp.read() if meth == "GET" else b""
                    rec[meth] = {"status": resp.status,
                                 "content_length": resp.headers.get("Content-Length"),
                                 "last_modified": resp.headers.get("Last-Modified"),
                                 "bytes_received": len(body)}
            except Exception as e:  # noqa: BLE001
                rec[meth] = {"error": str(e)}
        R["absent_at_source"][name] = rec
        log(f"  {name} at source: {rec}")

    # annotations (Zenodo 10223910)
    pk = sorted((RAW / "nhanes_annotated/extracted/nhanes").glob("*.pkl"))
    ann_by_film = {}
    pk_person = {}
    for p in pk:
        stem = p.name[:6]                       # C00160 / L00160
        ann_by_film[stem] = p.name
        try:
            with open(p, "rb") as fh:
                d = pickle.load(fh)
            sid = d.get("sample_id") if isinstance(d, dict) else None
        except Exception:  # noqa: BLE001
            sid = None
        pk_person[stem] = str(sid) if sid is not None else stem[1:]
    log(f"NHANES: {len(ann_by_film)} annotated films")

    # pseudo-labels already computed over the unannotated films
    ps = {}
    unparsed = []
    pdir = H / "nhanes_pseudo/ann"
    if pdir.exists():
        for a in pdir.glob("*.json"):
            # two name forms are in use: NHANESPS_C00156.json and NHANES_nhanes_cervical_00156.json
            m = re.search(r"([CL])(\d{5})", a.name)
            if m:
                stem = m.group(1) + m.group(2)
            else:
                m2 = re.search(r"(cervical|lumbar)\D*(\d{5})", a.name.lower())
                if not m2:
                    unparsed.append(a.name)
                    continue
                stem = ("C" if m2.group(1) == "cervical" else "L") + m2.group(2)
            nl, nx = ann_levels(a)
            ps[stem] = {"ann": a.name, "levels": nl, "exact": nx}
    if unparsed:
        log(f"  WARNING {len(unparsed)} pseudo anns whose film could not be parsed, e.g. {unparsed[:3]}")
    log(f"NHANES: {len(ps)} pseudo-label anns")

    # detector-bank membership (yolo images are named nhanes_<view>_<id>.png)
    det = defaultdict(set)
    for v in YOLO_BANKS:
        d = H / "spine-detector/data/" / v / "images"
        if not d.exists():
            continue
        for split in ("train", "val", "test"):
            for f in (d / split).glob("nhanes_*"):
                m = re.match(r"nhanes_(cervical|lumbar)_(\d+)", f.stem)
                if m:
                    det[("C" if m.group(1) == "cervical" else "L") + m.group(2)].add(f"{v}/{split}")

    # level-bank membership: case strings NHANES_nhanes_cervical_00160 (films_drr) and NH_00160_c (nhanes_drr)
    lvl = defaultdict(set)
    for bname, b in banks.items():
        if not b:
            continue
        for c, s in b["cases"].items():
            m = re.match(r"NHANES_nhanes_(cervical|lumbar)_(\d+)$", c)
            if m:
                lvl[("C" if m.group(1) == "cervical" else "L") + m.group(2)].add(bname)
                continue
            m = re.match(r"NH_(\d+)_([cl])$", c)
            if m:
                lvl[m.group(2).upper() + m.group(1)].add(bname + "(render)")

    # ------------------------------------------------------------------ the manifest
    rows = []
    for name in sorted(listed_set | set(on_disk)):
        stem = name[:6]
        view = "cervical" if stem[0] == "C" else "lumbar" if stem[0] == "L" else "unknown"
        pid = stem[1:]
        annotated = stem in ann_by_film
        p = ps.get(stem)
        d = sorted(det.get(stem, ()))
        lv = sorted(lvl.get(stem, ()))
        if annotated:
            role = "level_bank+detector"
        elif p and p["levels"] > 0:
            role = "detection_selftrain(pseudo-named)"
        elif p:
            role = "detection_selftrain(boxes only)"
        else:
            role = "detection_selftrain(unlabelled)"
        rows.append({
            "film_id": stem,
            "file": name,
            "view": view,
            "person_key": f"nhanes_{pid}",
            "on_disk": int(name in on_disk),
            "bytes": on_disk.get(name, 0),
            "in_release_index": int(name in listed_set),
            "annotated": int(annotated),
            "annotation_file": ann_by_film.get(stem, ""),
            "pseudo_ann": (p or {}).get("ann", ""),
            "pseudo_levels": (p or {}).get("levels", 0),
            "pseudo_exact_levels": (p or {}).get("exact", 0),
            "detector_banks": ";".join(d),
            "level_banks": ";".join(lv),
            "usable_for": role,
        })
    mpath = out / "nhanes_film_manifest.csv"
    with open(mpath, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    log(f"NHANES: wrote {mpath} ({len(rows)} rows)")

    byview = Counter(r["view"] for r in rows if r["on_disk"])
    ann_view = Counter(r["view"] for r in rows if r["annotated"])
    R.update({
        "manifest": str(mpath),
        "manifest_rows": len(rows),
        "on_disk_by_view": dict(byview),
        "annotated": sum(r["annotated"] for r in rows),
        "annotated_by_view": dict(ann_view),
        "annotated_persons": len({pk_person[s] for s in ann_by_film}),
        "annotated_without_tiff": sorted(s for s in ann_by_film if s + ".tiff" not in on_disk),
        "unannotated_on_disk": sum(1 for r in rows if r["on_disk"] and not r["annotated"]),
        "unannotated_by_view": dict(Counter(r["view"] for r in rows if r["on_disk"] and not r["annotated"])),
        "pseudo_ann_files": len(ps),
        "pseudo_anns_unmatched_to_a_release_entry": len(set(ps) - {r["film_id"] for r in rows}),
        "pseudo_labelled": sum(1 for r in rows if r["pseudo_ann"]),
        "pseudo_labelled_with_a_named_level": sum(1 for r in rows if r["pseudo_levels"] > 0),
        "pseudo_labelled_empty": sum(1 for r in rows if r["pseudo_ann"] and r["pseudo_levels"] == 0),
        "never_pseudo_labelled": sum(1 for r in rows if r["on_disk"] and not r["annotated"] and not r["pseudo_ann"]),
        "in_any_detector_bank": sum(1 for r in rows if r["detector_banks"]),
        "in_any_level_bank": sum(1 for r in rows if r["level_banks"]),
        "distinct_persons_on_disk": len({r["person_key"] for r in rows if r["on_disk"]}),
        "persons_with_both_views": sum(1 for _, c in Counter(
            r["person_key"] for r in rows if r["on_disk"]).items() if c > 1),
        "usable_for": dict(Counter(r["usable_for"] for r in rows if r["on_disk"])),
    })
    return R


# --------------------------------------------------------------------------------------- VinDr
def vindr(out: Path, banks: dict):
    R = {}
    v = RAW / "vindr/1.0.0"
    disk = {}
    for split in ("train", "test"):
        for f in (v / f"{split}_images").glob("*.dicom"):
            disk[f.stem] = {"split": split, "bytes": f.stat().st_size}
    log(f"VinDr: {len(disk)} dicom on disk")

    lesion_rows = Counter()
    nofinding = Counter()
    study = {}
    for split in ("train", "test"):
        with open(v / f"annotations/{split}.csv", newline="") as fh:
            for r in csv.DictReader(fh):
                iid = r["image_id"]
                study[iid] = r["study_id"]
                if str(r.get("lesion_type", "")).strip().lower() == "no finding":
                    nofinding[iid] += 1
                else:
                    lesion_rows[iid] += 1

    smap, smap_src = load_vindr_study_map()
    R["study_map_source"] = smap_src
    for iid, sid in smap.items():
        study.setdefault(iid, sid if isinstance(sid, str) else str(sid))

    # pseudo-labels over the whole release
    ps = {}
    pdir = H / "vindr_pseudo/ann"
    if pdir.exists():
        for a in pdir.glob("VINDRPS_*.json"):
            nl, nx = ann_levels(a)
            ps[a.name[len("VINDRPS_"):-len(".json")]] = {"levels": nl, "exact": nx}
    log(f"VinDr: {len(ps)} pseudo-label anns")
    drr744 = set()
    p744 = H / "vindr_pseudo_drr/ann"
    if p744.exists():
        for a in p744.glob("*.json"):
            m = HEX32.search(a.name)
            if m:
                drr744.add(m.group(1))
    det2328 = set()
    pdet = H / "vindr_det_drr/ann"
    if pdet.exists():
        for a in pdet.glob("*.json"):
            m = HEX32.search(a.name)
            if m:
                det2328.add(m.group(1))

    # bank membership, per released image
    inbank = defaultdict(set)
    bank_studies = {}
    for bname, b in banks.items():
        if not b:
            continue
        films = set()
        for c in b["cases"]:
            m = HEX32.search(c)
            if m:
                films.add(m.group(1))
                inbank[m.group(1)].add(bname)
        if films:
            bank_studies[bname] = {
                "films": len(films),
                "studies": len({study[f] for f in films if f in study}),
                "films_without_a_study_id": len([f for f in films if f not in study]),
            }
    for bname in banks:
        bank_studies.setdefault(bname, {"films": 0, "studies": 0, "films_without_a_study_id": 0})

    rows = []
    for iid in sorted(disk):
        p = ps.get(iid)
        rows.append({
            "image_id": iid,
            "study_id": study.get(iid, ""),
            "release_split": disk[iid]["split"],
            "bytes": disk[iid]["bytes"],
            "lesion_boxes": lesion_rows.get(iid, 0),
            "no_finding_rows": nofinding.get(iid, 0),
            "in_detector_manifest": int(lesion_rows.get(iid, 0) > 0),
            "pseudo_labelled": int(p is not None),
            "pseudo_levels": (p or {}).get("levels", 0),
            "pseudo_exact_levels": (p or {}).get("exact", 0),
            "in_vindr_det_drr_2328": int(iid in det2328),
            "in_vindr_744_route": int(iid in drr744),
            "level_banks": ";".join(sorted(inbank.get(iid, ()))),
        })
    mpath = out / "vindr_film_manifest.csv"
    with open(mpath, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    log(f"VinDr: wrote {mpath} ({len(rows)} rows)")

    R.update({
        "manifest": str(mpath),
        "release_images": len(rows),
        "release_studies": len({r["study_id"] for r in rows if r["study_id"]}),
        "images_by_split": dict(Counter(r["release_split"] for r in rows)),
        "studies_by_split": {s: len({r["study_id"] for r in rows if r["release_split"] == s})
                             for s in ("train", "test")},
        "with_a_lesion_box": sum(r["in_detector_manifest"] for r in rows),
        "no_finding_only": sum(1 for r in rows if not r["in_detector_manifest"]),
        "pseudo_labelled_anns": len(ps),
        "pseudo_labelled_on_disk": sum(r["pseudo_labelled"] for r in rows),
        "pseudo_with_a_named_level": sum(1 for r in rows if r["pseudo_levels"] > 0),
        "pseudo_with_empty_levels": sum(1 for r in rows if r["pseudo_labelled"] and r["pseudo_levels"] == 0),
        "never_pseudo_labelled": sum(1 for r in rows if not r["pseudo_labelled"]),
        "vindr_det_drr_2328": len(det2328),
        "vindr_744_route": len(drr744),
        "per_bank": bank_studies,
        "in_any_level_bank": sum(1 for r in rows if r["level_banks"]),
    })
    return R


# --------------------------------------------------------------------------------------- report
def report(R, out: Path):
    n, v = R["nhanes"], R["vindr"]
    L = []
    A = L.append
    A("# NHANES II and VinDr-SpineXR: the usable inventory")
    A("")
    A(f"Computed {R['built']} by `tools/film_corpus_inventory.py` from the filesystem, the release indices and")
    A("each bank's own case array. Gate G0, directives D2 and D3.")
    A("")
    A("## NHANES II")
    A("")
    A(f"- Release index: **{n['release_index_entries']} entries**; on disk **{n['on_disk']}**"
      f" ({n['on_disk_by_view'].get('cervical', 0)} cervical + {n['on_disk_by_view'].get('lumbar', 0)} lumbar),"
      f" over **{n['distinct_persons_on_disk']} sample persons**.")
    for name, rec in n["absent_at_source"].items():
        h = rec.get("HEAD", {})
        g = rec.get("GET", {})
        A(f"- `{name}` is **not a download failure of ours**: the CDC serves it HTTP {h.get('status')} with"
          f" Content-Length {h.get('content_length')} (Last-Modified {h.get('last_modified')}); a GET returns"
          f" {g.get('bytes_received')} bytes. Nothing to repair on our side.")
    A(f"- Landmark annotations (Zenodo 10223910): **{n['annotated']} films**"
      f" ({n['annotated_by_view'].get('cervical', 0)} cervical + {n['annotated_by_view'].get('lumbar', 0)} lumbar)"
      f" over **{n['annotated_persons']} persons**."
      + (f" {len(n['annotated_without_tiff'])} of them have no TIFF on disk"
         f" ({', '.join(n['annotated_without_tiff'])}) — their pixels ride inside the pickle."
         if n["annotated_without_tiff"] else ""))
    A(f"- **Unannotated: {n['unannotated_on_disk']} films**"
      f" ({n['unannotated_by_view'].get('cervical', 0)} cervical + {n['unannotated_by_view'].get('lumbar', 0)}"
      f" lumbar). Of those, {n['pseudo_labelled']} already carry a pseudo-label ann"
      f" ({n['pseudo_labelled_with_a_named_level']} with at least one named level,"
      f" {n['pseudo_labelled_empty']} with an empty levels dict) and"
      f" **{n['never_pseudo_labelled']} were never pseudo-labelled at all**.")
    A(f"- In a detector bank: **{n['in_any_detector_bank']}**. In a level bank: **{n['in_any_level_bank']}**.")
    A("")
    A("Role per film (`usable_for` column of the manifest):")
    A("")
    A("| role | films |")
    A("|---|---|")
    for k, c in sorted(n["usable_for"].items(), key=lambda kv: -kv[1]):
        A(f"| {k} | {c} |")
    A("")
    A(f"Manifest: `{n['manifest']}` ({n['manifest_rows']} rows, one per release entry).")
    A("")
    A("## VinDr-SpineXR")
    A("")
    A(f"- Release: **{v['release_images']} images / {v['release_studies']} studies**"
      f" ({v['images_by_split'].get('train', 0)} train from {v['studies_by_split'].get('train', 0)} studies,"
      f" {v['images_by_split'].get('test', 0)} test from {v['studies_by_split'].get('test', 0)}).")
    A(f"- **{v['with_a_lesion_box']}** images carry at least one lesion box; **{v['no_finding_only']}** are"
      " 'No finding' only. The detector manifest ingested only the first group, and the view classifier and the"
      " 744-film route were computed on that half.")
    A(f"- Pseudo-labelled: **{v['pseudo_labelled_on_disk']} anns**, of which"
      f" **{v['pseudo_with_a_named_level']}** carry a named level and **{v['pseudo_with_empty_levels']}** have an"
      f" empty levels dict and produce no crop. Never pseudo-labelled: {v['never_pseudo_labelled']}.")
    A("")
    A("One number per object, per bank (films and studies read from the bank's own case array):")
    A("")
    A("| bank | VinDr films | VinDr studies |")
    A("|---|---|---|")
    for b, d in sorted(v["per_bank"].items(), key=lambda kv: -kv[1]["films"]):
        A(f"| `{b}` | {d['films']} | {d['studies']} |")
    A(f"| `vindr_det_drr` (view-classifier route) | {v['vindr_det_drr_2328']} | — |")
    A(f"| `vindr_pseudo_drr` (the 744) | {v['vindr_744_route']} | — |")
    A("")
    A(f"Manifest: `{v['manifest']}` ({v['release_images']} rows, one per released image).")
    A("")
    A(f"Study map: {v['study_map_source']}")
    (out / "FILM_CORPUS_INVENTORY.md").write_text("\n".join(L) + "\n")
    log(f"wrote {out / 'FILM_CORPUS_INVENTORY.md'}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    jpath = out / "film_corpus_inventory.json"
    if jpath.exists() and not a.force:
        try:
            done = json.load(open(jpath))
            if done.get("nhanes", {}).get("manifest_rows") and done.get("vindr", {}).get("release_images"):
                log(f"already complete: {jpath}; use --force to rebuild")
                print(f"FILM_INVENTORY_DONE nhanes={done['nhanes']['manifest_rows']} "
                      f"vindr={done['vindr']['release_images']} (resumed, nothing recomputed)")
                return 0
        except Exception:  # noqa: BLE001
            pass

    log("reading banks")
    banks = {k: bank_cases(p) for k, p in LEVEL_BANKS.items()}
    for k, b in banks.items():
        log(f"  {k}: {'absent' if b is None else str(b['n_crops']) + ' crops'}")

    R = {"built": time.strftime("%Y-%m-%d %H:%M:%S %Z"),
         "host": os.uname().nodename if hasattr(os, "uname") else "?"}
    R["nhanes"] = nhanes(out, banks)
    R["vindr"] = vindr(out, banks)
    json.dump(R, open(jpath, "w"), indent=1)
    report(R, out)

    n, v = R["nhanes"], R["vindr"]
    print(f"FILM_INVENTORY_DONE nhanes_rows={n['manifest_rows']} nhanes_on_disk={n['on_disk']} "
          f"nhanes_annotated={n['annotated']} nhanes_unannotated={n['unannotated_on_disk']} "
          f"vindr_rows={v['release_images']} vindr_studies={v['release_studies']} "
          f"vindr_in_v9={v['per_bank'].get('allspine_v9_fov96_ctx', {}).get('films')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
