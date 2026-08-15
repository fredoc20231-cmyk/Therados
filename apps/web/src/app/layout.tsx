import type { Metadata } from 'next';
import './globals.css';
import Link from 'next/link';
import { Dna, ShieldCheck, Cpu, Layers, Terminal, Activity, FileText } from 'lucide-react';

export const metadata: Metadata = {
  title: 'TheraDOS — Therapeutic Domain Operating System',
  description: 'Provenance-aware therapeutic intelligence operating system converting evidence into falsifiable hypotheses.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
        {/* Top Enterprise Header */}
        <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50 px-6 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-brand-600 text-white p-2 rounded-lg font-bold shadow-lg shadow-brand-500/20 flex items-center space-x-2">
              <Dna className="w-5 h-5 animate-pulse" />
              <span className="tracking-wider text-lg font-mono">TheraDOS</span>
            </div>
            <span className="text-xs bg-slate-800 text-cyan-400 px-2.5 py-1 rounded-full font-mono border border-cyan-500/30">
              v1.0.0 PROD-READY
            </span>
          </div>

          <nav className="flex items-center space-x-6 text-sm font-medium">
            <Link href="/" className="text-slate-300 hover:text-cyan-400 transition flex items-center space-x-1.5">
              <span>Overview</span>
            </Link>
            <Link href="/dashboard" className="text-slate-300 hover:text-cyan-400 transition flex items-center space-x-1.5">
              <Activity className="w-4 h-4 text-cyan-400" />
              <span>Dashboard</span>
            </Link>
            <Link href="/workspace" className="text-slate-100 font-semibold bg-brand-600/30 border border-brand-500/50 hover:bg-brand-600/50 text-cyan-300 px-3 py-1.5 rounded-md transition flex items-center space-x-2">
              <Cpu className="w-4 h-4" />
              <span>Program Workspace</span>
            </Link>
          </nav>

          <div className="flex items-center space-x-3 text-xs">
            <div className="flex items-center space-x-1.5 text-emerald-400 bg-emerald-950/60 border border-emerald-800/80 px-2.5 py-1 rounded">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Provenanced Governance</span>
            </div>
          </div>
        </header>

        <main className="flex-1 flex flex-col">
          {children}
        </main>

        <footer className="border-t border-slate-800/80 bg-slate-950 px-6 py-3 text-xs text-slate-500 flex justify-between items-center">
          <div>
            TheraDOS Therapeutic Domain Operating System © 2026 — Research & Therapeutic Development Decision Support Software
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-amber-500/90 font-mono">NOT AUTONOMOUS MEDICAL ADVICE</span>
          </div>
        </footer>
      </body>
    </html>
  );
}
