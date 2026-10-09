# PolyPose as a generator: the polyrigid transform, read from the code

What this is: the exact mechanics of the transform class in `github.com/eigenvivek/polypose` (Gopalakrishnan,
Dey, Golland, *PolyPose: Deformable 2D/3D registration via polyrigid transformations*, NeurIPS 2025,
arXiv:2505.19256, MIT licence), read from the pinned source, for using it **forward** — per-bone rigid motions
chosen by us, one smooth field, CT and labels warped through the same field. Every statement below names the
file it comes from. Where a statement was checked by running the code, the measurement is in
`REPRODUCTION.md` (`tools/polypose_forward_test.py`) and is quoted here with the marker **[measured]**;
anything without that marker is a reading of the code, not a test of it.

Pinned identity (from `slurm/env/polypose.setup_status.json`):

| item | value |
|---|---|
| repository | `https://github.com/eigenvivek/polypose`, commit `909a9bb2eeccf05065c7bc1d3703fb99f87b35b9` (main, 2025-10-22, "Add DeepFluoro experiment scripts (#17)"); no tagged release exists |
| lock | `uv.lock` in the repo; python 3.10; `torch==2.4.1` (PyPI cu121 build), `diffdrr==0.6.0`, `xvr @ git+https://github.com/eigenvivek/xvr.git@3e0b26eb51ef4a9c37615611bb05e0e200e48092`, `cupy-cuda12x==13.6.0`, `monai==1.5.1`, `torchio==0.20.22`, `jaxtyping==0.3.3`, `numpy==2.2.6`, `scipy==1.15.3`, `nibabel==5.3.2`, `SimpleITK==2.5.2`, `antspyx==0.6.1`, `kornia==0.8.1` |
| grid env | `/rs/rs_grp_oschome/go2432/data/polypose/env/venv` (uv, `--frozen` from that lock); export in `slurm/env/polypose.yml`, `polypose.requirements.lock.txt` (with hashes), `polypose.freeze.txt`; env hash = sha256 of the freeze file |
| package | `src/polypose/`: `warp/{warp,polyrigid,se3field,nonrigid}.py`, `weights/{weights,sdf}.py`, `models/{renderer,polypose,densese3,densexyz}.py`, `loss/{loss,regularizers}.py`, `plot/plot.py`, `utils/ants.py` |
| data used to reproduce | HF dataset `eigenvivek/xvr-data`, `deepfluoro/subject01..06/{volume.nii.gz, mask.nii.gz, xrays/NNN.{dcm,pt}, segmentations/NNN.pt}` (CC BY-NC-ND 4.0), the authors' packaging of Grupp's six specimens |

**Caution — the packaged poses.** As shipped, each `xrays/NNN.pt` pose puts the CT **behind** the X-ray source in
diffdrr's geometry (every ray's box intersection at α ∈ [−0.83, −0.63]): the trilinear renderer, which integrates
α ∈ [0, 1], returns exactly zero, and the public experiment scripts fit against black images. Right-multiply each
pose by `diag(-1,-1,1,1)` (the DeepFluoro rot-180 convention) before use — measured in `diag/drr_diag{,2,3}.json`
(NCC vs real 0.13 → 0.71, GT outline aligned) and applied as the one recorded deviation
(`slurm/env/polypose.pose_flip.diff`); with it, the paper's Table-1 numbers reproduce (`REPRODUCTION.md`). This
caveat is irrelevant to generative use, which chooses its own motions and never touches the packaged poses.

---

## 1. The transform, as implemented

`src/polypose/warp/polyrigid.py`, class `PolyRigid(Warp)`:

```python
poses = torch.concat([self.poses_rot, self.poses_xyz], dim=-1)            # (K, 6): per body, se(3) log
logs  = torch.einsum("cdhw,cn->dhwn", self.weights, poses).reshape(-1, 6)  # (N, 6): weighted mean of logs per voxel
pose  = convert(*logs.split([3, 3], dim=1), parameterization="se3_log_map")  # (N, 4, 4): exp map per voxel
return self.drr.affine.compose(pose).compose(self.drr.affine_inverse)       # voxel -> world -> move -> voxel
```

