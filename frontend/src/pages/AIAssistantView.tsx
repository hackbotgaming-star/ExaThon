import React, { useState } from 'react';
import { Bot, Send, Sparkles, ShieldCheck, HelpCircle, Terminal } from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { sendChatMessage } from '../services/api';

export const AIAssistantView: React.FC = () => {
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'assistant'; text: string; mode?: string }>>([
    {
      sender: 'assistant',
      text: "Hello! I am the **SIGNALFIRE AI Investigation Assistant**. I evaluate live findings through approved analytical tools to provide verified, evidence-backed answers without hallucinating metrics.\n\nFeel free to ask questions about current operational signals, regional trends, or competing hypotheses.",
      mode: "Deterministic Analytical Assistant (Tool-Engine Active)"
    }
  ]);
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const sampleQuestions = [
    "What changed most significantly this week?",
    "Which region has the largest increase in refunds?",
    "Which findings deserve investigation first?",
    "What alternative explanations should I consider?",
    "Which datasets should I examine next?"
  ];

  const handleSend = async (queryText?: string) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || isLoading) return;

    const userMsg = { sender: 'user' as const, text: textToSend };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await sendChatMessage(textToSend);
      setMessages(prev => [...prev, {
        sender: 'assistant',
        text: res.answer,
        mode: res.mode
      }]);
    } catch (e: any) {
      setMessages(prev => [...prev, {
        sender: 'assistant',
        text: `Error retrieving analytical evidence: ${e.message}`,
        mode: "Error"
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
            AI Investigation Assistant
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Tool-grounded conversational analyst. Retrieves verified evidence from analytical database queries.
          </p>
        </div>

        {/* Mode Indicator Badge */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-lavender-50 border border-lavender-200/80 text-xs font-semibold text-lavender-700 shadow-2xs">
          <Terminal className="w-3.5 h-3.5" />
          <span>Active: <strong>Tool-Engine Grounded</strong></span>
        </div>
      </div>

      {/* Main Chat Container */}
      <GlassCard className="h-[600px] flex flex-col justify-between p-0 overflow-hidden">
        {/* Messages Scroll Area */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex items-start space-x-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {m.sender === 'assistant' && (
                <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-lavender-600 to-indigo-500 flex items-center justify-center text-white shrink-0 shadow-sm mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-2xl rounded-2xl p-4 text-xs leading-relaxed ${
                  m.sender === 'user'
                    ? 'bg-navy-900 text-white shadow-xs font-medium'
                    : 'bg-white border border-slate-200/80 text-slate-700 shadow-xs'
                }`}
              >
                {m.mode && (
                  <div className="text-[10px] font-mono text-lavender-600 font-bold mb-1 pb-1 border-b border-slate-100">
                    Mode: {m.mode}
                  </div>
                )}
                <div className="whitespace-pre-line prose prose-xs max-w-none">
                  {m.text}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex items-center space-x-3 text-xs text-slate-400 p-2">
              <Bot className="w-4 h-4 animate-spin text-lavender-500" />
              <span>Querying analytical engines and validating evidence...</span>
            </div>
          )}
        </div>

        {/* Quick Sample Questions Chips */}
        <div className="px-5 py-2.5 bg-slate-50/70 border-t border-slate-100 flex items-center space-x-2 overflow-x-auto scrollbar-none">
          <Sparkles className="w-3.5 h-3.5 text-lavender-600 shrink-0" />
          <span className="text-[10px] font-bold text-slate-400 uppercase shrink-0">Quick Queries:</span>
          {sampleQuestions.map((q, i) => (
            <button
              key={i}
              onClick={() => handleSend(q)}
              className="text-[11px] px-2.5 py-1 rounded-full bg-white hover:bg-lavender-50 text-slate-600 hover:text-lavender-700 border border-slate-200 shrink-0 transition-colors"
            >
              {q}
            </button>
          ))}
        </div>

        {/* Query Input Box */}
        <div className="p-4 bg-white border-t border-slate-200/80">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center space-x-2"
          >
            <input
              type="text"
              placeholder="Ask a question about active signals, regional trends, or alternative explanations..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 px-4 py-2.5 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-lavender-500/20 focus:border-lavender-500"
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="px-4 py-2.5 rounded-xl bg-navy-900 text-white text-xs font-bold hover:bg-navy-800 disabled:opacity-40 transition-all flex items-center space-x-1.5 shadow-sm"
            >
              <span>Ask</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>
      </GlassCard>
    </div>
  );
};
