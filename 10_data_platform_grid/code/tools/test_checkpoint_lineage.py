#!/usr/bin/env python
# Copied 2026-10-08 from spinesurg-ct-nnunet (branch L6_Class, commit 097933a): tools/test_checkpoint_lineage.py. committed state at 097933a. The repository is the executable source; this copy is a record.
"""Does tools/checkpoint_lineage.py find what a checkpoint's ANCESTORS saw? A synthetic tree with a known answer.

The tree reproduces the 2026-09-23 leak in miniature (SchwingNet/results/arc/ARC_CHECK.md item 4):
  anchor   an Ultralytics run from yolo11m.pt whose TRAIN holds subject s0585 and whose VAL holds s1062
  rx_child fine-tuned FROM anchor on real COBRA + DeepFluoro frames only -- its own lists name no TS subject
  pooled   from yolo11m.pt; s0585 is only in its VAL (selection) list, and its styled stems carry three pose donors
A tool that reads only a checkpoint's own train list calls s0585 held out for rx_child and for pooled. This one must
not. Around that: a level encoder found through a launch script, a fine-tune whose array index is bound from the
file name, a head on top, a checkpoint no reader understands, one that is not on disk, a list rewritten after
training began, and a bank case no rule can key -- each must surface as `unresolved` and travel to descendants.
The gaps the first full grid run left are reproduced too: a run that sits in its own directory under two candidate
cwds (detect_v3), a rewritten train dir whose Ultralytics label cache holds the training-time list (and one whose cache
holds another run's list), implant renders whose hardware records are gone, a trainer and a bank build launched inside
`$(sbatch --wrap="...")`, and a deleted bank bounded by its build line.
Runs anywhere with numpy, pyyaml and torch (no Ultralytics: a checkpoint is faked as a dict with train_args).
"""
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
TOOL = HERE / "checkpoint_lineage.py"
sys.path.insert(0, str(HERE))
import checkpoint_lineage as CL  # noqa: E402

bad = 0


def check(cond, msg):
    global bad
    print(("ok   " if cond else "FAIL ") + msg)
    bad += not cond


T0 = time.time() - 100000
R = tempfile.mkdtemp(prefix="ckptlineage_").replace("\\", "/")
H, D = f"{R}/home", f"{R}/data"


def touch(p, t, content=b""):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(p):
        Path(p).write_bytes(content)
    os.utime(p, (t, t))


def yolo_run(run_dir, model, data_yaml, t_start, t_end, pretrained=True):
    ta = {"model": model, "data": data_yaml, "pretrained": pretrained, "resume": False, "fraction": 1.0,
          "project": os.path.dirname(run_dir), "name": os.path.basename(run_dir)}
    Path(run_dir, "weights").mkdir(parents=True, exist_ok=True)
    Path(run_dir, "args.yaml").write_text("".join(f"{k}: {v}\n" for k, v in ta.items()))
    os.utime(f"{run_dir}/args.yaml", (t_start, t_start))
    torch.save({"train_args": ta, "model": None, "ema": None, "date": "x"}, f"{run_dir}/weights/best.pt")
    os.utime(f"{run_dir}/weights/best.pt", (t_end, t_end))
    return f"{run_dir}/weights/best.pt"


# ---- the public root
torch.save({"train_args": {"data": "coco.yaml"}, "model": None, "ema": None}, f"{R}/yolo11m_tmp.pt")
Path(f"{H}/spine-detector").mkdir(parents=True, exist_ok=True)
os.replace(f"{R}/yolo11m_tmp.pt", f"{H}/spine-detector/yolo11m.pt")

# ---- anchor: renders under DeepFluoro poses; s0585 trains, s1062 selects
A = f"{H}/model_night/anchor"
touch(f"{A}/images/train/s0585_00_17-1882-015.jpg", T0)
touch(f"{A}/images/val/s1062_00_17-1882-001.jpg", T0)
Path(f"{A}/data.yaml").write_text(f"path: {A}\ntrain: images/train\nval: images/val\nnames:\n  0: vertebra\n")
os.utime(f"{A}/data.yaml", (T0, T0))
for d in (f"{A}/images/train", f"{A}/images/val"):
    os.utime(d, (T0, T0))
anchor = yolo_run(f"{H}/spine-detector/runs/pose/anchor", "yolo11m.pt", f"{A}/data.yaml", T0 + 10, T0 + 1000)

# ---- rx_child: real frames only, initialised from anchor
for f in ("cobra_elekta/images/train/A001_0000.png", "deepfluoro/images/train/17-1882_000.png",
          "cobra_elekta/images/test/B002_0003.png"):
    touch(f"{D}/realxray/{f}", T0 + 1100)
for d in ("cobra_elekta/images/train", "deepfluoro/images/train", "cobra_elekta/images/test"):
    os.utime(f"{D}/realxray/{d}", (T0 + 1100, T0 + 1100))
RX = f"{H}/spine-detector/runs/realxray/rx_child"
Path(RX).mkdir(parents=True, exist_ok=True)
Path(f"{RX}/data.yaml").write_text(f"train:\n- {D}/realxray/cobra_elekta/images/train\n- {D}/realxray/deepfluoro/images/train\n"
                                   f"val:\n- {D}/realxray/cobra_elekta/images/test\n")
os.utime(f"{RX}/data.yaml", (T0 + 1100, T0 + 1100))
rx = yolo_run(RX, anchor, f"{RX}/data.yaml", T0 + 1200, T0 + 2000)

