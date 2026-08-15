from scientific.graphs.triclique_engine import NeighborhoodCompletionBaseline, MaximalTricliqueAugmentationEngine
from scientific.evidence.independence_engine import EvidenceIndependenceEngine
from scientific.genetics.causal_genetics_engine import CausalGeneticsEngine, GeneticMaturityState
from scientific.phenotype_inversion.cpi_engine import CPIEngine
from scientific.pharmacology.rdkit_engine import RDKitEngine
from scientific.pharmacology.safety_gate import HardSafetyGateEngine, GateOutcome
from scientific.hypothesis_compiler.compiler import HypothesisCompiler
from scientific.falsification.falsification_engine import AdversarialFalsificationEngine
from scientific.portfolio.pareto_engine import ParetoPortfolioEngine
from scientific.experiments.voi_designer import ValueOfInformationDesigner

def test_neighborhood_completion_baseline():
    engine = NeighborhoodCompletionBaseline()
    drugs = ["D1", "D2"]
    targets = ["T1", "T2"]
    diseases = ["Dis1"]

    dt_edges = [("D1", "T1")]
    td_edges = [("T1", "Dis1"), ("T2", "Dis1")]
    dd_edges = [("D1", "Dis1")]

    cands = engine.find_candidate_edges(drugs, targets, diseases, dt_edges, td_edges, dd_edges)
    assert len(cands) >= 1
    assert cands[0]["type"] in ["candidate_drug_target", "candidate_target_disease"]

def test_maximal_triclique_engine():
    engine = MaximalTricliqueAugmentationEngine(min_d=1, min_p=1, min_e=1)
    drugs = ["D1", "D2"]
    proteins = ["P1", "P2"]
    diseases = ["E1"]

    dp_edges = [("D1", "P1"), ("D1", "P2"), ("D2", "P1"), ("D2", "P2")]
    pe_edges = [("P1", "E1"), ("P2", "E1")]
    de_edges = [("D1", "E1"), ("D2", "E1")]

    res = engine.predict_candidate_edges(drugs, proteins, diseases, dp_edges, pe_edges, de_edges)
    assert res["maximal_tricliques_count"] >= 1

def test_evidence_independence():
    engine = EvidenceIndependenceEngine()
    claims = [
        {"id": "C1", "external_id": "PMID:123", "source_name": "PubMed", "quality_score": 0.9, "evidence_maturity": "experimentally_validated"},
        {"id": "C2", "external_id": "PMID:123", "source_name": "PubMed", "quality_score": 0.9, "evidence_maturity": "experimentally_validated"}
    ]
    res = engine.compute_independent_support(claims)
    assert "support_score" in res
    assert res["score_decomposition"][0]["independence_i"] < 1.0 or res["score_decomposition"][1]["independence_i"] < 1.0

def test_causal_genetics():
    genetics = CausalGeneticsEngine()
    dossier = genetics.evaluate_target_causality("PKMYT1", "Ovarian Cancer", gwas_pvalue=1e-9, coloc_pp4=0.85, eqtl_tissue_match=True, loss_of_function_evidence=True)
    assert dossier.maturity_state == GeneticMaturityState.CAUSALLY_CORROBORATED
    assert dossier.independent_evidence_lines_count >= 3

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

    # Test 2: Infeasible exposure
    res2 = gates.evaluate_gates(free_concentration_nm=10.0, required_ic50_nm=100.0)
    assert res2["passed"] is False

    # Test 3: Valid parameters
    res3 = gates.evaluate_gates(
        direction_of_effect_valid=True,
        target_expressed_in_context=True,
        free_concentration_nm=200.0,
        required_ic50_nm=50.0,
        herg_liability="LOW",
        genotoxicity_liability="LOW"
    )
    assert res3["passed"] is True
    assert res3["overall_outcome"] == GateOutcome.PASS.value

def test_hypothesis_compiler():
    compiler = HypothesisCompiler()
    dossier = compiler.compile_hypothesis("H-01", "RP-6306", "PKMYT1", "inhibit", "HGSOC Cell", "END-01")
    assert len(dossier.proof_obligations) == 5
    assert dossier.compilation_status == "COMPILED"

def test_falsification_engine():
    engine = AdversarialFalsificationEngine()
    alts = [{"mechanism_name": "Off-target", "description": "Competing pathway"}]
    dossier = engine.generate_falsification_dossier("H-01", "PKMYT1 Hypo", alts)
    assert dossier.survival_status == "SURVIVED_INITIAL_FALSIFICATION"

def test_pareto_portfolio():
    engine = ParetoPortfolioEngine()
    cands = [
        {"name": "Cand A", "cpi_score": 0.8, "novelty_score": 0.7, "gate_status": "PASS", "safety_gate_passed": True},
        {"name": "Cand B", "cpi_score": 0.5, "novelty_score": 0.4, "gate_status": "PASS", "safety_gate_passed": True},
        {"name": "Cand C", "cpi_score": 0.9, "novelty_score": 0.2, "gate_status": "REJECTED_BY_FATAL_GATE", "safety_gate_passed": False}
    ]
    res = engine.rank_candidates(cands)
    assert len(res["feasible_frontier"]) >= 1
    assert len(res["fatal_gate_failures"]) == 1

def test_voi_designer():
    designer = ValueOfInformationDesigner()
    res = designer.recommend_experiment("H-01", [{"id": "PO-01"}], [{"mechanism_name": "Off-target"}])
    assert "recommended_experiment" in res
    assert res["recommended_experiment"]["voi_score"] > 0
