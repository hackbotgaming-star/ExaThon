import React from 'react';
import { Flame, Database, RefreshCw, Server, AlertCircle } from 'lucide-react';
import { HealthStatus } from '../types';

interface NavbarProps {
  health: HealthStatus | null;
  onRefresh: () => void;
  onRunAnalysis: () => void;
  isAnalyzing: boolean;
  onOpenSettings: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  health,
  onRefresh,
  onRunAnalysis,
  isAnalyzing,
  onOpenSettings
}) => {
  const isExasol = health?.database?.is_exasol_active ?? false;
  const backendName = health?.database?.active_backend_name || "DuckDB Local";
  const recordsLoaded = health?.records_loaded ?? 0;

  return (
    <header className="h-16 border-b border-slate-200/80 bg-white/75 backdrop-blur-md sticky top-0 z-30 px-6 flex items-center justify-between shadow-subtle">
      {/* Brand Identity */}
      <div className="flex items-center space-x-3.5">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-lavender-600 via-indigo-500 to-ice-500 flex items-center justify-center shadow-md shadow-indigo-500/20 text-white">
          <Flame className="w-5 h-5 fill-white/20 stroke-[2.2]" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-lg font-bold tracking-tight text-navy-900 leading-none">
              SIGNALFIRE <span className="text-lavender-600 font-extrabold">AI</span>
            </h1>
            <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-lavender-100 text-lavender-700 border border-lavender-200/60">
              Enterprise Hackathon
            </span>
          </div>
          <p className="text-[11px] text-slate-500 font-medium tracking-tight mt-0.5">
            Find the warning signs hidden across your data.
          </p>
        </div>
      </div>

      {/* Right Actions & Active Backend Badge */}
      <div className="flex items-center space-x-3">
        {/* Active Database Badge - Transparency Mandate */}
        <button
          onClick={onOpenSettings}
          className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
            isExasol
              ? 'bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100/80 shadow-sm'
              : 'bg-ice-50 text-ice-700 border-ice-200 hover:bg-ice-100/80'
          }`}
          title="Click to view database connection status and configuration"
        >
          <Server className="w-3.5 h-3.5" />
          <span>Backend: <strong className="font-bold">{isExasol ? "Exasol Personal" : "DuckDB Local"}</strong></span>
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
        </button>

        {/* Records Count Badge */}
        <div className="hidden md:flex items-center space-x-1.5 text-xs text-slate-600 bg-slate-100/80 px-2.5 py-1.5 rounded-lg border border-slate-200/60">
          <Database className="w-3.5 h-3.5 text-slate-500" />
          <span>{recordsLoaded.toLocaleString()} records monitored</span>
        </div>

        {/* Run Analysis Action */}
        <button
          onClick={onRunAnalysis}
          disabled={isAnalyzing}
          className="flex items-center space-x-2 px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-navy-900 text-white hover:bg-navy-800 shadow-sm transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isAnalyzing ? "animate-spin" : ""}`} />
          <span>{isAnalyzing ? "Analyzing Streams..." : "Run Analysis"}</span>
        </button>
      </div>
    </header>
  );
};
