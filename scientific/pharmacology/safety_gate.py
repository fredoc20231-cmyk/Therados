"""
Hard Feasibility Gates Engine.

Evaluates safety liabilities, exposure feasibility, target context expression, and direction-of-effect constraints.
Enforces conservative missing-data semantics: missing evidence yields UNRESOLVED, NOT PASS.
"""

from typing import Dict, Any, List, Optional
import enum

class GateOutcome(str, enum.Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNRESOLVED = "UNRESOLVED"
    NOT_EVALUATED = "NOT_EVALUATED"

class HardSafetyGateEngine:
    def evaluate_gates(
        self,
        herg_liability: Optional[str] = None, # LOW, MEDIUM, HIGH, None
        hepatotoxicity_liability: Optional[str] = None,
        genotoxicity_liability: Optional[str] = None,
        free_concentration_nm: Optional[float] = None,
        required_ic50_nm: Optional[float] = None,
        target_expressed_in_context: Optional[bool] = None,
        direction_of_effect_valid: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Evaluates hard gates conservatively.
        Missing data leads to UNRESOLVED, never default PASS.
        """
        failed_gates: List[str] = []
        unresolved_gates: List[str] = []
        passed_gates: List[str] = []

        # 1. Direction of Effect
        if direction_of_effect_valid is False:
            failed_gates.append("FATAL_GATE: Invalid direction of effect (target action exacerbates disease pathway)")
        elif direction_of_effect_valid is True:
            passed_gates.append("GATE: Direction of effect validated")
        else:
            unresolved_gates.append("UNRESOLVED_GATE: Direction of effect unconfirmed")

        # 2. Target Expression in Context
        if target_expressed_in_context is False:
            failed_gates.append("FATAL_GATE: Target is not expressed in disease cellular context")
        elif target_expressed_in_context is True:
            passed_gates.append("GATE: Target context expression confirmed")
        else:
            unresolved_gates.append("UNRESOLVED_GATE: Target context expression unconfirmed")

        # 3. Exposure Feasibility
        if free_concentration_nm is not None and required_ic50_nm is not None:
            if free_concentration_nm < required_ic50_nm:
                failed_gates.append(f"FATAL_GATE: Infeasible exposure (Free concentration {free_concentration_nm}nM < required IC50 {required_ic50_nm}nM)")
            else:
                passed_gates.append("GATE: Exposure feasibility confirmed")
        else:
            unresolved_gates.append("UNRESOLVED_GATE: Free exposure or required IC50 unmeasured")

        # 4. Cardiac hERG
        if herg_liability is not None:
            if herg_liability.upper() == "HIGH":
                failed_gates.append("FATAL_GATE: High hERG cardiac QTc prolongation liability")
            elif herg_liability.upper() in ["LOW", "MEDIUM"]:
                passed_gates.append("GATE: hERG liability within acceptable parameters")
            else:
                unresolved_gates.append("UNRESOLVED_GATE: hERG liability unmeasured")
        else:
            unresolved_gates.append("UNRESOLVED_GATE: hERG liability unmeasured")

        # 5. Genotoxicity
        if genotoxicity_liability is not None:
            if genotoxicity_liability.upper() == "HIGH":
                failed_gates.append("FATAL_GATE: High genotoxicity liability detected")
            elif genotoxicity_liability.upper() in ["LOW", "MEDIUM"]:
                passed_gates.append("GATE: Genotoxicity acceptable")
            else:
                unresolved_gates.append("UNRESOLVED_GATE: Genotoxicity unmeasured")
        else:
            unresolved_gates.append("UNRESOLVED_GATE: Genotoxicity unmeasured")

        # Determine overall outcome
        if failed_gates:
            overall = GateOutcome.FAIL
        elif unresolved_gates:
            overall = GateOutcome.UNRESOLVED
        elif passed_gates:
            overall = GateOutcome.PASS
        else:
            overall = GateOutcome.NOT_EVALUATED

        return {
            "overall_outcome": overall.value,
            "passed": overall == GateOutcome.PASS,
            "failed_gates": failed_gates,
            "unresolved_gates": unresolved_gates,
            "passed_gates": passed_gates,
            "gate_status": (
                "PASS" if overall == GateOutcome.PASS else
                ("REJECTED_BY_FATAL_GATE" if overall == GateOutcome.FAIL else "UNRESOLVED_EVIDENCE_REQUIRED")
            ),
            "decision_recommendation": (
                "FEASIBLE" if overall == GateOutcome.PASS else
                ("SAFETY_OR_EXPOSURE_REJECTED" if overall == GateOutcome.FAIL else "HOLD_EXPERIMENT_REQUIRED")
            )
        }
