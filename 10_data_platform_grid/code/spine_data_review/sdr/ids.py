"""Record identity: the canonical string, the record id, and the known-item match (PROTOCOL.md 7.1, 18).

WHY IDENTITY IS ONE FUNCTION. Thirty sources return the same article or deposit under different
identifiers: a DOI with or without its resolver prefix, a PMID, a PMCID, an arXiv id with a
version suffix, a repository URL with a trailing slash or a query string. If each adapter
normalised its own way, the cross-source merge would count one record twice and the PRISMA
flow would be wrong by an amount nobody could audit. So every record's identity is the first
available of six normalised forms, in a fixed order, hashed once:

    doi:<doi> > pmid:<digits> > pmcid:PMC<digits> > arxiv:<id> > url:https://<host><path> > native:<source>:<id>

and the record id is `lit:` or `repo:` plus the first 12 hex characters of SHA-1 over that
string. The prefix is `repo:` for the repository sources R1-R14 and for Crossref, OpenAlex and
DataCite records typed dataset or image; everything else is `lit:`. The same normalisers serve
the merge passes (exact DOI, PMID/PMCID, arXiv<->DOI, normalised title + first author + year)
and the known-item recall check of section 18, whose `match_rule` is `doi`, `title-year` or `url`.

WHY THE NORMALISERS ARE ANCHORED. A normaliser that searches for "any run of digits" turns a
mis-mapped field into a finite, plausible id: `10.1038/x` would become PMC10 and the record
would merge with a real PMC10. So `norm_pmid` takes only the digits that END the value (after an
optional `PMID:` label or a pubmed URL path) and `norm_pmcid` only a value that IS a PMC id, with
or without the `PMC` label, optionally at the end of a URL path. Anything else is None, and a
record with no usable id fails loudly in `canonical_string`. Titles keep every Unicode
alphanumeric (str.isalnum after NFKC), not only ASCII, so a J-STAGE, KoreaMed or SciELO title
compares as itself instead of as its ASCII residue; PROTOCOL.md 7.1 says "alphanumerics only"
and this is that rule read literally. `tests/test_ids.py` fixes the worked examples; a change
here that moves one of them is a deviations-log row, because it changes every record id in a
finished run.
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from urllib.parse import urlsplit, urlunsplit

# Source names whose records are repository records (information_sources.md R1-R14 and the mention harvests).
REPO_SOURCES = frozenset({"zenodo", "figshare", "dryad", "osf", "mendeley", "datacite", "physionet", "tcia",
                          "kaggle", "kaggle-mention", "hf", "hf-mention", "gc", "github", "pwc", "odl"})
_DOI_RE = re.compile(r"10\.\d{4,9}/\S+", re.I)
_ARXIV_RE = re.compile(r"(\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?")
# The whole value is a PMID: `12345`, `PMID: 12345`, `https://pubmed.ncbi.nlm.nih.gov/12345/`.
_PMID_RE = re.compile(r"(?:PMID\s*:?\s*|(?:https?://)?(?:pubmed\.ncbi\.nlm\.nih\.gov|www\.ncbi\.nlm\.nih\.gov/pubmed)/)?(\d+)/?", re.I)
# The whole value is a PMC id: `PMC123`, `pmc123`, `123`, `.../pmc/articles/PMC123/`.
_PMCID_RE = re.compile(r"(?:.*/)?(?:PMC)?(\d+)/?", re.I)
_TRAILING_PUNCT = ".,;:)]}>\"'"


def norm_doi(s: str | None) -> str | None:
    """Lower-cased DOI with https://doi.org/, http://dx.doi.org/ and a leading `doi:` stripped and
    trailing punctuation removed; None when the string holds no DOI."""
    if not s:
        return None
    m = _DOI_RE.search(str(s).strip())
    return m.group(0).lower().rstrip(_TRAILING_PUNCT) if m else None


def norm_pmid(s: str | int | None) -> str | None:
    """`<digits>` when the whole value is a PMID (`12345`, `PMID: 12345`, a pubmed URL), or None.
    `0`, a DOI, a title ending in a year: None. PubMed has no PMID 0, and a digit run inside
    another kind of value must never become one."""
    if s is None:
        return None
    m = _PMID_RE.fullmatch(str(s).strip())
    return m.group(1) if m and int(m.group(1)) > 0 else None


def norm_pmcid(s: str | int | None) -> str | None:
    """`PMC<digits>` when the whole value is a PMC id (`PMC123`, `pmc123`, `123`, or one at the end
    of an ncbi/europepmc URL path); None for anything else, a DOI included."""
    if s is None:
        return None
    m = _PMCID_RE.fullmatch(str(s).strip())
    return f"PMC{m.group(1)}" if m and int(m.group(1)) > 0 else None


def norm_arxiv(s: str | None) -> str | None:
    """arXiv id without `arXiv:` prefix, URL or version suffix (`arXiv:2105.14711v2` -> `2105.14711`;
    old-style `math.GT/0309136` kept as written), or None."""
    m = _ARXIV_RE.search(str(s)) if s else None
    return m.group(1) if m else None


def norm_url(s: str | None) -> str | None:
    """`https://<host lower-cased><path without trailing slash>`: http rewritten to https, no query or
    fragment. None for an empty or non-http value."""
    if not s or not re.match(r"https?://", str(s).strip(), re.I):
        return None
    p = urlsplit(str(s).strip())
    return urlunsplit(("https", p.netloc.lower(), p.path.rstrip("/"), "", ""))


def norm_title(s: str | None) -> str:
    """NFKC, lower-case, Unicode alphanumerics only (`str.isalnum`; ligatures and full-width forms
    fold under NFKC, punctuation and spaces go, CJK and accented letters stay): merge rule 5 and
    the known-item `title_norm` column (that column is stored with spaces; compare through this
    function, never as text). Rule 5's 25-character floor is applied by the caller on this string."""
    return "".join(c for c in unicodedata.normalize("NFKC", s or "").lower() if c.isalnum())


