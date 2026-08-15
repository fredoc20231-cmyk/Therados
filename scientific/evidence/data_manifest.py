"""
Data Snapshot Manifest Builder.

Records provider queries, API endpoints, retrieval timestamps, SHA-256 checksums,
normalization versions, and data transformation lineage for reproducible discovery runs.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import hashlib

class DataSnapshotRecord(BaseModel):
    record_id: str
    provider_name: str
    endpoint: str
    query_parameters: Dict[str, Any]
    retrieval_timestamp: str
    payload_checksum_sha256: str
    normalization_version: str = "TheraDOS-Norm-v1.0"
    is_synthetic: bool = False

class DataSnapshotManifest(BaseModel):
    manifest_id: str
    program_id: str
    project_mode: str = "REAL"
    created_at: str
    git_sha: Optional[str] = None
    records: List[DataSnapshotRecord] = Field(default_factory=list)
    total_records_count: int = 0
    provenance_hash: str

class DataSnapshotManifestBuilder:
    def create_manifest(
        self,
        program_id: str,
        project_mode: str,
        provider_results: List[Dict[str, Any]],
        git_sha: Optional[str] = None
    ) -> DataSnapshotManifest:
        now_str = datetime.now(timezone.utc).isoformat()
        records: List[DataSnapshotRecord] = []

        for idx, res in enumerate(provider_results):
            rec_id = f"REC-{idx+1:04d}"
            prov = res.get("provider", "Unknown Provider")
            endp = res.get("endpoint", "Internal")
            payload_str = str(res)
            checksum = hashlib.sha256(payload_str.encode()).hexdigest()

            records.append(DataSnapshotRecord(
                record_id=rec_id,
                provider_name=prov,
                endpoint=endp,
                query_parameters={"disease": res.get("disease_efo_id", "HGSOC")},
                retrieval_timestamp=now_str,
                payload_checksum_sha256=checksum,
                is_synthetic=res.get("is_synthetic", False)
            ))

        manifest_raw = f"{program_id}:{project_mode}:{now_str}:{len(records)}"
        manifest_hash = hashlib.sha256(manifest_raw.encode()).hexdigest()

        return DataSnapshotManifest(
            manifest_id=f"MANIFEST-{manifest_hash[:10].upper()}",
            program_id=program_id,
            project_mode=project_mode,
            created_at=now_str,
            git_sha=git_sha,
            records=records,
            total_records_count=len(records),
            provenance_hash=manifest_hash
        )
