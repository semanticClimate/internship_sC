import os
import random
import csv
from multiprocessing import Pool

# ===============================
# CONFIG
# ===============================
BASE_PATH = "/lustre/scratch/gylab204/taiba/project"
OUTPUT_DIR = os.path.join(BASE_PATH, "fragments")

FRAGMENT_LENGTH = 150
COVERAGE = 2
NUM_CORES = 32

GENOME_CSV_OUTPUT = os.path.join(OUTPUT_DIR, "computed_genome_sizes.csv")

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

    # ===============================
    # FRAGMENTATION
    # ===============================
    num_fragments = int((COVERAGE * genome_size) / FRAGMENT_LENGTH)
    max_start = genome_size - FRAGMENT_LENGTH

    if max_start <= 0:
        return [], (species, strain, genome_size, genome_size_mb, 0, 0)

    fragments = []

    for _ in range(num_fragments):
        start = random.randint(0, max_start)
        frag = sequence[start:start + FRAGMENT_LENGTH]
        fragments.append((species, strain, frag))

    # ===============================
    # COVERAGE CHECK
    # ===============================
    coverage = (num_fragments * FRAGMENT_LENGTH) / genome_size if genome_size > 0 else 0

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
# MAIN FUNCTION
# ===============================
def run_fragmentation(input_folder, frag_output, stats_output, genome_csv_output):

    os.makedirs(os.path.dirname(frag_output), exist_ok=True)

    genome_list = collect_genomes(input_folder)
    print(f"Total genomes: {len(genome_list)}")

    total_fragments = 0

    with Pool(NUM_CORES) as pool, \
         open(frag_output, "w", newline="") as frag_f, \
         open(stats_output, "w", newline="") as stats_f, \
         open(genome_csv_output, "w", newline="") as genome_f:

        frag_writer = csv.writer(frag_f)
        stats_writer = csv.writer(stats_f)
        genome_writer = csv.writer(genome_f)

        # ✅ headers (simple names)
        frag_writer.writerow(["species", "strain", "fragment"])
        stats_writer.writerow(["species", "strain", "bp", "mb", "fragments", "coverage"])
        genome_writer.writerow(["species", "strain", "bp", "mb", "coverage"])

        for fragments, stats in pool.imap_unordered(process_genome, genome_list):

            species, strain, genome_size, genome_size_mb, num_fragments, coverage = stats

            # write fragments
            for row in fragments:
                frag_writer.writerow(row)

            # write stats
            stats_writer.writerow([species, strain, genome_size, genome_size_mb, num_fragments, coverage])

            # write genome csv
            genome_writer.writerow([species, strain, genome_size, genome_size_mb, coverage])

            total_fragments += num_fragments

    return total_fragments, len(genome_list)

# ===============================
# ENTRY
# ===============================
if __name__ == "__main__":

    train_path = os.path.join(BASE_PATH, "train")

    train_frag = os.path.join(OUTPUT_DIR, "train_fragments.csv")
    train_stats = os.path.join(OUTPUT_DIR, "train_fragment_stats.csv")

    print("\n🔹 TRAIN")
    train_total, train_genomes = run_fragmentation(
        train_path,
        train_frag,
        train_stats,
        GENOME_CSV_OUTPUT
    )

    summary_file = os.path.join(OUTPUT_DIR, "summary_stats.txt")

    with open(summary_file, "w") as f:
        f.write("=== Fragmentation Summary ===\n\n")
        f.write(f"Train genomes: {train_genomes}\n")
        f.write(f"Train fragments: {train_total}\n")

    print("\n✅ Done")
