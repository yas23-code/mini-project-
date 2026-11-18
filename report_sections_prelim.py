import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle

def add_cover_and_prelim(story, PageMarker, styles, fig_dir, toc_mapping=None):
    if toc_mapping is None:
        # Default fallback mapping
        toc_mapping = {
            'c1': '1', 'c1_1': '1', 'c1_2': '1', 'c1_3': '2', 'c1_4': '3', 'c1_5': '3', 'c1_6': '4',
            'c2': '5', 'c2_1': '5', 'c2_2': '7', 'c2_3': '7', 'c2_7': '8',
            'c3': '10', 'c3_1': '10', 'c3_2': '11', 'c3_3': '12', 'c3_4': '12', 'c3_5': '13', 'c3_6': '13',
            'c4': '15', 'c4_1': '15', 'c4_6': '17', 'c4_7': '18',
            'c5': '21', 'c5_1': '21', 'c5_2': '22',
            'app': '23',
            'ref': '25'
        }

    c_primary = styles['c_primary']

    # =========================================================================
    # 1. COVER PAGE (PAGE 1 - UNNUMBERED)
    # =========================================================================
    story.append(PageMarker('COVER'))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Mini Project Report", styles['cov_mini_style']))
    story.append(Paragraph("on", styles['cov_on_style']))
    story.append(Paragraph("<b>CRIMELENS 2.0: AI-POWERED PUBLIC SAFETY SUITE &amp;<br/>SAFE CORRIDOR INTELLIGENCE</b>", styles['cov_title_style']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Submitted for partial fulfillment of award of", styles['cov_submitted_style']))
    story.append(Paragraph("<b>BACHELOR OF TECHNOLOGY</b>", styles['cov_degree_style']))
    story.append(Paragraph("degree", styles['cov_degree_word']))
    story.append(Paragraph("In", styles['cov_in_style']))
    story.append(Paragraph("<b>Computer Science &amp; Engineering</b>", styles['cov_dept_style']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("By", styles['cov_by_style']))
    story.append(Paragraph("Utkarsh Yadav (2400320101209)", styles['cov_student_style']))
    story.append(Paragraph("Vaibhav Srivastav (2400320101215)", styles['cov_student_style']))
    story.append(Paragraph("Vanshika Goswami (2400320101229)", styles['cov_student_style']))
    story.append(Paragraph("Yash Saraswat (2400320101296)", styles['cov_student_style']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Under the Supervision of", styles['cov_supervision_style']))
    story.append(Paragraph("Ms. Anuksha Srivastav", styles['cov_supervisor_name']))
    story.append(Paragraph("(Assistant Professor)", styles['cov_designation']))
    story.append(Spacer(1, 10))

    abes_logo_path = os.path.join(fig_dir, 'image1.png')
    aktu_logo_path = os.path.join(fig_dir, 'image2.png')
    if os.path.exists(abes_logo_path) and os.path.exists(aktu_logo_path):
        img_abes = Image(abes_logo_path, width=130, height=73)
        img_aktu = Image(aktu_logo_path, width=73, height=73)
        t_logos = Table([[img_abes, img_aktu]], colWidths=[180, 180])
        t_logos.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(t_logos)
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>ABES ENGINEERING COLLEGE, GHAZIABAD</b>", styles['cov_college_style']))
    story.append(Paragraph("<b>AFFILIATED TO</b>", styles['cov_affiliated_style']))
    story.append(Paragraph("<b>Dr. A P J ABDUL KALAM TECHNICAL UNIVERSITY, LUCKNOW</b>", styles['cov_univ_style']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>November 2026</b>", styles['cov_date_style']))
    story.append(PageBreak())

    # =========================================================================
    # 2. STUDENT'S DECLARATION (PAGE ii)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>STUDENT'S DECLARATION</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "We hereby declare that the work being presented in this report entitled "
        "<b>\"CRIMELENS 2.0: AI-POWERED PUBLIC SAFETY SUITE &amp; SAFE CORRIDOR INTELLIGENCE\"</b> "
        "is an authentic record of our own work carried out under the supervision of <b>Ms. Anuksha Srivastav</b> "
        "(Assistant Professor, Department of Computer Science &amp; Engineering).", styles['prelim_body_style']))
    story.append(Paragraph(
        "The matter embodied in this report has not been submitted by us for the award of any other degree.", styles['prelim_body_style']))
    story.append(Spacer(1, 20))
    sig_student_table = [
        [Paragraph("<b>Dated:</b> November 2026", styles['table_cell_bold']),
         Paragraph("<b>Signature of student(s):</b>", styles['table_cell_bold'])],
        [Paragraph("<b>Department:</b> Computer Science &amp; Engineering", styles['table_cell_style']),
         Paragraph(
             "1. ______________________ (Utkarsh Yadav - 2400320101209)<br/>"
             "2. ______________________ (Vaibhav Srivastav - 2400320101215)<br/>"
             "3. ______________________ (Vanshika Goswami - 2400320101229)<br/>"
             "4. ______________________ (Yash Saraswat - 2400320101296)", styles['table_cell_style'])]
    ]
    t_std_sig = Table(sig_student_table, colWidths=[200, 295])
    t_std_sig.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
    story.append(t_std_sig)
    story.append(Spacer(1, 35))
    story.append(Paragraph(
        "This is to certify that the above statement made by the candidates is correct to the best of my knowledge.", styles['prelim_body_style']))
    story.append(Spacer(1, 20))
    hod_sup_table = [[
        Paragraph("____________________________<br/><b>Signature of HOD</b><br/>(Prof. (Dr.) Pankaj Kumar Sharma)<br/>(Computer Science Department)<br/>Date: ............................", styles['table_cell_style']),
        Paragraph("____________________________<br/><b>Signature of Supervisor</b><br/>(Name:- Ms. Anuksha Srivastav)<br/>(Designation: Assistant Professor)<br/>(Computer Science Department)", styles['table_cell_style'])
    ]]
    t_hod_sup = Table(hod_sup_table, colWidths=[245, 250])
    t_hod_sup.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_hod_sup)
    story.append(PageBreak())

    # =========================================================================
    # 3. CERTIFICATE (PAGE iii)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>CERTIFICATE</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 25))
    story.append(Paragraph(
        "This is to certify that project report entitled "
        "<b>\"CRIMELENS 2.0: AI-POWERED PUBLIC SAFETY SUITE &amp; SAFE CORRIDOR INTELLIGENCE\"</b> "
        "which is submitted by <b>Utkarsh Yadav</b> (2400320101209), <b>Vaibhav Srivastav</b> (2400320101215), "
        "<b>Vanshika Goswami</b> (2400320101229), and <b>Yash Saraswat</b> (2400320101296) in partial fulfilment of the requirement "
        "for the award of the degree of B. Tech. in the Department of Computer Science &amp; Engineering of "
        "<b>Dr A.P.J. Abdul Kalam Technical University, formerly Uttar Pradesh Technical University</b>, is a record of the candidate's "
        "own work carried out by them under my supervision. The matter embodied in this thesis is original and has not been submitted "
        "for the award of any other degree.", styles['prelim_body_style']))
    story.append(Spacer(1, 60))
    cert_sup_block = [[Paragraph("", styles['table_cell_style']),
        Paragraph("____________________________<br/><b>Signature of Supervisor</b><br/>(Name:- Ms. Anuksha Srivastav)<br/>(Designation: Assistant Professor)<br/>(Computer Science Department)", styles['table_cell_style'])]]
    t_cert_block = Table(cert_sup_block, colWidths=[240, 255])
    t_cert_block.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_cert_block)
    story.append(PageBreak())

    # =========================================================================
    # 4. ACKNOWLEDGEMENT (PAGE iv)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>ACKNOWLEDGEMENT</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "It gives us a great sense of pleasure to present the report of the B. Tech Project undertaken during B. Tech. 5th Semester. "
        "We owe special debt of gratitude to <b>Ms. Anuksha Srivastav</b>, Department of Computer Science &amp; Engineering, ABESEC Ghaziabad "
        "for her constant support and guidance throughout the course of our work. Her sincerity, thoroughness and perseverance have been "
        "a constant source of inspiration for us. It is only her cognizant efforts that our endeavors have seen light of the day.", styles['prelim_body_style']))
    story.append(Paragraph(
        "We also take the opportunity to acknowledge the contribution of <b>Prof. (Dr.) Pankaj Kumar Sharma</b>, Head, Department of "
        "Computer Science, ABESEC Ghaziabad for his full support and assistance during the development of the project.", styles['prelim_body_style']))
    story.append(Paragraph(
        "We also do not like to miss the opportunity to acknowledge the contribution of all faculty members of the department for their "
        "kind assistance and cooperation during the development of our project. Last but not the least, we acknowledge our friends for "
        "their contribution in the completion of the project.", styles['prelim_body_style']))
    story.append(Spacer(1, 25))
    ack_sig_grid = [
        [Paragraph("Signature: ______________________<br/><b>Name :</b> Utkarsh Yadav<br/><b>Roll No.:</b> 2400320101209<br/><b>Date :</b> November 2026", styles['table_cell_style']),
         Paragraph("Signature: ______________________<br/><b>Name :</b> Vaibhav Srivastav<br/><b>Roll No.:</b> 2400320101215<br/><b>Date :</b> November 2026", styles['table_cell_style'])],
        [Spacer(1, 15), Spacer(1, 15)],
        [Paragraph("Signature: ______________________<br/><b>Name :</b> Vanshika Goswami<br/><b>Roll No.:</b> 2400320101229<br/><b>Date :</b> November 2026", styles['table_cell_style']),
         Paragraph("Signature: ______________________<br/><b>Name :</b> Yash Saraswat<br/><b>Roll No.:</b> 2400320101296<br/><b>Date :</b> November 2026", styles['table_cell_style'])]
    ]
    t_ack_grid = Table(ack_sig_grid, colWidths=[245, 250])
    t_ack_grid.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    story.append(t_ack_grid)
    story.append(PageBreak())

    # =========================================================================
    # 5. ABSTRACT (PAGE v)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>ABSTRACT</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "Urban public safety and commuter navigation face severe limitations due to reactive reporting and maintenance-heavy IoT hardware "
        "that suffer from vandalism and sensory blind spots. This project presents CrimeLens 2.0, a 100% pure software, hardware-independent "
        "public safety intelligence suite designed for pedestrian safe corridor routing, municipal patrol fleet allocation, and explainable "
        "crime risk forecasting. To eliminate hardware dependencies, we formulate SafePath AI -- a multi-criteria graph routing engine that adapts "
        "Dijkstra's algorithm with a Dynamic Safety Index penalizing unlit segments and nocturnal temporal risks -- alongside a Smart Patrol Fleet Optimizer "
        "utilizing a diminishing returns response time model (R(u) = R<sub>0</sub> / sqrt(u)) for latency minimization. The system incorporates an explainable "
        "machine learning suite benchmarking Gradient Boosting (R<sup>2</sup> = 0.9896), Random Forest (R<sup>2</sup> = 0.9777), and Ridge Regression with waterfall "
        "feature attributions and 90% confidence intervals for What-If municipal policy simulations. Deployed on a modern decoupled web architecture "
        "using FastAPI and React with Leaflet mapping, CrimeLens 2.0 achieves a 66.7% danger reduction with only a 10.4% distance detour and cuts "
        "maximum patrol response latency from 24.0 to 9.8 minutes. All engineering objectives were fully accomplished, establishing a scalable, "
        "accessible, and transparent algorithmic paradigm for municipal safety governance.", styles['abstract_body_style']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>Keywords:</b> Public Safety Intelligence, Safe Corridor Routing, Multi-Criteria Dijkstra, Patrol Allocation, Machine Learning, Gradient Boosting, Explainable AI.",
        ParagraphStyle('KwStyle', fontName='Times-Roman', fontSize=10, leading=14, textColor=colors.black)))
    story.append(PageBreak())

    # =========================================================================
    # 6. TABLE OF CONTENTS (PAGE vi - STRICTLY 1 PAGE)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>TABLE OF CONTENTS</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 4))
    toc_entries = [
        ("<b>DECLARATION</b>", "<b>ii</b>", True),
        ("<b>CERTIFICATE</b>", "<b>iii</b>", True),
        ("<b>ACKNOWLEDGEMENTS</b>", "<b>iv</b>", True),
        ("<b>ABSTRACT</b>", "<b>v</b>", True),
        ("<b>LIST OF TABLES</b>", "<b>vii</b>", True),
        ("<b>LIST OF FIGURES</b>", "<b>viii</b>", True),
        ("<b>LIST OF SYMBOLS</b>", "<b>ix</b>", True),
        ("<b>LIST OF ABBREVIATIONS</b>", "<b>x</b>", True),
        ("<b>CHAPTER 1: INTRODUCTION</b>", f"<b>{toc_mapping.get('c1', '1')}</b>", True),
        ("&emsp;1.1 Problem Introduction", toc_mapping.get('c1_1', '1'), False),
        ("&emsp;1.2 Motivation", toc_mapping.get('c1_2', '1'), False),
        ("&emsp;1.3 Project Objective", toc_mapping.get('c1_3', '2'), False),
        ("&emsp;1.4 Scope of the Project", toc_mapping.get('c1_4', '3'), False),
        ("&emsp;1.5 Related Previous Work", toc_mapping.get('c1_5', '3'), False),
        ("&emsp;1.6 Organization of the Report", toc_mapping.get('c1_6', '4'), False),
        ("<b>CHAPTER 2: SOFTWARE REQUIREMENT SPECIFICATION</b>", f"<b>{toc_mapping.get('c2', '5')}</b>", True),
        ("&emsp;2.1 Product Perspective &amp; Interfaces", toc_mapping.get('c2_1', '5'), False),
        ("&emsp;2.2 Product Functions", toc_mapping.get('c2_2', '7'), False),
        ("&emsp;2.3 User Characteristics &amp; Constraints", toc_mapping.get('c2_3', '7'), False),
        ("&emsp;2.7 Use Case Modeling &amp; Scenarios", toc_mapping.get('c2_7', '8'), False),
        ("<b>CHAPTER 3: SYSTEM DESIGN</b>", f"<b>{toc_mapping.get('c3', '10')}</b>", True),
        ("&emsp;3.1 3-Tier Architecture &amp; Class Diagrams", toc_mapping.get('c3_1', '10'), False),
        ("&emsp;3.2 Data Flow &amp; Activity Diagrams", toc_mapping.get('c3_2', '11'), False),
        ("&emsp;3.5 Relational Database Schema", toc_mapping.get('c3_5', '12'), False),
        ("&emsp;3.6 SafePath AI &amp; Patrol Algorithmic Formulations", toc_mapping.get('c3_6', '13'), False),
        ("<b>CHAPTER 4: IMPLEMENTATION AND RESULTS</b>", f"<b>{toc_mapping.get('c4', '15')}</b>", True),
        ("&emsp;4.1 Software &amp; Hardware Requirements", toc_mapping.get('c4_1', '15'), False),
        ("&emsp;4.6 Test Cases Verification Suite", toc_mapping.get('c4_6', '17'), False),
        ("&emsp;4.7 Multi-Model Benchmarks &amp; Empirical Results", toc_mapping.get('c4_7', '18'), False),
        ("<b>CHAPTER 5: CONCLUSION</b>", f"<b>{toc_mapping.get('c5', '21')}</b>", True),
        ("&emsp;5.1 Performance Evaluation Summary", toc_mapping.get('c5_1', '21'), False),
        ("&emsp;5.2 State-of-the-Art Comparison &amp; Future Directions", toc_mapping.get('c5_2', '22'), False),
        ("<b>APPENDIX: GITHUB REPOSITORY &amp; CODE LISTINGS</b>", f"<b>{toc_mapping.get('app', '23')}</b>", True),
        ("<b>REFERENCES</b>", f"<b>{toc_mapping.get('ref', '25')}</b>", True)
    ]
    toc_rows = []
    for item, page, is_bold in toc_entries:
        p_item = Paragraph(item, styles['toc_item_bold'] if is_bold else styles['toc_item_style'])
        p_page = Paragraph(page, styles['toc_page_bold'] if is_bold else styles['toc_page_style'])
        toc_rows.append([p_item, p_page])
    t_toc = Table(toc_rows, colWidths=[435, 60])
    t_toc.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.0),
        ('TOPPADDING', (0,0), (-1,-1), 1.0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # 7. LIST OF TABLES (PAGE vii)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>LIST OF TABLES</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 10))
    lot_data = [
        [Paragraph("<b>Table</b>", styles['table_cell_header']), Paragraph("<b>Description</b>", styles['table_cell_header'])],
        [Paragraph("Table 2.1", styles['table_cell_bold']), Paragraph("Comparison Of Required Software Stack Components &amp; Interfaces", styles['table_cell_style'])],
        [Paragraph("Table 2.2", styles['table_cell_bold']), Paragraph("SafePath Route Query Use Case Scenario (UC-01)", styles['table_cell_style'])],
        [Paragraph("Table 2.3", styles['table_cell_bold']), Paragraph("Patrol Fleet Allocation Use Case Scenario (UC-02)", styles['table_cell_style'])],
        [Paragraph("Table 3.1", styles['table_cell_bold']), Paragraph("Relational Database Schema &amp; Field Definitions", styles['table_cell_style'])],
        [Paragraph("Table 3.2", styles['table_cell_bold']), Paragraph("Spatial Intersection Nodes Schema &amp; Topology Definition", styles['table_cell_style'])],
        [Paragraph("Table 4.1", styles['table_cell_bold']), Paragraph("Comprehensive Functional Verification &amp; Test Cases", styles['table_cell_style'])],
        [Paragraph("Table 4.2", styles['table_cell_bold']), Paragraph("Machine Learning Regression Model Benchmark Evaluation", styles['table_cell_style'])],
        [Paragraph("Table 4.3", styles['table_cell_bold']), Paragraph("12-Beat Municipal Patrol Fleet Optimization &amp; Latency Reduction", styles['table_cell_style'])],
        [Paragraph("Table 4.4", styles['table_cell_bold']), Paragraph("Comparative SafePath Routing Evaluation Across 6 NCR Corridors", styles['table_cell_style'])],
        [Paragraph("Table 5.1", styles['table_cell_bold']), Paragraph("Comparison with Existing State-of-the-Art Technologies", styles['table_cell_style'])],
        [Paragraph("Table A.1", styles['table_cell_bold']), Paragraph("Complete CrimeLens 2.0 REST API Endpoints Specification", styles['table_cell_style'])]
    ]
    t_lot = Table(lot_data, colWidths=[110, 385])
    t_lot.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_lot)
    story.append(PageBreak())

    # =========================================================================
    # 8. LIST OF FIGURES (PAGE viii)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>LIST OF FIGURES</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 10))
    lof_data = [
        [Paragraph("<b>Figure</b>", styles['table_cell_header']), Paragraph("<b>Description</b>", styles['table_cell_header'])],
        [Paragraph("Fig 2.1", styles['table_cell_bold']), Paragraph("CrimeLens 2.0 Use Case Interaction Model", styles['table_cell_style'])],
        [Paragraph("Fig 3.1", styles['table_cell_bold']), Paragraph("3-Tier Architecture Diagram for CrimeLens 2.0 Full Stack System", styles['table_cell_style'])],
        [Paragraph("Fig 3.2", styles['table_cell_bold']), Paragraph("SafePath Activity Diagram (Routing Decision Workflow)", styles['table_cell_style'])],
        [Paragraph("Fig 3.3", styles['table_cell_bold']), Paragraph("SafePath AI Multi-Criteria Optimization &amp; Corridor Decision Flowchart", styles['table_cell_style'])],
        [Paragraph("Fig 4.1", styles['table_cell_bold']), Paragraph("CrimeLens Analytics &amp; Operational Dashboard Interface Snapshot", styles['table_cell_style'])],
        [Paragraph("Fig 4.2", styles['table_cell_bold']), Paragraph("AI Crime Prediction &amp; Explainable AI (XAI) Studio Interface Snapshot", styles['table_cell_style'])],
        [Paragraph("Fig 4.3", styles['table_cell_bold']), Paragraph("Geospatial Crime Hotspot Visualization &amp; Regional Severity Ranking Snapshot", styles['table_cell_style'])],
        [Paragraph("Fig 4.4", styles['table_cell_bold']), Paragraph("Predictive Model Benchmarking &amp; Accuracy Comparison", styles['table_cell_style'])],
        [Paragraph("Fig 4.5", styles['table_cell_bold']), Paragraph("Explainable AI (XAI) Waterfall Feature Attribution", styles['table_cell_style'])],
        [Paragraph("Fig 4.6", styles['table_cell_bold']), Paragraph("Diminishing Marginal Returns in Patrol Unit Allocation Curve", styles['table_cell_style'])]
    ]
    t_lof = Table(lof_data, colWidths=[110, 385])
    t_lof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_lof)
    story.append(PageBreak())

    # =========================================================================
    # 9. LIST OF SYMBOLS (PAGE ix)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>LIST OF SYMBOLS</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 10))
    sym_data = [
        [Paragraph("<b>Symbol</b>", styles['table_cell_header']), Paragraph("<b>Description</b>", styles['table_cell_header'])],
        [Paragraph("G = (V, E)", styles['table_cell_bold']), Paragraph("Planar Road Graph representing urban intersections (V) and street segments (E)", styles['table_cell_style'])],
        [Paragraph("d(e)", styles['table_cell_bold']), Paragraph("Physical metric segment distance in kilometers", styles['table_cell_style'])],
        [Paragraph("S(e)", styles['table_cell_bold']), Paragraph("Dynamic Safety Index of edge e (normalized score from 0.0 to 1.0)", styles['table_cell_style'])],
        [Paragraph("lambda", styles['table_cell_bold']), Paragraph("User-configured risk aversion sensitivity multiplier (continuous range 0.0 to 5.0)", styles['table_cell_style'])],
        [Paragraph("C(e)", styles['table_cell_bold']), Paragraph("Normalized historical crime density score of edge e", styles['table_cell_style'])],
        [Paragraph("L(e)", styles['table_cell_bold']), Paragraph("Municipal streetlight infrastructure illumination score of edge e", styles['table_cell_style'])],
        [Paragraph("P(e)", styles['table_cell_bold']), Paragraph("Active police patrol coverage density score of edge e", styles['table_cell_style'])],
        [Paragraph("T(t)", styles['table_cell_bold']), Paragraph("Temporal nocturnal penalty (+0.25 applied between 20:00 and 05:00 hours)", styles['table_cell_style'])],
        [Paragraph("Cost(e)", styles['table_cell_bold']), Paragraph("Effective multi-objective edge traversal cost: d(e) * [1 + lambda * S(e)]", styles['table_cell_style'])],
        [Paragraph("R(u)", styles['table_cell_bold']), Paragraph("Expected emergency response latency given u patrol units: R<sub>0</sub> / sqrt(u)", styles['table_cell_style'])],
        [Paragraph("u_i", styles['table_cell_bold']), Paragraph("Integer count of patrol vehicles assigned to municipal beat i", styles['table_cell_style'])],
        [Paragraph("R<sup>2</sup>", styles['table_cell_bold']), Paragraph("Coefficient of determination measuring machine learning regression goodness-of-fit", styles['table_cell_style'])]
    ]
    t_sym = Table(sym_data, colWidths=[110, 385])
    t_sym.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sym)
    story.append(PageBreak())

    # =========================================================================
    # 10. LIST OF ABBREVIATIONS (PAGE x)
    # =========================================================================
    story.append(PageMarker('PRELIM'))
    story.append(Paragraph("<b>LIST OF ABBREVIATIONS</b>", styles['prelim_heading_style']))
    story.append(Spacer(1, 10))
    abbr_data = [
        [Paragraph("<b>Abbreviation</b>", styles['table_cell_header']), Paragraph("<b>Expansion / Full Form</b>", styles['table_cell_header'])],
        [Paragraph("AI", styles['table_cell_bold']), Paragraph("Artificial Intelligence", styles['table_cell_style'])],
        [Paragraph("AKTU", styles['table_cell_bold']), Paragraph("Dr. A.P.J. Abdul Kalam Technical University, Lucknow", styles['table_cell_style'])],
        [Paragraph("API", styles['table_cell_bold']), Paragraph("Application Programming Interface", styles['table_cell_style'])],
        [Paragraph("ASGI", styles['table_cell_bold']), Paragraph("Asynchronous Server Gateway Interface", styles['table_cell_style'])],
        [Paragraph("CAD", styles['table_cell_bold']), Paragraph("Computer Aided Dispatch", styles['table_cell_style'])],
        [Paragraph("CI", styles['table_cell_bold']), Paragraph("Confidence Interval (90% Statistical Coverage)", styles['table_cell_style'])],
        [Paragraph("CORS", styles['table_cell_bold']), Paragraph("Cross-Origin Resource Sharing", styles['table_cell_style'])],
        [Paragraph("CSS", styles['table_cell_bold']), Paragraph("Cascading Style Sheets", styles['table_cell_style'])],
        [Paragraph("DFD", styles['table_cell_bold']), Paragraph("Data Flow Diagram", styles['table_cell_style'])],
        [Paragraph("DSI", styles['table_cell_bold']), Paragraph("Dynamic Safety Index", styles['table_cell_style'])],
        [Paragraph("GBR", styles['table_cell_bold']), Paragraph("Gradient Boosting Regressor", styles['table_cell_style'])],
        [Paragraph("GIS", styles['table_cell_bold']), Paragraph("Geographic Information System", styles['table_cell_style'])],
        [Paragraph("HOD", styles['table_cell_bold']), Paragraph("Head of the Department", styles['table_cell_style'])],
        [Paragraph("HTTP/HTTPS", styles['table_cell_bold']), Paragraph("Hypertext Transfer Protocol (Secure)", styles['table_cell_style'])],
        [Paragraph("IEEE", styles['table_cell_bold']), Paragraph("Institute of Electrical and Electronics Engineers", styles['table_cell_style'])],
        [Paragraph("JSON", styles['table_cell_bold']), Paragraph("JavaScript Object Notation", styles['table_cell_style'])],
        [Paragraph("KDE", styles['table_cell_bold']), Paragraph("Kernel Density Estimation", styles['table_cell_style'])],
        [Paragraph("MAE", styles['table_cell_bold']), Paragraph("Mean Absolute Error", styles['table_cell_style'])],
        [Paragraph("ML", styles['table_cell_bold']), Paragraph("Machine Learning", styles['table_cell_style'])],
        [Paragraph("NCR", styles['table_cell_bold']), Paragraph("National Capital Region (Delhi/NCR)", styles['table_cell_style'])],
        [Paragraph("OSM", styles['table_cell_bold']), Paragraph("OpenStreetMap", styles['table_cell_style'])],
        [Paragraph("REST", styles['table_cell_bold']), Paragraph("Representational State Transfer", styles['table_cell_style'])],
        [Paragraph("RF", styles['table_cell_bold']), Paragraph("Random Forest", styles['table_cell_style'])],
        [Paragraph("RMSE", styles['table_cell_bold']), Paragraph("Root Mean Squared Error", styles['table_cell_style'])],
        [Paragraph("SPA", styles['table_cell_bold']), Paragraph("Single Page Application", styles['table_cell_style'])],
        [Paragraph("SRS", styles['table_cell_bold']), Paragraph("Software Requirement Specification", styles['table_cell_style'])],
        [Paragraph("SVM", styles['table_cell_bold']), Paragraph("Support Vector Machine", styles['table_cell_style'])],
        [Paragraph("TLS", styles['table_cell_bold']), Paragraph("Transport Layer Security", styles['table_cell_style'])],
        [Paragraph("UI/UX", styles['table_cell_bold']), Paragraph("User Interface / User Experience", styles['table_cell_style'])],
        [Paragraph("WCAG", styles['table_cell_bold']), Paragraph("Web Content Accessibility Guidelines", styles['table_cell_style'])],
        [Paragraph("XAI", styles['table_cell_bold']), Paragraph("Explainable Artificial Intelligence", styles['table_cell_style'])]
    ]
    t_abbr = Table(abbr_data, colWidths=[110, 385])
    t_abbr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_abbr)
    story.append(PageBreak())
