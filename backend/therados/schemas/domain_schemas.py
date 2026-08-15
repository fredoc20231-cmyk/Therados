from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from therados.models.domain_models import UserRole, EvidenceMaturity, DecisionOutcome

class OrganizationBase(BaseModel):
    name: str
    slug: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationRead(OrganizationBase):
    id: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: str
    display_name: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    status: str
    created_at: datetime
    last_login_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    disease_area: str

class ProjectCreate(ProjectBase):
    organization_id: str

class ProjectRead(ProjectBase):
    id: str
    organization_id: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ProgramBase(BaseModel):
    disease: str
    indication: str
    patient_context: Optional[str] = None
    disease_stage: Optional[str] = None
    treatment_context: Optional[str] = None
    program_objective: str
    constraints: Optional[Dict[str, Any]] = None

class ProgramCreate(ProgramBase):
    project_id: str

class ProgramRead(ProgramBase):
    id: str
    project_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class EvidenceRecordCreate(BaseModel):
    source_name: str
    external_id: Optional[str] = None
    evidence_type: str
    evidence_maturity: EvidenceMaturity = EvidenceMaturity.ASSOCIATIVE
    normalized_payload: Dict[str, Any]
    quality_score: float = 1.0
    is_synthetic: bool = False

class EvidenceRecordRead(BaseModel):
    id: str
    source_id: str
    external_id: Optional[str] = None
    evidence_type: str
    evidence_maturity: EvidenceMaturity
    checksum: str
    quality_score: float
    is_synthetic: bool
    retrieval_timestamp: datetime
    model_config = ConfigDict(from_attributes=True)

class HypothesisBase(BaseModel):
    title: str
    intervention_name: str
    intended_target: str
    intended_action: str
    cellular_context: str
    disease_endotype: str
    genomic_background: Optional[str] = None
    predictive_biomarkers: List[str] = Field(default_factory=list)
    dose_exposure_regime: Optional[str] = None
    schedule_duration: Optional[str] = None
    safety_constraints: Dict[str, Any] = Field(default_factory=dict)

class HypothesisCreate(HypothesisBase):
    program_id: str

class ProofObligationRead(BaseModel):
    id: str
    proposition: str
    required_evidence_type: str
    state: str
    threshold_value: Optional[str] = None
    evidence_references: List[str]
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class AlternativeMechanismRead(BaseModel):
    id: str
    mechanism_name: str
    description: str
    evidence_support: float
    discriminating_assay: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class HypothesisRead(HypothesisBase):
    id: str
    program_id: str
    maturity: EvidenceMaturity
    support_score: float
    status: str
    version: int
    created_at: datetime
    proof_obligations: List[ProofObligationRead] = Field(default_factory=list)
    alternative_mechanisms: List[AlternativeMechanismRead] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)

class CandidateRead(BaseModel):
    id: str
    program_id: str
    name: str
    smiles: Optional[str] = None
    modality: str
    primary_target: str
    cpi_score: float
    novelty_score: float
    overall_status: str
    molecular_weight: Optional[float] = None
    clogp: Optional[float] = None
    safety_gate_passed: bool
    docking_status: str
    docking_score_kcal_mol: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class ExperimentPlanRead(BaseModel):
    id: str
    hypothesis_id: str
    scientific_objective: str
    recommended_assay: str
    biological_model: str
    expected_voi: float
    estimated_cost_usd: float
    estimated_duration_days: int
    advance_threshold: str
    terminate_threshold: str
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DecisionCreate(BaseModel):
    hypothesis_id: str
    outcome: DecisionOutcome
    rationale: str

class DecisionRead(BaseModel):
    id: str
    hypothesis_id: str
    outcome: DecisionOutcome
    rationale: str
    reviewer_id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DigitalTwinSnapshotRead(BaseModel):
    id: str
    program_id: str
    snapshot_index: int
    trigger_event: str
    program_state: Dict[str, Any]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CopilotQueryRequest(BaseModel):
    program_id: str
    query: str

class CopilotQueryResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]]
    confidence: float
    uncertainties: List[str]
