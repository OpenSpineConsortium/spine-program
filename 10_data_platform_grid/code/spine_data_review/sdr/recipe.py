"""Generate the download recipe (SO3) from the charting records: recipe/download_all.sh, recipe/datasets/<id>.sh, recipe/manifest.csv.

WHY A GENERATOR AND NOT A HAND-WRITTEN SCRIPT. The recipe is a product of the charting records
(PROTOCOL.md section 2, SO3): a dataset's download method is a function of its verified
`access_route`, its `access_url` host and the checksums enrichment found, and nothing else; a
hand-written script would let a route be typed that the probe never observed. This module reads
`charting/datasets/*.json`, plans one action per dataset, renders one idempotent bash script per
dataset and one driver, and writes a manifest of every dataset with its route and what the recipe
does about it. Rerunning on the same records gives byte-identical output; the only date in it is
`--run-date`. Nothing here touches the network at generation time; the review downloads nothing.

WHAT EACH SCRIPT DOES. `open-download` datasets are fetched by the method their host supports: a
file list baked in from `checksums[]` when enrichment recorded one (URL, md5/sha256, size), else a
run-time listing through the repository's own API (Zenodo, Figshare, Mendeley Data, PhysioNet,
TCIA/NBIA, Dryad, OSF, Hugging Face, GitHub). `registration` datasets are fetched when the
credentialed client is configured (kaggle CLI, hf/huggingface-cli with a token), else they print the
registration step. The other routes print the manual step and exit 10, which the driver counts as
`manual`, not failure. Every fetch skips a file that exists and verifies (checksum, else size, else
non-empty), resumes a partial download, and verifies after fetching. Order is SAP A7 (see
`order_plans`). `DRY_RUN=1` makes no network call at all: a script prints the listing endpoint it
would query and the files it would fetch from a baked-in list, then exits 0 (or 10 for a manual
step); a listing or a fetch the host answers with an HTTP error exits 5 with `.recipe_status=failed`
(hf-cli, kaggle-cli and git-clone propagate their client's own exit status instead).

INPUTS, stated for the integrator: `charting/datasets/<id>.json` or a `.jsonl` of the same records
(`--datasets`); optional `analysis/quality.json` as sdr.quality writes it, `per_dataset.<id>.total`
a number and `per_dataset.<id>.fit_level_id` a boolean (the `{value: ...}` wrapping that sdr.stats
uses in quality_analysis.json is also accepted, as is a top-level mapping, a `datasets` key or a row
list, because a bare scalar and a wrapped one must sort identically); optional
`charting/enrichment/<id>.json` with a `files` list of `{name|file, url, size_bytes, md5, sha256}`
supplementing `checksums[]`. `access_route` is read from the charting record (the verified value),
never from a probe file. README.md in recipe/ tabulates route -> action -> method.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit

from sdr import PROTOCOL_VERSION
from sdr.common import add_common_args, init_run_dir, review_root

REACHABLE = ("open-download", "registration")
DATA_EXT = re.compile(r"\.(dcm|nii|nii\.gz|nrrd|mha|tif|tiff|png|jpe?g|zip|tar|gz|tgz|7z|rar)$", re.I)
API_METHOD = {"zenodo": "zenodo-api", "figshare": "figshare-api", "mendeley": "mendeley-api", "dryad": "dryad-zip",
              "osf": "osf-zip", "physionet": "physionet-wget", "tcia": "nbia-rest", "hf": "hf-cli", "github": "git-clone"}
MANIFEST_COLUMNS = ["recipe_order", "dataset_id", "name", "modality", "region", "n_subjects", "access_route",
                    "access_route_rule", "host_type", "host_key", "access_url", "recipe_action", "download_method",
                    "verification", "n_files_known", "size_gb", "licence_text", "licence_tier", "on_grid",
                    "fit_level_id", "quality_total", "script", "manual_step"]
_HOSTS = (("zenodo", "zenodo.org", "10.5281/"), ("figshare", "figshare.com", "10.6084/"), ("dryad", "datadryad.org", "10.5061/"),
          ("osf", "osf.io", "10.17605/"), ("mendeley", "data.mendeley.com", "10.17632/"), ("physionet", "physionet.org", "10.13026/"),
          ("tcia", "cancerimagingarchive.net", "10.7937/"), ("hf", "huggingface.co", None), ("kaggle", "kaggle.com", None),
          ("gc", "grand-challenge.org", None), ("github", "github.com", None))


# ----------------------------------------------------------------------------- host routing
# candidate for common.py: sdr/probe.py routes the same URLs through the protocol section-10 table.
def host_key(url: str | None, doi: str | None = None) -> str:
    """The recipe's download family for a landing URL or data DOI (protocol section 10 host
    table): zenodo, figshare, dryad, osf, mendeley, physionet, tcia, hf, kaggle, gc, github, generic."""
    host, d = urlsplit((url or "").lower()).netloc, (doi or "").lower()
    for key, h, prefix in _HOSTS:
        if host == h or host.endswith("." + h) or (prefix and d.startswith(prefix)):
            return key
    return "generic"


def _parts(url: str | None) -> list[str]:
    return [p for p in urlsplit(url or "").path.split("/") if p]


def _native_id(key: str, url: str | None, doi: str | None) -> str | None:
    """The identifier the host's API or client takes: Zenodo record id, Figshare article id, Mendeley
    Data `id` or `id/version`, OSF guid, PhysioNet slug/version, TCIA collection slug, HF repo id,
    Kaggle `datasets:owner/slug` or `competitions:slug`, GitHub owner/repo, Dryad DOI. None when the
    URL carries none."""
    P, d, u = _parts(url), doi or "", url or ""
    m = None
    if key == "zenodo":
        m = re.search(r"zenodo\.(\d+)", d) or re.search(r"/(?:records?/|doi/10\.5281/zenodo\.)(\d+)", u)
    elif key == "figshare":
        m = re.search(r"figshare\.(\d+)", d) or re.search(r"/(\d{6,})", u)
    elif key == "mendeley":   # data.mendeley.com/datasets/<id>[/<v>] or DOI 10.17632/<id>.<v>. The files API
        # REQUIRES a version (without one it answers HTTP 200 with the body {"error": 400}); when the URL and
        # the DOI carry none, the id alone is returned here and the script resolves the latest at run time.
        m = re.search(r"10\.17632/([a-z0-9]+)(?:\.(\d+))?", d, re.I) or re.search(r"/datasets/([a-z0-9]+)(?:/(\d+))?", u, re.I)
        return m.group(1).lower() + (f"/{m.group(2)}" if m.group(2) else "") if m else None
    elif key == "dryad":
        m = re.search(r"10\.5061/\S+", d) or re.search(r"(10\.5061/[^?#]+)", u)
        return m.group(0).rstrip("/") if m else None
    elif key == "osf":
        return P[0] if P and re.fullmatch(r"[a-z0-9]{5}", P[0]) else None
    elif key == "physionet":
        return "/".join(P[1:3]) if len(P) >= 2 and P[0] in ("content", "files") else None
    elif key == "tcia":
        return P[1] if len(P) >= 2 and P[0] == "collection" else None
    elif key == "hf":
        return "/".join(P[1:3]) if len(P) >= 3 and P[0] == "datasets" else None
    elif key == "kaggle":
        if P[:1] == ["datasets"] and len(P) >= 3:
            return "datasets:" + "/".join(P[1:3])
        return "competitions:" + P[1] if P[:1] in (["competitions"], ["c"]) and len(P) >= 2 else None
    elif key == "github":
        return "/".join(P[:2]) if len(P) >= 2 else None
    return m.group(1) if m else None

# ----------------------------------------------------------------------------- plan
@dataclass
class Plan:
    """What the recipe does for one dataset, derived from its charting record and nothing else."""
    id: str
    name: str
    route: str
    rule: str
    host_type: str
    key: str
    url: str | None
    action: str = "unavailable"     # download | registration | manual-dua | manual-request | unavailable | commercial
    method: str = "none"            # files | zenodo-api | ... | kaggle-cli | browser | none
    files: list[dict] = field(default_factory=list)
    manual: str = ""
    native: str | None = None
    fit: bool | None = None
    quality: float | None = None
    on_grid: str = "unknown"
    record: dict = field(default_factory=dict)

    @property
    def verification(self) -> str:
        """What the script checks after a fetch: the strongest published checksum in `files`, else
        the host API's checksum at run time, else what the client itself checks (not a published
        value the review recorded), else non-empty, else nothing (kaggle, browser steps)."""
        for k in ("sha256", "md5", "size_bytes"):
            if any(f.get(k) for f in self.files):
                return k.replace("_bytes", "")
        return {"zenodo-api": "md5 (API, run time)", "figshare-api": "md5 (API, run time)", "mendeley-api": "sha256 (API, run time)",
                "physionet-wget": "sha256 (SHA256SUMS.txt)", "hf-cli": "client (not a published checksum)",
                "git-clone": "client (not a published checksum)", "kaggle-cli": "none", "browser": "none",
                "none": "none"}.get(self.method, "non-empty")


def _files(rec: dict, enrich: dict | None) -> list[dict]:
    """Files with a URL from `checksums[]` then the enrichment `files` list; unique by URL, sorted."""
    out: dict[str, dict] = {}
    for f in list(rec.get("checksums") or []) + list((enrich or {}).get("files") or []):
        if f.get("url") and f["url"] not in out:
            out[f["url"]] = {"file": f.get("file") or f.get("name") or _parts(f["url"])[-1], "url": f["url"],
                             "size_bytes": f.get("size_bytes"), "md5": f.get("md5"), "sha256": f.get("sha256")}
    return sorted(out.values(), key=lambda f: (f["file"], f["url"]))


def _one(url: str) -> list[dict]:
    return [{"file": _parts(url)[-1], "url": url, "size_bytes": None, "md5": None, "sha256": None}]


def _val(x):
    """A quality field as sdr.quality writes it (a scalar) or as sdr.stats wraps it (`{value: ...}`).
    A nonzero total is truthy, so `(x or {}).get` on the scalar shape raised; this is shape-agnostic."""
    return x.get("value") if isinstance(x, dict) else x


def make_plan(rec: dict, quality: dict | None, enrich: dict | None) -> Plan:
    """Route + host -> action and method; the rules README.md tabulates."""
    url = rec.get("access_url")
    doi = (rec.get("versioning") or {}).get("dataset_doi") or (rec.get("source_record") or {}).get("doi")
    key = host_key(url, doi)
    p = Plan(rec["id"], rec.get("name", rec["id"]), rec.get("access_route", "unavailable"), rec.get("access_route_rule", ""),
             rec.get("host_type", "unknown"), key, url, files=_files(rec, enrich), native=_native_id(key, url, doi),
             on_grid=(rec.get("on_grid") or {}).get("status", "unknown"), record=rec)
    q = (quality or {}).get(p.id) or {}
    p.fit, p.quality = _val(q.get("fit_level_id")), _val(q.get("total"))
    last = next((pr.get("http_status") for pr in reversed(rec.get("access_probe") or []) if pr.get("http_status")), None)
    src = doi or url or p.name
    if p.route == "open-download":
        p.action = "download"
        if p.files:
            p.method = "files"
        elif key in API_METHOD and p.native:
            p.method = API_METHOD[key]
        elif rec.get("file_url_probed"):
            p.method, p.files = "files", _one(rec["file_url_probed"])
        elif url and DATA_EXT.search(urlsplit(url).path):
            p.method, p.files = "files", _one(url)
        else:
            p.method, p.manual = "browser", (f"open {url} in a browser: the probe classified it open-download ({p.rule}) "
                                             f"but no file URL was recorded; download the files and place them under $DEST")
    elif p.route == "registration":
        p.action = "registration"
        if key in ("kaggle", "hf") and p.native:
            p.method = "kaggle-cli" if key == "kaggle" else "hf-cli"
        else:
            p.method, p.manual = "browser", f"register at {url} and download through the site; then place the files under $DEST"
    elif p.route == "data-use-agreement":
        p.action, p.manual = "manual-dua", (f"a data-use agreement governs access at {url or src}; the review signed none "
                                            f"(protocol section 8); apply, and after approval place the files under $DEST")
    elif p.route == "request-to-authors":
        p.action, p.manual = "manual-request", (f"the images are available on request from the authors of {src}; the review sent "
                                                f"no request (an unrequested outcome, protocol section 16); write to the "
                                                f"corresponding author and place the files under $DEST")
    elif p.route == "commercial":
        p.action, p.manual = "commercial", f"commercial terms at {url or src}; this recipe does not purchase data"
    else:
        p.manual = (f"unavailable on both probe dates ({p.rule}; last HTTP status {last}); nothing to download; "
                    f"see notes in charting/datasets/{p.id}.json")
    return p


def order_plans(plans: list[Plan]) -> list[Plan]:
    """SAP A7 first-run order (see the module docstring)."""
    def tier(p: Plan) -> int:
        return 0 if p.route in REACHABLE and p.fit and p.on_grid in ("no", "unknown") else 1 if p.route in REACHABLE else 2
    return sorted(plans, key=lambda p: (tier(p), -(p.quality if p.quality is not None else -1), p.id))


# ----------------------------------------------------------------------------- rendering
Q = shlex.quote
HELPERS = r'''DATA_ROOT="${DATA_ROOT:-$HOME/data}"
DRY_RUN="${DRY_RUN:-0}"
DEST="$DATA_ROOT/$DATASET_ID"
log(){ printf '[%s] %s\n' "$DATASET_ID" "$*"; }
need(){ command -v "$1" >/dev/null 2>&1 || { log "missing tool: $1 ($2)"; exit 3; }; }
status(){ [ "$DRY_RUN" = 1 ] && return 0; mkdir -p "$DEST"; printf '%s\n' "$1" > "$DEST/.recipe_status"; }
manual(){ log "MANUAL STEP: $*"; status manual; exit 10; }   # exit 10 = a person must act; not a failure
finish(){ status downloaded; log "done: $DEST"; }
verify(){ # file md5 sha256 size -> 0 when the strongest published check passes
  local f=$1 md5=$2 sha=$3 size=$4
  if [ -n "$sha" ]; then [ "$(sha256sum "$f" | cut -d' ' -f1)" = "$sha" ]; return; fi
  if [ -n "$md5" ]; then [ "$(md5sum "$f" | cut -d' ' -f1)" = "$md5" ]; return; fi
  if [ -n "$size" ]; then [ "$(stat -c %s "$f")" = "$size" ]; return; fi
  [ -s "$f" ]; }
fetch(){ # url out [md5] [sha256] [size]: skip when present and verified, resume a partial, verify after
  local url=$1 out=$2 md5=${3:-} sha=${4:-} size=${5:-} rc=0
  if [ -f "$out" ] && verify "$out" "$md5" "$sha" "$size"; then log "exists, verified: ${out#$DEST/}"; return 0; fi
  if [ "$DRY_RUN" = 1 ]; then log "would fetch $url -> ${out#$DEST/}${sha:+ (sha256)}${md5:+ (md5)}${size:+ (size $size)}"; return 0; fi
  need curl "https://curl.se"; mkdir -p "$(dirname "$out")"
  # A host that answers 4xx/5xx gives curl 22; that is "the record is not there", not a transport fault, and it
  # must leave .recipe_status=failed behind (set -e alone would exit 22 silently). $out.part is kept, for -C -.
  curl -fL --retry 5 --retry-delay 5 -C - ${RECIPE_AUTH_HEADER:+-H "$RECIPE_AUTH_HEADER"} -o "$out.part" "$url" || rc=$?
  if [ "$rc" != 0 ]; then
    log "fetch FAILED (curl exit $rc): $url"; status failed
    [ "$rc" = 22 ] && exit 5 || exit "$rc"
  fi
  mv -f "$out.part" "$out"
  verify "$out" "$md5" "$sha" "$size" || { log "verification FAILED: $out"; status failed; exit 4; }
  log "fetched: ${out#$DEST/}"; }
listed(){ # stdin lines "url<US>name<US>md5<US>sha256<US>size" (US = \x1f; a tab would collapse empty fields): fetch each
  while IFS=$'\x1f' read -r url name md5 sha size; do [ -n "$url" ] && { fetch "$url" "$DEST/$name" "$md5" "$sha" "$size" || exit $?; }; done; }
'''
PY_JSON = "python3 -c 'import json,sys; d=json.load(sys.stdin); "
SEP = 'sep="\\x1f"'   # rendered inside a single-quoted bash string: python reads sep="\x1f"
# Mendeley /versions -> the highest available version; an {"error": ...} body iterates as strings and
# raises AttributeError, an empty list raises ValueError, and either way the caller's guard fires.
VERSIONS_PY = (PY_JSON + 'vs=[v["version"] for v in d if v.get("available")] or [v["version"] for v in d]; '
               "print(max(vs))'")
NBIA_PY = r'''import json, os, re, sys, urllib.parse, urllib.request
dest, slug = sys.argv[1], sys.argv[2]
base = "https://services.cancerimagingarchive.net/nbia-api/services/v1/"
get = lambda ep, **kw: json.load(urllib.request.urlopen(base + ep + ("?" + urllib.parse.urlencode(kw) if kw else ""), timeout=120))
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
coll = next((c["Collection"] for c in get("getCollectionValues") if norm(c["Collection"]) == norm(slug)), None)
if coll is None:
    print("collection not found in NBIA:", slug, "(limited-access collections are not listed)"); sys.exit(5)
series = [s for s in get("getSeries", Collection=coll) if s.get("Modality") in ("CT", "CR", "DX", "RF", "XA", "OT")]
print(f"{coll}: {len(series)} eligible series"); os.makedirs(dest, exist_ok=True)
for s in series:
    uid = s["SeriesInstanceUID"]; out = os.path.join(dest, uid + ".zip")
    if os.path.exists(out) and os.path.getsize(out) > 0: continue
    urllib.request.urlretrieve(base + "getImage?" + urllib.parse.urlencode({"SeriesInstanceUID": uid}), out + ".part")
    os.replace(out + ".part", out)
'''

def _dry(msg: str) -> str:
    """The DRY_RUN gate: printed and exit 0 before any network call (the header promises none)."""
    return f'[ "$DRY_RUN" = 1 ] && {{ log {Q(msg)}; exit 0; }}'


def _capture(url: str, what: str, expand: bool = False) -> str:
    """Capture a host API listing into $J, exit 5 when the record is gone: a missing record used to
    give curl 22 and then a JSONDecodeError traceback from python on empty stdin under pipefail.
    `expand` double-quotes the URL instead of single-quoting it, for a URL holding a shell variable
    the script resolved a line earlier (the Mendeley version)."""
    u = f'"{url}"' if expand else Q(url)
    return f'J=$(curl -fsSL {u}) || {{ log "{what} not found or unreachable (curl exit $?)"; status failed; exit 5; }}'


def _listing(url: str, what: str, py: str) -> list[str]:
    """`_capture`, then feed `py` (a list comprehension over the parsed body `d`) to `listed`."""
    return [_capture(url, what), f"printf '%s' \"$J\" | {PY_JSON}{py}' | listed"]


def _body(p: Plan) -> list[str]:
    """Bash lines after the helpers: one method, then `finish` or `manual`."""
    n, L = p.native or "", []
    if p.manual and p.method in ("browser", "none"):
        return [f"manual {Q(p.manual)}"]
    if p.method == "files":
        L += [f"fetch {Q(f['url'])} \"$DEST\"/{Q(f['file'])} {Q(f.get('md5') or '')} {Q(f.get('sha256') or '')} {Q(str(f.get('size_bytes') or ''))}"
              for f in p.files]
    elif p.method == "zenodo-api":
        url = f"https://zenodo.org/api/records/{n}"
        L += ["need curl https://curl.se; need python3 python", _dry(f"would list {url} and fetch each file (md5 from the API)"),
              f'log "listing files of Zenodo record {n} through the records API"']
        L += _listing(url, f"Zenodo record {n}", f'[print(f[\"links\"][\"self\"], f[\"key\"], f.get(\"checksum\",\"\").replace(\"md5:\",\"\"), '
                                                  f'\"\", f.get(\"size\",\"\"), {SEP}) for f in d.get(\"files\", [])]')
    elif p.method == "figshare-api":
        url = f"https://api.figshare.com/v2/articles/{n}/files"
        L += ["need curl https://curl.se; need python3 python", _dry(f"would list {url} and fetch each file (md5 from the API)"),
              f'log "listing files of Figshare article {n}"']
        L += _listing(url, f"Figshare article {n}", f'[print(f[\"download_url\"], f[\"name\"], f.get(\"computed_md5\",\"\"), \"\", '
                                                     f'f.get(\"size\",\"\"), {SEP}) for f in d]')
    elif p.method == "mendeley-api":
        # Field names checked against one live listing (5jdfdgp762 v1, 2026-09-19): filename, size,
        # content_details.{download_url, sha256_hash}. An unknown id or version answers HTTP 200 with
        # the body {"error": 404}, so the body's shape, not curl's exit, decides "not found".
        # The version is NOT optional: `files?folder_id=root` without one answers 200 {"error": 400}
        # (checked live on 5jdfdgp762, whose file list the same URL returns once &version=1 is added).
        # When the URL and the DOI carry no version, the script asks /versions for the highest available
        # one first (live: [{"version":1,"publish_date":...,"available":true}]), as sdr.availability does.
        did, ver = (n.split("/") + [""])[:2]
        base = f"https://data.mendeley.com/public-api/datasets/{did}"
        url = f"{base}/files?folder_id=root&version=$V"
        L += ["need curl https://curl.se; need python3 python"]
        if ver:
            L += [_dry(f"would list {base}/files?folder_id=root&version={ver} and fetch each file (sha256 from the API)"),
                  f"V={ver}"]
        else:
            L += [_dry(f"would resolve the latest available version at {base}/versions, then list "
                       f"{base}/files?folder_id=root&version=<v> and fetch each file (sha256 from the API)"),
                  f"V=$(curl -fsSL {Q(base + '/versions')} | {VERSIONS_PY}) || "
                  f'{{ log "Mendeley Data dataset {did}: no published version at /versions (not found)"; status failed; exit 5; }}']
        L += [f'log "listing files of Mendeley Data dataset {did} version $V through the public API"',
              _capture(url, f"Mendeley Data dataset {did} version $V", expand=True),
              f"printf '%s' \"$J\" | python3 -c 'import json,sys; sys.exit(5 if isinstance(json.load(sys.stdin), dict) else 0)' || "
              f'{{ log "Mendeley Data dataset {did} version $V: the API answered an error body (not found)"; status failed; exit 5; }}',
              f"printf '%s' \"$J\" | {PY_JSON}[print(f[\"content_details\"][\"download_url\"], f[\"filename\"], \"\", "
              f"f[\"content_details\"].get(\"sha256_hash\",\"\"), f.get(\"size\",\"\"), {SEP}) for f in d]' | listed"]
    elif p.method == "dryad-zip":
        L += ["need python3 python", f"ENC=$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=\"\"))' {Q(n)})",
              f'fetch "https://datadryad.org/api/v2/datasets/$ENC/download" "$DEST/{p.id}-dryad.zip"']
    elif p.method == "osf-zip":
        L.append(f'fetch "https://files.osf.io/v1/resources/{n}/providers/osfstorage/?zip=" "$DEST/{p.id}-osf.zip"')
    elif p.method == "physionet-wget":
        slug = n.split("/")[0]
        L += ["need wget https://www.gnu.org/software/wget/; need curl https://curl.se",
              _dry(f"would resolve the current version of https://physionet.org/content/{slug}/ and mirror "
                   f"https://physionet.org/files/{slug}/<version>/ (checked against its SHA256SUMS.txt)"),
              # A slug that is gone answers 404: curl exits 22 inside $( ) and set -e would end the script
              # at exit 22 with no .recipe_status, so the resolution is guarded like a listing.
              f'EFF=$(curl -fsSIL -o /dev/null -w "%{{url_effective}}" "https://physionet.org/content/{slug}/") || '
              f'{{ log "PhysioNet slug {slug} not found or unreachable (curl exit $?)"; status failed; exit 5; }}',
              f'VER=$(printf \'%s\' "$EFF" | sed -E "s#.*/content/[^/]+/([^/]+)/?#\\1#")',
              f'[ -n "$VER" ] && [ "$VER" != "$EFF" ] || {{ log "PhysioNet {slug}: no version in the effective URL $EFF"; status failed; exit 5; }}',
              f'log "PhysioNet {slug} version $VER (open access, {p.rule})"',
              f'mkdir -p "$DEST"; wget -r -N -c -np -nH --cut-dirs=3 -P "$DEST" "https://physionet.org/files/{slug}/$VER/"',
              '( cd "$DEST" && [ -f SHA256SUMS.txt ] && sha256sum --quiet -c SHA256SUMS.txt ) || { log "SHA256SUMS check FAILED"; status failed; exit 4; }']
    elif p.method == "nbia-rest":
        L += ["need python3 python",
              _dry(f"would list the CT/CR/DX/RF/XA/OT series of NBIA collection {n} (getCollectionValues, getSeries) "
                   f"and fetch one getImage zip per series"),
              f'log "NBIA REST: series of collection {n} (public, {p.rule})"',
              # NBIA_PY exits 5 when the collection is not listed; the guard is what writes .recipe_status.
              f'python3 - "$DEST" {Q(n)} <<\'PY\' || {{ log "NBIA collection {n}: listing or fetch failed (exit $?)"; status failed; exit 5; }}',
              NBIA_PY.rstrip(), "PY"]
    elif p.method == "hf-cli":
        # huggingface_hub 0.34+ names the CLI `hf` and keeps `huggingface-cli` as a deprecated alias: accept either.
        find = "HF=$(command -v hf || command -v huggingface-cli)"
        if p.route == "registration":   # gated: client AND token, else the person registers first
            L.append(find + ' && { [ -n "${HF_TOKEN:-}" ] || [ -f "$HOME/.cache/huggingface/token" ]; } || manual '
                     + Q(f"gated Hugging Face dataset {n}: accept the terms at {p.url}, pip install huggingface_hub, "
                         f"then set HF_TOKEN (hf auth login) and rerun"))
        else:
            L.append(find + ' || { log "missing tool: hf or huggingface-cli (pip install huggingface_hub)"; exit 3; }')
        L += [_dry(f"would run hf download --repo-type dataset {n} --local-dir $DEST"),
              f'"$HF" download --repo-type dataset {Q(n)} --local-dir "$DEST"']
    elif p.method == "kaggle-cli":
        kind, slug = n.split(":", 1)
        L += ['command -v kaggle >/dev/null 2>&1 && { [ -f "$HOME/.kaggle/kaggle.json" ] || [ -n "${KAGGLE_KEY:-}" ]; } || manual '
              + Q(f"Kaggle needs an account: register at {p.url}, accept the {kind[:-1]} rules, create an API token at "
                  f"kaggle.com/settings and save it as ~/.kaggle/kaggle.json, pip install kaggle, then rerun"),
              _dry(f"would run kaggle {kind} download {slug}"), 'mkdir -p "$DEST"',
              f'kaggle datasets download -d {Q(slug)} -p "$DEST" --unzip' if kind == "datasets" else f'kaggle competitions download -c {Q(slug)} -p "$DEST"']
    elif p.method == "git-clone":
        # A failed `lfs pull` must not be reported as "git-lfs absent" and then marked downloaded with pointer files.
        L += ["need git https://git-scm.com", _dry(f"would git clone https://github.com/{n} (then git lfs pull when git-lfs is installed)"),
              f'mkdir -p "$DEST"; [ -d "$DEST/repo/.git" ] || git clone --depth 1 "https://github.com/{n}" "$DEST/repo"',
              'if command -v git-lfs >/dev/null 2>&1; then git -C "$DEST/repo" lfs pull || { log "git lfs pull FAILED"; status failed; exit 4; }; '
              'else log "git-lfs absent: large files may be pointers"; fi']
    return L + ["finish"]


def render_dataset_script(p: Plan, run_date: str, demo: bool) -> str:
    lic = p.record.get("licence") or {}
    head = ["#!/usr/bin/env bash",
            f"# recipe/datasets/{p.id}.sh: generated by sdr.recipe (protocol {PROTOCOL_VERSION}) on run date {run_date}"
            + (" from DEMO records (not charted)" if demo else f" from charting/datasets/{p.id}.json"),
            f"# {p.name}; modality {','.join(p.record.get('modality') or ['?'])}; route {p.route} ({p.rule or 'no rule'}); "
            f"host {p.host_type}/{p.key}; licence {lic.get('text', 'unknown')} [{lic.get('tier', 'unknown')}]",
            f"# action {p.action}; method {p.method}; verification {p.verification}; landing {p.url or 'none'}",
            "# Usage: DATA_ROOT=~/data bash this.sh   (DRY_RUN=1 prints the listing endpoint it would query and the files it",
            "# would fetch from a baked-in list; no network call is made and nothing is written)",
            "# Idempotent: files that exist and verify are skipped. Exit 0 downloaded; 10 manual step printed; 3 missing tool;",
            "# 4 verification failed (.recipe_status=failed); 5 the host answered an HTTP error for this record, or listed",
            "# no files for it (.recipe_status=failed). A client method (hf-cli, kaggle-cli, git-clone) instead propagates",
            "# the client's own exit status, and writes .recipe_status only where this script checks the client's result.",
            "set -euo pipefail", f"DATASET_ID={Q(p.id)}"]
    return "\n".join(head + [HELPERS.rstrip()] + _body(p)) + "\n"


def render_download_all(plans: list[Plan], run_date: str, demo: bool) -> str:
    rows = "\n".join(f"  {Q(p.id)}:{p.action}" for p in plans)
    return f"""#!/usr/bin/env bash
