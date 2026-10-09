# Transitional gallery -- the candidate pool per phenotype and what was rendered

Pools are read from each source's own truth, never from a file name: `results/rare_class/transitional_subtypes.csv`
(CTSpinoPelvic1K v11 labels + adjudicated Castellvi reads; VerSe raw masks + the published table; C-ArmLSpine
`levels.json`), the BUU-LSPINE dataset report (`KIOM2022_dataset_report.xlsx`, sheet L4L6), and the C-ArmLSpine
frame meta. Rendered = in `slurm/gallery_spec.json` (grid job 40416670); used = in the figure (`GALLERY_SOURCES.md`).

| phenotype | column | pool | rendered | used | why this one |
|---|---|---|---|---|---|
| L6 | labelled CT, renders | CTSpinoPelvic1K 18 with label 25 (Castellvi: Ib 2, IIa/IIb 9, IIIa/IIIb 4, IV 1, none 2) | 0244 (Ib, "complete lumbarization"), 0565 (IIa) | 0244 | the cleanest L6: a mobile sixth body with no bony bridge; v9 validation split |
| L6 | released radiograph | BUU-LSPINE 15 films marked "L6" (8 of them subjects under 15 y) | 2580-F-031Y1, 3483-F-062Y1 | 2580-F-031Y1 | adult, no burned-in text in the crop, normal disc above the sacrum (9.4 mm) |
| L6 | real C-arm | C-ArmLSpine case42 (val), case121 (train), case136 (test), all VERIDAH-called | case136, case42 | case136 | test split; clean lateral (case121 carries a plate at the top of the frame) |
| T13 | labelled CT, renders | VerSe 6 subjects with raw-mask id 28: verse547, 582, 588, 601, 602, 631 | verse547, verse588 | verse547 | cleaner AP render (verse582 is crossed by cables; verse588's frame shows the same) |
| T13 | released radiograph | none: no released radiograph set carries a T13 label | -- | hatched | |
| T13 | real C-arm | none: the C-ArmLSpine cone-beam CTs are lumbar-only and no T13 was called | -- | hatched | |
| sacralised L5, own label | labelled CT, renders | CTSpinoPelvic1K 3 with five lumbar labels and a IIIb/IV read: 0008 (IV), 0021 (IV), 0049 (IIIb) | 0008, 0021 | 0008 | Castellvi IV, bilateral, the surface shows both bridges |
| sacralised L5 | released radiograph | none: BUU-LSPINE records counts only; CSXA and NHANES carry no Castellvi grade | -- | hatched | |
| sacralised L5 | real C-arm | none called in C-ArmLSpine | -- | hatched | |
| four lumbar | labelled CT, renders | CTSpinoPelvic1K 9 with four lumbar labels (all IIIb): 0094, 0151, 0156, 0158, 0760, 0785, 0787, 0875, 1031 | 0760, 0151 | 0760 | 0785/0787/0875/1031 carry a reader note of possible rudimentary ribs at L1 (a second anomaly); 0760 is v9 validation |
| four lumbar | released radiograph | BUU-LSPINE 129 films marked "L4" | 0233-F-064Y1, 0271-F-062Y1 | 0233-F-064Y1 | adult, clean; fused disc above the sacrum (2.3 mm) |
| four lumbar | real C-arm | none called in C-ArmLSpine | -- | hatched | |

Not used anywhere: TotalSegmentator's 12 SPINEPS+VERIDAH L6 calls (pseudo-truth; CTSpinoPelvic1K and VerSe carry
reader truth for every CT cell); VerSe's 34 `L6_fused` subjects (the fused body is unlabelled in the raw mask, so no
box could mark it); the CTSpinoPelvic1K lumbar-rib cases (a different phenotype).
