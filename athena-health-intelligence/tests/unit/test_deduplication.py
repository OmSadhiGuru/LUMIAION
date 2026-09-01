from __future__ import annotations

from datetime import datetime, timedelta, timezone

from athena.deduplication.engine import deduplicate
from athena.models.canonical import CanonicalHealthRecord


def _record(value, start_time, metric_type="body_weight_kg"):
    return CanonicalHealthRecord(
        metric_type=metric_type,
        start_time=start_time,
        timezone="UTC",
        original_value=value,
        original_unit="kg",
        normalized_value=value,
        normalized_unit="kg",
        source_platform="manual",
        extraction_method="manual_entry",
        measurement_type="manual",
    )


def test_near_duplicate_marked(db):
    t = datetime(2026, 7, 29, 7, 0, tzinfo=timezone.utc)
    original = _record(80.0, t)
    near_dup = _record(80.05, t + timedelta(minutes=1))
    db.insert_record(original)
    db.insert_record(near_dup)

    result = deduplicate(db)

    assert result["duplicates_found"] == 1
    fetched_dup = db.get_record(near_dup.id)
    fetched_orig = db.get_record(original.id)
    assert fetched_dup.duplicate_status == "duplicate"
    assert fetched_dup.duplicate_of == original.id
    assert fetched_orig.duplicate_status == "unique"


def test_different_values_not_marked_duplicate(db):
    t = datetime(2026, 7, 29, 7, 0, tzinfo=timezone.utc)
    db.insert_record(_record(80.0, t))
    db.insert_record(_record(85.0, t + timedelta(minutes=1)))

    result = deduplicate(db)

    assert result["duplicates_found"] == 0


def test_far_apart_in_time_not_marked_duplicate(db):
    t = datetime(2026, 7, 29, 7, 0, tzinfo=timezone.utc)
    db.insert_record(_record(80.0, t))
    db.insert_record(_record(80.0, t + timedelta(hours=5)))

    result = deduplicate(db)

    assert result["duplicates_found"] == 0


def test_duplicates_excluded_from_default_list(db):
    t = datetime(2026, 7, 29, 7, 0, tzinfo=timezone.utc)
    original = _record(80.0, t)
    dup = _record(80.0, t + timedelta(seconds=30))
    db.insert_record(original)
    db.insert_record(dup)
    deduplicate(db)

    assert len(db.list_records(exclude_duplicates=True)) == 1
    assert len(db.list_records(exclude_duplicates=False)) == 2
