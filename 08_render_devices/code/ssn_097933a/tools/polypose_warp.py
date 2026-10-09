#!/usr/bin/env python
"""PolyPose's polyrigid transform used FORWARD on a full-size CT: per-body rigid motions in, one field out, and the CT,
the label map and the body mask sampled through that one field.

THE TRANSFORM IS PUBLISHED, NOT OURS (Gopalakrishnan, Dey, Golland, NeurIPS 2025, arXiv:2505.19256; pinned clone
909a9bb2 in ~/polypose). What this file calls, and from where:

  weights   polypose.weights.sdf.distance_transform_edt (cupy EDT, mm) and polypose.weights.weights.gravity
            (m_k / (1 + d_k^2)), normalised to a partition of unity -- compute_weights' own arithmetic
  blend     logs(x) = sum_k w_k(x) xi_k with xi_k = [poses_rot | poses_xyz] as polypose.warp.PolyRigid stores them
  exp       diffdrr.pose.convert(rot, xyz, parameterization="se3_log_map"), composed exactly as PolyRigid.pose:
            affine.compose(pose).compose(affine_inverse), i.e. voxel -> centred world -> move -> voxel
  frame     the centred world diffdrr.data.canonicalize builds (file affine minus torchio's get_center())

TWO DEPARTURES FROM CALLING PolyRigid.warp() AS SHIPPED, both measured, both stated in every manifest row:

  1. CHUNKED EVALUATION. PolyRigid.warp() builds a 4x4 per voxel for the whole grid at once; a 512 x 570 x 512 CT
     is 149 M voxels and would need ~40 GB for the exp-map intermediates alone. The same three lines run here on
     slabs of the flattened grid. `verify_equivalence` builds the actual PolyRigid class on a crop of the same case
     and requires the two fields to agree (max |d| <= 1e-3 voxel) before any volume is written.
  2. WEIGHTS ON THE MOVED BODIES. PolyPose computes w_k from the SOURCE label map, and the field is evaluated at
     OUTPUT voxels (a pull-back: output(x) = source(T(x))). In registration the motions are small and iterated, so
     the two frames nearly coincide. Here the upper spine moves 10-40 mm -- more than a vertebral body's height --
     and a moved T10 would sit where the source-frame weights belong to T11 or to soft tissue, so it would not be
     rigid. The weights are therefore computed on each body's RIGIDLY MOVED mask (its rigid target on the output
     grid), which is the frame the pull-back is evaluated in. `--weights-frame source` keeps PolyPose's choice, so
     the difference is measured on a real case, not asserted.

SAMPLING (one boundary convention everywhere, shared with tools/polypose_invariants.pullback_mask): a pull-back
coordinate c is inside the source grid iff -0.5 <= c < n - 0.5 on every axis; outside it the output is air
(-1024 HU) and background (label 0) -- the CT's field of view does not extend, so nothing is invented there and the
share of such voxels is reported. Labels and body masks: nearest neighbour. CT: cubic B-spline (order 3, one
prefilter, cupyx.scipy.ndimage on the GPU), because trilinear resampling at random sub-voxel phases lowers the
image noise by up to 3x and would make a warped CT recognisable by its smoothness; the noise ratio is measured and
recorded per row.
"""
from __future__ import annotations

import math
import time

import numpy as np

AIR_HU = -1024.0
DEFAULT_CHUNK = 1 << 22


# ------------------------------------------------------------------------------------------------ frames
def centred_affine(ct_path: str) -> tuple:
    """(A_c, isocenter): the voxel -> centred-world affine diffdrr.data.canonicalize gives this volume."""
    import torchio as tio
    img = tio.ScalarImage(ct_path)
    iso = np.asarray(img.get_center(), float)
    T = np.eye(4)
    T[:3, 3] = -iso
    return T @ np.asarray(img.affine, float), iso


def voxel_pullback(affine, T_world):
    """Output voxel -> source voxel for a rigid world motion T (source -> output): A^-1 T^-1 A."""
    A = np.asarray(affine, float)
    return np.linalg.inv(A) @ np.linalg.inv(np.asarray(T_world, float)) @ A


