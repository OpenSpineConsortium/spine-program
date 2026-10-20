# GitHub Support purge requests (for Greg to file; they must come from the repository owner or an org owner)

File each at https://support.github.com/contact, category "Remove sensitive data / cached views". Attach the SHA list
named below. These are the only steps that stop GitHub serving the SchwingNet material by commit SHA; nothing done
locally can. A purge is irreversible, and the private evidence bundles were taken first:
`/rs/rs_grp_oschome/go2432/private_ip/git_bundles_2026-09-26/` (sha256 verified 26 Sep 2026).

Done on 26 Sep 2026, without Support:
- `Gregory-Schwing-MD-PhD/XRSpinoPelvic1K` was made private. It returned HTTP 404 to an anonymous request.
- CTSpinoPelvic1K 45df97d, pushed to both remotes: the CNS 2026 talk generator was untracked, and the ROADMAP "Landmark model (XR)" section was removed. The file returns 404 at master.
- The TTO package and the disclosure forms were moved out of the public repo folder, to `Desktop\private_ip\`.

---

## Request (a): Gregory-Schwing-MD-PhD/CTSpinoPelvic1K (its network includes the fork usmnashd1/CTSpinoPelvic1K)

> Hello. On 11 Sep 2026 I rewrote the history of Gregory-Schwing-MD-PhD/CTSpinoPelvic1K to remove unpublished documents that were pushed by mistake on 4 Sep 2026 under `proposals/`. No branch, tag or pull request references the removed commits, but they are still served by SHA from this repository and from the fork usmnashd1/CTSpinoPelvic1K in the same network, for example https://raw.githubusercontent.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K/a959ff7da5703ff9ea3c28cfe7ec2b71cc6a4f95/proposals/xr_fracture_detector.md
>
> Please remove the cached views and dereference and garbage-collect the attached 171 commits (the former tip is a959ff7da5703ff9ea3c28cfe7ec2b71cc6a4f95) across the whole network. The affected paths are `proposals/**`:
> xr_fracture_detector.md, XR_Fracture_Detector_Proposal.docx, lab_update_email_2026-09-07.md, irb_amendment_draft.md,
> IRB-21-10-4123_Amendment_Draft.docx, andreea_email.md, annotator_email.md, Annotator_Email.docx, irb/EMAIL.md,
> irb/IRB_PLAN.md, irb/PROPOSAL_SHORT.md, irb/CTSpinoPelvic1K_preprint.pdf.
> Current branches, tags and the open pull request do not depend on these commits. Thank you.

Attachment: `CTSpinoPelvic1K_orphaned_commits.txt` (171 SHAs).

## Request (b): OpenSpineConsortium/CTSpinoPelvic1K (separate network, same commits)

Use the text of (a) with the repository name changed. Example URL:
https://raw.githubusercontent.com/OpenSpineConsortium/CTSpinoPelvic1K/a959ff7da5703ff9ea3c28cfe7ec2b71cc6a4f95/proposals/xr_fracture_detector.md
Attachment: the same list.

## Request (c): OpenSpineConsortium/openspineconsortium.github.io

> Hello. On 14 Sep 2026 I rewrote the history of OpenSpineConsortium/openspineconsortium.github.io with git-filter-repo to remove model weight files under `pacs/models/`. They are still served by SHA, for example https://raw.githubusercontent.com/OpenSpineConsortium/openspineconsortium.github.io/45ae8f14223a0a78b7e10de7fcdf3274d4183543/pacs/models/v11m_640_v4_fp16.onnx
>
> Please remove the cached views and dereference and garbage-collect the attached 106 pre-rewrite commits (the former head is 5559d87947c13983a01e6f8f04dc88de0cec4339; the first changed commit is 4f7987e). The affected paths are:
> pacs/models/v11n_640.onnx, pacs/models/v11n_1024.onnx, pacs/models/v11m_640_v4_fp16.onnx,
> pacs/models/v11m_1024_fp16.onnx, pacs/models/v11m_1024_v4_fp16.onnx.
> The repository has no forks, and the current master (a3f7474) does not depend on these commits. Thank you.

Attachment: `openspineconsortium_site_rewritten_commits.txt` (106 SHAs).

**Alternative to (c), faster but disruptive:** delete the site repository and recreate it under the same name. Push master from a fresh clone of the current remote, never from the Desktop clone. The site is offline until Pages is re-enabled with the custom domain, and the certificate can take up to 24 h. Only do this if Support is slow.

---

## After GitHub confirms, check that each of these returns 404

- https://raw.githubusercontent.com/Gregory-Schwing-MD-PhD/CTSpinoPelvic1K/a959ff7da5703ff9ea3c28cfe7ec2b71cc6a4f95/proposals/xr_fracture_detector.md
- the same path under OpenSpineConsortium and usmnashd1
- https://raw.githubusercontent.com/OpenSpineConsortium/openspineconsortium.github.io/45ae8f14223a0a78b7e10de7fcdf3274d4183543/pacs/models/v11m_640_v4_fp16.onnx
- https://raw.githubusercontent.com/OpenSpineConsortium/openspineconsortium.github.io/4f7987e0b8ec681079394de91c896aaff0a8506b/pacs/models/v11n_640.onnx

**What no purge can remove:** arXiv 2609.22760 v1, the NeurIPS/OpenReview paper, Zenodo 22139642 and 22647933, and any copy anyone already downloaded.
