#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/or_audit_splits.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Leakage and independence audit, part 1: split disjointness by case, and what every model saw.

Reads only. Writes one JSON under the audit directory. Every check is a count, never a judgement: the report
(tools/or_audit_report.py) turns the counts into tables and names the defects.

  (a) split disjointness by case: realxray datasets (splits.json vs meta case/split vs image directory),
      C-ArmLSpine crops and the crops+frames set (carmlspine_multi), the five CV folds (fold test cases vs the
      per-fold DRR bank anns, vs the per-fold context banks rung_1.npz), the C-ArmLSpine fine-tune banks vs the
      fixed test split, DeepFluoro specimens (test 18-1109 never in train/val).
  (c) the render-only detector anchor_none_v2_17-1882: which specimens' POSES its renders were drawn under, and
      which specimens' REAL frames fitted the calibration fold and the photon range it used; plus every
      leave-one-specimen-out arm's eval (the clean number to set beside the exposed one).
  (d) the film keypoint detector v5z: weight mtimes against the download dates of the real X-ray datasets, and
      the corpus that its data.yaml chain names.
  (e) the whole-spine level bank allspine_v7: source counts; any DeepFluoro pose renders or real C-arm frames.
  (f) the fine-tuned level banks carm_fov96_ctx / carm_mix / carm_cvmix{k}: cases vs the fixed test split and
      vs each fold's test cases.
  (g) pose quality from the metas alone (edge NCC per view); the detector-vs-truth offset is run separately
      with tools/carmlspine_pose_qc.py.

    python tools/or_audit_splits.py --out /rs/rs_grp_oschome/go2432/data/or_ready/audit/splits.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import re
from collections import Counter, defaultdict

import numpy as np

H = os.path.expanduser("~")
R = "/rs/rs_grp_oschome/go2432/data/realxray"
DF_SPECS = ["17-1882", "17-1905", "18-0725", "18-1109", "18-2799", "18-2800"]


def mtime(p):
    try:
        return dt.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")
    except OSError:
        return None


def fold_of(case, n=5):
    return int(hashlib.md5(case.encode()).hexdigest(), 16) % n


def npz_arrays(path, keys=("case", "split", "source")):
    """Only the small string members of a bank; X is never touched."""
    z = np.load(path, allow_pickle=False)
    out = {}
    for k in keys:
        if k in z.files:
            out[k] = np.array([str(v) for v in z[k]])
    return out


# ---------------------------------------------------------------- (a) realxray datasets
def audit_dataset(ds):
    root = os.path.join(R, ds)
    S = json.load(open(os.path.join(root, "splits.json")))
    case_split = {}
    dup_cases = []
    for s in ("train", "val", "test"):
        for c in S.get(s, []):
            if c in case_split:
                dup_cases.append((c, case_split[c], s))
            case_split[c] = s
    rows = []
    mism_meta_vs_splits = []
    img_missing = []
    for mp in sorted(glob.glob(os.path.join(root, "meta", "*.json"))):
        m = json.load(open(mp))
        stem = m.get("stem") or os.path.splitext(os.path.basename(mp))[0]
        case, sp = m["case"], m["split"]
        exp = case_split.get(case)
        if exp != sp:
            mism_meta_vs_splits.append((stem, case, sp, exp))
        if not os.path.exists(os.path.join(root, "images", sp, stem + ".png")):
            img_missing.append(stem)
        rows.append((stem, case, sp))
    stem_split = {st: sp for st, _, sp in rows}
    # images on disk whose meta names another split, or that have no meta
    img_wrong_dir, img_no_meta = [], []
    per_split_frames, per_split_cases = {}, {}
    for s in ("train", "val", "test"):
        stems = [os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(root, "images", s, "*.png"))]
        per_split_frames[s] = len(stems)
        for st in stems:
            if st not in stem_split:
                img_no_meta.append(st)
            elif stem_split[st] != s:
                img_wrong_dir.append((st, s, stem_split[st]))
        on_disk = set(stems)
        per_split_cases[s] = len({c for t, c, sp in rows if sp == s and t in on_disk})
    cases_by_split = {s: {c for _, c, sp in rows if sp == s} for s in ("train", "val", "test")}
    inter = {f"{a}&{b}": sorted(cases_by_split[a] & cases_by_split[b]) for a, b in (("train", "val"), ("train", "test"), ("val", "test"))}
    # pose quality straight from the metas
    ncc = defaultdict(list)
    for mp in glob.glob(os.path.join(root, "meta", "*.json")):
        m = json.load(open(mp))
        v = m.get("view")
        key = v if isinstance(v, str) else "all"
        e = (m.get("pose") or {}).get("edge_ncc", (m.get("pose") or {}).get("qc_edge_ncc"))
        if e is not None:
            ncc[key].append(float(e))
    ncc_summary = {k: dict(n=len(v), median=float(np.median(v)), p10=float(np.percentile(v, 10)), min=float(np.min(v)))
                   for k, v in ncc.items() if v}
    return dict(dataset=ds, n_meta=len(rows), frames_per_split=per_split_frames, cases_per_split=per_split_cases,
                cases_in_splits_json={s: len(S.get(s, [])) for s in ("train", "val", "test")},
                case_in_two_split_lists=dup_cases, meta_split_disagrees_with_splits_json=mism_meta_vs_splits[:50],
                n_meta_split_disagrees=len(mism_meta_vs_splits), image_missing_for_meta=img_missing[:20],
                n_image_missing=len(img_missing), image_in_wrong_split_dir=img_wrong_dir[:20], n_image_wrong_dir=len(img_wrong_dir),
                image_without_meta=img_no_meta[:20], n_image_without_meta=len(img_no_meta),
                cross_split_case_intersections=inter, n_cross_split_case_overlap=sum(len(v) for v in inter.values()),
                edge_ncc=ncc_summary, case_split=case_split)


