import uuid
from datetime import datetime, timezone
from typing import Optional, Any, Dict, List
from sqlalchemy import (
    String, Text, Boolean, Float, Integer, DateTime, ForeignKey, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from therados.db.session import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class UserRole(str, enum.Enum):
    VIEWER = "viewer"
    SCIENTIST = "scientist"
    REVIEWER = "reviewer"
    ADMIN = "admin"

class EvidenceMaturity(str, enum.Enum):
    ASSOCIATIVE = "associative"
    STRUCTURALLY_INFERRED = "structurally_inferred"
    MECHANISTICALLY_SUPPORTED = "mechanistically_supported"
    CAUSALLY_CORROBORATED = "causally_corroborated"
    EXPERIMENTALLY_VALIDATED = "experimentally_validated"
    CLINICALLY_ESTABLISHED = "clinically_established"

class DecisionOutcome(str, enum.Enum):
    ADVANCE = "ADVANCE"
    HOLD = "HOLD"
    REDESIGN = "REDESIGN"
    TERMINATE = "TERMINATE"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"

# --- ORGANIZATION & AUTH ---

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    memberships: Mapped[List["Membership"]] = relationship("Membership", back_populates="organization", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="organization", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    memberships: Mapped[List["Membership"]] = relationship("Membership", back_populates="user", cascade="all, delete-orphan")

class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    organization_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.SCIENTIST, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="memberships")
    user: Mapped["User"] = relationship("User", back_populates="memberships")

# --- PROJECTS & PROGRAMS ---

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    organization_id: Mapped[str] = mapped_column(String, ForeignKey("organizations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disease_area: Mapped[str] = mapped_column(String, nullable=False)
    created_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="projects")
    programs: Mapped[List["TherapeuticProgram"]] = relationship("TherapeuticProgram", back_populates="project", cascade="all, delete-orphan")

class TherapeuticProgram(Base):
    __tablename__ = "therapeutic_programs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    disease: Mapped[str] = mapped_column(String, nullable=False)
    indication: Mapped[str] = mapped_column(String, nullable=False)
    patient_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disease_stage: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    treatment_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    program_objective: Mapped[str] = mapped_column(Text, nullable=False)
    constraints: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    project: Mapped["Project"] = relationship("Project", back_populates="programs")
    hypotheses: Mapped[List["TherapeuticHypothesis"]] = relationship("TherapeuticHypothesis", back_populates="program", cascade="all, delete-orphan")
    digital_twins: Mapped[List["DigitalTwinSnapshot"]] = relationship("DigitalTwinSnapshot", back_populates="program", cascade="all, delete-orphan")

# --- BIOLOGICAL ENTITIES & PROVENANCE ---

class BiologicalEntity(Base):
    __tablename__ = "biological_entities"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    entity_type: Mapped[str] = mapped_column(String, nullable=False, index=True) # Drug, Compound, Target, Gene, Disease, Endotype, CellType, Pathway
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    canonical_symbol: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    aliases: Mapped[List["EntityAlias"]] = relationship("EntityAlias", back_populates="entity", cascade="all, delete-orphan")
    identifiers: Mapped[List["EntityIdentifier"]] = relationship("EntityIdentifier", back_populates="entity", cascade="all, delete-orphan")

class EntityAlias(Base):
    __tablename__ = "entity_aliases"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    entity_id: Mapped[str] = mapped_column(String, ForeignKey("biological_entities.id"), nullable=False)
    alias: Mapped[str] = mapped_column(String, nullable=False, index=True)

    entity: Mapped["BiologicalEntity"] = relationship("BiologicalEntity", back_populates="aliases")

class EntityIdentifier(Base):
    __tablename__ = "entity_identifiers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    entity_id: Mapped[str] = mapped_column(String, ForeignKey("biological_entities.id"), nullable=False)
    namespace: Mapped[str] = mapped_column(String, nullable=False) # HGNC, UniProt, ChEMBL, DOID, PubChem, PubMed
    identifier: Mapped[str] = mapped_column(String, nullable=False, index=True)

    entity: Mapped["BiologicalEntity"] = relationship("BiologicalEntity", back_populates="identifiers")

class EvidenceSource(Base):
    __tablename__ = "evidence_sources"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    source_type: Mapped[str] = mapped_column(String, nullable=False) # PublicDB, Literature, AssayData, OmicsMatrix, Inferred
    version: Mapped[str] = mapped_column(String, default="1.0")
    licensing_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    retrieval_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class EvidenceRecord(Base):
    __tablename__ = "evidence_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    source_id: Mapped[str] = mapped_column(String, ForeignKey("evidence_sources.id"), nullable=False)
    external_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    evidence_type: Mapped[str] = mapped_column(String, nullable=False)
    evidence_maturity: Mapped[EvidenceMaturity] = mapped_column(SQLEnum(EvidenceMaturity), default=EvidenceMaturity.ASSOCIATIVE)
    raw_payload_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    normalized_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    checksum: Mapped[str] = mapped_column(String, nullable=False) # SHA-256
    retrieval_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    quality_score: Mapped[float] = mapped_column(Float, default=1.0) # q_k
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class EvidenceClaim(Base):
    __tablename__ = "evidence_claims"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    evidence_record_id: Mapped[str] = mapped_column(String, ForeignKey("evidence_records.id"), nullable=False)
    subject_entity_id: Mapped[str] = mapped_column(String, ForeignKey("biological_entities.id"), nullable=False)
    predicate: Mapped[str] = mapped_column(String, nullable=False) # binds, inhibits, activates, promotes, drives, causes
    object_entity_id: Mapped[str] = mapped_column(String, ForeignKey("biological_entities.id"), nullable=False)
    direction: Mapped[str] = mapped_column(String, default="increases") # increases, decreases, neutral
    sign: Mapped[int] = mapped_column(Integer, default=1) # +1, -1, 0
    context: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict) # tissue, cell_type, disease
    evidence_maturity: Mapped[EvidenceMaturity] = mapped_column(SQLEnum(EvidenceMaturity), default=EvidenceMaturity.ASSOCIATIVE)
    support_score: Mapped[float] = mapped_column(Float, default=0.5)
    provenance_chain: Mapped[List[str]] = mapped_column(JSON, default=list)

class EvidenceLineage(Base):
    __tablename__ = "evidence_lineages"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    parent_record_id: Mapped[str] = mapped_column(String, ForeignKey("evidence_records.id"), nullable=False)
    child_record_id: Mapped[str] = mapped_column(String, ForeignKey("evidence_records.id"), nullable=False)
    transformation_notes: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class GraphSnapshot(Base):
    __tablename__ = "graph_snapshots"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    program_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_programs.id"), nullable=False)
    node_count: Mapped[int] = mapped_column(Integer, default=0)
    edge_count: Mapped[int] = mapped_column(Integer, default=0)
    triclique_candidates: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

# --- HYPOTHESIS & FALSIFICATION ---

class TherapeuticHypothesis(Base):
    __tablename__ = "therapeutic_hypotheses"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    program_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_programs.id"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    intervention_name: Mapped[str] = mapped_column(String, nullable=False) # d
    intended_target: Mapped[str] = mapped_column(String, nullable=False) # P
    intended_action: Mapped[str] = mapped_column(String, nullable=False) # A (inhibit, activate, degrade)
    cellular_context: Mapped[str] = mapped_column(String, nullable=False) # C
    disease_endotype: Mapped[str] = mapped_column(String, nullable=False) # E
    genomic_background: Mapped[Optional[str]] = mapped_column(String, nullable=True) # G
    predictive_biomarkers: Mapped[List[str]] = mapped_column(JSON, default=list) # B
    dose_exposure_regime: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Δ
    schedule_duration: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Θ
    safety_constraints: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict) # Σ
    maturity: Mapped[EvidenceMaturity] = mapped_column(SQLEnum(EvidenceMaturity), default=EvidenceMaturity.ASSOCIATIVE)
    support_score: Mapped[float] = mapped_column(Float, default=0.5)
    status: Mapped[str] = mapped_column(String, default="proposed") # proposed, compiled, falsified, advanced, terminated
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    program: Mapped["TherapeuticProgram"] = relationship("TherapeuticProgram", back_populates="hypotheses")
    versions: Mapped[List["HypothesisVersion"]] = relationship("HypothesisVersion", back_populates="hypothesis", cascade="all, delete-orphan")
    proof_obligations: Mapped[List["ProofObligation"]] = relationship("ProofObligation", back_populates="hypothesis", cascade="all, delete-orphan")
    alternative_mechanisms: Mapped[List["AlternativeMechanism"]] = relationship("AlternativeMechanism", back_populates="hypothesis", cascade="all, delete-orphan")
    decisions: Mapped[List["Decision"]] = relationship("Decision", back_populates="hypothesis", cascade="all, delete-orphan")

