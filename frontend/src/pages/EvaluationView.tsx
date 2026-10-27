import React, { useState, useEffect } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  Layers,
  ShieldCheck,
  TrendingUp,
  Cpu,
  RefreshCw,
  Info
} from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { EvaluationResult } from '../types';
import { fetchEvaluation } from '../services/api';

export const EvaluationView: React.FC = () => {
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    loadEvaluation();
  }, []);

  const loadEvaluation = async () => {
    setIsLoading(true);
    try {
      const res = await fetchEvaluation();
      setEvaluation(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
            Empirical Anomaly Detection Evaluation
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Rigorous evaluation of SignalFire against a Simple Percent-Change Baseline Detector using known synthetic ground truth.
          </p>
        </div>

        <button
          onClick={loadEvaluation}
          disabled={isLoading}
          className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-navy-900 text-white hover:bg-navy-800 shadow-sm transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
          <span>{isLoading ? 'Running Evaluation...' : 'Re-run Evaluation'}</span>
        </button>
      </div>

      {evaluation && (
        <>
          {/* Comparative Model Performance Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Model A: SignalFire Robust Multi-Metric Detector */}
            <GlassCard
              className="border-indigo-200/90 bg-gradient-to-br from-white via-lavender-50/20 to-white ring-1 ring-lavender-200"
              title="SignalFire Multi-Metric Detector"
              subtitle="Robust Z-Score (MAD), IQR fences, and rolling window normalization"
              badge={
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                  RECOMMENDED
                </span>
              }
            >
              <div className="grid grid-cols-3 gap-3 pt-2 text-center">
                <div className="p-3 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Precision</span>
                  <div className="text-xl font-extrabold text-navy-900 mt-0.5 font-mono">
                    {(evaluation.signalfire_model.precision * 100).toFixed(1)}%
                  </div>
                  <span className="text-[10px] text-slate-400">TP / (TP + FP)</span>
                </div>

                <div className="p-3 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Recall</span>
                  <div className="text-xl font-extrabold text-emerald-600 mt-0.5 font-mono">
                    {(evaluation.signalfire_model.recall * 100).toFixed(1)}%
                  </div>
                  <span className="text-[10px] text-slate-400">TP / Total Ground Truth</span>
                </div>

                <div className="p-3 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">F1-Score</span>
                  <div className="text-xl font-extrabold text-lavender-700 mt-0.5 font-mono">
                    {evaluation.signalfire_model.f1_score.toFixed(3)}
                  </div>
                  <span className="text-[10px] text-slate-400">Harmonic Mean</span>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-3 text-xs text-slate-600">
                <div>True Positives: <strong className="text-navy-900 font-mono">{evaluation.signalfire_model.true_positives}</strong></div>
                <div>False Positives: <strong className="text-emerald-600 font-mono">{evaluation.signalfire_model.false_positives}</strong></div>
                <div>False Negatives: <strong className="text-slate-700 font-mono">{evaluation.signalfire_model.false_negatives}</strong></div>
              </div>
            </GlassCard>

            {/* Model B: Baseline Static Detector */}
            <GlassCard
              className="border-slate-200/90 bg-slate-50/50"
              title="Baseline Detector (Simple % Threshold)"
              subtitle="Fixed >30% change threshold without noise filtering or MAD"
              badge={
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-200 text-slate-700">
                  STANDARD BASELINE
                </span>
              }
            >
              <div className="grid grid-cols-3 gap-3 pt-2 text-center">
                <div className="p-3 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Precision</span>
                  <div className="text-xl font-extrabold text-navy-900 mt-0.5 font-mono">
                    {(evaluation.baseline_model.precision * 100).toFixed(1)}%
                  </div>
                  <span className="text-[10px] text-slate-400">High false alarm rate</span>
                </div>

                <div className="p-3 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Recall</span>
                  <div className="text-xl font-extrabold text-slate-700 mt-0.5 font-mono">
                    {(evaluation.baseline_model.recall * 100).toFixed(1)}%
                  </div>
                  <span className="text-[10px] text-slate-400">High sensitivity</span>
                </div>

                <div className="p-3 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">F1-Score</span>
                  <div className="text-xl font-extrabold text-slate-600 mt-0.5 font-mono">
                    {evaluation.baseline_model.f1_score.toFixed(3)}
                  </div>
                  <span className="text-[10px] text-slate-400">Compromised by noise</span>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-200 grid grid-cols-3 text-xs text-slate-600">
                <div>True Positives: <strong className="text-navy-900 font-mono">{evaluation.baseline_model.true_positives}</strong></div>
                <div>False Positives: <strong className="text-red-600 font-mono">{evaluation.baseline_model.false_positives}</strong></div>
                <div>False Negatives: <strong className="text-slate-700 font-mono">{evaluation.baseline_model.false_negatives}</strong></div>
              </div>
            </GlassCard>
          </div>

          {/* Analytical Findings Evaluation Notes */}
          <GlassCard title="Methodological Findings &amp; Takeaways">
            <p className="text-xs text-slate-700 leading-relaxed">
              {evaluation.evaluation_notes}
            </p>

            <div className="mt-4 p-4 rounded-xl bg-amber-50/70 border border-amber-200/70 text-xs text-amber-900 space-y-1">
              <div className="font-bold flex items-center space-x-1.5">
                <Info className="w-4 h-4 text-amber-700" />
                <span>Evaluation Caveats &amp; Synthetic Data Boundaries</span>
              </div>
              <ul className="list-disc pl-5 text-[11px] text-slate-600 space-y-1 pt-1">
                {evaluation.limitations.map((lim, idx) => (
                  <li key={idx}>{lim}</li>
                ))}
              </ul>
            </div>
          </GlassCard>
        </>
      )}
    </div>
  );
};
