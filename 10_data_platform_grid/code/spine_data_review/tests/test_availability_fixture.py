"""Fixture tests for sdr/availability.py: hand-calculated expectations for the pure functions, a local
HTTP server that exercises probe_fetch (64 KiB cap, redirect chains, login detection), a stubbed
GitHub pair that reproduces the README-link recursion offline, and a check that the module's regexes
are the ones printed in PROTOCOL.md section 10.

Run from spine_data_review/ (WSL): ~/sdr_venv/bin/python tests/test_availability_fixture.py
Writes only under tests/run_fixture/. Lines starting PASS/FAIL are expectations of the protocol;
lines starting BUG are confirmed defects (they do not fail the harness, they are the findings).
Exit status 1 when any PASS-expectation fails.
"""
from __future__ import annotations

import base64
import json
import re
import shutil
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sdr import availability as av  # noqa: E402
from sdr.common import Resp, init_run_dir  # noqa: E402

RESULTS = {"pass": 0, "fail": 0, "bug": 0}


def check(cond: bool, label: str, detail: str = "") -> None:
    RESULTS["pass" if cond else "fail"] += 1
    print(f"{'PASS' if cond else 'FAIL'}: {label}" + (f"  [{detail}]" if detail and not cond else ""))


def bug(cond: bool, label: str, detail: str = "") -> None:
    """cond=True means the defect reproduced."""
    if cond:
        RESULTS["bug"] += 1
    print(f"{'BUG CONFIRMED' if cond else 'BUG NOT REPRODUCED'}: {label}" + (f"  [{detail}]" if detail else ""))


def P(cls, rule, date="2026-09-19"):
    return {"classification_machine": cls, "rule": rule, "date": date}


