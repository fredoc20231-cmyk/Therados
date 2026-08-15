"""
Adversarial Falsification Engine.

Attempts to falsify therapeutic hypotheses by pitting them against competing mechanisms
and calculating mechanistic support margins.
"""

from typing import Dict, Any, List

class AdversarialFalsificationEngine:
    def generate_falsification_dossier(
        self,
        hypothesis_title: str,
        hypothesis_support_score: float,
        alternative_mechanisms: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Creates an adversarial Falsification Dossier evaluating primary hypothesis against alternatives.
        """
        max_alt_support = max((alt.get("evidence_support", 0.0) for alt in alternative_mechanisms), default=0.0)

        # Mechanistic margin = Primary support - Highest competing support
        mechanistic_margin = round(hypothesis_support_score - max_alt_support, 3)

        evaluated_alternatives = []
        for alt in alternative_mechanisms:
            alt_support = alt.get("evidence_support", 0.2)
            evaluated_alternatives.append({
                "mechanism_name": alt.get("mechanism_name"),
                "description": alt.get("description"),
                "competing_support_score": alt_support,
                "status": "CONTESTED" if alt_support > 0.4 else "UNSUBSTANTIATED",
                "discriminating_experiment": alt.get("discriminating_assay", "Assay required")
            })

        survival_status = "SURVIVED_FALSIFICATION" if mechanistic_margin > 0.2 else "HIGH_FALSIFICATION_RISK"

        return {
            "hypothesis_title": hypothesis_title,
            "primary_support_score": hypothesis_support_score,
            "highest_competing_support": max_alt_support,
            "mechanistic_margin": mechanistic_margin,
            "survival_status": survival_status,
            "falsification_dossier": evaluated_alternatives,
            "decisive_experiment_recommendation": (
                f"Perform '{evaluated_alternatives[0]['discriminating_experiment']}' to rule out competing mechanism '{evaluated_alternatives[0]['mechanism_name']}'."
                if evaluated_alternatives else "No active competing mechanisms registered."
            )
        }
