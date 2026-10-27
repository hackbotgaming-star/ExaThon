import React from 'react';
import {
  LayoutDashboard,
  Database,
  GitFork,
  Activity,
  Flame,
  Network,
  Briefcase,
  Sliders,
  Bot,
  CheckCircle2,
  FileDown,
  Settings,
  ShieldAlert
} from 'lucide-react';

export type NavTab =
  | 'overview'
  | 'explorer'
  | 'relationships'
  | 'signals'
  | 'cross-metric'
  | 'risk-map'
  | 'investigation'
  | 'what-if'
  | 'assistant'
  | 'evaluation'
  | 'reports'
  | 'settings';

interface SidebarProps {
  currentTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  criticalCount: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentTab, onSelectTab, criticalCount }) => {
  const navItems = [
    { id: 'overview' as NavTab, label: 'Overview Dashboard', icon: LayoutDashboard },
    { id: 'explorer' as NavTab, label: 'Data Explorer', icon: Database },
    { id: 'relationships' as NavTab, label: 'Relationships', icon: GitFork },
    { id: 'signals' as NavTab, label: 'Signal Detection', icon: Activity, badge: criticalCount > 0 ? criticalCount : undefined },
    { id: 'cross-metric' as NavTab, label: 'Cross-Metric Engine', icon: Flame, isDifferentiator: true },
    { id: 'risk-map' as NavTab, label: 'Interactive Risk Map', icon: Network },
    { id: 'investigation' as NavTab, label: 'Investigation Workspace', icon: Briefcase },
    { id: 'what-if' as NavTab, label: 'What-If Analysis', icon: Sliders },
    { id: 'assistant' as NavTab, label: 'AI Assistant', icon: Bot },
    { id: 'evaluation' as NavTab, label: 'Model Evaluation', icon: CheckCircle2 },
    { id: 'reports' as NavTab, label: 'Reports & Export', icon: FileDown },
    { id: 'settings' as NavTab, label: 'Settings & Exasol', icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-slate-200/80 bg-white/70 backdrop-blur-md flex flex-col justify-between p-4 shrink-0 select-none">
      <div className="space-y-1">
        <div className="px-3 py-2 text-[11px] font-semibold tracking-wider text-slate-400 uppercase">
          Analytical Modules
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentTab === item.id;

          return (
            <button
              key={item.id}
              onClick={() => onSelectTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all group ${
                isActive
                  ? 'bg-lavender-50 text-lavender-700 font-semibold shadow-xs border border-lavender-200/80'
                  : 'text-slate-600 hover:text-navy-900 hover:bg-slate-100/70 border border-transparent'
              }`}
            >
              <div className="flex items-center space-x-2.5">
                <Icon
                  className={`w-4 h-4 transition-colors ${
                    isActive
                      ? 'text-lavender-600'
                      : 'text-slate-400 group-hover:text-slate-600'
                  }`}
                />
                <span>{item.label}</span>
              </div>

              {item.isDifferentiator && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-amber-100 text-amber-800 border border-amber-200/60">
                  CORE
                </span>
              )}

              {item.badge !== undefined && (
                <span className="text-[10px] font-bold px-1.5 py-0.2 rounded-full bg-red-100 text-red-700 border border-red-200">
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Safety & Causation Principle Note */}
      <div className="p-3 rounded-xl bg-slate-50 border border-slate-200/60 text-[11px] text-slate-500 leading-relaxed">
        <div className="flex items-center space-x-1.5 text-navy-900 font-semibold mb-1">
          <ShieldAlert className="w-3.5 h-3.5 text-amber-500" />
          <span>Core Principle</span>
        </div>
        SIGNALFIRE AI separates observed facts, statistical associations, and hypotheses. Correlation is never presented as causation.
      </div>
    </aside>
  );
};
