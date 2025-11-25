# miRNA Data Collection Strategy

To match the quality and standardization of our Proteomics strategy (MaxQuant), we will target specific standardized outputs for miRNA sequencing.

## 1. The "ProteinGroups.txt" Equivalent

For miRNA-seq, there is no single software as dominant as MaxQuant. However, the **Output Data Structure** is highly standardized. We are looking for **Count Matrices**.

**Target File Types:**
1.  **`raw_counts.csv` / `counts.txt`:** Raw read counts mapped to miRNAs. (Preferred for `DESeq2` normalization).
2.  **`RPM.txt` / `CPM.txt`:** Reads/Counts Per Million (Pre-normalized).
3.  **`miRge` Output:** Files named `miR.Counts.csv`.

## 2. Search Strategy (GEO & SRA)

We will scout the **Gene Expression Omnibus (GEO)** using their API.

**Search Query:**
`((("plasma"[Sample Source] OR "serum"[Sample Source]) AND ("exosome"[Description] OR "extracellular vesicle"[Description])) AND "non coding rna profiling by high throughput sequencing"[DataSet Type])`

**Filtering Criteria:**
1.  **Sample Source:** Must be human Plasma or Serum.
2.  **Data Availability:** Must have a Supplementary File containing "count", "matrix", "table", or "abundance".
3.  **Sample Size:** > 20 samples preferred (to allow for ML splitting).

## 3. Data Processing Pipeline

Unlike Proteomics (where we use pre-processed `proteinGroups.txt`), miRNA data might need one normalization step if we mix Raw Counts and RPM.

**Proposed Pipeline:**
1.  **Download:** Fetch the `counts.csv` or `counts.txt.gz` from GEO.
2.  **Check:** Verify rows are miRNA IDs (e.g., `hsa-miR-21-5p`).
3.  **Normalize:** If Raw Counts → Apply TMM (Trimmed Mean of M-values) or DESeq2 size factor normalization to create a unified scale.
4.  **Harmonize:** Map all miRNA names to the latest miRBase version (v22) to ensure `hsa-miR-21` and `miR-21-5p` match.