class HypothesisVersion(Base):
    __tablename__ = "hypothesis_versions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    hypothesis_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_hypotheses.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    serialized_dossier: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    hypothesis: Mapped["TherapeuticHypothesis"] = relationship("TherapeuticHypothesis", back_populates="versions")

class ProofObligation(Base):
    __tablename__ = "proof_obligations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    hypothesis_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_hypotheses.id"), nullable=False)
    proposition: Mapped[str] = mapped_column(Text, nullable=False)
    required_evidence_type: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, default="unresolved") # unresolved, supported, contradicted, not_tested
    threshold_value: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    evidence_references: Mapped[List[str]] = mapped_column(JSON, default=list)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    hypothesis: Mapped["TherapeuticHypothesis"] = relationship("TherapeuticHypothesis", back_populates="proof_obligations")

class AlternativeMechanism(Base):
    __tablename__ = "alternative_mechanisms"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    hypothesis_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_hypotheses.id"), nullable=False)
    mechanism_name: Mapped[str] = mapped_column(String, nullable=False) # e.g. off-target toxicity, reactive pathway
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_support: Mapped[float] = mapped_column(Float, default=0.2)
    discriminating_assay: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default="active")

    hypothesis: Mapped["TherapeuticHypothesis"] = relationship("TherapeuticHypothesis", back_populates="alternative_mechanisms")

