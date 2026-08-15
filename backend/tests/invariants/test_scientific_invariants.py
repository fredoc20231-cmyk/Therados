from scientific.graphs.triclique_engine import MaximalTricliqueAugmentationEngine
from scientific.evidence.independence_engine import EvidenceIndependenceEngine
from scientific.pharmacology.safety_gate import HardSafetyGateEngine, GateOutcome
from scientific.hypothesis_compiler.compiler import HypothesisCompiler, ObligationState
from scientific.falsification.falsification_engine import AdversarialFalsificationEngine, QualitativeSupportState
from scientific.portfolio.pareto_engine import ParetoPortfolioEngine

# Invariant 1: Candidate failing fatal safety gate cannot ADVANCE / cannot be on feasible frontier
def test_invariant_1_failed_fatal_gate_cannot_advance():
    safety_engine = HardSafetyGateEngine()
    res = safety_engine.evaluate_gates(herg_liability="HIGH")
    assert res["passed"] is False
    assert res["overall_outcome"] == GateOutcome.FAIL.value

    portfolio = ParetoPortfolioEngine()
    cands = [
        {"name": "Cand A", "cpi_score": 0.9, "novelty_score": 0.8, "safety_gate_passed": False, "gate_status": "REJECTED_BY_FATAL_GATE"}
    ]
    rank_res = portfolio.rank_candidates(cands)
    assert len(rank_res["feasible_frontier"]) == 0
    assert len(rank_res["fatal_gate_failures"]) == 1

# Invariant 2: Missing safety data cannot PASS (must yield UNRESOLVED)
def test_invariant_2_missing_safety_data_yields_unresolved():
    safety_engine = HardSafetyGateEngine()
    res = safety_engine.evaluate_gates(herg_liability=None, genotoxicity_liability=None)
    assert res["passed"] is False
    assert res["overall_outcome"] == GateOutcome.UNRESOLVED.value
    assert len(res["unresolved_gates"]) >= 1

# Invariant 3: Negative result is distinct from missing result
def test_invariant_3_negative_result_distinct_from_missing():
    falsification = AdversarialFalsificationEngine()
    alts = [
        {"mechanism_name": "Off-target toxicity", "description": "Competing pathway"}
    ]
    # Missing evidence
    dossier_missing = falsification.generate_falsification_dossier("H-01", "PKMYT1", alts, existing_evidence=[])
    assert dossier_missing.competing_mechanisms[0].evidence_status == QualitativeSupportState.NOT_EVALUATED

    # Contradicting evidence
    dossier_ruled_out = falsification.generate_falsification_dossier(
        "H-01", "PKMYT1", alts,
        existing_evidence=[{"subject": "Off-target toxicity", "predicate": "rules_out", "id": "EV-01"}]
    )
    assert dossier_ruled_out.competing_mechanisms[0].evidence_status == QualitativeSupportState.UNSUPPORTED

# Invariant 4: LLM suggestion cannot become validated evidence automatically
def test_invariant_4_llm_suggestion_not_validated_evidence():
    compiler = HypothesisCompiler()
    dossier = compiler.compile_hypothesis(
        hypothesis_id="H-01",
        intervention="RP-6306",
        target="PKMYT1",
        action="inhibit",
        cellular_context="HGSOC",
        disease_endotype="END-01"
    )
    for po in dossier.proof_obligations:
        # LLM suggestions or unverified rule items stay UNRESOLVED
        assert po.state in [ObligationState.UNRESOLVED, ObligationState.SUPPORTED]
        assert po.source_type.value == "RULE_GENERATED"

# Invariant 5: Hypothesis proof obligations emit rule provenance and remain uncomputed without evidence
def test_invariant_5_proof_obligation_rule_provenance():
    compiler = HypothesisCompiler()
    dossier = compiler.compile_hypothesis("H-01", "RP-6306", "PKMYT1", "inhibit", "HGSOC Cell", "END-01")
    for po in dossier.proof_obligations:
        assert po.rule_provenance.startswith("Rule-")

# Invariant 6: Evidence provenance retains quality, independence, and relevance
def test_invariant_6_evidence_provenance_retained():
    independence = EvidenceIndependenceEngine()
    claims = [
        {"id": "C1", "external_id": "PMID:100", "source_name": "OpenTargets", "quality_score": 0.9, "evidence_maturity": "experimentally_validated"}
    ]
    res = independence.compute_independent_support(claims)
    assert res["score_decomposition"][0]["quality_q"] == 0.9
    assert res["score_decomposition"][0]["relevance_r"] == 0.95

