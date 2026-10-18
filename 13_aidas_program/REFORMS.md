# REFORMS in this program

REFORMS (Kapoor S, et al. Sci Adv 2024;10(18):eadk3452) is a checklist of 32 items in eight modules for science that
uses machine learning. Each study in this program keeps one REFORMS record (`templates/REFORMS_RECORD.md`, task E1.2),
filled as the work goes. The table says, for each module, which tasks fill it and what holds it: a check that runs, or
a person who reads. "Built" means the check exists today; the rest are tasks here.

| module | what it asks | tasks that fill it | what holds it |
|---|---|---|---|
| 1 Study design | the question, the population, the claim, written before the work | E2.1, E2.3, E3.5, E7.1, E8.1, E8.3 | the sealed gate (E1.2); the IRB and the exempt determination |
| 2 Computational reproducibility | code, environment, seeds and data versions that rerun | E1.3, E5.1, E7.3, E7.4 | beethoven-qa's gate (built, E1.3 brings it here); one-command reruns of gated code (to build) |
| 3 Data quality | where each source came from, its labels and their errors | E2.4, E2.6, E3.1, E3.2, E3.4, E4.1, E4.5, E5.2 | the data dictionary and double coding (E3.1, E3.4); a person looks at rendered samples |
| 4 Data preprocessing | each transformation and each exclusion, with counts | E3.2, E3.3, E4.1, E4.2, E5.3 | the counts at every step recorded in the task; renders looked at (root rule 3) |
| 5 Modeling | the models, their selection and tuning, on what data | E1.3, E4.3, E4.4, E5.4, E6.1, E6.2, E6.3, E6.6 | the sealed gate; model and weights hashed |
| 6 Data leakage | no patient, study, cadaver or CT volume in both training and test | E1.4, E4.3, E4.5, E6.3, E6.6, E7.1, E7.2 | beethoven-research's split check (built); the evaluation gate; the cadaver set sealed by hash |
| 7 Metrics and uncertainty | the metrics, intervals and the unit of clustering | E3.4, E3.5, E4.3, E4.6, E5.4, E6.4, E6.5, E7.3, E8.4, E8.5 | intervals clustered by case or patient; pre-registered measures |
| 8 Generalizability and limitations | where the result holds and where it does not | E1.5, E2.5, E6.5, E10.4 | leave-one-device-out; the CLAIM checklist (E1.5, to write); a loss reported as one |

CLAIM 2024 (Tejani AS, et al. Radiol Artif Intell 2024;6(4):e240300) is the imaging-specific checklist beside it; task
E1.5 writes it into beethoven-research, which today plans it and has no item written
(`../01_carm_level_detection/grants/aidas_2027/RECORD.md`, section 1).
