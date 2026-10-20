r"""Fill the WSU HPR Determination Tool (11/2021) for the VinDr-SpineXR follow-up to determination 2026-269.
Base = every value of the tool as filed 08/28/2026 (idf_work/hpr_previous_values.json); overrides below are the
VinDr-specific answers from spinesurg-ct-nnunet/docs/IRB/HPR_determination_VinDr-SpineXR_draft.md plus Greg's
facts of 2026-09-25 (surgery resident; sponsor Loren Schwiebert; PhysioNet account gschwing / go2432@wayne.edu,
restricted tier, no credentialing)."""
import json
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
prev = json.load(open(HERE / "hpr_previous_values.json", encoding="utf-8"))

T = {}  # text values
C = {}  # checkbox states

# ---------------- Section A
T["Project Title"] = ("Open Spine Consortium: Secondary Analysis of a De-Identified Radiograph Dataset (VinDr-SpineXR) Obtained Under the "
                      "PhysioNet Restricted Health Data Use Agreement -- supplement to HPR Determination 2026-269")
T["Name of person conducting the project"] = "Gregory Schwing"
T["Title"] = "Resident Physician, General Surgery, Detroit Medical Center / Wayne State University School of Medicine"
T["Date"] = "09/25/2026"
T["Email Address"] = "go2432@wayne.edu"
T["Phone"] = "504-994-0403"
C["ResidentFellowTrainee"] = "/On"
T["Wayne State Faculty DMC Staff WSU Graduate Student Karmanos Staff WSU Undergraduate Student J D Dingell VAMC Staff ResidentFellowTrainee OtherDivision or College"] = "School of Medicine"
T["Department"] = "Surgery"
T["Campus Address"] = "5057 Woodward Ave, Detroit, MI 48202"
T["Name"] = "Loren Schwiebert"
T["Title_2"] = "Professor, Department of Computer Science, Wayne State University"
T["I do not have a Faculty SponsorSupervisorForm completed by"] = "Gregory Schwing"
T[" Email"] = "go2432@wayne.edu"
C["Medical study"] = "/On"

# ---------------- Section B
T["Describe the locations where activities will take place"] = (
 "All activities are computational and take place at Wayne State University. No activity occurs at a clinical site, and no "
 "participant is contacted, recruited, observed, or enrolled at any location.\n\n"
 "Data are downloaded over the internet from public archives to WSU-managed computing resources, including the WSU High "
 "Performance Computing Grid and WSU-managed workstations. Analysis, annotation, model training, and manuscript preparation are "
 "performed on those resources. Derived annotations and software are published to public repositories (Zenodo, GitHub, Hugging "
 "Face) under open licences.\n\n"
 "Addition for this dataset: the VinDr-SpineXR files are held only on the WSU High Performance Computing Grid under the storage "
 "of the PhysioNet account holder (Gregory Schwing, PhysioNet username gschwing). Under the data use agreement they are not "
 "copied to any public repository, not shared with any person outside the agreement, and no image or derived frame from them "
 "is included in any published dataset.")
C["Secondary or retrospective data collection"] = "/On"
C["undefined_2"] = "/No"       # 3. access to identifiable information during collection: No
C["undefined_3"] = "/No_2"     # 4. individually identifiable information: No
T["If yes list all identifiers being collected eg name date of birth medical record number email address other codes etc"] = (
 "None. No individually identifiable information is obtained, used, generated, or retained. The depositors de-identified the "
 "images before release (protected health information removed from the DICOM tags; patient information burned into the pixel "
 "data removed after manual inspection of every scan; de-identified images manually reviewed), and the investigators receive no "
 "key or code permitting re-identification. The released per-image fields are the depositors' own study and image identifiers "
 "and their lesion annotations.")
C["undefined_5"] = "/On"       # 5. identities readily ascertained: No
C["Data Repository"] = "/On"
C["Other_2"] = "/On"
T["Medical Record Review Complete 6a Survey Interview Biobank Data Repository Other Describe"] = (
 "PhysioNet (physionet.org), a research data repository operated by the MIT Laboratory for Computational Physiology, serving "
 "the dataset VinDr-SpineXR v1.0.0 (Pham HH, Nguyen Trung H, Nguyen HQ, 2021; doi 10.13026/q45h-5h59) under the PhysioNet "
 "Restricted Health Data License 1.5.0 to registered users who sign the PhysioNet Restricted Health Data Use Agreement 1.5.0. "
 "This is PhysioNet's restricted-access tier (registered account plus the agreement); no credentialing and no CITI training is "
 "required for it. This differs from the sources covered by 2026-269, described there as public archives releasing de-identified "
 "imaging under open licences without application or data use agreement.")
