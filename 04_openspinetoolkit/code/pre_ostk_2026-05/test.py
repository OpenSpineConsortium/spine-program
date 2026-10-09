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

label_path = os.path.join("labels", label_filename)
ct_path = os.path.join("ct", ct_filename)

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

    homogenous = np.c_[
        points,
        np.ones(len(points))
    ]

    world = homogenous @ affine.T

    return world[:, :3]


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

label = f"SS {sacral_slope:.1f} deg"

draw.rectangle(
    [12, 12, 250, 40],
    fill=(0, 0, 0)
)
draw.text(
    (20, 20),
    label,
    fill=(255, 255, 255)
)

image.save(output_png)

title = f"Case 22 - Sagittal CT: Sacral Slope {sacral_slope:.2f} deg"

initial_points = {
    "s1a": {
        "x": float(line_start[0]),
        "y": float(line_start[1])
    },
    "s1b": {
        "x": float(line_end[0]),
        "y": float(line_end[1])
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
        const points = {{
            s1a: {{...initial.s1a}},
            s1b: {{...initial.s1b}}
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

        function acuteAngleDeg(vector) {{
            const angle = Math.abs(Math.atan2(vector.y, vector.x) * 180 / Math.PI);
            return Math.min(angle, 180 - angle);
        }}

        function computeMetrics() {{
            const endplate = {{
                x: points.s1b.x - points.s1a.x,
                y: points.s1b.y - points.s1a.y
            }};
            const ss = acuteAngleDeg(endplate);
            metrics.textContent = `Sacral slope ${{ss.toFixed(1)}} deg`;
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

            ctx.strokeStyle = "#ff2828";
            ctx.lineWidth = 5;
            ctx.beginPath();
            ctx.moveTo(points.s1a.x, points.s1a.y);
            ctx.lineTo(points.s1b.x, points.s1b.y);
            ctx.stroke();
            drawPoint(points.s1a, "#ff2828", "S1");
            drawPoint(points.s1b, "#ff2828", "S1");

            const mid = {{
                x: (points.s1a.x + points.s1b.x) / 2,
                y: (points.s1a.y + points.s1b.y) / 2
            }};
            const endplate = {{
                x: points.s1b.x - points.s1a.x,
                y: points.s1b.y - points.s1a.y
            }};
            ctx.strokeStyle = "#ffd400";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(0, mid.y);
            ctx.lineTo(canvas.width, mid.y);
            ctx.stroke();

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

            if (activeTool === "s1a" || activeTool === "s1b") {{
                points[activeTool] = point;
                setTool(activeTool === "s1a" ? "s1b" : "s1a");
            }}

            redraw();
        }});

        document.querySelectorAll("button[data-tool]").forEach((button) => {{
            button.addEventListener("click", () => setTool(button.dataset.tool));
        }});

        document.getElementById("reset").addEventListener("click", () => {{
            points.s1a = {{...initial.s1a}};
            points.s1b = {{...initial.s1b}};
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
