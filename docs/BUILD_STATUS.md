# TheraDOS Build Status Matrix

| Subsystem / Capability | Status | Real Implementation | External Provider Required | Tests |
| :--- | :--- | :--- | :--- | :--- |
| **Monorepo & CI/CD** | COMPLETE | Makefile, Docker Compose, GitHub Actions CI workflow | Docker / Node 20 / Python 3.12 | PASS (Green CI) |
| **Domain Models & DB** | FUNCTIONAL_BASELINE | PostgreSQL (pgvector), Async SQLAlchemy 2.x, Alembic migrations | PostgreSQL | PASS (32 tests) |
| **Evidence & Provenance** | FUNCTIONAL_BASELINE | Immutable records, SHA-256 checksums, synthetic tutorial guardrails | None | PASS |
| **Entity Resolution** | FUNCTIONAL_BASELINE | Mapping identifiers across HGNC, UniProt, ChEMBL, PubChem | None | PASS |
| **Maximal Triclique Augmentation** | FUNCTIONAL_BASELINE | Exact 3-partite maximal triclique enumeration & candidate edge inference | None | PASS (Invariants pass) |
| **Evidence Independence** | FUNCTIONAL_BASELINE | Citation duplication penalty $S = \sum q_k \cdot i_k \cdot r_k$ & asymptotic support curve | None | PASS |
| **Causal Hypergraph** | FUNCTIONAL_BASELINE | Directional signed claims & Neo4j graph driver adapter | Neo4j | PASS |
| **Human Causal Genetics** | FUNCTIONAL_BASELINE | Structured CausalGeneticsDossier & conservative maturity states | Public GWAS / QTL | PASS |
| **Endotype Analysis** | FUNCTIONAL_BASELINE | Endotype definitions, prevalence, pathway drivers, and stability tracking | Omics Matrix Provider | PASS |
| **Causal Phenotype Inversion** | FUNCTIONAL_BASELINE | Driver reversal minus harm induction ($CPI = \sum w_i r_i - \sum w_j h_j$) | None | PASS |
| **Pharmacology & RDKit** | FUNCTIONAL_BASELINE | Local RDKit SMILES descriptors, Lipinski Rule of 5, AutoDock Vina Adapter | AutoDock Vina executable | PASS |
| **Hard Feasibility Gates** | FUNCTIONAL_BASELINE | Exposure, toxicity, and direction gates with conservative missing-data semantics | None | PASS (Invariants pass) |
| **Hypothesis Compiler** | FUNCTIONAL_BASELINE | Typed proof obligations, evidence requirements, rule provenance | None | PASS (Invariants pass) |
| **Adversarial Falsification** | FUNCTIONAL_BASELINE | Competing mechanisms, qualitative support states, evidence priority selection | None | PASS (Invariants pass) |
| **Pareto Portfolio Engine** | FUNCTIONAL_BASELINE | Multi-objective non-dominated sorting separating feasible vs incomplete vs fatal gate failures | None | PASS |
| **Inverse Experiment Designer** | FUNCTIONAL_BASELINE | Decision-information framework & exact VOI when quantitative inputs exist | None | PASS |
| **Program Digital Twin** | FUNCTIONAL_BASELINE | Append-only historical state timeline & snapshot updates | None | PASS |
| **Model Fabric & Copilot** | FUNCTIONAL_BASELINE | Provider-neutral registry & grounded copilot citing EvidenceRecord IDs | OpenAI / Anthropic optional | PASS |
| **Next.js Web Workspace** | FUNCTIONAL_BASELINE | Therapeutic Program Workspace, Cytoscape, Plotly, 3Dmol UI | Node.js | PASS (Build clean) |
