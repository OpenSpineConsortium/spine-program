#!/usr/bin/env python3
"""Check the planning files against each other and against the files they cite. Standard library only.

    python3 data_platform/verify_planning.py            # prints a summary, writes verification_report.json

Checks (numbered as in VERIFICATION.md): V1 sources.yaml equals sources.json; V2 one manifest card per source and one
source per card; V3 every imaging row of the disk map has a layout row; V4 the batch item files are exactly the rows
to move; V5 every README.yaml template parses and names a known adapter; V6 every repository tool a command or the
migration plan names exists; V7 every command parses (shlex; bash -n is in reacquire/test_reacquire.py); V8 the word
check; V9 the manifest's citations resolve to files on this machine; V10 the generated blocks are filled; V11 bash -n on
every shell script here; V12 every Python file compiles for 3.6 syntax; V13 aliases are unique; V14 the numbers the
manifest quotes equal the plan's totals.
"""
import ast
import csv
import glob
import json
import os
import re
import shlex
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DESK = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(HERE, "lib"))
sys.path.insert(0, os.path.join(HERE, "db"))
import mini_yaml  # noqa: E402

SCRATCH = r"<session scratchpad; not a dependency>"
MEM = r"<memory notes; see MEMORY.md>"
PREFIX = {"ssn": REPO, "sscn": REPO, "nnunet": REPO, "ctsp": os.path.join(DESK, "CTSpinoPelvic1K-1"),
          "vfr": os.path.join(DESK, "NextPaper", "VerSeFusion"), "sps": os.path.join(DESK, "NextPaper", "spinopelvic-seg"),
          "xrsp": os.path.join(DESK, "XRaySpinoPelvic1K"), "sdet": os.path.join(DESK, "spine-detector"),
          "sdr": os.path.join(REPO, "spine_data_review"), "mem": MEM, "ostk": os.path.join(DESK, "OpenSpineToolkit"),
          "scr": SCRATCH, "dp": SCRATCH + "/dataplan", "cen": SCRATCH + "/census", "census": SCRATCH + "/census"}
R = {}
FORBIDDEN = "proven" + "ance"                     # spelled so that this file does not contain the word
# scripts that exist only on the grid, named on purpose (their cards say so)
GRID_ONLY = {"slurm/download_nhanes_full.sh"}
# cited paths that do not resolve on this machine, with the reason; every other unresolved citation fails V9
KNOWN_UNRESOLVED = {
    "xrsp:Spondylolisthesis": "false positive: the file name has spaces ('Spondylolisthesis Vertebral Landmark.zip'); it exists",
    "sscn:docs/fluoro_requests_eml/01..14_*.eml": "false positive: '01..14_*' is a range written in prose; docs/fluoro_requests_eml/*.eml exist",
    "ssn:slurm/download_raw.sh": "false positive: a CTSpinoPelvic1K-1 script cited without its ctsp: prefix in a family-E recipe; it exists there",
    "ssn:tools/identity/ts_alias.json": "the card's claim is that this file does not exist",
    "ssn:slurm/download_nhanes_full.sh": "grid-only script; the card says it is absent from the local repo",
    "ssn:tools/make_yolo_levels.py": "the card says the tool is not in the local checkout",
    "ssn:tools/make_mv_bands.py": "the card says the tool is not in the local checkout",
    "ssn:SchwingNet/results/repairs/CARMLSPINE_CHECK.md": "the card says it is absent locally",
    "ssn:SchwingNet/results/transitional_registry/acquisition/alias_pairs.csv": "the card says the dedupe outputs are on the grid only",
    "ssn:tools/carmlspine_multi_build.py": "FINDING: tools/realxray_banks.json names it as the builder of carmlspine_multi, but it is not in the "
                                           "local repository and has no git history",
}


def check(name, ok, detail):
    R[name] = dict(ok=bool(ok), detail=detail)
    print("%-4s %-6s %s" % (name, "ok" if ok else "FAIL", detail if isinstance(detail, str) else json.dumps(detail)[:300]))


