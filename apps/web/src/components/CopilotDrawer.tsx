'use client';

import { useState } from 'react';
import { Cpu, Send, BookOpen, AlertCircle } from 'lucide-react';
import { queryCopilot } from '@/lib/api-client';

interface Props {
  programId: string;
}

export default function CopilotDrawer({ programId }: Props) {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;
    const userMsg = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    const currQuery = query;
    setQuery('');

    try {
      const res = await queryCopilot(programId, currQuery);
      const botMsg = {
        role: 'copilot',
        answer: res.answer,
        citations: res.citations,
        confidence: res.confidence,
        uncertainties: res.uncertainties
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error("Copilot error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col h-[500px]">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-cyan-400" />
          <h3 className="text-base font-bold text-white">TheraDOS Grounded Scientific Copilot</h3>
        </div>
        <span className="text-[10px] bg-cyan-950 text-cyan-300 border border-cyan-800 px-2 py-0.5 rounded font-mono">
          Internal Citations Active
        </span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2 font-mono text-xs">
        {messages.map((m, idx) => (
          <div key={idx} className={`p-3 rounded-lg ${m.role === 'user' ? 'bg-brand-600/20 border border-brand-500/40 ml-8 text-cyan-200' : 'bg-slate-950 border border-slate-800 mr-8 text-slate-200'}`}>
            {m.role === 'user' ? (
              <div>{m.content}</div>
            ) : (
              <div className="space-y-2">
                <p className="leading-relaxed">{m.answer}</p>

                {m.citations && m.citations.length > 0 && (
                  <div className="pt-2 border-t border-slate-800 space-y-1">
                    <div className="text-[10px] text-slate-500 font-bold uppercase flex items-center gap-1">
                      <BookOpen className="w-3 h-3 text-cyan-400" />
                      <span>Internal Evidence Citations</span>
                    </div>
                    {m.citations.map((c: any, i: number) => (
                      <div key={i} className="text-[10px] text-cyan-400 bg-slate-900 p-1.5 rounded border border-slate-800">
                        [{c.evidence_id}] {c.source}: {c.claim}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="text-xs text-cyan-400 font-mono animate-pulse">Querying grounded program evidence...</div>}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Ask Copilot about program hypotheses, citations, or falsification..."
          className="flex-1 bg-slate-950 border border-slate-800 rounded px-3 py-2 text-slate-200 text-xs focus:outline-none focus:border-brand-500 font-mono"
        />
        <button
          onClick={handleSend}
          className="bg-brand-600 hover:bg-brand-500 text-white px-4 py-2 rounded font-semibold text-xs flex items-center gap-1 transition"
        >
          <Send className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
