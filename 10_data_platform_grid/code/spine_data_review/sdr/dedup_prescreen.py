"""Cross-source de-duplication and rule-based prescreen of the search records (PROTOCOL.md 7.1, 7.2).

WHY ONE MODULE FOR BOTH. The PRISMA flow's first three boxes (identified, duplicates removed,
records to screen) are one arithmetic identity, and the prescreen strata are defined on the
merged record, so the counts have to be produced by the code that made the merge. Doing them
in one pass means one `prisma_counts.json` whose numbers add up by construction:

    identified (after within-source de-duplication)
  - duplicates removed at merge (rules 1-6, each counted)
  = after_merge = pass + fail:S + fail:M + fail:D + uncertain + pass:non-english-route

Reads  <run-dir>/records/<source>.jsonl  (PROTOCOL.md section 15: record_id, source, query_id,
       retrieved_at, ids{doi,pmid,pmcid,arxiv,url,repo_id}, title, abstract_or_description,
       year, type, raw). Optional top-level keys an adapter may add and this module prefers over
       digging in `raw`: first_author, concept_doi, related_identifiers [{identifier, relation}].
Writes <run-dir>/merged.jsonl          one row per unique record, no `raw` (members are in records/)
       <run-dir>/screening_sheet.csv   one row per unique record for the reviewer (sdr/screen.py)
       <run-dir>/prisma_counts.json    the counts above, per source and per source class

MERGE (7.1): union-find over record indices, one pass per rule in protocol order, so each
duplicate is attributed to the first rule that would have caught it. Rules 1-3 key on the
normalised identifiers (norm_doi, norm_pmid, norm_pmcid, norm_arxiv), not the adapter's raw
strings, so a DOI in upper case or an arXiv id with a version suffix still merges. Rule 0 is
the identity clause of E7: the same canonical string found by two sources (github and pwc on
one GitHub URL, hf and hf-mention, datacite and zenodo) yields one record_id in two files, and
such identical records are removed and counted here, not screened twice. It runs after rules
1-3 so that an identical DOI, PMID or arXiv pair is attributed to the protocol rule that names
it and rule 0 counts only the URL- and native-id canonicals no identifier rule reads; whatever
the attribution, run_pipeline asserts that no two merged rows share a record_id. Rule 3
(arXiv <-> DOI) is the arXiv-id key: an arXiv record whose adapter filled `ids.doi` already
joins its article under rule 1, and a record carrying only the arXiv id joins that record here.
Rule 4 reads the Zenodo concept DOI (`concept_doi`, `raw.conceptdoi`, `raw.conceptrecid`, or a
DataCite IsVersionOf on prefix 10.5281). Rule 5 never uses fuzzy matching, never merges titles
under 25 characters, and unions each member of a title+author group with the group's earliest
member only when the year gap is at most one, so 2019/2020/2021 do not chain into one record.
Rule 6 links a REPOSITORY record to an ARTICLE (`lit:` target only, never repo <-> repo) through
IsSupplementTo / IsDescribedBy / IsReferencedBy identifiers and through DOI strings in its
description. Two things are deliberately not links: a description that cites more than two
foreign DOIs is a reference list (`rule_6_skipped_many_dois`), and a DOI whose surrounding 80
characters say derived / based on / subset / extends / built on / version of names a PARENT,
which 7.6 says is a different dataset (`rule_6_skipped_derived_context`). Every DOI a record
links to, merged or not, is kept on the merged row as `related_dois` for the mapping step.

PRESCREEN (7.2, Appendix A): the three positive regexes over title + abstract_or_description.
A record found only by literature sources whose merged abstract is empty is `uncertain` before
MODALITY_RE is tried (`NO_ABSTRACT_RULE`), because Semantic Scholar elides the abstract of every
paper whose publisher withholds it and the three regexes would otherwise record thousands of
exclusions as "no modality term" when nothing was there to match; the count is its own row in
prisma_counts.json and in the flow. Repository sources (R1-R14) and the figure routes (F1-F4) do
not need DATASET_RE and get `uncertain` instead of `fail:M`; the non-English routes (F5-F8) are never prescreened and every
hit goes to the reviewer with the per-language flags recorded. The negative flags (MRI, animal,
phantom, synthetic) and PUBLIC_RE are recorded and never exclude. A merged record found by
several sources is prescreened under its most lenient source (any repository or figure source
makes it a repository record for this purpose; any F5-F8 source makes it non-English-route),
because the protocol's leniency is a property of where the record was found. The regexes are
the built-in copies of Appendix A unless `screen/prescreen_rules.yaml` exists (keys SPINE_RE,
MODALITY_RE, DATASET_RE, MRI_RE, ANIMAL_RE, PHANTOM_RE, SYNTH_RE, PUBLIC_RE, SPINE_RE_JA,
SPINE_RE_KO, SPINE_RE_ES_PT); either way the SHA-1 of the rule text is written to the counts.

CLI: python -m sdr.dedup_prescreen --run-dir runs/<date> --run-date <date> [--limit N] [--dry-run]
     [--rules screen/prescreen_rules.yaml] [--sheet-dir DIR] [--selftest]
No network. `--limit` keeps the first N records (by record id) of every source. `--dry-run`
computes everything and prints the counts without writing. `--selftest` runs the merge and the
prescreen on eleven synthetic records and asserts the expected outcome of every rule, that a
derived deposit stays its own row, and that a known item carrying a Zenodo concept DOI is
matched through the merged row's `concept_doi` / `member_dois`.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from sdr import PROTOCOL_VERSION
from sdr.common import (REPO_SOURCES, RunDir, add_common_args, dump_json, init_run_dir, known_item_matches, load_yaml,
                        norm_arxiv, norm_doi, norm_family_name, norm_pmcid, norm_pmid, norm_title, read_jsonl, review_root,
                        write_jsonl)

# ----------------------------------------------------------------------------- rules (PROTOCOL.md Appendix A, 4.3)
DEFAULT_RULES = {
    "SPINE_RE": r"\b(spine|spinal|vertebr\w*|lumbar|lumbo-?sacral|thoraco-?lumbar|sacrum|cervical spine|thoracic spine|scoliosis|spondylo\w*|intervertebral|pedicle)\b",
    "MODALITY_RE": r"(\bcomputed tomograph\w*|\bCT\b|\bCBCT\b|cone-?beam|radiograph\w*|\bx-?rays?\b|roentgen\w*|fluoroscop\w*|\bc-?arm\b|image intensifier|\bDXA\b|\bDEXA\b|dual-energy x-?ray|absorptiometry|vertebral fracture assessment|\bEOS\b|biplanar|plain films?)",
    "DATASET_RE": r"\b(data\s?sets?|database|benchmark\w*|challenge|publicly available|public(ly)? (data|release)|open(-| )?(access|source|data)|data descriptor|corpus|image collection|repository|zenodo|figshare|physionet|kaggle|hugging ?face|grand-?challenge|github|download)\b",
    "MRI_RE": r"\b(MRI?|magnetic resonance|T[12]\*?-?weighted)\b",
    "ANIMAL_RE": r"\b(rats?|mice|mouse|murine|porcine|pigs?|swine|ovine|sheep|bovine|canine|dogs?|rabbits?|goats?|macaques?|primates?|zebrafish)\b",
    "PHANTOM_RE": r"\b(phantoms?|cadaver\w*|ex[- ]vivo|sawbones?)\b",
    "SYNTH_RE": r"\b(synthetic|simulated|DRR|digitally reconstructed|GAN|diffusion model)\b",
    "PUBLIC_RE": r"(data|dataset|images?|scans?|volumes?|radiographs?|cases) (are|is|were|will be|have been|has been) (made )?(publicly|freely|openly) available|(data|dataset|images?) (is|are) available (at|from|on) https?://|(data|dataset|images?) (is|are) (available|deposited|hosted) (at|from|on|in) (zenodo|figshare|physionet|kaggle|hugging ?face|github|synapse|osf|dryad|mendeley data|the cancer imaging archive|tcia|ieee dataport)",
    "SPINE_RE_JA": r"(脊椎|椎体|腰椎|頸椎|頚椎|胸椎|仙骨|側弯|側彎|脊柱)",
    "SPINE_RE_KO": r"(척추|요추|경추|흉추|천골|척추측만)",
    "SPINE_RE_ES_PT": r"(columna|vértebra|vertebra|coluna|lumbar|cervical|torácica|toracica|sacro|escoliosis|escoliose)",
}
FLAG_RULES = ("MRI_RE", "ANIMAL_RE", "PHANTOM_RE", "SYNTH_RE", "PUBLIC_RE")
LANG_RULES = ("SPINE_RE_JA", "SPINE_RE_KO", "SPINE_RE_ES_PT")
NON_ENGLISH = frozenset({"jstage", "koreamed", "scielo", "redalyc"})                       # F5-F8
FIGURE_ROUTES = frozenset({"openi", "multicare", "openpmc", "commons"})                    # F1-F4
FULL_HARVEST = frozenset({"biorxiv", "medrxiv", "physionet", "tcia", "gc", "pwc"})         # L6, R7, R8, R11, R13
CLASS_ORDER = ("non-english-route", "figure-route", "repository", "full-harvest", "literature")
OUTCOMES = ("pass", "fail:S", "fail:M", "fail:D", "uncertain", "pass:non-english-route")
# The rule string of 7.2's no-abstract clause; sdr.flow_counts counts the sheet rows that carry it.
NO_ABSTRACT_RULE = "no abstract in any source that found this record"
MERGE_RULES = ("rule_0_identical_canonical", "rule_1_doi", "rule_2_pmid_pmcid", "rule_3_arxiv", "rule_4_concept_doi",
               "rule_5_title_author_year", "rule_6_related_identifier")
_REL_OK = frozenset({"issupplementto", "isdescribedby", "isreferencedby"})
_DOI_IN_TEXT = re.compile(r"10\.\d{4,9}/[^\s\"'<>)\]]+")
_DERIVED_CONTEXT = re.compile(r"derived|based on|subset|extends|built (up)?on|version of", re.I)
_CONTEXT_CHARS = 80
SHEET_COLUMNS = ["record_id", "to_screen", "prescreen_outcome", "rule_fired", "source_class", "sources", "query_ids",
                 "n_members", "merge_rules", "flags", "lang_flags", "known_item", "title", "year", "type", "doi",
                 "pmid", "pmcid", "arxiv", "url", "first_author", "abstract_or_description", "member_record_ids"]


def load_rules(path: Path | None) -> tuple[dict[str, re.Pattern], str, str]:
    """(compiled rules, sha1 of the rule text, where they came from). A YAML file overrides the
    built-in Appendix A copies key by key; the sha1 covers the effective set so a rule change is
    visible in prisma_counts.json."""
    rules, origin = dict(DEFAULT_RULES), "built-in (PROTOCOL.md Appendix A)"
    if path and path.exists():
        rules.update({k: str(v) for k, v in (load_yaml(path) or {}).items() if k in rules})
        origin = str(path)
    sha1 = hashlib.sha1(json.dumps(rules, sort_keys=True).encode("utf-8")).hexdigest()
    return {k: re.compile(v, re.I) for k, v in rules.items()}, sha1, origin


def source_class(source: str) -> str:
    """Audit stratum of a source (7.2): non-english-route, figure-route, repository, full-harvest
    (checked before repository, because R7/R8/R11/R13 are harvested in full), literature."""
    if source in NON_ENGLISH:
        return "non-english-route"
    if source in FIGURE_ROUTES:
        return "figure-route"
    if source in FULL_HARVEST:
        return "full-harvest"
    return "repository" if source in REPO_SOURCES else "literature"


def prescreen(text: str, sources: set[str], rules: dict[str, re.Pattern], abstract: str = "") -> tuple[str, str]:
    """(outcome, rule that fired) for one merged record. Leniency follows the most lenient source.

    The no-abstract clause (7.2): a record found only by literature sources and carrying no abstract in any of
    them goes to `uncertain`, before MODALITY_RE and DATASET_RE are tried. Semantic Scholar elides the abstract
    of every paper whose publisher forbids redistributing it - 406 of the 1,000 records on the first s2_01 page,
    405 of which fail the three regexes on their title alone - and Spine, Eur Spine J and J Neurosurg Spine sit
    with those publishers, so roughly 4,700 records of an 11,631-hit query reach this function with a title and
    nothing else. Records S2 shares with PubMed, Europe PMC or Crossref are saved by the merge, which keeps the
    longest member abstract; S2-only records - conference proceedings, IEEE/CVF, theses, where challenge-dataset
    papers such as AASCE live - are not. Without this clause they are counted as fail:M or fail:D, and the flow
    would attribute thousands of exclusions to "no modality term" or "no dataset term" when the true reason is
    that no abstract was available to search. `abstract` is the merged record's abstract_or_description; when it
    is not passed the clause never fires and the three regexes decide as before."""
    if sources & NON_ENGLISH:
        return "pass:non-english-route", "non-english route F5-F8: not prescreened"
    lenient = bool(sources & (REPO_SOURCES | FIGURE_ROUTES))
    if not rules["SPINE_RE"].search(text):
        return "fail:S", "SPINE_RE did not match"
    if not abstract.strip() and all(source_class(s) == "literature" for s in sources):
        return "uncertain", NO_ABSTRACT_RULE
    if not rules["MODALITY_RE"].search(text):
        return ("uncertain", "MODALITY_RE did not match (repository/figure source)") if lenient \
            else ("fail:M", "MODALITY_RE did not match")
    if lenient:
        return "pass", "SPINE_RE and MODALITY_RE matched; DATASET_RE implied by source"
    if not rules["DATASET_RE"].search(text):
        return "fail:D", "DATASET_RE did not match"
    return "pass", "SPINE_RE, MODALITY_RE and DATASET_RE matched"


# ----------------------------------------------------------------------------- record fields
def _text(rec: dict) -> str:
    return f"{rec.get('title') or ''} {rec.get('abstract_or_description') or ''}"


def _year(rec: dict) -> int | None:
    try:
        return int(str(rec.get("year"))[:4]) if rec.get("year") not in (None, "") else None
    except ValueError:
        return None


def _first_author(rec: dict) -> str:
    """Normalised family name of the first author for merge rule 5, from `first_author` when the
    adapter set it, else from the common shapes in `raw` (PubMed, OpenAlex, Crossref, S2, Zenodo,
    DataCite). Empty string when none is found, and rule 5 then never merges the record."""
    raw = rec.get("raw") or {}
    cands = [rec.get("first_author"), rec.get("authors"), raw.get("authors"), raw.get("authorships"),
             raw.get("author"), raw.get("creators"), (raw.get("metadata") or {}).get("creators"),
             (raw.get("attributes") or {}).get("creators"), raw.get("AuthorList")]
    for c in cands:
        x = c[0] if isinstance(c, list) and c else c
        if isinstance(x, dict):
            a = x.get("author") if isinstance(x.get("author"), dict) else x
            x = a.get("family") or a.get("LastName") or a.get("lastName") or a.get("familyName") or a.get("display_name") or a.get("name")
        if isinstance(x, str) and x.strip():
            toks = x.split()
            # "Doe, J" -> Doe; "Doe J" / "Doe JA" (MEDLINE form: trailing initials) -> Doe; "Jane Doe" -> Doe
            fam = x.split(",")[0] if "," in x else (toks[0] if len(toks) > 1 and toks[-1].isupper() and len(toks[-1]) <= 3 else toks[-1])
            return norm_family_name(fam)
    return ""


def _concept_key(rec: dict) -> str | None:
    raw = rec.get("raw") or {}
    c = rec.get("concept_doi") or raw.get("conceptdoi") or raw.get("conceptrecid")
    if not c:
        for e in (raw.get("attributes") or {}).get("relatedIdentifiers") or []:
            if str(e.get("relationType", "")).lower() == "isversionof" and "10.5281" in str(e.get("relatedIdentifier")):
                c = e.get("relatedIdentifier")
    return f"concept:{norm_doi(str(c)) or str(c).strip().lower()}" if c else None


def _related_dois(rec: dict) -> dict:
    """Rule 6 material of one record, own DOI excluded:
    `link`    DOIs that may merge it into an article: IsSupplementTo/IsDescribedBy/IsReferencedBy
              identifiers, plus DOIs in the description that are not in a derived-from context;
    `related` every DOI seen (linkable or not), kept on the merged row for the 7.6 mapping;
    `skipped_many` count of in-text DOIs dropped because the description held more than two
              (a reference list); `skipped_derived` count of in-text DOIs whose 80 surrounding
              characters name a parent (derived / based on / subset / ...)."""
    raw, own = rec.get("raw") or {}, norm_doi((rec.get("ids") or {}).get("doi"))
    link, related = set(), set()
    lists = [rec.get("related_identifiers"), (raw.get("metadata") or {}).get("related_identifiers"),
             (raw.get("attributes") or {}).get("relatedIdentifiers"), raw.get("relatedIdentifiers"), raw.get("relation")]
    for lst in lists:
        items = ([{"identifier": e.get("id"), "relation": k} for k, v in lst.items() if isinstance(v, list) for e in v]
                 if isinstance(lst, dict) else lst or [])
        for e in items:
            rel = str(e.get("relation") or e.get("relationType") or "").replace("-", "").replace("_", "").lower()
            d = norm_doi(e.get("identifier") or e.get("relatedIdentifier"))
            if rel in _REL_OK and d and d != own:
                link.add(d)
                related.add(d)
    text = rec.get("abstract_or_description") or ""
    in_text: dict[str, bool] = {}                       # doi -> found in a derived-from context
    for m in _DOI_IN_TEXT.finditer(text):
        d = norm_doi(m.group(0))
        if d and d != own:
            ctx = text[max(0, m.start() - _CONTEXT_CHARS): m.end() + _CONTEXT_CHARS]
            in_text[d] = in_text.get(d, False) or bool(_DERIVED_CONTEXT.search(ctx))
    if len(in_text) > 2:
        return {"link": link, "related": related, "skipped_many": len(in_text), "skipped_derived": 0}
    related |= set(in_text)
    link |= {d for d, derived in in_text.items() if not derived}
    return {"link": link, "related": related, "skipped_many": 0, "skipped_derived": sum(in_text.values())}


# ----------------------------------------------------------------------------- merge
class _UF:
    def __init__(self, n: int):
        self.p = list(range(n))

    def find(self, i: int) -> int:
        while self.p[i] != i:
            self.p[i] = self.p[self.p[i]]
            i = self.p[i]
        return i

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.p[max(ra, rb)] = min(ra, rb)
        return True


def merge(recs: list[dict]) -> tuple[list[list[int]], dict[str, int], list[dict]]:
    """Group `recs` (sorted by record_id) by rules 1-3, 0, 4-6 in that order (rule 0 after the
    identifier rules, see the module docstring). Returns (groups of indices, count of unions per
    rule, per-union log rows {rule, kept, merged, key})."""
    uf, counts, log = _UF(len(recs)), Counter({r: 0 for r in MERGE_RULES}), []
    counts["rule_6_skipped_many_dois"] = counts["rule_6_skipped_derived_context"] = 0

    def run(rule: str, keys_of):
        index: dict[str, int] = {}
        for i, r in enumerate(recs):
            for k in keys_of(r):
                if k in index:
                    if uf.union(index[k], i):
                        counts[rule] += 1
                        log.append({"rule": rule, "kept": recs[index[k]]["record_id"], "merged": r["record_id"], "key": k})
                else:
                    index[k] = i
        return index

    ids = lambda r: r.get("ids") or {}  # noqa: E731
    doi_index = run("rule_1_doi", lambda r: [f"doi:{d}"] if (d := norm_doi(ids(r).get("doi"))) else [])
    run("rule_2_pmid_pmcid", lambda r: [f"{k}:{v}" for k, f in (("pmid", norm_pmid), ("pmcid", norm_pmcid)) if (v := f(ids(r).get(k)))])
    run("rule_3_arxiv", lambda r: [f"arxiv:{a}"] if (a := norm_arxiv(ids(r).get("arxiv"))) else [])
    run("rule_0_identical_canonical", lambda r: [r["record_id"]])     # E7: same canonical string in two files
    run("rule_4_concept_doi", lambda r: [_concept_key(r)] if _concept_key(r) else [])
    by_title: dict[tuple[str, str], list[tuple[int, int]]] = defaultdict(list)
    for i, r in enumerate(recs):
        t, a, y = norm_title(r.get("title")), _first_author(r), _year(r)
        if len(t) >= 25 and a and y is not None:
            by_title[(t, a)].append((y, i))
    for (t, a), members in sorted(by_title.items()):
        members.sort()
        (y0, i0) = members[0]                       # every member is compared with the earliest, so no chaining
        for (y1, i1) in members[1:]:
            if y1 - y0 <= 1 and uf.union(i0, i1):
                counts["rule_5_title_author_year"] += 1
                log.append({"rule": "rule_5_title_author_year", "kept": recs[i0]["record_id"],
                            "merged": recs[i1]["record_id"], "key": f"title:{t[:40]}|{a}|{y0}-{y1}"})
    for i, r in enumerate(recs):
        if not r["record_id"].startswith("repo:"):
            continue
        rel = _related_dois(r)
        counts["rule_6_skipped_many_dois"] += 1 if rel["skipped_many"] else 0
        counts["rule_6_skipped_derived_context"] += rel["skipped_derived"]
        for d in sorted(rel["link"]):
            j = doi_index.get(f"doi:{d}")
            if j is None or not recs[j]["record_id"].startswith("lit:"):    # repo <-> repo is never a duplicate (7.6)
                continue
            if uf.union(i, j):
                counts["rule_6_related_identifier"] += 1
                log.append({"rule": "rule_6_related_identifier", "kept": r["record_id"], "merged": recs[j]["record_id"], "key": f"doi:{d}"})
    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(recs)):
        groups[uf.find(i)].append(i)
    return [sorted(g) for g in sorted(groups.values())], dict(counts), log


def build_merged(recs: list[dict], group: list[int], rules_used: list[str]) -> dict:
    """One merged row: the representative is the member with a DOI, then the longest abstract,
    then the smallest record id; ids are filled from every member, except `repo_id`, which is
    taken only from members whose DOI is the representative's (or who have none), so a deposit
    merged through rule 6 does not lend its Zenodo id to the article; found_by keeps every
    source. `member_dois` and `concept_doi` are kept because a known item may be filed under a
    version or concept DOI that is not the representative's; `related_dois` feeds the 7.6 mapping."""
    members = [recs[i] for i in group]
    rep = sorted(members, key=lambda r: (not (r.get("ids") or {}).get("doi"),
                                         -len(r.get("abstract_or_description") or ""), r["record_id"]))[0]
    rep_doi = norm_doi((rep.get("ids") or {}).get("doi"))
    ids = {k: None for k in ("doi", "pmid", "pmcid", "arxiv", "url", "repo_id")}
    for m in [rep, *members]:
        m_doi = norm_doi((m.get("ids") or {}).get("doi"))
        for k, v in (m.get("ids") or {}).items():
            if k == "repo_id" and m_doi not in (None, rep_doi):
                continue
            ids[k] = ids.get(k) or v
    member_dois = sorted({d for m in members if (d := norm_doi((m.get("ids") or {}).get("doi")))})
    concept = next((c[len("concept:"):] for m in [rep, *members] if (c := _concept_key(m))), None)
    related = set().union(*(_related_dois(m)["related"] for m in members if m["record_id"].startswith("repo:"))) - set(member_dois)
    abstract = max((m.get("abstract_or_description") or "" for m in members), key=len)
    year = next((_year(m) for m in [rep, *members] if _year(m) is not None), None)
    sources = sorted({m["source"] for m in members})
    member_ids = sorted({m["record_id"] for m in members})
    return {"record_id": rep["record_id"], "ids": ids, "title": rep.get("title") or "", "abstract_or_description": abstract,
            "year": year, "type": rep.get("type"), "sources": sources,
            "first_author": next((a for m in [rep, *members] if (a := _first_author(m))), ""),
            "query_ids": sorted({m.get("query_id") or "" for m in members} - {""}),
            "found_by": sorted(({"source": m["source"], "query_id": m.get("query_id"), "record_id": m["record_id"]}
                                for m in members), key=lambda d: (d["source"], d["query_id"] or "", d["record_id"])),
            "member_record_ids": member_ids, "n_members": len(member_ids), "member_dois": member_dois,
            "concept_doi": concept, "related_dois": sorted(related),
            "merge_rules": sorted(set(rules_used)), "source_classes": sorted({source_class(s) for s in sources}),
            "source_class": next(c for c in CLASS_ORDER if c in {source_class(s) for s in sources})}