def local(p):
    """The laptop's C:/ paths, as WSL sees them when this runs under Linux."""
    return p if os.name == "nt" or not p.startswith("C:/") else "/mnt/c/" + p[3:]


def resolve_cite(prefix, path):
    base = local(PREFIX[prefix])
    path = path.rstrip(".,;:)`'\"")
    if not path or "<" in path or "{" in path:
        return None
    p = os.path.join(base, path)
    if prefix == "mem" and not os.path.splitext(path)[1]:
        p += ".md"
    if "*" in p:
        return bool(glob.glob(p))
    return os.path.exists(p)


def main():
    doc = json.load(open(os.path.join(HERE, "sources.json"), encoding="utf-8"))
    S = doc["sources"]
    ids = [s["id"] for s in S]
    # V1
    y = mini_yaml.load(open(os.path.join(HERE, "sources.yaml"), encoding="utf-8"))
    same = y == doc
    try:
        import yaml
        same_py = yaml.safe_load(open(os.path.join(HERE, "sources.yaml"), encoding="utf-8")) == doc
    except ImportError:
        same_py = None
    check("V1", same and same_py is not False, "sources.yaml == sources.json (mini_yaml %s, PyYAML %s); %d sources" % (same, same_py, len(S)))
    # V2
    man = open(os.path.join(HERE, "DATA_MANIFEST.md"), encoding="utf-8").read()
    anchors = re.findall(r'<a id="([^"]+)"></a>', man)
    check("V2", sorted(anchors) == sorted(ids) and len(anchors) == len(set(anchors)),
          "manifest cards %d, sources %d, missing %s, extra %s" % (len(anchors), len(ids), sorted(set(ids) - set(anchors))[:5], sorted(set(anchors) - set(ids))[:5]))
    # V3, V4
    dm = list(csv.DictReader(open(os.path.join(HERE, "plan", "disk_map.csv"), encoding="utf-8")))
    lm = list(csv.DictReader(open(os.path.join(HERE, "plan", "layout_map.csv"), encoding="utf-8")))
    img = {r["path"] for r in dm if r["role"] in ("raw imaging source", "converted or derived imaging", "unknown")}
    mapped = {r["current_path"] for r in lm}
    check("V3", img <= mapped, "imaging rows in the disk map %d, mapped %d, unmapped %s" % (len(img), len(img & mapped), sorted(img - mapped)[:5]))
    moves = {(r["current_path"], r["target_path"]) for r in lm if r["action"] in ("move", "optional_move")}
    items = set()
    for f in glob.glob(os.path.join(HERE, "plan", "batch_items", "*.tsv")):
        for line in open(f, encoding="utf-8"):
            if line.startswith("#") or not line.strip():
                continue
            src, dst = line.split("\t")[:2]
            items.add((src, dst))
    check("V4", items == moves, "batch item rows %d, move rows %d" % (len(items), len(moves)))
    # V5
    import build_index
    bad = []
    for f in sorted(glob.glob(os.path.join(HERE, "plan", "readme_yaml", "*.yaml"))):
        d = mini_yaml.load(open(f, encoding="utf-8"))
        try:
            import yaml
            if yaml.safe_load(open(f, encoding="utf-8")) != d:
                bad.append(os.path.basename(f) + " (PyYAML differs)")
        except ImportError:
            pass
        if d.get("index_adapter") not in build_index.ADAPTERS:
            bad.append(os.path.basename(f) + " adapter " + str(d.get("index_adapter")))
        for sid in d.get("source_ids") or []:
            if sid not in ids and sid != "multisource_banks":
                bad.append(os.path.basename(f) + " unknown id " + sid)
    check("V5", not bad, "README.yaml templates %d; problems %s" % (len(glob.glob(os.path.join(HERE, "plan", "readme_yaml", "*.yaml"))), bad[:5]))
    # V6
    roots = {"${REPO}": REPO, "${DP}": HERE, "${CTSP_REPO}": PREFIX["ctsp"], "${XRSP_REPO}": PREFIX["xrsp"], "${SDET_REPO}": PREFIX["sdet"]}
    missing, n_named = [], 0
    for s in S:
        for c in s["reacquire"]["command"] + s["reacquire"].get("chain", []):
            m = re.search(r'cd "?(\$\{[A-Z_]+\})"?', c)
            cd = roots.get(m.group(1)) if m else None
            for tok in re.findall(r"((?:\$\{[A-Z_]+\}/)?(?:tools|slurm|scripts|src|SchwingNet/slurm|reacquire)/[A-Za-z0-9_./-]+\.(?:py|sh|sbatch))", c):
                base, rel = (roots.get(tok.split("/", 1)[0]), tok.split("/", 1)[1]) if tok.startswith("${") else (cd, tok)
                if base and os.path.isdir(base):
                    n_named += 1
                    if not os.path.exists(os.path.join(base, rel)):
                        missing.append("%s: %s" % (s["id"], tok))
    for md in ("MIGRATION_PLAN.md", "LAYOUT.md", "reacquire/README.md", "db/README.md"):
        txt = open(os.path.join(HERE, md), encoding="utf-8").read()
        for tok in re.findall(r"`((?:tools|slurm)/[A-Za-z0-9_./-]+\.(?:py|sh|sbatch))", txt):
            n_named += 1
            if tok in GRID_ONLY:
                continue
            if not (os.path.exists(os.path.join(REPO, tok)) or os.path.exists(os.path.join(PREFIX["ctsp"], tok))):
                missing.append("%s: %s" % (md, tok))
    check("V6", not missing, "tool paths named %d; missing %s" % (n_named, missing[:8]))
    # V7
    perr = []
    for s in S:
        for c in s["reacquire"]["command"]:
            try:
                shlex.split(c)
            except ValueError as exc:
                perr.append("%s: %s" % (s["id"], exc))
    check("V7", not perr, "commands %d; shlex errors %s" % (sum(len(s["reacquire"]["command"]) for s in S), perr[:3]))
    # V8
    hits = []
    for f in glob.glob(os.path.join(HERE, "**", "*"), recursive=True):
        if os.path.isfile(f) and f.endswith((".md", ".yaml", ".json", ".py", ".sql", ".sh", ".sbatch", ".csv", ".tsv")) and \
                not f.endswith("path_refs_files.csv"):
            if FORBIDDEN in open(f, encoding="utf-8", errors="replace").read().lower():
                hits.append(os.path.relpath(f, HERE))
    check("V8", not hits, "files containing the forbidden word: %s" % hits)
    # V9
    rx = re.compile(r"(?<![A-Za-z0-9_])(ssn|sscn|nnunet|ctsp|vfr|sps|xrsp|sdet|sdr|mem|ostk|scr|dp|cen|census):([A-Za-z0-9_./\-*]+)")
    rx_mem = re.compile(r"MEM/([A-Za-z0-9_.\-]+)")
    rx_bare = re.compile(r"(?<![A-Za-z0-9_/:.~$\-])((?:docs|tools|slurm|SchwingNet)/[A-Za-z0-9_./\-*]+\.(?:md|py|sh|json|csv|tsv|txt|sbatch|bib|yaml))")
    rx_acq = re.compile(r"(?<![A-Za-z0-9_/])acquisition/([A-Za-z0-9_./\-*]+\.(?:md|csv|json|txt|tsv))")
    seen, unresolved = {}, {}
    for m in rx.finditer(man):
        key = (m.group(1), m.group(2).rstrip(".,;:)`'\""))
        if key not in seen:
            seen[key] = resolve_cite(*key)
    for m in rx_mem.finditer(man):
        key = ("mem", m.group(1).rstrip(".,;:)`"))
        if key not in seen:
            seen[key] = resolve_cite(*key)
    for m in rx_bare.finditer(man):
        key = ("ssn", m.group(1).rstrip(".,;:)`"))
        if key not in seen:
            seen[key] = resolve_cite(*key)
    for m in rx_acq.finditer(man):
        key = ("ssn", "SchwingNet/results/transitional_registry/acquisition/" + m.group(1).rstrip(".,;:)`"))
        if key not in seen:
            seen[key] = resolve_cite(*key)
    for k, v in seen.items():
        if v is False:
            unresolved["%s:%s" % k] = None
    # the context of each unresolved citation, so a reader can see whether the card already says it is absent locally
    for u in list(unresolved):
        path = u.split(":", 1)[1]
        i = man.find(path)
        unresolved[u] = re.sub(r"\s+", " ", man[max(0, i - 160):i + len(path) + 120]) if i >= 0 else ""
    checked = sum(1 for v in seen.values() if v is not None)
    unexplained = sorted(u for u in unresolved if u not in KNOWN_UNRESOLVED)
    check("V9", not unexplained, "distinct cited paths checked %d, resolved %d, unresolved %d (all explained: %s); unexplained %s" % (
        checked, checked - len(unresolved), len(unresolved), not unexplained, unexplained[:5]))
    R["V9"]["unresolved"] = dict((u, dict(reason=KNOWN_UNRESOLVED.get(u, "UNEXPLAINED"), context=c)) for u, c in unresolved.items())
    # V10
    empty = []
    for md, names in (("LAYOUT.md", ["layout_map", "ceph_keep"]), ("MIGRATION_PLAN.md", ["batches", "candidates", "path_refs"])):
        txt = open(os.path.join(HERE, md), encoding="utf-8").read()
        for n in names:
            m = re.search(r"<!-- BEGIN GENERATED: %s -->\n(.*?)<!-- END GENERATED: %s -->" % (n, n), txt, re.S)
            if not m or len(m.group(1).strip()) < 50:
                empty.append("%s:%s" % (md, n))
    check("V10", not empty, "generated blocks filled; empty: %s" % empty)
    # V11
    bash = r"C:\Program Files\Git\bin\bash.exe" if os.name == "nt" else "bash"
    serr = []
    shells = glob.glob(os.path.join(HERE, "**", "*.sh"), recursive=True) + glob.glob(os.path.join(HERE, "**", "*.sbatch"), recursive=True)
    for f in shells:
        p = subprocess.run([bash, "-n", f.replace("\\", "/")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode:
            serr.append("%s: %s" % (os.path.relpath(f, HERE), p.stderr.decode(errors="replace")[:200]))
        if b"\r\n" in open(f, "rb").read():
            serr.append("%s: CRLF line endings" % os.path.relpath(f, HERE))
    check("V11", not serr, "shell scripts checked %d; problems %s" % (len(shells), serr))
    # V12
    perr = []
    for f in glob.glob(os.path.join(HERE, "**", "*.py"), recursive=True):
        try:
            ast.parse(open(f, encoding="utf-8").read(), filename=f, feature_version=(3, 6))
        except SyntaxError as exc:
            perr.append("%s: %s" % (os.path.relpath(f, HERE), exc))
    check("V12", not perr, "python files parse as 3.6: %s" % (perr or "all"))
    # V13
    aliases = [a for s in S for a in s.get("aliases") or []]
    check("V13", len(aliases) == len(set(aliases)) and not set(aliases) & set(ids), "aliases %d, unique and distinct from ids" % len(aliases))
    # V14
    plan = json.load(open(os.path.join(HERE, "plan", "plan_summary.json")))["totals"]
    m = re.search(r"moves \*\*(\d+) HOME items, ([0-9.]+) GB", man)
    check("V14", m and int(m.group(1)) == plan["items"] and abs(float(m.group(2)) - plan["gb"]) < 0.05,
          "manifest quotes %s items / %s GB; plan %d / %.1f" % (m.group(1) if m else None, m.group(2) if m else None, plan["items"], plan["gb"]))
    json.dump(R, open(os.path.join(HERE, "verification_report.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    n_fail = sum(1 for v in R.values() if not v["ok"])
    print("VERIFY_PLANNING %s (%d checks, %d failed)" % ("OK" if not n_fail else "FAILED", len(R), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
