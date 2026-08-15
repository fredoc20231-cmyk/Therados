# AGENTS.md — TheraDOS Agent Governance & Scientific Rules

This document establishes non-negotiable scientific, engineering, and security directives for all automated and human agents operating within the **TheraDOS** codebase.

---

# 1. Core Scientific Rules (Non-Negotiable)

### 1. Scientific Truth
NEVER fabricate publications, database records, binding affinities, docking scores, gene expression, trial results, toxicity results, biomarkers, causal evidence, molecular structures, patient responses, or experimental validation.
If information has not been computed or retrieved, explicitly return `Not available`, `Not evaluated`, or `Provider not configured`.

### 2. Provenance First
Every evidence record must contain: source name, source identifier, source URL, version, retrieval timestamp, evidence type, originating publication/database, transformation history, checksum, confidence status, and parent lineage. Derived results must point back to their inputs.

### 3. Predictions Are Not Facts
Maintain explicit evidentiary categories:
1. Associative
2. Structurally inferred
3. Mechanistically supported
4. Causally corroborated
5. Experimentally validated
6. Clinically established
Never silently promote evidence between levels.

### 4. Probabilities Require Calibration
Do NOT display a value as $P(H|E)$ unless it actually possesses a defensible probabilistic interpretation. Call heuristic scores `support score`, not `probability`.

### 5. Explicit Uncertainty
Record multidimensional uncertainty vectors: evidence, causal, biological-context, structural, potency, exposure, safety, endotype, model, experimental, and OOD uncertainty.

### 6. Abstention Is Valid
When evidence is insufficient, TheraDOS must return:
`INSUFFICIENT EVIDENCE — DO NOT RANK` or `UNRESOLVED — EXPERIMENT REQUIRED`.

### 7. Hard Gates Cannot Be Averaged Away
Do not allow high graph scores to compensate for impossible exposure, catastrophic safety, irrelevant cellular context, absent target expression, or invalid direction-of-effect. Evaluate hard feasibility gates before portfolio ranking.

### 8. Negative Evidence Matters
Separately represent: not tested, tested negative, conflicting evidence, failed validation, discontinued program, and toxicity failure. Absence of evidence is not evidence of absence.

### 9. Research Use Disclaimer
The platform is research and therapeutic-development decision support software, not autonomous medical advice or an autonomous clinical decision system.

---

# 2. Engineering Directives

- Python 3.12+ backend with FastAPI, Pydantic v2, SQLAlchemy 2.x (async), Alembic, PostgreSQL + pgvector, Neo4j, Redis, Temporal.
- Next.js 14+ frontend with TypeScript strict mode, Tailwind CSS, shadcn/ui primitives, TanStack Query, Cytoscape.js, Plotly, 3Dmol.js.
- Type safety: No unhandled `any`, strict type checking on backend and frontend.
- Provider neutrality: Models and tools are replaceable interfaces (Model Fabric).
