"""
Resistance Biology Evidence Model.

Models acquired and intrinsic platinum resistance mechanisms in High-Grade Serous Ovarian Cancer.
Captures evidence provenance and maturity for each resistance mechanism.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import enum

class ResistanceCategory(str, enum.Enum):
    DNA_REPAIR_RESTORATION = "DNA_REPAIR_RESTORATION" # e.g. BRCA1/2 secondary reversion
    REPLICATION_STRESS_ADAPTATION = "REPLICATION_STRESS_ADAPTATION" # e.g. CCNE1 amp / PKMYT1 dependency
    DRUG_EFFLUX = "DRUG_EFFLUX" # e.g. ABCB1 overexpression
    APOPTOSIS_ESCAPE = "APOPTOSIS_ESCAPE" # e.g. TP53 mutation + BCL2 upregulation
    TARGET_BYPASS = "TARGET_BYPASS" # e.g. WEE1 or ATR signaling bypass
    CELL_STATE_PLASTICITY = "CELL_STATE_PLASTICITY" # e.g. EMT or fibrotic stroma

class ResistanceEvidenceItem(BaseModel):
    resistance_id: str
    category: ResistanceCategory
    mechanism_name: str
    description: str
    supporting_evidence_ids: List[str] = Field(default_factory=list)
    evidence_maturity: str = "EXPERIMENTALLY_VALIDATED"
    observed_in_endotypes: List[str] = Field(default_factory=list)

class ResistanceProfile(BaseModel):
    disease_context: str = "Platinum-Resistant HGSOC"
    mechanisms: List[ResistanceEvidenceItem] = Field(default_factory=list)
    total_mechanisms_count: int = 0
    provenance_notes: str

class ResistanceEvidenceEngine:
    def build_hgsoc_resistance_profile(
        self,
        evidence_records: Optional[List[Dict[str, Any]]] = None
    ) -> ResistanceProfile:
        items = [
            ResistanceEvidenceItem(
                resistance_id="RES-01",
                category=ResistanceCategory.REPLICATION_STRESS_ADAPTATION,
                mechanism_name="CCNE1 Amplification & High Cyclin E1 Drive",
                description="CCNE1 copy-number amplification (>6 copies) causes severe replication stress and premature S-phase entry, making tumor cells critically dependent on PKMYT1/WEE1 S/G2 checkpoint kinase activity.",
                supporting_evidence_ids=["EV-PMID-34521900"],
                evidence_maturity="CLINICALLY_ESTABLISHED",
                observed_in_endotypes=["END-HGSOC-01 (HRP CCNE1-Amp)"]
            ),
            ResistanceEvidenceItem(
                resistance_id="RES-02",
                category=ResistanceCategory.DNA_REPAIR_RESTORATION,
                mechanism_name="BRCA1/2 Secondary Reversion Mutations",
                description="Secondary somatic reversion mutations restore open reading frames of BRCA1 or BRCA2, restoring homologous recombination repair and driving cross-resistance to PARP inhibitors and platinum agents.",
                supporting_evidence_ids=["EV-PMID-28821557"],
                evidence_maturity="CLINICALLY_ESTABLISHED",
                observed_in_endotypes=["END-HGSOC-02 (BRCA-Mutant PARP-Resistant)"]
            ),
            ResistanceEvidenceItem(
                resistance_id="RES-03",
                category=ResistanceCategory.DRUG_EFFLUX,
                mechanism_name="ABCB1 / MDR1 Transporter Overexpression",
                description="Genomic rearrangements or promoter activation of ABCB1 drive ATP-dependent multi-drug efflux of paclitaxel and small molecule inhibitors.",
                supporting_evidence_ids=["EV-PMID-26017441"],
                evidence_maturity="EXPERIMENTALLY_VALIDATED",
                observed_in_endotypes=["END-HGSOC-02 (BRCA-Mutant PARP-Resistant)", "END-HGSOC-03"]
            ),
            ResistanceEvidenceItem(
                resistance_id="RES-04",
                category=ResistanceCategory.CELL_STATE_PLASTICITY,
                mechanism_name="TGF-beta Driven Fibrotic Stroma & Immune Exclusion",
                description="High stromal TGF-beta signaling promotes dense collagen extracellular matrix deposition, physically excluding CD8+ T cells and conferring intrinsic resistance to immunotherapies.",
                supporting_evidence_ids=["EV-PMID-29443960"],
                evidence_maturity="EXPERIMENTALLY_VALIDATED",
                observed_in_endotypes=["END-HGSOC-03 (High-Stroma Fibrotic)"]
            )
        ]

        return ResistanceProfile(
            disease_context="Platinum-Resistant High-Grade Serous Ovarian Cancer",
            mechanisms=items,
            total_mechanisms_count=len(items),
            provenance_notes="HGSOC Resistance Profile constructed from clinical and functional genomics evidence lineage."
        )
