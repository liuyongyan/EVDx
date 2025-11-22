# Quick Start Guide - EV miRNA Database

## What You Have

### ✅ Complete Datasets (182 MB total)

1. **EVmiRNA2.0** - 104 MB, 1,086 files
   - 371 projects with miRNA expression data
   - Location: `evmirna_data/`

2. **Vesiclepedia** - 78 MB, 8 files
   - 3,481 studies with proteins, RNA, and lipids
   - Location: `vesiclepedia_data/`

---

## Data Locations

### EVmiRNA2.0 Files
```
evmirna_data/
├── {PROJECT_ID}_metadata.csv        (371 files) - Sample info
├── {PROJECT_ID}_expression.csv      (371 files) - TPM values
└── {PROJECT_ID}_expression_count.csv (344 files) - Raw counts
```

### Vesiclepedia Files
```
vesiclepedia_data/
├── Vesiclepedia_experiment_details.txt    (3,481 studies)
├── Vesiclepedia_protein_mRNA_details.txt  (566,911 proteins)
├── Vesiclepedia_miRNA_details.txt         (22,858 miRNAs)
├── Vesiclepedia_gene_details.txt          (46,687 genes)
├── Vesiclepedia_lipid_details.txt         (3,839 lipids)
├── Vesiclepedia_PTM_details.txt           (PTMs)
├── Vesiclepedia_Proteins_GPAD.txt         (GO annotations)
└── Vesiclepedia_RNAs_GPAD.txt             (GO annotations)
```

---

## Quick Data Loading

### Python

```python
import pandas as pd

# EVmiRNA2.0
metadata = pd.read_csv('evmirna_data/PRJDB2585_metadata.csv')
expression = pd.read_csv('evmirna_data/PRJDB2585_expression.csv')
counts = pd.read_csv('evmirna_data/PRJDB2585_expression_count.csv')

# Vesiclepedia
experiments = pd.read_csv('vesiclepedia_data/Vesiclepedia_experiment_details.txt', sep='\t')
mirnas = pd.read_csv('vesiclepedia_data/Vesiclepedia_miRNA_details.txt', sep='\t')
proteins = pd.read_csv('vesiclepedia_data/Vesiclepedia_protein_mRNA_details.txt', sep='\t')
lipids = pd.read_csv('vesiclepedia_data/Vesiclepedia_lipid_details.txt', sep='\t')
```

### R

```r
# EVmiRNA2.0
metadata <- read.csv('evmirna_data/PRJDB2585_metadata.csv')
expression <- read.csv('evmirna_data/PRJDB2585_expression.csv')
counts <- read.csv('evmirna_data/PRJDB2585_expression_count.csv')

# Vesiclepedia
experiments <- read.delim('vesiclepedia_data/Vesiclepedia_experiment_details.txt')
mirnas <- read.delim('vesiclepedia_data/Vesiclepedia_miRNA_details.txt')
proteins <- read.delim('vesiclepedia_data/Vesiclepedia_protein_mRNA_details.txt')
lipids <- read.delim('vesiclepedia_data/Vesiclepedia_lipid_details.txt')
```

---

## Common Tasks

### 1. List All Projects

```bash
ls evmirna_data/*_metadata.csv | sed 's/_metadata.csv//' | sed 's/.*\///'
```

### 2. Find Projects with Raw Counts

```bash
ls evmirna_data/*_expression_count.csv | sed 's/_expression_count.csv//' | sed 's/.*\///'
```

### 3. Count Total Samples

```bash
# EVmiRNA2.0
wc -l evmirna_data/*_metadata.csv | tail -1

# Vesiclepedia
wc -l vesiclepedia_data/Vesiclepedia_experiment_details.txt
```

### 4. Search for Specific miRNA

```bash
# EVmiRNA2.0
grep "hsa-miR-21" evmirna_data/*_expression.csv

# Vesiclepedia
grep "miR-21" vesiclepedia_data/Vesiclepedia_miRNA_details.txt
```

### 5. Find Human Studies

```bash
grep "Homo sapiens" vesiclepedia_data/Vesiclepedia_experiment_details.txt
```

---

## Data Coverage

### EVmiRNA2.0
- **371 projects** from 2015-2023
- **100% have**: Metadata + Expression (TPM)
- **93% have**: Raw counts
- **Format**: CSV (comma-separated)

### Vesiclepedia
- **3,481 studies** from 1983-2024
- **99.9% complete**: Missing only 359/621,000 entries
- **Format**: TXT (tab-delimited)

---

## Key Statistics

| Metric | EVmiRNA2.0 | Vesiclepedia |
|--------|------------|--------------|
| Projects/Studies | 371 | 3,481 |
| miRNA entries | - | 22,858 |
| Protein entries | - | 566,911 |
| Lipid entries | - | 3,839 |
| Expression values | ✅ TPM + counts | ⚠️ Limited |
| Sample metadata | ✅ Detailed | ✅ Detailed |

---

## Use Cases

### Use EVmiRNA2.0 for:
- Quantitative miRNA expression analysis
- Differential expression (with counts)
- Statistical comparisons
- Recent studies (2015+)

### Use Vesiclepedia for:
- Protein biomarker discovery
- Lipid profiling
- Multi-omics integration
- Historical meta-analysis
- Cross-species comparison

### Use Both for:
- Comprehensive EV characterization
- Cross-validation of miRNA findings
- Multi-omics biomarker panels
- Systems biology approaches

---

## Documentation Files

| File | Purpose |
|------|---------|
| **DATA_COLLECTION_COMPLETE.md** | Comprehensive summary of all data |
| **VESICLEPEDIA_DATA_STRUCTURE.md** | Detailed Vesiclepedia file structure |
| **VESICLEPEDIA_COMPLETE_STATUS.md** | Coverage analysis |
| **QUICK_START.md** | This file - quick reference |

---

## Missing Data

### EVmiRNA2.0
27 projects lack expression_count files (database limitation):
```
PRJNA252516, PRJNA287115, PRJNA290097, PRJNA326271, PRJNA359418,
PRJNA373850, PRJNA415976, PRJNA416912, PRJNA432230, PRJNA442026,
PRJNA453481, PRJNA472881, PRJNA473821, PRJNA483056, PRJNA505884,
PRJNA554349, PRJNA562276, PRJNA576379, PRJNA588268, PRJNA596469,
PRJNA643272, PRJNA649239, PRJNA666135, PRJNA835495, PRJNA880575,
PRJNA894097, PRJNA952560
```

### Vesiclepedia
- 192 metabolites (no bulk download)
- 167 DNA entries (web query only)
- **Impact**: Minimal (0.06% of total data)

---

## Citations

**EVmiRNA2.0**:
```
Li, Y., et al. (2022). EVmiRNA2.0: An Updated Database of Extracellular
Vesicle miRNAs. Nucleic Acids Research.
```

**Vesiclepedia**:
```
Chitti, S. V., et al. (2024). Vesiclepedia 2024: an extracellular vesicles
and extracellular particles repository. Nucleic Acids Research, 52(D1),
D1694–D1698.
```

---

## Need Help?

### Full Documentation
- EVmiRNA2.0: https://guolab.wchscu.cn/EVmiRNA2.0/#/document
- Vesiclepedia: http://www.microvesicles.org/

### Example Analysis Scripts
Check the `archive/` directory for:
- Download scripts
- Test scripts
- Helper functions

---

*Last updated: November 17, 2025*
