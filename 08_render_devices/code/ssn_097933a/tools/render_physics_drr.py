"""Physics-lite cone-beam renders from labelled CT: perspective geometry, a polychromatic spectrum with three-material
attenuation, scatter, quantum noise, detector blur, collimation and image-intensifier vignetting.

What the parallel line integral (make_drr_dataset.drr) gets wrong about a C-arm frame, in order of size:
  1. geometry: a C-arm is a point source ~1000 mm from the detector with the patient ~600 mm from the source, so
     posterior and anterior structures magnify differently and the beam diverges (an L5 body near the detector is
     smaller than one near the source); here rays are cast from the source through every detector pixel
     (ray-marching with trilinear sampling on the GPU), with the pose (view angle, tilt, in-plane rotation,
     source-object distance, field size and centring) drawn per render;
  2. spectrum and beam hardening: an energy-integrating detector sees sum_E S(E) E exp(-sum mu(E) dl); with HU
     mapped to water and cortical-bone fractions and metal as a third material, mu(E) follows tabulated
     mass-attenuation shapes, so thick bone and metal harden the beam as they do in reality;
  3. scatter: a fraction of the primary, low-pass filtered (Gaussian, sigma ~ 1/20 of the field), added back;
  4. noise: Poisson at a photon budget drawn from a fluoroscopy-like range, then detector blur (MTF) and a
     log/display response with random gamma, plus round or rectangular collimation and radial vignetting.
Labels: every vertebra (and anchor) mask is projected with the same rays (max along the ray) to a silhouette box, so
the boxes match the perspective render exactly; a box that touches the detector edge is flagged `clipped`, because a
real C-arm field shows three or four vertebrae, not a whole spine. Output in the DRR-directory format (img/*.npy
uint8, ann/*.json) with the pose and every physics parameter recorded per image. Sources: the ctsp / verse /
totalseg / implant schemes of make_anchor_drr (label sets), one GPU, --shard i/n.

Two failures that produced a blank white frame and a crashed shard, fixed here and worth remembering: grid_sample
pads outside the volume with 0, which in HU is SOFT TISSUE, so every ray accumulated 300 mm of phantom water and the
image flattened to uniform grey - the volume is sampled shifted by +1000 so that the pad value is air; and the local
name `sid` was reused for the structure-id volume after being read as the source-image distance, which then went
into the JSON and killed the shard mid-write.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_anchor_drr import load_case, CLASSES  # noqa: E402

# linear attenuation (per cm) approximations vs energy (keV): water, cortical bone, titanium
ENERGIES = torch.tensor([40.0, 55.0, 70.0, 85.0, 100.0, 120.0])
SPECTRUM = torch.tensor([0.10, 0.25, 0.30, 0.20, 0.10, 0.05])           # a ~100 kVp tube with filtration, coarse
MU_WATER = torch.tensor([0.268, 0.227, 0.193, 0.178, 0.171, 0.162])
MU_BONE = torch.tensor([0.665, 0.416, 0.303, 0.246, 0.213, 0.190])       # cortical bone, per cm at 1.92 g/cm3
MU_TI = torch.tensor([12.0, 5.5, 2.9, 1.9, 1.4, 1.0])                     # titanium, per cm (4.5 g/cm3)
HU_SHIFT = 1000.0                                                         # sample vol + HU_SHIFT so the zero pad is air


def pir_zooms(img):
    """voxel size in millimetres along the PIR axes the loader produces.

    to_pir reorients but does NOT resample, so an anisotropic scan (VerSe sagittal acquisitions are commonly
    0.3 x 0.3 x 3 mm) keeps its anisotropy. Rendering such a volume with one mean spacing stretches it along the
    thick axis and the frame comes out as horizontal streaks with the anatomy smeared away."""
    import nibabel as nib
    z = np.asarray(img.header.get_zooms()[:3], np.float32)
    t = nib.orientations.ornt_transform(nib.orientations.io_orientation(img.affine),
                                        nib.orientations.axcodes2ornt(("P", "I", "R")))
    return np.array([z[int(t[i, 0])] for i in range(3)], np.float32)


MU_RATIO_E0 = 0.193 / 0.303          # water / cortical bone at 70 keV, from the tables above


def materials(hu: torch.Tensor):
    """HU -> (water-equivalent density, bone-equivalent fraction, metal fraction) per voxel.

    A Hounsfield unit is defined by mu(E0) = mu_water(E0) * (1 + HU/1000) at the scanner's effective energy, so a
    decomposition into water and bone basis materials should reproduce exactly that at E0 and then harden the beam
    correctly at the other energies. Water runs to 1.0 and everything above water is carried by the bone basis at
    `MU_RATIO_E0 * HU/1000`.

    The previous form clamped the water term at 1.2 and ramped bone from 150 HU over 1500. Checked against the HU
    definition on 15 September 2026, that was 4.4 to 4.5 per cent too attenuating for every voxel above 200 HU -
    a systematic bias in the direction of slightly too much bone contrast, not the loss of it. Small, but free to
    fix, and it removes a kink at 200 HU that no tissue has.
    """
    water = torch.clamp((hu + 1000.0) / 1000.0, 0.0, 1.0)
    bone = torch.clamp(hu, min=0.0) / 1000.0 * MU_RATIO_E0
    metal = torch.clamp((hu - 2500.0) / 5000.0, 0.0, 1.5)
    return water, bone, metal


def rot(axis, deg, dev):
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    m = torch.eye(3, device=dev)
    if axis == "y":
        m[0, 0], m[0, 2], m[2, 0], m[2, 2] = c, s, -s, c
    elif axis == "x":
        m[1, 1], m[1, 2], m[2, 1], m[2, 2] = c, -s, s, c
    else:
        m[0, 0], m[0, 1], m[1, 0], m[1, 1] = c, -s, s, c
    return m


def render(vol_pir: torch.Tensor, masks: list, vs_mm: float, rng: random.Random, det_px=640, det_mm=None, sid_mm=1000.0,
           sod_mm=None, view="lat", steps=None, chunk=16, preset="mixed"):
    """vol_pir: (P, I, R) float HU on the GPU. Returns image (det_px, det_px) in [0,1], per-mask boxes, meta."""
    dev = vol_pir.device; P, I, R = vol_pir.shape
    sod = sod_mm or rng.uniform(550.0, 780.0)
    det_mm = det_mm or rng.uniform(230.0, 430.0)             # 9 inch II to a wide flat panel
    sp = np.broadcast_to(np.asarray(vs_mm, np.float32).ravel(), (3,)).astype(np.float32)   # (P, I, R) mm per voxel
    # world frame: volume centred at origin, mm; x = R (left-right), y = I (superior-inferior, down), z = P (+posterior)
    ext = torch.tensor([float(R) * float(sp[2]), float(I) * float(sp[1]), float(P) * float(sp[0])], device=dev)
    yaw = {"lat": 90.0, "ap": 0.0}[view] + rng.uniform(-12.0, 12.0)     # around the SI axis
    tilt = rng.uniform(-8.0, 8.0)                                        # around the LR axis (cranio-caudal)
    roll = rng.uniform(-6.0, 6.0)                                        # in-plane
    Rm = rot("y", yaw, dev) @ rot("x", tilt, dev) @ rot("z", roll, dev)
    view_dir = Rm @ torch.tensor([0.0, 0.0, 1.0], device=dev)            # beam direction (anterior -> posterior for AP)
    up = Rm @ torch.tensor([0.0, 1.0, 0.0], device=dev); right = torch.cross(view_dir, up, dim=0)
    src = -view_dir * sod
    # where the field is centred, in the DETECTOR plane (not world axes): mostly along the spine
    off_u = rng.uniform(-0.10, 0.10) * float(ext[0]); off_v = rng.uniform(-0.38, 0.38) * float(ext[1])
    det_c = src + view_dir * sid_mm + right * off_u + up * off_v
    u = (torch.arange(det_px, device=dev) - det_px / 2 + 0.5) / det_px * det_mm
    gu, gv = torch.meshgrid(u, u, indexing="xy")
    pix = det_c[None, None] + gu[..., None] * right + gv[..., None] * up               # (H, W, 3) detector pixel positions
    dirs = pix - src; dirs = dirs / dirs.norm(dim=-1, keepdim=True)
    radius = float(ext.norm() / 2)
    t0 = max(0.0, sod - radius); t1 = sod + radius
    steps = steps or int(min(768, max(256, round((t1 - t0) / max(0.4, float(sp.min()) * 0.75)))))
    ts = torch.linspace(t0, t1, steps, device=dev)
    dl = (t1 - t0) / steps / 10.0                                                       # cm per sample
    water_acc = torch.zeros(det_px, det_px, device=dev); bone_acc = torch.zeros_like(water_acc); metal_acc = torch.zeros_like(water_acc)
    # one structure-id volume instead of one float volume per mask (30 masks x 600 MB was the memory failure)
    n_struct = len(masks); mask_max = [torch.zeros_like(water_acc) for _ in masks]
    struct = torch.zeros_like(vol_pir, dtype=torch.float32)
    for j, m in enumerate(masks):
        struct[m & (struct == 0)] = float(j + 1)
    vol5 = (vol_pir + HU_SHIFT)[None, None]     # (1,1,P,I,R): grid_sample coords are (x=R, y=I, z=P); zero pad == air
    str5 = struct[None, None]
    half = ext / 2
    for i in range(0, steps, chunk):
        tt = ts[i:i + chunk]; k = tt.numel()
        pts = src[None, None, None] + dirs[..., None, :] * tt[None, None, :, None]       # (H, W, k, 3) mm, x=R,y=I,z=P
        grid = (pts / half).clamp(-1.5, 1.5)
        g = grid.reshape(1, det_px, det_px * k, 1, 3)
        hu = F.grid_sample(vol5, g, mode="bilinear", padding_mode="zeros", align_corners=False).reshape(det_px, det_px, k) - HU_SHIFT
        w, b, m = materials(hu)
        water_acc += w.sum(-1) * dl; bone_acc += b.sum(-1) * dl; metal_acc += m.sum(-1) * dl
        smp = F.grid_sample(str5, g, mode="nearest", padding_mode="zeros", align_corners=False).reshape(det_px, det_px, k)
        present = set(torch.unique(smp).tolist())
        for j in range(n_struct):
            if float(j + 1) in present:
                mask_max[j] = torch.maximum(mask_max[j], (smp == float(j + 1)).float().amax(-1))
        del hu, w, b, m, smp, pts, grid, g
    E = ENERGIES.to(dev); S = SPECTRUM.to(dev); muw = MU_WATER.to(dev); mub = MU_BONE.to(dev); mut = MU_TI.to(dev)
    trans = torch.zeros_like(water_acc)
    for k in range(len(E)):
        trans += S[k] * E[k] * torch.exp(-(muw[k] * water_acc + mub[k] * bone_acc + mut[k] * metal_acc))
    trans = trans / (S * E).sum()
    # Scatter and photon budget, drawn per render from the acquisition being imitated. Measured on 15 September
    # 2026 against the tables above: on a lateral abdomen the primary behind the spine is about six times darker
    # than the primary through gas-filled bowel, so a scatter term that is a fraction of the GLOBALLY BLURRED
    # primary lands more signal at the vertebral body than the primary does. At the old draw of 0.15 to 0.45 the
    # scatter share at the spine was 50 to 82 per cent - the structure being classified was mostly a blurred copy
    # of the bowel beside it. A clinical grid leaves a scatter fraction of roughly 0.09 to 0.23, and fluoroscopy
    # without a grid rather more.
    # The photon budget was the other half of it: 300 to 4,000 incident photons leave 0.9 to 12 detected at the
    # spine, i.e. 29 to 106 per cent quantum noise on the vertebra. That is a fluoroscopic budget, and it was being
    # applied to every render including those meant to imitate a radiograph.
    mode = preset if preset != "mixed" else ("fluoro" if rng.random() < 0.4 else "radiograph")
    if mode == "fluoro":
        sf = rng.uniform(0.10, 0.30); n0 = rng.uniform(2.0e3, 4.0e4)      # photon-starved, no grid or a poor one
    else:
        sf = rng.uniform(0.03, 0.15); n0 = rng.uniform(1.0e5, 2.0e6)      # a radiograph behind a grid
    sigma = det_px / rng.uniform(12, 24)                                   # scatter: a blurred fraction of the primary
    ks = int(sigma * 3) | 1; xk = torch.arange(ks, device=dev) - ks // 2; g1 = torch.exp(-0.5 * (xk / sigma) ** 2); g1 = g1 / g1.sum()
    blur = F.conv2d(F.conv2d(trans[None, None], g1[None, None, None, :], padding=(0, ks // 2)), g1[None, None, :, None], padding=(ks // 2, 0))[0, 0]
    signal = (1 - sf) * trans + sf * blur
    counts = torch.poisson(signal.clamp_min(0) * n0) / n0
    sig2 = rng.uniform(0.6, 1.6); xk2 = torch.arange(7, device=dev) - 3; g2 = torch.exp(-0.5 * (xk2 / sig2) ** 2); g2 = g2 / g2.sum()
    counts = F.conv2d(F.conv2d(counts[None, None], g2[None, None, None, :], padding=(0, 3)), g2[None, None, :, None], padding=(3, 0))[0, 0]
    img = -torch.log(counts.clamp_min(1e-4))                                             # attenuation-like: bone bright
    lo, hi = torch.quantile(img.flatten(), 0.02), torch.quantile(img.flatten(), 0.995)
    img = ((img - lo) / (hi - lo + 1e-6)).clamp(0, 1) ** rng.uniform(0.7, 1.4)
    yy, xx = torch.meshgrid(torch.linspace(-1, 1, det_px, device=dev), torch.linspace(-1, 1, det_px, device=dev), indexing="ij")
    rr = torch.sqrt(yy ** 2 + xx ** 2)
    img = img * (1.0 - rng.uniform(0.0, 0.35) * rr ** 2)
    coll = "round" if rng.random() < 0.6 else "rect"
    if coll == "round":
        img = img * (rr <= rng.uniform(0.85, 1.0)).float()
    else:
        cx, cy = rng.uniform(0.55, 1.0), rng.uniform(0.55, 1.0); img = img * ((xx.abs() <= cx) & (yy.abs() <= cy)).float()
    boxes = []
    for mm in mask_max:
        ys, xs = torch.where(mm > 0.5)
        if len(ys) < 20:
            boxes.append(None); continue
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
        clipped = x0 <= 1 or y0 <= 1 or x1 >= det_px - 2 or y1 >= det_px - 2
        boxes.append({"box": [x0, y0, x1, y1], "clipped": bool(clipped), "px": int(len(ys))})
    meta = {"view": view, "yaw": yaw, "tilt": tilt, "roll": roll, "sod_mm": sod, "sid_mm": sid_mm, "det_mm": det_mm, "det_px": det_px, "voxel_mm_pir": [round(float(x), 4) for x in sp],
            "field_mm_at_isocentre": det_mm * sod / sid_mm, "offset_u_mm": off_u, "offset_v_mm": off_v, "steps": steps,
            "scatter_fraction": sf, "scatter_sigma_px": sigma, "photons_per_pixel": n0, "acquisition": mode, "detector_blur_sigma": sig2,
            "collimation": coll, "energies_keV": ENERGIES.tolist(), "spectrum": SPECTRUM.tolist()}
    return img, boxes, meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scheme", choices=["ctsp", "verse", "totalseg", "implant"], default="ctsp")
    ap.add_argument("--src", required=True); ap.add_argument("--dst", required=True)
    ap.add_argument("--per-case", type=int, default=2); ap.add_argument("--views", nargs="*", default=["lat", "ap"])
    ap.add_argument("--det-px", type=int, default=640); ap.add_argument("--det-mm", type=float, default=0.0, help="0 = draw per render")
    ap.add_argument("--preset", choices=["mixed", "radiograph", "fluoro"], default="mixed",
                    help="acquisition to imitate: a radiograph behind a grid, photon-starved fluoroscopy, or a per-render mix")
    ap.add_argument("--min-levels", type=int, default=2, help="drop a render with fewer unclipped vertebrae than this")
    ap.add_argument("--shard", default="0/1"); ap.add_argument("--seed", type=int, default=0); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--cases-file", default=None, help="one case id per line; renders only these (used to oversample L6/T13 and other rare anatomy)")
    a = ap.parse_args()
    si, sn = (int(x) for x in a.shard.split("/"))
    src, dst = Path(a.src).expanduser(), Path(a.dst).expanduser(); (dst / "img").mkdir(parents=True, exist_ok=True); (dst / "ann").mkdir(exist_ok=True)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    import nibabel as nib
    if a.scheme == "ctsp":
        cases = sorted(p.name.split("_")[0] for p in (src / "labels").glob("*_label.nii.gz"))
    elif a.scheme == "implant":
        cases = sorted(p.name.replace("_ct.nii.gz", "") for p in (src / "ct").glob("*_ct.nii.gz"))
    elif a.scheme == "verse":
        cases = sorted(p.name for p in src.iterdir() if p.is_dir() and (p / f"{p.name}_msk.nii.gz").exists())
    else:
        cases = sorted(p.name for p in src.iterdir() if p.is_dir() and (p / "ct.nii.gz").exists())
    if a.cases_file:
        want = {x.strip() for x in open(Path(a.cases_file).expanduser()) if x.strip()}
        cases = [c for c in cases if c in want or c.split("_v")[0] in want]
        print(f"cases-file kept {len(cases)} of {len(want)} requested ids", flush=True)
    if a.limit:
        cases = cases[: a.limit]
    cases = cases[si::sn]; n = 0; dropped = 0
    for k, cid in enumerate(cases):
        try:
            ct_pir, structs = load_case(a.scheme, src, cid)
            ctp = src / ("ct" if a.scheme in ("ctsp", "implant") else cid) / (f"{cid}_ct.nii.gz" if a.scheme in ("ctsp", "implant") else ("ct.nii.gz" if a.scheme == "totalseg" else f"{cid}_ct.nii.gz"))
            vs = pir_zooms(nib.load(str(ctp)))
        except Exception as e:  # noqa: BLE001
            print("skip", cid, repr(e)[:80], flush=True); continue
        # to_pir flips axes with negative strides; torch refuses those, so materialise contiguous copies
        vol = torch.from_numpy(np.ascontiguousarray(ct_pir, dtype=np.float32)).to(dev)
        masks = [torch.from_numpy(np.ascontiguousarray(m)).to(dev) for _, _, m in structs]
        for v in range(a.per_case):
            for view in a.views:
                rng = random.Random(f"{a.seed}:{cid}:{v}:{view}")
                with torch.no_grad():
                    img, boxes, meta = render(vol, masks, vs, rng, det_px=a.det_px, det_mm=(a.det_mm or None), view=view, preset=a.preset)
                levels = {}; anchors = []
                for (cls, vname, _), b in zip(structs, boxes):
                    if b is None:
                        continue
                    if cls == 0 and vname:
                        levels[vname] = {"name": vname, "box": b["box"], "clipped": b["clipped"], "px": b["px"]}
                    else:
                        anchors.append({"cls": CLASSES[cls], "box": b["box"], "clipped": b["clipped"]})
                if sum(0 if lv["clipped"] else 1 for lv in levels.values()) < a.min_levels:
                    dropped += 1; continue
                name = f"{a.scheme}_{cid}_{view}_p{v}"
                np.save(dst / "img" / f"{name}.npy", (img.cpu().numpy() * 255).astype(np.uint8))
                json.dump({"case": name, "source_case": cid, "scheme": a.scheme, "shape": [a.det_px, a.det_px], "axcodes": "film",
                           "levels": levels, "anchors": anchors, "physics": meta,
                           "renderer": "render_physics_drr v2 (cone-beam, 6-energy spectrum, water/bone/metal, scatter, Poisson, MTF, collimation, vignetting)"},
                          open(dst / "ann" / f"{name}.json", "w"))
                n += 1
        del vol, masks
        if dev == "cuda":
            torch.cuda.empty_cache()
        if k % 10 == 0:
            print(f"  {k}/{len(cases)} cases, {n} renders, {dropped} dropped", flush=True)
    print(f"shard {si}/{sn}: {n} renders, {dropped} dropped for too few unclipped vertebrae")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
