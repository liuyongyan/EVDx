# Unified Metadata Schema

To enable large-scale machine learning across heterogeneous datasets, all samples will be mapped to this unified schema.

## 1. Schema Definition

| Column Name | Description | Example |
| :--- | :--- | :--- |
| **Global_ID** | Unique ID across the entire EVDx database. Format: `{Accession}_{SampleID}` | `PXD024216_EV1` |
| **Dataset_Accession** | The source repository ID. | `PXD024216` |
| **Sample_ID** | The original sample name in the source file. | `EV1` |
| **Biofluid** | The specific blood fraction used. | `Plasma`, `Serum` |
| **Platform** | The molecular type and quantification method. | `Proteomics_MaxQuant`, `miRNA_Seq_Counts` |
| **Original_Label** | The raw label from the paper's metadata. | `AD_Patient`, `Control_group`, `HCC_early` |
| **Standardized_Label** | The harmonized disease name (Case) or Control. | `Alzheimer's Disease`, `Healthy Control` |
| **Disease_Category** | High-level grouping for multi-class tasks. | `Neurodegenerative`, `Cancer`, `Infectious`, `Control` |
| **Cohort** | (Optional) Specific sub-cohort within the study. | `Discovery`, `Validation` |

## 2. Standardization Rules

### Disease Labeling
*   **Healthy Control:** Any sample from a healthy donor. Standardized to `Healthy Control`.
*   **Disease Names:** Use the specific disease name (e.g., `Ovarian Cancer`, `Alzheimer's Disease`).
*   **Mappings (Example):**
    *   `HCC`, `Hepatocellular Carcinoma`, `Liver Cancer` → **`Liver Cancer`**
    *   `AD`, `Alzheimer's` → **`Alzheimer's Disease`**
    *   `Normal`, `Healthy`, `Control` → **`Healthy Control`**

### Biofluid
*   Must be `Plasma` or `Serum`. Samples labeled "Blood" should be investigated to specify which fraction.

## 3. Implementation Strategy
A master `metadata_map.csv` will be maintained. This file acts as a lookup table for the "Reverse Engineering" process for each dataset.

```csv
Dataset_Accession, Sample_Pattern_Regex, Inferred_Label, Biofluid
PXD024216,         EV[0-9]+,             (Requires ML inference), Plasma
PXD068982,         Control_.*,           Healthy Control,         Plasma
PXD068982,         Cancer_.*,            Ovarian Cancer,          Plasma
```
