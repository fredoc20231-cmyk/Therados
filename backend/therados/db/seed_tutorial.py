import asyncio
import hashlib
from passlib.context import CryptContext
from sqlalchemy.future import select

from therados.db.session import AsyncSessionLocal, engine, Base
from therados.models.domain_models import (
    Organization, User, Membership, UserRole, Project, TherapeuticProgram,
    BiologicalEntity, EntityAlias, EntityIdentifier, EvidenceSource, EvidenceRecord,
    EvidenceClaim, EvidenceMaturity, TherapeuticHypothesis, ProofObligation, AlternativeMechanism, CandidateIntervention, PharmacologyAssessment,
    SafetyAssessment, ExperimentPlan, ExperimentRun, Decision, DecisionOutcome,
    DigitalTwinSnapshot, ModelProvider
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

async def seed_tutorial_data() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Check if already seeded
        res = await session.execute(select(User).where(User.email == "scientist@therados.ai"))
        if res.scalar_one_or_none():
            print("Tutorial data already seeded.")
            return

        print("Seeding synthetic tutorial dataset...")

        # 1. Organization
        org = Organization(
            name="TheraDOS BioTech",
            slug="therados-biotech",
            status="active"
        )
        session.add(org)
        await session.flush()

        # 2. User
        hashed_pw = pwd_context.hash("therados123")
        user = User(
            email="scientist@therados.ai",
            display_name="Dr. Elena Vance (Lead Scientist)",
            hashed_password=hashed_pw,
            status="active"
        )
        session.add(user)
        await session.flush()

        # 3. Membership
        membership = Membership(
            organization_id=org.id,
            user_id=user.id,
            role=UserRole.ADMIN
        )
        session.add(membership)

        # 4. Project
        project = Project(
            organization_id=org.id,
            name="Gynecologic Oncology Targets",
            description="Identification and synthetic prioritization of target interventions for platinum-resistant HGSOC",
            disease_area="Ovarian Cancer",
            created_by=user.id
        )
        session.add(project)
        await session.flush()

        # 5. Program
        program = TherapeuticProgram(
            project_id=project.id,
            disease="High-Grade Serous Ovarian Cancer",
            indication="Platinum-Resistant HGSOC",
            patient_context="Recurrent disease following adjuvant carboplatin/paclitaxel chemotherapy",
            disease_stage="Stage III/IV Recurrent",
            treatment_context="Second-line or later monotherapy",
            program_objective="Identify synthetic lethal targets for CCNE1-amplified HR-proficient endotype",
            constraints={"max_acceptable_cmax_um": 5.0, "required_therapeutic_index": 10.0}
        )
        session.add(program)
        await session.flush()

        # 6. Biological Entities
        target_pkmyt1 = BiologicalEntity(
            entity_type="Target",
            name="PKMYT1",
            canonical_symbol="PKMYT1",
            description="Protein Kinase Membrane Associated Tyrosine/Threonine 1"
        )
        target_ccne1 = BiologicalEntity(
            entity_type="Gene",
            name="CCNE1",
            canonical_symbol="CCNE1",
            description="Cyclin E1 Oncogene"
        )
        cmpd_rp6306 = BiologicalEntity(
            entity_type="Compound",
            name="RP-6306",
            canonical_symbol="RP-6306",
            description="Potent, selective PKMYT1 inhibitor"
        )
        session.add_all([target_pkmyt1, target_ccne1, cmpd_rp6306])
        await session.flush()

        # Identifiers & Aliases
        session.add(EntityIdentifier(entity_id=target_pkmyt1.id, namespace="HGNC", identifier="9031"))
        session.add(EntityIdentifier(entity_id=cmpd_rp6306.id, namespace="ChEMBL", identifier="CHEMBL4801928"))
        session.add(EntityAlias(entity_id=target_pkmyt1.id, alias="MYT1"))

        # 7. Evidence Source & Records (Flagged as Synthetic)
        ev_source = EvidenceSource(
            name="Synthetic Tutorial Ingestion Source",
            source_type="Inferred",
            licensing_notes="SYNTHETIC TUTORIAL DATA — NOT SCIENTIFIC EVIDENCE"
        )
        session.add(ev_source)
        await session.flush()

        raw_payload = "SYNTHETIC TUTORIAL DATA — NOT SCIENTIFIC EVIDENCE: PKMYT1 inhibition in CCNE1 amplified cells leads to premature mitosis and mitotic catastrophe."
        checksum = hashlib.sha256(raw_payload.encode()).hexdigest()

        ev_record = EvidenceRecord(
            source_id=ev_source.id,
            external_id="PMID:34521900-SYNTHETIC",
            evidence_type="Literature",
            evidence_maturity=EvidenceMaturity.EXPERIMENTALLY_VALIDATED,
            normalized_payload={"claim": "PKMYT1 inhibition synthetic lethality in CCNE1 amplified HGSOC", "is_tutorial": True},
            checksum=checksum,
            quality_score=0.95,
            is_synthetic=True
        )
        session.add(ev_record)
        await session.flush()

        # 8. Evidence Claim
        ev_claim = EvidenceClaim(
            evidence_record_id=ev_record.id,
            subject_entity_id=cmpd_rp6306.id,
            predicate="inhibits",
            object_entity_id=target_pkmyt1.id,
            direction="decreases",
            sign=-1,
            context={"cellular_context": "HGSOC Tumor Cell", "disease": "Platinum-Resistant HGSOC"},
            evidence_maturity=EvidenceMaturity.EXPERIMENTALLY_VALIDATED,
            support_score=0.92
        )
        session.add(ev_claim)

        # 9. Therapeutic Hypothesis
        hypothesis = TherapeuticHypothesis(
            program_id=program.id,
            title="PKMYT1 Inhibition in CCNE1-Amplified Platinum-Resistant HGSOC",
            intervention_name="RP-6306 (PKMYT1 Inhibitor)",
            intended_target="PKMYT1",
            intended_action="inhibit",
            cellular_context="High-Grade Serous Ovarian Carcinoma Cell",
            disease_endotype="CCNE1-Amplified HR-Proficient (END-01)",
            genomic_background="CCNE1 Copy Number > 6, BRCA1 WT",
            predictive_biomarkers=["CCNE1 High Amplification", "BRCA1 Wild-Type"],
            dose_exposure_regime="20mg BID Oral",
            schedule_duration="Continuous 28-day cycle",
            safety_constraints={"max_cmax_um": 5.0, "herg_ic50_um": 30.0},
            maturity=EvidenceMaturity.EXPERIMENTALLY_VALIDATED,
            support_score=0.88,
            status="compiled",
            version=1
        )
        session.add(hypothesis)
        await session.flush()

        # Proof Obligations
        po1 = ProofObligation(
            hypothesis_id=hypothesis.id,
            proposition="PKMYT1 kinase is overexpressed in CCNE1-amplified HGSOC tumor cells relative to fallopian epithelium",
            required_evidence_type="Omics / Expression",
            state="supported",
            threshold_value="TPM > 15",
            evidence_references=[ev_record.id]
        )
        po2 = ProofObligation(
            hypothesis_id=hypothesis.id,
            proposition="RP-6306 achieves selective PKMYT1 target engagement at <50 nM in cellular binding assay",
            required_evidence_type="Biophysical / Binding Assay",
            state="supported",
            threshold_value="IC50 < 50 nM",
            evidence_references=[ev_record.id]
        )
        po3 = ProofObligation(
            hypothesis_id=hypothesis.id,
            proposition="RP-6306 free tissue plasma concentration maintains >3x IC50 without cardiac QTc prolongation",
            required_evidence_type="PK / Exposure / Safety",
            state="unresolved",
            threshold_value="Free Cmin / IC50 > 3.0",
            evidence_references=[]
        )
        session.add_all([po1, po2, po3])

        # Alternative Mechanism
        alt_mech = AlternativeMechanism(
            hypothesis_id=hypothesis.id,
            mechanism_name="Off-Target WEE1 Kinase Cross-Inhibition",
            description="Apparent cytotoxicity of RP-6306 is mediated by off-target WEE1 inhibition rather than selective PKMYT1 engagement.",
            evidence_support=0.22,
            discriminating_assay="PKMYT1 CRISPR Knockout rescue assay using WEE1-resistant expression construct"
        )
        session.add(alt_mech)

        # 10. Candidate Interventions
        cand1 = CandidateIntervention(
            program_id=program.id,
            name="RP-6306 (Selective PKMYT1 Inhibitor)",
            smiles="CC1=C(C=C(C=C1)C2=NC(=NC(=C2)N)N3CCN(CC3)C(=O)C4CC4)NC(=O)C5=CC=C(C=C5)F",
            modality="small_molecule",
            primary_target="PKMYT1",
            cpi_score=0.82,
            novelty_score=0.75,
            overall_status="ADVANCE"
        )
        cand2 = CandidateIntervention(
            program_id=program.id,
            name="Dinaciclib (CDK1/2/5/9 Inhibitor)",
            smiles="CCC1=C(N=C2N1C(=NC(=N2)NC3=CC=C(C=C3)O)N4CCCC4C5=CC=CN=C5)CO",
            modality="small_molecule",
            primary_target="CDK2",
            cpi_score=0.45,
            novelty_score=0.20,
            overall_status="HOLD"
        )
        session.add_all([cand1, cand2])
        await session.flush()

        # Pharmacology & Safety
        pharm1 = PharmacologyAssessment(
            candidate_id=cand1.id,
            molecular_weight=428.5,
            clogp=2.9,
            h_bond_donors=2,
            h_bond_acceptors=5,
            tpsa=76.2,
            rotatable_bonds=5,
            rule_of_five_violations=0,
            binding_affinity_nm=18.5,
            docking_status="Provider not configured"
        )
        safety1 = SafetyAssessment(
            candidate_id=cand1.id,
            herg_liability="LOW",
            hepatotoxicity_liability="LOW",
            genotoxicity_liability="LOW",
            safety_gate_passed=True
        )
        session.add_all([pharm1, safety1])

        # 11. Experiment Plan & Run
        exp_plan = ExperimentPlan(
            hypothesis_id=hypothesis.id,
            scientific_objective="Determine RP-6306 3D Spheroid Organoid cytotoxicity and driver reversal in CCNE1-amplified organoids",
            recommended_assay="3D Spheroid Cell Viability & Phospho-CDK1 Y15 Western Blot",
            biological_model="Patient-Derived Organoid HGSOC-042 (CCNE1 Amp)",
            expected_voi=0.82,
            estimated_cost_usd=4800.0,
            estimated_duration_days=10,
            advance_threshold="IC50 < 50 nM with >80% maximal cell death in CCNE1-amplified organoid",
            terminate_threshold="IC50 > 5 uM",
            status="completed"
        )
        session.add(exp_plan)
        await session.flush()

        exp_run = ExperimentRun(
            plan_id=exp_plan.id,
            executed_by=user.id,
            summary_result="positive",
            measured_values={"measured_ic50_nm": 22.4, "phospho_cdk1_inhibition_pct": 89.5, "viability_reduction_pct": 84.0}
        )
        session.add(exp_run)

        # 12. Decision
        decision = Decision(
            hypothesis_id=hypothesis.id,
            outcome=DecisionOutcome.ADVANCE,
            rationale="RP-6306 demonstrated potent 22.4 nM IC50 synthetic lethality in CCNE1-amplified HGSOC organoids with selective PKMYT1 target engagement and zero hERG liability.",
            supporting_evidence_ids=[ev_record.id],
            reviewer_id=user.id
        )
        session.add(decision)

        # 13. Digital Twin
        twin = DigitalTwinSnapshot(
            program_id=program.id,
            snapshot_index=1,
            trigger_event="Tutorial Dataset Initialization & Experiment Run Validation",
            program_state={
                "disease": program.disease,
                "indication": program.indication,
                "top_candidate": cand1.name,
                "top_candidate_cpi": cand1.cpi_score,
                "decision_outcome": "ADVANCE",
                "notes": "SYNTHETIC TUTORIAL DATA — NOT SCIENTIFIC EVIDENCE"
            }
        )
        session.add(twin)

        # 14. Model Provider
        provider = ModelProvider(
            provider_name="TheraDOS Internal Rules Compiler",
            is_configured=True,
            status_reason="Active"
        )
        session.add(provider)

        await session.commit()
        print("Tutorial dataset successfully seeded!")

if __name__ == "__main__":
    asyncio.run(seed_tutorial_data())
