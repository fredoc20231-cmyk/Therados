'use client';

import { useState, useEffect } from 'react';
import { ShieldCheck } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

export default function AuditLogViewer() {
  const [logs, setLogs] = useState<any[]>([]);

  useEffect(() => {
    async function loadLogs() {
      try {
        const res = await apiClient.get('/audit');
        setLogs(res.data);
      } catch (err) {
        console.error("Audit fetch error:", err);
      }
    }
    loadLogs();
  }, []);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-emerald-400" />
          <h3 className="text-base font-bold text-white">Audit Trail & Lineage Events</h3>
        </div>
      </div>

      <div className="space-y-2 font-mono text-xs">
        {logs.length > 0 ? (
          logs.map((log) => (
            <div key={log.id} className="p-2.5 bg-slate-950 border border-slate-800 rounded flex items-center justify-between">
              <div>
                <span className="text-cyan-400 font-bold">{log.action}</span>
                <span className="text-slate-400 text-[10px] ml-2">[{log.entity_type}: {log.entity_id}]</span>
              </div>
              <span className="text-slate-500 text-[10px]">{new Date(log.timestamp).toLocaleString()}</span>
            </div>
          ))
        ) : (
          <div className="p-4 bg-slate-950 border border-slate-800 rounded text-slate-400 text-[11px] text-center">
            All evidence ingestion, hypothesis compilations, decisions, and model runs are automatically recorded with SHA-256 provenance checksums.
          </div>
        )}
      </div>
    </div>
  );
}
