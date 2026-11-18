"""
CrimeLens — Smart Patrol Resource Allocation Optimizer
AI Dispatch Engine for algorithmic patrol deployment, deterrence maximization,
and rapid response unit assignment.
"""

from typing import List, Dict, Any, Optional
import math
from datetime import datetime


class PatrolOptimizer:
    """Calculates optimal patrol unit distribution and emergency dispatch tickets."""

    def __init__(self):
        # Patrol units in the fleet
        self.fleet_units = [
            {"id": "UNIT-101", "name": "Eagle-1 Mobile Cruiser", "type": "SUV Cruiser", "status": "patrolling", "current_zone": "Delhi Central"},
            {"id": "UNIT-102", "name": "Eagle-2 Rapid Response", "type": "Motorcycle Interceptor", "status": "standby", "current_zone": "India Gate"},
            {"id": "UNIT-103", "name": "Vanguard-1 Tactical", "type": "Command Van", "status": "patrolling", "current_zone": "Paharganj"},
            {"id": "UNIT-104", "name": "Sentinel-1 Drone Pilot", "type": "Autonomous Aerial Drone", "status": "airborne", "current_zone": "Connaught Place"},
            {"id": "UNIT-105", "name": "Shield-1 Night Patrol", "type": "PCR Patrol", "status": "patrolling", "current_zone": "ITO Crossing"},
            {"id": "UNIT-106", "name": "Shield-2 Rapid Response", "type": "Motorcycle Interceptor", "status": "standby", "current_zone": "South Delhi"},
        ]
        self.dispatch_history: List[Dict[str, Any]] = []

    def optimize_allocation(
        self,
        total_fleet_size: int = 30,
        regions_risk_data: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Formulate and solve patrol fleet allocation across sectors.
        Allocation is proportional to predicted crime density and geographic vulnerability.
        """
        total_fleet = max(6, min(150, total_fleet_size))

        # Default sectors if no live regions passed
        if not regions_risk_data:
            sectors = [
                {"name": "Delhi Central (Commercial / Transit)", "base_cases": 46500, "vulnerability_weight": 0.85, "vulnerability": "High"},
                {"name": "North Sector (Dense Residential)", "base_cases": 28400, "vulnerability_weight": 0.60, "vulnerability": "Moderate"},
                {"name": "East Sector (Industrial / Perimeter)", "base_cases": 35200, "vulnerability_weight": 0.75, "vulnerability": "High"},
                {"name": "South Sector (Institutional / Nightlife)", "base_cases": 21800, "vulnerability_weight": 0.50, "vulnerability": "Moderate"},
                {"name": "West Sector (Market Corridors)", "base_cases": 39100, "vulnerability_weight": 0.80, "vulnerability": "High"},
                {"name": "Transit Hubs & Outer Terminals", "base_cases": 51200, "vulnerability_weight": 0.95, "vulnerability": "Very High"},
            ]
        else:
            sectors = [
                {
                    "name": r["region"],
                    "base_cases": r.get("total_cases", 25000),
                    "vulnerability_weight": 0.5 + (0.1 * (i % 5)),
                    "vulnerability": r.get("risk_level", "Moderate"),
                }
                for i, r in enumerate(regions_risk_data[:8])
            ]

        # Calculate composite demand scores
        total_demand = 0.0
        for s in sectors:
            norm_cases = s["base_cases"] / 10000.0
            demand_score = norm_cases * (1.0 + (s["vulnerability_weight"] * 1.2))
            s["demand_score"] = demand_score
            total_demand += demand_score

        # Distribute patrol units proportionally with minimum floor of 1
        allocated_total = 0
        allocation_breakdown = []

        for s in sectors:
            ratio = s["demand_score"] / total_demand if total_demand > 0 else 1.0 / len(sectors)
            assigned_units = max(1, round(ratio * total_fleet))
            allocated_total += assigned_units

            # Expected response time reduces as assigned units increase: R(u) = base_time / sqrt(u)
            est_response_time_min = round(14.0 / math.sqrt(assigned_units), 1)

            # Estimated deterrence efficiency gain: 1 - exp(-0.16 * assigned_units)
            deterrence_pct = round((1.0 - math.exp(-0.16 * assigned_units)) * 100, 1)

            # Shift split (morning 25%, evening 35%, night 40%)
            morning_shift = max(1, round(assigned_units * 0.25))
            evening_shift = max(1, round(assigned_units * 0.35))
            night_shift = max(1, assigned_units - morning_shift - evening_shift)

            allocation_breakdown.append({
                "sector": s["name"],
                "vulnerability": s["vulnerability"],
                "base_cases": s["base_cases"],
                "assigned_units": assigned_units,
                "coverage_pct": round(ratio * 100, 1),
                "est_response_time_min": est_response_time_min,
                "projected_deterrence_gain_pct": deterrence_pct,
                "shifts": {
                    "morning": morning_shift,
                    "evening": evening_shift,
                    "night": night_shift,
                },
            })

        # Overall fleet metrics
        avg_response_time = round(
            sum(a["est_response_time_min"] for a in allocation_breakdown) / len(allocation_breakdown), 1
        )
        avg_deterrence_gain = round(
            sum(a["projected_deterrence_gain_pct"] for a in allocation_breakdown) / len(allocation_breakdown), 1
        )

        return {
            "total_fleet_size": total_fleet,
            "allocated_units": sum(a["assigned_units"] for a in allocation_breakdown),
            "sectors_count": len(allocation_breakdown),
            "overall_avg_response_time_min": avg_response_time,
            "overall_deterrence_gain_pct": avg_deterrence_gain,
            "allocation_breakdown": allocation_breakdown,
            "fleet_readiness": {
                "active_patrolling": sum(1 for u in self.fleet_units if u["status"] == "patrolling"),
                "airborne_drones": sum(1 for u in self.fleet_units if u["status"] == "airborne"),
                "standby_interceptors": sum(1 for u in self.fleet_units if u["status"] == "standby"),
            },
            "recent_dispatches": self.dispatch_history[-5:],
        }

    def dispatch_emergency_unit(
        self,
        alert_type: str,
        target_zone: str,
        severity: str = "critical",
    ) -> Dict[str, Any]:
        """Simulate real-time emergency response dispatch for reported incidents."""
        if severity == "critical":
            assigned_unit = next(
                (u for u in self.fleet_units if u["status"] == "standby" or "Rapid" in u["name"]),
                self.fleet_units[0],
            )
            est_eta = 4  # 4 minutes rapid interceptor
        else:
            assigned_unit = self.fleet_units[1 % len(self.fleet_units)]
            est_eta = 7

        ticket_id = f"DSP-{datetime.now().strftime('%H%M%S')}-{len(self.dispatch_history) + 1}"
        ticket = {
            "ticket_id": ticket_id,
            "timestamp": datetime.now().isoformat(),
            "alert_type": alert_type,
            "severity": severity,
            "target_zone": target_zone,
            "assigned_unit": assigned_unit["name"],
            "unit_type": assigned_unit["type"],
            "eta_minutes": est_eta,
            "status": "DISPATCHED_EN_ROUTE",
            "dispatch_protocol": (
                f"Immediate tactical response: {assigned_unit['name']} routed to {target_zone}. "
                f"Perimeter surveillance activated. ETA {est_eta} min."
            ),
        }
        self.dispatch_history.insert(0, ticket)
        return ticket
