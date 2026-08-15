"""
Causal Phenotype Inversion (CPI) Engine.

Computes CPI = sum(driver_reversal) - sum(harm_induction)
Evaluates drug impact on pathogenic driver modules versus critical normal cell harm modules.
"""

from typing import List, Dict, Any

class CPIEngine:
    def compute_cpi_score(
        self,
        driver_modules: List[Dict[str, Any]],
        harm_modules: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        driver_modules: list of dicts with 'name', 'weight' (0-1), 'reversal' (0-1)
        harm_modules: list of dicts with 'name', 'weight' (0-1), 'induction' (0-1)
        """
        driver_sum = 0.0
        driver_details = []
        for mod in driver_modules:
            w = float(mod.get("weight", 1.0))
            rev = float(mod.get("reversal", 0.0))
            contrib = w * rev
            driver_sum += contrib
            driver_details.append({
                "module": mod.get("name", "Unknown Driver"),
                "weight": w,
                "reversal": rev,
                "contribution": round(contrib, 3)
            })

        harm_sum = 0.0
        harm_details = []
        for mod in harm_modules:
            w = float(mod.get("weight", 1.0))
            ind = float(mod.get("induction", 0.0))
            contrib = w * ind
            harm_sum += contrib
            harm_details.append({
                "module": mod.get("name", "Unknown Harm"),
                "weight": w,
                "induction": ind,
                "contribution": round(contrib, 3)
            })

        cpi = driver_sum - harm_sum
        normalized_cpi = max(-1.0, min(1.0, cpi))

        return {
            "cpi_score": round(normalized_cpi, 3),
            "driver_reversal_sum": round(driver_sum, 3),
            "harm_induction_sum": round(harm_sum, 3),
            "driver_breakdown": driver_details,
            "harm_breakdown": harm_details,
            "interpretation": (
                "Net positive driver reversal in pathogenic cells without severe normal cell harm induction"
                if normalized_cpi > 0.3 else
                "Harm induction outweighs or cancels driver reversal benefits"
            )
        }