def audit_carmlspine_derived(case_split):
    """Crops (carmlspine_crops/k*/<split>/meta) and the frames+crops detector set (carmlspine_multi, stems only)."""
    out = {}
    # crops
    bad, n, per_k = [], 0, {}
    for k in range(1, 6):
        for s in ("train", "val", "test"):
            for mp in glob.glob(os.path.join(R, "carmlspine_crops", f"k{k}", s, "meta", "*.json")):
                m = json.load(open(mp)); n += 1
                per_k[f"k{k}/{s}"] = per_k.get(f"k{k}/{s}", 0) + 1
                if case_split.get(m["case"]) != s or m.get("split", s) != s:
                    bad.append((os.path.basename(mp), m["case"], s, case_split.get(m["case"])))
    out["crops"] = dict(n=n, per_dir=per_k, n_wrong_split=len(bad), wrong=bad[:30])
    # multi
    pat = re.compile(r"^(case\d+)_(AP|LAT)")
    badm, cnt, unparsed = [], {}, []
    for s in ("train", "val", "test"):
        stems = [os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(R, "carmlspine_multi", "images", s, "*.png"))]
        cnt[s] = dict(images=len(stems), whole_frames=sum(1 for st in stems if "_k" not in st),
                      crops=sum(1 for st in stems if "_k" in st), cases=len({pat.match(st).group(1) for st in stems if pat.match(st)}))
        for st in stems:
            mm = pat.match(st)
            if not mm:
                unparsed.append(st); continue
            if case_split.get(mm.group(1)) != s:
                badm.append((st, s, case_split.get(mm.group(1))))
    out["multi"] = dict(per_split=cnt, n_wrong_split=len(badm), wrong=badm[:30], n_unparsed=len(unparsed), unparsed=unparsed[:10])
    return out


