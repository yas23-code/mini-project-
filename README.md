# CrimeLens 2.0 — AI-Powered Public Safety Suite & Safe Corridor Intelligence

CrimeLens 2.0 is a 100% pure software, hardware-independent public safety intelligence suite engineered for pedestrian safe corridor routing, municipal patrol fleet allocation, and explainable crime risk forecasting.

### Quick Start
1. **Backend (FastAPI)**:
   ```bash
   cd CrimeLens/backend
   python -m uvicorn main:app --reload --port 8000
   ```
2. **Frontend (React + Vite + Leaflet)**:
   ```bash
   cd CrimeLens/frontend
   npm install
   npm run dev
   ```

### 100% Pure Software & AI Architecture:
1. **SafePath AI Corridor Engine**: Multi-criteria risk-penalized Dijkstra pathfinding balancing transit distance with Dynamic Safety Index (DSI).
2. **Multi-Model Machine Learning Suite**: Gradient Boosting ($R^2 = 0.9896$), Random Forest ($R^2 = 0.9777$), and Ridge Regularized Regression benchmarked on identical held-out test splits.
3. **Explainable AI (XAI)**: Local waterfall feature attribution and 90% bootstrap confidence prediction intervals for What-If municipal policy simulations.
4. **Smart Patrol Resource Allocation Optimizer**: Non-linear fleet distribution minimizing emergency response latency using Larson's square root model ($R(u) = R_0 / \sqrt{u}$).
5. **Interactive Geospatial Cartography**: Leaflet mapping with real-time route overlays, crime cluster heat bubbles, and municipal beat monitoring.

### Academic Project Report
- **Complete Academic Report (36 Pages):** [`CrimeLens_BTech_Project_Report.pdf`](CrimeLens_BTech_Project_Report.pdf)
- **Markdown Specification:** [`CrimeLens_BTech_Project_Report.md`](CrimeLens_BTech_Project_Report.md)
