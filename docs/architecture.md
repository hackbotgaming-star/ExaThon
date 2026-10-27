# SIGNALFIRE AI — Technical Architecture Documentation

## 1. System Overview
**SIGNALFIRE AI** is an AI-powered business intelligence, cross-dataset risk discovery, and decision-support platform designed for enterprise retail and supply chain operations.

Traditional dashboards visualize metrics independently (e.g. sales in one view, delivery SLA in another, customer complaints in a support portal). When operational breakdowns occur, early warning signs frequently manifest as subtle, co-occurring shifts across multiple disparate tables before triggering any single metric's critical threshold.

SIGNALFIRE AI resolves this by:
1. Ingesting multi-dataset operational streams into an analytical storage engine (Exasol Personal or local DuckDB OLAP).
2. Applying noise-resistant statistical anomaly detectors (Robust Z-scores via Median Absolute Deviation, Interquartile Range fences, rolling medians).
3. Aligning anomalies temporally and across business segments to discover cross-metric clusters.
4. Contrasting incident segments against unaffected control cohorts.
5. Computing empirical correlation coefficients and lead-lag time offsets.
6. Enforcing a disciplined separation of **Observed Facts**, **Statistical Associations**, **Hypotheses**, **Competing Explanations**, and **Recommendations**—never presenting correlation as proven causation.

---

## 2. High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                           SIGNALFIRE AI ARCHITECTURE                              |
+-----------------------------------------------------------------------------------+

 [CLIENT LAYER]
   │
   ├── React 18 + TypeScript + Vite
   ├── Tailwind CSS + Custom 3D Glassmorphism Design Language
   ├── Recharts (Area, Donut, Timeline Visualizations)
   └── Lucide Enterprise Icons
   │
   ▼ HTTP / JSON (RESTful API, Proxy Port 3000 -> 8000)
 [API & ORCHESTRATION LAYER]
   │
   ├── FastAPI (Asynchronous Python 3.12 Web Service)
   ├── Pydantic v2 (Strict Schema Validation & Serialization)
   ├── Session Caches & Health Monitors
   └── Ingestion Safeguards (25MB File Cap, Schema Verification, No Code/SQL Execution)
   │
   ▼
 [ANALYTICAL & STATISTICAL SERVICES]
   │
   ├── Signal Detection Engine (detector.py)
   │     • Robust Z-Score via Median Absolute Deviation (MAD)
   │     • Interquartile Range (IQR) Non-Parametric Outlier Fences
   │     • Rolling-Window Median Delta & Segment Normalization
   │
   ├── Cross-Metric Investigation Engine (cross_metric.py) [CORE DIFFERENTIATOR]
   │     • Temporal & Segment Cross-Dataset Alignment
   │     • Pearson & Spearman Correlation (Scipy / NumPy)
   │     • Lead-Lag Offset Synchronization (~3 Day Lag Discovery)
   │     • Control Cohort Contrast (North vs South, East, West)
   │     • Disciplined 5-Part Evidence Separation
   │
   ├── Ground Truth Evaluator (evaluator.py)
   │     • Evaluates SignalFire vs Baseline against Synthetic Ground Truth
   │     • Real Confusion Matrix (Precision, Recall, F1-Score)
   │
   ├── What-If Scenario Engine (what_if.py)
   │     • Parameterized Sensitivity Modeling
   │     • Explicit Separation of Direct Arithmetic vs Model Projections
   │
   ├── Evidence-Backed AI Assistant (assistant.py)
   │     • Tool-Grounded Query Resolution (Deterministic Tool Execution)
   │     • Zero Metric Hallucination Guarantee
   │
   └── Executive Report Generator (report_generator.py)
         • ReportLab PDF Compiler
         • Structured JSON & Tabular CSV Exporters
   │
   ▼
 [DATABASE ADAPTER LAYER (manager.py)]
   │
   ├── Abstract DatabaseAdapter Interface (base.py)
   │
   ├── ExasolAdapter (exasol_adapter.py) [PRIMARY ANALYTICAL DATABASE]
   │     • Official pyexasol Driver (WebSocket JSON-RPC Protocol)
   │     • Fast pandas import/export & In-Memory Analytical SQL
   │     • Live Health Check & Latency Telemetry
   │     • Configurable Credentials (EXASOL_DSN, EXASOL_USER, EXASOL_PASSWORD)
   │
   └── DuckDBAdapter (duckdb_adapter.py) [LOCAL DEVELOPMENT FALLBACK]
         • High-Performance In-Process Columnar OLAP Engine
         • Full SQL Schema Compatibility
         • Instant Offline Startup & Demo Capabilities