C["NAProject does not involve the review of or collection of"] = "/On"
_k6a = next(k for k in prev if k.startswith("Indicate the institutions Covered Entity"))
T[_k6a] = (
 "N/A. No medical records at any covered entity are accessed. All imaging is obtained from the repository, which received it "
 "already de-identified from the depositors (Hospital 108 and Hanoi Medical University Hospital, Viet Nam, 2011-2020, under those "
 "hospitals' IRB approval with a waiver of informed consent).")
T["Describe how the data will be obtained eg survey interview observation testing review of existing records etc"] = (
 "By direct download from PhysioNet after registering an individual PhysioNet account (username gschwing, registered with the "
 "WSU e-mail go2432@wayne.edu) and accepting the PhysioNet Restricted Health Data Use Agreement 1.5.0 online. No credentialing "
 "was required. No data are collected from participants, and no records at any covered entity are accessed. The dataset was "
 "downloaded to the WSU High Performance Computing Grid on 7 September 2026 and verified against the depositors' published SHA-256 "
 "checksums (10,466 images, 0 mismatches).\n\n"
 "Disclosure: the download and use (2,071 of the 10,466 films, in cropped form, as pseudo-labelled training data for a subset of "
 "machine-learning models in a manuscript under preparation) took place after the 2026-269 tool was completed (28 August 2026) and "
 "after that determination issued (2 September 2026). Item 7 of the 2026-269 tool promised a separate submission before any "
 "agreement-governed dataset was used; this is that submission, made late, and the investigator asks the office to determine "
 "whether this secondary analysis is human participant research. If the office determines that it is, the models trained on it "
 "will be withdrawn and retrained without it.\n\n"
 "The five criteria of item 7 of the 2026-269 tool, applied to this dataset: (1) publicly available and de-identified by the "
 "source before release -- MET (listed on PhysioNet since 24 August 2021 with a DOI; de-identification as described above); "
 "(2) downloadable without application, permission, eligibility review or data use agreement -- NOT MET (a data use agreement "
 "is accepted online; no eligibility review); (3) not designated restricted-use by the source -- NOT MET by name (the source "
 "calls the licence 'Restricted Health Data License'; the restriction is the agreement's terms: research use only, no "
 "re-identification, no sharing of access, report any identifying information found); (4) no key, code or relationship "
 "enabling re-identification -- MET; (5) no re-identification attempt and no linkage -- MET (the agreement also forbids it). "
 "The agreement's obligations are honoured: files reside only in the account holder's WSU storage; no image, crop or derived "
 "frame is redistributed; the project's code is released under an open licence as the agreement asks.")

# ---------------- Section C
T["Describe the purpose of this project"] = (
 "The Open Spine Consortium develops open, reproducible methods for analysing spinal and pelvic anatomy on computed tomography "
 "and radiographs. Its projects share one design: existing, publicly released, de-identified imaging is re-analysed to produce "
 "annotations, measurements, software, and machine-learning models, which are then released openly for others to use and check.\n\n"
 "The clinical problem motivating this work is that vertebral level is conventionally established by counting down from C2. An "
 "abdominal CT or a limited intraoperative image does not contain C2, so a transitional vertebra, a rib borne by a lumbar "
 "vertebra, and a stump rib produce overlapping appearances, and the correct label depends on a count the field of view cannot "
 "support. Mislabelling a level has direct consequences for surgical planning.\n\n"
 "The purpose of THIS determination is narrower than 2026-269. It asks whether the secondary analysis of one additional "
 "de-identified dataset, VinDr-SpineXR, which is governed by a data use agreement and therefore falls outside the scope that "
 "2026-269 defined for itself, constitutes human participant research. The dataset's role is as additional training images of "
 "the lumbar and thoracic spine on plain radiographs for a model that names vertebral levels on intraoperative C-arm images.")
