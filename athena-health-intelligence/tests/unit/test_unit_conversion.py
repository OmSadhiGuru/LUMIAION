from __future__ import annotations

from athena.importers.base import normalize_value


def test_lb_converted_to_kg():
    value, unit, warnings = normalize_value("body_weight_kg", 176.37, "lb")
    assert unit == "kg"
    assert abs(value - 80.0) < 0.01
    assert warnings == []


def test_already_canonical_unit_passes_through():
    value, unit, warnings = normalize_value("body_weight_kg", 80.0, "kg")
    assert value == 80.0
    assert unit == "kg"
    assert warnings == []


def test_unrecognized_unit_flagged_not_silently_converted():
    value, unit, warnings = normalize_value("body_weight_kg", 80.0, "stone")
    assert value == 80.0  # unchanged
    assert unit == "stone"  # unchanged, not coerced to kg
    assert len(warnings) == 1
    assert "no known conversion" in warnings[0]


def test_missing_unit_flagged():
    value, unit, warnings = normalize_value("body_weight_kg", 80.0, None)
    assert len(warnings) == 1
    assert "missing original_unit" in warnings[0]


def test_unknown_metric_type_passes_through_with_warning():
    value, unit, warnings = normalize_value("some_new_metric", 5, "widgets")
    assert value == 5
    assert unit == "widgets"
    assert "unknown metric_type" in warnings[0]
