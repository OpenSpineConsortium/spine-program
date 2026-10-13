# Shared memory index

Each project folder keeps its own MEMORY.md and its own memory/ (one fact per file); a fact about one project lives
there, not here. This file indexes only the facts that hold for the repository as a whole. The 13 project indexes:

- [01_carm_level_detection](../../01_carm_level_detection/MEMORY.md)
- [02_transitional_naming_truth](../../02_transitional_naming_truth/MEMORY.md)
- [03_ctspinopelvic1k_dataset](../../03_ctspinopelvic1k_dataset/MEMORY.md)
- [04_openspinetoolkit](../../04_openspinetoolkit/MEMORY.md)
- [05_ct_morphometry_parity](../../05_ct_morphometry_parity/MEMORY.md)
- [06_transitional_ct_census](../../06_transitional_ct_census/MEMORY.md)
- [07_plain_film_level_id](../../07_plain_film_level_id/MEMORY.md)
- [08_render_devices](../../08_render_devices/MEMORY.md)
- [09_wrong_level_clinical_qi](../../09_wrong_level_clinical_qi/MEMORY.md)
- [10_data_platform_grid](../../10_data_platform_grid/MEMORY.md)
- [11_students_grid_access](../../11_students_grid_access/MEMORY.md)
- [12_website_pacs_demo](../../12_website_pacs_demo/MEMORY.md)
- [99_archive](../../99_archive/MEMORY.md)

## Cross-project facts

One line per fact, `- [title](file-name.md): one line`, in alphabetical order of file name, added with the remember
skill (.claude/skills/remember/SKILL.md) in the same pull request as the change it came from.

- [The claim protocol updates itself](the-claim-protocol-updates-itself.md): tools/sdlc_protocol is symphony-protocol at the release tools/VENDORED records, and .github/workflows/protocol.yml brings each later release in as a pull request from the branch symphony-protocol/sync; how to vendor by hand, and what of the template's worker machinery is not here.
