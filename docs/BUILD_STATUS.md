# TheraDOS Build Status Matrix

| Subsystem / Capability | Status | Real Implementation | External Provider Required | Tests |
| :--- | :--- | :--- | :--- | :--- |
| **Monorepo & Infra** | COMPLETE | Makefile, Docker Compose, CI workflows | Docker | PASS |
| **Domain Models & DB** | IN_PROGRESS | PostgreSQL (pgvector), Async SQLAlchemy, Alembic | Postgres | Pending |
| **Evidence & Provenance** | PENDING | Immutable records, SHA-256 checksums, Lineage | None | Pending |
| **Entity Resolution** | PENDING | Normalization across HGNC, UniProt, ChEMBL | None | Pending |
| **Triclique Augmentation** | PENDING | Exact triclique enumeration, candidate edge scoring | None | Pending |
| **Evidence Independence** | PENDING | Lineage duplicate penalty $S = \sum q_k \cdot i_k \cdot r_k$ | None | Pending |
| **Causal Hypergraph** | PENDING | Directional sign, cell context, mechanistic events | Neo4j | Pending |
| **Human Causal Genetics** | PENDING | GWAS/QTL colocalization framework | Public data | Pending |
| **Endotype Analysis** | PENDING | Clustering, pathway scoring, stability | None | Pending |
| **Causal Phenotype Inversion** | PENDING | Driver reversal - Harm induction ($CPI$) | None | Pending |
| **Pharmacology & RDKit** | PENDING | Small molecule SMILES, descriptors, AutoDock adapter | Local RDKit / Vina | Pending |
| **Hard Feasibility Gates** | PENDING | Exposure, safety, context direction gates | None | Pending |
| **Hypothesis Compiler** | PENDING | Proof obligations, dossiers, evidence gaps | None | Pending |
| **Adversarial Falsification**| PENDING | Competing mechanisms, falsification dossiers | None | Pending |
| **Pareto Portfolio Engine** | PENDING | Multi-objective non-dominated sorting | None | Pending |
| **Inverse Experiment Designer**| PENDING | Value of Information (VOI) experiment rank | None | Pending |
| **Program Digital Twin** | PENDING | Append-only historical timeline & updates | None | Pending |
| **Model Fabric & Copilot** | PENDING | Provider-neutral registry, grounded citations | OpenAI / Anthropic optional | Pending |
| **Next.js Web Workspace** | PENDING | Therapeutic Program Workspace, Cytoscape, Plotly, 3Dmol | Node.js | Pending |