So for K rigid bodies with logs $\xi_k = (\omega_k, u_k) \in \mathfrak{se}(3)$ and per-voxel weights
$w_k(\mathbf x)$ that sum to 1 (`normalize=True`, default), the map at voxel $\mathbf x$ is

$$\bar T(\mathbf x) = \exp\Big(\sum_{k=1}^{K} w_k(\mathbf x)\, \xi_k\Big) \in SE(3),$$

paper eq. (4): a **log-Euclidean** poly-rigid fusion (Arsigny's 2003/2006 fusion in the Lie algebra, not the
ODE-integrated 2009 flow). Consequences of that choice:

- There is **no** integration step and no regulariser; the field is one algebraic expression of K six-vectors.
- Invertibility is **not** a theorem here. The fused log is a convex combination, so where the $\xi_k$ are small
  the exp is close to identity and folds do not occur; the paper's 0.00 % folds is an empirical number, and our
  gate (5) must measure it on every output rather than assume it. **[measured]** see `REPRODUCTION.md` T1/T3.
- The fused transform inside a body is $\exp(w_k \xi_k + \sum_{j\neq k} w_j \xi_j)$, so a body is exactly rigid
  **only where $w_k = 1$**. With the gravity kernel that is nowhere (section 3); the departure is what the
  per-body Dice-against-rigid gate measures.

`convert(..., parameterization="se3_log_map")` is DiffDRR's (`diffdrr/pose.py` l.167): it concatenates
`[translation, rotation]`, runs the pytorch3d-style `se3_exp_map` (row-vector convention) and transposes, so the
result is an ordinary column-vector 4×4. **The order of the two 3-vectors differs between the two APIs**:
`PolyRigid` stores `(poses_rot, poses_xyz)`; `se3_log_map` returns `[log_translation | log_rotation]`. The
translation part of an se(3) log is $V^{-1} t$, **not** the Euclidean translation $t$ (they coincide only for
zero rotation), so never write a millimetre offset straight into `poses_xyz` when a rotation is also present —
go through the log map (section 5).

`convert` rebuilds a 4×4 per voxel: N × 16 floats plus the exp-map intermediates. For a 1 mm DeepFluoro volume
(shape **[measured]**) this ran on a 48 GB L40S; the authors state ≥ 24 GB VRAM for the tutorial.

## 2. Coordinates — which frame the logs live in, and which way the bone moves

`src/polypose/warp/warp.py`, `Warp.__init__`:

- `drr.density` / `drr.mask` are torchio arrays in NIfTI index order (X, Y, Z); they are permuted to (Z, Y, X)
  for `grid_sample`. The variables are then unpacked as `*_, W, H, D = density.shape`, i.e. **D = X-size,
  H = Y-size, W = Z-size** (the names are back to front, harmlessly).
- `pts = meshgrid(arange(D), arange(H), arange(W))` stacked as `[X, Y, Z]`: the identity points are **voxel
  indices (i, j, k) in NIfTI order**, shape (X, Y, Z, 3), no half-voxel, no spacing.
