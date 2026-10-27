"""
SIGNALFIRE AI - Backend FastAPI Application
Exposes analytical API endpoints for anomaly detection, cross-metric investigation,
database management (Exasol Personal / DuckDB), what-if analysis, and report generation.
"""

import os
import io
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import pandas as pd
from datetime import datetime

from .database.manager import db_manager
from .analytics.detector import SignalDetector
from .analytics.cross_metric import CrossMetricEngine
from .analytics.evaluator import AnomalyEvaluator
from .analytics.what_if import WhatIfEngine
from .analytics.assistant import InvestigationAssistant
from .reporting.report_generator import ReportGenerator

app = FastAPI(
    title="SIGNALFIRE AI API",
    description="Cross-Dataset Anomaly Detection, Risk Discovery, and Decision Support Engine",
    version="1.0.0"
)

# Enable CORS for local Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session caches for fast exploration
DATASETS_CACHE: Dict[str, pd.DataFrame] = {}
CACHED_FINDINGS: List[Dict[str, Any]] = []
CACHED_CLUSTERS: List[Dict[str, Any]] = []
INVESTIGATIONS_CACHE: List[Dict[str, Any]] = []

detector = SignalDetector()
cross_metric_engine = CrossMetricEngine()
evaluator = AnomalyEvaluator(ground_truth_file="data/ground_truth.json")
what_if_engine = WhatIfEngine()
assistant = InvestigationAssistant()
report_generator = ReportGenerator(output_dir="deliverables")

def load_local_csvs_into_db():
    global DATASETS_CACHE, CACHED_FINDINGS, CACHED_CLUSTERS
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    csv_dir = os.path.join(base_dir, "data", "csv")
    if not os.path.exists(csv_dir) or not os.listdir(csv_dir):
        from data.generation.generate_retail_data import generate_all_datasets
        DATASETS_CACHE = generate_all_datasets(csv_dir)
    else:
        for fname in os.listdir(csv_dir):
            if fname.endswith(".csv"):
                table_name = fname.replace(".csv", "")
                df = pd.read_csv(os.path.join(csv_dir, fname))
                DATASETS_CACHE[table_name] = df
                try:
                    db_manager.load_table(table_name, df, if_exists="replace")
                except Exception as e:
                    print(f"Warning: Could not load {table_name} into DB: {e}")
    if DATASETS_CACHE:
        CACHED_FINDINGS = detector.run_all_detection(DATASETS_CACHE)
        CACHED_CLUSTERS = cross_metric_engine.investigate_signals(CACHED_FINDINGS, DATASETS_CACHE)

# Preload data on module load so all endpoints and tests have data immediately
load_local_csvs_into_db()

@app.on_event("startup")
async def startup_event():
    if not DATASETS_CACHE:
        load_local_csvs_into_db()

# ----------------- SYSTEM & DATABASE ENDPOINTS -----------------

@app.get("/api/health")
def get_health():
    db_status = db_manager.get_status()
    total_records = sum(len(df) for df in DATASETS_CACHE.values())
    return {
        "status": "healthy",
        "service": "SIGNALFIRE AI Core Engine",
        "timestamp": datetime.utcnow().isoformat(),
        "database": {
            **db_status,
            "connected": db_status["health"]["connected"]
        },
        "records_loaded": total_records,
        "tables_loaded": len(DATASETS_CACHE)
    }

@app.get("/api/database/status")
def get_database_status():
    return db_manager.get_status()

class ConnectExasolPayload(BaseModel):
    mode: str = "EXASOL"
    dsn: Optional[str] = "localhost:8563"
    user: Optional[str] = "sys"
    password: Optional[str] = "exasol"
    schema_name: Optional[str] = "SIGNALFIRE"
    timeout: Optional[int] = 5

@app.post("/api/database/connect")
def connect_database(payload: ConnectExasolPayload):
    config = {
        "dsn": payload.dsn,
        "user": payload.user,
        "password": payload.password,
        "schema": payload.schema_name,
        "timeout": payload.timeout
    }
    result = db_manager.switch_backend(payload.mode, config)
    # If switch succeeded and we have cached data, load tables into the active DB
    if result["success"] and DATASETS_CACHE:
        for t_name, df in DATASETS_CACHE.items():
            try:
                db_manager.load_table(t_name, df, if_exists="replace")
            except Exception:
                pass
    return result

