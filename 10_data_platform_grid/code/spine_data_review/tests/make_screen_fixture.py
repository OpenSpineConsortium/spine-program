"""Build the hand-countable fixture for sdr.dedup_prescreen (review of the 'screen' module).

Seventeen records over ten source files, designed so that merge rules 0, 1, 3, 4 and 5 fire
exactly once and every prescreen outcome appears, plus three traps the protocol names:
  (a) the same canonical URL found by two sources (github + pwc) -> one identical record_id in
      two files; PROTOCOL.md 7.1 / E7 say identical records are removed at de-duplication and
      counted there (rule 0), not screened twice;
  (b) a derived Zenodo deposit whose description cites its parent article's DOI in a
      derived-from context; PROTOCOL.md 7.6 says a derived dataset is not a duplicate of its
      parent, so rule 6 must NOT fire on it (it is counted as rule_6_skipped_derived_context and
      the deposit keeps its own screening row). The positive rule-6 case (IsSupplementTo) is
      exercised by `sdr.dedup_prescreen --selftest`, not here;
  (c) a Zenodo version DOI whose known-item row carries the concept DOI (ctspinopelvic1k).
The expected counts in expected_screen_counts.json are written here BY HAND (literal numbers),
not computed from the module, so the test is a genuine comparison.

Usage: ~/sdr_venv/bin/python tests/make_screen_fixture.py   (writes tests/fixtures/screen_run/records/)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
from sdr.ids import canonical_string, record_id  # noqa: E402

OUT = HERE / "fixtures" / "screen_run" / "records"
TS = "2026-09-19T00:00:00Z"

VERSE_DOI = "10.1016/j.media.2021.102166"
VERSE_TITLE = "VerSe: A Vertebrae labelling and segmentation benchmark for multi-detector CT images"
VERSE_ABS = ("We present VerSe, a benchmark of 374 multi-detector CT scans with vertebrae labels from C1 to L6. "
             "Segmentation masks were drawn by experts and the challenge data can be downloaded from OSF.")
CTSPINE_TITLE = "CTSpine1K: A Large-Scale Dataset for Spinal Vertebrae Segmentation in Computed Tomography"
CTSPINE_ABS = "A dataset of 1005 CT volumes with vertebra masks."
XR_TITLE = "A public dataset of lumbar spine radiographs for level identification"
XR_ABS = "We release 600 lateral lumbar spine radiographs. The dataset is publicly available on Zenodo."


def rec(source: str, qid: str, ids: dict, title: str, abstract: str, year, rtype=None, raw=None, native=None) -> dict:
    canon = canonical_string(ids, source, native)
    rid = record_id(canon, source, rtype)
    full = {"doi": None, "pmid": None, "pmcid": None, "arxiv": None, "url": None, "repo_id": None, **ids}
    return {"record_id": rid, "canonical": canon, "source": source, "query_id": qid, "query_ids": [qid], "retrieved_at": TS,
            "ids": full, "title": title, "abstract_or_description": abstract, "year": year, "type": rtype, "raw": raw or {}}


def build() -> dict[str, list[dict]]:
    f: dict[str, list[dict]] = {}
    # --- pubmed: VerSe (twice, a within-source duplicate), an MRI paper, a rat paper
    p1 = rec("pubmed", "pubmed_01", {"doi": VERSE_DOI, "pmid": "34340104"}, VERSE_TITLE, VERSE_ABS, 2021, "journal-article",
             {"authors": ["Sekuboyina A"]})
    p1b = dict(p1, query_id="pubmed_02", query_ids=["pubmed_02"])
    p2 = rec("pubmed", "pubmed_01", {"doi": "10.1000/mri.1", "pmid": "2"}, "A lumbar spine MRI dataset for disc degeneration grading",
             "T2-weighted MRI of 200 patients; the dataset is publicly available.", 2020, "journal-article", {"authors": ["Lee J"]})
    p3 = rec("pubmed", "pubmed_01", {"doi": "10.1000/rat.1", "pmid": "3"}, "Vertebral morphology in rats by micro-computed tomography",
             "Micro-computed tomography of 30 rats.", 2019, "journal-article", {"authors": ["Kim S"]})
    f["pubmed"] = [p1, p1b, p2, p3]
    # --- openalex: VerSe again (rule 1), and the radiograph paper (rule 5 partner in crossref)
    o1 = rec("openalex", "openalex_01", {"doi": VERSE_DOI}, VERSE_TITLE, VERSE_ABS[:80], 2021, "article",
             {"authorships": [{"author": {"display_name": "Anjany Sekuboyina"}}]})
    o2 = rec("openalex", "openalex_01", {"doi": "10.1000/spinexr.2"}, XR_TITLE, XR_ABS, 2022, "article",
             {"authorships": [{"author": {"display_name": "Jane Doe"}}]})
    f["openalex"] = [o1, o2]
    # --- crossref: same title, same first author, year + 1, no DOI -> rule 5
    c1 = rec("crossref", "crossref_01", {"url": "https://example.org/spinexr-2023"}, XR_TITLE, "", 2023, "journal-article",
             {"author": [{"family": "Doe", "given": "Jane"}]})
    f["crossref"] = [c1]
    # --- s2 (arXiv id only) and arxiv (arXiv id + DOI) -> rule 3
    s1 = rec("s2", "s2_01", {"arxiv": "2105.14711"}, CTSPINE_TITLE, CTSPINE_ABS, 2021, "preprint", {"authors": [{"name": "Yang Deng"}]})
    a1 = rec("arxiv", "arxiv_01", {"doi": "10.48550/arxiv.2105.14711", "arxiv": "2105.14711"}, CTSPINE_TITLE, CTSPINE_ABS, 2021, "preprint")
    f["s2"], f["arxiv"] = [s1], [a1]
    # --- zenodo: two versions of one concept (rule 4), a derived deposit citing VerSe (rule 6), a reference list (skipped)
    z1 = rec("zenodo", "zenodo_01", {"doi": "10.5281/zenodo.22642578", "repo_id": "22642578"}, "CTSpinoPelvic1K",
             "CT of 802 abdominopelvic records with per-level vertebrae, sacrum, hips and femora labels.", 2026, "dataset",
             {"conceptdoi": "10.5281/zenodo.22139642", "metadata": {"creators": [{"name": "Schwing, Gregory"}]}})
    z2 = rec("zenodo", "zenodo_01", {"doi": "10.5281/zenodo.22700000", "repo_id": "22700000"}, "CTSpinoPelvic1K v11",
             "CT of 802 abdominopelvic records, sacrum dissolved.", 2026, "dataset", {"conceptdoi": "10.5281/zenodo.22139642"})
    z3 = rec("zenodo", "zenodo_01", {"doi": "10.5281/zenodo.99", "repo_id": "99"}, "VerSe-derived L6 subset",
             f"Subset derived from VerSe (https://doi.org/{VERSE_DOI}): sixth lumbar vertebra CT masks for 28 subjects.", 2024, "dataset")
    z4 = rec("zenodo", "zenodo_01", {"doi": "10.5281/zenodo.100", "repo_id": "100"}, "Lumbar spine CT collection",
             "Lumbar spine CT collection. See 10.1000/a.1, 10.1000/b.2 and 10.1000/c.3 for related work.", 2023, "dataset")
    f["zenodo"] = [z1, z2, z3, z4]
    # --- github and pwc: the SAME canonical URL -> identical record_id in two files
    g1 = rec("github", "github_01", {"url": "https://github.com/MIRACLE-Center/CTPelvic1K"}, "CTPelvic1K",
             "Large-scale CT datasets of pelvic bones with sacrum.", 2021, "repository")
    w1 = rec("pwc", "pwc_01", {"url": "https://github.com/MIRACLE-Center/CTPelvic1K/"}, "CTPelvic1K",
             "Large-scale CT datasets of pelvic bones with sacrum.", 2021, "dataset")
    assert g1["record_id"] == w1["record_id"], "fixture: trailing slash must canonicalise to the same id"
    f["github"], f["pwc"] = [g1], [w1]
    # --- jstage (non-English route) and figshare (uncertain + fail:S)
    j1 = rec("jstage", "jstage_01", {"url": "https://www.jstage.jst.go.jp/article/x/1"}, "脊椎 CT データベースの構築", "", 2019, "article")
    f["jstage"] = [j1]
    f1 = rec("figshare", "figshare_01", {"url": "https://figshare.com/articles/dataset/1"}, "Scoliosis cohort images",
             "Images of 40 scoliosis patients.", 2020, "dataset")
    f2 = rec("figshare", "figshare_01", {"url": "https://figshare.com/articles/dataset/2"}, "Knee MRI cohort", "Knee MRI of 12 subjects.", 2020, "dataset")
    f["figshare"] = [f1, f2]
    return f


# Hand-derived expectations (PROTOCOL.md 7.1/7.2 applied on paper to the records above).
EXPECTED = {
    "identified_rows": 18,                       # rows in all files (pubmed has the within-source duplicate)
    "identified": 17,                            # after within-source de-duplication
    # rule 1: VerSe pubmed = openalex (same DOI); rule 3: CTSpine1K s2 = arxiv; rule 4: the two
    # CTSpinoPelvic1K versions; rule 5: the radiograph paper openalex = crossref; rule 0: github = pwc.
    # rule 6: 0, because the only candidate (z3) cites VerSe in a derived-from context (7.6) and z4's
    # three DOIs are a reference list; both are counted under their skipped_* keys.
    "merge": {"rule_0_identical_canonical": 1, "rule_1_doi": 1, "rule_2_pmid_pmcid": 0, "rule_3_arxiv": 1,
              "rule_4_concept_doi": 1, "rule_5_title_author_year": 1, "rule_6_related_identifier": 0,
              "rule_6_skipped_many_dois": 1, "rule_6_skipped_derived_context": 1},
    "after_merge_protocol": 12,                  # 17 - 4 rule merges (1, 3, 4, 5) - 1 identical-id record (github = pwc)
    "after_merge_if_identical_ids_not_merged": 13,
    # pass: VerSe, the radiograph paper, CTSpine1K, CTSpinoPelvic1K, the derived L6 subset (its own row),
    # the lumbar CT collection, CTPelvic1K; fail:M the MRI paper; fail:D the rat paper; fail:S knee MRI;
    # uncertain the scoliosis images (no modality word); non-English route the J-STAGE record.
    "prescreen_protocol": {"pass": 7, "fail:S": 1, "fail:M": 1, "fail:D": 1, "uncertain": 1, "pass:non-english-route": 1},
    "to_screen_protocol": 9,
    "flags": {"animal": 1, "mri": 2, "public": 2},   # mri: the MRI paper and the knee MRI deposit; public: PUBLIC_RE on the XR paper and the MRI paper
    "known_items_expected_by_protocol": ["verse", "ctspine1k", "ctspinopelvic1k"],   # ctspinopelvic1k via its concept DOI
    "note": "Values typed by hand from the protocol; the runner compares them to prisma_counts.json.",
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.jsonl"):
        old.unlink()
    files = build()
    for src, rows in files.items():
        with open(OUT / f"{src}.jsonl", "w", encoding="utf-8", newline="\n") as fh:
            for r in rows:
                fh.write(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n")
    (HERE / "expected_screen_counts.json").write_text(json.dumps(EXPECTED, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    n = sum(len(v) for v in files.values())
    print(f"wrote {len(files)} record files, {n} rows, to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
