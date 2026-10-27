import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar, NavTab } from './components/Sidebar';
import { OverviewDashboard } from './pages/OverviewDashboard';
import { DataExplorer } from './pages/DataExplorer';
import { RelationshipsExplorer } from './pages/RelationshipsExplorer';
import { SignalDetectionView } from './pages/SignalDetectionView';
import { CrossMetricView } from './pages/CrossMetricView';
import { InteractiveRiskMap } from './pages/InteractiveRiskMap';
import { InvestigationWorkspace } from './pages/InvestigationWorkspace';
import { WhatIfAnalysis } from './pages/WhatIfAnalysis';
import { AIAssistantView } from './pages/AIAssistantView';
import { EvaluationView } from './pages/EvaluationView';
import { ReportsView } from './pages/ReportsView';
import { SettingsView } from './pages/SettingsView';
import { HealthStatus, Finding, CrossMetricCluster } from './types';
import {
  fetchHealth,
  fetchFindings,
  fetchClusters,
  runAnomalyDetection
} from './services/api';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<NavTab>('overview');
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [clusters, setClusters] = useState<CrossMetricCluster[]>([]);
  const [selectedFinding, setSelectedFinding] = useState<Finding | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [hRes, fRes, cRes] = await Promise.all([
        fetchHealth(),
        fetchFindings(),
        fetchClusters()
      ]);
      setHealth(hRes);
      setFindings(fRes.findings);
      setClusters(cRes.clusters);
      if (fRes.findings.length > 0 && !selectedFinding) {
        setSelectedFinding(fRes.findings[0]);
      }
    } catch (e) {
      console.error("Failed to load initial data", e);
    }
  };

  const handleRunAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      await runAnomalyDetection();
      await loadInitialData();
    } catch (e) {
      console.error(e);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSelectFinding = (finding: Finding) => {
    setSelectedFinding(finding);
  };

  const handleOpenWorkspace = (finding: Finding) => {
    setSelectedFinding(finding);
    setCurrentTab('investigation');
  };

  const criticalCount = findings.filter(f => f.severity === 'CRITICAL').length;

  return (
    <div className="min-h-screen flex flex-col bg-[#f8fafc] text-navy-900 relative overflow-hidden">
      {/* 3D Ambient Depth Glow Spheres for Parallax Glass Depth */}
      <div className="glow-orb-lavender -top-20 -left-20 opacity-60" />
      <div className="glow-orb-cyan top-1/3 -right-24 opacity-50" />
      <div className="glow-orb-lavender -bottom-48 left-1/4 opacity-35" />

      {/* Top Navigation */}
      <Navbar
        health={health}
        onRefresh={loadInitialData}
        onRunAnalysis={handleRunAnalysis}
        isAnalyzing={isAnalyzing}
        onOpenSettings={() => setCurrentTab('settings')}
      />

      {/* Main Layout Area */}
      <div className="flex-1 flex overflow-hidden relative z-10">
        {/* Navigation Sidebar */}
        <Sidebar
          currentTab={currentTab}
          onSelectTab={setCurrentTab}
          criticalCount={criticalCount}
        />

        {/* Content View Area */}
        <main className="flex-1 overflow-y-auto custom-scrollbar p-6 md:p-8 max-w-7xl mx-auto w-full">
          {currentTab === 'overview' && (
            <OverviewDashboard
              findings={findings}
              clusters={clusters}
              health={health}
              onNavigate={setCurrentTab}
              onSelectFinding={(f) => {
                setSelectedFinding(f);
                setCurrentTab('signals');
              }}
            />
          )}

          {currentTab === 'explorer' && <DataExplorer />}

          {currentTab === 'relationships' && <RelationshipsExplorer />}

          {currentTab === 'signals' && (
            <SignalDetectionView
              findings={findings}
              selectedFinding={selectedFinding}
              onSelectFinding={handleSelectFinding}
              onCloseDetail={() => setSelectedFinding(null)}
              onOpenWorkspace={handleOpenWorkspace}
            />
          )}

          {currentTab === 'cross-metric' && (
            <CrossMetricView
              clusters={clusters}
              onSelectFindingId={(id) => {
                const f = findings.find(x => x.finding_id === id);
                if (f) {
                  setSelectedFinding(f);
                  setCurrentTab('signals');
                }
              }}
            />
          )}

          {currentTab === 'risk-map' && (
            <InteractiveRiskMap
              findings={findings}
              clusters={clusters}
              onSelectFinding={(f) => {
                setSelectedFinding(f);
                setCurrentTab('signals');
              }}
            />
          )}

          {currentTab === 'investigation' && (
            <InvestigationWorkspace
              findings={findings}
              selectedFinding={selectedFinding}
              onSelectFinding={setSelectedFinding}
            />
          )}

          {currentTab === 'what-if' && <WhatIfAnalysis />}

          {currentTab === 'assistant' && <AIAssistantView />}

          {currentTab === 'evaluation' && <EvaluationView />}

          {currentTab === 'reports' && (
            <ReportsView
              findings={findings}
              clusters={clusters}
              health={health}
            />
          )}

          {currentTab === 'settings' && (
            <SettingsView
              health={health}
              onRefreshHealth={loadInitialData}
            />
          )}
        </main>
      </div>
    </div>
  );
};
