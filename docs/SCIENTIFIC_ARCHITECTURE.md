# Scientific Architecture Specification

TheraDOS maps to **5 Scientific Layers** and **4 Cross-Cutting Fabrics**.

## 5 Scientific Layers

### Layer I — Evidence
1. Evidence Ingestion & Provenance Fabric (immutable records, SHA-256)
2. Entity Resolution (HGNC, UniProt, ChEMBL, DOID)
3. Multipartite Graph Builder
4. Triclique Augmentation Engine (exact triclique candidate inference)
5. Evidence Independence Engine ($S = \sum q_k \cdot i_k \cdot r_k$)

### Layer II — Biological Reasoning
1. Causal Hypergraph (directional signed relationships)
2. Human Causal Genetics Engine (GWAS, pQTL, eQTL)
3. Disease Endotype Engine (transcriptomic/proteomic cluster assignment)
4. Causal Phenotype Inversion ($CPI = \sum \text{driver\_reversal} - \sum \text{harm\_induction}$)
5. Resistance & Evolution Engine (longitudinal target mutation & bypass)

### Layer III — Pharmacology & Therapeutic Design
1. Binding & Functional Feasibility (RDKit, AutoDock Vina adapter)
2. Therapeutic Design Engine (Discover vs Design modes)
3. Selectivity Assessment
4. Exposure & PK Feasibility (free concentration, therapeutic window)
5. Safety Gate (cardiac, hepatic, renal, genotoxic hard gates)
6. Developability & Manufacturability (Rule of 5, TPSA, alerts)

### Layer IV — Decision
1. Therapeutic Hypothesis Compiler ($H \rightarrow$ Dossier with Proof Obligations)
2. Adversarial Falsification Engine (competing mechanisms, Falsification Dossier)
3. Ranking & Portfolio Engine (Pareto non-dominated sorting)
4. Inverse Experiment Designer (Value of Information algorithm)

### Layer V — Translation
1. Biomarker Strategy (responder, PD, safety, target engagement)
2. Translational Evidence
3. Trial Planning Workspace
4. Learning Memory (Digital Twin append-only timeline)
5. Governance & Audit
6. Therapeutic Landscape

---

## 4 Cross-Cutting Fabrics

- **Model Fabric**: Provider-neutral LLM/molecular model orchestration.
- **Uncertainty Fabric**: Multidimensional vector uncertainty quantification.
- **Execution Fabric**: Temporal workflow durable execution.
- **Governance Fabric**: Immutable provenance, RBAC, audit event log.
