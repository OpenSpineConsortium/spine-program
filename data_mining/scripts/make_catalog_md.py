"""Write data_mining/CATALOG.md: the atlas as Markdown, readable on GitHub without opening the HTML page.
Called by merge_atlas.py with the merged records; it can also be run alone on data_mining/data/*.json."""
import json
import os
import re
from collections import Counter

CAT = [
    ("fluoro_video", "Fluoroscopy video and cine", "Moving fluoroscopy: frame sequences or video, the closest thing to what a C-arm shows during a case."),
    ("fluoro_frames", "Fluoroscopy and C-arm frames", "Single fluoroscopy or C-arm exposures."),
    ("paired_ct_xray_real", "Paired CT and real X-ray", "The same body imaged by CT and by radiograph or fluoroscopy. With pose, these test 3-D to 2-D parity directly."),
    ("cbct_projections", "CBCT projections", "Raw cone-beam projection stacks: many calibrated C-arm-like views around one volume."),
    ("paired_ct_drr_synthetic", "Paired CT and synthetic X-ray (DRR)", "Released datasets of radiographs rendered from CT, and your own render banks."),
    ("radiograph", "Spine radiographs", "Plain films: the same projection physics as a C-arm, a different detector, dose and field of view."),
    ("private_request", "By request only", "Data that exists but is held privately; a letter is the only route."),
]
STATUS = {"held": "held", "requested (letter drafted)": "request ready", "not held": "not held"}
# keep in step with NEXT in atlas_template.html
NEXT = [
    ("COVID-19-NY-SBU", "You already hold the CTs of 439 patients. Fetching their CR/DX radiographs from the same TCIA collection gives same-patient CT and X-ray pairs with no request at all."),
    ("LUMOS", "1,620 real lumbar AP and lateral films in DICOM, with 280 lumbar CTs from the same cohort. Open download, CC BY-NC. Which film goes with which CT is not stated."),
    ("MIDRC Open Data", "10,100 living cases with both CT and a radiograph of the same patient, about 300 of them spine radiograph studies. Free registration and a click-through agreement. No pose."),
    ("Balgrist ex-vivo", "13 soft-tissue torsos, about 1,000 real shots on a Siemens Cios Spin and two Ziehm C-arms, with poses from implanted fiducials. The best fit that exists; request letter 15 is ready."),
    ("UCLA kV/MV", "254 living patients, 2,486 orthogonal kV pairs of the thoraco-abdominal spine registered to the planning CT. Request only; the authors call the data sensitive."),
    ("PENGWIN Task 2", "50,000 unwindowed DRRs in C-arm geometry with simulated K-wires and screws and sacrum masks. CC BY 4.0, 35 GB. Tests robustness to surgical hardware."),
    ("SyntheX deposit", "Simulated hip images matched in geometry to real C-arm frames from two systems. A benchmark for your own render physics. Open, CC BY-NC."),
    ("SPARE", "Real Varian and Elekta kV projections with per-projection geometry and a prior 4D-CT. Open, CC BY-NC; you register the CT to the projections yourself."),
    ("LIDC-IDRI", "290 patients with CT and a chest radiograph of the same patient. Open on TCIA."),
    ("Femur multi-view", "Five cadaveric distal femurs with CT and fiducial-calibrated X-rays from a Siemens Fluorospot Compact. Downloadable now under a research-only licence; no spine."),
]
REQ_FILE = "../01_carm_level_detection/docs/data_requests/FLUORO_VIDEO_REQUESTS_READY_2026-09-26.md"


def cell(x):
    if x is None or x == "":
        return ""
    return re.sub(r"\s+", " ", str(x)).replace("|", "\\|").strip()


