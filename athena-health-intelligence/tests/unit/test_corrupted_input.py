from __future__ import annotations

import pytest

from athena.importers.csv_importer import CsvImporter
from athena.importers.evolt import EvoltImporter
from athena.importers.json_importer import JsonImporter


def test_malformed_json_raises_decode_error_not_silently_ignored(config, tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(Exception):
        JsonImporter(config).import_source(bad)


def test_json_record_missing_required_field_reported_as_error_not_dropped(config, tmp_path):
    import json

    bad = tmp_path / "missing_field.json"
    bad.write_text(json.dumps({"records": [{"value": 80.0, "start_time": "2026-07-29T07:00:00", "timezone": "UTC"}]}), encoding="utf-8")
    result = JsonImporter(config).import_source(bad)
    assert not result.ok
    assert "rejected" in result.errors[0]


def test_evolt_malformed_json_raises(config, tmp_path):
    bad = tmp_path / "bad_evolt.json"
    bad.write_text("not json at all", encoding="utf-8")
    with pytest.raises(Exception):
        EvoltImporter(config).import_source(bad)


def test_csv_empty_file_reports_missing_columns(config, tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    result = CsvImporter(config).import_source(empty)
    assert not result.ok