# ---- pooled: styled renders; s0585 is a SELECTION subject only
L = f"{D}/devcorpus/lists/P_pooled"
Path(L).mkdir(parents=True, exist_ok=True)
S = f"{D}/devcorpus/styled"
Path(f"{L}/train.txt").write_text("\n".join([f"{S}/cios_fusion__cios_fusion/images/train/s0224_00_17-1882-015_cios_fusion_0.jpg",
                                             f"{S}/elekta_xvi__elekta_xvi/images/train/s0225_00_A102-0258_elekta_xvi_0.jpg",
                                             f"{S}/surgio_b51_dr__surgio_b51_dr/images/train/s0226_00_case114-LAT_surgio_b51_dr_1.jpg"]) + "\n")
Path(f"{L}/val.txt").write_text(f"{S}/cios_fusion__cios_fusion/images/val/s0585_00_17-1882-106_cios_fusion_0.jpg\n")
Path(f"{L}/data.yaml").write_text(f"path: {L}\ntrain: {L}/train.txt\nval: {L}/val.txt\n")
for f in ("train.txt", "val.txt", "data.yaml"):
    os.utime(f"{L}/{f}", (T0, T0))
pooled = yolo_run(f"{H}/spine-detector/runs/devcorpus/dc_P_pooled", "yolo11m.pt", f"{L}/data.yaml", T0 + 10, T0 + 900)

# ---- stale: its train list was rewritten after training began
L2 = f"{D}/devcorpus/lists/stale"
Path(L2).mkdir(parents=True, exist_ok=True)
Path(f"{L2}/train.txt").write_text(f"{S}/x/images/train/s0300_00_17-1882-015_cios_fusion_0.jpg\n")
Path(f"{L2}/val.txt").write_text(f"{S}/x/images/val/s0301_00_17-1882-015_cios_fusion_0.jpg\n")
Path(f"{L2}/data.yaml").write_text(f"path: {L2}\ntrain: train.txt\nval: val.txt\n")
for f, t in (("train.txt", T0 + 5000), ("val.txt", T0), ("data.yaml", T0)):
    os.utime(f"{L2}/{f}", (t, t))
stale = yolo_run(f"{H}/spine-detector/runs/devcorpus/dc_stale", "yolo11m.pt", f"{L2}/data.yaml", T0 + 10, T0 + 900)

# ---- level encoder (launcher, no --init) -> fine-tune (array index bound from the file name) -> head
B0 = f"{H}/allspine_x_fov96_ctx"
Path(f"{B0}/runs").mkdir(parents=True, exist_ok=True)
np.savez(f"{B0}/rung_1.npz", case=np.array(["TS_s0585", "TS_s0585", "gl003", "CTSP_COLONOG_1"]),
         split=np.array(["train", "train", "val", "train"]), source=np.array(["ts", "ts", "verse", "ctsp"]))
Path(f"{B0}/meta.json").write_text("{}")
os.utime(f"{B0}/rung_1.npz", (T0, T0))
torch.save({"conv1.weight": torch.zeros(1)}, f"{B0}/runs/model_rung_1_aug2.pt")
json.dump({"n_train": 3, "n_val": 1}, open(f"{B0}/runs/result_rung_1_aug2.json", "w"))
os.utime(f"{B0}/runs/model_rung_1_aug2.pt", (T0 + 3000, T0 + 3000))
B1 = f"{H}/carm_cvmix0_fov96_ctx"
Path(f"{B1}/runs").mkdir(parents=True, exist_ok=True)
np.savez(f"{B1}/rung_1.npz", case=np.array(["case017_AP", "case018_LAT"]), split=np.array(["train", "val"]),
         source=np.array(["carm", "carm"]))
Path(f"{B1}/meta.json").write_text("{}")
os.utime(f"{B1}/rung_1.npz", (T0 + 3100, T0 + 3100))
torch.save({"conv1.weight": torch.ones(1)}, f"{B1}/runs/model_rung_1_ft_cv0_aug2.pt")
os.utime(f"{B1}/runs/model_rung_1_ft_cv0_aug2.pt", (T0 + 4000, T0 + 4000))
Path(f"{H}/model_night/heads_carm").mkdir(parents=True, exist_ok=True)
torch.save({"w": torch.zeros(1)}, f"{H}/model_night/heads_carm/head_cv0.pt")
json.dump({"kind": "recurrent_head", "base_model": f"{B1}/runs/model_rung_1_ft_cv0_aug2.pt", "bank": B1, "rung": "1"},
          open(f"{H}/model_night/heads_carm/head_cv0.arch.json", "w"))
SL = f"{R}/slurm"
Path(SL).mkdir()
Path(f"{SL}/train_x.sh").write_text(
    "#!/bin/bash\nH=$HOME\nCTX=$H/allspine_x_fov96_ctx\n"
    "$PYD -u tools/train_level_classifier.py --data \"$CTX\" --rung 1 --out \"$CTX/runs\" --epochs 40 --augment 2 2>&1 | tail -30\n")
Path(f"{SL}/cv.sh").write_text(
    "#!/bin/bash\nK=${SLURM_ARRAY_TASK_ID:-0}; NF=${NFOLDS:-5}\n"
    "INIT=${INIT_MODEL:-$(ls \"$HOME\"/allspine_x_fov96_ctx/runs/model_rung_1*.pt 2>/dev/null | head -1)}\n"
    "BANK=$HOME/carm_cvmix${K}_fov96_ctx\nMODEL=$BANK/runs/model_rung_1_ft_cv${K}_aug2.pt\n"
    "[ -f $MODEL ] || $PY -u tools/train_level_classifier.py --data $BANK --rung 1 --out $BANK/runs --init \"$INIT\" --epochs 15 \\\n"
    "    --augment 2 --tag ft_cv$K 2>&1 | tail -8\n")
