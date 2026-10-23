"""RNA-side manuscript panels for the U251N LITT draft (MBR/nature_draft; untracked, never committed).

Reads only the frozen copies in ./data (sha256 in data/INPUT_SHA256.txt), which are byte copies of the
grid outputs under /rs/rs_grp_oschome/go2432/u251_science/. Draws, computes nothing new except plotting
positions. Style: sans-serif, grid on both axes, one point per animal. Run: python make_figures_rna.py
"""
import csv
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "data")

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.titlesize": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.grid": True,
    "axes.grid.axis": "both",
    "grid.color": "#DDDDDD",
    "grid.linewidth": 0.5,
    "axes.axisbelow": True,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "pdf.fonttype": 42,
    "savefig.dpi": 300,
})

# arm colours match the grid-drawn DNA panels (06_integrate.R)
PRIM = "#2B78D8"
REC = "#EC6A35"
CONTRA = "#1AAE7A"
CULT = "#4D4D4D"
FLOOR = "#9E9E9E"
# compartment colours (never reused for arms)
C_TUM = "#6A3D9A"
C_BOTH = "#BDBDBD"
C_HOST = "#D9B26F"
C_AMB = "#F4F4F4"
C_COMP = "#7F7F7F"

PRIMARIES = ["IL67B", "IL68B", "IL69B"]
RECURRENCES = ["IL66B", "NL70B", "NL71B"]
TUMOURS = PRIMARIES + RECURRENCES


def arm_colour(lib):
    if lib in PRIMARIES:
        return PRIM
    if lib in RECURRENCES:
        return REC
    if lib == "N269B":
        return CONTRA
    if lib == "C2B":
        return CULT
    return FLOOR


def read_tsv(name):
    with open(os.path.join(D, name), newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    header, body = rows[0], rows[1:]
    return header, body


def save(fig, stem):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(HERE, f"{stem}.{ext}"), bbox_inches="tight")
    plt.close(fig)
    print("wrote", stem)


# ---------------------------------------------------------------- Fig 1a: read composition per library
def fig1a():
    h, body = read_tsv("xengsort_classes.tsv")
    idx = {k: i for i, k in enumerate(h)}
    rows = {r[0]: r for r in body}
    order = ["C2B"] + PRIMARIES + RECURRENCES + ["N269B", "N168B", "IL64B"]
    labels = {
        "C2B": "C2B culture", "N269B": "N269B contra (rat 69)", "N168B": "N168B contra (rat 68)",
        "IL64B": "IL64B no tumour",
    }
    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    y = np.arange(len(order))[::-1]
    for yi, lib in zip(y, order):
        r = rows[lib]
        tot = float(r[idx["total"]])
        parts = [
            (float(r[idx["graft"]]) / tot, C_TUM, "human only (graft)"),
            (float(r[idx["both"]]) / tot, C_BOTH, "both"),
            (float(r[idx["host"]]) / tot, C_HOST, "rat only (host)"),
            ((float(r[idx["ambiguous"]]) + float(r[idx["neither"]])) / tot, C_AMB, "ambiguous + neither"),
        ]
        left = 0.0
        for val, col, _ in parts:
            ax.barh(yi, val, left=left, color=col, edgecolor="#555555", linewidth=0.3, height=0.72)
            left += val
    ax.set_yticks(y)
    ax.set_yticklabels([labels.get(l, l) for l in order])
    for t, lib in zip(ax.get_yticklabels(), order):
        t.set_color(arm_colour(lib) if lib != "IL64B" and lib != "N168B" else "#555555")
    ax.set_xlim(0, 1)
    ax.set_xlabel("Share of read pairs (xengsort)")
    handles = [plt.Rectangle((0, 0), 1, 1, fc=c, ec="#555555", lw=0.3) for c in (C_TUM, C_BOTH, C_HOST, C_AMB)]
    ax.legend(handles, ["human only", "both", "rat only", "ambiguous + neither"], ncol=2, loc="upper center",
              bbox_to_anchor=(0.45, 1.2), frameon=False)
    save(fig, "fig1a_read_composition")


