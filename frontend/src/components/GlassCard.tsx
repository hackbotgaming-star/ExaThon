import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
  badge?: React.ReactNode;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = "",
  title,
  subtitle,
  action,
  badge
}) => {
  return (
    <div className={`glass-card rounded-2xl p-5 ${className}`}>
      {(title || action || badge) && (
        <div className="flex items-start justify-between mb-4 border-b border-slate-100 pb-3">
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-sm font-bold text-navy-900 tracking-tight">{title}</h3>
              {badge}
            </div>
            {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
          </div>
          {action && <div className="shrink-0">{action}</div>}
        </div>
      )}
      {children}
    </div>
  );
};
