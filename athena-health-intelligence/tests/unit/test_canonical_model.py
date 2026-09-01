from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from athena.models.canonical import CanonicalHealthRecord


def _base_kwargs(**overrides):
    kwargs = dict(
        metric_type="body_weight_kg",
        start_time=datetime.now(timezone.utc),
        timezone="UTC",
        original_value=80.0,
        original_unit="kg",
        normalized_value=80.0,
        normalized_unit="kg",
        source_platform="manual",
        extraction_method="manual_entry",
        measurement_type="manual",
    )
    kwargs.update(overrides)
    return kwargs


def test_minimal_record_constructs_with_defaults():
    record = CanonicalHealthRecord(**_base_kwargs())
    assert record.id
    assert record.validation_status == "unverified"
    assert record.confidence == 0.0
    assert record.duplicate_status is None
    assert record.tags == []


def test_missing_value_is_stored_as_none_not_fabricated():
    record = CanonicalHealthRecord(**_base_kwargs(original_value=None, normalized_value=None))
    assert record.original_value is None
    assert record.normalized_value is None


def test_confidence_out_of_range_rejected():
    with pytest.raises(ValidationError):
        CanonicalHealthRecord(**_base_kwargs(confidence=1.5))


def test_unknown_measurement_type_rejected():
    with pytest.raises(ValidationError):
        CanonicalHealthRecord(**_base_kwargs(measurement_type="guessed"))


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        CanonicalHealthRecord(**_base_kwargs(made_up_field="nope"))


def test_json_round_trip_preserves_dict_value():
    record = CanonicalHealthRecord(**_base_kwargs(original_value={"a": 1}, normalized_value={"a": 1}))
    dumped = record.model_dump_json()
    restored = CanonicalHealthRecord.model_validate_json(dumped)
    assert restored.original_value == {"a": 1}
