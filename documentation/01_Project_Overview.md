# EVDx Project Overview

**Last Updated**: November 22, 2025

## Mission

EVDx aims to develop AI-powered diagnostic tools using extracellular vesicle (EV) biomarkers for early disease detection, with focus on cancer diagnosis.

---

## Background

### What are Extracellular Vesicles?

Extracellular vesicles (EVs) are membrane-bound particles released by cells into body fluids. They carry molecular cargo including:
- **Proteins** - Direct functional molecules
- **miRNAs** - Gene expression regulators
- **mRNAs, lipids** - Other bioactive molecules

### Why EVs for Diagnosis?

1. **Non-invasive** - Detectable in blood, urine, saliva
2. **Tissue-specific** - Reflect origin cell characteristics
3. **Early detection** - Present before clinical symptoms
4. **Stable** - Protected cargo for reliable measurement

### The Opportunity

Recent studies demonstrate:
- **90%+ sensitivity/specificity** for cancer detection (Hoshino 2020)
- **Universal markers** like Syntenin-1 for normalization (Kugeratski 2021)
- **Pan-cancer signatures** distinguishing 21 cancer types

---

## Project Goals

### Phase 1: Data Collection ✅ Complete

Assemble comprehensive EV datasets from published studies:
- 4 data sources acquired
- ~3.5 GB total data
- 586+ exosome samples with proteomics
- 371 projects with miRNA data

### Phase 2: Data Standardization (Next)

Harmonize data for machine learning:
- Map protein/gene identifiers
- Normalize across datasets
- Handle missing values
- Extract disease labels

### Phase 3: Model Development

Build diagnostic classifiers:
- Cancer vs healthy detection
- Multi-cancer type classification
- Biomarker panel optimization

---

## Data Summary

| Dataset | Type | Samples | Key Use |
|---------|------|---------|---------|
| **Hoshino 2020** | Proteins | 512 | Clinical classification |
| **Kugeratski 2021** | Proteins | 42 | Normalization markers |
| **EVmiRNA2.0** | miRNAs | 371 projects | miRNA signatures |
| **Vesiclepedia** | Mixed | 3,481 expts | Validation reference |

**Total storage**: ~3.5 GB

→ See [02_Data_Sources.md](02_Data_Sources.md) for detailed descriptions

---

## Project Structure

```
EVDx/
├── README.md                 # Quick start
├── documentation/            # Detailed docs
├── scripts/                  # Utility scripts
├── papers/                   # Reference papers
├── evmirna_data/            # miRNA database
├── vesiclepedia_data/       # EV cargo database
├── hoshino2020_data/        # Clinical proteomics
└── kugeratski2021_data/     # Cell line proteomics
```

---

## Key Publications

1. **Hoshino et al. (2020)**
   *Extracellular Vesicle and Particle Biomarkers Define Multiple Human Cancers*
   Cell 182(4):1044-1061 | PRIDE: PXD018301

2. **Kugeratski et al. (2021)**
   *Quantitative Proteomics Identifies the Core Proteome of Exosomes with Syntenin-1 as the Highest Abundant Protein*
   Nat Cell Biol 23(6):631-641 | PRIDE: PXD020260

3. **EVmiRNA2.0 (2022)**
   *An Updated Database of Extracellular Vesicle miRNAs*
   Nucleic Acids Res | https://bioinfo.life.hust.edu.cn/EVmiRNA

4. **Vesiclepedia (2024)**
   *An Extracellular Vesicles and Extracellular Particles Repository*
   Nucleic Acids Res 52(D1):D1694-D1698

---

## Next Steps

→ [03_Research_Directions.md](03_Research_Directions.md) - Integration strategies
→ [04_Quick_Reference.md](04_Quick_Reference.md) - Code examples
