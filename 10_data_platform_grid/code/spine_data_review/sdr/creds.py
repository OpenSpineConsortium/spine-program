"""Credentials by name, never by value (PROTOCOL.md section 5; information_sources.md placeholders).

The store is ~/.fluorocap/credentials.env on the WSL host (KEY=value lines, mode 600, shared with
the FluoroCap harvesters), read once and overlaid by the environment; ~/.kaggle/kaggle.json is
read for the two Kaggle values when it exists. Every adapter asks `cred("NAME")` and gets None
when the key is absent, so each route degrades to its credential-free form instead of failing,
and writes `credential_mode: credential-free` (or `needs-credentials`) to queries.json.

WHY VALUES NEVER LEAVE THIS MODULE'S CALLERS. A request log and a raw-response cache are
published with the review. `requests` puts the full URL, query string included, into its
exception messages, and a key pasted into a log line survives every later redaction pass
nobody runs. So the session redacts params by NAME before logging (common.SECRET_PARAMS) and
`redact_text` scrubs every loaded VALUE from every string that is about to be written or
printed: the logged url, every string-valued parameter, the error text, run_meta argv and the
response body before it is cached. Both are applied; neither is trusted alone. The value is
scrubbed in four spellings, because a value does not survive a URL unchanged: as loaded, as
`urllib.parse.quote(v, safe='')` (the form `requests` prints in "Max retries exceeded with
url: ...?mailto=a%40b"), as `quote_plus(v)` (form-encoded bodies) and lower-cased (hosts and
some error pages fold case). `creds_present()` returns names only and is what run_meta.json
and the `check` subcommand print.

UNPAYWALL_EMAIL is blank in the store as delivered; Unpaywall needs only a contact address, so
`unpaywall_email()` falls back to FLUOROCAP_CONTACT_EMAIL and the adapter records which name it
used. `probe_specs()` lists one harmless request per credentialed service for `check`; it lives
here so the probe URLs sit beside the names they test, but the requests are made by
common.RateLimitedSession so they obey the same limits and redaction as a real run.
"""
from __future__ import annotations

import base64
import json
import os
import stat
import sys
from pathlib import Path
from urllib.parse import quote, quote_plus

CRED_STORE = Path(os.environ.get("FLUOROCAP_CREDS", "~/.fluorocap")).expanduser() / "credentials.env"
KAGGLE_JSON = Path("~/.kaggle/kaggle.json").expanduser()
# The names the protocol reads. The optional ones (HF, GitHub, OSF, Kaggle) may come from the environment.
CRED_NAMES = ("NCBI_API_KEY", "S2_API_KEY", "FLUOROCAP_CONTACT_EMAIL", "SPRINGER_API_META_KEY",
              "SPRINGER_API_OPEN_ACCESS_KEY", "UNPAYWALL_EMAIL", "HF_TOKEN", "GITHUB_TOKEN", "OSF_TOKEN",
              "KAGGLE_USERNAME", "KAGGLE_KEY")
# A DOI that resolves at every literature service (CT-ORG, Scientific Data 2020); used only by probes.
PROBE_DOI = "10.1038/s41597-020-00715-8"
_CACHE: dict[str, str] | None = None
_FORMS: list[str] | None = None  # every spelling of every value, longest first; built once


