"""Health Connect JSON importer — PARTIAL, untested against a real export.

Important caveat (see docs/source-capabilities.md): Android Health
Connect does not have a simple "export everything to JSON" button for
end users. The JSON shape this importer expects is the shape the (not
yet built — see section 12 of the master spec / android/ scaffold)
companion app is expected to produce when it reads records via the
Health Connect Kotlin API and serializes them. Until that companion app
exists and is tested on-device, this importer has only been exercised
against a hand-written synthetic fixture that mirrors Health Connect's
publicly documented record shapes (StepsRecord, HeartRateRecord,
WeightRecord, SleepSessionRecord, OxygenSaturationRecord,
HeartRateVariabilityRmssdRecord, BloodPressureRecord). Treat this as
PARTIAL, not FUNCTIONAL, until it has run against real exported data.

Expected input:
    {
      "records": [
        {"recordType": "Weight", "value": 81.2, "unit": "kg",
         "startTime": "...", "zoneOffset": "-04:00",
         "metadata": {"id": "...", "device": "...", "dataOrigin": "com.sec.android.app.shealth"}},
        {"recordType": "HeartRate", "samples": [{"time": "...", "beatsPerMinute": 62}], ...},
        {"recordType": "SleepSession", "startTime": "...", "endTime": "...",
         "stages": [{"stage": "deep", "startTime": "...", "endTime": "..."}], ...},
        ...
      ]
    }
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from athena.importers.base import ImportResult, Importer, new_batch_id, preserve_raw_file, record_from_mapping
from athena.models.source import ExtractionMethod, SourceApplication, SourcePlatform

_STAGE_NAME_MAP = {
    "light": "sleep_stage_light_minutes",
    "deep": "sleep_stage_deep_minutes",
    "rem": "sleep_stage_rem_minutes",
    "awake": "sleep_stage_awake_minutes",
}


def _stage_minutes(stage: dict) -> float | None:
    try:
        start = datetime.fromisoformat(stage["startTime"])
        end = datetime.fromisoformat(stage["endTime"])
        return (end - start).total_seconds() / 60.0
    except (KeyError, ValueError):
        return None


class HealthConnectImporter(Importer):
    source_platform = SourcePlatform.HEALTH_CONNECT
    default_extraction_method = ExtractionMethod.HEALTH_CONNECT_EXPORT

    def import_source(self, source: str | Path) -> ImportResult:
        source = Path(source)
        batch_id = new_batch_id("health_connect")
        raw_path, _sha256 = preserve_raw_file(self.config, source, batch_id)

        with open(raw_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        records = []
        errors: list[str] = []
        for i, hc_record in enumerate(payload.get("records", [])):
            try:
                records.extend(self._convert(hc_record, batch_id, str(raw_path)))
            except (KeyError, ValueError, TypeError) as exc:
                errors.append(f"record[{i}] ({hc_record.get('recordType')}) rejected: {exc}")

        return ImportResult(batch_id=batch_id, records=records, errors=errors, raw_source_path=str(raw_path))

    def _convert(self, hc_record: dict, batch_id: str, raw_path: str) -> list:
        record_type = hc_record.get("recordType")
        metadata = hc_record.get("metadata", {})
        common = {
            "timezone": hc_record.get("zoneOffset", "UTC"),
            "source_record_id": metadata.get("id"),
            "source_device": metadata.get("device"),
            "measurement_type": "device_estimated",
        }
        out = []

        if record_type == "Weight":
            out.append(self._make(
                "body_weight_kg", hc_record["value"], hc_record.get("unit", "kg"),
                hc_record["startTime"], batch_id, raw_path, common,
            ))
        elif record_type == "OxygenSaturation":
            out.append(self._make(
                "spo2_percent", hc_record["percentage"], "%",
                hc_record["startTime"], batch_id, raw_path, common,
            ))
        elif record_type == "HeartRateVariabilityRmssd":
            out.append(self._make(
                "hrv_ms", hc_record["heartRateVariabilityMillis"], "ms",
                hc_record["startTime"], batch_id, raw_path, common,
            ))
        elif record_type == "BloodPressure":
            out.append(self._make(
                "blood_pressure_systolic_mmhg", hc_record["systolic"], "mmHg",
                hc_record["startTime"], batch_id, raw_path, common,
            ))
            out.append(self._make(
                "blood_pressure_diastolic_mmhg", hc_record["diastolic"], "mmHg",
                hc_record["startTime"], batch_id, raw_path, common,
            ))
        elif record_type == "HeartRate":
            for sample in hc_record.get("samples", []):
                out.append(self._make(
                    "heart_rate_bpm", sample["beatsPerMinute"], "bpm",
                    sample["time"], batch_id, raw_path, common,
                ))
        elif record_type == "Steps":
            out.append(self._make(
                "steps_count", hc_record["count"], "count",
                hc_record["startTime"], batch_id, raw_path, common,
                end_time=hc_record.get("endTime"),
            ))
        elif record_type == "SleepSession":
            start, end = hc_record["startTime"], hc_record["endTime"]
            duration_min = (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds() / 60.0
            out.append(self._make(
                "sleep_session_duration_minutes", duration_min, "min",
                start, batch_id, raw_path, common, end_time=end,
            ))
            stage_totals: dict[str, float] = {}
            for stage in hc_record.get("stages", []):
                minutes = _stage_minutes(stage)
                key = _STAGE_NAME_MAP.get(stage.get("stage"))
                if key and minutes is not None:
                    stage_totals[key] = stage_totals.get(key, 0.0) + minutes
            for metric_type, minutes in stage_totals.items():
                out.append(self._make(metric_type, minutes, "min", start, batch_id, raw_path, common, end_time=end))
        else:
            raise ValueError(f"unsupported Health Connect recordType: {record_type!r}")

        return out

    def _make(self, metric_type, value, unit, start_time, batch_id, raw_path, common, end_time=None):
        mapping = {
            "metric_type": metric_type,
            "value": value,
            "unit": unit,
            "start_time": start_time,
            "end_time": end_time,
            **common,
        }
        return record_from_mapping(
            mapping,
            source_platform=self.source_platform,
            source_application=SourceApplication.HEALTH_CONNECT_APP,
            extraction_method=self.default_extraction_method,
            batch_id=batch_id,
            raw_source_path=raw_path,
            default_measurement_type="device_estimated",
        )
