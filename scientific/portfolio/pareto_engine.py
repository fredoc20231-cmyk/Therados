"""
Multi-Objective Pareto Portfolio Engine.

Ranks candidate interventions using non-dominated sorting across distinct scientific dimensions.
Handles missing data gracefully and separates candidates into:
1. feasible_frontier
2. incomplete_evidence
3. fatal_gate_failures
"""

from typing import List, Dict, Any, Optional

class ParetoPortfolioEngine:
    def rank_candidates(
        self,
        candidates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates Pareto non-dominated frontiers across candidates.
        Do NOT compress everything into one opaque single score!
        """
        if not candidates:
            return {
                "feasible_frontier": [],
                "incomplete_evidence": [],
                "fatal_gate_failures": [],
                "total_candidates_evaluated": 0
            }

        feasible_candidates = []
        incomplete_candidates = []
        fatal_gate_failures = []

        for c in candidates:
            c_copy = dict(c)
            gate_status = c_copy.get("gate_status", "UNRESOLVED")

            # Check fatal gate failures
            if gate_status == "REJECTED_BY_FATAL_GATE" or c_copy.get("safety_gate_passed") is False:
                c_copy["pareto_category"] = "FATAL_GATE_FAILURE"
                fatal_gate_failures.append(c_copy)
                continue

            # Check if required metrics are present
            cpi = c_copy.get("cpi_score")
            novelty = c_copy.get("novelty_score")

            if cpi is None or novelty is None or gate_status == "UNRESOLVED_EVIDENCE_REQUIRED":
                c_copy["pareto_category"] = "INCOMPLETE_EVIDENCE"
                incomplete_candidates.append(c_copy)
                continue

            c_copy["cpi_metric"] = float(cpi)
            c_copy["novelty_metric"] = float(novelty)
            c_copy["is_frontier"] = True
            feasible_candidates.append(c_copy)

        # Non-dominated sorting on feasible candidates
        for i, c1 in enumerate(feasible_candidates):
            for j, c2 in enumerate(feasible_candidates):
                if i != j and c1["is_frontier"]:
                    c2_better_cpi = c2["cpi_metric"] >= c1["cpi_metric"]
                    c2_better_nov = c2["novelty_metric"] >= c1["novelty_metric"]
                    c2_strictly_better = (c2["cpi_metric"] > c1["cpi_metric"]) or (c2["novelty_metric"] > c1["novelty_metric"])

                    if c2_better_cpi and c2_better_nov and c2_strictly_better:
                        c1["is_frontier"] = False
                        break

        feasible_frontier = []
        dominated_candidates = []

        for c in feasible_candidates:
            if c.get("is_frontier"):
                c["pareto_rank"] = "TIER_A_PARETO_FRONTIER"
                c["pareto_category"] = "FEASIBLE_FRONTIER"
                feasible_frontier.append(c)
            else:
                c["pareto_rank"] = "TIER_B_DOMINATED"
                c["pareto_category"] = "FEASIBLE_DOMINATED"
                dominated_candidates.append(c)

        return {
            "total_candidates_evaluated": len(candidates),
            "feasible_frontier_count": len(feasible_frontier),
            "feasible_frontier": feasible_frontier,
            "dominated_candidates": dominated_candidates,
            "incomplete_evidence": incomplete_candidates,
            "fatal_gate_failures": fatal_gate_failures
        }