# the allspine_v2_chain.sh shape: bank build and training both inside $(sbatch ... --wrap="...")
Path(f"{SL}/chain_w.sh").write_text(
    "#!/bin/bash\nH=$HOME; cd $H\nCTX=$H/allspine_w_fov96_ctx\n"
    "J1=$(sbatch --parsable -J w_r1 -q gpu --wrap=\"export TMPDIR=$H/tmp; $H/py -u tools/train_level_classifier.py "
    "--data $CTX --rung 1 --out $CTX/runs --epochs 40 --augment 2\")\n"
    "G=$H/allspine_gone_fov96_ctx\n"
    "J0=$(sbatch --parsable -J g_bank --wrap=\"export TMPDIR=$H/tmp; $H/py -u tools/make_context_crops.py --drr $H/bnd_drr_a "
    "--drr $H/bnd_drr_b --dst $G --mode fov --group-regex '^(?:ctsp)_(.+?)_p[0-9]+\\$' --rungs 1 && touch $G/READY\")\n"
    "$PYC -u tools/make_implant_ct.py --scheme ctsp --src $H/data/CTSpinoPelvic1K --dst $H/implant_ct_gone --variants 2\n")
# the corpus_expand.sh shape: a builder inside a shell function, bound per call. Read as one line, `--dst "$H/$DST"`
# would match every bank (and make the deleted bank's bound above incomplete); read per call it builds only these two
Path(f"{SL}/fn_build.sh").write_text(
    "#!/bin/bash\nH=$HOME\n"
    "crops () {   # render-dir  bank-name\n"
    "  local SRC=$1 DST=$2 RE=$3\n"
    "  \"$PY\" -u tools/make_context_crops.py --drr \"$SRC\" --dst \"$H/$DST\" --size 320 2>&1 | tail -6\n"
    "}\n"
    "crops \"$H/mendeley_drr\" mendeley_fov96_ctx ''\n"
    "B=$(crops \"$H/vindr_pseudo\" vindrps_fov96_ctx '^V(.+)$')\n")
head = f"{H}/model_night/heads_carm/head_cv0.pt"

# ---- relative paths: a copied checkpoint whose train_args name project/model/data relative to the training cwd
#      (detect_v5z: project runs/pose/runs, model runs/pose/runs/pose/runs/detect_v3/weights/best.pt)
SD = f"{H}/spine-detector"
Path(f"{SD}/data/rel").mkdir(parents=True, exist_ok=True)
touch(f"{SD}/data/rel/images/train/nhanes_cervical_00161.jpg", T0)
touch(f"{SD}/data/rel/images/val/buu_0003-F-013Y0__zoom0.jpg", T0)
Path(f"{SD}/data/rel/data.yaml").write_text(f"path: {SD}/data/rel\ntrain: images/train\nval: images/val\n")
for p_ in (f"{SD}/data/rel/data.yaml", f"{SD}/data/rel/images/train", f"{SD}/data/rel/images/val"):
    os.utime(p_, (T0, T0))
rel_parent = yolo_run(f"{SD}/runs/pose/runs/pose/runs/rel_parent", "yolo11m.pt", f"{SD}/data/rel/data.yaml", T0 + 10, T0 + 500)
ta_rel = {"model": "runs/pose/runs/pose/runs/rel_parent/weights/best.pt", "data": "data/rel/data.yaml",
          "pretrained": True, "resume": False, "fraction": 1.0, "project": "runs/pose/runs", "name": "rel_child"}
Path(f"{SD}/runs/pose/runs/rel_child/weights").mkdir(parents=True, exist_ok=True)
Path(f"{SD}/runs/pose/runs/rel_child/args.yaml").write_text("".join(f"{k}: {v}\n" for k, v in ta_rel.items()))
os.utime(f"{SD}/runs/pose/runs/rel_child/args.yaml", (T0 + 600, T0 + 600))
Path(f"{H}/FluoroCap").mkdir(parents=True, exist_ok=True)
torch.save({"train_args": ta_rel, "model": None, "ema": None}, f"{H}/FluoroCap/rel_child_best.pt")
os.utime(f"{H}/FluoroCap/rel_child_best.pt", (T0 + 900, T0 + 900))
rel_copy = f"{H}/FluoroCap/rel_child_best.pt"

# ---- the same, with the run nested the way Ultralytics nests a relative project: <cwd>/runs/<task>/<project>/<name>
ta_nest = {**ta_rel, "name": "nest_child", "task": "pose"}
Path(f"{SD}/runs/pose/runs/pose/runs/nest_child/weights").mkdir(parents=True, exist_ok=True)
Path(f"{SD}/runs/pose/runs/pose/runs/nest_child/args.yaml").write_text("".join(f"{k}: {v}\n" for k, v in ta_nest.items()))
os.utime(f"{SD}/runs/pose/runs/pose/runs/nest_child/args.yaml", (T0 + 600, T0 + 600))
torch.save({"train_args": ta_nest, "model": None, "ema": None}, f"{H}/FluoroCap/nest_child_best.pt")
os.utime(f"{H}/FluoroCap/nest_child_best.pt", (T0 + 900, T0 + 900))
nest_copy = f"{H}/FluoroCap/nest_child_best.pt"

