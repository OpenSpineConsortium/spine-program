#!/usr/bin/env python3
"""Tests of the planning side of reacquire.py: sources.yaml and sources.json agree, every source has a usable
re-acquisition entry, every command parses, every repository tool a command names exists, the dry run prints every
command, the login-node refusal works, --run writes the state folder, and the helpers verify what they fetch.
No network and no grid: the Zenodo and HTTP helpers are exercised against local stand-ins.

    python3 data_platform/reacquire/test_reacquire.py -v
"""
import hashlib
import io
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager

HERE = os.path.dirname(os.path.abspath(__file__))
DPROOT = os.path.dirname(HERE)
REPO = os.path.dirname(DPROOT)
DESKTOP = os.path.dirname(REPO)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(DPROOT, "lib"))
import reacquire as rq   # noqa: E402
import mini_yaml         # noqa: E402

DOC = rq.load_sources()
FORBIDDEN = "proven" + "ance"        # the word Greg never uses, spelled so that this file does not contain it
USER_VARS = {"PHYSIONET_USER"}       # supplied by the person who runs a credentialed (manual) source
SOURCES = DOC["sources"]


@contextmanager
def captured():
    old = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    try:
        yield buf
    finally:
        sys.stdout = old


def bash():
    for b in ((r"C:\Program Files\Git\bin\bash.exe", "bash") if os.name == "nt" else ("bash",)):
        try:
            subprocess.check_output([b, "-c", "true"], stderr=subprocess.STDOUT)
            return b
        except (OSError, subprocess.CalledProcessError):
            continue
    return None


