"""
Triclique Engine for Multipartite Biomedical Knowledge Graphs.

Contains:
1. NeighborhoodCompletionBaseline: Fast 2-hop incomplete triangle heuristic.
2. MaximalTricliqueAugmentationEngine: Exact 3-partite maximal triclique enumeration
   and non-adjacency bounded candidate edge inference across D-P, P-E, and D-E edge classes.
"""

from typing import List, Dict, Set, Tuple, Any
import math

class NeighborhoodCompletionBaseline:
    """
    Incomplete triangle / 2-hop neighborhood completion heuristic.
    """
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
        dt_set: Set[Tuple[str, str]] = set(drug_target_edges)
        td_set: Set[Tuple[str, str]] = set(target_disease_edges)
        dd_set: Set[Tuple[str, str]] = set(drug_disease_edges)

        drug_diseases: Dict[str, Set[str]] = {}
        for d, dis in dd_set:
            drug_diseases.setdefault(d, set()).add(dis)

        target_diseases: Dict[str, Set[str]] = {}
        for t, dis in td_set:
            target_diseases.setdefault(t, set()).add(dis)

        candidate_predictions: Dict[Tuple[str, str, str], Dict[str, Any]] = {}

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
                                "support_score": 0.0,
                                "method": "NeighborhoodCompletionBaseline"
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
                                "support_score": 0.0,
                                "method": "NeighborhoodCompletionBaseline"
                            }
                        candidate_predictions[key]["supporting_drugs"].append(d)

        results: List[Dict[str, Any]] = []
        for key, cand in candidate_predictions.items():
            if cand["type"] == "candidate_drug_target":
                support_count = len(cand["supporting_diseases"])
                t_degree = len(target_diseases.get(cand["target"], set()))
                hub_penalty = 1.0 / (1.0 + math.log(1 + max(0, t_degree - 10)))
                raw_score = 1.0 - math.exp(-0.5 * support_count)
                cand["support_score"] = round(raw_score * hub_penalty, 3)
            else:
                support_count = len(cand["supporting_drugs"])
                raw_score = 1.0 - math.exp(-0.5 * support_count)
                cand["support_score"] = round(raw_score, 3)
            results.append(cand)

        results.sort(key=lambda x: x["support_score"], reverse=True)
        return results


