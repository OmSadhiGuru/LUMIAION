from __future__ import annotations

from datetime import date

from athena.analytics.daily import summarize_daily
from athena.exporters.obsidian import write_daily_note
from athena.importers.manual import ManualImporter


def test_daily_note_contains_measurement_and_record_id(config, db):
    result = ManualImporter(config).import_record(
        {
            "metric_type": "body_weight_kg",
            "value": 81.2,
            "unit": "kg",
            "start_time": "2026-07-29T07:00:00-04:00",
            "timezone": "America/New_York",
        }
    )
    for r in result.records:
        db.insert_record(r)

    summary = summarize_daily(db, date(2026, 7, 29))
    path = write_daily_note(config, summary)

    content = path.read_text()
    assert "body_weight_kg" in content
    assert result.records[0].id in content
    assert "type: athena-daily-note" in content


def test_daily_note_separates_quality_warnings(config, db):
    result = ManualImporter(config).import_record(
        {
            "metric_type": "resting_heart_rate_bpm",
            "value": 500,
            "unit": "bpm",
            "start_time": "2026-07-29T07:00:00-04:00",
            "timezone": "America/New_York",
            "measurement_type": "measured",
        }
    )
    record = result.records[0]
    record.validation_status = "invalid"
    record.validation_messages.append("[INVALID] out of range")
    db.insert_record(record)

    summary = summarize_daily(db, date(2026, 7, 29))
    path = write_daily_note(config, summary)
    content = path.read_text()

    assert "## Data Quality Warnings" in content
    warnings_section = content.split("## Data Quality Warnings")[1]
    assert "out of range" in warnings_section


def test_empty_day_produces_note_with_no_records_message(config, db):
    summary = summarize_daily(db, date(2099, 1, 1))
    path = write_daily_note(config, summary)
    assert "No records for this date" in path.read_text()
