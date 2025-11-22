# Vesiclepedia 2024 - Data Collection Strategy

## 📊 Overview

**Vesiclepedia** (http://www.microvesicles.org) is a comprehensive database of extracellular vesicle (EV) and extracellular particle (EP) cargo.

## 🗄️ Available Data (as of 2024)

### Current Database Contents

| Data Type | Total Entries | Unique Entries |
|-----------|---------------|----------------|
| **EV Studies** | 3,533 | - |
| **Proteins** | 566,911 | 46,687 |
| **RNA Total** | 50,550 | - |
| - mRNA | 27,692 | 17,008 |
| - miRNA | 22,858 | 5,253 |
| **Lipids** | 3,839 | - |
| **Metabolites** | 192 | - |
| **DNA** | 167 | - |
| **Quantified Data** | 62,822 entries | from 47 studies |
| **Organisms** | 56 | - |
| **Sample Sources** | 252 | - |

### EV/EP Subtypes Covered

1. **Small EVs**
   - Exosomes (30-150 nm)
   - Exomeres (< 50 nm)
   - Supermeres (< 30 nm)

2. **Large EVs**
   - Ectosomes/Microvesicles (100-1000 nm)
   - Apoptotic bodies (1000-5000 nm)
   - Migrasomes (500-3000 nm)
   - Large oncosomes (1-10 μm)
   - Exophers (3500-4000 nm)

## 📥 Download Options

According to the paper, Vesiclepedia offers:

### 1. Web-Based Download
- **Format**: Tab-delimited files
- **Location**: Download page on website
- **Cost**: FREE (academic and commercial)

### 2. FunRich Plugin
- **Tool**: FunRich software integration
- **Features**:
  - Functional enrichment analysis
  - Data filtering by:
    - Sample source
    - Cell type
    - Isolation method
    - Species
    - EV subtype
  - Heatmap visualization
  - Venn diagram analysis
  - Gene enrichment analysis

### 3. Query-Based Access
- Search by:
  - Gene symbol
  - Gene name
  - miRNA name
  - Lipid name
  - DNA (via dropdown)

## 🎯 What Makes Vesiclepedia Unique

### Advantages over EVmiRNA2.0:

1. **Broader Scope**
   - Proteins (566,911 entries) ⭐
   - Lipids (3,839 entries) ⭐
   - Metabolites (192 entries) ⭐
   - DNA (167 entries) ⭐
   - RNA (similar to EVmiRNA2.0)

2. **More EV Subtypes**
   - Includes migrasomes, exophers, large oncosomes
   - Extracellular particles (exomeres, supermeres)

3. **Quality Metrics**
   - EV-TRACK scores for study quality
   - MISEV guideline compliance

4. **Quantitative Data**
   - 62,822 quantified entries
   - Relative quantification within studies

## 🚀 Recommended Download Strategy

### Option 1: Web Download (Simple)
1. Visit http://www.microvesicles.org
2. Navigate to Download page
3. Download tab-delimited files for:
   - Proteins
   - RNA (mRNA + miRNA)
   - Lipids
   - Metabolites
   - DNA

### Option 2: FunRich Plugin (Advanced)
1. Download FunRich software (http://www.funrich.org)
2. Install Vesiclepedia plugin
3. Filter and download specific datasets
4. Perform enrichment analysis

### Option 3: Automated Scraping (if needed)
- Similar approach to EVmiRNA2.0
- Would need to investigate API endpoints
- May require browser automation

## 📋 Data Structure

Based on Figure 2 in the paper, each entry contains:

**For Proteins:**
- Gene symbol
- Gene name
- Experiment details
- EV isolation method
- Flotation density (if available)
- EV subtype
- Sample source
- Organism
- Western blot data (if available)
- MS/MS peptide data
- Quantification (if available)

**For RNA/Lipids/Metabolites:**
- Similar metadata structure
- Study-specific annotations
- Quantification data (for 47 studies)

## 🔍 Use Cases

### Complementary to EVmiRNA2.0:

| Feature | EVmiRNA2.0 | Vesiclepedia |
|---------|------------|--------------|
| **Focus** | miRNA expression profiles | All EV/EP cargo types |
| **RNA Data** | ✅ Extensive | ✅ Moderate |
| **Protein Data** | ❌ No | ✅ 566,911 entries |
| **Lipid Data** | ❌ No | ✅ 3,839 entries |
| **Metabolite Data** | ❌ No | ✅ 192 entries |
| **Projects** | 371 | 3,533 studies |
| **Download** | Individual CSVs | Bulk downloads |

## 🎓 Citation

Chitti, S. V., et al. (2024). Vesiclepedia 2024: an extracellular vesicles and extracellular particles repository. *Nucleic Acids Research*, 52(D1), D1694–D1698.

## ⚡ Next Steps

1. **Test website access**: Verify http://www.microvesicles.org is accessible
2. **Explore download page**: Check available file formats
3. **Download all datasets**: Get proteins, RNA, lipids, metabolites, DNA
4. **Install FunRich** (optional): For advanced analysis and filtering
5. **Compare with EVmiRNA2.0**: Cross-reference miRNA data

## 💡 Key Advantages for Your Research

1. **Protein cargo**: Identify protein markers in EVs
2. **Lipid profiles**: Understand EV membrane composition
3. **Multi-omics integration**: Combine with EVmiRNA2.0 miRNA data
4. **Quality filtering**: Use EV-TRACK scores to select high-quality studies
5. **Functional analysis**: Built-in enrichment analysis tools
