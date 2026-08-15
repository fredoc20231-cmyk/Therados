'use client';

import { useState } from 'react';
import { ShieldCheck, AlertTriangle, ArrowRight } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

export default function PharmacologyViewer() {
  const [smiles, setSmiles] = useState('CC1=C(C=C(C=C1)C2=NC(=NC(=C2)N)N3CCN(CC3)C(=O)C4CC4)NC(=O)C5=CC=C(C=C5)F');
  const [props, setProps] = useState<any>(null);
  const [safetyRes, setSafetyRes] = useState<any>(null);

  const handleEvaluate = async () => {
    try {
      const [pRes, sRes] = await Promise.all([
        apiClient.post('/pharmacology/evaluate-smiles', { smiles }),
        apiClient.post('/pharmacology/safety-gate')
      ]);
      setProps(pRes.data);
      setSafetyRes(sRes.data);
    } catch (err) {
      console.error("Pharmacology error:", err);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Pharmacology & Hard Safety Gates Engine</h3>
        </div>
      </div>

      <div className="space-y-4 font-mono text-xs">
        <div>
          <label className="block text-slate-400 mb-1">SMILES Structure Query</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={smiles}
              onChange={(e) => setSmiles(e.target.value)}
              className="flex-1 bg-slate-950 border border-slate-800 rounded px-3 py-2 text-slate-200 text-xs focus:outline-none focus:border-brand-500 font-mono"
            />
            <button
              onClick={handleEvaluate}
              className="bg-brand-600 hover:bg-brand-500 text-white px-4 py-2 rounded font-semibold text-xs transition"
            >
              Evaluate Molecular Structure
            </button>
          </div>
        </div>

        {props && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-950 p-4 border border-slate-800 rounded-lg">
            <div>
              <div className="text-[10px] text-slate-500">MOL WEIGHT</div>
              <div className="text-white font-bold">{props.molecular_weight} g/mol</div>
            </div>
            <div>
              <div className="text-[10px] text-slate-500">cLogP</div>
              <div className="text-cyan-400 font-bold">{props.clogp}</div>
            </div>
            <div>
              <div className="text-[10px] text-slate-500">H-DONORS / ACCEPTORS</div>
              <div className="text-slate-300">{props.hbd} / {props.hba}</div>
            </div>
            <div>
              <div className="text-[10px] text-slate-500">RULE OF 5 VIOLATIONS</div>
              <div className="text-emerald-400 font-bold">{props.rule_of_five_violations}</div>
            </div>
          </div>
        )}

        {safetyRes && (
          <div className={`p-4 border rounded-lg flex items-center justify-between ${
            safetyRes.passed ? 'bg-emerald-950/40 border-emerald-800 text-emerald-300' : 'bg-rose-950/40 border-rose-800 text-rose-300'
          }`}>
            <div>
              <div className="text-[10px] opacity-75 font-bold uppercase">HARD FEASIBILITY GATE STATUS</div>
              <div className="text-sm font-bold">{safetyRes.gate_status}</div>
            </div>
            <div className="text-xs font-semibold">
              {safetyRes.passed ? 'FEASIBLE & EXPOSURE SAFE' : 'REJECTED BY FATAL GATE'}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
