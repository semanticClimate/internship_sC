#!/bin/bash
#SBATCH --job-name=xgb_3node
#SBATCH --partition=vriksha
#SBATCH --nodelist=service2,service7,service10
#SBATCH --nodes=3
#SBATCH --ntasks=3
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=112
#SBATCH --mem=450G
#SBATCH --time=140:00:00
#SBATCH --output=/lustre/scratch/gylab204/taiba/project/kmers/ml/logs/train_%j.out
#SBATCH --error=/lustre/scratch/gylab204/taiba/project/kmers/ml/logs/train_%j.err

# ══════════════════════════════════════════════════════
# WHY THESE 3 NODES:
#   service2  → 1% RAM used  (6GB)   ✅ clean
#   service7  → 1% RAM used  (5GB)   ✅ clean
#   service10 → 1% RAM used  (6GB)   ✅ clean
#
#   service4  → EXCLUDED (437GB used by others — OOM)
#   service8  → EXCLUDED (393GB used by others — OOM)
#   service3  → EXCLUDED (DOWN+DRAIN)
# ══════════════════════════════════════════════════════

export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export XGB_NTHREAD=56

# ══════════════════════════════════════════════════════
# DIRS
# ══════════════════════════════════════════════════════
mkdir -p /lustre/scratch/gylab204/taiba/project/kmers/ml/logs
mkdir -p /lustre/scratch/gylab204/taiba/project/kmers/ml/cache
mkdir -p /lustre/scratch/gylab204/taiba/project/kmers/ml/plots

cd /lustre/scratch/gylab204/taiba/project || exit 1

PYTHON=/lustre/home/gylab204/.conda/envs/mgs/bin/python
SCRIPT=/lustre/scratch/gylab204/taiba/project/kmers/ml/model_train.py

# ══════════════════════════════════════════════════════
# BANNER
# ══════════════════════════════════════════════════════
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   3-NODE DISTRIBUTED XGBOOST — 306 SPECIES          ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  Python     : $($PYTHON --version 2>&1)              "
echo "║  Job ID     : $SLURM_JOB_ID                          "
echo "║  Nodes      : $SLURM_NODELIST                        "
echo "║  Num nodes  : $SLURM_NNODES                          "
echo "║  CPUs/node  : $SLURM_CPUS_PER_TASK                   "
echo "║  Memory     : 450G per node                          ║"
echo "║  XGB/node   : $XGB_NTHREAD threads                   ║"
echo "║  Start      : $(date)                                "
echo "╠══════════════════════════════════════════════════════╣"
echo "║  NODE STATUS AT SUBMISSION:                          ║"
echo "║  service2  → clean (1% RAM)  rank 0 master          ║"
echo "║  service7  → clean (1% RAM)  rank 1 worker          ║"
echo "║  service10 → clean (1% RAM)  rank 2 worker          ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  DATA:  93,822,292 rows ÷ 3 nodes = 31.3M/node      ║"
echo "║  SPEED: max_depth=6 sub=0.5 col=0.5 lr=0.15         ║"
echo "║  EST:   ~1.5-2.5 min/round → 5-9 hrs total          ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# ══════════════════════════════════════════════════════
# CHECK ALL 3 NODES REACHABLE
# ══════════════════════════════════════════════════════
echo "Checking all 3 nodes are reachable..."
srun --ntasks=3 --ntasks-per-node=1 hostname
if [ $? -ne 0 ]; then
    echo "ERROR: Not all nodes reachable. Exiting."
    exit 1
fi
echo "All 3 nodes reachable ✅"
echo ""

# ══════════════════════════════════════════════════════
# CHECK RAM ON ALL NODES BEFORE STARTING
# ══════════════════════════════════════════════════════
echo "Checking RAM on all nodes..."
srun --ntasks=3 --ntasks-per-node=1 bash -c \
    'echo "$(hostname): $(free -h | awk \"/Mem:/{print \\$3 \\\" used / \\\" \\$2 \\\" total\\\"}\") "'
echo ""

# ══════════════════════════════════════════════════════
# CLEAN STALE FILES
# ══════════════════════════════════════════════════════
echo "Cleaning stale cache files..."
rm -f /lustre/scratch/gylab204/taiba/project/kmers/ml/cache/worker_args.json
rm -f /lustre/scratch/gylab204/taiba/project/kmers/ml/cache/shard_offsets.json
rm -f /lustre/scratch/gylab204/taiba/project/kmers/ml/cache/tmp_*.libsvm
echo "Cache cleaned ✅"
echo ""

# ══════════════════════════════════════════════════════
# LAUNCH
# SLURM_NODEID:
#   service2  → rank 0  (master + tracker + evaluator)
#   service7  → rank 1  (worker)
#   service10 → rank 2  (worker)
# ══════════════════════════════════════════════════════
echo "Launching 3-node distributed XGBoost..."
echo "(service2=r0, service7=r1, service10=r2)"
echo ""

srun --ntasks=3 \
     --ntasks-per-node=1 \
     --cpus-per-task=112 \
     $PYTHON $SCRIPT

EXIT_CODE=$?

# ══════════════════════════════════════════════════════
# FINISHED
# ══════════════════════════════════════════════════════
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  JOB FINISHED                                        ║"
echo "║  Exit code : $EXIT_CODE                              "
echo "║  End time  : $(date)                                 "
echo "╚══════════════════════════════════════════════════════╝"
echo ""

METRICS=/lustre/scratch/gylab204/taiba/project/kmers/ml/metrics.json
if [ -f "$METRICS" ]; then
    NUM_CLASSES=$(python3 -c \
        "import json; d=json.load(open('$METRICS')); print(d.get('num_classes',0))" 2>/dev/null)
    echo "════════════════════════════════════════════════"
    echo "  RESULTS  (num_classes=$NUM_CLASSES)"
    echo "════════════════════════════════════════════════"
    cat "$METRICS"
    echo ""
    if [ "$NUM_CLASSES" != "306" ]; then
        echo "⚠️  WARNING: num_classes=$NUM_CLASSES — this looks like old metrics!"
    else
        echo "✅ num_classes=306 confirmed — these are the correct results!"
    fi
else
    echo "WARNING: metrics.json not found — check .err log"
fi

exit $EXIT_CODE

