import React, { useRef, useEffect, useState } from 'react';
import { Rotate3d, Play, Pause, ZoomIn, Eye } from 'lucide-react';

interface Node3D {
  id: string;
  label: string;
  sublabel: string;
  x: number;
  y: number;
  z: number;
  baseRadius: number;
  color: string;
  glowColor: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'HEALTHY';
  metric: string;
}

interface Edge3D {
  source: string;
  target: string;
  color: string;
  dashed?: boolean;
}

export const Interactive3DRiskCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // 3D camera angles in radians
  const rotX = useRef<number>(0.25);
  const rotY = useRef<number>(0.4);
  const isDragging = useRef<boolean>(false);
  const lastMousePos = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const isAutoRotate = useRef<boolean>(true);
  const [autoRotateState, setAutoRotateState] = useState<boolean>(true);
  const [hoveredNode, setHoveredNode] = useState<Node3D | null>(null);

  // Operational 3D topology nodes
  const nodes: Node3D[] = [
    {
      id: 'north_logistics',
      label: 'North Distribution Hub',
      sublabel: 'Carrier Transit Failure (+2568%)',
      x: -160,
      y: -90,
      z: 70,
      baseRadius: 18,
      color: '#ef4444',
      glowColor: 'rgba(239, 68, 68, 0.45)',
      severity: 'CRITICAL',
      metric: 'Transit Delay: 2.78d (Z=56.4)'
    },
    {
      id: 'plant_alpha',
      label: 'Plant Alpha (Detroit)',
      sublabel: 'Vibration & Seizure Drift (8.4 mm/s)',
      x: 170,
      y: -110,
      z: -40,
      baseRadius: 17,
      color: '#ef4444',
      glowColor: 'rgba(239, 68, 68, 0.45)',
      severity: 'CRITICAL',
      metric: 'Stoppage Loss: $280,000'
    },
    {
      id: 'complaints_cluster',
      label: 'Customer Escalations',
      sublabel: 'Delayed Delivery Influx (+961%)',
      x: -70,
      y: 80,
      z: 140,
      baseRadius: 14,
      color: '#f59e0b',
      glowColor: 'rgba(245, 158, 11, 0.4)',
      severity: 'HIGH',
      metric: 'Volume: 12.8 / day'
    },
    {
      id: 'refunds_cluster',
      label: 'Refund Claims Center',
      sublabel: 'Elevated North Returns (+276%)',
      x: -150,
      y: 130,
      z: -30,
      baseRadius: 13,
      color: '#f59e0b',
      glowColor: 'rgba(245, 158, 11, 0.4)',
      severity: 'HIGH',
      metric: 'Disbursements: $14,200'
    },
    {
      id: 'bearing_depot',
      label: 'Precision Bearings Store',
      sublabel: 'Stock Exhaustion (0 units)',
      x: 120,
      y: 60,
      z: 110,
      baseRadius: 12,
      color: '#0284c7',
      glowColor: 'rgba(2, 132, 199, 0.35)',
      severity: 'MEDIUM',
      metric: 'Stockout Duration: 18 days'
    },
    {
      id: 'south_cohort',
      label: 'South Region (Control)',
      sublabel: 'Normal Logistics Flow',
      x: -60,
      y: -140,
      z: -120,
      baseRadius: 10,
      color: '#10b981',
      glowColor: 'rgba(16, 185, 129, 0.25)',
      severity: 'HEALTHY',
      metric: 'Delay: 0.12 days (Stable)'
    },
    {
      id: 'plant_beta',
      label: 'Plant Beta (Control)',
      sublabel: 'Telemetry Baseline',
      x: 80,
      y: -50,
      z: -150,
      baseRadius: 10,
      color: '#10b981',
      glowColor: 'rgba(16, 185, 129, 0.25)',
      severity: 'HEALTHY',
      metric: 'Vibration: 2.1 mm/s'
    }
  ];

  const edges: Edge3D[] = [
    { source: 'north_logistics', target: 'complaints_cluster', color: '#f87171' },
    { source: 'complaints_cluster', target: 'refunds_cluster', color: '#fbbf24' },
    { source: 'plant_alpha', target: 'bearing_depot', color: '#f87171' },
    { source: 'south_cohort', target: 'north_logistics', color: '#cbd5e1', dashed: true },
    { source: 'plant_beta', target: 'plant_alpha', color: '#cbd5e1', dashed: true }
  ];

  // 3D Particle dust
  const particles = useRef<Array<{ x: number; y: number; z: number; size: number }>>(
    Array.from({ length: 45 }, () => ({
      x: (Math.random() - 0.5) * 500,
      y: (Math.random() - 0.5) * 350,
      z: (Math.random() - 0.5) * 500,
      size: Math.random() * 2 + 1
    }))
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let pulseAngle = 0;

    const render = () => {
      if (isAutoRotate.current && !isDragging.current) {
        rotY.current += 0.005;
      }
      pulseAngle += 0.04;

      const width = canvas.width;
      const height = canvas.height;
      const centerX = width / 2;
      const centerY = height / 2;
      const focalLength = 480;

      ctx.clearRect(0, 0, width, height);

      // Coordinate transformation function
      const project = (x: number, y: number, z: number) => {
        // Rotate around Y-axis
        const cosY = Math.cos(rotY.current);
        const sinY = Math.sin(rotY.current);
        const x1 = x * cosY + z * sinY;
        const z1 = -x * sinY + z * cosY;

        // Rotate around X-axis
        const cosX = Math.cos(rotX.current);
        const sinX = Math.sin(rotX.current);
        const y2 = y * cosX - z1 * sinX;
        const z2 = y * sinX + z1 * cosX;

        const distance = focalLength + z2;
        const scale = distance > 10 ? focalLength / distance : 0.001;

        return {
          px: centerX + x1 * scale,
          py: centerY + y2 * scale,
          scale,
          z: z2
        };
      };

      // 1. Draw 3D Floating Particle Dust
      ctx.fillStyle = 'rgba(196, 181, 253, 0.4)';
      particles.current.forEach((p) => {
        const pr = project(p.x, p.y, p.z);
        if (pr.scale > 0) {
          ctx.beginPath();
          ctx.arc(pr.px, pr.py, p.size * pr.scale, 0, Math.PI * 2);
          ctx.fill();
        }
      });

      // 2. Project Nodes
      const projectedNodes = nodes.map((n) => {
        const pr = project(n.x, n.y, n.z);
        return { ...n, ...pr };
      });

      // Sort by Z (painter's algorithm: draw farthest objects first)
      projectedNodes.sort((a, b) => a.z - b.z);

      // Node lookup map
      const nodeMap = new Map<string, (typeof projectedNodes)[0]>();
      projectedNodes.forEach((pn) => nodeMap.set(pn.id, pn));

      // 3. Draw 3D Connecting Edges
      edges.forEach((edge) => {
        const source = nodeMap.get(edge.source);
        const target = nodeMap.get(edge.target);
        if (!source || !target || source.scale <= 0 || target.scale <= 0) return;

        ctx.save();
        ctx.beginPath();
        if (edge.dashed) {
          ctx.setLineDash([4, 4]);
        }
        ctx.strokeStyle = edge.color;
        ctx.lineWidth = Math.max(1, 2 * ((source.scale + target.scale) / 2));
        ctx.globalAlpha = Math.min(0.8, Math.max(0.15, (source.scale + target.scale) / 2));
        ctx.moveTo(source.px, source.py);
        ctx.lineTo(target.px, target.py);
        ctx.stroke();
        ctx.restore();
      });

      // 4. Draw 3D Nodes with Perspective Spheres & Glow
      projectedNodes.forEach((node) => {
        if (node.scale <= 0) return;

        const radius = Math.max(4, node.baseRadius * node.scale);

        // Ambient outer glow
        ctx.save();
        const glowRadius = radius * (1.8 + 0.25 * Math.sin(pulseAngle));
        const gradient = ctx.createRadialGradient(
          node.px,
          node.py,
          radius * 0.4,
          node.px,
          node.py,
          glowRadius
        );
        gradient.addColorStop(0, node.glowColor);
        gradient.addColorStop(1, 'transparent');

        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(node.px, node.py, glowRadius, 0, Math.PI * 2);
        ctx.fill();

        // 3D Orbital ring for Critical findings
        if (node.severity === 'CRITICAL') {
          ctx.strokeStyle = 'rgba(239, 68, 68, 0.45)';
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.ellipse(node.px, node.py, radius * 2.2, radius * 0.9, rotY.current * 2, 0, Math.PI * 2);
          ctx.stroke();
        }

        // 3D Shaded Sphere
        const sphereGrad = ctx.createRadialGradient(
          node.px - radius * 0.35,
          node.py - radius * 0.35,
          radius * 0.1,
          node.px,
          node.py,
          radius
        );
        sphereGrad.addColorStop(0, '#ffffff');
        sphereGrad.addColorStop(0.3, node.color);
        sphereGrad.addColorStop(1, '#0f172a');

        ctx.fillStyle = sphereGrad;
        ctx.beginPath();
        ctx.arc(node.px, node.py, radius, 0, Math.PI * 2);
        ctx.fill();

        // Specular 3D highlight rim
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.lineWidth = 1;
        ctx.stroke();

        // Node Label
        ctx.fillStyle = '#0f172a';
        ctx.font = `600 ${Math.max(9, Math.round(11 * node.scale))}px "Plus Jakarta Sans", sans-serif`;
        ctx.textAlign = 'center';
        ctx.fillText(node.label, node.px, node.py + radius + 14);

        ctx.fillStyle = '#64748b';
        ctx.font = `500 ${Math.max(8, Math.round(9 * node.scale))}px "Plus Jakarta Sans", sans-serif`;
        ctx.fillText(node.sublabel, node.px, node.py + radius + 26);

        ctx.restore();
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  // Mouse drag handlers for 3D rotation
  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    isDragging.current = true;
    lastMousePos.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDragging.current) {
      // Check node hover
      const canvas = canvasRef.current;
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      // Project nodes to screen
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const focalLength = 480;

      let found: Node3D | null = null;
      for (const n of nodes) {
        const cosY = Math.cos(rotY.current);
        const sinY = Math.sin(rotY.current);
        const x1 = n.x * cosY + n.z * sinY;
        const z1 = -n.x * sinY + n.z * cosY;

        const cosX = Math.cos(rotX.current);
        const sinX = Math.sin(rotX.current);
        const y2 = n.y * cosX - z1 * sinX;
        const z2 = n.y * sinX + z1 * cosX;

        const distance = focalLength + z2;
        const scale = distance > 10 ? focalLength / distance : 0.001;
        const px = centerX + x1 * scale;
        const py = centerY + y2 * scale;
        const dist = Math.hypot(mouseX - px, mouseY - py);

        if (dist <= n.baseRadius * scale + 10) {
          found = n;
          break;
        }
      }
      setHoveredNode(found);
      return;
    }

    const dx = e.clientX - lastMousePos.current.x;
    const dy = e.clientY - lastMousePos.current.y;

    rotY.current += dx * 0.008;
    rotX.current = Math.max(-1.2, Math.min(1.2, rotX.current + dy * 0.008));

    lastMousePos.current = { x: e.clientX, y: e.clientY };
  };

  const handleMouseUp = () => {
    isDragging.current = false;
  };

  const handleResetAngle = () => {
    rotX.current = 0.25;
    rotY.current = 0.4;
  };

  const toggleAutoRotate = () => {
    isAutoRotate.current = !isAutoRotate.current;
    setAutoRotateState(isAutoRotate.current);
  };

  return (
    <div
      ref={containerRef}
      className="relative rounded-3xl bg-gradient-to-b from-white/95 to-slate-50/90 border border-white/90 shadow-[inset_0_2px_2px_rgba(255,255,255,1),0_15px_40px_-10px_rgba(15,23,42,0.08)] p-4 overflow-hidden"
    >
      {/* 3D Visualizer Top Controls */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-2 px-2 z-20 relative">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-xl bg-lavender-100 flex items-center justify-center text-lavender-700 shadow-xs">
            <Rotate3d className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-extrabold text-navy-900 tracking-tight flex items-center space-x-2">
              <span>Interactive 3D Operational Risk Universe</span>
              <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-cyan-100 text-cyan-800 border border-cyan-200">
                Live 3D WebGL / Canvas
              </span>
            </h3>
            <p className="text-[11px] text-slate-500">
              Click and drag to rotate in 3D space. Inspect cross-dataset lead-lag risk clusters.
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={toggleAutoRotate}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-white/90 border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-xs transition-colors"
          >
            {autoRotateState ? <Pause className="w-3.5 h-3.5 text-lavender-600" /> : <Play className="w-3.5 h-3.5 text-emerald-600" />}
            <span>{autoRotateState ? 'Pause Orbit' : 'Auto-Orbit'}</span>
          </button>
          <button
            onClick={handleResetAngle}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-white/90 border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 shadow-xs transition-colors"
          >
            <Rotate3d className="w-3.5 h-3.5" />
            <span>Reset View</span>
          </button>
        </div>
      </div>

      {/* 3D Canvas */}
      <div className="relative w-full h-[380px] cursor-grab active:cursor-grabbing flex items-center justify-center">
        <canvas
          ref={canvasRef}
          width={900}
          height={380}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          className="w-full h-full block"
        />

        {/* Hovered Node Telemetry HUD Popover */}
        {hoveredNode && (
          <div className="absolute top-4 right-4 pointer-events-none z-30 p-3.5 rounded-2xl bg-white/95 backdrop-blur-md border border-slate-200 shadow-xl max-w-xs animate-in fade-in duration-150">
            <div className="flex items-center space-x-2">
              <span
                className="w-2.5 h-2.5 rounded-full"
                style={{ backgroundColor: hoveredNode.color }}
              />
              <span className="font-extrabold text-navy-900 text-xs">{hoveredNode.label}</span>
            </div>
            <p className="text-[11px] text-slate-600 mt-1">{hoveredNode.sublabel}</p>
            <div className="mt-2 pt-2 border-t border-slate-100 flex justify-between items-center text-[10px]">
              <span className="font-bold text-slate-400">TELEMETRY</span>
              <span className="font-mono font-bold text-navy-900">{hoveredNode.metric}</span>
            </div>
          </div>
        )}

        {/* Bottom Legend */}
        <div className="absolute bottom-3 left-4 pointer-events-none flex items-center space-x-4 text-[10px] font-bold text-slate-500 bg-white/80 backdrop-blur-xs px-3 py-1.5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-red-500 shadow-xs" />
            <span>Critical Cascade</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-amber-500" />
            <span>Downstream Escalation</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-sky-500" />
            <span>Depleted Buffer</span>
          </div>
          <div className="flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            <span>Control Cohorts</span>
          </div>
        </div>
      </div>
    </div>
  );
};
