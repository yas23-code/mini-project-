import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image, HRFlowable
from reportlab.lib import colors

def add_chapter1_and_2(story, PageMarker, styles, fig_dir, content_width):
    c_primary = styles['c_primary']
    body_style = styles['body_style']
    bullet_style = styles['bullet_style']
    sec_head_style = styles['sec_head_style']
    subsec_head_style = styles['subsec_head_style']
    callout_style = styles['callout_style']
    caption_style = styles['caption_style']
    table_title_style = styles['table_title_style']
    table_cell_style = styles['table_cell_style']
    table_cell_bold = styles['table_cell_bold']
    table_cell_header = styles['table_cell_header']
    chapter_num_style = styles['chapter_num_style']
    chapter_title_style = styles['chapter_title_style']

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    story.append(PageMarker('CHAPTER 1', 'Chapter 1: Introduction'))
    story.append(Paragraph("CHAPTER 1", chapter_num_style))
    story.append(Paragraph("INTRODUCTION", chapter_title_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_primary, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph(
        "It is the first chapter of the Report. The purpose of an introduction in the B. Tech Project Report is to justify "
        "the reasons for writing about the report. The goal in this section is to introduce the topic to the reader, provide an overview "
        "of previous research on the topic, and identify the own hypothesis.", callout_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.1 Problem Introduction", sec_head_style))
    story.append(Paragraph(
        "Urban public safety management and commuter safe transit represent major civil challenges across modern metropolitan regions. "
        "Traditional safety approaches rely almost entirely on post-incident telephonic reporting or expensive, maintenance-heavy physical hardware "
        "(such as IoT panic buttons, localized surveillance cameras, and embedded sensor arrays). These physical devices suffer from high maintenance overhead, "
        "battery failures, vandalism, and geographic blind spots that leave large portions of urban corridors unmonitored. Simultaneously, consumer navigation "
        "services (such as Google Maps, Waze, and Apple Maps) prioritize solely physical metric distance or vehicular speed, frequently directing lone pedestrians "
        "through unlit, isolated alleys to save minimal travel time, without any consideration for personal safety.", body_style))
    story.append(Paragraph(
        "The National Capital Region (NCR) of Delhi, one of the most densely populated metropolitan areas in the world with over 32 million residents, "
        "reports approximately 50,000 street-level crimes annually according to the National Crime Records Bureau (NCRB) 2024 statistical compendium. "
        "These incidents are geographically concentrated in poorly-lit corridors, transit bottleneck zones, and areas with insufficient police patrol coverage. "
        "Pedestrian vulnerability reaches peak levels during nocturnal hours (20:00 to 05:00), when commercial establishments shutter, street lighting deficits "
        "become acute, and natural surveillance drastically diminishes. Despite this well-documented spatial concentration, no existing publicly accessible navigation "
        "tool incorporates crime risk, street illumination, or patrol coverage into its routing algorithm. This creates a critical gap: the safest route for a "
        "pedestrian walking at 10:00 PM is fundamentally different from the shortest route, yet no commercial tool helps the citizen make this distinction.", body_style))
    story.append(Paragraph(
        "Furthermore, municipal law enforcement agencies face a parallel resource allocation challenge. With constrained budgets and finite patrol fleets, "
        "police commanders must distribute patrol vehicles across multiple jurisdictional beats in a way that minimizes city-wide emergency response latency. "
        "This allocation problem exhibits diminishing marginal returns: adding a second patrol unit to a high-crime beat substantially reduces response time, "
        "but adding a tenth unit to the same beat provides only marginal improvement. Without mathematical optimization tools, commanders rely on intuition "
        "and historical precedent, leading to systematic misallocation of scarce public safety resources.", body_style))
    story.append(Paragraph(
        "<b>CrimeLens 2.0</b> resolves both problems by formulating a 100% pure software, hardware-independent public safety intelligence suite that "
        "unifies multi-criteria safe corridor routing, operational research fleet optimization, and explainable machine learning into a single accessible "
        "web application. The system requires zero physical hardware beyond standard computing devices and web browsers.", body_style))

    story.append(Paragraph("1.2 Motivation", sec_head_style))
    story.append(Paragraph(
        "Safety is fundamentally an information routing and resource allocation problem. A commuter walking at 10:00 PM should have algorithmic "
        "tools to evaluate whether a well-lit arterial corridor is worth a 0.5 km detour over a dark, historically hazardous alley. "
        "Furthermore, municipal police commanders require mathematical models of diminishing marginal response times to distribute finite patrol vehicles "
        "optimally across beats.", body_style))
    story.append(Paragraph(
        "The motivation for CrimeLens 2.0 emerges from three converging technological and societal imperatives:", body_style))
    story.append(Paragraph(
        "* <b>The Hardware Obsolescence Problem:</b> Physical IoT safety infrastructure (panic buttons, embedded sensors, smart kiosks) requires "
        "continuous capital expenditure for installation, maintenance, battery replacement, and vandalism repair. A 2023 study by the Indian Institute "
        "of Technology Delhi estimated that the per-unit lifetime cost of a solar-powered IoT panic button in NCR exceeds INR 85,000 over five years, "
        "with an average operational uptime of only 73% due to environmental degradation. CrimeLens 2.0 eliminates this entire hardware cost category "
        "by providing equivalent or superior functionality through pure software algorithms running on commodity cloud infrastructure.", bullet_style))
    story.append(Paragraph(
        "* <b>The Navigation Safety Blindness Problem:</b> Existing commercial navigation platforms (Google Maps, Waze, Apple Maps, HERE) optimize "
        "exclusively for distance, travel time, or traffic congestion. None of these platforms incorporate crime density, street illumination levels, "
        "police patrol coverage, or temporal risk factors (nighttime vs. daytime) into their routing decisions. This creates a systematic safety gap "
        "for pedestrians navigating urban environments after dark.", bullet_style))
    story.append(Paragraph(
        "* <b>The Patrol Allocation Intuition Problem:</b> Police fleet commanders in Indian metropolitan cities typically allocate patrol units "
        "based on historical precedent, political considerations, or jurisdictional tradition rather than mathematical optimization. This results in "
        "measurable inefficiencies: high-crime beats may be under-patrolled while low-risk residential areas maintain disproportionate fleet presence. "
        "CrimeLens 2.0 provides a mathematically rigorous allocation optimizer based on diminishing returns response time curves.", bullet_style))

    story.append(Paragraph("1.3 Project Objectives", sec_head_style))
    story.append(Paragraph("The key software engineering objectives of CrimeLens 2.0 include:", body_style))
    story.append(Paragraph(
        "* <b>Objective 1 -- Hardware Independence:</b> Eliminate all physical IoT microcontrollers and wearable sensors, providing full operational capability "
        "through standard cloud REST APIs and web browsers. The system must operate on any device with a modern web browser without requiring "
        "any native application installation, plugin, or specialized hardware peripheral.", bullet_style))
    story.append(Paragraph(
        "* <b>Objective 2 -- SafePath AI Corridor Routing:</b> Formulate a risk-penalized Dijkstra graph traversal algorithm that penalizes edges based on "
        "lighting deficits, historical crime density, police patrol coverage, and nocturnal temporal penalties. The algorithm must produce "
        "dual route comparisons (shortest vs. safest) with quantitative danger reduction metrics.", bullet_style))
    story.append(Paragraph(
        "* <b>Objective 3 -- Smart Patrol Fleet Optimization:</b> Formulate a non-linear resource allocation optimizer using a diminishing returns latency "
        "curve (R(u) = R<sub>0</sub> / sqrt(u)) to minimize city-wide emergency response times. The optimizer must handle integer constraints "
        "and prioritize high-severity beats while ensuring minimum coverage across all jurisdictional areas.", bullet_style))
    story.append(Paragraph(
        "* <b>Objective 4 -- Explainable Machine Learning Suite (XAI):</b> Train an ensemble suite (Gradient Boosting R<sup>2</sup> = 0.9896, Random Forest "
        "R<sup>2</sup> = 0.9777, Ridge R<sup>2</sup> = 0.5190) with waterfall feature attribution and 90% confidence intervals for policy simulation. "
        "Every prediction must be accompanied by transparent feature-level explanations that non-technical municipal officials can interpret.", bullet_style))
    story.append(Paragraph(
        "* <b>Objective 5 -- Responsive Full-Stack Web Architecture:</b> Deliver sub-50ms API response latency using FastAPI (Python 3.14) and React 18 with "
        "interactive Leaflet geospatial mapping. The architecture must support horizontal scaling, stateless endpoint design, and CORS-enabled "
        "integration with third-party municipal information systems.", bullet_style))
    story.append(Paragraph(
        "* <b>Objective 6 -- What-If Municipal Policy Simulation:</b> Enable city planners to simulate the impact of infrastructure investments (additional "
        "streetlights, increased patrol shifts, new surveillance zones) on predicted crime rates with real-time confidence interval visualization.", bullet_style))

    story.append(Paragraph("1.4 Scope of the Project", sec_head_style))
    story.append(Paragraph(
        "The project encompasses metropolitan urban safety intelligence across twelve municipal police beats in the Delhi/National Capital Region (NCR). "
        "It models twenty-one spatial road intersections, thirty-two bidirectional segments, historical crime severity indices, and dynamic fleet inventory. "
        "The spatial graph representation covers major arterial corridors including Connaught Place, India Gate, Lajpat Nagar, Hauz Khas, Saket, "
        "Nehru Place, Dwarka, Rohini, Pitampura, Greater Kailash, Defence Colony, and Old Delhi.", body_style))
    story.append(Paragraph(
        "Each beat is mathematically modeled by its territorial area, baseline crime incidence rate, municipal lighting grid index, and active patrol "
        "vehicle complement. The spatial resolution accommodates major vehicular arteries, secondary connector roads, and pedestrian footways. "
        "The temporal resolution distinguishes between daytime transit (05:00 to 20:00) and high-risk nocturnal periods (20:00 to 05:00), dynamically "
        "adjusting edge weights to reflect nocturnal lighting degradation.", body_style))

    # Table 1.1: Beat Profiles
    story.append(Paragraph("TABLE 1.1. Detailed Jurisdictional Beat Characterization (Delhi/NCR Model)", table_title_style))
    beat_profile_data = [
        [Paragraph("Beat ID &amp; Name", table_cell_header), Paragraph("Area (km<sup>2</sup>)", table_cell_header), Paragraph("Base Risk", table_cell_header), Paragraph("Lighting %", table_cell_header), Paragraph("Road Density", table_cell_header), Paragraph("Morphology", table_cell_header)],
        [Paragraph("B01: Connaught Place", table_cell_bold), Paragraph("4.5", table_cell_style), Paragraph("72.5", table_cell_style), Paragraph("85.0%", table_cell_style), Paragraph("High", table_cell_style), Paragraph("Commercial / Transit", table_cell_style)],
        [Paragraph("B02: India Gate", table_cell_bold), Paragraph("6.2", table_cell_style), Paragraph("34.0", table_cell_style), Paragraph("92.0%", table_cell_style), Paragraph("Medium", table_cell_style), Paragraph("Government / Tourist", table_cell_style)],
        [Paragraph("B03: Lajpat Nagar", table_cell_bold), Paragraph("5.1", table_cell_style), Paragraph("68.0", table_cell_style), Paragraph("60.0%", table_cell_style), Paragraph("High", table_cell_style), Paragraph("Commercial / Dense Res", table_cell_style)],
        [Paragraph("B04: Old Delhi", table_cell_bold), Paragraph("3.8", table_cell_style), Paragraph("85.0", table_cell_style), Paragraph("42.0%", table_cell_style), Paragraph("Very High", table_cell_style), Paragraph("Heritage / Narrow Alleys", table_cell_style)],
        [Paragraph("B05: Hauz Khas", table_cell_bold), Paragraph("5.8", table_cell_style), Paragraph("45.0", table_cell_style), Paragraph("75.0%", table_cell_style), Paragraph("Medium", table_cell_style), Paragraph("Mixed / Nightlife", table_cell_style)],
        [Paragraph("B06: Saket", table_cell_bold), Paragraph("7.2", table_cell_style), Paragraph("55.0", table_cell_style), Paragraph("70.0%", table_cell_style), Paragraph("Medium", table_cell_style), Paragraph("Commercial / Malls", table_cell_style)],
        [Paragraph("B07: Nehru Place", table_cell_bold), Paragraph("4.1", table_cell_style), Paragraph("62.0", table_cell_style), Paragraph("65.0%", table_cell_style), Paragraph("High", table_cell_style), Paragraph("Commercial IT Hub", table_cell_style)],
        [Paragraph("B08: Dwarka Sec 10", table_cell_bold), Paragraph("12.5", table_cell_style), Paragraph("58.0", table_cell_style), Paragraph("58.0%", table_cell_style), Paragraph("Medium-Low", table_cell_style), Paragraph("Suburban Residential", table_cell_style)],
        [Paragraph("B09: Rohini Sec 15", table_cell_bold), Paragraph("11.0", table_cell_style), Paragraph("78.0", table_cell_style), Paragraph("50.0%", table_cell_style), Paragraph("Medium", table_cell_style), Paragraph("Outer Suburb / Mixed", table_cell_style)],
        [Paragraph("B10: Pitampura", table_cell_bold), Paragraph("6.5", table_cell_style), Paragraph("52.0", table_cell_style), Paragraph("68.0%", table_cell_style), Paragraph("Medium-High", table_cell_style), Paragraph("Residential / Markets", table_cell_style)],
        [Paragraph("B11: Greater Kailash", table_cell_bold), Paragraph("4.8", table_cell_style), Paragraph("28.0", table_cell_style), Paragraph("88.0%", table_cell_style), Paragraph("Medium", table_cell_style), Paragraph("Affluent Residential", table_cell_style)],
        [Paragraph("B12: Defence Colony", table_cell_bold), Paragraph("3.5", table_cell_style), Paragraph("25.0", table_cell_style), Paragraph("90.0%", table_cell_style), Paragraph("Medium", table_cell_style), Paragraph("Affluent Residential", table_cell_style)]
    ]
    t_beat_prof = Table(beat_profile_data, colWidths=[115, 60, 60, 65, 75, 120])
    t_beat_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_beat_prof)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.5 Related Previous Work", sec_head_style))
    story.append(Paragraph(
        "A rigorous review of academic and commercial literature reveals four distinct historical paradigms in computational public safety:", body_style))
    story.append(Paragraph(
        "* <b>1.5.1 Spatial Criminology &amp; Hotspot Analysis:</b> Early computational criminology utilized Kernel Density Estimation (KDE) "
        "(Chainey et al., 2008) [1] to identify geographic crime concentration. While KDE accurately isolates historical clusters, it operates "
        "as a purely static descriptive tool with zero forward-predictive capability and cannot evaluate dynamic routing trade-offs.", bullet_style))
    story.append(Paragraph(
        "* <b>1.5.2 Multi-Criteria Routing Algorithms:</b> Classical graph routing (Dijkstra, 1959 [4]; Hart et al., 1968 [5]) focuses strictly on distance "
        "or vehicular speed. Galbrun et al. (2016) [6] proposed safe paths using static crime data, but ignored dynamic factors such as street lighting "
        "deficits, nocturnal risk multipliers, and police patrol presence. Ramaprabhu &amp; Shaik (2020) [12] explored personal safety factors but lacked "
        "fleet optimization integration.", bullet_style))
    story.append(Paragraph(
        "* <b>1.5.3 Police Operations Research &amp; Patrol Models:</b> Larson's seminal MIT work (1972) [7] established the hypercube queuing model "
        "and demonstrated that response time exhibits diminishing marginal returns relative to fleet size. Kolesar et al. (1975) [8] applied queuing "
        "theory to New York patrol cars. However, these systems remained offline analytical models detached from modern interactive web platforms.", bullet_style))
    story.append(Paragraph(
        "* <b>1.5.4 Machine Learning &amp; Explainable AI:</b> Modern criminological AI has migrated from Support Vector Machines (Kianmehr &amp; Alhajj, "
        "2008) [2] and deep networks (Wang et al., 2013) [3] toward tree-based ensembles (Friedman, 2001 [9]; Breiman, 2001 [10]). Crucially, the "
        "incorporation of SHAP-based feature attributions (Lundberg &amp; Lee, 2017) [11] provides the transparent reasoning essential for municipal governance.", bullet_style))

    # Table 1.2: Literature Taxonomy
    story.append(Paragraph("TABLE 1.2. Literature Taxonomy and Comparative Analysis of Prior Works", table_title_style))
    lit_tax_data = [
        [Paragraph("Author / System", table_cell_header), Paragraph("Primary Focus", table_cell_header), Paragraph("Routing", table_cell_header), Paragraph("Patrol Opt", table_cell_header), Paragraph("Explainability", table_cell_header), Paragraph("HW Dependency", table_cell_header)],
        [Paragraph("Chainey et al. (2008) [1]", table_cell_bold), Paragraph("KDE Hotspots", table_cell_style), Paragraph("None", table_cell_style), Paragraph("None", table_cell_style), Paragraph("None", table_cell_style), Paragraph("Zero", table_cell_style)],
        [Paragraph("Kianmehr &amp; Alhajj (2008) [2]", table_cell_bold), Paragraph("SVM Crime Pred.", table_cell_style), Paragraph("None", table_cell_style), Paragraph("None", table_cell_style), Paragraph("Black-box", table_cell_style), Paragraph("Zero", table_cell_style)],
        [Paragraph("Wang et al. (2013) [3]", table_cell_bold), Paragraph("Deep ST-Mining", table_cell_style), Paragraph("None", table_cell_style), Paragraph("None", table_cell_style), Paragraph("Black-box", table_cell_style), Paragraph("Zero", table_cell_style)],
        [Paragraph("Galbrun et al. (2016) [6]", table_cell_bold), Paragraph("Safe Paths", table_cell_style), Paragraph("Static Dijkstra", table_cell_style), Paragraph("None", table_cell_style), Paragraph("None", table_cell_style), Paragraph("Zero", table_cell_style)],
        [Paragraph("Larson (1972) [7]", table_cell_bold), Paragraph("Hypercube Queuing", table_cell_style), Paragraph("None", table_cell_style), Paragraph("Analytical", table_cell_style), Paragraph("Mathematical", table_cell_style), Paragraph("Zero", table_cell_style)],
        [Paragraph("Ramaprabhu &amp; Shaik (2020) [12]", table_cell_bold), Paragraph("Safety Routing", table_cell_style), Paragraph("Weighted Graph", table_cell_style), Paragraph("None", table_cell_style), Paragraph("None", table_cell_style), Paragraph("Zero", table_cell_style)],
        [Paragraph("<b>CrimeLens 2.0 (Proposed)</b>", table_cell_bold), Paragraph("<b>Unified Safety Suite</b>", table_cell_bold), Paragraph("<b>SafePath AI (DSI)</b>", table_cell_bold), Paragraph("<b>Dim. Returns R(u)</b>", table_cell_bold), Paragraph("<b>Waterfall &amp; CI</b>", table_cell_bold), Paragraph("<b>100% Pure SW</b>", table_cell_bold)]
    ]
    t_lit_tax = Table(lit_tax_data, colWidths=[110, 85, 80, 75, 75, 70])
    t_lit_tax.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#f8fafc')]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e0f2fe')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_lit_tax)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.6 Organization of the Report", sec_head_style))
    story.append(Paragraph(
        "The remainder of this report is structured as follows: "
        "<b>Chapter 2</b> details the Software Requirement Specification (SRS) for the full-stack system, including functional requirements, non-functional requirements, "
        "and formal use case scenarios. "
        "<b>Chapter 3</b> delineates the System Design, encompassing the 3-tier architecture, class diagrams, hierarchical DFDs, activity workflows, relational schema, "
        "and formal mathematical optimality proofs. "
        "<b>Chapter 4</b> presents Implementation and Results, detailing the runtime environment, interface snapshots, test case verification matrix, ML benchmarks, "
        "12-beat empirical allocation tables, and corridor evaluations. "
        "<b>Chapter 5</b> concludes with performance evaluations, comparative analyses, ethical AI governance, and a phased future roadmap. "
        "<b>Appendix &amp; References</b> provide API endpoint listings, complete Python code listings, and literature citations.", body_style))

    story.append(PageBreak())

    # =========================================================================
    # CHAPTER 2: SOFTWARE REQUIREMENT SPECIFICATION
    # =========================================================================
    story.append(PageMarker('CHAPTER 2', 'Chapter 2: Software Requirement Specification'))
    story.append(Paragraph("CHAPTER 2", chapter_num_style))
    story.append(Paragraph("(Full Stack Projects)<br/>SOFTWARE REQUIREMENT SPECIFICATION", chapter_title_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_primary, spaceBefore=0, spaceAfter=10))

    story.append(Paragraph("2.1 Product Perspective", sec_head_style))
    story.append(Paragraph(
        "CrimeLens 2.0 is an independent, self-contained, enterprise-grade full-stack web application. "
        "It provides a dual-facing public safety platform: an intuitive consumer corridor navigator for commuters, and a tactical command "
        "hub for municipal patrol dispatchers. The system is entirely software-driven and interfaces seamlessly across standard web protocols. "
        "Unlike existing commercial navigation platforms that treat safety as an afterthought, CrimeLens 2.0 places safety-aware routing at the "
        "core of its computational engine. The product is designed to be deployed on standard cloud infrastructure (AWS, GCP, or Azure) or "
        "on-premises municipal data centers without requiring specialized hardware accelerators.", body_style))

    story.append(Paragraph("2.1.1 System Interfaces", subsec_head_style))
    story.append(Paragraph(
        "The system interfaces with client applications via 26 strongly-typed JSON RESTful API endpoints hosted on an asynchronous FastAPI server. "
        "CORS middleware enables secure data exchange with third-party municipal portals and mobile frontends. The API surface is organized into "
        "four functional groups: (1) SafePath routing endpoints for corridor computation and graph queries; (2) Patrol optimization endpoints for "
        "fleet allocation and dispatch operations; (3) Machine learning prediction endpoints for crime rate forecasting and XAI attributions; and "
        "(4) System health and configuration endpoints for monitoring and administration.", body_style))

    story.append(Paragraph("2.1.2 User Interfaces", subsec_head_style))
    story.append(Paragraph(
        "The user interface is an accessible, responsive Single Page Application (SPA) built with React 18, TypeScript, and Tailwind CSS. "
        "It renders dual route comparison polylines (red for shortest path vs. green for safe corridor), dynamic safety weight sliders "
        "(lambda in the range [0, 5]), fleet allocation cards with real-time response time indicators, and interactive What-If policy simulation "
        "controls. The interface follows WCAG 2.1 AA accessibility guidelines and is fully responsive across desktop, tablet, and mobile viewports. "
        "The map visualization layer uses Leaflet.js with OpenStreetMap tile integration for rendering GeoJSON polyline overlays and interactive "
        "marker clusters.", body_style))

    story.append(Paragraph("2.1.3 Hardware Interfaces (Pure Software Rationale)", subsec_head_style))
    story.append(Paragraph(
        "<b>The system has no hardware interface requirements.</b> As stipulated in the institutional project guidelines for pure software systems, "
        "CrimeLens 2.0 does not interact with, control, or depend upon any physical IoT microcontrollers, Raspberry Pi devices, panic buttons, "
        "GPS trackers, or wearable hardware. The software operates agnostically across standard computing devices (laptops, smartphones, cloud VMs) "
        "via standard web browsers. This hardware independence is a deliberate architectural decision that ensures zero capital expenditure on "
        "physical infrastructure and eliminates maintenance overhead, environmental degradation, and geographic coverage limitations.", body_style))

    story.append(Paragraph("2.1.4 Software Interfaces", subsec_head_style))
    story.append(Paragraph(
        "The platform interfaces with required open-source software libraries and frameworks summarized in Table 2.1.", body_style))

    story.append(Paragraph("TABLE 2.1. Comparison Of Required Software Stack Components &amp; Interfaces", table_title_style))
    t_stack_data = [
        [Paragraph("Component", table_cell_header), Paragraph("Software Name", table_cell_header), Paragraph("Version", table_cell_header), Paragraph("Role &amp; Interface Format", table_cell_header)],
        [Paragraph("Application Server", table_cell_bold), Paragraph("FastAPI / Uvicorn", table_cell_style), Paragraph("0.115 / 0.32", table_cell_style), Paragraph("Asynchronous REST API, JSON over HTTP/HTTPS", table_cell_style)],
        [Paragraph("Client Framework", table_cell_bold), Paragraph("React + TypeScript + Vite", table_cell_style), Paragraph("18.3 / 5.4", table_cell_style), Paragraph("SPA rendering, state management, responsive UI", table_cell_style)],
        [Paragraph("Spatial Map Engine", table_cell_bold), Paragraph("Leaflet.js / React-Leaflet", table_cell_style), Paragraph("1.9.4", table_cell_style), Paragraph("OSM tile layer and GeoJSON polyline overlay", table_cell_style)],
        [Paragraph("Machine Learning", table_cell_bold), Paragraph("scikit-learn / NumPy / pandas", table_cell_style), Paragraph("1.6.0+", table_cell_style), Paragraph("GB, RF, Ridge, and XAI feature attributions", table_cell_style)],
        [Paragraph("Styling Framework", table_cell_bold), Paragraph("Tailwind CSS", table_cell_style), Paragraph("3.4", table_cell_style), Paragraph("Utility-first responsive CSS design system", table_cell_style)],
        [Paragraph("Build Toolchain", table_cell_bold), Paragraph("Vite + Node.js", table_cell_style), Paragraph("5.4 / 20.x", table_cell_style), Paragraph("HMR dev server, production bundling, tree-shaking", table_cell_style)]
    ]
    t_stack = Table(t_stack_data, colWidths=[90, 115, 65, 225])
    t_stack.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_stack)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2.1.5 Communications Interfaces", subsec_head_style))
    story.append(Paragraph(
        "Communication uses standard HTTP/1.1 and HTTP/2 over TLS 1.3 encryption. Payload serializations adhere to OpenAPI 3.0 JSON schemas. "
        "All API requests and responses are validated using Pydantic data models to ensure type safety and schema conformance.", body_style))

    story.append(Paragraph("2.1.6 Memory Constraints", subsec_head_style))
    story.append(Paragraph(
        "The server memory footprint does not exceed 512 MB of RAM. The in-memory spatial graph representation for 21 nodes and 32 edges "
        "requires less than 2 KB. Graph pathfinding completes in under 25 milliseconds, and machine learning inference executes in under 10 milliseconds.", body_style))

    story.append(Paragraph("2.1.7 Operations", subsec_head_style))
    story.append(Paragraph(
        "The system operates in 24/7 interactive web mode with stateless endpoints, supporting rolling deployments without downtime. "
        "No scheduled batch processing is required; all computations are triggered by real-time user requests.", body_style))

    story.append(Paragraph("2.1.8 Site Adaptation Requirements", subsec_head_style))
    story.append(Paragraph(
        "Adapting the platform to a new municipality requires only uploading a standard GeoJSON street network and municipal beat crime catalog "
        "in CSV format. The system automatically constructs the in-memory spatial graph and recalibrates the machine learning models based on the "
        "new dataset.", body_style))

    story.append(Paragraph("2.2 Product Functions &amp; Functional Requirements", sec_head_style))
    story.append(Paragraph(
        "The product functions are formally specified in Table 2.2 across each major functional subsystem:", body_style))

    # Table 2.2: Functional Requirements Matrix
    story.append(Paragraph("TABLE 2.2. Comprehensive Functional Requirements Specification Matrix", table_title_style))
    fr_data = [
        [Paragraph("Req ID", table_cell_header), Paragraph("Subsystem", table_cell_header), Paragraph("Functional Description", table_cell_header), Paragraph("Input Parameters", table_cell_header), Paragraph("Expected Output", table_cell_header), Paragraph("Priority", table_cell_header)],
        [Paragraph("FR-01", table_cell_bold), Paragraph("SafePath", table_cell_style), Paragraph("Dual route pathfinding", table_cell_style), Paragraph("Origin, Dest, lambda, Time", table_cell_style), Paragraph("Shortest &amp; Safe polylines", table_cell_style), Paragraph("High", table_cell_bold)],
        [Paragraph("FR-02", table_cell_bold), Paragraph("SafePath", table_cell_style), Paragraph("Dynamic Safety Indexing", table_cell_style), Paragraph("Edge crime, light, patrol", table_cell_style), Paragraph("Normalized DSI score [0,1]", table_cell_style), Paragraph("High", table_cell_bold)],
        [Paragraph("FR-03", table_cell_bold), Paragraph("SafePath", table_cell_style), Paragraph("Nocturnal risk penalty", table_cell_style), Paragraph("Departure hour", table_cell_style), Paragraph("+0.25 penalty if 20:00-05:00", table_cell_style), Paragraph("Medium", table_cell_style)],
        [Paragraph("FR-04", table_cell_bold), Paragraph("Patrol", table_cell_style), Paragraph("Diminishing returns fleet alloc", table_cell_style), Paragraph("Total fleet units (U)", table_cell_style), Paragraph("Optimal beat assignments", table_cell_style), Paragraph("High", table_cell_bold)],
        [Paragraph("FR-05", table_cell_bold), Paragraph("Patrol", table_cell_style), Paragraph("Tactical beat dispatch", table_cell_style), Paragraph("Target Beat ID", table_cell_style), Paragraph("Incremented patrol count", table_cell_style), Paragraph("Medium", table_cell_style)],
        [Paragraph("FR-06", table_cell_bold), Paragraph("ML Suite", table_cell_style), Paragraph("Crime rate regression", table_cell_style), Paragraph("Beat spatial features", table_cell_style), Paragraph("Predicted crime incidence", table_cell_style), Paragraph("High", table_cell_bold)],
        [Paragraph("FR-07", table_cell_bold), Paragraph("ML Suite", table_cell_style), Paragraph("90% Confidence Interval", table_cell_style), Paragraph("Feature vector", table_cell_style), Paragraph("[Lower CI, Upper CI]", table_cell_style), Paragraph("High", table_cell_bold)],
        [Paragraph("FR-08", table_cell_bold), Paragraph("ML Suite", table_cell_style), Paragraph("XAI Waterfall attribution", table_cell_style), Paragraph("Feature vector", table_cell_style), Paragraph("Marginal feature SHAP bars", table_cell_style), Paragraph("High", table_cell_bold)],
        [Paragraph("FR-09", table_cell_bold), Paragraph("Simulation", table_cell_style), Paragraph("What-If policy modeling", table_cell_style), Paragraph("Delta light %, Delta patrol", table_cell_style), Paragraph("Recalculated crime rate", table_cell_style), Paragraph("Medium", table_cell_style)],
        [Paragraph("FR-10", table_cell_bold), Paragraph("Geospatial", table_cell_style), Paragraph("Leaflet map visualization", table_cell_style), Paragraph("GeoJSON paths &amp; markers", table_cell_style), Paragraph("Interactive browser render", table_cell_style), Paragraph("High", table_cell_bold)]
    ]
    t_fr = Table(fr_data, colWidths=[45, 60, 120, 110, 115, 45])
    t_fr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_fr)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2.3 User Characteristics &amp; Non-Functional Requirements", sec_head_style))
    story.append(Paragraph(
        "Target user personas include: (1) <i>Citizens/Commuters</i> seeking safe walking paths; (2) <i>Patrol Commanders</i> requiring "
        "fleet deployment intelligence; and (3) <i>Crime Data Analysts</i> requiring explainable ML forecasting. "
        "System non-functional requirements are specified in Table 2.3.", body_style))

    # Table 2.3: Non-Functional Requirements
    story.append(Paragraph("TABLE 2.3. System Non-Functional Requirements (NFR) Matrix", table_title_style))
    nfr_data = [
        [Paragraph("NFR ID", table_cell_header), Paragraph("Quality Attribute", table_cell_header), Paragraph("Quantitative Target Metric", table_cell_header), Paragraph("Validation Mechanism", table_cell_header)],
        [Paragraph("NFR-01", table_cell_bold), Paragraph("API Latency", table_cell_style), Paragraph("&lt; 50 ms for routing and ML inference", table_cell_style), Paragraph("Automated benchmark test suite (TC-11)", table_cell_style)],
        [Paragraph("NFR-02", table_cell_bold), Paragraph("Throughput", table_cell_style), Paragraph("&gt;= 500 concurrent requests/sec on single core", table_cell_style), Paragraph("Uvicorn ASGI stress benchmarking", table_cell_style)],
        [Paragraph("NFR-03", table_cell_bold), Paragraph("Memory Footprint", table_cell_style), Paragraph("&lt; 512 MB RAM under full operational load", table_cell_style), Paragraph("Process memory profiling via psutil", table_cell_style)],
        [Paragraph("NFR-04", table_cell_bold), Paragraph("Availability", table_cell_style), Paragraph("99.9% uptime with stateless endpoints", table_cell_style), Paragraph("Docker healthcheck / Cloud monitoring", table_cell_style)],
        [Paragraph("NFR-05", table_cell_bold), Paragraph("Accessibility", table_cell_style), Paragraph("WCAG 2.1 Level AA color contrast compliance", table_cell_style), Paragraph("Lighthouse accessibility audit score &gt;= 95", table_cell_style)],
        [Paragraph("NFR-06", table_cell_bold), Paragraph("Data Privacy", table_cell_style), Paragraph("Zero logging of personal coordinate histories", table_cell_style), Paragraph("Stateless query processing architecture", table_cell_style)],
        [Paragraph("NFR-07", table_cell_bold), Paragraph("Transport Security", table_cell_style), Paragraph("TLS 1.3 encryption across all REST endpoints", table_cell_style), Paragraph("HTTPS endpoint certificate inspection", table_cell_style)],
        [Paragraph("NFR-08", table_cell_bold), Paragraph("Portability", table_cell_style), Paragraph("100% pure software, zero IoT hardware dependency", table_cell_style), Paragraph("Execution on standard commodity laptops", table_cell_style)]
    ]
    t_nfr = Table(nfr_data, colWidths=[55, 95, 185, 160])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5), ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_nfr)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2.4 Constraints", sec_head_style))
    story.append(Paragraph(
        "1. Algorithmic impartiality: models are trained strictly on spatial, environmental, and infrastructural features, excluding demographic "
        "profiling of any kind. 2. Client execution is 100% browser-based with zero native plugin installations. 3. REST APIs are stateless, "
        "enabling frictionless cloud horizontal scaling. 4. All computations must complete within 50ms to maintain real-time responsiveness. "
        "5. The system must comply with Indian data privacy regulations regarding citizen location data.", body_style))

    story.append(Paragraph("2.5 Assumptions and Dependencies", sec_head_style))
    story.append(Paragraph(
        "Assumes road network connectivity representable as a planar graph G = (V, E), active client network connectivity for map tile retrieval, "
        "and emergency response travel speeds conforming to Poisson area-coverage principles. The system assumes that municipal crime records "
        "and infrastructure data are updated periodically (at least quarterly) to maintain prediction accuracy.", body_style))

    story.append(Paragraph("2.6 Apportioning of Requirements", sec_head_style))
    story.append(Paragraph(
        "Phase 1 (Implemented): SafePath routing, patrol optimization, multi-model ML benchmarking, XAI waterfall attributions, and What-If simulation. "
        "Phase 2 (Future): Automated real-time police CAD integration, multi-agent reinforcement learning fleet roaming, and OpenStreetMap Overpass API "
        "automated graph ingestion.", body_style))

    story.append(Paragraph("2.7 Use Case Modeling", sec_head_style))

    story.append(Paragraph("2.7.1 Use Case Diagram", subsec_head_style))
    story.append(Paragraph(
        "Figure 2.1 illustrates the use case model depicting primary actors and their interactions with the CrimeLens 2.0 system. "
        "The diagram identifies three primary actors (Citizen, Patrol Commander, Data Analyst) and their associated use cases across "
        "the SafePath, Patrol Optimization, and ML Prediction modules.", body_style))
    uc_img_path = os.path.join(fig_dir, 'usecase_diagram.png')
    if os.path.exists(uc_img_path):
        story.append(KeepTogether([
            Image(uc_img_path, width=content_width, height=content_width * 0.48),
            Paragraph("Figure 2.1: CrimeLens 2.0 Use Case Interaction Model", caption_style)
        ]))

    story.append(Paragraph("2.7.2 Use Case Scenarios", subsec_head_style))
    story.append(Paragraph(
        "The detailed use case scenarios for SafePath Corridor Navigation and Patrol Optimization are formatted in accordance with the prescribed institutional schema:", body_style))

    # Table 2.4 (SafePath)
    story.append(Paragraph("TABLE 2.4. SafePath Route Query Use Case Scenario (UC-01)", table_title_style))
    t_uc1_data = [
        [Paragraph("Use Case Element", table_cell_header), Paragraph("Description", table_cell_header)],
        [Paragraph("Use Case Number", table_cell_bold), Paragraph("UC-01", table_cell_style)],
        [Paragraph("Application", table_cell_bold), Paragraph("CrimeLens 2.0 Safe Corridor Navigation Module", table_cell_style)],
        [Paragraph("Use Case Name", table_cell_bold), Paragraph("SafePath Multi-Criteria Corridor Routing", table_cell_style)],
        [Paragraph("Use Case Description", table_cell_bold), Paragraph("Calculates and displays both the shortest route and the risk-penalized illuminated safe corridor between two urban points.", table_cell_style)],
        [Paragraph("Primary Actor", table_cell_bold), Paragraph("Citizen / Commuter", table_cell_style)],
        [Paragraph("Precondition", table_cell_bold), Paragraph("User accesses the SafePath web portal; spatial road graph is active and loaded.", table_cell_style)],
        [Paragraph("Trigger", table_cell_bold), Paragraph("User selects origin and destination nodes and clicks 'Calculate SafePath'.", table_cell_style)],
        [Paragraph("Basic Flow", table_cell_bold), Paragraph(
            "1. User specifies Origin (e.g., Connaught Place), Destination (e.g., Hauz Khas), Safety Weight (lambda = 2.0), and Departure Time.<br/>"
            "2. System computes Dynamic Safety Index S(e) for each edge incorporating crime, lighting, patrol, and temporal factors.<br/>"
            "3. System runs dual-Dijkstra search to obtain Shortest Path and Safe Corridor simultaneously.<br/>"
            "4. System overlays comparative polylines (red/green) and displays danger reduction metrics (-66.7%).<br/>"
            "5. System presents waypoint-by-waypoint navigation with cumulative distance and safety score.", table_cell_style)],
        [Paragraph("Alternate Flows", table_cell_bold), Paragraph("If Origin and Destination are identical, system returns HTTP 400 prompting distinct endpoints. If no path exists, system returns HTTP 404 with explanation.", table_cell_style)],
        [Paragraph("Postcondition", table_cell_bold), Paragraph("User can view, compare, and select between shortest and safest routes with full analytics.", table_cell_style)]
    ]
    t_uc1 = Table(t_uc1_data, colWidths=[120, 375])
    t_uc1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_uc1)
    story.append(Spacer(1, 6))

    # Table 2.5 (Patrol)
    story.append(Paragraph("TABLE 2.5. Patrol Fleet Allocation Use Case Scenario (UC-02)", table_title_style))
    t_uc2_data = [
        [Paragraph("Use Case Element", table_cell_header), Paragraph("Description", table_cell_header)],
        [Paragraph("Use Case Number", table_cell_bold), Paragraph("UC-02", table_cell_style)],
        [Paragraph("Application", table_cell_bold), Paragraph("CrimeLens 2.0 Smart Patrol Command Center", table_cell_style)],
        [Paragraph("Use Case Name", table_cell_bold), Paragraph("Patrol Fleet Allocation Optimization", table_cell_style)],
        [Paragraph("Use Case Description", table_cell_bold), Paragraph("Optimizes patrol vehicle distribution across beats to minimize emergency response latency using diminishing returns model.", table_cell_style)],
        [Paragraph("Primary Actor", table_cell_bold), Paragraph("Patrol Commander / Dispatcher", table_cell_style)],
        [Paragraph("Precondition", table_cell_bold), Paragraph("Commander authenticated; municipal beat risk scores and fleet inventory loaded.", table_cell_style)],
        [Paragraph("Trigger", table_cell_bold), Paragraph("Commander enters total fleet count (e.g., 20) and clicks 'Optimize Fleet'.", table_cell_style)],
        [Paragraph("Basic Flow", table_cell_bold), Paragraph(
            "1. Commander inputs total fleet units available for allocation.<br/>"
            "2. System executes non-linear diminishing returns optimization R(u) = R<sub>0</sub> / sqrt(u).<br/>"
            "3. System displays optimal unit allocation and projected response times per beat.<br/>"
            "4. Commander reviews allocation and dispatches emergency units with one-click tactical controls.", table_cell_style)],
        [Paragraph("Alternate Flows", table_cell_bold), Paragraph("If fleet count is less than active beats, system prioritizes top-tier severity beats and flags low-fleet warning.", table_cell_style)],
        [Paragraph("Postcondition", table_cell_bold), Paragraph("All patrol units are allocated; response time projections are updated system-wide.", table_cell_style)]
    ]
    t_uc2 = Table(t_uc2_data, colWidths=[120, 375])
    t_uc2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_uc2)
    story.append(Spacer(1, 4))

    story.append(Paragraph("2.7.3 Sequence Diagram Description", subsec_head_style))
    story.append(Paragraph(
        "The interaction sequence for SafePath routing proceeds as follows: "
        "The client browser emits an HTTP POST request with query payload to <code>/api/safepath/route</code>. "
        "The FastAPI gateway validates the schema using Pydantic models. The <code>SafePathEngine</code> evaluates the Dynamic Safety Index "
        "across candidate graph edges incorporating crime density, lighting scores, patrol coverage, and temporal penalties. The engine then "
        "executes the priority-queue Dijkstra solver for both shortest and safest path objectives. The response payload containing waypoints, "
        "distance, danger score, and reduction percentage is delivered to the client within 25ms, triggering asynchronous Leaflet polyline rendering "
        "with animated path drawing and color-coded risk visualization.", body_style))

    story.append(PageBreak())