# ----------------------------------------------------------------------------- A. pure functions
def part_a() -> None:
    print("\n== A. pure functions, hand-calculated ==")
    ag = av.agreement
    check(ag([])["status"] == "not-probed", "agreement: no probes -> not-probed")
    check(ag([P("open-download", "P1")])["status"] == "one-probe", "agreement: one probe -> one-probe")
    r = ag([P("open-download", "P1"), P("open-download", "P1", "2026-09-21")])
    check(r == {"status": "agreed", "route": "open-download", "rule": "P1", "dates": ["2026-09-19", "2026-09-21"]}, "agreement: two agreeing -> agreed P1", str(r))
    r = ag([P("open-download", "P15"), P("open-download", "P20", "2026-09-21")])
    check(r["rule"] == "P15/P20" and r["route"] == "open-download", "agreement: same class, different rules -> P15/P20", str(r))
    r = ag([P("open-download", "P1"), P("unavailable", "P23", "2026-09-21")])
    check(r["status"] == "needs-third-probe", "agreement: two disagreeing -> needs-third-probe", str(r))
    r = ag([P("open-download", "P1"), P("unavailable", "P23", "2026-09-21"), P("open-download", "P1", "2026-09-23")])
    check(r["status"] == "agreed" and r["dates"] == ["2026-09-19", "2026-09-23"], "agreement: third probe pairs with the first", str(r))
    r = ag([P("unresolved", "P21"), P("unresolved", "P21", "2026-09-21")])
    check(r["status"] == "verifier" and r["route"] is None, "agreement: agreed non-route class -> verifier", str(r))
    r = ag([P("a", "P1"), P("b", "P2", "2026-09-21"), P("c", "P3", "2026-09-23")])
    check(r["status"] == "verifier", "agreement: three different -> verifier", str(r))

    # Summary aggregation as main() does it, on the review run's rows: hand count = registration 3; P12 2, P14 1.
    jl = ROOT / "runs" / "review_availability" / "probes" / "2026-09-19.jsonl"
    if jl.exists():
        rows = [json.loads(l) for l in jl.read_text(encoding="utf-8").splitlines() if l.strip()]
        by_class, by_rule = {}, {}
        for x in rows:
            by_class[x["probe"]["classification_machine"]] = by_class.get(x["probe"]["classification_machine"], 0) + 1
            by_rule[x["probe"]["rule"]] = by_rule.get(x["probe"]["rule"], 0) + 1
        s = json.loads((jl.parent / "summary.json").read_text(encoding="utf-8"))
        check(s["by_class"] == by_class and s["by_rule"] == by_rule and s["n_datasets"] == len(rows),
              "summary.json counts equal a hand count over probes/<date>.jsonl", f"{s['by_class']} {by_class}")
        check(by_class == {"registration": 3} and by_rule == {"P12": 2, "P14": 1}, "review run: registration 3, P12 2, P14 1", str((by_class, by_rule)))

    tr = av.text_rule
    check(tr("Users must sign the data use agreement before download.")[0] == "P16", "P16 DUA text")
    check(tr("Pricing: purchase the data here.")[0] == "P17", "P17 pay text near 'data'")
    check(tr("You can purchase our merchandise in the shop.") is None, "P17 needs NEAR_RE within 200 chars (none here)")
    check(tr("Create a free account to download the images.")[0] == "P18", "P18 register text near 'download'")
    check(tr("Images are available on request from the authors.")[0] == "P19", "P19 request text")
    check(tr("Log in  Sign in  About us") is None, "bare 'Log in'/'Sign in' never classifies")
    check(tr("data use agreement; also purchase data")[0] == "P16", "P16 precedes P17 when both match")
    far = "purchase " + "x" * 250 + " download"
    nearer = "purchase " + "x" * 150 + " download"
    check(av.near(av.PAY_RE, far) is None and av.near(av.PAY_RE, nearer) == "purchase", "near(): 200-character window")
    vt = av.visible_text("<html><nav>Log in to download</nav><body><p>Hello &amp; welcome</p><script>x=1</script><footer>Pricing</footer></body></html>")
    check(vt == "Hello & welcome", "visible_text strips nav/script/footer and decodes entities", repr(vt))
    check(av._len({"content-range": "bytes 0-65535/883912953"}) == 883912953, "_len from Content-Range total")
    check(av._len({"content-length": "123"}) == 123 and av._len({}) is None, "_len from Content-Length / none")
    ht = av.host_type
    check(ht("https://zenodo.org/records/1") == "repository-api", "host_type zenodo")
    check(ht("https://www.kaggle.com/competitions/x") == "challenge-platform", "host_type kaggle competition")
    check(ht("https://www.kaggle.com/datasets/x/y") == "repository-api", "host_type kaggle dataset")
    check(ht("https://drive.google.com/x") == "personal-or-cloud-drive", "host_type google drive")
    check(ht("https://services.informatics.buu.ac.th/spine/") == "institutional", "host_type .ac.th")
    check(ht("https://example.com/x") == "unknown", "host_type unknown")
    check(ht("https://doi.org/10.5281/zenodo.1") == "repository-api", "host_type DOI prefix 10.5281")
    check(av.doi_in("https://doi.org/10.7937/tcia.2019.tt7f4v7o") == "10.7937/tcia.2019.tt7f4v7o", "doi_in doi.org")
    check(av.doi_in("https://zenodo.org/doi/10.5281/zenodo.22139642") == "10.5281/zenodo.22139642", "doi_in zenodo /doi/")
    check(av.doi_in("https://zenodo.org/records/1") is None, "doi_in plain record -> None")
    check(av.route_for("https://github.com/a/b", "10.5281/zenodo.1") == "zenodo", "route_for: DOI prefix precedes host")
    check(av.route_for("https://example.org/x", "10.1016/j.x") == "generic", "route_for: paper DOI does not route")
    an = av.anchors('<a href="data/x.zip">a</a> <a href="f.nii.gz?dl=1">b</a> <a href="paper.pdf">c</a>', "https://h.org/d/")
    check(an == ["https://h.org/d/data/x.zip", "https://h.org/d/f.nii.gz?dl=1"], "anchors(): data extensions only, joined to base", str(an))

    # Regexes must be the protocol's (section 10 fenced block).
    proto = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
    sec = proto[proto.index("## 10. Availability probe"):proto.index("## 11.")]
    for name in ("DUA_RE", "REG_RE", "REQ_RE", "PAY_RE", "NEAR_RE"):
        m = re.search(rf'^{name} = r"(.*)"', sec, re.M)
        check(bool(m) and getattr(av, name).pattern == m.group(1), f"{name} identical to PROTOCOL.md")
    check(all(getattr(av, n).flags & re.I for n in ("DUA_RE", "REG_RE", "REQ_RE", "PAY_RE")),
          "module applies re.I (case-insensitive) to text rules; PROTOCOL.md does not state a flag -> document as a deviation")
    check(set(av.ALLOW_CT) == {"application/zip", "application/gzip", "application/x-gzip", "application/x-tar",
                                "application/x-7z-compressed", "application/dicom", "application/octet-stream"}, "P15 allow-list")


