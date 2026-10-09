#!/usr/bin/env python3
"""Build or refresh the SQLite index of the imaging holding (schema: SCHEMA.sql). Python 3.6+, standard library;
pydicom is used when importable (DICOM headers), and tools/patient_keys.py when it is on the path (subject keys).

It walks the CephFS layout one source folder at a time. A folder is indexed only when it holds a README.yaml (written
at cut-over from data_platform/plan/readme_yaml/), and the README names the adapter that reads it:

  ctsp_manifest   CTSpinoPelvic1K: manifest.json records (position, scanner, LSTV fields), labels v11 / v10, 5-fold splits
  acquisition     acquisition collections: ../anomaly_harvest/<collection>/cases.csv (patient keys) and rows.csv (calls)
  vindr_csv       VinDr-SpineXR: annotations/{train,test}.csv (study_id, lesion boxes)
  buu             BUU-LSPINE: AP/LA jpg + csv end-plate lines; view from the file name
  nhanes_tiff     NHANES II CDC films [CL]#####.tiff
  nhanes_pickle   NHANES II Zenodo landmark pickles
  csxa            CSXA png + labelme json
  realxray_meta   the real-frame banks: meta/<stem>.json (device, kVp, px_mm, view angles, boxes, split)
  cobra           COBRA2026 cases/<case>/ (projections sweep, planning CT, CBCT; metadata.yaml dates)
  totalsegmentator  s####/ct.nii.gz + segmentations/ + meta.csv
  verse           VerSe / VerSeFusion NIfTI and vertebra masks
  dicom_tree      DICOM directories (a series directory per CT/CBCT, a file per projection)
  render_bank     ann/*.json + img/*.npy banks and *_ctx crop banks (also run on every <folder>/derived/*)
  generic         any other folder: files classified by extension; mask-named volumes (_seg, _msk, _mask, label,
                  segmentation, labelsTr ...) attach to their image as annotation rows; with no file-level label the
                  item carries the release's annotation status from sources.json, marked per-release

A README.yaml may list `index_skip` (sub-paths not indexed, such as a duplicate HOME copy). A file that is a hard link
of an item already indexed is recorded with duplicate_of and counted = 0; conversions and derived outputs that sit
beside a release (tcia_nifti, C-ArmLSpine nifti/, spineps/) are kept with counted = 0, so the views count each
acquisition once.

Incremental: an item whose (size, mtime) is unchanged is not re-read; items that vanished from a folder that was
walked completely are removed. Re-running is cheap.

    sbatch -D ~/spinesurg-ct-nnunet/data_platform/db build_index.sbatch                 # the whole layout
    python3 build_index.py --root /rs/rs_grp_oschome/go2432/data --db <db> --folders ctspinopelvic1k vindr_spinexr
    python3 build_index.py --root <tree> --db test.sqlite --allow-local                  # off the grid (tests)
"""
import argparse
import csv
import datetime
import glob
import hashlib
import json
import os
import re
import socket
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DPROOT = os.path.dirname(HERE)
REPO = os.path.dirname(DPROOT)
sys.path.insert(0, os.path.join(DPROOT, "lib"))
import mini_yaml  # noqa: E402

try:                                    # the project's person-key rules (tools/patient_keys.py)
    sys.path.insert(0, os.path.join(REPO, "tools"))
    import patient_keys as _pk          # noqa: E402
except Exception:                       # noqa: BLE001  (absent off the repo checkout: a local fallback applies)
    _pk = None

try:
    import pydicom                      # noqa: F401
except Exception:                       # noqa: BLE001
    pydicom = None

DEFAULT_ROOT = "/rs/rs_grp_oschome/go2432/data"
VOL_EXT = (".nii.gz", ".nii", ".mha", ".mhd", ".nrrd")
IMG_EXT = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")
DCM_EXT = (".dcm", ".dicom")
ARC_EXT = (".zip", ".tar", ".tar.gz", ".tgz", ".tar.zst")
MODALITY_ENUM = ("CT", "CBCT", "CR", "DX", "RF", "XA", "MR", "RENDER", "OTHER")
ANN_KINDS = ("none", "release_labels", "pseudo", "two_labeller", "expert", "reviewed", "unknown")
MASK_TOKENS = r"seg|segmentation|segmentations|msk|mask|masks|label|labels|gt"
MASK_RX = re.compile(r"(?:^|[_\-.])(?:%s)(?:[_\-.]|$)" % MASK_TOKENS, re.I)
MASK_STRIP = re.compile(r"[_\-.]?(?:%s)(?:[_\-.].*)?$" % MASK_TOKENS, re.I)
MASK_DIRS = {"labels", "labelstr", "labelsts", "segmentations", "masks", "seg", "gt", "label"}
SIDECAR_EXT = (".json", ".mat", ".txt", ".csv", ".xml")


# ------------------------------------------------------------------------------------------------ small helpers
def now():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def ext_of(name):
    n = name.lower()
    for e in VOL_EXT + ARC_EXT + DCM_EXT + IMG_EXT + (".npy", ".npz", ".h5", ".hdf5", ".pkl", ".json", ".csv", ".txt"):
        if n.endswith(e):
            return e
    return os.path.splitext(n)[1]


def fmt_of(name):
    e = ext_of(name)
    return {".nii.gz": "nifti", ".nii": "nifti", ".mha": "mha", ".mhd": "mha", ".nrrd": "nrrd", ".dcm": "dicom",
            ".dicom": "dicom", ".png": "png", ".jpg": "jpg", ".jpeg": "jpg", ".tif": "tiff", ".tiff": "tiff", ".bmp": "bmp",
            ".npy": "npy", ".npz": "npz", ".h5": "h5", ".hdf5": "h5", ".pkl": "pkl"}.get(e, "archive" if e in ARC_EXT else e.lstrip("."))


def canon(key):
    if not key:
        return None
    if _pk is not None:
        try:
            return _pk.canon_key(key)
        except Exception:               # noqa: BLE001
            pass
    corpus, _, person = str(key).partition(":")
    if not person:
        return None
    if corpus == "ctsp" and person.isdigit():
        person = person.zfill(4)
    if corpus == "nhanes" and person.isdigit():
        person = str(int(person)).zfill(5)
    return "%s:%s" % ({"totalseg": "ts", "case": "carmlspine", "gl": "verse"}.get(corpus, corpus), person)


def view_from_angle(lat_from_ap):
    try:
        a = abs(float(lat_from_ap))
    except (TypeError, ValueError):
        return "unknown"
    return "AP" if a <= 20 else "LAT" if a >= 70 else "OBL"


def prefix_range(folder):
    """(lo, hi) so that lo <= path < hi selects every path strictly below folder (separator-aware, index-friendly)."""
    sep = os.sep
    base = folder.rstrip("/").rstrip(sep)
    return base + sep, base + chr(ord(sep) + 1)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_csv(p):
    with open(p, encoding="utf-8", errors="replace", newline="") as fh:
        return list(csv.DictReader(fh))


def walk_files(root, exts=None):
    for dp, dn, fn in os.walk(root, followlinks=False):
        dn.sort()
        for f in sorted(fn):
            if exts is None or ext_of(f) in exts:
                yield os.path.join(dp, f)


