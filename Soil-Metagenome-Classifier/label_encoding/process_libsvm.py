import json
import csv
from collections import defaultdict

# ===============================
# PATHS
# ===============================
TRAIN_INPUT  = "/lustre/scratch/gylab204/taiba/project/kmers/train.libsvm"
TEST_INPUT   = "/lustre/scratch/gylab204/taiba/project/kmers/test.libsvm"

TRAIN_OUTPUT = "/lustre/scratch/gylab204/taiba/project/kmers/ml/train_encoded.libsvm"
TEST_OUTPUT  = "/lustre/scratch/gylab204/taiba/project/kmers/ml/test_encoded.libsvm"

LABEL_MAP_FILE  = "/lustre/scratch/gylab204/taiba/project/kmers/ml/label_map.json"
KMER_STATS_FILE = "/lustre/scratch/gylab204/taiba/project/kmers/ml/kmer_stats.csv"

import os
os.makedirs(os.path.dirname(TRAIN_OUTPUT), exist_ok=True)

# ===============================
# STEP 1 — ENCODE TRAIN
# build label map from train only
# ===============================
print("=" * 50)
print("STEP 1 — Encoding train set")
print("=" * 50)

label_map     = {}
label_counter = 0

# species → kmer_idx → [total_freq, count]
kmer_stats = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))

with open(TRAIN_INPUT, "r") as fin, open(TRAIN_OUTPUT, "w") as fout:

    for i, line in enumerate(fin):

        parts = line.strip().split()
        if not parts:
            continue

        species  = parts[0]
        features = parts[1:]

        # ---------------------------
        # BUILD LABEL MAP FROM TRAIN
        # ---------------------------
        if species not in label_map:
            label_map[species] = label_counter
            label_counter += 1

        label = label_map[species]

        # ---------------------------
        # WRITE ENCODED TRAIN LIBSVM
        # ---------------------------
        fout.write(f"{label} {' '.join(features)}\n")

        # ---------------------------
        # TRACK KMER STATS
        # ---------------------------
        for feat in features:
            idx, val = feat.split(":")
            val = float(val)
            stats = kmer_stats[species][idx]
            stats[0] += val
            stats[1] += 1

        if i % 100000 == 0:
            print(f"  Train lines processed: {i:,}")

print(f"\n  Train encoding done")
print(f"  Total species found : {len(label_map)}")
print(f"✅ Saved: {TRAIN_OUTPUT}")

# ===============================
# STEP 2 — SAVE LABEL MAP
# must be saved before encoding test
# ===============================
with open(LABEL_MAP_FILE, "w") as f:
    json.dump(label_map, f, indent=2)

print(f"\n✅ Saved label map : {LABEL_MAP_FILE}")
print(f"   Species in map  : {len(label_map)}")

# ===============================
# STEP 3 — ENCODE TEST
# use the SAME label map from train
# never build a new one from test
# ===============================
print("\n" + "=" * 50)
print("STEP 3 — Encoding test set")
print("=" * 50)

skipped = 0

with open(TEST_INPUT, "r") as fin, open(TEST_OUTPUT, "w") as fout:

    for i, line in enumerate(fin):

        parts = line.strip().split()
        if not parts:
            continue

        species  = parts[0]
        features = parts[1:]

        # ---------------------------
        # USE EXISTING LABEL MAP ONLY
        # if a species appears in test
        # but not in train → skip it
        # (should not happen in your setup)
        # ---------------------------
        if species not in label_map:
            print(f"  WARNING: '{species}' not in train label map — skipping")
            skipped += 1
            continue

        label = label_map[species]

        # ---------------------------
        # WRITE ENCODED TEST LIBSVM
        # ---------------------------
        fout.write(f"{label} {' '.join(features)}\n")

        if i % 100000 == 0:
            print(f"  Test lines processed: {i:,}")

print(f"\n  Test encoding done")
print(f"  Skipped lines (unknown species): {skipped}")
print(f"✅ Saved: {TEST_OUTPUT}")

# ===============================
# STEP 4 — SAVE KMER STATS
# ===============================
with open(KMER_STATS_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["species", "kmer_idx", "total_freq", "count"])

    for species in kmer_stats:
        for kmer_idx, (total_freq, count) in kmer_stats[species].items():
            writer.writerow([species, kmer_idx, total_freq, count])

print(f"\n✅ Saved kmer stats : {KMER_STATS_FILE}")

# ===============================
# FINAL SUMMARY
# ===============================
print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print(f"  Species encoded     : {len(label_map)}")
print(f"  Train output        : {TRAIN_OUTPUT}")
print(f"  Test output         : {TEST_OUTPUT}")
print(f"  Label map           : {LABEL_MAP_FILE}")
print(f"  Skipped test lines  : {skipped}")
print("\n✅ DONE")
