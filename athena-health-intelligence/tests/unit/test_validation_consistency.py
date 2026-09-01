from __future__ import annotations

from datetime import datetime, timezone

from athena.models.canonical import CanonicalHealthRecord
from athena.validation.consistency import (
    check_body_composition_group,
    check_calorie_reconciliation,
    check_sleep_stages,
)


def test_calorie_reconciliation_within_tolerance_passes():
    # 100g protein + 100g carb + 50g fat = 400+400+450 = 1250 kcal, stated 1280 -> ~2.4% off
    assert check_calorie_reconciliation(100, 100, 50, 1280) is None


def test_calorie_reconciliation_mismatch_flagged():
    finding = check_calorie_reconciliation(100, 100, 50, 2000)
    assert finding is not None
    assert finding.severity == "questionable"
    assert "calories_kcal" in finding.metric_types


def test_calorie_reconciliation_missing_field_skips_check():
    assert check_calorie_reconciliation(100, None, 50, 1500) is None


def test_sleep_stage_sum_matches_duration():
    assert check_sleep_stages(480, {"sleep_stage_light_minutes": 240, "sleep_stage_deep_minutes": 120, "sleep_stage_rem_minutes": 120}) is None


def test_sleep_stage_sum_mismatch_flagged():
    finding = check_sleep_stages(480, {"sleep_stage_light_minutes": 100, "sleep_stage_deep_minutes": 50})
    assert finding is not None
    assert finding.severity == "questionable"


def test_sleep_negative_duration_flagged_invalid():
    finding = check_sleep_stages(-10, {"sleep_stage_light_minutes": 50})
    assert finding is not None
    assert finding.severity == "invalid"


def _record(metric_type, value, source_record_id="scan-1"):
    return CanonicalHealthRecord(
        metric_type=metric_type,
        start_time=datetime(2026, 7, 20, 8, 0, tzinfo=timezone.utc),
        timezone="UTC",
        original_value=value,
        original_unit=None,
        normalized_value=value,
        normalized_unit=None,
        source_platform="evolt",
        source_record_id=source_record_id,
        extraction_method="verified_field_mapping",
        measurement_type="device_estimated",
    )


def test_skeletal_muscle_exceeding_weight_flagged_invalid():
    records = [_record("body_weight_kg", 80.0), _record("skeletal_muscle_mass_kg", 85.0)]
    findings = check_body_composition_group(records)
    checks = {f.check for f in findings}
    assert "skeletal_muscle_exceeds_weight" in checks
    assert all(f.severity == "invalid" for f in findings if f.check == "skeletal_muscle_exceeds_weight")


def test_lean_mass_exceeding_weight_flagged_invalid():
    records = [_record("body_weight_kg", 70.0), _record("lean_body_mass_kg", 75.0)]
    findings = check_body_composition_group(records)
    assert any(f.check == "lean_mass_exceeds_weight" for f in findings)


def test_skeletal_muscle_exceeding_lean_mass_flagged():
    records = [_record("skeletal_muscle_mass_kg", 50.0), _record("lean_body_mass_kg", 40.0)]
    findings = check_body_composition_group(records)
    assert any(f.check == "skeletal_muscle_exceeds_lean_mass" for f in findings)


def test_implausible_total_body_water_flagged():
    records = [_record("total_body_water_percent", 999.0)]
    findings = check_body_composition_group(records)
    assert any(f.check == "total_body_water_implausible" for f in findings)


def test_physiologically_plausible_scan_produces_no_findings():
    records = [
        _record("body_weight_kg", 80.0),
        _record("skeletal_muscle_mass_kg", 35.0),
        _record("lean_body_mass_kg", 62.0),
        _record("body_fat_percent", 18.0),
        _record("total_body_water_percent", 55.0),
    ]
    findings = check_body_composition_group(records)
    assert findings == []
