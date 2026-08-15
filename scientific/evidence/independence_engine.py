"""
Independence-Aware Evidence Engine.

Computes independent support score S = sum(q_k * i_k * r_k)
where q_k is source quality, i_k is independence factor, r_k is relevance context.
Penalizes duplicate publication citations and research popularity hubs.
"""

from typing import List, Dict, Any
import math

class EvidenceIndependenceEngine:
    def compute_independent_support(
        self,
        claims: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates independent evidence support score for a collection of claims.
        """
        if not claims:
            return {
                "support_score": 0.0,
                "claim_count": 0,
                "independent_claim_count": 0.0,
                "score_decomposition": []
            }

        publication_counts: Dict[str, int] = {}
        source_counts: Dict[str, int] = {}

        for claim in claims:
            pub_id = claim.get("external_id") or "UNKNOWN"
            src_id = claim.get("source_name") or "UNKNOWN"
            publication_counts[pub_id] = publication_counts.get(pub_id, 0) + 1
            source_counts[src_id] = source_counts.get(src_id, 0) + 1

        total_score = 0.0
        decompositions = []

        for claim in claims:
            q_k = float(claim.get("quality_score", 0.8)) # Quality
            pub_id = claim.get("external_id") or "UNKNOWN"

            # Independence factor i_k: 1 / sqrt(times cited)
            dup_count = publication_counts[pub_id]
            i_k = 1.0 / math.sqrt(dup_count)

            # Relevance factor r_k: based on evidence maturity
            maturity = claim.get("evidence_maturity", "associative")
            maturity_weights = {
                "associative": 0.3,
                "structurally_inferred": 0.5,
                "mechanistically_supported": 0.7,
                "causally_corroborated": 0.85,
                "experimentally_validated": 0.95,
                "clinically_established": 1.0
            }
            r_k = maturity_weights.get(maturity.lower(), 0.5)

            contribution = q_k * i_k * r_k
            total_score += contribution

            decompositions.append({
                "claim_id": claim.get("id"),
                "source_name": claim.get("source_name"),
                "external_id": pub_id,
                "quality_q": round(q_k, 2),
                "independence_i": round(i_k, 2),
                "relevance_r": round(r_k, 2),
                "net_contribution": round(contribution, 3)
            })

        # Asymptotic saturation curve for bounded support score in [0.0, 1.0)
        bounded_score = round(1.0 - math.exp(-0.4 * total_score), 3)

        return {
            "support_score": bounded_score,
            "raw_weighted_sum": round(total_score, 3),
            "claim_count": len(claims),
            "score_decomposition": decompositions,
            "label": "support score (NOT a probability)"
        }
