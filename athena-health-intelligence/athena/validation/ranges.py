"""Single-value physiological plausibility ranges.

Ranges are deliberately generous (they classify, not diagnose) — the
job here is to catch obviously-wrong extraction/unit errors ("skeletal
muscle mass of 450 kg"), not to flag normal human variation as invalid.
Anything outside `hard` bounds is INVALID (almost certainly an
extraction/unit error); outside `soft` but inside `hard` is QUESTIONABLE
(plausible for some people, worth a second look); inside `soft` is VALID
for range purposes (other checks may still downgrade it).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RangeResult:
    severity: str  # "valid" | "questionable" | "invalid"
    detail: str


# metric_type -> (soft_min, soft_max, hard_min, hard_max)
RANGES: dict[str, tuple[float, float, float, float]] = {
    "body_weight_kg": (35, 200, 20, 400),
    "body_fat_percent": (3, 45, 1, 70),
    "skeletal_muscle_mass_kg": (10, 50, 3, 80),
    "lean_body_mass_kg": (20, 100, 10, 150),
    "total_body_water_percent": (35, 65, 20, 80),
    "total_body_water_liters": (15, 60, 5, 100),
    "bmr_kcal": (800, 3000, 500, 4500),
    "visceral_fat_rating": (1, 20, 1, 30),
    "biological_age_years": (10, 90, 0, 120),
    "resting_heart_rate_bpm": (35, 100, 25, 200),
    "heart_rate_bpm": (40, 200, 25, 250),
    "blood_pressure_systolic_mmhg": (85, 160, 60, 250),
    "blood_pressure_diastolic_mmhg": (50, 100, 30, 150),
    "spo2_percent": (90, 100, 50, 100),
    "hrv_ms": (10, 200, 1, 400),
    "sleep_session_duration_minutes": (60, 720, 0, 1440),
    "steps_count": (0, 40000, 0, 100000),
    "calories_kcal": (800, 5000, 0, 10000),
}


def check_range(metric_type: str, value) -> RangeResult | None:
    """Returns None if the metric has no configured range or the value is
    not numeric (non-numeric values are a different importer's problem).
    """
    if metric_type not in RANGES or not isinstance(value, (int, float)):
        return None
    soft_min, soft_max, hard_min, hard_max = RANGES[metric_type]
    if value < hard_min or value > hard_max:
        return RangeResult(
            "invalid",
            f"{metric_type} value {value} is outside the physiologically plausible hard range "
            f"[{hard_min}, {hard_max}] — likely an extraction or unit error",
        )
    if value < soft_min or value > soft_max:
        return RangeResult(
            "questionable",
            f"{metric_type} value {value} is outside the typical range [{soft_min}, {soft_max}] "
            f"but within plausible bounds — recommend manual verification",
        )
    return None
