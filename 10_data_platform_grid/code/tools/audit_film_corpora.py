# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/audit_film_corpora.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Audit the plain-film corpora (CSXA, BUU-LSPINE, NHANES II, VinDr-SpineXR): release vs disk vs bank.

Every number is computed from the filesystem or from a bank's own case array; nothing is copied from a document.
Runs as an sbatch job (never on the login node). Writes one JSON.

    python tools/audit_film_corpora.py --out /rs/rs_grp_oschome/go2432/tmp/film_corpora_audit.json
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import pickle
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

H = Path(os.path.expanduser("~"))
RAW = H / "spine-detector/data/raw"


def bank_summary(bank: Path):
    """Distinct films per source prefix, split by train/val, from rung_1.npz + meta.json."""
    out = {"path": str(bank), "present": bank.exists()}
    if not bank.exists():
        return out
    try:
        z = np.load(bank / "rung_1.npz", allow_pickle=True)
    except Exception as e:  # noqa: BLE001
        out["error"] = f"npz unreadable: {e}"
        return out
    keys = list(z.keys())
    out["npz_keys"] = keys
    case = np.array([str(c) for c in z["case"]])
    out["n_crops"] = int(len(case))
    src = None
    if "source" in keys:
        src = np.array([str(s) for s in z["source"]])
    val = set()
    if (bank / "meta.json").exists():
        try:
            m = json.load(open(bank / "meta.json"))
            val = set(m.get("val_cases") or []) | set(m.get("val_patients") or [])
            out["meta_keys"] = sorted(m.keys())
        except Exception as e:  # noqa: BLE001
            out["meta_error"] = str(e)
    split = None
    if "split" in keys:
        split = np.array([str(s) for s in z["split"]])
    per = defaultdict(lambda: {"films": set(), "films_val": set(), "crops": 0, "crops_val": 0})
    for i, c in enumerate(case):
        if src is not None:
            s = src[i]
        else:
            s = c.split("_")[0]
        d = per[s]
        d["films"].add(c)
        d["crops"] += 1
        is_val = (split[i] == "val") if split is not None else (c in val)
        if is_val:
            d["films_val"].add(c)
            d["crops_val"] += 1
    out["per_source"] = {
        s: {"films": len(d["films"]), "films_val": len(d["films_val"]), "films_train": len(d["films"]) - len(d["films_val"]),
            "crops": d["crops"], "crops_val": d["crops_val"]}
        for s, d in sorted(per.items())
    }
    out["distinct_films"] = int(len(set(case.tolist())))
    # vindr: distinct studies among the films
    vmap_p = H / "spinesurg-ct-nnunet/tools/identity/vindr_image_to_study.json"
    if vmap_p.exists():
        vmap = json.load(open(vmap_p))
        studies = set()
        for c in set(case.tolist()):
            m = re.search(r"([0-9a-f]{32})", c)
            if m and m.group(1) in vmap:
                studies.add(vmap[m.group(1)])
        out["vindr_distinct_studies"] = len(studies)
    return out


