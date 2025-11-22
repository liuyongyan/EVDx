# Proteomics Data Overview

**Last Updated**: November 17, 2025

## Summary

Two proteomics datasets have been downloaded to complete Phase 1 data collection:

| Dataset | Source | Size | Files | Samples | Key Features |
|---------|--------|------|-------|---------|--------------|
| **Hoshino 2020** | PXD018301 | 123 MB | 3 | 512 human, 74 mouse | Pan-cancer exosome biomarkers |
| **Batagov 2021** | PXD020260 | 3.2 GB | 4 | 14 cell lines | Core exosome proteome, Syntenin-1 |

**Total**: 3.3 GB, 7 files covering 586 exosome samples

---

## Dataset 1: Hoshino 2020 - Multiple Human Cancers

### Overview
**Study**: "Tissue- and plasma-derived exosomal protein biomarkers define multiple human cancers"
**PRIDE ID**: PXD018301
**Publication**: Hoshino et al., Cell 2020
**Location**: `hoshino2020_data/`

### Key Research Findings
- Analyzed 426 human samples (tissue explants, plasma, body fluids)
- Identified universal exosome markers (CD9, HSPA8, ALIX, HSP90AB1, ACTB, MSN, RAP1B)
- **Tissue Exosomes**: 90% sensitivity / 94% specificity for tumor vs normal
- **Plasma Exosomes**: 95% sensitivity / 90% specificity for cancer detection
- Defined tumor-type specific exosomal protein panels

### Files Downloaded

#### 1. Human512Reports.xlsx (108 MB)
**Content**: Processed proteomics data for 512 human exosome samples
- **Samples from**:
  - Tissue explants (151 samples)
  - Plasma-derived exosomes (120 samples)
  - Other bodily fluids (241 samples)
- **Cancer Types** (21 types total):
  - Pancreatic cancer
  - Lung carcinoma
  - Colon cancer
  - Melanoma
  - Prostate adenocarcinoma
  - Brain cancer
  - Head and neck cancer
  - Cholangiocarcinoma
  - And 13 other cancer types
- **Sample Sources**:
  - Blood plasma
  - Tissue (brain, liver, lung, pancreas, kidney, colon, etc.)
  - Bile, lymph
  - Cell culture

#### 2. Mouse74Reports.xlsx (15 MB)
**Content**: Processed proteomics data for 74 mouse exosome samples
- Control and model organism data

#### 3. README.txt (86 KB)
**Content**: File inventory and download links for all .raw mass spectrometry files

### Disease Coverage
21 disease types represented:
- **Cancers**: Pancreatic, lung, colon, melanoma, prostate, brain, neuroblastoma, retinoblastoma, osteosarcoma, rhabdomyosarcoma, Wilms' tumor, mesothelioma, cholangiocarcinoma, head/neck, synovial sarcoma, uveal melanoma, stomach
- **Other**: Chronic bronchitis, acute leukemia

### Methodology
- **Technique**: Shotgun proteomics, LC-MS/MS
- **Instruments**: Orbitrap Fusion Lumos, Q Exactive (Plus, HF)
- **Software**: Proteome Discoverer 1.4, Mascot 2.5, Percolator
- **Quantification**: MS1 intensity-based label-free

---

## Dataset 2: Batagov 2021 - Core Exosome Proteome

### Overview
**Study**: "Quantitative Proteomics Identifies Syntenin-1 as Universal Biomarker of Exosomes"
**PRIDE ID**: PXD020260
**Publication**: Batagov et al., Nature Communications 2021
**Location**: `batagov2021_data/`

### Key Research Findings
- Quantified 1,243 proteins in exosomes using Super SILAC mass spectrometry
- Identified **Syntenin-1** as the most abundant universal exosome marker
- Found 22 universally enriched proteins across cell types
- Found 15 consistently depleted proteins
- Compared exosome isolation methods (ultracentrifugation, density gradient, size exclusion)

### Files Downloaded

