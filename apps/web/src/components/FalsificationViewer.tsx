'use client';

import { useState } from 'react';
import { Crosshair, ShieldAlert, ArrowRight } from 'lucide-react';
import { falsifyHypothesis, Hypothesis } from '@/lib/api-client';

interface Props {
  hypothesis: Hypothesis;
}

export default function FalsificationViewer({ hypothesis }: Props) {
  const [falsificationData, setFalsificationData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleRunFalsification = async () => {
    setLoading(true);
    try {
      const data = await falsifyHypothesis(hypothesis.id);
      setFalsificationData(data);
    } catch (err) {
      console.error("Falsification error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Crosshair className="w-5 h-5 text-amber-400" />
          <h3 className="text-base font-bold text-white">Adversarial Falsification Engine</h3>
        </div>

        <button
          onClick={handleRunFalsification}
          disabled={loading}
          className="bg-amber-600 hover:bg-amber-500 text-white font-semibold text-xs px-4 py-2 rounded-lg flex items-center space-x-2 transition shadow-lg shadow-amber-500/20"
        >
          <span>{loading ? 'Testing Competing Mechanisms...' : 'Execute Adversarial Falsification'}</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {falsificationData ? (
        <div className="space-y-4 font-mono text-xs">
          {/* Summary Banner */}
          <div className="bg-slate-950 border border-slate-800 p-4 rounded-lg flex items-center justify-between">
            <div>
              <div className="text-[10px] text-slate-500">SURVIVAL STATUS</div>
              <div className={`text-base font-bold ${
                falsificationData.survival_status === 'SURVIVED_FALSIFICATION' ? 'text-emerald-400' : 'text-amber-400'
              }`}>
                {falsificationData.survival_status}
              </div>
            </div>
            <div className="text-right">
              <div className="text-[10px] text-slate-500">MECHANISTIC MARGIN</div>
              <div className="text-cyan-400 font-bold text-base">+{falsificationData.mechanistic_margin}</div>
            </div>
          </div>

          {/* Competing Mechanisms Table */}
          <div className="space-y-2">
            <div className="text-slate-400 font-bold uppercase text-[10px]">Evaluated Competing Mechanisms</div>
            {falsificationData.falsification_dossier.map((alt: any) => (
              <div key={alt.mechanism_name} className="p-3 bg-slate-950 border border-slate-800 rounded space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-white font-bold">{alt.mechanism_name}</span>
                  <span className="text-amber-400 font-semibold text-[10px]">
                    Competing Support: {alt.competing_support_score}
                  </span>
                </div>
                <p className="text-slate-400 text-[11px]">{alt.description}</p>
                <div className="text-[10px] text-cyan-300 pt-1 border-t border-slate-800/80">
                  <span className="text-slate-500">DISCRIMINATING ASSAY: </span>
                  {alt.discriminating_experiment}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-slate-500 text-xs italic text-center py-6">
          Click &quot;Execute Adversarial Falsification&quot; to test hypothesis against competing off-target and bypass signaling mechanisms.
        </div>
      )}
    </div>
  );
}