# ----------------------------------------------------------------------------- pipeline
def load_records(rd: RunDir, limit: int | None) -> tuple[list[dict], dict[str, dict]]:
    """Records of every records/<source>.jsonl, de-duplicated within each source by record_id
    (the first row by record_id order kept), the first `limit` per source, sorted by record_id."""
    recs, per_source = [], {}
    for f in sorted(rd.records.glob("*.jsonl")):
        rows = sorted(read_jsonl(f), key=lambda r: (r.get("record_id") or "", r.get("query_id") or ""))
        seen, kept = set(), []
        for r in rows:
            if not r.get("record_id") or not r.get("source"):
                raise ValueError(f"{f.name}: a record without record_id or source cannot be merged")
            if r["record_id"] not in seen:
                seen.add(r["record_id"])
                kept.append(r)
        limited = kept[:limit] if limit else kept
        per_source[f.stem] = {"n_rows": len(rows), "n_after_within_source_dedup": len(limited),
                              "within_source_duplicates": len(rows) - len(kept), "source_class": source_class(f.stem),
                              "limit_applied": len(limited) < len(kept)}
        recs.extend(limited)
    return sorted(recs, key=lambda r: r["record_id"]), per_source


def load_known_items() -> list[dict]:
    p = review_root() / "screen" / "known_items.csv"
    return list(csv.DictReader(p.open(encoding="utf-8"))) if p.exists() else []


