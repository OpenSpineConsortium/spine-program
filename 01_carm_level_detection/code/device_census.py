#!/usr/bin/env python
# Copied 2026-10-08 from the private repository spinesurg-ct-nnunet (branch L6_Class): tools/device_census.py [tracked at 097933a]
"""Header and image census of every C-arm the project holds frames from: what the DICOM headers say about each
device and its exposures, and what the frames themselves say without a CT (field shape, collimator penumbra,
noise power spectrum, edge halo, histogram). One card per device under docs/devices/census/.

  headers   walk a directory, read every DICOM header (pydicom, forced, pixels not read), group by device
            (Manufacturer | ManufacturerModelName, or --name), tabulate every public tag of interest and EVERY
            private tag (creator, VR, length, short values) with counts of distinct values, and write one row per
            frame (kVp, mA, ms, mAs, pulse, SID, SOD, angles, dose, field, collimator edges) to <name>__frames.csv
            for the exposure distribution. Patient identity is never copied: only whether the tag is present.
  images    per 8-bit display frame: exposed field and its shape, blade / iris geometry, the border profile and
            its penumbra sigma (device_physics.border_profile), the radial NPS of flat regions, the cortical-edge
            halo (unsharp gain / radius), histogram and gradient quantiles; pooled per device; a figure.
  report    README.md across every device card: one table (make, model, detector, pitch, size, bits, photometric,
            intensity relationship, kVp / mA / ms ranges, SID, field shape, penumbra, halo gain, NPS peak).

    python tools/device_census.py headers --name surgio_b51 --root /rs/.../data/carmlspine --exclude-modality CT
    python tools/device_census.py images  --name surgio_b51 --images "/rs/.../realxray/carmlspine/images/*/*.png" --limit 300
    python tools/device_census.py report
"""
from __future__ import annotations

import argparse
import collections
import csv
import glob
import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import device_physics as PH  # noqa: E402

OUT_DEFAULT = str(Path(__file__).resolve().parents[1] / "docs" / "devices" / "census")

# public tags worth a distribution; PHI tags are never read for value
PUBLIC = ["Manufacturer", "ManufacturerModelName", "SoftwareVersions", "Modality", "ImageType", "SOPClassUID", "Rows", "Columns",
          "BitsAllocated", "BitsStored", "HighBit", "PixelRepresentation", "PhotometricInterpretation", "PixelIntensityRelationship",
          "PixelIntensityRelationshipSign", "RescaleSlope", "RescaleIntercept", "RescaleType", "WindowCenter", "WindowWidth", "VOILUTFunction",
          "ImagerPixelSpacing", "PixelSpacing", "PixelSpacingCalibrationType", "DistanceSourceToDetector", "DistanceSourceToPatient",
          "EstimatedRadiographicMagnificationFactor", "PositionerType", "PositionerPrimaryAngle", "PositionerSecondaryAngle",
          "PositionerPrimaryAngleIncrement", "PositionerSecondaryAngleIncrement", "DetectorPrimaryAngle", "DetectorSecondaryAngle",
          "KVP", "XRayTubeCurrent", "XRayTubeCurrentInuA", "ExposureTime", "ExposureTimeInuS", "Exposure", "ExposureInuAs", "AveragePulseWidth",
          "RadiationSetting", "RadiationMode", "XRayReceptorType", "FilterType", "FilterMaterial", "FilterThicknessMinimum", "FilterThicknessMaximum",
          "FocalSpots", "Grid", "CollimatorShape", "CollimatorLeftVerticalEdge", "CollimatorRightVerticalEdge", "CollimatorUpperHorizontalEdge",
          "CollimatorLowerHorizontalEdge", "CenterOfCircularCollimator", "RadiusOfCircularCollimator", "ShutterShape", "ShutterLeftVerticalEdge",
          "ShutterRightVerticalEdge", "ShutterUpperHorizontalEdge", "ShutterLowerHorizontalEdge", "CenterOfCircularShutter", "RadiusOfCircularShutter",
          "DetectorType", "DetectorConfiguration", "DetectorDescription", "DetectorID", "DetectorBinning", "DetectorElementPhysicalSize",
          "DetectorElementSpacing", "DetectorActiveShape", "DetectorActiveDimensions", "DetectorActiveOrigin", "FieldOfViewShape",
          "FieldOfViewDimensions", "FieldOfViewOrigin", "FieldOfViewRotation", "FieldOfViewHorizontalFlip", "ImageAndFluoroscopyAreaDoseProduct",
          "EntranceDoseInmGy", "ExposureIndex", "NumberOfFrames", "FrameTime", "CineRate", "RecommendedDisplayFrameRate", "FrameIncrementPointer",
          "LossyImageCompression", "LossyImageCompressionRatio", "TransferSyntaxUID", "PatientOrientation", "PatientPosition", "ViewPosition",
          "TableHeight", "TableMotion", "BodyPartExamined", "ProtocolName", "PerformedProcedureStepDescription", "SeriesDescription",
          "AcquisitionDeviceProcessingDescription", "AcquisitionDeviceProcessingCode", "ProcessingFunction", "BurnedInAnnotation",
          "DerivationDescription", "AnodeTargetMaterial", "TableType", "DateOfLastCalibration", "SpatialResolution", "StationName", "DeviceSerialNumber"]
