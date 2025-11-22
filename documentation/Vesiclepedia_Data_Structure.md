# Vesiclepedia Data Structure Guide

## ✅ Successfully Downloaded Files

All 8 Vesiclepedia data files downloaded (78 MB total):

| File | Size | Records | Description |
|------|------|---------|-------------|
| **Vesiclepedia_protein_mRNA_details.txt** | 33 MB | ~566,911 | Protein and mRNA cargo |
| **Vesiclepedia_gene_details.txt** | 38 MB | ~46,687 | Gene annotations |
| **Vesiclepedia_miRNA_details.txt** | 1.7 MB | ~22,858 | miRNA cargo |
| **Vesiclepedia_experiment_details.txt** | 974 KB | 3,481 | Study/experiment metadata |
| **Vesiclepedia_Proteins_GPAD.txt** | 4.5 MB | - | Gene Ontology annotations (proteins) |
| **Vesiclepedia_RNAs_GPAD.txt** | 539 KB | - | Gene Ontology annotations (RNAs) |
| **Vesiclepedia_lipid_details.txt** | 241 KB | ~3,839 | Lipid cargo |
| **Vesiclepedia_PTM_details.txt** | 4.1 KB | - | Post-translational modifications |

---

## 📊 Data Structure Breakdown

### 1. **Vesiclepedia_experiment_details.txt**

**Purpose**: Master table of all EV studies

**Columns**:
- `EXPERIMENT ID` - Unique study identifier
- `PUBMED ID` - PubMed reference
- `SPECIES` - Organism (Homo sapiens, Mus musculus, etc.)
- `EXPERIMENT DESCRIPTION` - Study description
- `SAMPLE` - Sample type (e.g., plasma, urine, cell culture)
- `SAMPLE SOURCE` - Detailed source information
- `SAMPLE NAME` - Specific sample name
- `IDENTIFICATIONS` - What was identified (Protein|RNA|Lipids)
- `METHODS` - Detection methods used
- `YEAR` - Publication year
- `ISOLATION METHOD` - EV isolation technique
- `VESICLE TYPE` - EV subtype (Exosomes, Ectosomes, etc.)

**Key for analysis**:
- Links experiments to cargo via `EXPERIMENT ID`
- Filter by species, year, or vesicle type
- 3,481 studies from 1983-2023

---

### 2. **Vesiclepedia_protein_mRNA_details.txt** ⭐

**Purpose**: Comprehensive protein and mRNA cargo catalog

**Columns**:
- `CONTENT ID` - Unique cargo identifier
- `CONTENT TYPE` - "protein" or "mrna"
- `ENTREZ GENE ID` - NCBI Gene ID
- `GENE SYMBOL` - Gene name
- `SPECIES` - Organism
- `EXPERIMENT ID` - Links to experiment_details
- `METHODS` - Detection method

**566,911 protein entries**

**Usage**:
```bash
# Find all proteins from human exosomes
grep "Homo sapiens" Vesiclepedia_protein_mRNA_details.txt | \
  grep "protein"

# Get proteins for specific experiment
grep "^.*protein.*161" Vesiclepedia_protein_mRNA_details.txt
```

---

### 3. **Vesiclepedia_miRNA_details.txt** ⭐

**Purpose**: miRNA cargo catalog

**Columns**:
- `CONTENT ID` - Unique ID
- `CONTENT TYPE` - "mirna"
- `MIRNA ID` - miRNA name (e.g., let-7a, miR-21)
- `SPECIES` - Organism
- `EXPERIMENT ID` - Links to experiment
- `METHODS` - Detection method (qPCR, microarray, RNA-seq)
- `Entrez GENE ID` - Gene database ID
- `COMMENTS` - Annotation notes

**22,858 miRNA entries**

**Comparison with EVmiRNA2.0**:
- EVmiRNA2.0: Expression values + metadata for 371 projects
- Vesiclepedia: Presence/absence + methods for 3,481 studies
- **Complementary data sources!**

