# What the device cards do not reproduce

Standardised mean difference (Cohen's d) between a STYLED RENDER and a REAL FRAME of the same device, per image statistic, with a 2,000-resample cluster bootstrap. |d| >= 0.8 is a large difference; the sign says which way. The right-hand column says whether a fitted term owns that statistic (its value is wrong) or no term does (it is missing from the model).

## cios_fusion: styled `styled cios_fusion on cios_fusion poses` (370 frames) vs real `DeepFluoro` (366 frames)

| statistic | d [95 % CI] | styled mean | real mean | owned by |
|---|---|---|---|---|
| field_frac | **+14.19** [11.74, 19.27] | 1 | 0.9672 | NO TERM: collimation / field shape |
| g99 | **-7.19** [-8.46, -6.31] | 3.636 | 5.906 | unmapped |
| g95 | **-3.33** [-4.14, -2.78] | 3.25 | 4.429 | unmapped |
| p1 | **-2.70** [-3.19, -2.29] | 0.04837 | 0.1056 | unmapped |
| g90 | **-2.58** [-3.30, -2.08] | 3.029 | 3.999 | unmapped |
| p5 | **-2.32** [-2.71, -1.89] | 0.0958 | 0.1809 | unmapped |
| p95 | **-2.15** [-2.48, -1.92] | 0.8152 | 0.8443 | unmapped |
| nps5 | **-1.94** [-2.55, -1.59] | 0.003763 | 0.0103 | sigma_r (receptor blur) + photon statistics |
| g75 | **-1.94** [-2.56, -1.43] | 2.605 | 3.376 | unmapped |
| p99 | **-1.85** [-2.25, -1.60] | 0.8914 | 0.9227 | unmapped |
| edge_sigma | **+1.84** [1.30, 2.62] | 3.576 | 1.55 | sigma_r (receptor blur) |
| g50 | **-1.73** [-2.32, -1.29] | 1.966 | 2.706 | unmapped |
| nps6 | **-1.72** [-2.34, -1.36] | 0.002141 | 0.006279 | sigma_r (receptor blur) + photon statistics |
| nps4 | **-1.45** [-2.04, -0.90] | 0.01055 | 0.01776 | sigma_r (receptor blur) + photon statistics |

**Not in the model at all, and large here:** `field_frac` (collimation / field shape)

## surgio_b51_dr: styled `styled surgio_b51_dr on surgio_b51_dr poses` (370 frames) vs real `C-ArmLSpine` (296 frames)

| statistic | d [95 % CI] | styled mean | real mean | owned by |
|---|---|---|---|---|
| nps1 | **+4.47** [3.30, 6.07] | 0.4526 | 0.2533 | sigma_r (receptor blur) + photon statistics |
| nps4 | **-3.42** [-3.73, -3.16] | 0.002313 | 0.03559 | sigma_r (receptor blur) + photon statistics |
| nps5 | **-3.25** [-3.56, -2.97] | 0.001006 | 0.02304 | sigma_r (receptor blur) + photon statistics |
| nps6 | **-3.08** [-3.39, -2.78] | 0.0005615 | 0.01489 | sigma_r (receptor blur) + photon statistics |
| nps3 | **-3.00** [-3.33, -2.75] | 0.01186 | 0.05481 | sigma_r (receptor blur) + photon statistics |
| nps7 | **-2.91** [-3.21, -2.63] | 0.0003575 | 0.009672 | sigma_r (receptor blur) + photon statistics |
| nps8 | **-2.72** [-3.02, -2.45] | 0.0002483 | 0.006333 | unmapped |
| nps9 | **-2.50** [-2.78, -2.23] | 0.0001913 | 0.004104 | unmapped |
| nps10 | **-2.26** [-2.52, -2.02] | 0.0001542 | 0.002633 | unmapped |
| penumbra_px | **-2.03** [-2.40, -1.65] | 1.352 | 3.587 | NO TERM: focal-spot size / geometric magnification |
| nps11 | **-2.02** [-2.27, -1.81] | 0.0001297 | 0.001697 | unmapped |
| p5 | **+1.99** [1.83, 2.20] | 0.1815 | 0.1311 | unmapped |
| overshoot | **+1.93** [1.56, 2.35] | 0.4732 | 0.03642 | alpha |
| p1 | **+1.82** [1.72, 1.97] | 0.1076 | 0.05986 | unmapped |

**Not in the model at all, and large here:** `penumbra_px` (focal-spot size / geometric magnification)

## elekta_xvi: styled `styled elekta_xvi on elekta_xvi poses` (272 frames) vs real `COBRA Elekta` (499 frames)

| statistic | d [95 % CI] | styled mean | real mean | owned by |
|---|---|---|---|---|
| p1 | **-4.48** [-5.50, -3.80] | 0.03838 | 0.1057 | unmapped |
| undershoot | **-3.56** [-4.91, -2.61] | -0.09895 | -0.01203 | alpha |
| edge_sigma | **+3.21** [2.90, 3.61] | 5.254 | 2.185 | sigma_r (receptor blur) |
| p50 | **-2.34** [-2.65, -2.08] | 0.2417 | 0.4806 | unmapped |
| p5 | **-2.12** [-2.53, -1.81] | 0.04746 | 0.1239 | unmapped |
| p75 | **-2.04** [-2.27, -1.86] | 0.508 | 0.7159 | unmapped |
| p25 | **-1.71** [-1.91, -1.52] | 0.1047 | 0.2862 | unmapped |
| nps0 | **-1.50** [-1.74, -1.26] | 0.279 | 0.5739 | sigma_r (receptor blur) + photon statistics |
| g50 | **-1.44** [-1.65, -1.25] | -2.102 | 1.474 | unmapped |
| p95 | **-1.22** [-1.45, -1.07] | 0.7287 | 0.8191 | unmapped |
| border_halo | **+1.15** [0.94, 1.39] | 0.07312 | -0.02051 | NO TERM: collimator scatter at the field edge |
| overshoot | **+1.12** [0.75, 1.67] | 0.1031 | 0.06041 | alpha |
| nps13 | **-1.01** [-1.14, -0.89] | 0.001485 | 0.005311 | unmapped |
| nps14 | **-1.00** [-1.14, -0.88] | 0.001393 | 0.004784 | unmapped |

**Not in the model at all, and large here:** `border_halo` (collimator scatter at the field edge)