def norm_family_name(s: str | None) -> str:
    """The first author's family name normalised like a title (merge rule 5)."""
    return norm_title(s)


def canonical_string(ids: dict, source: str = "", native_id: str | int | None = None) -> str:
    """The first available of doi:, pmid:, pmcid:, arxiv:, url:, native:<source>:<id> over an `ids`
    dict with keys doi, pmid, pmcid, arxiv, url (raw or already normalised). Raises ValueError when
    nothing identifies the record: an unidentifiable record must not be kept silently."""
    for key, f in (("doi", norm_doi), ("pmid", norm_pmid), ("pmcid", norm_pmcid), ("arxiv", norm_arxiv), ("url", norm_url)):
        v = f(ids.get(key))
        if v:
            return f"{key}:{v}"
    if native_id not in (None, ""):
        return f"native:{source}:{native_id}"
    raise ValueError("record has no DOI, PMID, PMCID, arXiv id, URL or native id")


def record_id(canonical: str, source: str, rtype: str | None = None) -> str:
    """`lit:` or `repo:` + first 12 hex of SHA-1 (UTF-8) over the canonical string. `repo:` iff the
    source is in REPO_SOURCES or `rtype` (Crossref/OpenAlex/DataCite type) is dataset or image."""
    is_repo = source in REPO_SOURCES or (rtype or "").strip().lower() in ("dataset", "image")
    return f"{'repo' if is_repo else 'lit'}:{hashlib.sha1(canonical.encode('utf-8')).hexdigest()[:12]}"


def normalised_ids(ids: dict) -> dict:
    """The `ids` block written to records/<source>.jsonl: every key present, normalised, None when absent."""
    return {"doi": norm_doi(ids.get("doi")), "pmid": norm_pmid(ids.get("pmid")), "pmcid": norm_pmcid(ids.get("pmcid")),
            "arxiv": norm_arxiv(ids.get("arxiv")), "url": norm_url(ids.get("url")), "repo_id": ids.get("repo_id") or None}


def known_item_matches(record: dict, item: dict) -> str | None:
    """Section 18 recall check: the rule under which a merged `record` retrieves a known `item`
    (a row of screen/known_items.csv), or None. `doi` when the item has a DOI and the record's DOI
    equals it; else `title-year` when normalised titles are identical and |year difference| <= 1;
    else `url` when canonical URLs are identical. Only the item's own `match_rule` is applied, so
    a DOI-bearing item never matches by title."""
    rule = (item.get("match_rule") or "").strip()
    rids = record.get("ids") or {}
    if rule == "doi":
        d = norm_doi(item.get("doi"))
        return "doi" if d and norm_doi(rids.get("doi")) == d else None
    if rule == "title-year":
        try:
            dy = abs(int(record.get("year") or 0) - int(item.get("year") or 0))
        except ValueError:
            return None
        t = norm_title(item.get("title_norm"))
        return "title-year" if t and norm_title(record.get("title")) == t and dy <= 1 else None
    if rule == "url":
        u = norm_url(item.get("url"))
        return "url" if u and norm_url(rids.get("url")) == u else None
    return None