# ------------------------------------------------------------------------------------------------ the writer
class Indexer(object):
    def __init__(self, db, root, hash_mode="none", verbose=False):
        self.db = db
        self.root = root.rstrip("/")
        self.hash_mode = hash_mode
        self.verbose = verbose
        self.run_id = None
        self.counts = dict(new=0, updated=0, unchanged=0, removed=0)
        self.sources = {}
        self.ann_status = {}
        self.skip = ()                  # absolute sub-paths of the current folder that README.yaml index_skip names

    def start(self, notes=""):
        cur = self.db.execute("INSERT INTO index_run(started, root, host, slurm_job, notes) VALUES (?,?,?,?,?)",
                              (now(), self.root, socket.gethostname(), os.environ.get("SLURM_JOB_ID", ""), notes))
        self.run_id = cur.lastrowid
        self.sources = {r[0]: r for r in self.db.execute("SELECT source_id, modality, restricted FROM source")}
        self.ann_status = {r[0]: json.loads(r[1] or "[]") for r in self.db.execute("SELECT source_id, annotation_status FROM source")}

    def finish(self):
        c = self.counts
        self.db.execute("UPDATE index_run SET finished=?, n_new=?, n_updated=?, n_unchanged=?, n_removed=? WHERE run_id=?",
                        (now(), c["new"], c["updated"], c["unchanged"], c["removed"], self.run_id))
        self.db.commit()

    def subject(self, key, rule="", sex=None, age_band=None):
        key = canon(key)
        if not key:
            return None
        corpus, _, person = key.partition(":")
        self.db.execute("INSERT OR IGNORE INTO subject(subject_key, corpus, person, key_rule) VALUES (?,?,?,?)",
                        (key, corpus, person, rule))
        if sex or age_band:
            self.db.execute("UPDATE subject SET sex=COALESCE(sex, ?), age_band=COALESCE(age_band, ?) WHERE subject_key=?",
                            (sex, age_band, key))
        return key

    def stat(self, path):
        """(bytes, mtime) of a file, or of a directory as the sum / max over its files."""
        if os.path.isdir(path):
            b, m = 0, 0.0
            for p in walk_files(path):
                try:
                    st = os.stat(p)
                except OSError:
                    continue
                b += st.st_size
                m = max(m, st.st_mtime)
            return b, m
        st = os.stat(path)
        return st.st_size, st.st_mtime

    def skipped(self, path):
        return any(path == s or path.startswith(s.rstrip(os.sep) + os.sep) for s in self.skip)

    def item(self, rec, annotations=(), splits=(), lineage=()):
        """Insert or refresh one item; returns item_id. Unchanged items (same size and mtime) are only touched."""
        path = rec["path"]
        if self.skipped(path):
            return None
        try:
            size, mtime = self.stat(path)
        except OSError:
            return None
        inode, dup = None, None
        if os.path.isfile(path):
            st = os.stat(path)
            if st.st_nlink > 1:         # a hard link of a file indexed under another path counts once
                inode = "%d:%d" % (st.st_dev, st.st_ino)
                r0 = self.db.execute("SELECT item_id FROM item WHERE inode=? AND path<>? AND duplicate_of IS NULL ORDER BY item_id LIMIT 1",
                                     (inode, path)).fetchone()
                dup = r0[0] if r0 else None
        row = self.db.execute("SELECT item_id, bytes, mtime FROM item WHERE path=?", (path,)).fetchone()
        if row and row[1] == size and abs((row[2] or 0) - mtime) < 1e-6 and not rec.get("force"):
            self.db.execute("UPDATE item SET run_id=? WHERE item_id=?", (self.run_id, row[0]))
            self.counts["unchanged"] += 1
            return row[0]
        sha = None
        if self.hash_mode == "all" or (self.hash_mode == "small" and size < (64 << 20)):
            sha = sha256_file(path) if os.path.isfile(path) else None
        mod = rec.get("modality") or "OTHER"
        if mod not in MODALITY_ENUM:
            mod = "OTHER"
        vals = dict(source_id=rec["source_id"], subject_key=rec.get("subject_key"), case_id=rec.get("case_id"), modality=mod,
                    body_region=rec.get("body_region"), position=rec.get("position") or "unknown", view=rec.get("view") or "unknown",
                    device=rec.get("device"), px_mm=rec.get("px_mm"), spacing=rec.get("spacing"), extent=rec.get("extent"),
                    acquisition_date=rec.get("acquisition_date"), path=path, role=rec.get("role"), format=rec.get("format") or fmt_of(path),
                    bytes=size, mtime=mtime, sha256=sha, series_uid=rec.get("series_uid"), adapter=rec.get("adapter"),
                    extra=json.dumps(rec.get("extra") or {}, sort_keys=True), run_id=self.run_id,
                    inode=inode, duplicate_of=dup, counted=0 if (dup or rec.get("counted") == 0) else 1)
        if vals["position"] not in ("supine", "prone", "standing", "decubitus", "unknown"):
            vals["position"] = "unknown"
        if vals["view"] not in ("AP", "PA", "LAT", "OBL", "sweep", "volume", "unknown"):
            vals["view"] = "unknown"
        cols = list(vals.keys())
        if row:
            self.db.execute("UPDATE item SET %s WHERE item_id=?" % ", ".join("%s=?" % c for c in cols), [vals[c] for c in cols] + [row[0]])
            iid = row[0]
            self.db.execute("DELETE FROM annotation WHERE item_id=?", (iid,))
            self.db.execute("DELETE FROM split WHERE item_id=?", (iid,))
            self.db.execute("DELETE FROM lineage WHERE derived_item_id=?", (iid,))
            self.counts["updated"] += 1
        else:
            cur = self.db.execute("INSERT INTO item(%s) VALUES (%s)" % (", ".join(cols), ", ".join("?" * len(cols))), [vals[c] for c in cols])
            iid = cur.lastrowid
            self.counts["new"] += 1
        for a in annotations or [dict(kind="none")]:
            self.db.execute("INSERT OR IGNORE INTO annotation(item_id, kind, labeller, version, path, status, detail) VALUES (?,?,?,?,?,?,?)",
                            (iid, a["kind"], a.get("labeller", ""), a.get("version", ""), a.get("path", ""), a.get("status"),
                             json.dumps(a.get("detail") or {}, sort_keys=True)))
        for s in splits:
            self.db.execute("INSERT OR REPLACE INTO split(experiment, item_id, part, source_file) VALUES (?,?,?,?)",
                            (s["experiment"], iid, s["part"], s.get("source_file")))
        if dup:
            lineage = list(lineage) + [dict(source_ref=self.db.execute("SELECT path FROM item WHERE item_id=?", (dup,)).fetchone()[0],
                                            relation="copy_of", tool="hard link (same inode)")]
        for l in lineage:
            ref = l.get("source_ref")
            if not ref:
                continue
            src = self.db.execute("SELECT item_id FROM item WHERE path=?", (ref,)).fetchone()
            self.db.execute("INSERT OR REPLACE INTO lineage(derived_item_id, source_ref, source_item_id, relation, tool) VALUES (?,?,?,?,?)",
                            (iid, ref, src[0] if src else None, l.get("relation"), l.get("tool")))
        return iid

    def remove_unseen(self, folder):
        lo, hi = prefix_range(folder)
        n = self.db.execute("DELETE FROM item WHERE path >= ? AND path < ? AND (run_id IS NULL OR run_id <> ?)", (lo, hi, self.run_id)).rowcount
        self.counts["removed"] += max(n, 0)
        # a hard-link copy whose original vanished becomes the counted item
        self.db.execute("UPDATE item SET counted=1, duplicate_of=NULL WHERE duplicate_of IS NOT NULL "
                        "AND duplicate_of NOT IN (SELECT item_id FROM item)")
        return n


