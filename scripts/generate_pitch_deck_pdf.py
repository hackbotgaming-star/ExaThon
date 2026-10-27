import os
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_deck(output_path: str = "deliverables/pitch_deck.pdf"):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DeckTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold'
    )
    tag_style = ParagraphStyle(
        'DeckTag',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#6366f1'),
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'DeckSub',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#64748b')
    )
    body_style = ParagraphStyle(
        'DeckBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )
    h2_style = ParagraphStyle(
        'DeckH2',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        fontName='Helvetica-Bold'
    )

    story = []

    slides = [
        ("EXATHON 2026 HACKATHON ENTRY", "SIGNALFIRE AI", "Find the warning signs hidden across your data.",
         ["<b>Category:</b> AI-Powered BI, Anomaly Detection & Cross-Dataset Risk Discovery",
          "<b>Core Idea:</b> Unifies fragmented data silos, detects multi-metric lead-lag cascades, and formulates evidence-backed investigation hypotheses.",
          "<b>Analytical Architecture:</b> Native Exasol Personal integration via pyexasol with local in-process DuckDB fallback.",
          "<b>Demonstration Domains:</b> Retail Logistics & Industrial MRO Equipment Reliability."]),

        ("PROBLEM STATEMENT", "The Cost of Monitoring in Departmental Silos", "Why isolated dashboards fail to catch emerging systemic operational crises",
         ["• <b>Disjointed Data Silos:</b> Fulfillment delays, customer complaints, refunds, and machinery telemetry are reviewed in silos.",
          "• <b>The Lead-Lag Blind Spot:</b> Incidents unfold as multi-day chains (Carrier Delay Day 50 -> Complaints Day 52 -> Returns Day 54).",
          "• <b>Alert Fatigue & False Alarms:</b> Static >25% change thresholds trigger relentless false alarms during normal demand cycles.",
          "• <b>Compounding Financial Impact:</b> By the time executive dashboards alert, irreparable customer churn and downtime have occurred."]),

        ("PRODUCT ARCHITECTURE", "Cross-Dataset Intelligence & Epistemic Rigor", "Rigorous epistemic separation between facts, statistical associations, and hypotheses",
         ["• <b>Observed Facts:</b> Deterministic data points directly computed from verified database records (e.g. 2.78-day delay).",
          "• <b>Statistical Associations:</b> Empirical Pearson ($r=0.89$) and Spearman correlation coefficients with automated lead-lag offsets.",
          "• <b>Hypotheses & Alternative Explanations:</b> Structured explanations for human investigation; explicitly tracks competing confounders.",
          "• <b>Core Epistemic Mandate:</b> Never presents statistical correlation as proven causation.",
          "• <b>Targeted Action Playbooks:</b> Proactive remediation steps (carrier SLA audit, supplier buffer prioritization)."]),

        ("DOMAIN VALIDATION", "Dual-Domain Operational Demonstrations", "Proving multi-metric lead-lag discovery across Retail and Industrial MRO sectors",
         ["• <b>Retail Logistics (North Hub Breakdown):</b> Transit delays surge from 0.10d to 2.78d (+2,568%) -> Customer complaints surge +961% -> Refund disbursements jump +276% ($14,200 loss).",
          "• <b>Industrial MRO (Plant Alpha Stamping Press):</b> RMS vibration velocity surges from 2.1 to 8.4 mm/s (ISO 10816-3 breach) -> Overdue PM backlog surges 3.8x -> Bearing stockout -> Catastrophic 46.5-hr stoppage ($280k loss).",
          "• <b>Control Cohorts:</b> Contrasted against unaffected cohorts (South/East/West; Plant Beta/Gamma) to isolate localized root causes."]),

        ("HIGH-PERFORMANCE ANALYTICS", "Exasol Personal Analytical Integration", "In-memory column-store analytical SQL with zero-downtime DuckDB fallback transparency",
         ["• <b>Official pyexasol Driver:</b> Native WebSocket JSON-RPC connection executing high-throughput analytical rollups and aggregations.",
          "• <b>Database Adapter Pattern:</b> Polymorphic abstraction completely isolates analytics from storage, switching between Exasol and DuckDB.",
          "• <b>Strict Transparency Mandate:</b> Real-time database status indicator in top navigation bar; local calculations are NEVER labeled as Exasol-powered.",
          "• <b>Zero-Friction Offline Evaluation:</b> Judges can evaluate the full application offline without Docker via DuckDB."]),

        ("EMPIRICAL BENCHMARKS", "Ground-Truth Evaluation & Accuracy Benchmark", "Audited performance comparison against a traditional static percent-change baseline",
         ["• <b>SIGNALFIRE AI (Robust MAD & IQR):</b> Precision = 70.0% | Recall = 77.8% | F1-Score = 0.737 | False Positives = 3.",
          "• <b>Traditional Baseline (>30% Change Rule):</b> Precision = 42.9% | Recall = 75.0% | F1-Score = 0.545 | False Positives = 8.",
          "• <b>Key Advantage:</b> SignalFire's non-parametric Median Absolute Deviation fences filter cyclical demand noise while catching true multi-metric crises.",
          "• <b>Automated Pytest Suite:</b> 12/12 unit and integration tests passing in 3.09s."]),

        ("UI/UX & VISUAL ENGINEERING", "Enterprise 3D Glassmorphism & Working 3D Effects", "Tactile, refined interface interactions designed to enhance data comprehension",
         ["• <b>Interactive 3D Risk Universe:</b> Real-time HTML5 3D Canvas with drag-to-rotate pitch/yaw controls, auto-orbiting, and live telemetry HUD.",
          "• <b>Real-Time 3D Gyro Tilt:</b> Dashboard cards physically tilt in 3D perspective based on mouse position with dynamic holographic specular light glare.",
          "• <b>3D Modal Parallax:</b> Deep inspection modal card dynamically responds to mouse gyro coordinates with embossed tactile KPI tiles.",
          "• <b>Custom 3D Glass Scrollbars:</b> Slim 7px gradient floating pill scrollbars across modal and table containers."]),

        ("DECISION SUPPORT", "Decision Support & What-If Sensitivity Simulator", "Translating detected signals into verified conclusions and simulated financial risk",
         ["• <b>Dual-Domain What-If Simulator:</b> Interactive sensitivity sliders for Retail (delay %, return %, demand %, inventory %) and Industrial MRO (vibration %, PM backlog %, parts lead time, hourly cost).",
          "• <b>Methodological Boundary:</b> Separates direct arithmetic calculations from model-based behavioral projections and stated engineering assumptions.",
          "• <b>Investigation Workspace:</b> Decision-support ticket manager allowing analysts to assign operational priorities (P1-P3) and record audit conclusions.",
          "• <b>Tool-Grounded AI Assistant:</b> Conversational analyst retrieving verified evidence from database queries, preventing hallucinations."]),

        ("MARKET POSITIONING", "Competitive Advantage: Beyond Siloed BI", "Why traditional enterprise dashboards leave millions in unaddressed operational risk",
         ["• <b>Traditional BI (Tableau/PowerBI):</b> Sits on static data, requires manual cross-filtering, lacks automated lead-lag discovery and epistemic rigor.",
          "• <b>APM / Monitoring (Datadog/PagerDuty):</b> Focuses on infrastructure uptime, relies on noisy static thresholds, misses cross-table business cascades.",
          "• <b>SIGNALFIRE AI Advantage:</b> Automated multi-dataset correlation ($r=0.89$), noise-robust MAD normalization, control cohort benchmarking, and what-if simulation in one unified platform."]),

        ("CONCLUSION & ROADMAP", "Delivering Operational Resilience", "Transforming hidden warning signs into proactive business interventions",
         ["• <b>What We Built & Verified:</b> Complete full-stack system, 13 datasets (60,653+ records), interactive 3D universe, 3D glassmorphism, 12/12 passing tests.",
          "• <b>Near-Term Horizon:</b> Multi-node Exasol cluster deployment for multi-billion record datasets.",
          "• <b>Multimodal Signal Ingestion:</b> Embedding vectors for customer call audio transcripts and technician maintenance notes.",
          "• <b>Automated ERP Enforcement:</b> SAP and NetSuite webhook triggers for automatic vendor SLA penalty clawbacks upon confirmed lead-lag breach."])
    ]

    for idx, (tag, title, sub, points) in enumerate(slides):
        story.append(Paragraph(tag.upper(), tag_style))
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(sub, subtitle_style))
        story.append(Spacer(1, 14))

        for pt in points:
            story.append(Paragraph(pt, body_style))
            story.append(Spacer(1, 8))

        if idx < len(slides) - 1:
            story.append(PageBreak())

    doc.build(story)
    print(f"Successfully generated PDF pitch deck at: {output_path}")

if __name__ == "__main__":
    generate_pdf_deck()
