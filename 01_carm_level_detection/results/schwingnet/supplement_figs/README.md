# Inputs of the supplementary figures that live on the grid

Copied 2026-09-23 so `SchwingNet/tools/figS_supplement.py` reads nothing outside the repository.

| here | grid original |
|---|---|
| `card_refit/full/<device>.refit.json` | `/rs/rs_grp_oschome/go2432/data/or_ready/devices_refit/<device>.refit.json` (array 40418162; Cios 16:17, Elekta 17:13, Surgio 18:16) |
| `card_refit/constrained/<device>.refit.json` | `/rs/rs_grp_oschome/go2432/data/or_ready/devices_refit_constrained/<device>.refit.json` (job 40424648; Cios not run: out of memory at 48 GB) |
| `case134/frames.csv` | one row per frame of `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep/meta/*.json`: `lat_signed_deg`, `tilt_signed_deg`, `angle`, `pose.edge_ncc`, `n_kept`, `pose.from_header.*` (no other field) |
| `case134/summary.json` | `/rs/rs_grp_oschome/go2432/data/realxray/carmlspine_sweep/summary.json` |
| `case134/frames/case134_sw{054,129,205,280}.{png,json}` | `.../carmlspine_sweep/images/test/` and `.../meta/`: the frames nearest lat_signed -90, -45, 0 and +45 degrees |

The case134 export carries no patient identifier (identifier scan: 0 hits; results/arc/ARC_CHECK.md item 5).
