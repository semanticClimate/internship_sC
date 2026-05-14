#!/bin/bash
#SBATCH --job-name=encode_libsvm
#SBATCH --partition=vriksha
#SBATCH --nodelist=service2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=150G
#SBATCH --time=24:00:00
#SBATCH --output=/lustre/scratch/gylab204/taiba/project/kmers/ml/encode_%j.out
#SBATCH --error=/lustre/scratch/gylab204/taiba/project/kmers/ml/encode_%j.err

# ===============================
# CREATE OUTPUT DIR
# ===============================
mkdir -p /lustre/scratch/gylab204/taiba/project/kmers/ml

# ===============================
# GO TO PROJECT DIR
# ===============================
cd /lustre/scratch/gylab204/taiba/project || exit 1

# ===============================
# PYTHON
# ===============================
PYTHON=/lustre/home/gylab204/.conda/envs/mgs/bin/python

echo "======================================"
echo "Running on   : $(hostname)"
echo "Start time   : $(date)"
echo "Using Python :"
$PYTHON --version
echo "======================================"

# ===============================
# THIS SCRIPT IS SINGLE THREADED
# no multiprocessing — these vars
# prevent any library from spawning
# extra threads unnecessarily
# ===============================
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

# ===============================
# RUN
# ===============================
echo "Starting label encoding..."
$PYTHON /lustre/scratch/gylab204/taiba/project/kmers/process_libsvm.py

echo "Finished encoding!"
echo "End time: $(date)"
echo "======================================"

