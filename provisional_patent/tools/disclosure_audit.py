"""What of this project is reachable by the public, right now, and what does each thing reveal?

WHY THIS IS A TOOL AND NOT A CHECKLIST. The project's own notes recorded the review Spaces as "public, but
not enabling -- they display a label, not the method." That was read off intent rather than off the API, and
it was wrong: the deploy script uploads app.py verbatim, and app.py's docstring describes the monotone
consecutive-run decode and the alternative-alphabet handling of a supernumerary segment in plain language.
A prose inventory of what is public is worth nothing; a query is worth something.

WHAT IT DOES AND DOES NOT DO. It reports. It changes nothing unless --close is given, and even then it only
flips visibility, never deletes. Deleting would destroy the record of what was exposed and when, which is
the evidence a patent attorney needs.

Every check prints a UTC timestamp, because for this purpose the time of the observation is part of the
observation.

    python tools/disclosure_audit.py            # report only
    python tools/disclosure_audit.py --close    # privatise what can be privatised
"""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

HF_SPACES = [
    ("anonymous-mlhc/CTSpinoPelvic1K-review-spine", "raw X-ray review; serves app.py under Files"),
    ("anonymous-mlhc/CTSpinoPelvic1K-review-ribs", "FluoroCap panel review; serves app.py under Files"),
    ("gregoryschwingmdphd/CTSpinoPelvic1K-review", "reader study"),
    ("gregoryschwingmdphd/openspine-level-id", "inference service; deploy_service.py creates it public"),
]
HF_DATASETS = [
    ("gregoryschwingmdphd/level-id-weights", "trained level weights -- must be private"),
    ("gregoryschwingmdphd/reader-study-films", "reader study pack"),
    ("gregoryschwingmdphd/level-review-films", "review pack"),
    ("gregoryschwingmdphd/fluorocap-review-panels", "review pack"),
]
GITHUB_REPOS = [
    ("Gregory-Schwing-MD-PhD/spinesurg-ct-nnunet", "the method; must be private"),
    ("gschwing/spinesurg-ct-nnunet", "published as the repo URL in CITATION.cff and pyproject.toml"),
    ("OpenSpineConsortium/openspineconsortium.github.io", "the public website; expected public"),
]
ENDPOINTS = [
    ("https://level-id.openspineconsortium.org", "hard-coded in public pacs/remote.js since 2026-09-14"),
    ("https://openspineconsortium.com/pacs/", "public viewer"),
]


def stamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def anon_get(url, timeout=20):
    """Fetch with NO credentials. The question is what an anonymous visitor sees, not what we can see."""
    req = urllib.request.Request(url, headers={"User-Agent": "disclosure-audit"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(4096)
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:  # noqa: BLE001
        return None, str(e).encode()[:200]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--close", action="store_true", help="privatise what is public; never deletes")
    ap.add_argument("--out", default="docs/disclosure_audit.json")
    a = ap.parse_args()

    print(f"disclosure audit  {stamp()}\n")
    findings = []

    print("HUGGINGFACE SPACES  (anonymous API -- what the public sees)")
    for sid, what in HF_SPACES:
        code, _ = anon_get(f"https://huggingface.co/api/spaces/{sid}")
        public = code == 200
        print(f"  {'PUBLIC ' if public else 'private' if code == 401 else f'HTTP {code}'}  {sid}")
        print(f"            {what}")
        findings.append({"kind": "hf_space", "id": sid, "anon_http": code,
                         "public": public, "what": what})

    print("\nHUGGINGFACE DATASETS")
    for rid, what in HF_DATASETS:
        code, _ = anon_get(f"https://huggingface.co/api/datasets/{rid}")
        public = code == 200
        flag = "  <-- MUST NOT BE PUBLIC" if public and "weights" in rid else ""
        print(f"  {'PUBLIC ' if public else 'private' if code == 401 else f'HTTP {code}'}  {rid}{flag}")
        findings.append({"kind": "hf_dataset", "id": rid, "anon_http": code,
                         "public": public, "what": what})

    print("\nGITHUB REPOSITORIES")
    for rid, what in GITHUB_REPOS:
        code, _ = anon_get(f"https://api.github.com/repos/{rid}")
        public = code == 200
        state = "PUBLIC " if public else "private/absent" if code == 404 else f"HTTP {code}"
        print(f"  {state}  {rid}")
        print(f"            {what}")
        findings.append({"kind": "github", "id": rid, "anon_http": code,
                         "public": public, "what": what})

    print("\nLIVE ENDPOINTS")
    for url, what in ENDPOINTS:
        code, body = anon_get(url)
        reachable = code is not None and code < 400
        print(f"  {'REACHABLE' if reachable else 'unreachable'}  HTTP {code}  {url}")
        print(f"            {what}")
        findings.append({"kind": "endpoint", "id": url, "anon_http": code,
                         "public": reachable, "what": what})

    pub = [f for f in findings if f["public"]]
    print(f"\n{'=' * 74}\n{len(pub)} of {len(findings)} surfaces are reachable anonymously.")
    for f in pub:
        print(f"   {f['kind']:11s} {f['id']}")

    if a.close:
        print("\nclosing what can be closed (visibility only; nothing is deleted)")
        try:
            from huggingface_hub import HfApi
        except Exception as e:  # noqa: BLE001
            print(f"   huggingface_hub unavailable: {type(e).__name__}")
            HfApi = None
        if HfApi is not None:
            # Org-owned repos need the org token; a personal token returns 403 on them. Try the org token
            # first for anything not in the personal namespace, and fall back.
            def tok_for(rid):
                cands = []
                if not rid.startswith("gregoryschwingmdphd/"):
                    cands.append(os.path.expanduser("~/.hf_org_token"))
                cands.append(os.path.expanduser("~/.cache/huggingface/token"))
                cands.append(os.path.expanduser("~/.hf_org_token"))
                for c in cands:
                    try:
                        t = open(c).read().strip()
                        if t:
                            yield c, t
                    except Exception:  # noqa: BLE001
                        continue

            for f in findings:
                if not f["public"] or f["kind"] not in ("hf_space", "hf_dataset"):
                    continue
                rt = "space" if f["kind"] == "hf_space" else "dataset"
                done = False
                for src, t in tok_for(f["id"]):
                    try:
                        # renamed in huggingface_hub 1.x
                        HfApi(token=t).update_repo_settings(f["id"], private=True, repo_type=rt)
                        f["closed_at"] = stamp()
                        f["closed_with"] = Path(src).name
                        print(f"   private now: {f['id']}  at {f['closed_at']}  ({Path(src).name})")
                        done = True
                        break
                    except Exception as e:  # noqa: BLE001
                        last = f"{type(e).__name__}: {str(e)[:80]}"
                if not done:
                    print(f"   FAILED {f['id']}: {last}")
                    f["close_error"] = last

        # VERIFY anonymously. A successful API call is a claim; an anonymous 401 is proof.
        print("\n   verifying, uncredentialed:")
        for f in findings:
            if f["kind"] not in ("hf_space", "hf_dataset") or not f.get("closed_at"):
                continue
            path = "spaces" if f["kind"] == "hf_space" else "datasets"
            code, _ = anon_get(f"https://huggingface.co/api/{path}/{f['id']}")
            f["anon_http_after"] = code
            ok = code in (401, 404)
            print(f"     {'CLOSED ' if ok else 'STILL OPEN'}  HTTP {code}  {f['id']}")
            if not ok:
                print("       still reachable -- do not treat this as closed")

        print("\n   GitHub visibility is not changed here -- it needs an authenticated gh/API call and")
        print("   should be done together with exporting the audit log, so both are recorded at once.")

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    json.dump({"observed_at": stamp(), "findings": findings,
               "note": ("anonymous, uncredentialed checks: this records what a member of the public sees, "
                        "not what the account owner sees. HTTP 401 on a HuggingFace API path means private; "
                        "404 on a GitHub repo means private or absent and the two cannot be distinguished "
                        "anonymously.")},
              open(out, "w"), indent=1)
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
