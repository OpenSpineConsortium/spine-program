# Acquisition screen -- validation against VertebralBodiesCT-Labels (outside the screen)

70 of 70 listed TotalSegmentator v2 cases scored. External truth: fhofmann/VertebralBodiesCT-Labels data.csv (free L6 only; twelve thoracic assumed where T1 is out of field). TotalSegmentator was trained on these CTs, so labeller B is scored on its own training images.

| labeller | L6 called / ext L6 | L6 no count | L6 called as | T13 called / ext T13 | T13 no count | negatives: LS ordinary / n | false L6 | false T13 | LS no count |
|---|---|---:|---|---|---:|---|---:|---:|---:|
| A (SPINEPS+VERIDAH ctd) | 12 / 28 | 6 | {'ordinary': 10} | 5 / 7 | 0 | 30 / 35 | 2 | 0 | 2 |
| B (TS geometric) | 17 / 28 | 9 | {'ordinary': 2} | 0 / 7 | 7 | 24 / 35 | 1 | 0 | 7 |

| ext L6 | ext T13 | combined subtype | tier | n |
|---|---|---|---|---:|
| False | False | ordinary | two-labeller | 21 |
| True | False | review | review | 9 |
| True | False | L6 | two-labeller | 9 |
| False | False | ordinary | single-labeller | 7 |
| True | False | no_count | - | 5 |
| False | False | review | review | 5 |
| False | True | T13 | single-labeller | 5 |
| True | False | L6 | single-labeller | 2 |
| True | False | T13 | single-labeller | 2 |
| False | True | ordinary | two-labeller | 2 |
| False | False | L6 | two-labeller | 1 |
| True | False | ordinary | single-labeller | 1 |
| False | False | no_count | - | 1 |
