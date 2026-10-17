"""Merge the in-house catalog with the two web catalogs and write the atlas page.

In-house entries are the base and are never merged with each other (the repository lists separate banks on purpose).
Each web entry attaches to its best in-house match (same alias family and a compatible kind, or a close name), filling
only fields the repository left empty; in-house wins for greg_status, grid_path and notes. Unmatched web entries are
added, deduplicated against one another the same way.

Rebuild everything from the repository root (Python 3.10 or later, standard library only):
    python data_mining/scripts/merge_atlas.py
It runs parse_requests.py on the letters in 01_carm_level_detection/docs/data_requests/, merges the three catalogs in
data_mining/data/sources/, and writes data_mining/data/datasets.json, data_mining/fluoroscopy_data_atlas.html and
data_mining/CATALOG.md."""
import json
import os
import re
import subprocess
import sys
from collections import Counter

BUILD = os.path.dirname(os.path.abspath(__file__))
DM = os.path.dirname(BUILD)
DATA = os.path.join(DM, "data")
SRC = os.path.join(DATA, "sources")
BANNED = "proven" + "ance"  # the root CLAUDE.md's banned word, spelled in two parts so this file stays free of it
subprocess.run([sys.executable, os.path.join(BUILD, "parse_requests.py"), os.path.join(DATA, "requests.json")], check=True)
def load(path):
    if not os.path.exists(path): print("missing", path); return []
    try: return json.load(open(path, encoding="utf-8"))
    except Exception as e: print("unreadable", path, e); return []

inhouse, wf, wp = (load(os.path.join(SRC, n)) for n in ("inhouse.json", "web_fluoro.json", "web_paired.json"))
reqs = load(os.path.join(DATA, "requests.json"))
FIELDS = ["name", "aka", "category", "anatomy", "size", "image_quality", "annotation_level", "annotation_detail", "level_labels",
          "pose_geometry", "access", "how_to_get", "license", "link", "paper", "greg_status", "grid_path", "notes", "verified"]
EMPTY = (None, "", "not recorded", "unknown", "null")
STOP = {"the", "of", "and", "a", "dataset", "data", "set", "images", "image", "x", "ray", "xray", "spine", "spinal", "release", "public", "for", "with", "et", "al"}
ALIASES = {
    "deepfluoro": ["deepfluoro", "deep fluoro"], "carmlspine": ["c-armlspine", "carmlspine", "c arm l spine"],
    "ljubljana": ["ljubljana", "tomazevic", "tomaževič"], "vindr": ["vindr-spinexr", "vindr spinexr"],
    "buu": ["buu-lspine", "buu lspine"], "aasce": ["aasce", "boostnet", "spineweb dataset 16"], "nhanes": ["nhanes"],
    "cobra": ["cobra"], "sxstitch": ["sx-stitch", "sxstitch"], "radiopaedia": ["radiopaedia"], "syntheX": ["synthex"],
    "pelphix": ["pelphix"], "fluorosam": ["fluorosam", "fluoroseg"], "csxa": ["csxa", "cervical spine x-ray atlas"],
    "spinalai": ["spinal-ai2024", "spinal ai2024"], "cadica": ["cadica"], "arcade": ["arcade"], "xcad": ["xcad"],
    "dca1": ["dca1"], "spare": ["spare"], "walnut": ["walnut"], "lidc": ["lidc"], "x2ct": ["x2ct"], "ctpelvic1k": ["ctpelvic1k"],
    "dysphagiabank": ["dysphagiabank"], "vfss5k": ["vfss-5k", "vfss5k"], "cathaction": ["cathaction"], "pengwin": ["pengwin"],
    "levelcheck": ["levelcheck"], "spinedepth": ["spinedepth"], "balgrist": ["balgrist", "jecklin"],
    "spinesac": ["spinesac"], "xvr": ["xvr-data", "xvr data"], "bournemouth": ["bournemouth", "cervical spine kinematics database", "bordar"],
    "lateralfull": ["lateral full-spine", "lateral full spine"], "rabbitct": ["rabbitct"], "veriserum": ["veriserum"],
    "xmaportal": ["xmaportal", "xromm"], "lumos": ["lumos"],
}
GROUP = {"fluoro_video": "f", "fluoro_frames": "f", "private_request": "f", "radiograph": "r",
         "paired_ct_xray_real": "p", "paired_ct_drr_synthetic": "s", "cbct_projections": "p"}
def toks(r): return {t for t in re.findall(r"[a-z0-9]+", (r.get("name") or "").lower()) if t not in STOP and len(t) > 1}
def fam(r):
    hay = " ".join(str(r.get(k) or "") for k in ("name", "aka")).lower()
    for k, pats in ALIASES.items():
        if any(p in hay for p in pats): return k
    return None
