import React, { useState } from 'react';
import {
  Settings,
  Server,
  Database,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  ShieldAlert,
  Info,
  Sliders,
  ExternalLink
} from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { HealthStatus } from '../types';
import { connectDatabase, resetSampleData } from '../services/api';

interface SettingsViewProps {
  health: HealthStatus | null;
  onRefreshHealth: () => void;
}

export const SettingsView: React.FC<SettingsViewProps> = ({ health, onRefreshHealth }) => {
  const isExasol = health?.database?.is_exasol_active ?? false;
  const backendName = health?.database?.active_backend_name || "DuckDB Local";

  const [dsn, setDsn] = useState<string>("localhost:8563");
  const [user, setUser] = useState<string>("sys");
  const [password, setPassword] = useState<string>("");
  const [schema, setSchema] = useState<string>("SIGNALFIRE");
  const [isConnecting, setIsConnecting] = useState<boolean>(false);
  const [connectMessage, setConnectMessage] = useState<{ success: boolean; text: string } | null>(null);

  const [isResetting, setIsResetting] = useState<boolean>(false);

  const handleConnectExasol = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsConnecting(true);
    setConnectMessage(null);
    try {
      const res = await connectDatabase({
        mode: "EXASOL",
        dsn,
        user,
        password,
        schema_name: schema,
        timeout: 5
      });
      if (res.success) {
        setConnectMessage({ success: true, text: res.message });
      } else {
        setConnectMessage({ success: false, text: res.message });
      }
      onRefreshHealth();
    } catch (err: any) {
      setConnectMessage({ success: false, text: `Connection failure: ${err.message}` });
    } finally {
      setIsConnecting(false);
    }
  };

  const handleSwitchDuckDB = async () => {
    setIsConnecting(true);
    setConnectMessage(null);
    try {
      const res = await connectDatabase({ mode: "DUCKDB" });
      setConnectMessage({ success: true, text: res.message });
      onRefreshHealth();
    } catch (err: any) {
      setConnectMessage({ success: false, text: `Switch error: ${err.message}` });
    } finally {
      setIsConnecting(false);
    }
  };

  const handleResetDatasets = async () => {
    if (!window.confirm("Reload and re-index all synthetic retail tables?")) return;
    setIsResetting(true);
    try {
      await resetSampleData();
      alert("Sample retail datasets re-indexed into active analytical storage.");
      onRefreshHealth();
    } catch (e: any) {
      alert(`Reset failed: ${e.message}`);
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
          System Settings &amp; Exasol Configuration
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Manage analytical database engines, configure Exasol Personal connectivity, and calibrate anomaly detection parameters.
        </p>
      </div>

      {/* Backend Status Transparency Card */}
      <GlassCard
        className={isExasol ? "border-purple-200/90 bg-purple-50/20" : "border-ice-200/90 bg-ice-50/20"}
        title="Active Analytical Database Backend"
        subtitle="Transparent indication of the live execution engine"
        badge={
          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
            isExasol ? 'bg-purple-100 text-purple-800' : 'bg-ice-100 text-ice-800'
          }`}>
            {isExasol ? 'EXASOL PERSONAL' : 'DUCKDB LOCAL (DEMO / FALLBACK)'}
          </span>
        }
      >
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-1 text-xs">
          <div className="space-y-1">
            <div className="text-sm font-bold text-navy-900 flex items-center space-x-2">
              <Server className="w-4 h-4 text-lavender-600" />
              <span>{backendName}</span>
            </div>
            <p className="text-slate-600 max-w-xl">
              {isExasol
                ? "Analytical queries, aggregation routines, and cross-dataset metrics are being computed directly on Exasol Personal using pyexasol."
                : "Exasol Personal is currently offline or unconfigured. Queries are safely executing against DuckDB in-process OLAP database for full demo functionality."}
            </p>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            {isExasol ? (
              <button
                onClick={handleSwitchDuckDB}
                className="px-3 py-1.5 rounded-xl text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-xs transition-colors"
              >
                Switch to DuckDB Local
              </button>
            ) : (
              <span className="text-[11px] font-semibold text-slate-500">
                Local Fallback Active
              </span>
            )}
          </div>
        </div>
      </GlassCard>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Exasol Connection Form */}
        <GlassCard
          title="Connect Exasol Personal"
          subtitle="Configure credentials for high-performance in-memory analytics"
        >
          <form onSubmit={handleConnectExasol} className="space-y-3.5 text-xs">
            <div>
              <label className="font-bold text-navy-900 block mb-1">Exasol DSN (Host:Port)</label>
              <input
                type="text"
                value={dsn}
                onChange={(e) => setDsn(e.target.value)}
                placeholder="localhost:8563 or 127.0.0.1:8563"
                className="w-full p-2.5 rounded-xl bg-slate-50 border border-slate-200 font-mono text-[11px] focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="font-bold text-navy-900 block mb-1">Database Username</label>
                <input
                  type="text"
                  value={user}
                  onChange={(e) => setUser(e.target.value)}
                  placeholder="sys"
                  className="w-full p-2.5 rounded-xl bg-slate-50 border border-slate-200 font-mono text-[11px] focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
                />
              </div>

              <div>
                <label className="font-bold text-navy-900 block mb-1">Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full p-2.5 rounded-xl bg-slate-50 border border-slate-200 font-mono text-[11px] focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
                />
              </div>
            </div>

            <div>
              <label className="font-bold text-navy-900 block mb-1">Target Schema</label>
              <input
                type="text"
                value={schema}
                onChange={(e) => setSchema(e.target.value)}
                placeholder="SIGNALFIRE"
                className="w-full p-2.5 rounded-xl bg-slate-50 border border-slate-200 font-mono text-[11px] focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
              />
            </div>

            {connectMessage && (
              <div className={`p-3 rounded-xl flex items-start space-x-2 ${
                connectMessage.success
                  ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                  : 'bg-red-50 text-red-800 border border-red-200'
              }`}>
                {connectMessage.success ? <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" /> : <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />}
                <span className="leading-tight">{connectMessage.text}</span>
              </div>
            )}

            <div className="flex items-center justify-between pt-2">
              <span className="text-[10px] text-slate-400">
                Uses official <code>pyexasol</code> driver over WebSocket JSON-RPC.
              </span>
              <button
                type="submit"
                disabled={isConnecting}
                className="px-4 py-2 rounded-xl text-xs font-bold bg-navy-900 text-white hover:bg-navy-800 shadow-sm transition-all disabled:opacity-40"
              >
                {isConnecting ? "Testing Connection..." : "Test & Connect Exasol"}
              </button>
            </div>
          </form>
        </GlassCard>

        {/* Exasol Setup Quick Guide */}
        <GlassCard
          title="Exasol Personal Setup Guide"
          subtitle="How to run Exasol Personal locally via Docker"
        >
          <div className="space-y-3 text-xs text-slate-700">
            <p>
              To run an official Exasol Personal instance for testing high-throughput SQL analytics:
            </p>
            <div className="p-3 rounded-xl bg-navy-900 text-slate-200 font-mono text-[11px] overflow-x-auto">
              <code>docker run --name exasol-test -p 8563:8563 -d exasol/docker-db:latest</code>
            </div>
            <ul className="space-y-1.5 text-slate-600 text-[11px]">
              <li>• Default Port: <code>8563</code></li>
              <li>• Default User: <code>sys</code></li>
              <li>• Default Password: <code>exasol</code></li>
              <li>• Target Schema: <code>SIGNALFIRE</code> (auto-created on connect)</li>
            </ul>
            <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-600 text-[11px]">
              <strong>Local Development Mode:</strong> When Exasol is not running, SIGNALFIRE AI seamlessly executes all analytics on DuckDB with zero feature degradation.
            </div>
          </div>
        </GlassCard>
      </div>

      {/* Dataset Maintenance & Threshold Calibration */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard title="Sample Dataset Maintenance" subtitle="Reload synthetic retail operations data">
          <div className="space-y-3 text-xs text-slate-600">
            <p>
              Reloads the 8 baseline tables (sales, orders, deliveries, complaints, refunds, inventory, suppliers, customer retention)
              along with the multi-stage injected anomaly scenario.
            </p>
            <button
              onClick={handleResetDatasets}
              disabled={isResetting}
              className="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-white border border-slate-200 text-navy-900 hover:bg-slate-50 shadow-xs transition-all disabled:opacity-40"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isResetting ? 'animate-spin' : ''}`} />
              <span>{isResetting ? "Re-indexing..." : "Reset All Sample Datasets"}</span>
            </button>
          </div>
        </GlassCard>

        <GlassCard title="Detection Sensitivity Thresholds" subtitle="Calibrated parameters for outlier detection">
          <div className="space-y-2 text-xs text-slate-700">
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="font-semibold text-slate-600">Robust Z-Score Threshold:</span>
              <strong className="font-mono text-navy-900">2.50 (MAD normalized)</strong>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="font-semibold text-slate-600">Interquartile Range Factor:</span>
              <strong className="font-mono text-navy-900">1.75 × IQR</strong>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-100">
              <span className="font-semibold text-slate-600">Minimum Lead-Lag Window:</span>
              <strong className="font-mono text-navy-900">3 Days</strong>
            </div>
            <div className="flex justify-between py-1.5">
              <span className="font-semibold text-slate-600">Cross-Metric Correlation Threshold:</span>
              <strong className="font-mono text-navy-900">r &ge; 0.75 (p &lt; 0.01)</strong>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};
