#!/usr/bin/env python3
"""
cami_simulate_and_predict_fixed.py
==============================================================================
FIXED VERSION — two key fixes over the original:

  FIX 1 — ROC curves now saved correctly:
      model.predict_proba(X) is called to get per-class probability scores.
      One-vs-rest ROC is computed and plotted for each of the 10 species.
      cami_roc_curves.png and cami_y_prob.npy are saved to OUTPUT_DIR.

  FIX 2 — Per-species accuracy bar chart uses distinct subtle colours:
      Each of the 10 species gets its own muted colour (no red/green logic).
      A reference dashed line shows overall accuracy.

  FIX 3 — All plots scoped to 10 simulated species only (not all 306).

OUTPUT FILES:
    cami_confusion_matrix.png
    cami_per_species_accuracy.png     <- distinct colour per species
    cami_per_species_precision.png
    cami_per_species_recall.png
    cami_precision_recall_f1.png
    cami_roc_curves.png               <- NEW: saved from predict_proba
    cami_abundance_vs_accuracy.png
    cami_metrics.json
    cami_y_true.npy
    cami_y_pred.npy
    cami_y_prob.npy                   <- NEW: saved probability scores
    cami_confusion_matrix.npy

USAGE:
    python cami_simulate_and_predict_fixed.py

REQUIREMENTS:
    pip install xgboost scikit-learn numpy scipy biopython matplotlib seaborn
==============================================================================
"""

import os
import sys
import json
import time
import random
import numpy as np
import scipy.sparse as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from itertools import product
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report,
    roc_curve, auc
)
from sklearn.preprocessing import label_binarize
import xgboost as xgb

# ══════════════════════════════════════════════════════════════════════════════
# PATHS
# ══════════════════════════════════════════════════════════════════════════════
FASTA_BASE_DIR = "/lustre/scratch/gylab204/taiba/project/train"
MODEL_PATH     = "/lustre/scratch/gylab204/taiba/project/kmers/ml/xgboost_model_cpu.json"
LABEL_MAP_PATH = "/lustre/scratch/gylab204/taiba/project/kmers/ml/label_map.json"
OUTPUT_DIR     = "/lustre/scratch/gylab204/taiba/project/kmers/ml/cami_results"

# ══════════════════════════════════════════════════════════════════════════════
# SIMULATION PARAMETERS
# ══════════════════════════════════════════════════════════════════════════════
FRAGMENT_LEN = 150
K            = 6
RANDOM_SEED  = 42
VALID_BASES  = set("ACGT")

ABUNDANCE_PROFILE = {
    "Ehrlichia_ruminantium"              : 2000,
    "Methanobrevibacter_smithii"         : 8000,
    "Campylobacter_curvus"               : 4000,
    "Candidatus_Nitrosotenuis_uzonensis" : 1500,
    "Riemerella_anatipestifer"           : 3000,
    "Listeria_innocua"                   : 6000,
    "Clostridium_perfringens"            : 7000,
    "Methylibium_petroleiphilum"         : 2500,
    "Chromobacterium_violaceum"          : 5000,
    "Xenorhabdus_nematophila"            : 4000,
}

# ── Subtle, distinct colours for 10 species (muted palette) ──────────────────
SPECIES_COLOURS = [
    "#5B8DB8",   # muted blue         — Ehrlichia ruminantium
    "#7BAF7B",   # sage green         — Methanobrevibacter smithii
    "#C97B5A",   # terracotta         — Campylobacter curvus
    "#9B7BB8",   # dusty purple       — Ca. Nitrosotenuis uzonensis
    "#C9A84C",   # warm gold          — Riemerella anatipestifer
    "#5AABAB",   # teal               — Listeria innocua
    "#C96B6B",   # muted rose         — Clostridium perfringens
    "#7B9BB8",   # steel blue         — Methylibium petroleiphilum
    "#8FAF6B",   # olive green        — Chromobacterium violaceum
    "#B8856B",   # sandy brown        — Xenorhabdus nematophila
]

# ══════════════════════════════════════════════════════════════════════════════
# K-MER INDEX
# ══════════════════════════════════════════════════════════════════════════════
def reverse_complement(seq):
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def canonical(kmer):
    return min(kmer, reverse_complement(kmer))

