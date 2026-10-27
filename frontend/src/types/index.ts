export interface HealthStatus {
  status: string;
  service: string;
  timestamp: string;
  database: {
    active_mode: string;
    active_backend_name: string;
    is_exasol_active: boolean;
    connected: boolean;
    health: {
      status: string;
      latency_ms: number;
      connected: boolean;
    };
    exasol_status?: {
      configured?: boolean;
      connected: boolean;
      message?: string;
      error?: string;
    };
  };
  records_loaded: number;
  tables_loaded: number;
}

export interface DatasetSummary {
  table_name: string;
  row_count: number;
  column_count: number;
  missing_values_count: number;
  missing_percentage: number;
  memory_usage_kb: number;
  date_range: string;
}

export interface DatasetSchemaColumn {
  column_name: string;
  data_type: string;
  null_count: number;
  null_percentage: number;
  unique_values: number;
}

export interface Finding {
  finding_id: string;
  title: string;
  description: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  confidence: number;
  confidence_rationale: string;
  affected_dataset: string;
  affected_segment: string;
  relevant_time_window: string;
  baseline_period: string;
  observed_value: number;
  expected_value: number;
  change_magnitude_pct: number;
  detection_method: string;
  supporting_metrics: Record<string, any>;
  data_quality_warnings: string;
  suggested_next_investigation: string;
  timestamp: string;
  status: "New" | "Investigating" | "Confirmed" | "Dismissed" | "Resolved";
  priority: "P1" | "P2" | "P3";
}

export interface CrossMetricCluster {
  cluster_id: string;
  title: string;
  summary: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM";
  segment: string;
  signals_involved: string[];
  signal_titles: string[];
  datasets_involved: string[];
  signal_count: number;
  evidence_strength: number;
  observed_facts: string[];
  statistical_associations: string[];
  hypotheses: string[];
  competing_explanations: string[];
  limitations: string[];
  recommendations: string[];
  correlation_metrics: {
    delivery_refund_r: number;
    p_value_str: string;
    estimated_lead_days: number;
    sample_points: number;
  };
  cohort_comparison: {
    target_region: string;
    unaffected_regions: string[];
    unaffected_count: number;
    target_avg_delay: number;
    control_avg_delay: number;
    delta_delay_ratio: number;
    target_refund_rate_pct: number;
    control_refund_rate_pct: number;
  };
  status: string;
}

export interface InvestigationRecord {
  investigation_id: string;
  finding_id: string;
  title: string;
  status: string;
  priority: string;
  suspected_cause: string;
  verified_conclusion: string;
  notes: string;
  created_at: string;
  updated_at: string;
}

export interface WhatIfResponse {
  inputs: {
    delivery_delay_delta_pct: number;
    refund_rate_delta_pct: number;
    demand_delta_pct: number;
    inventory_reduction_pct: number;
  };
  baseline: {
    monthly_orders: number;
    monthly_revenue: number;
    avg_delivery_delay_days: number;
    refund_rate_pct: number;
    stockout_rate_pct: number;
    monthly_refund_cost: number;
    monthly_complaint_count: number;
  };
  simulated: {
    monthly_orders: number;
    monthly_revenue: number;
    avg_delivery_delay_days: number;
    refund_rate_pct: number;
    stockout_rate_pct: number;
    monthly_refund_cost: number;
    projected_complaint_count: number;
  };
  direct_arithmetic_consequences: string[];
  model_based_projections: string[];
  assumptions_and_limitations: string[];
}

export interface EvaluationResult {
  evaluated: boolean;
  total_ground_truth_anomalies: number;
  signalfire_model: {
    name: string;
    methodology: string;
    detected_count: number;
    true_positives: number;
    false_positives: number;
    false_negatives: number;
    precision: number;
    recall: number;
    f1_score: number;
    detected_findings: string[];
  };
  baseline_model: {
    name: string;
    methodology: string;
    detected_count: number;
    true_positives: number;
    false_positives: number;
    false_negatives: number;
    precision: number;
    recall: number;
    f1_score: number;
  };
  evaluation_notes: string;
  limitations: string[];
}
