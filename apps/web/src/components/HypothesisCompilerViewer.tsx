'use client';

import { useState } from 'react';
import { Cpu, CheckCircle2, AlertCircle, FileText, ArrowRight } from 'lucide-react';
import { compileHypothesis, Hypothesis } from '@/lib/api-client';

interface Props {
  hypothesis: Hypothesis;
}

export default function HypothesisCompilerViewer({ hypothesis }: Props) {
  const [dossier, setDossier] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleCompile = async () => {
    setLoading(true);
    try {
      const compiled = await compileHypothesis(hypothesis.id);
      setDossier(compiled);
    } catch (err) {
      console.error("Compilation error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center space-x-2">
            <Cpu className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base font-bold text-white">Therapeutic Hypothesis Compiler</h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">{hypothesis.title}</p>
        </div>

        <button
          onClick={handleCompile}
          disabled={loading}
          className="bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs px-4 py-2 rounded-lg flex items-center space-x-2 transition shadow-lg shadow-brand-500/20"
        >
          <span>{loading ? 'Compiling Proof Obligations...' : 'Compile Hypothesis Dossier'}</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Formal Contextual Hypothesis Parameters */}
      <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 font-mono text-xs mb-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div>
          <div className="text-[10px] text-slate-500">INTERVENTION (d)</div>
          <div className="text-cyan-400 font-bold">{hypothesis.intervention_name}</div>
        </div>
        <div>
          <div className="text-[10px] text-slate-500">TARGET (P) & ACTION (A)</div>
          <div className="text-white font-bold">{hypothesis.intended_target} ({hypothesis.intended_action})</div>
        </div>
        <div>
          <div className="text-[10px] text-slate-500">CONTEXT (C)</div>
          <div className="text-slate-300">{hypothesis.cellular_context}</div>
        </div>
        <div>
          <div className="text-[10px] text-slate-500">ENDOTYPE (E)</div>
          <div className="text-emerald-400 font-bold">{hypothesis.disease_endotype}</div>
        </div>
      </div>

      {/* Compiled Dossier & Proof Obligations Output */}
      {dossier && (
        <div className="space-y-4">
          <div className="bg-slate-950 border border-brand-500/30 rounded-lg p-4">
            <div className="text-xs text-slate-400 font-mono mb-1">FORMAL PROPOSITION</div>
            <p className="text-xs text-cyan-200 font-mono leading-relaxed">{dossier.formal_proposition}</p>
          </div>

          <div>
            <h4 className="text-xs font-mono font-bold text-slate-300 uppercase mb-2">Mandatory Proof Obligations</h4>
            <div className="space-y-2">
              {dossier.proof_obligations.map((po: any) => (
                <div key={po.id} className="p-3 bg-slate-950 border border-slate-800 rounded flex items-center justify-between text-xs font-mono">
                  <div className="flex items-center space-x-3">
                    {po.state === 'supported' ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    ) : (
                      <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
                    )}
                    <div>
                      <div className="text-slate-200 font-bold">{po.proposition}</div>
                      <div className="text-[10px] text-slate-400 mt-0.5">Threshold: {po.threshold_value} | Required: {po.required_evidence_type}</div>
                    </div>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold ${
                    po.state === 'supported' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-amber-950 text-amber-400 border border-amber-800'
                  }`}>
                    {po.state}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