def audit_cv_folds(case_split):
    """Fold k's test cases (md5 rule) against the per-fold DRR bank anns and the per-fold context banks."""
    all_cases = sorted(case_split)
    out = {}
    for k in range(5):
        fold_cases = {c for c in all_cases if fold_of(c) == k}
        # the symlinked fold view
        view_cases = set()
        for mp in glob.glob(os.path.join(R, "carmlspine_cv", f"fold{k}", "kfull", "meta", "*.json")):
            view_cases.add(json.load(open(mp))["case"])
        # DRR bank anns
        ann_pat, ann_split, ann_bad_rule = set(), Counter(), []
        for ap in glob.glob(os.path.join(H, f"carm_cv{k}_drr", "ann", "*.json")):
            a = json.load(open(ap)); pid = a.get("patient_id") or a.get("case", "").split("_")[0]
            ann_pat.add(pid); ann_split[a.get("split")] += 1
            exp = "test" if fold_of(pid) == k else ("val" if fold_of(pid) == (k + 1) % 5 else "train")
            if a.get("split") != exp:
                ann_bad_rule.append((os.path.basename(ap), a.get("split"), exp))
        row = dict(fold=k, n_fold_cases=len(fold_cases), fold_view_cases=len(view_cases),
                   fold_view_equals_rule=(view_cases == fold_cases), view_minus_rule=sorted(view_cases - fold_cases),
                   rule_minus_view=sorted(fold_cases - view_cases),
                   drr_ann_patients=len(ann_pat), drr_ann_splits=dict(ann_split),
                   drr_ann_in_fold_test=sorted(ann_pat & fold_cases), n_drr_ann_split_rule_violations=len(ann_bad_rule),
                   drr_ann_split_rule_violations=ann_bad_rule[:10])
        for bank in (f"carm_cv{k}_fov96_ctx", f"carm_cvmix{k}_fov96_ctx"):
            p = os.path.join(H, bank, "rung_1.npz")
            if not os.path.exists(p):
                row[bank] = None; continue
            z = npz_arrays(p)
            pats = np.array([c.split("_")[0] for c in z["case"]])
            real = np.array([s.startswith("carm") for s in z.get("source", np.array(["carm"] * len(pats)))])
            row[bank] = dict(n=int(len(pats)), n_real=int(real.sum()), splits=dict(Counter(z["split"].tolist())),
                             source_counts=dict(Counter(z.get("source", np.array([])).tolist())) if "source" in z else None,
                             real_patients=int(len(set(pats[real]))),
                             real_patients_in_fold_test=sorted(set(pats[real]) & fold_cases),
                             n_real_crops_in_fold_test=int(np.isin(pats, list(fold_cases))[real].sum()))
        out[f"fold{k}"] = row
    return out


def audit_carm_banks(case_split):
    test = {c for c, s in case_split.items() if s == "test"}
    val = {c for c, s in case_split.items() if s == "val"}
    out = {}
    for bank in ("carm_fov96_ctx", "carm_mix_fov96_ctx"):
        p = os.path.join(H, bank, "rung_1.npz")
        if not os.path.exists(p):
            out[bank] = None; continue
        z = npz_arrays(p)
        pats = np.array([c.split("_")[0] for c in z["case"]])
        src = z.get("source", np.array(["?"] * len(pats)))
        real = np.array([s.startswith("carm") for s in src])
        rp = set(pats[real])
        out[bank] = dict(n=int(len(pats)), n_real=int(real.sum()), splits=dict(Counter(z["split"].tolist())),
                         source_counts=dict(Counter(src.tolist())), real_patients=len(rp),
                         real_patients_in_fixed_test=sorted(rp & test), real_val_patients=len(rp & val),
                         real_split_by_patient=dict(Counter(f"{case_split.get(pp, '?')}->{ss}" for pp, ss in zip(pats[real], z["split"][real]))),
                         meta=json.load(open(os.path.join(H, bank, "meta.json"))).get("mixed_from"))
    return out


def audit_deepfluoro():
    root = os.path.join(R, "deepfluoro")
    S = json.load(open(os.path.join(root, "splits.json")))
    per = {}
    for s in ("train", "val", "test"):
        c = Counter(os.path.basename(p).split("_")[0] for p in glob.glob(os.path.join(root, "images", s, "*.png")))
        per[s] = dict(c)
    test_spec = S["test"]
    leak = {s: {k: v for k, v in per[s].items() if k in test_spec} for s in ("train", "val")}
    return dict(splits={k: S[k] for k in ("train", "val", "test")}, frames_per_specimen_per_split=per,
                test_specimen_frames_in_train_or_val=leak, n_leak=sum(sum(v.values()) for v in leak.values()))


