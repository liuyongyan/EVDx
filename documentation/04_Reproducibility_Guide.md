# Reproducibility Guide

Follow these steps to rebuild the EVDx database from scratch using the provided scripts.

## Prerequisites
*   Python 3.8+
*   Internet connection (for API access and downloads)
*   ~2 GB of Disk Space (cleaned) / ~5 GB (during processing)

## Installation
Install the required Python packages:
```bash
pip install pandas numpy requests beautifulsoup4 openpyxl lxml html5lib fastparquet pyarrow
```

---

## Step-by-Step Reproduction

### 1. Scout for Datasets
Generate the initial candidate lists from PRIDE and GEO.
```bash
python3 scripts/01_pride_scout.py  # Generates pride_scout_results.csv
python3 scripts/05_geo_scout.py    # Generates geo_mirna_candidates.csv
```

### 2. Generate Review Lists
Filter raw scout results for high-quality candidates (Blood + Results available).
```bash
python3 scripts/generate_candidate_list.py
```

### 3. Enrich Metadata
Fetch detailed metadata and PubMed abstracts to infer disease labels.
```bash
# Fetch API metadata
python3 scripts/06_enrich_geo_metadata.py
python3 scripts/07_enrich_pride_metadata.py

# Fetch Abstracts & Infer Diseases
python3 scripts/11_fetch_pubmed_abstracts.py
```

### 4. Download Data
Download the actual data matrices. Files will be saved to `raw_data/` (ignored by git).
```bash
python3 scripts/02_download_pride_data.py
python3 scripts/08_download_geo_data.py
```

### 5. Process & Normalize
Clean the data and generate the final merged matrices.
```bash
# Create Protein Matrix
python3 scripts/09_normalize_proteins.py

# Create miRNA Matrix
python3 scripts/10_normalize_mirna.py
```

### 6. Final Sync
Apply the refined disease labels to the final metadata files.
```bash
python3 scripts/12_sync_labels.py
```

---

## Outputs
The final database will be generated in `analysis_results/`:

*   **Proteomics:**
    *   `analysis_results/proteomics/merged_protein_matrix_log2.csv`
    *   `analysis_results/proteomics/merged_metadata.csv`
*   **miRNA:**
    *   `analysis_results/mirna/merged_mirna_matrix_log2.csv`
    *   `analysis_results/mirna/merged_mirna_metadata.csv`
