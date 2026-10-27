import React from 'react';
import { FileDown, FileText, Download, CheckCircle2, ShieldAlert, Sparkles } from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { Finding, CrossMetricCluster, HealthStatus } from '../types';

interface ReportsViewProps {
  findings: Finding[];
  clusters: CrossMetricCluster[];
  health: HealthStatus | null;
}

export const ReportsView: React.FC<ReportsViewProps> = ({ findings, clusters, health }) => {
  const backendName = health?.database?.active_backend_name || "DuckDB Local";
  const recordsLoaded = health?.records_loaded ?? 0;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
          Executive Reports &amp; Data Export
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Generate audit-ready reports containing cross-metric syntheses, empirical statistics, and remediation plans.
        </p>
      </div>

      {/* Export Format Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* PDF Executive Report Card */}
        <GlassCard
          className="border-indigo-200/90 bg-gradient-to-br from-white via-lavender-50/20 to-white ring-1 ring-lavender-200 flex flex-col justify-between"
          title="Executive PDF Report"
          subtitle="Audit-ready publication layout generated via ReportLab"
          badge={
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-lavender-100 text-lavender-700">
              PDF FORMAT
            </span>
          }
        >
          <div className="space-y-3 text-xs text-slate-600 my-4">
            <p>
              Includes Executive Summary, Prioritized Findings Table, Cross-Metric Risk Clusters,
              Empirical Pearson Correlations, Control Cohort Benchmarks, and Recommendations.
            </p>
            <div className="text-[11px] text-slate-500 font-mono">
              Engine Backend: {backendName}
            </div>
          </div>

          <a
            href="/api/reports/pdf"
            download="SIGNALFIRE_Executive_Report.pdf"
            className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl text-xs font-bold bg-navy-900 text-white hover:bg-navy-800 shadow-sm transition-all"
          >
            <Download className="w-4 h-4" />
            <span>Download Executive PDF</span>
          </a>
        </GlassCard>

        {/* JSON Structured Data Export Card */}
        <GlassCard
          className="flex flex-col justify-between"
          title="Structured JSON Export"
          subtitle="Machine-readable data manifest for BI integrations"
          badge={
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
              JSON SCHEMA
            </span>
          }
        >
          <div className="space-y-3 text-xs text-slate-600 my-4">
            <p>
              Complete telemetry export containing finding schemas, confidence metrics, baseline
              windows, observed values, and cross-dataset correlation matrices.
            </p>
            <div className="text-[11px] text-slate-500 font-mono">
              Findings Count: {findings.length} records
            </div>
          </div>

          <a
            href="/api/reports/json"
            download="SIGNALFIRE_Report.json"
            className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl text-xs font-bold bg-white border border-slate-200 text-navy-900 hover:bg-slate-50 shadow-xs transition-all"
          >
            <Download className="w-4 h-4" />
            <span>Download Full JSON Manifest</span>
          </a>
        </GlassCard>

        {/* CSV Tabular Export Card */}
        <GlassCard
          className="flex flex-col justify-between"
          title="Tabular CSV Export"
          subtitle="Spreadsheet format for Excel, Tableau, and PowerBI"
          badge={
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
              CSV TABULAR
            </span>
          }
        >
          <div className="space-y-3 text-xs text-slate-600 my-4">
            <p>
              Flat tabular export of detected signals, severity ratings, segments, observed vs baseline values,
              detection methods, and current investigation statuses.
            </p>
            <div className="text-[11px] text-slate-500 font-mono">
              Ready for spreadsheet analysis
            </div>
          </div>

          <a
            href="/api/reports/csv"
            download="SIGNALFIRE_Findings.csv"
            className="w-full flex items-center justify-center space-x-2 py-2.5 px-4 rounded-xl text-xs font-bold bg-white border border-slate-200 text-navy-900 hover:bg-slate-50 shadow-xs transition-all"
          >
            <Download className="w-4 h-4" />
            <span>Download Findings CSV</span>
          </a>
        </GlassCard>
      </div>

      {/* Live Report Preview Snapshot */}
      <GlassCard title="Executive Report Content Summary" subtitle="Preview of live sections compiled into exported documents">
        <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-3 text-xs text-slate-700">
          <div className="font-bold text-navy-900 text-sm">
            SIGNALFIRE AI Executive Findings Preview
          </div>
          <p className="leading-relaxed">
            During the evaluated operational window ({recordsLoaded.toLocaleString()} records analyzed across 8 operational tables),
            the engine discovered a synchronized multi-dataset cascade centered in the <strong>North region</strong>.
            Delivery delays escalated by <strong>+325%</strong>, followed by a surge in customer complaints and refund requests,
            depleting inventory buffer and contracting repeat purchase retention. Unaffected cohorts (South, East, West)
            served as statistical control baselines.
          </p>

          <div className="pt-2 border-t border-slate-200 grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px]">
            <div>Total Findings: <strong>{findings.length}</strong></div>
            <div>Critical Severity: <strong>{findings.filter(f => f.severity === 'CRITICAL').length}</strong></div>
            <div>Risk Clusters: <strong>{clusters.length}</strong></div>
            <div>Analytical Backend: <strong>{backendName}</strong></div>
          </div>
        </div>
      </GlassCard>
    </div>
  );
};
