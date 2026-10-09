Written for: the SX-Stitch authors (Wei Liu, SUSTech; Jinqian Liang, PUMCH), as a data-sharing request to be sent by Greg.

# Request for the SX-Stitch intraoperative C-arm image set

Paper: Li Y, Gao H, He M, Liang J, Gu J, Liu W. *SX-Stitch: An Efficient VMS-UNet Based Framework for
Intraoperative Scoliosis X-Ray Image Stitching.* arXiv:2409.05681. Corresponding authors marked in the
paper: Jinqian Liang (Peking Union Medical College Hospital) and Wei Liu (Department of Mechanical and
Energy Engineering, Southern University of Science and Technology). No email is printed in the arXiv
version; use the SUSTech and PUMCH directory addresses.

The set they describe: 1,032 intraoperative C-arm spinal images at 512, 1024 and 1920 px, in
consecutive overlapping series from the same patient with 20–90 % overlap, with vertebra segmentation
masks used to train VMS-UNet. It is the only published collection of overlapping intraoperative C-arm
frames of the spine, which is exactly the acquisition our sweep protocol simulates.

---

Subject: Request for the SX-Stitch C-arm image series for a non-commercial validation study

Dear Professor Liu and Dr Liang,

I am a general surgery resident at Wayne State University / Detroit Medical Center working on
intraoperative vertebral level confirmation from limited-field C-arm images. We have built and
published a protocol in which a short series of overlapping C-arm exposures, taken from the sacrum
upward, is linked into one map so that a later spot image containing no landmark can still be named.
Every number we have so far comes from CT renders and from single lateral radiographs cut into
overlapping frames; we have no real overlapping intraoperative series to test on.

Your SX-Stitch paper (arXiv:2409.05681) describes 1,032 intraoperative C-arm images in consecutive
overlapping series with 20–90 % overlap. That is precisely the acquisition our method assumes, and it
would let us report the protocol on real intraoperative frames rather than simulated ones.

I would like to ask whether the image series, with or without the segmentation masks, could be shared
for non-commercial research use. Specifically:

- the consecutive image series grouped by patient, with the acquisition order;
- any vertebra-level labels or masks that exist;
- the licence or data-use terms you require.

We would use the data only to evaluate (not train) our level-naming pipeline, would not redistribute
it, would cite SX-Stitch as the source in any resulting publication, and would be glad to share our
results on your series with you before publication. If a data-use agreement through Wayne State
University is needed, I can initiate it.

Thank you for considering this.

Gregory Schwing, MD, PhD
Department of General Surgery, Wayne State University School of Medicine / Detroit Medical Center
go2432@wayne.edu
