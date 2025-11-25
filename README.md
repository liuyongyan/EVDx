# EVDx: AI-Powered Disease Diagnosis from Extracellular Vesicles (Phase 2)

**Status:** Data Collection & Harmonization Complete. Ready for Analysis.

## 1. Objective
To develop a diagnostic machine learning model using a massive, aggregated database of Extracellular Vesicle (EV) omics data from human blood.

## 2. The "Wide Net" Database
We have successfully aggregated and harmonized data from over **50 studies** using strict quality filters (Human Blood only, Standardized Pipelines).

### A. Proteomics Database
*   **Source:** PRIDE (MaxQuant processed).
*   **Total Samples:** 258
*   **Total Features:** 4,469 Proteins
*   **Key Cohorts:**
    *   **Ovarian Cancer:** 121 samples
    *   **COVID-19:** 60 samples
    *   **Alzheimer's Disease:** 57 samples
    *   **Lung Cancer:** 9 samples
    *   **ALS:** 11 samples
*   **File:** `analysis_results/proteomics/merged_protein_matrix_log2.csv`

### B. miRNA Database
*   **Source:** GEO (RNA-seq Counts).
*   **Total Samples:** 1,455
*   **Total Features:** 56,359 miRNA entries
*   **Key Cohorts:**
    *   **Parkinson's Disease:** 222 samples
    *   **Cancer (Mixed):** 272 samples
*   **File:** `analysis_results/mirna/merged_mirna_matrix_log2.csv`

## 3. Methodology

### Automated Scouting
We replaced manual literature search with automated API scouts:
*   **Proteomics Scout (`scripts/01_pride_scout.py`):** Targeted datasets with `proteinGroups.txt` or result tables.
*   **miRNA Scout (`scripts/05_geo_scout.py`):** Targeted datasets with `raw_counts` or `matrix` files.

### Deep Metadata Enrichment
To resolve missing labels (e.g., "Cancer vs Healthy"), we implemented a multi-stage inference pipeline:
1.  **Repository Metadata:** Parsed PRIDE/GEO descriptions.
2.  **Literature Mining:** Scraped PubMed Abstracts (`scripts/11_fetch_pubmed_abstracts.py`) to identify specific disease cohorts (e.g., "Triple-Negative Breast Cancer" instead of just "Cancer").
3.  **File Header Inspection:** Inferred "Control" vs "Case" based on sample naming conventions (`Ctrl_01`, `Cancer_03`).

### Normalization & Traceability
*   **Global ID:** Every sample is assigned a unique ID: `{Accession}_{OriginalName}` (e.g., `PXD024216_EV1`).
*   **Batch Tracking:** The `Batch` column in metadata allows for "Leave-One-Study-Out" validation to prevent overfitting to specific lab conditions.
*   **Quantification:**
    *   Proteins: Log2 LFQ Intensity.
    *   miRNA: Log2 Counts (aggregated by ID).

## 4. Next Steps: Machine Learning
With the database built, we will now proceed to:
1.  **Exploratory Data Analysis (EDA):** Visualize batch effects using PCA/t-SNE.
2.  **Batch Correction:** Apply ComBat or similar methods to remove lab-specific variation.
3.  **Classifier Training:** Train Random Forest / XGBoost models to predict disease status.
4.  **Biomarker Discovery:** Identify universal markers that persist across different studies.

## 5. Repository Structure
```
EVDx/
├── analysis_results/       # FINAL DATABASE
│   ├── proteomics/
│   │   ├── merged_protein_matrix_log2.csv  # The Main Protein Data
│   │   └── merged_metadata.csv             # Clinical Labels
│   └── mirna/
│       ├── merged_mirna_matrix_log2.csv    # The Main miRNA Data
│       └── merged_mirna_metadata.csv       # Clinical Labels
├── candidate_papers_final.csv      # Master list of Proteomics sources
├── geo_mirna_candidates_final.csv  # Master list of miRNA sources
├── scripts/                # All automation scripts
│   ├── 01_pride_scout.py
│   ├── 09_normalize_proteins.py
│   ├── 10_normalize_mirna.py
│   └── ...
└── raw_data/               # Source files (Gitignored mostly)
```
