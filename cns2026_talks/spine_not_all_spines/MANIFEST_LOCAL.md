# Not All Spines Are Created Equal (MP4SP1): what was copied, from where, and what was left out

Copied on 2026-10-23 for issue #224 by `stage.py` and checked by `pd_scan.py`, `office_attrs.py` and `redact.py` (session scripts, not kept). 214 files, 120.7 MB. A source is spelled with the markers of the root CLAUDE.md (`<laptop:Desktop>`, `<laptop home>`); the md5 is the source file's, taken before any redaction, and git stores text files with LF line endings, so a text file's bytes here can differ from its source by line endings alone.

## Edits made to the copies (CLAUDE.md rules 1 and 12)

| Kind | Files |
| --- | --- |
| researcher e-mail address, replaced by [withheld e-mail] | 3 |
| student name in a text file, replaced by [student A-J] | 12 |
| the banned word in the forbidden-word tuple, spelled in two parts | 2 |

Each edited file is marked in the table at the end. No value that was withheld is written here.

## Left out

| Source | Bytes | Why |
| --- | ---: | --- |
| `<laptop:Desktop>/CNS2026_Schwing_SchwingNet_CNStemplate.pptx` | 13608401 | byte-identical to decks/CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx (md5 aa8df26f) |
| `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/figure2/figure2_map.npz` | 129790 | an array (.npz, kept out by .gitignore); read by prep_v14_figs.py for the level map |
| `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/figure2/occlusion_clean/gradcam.npz` | 12001193 | an array (.npz, kept out by .gitignore); read by prep_v12_figs.py and prep_v14_figs.py for the occlusion map |
| `<laptop:Desktop>/CTSpinoPelvic1K-1/3474_Not_All_Spines_Are_Create.pdf` | 3181182 | the anonymous NeurIPS submission, superseded by the camera-ready copied under CTSpinoPelvic1K/CAMERA_READY_NEURIPS |
| `C:/Windows/Fonts/arial.ttf` | 1045720 | system font, licensed with Windows |
| `C:/Windows/Fonts/arialbd.ttf` | 989780 | system font, licensed with Windows |

## Every copied file

