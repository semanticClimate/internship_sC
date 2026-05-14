#!/bin/bash
#SBATCH --job-name=fragmentation
#SBATCH --nodelist=service2
#SBATCH --output=/lustre/scratch/gylab204/taiba/project/logs/fragmentation_%j.out
#SBATCH --error=/lustre/scratch/gylab204/taiba/project/logs/fragmentation_%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=50
#SBATCH --mem=100G
#SBATCH --time=48:00:00

# ===============================
# CREATE LOG DIRECTORY (must exist before job starts)
# ===============================
mkdir -p /lustre/scratch/gylab204/taiba/project/logs

# ===============================
# PRINT JOB INFO
# ===============================
echo "======================================"
echo "Job ID: $SLURM_JOB_ID"
echo "Running on: $(hostname)"
echo "Start Time: $(date)"
echo "======================================"

# ===============================
# GO TO PROJECT DIRECTORY
# ===============================
cd /lustre/scratch/gylab204/taiba/project/ || exit 1

# ===============================
# USE ENV PYTHON DIRECTLY (robust)
# ===============================
PYTHON=/lustre/home/gylab204/.conda/envs/mgs/bin/python

echo "Using Python:"
$PYTHON --version

# ===============================
# MULTIPROCESSING SAFETY
# ===============================
export OMP_NUM_THREADS=1

# ===============================
# DEBUG (important)
# ===============================
echo "Working directory: $(pwd)"
echo "Check fragments script:"
ls fragments

# ===============================
# RUN SCRIPT
# ===============================
echo "Starting fragmentation..."
$PYTHON fragments/fragmentation_test.py

echo "Fragmentation test finished!"

# ===============================
# RESOURCE USAGE CHECK
# ===============================
echo "Max memory usage:"
sstat -j ${SLURM_JOB_ID}.batch --format=MaxRSS 2>/dev/null

# ===============================
# END INFO
# ===============================
echo "End Time: $(date)"
echo "======================================"
