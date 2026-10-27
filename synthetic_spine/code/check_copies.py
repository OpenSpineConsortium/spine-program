"""The copied tables are the bytes they came from, and their generators still write them.

    python3 code/check_copies.py                       # from synthetic_spine/; standard library only, no network
    python3 code/check_copies.py --against ../../CTSpinoPelvic1K   # also ask that clone for each recorded blob

data/COPIED_FROM.csv names, for every copied file, the repository, commit and path it was copied from, its git blob
id and its SHA-256. This checks:
1. every file's bytes have the recorded SHA-256 and git blob id, and data/SHA256SUMS (for `sha256sum -c`) agrees;
2. the files copied from this repository (06's whole-spine Panjabi table and its builder) are byte-identical to
   06's own copies, so a later change to one without the other fails here;
3. with --against <path to a CTSpinoPelvic1K clone>, `git rev-parse <commit>:<path>` in that clone gives the
   recorded blob id for every file copied from it, which proves the bytes are the ones committed there;
4. data/make_reference_table.py, run in a temporary folder, writes level_references.csv identical to data/'s, and
   data/build_panjabi.py writes panjabi_full_spine.csv identical to data/'s and passes its own check. Line endings
   aside: Python's csv writer ends rows with CRLF on every platform; the committed files have LF.
Exit 1 on any difference, naming it.
"""
import csv
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
REPO = HERE.parent


def blob_id(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main(argv):
    against = Path(argv[argv.index("--against") + 1]) if "--against" in argv else None
    problems = []
    record = list(csv.DictReader((DATA / "COPIED_FROM.csv").read_text(encoding="ascii").splitlines()))
    sums = dict(reversed(l.split("  ", 1)) for l in (DATA / "SHA256SUMS").read_text(encoding="ascii").splitlines())
    if set(sums) != {r["file"] for r in record}:
        problems.append("data/SHA256SUMS and data/COPIED_FROM.csv list different files")
    for r in record:
        data = (DATA / r["file"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != r["sha256"] or sums.get(r["file"]) != r["sha256"]:
            problems.append(f"data/{r['file']}: SHA-256 {hashlib.sha256(data).hexdigest()}, recorded {r['sha256']}")
        if blob_id(data) != r["git_blob"]:
            problems.append(f"data/{r['file']}: git blob {blob_id(data)}, recorded {r['git_blob']}")
        if r["repository"].startswith("spine-program"):
            # git stores both with LF; only synthetic_spine/ is pinned to LF on checkout, so a Windows clone with
            # core.autocrlf may hold 06's copy with CRLF
            own = REPO / r["path"]
            if not own.exists() or own.read_bytes().replace(b"\r\n", b"\n") != data:
                problems.append(f"data/{r['file']} is not byte-identical to {r['path']}")
        elif against is not None:
            run = subprocess.run(["git", "-C", str(against), "rev-parse", f"{r['commit']}:{r['path']}"],
                                 capture_output=True, text=True)
            if run.returncode != 0 or run.stdout.strip() != r["git_blob"]:
                problems.append(f"{against}: {r['commit'][:12]}:{r['path']} is {run.stdout.strip() or run.stderr.strip()}, "
                                f"recorded {r['git_blob']}")
    for script, output in (("make_reference_table.py", "level_references.csv"), ("build_panjabi.py", "panjabi_full_spine.csv")):
        with tempfile.TemporaryDirectory() as tmp:
            shutil.copy(DATA / script, tmp)
            run = subprocess.run([sys.executable, script], cwd=tmp, capture_output=True, text=True)
            if run.returncode != 0:
                problems.append(f"data/{script} exited {run.returncode}: {run.stdout[-300:]} {run.stderr[-300:]}")
                continue
            built = (Path(tmp) / output).read_bytes().replace(b"\r\n", b"\n")
            if built != (DATA / output).read_bytes().replace(b"\r\n", b"\n"):
                problems.append(f"data/{script} no longer writes data/{output} as committed")
    for p in problems:
        print(p)
    checked = "copies intact" + (", their blobs found in " + str(against) if against else "")
    print(checked + "; both generators reproduce their tables" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
