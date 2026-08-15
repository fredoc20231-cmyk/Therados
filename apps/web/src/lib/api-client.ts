import axios, { AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor for Auth Token
apiClient.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('therados_auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Structured Error Handling Interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      const detail = (error.response.data as any)?.detail || error.message;
      console.error(`[TheraDOS API Error ${error.response.status}]:`, detail);
    } else if (error.request) {
      console.error('[TheraDOS API Network Error]: Server unreachable or timeout');
    }
    return Promise.reject(error);
  }
);

export interface Program {
  id: string;
  project_id: string;
  disease: string;
  indication: string;
  patient_context?: string;
  disease_stage?: string;
  treatment_context?: string;
  program_objective: string;
  status: string;
}

export interface ProofObligation {
  id: string;
  proposition: string;
  required_evidence_type: string;
  state: string;
  threshold_value: string;
  evidence_references: string[];
  source_type: string;
  rule_provenance: string;
}

export interface AlternativeMechanism {
  mechanism_id: string;
  mechanism_statement: string;
  description: string;
  evidence_status: string;
  discriminating_experiment_candidates: string[];
}

export interface Hypothesis {
  id: string;
  program_id: string;
  title: string;
  intervention_name: string;
  intended_target: string;
  intended_action: string;
  cellular_context: string;
  disease_endotype: string;
  genomic_background?: string;
  predictive_biomarkers: string[];
  maturity: string;
  support_score: number;
  status: string;
  version: number;
  proof_obligations?: ProofObligation[];
  alternative_mechanisms?: AlternativeMechanism[];
}

export interface Candidate {
  id: string;
  program_id: string;
  name: string;
  smiles?: string;
  modality: string;
  primary_target: string;
  cpi_score: number;
  novelty_score: number;
  overall_status: string;
  molecular_weight?: number;
  clogp?: number;
  safety_gate_passed: boolean;
  docking_status: string;
  docking_score_kcal_mol?: number;
}

export interface CompiledDossier {
  hypothesis_id: string;
  formal_proposition: string;
  proof_obligations: ProofObligation[];
  unresolved_obligations_count: number;
  alternative_mechanisms: AlternativeMechanism[];
  uncertainty_vector: Array<{ dimension: string; status: string; value?: number }>;
  compilation_status: string;
  provenance_manifest: Record<string, any>;
}

export interface FalsificationDossier {
  hypothesis_id: string;
  hypothesis_title: string;
  competing_mechanisms: AlternativeMechanism[];
  survival_status: string;
  support_comparison_summary: string;
  recommended_discriminating_experiment: string;
  provenance_notes: string;
}

export interface ParetoPortfolioResponse {
  total_candidates_evaluated: number;
  feasible_frontier_count: number;
  feasible_frontier: Candidate[];
  dominated_candidates: Candidate[];
  incomplete_evidence: Candidate[];
  fatal_gate_failures: Candidate[];
}

export interface ExperimentRecommendationResponse {
  hypothesis_id: string;
  voi_status: string;
  recommended_experiment: {
    assay_name: string;
    biological_model: string;
    target_proof_obligation: string;
    discriminates_competing_mechanism: string;
    estimated_cost_usd?: number;
    estimated_duration_days?: number;
    expected_uncertainty_reduction?: number;
    advance_threshold: string;
    terminate_threshold: string;
    voi_score?: number;
  };
  all_evaluated_options: any[];
}

export const fetchPrograms = async (): Promise<Program[]> => {
  const res = await apiClient.get<Program[]>('/programs');
  return res.data;
};

export const fetchHypotheses = async (): Promise<Hypothesis[]> => {
  const res = await apiClient.get<Hypothesis[]>('/hypotheses');
  return res.data;
};

export const fetchCandidates = async (): Promise<Candidate[]> => {
  const res = await apiClient.get<Candidate[]>('/candidates');
  return res.data;
};

export const compileHypothesis = async (hypothesisId: string): Promise<CompiledDossier> => {
  const res = await apiClient.post<CompiledDossier>(`/hypotheses/${hypothesisId}/compile`);
  return res.data;
};

export const falsifyHypothesis = async (hypothesisId: string): Promise<FalsificationDossier> => {
  const res = await apiClient.post<FalsificationDossier>(`/hypotheses/${hypothesisId}/falsify`);
  return res.data;
};

export const fetchParetoPortfolio = async (): Promise<ParetoPortfolioResponse> => {
  const res = await apiClient.get<ParetoPortfolioResponse>('/portfolio/pareto-ranking');
  return res.data;
};

export const fetchExperimentRecommendation = async (hypothesisId: string): Promise<ExperimentRecommendationResponse> => {
  const res = await apiClient.post<ExperimentRecommendationResponse>(`/experiments/recommend/${hypothesisId}`);
  return res.data;
};

export const recordDecision = async (hypothesisId: string, outcome: string, rationale: string): Promise<any> => {
  const res = await apiClient.post('/decisions', { hypothesis_id: hypothesisId, outcome, rationale });
  return res.data;
};

export const fetchDigitalTwinTimeline = async (programId: string): Promise<any[]> => {
  const res = await apiClient.get<any[]>(`/programs/${programId}/digital-twin`);
  return res.data;
};

export const queryCopilot = async (programId: string, query: string): Promise<any> => {
  const res = await apiClient.post('/copilot/query', { program_id: programId, query });
  return res.data;
};

export const fetchModelProviders = async (): Promise<any[]> => {
  const res = await apiClient.get<any[]>('/models');
  return res.data;
};

export const fetchIntegrations = async (): Promise<any[]> => {
  const res = await apiClient.get<any[]>('/integrations');
  return res.data;
};
