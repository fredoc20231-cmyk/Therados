# Canonical Data Model Specification

All entities use UUID v4 or v7 primary keys.

## Core Entities
1. `Organization`: Multi-tenant organization boundaries.
2. `User` & `Membership`: RBAC roles (`viewer`, `scientist`, `reviewer`, `admin`).
3. `Project`: Research project container.
4. `TherapeuticProgram`: Indication/disease program (e.g. Platinum-resistant HGSOC).
5. `BiologicalEntity`: Typed entities (`Drug`, `Compound`, `Gene`, `Target`, `Disease`, `Endotype`, `CellType`, `Pathway`).
6. `EvidenceSource` & `EvidenceRecord`: Immutable records with source URL, checksum, provenance.
7. `EvidenceClaim`: Subject-Predicate-Object claims with direction, sign, and evidence maturity.
8. `TherapeuticHypothesis`: Contextual hypothesis $H = (d, P, A, C, E, G, B, \Delta, \Theta, \Sigma)$.
9. `ProofObligation`: Propositional requirement for hypothesis advancement.
10. `AlternativeMechanism`: Competing hypothesis used for adversarial falsification.
11. `CandidateIntervention`: Approved or novel compound/modality.
12. `ExperimentPlan` & `ExperimentRun`: Structured experimental protocol and result.
13. `Decision`: ADVANCE, HOLD, REDESIGN, TERMINATE, or INSUFFICIENT_EVIDENCE.
14. `TherapeuticProgramDigitalTwin`: Persistent, append-only historical timeline of program state.