# ------------------------------------------------------------------------------------------------ adapters
def src_modality(ix, sid, default="OTHER"):
    row = ix.sources.get(sid)
    if not row:
        return default
    mods = json.loads(row[1] or "[]")
    for m in mods:
        if m in MODALITY_ENUM:
            return m
    return default


def source_modalities(ix, sid):
    row = ix.sources.get(sid)
    return [m for m in json.loads(row[1] or "[]")] if row else []


def volume_modality(ix, sid, path):
    """What a volume file of this source is: CBCT when the path says so, else the first volume modality the source holds."""
    if "cbct" in path.lower():
        return "CBCT"
    mods = source_modalities(ix, sid)
    for m in ("CT", "CBCT", "MR", "RENDER"):
        if m in mods:
            return m
    return "OTHER"


def stem_of(p):
    b = os.path.basename(p)
    for e in VOL_EXT + IMG_EXT + DCM_EXT:
        if b.lower().endswith(e):
            return b[:-len(e)]
    return os.path.splitext(b)[0]


def is_mask(p):
    parts = [x.lower() for x in p.replace("\\", "/").split("/")[:-1]]
    return bool(MASK_RX.search(stem_of(p))) or any(x in MASK_DIRS for x in parts[-3:])


def mask_key(p):
    return MASK_STRIP.sub("", stem_of(p)).lower()


def image_key(p):
    """The case stem of an image: without an nnU-Net channel suffix (_0000) or an image-kind suffix (_ct, _img ...)."""
    return re.sub(r"[_\-](?:0000|ct|cbct|img|image|vol|volume)$", "", stem_of(p), flags=re.I).lower()


def release_default(ix, sid):
    """The source's annotation status from sources.json, as an annotation row marked per-release (not read from a file)."""
    st = [s for s in ix.ann_status.get(sid, []) if s in ANN_KINDS]
    kind = st[0] if st else "unknown"
    return dict(kind=kind, labeller="per-release status (sources.json annotation.status)",
                detail=dict(scope="per-release, not read from the file", statuses=ix.ann_status.get(sid, [])))


def adapter_generic(ix, folder, readme, sid, role_hint=None, skip_dirs=("derived",), exts=None, counted=1, note=None):
    mod = src_modality(ix, sid)
    files = []
    for p in walk_files(folder, exts):
        rel = os.path.relpath(p, folder)
        if rel.split(os.sep)[0] in skip_dirs or os.path.basename(p) == "README.yaml" or os.path.islink(p):
            continue
        files.append(p)
    vols = [p for p in files if ext_of(p) in VOL_EXT]
    masks = [p for p in vols if is_mask(p)]
    images = [p for p in vols if p not in set(masks)]
    by_key = {}
    for p in images:
        by_key.setdefault(image_key(p), []).append(p)
    mask_of = {}
    orphan_masks = []
    for m in masks:
        hits = by_key.get(mask_key(m), [])
        same_dir = [h for h in hits if os.path.dirname(h) == os.path.dirname(m)]
        for h in (same_dir or hits):
            mask_of.setdefault(h, []).append(m)
        if not hits:
            orphan_masks.append(m)
    default = release_default(ix, sid)
    file_kind = default["kind"] if default["kind"] not in ("none", "unknown", "two_labeller") else "release_labels"
    folder_has_masks = bool(masks)

    def role_of(p):
        top = os.path.relpath(p, folder).split(os.sep)[0]
        return role_hint or (top if top in ("raw", "converted", "derived", "labels", "meta") else "raw")

    extra = dict(note=note) if note else {}
    for p in images:
        if p in mask_of:
            ann = [dict(kind=file_kind, labeller="mask file matched to the image by name", path=m,
                        detail=dict(scope="per-file", release_statuses=default["detail"]["statuses"])) for m in mask_of[p][:4]]
        elif folder_has_masks:
            ann = [dict(kind="none", detail=dict(note="this release folder holds masks, none matched this image by name"))]
        else:
            ann = [default]
        ix.item(dict(path=p, source_id=sid, modality=volume_modality(ix, sid, p), view="volume", role=role_of(p), adapter="generic",
                     counted=counted, extra=extra), annotations=ann)
    for m in orphan_masks:                       # a mask with no image beside it: kept as a labels item, never counted
        ix.item(dict(path=m, source_id=sid, modality=volume_modality(ix, sid, m), view="volume", role="labels", adapter="generic",
                     counted=0, extra=dict(note="mask file with no image matched by name")), annotations=[dict(kind=file_kind, path=m)])
    stems = {}
    for p in files:
        if ext_of(p) in SIDECAR_EXT:
            stems.setdefault((os.path.dirname(p), stem_of(p)), []).append(p)
    for p in files:
        e = ext_of(p)
        if e in IMG_EXT or e in DCM_EXT:
            side = stems.get((os.path.dirname(p), stem_of(p)))
            if side:
                k = default["kind"] if default["kind"] not in ("none", "two_labeller") else "unknown"
                ann = [dict(kind=k, labeller="sidecar file with the image's name", path=side[0],
                            detail=dict(scope="per-file", release_statuses=default["detail"]["statuses"]))]
            else:
                ann = [default]
            ix.item(dict(path=p, source_id=sid, modality=mod, role=role_of(p), adapter="generic", counted=counted, extra=extra), annotations=ann)
        elif e in ARC_EXT or e in (".h5", ".hdf5"):
            ix.item(dict(path=p, source_id=sid, modality=mod, role="raw", adapter="generic", counted=counted, extra=extra), annotations=[default])


def adapter_ctsp_manifest(ix, folder, readme, sid):
    mans = sorted(glob.glob(os.path.join(folder, "**", "manifest.json"), recursive=True))
    mans = [m for m in mans if os.path.isfile(os.path.join(os.path.dirname(m), "splits_5fold.json")) or os.path.isdir(os.path.join(os.path.dirname(m), "ct"))]
    for man in mans:
        base = os.path.dirname(man)
        recs = json.load(open(man, encoding="utf-8"))
        folds = {}
        sp = os.path.join(base, "splits_5fold.json")
        if os.path.isfile(sp):
            sj = json.load(open(sp, encoding="utf-8"))
            for f in sj.get("folds", []):
                for part, toks in f.items():
                    if isinstance(toks, list):
                        for t in toks:
                            folds.setdefault(str(t), []).append(("ctsp_splits_5fold/fold%s" % f.get("fold"), part))
        for r in recs:
            vid = str(r["volume_id"]).zfill(4)
            ct = os.path.join(base, r.get("ct_file") or "ct/%s_ct.nii.gz" % vid)
            if not os.path.exists(ct):
                continue
            pos = (r.get("position") or "unknown").lower()
            pos = "decubitus" if pos.startswith("decubitus") else pos
            key = ix.subject("ctsp:" + vid, "manifest volume_id (one record per patient)", r.get("sex"), r.get("age_band"))
            ann = []
            lab = os.path.join(base, r.get("label_file") or "labels/%s_label.nii.gz" % vid)
            if os.path.exists(lab):
                ann.append(dict(kind="expert" if r.get("prov_spine") == "manual" else "pseudo", labeller="CTSpine1K radiologists (vertebrae)"
                                if r.get("prov_spine") == "manual" else "out-of-fold model (vertebrae)", version="CTSP v11", path=lab))
                ann.append(dict(kind="expert" if r.get("prov_pelvis") == "manual" else "pseudo", labeller="CTPelvic1K (sacrum, hips)"
                                if r.get("prov_pelvis") == "manual" else "Dataset803 out-of-fold pseudolabel (pelvis)", version="CTSP v11", path=lab))
                ann.append(dict(kind="reviewed", labeller="TotalSegmentator + Moller network, student-corrected (ribs)", version="CTSP v11", path=lab))
            v10 = os.path.join(base, "labels_v10", os.path.basename(lab))
            if os.path.exists(v10):
                ann.append(dict(kind="release_labels", labeller="CTSpinoPelvic1K release", version="CTSP v10 (id 29 live)", path=v10))
            if r.get("castellvi_type"):
                ann.append(dict(kind="expert", labeller="two radiology residents, consensus (Castellvi)", version="CTSP v11",
                                status=str(r.get("castellvi_type")), detail=dict(agreement=r.get("castellvi_agreement"))))
            splits = [dict(experiment=e, part=p, source_file=sp) for e, p in folds.get(str(r.get("token")), [])]
            extra = {k: r.get(k) for k in ("token", "side", "match_type", "kvp", "slice_thickness", "convolution_kernel", "lstv_label",
                                           "has_l6", "has_lumbar_rib", "prov_spine", "prov_pelvis", "pelvic_series_uid")}
            ix.item(dict(path=ct, source_id=sid, subject_key=key, case_id=vid, modality="CT", body_region="thoracolumbar-pelvis",
                         position=pos, view="volume", device=" ".join(x for x in (r.get("manufacturer"), r.get("manufacturer_model")) if x) or None,
                         role="converted", series_uid=r.get("spine_series_uid"), adapter="ctsp_manifest", extra=extra),
                    annotations=ann, splits=splits,
                    lineage=[dict(source_ref="tcia:" + str(r.get("spine_series_uid")), relation="converted_from", tool="fetch_from_tcia.py")])
    attach_harvest_calls(ix, "ctsp", (sid,))


