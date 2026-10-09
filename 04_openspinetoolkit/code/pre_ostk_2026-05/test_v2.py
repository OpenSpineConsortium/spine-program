# spine-program/04_openspinetoolkit: copied 2026-10-08 from the NextPaper working folder on the laptop
# (untracked, in no repository; file dated 2026-05-17). The copy's source path and hash are recorded in
# 04_openspinetoolkit/MANIFEST_LOCAL.md. Superseded by OpenSpineToolkit (main, cb43197); kept as dated lineage.
# Reads the CTSpinoPelvic1K-Sample export of May 2026 under the legacy label map (L1 = 1 ... femur_right = 12);
# never run it on a v11 volume without ostk.labels.labels_for(volume).
import os
import time
import json

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), ".matplotlib-cache"))

import nibabel as nib
import numpy as np

COMPUTE_FULL_LABEL_METRICS = False

# --------------------------------------------------
# LOAD LABEL FILE
# --------------------------------------------------

label_filename = "0022_pelvic_label.nii.gz"
ct_filename = "0022_pelvic_ct.nii.gz"

# --- hip mask: EDIT these to match your data ---------------------------
hip_label_filename = "0022_pelvic_hip_label.nii.gz"
LEFT_HIP_LABEL = 2
RIGHT_HIP_LABEL = 3
# Works whether the hip mask is the os coxae or the femur: the sphere fit
# locks onto the acetabulum (concave) or the femoral head (convex) -- the
# sphere centre is the femoral head centre either way.

label_path = os.path.join("labels", label_filename)
ct_path = os.path.join("ct", ct_filename)
hip_path = os.path.join("labels", hip_label_filename)

nii = nib.load(label_path)

labels = np.asanyarray(nii.dataobj)

affine = nii.affine

ct_nii = nib.load(ct_path)

ct = ct_nii.dataobj

print("Shape:", labels.shape)

# --------------------------------------------------
# LABEL DEFINITIONS
# --------------------------------------------------

LABELS = {
    1: "L1",
    2: "L2",
    3: "L3",
    4: "L4",
    5: "L5",
    6: "L6",
    7: "Sacrum"
}

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def voxel_to_world(points, affine):

    points = np.atleast_2d(np.asarray(points, dtype=float))

    homogenous = np.c_[
        points,
        np.ones(len(points))
    ]

    world = homogenous @ affine.T

    return world[:, :3]


def world_to_voxel(points, affine):

    points = np.atleast_2d(np.asarray(points, dtype=float))

    homogenous = np.c_[
        points,
        np.ones(len(points))
    ]

    return (homogenous @ np.linalg.inv(affine).T)[:, :3]


def compute_centroid(points):

    return np.mean(points, axis=0)


def compute_pca(points):

    from sklearn.decomposition import PCA

    pca = PCA(n_components=3)

    pca.fit(points)

    return pca


def sagittal_angle(vector):

    sagittal_vec = np.array([
        vector[1],
        vector[2]
    ])

    sagittal_vec = sagittal_vec / np.linalg.norm(sagittal_vec)

    angle = np.degrees(
        np.arctan2(
            sagittal_vec[0],
            sagittal_vec[1]
        )
    )

    return angle


def window_ct_slice(ct_slice):

    finite_values = ct_slice[np.isfinite(ct_slice)]

    body_values = finite_values[finite_values > -1000]

    if len(body_values) > 0:

        low, high = np.percentile(body_values, [1, 99])

    else:

        low, high = np.percentile(finite_values, [1, 99])

    return np.clip(
        (ct_slice - low) / (high - low + 1e-6),
        0,
        1
    )


def lateral_ct_projection(ct_proxy, start_index, stop_index, stride=6):

    projection = None
    n_slices = 0
    start = max(0, start_index)
    stop = min(ct_proxy.shape[2], stop_index)

    for z_index in range(start, stop, stride):

        ct_slice = np.asarray(ct_proxy[:, :, z_index], dtype=float)
        ct_slice = np.clip(ct_slice, -300, 1200)

        if projection is None:

            projection = ct_slice

        else:

            projection += ct_slice

        n_slices += 1

    return projection / max(n_slices, 1)