#### 1. txtfolderMaxQuant-MS14celllinesderivedexosomesfiles.zip (2.0 GB)
**Content**: MaxQuant processed files from 14 cell line-derived exosomes

**Cell Lines Studied**:
1. BJ (fibroblast)
2. BxPC3 (pancreatic cancer)
3. HEK293T (kidney epithelial)
4. HPDE (pancreatic ductal epithelium)
5. HPNE (pancreatic normal epithelium)
6. Jurkat (T-cell leukemia)
7. mCAF (cancer-associated fibroblasts)
8. MCF10A (breast epithelial, normal)
9. MCF7 (breast cancer)
10. MDA-MB-231 (breast cancer)
11. PANC1 (pancreatic cancer)
12. PSC (pancreatic stellate cells)
13. Raji (B-cell lymphoma)
14. THP1 (monocytic leukemia)

**Files in archive**:
- `peptides.txt` (188 MB) - Peptide-level data
- `evidence.txt` (683 MB) - Raw evidence for identifications
- `msmsScans.txt` (856 MB) - MS/MS scan information
- `allPeptides.txt` (655 MB) - All peptide matches
- `modificationSpecificPeptides.txt` (204 MB) - Modified peptides
- `mzRange.txt` (24 MB) - m/z ranges
- `parameters.txt` - MaxQuant search parameters

#### 2. txtfolderMaxQuant-MSisolationmethodscomparisonfiles.zip (1.2 GB)
**Content**: MaxQuant processed files comparing 3 isolation methods

**Isolation Methods Compared**:
1. UC - Ultracentrifugation (100,000 × g)
2. DG - Density gradient (OptiPrep/sucrose)
3. SEC - Size exclusion chromatography (qEV columns)

**Cell Lines in Comparison** (3 replicates each):
- HEK293T
- MDA-MB-231
- PANC1

**Files in archive**: Same structure as dataset 1

#### 3. Source Quantitative.xlsx (2.4 MB)
**Content**: Supplementary tables with quantitative proteomics data

**Sheets**:
- **Supplementary Table 1**: BJ cell line proteome
- **Supplementary Table 2**: Log2 SILAC ratios across all 14 cell lines
  - Contains protein names, gene names
  - Quantification for each cell line (3 replicates)
  - Gene Ontology annotations (GOBP, GOMF, GOCC)
  - KEGG pathway annotations
  - Peptide counts, sequence coverage, intensities
- **Supplementary Tables 3-6**: Additional comparative analyses

**Key Proteins Quantified** (examples from Table 2):
- **Syntenin-1 (SDCBP)**: Highest abundance across cell types
- **Collagen alpha-2(I) chain (COL1A2)**
- **Gamma-enolase (ENO2)**
- 1,240+ additional proteins

#### 4. README.txt (11 KB)
**Content**: File inventory with checksums

### Methodology
- **Technique**: Super SILAC (Stable Isotope Labeling by Amino acids in Cell culture)
- **Instruments**: Orbitrap Fusion Lumos, Q Exactive HF
- **Software**: MaxQuant for peptide identification and quantification
- **Species**: Human (Homo sapiens)
- **Replicates**: 3 technical replicates per condition

---

## Data Integration Potential

### Complementary Strengths

| Aspect | Hoshino 2020 | Batagov 2021 |
|--------|-------------|--------------|
| **Sample Type** | Clinical (tissue, plasma) | Cell line-derived |
| **Diseases** | 21 cancer types + controls | Cancer cell lines |
| **Sample Size** | 512 human, 74 mouse | 14 cell lines (42 samples) |
| **Quantification** | Label-free | SILAC (heavy/light) |
| **Disease Labels** | Yes (21 types) | Cell line identity |
| **Biomarkers** | Pan-cancer panels | Universal exosome markers |

### Cross-Validation Opportunities

1. **Universal Markers**: Validate Batagov's Syntenin-1 findings across Hoshino's 512 clinical samples
2. **Cell Line to Clinical**: Link cell line proteomes to tissue/plasma profiles
3. **Biomarker Discovery**: Integrate label-free and SILAC quantification approaches
4. **Method Validation**: Compare exosome isolation effects on disease signatures