def _load() -> dict[str, str]:
    """Read the store (warning on stderr if group/other-readable), then env (wins), then kaggle.json."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    out: dict[str, str] = {}
    if CRED_STORE.exists():
        try:
            if stat.S_IMODE(CRED_STORE.stat().st_mode) & 0o077:
                print(f"warning: {CRED_STORE} is readable by others; run: chmod 600 {CRED_STORE}", file=sys.stderr)
        except OSError:
            pass
        for line in CRED_STORE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() and v.strip():
                    out[k.strip()] = v.strip().strip('"').strip("'")
    for k in CRED_NAMES:
        if os.environ.get(k):
            out[k] = os.environ[k]
    if KAGGLE_JSON.exists():
        try:
            kj = json.loads(KAGGLE_JSON.read_text(encoding="utf-8"))
            if kj.get("username") and kj.get("key"):
                out.setdefault("KAGGLE_USERNAME", str(kj["username"]))
                out.setdefault("KAGGLE_KEY", str(kj["key"]))
        except (OSError, ValueError):
            pass
    _CACHE = out
    return out


def cred(name: str) -> str | None:
    """Value of credential `name`, or None when absent. The caller places it in a request header or
    parameter and nowhere else; the session redacts it from the log by name and by value."""
    return _load().get(name)


def creds_present() -> list[str]:
    """Sorted NAMES of the protocol credentials that are set. Safe to print and to record."""
    return sorted(k for k in CRED_NAMES if _load().get(k))


def contact() -> str | None:
    """FLUOROCAP_CONTACT_EMAIL, the polite-pool address for Crossref, OpenAlex, NCBI and the User-Agent."""
    return cred("FLUOROCAP_CONTACT_EMAIL")


def unpaywall_email() -> tuple[str | None, str]:
    """(address, name-used): UNPAYWALL_EMAIL when set, else the contact address; the name is what the
    adapter logs as `credential` so the fallback is visible in the run."""
    if cred("UNPAYWALL_EMAIL"):
        return cred("UNPAYWALL_EMAIL"), "UNPAYWALL_EMAIL"
    return contact(), "FLUOROCAP_CONTACT_EMAIL"


def _forms() -> list[str]:
    """Every loaded value of six or more characters in its four spellings (plain, percent-encoded,
    plus-encoded, lower-cased), de-duplicated, longest first so a longer spelling is never left
    half-replaced by a shorter one. Values under six characters are not scrubbed: a two-letter
    value would blank ordinary text, and no protocol credential is that short."""
    global _FORMS
    if _FORMS is None:
        forms: set[str] = set()
        for v in _load().values():
            if len(v) >= 6:
                forms.update((v, quote(v, safe=""), quote_plus(v), v.lower()))
        _FORMS = sorted(forms, key=lambda f: (-len(f), f))
    return _FORMS


def redact_text(s: str) -> str:
    """Replace every loaded credential value of six or more characters in `s` by `<redacted>`, in
    each of the spellings `_forms` lists. Applied by the session to every logged url, parameter
    value, error message and cached body, to run_meta argv, and to `check` output. Returns `s`
    unchanged (same object) when nothing matches, so the cost on a clean body is one scan per form."""
    if not s:
        return s
    for f in _forms():
        if f in s:
            s = s.replace(f, "<redacted>")
    return s


def probe_specs() -> list[tuple[str, str, str, dict, dict]]:
    """One harmless request per credentialed service, as (credential name, source, url, params, headers).
    Each is a fixed-cost read (retmax=0, a known DOI, rate_limit, whoami) that proves the key is
    accepted; `check` skips the ones whose name is absent and says which credential-free form the
    adapter will use instead. Values are placed into params/headers here and nowhere else."""
    up_email, up_name = unpaywall_email()
    kaggle_basic = base64.b64encode(f"{cred('KAGGLE_USERNAME')}:{cred('KAGGLE_KEY')}".encode()).decode()
    return [
        ("NCBI_API_KEY", "pubmed", "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
         {"db": "pubmed", "term": "spine", "retmax": 0, "retmode": "json", "api_key": cred("NCBI_API_KEY")}, {}),
        ("S2_API_KEY", "s2", "https://api.semanticscholar.org/graph/v1/paper/search",
         {"query": "vertebra", "limit": 1}, {"x-api-key": cred("S2_API_KEY")}),
        ("FLUOROCAP_CONTACT_EMAIL", "openalex", f"https://api.openalex.org/works/https://doi.org/{PROBE_DOI}",
         {"mailto": contact()}, {}),
        ("FLUOROCAP_CONTACT_EMAIL", "crossref", f"https://api.crossref.org/works/{PROBE_DOI}",
         {"mailto": contact()}, {}),
        ("SPRINGER_API_META_KEY", "springer", "https://api.springernature.com/meta/v2/json",
         {"q": f"doi:{PROBE_DOI}", "p": 1, "api_key": cred("SPRINGER_API_META_KEY")}, {}),
        ("SPRINGER_API_OPEN_ACCESS_KEY", "springer", "https://api.springernature.com/openaccess/json",
         {"q": f"doi:{PROBE_DOI}", "p": 1, "api_key": cred("SPRINGER_API_OPEN_ACCESS_KEY")}, {}),
        (up_name, "unpaywall", f"https://api.unpaywall.org/v2/{PROBE_DOI}", {"email": up_email}, {}),
        ("HF_TOKEN", "hf", "https://huggingface.co/api/whoami-v2", {},
         {"Authorization": f"Bearer {cred('HF_TOKEN')}"}),
        ("GITHUB_TOKEN", "github", "https://api.github.com/rate_limit", {},
         {"Authorization": f"Bearer {cred('GITHUB_TOKEN')}"}),
        ("OSF_TOKEN", "osf", "https://api.osf.io/v2/users/me/", {},
         {"Authorization": f"Bearer {cred('OSF_TOKEN')}"}),
        ("KAGGLE_KEY", "kaggle", "https://www.kaggle.com/api/v1/datasets/list",
         {"search": "spine", "page": 1}, {"Authorization": f"Basic {kaggle_basic}"}),
    ]


# What each adapter does when its credential is absent (information_sources.md, per-source blocks).
CREDENTIAL_FREE_FORM = {
    "NCBI_API_KEY": "api_key omitted, 3 requests/s (credential-free)",
    "S2_API_KEY": "same bulk endpoint at one request per 5 s (credential-free)",
    "FLUOROCAP_CONTACT_EMAIL": "no mailto; OpenAlex and Crossref outside the polite pool (credential-free)",
    "SPRINGER_API_META_KEY": "S1 venue sweep skipped (needs-credentials); pubmed_02 covers the journal",
    "SPRINGER_API_OPEN_ACCESS_KEY": "not used by any route",
    "UNPAYWALL_EMAIL": "falls back to FLUOROCAP_CONTACT_EMAIL",
    "HF_TOKEN": "anonymous Hub API (credential-free)",
    "GITHUB_TOKEN": "10 requests/min; search/code recorded needs-credentials",
    "OSF_TOKEN": "anonymous throttle 100/h (credential-free)",
    "KAGGLE_KEY": "one unauthenticated request recorded; kaggle_mention harvest (needs-credentials)",
}
