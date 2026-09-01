# ATHENA Data Model

## CanonicalHealthRecord

Defined in `athena/models/canonical.py`; the authoritative machine-readable version is
generated from the pydantic model into `schemas/canonical-health-record.schema.json` (run
`python scripts/generate_schemas.py` after any model change — do not hand-edit the schema
file).

| Field | Meaning |
|---|---|
| `id` | UUID4, generated at construction |
| `metric_type` | See "Metric vocabulary" below |
| `start_time` / `end_time` | When the measurement occurred; `end_time` is null for point-in-time values |
| `timezone` | IANA zone name as reported by the source, e.g. `America/New_York` |
| `original_value` / `original_unit` | Exactly what the source reported — never mutated after construction |
| `normalized_value` / `normalized_unit` | ATHENA's canonical-unit form; may equal the original if already canonical, or be unchanged-but-flagged if no conversion is known (see `athena/importers/base.py::normalize_value`) |
| `source_platform` / `source_application` / `source_device` / `source_record_id` | Provenance — see `athena/models/source.py` for the known vocabulary |
| `extraction_method` | How `normalized_value` was derived (manual entry, structured JSON/CSV, verified field mapping, PDF extraction, Health Connect export, calculated) |
| `measurement_type` | One of `measured`, `device_estimated`, `calculated`, `manual`, `inferred`, `unverified` — required, closed vocabulary |
| `validation_status` | One of `valid`, `questionable`, `invalid`, `unverified` — set by `athena/validation/engine.py`, not by the importer |
| `confidence` | 0.0–1.0, deterministic and cap-based (see `athena/validation/engine.py`) |
| `validation_messages` | Human-readable findings, append-only |
| `raw_source_path` | Path to the immutable copy under `data/raw/<batch_id>/`; null for interactive manual entry |
| `imported_at` / `transformation_version` / `transformations` | When/how it entered ATHENA |
| `duplicate_status` / `duplicate_of` | Set by the deduplication engine; never set by an importer |
| `tags` | Free-form, importer- or user-supplied |
| `import_batch_id` | Groups records from the same import run/scan session for cross-field consistency checks and Obsidian import-log notes. Not in the master spec's literal field list, but required for the body-composition/calorie/sleep-stage group checks in `athena/validation/consistency.py` to know which records belong to the same scan. |

`validation_status == "valid"` means **"passed ATHENA's automated deterministic checks,"**
not **"a human confirmed it."** Those are deliberately different things. For Evolt scans
specifically, every record starts `measurement_type="device_estimated"` and the importer
also writes a `evolt-import-review-*.md` file with an explicit `UNCONFIRMED` status that
a human is expected to check against the original report — passing the automated checks
does not clear that expectation. See `athena/importers/evolt.py`.

## Metric vocabulary

`athena/models/metrics.py` is the single source of truth for which `metric_type` strings
ATHENA knows about and their canonical unit. It intentionally does not accept arbitrary
metric names silently — an importer that encounters an unrecognized metric still stores
the record (nothing is dropped) but flags it (`unknown metric_type '...': stored without
unit normalization`) rather than guessing at a unit conversion.

## Three data layers

- `data/raw/` — immutable copies of every imported source file, one subdirectory per
  import batch, named after the batch id. Nothing in this codebase opens these for
  writing after `preserve_raw_file()` creates them.
- `data/normalized/` — reserved for future use (e.g. cached normalized exports); no
  importer currently writes here directly, since normalization happens in-memory at
  import time and the result is persisted to SQLite, not to this directory.
- `data/derived/` — audit log (`audit_log.jsonl`), export manifests, and other generated
  artifacts that are not raw source data and not the canonical store itself.

## Why validation is separate from the schema

See `docs/architecture.md`'s "Design decisions" section. In one line: the schema enforces
*shape*, the validation engine enforces *plausibility*, and keeping them separate is what
lets ATHENA store an uncertain value instead of rejecting it outright.
