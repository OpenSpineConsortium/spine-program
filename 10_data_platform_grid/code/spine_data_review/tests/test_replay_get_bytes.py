"""Reviewer check: does `--replay` stay off the network for the Papers-with-Code dump?
Builds a RateLimitedSession(replay=True) whose underlying requests.Session.get is stubbed to record
any call, then calls sdr.search_repositories._get_bytes. Under the protocol (section 15) replay must
never touch the network; a recorded call is a FAIL. Also checks that a 200 dump is cached under a
sha1-named file like every other body (it is written to raw/pwc/dump.b64.json instead)."""
import shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from sdr.common import RateLimitedSession, ReplayMiss, init_run_dir
import sdr.search_repositories as sr

rd = init_run_dir(ROOT / "tests" / "_fixture_run_replay", "2026-09-19", ["fixture"])
sess = RateLimitedSession(rd, replay=True)
calls = []


class R:
    status_code, content = 200, b"\x1f\x8b"


sess.s.get = lambda url, **kw: (calls.append(url), R())[1]
run = sr.Run(rd, sess, "2026-09-19", None, False)
try:
    status, body = sr._get_bytes(run, "pwc", "pwc_dump", "https://production-media.paperswithcode.com/about/datasets.json.gz")
    print("FAIL a replay cache miss returned silently:", status)
    calls.append("<no ReplayMiss raised>")
except ReplayMiss as e:  # the loud failure PROTOCOL.md section 15 asks for
    print("PASS replay cache miss raises ReplayMiss:", e)
print("network calls under --replay:", calls)
print("PASS" if not calls else "FAIL", "replay stays off the network for _get_bytes")
files = sorted(p.name for p in (rd.raw / "pwc").glob("*")) if (rd.raw / "pwc").exists() else []
print("raw/pwc files:", files)
log = (rd.requests_log.read_text() if rd.requests_log.exists() else "")
print("PASS" if '"cache_sha1": null' not in log else "FAIL", "request log line carries a cache sha1 (it is null)")
shutil.rmtree(ROOT / "tests" / "_fixture_run_replay", ignore_errors=True)
sys.exit(1 if calls else 0)