PHI = ["PatientName", "PatientID", "PatientBirthDate", "OtherPatientIDs", "PatientAddress", "InstitutionName", "ReferringPhysicianName",
       "OperatorsName", "PerformingPhysicianName", "InstitutionAddress", "PatientSex", "PatientAge"]
HASHED = {"StationName", "DeviceSerialNumber"}
ROW_COLS = ["file", "device", "modality", "rows", "cols", "bits", "photometric", "intensity_rel", "kvp", "ma", "ms", "mas", "pulse_ms", "sid_mm", "sod_mm",
            "primary_deg", "secondary_deg", "pixel_mm", "imager_pixel_mm", "dap", "entrance_dose_mgy", "fov_shape", "fov_dims", "coll_shape",
            "coll_l", "coll_r", "coll_u", "coll_d", "coll_radius", "n_frames", "frame_time_ms", "radiation_setting", "filter", "focal"]
TEXT_VR = {"AE", "AS", "CS", "DA", "DS", "DT", "IS", "LO", "LT", "PN", "SH", "ST", "TM", "UI", "UT", "UC", "UR"}
NUM_VR = {"FL", "FD", "SL", "SS", "UL", "US", "SV", "UV"}


def _s(v, maxlen=80):
    if v is None:
        return None
    try:
        if isinstance(v, (list, tuple)) or v.__class__.__name__ == "MultiValue":
            v = "\\".join(str(x) for x in v)
    except Exception:  # noqa: BLE001
        pass
    s = str(v)
    return s if len(s) <= maxlen else s[:maxlen] + f"...({len(s)})"


def _f(v):
    try:
        if isinstance(v, (list, tuple)) or v.__class__.__name__ == "MultiValue":
            v = v[0]
        return float(v)
    except Exception:  # noqa: BLE001
        return None


def _hash(s):
    import hashlib
    return hashlib.sha1(str(s).encode()).hexdigest()[:10] if s not in (None, "") else None


def read_header(path):
    import pydicom
    try:
        return pydicom.dcmread(path, force=True, stop_before_pixels=True)
    except Exception:  # noqa: BLE001
        return None


def is_dicom_candidate(path, exts, max_bytes=400_000_000):
    """A file is read as DICOM when it carries the DICM preamble, or when its extension is in `exts` (for vendors that
    write no preamble). The first version admitted EVERY file when no extension list was given, and pydicom with
    force=True then sat on a 100 GB zip for twenty minutes; files above `max_bytes` are never candidates."""
    ext = os.path.splitext(path)[1].lower()
    if exts is not None and ext not in exts:
        return False
    try:
        sz = os.path.getsize(path)
        if sz < 200 or sz > max_bytes:
            return False
        with open(path, "rb") as fh:
            fh.seek(128); pre = fh.read(4)
    except OSError:
        return False
    if pre == b"DICM":
        return True
    return bool(exts) and ext in exts


