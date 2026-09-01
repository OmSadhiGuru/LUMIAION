"""Structured CSV importer.

Expected columns (header row required): metric_type, value, unit,
start_time, timezone. Optional columns: end_time, source_platform,
source_application, source_device, source_record_id, measurement_type,
tags (semicolon-separated).

`value` is parsed as float when possible, otherwise kept as the raw
string — CSV has no native type system, so a non-numeric value is never
silently coerced to 0 or discarded.
"""

from __future__ import annotations

import csv
from pathlib import Path

from athena.importers.base import (
    ImportResult,
    Importer,
    new_batch_id,
    preserve_raw_file,
    record_from_mapping,
)
from athena.models.source import ExtractionMethod, SourcePlatform

REQUIRED_COLUMNS = {"metric_type", "value", "start_time", "timezone"}


def _parse_value(raw: str):
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return raw


class CsvImporter(Importer):
    source_platform = SourcePlatform.MANUAL
    default_extraction_method = ExtractionMethod.STRUCTURED_CSV

    def import_source(self, source: str | Path) -> ImportResult:
        source = Path(source)
        batch_id = new_batch_id("csv")

        try:
            raw_path, _sha256 = preserve_raw_file(self.config, source, batch_id)
        except FileNotFoundError as exc:
            return ImportResult(batch_id=batch_id, errors=[str(exc)])

        records = []
        errors: list[str] = []

        with open(raw_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
            if missing:
                return ImportResult(
                    batch_id=batch_id,
                    errors=[f"CSV missing required columns: {sorted(missing)}"],
                    raw_source_path=str(raw_path),
                )
            for i, row in enumerate(reader):
                mapping = dict(row)
                mapping["value"] = _parse_value(row.get("value"))
                if row.get("tags"):
                    mapping["tags"] = [t.strip() for t in row["tags"].split(";") if t.strip()]
                try:
                    record = record_from_mapping(
                        mapping,
                        source_platform=self.source_platform,
                        source_application=None,
                        extraction_method=self.default_extraction_method,
                        batch_id=batch_id,
                        raw_source_path=str(raw_path),
                        default_measurement_type=mapping.get("measurement_type") or "unverified",
                    )
                    records.append(record)
                except (KeyError, ValueError, TypeError) as exc:
                    errors.append(f"row {i + 2}: rejected: {exc}")

        return ImportResult(batch_id=batch_id, records=records, errors=errors, raw_source_path=str(raw_path))
