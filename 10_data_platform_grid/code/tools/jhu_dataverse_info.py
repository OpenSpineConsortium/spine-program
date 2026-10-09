#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/jhu_dataverse_info.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""What a JHU Data Archive (Dataverse) deposit holds: title, licence/terms, and every file with its size.

archive.data.jhu.edu answers plain curl with a Cloudflare 403 from every IP (the TLS fingerprint is blocked);
curl_cffi impersonating a browser is served normally. This queries the public Dataverse API only.

    python tools/jhu_dataverse_info.py doi:10.7281/T1/C304HZ
"""
from __future__ import annotations

import json
import sys


def main() -> int:
    pid = sys.argv[1] if len(sys.argv) > 1 else "doi:10.7281/T1/C304HZ"
    from curl_cffi import requests
    url = f"https://archive.data.jhu.edu/api/datasets/:persistentId/?persistentId={pid}"
    r = requests.get(url, impersonate="chrome", timeout=60)
    print("HTTP", r.status_code)
    if r.status_code != 200:
        print(r.text[:500]); return 1
    d = r.json()["data"]; v = d["latestVersion"]
    cit = {f["typeName"]: f["value"] for f in v["metadataBlocks"]["citation"]["fields"]}
    print("title:", cit.get("title"))
    print("authors:", [a["authorName"]["value"] for a in cit.get("author", [])])
    print("published:", d.get("publicationDate"), "| version", v.get("versionNumber"), "| state", v.get("versionState"))
    for k in ("license", "termsOfUse", "termsOfAccess", "fileAccessRequest", "restrictions", "conditions"):
        if v.get(k):
            print(f"{k}:", json.dumps(v[k])[:600])
    desc = cit.get("dsDescription", [])
    if desc:
        print("description:", desc[0]["dsDescriptionValue"]["value"][:1500])
    files = v.get("files", [])
    tot = 0
    for f in files:
        df = f["dataFile"]; tot += df.get("filesize", 0)
        print(f"  {df.get('filename')}  {df.get('filesize', 0) / 1e9:.2f} GB  {df.get('contentType')}  restricted={f.get('restricted')}  id={df.get('id')}")
    print(f"{len(files)} files, {tot / 1e9:.1f} GB total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
