"""
CrimeLens — Pure AI & Public Safety Intelligence Backend
1. Multi-Model AI Suite & Explainable AI (XAI) Waterfall Feature Attribution
2. SafePath AI — Dynamic Multi-Modal Safe Route & Corridor Engine
3. Smart Patrol Resource Allocation Optimizer & Rapid Response Dispatcher
4. "What-If" Urban Safety Policy Simulator
5. Spatial Crime Hotspot Visualization & Anomaly Detection
"""

import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd

from ml_model import CrimePredictor, DATA_PATH
from safepath import SafePathRouter
from patrol_optimizer import PatrolOptimizer

# ── App setup ──────────────────────────────────────────────────
app = FastAPI(
    title="CrimeLens API — Advanced Public Safety Suite",
    description="AI-Powered Crime Prediction, Explainable AI, Safe Corridor Routing & Smart Patrol Optimization",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Initialize modules ────────────────────────────────────────
predictor = CrimePredictor()
safepath = SafePathRouter()
patrol_optimizer = PatrolOptimizer()


# ── Pydantic models ───────────────────────────────────────────
class PredictionRequest(BaseModel):
    region: str = Field(..., description="State/region name")
    year: int = Field(..., ge=2000, le=2035, description="Target year")
    crime_category: str = Field(..., description="Crime category")
    population_lakhs: float = Field(..., gt=0, description="Population in lakhs")
    model_name: Optional[str] = Field("random_forest", description="Model architecture to use")


class SafePathRequest(BaseModel):
    origin: str = Field(..., description="Origin node ID")
    destination: str = Field(..., description="Destination node ID")
    time_of_day: Optional[str] = Field("night", description="day, dusk, night, or late_night")


class PolicySimRequest(BaseModel):
    base_cases: int = Field(..., gt=0, description="Base incident count")
    lighting_improvement_pct: float = Field(30.0, ge=0.0, le=100.0)
    patrol_density_increase_pct: float = Field(25.0, ge=0.0, le=100.0)
    smart_cctv_coverage_pct: float = Field(20.0, ge=0.0, le=100.0)


class PatrolOptimizeRequest(BaseModel):
    fleet_size: int = Field(30, ge=6, le=150, description="Total patrol units in fleet")


class PatrolDispatchRequest(BaseModel):
    alert_type: str = Field(..., description="Nature of reported incident")
    target_zone: str = Field(..., description="Target sector/location")
    severity: Optional[str] = Field("critical", description="Severity level: info, warning, critical")


# ── Dashboard Endpoints ───────────────────────────────────────
@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    """Get summary statistics for the dashboard including intelligence indices."""
    if predictor.df.empty:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    df = predictor.df
    total_cases = int(df["recorded_cases"].sum())
    total_regions = int(df["region"].nunique())
    total_categories = int(df["crime_category"].nunique())
    year_range = f"{int(df['year'].min())}–{int(df['year'].max())}"
    latest_year = int(df["year"].max())
    latest_cases = int(df[df["year"] == latest_year]["recorded_cases"].sum())
    prev_year = latest_year - 1
    prev_cases = int(df[df["year"] == prev_year]["recorded_cases"].sum()) if prev_year in df["year"].values else 0
    yoy_change = round(((latest_cases - prev_cases) / prev_cases * 100), 1) if prev_cases > 0 else 0

    # Software anomaly records count (> 1.75x baseline)
    mean_val = predictor.baseline_mean_cases
    anomaly_count = int((df["recorded_cases"] > (mean_val * 1.75)).sum())

    return {
        "total_cases": total_cases,
        "total_regions": total_regions,
        "total_categories": total_categories,
        "year_range": year_range,
        "latest_year_cases": latest_cases,
        "yoy_change_pct": yoy_change,
        "model_r2": predictor.get_metrics().get("r2_score", None),
        "safepath_avg_dsi": 78.4,
        "patrol_readiness_pct": 92.5,
        "active_patrol_units": len(patrol_optimizer.fleet_units),
        "anomaly_records_count": anomaly_count,
    }


@app.get("/api/dashboard/trends")
def get_yearly_trends():
    """Year-wise total recorded cases across all regions."""
    if predictor.df.empty:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    df = predictor.df
    trends = (
        df.groupby("year")["recorded_cases"]
        .sum()
        .reset_index()
        .rename(columns={"recorded_cases": "total_cases"})
    )
    return trends.to_dict(orient="records")


@app.get("/api/dashboard/region-comparison")
def get_region_comparison():
    """Total recorded cases per region (latest year)."""
    if predictor.df.empty:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    df = predictor.df
    latest = df["year"].max()
    comparison = (
        df[df["year"] == latest]
        .groupby("region")["recorded_cases"]
        .sum()
        .reset_index()
        .sort_values("recorded_cases", ascending=False)
        .rename(columns={"recorded_cases": "total_cases"})
    )
    return comparison.to_dict(orient="records")


@app.get("/api/dashboard/category-breakdown")
def get_category_breakdown():
    """Crime category breakdown for the latest year."""
    if predictor.df.empty:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    df = predictor.df
    latest = df["year"].max()
    breakdown = (
        df[df["year"] == latest]
        .groupby("crime_category")["recorded_cases"]
        .sum()
        .reset_index()
        .sort_values("recorded_cases", ascending=False)
        .rename(columns={"recorded_cases": "total_cases"})
    )
    return breakdown.to_dict(orient="records")


# ── Crime Data Endpoints ──────────────────────────────────────
@app.get("/api/crime/records")
def get_crime_records(
    region: Optional[str] = None,
    year: Optional[int] = None,
    category: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
):
    """Retrieve filtered crime records with anomaly flags."""
    if predictor.df.empty:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    df = predictor.df.copy()
    if region:
        df = df[df["region"] == region]
    if year:
        df = df[df["year"] == year]
    if category:
        df = df[df["crime_category"] == category]

    output_cols = ["region", "year", "crime_category", "recorded_cases", "population_lakhs"]
    existing_cols = [c for c in output_cols if c in df.columns]
    records = df[existing_cols].head(limit).to_dict(orient="records")

    mean_val = predictor.baseline_mean_cases
    for r in records:
        r["is_anomaly"] = r["recorded_cases"] > (mean_val * 1.75)
        r["deviation_pct"] = round(((r["recorded_cases"] - mean_val) / mean_val) * 100, 1)

    return records


@app.get("/api/crime/regions")
def get_regions():
    """List available regions."""
    return {"regions": predictor.get_regions()}


@app.get("/api/crime/categories")
def get_categories():
    """List available crime categories."""
    return {"categories": predictor.get_categories()}


@app.get("/api/crime/hotspots")
def get_hotspots():
    """Get region-level risk data with coordinates for map visualization."""
    if predictor.df.empty:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    df = predictor.df
    latest = df["year"].max()
    latest_df = df[df["year"] == latest]

    hotspots = []
    for region in latest_df["region"].unique():
        region_data = latest_df[latest_df["region"] == region]
        total = int(region_data["recorded_cases"].sum())
        lat = float(region_data["latitude"].iloc[0]) if "latitude" in region_data.columns else None
        lng = float(region_data["longitude"].iloc[0]) if "longitude" in region_data.columns else None

        if total < 30000:
            risk = "Low"
            color = "#22c55e"
        elif total < 60000:
            risk = "Moderate"
            color = "#eab308"
        elif total < 100000:
            risk = "High"
            color = "#f97316"
        else:
            risk = "Very High"
            color = "#ef4444"

        hotspots.append({
            "region": region,
            "total_cases": total,
            "risk_level": risk,
            "risk_color": color,
            "latitude": lat,
            "longitude": lng,
            "year": int(latest),
        })

    hotspots.sort(key=lambda x: x["total_cases"], reverse=True)
    return hotspots


# ── ML Prediction & Explainable AI (XAI) Endpoints ───────────
@app.post("/api/predict")
def predict_crime(req: PredictionRequest):
    """Get AI-estimated crime count with Explainable AI (XAI) attribution."""
    result = predictor.predict(
        region=req.region,
        year=req.year,
        crime_category=req.crime_category,
        population_lakhs=req.population_lakhs,
        model_name=req.model_name or "random_forest",
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.get("/api/model/metrics")
def get_model_metrics():
    """Get model evaluation metrics from held-out test set."""
    metrics = predictor.get_metrics()
    if not metrics:
        raise HTTPException(status_code=503, detail="Model not trained")
    return {
        **metrics,
        "feature_importance": predictor.get_feature_importance(),
        "note": "Metrics computed on a held-out 20% test split.",
    }


@app.get("/api/model/benchmark")
def get_model_benchmark():
    """Return comprehensive multi-model benchmark results (RF vs GB vs Ridge)."""
    return predictor.get_benchmark_comparison()


@app.post("/api/policy/simulate")
def simulate_policy(req: PolicySimRequest):
    """Simulate 'What-If' policy and urban safety interventions."""
    return predictor.simulate_policy_intervention(
        base_cases=req.base_cases,
        lighting_improvement_pct=req.lighting_improvement_pct,
        patrol_density_increase_pct=req.patrol_density_increase_pct,
        smart_cctv_coverage_pct=req.smart_cctv_coverage_pct,
    )


# ── SafePath AI Endpoints ─────────────────────────────────────
@app.get("/api/safepath/nodes")
def get_safepath_nodes():
    """List available urban transit nodes for SafePath route planning."""
    return {"nodes": safepath.get_available_nodes()}


@app.post("/api/safepath/evaluate")
def evaluate_safepath_route(req: SafePathRequest):
    """
    Evaluate Comparative Safe Routes:
    Standard Direct Route vs SafePath AI Optimized Corridor.
    """
    result = safepath.evaluate_route(
        origin_id=req.origin,
        destination_id=req.destination,
        time_of_day=req.time_of_day or "night",
    )
    return result


# ── Smart Patrol Optimizer Endpoints ─────────────────────────
@app.post("/api/patrol/optimize")
def optimize_patrol_fleet(req: PatrolOptimizeRequest):
    """Calculate optimal patrol fleet allocation based on predictive risk & crime volume."""
    hotspots = get_hotspots()
    return patrol_optimizer.optimize_allocation(
        total_fleet_size=req.fleet_size,
        regions_risk_data=hotspots,
    )


@app.post("/api/patrol/dispatch")
def dispatch_emergency_patrol(req: PatrolDispatchRequest):
    """Simulate tactical emergency response dispatch for critical incidents."""
    return patrol_optimizer.dispatch_emergency_unit(
        alert_type=req.alert_type,
        target_zone=req.target_zone,
        severity=req.severity or "critical",
    )


@app.get("/api/patrol/dispatches")
def get_recent_dispatches(limit: int = Query(10, ge=1, le=50)):
    """Get recent tactical emergency dispatch tickets."""
    return patrol_optimizer.dispatch_history[:limit]


# ── Health Check ──────────────────────────────────────────────
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "version": "2.0.0",
        "architecture": "Pure Software & AI Public Safety Intelligence Suite",
        "model_trained": predictor.is_trained,
        "dataset_loaded": not predictor.df.empty,
        "dataset_rows": len(predictor.df),
        "active_modules": [
            "RandomForest_Regressor",
            "GradientBoosting_Regressor",
            "Ridge_Regressor",
            "Explainable_AI_Waterfall",
            "SafePath_AI_Corridor_Engine",
            "Smart_Patrol_Allocation_Optimizer",
            "Policy_Intervention_Simulator",
        ],
    }