# ----------------------------------------------------------------------------- B. classify_generic on envelopes
def env(status, ct=None, body="", final="https://h.org/p", chain=None, length=None, disp=None, error=None, attempts=1):
    h = {}
    if ct:
        h["content-type"] = ct
    if length is not None:
        h["content-length"] = str(length)
    if disp:
        h["content-disposition"] = disp
    return {"status": status, "headers": h, "body": body, "final_url": final, "chain": chain or [status], "sha1": "0" * 40, "error": error, "attempts": attempts}


def part_b(ctx) -> None:
    print("\n== B. classify_generic on synthetic envelopes ==")
    cg = lambda e, m="GET-range": av.classify_generic(ctx, "https://h.org/p", e, m)
    check(cg(env(404))["rule"] == "P23", "404 -> P23")
    check(cg(env(0, error="ConnectionError: x", attempts=3))["rule"] == "P23", "transport error -> P23")
    check(cg(env(200, "application/zip", length=2 << 20), "HEAD")["rule"] == "P15", "zip 2 MiB -> P15")
    check(cg(env(200, "application/zip", length=100_000), "HEAD")["rule"] == "P21", "zip 100 KB -> not P15 (P21)")
    check(cg(env(200, "application/pdf", length=5 << 20), "HEAD")["rule"] == "P21", "PDF never P15")
    check(cg(env(200, "image/png", length=5 << 20, final="https://h.org/a.png"))["rule"] == "P15", "image/* with data ext -> P15")
    check(cg(env(200, "image/png", length=5 << 20, final="https://h.org/a"))["rule"] == "P21", "image/* without data ext -> not P15")
    check(cg(env(200, "text/html", disp="attachment; filename=x.bin", length=5 << 20))["rule"] == "P15", "Content-Disposition attachment -> P15")
    check(cg(env(200, "text/html", body="<p>please sign the data use agreement</p>"))["rule"] == "P16", "200 html DUA -> P16")
    check(cg(env(403, "text/html", body="<p>forbidden</p>"))["rule"] == "P22", "403 -> P22")
    check(cg(env(302, "text/html", chain=[302] * 6))["rule"] == "P21", "six redirects (chain unresolved) -> P21")
    check(cg(env(500, "text/html", body="<p>error</p>", attempts=3))["rule"] == "P21", "persistent 500 -> P21 unresolved")
    check(cg(env(200, "application/json", body='{"a":1}'))["rule"] == "P21", "200 JSON -> P21")
    check(cg(env(200, "text/html", body="<nav>Log in to download</nav><p>dataset</p>"))["rule"] == "P21", "REG_RE inside <nav> only -> P21")
    e = cg(env(200, "text/html", body="<p>x</p>", chain=[302, 200], final="https://h.org/login?next=/d"))
    check(e["rule"] == "P22" and e["classification_machine"] == "auth-required", "redirect chain ending at /login -> P22")
    # Deviation: text rules run on a 403 body before P22
    e = cg(env(403, "text/html", body="<p>apply for access</p>"))
    bug(e["rule"] == "P16", "P16-P19 fire on a 403 body (protocol: P16-P19 are for 200 HTML; 403 is P22)", e["rule"])
    # The `auth` alternative of LOGIN_RE matches 'author'
    e = cg(env(200, "text/html", body="<p>please sign the data use agreement</p>", final="https://h.org/authors-dataset/"))
    bug(e["rule"] == "P22", "LOGIN_RE 'auth' matches 'authors' in a 200 landing path -> P22 instead of P16/P20", e["rule"])
    # P20 precedes P16 (stub the anchor fetch)
    orig = av.probe_fetch
    av.probe_fetch = lambda c, s, u, m="GET": {"status": 200, "headers": {"content-type": "application/zip"}, "body": "", "final_url": u, "chain": [200], "sha1": "1" * 40, "error": None, "attempts": 1}
    try:
        e = cg(env(200, "text/html", body='<a href="d.zip">zip</a> <p>data use agreement</p>'))
        check(e["rule"] == "P20", "anchor answering 200 -> P20 before P16", e["rule"])
    finally:
        av.probe_fetch = orig
    # entry() shape against the schema's probe definition
    S = json.loads((ROOT / "charting_schema.json").read_text(encoding="utf-8"))["definitions"]["probe"]
    e = cg(env(200, "text/html", body="<p>x</p>"))
    check(set(e) == set(S["required"]), "entry() keys == schema required keys", str(set(e) ^ set(S["required"])))
    check(e["classification_machine"] in S["properties"]["classification_machine"]["enum"] and re.fullmatch(S["properties"]["rule"]["pattern"], e["rule"]) is not None, "entry() enum/pattern")
    # attempts is hard-coded to 1 in api_entry
    r = Resp(503, "", {}, "2" * 40, False, 10, None)
    check(av.api_entry(ctx, "https://api", r, "unresolved", "P21", "x")["attempts"] == 1, "api_entry attempts field is always 1 (RateLimitedSession may have made 3) -> minor")