# --- CANDIDATES, PHARMACOLOGY, SAFETY ---

class CandidateIntervention(Base):
    __tablename__ = "candidate_interventions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    program_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_programs.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    smiles: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    modality: Mapped[str] = mapped_column(String, default="small_molecule") # small_molecule, antibody, degrader, peptide
    primary_target: Mapped[str] = mapped_column(String, nullable=False)
    cpi_score: Mapped[float] = mapped_column(Float, default=0.0) # Causal Phenotype Inversion
    novelty_score: Mapped[float] = mapped_column(Float, default=0.5)
    overall_status: Mapped[str] = mapped_column(String, default="HOLD") # ADVANCE, HOLD, REDESIGN, TERMINATE
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    pharmacology: Mapped[Optional["PharmacologyAssessment"]] = relationship("PharmacologyAssessment", uselist=False, cascade="all, delete-orphan")
    safety: Mapped[Optional["SafetyAssessment"]] = relationship("SafetyAssessment", uselist=False, cascade="all, delete-orphan")

class PharmacologyAssessment(Base):
    __tablename__ = "pharmacology_assessments"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    candidate_id: Mapped[str] = mapped_column(String, ForeignKey("candidate_interventions.id"), nullable=False)
    molecular_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    clogp: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    h_bond_donors: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    h_bond_acceptors: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tpsa: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rotatable_bonds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    rule_of_five_violations: Mapped[int] = mapped_column(Integer, default=0)
    binding_affinity_nm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    docking_score_kcal_mol: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    docking_status: Mapped[str] = mapped_column(String, default="Provider not configured")

