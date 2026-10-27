# SIGNALFIRE AI — Deployment & Run Guide

This guide provides instructions for running SIGNALFIRE AI locally for development, evaluating it against synthetic data, connecting it to an Exasol Personal database instance, or running it via Docker.

---

## 1. Prerequisites
- **Python**: 3.11 or 3.12 installed.
- **Node.js**: v18+ (tested on Node v20/v24).
- **npm**: 9.x+ (tested on npm 11.x).
- **Docker** *(Optional)*: Required only if running Exasol Personal in a local container or deploying via Docker Compose.

---

## 2. Environment Configuration

Copy the sample environment file:
```bash
cp .env.example .env
```

### Environment Variables Overview
```ini
# --- Analytical Storage Configuration ---
# If EXASOL_DSN is omitted or unreachable, SIGNALFIRE AI runs on DuckDB Local automatically.
EXASOL_DSN=localhost:8563
EXASOL_USER=sys
EXASOL_PASSWORD=exasol
EXASOL_SCHEMA=SIGNALFIRE
EXASOL_TIMEOUT=5

# --- Local Fallback Database ---
DUCKDB_PATH=signalfire_local.duckdb

# --- Server Ports ---
BACKEND_PORT=8000
FRONTEND_PORT=3000

# --- Optional AI Assistant LLM Key ---
# When omitted, the assistant operates in Deterministic Tool-Engine Mode with zero hallucinations.
# OPENAI_API_KEY=
# GEMINI_API_KEY=
```

---

## 3. Running Exasol Personal (Optional)

To start an official Exasol Personal analytical instance using Docker:

```bash
docker run --name exasol-personal \
  -p 8563:8563 \
  --privileged \
  -d exasol/docker-db:latest
```

Wait approximately 45–60 seconds for the database to complete startup. You can test connectivity directly inside the SIGNALFIRE AI Settings page or via `pyexasol`.

*Note: If Exasol is not running, SIGNALFIRE AI will transparently run using the local DuckDB adapter. The UI and API clearly indicate which engine is active.*

---

## 4. Local Development Startup (Recommended)

### Step 1: Install Dependencies
From the repository root:

```bash
# Install backend Python packages
pip install fastapi pydantic duckdb pyexasol python-pptx pytest reportlab scikit-learn pandas numpy uvicorn

# Install frontend Node dependencies
cd frontend
npm install
cd ..
```

### Step 2: Start Backend API Server
```bash
# From repository root
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
The FastAPI backend will start on `http://127.0.0.1:8000`.  
Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`.

### Step 3: Start Frontend Dev Server
Open a separate terminal window:
```bash
cd frontend
npm run dev
```
The React/Vite development server will start on `http://localhost:3000`.

---

## 5. Running Automated Backend Tests

SIGNALFIRE AI includes a comprehensive pytest suite covering all endpoints, statistical anomaly detection, cross-metric investigation, ground-truth evaluation, what-if analysis, and report generation.

From the repository root:
```bash
python -m pytest backend/tests/test_api.py -v
```

All 12 tests should report `PASSED`.

---

## 6. Running with Docker Compose

A multi-container `docker-compose.yml` is provided for containerized execution:

```bash
docker-compose up --build
```

This starts:
- `backend`: FastAPI API on port 8000
- `frontend`: Vite preview on port 3000
- `exasol`: Exasol Personal container on port 8563 (pre-configured)

---

## 7. Generating Hackathon Deliverables

Deliverables (pitch deck slides, executive PDF reports) can be regenerated at any time using:

```bash
# Generate PowerPoint (PPTX) and PDF pitch decks:
python scripts/generate_pitch_deck.py

# Re-generate synthetic datasets:
python data/generation/generate_retail_data.py
```
Outputs are placed in the `deliverables/` directory:
- `deliverables/pitch_deck.pptx`
- `deliverables/pitch_deck.pdf`
- `deliverables/signalfire_executive_report.pdf`
- `deliverables/signalfire_findings.csv`
- `deliverables/signalfire_investigation_report.json`
