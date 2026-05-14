#!/usr/bin/env python3
"""
model_train.py
==============================================================================
4-Node Distributed XGBoost
Nodes : service2 (r0) + service7 (r1) + service8 (r2) + service10 (r3)
All in vriksha partition — no partition issues.

DATA SPLIT:
  93,822,292 total train rows ÷ 4 nodes = ~23.5M rows per node
  Each node: 80% train (~18.8M) / 20% val (~4.7M)
  Test set (52M rows): loaded by rank 0 AFTER training only

MEMORY PER NODE (safe for service8 with 114GB free):
  scipy sparse during load  : ~24GB → freed immediately after DMatrix
  GHistIndexMatrix          : ~39GB (18.8M rows × 2080 × 1 byte)
  Gradient pairs            : ~47GB (18.8M × 306 × 8 bytes)
  Model + buffers           : ~15GB
  PEAK                      : ~101GB → fits in 114GB free on service8 ✅

ESTIMATED TIMING:
  Data loading  : ~25 min  (all 4 nodes parallel, 23.5M each)
  Per round     : ~1–1.5 min  (25% less data vs 3-node)
  Total rounds  : ~150–200
  Training      : ~3–5 hrs
  Test + save   : ~1 hr
  TOTAL         : ~4–6 hrs

SPEED PARAMETERS (same as before):
  max_depth=6  subsample=0.5  colsample=0.5  lr=0.15
  val_only eval  verbose/5  early_stop=20  80/20 split
==============================================================================
"""

import gc
import io
import json
import os
import re
import sys
import time
import socket
import numpy as np
import multiprocessing
import pandas as pd
import scipy.sparse as sp
from datetime import datetime

import xgboost as xgb
from xgboost import collective
from xgboost.tracker import RabitTracker
from sklearn.datasets import load_svmlight_file
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix,
)

# ══════════════════════════════════════════════════════════════════════════════
# THREAD CONTROL
# ══════════════════════════════════════════════════════════════════════════════
os.environ["OMP_NUM_THREADS"]      = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"]      = "1"
os.environ["NUMEXPR_NUM_THREADS"]  = "1"

# ══════════════════════════════════════════════════════════════════════════════
# PATHS
# ══════════════════════════════════════════════════════════════════════════════
DATA_DIR  = "/lustre/scratch/gylab204/taiba/project/kmers/ml"
CACHE_DIR = os.path.join(DATA_DIR, "cache")
LOG_DIR   = os.path.join(DATA_DIR, "logs")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(LOG_DIR,   exist_ok=True)

TRAIN_FILE       = f"{DATA_DIR}/train_encoded.libsvm"
TEST_FILE        = f"{DATA_DIR}/test_encoded.libsvm"
LABEL_MAP_FILE   = f"{DATA_DIR}/label_map.json"
MODEL_SAVE_PATH  = f"{DATA_DIR}/xgboost_model.json"
METRICS_PATH     = f"{DATA_DIR}/metrics.json"
WORKER_ARGS_FILE = f"{CACHE_DIR}/worker_args.json"
OFFSET_FILE      = f"{CACHE_DIR}/shard_offsets.json"
TMP_CHUNK        = f"{CACHE_DIR}/tmp_{os.getpid()}.libsvm"

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
NUM_CORES   = multiprocessing.cpu_count()
NTHREAD     = int(os.environ.get("XGB_NTHREAD", 56))
N_FEATURES  = 2080
CHUNK_LINES = 5_000_000
NUM_ROUNDS  = 500
EARLY_STOP  = 20
RABIT_PORT  = 9091
VAL_FRAC    = 0.20

# ══════════════════════════════════════════════════════════════════════════════
# SLURM IDENTITY
# ══════════════════════════════════════════════════════════════════════════════
RANK      = int(os.environ.get("SLURM_NODEID", 0))
NODE_LIST = os.environ.get("SLURM_NODELIST",   socket.gethostname())
HOSTNAME  = socket.gethostname()
NUM_NODES = int(os.environ.get("SLURM_NNODES", 1))

