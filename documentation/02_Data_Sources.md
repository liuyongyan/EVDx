# Data Sources

**Last Updated**: November 22, 2025

## Overview

Four complementary datasets provide proteins, miRNAs, and metadata for EV-based diagnostics.

| Dataset | Samples | Features | Quantification | Disease Labels |
|---------|---------|----------|----------------|----------------|
| Hoshino 2020 | 512 | 9,938 proteins | MS intensity | 21 cancers |
| Kugeratski 2021 | 42 | 1,243 proteins | SILAC ratio | Cell lines |
| EVmiRNA2.0 | 371 projects | ~2,000 miRNAs | TPM | Varied |
| Vesiclepedia | 3,481 expts | 566K proteins | Binary | ~26% |

---

## 1. Hoshino 2020 - Clinical Proteomics

**Purpose**: Pan-cancer exosome biomarkers from clinical samples

### Key Highlights
- **90% sensitivity / 94% specificity** for tumor detection
- **21 cancer types** with disease labels
- Clinical samples (plasma, tissue, body fluids)

### Files

| File | Size | Content |
|------|------|---------|
| `Human512Reports.xlsx` | 108 MB | 512 samples × 9,938 proteins |
| `Mouse74Reports.xlsx` | 15 MB | 74 mouse samples |
| `README.txt` | 86 KB | File inventory |

**Location**: `hoshino2020_data/`

### Sample Distribution

| Source Type | Count |
|-------------|-------|
| Plasma | 133 |
| Tissue | 226 |
| Cell culture | 153 |

### Cancer Types Covered
Pancreatic, lung, colon, melanoma, prostate, brain, breast, neuroblastoma, osteosarcoma, cholangiocarcinoma, head/neck, and 10 others

### Data Characteristics
- **Format**: Excel with protein intensities
- **Values**: 0 to 5.4×10¹¹
- **Missing rate**: 87% (typical for shotgun proteomics)
- **Disease labels**: Embedded in filenames (requires parsing)

### Strengths
- Direct clinical relevance
- Large sample size
- Published diagnostic benchmarks

### Limitations
- High missing rate
- No technical replicates
- Single study

---

## 2. Kugeratski 2021 - Core Exosome Proteome

**Purpose**: Identify universal exosome markers for normalization

### Key Highlights
- **Syntenin-1** identified as most abundant universal marker
- **22 proteins** consistently enriched in exosomes
- Comparison of 3 isolation methods

### Files

| File | Size | Content |
|------|------|---------|
| `Source Quantitative.xlsx` | 2.4 MB | Main quantitative data |
| `*14celllines*.zip` | 2.0 GB | MaxQuant output (14 cell lines) |
| `*isolationmethods*.zip` | 1.2 GB | Method comparison data |

**Location**: `kugeratski2021_data/`

### Cell Lines (14 total)

| Category | Cell Lines |
|----------|------------|
| **Cancer** | MCF7, MDA-MB-231, BxPC3, PANC1, Jurkat, Raji, THP1 |
| **Normal** | MCF10A, BJ, HPDE, HPNE, HEK293T |
| **Stromal** | PSC, mCAF |

### Data Characteristics
- **Format**: Log2 SILAC ratios (exosome/standard)
- **Values**: -9 to +13
- **Missing rate**: 0.9% (nearly complete)
- **Replicates**: 3 technical replicates per cell line

### Universal Markers Identified
Top markers for normalization:
1. Syntenin-1 (SDCBP)
2. ALIX (PDCD6IP)
3. TSG101
4. CD9, CD63, CD81

### Strengths
- Dense matrix (almost no missing data)
- Universal markers for cross-dataset normalization
- Controlled experimental conditions

### Limitations
- Cell lines only (not clinical)
- No disease phenotype
- Small sample size

### Integration Value
Use universal markers to normalize Hoshino clinical data.

---

## 3. EVmiRNA2.0 - miRNA Expression Database

**Purpose**: Comprehensive EV miRNA profiles from published studies

### Key Highlights
- **371 projects** from diverse studies
- **TPM normalized** expression
- Multiple diseases and sample types

### Files

**Location**: `evmirna_data/`

Each project has up to 3 CSV files with naming pattern `{PROJECT_ID}_*.csv`:

