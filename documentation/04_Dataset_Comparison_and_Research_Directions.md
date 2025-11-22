# Dataset Comparison and Research Directions

**Last Updated**: November 22, 2025

## Overview

This document provides a comprehensive comparison of all four datasets in the EVDx project and proposes potential research directions for Phase 2 (Data Standardization) and Phase 3 (Model Development).

---

## 1. Dataset Summary

### 1.1 At a Glance

| Dataset | Data Type | Samples | Features | Quantification | Disease Labels |
|---------|-----------|---------|----------|----------------|----------------|
| **Hoshino 2020** | Proteins | 512 human | 9,938 | MS intensity | Yes (21 cancers) |
| **Batagov 2021** | Proteins | 42 (14 cell lines × 3) | 1,243 | Log2 SILAC ratio | No (cell lines) |
| **EVmiRNA2.0** | miRNAs | 371 projects | ~2,000 | TPM / counts | Yes (varied) |
| **Vesiclepedia** | Mixed | 3,481 experiments | 566K prot, 23K miRNA | Presence/absence | Partial (~26%) |

### 1.2 Data Sources

| Dataset | Source | PRIDE ID | Publication |
|---------|--------|----------|-------------|
| Hoshino 2020 | PRIDE | PXD018301 | Cell 2020 |
| Batagov 2021 | PRIDE | PXD020260 | Nat Commun 2021 |
| EVmiRNA2.0 | Database | N/A | Nucleic Acids Res 2022 |
| Vesiclepedia | Database | N/A | Nucleic Acids Res 2024 |

---

## 2. Detailed Dataset Characteristics

### 2.1 Hoshino 2020 - Pan-Cancer Proteomics

**Purpose**: Identify exosomal protein biomarkers for cancer diagnosis

**Data Structure**:
- Format: Excel (.xlsx)
- Main file: `Human512Reports.xlsx` (108 MB)
- Structure: 9,938 proteins × 512 samples
- Rows 0-2: Metadata (source type, filename, headers)
- Rows 3+: Protein intensity values

**Sample Composition**:
- 133 plasma samples
- 226 tissue samples ("not plasma")
- 153 cell culture samples

**Key Features**:
- Label-free quantification (MS1 intensity)
- Absolute values: 0 to 5.4 × 10¹¹
- High sparsity: 87% missing values
- Disease labels embedded in filenames
- 21 cancer types represented

**Strengths**:
- Clinical samples (directly relevant to diagnosis)
- Large sample size (512)
- Multiple cancer types
- Published diagnostic performance (90%+ sensitivity/specificity)

**Limitations**:
- High missing rate (typical for shotgun proteomics)
- No technical replicates
- Disease labels require parsing from filenames

### 2.2 Batagov 2021 - Core Exosome Proteome

**Purpose**: Identify universal exosome markers using SILAC quantification

**Data Structure**:
- Format: MaxQuant output (.txt) + Excel (.xlsx)
- Main file: `Source Quantitative.xlsx` (2.4 MB)
- Structure: 1,243 proteins × 42 samples (14 cell lines × 3 replicates)
- Values: Log2 SILAC ratios (exosome/standard)

**Cell Lines Included**:
| Category | Cell Lines |
|----------|------------|
| Cancer | MCF7, MDA-MB-231, BxPC3, PANC1, Jurkat, Raji, THP1 |
| Normal | MCF10A, BJ, HPDE, HPNE, HEK293T |
| Stromal | PSC, mCAF |

**Key Features**:
- SILAC quantification (relative to standard)
- Log2 ratios: -9 to +13
- Very low sparsity: 0.9% missing values
- 3 technical replicates per cell line
- Includes isolation method comparison (UC vs DG vs SEC)

**Key Findings**:
- **Syntenin-1 (SDCBP)**: Most abundant universal marker
- 22 proteins consistently enriched in exosomes
- 15 proteins consistently depleted

**Strengths**:
- Dense matrix (almost no missing data)
- Technical replicates for quality assessment
- Universal markers for normalization
- Controlled experimental conditions

**Limitations**:
- Cell lines only (not clinical samples)
- No disease phenotype (cannot train classifiers)
- Relative quantification (not absolute)
- Small sample size

### 2.3 EVmiRNA2.0 - miRNA Expression Database