# ══════════════════════════════════════════════════════════════════════════════
# LOGGING
# ══════════════════════════════════════════════════════════════════════════════
ICONS = {
    "INFO" : "ℹ ",
    "OK"   : "✅",
    "WARN" : "⚠️ ",
    "ERR"  : "❌",
    "MEM"  : "🧠",
    "SYNC" : "🔗",
    "TRAIN": "🌲",
    "SPEED": "⚡",
    "DATA" : "📂",
    "SAVE" : "💾",
}

def log(msg, level="INFO"):
    ts  = datetime.now().strftime("%H:%M:%S")
    tag = ICONS.get(level, "  ")
    print(f"[{HOSTNAME}|r{RANK}] [{ts}] {tag}  {msg}", flush=True)

def section(title):
    bar = "═" * 72
    print(f"\n{bar}", flush=True)
    print(f"  [{HOSTNAME}|r{RANK}]  {title}", flush=True)
    print(f"{bar}\n", flush=True)

def log_mem():
    try:
        with open("/proc/meminfo") as f:
            info = {}
            for line in f:
                p = line.split()
                info[p[0].rstrip(":")] = int(p[1])
        total = info["MemTotal"]     / 1024 / 1024
        avail = info["MemAvailable"] / 1024 / 1024
        used  = total - avail
        pct   = used / total * 100
        bar   = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        log(f"RAM [{bar}] {pct:.0f}%  used:{used:.0f}GB  free:{avail:.0f}GB  total:{total:.0f}GB", "MEM")
    except Exception:
        pass

def wait_for_file(path, label, timeout=300, poll=5):
    waited = 0
    while not os.path.exists(path):
        time.sleep(poll)
        waited += poll
        if waited % 30 == 0:
            log(f"Still waiting for {label}... ({waited}s / {timeout}s)", "WARN")
        if waited >= timeout:
            log(f"TIMEOUT — {label} never appeared after {timeout}s", "ERR")
            sys.exit(1)
    time.sleep(2)
    log(f"Received: {label}", "OK")

# ══════════════════════════════════════════════════════════════════════════════
# PARSE NODE 0 HOSTNAME
# ══════════════════════════════════════════════════════════════════════════════
def parse_first_host(node_list):
    m = re.match(r'^([^\[,]+)(?:\[([^\]]+)\])?', node_list)
    if not m:
        return node_list.split(",")[0]
    base, ranges = m.group(1), m.group(2)
    if not ranges:
        return base
    return base + re.split(r'[-,]', ranges)[0]

NODE0_HOST = parse_first_host(NODE_LIST)

# ══════════════════════════════════════════════════════════════════════════════
# STARTUP BANNER
# ══════════════════════════════════════════════════════════════════════════════
section("3-NODE DISTRIBUTED XGBOOST — service2+service7+service10 — 306 SPECIES")
log(f"XGBoost version  : {xgb.__version__}")
log(f"Python version   : {sys.version.split()[0]}")
log(f"Hostname         : {HOSTNAME}")
log(f"SLURM rank       : {RANK}  ({'master+tracker' if RANK == 0 else 'worker'})")
log(f"Total nodes      : {NUM_NODES}")
log(f"CPU cores avail  : {NUM_CORES}")
log(f"XGBoost threads  : {NTHREAD}")
log(f"SLURM_NODELIST   : {NODE_LIST}")
log(f"Node 0 host      : {NODE0_HOST}")
log(f"Rabit tracker    : {NODE0_HOST}:{RABIT_PORT}")
log("")
log("SPEED PARAMETERS:", "SPEED")
log("  max_depth=6  subsample=0.5  colsample=0.5  lr=0.15", "SPEED")
log("  80/20 split  val_only  verbose/5  early_stop=20", "SPEED")
log("  3 nodes × 31.3M rows = 93.8M total — ZERO DATA LOSS", "SPEED")
log("  est. ~1.5–2.5 min/round → ~5–9 hrs total", "SPEED")
log("")
log_mem()

# ══════════════════════════════════════════════════════════════════════════════
# LABEL MAP
# ══════════════════════════════════════════════════════════════════════════════
with open(LABEL_MAP_FILE) as f:
    label_map = json.load(f)
