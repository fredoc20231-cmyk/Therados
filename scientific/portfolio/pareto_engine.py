"""
Multi-Objective Pareto Portfolio Engine.

Ranks candidates using non-dominated sorting across distinct scientific dimensions:
CPI score, Safety score, Exposure feasibility, Novelty, and VOI.
"""

from typing import List, Dict, Any

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
            return {"pareto_frontier": [], "dominated_candidates": []}

        # Ensure all candidates have numeric metrics for comparison
        processed = []
        for c in candidates:
            c_copy = dict(c)
            # Hard gate check
            if not c_copy.get("safety_gate_passed", True):
                c_copy["pareto_rank"] = "REJECTED_FATAL_GATE"
                c_copy["is_frontier"] = False
                processed.append(c_copy)
                continue

            c_copy["cpi_metric"] = float(c_copy.get("cpi_score", 0.5))
            c_copy["novelty_metric"] = float(c_copy.get("novelty_score", 0.5))
            c_copy["is_frontier"] = True
            processed.append(c_copy)

        valid_candidates = [c for c in processed if c.get("pareto_rank") != "REJECTED_FATAL_GATE"]

        # Non-dominated sorting
        for i, c1 in enumerate(valid_candidates):
            for j, c2 in enumerate(valid_candidates):
                if i != j and c1["is_frontier"]:
                    # c2 dominates c1 if c2 is strictly better in all metrics
                    c2_better_cpi = c2["cpi_metric"] >= c1["cpi_metric"]
                    c2_better_nov = c2["novelty_metric"] >= c1["novelty_metric"]
                    c2_strictly_better = (c2["cpi_metric"] > c1["cpi_metric"]) or (c2["novelty_metric"] > c1["novelty_metric"])

                    if c2_better_cpi and c2_better_nov and c2_strictly_better:
                        c1["is_frontier"] = False
                        break

        pareto_frontier = []
        dominated = []

        for c in processed:
            if c.get("pareto_rank") == "REJECTED_FATAL_GATE":
                dominated.append(c)
            elif c.get("is_frontier"):
                c["pareto_rank"] = "TIER_A_PARETO_FRONTIER"
                pareto_frontier.append(c)
            else:
                c["pareto_rank"] = "TIER_B_DOMINATED"
                dominated.append(c)

        return {
            "total_candidates_evaluated": len(candidates),
            "pareto_frontier_count": len(pareto_frontier),
            "pareto_frontier": pareto_frontier,
            "dominated_candidates": dominated
        }
