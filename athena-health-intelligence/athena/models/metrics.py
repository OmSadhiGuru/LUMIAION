"""Canonical metric-type vocabulary and their normalized units.

This is deliberately a small, explicit registry rather than a free-text
field: every metric ATHENA can store has one canonical unit so
downstream code (validation, analytics, exporters) never has to guess
whether a weight value is kg or lb. New metric types must be added here
before an importer can normalize into them — that is a feature, not a
limitation: it is what keeps "unverified until confirmed" true for the
schema itself, not just for the values inside it.
"""

from __future__ import annotations

# metric_type -> canonical (normalized) unit
CANONICAL_UNITS: dict[str, str] = {
    # Body composition
    "body_weight_kg": "kg",
    "body_fat_percent": "%",
    "skeletal_muscle_mass_kg": "kg",
    "lean_body_mass_kg": "kg",
    "total_body_water_percent": "%",
    "total_body_water_liters": "L",
    "bmr_kcal": "kcal",
    "visceral_fat_rating": "rating",
    "biological_age_years": "years",
    # Cardiovascular
    "resting_heart_rate_bpm": "bpm",
    "heart_rate_bpm": "bpm",
    "blood_pressure_systolic_mmhg": "mmHg",
    "blood_pressure_diastolic_mmhg": "mmHg",
    "spo2_percent": "%",
    "hrv_ms": "ms",
    # Sleep
    "sleep_session_duration_minutes": "min",
    "sleep_stage_light_minutes": "min",
    "sleep_stage_deep_minutes": "min",
    "sleep_stage_rem_minutes": "min",
    "sleep_stage_awake_minutes": "min",
    # Activity
    "steps_count": "count",
    "activity_duration_minutes": "min",
    "activity_distance_km": "km",
    "vo2max_ml_kg_min": "mL/kg/min",
    # Nutrition
    "calories_kcal": "kcal",
    "protein_g": "g",
    "carbohydrate_g": "g",
    "fat_g": "g",
    "water_intake_ml": "mL",
}

BODY_COMPOSITION_METRICS = frozenset(
    {
        "body_weight_kg",
        "body_fat_percent",
        "skeletal_muscle_mass_kg",
        "lean_body_mass_kg",
        "total_body_water_percent",
        "total_body_water_liters",
        "bmr_kcal",
        "visceral_fat_rating",
        "biological_age_years",
    }
)

SLEEP_STAGE_METRICS = frozenset(
    {
        "sleep_stage_light_minutes",
        "sleep_stage_deep_minutes",
        "sleep_stage_rem_minutes",
        "sleep_stage_awake_minutes",
    }
)

NUTRITION_MACRO_METRICS = frozenset({"protein_g", "carbohydrate_g", "fat_g"})


def is_known_metric(metric_type: str) -> bool:
    return metric_type in CANONICAL_UNITS


def canonical_unit_for(metric_type: str) -> str | None:
    return CANONICAL_UNITS.get(metric_type)