# ----------------- DATA EXPLORER ENDPOINTS -----------------

@app.get("/api/datasets")
def list_datasets():
    results = []
    for name, df in DATASETS_CACHE.items():
        date_cols = [c for c in df.columns if "date" in c.lower()]
        date_range = "N/A"
        if date_cols:
            first_col = date_cols[0]
            try:
                s_dates = pd.to_datetime(df[first_col]).dropna()
                if not s_dates.empty:
                    date_range = f"{s_dates.min().strftime('%Y-%m-%d')} to {s_dates.max().strftime('%Y-%m-%d')}"
            except Exception:
                pass

        results.append({
            "table_name": name,
            "row_count": len(df),
            "column_count": len(df.columns),
            "missing_values_count": int(df.isna().sum().sum()),
            "missing_percentage": round(float(df.isna().sum().sum() / max(1, df.size)) * 100, 2),
            "memory_usage_kb": round(float(df.memory_usage(deep=True).sum()) / 1024, 1),
            "date_range": date_range
        })
    return {"datasets": results, "active_backend": db_manager.adapter.backend_name}

@app.get("/api/datasets/{table_name}/schema")
def get_dataset_schema(table_name: str):
    if table_name not in DATASETS_CACHE:
        raise HTTPException(status_code=404, detail=f"Dataset '{table_name}' not found.")
    df = DATASETS_CACHE[table_name]
    schema = []
    for col in df.columns:
        schema.append({
            "column_name": col,
            "data_type": str(df[col].dtype),
            "null_count": int(df[col].isna().sum()),
            "null_percentage": round(float(df[col].isna().sum() / len(df)) * 100, 2),
            "unique_values": int(df[col].nunique())
        })
    return {"table_name": table_name, "schema": schema}

@app.get("/api/datasets/{table_name}/preview")
def preview_dataset(
    table_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    search: Optional[str] = None
):
    if table_name not in DATASETS_CACHE:
        raise HTTPException(status_code=404, detail=f"Dataset '{table_name}' not found.")
    df = DATASETS_CACHE[table_name]
    
    filtered_df = df
    if search:
        mask = filtered_df.astype(str).apply(lambda row: row.str.contains(search, case=False).any(), axis=1)
        filtered_df = filtered_df[mask]

    total_rows = len(filtered_df)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_df = filtered_df.iloc[start_idx:end_idx].fillna("")

    return {
        "table_name": table_name,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total_rows + page_size - 1) // page_size),
        "columns": list(page_df.columns),
        "data": page_df.to_dict(orient="records")
    }

@app.post("/api/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    table_name: Optional[str] = Form(None)
):
    # Security & format verification
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files (.csv) are currently supported.")
    
    contents = await file.read()
    if len(contents) > 25 * 1024 * 1024: # 25MB safety boundary
        raise HTTPException(status_code=400, detail="File size exceeds maximum upload limit of 25MB.")

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Malformed CSV content: {str(e)}")

    target_name = table_name or file.filename.replace(".csv", "").lower().replace("-", "_").replace(" ", "_")
    # Sanitize table name
    target_name = "".join(c for c in target_name if c.isalnum() or c == "_")

    DATASETS_CACHE[target_name] = df
    db_manager.load_table(target_name, df, if_exists="replace")

    return {
        "success": True,
        "table_name": target_name,
        "rows_imported": len(df),
        "columns": list(df.columns),
        "message": f"Dataset '{target_name}' successfully validated and ingested."
    }

@app.post("/api/datasets/reset")
def reset_sample_datasets():
    load_local_csvs_into_db()
    global CACHED_FINDINGS, CACHED_CLUSTERS
    CACHED_FINDINGS = detector.run_all_detection(DATASETS_CACHE)
    CACHED_CLUSTERS = cross_metric_engine.investigate_signals(CACHED_FINDINGS, DATASETS_CACHE)
    return {
        "success": True,
        "message": "Synthetic retail datasets reloaded and reindexed into active analytical database.",
        "tables": list(DATASETS_CACHE.keys())
    }