---

### 4. **Vesiclepedia_gene_details.txt**

**Purpose**: Comprehensive gene annotations

**Columns**:
- `PRIMARY ID` - Internal ID
- `ENTREZ GENE ID` - NCBI Gene ID
- `SPECIES` - Organism
- `GENE SYMBOL` - Gene name
- `GENE NAME` - Full gene name
- `SYNONYMS` - Alternative names
- `HGNC` - HUGO Gene Nomenclature Committee ID
- `MIM` - Mendelian Inheritance in Man ID

**46,687 unique genes**

**Usage**: Look up detailed gene information
- Cross-reference with protein/mRNA data
- Get official gene symbols and synonyms

---

### 5. **Vesiclepedia_lipid_details.txt** ⭐

**Purpose**: Lipid cargo catalog (UNIQUE TO VESICLEPEDIA)

**Columns**:
- `CONTENT ID` - Unique ID
- `CONTENT TYPE` - "lipid"
- `LIPID ID` - Lipid name
- `SPECIES` - Organism
- `EXPERIMENT ID` - Links to experiment
- `METHODS` - Detection method

**3,839 lipid entries**

**Examples**:
- Lysobisphosphatidic acid
- Sphingomyelin (SM)
- Phosphatidylcholine
- Ceramides

**NOT available in EVmiRNA2.0!**

---

### 6. **Vesiclepedia_PTM_details.txt**

**Purpose**: Post-translational modifications

**Columns**:
- `PTM ID` - Modification ID
- `ENTREZ GENE ID` - Gene ID
- `SPECIES` - Organism
- `EXPERIMENT ID` - Study ID
- `METHODS` - Detection method
- `PTM SITE` - Amino acid position
- `PTM RESIDUE` - Amino acid (K, S, T, Y, etc.)
- `PTM TYPE` - Modification type (Ubiquitination, Phosphorylation, etc.)
- `SEQUENCE ACCESSION IDENTIFIER` - Protein ID

**Use case**: Study protein modifications in EVs

---

### 7. **Vesiclepedia_Proteins_GPAD.txt** & **Vesiclepedia_RNAs_GPAD.txt**

**Purpose**: Gene Ontology (GO) annotations in GPAD format

**Use for**:
- Functional enrichment analysis
- Pathway analysis
- GO term associations

**Format**: Standard Gene Product Association Data (GPAD)

---

## 🔗 How Tables Relate

```
Vesiclepedia_experiment_details.txt
         ↓ (EXPERIMENT ID)
         ├─→ Vesiclepedia_protein_mRNA_details.txt
         ├─→ Vesiclepedia_miRNA_details.txt
         ├─→ Vesiclepedia_lipid_details.txt
         └─→ Vesiclepedia_PTM_details.txt

Vesiclepedia_gene_details.txt
         ↑ (ENTREZ GENE ID)
         └─→ All cargo tables
```

---

## 💡 Key Analysis Workflows

### Workflow 1: Find all cargo for a specific study

```bash
# Get experiment ID from PubMed
EXPID=$(grep "34900962" Vesiclepedia_experiment_details.txt | cut -f1)

# Get all proteins
grep "^.*protein.*$EXPID" Vesiclepedia_protein_mRNA_details.txt

# Get all miRNAs
grep "$EXPID" Vesiclepedia_miRNA_details.txt

# Get all lipids
grep "$EXPID" Vesiclepedia_lipid_details.txt
```

### Workflow 2: Find all studies with a specific miRNA

```bash
# Find let-7a across all studies
grep "let-7a" Vesiclepedia_miRNA_details.txt | \
  cut -f5 | sort -u | \
  while read expid; do
    grep "^$expid" Vesiclepedia_experiment_details.txt
  done
```

### Workflow 3: Get all human exosome proteins

