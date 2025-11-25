# EVDx Project Overview

**Phase:** 2 - Data Aggregation & Harmonization (Complete)
**Date:** November 2025

## 1. Mission Statement
EVDx aims to revolutionize disease diagnosis by leveraging the latent information within Extracellular Vesicles (EVs) found in human blood. By aggregating heterogeneous omics data from dozens of independent studies into a unified, machine-learning-ready database, we seek to identify robust, universal biomarkers that transcend specific laboratory conditions.

## 2. The Challenge
EV research is highly fragmented. Thousands of studies exist, but they use different:
*   **Isolation Methods:** Ultracentrifugation, Kits, SEC.
*   **Profiling Platforms:** Mass Spectrometry (Proteomics), RNA-seq (miRNA).
*   **Data Formats:** Raw outputs, processed tables, supplementary Excel sheets.
*   **Nomenclature:** `hsa-miR-21` vs `miR-21-5p`; `Uniprot ID` vs `Gene Name`.

Previous attempts to manually curate datasets were slow and resulted in small, disconnected cohorts.

## 3. The Solution: The "Wide Net" Strategy
Instead of manual curation, EVDx employs an **Automated Aggregation Pipeline** that prioritizes **technical consistency** over manual inspection.

### Core Principles
1.  **Strict Quality Filters:** We only accept data that meets "Gold Standard" criteria:
    *   **Human Blood** (Plasma/Serum) only.
    *   **Standardized Software Outputs** (MaxQuant for Proteins, Count Matrices for miRNA).
2.  **Automated Scouting:** Custom scripts scan public repositories (PRIDE, GEO) for compatible datasets.
3.  **Metadata Inference:** We use NLP on PubMed abstracts to "reverse engineer" clinical labels (e.g., mapping "Case" to "Ovarian Cancer").
4.  **Harmonization:** We force all data into a single, unified matrix structure.

## 4. Current Status (Phase 2 Complete)
We have successfully built the largest known open-source harmonized EV database:

| Modality | Studies | Samples | Features | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Proteomics** | 14 | 258 | 4,469 | **Ready** |
| **miRNA** | 20+ | 1,455 | 7,480 | **Ready** |

### Key Disease Cohorts
*   **Neurodegenerative:** Parkinson's Disease, Alzheimer's Disease (with Controls), ALS.
*   **Oncology:** Ovarian, Lung, Pancreatic, Liver, and Gastric Cancers.
*   **Infectious:** COVID-19 (with Controls), Sepsis.
*   **Inflammatory:** Rheumatoid Arthritis.

*Note: Ovarian Cancer cohort (PXD068982) currently requires manual label verification.*

## 5. Repository Contents
*   **`analysis_results/`**: The final merged databases (CSV/Parquet).
*   **`scripts/`**: The complete automation pipeline.
*   **`candidate_papers_final.csv`**: Traceability logs linking every sample to its source publication.

## 6. Next Phase: Machine Learning
With the database built, Phase 3 focuses on:
1.  **Batch Effect Correction:** Using ComBat to remove study-specific technical variation.
2.  **Multi-Modal Integration:** Combining Protein and miRNA signals.
3.  **Diagnostic Classifiers:** Training Random Forest/XGBoost models to predict disease status across studies.