```
evmirna_data/
├── PRJDB2585_metadata.csv
├── PRJDB2585_expression.csv
├── PRJDB2585_expression_count.csv
├── PRJDB6853_metadata.csv
├── PRJDB6853_expression.csv
├── PRJDB6853_expression_count.csv
└── ... (1,086 files total)
```

**File types per project**:
- `{PROJECT_ID}_metadata.csv` - Sample information
- `{PROJECT_ID}_expression.csv` - TPM normalized values
- `{PROJECT_ID}_expression_count.csv` - Raw counts (344/371 projects)

### Data Summary
- **Total projects**: 371
- **Total files**: 1,086
- **miRNAs**: ~2,000 per project
- **Expression**: TPM (transcripts per million)

### Disease Coverage (Top Examples)

| Disease | Samples |
|---------|---------|
| Colorectal cancer | 441 |
| Parkinson's disease | 315 |
| Prostate cancer | 267 |
| Type I diabetes | 195 |
| Healthy controls | 1,789 |

### Sample Sources
Blood plasma, serum, urine, saliva, cell culture media, cerebrospinal fluid

### Data Characteristics
- **Format**: CSV (one matrix per project)
- **Values**: TPM (0 to ~10⁶)
- **Raw counts**: Available for 344/371 projects

### Strengths
- Large number of independent studies
- Disease labels available
- Both normalized and raw data

### Limitations
- Variable quality across projects
- Batch effects between studies
- miRNA nomenclature variations

---

## 4. Vesiclepedia - EV Cargo Database

**Purpose**: Curated reference database of published EV content

### Key Highlights
- **3,481 experiments** from 619 publications
- **566K protein entries**
- GO annotations included

### Files

| File | Content |
|------|---------|
| `VESICLEPEDIA_PROTEIN_MRNA_DATA_*.txt` | Protein/mRNA entries |
| `VESICLEPEDIA_MIRNA_DATA_*.txt` | miRNA entries |
| `VESICLEPEDIA_LIPID_DATA_*.txt` | Lipid entries |
| `VESICLEPEDIA_EXPERIMENT_*.txt` | Experiment metadata |
| `*_PUBMEDID.txt` | Literature references |

**Location**: `vesiclepedia_data/`

### Content Summary

| Cargo Type | Entries |
|------------|---------|
| Proteins/mRNAs | 566,911 |
| miRNAs | 22,858 |
| Lipids | 3,839 |

### Data Characteristics
- **Format**: Tab-delimited text
- **Values**: Binary (presence/absence only)
- **Disease context**: ~26% of experiments

### Strengths
- Comprehensive literature coverage
- GO annotations for pathway analysis
- Independent validation source

### Limitations
- No quantitative data
- Cannot train models directly
- Publication bias

### Best Use
Validate discovered biomarkers against published literature.

---

## Dataset Comparison

### By Sample Type

| Dataset | Clinical | Cell Line |
|---------|----------|-----------|
| Hoshino | ✅ Primary | ✅ Some |
| Kugeratski | ❌ | ✅ All |
| EVmiRNA | ✅ Mixed | ✅ Mixed |
| Vesiclepedia | ✅ Mixed | ✅ Mixed |

### By Data Quality

| Metric | Hoshino | Kugeratski | EVmiRNA |
|--------|---------|------------|---------|
| Missing rate | 87% | 0.9% | 60-70% |
| Replicates | No | Yes (3×) | Varies |
| Batch effects | Minimal | Minimal | High |

### Overlapping Cell Lines

These appear in both Hoshino and Kugeratski, enabling cross-validation:
- MCF7 (breast cancer)
- MDA-MB-231 (breast cancer)
- PANC1 (pancreatic cancer)
- HEK293 (kidney normal)

---

## Download Instructions

### Small files (included in repo)
```bash
git clone https://github.com/[username]/EVDx.git
```

### Large files (3.3 GB)
```bash
cd EVDx
./scripts/download_large_files.sh
```

This downloads:
- `hoshino2020_data/Human512Reports.xlsx` (108 MB)
- `hoshino2020_data/Mouse74Reports.xlsx` (15 MB)
- `kugeratski2021_data/*.zip` (3.2 GB)

---

## Data Loading Examples

→ See [04_Quick_Reference.md](04_Quick_Reference.md) for code examples
