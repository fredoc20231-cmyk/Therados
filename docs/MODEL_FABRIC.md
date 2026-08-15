# Model Fabric Specification

The Model Fabric provides a provider-neutral abstraction layer for computational models and LLMs.

## Supported Providers
- **LLM Providers**: OpenAI, Anthropic, Gemini, Local vLLM/Ollama
- **Molecular Providers**: RDKit (local), AutoDock Vina (adapter)
- **Graph Engines**: Native Triclique Engine, Neo4j Graph Data Science

## Citation & Grounding Protocol
All copilot responses and model outputs MUST cite internal `EvidenceRecord` IDs. Models cannot introduce ungrounded claims into persistent storage without explicit user confirmation (`PROPOSED` state).