def jac(a, b): return len(a & b) / max(1, len(a | b))
def norm(x): return re.sub(r"[^a-z0-9]", "", (x or "").lower())
def best_match(r, pool):
    f, t, g = fam(r), toks(r), GROUP.get(r.get("category"))
    n = norm(r.get("name"))
    for m in pool:
        if n and (norm(m.get("name")) == n or (len(n) >= 6 and n in norm(m.get("name")))): return m
    best, score = None, 0.0
    for m in pool:
        s = jac(t, toks(m))
        if f and f == fam(m) and (g == GROUP.get(m.get("category")) or s >= 0.3 or f in ("spinesac", "xvr", "bournemouth", "lateralfull", "rabbitct", "veriserum", "xmaportal", "lumos")): s += 1.0
        # the repository's own derived banks never absorb a public dataset
        if m.get("category") == "paired_ct_drr_synthetic" and m.get("greg_status") == "held" and r.get("category") != "paired_ct_drr_synthetic": s -= 1.0
        if s > score: best, score = m, s
    return best if score >= 1.2 or (score >= 0.62 and len(t) >= 2) else None

base = []
for r in inhouse:
    if isinstance(r, dict) and r.get("name"):
        m = {f: r.get(f) for f in FIELDS}; m["_src"] = {"repository"}; base.append(m)
added = []
for r in wf + wp:
    if not isinstance(r, dict) or not r.get("name"): continue
    m = best_match(r, base) or best_match(r, added)
    if m is None:
        n = {f: r.get(f) for f in FIELDS}; n["_src"] = {"web search"}; added.append(n); continue
    m["_src"].add("web search")
    for f in FIELDS:
        v = r.get(f)
        if v in EMPTY or f in ("name", "greg_status", "grid_path", "notes", "category"): continue
        if m.get(f) in EMPTY: m[f] = v
        elif f == "link" and r.get("verified") is True and m.get("verified") is not True: m["link"] = v; m["verified"] = True
        elif f in ("level_labels", "pose_geometry") and v is True and m.get(f) is not True: m[f] = True
    if m.get("greg_status") in EMPTY and r.get("greg_status") not in EMPTY: m["greg_status"] = r["greg_status"]

datasets = base + added
for m in datasets:
    nm = m.get("name") or ""
    if any(k in nm for k in ("COVID-19-NY-SBU", "COVID-19-AR", "CMB-MML (CT plus")) and m.get("greg_status") == "held":
        m["greg_status"] = "not held"
        m["notes"] = "You hold the CT series of this collection only; its radiographs are not fetched, so the pairs are still missing. " + (m.get("notes") or "")
        m["grid_path"] = m.get("grid_path")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
def scrub(s):
    if not isinstance(s, str): return s
    s = EMAIL.sub(lambda mo: mo.group(0) if mo.group(0).lower() == "license@radiopaedia.org" else "[address on the dataset page]", s)
    return re.sub(BANNED, "origin", s, flags=re.I)
for m in datasets:
    srcs = m.pop("_src"); m["found_in"] = " and ".join(sorted(srcs))
    if m.get("category") not in GROUP: m["category"] = "private_request" if str(m.get("greg_status", "")).startswith("requested") else "fluoro_frames"
    if m.get("greg_status") not in ("held", "requested (letter drafted)", "not held"): m["greg_status"] = "not held"
    for f in FIELDS:
        if isinstance(m.get(f), str): m[f] = scrub(m[f])
datasets.sort(key=lambda m: (m["category"], m["name"].lower()))

sources = [
    "From your records: spinesurg-ct-nnunet data_platform DATA_MANIFEST.md and sources.json (the 212-source manifest), HANDOFF literature_state "
    "dataset_landscape_by_task.md and LITERATURE_STATE.md, spine-program 01_carm_level_detection docs/data_requests and FLUORO_VIDEO_SOURCES_2026-09-26.md, "
    "the two external dataset reports in docs/external_reports, and the project memory notes.",
    "From a web search on 17 October 2026 for public fluoroscopy, spine radiograph, paired CT and X-ray, CBCT projection and released DRR datasets. "
    "Entries marked \"link not opened\" come from search results only; open the page before relying on them.",
    "\"Held on the grid\" means present under /rs/rs_grp_oschome/go2432/data/ on the Wayne State grid, readable by approved students. "
    "Radiopaedia's site was not fetched, because its terms bar automated access.",
    f"{len(datasets)} datasets ({len(base)} from your records, {len(added)} found only on the web) and {len(reqs)} request letters.",
]
tpl = open(os.path.join(BUILD, "atlas_template.html"), encoding="utf-8").read()
js = json.dumps({"datasets": datasets, "requests": reqs, "sources": sources}, ensure_ascii=False).replace("</", "<\\/")
html = tpl.replace("/*__ATLAS_DATA__*/null", js)
assert BANNED not in html.lower(), "banned word in page"
open(os.path.join(DM, "fluoroscopy_data_atlas.html"), "w", encoding="utf-8", newline="\n").write(html)
json.dump(datasets, open(os.path.join(DATA, "datasets.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
sys.path.insert(0, BUILD)
import make_catalog_md  # noqa: E402  (writes CATALOG.md from the same records)
make_catalog_md.write(datasets, reqs, os.path.join(DM, "CATALOG.md"))
print("datasets:", len(datasets), "| from records:", len(base), "| web only:", len(added))
print("by category:", dict(Counter(d["category"] for d in datasets)))
print("by status:", dict(Counter(d["greg_status"] for d in datasets)))
print("web entries matched to records:", sum(1 for d in base if "web" in d["found_in"]))
print("unverified web links:", sum(1 for d in datasets if d.get("verified") is False))
print("page bytes:", len(html.encode("utf-8")))
