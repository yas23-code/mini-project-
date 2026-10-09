"""
CrimeLens — ML Model Module
Trains a Random Forest model on historical crime data for case count prediction.
All predictions are estimates based on sample data; not official forecasts.
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "crime_data.csv")


class CrimePredictor:
    """Random Forest model for estimating recorded crime case counts."""

    def __init__(self):
        self.model = None
        self.region_encoder = LabelEncoder()
        self.category_encoder = LabelEncoder()
        self.df: pd.DataFrame = pd.DataFrame()
        self.metrics: dict = {}
        self.is_trained = False
        self._load_and_train()

    def _load_and_train(self):
        """Load CSV data, encode features, and train the model."""
        if not os.path.exists(DATA_PATH):
            print(f"[WARNING] Dataset not found at {DATA_PATH}")
            return

        self.df = pd.read_csv(DATA_PATH)
        # Drop rows with missing target
        self.df.dropna(subset=["recorded_cases"], inplace=True)
        # Fill missing population with median
        if "population_lakhs" in self.df.columns:
            self.df["population_lakhs"] = self.df["population_lakhs"].fillna(
                self.df["population_lakhs"].median()
            )

        # Encode categorical features
        self.df["region_encoded"] = self.region_encoder.fit_transform(
            self.df["region"]
        )
        self.df["category_encoded"] = self.category_encoder.fit_transform(
            self.df["crime_category"]
        )

        feature_cols = ["region_encoded", "year", "category_encoded", "population_lakhs"]
        X = self.df[feature_cols]
        y = self.df["recorded_cases"]

        # Train/test split for evaluation
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model = RandomForestRegressor(
            n_estimators=100, max_depth=12, random_state=42, n_jobs=-1
        )
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        self.metrics = {
            "mae": round(float(mean_absolute_error(y_test, y_pred)), 2),
            "r2_score": round(float(r2_score(y_test, y_pred)), 4),
            "test_samples": int(len(X_test)),
            "train_samples": int(len(X_train)),
        }
        self.is_trained = True
        print(f"[ML] Model trained. R²={self.metrics['r2_score']}, MAE={self.metrics['mae']}")

    def predict(self, region: str, year: int, crime_category: str, population_lakhs: float) -> dict:
        """Predict estimated recorded cases for given inputs."""
        if not self.is_trained:
            return {"error": "Model not trained. Check that the dataset exists."}

        # Validate inputs
        known_regions = list(self.region_encoder.classes_)
        known_categories = list(self.category_encoder.classes_)

        if region not in known_regions:
            return {"error": f"Unknown region '{region}'. Known: {known_regions}"}
        if crime_category not in known_categories:
            return {"error": f"Unknown category '{crime_category}'. Known: {known_categories}"}

        region_enc = self.region_encoder.transform([region])[0]
        category_enc = self.category_encoder.transform([crime_category])[0]

        X_input = pd.DataFrame(
            [[region_enc, year, category_enc, population_lakhs]],
            columns=["region_encoded", "year", "category_encoded", "population_lakhs"],
        )
        predicted_cases = max(0, float(self.model.predict(X_input)[0]))

        # Risk category based on predicted case count
        if predicted_cases < 5000:
            risk = "Low"
        elif predicted_cases < 15000:
            risk = "Moderate"
        elif predicted_cases < 40000:
            risk = "High"
        else:
            risk = "Very High"

        return {
            "region": region,
            "year": year,
            "crime_category": crime_category,
            "population_lakhs": population_lakhs,
            "estimated_cases": round(predicted_cases),
            "risk_category": risk,
            "note": "This is an estimate from a sample-data-trained model, not an official prediction.",
        }

    def get_regions(self) -> list:
        return sorted(list(self.region_encoder.classes_)) if self.is_trained else []

    def get_categories(self) -> list:
        return sorted(list(self.category_encoder.classes_)) if self.is_trained else []

    def get_metrics(self) -> dict:
        return self.metrics

    def get_feature_importance(self) -> dict:
        if not self.is_trained:
            return {}
        features = ["region", "year", "crime_category", "population_lakhs"]
        importances = self.model.feature_importances_
        return {f: round(float(v), 4) for f, v in zip(features, importances)}
