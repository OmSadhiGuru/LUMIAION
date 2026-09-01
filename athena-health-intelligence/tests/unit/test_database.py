from __future__ import annotations

from datetime import datetime, timezone

from athena.models.canonical import CanonicalHealthRecord


def _record(**overrides) -> CanonicalHealthRecord:
    kwargs = dict(
        metric_type="body_weight_kg",
        start_time=datetime(2026, 7, 29, 7, 0, tzinfo=timezone.utc),
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
    return CanonicalHealthRecord(**kwargs)


def test_insert_and_get_round_trip(db):
    record = _record()
    db.insert_record(record)
    fetched = db.get_record(record.id)
    assert fetched is not None
    assert fetched.id == record.id
    assert fetched.normalized_value == 80.0
    assert fetched.start_time == record.start_time


def test_schema_version_reported(db):
    assert db.schema_version() == 1


def test_list_records_filters_by_metric_type(db):
    db.insert_record(_record(metric_type="body_weight_kg"))
    db.insert_record(_record(metric_type="resting_heart_rate_bpm", normalized_value=60, normalized_unit="bpm", original_value=60, original_unit="bpm"))
    results = db.list_records(metric_type="body_weight_kg")
    assert len(results) == 1
    assert results[0].metric_type == "body_weight_kg"


def test_update_validation_persists(db):
    record = _record()
    db.insert_record(record)
    db.update_validation(record.id, validation_status="questionable", confidence=0.4, validation_messages=["flagged"])
    fetched = db.get_record(record.id)
    assert fetched.validation_status == "questionable"
    assert fetched.confidence == 0.4
    assert fetched.validation_messages == ["flagged"]


def test_mark_duplicate_and_exclude(db):
    original = _record()
    dup = _record()
    db.insert_record(original)
    db.insert_record(dup)
    db.mark_duplicate(dup.id, duplicate_status="duplicate", duplicate_of=original.id)
    all_records = db.list_records()
    unique_only = db.list_records(exclude_duplicates=True)
    assert len(all_records) == 2
    assert len(unique_only) == 1
    assert unique_only[0].id == original.id


def test_string_value_round_trips_not_coerced_to_number(db):
    record = _record(metric_type="notes", original_value="fasted", normalized_value="fasted", original_unit=None, normalized_unit=None)
    db.insert_record(record)
    fetched = db.get_record(record.id)
    assert fetched.normalized_value == "fasted"
    assert isinstance(fetched.normalized_value, str)
