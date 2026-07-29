"""Provenance is not a side note in ATHENA — it is required for every record.

CanonicalHealthRecord (see canonical.py) stores provenance fields flat,
per the ATHENA data-model spec (docs/data-model.md), rather than as a
nested object, so that they are first-class SQLite columns and can be
queried/filtered directly (e.g. "show me every questionable record that
came from evolt PDF extraction"). This module provides a single
`Provenance` container and `build_provenance()` factory so importers
build that bundle of fields in one place instead of repeating six
keyword arguments at every call site, then spread it into
CanonicalHealthRecord(**provenance.as_kwargs(), ...).
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel

from athena.models.source import ExtractionMethod, SourcePlatform


class Provenance(BaseModel):
    source_platform: str
    source_application: str | None = None
    source_device: str | None = None
    source_record_id: str | None = None
    extraction_method: str
    raw_source_path: str | None = None
    imported_at: datetime

    def as_kwargs(self) -> dict:
        return self.model_dump()


def build_provenance(
    *,
    source_platform: str,
    extraction_method: str = ExtractionMethod.MANUAL_ENTRY,
    source_application: str | None = None,
    source_device: str | None = None,
    source_record_id: str | None = None,
    raw_source_path: str | None = None,
    imported_at: datetime | None = None,
) -> Provenance:
    return Provenance(
        source_platform=source_platform,
        source_application=source_application,
        source_device=source_device,
        source_record_id=source_record_id,
        extraction_method=extraction_method,
        raw_source_path=raw_source_path,
        imported_at=imported_at or datetime.now(timezone.utc),
    )


__all__ = ["Provenance", "build_provenance", "SourcePlatform"]
