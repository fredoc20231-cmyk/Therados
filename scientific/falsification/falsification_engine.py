"""
Adversarial Falsification Engine.

Pits primary therapeutic hypothesis against competing mechanism explanations.
Uses qualitative evidence support states and evidence-priority alternative ranking
to generate a Falsification Dossier and select the decisive discriminating experiment.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import enum

class QualitativeSupportState(str, enum.Enum):
    UNSUPPORTED = "UNSUPPORTED"
    WEAK_SUPPORT = "WEAK_SUPPORT"
    MIXED_EVIDENCE = "MIXED_EVIDENCE"
    SUPPORTED = "SUPPORTED"
    STRONG_SUPPORT = "STRONG_SUPPORT"
    NOT_EVALUATED = "NOT_EVALUATED"

class CompetingMechanism(BaseModel):
    mechanism_id: str
    mechanism_statement: str
    description: str
    provenance: str = "Rule-Generated Competing Hypothesis"
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    contradicting_evidence_ids: List[str] = Field(default_factory=list)
    evidence_status: QualitativeSupportState = QualitativeSupportState.NOT_EVALUATED
    consequence_severity: str = "HIGH"
    discriminating_experiment_candidates: List[str] = Field(default_factory=list)

class FalsificationDossier(BaseModel):
    hypothesis_id: str
    hypothesis_title: str
    competing_mechanisms: List[CompetingMechanism]
    highest_priority_alternative: Optional[CompetingMechanism] = None
    survival_status: str = "UNRESOLVED_COMPETING_MECHANISMS"
    support_comparison_summary: str
    recommended_discriminating_experiment: str
    provenance_notes: str

class AdversarialFalsificationEngine:
    def generate_falsification_dossier(
        self,
        hypothesis_id: str,
        hypothesis_title: str,
        alternative_mechanisms: List[Dict[str, Any]],
        existing_evidence: Optional[List[Dict[str, Any]]] = None
    ) -> FalsificationDossier:
        evidence = existing_evidence or []

        typed_alternatives: List[CompetingMechanism] = []

        for idx, alt in enumerate(alternative_mechanisms):
            m_id = f"ALT-{idx+1:02d}"
            name = str(alt.get("mechanism_name", alt.get("mechanism_statement", f"Alternative Mechanism {idx+1}")))
            desc = str(alt.get("description", "Alternative competing explanation"))
            disc_assay = str(alt.get("discriminating_assay", "Target-knockout or time-course perturbation assay"))

            # Check matching evidence
            sup_ids = [
                e.get("id", "EV-UNKNOWN") for e in evidence
                if (e.get("subject") == name or e.get("object") == name)
                and e.get("predicate") in ["causes_off_target", "supports", "drives", "inhibits", "activates"]
            ]
            con_ids = [
                e.get("id", "EV-UNKNOWN") for e in evidence
                if (e.get("subject") == name or e.get("object") == name)
                and e.get("predicate") in ["rules_out", "contradicts", "refutes"]
            ]

            if sup_ids and not con_ids:
                status = QualitativeSupportState.SUPPORTED
            elif sup_ids and con_ids:
                status = QualitativeSupportState.MIXED_EVIDENCE
            elif con_ids and not sup_ids:
                status = QualitativeSupportState.UNSUPPORTED
            else:
                status = QualitativeSupportState.NOT_EVALUATED

            typed_alternatives.append(CompetingMechanism(
                mechanism_id=m_id,
                mechanism_statement=name,
                description=desc,
                supporting_evidence_ids=sup_ids,
                contradicting_evidence_ids=con_ids,
                evidence_status=status,
                consequence_severity="HIGH",
                discriminating_experiment_candidates=[disc_assay]
            ))

        # Select highest-priority alternative based on evidence status
        status_priority = {
            QualitativeSupportState.STRONG_SUPPORT: 5,
            QualitativeSupportState.SUPPORTED: 4,
            QualitativeSupportState.MIXED_EVIDENCE: 3,
            QualitativeSupportState.NOT_EVALUATED: 2,
            QualitativeSupportState.WEAK_SUPPORT: 1,
            QualitativeSupportState.UNSUPPORTED: 0
        }

        sorted_alts = sorted(
            typed_alternatives,
            key=lambda x: status_priority.get(x.evidence_status, 0),
            reverse=True
        )

        highest_priority = sorted_alts[0] if sorted_alts else None

        if highest_priority and highest_priority.evidence_status in [QualitativeSupportState.SUPPORTED, QualitativeSupportState.STRONG_SUPPORT]:
            survival_status = "HIGH_FALSIFICATION_RISK"
        elif highest_priority and highest_priority.evidence_status == QualitativeSupportState.MIXED_EVIDENCE:
            survival_status = "CONTESTED_EVIDENCE"
        else:
            survival_status = "SURVIVED_INITIAL_FALSIFICATION"

        rec_exp = (
            highest_priority.discriminating_experiment_candidates[0]
            if highest_priority and highest_priority.discriminating_experiment_candidates
            else "Target engagement and specificity assay required"
        )

        summary = (
            f"Evaluated {len(typed_alternatives)} competing alternative mechanism(s). "
            f"Highest priority alternative: '{highest_priority.mechanism_statement if highest_priority else 'None'}' "
            f"with status [{highest_priority.evidence_status.value if highest_priority else 'NONE'}]. "
            f"This is a qualitative support comparison, not a calibrated probability."
        )

        return FalsificationDossier(
            hypothesis_id=hypothesis_id,
            hypothesis_title=str(hypothesis_title),
            competing_mechanisms=typed_alternatives,
            highest_priority_alternative=highest_priority,
            survival_status=survival_status,
            support_comparison_summary=summary,
            recommended_discriminating_experiment=rec_exp,
            provenance_notes="Falsification Dossier generated via AdversarialFalsificationEngine v2.0."
        )