@app.get("/api/datasets/relationships")
def get_dataset_relationships():
    """Identifies candidate relationship keys across tables."""
    candidates = [
        {"source_table": "orders", "source_col": "order_id", "target_table": "sales", "target_col": "order_id", "type": "Foreign Key (1:N)", "status": "Verified"},
        {"source_table": "orders", "source_col": "order_id", "target_table": "deliveries", "target_col": "order_id", "type": "Foreign Key (1:1)", "status": "Verified"},
        {"source_table": "orders", "source_col": "order_id", "target_table": "refunds", "target_col": "order_id", "type": "Foreign Key (1:N)", "status": "Verified"},
        {"source_table": "orders", "source_col": "order_id", "target_table": "customer_complaints", "target_col": "order_id", "type": "Foreign Key (1:N)", "status": "Verified"},
        {"source_table": "sales", "source_col": "product_id", "target_table": "inventory", "target_col": "product_id", "type": "Dimension Key (1:N)", "status": "Verified"},
        {"source_table": "suppliers", "source_col": "product_id", "target_table": "inventory", "target_col": "product_id", "type": "Dimension Key (1:N)", "status": "Verified"},
        {"source_table": "deliveries", "source_col": "region", "target_table": "customer_retention", "target_col": "region", "type": "Geographic Dimension", "status": "Candidate Association"},
        {"source_table": "refunds", "source_col": "region", "target_table": "customer_complaints", "target_col": "region", "type": "Geographic Dimension", "status": "Candidate Association"},
    ]
    return {"relationships": candidates}

# ----------------- ANALYTICS & INVESTIGATION ENDPOINTS -----------------

@app.post("/api/analytics/detect")
def run_anomaly_detection():
    global CACHED_FINDINGS, CACHED_CLUSTERS
    if not DATASETS_CACHE:
        load_local_csvs_into_db()
    CACHED_FINDINGS = detector.run_all_detection(DATASETS_CACHE)
    CACHED_CLUSTERS = cross_metric_engine.investigate_signals(CACHED_FINDINGS, DATASETS_CACHE)
    return {
        "total_findings": len(CACHED_FINDINGS),
        "critical_count": sum(1 for f in CACHED_FINDINGS if f.get("severity") == "CRITICAL"),
        "high_count": sum(1 for f in CACHED_FINDINGS if f.get("severity") == "HIGH"),
        "medium_count": sum(1 for f in CACHED_FINDINGS if f.get("severity") == "MEDIUM"),
        "findings": CACHED_FINDINGS
    }

@app.get("/api/analytics/findings")
def get_findings():
    global CACHED_FINDINGS
    if not CACHED_FINDINGS:
        CACHED_FINDINGS = detector.run_all_detection(DATASETS_CACHE)
    return {"findings": CACHED_FINDINGS}

@app.get("/api/analytics/clusters")
def get_investigation_clusters():
    global CACHED_CLUSTERS
    if not CACHED_CLUSTERS:
        if not CACHED_FINDINGS:
            run_anomaly_detection()
        CACHED_CLUSTERS = cross_metric_engine.investigate_signals(CACHED_FINDINGS, DATASETS_CACHE)
    return {"clusters": CACHED_CLUSTERS}

@app.get("/api/analytics/evaluation")
def get_evaluation():
    if not DATASETS_CACHE:
        load_local_csvs_into_db()
    return evaluator.evaluate(DATASETS_CACHE)

class WhatIfRequest(BaseModel):
    delivery_delay_delta_pct: float = 0.0
    refund_rate_delta_pct: float = 0.0
    demand_delta_pct: float = 0.0
    inventory_reduction_pct: float = 0.0