- `drr.affine` (`diffdrr/drr.py` l.72) is `subject.volume.affine` as a `RigidTransform`: voxel index → world mm.
  That affine is the file affine **after `diffdrr.data.read()` → `canonicalize()`** (`diffdrr/data.py` l.139,
  200), which subtracts the volume's isocentre so that **world origin = volume centre**. No reorientation to
  RAS is performed on the data (torchio keeps the file's axes); the `orientation="AP"/"PA"` argument only builds
  the detector's `reorient` matrix and never touches the affine or the arrays. `read_kwargs["resample_target"]`
  (mm) resamples through torchio before anything else — the weights are computed on whatever grid the subject
  has when `compute_weights` is called and then trilinearly interpolated to the DRR grid in `PolyRigid.__init__`.
- Therefore **every $\xi_k$ is a motion about the volume centre, in the file's world axes (mm)**. A rotation of a
  bone "about itself" must be composed as $M = T(c_k)\,R\,T(-c_k)$ with $c_k$ the bone centroid in that centred
  world frame (`drr.affine.matrix[0] @ [i, j, k, 1]`), then logged.

`Warp.warp()` returns `pose(pts)`: the identity voxel points pushed through
$A \bar T A^{-1}$ — **the position each output voxel samples from**. `Warp.forward` / `warp_subject` then call
`F.grid_sample(input, normalize(warp()))`. That is a **pull-back**: `output(x) = input(A⁻¹ T̄(A x))`. A body
whose log is $\xi_k = \log M$ therefore **appears moved by $M^{-1}$** in the output. To realise a chosen physical
motion $M_k$ of body k, store $\log(M_k^{-1}) = -\log(M_k)$ (negating a Lie-algebra element inverts the
element it exponentiates). **[measured]** T1 in `REPRODUCTION.md` settles this with Dice under both
hypotheses and the world centroid of the moved femur.

## 3. The weights — kernel, "mass", and what controls smoothness

`src/polypose/weights/weights.py`, `compute_weights(subject, labels, weightfn="gravity", normalize=True, **kwargs)`:

```
for each body k = union of the listed label ids            (labels: list[int] or list[list[int]])
    structure_k = (mask ∈ ids_k)          skipped SILENTLY if empty (commit c8addb4) -> K shrinks, indices shift
    d_k(x)      = EDT(~structure_k, sampling=spacing)   Euclidean distance in mm to the body, 0 inside  (cupy, GPU)
                  (weightfn="exp" uses the SIGNED distance: negative inside)
m_k = |structure_k| / Σ_j |structure_j|                  "mass" = voxel-count fraction (uniform density assumed)
gravity : w_k(x) = m_k / (1 + d_k(x)²)                    paper eq. (6); NO free parameter
invdf   : w_k(x) = 1 / (eps · d_k(x)² + 1)                eps [mm⁻²] is the one smoothness knob
exp     : w_k(x) = exp(eps · sdf_k(x))                    with sdf < 0 inside; eps must be NEGATIVE for a decay
normalize: w_k(x) /= Σ_j w_j(x)                           partition of unity (a voxel far from every body still moves
                                                          by the mass-weighted mean of all logs)
returns (segmentations: int (X,Y,Z) with body index 1..K, weights: float32 (K, X, Y, Z))
```

What that means for control:

- **Rigidity inside a body.** At a voxel inside body k, $d_k = 0$, so its own normalised weight is
  $w_k = m_k \big/ \big(m_k + \sum_{j \ne k} m_j/(1+d_j^2)\big) < 1$. A small body touching a large one is the
  worst case: a femoral head 3 mm from the pelvis (mass ≈ 0.8) against its own mass ≈ 0.1 gets
  $w \approx 0.1/(0.1 + 0.8/10) = 0.56$ — the head is blended, not rigid. Adjacent vertebrae of equal mass 5 mm
  apart give $w \approx 1/(1 + 1/26) = 0.96$ at the end plate. **[measured]** T2 quantifies this per body for
  the 3-body and 7-body groupings and three kernels.
- **The only knobs are the grouping, the kernel and (for `invdf`) eps.** Gravity has no parameter: the
  blend band is set by geometry and by the mass ratio. Larger `invdf` eps → sharper decay → more rigid bodies
  and a thinner blend band (and, past some point, folds where two bodies rotate against each other); eps → 0 →
  every voxel takes the plain mean of all logs (one global rigid motion).
- **Grouping is the fusion rule.** Bodies are unions of label ids, so a fused or sacralised junction is
  expressed by listing its ids in **one** body (hard rule 1): the fused unit then has one $\xi$ and zero relative
  motion by construction, to numerical precision.
- **Check K.** Because absent labels are dropped silently, assert `int(segmentations.max()) == len(bodies)`
  before indexing `poses_rot[k]`; with v11 labels (`ostk.labels.labels_for(volume)`, never a fixed map) a
  missing femur or an FOV-cut vertebra would otherwise shift every index after it.
- **GPU is required** for the EDT (`cupyx.scipy.ndimage.distance_transform_edt`); `scipy.ndimage.distance_transform_edt(~structure, sampling=spacing)`
  is the identical CPU computation if needed.
- **Memory** is K × N float32 for the weights (K = 12 bodies on a 512×512×400 grid = 5 GB) plus the per-voxel
  4×4 of section 1.

## 4. Applying one field to the image AND the label (and anything else)

`src/polypose/warp/warp.py`:

```python
def forward(self):                    # used during registration (density for the renderer)
    pts = self.normalize(self.warp())                     # 2*x/shape - 1, align_corners=False
    warped_density = grid_sample(density, pts, mode="bilinear", padding_mode="border", align_corners=False)
    warped_mask    = grid_sample(mask,    pts, mode="nearest",                        align_corners=False)

@torch.no_grad
def warp_subject(self):               # used to write outputs: HU volume + labels
    pts = self.normalize(self.warp())
    return _warp_volume(self.volume, pts), _warp_mask(self.mask, pts)
```

- The image and the label are sampled from **the same `pts` tensor**, so they share the field by construction.
  `DeformableRenderer.warp_subject(affine=...)` (`models/renderer.py`) wraps them as `torchio.ScalarImage`
  (float32 HU) and `torchio.LabelMap` (uint8) with whatever affine is passed — the authors pass the **original
  file affine** (`run.py: ScalarImage(volume).affine`), so the written NIfTI has the input's affine and axes
  (no reorientation on write). **[measured]** T3 re-reads the saved files and compares affine and axcodes.
- **Any further map** (the SPINEPS body mask, a second label set, a distance map) goes through the same field by
  reusing the grid: take `pts = model.warp.warp()`, normalise the same way, feed the extra array permuted
  (2, 1, 0) as `(1, 1, Z, Y, X)`, and `grid_sample(..., mode="nearest" or "bilinear")`; the output comes back in
  (X, Y, Z) order. The field itself, in voxel displacement units, is `model.warp.warp()[0] - model.warp.pts`,
  and in mm it is that displacement mapped through the affine's linear part.
- **Half-voxel offset in the sampler.** `normalize` maps index $x$ to $2x/\text{size} - 1$ while `grid_sample` with
  `align_corners=False` places voxel centre $i$ at $(2i+1)/\text{size} - 1$. The identity warp therefore samples
  each voxel at $i - \tfrac12$: the image is blurred by a half-voxel bilinear shift and the nearest-neighbour
  label rounds ties. This is invisible at the paper's 1.56 mm detector pixels but is not acceptable for a
  label-adherence gate at 0.98 Dice; the corrected normalisation is $(2x+1)/\text{size} - 1$. **[measured]** T0
  reports the identity mismatch for both normalisations.
- The label is warped with `mode="nearest"`; partial-volume mixing between two labels in the blend band is
  therefore impossible (a voxel is one id), but a label can be **stretched or compressed** there.

## 5. Recipe: from per-body world transforms to a warped CT + labels

```python
from diffdrr.data import read
from diffdrr.drr import DRR
from diffdrr.pose import se3_log_map
from polypose import PolyPose
from polypose.weights import compute_weights

subject = read(ct_nii, label_nii, orientation=None, bone_attenuation_multiplier=1.0)   # torchio; centres the world
bodies  = [[20], [21], [22], [23], [24], [26], [30], [31], [32], [33]]   # ids from ostk.labels.labels_for(volume);
                                                                         # a fused junction = ONE list, e.g. [24, 26]
segs, W = compute_weights(subject, bodies)                               # gravity kernel; W: (K, X, Y, Z)
assert int(segs.max()) == len(bodies), "a body had no voxels and was dropped"
drr   = DRR(subject, sdd=1020.0, height=64, delx=2.0, renderer="trilinear")  # detector irrelevant; only affine/density/mask buffers are used
model = PolyPose(drr, W).cuda()
model.warp.poses_rot.data.zero_(); model.warp.poses_xyz.data.zero_()
A = model.drr.affine.matrix[0]                                           # voxel index -> centred world mm
for k, M_k in enumerate(desired_world_motions):                          # M_k: 4x4, column convention, about the world origin
    xi = se3_log_map(torch.linalg.inv(M_k)[None].mT)[0]                  # log of the INVERSE (pull-back), [xyz | rot]
    model.warp.poses_xyz.data[k] = xi[:3]; model.warp.poses_rot.data[k] = xi[3:]
hu, lab = model.warp_subject(affine=subject.volume.affine)               # same grid for both  (see the sampler note)
folds   = (model.warp.jacdet < 0).float().mean() * 100                   # authors' fold metric, %
```

The fold metric (`loss/regularizers.py::jacdet`) is a forward-difference determinant of `-warp()`. The three
row derivatives are stacked in the order (axis 1, axis 0, axis 2) — a row swap that flips the sign — and the
negation flips it back, so `jacdet < 0` does mark folds and the identity gives +1. **[measured]** T0 checks
the identity value and `tools/polypose_forward_test.py::independent_jacdet` recomputes the determinant with
`torch.gradient` in the natural order.

## 6. What the registration pipeline adds (for completeness; not used forward)

`experiments/deepfluoro/models.py::fit_polypose`: bodies `[[1,2,3,4,7],[5],[6]]` (pelvis+sacrum+vertebrae as
one rigid body, each femur its own), gravity weights, three-level pyramid `resample_target = 4, 2, None` mm ×
51 Adam iterations each (`lr` 1e-2 on `poses_rot`, 1e0 on `poses_xyz`, `maximize=True`), detector rescaled
to 0.125 (1436 px → 179 px, 1.556 mm/px), loss = 0.5·multiscale NCC (global + 9-px patches) + 0.5·gradient
NCC (11-px), two training views per subject, `torch.manual_seed(42)`. Evaluation (`eval.py`) is **2-D**: DRRs
of the warped volume per label channel at the ground-truth poses of the held-out views (frames 0–36 minus the
two training frames, minus frame 3 for subject 1), Dice/HD95 by monai against the 2-D ground-truth
segmentations resized to 179 px, structures under 500 px set to NaN; HD95 is in **pixels** (no spacing
passed). The paper's 0.99 / 0.98 / 0.98 Dice and 1.00 / 1.48 / 1.56 HD95 are those quantities.

## 7. Things a generative wrapper must do that the package does not

1. Use the corrected grid normalisation (section 4) or accept the half-voxel shift and document it.
2. Build the bodies from `ostk.labels.labels_for(volume)`; assert K; put every fused unit in one body.
3. Compose rotations about each body's centroid and store `log(M_k⁻¹)`; keep the pelvis (and everything the
   junction rules freeze) at $\xi = 0$ — with normalised weights those voxels still receive the mass-weighted
   mean of the *other* bodies' logs, attenuated by distance; the pelvic-incidence gate (rule 5) is what catches
   leakage, and a large `invdf` eps or an explicit "anchor" body with large mass reduces it.
4. Gate every output: fold fraction (both determinants), per-body Dice against `scipy.ndimage.affine_transform`
   of the original label under $A^{-1} M_k^{-1} A$, unmoved-body Dice against the original, the body mask through
   the same grid, a DRR rendered and looked at.
5. Record: source case + patient key, seed, the K logs (and the M_k they came from), polypose commit
   `909a9bb2…`, env hash, output sha256, the re-measured angles.
