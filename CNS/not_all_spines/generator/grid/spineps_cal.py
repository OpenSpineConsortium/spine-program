"""The body's chords on SPINEPS's corpus label: each vertebra built by the engine from SPINEPS's instance
mask (frame, canal wall), its body then taken as SPINEPS's corpus and end plates (subregions 49, 52, 53),
which hold neither the arch nor the costal processes nor, where SPINEPS draws them apart, the uncinate
processes; read by scanimport's body_chords and by morphometry/plates.py. One CSV a study.

    python spineps_cal.py <list of seg-vert paths> <out dir> <workers>
"""
import csv, math, os, sys, traceback
from concurrent.futures import ProcessPoolExecutor
import numpy as np

BODY = (49, 52, 53)


def one(job):
    vert, outdir = job
    sub_path = vert.replace("_seg-vert_msk", "_seg-spine_msk")
    name = os.path.basename(os.path.dirname(os.path.dirname(vert))) + "-" + os.path.basename(vert).split("_seg-vert")[0]
    dest = os.path.join(outdir, name + ".csv")
    if os.path.exists(dest):
        return
    try:
        from scanimport import volume as V, geometry as G
        from morphometry import measure as M, anatomy as A, plates as PL
        vol, grid, names, problems, merged = V.read_labels(vert, "spineps")
        sdata, _ = V.load(sub_path)
        sub = np.asarray(sdata).astype(np.int16)
        keep = {}
        M.measure_volume(vol, grid, names, name, pelvis=False, keep=keep)
        rows = []
        for lv, v in keep.get("verts", {}).items():
            corpus = np.isin(sub[tuple(v.idx.T)], BODY)
            if corpus.sum() < G.MIN_BODY_VOXELS:
                continue
            v.body = corpus
            got = G.body_chords(A.square_to_wall(v, v.body_pts), v.wall_y0, v.grid, v.frame)
            plates, _ = PL.measures(v)
            for k in ("endplate", "endplate_depth", "endplate_lower", "endplate_lower_depth"):
                rows.append((lv, "sp_" + k, got.get(k, math.nan)))
            for k, x in plates.items():
                rows.append((lv, "sp_" + k, x))
        with open(dest, "w", newline="") as h:
            w = csv.writer(h)
            w.writerow(["source", "study", "level", "key", "value"])
            for lv, k, x in rows:
                w.writerow([name.split("-")[0], name, lv, k, "" if not np.isfinite(x) else "%.4f" % x])
    except Exception:
        open(dest + ".err", "w").write(traceback.format_exc())


if __name__ == "__main__":
    paths = [l.strip() for l in open(sys.argv[1]) if l.strip()]
    os.makedirs(sys.argv[2], exist_ok=True)
    with ProcessPoolExecutor(int(sys.argv[3])) as pool:
        list(pool.map(one, [(p, sys.argv[2]) for p in paths]))
