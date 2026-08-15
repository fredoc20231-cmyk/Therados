'use client';

import { useState, useEffect } from 'react';
import { Layers, CheckCircle2 } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

export default function EndotypeViewer() {
  const [endotypeData, setEndotypeData] = useState<any>(null);

  useEffect(() => {
    async function loadEndotypes() {
      try {
        const res = await apiClient.get('/endotypes');
        setEndotypeData(res.data);
      } catch (err) {
        console.error("Endotype fetch error:", err);
      }
    }
    loadEndotypes();
  }, []);

  if (!endotypeData) {
    return <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 text-xs">Loading endotype clustering...</div>;
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Layers className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Disease Endotype Clustering ({endotypeData.disease_area})</h3>
        </div>
        <span className="text-xs bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-0.5 rounded font-mono">
          QC STATUS: {endotypeData.endotype_qc_status}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {endotypeData.endotypes.map((endotype: any) => (
          <div key={endotype.endotype_id} className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono font-bold text-cyan-400">{endotype.endotype_id}</span>
                <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
                  {(endotype.prevalence * 100).toFixed(0)}% Prevalence
                </span>
              </div>
              <h4 className="text-sm font-bold text-white mb-2 leading-tight">{endotype.name}</h4>

              <div className="space-y-2 text-xs font-mono my-3">
                <div className="text-[10px] text-slate-400 uppercase font-semibold">Driver Pathways</div>
                <div className="flex flex-wrap gap-1">
                  {endotype.driver_pathways.map((path: string) => (
                    <span key={path} className="bg-slate-900 border border-slate-800 text-slate-300 px-2 py-0.5 rounded text-[10px]">
                      {path}
                    </span>
                  ))}
                </div>
              </div>

              <div className="space-y-1 text-xs font-mono">
                <div className="text-[10px] text-slate-400 uppercase font-semibold">Key Predictive Biomarkers</div>
                <div className="text-emerald-400 font-semibold">{endotype.key_biomarkers.join(' | ')}</div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono text-slate-400">
              <span>Cluster Stability</span>
              <span className="text-white font-bold">{(endotype.stability_score * 100).toFixed(0)}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