# ---- an encoder from tools/train_level_backbone.py: an .arch.json with no bank, and result_<name>.json recording it
torch.save({"conv1.weight": torch.zeros(2)}, f"{H}/model_night/r18_x_tmp.pt")
Path(f"{H}/model_night/runs").mkdir(parents=True, exist_ok=True)
os.replace(f"{H}/model_night/r18_x_tmp.pt", f"{H}/model_night/runs/model_r18_x.pt")
json.dump({"arch": "resnet18", "loss": "ce", "img_size": 320}, open(f"{H}/model_night/runs/model_r18_x.arch.json", "w"))
json.dump({"name": "r18_x", "arch": "resnet18", "bank": B0, "rung": "1", "init": None, "n_train": 3, "n_val": 1,
           "marker_route": "fine-tuned"}, open(f"{H}/model_night/runs/result_r18_x.json", "w"))
os.utime(f"{H}/model_night/runs/model_r18_x.pt", (T0 + 3000, T0 + 3000))
os.utime(f"{H}/model_night/runs/result_r18_x.json", (T0 + 2990, T0 + 2990))
backbone = f"{H}/model_night/runs/model_r18_x.pt"

# ---- detect_v3's shape: the run sits in its OWN directory, so both layouts match (cwd .../runs/pose flat, or
#      spine-detector nested); only the nested reading makes the relative data yaml exist
ta_v3 = {"model": "yolo11m.pt", "data": "data/rel/data.yaml", "pretrained": True, "resume": False, "fraction": 1.0,
         "project": "runs/pose/runs", "name": "v3like", "task": "pose"}
V3 = f"{SD}/runs/pose/runs/pose/runs/v3like"
Path(f"{V3}/weights").mkdir(parents=True, exist_ok=True)
Path(f"{V3}/args.yaml").write_text("".join(f"{k}: {v}\n" for k, v in ta_v3.items()))
os.utime(f"{V3}/args.yaml", (T0 + 600, T0 + 600))
torch.save({"train_args": ta_v3, "model": None, "ema": None}, f"{V3}/weights/best.pt")
os.utime(f"{V3}/weights/best.pt", (T0 + 900, T0 + 900))
v3like = f"{V3}/weights/best.pt"