def adapter_vindr(ix, folder, readme, sid):
    for rel in sorted(glob.glob(os.path.join(folder, "**", "1.0.0"), recursive=True)):
        for split in ("train", "test"):
            ann_csv = os.path.join(rel, "annotations", split + ".csv")
            by_img = {}
            if os.path.isfile(ann_csv):
                for r in read_csv(ann_csv):
                    by_img.setdefault(r.get("image_id"), []).append(r)
            imgdir = os.path.join(rel, split + "_images")
            for p in walk_files(imgdir, DCM_EXT):
                iid = os.path.splitext(os.path.basename(p))[0]
                rows = by_img.get(iid, [])
                study = rows[0].get("study_id") if rows else None
                key = ix.subject("vindr:" + study, "annotations csv study_id (no PatientID in the headers)") if study else None
                lesions = sorted({r.get("lesion_type") for r in rows if r.get("lesion_type") and r.get("lesion_type") != "No finding"})
                ann = [dict(kind="release_labels", labeller="VinDr radiologists (lesion boxes)", version="1.0.0", path=ann_csv,
                            detail=dict(lesions=lesions))] if lesions else [dict(kind="none", detail=dict(finding="No finding" if rows else "no csv row"))]
                ix.item(dict(path=p, source_id=sid, subject_key=key, case_id=iid, modality="DX", body_region="spine (cervical or lumbar)",
                             role="raw", series_uid=rows[0].get("series_id") if rows else None, adapter="vindr_csv",
                             extra=dict(note="DICOM modality and view tags not read")),
                        annotations=ann, splits=[dict(experiment="vindr_release", part=split, source_file=ann_csv)])


def adapter_buu(ix, folder, readme, sid):
    for p in walk_files(os.path.join(folder, "raw"), (".jpg", ".jpeg")):
        stem = os.path.splitext(os.path.basename(p))[0]
        m = re.match(r"^(\d{3,5})", stem)
        mv = re.search(r"Y([01])", stem)
        parent = os.path.basename(os.path.dirname(p)).upper()
        view = "AP" if (mv and mv.group(1) == "0") or parent == "AP" else "LAT" if (mv and mv.group(1) == "1") or parent in ("LA", "LAT") else "unknown"
        key = ix.subject("buu:" + m.group(1), "file name leading number") if m else None
        csvp = os.path.splitext(p)[0] + ".csv"
        ann = [dict(kind="release_labels", labeller="BUU-LSPINE readers (end-plate lines; level names by row order)", path=csvp)] if os.path.exists(csvp) else []
        ix.item(dict(path=p, source_id=sid, subject_key=key, case_id=stem, modality="DX", body_region="lumbar", position="standing",
                     view=view, role="raw", adapter="buu", extra=dict(duplicate_copy=bool(re.search(r"\(\d\)$", stem)))), annotations=ann)


def adapter_nhanes_tiff(ix, folder, readme, sid):
    for p in walk_files(os.path.join(folder, "raw"), (".tif", ".tiff")):
        m = re.match(r"^([CL])(\d{5})", os.path.basename(p))
        key = ix.subject("nhanes:" + m.group(2), "NHANES sample sequence number in the file name") if m else None
        ix.item(dict(path=p, source_id=sid, subject_key=key, case_id=os.path.basename(p), modality="DX",
                     body_region={"C": "cervical", "L": "lumbar"}.get(m.group(1)) if m else None, view="LAT", role="raw",
                     adapter="nhanes_tiff", extra=dict(film="digitised survey film 1976-80")))


def adapter_nhanes_pickle(ix, folder, readme, sid):
    for p in walk_files(os.path.join(folder, "raw"), (".pkl",)):
        name = os.path.basename(p)
        m = re.search(r"([CL])?_?(\d{5,6})", name)
        key = ix.subject("nhanes:" + m.group(2), "sequence number in the pickle name") if m else None
        region = {"C": "cervical", "L": "lumbar"}.get((m.group(1) if m else "") or "")
        ix.item(dict(path=p, source_id=sid, subject_key=key, case_id=name, modality="DX", body_region=region, view="LAT", role="raw",
                     format="pkl", adapter="nhanes_pickle"),
                annotations=[dict(kind="release_labels", labeller="Mo et al. 2023 (per-level masks)", version="zenodo 10223910", path=p)])
    adapter_generic(ix, folder, readme, sid, skip_dirs=("derived", "raw"))


def adapter_csxa(ix, folder, readme, sid):
    jsons = {os.path.splitext(os.path.basename(j))[0]: j for j in walk_files(os.path.join(folder, "raw"), (".json",))}
    for p in walk_files(os.path.join(folder, "raw"), (".png",)):
        stem = os.path.splitext(os.path.basename(p))[0]
        m = re.match(r"^(\d+)", stem)
        key = ix.subject("csxa:" + m.group(1), "leading digits of the file name (the <G><AA> tail is not part of the key)") if m else None
        ann = [dict(kind="release_labels", labeller="CSXA annotators (corner keypoints named by level)", path=jsons[stem])] if stem in jsons else []
        ix.item(dict(path=p, source_id=sid, subject_key=key, case_id=stem, modality="DX", body_region="cervical", view="LAT",
                     role="raw", adapter="csxa"), annotations=ann)


REALX_SOURCE = (("carmlspine", "carmlspine", "XA"), ("cobra_", "cobra2026", "CBCT"), ("deepfluoro", "deepfluoro_h5", "RF"),
                ("geneva", "geneva_hip", "RF"), ("bournemouth", "bournemouth_qf_cervical_tracks", "RF"))
REALX_CORPUS = {"carmlspine": "carmlspine", "cobra2026": "cobra", "deepfluoro_h5": "deepfluoro", "geneva_hip": "geneva",
                "bournemouth_qf_cervical_tracks": "bournemouth"}


