'use client';

import { useState, useEffect } from 'react';
import { GitBranch, Info } from 'lucide-react';
import { apiClient } from '@/lib/api-client';

export default function CausalGraphViewer() {
  const [graphData, setGraphData] = useState<{ nodes: any[]; edges: any[] }>({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState<any>(null);

  useEffect(() => {
    async function loadGraph() {
      try {
        const res = await apiClient.get('/graphs');
        setGraphData(res.data);
      } catch (err) {
        console.error("Graph fetch error:", err);
      }
    }
    loadGraph();
  }, []);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col h-[500px]">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <GitBranch className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">Multipartite & Causal Knowledge Graph</h3>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          {graphData.nodes.length} Entities | {graphData.edges.length} Relationships
        </span>
      </div>

      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-4 overflow-hidden">
        {/* Node/Edge List Visualizer */}
        <div className="md:col-span-2 bg-slate-950 border border-slate-800 rounded-lg p-4 overflow-y-auto font-mono text-xs">
          <div className="text-slate-400 mb-3 font-semibold text-[11px] uppercase tracking-wider">Active Multipartite Subgraph Nodes</div>
          <div className="grid grid-cols-2 gap-2 mb-4">
            {graphData.nodes.map((n) => (
              <button
                key={n.data.id}
                onClick={() => setSelectedNode(n.data)}
                className={`p-2.5 rounded border text-left transition flex items-center justify-between ${
                  selectedNode?.id === n.data.id
                    ? 'bg-brand-600/30 border-brand-500 text-cyan-300'
                    : 'bg-slate-900 border-slate-800 hover:border-slate-700 text-slate-200'
                }`}
              >
                <div>
                  <div className="font-bold">{n.data.symbol}</div>
                  <div className="text-[10px] text-slate-400">{n.data.type}</div>
                </div>
                <span className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-300">
                  {n.data.type}
                </span>
              </button>
            ))}
          </div>

          <div className="text-slate-400 mb-2 font-semibold text-[11px] uppercase tracking-wider">Causal Relationships</div>
          <div className="space-y-1.5">
            {graphData.edges.map((e) => (
              <div key={e.data.id} className="p-2 bg-slate-900 border border-slate-800/80 rounded flex items-center justify-between">
                <span className="text-cyan-400 font-bold">{e.data.source}</span>
                <span className="text-amber-400 font-mono text-[10px] bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800/50">
                  -- [{e.data.label}] --&gt;
                </span>
                <span className="text-emerald-400 font-bold">{e.data.target}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Selected Entity Details Panel */}
        <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 flex flex-col justify-between">
          <div>
            <div className="text-xs text-slate-400 font-mono mb-2 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-cyan-400" />
              <span>Entity Provenance Inspector</span>
            </div>
            {selectedNode ? (
              <div className="space-y-3 font-mono text-xs">
                <div>
                  <div className="text-[10px] text-slate-500">CANONICAL NAME</div>
                  <div className="text-white font-bold text-sm">{selectedNode.label}</div>
                </div>
                <div>
                  <div className="text-[10px] text-slate-500">ENTITY TYPE</div>
                  <div className="text-cyan-400">{selectedNode.type}</div>
                </div>
                <div>
                  <div className="text-[10px] text-slate-500">EXTERNAL IDENTIFIERS</div>
                  <div className="text-slate-300">HGNC:9031 | ChEMBL:4801928</div>
                </div>
                <div>
                  <div className="text-[10px] text-slate-500">EVIDENCE MATURITY</div>
                  <div className="text-emerald-400 font-semibold">EXPERIMENTALLY_VALIDATED</div>
                </div>
              </div>
            ) : (
              <div className="text-slate-500 text-xs italic mt-8 text-center">
                Select an entity node to inspect evidence lineage and provenance parameters.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
