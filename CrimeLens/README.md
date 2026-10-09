# CrimeLens — AI-Powered Crime Prediction & IoT Safety Monitoring System

> **College Mini Project** | React + FastAPI + Machine Learning + IoT Simulation

CrimeLens is a full-stack web application that analyzes historical crime data, estimates crime risk using machine learning (Random Forest), visualizes crime patterns on interactive charts and maps, and simulates real-time IoT safety monitoring — all without requiring physical hardware or paid services.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [API Endpoints](#-api-endpoints)
- [Dataset Details](#-dataset-details)
- [How It Works](#-how-it-works)
- [Screenshots](#-screenshots)
- [Limitations](#-limitations)
- [Future Scope](#-future-scope)

---

## ✨ Features

### 1. Dashboard
- Total recorded cases, region count, and YoY change statistics
- Year-wise crime trend line chart
- Crime category pie chart breakdown
- Region comparison horizontal bar chart
- Recent IoT alerts panel
- ML model R² score indicator

### 2. Crime Analytics
- Filter records by region and crime category
- Multi-line trend chart (category-wise over years)
- Category comparison bar chart
- Region-wise statistics
- Raw data table with search

### 3. AI Crime Prediction
- Random Forest regression model trained on historical data
- User selects: Region, Year, Crime Category, Population
- Returns estimated case count + explainable risk category (Low/Moderate/High/Very High)
- Model evaluation metrics: R² score, MAE, train/test sample counts
- Feature importance visualization

### 4. Crime Hotspot Visualization
- Interactive Leaflet map with circle markers sized by crime volume
- Circle markers color-coded by risk level
- Ranked regional cards with progress bars
- Verified approximate state-capital coordinates

### 5. IoT Safety Simulator
- PIR motion detection toggle
- Ambient light intensity slider (0–100)
- Sound level slider (0–100 dB)
- Manual SOS emergency button
- Real-time simulated sensor readings
- Automatic alert generation based on configurable rules
- Alert history timeline with severity and timestamps
- Random event generator for demo purposes
- **All values are software-simulated — no physical hardware required**

---

## 🛠 Tech Stack

| Layer         | Technology                                    |
| ------------- | --------------------------------------------- |
| **Frontend**  | React 19 + TypeScript + Vite                  |
| **Styling**   | Custom CSS Design System (dark theme)         |
| **Charts**    | Recharts                                      |
| **Maps**      | React Leaflet + OpenStreetMap                 |
| **Icons**     | Lucide React                                  |
| **Backend**   | Python 3.10+ + FastAPI                        |
| **ML**        | scikit-learn (Random Forest) + Pandas + NumPy |
| **Dataset**   | CSV file (sample data modeled after NCRB)     |

---

## 📁 Project Structure

```
CrimeLens/
├── backend/
│   ├── main.py              # FastAPI server with all endpoints
│   ├── ml_model.py          # Random Forest model training & prediction
│   ├── iot_simulator.py     # Software-simulated IoT sensors & alerts
│   ├── requirements.txt     # Python dependencies
│   └── data/
│       └── crime_data.csv   # Sample crime dataset
│
├── frontend/
│   ├── index.html           # HTML entry point
│   ├── package.json         # Node dependencies & scripts
│   ├── vite.config.ts       # Vite build configuration
│   ├── tsconfig.json        # TypeScript configuration
│   └── src/
│       ├── main.tsx          # React entry point
│       ├── App.tsx           # Root component with routing
│       ├── index.css         # Complete dark-theme design system
│       ├── services/
│       │   └── api.ts        # API client for all backend endpoints
│       └── pages/
│           ├── Dashboard.tsx   # Overview dashboard
│           ├── Analytics.tsx   # Crime data analytics
│           ├── Prediction.tsx  # ML prediction interface
│           ├── Hotspots.tsx    # Map & ranked visualization
│           └── IoTMonitor.tsx  # IoT safety simulator
│
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **npm** (comes with Node.js)
- **pip** (comes with Python)

### Step 1: Clone / Download the Project
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

### Terminal 1 — Start the Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
You should see:
```
[ML] Model trained. R²=0.99xx, MAE=xxxx
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 — Start the Frontend
```bash
cd frontend
npm run dev
```
Open the URL shown (usually `http://localhost:5173`) in your browser.

### Quick Verify
- Backend health check: http://localhost:8000/api/health
- Backend API docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

---

## 📡 API Endpoints

### Dashboard
| Method | Endpoint                          | Description                       |
| ------ | --------------------------------- | --------------------------------- |
| GET    | `/api/dashboard/stats`            | Summary statistics                |
| GET    | `/api/dashboard/trends`           | Year-wise total crime trends      |
| GET    | `/api/dashboard/region-comparison` | Region comparison (latest year)  |
| GET    | `/api/dashboard/category-breakdown`| Category breakdown (latest year) |

### Crime Data
| Method | Endpoint               | Description                        |
| ------ | ---------------------- | ---------------------------------- |
| GET    | `/api/crime/records`   | Filtered crime records             |
| GET    | `/api/crime/regions`   | List of available regions          |
| GET    | `/api/crime/categories`| List of crime categories           |
| GET    | `/api/crime/hotspots`  | Region risk data with coordinates  |

### ML Prediction
| Method | Endpoint             | Description                       |
| ------ | -------------------- | --------------------------------- |
| POST   | `/api/predict`       | Get AI prediction for parameters  |
| GET    | `/api/model/metrics` | Model evaluation metrics          |

### IoT Simulator
| Method | Endpoint                | Description                      |
| ------ | ----------------------- | -------------------------------- |
| GET    | `/api/iot/sensors`      | Current sensor readings          |
| POST   | `/api/iot/sensors`      | Update sensor values             |
| GET    | `/api/iot/alerts`       | Alert history                    |
| POST   | `/api/iot/random-event` | Generate random demo event       |

### System
| Method | Endpoint        | Description        |
| ------ | --------------- | ------------------ |
| GET    | `/api/health`   | Health check       |

---

## 📊 Dataset Details

### Sample Dataset (Included)
The file `backend/data/crime_data.csv` contains **sample/synthetic data** created for demonstration purposes:

- **8 Indian states**: Delhi, Maharashtra, Karnataka, Tamil Nadu, Uttar Pradesh, Rajasthan, West Bengal, Kerala
- **5 crime categories**: Theft, Assault, Burglary, Cybercrime, Fraud
- **6 years**: 2018–2023
- **240 records** total
- Fields: region, year, crime_category, recorded_cases, population_lakhs, latitude, longitude

> ⚠ **This is sample data for demonstration only.** It is NOT official crime statistics and should not be presented as such.

### Using Real NCRB Data
To use verified data from the National Crime Records Bureau (NCRB):

1. Visit https://ncrb.gov.in/crime-in-india.html
2. Download the relevant "Crime in India" annual reports
3. Format the data into a CSV with these columns:
   ```
   region,year,crime_category,recorded_cases,population_lakhs,latitude,longitude
   ```
4. Replace `backend/data/crime_data.csv` with your formatted file
5. Restart the backend — the model will retrain automatically

---

## 🔧 How It Works

### Machine Learning Pipeline
1. Load CSV data with Pandas
2. Encode categorical features (region, crime_category) using LabelEncoder
3. Feature vector: `[region_encoded, year, category_encoded, population_lakhs]`
4. Split into 80% train / 20% test
5. Train Random Forest Regressor (100 trees, max_depth=12)
6. Evaluate on held-out test set (R² score, MAE)
7. For prediction: encode inputs → predict → classify into risk category

### Risk Categories
| Estimated Cases | Risk Level  |
| --------------- | ----------- |
| < 5,000         | Low         |
| 5,000–14,999    | Moderate    |
| 15,000–39,999   | High        |
| ≥ 40,000        | Very High   |

### IoT Simulation Rules
| Condition             | Alert Type      | Severity |
| --------------------- | --------------- | -------- |
| PIR motion = true     | motion_detected | warning  |
| Light < 20%           | low_light       | info     |
| Sound > 75 dB         | loud_sound      | warning  |
| SOS button active     | sos_triggered   | critical |

---

## ⚠ Limitations

1. **Sample data only**: The included dataset is synthetic. Model accuracy reflects patterns in sample data, not real-world conditions.
2. **Simple feature set**: The model uses only 4 features. Real crime prediction would require socioeconomic, demographic, temporal, and environmental factors.
3. **No user authentication**: This prototype has no login/registration system.
4. **In-memory storage**: Alerts and sensor data are stored in memory and reset when the backend restarts.
5. **No real hardware**: All IoT readings are software-simulated.
6. **Limited geographic data**: Coordinates are approximate state capitals, not precise crime locations.

---

## 🔮 Future Scope

### Hardware Integration
- **ESP32 microcontroller** with physical sensors:
  - PIR motion sensor (HC-SR501) for intrusion detection
  - Light sensor (LDR/BH1750) for ambient light measurement
  - Sound sensor (KY-038) for noise detection
  - GPS module (NEO-6M) for location tracking
  - Physical SOS button with buzzer and LED
- MQTT/WebSocket for real-time sensor data streaming
- Battery-powered portable safety device

### Software Enhancements
- Real NCRB dataset integration
- User authentication and role-based access
- PostgreSQL/MongoDB database for persistent storage
- Time-series forecasting (LSTM/Prophet)
- Geospatial clustering (DBSCAN) for precise hotspot detection
- Push notifications and SMS alerts
- Mobile-responsive PWA
- Multi-language support (Hindi, regional languages)
- Community safety reporting system

---

## 👥 Team

> Add your team member names, roll numbers, and college details here.

---

## 📄 License

This project is created for educational purposes as a college mini project.

---

*Built with ❤ using React, FastAPI, and scikit-learn*
