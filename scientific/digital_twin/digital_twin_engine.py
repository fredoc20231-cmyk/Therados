"""
Therapeutic Program Digital Twin Engine.

Maintains an append-only state timeline recording how program beliefs,
hypotheses, and decision status evolve over time.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone

class DigitalTwinEngine:
    def create_snapshot(
        self,
        program_id: str,
        current_index: int,
        trigger_event: str,
        hypotheses_state: List[Dict[str, Any]],
        candidates_state: List[Dict[str, Any]],
        latest_decision: str
    ) -> Dict[str, Any]:
        """
        Generates an immutable digital twin snapshot representing program state at timestamp t.
        """
        snapshot_payload = {
            "program_id": program_id,
            "snapshot_index": current_index + 1,
            "trigger_event": trigger_event,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "program_state": {
                "active_hypotheses_count": len(hypotheses_state),
                "hypotheses_summary": [
                    {"id": h.get("id"), "title": h.get("title"), "status": h.get("status"), "support_score": h.get("support_score")}
                    for h in hypotheses_state
                ],
                "active_candidates_count": len(candidates_state),
                "latest_program_decision": latest_decision
            }
        }
        return snapshot_payload
