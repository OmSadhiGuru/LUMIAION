"""Simple, explainable trend direction — no smoothing model, no forecast.
Used by weekly.py to compare this week's average against last week's.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Trend:
    direction: str  # "up" | "down" | "flat" | "insufficient_data"
    delta: float | None
    delta_percent: float | None


def compute_trend(previous_avg: float | None, current_avg: float | None, flat_threshold: float = 0.02) -> Trend:
    if previous_avg is None or current_avg is None:
        return Trend(direction="insufficient_data", delta=None, delta_percent=None)
    delta = current_avg - previous_avg
    delta_pct = (delta / previous_avg) if previous_avg != 0 else None
    if delta_pct is None:
        direction = "flat" if delta == 0 else ("up" if delta > 0 else "down")
    elif abs(delta_pct) <= flat_threshold:
        direction = "flat"
    else:
        direction = "up" if delta_pct > 0 else "down"
    return Trend(direction=direction, delta=round(delta, 3), delta_percent=round(delta_pct, 4) if delta_pct is not None else None)
