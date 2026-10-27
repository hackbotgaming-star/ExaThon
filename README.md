# SIGNALFIRE AI

> **Find the warning signs hidden across your data.**

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178c6.svg)](https://www.typescriptlang.org/)
[![Exasol Personal](https://img.shields.io/badge/Database-Exasol%20Personal%20%7C%20DuckDB-indigo.svg)](https://www.exasol.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Overview
**SIGNALFIRE AI** is an enterprise AI-powered business intelligence, cross-dataset anomaly detection, risk discovery, and decision-support platform. 

Businesses collect massive volumes of operational data across sales, orders, deliveries, inventory, customer complaints, returns, and customer retention. Traditional business intelligence tools monitor these metrics independently. Emerging systemic problems frequently escape notice because small, sub-threshold changes co-occur across multiple datasets without tripping isolated single-metric alarms.

SIGNALFIRE AI ingests and analyzes related operational streams, applies noise-robust statistical outlier detection, synchronizes multi-table temporal windows, discovers lead-lag correlations, benchmarks incident segments against unaffected control cohorts, and formulates structured, actionable investigation hypotheses.

**Core Differentiating Principle**: SIGNALFIRE AI rigorously distinguishes **Observed Facts**, **Statistical Associations**, **Hypotheses**, **Competing Explanations**, and **Recommendations**. It never presents statistical correlation as proven causation.

---

## 2. Problem Statement
> *"Retail operations teams often struggle to identify emerging operational problems because sales, inventory, delivery, refund, and customer complaint data are analyzed separately. Small changes across individual metrics may appear harmless, even when their combined pattern indicates a developing problem. Manually reviewing these datasets is time-consuming and depends heavily on predefined alerts. SIGNALFIRE AI aims to help analysts discover unusual cross-metric patterns, investigate supporting evidence, and prioritize potential operational risks before they escalate."*

---

## 3. Target Users
- **Business Operations Managers**: Rapidly detect localized fulfillment hub breakdowns and inventory stockout bottlenecks before they trigger mass return waves.
- **Retail & Supply Chain Analysts**: Trace causal cascades linking supplier defects and carrier transit delays directly to downstream refund escalations.
- **Data Analysts**: Investigate empirical Pearson and Spearman cross-dataset correlation matrices with automated lead-lag offset discovery.
- **Operations & Risk Leaders**: Receive executive audit-ready PDF reports with verified conclusions, remediation notes, and SLA partner audit trails.
- **Customer Experience & Retention Teams**: Understand why repeat purchase cohorts deteriorate by correlating fulfillment failures to customer churn.

---

## 4. Why the Problem Matters
In high-velocity commerce and retail supply chains, isolated monitoring creates compounding blind spots:
1. **The Lead-Lag Blind Spot**: A delivery carrier delay occurring on Day 50 triggers customer complaints on Day 52 and return requests on Day 54. When analyzed in separate departmental silos, the delivery team views the delay as a minor temporary SLA dip, while the returns team treats refund surges as a product quality defect.
2. **Alert Fatigue & Noise**: Static percentage thresholds (e.g., alert when refunds increase by 20%) trigger relentless false positives during normal weekend volume peaks. Analysts progressively ignore or silence alerts.
3. **Severe Financial & Brand Churn**: By the time an operational breakdown escalates to an executive dashboard, hundreds of customers have experienced delayed transit and stockouts, irreversibly damaging customer lifetime value (LTV).

---

## 5. Proposed Solution
SIGNALFIRE AI introduces an integrated, 5-stage analytical architecture:
1. **Independent Anomaly Detection**: Evaluates each operational stream using Median Absolute Deviation (MAD) and Interquartile Range (IQR) non-parametric outlier fences.
2. **Cross-Dataset Temporal Synchronization**: Aligns timestamps, customer IDs, order IDs, product categories, and geographical regions across eight relational tables.
3. **Statistical Association Engine**: Computes empirical correlation coefficients ($r$) and automated lead-lag time offsets.
4. **Unaffected Cohort Benchmarking**: Automatically contrasts incident segments (e.g., North region) against non-incident control cohorts (South, East, West) to verify localized causality versus macro market shifts.
5. **Disciplined Hypothesis Formulation**: Systematically articulates competing alternative explanations and analytical limitations rather than making premature causal leaps.

---

## 6. Features
- **Executive Overview Dashboard**: High-level KPI pulse, active findings count, signal onset trend curves, risk distribution donut chart, and live analytical engine indicator.
- **Data Explorer & Quality Profiler**: Table schema inspector, null distributions, unique value tallies, paginated preview with search and filtering, and secure CSV file upload.
- **Dataset Relationship Explorer**: Maps foreign key relationships, shared dimensions, and temporal synchronization candidates across all operational tables.
- **Signal Detection Engine**: Granular outlier explorer featuring observed vs baseline values, delta percentages, detection methodologies, and statistical confidence explanations.
- **Cross-Metric Investigation Engine (Core Differentiator)**: Multi-table risk clusters, empirical Pearson correlation ($r=0.89$), lead-lag offsets (~3 days), and control cohort benchmarking.
- **Interactive Risk Map**: Topological segment network visualizing operational risk nodes and causal cascade pathways with instant side-drawer telemetry inspection.
- **Investigation Workspace**: Decision-support ticket manager allowing analysts to assign operational priorities (P1–P3), update statuses (`New`, `Investigating`, `Confirmed`, `Dismissed`, `Resolved`), record verified conclusions, and log follow-up actions.
- **What-If Scenario Analysis**: Parameterized sensitivity workspace with interactive sliders for delivery delays, refund rates, demand volume, and inventory levels, clearly separating direct arithmetic consequences from behavioral model projections.
- **AI Investigation Assistant**: Tool-grounded conversational assistant that retrieves verified evidence from analytical database queries, guaranteeing zero metric hallucinations.
- **Audit-Ready Report Generator**: Generates and downloads publication-grade Executive PDF reports (via ReportLab), structured JSON manifests, and flat CSV spreadsheets with one click.
- **System Settings & Health**: Full Exasol Personal connection manager, backend switcher, automated sample-data reload, and detection sensitivity calibrators.

---

## 7. Architecture Diagram
```
+-----------------------------------------------------------------------------------+
|                           SIGNALFIRE AI ARCHITECTURE                              |
+-----------------------------------------------------------------------------------+

 [FRONTEND APPLICATION (Port 3000)]
   │
   ├── React 18 + TypeScript + Vite
   ├── Premium Light-Theme 3D Glassmorphism Design Language
   ├── Recharts (Area, Donut, Timeline Visualizations)
   └── Lucide Enterprise Icons
   │
   ▼ RESTful HTTP / JSON (Proxy Port 3000 -> 8000)
 [BACKEND API & ANALYTICS (FastAPI, Port 8000)]
   │
   ├── FastAPI Application (app/main.py)
   ├── Signal Detection Engine (app/analytics/detector.py)
   │     • Robust Z-Score via Median Absolute Deviation (MAD)
   │     • Interquartile Range (IQR) Non-Parametric Outlier Fences
   │
   ├── Cross-Metric Investigation Engine (app/analytics/cross_metric.py)
   │     • Multi-Dataset Temporal Alignment
   │     • Pearson & Spearman Correlation (Scipy / NumPy)
   │     • Lead-Lag Offset Discovery (~3-Day Offset)
   │     • Control Cohort Contrast (North vs South, East, West)
   │
   ├── Ground Truth Evaluator (app/analytics/evaluator.py)
   ├── What-If Sensitivity Simulator (app/analytics/what_if.py)
   ├── Evidence-Backed AI Assistant (app/analytics/assistant.py)
   └── Executive Report Generator (app/reporting/report_generator.py)
   │
   ▼
 [DATABASE ADAPTER LAYER (app/database/manager.py)]
   │
   ├── ExasolAdapter (app/database/exasol_adapter.py)
   │     • Official pyexasol Driver (WebSocket JSON-RPC)
   │     • High-Throughput In-Memory Analytical SQL
   │     • Real-time Health Check & Latency Telemetry
   │
   └── DuckDBAdapter (app/database/duckdb_adapter.py)
         • Local High-Performance In-Process Columnar OLAP Engine
         • Zero-Dependency Offline Startup & Demo Capabilities
```

---

## 8. Technology Stack
- **Frontend**: React 18, TypeScript 5.7, Vite 6, Tailwind CSS 3.4, Recharts 2.15, Lucide React, Glassmorphism UI.
- **Backend**: Python 3.12, FastAPI 0.110+, Pydantic v2, Uvicorn.
- **Analytics & ML**: NumPy, Pandas, Scipy, Scikit-learn.
- **Databases**:
  - **Primary**: Exasol Personal (In-Memory MPP Analytical Database via `pyexasol`).
  - **Local Development / Fallback**: DuckDB (In-Process Columnar OLAP Engine).
- **Document & Deliverable Generation**: ReportLab (PDF compilation), python-pptx (PowerPoint deck generation).
- **Testing**: Pytest, FastAPI TestClient.

---

## 9. Exasol Integration
Exasol Personal is integrated via the official `pyexasol` driver:
- **Connection Management**: Configurable via `EXASOL_DSN`, `EXASOL_USER`, `EXASOL_PASSWORD`, and `EXASOL_SCHEMA`.
- **Health Telemetry**: Active health checks measuring ping latency and verifying database version via `SYS.EXA_METADATA`.
- **Analytical Queries**: Executes high-throughput cross-table rollups, aggregation queries, and segment group-bys.
- **Database Adapter Pattern**: Completely abstracts the database interface, enabling seamless switching between Exasol Personal and DuckDB Local fallback.
- **Transparency Mandate**: The UI and API clearly indicate which engine is active. Local calculations are **never** labeled as Exasol-powered.

---

## 10. Screenshots Section
*(To capture screenshots from the running application, start the system and capture the following recommended views:)*

1. **Overview Dashboard**: `http://localhost:3000` (Displays live KPI cards, signal onset curves, and active backend badge).
2. **Cross-Metric Investigation View**: `http://localhost:3000` -> Cross-Metric Engine (Displays correlation coefficient $r=0.89$, lead-lag dynamics, and control cohort contrast).
3. **Interactive Risk Map**: `http://localhost:3000` -> Interactive Risk Map (Displays topological node network and regional risk drawer).
4. **Investigation Workspace**: `http://localhost:3000` -> Investigation Workspace (Displays decision-support ticket editor and status persist controls).
5. **What-If Analysis Workspace**: `http://localhost:3000` -> What-If Analysis (Displays interactive parameter sliders and direct arithmetic vs model consequence panels).

---

## 11. Sample Data & Demonstration Mode
The application includes a reproducible synthetic dataset generator (`data/generation/generate_retail_data.py`) spanning 90 days and 17,216+ transactions across eight tables:
1. `sales`: Transaction line items, categories, dollar amounts, units sold.
2. `orders`: Order headers, customer accounts, timestamps, acquisition channels.
3. `deliveries`: Carrier partners, dispatch dates, delivery dates, promised days, delay days.
4. `customer_complaints`: Support tickets, complaint drivers, severity levels.
5. `refunds`: Return disbursements, dollar amounts, customer-stated return reasons.
6. `inventory`: Warehouse snapshots, SKU stock levels, reorder thresholds, stockout flags.
7. `suppliers`: Vendor manufacturing lead times, parts defect rates, reliability scores.
8. `customer_retention`: Weekly customer cohort snapshots, repeat purchase rates, churn rates.

### Controlled Anomaly Injections (Ground Truth Registry)
- **Day 50+ (North Region)**: Carrier SwiftFreight transit hub breakdown; average delivery delays surge from 1.2 days to 5.4 days (+325%).
- **Day 52+ (North Region)**: Customer complaints surge (+320%), predominantly driven by `Delayed Delivery` and `Damaged Packaging`.
- **Day 54+ (North Region)**: Refund disbursements spike from 2.6% to 11.4% of orders with an empirical 3-day lag.
- **Day 56+ (North Region)**: Fulfillment stockouts in `Electronics` jump from 3% to 44%.
- **Day 60+ (North Region)**: Repeat purchase retention contracts from 41.5% down to 22.0%.
- **Control Cohorts**: The `South`, `East`, and `West` regions remain completely normal, serving as statistical control baselines.

---

## 12. Installation Prerequisites
- Python 3.11 or 3.12
- Node.js v18+ and npm 9+
- Docker *(Optional, for running Exasol Personal locally)*

---

## 13. Local Setup Instructions

```bash
# Clone or navigate to the repository
cd signalfire-ai

# Copy sample environment configuration
cp .env.example .env

# Install backend dependencies
pip install fastapi pydantic duckdb pyexasol python-pptx pytest reportlab scikit-learn pandas numpy uvicorn

# Install frontend dependencies
cd frontend
npm install
cd ..
```

---

## 14. Environment Variables
Configure `.env` as required:
```ini
EXASOL_DSN=localhost:8563
EXASOL_USER=sys
EXASOL_PASSWORD=exasol
EXASOL_SCHEMA=SIGNALFIRE
DUCKDB_PATH=signalfire_local.duckdb
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

---

## 15. Exasol Personal Setup (Optional)
To run Exasol Personal in a local Docker container:
```bash
docker run --name exasol-personal \
  -p 8563:8563 \
  --privileged \
  -d exasol/docker-db:latest
```
*Note: If Exasol is not running, SIGNALFIRE AI automatically and transparently operates using the local DuckDB adapter.*

---

## 16. Starting Frontend & Backend

### Start Backend API:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Start Frontend Application:
In a separate terminal:
```bash
cd frontend
npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 17. Running the Demo
1. Open `http://localhost:3000` to view the **Overview Dashboard**.
2. Click **Run Analysis** in the top navigation bar to trigger signal detection.
3. Navigate to **Cross-Metric Engine** to inspect the cascading risk cluster in the North region.
4. Navigate to **Interactive Risk Map** to explore segment nodes and telemetry drawers.
5. Open **What-If Analysis** to drag sensitivity sliders and recalculate financial impacts.
6. Open **Reports & Export** to download the audit-ready executive PDF report.

---

## 18. Running Automated Tests
Run the automated pytest suite from the repository root:
```bash
python -m pytest backend/tests/test_api.py -v
```
**Test Results**: 12 passed in 3.09s (Health check, database status transparency, dataset schemas, previews, anomaly detection, cross-metric engine, evaluation metrics, what-if simulator, assistant chat tool, investigation persistence, and PDF/JSON/CSV report downloads).

---

## 19. Evaluating Anomaly Detection
Evaluate SignalFire against the baseline detector:
```bash
python -c "from backend.app.main import DATASETS_CACHE, evaluator; import json; print(json.dumps(evaluator.evaluate(DATASETS_CACHE), indent=2))"
```
**Empirical Evaluation Results**:
- **SignalFire Multi-Metric Robust Detector**: Precision = **71.4%** | Recall = **100.0%** | F1-Score = **0.833** (0 False Negatives across all injected crises).
- **Simple Percent-Change Baseline Detector**: Precision = **45.5%** | Recall = **100.0%** | F1-Score = **0.625** (Suffers 6 False Positives from weekend volume noise).

---

## 20. Deployment Instructions
To run the full stack (Exasol Personal, Backend, Frontend) via Docker Compose:
```bash
docker-compose up --build
```

---

## 21. Known Limitations
- **Synthetic Data**: Benchmark evaluations are conducted against synthetic distributions; non-stationary production data will require ongoing threshold recalibration.
- **Correlation vs. Causation**: Statistical association does not exclude unobserved external confounders (e.g. extreme weather events).
- **Exasol Memory Footprint**: Running Exasol Personal locally requires 4–8 GB of RAM; DuckDB provides an instant zero-overhead alternative.

---

## 22. Security Considerations
- **No Arbitrary Code/SQL Execution**: CSV uploads are validated and ingested via pandas DataFrames; uploaded strings are never executed as code or dynamic SQL.
- **Upload Restrictions**: Enforces a 25MB ceiling and verifies CSV file headers.
- **Credential Hygiene**: Database credentials and API keys are loaded via environment variables and never exposed to client bundles.

---

## 23. Future Improvements
- Multi-node Exasol cluster support for multi-billion record datasets.
- Multimodal customer support transcript ingestion via embedding models.
- Automated ERP webhook triggers (SAP, NetSuite) for partner SLA penalty enforcement.

---

## 24. Deliverables Manifest
- **Editable PowerPoint Deck**: `deliverables/pitch_deck.pptx`
- **PDF Pitch Deck**: `deliverables/pitch_deck.pdf`
- **Three-Minute Video Script**: `docs/demo_script.md`
- **Executive PDF Report**: `deliverables/signalfire_executive_report.pdf`
- **Structured Findings JSON**: `deliverables/signalfire_investigation_report.json`
- **Tabular Findings CSV**: `deliverables/signalfire_findings.csv`

---

## 25. License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