def private_elements(ds, depth=0):
    """Every private element at the top level and one sequence level down: (tag, creator, VR, length, short value)."""
    out = []
    for el in ds:
        if el.VR == "SQ":
            if depth < 1:
                for item in el.value or []:
                    out.extend(private_elements(item, depth + 1))
            continue
        if not el.tag.is_private:
            continue
        creator = getattr(el, "private_creator", None) or ""
        val = None
        try:
            if el.VR in TEXT_VR or el.VR in NUM_VR:
                val = _s(el.value, 64)
        except Exception:  # noqa: BLE001
            val = None
        try:
            ln = len(el.value) if el.value is not None and not isinstance(el.value, (int, float)) else 1
        except Exception:  # noqa: BLE001
            ln = -1
        out.append((f"({el.tag.group:04x},{el.tag.element:04x})", creator, el.VR, ln, val))
    return out


def frame_row(ds, path, device):
    g = ds.get
    ma = _f(g("XRayTubeCurrent")); ms = _f(g("ExposureTime")); mas = _f(g("Exposure"))
    if ma is None and g("XRayTubeCurrentInuA") is not None:
        ma = _f(g("XRayTubeCurrentInuA")) / 1000.0
    if ms is None and g("ExposureTimeInuS") is not None:
        ms = _f(g("ExposureTimeInuS")) / 1000.0
    if mas is None and g("ExposureInuAs") is not None:
        mas = _f(g("ExposureInuAs")) / 1000.0
    if mas is None and ma is not None and ms is not None:
        mas = ma * ms / 1000.0
    ips = g("ImagerPixelSpacing"); ps = g("PixelSpacing")
    return dict(file=os.path.basename(path), device=device, modality=_s(g("Modality")), rows=_f(g("Rows")), cols=_f(g("Columns")), bits=_f(g("BitsStored")),
                photometric=_s(g("PhotometricInterpretation")), intensity_rel=_s(g("PixelIntensityRelationship")), kvp=_f(g("KVP")), ma=ma, ms=ms, mas=mas,
                pulse_ms=_f(g("AveragePulseWidth")), sid_mm=_f(g("DistanceSourceToDetector")), sod_mm=_f(g("DistanceSourceToPatient")),
                primary_deg=_f(g("PositionerPrimaryAngle")), secondary_deg=_f(g("PositionerSecondaryAngle")), pixel_mm=_f(ps), imager_pixel_mm=_f(ips),
                dap=_f(g("ImageAndFluoroscopyAreaDoseProduct")), entrance_dose_mgy=_f(g("EntranceDoseInmGy")), fov_shape=_s(g("FieldOfViewShape")),
                fov_dims=_s(g("FieldOfViewDimensions")), coll_shape=_s(g("CollimatorShape")), coll_l=_f(g("CollimatorLeftVerticalEdge")),
                coll_r=_f(g("CollimatorRightVerticalEdge")), coll_u=_f(g("CollimatorUpperHorizontalEdge")), coll_d=_f(g("CollimatorLowerHorizontalEdge")),
                coll_radius=_f(g("RadiusOfCircularCollimator")), n_frames=_f(g("NumberOfFrames")), frame_time_ms=_f(g("FrameTime")),
                radiation_setting=_s(g("RadiationSetting")), filter=_s(g("FilterType")) or _s(g("FilterMaterial")), focal=_s(g("FocalSpots")))


