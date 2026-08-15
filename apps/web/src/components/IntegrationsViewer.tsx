'use client';

import { useState, useEffect } from 'react';
import { Database } from 'lucide-react';
import { fetchIntegrations } from '@/lib/api-client';

export default function IntegrationsViewer() {
  const [integrations, setIntegrations] = useState<any[]>([]);

  useEffect(() => {
    async function loadIntegrations() {
      try {
        const data = await fetchIntegrations();
        setIntegrations(data);
      } catch (err) {
        console.error("Integrations error:", err);
      }
    }
    loadIntegrations();
  }, []);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Database className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Public Data & Provider Integrations</h3>
        </div>
      </div>

      <div className="space-y-3 font-mono text-xs">
        {integrations.map((item) => (
          <div key={item.name} className="p-3 bg-slate-950 border border-slate-800 rounded flex items-center justify-between">
            <div>
              <div className="text-white font-bold">{item.name}</div>
              <div className="text-[10px] text-slate-400 mt-0.5">{item.type}</div>
            </div>
            <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold ${
              item.status === 'HEALTHY' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' : 'bg-amber-950 text-amber-400 border border-amber-800'
            }`}>
              {item.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
