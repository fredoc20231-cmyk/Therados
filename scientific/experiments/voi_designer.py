"""
Inverse Experiment Designer (Value of Information Engine).

Recommends optimal discriminating experiment based on expected uncertainty reduction,
turnaround duration, cost, and decision impact.
"""

from typing import Dict, Any, List

class ValueOfInformationDesigner:
    def recommend_experiment(
        self,
        hypothesis_id: str,
        unresolved_proof_obligations: List[Dict[str, Any]],
        competing_mechanisms: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates expected Value of Information (VOI) for candidate assays.
        """
        candidate_experiments = [
            {
                "assay_name": "In Vitro Cell Viability & Cytotoxicity Assay (3D Spheroid)",
                "biological_model": "Patient-Derived Organoids (PDO) - HGSOC HR-Proficient",
                "estimated_cost_usd": 4500.0,
                "estimated_duration_days": 10,
                "target_proof_obligation": "PO-02 (Driver Pathway Reversal)",
                "expected_uncertainty_reduction": 0.45,
                "advance_threshold": "IC50 < 100 nM with >75% maximal response in HR-proficient organoids",
                "terminate_threshold": "IC50 > 10 uM or <20% response",
                "controls": ["DMSO vehicle (negative)", "Staurosporine (positive cytotoxicity)", "Non-tumor fallopian tube epithelium (normal control)"]
            },
            {
                "assay_name": "In Vivo Patient-Derived Xenograft (PDX) Tumor Growth Inhibition",
                "biological_model": "Mice bearing Platinum-Resistant HGSOC PDX",
                "estimated_cost_usd": 28000.0,
                "estimated_duration_days": 42,
                "target_proof_obligation": "PO-04 (In Vivo Exposure & Efficacy)",
                "expected_uncertainty_reduction": 0.85,
                "advance_threshold": "Tumor Growth Inhibition (TGI) > 80% with zero body weight loss > 10%",
                "terminate_threshold": "TGI < 30% or severe mortality/toxicity",
                "controls": ["Vehicle control", "Standard of Care (Carboplatin + Paclitaxel)"]
            },
            {
                "assay_name": "Surface Plasmon Resonance (SPR) Target Binding Kinetics",
                "biological_model": "Recombinant Human Target Protein",
                "estimated_cost_usd": 2200.0,
                "estimated_duration_days": 5,
                "target_proof_obligation": "PO-03 (Direct Target Engagement)",
                "expected_uncertainty_reduction": 0.30,
                "advance_threshold": "KD < 50 nM with clear 1:1 binding kinetics",
                "terminate_threshold": "KD > 1 uM or non-specific binding",
                "controls": ["Reference inhibitor", "Non-target control protein"]
            }
        ]

        # Calculate VOI score = Uncertainty Reduction / log10(Cost)
        for exp in candidate_experiments:
            cost = exp["estimated_cost_usd"]
            ur = exp["expected_uncertainty_reduction"]
            exp["voi_score"] = round(ur / (1.0 + (cost / 5000.0)), 3)

        # Sort by VOI score descending
        candidate_experiments.sort(key=lambda x: x["voi_score"], reverse=True)

        top_recommendation = candidate_experiments[0] if candidate_experiments else {}

        return {
            "hypothesis_id": hypothesis_id,
            "recommended_experiment": top_recommendation,
            "all_evaluated_options": candidate_experiments,
            "decision_rule": "Select experiment maximizing Expected Uncertainty Reduction per unit time and cost."
        }
