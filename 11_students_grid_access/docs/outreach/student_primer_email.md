<!-- spine-program/11_students_grid_access copy record. Source: OpenSpineConsortium/CTSpinoPelvic1K master 7ddfe38, 7ddfe38, path proposals/student_primer_email.md. Copied 2026-10-08. Redactions applied by kind: lead address (1), student names (1). Any laptop path or short prefix inside this text is the source's own wording and is history, not a dependency of this folder; the live reference is the repository at the commit named. -->

**To:** OpenSpineConsortium students
**Subject:** CTSpinoPelvic1K goes to the journal, a new onboarding primer, and two datasets that need you

Hi everyone,

Three things, and the first is the good one.

**The CTSpinoPelvic1K paper is about to be submitted.** The dataset article goes to *Medical Physics* this week, and eleven of you are on it as coauthors: Ashley Schehr, who led the annotation effort and edited the manuscript, and [ten student annotators, names struck], who annotated the data. Dr. Ismoilov and Dr. Alnabahneh graded the transitional vertebrae and trained you in CT reading. The release itself is public now, version 10, at https://doi.org/10.5281/zenodo.22642578 and on Hugging Face at https://huggingface.co/datasets/OpenSpineConsortium/CTSpinoPelvic1K. That is 802 patients with the spine, sacrum, S1, pelvis, femora and every rib labeled on one frame, and it exists because of your work. Congratulations, and thank you. You will get the draft for your approval in a separate message with a sign-off sheet.

**There is now an onboarding primer, and a place for your own projects.** The consortium site has a new Onboarding tab: https://openspineconsortium.com/onboarding/. It assumes no coding experience and takes you, in order, through installing VS Code and Claude Code, getting an account and an SSH key on the WSU grid, teaching Claude how the grid works, downloading CTSpinoPelvic1K and understanding what is in it, and running a complete population-level study that I ran today on all 802 records (whether the female pelvis is relatively wider than the male pelvis; the honest answer, for the measurement we chose, is no, and the primer explains why that is the lesson). The last section is how to propose a project of your own.

Projects live in a new private repository, https://github.com/OpenSpineConsortium/Student_Projects. To get access, email me your GitHub username. The procedure is short. Copy the proposal template, fill in one page (the question, exactly what you will measure and from which labels, who you compare, the analysis, milestones), and open a pull request that adds your proposal folder. The pull request template asks for the email address you want your ClickUp invitation sent to. Once we have gone back and forth in the review and the proposal is approved, I merge it and you get the ClickUp invitation, and from then on your milestones are tracked there. Pull request #1 in that repository is a worked example to imitate. The dataset can answer a lot of questions: any bone dimension by sex, age or posture; anything about the transitional vertebrae; anything about the sacrum and pelvis together. Bring the question you actually want answered.

**Two new datasets need annotators.** CTSpinoPelvic1K was the first. Next are XRSpinoPelvic1K, the radiograph counterpart, which needs X-ray annotation, and VerseFusion, a full-spine CT dataset, which needs vertebral annotation across the whole column. Both follow the same workflow you already know, and both lead to the same place: a public release and a dataset paper with the annotators as coauthors. If you want to be part of either, reply with which one and roughly how many hours a week you can give it, and I will set you up.

If you are new and none of this makes sense yet, start with the primer and email me when you get stuck. That is what it is for.

Greg

Gregory Schwing, MD, PhD
Department of Surgery, Detroit Medical Center and Wayne State University
[the lead's university address]
