from __future__ import annotations

from athena.importers.csv_importer import CsvImporter
from athena.importers.json_importer import JsonImporter


def test_json_importer_reads_batch(config, fixtures_dir):
    result = JsonImporter(config).import_source(fixtures_dir / "records_batch.json")
    assert result.ok
    assert len(result.records) == 4
    assert all(r.source_platform == "manual" for r in result.records)


def test_json_importer_preserves_raw_file(config, fixtures_dir):
    result = JsonImporter(config).import_source(fixtures_dir / "records_batch.json")
    raw_path = config.raw_dir / result.batch_id / "records_batch.json"
    assert raw_path.exists()
    assert result.raw_source_path == str(raw_path)


def test_json_importer_missing_file_reports_error(config, tmp_path):
    result = JsonImporter(config).import_source(tmp_path / "does_not_exist.json")
    assert not result.ok
    assert result.records == []


def test_csv_importer_reads_rows(config, fixtures_dir):
    result = CsvImporter(config).import_source(fixtures_dir / "records.csv")
    assert result.ok
    assert len(result.records) == 2
    metric_types = {r.metric_type for r in result.records}
    assert metric_types == {"body_weight_kg", "steps_count"}


def test_csv_importer_missing_required_column_errors(config, tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("metric_type,value\nbody_weight_kg,80\n", encoding="utf-8")
    result = CsvImporter(config).import_source(bad_csv)
    assert not result.ok
    assert "missing required columns" in result.errors[0].lower()


def test_csv_importer_non_numeric_value_preserved_as_string(config, tmp_path):
    csv_path = tmp_path / "notes.csv"
    csv_path.write_text(
        "metric_type,value,unit,start_time,timezone\nnotes,fasted,,2026-07-20T08:00:00,UTC\n", encoding="utf-8"
    )
    result = CsvImporter(config).import_source(csv_path)
    assert result.ok
    assert result.records[0].original_value == "fasted"
