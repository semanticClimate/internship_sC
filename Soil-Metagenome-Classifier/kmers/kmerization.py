import csv
import os
from itertools import product
from multiprocessing import Pool

K = 6

TRAIN_INPUT  = "/lustre/scratch/gylab204/taiba/project/fragments/train_fragments.csv"
TEST_INPUT   = "/lustre/scratch/gylab204/taiba/project/fragments/test/test_fragments.csv"

TRAIN_OUTPUT = "/lustre/scratch/gylab204/taiba/project/kmers/train.libsvm"
TEST_OUTPUT  = "/lustre/scratch/gylab204/taiba/project/kmers/test.libsvm"

NUM_CORES  = 48
CHUNK_SIZE = 1000

# ===============================
# VALID BASES
# ===============================
VALID = set("ACGT")

# ===============================
# REVERSE COMPLEMENT
# ===============================
def reverse_complement(seq):
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def canonical(kmer):
    rc = reverse_complement(kmer)
    return min(kmer, rc)

# ===============================
# BUILD INDEX
# ===============================
def build_kmer_index():
    kmers = [''.join(p) for p in product("ACGT", repeat=K)]
    canonical_set = sorted(set(canonical(k) for k in kmers))
    return {k: i for i, k in enumerate(canonical_set)}

KMER_INDEX = build_kmer_index()

# ===============================
# VECTOR → SPARSE FORMAT
# ===============================
def kmer_sparse(seq):
    counts = {}
    total = 0

    for i in range(len(seq) - K + 1):
        kmer = seq[i:i+K]

        # skip any kmer with ambiguous/non-standard bases (N, K, R, Y, S, W, M, etc.)
        if not all(b in VALID for b in kmer):
            continue

        kmer = canonical(kmer)
        idx = KMER_INDEX[kmer]

        counts[idx] = counts.get(idx, 0) + 1
        total += 1

    # normalize
    if total > 0:
        for k in counts:
            counts[k] /= total

    return counts

# ===============================
# PROCESS CHUNK
# ===============================
def process_chunk(rows):
    lines = []

    for row in rows:
        species  = row["species"]
        fragment = row["fragment"]

        features = kmer_sparse(fragment)

        # species name kept as string label here —
        # process_libsvm.py will encode it to integers
        feature_str = " ".join(f"{idx}:{val:.6f}" for idx, val in sorted(features.items()))
        line = f"{species} {feature_str}"

        lines.append(line)

    return lines

# ===============================
# RUN ONE FILE
# ===============================
def run(input_path, output_path):
    print(f"\n🔹 Processing: {input_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    chunk  = []
    tasks  = []

    with open(input_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            chunk.append(row)
            if len(chunk) == CHUNK_SIZE:
                tasks.append(chunk)
                chunk = []
        if chunk:
            tasks.append(chunk)

    print(f"   Total chunks: {len(tasks)}")

    pool = Pool(NUM_CORES)

    with open(output_path, "w") as out_f:
        for i, result in enumerate(pool.imap(process_chunk, tasks)):
            for line in result:
                out_f.write(line + "\n")
            if (i + 1) % 100 == 0:
                print(f"   Chunks done: {i + 1}/{len(tasks)}")

    pool.close()
    pool.join()

    print(f"✅ Saved: {output_path}")

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    run(TRAIN_INPUT,  TRAIN_OUTPUT)
    run(TEST_INPUT,   TEST_OUTPUT)
    print("\n✅ Both train and test LIBSVM files created")