# --------------------------------------------------
# PELVIC PARAMETER HELPERS
#   SS = angle(endplate line, horizontal)
#   PI = angle(endplate normal at S1, S1->FH line)   [orientation free]
#   PT = PI - SS
# All angle math is done in world mm, so anisotropic voxel spacing
# (e.g. a thick slice axis) does not distort the result.
# --------------------------------------------------

def sagittal_frame(affine, ap_axis=0, si_axis=1):

    # File axes here are (P, I, R): ap_axis=0 posterior, si_axis=1 inferior.

    u_ap = affine[:3, ap_axis]
    u_si = affine[:3, si_axis]

    e_ap = u_ap / np.linalg.norm(u_ap)
    e_si = u_si / np.linalg.norm(u_si)

    def to2d(world_pts):
        w = np.atleast_2d(np.asarray(world_pts, dtype=float))
        return np.c_[w @ e_ap, w @ e_si]

    return e_ap, e_si, to2d


def surface_voxels(mask):

    # Boundary voxels (6-connectivity), no scipy needed.

    m = np.asarray(mask, dtype=bool)
    surf = np.zeros_like(m)

    for ax in range(3):

        for shift in (-1, 1):

            nb = np.roll(m, shift, axis=ax)

            face = [slice(None)] * 3
            face[ax] = 0 if shift == 1 else -1
            nb[tuple(face)] = False

            surf |= m & ~nb

    return np.argwhere(surf)


def fit_sphere_lsq(pts):

    # Coope linear least-squares sphere fit (exact for 4 points).

    pts = np.asarray(pts, dtype=float)

    A = np.c_[2.0 * pts, np.ones(len(pts))]
    b = np.sum(pts ** 2, axis=1)

    sol, *_ = np.linalg.lstsq(A, b, rcond=None)

    centre = sol[:3]
    radius = np.sqrt(max(sol[3] + centre @ centre, 0.0))

    return centre, radius


def fit_sphere_ransac(pts, r_min=14.0, r_max=34.0, thresh=2.0,
                      iters=4000, min_inliers=60, seed=0):

    # RANSAC with localised 4-point sampling so minimal sets land on the
    # same structure -- this is what makes it lock onto the femoral head.

    rng = np.random.default_rng(seed)
    pts = np.asarray(pts, dtype=float)

    if len(pts) > 15000:
        pts = pts[rng.choice(len(pts), 15000, replace=False)]

    n = len(pts)

    if n < 4:
        raise RuntimeError("Not enough surface points for a sphere fit.")

    best_inliers, best_score = None, 0

    for _ in range(iters):

        seed_pt = pts[rng.integers(n)]
        dist = np.linalg.norm(pts - seed_pt, axis=1)
        local = np.where(dist < 2.0 * r_max)[0]

        if len(local) < 4:
            continue

        idx = rng.choice(local, 4, replace=False)

        try:
            c, r = fit_sphere_lsq(pts[idx])
        except np.linalg.LinAlgError:
            continue

        if not (r_min <= r <= r_max) or not np.all(np.isfinite(c)):
            continue

        resid = np.abs(np.linalg.norm(pts - c, axis=1) - r)
        score = int(np.count_nonzero(resid < thresh))

        if score > best_score:
            best_score, best_inliers = score, resid < thresh

    if best_inliers is None or best_score < min_inliers:
        raise RuntimeError(
            f"RANSAC found no femoral-head sphere (best inliers={best_score}). "
            f"Try widening r_min/r_max or raising thresh.")

    centre, radius = fit_sphere_lsq(pts[best_inliers])

    return centre, radius, best_score


