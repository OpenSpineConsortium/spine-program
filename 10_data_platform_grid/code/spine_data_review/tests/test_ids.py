"""Worked examples for sdr.ids (PROTOCOL.md 7.1 and 18): the canonical string, the record id, the
anchored PMID/PMCID normalisers, Unicode titles and the known-item rules.

WHY A FIXED LIST. The record id is a hash of the canonical string, so a normaliser that moves by
one character renumbers every record in a finished run and silently breaks every join on
record_id. The ids.py docstring names this file as the place those examples are frozen; a change
in ids.py that moves one of them is a deviations-log row. The anchored cases are the ones the
2026-09-19 review found unguarded: an unanchored digit search turned `10.1038/x` into PMC10 and
`0` into PMID 0. Offline; no run dir; nothing written.

Usage: ~/sdr_venv/bin/python tests/test_ids.py    (exit 1 on any failure)
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sdr import ids  # noqa: E402

DOI = "10.1038/s41597-020-00715-8"
CASES: list[tuple[str, object, object]] = [
    # norm_doi: resolver prefixes and a leading label stripped, lower-cased, trailing punctuation removed
    ("doi https", ids.norm_doi(f"https://doi.org/{DOI.upper()}."), DOI),
    ("doi dx", ids.norm_doi("http://dx.doi.org/10.1000/ABC)"), "10.1000/abc"),
    ("doi label", ids.norm_doi("doi:10.5281/zenodo.10079370"), "10.5281/zenodo.10079370"),
    ("doi absent", ids.norm_doi("no identifier here"), None),
    ("doi None", ids.norm_doi(None), None),
    # norm_pmid: only a value that IS a PMID (digits, `PMID:` label, pubmed URL); never a digit run inside another value
    ("pmid digits", ids.norm_pmid("12345"), "12345"),
    ("pmid int", ids.norm_pmid(12345), "12345"),
    ("pmid label", ids.norm_pmid("PMID: 123"), "123"),
    ("pmid url", ids.norm_pmid("https://pubmed.ncbi.nlm.nih.gov/12345/"), "12345"),
    ("pmid old url", ids.norm_pmid("https://www.ncbi.nlm.nih.gov/pubmed/777"), "777"),
    ("pmid zero int", ids.norm_pmid(0), None),
    ("pmid zero str", ids.norm_pmid("0"), None),
    ("pmid doi-like", ids.norm_pmid("10.1038/x"), None),
    ("pmid title-year", ids.norm_pmid("Lumbar CT 2020"), None),
    ("pmid empty", ids.norm_pmid(""), None),
    ("pmid None", ids.norm_pmid(None), None),
    # norm_pmcid: `PMC` label optional, case-insensitive, URL path forms; a DOI is not a PMC id
    ("pmcid label", ids.norm_pmcid("PMC123"), "PMC123"),
    ("pmcid lower", ids.norm_pmcid("pmc123"), "PMC123"),
    ("pmcid digits", ids.norm_pmcid("123"), "PMC123"),
    ("pmcid int", ids.norm_pmcid(123), "PMC123"),
    ("pmcid ncbi url", ids.norm_pmcid("https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123/"), "PMC123"),
    ("pmcid epmc url", ids.norm_pmcid("https://europepmc.org/article/PMC/PMC123"), "PMC123"),
    ("pmcid doi-like", ids.norm_pmcid("10.1038/x"), None),
    ("pmcid zero", ids.norm_pmcid("PMC0"), None),
    ("pmcid word", ids.norm_pmcid("abc"), None),
    # norm_arxiv: prefix, URL and version suffix dropped; old-style ids kept
    ("arxiv version", ids.norm_arxiv("arXiv:2105.14711v2"), "2105.14711"),
    ("arxiv url", ids.norm_arxiv("https://arxiv.org/abs/2105.14711"), "2105.14711"),
    ("arxiv old", ids.norm_arxiv("math.GT/0309136"), "math.GT/0309136"),
    ("arxiv absent", ids.norm_arxiv("nothing"), None),
    # norm_url: https, lower-cased host, no trailing slash, query or fragment
    ("url canonical", ids.norm_url("HTTP://Zenodo.org/records/10079370/?x=1#f"), "https://zenodo.org/records/10079370"),
    ("url ftp", ids.norm_url("ftp://x"), None),
    ("url empty", ids.norm_url(""), None),
    # norm_title: NFKC, lower-case, every Unicode alphanumeric kept (not only ASCII)
    ("title ligature", ids.norm_title("VerSe: A Vertebrae Labelling — ﬁne"), "verseavertebraelabellingfine"),
    ("title japanese", ids.norm_title("腰椎X線画像データセット 2020"), "腰椎x線画像データセット2020"),
    ("title korean", ids.norm_title("요추 X선 데이터"), "요추x선데이터"),
    ("title portuguese", ids.norm_title("Radiografias da coluna lombar: avaliação"), "radiografiasdacolunalombaravaliação"),
    ("title None", ids.norm_title(None), ""),
    ("family name", ids.norm_family_name("Müller-Löwe"), "müllerlöwe"),
    # canonical_string: first available of doi > pmid > pmcid > arxiv > url > native
    ("canon doi", ids.canonical_string({"doi": f"https://doi.org/{DOI}", "pmid": "1"}, "pubmed", 1), f"doi:{DOI}"),
    ("canon pmid", ids.canonical_string({"pmid": "PMID: 123", "pmcid": "PMC5"}, "x", 9), "pmid:123"),
    ("canon pmcid", ids.canonical_string({"pmcid": "pmc55"}, "x", 9), "pmcid:PMC55"),
    ("canon arxiv", ids.canonical_string({"arxiv": "arXiv:2105.14711v2"}, "x", 9), "arxiv:2105.14711"),
    ("canon url", ids.canonical_string({"url": "HTTP://Zenodo.org/records/10079370/?x=1#f"}, "x", 9), "url:https://zenodo.org/records/10079370"),
    ("canon native", ids.canonical_string({}, "zenodo", 10079370), "native:zenodo:10079370"),
    ("canon doi-like pmid ignored", ids.canonical_string({"pmid": "10.1038/x"}, "s2", "abc"), "native:s2:abc"),
    # record_id: prefix by source or type, 12 hex of SHA-1 over the canonical string
    ("rid hash", ids.record_id(f"doi:{DOI}", "pubmed"), "lit:" + hashlib.sha1(f"doi:{DOI}".encode()).hexdigest()[:12]),
    ("rid repo source", ids.record_id(f"doi:{DOI}", "zenodo")[:5], "repo:"),
    ("rid dataset type", ids.record_id(f"doi:{DOI}", "crossref", "Dataset")[:5], "repo:"),
    ("rid image type", ids.record_id(f"doi:{DOI}", "openalex", "image")[:5], "repo:"),
    ("rid article", ids.record_id(f"doi:{DOI}", "crossref", "journal-article")[:4], "lit:"),
    # normalised_ids: every key present, None when absent, repo_id passed through
    ("normalised_ids", ids.normalised_ids({"doi": f"doi:{DOI}", "pmid": "0", "repo_id": "r1"}),
     {"doi": DOI, "pmid": None, "pmcid": None, "arxiv": None, "url": None, "repo_id": "r1"}),
]
REC = {"ids": {"doi": DOI, "url": "http://zenodo.org/records/1/"}, "year": "2020",
       "title": "CT-ORG, a new dataset for multiple organ segmentation in computed tomography"}
TN = "ct org a new dataset for multiple organ segmentation in computed tomography"
CASES += [
    ("known doi", ids.known_item_matches(REC, {"match_rule": "doi", "doi": f"doi:{DOI}"}), "doi"),
    ("known doi other", ids.known_item_matches(REC, {"match_rule": "doi", "doi": "10.1/other"}), None),
    ("known title-year +1", ids.known_item_matches(REC, {"match_rule": "title-year", "title_norm": TN, "year": 2021}), "title-year"),
    ("known title-year +2", ids.known_item_matches(REC, {"match_rule": "title-year", "title_norm": TN, "year": 2022}), None),
    ("known title-year bad year", ids.known_item_matches({**REC, "year": "n.d."}, {"match_rule": "title-year", "title_norm": TN, "year": 2020}), None),
    ("known url", ids.known_item_matches(REC, {"match_rule": "url", "url": "https://zenodo.org/records/1"}), "url"),
    ("known doi item never by title", ids.known_item_matches(REC, {"match_rule": "doi", "doi": "", "title_norm": TN, "year": 2020}), None),
    ("known no rule", ids.known_item_matches(REC, {"doi": f"doi:{DOI}"}), None),
]


def main() -> int:
    n_fail = 0
    for name, got, want in CASES:
        ok = got == want
        n_fail += not ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f" -- got {got!r}, want {want!r}"))
    try:
        ids.canonical_string({"doi": None, "url": "ftp://x"}, "zenodo", None)
        print("[FAIL] unidentifiable record raises")
        n_fail += 1
    except ValueError:
        print("[PASS] unidentifiable record raises")
    print(f"\n{len(CASES) + 1 - n_fail}/{len(CASES) + 1} checks passed; {n_fail} failed")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