def logs_for(A_c, V_list):
    """The (K, 6) [rot | xyz] parameters PolyRigid would hold for voxel pull-back maps V_k, in the centred frame:
    P_k = A_c V_k A_c^-1, xi_k = se3_log_map(P_k^T) = [log_translation | log_rotation]."""
    import torch
    from diffdrr.pose import se3_log_map
    out = []
    for V in V_list:
        P = np.asarray(A_c, float) @ np.asarray(V, float) @ np.linalg.inv(np.asarray(A_c, float))
        xi = se3_log_map(torch.tensor(P, dtype=torch.float64)[None].mT)[0]
        out.append(torch.cat([xi[3:], xi[:3]]))
    return torch.stack(out).to(torch.float32)


# ------------------------------------------------------------------------------------------------ masks
def _bbox(mask_t):
    import torch
    idx = [torch.nonzero(mask_t.any(dim=tuple(d for d in range(3) if d != a))).flatten() for a in range(3)]
    if any(len(i) == 0 for i in idx):
        return None
    return [(int(i.min()), int(i.max()) + 1) for i in idx]


def pull_mask(src_mask_t, V, shape, pad=3):
    """The rigid target of a source mask on the output grid: output voxel x takes src_mask[round(V x)], with the
    shared boundary convention. Only the moved bbox is evaluated."""
    import torch
    dev = src_mask_t.device
    out = torch.zeros(shape, dtype=torch.bool, device=dev)
    bb = _bbox(src_mask_t)
    if bb is None:
        return out
    Vinv = np.linalg.inv(np.asarray(V, float))                    # source voxel -> output voxel
    corners = np.array([[bb[0][1] - 1 if (i & 1) else bb[0][0],
                         bb[1][1] - 1 if (i & 2) else bb[1][0],
                         bb[2][1] - 1 if (i & 4) else bb[2][0], 1.0] for i in range(8)], float).T
    oc = Vinv @ corners
    lo = np.maximum(0, np.floor(oc[:3].min(axis=1)).astype(int) - pad)
    hi = np.minimum(np.asarray(shape), np.ceil(oc[:3].max(axis=1)).astype(int) + 1 + pad)
    if np.any(hi <= lo):
        return out
    gx, gy, gz = (torch.arange(int(l), int(h), device=dev, dtype=torch.float64) for l, h in zip(lo, hi))
    X, Y, Z = torch.meshgrid(gx, gy, gz, indexing="ij")
    Vt = torch.tensor(np.asarray(V, float), device=dev)
    sx = Vt[0, 0] * X + Vt[0, 1] * Y + Vt[0, 2] * Z + Vt[0, 3]
    sy = Vt[1, 0] * X + Vt[1, 1] * Y + Vt[1, 2] * Z + Vt[1, 3]
    sz = Vt[2, 0] * X + Vt[2, 1] * Y + Vt[2, 2] * Z + Vt[2, 3]
    n = src_mask_t.shape
    ok = (sx >= -0.5) & (sx < n[0] - 0.5) & (sy >= -0.5) & (sy < n[1] - 0.5) & (sz >= -0.5) & (sz < n[2] - 0.5)
    ix = torch.clamp(torch.round(sx), 0, n[0] - 1).long()
    iy = torch.clamp(torch.round(sy), 0, n[1] - 1).long()
    iz = torch.clamp(torch.round(sz), 0, n[2] - 1).long()
    vals = src_mask_t[ix, iy, iz] & ok
    out[int(lo[0]):int(hi[0]), int(lo[1]):int(hi[1]), int(lo[2]):int(hi[2])] = vals
    return out


