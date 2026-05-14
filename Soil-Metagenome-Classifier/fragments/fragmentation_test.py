import os
import random
import csv
from multiprocessing import Pool

# ===============================
# CONFIG
# ===============================
BASE_PATH = "/lustre/scratch/gylab204/taiba/project"

INPUT_DIR = os.path.join(BASE_PATH, "test_later")
OUTPUT_DIR = os.path.join(BASE_PATH, "fragments/test")

FRAGMENT_LENGTH = 150
COVERAGE = 2
NUM_CORES = 48

# ===============================
# READ FASTA
# ===============================
def read_fna(file_path):
    seq = []
    with open(file_path, "r") as f:
        for line in f:
            if not line.startswith(">"):
                seq.append(line.strip().upper())
    sequence = "".join(seq)
    return sequence, len(sequence)

# ===============================
# PROCESS ONE GENOME
# ===============================
def process_genome(args):
    species, file_path = args

    strain = os.path.basename(file_path).replace(".fna", "")

    sequence, genome_size = read_fna(file_path)
    genome_size_mb = genome_size / 1e6

    num_fragments = int((COVERAGE * genome_size) / FRAGMENT_LENGTH)
    max_start = genome_size - FRAGMENT_LENGTH

    if max_start <= 0:
        return [], (species, strain, genome_size, genome_size_mb, 0, 0.0)

    fragments = []

    for _ in range(num_fragments):
        start = random.randint(0, max_start)
        frag = sequence[start:start + FRAGMENT_LENGTH]
        fragments.append((species, strain, frag))

    coverage = (num_fragments * FRAGMENT_LENGTH) / genome_size

    stats = (species, strain, genome_size, genome_size_mb, num_fragments, coverage)

    return fragments, stats

# ===============================
# COLLECT GENOMES
# ===============================
def collect_genomes(base_dir):
    genome_list = []

    for species in os.listdir(base_dir):
        species_path = os.path.join(base_dir, species)

        if not os.path.isdir(species_path):
            continue

        for file in os.listdir(species_path):
            if file.endswith(".fna"):
                genome_list.append((species, os.path.join(species_path, file)))

    return genome_list

# ===============================
# MAIN
# ===============================
def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    genome_list = collect_genomes(INPUT_DIR)
    print(f"Total test genomes: {len(genome_list)}")

    frag_file = os.path.join(OUTPUT_DIR, "test_fragments.csv")
    stats_file = os.path.join(OUTPUT_DIR, "test_fragment_stats.csv")
    genome_file = os.path.join(OUTPUT_DIR, "test_genome_sizes.csv")
    summary_file = os.path.join(OUTPUT_DIR, "test_summary.txt")

    total_fragments = 0
    total_genomes = 0
    species_set = set()

    with Pool(NUM_CORES) as pool, \
         open(frag_file, "w", newline="") as frag_f, \
         open(stats_file, "w", newline="") as stats_f, \
         open(genome_file, "w", newline="") as genome_f:

        frag_writer = csv.writer(frag_f)
        stats_writer = csv.writer(stats_f)
        genome_writer = csv.writer(genome_f)

        # SAME HEADERS AS TRAIN
        frag_writer.writerow(["species", "strain", "fragment"])
        stats_writer.writerow(["species", "strain", "bp", "mb", "fragments", "coverage"])
        genome_writer.writerow(["species", "strain", "bp", "mb", "coverage"])

        for fragments, stats in pool.imap_unordered(process_genome, genome_list):

            species, strain, bp, mb, n_frag, cov = stats

            for row in fragments:
                frag_writer.writerow(row)

            stats_writer.writerow([species, strain, bp, mb, n_frag, cov])
            genome_writer.writerow([species, strain, bp, mb, cov])

            total_fragments += n_frag
            total_genomes += 1
            species_set.add(species)

    # ===============================
    # SUMMARY FILE
    # ===============================
    with open(summary_file, "w") as f:
        f.write("=== Test Fragmentation Summary ===\n\n")
        f.write(f"Total genomes: {total_genomes}\n")
        f.write(f"Total species: {len(species_set)}\n")
        f.write(f"Total fragments: {total_fragments}\n")

    print("\n✅ Test fragmentation complete!")
    print(f"📊 Total fragments: {total_fragments}")
    print(f"📁 Output: {OUTPUT_DIR}")

# ===============================
if __name__ == "__main__":
    main()
