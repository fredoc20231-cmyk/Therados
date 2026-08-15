import Link from 'next/link';
import { ArrowRight, Shield, Dna, Cpu, GitBranch, Crosshair, CheckCircle2, AlertTriangle, FileText, Database } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="flex-1 flex flex-col bg-slate-950 text-slate-100">
      {/* Hero Section */}
      <section className="relative px-6 py-20 max-w-6xl mx-auto text-center flex flex-col items-center">
        <div className="inline-flex items-center space-x-2 bg-slate-900 border border-brand-500/30 text-cyan-400 px-3 py-1 rounded-full text-xs font-mono mb-6">
          <Shield className="w-3.5 h-3.5 text-cyan-400" />
          <span>Falsifiable, Endotype-Specific Therapeutic Intelligence</span>
        </div>

        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white mb-6 max-w-4xl leading-tight">
          Convert Heterogeneous Biomedical Evidence into <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-brand-500">Experiment-Ready Hypotheses</span>
        </h1>

        <p className="text-lg md:text-xl text-slate-400 max-w-3xl mb-10 leading-relaxed">
          TheraDOS is an operating system for therapeutic reasoning and experimental decision-making.
          It owns provenance, evidence lineage, proof obligations, hard safety gates, adversarial falsification, and inverse experiment selection.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4">
          <Link
            href="/workspace"
            className="bg-gradient-to-r from-brand-600 to-cyan-600 hover:from-brand-500 hover:to-cyan-500 text-white font-semibold px-6 py-3 rounded-lg shadow-lg shadow-brand-500/25 flex items-center space-x-2 transition"
          >
            <span>Launch Therapeutic Program Workspace</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/dashboard"
            className="bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 font-medium px-6 py-3 rounded-lg transition"
          >
            <span>View Active Dashboard</span>
          </Link>
        </div>
      </section>

      {/* Core Identity & Formula Box */}
      <section className="border-y border-slate-800/80 bg-slate-900/50 py-12 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-white mb-2">The Fundamental Computational Object</h2>
            <p className="text-sm text-slate-400">TheraDOS does not predict simple drug-target edges. It executes contextual hypotheses.</p>
          </div>

          <div className="bg-slate-950 border border-brand-500/40 rounded-xl p-6 font-mono text-center shadow-xl">
            <div className="text-xl md:text-2xl text-cyan-300 font-bold mb-4 tracking-wider">
              H = (d, P, A, C, E, G, B, Δ, Θ, Σ)
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 text-xs text-slate-400 text-left pt-4 border-t border-slate-800">
              <div><span className="text-cyan-400 font-bold">d</span>: Intervention</div>
              <div><span className="text-cyan-400 font-bold">P</span>: Target Set</div>
              <div><span className="text-cyan-400 font-bold">A</span>: Intended Action</div>
              <div><span className="text-cyan-400 font-bold">C</span>: Cellular Context</div>
              <div><span className="text-cyan-400 font-bold">E</span>: Disease Endotype</div>
              <div><span className="text-cyan-400 font-bold">G</span>: Genomic Background</div>
              <div><span className="text-cyan-400 font-bold">B</span>: Biomarkers</div>
              <div><span className="text-cyan-400 font-bold">Δ</span>: Dose Exposure</div>
              <div><span className="text-cyan-400 font-bold">Θ</span>: Schedule/Seq</div>
              <div><span className="text-cyan-400 font-bold">Σ</span>: Safety/Constraints</div>
            </div>
          </div>
        </div>
      </section>

      {/* Non-Negotiable Scientific Principles */}
      <section className="px-6 py-16 max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-white">Scientific Principles & Governance</h2>
          <p className="text-slate-400 text-sm mt-2">Built-in safeguards preventing hallucination and uncalibrated claims.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
            <CheckCircle2 className="w-8 h-8 text-emerald-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Scientific Truth</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              NEVER fabricates binding affinities, docking scores, or trial results. Uncalculated metrics report <code className="text-amber-400">Not evaluated</code> or <code className="text-amber-400">Provider not configured</code>.
            </p>
          </div>

          <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
            <AlertTriangle className="w-8 h-8 text-amber-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Hard Feasibility Gates</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Exposure infeasibility or high cardiac/genotoxicity liabilities act as non-negotiable hard fatal gates. Excellent graph scores cannot average them away.
            </p>
          </div>

          <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl">
            <Crosshair className="w-8 h-8 text-cyan-400 mb-4" />
            <h3 className="text-lg font-bold text-white mb-2">Adversarial Falsification</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Pits top hypotheses against competing off-target or bypass mechanisms to generate a Falsification Dossier with calculated mechanistic margins.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
