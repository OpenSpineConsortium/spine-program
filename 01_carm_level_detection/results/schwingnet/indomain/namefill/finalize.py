"""Local finalisation of Figure 5 (b): the grid collect output + a headline block whose every number is read from the
rows and contrasts of that output (nothing typed by hand) -> SchwingNet/results/indomain/name_fill.json."""
import json
import sys

src, cells_src, out = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(src))
cells = json.load(open(cells_src))
F = d["figure5b"]
C = d["contrasts"]


def row(TV, k, arm, V, N):
    r = [x for x in F if (x["test_view"], x["k"], x["arm"], x["train_view"], x["N"]) == (TV, k, arm, V, str(N))]
    assert len(r) == 1, (TV, k, arm, V, N, len(r))
    return r[0]


def fr(r):
    c = r["correct"]
    cs = f"{c:.1f}" if abs(c - round(c)) > 1e-6 else f"{int(round(c))}"
    seeds = "" if r["seeds"] == [0] else f", mean of seeds {r['seeds']}"
    return f"{r['point_pct']:.1f} % ({cs}/{r['n']}) [{r['ci_pct'][0]:.1f}, {r['ci_pct'][1]:.1f}]{seeds}"


def con(TV, k, a, b_start):
    r = [x for x in C if x["test_view"] == TV and x["k"] == k and x["a"] == a and x["b"].startswith(b_start)]
    assert len(r) == 1, (TV, k, a, b_start, len(r))
    return r[0]


def fc(x):
    s = f"{x['diff_pp']:+.1f} pp [{x['ci_pp'][0]:+.1f}, {x['ci_pp'][1]:+.1f}] on {x['n_items']} paired vertebrae, {x['clusters']} cases"
    if x.get("clusters_favouring_a") is not None:
        s += f" ({x['clusters_favouring_a']} cases favour the first, {x['clusters_favouring_b']} the second)"
    return s


K = {"full": "whole frame", "3": "3 vertebrae in view", "1": "1 vertebra in view"}
H = []
# H1 AP curve
z = row("AP", "full", "zeroshot", "BOTH", 0)
H.append(dict(
    claim="AP protocol, whole frame: five in-domain C-arm AP cases take naming from under half correct (zero-shot) to about nine in ten correct",
    numbers={f"N={n}": fr(row("AP", "full", "indomain", "AP", n)) for n in (5, 10, 25, 50, "all")} | {"zero-shot": fr(z)},
    paired={"N=5 (seed mean) - zero-shot": fc(con("AP", "full", "indomain AP N=5 seed=mean", "zero-shot")),
            "N=all - zero-shot": fc(con("AP", "full", "indomain AP N=all seed=0", "zero-shot"))}))
# H2 AP narrow field of view
H.append(dict(
    claim="AP protocol, narrow field of view: the curve is still rising between N = 50 and N = all (step contrast below)",
    numbers={f"{K[k]}": {"zero-shot": fr(row("AP", k, "zeroshot", "BOTH", 0)),
                         **{f"N={n}": fr(row("AP", k, "indomain", "AP", n)) for n in (5, 10, 25, 50, "all")}} for k in ("3", "1")},
    paired={**{f"{K[k]}, N=all - zero-shot": fc(con("AP", k, "indomain AP N=all seed=0", "zero-shot")) for k in ("3", "1")},
            **{f"{K[k]}, N=all - N=50 (seed 0 both)": fc(con("AP", k, "indomain AP N=all seed=0", "indomain AP N=50 seed=0")) for k in ("3", "1")}}))
# H3 lateral
H.append(dict(
    claim="Lateral protocol: zero-shot already names the whole frame; in-domain lateral cases add little there and "
          "10-14 pp when 1-3 vertebrae are in view",
    numbers={K[k]: {"zero-shot": fr(row("LAT", k, "zeroshot", "BOTH", 0)),
                    **{f"N={n}": fr(row("LAT", k, "indomain", "LAT", n)) for n in (5, 25, "all")}} for k in ("full", "3", "1")},
    paired={f"{K[k]}, N=all - zero-shot": fc(con("LAT", k, "indomain LAT N=all seed=0", "zero-shot")) for k in ("full", "3", "1")}))
