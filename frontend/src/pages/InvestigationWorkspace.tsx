import React, { useState, useEffect } from 'react';
import {
  Briefcase,
  Save,
  CheckCircle2,
  Clock,
  AlertCircle,
  FileText,
  UserCheck,
  Tag,
  ShieldCheck
} from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { Finding, InvestigationRecord } from '../types';
import { fetchInvestigations, saveInvestigation } from '../services/api';

interface InvestigationWorkspaceProps {
  findings: Finding[];
  selectedFinding: Finding | null;
  onSelectFinding: (f: Finding) => void;
}

export const InvestigationWorkspace: React.FC<InvestigationWorkspaceProps> = ({
  findings,
  selectedFinding,
  onSelectFinding
}) => {
  const [investigations, setInvestigations] = useState<InvestigationRecord[]>([]);
  const activeFinding = selectedFinding || findings[0];

  const [status, setStatus] = useState<string>('Investigating');
  const [priority, setPriority] = useState<string>('P1');
  const [suspectedCause, setSuspectedCause] = useState<string>('');
  const [verifiedConclusion, setVerifiedConclusion] = useState<string>('');
  const [notes, setNotes] = useState<string>('');
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  useEffect(() => {
    loadInvestigations();
  }, []);

  useEffect(() => {
    if (activeFinding) {
      // Find matching existing investigation if any
      const existing = investigations.find(i => i.finding_id === activeFinding.finding_id);
      if (existing) {
        setStatus(existing.status);
        setPriority(existing.priority);
        setSuspectedCause(existing.suspected_cause || '');
        setVerifiedConclusion(existing.verified_conclusion || '');
        setNotes(existing.notes || '');
      } else {
        setStatus(activeFinding.status || 'Investigating');
        setPriority(activeFinding.priority || 'P1');
        setSuspectedCause(activeFinding.suggested_next_investigation || '');
        setVerifiedConclusion('');
        setNotes('');
      }
      setSaveMessage(null);
    }
  }, [activeFinding, investigations]);

  const loadInvestigations = async () => {
    try {
      const res = await fetchInvestigations();
      setInvestigations(res.investigations);
    } catch (e) {
      console.error(e);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeFinding) return;

    setIsSaving(true);
    setSaveMessage(null);
    try {
      await saveInvestigation({
        finding_id: activeFinding.finding_id,
        title: activeFinding.title,
        status,
        priority,
        suspected_cause: suspectedCause,
        verified_conclusion: verifiedConclusion,
        notes
      });
      setSaveMessage("Investigation record saved and persisted successfully.");
      await loadInvestigations();
    } catch (e: any) {
      setSaveMessage(`Error saving: ${e.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  if (!activeFinding) {
    return (
      <div className="p-8 text-center glass-card rounded-2xl">
        <Briefcase className="w-10 h-10 text-slate-300 mx-auto mb-2" />
        <h3 className="text-sm font-bold text-navy-900">No Findings Available</h3>
        <p className="text-xs text-slate-500 mt-1">Run anomaly detection to populate the investigation workspace.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
          Investigation Workspace &amp; Decision Support
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Record analytical findings, verify hypotheses, track remediation status, and maintain an audit trail.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Finding Selector List */}
        <div>
          <GlassCard title="Active Finding Stream" subtitle="Select a finding to record investigation outcomes">
            <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
              {findings.map((f) => {
                const isSelected = f.finding_id === activeFinding.finding_id;
                const invRecord = investigations.find(i => i.finding_id === f.finding_id);
                const currentStatus = invRecord ? invRecord.status : f.status;

                return (
                  <div
                    key={f.finding_id}
                    onClick={() => onSelectFinding(f)}
                    className={`p-3 rounded-xl border cursor-pointer transition-all ${
                      isSelected
                        ? 'border-lavender-500 bg-lavender-50/50 shadow-xs ring-1 ring-lavender-500'
                        : 'border-slate-200/80 bg-white hover:bg-slate-50/80'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono text-slate-400">{f.finding_id}</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        currentStatus === 'Confirmed' ? 'bg-emerald-100 text-emerald-800' :
                        currentStatus === 'Investigating' ? 'bg-amber-100 text-amber-800' :
                        'bg-slate-100 text-slate-600'
                      }`}>
                        {currentStatus}
                      </span>
                    </div>
                    <h4 className="text-xs font-bold text-navy-900 mt-1 line-clamp-1">{f.title}</h4>
                    <div className="flex items-center justify-between text-[11px] text-slate-500 mt-2">
                      <span>{f.affected_segment}</span>
                      <strong className="text-red-600 font-extrabold">
                        {f.change_magnitude_pct > 0 ? `+${f.change_magnitude_pct}%` : `${f.change_magnitude_pct}%`}
                      </strong>
                    </div>
                  </div>
                );
              })}
            </div>
          </GlassCard>
        </div>

        {/* Right Column: Active Investigation Record Editor */}
        <div className="lg:col-span-2">
          <GlassCard
            title={`Investigating: ${activeFinding.finding_id}`}
            subtitle={activeFinding.title}
            badge={
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full uppercase ${
                activeFinding.severity === 'CRITICAL' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-800'
              }`}>
                {activeFinding.severity}
              </span>
            }
          >
            <form onSubmit={handleSave} className="space-y-4 pt-2 text-xs">
              {/* Supporting Metrics Snapshot */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3 rounded-xl bg-slate-50 border border-slate-200">
                <div>
                  <span className="text-slate-400 uppercase font-bold text-[10px]">Observed</span>
                  <div className="text-sm font-extrabold text-navy-900">{activeFinding.observed_value}</div>
                </div>
                <div>
                  <span className="text-slate-400 uppercase font-bold text-[10px]">Baseline</span>
                  <div className="text-sm font-extrabold text-slate-600">{activeFinding.expected_value}</div>
                </div>
                <div>
                  <span className="text-slate-400 uppercase font-bold text-[10px]">Confidence</span>
                  <div className="text-sm font-extrabold text-emerald-600">{(activeFinding.confidence * 100).toFixed(0)}%</div>
                </div>
                <div>
                  <span className="text-slate-400 uppercase font-bold text-[10px]">Time Window</span>
                  <div className="text-[11px] font-medium text-slate-700 truncate">{activeFinding.relevant_time_window}</div>
                </div>
              </div>

              {/* Status & Priority Row */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="font-bold text-navy-900 block mb-1">Investigation Status</label>
                  <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                    className="w-full p-2 rounded-xl bg-white border border-slate-200 font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
                  >
                    <option value="New">New</option>
                    <option value="Investigating">Investigating</option>
                    <option value="Confirmed">Confirmed</option>
                    <option value="Dismissed">Dismissed</option>
                    <option value="Resolved">Resolved</option>
                  </select>
                </div>

                <div>
                  <label className="font-bold text-navy-900 block mb-1">Operational Priority</label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                    className="w-full p-2 rounded-xl bg-white border border-slate-200 font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
                  >
                    <option value="P1">P1 — Critical Operational Escalation</option>
                    <option value="P2">P2 — High Impact / Rapid Review</option>
                    <option value="P3">P3 — Moderate / Monitoring Only</option>
                  </select>
                </div>
              </div>

              {/* Suspected Cause */}
              <div>
                <label className="font-bold text-navy-900 block mb-1">Suspected Cause / Working Hypothesis</label>
                <textarea
                  rows={2}
                  value={suspectedCause}
                  onChange={(e) => setSuspectedCause(e.target.value)}
                  placeholder="e.g. Carrier SwiftFreight regional distribution hub hub-failure in North..."
                  className="w-full p-2.5 rounded-xl bg-white border border-slate-200 text-slate-700 focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
                />
              </div>

              {/* Verified Conclusion */}
              <div>
                <label className="font-bold text-navy-900 block mb-1">Verified Conclusion &amp; Root-Cause Audit</label>
                <textarea
                  rows={2}
                  value={verifiedConclusion}
                  onChange={(e) => setVerifiedConclusion(e.target.value)}
                  placeholder="Record empirical conclusion after cross-verifying with dispatch/carrier logs..."
                  className="w-full p-2.5 rounded-xl bg-white border border-slate-200 text-slate-700 focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
                />
              </div>

              {/* Follow-up Notes */}
              <div>
                <label className="font-bold text-navy-900 block mb-1">Follow-up Remediation Notes</label>
                <textarea
                  rows={3}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Next steps, tickets filed with logistics partners, SLA penalties, customer outreach..."
                  className="w-full p-2.5 rounded-xl bg-white border border-slate-200 text-slate-700 focus:outline-none focus:ring-2 focus:ring-lavender-500/20"
                />
              </div>

              {saveMessage && (
                <div className="p-3 rounded-xl bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center space-x-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{saveMessage}</span>
                </div>
              )}

              <div className="flex items-center justify-end space-x-3 pt-2">
                <button
                  type="submit"
                  disabled={isSaving}
                  className="flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-navy-900 text-white hover:bg-navy-800 shadow-sm transition-all disabled:opacity-40"
                >
                  <Save className="w-3.5 h-3.5" />
                  <span>{isSaving ? "Saving..." : "Save Investigation Record"}</span>
                </button>
              </div>
            </form>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};