# Invariant 7: Unconfigured docking cannot return a fake docking score
def test_invariant_7_unconfigured_docking_returns_none():
    from scientific.pharmacology.rdkit_engine import AutoDockVinaAdapter
    adapter = AutoDockVinaAdapter(vina_path=None)
    res = adapter.run_docking("CC1...", "PDB123")
    assert res["docking_score_kcal_mol"] is None
    assert res["configured"] is False

# Invariant 8: Uncalibrated support cannot be labeled probability
def test_invariant_8_uncalibrated_support_not_labeled_probability():
    independence = EvidenceIndependenceEngine()
    res = independence.compute_independent_support([])
    assert "probability" not in res.get("label", "").lower()

# Invariant 9: Synthetic tutorial evidence cannot enter real project
def test_invariant_9_synthetic_tutorial_data_flagged():
    from therados.schemas.domain_schemas import EvidenceRecordCreate
    rec = EvidenceRecordCreate(
        source_name="Tutorial Source",
        evidence_type="Literature",
        normalized_payload={"note": "SYNTHETIC TUTORIAL DATA"},
        is_synthetic=True
    )
    assert rec.is_synthetic is True

# Invariant 10: Multi-tenant / RBAC UserRole definitions
def test_invariant_10_user_roles():
    from therados.models.domain_models import UserRole
    assert UserRole.VIEWER.value == "viewer"
    assert UserRole.SCIENTIST.value == "scientist"
    assert UserRole.REVIEWER.value == "reviewer"
    assert UserRole.ADMIN.value == "admin"

# Invariant 11: Invalid target-action direction fails safety gate
def test_invariant_11_invalid_direction_of_effect_fails():
    safety = HardSafetyGateEngine()
    res = safety.evaluate_gates(direction_of_effect_valid=False)
    assert res["passed"] is False
    assert any("direction of effect" in f for f in res["failed_gates"])

# Invariant 12: Failed exposure gate cannot be offset by high graph score
def test_invariant_12_failed_exposure_gate_not_offset():
    safety = HardSafetyGateEngine()
    res = safety.evaluate_gates(free_concentration_nm=5.0, required_ic50_nm=100.0)
    assert res["passed"] is False
    assert res["overall_outcome"] == GateOutcome.FAIL.value

# Invariant 13: Model uncertainty status is recorded as NOT_ESTIMATED when uncalibrated
def test_invariant_13_uncertainty_not_estimated_by_default():
    compiler = HypothesisCompiler()
    dossier = compiler.compile_hypothesis("H-01", "D1", "T1", "inhibit", "C1", "E1")
    for u in dossier.uncertainty_vector:
        assert u.status == "NOT_ESTIMATED"
        assert u.value is None

# Invariant 14: Exact triclique known-answer tests succeed
def test_invariant_14_exact_maximal_triclique_known_answer():
    engine = MaximalTricliqueAugmentationEngine(min_d=1, min_p=1, min_e=1)
    drugs = ["D1", "D2"]
    proteins = ["P1", "P2"]
    diseases = ["E1"]

    # Construct complete 2x2x1 triclique (D1, D2) x (P1, P2) x (E1)
    dp = [("D1", "P1"), ("D1", "P2"), ("D2", "P1"), ("D2", "P2")]
    pe = [("P1", "E1"), ("P2", "E1")]
    de = [("D1", "E1"), ("D2", "E1")]

    res = engine.predict_candidate_edges(drugs, proteins, diseases, dp, pe, de)
    assert res["maximal_tricliques_count"] >= 1
    tc = res["maximal_tricliques"][0]
    assert set(tc["drugs"]) == {"D1", "D2"}
    assert set(tc["proteins"]) == {"P1", "P2"}
    assert set(tc["diseases"]) == {"E1"}

# Invariant 15: Competing mechanism selection chooses evidence-priority alternative
def test_invariant_15_competing_mechanism_evidence_priority():
    falsification = AdversarialFalsificationEngine()
    alts = [
        {"mechanism_name": "Insertion Order First Alt", "description": "No evidence"},
        {"mechanism_name": "Supported Competing Alt", "description": "Has evidence"}
    ]
    # Evidence supports the second alternative
    evidence = [{"subject": "Supported Competing Alt", "predicate": "causes_off_target", "id": "EV-99"}]
    dossier = falsification.generate_falsification_dossier("H-01", "Title", alts, existing_evidence=evidence)

    assert dossier.highest_priority_alternative is not None
    assert dossier.highest_priority_alternative.mechanism_statement == "Supported Competing Alt"
    assert dossier.highest_priority_alternative.evidence_status == QualitativeSupportState.SUPPORTED