def drr_dir_summary(d: Path, id_re=None):
    out = {"path": str(d), "present": d.exists()}
    if not d.exists():
        return out
    anns = sorted((d / "ann").glob("*.json"))
    out["n_ann"] = len(anns)
    out["n_img"] = len(list((d / "img").glob("*"))) if (d / "img").exists() else None
    src = Counter()
    lvl_src = Counter()
    pids = set()
    n_levels = 0
    for a in anns:
        try:
            j = json.load(open(a))
        except Exception:  # noqa: BLE001
            src["<unreadable>"] += 1
            continue
        src[str(j.get("source") or a.name.split("_")[0])] += 1
        if j.get("patient_id"):
            pids.add(j["patient_id"])
        for v in (j.get("levels") or {}).values():
            n_levels += 1
            lvl_src[str(v.get("level_source") or ("pseudo" if j.get("pseudo_label") else "?"))] += 1
    out["per_source"] = dict(src)
    out["distinct_patient_id"] = len(pids)
    out["n_levels"] = n_levels
    out["level_source"] = dict(lvl_src)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    R = {}

    # ---------------- CSXA ----------------
    c = RAW / "csxa"
    pngs = sorted((c / "images/datasets-PNG").glob("*.png"))
    jsons = sorted((c / "annotations/datasets-JSON").glob("*.json"))
    R["csxa"] = {
        "png": len(pngs), "json": len(jsons),
        "png_without_json": len({p.stem for p in pngs} - {j.stem for j in jsons}),
        "json_without_png": len({j.stem for j in jsons} - {p.stem for p in pngs}),
        "zero_byte_png": sum(1 for p in pngs if p.stat().st_size == 0),
        "distinct_4digit_seq": len({p.stem[:4] for p in pngs}),
        "extracted_repo_files": len(list((c / "extracted").rglob("*"))),
    }
    try:
        import openpyxl  # noqa: F401
        wb = openpyxl.load_workbook(c / "datasets.xlsx", read_only=True)
        R["csxa"]["xlsx_sheets"] = {ws.title: ws.max_row for ws in wb.worksheets}
    except Exception as e:  # noqa: BLE001
        R["csxa"]["xlsx_error"] = str(e)

    # ---------------- BUU ----------------
    b = RAW / "buu_full/BUU-LSPINEv1"
    buu = {}
    for view in ("AP", "LA"):
        files = sorted((b / view).iterdir())
        jpg = [f for f in files if f.suffix == ".jpg"]
        csvf = [f for f in files if f.suffix == ".csv"]
        dup = [f.name for f in files if "(1)" in f.name]
        ids = {re.match(r"(\d{4})", f.name).group(1) for f in jpg if re.match(r"\d{4}", f.name)}
        buu[view] = {"jpg": len(jpg), "csv": len(csvf), "dup_paren_files": dup,
                     "distinct_4digit_ids_jpg": len(ids),
                     "jpg_without_csv": sorted({f.stem for f in jpg} - {f.stem for f in csvf}),
                     "csv_without_jpg": sorted({f.stem for f in csvf} - {f.stem for f in jpg}),
                     "zero_byte": sum(1 for f in files if f.is_file() and f.stat().st_size == 0)}
    ap_ids = {re.match(r"(\d{4})", f.name).group(1) for f in (b / "AP").glob("*.jpg")}
    la_ids = {re.match(r"(\d{4})", f.name).group(1) for f in (b / "LA").glob("*.jpg")}
    buu["ids_AP_only"] = sorted(ap_ids - la_ids)
    buu["ids_LA_only"] = sorted(la_ids - ap_ids)
    buu["ids_both"] = len(ap_ids & la_ids)
    # buu_2000 and buu_v1: names vs buu_full
    for extra in ("buu_2000", "buu_v1"):
        e = RAW / extra
        if e.exists():
            names = {f.name for v in ("AP", "LA") for f in (e / v).glob("*") if f.is_file()}
            full = {f.name for v in ("AP", "LA") for f in (b / v).glob("*")}
            buu[extra] = {"files": len(names), "jpg": sum(1 for n in names if n.endswith(".jpg")),
                          "names_not_in_buu_full": len(names - full)}
    # KIOM report sheets
    try:
        import openpyxl
        wb = openpyxl.load_workbook(b / "KIOM2022_dataset_report.xlsx", read_only=True)
        buu["kiom_sheets"] = {ws.title: ws.max_row for ws in wb.worksheets}
    except Exception as e:  # noqa: BLE001
        buu["kiom_error"] = str(e)
    R["buu"] = buu

    # ---------------- NHANES ----------------
    n = RAW / "nhanes_full"
    tif = sorted(n.glob("*.tiff"))
    byv = Counter(f.name[0] for f in tif)
    ids = {f.name[1:6] for f in tif}
    small = [f.name for f in tif if f.stat().st_size < 100_000]
    pk = sorted((RAW / "nhanes_annotated/extracted/nhanes").glob("*.pkl"))
    pk_ids = set()
    pk_view = Counter()
    pk_unreadable = 0
    for p in pk:
        pk_view[p.name[0]] += 1
        try:
            with open(p, "rb") as fh:
                d = pickle.load(fh)
            sid = d.get("sample_id") if isinstance(d, dict) else None
            pk_ids.add(str(sid) if sid is not None else p.name[1:6])
        except Exception:  # noqa: BLE001
            pk_unreadable += 1
            pk_ids.add(p.name[1:6])
    pk_stems = {p.name[:6] for p in pk}
    tif_stems = {f.name[:6] for f in tif}
    R["nhanes"] = {
        "tiff": len(tif), "by_view": dict(byv), "distinct_persons_on_disk": len(ids),
        "files_under_100kB": small,
        "annotated_pkl": len(pk), "pkl_by_view": dict(pk_view), "pkl_distinct_sample_id": len(pk_ids),
        "pkl_unreadable": pk_unreadable,
        "pkl_without_tiff": sorted(pk_stems - tif_stems),
        "zip": [(z.name, z.stat().st_size) for z in (RAW / "nhanes_annotated").glob("*.zip")],
    }
    # CDC listing of the release, fetched from the compute node (internet); count C/L file names
    try:
        import urllib.request
        url = "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/nhanes/nhanes2/xray/"
        for u in (url, "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/nhanes/nhanes2/"):
            try:
                html = urllib.request.urlopen(u, timeout=60).read().decode("utf-8", "ignore")
                names = set(re.findall(r'href="([^"]+)"', html))
                R["nhanes"].setdefault("cdc_listing", {})[u] = {
                    "n_hrefs": len(names),
                    "tiff_hrefs": sorted(x for x in names if x.lower().endswith(".tiff") or x.lower().endswith(".tif"))[:5],
                    "n_tiff": sum(1 for x in names if x.lower().endswith((".tiff", ".tif"))),
                    "dirs": sorted(x for x in names if x.endswith("/"))[:40],
                }
            except Exception as e:  # noqa: BLE001
                R["nhanes"].setdefault("cdc_listing", {})[u] = f"error: {e}"
    except Exception as e:  # noqa: BLE001
        R["nhanes"]["cdc_listing_error"] = str(e)

    # ---------------- VinDr ----------------
    v = RAW / "vindr/1.0.0"
    tr = sorted((v / "train_images").glob("*.dicom"))
    te = sorted((v / "test_images").glob("*.dicom"))
    rows = {}
    for split in ("train", "test"):
        with open(v / f"annotations/{split}.csv", newline="") as fh:
            rd = list(csv.DictReader(fh))
        rows[split] = {"rows": len(rd), "images": len({r["image_id"] for r in rd}),
                       "studies": len({r["study_id"] for r in rd}), "cols": list(rd[0].keys()) if rd else []}
        rows[split]["images_in_csv_not_on_disk"] = len({r["image_id"] for r in rd} - {f.stem for f in (tr if split == "train" else te)})
    sums = {}
    if (v / "SHA256SUMS.txt").exists():
        for line in open(v / "SHA256SUMS.txt"):
            parts = line.split()
            if len(parts) >= 2:
                sums[parts[1].lstrip("*").split("/")[-1]] = parts[0]
    small = [f.name for f in tr + te if f.stat().st_size < 50_000]
    R["vindr"] = {"train_dicom": len(tr), "test_dicom": len(te), "csv": rows,
                  "sha256sums_entries": len(sums),
                  "dicom_on_disk_not_in_sums": len({f.name for f in tr + te} - set(sums)) if sums else None,
                  "sums_not_on_disk": len({s for s in sums if s.endswith(".dicom")} - {f.name for f in tr + te}) if sums else None,
                  "dicom_under_50kB": small[:20], "n_dicom_under_50kB": len(small)}
    # vindr_pseudo membership train/test
    vp = H / "vindr_pseudo/ann"
    if vp.exists():
        stems = {a.name[len("VINDRPS_"):-5] for a in vp.glob("VINDRPS_*.json")}
        trs = {f.stem for f in tr}
        tes = {f.stem for f in te}
        vmap_p = H / "spinesurg-ct-nnunet/tools/identity/vindr_image_to_study.json"
        studies = None
        if vmap_p.exists():
            vmap = json.load(open(vmap_p))
            studies = len({vmap[s] for s in stems if s in vmap})
        R["vindr"]["vindr_pseudo"] = {"anns": len(stems), "in_train": len(stems & trs), "in_test": len(stems & tes),
                                       "neither": len(stems - trs - tes), "distinct_studies": studies,
                                       "train_not_pseudolabelled": len(trs - stems), "test_not_pseudolabelled": len(tes - stems)}
    for d in ("vindr_pseudo_drr", "vindr_det_drr"):
        p = H / d / "ann"
        if p.exists():
            stems = set()
            for a in p.glob("*.json"):
                m = re.search(r"([0-9a-f]{32})", a.name)
                if m:
                    stems.add(m.group(1))
            R["vindr"][d] = {"anns": len(list(p.glob('*.json'))), "distinct_image_ids": len(stems),
                              "in_train": len(stems & {f.stem for f in tr}), "in_test": len(stems & {f.stem for f in te})}
    if (H / "vindr_pseudo_drr/ann").exists() and (H / "vindr_det_drr/ann").exists():
        a = {re.search(r"([0-9a-f]{32})", x.name).group(1) for x in (H / "vindr_pseudo_drr/ann").glob("*.json") if re.search(r"[0-9a-f]{32}", x.name)}
        b2 = {re.search(r"([0-9a-f]{32})", x.name).group(1) for x in (H / "vindr_det_drr/ann").glob("*.json") if re.search(r"[0-9a-f]{32}", x.name)}
        R["vindr"]["pseudo_drr_subset_of_det_drr"] = a <= b2
        R["vindr"]["pseudo_drr_minus_det_drr"] = len(a - b2)

    # ---------------- render dirs ----------------
    R["render_dirs"] = {d: drr_dir_summary(H / d) for d in
                        ("films_drr", "films_ap_drr", "nhanes_drr", "nhanes_pseudo", "vindr_pseudo",
                         "vindr_pseudo_drr", "vindr_det_drr", "films_drr_buucorr", "mendeley_drr")}
    for d in ("nhanes_pseudo_anchored", "vindr_pseudo_anchored", "lateral236_pseudo_anchored"):
        R["render_dirs"]["pseudo_filtered/" + d] = drr_dir_summary(H / "pseudo_filtered" / d)

    # ---------------- banks ----------------
    banks = ["allspine_v8_fov96_ctx", "allspine_v9_fov96_ctx", "vindrps_fov96_ctx", "vindr_fov96_ctx",
             "carm_mix_fov96_ctx", "allspine_v7_fov96_ctx", "allspine_v7nofluoro_fov96_ctx", "films_all2_fov96_ctx",
             "allspine_v3_fov96_ctx", "allspine_v4_fov96_ctx", "allspine_v6_fov96_ctx", "fluorocap_fov96_ctx",
             "buu_pair_fov48_ctx"]
    banks += [p.name for p in sorted(H.glob("carm_cv*_fov96_ctx"))]
    banks += [p.name for p in sorted(H.glob("carm_mix*_ctx"))]
    R["banks"] = {}
    for bname in dict.fromkeys(banks):
        R["banks"][bname] = bank_summary(H / bname)
    # or_ready fold banks, if any
    for p in sorted(Path("/rs/rs_grp_oschome/go2432/data/or_ready").glob("**/rung_1.npz")):
        if len(p.parts) < 12:
            R["banks"]["or_ready:" + str(p.parent)] = bank_summary(p.parent)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(R, open(args.out, "w"), indent=1, default=str)
    print(json.dumps(R, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
