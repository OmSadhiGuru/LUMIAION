"""Vocabulary for where a canonical record came from.

These are plain string constants rather than a closed Literal/Enum on
purpose: new source platforms and extraction methods will be added as
integrations are built (see docs/source-capabilities.md for what is
actually confirmed working vs. planned), and a canonical record must be
able to name a source ATHENA does not fully support yet without the
model rejecting it outright. The KNOWN_* tuples exist for CLI validation
and documentation, not to gate what can be stored.
"""

from __future__ import annotations


class SourcePlatform:
    """Known values for CanonicalHealthRecord.source_platform."""

    MANUAL = "manual"
    EVOLT = "evolt"
    SAMSUNG_HEALTH = "samsung_health"
    HEALTH_CONNECT = "health_connect"
    STRAVA = "strava"
    SMARTHEALTH = "smarthealth"
    ATHENA_CALCULATED = "athena_calculated"


KNOWN_SOURCE_PLATFORMS = (
    SourcePlatform.MANUAL,
    SourcePlatform.EVOLT,
    SourcePlatform.SAMSUNG_HEALTH,
    SourcePlatform.HEALTH_CONNECT,
    SourcePlatform.STRAVA,
    SourcePlatform.SMARTHEALTH,
    SourcePlatform.ATHENA_CALCULATED,
)


class SourceApplication:
    """Known values for CanonicalHealthRecord.source_application."""

    ATHENA_CLI = "athena_cli"
    EVOLT_360 = "Evolt 360"
    SAMSUNG_HEALTH_APP = "Samsung Health"
    HEALTH_CONNECT_APP = "Health Connect"
    STRAVA_APP = "Strava"


class ExtractionMethod:
    """How the normalized_value was obtained from the original source."""

    MANUAL_ENTRY = "manual_entry"
    STRUCTURED_JSON = "structured_json"
    STRUCTURED_CSV = "structured_csv"
    VERIFIED_FIELD_MAPPING = "verified_field_mapping"
    PDF_EXTRACTION = "pdf_extraction"
    HEALTH_CONNECT_EXPORT = "health_connect_export"
    CALCULATED = "calculated"


KNOWN_EXTRACTION_METHODS = (
    ExtractionMethod.MANUAL_ENTRY,
    ExtractionMethod.STRUCTURED_JSON,
    ExtractionMethod.STRUCTURED_CSV,
    ExtractionMethod.VERIFIED_FIELD_MAPPING,
    ExtractionMethod.PDF_EXTRACTION,
    ExtractionMethod.HEALTH_CONNECT_EXPORT,
    ExtractionMethod.CALCULATED,
)