| Path here | Source | Bytes | md5 of the source | Edited |
| --- | --- | ---: | --- | --- |
| `CTSpinoPelvic1K/2026 CNS AM Speaker Powerpoint Template.pptx` | `<laptop:Desktop>/CTSpinoPelvic1K-1/2026 CNS AM Speaker Powerpoint Template.pptx` | 2342329 | `d9277581534b3db53f0ef80c2a459647` |  |
| `CTSpinoPelvic1K/ACCME Accreditation Guidelines for Posters and PowerPoint Presentations.pdf` | `<laptop:Desktop>/CTSpinoPelvic1K-1/ACCME Accreditation Guidelines for Posters and PowerPoint Presentations.pdf` | 50287 | `06bb480c730d8f0a9d7afd63add15c4f` |  |
| `CTSpinoPelvic1K/CAMERA_READY_NEURIPS/src/neurips_2026.pdf` | `<laptop:Desktop>/CTSpinoPelvic1K-1/CAMERA_READY_NEURIPS/src/neurips_2026.pdf` | 1071520 | `4d99a2f4b1a62bcebf14037b038f4230` |  |
| `CTSpinoPelvic1K/paper/cns2026/abs418_tables.json` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/abs418_tables.json` | 1873 | `9b20a8ca3ee0787b1b8d2b7075b6ed91` |  |
| `CTSpinoPelvic1K/paper/cns2026/chart_level_sweep.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/chart_level_sweep.py` | 12286 | `1986a9afaaab417fe690b6b0631628af` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_anchors.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_anchors.png` | 317041 | `d353b46f2b008483b3e8521517fece9a` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_architecture.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_architecture.png` | 190755 | `16fb1aae1092a3101c4c2118d6ddc00e` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_capabilities.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_capabilities.png` | 109408 | `56bcedd93942ccdfdebde32cb5c6373b` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_countfree.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_countfree.png` | 104545 | `b49d0b57a2155a5db0aef57378920035` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_fov.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_fov.png` | 22880 | `382551c9ab3823791837f42ab1eb3fd3` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_hardware.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_hardware.png` | 260576 | `37c83f01bf781401aefdf652c77aeecc` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_levelatlas.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_levelatlas.png` | 128992 | `7d10051ba04b62834cb0b4e009302297` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_patch_context_0376.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_patch_context_0376.png` | 161941 | `25635124e9edf6313c59648482ea30af` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_pipeline.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_pipeline.png` | 143146 | `ffe8a04c38d7d8e39daf40d3d3a07b4f` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_pipeline_oneshot.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_pipeline_oneshot.png` | 150219 | `ff048af04a30e55b1b46f57dd8747894` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_training.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_training.png` | 169326 | `ddac500974152976b0944bc4498204ab` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/fig_validation.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/fig_validation.png` | 53356 | `cebad7b09aaf8e8f033e0e9e32cc6169` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/pelvic_width.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/pelvic_width.png` | 165529 | `b73392aeedce2063eda7780c99227557` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/reading_sheet_0376.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/reading_sheet_0376.png` | 679108 | `b7c6d3bd7683a7a31b6653e34ffa711b` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs/six_lumbar_readings.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs/six_lumbar_readings.png` | 125369 | `c991fb8d3b49c6689e2accc7827e3b95` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/ajnr2023_fig1.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/ajnr2023_fig1.jpg` | 95905 | `e241f6452b7565c83ff363df5d2248c2` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/bettis2026_article.html` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/bettis2026_article.html` | 261424 | `d9e88818c609cafd070aeff90be784d2` | researcher e-mail address, replaced by [withheld e-mail] (3) |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/bettis2026_fig1.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/bettis2026_fig1.png` | 442001 | `285a4d8ce200982b0a5cc24bf59ddd64` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/bettis2026_fig1_digitised.csv` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/bettis2026_fig1_digitised.csv` | 954 | `e76488cf974062e5b7a6f06fa6998b2c` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/bettis2026_fig2.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/bettis2026_fig2.png` | 4059 | `4ae7fa4b658d324038a0495a08bfb280` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/bettis2026_fig3.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/bettis2026_fig3.png` | 4059 | `4ae7fa4b658d324038a0495a08bfb280` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/childers2018_fig1.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/childers2018_fig1.jpg` | 45497 | `393a4d6d367ecccf546da718e3880a7d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/desilva2016_fig1.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/desilva2016_fig1.jpg` | 139527 | `4a99d6583e1dea5dcab59a82634e260a` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/desilva2016_fig4.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/desilva2016_fig4.jpg` | 126670 | `dade9825d38384bf158d96ddc9114019` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/furuya2026_article.html` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/furuya2026_article.html` | 333112 | `bea2096ab92e30f77a0301711488d13f` | researcher e-mail address, replaced by [withheld e-mail] (6) |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/machin2018_article.html` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/machin2018_article.html` | 289512 | `a842d928d8ed0268a720fb119b2ad605` | researcher e-mail address, replaced by [withheld e-mail] (3) |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/machin2018_fig1.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/machin2018_fig1.png` | 96770 | `eab155931a9d40bf210e6bbab00f4bc3` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/machin2018_fig2.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/machin2018_fig2.png` | 133415 | `e468d92e783634b7b1e01ef9f365bc8b` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/machin2018_fig2_digitised.csv` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/machin2018_fig2_digitised.csv` | 870 | `3f1d9dcc970d6de3228edda280f717a1` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/manbachi2018_fig2.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/manbachi2018_fig2.jpg` | 135546 | `1883d9afa506a813c26d5901cae9d1ba` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/manbachi2018_fig6.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/manbachi2018_fig6.jpg` | 85150 | `da77da70b000aab9fceca2f87d80a6bf` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/otake2012_fig14.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/otake2012_fig14.jpg` | 35232 | `72ffd7be9af0eca3a7e4100adf47920d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/otake2012_fig6.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/otake2012_fig6.jpg` | 38087 | `5750b741c9347f582854977577689214` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/sabri2025_article.html` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/sabri2025_article.html` | 2263 | `62efddaae57863afa0257c68508a0236` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/strong2021_fig2.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/strong2021_fig2.jpg` | 363123 | `934b3a17dfd4e6ad3fa8970f078499db` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_cited/strong2021_fig3.jpg` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_cited/strong2021_fig3.jpg` | 221711 | `abc049afb419519ee93ab2e7c2b70415` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_public/chart_pub_castellvi.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_public/chart_pub_castellvi.png` | 84413 | `11d9fef5ae179b786e22ee71cbdc410f` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_public/chart_pub_gain.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_public/chart_pub_gain.png` | 118511 | `1041ef613d54b906a2259897eb1c933d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_public/chart_pub_l6.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_public/chart_pub_l6.png` | 85308 | `8662341e5c3ed7caaa750bafefafdb7e` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_public/chart_pub_levels.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_public/chart_pub_levels.png` | 133462 | `a75a1d40db018147a3a091b8a0dd2096` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_public/mpda/fig_hardware.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_public/mpda/fig_hardware.png` | 514601 | `4178f35035d9691c8925fd1775970907` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_public/mpda/fig_pipeline.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_public/mpda/fig_pipeline.png` | 192600 | `77f75f6f96ef3bb24a43f95d6aa19a74` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_public/mpda/fig_validation.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_public/mpda/fig_validation.png` | 76001 | `625cbf6286a0d59c51b5f8567ad3284d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_public/public_numbers.json` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_public/public_numbers.json` | 978 | `2ae4c1201bf0a66e890bfba3ade77cc1` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig1_ct_row.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig1_ct_row.png` | 865770 | `f59ad6f4609376e391671e666464915c` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig1_ct_vs_film.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig1_ct_vs_film.png` | 928785 | `23e25db0716a27524493b890f528ae0f` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig2_a.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig2_a.png` | 500287 | `df6c5c2cfd4e30d01d4b65c48b0f9dc7` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig2_ab_side.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig2_ab_side.png` | 924933 | `076a48dd9abb45244a6e4b00e6576e05` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig2_b.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig2_b.png` | 273876 | `3e6a86575dfd63911d535063262a24e8` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig4_ab.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig4_ab.png` | 602540 | `6aac0f257ae8ca828ded7b74f0261939` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig4_c.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig4_c.png` | 271896 | `eb79d775ab4a824f265ca9c02fd16f2e` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig4_cd.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig4_cd.png` | 545156 | `62abda43946fd782406b1c5c32972356` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig4_d.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig4_d.png` | 280832 | `c0d11bc1dc7aa3d8b016f5cbca10a3e1` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig5_a.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig5_a.png` | 129590 | `4ede122da9ba39c460cf759b44aef8b0` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig5_b.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig5_b.png` | 88140 | `8ddda4581b69b125ee569a561266fd5e` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_fig5_cd.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_fig5_cd.png` | 266984 | `28d3f1aee377a9e211318bf22546f163` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_figS1_a.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_figS1_a.png` | 368261 | `f765607938e896278c5f407b76dbf3e8` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_figS1_legend.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_figS1_legend.png` | 11395 | `6c66fe26d8b3329d491a1eff3aa2e6cc` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_figS5_a.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_figS5_a.png` | 695090 | `0132f1d7ecdf7718074e55af62952b79` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_figS5_a_grid.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_figS5_a_grid.png` | 702987 | `5e31629da55e0e5fb6b1ab75f438a062` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_figS5_ab.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_figS5_ab.png` | 836151 | `dc658ca28784c4ee9aa143941affa625` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_figS5_b.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_figS5_b.png` | 127530 | `97c1986f6c170e2540de36c1119743d2` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/big_gallery_trio.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/big_gallery_trio.png` | 389883 | `f3774d319bc1205192c32c886cdf578d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/board_wrongsite_cost.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/board_wrongsite_cost.png` | 640656 | `494a48e17ae850b0256c86d0fe1d46ce` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/cartoon_sweep.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/cartoon_sweep.png` | 119849 | `25c0bb52d6a46003be73bb040274af3d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_bettis_redrawn.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_bettis_redrawn.png` | 351672 | `2586230e0aef6cded530248c92cc36b9` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_census.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_census.png` | 139702 | `98d50447c008270e937999f272208005` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_census_cumulative.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_census_cumulative.png` | 317676 | `0522ba7b3eca980cfc09fe0a6792df0e` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_census_map.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_census_map.png` | 287716 | `52718980cce5d935624ea95ac427b35b` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_corpus.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_corpus.png` | 258325 | `b9a8f47df6ae295d6932c1dc607fcc02` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_costs.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_costs.png` | 220603 | `acd995d5100fb2119aaae6a97acc86b8` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_coupling.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_coupling.png` | 282213 | `a1591dd79b21f82e1c83a5fcf2bfa9b0` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_coverage.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_coverage.png` | 117209 | `647a6c51baf1ac3897c582b1eeabe260` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_fig5a_census.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_fig5a_census.png` | 484884 | `ba363e43f954e04e78e40906edf355c7` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_fov_lines.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_fov_lines.png` | 179797 | `77d8d560b6c856d4af39bb8c5e6a030b` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_headline.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_headline.png` | 170866 | `4bf7853250910ac8a33aa10876a97221` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_l6.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_l6.png` | 138243 | `7ce94e86a6735f3bfb9d3cc5816891b7` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_level_accuracy.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_level_accuracy.png` | 245873 | `31b4f41274f8b7e66bd1f83d41cf02d8` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_level_sweep.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_level_sweep.png` | 363325 | `e1c580a0211b7b624d0772071e4931ab` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_machin_redrawn.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_machin_redrawn.png` | 340585 | `77ecd5e3f813c24b2a083329b775fe53` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_power_with_census.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_power_with_census.png` | 480735 | `20c401c92bd286e72471020a97fa6fe0` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_priorart.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_priorart.png` | 184325 | `9b09d984afa47fac1630e4ee8c752825` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_rates.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_rates.png` | 253229 | `255604fbf7c5cf4d5f60d708fe71972b` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/chart_testset.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/chart_testset.png` | 167268 | `dd3daafbb93c79ee6894c7e9dff20103` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/cited_bettis_fig1.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/cited_bettis_fig1.png` | 448161 | `78548f9669cc5939d7f7fbfbb3c8a887` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/cited_cost_composite.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/cited_cost_composite.png` | 1060842 | `3a263e791f12545b0c0be82220f6de98` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/cited_levelcheck_composite.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/cited_levelcheck_composite.png` | 1076681 | `51e1b17550e0d07677f71975485f373a` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/cited_strong2022_fig3.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/cited_strong2022_fig3.png` | 318941 | `ea9e504701698e41e70bba988e202c3a` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/claims.json` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/claims.json` | 3226 | `0302d0a463f5dc5014abdabf3e4523a0` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/diagram_disclosure.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/diagram_disclosure.png` | 150610 | `bdd462b1b5e43cadc0058e2dda11caf1` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig2_wide.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig2_wide.png` | 1121039 | `6541b6cd68eb624df5b0ae94ed3f0a62` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_anchors.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_anchors.png` | 618745 | `4d3315f8d4f7cea918e93aa3daf46f38` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_countfree.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_countfree.png` | 119091 | `0a6ff8044846cfdfb25d4b4e30de19a3` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_fov.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_fov.png` | 27509 | `64ea125e5dc03d60e247f5b6a17adb9c` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_hardware.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_hardware.png` | 414779 | `d9aff94fcb34e3084ac448c725ecbf7d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_levelatlas.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_levelatlas.png` | 112579 | `f4433999afb17954cbacf99df60f9150` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_opportunistic.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_opportunistic.png` | 98903 | `80bdd24b733e5fa98353a80b37a0d842` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_phenotypes.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_phenotypes.png` | 430104 | `97840af6bc2d1013ffb58b0fbe2f56be` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_pipeline.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_pipeline.png` | 166708 | `8f2d05caf9290b861792ce05fcd55c34` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_priorart.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_priorart.png` | 163489 | `3352a0354c370092fe212196520c1ca3` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fig_validation.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fig_validation.png` | 65056 | `830bfc4f81dae2df263ed5b47f6ca47f` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/fov_lines.json` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/fov_lines.json` | 1064 | `2299c18f8229b896a688e02f6e12563d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/gallery_case83.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/gallery_case83.png` | 94454 | `1d5cf1a48bc7a8ce9fca6e94f863ad71` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/l6_result.json` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/l6_result.json` | 328 | `948f6b7d83c57dc5bd34a2bf2614431d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/level_accuracy.json` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/level_accuracy.json` | 1420 | `44672de7ee85991dfd151eca3d03c051` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/nas_gt_vs_ts.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/nas_gt_vs_ts.png` | 532422 | `0a80a58271311808dbd09f81e13ef267` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/nas_lumbarization_215.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/nas_lumbarization_215.png` | 631555 | `3ae5311b60f7b807c8ed453328820630` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/occlusion_2x2.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/occlusion_2x2.png` | 950320 | `8cda5ebbbe5c6e93e2d9d820126e4d67` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/occlusion_grid.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/occlusion_grid.png` | 1189462 | `2dfd40b403c5408e7ec056c55d35ff39` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/osc_logo.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/osc_logo.png` | 53444 | `db8c9a4d1a14dd79d84985ae392fbf91` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/osc_mark.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/osc_mark.png` | 11049 | `8102a1bba3e8d4c5cef0f52c73b44bcb` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/pictogram_census.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/pictogram_census.png` | 205465 | `c802919e0de217fa39a37246909cbf31` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/render_case42_L6.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/render_case42_L6.png` | 578647 | `b4b7ae79931cc4e75d268db89fc19e44` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/render_case42_check.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/render_case42_check.png` | 547172 | `9e8c09ebc8a22f281b4436250e7c04b4` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/render_case42_find.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/render_case42_find.png` | 521646 | `23881162c6429440de64a144513c41e8` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_carmlspine_gallery.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_carmlspine_gallery.png` | 887539 | `551ac1a9c0309a8894731a0714f3735c` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_carmlspine_results.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_carmlspine_results.png` | 152953 | `2e9b1de90540879c396cae595c1838d1` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_fig2_ab.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_fig2_ab.png` | 970170 | `f83691859a6f7a6fff5ce1c64a94f78a` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_fig4_a_img.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_fig4_a_img.png` | 292763 | `059ca2b5ba14e684eb2e33ab8b0e636e` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_fig4_ab.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_fig4_ab.png` | 728668 | `e659701394ed2ec493acfcd44720ade0` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_fig4_ab_img.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_fig4_ab_img.png` | 590432 | `7e675c52baefa4f4fa624c6989647c4a` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_fig4_b_img.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_fig4_b_img.png` | 283913 | `c67daa55e6a98b58a95ab76f08e3ffad` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_fig5_a.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_fig5_a.png` | 192276 | `9247fc5e09b88e827591da22c37db901` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_fig5_ab.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_fig5_ab.png` | 305875 | `bd597f5520fdb7c755582b0b1558af64` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_fig5_cd.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_fig5_cd.png` | 291750 | `a15dac303b72d65d67750b439c96b83f` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_figS1_ab.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_figS1_ab.png` | 757764 | `a3488710733e8c7dae7c03fa4655d512` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_figS5_abc.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_figS5_abc.png` | 904665 | `77bbeeb1ea7602ec919849c7a74671f1` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_figure1.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_figure1.png` | 2037289 | `c9002db96b163b0bf8a91e48a83e444a` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sn_table3_rotated.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sn_table3_rotated.png` | 509882 | `17f1e2656334d5eed294cb292ee77513` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sweep_curve.json` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sweep_curve.json` | 6366 | `d1ce88c0f34bd45ab3e7b4224414c1e1` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/sweep_per_level.json` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/sweep_per_level.json` | 22397 | `616fed7dd2a5253fe78bd42eb4ec42d4` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/table_census.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/table_census.png` | 731137 | `13a62f451254236c7918d1a68c2e2237` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/table_claims.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/table_claims.png` | 385027 | `d446832f5b24bc26dd4120e5da9a799e` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/table_corpus.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/table_corpus.png` | 147187 | `c1b4480c60ae0fc93b4d841d507b00cc` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/table_fov.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/table_fov.png` | 194259 | `aa1597d0588d6627219a81c9298d02c6` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/table_levelcheck.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/table_levelcheck.png` | 187036 | `b61ea313da46162c7ad3807bc9351f3d` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/table_modalities.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/table_modalities.png` | 150217 | `b12575cc199d327dda559101ec7e5bcf` |  |
| `CTSpinoPelvic1K/paper/cns2026/figs_v2/table_result1.png` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/figs_v2/table_result1.png` | 333446 | `739588f4b179fed6b09f5359faaaed88` |  |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck.py` | 25600 | `5e9a4c8e4c81d44acac0f5277dc65a91` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v10.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v10.py` | 33807 | `e265b54e29585a0f4b71bc1fdcbace37` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v11_public.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v11_public.py` | 22494 | `4bcde542401571746feab9a6a74c9536` | student name in a text file, replaced by [student A-J] (10); the banned word in the forbidden-word tuple, spelled in two parts (same check) (1) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v12_public.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v12_public.py` | 27089 | `aa48c955efa86ebf6ac0f4274f20bf09` | student name in a text file, replaced by [student A-J] (10); the banned word in the forbidden-word tuple, spelled in two parts (same check) (1) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v2.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v2.py` | 30009 | `92d619e614be12ccaa7ff7a6a57f9864` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v3.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v3.py` | 34474 | `55f504fbbd8db2d0ce11d5d715dcfdbd` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v4.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v4.py` | 28125 | `2fb3e3fe5b2c06511a33fb003d9e730c` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v5.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v5.py` | 25052 | `26aed0ed5d3d73af4e0d0044f8449030` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v6.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v6.py` | 26429 | `d253fbd0a48fdfc612438c1d119c40ab` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v7.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v7.py` | 27852 | `52f62015b1b1f5523e310512be85d718` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v8.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v8.py` | 31160 | `c3d83e0c1bd1e489ea0449633eea50e9` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_cns_deck_v9.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_cns_deck_v9.py` | 32226 | `53647a4fbdfb0e59d568d86c6551a742` | student name in a text file, replaced by [student A-J] (10) |
| `CTSpinoPelvic1K/paper/cns2026/make_v3_charts.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/make_v3_charts.py` | 16425 | `d9b3a88909bc619c2cad9fcbeab2e5ca` |  |
| `CTSpinoPelvic1K/paper/cns2026/posterior/analyze.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/posterior/analyze.py` | 10517 | `a3f57757723466e26af82e4c2b503fc5` |  |
| `CTSpinoPelvic1K/paper/cns2026/posterior/analyze.sbatch` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/posterior/analyze.sbatch` | 814 | `5411657da77c75753df1dfa483e9f396` |  |
| `CTSpinoPelvic1K/paper/cns2026/posterior/fetch.sbatch` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/posterior/fetch.sbatch` | 2707 | `8e3971a4232540a61e0271feed1f4bc5` |  |
| `CTSpinoPelvic1K/paper/cns2026/posterior/predict.sbatch` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/posterior/predict.sbatch` | 2689 | `96dfd690083dfb70e83939e80b6982f7` |  |
| `CTSpinoPelvic1K/paper/cns2026/posterior/submit.sh` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/posterior/submit.sh` | 1994 | `df2850f4ae6d5745853d23f4b0229a83` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_bettis.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_bettis.py` | 8274 | `cc077903f4c66e32ecc3bff46592f288` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_big_panels.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_big_panels.py` | 3710 | `52f040ab3c1598b9abb3e0b66c69a808` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_cited_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_cited_figs.py` | 3536 | `01c73afee29e5a321f909b6372515b6c` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v10_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v10_figs.py` | 8978 | `c2299f1c782593dc42bdc31cc5c9f84f` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v11_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v11_figs.py` | 10878 | `384e805563a191200b9566505f6b3203` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v12_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v12_figs.py` | 9739 | `0aba55256a78ed3f5e6cbdca44e819d8` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v13_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v13_figs.py` | 6939 | `d6a90a1863df307b974910b3e7dbaf31` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v14_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v14_figs.py` | 18678 | `3309a7b211339e2d74f63989e70c6473` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v15_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v15_figs.py` | 7619 | `22baa0b86adfa595d22cf9c0bef5040d` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v16_public_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v16_public_figs.py` | 6772 | `a5558a9316c42c3a080666dd8e02aa5e` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v5_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v5_figs.py` | 8348 | `df885b787863b829f3773a52558ed130` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v6_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v6_figs.py` | 9581 | `4398d19ddc1d1be1b29a75c6e8ed7f1f` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v7_figs.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v7_figs.py` | 6700 | `a623b831bac28048baa7977e205710f3` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v8_table.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v8_table.py` | 7851 | `37b682db1f819d2fbd19e3f2061d5303` |  |
| `CTSpinoPelvic1K/paper/cns2026/prep_v9_claims.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/prep_v9_claims.py` | 6559 | `e2e12c4f4ae493245e58f5966fc6d4aa` |  |
| `CTSpinoPelvic1K/paper/cns2026/render_case42.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/render_case42.py` | 3176 | `2af3705f0f5bb802e6dd26844c18deee` |  |
| `CTSpinoPelvic1K/paper/cns2026/sweep_per_level.py` | `<laptop:Desktop>/CTSpinoPelvic1K-1/paper/cns2026/sweep_per_level.py` | 5832 | `9cd09286b2c3503f3210bba9bf64e6b7` |  |
| `decks/CNS2026_Schwing_LSTV.pptx` | `<laptop:Desktop>/CNS2026_Schwing_LSTV.pptx` | 2276047 | `aaf418aa687c889cf5049965f587454e` |  |
| `decks/CNS2026_Schwing_NotAllSpines_public_v11.pptx` | `<laptop:Desktop>/CNS2026_Schwing_NotAllSpines_public_v11.pptx` | 6181487 | `bd64e7fc1b8b89ac63683fb340512001` |  |
| `decks/CNS2026_Schwing_NotAllSpines_public_v12.pptx` | `<laptop:Desktop>/CNS2026_Schwing_NotAllSpines_public_v12.pptx` | 6945073 | `c18fdb0444b8865c81ce0c6abd6865b7` |  |
| `decks/CNS2026_Schwing_SchwingNet.pptx` | `<laptop:Desktop>/CNS2026_Schwing_SchwingNet.pptx` | 10972555 | `81be3bb673bde6f43507a8f6f3fb4eff` |  |
| `decks/CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx` | `<laptop:Desktop>/CNS2026_Schwing_SchwingNet_CNStemplate_v10.pptx` | 13608401 | `aa8df26fb2644e598a9836c959821c3c` |  |
| `decks/CNS2026_Schwing_SchwingNet_CNStemplate_v9.pptx` | `<laptop:Desktop>/CNS2026_Schwing_SchwingNet_CNStemplate_v9.pptx` | 13806896 | `3dfd9307b88303832520ae4e68493e71` |  |
| `decks/CNS2026_Schwing_Spine_v2.pptx` | `<laptop:Desktop>/CNS2026_Schwing_Spine_v2.pptx` | 6918724 | `60c5c459ef3759973f3aa7a13e9d7253` |  |
| `model_night/sweep_v3/end/jit_skip_open/sweep.json` | `<laptop home>/model_night/sweep_v3/end/jit_skip_open/sweep.json` | 1217803 | `defc7c75e6b9baefe768ad06ef08e1ba` |  |
| `model_night/sweep_v3/ts/ts_c2_ii9_o1_gt/sweep.json` | `<laptop home>/model_night/sweep_v3/ts/ts_c2_ii9_o1_gt/sweep.json` | 2342057 | `6d6141a9839584d0845023d3a7a053c3` |  |
| `model_night/sweep_v3/ts/ts_ii9_o2_gt_fixed/sweep.json` | `<laptop home>/model_night/sweep_v3/ts/ts_ii9_o2_gt_fixed/sweep.json` | 6411496 | `63bc1e8d0396dffd2e70a0c77b529845` |  |
| `spinesurg-ct-nnunet/SchwingNet/LEVELCHECK_MODEL.md` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/LEVELCHECK_MODEL.md` | 45815 | `a94353441ffe08387a75cab00ac46eae` |  |
| `spinesurg-ct-nnunet/SchwingNet/NUMBERS.md` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/NUMBERS.md` | 114508 | `e960ceef91970fd471ce6928bab8947b` |  |
| `spinesurg-ct-nnunet/SchwingNet/figures/fig1d_algorithm.png` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/figures/fig1d_algorithm.png` | 155814 | `04b5761fb3c4b93ef4125ebfc8546b06` |  |
| `spinesurg-ct-nnunet/SchwingNet/figures/figS1.png` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/figures/figS1.png` | 813753 | `78a2f6b6791e99c82802a381c8b32837` |  |
| `spinesurg-ct-nnunet/SchwingNet/figures/figS4.png` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/figures/figS4.png` | 1112817 | `0a7aeae7b7be25d9f6454257aaca54be` |  |
| `spinesurg-ct-nnunet/SchwingNet/figures/figure2.png` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/figures/figure2.png` | 1369688 | `8c833093fea4fa4f15b02cdaa9f7f611` |  |
| `spinesurg-ct-nnunet/SchwingNet/figures/figure4.png` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/figures/figure4.png` | 1612927 | `39e7acf804ffe48d271bf117044f7710` |  |
| `spinesurg-ct-nnunet/SchwingNet/figures/figure5.png` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/figures/figure5.png` | 596623 | `63ee6680d91bbe53718720f2401b44a4` |  |
| `spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed0/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed0.json` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed0/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed0.json` | 16993 | `c403c0a977b5b82e445c0f01b29af5d7` |  |
| `spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed1/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed1.json` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed1/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed1.json` | 16985 | `d5145c7e1ed231e96f4047ad17829387` |  |
| `spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed2/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed2.json` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/alpha_0.3_seed2/mixed_allspine_v9_mixed_kmax4_alpha0.3_seed2.json` | 16999 | `0b37a2bdd7c9b06eac066110a8cd4a07` |  |
| `spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case42_LAT.couple.json` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/fig4_frames/case42_LAT.couple.json` | 3587 | `9b6ec4c0b4146d293145809f4d8755b6` |  |
| `spinesurg-ct-nnunet/SchwingNet/results/fig5_frames/case42_LAT.png` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/fig5_frames/case42_LAT.png` | 427710 | `c90c1c2a89ea82fff60693f1fed179c8` |  |
| `spinesurg-ct-nnunet/SchwingNet/results/figure2/figure2_metrics.json` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/figure2/figure2_metrics.json` | 50739 | `6bb78234719116f7b041d17c1a04a84a` |  |
| `spinesurg-ct-nnunet/SchwingNet/results/figure2/figure2_transitional.json` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/figure2/figure2_transitional.json` | 8989 | `bd24194ef9c88d9cc014228bf1341007` |  |
| `spinesurg-ct-nnunet/SchwingNet/results/power/power.json` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/results/power/power.json` | 119647 | `f69db5819991250164819d4ae1cc8ed2` |  |
| `spinesurg-ct-nnunet/SchwingNet/sections/results.tex` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/sections/results.tex` | 12585 | `9818f391a2073a9efcddf591e3c7d01c` |  |
| `spinesurg-ct-nnunet/SchwingNet/tables/main_p20.png` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/tables/main_p20.png` | 502646 | `ea51bce204139dabce05d67df9bc7118` |  |
| `spinesurg-ct-nnunet/SchwingNet/tables/tab2_detection.md` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/tables/tab2_detection.md` | 10348 | `7f6c2aee50a2a68c81841374d1df4392` |  |
| `spinesurg-ct-nnunet/SchwingNet/tables/tab3_naming.md` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/tables/tab3_naming.md` | 12302 | `a762f9291e4fb744f89383830050c13a` |  |
| `spinesurg-ct-nnunet/SchwingNet/tools/fig_power.py` | `<laptop:Desktop>/spinesurg-ct-nnunet/SchwingNet/tools/fig_power.py` | 54238 | `1c885f32da9235847c2c0c2258e01475` |  |
| `spinesurg-ct-nnunet/docs/CENSUS_TABLE_2026-09-25.md` | `<laptop:Desktop>/spinesurg-ct-nnunet/docs/CENSUS_TABLE_2026-09-25.md` | 10230 | `198e7d549173a00f8df266ed32176714` |  |
| `spinesurg-ct-nnunet/docs/WRONG_LEVEL_COST_EVIDENCE.md` | `<laptop:Desktop>/spinesurg-ct-nnunet/docs/WRONG_LEVEL_COST_EVIDENCE.md` | 19631 | `962faf98a884d08fc71dabd53eea7bd8` |  |
| `spinesurg-ct-nnunet/docs/WRONG_SITE_BURDEN_EVIDENCE.md` | `<laptop:Desktop>/spinesurg-ct-nnunet/docs/WRONG_SITE_BURDEN_EVIDENCE.md` | 18122 | `cb1969e9f8440a2c59851c3c829c7937` |  |
| `spinesurg-ct-nnunet/docs/figures_carmlspine_gallery.pdf` | `<laptop:Desktop>/spinesurg-ct-nnunet/docs/figures_carmlspine_gallery.pdf` | 515727 | `b43608919bdec5f63a86f1cdcf235dc4` |  |
| `spinesurg-ct-nnunet/docs/figures_carmlspine_results.pdf` | `<laptop:Desktop>/spinesurg-ct-nnunet/docs/figures_carmlspine_results.pdf` | 24356 | `237261a8ad4a5103b31b3469709741a9` |  |
