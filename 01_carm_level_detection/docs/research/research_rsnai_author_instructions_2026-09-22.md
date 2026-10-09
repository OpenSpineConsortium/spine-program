# Radiology: Artificial Intelligence: author instructions for Original Research (researched 2026-09-22)

## Where these quotes come from, and how current they are

The live pages at pubs.rsna.org are behind a Cloudflare JavaScript challenge. On 2026-09-22 every
scripted fetch returned HTTP 403 "Just a moment...": WebFetch, curl, curl_cffi posing as Chrome,
r.jina.ai, and Playwright driving real Chrome both headless and headed. archive.today has no copy.
Every quote below therefore comes from the **Internet Archive's most recent capture** of the
official RSNA page. The Wayback availability API, asked for the capture nearest 2026-09-22,
returned these (its CDX index was offline, so the full list of captures could not be checked):

| Key | Official page | Wayback capture used |
|---|---|---|
| **AI** | https://pubs.rsna.org/page/ai/author-instructions | https://web.archive.org/web/20250610013331/https://pubs.rsna.org/page/ai/author-instructions (**2025-06-10**) |
| **POL** | https://pubs.rsna.org/page/policies (RSNA-journals editorial policies, linked from AI) | https://web.archive.org/web/20250613064524/https://pubs.rsna.org/page/policies (**2025-06-13**) |
| **CLAIM** | https://pubs.rsna.org/page/ai/claim | https://web.archive.org/web/20250503145025/https://pubs.rsna.org/page/ai/claim (**2025-05-03**) |
| **CLAIM-docx** | https://pubs.rsna.org/pb-assets/AI/CLAIM/CLAIMChecklist-6142024-1718376172847.docx | https://web.archive.org/web/20250503145033/https://pubs.rsna.org/pb-assets/AI/CLAIM/CLAIMChecklist-6142024-1718376172847.docx (2025-05-03) |

The AI page's own "What's New" log ends at "May 2025", a change to the transfer section. **Changes made
after 2025-06-10 cannot be ruled out.** Before you submit, open the live page in a normal browser
and check it against the limits below. A Google snippet seen on 2026-09-22 still showed "no more than
3000 words (Introduction to Discussion)" for Original Research. No third-party summaries were used.

## 1. Main-text word limit: 3000 words, Introduction through Discussion

- **Limit: 3000 words.** "Word count: no more than 3000 words (Introduction to Discussion)". Source: AI, section #original_research.
- **What counts: Introduction through Discussion.** The same line says "(Introduction to Discussion)". The Main Body section says "Original Research (total word count of 3000 words) and Technical Development (total word count of 2000 words) articles use the following headings: Introduction, Materials and Methods, Results, and Discussion." Source: AI, #main_body.
  - The page never says in so many words that the abstract, references, legends or tables are excluded. "(Introduction to Discussion)" is the only definition it gives.
- **Where you declare it.** The Full Title Page must include "Word Count for Text". Source: AI, #full_title_page.

## 2. Abstract: structured, at most 250 words, four sections

- **Limit.** "Original Research and Technical Developments manuscripts must include a structured abstract of 250 words or less divided into four sections." Source: AI, #abstract.
- **The four sections, quoted:**
  - "Purpose: In one to two sentences, succinctly state the study purpose."
  - "Materials and Methods: (1) Identify as prospective or retrospective; (2) Date range of study; (3) Number of patients/animals including age and sex, if appropriate; (4) Describe various groups, including controls; (5) Describe procedures performed; (6) Specifics of evaluation should parallel the results portion of the abstract; (7) Include one sentence on statistical analyses"
  - "Results: Provide the findings in parallel with the Methods and include indicators of statistical significance, actual numbers, and percentages."
  - "Conclusion: Must derive directly from the results. Do not elaborate on the significance or other implications of your study. Must address the purpose of the study."
  - Source: AI, #abstract.

## 3. Required extra elements