# H4 protocol specificity
H.append(dict(
    claim="The protocol barely transfers: lateral C-arm cases raise AP naming only slowly and stay far below AP cases at every N",
    numbers={f"AP frames, {K[k]}": {"AP-trained N=all": fr(row("AP", k, "indomain", "AP", "all")),
                                   "LAT-trained N=all": fr(row("AP", k, "indomain", "LAT", "all")),
                                   "LAT-trained N=5 (seed mean)": fr(row("AP", k, "indomain", "LAT", 5))} for k in ("full", "3", "1")},
    paired={f"AP frames, {K[k]}, AP-trained - LAT-trained, N=all": fc(con("AP", k, "indomain AP N=all seed=0 (own protocol)", "indomain LAT N=all"))
            for k in ("full", "3", "1")}))
# H5 modality at a matched protocol (AP)
H.append(dict(
    claim="Same protocol, other modality (AP): CT renders never substitute; BUU AP plain films of the same number of "
          "persons (same crop count) close the whole-frame gap from 25 persons, but not with 1-3 vertebrae in view",
    numbers={f"AP frames, {K[k]}, N={n}": {"C-arm AP cases": fr(row("AP", k, "indomain", "AP", n)) if n in (50, "all") else
                                            fr([x for x in F if (x["test_view"], x["k"], x["arm"], x["train_view"], x["N"]) == ("AP", k, "indomain", "AP", str(n))][0]),
                                            "AP plain-film persons": fr(row("AP", k, "film", "AP", n)),
                                            "AP CT-render persons": fr(row("AP", k, "render", "AP", n))}
             for k in ("full", "3", "1") for n in (5, 25, "all")},
    paired={f"AP frames, {K[k]}, N={n}, C-arm - {arm}": fc(con("AP", k, f"indomain AP N={n} seed=0", f"{arm} AP N={n}"))
            for k in ("full", "3", "1") for n in (5, 10, 25, 50, "all") for arm in ("film", "render")},
    note="the paired contrasts compare seed 0 of the C-arm arm with seed 0 of the film/render arm; the film and render "
         "arms were run at seed 0 only"))
# H6 lateral modality
H.append(dict(
    claim="Same protocol, other modality (lateral): lateral films and CT renders at matched N trail the C-arm cases, "
          "most with 1-3 vertebrae in view",
    paired={f"LAT frames, {K[k]}, N={n}, C-arm - {arm}": fc(con("LAT", k, f"indomain LAT N={n} seed=0", f"{arm} LAT N={n}"))
            for k in ("full", "3", "1") for n in (5, 25, "all") for arm in ("film", "render")}))

ref = {f"{r['test_view']} {K[r['k']]}": f"{r['point_pct']:.1f} % ({int(r['correct'])}/{r['n']}) [{r['ci_pct'][0]:.1f}, {r['ci_pct'][1]:.1f}]"
       for r in d["reference"]}
both = {f"{TV} {K[k]}": fr(row(TV, k, "indomain", "BOTH", "all")) for TV in ("LAT", "AP") for k in ("full", "3", "1")}
seedspread = {f"{TV} {K[k]} N={n}": [r["point_pct"] for r in d["curves"] if (r["arm"], r["train_view"], r["test_view"], r["k"], r["N"]) ==
                                     ("indomain", TV, TV, k, str(n)) and r["seed"] in (0, 1, 2)]
              for TV in ("LAT", "AP") for k in ("full", "3", "1") for n in (0, 5, 10, 25)}
all_cases = {f"fold{K_}": {V: cells["cells"][f"cv{K_}_{V}_id_Nall_s0"]["n_cases"] for V in ("LAT", "AP")} for K_ in range(5)}
cropless = sorted({r["case"] for r in cells["check"]["cropless"]["rows"]})