T["Describe the objectives or aims for the project"] = (
 "Across current and planned Open Spine Consortium projects:\n"
 "1. Produce and openly release expert-reviewed anatomical annotations of existing public imaging datasets (vertebrae by level, "
 "sacrum, pelvis, femurs, ribs by level, and surgical instrumentation where present).\n"
 "2. Characterise anatomical variation in these cohorts, particularly lumbosacral transitional anatomy and its effect on vertebral "
 "level assignment.\n"
 "3. Develop, train, and evaluate segmentation and measurement algorithms on those annotations, and release the software and "
 "trained models under open licences.\n"
 "4. Compute spinopelvic parameters reproducibly from segmentations, and evaluate agreement against established methods.\n"
 "5. Report methods and results in peer-reviewed publications, with the underlying annotations and code archived publicly.\n\n"
 "No objective requires the identity of any individual, and none is served by knowing it. For this dataset only objective 3 is "
 "engaged: VinDr-SpineXR images serve as training data. No annotation of VinDr-SpineXR is released (the vertebral levels assigned "
 "to its images were generated automatically and are not distributed), and no VinDr-SpineXR image appears in any released "
 "dataset, figure or accuracy table.")
T["Describe how the results will be usedapplied"] = (
 "Results are used to advance scientific and clinical understanding of spinal anatomy and its measurement, and are disseminated "
 "as peer-reviewed journal articles and conference papers; openly licensed datasets of derived annotations archived with a DOI; "
 "open-source software and trained models; and educational and reference material for clinicians and researchers.\n\n"
 "Findings are not applied to the care of any individual whose images appear in these datasets. No individual is contacted, and "
 "no result is returned to any individual, because no individual can be identified from the data. Software released by the "
 "consortium is provided for research use only and is not offered for clinical diagnosis or treatment; should FDA clearance later "
 "be sought for any device, a separate determination would be obtained beforehand.\n\n"
 "Addition for this dataset: the PhysioNet licence requires the licensee to contribute code associated with publications arising "
 "from the data to an open repository; the project's code is released under an open licence, which satisfies this. Trained model "
 "weights that learned from VinDr-SpineXR images do not contain, and cannot reproduce, any source image.")
T["Describe the participants for the project"] = (
 "There are no participants in this project as the term is used in 45 CFR 46.\n\n"
 "The project analyses imaging studies that were acquired previously, for clinical or research purposes unrelated to this work, "
 "and that were de-identified and released by their source before the investigators obtained them. The investigators have no "
 "contact of any kind with the individuals whose images these were, have no means of identifying them, and receive no key or code "
 "that would permit re-identification.\n\n"
 "For this dataset: VinDr-SpineXR comprises 10,466 spine radiographs from 5,000 studies (4,000 training studies with 8,389 images; "
 "1,000 test studies with 2,077 images), collected retrospectively by the depositors at Hospital 108 and Hanoi Medical University "
 "Hospital over 2011-2020 under those hospitals' IRB approval with a waiver of informed consent, de-identified, and deposited on "
 "PhysioNet in 2021. The per-image information available to the investigators is the image itself, the depositors' study and image "
 "identifiers, and their lesion annotations. Of the 10,466 images, 2,071 were used in this project.")

# ---------------- Section D (as filed on 2026-269)
for k in ("undefined_6", "undefined_7", "undefined_8", "undefined_9"): C[k] = "/On"   # 1.1 (+ both sub-boxes), 1.2
C["undefined_10"] = "/No_3"   # 2.1 intervention/interaction: No
C["undefined_11"] = "/No_4"   # 2.2 identifiable private information: No
# Step 3 (FDA) boxes and the office's determination boxes stay unchecked

# ---------------- write
reader = PdfReader(str(ROOT / "hpr_determination_tool_revised_11_2021.pdf"))
writer = PdfWriter(clone_from=reader)
fields = reader.get_fields()
missing = [k for k in list(T) + list(C) if k not in fields]
assert not missing, missing
for page in writer.pages:
    writer.update_page_form_field_values(page, {**T, **C}, auto_regenerate=False)
writer._root_object["/AcroForm"][NameObject("/NeedAppearances")] = BooleanObject(True)
out = ROOT / "IRB_VinDr_2026-09-25" / "01_HPR_Determination_Tool_VinDr-SpineXR_Schwing_2026-09-25.pdf"
out.parent.mkdir(exist_ok=True)
with open(out, "wb") as f: writer.write(f)
# read back
rb = PdfReader(str(out)).get_fields()
filled = {k: str(v.get("/V")) for k, v in rb.items() if v.get("/V") not in (None, "", "/Off")}
print("written", out.name, "| fields with values:", len(filled))
for k in ["Project Title", "Title", "Date", "Email Address", "Name", "Title_2", "ResidentFellowTrainee", "Medical study", "undefined_2", "undefined_3", "undefined_5", "Data Repository", "undefined_10", "undefined_11"]:
    print(f"  {k[:40]!r:42} = {filled.get(k, '(unset)')[:90]!r}")
