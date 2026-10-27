import React, { useState } from 'react';
import { Network, Activity, AlertTriangle, ShieldCheck, ChevronRight, Layers, X } from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { Finding, CrossMetricCluster } from '../types';

interface InteractiveRiskMapProps {
  findings: Finding[];
  clusters: CrossMetricCluster[];
  onSelectFinding: (f: Finding) => void;
}

export const InteractiveRiskMap: React.FC<InteractiveRiskMapProps> = ({
  findings,
  clusters,
  onSelectFinding
}) => {
  const [activeNode, setActiveNode] = useState<any | null>(null);

  // Group nodes by region
  const regions = [
    { id: 'North', name: 'North Operational Region', status: 'CRITICAL', riskScore: 88, signals: findings.filter(f => f.affected_segment.includes('North')) },
    { id: 'South', name: 'South Operational Region', status: 'HEALTHY', riskScore: 12, signals: findings.filter(f => f.affected_segment.includes('South')) },
    { id: 'East', name: 'East Operational Region', status: 'HEALTHY', riskScore: 14, signals: findings.filter(f => f.affected_segment.includes('East')) },
    { id: 'West', name: 'West Operational Region', status: 'HEALTHY', riskScore: 16, signals: findings.filter(f => f.affected_segment.includes('West')) },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
          Interactive Operational Risk Map
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Topological map of business segments, interconnected anomaly nodes, and causal cascade pathways.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Interactive Topological Canvas */}
        <div className="lg:col-span-2">
          <GlassCard title="Topological Risk Network" subtitle="Click any segment or node to inspect interconnected telemetry">
            <div className="h-[460px] w-full rounded-2xl bg-gradient-to-br from-slate-50/80 via-white to-lavender-50/20 border border-slate-200/80 relative flex items-center justify-center p-6 overflow-hidden">
              {/* Background topological grid */}
              <div className="absolute inset-0 bg-[radial-gradient(#cbd5e1_1px,transparent_1px)] [background-size:20px_20px] opacity-40 pointer-events-none" />

              {/* Central Core SignalFire Hub */}
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center pointer-events-none z-10">
                <div className="w-20 h-20 rounded-full bg-lavender-100/90 border-2 border-lavender-300 flex items-center justify-center shadow-lg backdrop-blur-xs animate-pulse">
                  <Network className="w-8 h-8 text-lavender-600" />
                </div>
                <span className="text-[10px] font-extrabold uppercase tracking-wider text-slate-400 mt-1 block">
                  SignalFire Nexus
                </span>
              </div>

              {/* Connecting SVG lines between central hub and regional nodes */}
              <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
                <line x1="50%" y1="50%" x2="25%" y2="25%" stroke="#ef4444" strokeWidth="2.5" strokeDasharray="4,4" className="animate-[dash_1s_linear_infinite]" />
                <line x1="50%" y1="50%" x2="75%" y2="25%" stroke="#10b981" strokeWidth="1.5" />
                <line x1="50%" y1="50%" x2="25%" y2="75%" stroke="#10b981" strokeWidth="1.5" />
                <line x1="50%" y1="50%" x2="75%" y2="75%" stroke="#10b981" strokeWidth="1.5" />
              </svg>

              {/* Regional Segment Nodes */}
              {/* North: Top Left (CRITICAL) */}
              <div
                onClick={() => setActiveNode(regions[0])}
                className={`absolute top-8 left-8 sm:top-12 sm:left-12 p-4 rounded-2xl cursor-pointer transition-all z-20 ${
                  activeNode?.id === 'North'
                    ? 'ring-4 ring-red-400 bg-white shadow-xl scale-105'
                    : 'bg-white/95 border-2 border-red-300 hover:border-red-400 hover:scale-102 shadow-md'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span className="w-3 h-3 rounded-full bg-red-500 animate-ping" />
                  <span className="text-xs font-bold text-navy-900">North Region</span>
                </div>
                <div className="text-[11px] text-red-600 font-extrabold mt-1">
                  Risk Score: 88 / 100
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">
                  5 Co-occurring Anomalies
                </div>
              </div>

              {/* South: Top Right (HEALTHY) */}
              <div
                onClick={() => setActiveNode(regions[1])}
                className={`absolute top-8 right-8 sm:top-12 sm:right-12 p-4 rounded-2xl cursor-pointer transition-all z-20 ${
                  activeNode?.id === 'South'
                    ? 'ring-4 ring-emerald-400 bg-white shadow-xl scale-105'
                    : 'bg-white/95 border border-emerald-200 hover:border-emerald-300 hover:scale-102 shadow-md'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                  <span className="text-xs font-bold text-navy-900">South Region</span>
                </div>
                <div className="text-[11px] text-emerald-600 font-bold mt-1">
                  Risk Score: 12 / 100
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">
                  Baseline Fluctuations
                </div>
              </div>

              {/* East: Bottom Left (HEALTHY) */}
              <div
                onClick={() => setActiveNode(regions[2])}
                className={`absolute bottom-8 left-8 sm:bottom-12 sm:left-12 p-4 rounded-2xl cursor-pointer transition-all z-20 ${
                  activeNode?.id === 'East'
                    ? 'ring-4 ring-emerald-400 bg-white shadow-xl scale-105'
                    : 'bg-white/95 border border-emerald-200 hover:border-emerald-300 hover:scale-102 shadow-md'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                  <span className="text-xs font-bold text-navy-900">East Region</span>
                </div>
                <div className="text-[11px] text-emerald-600 font-bold mt-1">
                  Risk Score: 14 / 100
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">
                  Baseline Fluctuations
                </div>
              </div>

              {/* West: Bottom Right (HEALTHY) */}
              <div
                onClick={() => setActiveNode(regions[3])}
                className={`absolute bottom-8 right-8 sm:bottom-12 sm:right-12 p-4 rounded-2xl cursor-pointer transition-all z-20 ${
                  activeNode?.id === 'West'
                    ? 'ring-4 ring-emerald-400 bg-white shadow-xl scale-105'
                    : 'bg-white/95 border border-emerald-200 hover:border-emerald-300 hover:scale-102 shadow-md'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                  <span className="text-xs font-bold text-navy-900">West Region</span>
                </div>
                <div className="text-[11px] text-emerald-600 font-bold mt-1">
                  Risk Score: 16 / 100
                </div>
                <div className="text-[10px] text-slate-500 mt-0.5">
                  Baseline Fluctuations
                </div>
              </div>
            </div>
          </GlassCard>
        </div>

        {/* Node Detail Drawer / Inspection Panel */}
        <div>
          <GlassCard
            title={activeNode ? activeNode.name : "Segment Risk Inspector"}
            subtitle={activeNode ? `Active status: ${activeNode.status}` : "Select any segment node to review signals"}
            badge={
              activeNode && (
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
                  activeNode.status === 'CRITICAL' ? 'bg-red-100 text-red-700' : 'bg-emerald-100 text-emerald-700'
                }`}>
                  {activeNode.status}
                </span>
              )
            }
          >
            {activeNode ? (
              <div className="space-y-4 text-xs">
                <div className="p-3 rounded-xl bg-slate-50 border border-slate-200">
                  <div className="flex justify-between items-center text-[11px] mb-1">
                    <span className="text-slate-500">Composite Risk Index</span>
                    <strong className={activeNode.riskScore > 50 ? 'text-red-600' : 'text-emerald-600'}>
                      {activeNode.riskScore} / 100
                    </strong>
                  </div>
                  <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                    <div
                      className={`h-full rounded-full ${activeNode.riskScore > 50 ? 'bg-red-500' : 'bg-emerald-500'}`}
                      style={{ width: `${activeNode.riskScore}%` }}
                    />
                  </div>
                </div>

                <div>
                  <h4 className="font-bold text-navy-900 mb-2">Interconnected Anomalies ({activeNode.signals.length}):</h4>
                  {activeNode.signals.length === 0 ? (
                    <p className="text-slate-400 italic">No statistical anomalies detected in this segment.</p>
                  ) : (
                    <div className="space-y-2">
                      {activeNode.signals.map((s: Finding) => (
                        <div
                          key={s.finding_id}
                          onClick={() => onSelectFinding(s)}
                          className="p-2.5 rounded-xl bg-white border border-slate-200 hover:border-lavender-300 hover:bg-slate-50 cursor-pointer transition-all"
                        >
                          <div className="flex justify-between items-center">
                            <span className="font-bold text-navy-900 text-xs">{s.title}</span>
                            <span className="text-[10px] font-extrabold text-red-600">
                              {s.change_magnitude_pct > 0 ? `+${s.change_magnitude_pct}%` : `${s.change_magnitude_pct}%`}
                            </span>
                          </div>
                          <span className="text-[10px] text-slate-400 font-mono mt-0.5 block">{s.finding_id}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="p-8 text-center text-slate-400">
                <Layers className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>Click on North, South, East, or West on the map to inspect localized telemetries.</p>
              </div>
            )}
          </GlassCard>
        </div>
      </div>
    </div>
  );
};
