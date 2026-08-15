'use client';

import { useState, useEffect } from 'react';
import { Clock, ShieldCheck } from 'lucide-react';
import { fetchDigitalTwinTimeline } from '@/lib/api-client';

interface Props {
  programId: string;
}

export default function DigitalTwinTimeline({ programId }: Props) {
  const [timeline, setTimeline] = useState<any[]>([]);

  useEffect(() => {
    async function loadTimeline() {
      try {
        const data = await fetchDigitalTwinTimeline(programId);
        setTimeline(data);
      } catch (err) {
        console.error("Timeline error:", err);
      }
    }
    loadTimeline();
  }, [programId]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Clock className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Therapeutic Program Digital Twin Timeline</h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">Append-Only Immutable Audit Log</span>
      </div>

      <div className="space-y-3 font-mono text-xs">
        {timeline.map((snap) => (
          <div key={snap.id} className="p-3 bg-slate-950 border border-slate-800 rounded flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-2 mb-1">
                <span className="bg-brand-600/30 text-cyan-300 border border-brand-500/50 px-2 py-0.5 rounded text-[10px] font-bold">
                  SNAPSHOT #{snap.snapshot_index}
                </span>
                <span className="text-slate-400 text-[11px]">{new Date(snap.created_at).toLocaleString()}</span>
              </div>
              <div className="text-white font-bold">{snap.trigger_event}</div>
            </div>
            <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-1 rounded text-[10px] font-bold">
              STATE PRESERVED
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
