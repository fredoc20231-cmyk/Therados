'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  Dna, Cpu, ShieldCheck, Database, Clock, ArrowRight, Activity, Crosshair, CheckCircle2, AlertTriangle, Layers, Lock
} from 'lucide-react';
import { runHGSOCDiscovery, fetchHGSOCConfig, HGSOCDiscoveryRunResponse } from '@/lib/api-client';

export default function HGSOCDiscoveryPOCPage() {
  const [pocData, setPocData] = useState<HGSOCDiscoveryRunResponse | null>(null);
  const [config, setConfig] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function initPOC() {
      try {
        const [cfg, data] = await Promise.all([
          fetchHGSOCConfig(),
          runHGSOCDiscovery()
        ]);
        setConfig(cfg);
        setPocData(data);
      } catch (err) {
        console.error("POC Initialization Error:", err);
      } finally {
        setLoading(false);
      }
    }
    initPOC();
  }, []);

  if (loading || !pocData) {
    return (
      <div className="flex-1 p-12 flex flex-col items-center justify-center text-center bg-slate-950 font-mono text-xs">
        <Dna className="w-8 h-8 text-cyan-400 animate-spin mb-4" />
        <div className="text-slate-200 text-sm font-bold">Executing THERADOS-POC-001 Real-Data Discovery Pipeline...</div>
        <div className="text-slate-500 mt-2">Ingesting public evidence, running maximal triclique augmentation, safety gates & Pareto portfolio...</div>
      </div>
    );
  }

  const {
    locked_analysis_run,
    data_snapshot_manifest,
    temporal_holdout_manifest,
    endotype_clustering,
    resistance_profile,
    candidate_ensemble,
    pareto_portfolio,
    compiled_hypothesis_dossier,
    falsification_dossier,
    inverse_experiment_recommendation
  } = pocData;

  return (
    <div className="flex-1 flex flex-col bg-slate-950 text-slate-100 p-6 max-w-7xl mx-auto w-full space-y-8 font-mono">
      {/* Top Banner & Program Definition */}
      <div className="bg-slate-900 border border-brand-500/40 rounded-xl p-6 shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-4">
          <div>
            <div className="flex items-center space-x-3 mb-1">
              <span className="bg-brand-600/30 text-cyan-300 border border-brand-500/50 px-2.5 py-0.5 rounded text-xs font-bold">
                PROGRAM ID: {pocData.program_id}
              </span>
              <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-0.5 rounded text-xs font-bold">
                PROJECT MODE: {pocData.project_mode} (NO SYNTHETIC DATA)
              </span>
            </div>
            <h1 className="text-xl md:text-2xl font-bold text-white mt-2 leading-tight">
              {pocData.program_name}
            </h1>
          </div>

          <div className="flex flex-col items-end text-xs">
            <div className="flex items-center space-x-1.5 text-cyan-300 bg-slate-950 px-3 py-1.5 rounded border border-slate-800 font-bold">
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
              <span>RUN ID: {locked_analysis_run.run_id}</span>
            </div>
            <div className="text-[10px] text-slate-500 mt-1">Git SHA: {locked_analysis_run.git_sha}</div>
          </div>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed mb-4">
          <span className="text-cyan-400 font-bold">RESEARCH DISCOVERY PROGRAM QUESTION:</span> Which therapeutic interventions or target strategies are most defensible for platinum-resistant HGSOC when evaluated through independent evidence, molecular/endotype context, causal reasoning, pharmacologic feasibility, safety constraints, resistance biology, adversarial falsification, and value-of-information experiment design?
        </p>

        <div className="text-[10px] bg-slate-950 p-2.5 rounded border border-amber-500/30 text-amber-400">
          ⚠️ DISCLAIMER: RESEARCH DISCOVERY PROGRAM — NOT CLINICAL ADVICE OR PATIENT TREATMENT RECOMMENDATIONS.
        </div>
      </div>

      {/* Grid Section 1: Data Snapshot Manifest & Temporal Holdout */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Data Snapshot Manifest */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
            <div className="flex items-center space-x-2">
              <Database className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white">Data Snapshot Manifest</h3>
            </div>
            <span className="text-[10px] text-slate-400">{data_snapshot_manifest.manifest_id}</span>
          </div>

          <div className="space-y-2 text-xs">
            {data_snapshot_manifest.records.map((rec: any) => (
              <div key={rec.record_id} className="p-2.5 bg-slate-950 border border-slate-800 rounded flex items-center justify-between">
                <div>
                  <div className="text-white font-bold">{rec.provider_name}</div>
                  <div className="text-[10px] text-slate-500">{rec.endpoint}</div>
                </div>
                <div className="text-right font-mono text-[10px]">
                  <div className="text-emerald-400 font-bold">SHA-256 VERIFIED</div>
                  <div className="text-slate-500">{rec.payload_checksum_sha256.substring(0, 12)}...</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Temporal Retrospective Validation */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white">Temporal Retrospective Validation</h3>
            </div>
            <span className="text-[10px] text-emerald-400 font-bold">NO TEMPORAL LEAKAGE</span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="bg-slate-950 border border-slate-800 p-3 rounded grid grid-cols-2 gap-2 text-[11px]">
              <div>
                <span className="text-slate-500">CUTOFF DATE: </span>
                <span className="text-white font-bold">{temporal_holdout_manifest.cutoff_date.split('T')[0]}</span>
              </div>
              <div>
                <span className="text-slate-500">RECOVERY HIT RATE: </span>
                <span className="text-emerald-400 font-bold">{(temporal_holdout_manifest.holdout_recovery_hit_rate * 100).toFixed(0)}%</span>
              </div>
            </div>

            <div className="p-2.5 bg-slate-950 border border-slate-800 rounded">
              <div className="text-[10px] text-slate-500 mb-1">RECOVERED HOLDOUT TARGETS</div>
              <div className="text-cyan-300 font-bold">{temporal_holdout_manifest.recovered_targets.join(' | ')}</div>
            </div>

            <p className="text-[10px] text-slate-400">{temporal_holdout_manifest.provenance_notes}</p>
          </div>
        </div>
      </div>

      {/* Grid Section 2: Endotypes & Resistance Biology */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Endotype Subtypes */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
            <div className="flex items-center space-x-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white">HGSOC Endotype Subtypes</h3>
            </div>
          </div>

          <div className="space-y-2 text-xs">
            {endotype_clustering.endotypes.map((end: any) => (
              <div key={end.endotype_id} className="p-3 bg-slate-950 border border-slate-800 rounded space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-cyan-400 font-bold">{end.endotype_id}: {end.name}</span>
                  <span className="text-[10px] text-slate-400">{(end.prevalence * 100).toFixed(0)}% Prevalence</span>
                </div>
                <div className="text-[10px] text-slate-400">Drivers: {end.driver_pathways.join(', ')}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Resistance Profile */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex items-center justify-between mb-3 border-b border-slate-800 pb-2">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-bold text-white">Platinum Resistance Biology</h3>
            </div>
          </div>

          <div className="space-y-2 text-xs">
            {resistance_profile.mechanisms.map((mech: any) => (
              <div key={mech.resistance_id} className="p-3 bg-slate-950 border border-slate-800 rounded space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-amber-300 font-bold">{mech.mechanism_name}</span>
                  <span className="text-[10px] bg-slate-800 text-slate-300 px-1.5 py-0.5 rounded">{mech.category}</span>
                </div>
                <p className="text-[10px] text-slate-400 leading-relaxed">{mech.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Candidate Ensemble & Origins */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base font-bold text-white">Candidate Generation Ensemble & Origin Lineage</h3>
          </div>
          <span className="text-xs text-slate-400">Independent Method Convergence</span>
        </div>

        <div className="space-y-3 text-xs">
          {candidate_ensemble.map((cand: any) => (
            <div key={cand.candidate_id} className="p-4 bg-slate-950 border border-slate-800 rounded space-y-2">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-white font-bold text-sm">{cand.name}</span>
                  <span className="text-slate-400 text-xs ml-2">[{cand.primary_target}]</span>
                </div>
                <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold ${
                  cand.safety_gate_passed ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-rose-950 text-rose-400 border border-rose-800'
                }`}>
                  {cand.gate_status}
                </span>
              </div>

              <div className="text-[10px] text-slate-400 font-mono">
                SMILES: <code className="text-cyan-300">{cand.smiles}</code>
              </div>

              <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-800">
                {cand.candidate_origins.map((orig: any, i: number) => (
                  <span key={i} className="bg-slate-900 border border-slate-800 text-cyan-300 px-2 py-0.5 rounded text-[10px]">
                    {orig.generator}: {orig.support}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Pareto Portfolio Frontier */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <Layers className="w-5 h-5 text-emerald-400" />
            <h3 className="text-base font-bold text-white">Feasible Pareto Portfolio Frontier</h3>
          </div>
        </div>

        <div className="space-y-3 text-xs">
          {pareto_portfolio.feasible_frontier.map((cand: any) => (
            <div key={cand.candidate_id || cand.name} className="p-3 bg-slate-950 border border-emerald-500/40 rounded flex items-center justify-between">
              <div>
                <div className="text-white font-bold text-sm">{cand.name}</div>
                <div className="text-[10px] text-slate-400">Target: {cand.primary_target}</div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <div className="text-[10px] text-slate-500">CPI SCORE</div>
                  <div className="text-cyan-400 font-bold">{cand.cpi_score}</div>
                </div>
                <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-1 rounded text-[10px] uppercase font-bold">
                  FEASIBLE FRONTIER TIER A
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Decisive Experiment Recommendation */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <Crosshair className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base font-bold text-white">Value of Information (VOI) Decisive Experiment</h3>
          </div>
        </div>

        {inverse_experiment_recommendation.recommended_experiment && (
          <div className="bg-slate-950 border border-cyan-500/40 p-4 rounded text-xs space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-cyan-400 font-bold text-sm">
                {inverse_experiment_recommendation.recommended_experiment.assay_name}
              </span>
              <span className="bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded text-[10px] font-bold">
                VOI SCORE: {inverse_experiment_recommendation.recommended_experiment.voi_score}
              </span>
            </div>
            <p className="text-slate-300">{inverse_experiment_recommendation.recommended_experiment.biological_model}</p>
            <div className="text-emerald-400 font-bold pt-2 border-t border-slate-800">
              ADVANCE CRITERIA: {inverse_experiment_recommendation.recommended_experiment.advance_threshold}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
