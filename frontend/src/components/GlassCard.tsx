import React, { useRef, useState } from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
  badge?: React.ReactNode;
  tilt3D?: boolean;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = "",
  title,
  subtitle,
  action,
  badge,
  tilt3D = true
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const [tiltStyle, setTiltStyle] = useState<React.CSSProperties>({});
  const [glareStyle, setGlareStyle] = useState<React.CSSProperties>({ opacity: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!tilt3D || !cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = -((y - centerY) / centerY) * 6; // max 6 deg
    const rotateY = ((x - centerX) / centerX) * 6;

    const glareX = (x / rect.width) * 100;
    const glareY = (y / rect.height) * 100;

    setTiltStyle({
      transform: `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-2px)`,
      transition: 'transform 0.12s ease-out'
    });

    setGlareStyle({
      opacity: 0.35,
      background: `radial-gradient(circle 320px at ${glareX}% ${glareY}%, rgba(255, 255, 255, 0.75) 0%, rgba(224, 231, 255, 0.2) 50%, transparent 80%)`,
      transition: 'opacity 0.2s ease'
    });
  };

  const handleMouseLeave = () => {
    if (!tilt3D) return;
    setTiltStyle({
      transform: 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0px)',
      transition: 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)'
    });
    setGlareStyle({
      opacity: 0,
      transition: 'opacity 0.35s ease'
    });
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        ...tiltStyle,
        transformStyle: 'preserve-3d'
      }}
      className={`glass-card rounded-2xl p-5 relative overflow-hidden ${className}`}
    >
      {/* Dynamic 3D Holographic Glare Overlay */}
      {tilt3D && (
        <div
          className="pointer-events-none absolute inset-0 rounded-2xl z-20"
          style={{
            ...glareStyle,
            mixBlendMode: 'overlay'
          }}
        />
      )}

      {/* Card Content */}
      <div className="relative z-10" style={{ transformStyle: 'preserve-3d' }}>
        {(title || action || badge) && (
          <div className="flex items-start justify-between mb-4 border-b border-slate-100 pb-3" style={{ transform: 'translateZ(8px)' }}>
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
        <div style={{ transform: 'translateZ(12px)' }}>
          {children}
        </div>
      </div>
    </div>
  );
};
