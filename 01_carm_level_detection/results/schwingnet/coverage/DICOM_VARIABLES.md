# DICOM acquisition variables, C-arm against plain film: not built, and why (2026-09-25)

Greg asked for a plot of the DICOM header variables of the C-arm frames against those of the films (a t-SNE or
similar) to show why the fluoroscopy problem might be harder. The rule for this pass was to build it only from
metadata already on disk, and only if at least two device groups carry five or more usable header fields per image.
One group does. The film side carries none.

What is on disk, per group. **C-ArmLSpine (Surgio-B51, 149 cases):** per-frame headers for 299 spot frames in
`SchwingNet/results/inputs/headers_dossier.json` (KVP, XRayTubeCurrent, ExposureTime, DistanceSourceToDetector,
DistanceSourceToPatient, PositionerPrimaryAngle, PositionerSecondaryAngle, PixelSpacing, Rows/Columns, BitsStored,
WindowCenter/Width) and a 901-file numeric census in `docs/devices/census/surgio_b51__headers.json` (kVp 73-111,
mAs 0.12-0.13, pulse 14-20 ms, SID 1140 mm, SOD 745 mm, primary angle -58 to +37 deg). That is the one group with
five or more per-image fields. **COBRA2026 (Elekta XVI):** ships no DICOM; its per-case metadata.yaml carries
PatientAge/Sex/StudyDate and the projection geometry (gantry angle, SID, SDD, imager size), no exposure fields
(COVERAGE.md section D). **DeepFluoro and Ljubljana:** vendor placeholders and an h5 with no header block
(`results/age_sex_by_source.json`). **The spinesac census fluoroscopes** (GE Fluorostar 59 files, Philips Allura
590, Siemens 39, Skanray 53, Ziehm 8; `docs/devices/census/*_headers.json`) hold per-device summary statistics of
kVp, mA, ms, SID and pixel size, not per-file values, and their positioner tags take one value per device across AP
and lateral files (COVERAGE.md, "tags exist, but do not vary with the view"); none of them is a corpus the paper
trains or scores on. **The plain-film corpora** are the problem: NHANES II, BUU-LSPINE and CSXA are distributed as
pixel files with no DICOM header (view protocol only; COVERAGE.md section D), and VinDr-SpineXR, which is DICOM,
has had only PatientAge and PatientSex read from its headers (`results/age_sex_cache/vindr_age_sex.csv`, grid job
40438307); its exposure and geometry tags exist only as the publisher's supplemental PDF on disk, not as a table.

So an embedding of "the C-arm's header variables against the film's" would place one device's 299 frames in a
cloud and every film at the origin of a space it has no coordinates in; the picture would show the absence of
metadata, not a harder acquisition space. It is not built. The acquisition-space contrast the paper can state is the
one COVERAGE.md already measures from what does exist: coverage C and normalised entropy H* over lateral angle,
tilt, roll, magnification and field per training set (films: one view protocol, H* = 0 by construction; Surgio
spot frames: H*_lat 0.24 over the AP/lateral pool; the arc pool 0.99), and the matched-N render arms that vary that
axis alone (POOLED_FIT.md).

What would make the figure possible, if wanted later: one grid job that reads the exposure tags (KVP,
Exposure/ExposureTime/XRayTubeCurrent, ImagerPixelSpacing or PixelSpacing, Rows/Columns, BitsStored,
DistanceSourceToDetector where present, ViewPosition) from every VinDr-SpineXR DICOM into a per-image CSV, which
gives one film corpus with five or more fields to set beside the Surgio frames. NHANES II, BUU and CSXA would still
have nothing to plot.