# ---------------------------------------------------------------- Fig 1d: lesion accounting
def fig1d():
    h, body = read_tsv("m4_lesion_accounting.tsv")
    idx = {k: i for i, k in enumerate(h)}
    rows = {r[0]: r for r in body}
    order = PRIMARIES + RECURRENCES + ["N269B", "N168B", "IL64B"]
    host_types = [("host_mic", "microglia/myeloid", "#8C510A"), ("host_ast", "astrocyte", "#DFC27D"),
                  ("host_neu", "neuron", "#80CDC1"), ("host_oli", "oligodendrocyte", "#35978F"),
                  ("host_opc", "OPC", "#C7EAE5"), ("host_end", "endothelial", "#F6E8C3")]
    fig, ax = plt.subplots(figsize=(3.9, 2.7))
    x = np.arange(len(order))
    for xi, lib in zip(x, order):
        r = rows[lib]
        bottom = 0.0
        for key, col in (("graft", C_TUM), ("both", C_BOTH)):
            v = float(r[idx[key]])
            ax.bar(xi, v, bottom=bottom, color=col, edgecolor="#555555", linewidth=0.3, width=0.75)
            bottom += v
        for key, _, col in host_types:
            v = float(r[idx[key]])
            ax.bar(xi, v, bottom=bottom, color=col, edgecolor="#555555", linewidth=0.3, width=0.75)
            bottom += v
        v = float(r[idx["ambiguous_neither"]])
        ax.bar(xi, v, bottom=bottom, color=C_AMB, edgecolor="#555555", linewidth=0.3, width=0.75)
    ax.set_xticks(x)
    ax.set_xticklabels(order, rotation=45, ha="right")
    for t, lib in zip(ax.get_xticklabels(), order):
        t.set_color(arm_colour(lib))
    ax.set_ylim(0, 1)
    ax.set_ylabel("Share of library read pairs")
    handles = [plt.Rectangle((0, 0), 1, 1, fc=c, ec="#555555", lw=0.3)
               for c in [C_TUM, C_BOTH] + [t[2] for t in host_types] + [C_AMB]]
    names = ["human only", "both"] + [f"rat: {t[1]}" for t in host_types] + ["ambiguous + neither"]
    ax.legend(handles, names, loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    save(fig, "fig1d_lesion_accounting")


# ---------------------------------------------------------------- Fig 2a: Shapley terms of species-blind DE genes
def fig2a():
    h, body = read_tsv("ha2_true_split_DE_padj05_decomposition.tsv")
    idx = {k: i for i, k in enumerate(h)}
    recs = sorted(body, key=lambda r: float(r[idx["LFC"]]))
    lfc = np.array([float(r[idx["LFC"]]) for r in recs])
    terms = {k: np.array([float(r[idx[k]]) for r in recs]) for k in ("phi_f", "phi_T", "phi_H")}
    x = np.arange(len(recs))
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    pos_bottom = np.zeros(len(recs))
    neg_bottom = np.zeros(len(recs))
    for key, col, lab in (("phi_f", C_COMP, "composition"), ("phi_T", C_TUM, "tumour cells changed"),
                          ("phi_H", C_HOST, "host cells changed")):
        v = terms[key]
        b = np.where(v >= 0, pos_bottom, neg_bottom)
        ax.bar(x, v, bottom=b, color=col, width=0.9, linewidth=0, label=lab)
        pos_bottom += np.where(v >= 0, v, 0)
        neg_bottom += np.where(v < 0, v, 0)
    ax.scatter(x, lfc, s=3, color="black", zorder=3, label="log2 fold change (sum)")
    ax.axhline(0, color="black", lw=0.5)
    ax.set_xlim(-1, len(recs))
    ax.set_xlabel(f"Species-blind DE genes, recurrent v primary (n = {len(recs)}), ordered by fold change")
    ax.set_ylabel("Exact Shapley term (log2)")
    ax.legend(loc="upper left", frameon=False, ncol=2)
    save(fig, "fig2a_shapley_de_genes")


# ---------------------------------------------------------------- Fig 2b: C-share and DE count over the ten splits
def fig2b():
    h, body = read_tsv("c3_splits_summary.tsv")
    idx = {k: i for i, k in enumerate(h)}
    df = np.array([float(r[idx["abs_diff_f_RNA"]]) for r in body])
    cs = np.array([float(r[idx["C_share"]]) for r in body])
    nde = np.array([float(r[idx["n_DE_padj05"]]) for r in body])
    true = np.array([r[idx["true_split"]] == "True" for r in body])
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.2))
    for ax, yv, lab in ((axes[0], cs, "C-share (composition share of |LFC|)"),
                        (axes[1], nde, "DE genes, padj < 0.05")):
        ax.scatter(df[~true], yv[~true], s=18, facecolor="white", edgecolor="#333333", lw=0.8,
                   label="other nine splits")
        ax.scatter(df[true], yv[true], s=30, color=REC, edgecolor="black", lw=0.6, zorder=3,
                   label="true split")
        ax.set_xlabel("|between-group difference in RNA share|")
        ax.set_ylabel(lab)
    axes[0].axhline(0.5, color="black", ls="--", lw=0.7)
    axes[0].text(0.012, 0.51, "H-A1 threshold 0.50", fontsize=6, va="bottom")
    axes[0].set_ylim(0, 0.6)
    axes[0].legend(frameon=False, loc="lower right")
    fig.tight_layout()
    save(fig, "fig2b_splits")


