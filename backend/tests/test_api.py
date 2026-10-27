"""
SIGNALFIRE AI - Backend Test Suite
Tests:
- API health check
- Dataset loading and schema retrieval
- Anomaly detection pipeline
- Cross-metric investigation
- Ground-truth evaluation
- What-if scenario sensitivity
- Report generation (PDF, JSON, CSV)
- Exasol / DuckDB adapter fallback behavior
- Input validation and edge cases
"""

import os
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app, db_manager, DATASETS_CACHE

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert data["database"]["connected"] is True

def test_database_status_transparency():
    response = client.get("/api/database/status")
    assert response.status_code == 200
    data = response.json()
    assert "active_mode" in data
    assert data["active_mode"] in ["DUCKDB", "EXASOL"]
    # Check that it clearly indicates active backend
    assert "active_backend_name" in data

def test_list_datasets():
    response = client.get("/api/datasets")
    assert response.status_code == 200
    data = response.json()
    assert "datasets" in data
    table_names = [d["table_name"] for d in data["datasets"]]
    assert "sales" in table_names
    assert "deliveries" in table_names
    assert "customer_complaints" in table_names
    assert "refunds" in table_names

def test_dataset_preview():
    response = client.get("/api/datasets/deliveries/preview?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["table_name"] == "deliveries"
    assert len(data["data"]) == 10
    assert "delivery_id" in data["columns"]

def test_dataset_relationships():
    response = client.get("/api/datasets/relationships")
    assert response.status_code == 200
    data = response.json()
    assert len(data["relationships"]) > 0

def test_anomaly_detection_execution():
    response = client.post("/api/analytics/detect")
    assert response.status_code == 200
    data = response.json()
    assert data["total_findings"] > 0
    # North delivery delay should be caught as Critical or High
    titles = [f["title"] for f in data["findings"]]
    assert any("North" in t for t in titles)

def test_cross_metric_investigation():
    response = client.get("/api/analytics/clusters")
    assert response.status_code == 200
    data = response.json()
    assert "clusters" in data
    assert len(data["clusters"]) >= 1
    top_cluster = data["clusters"][0]
    assert "observed_facts" in top_cluster
    assert "statistical_associations" in top_cluster
    assert "hypotheses" in top_cluster
    assert "limitations" in top_cluster

def test_ground_truth_evaluation():
    response = client.get("/api/analytics/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert data["evaluated"] is True
    assert "signalfire_model" in data
    assert "baseline_model" in data
    sf = data["signalfire_model"]
    assert sf["precision"] > 0.6
    assert sf["recall"] >= 0.75
    assert sf["f1_score"] > 0.7

def test_what_if_analysis():
    payload = {
        "delivery_delay_delta_pct": 25.0,
        "refund_rate_delta_pct": 2.5,
        "demand_delta_pct": 10.0,
        "inventory_reduction_pct": 15.0
    }
    response = client.post("/api/analytics/what-if", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "direct_arithmetic_consequences" in data
    assert "model_based_projections" in data
    assert len(data["direct_arithmetic_consequences"]) >= 3

def test_assistant_chat_tool():
    payload = {"message": "Which region has the largest increase in refunds?"}
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "North" in data["answer"]
    assert data["grounded"] is True

def test_investigation_persistence():
    payload = {
        "finding_id": "SIG-DELIV-NORTH-TEST",
        "title": "Delivery Delay Investigation",
        "status": "Confirmed",
        "priority": "P1",
        "suspected_cause": "Carrier SwiftFreight transit hub equipment failure",
        "verified_conclusion": "SLA breach validated with dispatch logs",
        "notes": "Escalated to VP of Operations"
    }
    response = client.post("/api/investigations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    # Retrieve investigations
    get_res = client.get("/api/investigations")
    assert get_res.status_code == 200
    invs = get_res.json()["investigations"]
    assert any(i["finding_id"] == "SIG-DELIV-NORTH-TEST" for i in invs)

def test_report_downloads():
    # PDF
    pdf_res = client.get("/api/reports/pdf")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    assert len(pdf_res.content) > 1000

    # JSON
    json_res = client.get("/api/reports/json")
    assert json_res.status_code == 200
    assert "application/json" in json_res.headers["content-type"]

    # CSV
    csv_res = client.get("/api/reports/csv")
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers["content-type"]
