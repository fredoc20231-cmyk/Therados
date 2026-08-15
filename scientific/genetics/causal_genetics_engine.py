"""
Human Causal Genetics Engine.

Evaluates GWAS, eQTL, pQTL, colocalization, and direction-of-effect support for target-disease pairs.
"""

from typing import Dict, Any, Optional

class CausalGeneticsEngine:
    def evaluate_target_causality(
        self,
        target_symbol: str,
        disease_name: str,
        gwas_pvalue: Optional[float] = None,
        coloc_pp4: Optional[float] = None,
        eqtl_tissue_match: bool = False,
        loss_of_function_evidence: bool = False
    ) -> Dict[str, Any]:
        """
        Calculates causal genetics support for target P in disease D.
        """
        score = 0.0
        reasons = []

        if gwas_pvalue is not None:
            if gwas_pvalue <= 5e-8:
                score += 0.3
                reasons.append(f"Genome-wide significant GWAS association (p = {gwas_pvalue:.2e})")
            elif gwas_pvalue <= 1e-5:
                score += 0.15
                reasons.append(f"Suggestive GWAS association (p = {gwas_pvalue:.2e})")

        if coloc_pp4 is not None:
            if coloc_pp4 >= 0.8:
                score += 0.35
                reasons.append(f"Strong colocalization PP4 = {coloc_pp4:.2f} (shared causal variant)")
            elif coloc_pp4 >= 0.5:
                score += 0.2
                reasons.append(f"Moderate colocalization PP4 = {coloc_pp4:.2f}")

        if eqtl_tissue_match:
            score += 0.2
            reasons.append("eQTL signal matches disease-relevant cellular context")

        if loss_of_function_evidence:
            score += 0.25
            reasons.append("Human loss-of-function (LoF) phenotypic corroboration present")

        final_score = min(1.0, round(score, 3))

        return {
            "target_symbol": target_symbol,
            "disease_name": disease_name,
            "causal_score": final_score,
            "evidence_maturity": "causally_corroborated" if final_score >= 0.6 else "associative",
            "supporting_reasons": reasons if reasons else ["No direct human causal genetics data configured"]
        }