# ---------------------------------------------------------------- Fig 2c: named categories by view
def fig2c():
    h, body = read_tsv("c4_categories_by_view.tsv")
    idx = {k: i for i, k in enumerate(h)}
    views = ["species_blind_DE", "composition_only", "human_stream", "host_stream"]
    vlab = ["species-blind DE", "composition-only", "human stream", "host stream"]
    terms = ["cell cycle", "cell motility", "inflammatory response"]
    mat = np.zeros((len(views), len(terms)))
    qsize = {}
    for r in body:
        v, t = r[idx["view"]], r[idx["name"]]
        p = float(r[idx["p_holm_12"]])
        mat[views.index(v), terms.index(t)] = -np.log10(max(p, 1e-300))
        qsize[v] = int(r[idx["query_size"]])
    fig, ax = plt.subplots(figsize=(3.4, 2.1))
    im = ax.imshow(mat, cmap="Purples", vmin=0, vmax=12, aspect="auto")
    ax.grid(False)
    ax.set_xticks(range(len(terms)))
    ax.set_xticklabels(terms, rotation=20, ha="right")
    ax.set_yticks(range(len(views)))
    ax.set_yticklabels([f"{l} (n = {qsize[v]})" for l, v in zip(vlab, views)])
    for i in range(len(views)):
        for j in range(len(terms)):
            val = mat[i, j]
            txt = "empty" if qsize[views[i]] == 0 else f"{abs(val):.1f}"
            ax.text(j, i, txt, ha="center", va="center", fontsize=6.5,
                    color="white" if val > 6 else "black")
    cb = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03)
    cb.set_label("-log10 Holm p (12 tests)")
    save(fig, "fig2c_categories_by_view")