**Purpose**: Comprehensive EV miRNA expression data from published studies

**Data Structure**:
- Format: CSV files per project
- Files per project: metadata, expression (TPM), counts
- Total: 371 projects, 1,086 files
- Expression matrix: miRNAs × samples

**Example Project (PRJDB2585)**:
- 168 miRNAs × 3 samples
- Source: Saliva
- Values: TPM (0 to ~600)

**Key Features**:
- Normalized expression (TPM)
- Raw counts also available (344/371 projects)
- Disease information in metadata
- Multiple EV types and sources

**Disease Coverage** (examples):
- Colorectal cancer: 441 samples
- Prostate cancer: 267 samples
- Parkinson's disease: 315 samples
- Type I diabetes: 195 samples
- Healthy donors: 1,789 samples

**Strengths**:
- Large number of independent studies
- Disease labels available
- Both normalized and raw data
- Diverse sample sources

**Limitations**:
- Variable quality across projects
- Different experimental protocols
- Batch effects between projects
- miRNA nomenclature variations

### 2.4 Vesiclepedia - Comprehensive EV Database

**Purpose**: Curated database of all published EV cargo

**Data Structure**:
- Format: Tab-delimited text files
- 8 main files covering different cargo types
- Relational structure (experiment → cargo)

**Content**:
- 3,481 experiments from 619 publications
- 566,911 protein/mRNA entries
- 22,858 miRNA entries
- 3,839 lipid entries
- Gene Ontology annotations included

**Key Features**:
- Binary data (presence/absence only)
- No quantification
- Extensive metadata per experiment
- Cross-references to other databases

**Strengths**:
- Comprehensive coverage
- Literature-backed entries
- GO annotations available
- Useful as reference

**Limitations**:
- No quantitative data
- Cannot be used for training models directly
- Mixed quality from different sources
- ~26% have disease context

---

## 3. Cross-Dataset Comparison

### 3.1 Molecular Type Comparison

| Aspect | Proteins (Hoshino/Batagov) | miRNAs (EVmiRNA) |
|--------|---------------------------|------------------|
| Function | Direct effectors | Regulators |
| Number | ~10,000 | ~2,000 |
| Detection | Mass spectrometry | Sequencing |
| ID system | UniProt | miRBase |
| Pathway mapping | Direct | Via targets |

### 3.2 Quantification Methods

| Dataset | Method | Scale | Interpretation |
|---------|--------|-------|----------------|
| Hoshino | Label-free MS | 0 to 10¹¹ | Higher = more protein |
| Batagov | SILAC ratio | -9 to +13 (log2) | Positive = enriched in EV |
| EVmiRNA | TPM | 0 to 10⁶ | Normalized expression |
| Vesiclepedia | Binary | 0/1 | Detected or not |

### 3.3 Sample Type Comparison

| Dataset | Clinical | Cell Line | Disease Labels |
|---------|----------|-----------|----------------|
| Hoshino | ✅ Yes | ✅ Some | ✅ 21 cancers |
| Batagov | ❌ No | ✅ All | ❌ Cell line only |
| EVmiRNA | ✅ Mixed | ✅ Mixed | ✅ Varied |
| Vesiclepedia | ✅ Mixed | ✅ Mixed | ⚠️ Partial |

### 3.4 Data Quality Comparison

| Metric | Hoshino | Batagov | EVmiRNA | Vesiclepedia |
|--------|---------|---------|---------|--------------|
| Missing rate | 87% | 0.9% | 60-70% | N/A |
| Replicates | No | Yes (3×) | Varies | N/A |
| Standardization | Single study | Single study | Multi-study | Multi-study |
| Batch effects | Minimal | Minimal | High | High |

### 3.5 Overlapping Cell Lines

Hoshino and Batagov share several cell lines:

| Cell Line | Cancer Type | In Hoshino | In Batagov |
|-----------|-------------|------------|------------|
| MCF7 | Breast cancer | ✅ | ✅ |
| MDA-MB-231 | Breast cancer | ✅ | ✅ |
| PANC1 | Pancreatic cancer | ✅ | ✅ |
| HEK293 | Kidney (normal) | ✅ | ✅ |

This overlap enables cross-dataset validation and normalization.

---

## 4. Key Integration Challenges

### 4.1 Technical Challenges

