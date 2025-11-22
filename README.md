# EVDx - AI-Powered Disease Diagnosis from Extracellular Vesicles

## Project Overview

**EVDx** (EV Diagnosis) is a research project developing machine learning and AI models for disease diagnosis using extracellular vesicle (EV) cargo data. Our goal is to predict potential diseases from unlabeled EV samples by training models on comprehensive, multi-source EV datasets.

### Research Question
**Can we diagnose diseases from EV molecular profiles using machine learning?**

Given an EV sample without disease labeling, can we identify potential diseases in the patient based on the molecular cargo (miRNAs, proteins, lipids) present in their extracellular vesicles?

### Approach

1. **Data Collection** ✅ COMPLETED
   - Aggregate EV cargo data from published research papers
   - Download raw data from public databases (EVmiRNA2.0, Vesiclepedia)
   - Process additional datasets from peer-reviewed publications
   - **Status**: All 4 data sources downloaded and analyzed

2. **Data Standardization** (Next Phase)
   - Transform data from different sources into unified format
   - Harmonize feature representations across datasets
   - Minimize data loss during transformation
   - Create standardized training datasets

3. **Model Development** (Future Phase)
   - Identify diseases with sufficient sample sizes
   - Build and validate machine learning models
   - Evaluate diagnostic performance
   - Assess model generalizability

### Current Data Collection

Comprehensive extracellular vesicle (EV) cargo data from four sources:

| Dataset | Data Type | Samples | Features | Quantification | Disease Labels |
|---------|-----------|---------|----------|----------------|----------------|
| **EVmiRNA2.0** | miRNAs | 371 projects | ~2,000 | TPM / counts | Yes |
| **Vesiclepedia** | Mixed | 3,481 experiments | 566K prot, 23K miRNA | Presence/absence | Partial |
| **Hoshino 2020** | Proteins | 512 human | 9,938 | MS intensity | Yes (21 cancers) |
| **Batagov 2021** | Proteins | 42 (cell lines) | 1,243 | Log2 SILAC ratio | No |

**Total**: 1,101 files, 3.5 GB

See `documentation/04_Dataset_Comparison_and_Research_Directions.md` for detailed comparison and research strategies.

---

## Directory Structure

```
EV_database/
├── evmirna_data/              # EVmiRNA2.0 data (371 projects, 1,086 CSV files)
├── vesiclepedia_data/         # Vesiclepedia data (8 comprehensive files)
├── hoshino2020_data/          # Hoshino 2020 proteomics (3 files, 123 MB)
├── batagov2021_data/          # Batagov 2021 proteomics (4 files, 3.2 GB)
├── scripts/                   # Download and utility scripts
├── documentation/             # Data structure guides and analysis docs
├── papers/                    # Original research papers
└── README.md                  # This file
```

---

## Data Download

**Note**: Large data files (>50 MB) are not included in the GitHub repository due to size limits. After cloning, download them separately:

### Hoshino 2020 (123 MB)
```bash
cd hoshino2020_data/
# Download from PRIDE
curl -O ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2020/08/PXD018301/Human512Reports.xlsx
curl -O ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2020/08/PXD018301/Mouse74Reports.xlsx
```

### Batagov 2021 (3.2 GB)
```bash
cd batagov2021_data/
# Download from PRIDE
curl -O "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2021/06/PXD020260/txt folder MaxQuant - MS 14 cell lines derived exosomes files.zip"
curl -O "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2021/06/PXD020260/txt folder MaxQuant - MS isolation methods comparison files.zip"

# Extract
unzip "txt folder MaxQuant - MS 14 cell lines derived exosomes files.zip"
unzip "txt folder MaxQuant - MS isolation methods comparison files.zip"
```

**Included in repo**: README files, `Source Quantitative.xlsx` (2.4 MB), all EVmiRNA and Vesiclepedia data.

---

## Data Files

### evmirna_data/ (104 MB, 1,086 files)

371 projects with up to 3 CSV files each:
- `{PROJECT_ID}_metadata.csv` - Sample information and experimental conditions
- `{PROJECT_ID}_expression.csv` - Normalized miRNA expression (TPM)
- `{PROJECT_ID}_expression_count.csv` - Raw miRNA read counts

**Example**:
```
PRJDB2585_metadata.csv
PRJDB2585_expression.csv
PRJDB2585_expression_count.csv
```

