'use client';

import { useState, useEffect } from 'react';
import { Cpu, CheckCircle2, AlertCircle } from 'lucide-react';
import { fetchModelProviders } from '@/lib/api-client';

export default function ModelRegistryViewer() {
  const [providers, setProviders] = useState<any[]>([]);

  useEffect(() => {
    async function loadModels() {
      try {
        const data = await fetchModelProviders();
        setProviders(data);
      } catch (err) {
        console.error("Model registry error:", err);
      }
    }
    loadModels();
  }, []);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Model Fabric Provider Registry</h3>
        </div>
      </div>

      <div className="space-y-3 font-mono text-xs">
        {providers.map((p) => (
          <div key={p.provider_name} className="p-3 bg-slate-950 border border-slate-800 rounded flex items-center justify-between">
            <div>
              <div className="text-white font-bold">{p.provider_name}</div>
              <div className="text-[10px] text-slate-400 mt-0.5">{p.status_reason}</div>
            </div>
            <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold ${
              p.is_configured ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-slate-800 text-slate-400 border border-slate-700'
            }`}>
              {p.is_configured ? 'ACTIVE' : 'NOT CONFIGURED'}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