class SafetyAssessment(Base):
    __tablename__ = "safety_assessments"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    candidate_id: Mapped[str] = mapped_column(String, ForeignKey("candidate_interventions.id"), nullable=False)
    herg_liability: Mapped[str] = mapped_column(String, default="UNEVALUATED") # LOW, MEDIUM, HIGH, UNEVALUATED
    hepatotoxicity_liability: Mapped[str] = mapped_column(String, default="UNEVALUATED")
    genotoxicity_liability: Mapped[str] = mapped_column(String, default="UNEVALUATED")
    safety_gate_passed: Mapped[bool] = mapped_column(Boolean, default=True)
    failure_reasons: Mapped[List[str]] = mapped_column(JSON, default=list)

class UncertaintyVector(Base):
    __tablename__ = "uncertainty_vectors"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    entity_id: Mapped[str] = mapped_column(String, nullable=False, index=True) # hypothesis_id or candidate_id
    evidence_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)
    causal_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)
    biological_context_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)
    structural_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)
    potency_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)
    exposure_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)
    safety_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)
    endotype_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)
    experimental_uncertainty: Mapped[float] = mapped_column(Float, default=0.5)

# --- EXPERIMENTS, DECISIONS & DIGITAL TWIN ---

class ExperimentPlan(Base):
    __tablename__ = "experiment_plans"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    hypothesis_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_hypotheses.id"), nullable=False)
    scientific_objective: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_assay: Mapped[str] = mapped_column(String, nullable=False)
    biological_model: Mapped[str] = mapped_column(String, nullable=False)
    expected_voi: Mapped[float] = mapped_column(Float, default=0.7) # Value of Information
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=5000.0)
    estimated_duration_days: Mapped[int] = mapped_column(Integer, default=14)
    protocol_details: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    advance_threshold: Mapped[str] = mapped_column(String, nullable=False)
    terminate_threshold: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="planned") # planned, running, completed, cancelled
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    runs: Mapped[List["ExperimentRun"]] = relationship("ExperimentRun", back_populates="plan", cascade="all, delete-orphan")

class ExperimentRun(Base):
    __tablename__ = "experiment_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    plan_id: Mapped[str] = mapped_column(String, ForeignKey("experiment_plans.id"), nullable=False)
    executed_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    run_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    raw_data_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    summary_result: Mapped[str] = mapped_column(String, nullable=False) # positive, negative, inconclusive
    measured_values: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    plan: Mapped["ExperimentPlan"] = relationship("ExperimentPlan", back_populates="runs")

class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    hypothesis_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_hypotheses.id"), nullable=False)
    outcome: Mapped[DecisionOutcome] = mapped_column(SQLEnum(DecisionOutcome), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    supporting_evidence_ids: Mapped[List[str]] = mapped_column(JSON, default=list)
    contradicting_evidence_ids: Mapped[List[str]] = mapped_column(JSON, default=list)
    reviewer_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    hypothesis: Mapped["TherapeuticHypothesis"] = relationship("TherapeuticHypothesis", back_populates="decisions")

class DigitalTwinSnapshot(Base):
    __tablename__ = "digital_twin_snapshots"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    program_id: Mapped[str] = mapped_column(String, ForeignKey("therapeutic_programs.id"), nullable=False)
    snapshot_index: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_event: Mapped[str] = mapped_column(String, nullable=False)
    program_state: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    program: Mapped["TherapeuticProgram"] = relationship("TherapeuticProgram", back_populates="digital_twins")

# --- MODEL FABRIC & AUDIT ---

class ModelProvider(Base):
    __tablename__ = "model_providers"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    provider_name: Mapped[str] = mapped_column(String, nullable=False, unique=True) # OpenAI, Anthropic, Gemini, RDKit, AutoDock
    is_configured: Mapped[bool] = mapped_column(Boolean, default=False)
    status_reason: Mapped[str] = mapped_column(String, default="Healthy")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class ModelRun(Base):
    __tablename__ = "model_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    provider_name: Mapped[str] = mapped_column(String, nullable=False)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    prompt_template_version: Mapped[str] = mapped_column(String, default="1.0")
    inputs: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    outputs: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
