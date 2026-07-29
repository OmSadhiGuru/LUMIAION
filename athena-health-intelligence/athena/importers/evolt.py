"""Evolt 360 body-composition scan importer.

Implemented in stages, per the ATHENA rules — do not assume PDF
extraction is reliable:

  Stage 1 (IMPLEMENTED): structured JSON/CSV input, one row/entry per
    scanned field. This is the only path wired into the CLI.
  Stage 2 (PARTIAL): field-label -> metric_type mapping is hand-verified
    (EVOLT_FIELD_LABEL_MAP below) rather than guessed, so a recognized
    label gets extraction_method=verified_field_mapping; an
    unrecognized label is still imported (never dropped) but tagged
    extraction_method=structured_json and flagged for review.
  Stage 3 (NOT IMPLEMENTED): PDF extraction. import_pdf() raises
    NotImplementedError on purpose — there is no PDF layout parser in
    this codebase, and building one without a confidence-scored,
    human-reviewed path would risk exactly the fabrication the ATHENA
    rules forbid.

Every scan also produces a review Markdown file
(evolt-import-review-YYYY-MM-DD.md) that lists every extracted field,
its validation result, and an explicit UNCONFIRMED status — nothing
from this importer should be treated as ground truth until a human
reads that file against the original report.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from athena.config import AthenaConfig
from athena.importers.base import (
    ImportResult,
    Importer,
    new_batch_id,
    preserve_raw_file,
    record_from_mapping,
)
from athena.models.canonical import CanonicalHealthRecord
from athena.models.source import ExtractionMethod, SourceApplication, SourcePlatform
from athena.validation.consistency import check_body_composition_group
from athena.validation.ranges import check_range

# Evolt 360 report label -> (metric_type, expected_unit). Hand-verified
# against Evolt's own report glossary — extend this table rather than
# guessing at unrecognized labels.
EVOLT_FIELD_LABEL_MAP: dict[str, tuple[str, str]] = {
    "weight": ("body_weight_kg", "kg"),
    "body weight": ("body_weight_kg", "kg"),
    "body fat": ("body_fat_percent", "%"),
    "body fat percentage": ("body_fat_percent", "%"),
    "skeletal muscle mass": ("skeletal_muscle_mass_kg", "kg"),
    "lean body mass": ("lean_body_mass_kg", "kg"),
    "total body water": ("total_body_water_percent", "%"),
    "bmr": ("bmr_kcal", "kcal"),
    "basal metabolic rate": ("bmr_kcal", "kcal"),
    "visceral fat rating": ("visceral_fat_rating", "rating"),
    "biological age": ("biological_age_years", "years"),
}


class EvoltImporter(Importer):
    source_platform = SourcePlatform.EVOLT
    default_extraction_method = ExtractionMethod.STRUCTURED_JSON

    def import_source(self, source: str | Path) -> ImportResult:
        source = Path(source)
        if source.suffix.lower() == ".pdf":
            raise NotImplementedError(
                "Evolt PDF extraction (Stage 3) is not implemented. Export the scan as "
                "structured JSON/CSV instead, or see docs/architecture.md for the staged "
                "importer plan."
            )
        if source.suffix.lower() == ".csv":
            return self._import_csv(source)
        return self._import_json(source)

    def _import_json(self, source: Path) -> ImportResult:
        batch_id = new_batch_id("evolt")
        raw_path, _sha256 = preserve_raw_file(self.config, source, batch_id)
        with open(raw_path, "r", encoding="utf-8") as f:
            payload = json.load(f)

        scan_id = payload.get("scan_id") or batch_id
        scan_date = payload.get("scan_date")
        fields = payload.get("fields", [])
        records, errors = self._build_records(fields, scan_id, scan_date, batch_id, str(raw_path))
        self._write_review_file(records, errors, raw_path)
        return ImportResult(batch_id=batch_id, records=records, errors=errors, raw_source_path=str(raw_path))

    def _import_csv(self, source: Path) -> ImportResult:
        import csv as csv_module

        batch_id = new_batch_id("evolt")
        raw_path, _sha256 = preserve_raw_file(self.config, source, batch_id)
        with open(raw_path, "r", encoding="utf-8", newline="") as f:
            reader = csv_module.DictReader(f)
            rows = list(reader)
        if not rows:
            return ImportResult(batch_id=batch_id, errors=["CSV has no data rows"], raw_source_path=str(raw_path))
        scan_id = rows[0].get("scan_id") or batch_id
        scan_date = rows[0].get("scan_date")
        fields = [{"label": r.get("label"), "value": r.get("value"), "unit": r.get("unit")} for r in rows]
        records, errors = self._build_records(fields, scan_id, scan_date, batch_id, str(raw_path))
        self._write_review_file(records, errors, raw_path)
        return ImportResult(batch_id=batch_id, records=records, errors=errors, raw_source_path=str(raw_path))

    def _build_records(
        self, fields: list[dict], scan_id: str, scan_date: str | None, batch_id: str, raw_path: str
    ) -> tuple[list[CanonicalHealthRecord], list[str]]:
        records: list[CanonicalHealthRecord] = []
        errors: list[str] = []
        start_time = scan_date or datetime.now().isoformat()

        for i, field_entry in enumerate(fields):
            label_raw = (field_entry.get("label") or "").strip()
            label = label_raw.lower()
            value = field_entry.get("value")
            try:
                value = float(value)
            except (TypeError, ValueError):
                pass

            if label in EVOLT_FIELD_LABEL_MAP:
                metric_type, expected_unit = EVOLT_FIELD_LABEL_MAP[label]
                extraction_method = ExtractionMethod.VERIFIED_FIELD_MAPPING
                unit = field_entry.get("unit") or expected_unit
            else:
                metric_type = f"evolt_unmapped__{label_raw.replace(' ', '_').lower()}" if label_raw else f"evolt_unmapped__field_{i}"
                extraction_method = ExtractionMethod.STRUCTURED_JSON
                unit = field_entry.get("unit")

            mapping = {
                "metric_type": metric_type,
                "value": value,
                "unit": unit,
                "start_time": start_time,
                "timezone": field_entry.get("timezone", "UTC"),
                "source_record_id": scan_id,
                "measurement_type": "device_estimated",
                "extraction_method": extraction_method,
            }
            try:
                record = record_from_mapping(
                    mapping,
                    source_platform=self.source_platform,
                    source_application=SourceApplication.EVOLT_360,
                    extraction_method=extraction_method,
                    batch_id=batch_id,
                    raw_source_path=raw_path,
                    default_measurement_type="device_estimated",
                )
                if label_raw not in EVOLT_FIELD_LABEL_MAP and label not in EVOLT_FIELD_LABEL_MAP:
                    record.validation_messages.append(
                        f"unrecognized Evolt field label '{label_raw}': not in EVOLT_FIELD_LABEL_MAP, "
                        f"stored as '{metric_type}' pending manual mapping"
                    )
                    record.validation_status = "unverified"
                records.append(record)
            except (KeyError, ValueError, TypeError) as exc:
                errors.append(f"field[{i}] ('{label_raw}') rejected: {exc}")

        # Deterministic range + cross-field consistency checks, run
        # immediately so the review file reflects real findings rather
        # than raw dumps a human has to re-derive by hand.
        for record in records:
            range_result = check_range(record.metric_type, record.normalized_value)
            if range_result is not None:
                record.validation_status = range_result.severity
                record.validation_messages.append(range_result.detail)

        for finding in check_body_composition_group(records):
            for record in records:
                if record.metric_type in finding.metric_types:
                    record.validation_status = finding.severity
                    record.validation_messages.append(str(finding))

        return records, errors

    def _write_review_file(self, records: list[CanonicalHealthRecord], errors: list[str], raw_path: Path) -> None:
        review_dir = self.config.vault_subdir("17-IMPORT-LOGS")
        review_dir.mkdir(parents=True, exist_ok=True)
        today = date.today().isoformat()
        review_path = review_dir / f"evolt-import-review-{today}.md"

        lines = [
            "---",
            f"generated: {datetime.now().isoformat()}",
            f"raw_source_path: {raw_path}",
            "confirmation_status: UNCONFIRMED",
            "---",
            "",
            "# Evolt Import Review",
            "",
            "**Do not treat any value below as confirmed until checked against the original report.**",
            "",
            "| Label / metric_type | Value | Unit | Confidence source | Validation result | Confirmation |",
            "|---|---|---|---|---|---|",
        ]
        for r in records:
            confidence_source = "verified field mapping" if r.extraction_method == ExtractionMethod.VERIFIED_FIELD_MAPPING else "unmapped — needs review"
            lines.append(
                f"| {r.metric_type} | {r.normalized_value} | {r.normalized_unit} | {confidence_source} "
                f"| {r.validation_status} | UNCONFIRMED |"
            )
        if errors:
            lines += ["", "## Errors", ""]
            lines += [f"- {e}" for e in errors]

        review_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