def build_kmer_index():
    kmers = [''.join(p) for p in product("ACGT", repeat=K)]
    canonical_set = sorted(set(canonical(k) for k in kmers))
    return {k: i for i, k in enumerate(canonical_set)}

KMER_INDEX = build_kmer_index()
N_FEATURES = len(KMER_INDEX)
print(f"K-mer index built: {N_FEATURES} canonical {K}-mers")

# ══════════════════════════════════════════════════════════════════════════════
# FASTA READER
# ══════════════════════════════════════════════════════════════════════════════
def read_fasta(path):
    seqs, current = [], []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current:
                    seqs.append("".join(current))
                current = []
            else:
                current.append(line.upper())
    if current:
        seqs.append("".join(current))
    return seqs

def load_species_genome(species_name):
    species_dir = os.path.join(FASTA_BASE_DIR, species_name)
    if not os.path.isdir(species_dir):
        raise FileNotFoundError(f"Directory not found: {species_dir}")
    all_seq = []
    fna_files = [f for f in os.listdir(species_dir) if f.endswith(".fna")]
    if not fna_files:
        raise FileNotFoundError(f"No .fna files in: {species_dir}")
    for fname in fna_files:
        for s in read_fasta(os.path.join(species_dir, fname)):
            clean = ''.join(c for c in s if c in VALID_BASES)
            if len(clean) >= FRAGMENT_LEN:
                all_seq.append(clean)
    return all_seq

# ══════════════════════════════════════════════════════════════════════════════
# FRAGMENT SAMPLER
# ══════════════════════════════════════════════════════════════════════════════
def sample_fragments(sequences, n_fragments, frag_len, rng):
    total_bp = sum(len(s) for s in sequences)
    if total_bp < frag_len:
        raise ValueError(f"Genome too small ({total_bp}bp) for {frag_len}bp fragments")
    fragments, attempts = [], 0
    max_tries = n_fragments * 20
    while len(fragments) < n_fragments and attempts < max_tries:
        attempts += 1
        seq = rng.choices(sequences, weights=[len(s) for s in sequences], k=1)[0]
        if len(seq) < frag_len:
            continue
        start = rng.randint(0, len(seq) - frag_len)
        frag  = seq[start : start + frag_len]
        if sum(1 for c in frag if c in VALID_BASES) / frag_len >= 0.95:
            fragments.append(frag)
    if len(fragments) < n_fragments:
        print(f"  WARNING: Only got {len(fragments)}/{n_fragments} valid fragments")
    return fragments

# ══════════════════════════════════════════════════════════════════════════════
# K-MER ENCODER
# ══════════════════════════════════════════════════════════════════════════════
def encode_fragment(seq):
    counts, total = {}, 0
    for i in range(len(seq) - K + 1):
        kmer = seq[i : i + K]
        if not all(b in VALID_BASES for b in kmer):
            continue
        idx = KMER_INDEX[canonical(kmer)]
        counts[idx] = counts.get(idx, 0) + 1
        total += 1
    if total > 0:
        for k in counts:
            counts[k] /= total
    return counts

def encode_fragments_batch(fragments):
    rows, cols, vals = [], [], []
    for i, frag in enumerate(fragments):
        for col, val in encode_fragment(frag).items():
            rows.append(i)
            cols.append(col)
            vals.append(val)
    return sp.csr_matrix(
        (vals, (rows, cols)),
        shape=(len(fragments), N_FEATURES),
        dtype=np.float32,
    )

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def make_short_name(sp):
    """Campylobacter_curvus  ->  C. curvus"""
    s = sp.replace("Candidatus_", "Ca. ").replace("_", " ")
    parts = s.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}. {' '.join(parts[1:])}"
    return s