def adapter_realxray(ix, folder, readme, sid):
    for metadir in sorted(glob.glob(os.path.join(folder, "**", "meta"), recursive=True)):
        bank = os.path.relpath(os.path.dirname(metadir), folder)
        name = bank.split(os.sep)[-1]
        src, mod = next(((s, m) for pre, s, m in REALX_SOURCE if name.startswith(pre)), ("realxray_layout", "OTHER"))
        if src not in ix.sources:
            src = sid
        for mp in sorted(glob.glob(os.path.join(metadir, "*.json"))):
            stem = os.path.splitext(os.path.basename(mp))[0]
            try:
                meta = json.load(open(mp, encoding="utf-8"))
            except ValueError:
                continue
            split = meta.get("split") or ""
            imgs = glob.glob(os.path.join(folder, bank, "images", split or "*", stem + ".png"))
            if not imgs:
                continue
            img = imgs[0]
            split = split or os.path.basename(os.path.dirname(img))
            case = meta.get("case")
            key = ix.subject("%s:%s" % (REALX_CORPUS.get(src, src), case), "meta case (REAL_XRAY_DATASETS_SPEC.md)") if case else None
            dev = meta.get("device") or {}
            v = meta.get("view") or {}
            view = view_from_angle(v.get("lat_from_ap_deg")) if isinstance(v, dict) else str(v).upper()
            lab = os.path.join(folder, bank, "labels", split, stem + ".txt")
            boxes = meta.get("boxes") or []
            agree = sum(1 for b in boxes if b.get("level"))
            ann = [dict(kind="two_labeller", labeller="TotalSegmentator + SPINEPS/VERIDAH, agreed levels only", version=meta.get("label_source", ""),
                        path=lab if os.path.exists(lab) else "", detail=dict(n_boxes=len(boxes), n_named=agree))] if boxes or os.path.exists(lab) else []
            ix.item(dict(path=img, source_id=src, subject_key=key, case_id=case, modality=mod, view=view if view in ("AP", "LAT", "OBL") else "unknown",
                         device=" ".join(str(x) for x in (dev.get("make"), dev.get("model")) if x) or None, px_mm=meta.get("px_mm"),
                         role="derived", format="png", adapter="realxray_meta",
                         extra=dict(bank=bank, kvp=dev.get("kvp"), mas=dev.get("mas"), detector=dev.get("detector"),
                                    gantry_deg=v.get("gantry_deg") if isinstance(v, dict) else None,
                                    lat_from_ap_deg=v.get("lat_from_ap_deg") if isinstance(v, dict) else None)),
                    annotations=ann, splits=[dict(experiment="realxray:" + bank, part=split, source_file=os.path.join(folder, bank, "splits.json"))],
                    lineage=[dict(source_ref=meta.get("source_image"), relation="converted_from", tool="realxray exporter")])


def _yaml_scalar(path, key):
    try:
        for line in open(path, encoding="utf-8", errors="replace"):
            m = re.match(r"^\s*%s\s*:\s*['\"]?([^'\"#]+)" % re.escape(key), line)
            if m:
                return m.group(1).strip()
    except OSError:
        return None
    return None


def adapter_cobra(ix, folder, readme, sid):
    for cdir in sorted(glob.glob(os.path.join(folder, "cases", "*"))):
        if not os.path.isdir(cdir):
            continue
        case = os.path.basename(cdir)
        key = ix.subject("cobra:" + case, "case id")
        meta = os.path.join(folder, "meta", case, "metadata.yaml")
        date = _yaml_scalar(meta, "StudyDate") if os.path.exists(meta) else None
        centre = case[:1]
        dev = "Elekta XVI" if centre in "ABCD" else "Varian" if centre in "FG" else None
        for f, mod, view in (("projections.mha", "CBCT", "sweep"), ("ct_original.mha", "CT", "volume"), ("ct_def.mha", "CT", "volume"),
                             ("cbct_clinical.mha", "CBCT", "volume"), ("cbct_rtk.mha", "CBCT", "volume")):
            p = os.path.join(cdir, f)
            if os.path.exists(p):
                ix.item(dict(path=p, source_id=sid, subject_key=key, case_id=case, modality=mod, body_region="pelvis", view=view,
                             device=dev, acquisition_date=date, role="raw", format="mha", adapter="cobra",
                             extra=dict(file=f, centre=centre, split="train (public)")),
                        annotations=[dict(kind="none", detail=dict(note="release ships images, geometry, registered CT, FOV masks; no labels"))])


def _dicom_header(p):
    if pydicom is None:
        return {}
    try:
        d = pydicom.dcmread(p, stop_before_pixels=True, force=True)
    except Exception:                   # noqa: BLE001
        return {}
    g = lambda k: str(getattr(d, k, "") or "") or None
    return dict(Modality=g("Modality"), PatientPosition=g("PatientPosition"), ViewPosition=g("ViewPosition"), StudyDate=g("StudyDate"),
                SeriesInstanceUID=g("SeriesInstanceUID"), PatientID=g("PatientID"), Manufacturer=g("Manufacturer"),
                PixelSpacing=g("PixelSpacing"), Rows=g("Rows"), Columns=g("Columns"), PositionerPrimaryAngle=g("PositionerPrimaryAngle"))


POS_MAP = {"HFS": "supine", "FFS": "supine", "HFP": "prone", "FFP": "prone", "HFDR": "decubitus", "HFDL": "decubitus",
           "FFDR": "decubitus", "FFDL": "decubitus"}


def _subject_from_path(sid, path):
    s = path.replace("\\", "/")
    if sid.startswith("carmlspine"):
        m = re.search(r"/(case\d+)(/|$)", s)
        return ("carmlspine:" + m.group(1)) if m else None
    if sid.startswith("deepfluoro"):
        m = re.search(r"(\d{2}-\d{4})", s)
        return ("deepfluoro:" + m.group(1)) if m else None
    return None


def adapter_dicom_tree(ix, folder, readme, sid):
    smod = src_modality(ix, sid)
    by_dir = {}
    for p in walk_files(folder):
        rel = os.path.relpath(p, folder)
        if rel.split(os.sep)[0] == "derived":
            continue
        if ext_of(p) in DCM_EXT:
            by_dir.setdefault(os.path.dirname(p), []).append(p)
        elif ext_of(p) in ARC_EXT:
            ix.item(dict(path=p, source_id=sid, modality=smod, role="raw", adapter="dicom_tree"))
    for d, files in sorted(by_dir.items()):
        h = _dicom_header(files[0])
        mod = (h.get("Modality") or "").upper()
        mod = {"CT": "CT", "XA": "XA", "RF": "RF", "CR": "CR", "DX": "DX", "MR": "MR"}.get(mod, "")
        key = ix.subject(_subject_from_path(sid, d), "folder name") if _subject_from_path(sid, d) else None
        if not key and h.get("PatientID") and sid == "tcia_ct_colonography":
            key = ix.subject("tcia_ctc:" + h["PatientID"], "DICOM PatientID")
        pos = POS_MAP.get((h.get("PatientPosition") or "").upper(), "unknown")
        volume = (mod in ("CT", "MR") or (not mod and smod in ("CT", "CBCT"))) and len(files) > 1
        if "CBCT" in d.upper() and mod in ("CT", ""):
            mod = "CBCT"
        if volume or mod == "CBCT" and len(files) > 1:
            ix.item(dict(path=d, source_id=sid, subject_key=key, modality=mod or smod, position=pos, view="volume", role="raw",
                         format="dicom_series", series_uid=h.get("SeriesInstanceUID"), acquisition_date=h.get("StudyDate"),
                         device=h.get("Manufacturer"), adapter="dicom_tree", extra=dict(n_files=len(files))))
        else:
            for p in files:
                hp = _dicom_header(p) if pydicom else {}
                m2 = {"XA": "XA", "RF": "RF", "CR": "CR", "DX": "DX", "CT": "CT"}.get((hp.get("Modality") or mod or "").upper(), smod)
                vp = (hp.get("ViewPosition") or "").upper()
                view = vp if vp in ("AP", "PA", "LAT") else view_from_angle(hp.get("PositionerPrimaryAngle")) if hp.get("PositionerPrimaryAngle") else "unknown"
                ix.item(dict(path=p, source_id=sid, subject_key=key, modality=m2, position=POS_MAP.get((hp.get("PatientPosition") or "").upper(), "unknown"),
                             view=view, role="raw", format="dicom", acquisition_date=hp.get("StudyDate"), device=hp.get("Manufacturer"),
                             adapter="dicom_tree"))
    # volumes beside the DICOM: conversions (C-ArmLSpine nifti/, TCIA tcia_nifti/) and outputs (spineps/, proto*/) are
    # kept, never counted as more acquisitions; their masks attach to their images
    conv = [d for d in sorted(os.listdir(folder)) if os.path.isdir(os.path.join(folder, d)) and d not in ("derived", "raw", "unpacked", "fetch")]
    for top in conv:
        sub = os.path.join(folder, top)
        is_conv = "nifti" in top.lower() or any("nifti" in x.lower() for x in os.listdir(sub) if os.path.isdir(os.path.join(sub, x)))
        adapter_generic(ix, sub, readme, sid, role_hint="converted" if is_conv else "derived", skip_dirs=(), exts=VOL_EXT, counted=0,
                        note="conversion of a DICOM series indexed under raw/ (not matched by series)" if is_conv
                        else "output beside the release (not a release item)")


