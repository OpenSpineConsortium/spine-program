# Pose pools before and after `poses --arc`

Angles read back from each pose's extrinsics (`pose_arc.angles_of`), not from its recorded fields;
the worst recorded-vs-readback lat disagreement is in the table. Convention: `tools/pose_arc.py`.

| device | pool | poses | arc | \|lat\| 0-10 | \|lat\| 10-30 | \|lat\| 30-60 | \|lat\| 60-90 | \|lat\| 90-180 | tilt p5..p95 | roll p5..p95 | rec-vs-readback lat (deg) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| cios_fusion | before | 366 | 0 | 208 | 149 | 9 | 0 | 0 | -19.0..+1.5 | -178.9..+176.0 | 0.000 |
| cios_fusion | after | 1466 | 1100 | 327 | 400 | 395 | 344 | 0 | -14.0..+12.8 | -12.7..+172.0 | 0.000 |
| elekta_xvi | before | 8418 | 0 | 701 | 1411 | 2084 | 1 | 4221 | -0.0..+0.0 | -0.0..+0.0 | 0.000 |
| elekta_xvi | after | 12634 | 4216 | 1182 | 2365 | 3492 | 1374 | 4221 | -10.4..+10.3 | -7.1..+7.1 | 0.000 |
| surgio_b51_dr | before | 296 | 0 | 148 | 0 | 0 | 15 | 133 | -3.9..+3.9 | -0.5..+1.0 | 0.000 |
| surgio_b51_dr | after | 888 | 592 | 213 | 136 | 214 | 192 | 133 | -12.6..+12.8 | -8.8..+8.2 | 0.000 |