def known_item_rule(m: dict, item: dict) -> str | None:
    """`known_item_matches` on the merged row, then, for a DOI-keyed item, on each DOI the row
    carries besides its representative's: the Zenodo concept DOI and every member's version DOI.
    A known item filed under the concept DOI (screen/known_items.csv notes say so) would otherwise
    read as 'not retrieved' while both of its versions sit in the merged row."""
    hit = known_item_matches(m, item)
    if hit or (item.get("match_rule") or "").strip() != "doi":
        return hit
    others = sorted({d for d in [m.get("concept_doi"), *(m.get("member_dois") or [])] if d} - {norm_doi((m.get("ids") or {}).get("doi"))})
    return next(("doi" for d in others if known_item_matches({"ids": {"doi": d}}, item)), None)


def run_pipeline(recs: list[dict], per_source: dict, rules: dict[str, re.Pattern], known: list[dict]) -> tuple[list[dict], list[dict], dict]:
    """Merge, prescreen and count. Returns (merged rows, sheet rows, prisma counts without paths).
    Raises AssertionError before anything is written when the flow identity fails or two merged
    rows share a record_id (rule 0 must have folded them)."""
    groups, mcounts, mlog = merge(recs)
    rules_by_rec = defaultdict(list)
    for row in mlog:
        rules_by_rec[row["kept"]].append(row["rule"])
        rules_by_rec[row["merged"]].append(row["rule"])
    merged, sheet = [], []
    outcome_c, class_c, flag_c, ki = Counter(), defaultdict(Counter), Counter(), {}
    no_abstract = 0
    for g in groups:
        m = build_merged(recs, g, [r for i in g for r in rules_by_rec[recs[i]["record_id"]]])
        text = _text(m)
        outcome, fired = prescreen(text, set(m["sources"]), rules, m.get("abstract_or_description") or "")
        flags = sorted(k[:-3].lower() for k in FLAG_RULES if rules[k].search(text))
        lang = sorted(k[9:].lower() for k in LANG_RULES if rules[k].search(text)) if set(m["sources"]) & NON_ENGLISH else []
        item = next((k["item"] for k in known if known_item_rule(m, k)), "")
        if item:
            ki[item] = m["record_id"]
        m.update({"prescreen_outcome": outcome, "prescreen_rule": fired, "flags": flags, "lang_flags": lang,
                  "known_item": item or None, "to_screen": outcome in ("pass", "uncertain", "pass:non-english-route")})
        merged.append(m)
        outcome_c[outcome] += 1
        no_abstract += fired == NO_ABSTRACT_RULE
        class_c[m["source_class"]][outcome] += 1
        flag_c.update(flags)
        sheet.append({"record_id": m["record_id"], "to_screen": "yes" if m["to_screen"] else "no", "prescreen_outcome": outcome,
                      "rule_fired": fired, "source_class": m["source_class"], "sources": ";".join(m["sources"]),
                      "query_ids": ";".join(m["query_ids"]), "n_members": m["n_members"], "merge_rules": ";".join(m["merge_rules"]),
                      "flags": ";".join(flags), "lang_flags": ";".join(lang), "known_item": item, "title": m["title"],
                      "year": m["year"] if m["year"] is not None else "", "type": m["type"] or "", **{k: m["ids"][k] or "" for k in ("doi", "pmid", "pmcid", "arxiv", "url")},
                      "first_author": m["first_author"], "abstract_or_description": m["abstract_or_description"],
                      "member_record_ids": ";".join(m["member_record_ids"])})
    identified = sum(s["n_after_within_source_dedup"] for s in per_source.values())
    removed = sum(mcounts[r] for r in MERGE_RULES)
    counts = {"protocol_version": PROTOCOL_VERSION, "per_source": per_source, "identified": identified,
              "merge": mcounts, "duplicates_removed": removed, "after_merge": len(merged),
              "identity_check": {"identified_minus_duplicates_equals_after_merge": identified - removed == len(merged)},
              "prescreen": {o: outcome_c.get(o, 0) for o in OUTCOMES}, "prescreen_uncertain_no_abstract": no_abstract,
              "prescreen_by_source_class": {c: {o: class_c[c].get(o, 0) for o in OUTCOMES} for c in CLASS_ORDER},
              "to_screen": sum(1 for m in merged if m["to_screen"]), "flags": dict(sorted(flag_c.items())),
              "known_items": {"n_in_file": len(known), "n_matched": len(ki), "matched": dict(sorted(ki.items()))},
              "merge_log_n": len(mlog)}
    if identified - removed != len(merged):
        raise AssertionError(f"flow identity broken: {identified} - {removed} != {len(merged)}")
    dup = [k for k, n in Counter(m["record_id"] for m in merged).items() if n > 1]
    if dup:
        raise AssertionError(f"merged rows share a record_id (rule 0 should have folded them): {sorted(dup)}")
    return merged, sheet, counts


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:  # candidate for common.py
    """UTF-8 CSV with a fixed column order, LF line ends, sorted by record_id; path must be under review_root()."""
    p = Path(path).resolve()
    if review_root() not in p.parents:
        raise ValueError(f"refusing to write outside spine_data_review/: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: r["record_id"]))


def selftest(rules: dict[str, re.Pattern]) -> int:
    """Eleven synthetic records: rule 0 (one GitHub URL found by github and pwc, one record_id in two
    files), rule 1 (DOI, pubmed+openalex, one in upper case), rule 3 (arXiv id only, s2, versioned on one side), rule 4
    (two Zenodo versions of one concept), rule 6 (deposit IsSupplementTo the article), a derived
    deposit citing the article's DOI as its parent (must stay its own row), a J-STAGE record
    (non-English route), a repository record with no modality word (uncertain), and an S2-only
    record whose abstract the publisher elided (uncertain under the no-abstract rule, not fail:M).
    The known item carries the concept DOI and must be matched through the merged row."""
    title = "A large annotated dataset of lumbar spine radiographs for vertebra detection"
    abstract = "We release 500 lumbar spine radiographs with vertebra labels; the dataset is publicly available on Zenodo."
    art = {"ids": {"doi": "10.1000/spine.1"}, "title": title, "abstract_or_description": abstract, "year": 2021, "type": "journal-article"}
    recs = [{"record_id": "lit:000000000001", "source": "pubmed", "query_id": "pubmed_01", **art, "raw": {"authors": ["Doe J"]}},
            {"record_id": "lit:000000000002", "source": "openalex", "query_id": "openalex_01", **art, "ids": {"doi": "10.1000/SPINE.1", "arxiv": "2101.00001"}},
            {"record_id": "lit:000000000003", "source": "s2", "query_id": "s2_01", "ids": {"arxiv": "2101.00001v2"}, "title": title, "abstract_or_description": abstract, "year": 2021},
            {"record_id": "repo:000000000004", "source": "zenodo", "query_id": "zenodo_01", "ids": {"doi": "10.5281/zenodo.11", "repo_id": "11"}, "title": "Lumbar spine radiograph dataset v1",
             "abstract_or_description": "X-ray images of the lumbar spine", "year": 2021, "raw": {"conceptdoi": "10.5281/zenodo.10", "metadata": {"related_identifiers": [{"identifier": "10.1000/spine.1", "relation": "isSupplementTo"}]}}},
            {"record_id": "repo:000000000005", "source": "zenodo", "query_id": "zenodo_02", "ids": {"doi": "10.5281/zenodo.12", "repo_id": "12"}, "title": "Lumbar spine radiograph dataset v2",
             "abstract_or_description": "X-ray images of the lumbar spine", "year": 2022, "raw": {"conceptdoi": "10.5281/zenodo.10"}},
            {"record_id": "lit:000000000006", "source": "jstage", "query_id": "jstage_06", "ids": {"url": "https://www.jstage.jst.go.jp/article/x/1"}, "title": "脊椎 CT データベースの構築", "abstract_or_description": "", "year": 2019},
            {"record_id": "repo:000000000007", "source": "figshare", "query_id": "figshare_01", "ids": {"url": "https://figshare.com/articles/dataset/1"}, "title": "Scoliosis cohort images", "abstract_or_description": "Images of 40 scoliosis patients.", "year": 2020},
            {"record_id": "repo:000000000008", "source": "zenodo", "query_id": "zenodo_03", "ids": {"doi": "10.5281/zenodo.99", "repo_id": "99"}, "title": "Lumbar radiograph L6 subset",
             "abstract_or_description": "Subset derived from the lumbar radiograph dataset (https://doi.org/10.1000/spine.1): x-ray images of 28 subjects with a sixth lumbar vertebra.", "year": 2023},
            {"record_id": "repo:000000000009", "source": "github", "query_id": "github_01", "ids": {"url": "https://github.com/a/spine-xr"}, "title": "spine-xr", "abstract_or_description": "Lumbar radiograph code and data.", "year": 2022},
            {"record_id": "repo:000000000009", "source": "pwc", "query_id": "pwc_01", "ids": {"url": "https://github.com/a/spine-xr"}, "title": "spine-xr", "abstract_or_description": "Lumbar radiograph code and data.", "year": 2022},
            {"record_id": "lit:000000000010", "source": "s2", "query_id": "s2_01", "ids": {"doi": "10.1000/elided.1"}, "title": "Fusion outcomes at the lumbosacral junction",
             "abstract_or_description": "", "year": 2018, "raw": {"abstract_elided": True, "disclaimer": "the following paper fields have been elided by the publisher: {abstract}"}}]
    known = [{"item": "lumbar-xr", "match_rule": "doi", "doi": "10.5281/zenodo.10"}]
    per_source = {s: {"n_rows": n, "n_after_within_source_dedup": n} for s, n in Counter(r["source"] for r in recs).items()}
    merged, _, counts = run_pipeline(sorted(recs, key=lambda r: r["record_id"]), per_source, rules, known)
    m = counts["merge"]
    expect = {"rule_0_identical_canonical": 1, "rule_1_doi": 1, "rule_3_arxiv": 1, "rule_4_concept_doi": 1,
              "rule_6_related_identifier": 1, "rule_6_skipped_derived_context": 1}
    got = {k: m[k] for k in expect}
    outcomes = {x["record_id"]: x["prescreen_outcome"] for x in merged}
    lead = next(x for x in merged if x["record_id"] == "lit:000000000001")
    derived = next((x for x in merged if x["record_id"] == "repo:000000000008"), None)
    no_abs = next((x for x in merged if x["record_id"] == "lit:000000000010"), None)
    checks = {"merge_counts": got == expect, "after_merge": counts["after_merge"] == 6,
              "outcomes": outcomes.get("lit:000000000001") == "pass" and outcomes.get("lit:000000000006") == "pass:non-english-route"
              and outcomes.get("repo:000000000007") == "uncertain",
              "no_abstract_uncertain": no_abs is not None and no_abs["prescreen_rule"] == NO_ABSTRACT_RULE
              and no_abs["prescreen_outcome"] == "uncertain" and counts["prescreen_uncertain_no_abstract"] == 1,
              "n_members": lead["n_members"] == 5 and len(lead["member_record_ids"]) == 5,
              "repo_id_not_unioned_across_dois": lead["ids"]["repo_id"] is None,
              "concept_and_member_dois": lead["concept_doi"] == "10.5281/zenodo.10" and "10.5281/zenodo.12" in lead["member_dois"],
              "known_item_via_concept_doi": counts["known_items"]["matched"] == {"lumbar-xr": "lit:000000000001"},
              "derived_keeps_own_row": derived is not None and derived["related_dois"] == ["10.1000/spine.1"] and "zenodo.99" not in json.dumps(lead),
              "identical_rows_folded": next(x for x in merged if x["record_id"] == "repo:000000000009")["n_members"] == 1}
    ok = all(checks.values())
    print(json.dumps({"merge": m, "after_merge": counts["after_merge"], "outcomes": outcomes, "checks": checks}, indent=2, ensure_ascii=False))
    print("selftest: ok" if ok else "selftest: FAIL")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = add_common_args(argparse.ArgumentParser(prog="python -m sdr.dedup_prescreen", description=__doc__.split("\n")[0]))
    ap.add_argument("--rules", default=str(review_root() / "screen" / "prescreen_rules.yaml"), help="YAML overriding Appendix A regexes")
    ap.add_argument("--sheet-dir", default=None, help="where screening_sheet.csv and prisma_counts.json go (default: the run dir)")
    ap.add_argument("--selftest", action="store_true", help="run the synthetic ten-record check and exit")
    a = ap.parse_args(argv)
    rules, rules_sha1, rules_origin = load_rules(Path(a.rules))
    if a.selftest:
        return selftest(rules)
    rd = RunDir(Path(a.run_dir)) if a.dry_run else init_run_dir(a.run_dir, a.run_date, argv)
    recs, per_source = load_records(rd, a.limit)
    if not recs:
        print(f"no records under {rd.records}; nothing to merge", file=sys.stderr)
        return 1
    merged, sheet, counts = run_pipeline(recs, per_source, rules, load_known_items())
    out = Path(a.sheet_dir) if a.sheet_dir else rd.root
    out = out if out.is_absolute() else review_root() / out
    counts.update({"run_date": a.run_date, "limit": a.limit, "rules": {"sha1": rules_sha1, "origin": rules_origin},
                   "derived_from": sorted(str(p.relative_to(review_root())) for p in rd.records.glob("*.jsonl")),
                   "outputs": {"merged": str(rd.merged), "screening_sheet": str(out / "screening_sheet.csv")}})
    summary = {k: counts[k] for k in ("identified", "duplicates_removed", "after_merge", "prescreen", "to_screen", "merge")}
    if a.dry_run:
        print("dry run; would write", rd.merged, out / "screening_sheet.csv", out / "prisma_counts.json")
        print(json.dumps(summary, indent=2))
        return 0
    write_jsonl(rd.merged, merged, key=lambda r: r["record_id"])
    write_csv(out / "screening_sheet.csv", sheet, SHEET_COLUMNS)
    dump_json(out / "prisma_counts.json", counts)
    print(json.dumps(summary, indent=2))
    print(f"wrote {rd.merged} ({len(merged)} rows), {out / 'screening_sheet.csv'}, {out / 'prisma_counts.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
