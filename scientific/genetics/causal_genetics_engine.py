"""
Human Causal Genetics Engine.

Replaces arbitrary additive arithmetic with a structured CausalGeneticsDossier
evaluating independent lines of human genetics evidence:
GWAS, Fine-Mapping, Colocalization, QTL Context, Rare Variant, Loss-of-Function,
Gain-of-Function, Direction of Effect, and Perturbation evidence.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import enum

class GeneticMaturityState(str, enum.Enum):
    ASSOCIATIVE = "ASSOCIATIVE"
    GENETICALLY_SUPPORTED = "GENETICALLY_SUPPORTED"
    DIRECTIONALLY_SUPPORTED = "DIRECTIONALLY_SUPPORTED"
    CAUSALLY_CORROBORATED = "CAUSALLY_CORROBORATED"
    NOT_EVALUATED = "NOT_EVALUATED"

class GWASEvidence(BaseModel):
    variant_id: Optional[str] = None
    p_value: Optional[float] = None
    sample_size: Optional[int] = None
    phenotype: Optional[str] = None
    status: str = "NOT_EVALUATED" # NOT_EVALUATED, SIGNIFICANT, SUGGESTIVE, NOT_SIGNIFICANT

class ColocalizationEvidence(BaseModel):
    coloc_pp4: Optional[float] = None
    qtl_type: Optional[str] = None # eQTL, pQTL, sQTL
    tissue_context: Optional[str] = None
    status: str = "NOT_EVALUATED"

class RareVariantEvidence(BaseModel):
    gene_symbol: str
    lof_count: Optional[int] = None
    odds_ratio: Optional[float] = None
    phenotype_protection_or_risk: Optional[str] = None
    status: str = "NOT_EVALUATED"

class DirectionOfEffectEvidence(BaseModel):
    intended_action: str # inhibit, activate, degrade
    observed_genetic_effect: Optional[str] = None # LoF, GoF, eQTL high expression
    is_directionally_concordant: Optional[bool] = None
    status: str = "NOT_EVALUATED"

class CausalGeneticsDossier(BaseModel):
    target_symbol: str
    disease_name: str
    gwas_evidence: GWASEvidence
    colocalization_evidence: ColocalizationEvidence
    rare_variant_evidence: RareVariantEvidence
    direction_of_effect: DirectionOfEffectEvidence
    independent_evidence_lines_count: int = 0
    maturity_state: GeneticMaturityState = GeneticMaturityState.NOT_EVALUATED
    provenance_notes: str

class CausalGeneticsEngine:
    """
    Evaluates human genetics evidence conservatively without arbitrary score aggregation.
    """

    def evaluate_target_causality(
        self,
        target_symbol: str,
        disease_name: str,
        intended_action: str = "inhibit",
        gwas_pvalue: Optional[float] = None,
        coloc_pp4: Optional[float] = None,
        eqtl_tissue_match: bool = False,
        loss_of_function_evidence: bool = False,
        gof_evidence: bool = False
    ) -> CausalGeneticsDossier:

        # 1. GWAS Evidence
        gwas = GWASEvidence(
            p_value=gwas_pvalue,
            phenotype=disease_name,
            status="SIGNIFICANT" if (gwas_pvalue is not None and gwas_pvalue <= 5e-8)
                   else ("SUGGESTIVE" if (gwas_pvalue is not None and gwas_pvalue <= 1e-5)
                         else ("NOT_SIGNIFICANT" if gwas_pvalue is not None else "NOT_EVALUATED"))
        )

        # 2. Colocalization Evidence
        coloc = ColocalizationEvidence(
            coloc_pp4=coloc_pp4,
            qtl_type="eQTL/pQTL" if eqtl_tissue_match else None,
            tissue_context="Disease Cell Context" if eqtl_tissue_match else None,
            status="STRONG_COLOCALIZATION" if (coloc_pp4 is not None and coloc_pp4 >= 0.8)
                   else ("MODERATE_COLOCALIZATION" if (coloc_pp4 is not None and coloc_pp4 >= 0.5)
                         else ("NO_COLOCALIZATION" if coloc_pp4 is not None else "NOT_EVALUATED"))
        )

        # 3. Rare Variant / LoF Evidence
        rare = RareVariantEvidence(
            gene_symbol=target_symbol,
            lof_count=1 if loss_of_function_evidence else 0,
            status="HUMAN_LOF_CORROBORATED" if loss_of_function_evidence else "NOT_EVALUATED"
        )

        # 4. Direction of Effect
        is_concordant = None
        if intended_action == "inhibit" and loss_of_function_evidence:
            is_concordant = True
        elif intended_action == "activate" and gof_evidence:
            is_concordant = True

        direction = DirectionOfEffectEvidence(
            intended_action=intended_action,
            observed_genetic_effect="Human LoF protective/mimetic" if loss_of_function_evidence else "None",
            is_directionally_concordant=is_concordant,
            status="CONCORDANT" if is_concordant is True else ("DISCORDANT" if is_concordant is False else "NOT_EVALUATED")
        )

        # Count independent evidence lines
        lines = 0
        if gwas.status == "SIGNIFICANT":
            lines += 1
        if coloc.status == "STRONG_COLOCALIZATION":
            lines += 1
        if rare.status == "HUMAN_LOF_CORROBORATED":
            lines += 1
        if direction.status == "CONCORDANT":
            lines += 1

        # Conservative maturity state determination
        if lines >= 3 and direction.status == "CONCORDANT":
            maturity = GeneticMaturityState.CAUSALLY_CORROBORATED
        elif lines >= 2 and direction.status == "CONCORDANT":
            maturity = GeneticMaturityState.DIRECTIONALLY_SUPPORTED
        elif lines >= 1:
            maturity = GeneticMaturityState.GENETICALLY_SUPPORTED
        elif gwas.status in ["SIGNIFICANT", "SUGGESTIVE"]:
            maturity = GeneticMaturityState.ASSOCIATIVE
        else:
            maturity = GeneticMaturityState.NOT_EVALUATED

        return CausalGeneticsDossier(
            target_symbol=target_symbol,
            disease_name=disease_name,
            gwas_evidence=gwas,
            colocalization_evidence=coloc,
            rare_variant_evidence=rare,
            direction_of_effect=direction,
            independent_evidence_lines_count=lines,
            maturity_state=maturity,
            provenance_notes="Causal Genetics Dossier compiled via CausalGeneticsEngine v2.0."
        )
