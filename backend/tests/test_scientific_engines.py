import pytest
from scientific.graphs.triclique_engine import TricliqueEngine
from scientific.evidence.independence_engine import EvidenceIndependenceEngine
from scientific.genetics.causal_genetics_engine import CausalGeneticsEngine
from scientific.phenotype_inversion.cpi_engine import CPIEngine
from scientific.pharmacology.rdkit_engine import RDKitEngine
from scientific.pharmacology.safety_gate import HardSafetyGateEngine
from scientific.hypothesis_compiler.compiler import HypothesisCompiler
from scientific.falsification.falsification_engine import AdversarialFalsificationEngine
from scientific.portfolio.pareto_engine import ParetoPortfolioEngine
from scientific.experiments.voi_designer import ValueOfInformationDesigner

def test_triclique_engine():
    engine = TricliqueEngine()
    drugs = ["D1", "D2"]
    targets = ["T1", "T2"]
    diseases = ["Dis1"]

    dt_edges = [("D1", "T1")]
    td_edges = [("T1", "Dis1"), ("T2", "Dis1")]
    dd_edges = [("D1", "Dis1")]

    cands = engine.find_candidate_edges(drugs, targets, diseases, dt_edges, td_edges, dd_edges)
    assert len(cands) >= 1
    assert cands[0]["type"] in ["candidate_drug_target", "candidate_target_disease"]

def test_evidence_independence():
    engine = EvidenceIndependenceEngine()
    claims = [
        {"id": "C1", "external_id": "PMID:123", "source_name": "PubMed", "quality_score": 0.9, "evidence_maturity": "experimentally_validated"},
        {"id": "C2", "external_id": "PMID:123", "source_name": "PubMed", "quality_score": 0.9, "evidence_maturity": "experimentally_validated"}
    ]
    res = engine.compute_independent_support(claims)
    assert "support_score" in res
    # duplicate citation should have lower independence factor
    assert res["score_decomposition"][0]["independence_i"] < 1.0 or res["score_decomposition"][1]["independence_i"] < 1.0

def test_causal_genetics():
    genetics = CausalGeneticsEngine()
    res = genetics.evaluate_target_causality("PKMYT1", "Ovarian Cancer", gwas_pvalue=1e-9, coloc_pp4=0.85)
    assert res["causal_score"] >= 0.6
    assert "Strong colocalization" in res["supporting_reasons"][1]

def test_cpi_engine():
    cpi_engine = CPIEngine()
    drivers = [{"name": "CCNE1", "weight": 1.0, "reversal": 0.8}]
    harms = [{"name": "Apoptosis Normal", "weight": 0.5, "induction": 0.1}]
    res = cpi_engine.compute_cpi_score(drivers, harms)
    assert res["cpi_score"] > 0.5

def test_rdkit_smiles_evaluator():
    rdkit = RDKitEngine()
    res = rdkit.evaluate_smiles("CC1=C(C=C(C=C1)C2=NC(=NC(=C2)N)N3CCN(CC3)C(=O)C4CC4)NC(=O)C5=CC=C(C=C5)F")
    assert res["valid_smiles"] is True
    assert res["molecular_weight"] > 200

def test_hard_safety_gates():
    gates = HardSafetyGateEngine()
    # Test 1: Fatal invalid direction of effect
    res1 = gates.evaluate_gates(direction_of_effect_valid=False)
    assert res1["passed"] is False
    assert len(res1["failed_gates"]) >= 1

    # Test 2: Infeasible exposure
    res2 = gates.evaluate_gates(free_concentration_nm=10.0, required_ic50_nm=100.0)
    assert res2["passed"] is False

    # Test 3: Valid parameters
    res3 = gates.evaluate_gates(free_concentration_nm=200.0, required_ic50_nm=50.0)
    assert res3["passed"] is True

def test_hypothesis_compiler():
    compiler = HypothesisCompiler()
    dossier = compiler.compile_hypothesis("H-01", "RP-6306", "PKMYT1", "inhibit", "HGSOC Cell", "END-01")
    assert len(dossier["proof_obligations"]) == 5
    assert dossier["compilation_status"] == "COMPILED"

def test_falsification_engine():
    engine = AdversarialFalsificationEngine()
    alts = [{"mechanism_name": "Off-target", "evidence_support": 0.2}]
    dossier = engine.generate_falsification_dossier("PKMYT1 Hypo", 0.8, alts)
    assert dossier["mechanistic_margin"] == 0.6
    assert dossier["survival_status"] == "SURVIVED_FALSIFICATION"

def test_pareto_portfolio():
    engine = ParetoPortfolioEngine()
    cands = [
        {"name": "Cand A", "cpi_score": 0.8, "novelty_score": 0.7, "safety_gate_passed": True},
        {"name": "Cand B", "cpi_score": 0.5, "novelty_score": 0.4, "safety_gate_passed": True},
        {"name": "Cand C", "cpi_score": 0.9, "novelty_score": 0.2, "safety_gate_passed": False}
    ]
    res = engine.rank_candidates(cands)
    assert len(res["pareto_frontier"]) >= 1
    assert len(res["dominated_candidates"]) >= 1

def test_voi_designer():
    designer = ValueOfInformationDesigner()
    res = designer.recommend_experiment("H-01", [], [])
    assert "recommended_experiment" in res
    assert res["recommended_experiment"]["voi_score"] > 0