def cmd_headers(a):
    exts = set(x.lower() for x in a.ext.split(",") if x != "") if a.ext is not None else None
    files = []
    for dp, dn, fn in os.walk(a.root):
        if any(s and s in dp for s in a.skip_dirs.split(",")):
            continue
        for f in fn:
            p = os.path.join(dp, f)
            if is_dicom_candidate(p, exts):
                files.append(p)
    files.sort()
    if a.limit:
        files = files[: a.limit]
    print(f"{len(files)} candidate files under {a.root}", flush=True)
    excl = set(x.upper() for x in a.exclude_modality.split(",") if x)
    per_dev = collections.defaultdict(lambda: dict(n=0, public=collections.defaultdict(collections.Counter), private=collections.defaultdict(collections.Counter),
                                                   private_creators=collections.Counter(), phi_present=collections.Counter(), rows=[], sop=collections.Counter(),
                                                   files_sample=[]))
    n_read = 0
    for i, p in enumerate(files):
        ds = read_header(p)
        if ds is None or "Modality" not in ds and "Rows" not in ds:
            continue
        mod = str(ds.get("Modality", "")).upper()
        if mod in excl:
            continue
        n_read += 1
        dev = a.name or f"{_s(ds.get('Manufacturer')) or '?'} | {_s(ds.get('ManufacturerModelName')) or '?'}"
        D = per_dev[dev]; D["n"] += 1
        if len(D["files_sample"]) < 5:
            D["files_sample"].append(os.path.relpath(p, a.root))
        for kw in PUBLIC:
            v = ds.get(kw)
            if v is None:
                continue
            D["public"][kw][_hash(v) if kw in HASHED else _s(v)] += 1
        for kw in PHI:
            if kw in ds:
                D["phi_present"][kw] += 1
        for tag, creator, vr, ln, val in private_elements(ds):
            key = f"{tag} {creator} {vr}"
            D["private"][key][val if val is not None else f"<{ln} bytes>"] += 1
            if creator:
                D["private_creators"][creator] += 1
        D["rows"].append(frame_row(ds, p, dev))
        if (i + 1) % 2000 == 0:
            print(f"  {i + 1}/{len(files)} read, {n_read} kept", flush=True)
    os.makedirs(a.out, exist_ok=True)
    for dev, D in per_dev.items():
        name = a.name or "".join(ch if ch.isalnum() else "_" for ch in dev)[:60]
        pub = {kw: dict(n=sum(c.values()), distinct=len(c), values=c.most_common(a.top)) for kw, c in D["public"].items()}
        prv = {k: dict(n=sum(c.values()), distinct=len(c), values=c.most_common(6)) for k, c in sorted(D["private"].items())}
        num = {}
        for col in ["kvp", "ma", "ms", "mas", "pulse_ms", "sid_mm", "sod_mm", "primary_deg", "secondary_deg", "dap", "entrance_dose_mgy", "pixel_mm", "imager_pixel_mm", "frame_time_ms"]:
            v = np.array([r[col] for r in D["rows"] if r[col] is not None], float)
            if v.size:
                num[col] = dict(n=int(v.size), min=float(v.min()), p5=float(np.percentile(v, 5)), median=float(np.median(v)), p95=float(np.percentile(v, 95)), max=float(v.max()))
        card = dict(device=dev, name=name, root=a.root, n_files=D["n"], files_sample=D["files_sample"], public=pub, private=prv,
                    private_creators=D["private_creators"].most_common(), phi_tags_present=dict(D["phi_present"]), numeric=num)
        json.dump(card, open(os.path.join(a.out, f"{name}__headers.json"), "w"), indent=1)
        with open(os.path.join(a.out, f"{name}__frames.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=ROW_COLS); w.writeheader(); w.writerows(D["rows"])
        write_header_card(card, os.path.join(a.out, f"{name}__headers.md"))
        print(f"{name}: {D['n']} files, {len(pub)} public tags, {len(prv)} private tags, creators {[c for c, _ in D['private_creators'].most_common(6)]}", flush=True)
    return 0


def write_header_card(c, path):
    L = [f"# {c['device']} — header census", "", f"{c['n_files']} DICOM headers under `{c['root']}` (samples: {', '.join(c['files_sample'])}).", ""]
    L += ["## Exposure and geometry (per frame)", "", "| field | n | min | p5 | median | p95 | max |", "|---|---:|---:|---:|---:|---:|---:|"]
    for k, v in c["numeric"].items():
        L.append(f"| {k} | {v['n']} | {v['min']:.4g} | {v['p5']:.4g} | {v['median']:.4g} | {v['p95']:.4g} | {v['max']:.4g} |")
    L += ["", "## Public tags", "", "| tag | n | distinct | most common values (count) |", "|---|---:|---:|---|"]
    for k, v in c["public"].items():
        vals = "; ".join(f"{val} ({n})" for val, n in v["values"][:5])
        L.append(f"| {k} | {v['n']} | {v['distinct']} | {vals} |")
    L += ["", f"Identity tags present (values never copied): {c['phi_tags_present']}", "",
          "## Private tags", "", f"Private creators: {c['private_creators']}", "", "| tag creator VR | n | distinct | values |", "|---|---:|---:|---|"]
    for k, v in c["private"].items():
        vals = "; ".join(f"{val} ({n})" for val, n in v["values"][:4])
        L.append(f"| {k} | {v['n']} | {v['distinct']} | {vals} |")
    open(path, "w").write("\n".join(L) + "\n")


def cmd_images(a):
    from PIL import Image
    files = sorted(glob.glob(a.images))
    if a.limit and len(files) > a.limit:
        rng = np.random.default_rng(0); files = sorted(rng.choice(files, a.limit, replace=False).tolist())
    print(f"{a.name}: {len(files)} frames", flush=True)
    shapes, borders, stats, sizes = [], [], [], collections.Counter()
    for i, p in enumerate(files):
        im = np.asarray(Image.open(p).convert("L"), np.float64)
        sizes[im.shape] += 1
        mask = PH.exposed_field(im, polarity=a.polarity)
        sh = PH.field_shape(mask); shapes.append(sh)
        b = PH.border_profile(im, mask, polarity=a.polarity)
        if b:
            borders.append(dict(sigma_p_px=b["sigma_p_px"], halo=b["halo"], profile=b["profile"], t=b["t"], rms_fit=b["rms_fit"]))
        try:
            stats.append(PH.image_stats(im, mask))
        except Exception as e:  # noqa: BLE001
            print(f"  stats failed on {os.path.basename(p)}: {e}", flush=True)
        if (i + 1) % 25 == 0:
            print(f"  {i + 1}/{len(files)}", flush=True)
    pooled = PH.pool_stats(stats)
    sh_ok = [s for s in shapes if s.get("shape")]
    q = lambda v: (dict(p10=float(np.percentile(v, 10)), median=float(np.median(v)), p90=float(np.percentile(v, 90))) if len(v) else None)  # noqa: E731
    out = dict(name=a.name, images=a.images, n=len(files), sizes={str(k): v for k, v in sizes.items()}, polarity=a.polarity,
               field=dict(circle_frac=float(np.mean([s["shape"] == "circle" for s in sh_ok])) if sh_ok else None,
                          field_frac=q([s["field_frac"] for s in sh_ok]), left=q([s["left"] for s in sh_ok]), right=q([s["right"] for s in sh_ok]),
                          top=q([s["top"] for s in sh_ok]), bottom=q([s["bottom"] for s in sh_ok]), radius=q([s["radius"] for s in sh_ok]),
                          centre_u=q([s["centre_u"] for s in sh_ok]), centre_v=q([s["centre_v"] for s in sh_ok])),
               border=dict(n=len(borders), sigma_p_px=q([b["sigma_p_px"] for b in borders]), halo=q([b["halo"] for b in borders]),
                           profile=(np.median(np.array([b["profile"] for b in borders]), 0).round(4).tolist() if borders else None),
                           t=(borders[0]["t"] if borders else None)),
               stats=pooled)
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, f"{a.name}__images.json"), "w"), indent=1)
    fig_images(out, os.path.join(a.out, f"{a.name}__images.png"))
    print(f"{a.name}: field circle {out['field']['circle_frac']}, penumbra sigma {out['border']['sigma_p_px']}, halo {out['border']['halo']}, "
          f"unsharp gain {pooled['halo']['gain'] if pooled and pooled.get('halo') else None}", flush=True)
    return 0


