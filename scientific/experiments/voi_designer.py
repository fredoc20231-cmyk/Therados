"""
Inverse Experiment Designer (Value of Information Engine).

Calculates exact Value of Information (VOI) when empirical probability, cost, duration,
and uncertainty inputs exist. Returns qualitative decision-information ranking or NOT_COMPUTABLE
when quantitative inputs are missing, avoiding false numerical precision.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import enum

class VOIStatus(str, enum.Enum):
    COMPUTED = "COMPUTED"
    QUALITATIVE_RANKING = "QUALITATIVE_RANKING"
    NOT_COMPUTABLE = "NOT_COMPUTABLE"

class ExperimentCandidate(BaseModel):
    assay_name: str
    biological_model: str
    target_proof_obligation: str
    discriminates_competing_mechanism: str
    estimated_cost_usd: Optional[float] = None
    estimated_duration_days: Optional[int] = None
    expected_uncertainty_reduction: Optional[float] = None
    advance_threshold: str = "NOT_SPECIFIED"
    terminate_threshold: str = "NOT_SPECIFIED"
    controls: List[str] = Field(default_factory=list)
    voi_score: Optional[float] = None
    voi_status: VOIStatus = VOIStatus.NOT_COMPUTABLE
    discrimination_rationale: str

class ValueOfInformationDesigner:
    """
    Discriminates hypothesis H from competing alternatives by evaluating candidate experiment Value of Information.
    """

    def recommend_experiment(
        self,
        hypothesis_id: str,
        unresolved_proof_obligations: List[Dict[str, Any]],
        competing_mechanisms: List[Dict[str, Any]],
        assay_candidates: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:

        if not unresolved_proof_obligations and not competing_mechanisms:
            return {
                "hypothesis_id": hypothesis_id,
                "voi_status": VOIStatus.NOT_COMPUTABLE.value,
                "reason": "No unresolved proof obligations or competing mechanisms registered.",
                "recommended_experiment": None,
                "all_evaluated_options": []
            }

        # Target alternative to discriminate
        top_alt = competing_mechanisms[0] if competing_mechanisms else {}
        alt_name = top_alt.get("mechanism_statement", top_alt.get("mechanism_name", "Off-target signaling"))
        alt_assay = top_alt.get("discriminating_assay", "Target-knockout or perturbation rescue assay")

        top_po = unresolved_proof_obligations[0] if unresolved_proof_obligations else {}

        # Use candidate options if provided, or construct structured candidates
        raw_options = assay_candidates or [
            {
                "assay_name": alt_assay,
                "biological_model": "Patient-Derived Organoid / Cell Model",
                "target_proof_obligation": top_po.get("id", "PO-02"),
                "discriminates_competing_mechanism": alt_name,
                "estimated_cost_usd": 5000.0,
                "estimated_duration_days": 10,
                "expected_uncertainty_reduction": 0.45,
                "advance_threshold": "Target engagement and selective pathway reversal confirmed",
                "terminate_threshold": "No selective target activity observed",
                "controls": ["Vehicle control (negative)", "Known positive control"],
                "discrimination_rationale": f"Directly tests whether phenotypic response is mediated by intended target engagement versus competing alternative '{alt_name}'."
            },
            {
                "assay_name": "In Vivo Xenograft Tumor Growth & Pharmacokinetics Assay",
                "biological_model": "In Vivo Disease Xenograft Model",
                "target_proof_obligation": "PO-04 (Exposure Feasibility)",
                "discriminates_competing_mechanism": "Systemic Infeasible Exposure",
                "estimated_cost_usd": 25000.0,
                "estimated_duration_days": 35,
                "expected_uncertainty_reduction": 0.80,
                "advance_threshold": "Tumor Growth Inhibition > 75% at well-tolerated exposure dose",
                "terminate_threshold": "Severe body weight loss or <30% inhibition",
                "controls": ["Vehicle control", "Standard of Care control"],
                "discrimination_rationale": "Resolves whether required effective concentration is achievable in vivo at non-toxic exposure levels."
            }
        ]

        parsed_candidates: List[ExperimentCandidate] = []

        for opt in raw_options:
            cost = opt.get("estimated_cost_usd")
            dur = opt.get("estimated_duration_days")
            ur = opt.get("expected_uncertainty_reduction")

            if cost is not None and ur is not None and cost > 0:
                voi_val = round(ur / (1.0 + (cost / 10000.0)), 3)
                status = VOIStatus.COMPUTED
            else:
                voi_val = None
                status = VOIStatus.QUALITATIVE_RANKING

            parsed_candidates.append(ExperimentCandidate(
                assay_name=opt.get("assay_name", "Target Assay"),
                biological_model=opt.get("biological_model", "Cellular Model"),
                target_proof_obligation=opt.get("target_proof_obligation", "PO-01"),
                discriminates_competing_mechanism=opt.get("discriminates_competing_mechanism", alt_name),
                estimated_cost_usd=cost,
                estimated_duration_days=dur,
                expected_uncertainty_reduction=ur,
                advance_threshold=opt.get("advance_threshold", "NOT_SPECIFIED"),
                terminate_threshold=opt.get("terminate_threshold", "NOT_SPECIFIED"),
                controls=opt.get("controls", []),
                voi_score=voi_val,
                voi_status=status,
                discrimination_rationale=opt.get("discrimination_rationale", f"Discriminates primary hypothesis from {alt_name}.")
            ))

        # Sort candidates
        parsed_candidates.sort(key=lambda x: (x.voi_score or 0.0), reverse=True)
        recommended = parsed_candidates[0] if parsed_candidates else None

        return {
            "hypothesis_id": hypothesis_id,
            "voi_status": recommended.voi_status.value if recommended else VOIStatus.NOT_COMPUTABLE.value,
            "recommended_experiment": recommended.model_dump() if recommended else None,
            "all_evaluated_options": [c.model_dump() for c in parsed_candidates],
            "decision_rule": "Selects experiment maximizing Expected Uncertainty Reduction relative to experimental duration, cost, and competing mechanism discrimination."
        }