# ---------------------------------------------------------------- Fig 2d: MES with and without host reads
def fig2d():
    with open(os.path.join(D, "c5_l2_t1r.json")) as fh:
        c5 = json.load(fh)["C5"]
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.3), sharey=True)
    for ax, key, title in ((axes[0], "neftel_MES", "Neftel MES"), (axes[1], "wang2017_MES", "Wang 2017 MES")):
        hu, vb = c5[key]["per_tumour_human"], c5[key]["per_tumour_virtual"]
        for xi, lib in enumerate(TUMOURS):
            col = arm_colour(lib)
            ax.annotate("", xy=(xi, vb[lib]), xytext=(xi, hu[lib]),
                        arrowprops=dict(arrowstyle="->", color=col, lw=1.0))
            ax.scatter([xi], [hu[lib]], s=16, color=col, zorder=3)
        ax.set_xticks(range(len(TUMOURS)))
        ax.set_xticklabels(TUMOURS, rotation=45, ha="right")
        for t, lib in zip(ax.get_xticklabels(), TUMOURS):
            t.set_color(arm_colour(lib))
        ax.set_title(title)
        ax.axhline(0, color="black", lw=0.5)
    axes[0].set_ylabel("GSVA score (dot: human reads;\narrow head: virtual bulk)")
    fig.tight_layout()
    save(fig, "fig2d_mes_human_vs_virtual")


# ---------------------------------------------------------------- Fig 5a: DiG, per tumour and over 20 labellings
def fig5a():
    with open(os.path.join(D, "t1_e1.json")) as fh:
        t1 = json.load(fh)["T1"]["DiG"]
    h, body = read_tsv("composition_samples_main.tsv")
    idx = {k: i for i, k in enumerate(h)}
    f = {r[0]: float(r[idx["f_RNA_graft_total_floorcorr_IL64B"]]) for r in body}
    per = t1["unadjusted"]["per_animal"]
    coefs = np.array(t1["all_coefs"])
    obs = t1["arm_coef_adjusted_for_f"]
    fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.2))
    ax = axes[0]
    for lib in TUMOURS:
        ax.scatter(f[lib], per[lib], s=22, color=arm_colour(lib), edgecolor="black", lw=0.4, zorder=3)
        ax.annotate(lib, (f[lib], per[lib]), xytext=(3, 2), textcoords="offset points", fontsize=6)
    ax.set_xlabel("RNA tumour share (floor-corrected)")
    ax.set_ylabel("DiG contrast (singscore up - down)")
    ax = axes[1]
    order = np.sort(coefs)
    ax.scatter(np.arange(1, 21), order, s=12, facecolor="white", edgecolor="#333333", lw=0.7)
    k = int(np.where(np.isclose(order, obs))[0][-1]) + 1
    ax.scatter([k], [obs], s=28, color=REC, edgecolor="black", lw=0.6, zorder=3, label="true labelling")
    ax.axhline(0, color="black", lw=0.5)
    ax.set_xlabel("Labelling, ordered (20 balanced)")
    ax.set_ylabel("Arm coefficient, adjusted for share")
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    save(fig, "fig5a_dig_arms")


# ---------------------------------------------------------------- Fig 5e: DiG in every library; the H-E0 floor gate
def fig5e():
    h, body = read_tsv("dig_scores_all_libraries.tsv")
    vals = {r[0]: float(r[1]) for r in body}
    order = ["C2B"] + PRIMARIES + RECURRENCES + ["N269B", "N168B", "IL64B"]
    fig, ax = plt.subplots(figsize=(3.4, 2.3))
    for xi, lib in enumerate(order):
        ax.scatter(xi, vals[lib], s=22, color=arm_colour(lib), edgecolor="black", lw=0.4, zorder=3)
    ax.axhline(vals["N269B"], color=CONTRA, ls="--", lw=0.7)
    ax.text(len(order) - 0.6, vals["N269B"] + 0.004, "N269B", color=CONTRA, fontsize=6, ha="right")
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=45, ha="right")
    for t, lib in zip(ax.get_xticklabels(), order):
        t.set_color(arm_colour(lib))
    ax.set_ylabel("DiG contrast, human reads")
    save(fig, "fig5e_dig_floor_gate")


if __name__ == "__main__":
    fig1a()
    fig1d()
    fig2a()
    fig2b()
    fig2c()
    fig2d()
    fig5a()
    fig5e()
