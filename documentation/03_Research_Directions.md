# Research Directions

**Last Updated**: November 22, 2025

## Overview

This document outlines integration strategies and machine learning approaches for EV-based disease diagnosis.

---

## Integration Challenges

### Technical Challenges

| Challenge | Description | Solution |
|-----------|-------------|----------|
| **ID Mapping** | Different protein/gene identifiers | UniProt/HGNC mapping |
| **Quantification** | Different scales (absolute vs relative) | Rank normalization |
| **Missing Data** | 87% missing in Hoshino | Imputation or filtering |
| **Batch Effects** | Between datasets/projects | ComBat, limma |

### Biological Challenges

1. **Cell Line vs Clinical** - Cell lines lack tumor microenvironment
2. **Multi-Omics Integration** - Proteins and miRNAs measure different biology
3. **Disease Heterogeneity** - Same disease may have subtypes

---

## Research Strategies

### Strategy A: Proteomics-Focused Classification

**Goal**: Build cancer classifiers using Hoshino clinical data

**Approach**:
1. Parse disease labels from Hoshino filenames
2. Use Kugeratski universal markers (Syntenin-1) for normalization
3. Handle missing values (imputation/filtering)
4. Train multi-class classifier (21 cancers)

**Advantages**:
- Direct clinical relevance
- Published benchmark (90%+ accuracy)
- Same data type

**Challenges**:
- High missing rate
- Single study (limited generalizability)

---

### Strategy B: Pathway-Level Integration

**Goal**: Integrate proteins and miRNAs via biological pathways

**Approach**:
1. Map proteins to KEGG/Reactome pathways
2. Map miRNAs → target genes → pathways
3. Calculate pathway activity scores per sample
4. Use pathway scores as ML features

**Advantages**:
- Integrates all datasets
- Reduces dimensions (10K features → 300 pathways)
- Biologically interpretable
- Robust to technical variation

**Challenges**:
- Requires external databases
- miRNA target prediction has false positives

---

### Strategy C: Disease-Specific Models

**Goal**: Build focused models for well-sampled diseases

**Priority Diseases** (by sample count):

| Disease | Source | Samples |
|---------|--------|---------|
| Colorectal cancer | EVmiRNA | 441 |
| Parkinson's | EVmiRNA | 315 |
| Prostate cancer | EVmiRNA | 267 |
| Pancreatic cancer | Hoshino + cell lines | Multiple |
| Breast cancer | Hoshino + cell lines | Multiple |

**Approach**:
1. Select diseases with ≥50 samples
2. Build binary classifiers (disease vs healthy)
3. Compare protein vs miRNA models
4. Ensemble predictions

**Advantages**:
- Well-powered analyses
- Clinical relevance
- Can compare modalities

---

## Recommended Workflow

### Phase 2A: Proteomics Integration (Immediate)

1. **Map proteins between Hoshino and Kugeratski**
   - Use gene names as primary key
   - Expect ~1,000 overlapping proteins

2. **Extract Hoshino disease labels**
   - Parse filenames
   - Create clean metadata file

3. **Normalize using Kugeratski markers**
   - Apply Syntenin-1 normalization
   - Assess isolation method effects

4. **Build baseline classifier**
   - Start with 2-3 cancer types
   - Establish baseline performance

### Phase 2B: EVmiRNA Integration (Next)

1. **Standardize miRNA names**
   - Handle nomenclature variations
   - Map to current miRBase

2. **Select well-annotated projects**
   - Clear disease labels
   - Minimum sample size ≥30

3. **Pathway mapping pilot**
   - Test with colorectal cancer
   - Compare protein vs miRNA results

### Phase 2C: Cross-Validation (Later)

1. **Cross-modality validation**
   - Compare protein vs miRNA predictions
   - Ensemble approaches

2. **External validation**
   - Test on held-out samples
   - Cross-dataset generalization

---

## ML Model Options

### For Classification

| Model | Use Case | Notes |
|-------|----------|-------|
| Random Forest | Baseline | Handles missing data |
| XGBoost | Performance | Feature importance |
| Neural Network | Multi-omics | Requires more data |
| SVM | Small datasets | Good with high dimensions |

### For Feature Selection

| Method | Purpose |
|--------|---------|
| LASSO | Minimal biomarker panel |
| Elastic Net | Grouped features |
| mRMR | Non-redundant features |
| SHAP | Interpretability |

---

## Success Metrics

### Technical
- Protein mapping rate: >80%
- Missing rate after imputation: <20%
- Batch effect reduction: PCA shows no dataset clustering

### Model Performance
- Binary accuracy: >80%
- AUC-ROC: >0.85
- Cross-dataset drop: <10%

### Biological Validation
- Pathway enrichment: FDR <0.05
- Cross-modality consistency: Same pathways identified
- Known biomarker overlap: Published markers detected

---

## Required Resources

### External Databases

| Resource | Purpose | URL |
|----------|---------|-----|
| UniProt | Protein ID mapping | uniprot.org |
| HGNC | Gene name standard | genenames.org |
| miRBase | miRNA nomenclature | mirbase.org |
| TargetScan | miRNA targets | targetscan.org |
| KEGG | Pathways | genome.jp/kegg |
| Reactome | Pathways | reactome.org |

### Software

**Python**: pandas, scikit-learn, PyTorch, XGBoost
**R**: limma, ComBat, clusterProfiler, DESeq2
**Pathway**: GSEA, ssGSEA, PROGENy

---

## Next Steps

1. Start with **Strategy A** (proteomics classification)
2. Establish baseline performance
3. Add **Strategy B** (pathway integration) for multi-omics
4. Build **Strategy C** (disease-specific models) for well-sampled diseases

→ [04_Quick_Reference.md](04_Quick_Reference.md) - Code examples for data loading
