"""Shared importer machinery: raw-file immutability, batch bookkeeping,
and the mapping->CanonicalHealthRecord construction every file-based
importer (manual, JSON, CSV, Evolt) funnels through.

Design constraint from the ATHENA rules: raw source files are
immutable. `preserve_raw_file` copies the source into data/raw/ under a
batch-scoped subdirectory and hashes it; nothing in this codebase is
allowed to open that copy for writing again.
"""

from __future__ import annotations

import shutil
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from athena.config import AthenaConfig
from athena.models.canonical import CanonicalHealthRecord
from athena.models.metrics import canonical_unit_for, is_known_metric
from athena.models.source import ExtractionMethod
from athena.security.audit_log import compute_sha256

# unit -> (target_unit, multiply-by) — deliberately small and explicit.
# Anything not listed here is either already canonical or gets flagged
# rather than silently guessed at.
_UNIT_CONVERSIONS: dict[str, tuple[str, float]] = {
    "lb": ("kg", 0.45359237),
    "lbs": ("kg", 0.45359237),
    "mL": ("L", 0.001),
    "ml": ("L", 0.001),
}


@dataclass
class ImportResult:
    batch_id: str
    records: list[CanonicalHealthRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    raw_source_path: str | None = None

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0


def new_batch_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:8]}"


def preserve_raw_file(config: AthenaConfig, source_path: str | Path, batch_id: str) -> tuple[Path, str]:
    """Copy `source_path` into data/raw/<batch_id>/ and return (path, sha256).
    The original file is never modified or moved.
    """
    source_path = Path(source_path)
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")
    dest_dir = config.raw_dir / batch_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / source_path.name
    shutil.copy2(source_path, dest_path)
    return dest_path, compute_sha256(dest_path)


def normalize_value(metric_type: str, value, unit: str | None) -> tuple[object, str | None, list[str]]:
    """Best-effort normalization into the metric's canonical unit.

    Returns (normalized_value, normalized_unit, warnings). Never fabricates
    a conversion it isn't sure of — an unrecognized unit is passed through
    unchanged with a warning rather than silently coerced.
    """
    warnings: list[str] = []
    target_unit = canonical_unit_for(metric_type)

    if not is_known_metric(metric_type):
        warnings.append(f"unknown metric_type '{metric_type}': stored without unit normalization")
        return value, unit, warnings

    if unit is None:
        warnings.append(f"missing original_unit for '{metric_type}': cannot confirm normalization")
        return value, target_unit, warnings

    if unit == target_unit:
        return value, target_unit, warnings

    if unit in _UNIT_CONVERSIONS and isinstance(value, (int, float)):
        conv_target, factor = _UNIT_CONVERSIONS[unit]
        if conv_target == target_unit:
            return round(value * factor, 6), target_unit, warnings

    warnings.append(
        f"no known conversion from '{unit}' to canonical unit '{target_unit}' for '{metric_type}': "
        f"stored as-is, requires manual verification"
    )
    return value, unit, warnings


def record_from_mapping(
    mapping: dict,
    *,
    source_platform: str,
    source_application: str | None,
    extraction_method: str,
    batch_id: str,
    raw_source_path: str | None,
    default_measurement_type: str,
) -> CanonicalHealthRecord:
    """Build one CanonicalHealthRecord from a flat field mapping shared by
    manual/json/csv/evolt importers. `mapping` must supply at least
    metric_type, value, start_time, timezone.
    """
    metric_type = mapping["metric_type"]
    value = mapping["value"]
    unit = mapping.get("unit")
    source_platform = mapping.get("source_platform", source_platform)
    source_application = mapping.get("source_application", source_application)
    extraction_method = mapping.get("extraction_method", extraction_method)

    normalized_value, normalized_unit, norm_warnings = normalize_value(metric_type, value, unit)

    start_time = mapping["start_time"]
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    end_time = mapping.get("end_time")
    if isinstance(end_time, str):
        end_time = datetime.fromisoformat(end_time)

    validation_status = "unverified"
    messages = list(norm_warnings)
    if mapping.get("value") is None:
        validation_status = "unverified"
        messages.append("value is missing at import time; stored as missing, not estimated")

    return CanonicalHealthRecord(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        timezone=mapping.get("timezone", "UTC"),
        original_value=value,
        original_unit=unit,
        normalized_value=normalized_value,
        normalized_unit=normalized_unit,
        source_platform=source_platform,
        source_application=source_application,
        source_device=mapping.get("source_device"),
        source_record_id=mapping.get("source_record_id"),
        extraction_method=extraction_method,
        measurement_type=mapping.get("measurement_type", default_measurement_type),
        validation_status=validation_status,
        confidence=0.0,
        validation_messages=messages,
        raw_source_path=raw_source_path,
        transformations=[f"imported via {extraction_method}"],
        tags=mapping.get("tags", []),
        import_batch_id=batch_id,
    )


class Importer(ABC):
    """Base for file/manual-entry based importers."""

    source_platform: str
    default_extraction_method: str = ExtractionMethod.STRUCTURED_JSON

    def __init__(self, config: AthenaConfig):
        self.config = config

    @abstractmethod
    def import_source(self, source) -> ImportResult:
        ...


class HealthSourceAdapter(ABC):
    """Base for pull-based external API sources (as opposed to file-based
    Importers above). An adapter authenticates against a remote service
    and pulls records on demand; an Importer reads a local file or manual
    input. See athena/adapters/strava.py for the (unimplemented) example.
    """

    source_platform: str

    @abstractmethod
    def authenticate(self) -> None:
        ...

    @abstractmethod
    def fetch_records(self, *, start: datetime, end: datetime) -> ImportResult:
        ...