1. **ID Mapping**
   - Hoshino: UniProt accessions (e.g., P06731)
   - Batagov: Gene names + UniProt
   - EVmiRNA: miRBase IDs (e.g., hsa-let-7a-5p)
   - Solution: Use mapping databases (UniProt, HGNC)

2. **Quantification Harmonization**
   - Different scales (absolute vs relative vs normalized)
   - Different distributions
   - Solution: Rank-based normalization or pathway scores

3. **Missing Data Handling**
   - Hoshino: 87% missing (imputation needed)
   - Batagov: Nearly complete
   - EVmiRNA: Variable by project

4. **Batch Effects**
   - Between Hoshino and Batagov
   - Between EVmiRNA projects
   - Solution: ComBat, limma, or similar methods

### 4.2 Biological Challenges

1. **Cell Line vs Clinical**
   - Cell lines lack tumor microenvironment
   - May not reflect in vivo biology
   - Need validation across sample types

2. **Multi-Omics Integration**
   - Proteins and miRNAs measure different things
   - miRNAs regulate protein expression
   - Pathway-level integration recommended

3. **Disease Heterogeneity**
   - Same disease may have different subtypes
   - Limited metadata on disease stage/grade
   - May need to focus on well-annotated samples

---

## 5. Research Directions

### 5.1 Strategy A: Proteomics-Focused Disease Classification

**Approach**: Use Hoshino 2020 as primary training data, Batagov for normalization

**Steps**:
1. Extract disease labels from Hoshino filenames
2. Map proteins between Hoshino and Batagov (gene name/UniProt)
3. Use Batagov's universal markers (Syntenin-1, etc.) for normalization
4. Handle missing values (imputation or filtering)
5. Train multi-class classifier (21 cancers)
6. Validate on held-out samples or cross-validation

**Advantages**:
- Direct use of clinical samples
- Published benchmark (90%+ accuracy in paper)
- Same data type (proteins)

**Challenges**:
- High missing rate in Hoshino
- Single study (limited generalizability)

### 5.2 Strategy B: Multi-Omics Pathway Integration

**Approach**: Map proteins and miRNAs to biological pathways

**Steps**:
1. Annotate proteins with pathways (KEGG, Reactome, GO)
2. Map miRNAs to target genes (TargetScan, miRDB)
3. Map target genes to pathways
4. Calculate pathway activity scores per sample
5. Use pathway scores as features for ML
6. Train models that work across data types

**Advantages**:
- Integrates all datasets
- Reduces dimensionality (10,000 features → 300 pathways)
- Biologically interpretable
- More robust to technical variation

**Challenges**:
- Requires external databases
- Loses molecular-level resolution
- miRNA target prediction has false positives

### 5.3 Strategy C: Disease-Specific Models

**Approach**: Build separate models for diseases with sufficient samples

**Priority Diseases** (based on sample counts):
1. **Colorectal cancer** - 441 samples (EVmiRNA)
2. **Parkinson's disease** - 315 samples (EVmiRNA)
3. **Prostate cancer** - 267 samples (EVmiRNA)
4. **Pancreatic cancer** - Multiple in Hoshino + cell lines
5. **Breast cancer** - Multiple in Hoshino + cell lines

**Steps**:
1. Identify diseases with ≥50 samples
2. Build binary classifiers (disease vs healthy)
3. Compare protein-based vs miRNA-based models
4. Ensemble predictions from multiple data types

**Advantages**:
- Focused, well-powered analyses
- Can compare modalities
- Clinical relevance

**Challenges**:
- Limited to diseases with enough samples
- Cannot discover new disease associations

### 5.4 Strategy D: Transfer Learning / Cell Line Bridge

**Approach**: Use cell lines to bridge datasets and enable transfer learning

**Steps**:
1. Identify overlapping cell lines (MCF7, MDA-MB-231, PANC1, HEK293)
2. Learn transformation between Hoshino and Batagov
3. Apply to clinical samples
4. Use cell line identity as proxy for cancer type
5. Validate cell line predictions against clinical data

**Advantages**:
- Leverages both datasets
- Can learn normalization factors
- Validation across studies

**Challenges**:
- Cell lines may not represent tumors well
- Limited number of overlapping lines

### 5.5 Strategy E: Vesiclepedia as Validation/Filter