```bash
# Get human exosome experiment IDs
grep "Homo sapiens.*Exosomes" Vesiclepedia_experiment_details.txt | \
  cut -f1 > human_exosome_ids.txt

# Get all proteins from these experiments
grep -f human_exosome_ids.txt Vesiclepedia_protein_mRNA_details.txt
```

---

## 📈 Data Statistics

### By Organism (Top 5)
1. **Homo sapiens** - Majority of studies
2. **Mus musculus** - Second most
3. **Drosophila melanogaster**
4. **Rattus norvegicus**
5. **Others** - 52 more species

### By EV Type
- **Exosomes** (30-150 nm) - Most studied
- **Ectosomes/Microvesicles** (100-1000 nm)
- **Apoptotic bodies** (1000-5000 nm)
- **Migrasomes** (500-3000 nm)
- **Exomeres** (< 50 nm)
- **Supermeres** (< 30 nm)

### By Sample Type
252 different sample sources including:
- Blood plasma/serum
- Urine
- Saliva
- Cell culture media
- Milk
- CSF
- Tears
- And many more...

---

## 🆚 Vesiclepedia vs EVmiRNA2.0

| Feature | Vesiclepedia | EVmiRNA2.0 |
|---------|-------------|------------|
| **Studies** | 3,481 | 371 |
| **Focus** | All EV cargo types | miRNA expression |
| **Proteins** | ✅ 566,911 entries | ❌ None |
| **miRNA** | ✅ 22,858 entries (presence/absence) | ✅ Expression values + counts |
| **Lipids** | ✅ 3,839 entries | ❌ None |
| **Metabolites** | ✅ 192 entries | ❌ None |
| **Quantification** | Limited (47 studies) | ✅ All studies |
| **Expression values** | ❌ No | ✅ Yes (TPM + counts) |
| **Sample metadata** | ✅ Extensive | ✅ Good |
| **Data format** | Tab-delimited | CSV |
| **Download** | ✅ Bulk files | Individual project CSVs |

---

## 🎯 Recommended Use Cases

### Use Vesiclepedia for:
1. **Protein markers** - Identify EV-enriched proteins
2. **Lipid profiles** - Study EV membrane composition
3. **Multi-omics** - Integrate proteins, RNA, lipids
4. **Historical data** - Studies from 1983-present
5. **Cross-species** - Compare EVs across 56 organisms
6. **Method validation** - See what methods detected each cargo

### Use EVmiRNA2.0 for:
1. **miRNA expression analysis** - Quantitative values
2. **Differential expression** - Compare conditions
3. **Raw counts** - For statistical analysis
4. **Recent studies** - More up-to-date miRNA data
5. **Normalized data** - TPM values ready for comparison

### Use Both Together for:
1. **Comprehensive EV profiling**
2. **Biomarker discovery** (proteins + miRNAs)
3. **Cross-validation** of miRNA findings
4. **Multi-omics integration**

---

## 📝 File Format

All files are **tab-delimited text** files:
- Easy to import into R, Python, Excel
- Can use `cut`, `grep`, `awk` for quick analysis
- UTF-8 encoding

---

## 💾 Storage Location

```
/Users/yliu/Desktop/Columbia - Biostatistics/Cheng Lab/EV miRNA database/
├── evmirna_data/          # EVmiRNA2.0 data (371 projects × 3 files)
└── vesiclepedia_data/     # Vesiclepedia data (8 comprehensive files)
```

---

## 🚀 Next Steps

1. ✅ Downloaded all Vesiclepedia data files
2. ⏳ Waiting for EVmiRNA2.0 download to complete
3. 📊 Ready for data integration and analysis!

---

## 📚 Citation

When using Vesiclepedia data, cite:

Chitti, S. V., et al. (2024). Vesiclepedia 2024: an extracellular vesicles and extracellular particles repository. *Nucleic Acids Research*, 52(D1), D1694–D1698.