# ---------------------------------------------------------------- (c) render-only detector
def audit_render_detector(name="anchor_none_v2_17-1882"):
    root = os.path.join(H, "model_night", name)
    pat = re.compile(r"^(s\d+)_\d+_(\d{2}-\d{4})-(\d+)\.jpg$")
    out = dict(name=name, root=root, weights=os.path.join(H, "spine-detector", "runs", "pose", name, "weights", "best.pt"),
               weights_mtime=mtime(os.path.join(H, "spine-detector", "runs", "pose", name, "weights", "best.pt")))
    for s in ("train", "val"):
        specs, subjects, pids = Counter(), set(), set()
        for p in glob.glob(os.path.join(root, "images", s, "*.jpg")):
            m = pat.match(os.path.basename(p))
            if m:
                subjects.add(m.group(1)); specs[m.group(2)] += 1; pids.add((m.group(2), m.group(3)))
        out[s] = dict(n=sum(specs.values()), renders_per_pose_specimen=dict(specs), distinct_poses=len(pids),
                      distinct_poses_per_specimen=dict(Counter(sp for sp, _ in pids)), synthetic_subjects=len(subjects))
    rt = glob.glob(os.path.join(root, "real_test", "*.jpg"))
    out["real_test"] = dict(n=len(rt), specimens=dict(Counter(os.path.basename(p).split("_")[0] for p in rt)))
    # calibration fold actually used
    cal = json.load(open(os.path.join(H, "model_night", "deepfluoro", "calibration_best.json")))
    held = name.split("_")[-1]
    fold = next((f for f in cal["folds"] if f.get("held") == held), None)
    df_frames = json.load(open(os.path.join(R, "deepfluoro", "splits.json"))).get("frames", {})
    out["calibration"] = dict(file="~/model_night/deepfluoro/calibration_best.json", held=held,
                              fold_found=fold is not None, n_held_frames=fold["n"] if fold else None,
                              theta=fold["theta"] if fold else None,
                              real_frames_that_fitted_theta={s: df_frames.get(s) for s in DF_SPECS if s != held},
                              n_real_frames_that_fitted_theta=sum(df_frames.get(s, 0) for s in DF_SPECS if s != held))
    pj = os.path.join(H, "model_night", "deepfluoro", "photons_folds.json")
    if os.path.exists(pj):
        P = json.load(open(pj))
        rows = [r for r in P.get("rows", []) if r.get("fold") == held]
        out["photons"] = dict(file=pj, rows_under_fold=len(rows), specimens=dict(Counter(r["spec"] for r in rows)))
    # every LOSO arm's eval: the clean number per specimen (seeds 0,1,2)
    loso = {}
    for spec in DF_SPECS:
        for seed in ("", "_s1", "_s2"):
            p = os.path.join(H, "model_night", f"anchor_none_v2_{spec}", f"eval_anchor_none_v2_{spec}{seed}.json")
            if os.path.exists(p):
                e = json.load(open(p))
                loso[f"{spec}{seed}"] = {c: dict(sacrum_recall=v["sacrum_recall"], anchor_called=v["anchor_called"],
                                                  false_sacrum_per_frame=v["false_sacrum_per_frame"], n=v["n_sacrum"]) for c, v in e.items()}
    out["loso_evals"] = loso
    return out


# ---------------------------------------------------------------- real-fine-tuned detectors (lineage)
def audit_rx_runs():
    import yaml
    out = {}
    for d in sorted(glob.glob(os.path.join(H, "spine-detector", "runs", "realxray", "rx_*"))):
        y = os.path.join(d, "data.yaml"); a = os.path.join(d, "args.yaml")
        row = dict(name=os.path.basename(d), best_mtime=mtime(os.path.join(d, "weights", "best.pt")),
                   has_best=os.path.exists(os.path.join(d, "weights", "best.pt")))
        if os.path.exists(y):
            Y = yaml.safe_load(open(y))
            row["train"] = [p.replace(R + "/", "") for p in (Y.get("train") or [])]
            row["val"] = [p.replace(R + "/", "") for p in (Y.get("val") or [])]
        if os.path.exists(a):
            A = yaml.safe_load(open(a)); row["init"] = A.get("model"); row["imgsz"] = A.get("imgsz"); row["epochs"] = A.get("epochs")
        sc = os.path.join(d, "scores.json")
        if os.path.exists(sc):
            S = json.load(open(sc))
            row["scores"] = {k: dict(frames=v["frames"], sacrum_recall=v["sacrum"]["recall"], sacrum_ap50=v["sacrum"]["ap50"],
                                     vertebra_recall=v["vertebra"]["recall"], naming_accuracy=v["naming"]["accuracy"],
                                     naming_coverage=v["naming"]["coverage"]) for k, v in S.get("results", {}).items()}
        out[row["name"]] = row
    return out