# recipe/download_all.sh: generated by sdr.recipe (protocol {PROTOCOL_VERSION}) on run date {run_date}{' from DEMO records' if demo else ''}
# Runs recipe/datasets/<id>.sh in the SAP A7 order (reachable fit_level_id sets not on the grid first, by quality).
# Usage: DATA_ROOT=~/data bash download_all.sh [--only id,id] [--skip-manual] [--dry-run]
#   Exit codes of a dataset script: 0 downloaded, 10 manual step printed (a person must act), 3 missing tool,
#   4 verification failed, 5 the host answered an HTTP error (a client method propagates its client's status);
#   a failure stops that dataset only.
set -uo pipefail
HERE="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
export DATA_ROOT="${{DATA_ROOT:-$HOME/data}}"; ONLY=""; SKIP_MANUAL=0
while [ $# -gt 0 ]; do case "$1" in
  --only) ONLY=",$2,"; shift 2;; --skip-manual) SKIP_MANUAL=1; shift;; --dry-run) export DRY_RUN=1; shift;;
  *) echo "unknown flag $1"; exit 2;; esac; done
ORDER=(
{rows}
)
ok=0; failed=0; manual=0; skipped=0
for entry in "${{ORDER[@]}}"; do
  id="${{entry%%:*}}"; action="${{entry##*:}}"
  if [ -n "$ONLY" ] && [ "${{ONLY/,$id,/}}" = "$ONLY" ]; then skipped=$((skipped+1)); continue; fi
  if [ "$SKIP_MANUAL" = 1 ] && [ "$action" != download ] && [ "$action" != registration ]; then skipped=$((skipped+1)); continue; fi
  echo "== $id ($action)"
  bash "$HERE/datasets/$id.sh"; rc=$?
  case "$rc" in 0) ok=$((ok+1));; 10) manual=$((manual+1));; *) failed=$((failed+1)); echo "!! $id failed (exit $rc)";; esac
