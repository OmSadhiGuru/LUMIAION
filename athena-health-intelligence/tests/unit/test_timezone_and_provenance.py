from __future__ import annotations

from athena.importers.manual import ManualImporter


def test_timezone_field_and_offset_preserved(config):
    result = ManualImporter(config).import_record(
        {
            "metric_type": "body_weight_kg",
            "value": 81.2,
            "unit": "kg",
            "start_time": "2026-07-29T07:00:00-04:00",
            "timezone": "America/New_York",
        }
    )
    record = result.records[0]
    assert record.timezone == "America/New_York"
    assert record.start_time.utcoffset().total_seconds() == -4 * 3600


def test_provenance_fields_populated(config):
    result = ManualImporter(config).import_record(
        {
            "metric_type": "body_weight_kg",
            "value": 81.2,
            "unit": "kg",
            "start_time": "2026-07-29T07:00:00-04:00",
            "timezone": "America/New_York",
        }
    )
    record = result.records[0]
    assert record.source_platform == "manual"
    assert record.extraction_method == "manual_entry"
    assert record.import_batch_id == result.batch_id
    assert record.imported_at is not None
    assert record.transformation_version
    assert record.transformations


def test_json_import_provenance_includes_raw_source_path(config, fixtures_dir):
    from athena.importers.json_importer import JsonImporter

    result = JsonImporter(config).import_source(fixtures_dir / "manual_record.json")
    record = result.records[0]
    assert record.raw_source_path is not None
    assert record.raw_source_path.endswith("manual_record.json")