### vesiclepedia_data/ (78 MB, 8 files)

Comprehensive EV cargo from 3,481 studies:
- `Vesiclepedia_experiment_details.txt` - Study metadata (3,481 experiments)
- `Vesiclepedia_protein_mRNA_details.txt` - Protein and mRNA cargo (566,911 entries)
- `Vesiclepedia_miRNA_details.txt` - miRNA cargo (22,858 entries)
- `Vesiclepedia_gene_details.txt` - Gene annotations (46,687 genes)
- `Vesiclepedia_lipid_details.txt` - Lipid cargo (3,839 entries)
- `Vesiclepedia_PTM_details.txt` - Post-translational modifications
- `Vesiclepedia_Proteins_GPAD.txt` - Gene Ontology annotations (proteins)
- `Vesiclepedia_RNAs_GPAD.txt` - Gene Ontology annotations (RNAs)

### hoshino2020_data/ (123 MB, 3 files)

Pan-cancer exosome proteomics from tissue and plasma:
- `Human512Reports.xlsx` - 512 human samples across 21 cancer types
- `Mouse74Reports.xlsx` - 74 mouse exosome samples
- `README.txt` - File inventory and metadata

**PRIDE ID**: PXD018301 | **Paper**: Hoshino et al., Cell 2020

### batagov2021_data/ (3.2 GB, 4 files)

Core exosome proteome with Syntenin-1 as universal marker:
- `txtfolderMaxQuant-MS14celllinesderivedexosomesfiles.zip` - 14 cell lines (2.0 GB)
- `txtfolderMaxQuant-MSisolationmethodscomparisonfiles.zip` - Isolation methods (1.2 GB)
- `Source Quantitative.xlsx` - Quantitative SILAC data (2.4 MB)
- `README.txt` - File inventory with checksums

**PRIDE ID**: PXD020260 | **Paper**: Batagov et al., Nat Commun 2021

---

## Scripts

### EVmiRNA2.0 Scripts
- `EVmiRNA2.0_download_all_projects.sh` - Main download script (bash)
- `EVmiRNA2.0_get_project_ids.js` - Browser script to extract project IDs
- `EVmiRNA2.0_project_ids.txt` - List of 371 project IDs
- `EVmiRNA2.0_project_ids.json` - Project IDs in JSON format
- `EVmiRNA2.0_download.log` - Download log file

### Usage

**To download all EVmiRNA2.0 data**:
```bash
cd scripts/
./EVmiRNA2.0_download_all_projects.sh
```

**To get project IDs** (if needed):
1. Open https://guolab.wchscu.cn/EVmiRNA2.0/#/download in browser
2. Open browser console (F12)
3. Copy and paste contents of `EVmiRNA2.0_get_project_ids.js`
4. Wait for automatic pagination and download

---

## Documentation

### Core Documents
- **04_Dataset_Comparison_and_Research_Directions.md** - **START HERE** - Comprehensive comparison of all 4 datasets with research strategies
- **01_Quick_Start_Guide.md** - Quick reference for loading and using data

### Dataset-Specific Guides
- **00_Data_Collection_Complete.md** - Complete summary of all downloaded data
- **02_Disease_And_Demographics_Info.md** - Disease information and study design details
- **03_Proteomics_Data_Overview.md** - Proteomics datasets (Hoshino 2020, Batagov 2021)

### Vesiclepedia Reference
- **Vesiclepedia_Overview.md** - Introduction to Vesiclepedia database
- **Vesiclepedia_Data_Structure.md** - Detailed file structure and relationships
- **Vesiclepedia_Coverage_Analysis.md** - Data completeness assessment (99.9%)

---

## Papers

- `EVmiRNA2.0_paper.pdf` - EVmiRNA2.0 database publication
- `Vesiclepedia_2024_paper.pdf` - Vesiclepedia 2024 database publication
- `Link to raw data.xlsx` - Additional data links

---

## Quick Data Loading

