"""
NSW Eco-Transit Monitor (ETM) — US09
IoT Sensor Data Collection and Cloud Processing (Prototype)

User Story:
As a TfNSW Sustainability Officer, I want IoT sensor data to be automatically
collected and analysed by the cloud data engine, so that I can access reliable
and updated sustainability information.

This is a PROTOTYPE using simulated sensor data (not a live production feed).
It demonstrates the data flow required by the ETM project:

  IoT Sensor Data -> Cloud Processing -> Structured Sustainability Data -> Dashboard-ready JSON

Output of this module feeds directly into Sovin's dashboard (US04), which
reads the structured JSON payload to render KPI cards and route-level charts.
"""

import json
import random
from datetime import datetime


# --- Layer 1: Simulated IoT Sensor Data Collection ---
def generate_sensor_reading(vehicle_id, route_id):
    """Simulates a single IoT sensor reading from an electric bus."""
    return {
        "vehicle_id": vehicle_id,
        "route_id": route_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "energy_consumption_kwh": round(random.uniform(0.8, 2.5), 2),
        "distance_km": round(random.uniform(3.0, 8.0), 2),
        "co2_emissions_kg": round(random.uniform(0.0, 0.3), 2),  # near-zero, electric fleet
    }


# --- Layer 2: Cloud Processing / Data Handling ---
BASELINE_EFFICIENCY_KWH_PER_KM = 0.30  # pre-ETM baseline used for the 15% target


def process_sensor_data(reading):
    """Calculates efficiency metrics from a raw sensor reading and flags
    whether the route is meeting ETM's 15% energy-saving target."""
    efficiency = reading["energy_consumption_kwh"] / reading["distance_km"]
    savings_pct = round((1 - (efficiency / BASELINE_EFFICIENCY_KWH_PER_KM)) * 100, 1)

    return {
        **reading,
        "efficiency_kwh_per_km": round(efficiency, 3),
        "vs_baseline_pct": savings_pct,
        "meets_15pct_target": savings_pct >= 15.0,
    }


# --- Layer 3: Dashboard-ready structured output ---
def build_dashboard_payload(readings):
    """Aggregates processed readings into the JSON structure Sovin's
    dashboard consumes to render fleet-wide KPIs and route-level charts."""
    processed = [process_sensor_data(r) for r in readings]
    fleet_avg_efficiency = round(
        sum(r["efficiency_kwh_per_km"] for r in processed) / len(processed), 3
    )
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "fleet_average_efficiency_kwh_per_km": fleet_avg_efficiency,
        "baseline_kwh_per_km": BASELINE_EFFICIENCY_KWH_PER_KM,
        "route_readings": processed,
    }


if __name__ == "__main__":
    # Simulated fleet: 3 electric buses across 2 routes (sample data, per ETM scope)
    sample_readings = [
        generate_sensor_reading("BUS-014", "M20"),
        generate_sensor_reading("BUS-027", "M20"),
        generate_sensor_reading("BUS-031", "333"),
    ]

    payload = build_dashboard_payload(sample_readings)
    print(json.dumps(payload, indent=2))