# ------------------------------------------------------------------------------------------------ weights
def polyrigid_weights(label_t, bodies, spacing, frame="moved", log=print, kernel="gravity"):
    """Normalised gravity weights (K, X, Y, Z) float32 on the label's device, PolyPose's kernel. `bodies` is a list
    of (ids, V) with V the body's voxel pull-back. Returns (W, masses, per-body facts)."""
    import torch
    from polypose.weights.sdf import distance_transform_edt
    from polypose.weights.weights import gravity, inverse_distance
    shape = tuple(label_t.shape)
    masks_src, facts = [], []
    for ids, V in bodies:
        m = torch.zeros(shape, dtype=torch.bool, device=label_t.device)
        for i in ids:
            m |= label_t == int(i)
        masks_src.append(m)
    counts = torch.tensor([float(m.sum()) for m in masks_src], dtype=torch.float64)
    if (counts == 0).any():
        raise ValueError(f"a body has no voxels: {[b[0] for b, c in zip(bodies, counts) if c == 0]}")
    masses = counts / counts.sum()
    W = torch.empty((len(bodies),) + shape, dtype=torch.float32, device=label_t.device)
    moved_union = torch.zeros(shape, dtype=torch.int16, device=label_t.device)
    for k, ((ids, V), m) in enumerate(zip(bodies, masks_src)):
        t0 = time.time()
        mk = pull_mask(m, V, shape) if frame == "moved" else m
        moved_union += mk.to(torch.int16)
        # PolyPose's own EDT, called with a CUDA uint8 tensor: cupy 13.6 cannot take a CUDA *bool* tensor (it falls
        # back to __array__ and torch refuses; PolyPose itself only ever passes CPU masks). Nonzero = the voxels to
        # measure from, exactly as with ~structure.
        if mk.is_cuda:
            D = distance_transform_edt((~mk).to(torch.uint8), spacing=tuple(float(s) for s in spacing))
        else:
            # the CPU path: scipy's EDT, the computation cupyx's performs (POLYPOSE_API.md section 3)
            from scipy import ndimage as _ndi
            D = torch.from_numpy(_ndi.distance_transform_edt(~mk.numpy(), sampling=tuple(float(s) for s in spacing)))
        # PolyPose's two distance kernels (weights.py): 'gravity' m_k / (1 + d^2), the paper's; 'invdf:<eps>'
        # 1 / (eps d^2 + 1), mass-free, one smoothness knob
        if kernel == "gravity":
            W[k] = gravity(D, float(masses[k])).to(torch.float32)
        else:
            W[k] = inverse_distance(D, float(kernel.split(":", 1)[1])).to(torch.float32)
        facts.append(dict(ids=[int(i) for i in ids], voxels=int(counts[k]), mass=round(float(masses[k]), 6),
                          moved_voxels=int(mk.sum()), seconds=round(time.time() - t0, 2)))
        del D, mk
    W /= W.sum(dim=0, keepdim=True)
    overlap = int((moved_union > 1).sum())
    return W, masses, dict(bodies=facts, moved_overlap_voxels=overlap, frame=frame, kernel=kernel,
                           edt="polypose.weights.sdf (cupyx)" if label_t.is_cuda else "scipy.ndimage.distance_transform_edt")


