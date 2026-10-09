---
title: "Computer methods for reading spine and pelvis images at DMC: what we have built, what we plan to do, and what we need"
subtitle: "Two new protocols: a retrospective imaging and records study, and a prospective silent-evaluation study, submitted to WSU and DMC together"
author: "Gregory Schwing, MD, PhD, PGY-1 Surgery, Detroit Medical Center; Research Director, Open Spine Consortium"
date: "September 2026"
---

# In one paragraph

Surgeons and radiologists count vertebrae on scans to know where to operate. In about one person in six the spine is built differently, with an extra lumbar vertebra, an extra rib, or a vertebra fused to the pelvis, and counting goes wrong. That is the most common cause of operating on the wrong level. Our group has already built, from public scans, a computer program that outlines every bone of the spine and pelvis and names each vertebra from its own shape, including the unusual ones. We now want to check it on DMC patients and extend it to trauma: finding fractures on the X-rays and CT scans trauma patients already get, and naming the level correctly on the first film. Everything is done on images and records that already exist. No patient is contacted and nothing goes back into the medical record.

# What we can already do (all on public, de-identified data, WSU determination 2026 269)

- **A labelled dataset the field did not have.** 802 CT scans with every bone of the spine, pelvis and ribs outlined and named, including the extra lumbar vertebra, lumbar ribs and surgical hardware. Thirteen student annotators and two radiologists corrected the labels; two readers graded every transitional case. It is public on Zenodo (10.5281/zenodo.22642578) and described at https://openspineconsortium.com.
- **Proof that a vertebra can be named from its shape.** Using measurements from those labels, a simple classifier tells a thoracic from a lumbar vertebra with 99.8 percent reliability and T12 from L1 with 99 percent, without counting from the skull.
- **A program that does it on CT.** The model now training names the extra lumbar vertebra as its own class on scans it has never seen, with overlap scores between 0.77 and 0.96 after a tenth of its training, where public tools cannot name it at all. It reports how confident it is in the count instead of guessing.
- **Where the extra vertebra actually is.** In 18 patients with six lumbar vertebrae, the labels show the extra segment belongs at the bottom of the spine in 15, which matters for which joint is mobile and where the nerve exits.
- **X-rays too.** A detector trained on 33,943 vertebrae from 5,401 public radiographs finds the four corners of each vertebral body on both film and digital images (97 percent detection at the standard threshold). Corners give the angles surgeons measure by hand.
- **A team and the machinery.** Thirteen trained student annotators, a public web viewer that measures spinopelvic alignment automatically, and Wayne State's H200 GPU cluster for training.

# What we plan to do with DMC data

1. **Check the CT program on our own patients.** Run it on DMC spine and pelvis CT scans and compare its level names and measurements with the radiology report and with surgeons' reads, separately for patients with usual and unusual anatomy.
2. **Name the level on the trauma X-ray.** Train the radiograph detector to name vertebrae on DMC trauma films using the CT from the same visit as the answer key, and measure how often a film alone would have led to the wrong level.
3. **Find fractures.** Train and test fracture detection on trauma spine and pelvis radiographs and CT, against the radiology report and the CT.
4. **Link to what happened next.** For trauma patients, relate what the images show to the treatment given and the outcome recorded in the trauma registry, to see which findings changed management.
5. **Teach with it.** De-identified, labelled images become teaching material for students and residents, the same way the public dataset already does.

# What we need, in plain terms

- **Patients.** Every DMC patient from 2006 onward with a CT, X-ray or MRI of the spine, pelvis or limbs, whether they came through trauma or an elective clinic. Adults only for now.
- **Images.** The CT scans, X-rays and MRIs, with their radiology reports, from DMC Radiology (PACS). Intra-operative fluoroscopy where it was archived.
- **Records.** Age, sex, insurance, mechanism of injury, injury severity score, diagnoses and procedures, operative notes, implants, complications, length of stay, disposition, mortality and follow-up, from the EMR and the trauma registry.
- **Identifiers only to link, then removed.** Medical record number, FIN and accession number are used once to match images to records, replaced by a study code, and the key stays on DMC Citrix with the PI. Images leave DMC with all header identifiers removed and any burned-in text checked and removed.
- **A count.** As many records as exist, expected in the tens of thousands, because the unusual anatomy is rare and the program needs hundreds of examples of it. The same number must appear on the WSU form, the protocol document and the DMC application.

# Why DMC

DMC is one of the busiest trauma centers in the country, and its patients are the ones the public datasets under-represent: a largely underinsured, urban population with a heavy burden of high-energy injury. Spine and pelvic fractures in this setting are missed on the first read often enough that the trauma literature treats it as expected. A program that reads every trauma CT and film as it is acquired, names the level and flags the fracture, is built for exactly this place, and it can only be trained and tested here.

# Two protocols, submitted together

**Protocol 1, retrospective (Exempt Category 4, waiver of consent and of HIPAA authorization).** Pull the imaging and records above for 2006 to present, code them inside DMC with the key on Citrix held by the PI, de-identify the images inside DMC, and train and evaluate the models on the WSU research cluster. Two things this protocol is written to allow from the start, so they never need an amendment: release of the de-identified images and labels under a restricted data use agreement to other institutions, and release of the trained model weights, both after a separate WSU determination like 2026 269.

**Protocol 2, prospective (Expedited).** Run the finished models silently on incoming trauma spine and pelvic imaging, with no output shown to anyone treating the patient, and compare them with the formal radiology read and any later imaging. Endpoints: fractures found by the model and missed on the initial read, and level names that disagree with the CT; both adjudicated afterward by a radiologist and a surgeon. No change to care, no contact with patients; waiver of consent requested on that basis. This is the study that says whether the tools are worth putting in front of a clinician, and it is submitted now so it can start the day Protocol 1 delivers the models.

# Risks and safeguards, in plain terms

No patient is contacted, treated differently, or affected. The one risk is a breach of confidentiality, and the safeguards are the ones already approved: coded data, the key on Citrix with the PI, de-identified images only on the WSU cluster, access limited to named study staff, and nothing identifiable ever released. Anything we publish or share is de-identified and goes through a separate WSU determination first, as the current dataset did.
