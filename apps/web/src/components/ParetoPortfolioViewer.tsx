'use client';

import { useState, useEffect } from 'react';
import { Layers, CheckCircle } from 'lucide-react';
import { fetchParetoPortfolio } from '@/lib/api-client';

export default function ParetoPortfolioViewer() {
  const [portfolio, setPortfolio] = useState<any>(null);

  useEffect(() => {
    async function loadPortfolio() {
      try {
        const data = await fetchParetoPortfolio();
        setPortfolio(data);
      } catch (err) {
        console.error("Portfolio error:", err);
      }
    }
    loadPortfolio();
  }, []);

  if (!portfolio) {
    return <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 text-xs font-mono">Loading Pareto Frontier...</div>;
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Layers className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Multi-Objective Pareto Portfolio Engine</h3>
        </div>
        <span className="text-xs bg-cyan-950 text-cyan-300 border border-cyan-800 px-2.5 py-0.5 rounded font-mono">
          Frontier Size: {portfolio.pareto_frontier_count} Candidates
        </span>
      </div>

      <div className="space-y-4 font-mono text-xs">
        <div>
          <h4 className="text-xs font-bold text-emerald-400 uppercase mb-2">Tier A — Pareto Non-Dominated Frontier</h4>
          <div className="space-y-2">
            {portfolio.pareto_frontier.map((cand: any) => (
              <div key={cand.id} className="p-3 bg-slate-950 border border-emerald-500/40 rounded flex items-center justify-between">
                <div>
                  <div className="text-white font-bold text-sm">{cand.name}</div>
                  <div className="text-[10px] text-slate-400">Primary Target: {cand.primary_target}</div>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <div className="text-[10px] text-slate-500">CPI SCORE</div>
                    <div className="text-cyan-400 font-bold">{cand.cpi_score}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-[10px] text-slate-500">NOVELTY</div>
                    <div className="text-emerald-400 font-bold">{cand.novelty_score}</div>
                  </div>
                  <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-1 rounded text-[10px] uppercase font-bold">
                    {cand.overall_status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {portfolio.dominated_candidates.length > 0 && (
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase mb-2">Tier B / Dominated Candidates</h4>
            <div className="space-y-2">
              {portfolio.dominated_candidates.map((cand: any) => (
                <div key={cand.id} className="p-3 bg-slate-950/60 border border-slate-800 rounded flex items-center justify-between opacity-75">
                  <div>
                    <div className="text-slate-300 font-semibold">{cand.name}</div>
                    <div className="text-[10px] text-slate-500">Primary Target: {cand.primary_target}</div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <div className="text-[10px] text-slate-500">CPI SCORE</div>
                      <div className="text-slate-400 font-bold">{cand.cpi_score}</div>
                    </div>
                    <span className="bg-slate-800 text-slate-400 border border-slate-700 px-2 py-1 rounded text-[10px] uppercase font-bold">
                      {cand.pareto_rank}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