# ----------------------------------------------------------------------------- C. local server, real probe_fetch
class H(BaseHTTPRequestHandler):
    sent: dict = {}
    ranges: dict = {}
    lock = threading.Lock()
    BIG = 200 << 20  # 200 MiB streamed; a client that reads everything would take noticeably long

    def log_message(self, *a):
        pass

    def _count(self, n):
        with self.lock:
            self.sent[self.path] = self.sent.get(self.path, 0) + n

    def _stream(self, ct, total, chunk=b"<p>" + b"x" * 65533):
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(total))
        self.end_headers()
        try:
            done = 0
            while done < total:
                self.wfile.write(chunk)
                self.wfile.flush()
                done += len(chunk)
                self._count(len(chunk))
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass

    def do_HEAD(self):
        self.ranges[self.path] = self.headers.get("Range")
        if self.path == "/data.bin":
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(self.BIG))
            self.end_headers()
        else:
            self.send_response(405)
            self.end_headers()

    def do_GET(self):
        self.ranges[self.path] = self.headers.get("Range")
        if self.path == "/big.html":
            return self._stream("text/html; charset=utf-8", self.BIG)
        if self.path == "/data.bin":
            return self._stream("application/octet-stream", self.BIG, b"\0" * 65536)
        if self.path == "/redir":
            self.send_response(302)
            self.send_header("Location", "/login?next=/redir")
            self.end_headers()
            return
        if self.path == "/loop":
            self.send_response(302)
            self.send_header("Location", "/loop")
            self.end_headers()
            return
        body = {"/login?next=/redir": b"<form>Username Password</form>",
                "/authors-dataset/": b'<html><body><p>Lumbar spine CT dataset</p><a href="/data.bin">download data.bin</a></body></html>',
                "/dua.html": b"<html><nav>Log in</nav><body><p>To obtain the images you must sign the data use agreement.</p></body></html>",
                "/navonly.html": b"<html><nav>Log in to download</nav><body><p>A spine dataset page.</p></body></html>"}.get(self.path)
        if body is None:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def part_c(ctx) -> None:
    print("\n== C. local HTTP server through probe_fetch / probe_generic ==")
    srv = ThreadingHTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"
    try:
        t0 = time.monotonic()
        e = av.probe_fetch(ctx, "probe", base + "/big.html", "GET")
        dt = time.monotonic() - t0
        check(e["status"] == 200 and len(e["body"].encode()) <= 65536, "GET-range on a 200 MiB HTML page keeps <= 64 KiB body", str(len(e["body"])))
        check(H.sent.get("/big.html", 0) < 16 << 20 and dt < 20, "server wrote far less than 200 MiB before the client hung up", f"{H.sent.get('/big.html')} bytes, {dt:.1f}s")
        check(H.ranges.get("/big.html") == "bytes=0-65535", "Range: bytes=0-65535 was sent")
        check((ctx.rd.raw / "probe" / f"{e['sha1']}.json").exists(), "cache file written for the capped body")
        H.sent.clear()
        e = av.probe_generic(ctx, base + "/data.bin")
        check(e["rule"] == "P15" and e["method"] == "HEAD" and e["content_length"] == H.BIG, "HEAD on a 200 MiB octet-stream -> P15 from headers", f"{e['rule']} {e['method']} {e['content_length']}")
        ds = {"_file_probes": []}
        fp = av.file_probe(ctx, ds, base + "/data.bin")
        check(fp["http_status"] == 200 and H.sent.get("/data.bin", 0) < 16 << 20, "file_probe of a binary that ignores Range does not download it", f"{H.sent.get('/data.bin')} bytes")
        e = av.classify_generic(ctx, base + "/redir", av.probe_fetch(ctx, "probe", base + "/redir", "GET"), "GET-range")
        check(e["rule"] == "P22" and e["status_chain"] == [302, 200], "302 -> /login page -> P22 with chain [302, 200]", f"{e['rule']} {e['status_chain']}")
        e = av.classify_generic(ctx, base + "/loop", av.probe_fetch(ctx, "probe", base + "/loop", "GET"), "GET-range")
        check(e["status_chain"] == [302] * 6 and e["rule"] == "P21", "redirect loop stops after five hops -> P21", f"{e['rule']} {e['status_chain']}")
        e = av.probe_generic(ctx, base + "/dua.html")
        check(e["rule"] == "P16", "HEAD 405 then GET-range; DUA in body -> P16", e["rule"])
        e = av.probe_generic(ctx, base + "/navonly.html")
        check(e["rule"] == "P21", "REG_RE only inside <nav> -> P21", e["rule"])
        e = av.probe_generic(ctx, base + "/authors-dataset/")
        bug(e["rule"] == "P22", "live: landing path containing 'author' with a working .bin anchor classified auth-required (should be P20 open-download)", f"{e['rule']} {e['classification_machine']}")
        # DNS failure: three attempts, P23, but raw_sha1 names a cache file that was never written
        t0 = time.monotonic()
        e = av.probe_fetch(ctx, "probe", "http://nonexistent-host.invalid/x", "GET")
        e2 = av.classify_generic(ctx, "http://nonexistent-host.invalid/x", e, "GET-range")
        check(e["status"] == 0 and e["attempts"] == 3 and e2["rule"] == "P23", "DNS failure: 3 attempts, status 0 -> P23", f"{e['status']} {e['attempts']} {e2['rule']} {time.monotonic() - t0:.1f}s")
        bug(e2["raw_sha1"] is not None and not (ctx.rd.raw / "probe" / f"{e['sha1']}.json").exists(),
            "raw_sha1 recorded for a failed probe whose envelope was never cached -> --replay of a P23 run raises ReplayMiss")
        log = [json.loads(l) for l in ctx.rd.requests_log.read_text(encoding="utf-8").splitlines() if l.strip()]
        check(sum(r["url"].endswith("nonexistent-host.invalid/x") for r in log) == 3, "each of the three attempts is logged")
    finally:
        srv.shutdown()


