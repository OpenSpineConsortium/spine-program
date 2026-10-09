To: [e-mail withheld]
Cc: [e-mail withheld]
Subject: Data request: ex-vivo lumbar CT and C-arm X-rays from Jecklin et al., Medical Image Analysis 2024

Dear Dr. Jecklin,

I am [a neurosurgery resident; confirm title] at Wayne State University and the Detroit Medical Center. I work on counting vertebral levels on intraoperative fluoroscopy, to prevent wrong-level spine surgery. I read your Medical Image Analysis paper on domain adaptation for lumbar reconstruction from real fluoroscopy, and your 2025 Scientific Reports follow-up. Your ex-vivo set is the only one I have found that pairs CT with real mobile C-arm images of the lumbar spine inside an intact torso, on more than one device. I am writing to ask whether you would share the full dataset under a data use agreement.

What I would use it for. We train a vertebra detector on simulated fluoroscopy rendered from CT, and we calibrate the rendering against real frames. So far the only real frames with known pose we have are DeepFluoro: six cadaveric pelves on one Siemens Cios Fusion. On those, the calibrated renderer explains about 90 per cent of the variance of held-out real frames. We also found that the device stores log-compressed display images, not raw transmission. Neither result can be trusted until it is repeated on the lumbar spine and on other C-arms. Your Cios Spin, Ziehm Vision and Ziehm Vision FD images would let us test both.

What I am asking for:
1. All 13 specimens from the Medical Image Analysis paper and the six validation specimens: the CT volumes, every real X-ray, the fiducial-based projection matrix for each image, and the device that took it.
2. The specimens from the Scientific Reports paper, if they are not among these.
3. The X-rays as the C-arms exported them (original DICOM with headers, if you have them), rather than the 512-pixel crops. We need kVp, detector type and the Pixel Intensity Relationship tag.

What I can offer:
- A data use or transfer agreement through Wayne State on your terms: research use only, no redistribution, secure storage, no attempt to re-identify donors.
- Citation of both papers, and acknowledgement or co-authorship as you judge appropriate.
- Our calibration code and the device terms fitted for your three C-arms. I would share any result with you before submission.

I understand the set is restricted because of pending patents, and I will work within whatever terms that requires.

With thanks,

Gregory Schwing, MD, PhD
[title], Department of General Surgery
Wayne State University School of Medicine / Detroit Medical Center
[e-mail withheld]
