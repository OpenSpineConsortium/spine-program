# COBRA2026 LSTV screen

Generated 2026-09-23 18:46:19 EDT from `/rs/rs_grp_oschome/go2432/data/cobra2026/lstv`.

> Pseudo-truth: every call below is a SPINEPS+VERIDAH model call on ct_def.mha, the planning CT DEFORMABLY REGISTERED to the CBCT -- not a radiologist read and not release truth. The registration can move end plates and VERIDAH's naming is itself a model output; a transitional call that enters the claim's test set gets looked at before it counts.

**Coverage: 692 of 692 cases on disk screened**.

## Per centre and subtype

| centre | ordinary | L6 | T13 | both | four_lumbar | unreadable | total |
|---|---|---|---|---|---|---|---|
| A | 37 | 5 | 7 | 0 | 2 | 69 | 120 |
| B | 76 | 4 | 19 | 0 | 0 | 8 | 107 |
| C | 80 | 1 | 2 | 0 | 1 | 36 | 120 |
| D | 91 | 5 | 11 | 0 | 3 | 10 | 120 |
| F | 46 | 1 | 5 | 0 | 2 | 38 | 92 |
| G | 14 | 22 | 1 | 0 | 0 | 96 | 133 |
| **all** | 344 | 38 | 45 | 0 | 8 | 257 | 692 |

## Transitional cases (91)

- **L6** (38): A158, A162, A172, A213, A270, B015, B041, B067, B127, C129, D004, D015, D238, D244, D271, F108, G010, G055, G061, G095, G096, G103, G111, G113, G127, G143, G155, G159, G161, G163, G164, G178, G190, G193, G194, G202, G203, G206
- **T13** (45): A024, A043, A053, A260, A268, A283, A302, B000, B002, B005, B012, B022, B026, B028, B066, B083, B084, B085, B091, B095, B102, B106, B111, B126, B141, B147, C156, C170, D014, D054, D138, D254, D357, D389, D405, D501, D504, D516, D548, F003, F017, F037, F102, F118, G039
- **four_lumbar** (8): A026, A072, C101, D152, D391, D484, F058, F089

## Unreadable, by reason

- 120 x lumbar set cut by the FOV (seen L2+L3+L4+L5, cranial-most is not L1)
- 66 x lumbar set cut by the FOV (seen L3+L4+L5, cranial-most is not L1)
- 40 x lumbar set cut by the FOV (seen L4+L5, cranial-most is not L1)
- 9 x spineps/convert failed: RuntimeError('spineps exited 1: ravel()) if int(arr.max()) > 256 else cc3dstatistics(arr, use_cr
- 5 x lumbar set cut by the FOV (seen L5, cranial-most is not L1)
- 3 x lumbar set cut by the FOV (seen L2+L3+L4, cranial-most is not L1)
- 3 x VERIDAH ctd naming failed its checks: instance 26 holds the points of L6+sacrum
- 3 x L1-L4 above the sacrum but no thoracic vertebra in the field to confirm the count
- 2 x spineps/convert failed: RuntimeError('spineps exited 1: avel()) if int(arr.max()) > 256 else cc3dstatistics(arr, use_cro
- 2 x no lumbar vertebra labelled
- 1 x VERIDAH ctd naming failed its checks: L6 (S 94.2 mm) is not above sacrum (S 94.7 mm)
- 1 x VERIDAH ctd naming failed its checks: instance 26 holds the points of L5+sacrum
- 1 x VERIDAH ctd naming failed its checks: instance 24 holds the points of L5+L6
- 1 x VERIDAH ctd naming failed its checks: instance 18 holds the points of T10+T11

## Lumbar count (readable cases)

2 lumbar: 19, 3 lumbar: 6, 4 lumbar: 17, 5 lumbar: 382, 6 lumbar: 11