# ----------------------------------------------------------------------------- D. GitHub README recursion, offline
def part_d(ctx) -> None:
    print("\n== D. r_github README link recursion (stubbed API, no network) ==")
    readme = {"a/data": "See the code at https://github.com/a/code", "a/code": "Data at https://github.com/a/data"}

    def fake_api(source, url, params=None, headers=None, credential=None):
        m = re.search(r"repos/([^/]+/[^/]+)(/releases|/readme)?$", url)
        repo, part = m.group(1), m.group(2)
        if part == "/releases":
            body = "[]"
        elif part == "/readme":
            body = json.dumps({"content": base64.b64encode(readme[repo].encode()).decode()})
        else:
            body = json.dumps({"full_name": repo})
        return Resp(200, body, {"content-type": "application/json"}, "3" * 40, True, 0)

    ctx.api = fake_api
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(400)
    try:
        av.r_github(ctx, {"_file_probes": []}, "https://github.com/a/data", None)
        bug(False, "two GitHub repos linking each other in their READMEs recurse without limit")
    except RecursionError:
        bug(True, "two GitHub repos linking each other in their READMEs recurse without limit (classify_url drops `depth`)")
    finally:
        sys.setrecursionlimit(old)
    # a DOI link in a README is not followed (doi.org is neither in HOSTS nor CLOUD_RE)
    readme["a/data"] = "Dataset DOI: https://doi.org/10.5281/zenodo.4588403"
    calls = []
    orig = av.classify_url
    av.classify_url = lambda *a, **k: calls.append(a[2]) or {"rule": "P1", "classification_machine": "open-download", "evidence": ""}
    try:
        e = av.r_github(ctx, {"_file_probes": []}, "https://github.com/a/data", None)
        bug(not calls and e["rule"] == "P21", "README whose only data link is a doi.org DOI is not followed -> P21 unresolved", f"followed={calls} rule={e['rule']}")
    finally:
        av.classify_url = orig


def main() -> int:
    rd_path = ROOT / "tests" / "run_fixture"
    if rd_path.exists():
        shutil.rmtree(rd_path)
    rd = init_run_dir(rd_path, "2026-09-19", ["tests/test_availability_fixture.py"])
    ctx = av.Ctx(rd, "2026-09-19", replay=False)
    part_a()
    part_b(ctx)
    part_c(ctx)
    part_d(ctx)
    print(f"\n{RESULTS['pass']} pass, {RESULTS['fail']} fail, {RESULTS['bug']} bugs confirmed")
    return 1 if RESULTS["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