def femoral_head_center(mask, label, affine, **ransac_kw):

    side = (np.asanyarray(mask) == label)

    if int(side.sum()) == 0:
        raise ValueError(f"Label {label} not present in hip mask.")

    surf_mm = voxel_to_world(surface_voxels(side), affine)
    centre, radius, n_in = fit_sphere_ransac(surf_mm, **ransac_kw)

    return {"center": centre, "radius": radius,
            "n_inliers": n_in, "n_surface": len(surf_mm)}


def bicoxofemoral_midpoint(mask, left_label, right_label, affine, **ransac_kw):

    left = femoral_head_center(mask, left_label, affine, **ransac_kw)
    right = femoral_head_center(mask, right_label, affine, **ransac_kw)

    midpoint = 0.5 * (left["center"] + right["center"])
    separation = float(np.linalg.norm(left["center"] - right["center"]))

    return {"midpoint": midpoint, "left": left, "right": right,
            "separation_mm": separation}


def acute_angle(deg):

    deg = abs(deg) % 180.0
    return min(deg, 180.0 - deg)


def pelvic_parameters(endplate_pts_world, fh_midpoint_world, affine,
                      s1_midpoint_world=None):

    _, _, to2d = sagittal_frame(affine)

    ep = to2d(endplate_pts_world)              # (N,2) -> (AP, SI)
    fh = to2d(fh_midpoint_world).ravel()

    if s1_midpoint_world is None:
        s1 = ep.mean(axis=0)
    else:
        s1 = to2d(s1_midpoint_world).ravel()

    # endplate line direction (least squares in mm)
    m = np.polyfit(ep[:, 0], ep[:, 1], 1)[0]
    ep_dir = np.array([1.0, m])
    ep_dir /= np.linalg.norm(ep_dir)

    # sacral slope: endplate vs horizontal (AP axis)
    SS = acute_angle(np.degrees(np.arctan2(ep_dir[1], ep_dir[0])))

    # endplate normal oriented toward the femoral head
    normal = np.array([-ep_dir[1], ep_dir[0]])
    v_s1_fh = fh - s1
    if normal @ v_s1_fh < 0:
        normal = -normal

    # pelvic incidence: angle(normal, S1->FH) -- orientation independent
    cos_pi = (normal @ v_s1_fh) / (np.linalg.norm(v_s1_fh) + 1e-9)
    PI = float(np.degrees(np.arccos(np.clip(cos_pi, -1.0, 1.0))))

    PT = PI - SS

    return {"SS": SS, "PT": PT, "PI": PI}

# --------------------------------------------------
# STORE RESULTS
# --------------------------------------------------

centroids = {}

principal_axes = {}

# --------------------------------------------------
# PROCESS EACH LABEL
# --------------------------------------------------

if COMPUTE_FULL_LABEL_METRICS:

    for label_id, label_name in LABELS.items():

        print(f"\nProcessing {label_name}")

        voxels = np.argwhere(labels == label_id)

        if len(voxels) == 0:

            print("No voxels found.")

            continue

        points_mm = voxel_to_world(
            voxels,
            affine
        )

        centroid = compute_centroid(points_mm)

        centroids[label_name] = centroid

        print("Centroid (mm):", centroid)

        pca = compute_pca(points_mm)

        primary_axis = pca.components_[0]

        principal_axes[label_name] = primary_axis

        print("Primary Axis:", primary_axis)

        angle = sagittal_angle(primary_axis)

        print(f"Sagittal Angle: {angle:.2f} degrees")

# --------------------------------------------------
# LUMBAR LORDOSIS
# --------------------------------------------------

if COMPUTE_FULL_LABEL_METRICS and "L1" in principal_axes and "Sacrum" in principal_axes:

    l1_axis = principal_axes["L1"]

    sacrum_axis = principal_axes["Sacrum"]

    l1_angle = sagittal_angle(l1_axis)

    sacrum_angle = sagittal_angle(sacrum_axis)

    lumbar_lordosis = abs(
        l1_angle - sacrum_angle
    )

    print("\n--------------------------------")
    print(f"Lumbar Lordosis: {lumbar_lordosis:.2f} degrees")
    print("--------------------------------")

