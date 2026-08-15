# System Architecture Specification

## Monorepo Architecture
TheraDOS is built as a production-oriented modular monorepo.

```text
Therados/
├── apps/
│   └── web/                    # Next.js 14+ App Router Client Application
├── backend/                    # FastAPI Core REST API & Workflows
│   ├── therados/
│   │   ├── main.py
│   │   ├── config/             # Environment & System Settings
│   │   ├── db/                 # PostgreSQL & Neo4j Connections
│   │   ├── models/             # SQLAlchemy ORM Models
│   │   ├── schemas/            # Pydantic Schemas
│   │   ├── api/                # REST Endpoints (/api/v1/...)
│   │   ├── services/           # Application Services
│   │   ├── workflows/          # Temporal Workflows
│   │   └── observability/      # Logging & Audit
├── scientific/                 # Core Domain Engines
│   ├── evidence/               # Evidence Ingestion & Independence
│   ├── graphs/                 # Multipartite Graph & Triclique Engine
│   ├── genetics/               # Causal Genetics & Colocalization
│   ├── endotypes/              # Endotype Clustering & Pathway Scoring
│   ├── phenotype_inversion/    # CPI Engine
│   ├── pharmacology/           # RDKit, Docking, Exposure & Safety
│   ├── hypothesis_compiler/    # Compiler & Proof Obligations
│   ├── falsification/          # Adversarial Falsification Dossier Engine
│   ├── portfolio/              # Multi-objective Pareto Ranking
│   ├── experiments/            # Inverse Experiment Designer (VOI)
│   └── digital_twin/           # Program Digital Twin Timeline
├── integrations/               # External Providers & Public Data
│   ├── public_data/            # Open Targets, ChEMBL, UniProt
│   ├── model_providers/        # OpenAI, Anthropic, Local LLMs
│   └── molecular_tools/        # AutoDock Vina, RDKit Adapters
```

## Datastores
- **PostgreSQL 16 (pgvector)**: Canonical system of record for organizations, users, projects, evidence records, hypotheses, proof obligations, candidate interventions, experiment plans, and digital twin state snapshots.
- **Neo4j 5**: Graph datastore representing causal hypergraphs, entity relationships, subgraphs, and triclique neighborhoods.
- **Redis 7**: Ephemeral cache and task queue state.
- **MinIO / AWS S3**: Object storage for raw uploaded files, dataset matrices, and docking structures.
- **Temporal**: Workflow orchestrator for long-running ingestion, docking, graph computation, and compiler jobs.