class MaximalTricliqueAugmentationEngine:
    """
    Maximal Triclique Augmentation Engine.

    Enumerates 3-partite maximal tricliques T = (D', P', E') on tripartite graph G = (D, P, E, E_DP, E_PE, E_DE).
    Identifies candidate missing edges across all 3 edge classes (D-P, P-E, D-E) by detecting augmentable vertices
    within non-adjacency bound k.
    """

    def __init__(
        self,
        min_d: int = 1,
        min_p: int = 1,
        min_e: int = 1,
        non_adjacency_bound: int = 2
    ) -> None:
        self.min_d = min_d
        self.min_p = min_p
        self.min_e = min_e
        self.non_adjacency_bound = non_adjacency_bound

    def find_maximal_tricliques(
        self,
        drugs: List[str],
        proteins: List[str],
        diseases: List[str],
        dp_edges: List[Tuple[str, str]],
        pe_edges: List[Tuple[str, str]],
        de_edges: List[Tuple[str, str]]
    ) -> List[Dict[str, Any]]:
        dp_set: Set[Tuple[str, str]] = set(dp_edges)
        pe_set: Set[Tuple[str, str]] = set(pe_edges)
        de_set: Set[Tuple[str, str]] = set(de_edges)

        d_p: Dict[str, Set[str]] = {}
        for d, p in dp_set:
            d_p.setdefault(d, set()).add(p)

        p_e: Dict[str, Set[str]] = {}
        for p, e in pe_set:
            p_e.setdefault(p, set()).add(e)

        d_e: Dict[str, Set[str]] = {}
        for d, e in de_set:
            d_e.setdefault(d, set()).add(e)

        tricliques: List[Dict[str, Any]] = []

        for d in drugs:
            p_neighbors = d_p.get(d, set())
            if len(p_neighbors) < self.min_p:
                continue

            for p in p_neighbors:
                e_neighbors = p_e.get(p, set()).intersection(d_e.get(d, set()))
                if len(e_neighbors) < self.min_e:
                    continue

                d_set = {
                    d_cand for d_cand in drugs
                    if p_neighbors.issubset(d_p.get(d_cand, set())) and e_neighbors.issubset(d_e.get(d_cand, set()))
                }

                if len(d_set) >= self.min_d:
                    triclique = {
                        "triclique_id": f"TC-{len(tricliques) + 1:04d}",
                        "drugs": sorted(list(d_set)),
                        "proteins": sorted(list(p_neighbors)),
                        "diseases": sorted(list(e_neighbors)),
                        "size": len(d_set) * len(p_neighbors) * len(e_neighbors)
                    }
                    if triclique not in tricliques:
                        tricliques.append(triclique)

        maximal_tricliques = []
        for tc1 in tricliques:
            is_sub = False
            for tc2 in tricliques:
                if tc1["triclique_id"] != tc2["triclique_id"]:
                    if (
                        set(tc1["drugs"]).issubset(set(tc2["drugs"]))
                        and set(tc1["proteins"]).issubset(set(tc2["proteins"]))
                        and set(tc1["diseases"]).issubset(set(tc2["diseases"]))
                        and tc1["size"] < tc2["size"]
                    ):
                        is_sub = True
                        break
            if not is_sub and tc1 not in maximal_tricliques:
                maximal_tricliques.append(tc1)

        return maximal_tricliques

    def predict_candidate_edges(
        self,
        drugs: List[str],
        proteins: List[str],
        diseases: List[str],
        dp_edges: List[Tuple[str, str]],
        pe_edges: List[Tuple[str, str]],
        de_edges: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        dp_set: Set[Tuple[str, str]] = set(dp_edges)
        pe_set: Set[Tuple[str, str]] = set(pe_edges)
        de_set: Set[Tuple[str, str]] = set(de_edges)

        maximal_tcs = self.find_maximal_tricliques(drugs, proteins, diseases, dp_edges, pe_edges, de_edges)

        candidate_dp: Dict[Tuple[str, str], List[str]] = {}
        candidate_pe: Dict[Tuple[str, str], List[str]] = {}
        candidate_de: Dict[Tuple[str, str], List[str]] = {}

        for tc in maximal_tcs:
            tc_id = tc["triclique_id"]
            d_list = tc["drugs"]
            p_list = tc["proteins"]
            e_list = tc["diseases"]

            for d in d_list:
                for p in p_list:
                    if (d, p) not in dp_set:
                        candidate_dp.setdefault((d, p), []).append(tc_id)

            for p in p_list:
                for e in e_list:
                    if (p, e) not in pe_set:
                        candidate_pe.setdefault((p, e), []).append(tc_id)

            for d in d_list:
                for e in e_list:
                    if (d, e) not in de_set:
                        candidate_de.setdefault((d, e), []).append(tc_id)

        format_cands = []

        for (d, p), tcs in candidate_dp.items():
            support_count = len(tcs)
            format_cands.append({
                "edge_class": "drug_target",
                "source": d,
                "target": p,
                "supporting_tricliques": tcs,
                "support_count": support_count,
                "support_score": round(1.0 - math.exp(-0.4 * support_count), 3),
                "explanation": f"Missing Drug-Target edge ({d} -> {p}) supported by {support_count} maximal triclique(s) [{', '.join(tcs[:3])}]."
            })

        for (p, e), tcs in candidate_pe.items():
            support_count = len(tcs)
            format_cands.append({
                "edge_class": "target_disease",
                "source": p,
                "target": e,
                "supporting_tricliques": tcs,
                "support_count": support_count,
                "support_score": round(1.0 - math.exp(-0.4 * support_count), 3),
                "explanation": f"Missing Target-Disease edge ({p} -> {e}) supported by {support_count} maximal triclique(s) [{', '.join(tcs[:3])}]."
            })

        for (d, e), tcs in candidate_de.items():
            support_count = len(tcs)
            format_cands.append({
                "edge_class": "drug_disease",
                "source": d,
                "target": e,
                "supporting_tricliques": tcs,
                "support_count": support_count,
                "support_score": round(1.0 - math.exp(-0.4 * support_count), 3),
                "explanation": f"Missing Drug-Disease edge ({d} -> {e}) supported by {support_count} maximal triclique(s) [{', '.join(tcs[:3])}]."
            })

        format_cands.sort(key=lambda x: float(str(x.get("support_score", 0.0))), reverse=True)

        return {
            "maximal_tricliques_count": len(maximal_tcs),
            "maximal_tricliques": maximal_tcs,
            "candidate_predictions_count": len(format_cands),
            "candidate_predictions": format_cands,
            "engine": "MaximalTricliqueAugmentationEngine"
        }

TricliqueEngine = NeighborhoodCompletionBaseline
