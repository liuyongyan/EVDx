# Quick Reference

**Last Updated**: November 22, 2025

Code examples for loading and exploring EVDx datasets.

---

## Setup

### Requirements
```bash
pip install pandas openpyxl
```

### Clone and Download Data
```bash
git clone https://github.com/[username]/EVDx.git
cd EVDx
./scripts/download_large_files.sh  # Downloads 3.3 GB
```

---

## 1. Hoshino 2020 - Clinical Proteomics

### Load Data
```python
import pandas as pd

# Load human samples (512 samples × 9,938 proteins)
hoshino = pd.read_excel(
    'hoshino2020_data/Human512Reports.xlsx',
    header=None
)

# Extract metadata (rows 0-2) and data (rows 3+)
sample_sources = hoshino.iloc[0, :]    # Source type
sample_names = hoshino.iloc[2, :]      # Sample names
proteins = hoshino.iloc[3:, 0]         # Protein names
data_matrix = hoshino.iloc[3:, 1:]     # Intensity values
```

### Parse Disease Labels
```python
# Disease info is in filenames (column names)
def parse_disease(filename):
    # Example: "Pancreas_Cancer_01" → "Pancreatic cancer"
    parts = filename.lower().split('_')
    # Custom parsing logic needed
    return disease_type

diseases = [parse_disease(name) for name in sample_names]
```

### Basic Exploration
```python
# Check dimensions
print(f"Samples: {data_matrix.shape[1]}")
print(f"Proteins: {data_matrix.shape[0]}")

# Missing rate
missing = (data_matrix == 0).sum().sum() / data_matrix.size
print(f"Missing rate: {missing:.1%}")
```

---

## 2. Kugeratski 2021 - Cell Line Proteomics

### Load Quantitative Data
```python
# Load SILAC ratios (1,243 proteins × 42 samples)
kugeratski = pd.read_excel(
    'kugeratski2021_data/Source Quantitative.xlsx',
    sheet_name='Supplementary Table 2',
    header=None
)

# Skip header rows, get protein data
# Columns: Protein info, then 3 replicates per cell line
```

### Cell Lines
```python
cell_lines = [
    'BJ', 'BxPC3', 'HEK293T', 'HPDE', 'HPNE', 'Jurkat', 'mCAF',
    'MCF10A', 'MCF7', 'MDA-MB-231', 'PANC1', 'PSC', 'Raji', 'THP1'
]
```

### Universal Markers
```python
# Key markers for normalization
universal_markers = [
    'SDCBP',    # Syntenin-1 (most abundant)
    'PDCD6IP', # ALIX
    'TSG101',
    'CD9', 'CD63', 'CD81'
]
```

---

## 3. EVmiRNA2.0 - miRNA Database

### Load Single Project
```python
project_id = 'PRJDB2585'  # Example project

# Metadata
metadata = pd.read_csv(f'evmirna_data/{project_id}_metadata.csv')

# Expression (TPM normalized)
expression = pd.read_csv(
    f'evmirna_data/{project_id}_expression.csv',
    index_col=0
)

# Raw counts (if available - 344/371 projects have this)
counts = pd.read_csv(
    f'evmirna_data/{project_id}_expression_count.csv',
    index_col=0
)
```

### Get All Project IDs
```python
import os
import re

# Extract unique project IDs from filenames
files = os.listdir('evmirna_data')
project_ids = sorted(set(
    re.match(r'(PRJ\w+)_', f).group(1)
    for f in files if f.startswith('PRJ')
))

print(f"Total projects: {len(project_ids)}")  # 371
```

### Explore All Projects
```python
for project_id in project_ids:
    # Check available files
    has_counts = os.path.exists(
        f'evmirna_data/{project_id}_expression_count.csv'
    )

    # Load metadata for disease info
    meta = pd.read_csv(f'evmirna_data/{project_id}_metadata.csv')
    # Disease labels in metadata columns
```

---

## 4. Vesiclepedia - Reference Database

