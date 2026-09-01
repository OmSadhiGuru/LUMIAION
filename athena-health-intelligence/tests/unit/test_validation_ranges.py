from __future__ import annotations

from athena.validation.ranges import check_range


def test_plausible_value_returns_none():
    assert check_range("body_weight_kg", 80.0) is None


def test_questionable_value_flagged():
    result = check_range("body_weight_kg", 25.0)
    assert result is not None
    assert result.severity == "questionable"


def test_impossible_value_flagged_invalid():
    result = check_range("skeletal_muscle_mass_kg", 450.0)
    assert result is not None
    assert result.severity == "invalid"


def test_unknown_metric_type_returns_none():
    assert check_range("some_unregistered_metric", 999999) is None


def test_non_numeric_value_returns_none():
    assert check_range("body_weight_kg", "heavy") is None
