'use client';

import { useState } from 'react';
import { Crosshair, ArrowRight, DollarSign, Clock } from 'lucide-react';
import { fetchExperimentRecommendation, Hypothesis } from '@/lib/api-client';

interface Props {
  hypothesis: Hypothesis;
}

export default function ExperimentDesignerViewer({ hypothesis }: Props) {
  const [recommendation, setRecommendation] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFetchVOI = async () => {
    setLoading(true);
    try {
      const data = await fetchExperimentRecommendation(hypothesis.id);
      setRecommendation(data);
    } catch (err) {
      console.error("VOI error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Crosshair className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Inverse Experiment Designer (VOI Engine)</h3>
        </div>

        <button
          onClick={handleFetchVOI}
          disabled={loading}
          className="bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs px-4 py-2 rounded-lg flex items-center space-x-2 transition shadow-lg shadow-brand-500/20"
        >
          <span>{loading ? 'Calculating VOI...' : 'Recommend Decisive Experiment'}</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {recommendation ? (
        <div className="space-y-4 font-mono text-xs">
          <div className="bg-slate-950 border border-cyan-500/40 p-4 rounded-lg">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] text-cyan-400 font-bold uppercase">TOP RECOMMENDED ASSAY (HIGHEST VOI)</span>
              <span className="bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded text-[10px] font-bold">
                VOI SCORE: {recommendation.recommended_experiment.voi_score}
              </span>
            </div>

            <h4 className="text-sm font-bold text-white mb-2">{recommendation.recommended_experiment.assay_name}</h4>
            <div className="text-slate-300 mb-3">{recommendation.recommended_experiment.biological_model}</div>

            <div className="grid grid-cols-2 gap-3 pt-3 border-t border-slate-800 text-[11px]">
              <div>
                <span className="text-slate-500">ESTIMATED COST: </span>
                <span className="text-emerald-400 font-bold">${recommendation.recommended_experiment.estimated_cost_usd}</span>
              </div>
              <div>
                <span className="text-slate-500">ESTIMATED TURNAROUND: </span>
                <span className="text-cyan-400 font-bold">{recommendation.recommended_experiment.estimated_duration_days} Days</span>
              </div>
            </div>

            <div className="mt-3 pt-3 border-t border-slate-800/80 space-y-1">
              <div><span className="text-emerald-400 font-bold">ADVANCE CRITERIA: </span>{recommendation.recommended_experiment.advance_threshold}</div>
              <div><span className="text-rose-400 font-bold">TERMINATE CRITERIA: </span>{recommendation.recommended_experiment.terminate_threshold}</div>
            </div>
          </div>
        </div>
      ) : (
        <div className="text-slate-500 text-xs italic text-center py-6">
          Click &quot;Recommend Decisive Experiment&quot; to calculate the Value-of-Information (VOI) for resolving open proof obligations.
        </div>
      )}
    </div>
  );
}