def fig_images(o, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 4, figsize=(16, 3.6))
    if o["border"]["profile"]:
        ax[0].plot(o["border"]["t"], o["border"]["profile"], color="#1f4fb3"); ax[0].axvline(0, color="grey", lw=0.8)
        s = o["border"]["sigma_p_px"]; ax[0].set_title(f"collimator border (sigma_p {s['median']:.2f} px, p10-90 {s['p10']:.2f}-{s['p90']:.2f})", fontsize=9)
        ax[0].set_xlabel("px from border (inward +)"); ax[0].set_ylabel("level / interior")
    st = o.get("stats") or {}
    if st.get("nps"):
        ax[1].plot(st["nps_freq"], st["nps"], color="#b3303a"); ax[1].set_title("radial NPS of flat regions (unit sum)", fontsize=9); ax[1].set_xlabel("cycles / px")
    if st.get("halo"):
        h = st["halo"]; ax[2].plot(h["t"], h["profile"], color="#1e7f4b"); ax[2].axvline(0, color="grey", lw=0.8)
        ax[2].set_title(f"edge profile (unsharp gain {h['gain']:.2f}, radius {h['radius_px']:.1f} px, edge sigma {h['edge_sigma_px']:.2f})", fontsize=9)
        ax[2].set_xlabel("px across strongest edges")
    if st.get("hist"):
        ks = list(st["hist"]); ax[3].bar(range(len(ks)), [st["hist"][k] for k in ks], color="#7b8794"); ax[3].set_xticks(range(len(ks))); ax[3].set_xticklabels(ks, fontsize=8)
        ax[3].set_title("grey percentiles in the field (8-bit display)", fontsize=9)
    f = o["field"]
    fig.suptitle(f"{o['name']}: {o['n']} frames, sizes {o['sizes']}, circle field {f['circle_frac']}, field fraction {f['field_frac']['median'] if f['field_frac'] else None}", fontsize=10)
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)


