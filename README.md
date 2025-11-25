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
*   **Total Features:** 7,480 miRNA entries (Cleaned & Harmonized).
*   **Key Cohorts:**
    *   **Parkinson's Disease:** 222 samples
    *   **Cancer (Mixed):** 272 samples
*   **File:** `analysis_results/mirna/merged_mirna_matrix_log2.csv`

---

## 3. Methodology & Pipeline

We pivoted from manual curation to an **automated "Wide Net" strategy** to maximize data volume while ensuring technical consistency.

### Step 1: Automated Scouting (Paper Selection)
Instead of reading papers manually, we built API scouts to filter repositories based on strict metadata criteria.

*   **Proteomics (PRIDE Database):**
    *   **Script:** `scripts/01_pride_scout.py`
    *   **Filters:**
        1.  **Keywords:** "exosome", "extracellular vesicle", "plasma", "serum".
        2.  **Software:** Must be processed with **MaxQuant** (to ensure `proteinGroups.txt` output structure).
        3.  **Species:** *Homo sapiens*.
        4.  **File Availability:** Must have processed results accessible (txt/xlsx/csv).
*   **miRNA (GEO Database):**
    *   **Script:** `scripts/05_geo_scout.py`
    *   **Filters:**
        1.  **Query:** `("plasma" OR "serum") AND ("exosome" OR "EV") AND ("miRNA" OR "non-coding")`.
        2.  **Sample Size:** > 10 samples (to allow for ML splitting).
        3.  **Data Type:** Must have a "Supplementary File" containing count matrices (`_counts.txt`, `_matrix.csv`).

### Step 2: Deep Metadata Enrichment
Repository metadata is often incomplete. We implemented a multi-stage inference engine to assign clinical labels.

*   **Scripts:** `scripts/06_enrich_geo_metadata.py`, `scripts/07_enrich_pride_metadata.py`, `scripts/11_fetch_pubmed_abstracts.py`
*   **Logic:**
    1.  **API Fetch:** Pull detailed sample attributes from GEO/PRIDE APIs.
    2.  **Literature Mining:** Scrape **PubMed Abstracts** for the linked papers to extract specific disease cohorts (e.g., "Triple-Negative Breast Cancer" vs just "Cancer").
    3.  **Keyword Mapping:** Map text descriptions to standardized labels (e.g., "HCC" -> "Liver Cancer").

### Step 3: Data Acquisition
*   **Scripts:** `scripts/02_download_pride_data.py`, `scripts/08_download_geo_data.py`
*   **Process:** Automatically locates and downloads the specific result files (skipping Terabytes of raw MS/Sequencing data).
*   **Validation:** Checks for valid file formats (`.txt`, `.csv`, `.xlsx`) and standard headers.

### Step 4: Harmonization & Cleaning
This was the most critical step to enable cross-study analysis.

*   **Proteomics (`scripts/09_normalize_proteins.py`):**
    *   **Extraction:** Pulls `LFQ intensity` columns from `proteinGroups.txt`.
    *   **Mapping:** Uses `Gene names` as the universal index. Fallback to `Majority protein IDs` if missing.
    *   **Normalization:** Log2 transformation (`log2(x+1)`).
    *   **Traceability:** Assigns a Global ID: `{Accession}_{OriginalSampleName}`.

*   **miRNA (`scripts/10_normalize_mirna.py`):**
    *   **ID Cleaning:** The biggest challenge was inconsistent naming (`hsa-let-7a` vs `Let-7a-5p` vs `hsa-mir-let-7a`).
    *   **Harmonization Logic:**
        1.  Lowercase everything.
        2.  Strip prefixes (`hsa-`, `mir-`, `miR-`) and re-apply standard `hsa-mir-`.
        3.  **Pipe-ID Extraction:** For IDs like `sequence|name|annotation`, we extract the canonical name (e.g., `let-7i`) and discard the sequence.
        4.  **Filter Noise:** Removed rows corresponding to GO Terms, KEGG pathways, or non-miRNA features.
    *   **Aggregation:** Summed counts for duplicate IDs (e.g., isomiRs mapping to the same canonical name).

---

## 4. Reproduction Guide

To reproduce the entire database from scratch, follow these steps:

### 1. Environment Setup
```bash
# Install dependencies
pip install pandas numpy requests beautifulsoup4 openpyxl lxml html5lib fastparquet pyarrow
```

### 2. Scout for Datasets
Generate the list of candidate papers.
```bash
# Find Proteomics papers
python3 scripts/01_pride_scout.py

# Find miRNA papers
python3 scripts/05_geo_scout.py
```

### 3. Enrich Metadata (Labeling)
Fetch PubMed abstracts and infer disease labels.
```bash
# Get deep metadata from APIs
python3 scripts/06_enrich_geo_metadata.py
python3 scripts/07_enrich_pride_metadata.py

# Scrape PubMed for better diagnosis labels
python3 scripts/11_fetch_pubmed_abstracts.py
```

### 4. Download Data
Download the count matrices and protein groups (approx. 1GB total).
*Note: Data goes into `raw_data/`, which is gitignored.*
```bash
python3 scripts/02_download_pride_data.py
python3 scripts/08_download_geo_data.py
```

### 5. Process & Normalize
Generate the final merged matrices in `analysis_results/`.
```bash
# Process Proteins
python3 scripts/09_normalize_proteins.py

# Process miRNAs (includes ID harmonization)
python3 scripts/10_normalize_mirna.py

# Sync final clinical labels to the merged metadata
python3 scripts/12_sync_labels.py
```

### 6. Output
You will find the final ML-ready files in:
*   `analysis_results/proteomics/merged_protein_matrix_log2.csv`
*   `analysis_results/mirna/merged_mirna_matrix_log2.csv`

---

## 5. Repository Structure
```
EVDx/
├── analysis_results/       # FINAL DATABASE
│   ├── proteomics/
│   │   ├── merged_protein_matrix_log2.csv  # The Main Protein Data (CSV)
│   │   └── merged_metadata.csv             # Clinical Labels
│   └── mirna/
│       ├── merged_mirna_matrix_log2.csv    # The Main miRNA Data (CSV)
│       └── merged_mirna_metadata.csv       # Clinical Labels
├── scripts/                # Automation Pipeline
│   ├── 01_pride_scout.py              # Step 1: Scout Proteomics (PRIDE)
│   ├── 02_download_pride_data.py      # Step 4: Download Proteomics Data
│   ├── 05_geo_scout.py                # Step 1: Scout miRNA (GEO)
│   ├── 06_enrich_geo_metadata.py      # Step 2: Fetch GEO Metadata (Deep)
│   ├── 07_enrich_pride_metadata.py    # Step 2: Fetch PRIDE Metadata (Deep)
│   ├── 08_download_geo_data.py        # Step 4: Download miRNA Data
│   ├── 09_normalize_proteins.py       # Step 5: Process & Normalize Proteins
│   ├── 10_normalize_mirna.py          # Step 5: Process & Normalize miRNA
│   ├── 11_fetch_pubmed_abstracts.py   # Step 3: Scrape PubMed for Disease Labels
│   ├── 12_sync_labels.py              # Step 6: Sync Refined Labels to Metadata
│   └── generate_candidate_list.py     # Helper: Filter scouts for review
├── candidate_papers_final.csv      # Master list of Proteomics sources
├── geo_mirna_candidates_final.csv  # Master list of miRNA sources
└── raw_data/               # Source files (Gitignored)
```