# Disease Information and Demographics in EV miRNA Databases

## Summary of Your Questions

### Q1: Does Vesiclepedia data have disease information?
**YES** - Disease information is present in multiple ways

### Q2: Are 3,481 studies from 3,481 different people?
**NO** - Studies ≠ Individual people. See detailed breakdown below.

### Q3: Do we have demographics information about these people?
**LIMITED** - Very minimal demographic information available

---

## Detailed Answers

### 1. Disease Information in Vesiclepedia ✅

#### Disease Coverage
- **Total studies with disease context**: ~912 out of 3,481 (26%)
- Disease information appears in:
  - `SAMPLE` column (e.g., "Breast cancer cells", "Melanoma cells")
  - `SAMPLE NAME` column (e.g., "Urine - Prostate cancer", "Serum - Brain tumor")
  - `EXPERIMENT DESCRIPTION` column (study titles mentioning disease)

#### Disease Categories Found

**Cancer Studies** (Most Common):
```
- Breast cancer
- Colorectal cancer
- Melanoma
- Ovarian cancer
- Prostate cancer
- Lung cancer
- Brain cancer/Glioma
- Pancreatic cancer
- Gastric cancer
- Bladder cancer
- Leukemia
- Lymphoma
```

**Other Disease Types**:
```
- Cardiovascular: Acute coronary syndrome, stable angina
- Autoimmune: Lupus anticoagulant, systemic lupus erythematosus
- Hematological: Paroxysmal nocturnal hemoglobinuria, acute myeloid leukemia
- Respiratory: Adult respiratory distress syndrome
- Infectious: Prion diseases
- Pregnancy-related: Preeclampsia
```

**Sample Source Examples**:
```bash
# Cancer samples
Serum - Brain tumor
Serum - Papillary adenocarcinoma of ovary
Plasma - Ovarian cancer
Plasma - melanoma
Urine - Prostate cancer
Urine - Lung cancer
Malignant ascites - Colorectal cancer
Pleural Fluid - Breast cancer

# Normal/Control samples
Urine - Normal
Plasma - Normal
Serum - Normal
Saliva - Normal
```

#### Sample Source Classification
- **cl** (cell line): 2,069 studies (59%)
- **ts** (tissue/biofluid): 1,382 studies (40%)
- **cl|ts** (both): 26 studies
- **fl** (fluid): 1 study

**Important**: Many studies use cell lines rather than patient samples, so disease context is experimental, not from actual patients.

---

### 2. Understanding the 3,481 "Studies" vs People

#### What is an "Experiment" in Vesiclepedia?

Each row in `Vesiclepedia_experiment_details.txt` represents a **unique sample/experiment**, NOT a unique person.

**Key Finding**:
- **3,481 experiments** come from only **619 unique publications** (PubMed IDs)
- Average: ~5.6 experiments per publication

#### Why Multiple Experiments per Publication?

One study can have many experiments because:

1. **Multiple Sample Types**
   - Example: Same paper studies plasma, urine, and cell lines

2. **Multiple Cell Lines**
   - Example: Paper tests 5 different cancer cell lines

3. **Multiple Conditions**
   - Example: Treated vs untreated, different time points

4. **Multiple Patient Samples**
   - Example: 10 cancer patients + 10 controls = 20 experiments

5. **Technical Replicates**
   - Same sample, different isolation methods

#### Example Breakdown

**PubMed ID 30089911** has **70 experiments** including:
- Different tissue types
- Different treatment conditions
- Multiple biological replicates

**Single Publication Example**:
```
PubMed: 12626558
Experiments: 3 entries
  - Mast cells (bone marrow-derived)
  - B cells
  - Macrophages
Same study, 3 different cell types = 3 experiments
```

#### How Many Individual People?

**Cannot be determined from Vesiclepedia data alone** because:
- Cell line experiments (59%) don't involve people
- Tissue samples don't specify number of donors
- Patient samples rarely specify individual IDs
- Same patients may contribute multiple samples

**Best Estimate for Human Biofluid Samples**:
- ~1,382 tissue/biofluid experiments
- Subtract cell culture media
- Subtract animal samples
- **Rough estimate**: 500-800 human biofluid samples
- **Individual people**: Likely 200-500 unique individuals (many studies pool samples or use multiple samples per person)