def adapter_totalsegmentator(ix, folder, readme, sid):
    for metap in sorted(glob.glob(os.path.join(folder, "raw", "**", "meta.csv"), recursive=True)):
        base = os.path.dirname(metap)
        meta = {}
        try:
            with open(metap, encoding="utf-8", errors="replace") as fh:
                sample = fh.read(4096)
            dialect = csv.Sniffer().sniff(sample, delimiters=";,\t")
            with open(metap, encoding="utf-8", errors="replace", newline="") as fh:
                for r in csv.DictReader(fh, dialect=dialect):
                    meta[r.get("image_id") or r.get("subject") or ""] = r
        except Exception:               # noqa: BLE001
            meta = {}
        for sdir in sorted(glob.glob(os.path.join(base, "s[0-9][0-9][0-9][0-9]"))):
            ct = os.path.join(sdir, "ct.nii.gz")
            if not os.path.exists(ct):
                continue
            s = os.path.basename(sdir)
            m = meta.get(s, {})
            key = ix.subject("ts:" + s, "release subject id (v201 and v300 ids are not reconciled: docs/PATIENT_IDENTITY_SPEC.md)",
                             (m.get("gender") or None), None)
            seg = os.path.join(sdir, "segmentations")
            ann = [dict(kind="release_labels", labeller="TotalSegmentator release (model output, manually refined; no L6/T13 class)",
                        version=sid, path=seg)] if os.path.isdir(seg) else []
            splits = [dict(experiment=sid + "_release", part=m["split"], source_file=metap)] if m.get("split") else []
            ix.item(dict(path=ct, source_id=sid, subject_key=key, case_id=s, modality="CT", view="volume", role="raw", adapter="totalsegmentator",
                         body_region=m.get("study_type"), extra={k: m.get(k) for k in ("age", "study_type", "institute", "manufacturer", "kvp") if m.get(k)}),
                    annotations=ann, splits=splits)
    for p in glob.glob(os.path.join(folder, "raw", "*", "*.zip")):
        ix.item(dict(path=p, source_id=sid, modality="CT", role="raw", adapter="totalsegmentator", counted=0,
                     extra=dict(note="the release archive; its unpacked subjects are the counted items")))
    attach_harvest_calls(ix, "totalsegmentator", (sid,))


VERSE_SUB = re.compile(r"((?:gl)+\d{3,4}[a-z]?|verse\d{3,4}[a-z]?)")


def verse_component(folder, p):
    """The tree a VerSeFusion file sits in: the first component below VerSeFusion_data (raw, canonical, corrected,
    unified, qc), or '' when the path has no VerSeFusion_data level."""
    parts = os.path.relpath(p, folder).split(os.sep)
    if "VerSeFusion_data" in parts:
        i = parts.index("VerSeFusion_data")
        return parts[i + 1] if i + 1 < len(parts) else ""
    return ""


def adapter_verse(ix, folder, readme, sid):
    """raw/ is the OSF download (verse19_20, role raw); canonical/ and corrected/ are VerSeFusion's own trees (role
    converted); unified/ holds only links into raw/ and canonical/ and is not indexed; derived/ is the render banks."""
    segs = {}
    files = []
    for p in walk_files(folder, (".nii.gz", ".nii")):
        if os.path.relpath(p, folder).split(os.sep)[0] == "derived" or os.path.islink(p):
            continue
        comp = verse_component(folder, p)
        if comp in ("unified", "qc"):
            continue
        files.append((p, comp))
    for p, comp in files:
        if "_seg" in os.path.basename(p) or "msk" in os.path.basename(p):
            m = VERSE_SUB.search(p)
            if m:
                segs.setdefault((comp, m.group(1)), []).append(p)
    for p, comp in files:
        b = os.path.basename(p)
        if "_seg" in b or "msk" in b:
            continue
        m = VERSE_SUB.search(p)
        sub = m.group(1) if m else None
        raw = comp == "raw"
        if raw:
            src = "verse19_20" if "verse19_20" in ix.sources else sid
        else:
            src = "versefusion" if "versefusion" in ix.sources else sid
        key = ix.subject("verse:" + sub, "VerSe series name (series is not subject: docs/PATIENT_IDENTITY_SPEC.md)") if sub else None
        ann = [dict(kind="expert", labeller="VerSe annotators (vertebra masks)", path=s) for s in segs.get((comp, sub), [])][:2]
        ix.item(dict(path=p, source_id=src, subject_key=key, case_id=sub, modality="CT", view="volume", role="raw" if raw else "converted",
                     adapter="verse", extra=dict(tree=comp or "(no VerSeFusion_data level)")), annotations=ann or [release_default(ix, src)])
    attach_harvest_calls(ix, "verse", ("verse19_20", sid))


REAL_FILM_BANKS = ("films_drr", "films_drr_buucorr", "films_ap_drr", "films_smoke", "nhanes_drr", "vindr_det_drr", "vindr_pseudo_drr",
                   "aasce_drr", "mendeley_drr", "lateral236_pseudo", "nhanes_pseudo", "vindr_pseudo")
BANK_SOURCE = (("ctsp_drr_obl", "ctsp_drr_obl"), ("ctsp_drr", "ctsp_drr"), ("verse_soft_drr", "verse_soft_drr"), ("verse_drr", "verse_drr"),
               ("ts_drr_v3", "ts_drr_v3"), ("ts_drr", "ts_drr"), ("anchor_drr_c2", "anchor_drr_c2"), ("anchor_drr", "anchor_drr"),
               ("physics_rare", "physics_rare"), ("cut_rare", "physics_rare"), ("physics_drr", "physics_drr"), ("cut_physics", "physics_drr"),
               ("spinalai_drr", "spinalai_drr"), ("aasce_drr", "aasce_drr"), ("carm_", "carm_drr"), ("implant_", "implant_ct_synthetic"),
               ("lstv_flag", "lstv_flag_renders"), ("fluorogen", "fluorogen_synthetic"), ("xrsp1k", "xrspinopelvic1k"))


