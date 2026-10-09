"""VERIFY item 2 (fourth row): the case-name shapes of every source in the allspine_v9 rung-1 bank, so that a
C-ArmLSpine patient hiding under another spelling (a CBCT render, a physics_rare render) would show."""
import collections
import re

import numpy as np

z = np.load("/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx/rung_1.npz", allow_pickle=True)
c = z["case"].astype(str)
s = z["source"].astype(str)
d = collections.defaultdict(set)
for a, b in zip(c, s):
    d[b].add(a)
for k, v in sorted(d.items()):
    shapes = collections.Counter(re.sub(r"[0-9]+", "#", x) for x in v).most_common(6)
    print(k, len(v), sorted(v)[:4], sorted(v)[-3:], shapes)
hits = sorted(x for v in d.values() for x in v if re.search(r"(?i)carm|cbct|(?<![0-9A-Za-z])case\d+|(?<![0-9])(42|121|136)(?![0-9])", x)
              and not re.match(r"^(C|L)?\d+$", x))
print("names mentioning carm / cbct / case<n> / 42 / 121 / 136:", len(hits), hits[:40])