done
echo "== summary: ok=$ok manual=$manual failed=$failed skipped=$skipped (of ${{#ORDER[@]}}); see recipe/manifest.csv"
[ "$failed" -eq 0 ]
"""


def manifest_row(i: int, p: Plan) -> dict:
    r, lic = p.record, p.record.get("licence") or {}
    return {"recipe_order": i, "dataset_id": p.id, "name": p.name, "modality": ";".join(r.get("modality") or []),
            "region": ";".join(r.get("region") or []), "n_subjects": r.get("n_subjects"), "access_route": p.route,
            "access_route_rule": p.rule, "host_type": p.host_type, "host_key": p.key, "access_url": p.url or "",
            "recipe_action": p.action, "download_method": p.method,
            "verification": p.verification if p.action in ("download", "registration") else "", "n_files_known": len(p.files),
            "size_gb": r.get("size_gb"), "licence_text": lic.get("text", ""), "licence_tier": lic.get("tier", ""), "on_grid": p.on_grid,
            "fit_level_id": "" if p.fit is None else p.fit, "quality_total": "" if p.quality is None else p.quality,
            "script": f"datasets/{p.id}.sh", "manual_step": p.manual.replace("\n", " ")}


# ----------------------------------------------------------------------------- inputs and outputs
def load_records(path: Path) -> list[dict]:
    """Charting records from a directory of <id>.json or one .jsonl; sorted by id."""
    if path.is_dir():
        recs = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(path.glob("*.json"))]
    else:
        recs = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.suffix == ".jsonl" and path.exists() else []
    return sorted((r for r in recs if r.get("id")), key=lambda r: r["id"])


def load_quality(path: Path) -> dict:
    """analysis/quality.json -> {id: {total, fit_level_id}}; {} when absent (see the module docstring)."""
    if not path.exists():
        return {}
    d = json.loads(path.read_text(encoding="utf-8"))
    d = d.get("datasets", d.get("per_dataset", d)) if isinstance(d, dict) else d
    if isinstance(d, list):
        d = {r.get("id") or r.get("dataset_id"): r for r in d}
    return {k: v for k, v in d.items() if isinstance(v, dict)}


def _write_text(path: Path, text: str, executable: bool = False) -> None:
    """LF text, UTF-8, refused outside review_root(). candidate for common.py (dump_json is JSON-only)."""
    p = path.resolve()
    if review_root() not in p.parents:
        raise ValueError(f"refusing to write outside spine_data_review/: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    if executable:
        try:
            os.chmod(p, 0o755)
        except OSError:
            pass


def demo_records() -> list[dict]:
    """Three in-memory records (Zenodo open-download, PhysioNet DUA, Kaggle registration) for
    --demo smoke tests only; never written to charting/. MultiCaRe's record is the Zenodo example
    because its files are the review's own metadata download (F2)."""
    base = {"schema_version": "1.0", "modality": ["CT"], "region": ["lumbar"], "n_subjects": 100, "size_gb": None, "checksums": [],
            "licence": {"text": "CC BY 4.0", "tier": "open"}, "on_grid": {"status": "no"}, "access_probe": [], "file_url_probed": None,
            "versioning": {"dataset_doi": None}, "source_record": {"doi": None}}
    return [{**base, "id": "demo-zenodo-ct", "name": "Demo Zenodo CT set", "access_route": "open-download", "access_route_rule": "P1",
             "host_type": "repository-api", "access_url": "https://zenodo.org/records/10079370"},
            {**base, "id": "demo-physionet-xr", "name": "Demo PhysioNet radiographs", "modality": ["radiograph"], "access_route": "data-use-agreement",
             "access_route_rule": "P8", "host_type": "repository-api", "access_url": "https://physionet.org/content/vindr-spinexr/1.0.0/",
             "licence": {"text": "PhysioNet Credentialed Health Data License 1.5.0", "tier": "restricted"}},
            {**base, "id": "demo-kaggle-ct", "name": "Demo Kaggle competition CT", "access_route": "registration", "access_route_rule": "P12",
             "host_type": "challenge-platform", "access_url": "https://www.kaggle.com/competitions/rsna-2022-cervical-spine-fracture-detection",
             "licence": {"text": "Kaggle competition rules", "tier": "restricted"}}]


