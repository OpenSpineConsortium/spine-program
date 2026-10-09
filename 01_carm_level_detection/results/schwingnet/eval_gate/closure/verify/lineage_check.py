"""Test-fold cases against the fold model's own train/val keys and the allspine_v9 ancestor's keys, read from the lineage store's on-demand cache (closure VERIFY.md).

    python lineage_check.py    # reads lineage_rows.txt, writes lineage_check.json
"""
import re, json, sys, bisect, os
sys.path.insert(0, "spinesurg-ct-nnunet:")
from tools.patient_keys import canon_key
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, "lineage_rows.txt"), encoding="utf-8", errors="replace").read()  # login-node grep of or_ready/eval_gate/ondemand/*.json, 2026-09-24 15:44 EDT
blocks = re.split(r"^### ", t, flags=re.M)[1:]

R = os.path.join(HERE, "raw", "proto_v9init_prerepair")
def test_cases(fold):
    d = json.load(open(f"{R}/{fold}/det_score_kfull.json", encoding="utf-8"))
    return {canon_key("carmlspine:" + fr["case"]) for fr in d["frames"]}
out = {}
for b in blocks:
    head, rest = b.split("\n", 1)
    tag, path = head.split(" ", 1)
    hdrs = [(int(m.group(1)), m.group(2)) for m in re.finditer(r'^(\d+): "(/[^"]+)"', rest, re.M)]        # row starts
    secs = [(int(m.group(1)), m.group(2)) for m in re.finditer(r'^(\d+):  "([a-z_]+)"', rest, re.M)]     # sections
    case_lines = [(int(m.group(1)), m.group(2)) for m in re.finditer(r'^(\d+):   "((?:case|carmlspine):[^"]+)"', rest, re.M)]
    rows = {}
    for L, key in case_lines:
        ri = bisect.bisect_right([h[0] for h in hdrs], L) - 1; row = hdrs[ri][1].split("/")[-1]
        si = bisect.bisect_right([s[0] for s in secs], L) - 1; sec = secs[si][1]
        rows.setdefault(row, {}).setdefault(sec, set()).add(canon_key(key))
    rec = dict(file=path.split("/")[-1], rows_in_file=[h[1].split("/")[-1] for h in hdrs],
               carm_keys_by_row_and_section={r: {s: len(v) for s, v in d.items()} for r, d in rows.items()})
    m = re.match(r"model_rung_1_ft_(cv(?:day)?\d)_v9init_aug2", tag)
    if m:
        fold = m.group(1).replace("cv", "cv_fold", 1) if not m.group(1).startswith("cvday") else m.group(1).replace("cvday", "cvday_fold")
        tc = test_cases(fold)
        own = rows.get(f"{tag}.pt", {})
        seen = set().union(*[v for s, v in own.items() if s in ("train_keys", "val_keys")]) if own else set()
        rec["test_fold"] = fold; rec["n_test_cases"] = len(tc)
        rec["test_in_own_train_or_val"] = sorted(tc & seen); rec["own_train_val_persons"] = len(seen)
        rec["test_in_touched_keys"] = len(tc & own.get("touched_keys", set()))
    v9 = rows.get("model_rung_1_aug2.pt", {})
    rec["v9_encoder_row_carm_keys"] = {s: len(v) for s, v in v9.items()}
    out[tag] = rec
json.dump(out, open(os.path.join(HERE, "lineage_check.json"), "w"), indent=1)
for k, v in out.items():
    print(k, "| rows:", v["rows_in_file"], "| carm keys:", v["carm_keys_by_row_and_section"], "| v9 row carm keys:", v["v9_encoder_row_carm_keys"],
          ("| test %s: %d cases, in own train/val %s, own persons %d, in touched %d" % (v["test_fold"], v["n_test_cases"], v["test_in_own_train_or_val"], v["own_train_val_persons"], v["test_in_touched_keys"])) if "test_fold" in v else "")
