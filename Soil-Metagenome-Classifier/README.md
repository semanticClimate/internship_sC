# AI-Based Taxonomic Classification of Soil Metagenome

An alignment-free, machine learning framework for species-level taxonomic 
classification of soil metagenomes usin XGBoost.

---

## Overview

Soil microbiomes harbour extraordinary taxonomic diversity, with a single 
gram containing up to 10⁹ bacterial cells representing thousands of species. 
Conventional alignment-based classifiers such as BLAST and Kraken2 depend 
heavily on reference database completeness and impose substantial 
computational overhead, limiting their applicability to large, complex soil 
datasets.

This project develops an **alignment-free**, **machine learning-driven** 
pipeline that classifies short metagenomic DNA fragments to species level 
using canonical hexanucleotide (6-mer) frequency profiles and an XGBoost 
gradient boosting model.

---

## Pipeline


<img width="1280" height="720" alt="pipeline-overview" src="https://github.com/user-attachments/assets/8776a5e6-cf81-449d-b8cd-105285fdb6a0" />

The pipeline consists of the following stages:

1. **Reference genome curation** — 306 soil-associated bacterial species from NCBI RefSeq
2. **Genome fragmentation** — simulating short-read sequencing
3. **Canonical k-mer extraction** — 2,080-dimensional feature vectors
4. **Label encoding** — bijective species-to-integer mapping
5. **Model training** — XGBoost classifier on 93.8M fragments
6. **Internal evaluation** — held-out test set of 52.4M fragments
7. **External validation** — CAMISIM-simulated metagenomic communities

---

## Results

| Metric | Held-out Test Set | CAMISIM Validation |
|--------|-------------------|--------------------|
| Macro AUC | 0.96 | 0.986 – 0.999 |
| Macro AUPRC | 0.91 | — |
| Overall Accuracy | — | 86.9% |
| Training Fragments | 93,822,292 | — |
| Test Fragments | 52,376,010 | — |
| Species Covered | 306 | 10 |

---

## Repository Structure

Soil-Metagenome-Classifier/
│
├── README.md
├── LICENSE
├── .gitignore
├── species_list.txt              List of 306 reference species
│
├── dataset/                      Reference genome data and accessions
├── fragments/                    Genome fragmentation scripts and statistics
├── kmers/                        Canonical k-mer extraction pipeline
├── label_encoding/               Species-to-integer label mapping
├── model_train/                  XGBoost training scripts and trained model
├── CAMISIM-validation/           External validation using CAMISIM simulations
└── cami_results/                 Validation results, figures, and metrics


Each subdirectory contains its own README describing the inputs, outputs, 
and scripts for that stage of the pipeline.

---

## Methodology

### Data

Reference genomes for **306 soil-associated bacterial species** were 
retrieved from the NCBI RefSeq database. The full species list is 
available in `species_list.txt`.

### Feature Representation

Each DNA fragment is encoded as a normalised **2,080-dimensional canonical 
6-mer frequency vector**. Canonical k-mers reduce the feature space from 
4⁶ = 4,096 possible 6-mers to 2,080 by collapsing reverse complements, 
exploiting DNA strand symmetry.

### Model

An **XGBoost gradient boosting classifier** was selected for its scalability, 
implicit feature selection, and demonstrated performance on high-dimensional 
sparse data. Hyperparameters were tuned via grid search with early stopping. 
Training was parallelised across 32 cores on a high-performance computing 
cluster.

### Validation

- **Internal:** held-out test set of 52.4M fragments from disjoint genomes
- **External:** CAMISIM-simulated metagenomic communities across 10 species

---

## Requirements

- Python 3.8 or higher
- XGBoost
- scikit-learn
- NumPy, SciPy, pandas
- BioPython
- Matplotlib, seaborn

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

The pipeline is organised as sequential stages. Run them in order:

```bash
# 1. Fragment reference genomes
cd fragments && python fragment_train.py && python fragment_test.py

# 2. Extract canonical k-mers
cd ../kmers && python kmerize.py

# 3. Encode species labels
cd ../label_encoding && python label_encoder.py

# 4. Train the model
cd ../model_train && python train_xgboost.py

# 5. Validate on CAMISIM simulations
cd ../CAMISIM-validation && bash run_camisim.sh
```

Refer to the README inside each directory for stage-specific details.

---



---

## Author

**Taiba Shamim**  
M.Sc. Bioinformatics  
Department of Computer Science, Jamia Millia Islamia

**Supervisor**  
Dr. Gitanjali Yadav, Staff Scientist VI  
Biodiversity Informatics Laboratory  
National Institute of Plant Genome Research (NIPGR)

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
