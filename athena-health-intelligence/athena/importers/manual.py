"""Manual entry: the only importer the vertical slice depends on to prove
the pipeline end-to-end without any external device or file.

The CLI (`athena import manual`) wraps `import_record` with interactive
prompts; `import_record` itself takes a plain dict so it is directly
testable and scriptable (`athena import manual --from-json path.json`).
"""

from __future__ import annotations

from athena.config import AthenaConfig
from athena.importers.base import ImportResult, new_batch_id, record_from_mapping
from athena.models.source import ExtractionMethod, SourceApplication, SourcePlatform


class ManualImporter:
    source_platform = SourcePlatform.MANUAL

    def __init__(self, config: AthenaConfig):
        self.config = config

    def import_record(self, mapping: dict) -> ImportResult:
        batch_id = new_batch_id("manual")
        errors: list[str] = []
        records = []
        try:
            record = record_from_mapping(
                mapping,
                source_platform=self.source_platform,
                source_application=SourceApplication.ATHENA_CLI,
                extraction_method=ExtractionMethod.MANUAL_ENTRY,
                batch_id=batch_id,
                raw_source_path=None,
                default_measurement_type="manual",
            )
            records.append(record)
        except (KeyError, ValueError, TypeError) as exc:
            errors.append(f"manual entry rejected: {exc}")
        return ImportResult(batch_id=batch_id, records=records, errors=errors, raw_source_path=None)
