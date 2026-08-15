'use client';

import { useState, useEffect } from 'react';
import { Cpu, Layers, GitBranch, Crosshair, ShieldCheck, Database, Clock, ArrowRight, Dna } from 'lucide-react';
import { fetchPrograms, fetchHypotheses, fetchCandidates, Program, Hypothesis, Candidate } from '@/lib/api-client';

import CausalGraphViewer from '@/components/CausalGraphViewer';
import EndotypeViewer from '@/components/EndotypeViewer';
import HypothesisCompilerViewer from '@/components/HypothesisCompilerViewer';
import FalsificationViewer from '@/components/FalsificationViewer';
import PharmacologyViewer from '@/components/PharmacologyViewer';
import ParetoPortfolioViewer from '@/components/ParetoPortfolioViewer';
import ExperimentDesignerViewer from '@/components/ExperimentDesignerViewer';
import DigitalTwinTimeline from '@/components/DigitalTwinTimeline';
import CopilotDrawer from '@/components/CopilotDrawer';
import ModelRegistryViewer from '@/components/ModelRegistryViewer';
import IntegrationsViewer from '@/components/IntegrationsViewer';
import AuditLogViewer from '@/components/AuditLogViewer';

export default function WorkspacePage() {
  const [activeTab, setActiveTab] = useState<'workspace' | 'graph' | 'endotypes' | 'portfolio' | 'pharmacology' | 'integrations' | 'audit'>('workspace');
  const [programs, setPrograms] = useState<Program[]>([]);
  const [selectedProgram, setSelectedProgram] = useState<Program | null>(null);
  const [hypotheses, setHypotheses] = useState<Hypothesis[]>([]);
  const [selectedHypothesis, setSelectedHypothesis] = useState<Hypothesis | null>(null);

  useEffect(() => {
    async function loadWorkspaceData() {
      try {
        const progs = await fetchPrograms();
        setPrograms(progs);
        if (progs.length > 0) {
          setSelectedProgram(progs[0]);
        }

        const hypos = await fetchHypotheses();
        setHypotheses(hypos);
        if (hypos.length > 0) {
          setSelectedHypothesis(hypos[0]);
        }
      } catch (err) {
        console.error("Workspace load error:", err);
      }
    }
    loadWorkspaceData();
  }, []);

  return (
    <div className="flex-1 flex flex-col bg-slate-950 text-slate-100">
      {/* Biological Pipeline Header Stepper */}
      <div className="bg-slate-900/90 border-b border-slate-800 px-6 py-3 flex items-center justify-between text-xs font-mono overflow-x-auto">
        <div className="flex items-center space-x-2 text-slate-300 whitespace-nowrap">
          <span className="text-cyan-400 font-bold">Disease</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Endotype</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Drivers</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Targets</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Interventions</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Mechanisms</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Exposure</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Safety</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Falsification</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-cyan-400 font-bold">Experiment</span>
          <ArrowRight className="w-3 h-3 text-slate-600" />
          <span className="text-emerald-400 font-bold">Decision</span>
        </div>

        {selectedProgram && (
          <div className="bg-slate-950 px-3 py-1 rounded border border-slate-800 text-cyan-300 font-semibold ml-4 whitespace-nowrap">
            {selectedProgram.disease} ({selectedProgram.indication})
          </div>
        )}
      </div>

      {/* Navigation Sub-Header */}
      <div className="bg-slate-900 border-b border-slate-800 px-6 py-2.5 flex items-center space-x-4 text-xs font-semibold">
        <button
          onClick={() => setActiveTab('workspace')}
          className={`px-3 py-1.5 rounded transition ${
            activeTab === 'workspace' ? 'bg-brand-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          Program Workspace
        </button>
        <button
          onClick={() => setActiveTab('graph')}
          className={`px-3 py-1.5 rounded transition ${
            activeTab === 'graph' ? 'bg-brand-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          Causal Graph
        </button>
        <button
          onClick={() => setActiveTab('endotypes')}
          className={`px-3 py-1.5 rounded transition ${
            activeTab === 'endotypes' ? 'bg-brand-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          Endotypes
        </button>
        <button
          onClick={() => setActiveTab('portfolio')}
          className={`px-3 py-1.5 rounded transition ${
            activeTab === 'portfolio' ? 'bg-brand-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          Pareto Portfolio
        </button>
        <button
          onClick={() => setActiveTab('pharmacology')}
          className={`px-3 py-1.5 rounded transition ${
            activeTab === 'pharmacology' ? 'bg-brand-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          Pharmacology & Safety
        </button>
        <button
          onClick={() => setActiveTab('integrations')}
          className={`px-3 py-1.5 rounded transition ${
            activeTab === 'integrations' ? 'bg-brand-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          Connectors & Models
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          className={`px-3 py-1.5 rounded transition ${
            activeTab === 'audit' ? 'bg-brand-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`}
        >
          Audit Log
        </button>
      </div>

      {/* Main Workspace Body */}
      <div className="flex-1 p-6 max-w-7xl mx-auto w-full space-y-6">
        {activeTab === 'workspace' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              {selectedHypothesis ? (
                <>
                  <HypothesisCompilerViewer hypothesis={selectedHypothesis} />
                  <FalsificationViewer hypothesis={selectedHypothesis} />
                  <ExperimentDesignerViewer hypothesis={selectedHypothesis} />
                </>
              ) : (
                <div className="p-8 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 text-xs">
                  Loading hypothesis dossier...
                </div>
              )}
            </div>

            <div className="space-y-6">
              {selectedProgram && <DigitalTwinTimeline programId={selectedProgram.id} />}
              {selectedProgram && <CopilotDrawer programId={selectedProgram.id} />}
            </div>
          </div>
        )}

        {activeTab === 'graph' && <CausalGraphViewer />}
        {activeTab === 'endotypes' && <EndotypeViewer />}
        {activeTab === 'portfolio' && <ParetoPortfolioViewer />}
        {activeTab === 'pharmacology' && <PharmacologyViewer />}
        {activeTab === 'integrations' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <IntegrationsViewer />
            <ModelRegistryViewer />
          </div>
        )}
        {activeTab === 'audit' && <AuditLogViewer />}
      </div>
    </div>
  );
}