class Planning(unittest.TestCase):
    def test_yaml_equals_json(self):
        y = mini_yaml.load(open(os.path.join(DPROOT, "sources.yaml"), encoding="utf-8"))
        self.assertEqual(y, DOC)
        try:
            import yaml
        except ImportError:
            return
        self.assertEqual(yaml.safe_load(open(os.path.join(DPROOT, "sources.yaml"), encoding="utf-8")), DOC)

    def test_ids_unique_and_fields_present(self):
        ids = [s["id"] for s in SOURCES]
        self.assertEqual(len(ids), len(set(ids)))
        need = ["name", "citation", "doi_or_url", "modality", "anatomy", "position_view", "licence", "access", "acquired",
                "contents", "locations", "annotation", "derived", "defects", "reacquire", "layout"]
        for s in SOURCES:
            for k in need:
                self.assertIn(k, s, "%s lacks %s" % (s["id"], k))
            for k in ("method", "tool", "args", "date", "date_basis"):
                self.assertIn(k, s["acquired"], s["id"])
            for k in ("subjects", "items", "formats", "bytes", "counts_file"):
                self.assertIn(k, s["contents"], s["id"])
            for k in ("route", "mode", "command", "verify", "gated_steps"):
                self.assertIn(k, s["reacquire"], s["id"])
            for loc in s["locations"]:
                self.assertIn(loc["storage"], ("HOME", "CEPH"))
            self.assertNotIn(FORBIDDEN, json.dumps(s).lower())

    def test_every_source_has_a_route(self):
        for s in SOURCES:
            r = s["reacquire"]
            self.assertIn(r["mode"], ("run", "submit", "manual"), s["id"])
            if r["mode"] in ("run", "submit"):
                self.assertTrue(r["command"], "%s: %s mode without a command" % (s["id"], r["mode"]))
            else:
                self.assertTrue(r["gated_steps"] or r["route"] in ("none",), "%s: manual without steps" % s["id"])

    def test_commands_parse(self):
        env = rq.env_defaults()
        b = bash()
        n = 0
        for s in SOURCES:
            e = rq.source_env(s, env)
            for c in s["reacquire"]["command"]:
                rc = rq.resolve(c, e)
                left = set(re.findall(r"\$\{([A-Z_]+)\}", rc)) - USER_VARS
                self.assertEqual(left, set(), "%s: unresolved variable in %s" % (s["id"], rc))
                shlex.split(rc)              # raises on unbalanced quotes
                if b:
                    p = subprocess.run([b, "-n", "-c", rc], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.assertEqual(p.returncode, 0, "%s: bash -n failed: %s\n%s" % (s["id"], rc, p.stderr.decode(errors="replace")))
                n += 1
        self.assertGreater(n, 80)

    def test_named_tools_exist(self):
        roots = {"${REPO}": REPO, "${DP}": DPROOT, "${CTSP_REPO}": os.path.join(DESKTOP, "CTSpinoPelvic1K-1"),
                 "${XRSP_REPO}": os.path.join(DESKTOP, "XRaySpinoPelvic1K")}
        missing = []
        for s in SOURCES:
            for c in s["reacquire"]["command"] + s["reacquire"].get("chain", []):
                cd = None
                m = re.search(r'cd "?(\$\{[A-Z_]+\})"?', c)
                if m:
                    cd = roots.get(m.group(1))
                for tok in re.findall(r"((?:\$\{[A-Z_]+\}/)?(?:tools|slurm|scripts|SchwingNet/slurm|reacquire)/[A-Za-z0-9_./-]+\.(?:py|sh|sbatch))", c):
                    if tok.startswith("${"):
                        var, rel = tok.split("/", 1)
                        base = roots.get(var)
                    else:
                        base, rel = cd, tok
                    if base is None or not os.path.isdir(base):
                        continue             # a checkout that is not on this machine (VerSeFusion, spine-detector)
                    if not os.path.exists(os.path.join(base, rel)):
                        missing.append("%s: %s" % (s["id"], tok))
        self.assertEqual(missing, [])

    def test_dry_run_prints_every_command(self):
        with captured() as out:
            rc = rq.main(["--all"])
        self.assertEqual(rc, 0)
        printed = [l for l in out.getvalue().splitlines() if l.startswith("  $ ")]
        total = sum(len(s["reacquire"]["command"]) for s in SOURCES)
        self.assertEqual(len(printed), total)
        self.assertEqual(out.getvalue().count("\n=== "), len(SOURCES))

    def test_aliases_resolve(self):
        with captured() as out:
            rc = rq.main(["ctpelvic1k_clinic", "xrsp1k_drr"])
        self.assertEqual(rc, 0)
        self.assertIn("=== ctpelvic1k ", out.getvalue())
        self.assertIn("=== xrspinopelvic1k ", out.getvalue())

    def test_unknown_id(self):
        with captured():
            self.assertEqual(rq.main(["no_such_source"]), 2)


class Running(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="dp_reacq_")
        self.old_env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.old_env)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_login_node_refusal(self):
        real = rq.socket.gethostname
        rq.socket.gethostname = lambda: "warrior2.grid.wayne.edu"
        try:
            with captured() as out:
                rc = rq.main(["--run", "carmlspine"])
        finally:
            rq.socket.gethostname = real
        self.assertEqual(rc, 3)
        self.assertIn("reacquire.sbatch", out.getvalue())
        self.assertIn("sbatch -D", out.getvalue())

    def test_refuses_outside_slurm(self):
        os.environ.pop("SLURM_JOB_ID", None)
        with captured() as out:
            rc = rq.main(["--run", "carmlspine"])
        self.assertEqual(rc, 3)
        self.assertIn("sbatch", out.getvalue())

    def test_run_writes_state(self):
        if not bash():
            self.skipTest("no bash")
        doc = dict(meta={}, sources=[dict(id="toy", name="toy source", kind="upstream_release", status="on_disk", access="open",
                                           layout=dict(folder="toy", subpath=""),
                                           reacquire=dict(route="http", mode="run", py_env="vfr",
                                                          command=['mkdir -p "${DEST}" && printf abc > "${DEST}/a.txt"'],
                                                          verify=[dict(type="count", path="${DEST}", glob="*.txt", expect=1),
                                                                  dict(type="md5", path="${DEST}/a.txt", expect=hashlib.md5(b"abc").hexdigest()),
                                                                  dict(type="note", text="look at it")],
                                                          gated_steps=[]))])
        sp = os.path.join(self.tmp, "sources.json")
        json.dump(doc, open(sp, "w"))
        os.environ["BASH_BIN"] = bash()
        os.environ["RS"] = os.path.join(self.tmp, "rs").replace("\\", "/")
        os.environ["DATA"] = os.environ["RS"] + "/data"
        with captured() as out:
            rc = rq.main(["--run", "--outside-slurm", "--sources", sp, "toy"])
        self.assertEqual(rc, 0, out.getvalue())
        st = os.path.join(os.environ["DATA"], "toy", "meta", "reacquire", "toy")
        status = json.load(open(os.path.join(st, "REACQUIRE_STATUS.json")))
        self.assertEqual(status["status"], "verified_with_manual_checks")
        lines = [json.loads(l) for l in open(os.path.join(st, "verified.jsonl"))]
        self.assertEqual([l["unit"].split(":")[0] for l in lines], ["cmd", "check", "check"])
        self.assertTrue(os.path.exists(os.path.join(st, "commands.sh")))
        # --verify alone re-runs the checks
        with captured():
            self.assertEqual(rq.main(["--verify", "--outside-slurm", "--sources", sp, "toy"]), 0)

    def test_manual_source_runs_nothing(self):
        os.environ["SLURM_JOB_ID"] = "1"
        st = os.path.join(self.tmp, "state")
        with captured() as out:
            rc = rq.main(["--run", "--state-root", st, "stanford_aimi_merlin"])
        self.assertEqual(rc, 0)
        status = json.load(open(os.path.join(st, "stanford_aimi_merlin", "REACQUIRE_STATUS.json")))
        self.assertEqual(status["status"], "manual_required")
        self.assertTrue(status["gated_steps"])

    def test_http_get_file_url(self):
        src = os.path.join(self.tmp, "blob.bin")
        open(src, "wb").write(b"hello world")
        url = "file:///" + src.replace("\\", "/").lstrip("/")
        dst = os.path.join(self.tmp, "out", "blob.bin")
        with captured():
            rc = rq.main(["http-get", "--outside-slurm", "--url", url, "--dest", dst, "--md5", hashlib.md5(b"hello world").hexdigest(), "--bytes", "11"])
        self.assertEqual(rc, 0)
        self.assertEqual(open(dst, "rb").read(), b"hello world")
        with captured():
            rc = rq.main(["http-get", "--outside-slurm", "--url", url, "--dest", dst + ".2", "--md5", "0" * 32])
        self.assertEqual(rc, 1)
        self.assertFalse(os.path.exists(dst + ".2"), "a download that fails its md5 must not appear at the destination")

    def test_helpers_refuse_outside_a_job(self):
        os.environ.pop("SLURM_JOB_ID", None)
        with captured() as out:
            rc = rq.main(["http-get", "--url", "file:///x", "--dest", os.path.join(self.tmp, "x")])
        self.assertEqual(rc, 3)
        self.assertIn("refusing", out.getvalue())
        real = rq.socket.gethostname
        rq.socket.gethostname = lambda: "warrior.grid.wayne.edu"
        os.environ["SLURM_JOB_ID"] = "5"
        try:
            with captured() as out:
                rc = rq.main(["zenodo-get", "--record", "1", "--dest", self.tmp])
        finally:
            rq.socket.gethostname = real
        self.assertEqual(rc, 3)
        self.assertIn("login node", out.getvalue())

    def test_bad_download_never_replaces_a_good_copy(self):
        good = os.path.join(self.tmp, "good.bin")
        open(good, "wb").write(b"GOOD")
        other = os.path.join(self.tmp, "other.bin")
        open(other, "wb").write(b"EVIL")
        url = "file:///" + other.replace("\\", "/").lstrip("/")
        with captured():
            rc = rq.main(["http-get", "--outside-slurm", "--url", url, "--dest", good, "--md5", hashlib.md5(b"GOOD").hexdigest()])
        self.assertEqual(rc, 0, "an existing copy that verifies is kept without fetching")
        self.assertEqual(open(good, "rb").read(), b"GOOD")
        open(good, "wb").write(b"GOOX")              # now the copy is damaged and the server serves the wrong bytes
        with captured():
            rc = rq.main(["http-get", "--outside-slurm", "--url", url, "--dest", good, "--md5", hashlib.md5(b"GOOD").hexdigest()])
        self.assertEqual(rc, 1)
        self.assertEqual(open(good, "rb").read(), b"GOOX", "the failed download must not overwrite the destination")
        self.assertTrue(os.path.exists(good + ".bad"))

    def test_complete_part_is_finished_without_the_network(self):
        dst = os.path.join(self.tmp, "big.bin")
        open(dst + ".part", "wb").write(b"0123456789")
        got = rq.download("http://unreachable.invalid/big.bin", dst, size=10, check=rq._hash_check(md5=hashlib.md5(b"0123456789").hexdigest()))
        self.assertEqual(got, 10)
        self.assertEqual(open(dst, "rb").read(), b"0123456789")

    def test_new_check_types(self):
        env = dict(rq.env_defaults(), DEST=self.tmp, STATE=self.tmp, PY="python3")
        vj = os.path.join(self.tmp, "verified.jsonl")
        with open(vj, "w") as fh:
            for u, c in (("1.1", "a"), ("1.2", "a"), ("1.2", "a"), ("2.1", "b")):
                fh.write(json.dumps(dict(unit=u, coll=c)) + "\n")
        self.assertEqual(rq.run_check(dict(type="jsonl_count", path=vj, field="coll", value="a", expect=2), env)["ok"], True)
        self.assertEqual(rq.run_check(dict(type="jsonl_count", path=vj, expect=3), env)["ok"], True)
        import tarfile
        arc = os.path.join(self.tmp, "arcs")
        os.makedirs(arc)
        payload = os.path.join(self.tmp, "m.txt")
        open(payload, "w").write("member")
        with tarfile.open(os.path.join(arc, "a.tar.gz"), "w:gz") as tf:
            tf.add(payload, arcname="m.txt")
        self.assertEqual(rq.run_check(dict(type="archive_ok", path=arc, glob="*.tar.gz", expect=1), env)["ok"], True)
        open(os.path.join(arc, "b.tar.gz"), "wb").write(open(os.path.join(arc, "a.tar.gz"), "rb").read()[:20])
        self.assertEqual(rq.run_check(dict(type="archive_ok", path=arc, glob="*.tar.gz", expect=2), env)["ok"], False)
        d = os.path.join(self.tmp, "imgs")
        os.makedirs(d)
        open(os.path.join(d, "real.jpg"), "wb").write(b"x" * 2048)
        open(os.path.join(d, "stub.jpg"), "wb").write(b"version https://git-lfs.github.com/spec/v1\n")
        self.assertEqual(rq.run_check(dict(type="count", path=d, glob="*.jpg", min_bytes=1024, expect=1), env)["ok"], True)

    def test_nifti_check_catches_a_truncated_gzip(self):
        import gzip
        ct, lab = os.path.join(self.tmp, "ct"), os.path.join(self.tmp, "labels")
        os.makedirs(ct)
        os.makedirs(lab)
        blob = gzip.compress(os.urandom(4096))
        open(os.path.join(ct, "0001_ct.nii.gz"), "wb").write(blob)
        open(os.path.join(ct, "0002_ct.nii.gz"), "wb").write(blob[: len(blob) // 2])
        for c in ("0001", "0002"):
            open(os.path.join(lab, c + "_label.nii.gz"), "wb").write(blob)
        out = os.path.join(self.tmp, "nc.json")
        import builtins
        real_import = builtins.__import__

        def no_nib(name, *a, **k):                 # gzip-only path: a random blob is not a NIfTI
            if name in ("nibabel",):
                raise ImportError(name)
            return real_import(name, *a, **k)
        builtins.__import__ = no_nib
        try:
            with captured():
                rc = rq.main(["nifti-check", "--outside-slurm", "--ct-dir", ct, "--label-dir", lab, "--out", out])
        finally:
            builtins.__import__ = real_import
        rep = json.load(open(out))
        self.assertEqual(rc, 1)
        self.assertEqual((rep["n_checked"], rep["n_bad"], rep["bad"]), (2, 1, ["0002"]))

    def test_submit_command_not_repeated_on_requeue(self):
        if not bash():
            self.skipTest("no bash")
        marker = os.path.join(self.tmp, "submissions.txt").replace("\\", "/")
        doc = dict(meta={}, sources=[dict(id="toy_submit", name="toy", kind="derived", status="on_disk", access="open",
                                           layout=dict(folder="toy", subpath=""),
                                           reacquire=dict(route="rebuild", mode="submit", py_env="vfr",
                                                          command=['echo submitted >> "%s"' % marker], verify=[], gated_steps=[]))])
        sp = os.path.join(self.tmp, "sources.json")
        json.dump(doc, open(sp, "w"))
        os.environ.update(BASH_BIN=bash(), SLURM_JOB_ID="777", RS=os.path.join(self.tmp, "rs").replace("\\", "/"))
        os.environ["DATA"] = os.environ["RS"] + "/data"
        for _ in range(2):                           # the second call is the requeued job (same SLURM_JOB_ID)
            with captured():
                self.assertEqual(rq.main(["--run", "--sources", sp, "toy_submit"]), 0)
        self.assertEqual(open(marker).read().count("submitted"), 1)
        os.environ["SLURM_JOB_ID"] = "778"            # a new job submits again
        with captured():
            rq.main(["--run", "--sources", sp, "toy_submit"])
        self.assertEqual(open(marker).read().count("submitted"), 2)

    def test_overlapping_sources_refused(self):
        mk = lambda i: dict(id=i, name=i, kind="upstream_release", status="on_disk", access="open", layout=dict(folder="idc"),
                            reacquire=dict(route="idc", mode="submit", command=["sbatch acquisition_fetch.sh idc --collection idc --manifest x.csv"],
                                           verify=[], gated_steps=[]))
        sp = os.path.join(self.tmp, "sources.json")
        json.dump(dict(meta={}, sources=[mk("a"), mk("b")]), open(sp, "w"))
        with captured() as out:
            rc = rq.main(["--sources", sp, "a", "b"])
        self.assertEqual(rc, 2)
        self.assertIn("--collection idc", out.getvalue())


    def test_zenodo_get_with_stand_in(self):
        payload = {"a_ct_scan.zip": b"AAAA", "readme.txt": b"r"}
        meta = {"files": [{"key": k, "size": len(v), "checksum": "md5:" + hashlib.md5(v).hexdigest(),
                           "links": {"self": "https://zenodo.org/api/records/1/files/%s/content" % k}} for k, v in payload.items()]}

        class R(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        opener = lambda url, *a, **k: R(json.dumps(meta).encode())

        def fetch(url, dst, size):
            key = url.split("/files/")[1].split("/")[0]
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, "wb").write(payload[key])
            return size

        dest = os.path.join(self.tmp, "z")
        with captured():
            rc = rq.cmd_zenodo_get(["--record", "1", "--dest", dest, "--include", r"_ct_.*\.zip$"], opener=opener, fetch=fetch)
        self.assertEqual(rc, 0)
        rep = json.load(open(os.path.join(dest, ".reacquire_state", "zenodo_1.json")))
        self.assertTrue(rep["all_verified"])
        self.assertEqual(rep["n_files"], 1)
        # a corrupted payload fails the md5
        payload["a_ct_scan.zip"] = b"AAAB"
        os.remove(os.path.join(dest, "a_ct_scan.zip"))
        open(os.path.join(dest, ".reacquire_state", "verified.jsonl"), "w").close()
        with captured():
            rc = rq.cmd_zenodo_get(["--record", "1", "--dest", dest, "--include", r"_ct_"], opener=opener, fetch=fetch)
        self.assertEqual(rc, 1)

    def test_list_sha256_matches_data_manifest(self):
        root = os.path.join(self.tmp, "tree")
        for p, b in (("a/x.bin", b"1"), ("a/b/y.bin", b"22"), ("z.txt", b"333")):
            os.makedirs(os.path.dirname(os.path.join(root, p)), exist_ok=True)
            open(os.path.join(root, p), "wb").write(b)
        sys.path.insert(0, os.path.join(REPO, "tools"))
        import data_manifest
        want = data_manifest.walk(root)
        got, n, b = rq.list_sha256(root)
        self.assertEqual((got, n, b), (want["list_sha256"], want["files"], want["bytes"]))


class Recipes(unittest.TestCase):
    """The recipes the 2026-10-08 verifiers found broken stay fixed."""

    def test_derived_dest_is_the_layout_path(self):
        e = rq.source_env(dict(id="verse_drr", layout=dict(folder="versefusion", subpath="derived/verse_drr")), rq.env_defaults())
        self.assertTrue(e["DEST"].endswith("/versefusion/derived/verse_drr"), e["DEST"])
        e = rq.source_env(dict(id="x", layout=dict(folder="multisource_banks", subpath="derived/implant_*")), rq.env_defaults())
        self.assertTrue(e["DEST"].endswith("/multisource_banks/derived"), e["DEST"])

    def test_no_recipe_writes_to_home(self):
        allowed = ("${HOME}/mambaforge/", "${HOME}/model_night/ts_clean_subjects.txt")
        bad = []
        for s in SOURCES:
            r = s["reacquire"]
            for c in r["command"] + [json.dumps(v) for v in r["verify"] if v.get("type") != "note"]:
                for m in re.finditer(r"\$\{HOME\}/[^\s\"']*", c):
                    if not m.group(0).startswith(allowed):
                        bad.append("%s: %s" % (s["id"], m.group(0)))
                if re.search(r"\$\{(CTSP|VFR|XRSP|SDET)_REPO\}/data\b", c):
                    bad.append("%s: repository data/ path in %s" % (s["id"], c[:80]))
        self.assertEqual(bad, [])

    def test_family_b_creates_logs_and_reads_repo_manifests(self):
        for s in SOURCES:
            for c in s["reacquire"]["command"]:
                if "sbatch -D $D" in c:
                    self.assertIn("mkdir -p $D/logs", c.split("sbatch -D $D")[0], s["id"])
                for m in re.findall(r"\$\{REPO\}/(SchwingNet/results/transitional_registry/acquisition/manifests/[A-Za-z0-9_]+\.csv)", c):
                    self.assertTrue(os.path.exists(os.path.join(REPO, m)), m)

    def test_idc_collections_are_covered_by_the_pooled_fetch(self):
        cov = [s for s in SOURCES if s["reacquire"].get("covered_by") == "idc_tier1"]
        self.assertEqual(len(cov), 39)
        self.assertTrue(all(s["reacquire"]["mode"] == "manual" for s in cov))
        self.assertEqual(sum(v["expect"] for s in cov for v in s["reacquire"]["verify"] if v["type"] == "jsonl_count"), 3600)
        runnable = [s["id"] for s in SOURCES if s["reacquire"]["mode"] in ("run", "submit")]
        self.assertEqual(rq.overlapping([s for s in SOURCES if s["id"] in runnable]), [])

    def test_gpu_scripts_not_forced_onto_reqp(self):
        for s in SOURCES:
            for c in s["reacquire"]["command"]:
                for script in ("lstv_flag_render.sh", "fluorocap_v2.sh", "carmlspine_finetune.sh"):
                    self.assertFalse(script in c and "reqp" in c, "%s: %s" % (s["id"], c))

    def test_dry_run_prints_check_fields_and_the_all_spec(self):
        with captured() as out:
            rq.main(["--grid", "--all", "--modes", "run"])
        txt = out.getvalue()
        self.assertIn('field="all_verified"', txt)
        self.assertIn('IDS="--all --modes run"', txt)
        self.assertIn("/wsu/home/go/go24/go2432/", txt)
        self.assertIn("mkdir -p logs && sbatch", txt)


if __name__ == "__main__":
    unittest.main()
