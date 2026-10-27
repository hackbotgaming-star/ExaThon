import React, { useState, useEffect } from 'react';
import { Sliders, Calculator, TrendingUp, AlertTriangle, Info, RefreshCw, Cpu, ShoppingBag } from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { WhatIfResponse } from '../types';
import { calculateWhatIf } from '../services/api';

export const WhatIfAnalysis: React.FC = () => {
  const [selectedDomain, setSelectedDomain] = useState<'retail' | 'mro'>('retail');

  // Retail scenario parameters
  const [delayDelta, setDelayDelta] = useState<number>(20);
  const [refundDelta, setRefundDelta] = useState<number>(2.0);
  const [demandDelta, setDemandDelta] = useState<number>(15);
  const [inventoryReduction, setInventoryReduction] = useState<number>(10);

  // MRO scenario parameters
  const [vibrationDelta, setVibrationDelta] = useState<number>(35);
  const [pmBacklogDelta, setPmBacklogDelta] = useState<number>(25);
  const [leadTimeDelta, setLeadTimeDelta] = useState<number>(5);
  const [hourlyCost, setHourlyCost] = useState<number>(6500);

  const [result, setResult] = useState<WhatIfResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    runSimulation();
  }, [
    selectedDomain,
    delayDelta,
    refundDelta,
    demandDelta,
    inventoryReduction,
    vibrationDelta,
    pmBacklogDelta,
    leadTimeDelta,
    hourlyCost
  ]);

  const runSimulation = async () => {
    setIsLoading(true);
    try {
      if (selectedDomain === 'retail') {
        const res = await calculateWhatIf({
          domain: 'retail',
          delivery_delay_delta_pct: delayDelta,
          refund_rate_delta_pct: refundDelta,
          demand_delta_pct: demandDelta,
          inventory_reduction_pct: inventoryReduction
        });
        setResult(res);
      } else {
        const res = await calculateWhatIf({
          domain: 'mro',
          vibration_delta_pct: vibrationDelta,
          pm_backlog_delta_pct: pmBacklogDelta,
          parts_lead_time_days_delta: leadTimeDelta,
          hourly_downtime_cost: hourlyCost
        });
        setResult(res);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    if (selectedDomain === 'retail') {
      setDelayDelta(0);
      setRefundDelta(0);
      setDemandDelta(0);
      setInventoryReduction(0);
    } else {
      setVibrationDelta(0);
      setPmBacklogDelta(0);
      setLeadTimeDelta(0);
      setHourlyCost(6500);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
            What-If Operational Scenario Analysis
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Stress-test operational dynamics under multi-variable shifts. Clearly separates deterministic arithmetic from empirical model projections.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          {/* Domain Toggle Tabs */}
          <div className="inline-flex rounded-lg p-1 bg-slate-100 border border-slate-200 text-xs font-semibold">
            <button
              onClick={() => setSelectedDomain('retail')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md transition-all ${
                selectedDomain === 'retail'
                  ? 'bg-white text-navy-900 shadow-xs'
                  : 'text-slate-600 hover:text-navy-900'
              }`}
            >
              <ShoppingBag className="w-3.5 h-3.5 text-lavender-600" />
              <span>Retail Operations</span>
            </button>
            <button
              onClick={() => setSelectedDomain('mro')}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md transition-all ${
                selectedDomain === 'mro'
                  ? 'bg-white text-navy-900 shadow-xs'
                  : 'text-slate-600 hover:text-navy-900'
              }`}
            >
              <Cpu className="w-3.5 h-3.5 text-cyan-600" />
              <span>Industrial MRO</span>
            </button>
          </div>

          <button
            onClick={handleReset}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 shadow-xs transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Reset</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Interactive Scenario Sliders */}
        <div>
          {selectedDomain === 'retail' ? (
            <GlassCard title="Retail Operational Variables" subtitle="Adjust retail logistics and demand parameters">
              <div className="space-y-5 text-xs">
                {/* Slider 1: Delivery Delay */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-bold text-navy-900">Delivery Delay Shift</span>
                    <span className={`font-mono font-bold ${delayDelta > 0 ? 'text-red-600' : 'text-slate-600'}`}>
                      {delayDelta > 0 ? `+${delayDelta}%` : `${delayDelta}%`}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="-50"
                    max="150"
                    step="5"
                    value={delayDelta}
                    onChange={(e) => setDelayDelta(Number(e.target.value))}
                    className="w-full accent-lavender-600 cursor-pointer"
                  />
                  <span className="text-[10px] text-slate-400">Carrier transit duration alteration</span>
                </div>

                {/* Slider 2: Refund Rate Delta */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-bold text-navy-900">Refund Rate Delta</span>
                    <span className={`font-mono font-bold ${refundDelta > 0 ? 'text-red-600' : 'text-slate-600'}`}>
                      {refundDelta > 0 ? `+${refundDelta}%` : `${refundDelta}%`}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="-3.0"
                    max="10.0"
                    step="0.5"
                    value={refundDelta}
                    onChange={(e) => setRefundDelta(Number(e.target.value))}
                    className="w-full accent-lavender-600 cursor-pointer"
                  />
                  <span className="text-[10px] text-slate-400">Percentage-point shift in customer return rate</span>
                </div>

                {/* Slider 3: Demand Volume */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-bold text-navy-900">Sales Demand Shift</span>
                    <span className={`font-mono font-bold ${demandDelta > 0 ? 'text-emerald-600' : 'text-slate-600'}`}>
                      {demandDelta > 0 ? `+${demandDelta}%` : `${demandDelta}%`}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="-30"
                    max="50"
                    step="5"
                    value={demandDelta}
                    onChange={(e) => setDemandDelta(Number(e.target.value))}
                    className="w-full accent-lavender-600 cursor-pointer"
                  />
                  <span className="text-[10px] text-slate-400">Monthly gross order volume shift</span>
                </div>

                {/* Slider 4: Inventory Reduction */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-bold text-navy-900">Inventory Level Shift</span>
                    <span className={`font-mono font-bold ${inventoryReduction > 0 ? 'text-amber-600' : 'text-slate-600'}`}>
                      {inventoryReduction > 0 ? `-${inventoryReduction}%` : `${inventoryReduction}%`}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="60"
                    step="5"
                    value={inventoryReduction}
                    onChange={(e) => setInventoryReduction(Number(e.target.value))}
                    className="w-full accent-lavender-600 cursor-pointer"
                  />
                  <span className="text-[10px] text-slate-400">Fulfillment center buffer reduction</span>
                </div>
              </div>
            </GlassCard>
          ) : (
            <GlassCard title="MRO Equipment & Reliability Variables" subtitle="Adjust plant machinery telemetry and maintenance schedules">
              <div className="space-y-5 text-xs">
                {/* Slider 1: Vibration Velocity */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-bold text-navy-900">Machinery Vibration Shift</span>
                    <span className={`font-mono font-bold ${vibrationDelta > 0 ? 'text-red-600' : 'text-slate-600'}`}>
                      {vibrationDelta > 0 ? `+${vibrationDelta}%` : `${vibrationDelta}%`}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="-30"
                    max="120"
                    step="5"
                    value={vibrationDelta}
                    onChange={(e) => setVibrationDelta(Number(e.target.value))}
                    className="w-full accent-cyan-600 cursor-pointer"
                  />
                  <span className="text-[10px] text-slate-400">RMS vibration velocity deviation from baseline 2.8 mm/s</span>
                </div>

                {/* Slider 2: PM Work Order Backlog */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-bold text-navy-900">Preventive Maintenance Backlog</span>
                    <span className={`font-mono font-bold ${pmBacklogDelta > 0 ? 'text-red-600' : 'text-slate-600'}`}>
                      {pmBacklogDelta > 0 ? `+${pmBacklogDelta}%` : `${pmBacklogDelta}%`}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="-40"
                    max="100"
                    step="5"
                    value={pmBacklogDelta}
                    onChange={(e) => setPmBacklogDelta(Number(e.target.value))}
                    className="w-full accent-cyan-600 cursor-pointer"
                  />
                  <span className="text-[10px] text-slate-400">Overdue routine service orders awaiting technician dispatch</span>
                </div>

                {/* Slider 3: Spare Parts Lead Time */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-bold text-navy-900">Critical Parts Lead Time Delta</span>
                    <span className={`font-mono font-bold ${leadTimeDelta > 0 ? 'text-amber-600' : 'text-slate-600'}`}>
                      {leadTimeDelta > 0 ? `+${leadTimeDelta} days` : `${leadTimeDelta} days`}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="-5"
                    max="20"
                    step="1"
                    value={leadTimeDelta}
                    onChange={(e) => setLeadTimeDelta(Number(e.target.value))}
                    className="w-full accent-cyan-600 cursor-pointer"
                  />
                  <span className="text-[10px] text-slate-400">Supplier procurement delay for heavy machine components</span>
                </div>

                {/* Slider 4: Hourly Stoppage Cost */}
                <div>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="font-bold text-navy-900">Line Stoppage Cost Rate</span>
                    <span className="font-mono font-bold text-navy-900">
                      ${hourlyCost.toLocaleString()}/hr
                    </span>
                  </div>
                  <input
                    type="range"
                    min="2000"
                    max="15000"
                    step="500"
                    value={hourlyCost}
                    onChange={(e) => setHourlyCost(Number(e.target.value))}
                    className="w-full accent-cyan-600 cursor-pointer"
                  />
                  <span className="text-[10px] text-slate-400">Assumed downtime financial burden per facility hour</span>
                </div>
              </div>
            </GlassCard>
          )}
        </div>

        {/* Right Column: Comparative Analytical Consequences */}
        <div className="lg:col-span-2 space-y-4">
          {result && (
            <>
              {/* Baseline vs Simulated Metric Cards */}
              {selectedDomain === 'retail' && result.baseline.monthly_revenue !== undefined ? (
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-400">Monthly Revenue</span>
                    <div className="text-base font-extrabold text-navy-900 mt-1 font-mono">
                      ${result.simulated.monthly_revenue?.toLocaleString()}
                    </div>
                    <span className="text-[10px] text-slate-500">Base: ${result.baseline.monthly_revenue?.toLocaleString()}</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-400">Average Transit Delay</span>
                    <div className={`text-base font-extrabold mt-1 font-mono ${(result.simulated.avg_delivery_delay_days || 0) > (result.baseline.avg_delivery_delay_days || 0) ? 'text-red-600' : 'text-emerald-600'}`}>
                      {result.simulated.avg_delivery_delay_days} days
                    </div>
                    <span className="text-[10px] text-slate-500">Base: {result.baseline.avg_delivery_delay_days}d</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-400">Refund Cost</span>
                    <div className="text-base font-extrabold text-red-600 mt-1 font-mono">
                      ${result.simulated.monthly_refund_cost?.toLocaleString()}
                    </div>
                    <span className="text-[10px] text-slate-500">Base: ${result.baseline.monthly_refund_cost?.toLocaleString()}</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-400">Projected Complaints</span>
                    <div className="text-base font-extrabold text-navy-900 mt-1 font-mono">
                      {result.simulated.projected_complaint_count}
                    </div>
                    <span className="text-[10px] text-slate-500">Base: {result.baseline.monthly_complaint_count}</span>
                  </div>
                </div>
              ) : (
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-400">Downtime Hours</span>
                    <div className={`text-base font-extrabold mt-1 font-mono ${(result.simulated.monthly_downtime_hours || 0) > (result.baseline.monthly_downtime_hours || 0) ? 'text-red-600' : 'text-slate-900'}`}>
                      {result.simulated.monthly_downtime_hours} hrs
                    </div>
                    <span className="text-[10px] text-slate-500">Base: {result.baseline.monthly_downtime_hours}h</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-400">Downtime Loss</span>
                    <div className="text-base font-extrabold text-red-600 mt-1 font-mono">
                      ${result.simulated.monthly_downtime_loss_usd?.toLocaleString()}
                    </div>
                    <span className="text-[10px] text-slate-500">Base: ${result.baseline.monthly_downtime_loss_usd?.toLocaleString()}</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-400">PM Compliance</span>
                    <div className={`text-base font-extrabold mt-1 font-mono ${(result.simulated.pm_compliance_rate_pct || 0) < 80 ? 'text-amber-600' : 'text-emerald-600'}`}>
                      {result.simulated.pm_compliance_rate_pct}%
                    </div>
                    <span className="text-[10px] text-slate-500">Base: {result.baseline.pm_compliance_rate_pct}%</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                    <span className="text-[10px] uppercase font-bold text-slate-400">Seizure Failure Risk</span>
                    <div className={`text-base font-extrabold mt-1 font-mono ${(result.simulated.catastrophic_seizure_risk_pct || 0) > 40 ? 'text-red-600' : 'text-blue-600'}`}>
                      {result.simulated.catastrophic_seizure_risk_pct}%
                    </div>
                    <span className="text-[10px] text-slate-500">Weibull modeled</span>
                  </div>
                </div>
              )}

              {/* Direct Arithmetic vs Model-Based Projections */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <GlassCard
                  className="border-blue-200/80"
                  title="Direct Arithmetic Calculations"
                  subtitle="Deterministic consequences of parameter definitions"
                  badge={<Calculator className="w-4 h-4 text-blue-600" />}
                >
                  <ul className="space-y-2 text-xs text-slate-700">
                    {result.direct_arithmetic_consequences.map((c, idx) => (
                      <li key={idx} className="p-2.5 rounded-xl bg-blue-50/40 border border-blue-100/70 flex items-start space-x-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-500 mt-1.5 shrink-0" />
                        <span>{c}</span>
                      </li>
                    ))}
                  </ul>
                </GlassCard>

                <GlassCard
                  className="border-lavender-200/80"
                  title="Model-Based Behavioral Projections"
                  subtitle="Empirical elasticity estimates across response curves"
                  badge={<TrendingUp className="w-4 h-4 text-lavender-600" />}
                >
                  <ul className="space-y-2 text-xs text-slate-700">
                    {result.model_based_projections.map((p, idx) => (
                      <li key={idx} className="p-2.5 rounded-xl bg-lavender-50/40 border border-lavender-100/70 flex items-start space-x-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-lavender-500 mt-1.5 shrink-0" />
                        <span>{p}</span>
                      </li>
                    ))}
                  </ul>
                </GlassCard>
              </div>

              {/* Explicit Assumptions Callout */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 text-xs text-slate-600 space-y-1.5">
                <div className="flex items-center space-x-1.5 font-bold text-navy-900">
                  <Info className="w-4 h-4 text-slate-500" />
                  <span>Stated Assumptions &amp; Methodological Boundaries:</span>
                </div>
                <ul className="list-disc pl-5 space-y-1 text-[11px] text-slate-500">
                  {result.assumptions_and_limitations.map((a, idx) => (
                    <li key={idx}>{a}</li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
