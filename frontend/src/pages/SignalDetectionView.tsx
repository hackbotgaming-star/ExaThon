import React, { useState } from 'react';
import {
  Activity,
  AlertTriangle,
  Filter,
  CheckCircle2,
  Calendar,
  Layers,
  Search,
  ExternalLink,
  ChevronRight,
  X
} from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { Finding } from '../types';

interface SignalDetectionViewProps {
  findings: Finding[];
  onSelectFinding: (f: Finding) => void;
  selectedFinding: Finding | null;
  onCloseDetail: () => void;
  onOpenWorkspace: (f: Finding) => void;
}

export const SignalDetectionView: React.FC<SignalDetectionViewProps> = ({
  findings,
  onSelectFinding,
  selectedFinding,
  onCloseDetail,
  onOpenWorkspace
}) => {
  const [severityFilter, setSeverityFilter] = useState<string>('ALL');
  const [datasetFilter, setDatasetFilter] = useState<string>('ALL');
  const [search, setSearch] = useState<string>('');

  const datasets = Array.from(new Set(findings.map(f => f.affected_dataset)));

  const filtered = findings.filter(f => {
    if (severityFilter !== 'ALL' && f.severity !== severityFilter) return false;
    if (datasetFilter !== 'ALL' && f.affected_dataset !== datasetFilter) return false;
    if (search && !f.title.toLowerCase().includes(search.toLowerCase()) && !f.description.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
            Signal Detection Engine
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Statistical outliers and multi-dimensional anomalies isolated via Robust Z-Score, MAD, and IQR fences.
          </p>
        </div>

        {/* Severity Count Pills */}
        <div className="flex items-center space-x-2">
          {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM'].map((sev) => {
            const count = sev === 'ALL' ? findings.length : findings.filter(f => f.severity === sev).length;
            return (
              <button
                key={sev}
                onClick={() => setSeverityFilter(sev)}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all border ${
                  severityFilter === sev
                    ? 'bg-navy-900 text-white border-navy-900 shadow-xs'
                    : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                }`}
              >
                {sev} ({count})
              </button>
            );
          })}
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search findings by keyword, segment, or description..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-xs rounded-xl bg-white border border-slate-200 focus:outline-none focus:ring-2 focus:ring-lavender-500/20 focus:border-lavender-500"
          />
        </div>

        <div className="flex items-center space-x-2 shrink-0">
          <Filter className="w-3.5 h-3.5 text-slate-400" />
          <select
            value={datasetFilter}
            onChange={(e) => setDatasetFilter(e.target.value)}
            className="px-3 py-2 rounded-xl text-xs bg-white border border-slate-200 font-semibold text-slate-700 focus:outline-none"
          >
            <option value="ALL">All Datasets</option>
            {datasets.map(d => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Findings Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((f) => {
          const isCritical = f.severity === 'CRITICAL';
          const isHigh = f.severity === 'HIGH';

          return (
            <GlassCard
              key={f.finding_id}
              className={`cursor-pointer transition-all ${
                selectedFinding?.finding_id === f.finding_id ? 'ring-2 ring-lavender-500 bg-lavender-50/20' : ''
              }`}
            >
              <div onClick={() => onSelectFinding(f)} className="space-y-3">
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2">
                    <span
                      className={`px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase border ${
                        isCritical
                          ? 'bg-red-100 text-red-700 border-red-200'
                          : isHigh
                          ? 'bg-amber-100 text-amber-800 border-amber-200'
                          : 'bg-blue-100 text-blue-700 border-blue-200'
                      }`}
                    >
                      {f.severity}
                    </span>
                    <span className="text-[11px] font-mono text-slate-400">
                      {f.finding_id}
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-xs font-extrabold text-red-600">
                      {f.change_magnitude_pct > 0 ? `+${f.change_magnitude_pct}%` : `${f.change_magnitude_pct}%`}
                    </span>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-bold text-navy-900 hover:text-lavender-700 transition-colors">
                    {f.title}
                  </h3>
                  <p className="text-xs text-slate-600 mt-1 line-clamp-2 leading-relaxed">
                    {f.description}
                  </p>
                </div>

                {/* Metrics Breakdown */}
                <div className="grid grid-cols-3 gap-2 py-2 border-y border-slate-100 text-[11px]">
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase font-bold">Observed</span>
                    <strong className="text-navy-900 font-mono">{f.observed_value}</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase font-bold">Baseline</span>
                    <strong className="text-slate-600 font-mono">{f.expected_value}</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase font-bold">Confidence</span>
                    <strong className="text-emerald-700 font-mono">{(f.confidence * 100).toFixed(0)}%</strong>
                  </div>
                </div>

                {/* Footer metadata */}
                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span className="bg-slate-100 px-2 py-0.5 rounded font-medium text-slate-600">
                    {f.affected_segment}
                  </span>
                  <div className="flex items-center space-x-1 text-lavender-600 font-semibold group-hover:translate-x-1 transition-transform">
                    <span>Inspect Evidence</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </div>
                </div>
              </div>
            </GlassCard>
          );
        })}
      </div>

      {/* Finding Deep Inspection Modal / Slide-out */}
      {selectedFinding && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-md flex items-center justify-center p-4 overflow-y-auto custom-scrollbar">
          <div className="glass-modal-3d custom-scrollbar rounded-3xl max-w-2xl w-full max-h-[88vh] overflow-y-auto p-6 md:p-8 space-y-5 animate-in fade-in zoom-in-95 duration-200">
            {/* Modal Header */}
            <div className="flex items-start justify-between border-b border-slate-200/60 pb-4">
              <div>
                <div className="flex items-center space-x-2">
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase border shadow-xs ${
                    selectedFinding.severity === 'CRITICAL' ? 'bg-red-100/90 text-red-700 border-red-200' : 'bg-amber-100/90 text-amber-800 border-amber-200'
                  }`}>
                    {selectedFinding.severity}
                  </span>
                  <span className="text-xs font-mono text-slate-400 font-semibold">{selectedFinding.finding_id}</span>
                </div>
                <h3 className="text-lg font-extrabold text-navy-900 mt-2 tracking-tight">{selectedFinding.title}</h3>
              </div>
              <button
                onClick={onCloseDetail}
                className="p-2 rounded-xl bg-white/70 hover:bg-slate-100 text-slate-400 hover:text-slate-700 border border-slate-200/60 shadow-xs transition-all"
                title="Close modal"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Evidence & Methodology Breakdown */}
            <div className="space-y-4 text-xs">
              <div>
                <h4 className="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Description</h4>
                <p className="text-slate-700 mt-1 leading-relaxed text-xs">{selectedFinding.description}</p>
              </div>

              {/* 3D Embossed KPI Metric Tiles */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="tile-3d-embossed p-3.5 rounded-2xl">
                  <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Observed Value</span>
                  <div className="text-base font-extrabold text-navy-900 mt-1 font-mono">{selectedFinding.observed_value}</div>
                </div>
                <div className="tile-3d-embossed p-3.5 rounded-2xl">
                  <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Baseline Expectation</span>
                  <div className="text-base font-extrabold text-slate-600 mt-1 font-mono">{selectedFinding.expected_value}</div>
                </div>
                <div className="tile-3d-embossed p-3.5 rounded-2xl">
                  <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Shift Magnitude</span>
                  <div className="text-base font-extrabold text-red-600 mt-1 font-mono">
                    {selectedFinding.change_magnitude_pct > 0 ? `+${selectedFinding.change_magnitude_pct}%` : `${selectedFinding.change_magnitude_pct}%`}
                  </div>
                </div>
                <div className="tile-3d-embossed p-3.5 rounded-2xl">
                  <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Confidence</span>
                  <div className="text-base font-extrabold text-emerald-700 mt-1 font-mono">
                    {(selectedFinding.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              {/* 3D Detection Methodology Glass Card */}
              <div>
                <h4 className="font-bold text-slate-400 uppercase text-[10px] tracking-wider mb-1">Detection Methodology</h4>
                <div className="p-3.5 rounded-2xl bg-gradient-to-br from-lavender-50/70 via-white/80 to-indigo-50/40 border border-lavender-200/80 shadow-[inset_0_1.5px_2px_rgba(255,255,255,1),0_2px_8px_rgba(99,102,241,0.06)] text-slate-700 font-mono text-[11px]">
                  <div className="font-bold text-indigo-900">{selectedFinding.detection_method}</div>
                  <div className="text-slate-600 font-sans mt-1 leading-normal">
                    {selectedFinding.confidence_rationale}
                  </div>
                </div>
              </div>

              {/* Time Windows 3D Tiles */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="tile-3d-embossed p-3.5 rounded-2xl">
                  <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Active Time Window</span>
                  <div className="text-xs font-semibold text-slate-800 mt-1 font-mono">{selectedFinding.relevant_time_window}</div>
                </div>
                <div className="tile-3d-embossed p-3.5 rounded-2xl">
                  <span className="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Baseline Reference Period</span>
                  <div className="text-xs font-semibold text-slate-800 mt-1 font-mono">{selectedFinding.baseline_period}</div>
                </div>
              </div>

              {/* Recommended Next Action 3D Rim Card */}
              <div className="p-4 rounded-2xl bg-gradient-to-r from-amber-50/90 via-amber-50/50 to-white/90 border border-amber-200/90 shadow-[inset_0_1.5px_2px_rgba(255,255,255,1),0_4px_12px_-2px_rgba(245,158,11,0.12)] text-amber-950">
                <span className="font-bold block mb-1 text-xs text-amber-900">Recommended Next Action:</span>
                <p className="leading-relaxed text-xs">{selectedFinding.suggested_next_investigation}</p>
              </div>

              <div className="text-[11px] text-slate-400 italic">
                Data Quality Warning: {selectedFinding.data_quality_warnings}
              </div>
            </div>

            {/* Modal Actions */}
            <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-200/60">
              <button
                onClick={onCloseDetail}
                className="btn-3d px-4 py-2 rounded-xl text-xs font-bold text-slate-600 bg-white border border-slate-200 hover:bg-slate-50"
              >
                Close
              </button>
              <button
                onClick={() => {
                  onOpenWorkspace(selectedFinding);
                  onCloseDetail();
                }}
                className="btn-3d px-4 py-2 rounded-xl text-xs font-bold bg-navy-900 text-white hover:bg-navy-800 shadow-md"
              >
                Open in Investigation Workspace
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
