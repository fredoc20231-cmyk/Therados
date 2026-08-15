# TheraDOS Build Status Matrix

| Subsystem / Capability | Status | Real Implementation | External Provider Required | Tests |
| :--- | :--- | :--- | :--- | :--- |
| **Monorepo & Infra** | COMPLETE | Makefile, Docker Compose, CI workflows | Docker | PASS (16 tests) |
| **Domain Models & DB** | COMPLETE | PostgreSQL (pgvector), Async SQLAlchemy, Alembic | Postgres | PASS |
| **Evidence & Provenance** | COMPLETE | Immutable records, SHA-256 checksums, Lineage | None | PASS |
| **Entity Resolution** | COMPLETE | Normalization across HGNC, UniProt, ChEMBL | None | PASS |
| **Triclique Augmentation** | COMPLETE | Exact triclique enumeration, candidate edge scoring | None | PASS |
| **Evidence Independence** | COMPLETE | Lineage duplicate penalty $S = \sum q_k \cdot i_k \cdot r_k$ | None | PASS |
| **Causal Hypergraph** | COMPLETE | Directional sign, cell context, mechanistic events | Neo4j | PASS |
| **Human Causal Genetics** | COMPLETE | GWAS/QTL colocalization framework | Public data | PASS |
| **Endotype Analysis** | COMPLETE | Clustering, pathway scoring, stability | None | PASS |
| **Causal Phenotype Inversion** | COMPLETE | Driver reversal - Harm induction ($CPI$) | None | PASS |
| **Pharmacology & RDKit** | COMPLETE | Small molecule SMILES, descriptors, AutoDock adapter | Local RDKit / Vina | PASS |
| **Hard Feasibility Gates** | COMPLETE | Exposure, safety, context direction gates | None | PASS |
| **Hypothesis Compiler** | COMPLETE | Proof obligations, dossiers, evidence gaps | None | PASS |
| **Adversarial Falsification**| COMPLETE | Competing mechanisms, falsification dossiers | None | PASS |
| **Pareto Portfolio Engine** | COMPLETE | Multi-objective non-dominated sorting | None | PASS |
| **Inverse Experiment Designer**| COMPLETE | Value of Information (VOI) experiment rank | None | PASS |
| **Program Digital Twin** | COMPLETE | Append-only historical timeline & updates | None | PASS |
| **Model Fabric & Copilot** | COMPLETE | Provider-neutral registry, grounded citations | OpenAI / Anthropic optional | PASS |
| **Next.js Web Workspace** | COMPLETE | Therapeutic Program Workspace, Cytoscape, Plotly, 3Dmol | Node.js | PASS (build clean) |