**Approach**: Use Vesiclepedia to validate and filter features

**Applications**:
1. **Feature filtering**: Keep only proteins/miRNAs reported in multiple studies
2. **Biomarker validation**: Check if discovered markers are in Vesiclepedia
3. **GO enrichment**: Use annotations for pathway analysis
4. **Literature support**: Prioritize features with published evidence

**Advantages**:
- Independent validation
- Increases confidence in results
- Literature backing

**Challenges**:
- No quantitative data
- Publication bias

---

## 6. Recommended Starting Point

Based on data quality and research goals, we recommend:

### Phase 2A: Proteomics Integration (Immediate)

1. **Map Hoshino ↔ Batagov proteins**
   - Use gene names as primary key
   - Identify ~1,000 overlapping proteins

2. **Extract and structure Hoshino disease labels**
   - Parse filenames for cancer types
   - Create clean metadata file

3. **Normalize Hoshino using Batagov markers**
   - Use Syntenin-1 and universal markers
   - Compare isolation methods

4. **Build initial classifier**
   - Start with 2-3 cancer types
   - Establish baseline performance

### Phase 2B: EVmiRNA Integration (Next)

1. **Standardize miRNA names**
   - Handle nomenclature variations
   - Map to current miRBase

2. **Select well-annotated projects**
   - Focus on projects with clear disease labels
   - Minimum sample size threshold

3. **Pathway mapping pilot**
   - Test with one disease (e.g., colorectal cancer)
   - Compare protein vs miRNA pathway scores

### Phase 2C: Cross-Validation (Later)

1. **Vesiclepedia validation**
   - Check biomarker overlap
   - Literature support analysis

2. **Cross-modality validation**
   - Do protein and miRNA models agree?
   - Ensemble approaches

---

## 7. Required External Resources

### Databases Needed

| Resource | Purpose | URL |
|----------|---------|-----|
| UniProt | Protein ID mapping | uniprot.org |
| HGNC | Gene name standardization | genenames.org |
| miRBase | miRNA nomenclature | mirbase.org |
| TargetScan | miRNA targets | targetscan.org |
| miRDB | miRNA targets | mirdb.org |
| KEGG | Pathway annotations | genome.jp/kegg |
| Reactome | Pathway annotations | reactome.org |
| Gene Ontology | Function annotations | geneontology.org |

### Software/Packages

- **Python**: pandas, scikit-learn, PyTorch
- **R**: limma, ComBat, clusterProfiler
- **Pathway analysis**: GSEA, ssGSEA, PROGENy

---

## 8. Success Metrics

### Technical Metrics
- Protein mapping rate: >80% of Batagov proteins found in Hoshino
- Missing value rate after imputation: <20%
- Batch effect reduction: significant reduction in PCA clustering by dataset

### Model Performance Metrics
- Classification accuracy: >80% for binary (cancer vs healthy)
- AUC-ROC: >0.85
- Cross-dataset generalization: performance drop <10%

### Biological Validation
- Pathway enrichment p-value: <0.05 (FDR corrected)
- Literature support: >50% of top markers in Vesiclepedia
- Consistency: protein and miRNA models identify same pathways

---

## 9. Timeline Estimate

| Phase | Tasks | Duration |
|-------|-------|----------|
| 2A | Proteomics integration | 2-3 weeks |
| 2B | EVmiRNA integration | 2-3 weeks |
| 2C | Cross-validation | 1-2 weeks |
| 3 | Model development | 4-6 weeks |

**Total estimated time**: 9-14 weeks

---

## 10. References

1. Hoshino A, et al. (2020). Extracellular Vesicle and Particle Biomarkers Define Multiple Human Cancers. Cell. 182(4):1044-1061.e18.

2. Batagov AO, et al. (2021). Quantitative Proteomics Identifies Syntenin-1 as Universal Biomarker of Exosomes. Nature Communications.

3. Li Y, et al. (2022). EVmiRNA2.0: An Updated Database of Extracellular Vesicle miRNAs. Nucleic Acids Research.

4. Chitti SV, et al. (2024). Vesiclepedia 2024: an extracellular vesicles and extracellular particles repository. Nucleic Acids Research. 52(D1):D1694–D1698.

---

*Document created: November 22, 2025*
*Author: Claude Code Assistant*
