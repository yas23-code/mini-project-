import os
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image, HRFlowable
from reportlab.lib import colors

def add_chapter3(story, PageMarker, styles, fig_dir, content_width):
    c_primary = styles['c_primary']
    c_secondary = styles['c_secondary']
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
    # CHAPTER 3: SYSTEM DESIGN
    # =========================================================================
    story.append(PageMarker('CHAPTER 3', 'Chapter 3: System Design'))
    story.append(Paragraph("CHAPTER 3", chapter_num_style))
    story.append(Paragraph("(For Full Stack Projects)<br/>SYSTEM DESIGN", chapter_title_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_primary, spaceBefore=0, spaceAfter=8))

    story.append(Paragraph(
        "System Design encompasses the structural, behavioral, and algorithmic architecture of CrimeLens 2.0. "
        "The system adheres to standard full-stack engineering paradigms, completely decoupled across three distinct tiers. "
        "All architectural diagrams, data flows, relational entities, and algorithmic theorems are formally delineated below.", callout_style))
    story.append(Spacer(1, 4))

    # 3.1 3-TIER ARCHITECTURE
    story.append(Paragraph("3.1 3-Tier Architecture &amp; System Flow", sec_head_style))
    story.append(Paragraph(
        "CrimeLens 2.0 implements a modular 3-Tier Architecture separating presentation, business logic, and data persistence, as shown in Figure 3.1. "
        "The architecture follows modern asynchronous distributed system standards, ensuring strict loose coupling and high cohesion across all layers:", body_style))
    story.append(Paragraph(
        "* <b>Presentation Tier (Client Layer):</b> Engineered as a high-performance Single Page Application (SPA) utilizing React 18.3, "
        "TypeScript 5.5, and Tailwind CSS. Spatial GIS mapping is executed client-side via Leaflet.js with reactive React-Leaflet bindings. "
        "The client manages ephemeral UI state through React Context providers and custom hooks, delivering sub-second visual transitions, "
        "interactive parameter sliders, and dual polyline route renderings without requiring full-page browser refreshes.", bullet_style))
    story.append(Paragraph(
        "* <b>Application Tier (Business Logic Layer):</b> Built on Python 3.14 with FastAPI 0.115 and the high-throughput Uvicorn ASGI server. "
        "The application tier hosts 26 RESTful endpoints partitioned into four core micro-modules: SafePath Routing Engine, Smart Patrol Fleet "
        "Optimizer, Explainable ML Predictive Suite, and System Administration. It enforces strict input data validation via Pydantic v2 schemas, "
        "manages cross-origin resource sharing (CORS), and executes concurrent non-blocking asynchronous event loops.", bullet_style))
    story.append(Paragraph(
        "* <b>Data Persistence Tier (Storage Layer):</b> Utilizes an in-memory spatial graph representation backed by adjacency-list dictionaries "
        "for O(1) vertex and edge traversal. Relational jurisdictional beat datasets, municipal infrastructure records, and historical crime incident "
        "logs are structured in tabular CSV formats with on-startup caching into optimized pandas DataFrames and NumPy memory matrices.", bullet_style))

    arch_img_path = os.path.join(fig_dir, 'system_architecture.png')
    if os.path.exists(arch_img_path):
        story.append(KeepTogether([
            Image(arch_img_path, width=content_width, height=content_width * 0.48),
            Paragraph("Figure 3.1: 3-Tier Architecture Diagram for CrimeLens 2.0 Full Stack System", caption_style)
        ]))

    story.append(Paragraph("3.1.1 Architectural Design Patterns Applied", subsec_head_style))
    story.append(Paragraph(
        "To ensure maintainability, scalability, and code testability, four classical Gang of Four (GoF) design patterns are integrated into the core codebase:", body_style))
    story.append(Paragraph(
        "* <b>Repository Pattern:</b> Isolates the spatial graph topology and municipal beat repositories from routing and optimization business logic. "
        "Data access classes expose standardized query interfaces (e.g., get_neighbors(), get_beat_by_id()), allowing storage backends to transition from CSV "
        "to PostgreSQL/PostGIS seamlessly without altering pathfinding algorithms.", bullet_style))
    story.append(Paragraph(
        "* <b>Strategy Pattern:</b> Encapsulates graph traversal cost evaluation. The routing engine dynamically selects between a pure distance-minimizing "
        "strategy (lambda = 0), a composite multi-criteria safety strategy (lambda &gt; 0), and a nocturnal penalty strategy depending on request parameters.", bullet_style))
    story.append(Paragraph(
        "* <b>Factory Method Pattern:</b> Instantiates machine learning regression estimators dynamically within the ML predictive suite. Depending on client "
        "payload specifications, the factory provisions trained instances of Gradient Boosting, Random Forest, or Ridge Regression models.", bullet_style))
    story.append(Paragraph(
        "* <b>Observer Pattern:</b> Governs patrol fleet dispatch operations. When a dispatcher assigns patrol units to a beat, registered observers trigger "
        "automatic recalculation of jurisdictional latency metrics and broadcast updated beat status to connected dashboard clients.", bullet_style))

    # 3.2 CLASS DIAGRAMS & COMPONENT SPECIFICATIONS
    story.append(Paragraph("3.2 Class Diagrams &amp; Component Specifications", sec_head_style))
    story.append(Paragraph(
        "The object-oriented domain model of CrimeLens 2.0 is partitioned into five primary domain classes that encapsulate business rules and invariants:", body_style))
    story.append(Paragraph(
        "* <b>RoadGraph (Spatial Network Model):</b> Represents the urban road network as an undirected attributed graph G = (V, E). "
        "Encapsulates dictionary-based adjacency lists adj: Dict[str, List[Edge]] and vertex mappings nodes: Dict[str, Node]. Exposes methods "
        "add_node(node_id, lat, lon), add_edge(u, v, dist, crime, light), and compute_dynamic_edge_cost(edge, lambda_w, is_night). "
        "Guarantees O(1) edge retrieval and O(|V| + |E|) memory footprint.", bullet_style))
    story.append(Paragraph(
        "* <b>SafePathEngine (Multi-Criteria Routing Service):</b> Implements multi-objective priority-queue Dijkstra pathfinding. "
        "Exposes find_shortest_path(origin, dest) returning the baseline distance path and find_safe_corridor(origin, dest, lambda_w, time) "
        "returning the risk-penalized path. Contains compute_corridor_metrics() which calculates distance overhead and danger reduction percentages.", bullet_style))
    story.append(Paragraph(
        "* <b>BeatRecord (Municipal Domain Entity):</b> Encapsulates jurisdictional police beat properties: beat_id: int, beat_name: str, "
        "risk_score: float, lighting_score: float, patrol_units: int, and response_time: float. Enforces domain invariants: 0 &lt;= risk_score &lt;= 100 "
        "and patrol_units &gt;= 1.", bullet_style))
    story.append(Paragraph(
        "* <b>PatrolOptimizer (Diminishing Marginal Returns Dispatcher):</b> Implements greedy submodular resource distribution. "
        "Encapsulates optimize_fleet(total_units, beats) which allocates vehicles to minimize city-wide response latency, and dispatch_unit(beat_id) "
        "which dynamically handles emergency reinforcement.", bullet_style))
    story.append(Paragraph(
        "* <b>CrimeMLSuite (Explainable Predictive Service):</b> Manages machine learning regression models. Exposes train_models(), "
        "predict_risk(features), get_waterfall_attribution(features), and simulate_what_if(beat_id, delta_lighting, delta_patrol). "
        "Computes 90% confidence intervals using bootstrap residual standard error estimation.", bullet_style))

    # 3.3 DATA FLOW DIAGRAMS
    story.append(Paragraph("3.3 Data Flow Diagrams (DFD)", sec_head_style))
    story.append(Paragraph(
        "The system's functional data flow operates across three hierarchical abstraction levels:", body_style))
    story.append(Paragraph(
        "* <b>Level 0 (Context Diagram):</b> Depicts the macro system boundaries of CrimeLens 2.0. External entities include the Citizen/Commuter, "
        "the Police Patrol Commander, and the Municipal City Planner. Citizens submit origin, destination, and safety weighting parameters and receive "
        "navigable safe corridor GeoJSON routes. Commanders supply available fleet counts and dispatch directives and receive optimal unit allocations. "
        "Planners supply infrastructure modification values (e.g., lighting upgrades) and receive What-If crime risk projections with confidence bounds.", bullet_style))
    story.append(Paragraph(
        "* <b>Level 1 (System Decomposition):</b> Deconstructs the core architecture into four primary processes: "
        "Process 1.0 (Spatial Network Ingestion &amp; Topology Indexing), Process 2.0 (SafePath Multi-Criteria Pathfinding), "
        "Process 3.0 (Patrol Fleet Diminishing Returns Optimization), and Process 4.0 (Explainable Predictive Risk Modeling). "
        "Two persistent stores are maintained: Data Store D1 (Spatial Network &amp; Edge Attributes Store) and Data Store D2 (Municipal Beat &amp; Crime Statistics Registry).", bullet_style))
    story.append(Paragraph(
        "* <b>Level 2 (Subsystem Data Flows):</b> Delineates the internal pipeline of Process 2.0: Sub-process 2.1 validates origin and destination node identifiers. "
        "Sub-process 2.2 queries D1 to retrieve candidate road segments. Sub-process 2.3 computes the Dynamic Safety Index S(e) incorporating real-time "
        "nocturnal penalties T(t). Sub-process 2.4 executes min-heap dual-Dijkstra traversal to extract shortest and safest node sequences. Sub-process 2.5 "
        "assembles GeoJSON coordinate arrays, calculates comparative safety metrics, and streams the serialized JSON response to the presentation tier.", bullet_style))

    # 3.4 ACTIVITY DIAGRAM
    story.append(Paragraph("3.4 Activity Diagram &amp; Operational Workflow", sec_head_style))
    story.append(Paragraph(
        "Figure 3.2 illustrates the operational activity workflow of the SafePath routing decision process, mapping the sequential logic "
        "from initial user interaction through dual graph evaluation to final cartographic rendering.", body_style))

    act_img_path = os.path.join(fig_dir, 'activity_diagram.png')
    if os.path.exists(act_img_path):
        story.append(KeepTogether([
            Image(act_img_path, width=content_width, height=content_width * 0.40),
            Paragraph("Figure 3.2: SafePath Activity Diagram (Routing Decision Workflow)", caption_style)
        ]))

    story.append(Paragraph(
        "The activity workflow proceeds through four sequential execution phases: (1) Parameter Acquisition, where the user selects origin, destination, "
        "and lambda safety preference via the React interface; (2) Spatial Snapping, where GPS coordinates are validated against graph node boundaries; "
        "(3) Dual Cost Evaluation, where the backend concurrently computes unweighted physical shortest path and safety-penalized optimal corridor; "
        "and (4) Map Visualization, where dual polylines are overlaid on Leaflet with comparative safety metrics displayed on an analytical HUD panel.", body_style))

    # 3.5 RELATIONAL DATABASE SCHEMA
    story.append(Paragraph("3.5 Relational Database Schema &amp; Topology Definition", sec_head_style))
    story.append(Paragraph(
        "The persistence model governs municipal beats, spatial road segments, and intersection nodes. Tables 3.1, 3.2, and 3.3 detail the primary relational schemas.", body_style))

    story.append(Paragraph("TABLE 3.1. Relational Database Schema &amp; Field Definitions (Beat &amp; RoadEdge)", table_title_style))
    t_schema_data = [
        [Paragraph("Table Name", table_cell_header), Paragraph("Field Name", table_cell_header), Paragraph("Data Type", table_cell_header), Paragraph("Constraints", table_cell_header), Paragraph("Description", table_cell_header)],
        [Paragraph("Beat", table_cell_bold), Paragraph("beat_id", table_cell_bold), Paragraph("INTEGER", table_cell_style), Paragraph("PRIMARY KEY", table_cell_style), Paragraph("Unique beat ID (1..12)", table_cell_style)],
        [Paragraph("Beat", table_cell_bold), Paragraph("beat_name", table_cell_style), Paragraph("VARCHAR(64)", table_cell_style), Paragraph("NOT NULL, UNIQUE", table_cell_style), Paragraph("Locality name (e.g., Connaught Place)", table_cell_style)],
        [Paragraph("Beat", table_cell_bold), Paragraph("risk_score", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("CHECK(0 &lt;= val &lt;= 100)", table_cell_style), Paragraph("Composite crime severity index", table_cell_style)],
        [Paragraph("Beat", table_cell_bold), Paragraph("lighting_score", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("CHECK(0 &lt;= val &lt;= 100)", table_cell_style), Paragraph("Municipal lighting coverage", table_cell_style)],
        [Paragraph("Beat", table_cell_bold), Paragraph("patrol_units", table_cell_style), Paragraph("INTEGER", table_cell_style), Paragraph("DEFAULT 1, &gt;= 0", table_cell_style), Paragraph("Stationed patrol fleet vehicles", table_cell_style)],
        [Paragraph("Beat", table_cell_bold), Paragraph("response_time", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("COMPUTED", table_cell_style), Paragraph("Projected emergency response minutes", table_cell_style)],
        [Paragraph("RoadEdge", table_cell_bold), Paragraph("edge_id", table_cell_bold), Paragraph("INTEGER", table_cell_style), Paragraph("PRIMARY KEY", table_cell_style), Paragraph("Unique road segment identifier", table_cell_style)],
        [Paragraph("RoadEdge", table_cell_bold), Paragraph("u, v", table_cell_style), Paragraph("VARCHAR(32)", table_cell_style), Paragraph("FOREIGN KEY", table_cell_style), Paragraph("Connecting intersection nodes", table_cell_style)],
        [Paragraph("RoadEdge", table_cell_bold), Paragraph("distance_km", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("NOT NULL, &gt; 0", table_cell_style), Paragraph("Physical segment distance in km", table_cell_style)],
        [Paragraph("RoadEdge", table_cell_bold), Paragraph("crime_score", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("0 &lt;= val &lt;= 1", table_cell_style), Paragraph("Normalized crime density", table_cell_style)],
        [Paragraph("RoadEdge", table_cell_bold), Paragraph("lighting", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("0 &lt;= val &lt;= 1", table_cell_style), Paragraph("Street illumination coverage", table_cell_style)]
    ]
    t_schema = Table(t_schema_data, colWidths=[65, 75, 70, 115, 170])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 6))

    # Table 3.2 (Nodes Schema)
    story.append(Paragraph("TABLE 3.2. Spatial Intersection Nodes Schema &amp; Topology Definition", table_title_style))
    t_node_data = [
        [Paragraph("Field Name", table_cell_header), Paragraph("Data Type", table_cell_header), Paragraph("Constraints", table_cell_header), Paragraph("Functional Role in Spatial Graph G=(V,E)", table_cell_header)],
        [Paragraph("node_id", table_cell_bold), Paragraph("VARCHAR(32)", table_cell_style), Paragraph("PRIMARY KEY", table_cell_style), Paragraph("Unique topological identifier (e.g., 'CP', 'HK', 'DW')", table_cell_style)],
        [Paragraph("node_name", table_cell_bold), Paragraph("VARCHAR(64)", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("Human-readable landmark (e.g., 'Connaught Place Radial')", table_cell_style)],
        [Paragraph("latitude", table_cell_bold), Paragraph("DECIMAL(9,6)", table_cell_style), Paragraph("NOT NULL, CHECK(-90..90)", table_cell_style), Paragraph("WGS84 geographic latitude coordinate", table_cell_style)],
        [Paragraph("longitude", table_cell_bold), Paragraph("DECIMAL(9,6)", table_cell_style), Paragraph("NOT NULL, CHECK(-180..180)", table_cell_style), Paragraph("WGS84 geographic longitude coordinate", table_cell_style)],
        [Paragraph("beat_id", table_cell_bold), Paragraph("INTEGER", table_cell_style), Paragraph("FOREIGN KEY (Beat)", table_cell_style), Paragraph("Jurisdictional police beat overseeing node", table_cell_style)],
        [Paragraph("node_type", table_cell_bold), Paragraph("VARCHAR(20)", table_cell_style), Paragraph("CHECK(transit, comm, res)", table_cell_style), Paragraph("Urban morphology type: Transit hub, Commercial, or Residential", table_cell_style)]
    ]
    t_node = Table(t_node_data, colWidths=[80, 85, 120, 210])
    t_node.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_node)
    story.append(Spacer(1, 6))

    # Table 3.3 (Dispatch Audit Trail & Simulation Schema)
    story.append(Paragraph("TABLE 3.3. Dispatch Audit Trail &amp; What-If Simulation Event Schema", table_title_style))
    t_audit_data = [
        [Paragraph("Table Name", table_cell_header), Paragraph("Field Name", table_cell_header), Paragraph("Data Type", table_cell_header), Paragraph("Constraints", table_cell_header), Paragraph("Description", table_cell_header)],
        [Paragraph("DispatchLog", table_cell_bold), Paragraph("log_id", table_cell_bold), Paragraph("INTEGER", table_cell_style), Paragraph("PRIMARY KEY, AUTO", table_cell_style), Paragraph("Unique dispatch operation ID", table_cell_style)],
        [Paragraph("DispatchLog", table_cell_bold), Paragraph("beat_id", table_cell_style), Paragraph("INTEGER", table_cell_style), Paragraph("FOREIGN KEY (Beat)", table_cell_style), Paragraph("Recipient police beat ID", table_cell_style)],
        [Paragraph("DispatchLog", table_cell_bold), Paragraph("units_added", table_cell_style), Paragraph("INTEGER", table_cell_style), Paragraph("NOT NULL, &gt;= 1", table_cell_style), Paragraph("Number of vehicles dispatched", table_cell_style)],
        [Paragraph("DispatchLog", table_cell_bold), Paragraph("prev_latency", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("NOT NULL, &gt; 0", table_cell_style), Paragraph("Response time before dispatch (min)", table_cell_style)],
        [Paragraph("DispatchLog", table_cell_bold), Paragraph("post_latency", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("NOT NULL, &gt; 0", table_cell_style), Paragraph("Response time after dispatch (min)", table_cell_style)],
        [Paragraph("SimulationLog", table_cell_bold), Paragraph("sim_id", table_cell_bold), Paragraph("INTEGER", table_cell_style), Paragraph("PRIMARY KEY, AUTO", table_cell_style), Paragraph("Unique simulation experiment ID", table_cell_style)],
        [Paragraph("SimulationLog", table_cell_bold), Paragraph("lighting_delta", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("DEFAULT 0.0", table_cell_style), Paragraph("Simulated lighting change (-100..+100)", table_cell_style)],
        [Paragraph("SimulationLog", table_cell_bold), Paragraph("patrol_delta", table_cell_style), Paragraph("INTEGER", table_cell_style), Paragraph("DEFAULT 0", table_cell_style), Paragraph("Simulated patrol fleet change", table_cell_style)],
        [Paragraph("SimulationLog", table_cell_bold), Paragraph("pred_crime_rate", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("ML projected crime rate", table_cell_style)],
        [Paragraph("SimulationLog", table_cell_bold), Paragraph("ci_lower, ci_upper", table_cell_style), Paragraph("FLOAT", table_cell_style), Paragraph("NOT NULL", table_cell_style), Paragraph("90% confidence interval bounds", table_cell_style)]
    ]
    t_audit = Table(t_audit_data, colWidths=[70, 80, 65, 115, 165])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_audit)
    story.append(Spacer(1, 6))

    # 3.6 CORE ALGORITHMIC FORMULATIONS
    story.append(Paragraph("3.6 Core Algorithmic Formulations (Pure Software Novelty)", sec_head_style))
    story.append(Paragraph(
        "<b>1. SafePath AI Graph Routing Formulation &amp; Optimality Proof:</b> For road graph G = (V, E) with segment metric distance d(e), "
        "the Dynamic Safety Index S(e) is computed as:<br/>"
        "&emsp;&emsp;<b>S(e) = 0.45 * C(e) + 0.35 * [1 - L(e)] - 0.20 * P(e) + T(t)</b><br/>"
        "where C(e) in [0, 1] is historical crime density, L(e) in [0, 1] is street illumination coverage, P(e) in [0, 1] is patrol frequency, "
        "and T(t) is the temporal nocturnal penalty (+0.25 added between 20:00 and 05:00 hours). Under worst-case bounds, S(e) ranges in [0.0, 1.25].<br/>"
        "The multi-objective edge traversal cost function is defined as:<br/>"
        "&emsp;&emsp;<b>Cost(e) = d(e) * [ 1 + lambda * S(e) ]</b> &emsp; (lambda in [0, 5])<br/>"
        "<i>Optimality Theorem:</i> Since metric distance d(e) &gt; 0, user sensitivity lambda &gt;= 0, and S(e) &gt;= 0 across all edges e in E, "
        "the effective cost satisfies Cost(e) &gt;= d(e) &gt; 0 for all e. Because edge costs are strictly positive, the sub-path optimality principle "
        "(Bellman's principle) holds unconditionally. Hence, min-heap Dijkstra execution over Cost(e) is guaranteed to converge to the globally optimal "
        "Pareto-efficient safe corridor without negative cycle anomalies in O((|V| + |E|) log |V|) runtime complexity.", body_style))
    story.append(Paragraph(
        "<b>2. Smart Patrol Fleet Optimizer &amp; Greedy Submodularity Proof:</b> Emergency response latency in municipal beat i with area A_i, "
        "road network density rho_i, and u_i allocated patrol vehicles is modeled by Larson's square-root law:<br/>"
        "&emsp;&emsp;<b>R_i(u_i) = R<sub>0,i</sub> / sqrt(u_i)</b><br/>"
        "where R<sub>0,i</sub> = k * sqrt(A_i) / (v * rho_i) is the single-unit baseline latency. The city-wide objective is to minimize total risk-weighted "
        "latency across all N beats subject to integer fleet constraints:<br/>"
        "&emsp;&emsp;<b>Minimize F(u) = Sum_{i=1 to N} w_i * [ R<sub>0,i</sub> / sqrt(u_i) ] &emsp; subject to Sum u_i &lt;= U_total, u_i &gt;= 1</b><br/>"
        "<i>Greedy Optimality Proof:</i> Let f_i(u_i) = w_i * R<sub>0,i</sub> * [1 - 1/sqrt(u_i)] represent the cumulative latency reduction in beat i. "
        "The marginal gain of adding the (k+1)-th unit is Delta_i(k) = w_i * R<sub>0,i</sub> * [ 1/sqrt(k) - 1/sqrt(k+1) ]. "
        "Taking the continuous second derivative of 1/sqrt(u) gives d^2/du^2 [u^(-1/2)] = (3/4) * u^(-5/2) &gt; 0, proving that R_i(u_i) is strictly "
        "convex and f_i(u_i) is strictly concave (submodular). By Nemhauser et al. (1978), the greedy priority-queue algorithm that iteratively assigns "
        "each incremental patrol unit to the beat with the maximum Delta_i(k) attains the exact global integer optimum. This guarantees that scarce "
        "police resources are distributed with maximum mathematical efficiency.", body_style))
    story.append(Paragraph(
        "<b>3. Explainable Machine Learning Formulation &amp; Bootstrap Confidence Bounds:</b> The predictive risk engine estimates jurisdictional "
        "crime incident rates y_hat using a Gradient Boosted Decision Tree ensemble G(x) = Sum_{m=1 to M} f_m(x), where each weak learner f_m "
        "fits the negative gradient pseudo-residuals of the squared error loss function L(y, F(x)) = (1/2) * [y - F(x)]^2. "
        "To quantify epistemic uncertainty and deliver actionable confidence intervals for municipal decision makers, CrimeLens 2.0 implements "
        "a residual bootstrap resampling procedure. For test feature vector x_0, the 90% confidence interval is computed as:<br/>"
        "&emsp;&emsp;<b>CI_{0.90}(x_0) = [ y_hat(x_0) - z_{0.05} * sigma_res , y_hat(x_0) + z_{0.05} * sigma_res ]</b><br/>"
        "where z_{0.05} = 1.645 is the critical standard normal quantile and sigma_res = sqrt( (1 / (N - p)) * Sum (y_i - y_hat_i)^2 ) is the "
        "unbiased residual standard error. This mathematical formulation allows city planners to simulate infrastructure interventions (e.g., street "
        "lighting upgrades) and ascertain with rigorous statistical certainty whether projected crime reductions are statistically significant.", body_style))

    flow_img_path = os.path.join(fig_dir, 'safepath_flowchart.png')
    if os.path.exists(flow_img_path):
        story.append(KeepTogether([
            Image(flow_img_path, width=content_width, height=content_width * 0.46),
            Paragraph("Figure 3.3: SafePath AI Multi-Criteria Optimization &amp; Corridor Decision Flowchart", caption_style)
        ]))

    story.append(PageBreak())
