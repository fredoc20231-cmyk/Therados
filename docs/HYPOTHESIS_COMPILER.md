# Hypothesis Compiler Specification

The Therapeutic Hypothesis Compiler converts a contextual hypothesis $H$ into an executable **Compiled Hypothesis Dossier**.

## Compiler Pipeline
1. **Proposition Construction**: Formalizes intervention, target set, action, and context.
2. **Proof Obligation Emission**: Generates mandatory requirements:
   - Target expression in context cell/tissue
   - Functional action is directionally beneficial
   - Engagement attainable at safe exposure
   - Phenotype reversal confirmed in disease endotype
3. **Evidence Association**: Maps `EvidenceClaim` records to proof obligations.
4. **Gap Analysis**: Identifies unresolved obligations.
5. **Alternative Mechanism Generation**: Constructs competing explanations.
6. **Hard Gate Evaluation**: Evaluates exposure, safety, and direction gates.
7. **Dossier Serialization**: Outputs JSON/HTML/CSV dossier with complete provenance.