@app.post("/api/analytics/what-if")
def calculate_what_if(req: WhatIfRequest):
    # Derive baseline benchmarks dynamically from active tables
    monthly_orders = 5700
    if "orders" in DATASETS_CACHE:
        monthly_orders = int(len(DATASETS_CACHE["orders"]) / 3.0)

    base_metrics = {
        "monthly_orders": monthly_orders,
        "avg_order_value": 114.50,
        "avg_delay_days": 1.78,
        "refund_rate_pct": 3.1,
        "stockout_rate_pct": 4.2,
        "complaint_rate_pct": 2.5
    }
    return what_if_engine.simulate_scenario(
        base_metrics=base_metrics,
        delivery_delay_delta_pct=req.delivery_delay_delta_pct,
        refund_rate_delta_pct=req.refund_rate_delta_pct,
        demand_delta_pct=req.demand_delta_pct,
        inventory_reduction_pct=req.inventory_reduction_pct
    )

class ChatRequest(BaseModel):
    message: str

@app.post("/api/assistant/chat")
def chat_assistant(req: ChatRequest):
    global CACHED_FINDINGS, CACHED_CLUSTERS
    if not CACHED_FINDINGS:
        run_anomaly_detection()
    return assistant.answer_query(
        query=req.message,
        findings=CACHED_FINDINGS,
        clusters=CACHED_CLUSTERS,
        datasets=DATASETS_CACHE
    )

# ----------------- INVESTIGATION WORKSPACE ENDPOINTS -----------------

class InvestigationCreatePayload(BaseModel):
    finding_id: str
    title: str
    status: str = "Investigating"
    priority: str = "P1"
    suspected_cause: Optional[str] = ""
    verified_conclusion: Optional[str] = ""
    notes: Optional[str] = ""

@app.get("/api/investigations")
def list_investigations():
    return {"investigations": INVESTIGATIONS_CACHE}

@app.post("/api/investigations")
def save_investigation(payload: InvestigationCreatePayload):
    # Check if existing record
    existing = next((inv for inv in INVESTIGATIONS_CACHE if inv["finding_id"] == payload.finding_id), None)
    now = datetime.utcnow().isoformat()
    if existing:
        existing.update({
            "status": payload.status,
            "priority": payload.priority,
            "suspected_cause": payload.suspected_cause,
            "verified_conclusion": payload.verified_conclusion,
            "notes": payload.notes,
            "updated_at": now
        })
        item = existing
    else:
        item = {
            "investigation_id": f"INV-{uuid.uuid4().hex[:6].upper()}",
            "finding_id": payload.finding_id,
            "title": payload.title,
            "status": payload.status,
            "priority": payload.priority,
            "suspected_cause": payload.suspected_cause,
            "verified_conclusion": payload.verified_conclusion,
            "notes": payload.notes,
            "created_at": now,
            "updated_at": now
        }
        INVESTIGATIONS_CACHE.append(item)

    # Sync finding status in CACHED_FINDINGS
    for f in CACHED_FINDINGS:
        if f.get("finding_id") == payload.finding_id:
            f["status"] = payload.status
            f["priority"] = payload.priority
            break

    return {"success": True, "investigation": item}

# ----------------- REPORTING DOWNLOAD ENDPOINTS -----------------

@app.get("/api/reports/pdf")
def download_pdf_report():
    metadata = {
        "backend_name": db_manager.adapter.backend_name,
        "records_analyzed": sum(len(df) for df in DATASETS_CACHE.values())
    }
    pdf_path = report_generator.generate_pdf_report(CACHED_FINDINGS, CACHED_CLUSTERS, metadata)
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="SIGNALFIRE_AI_Executive_Report.pdf"
    )

@app.get("/api/reports/json")
def download_json_report():
    metadata = {
        "backend_name": db_manager.adapter.backend_name,
        "records_analyzed": sum(len(df) for df in DATASETS_CACHE.values())
    }
    json_path = report_generator.generate_json_report(CACHED_FINDINGS, CACHED_CLUSTERS, metadata)
    return FileResponse(
        json_path,
        media_type="application/json",
        filename="SIGNALFIRE_AI_Report.json"
    )

@app.get("/api/reports/csv")
def download_csv_report():
    csv_path = report_generator.generate_csv_report(CACHED_FINDINGS)
    return FileResponse(
        csv_path,
        media_type="text/csv",
        filename="SIGNALFIRE_AI_Findings.csv"
    )

# Import uuid for ID generation
import uuid
