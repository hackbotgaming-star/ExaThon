import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str = "deliverables/pitch_deck.pptx"):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Palette
    NAVY = RGBColor(15, 23, 42)       # #0f172a
    SLATE = RGBColor(100, 116, 139)   # #64748b
    INDIGO = RGBColor(99, 102, 241)   # #6366f1
    CYAN = RGBColor(2, 132, 199)      # #0284c7
    RED = RGBColor(239, 68, 68)       # #ef4444
    EMERALD = RGBColor(16, 185, 129)  # #10b981
    AMBER = RGBColor(245, 158, 11)    # #f59e0b
    BG_LIGHT = RGBColor(248, 250, 252) # #f8fafc
    WHITE = RGBColor(255, 255, 255)
    BORDER_LIGHT = RGBColor(226, 232, 240)

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()
        return bg

    def add_header(slide, tag: str, title: str, subtitle: str):
        # Category Tag Pill
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = INDIGO

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = "Arial"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.5), Inches(0.5))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = SLATE

    def add_card(slide, left, top, width, height, title="", border_color=BORDER_LIGHT, bg_color=WHITE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
            p = tb.text_frame.paragraphs[0]
            p.text = title
            p.font.name = "Arial"
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = NAVY
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    # Accent decorative background pill
    dec = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.733), Inches(5.1))
    dec.fill.solid()
    dec.fill.fore_color.rgb = WHITE
    dec.line.color.rgb = BORDER_LIGHT
    dec.line.width = Pt(1.5)

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(11), Inches(4.3))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "EXATHON 2026 HACKATHON ENTRY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INDIGO

    p = tf1.add_paragraph()
    p.text = "SIGNALFIRE AI"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Find the warning signs hidden across your data."
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p.space_before = Pt(6)

    p = tf1.add_paragraph()
    p.text = (
        "An enterprise decision-support platform that unifies fragmented operational telemetry, "
        "detects cross-dataset lead-lag risk cascades, and provides evidence-grounded investigation support. "
        "Powered by Exasol Personal with local DuckDB in-process OLAP fallback."
    )
    p.font.size = Pt(13)
    p.font.color.rgb = SLATE
    p.space_before = Pt(14)

    p = tf1.add_paragraph()
    p.text = "Domain Demonstrations: Retail Commerce Logistics & Industrial MRO Equipment Reliability"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_before = Pt(18)

    # ==========================================
    # SLIDE 2: THE OPERATIONAL BLIND SPOT (PROBLEM)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Problem Statement", "The Cost of Monitoring in Departmental Silos",
               "Why isolated dashboards fail to catch systemic operational crises before they escalate")

    # 3 Problem Pillars
    col_w = Inches(3.64)
    h = Inches(4.6)
    c1 = add_card(s2, Inches(0.8), Inches(2.0), col_w, h, "1. Disjointed Data Silos")
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.7), col_w - Inches(0.4), h - Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Delivery, complaint, inventory, refund, and telemetry streams are analyzed separately."
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.color.rgb = SLATE
    p = tf.add_paragraph()
    p.text = "When viewed independently, small incremental shifts appear as harmless routine variance, concealing the developing crisis."
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE
    p.space_before = Pt(10)

    c2 = add_card(s2, Inches(4.84), Inches(2.0), col_w, h, "2. The Lead-Lag Blind Spot")
    tb = s2.shapes.add_textbox(Inches(5.04), Inches(2.7), col_w - Inches(0.4), h - Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Operational failures unfold as temporal chains: Carrier Delay (Day 50) -> Complaint Surge (Day 52) -> Return Wave (Day 54)."
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.color.rgb = SLATE
    p = tf.add_paragraph()
    p.text = "Traditional dashboards fail to link upstream causes to downstream symptoms across multi-day offsets."
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE
    p.space_before = Pt(10)

    c3 = add_card(s2, Inches(8.88), Inches(2.0), col_w, h, "3. Alert Fatigue & Noise")
    tb = s2.shapes.add_textbox(Inches(9.08), Inches(2.7), col_w - Inches(0.4), h - Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Static percentage-change rules (e.g. >25% change) trigger relentless false alarms during normal demand cycles."
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.color.rgb = SLATE
    p = tf.add_paragraph()
    p.text = "Analysts suffer alert fatigue, silencing notifications until catastrophic customer churn or plant downtime occurs."
    p.font.size = Pt(12)
    p.font.color.rgb = SLATE
    p.space_before = Pt(10)

    # ==========================================
    # SLIDE 3: THE SOLUTION & CORE PRINCIPLE
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Product Architecture", "SIGNALFIRE AI: Cross-Dataset Intelligence",
               "Discovering interconnected risk cascades with strict epistemic rigor")

    # Left: Epistemological Architecture
    add_card(s3, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.6), "Strict Epistemological Separation")
    tb = s3.shapes.add_textbox(Inches(1.0), Inches(2.65), Inches(5.2), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    bullets = [
        ("Observed Facts: ", "Deterministic data values directly computed from verified database records (e.g. 2.78-day delay vs 0.10-day baseline)."),
        ("Statistical Associations: ", "Empirical Pearson & Spearman correlation coefficients ($r = 0.89$) and lead-lag temporal window synchronization."),
        ("Hypotheses: ", "Testable explanations generated for human investigation without jumping to unsupported conclusions."),
        ("Competing Explanations: ", "Explicit identification of alternative confounders (e.g. regional weather disruptions or promo surges)."),
        ("Remediation Actions: ", "Targeted next-step operational playbooks (carrier SLA audit, supplier buffer prioritization)."),
        ("Core Rule: ", "Never presents statistical correlation as proven causation.")
    ]
    for idx, (b_title, b_desc) in enumerate(bullets):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        run1 = p.add_run()
        run1.text = b_title
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = INDIGO if idx == 5 else NAVY
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(11)
        run2.font.color.rgb = SLATE
        if idx > 0:
            p.space_before = Pt(6)

    # Right: The 5-Stage Cross-Metric Pipeline
    add_card(s3, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.6), "5-Stage Analytical Pipeline")
    tb = s3.shapes.add_textbox(Inches(7.0), Inches(2.65), Inches(5.3), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    steps = [
        ("1. Multi-Stream Ingestion: ", "Syncs 13 tables across sales, logistics, inventory, feedback, and telemetry."),
        ("2. Noise-Robust Detection: ", "Filters variance using Median Absolute Deviation (MAD) & Interquartile Ranges (IQR)."),
        ("3. Temporal Lead-Lag Clustering: ", "Identifies multi-day delay offsets between co-occurring anomalies."),
        ("4. Control Cohort Benchmarking: ", "Validates local incident hubs against healthy control cohorts (South/East/West; Plant Beta/Gamma)."),
        ("5. Decision-Support Workspace: ", "Interactive ticket triage (P1-P3), sensitivity simulation, and audit PDF exports.")
    ]
    for idx, (s_title, s_desc) in enumerate(steps):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        run1 = p.add_run()
        run1.text = s_title
        run1.font.bold = True
        run1.font.size = Pt(11.5)
        run1.font.color.rgb = CYAN
        run2 = p.add_run()
        run2.text = s_desc
        run2.font.size = Pt(11.5)
        run2.font.color.rgb = SLATE
        if idx > 0:
            p.space_before = Pt(8)

    # ==========================================
    # SLIDE 4: DUAL-DOMAIN DEMONSTRATION
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Domain Validation", "Dual-Domain Operational Demonstrations",
               "Proving multi-metric lead-lag risk discovery across Retail and Industrial MRO sectors")

    # Domain A: Retail
    add_card(s4, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.6), "Domain A: Retail Logistics & Commerce")
    tb = s4.shapes.add_textbox(Inches(1.0), Inches(2.65), Inches(5.2), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Scenario: Localized North Fulfillment Breakdown (Day 50+)"
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = NAVY

    retail_chain = [
        "Day 50: Carrier transit delays in North surge from 0.10d to 2.78d (+2,568%, Z=56.4).",
        "Day 52 (+2d): Customer service complaints spike +961%, led by 'Delayed Delivery'.",
        "Day 54 (+4d): Refund disbursements escalate +276% ($14,200 return volume).",
        "Day 56 (+6d): Warehouse inventory buffer stockouts jump from 3% to 44%.",
        "Control Benchmark: South, East, and West hubs remain stable, isolating local carrier failure."
    ]
    for item in retail_chain:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE
        p.space_before = Pt(6)

    # Domain B: Industrial MRO
    add_card(s4, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.6), "Domain B: Industrial MRO Equipment")
    tb = s4.shapes.add_textbox(Inches(7.0), Inches(2.65), Inches(5.3), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Scenario: Plant Alpha Mechanical Failure Cascade (Day 48+)"
    tf.paragraphs[0].font.size = Pt(12)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = NAVY

    mro_chain = [
        "Day 48: Stamping press RMS vibration velocity surges from 2.1 to 8.4 mm/s (ISO 10816-3 breach).",
        "Day 50 (+2d): Overdue Preventive Maintenance (PM) work order backlog surges 3.8x baseline.",
        "Day 52 (+4d): Replacement precision roller bearing inventory reaches total exhaustion (0 units).",
        "Day 53 (+5d): Catastrophic bearing seizure triggers 46.5-hr line stoppage ($280k loss).",
        "Control Benchmark: Plants Beta, Gamma, and Delta maintain normal telemetry, ruling out supplier flaw."
    ]
    for item in mro_chain:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE
        p.space_before = Pt(6)

    # ==========================================
    # SLIDE 5: EXASOL PERSONAL INTEGRATION
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "High-Performance Analytics", "Exasol Personal Analytical Integration",
               "In-memory column-store analytical SQL with zero-downtime DuckDB fallback transparency")

    col_w = Inches(3.64)
    c1 = add_card(s5, Inches(0.8), Inches(2.0), col_w, Inches(4.6), "Official pyexasol Driver")
    tb = s5.shapes.add_textbox(Inches(1.0), Inches(2.7), col_w - Inches(0.4), Inches(3.7))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "• Native WebSocket JSON-RPC connection via pyexasol 3.0.1."
    tf.paragraphs[0].font.size = Pt(11.5)
    tf.paragraphs[0].font.color.rgb = SLATE
    for txt in [
        "• High-throughput execution of complex analytical SQL aggregations across multi-table operational schemas.",
        "• Schema bootstrapping and automated CSV table staging.",
        "• Active health monitoring measuring round-trip query latency and SYS.EXA_METADATA versioning."
    ]:
        p = tf.add_paragraph()
        p.text = txt
        p.font.size = Pt(11.5)
        p.font.color.rgb = SLATE
        p.space_before = Pt(8)

    c2 = add_card(s5, Inches(4.84), Inches(2.0), col_w, Inches(4.6), "Database Adapter Architecture")
    tb = s5.shapes.add_textbox(Inches(5.04), Inches(2.7), col_w - Inches(0.4), Inches(3.7))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "• Polymorphic DatabaseAdapter abstraction isolates analytical logic from underlying storage."
    tf.paragraphs[0].font.size = Pt(11.5)
    tf.paragraphs[0].font.color.rgb = SLATE
    for txt in [
        "• Seamless switching between Exasol Personal and DuckDB local in-process OLAP.",
        "• Zero external runtime blocker: hackathon judges can explore the complete application offline without local Docker setup."
    ]:
        p = tf.add_paragraph()
        p.text = txt
        p.font.size = Pt(11.5)
        p.font.color.rgb = SLATE
        p.space_before = Pt(8)

    c3 = add_card(s5, Inches(8.88), Inches(2.0), col_w, Inches(4.6), "Strict Transparency Mandate")
    tb = s5.shapes.add_textbox(Inches(9.08), Inches(2.7), col_w - Inches(0.4), Inches(3.7))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "• Visible real-time database status indicator in top navigation bar."
    tf.paragraphs[0].font.size = Pt(11.5)
    tf.paragraphs[0].font.color.rgb = SLATE
    for txt in [
        "• Clearly reveals active engine: 'Exasol Personal' vs 'DuckDB Local (Fallback)'.",
        "• Local calculations are NEVER labeled as Exasol-powered.",
        "• Production-grade credential hygiene via environment variables (.env)."
    ]:
        p = tf.add_paragraph()
        p.text = txt
        p.font.size = Pt(11.5)
        p.font.color.rgb = SLATE
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 6: EVALUATION & BENCHMARKS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Empirical Validation", "Ground-Truth Evaluation & Accuracy Benchmark",
               "Audited performance comparison against a traditional static percent-change baseline")

    # Metrics Table
    add_card(s6, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.6), "Benchmark Comparison (13 Datasets, 60,653 Records)")

    tb = s6.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(11.3), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Metric Results on Injected Operational Crises:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # Add visual comparison box
    box1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(3.1), Inches(5.2), Inches(3.0))
    box1.fill.solid()
    box1.fill.fore_color.rgb = RGBColor(240, 253, 250)
    box1.line.color.rgb = EMERALD
    tb_b1 = s6.shapes.add_textbox(Inches(1.4), Inches(3.2), Inches(4.8), Inches(2.8))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True
    tf_b1.paragraphs[0].text = "SIGNALFIRE AI (Robust MAD & IQR)"
    tf_b1.paragraphs[0].font.bold = True
    tf_b1.paragraphs[0].font.size = Pt(13)
    tf_b1.paragraphs[0].font.color.rgb = EMERALD
    for line in [
        "• Precision: 70.0% (Suppresses cyclical variance)",
        "• Recall: 77.8% (Catches cross-metric cascades)",
        "• F1-Score: 0.737 (High signal fidelity)",
        "• False Positives: 3 (Robust noise rejection)",
        "• Method: Non-parametric MAD fences & control cohort offsets"
    ]:
        p = tf_b1.add_paragraph()
        p.text = line
        p.font.size = Pt(11)
        p.font.color.rgb = NAVY
        p.space_before = Pt(4)

    box2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.1), Inches(5.2), Inches(3.0))
    box2.fill.solid()
    box2.fill.fore_color.rgb = RGBColor(254, 242, 242)
    box2.line.color.rgb = RED
    tb_b2 = s6.shapes.add_textbox(Inches(7.0), Inches(3.2), Inches(4.8), Inches(2.8))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True
    tf_b2.paragraphs[0].text = "TRADITIONAL BASELINE (>30% Change Rule)"
    tf_b2.paragraphs[0].font.bold = True
    tf_b2.paragraphs[0].font.size = Pt(13)
    tf_b2.paragraphs[0].font.color.rgb = RED
    for line in [
        "• Precision: 42.9% (Suffers heavy false alarms)",
        "• Recall: 75.0% (Misses co-occurring sub-threshold shifts)",
        "• F1-Score: 0.545 (Poor operational utility)",
        "• False Positives: 8 (Triggered by weekend spikes)",
        "• Method: Static threshold without day-of-week normalization"
    ]:
        p = tf_b2.add_paragraph()
        p.text = line
        p.font.size = Pt(11)
        p.font.color.rgb = NAVY
        p.space_before = Pt(4)

    # ==========================================
    # SLIDE 7: WORKING 3D EFFECTS & DESIGN
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "UI/UX & Visual Engineering", "Enterprise 3D Glassmorphism & Working 3D Effects",
               "Refined tactile interactions designed to enhance data comprehension, not distract")

    col_w = Inches(3.64)
    c1 = add_card(s7, Inches(0.8), Inches(2.0), col_w, Inches(4.6), "Interactive 3D Risk Universe")
    tb = s7.shapes.add_textbox(Inches(1.0), Inches(2.7), col_w - Inches(0.4), Inches(3.7))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "• Real-time HTML5 3D Canvas with perspective projection."
    tf.paragraphs[0].font.size = Pt(11)
    tf.paragraphs[0].font.color.rgb = SLATE
    for txt in [
        "• Drag-to-Rotate 3D Space: Pitch and yaw controls with smooth inertia damping.",
        "• Auto-Orbit Mode: Continuous smooth orbital rotation with pause/resume.",
        "• 3D Shaded Spheres & Dust: Volumetric particle field and pulsing orbital rings.",
        "• Live Telemetry HUD: Real-time popover inspection of 3D node metrics on hover."
    ]:
        p = tf.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE
        p.space_before = Pt(6)

    c2 = add_card(s7, Inches(4.84), Inches(2.0), col_w, Inches(4.6), "3D Gyro Tilt & Light Glare")
    tb = s7.shapes.add_textbox(Inches(5.04), Inches(2.7), col_w - Inches(0.4), Inches(3.7))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "• Real-Time Mouse Parallax: Cards tilt in 3D perspective based on cursor coordinates."
    tf.paragraphs[0].font.size = Pt(11)
    tf.paragraphs[0].font.color.rgb = SLATE
    for txt in [
        "• Holographic Specular Glare: Dynamic radial light gradient moves across the card surface in real time.",
        "• Modal 3D Gyro: Deep inspection dialog physically tilts dynamically in 3D space.",
        "• Layered Z-Depth: Headers and badges float at translateZ(12px) for true depth."
    ]:
        p = tf.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE
        p.space_before = Pt(6)

    c3 = add_card(s7, Inches(8.88), Inches(2.0), col_w, Inches(4.6), "Custom 3D Glass Scrollbar")
    tb = s7.shapes.add_textbox(Inches(9.08), Inches(2.7), col_w - Inches(0.4), Inches(3.7))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "• Universal 7px slim floating pill thumb replacing standard gray OS bars."
    tf.paragraphs[0].font.size = Pt(11)
    tf.paragraphs[0].font.color.rgb = SLATE
    for txt in [
        "• Translucent frosted track prevents card border clipping.",
        "• Lavender-ice gradient thumb with top specular highlight.",
        "• Hover Luminescence: Illuminates with soft indigo glow on hover.",
        "• Cross-browser consistency across Chrome, Edge, and Firefox."
    ]:
        p = tf.add_paragraph()
        p.text = txt
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE
        p.space_before = Pt(6)

    # ==========================================
    # SLIDE 8: DECISION SUPPORT & WHAT-IF
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Operational Impact", "Decision Support & What-If Stress Testing",
               "Translating detected signals into verified conclusions and simulated financial risk")

    add_card(s8, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.6), "Dual-Domain What-If Simulator")
    tb = s8.shapes.add_textbox(Inches(1.0), Inches(2.65), Inches(5.2), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Interactive sensitivity analysis with dual domain toggle:"
    tf.paragraphs[0].font.size = Pt(11.5)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = NAVY
    for item in [
        "Retail Sliders: Delivery delay (+/- %), refund rate delta, sales demand shift, inventory buffer reduction.",
        "MRO Sliders: Machinery vibration shift, PM backlog surge, parts lead time days, hourly downtime cost.",
        "Rigorous Methodological Boundary: Clearly categorizes direct arithmetic consequences vs empirical elasticity projections vs stated engineering assumptions."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE
        p.space_before = Pt(6)

    add_card(s8, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.6), "Investigation Workspace & Tool-AI")
    tb = s8.shapes.add_textbox(Inches(7.0), Inches(2.65), Inches(5.3), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = "Operational governance and evidence-grounded assistance:"
    tf.paragraphs[0].font.size = Pt(11.5)
    tf.paragraphs[0].font.bold = True
    tf.paragraphs[0].font.color.rgb = NAVY
    for item in [
        "Priority Triage: Assign P1, P2, or P3 operational urgency to risk findings.",
        "Audit Trail: Update investigation statuses ('New', 'Investigating', 'Confirmed', 'Resolved') and record conclusions.",
        "Tool-Grounded AI Assistant: Answers questions by executing deterministic database queries, preventing hallucination.",
        "One-Click Executive PDF: Compiles audit-ready PDF reports via ReportLab alongside structured JSON and CSV."
    ]:
        p = tf.add_paragraph()
        p.text = "• " + item
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE
        p.space_before = Pt(6)

    # ==========================================
    # SLIDE 9: COMPETITIVE ADVANTAGE
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Market Positioning", "Competitive Advantage: Beyond Siloed BI",
               "Why traditional enterprise dashboards leave millions in unaddressed operational risk")

    add_card(s9, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.6), "Feature & Capability Matrix")

    # Table
    rows = 6
    cols = 4
    left = Inches(1.1)
    top = Inches(2.6)
    width = Inches(11.133)
    height = Inches(3.6)

    table_shape = s9.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table
    table.columns[0].width = Inches(3.3)
    table.columns[1].width = Inches(2.6)
    table.columns[2].width = Inches(2.6)
    table.columns[3].width = Inches(2.6)

    headers = ["Capability", "Traditional BI (Tableau)", "APM / Monitoring", "SIGNALFIRE AI"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE
        cell.fill.solid()
        cell.fill.fore_color.rgb = INDIGO if i == 3 else NAVY

    matrix_data = [
        ("Cross-Dataset Anomaly Correlation", "Manual cross-filtering", "Isolated metric alerts", "Automated Lead-Lag Engine (r=0.89)"),
        ("Noise-Robust Outlier Detection", "Rarely available (mean/std)", "Static % change thresholds", "Robust MAD & IQR Fences"),
        ("Epistemic Fact/Hypothesis Rigor", "No distinction", "No distinction", "Strict Epistemic Architecture"),
        ("Analytical Engine", "External SQL warehouse", "Proprietary timeseries", "Exasol Personal + DuckDB OLAP"),
        ("Decision Support & What-If", "Static parameter reports", "Runbook links only", "Live Multi-Variable Stress-Testing")
    ]

    for row_idx, row_data in enumerate(matrix_data):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = text
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            if col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = INDIGO
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(238, 242, 255)
            else:
                p.font.color.rgb = NAVY if col_idx == 0 else SLATE

    # ==========================================
    # SLIDE 10: SUMMARY & ROADMAP
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Conclusion", "Delivering Operational Resilience",
               "SIGNALFIRE AI: Transforming hidden warning signs into proactive business interventions")

    c1 = add_card(s10, Inches(0.8), Inches(2.0), Inches(5.6), Inches(4.6), "What We Built & Verified")
    tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.65), Inches(5.2), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    bullets = [
        ("Fully Working Full-Stack System: ", "FastAPI + React 18 + TypeScript + Exasol Personal + DuckDB."),
        ("13 Datasets & Ground Truth: ", "60,653+ records spanning Retail and Industrial MRO domains."),
        ("Working 3D WebGL/Canvas: ", "Interactive 3D orbital risk universe with mouse drag-to-rotate."),
        ("3D Glassmorphic Interface: ", "Real-time mouse gyro-tilt cards, light glare, and custom slim scrollbars."),
        ("Empirically Validated: ", "12/12 pytest tests passing; F1=0.74 benchmark superiority over static rules.")
    ]
    for idx, (b_title, b_desc) in enumerate(bullets):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        run1 = p.add_run()
        run1.text = b_title
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = NAVY
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(11)
        run2.font.color.rgb = SLATE
        p.space_before = Pt(6)

    c2 = add_card(s10, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.6), "Future Horizon & Production Scaling")
    tb = s10.shapes.add_textbox(Inches(7.0), Inches(2.65), Inches(5.3), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True
    future = [
        ("Exasol Multi-Node Cluster Scaling: ", "Deploying across distributed Exasol clusters for multi-billion record datasets."),
        ("Multimodal Unstructured Signals: ", "Integrating customer support phone audio transcripts and maintenance logs via LLM embedding vectors."),
        ("Automated ERP Webhook Enforcement: ", "Triggering automated SAP/NetSuite carrier SLA penalty clawbacks upon confirmed lead-lag breach."),
        ("Predictive Digital Twins: ", "Connecting real-time IoT vibration sensors for predictive mechanical wear simulation.")
    ]
    for idx, (f_title, f_desc) in enumerate(future):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        run1 = p.add_run()
        run1.text = f_title
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = CYAN
        run2 = p.add_run()
        run2.text = f_desc
        run2.font.size = Pt(11)
        run2.font.color.rgb = SLATE
        p.space_before = Pt(8)

    prs.save(output_path)
    print(f"Successfully generated 10-slide PowerPoint pitch deck at: {output_path}")

if __name__ == "__main__":
    create_deck()