# --------------------------------------------------
# SACRAL SLOPE SECTION
# --------------------------------------------------

sacrum_voxels = np.argwhere(labels == 7)

if len(sacrum_voxels) == 0:

    raise ValueError("No sacrum voxels found in label file.")

# TRUE sagittal slice direction, centered left-to-right on the sacrum.
# The file axes are P, I, R, so axis 2 is the left/right axis to hold fixed.
x_mid = int(round(np.mean(sacrum_voxels[:, 2])))

del sacrum_voxels

# Anatomical slice
sagittal = np.asarray(labels[:, :, x_mid]).copy()

del labels

# Matching CT slice
ct_sagittal = np.asarray(ct[:, :, x_mid], dtype=float)

# Sacrum-only slice
sacrum_slice = sagittal == 7

# Orient as a lateral sagittal view:
#   horizontal = anterior to posterior
#   vertical = superior to inferior
display_slice = window_ct_slice(ct_sagittal).T

sacrum_overlay = sagittal.T == 7
sacrum_slice = sacrum_overlay

# --------------------------------------------------
# FIND SUPERIOR SACRAL ENDPLATE
# --------------------------------------------------

points = np.argwhere(sacrum_slice > 0)

columns = np.where(sacrum_slice.any(axis=0))[0]
top_boundary = []

for x in columns:

    y_values = np.where(sacrum_slice[:, x])[0]

    top_boundary.append([x, np.min(y_values)])

top_boundary = np.asarray(top_boundary)

# Fit the anterior-superior S1 plate, not the tiny posterior contour.
# In this dataset, displayed x increases anterior -> posterior, so the
# lumbosacral joint plane is best approximated by the anterior third of
# the superior sacrum boundary.
x_min = np.percentile(top_boundary[:, 0], 0)
x_max = np.percentile(top_boundary[:, 0], 35)
endplate_candidates = top_boundary[
    (top_boundary[:, 0] >= x_min) &
    (top_boundary[:, 0] <= x_max)
]

if len(endplate_candidates) < 2:

    raise ValueError("Could not identify enough S1 endplate boundary points.")

slope, intercept = np.polyfit(
    endplate_candidates[:, 0],
    endplate_candidates[:, 1],
    1
)

left_x = np.min(endplate_candidates[:, 0])
right_x = np.max(endplate_candidates[:, 0])

left_point = np.array([
    slope * left_x + intercept,
    left_x
])

right_point = np.array([
    slope * right_x + intercept,
    right_x
])

# --------------------------------------------------
# SACRAL SLOPE
# --------------------------------------------------

dy = right_point[0] - left_point[0]

dx = right_point[1] - left_point[1]

raw_sacral_slope = abs(np.degrees(np.arctan2(dy, dx)))
sacral_slope = min(raw_sacral_slope, 180 - raw_sacral_slope)

endplate_midpoint = (left_point + right_point) / 2

pelvic_incidence = None

print("\n===================================")
print(f"Sacral Slope: {sacral_slope:.2f} degrees")
print("===================================")

# --------------------------------------------------
# PELVIC TILT + PELVIC INCIDENCE
# --------------------------------------------------
# endplate_candidates are display (col=P, row=I) pairs on the slice at
# R = x_mid. Convert them, and the S1 midpoint, to world mm.

endplate_pts_world = voxel_to_world(
    np.c_[
        endplate_candidates[:, 0],                    # P
        endplate_candidates[:, 1],                    # I
        np.full(len(endplate_candidates), x_mid),     # R
    ],
    affine,
)

# endplate_midpoint is stored as [I, P] -> reorder to [P, I, R]
s1_mid_world = voxel_to_world(
    [[endplate_midpoint[1], endplate_midpoint[0], x_mid]],
    affine,
)

