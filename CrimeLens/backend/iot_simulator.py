"""
CrimeLens — IoT Safety Simulator Module
Generates simulated sensor readings and alerts in software.
No physical hardware is required or connected.
"""

import random
import time
from datetime import datetime, timedelta
from typing import Optional


class IoTSimulator:
    """Software simulator for ESP32-style safety sensors."""

    def __init__(self):
        self.alerts: list[dict] = []
        self.sensor_state = {
            "pir_motion": False,
            "light_intensity": 50,    # 0-100 scale (0=dark, 100=bright)
            "sound_level": 30,        # 0-100 dB scale
            "sos_active": False,
            "timestamp": datetime.now().isoformat(),
            "note": "All values are software-simulated. No physical sensors connected.",
        }
        # Generate some demo alerts on startup
        self._generate_demo_history()

    def _generate_demo_history(self):
        """Create a small set of historical demo alerts."""
        demo_events = [
            {"type": "motion_detected", "severity": "warning", "message": "PIR motion sensor triggered in Zone A (simulated)"},
            {"type": "low_light", "severity": "info", "message": "Ambient light dropped below threshold — area may be poorly lit (simulated)"},
            {"type": "loud_sound", "severity": "warning", "message": "Sound level exceeded 80 dB in Zone B (simulated)"},
            {"type": "sos_triggered", "severity": "critical", "message": "SOS button pressed — emergency alert (simulated)"},
            {"type": "motion_detected", "severity": "warning", "message": "Repeated motion detected near perimeter (simulated)"},
        ]
        now = datetime.now()
        for i, evt in enumerate(demo_events):
            self.alerts.append({
                "id": i + 1,
                "timestamp": (now - timedelta(minutes=random.randint(5, 120))).isoformat(),
                **evt,
            })
        self.alerts.sort(key=lambda x: x["timestamp"], reverse=True)

    def get_sensor_readings(self) -> dict:
        """Return current simulated sensor readings."""
        self.sensor_state["timestamp"] = datetime.now().isoformat()
        return self.sensor_state

    def update_sensor(
        self,
        pir_motion: Optional[bool] = None,
        light_intensity: Optional[int] = None,
        sound_level: Optional[int] = None,
        sos_active: Optional[bool] = None,
    ) -> dict:
        """Update simulated sensor values and generate alerts if thresholds exceeded."""
        if pir_motion is not None:
            self.sensor_state["pir_motion"] = pir_motion
        if light_intensity is not None:
            self.sensor_state["light_intensity"] = max(0, min(100, light_intensity))
        if sound_level is not None:
            self.sensor_state["sound_level"] = max(0, min(100, sound_level))
        if sos_active is not None:
            self.sensor_state["sos_active"] = sos_active

        self.sensor_state["timestamp"] = datetime.now().isoformat()

        # Check alert rules
        new_alerts = []
        next_id = max((a["id"] for a in self.alerts), default=0) + 1

        if self.sensor_state["pir_motion"]:
            new_alerts.append({
                "id": next_id,
                "timestamp": datetime.now().isoformat(),
                "type": "motion_detected",
                "severity": "warning",
                "message": "PIR motion sensor triggered (simulated)",
            })
            next_id += 1

        if self.sensor_state["light_intensity"] < 20:
            new_alerts.append({
                "id": next_id,
                "timestamp": datetime.now().isoformat(),
                "type": "low_light",
                "severity": "info",
                "message": f"Low ambient light: {self.sensor_state['light_intensity']}% — area may be unsafe (simulated)",
            })
            next_id += 1

        if self.sensor_state["sound_level"] > 75:
            new_alerts.append({
                "id": next_id,
                "timestamp": datetime.now().isoformat(),
                "type": "loud_sound",
                "severity": "warning",
                "message": f"High sound level: {self.sensor_state['sound_level']} dB detected (simulated)",
            })
            next_id += 1

        if self.sensor_state["sos_active"]:
            new_alerts.append({
                "id": next_id,
                "timestamp": datetime.now().isoformat(),
                "type": "sos_triggered",
                "severity": "critical",
                "message": "SOS emergency button activated (simulated)",
            })
            next_id += 1

        self.alerts = new_alerts + self.alerts
        return {
            "sensor_state": self.sensor_state,
            "new_alerts": new_alerts,
            "total_alerts": len(self.alerts),
        }

    def get_alerts(self, limit: int = 50) -> list[dict]:
        """Return recent alerts, newest first."""
        return self.alerts[:limit]

    def generate_random_event(self) -> dict:
        """Generate a single random simulated sensor event for demo purposes."""
        event_type = random.choice(["motion_detected", "low_light", "loud_sound", "normal"])
        next_id = max((a["id"] for a in self.alerts), default=0) + 1

        if event_type == "motion_detected":
            zones = ["Zone A", "Zone B", "Zone C", "Perimeter"]
            alert = {
                "id": next_id,
                "timestamp": datetime.now().isoformat(),
                "type": "motion_detected",
                "severity": "warning",
                "message": f"Motion detected in {random.choice(zones)} (simulated)",
            }
            self.sensor_state["pir_motion"] = True
        elif event_type == "low_light":
            light_val = random.randint(2, 18)
            alert = {
                "id": next_id,
                "timestamp": datetime.now().isoformat(),
                "type": "low_light",
                "severity": "info",
                "message": f"Light level dropped to {light_val}% (simulated)",
            }
            self.sensor_state["light_intensity"] = light_val
        elif event_type == "loud_sound":
            sound_val = random.randint(76, 98)
            alert = {
                "id": next_id,
                "timestamp": datetime.now().isoformat(),
                "type": "loud_sound",
                "severity": "warning",
                "message": f"Sound level at {sound_val} dB (simulated)",
            }
            self.sensor_state["sound_level"] = sound_val
        else:
            # Normal reading, no alert
            self.sensor_state["pir_motion"] = False
            self.sensor_state["light_intensity"] = random.randint(40, 80)
            self.sensor_state["sound_level"] = random.randint(20, 45)
            return {"event": "normal", "sensor_state": self.sensor_state, "alert": None}

        self.sensor_state["timestamp"] = datetime.now().isoformat()
        self.alerts.insert(0, alert)
        return {"event": event_type, "sensor_state": self.sensor_state, "alert": alert}