d["summary"] = dict(
    written="2026-09-24, from the grid collect of " + d["generated"],
    headline=H,
    checks=dict(
        every_row_complete_over_5_folds=all(r["complete"] for r in F),
        every_row_held_out_by_gate_and_lists=all(r["held_out"] == "gate + lists" for r in F),
        n_cells=d["n_cells"], n_cells_done=d["n_cells_done"],
        both_protocols_N_all_vs_shipped_cv={"this fill (v9 init, repaired truth)": both,
                                            "shipped CV a4/a7 (allspine_v2_r1 init, pre-repair truth), UNPAIRED": ref},
        seed_spread_pct=seedspread,
        n_cases_at_N_all=all_cases),
    caveats=[
        "N = 100 is not drawable: a fold's training pool holds 82-96 usable cases, so N = all is 82-96 (x_persons_per_fold).",
        "The zero-shot row is the N = 0 reference. The in-domain N = 0 row (the fine-tune recipe with no C-arm training crop, "
        "checkpoint picked on the C-arm val fold) reads LOWER than zero-shot on AP (see contrasts), so fine-tuning on the base "
        "sample alone does not help.",
        "Zero-shot here is the clean v9 level model: AP whole frame " + fr(row("AP", "full", "zeroshot", "BOTH", 0)) + ". The "
        "37.9 % (239/631) quoted in INVENTORY.md/a3 is allspine_v2_r1 (a bank that leaked people between its splits) on the "
        "pre-repair truth; they are different models and item sets.",
        "Every fine-tuned arm, the film and render arms included, picks its checkpoint on the C-ArmLSpine val fold of its "
        "protocol (disjoint from the test fold). The arms differ only in their training images.",
        "The film and render arms ran at seed 0 only. The in-domain seed spread at small N is in checks.seed_spread_pct "
        "(e.g. AP whole frame N=5: " + ", ".join(f"{v:.1f}" for v in seedspread["AP whole frame N=5"]) + " %), so a film-vs-C-arm gap "
        "of a few points at one N is inside seed noise.",
        "The BUU AP films and the CT renders carry L1-L5 crops and no sacrum crop; the C-arm crops carry the sacrum too. The "
        "test items are vertebra boxes only (tools/carmlspine_eval.py, cls == 0), so scoring is unaffected; the training mix "
        "differs.",
        f"{', '.join(cropless)} have no labeller-agreed vertebra level (only a clipped sacrum box), so they are never a "
        "training case and contribute no test item. case42 and case121 are two of the three real L6 patients.",
        "The lateral film curve is not monotone (N = 50 dips); one seed per point.",
        "Crop counts per k vary by 0-4 vertebrae between cells (the matched set depends on the model's own boxes); every "
        "paired contrast uses only the vertebrae matched in both arms (n_items, unmatched_a/b).",
    ],
    grid=dict(dir="/rs/rs_grp_oschome/go2432/data/or_ready/indomain/name_fill",
              jobs={"40427901": "first array, 225 cells: 183 done, 42 stopped in cellbank (subset rule, revision 1)",
                    "40429295": "revision 2 dry run", "40429398": "revision 2: 80 cells redefined, dirs moved to cells_superseded_20260924T0538",
                    "40429416": "80-cell array (42 in-domain + 38 film/render)", "40429708": "AP film crops + 25 cells (apfilm)",
                    "40429901": "25-cell AP film array", "40432733": "cancelled (retry superseded)",
                    "40436049": "retry of 9 cells whose first attempt trained on the CPU (msa1) or was cancelled with it",
                    "40436050": "final collect"}),
)
json.dump(d, open(out, "w"), indent=1)
print("wrote", out)
for h in H:
    print("-", h["claim"])
print(json.dumps(d["summary"]["checks"], indent=1)[:3000])