num_classes      = len(label_map)
label_to_species = {v: k for k, v in label_map.items()}
log(f"Species (classes): {num_classes}", "OK")

# ══════════════════════════════════════════════════════════════════════════════
# RABIT TRACKER
# ══════════════════════════════════════════════════════════════════════════════
section("RABIT TRACKER SETUP")

tracker     = None
worker_args = None

if RANK == 0:
    log(f"Starting RabitTracker for {NUM_NODES} workers on {NODE0_HOST}:{RABIT_PORT}", "SYNC")
    tracker = RabitTracker(
        n_workers = NUM_NODES,
        host_ip   = NODE0_HOST,
        port      = RABIT_PORT,
    )
    tracker.start()
    worker_args = tracker.worker_args()
    log(f"Tracker started — worker_args: {worker_args}", "SYNC")
    with open(WORKER_ARGS_FILE, "w") as f:
        json.dump(worker_args, f)
    log(f"Worker args written for all ranks", "OK")

else:
    log(f"Rank {RANK}: waiting for rank 0 tracker...", "SYNC")
    wait_for_file(WORKER_ARGS_FILE, "worker_args.json", timeout=300)
    with open(WORKER_ARGS_FILE) as f:
        worker_args = json.load(f)
    log(f"Worker args received: {worker_args}", "OK")

log(f"All ranks have worker_args — ready for distributed training", "SYNC")

# ══════════════════════════════════════════════════════════════════════════════
# SHARD COMPUTATION
# ══════════════════════════════════════════════════════════════════════════════
section("COMPUTING DATA SHARDS  (4 equal parts of 93.8M rows)")

def compute_shard_offsets(path, n_nodes):
    log(f"Counting total lines in {os.path.basename(path)}...", "DATA")
    total = 0
    with open(path, "rb") as f:
        for _ in f:
            total += 1
    log(f"Total lines: {total:,}", "OK")

    base_rows = total // n_nodes
    offsets   = []

    with open(path, "rb") as f:
        for node in range(n_nodes):
            byte_start = f.tell()
            n_rows     = base_rows if node < n_nodes - 1 else total - base_rows * (n_nodes - 1)
            for _ in range(n_rows):
                if not f.readline():
                    break
            offsets.append((byte_start, n_rows))
            log(f"  Shard {node} (rank {node}): "
                f"byte={byte_start:>16,}  "
                f"rows={n_rows:,}  "
                f"({n_rows/total*100:.1f}%)")

    return total, offsets

if RANK == 0:
    total_lines, shard_offsets = compute_shard_offsets(TRAIN_FILE, NUM_NODES)
    with open(OFFSET_FILE, "w") as f:
        json.dump({"total": total_lines, "offsets": shard_offsets}, f)
    log(f"Shard offsets written: {OFFSET_FILE}", "OK")
else:
    log(f"Rank {RANK}: waiting for shard offsets from rank 0...", "DATA")
    wait_for_file(OFFSET_FILE, "shard_offsets.json", timeout=300)
    with open(OFFSET_FILE) as f:
        d = json.load(f)
    total_lines   = d["total"]
    shard_offsets = [tuple(x) for x in d["offsets"]]
    log(f"Shard offsets received — total_lines={total_lines:,}", "OK")

my_byte_start, my_shard_rows = shard_offsets[RANK]

log(f"")
log(f"My shard summary:")
log(f"  Rank         : {RANK}")
log(f"  Byte start   : {my_byte_start:,}")
log(f"  Rows         : {my_shard_rows:,}  ({my_shard_rows/total_lines*100:.1f}% of total)")
log(f"  Train (80%)  : {int(my_shard_rows * 0.80):,}")
log(f"  Val   (20%)  : {int(my_shard_rows * 0.20):,}")

