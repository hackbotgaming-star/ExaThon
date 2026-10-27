import {
  HealthStatus,
  DatasetSummary,
  DatasetSchemaColumn,
  Finding,
  CrossMetricCluster,
  InvestigationRecord,
  WhatIfResponse,
  EvaluationResult
} from "../types";

const BASE_URL = "/api";

export async function fetchHealth(): Promise<HealthStatus> {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) throw new Error("Failed to fetch health status");
  return res.json();
}

export async function fetchDatabaseStatus(): Promise<any> {
  const res = await fetch(`${BASE_URL}/database/status`);
  if (!res.ok) throw new Error("Failed to fetch database status");
  return res.json();
}

export async function connectDatabase(config: any): Promise<any> {
  const res = await fetch(`${BASE_URL}/database/connect`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(config)
  });
  return res.json();
}

export async function fetchDatasets(): Promise<{ datasets: DatasetSummary[]; active_backend: string }> {
  const res = await fetch(`${BASE_URL}/datasets`);
  if (!res.ok) throw new Error("Failed to fetch datasets");
  return res.json();
}

export async function fetchDatasetSchema(tableName: string): Promise<{ table_name: string; schema: DatasetSchemaColumn[] }> {
  const res = await fetch(`${BASE_URL}/datasets/${tableName}/schema`);
  if (!res.ok) throw new Error(`Failed to fetch schema for ${tableName}`);
  return res.json();
}

export async function fetchDatasetPreview(
  tableName: string,
  page: number = 1,
  pageSize: number = 20,
  search?: string
): Promise<any> {
  let url = `${BASE_URL}/datasets/${tableName}/preview?page=${page}&page_size=${pageSize}`;
  if (search) url += `&search=${encodeURIComponent(search)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to preview ${tableName}`);
  return res.json();
}

export async function uploadDataset(file: File, tableName?: string): Promise<any> {
  const formData = new FormData();
  formData.append("file", file);
  if (tableName) formData.append("table_name", tableName);
  const res = await fetch(`${BASE_URL}/datasets/upload`, {
    method: "POST",
    body: formData
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Upload failed");
  }
  return res.json();
}

export async function resetSampleData(): Promise<any> {
  const res = await fetch(`${BASE_URL}/datasets/reset`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to reset sample datasets");
  return res.json();
}

export async function fetchRelationships(): Promise<{ relationships: any[] }> {
  const res = await fetch(`${BASE_URL}/datasets/relationships`);
  if (!res.ok) throw new Error("Failed to fetch dataset relationships");
  return res.json();
}

export async function runAnomalyDetection(): Promise<{ findings: Finding[]; total_findings: number }> {
  const res = await fetch(`${BASE_URL}/analytics/detect`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to execute anomaly detection");
  return res.json();
}

export async function fetchFindings(): Promise<{ findings: Finding[] }> {
  const res = await fetch(`${BASE_URL}/analytics/findings`);
  if (!res.ok) throw new Error("Failed to fetch findings");
  return res.json();
}

export async function fetchClusters(): Promise<{ clusters: CrossMetricCluster[] }> {
  const res = await fetch(`${BASE_URL}/analytics/clusters`);
  if (!res.ok) throw new Error("Failed to fetch investigation clusters");
  return res.json();
}

export async function fetchEvaluation(): Promise<EvaluationResult> {
  const res = await fetch(`${BASE_URL}/analytics/evaluation`);
  if (!res.ok) throw new Error("Failed to run evaluation");
  return res.json();
}

export async function calculateWhatIf(payload: {
  domain?: string;
  delivery_delay_delta_pct?: number;
  refund_rate_delta_pct?: number;
  demand_delta_pct?: number;
  inventory_reduction_pct?: number;
  vibration_delta_pct?: number;
  pm_backlog_delta_pct?: number;
  parts_lead_time_days_delta?: number;
  hourly_downtime_cost?: number;
}): Promise<WhatIfResponse> {
  const res = await fetch(`${BASE_URL}/analytics/what-if`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Failed to run what-if calculation");
  return res.json();
}

export async function sendChatMessage(message: string): Promise<any> {
  const res = await fetch(`${BASE_URL}/assistant/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  });
  if (!res.ok) throw new Error("Assistant request failed");
  return res.json();
}

export async function fetchInvestigations(): Promise<{ investigations: InvestigationRecord[] }> {
  const res = await fetch(`${BASE_URL}/investigations`);
  if (!res.ok) throw new Error("Failed to fetch investigations");
  return res.json();
}

export async function saveInvestigation(payload: {
  finding_id: string;
  title: string;
  status: string;
  priority: string;
  suspected_cause?: string;
  verified_conclusion?: string;
  notes?: string;
}): Promise<any> {
  const res = await fetch(`${BASE_URL}/investigations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error("Failed to save investigation");
  return res.json();
}
