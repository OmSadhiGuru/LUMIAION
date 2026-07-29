"""Trend-based anomaly detection: does a new value deviate sharply from
recent history for the same metric_type? This requires historical
context (unlike ranges.py) so it takes an explicit list of prior values
rather than reaching into the database itself — callers (CLI, tests)
decide what "recent history" means.
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_DEVIATION_THRESHOLD = 0.25  # 25% change from the recent mean


@dataclass
class AnomalyResult:
    severity: str  # "questionable"
    detail: str


def check_anomaly(
    metric_type: str,
    new_value: float,
    recent_values: list[float],
    threshold: float = DEFAULT_DEVIATION_THRESHOLD,
) -> AnomalyResult | None:
    if not recent_values or not isinstance(new_value, (int, float)):
        return None
    baseline = sum(recent_values) / len(recent_values)
    if baseline == 0:
        return None
    deviation = abs(new_value - baseline) / abs(baseline)
    if deviation > threshold:
        return AnomalyResult(
            severity="questionable",
            detail=(
                f"{metric_type} value {new_value} deviates {deviation:.0%} from the recent average "
                f"({baseline:.2f} over {len(recent_values)} prior records) — flagged for review, "
                f"not treated as false"
            ),
        )
    return None