def adapter_render_bank(ix, folder, readme, sid, banks_root=None):
    root = banks_root or os.path.join(folder, "derived")
    if not os.path.isdir(root):
        return
    for bank in sorted(os.listdir(root)):
        bdir = os.path.join(root, bank)
        if not os.path.isdir(bdir):
            continue
        bsrc = next((s for pre, s in BANK_SOURCE if bank.startswith(pre) and s in ix.sources), sid)
        if os.path.isdir(os.path.join(bdir, "ann")):
            real = bank in REAL_FILM_BANKS
            carm = bank.startswith("carm_")
            mod = "XA" if carm else "DX" if real else "RF" if bank.startswith("fluorocap") else "RENDER"
            kind = "two_labeller" if carm else "pseudo" if ("pseudo" in bank or bank in ("vindr_det_drr",) or not real) else "release_labels"
            for ap in sorted(glob.glob(os.path.join(bdir, "ann", "*.json"))):
                stem = os.path.splitext(os.path.basename(ap))[0]
                img = next((p for p in (os.path.join(bdir, "img", stem + ".npy"), os.path.join(bdir, "img", stem + ".png")) if os.path.exists(p)), ap)
                try:
                    ann = json.load(open(ap, encoding="utf-8"))
                except ValueError:
                    ann = {}
                key = None
                if _pk is not None:
                    try:
                        res = _pk.key_any(stem, ann=ann)          # (dict(key=..., scheme=...), None) or (None, reason)
                        res = res[0] if isinstance(res, tuple) else res
                        k = res.get("key") if isinstance(res, dict) else res
                        key = ix.subject(k, "tools/patient_keys.py key_any") if k else None
                    except Exception:   # noqa: BLE001
                        key = None
                view = str(ann.get("view") or "").upper()
                view = "LAT" if view.startswith("LAT") else "AP" if view.startswith("AP") else "OBL" if view.startswith("OBL") else "unknown"
                ix.item(dict(path=img, source_id=bsrc, subject_key=key, case_id=stem, modality=mod, view=view, role="derived",
                             adapter="render_bank", extra=dict(bank=bank, ann=ap)),
                        annotations=[dict(kind=kind, labeller="projected or converted labels (see the bank's builder)", version=bank, path=ap,
                                          detail=dict(n_levels=len(ann.get("levels") or {})))],
                        lineage=[dict(source_ref=ann.get("source_case") or ann.get("patient_id"), relation="rendered_from")])
        elif glob.glob(os.path.join(bdir, "rung_*.npz")) or os.path.exists(os.path.join(bdir, "meta.json")):
            ix.item(dict(path=bdir, source_id=bsrc, case_id=bank, modality="OTHER", role="derived", format="crop_bank", adapter="render_bank",
                         extra=dict(bank=bank, note="context crop bank: crops live inside rung_*.npz; one row per bank")))