def label_cache(path, im_files, t):
    """an Ultralytics label cache: a pickled dict saved with np.save, then renamed to .cache"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    np.save(path + ".npy", {"labels": [{"im_file": f} for f in im_files], "hash": "h", "version": "1.0.3"},
            allow_pickle=True)
    os.replace(path + ".npy", path)
    os.utime(path, (t, t))


# ---- a train directory rewritten after training began, with Ultralytics' own cache of the list it scanned:
#      s0402 was trained on and has since been deleted; the cache must bring it back
LC = f"{D}/lc"
for s in ("s0400", "s0401"):
    touch(f"{LC}/images/train/{s}_00_17-1882-015.jpg", T0)
touch(f"{LC}/images/val/s0403_00_17-1882-015.jpg", T0)
label_cache(f"{LC}/labels/train.cache", [f"{LC}/images/train/{s}_00_17-1882-015.jpg" for s in ("s0400", "s0401", "s0402")],
            T0 + 40)
Path(f"{LC}/data.yaml").write_text(f"path: {LC}\ntrain: images/train\nval: images/val\n")
os.utime(f"{LC}/data.yaml", (T0, T0))
os.utime(f"{LC}/images/val", (T0, T0))
os.utime(f"{LC}/images/train", (T0 + 5000, T0 + 5000))
lc_run = yolo_run(f"{H}/spine-detector/runs/pose/lc_run", "yolo11m.pt", f"{LC}/data.yaml", T0 + 10, T0 + 900)
# ... and one whose cache was written by a run on a DIFFERENT list (a file from outside its entries): no stand-in
LC2 = f"{D}/lc2"
touch(f"{LC2}/images/train/s0410_00_17-1882-015.jpg", T0)
touch(f"{LC2}/images/val/s0411_00_17-1882-015.jpg", T0)
label_cache(f"{LC2}/labels/train.cache", [f"{LC2}/images/train/s0410_00_17-1882-015.jpg",
                                          f"{D}/elsewhere/images/train/s0499_00_17-1882-015.jpg"], T0 + 40)
Path(f"{LC2}/data.yaml").write_text(f"path: {LC2}\ntrain: images/train\nval: images/val\n")
os.utime(f"{LC2}/data.yaml", (T0, T0))
os.utime(f"{LC2}/images/val", (T0, T0))
os.utime(f"{LC2}/images/train", (T0 + 5000, T0 + 5000))
lc2_run = yolo_run(f"{H}/spine-detector/runs/pose/lc2_run", "yolo11m.pt", f"{LC2}/data.yaml", T0 + 10, T0 + 900)

# ---- a C-ArmLSpine export directory rewritten after training began, with no usable label cache: its patients are
#      bounded by the exporter's deterministic split over the release's case list. One train case's frames have been
#      deleted from the export since; the bound must still count it. A second export holds a frame in the wrong split
#      directory, so the declaration does not describe it and the row stays unresolved.
REL = f"{R}/release/C-ArmLSpine"
for i in range(1, 13):
    Path(f"{REL}/case{i}").mkdir(parents=True, exist_ok=True)
os.utime(REL, (T0 - 100, T0 - 100))
sp = {c: CL._carmlspine_split_of(c) for c in (f"case{i}" for i in range(1, 13))}
tr_cases = sorted(c for c, s in sp.items() if s == "train")
dropped = tr_cases[0]
CX = f"{D}/realxray/carmlspine"
for c, s in sp.items():
    if c != dropped:
        touch(f"{CX}/images/{s}/{c}_AP.png", T0)
for s in ("train", "val", "test"):
    Path(f"{CX}/images/{s}").mkdir(parents=True, exist_ok=True)
Path(f"{CX}/det.yaml").write_text(f"train: {CX}/images/train\nval: {CX}/images/val\n")
os.utime(f"{CX}/det.yaml", (T0, T0))
os.utime(f"{CX}/images/val", (T0, T0))
os.utime(f"{CX}/images/train", (T0 + 5000, T0 + 5000))
det_run = yolo_run(f"{H}/spine-detector/runs/realxray/rx_det", "yolo11m.pt", f"{CX}/det.yaml", T0 + 10, T0 + 900)
CB = f"{D}/bad/realxray/carmlspine"
wrong = next(c for c, s in sp.items() if s == "test")
touch(f"{CB}/images/train/{wrong}_AP.png", T0)                    # a test-split case sitting in train
touch(f"{CB}/images/val/{next(c for c, s in sp.items() if s == 'val')}_AP.png", T0)
Path(f"{CB}/det.yaml").write_text(f"train: {CB}/images/train\nval: {CB}/images/val\n")
os.utime(f"{CB}/det.yaml", (T0, T0))
os.utime(f"{CB}/images/val", (T0, T0))
os.utime(f"{CB}/images/train", (T0 + 5000, T0 + 5000))
det_bad = yolo_run(f"{H}/spine-detector/runs/realxray/rx_det_bad", "yolo11m.pt", f"{CB}/det.yaml", T0 + 10, T0 + 900)

# ---- implant renders whose build's hardware records are gone: only the launch line declares the build (ctsp)
IM = f"{D}/imp"
touch(f"{IM}/images/train/implant_0004_v0_ap.png", T0)
touch(f"{IM}/images/val/implant_s0005_v0_lat.png", T0)   # a TotalSegmentator build is NOT declared: refused
Path(f"{IM}/data.yaml").write_text(f"path: {IM}\ntrain: images/train\nval: images/val\n")
for p_ in (f"{IM}/data.yaml", f"{IM}/images/train", f"{IM}/images/val"):
    os.utime(p_, (T0, T0))
imp_run = yolo_run(f"{H}/spine-detector/runs/pose/imp_run", "yolo11m.pt", f"{IM}/data.yaml", T0 + 10, T0 + 900)

# ---- a level encoder launched inside `J1=$(sbatch ... --wrap="...")` (slurm/allspine_v2_chain.sh:24)
BW = f"{H}/allspine_w_fov96_ctx"
Path(f"{BW}/runs").mkdir(parents=True, exist_ok=True)
np.savez(f"{BW}/rung_1.npz", case=np.array(["TS_s0600", "gl004"]), split=np.array(["train", "val"]),
         source=np.array(["ts", "verse"]))
Path(f"{BW}/meta.json").write_text("{}")
os.utime(f"{BW}/rung_1.npz", (T0, T0))
torch.save({"conv1.weight": torch.full((1,), 3.0)}, f"{BW}/runs/model_rung_1_aug2.pt")
json.dump({"n_train": 1, "n_val": 1}, open(f"{BW}/runs/result_rung_1_aug2.json", "w"))
os.utime(f"{BW}/runs/model_rung_1_aug2.pt", (T0 + 3000, T0 + 3000))
wrapped = f"{BW}/runs/model_rung_1_aug2.pt"

# ---- an encoder whose bank was DELETED, and the launch line that built that bank from two roots
for root, case in (("bnd_drr_a", "TS_s0700"), ("bnd_drr_b", "gl009")):
    Path(f"{H}/{root}/ann").mkdir(parents=True, exist_ok=True)
    Path(f"{H}/{root}/ann/{case}.json").write_text("{}")
    os.utime(f"{H}/{root}/ann", (T0, T0))
torch.save({"conv1.weight": torch.full((2,), 5.0)}, f"{H}/model_night/runs/model_r18_gone.pt")
json.dump({"arch": "resnet18", "loss": "ce", "img_size": 320}, open(f"{H}/model_night/runs/model_r18_gone.arch.json", "w"))
json.dump({"name": "r18_gone", "arch": "resnet18", "bank": f"{H}/allspine_gone_fov96_ctx", "rung": "1", "init": None},
          open(f"{H}/model_night/runs/result_r18_gone.json", "w"))
os.utime(f"{H}/model_night/runs/model_r18_gone.pt", (T0 + 3000, T0 + 3000))
os.utime(f"{H}/model_night/runs/result_r18_gone.json", (T0 + 2990, T0 + 2990))
gone_bank = f"{H}/model_night/runs/model_r18_gone.pt"

# ---- a family nobody reads, and a file that is gone
Path(f"{H}/other").mkdir()
torch.save({"x": 1}, f"{H}/other/mystery.pt")
missing = f"{H}/spine-detector/runs/gone/weights/best.pt"

# ---- registry: the base encoder is registered with its bank
Path(f"{H}/model_registry").mkdir()
sha0 = CL.ShaCache(f"{R}/sc.json").get(f"{B0}/runs/model_rung_1_aug2.pt")
Path(f"{H}/model_registry/registry.jsonl").write_text(json.dumps(
    {"ts": "2026-01-01T00:00:00", "name": "allspine_x_rung_1_aug2", "stage": "level_model", "sha": sha0,
     "store_path": f"{H}/model_registry/{sha0[:16]}/model_rung_1_aug2.pt", "source_path": f"{B0}/runs/model_rung_1_aug2.pt",
     "bank": B0, "params": {"rung": "1", "arch": "resnet18"}}) + "\n")

OUT = f"{R}/out"
cmd = [sys.executable, str(TOOL), "resolve", "--out", OUT, "--home", H, "--data", D, "--registry", f"{H}/model_registry",
       "--slurm-dir", SL, "--d813", f"{R}/no_d813", "--verse-manifest", "", "--sweep-set", "", "--arc-json", "",
       "--register"]
for c in (rx, pooled, stale, head, f"{H}/other/mystery.pt", missing, rel_copy, nest_copy, backbone,
          v3like, lc_run, lc2_run, imp_run, wrapped, gone_bank, det_run, det_bad):
    cmd += ["--ckpt", c]
os.environ["CKPT_LINEAGE_CARMLSPINE_RELEASE"] = REL
p = subprocess.run(cmd, capture_output=True, text=True)
print(p.stdout[-1500:], p.stderr[-3000:])
check(p.returncode == 0, "resolve exits 0")
T = json.load(open(f"{OUT}/touched.json"))
n = lambda x: os.path.normpath(x).replace("\\", "/")  # noqa: E731
e_rx, e_an, e_p = T[n(rx)], T[n(anchor)], T[n(pooled)]

print("\n-- the leak this tool exists for")
check("ts:s0585" not in e_rx["train_keys"] and "ts:s0585" not in e_rx["val_keys"],
      "rx_child's OWN lists do not name s0585 (a reader of its lists alone calls s0585 held out)")
check({"ts:s0585", "ts:s1062"} <= set(e_rx["touched_keys"]),
      "rx_child's touched set holds s0585 (parent's train) and s1062 (parent's val)")
check(e_rx["ancestors"] == [n(anchor)], "rx_child's ancestor is the anchor run, read from train_args.model")
check(any("yolo11m" in x and "verified" in x for x in e_rx["public_roots"]),
      "the COCO root is declared exempt and verified from the file's own train_args")
check({"cobra:A001", "deepfluoro:17-1882"} <= set(e_rx["train_keys"]) and e_rx["val_keys"] == ["cobra:B002"],
      "real frames keyed per corpus from the directory they sit in")
check(e_p["val_keys"] == ["ts:s0585"] and "ts:s0585" in e_p["touched_keys"],
      "pooled: s0585 is a selection (val) subject, and selection counts as touched")
check(set(e_p["train_pose_keys"]) == {"deepfluoro:17-1882", "cobra:A102", "carmlspine:case114"},
      "pose donors of all three styled geometries are keyed (the Elekta/Surgio forms were unkeyed before)")
check(not e_rx["unresolved"] and not e_p["unresolved"], "the clean chains carry no unresolved rows")

print("\n-- level models, found through launch scripts")
e_b0 = T[n(f"{B0}/runs/model_rung_1_aug2.pt")]
e_b1 = T[n(f"{B1}/runs/model_rung_1_ft_cv0_aug2.pt")]
e_h = T[n(head)]
check(e_b0["family"] == "level_encoder" and any("torchvision" in x for x in e_b0["public_roots"]),
      "base encoder: launcher has no --init, so its root is the declared ImageNet start")
check(any("verified" in x for x in e_b0["notes"]), "base encoder: bank split verified against result_rung json counts")
check(e_b1["parents"] == [n(f"{B0}/runs/model_rung_1_aug2.pt")],
      "fine-tune: --init read from the launcher, the array index bound from the file name (K=0)")
check(e_h["ancestors"] == [n(f"{B1}/runs/model_rung_1_ft_cv0_aug2.pt"), n(f"{B0}/runs/model_rung_1_aug2.pt")],
      "head: base_model from its arch.json, and the encoder's own chain behind it")
check({"ts:s0585", "verse:gl003", "carmlspine:case017", "carmlspine:case018"} <= set(e_h["touched_keys"]),
      "head: touched is the union over head, fine-tune and base encoder")
check(any("could not be keyed" in u["what"] for u in e_b0["unresolved"]),
      "an unkeyable bank case (Dataset813 stem, no crosswalk) is unresolved, not a patient of its own")
check(any(u["at"] == n(f"{B0}/runs/model_rung_1_aug2.pt") for u in e_h["unresolved"]),
      "... and that unresolved row travels to every descendant (the head's touched set is a lower bound)")

print("\n-- relative train_args (the detect_v5z case)")
e_rc = T[n(rel_copy)]
check(e_rc["parents"] == [n(rel_parent)], "a relative model path is resolved against the cwd read off the disk, "
                                          "not against the run directory")
check(set(e_rc["train_keys"]) == {"nhanes:00161"} and set(e_rc["val_keys"]) == {"buu:0003"} and not e_rc["unresolved"],
      "a relative data yaml resolves the same way; detector-corpus stems (incl. __zoom views) are keyed")

e_nc = T[n(nest_copy)]
check(e_nc["parents"] == [n(rel_parent)] and not e_nc["unresolved"],
      "a relative project nested under runs/<task>/ is found, and the cwd it implies resolves model and data")
e_bb = T[n(backbone)]
check(e_bb["family"] == "level_encoder" and set(e_bb["train_keys"]) == {"ts:s0585"} and e_bb["val_keys"] == ["verse:gl003"]
      and any("verified" in x for x in e_bb["notes"]),
      "an encoder sidecar with no bank is read through its result_<name>.json, not mistaken for a head")

print("\n-- what cannot be read is said, never treated as empty")
e_m = T[n(f"{H}/other/mystery.pt")]
check(e_m["family"] == "unknown" and e_m["unresolved"], "a checkpoint no reader understands is unresolved")
check(T[n(missing)]["unresolved"] and not T[n(missing)]["exists"], "a checkpoint not on disk is unresolved")
check(any("rewritten after training began" in u["what"] for u in T[n(stale)]["unresolved"]),
      "a train list modified after args.yaml was written is unresolved")

print("\n-- the gaps the first full grid run left (2026-09-23)")
e_v3 = T[n(v3like)]
check(set(e_v3["train_keys"]) == {"nhanes:00161"} and not e_v3["unresolved"],
      "detect_v3 shape: of two cwds holding the run's args.yaml, the one where its relative data yaml exists is read")
e_lc = T[n(lc_run)]
check(set(e_lc["train_keys"]) == {"ts:s0400", "ts:s0401", "ts:s0402"} and not e_lc["unresolved"]
      and any("label cache" in x for x in e_lc["notes"]),
      "a train dir rewritten after training began is read from Ultralytics' own label cache (the deleted s0402 counts)")
e_lc2 = T[n(lc2_run)]
check(any("rewritten after training began" in u["what"] and "outside this run" in u["why"] for u in e_lc2["unresolved"])
      and "ts:s0499" not in e_lc2["train_keys"],
      "a label cache holding another run's list does not stand in: the rewritten dir stays unresolved")
check(all("corpus" in u and u["corpus"] is None for u in e_lc2["unresolved"] if "rewritten" in u["what"]),
      "a rewritten-list row states the corpus its location declares (none here, so no claim is made)")
e_dt = T[n(det_run)]
check(set(e_dt["train_keys"]) == {f"carmlspine:{c}" for c in tr_cases} and not e_dt["unresolved"]
      and any("deterministic split" in x for x in e_dt["notes"]),
      "a rewritten C-ArmLSpine export dir is bounded by the exporter's md5 split over the release (a case deleted "
      "from the export since is still counted)")
e_db = T[n(det_bad)]
check(any("rewritten" in u["what"] and "do not sit where" in u["why"] and u["corpus"] == "carmlspine"
          for u in e_db["unresolved"]),
      "an export whose frames contradict the declared split is not bounded by it: unresolved, with its corpus")
e_im = T[n(imp_run)]
check(e_im["train_keys"] == ["ctsp:0004"] and e_im["unkeyed"].get("val", {}).get("shapes", {}).get("implant_s#_v#_lat.png") == 1,
      "an implant render with no hardware record is keyed through the one declared build (ctsp); an undeclared "
      "scheme is refused and counted by name family")
e_w = T[n(wrapped)]
check(e_w["family"] == "level_encoder" and any("torchvision" in x for x in e_w["public_roots"])
      and not any(u["what"] == "initialisation" for u in e_w["unresolved"]),
      "a trainer launched inside $(sbatch --wrap=\"...\") is read: its (absent) --init is recorded, not unresolved")
e_g = T[n(gone_bank)]
gb = [u for u in e_g["unresolved"] if u["what"] == "training bank"]
check(len(gb) == 1 and gb[0]["bound"]["corpora"] == {"ts": 1, "verse": 1} and gb[0]["bound"]["complete"]
      and gb[0]["bound"]["built_by"] and not e_g["train_keys"],
      "a deleted bank stays unresolved and carries the bound its --wrap'd build line gives (two roots, ts + verse)")
bj = json.load(open(f"{OUT}/bounds.json"))
check(bj["banks"][n(f"{H}/allspine_gone_fov96_ctx")]["keys"] == ["ts:s0700", "verse:gl009"],
      "bounds.json holds the bound's patient keys")
run_j = json.load(open(f"{OUT}/touched_run.json"))
check("implant_s#_v#_lat.png" in run_j["unkeyed_census"] and run_j["implant_builds_declared"][0]["scheme"] == "ctsp",
      "touched_run.json carries the unkeyed name-family census and the declared implant builds")

print("\n-- registry, why, shell reading, collect")
lin = [json.loads(l) for l in open(f"{H}/model_registry/lineage.jsonl")]
check(len(lin) == sum(1 for e in T.values() if e["sha"]), "one lineage row per hashed checkpoint")
subprocess.run(cmd, capture_output=True, text=True)
check(len(open(f"{H}/model_registry/lineage.jsonl").readlines()) == len(lin), "re-running appends no duplicate rows")
w = subprocess.run([sys.executable, str(TOOL), "why", "--touched", f"{OUT}/touched.json", "--ckpt", rx, "--key", "ts:s0585",
                    "--home", H], capture_output=True, text=True)
check(w.returncode == 1 and "(ancestor)" in w.stdout, "why: names the ancestor through which s0585 entered")
imap = {"0001_v0": ("ctsp", "0001"), "verse547_v1": ("verse", "verse547"), "s0224_v0": ("totalseg", "s0224")}
got = [CL.PK.key_any(s, implant_map=imap)[0] for s in ("implant_0001_v0_ap", "implant_verse547_v1_lat_p2",
                                                         "implant_s0224_v0_ap")]
check([g and g["key"] for g in got] == ["ctsp:0001", "verse:verse547", "ts:s0224"],
      "an implant render is keyed to its SOURCE CT through make_implant_ct's hardware record")
check(CL.PK.key_any("implant_0999_v0_ap", implant_map=imap)[0] is None,
      "an implant render with no hardware record is refused, not keyed as a patient called implant:<case>")
check([CL.PK.key_any(s)[0]["key"] for s in ("video_panels:-0VlDsfUPac_00059__full", "case101_AP_kfull_0",
                                            "ctsp_0001_ap", "VINDRPS_0036129847a418b87f0882c991fdb089")]
      == ["fluorocap_video:-0VlDsfUPac", "carmlspine:case101", "ctsp:0001", "vindr:0036129847a418b87f0882c991fdb089"],
      "the spellings the first grid run could not key now key (bank video panels, kfull crops, view-only renders, VinDr)")
got2 = [CL.PK.key_any(s, None, {"COLONOG_1": "0149"}, {}, h)[0] for s, h in (
    ("totalseg_s0001_ap", None), ("verse_scan-verse533_ap", None), ("ctsp_drr__CTSP_COLONOG_1", None),
    ("ctsp_drr_obl2__CTSP_VERSE_verse004_p0", None), ("LAT236PS_000001", None), ("000001", "lat236"),
    ("NHANESPS_C00156", None), ("C00156", "nhanes"), ("video_panels_med:jlwuTgJIilo_00012__right", None),
    ("vindr_pseudo__VINDRPS_0036129847a418b87f0882c991fdb089", None))]
check([g and g["key"] for g in got2] == ["ts:s0001", "verse:verse533", "ctsp:0149", "verse:verse004", "lat236:000001",
                                          "lat236:000001", "nhanes:00156", "nhanes:00156", "fluorocap_video:jlwuTgJIilo",
                                          "vindr:0036129847a418b87f0882c991fdb089"],
      "second-run spellings key: view-only TS/VerSe renders, <bank>_drr__<case> stems, pseudo-labelled films meet "
      "their raw file's key")
check(CL.PK.key_any("CTSP_COLONOG_7")[0] is None, "a Dataset813 stem with no crosswalk is still refused")
check(CL._cli_all(CL.ShellEnv("/h").expand("x; py tools/make_context_crops.py --drr /a --drr /b --dst /c; echo --drr /z"),
                  "make_context_crops.py") == {"--drr": ["/a", "/b"], "--dst": ["/c"]},
      "a repeated flag keeps every value, and the command ends at its `;`")
check(CL._inner_command('J=$(sbatch -J x --wrap="py tools/t.py --a 1")', "tools/t.py") == "py tools/t.py --a 1",
      "the invocation inside --wrap=\"...\" is what is read")
fl = [x for x in CL.scan_launchers([SL], H, ("make_context_crops.py",)) if x["script"].endswith("fn_build.sh")]
check(sorted((x["args"]["--drr"], x["args"]["--dst"], x["called_at"]) for x in fl)
      == [(f"{H}/mendeley_drr", f"{H}/mendeley_fov96_ctx", 7), (f"{H}/vindr_pseudo", f"{H}/vindrps_fov96_ctx", 8)],
      "a builder inside a shell function is read once per call site, with that call's arguments bound")
env = CL.ShellEnv("/h")
for line in ["case $SLURM_ARRAY_TASK_ID in", "  0) TARGET=LSTV_flag; EXP=lstv_flag_v2 ;;",
             "  1) TARGET=TLTV_flag; EXP=tltv_flag_v2 ;;", "esac", "OUT=$HOME/x"]:
    env.feed(line)
check(CL.is_template(env.expand("$EXP")) and env.expand("$OUT") == "/h/x",
      "a variable set inside case arms stays symbolic; plain assignments expand")
repo = Path(R) / "repo"
(repo / "SchwingNet" / "results").mkdir(parents=True)
(repo / "slurm").mkdir()
(repo / "SchwingNet" / "results" / "r.json").write_text(json.dumps(
    {"weights": "/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt", "init": "yolo11m.pt"}))
(repo / "SchwingNet" / "NUMBERS.md").write_text("scored with `~/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt`\n")
(repo / "slurm" / "s.sh").write_text("RX=$HOME/spine-detector/runs/realxray\nW=$RX/rx_pooled_1024/weights/best.pt\n"
                                     "python x.py --weights $H/spine-detector/runs/pose/$RUN/weights/best.pt\n")
c = subprocess.run([sys.executable, str(TOOL), "collect", "--repo", str(repo), "--out", f"{R}/seed.json"],
                   capture_output=True, text=True)
sd = json.load(open(f"{R}/seed.json"))
check("/wsu/home/go/go24/go2432/spine-detector/runs/devcorpus/dc_P_pooled/weights/best.pt" in sd["seeds"]
      and "/wsu/home/go/go24/go2432/allspine_v9_fov96_ctx/runs/model_rung_1_aug2.pt" in sd["seeds"],
      "collect: result JSON paths and ~-paths in NUMBERS.md become seeds")
check("/wsu/home/go/go24/go2432/spine-detector/runs/realxray/rx_pooled_1024/weights/best.pt" in sd["seeds"],
      "collect: a launch-script path built from script variables is expanded")
check(any("{RUN}" in t["shown"] for t in sd["templates"]) and "yolo11m.pt" in sd["relative_names"],
      "collect: an unexpandable path is kept as a template, a bare name as a relative name -- neither dropped")
print(f"\nfixture kept at {R}")
print("failures:", bad)
sys.exit(1 if bad else 0)