### Python
```python
import pandas as pd

# === EVmiRNA2.0 ===
metadata = pd.read_csv('evmirna_data/PRJDB2585_metadata.csv')
expression = pd.read_csv('evmirna_data/PRJDB2585_expression.csv')
counts = pd.read_csv('evmirna_data/PRJDB2585_expression_count.csv')

# === Vesiclepedia ===
experiments = pd.read_csv('vesiclepedia_data/Vesiclepedia_experiment_details.txt', sep='\t')
mirnas = pd.read_csv('vesiclepedia_data/Vesiclepedia_miRNA_details.txt', sep='\t')
proteins = pd.read_csv('vesiclepedia_data/Vesiclepedia_protein_mRNA_details.txt', sep='\t')

# === Hoshino 2020 ===
# Note: Complex Excel structure - rows 0-2 are metadata, data starts row 3
hoshino = pd.read_excel('hoshino2020_data/Human512Reports.xlsx',
                        sheet_name='proteins', header=None)
# Row 0: source type (plasma/not plasma/cell culture)
# Row 1: sample filenames
# Row 2: column headers
# Rows 3+: protein intensity data (9,938 proteins × 512 samples)

# === Batagov 2021 ===
# Supplementary table with curated SILAC ratios
batagov = pd.read_excel('batagov2021_data/Source Quantitative.xlsx',
                        sheet_name='Supplementary Table 2', header=None)
# Row 0: column headers (cell line names)
# Row 1+: protein data (1,243 proteins × 42 samples)
# Values: Log2 SILAC ratios (exosome/standard)
```

### R
```r
library(readxl)

# === EVmiRNA2.0 ===
metadata <- read.csv('evmirna_data/PRJDB2585_metadata.csv')
expression <- read.csv('evmirna_data/PRJDB2585_expression.csv')
counts <- read.csv('evmirna_data/PRJDB2585_expression_count.csv')

# === Vesiclepedia ===
experiments <- read.delim('vesiclepedia_data/Vesiclepedia_experiment_details.txt')
mirnas <- read.delim('vesiclepedia_data/Vesiclepedia_miRNA_details.txt')
proteins <- read.delim('vesiclepedia_data/Vesiclepedia_protein_mRNA_details.txt')

# === Hoshino 2020 ===
hoshino <- read_excel('hoshino2020_data/Human512Reports.xlsx',
                      sheet = 'proteins', col_names = FALSE)

# === Batagov 2021 ===
batagov <- read_excel('batagov2021_data/Source Quantitative.xlsx',
                      sheet = 'Supplementary Table 2', col_names = FALSE)
```

---

## Data Summary

### EVmiRNA2.0 (371 projects)
- **Metadata**: 371/371 files (100%)
- **Expression**: 371/371 files (100%)
- **Expression Count**: 344/371 files (93%)
- **Coverage**: Excellent for miRNA expression analysis
- **Format**: CSV (comma-separated)

### Vesiclepedia (3,481 studies)
- **Completeness**: 99.9% (missing 0.1% - metabolites and DNA)
- **Studies**: From 619 unique publications
- **Timespan**: 1983-2024
- **Species**: 73% human, 14% mouse, 13% other
- **Format**: Tab-delimited text

### Disease Information
- **EVmiRNA2.0**: Disease field available for most projects
  - Colorectal cancer: 441 samples
  - Prostate cancer: 267 samples
  - Healthy donors: 1,789 samples
  - Many other diseases represented

- **Vesiclepedia**: ~26% have disease context
  - Various cancers, cardiovascular, autoimmune diseases
  - Sample names indicate disease state

### Demographics
- ⚠️ **Limited**: No systematic age, sex, or race information
- ✅ **Available**: Species, disease status, sample type
- **Note**: Would need original publications for detailed demographics

---

## Project Roadmap

### Phase 1: Data Collection ✅ COMPLETED

**Completed Sources**:
- ✅ EVmiRNA2.0 (371 projects, 1,086 files, 104 MB)
- ✅ Vesiclepedia (3,481 studies, 8 files, 78 MB)
- ✅ Hoshino 2020 Proteomics (512 human + 74 mouse samples, 123 MB)
- ✅ Batagov 2021 Proteomics (14 cell lines + isolation methods, 3.2 GB)

**Phase 1 Summary**:
- **Total Files**: 1,101 files
- **Total Size**: 3.5 GB
- **Data Types**: miRNAs, proteins, lipids, RNA
- **Samples**: ~4,500+ experiments
- **Completion Date**: November 17, 2025

### Phase 2: Data Standardization ⏳ Planned

