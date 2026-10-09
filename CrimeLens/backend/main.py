"""
CrimeLens — FastAPI Backend
Provides REST API endpoints for crime analytics, ML predictions,
and IoT safety simulation.
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd

from ml_model import CrimePredictor, DATA_PATH
from iot_simulator import IoTSimulator

# ── App setup ──────────────────────────────────────────────────
app = FastAPI(
    title="CrimeLens API",
    description="AI-Powered Crime Prediction and IoT Safety Monitoring",
    version="1.0.0",
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
iot = IoTSimulator()


# ── Pydantic models ───────────────────────────────────────────
class PredictionRequest(BaseModel):
    region: str = Field(..., description="State/region name")
    year: int = Field(..., ge=2000, le=2035, description="Target year")
    crime_category: str = Field(..., description="Crime category")
    population_lakhs: float = Field(..., gt=0, description="Population in lakhs")


class SensorUpdateRequest(BaseModel):
    pir_motion: Optional[bool] = None
    light_intensity: Optional[int] = Field(None, ge=0, le=100)
    sound_level: Optional[int] = Field(None, ge=0, le=100)
    sos_active: Optional[bool] = None


# ── Dashboard Endpoints ───────────────────────────────────────
@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    """Get summary statistics for the dashboard."""
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

    return {
        "total_cases": total_cases,
        "total_regions": total_regions,
        "total_categories": total_categories,
        "year_range": year_range,
        "latest_year_cases": latest_cases,
        "yoy_change_pct": yoy_change,
        "active_alerts": len(iot.get_alerts(limit=10)),
        "model_r2": predictor.get_metrics().get("r2_score", None),
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
    """Retrieve filtered crime records."""
    if predictor.df.empty:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    df = predictor.df.copy()
    if region:
        df = df[df["region"] == region]
    if year:
        df = df[df["year"] == year]
    if category:
        df = df[df["crime_category"] == category]

    # Drop encoded columns for clean output
    output_cols = ["region", "year", "crime_category", "recorded_cases", "population_lakhs"]
    existing_cols = [c for c in output_cols if c in df.columns]
    return df[existing_cols].head(limit).to_dict(orient="records")


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
        elif total < 60000:
            risk = "Moderate"
        elif total < 100000:
            risk = "High"
        else:
            risk = "Very High"

        hotspots.append({
            "region": region,
            "total_cases": total,
            "risk_level": risk,
            "latitude": lat,
            "longitude": lng,
            "year": int(latest),
        })

    hotspots.sort(key=lambda x: x["total_cases"], reverse=True)
    return hotspots


# ── ML Prediction Endpoints ──────────────────────────────────
@app.post("/api/predict")
def predict_crime(req: PredictionRequest):
    """Get AI-estimated crime case count for given parameters."""
    result = predictor.predict(
        region=req.region,
        year=req.year,
        crime_category=req.crime_category,
        population_lakhs=req.population_lakhs,
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
        "note": "Metrics computed on a held-out 20% test split of sample data.",
    }


# ── IoT Simulator Endpoints ──────────────────────────────────
@app.get("/api/iot/sensors")
def get_sensor_readings():
    """Get current simulated sensor readings."""
    return iot.get_sensor_readings()


@app.post("/api/iot/sensors")
def update_sensors(req: SensorUpdateRequest):
    """Update simulated sensor values and trigger alerts if thresholds met."""
    result = iot.update_sensor(
        pir_motion=req.pir_motion,
        light_intensity=req.light_intensity,
        sound_level=req.sound_level,
        sos_active=req.sos_active,
    )
    return result


@app.get("/api/iot/alerts")
def get_alerts(limit: int = Query(50, ge=1, le=200)):
    """Get recent simulated alerts."""
    return iot.get_alerts(limit=limit)


@app.post("/api/iot/random-event")
def generate_random_event():
    """Generate a random simulated sensor event for demonstration."""
    return iot.generate_random_event()


# ── Health Check ──────────────────────────────────────────────
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "model_trained": predictor.is_trained,
        "dataset_loaded": not predictor.df.empty,
        "dataset_rows": len(predictor.df),
    }