def main(argv: list[str] | None = None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.recipe", description=__doc__.split("\n")[0]))
    ap.add_argument("--datasets", default="charting/datasets", help="directory of <id>.json or a .jsonl (relative to spine_data_review/)")
    ap.add_argument("--quality", default="analysis/quality.json", help="analysis/quality.json for fit_level_id and totals (optional)")
    ap.add_argument("--enrichment", default="charting/enrichment", help="directory of <id>.json enrichment records (optional)")
    ap.add_argument("--out", default=None, help="output directory (default recipe/; with --demo, <run-dir>/recipe_demo)")
    ap.add_argument("--demo", action="store_true", help="use three built-in demo records instead of charting/ (smoke test)")
    a = ap.parse_args(argv)
    rd, root = init_run_dir(a.run_dir, a.run_date, argv), review_root()
    out = Path(a.out) if a.out else (rd.root / "recipe_demo" if a.demo else Path("recipe"))
    out = out if out.is_absolute() else root / out
    recs = (demo_records() if a.demo else load_records(root / a.datasets))[: a.limit]
    quality, enr = load_quality(root / a.quality), root / a.enrichment
    plans = order_plans([make_plan(r, quality, json.loads((enr / f"{r['id']}.json").read_text(encoding="utf-8"))
                                   if (enr / f"{r['id']}.json").exists() else None) for r in recs])
    if not plans:
        print(f"no charting records at {root / a.datasets} (accepted: a directory of <id>.json, or a .jsonl with one record "
              f"per line); nothing generated", file=sys.stderr)
        if a.dry_run:   # nothing would be written anyway; protocol-check runs this before any record is charted
            print(f"dry run: 0 records, nothing to write under {out}")
            return 0
        return 1
    for i, p in enumerate(plans, 1):
        print(f"{i:3d} {p.id:32s} {p.route:20s} {p.action:15s} {p.method:15s} files={len(p.files)} verify={p.verification}")
    if a.dry_run:
        print(f"dry run: would write {out / 'download_all.sh'}, {len(plans)} scripts under {out / 'datasets'}, {out / 'manifest.csv'}")
        return 0
    for p in plans:
        _write_text(out / "datasets" / f"{p.id}.sh", render_dataset_script(p, a.run_date, a.demo), executable=True)
    _write_text(out / "download_all.sh", render_download_all(plans, a.run_date, a.demo), executable=True)
    with open(out / "manifest.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(manifest_row(i, p) for i, p in enumerate(plans, 1))
    n = {k: sum(p.action == k for p in plans) for k in ("download", "registration", "manual-dua", "manual-request", "unavailable", "commercial")}
    print(f"wrote {out}: {len(plans)} dataset scripts, download_all.sh, manifest.csv; actions {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
