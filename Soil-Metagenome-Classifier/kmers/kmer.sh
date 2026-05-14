#!/bin/bash
#SBATCH --job-name=Ktask
#SBATCH --partition=vriksha
#SBATCH --nodelist=service2
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=80
#SBATCH --mem=200G
#SBATCH --time=140:00:00
#SBATCH --output=/lustre/scratch/gylab204/taiba/project/kmers/kmer_%j.out
#SBATCH --error=/lustre/scratch/gylab204/taiba/project/kmers/kmer_%j.err

mkdir -p /lustre/scratch/gylab204/taiba/project/logs

cd /lustre/scratch/gylab204/taiba/project || exit 1

PYTHON=/lustre/home/gylab204/.conda/envs/mgs/bin/python

echo "======================================"
echo "Running on   : $(hostname)"
echo "Start time   : $(date)"
echo "CPUs assigned: $SLURM_CPUS_PER_TASK"
echo "Using Python :"
$PYTHON --version
echo "======================================"

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1

echo "Starting k-merization..."
$PYTHON /lustre/scratch/gylab204/taiba/project/kmers/kmerization.py
echo "Finished k-merization!"

echo "End time: $(date)"
echo "======================================"

