from __future__ import annotations

from athena.importers.evolt import EvoltImporter
from athena.validation.engine import validate_records


def test_suspicious_evolt_scan_flagged_invalid_by_engine(config, db, fixtures_dir):
    result = EvoltImporter(config).import_source(fixtures_dir / "evolt_scan_suspicious.json")
    for r in result.records:
        db.insert_record(r)

    summary = validate_records(db)

    assert summary["invalid"] > 0
    weight = next(r for r in db.list_records() if r.metric_type == "body_weight_kg")
    smm = next(r for r in db.list_records() if r.metric_type == "skeletal_muscle_mass_kg")
    assert weight.validation_status == "invalid"
    assert smm.validation_status == "invalid"
    assert any("skeletal_muscle" in msg.lower() for msg in smm.validation_messages)


def test_valid_evolt_scan_not_flagged_invalid(config, db, fixtures_dir):
    result = EvoltImporter(config).import_source(fixtures_dir / "evolt_scan_valid.json")
    for r in result.records:
        db.insert_record(r)

    summary = validate_records(db)

    assert summary["invalid"] == 0
    weight = next(r for r in db.list_records() if r.metric_type == "body_weight_kg")
    assert weight.validation_status == "valid"


def test_extreme_heart_rate_flagged_by_range_check(config, db, fixtures_dir):
    from athena.importers.json_importer import JsonImporter

    result = JsonImporter(config).import_source(fixtures_dir / "records_batch.json")
    for r in result.records:
        db.insert_record(r)

    validate_records(db)

    extreme_hr = next(r for r in db.list_records() if r.metric_type == "resting_heart_rate_bpm" and r.normalized_value == 500)
    assert extreme_hr.validation_status == "invalid"