---

## Machine Learning Applications

### Features Available

**From Hoshino 2020**:
- Protein intensity values (512 human samples × thousands of proteins)
- Disease labels (21 cancer types)
- Sample metadata (tissue type, cancer vs normal)

**From Batagov 2021**:
- SILAC ratios (exosome/standard) for 1,243 proteins
- Isolation method comparisons
- Universal exosome markers for normalization

### Potential Models

1. **Cancer Type Classification**
   - Multi-class classifier for 21 cancer types
   - Binary classifier: cancer vs normal
   - Features: exosomal protein intensities

2. **Tumor Tissue of Origin Prediction**
   - Classify cancer type from plasma exosomes
   - Address "tumors of unknown primary"

3. **Biomarker Panel Optimization**
   - Feature selection to identify minimal protein panels
   - 90%+ sensitivity/specificity reported in paper

4. **Batch Effect Correction**
   - Use Syntenin-1 and universal markers for normalization
   - Integrate across datasets

---

## Data Formats

### Hoshino 2020
**Format**: Excel (.xlsx)
**Structure**:
- Rows: Samples
- Columns: Proteins, metadata
- Values: Protein intensities (log-transformed likely)

### Batagov 2021
**Format**:
- Tab-delimited text files (.txt) in zip archives
- Excel (.xlsx) for supplementary tables

**MaxQuant Output Structure**:
- Peptide-level: All identified peptides with modifications
- Protein-level: Aggregated protein quantification
- Evidence: Raw MS/MS identification evidence
- Metadata: Experimental parameters, sample annotations

---

## Next Steps

### Immediate Tasks

1. **Extract and Explore**:
   ```bash
   # Extract MaxQuant files
   cd batagov2021_data
   unzip txtfolderMaxQuant-MS14celllinesderivedexosomesfiles.zip
   unzip txtfolderMaxQuant-MSisolationmethodscomparisonfiles.zip
   ```

2. **Load Data into Python/R**:
   ```python
   import pandas as pd

   # Hoshino data
   hoshino_human = pd.read_excel('hoshino2020_data/Human512Reports.xlsx')

   # Batagov data
   batagov_quant = pd.read_excel('batagov2021_data/Source Quantitative.xlsx',
                                   sheet_name='Supplementary Table 2')
   ```

3. **Data Exploration**:
   - Sample size per disease
   - Number of proteins quantified
   - Missing data patterns
   - Distribution of protein intensities

### Phase 2 Preparation

1. **Standardization Requirements**:
   - Map protein IDs to common nomenclature (UniProt)
   - Normalize intensities across datasets
   - Harmonize disease labels
   - Handle missing values

2. **Integration Strategy**:
   - Identify overlapping proteins
   - Cross-dataset normalization approach
   - Batch effect assessment

3. **Quality Control**:
   - Filter low-quality proteins
   - Assess replicate consistency
   - Remove outlier samples

---

## Citations

**Hoshino et al. (2020)**:
```
Hoshino A, et al. Extracellular Vesicle and Particle Biomarkers Define
Multiple Human Cancers. Cell. 2020 182(4):1044-1061.e18
DOI: 10.1016/j.cell.2020.07.009
PMID: 32795414
```

**Batagov et al. (2021)**:
```
Batagov AO, et al. Quantitative Proteomics Identifies Sytenin-1 as a
Universal Biomarker of Exosomes. Nature Communications. 2021
PRIDE: PXD020260
```

---

## Data Availability

**Download Locations**:
- Hoshino 2020: ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2020/08/PXD018301/
- Batagov 2021: ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2021/06/PXD020260/

**Local Directories**:
- `hoshino2020_data/` (123 MB)
- `batagov2021_data/` (3.2 GB compressed)

**Completion Status**: ✅ Both datasets fully downloaded (November 17, 2025)
