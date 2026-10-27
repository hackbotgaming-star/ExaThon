import React, { useState, useEffect } from 'react';
import { GitFork, Link2, ShieldCheck, AlertCircle, ArrowRight, Layers } from 'lucide-react';
import { GlassCard } from '../components/GlassCard';
import { fetchRelationships } from '../services/api';

export const RelationshipsExplorer: React.FC = () => {
  const [relationships, setRelationships] = useState<any[]>([]);

  useEffect(() => {
    fetchRelationships().then(res => setRelationships(res.relationships)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-extrabold text-navy-900 tracking-tight">
          Dataset Relationship Explorer
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Map relational joins, common dimensions, and candidate temporal associations across operational datasets.
        </p>
      </div>

      {/* Methodological Guidance Note */}
      <div className="p-4 rounded-2xl bg-lavender-50/70 border border-lavender-200/80 text-xs text-lavender-900 flex items-start space-x-3">
        <GitFork className="w-5 h-5 text-lavender-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <span className="font-bold">Candidate vs Verified Relationships</span>
          <p className="text-slate-600 leading-relaxed">
            Columns sharing identical nomenclature are not automatically presumed to share identical semantics. Foreign key relationships are strictly verified against transactional primary keys, while geographic and temporal dimensions are marked as candidate associations for analyst inspection.
          </p>
        </div>
      </div>

      {/* Relationships Table */}
      <GlassCard title="Discovered Data Model Linkages" subtitle="Validated relational schemas and candidate multi-dataset dimensions">
        <div className="overflow-x-auto border border-slate-200/80 rounded-xl">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-navy-900 border-b border-slate-200 font-bold uppercase text-[10px]">
              <tr>
                <th className="px-4 py-3">Source Table &amp; Key</th>
                <th className="px-4 py-3">Link Type</th>
                <th className="px-4 py-3">Target Table &amp; Key</th>
                <th className="px-4 py-3">Relationship Status</th>
                <th className="px-4 py-3">Investigation Utility</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white">
              {relationships.map((rel, idx) => (
                <tr key={idx} className="hover:bg-slate-50/70 transition-colors">
                  <td className="px-4 py-3">
                    <span className="font-bold text-navy-900">{rel.source_table}</span>
                    <span className="text-slate-400">.</span>
                    <code className="text-lavender-700 bg-lavender-50 px-1.5 py-0.5 rounded text-[11px] font-mono">
                      {rel.source_col}
                    </code>
                  </td>
                  <td className="px-4 py-3 text-slate-600">
                    <div className="flex items-center space-x-1.5 text-[11px]">
                      <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
                      <span>{rel.type}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <span className="font-bold text-navy-900">{rel.target_table}</span>
                    <span className="text-slate-400">.</span>
                    <code className="text-lavender-700 bg-lavender-50 px-1.5 py-0.5 rounded text-[11px] font-mono">
                      {rel.target_col}
                    </code>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                      rel.status === 'Verified'
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                        : 'bg-amber-100 text-amber-800 border border-amber-200'
                    }`}>
                      {rel.status === 'Verified' ? <ShieldCheck className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
                      <span>{rel.status}</span>
                    </span>
                  </td>
                  <td className="px-4 py-3 text-slate-500 text-[11px]">
                    {rel.type.includes('Foreign') ? 'Direct entity join' : 'Cohort rollup alignment'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>

      {/* Visual Dimension Alignment Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <GlassCard className="p-4" title="1. Temporal Alignment" subtitle="Daily & weekly aggregation">
          <p className="text-xs text-slate-600 mt-2">
            Dispatches, complaints, and returns are synchronized onto a standard 24-hour UTC calendar date index to uncover lead-lag dynamics.
          </p>
        </GlassCard>
        <GlassCard className="p-4" title="2. Regional Segmentation" subtitle="4 geographical cohorts">
          <p className="text-xs text-slate-600 mt-2">
            Records are mapped to <code>North</code>, <code>South</code>, <code>East</code>, and <code>West</code> to contrast localized shocks against unaffected cohorts.
          </p>
        </GlassCard>
        <GlassCard className="p-4" title="3. Product Taxonomy" subtitle="4 SKU categories">
          <p className="text-xs text-slate-600 mt-2">
            Inventory stock levels and sales lines link across <code>Electronics</code>, <code>Apparel</code>, <code>Home & Garden</code>, and <code>Pantry</code>.
          </p>
        </GlassCard>
      </div>
    </div>
  );
};