# ---------------------------------------------------------------- (d) film detector v5z
def audit_film_detector():
    out = dict(registry=[], weights={}, corpus={}, downloads={})
    reg = os.path.join(H, "model_registry", "registry.jsonl")
    if os.path.exists(reg):
        for ln in open(reg):
            if "v5z" in ln:
                j = json.loads(ln); out["registry"].append({k: j.get(k) for k in ("ts", "name", "file", "source_path", "git", "note")})
    for p in glob.glob(os.path.join(H, "FluoroCap", "detect_v5z*.pt")):
        out["weights"][os.path.basename(p)] = mtime(p)
    for ds in ("yolo_v3", "yolo_v4z", "yolo_v5f_p00", "yolo_v6f"):
        d = os.path.join(H, "spine-detector", "data", ds)
        if not os.path.isdir(d):
            continue
        row = dict(data_yaml_mtime=mtime(os.path.join(d, "data.yaml")))
        try:
            import yaml
            row["train_dirs"] = yaml.safe_load(open(os.path.join(d, "data.yaml"))).get("train")
        except Exception as e:  # noqa
            row["train_dirs"] = str(e)
        pref, sus = Counter(), []
        for s in ("train", "val", "test"):
            for p in glob.glob(os.path.join(d, "images", s, "*")):
                b = os.path.basename(p); pref[b.split("_")[0]] += 1
                if re.search(r"deepfluoro|cobra|carm|geneva|1[78]-\d{4}|surgio|pulsera", b, re.I):
                    sus.append(b)
        row["source_prefix_counts"] = dict(pref); row["n_stems_naming_a_test_dataset"] = len(sus); row["examples"] = sus[:10]
        out["corpus"][ds] = row
    for name, p in (("deepfluoro_h5", os.path.join(H, "deepfluoro", "unpacked_full", "ipcai_2020_full_res_data.h5")),
                    ("deepfluoro_dir", os.path.join(H, "deepfluoro")), ("realxray_deepfluoro", os.path.join(R, "deepfluoro", "splits.json")),
                    ("realxray_carmlspine", os.path.join(R, "carmlspine", "splits.json")), ("realxray_cobra", os.path.join(R, "cobra_elekta", "splits.json")),
                    ("realxray_geneva", os.path.join(R, "geneva_hip", "splits.json")),
                    ("carmlspine_zip", "/rs/rs_grp_oschome/go2432/data/carmlspine/C-ArmLSpine.zip"),
                    ("cobra_src", "/rs/rs_grp_oschome/go2432/data/cobra2026"), ("geneva_src", "/rs/rs_grp_oschome/go2432/data/geneva_hip_src")):
        out["downloads"][name] = mtime(p)
    return out


# ---------------------------------------------------------------- (e) whole-spine level bank
def audit_allspine():
    out = {}
    for bank in ("allspine_v7_fov96_ctx", "fluorocap_fov96_ctx", "vindrps_fov96_ctx"):
        p = os.path.join(H, bank, "rung_1.npz")
        if not os.path.exists(p):
            out[bank] = None; continue
        z = npz_arrays(p)
        src = z.get("source", np.array([]))
        cases = z["case"]
        sus = Counter()
        for c in cases:
            m = re.search(r"deepfluoro|physics|1[78]-\d{4}|carm|cobra|geneva|surgio|cios", c, re.I)
            if m:
                sus[m.group(0).lower()] += 1
        row = dict(n=int(len(cases)), source_counts=dict(Counter(src.tolist())) if len(src) else None,
                   splits=dict(Counter(z["split"].tolist())) if "split" in z else None,
                   case_name_hits=dict(sus), distinct_cases=int(len(set(cases.tolist()))), example_cases=sorted(set(cases.tolist()))[:5])
        try:
            meta = json.load(open(os.path.join(H, bank, "meta.json")))
            row["merged_from"] = meta.get("merged_from"); row["n_val_cases"] = len(meta.get("val_cases", []))
        except Exception:
            pass
        out[bank] = row
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    A = {"generated": dt.datetime.now().isoformat(timespec="seconds"), "datasets": {}}
    for ds in ("carmlspine", "cobra_elekta", "deepfluoro", "geneva_hip"):
        A["datasets"][ds] = audit_dataset(ds); print(f"{ds}: {A['datasets'][ds]['frames_per_split']} overlap={A['datasets'][ds]['n_cross_split_case_overlap']}", flush=True)
    cs = A["datasets"]["carmlspine"]["case_split"]
    A["carmlspine_derived"] = audit_carmlspine_derived(cs); print("derived done", flush=True)
    A["cv_folds"] = audit_cv_folds(cs); print("cv folds done", flush=True)
    A["carm_banks"] = audit_carm_banks(cs); print("carm banks done", flush=True)
    A["deepfluoro_specimens"] = audit_deepfluoro()
    A["render_detector"] = audit_render_detector(); print("render detector done", flush=True)
    A["rx_runs"] = audit_rx_runs()
    A["film_detector"] = audit_film_detector(); print("film detector done", flush=True)
    A["allspine"] = audit_allspine(); print("allspine done", flush=True)
    for ds in A["datasets"].values():
        ds.pop("case_split", None)
    json.dump(A, open(a.out, "w"), indent=1, default=str)
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
