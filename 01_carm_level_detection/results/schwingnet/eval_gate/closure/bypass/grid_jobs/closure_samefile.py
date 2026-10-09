"""Was the pre-gate dump behind the 21 headline-detector rows (or_ready/lodo/sweeps/lodo_carm__carm_test.json) made by
the weights file now at its path? It records no sha256, so eval_gate/2 refuses it. The closure run re-scored the same
56 frames with that file (tools/realxray_eval.py, eval_gate/2, out/C_rx.json, sha256 recorded). If every frame's raw
predictions agree, the old dump was made by a file that predicts identically to today's -- evidence from outside the
gate that the path-keyed verdict it was carried under described the right weights."""
import json
import sys

old, new, out = sys.argv[1], sys.argv[2], sys.argv[3]
a, b = json.load(open(old)), json.load(open(new))
fa = {r["stem"]: r for r in a["frames"]}
fb = {r["stem"]: r for r in b["frames"]}
same_raw = same_det = 0
diff = []
for s in sorted(set(fa) | set(fb)):
    x, y = fa.get(s), fb.get(s)
    if x is None or y is None:
        diff.append(dict(stem=s, why="frame in one dump only"))
        continue
    same_det += x.get("det") == y.get("det")
    if x.get("raw") == y.get("raw"):
        same_raw += 1
    elif len(diff) < 5:
        diff.append(dict(stem=s, old_n=len(x.get("raw") or []), new_n=len(y.get("raw") or []),
                         old_first=(x.get("raw") or [None])[0], new_first=(y.get("raw") or [None])[0]))
r = dict(old=old, new=new, old_weights=a.get("weights"), new_weights=b.get("weights"),
         new_weights_sha256=b.get("weights_sha256"), frames_old=len(fa), frames_new=len(fb),
         frames_raw_identical=same_raw, frames_det_identical=same_det, pooled_identical=a.get("pooled") == b.get("pooled"),
         old_params={k: a.get(k) for k in ("conf", "min_vis", "data", "split")},
         new_params={k: b.get(k) for k in ("conf", "min_vis", "data", "split")}, examples_of_difference=diff)
json.dump(r, open(out, "w"), indent=1)
print(json.dumps(r, indent=1)[:3000])
