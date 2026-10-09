"""Is Appendix A built from exactly the strings in queries/*.yaml (and information_sources.md)?

For a run dir, compares (1) what sdr.manuscript.load_query_records() will print as `query_string`
against the `string` of the same id in queries/*.yaml, (2) the run's queries.json `query_string`
against the YAML, (3) which record ids come from neither the YAML nor the run's queries.json (they
can only come from counts.json's source-keyed top level), and (4) whether every non-chase id in
load_query_records() appears in the rendered search_strings.tex. Prints ids and 80-char previews.
Run in WSL:  ~/sdr_venv/bin/python tests/check_query_strings.py runs/review_manuscript runs/review_manuscript/a/tables/search_strings.tex
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sdr import manuscript as M  # noqa: E402
from sdr.common import load_queries  # noqa: E402


def main(argv: list[str]) -> int:
    run_dir = ROOT / (argv[0] if argv else "runs/review_manuscript")
    tex = ROOT / argv[1] if len(argv) > 1 else None
    yaml_recs: dict[str, dict] = {}
    for y in sorted((ROOT / "queries").glob("*.y*ml")):
        yaml_recs.update(load_queries(y))
    md_recs = load_queries()
    run_q = json.loads((run_dir / "queries.json").read_text(encoding="utf-8")) if (run_dir / "queries.json").exists() else {}
    run_q = {k: v for k, v in run_q.items() if not k.startswith("_") and isinstance(v, dict)}
    counts = json.loads((run_dir / "counts.json").read_text(encoding="utf-8")) if (run_dir / "counts.json").exists() else {}
    recs = M.load_query_records(run_dir)
    print(f"yaml ids {len(yaml_recs)}; markdown ids {len(md_recs)}; run queries.json ids {len(run_q)}; counts.json top keys {len(counts)}; loaded records {len(recs)}")

    # (1) rendered string vs YAML for ids the YAML defines
    diff1 = [k for k in yaml_recs if k in recs and recs[k].get("query_string") != yaml_recs[k].get("string")]
    print(f"(1) ids whose rendered query_string differs from queries/*.yaml string: {len(diff1)}")
    for k in diff1[:8]:
        print(f"    {k}: yaml={str(yaml_recs[k].get('string'))[:80]!r} rendered={str(recs[k].get('query_string'))[:80]!r}")

    # (2) run queries.json vs YAML (what was SENT vs what the protocol says)
    diff2 = [k for k in run_q if k in yaml_recs and run_q[k].get("query_string") not in (None, yaml_recs[k].get("string"))]
    print(f"(2) run ids whose sent query_string differs from the YAML: {len(diff2)} of {sum(1 for k in run_q if k in yaml_recs)} shared ids")
    for k in diff2[:8]:
        print(f"    {k}: yaml={str(yaml_recs[k].get('string'))[:80]!r} sent={str(run_q[k].get('query_string'))[:80]!r}")
    subids = [k for k in run_q if k not in yaml_recs]
    print(f"    run ids absent from the YAML (run-time sub-ids): {len(subids)}; e.g. {subids[:6]}")

    # (3) records that come only from counts.json's top level (source names, not query ids)
    only_counts = sorted(k for k in recs if k not in yaml_recs and k not in run_q and k not in md_recs
                         and not k.startswith("pilot_"))
    print(f"(3) loaded ids that are neither YAML, markdown, run queries.json nor pilot ids: {len(only_counts)}")
    print(f"    {only_counts[:32]}")
    roles = {recs[k].get("role") for k in only_counts}
    print(f"    their roles: {roles}; counted as search in Table 2 / numQueries: {sum(1 for k in only_counts if recs[k].get('role') in M.SEARCH_ROLES)}")
    print(f"    fields of the first: {sorted(recs[only_counts[0]]) if only_counts else None}")

    # (4) appendix coverage
    if tex and tex.exists():
        body = tex.read_text(encoding="utf-8")
        printed = {re.sub(r"\\allowbreak\{\}|\\_", lambda m: "_" if m.group(0) == "\\_" else "", i)
                   for i in re.findall(r"\\textbf\{\\texttt\{(.*?)\}\}", body)}
        expected = {k for k, r in recs.items() if M.source_key(k, r) != "chase"}
        print(f"(4) appendix prints {len(printed)} ids; expected non-chase ids {len(expected)}; missing {len(expected - printed)}; extra {len(printed - expected)}")
        print(f"    bogus source-keyed ids printed in the appendix: {sorted(printed & set(only_counts))[:32]}")
        print(f"    '(no string recorded)' blocks: {body.count('(no string recorded)')}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