---

### 3. Demographics Information Available

#### In Vesiclepedia: VERY LIMITED ❌

**Available Information**:
- ✅ Species (Human, Mouse, Rat, etc.)
- ✅ Sample type (Plasma, Urine, Cell line, etc.)
- ✅ Disease status (Cancer, Normal, specific diseases)
- ✅ Publication year
- ❌ Age - **NOT AVAILABLE**
- ❌ Sex/Gender - **NOT AVAILABLE**
- ❌ Race/Ethnicity - **NOT AVAILABLE**
- ❌ Geographic location - **NOT AVAILABLE**
- ❌ Individual patient IDs - **NOT AVAILABLE**

**Why No Demographics?**

Vesiclepedia aggregates data from publications that:
1. Often use pooled samples (multiple people combined)
2. Focus on molecular cargo, not patient characteristics
3. Use cell lines (no demographics applicable)
4. Report aggregate findings, not individual-level data

**What You CAN Determine**:
```
Species Distribution:
- Homo sapiens: 2,526 experiments (73%)
- Mus musculus: 492 experiments (14%)
- Rattus norvegicus: 106 experiments (3%)
- Other species: 357 experiments (10%)
```

#### In EVmiRNA2.0: SLIGHTLY BETTER ⚠️

**Metadata Columns Available**:
```
- BioProject
- Run (sample ID)
- EV_type (sEV, exosomes, etc.)
- Source (tissue/cell type)
- disease (disease status)
- Disease_stage/treatment
- Release_date
- URL (PubMed link)
- EV_isolated_method
- Project_Title
- Project_Description
```

**Disease Information** (From 371 projects):
```
Disease Distribution (approximate):
- No disease/Healthy: ~1,789 samples
- Missing/Not specified: ~7,681 samples (many from project descriptions)
- Colorectal cancer: 441 samples
- Prostate cancer: 267 samples
- Ovarian cancer: 203 samples
- Type I diabetes: 195 samples
- Breast cancer: 82 samples
- Gastric cancer: 94 samples
- Parkinson's disease: 315 samples
- Multiple sclerosis: 54 samples
- Hypertension: 102 samples
- Preeclampsia: 75 samples
- And many others...
```

**Sample Disease Examples**:
```csv
Project,        Disease
PRJNA1017860,   Diabetes mellitus
PRJNA1017860,   Healthy donor
PRJNA326271,    - (no disease, cell line study)
```

**Demographics in EVmiRNA2.0**: ALSO LIMITED ❌
- ❌ Age - Rarely specified
- ❌ Sex/Gender - Occasionally mentioned in project descriptions, not systematically
- ❌ Race/Ethnicity - Almost never mentioned
- ⚠️ Disease stage/treatment - Sometimes available in "Disease_stage/treatment" column

---

## What Clinical Information IS Available?

### Vesiclepedia

#### Sample Source Types (Most Detailed Info)
```
Human Biofluids with Disease Context:
- Plasma - Ovarian cancer
- Plasma - Prostate cancer
- Serum - Breast cancer
- Serum - Brain tumor
- Urine - Prostate cancer
- Urine - Lung cancer
- Malignant ascites - Colorectal cancer patient 1/2/3
- Pleural effusions - Breast cancer
- Plasma - Pregnant and not-pregnant women
- Plasma - Acute coronary syndromes
- Plasma - Stable angina
- Serum - Acute myeloid leukemia
```

#### Cancer Cell Lines (Most Common)
```
- MCF-7 (breast cancer)
- HT29, SW480, SW620 (colorectal cancer)
- Me665/1, Mel1 (melanoma)
- BG-1 (ovarian cancer)
- HT1376 (bladder cancer)
- And 100+ more cell lines
```

### EVmiRNA2.0

#### Disease Status
- Systematically captured in "disease" column
- ~1,789 samples labeled "Healthy donor"
- ~441 colorectal cancer samples
- Many disease types represented

#### Treatment/Stage Information
- Available in "Disease_stage/treatment" column
- Often missing or marked "-"
- When present, includes:
  - Treatment regimens
  - Disease stage (early, advanced)
  - Vaccination status
  - Control vs treated

---

## Practical Implications

### For Your Research

#### ✅ What You CAN Do:

