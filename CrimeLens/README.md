# CrimeLens 2.0 — AI-Powered Public Safety Suite & Safe Corridor Intelligence

> **College Mini Project** | React 19 + TypeScript + FastAPI + Multi-Model Machine Learning + Explainable AI (XAI) + SafePath Engine

CrimeLens 2.0 is a 100% pure software, data-driven public safety analytics and predictive criminology system. It is designed to be completely hardware-independent, requiring no physical microcontrollers, sensors, or external paid APIs.

---

## 📋 Table of Contents

- [Novel Software Features](#-novel-software-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [Dataset Details](#-dataset-details)
- [Mathematical & Algorithmic Formulations](#-mathematical--algorithmic-formulations)
- [Limitations & Future Scope](#-limitations--future-scope)

---

## ✨ Novel Software Features

### 1. 🧭 SafePath AI — Dynamic Route & Safe Corridor Engine
- Unlike traditional navigation apps that optimize solely for travel time, SafePath solves the **Risk-Aware Routing Problem**.
- Evaluates two routes between origin and destination:
  1. **Standard / Direct Shortest Route**: Minimal travel distance, but potentially traverses poorly-lit or historically vulnerable areas.
  2. **AI-Optimized Safe Corridor Route**: Algorithmic corridor routing prioritizing well-lit arterial streets, high CCTV density, and active police kiosks.
- Calculates a **Dynamic Safety Index (DSI)** (0–100 score) along waypoints:
  $$\text{DSI} = 100 - \Big(\alpha \cdot \text{BaseRisk} \cdot \text{TimePenalty} - \beta \cdot \text{Illumination} - \gamma \cdot \text{CCTV} - \delta \cdot \text{PolicePresence}\Big)$$
- Visualizes both polylines on an interactive Leaflet map with waypoint hazard flags and safety differential gains (e.g. `+38.5% Safer`).

### 2. 🧠 Multi-Model AI Suite & Explainable AI (XAI)
- **Multi-Model Dynamic Benchmark**:
  - Compares **Random Forest Regressor** (Ensemble Bagging), **Gradient Boosting Regressor** (Sequential Boosting, top R²=0.9896), and **Ridge Regularized Regression** (L2 Linear Baseline).
  - Evaluates $R^2$, MAE, RMSE, and sub-millisecond inference latency side-by-side with 1-click model switching.
- **Explainable AI (Waterfall Feature Attribution)**:
  - Decomposes every prediction into local force contributions: Global Baseline $\to$ Regional Shift $\to$ Category Vulnerability $\to$ Population Scaling $\to$ Temporal Year Trend.
- **90% Confidence Prediction Intervals**:
  - Reports statistical uncertainty bounds $[y_{\min}, y_{\max}]$ using test residual variance.

### 3. 🚓 Smart Patrol Resource Allocation Optimizer
- Solves the constrained fleet allocation problem for police departments and campus security.
- Inputs total fleet size (10–100 units) and distributes cruisers, drones, and rapid motorcycle interceptors across jurisdictions.
- Minimizes expected emergency response time ($R(u) = \frac{R_0}{\sqrt{u}}$) and computes non-linear crime deterrence gains.
- Provides shift breakdown (Morning, Evening, Night) and a **1-click Emergency Tactical Dispatch Simulator** with live ticket tracking.

### 4. 🎛 "What-If" Policy Intervention Simulator
- Allows civic administrators and researchers to simulate public safety interventions:
  - Municipal street lighting upgrades ($0–100\%$)
  - Patrol density increase ($0–100\%$)
  - Smart CCTV coverage ($0–100\%$)
- Models non-linear compound mitigation and computes estimated averted crime incidents and safety score improvement points.

### 5. 🗺 Spatial Hotspots & Statistical Anomaly Detection
- Interactive Leaflet geographic hotspot map sized by crime volume and color-coded by risk category.
- Automated anomaly detection flagging statistical outliers (> 1.75x mean baseline) across categories and years.

---

## 🛠 Tech Stack

| Layer         | Technology                                                            |
| ------------- | --------------------------------------------------------------------- |
| **Frontend**  | React 19 + TypeScript + Vite                                          |
| **Styling**   | Custom CSS Design System (dark theme)                                 |
| **Charts**    | Recharts                                                              |
| **Maps**      | React Leaflet + OpenStreetMap                                         |
| **Icons**     | Lucide React                                                          |
| **Backend**   | Python 3.10+ + FastAPI + Pydantic v2                                  |
| **ML Engine** | scikit-learn (Gradient Boosting, Random Forest, Ridge) + NumPy/Pandas |
| **Algorithms**| Dijkstra Risk-Weighted SafePath Router, Non-linear Patrol Optimizer    |

---

## 📁 Project Structure

```
CrimeLens/
├── backend/
│   ├── main.py              # FastAPI server with pure software AI endpoints
│   ├── ml_model.py          # Multi-model suite (RF, GB, Ridge) & XAI explainer
│   ├── safepath.py          # SafePath AI route & corridor evaluation engine
│   ├── patrol_optimizer.py  # Smart patrol resource allocation & dispatch hub
│   ├── requirements.txt     # Python dependencies
│   └── data/
│       └── crime_data.csv   # Historical crime dataset (NCRB schema)
│
├── frontend/
│   ├── index.html           # HTML entry point
│   ├── package.json         # Dependencies & scripts
│   ├── vite.config.ts       # Vite configuration
│   ├── tsconfig.json        # TypeScript configuration
│   └── src/
│       ├── main.tsx          # React entry point
│       ├── App.tsx           # Router with pure software navigation
│       ├── index.css         # Complete dark-theme design system
│       ├── services/
│       │   └── api.ts        # Fully typed API client for all backend endpoints
│       └── pages/
│           ├── Dashboard.tsx       # Command center with intelligence metrics
│           ├── SafePath.tsx        # Safe corridor interactive map & evaluator
│           ├── PatrolOptimizer.tsx # AI patrol distribution & dispatch hub
│           ├── Prediction.tsx      # Multi-model suite, XAI & policy simulator
│           ├── Hotspots.tsx        # Geographic hotspot visualization
│           └── Analytics.tsx       # Multi-dimensional crime data analytics
│
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python** 3.10+
- **Node.js** 18+
- **npm**

### Step 1: Navigate to Project
```bash
cd "mini project ABES/CrimeLens"
```

### Step 2: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

---

## ▶ Running the Application

### Terminal 1 — Start FastAPI Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Interactive Swagger API Documentation: `http://localhost:8000/docs`

### Terminal 2 — Start React Vite Frontend
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 📡 API Endpoints Summary

| Method | Endpoint                  | Description                                            |
| ------ | ------------------------- | ------------------------------------------------------ |
| POST   | `/api/safepath/evaluate`  | Evaluates Direct Route vs AI Safe Corridor with DSI    |
| GET    | `/api/safepath/nodes`     | Available urban transit nodes with safety attributes   |
| POST   | `/api/patrol/optimize`    | Solves patrol fleet allocation matrix across sectors   |
| POST   | `/api/patrol/dispatch`    | Authorizes rapid response tactical dispatch ticket     |
| GET    | `/api/patrol/dispatches`  | Retrieves recent tactical patrol dispatches            |
| GET    | `/api/model/benchmark`    | Side-by-side benchmark (Random Forest, GB, Ridge)      |
| POST   | `/api/predict`            | ML prediction with XAI waterfall feature attribution   |
| GET    | `/api/model/metrics`      | Held-out evaluation metrics (R², MAE, RMSE)            |
| POST   | `/api/policy/simulate`    | "What-If" municipal safety intervention simulation     |
| GET    | `/api/dashboard/stats`    | Summary statistics with intelligence indices           |
| GET    | `/api/dashboard/trends`   | Yearly total crime trends                              |
| GET    | `/api/dashboard/region-comparison` | Region comparison for latest year             |
| GET    | `/api/dashboard/category-breakdown`| Category breakdown for latest year            |
| GET    | `/api/crime/records`      | Filtered crime records with statistical anomaly flags  |
| GET    | `/api/crime/hotspots`     | Region risk data with coordinates                      |
| GET    | `/api/health`             | System health check & active modules roster            |

---

## 👥 Team & College Details

> **College**: ABES Engineering College  
> **Project**: College Mini Project — Public Safety & Intelligent Systems  

---

*CrimeLens 2.0 — Engineered with React 19, FastAPI, scikit-learn, and Leaflet*
