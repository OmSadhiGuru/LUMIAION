from __future__ import annotations

from athena.validation.anomalies import check_anomaly


def test_no_history_returns_none():
    assert check_anomaly("body_weight_kg", 80.0, []) is None


def test_value_within_threshold_returns_none():
    assert check_anomaly("body_weight_kg", 81.0, [80.0, 80.5, 79.8]) is None


def test_value_far_from_history_flagged():
    result = check_anomaly("resting_heart_rate_bpm", 500.0, [58.0, 60.0, 59.0])
    assert result is not None
    assert result.severity == "questionable"