pelvic_tilt = None
fh_display = None        # (x, y) on the display image
fh_auto = False

if os.path.exists(hip_path):

    hip_nii = nib.load(hip_path)

    if not np.allclose(hip_nii.affine, affine):
        raise ValueError("Hip mask is not in the same image space as the CT/label.")

    hip_data = np.asanyarray(hip_nii.dataobj)

    bcf = bicoxofemoral_midpoint(
        hip_data, LEFT_HIP_LABEL, RIGHT_HIP_LABEL, affine
    )

    print("\n--- femoral head QC ---")
    print(f"Left  FH: r={bcf['left']['radius']:.1f} mm  "
          f"inliers={bcf['left']['n_inliers']}")
    print(f"Right FH: r={bcf['right']['radius']:.1f} mm  "
          f"inliers={bcf['right']['n_inliers']}")
    print(f"FH separation: {bcf['separation_mm']:.1f} mm "
          f"(expect ~150-200 mm)")

    params = pelvic_parameters(
        endplate_pts_world,
        bcf["midpoint"],
        affine,
        s1_midpoint_world=s1_mid_world,
    )

    pelvic_tilt = params["PT"]
    pelvic_incidence = params["PI"]

    # project the femoral head midpoint onto the display image
    fh_vox = world_to_voxel(bcf["midpoint"], affine).ravel()
    fh_display = (float(fh_vox[0]), float(fh_vox[1]))   # (P, I) = (x, y)
    fh_auto = True

    print("\n===================================")
    print(f"Sacral Slope     : {params['SS']:.2f} degrees")
    print(f"Pelvic Tilt      : {pelvic_tilt:.2f} degrees")
    print(f"Pelvic Incidence : {pelvic_incidence:.2f} degrees")
    print("===================================")

else:

    print(f"\n[warn] hip mask not found at '{hip_path}'.")
    print("[warn] Skipping PT/PI. Set hip_label_filename / hip labels above.")
    # fallback FH point so the viewer is still usable for manual placement
    fh_display = (float(endplate_midpoint[1]),
                  float(endplate_midpoint[0] + 0.30 * display_slice.shape[0]))

output_png = "test_output.png"
base_png = "sagittal_measurement_base.png"
output_html_files = ["test_22.html", "view_image.html"]
timestamp = int(time.time())

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

from PIL import Image, ImageDraw

ct_pixels = (display_slice * 255).astype(np.uint8)
rgb = np.repeat(ct_pixels[:, :, None], 3, axis=2)

sacrum_mask = sacrum_overlay > 0
rgb[sacrum_mask] = (
    0.65 * rgb[sacrum_mask] +
    0.35 * np.array([255, 190, 0])
).astype(np.uint8)

image = Image.fromarray(rgb)
image.save(base_png)
draw = ImageDraw.Draw(image)

line_start = (int(left_point[1]), int(left_point[0]))
line_end = (int(right_point[1]), int(right_point[0]))

draw.line(
    [line_start, line_end],
    fill=(255, 40, 40),
    width=5
)

for point in [line_start, line_end]:

    x, y = point

    draw.ellipse(
        [x - 5, y - 5, x + 5, y + 5],
        fill=(255, 40, 40)
    )

endplate_mid = (int(endplate_midpoint[1]), int(endplate_midpoint[0]))
draw.line(
    [(0, endplate_mid[1]), (image.width, endplate_mid[1])],
    fill=(255, 220, 0),
    width=3
)

# femoral head point + line to the S1 endplate midpoint
if fh_display is not None:

    fh_xy = (int(fh_display[0]), int(fh_display[1]))

    draw.line([fh_xy, endplate_mid], fill=(40, 220, 120), width=4)

    draw.ellipse(
        [fh_xy[0] - 6, fh_xy[1] - 6, fh_xy[0] + 6, fh_xy[1] + 6],
        fill=(40, 220, 220)
    )

