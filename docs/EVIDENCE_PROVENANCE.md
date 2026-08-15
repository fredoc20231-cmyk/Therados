# Evidence Provenance Specification

Every piece of evidence in TheraDOS is backed by an immutable `EvidenceRecord`.

## Fields
- `id`: UUID
- `source_id`: Source reference
- `external_id`: Original source ID (e.g. PubMed ID, ChEMBL ID)
- `evidence_type`: Literature, Assay, Omics, Structure, ClinicalTrial, Inferred
- `evidence_maturity`: Associative, Structurally Inferred, Mechanistically Supported, Causally Corroborated, Experimentally Validated, Clinically Established
- `raw_payload_url`: Pointer to MinIO/S3 payload
- `checksum`: SHA-256 hash
- `retrieval_timestamp`: UTC datetime
- `quality_score`: Normalized source quality $q_k \in [0, 1]$
- `lineage_parent_ids`: Parent evidence records if derived
