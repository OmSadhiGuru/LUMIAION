from __future__ import annotations

from athena.importers.health_connect import HealthConnectImporter


def test_synthetic_export_produces_expected_metric_types(config, fixtures_dir):
    result = HealthConnectImporter(config).import_source(fixtures_dir / "health_connect_export.json")
    assert result.ok
    metric_types = {r.metric_type for r in result.records}
    assert "body_weight_kg" in metric_types
    assert "spo2_percent" in metric_types
    assert "hrv_ms" in metric_types
    assert "blood_pressure_systolic_mmhg" in metric_types
    assert "blood_pressure_diastolic_mmhg" in metric_types
    assert "heart_rate_bpm" in metric_types
    assert "steps_count" in metric_types
    assert "sleep_session_duration_minutes" in metric_types


def test_heart_rate_samples_expand_to_individual_records(config, fixtures_dir):
    result = HealthConnectImporter(config).import_source(fixtures_dir / "health_connect_export.json")
    hr_records = [r for r in result.records if r.metric_type == "heart_rate_bpm"]
    assert len(hr_records) == 2


def test_sleep_stages_summed_from_stage_list(config, fixtures_dir):
    result = HealthConnectImporter(config).import_source(fixtures_dir / "health_connect_export.json")
    light = next(r for r in result.records if r.metric_type == "sleep_stage_light_minutes")
    deep = next(r for r in result.records if r.metric_type == "sleep_stage_deep_minutes")
    # two light segments: 23:00-01:00 (120m) + 04:00-06:30 (150m) = 270m
    assert light.normalized_value == 270.0
    assert deep.normalized_value == 90.0


def test_unsupported_record_type_reported_as_error_not_dropped_silently(config, tmp_path):
    import json

    bad = tmp_path / "bad_hc.json"
    bad.write_text(json.dumps({"records": [{"recordType": "SomethingNew"}]}), encoding="utf-8")
    result = HealthConnectImporter(config).import_source(bad)
    assert not result.ok
    assert "unsupported" in result.errors[0].lower()
