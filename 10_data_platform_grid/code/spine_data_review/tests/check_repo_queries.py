"""Reviewer check: do the repository adapters send the strings queries/*.yaml records?

The adapters (sdr.search_repositories R1-R8, sdr.search_platforms R9-R14, sdr.search_figure_routes
F1, F4-F8) read their strings through sdr.repo_run.load_repo_queries, i.e. queries/repositories.yaml
and queries/literature.yaml, the files the appendix prints. This script lists every query id an
adapter references (literal ids found in the three module sources, plus the grid/term families the
adapters expand through repo_run._family and _first), reports any id absent from the YAML, and, for
every YAML id marked verbatim_in_markdown, that its string is byte-identical to information_sources.md.
It also lists YAML ids no adapter executes. Run from spine_data_review/:
  ~/sdr_venv/bin/python tests/check_repo_queries.py
Exit 1 when an adapter references an id the YAML does not carry.
"""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sdr.common import load_queries, review_root
from sdr.repo_run import load_repo_queries

md = load_queries()
yml = load_repo_queries()
src = "\n".join((review_root() / "sdr" / f).read_text(encoding="utf-8") for f in ("search_repositories.py", "search_platforms.py", "search_figure_routes.py"))

# literal ids: Q["<id>"] and f"<prefix>_{i:02d}" loops, reconstructed from the adapters' ranges
used = set(re.findall(r'Q\["([a-z0-9_]+)"\]', src)) | set(re.findall(r'_first\(Q, "([a-z0-9_]+)"', src))
used |= {f"hf_{i:02d}" for i in range(1, 24)} | {f"github_{i:02d}" for i in range(1, 19)} | {"github_c01", "github_c02"}
used |= {f"pwc_{i:02d}" for i in range(1, 7)} | {f"openi_{i:02d}" for i in range(1, 19)} | {f"jstage_{i:02d}" for i in range(1, 15)}
used |= {f"koreamed_{i:02d}" for i in range(1, 10)} | {f"scielo_{i:02d}" for i in range(1, 12)} | {f"redalyc_{i:02d}" for i in range(1, 10)}
used |= {f"commons_c{i:02d}" for i in range(1, 8)} | {f"osf_{i:02d}" for i in range(1, 25)} | {f"mendeley_{i:02d}" for i in range(1, 9)}
used |= {f"odl_t{i:02d}" for i in range(1, 9)} | {"odl_01", "odl_02", "odl_03", "kaggle_mention", "hf_mention"}
used |= {"zenodo_02", "figshare_02", "datacite_02", "gc_list", "physionet_list", "tcia_list"}  # referenced as Q[qid] inside loops
# families expanded by repo_run._family(Q, prefix, base_re): every YAML id matching prefix+base
families = [("dryad_", r"g\d\d"), ("kaggle_", r"g\d\d"), ("kaggle_", r"c\d\d"), ("commons_", r"g\d\d")]
fam_ids = {k for k in yml for p, b in families if re.fullmatch(p + b, k)}
used |= fam_ids
used -= {k for k in used if re.fullmatch(r"[gt]\d\d", k)}  # markdown primitives are fixture fallbacks, not YAML ids

print("== adapter-referenced ids absent from queries/*.yaml (the appendix source)")
missing = sorted(q for q in used if q not in yml)
for q in missing:
    print("  MISSING in yaml:", q)
print("  missing:", len(missing))
print("== family sizes the adapters expand from the YAML")
for p, b in families:
    print(f"  {p}{b}: {sum(1 for k in yml if re.fullmatch(p + b, k))} ids")
print("== YAML ids marked verbatim_in_markdown whose string differs from information_sources.md")
n = 0
for q in sorted(used & set(yml)):
    v = yml[q]
    if not v.get("verbatim_in_markdown"):
        continue
    ref = v.get("markdown_id") or v.get("grid_id") or q
    if ref not in md:
        n += 1; print(f"  NO MARKDOWN BLOCK {q} (ref {ref})")
    elif md[ref]["string"] != v["string"]:
        n += 1; print(f"  DIFF {q}:\n    md : {md[ref]['string'][:200]}\n    yml: {v['string'][:200]}")
print("  mismatches:", n)
print("== YAML ids no adapter executes (literature ids belong to sdr.search_literature; not_run_reason ids are written as not-run)")
executed = used | {"openi_enrich", "koreamed_enrich"} | {f"openi_{i:02d}_{it}" for i in range(1, 19) for it in ("xg", "c")}
for q in sorted(yml):
    if q not in executed and not q.startswith(("pubmed", "epmc", "openalex", "s2_", "arxiv", "biorxiv", "medrxiv", "crossref", "springer")):
        print("  never executed:", q, "| section:", yml[q].get("section"), "| not_run_reason:", bool(yml[q].get("not_run_reason")))
sys.exit(1 if missing else 0)