### Load Protein Data
```python
# Protein/mRNA entries
proteins = pd.read_csv(
    'vesiclepedia_data/VESICLEPEDIA_PROTEIN_MRNA_DATA_2024_10_13.txt',
    sep='\t'
)

# Columns: VESICLE_ID, GENE_SYMBOL, ENTREZ_GENE_ID,
#          GENE_NAMES, CONTENT_TYPE, GO_ANNOTATIONS, etc.
```

### Load miRNA Data
```python
mirnas = pd.read_csv(
    'vesiclepedia_data/VESICLEPEDIA_MIRNA_DATA_2024_10_13.txt',
    sep='\t'
)
```

### Load Experiment Metadata
```python
experiments = pd.read_csv(
    'vesiclepedia_data/VESICLEPEDIA_EXPERIMENT_2024_10_13.txt',
    sep='\t'
)

# Get experiment details: species, sample type, isolation method
```

### Query by Gene
```python
def get_vesicle_experiments(gene_symbol):
    """Find all experiments detecting a gene"""
    matches = proteins[proteins['GENE_SYMBOL'] == gene_symbol]
    return matches['VESICLE_ID'].unique()

# Example: Find experiments with Syntenin-1
expts = get_vesicle_experiments('SDCBP')
print(f"Syntenin-1 found in {len(expts)} experiments")
```

---

## 5. Cross-Dataset Analysis

### Map Proteins Between Datasets
```python
# Get proteins from both datasets
hoshino_proteins = set(hoshino.iloc[3:, 0].dropna())
kugeratski_proteins = set(kugeratski['gene_name'].dropna())

# Find overlap
overlap = hoshino_proteins & kugeratski_proteins
print(f"Overlapping proteins: {len(overlap)}")
```

### Normalize Using Universal Markers
```python
def normalize_by_syntenin(data, protein_col):
    """Normalize protein intensities by Syntenin-1"""
    syntenin_idx = data[protein_col] == 'SDCBP'
    syntenin_values = data.loc[syntenin_idx].iloc[0, 1:]

    # Divide all values by Syntenin-1
    normalized = data.iloc[:, 1:].div(syntenin_values)
    return normalized
```

---

## R Examples

### Load Hoshino Data
```r
library(readxl)

hoshino <- read_excel(
    "hoshino2020_data/Human512Reports.xlsx",
    col_names = FALSE
)

# Extract components
sample_sources <- hoshino[1, ]
sample_names <- hoshino[3, ]
proteins <- hoshino[4:nrow(hoshino), 1]
data_matrix <- hoshino[4:nrow(hoshino), 2:ncol(hoshino)]
```

### Load EVmiRNA Project
```r
# Load single project
project_id <- "PRJDB2585"

metadata <- read.csv(sprintf("evmirna_data/%s_metadata.csv", project_id))
expression <- read.csv(
    sprintf("evmirna_data/%s_expression.csv", project_id),
    row.names = 1
)
counts <- read.csv(
    sprintf("evmirna_data/%s_expression_count.csv", project_id),
    row.names = 1
)
```

---

## File Locations Summary

| Dataset | Main Files | Path |
|---------|------------|------|
| Hoshino | Human512Reports.xlsx | `hoshino2020_data/` |
| Kugeratski | Source Quantitative.xlsx | `kugeratski2021_data/` |
| EVmiRNA | {PROJECT_ID}_*.csv (1,086 files) | `evmirna_data/` |
| Vesiclepedia | *_DATA_*.txt | `vesiclepedia_data/` |

---

## Troubleshooting

### Large Files Missing
```bash
# Run download script
./scripts/download_large_files.sh
```

### Excel Loading Errors
```python
# Install openpyxl
pip install openpyxl

# Specify engine
pd.read_excel('file.xlsx', engine='openpyxl')
```

### Memory Issues
```python
# Load subset of rows
df = pd.read_excel('file.xlsx', nrows=1000)

# Load specific columns
df = pd.read_excel('file.xlsx', usecols='A:D')
```
