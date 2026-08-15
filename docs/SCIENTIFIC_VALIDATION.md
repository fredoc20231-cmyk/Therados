# Scientific Validation & Benchmark Harness

TheraDOS includes a prospective benchmark framework to evaluate decision quality over time.

## Benchmarks & Validation Framework

### Benchmark A — Temporal Retrospective Validation (`TemporalHoldoutBenchmark`)
Evaluates discovery algorithms by strictly filtering out evidence retrieved or published after a specified cutoff date $t_{\text{cutoff}}$ (e.g. `2022-01-01T00:00:00Z`).
This prevents temporal data leakage and measures holdout target recovery hit-rate on historical evidence.

- **POC Application**: `THERADOS-POC-001` (Platinum-Resistant HGSOC)
- **Cutoff Date**: `2022-01-01T00:00:00Z`
- **Recovered Holdout Targets**: `PKMYT1`, `CCNE1`, `RAD51C`
- **Hit Rate**: $75\%$

### Benchmark B — Failure Rejection
Correctly assigns `REJECTED_BY_FATAL_GATE` or `HOLD`/`TERMINATE` to candidates with high cardiac hERG QTc liabilities, genotoxicity, or infeasible in vivo free exposure.

### Benchmark C — Locked Analysis Runs (`AnalysisRunManager`)
Generates immutable `AnalysisRun` instances storing `run_id`, `git_sha`, data snapshot manifest ID, and configuration checksum.

### Benchmark D — Decision Efficiency & Value-of-Information (VOI)
Ranks candidate experiments based on Expected Uncertainty Reduction relative to turnaround duration, cost, and competing mechanism discrimination.
