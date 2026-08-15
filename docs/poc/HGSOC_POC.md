# THERADOS-POC-001: Platinum-Resistant High-Grade Serous Ovarian Cancer Therapeutic Discovery Program

## 1. Scientific Objective
The **THERADOS-POC-001** research discovery program evaluates therapeutic interventions and target strategies for platinum-resistant High-Grade Serous Ovarian Carcinoma (HGSOC) through independent biomedical evidence, endotype context, causal genetics, pharmacologic feasibility, hard safety gates, adversarial falsification, and Value-of-Information (VOI) experiment design.

> **Disclaimer**: THERADOS-POC-001 is a research discovery program and decision support framework. It is NOT intended as autonomous medical advice or patient treatment recommendations.

---

## 2. Program Configuration (`configs/programs/hgsoc_platinum_resistant.yaml`)
- **Program ID**: `THERADOS-POC-001`
- **Disease Area**: High-Grade Serous Ovarian Carcinoma (`DOID:4030`)
- **Therapeutic Setting**: Platinum-Resistant Recurrent HGSOC
- **Project Mode**: `REAL` (Synthetic tutorial data strictly prohibited)
- **Primary Cellular Context**: HGSOC High-Grade Epithelial Tumor Cell
- **Safety Context Tissues**: Fallopian Tube Epithelium, Normal Cardiac Ventricular Myocytes, Human Primary Hepatocytes, Hematopoietic Stem Cells

---

## 3. Public Data Provider Integration
Official public APIs and adapters integrated into the discovery run:
1. **Open Targets Platform API** (`https://api.platform.opentargets.org/api/v4/graphql`): Disease EFO `EFO_0005537` target association scores.
2. **ChEMBL Bioactivity API** (`https://www.ebi.ac.uk/chembl/api/data`): Target IC50/Ki bioactivities (e.g. `CHEMBL3834` PKMYT1).
3. **UniProt REST API**: Protein annotations and human gene symbols.
4. **PubChem PUG REST API**: Small-molecule SMILES structures and molecular weight.
5. **ClinicalTrials.gov API v2**: Clinical trial status and terminated/failed program evidence.
6. **NCBI PubMed E-utilities API**: Literature PMID citations and lineage.

Every discovery run generates an immutable `DataSnapshotManifest` with SHA-256 payload checksums for complete auditability.

---

## 4. Endotype Clustering & Resistance Profile
### Endotype Subtypes
- **`END-HGSOC-01`**: Platinum-Resistant Homologous Recombination Proficient (HRP) / CCNE1-Amplified
  - *Drivers*: CCNE1 Amplification, NOTCH signaling, PI3K/AKT
  - *Prevalence*: 45%
  - *Stability Score*: 0.88
- **`END-HGSOC-02`**: BRCA-Mutant PARP-Resistant Secondary Reversion
  - *Drivers*: BRCA1/2 Reversion, ABCB1 Multi-Drug Efflux
  - *Prevalence*: 30%
  - *Stability Score*: 0.82
- **`END-HGSOC-03`**: Immune-Excluded High-Stroma Fibrotic
  - *Drivers*: TGF-beta Signaling, ECM Remodeling, VEGF Pathway
  - *Prevalence*: 25%
  - *Stability Score*: 0.79

### Resistance Mechanisms
1. `RES-01`: CCNE1 Amplification & High Cyclin E1 Drive (Replication stress dependency on S/G2 checkpoint kinases PKMYT1/WEE1)
2. `RES-02`: BRCA1/2 Secondary Reversion Mutations (Homologous recombination repair restoration)
3. `RES-03`: ABCB1 / MDR1 Transporter Overexpression (Paclitaxel and small molecule drug efflux)
4. `RES-04`: TGF-beta Driven Fibrotic Stroma (Immune exclusion)

---

## 5. Candidate Generation Ensemble & Origins
Candidates are generated across multiple independent routes:
- **`MaximalTricliqueAugmentationEngine`**: 3-partite maximal tricliques on $D \times P \times E$ graph.
- **`NeighborhoodCompletionBaseline`**: 2-hop graph neighborhood completion.
- **`OPEN_TARGETS`**: Target-disease association score $>0.80$.
- **`ENDOTYPE_DRIVER`**: Target dependency in specific endotype (e.g., CCNE1-Amp PKMYT1 dependency).

Each candidate records its origins in `candidate_origins[]`.

---

## 6. Hard Feasibility Gates
Candidates undergo strict feasibility evaluation:
1. **Direction of Effect**: Must be directionally beneficial.
2. **Target Context Expression**: Must be expressed in HGSOC tumor cells.
3. **Free Exposure Feasibility**: $C_{\text{free}} \ge \text{IC}_{50}$.
4. **Cardiac & Genotoxicity Liabilities**: hERG HIGH or Genotoxicity HIGH results in fatal `REJECTED_BY_FATAL_GATE`.

---

## 7. Portfolio & Value of Information (VOI)
- **Feasible Pareto Frontier**: Candidates passing hard safety gates are ranked across CPI score, novelty, and safety without single-score compression.
- **Value of Information**: The Inverse Experiment Designer calculates VOI score to select the most decisive discriminating experiment (e.g., 3D Spheroid Organoid Viability Assay).
- **Temporal Retrospective Validation**: Evidence published after cutoff date (e.g., `2022-01-01`) is strictly hidden during candidate generation to evaluate holdout target recovery hit-rate.

---

## 8. Reproducibility
Every run produces a locked `AnalysisRun` with `run_id`, `git_sha`, configuration checksum, and manifest ID.
