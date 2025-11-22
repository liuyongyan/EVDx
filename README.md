# EVDx - AI-Powered Disease Diagnosis from Extracellular Vesicles

## Overview

EVDx develops machine learning models for disease diagnosis using extracellular vesicle (EV) biomarkers. The goal is to predict diseases from EV molecular profiles (proteins, miRNAs).

**Current Status**: Phase 1 Complete | Phase 2 In Progress

---

## Data Summary

Four complementary datasets covering proteins, miRNAs, and metadata:

| Dataset | Type | Samples | Key Use |
|---------|------|---------|---------|
| **Hoshino 2020** | Proteins | 512 | Clinical classification (21 cancers) |
| **Kugeratski 2021** | Proteins | 42 | Normalization markers |
| **EVmiRNA2.0** | miRNAs | 371 projects | miRNA signatures |
| **Vesiclepedia** | Mixed | 3,481 expts | Validation reference |

**Total**: ~3.5 GB, 1,101 files

→ See [documentation/02_Data_Sources.md](documentation/02_Data_Sources.md) for details

---

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/[username]/EVDx.git
cd EVDx
```

### 2. Download Large Files (3.3 GB)
```bash
./scripts/download_large_files.sh
```

### 3. Load Data

**Python**:
```python
import pandas as pd

# Hoshino 2020 - Clinical proteomics
hoshino = pd.read_excel('hoshino2020_data/Human512Reports.xlsx', header=None)

# Kugeratski 2021 - Cell line proteomics
kugeratski = pd.read_excel('kugeratski2021_data/Source Quantitative.xlsx',
                           sheet_name='Supplementary Table 2', header=None)

# EVmiRNA2.0 - miRNA expression
expression = pd.read_csv('evmirna_data/projects/PRJDB2585/expression.csv')

# Vesiclepedia - Reference database
proteins = pd.read_csv('vesiclepedia_data/VESICLEPEDIA_PROTEIN_MRNA_DATA_2024_10_13.txt', sep='\t')
```

→ See [documentation/04_Quick_Reference.md](documentation/04_Quick_Reference.md) for more examples

---

## Project Structure

```
EVDx/
├── README.md                    # This file
├── documentation/               # Detailed documentation
│   ├── 01_Project_Overview.md   # Background and goals
│   ├── 02_Data_Sources.md       # Dataset details
│   ├── 03_Research_Directions.md # Integration strategies
│   └── 04_Quick_Reference.md    # Code examples
├── scripts/                     # Utility scripts
├── papers/                      # Reference papers
├── evmirna_data/               # miRNA database (371 projects)
├── vesiclepedia_data/          # EV cargo database
├── hoshino2020_data/           # Clinical proteomics
└── kugeratski2021_data/        # Cell line proteomics
```

---

## Documentation

| Document | Content |
|----------|---------|
| [01_Project_Overview.md](documentation/01_Project_Overview.md) | Project background, goals, and scope |
| [02_Data_Sources.md](documentation/02_Data_Sources.md) | Detailed description of all 4 datasets |
| [03_Research_Directions.md](documentation/03_Research_Directions.md) | Integration strategies and ML approaches |
| [04_Quick_Reference.md](documentation/04_Quick_Reference.md) | Code examples for data loading |

---

## Project Phases

### Phase 1: Data Collection ✅ Complete
- 4 data sources acquired
- ~3.5 GB total data
- 586+ exosome samples with proteomics
- 371 projects with miRNA data

### Phase 2: Data Standardization ⏳ In Progress
- Map protein/gene identifiers
- Normalize across datasets
- Handle missing values
- Extract disease labels

### Phase 3: Model Development 📋 Planned
- Cancer vs healthy classification
- Multi-cancer type classification
- Biomarker panel optimization

---

## Key Findings from Data

- **90%+ sensitivity/specificity** for cancer detection (Hoshino 2020)
- **Syntenin-1** identified as universal exosome marker (Kugeratski 2021)
- **21 cancer types** represented in clinical samples
- **Overlapping cell lines** (MCF7, MDA-MB-231, PANC1, HEK293) enable cross-validation

---

## Citations

**Hoshino et al. (2020)** - Cell 182(4):1044-1061 | PRIDE: PXD018301

**Kugeratski et al. (2021)** - Nat Cell Biol 23(6):631-641 | PRIDE: PXD020260

**EVmiRNA2.0 (2022)** - Nucleic Acids Res | https://bioinfo.life.hust.edu.cn/EVmiRNA

**Vesiclepedia (2024)** - Nucleic Acids Res 52(D1):D1694-D1698

---

## Resources

- [EVmiRNA2.0 Website](https://guolab.wchscu.cn/EVmiRNA2.0/)
- [Vesiclepedia Website](http://www.microvesicles.org/)
- [PRIDE Archive](https://www.ebi.ac.uk/pride/)

---

**Last Updated**: November 22, 2025