# ------------------------------------------------------------------------------------------------ the field
def polyrigid_coords(W, poses, A_c, shape, chunk=DEFAULT_CHUNK):
    """Pull-back coordinates (N, 3) float32 (voxel index units, NIfTI order) for every output voxel: PolyRigid.pose
    evaluated on slabs of the flattened grid. `poses` is (K, 6) [rot | xyz]."""
    import torch
    from diffdrr.pose import RigidTransform, convert
    dev = W.device
    K = W.shape[0]
    Wf = W.reshape(K, -1)
    N = Wf.shape[1]
    A = RigidTransform(torch.tensor(np.asarray(A_c, float), dtype=torch.float32, device=dev)[None])
    # the TRUE matrix inverse, as DRR._affine_inverse is (drr.py: self._affine.inverse()). RigidTransform.inverse() is
    # the closed-form RIGID inverse (R^T, -R^T t), wrong for a voxel affine that carries spacing and the PIR
    # permutation: the first version used it and verify_equivalence caught the field 27 voxels off the class (0874).
    Ainv = RigidTransform(torch.linalg.inv(A.matrix[0].double()).to(torch.float32)[None])
    P = poses.to(dev)
    X, Y, Z = shape
    out = torch.empty((N, 3), dtype=torch.float32, device=dev)
    for s in range(0, N, chunk):
        e = min(N, s + chunk)
        lin = torch.arange(s, e, device=dev)
        pts = torch.stack([lin // (Y * Z), (lin // Z) % Y, lin % Z], dim=-1).to(torch.float32)
        logs = torch.einsum("cn,ck->nk", Wf[:, s:e], P)
        pose = convert(*logs.split([3, 3], dim=1), parameterization="se3_log_map")
        T = A.compose(pose).compose(Ainv)
        out[s:e] = T(pts.reshape(-1, 1, 3)).reshape(-1, 3)
        del lin, pts, logs, pose, T
    return out


# ------------------------------------------------------------------------------------------------ sampling
def inside(coords, shape):
    import torch
    n = torch.tensor(shape, device=coords.device, dtype=coords.dtype)
    return ((coords >= -0.5) & (coords < n - 0.5)).all(dim=-1)


def sample_nearest(vol_t, coords, shape, chunk=DEFAULT_CHUNK):
    """vol_t (X,Y,Z) integer tensor sampled at coords (N,3) by nearest neighbour; outside the grid -> 0."""
    import torch
    out = torch.zeros(coords.shape[0], dtype=vol_t.dtype, device=vol_t.device)
    for s in range(0, coords.shape[0], chunk):
        c = coords[s:s + chunk]
        ok = inside(c, shape)
        ix = torch.clamp(torch.round(c[:, 0]), 0, shape[0] - 1).long()
        iy = torch.clamp(torch.round(c[:, 1]), 0, shape[1] - 1).long()
        iz = torch.clamp(torch.round(c[:, 2]), 0, shape[2] - 1).long()
        v = vol_t[ix, iy, iz]
        v[~ok] = 0
        out[s:s + chunk] = v
    return out.reshape(shape)


def sample_cubic(ct_np, coords, shape, fill=AIR_HU, chunk=DEFAULT_CHUNK):
    """Cubic B-spline sample of the CT at coords (torch (N,3)), prefilter once; outside -> fill. cupyx on the GPU,
    scipy.ndimage on the CPU (the same spline, mode and prefilter)."""
    if not coords.is_cuda:
        from scipy import ndimage as nd
        coef = nd.spline_filter(np.asarray(ct_np, np.float32), order=3, output=np.float32, mode="nearest")
        out = np.empty(coords.shape[0], np.float32)
        for s in range(0, coords.shape[0], chunk):
            c = coords[s:s + chunk]
            ok = inside(c, shape).numpy()
            v = nd.map_coordinates(coef, c.T.contiguous().numpy(), order=3, mode="nearest", prefilter=False)
            v[~ok] = fill
            out[s:s + chunk] = v
        return out.reshape(shape)
    import cupy as cp
    import torch
    from cupyx.scipy import ndimage as cnd
    vol = cp.asarray(np.asarray(ct_np, np.float32))
    coef = cnd.spline_filter(vol, order=3, output=cp.float32, mode="nearest")
    del vol
    out = cp.empty(coords.shape[0], dtype=cp.float32)
    for s in range(0, coords.shape[0], chunk):
        c = coords[s:s + chunk]
        ok = cp.asarray(inside(c, shape).to(torch.uint8)).astype(cp.bool_)     # no CUDA bool across the torch/cupy boundary
        cc = cp.asarray(c.T.contiguous())
        v = cnd.map_coordinates(coef, cc, order=3, mode="nearest", prefilter=False)
        v[~ok] = fill
        out[s:s + chunk] = v
        del cc, v, ok
    del coef
    res = cp.asnumpy(out).reshape(shape)
    del out
    cp.get_default_memory_pool().free_all_blocks()
    torch.cuda.empty_cache()
    return res


# ------------------------------------------------------------------------------------------------ one call
def warp_volumes(ct_np, label_np, body_np, affine, A_c, spacing, bodies, frame="moved", chunk=DEFAULT_CHUNK,
                 device="cuda", log=print, kernel="gravity"):
    """The whole forward warp. `bodies` = [(ids, T_world)] with T_world the 4x4 source -> output motion of that body
    in FILE world mm. Returns dict(ct, label, body, disp (3,X,Y,Z) float32, facts)."""
    import torch
    t0 = time.time()
    shape = tuple(label_np.shape)
    lab_t = torch.as_tensor(np.asarray(label_np).astype(np.int32), device=device)
    V_list = [voxel_pullback(affine, T) for _, T in bodies]
    W, masses, wf = polyrigid_weights(lab_t, [(ids, V) for (ids, _), V in zip(bodies, V_list)], spacing, frame=frame, log=log, kernel=kernel)
    t_w = time.time() - t0
    poses = logs_for(A_c, V_list)
    coords = polyrigid_coords(W, poses, A_c, shape, chunk=chunk)
    del W
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    t_f = time.time() - t0 - t_w
    fov_out = ~inside(coords, shape)
    out_label = sample_nearest(lab_t, coords, shape, chunk).cpu().numpy()
    body_t = torch.as_tensor(np.asarray(body_np).astype(np.int32), device=device)
    out_body = sample_nearest(body_t, coords, shape, chunk).cpu().numpy()
    del body_t, lab_t
    out_ct = sample_cubic(ct_np, coords, shape)
    fov_out_np = fov_out.reshape(shape).cpu().numpy()
    X, Y, Z = shape
    grid = np.stack(np.meshgrid(np.arange(X, dtype=np.float32), np.arange(Y, dtype=np.float32),
                                np.arange(Z, dtype=np.float32), indexing="ij"), axis=0)
    disp = coords.reshape(X, Y, Z, 3).permute(3, 0, 1, 2).cpu().numpy() - grid
    del coords, grid
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    facts = dict(device=str(device), weights=wf, poses_rot_xyz=poses.tolist(), seconds_weights=round(t_w, 1), seconds_field=round(t_f, 1),
                 seconds_total=round(time.time() - t0, 1), fov_out_voxels=int(fov_out_np.sum()),
                 disp_max_vox=float(np.abs(disp).max()), gpu=torch.cuda.get_device_name(0) if str(device).startswith("cuda") else None)
    return dict(ct=out_ct, label=out_label, body=out_body, disp=disp.astype(np.float32), fov_out=fov_out_np, facts=facts)


# ------------------------------------------------------------------------------------------------ outside check
def verify_equivalence(ct_path, label_path, bodies_T, affine_file, crop_centre_vox, size=64, device="cuda", tmpdir=None, kernel="gravity"):
    """Run the actual polypose.warp.PolyRigid class and this file's chunked evaluator on the same crop of the same
    case, with the same weights and poses, and return the largest coordinate difference (voxels). A frame, a compose
    order or an axis order that differed from the class would show here as a difference of voxels, not 1e-5."""
    import os
    import tempfile
    import nibabel as nib
    import torch
    from diffdrr.data import read
    from diffdrr.drr import DRR
    from polypose.warp import PolyRigid
    ct = nib.load(ct_path)
    lb = nib.load(label_path)
    c = np.asarray(crop_centre_vox, int)
    lo = np.maximum(0, c - size // 2)
    hi = np.minimum(np.asarray(lb.shape), lo + size)
    lo = np.maximum(0, hi - size)
    sl = tuple(slice(int(a), int(b)) for a, b in zip(lo, hi))
    A = np.asarray(affine_file, float)
    Ac = A.copy()
    Ac[:3, 3] = A[:3, :3] @ lo + A[:3, 3]                      # crop affine: voxel 0 of the crop = voxel lo
    d = tempfile.mkdtemp(dir=tmpdir)
    cp_, lp_ = os.path.join(d, "ct.nii.gz"), os.path.join(d, "lab.nii.gz")
    nib.save(nib.Nifti1Image(np.asarray(ct.dataobj)[sl].astype(np.float32), Ac), cp_)
    lab = np.asarray(lb.dataobj)[sl].astype(np.int16)
    nib.save(nib.Nifti1Image(lab, Ac), lp_)
    # the crop keeps only the bodies present in it
    present = set(np.unique(lab).tolist())
    keep = [(ids, T) for ids, T in bodies_T if any(i in present for i in ids)]
    subject = read(cp_, lp_, orientation=None)
    drr = DRR(subject, sdd=1020.0, height=16, delx=8.0).to(device)
    A_c_class = drr.affine.matrix[0].detach().cpu().double().numpy()
    A_c_mine, _ = centred_affine(cp_)
    zooms = nib.load(cp_).header.get_zooms()[:3]
    lab_t = torch.as_tensor(lab.astype(np.int32), device=device)
    V_list = [voxel_pullback(Ac, T) for _, T in keep]
    W, _, _ = polyrigid_weights(lab_t, [(ids, V) for (ids, _), V in zip(keep, V_list)], zooms, frame="moved", kernel=kernel)
    poses = logs_for(A_c_mine, V_list)
    model = PolyRigid(drr, W).to(device)
    with torch.no_grad():
        model.poses_rot.data[:] = poses[:, :3].to(device)
        model.poses_xyz.data[:] = poses[:, 3:].to(device)
        ref = model.warp()[0].reshape(-1, 3)
    mine = polyrigid_coords(W, poses, A_c_mine, lab.shape, chunk=1 << 15)
    diff = float((ref - mine).abs().max())
    return dict(crop_lo=lo.tolist(), crop_shape=list(lab.shape), bodies_in_crop=len(keep),
                affine_centred_max_abs_diff=float(np.abs(A_c_class - A_c_mine).max()),
                max_coord_diff_vox=diff, max_disp_vox=float((ref - torch.stack(torch.meshgrid(
                    *(torch.arange(n, device=device, dtype=torch.float32) for n in lab.shape), indexing="ij"), -1).reshape(-1, 3)).abs().max()),
                ok=bool(diff <= 1e-3 and np.abs(A_c_class - A_c_mine).max() <= 1e-4))
