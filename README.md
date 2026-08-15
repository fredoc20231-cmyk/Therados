# TheraDOS (Therapeutic Domain Operating System)

> **TheraDOS** is a provenance-aware therapeutic intelligence operating system that converts heterogeneous biomedical evidence into falsifiable, endotype-specific, safety-constrained, experiment-ready intervention hypotheses.

---

## 🏛 Product Identity & Principles

TheraDOS is **an operating system for therapeutic reasoning and experimental decision-making**.

Its fundamental computational object is the **Therapeutic Intervention Hypothesis**:

$$H = (d, P, A, C, E, G, B, \Delta, \Theta, \Sigma)$$

where:
- $d$: intervention
- $P$: intended target / target set
- $A$: intended target action (e.g. inhibit, activate, degrade)
- $C$: cellular / tissue context
- $E$: disease endotype
- $G$: genomic / pharmacogenomic background
- $B$: predictive / PD biomarkers
- $\Delta$: dose / exposure regime
- $\Theta$: schedule / sequencing
- $\Sigma$: safety, resistance, and evidence constraints

---

## 🔬 Core Scientific Rules

1. **Scientific Truth**: TheraDOS NEVER fabricates binding affinities, p-values, docking scores, gene expression, or trial results. Uncalculated metrics report `Not available` or `Provider not configured`.
2. **Provenance First**: Every claim retains complete lineage to source `EvidenceRecord` items with SHA-256 checksums and source URLs.
3. **Hard Feasibility Gates**: Exposure, safety liabilities, target expression, and action direction are hard gates evaluated before portfolio ranking.
4. **Adversarial Falsification**: Every hypothesis is subjected to competing mechanism evaluations to establish a Falsification Dossier.
5. **Inverse Experiment Design**: Recommends the highest Value-of-Information (VOI) experiment to resolve proof obligations.
6. **Research Use Only**: TheraDOS is therapeutic-development decision-support software, not autonomous medical advice.

---

## 🏗 Architecture Overview

```text
Therados/
├── apps/
│   └── web/                   # Next.js 14+ App Router, Cytoscape.js, Plotly, 3Dmol.js UI
├── backend/                   # FastAPI, SQLAlchemy 2.x, Pydantic v2, PostgreSQL (pgvector)
├── scientific/                # Domain engines: Triclique, CPI, Compiler, Falsification, Portfolio, VOI
├── integrations/              # Public & Provider Adapters (ChEMBL, UniProt, Open Targets, RDKit, LLMs)
├── infrastructure/            # Docker, PostgreSQL, Neo4j, Redis, MinIO, Temporal configuration
└── docs/                      # Architectural & scientific specifications
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+
- Node.js 20+ & npm

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/fredoc20231-cmyk/Therados.git
cd Therados

# 2. Copy environment variables
cp .env.example .env

# 3. Spin up infrastructure services
make infra

# 4. Bootstrap dependencies
make bootstrap

# 5. Run database migrations
make migrate

# 6. Seed synthetic tutorial dataset
make seed

# 7. Start development servers
make dev
```

Visit the application at `http://localhost:3000` and API docs at `http://localhost:8000/docs`.

---

## 🧪 Testing & Verification

```bash
make lint       # Run Ruff and ESLint
make typecheck  # Run mypy and tsc
make test       # Run pytest and frontend unit tests
make verify     # Run all checks
```

---

## 📜 License & Research Use

TheraDOS is released under the MIT License for research and therapeutic development decision support.