label_lines = [f"SS {sacral_slope:.1f} deg"]
if pelvic_tilt is not None:
    label_lines.append(f"PT {pelvic_tilt:.1f} deg")
    label_lines.append(f"PI {pelvic_incidence:.1f} deg")

draw.rectangle(
    [12, 12, 250, 16 + 18 * len(label_lines)],
    fill=(0, 0, 0)
)
for i, line in enumerate(label_lines):
    draw.text((20, 18 + 18 * i), line, fill=(255, 255, 255))

image.save(output_png)

if pelvic_incidence is not None:
    title = (f"Case 22 - Sagittal CT: SS {sacral_slope:.1f} / "
             f"PT {pelvic_tilt:.1f} / PI {pelvic_incidence:.1f} deg")
else:
    title = f"Case 22 - Sagittal CT: Sacral Slope {sacral_slope:.2f} deg"

# voxel spacing (mm/pixel) along the display axes, so the viewer can do
# its angle math in mm and match the Python result under anisotropy
spacing_ap = float(np.linalg.norm(affine[:3, 0]))
spacing_si = float(np.linalg.norm(affine[:3, 1]))

initial_points = {
    "s1a": {
        "x": float(line_start[0]),
        "y": float(line_start[1])
    },
    "s1b": {
        "x": float(line_end[0]),
        "y": float(line_end[1])
    },
    "fh": {
        "x": float(fh_display[0]),
        "y": float(fh_display[1])
    }
}