- **Summary statement: one sentence, at most 255 characters, in boldface.** "A summary statement (for Original Research and Technical Development papers) of no more than 255 characters in boldface. This should be a single sentence that highlights the key finding in your study." It goes on the anonymized Abbreviated Title Page. Source: AI, #abbreviated_title_page.
  - The article-type block says something looser: "Required Summary Statement: 1-2 sentences summarizing the important findings of your manuscript." (AI, #original_research). The two conflict, so meet the stricter one: a single sentence of 255 characters or fewer.
  - "Do not use abbreviations in the Summary Statement." Source: AI, Units/Abbreviations.
- **Key Points: up to 3, no word limit stated.** "Key Points: Include up to 3 main points/conclusions from your study including summary data. Do NOT repeat your summary statement. Please avoid using vague language and abbreviations in the Key Points. Obvious abbreviations like CT and MRI are fine." Source: AI, #original_research; the same text appears under #abbreviated_title_page.
- **Abbreviations: at most 10.** "A maximum of 10 abbreviations are allowed." Also: "Spell out abbreviations when first used in the abstract and text" and "Define all abbreviations used in figures and tables in the legend." Source: AI, Units/Abbreviations.
- **Keywords: not a manuscript element.** The page asks for none. The nearest rule is a submission-form step: "You are required to select at least two manuscript categorization terms." Source: AI, #aisubmission, Step 3: Attributes.

## 4. Limits on figures, tables, references and supplemental material

- **Figures: 6.** "Figure Limit (images, charts, or graphs): 6". Source: AI, #original_research.
- **Tables: 4.** "Table Limit: 4". Source: AI, #original_research.
- **References: 35.** "Reference Limit: 35". Source: AI, #original_research.
- **Supplemental material: no size or count limit stated.** The page says:
  - "Additional figures may be submitted as supplemental material." (AI, #figures)
  - "Supplemental text, tables, and figures (with captions) should be submitted together in one Word document, separate from the main body manuscript file, and uploaded as a 'Supplemental File for Review.'" (AI, #supplemental_material)
  - "Your Supplemental Materials will not be copyedited." (AI, #main_body)
  - Movies should stay "less than 30 MB" unless there is a compelling reason. (AI, #supplemental_material)
  - Accepted content includes "(5) algorithms; (6) Jupyter notebooks; and (7) annotated image sets." (AI, #supplemental_material)

## 5. Reporting checklist and data and code statements

- **A checklist is mandatory at first submission.** "Upon initial submission of Original Research and Technical Development papers that involve human subjects, you will be required to choose the checklist that is applicable to your study … Note: Your paper will be sent back if this checklist is not included upon first submission." It is also listed as a separate file to "Submit separately: … Checklist (Original Research and Technical Development papers only)". Source: AI, #checklist and #main_body.
- **The instructions name CLAIM, but cite the 2020 version.** "For AI manuscripts in medical imaging, use the Checklist for AI in Medical Imaging (CLAIM) ( Radiology: Artificial Intelligence 2020 doi:10.1148/ryai.2020200029 )." The page's "Get the CLAIM Checklist (Word)" link points to the older file `…/PIA/Toolkit/CLAIM - Checklist for AI in Medical imaging.docx`. Source: AI, #checklist.
- **The 2024 update is offered on a different page, and is encouraged rather than required.** "we encourage the use of CLAIM" … "Microsoft Word® document: CLAIM Checklist (2024 Update). This document is available to be filled out and submitted with your manuscript." Source: CLAIM.
  - **No official page found says "CLAIM 2024 is required."** The requirement is "CLAIM", and the page that states it cites 2020. Submit the 2024 Word file: it is the version the journal distributes. The 2024 update is Tejani et al, Radiol Artif Intell 2024;6(4):e240300, doi:10.1148/ryai.240300.
  - The RSNA-wide policies page lists only "Checklist (STARD, CONSORT, PRISMA, or STROBE)". CLAIM is absent there (POL, #checklist).
- **Data sharing statement: required on the full title page, in one of four verbatim forms.** "The submitted manuscript must contain a data sharing statement on the full title page that indicates whether individual deidentified participant data will be shared; what data in particular will be shared; … when the data will become available and for how long; and by what access criteria data will be shared." Then: "Authors must include one of the following statements verbatim:"
  - "Data generated by the authors or analyzed during the study are available at: (author provides citation to data)."
  - "Data analyzed during the study were provided by a third party. Requests for data should be directed to the provider indicated in the Acknowledgements."
  - "Data generated or analyzed during the study are available from the corresponding author by request."
  - "All data generated or analyzed during the study are included in the published paper."
  - Source: POL, #clinical. The AI page's Full Title Page list includes "Data sharing statement. See /page/policies#clinical for details."
- **Code: requested in a public repository on publication.** "We request that all computer code used for modeling and/or data analysis be deposited in a publicly accessible repository upon publication." Authors "should indicate in the Materials and Methods section of their article: A link to the webpage where the software can be found, and The unique identifier for the revision of the code used in the publication." They must also "maintain the archived software and published link … for a period of at least five years after publication." Source: POL, #algorithm.
  - For code with commercial or security conflicts: "code-sharing arrangements that facilitate reproduction of the work should be discussed with the Editor." Source: POL, #algorithm.
- **The CLAIM 2024 checklist has a matching item.** Item 43 reads "Statement about the availability of software, trained model, and/or data". Source: CLAIM-docx.

## 6. Figure legends, file formats and multi-panel figures

- **Legends: no word limit found.** The page gives content rules only. "All abbreviations used in figures and figure legends need to be defined in the figure legend." "Do not duplicate text material." "The legend must describe all labels placed on an illustration." "For drawings and graphs, the legend must state the important points to be observed." Source: AI, #legends.
  - Placement: "For new submissions, figure legends should appear directly after the relevant figure in the combined figure text document. For revised manuscripts, all figure legends should appear collectively on one or more pages at the end of the main document." Source: AI, #legends.
- **Multi-panel figures: up to four panels each.** "Number figures (figure 1a, figure 1b, figure 2) and include no more than four components (a, b, c, d) for each figure." Source: AI, #figures.
  - **The page never says whether a multi-panel figure counts as one figure toward the limit of 6.**
    - The Original Research limit reads "Figure Limit (images, charts, or graphs): 6".
    - The Technical Developments and Data Resources limits read "(individual images, charts, or graphs)". Read strictly, "individual" could mean each panel counts.
    - Collages: "Radiology: Artificial Intelligence accepts figures grouped as a collage if the relationship requires arrows/tags to convey meaning."
    - At revision: "If figures are multi-part, submit each figure part as a separate figure file and enter a separate legend/citation for each part."
    - Source: AI, #figures.
- **Initial submission.** "For new submissions, figures should be combined into one text document in the order they appear in the text, with figure legends immediately following the relevant figure." Source: AI, #figures.
- **Revision and production files.** Source for everything in this list: AI, #figures.
  - **Images:** "Formats: PSD (Photoshop), TIF, AI, and EPS, unflattened vector files. PNG files are not accepted." "Resolution: 300 dpi". "Size: minimum of 3 inches to a maximum of 7 inches."
  - **Graphs:** submit "in Photoshop (.psd), TIFF (.tif), Powerpoint (.ppt), AI (.ai), or encapsulated Postscript (.eps) format at 1200 dpi. Layers should be retained (do not "flatten" the image), and image should not be upsampled."
  - **Collages:** "Resolution: minimum of 300 dpi if substantial text/labeling." "Size: 3 inches for each image." "Labels: san-serif font, such as Arial, bold, point size 12 or larger."

## 7. Preprints and statistics

- **Preprints: allowed before submission.** "Authors may post their article on preprint servers such as arXiv.org . Such a post does not count as a prior publication." Source: AI, #preprintpolicy, "Before Submission".
  - **After submission, the page lists where the submitted version may be posted, and arXiv is not on the list.** The list is "On the author's personal website or their employer's website; On institutional or funder websites, if required; In the author's own classroom use". Those postings must carry: "This work has been submitted to Radiology: Artificial Intelligence for possible publication. Copyright may be transferred without notice, after which this version may no longer be accessible." Source: AI, #preprintpolicy.
  - **On acceptance:** authors who posted "arXiv.org or similar preprint server" versions must "replace the submitted version with the accepted version and add the RSNA copyright notice (© 20XX RSNA)", and "The posted article must be removed from any other third-party servers." Source: AI, #preprintpolicy.
  - **Disclosure:** "Authors should disclose details of preprint posting, including DOI and licensing terms, upon submission" (POL, #preprint). Also: "Radiology: Artificial Intelligence asks authors to disclose where and when earlier version(s) of the submitted manuscript were presented and to provide access to those version(s)" (AI, Plagiarism).
- **Statistics: no rule requiring confidence intervals was found in the author instructions.** What they do require:
  - "These articles require appropriate statistical analyses." (AI, #original_research)
  - "State the statistical methods used to analyze the data. Mention the statistical software used, along with version and manufacturer information. State the P value used for significance. A statement of justification of sample size and/ or power calculation is strongly recommended." This goes in the last paragraph of Methods. (AI, #main_body)
  - "Provide numerators and denominators for all percentages, including sensitivity, specificity, accuracy, positive predictive value, and negative predictive value. Regression coefficients or mean values of compared groups must be given along with P values." (AI, #main_body)
  - "Report the results of the statistical analyses for all variables collected and analyzed, not just for those which exhibited statistical or near statistical significance." (AI, #main_body)
  - **Uncertainty is required through CLAIM 2024 instead.** Item 29: "Statistical measures of significance and uncertainty". Item 37: "Performance metrics and measures of statistical uncertainty". Item 38: "Estimates of diagnostic performance and their precision". (CLAIM-docx)

## 8. Other article types that could suit a technical-development paper

- **Technical Developments.** "Technical developments provide a brief description and results of new algorithms, equipment, or datasets. These are typically exploratory feasibility studies. … The Introduction and Discussion are more limited than in Original Research articles." Source: AI, #technical_developments.
  - Limits: "no more than 2000 words (Introduction to Discussion)"; "Abstract: Structured and no more than 250 words"; "Reference Limit: 25"; "Figure Limit (individual images, charts, or graphs): 6"; "Table Limit: 2"; Summary Statement required.
  - Key Points are not listed in this block. The Abbreviated Title Page asks for Key Points in general, with "Type 'N/A' if your study has none."
  - A checklist is required, as for Original Research.
- **AI in Brief.** "AI in Brief articles describe original research that applies previously described AI techniques to new or previously addressed challenges … may be smaller in scale than Original Research articles." Source: AI, #aiinbrief.
  - Limits: "Word count: 1500 words"; "Abstract: Unstructured and no more than 200 words"; "Reference Limit: 20"; "Figure and Table Limit: 4"; summary statement; "Key points: up to 3".
- **Data Resources.** 1200 words; "Abstract: none"; 25 references; 3 figures; 2 tables. Since October 2023 these must follow separate guidelines. Source: AI, #data_resources.
- **Special Reports.** "some original data but not a full scientific study". 6500 words; 250-word abstract; 100 references; 6 figures; 2 tables. Source: AI, #special_reports.

## Other rules that constrain a concise manuscript

All from AI unless marked.

- **Double-anonymized review.** The journal "uses a double-anonymized peer-review process." "Do not mention the author(s)' institution or funding information in the manuscript." "Avoid language that reveals work previously published by the submitting authors' group."
- **File format: LaTeX is accepted only for the first submission.** "Authors may submit an initial manuscript as a Word document, an Adobe Portable Document Format (PDF) document, or as a LaTeX file. … Please note that LaTeX files (.tex) cannot be used for production of accepted articles." (#aisubmission, Step 2)
- **Text layout:** "Double space all text"; "Use basic fonts such as Arial, Calibri, or Times New Roman at 11 points"; "Do not number the pages of the manuscript."
- **Wording:** "Avoid self-evaluation of your work, for example, 'novel,' 'unique,' 'ground-breaking.'"
- **Authors:** "Each manuscript may have at most two first authors. More than 20 authors requires Editor consent."
- **Tables:** "Do not use the merged cell feature of Word. Use sub-headings instead."
- **Declaring AI tools (POL, #llm):** "At submission, authors must disclose whether they used AI or AI-assisted technologies in the preparation of the manuscript." They must describe that use "in both the cover letter and the manuscript".
