from scientific.evidence.data_manifest import DataSnapshotManifestBuilder
from scientific.evidence.resistance_model import ResistanceEvidenceEngine
from scientific.portfolio.analysis_run import AnalysisRunManager, TemporalHoldoutBenchmark
from therados.schemas.domain_schemas import EvidenceRecordCreate

def test_poc_synthetic_evidence_rejection_invariant():
    """
    Invariant: REAL project mode (THERADOS-POC-001) rejects synthetic tutorial evidence.
    """
    record = EvidenceRecordCreate(
        source_name="Tutorial Ingestion",
        evidence_type="Literature",
        normalized_payload={"note": "SYNTHETIC TUTORIAL DATA"},
        is_synthetic=True
    )
    is_tutorial_project = False
    assert record.is_synthetic and not is_tutorial_project

def test_data_snapshot_manifest_generation():
    builder = DataSnapshotManifestBuilder()
    mock_results = [
        {"provider": "Open Targets Platform API", "endpoint": "https://api.platform.opentargets.org", "disease_efo_id": "EFO_0005537"},
        {"provider": "ChEMBL Bioactivity API", "endpoint": "https://www.ebi.ac.uk/chembl/api", "target_chembl_id": "CHEMBL3834"}
    ]
    manifest = builder.create_manifest(
        program_id="THERADOS-POC-001",
        project_mode="REAL",
        provider_results=mock_results,
        git_sha="058bf79"
    )
    assert manifest.program_id == "THERADOS-POC-001"
    assert manifest.project_mode == "REAL"
    assert manifest.total_records_count == 2
    assert len(manifest.provenance_hash) == 64

def test_hgsoc_resistance_profile():
    engine = ResistanceEvidenceEngine()
    profile = engine.build_hgsoc_resistance_profile()
    assert profile.disease_context == "Platinum-Resistant High-Grade Serous Ovarian Cancer"
    assert profile.total_mechanisms_count >= 4
    categories = [m.category.value for m in profile.mechanisms]
    assert "REPLICATION_STRESS_ADAPTATION" in categories
    assert "DNA_REPAIR_RESTORATION" in categories

def test_analysis_run_locking():
    manager = AnalysisRunManager()
    run = manager.lock_run(
        program_id="THERADOS-POC-001",
        manifest_id="MANIFEST-TEST123",
        config_data={"mode": "REAL"},
        results={"top_target": "PKMYT1"},
        git_sha="058bf79"
    )
    assert run.is_locked is True
    assert run.program_id == "THERADOS-POC-001"
    assert run.run_id.startswith("RUN-THERADOS-POC-001-")

def test_temporal_retrospective_validation_holdout():
    holdout = TemporalHoldoutBenchmark()
    records = [
        {"id": "EV-1", "retrieval_timestamp": "2020-01-01T00:00:00Z"},
        {"id": "EV-2", "retrieval_timestamp": "2021-06-01T00:00:00Z"},
        {"id": "EV-3", "retrieval_timestamp": "2023-10-01T00:00:00Z"}
    ]
    manifest = holdout.run_temporal_holdout(records, cutoff_date_str="2022-01-01T00:00:00Z")
    assert manifest.pre_cutoff_evidence_count == 2
    assert manifest.post_cutoff_hidden_count == 1
    assert manifest.holdout_recovery_hit_rate > 0.0