html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test - Case 22</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            background: #f3f4f6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 16px;
        }}
        .toolbar {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            margin-bottom: 12px;
        }}
        button {{
            border: 1px solid #cbd5e1;
            background: #ffffff;
            color: #111827;
            border-radius: 6px;
            padding: 8px 10px;
            cursor: pointer;
            font-size: 14px;
        }}
        button.active {{
            background: #111827;
            color: #ffffff;
            border-color: #111827;
        }}
        .metrics {{
            font-weight: 700;
            margin-left: auto;
        }}
        .stage {{
            background: #ffffff;
            border: 1px solid #d1d5db;
            overflow: auto;
            max-height: calc(100vh - 96px);
        }}
        canvas {{
            display: block;
            max-width: 100%;
            height: auto;
        }}
        h1 {{
            margin: 0 0 12px;
            color: #333;
            font-size: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="toolbar">
            <button id="tool-s1a" data-tool="s1a">S1 point A</button>
            <button id="tool-s1b" data-tool="s1b">S1 point B</button>
            <button id="tool-fh" data-tool="fh">Femoral head</button>
            <button id="reset">Reset</button>
            <span class="metrics" id="metrics"></span>
        </div>
        <div class="stage">
            <canvas id="canvas"></canvas>
        </div>
    </div>
    <script>
        const imageUrl = "{base_png}?v={timestamp}";
        const initial = {json.dumps(initial_points)};
        const spacing = {{ ap: {spacing_ap}, si: {spacing_si} }};
        const points = {{
            s1a: {{...initial.s1a}},
            s1b: {{...initial.s1b}},
            fh: {{...initial.fh}}
        }};
        let activeTool = "s1a";

        const canvas = document.getElementById("canvas");
        const ctx = canvas.getContext("2d");
        const metrics = document.getElementById("metrics");
        const img = new Image();

        function setTool(tool) {{
            activeTool = tool;
            document.querySelectorAll("button[data-tool]").forEach((button) => {{
                button.classList.toggle("active", button.dataset.tool === tool);
            }});
        }}

        // pixels -> mm, so angles are correct under anisotropic spacing
        function mm(point) {{
            return {{ x: point.x * spacing.ap, y: point.y * spacing.si }};
        }}

        function acuteAngleDeg(vector) {{
            const angle = Math.abs(Math.atan2(vector.y, vector.x) * 180 / Math.PI);
            return Math.min(angle, 180 - angle);
        }}

        function computeMetrics() {{
            const a = mm(points.s1a), b = mm(points.s1b), f = mm(points.fh);
            const s1mid = {{ x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }};

            // sacral slope: endplate vs horizontal
            const endplate = {{ x: b.x - a.x, y: b.y - a.y }};
            const ss = acuteAngleDeg(endplate);

            // endplate normal, oriented toward the femoral head
            let nx = -endplate.y, ny = endplate.x;
            const v = {{ x: f.x - s1mid.x, y: f.y - s1mid.y }};
            if (nx * v.x + ny * v.y < 0) {{ nx = -nx; ny = -ny; }}

            // pelvic incidence: angle(normal, S1->FH)  [orientation free]
            const nLen = Math.hypot(nx, ny), vLen = Math.hypot(v.x, v.y);
            const cosPI = (nx * v.x + ny * v.y) / (nLen * vLen + 1e-9);
            const pi = Math.acos(Math.min(1, Math.max(-1, cosPI))) * 180 / Math.PI;

            const pt = pi - ss;
            metrics.textContent =
                `SS ${{ss.toFixed(1)}}  PT ${{pt.toFixed(1)}}  PI ${{pi.toFixed(1)}} deg`;
        }}

        function drawPoint(point, color, label) {{
            ctx.beginPath();
            ctx.arc(point.x, point.y, 6, 0, Math.PI * 2);
            ctx.fillStyle = color;
            ctx.fill();
            ctx.lineWidth = 2;
            ctx.strokeStyle = "#ffffff";
            ctx.stroke();
            ctx.fillStyle = "#ffffff";
            ctx.fillText(label, point.x + 9, point.y - 9);
        }}

        function redraw() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);

            ctx.font = "14px Arial";
            ctx.lineCap = "round";

            const mid = {{
                x: (points.s1a.x + points.s1b.x) / 2,
                y: (points.s1a.y + points.s1b.y) / 2
            }};

            // S1 endplate line
            ctx.strokeStyle = "#ff2828";
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(points.s1a.x, points.s1a.y);
            ctx.lineTo(points.s1b.x, points.s1b.y);
            ctx.stroke();

            // femoral head -> S1 midpoint line
            ctx.strokeStyle = "#28dc78";
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.moveTo(points.fh.x, points.fh.y);
            ctx.lineTo(mid.x, mid.y);
            ctx.stroke();

            // horizontal reference through the endplate midpoint
            ctx.strokeStyle = "#ffd400";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, mid.y);
            ctx.lineTo(canvas.width, mid.y);
            ctx.stroke();

            drawPoint(points.s1a, "#ff2828", "S1");
            drawPoint(points.s1b, "#ff2828", "S1");
            drawPoint(points.fh, "#28dcdc", "FH");

            computeMetrics();
        }}

        canvas.addEventListener("click", (event) => {{
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const point = {{
                x: (event.clientX - rect.left) * scaleX,
                y: (event.clientY - rect.top) * scaleY
            }};

            if (activeTool in points) {{
                points[activeTool] = point;
                if (activeTool === "s1a") setTool("s1b");
                else if (activeTool === "s1b") setTool("fh");
            }}

            redraw();
        }});

        document.querySelectorAll("button[data-tool]").forEach((button) => {{
            button.addEventListener("click", () => setTool(button.dataset.tool));
        }});

        document.getElementById("reset").addEventListener("click", () => {{
            points.s1a = {{...initial.s1a}};
            points.s1b = {{...initial.s1b}};
            points.fh = {{...initial.fh}};
            setTool("s1a");
            redraw();
        }});

        img.onload = () => {{
            canvas.width = img.width;
            canvas.height = img.height;
            setTool("s1a");
            redraw();
        }};
        img.src = imageUrl;
    </script>
</body>
</html>
"""

for output_html in output_html_files:

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)

print(f"Saved image: {output_png}")
print(f"Open in browser: {', '.join(output_html_files)}")
