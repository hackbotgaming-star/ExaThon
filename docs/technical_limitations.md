# SIGNALFIRE AI — Technical Limitations & Methodological Boundaries

In alignment with our core engineering principles, SIGNALFIRE AI never claims unverified capabilities, fabricates metrics, or overstates analytical conclusions. This document details the architectural and statistical boundaries of the current system.

---

## 1. Correlation vs. Proven Causation
- **Empirical Boundary**: The Cross-Metric Investigation Engine identifies temporal co-occurrences, compute Pearson and Spearman correlation coefficients ($r$), and estimates lead-lag offsets across datasets.
- **Principle**: *Correlation does not prove causation.* A high statistical correlation between delivery delays and customer refunds does not exclude third-variable confounders (such as extreme local weather disruptions, holiday promotion surges, or simultaneous catalog pricing alterations).
- **Enforcement**: The application strictly categorizes discoveries into **Observed Facts**, **Statistical Associations**, **Hypotheses**, **Competing Explanations**, and **Recommendations**. Analysts must audit external operational logs before executing punitive commercial decisions against suppliers or carriers.

---

## 2. Synthetic Data Evaluation Limitations
- **Evaluation Context**: The benchmark evaluation metrics (Precision: 71.4%, Recall: 100.0%, F1: 0.833) are measured against known synthetic anomalies injected into an 8-table retail simulation.
- **Limitations**:
  - Synthetic data distributions exhibit cleaner stationarity than real-world enterprise telemetry, which is subject to irregular macro shocks, tracking outages, and manual data-entry errors.
  - Injected anomalies were modeled with explicit onset timelines. Real-world operational drift may develop more gradually, potentially increasing detection latency from 1–3 days to 4–7 days.
  - The demonstration domain is retail and supply chain operations. While the statistical methodologies (MAD, IQR, lead-lag alignment) are domain-agnostic, schema mappers must be tailored for financial fraud, healthcare logistics, or IoT telemetry.

---

## 3. Multiple Comparisons & False Discovery Control
- When evaluating hundreds of permutations across tables, SKUs, and geographic territories, the probability of false positives increases (the *look-elsewhere effect*).
- SIGNALFIRE AI mitigates this through:
  1. Non-parametric Median Absolute Deviation (MAD) scaling ($1.4826 \times \text{MAD}$).
  2. Aggregated segment-level grouping rather than unconstrained point-by-point scanning.
  3. Requiring temporal co-occurrence across at least two independent datasets before escalating a signal to a Cross-Metric Risk Cluster.
- Future enterprise releases will incorporate formal Benjamini-Hochberg False Discovery Rate (FDR) adjustments for multi-million SKU environments.

---

## 4. What-If Scenario Boundaries
- The What-If Analysis workspace explicitly separates **Direct Arithmetic Consequences** (e.g. gross revenue shifts directly multiplied by demand percentage adjustments) from **Model-Based Behavioral Elasticities** (e.g. customer complaint rates modeled as a linear function of transit delay).
- Stated boundaries:
  - Assumes uniform average order values across product lines.
  - Assumes linear elasticity within reasonable test bounds ($\pm 30\%$). Extreme operational stress (e.g. $+300\%$ transit delays) may trigger non-linear churn tipping points.

---

## 5. Exasol Personal Connectivity & Fallback
- While native Exasol integration via `pyexasol` is fully implemented and tested, running Exasol Personal locally requires approximately 4–8 GB of RAM and Docker privileges.
- When Exasol is not configured or reachable, the application seamlessly activates DuckDB Local. The active engine is prominently displayed in the UI and API responses to guarantee complete architectural transparency.