def links(d):
    out = []
    if d.get("link") and re.match(r"^https?://", d["link"]):
        out.append(f"[page]({d['link']})")
    p = d.get("paper") or ""
    doi = re.search(r"10\.\d{4,9}/[^\s;,)]+", p)
    arx = re.search(r"arXiv[: ]\s*(\d{4}\.\d{4,5})", p, re.I)
    if doi:
        out.append(f"[paper](https://doi.org/{doi.group(0).rstrip('.')})")
    elif arx:
        out.append(f"[arXiv {arx.group(1)}](https://arxiv.org/abs/{arx.group(1)})")
    return " ".join(out)


def flags(d):
    f = []
    if d.get("level_labels") is True:
        f.append("levels named")
    if d.get("pose_geometry") is True:
        f.append("pose known")
    if d.get("verified") is False:
        f.append("link not opened")
    return ", ".join(f)


def write(datasets, reqs, path):
    L = []
    w = L.append
    w("# Fluoroscopy Data Atlas: catalog")
    w("")
    w("Every fluoroscopy, spine radiograph, paired CT and X-ray, CBCT projection and DRR dataset found for intraoperative "
      "vertebral level identification, as of 17 October 2026, with what is already on the grid and how to get the rest. "
      "This file is the same records as [`fluoroscopy_data_atlas.html`](fluoroscopy_data_atlas.html), which adds search and filters "
      "(download it and open it in a browser; [README.md](README.md) says how).")
    w("")
    w("**Status**: *held* means present under `/rs/rs_grp_oschome/go2432/data/` on the Wayne State grid, readable by approved students; "
      "*request ready* means a letter is drafted; *not held* means you do not have it. **Flags**: *levels named* (spinal levels are labelled), "
      "*pose known* (projection geometry links each X-ray to its CT or to the C-arm), *link not opened* (from search results only).")
    w("")
    w("## Summary")
    w("")
    w("| Kind | Datasets | Held | Request ready | Not held |")
    w("|---|---:|---:|---:|---:|")
    for k, name, _ in CAT:
        ds = [d for d in datasets if d["category"] == k]
        if not ds:
            continue
        c = Counter(STATUS.get(d["greg_status"], "not held") for d in ds)
        w(f"| [{name}](#{re.sub(r'[^a-z0-9 -]', '', name.lower()).replace(' ', '-')}) | {len(ds)} | {c['held']} | {c['request ready']} | {c['not held']} |")
    c = Counter(STATUS.get(d["greg_status"], "not held") for d in datasets)
    w(f"| **All** | **{len(datasets)}** | **{c['held']}** | **{c['request ready']}** | **{c['not held']}** |")
    w("")
    w("## Worth getting next")
    w("")
    for i, (key, why) in enumerate(NEXT, 1):
        d = next((x for x in datasets if key in (x.get("name") or "")), None)
        nm = d["name"] if d else key
        extra = (" " + links(d)) if d and links(d) else ""
        acc = f" *{d['access']}*." if d and d.get("access") else ""
        w(f"{i}. **{cell(nm)}**.{acc} {why}{extra}")
    w("")
    w("## Requests to send")
    w("")
    w(f"Sixteen sources can only be had by asking. The letters, with what to expect from each, are in [{os.path.basename(REQ_FILE)}]({REQ_FILE}) "
      "and, for Balgrist and SX-Stitch, beside it in the same folder. Eleven also exist as unsent Outlook drafts in "
      "`spinesurg-ct-nnunet/docs/fluoro_requests_eml/` on Greg's laptop. The HTML page carries every letter with a copy button.")
    w("")
    w("**Radiopaedia (request 8).** Seven multi-frame spine fluoroscopy cases, among them rID 24796 (a rotational C-arm spin), "
      "rID 90103 (a 61-projection oblique lumbar puncture series) and rID 21585 (a lateral L1 vertebroplasty series).")
    w("")
    w("1. Open [radiopaedia.org/licence](https://radiopaedia.org/licence) in your own browser and read the current machine-learning terms.")
    w("2. File their application for non-commercial machine-learning use, or email the licensing team with letter 8. Published studies cite "
      "`license@radiopaedia.org` and an approval under \"Non-commercial use of Radiopaedia content for Machine Learning\"; confirm the address on the page.")
    w("3. Expect a non-refundable fee: the draft recorded USD 250, which could not be confirmed from public sources on 17 October 2026.")
    w("4. Save no frames before approval: their terms bar scripted downloading, and validating the 510(k) product would need a separately negotiated licence.")
    w("")
    w("| # | Source | What it gets you | Route | Status |")
    w("|---:|---|---|---|---|")
    for r in reqs:
        w(f"| {r['n']} | {cell(r.get('title'))} | {cell(r.get('gets'))} | {cell((r.get('route') or '').replace('`', ''))} | {cell((r.get('status') or '').replace('**', ''))} |")
    w("")
    w("Before sending: the letters say non-commercial academic use (change that if the data might validate the product); ask the WSU IRB whether "
      "data received under a data-use agreement falls under the existing not-human-research determination; letters 1 to 3 promise no training on "
      "the data and letters 1 to 4 offer co-authorship.")
    for k, name, desc in CAT:
        ds = [d for d in datasets if d["category"] == k]
        if not ds:
            continue
        order = {"held": 0, "requested (letter drafted)": 1, "not held": 2}
        ds.sort(key=lambda d: (order.get(d["greg_status"], 2), d.get("level_labels") is not True, d.get("pose_geometry") is not True, d["name"].lower()))
        w("")
        w(f"## {name}")
        w("")
        w(f"{desc} {len(ds)} datasets.")
        w("")
        w("| Dataset | Status | Anatomy | Annotation | Image quality | Access | Flags | Links |")
        w("|---|---|---|---|---|---|---|---|")
        for d in ds:
            ann = cell(d.get("annotation_level"))
            if d.get("annotation_detail"):
                ann = f"{ann}: {cell(d['annotation_detail'])}" if ann else cell(d["annotation_detail"])
            w(f"| **{cell(d['name'])}**{(' (' + cell(d['aka']) + ')') if d.get('aka') else ''} | {STATUS.get(d['greg_status'], 'not held')} | "
              f"{cell(d.get('anatomy'))} | {ann} | {cell(d.get('image_quality'))} | {cell(d.get('access'))} | {flags(d)} | {links(d)} |")
        w("")
        w("<details><summary>How to get each one, and what to watch for</summary>")
        w("")
        for d in ds:
            bits = []
            if d.get("size"):
                bits.append(f"Size: {cell(d['size'])}.")
            if d.get("how_to_get"):
                bits.append(f"How to get it: {cell(d['how_to_get'])}")
            if d.get("license"):
                bits.append(f"Licence: {cell(d['license'])}.")
            if d.get("grid_path"):
                bits.append(f"On the grid: `{cell(d['grid_path'])}`.")
            if d.get("notes"):
                bits.append(cell(d["notes"]))
            if d.get("paper"):
                bits.append(f"Paper: {cell(d['paper'])}")
            w(f"- **{cell(d['name'])}**. " + " ".join(bits))
        w("")
        w("</details>")
    w("")
    w("## How this was built")
    w("")
    w("From Greg's records (spinesurg-ct-nnunet `data_platform/DATA_MANIFEST.md` and `sources.json`, `HANDOFF/literature_state/`, "
      "this repository's `01_carm_level_detection/docs/data_requests/`, `FLUORO_VIDEO_SOURCES_2026-09-26.md` and `docs/external_reports/`, "
      "and the project memory notes), and from a web search on 17 October 2026. Rebuild with `python data_mining/scripts/merge_atlas.py`; "
      "[README.md](README.md) explains the inputs.")
    text = "\n".join(L) + "\n"
    assert ("proven" + "ance") not in text.lower(), "banned word in CATALOG.md"
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    return len(text)


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ds = json.load(open(os.path.join(here, "data", "datasets.json"), encoding="utf-8"))
    rq = json.load(open(os.path.join(here, "data", "requests.json"), encoding="utf-8"))
    print("CATALOG.md bytes:", write(ds, rq, os.path.join(here, "CATALOG.md")))
