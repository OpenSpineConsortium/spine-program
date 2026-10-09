<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/CTSpinoPelvic1K master 7ddfe38, 7ddfe38, path proposals/cm_spine_request_email.md. Copied 2026-10-08. Redactions applied by kind: affiliation (1), lead address (1), researcher e-mail (1). Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

# CM Spine dataset — access request

**What it is.** The "CM Spine" set from Zeng et al., *Exploring Neighbor Spatial Relationships for
Enhanced Lumbar Vertebrae Detection in X-ray Images*, Electronics 13(11):2137, 2024
(https://doi.org/10.3390/electronics13112137): 208 lumbar AP radiographs, 1024×1024, acquired
**during surgery** on a Geelin500-A mobile G-arm, with per-level vertebra boxes. The only host
was a Google Drive link in the code repo (github.com/zengyuyuyu/Neighbor); it now returns 404.
No forks, no Wayback copy, no other host.

**Who to write.** Authors: Yu Zeng, Kun Wang, Lai Dai, Changqing Wang, Chi Xiong, Peng Xiao,
Bin Cai, Qiang Zhang, Zhiyong Sun, Erkang Cheng, Bo Song — School of Biomedical Engineering,
Anhui Medical University, and the Institute of Intelligent Machines, Hefei Institutes of
Physical Science, Chinese Academy of Sciences. The corresponding author's email is printed on
the MDPI article page under "Correspondence" (the site blocks scripted access, so open it in a
browser). Two further channels:

- the GitHub account that pushed the repo's commits: Yifeng Bai, [researcher e-mail withheld]
- an issue on github.com/zengyuyuyu/Neighbor (public, and the owner gets notified)

Send to the corresponding author, cc Yifeng Bai, and open the issue the same day.

---

**Subject:** Request for the CM Spine intraoperative lumbar X-ray dataset (Electronics 2024, 13:2137)

Dear Dr. Song and colleagues,

I am a surgical resident at Wayne State University / Detroit Medical Center and lead the
OpenSpineConsortium (openspineconsortium.com), an open research group that builds documented,
openly licensed spine imaging datasets and benchmarks. We recently released CTSpinoPelvic1K
(Zenodo, 802 CT records with unified spine, pelvis, rib and femur labels) and are now assembling
a spine radiograph corpus for vertebra localization and fracture detection.

Your paper "Exploring Neighbor Spatial Relationships for Enhanced Lumbar Vertebrae Detection in
X-ray Images" describes the CM Spine dataset: 208 intraoperative lumbar AP images from a
Geelin500-A G-arm with per-vertebra annotations. Intraoperative radiographs are exactly what
public collections lack, and your set is the only annotated one we have found. The Google Drive
link in the Neighbor repository (drive.google.com/file/d/1r9wX1802gkU4-EQHMMlyAlEiWXGWLhhJ) now
returns "Page not found".

Would you be willing to share the dataset with us? Specifically:

1. The 208 images and their annotation files, in whatever format you used for the paper.
2. Any terms you would like attached: we will use it for research only, cite the paper in every
   work that touches it, and not redistribute it unless you say we may.
3. If a re-hosted public copy would help you (Zenodo or HuggingFace, under your names and a
   license you choose), we would be glad to set that up and maintain it.

A Google Drive, Baidu Netdisk, or OneDrive link would all work for us; the set is small enough
to email in parts as well.

Thank you for considering this, and congratulations on the paper: the neighbor-offset fusion is
a clean idea and we would like to evaluate it on our own data.

Best regards,

Gregory Schwing, MD, PhD
Resident, Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center
OpenSpineConsortium — https://github.com/OpenSpineConsortium
[the lead's university address]

---

**GitHub issue text** (title: "CM Spine dataset link returns 404"):

The Google Drive link for the CM Spine dataset in the README
(drive.google.com/file/d/1r9wX1802gkU4-EQHMMlyAlEiWXGWLhhJ) now returns "Page not found".
Could you re-share the file, or point to another host? We are an open spine-imaging research
group and would like to evaluate on it, with full citation of the Electronics paper. Happy to
help re-host it under your names if useful. Thank you.
