# EVDx Data Dictionary

This document describes the structure and schema of the harmonized databases located in `analysis_results/`.

## 1. File Formats
All data is provided in **CSV (Comma Separated Values)** format for maximum compatibility.
*   **Missing Values:** Represented as empty cells (sparse data).
*   **Compression:** Files may be gzipped (`.csv.gz`) for storage, but current versions are uncompressed.

---

## 2. Proteomics Database
**Location:** `analysis_results/proteomics/merged_protein_matrix_log2.csv`

### Matrix Structure
*   **Rows (Index):** **Gene Symbols** (e.g., `ALB`, `RBP4`, `CD9`).
    *   *Source:* Extracted from MaxQuant `Gene names` column.
    *   *Fallback:* If Gene Name is missing, the Uniprot ID is used.
*   **Columns:** **Global Sample IDs** (e.g., `PXD068982_Control_01`).
*   **Values:** **Log2 LFQ Intensity** (`log2(x + 1)`).
    *   LFQ (Label-Free Quantification) is a normalized intensity value from MaxQuant.

### Metadata
**Location:** `analysis_results/proteomics/merged_metadata.csv`

| Column | Description | Example |
| :--- | :--- | :--- |
| `Global_ID` | Unique Primary Key. Format: `{Accession}_{OriginalID}` | `PXD068982_Control_01` |
| `Accession` | Source Study ID (PRIDE). | `PXD068982` |
| `Original_Sample_ID` | The raw column name from the source file. | `Control_01` |
| `Condition` | Inferred Label (Case/Control) from sample name. | `Healthy Control` |
| `Refined_Condition` | **Final Clinical Label** derived from PubMed. | `Ovarian Cancer` |
| `Proteins_Detected` | Quality metric: Number of non-zero proteins. | `450` |
| `Batch` | Batch identifier (usually same as Accession). | `PXD068982` |

---

## 3. miRNA Database
**Location:** `analysis_results/mirna/merged_mirna_matrix_log2.csv`

### Matrix Structure
*   **Rows (Index):** **Standardized miRNA IDs** (e.g., `hsa-mir-let-7a-5p`).
    *   *Harmonization:* All IDs are lowercased, prefixes standardized to `hsa-mir-`, and sequence/pipe annotations stripped.
*   **Columns:** **Global Sample IDs** (e.g., `GSE269779_Sample_1`).
*   **Values:** **Log2 Count** (`log2(x + 1)`).
    *   Source values are raw read counts or RPM (Reads Per Million), log-transformed.

### Metadata
**Location:** `analysis_results/mirna/merged_mirna_metadata.csv`

| Column | Description | Example |
| :--- | :--- | :--- |
| `Global_ID` | Unique Primary Key. | `GSE269779_Sample_1` |
| `Accession` | Source Study ID (GEO Series). | `GSE269779` |
| `Condition` | Inferred Label (Case/Control). | `Parkinson's Disease` |
| `Biofluid` | Sample source. | `Serum/Plasma (inferred)` |
| `Refined_Condition` | **Final Clinical Label**. | `Parkinson's Disease` |

---

## 4. Data nuances
*   **Sparsity:** The matrices are sparse (contain `NaN`). This is expected as not all studies measure the same features.
*   **Batch Effects:** Distinct clusters may exist corresponding to `Accession` IDs. **Batch correction is required before training.**
*   **"Junk" Features:** Some miRNA rows may look like `hsa-mir-12128`. These are valid features from specific array platforms but may not map to canonical miRBase IDs. We retained them to preserve information.