1. **Disease Association Studies**
   - Compare EV cargo between disease vs normal samples
   - Identify disease-specific miRNA patterns
   - Use ~500-800 human biofluid experiments from Vesiclepedia
   - Use ~2,000+ disease-specific samples from EVmiRNA2.0

2. **Cancer Biomarker Discovery**
   - Multiple cancer types represented
   - Both cell lines and patient samples available
   - Cross-validate findings across studies

3. **Cross-Disease Comparisons**
   - Compare EV profiles across different diseases
   - Identify disease-specific vs shared markers

4. **Cell Line Studies**
   - 2,069 cell line experiments
   - Controlled conditions
   - Mechanistic studies

#### ❌ What You CANNOT Do:

1. **Demographic-Based Analysis**
   - Cannot stratify by age, sex, race
   - Cannot study population-level patterns
   - Cannot assess demographic disparities

2. **Individual-Level Analysis**
   - No patient identifiers
   - Cannot track same individual over time
   - Cannot link samples to clinical outcomes

3. **Epidemiological Studies**
   - No incidence/prevalence data
   - No geographic distribution
   - No population-representative sampling

4. **Personalized Medicine**
   - Cannot link EV profiles to individual patient characteristics
   - Cannot assess inter-individual variability systematically

---

## Recommendations

### If You Need Demographics:

1. **Contact Original Authors**
   - Use PubMed IDs to find original publications
   - Request de-identified demographic data
   - May require data use agreements

2. **Use Public Repositories**
   - GEO (Gene Expression Omnibus)
   - SRA (Sequence Read Archive)
   - Sometimes have more detailed metadata

3. **Focus on Specific Studies**
   - Identify key studies with clinical cohorts
   - Those may have published demographic tables
   - Supplement database data with literature review

### For Disease-Focused Research:

**Best Approach**:
1. Filter EVmiRNA2.0 by disease column
2. Cross-reference with Vesiclepedia using:
   - Sample type
   - miRNA identifiers
   - Publication year
3. Validate findings across multiple studies
4. Use cell lines for mechanistic validation

**Example Workflow**:
```python
# EVmiRNA2.0: Get colorectal cancer samples
cancer_samples = metadata[metadata['disease'] == 'Colorectal cancer']

# Vesiclepedia: Get colorectal cancer experiments
vesiclepedia_cancer = experiments[
    experiments['SAMPLE'].str.contains('Colorectal cancer', na=False)
]

# Compare miRNA profiles
# Validate with cell line studies
```

---

## Data Quality Summary

| Database | Disease Info | Sample Type | Demographics | Individual IDs |
|----------|--------------|-------------|--------------|----------------|
| **Vesiclepedia** | ⚠️ Partial (26%) | ✅ Detailed | ❌ None | ❌ None |
| **EVmiRNA2.0** | ✅ Good (field provided) | ✅ Good | ❌ Very limited | ❌ None |

---

## Key Takeaways

1. **Disease Information**: ✅ Available in both databases
   - Vesiclepedia: Sample names and descriptions
   - EVmiRNA2.0: Dedicated "disease" column

2. **Study Design**: 3,481 experiments ≠ 3,481 people
   - 619 unique publications
   - ~5.6 experiments per paper
   - Mix of cell lines (59%) and patient samples (40%)
   - Estimated 200-500 unique human individuals (rough estimate)

3. **Demographics**: ❌ Severely Limited
   - No age, sex, race information systematically available
   - Species is the main demographic variable
   - Would need original publications for demographics

4. **Research Value**: Still excellent for:
   - Disease biomarker discovery
   - Molecular characterization
   - Cross-disease comparisons
   - Method development
   - BUT: Not suitable for demographic/population studies

---

## Additional Resources

### To Get More Metadata:

1. **Original Publications**
   - Follow PubMed links in both databases
   - Check supplementary materials
   - Look for patient characteristics tables

2. **GEO/SRA Accessions**
   - Some EVmiRNA2.0 projects link to GEO
   - GEO often has more detailed sample information
   - Example: GSE118720, GSM2208752

3. **Contact Database Curators**
   - Vesiclepedia: http://www.microvesicles.org/contact
   - EVmiRNA2.0: guolab.wchscu.cn (check website for contact)

---

*Document created: November 17, 2025*
*Based on analysis of both downloaded databases*
