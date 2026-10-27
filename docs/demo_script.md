# SIGNALFIRE AI — Three-Minute Demonstration Video Script

**Product:** SIGNALFIRE AI  
**Tagline:** *Find the warning signs hidden across your data.*  
**Duration:** Exactly 3:00 Minutes  
**Demonstration Domain:** Retail Operations & Supply Chain Telemetry  

---

## Screen Recording Checklist & Setup
- [ ] Screen resolution set to 1920x1080 (16:9).
- [ ] Browser zoom set to 100% in Chrome/Edge, Light Theme enabled.
- [ ] Backend running on `http://127.0.0.1:8000` with preloaded synthetic retail data.
- [ ] Frontend running on `http://localhost:3000`.
- [ ] Microphone tested and background noise minimized.

---

## Timestamped Narration & UI Action Sequence

### 0:00 – 0:20 | Introduction & The Operational Problem
- **Voiceover:**  
  *"Retail operations teams often struggle to identify emerging operational problems because sales, inventory, delivery, refund, and customer complaint data are analyzed separately. Small changes across individual metrics may appear harmless, even when their combined pattern indicates a developing catastrophe. Manually reviewing these datasets is time-consuming and depends heavily on predefined alerts. Welcome to SIGNALFIRE AI—designed to discover unusual cross-metric patterns, investigate supporting evidence, and prioritize potential operational risks before they escalate."*
- **UI Actions:**
  1. Open the **Overview Dashboard** (`http://localhost:3000`).
  2. Hover smoothly over the KPI cards: Total Records (17,216+), Critical Findings, and Cross-Metric Clusters.
  3. Highlight the **Active Analytical Engine Badge** showing live database connectivity.

---

### 0:20 – 0:45 | Relational Telemetry & Data Explorer
- **Voiceover:**  
  *"Behind SIGNALFIRE AI is an enterprise data model spanning eight interconnected tables: sales, orders, deliveries, customer complaints, refunds, inventory, suppliers, and customer retention cohorts. In the Data Explorer, analysts can profile field distributions, check null percentages, preview records, or validate custom CSV imports safely without risk of code injection."*
- **UI Actions:**
  1. Click **Data Explorer** in the sidebar.
  2. Switch between the `deliveries`, `customer_complaints`, and `refunds` tabs.
  3. Show the **Schema Inspector** highlighting field types and null distributions.
  4. Click **Relationships** in the sidebar to reveal foreign key linkages and temporal candidate alignments.

---

### 0:45 – 1:20 | Signal Detection & Statistical Rigor
- **Voiceover:**  
  *"Traditional dashboards alert on arbitrary static thresholds that trigger constant false alarms during weekend volume spikes. SIGNALFIRE AI implements a robust analytical detection engine combining Median Absolute Deviation (MAD), Interquartile Range (IQR) fences, and rolling medians. Clicking 'Run Analysis' isolates genuine statistical outliers across regions."*
- **UI Actions:**
  1. Click the **Run Analysis** button in the top navigation bar.
  2. Navigate to **Signal Detection** in the sidebar.
  3. Filter by `CRITICAL` severity to show the delivery delay spike in the `North` region (+325%, Robust Z = 4.2).
  4. Click **Inspect Evidence** on the North delivery finding to open the modal detailing observed vs baseline values and detection methodology.

---

### 1:20 – 1:55 | Cross-Metric Investigation & Control Cohorts (The Core Differentiator)
- **Voiceover:**  
  *"Here is our central breakthrough: the Cross-Metric Investigation Engine. Rather than treating this delay as an isolated logistics ticket, SIGNALFIRE AI aligns signals across tables by time and segment. It uncovers a cascading failure in the North region: transit delays preceded a 3.5x surge in customer complaints and an 11% refund rate spike with an empirical lead-lag offset of three days (Pearson r = 0.89). Crucially, the system contrasts the North region against unaffected control cohorts—South, East, and West—proving this is a localized carrier hub failure rather than macro market seasonality. In accordance with our core principle, observed facts, statistical associations, and hypotheses are strictly separated—correlation is never presented as proven causation."*
- **UI Actions:**
  1. Navigate to **Cross-Metric Engine** in the sidebar.
  2. Point out the **Pearson correlation (r = 0.89, p < 0.001)** and **~3-day lead-lag offset**.
  3. Highlight the **Control Cohort Benchmarking Card** comparing North (anomalous) against South/East/West (normal baseline).
  4. Scroll down through the disciplined separation: *1. Observed Facts*, *2. Statistical Associations*, *3. Formulated Hypotheses*, and *4. Competing Explanations*.

---

### 1:55 – 2:25 | Interactive Risk Map & Investigation Workspace
- **Voiceover:**  
  *"Analysts can explore these connections topographically on the Interactive Risk Map. Clicking the North node reveals its composite risk index of 88 out of 100. From there, analysts transition to the Investigation Workspace to update finding statuses, assign operational priorities (P1), log suspected root causes, record verified audit conclusions, and track remediation tickets directly within the persistent database layer."*
- **UI Actions:**
  1. Click **Interactive Risk Map** in the sidebar.
  2. Click on the pulsating red **North Region** node to inspect its telemetry drawer.
  3. Click **Investigation Workspace** in the sidebar.
  4. Select finding `SIG-DELIV-NORTH`, set status to **Confirmed**, priority to **P1**, and click **Save Investigation Record** (show success toast).

---

### 2:25 – 2:45 | What-If Scenario Analysis & Executive Reporting
- **Voiceover:**  
  *"To support executive decision-making, our What-If Analysis workspace allows operators to adjust parameters—such as increasing transit delays by 20% or refund rates by 2%—to recalculate financial impacts while explicitly separating direct arithmetic consequences from model-based projections. Once evaluated, analysts can download audit-ready executive PDF reports, structured JSON manifests, or CSV spreadsheets with one click."*
- **UI Actions:**
  1. Click **What-If Analysis** in the sidebar.
  2. Drag the **Delivery Delay Shift** slider to +25% and observe the live recalculation.
  3. Navigate to **Reports & Export** in the sidebar.
  4. Click **Download Executive PDF** and open the generated ReportLab PDF to display its clean publication layout.

---

### 2:45 – 3:00 | Exasol Personal Architecture & Closing Statement
- **Voiceover:**  
  *"SIGNALFIRE AI is architected for enterprise scale with a native Exasol Personal integration via pyexasol for high-throughput in-memory SQL analytics, backed by a transparent DuckDB local engine for seamless development. By connecting the warning signs hidden across your operational data, SIGNALFIRE AI helps organizations act before problems become crises. Thank you."*
- **UI Actions:**
  1. Navigate to **Settings & Exasol** in the sidebar.
  2. Show the **Exasol Connection Form**, **Active Backend Transparency Indicator**, and **Setup Guide**.
  3. End on the clean, glassmorphic **Overview Dashboard**.
