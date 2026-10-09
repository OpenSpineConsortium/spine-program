# spinesurg-ct-nnunet — working context

**Start every session at [docs/PIPELINE_RESUME.md](docs/PIPELINE_RESUME.md), then run the state tool:**

```
ssh go2432@grid.wayne.edu
~/mambaforge/envs/spineps/bin/python ~/spinesurg-ct-nnunet/tools/pipeline_state.py
```

That tool computes what is done, running, ready and blocked from the filesystem and the scheduler. Do not trust
any status written in prose, including in this file. If you add a pipeline stage, add it to
`tools/pipeline_state.py`, or it will be lost the way the run-level head was.

**For the fluoroscopic physics and vertebra-linking work, start at
[docs/HANDOFF_PHYSICS.md](docs/HANDOFF_PHYSICS.md) and run `make physics-tables`.** It leads with the
finding that reframes that whole work stream -- detection is the binding constraint and costs about
sixty points where realistic physics costs eleven to twenty-eight -- and lists nine linking fixes that
are refuted and must not be re-tried, and seven claims that were withdrawn after being believed.
`make physics` reproduces every number in it and EXITS NON-ZERO if one has moved.

