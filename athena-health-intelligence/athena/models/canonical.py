"""The single record type every ATHENA metric is stored as.

Field shape follows the ATHENA master spec (docs/data-model.md) verbatim:
provenance fields are flat on the record, not nested, so SQLite columns
map 1:1 and every field can be filtered on directly. This model only
enforces *structural* validity (types, required fields). Physiological
plausibility (e.g. "skeletal muscle can't exceed body weight") is
deliberately NOT a pydantic validator here — that lives in
athena/validation/, runs as an explicit separate step, and is allowed to
downgrade validation_status/confidence after construction without ever
mutating original_value. See athena/validation/consistency.py.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, field_validator

from athena.models.validation import DuplicateStatus, MeasurementType, ValidationStatus

TRANSFORMATION_VERSION = "1.0.0"

JsonValue = float | str | dict | None


class CanonicalHealthRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    metric_type: str

    start_time: datetime
    end_time: datetime | None = None
    timezone: str

    original_value: JsonValue
    original_unit: str | None = None

    normalized_value: JsonValue
    normalized_unit: str | None = None

    source_platform: str
    source_application: str | None = None
    source_device: str | None = None
    source_record_id: str | None = None
    extraction_method: str

    measurement_type: MeasurementType

    validation_status: ValidationStatus = "unverified"
    confidence: float = 0.0
    validation_messages: list[str] = Field(default_factory=list)

    raw_source_path: str | None = None
    imported_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    transformation_version: str = TRANSFORMATION_VERSION
    transformations: list[str] = Field(default_factory=list)

    duplicate_status: DuplicateStatus | None = None
    duplicate_of: str | None = None

    tags: list[str] = Field(default_factory=list)

    import_batch_id: str | None = None
    """Not in the original spec's field list, but every importer needs a
    way to group records that came from the same import run/scan session
    (e.g. all fields from one Evolt scan) for cross-field consistency
    checks and for the review-file / import-log exporters. Nullable so it
    never blocks a record from being constructed."""

    @field_validator("confidence")
    @classmethod
    def _confidence_in_range(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("confidence must be between 0.0 and 1.0")
        return v

    model_config = {"extra": "forbid"}
