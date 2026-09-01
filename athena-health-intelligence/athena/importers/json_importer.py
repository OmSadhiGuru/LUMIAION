"""Structured JSON importer.

Expected input shape (see schemas/canonical-health-record.schema.json for
the full field vocabulary this maps into):

    {
      "source_platform": "manual",          # optional default for all records
      "source_application": "...",           # optional default
      "records": [
        {"metric_type": "body_weight_kg", "value": 81.2, "unit": "kg",
         "start_time": "2026-07-29T07:00:00-04:00", "timezone": "America/New_York"},
        ...
      ]
    }

A bare list of record mappings (no wrapper object) is also accepted.
Every record is preserved even if it fails to parse — failures are
collected in ImportResult.errors with enough context to fix the file
rather than being silently dropped.
"""

from __future__ import annotations

import json
from pathlib import Path

from athena.config import AthenaConfig
from athena.importers.base import (
    ImportResult,
    Importer,
    new_batch_id,
    preserve_raw_file,
    record_from_mapping,
)
from athena.models.source import ExtractionMethod, SourcePlatform


class JsonImporter(Importer):
    source_platform = SourcePlatform.MANUAL
    default_extraction_method = ExtractionMethod.STRUCTURED_JSON

    def import_source(self, source: str | Path) -> ImportResult:
        source = Path(source)
        batch_id = new_batch_id("json")
        errors: list[str] = []
        records = []

        try:
            raw_path, _sha256 = preserve_raw_file(self.config, source, batch_id)
        except FileNotFoundError as exc:
            return ImportResult(batch_id=batch_id, errors=[str(exc)])

        with open(raw_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        if isinstance(payload, list):
            default_platform = self.source_platform
            default_app = None
            entries = payload
        elif "metric_type" in payload:
            # A bare single-record mapping, not wrapped in {"records": [...]}.
            default_platform = self.source_platform
            default_app = None
            entries = [payload]
        else:
            default_platform = payload.get("source_platform", self.source_platform)
            default_app = payload.get("source_application")
            entries = payload.get("records", [])

        for i, mapping in enumerate(entries):
            try:
                record = record_from_mapping(
                    mapping,
                    source_platform=default_platform,
                    source_application=default_app,
                    extraction_method=self.default_extraction_method,
                    batch_id=batch_id,
                    raw_source_path=str(raw_path),
                    default_measurement_type=mapping.get("measurement_type", "unverified"),
                )
                records.append(record)
            except (KeyError, ValueError, TypeError) as exc:
                errors.append(f"record[{i}] rejected: {exc}")

        return ImportResult(batch_id=batch_id, records=records, errors=errors, raw_source_path=str(raw_path))