def save_bar(values_0to1, title, ylabel, short_names, ref_line_0to1,
             filename, colours):
    """
    Generic per-species bar chart.
    values_0to1  : list of floats in [0, 1]
    ref_line_0to1: float in [0, 1] — drawn as dashed reference line
    colours      : list of hex colours, one per bar
    """
    pct    = [v * 100 for v in values_0to1]
    ref    = ref_line_0to1 * 100
    fig, ax = plt.subplots(figsize=(13, 6))
    bars = ax.bar(short_names, pct, color=colours,
                  edgecolor="white", linewidth=0.8, width=0.6)
    ax.axhline(y=ref, color="#444444", linestyle="--", linewidth=1.8,
               label=f"Macro avg: {ref:.1f}%", alpha=0.75)
    ax.set_ylabel(ylabel, fontsize=13)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_ylim(0, 112)
    ax.set_yticks(range(0, 110, 10))
    ax.grid(axis="y", alpha=0.25, linestyle="--")
    ax.legend(fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bar, val in zip(bars, pct):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 1.5,
                f"{val:.1f}%",
                ha="center", va="bottom",
                fontsize=9.5, fontweight="bold",
                color="#333333")
    plt.xticks(fontsize=9, rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(filename, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {os.path.basename(filename)}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    rng = random.Random(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("\n" + "="*70)
    print("  CAMI-STYLE METAGENOME SIMULATION + PREDICTION  (FIXED)")
    print("="*70)

    # ── Load label map ────────────────────────────────────────────────────
    with open(LABEL_MAP_PATH) as f:
        label_map = json.load(f)
    num_classes = len(label_map)
    print(f"\nLoaded label map: {num_classes} total species in model")

    # Ordered lists for our 10 simulated species
    simulated_labels      = [label_map[sp] for sp in ABUNDANCE_PROFILE]
    simulated_full_names  = [
        sp.replace("Candidatus_", "Ca. ").replace("_", " ")
        for sp in ABUNDANCE_PROFILE
    ]
    simulated_short_names = [make_short_name(sp) for sp in ABUNDANCE_PROFILE]
    total_frags           = sum(ABUNDANCE_PROFILE.values())

    # ── Step 1: Simulate ──────────────────────────────────────────────────
    print("\n" + "-"*70)
    print("STEP 1: Simulating CAMI-style metagenome (10 species)")
    print("-"*70)

    all_fragments, all_labels = [], []
    t0 = time.time()
    for sp, n_frags in ABUNDANCE_PROFILE.items():
        label = label_map[sp]
        pct   = n_frags / total_frags * 100
        print(f"  {sp:<45} {n_frags:>6,} frags ({pct:.1f}%)")
        sequences = load_species_genome(sp)
        fragments = sample_fragments(sequences, n_frags, FRAGMENT_LEN, rng)
        all_fragments.extend(fragments)
        all_labels.extend([label] * len(fragments))

    sim_time = time.time() - t0
    combined = list(zip(all_fragments, all_labels))
    random.Random(RANDOM_SEED).shuffle(combined)
    all_fragments, all_labels = zip(*combined)
    all_labels = np.array(all_labels, dtype=np.int32)
    print(f"\nSimulation complete: {len(all_fragments):,} fragments in {sim_time:.1f}s")

    # ── Step 2: Encode ────────────────────────────────────────────────────
    print("\n" + "-"*70)
    print("STEP 2: Encoding fragments (canonical k=6 k-mers)")
    print("-"*70)
    t0 = time.time()
    X  = encode_fragments_batch(all_fragments)
    enc_time = time.time() - t0
    print(f"Encoded: {X.shape} matrix in {enc_time:.1f}s")

    # ── Step 3: Load model ────────────────────────────────────────────────
    print("\n" + "-"*70)
    print("STEP 3: Loading XGBoost model")
    print("-"*70)
    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    print(f"Model loaded OK  ({num_classes} classes)")

    # ── Step 4: Predict — hard labels AND probability scores ──────────────
    print("\n" + "-"*70)
    print("STEP 4: Predicting (hard labels + predict_proba for ROC)")
    print("-"*70)
    t0        = time.time()
    y_pred    = model.predict(X)
    y_prob    = model.predict_proba(X)   # shape: (n_samples, num_classes)
    pred_time = time.time() - t0
    print(f"Predicted {len(y_pred):,} fragments in {pred_time:.2f}s  "
          f"({len(y_pred)/pred_time:,.0f} frags/sec)")
    print(f"y_prob shape: {y_prob.shape}  — ready for ROC curves")

    # ── Step 5: Evaluate ──────────────────────────────────────────────────
    print("\n" + "-"*70)
    print("STEP 5: Evaluation")
    print("-"*70)

    y_true = all_labels

    accuracy        = accuracy_score(y_true, y_pred)
    precision_macro = precision_score(y_true, y_pred, average="macro",
                                      labels=simulated_labels, zero_division=0)
    recall_macro    = recall_score(y_true, y_pred, average="macro",
                                   labels=simulated_labels, zero_division=0)
    f1_macro        = f1_score(y_true, y_pred, average="macro",
                               labels=simulated_labels, zero_division=0)

    # Confusion matrix — 10×10 only
    cm = confusion_matrix(y_true, y_pred, labels=simulated_labels)

    # Macro specificity
    specificities = []
    total_cm = int(np.sum(cm))
    for i in range(len(simulated_labels)):
        tn = total_cm - np.sum(cm[i, :]) - np.sum(cm[:, i]) + cm[i, i]
        fp = np.sum(cm[:, i]) - cm[i, i]
        specificities.append(tn / (tn + fp) if (tn + fp) > 0 else 0.0)
    macro_spec = float(np.mean(specificities))

    # Per-species metrics
    per_prec = precision_score(y_true, y_pred, average=None,
                               labels=simulated_labels, zero_division=0)
    per_rec  = recall_score(y_true, y_pred, average=None,
                            labels=simulated_labels, zero_division=0)
    per_f1   = f1_score(y_true, y_pred, average=None,
                        labels=simulated_labels, zero_division=0)
    per_acc  = np.array([
        np.sum((y_true == lbl) & (y_pred == lbl)) / np.sum(y_true == lbl)
        for lbl in simulated_labels
    ])

    print(f"\n  Accuracy            : {accuracy:.4f}  ({accuracy*100:.2f}%)")
    print(f"  Precision (macro)   : {precision_macro:.4f}  ({precision_macro*100:.2f}%)")
    print(f"  Recall    (macro)   : {recall_macro:.4f}  ({recall_macro*100:.2f}%)")
    print(f"  Specificity (macro) : {macro_spec:.4f}  ({macro_spec*100:.2f}%)")
    print(f"  F1-score  (macro)   : {f1_macro:.4f}")

    print(f"\n  {'Species':<40} {'Acc%':>6} {'Prec%':>6} {'Rec%':>6} {'F1':>6}")
    print(f"  {'-'*40} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")
    for name, acc, prec, rec, f1 in zip(
            simulated_full_names, per_acc, per_prec, per_rec, per_f1):
        print(f"  {name:<40} {acc*100:>5.1f}% {prec*100:>5.1f}% "
              f"{rec*100:>5.1f}% {f1:>5.3f}")

    print("\n  Classification report (10 species):")
    print(classification_report(
        y_true, y_pred,
        labels=simulated_labels,
        target_names=simulated_full_names,
        zero_division=0
    ))

    # ── Step 6: Save arrays & metrics ─────────────────────────────────────
    print("\n" + "-"*70)
    print("STEP 6: Saving results")
    print("-"*70)

    results = {
        "dataset"              : "CAMI-simulated metagenome",
        "fragment_length_bp"   : FRAGMENT_LEN,
        "total_fragments"      : len(all_fragments),
        "num_species_simulated": len(ABUNDANCE_PROFILE),
        "accuracy"             : float(accuracy),
        "precision_macro"      : float(precision_macro),
        "recall_macro"         : float(recall_macro),
        "specificity_macro"    : macro_spec,
        "f1_macro"             : float(f1_macro),
        "simulation_time_sec"  : sim_time,
        "encoding_time_sec"    : enc_time,
        "prediction_time_sec"  : pred_time,
        "per_species"          : {
            name: {
                "accuracy"  : float(acc),
                "precision" : float(prec),
                "recall"    : float(rec),
                "f1"        : float(f1),
            }
            for name, acc, prec, rec, f1 in zip(
                simulated_full_names, per_acc, per_prec, per_rec, per_f1)
        }
    }
    with open(os.path.join(OUTPUT_DIR, "cami_metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    np.save(os.path.join(OUTPUT_DIR, "cami_y_true.npy"), y_true)
    np.save(os.path.join(OUTPUT_DIR, "cami_y_pred.npy"), y_pred)
    np.save(os.path.join(OUTPUT_DIR, "cami_y_prob.npy"), y_prob)   # NEW
    np.save(os.path.join(OUTPUT_DIR, "cami_confusion_matrix.npy"), cm)
    print(f"  All files saved to: {OUTPUT_DIR}/")

    # ── Step 7: Plots ─────────────────────────────────────────────────────
    print("\n" + "-"*70)
    print("STEP 7: Generating plots")
    print("-"*70)

    sn  = simulated_short_names
    col = SPECIES_COLOURS   # one subtle colour per species

    # ── Plot 1: Confusion Matrix (10×10 normalised) ───────────────────────
    cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True)
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(cm_norm, annot=True, fmt=".2f", cmap="Blues",
                xticklabels=sn, yticklabels=sn,
                ax=ax, linewidths=0.8, linecolor="white",
                annot_kws={"size": 11, "weight": "bold"},
                vmin=0, vmax=1)
    ax.set_xlabel("Predicted Species", fontsize=13, labelpad=12)
    ax.set_ylabel("True Species", fontsize=13, labelpad=12)
    ax.set_title(
        f"CAMI Confusion Matrix — 10 Simulated Species (Normalised)\n"
        f"Accuracy = {accuracy*100:.2f}%  |  Macro F1 = {f1_macro:.4f}",
        fontsize=13, fontweight="bold", pad=15)
    plt.xticks(rotation=35, ha="right", fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cami_confusion_matrix.png"),
                dpi=180, bbox_inches="tight")
    plt.close()
    print("  Saved: cami_confusion_matrix.png")

    # ── Plot 2: Per-species Accuracy — distinct colour per species ────────
    save_bar(
        per_acc,
        "CAMI: Per-Species Classification Accuracy (10 Species)",
        "Accuracy (%)", sn, accuracy,
        os.path.join(OUTPUT_DIR, "cami_per_species_accuracy.png"),
        colours=col
    )

    # ── Plot 3: Per-species Precision ─────────────────────────────────────
    save_bar(
        per_prec,
        "CAMI: Per-Species Precision (10 Species)",
        "Precision (%)", sn, precision_macro,
        os.path.join(OUTPUT_DIR, "cami_per_species_precision.png"),
        colours=col
    )

    # ── Plot 4: Per-species Recall ────────────────────────────────────────
    save_bar(
        per_rec,
        "CAMI: Per-Species Recall (10 Species)",
        "Recall (%)", sn, recall_macro,
        os.path.join(OUTPUT_DIR, "cami_per_species_recall.png"),
        colours=col
    )

    # ── Plot 5: Grouped Precision / Recall / F1 ───────────────────────────
    x     = np.arange(len(sn))
    width = 0.25
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(x - width, per_prec * 100, width, label="Precision",
           color="#5B8DB8", edgecolor="white", linewidth=0.6)
    ax.bar(x,          per_rec  * 100, width, label="Recall",
           color="#9B7BB8", edgecolor="white", linewidth=0.6)
    ax.bar(x + width,  per_f1   * 100, width, label="F1-score",
           color="#7BAF7B", edgecolor="white", linewidth=0.6)
    ax.set_xticks(x)
    ax.set_xticklabels(sn, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("Score (%)", fontsize=13)
    ax.set_ylim(0, 112)
    ax.set_yticks(range(0, 110, 10))
    ax.set_title("CAMI: Precision, Recall & F1-score per Species (10 Species)",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.25, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cami_precision_recall_f1.png"),
                dpi=180, bbox_inches="tight")
    plt.close()
    print("  Saved: cami_precision_recall_f1.png")

    # ── Plot 6: ROC Curves — one-vs-rest, saved from predict_proba ───────
    # y_prob shape: (n_samples, num_classes)
    # We index column by the numeric label from label_map for each species
    y_true_bin = label_binarize(y_true, classes=list(range(num_classes)))

    fig, ax = plt.subplots(figsize=(11, 8))
    for i, (label, name, colour) in enumerate(
            zip(simulated_labels, sn, col)):
        prob_col = y_prob[:, label]   # probability of being this species
        true_col = y_true_bin[:, label]
        fpr, tpr, _ = roc_curve(true_col, prob_col)
        roc_auc     = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=colour, linewidth=2.2,
                label=f"{name}  (AUC = {roc_auc:.3f})")

    ax.plot([0, 1], [0, 1], color="#999999", linestyle="--",
            linewidth=1.2, label="Random classifier")
    ax.set_xlabel("False Positive Rate", fontsize=13)
    ax.set_ylabel("True Positive Rate (Sensitivity)", fontsize=13)
    ax.set_title(
        "CAMI: ROC Curves — One-vs-Rest per Species\n"
        f"(10 simulated species, {len(y_true):,} fragments)",
        fontsize=14, fontweight="bold")
    ax.legend(fontsize=9, loc="lower right",
              framealpha=0.9, edgecolor="#cccccc")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.02])
    ax.grid(True, alpha=0.2, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cami_roc_curves.png"),
                dpi=180, bbox_inches="tight")
    plt.close()
    print("  Saved: cami_roc_curves.png")

    # ── Plot 7: Abundance vs Accuracy scatter ─────────────────────────────
    ab_pct = [ABUNDANCE_PROFILE[sp] / total_frags * 100
              for sp in ABUNDANCE_PROFILE]
    fig, ax = plt.subplots(figsize=(11, 7))
    for i, (name, ab, acc, colour) in enumerate(
            zip(sn, ab_pct, per_acc, col)):
        ax.scatter(ab, acc * 100, s=200, color=colour, zorder=3,
                   edgecolors="white", linewidth=1.5)
        ax.annotate(name, (ab, acc * 100),
                    textcoords="offset points", xytext=(9, 4),
                    fontsize=9, color=colour, fontweight="bold")
    ax.axhline(y=accuracy * 100, color="#888888", linestyle="--",
               linewidth=1.8,
               label=f"Overall accuracy ({accuracy*100:.1f}%)", alpha=0.8)
    ax.set_xlabel("Relative Abundance in Simulated Metagenome (%)", fontsize=12)
    ax.set_ylabel("Per-Species Classification Accuracy (%)", fontsize=12)
    ax.set_title("CAMI: Abundance vs Classification Accuracy per Species",
                 fontsize=14, fontweight="bold")
    ax.set_ylim(60, 105)
    ax.grid(True, alpha=0.2, linestyle="--")
    ax.legend(fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "cami_abundance_vs_accuracy.png"),
                dpi=180, bbox_inches="tight")
    plt.close()
    print("  Saved: cami_abundance_vs_accuracy.png")

    # ── Final summary ─────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("  CAMI SIMULATION COMPLETE")
    print("="*70)
    print(f"  Fragments simulated  : {len(all_fragments):,}")
    print(f"  Species tested       : {len(ABUNDANCE_PROFILE)}")
    print(f"  Accuracy             : {accuracy*100:.2f}%")
    print(f"  Precision (macro)    : {precision_macro*100:.2f}%")
    print(f"  Recall    (macro)    : {recall_macro*100:.2f}%")
    print(f"  Specificity (macro)  : {macro_spec*100:.2f}%")
    print(f"  F1-score  (macro)    : {f1_macro:.4f}")
    print(f"  Results saved to     : {OUTPUT_DIR}/")
    print("="*70)
    print("\n  Output files:")
    for fname in [
        "cami_confusion_matrix.png",
        "cami_per_species_accuracy.png",
        "cami_per_species_precision.png",
        "cami_per_species_recall.png",
        "cami_precision_recall_f1.png",
        "cami_roc_curves.png",
        "cami_abundance_vs_accuracy.png",
        "cami_metrics.json",
        "cami_y_true.npy",
        "cami_y_pred.npy",
        "cami_y_prob.npy",
        "cami_confusion_matrix.npy",
    ]:
        print(f"    {OUTPUT_DIR}/{fname}")
    print("\nDONE\n")


if __name__ == "__main__":
    main()
