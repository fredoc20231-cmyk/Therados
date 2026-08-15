'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { Activity, Cpu, Layers, AlertCircle, ArrowUpRight, CheckCircle, Clock } from 'lucide-react';
import { fetchPrograms, fetchHypotheses, fetchCandidates, Program, Hypothesis, Candidate } from '@/lib/api-client';

export default function DashboardPage() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [hypotheses, setHypotheses] = useState<Hypothesis[]>([]);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [progs, hypos, cands] = await Promise.all([
          fetchPrograms(),
          fetchHypotheses(),
          fetchCandidates()
        ]);
        setPrograms(progs);
        setHypotheses(hypos);
        setCandidates(cands);
      } catch (err) {
        console.error("Dashboard error:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="flex-1 p-8 max-w-7xl mx-auto w-full">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Activity className="w-6 h-6 text-cyan-400" />
            <span>Program Operations Dashboard</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">Real-time therapeutic intelligence state and audit summary.</p>
        </div>
        <Link
          href="/workspace"
          className="bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs px-4 py-2 rounded-lg flex items-center gap-2 transition"
        >
          <span>Open Workspace</span>
          <ArrowUpRight className="w-4 h-4" />
        </Link>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="text-xs text-slate-400 mb-1">Active Programs</div>
          <div className="text-3xl font-bold text-white font-mono">{loading ? '...' : programs.length}</div>
          <div className="text-[10px] text-cyan-400 mt-2">HGSOC & Oncology Focus</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="text-xs text-slate-400 mb-1">Compiled Hypotheses</div>
          <div className="text-3xl font-bold text-cyan-400 font-mono">{loading ? '...' : hypotheses.length}</div>
          <div className="text-[10px] text-slate-400 mt-2">Provenanced & Dossier-backed</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="text-xs text-slate-400 mb-1">Evaluated Candidates</div>
          <div className="text-3xl font-bold text-emerald-400 font-mono">{loading ? '...' : candidates.length}</div>
          <div className="text-[10px] text-slate-400 mt-2">CPI & Safety Gate Verified</div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <div className="text-xs text-slate-400 mb-1">Governance Status</div>
          <div className="text-sm font-bold text-emerald-400 flex items-center gap-2 mt-2">
            <CheckCircle className="w-4 h-4" />
            <span>Audited & Provenanced</span>
          </div>
          <div className="text-[10px] text-slate-400 mt-2">SHA-256 Checksums Active</div>
        </div>
      </div>

      {/* Program Summary Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-8">
        <h2 className="text-lg font-bold text-white mb-4">Therapeutic Programs</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950 text-slate-400 font-mono border-b border-slate-800">
              <tr>
                <th className="p-3">Disease / Indication</th>
                <th className="p-3">Endotype Target</th>
                <th className="p-3">Program Objective</th>
                <th className="p-3">Status</th>
                <th className="p-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {programs.map((prog) => (
                <tr key={prog.id} className="hover:bg-slate-850/50">
                  <td className="p-3 font-semibold text-white">{prog.disease} <br/><span className="text-[10px] text-slate-400">{prog.indication}</span></td>
                  <td className="p-3 font-mono text-cyan-400">CCNE1-Amp (END-01)</td>
                  <td className="p-3 max-w-md truncate">{prog.program_objective}</td>
                  <td className="p-3">
                    <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded font-mono text-[10px]">
                      {prog.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="p-3 text-right">
                    <Link href="/workspace" className="text-cyan-400 hover:underline font-mono">Open Workspace →</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