# ══════════════════════════════════════════════════════════════════════════════
# CHUNKED LIBSVM LOADER
# ══════════════════════════════════════════════════════════════════════════════
def load_libsvm_chunked(path, n_features, chunk_lines, label,
                         byte_start=0, max_rows=None):

    section(f"LOADING {label}  ({max_rows:,} rows)" if max_rows else f"LOADING {label}")

    est_chunks = max(1, (max_rows // chunk_lines)) if max_rows else "?"
    log(f"File       : {os.path.basename(path)}", "DATA")
    log(f"Byte start : {byte_start:,}", "DATA")
    log(f"Max rows   : {max_rows:,}" if max_rows else "Max rows   : all", "DATA")
    log(f"Chunk size : {chunk_lines:,} lines/chunk", "DATA")
    log(f"Est chunks : {est_chunks}", "DATA")
    log_mem()

    X_chunks, y_chunks = [], []
    loaded   = 0
    chunk_no = 0
    t_start  = time.time()

    with open(path, "rb") as raw:
        raw.seek(byte_start)
        f = io.TextIOWrapper(raw, encoding="utf-8")

        while True:
            want = (min(chunk_lines, max_rows - loaded)
                    if max_rows else chunk_lines)
            if want <= 0:
                break

            lines = []
            for _ in range(want):
                line = f.readline()
                if not line:
                    break
                lines.append(line)
            if not lines:
                break

            chunk_no += 1
            t0 = time.time()

            with open(TMP_CHUNK, "w") as tmp:
                tmp.writelines(lines)

            X_c, y_c = load_svmlight_file(
                TMP_CHUNK,
                n_features = n_features,
                zero_based = True,
                dtype      = np.float32,
            )
            X_chunks.append(X_c)
            y_chunks.append(y_c)

            loaded       += len(lines)
            elapsed       = time.time() - t0
            total_elapsed = time.time() - t_start
            pct           = (loaded / max_rows * 100) if max_rows else 0
            remain        = (est_chunks - chunk_no) if isinstance(est_chunks, int) else "?"
            eta           = (f"{elapsed * remain / 60:.1f} min"
                             if isinstance(remain, int) else "?")
            filled = int(pct / 5)
            bar    = "█" * filled + "░" * (20 - filled)

            log(f"Chunk {chunk_no:>2}/{est_chunks}  [{bar}] {pct:5.1f}%"
                f"  rows: {loaded:>11,}/{max_rows if max_rows else '?':,}"
                f"  chunk: {elapsed:.0f}s"
                f"  elapsed: {total_elapsed/60:.1f}min"
                f"  ETA: {eta}", "DATA")

    if os.path.exists(TMP_CHUNK):
        os.remove(TMP_CHUNK)

    log(f"All {chunk_no}/{chunk_no} chunks loaded — stacking...", "OK")
    t0 = time.time()
    X  = sp.vstack(X_chunks, format="csr")
    y  = np.concatenate(y_chunks)
    del X_chunks, y_chunks
    gc.collect()

    log(f"Stack done     : {time.time()-t0:.1f}s", "OK")
    log(f"Final shape    : {X.shape[0]:,} rows × {X.shape[1]} features", "OK")
    log(f"Total load time: {(time.time()-t_start)/60:.1f} min", "OK")
    log_mem()
    return X, y

# ══════════════════════════════════════════════════════════════════════════════
# LOAD THIS NODE'S SHARD
# ══════════════════════════════════════════════════════════════════════════════
X_shard, y_shard = load_libsvm_chunked(
    TRAIN_FILE, N_FEATURES, CHUNK_LINES,
    label      = f"TRAIN-SHARD-r{RANK}",
    byte_start = my_byte_start,
    max_rows   = my_shard_rows,
)

# ══════════════════════════════════════════════════════════════════════════════
# VERIFY CLASSES
# ══════════════════════════════════════════════════════════════════════════════
section(f"CLASS VERIFICATION  (rank {RANK})")

unique_shard  = np.unique(y_shard.astype(int))
missing_shard = set(range(num_classes)) - set(unique_shard.tolist())

log(f"Classes in this shard : {len(unique_shard)} / {num_classes}")
log(f"Label range           : {unique_shard.min()} → {unique_shard.max()}")
if missing_shard:
    log(f"Missing from shard    : {len(missing_shard)} classes", "WARN")
    log(f"  Covered by other nodes via Rabit allreduce ✅", "WARN")
else:
    log(f"All {num_classes} classes present in this shard", "OK")

# ══════════════════════════════════════════════════════════════════════════════
# 80/20 SPLIT
# ══════════════════════════════════════════════════════════════════════════════
section(f"TRAIN / VALIDATION SPLIT  80/20  (rank {RANK})")

np.random.seed(42 + RANK)
idx    = np.random.permutation(X_shard.shape[0])
split  = int((1 - VAL_FRAC) * len(idx))
tr_idx = idx[:split]
va_idx = idx[split:]

X_tr, y_tr = X_shard[tr_idx], y_shard[tr_idx]
X_va, y_va = X_shard[va_idx], y_shard[va_idx]
del X_shard, y_shard, idx, tr_idx, va_idx
gc.collect()

log(f"Train rows (80%) : {X_tr.shape[0]:,}", "OK")
log(f"Val   rows (20%) : {X_va.shape[0]:,}", "OK")
log_mem()

# ══════════════════════════════════════════════════════════════════════════════
# BUILD DMATRIX
# ══════════════════════════════════════════════════════════════════════════════
section(f"BUILDING DMATRIX  (rank {RANK})")

log("Converting train → DMatrix...")
dtrain_local = xgb.DMatrix(X_tr, label=y_tr)
del X_tr, y_tr
gc.collect()
log(f"dtrain_local ready : {dtrain_local.num_row():,} rows × {dtrain_local.num_col()} features", "OK")
log_mem()

log("Converting val → DMatrix...")
dval_local = xgb.DMatrix(X_va, label=y_va)
del X_va, y_va
gc.collect()
log(f"dval_local ready   : {dval_local.num_row():,} rows", "OK")
log_mem()

# ══════════════════════════════════════════════════════════════════════════════
# XGBOOST PARAMETERS
# ══════════════════════════════════════════════════════════════════════════════
params = {
    "objective"        : "multi:softprob",
    "eval_metric"      : "mlogloss",
    "num_class"        : num_classes,
    "max_depth"        : 6,
    "max_bin"          : 128,
    "tree_method"      : "hist",
    "min_child_weight" : 5,
    "subsample"        : 0.5,
    "colsample_bytree" : 0.5,
    "learning_rate"    : 0.15,
    "seed"             : 42,
    "nthread"          : NTHREAD,
    "verbosity"        : 1,
}

# ══════════════════════════════════════════════════════════════════════════════
# DISTRIBUTED TRAINING
# ══════════════════════════════════════════════════════════════════════════════
section(f"DISTRIBUTED TRAINING  (max {NUM_ROUNDS} | early stop {EARLY_STOP} | print every 5)")

log("XGBoost parameters:")
log("─" * 52)
for k, v in params.items():
    log(f"  {k:<22} : {v}")
log("─" * 52)
log("")
log("DISTRIBUTED SETUP:", "SYNC")
log(f"  3 nodes × ~31.3M rows = 93.8M total — ZERO DATA LOSS", "SYNC")
log(f"  Each node trains on 80% of its shard (~18.8M rows)", "SYNC")
log(f"  Rabit allreduce sums gradients after every tree", "SYNC")
log(f"  All 4 nodes produce IDENTICAL loss values each round", "SYNC")
log(f"  Rank 0 handles test evaluation and saving", "SYNC")
log("")
log(f"  worker_args: {worker_args}", "SYNC")
log("")
log("Entering CommunicatorContext — handshake with tracker...", "SYNC")
log_mem()

evals        = [(dval_local, "eval")]
evals_result = {}
start_train  = time.time()

with collective.CommunicatorContext(**worker_args):
    log("CommunicatorContext active — all 4 nodes synchronised ✅", "SYNC")
    log("Training starts now — round progress every 5 rounds:", "TRAIN")
    log("")

    model = xgb.train(
        params,
        dtrain_local,
        num_boost_round       = NUM_ROUNDS,
        evals                 = evals,
        evals_result          = evals_result,
        early_stopping_rounds = EARLY_STOP,
        verbose_eval          = 5,
    )

train_time = time.time() - start_train
best_round = model.best_iteration
best_score = model.best_score

log("")
log("CommunicatorContext exited cleanly", "SYNC")
log(f"Training complete!", "OK")
log(f"  Best round       : {best_round}")
log(f"  Best mlogloss    : {best_score:.6f}")
log(f"  Training time    : {train_time:.0f}s  ({train_time/60:.1f} min)  ({train_time/3600:.2f} hrs)")
log(f"  Approx speed     : {best_round / (train_time/60):.1f} rounds/min")

del dtrain_local, dval_local
gc.collect()
log("Train/val DMatrices freed", "OK")
log_mem()

# ══════════════════════════════════════════════════════════════════════════════
# RANK 0 — EVALUATION AND SAVING
# ══════════════════════════════════════════════════════════════════════════════
if RANK == 0:

    if tracker:
        log("Calling tracker.wait_for()...", "SYNC")
        tracker.wait_for()
        log("Tracker shut down cleanly", "OK")

    # ── Load test ─────────────────────────────────────────────────────────
    X_test, y_test_raw = load_libsvm_chunked(
        TEST_FILE, N_FEATURES, CHUNK_LINES,
        label="TEST", byte_start=0, max_rows=None,
    )

    unique_test  = np.unique(y_test_raw.astype(int))
    missing_test = set(range(num_classes)) - set(unique_test.tolist())
    log(f"Classes in test  : {len(unique_test)} / {num_classes}")
    if missing_test:
        log(f"Missing from test : {len(missing_test)}", "WARN")
    else:
        log("All 306 classes present in test", "OK")

    log("Converting test → DMatrix...")
    dtest       = xgb.DMatrix(X_test, label=y_test_raw)
    y_test      = y_test_raw.astype(int)
    del X_test, y_test_raw
    gc.collect()
    log(f"Test DMatrix     : {dtest.num_row():,} rows", "OK")
    log_mem()

    # ── Inference ─────────────────────────────────────────────────────────
    section("INFERENCE ON TEST SET")
    log(f"Test samples     : {dtest.num_row():,}")
    log("Running model.predict()...")
    start_test = time.time()
    y_prob     = model.predict(dtest)
    y_pred     = np.argmax(y_prob, axis=1)
    del y_prob
    gc.collect()
    test_time      = time.time() - start_test
    y_test_labels  = dtest.get_label().astype(int)

    log(f"Inference done   : {test_time:.1f}s", "OK")
    log(f"Unique predicted : {len(np.unique(y_pred))} / {num_classes} classes")
    log(f"Unique true      : {len(np.unique(y_test_labels))} / {num_classes} classes")

    # ── Metrics ───────────────────────────────────────────────────────────
    section("EVALUATION METRICS")

    accuracy  = accuracy_score(y_test_labels, y_pred)
    precision = precision_score(y_test_labels, y_pred, average="macro", zero_division=0)
    recall    = recall_score(y_test_labels,    y_pred, average="macro", zero_division=0)
    f1        = f1_score(y_test_labels,        y_pred, average="macro", zero_division=0)
    cm        = confusion_matrix(y_test_labels, y_pred)

    specificities = []
    total_cm      = int(np.sum(cm))
    for i in range(num_classes):
        tn   = total_cm - np.sum(cm[i,:]) - np.sum(cm[:,i]) + cm[i,i]
        fp   = np.sum(cm[:,i]) - cm[i,i]
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        specificities.append(spec)
    macro_spec = float(np.mean(specificities))

    log(f"Accuracy            : {accuracy:.4f}  ({accuracy*100:.2f}%)", "OK")
    log(f"Precision (macro)   : {precision:.4f}", "OK")
    log(f"Recall (macro)      : {recall:.4f}", "OK")
    log(f"Specificity (macro) : {macro_spec:.4f}", "OK")
    log(f"F1-score (macro)    : {f1:.4f}", "OK")

    # ── Save ──────────────────────────────────────────────────────────────
    section("SAVING ALL OUTPUTS")

    model.save_model(MODEL_SAVE_PATH)
    log(f"Model              : {MODEL_SAVE_PATH}", "SAVE")

    metrics = {
        "accuracy"          : float(accuracy),
        "precision_macro"   : float(precision),
        "recall_macro"      : float(recall),
        "specificity_macro" : macro_spec,
        "f1_macro"          : float(f1),
        "training_time_sec" : train_time,
        "training_time_hrs" : round(train_time / 3600, 3),
        "inference_time_sec": test_time,
        "total_time_sec"    : train_time + test_time,
        "num_classes"       : num_classes,
        "best_round"        : best_round,
        "best_mlogloss"     : float(best_score),
        "total_train_rows"  : int(total_lines),
        "test_rows"         : int(dtest.num_row()),
        "nodes_used"        : ["service2", "service7", "service10"],
        "rows_per_node"     : int(my_shard_rows),
        "nthread_per_node"  : NTHREAD,
        "xgb_params"        : {k: str(v) for k, v in params.items()},
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    log(f"Metrics            : {METRICS_PATH}", "SAVE")

    np.save(os.path.join(DATA_DIR, "y_test.npy"),           y_test_labels)
    np.save(os.path.join(DATA_DIR, "y_pred.npy"),           y_pred)
    np.save(os.path.join(DATA_DIR, "confusion_matrix.npy"), cm)
    log("y_test.npy         : saved", "SAVE")
    log("y_pred.npy         : saved", "SAVE")
    log("confusion_matrix   : saved", "SAVE")

    tp_list, fp_list, fn_list, tn_list = [], [], [], []
    for i in range(num_classes):
        tp = cm[i,i]
        fp = np.sum(cm[:,i]) - tp
        fn = np.sum(cm[i,:]) - tp
        tn = total_cm - (tp + fp + fn)
        tp_list.append(int(tp))
        fp_list.append(int(fp))
        fn_list.append(int(fn))
        tn_list.append(int(tn))

    conf_path = os.path.join(DATA_DIR, "tp_fp_tn_fn_per_class.csv")
    pd.DataFrame({
        "species" : [label_to_species[i] for i in range(num_classes)],
        "TP" : tp_list, "FP": fp_list,
        "FN" : fn_list, "TN": tn_list,
    }).to_csv(conf_path, index=False)
    log(f"Per-class stats    : {conf_path}", "SAVE")

    for fpath in [WORKER_ARGS_FILE, OFFSET_FILE]:
        if os.path.exists(fpath):
            os.remove(fpath)
    log("Cache flag files cleaned up", "OK")

    # ── Final summary ──────────────────────────────────────────────────────
    section("FINAL SUMMARY")
    log(f"Nodes               : service2(r0)  service7(r1)  service10(r2)")
    log(f"Total train rows    : {total_lines:,}  (ALL used — zero dropped)")
    log(f"Rows per node       : ~{my_shard_rows:,}")
    log(f"Species             : {num_classes}")
    log(f"Test samples        : {dtest.num_row():,}")
    log(f"")
    log(f"Best round          : {best_round}", "TRAIN")
    log(f"Best mlogloss       : {best_score:.6f}", "TRAIN")
    log(f"")
    log(f"Accuracy            : {accuracy*100:.2f}%", "OK")
    log(f"F1-score (macro)    : {f1:.4f}", "OK")
    log(f"Precision (macro)   : {precision:.4f}", "OK")
    log(f"Recall (macro)      : {recall:.4f}", "OK")
    log(f"Specificity (macro) : {macro_spec:.4f}", "OK")
    log(f"")
    log(f"Training time       : {train_time/3600:.2f} hrs  ({train_time/60:.1f} min)")
    log(f"Inference time      : {test_time:.1f}s")
    log(f"Total time          : {(train_time+test_time)/3600:.2f} hrs")
    log(f"")
    log("ALL OUTPUTS SAVED SUCCESSFULLY", "SAVE")
    print("\n✅ RANK 0 COMPLETE\n", flush=True)

else:
    log(f"Rank {RANK} complete — outputs handled by rank 0", "OK")
    print(f"\n✅ RANK {RANK} COMPLETE\n", flush=True)
