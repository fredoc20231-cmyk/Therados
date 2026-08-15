"""
Triclique Augmentation Engine for Multipartite Biomedical Knowledge Graphs.

Identifies missing candidate edges (e.g. Drug-Target or Target-Disease) by detecting
incomplete 3-partite cliques (e.g., Drug-Target-Disease) and computing neighborhood overlap,
hub penalties, and source diversity.
"""

from typing import List, Dict, Set, Tuple, Any
import math

class TricliqueEngine:
    def __init__(self, hub_threshold: int = 50) -> None:
        self.hub_threshold = hub_threshold

    def find_candidate_edges(
        self,
        drugs: List[str],
        targets: List[str],
        diseases: List[str],
        drug_target_edges: List[Tuple[str, str]],
        target_disease_edges: List[Tuple[str, str]],
        drug_disease_edges: List[Tuple[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Enumerates qualifying 3-partite neighborhoods (Drug, Target, Disease)
        and predicts candidate missing Drug-Target or Target-Disease edges based on structural support.
        """
        dt_set: Set[Tuple[str, str]] = set(drug_target_edges)
        td_set: Set[Tuple[str, str]] = set(target_disease_edges)
        dd_set: Set[Tuple[str, str]] = set(drug_disease_edges)

        # Build adjacency maps
        drug_targets: Dict[str, Set[str]] = {}
        for d, t in dt_set:
            drug_targets.setdefault(d, set()).add(t)

        target_diseases: Dict[str, Set[str]] = {}
        for t, dis in td_set:
            target_diseases.setdefault(t, set()).add(dis)

        drug_diseases: Dict[str, Set[str]] = {}
        for d, dis in dd_set:
            drug_diseases.setdefault(d, set()).add(dis)

        candidate_predictions: Dict[Tuple[str, str, str], Dict[str, Any]] = {}

        # Search for incomplete tricliques (d, t, dis) where:
        # - (d, dis) is known AND (t, dis) is known, but (d, t) is missing -> Candidate Drug-Target edge
        # - OR (d, t) is known AND (d, dis) is known, but (t, dis) is missing -> Candidate Target-Disease edge
        for d in drugs:
            known_dis = drug_diseases.get(d, set())
            for dis in known_dis:
                for t in targets:
                    has_dt = (d, t) in dt_set
                    has_td = (t, dis) in td_set

                    if has_td and not has_dt:
                        key = ("drug_target", d, t)
                        if key not in candidate_predictions:
                            candidate_predictions[key] = {
                                "type": "candidate_drug_target",
                                "source": d,
                                "target": t,
                                "supporting_diseases": [],
                                "structural_score": 0.0
                            }
                        candidate_predictions[key]["supporting_diseases"].append(dis)

                    elif has_dt and not has_td:
                        key = ("target_disease", t, dis)
                        if key not in candidate_predictions:
                            candidate_predictions[key] = {
                                "type": "candidate_target_disease",
                                "source": t,
                                "target": dis,
                                "supporting_drugs": [],
                                "structural_score": 0.0
                            }
                        candidate_predictions[key]["supporting_drugs"].append(d)

        results: List[Dict[str, Any]] = []
        for key, cand in candidate_predictions.items():
            if cand["type"] == "candidate_drug_target":
                support_count = len(cand["supporting_diseases"])
                # Apply hub penalty if target connects to too many diseases
                t_degree = len(target_diseases.get(cand["target"], set()))
                hub_penalty = 1.0 / (1.0 + math.log(1 + max(0, t_degree - 10)))
                raw_score = 1.0 - math.exp(-0.5 * support_count)
                cand["structural_score"] = round(raw_score * hub_penalty, 3)
                cand["explanation"] = (
                    f"Predicted Drug-Target edge ({cand['source']} -> {cand['target']}) "
                    f"supported by {support_count} shared disease pathway(s) [{', '.join(cand['supporting_diseases'][:3])}]."
                )
            else:
                support_count = len(cand["supporting_drugs"])
                raw_score = 1.0 - math.exp(-0.5 * support_count)
                cand["structural_score"] = round(raw_score, 3)
                cand["explanation"] = (
                    f"Predicted Target-Disease edge ({cand['source']} -> {cand['target']}) "
                    f"supported by {support_count} shared targeting drug(s) [{', '.join(cand['supporting_drugs'][:3])}]."
                )
            results.append(cand)

        # Sort by structural support score descending
        results.sort(key=lambda x: x["structural_score"], reverse=True)
        return results
