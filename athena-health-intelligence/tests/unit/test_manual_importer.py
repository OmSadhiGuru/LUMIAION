from __future__ import annotations

import pytest

from athena.importers.manual import ManualImporter


def test_manual_import_produces_one_record(config):
    result = ManualImporter(config).import_record(
        {
            "metric_type": "body_weight_kg",
            "value": 81.2,
            "unit": "kg",
            "start_time": "2026-07-29T07:00:00-04:00",
            "timezone": "America/New_York",
        }
    )
    assert result.ok
    assert len(result.records) == 1
    record = result.records[0]
    assert record.source_platform == "manual"
    assert record.measurement_type == "manual"
    assert record.raw_source_path is None
    assert record.import_batch_id.startswith("manual-")


def test_manual_import_missing_metric_type_errors(config):
    result = ManualImporter(config).import_record({"value": 1, "start_time": "2026-07-29T07:00:00", "timezone": "UTC"})
    assert not result.ok
    assert result.records == []


def test_manual_import_missing_value_stored_as_missing_not_fabricated(config):
    result = ManualImporter(config).import_record(
        {"metric_type": "body_weight_kg", "value": None, "start_time": "2026-07-29T07:00:00", "timezone": "UTC"}
    )
    assert result.ok
    record = result.records[0]
    assert record.original_value is None
    assert record.normalized_value is None
    assert any("missing" in m for m in record.validation_messages)