**Objectives**:
- Unify data formats across all sources
- Standardize feature nomenclature (miRNA names, protein IDs, etc.)
- Handle missing values and batch effects
- Create merged dataset with minimal information loss

**Key Challenges**:
- Different molecular profiling platforms
- Varying data normalization methods
- Inconsistent disease labeling
- Multi-omics integration (miRNA + proteins + lipids)

**Deliverables**:
- Unified data schema
- Transformation pipeline scripts
- Quality control reports
- Training-ready datasets

### Phase 3: Disease Model Development ⏳ Planned

**Prerequisites**:
- Identify diseases with ≥50 samples (or threshold TBD)
- Ensure balanced disease/healthy controls
- Assess data quality per disease category

**Model Objectives**:
- Multi-class disease classification
- Disease probability scoring
- Feature importance analysis (which miRNAs/proteins are diagnostic)
- Cross-validation across data sources

**Potential Diseases** (based on current data):
- Colorectal cancer (441 samples in EVmiRNA2.0)
- Prostate cancer (267 samples)
- Parkinson's disease (315 samples)
- Type I diabetes (195 samples)
- Multiple cancers from Vesiclepedia

---

## Current Use Cases

### For Machine Learning Training:

**EVmiRNA2.0**:
- Quantitative features: miRNA expression (TPM) and counts
- Disease labels available in metadata
- 371 projects across multiple diseases
- Ideal for supervised learning

**Vesiclepedia**:
- Multi-omics features: proteins, miRNAs, lipids
- 3,481 experiments with disease annotations
- Feature discovery and biomarker identification
- Cross-validation of findings

**Combined Dataset**:
- Comprehensive feature space for model training
- Cross-database validation to reduce overfitting
- Multi-omics integration for improved accuracy
- Large sample size for deep learning approaches

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

**Hoshino 2020**:
```
Hoshino A, et al. (2020). Extracellular Vesicle and Particle Biomarkers
Define Multiple Human Cancers. Cell. 182(4):1044-1061.e18.
DOI: 10.1016/j.cell.2020.07.009
```

**Batagov 2021**:
```
Batagov AO, Kurochkin IV, Gorshkov K, Galieva ER, Shagimardanova EI,
Gusev OA. (2021). Quantitative proteomics identifies Sytenin-1 as the most
abundant protein in exosomes purified from human cell lines. [Journal TBD]
PRIDE: PXD020260
```

---

## Resources

- **EVmiRNA2.0 Website**: https://guolab.wchscu.cn/EVmiRNA2.0/
- **EVmiRNA2.0 Docs**: https://guolab.wchscu.cn/EVmiRNA2.0/#/document
- **Vesiclepedia Website**: http://www.microvesicles.org/
- **Vesiclepedia Help**: Available on website

---

## Notes

### Missing Data

**EVmiRNA2.0**: 27 projects lack raw count files (database limitation, not download error)

**Vesiclepedia**: 0.06% missing (359 entries)
- 192 metabolites (no bulk download)
- 167 DNA entries (web query only)

### Study Design
- 3,481 Vesiclepedia "experiments" ≠ 3,481 people
- Come from 619 unique publications
- ~59% cell line studies, ~40% tissue/biofluid samples
- Estimated 200-500 unique human individuals in biofluid studies

---

## Project Status

**Current Phase**: Phase 2 - Data Standardization ⏳ IN PROGRESS

**Last Updated**: November 22, 2025

**Phase 1 Summary** (Completed):
- Sources completed: 4/4 (100%)
- Total files: 1,101 files
- Total size: 3.5 GB
- Data types: miRNAs, proteins, lipids, RNA
- Disease categories: 20+ cancer types represented
- Sample size: ~4,500+ experiments

**Current Focus**: Dataset Integration Planning
- Analyzed all 4 dataset structures
- Identified integration challenges (different IDs, quantification methods, sample types)
- Proposed 5 research strategies (see documentation)
- Created comprehensive comparison document

**Next Steps**:
1. Map proteins between Hoshino and Batagov (UniProt/gene names)
2. Extract disease labels from Hoshino filenames
3. Standardize EVmiRNA project data
4. Implement pathway-level integration for multi-omics analysis

**Key Documents**:
- `documentation/04_Dataset_Comparison_and_Research_Directions.md` - Research strategies

---

*This README is automatically updated as the project progresses.*
