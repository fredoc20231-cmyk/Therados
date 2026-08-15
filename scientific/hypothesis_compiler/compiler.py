"""
Therapeutic Hypothesis Compiler Engine.

Converts a contextual TherapeuticHypothesis into a CompiledHypothesisDossier with typed proof obligations,
evidence requirements, alternative mechanisms, and rule provenance.

Does NOT invent disease-specific thresholds, biomarkers, or false certainty.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import enum

class SourceType(str, enum.Enum):
    RULE_GENERATED = "RULE_GENERATED"
    EVIDENCE_SUPPORTED = "EVIDENCE_SUPPORTED"
    MODEL_SUGGESTED = "MODEL_SUGGESTED"
    HUMAN_ENTERED = "HUMAN_ENTERED"

class ObligationState(str, enum.Enum):
    UNRESOLVED = "UNRESOLVED"
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    NOT_TESTED = "NOT_TESTED"

class HypothesisContext(BaseModel):
    cellular_context: str
    disease_endotype: str
    genomic_background: Optional[str] = None
    predictive_biomarkers: List[str] = Field(default_factory=list)

class ProofObligation(BaseModel):
    id: str
    proposition: str
    required_evidence_type: str
    state: ObligationState = ObligationState.UNRESOLVED
    threshold_value: str = "NOT_SPECIFIED"
    evidence_references: List[str] = Field(default_factory=list)
    source_type: SourceType = SourceType.RULE_GENERATED
    rule_provenance: str

class AlternativeMechanism(BaseModel):
    mechanism_name: str
    description: str
    evidence_status: str = "UNSUPPORTED"
    discriminating_assay: str = "NOT_SPECIFIED"
    source_type: SourceType = SourceType.RULE_GENERATED

class UncertaintyEstimate(BaseModel):
    dimension: str
    status: str = "NOT_ESTIMATED" # NOT_ESTIMATED, ESTIMATED, CALIBRATED, OUT_OF_DOMAIN
    value: Optional[float] = None
    method: str = "Uncalibrated Baseline"
    limitations: Optional[str] = "No empirical calibration model configured"

class CompiledHypothesisDossier(BaseModel):
    hypothesis_id: str
    formal_proposition: str
    context: HypothesisContext
    proof_obligations: List[ProofObligation]
    unresolved_obligations_count: int
    alternative_mechanisms: List[AlternativeMechanism]
    uncertainty_vector: List[UncertaintyEstimate]
    compilation_status: str = "COMPILED"
    provenance_manifest: Dict[str, Any]

class HypothesisCompiler:
    """
    Deterministic rule-based compiler.
    Emits formal proof obligations required to establish a therapeutic hypothesis.
    """

    def compile_hypothesis(
        self,
        hypothesis_id: str,
        intervention: str,
        target: str,
        action: str,
        cellular_context: str,
        disease_endotype: str,
        genomic_background: Optional[str] = None,
        predictive_biomarkers: Optional[List[str]] = None,
        safety_constraints: Optional[Dict[str, Any]] = None,
        existing_evidence: Optional[List[Dict[str, Any]]] = None
    ) -> CompiledHypothesisDossier:
        biomarkers = predictive_biomarkers or []
        evidence = existing_evidence or []

        context = HypothesisContext(
            cellular_context=cellular_context,
            disease_endotype=disease_endotype,
            genomic_background=genomic_background,
            predictive_biomarkers=biomarkers
        )

        formal_proposition = (
            f"Therapeutic intervention '{intervention}' targeting '{target}' via '{action}' "
            f"in cellular context '{cellular_context}' for endotype '{disease_endotype}' "
            f"will produce clinically decisive driver pathway reversal."
        )

        # Deterministic generic proof obligations
        obligations: List[ProofObligation] = []

        # PO-1: Target Expression
        po1_supported = any(
            e.get("predicate") == "expressed_in" and e.get("object") == cellular_context
            for e in evidence
        )
        obligations.append(ProofObligation(
            id="PO-01",
            proposition=f"Target '{target}' expression is demonstrated in disease context '{cellular_context}'",
            required_evidence_type="Omics / Target Expression",
            state=ObligationState.SUPPORTED if po1_supported else ObligationState.UNRESOLVED,
            threshold_value="Context expression established" if po1_supported else "NOT_SPECIFIED",
            evidence_references=[e.get("id") for e in evidence if e.get("predicate") == "expressed_in"],
            source_type=SourceType.RULE_GENERATED,
            rule_provenance="Rule-01: Target Context Expression Requirement"
        ))

        # PO-2: Direction of Effect & Pathway Reversal
        po2_supported = any(
            e.get("predicate") in ["inhibits", "activates", "degrades"] and e.get("object") == target
            for e in evidence
        )
        obligations.append(ProofObligation(
            id="PO-02",
            proposition=f"Action '{action}' on target '{target}' directionally mediates driver pathway reversal",
            required_evidence_type="Causal / Perturbation Assay",
            state=ObligationState.SUPPORTED if po2_supported else ObligationState.UNRESOLVED,
            threshold_value="Directional benefit established" if po2_supported else "NOT_SPECIFIED",
            evidence_references=[e.get("id") for e in evidence if e.get("predicate") in ["inhibits", "activates", "degrades"]],
            source_type=SourceType.RULE_GENERATED,
            rule_provenance="Rule-02: Direction of Effect Requirement"
        ))

        # PO-3: Target Engagement
        po3_supported = any(
            e.get("predicate") == "binds" and e.get("subject") == intervention
            for e in evidence
        )
        obligations.append(ProofObligation(
            id="PO-03",
            proposition=f"Intervention '{intervention}' achieves selective target engagement on '{target}'",
            required_evidence_type="Biophysical / Binding Assay",
            state=ObligationState.SUPPORTED if po3_supported else ObligationState.UNRESOLVED,
            threshold_value="Target engagement established" if po3_supported else "NOT_SPECIFIED",
            evidence_references=[e.get("id") for e in evidence if e.get("predicate") == "binds"],
            source_type=SourceType.RULE_GENERATED,
            rule_provenance="Rule-03: Biophysical Target Engagement Requirement"
        ))

        # PO-4: Exposure Feasibility
        obligations.append(ProofObligation(
            id="PO-04",
            proposition=f"In vivo free exposure of '{intervention}' satisfies target inhibition concentration",
            required_evidence_type="PK / Pharmacokinetics / Exposure",
            state=ObligationState.UNRESOLVED,
            threshold_value="NOT_SPECIFIED",
            evidence_references=[],
            source_type=SourceType.RULE_GENERATED,
            rule_provenance="Rule-04: Exposure Feasibility Requirement"
        ))

        # PO-5: Safety Feasibility
        obligations.append(ProofObligation(
            id="PO-05",
            proposition=f"Intervention '{intervention}' satisfies cardiac, hepatic, and genotoxicity safety limits",
            required_evidence_type="Safety / Cytotoxicity Assay",
            state=ObligationState.UNRESOLVED,
            threshold_value="NOT_SPECIFIED",
            evidence_references=[],
            source_type=SourceType.RULE_GENERATED,
            rule_provenance="Rule-05: Hard Safety Feasibility Requirement"
        ))

        unresolved_count = sum(1 for po in obligations if po.state == ObligationState.UNRESOLVED)

        # Alternative Mechanisms for Adversarial Falsification
        alternatives = [
            AlternativeMechanism(
                mechanism_name="Off-Target Cytotoxicity",
                description=f"Apparent phenotypic benefit of '{intervention}' is mediated by off-target activity rather than selective '{target}' engagement.",
                evidence_status="UNSUPPORTED",
                discriminating_assay=f"Target-knockout rescue assay or '{target}'-resistant mutant allele overexpression",
                source_type=SourceType.RULE_GENERATED
            ),
            AlternativeMechanism(
                mechanism_name="Compensatory Signaling Bypass",
                description=f"Inhibition of '{target}' leads to rapid feedback upregulation of alternative survival signaling pathways.",
                evidence_status="UNSUPPORTED",
                discriminating_assay="Phospho-proteomics time-course signaling cascade assay",
                source_type=SourceType.RULE_GENERATED
            )
        ]

        # Multidimensional Uncertainty Vector with explicit estimation statuses
        uncertainties = [
            UncertaintyEstimate(dimension="evidence_uncertainty", status="NOT_ESTIMATED", value=None),
            UncertaintyEstimate(dimension="causal_uncertainty", status="NOT_ESTIMATED", value=None),
            UncertaintyEstimate(dimension="biological_context_uncertainty", status="NOT_ESTIMATED", value=None),
            UncertaintyEstimate(dimension="structural_uncertainty", status="NOT_ESTIMATED", value=None),
            UncertaintyEstimate(dimension="potency_uncertainty", status="NOT_ESTIMATED", value=None),
            UncertaintyEstimate(dimension="exposure_uncertainty", status="NOT_ESTIMATED", value=None),
            UncertaintyEstimate(dimension="safety_uncertainty", status="NOT_ESTIMATED", value=None),
            UncertaintyEstimate(dimension="endotype_uncertainty", status="NOT_ESTIMATED", value=None)
        ]

        manifest = {
            "compiler_version": "TheraDOS Deterministic Compiler v2.0",
            "rule_set": "TheraDOS Governance Ruleset v1.0",
            "evidence_items_evaluated": len(evidence),
            "disclaimer": "Rule-generated proof obligations require experimental and clinical verification."
        }

        return CompiledHypothesisDossier(
            hypothesis_id=hypothesis_id,
            formal_proposition=formal_proposition,
            context=context,
            proof_obligations=obligations,
            unresolved_obligations_count=unresolved_count,
            alternative_mechanisms=alternatives,
            uncertainty_vector=uncertainties,
            compilation_status="COMPILED",
            provenance_manifest=manifest
        )
