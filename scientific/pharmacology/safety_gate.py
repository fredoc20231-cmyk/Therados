"""
Hard Feasibility Gates Engine.

Evaluates safety liabilities, exposure feasibility, and direction-of-effect constraints.
A candidate failing any hard fatal gate CANNOT advance regardless of graph score.
"""

from typing import Dict, Any, List

class HardSafetyGateEngine:
    def evaluate_gates(
        self,
        herg_liability: str = "LOW",
        hepatotoxicity_liability: str = "LOW",
        genotoxicity_liability: str = "LOW",
        free_concentration_nm: float = 100.0,
        required_ic50_nm: float = 50.0,
        target_expressed_in_context: bool = True,
        direction_of_effect_valid: bool = True
    ) -> Dict[str, Any]:
        """
        Evaluates hard gates:
        1. Direction of Effect (e.g. activating an oncogene is fatal)
        2. Target Expression in Context
        3. Exposure Feasibility (Free concentration >= IC50)
        4. Fatal Toxicities (Genotoxicity HIGH or hERG HIGH)
        """
        failed_gates: List[str] = []

        if not direction_of_effect_valid:
            failed_gates.append("FATAL_GATE: Invalid direction of effect (target action exacerbates disease pathway)")

        if not target_expressed_in_context:
            failed_gates.append("FATAL_GATE: Target is not expressed in disease cellular context")

        if free_concentration_nm < required_ic50_nm:
            failed_gates.append(f"FATAL_GATE: Exposure infeasible (Free concentration {free_concentration_nm}nM < required IC50 {required_ic50_nm}nM)")

        if genotoxicity_liability.upper() == "HIGH":
            failed_gates.append("FATAL_GATE: High genotoxicity liability detected")

        if herg_liability.upper() == "HIGH":
            failed_gates.append("FATAL_GATE: High hERG cardiac QT prolongation liability")

        passed = len(failed_gates) == 0

        return {
            "passed": passed,
            "failed_gates": failed_gates,
            "gate_status": "PASS" if passed else "REJECTED_BY_FATAL_GATE",
            "decision_recommendation": "FEASIBLE" if passed else "SAFETY_OR_EXPOSURE_REJECTED"
        }
