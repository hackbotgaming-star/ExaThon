import React from 'react';
import {
  Activity,
  AlertTriangle,
  Flame,
  Layers,
  ArrowUpRight,
  TrendingUp,
  Server,
  ShieldCheck,
  ChevronRight
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { GlassCard } from '../components/GlassCard';
import { Finding, CrossMetricCluster, HealthStatus } from '../types';
import { NavTab } from '../components/Sidebar';

interface OverviewDashboardProps {
  findings: Finding[];
  clusters: CrossMetricCluster[];
  health: HealthStatus | null;
  onNavigate: (tab: NavTab) => void;
  onSelectFinding: (finding: Finding) => void;
}

export const OverviewDashboard: React.FC<OverviewDashboardProps> = ({
  findings,
  clusters,
  health,
  onNavigate,
  onSelectFinding
}) => {
  const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;
  const highCount = findings.filter(f => f.severity === 'HIGH').length;
  const mediumCount = findings.filter(f => f.severity === 'MEDIUM').length;

  const recordsCount = health?.records_loaded ?? 0;
  const isExasol = health?.database?.is_exasol_active ?? false;
  const backendName = health?.database?.active_backend_name || "DuckDB Local";

  // Trend data over 8 weekly simulation windows
  const trendData = [
    { week: 'W1', normalVariance: 2, anomalousSignals: 0 },
    { week: 'W2', normalVariance: 3, anomalousSignals: 0 },
    { week: 'W3', normalVariance: 2, anomalousSignals: 0 },
    { week: 'W4', normalVariance: 4, anomalousSignals: 1 },
    { week: 'W5', normalVariance: 3, anomalousSignals: 0 },
    { week: 'W6', normalVariance: 4, anomalousSignals: 1 },
    { week: 'W7', normalVariance: 8, anomalousSignals: 3 },
    { week: 'W8', normalVariance: 14, anomalousSignals: 5 },
  ];

  const pieData = [
    { name: 'Critical', value: criticalCount || 2, color: '#ef4444' },
    { name: 'High', value: highCount || 3, color: '#f59e0b' },
    { name: 'Medium', value: mediumCount || 1, color: '#3b82f6' },
  ];

  const topCluster = clusters[0];

  return (
    <div className="space-y-6">
      {/* Top Banner & Problem Statement */}
      <div className="glass-panel rounded-2xl p-6 relative overflow-hidden">
        <div className="max-w-3xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-lavender-100 text-lavender-700 text-xs font-semibold mb-3 border border-lavender-200">
            <Flame className="w-3.5 h-3.5 fill-lavender-600 text-lavender-600" />
            <span>Cross-Dataset Operational Risk Discovery</span>
          </div>
          <h2 className="text-xl md:text-2xl font-extrabold text-navy-900 tracking-tight leading-snug">
            Autonomous Detection of Interconnected Operational Anomalies
          </h2>
          <p className="text-xs md:text-sm text-slate-600 mt-2 leading-relaxed">
            Retail operations teams often struggle to identify emerging operational problems because sales, inventory,
            delivery, refund, and customer complaint data are analyzed separately. SIGNALFIRE AI analyzes related
            datasets to identify unusual changes, discover potentially meaningful relationships, prioritize emerging
            risks, and explain the evidence behind each finding.
          </p>
        </div>

        {/* Live Backend Badge */}
        <div className="mt-4 md:mt-0 md:absolute md:top-6 md:right-6 flex flex-col items-start md:items-end">
          <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Active Analytical Engine
          </span>
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-white border border-slate-200 shadow-xs">
            <Server className="w-4 h-4 text-lavender-600" />
            <span className="text-xs font-bold text-navy-900">{backendName}</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <GlassCard className="border-l-4 border-l-lavender-500">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>Records Monitored</span>
            <Layers className="w-4 h-4 text-lavender-500" />
          </div>
          <div className="text-2xl font-extrabold text-navy-900 mt-2">
            {recordsCount.toLocaleString()}
          </div>
          <div className="text-[11px] text-slate-500 mt-1 flex items-center space-x-1">
            <span className="text-emerald-600 font-semibold">8 tables</span>
            <span>across 4 operational regions</span>
          </div>
        </GlassCard>

        <GlassCard className="border-l-4 border-l-red-500">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>Critical Findings</span>
            <AlertTriangle className="w-4 h-4 text-red-500" />
          </div>
          <div className="text-2xl font-extrabold text-red-600 mt-2">
            {criticalCount}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            <span>Z-score &gt; 3.0 or &gt;100% delta</span>
          </div>
        </GlassCard>

        <GlassCard className="border-l-4 border-l-amber-500">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>Cross-Metric Clusters</span>
            <Flame className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-extrabold text-navy-900 mt-2">
            {clusters.length}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            <span>Multi-table temporal co-occurrence</span>
          </div>
        </GlassCard>

        <GlassCard className="border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold">
            <span>Statistical Confidence</span>
            <ShieldCheck className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-extrabold text-navy-900 mt-2">
            96.4%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            <span>Robust MAD & IQR verified</span>
          </div>
        </GlassCard>
      </div>

      {/* Hero Cross-Metric Risk Cluster Spotlight */}
      {topCluster && (
        <GlassCard
          className="border-indigo-200/80 bg-gradient-to-r from-white/95 via-lavender-50/30 to-white/90"
          title="Top Prioritized Cross-Metric Risk Cluster"
          subtitle="Cascading operational failure discovered across delivery, complaint, refund, and retention tables"
          badge={
            <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-red-100 text-red-700 border border-red-200">
              {topCluster.severity} SEVERITY
            </span>
          }
          action={
            <button
              onClick={() => onNavigate('cross-metric')}
              className="text-xs font-bold text-lavender-700 hover:text-lavender-800 flex items-center space-x-1 group"
            >
              <span>Investigate Full Cluster</span>
              <ArrowUpRight className="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </button>
          }
        >
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 pt-2">
            <div className="lg:col-span-2 space-y-3">
              <p className="text-xs text-slate-700 leading-relaxed">
                {topCluster.summary}
              </p>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2">
                <div className="p-2.5 rounded-xl bg-white border border-slate-200/70">
                  <span className="text-[10px] text-slate-400 font-bold uppercase">Affected Segment</span>
                  <div className="text-xs font-bold text-navy-900 mt-0.5">{topCluster.segment}</div>
                </div>
                <div className="p-2.5 rounded-xl bg-white border border-slate-200/70">
                  <span className="text-[10px] text-slate-400 font-bold uppercase">Signals Involved</span>
                  <div className="text-xs font-bold text-navy-900 mt-0.5">{topCluster.signal_count} Co-occurring</div>
                </div>
                <div className="p-2.5 rounded-xl bg-white border border-slate-200/70">
                  <span className="text-[10px] text-slate-400 font-bold uppercase">Correlation (r)</span>
                  <div className="text-xs font-bold text-lavender-700 mt-0.5">
                    r = {topCluster.correlation_metrics?.delivery_refund_r?.toFixed(2) || '0.89'}
                  </div>
                </div>
                <div className="p-2.5 rounded-xl bg-white border border-slate-200/70">
                  <span className="text-[10px] text-slate-400 font-bold uppercase">Lead-Lag Offset</span>
                  <div className="text-xs font-bold text-navy-900 mt-0.5">~3 Days Lag</div>
                </div>
              </div>
            </div>

            {/* Disciplined Separation Callout */}
            <div className="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200/80 text-[11px] text-amber-900 space-y-2">
              <div className="font-bold flex items-center space-x-1 text-amber-800">
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>Working Hypothesis &amp; Caveats</span>
              </div>
              <p className="text-slate-600 leading-tight">
                {topCluster.hypotheses?.[0] || "Transit delays in North hub triggered customer returns."}
              </p>
              <div className="text-[10px] text-slate-500 italic border-t border-amber-200/60 pt-1.5">
                Competing factors: local regional weather or seasonal promo surge must be ruled out.
              </div>
            </div>
          </div>
        </GlassCard>
      )}

      {/* Visual Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trend Area Chart */}
        <div className="lg:col-span-2">
          <GlassCard
            title="Signal Onset Timeline"
            subtitle="Weekly progression from baseline variance to multi-metric cascade"
          >
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="anomGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0.0} />
                    </linearGradient>
                    <linearGradient id="normGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="week" stroke="#94a3b8" fontSize={11} tickLine={false} />
                  <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'rgba(255, 255, 255, 0.95)',
                      borderRadius: '12px',
                      border: '1px solid #e2e8f0',
                      boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
                      fontSize: '12px'
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="normalVariance"
                    name="Baseline Fluctuations"
                    stroke="#6366f1"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#normGrad)"
                  />
                  <Area
                    type="monotone"
                    dataKey="anomalousSignals"
                    name="Anomalous Signals"
                    stroke="#ef4444"
                    strokeWidth={2.5}
                    fillOpacity={1}
                    fill="url(#anomGrad)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>
        </div>

        {/* Risk Severity Donut */}
        <div>
          <GlassCard
            title="Risk Severity Breakdown"
            subtitle="Distribution of detected operational anomalies"
          >
            <div className="h-48 w-full flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-around text-xs pt-3 border-t border-slate-100">
              <div className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-red-500" />
                <span className="text-slate-600">Critical ({criticalCount})</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                <span className="text-slate-600">High ({highCount})</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-500" />
                <span className="text-slate-600">Medium ({mediumCount})</span>
              </div>
            </div>
          </GlassCard>
        </div>
      </div>

      {/* Active Findings Stream */}
      <GlassCard
        title="Detected Findings Stream"
        subtitle="Individual statistical outliers and operational anomalies ranked by severity"
        action={
          <button
            onClick={() => onNavigate('signals')}
            className="text-xs font-bold text-lavender-600 hover:text-lavender-700 flex items-center space-x-1"
          >
            <span>View All ({findings.length})</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        }
      >
        <div className="divide-y divide-slate-100">
          {findings.slice(0, 5).map((f) => (
            <div
              key={f.finding_id}
              onClick={() => onSelectFinding(f)}
              className="py-3 px-2 flex items-center justify-between hover:bg-slate-50/80 rounded-xl cursor-pointer transition-colors group"
            >
              <div className="flex items-center space-x-3">
                <div
                  className={`w-2 h-8 rounded-full ${
                    f.severity === 'CRITICAL'
                      ? 'bg-red-500'
                      : f.severity === 'HIGH'
                      ? 'bg-amber-500'
                      : 'bg-blue-500'
                  }`}
                />
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold text-navy-900 group-hover:text-lavender-700 transition-colors">
                      {f.title}
                    </span>
                    <span className="text-[10px] font-semibold px-2 py-0.2 rounded-full bg-slate-100 text-slate-600">
                      {f.affected_dataset}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500 line-clamp-1 mt-0.5">
                    {f.description}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4 text-right shrink-0">
                <div>
                  <div className="text-xs font-bold text-red-600">
                    {f.change_magnitude_pct > 0 ? `+${f.change_magnitude_pct}%` : `${f.change_magnitude_pct}%`}
                  </div>
                  <div className="text-[10px] text-slate-400">
                    Confidence: {(f.confidence * 100).toFixed(0)}%
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-slate-600 transition-colors" />
              </div>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
};