```

---

## 3. Database Layer & Exasol Integration

A core requirement of SIGNALFIRE AI is meaningful integration with **Exasol Personal**, the high-performance in-memory analytical database.

### Database Adapter Design Pattern
To preserve architectural separation and ensure that the application never depends on hardcoded storage implementations, all data access flows through the abstract `DatabaseAdapter` interface:

```python
class DatabaseAdapter(ABC):
    @property
    def backend_name(self) -> str: ...
    @property
    def is_connected(self) -> bool: ...
    def connect(self) -> bool: ...
    def disconnect(self) -> None: ...
    def health_check(self) -> Dict[str, Any]: ...
    def execute_query(self, sql: str, params: Optional[Dict] = None) -> List[Dict]: ...
    def execute_df(self, sql: str, params: Optional[Dict] = None) -> pd.DataFrame: ...
    def load_table(self, table_name: str, df: pd.DataFrame, if_exists: str = "replace") -> int: ...
    def list_tables(self) -> List[str]: ...
    def get_table_schema(self, table_name: str) -> List[Dict]: ...
```

### Exasol Adapter (`ExasolAdapter`)
- Connects to Exasol instances using `pyexasol`.
- Communicates via WebSocket JSON-RPC over port 8563.
- Executes analytical rollups and multi-table queries.
- Ingests DataFrames using Exasol's native bulk loading protocol.
- Measures live roundtrip connection latency and verifies Exasol metadata versions (`SYS.EXA_METADATA`).

### Local Development Adapter (`DuckDBAdapter`)
- When Exasol is offline or credentials are not supplied in `.env`, the system automatically activates DuckDB.
- Executes analytical queries using vectorized SIMD-accelerated SQL.
- Guarantees 100% demo functionality on any machine without requiring external Docker services.

### Transparency Principle
The active database engine is visibly badged in the navigation header, the Overview Dashboard, the API health endpoint, and all generated reports. The application **never** misrepresents local calculations as Exasol-powered.

---

## 4. Analytical Detection Logic

### Robust Z-Scores via Median Absolute Deviation (MAD)
Standard z-scores rely on mean and standard deviation, both of which are severely corrupted by the very anomalies they aim to detect. SIGNALFIRE AI calculates the Median Absolute Deviation:

$$\text{MAD} = \text{median}(|X_i - \text{median}(X)|)$$

$$\text{Robust } Z = \frac{X_i - \text{median}(X)}{1.4826 \times \text{MAD}}$$

### Interquartile Range (IQR) Fences
For skewed operational metrics (e.g. inventory stockouts, customer return counts), non-parametric quartile fences are evaluated:

$$\text{Upper Fence} = Q_3 + 1.75 \times (Q_3 - Q_1)$$

---

## 5. Security & Reliability Controls
- **Zero Arbitrary Execution:** CSV uploads are parsed strictly as tabular data through pandas; no code or unparameterized SQL is ever executed.
- **Upload Safety:** Enforces a 25MB file size ceiling and validates file extensions and delimiters.
- **Credential Protection:** Secrets are never hardcoded, never bundled into frontend assets, and never echoed back in health responses.
- **Deterministic AI Assistant:** Operates via tool-directed queries rather than open-ended SQL generation, preventing SQL injection or numerical hallucinations.
