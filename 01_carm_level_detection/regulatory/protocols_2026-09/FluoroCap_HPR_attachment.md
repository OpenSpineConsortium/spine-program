# Attachment: what "publicly available images" means in this project

Prepared for the Wayne State University Human Participant Research determination request.
Companion to the FluoroCap protocol (`docs/FLUOROCAP_PROTOCOL.md` in the spinesurg-ct-nnunet
repository) and the per-image manifest it produces.

## 1. Summary

The project assembles a collection of previously published fluoroscopic and radiographic
images of the human spine from the open biomedical literature, and uses them to evaluate a
software algorithm that names the vertebral level shown. There is no contact with any person,
no prospective imaging, no intervention, and no access to any record other than what the
authors published. Every image is a figure, or a panel cut from a figure, of an article in the
PubMed Central Open Access subset (or, for a small number, a file on Wikimedia Commons with a
declared free licence). The images were de-identified by the authors before publication under
journal policy (ICMJE); the collection holds rasterised pixel data only, no DICOM headers or
EXIF metadata, and the figure captions are scanned automatically for dates, record numbers and
honorifics, with any hit held out of use.

## 2. How the images are found (predefined search protocol)

1. Europe PMC is searched for open-access articles whose text mentions fluoroscopy, C-arm,
   image intensifier or intra-operative radiography together with the spine (the exact query
   is recorded in the protocol and in every frozen release).
2. For each article the figure captions are read through the PMC BioC service (or the
   Europe PMC full-text XML). A figure is kept only when its caption states fluoroscopy /
   C-arm / intra-operative imaging, refers to the spine, and names a vertebral level
   (criteria I1–I4 of the protocol).
3. Three further routes to the same PMC figures are searched with the same caption rules
   (NLM Open-i; the MultiCaRe case-report set, Zenodo record 10079370; the Open-PMC-18M
   set of decomposed PMC sub-figures), and Wikimedia Commons is searched for files whose
   declared licence and description meet the same rules.
4. The kept figures are downloaded from the PMC content delivery network at a rate of a few
   requests per second, with the URL, time, HTTP status and user agent logged for each.

## 3. What is recorded for every image (manifest fields)

| Group | Fields |
|---|---|
| identity | image_id, figure_id, panel_hash (SHA-256), original_figure_hash, dataset_version, manifest_version |
| origin | source_repository, source_image_url, source_article_url, DOI / PMID / PMCID, journal, year, title, authors, access_date, http_status, user_agent |
| rights | license (as published), license_url, license_source, license_verified_date, license_tier (A–E), commercial_use_allowed, derivative_use_allowed, redistribution_allowed, restriction text |
| de-identification | patient_identifier_present (caption scan), deidentification_basis, metadata_removed, the article's ethics / consent statement when one is found |
| content | modality, anatomic_region, projection, vertebral levels named in the caption, phase (intra-/pre-/post-operative), hardware, positioning |
| population (article level, as published) | age / sex mentions, study population sentences, species, cadaver / phantom flags, MeSH headings |
| acquisition (article level) | equipment and exposure sentences from the methods |
| selection | inclusion criteria met (I1–I4), exclusion codes (E1–E8), human QC status and reason |
| processing | panel box in the parent figure, splitter version and confidence, preprocessing description |
| labels | the caption-stated level; reader labels and adjudication once the reading study is done |

Images and manifest are frozen as a version with a checksum file over every file and a lock
record containing the manifest hash, so the collection used in any analysis can be shown to be
exactly the collection described.

## 4. Why no individual can be identified

- The images are figures the authors chose to publish in journals that require identifying
  information to be removed or consent for publication to be obtained.
- No image is linked to any clinical record, name, date of service, or institution beyond the
  published article's own text.
- The only text kept is the published caption and sentences from the published article.
- The collection is not combined with any other data source that could re-identify a person.

## 5. What the investigators will do with the images

Run a locked software algorithm on each image, compare its output with the level named in
the caption and with labels from independent readers, and report accuracy. No image is used to
contact anyone, no result is returned to any patient or clinician, and no clinical decision
depends on the output.