def cmd_report(a):
    H = {Path(p).name.replace("__headers.json", ""): json.load(open(p)) for p in sorted(glob.glob(os.path.join(a.out, "*__headers.json")))}
    I = {Path(p).name.replace("__images.json", ""): json.load(open(p)) for p in sorted(glob.glob(os.path.join(a.out, "*__images.json")))}
    names = sorted(set(H) | set(I))
    L = ["# Device census", "", "One row per device the project holds frames from. Header columns come from DICOM headers (`<name>__headers.md`), "
         "image columns from the frames alone (`<name>__images.png`). '—' = not recorded / not measured.", "",
         "| device | files | rows x cols | bits | photometric | intensity | pixel mm | kVp (p5–p95) | mA | ms | SID mm | field | circle | penumbra sigma px | halo | unsharp gain / radius | private creators |",
         "|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for n in names:
        h = H.get(n, {}); im = I.get(n, {}); pub = h.get("public", {}); num = h.get("numeric", {})
        first = lambda kw: (pub[kw]["values"][0][0] if kw in pub and pub[kw]["values"] else "—")  # noqa: E731
        rng = lambda k: (f"{num[k]['p5']:.3g}–{num[k]['p95']:.3g}" if k in num else "—")  # noqa: E731
        f = im.get("field", {}); b = im.get("border", {}); st = im.get("stats") or {}
        L.append(f"| {n} | {h.get('n_files', '—')} | {first('Rows')} x {first('Columns')} | {first('BitsStored')} | {first('PhotometricInterpretation')} | "
                 f"{first('PixelIntensityRelationship')} | {first('ImagerPixelSpacing') if 'ImagerPixelSpacing' in pub else first('PixelSpacing')} | {rng('kvp')} | {rng('ma')} | {rng('ms')} | "
                 f"{rng('sid_mm')} | {f.get('field_frac', {}).get('median', '—') if f.get('field_frac') else '—'} | {f.get('circle_frac', '—')} | "
                 f"{b.get('sigma_p_px', {}).get('median', '—') if b.get('sigma_p_px') else '—'} | {b.get('halo', {}).get('median', '—') if b.get('halo') else '—'} | "
                 f"{(str(round(st['halo']['gain'], 2)) + ' / ' + str(round(st['halo']['radius_px'], 1))) if st.get('halo') else '—'} | "
                 f"{', '.join(c for c, _ in h.get('private_creators', [])[:4]) if h.get('private_creators') else '—'} |")
    L += ["", "## Cards", ""]
    for n in names:
        L.append(f"- **{n}**: " + ", ".join(x for x in [f"[headers]({n}__headers.md)" if n in H else "", f"[images]({n}__images.png)" if n in I else "", f"frames.csv" if n in H else ""] if x))
    open(os.path.join(a.out, "README.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L[:12]))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["headers", "images", "report"])
    ap.add_argument("--name", default=None); ap.add_argument("--root", default=None); ap.add_argument("--images", default=None)
    ap.add_argument("--out", default=OUT_DEFAULT); ap.add_argument("--limit", type=int, default=0); ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--ext", default=None, help="comma list of extensions to consider ('' = no extension); default: any file with a DICM preamble")
    ap.add_argument("--exclude-modality", default="CT,MR,SR,PR"); ap.add_argument("--skip-dirs", default="")
    ap.add_argument("--polarity", default="bright_is_more_bone", choices=["bright_is_more_bone", "bright_is_more_photons"])
    a = ap.parse_args()
    return dict(headers=cmd_headers, images=cmd_images, report=cmd_report)[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