def adapter_acquisition(ix, folder, readme, sid):
    coll = os.path.basename(folder.rstrip("/"))
    harvest = os.path.join(os.path.dirname(folder.rstrip("/")), "anomaly_harvest", coll)
    calls = {}
    for fn in ("rows.csv", "registry_rows.csv"):
        p = os.path.join(harvest, fn)
        if os.path.isfile(p):
            for r in read_csv(p):
                calls[r.get("case")] = (r, p)
    cases = read_csv(os.path.join(harvest, "cases.csv")) if os.path.isfile(os.path.join(harvest, "cases.csv")) else []
    if not cases:
        cases = [dict(case=os.path.basename(p).replace("_ct.nii.gz", ""), ct=p, patient_key="") for p in
                 sorted(glob.glob(os.path.join(folder, "nifti", "*_ct.nii.gz")))]
    ids = [i for i in (readme.get("source_ids") or [sid]) if i in ix.sources] or [sid]
    # case -> series UID (the screen's convert shards) -> DICOM folder (the fetcher's verified.jsonl): one header per case
    case_uid = {}
    for sp in sorted(glob.glob(os.path.join(harvest, "convert", "shard*.jsonl"))):
        for line in open(sp, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("case") and d.get("item"):
                case_uid[d["case"]] = d["item"]
    uid_dir = {}
    vp = os.path.join(folder, "fetch", "verified.jsonl")
    if os.path.isfile(vp):
        for line in open(vp, encoding="utf-8", errors="replace"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("dir"):
                uid_dir[d.get("unit")] = os.path.join(folder, d["dir"])
    for c in cases:
        ct = c.get("ct") or ""
        if not ct or not os.path.exists(ct):
            continue
        src = sid
        if coll == "idc":
            cand = "idc_" + (c.get("source") or "")
            src = cand if cand in ix.sources else ("idc_tier1" if "idc_tier1" in ix.sources else sid)
        elif len(ids) == 1:
            src = ids[0]
        key = ix.subject(c.get("patient_key"), "acquisition_screen.py patient_key") if c.get("patient_key") else None
        r, rp = calls.get(c.get("case"), (None, None))
        ann = [dict(kind="two_labeller", labeller="SPINEPS+VERIDAH (A) + TotalSegmentator geometry (B)", version="acquisition screen",
                    path=rp, status=r.get("subtype"),
                    detail={k: r.get(k) for k in ("labeller_a", "labeller_b", "agree", "truth_tier", "n_lumbar", "four_lumbar", "lumbar_rib")})] if r else \
            [dict(kind="none", detail=dict(note="no call row for this case"))]
        uid = case_uid.get(c.get("case"))
        h = {}
        sdir = uid_dir.get(uid) if uid else None
        if sdir and os.path.isdir(sdir):
            first = next((os.path.join(dp, f) for dp, dn, fn in os.walk(sdir) for f in sorted(fn) if ext_of(f) in DCM_EXT), None)
            h = _dicom_header(first) if first else {}
        ix.item(dict(path=ct, source_id=src, subject_key=key, case_id=c.get("case"), modality="CT", view="volume",
                     position=POS_MAP.get((h.get("PatientPosition") or "").upper(), "unknown"), acquisition_date=h.get("StudyDate"),
                     device=h.get("Manufacturer"), series_uid=h.get("SeriesInstanceUID") or uid,
                     role="converted" if "/nifti/" in ct.replace("\\", "/") else "raw", adapter="acquisition",
                     extra=dict(extent_mm=c.get("extent_mm"), dz_mm=c.get("dz_mm"), pixel_sha1=c.get("pixel_sha1"),
                                position_basis="DICOM (0018,5100) of %s" % sdir if h.get("PatientPosition") else
                                ("no DICOM header read" + ("" if sdir else ": no series folder matched")))),
                annotations=ann)


def attach_harvest_calls(ix, harvest_name, source_ids):
    """The anomaly-harvest screen of a CT release (<root>/anomaly_harvest/<name>/rows.csv or registry_rows.csv) as
    two-labeller annotation rows on that release's items, matched by subject key (canon of the row's patient_key)."""
    hdir = os.path.join(ix.root, "anomaly_harvest", harvest_name)
    rows = []
    for fn in ("rows.csv", "registry_rows.csv"):
        p = os.path.join(hdir, fn)
        if os.path.isfile(p):
            rows += [(r, p) for r in read_csv(p)]
    n = 0
    for r, p in rows:
        key = canon(r.get("patient_key"))
        if not key:
            continue
        for (iid,) in ix.db.execute("SELECT item_id FROM item WHERE subject_key=? AND source_id IN (%s) AND counted=1"
                                    % ",".join("?" * len(source_ids)), [key] + list(source_ids)).fetchall():
            ix.db.execute("INSERT OR IGNORE INTO annotation(item_id, kind, labeller, version, path, status, detail) VALUES (?,?,?,?,?,?,?)",
                          (iid, "two_labeller", "SPINEPS+VERIDAH (A) + TotalSegmentator geometry (B)", "anomaly harvest " + harvest_name,
                           p, r.get("subtype"), json.dumps({k: r.get(k) for k in ("case", "labeller_a", "labeller_b", "agree", "truth_tier")
                                                            if r.get(k) is not None}, sort_keys=True)))
            n += 1
    return n


ADAPTERS = dict(generic=adapter_generic, ctsp_manifest=adapter_ctsp_manifest, vindr_csv=adapter_vindr, buu=adapter_buu,
                nhanes_tiff=adapter_nhanes_tiff, nhanes_pickle=adapter_nhanes_pickle, csxa=adapter_csxa, realxray_meta=adapter_realxray,
                cobra=adapter_cobra, dicom_tree=adapter_dicom_tree, totalsegmentator=adapter_totalsegmentator, verse=adapter_verse,
                render_bank=adapter_render_bank, acquisition=adapter_acquisition)


# ------------------------------------------------------------------------------------------------ driver
def load_sources(db, sources_json):
    raw = open(sources_json, "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    doc = json.loads(raw.decode("utf-8"))
    for e in doc["sources"]:
        ann = e.get("annotation") or {}
        pv = e.get("position_view") or {}
        db.execute("INSERT OR REPLACE INTO source(source_id, name, kind, status, family, modality, anatomy, licence, access, restricted, "
                   "layout_path, doi_or_url, manifest_anchor, reacquire_route, annotation_status, annotation_kinds, position, view, loaded_from) "
                   "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (e["id"], e["name"], e["kind"], e["status"], e["family"], json.dumps(e["modality"]), json.dumps(e["anatomy"]),
                    e["licence"], e["access"], 1 if e["id"] in ("vindr_spinexr",) or e["id"].startswith("buu_lspine") else 0,
                    e["layout"]["path"], json.dumps(e["doi_or_url"]), e.get("manifest_anchor"), e["reacquire"]["route"],
                    json.dumps(ann.get("status") or []), json.dumps(ann.get("kinds") or []), json.dumps(pv.get("position") or []),
                    json.dumps(pv.get("view") or []), h))
    db.execute("INSERT OR REPLACE INTO source(source_id, name, kind, status, family, modality, anatomy, licence, access, restricted, layout_path, loaded_from) "
               "VALUES ('multisource_banks', 'Banks built from several sources (see layout_map.csv)', 'derived', 'on_disk', '-', '[\"RENDER\"]', '[]', "
               "'inherits the sources'' terms', 'project', 0, ?, ?)", (DEFAULT_ROOT + "/multisource_banks", h))
    db.commit()
    return len(doc["sources"])


def fetch_state(folder):
    """The acquisition fetcher's own record of what it verified (tools/acquisition_fetch.py writes fetch/), or None."""
    fdir = os.path.join(folder, "fetch")
    if not os.path.isdir(fdir):
        return None
    st = {}
    sp = os.path.join(fdir, "FETCH_STATUS.json")
    if os.path.isfile(sp):
        try:
            st = json.load(open(sp, encoding="utf-8"))
        except ValueError:
            st = {"error": "FETCH_STATUS.json unreadable"}
    vp = os.path.join(fdir, "verified.jsonl")
    if os.path.isfile(vp):
        units = set()
        for line in open(vp, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line:
                try:
                    units.add(json.loads(line).get("unit"))
                except ValueError:
                    pass
        st["verified_jsonl_units"] = len(units)
    fp = os.path.join(fdir, "failed.jsonl")
    if os.path.isfile(fp):
        st["failed_jsonl_lines"] = sum(1 for l in open(fp, encoding="utf-8", errors="replace") if l.strip())
    return json.dumps(st, sort_keys=True)


def on_login_node():
    return socket.gethostname().startswith("warrior") or not os.environ.get("SLURM_JOB_ID")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--db", default=os.path.join(DEFAULT_ROOT, "_index", "holding.sqlite"))
    ap.add_argument("--sources", default=os.path.join(DPROOT, "sources.json"))
    ap.add_argument("--folders", nargs="*", default=[], help="only these folder names under --root")
    ap.add_argument("--hash", choices=["none", "small", "all"], default="none", help="sha256: none, files < 64 MB, or every file")
    ap.add_argument("--allow-local", action="store_true", help="run outside a Slurm job (tests, a laptop copy)")
    a = ap.parse_args(argv)
    if on_login_node() and not a.allow_local:
        print("refusing: run with sbatch (build_index.sbatch), never on the login node; --allow-local for a local test tree")
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.db)), exist_ok=True)
    db = sqlite3.connect(a.db)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(open(os.path.join(HERE, "SCHEMA.sql"), encoding="utf-8").read())
    n_src = load_sources(db, a.sources)
    ix = Indexer(db, a.root, a.hash)
    ix.start(notes="folders=%s hash=%s" % (",".join(a.folders) or "all", a.hash))
    folders = a.folders or sorted(d for d in os.listdir(a.root) if os.path.isfile(os.path.join(a.root, d, "README.yaml")))
    for name in folders:
        folder = os.path.join(a.root, name)
        rp = os.path.join(folder, "README.yaml")
        if not os.path.isfile(rp):
            print("skip %s: no README.yaml" % name)
            continue
        with open(rp, encoding="utf-8") as fh:
            txt = fh.read()
        readme = mini_yaml.loads(txt) or {}
        ids = [i for i in (readme.get("source_ids") or []) if i in ix.sources] or ["multisource_banks"]
        sid = ids[0]
        adapter = readme.get("index_adapter") or "generic"
        fn = ADAPTERS.get(adapter, adapter_generic)
        ix.skip = tuple(os.path.join(folder, s.strip("/").replace("/", os.sep)) for s in (readme.get("index_skip") or []))
        before = dict(ix.counts)
        try:
            fn(ix, folder, readme, sid)
            if adapter != "render_bank":
                adapter_render_bank(ix, folder, readme, sid)
            complete = True
        except Exception as exc:        # noqa: BLE001  (one folder failing must not lose the others; it is reported)
            print("FOLDER FAILED %s (%s): %r" % (name, adapter, exc))
            complete = False
        if complete:
            ix.remove_unseen(folder)
        n_items = db.execute("SELECT COUNT(*) FROM item WHERE path >= ? AND path < ?", prefix_range(folder)).fetchone()[0]
        db.execute("INSERT OR REPLACE INTO folder(folder, readme_sha256, adapter, source_ids, restricted, last_run, n_items, fetch_status) "
                   "VALUES (?,?,?,?,?,?,?,?)",
                   (folder, hashlib.sha256(txt.encode("utf-8")).hexdigest(), adapter, json.dumps(ids), 1 if readme.get("restricted") else 0,
                    ix.run_id, n_items, fetch_state(folder)))
        db.commit()
        delta = {k: ix.counts[k] - before[k] for k in ix.counts}
        print("%-36s %-16s items %6d  new %d updated %d unchanged %d removed %d%s" % (
            name, adapter, n_items, delta["new"], delta["updated"], delta["unchanged"], delta["removed"], "" if complete else "  (INCOMPLETE)"))
    ix.finish()
    print("INDEX_DONE run %d sources %d: %s" % (ix.run_id, n_src, json.dumps(ix.counts)))
    db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
