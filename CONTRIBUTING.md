# Contributing to TheraDOS

We welcome contributions to TheraDOS! Please review our core scientific and engineering principles before submitting code.

## Scientific Integrity
- All evidence records MUST preserve complete provenance.
- Do NOT introduce heuristic mock numbers into production pipelines.
- Ensure all hard gates are tested with negative controls.

## Development Workflow
1. Run `make verify` before submitting pull requests.
2. Ensure all backend code passes `ruff` and `mypy`.
3. Ensure frontend passes `npm run typecheck` and `npm run build`.
